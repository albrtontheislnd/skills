# findings.json schema

This is the file Claude writes by hand after doing live research
(`web_search` / `web_fetch`) for the qualitative parts of the report. Pass
its path to `build_report.py --findings`. Numbers/dates that already exist
in `raw_market_data.json` (from `fetch_gold_data.py`) do not need to be
repeated here — `build_report.py` recomputes all price statistics itself.

```json
{
  "as_of_date": "2026-08-14",

  "timeline": [
    {
      "date": "2026-08-03",
      "movement": "+1.2%",
      "driver": "Soft NFP print raised Fed rate-cut odds"
    }
  ],

  "key_drivers": [
    {
      "factor": "Federal Reserve communications",
      "direction": "Bullish",
      "explanation": "One or two sentences on how this factor moved gold."
    }
  ],

  "technical": {
    "momentum": "Short summary",
    "trend": "Short summary",
    "support": "$2,420",
    "resistance": "$2,470",
    "notes": "Optional: breakouts, pullbacks, chart patterns"
  },

  "sentiment": {
    "summary": "1-2 sentence consensus read",
    "facts": ["Verifiable, sourced statements"],
    "expectations": ["What the market is currently pricing in"],
    "opinions": ["Named or attributed analyst/trader views"]
  },

  "investor_recommendation": [
    {
      "investor_type": "Long-term investor (no gold exposure)",
      "recommendation": "Buy",
      "rationale": "Evidence-based judgement tied to the report's data and facts"
    },
    {
      "investor_type": "Existing gold holder",
      "recommendation": "Hold",
      "rationale": "Evidence-based judgement tied to the report's data and facts"
    },
    {
      "investor_type": "Short-term trader",
      "recommendation": "Sell",
      "rationale": "Evidence-based judgement tied to the report's data and facts"
    },
    {
      "investor_type": "New trader / speculative",
      "recommendation": "Hold",
      "rationale": "Evidence-based judgement tied to the report's data and facts"
    }
  ],

  "executive_summary": [
    "3 to 5 bullets total",
    "Each one a single, concrete takeaway",
    "..."
  ],

  "sources": [
    {"name": "Kitco", "url": "https://www.kitco.com/..."}
  ]
}
```

## Field notes

- **timeline**: chronological, oldest first. Every entry's `date` should come
  from `raw_market_data.json`'s `candidate_movements` list (the days whose
  day-over-day move exceeded the threshold) — don't invent dates, and don't
  skip a candidate date without at least checking what caused it.
- **key_drivers**: `direction` must be exactly `"Bullish"`, `"Bearish"`, or
  `"Neutral"` — `build_report.py` doesn't validate this, but the output
  format depends on it reading cleanly.
- **sentiment**: keep `facts` / `expectations` / `opinions` genuinely
  distinct — don't let an analyst's opinion slide into `facts`.
- **investor_recommendation**: provide exactly one entry for each of the four
  investor types: `Long-term investor (no gold exposure)`, `Existing gold
  holder`, `Short-term trader`, and `New trader / speculative`. The
  `recommendation` must be exactly `"Buy"`, `"Hold"`, or `"Sell"`. Each
  `rationale` must connect the judgement to current report data and sourced
  facts, distinguish judgement from fact, and avoid individualized advice.
- **sources**: list every source actually used for the qualitative content
  (prices are already attributed via `raw_market_data.json`'s `source`
  field). Only include sources you actually fetched or searched — never
  fabricate a URL.
- Any field you can't fill in from real research: omit it or leave the list
  empty rather than filling in a plausible-sounding placeholder.
