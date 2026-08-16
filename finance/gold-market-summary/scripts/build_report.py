#!/usr/bin/env python3
"""
build_report.py

Deterministic report-assembly helper for the gold-market-summary skill.

Takes:
  1. raw-data JSON -- either the exact JSON produced by fetch_gold_data.py,
     or a hand-built equivalent (see below) if that script couldn't reach
     the network and Claude sourced the numbers via web_search / web_fetch
     instead. Ground truth for every number in the report; never re-typed
     or "recalled" by the model. Must contain a "daily_series" list of
     {"date": "YYYY-MM-DD", "close": <float>, "high": <float>, "low": <float>}
     entries (open is optional). This script recomputes the 14-day change,
     period high/low, and trend itself from that series -- it never trusts
     precomputed stats, even the ones fetch_gold_data.py includes for
     convenience -- so arithmetic is never left to the model.
  2. findings.json -- a structured document Claude fills in after doing
     web_search / web_fetch research for the qualitative parts (timeline,
      qualitative parts (timeline, key drivers, technical read, sentiment,
      investor recommendations, executive summary, sources).
     See the schema below. Use raw-data's "candidate_movements" (if present)
     to know which dates need a researched catalyst for the Timeline.

Renders the final Markdown using the Output Format defined in SKILL.md,
and writes it to:

    <workspace>/gold-price-reports/gold-market-summary-<UTC timestamp>.md

Usage:
    python3 build_report.py \\
        --raw-data /path/to/workspace/gold-price-reports/raw_market_data.json \\
        --findings /path/to/workspace/gold-price-reports/findings.json \\
        --workspace /path/to/workspace

    If --workspace is omitted, it defaults to the current working directory
    (os.getcwd()). Since a SKILL.md is just text injected into the agent's
    context -- there's no process to read environment variables from -- the
    agent should either `cd` into the workspace directory before running
    this script, or pass --workspace explicitly if the runtime exposes the
    workspace path some other way (e.g. a `host.state.cwd` value).

Prints the full output path on success (that's what should be reported
back to the user).

--------------------------------------------------------------------
findings.json schema
--------------------------------------------------------------------
{
  "as_of_date": "2026-08-14",                 // ISO date the report covers

  "timeline": [                               // chronological, oldest first
    {"date": "2026-08-03", "movement": "+1.2%", "driver": "Soft NFP print"}
  ],

  "key_drivers": [
    {
      "factor": "Federal Reserve communications",
      "direction": "Bullish",                 // Bullish | Bearish | Neutral
      "explanation": "..."
    }
  ],

  "technical": {
    "momentum": "...",
    "trend": "...",
    "support": "...",
    "resistance": "...",
    "notes": "..."                            // optional
  },

  "sentiment": {
    "summary": "...",
    "facts": ["..."],                         // optional
    "expectations": ["..."],                  // optional
    "opinions": ["..."]                       // optional
  },

  "investor_recommendation": [
    {
      "investor_type": "Long-term investor (no gold exposure)",
      "recommendation": "Buy",                 // Buy | Hold | Sell
      "rationale": "Evidence-based judgement tied to this report's data"
    }
  ],

  "executive_summary": ["...", "...", "...", "...", "..."],   // 3-5 bullets

  "sources": [
    {"name": "Kitco", "url": "https://..."}
  ]
}
--------------------------------------------------------------------
"""

import argparse
import json
import os
from datetime import datetime, timezone


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_price_stats(gold_series):
    """All arithmetic lives here, not in the model's head."""
    if not gold_series:
        return None
    ordered = sorted(gold_series, key=lambda r: r["date"])
    current = ordered[-1]
    start = ordered[0]
    highest = max(ordered, key=lambda r: r.get("high", r["close"]))
    lowest = min(ordered, key=lambda r: r.get("low", r["close"]))
    pct_change = (
        ((current["close"] - start["close"]) / start["close"]) * 100
        if start["close"]
        else None
    )

    if pct_change is None:
        trend = "Unknown"
    elif pct_change > 0.5:
        trend = "Up"
    elif pct_change < -0.5:
        trend = "Down"
    else:
        trend = "Flat / range-bound"

    return {
        "current_price": current["close"],
        "current_date": current["date"],
        "period_start_price": start["close"],
        "period_start_date": start["date"],
        "pct_change": pct_change,
        "highest": highest,
        "lowest": lowest,
        "trend": trend,
    }


def fmt_price(value):
    return f"${value:,.2f}" if isinstance(value, (int, float)) else "N/A"


def fmt_pct(value):
    return f"{value:+.2f}%" if isinstance(value, (int, float)) else "N/A"


