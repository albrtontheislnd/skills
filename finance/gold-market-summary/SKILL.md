---
name: gold-market-summary
description: Analyze and summarize global gold price movements over the past 14 days using live market data, deterministic price-stat calculations, and a timestamped Markdown report saved to the gold-price-reports folder. Use this whenever the user asks for a gold market update, briefing, or summary; asks what happened to gold/XAU-USD recently or why it moved; or asks about current gold price trends, sentiment, or technicals — even if they don't say "report" explicitly.
version: 2.0.0
author: Quang Tu Do
license: MIT

metadata:
  hermes:
    category: finance
    tags:
      - gold
      - xauusd
      - commodities
      - macroeconomics
      - investing
      - market-analysis
      - precious-metals
      - finance
      - report-generation
    requires_toolsets: [web]              # Hide if the web toolset is NOT active
    requires_tools: [web_search, web_extract, bash]  # Needs live search/fetch AND the ability to run the bundled scripts
    fallback_for_toolsets: [browser]      # Hide if the browser toolset IS active
    fallback_for_tools: [browser_navigate] # Hide if browser_navigate IS available
---

# Gold Market Summary

## Purpose

Produce an objective, data-driven summary of **global gold price movements
during the previous 14 calendar days** using **live data retrieved at
execution time**, and save it as a timestamped Markdown file.

This skill is intended for investment research, market monitoring, and
macroeconomic analysis.

## When to Use

Use this skill whenever the user asks things like:

- Summarize gold prices over the last two weeks.
- What happened to gold recently?
- Explain the latest movements in XAU/USD.
- Why did gold rise (or fall) recently?
- Provide a market update / briefing on gold.
- Analyze current gold market sentiment.

## Bundled Resources

```
gold-market-summary/
├── SKILL.md
├── scripts/
│   ├── fetch_gold_data.py   -- deterministic: pulls a live daily XAU/USD
│   │                            series and computes price stats + flags
│   │                            candidate "movement days" to research
│   └── build_report.py      -- deterministic: recomputes all price stats
│                                from raw data and renders + saves the final
│                                timestamped Markdown report
└── references/
    └── report_schema.md     -- full findings.json schema + field notes
```

**Why two scripts, not one LLM-written report:** every number in this report
(spot price, % change, high, low, trend) is arithmetic that should never be
left to the model to compute or recall. The scripts own all arithmetic and
file I/O; The agent owns the research (via `web_search` / `web_extract`) and the
narrative (drivers, technicals, sentiment).

## Core Principles

### Always use live information

Never answer using model pretraining alone. Retrieve current market
information before beginning the analysis. If live data cannot be
retrieved by any means, explicitly state this limitation instead of
generating estimates.

### Time Window

Analyze only: **Current Date − 14 calendar days → Current Date**. Do not
include older events unless necessary to explain recent price action.

### Preferred Information Sources

Prioritize authoritative financial sources:
- LBMA
- CME Group
- Kitco
- TradingView
- Bloomberg
- Reuters
- CNBC
- Financial Times
- Investing.com
- MarketWatch
- World Gold Council
- Federal Reserve releases
- U.S. Bureau of Labor Statistics
- U.S. Treasury
- FRED

---

## Workspace and output rules

This skill must obey the workspace rules in `.docs/agent-instructions.md`.
Resolve the workspace root from the process working directory (`os.getcwd()`),
not from the directory containing this skill. Before creating any directory or
file, reject the run if the resolved workspace path contains both `<` and `>`
as an unresolved placeholder.

Use `gold-price-reports` as this skill's dedicated output subfolder at the
workspace root. This is the skill's suggested output-subfolder name and is
already fixed by its report format; do not create a folder under
`finance/gold-market-summary/`. Create the workspace-root subfolder only after
workspace validation succeeds. Keep the report, raw market data, findings,
and all other execution artifacts in that folder. Preserve existing reports
and never overwrite them.

Every command below must use these workspace-root paths (replace
`<workspace>` with the validated process working directory):

- `<workspace>/gold-price-reports/raw_market_data.json`
- `<workspace>/gold-price-reports/findings.json`

Do not use bare filenames for generated artifacts, and do not write generated
files into this skill's source directory or any of its subdirectories.

### Step 1 — Fetch live price data (deterministic)

```bash
python3 finance/gold-market-summary/scripts/fetch_gold_data.py \
  --days 14 --threshold 0.5 \
  --out "<workspace>/gold-price-reports/raw_market_data.json"
```

This pulls a daily XAU/USD series from Stooq (free, no API key) and writes
JSON containing: current price, price 14 days ago, period high/low, % change,
trend, the full daily series, and a `candidate_movements` list — the specific
dates whose day-over-day move exceeded the threshold, which need a
researched catalyst.

**If the script fails** (e.g. no network access to Stooq in this sandbox):
gather the same fields yourself via `web_search` / `web_extract` against the
preferred sources above (current spot, price ~14 days ago, period high/low,
and enough daily closes to identify big-move days), and hand-write a JSON
file with the same shape — at minimum a `daily_series` list of
`{"date": "YYYY-MM-DD", "close": <float>, "high": <float>, "low": <float>}`
entries. Save it as `<workspace>/gold-price-reports/raw_market_data.json` and continue
to Step 2. Do not
proceed to Step 4 with fabricated numbers — if truly no live data is
obtainable, say so in the final report instead.

### Step 2 — Research the qualitative content

Using `web_search` / `web_extract`:

1. **Timeline** — for each date in `candidate_movements`, find the actual
   news catalyst (Fed comments, CPI print, geopolitical event, etc.).
