---
name: apac-econ-tracker
description: Use this skill whenever the user wants a daily or periodic briefing on Asia-Pacific (APAC) economics, finance, trade, labor markets, or macro data — including requests like "what's happening in Asian markets today," "give me my APAC econ update," "check the data calendar for this week," "any Vietnam trade news," or "summarize APAC central bank moves." Also use it to build, refresh, or extend a curated source list / RSS feed set for APAC economic news, or to fetch and summarize economic indicator releases (CPI, PMI, trade balance, GDP) across APAC countries. Covers pan-Asia wires, market data, trade/supply chain, labor statistics, and central bank primary sources, with an extra module for Vietnam-specific tracking. Make sure to trigger this even if the user just says "morning brief" or "econ news" without explicitly naming APAC, if the surrounding context is Asia-Pacific economics.
version: 1.0.0
author: Albert
license: MIT
metadata:
  hermes:
    tags: [Finance, Economics, APAC, Markets, Trade, Labor, Central Banks, News, Briefing]
    related_skills: [vn-policy-tracker]
    requires_toolsets: [web]
    requires_tools: [web_search]
    fallback_for_toolsets: [browser]
    fallback_for_tools: [browser_navigate]
---

# APAC Economic Tracker

A skill for building daily/periodic briefings on Asia-Pacific economics, finance, trade, and labor markets, and for maintaining a curated, agent-usable source list to pull from.

## When to Use

Use this skill when the user asks for:

- A daily or periodic APAC economics, finance, trade, or labor briefing.
- Current developments in Asian markets or APAC macroeconomics.
- A data calendar or upcoming APAC economic releases.
- A deep dive into APAC trade, supply chains, labor markets, central banks, or macro data.
- Vietnam-specific economic, trade, labor, or central-bank coverage.
- A new or expanded curated APAC economic source list or RSS feed set.

This skill covers:

- **Economics & markets**: growth data, inflation, rates, equity/FX moves across APAC.
- **Trade**: bilateral/regional flows, RCEP/ASEAN implementation, supply chain shifts.
- **Labor**: employment, wages, and labor-market structure across the region.
- **Central banks**: BOJ, PBOC, BOK, RBI, Bank Indonesia, RBA, SBV (Vietnam), and others.
- **Vietnam-specific tracking**: a dedicated module, since Vietnam data releases and local press often don't surface in pan-Asia wires.

This skill does **not** try to be a general news reader. It is scoped to economics, finance, trade, and labor for the APAC region. Do not use it for single-country deep dives outside APAC or for non-economic news.

## Quick Reference

Read these references before researching:

- `${HERMES_SKILL_DIR}/references/sources.md` — curated wires, markets, trade, labor, central-bank, and cross-country data sources.
- `${HERMES_SKILL_DIR}/references/vietnam-focus.md` — additional sources and watch items for Vietnam-specific coverage.

Optional helper scripts:

```bash
python ${HERMES_SKILL_DIR}/scripts/data_calendar.py --days 7
python ${HERMES_SKILL_DIR}/scripts/rss_pull.py
python ${HERMES_SKILL_DIR}/scripts/rss_pull.py --limit 5 --json
```

The scripts require network access and may require `requests` or `feedparser`; see each script's error message for installation instructions. Agents with `web_search`, `web_fetch`, or `web_extract` can work directly from the references instead.

## Procedure

1. Read `${HERMES_SKILL_DIR}/references/sources.md` for the relevant curated source list.
2. If the user wants Vietnam-specific coverage, also read `${HERMES_SKILL_DIR}/references/vietnam-focus.md`.
3. Decide what research is needed:
   - **"What's happening today"** → pull headlines from Nikkei Asia and Reuters Asia Economy, then check the data calendar for releases today or this week.
   - **"Data calendar" / "what's releasing this week"** → use `data_calendar.py` or fetch Trading Economics' APAC calendar directly.
   - **"Deep dive on X"** → use the specific category sources: trade → ADB/RCEP; labor → ILO; markets → FT/Bloomberg; central banks → the relevant primary source.
