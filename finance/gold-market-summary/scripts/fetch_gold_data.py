#!/usr/bin/env python3
"""
fetch_gold_data.py

Deterministic data-fetching helper for the gold-market-summary skill.

Pulls a daily XAU/USD price series covering the last N days (default 14 + a
few days of buffer for weekends/holidays) from a free, no-API-key source
(Stooq), then computes:

  - current spot price / as-of date
  - price N days ago
  - period high / low (with dates)
  - percentage change
  - a simple trend label (up / down / sideways)
  - the full daily series
  - "candidate movement" days -- days whose day-over-day % change exceeds a
    threshold, which Claude should research (via web_search / web_fetch) to
    find the news catalyst behind each one before building the timeline.

This script does NOT explain *why* the price moved -- that requires live web
research and is intentionally left to Claude. It only does the arithmetic
that should never be hallucinated.

Usage:
    python3 fetch_gold_data.py [--days 14] [--threshold 0.5] [--out FILE]

    If --out is omitted, JSON is printed to stdout.

Fallback:
    If network access to Stooq is unavailable in the current sandbox
    (common in restricted environments), this script exits with a non-zero
    code and a clear error on stderr. In that case, Claude should instead
    gather the same fields (current price, 14-day-ago price, high, low,
    daily closes) via web_search / web_fetch against sources such as Kitco,
    TradingView, or the World Gold Council, and hand-build the JSON object
    described in references/report_schema.md, then pass it straight to
    build_report.py.
"""

import argparse
import csv
import io
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

STOOQ_URL = "https://stooq.com/q/d/l/?s=xauusd&i=d"
USER_AGENT = "gold-market-summary-skill/2.0 (+deterministic data fetch)"


def fetch_csv(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError) as e:
        raise RuntimeError(
            f"Could not reach {url} ({e}). This sandbox may not have network "
            "access to Stooq. Fall back to web_search/web_fetch for the same "
            "data points -- see the docstring in this file."
        ) from e


def parse_series(csv_text: str):
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = []
    for row in reader:
        try:
            rows.append(
                {
                    "date": row["Date"],
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                }
            )
        except (KeyError, ValueError):
            continue
    rows.sort(key=lambda r: r["date"])
    if not rows:
        raise RuntimeError(
            "Fetched data but couldn't parse any rows. Stooq's response "
            "format may have changed -- inspect the raw response."
        )
    return rows


def trend_label(pct_change: float) -> str:
    if pct_change > 1.0:
        return "up"
    if pct_change < -1.0:
        return "down"
    return "sideways"


def build_stats(rows, days: int, threshold: float):
    window = rows[-(days + 1):] if len(rows) > days else rows
    for i in range(1, len(window)):
        prev_close = window[i - 1]["close"]
        curr_close = window[i]["close"]
        window[i]["pct_change_from_prev"] = round(
            (curr_close - prev_close) / prev_close * 100, 3
        )
    window[0]["pct_change_from_prev"] = None

    current = window[-1]
    baseline = window[0]
    pct_change = round(
        (current["close"] - baseline["close"]) / baseline["close"] * 100, 3
    )
    period_high = max(window, key=lambda r: r["high"])
    period_low = min(window, key=lambda r: r["low"])

    candidate_movements = [
        {
            "date": r["date"],
            "close": r["close"],
            "pct_change_from_prev": r["pct_change_from_prev"],
        }
        for r in window[1:]
        if r["pct_change_from_prev"] is not None
        and abs(r["pct_change_from_prev"]) >= threshold
    ]

    return {
        "source": "stooq.com (XAUUSD, daily)",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "window_days_requested": days,
        "as_of_date": current["date"],
        "current_price": current["close"],
        "price_n_days_ago": baseline["close"],
        "baseline_date": baseline["date"],
        "period_high": {"price": period_high["high"], "date": period_high["date"]},
        "period_low": {"price": period_low["low"], "date": period_low["date"]},
        "pct_change": pct_change,
        "trend": trend_label(pct_change),
        "daily_series": window,
        "candidate_movements": candidate_movements,
        "note": (
            "candidate_movements lists days whose day-over-day change exceeded "
            f"the {threshold}% threshold. Research each date's news catalyst "
            "via web_search/web_fetch before writing the Timeline section -- "
            "do not invent catalysts."
        ),
    }


def validate_workspace(workspace: str) -> Path:
    if "<" in workspace and ">" in workspace:
        raise ValueError(
            "Refusing to run: the workspace path is an unfilled placeholder."
        )
    return Path(workspace).resolve()


def output_path_within_workspace(path: str, workspace: Path) -> Path:
    candidate = Path(path).resolve()
    output_dir = (workspace / "gold-price-reports").resolve()
    try:
        candidate.relative_to(output_dir)
    except ValueError as exc:
        raise ValueError(
            f"--out must be inside the workspace output folder {output_dir}, "
            "never the skill source directory or another location."
        ) from exc
    return candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=14, help="Lookback window in calendar days (default 14)")
    parser.add_argument("--threshold", type=float, default=0.5, help="Day-over-day %% move threshold to flag as a candidate timeline entry (default 0.5)")
    parser.add_argument("--out", type=str, default=None, help="Optional output path; when provided it must be inside <workspace>/gold-price-reports/")
    parser.add_argument("--workspace", type=str, default=None, help="Workspace root; defaults to os.getcwd()")
    args = parser.parse_args()

    workspace = validate_workspace(args.workspace or os.getcwd())
    output_path = output_path_within_workspace(args.out, workspace) if args.out else None

    csv_text = fetch_csv(STOOQ_URL)
    rows = parse_series(csv_text)

    oldest = datetime.strptime(rows[0]["date"], "%Y-%m-%d")
    newest = datetime.strptime(rows[-1]["date"], "%Y-%m-%d")
    if (newest - oldest) < timedelta(days=args.days - 3):
        sys.stderr.write(
            "Warning: fetched series is shorter than the requested window; "
            "results may be based on fewer than the requested days.\n"
        )

    stats = build_stats(rows, args.days, args.threshold)
    output = json.dumps(stats, indent=2)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            f.write(output)
        sys.stderr.write(f"Wrote price data to {output_path}\n")
    else:
        print(output)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError) as e:
        sys.stderr.write(f"ERROR: {e}\n")
        sys.exit(1)