2. **Key drivers** — Federal Reserve communications, interest-rate
   expectations, Treasury yields, USD Index (DXY), CPI, PPI, employment
   reports, GDP, central bank purchases, ETF flows, geopolitical events, risk
   sentiment, major economic releases. Mark each Bullish / Bearish / Neutral.
3. **Technical perspective** — momentum, trend, support, resistance,
   breakouts/pullbacks, chart patterns (concise, minimal jargon).
4. **Market sentiment** — current consensus among analysts, institutional
   investors, precious-metals traders. Keep facts, expectations, and
   opinions clearly distinguished.
5. **Investor's recommendation** — provide a general, evidence-based
   `Buy`, `Hold`, or `Sell` judgement for each of these investor types:
   `Long-term investor (no gold exposure)`, `Existing gold holder`,
   `Short-term trader`, and `New trader / speculative`. Tie every rationale
   to the current price data, technicals, drivers, sentiment, and sourced
   facts. Clearly distinguish judgement from fact; do not present this as
   individualized financial advice.
6. **Executive summary** — 3–5 bullets on the most important developments.

Write all of this into `<workspace>/gold-price-reports/findings.json`
following the schema in `finance/gold-market-summary/references/report_schema.md`.

### Step 3 — Build and save the report (deterministic)

A `SKILL.md` is just text injected into the agent's context — there's no
process env to read, so this doesn't rely on any environment variable.
Workspace resolution is just the current working directory:

```bash
python3 finance/gold-market-summary/scripts/build_report.py \
  --raw-data "<workspace>/gold-price-reports/raw_market_data.json" \
  --findings "<workspace>/gold-price-reports/findings.json" \
  --workspace "<workspace>"
```

Pass the validated workspace root explicitly as shown above. If
`--workspace` is omitted, `build_report.py` defaults to `os.getcwd()`. The
script refuses to run if the resolved workspace path still looks like an
unfilled placeholder (contains `<` and `>`).

The script:
- Recomputes every price statistic itself from `raw_market_data.json`'s
  `daily_series` (never trusts pre-computed numbers, even its own).
- Renders the full Markdown report per the Output Format below.
- Saves it to **`<workspace>/gold-price-reports/gold-market-summary-<UTC
  timestamp>.md`**, creating the folder if needed.
- Prints the full saved path on success — report that path back to the user.

**Output location is fixed:** every file this skill produces, including
intermediate JSON and the final report, must land in the workspace-root
`gold-price-reports` subfolder, never elsewhere. **Every run gets its own timestamped file** — never overwrite a
previous report.

### Step 4 — Verify before reporting back

Before telling the user it's done, confirm:

- ✓ Live market data was retrieved (or its absence was explicitly disclosed).
- ✓ The analysis covers only the previous 14 days.
- ✓ Numerical values are internally consistent (build_report.py guarantees
  this, since it recomputes them — but sanity-check the rendered file).
- ✓ Every `candidate_movements` date got a researched catalyst in the
  timeline, not a guess.
- ✓ Facts are distinguished from opinions in the Sentiment section.
- ✓ The Investor's Recommendation table contains all four investor types,
  uses only Buy/Hold/Sell, and ties each judgement to current evidence.
- ✓ The file was written under `<workspace>/gold-price-reports/`.
- ✓ Sources are cited in `findings.json`'s `sources` list.

---

## Output Format

(This is what `build_report.py` renders — shown here for reference, not to
be reproduced by hand.)

```
# Gold Market Summary (Last 14 Days)

## Price Overview
- Current Spot Price
- 14-Day Change
- Highest Price
- Lowest Price
- Overall Trend

## Timeline
| Date | Price Movement | Main Driver |

## Key Drivers
(one subsection per factor, with Bullish/Bearish/Neutral)

## Technical Perspective
- Momentum / Trend / Support / Resistance

## Market Sentiment
(summary + Facts / Market Expectations / Analyst Opinions)

## Investor's Recommendation
_General market analysis, not individualized financial advice._
| Investor Type | Recommendation | Evidence-Based Rationale |
|---|---|---|
| Long-term investor (no gold exposure) | Buy / Hold / Sell | Data-based rationale |
| Existing gold holder | Buy / Hold / Sell | Data-based rationale |
| Short-term trader | Buy / Hold / Sell | Data-based rationale |
| New trader / speculative | Buy / Hold / Sell | Data-based rationale |

## Executive Summary
- 3-5 bullets

## Data Notes            (only if raw data had errors/gaps)
## Sources                (only if findings.json listed any)
```

## Style Guidelines

Write in a professional, objective tone with concise paragraphs and
evidence-based analysis. Avoid: speculation presented as fact, unsupported
predictions, hallucinated prices, and using pretrained knowledge when
current data is available. Whenever numerical values are available: include
approximate prices, include percentage changes, mention the reporting
currency (USD), and clearly flag when a value is approximate.

## Troubleshooting

- **`fetch_gold_data.py` can't reach Stooq** → see the fallback in Step 1.
- **`build_report.py` errors on `--workspace`** → the resolved path (either
  what you passed, or `os.getcwd()`) looks like a literal placeholder such
  as `<workspace>`; run the script from the real workspace directory, or
  pass `--workspace` with an actual path.
- **Fewer than 14 days of data returned** → the script warns on stderr but
  still proceeds with what it has; mention the shorter window in the report
  if it's more than a day or two short.
- **No candidate_movements found** → gold was unusually quiet over the
  window; say so plainly in the Timeline/Executive Summary rather than
  inventing movement.