4. Use `web_search`, `web_fetch`, or `web_extract` against URLs in `sources.md`; do not invent URLs. If a source is paywalled, search for the headline and cite what is available.
5. Summarize the findings using the output format below. Keep the most market-moving items first, paraphrase rather than reproduce article text, and cite sources.
6. Save the completed brief to `apac-briefing-reports/` at the workspace root using the timestamped filename described below. Do not only return the brief in chat.

### Output format

Keep the report scannable and grouped by category:

```markdown
## APAC Econ Brief — [date]

### Markets & Rates
- [1–2 line item] (source)

### Trade & Supply Chain
- [1–2 line item] (source)

### Labor
- [1–2 line item] (source)

### Central Banks
- [1–2 line item] (source)

### Data releases today/this week
- [Country] [Indicator] [scheduled date/time if known]

### Vietnam (if in scope)
- [1–2 line item] (source)
```

Do not pad the report with items that are not market- or policy-relevant. If nothing significant happened in a category, omit that section.

### Saving the briefing report

Always write the brief to a Markdown file in the workspace. Save it to `apac-briefing-reports/` at the **workspace root** (the folder currently open in the editor), not inside the `finance/apac-econ-tracker` skill folder. Create the folder if it does not exist.

Use this exact filename format, based on the date and time the skill is run:

```text
apac-econ-brief_<YYYY-MM-DD>_<HHMM>.md
```

For example: `apac-econ-brief_2026-08-14_1345.md`.

If a terminal is available, get a local-time timestamp with:

```bash
date +%Y-%m-%d_%H%M
```

For UTC, use `date -u +%Y-%m-%d_%H%M`. Record the timestamp, timezone, coverage scope, and whether Vietnam coverage was included at the top of the report.

Never overwrite an existing brief. Every run must create a new file and preserve the full report history. Route any other files created by this skill — such as raw data-calendar HTML, RSS output, or saved source lists — into `apac-briefing-reports/`, prefixed with the same run timestamp so they remain grouped with the report that produced them.

## Pitfalls

- Do not fabricate headlines, data, prices, release dates, or source URLs.
- Do not rely on model pretraining when current information is required. If live data cannot be retrieved, state the limitation plainly.
- Do not treat a paywalled or inaccessible source as if its full content was retrieved; use an available headline or alternate source and identify the limitation.
- Do not pad categories with irrelevant items; omit empty categories.
- Do not reproduce long article passages. Paraphrase and cite the source.
- Sandboxed environments may not reach news and data domains. Prefer the available web tools over bundled scripts in that case. If neither web tools nor scripts can retrieve current information, do not invent a summary.

## Verification

Before finishing, confirm that:

- [ ] The report contains only APAC economics, finance, trade, labor, markets, or central-bank material relevant to the request.
- [ ] Current information was retrieved, or retrieval limitations are explicitly stated.
- [ ] Every factual item has an available source citation or URL where appropriate.
- [ ] The report is scannable, ordered by market/policy importance, and has no filler sections.
- [ ] The timestamp, timezone, coverage scope, and Vietnam-coverage status appear at the top of the file.
- [ ] The report is saved as `apac-econ-brief_<YYYY-MM-DD>_<HHMM>.md` in the workspace-root `apac-briefing-reports/` folder.
- [ ] Existing reports were not overwritten.
- [ ] Any other files created during the run were saved in the same folder with the same run timestamp.

## Maintaining the source list

If the user asks to add a source, country, or category (for example, Philippines labor data or semiconductor trade), edit `${HERMES_SKILL_DIR}/references/sources.md` directly. Append the source to the relevant category table and keep the existing columns: Source, Best for, URL, and RSS when applicable. Keep entries scoped to economics, finance, trade, and labor; do not let the list drift into general geopolitics or culture coverage.