def render_markdown(raw_data, findings, stats):
    lookback = raw_data.get("window_days_requested", raw_data.get("lookback_days", 14))
    lines = []
    lines.append(f"# Gold Market Summary (Last {lookback} Days)")
    lines.append("")
    as_of = findings.get("as_of_date") or (stats["current_date"] if stats else "N/A")
    lines.append(
        f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} "
        f"\u00b7 covers through {as_of}_"
    )
    lines.append("")

    lines.append("## Price Overview")
    lines.append("")
    if stats:
        lines.append(f"- **Current Spot Price:** {fmt_price(stats['current_price'])} (as of {stats['current_date']})")
        lines.append(
            f"- **{lookback}-Day Change:** {fmt_pct(stats['pct_change'])} "
            f"(from {fmt_price(stats['period_start_price'])} on {stats['period_start_date']})"
        )
        lines.append(f"- **Highest Price:** {fmt_price(stats['highest'].get('high', stats['highest']['close']))} ({stats['highest']['date']})")
        lines.append(f"- **Lowest Price:** {fmt_price(stats['lowest'].get('low', stats['lowest']['close']))} ({stats['lowest']['date']})")
        lines.append(f"- **Overall Trend:** {stats['trend']}")
    else:
        lines.append("- \u26a0\ufe0f Live price data could not be retrieved. Numbers are omitted rather than estimated.")
    lines.append("")
    lines.append(
        "All prices in USD. Figures are sourced from live market data at generation "
        "time; treat intraday moves after generation as approximate."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Timeline")
    lines.append("")
    lines.append("| Date | Price Movement | Main Driver |")
    lines.append("|------|----------------|-------------|")
    for row in findings.get("timeline", []):
        lines.append(f"| {row.get('date', '')} | {row.get('movement', '')} | {row.get('driver', '')} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Key Drivers")
    lines.append("")
    for d in findings.get("key_drivers", []):
        lines.append(f"**{d.get('factor', '')} \u2014 {d.get('direction', 'Neutral')}**")
        lines.append("")
        lines.append(d.get("explanation", ""))
        lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Technical Perspective")
    lines.append("")
    tech = findings.get("technical", {})
    lines.append(f"- **Momentum:** {tech.get('momentum', 'N/A')}")
    lines.append(f"- **Trend:** {tech.get('trend', 'N/A')}")
    lines.append(f"- **Support:** {tech.get('support', 'N/A')}")
    lines.append(f"- **Resistance:** {tech.get('resistance', 'N/A')}")
    if tech.get("notes"):
        lines.append(f"- **Notes:** {tech['notes']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Market Sentiment")
    lines.append("")
    sentiment = findings.get("sentiment", {})
    lines.append(sentiment.get("summary", ""))
    lines.append("")
    if sentiment.get("facts"):
        lines.append("**Facts:**")
        for f in sentiment["facts"]:
            lines.append(f"- {f}")
        lines.append("")
    if sentiment.get("expectations"):
        lines.append("**Market Expectations:**")
        for e in sentiment["expectations"]:
            lines.append(f"- {e}")
        lines.append("")
    if sentiment.get("opinions"):
        lines.append("**Analyst Opinions:**")
        for o in sentiment["opinions"]:
            lines.append(f"- {o}")
        lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Investor's Recommendation")
    lines.append("")
    lines.append(
        "The following are general, evidence-based judgements from this "
        "14-day market analysis, not individualized financial advice. "
        "Investors should consider their objectives, risk tolerance, time "
        "horizon, and position size before acting."
    )
    lines.append("")
    lines.append("| Investor Type | Recommendation | Evidence-Based Rationale |")
    lines.append("|---|---|---|")
    recommendations = {
        row.get("investor_type"): row
        for row in findings.get("investor_recommendation", [])
        if isinstance(row, dict)
    }
    investor_types = [
        "Long-term investor (no gold exposure)",
        "Existing gold holder",
        "Short-term trader",
        "New trader / speculative",
    ]
    for investor_type in investor_types:
        row = recommendations.get(investor_type, {})
        lines.append(
            f"| {investor_type} | {row.get('recommendation', 'N/A')} "
            f"| {row.get('rationale', 'No evidence-based recommendation provided.')} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Executive Summary")
    lines.append("")
    for bullet in findings.get("executive_summary", []):
        lines.append(f"- {bullet}")
    lines.append("")

    if raw_data.get("errors"):
        lines.append("---")
        lines.append("")
        lines.append("## Data Notes")
        lines.append("")
        lines.append("Issues encountered while fetching live data (disclosed rather than papered over):")
        lines.append("")
        for err in raw_data["errors"]:
            lines.append(f"- {err}")
        lines.append("")

    if findings.get("sources"):
        lines.append("---")
        lines.append("")
        lines.append("## Sources")
        lines.append("")
        for s in findings["sources"]:
            name = s.get("name", s.get("url", "source"))
            url = s.get("url", "")
            lines.append(f"- [{name}]({url})" if url else f"- {name}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Assemble the gold market summary Markdown report.")
    parser.add_argument("--raw-data", required=True, help="Path to JSON produced by fetch_gold_data.py")
    parser.add_argument("--findings", required=True, help="Path to findings.json (see module docstring for schema)")
    parser.add_argument(
        "--workspace",
        default=None,
        help=(
            "Workspace directory to write into. Report is written to "
            "<workspace>/gold-price-reports/. If omitted, defaults to the "
            "current working directory (os.getcwd()) -- the agent should "
            "either run this script from the workspace directory, or pass "
            "--workspace explicitly with the real path (e.g. from "
            "host.state.cwd or wherever the runtime exposes it)."
        ),
    )
    args = parser.parse_args()

    workspace = args.workspace or os.getcwd()
    if "<" in workspace and ">" in workspace:
        raise SystemExit(
            f"--workspace resolved to a literal placeholder ({workspace!r}). "
            "Pass --workspace /real/path, or run this script from the "
            "actual workspace directory so os.getcwd() resolves correctly."
        )

    raw_data = load_json(args.raw_data)
    findings = load_json(args.findings)

    series = raw_data.get("daily_series") or raw_data.get("gold_xauusd") or []
    stats = compute_price_stats(series)
    markdown = render_markdown(raw_data, findings, stats)

    out_dir = os.path.join(workspace, "gold-price-reports")
    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_path = os.path.join(out_dir, f"gold-market-summary-{timestamp}.md")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(out_path)


if __name__ == "__main__":
    main()
