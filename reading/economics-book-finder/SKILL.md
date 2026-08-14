---
name: economics-book-finder
description: Find and rank prominent economics books for a given year (e.g. 2026) by querying a curated list of source websites — award pages, bestseller trackers, and economist-run outlets — via web_search/web_extract, then aggregating and scoring the results into a ranked markdown report with citations. Use this whenever the user asks for "best economics books this year", "notable economics books published in [year]", a reading list for an agent/research pipeline, or wants a prominence-ranked (not just alphabetical) list of economics titles. Also use if the user asks to refresh an existing economics book list.
version: 1.2.0
author: Albert
license: MIT
metadata:
  hermes:
    category: reading
    tags: [Reading, Books]
    related_skills: []
---

# Economics Book Finder

Finds the economics books that are most *prominently* discussed right now — not just any list of economics books, but the ones multiple independent, credible sources are all pointing at. Prominence is inferred from cross-source agreement (a title several tiers of sources mention independently outranks one only a single blog mentions), weighted by source tier and recency.

## When to use this

Trigger on requests like:
- "What are the best economics books of [year]?"
- "Build me a ranked reading list of notable economics books this year"
- "Find prominent economics books for my agent's recommendation pipeline"
- "Refresh the economics book list with this new source"

Don't use this for a single well-known book lookup ("what is Thinking, Fast and Slow about") — that's a direct question, answer it directly.

## Workflow

This skill has three phases: **collect**, **aggregate**, **report**. The agent does the collecting itself (via `web_search`/`web_extract`) — the bundled scripts only do the aggregation and report rendering, since those steps are mechanical and benefit from deterministic code rather than manual tallying.

### Output location

All files generated during a run — `source_log.json`, `raw_mentions.json`, `ranked_books.json`, and the final Markdown report — must be saved in the `economics-book-reports/` subdirectory of the workspace.

The workspace is **the workspace determined by the Hermes agent at runtime**. It is not the skill source directory (`reading/economics-book-finder/`) or the repository containing the skill. The skill source directory contains only skill code and documentation; do not write agent-generated data there. Create `economics-book-reports/` in the runtime workspace if it does not already exist. Run the commands below from the workspace root so all output paths resolve to that directory.

### Phase 1 — Collect

**This phase is not done until every source has been accounted for — not until it "feels" done.** With a long source list, it's easy to work through the first dozen and stop once the results feel sufficient. That silent drop-off is the main failure mode of this skill, so Phase 1 uses a hard gate (`check_coverage.py`) rather than relying on Claude's own sense of completion.

1. Read `{HERMES_SKILL_DIR}/references/sources.md` for the suggested source list, organized by tier. **If the user has supplied their own list of websites, use those instead** (or merge — user-supplied sources are never overridden, only supplemented). Confirm the tier weighting for any user-supplied source with the user if it's not obvious (award page vs. casual blog vs. bestseller chart).
2. For each source, use `web_search` and/or `web_extract` to find its current economics-book content for the target year. Award/best-of pages usually need `web_extract` directly (search their site or fetch a known URL pattern, e.g. `ft.com/bookaward`). Bestseller charts and blogs are often better reached via `web_search` first to find the current live URL, since these pages move or get re-published each year.

For the Tier 4 "open domain search" list in `{HERMES_SKILL_DIR}/references/sources.md`, there's no single page to fetch — instead run each domain through `web_search` using the query templates given there (e.g. `site:domain.com "economics book" [year]`), then `web_fetch` whichever resulting articles look relevant. Treat each article as one mention at Tier 3's weight, same as any other source.

4. **Immediately after checking each source — not in a batch at the end — append one entry to `economics-book-reports/source_log.json`** recording what happened, using status `"ok"` (found mentions), `"empty"` (checked, nothing relevant), or `"failed"` (couldn't access — must include a `notes` reason). See the schema and rationale in `{HERMES_SKILL_DIR}/scripts/check_coverage.py`'s docstring. Logging as you go, rather than reconstructing it afterward, is what actually catches a dropped source — reconstructing from memory tends to just "remember" the ones that were interesting.

5. From each source, extract every distinct book mentioned: title, author, source name, source URL, and (if available) the date/edition. Do **not** copy long excerpts — a title, author, and one-line reason-for-inclusion is enough (see copyright guidance below). Append these to `raw_mentions.json` (schema below).

6. **Once you believe the sweep is complete, run the coverage gate — do not proceed to Phase 2 until it exits 0:**

   ```bash
   python {HERMES_SKILL_DIR}/scripts/check_coverage.py --sources {HERMES_SKILL_DIR}/references/sources.md --log economics-book-reports/source_log.json
   ```

   If it reports missing sources, go check them — don't mark them `"failed"` just to satisfy the gate. `"failed"` is for genuine access problems (blocked fetch, dead link), not for "ran out of time." If a source is genuinely unreachable after a real attempt, log it as `"failed"` with why, and mention the gap to the user in your final summary rather than hiding it.

`raw_mentions.json` schema (one entry per book-source pair — the same book found on three sources becomes three entries):

```json
[
  {"title": "The Thinking Machine", "author": "Stephen Witt", "source": "FT & Standard Chartered Business Book of the Year", "source_tier": 1, "url": "https://...", "note": "2025/26 award winner"},
  {"title": "The Thinking Machine", "author": "Stephen Witt", "source": "Amazon Business Bestsellers", "source_tier": 3, "url": "https://...", "note": "#4 in Economics"}
]
```

Save this as `<workspace>/economics-book-reports/raw_mentions.json`.

### Phase 2 — Aggregate

Run the aggregation script to dedupe titles (it fuzzy-matches on title+author so minor formatting differences don't split one book into two entries) and compute a prominence score:

```bash
python {HERMES_SKILL_DIR}/scripts/aggregate_books.py economics-book-reports/raw_mentions.json --output economics-book-reports/ranked_books.json
```

Scoring, in brief (full detail in the script's docstring): each mention contributes its source tier's weight; a book cited by more distinct sources gets a small additional cross-source bonus so agreement is rewarded beyond just summing weights. Ties are broken by number of distinct sources, then alphabetically.

Look at `ranked_books.json` before moving on — sanity-check that no two entries are obviously the same book that failed to merge (the fuzzy matcher isn't perfect on subtitles), and that nothing wildly off-topic slipped in (e.g. a personal-finance title from a bestseller chart that isn't really "economics").

### Phase 3 — Report

Render the final markdown report:

```bash
python {HERMES_SKILL_DIR}/scripts/render_report.py economics-book-reports/ranked_books.json --year 2026 --output economics-book-reports/economics_books_2026.md
```

This produces a ranked list with each book's title, author, prominence score, and the sources that named it (linked). Present this file to the user rather than re-typing the list into the chat response — but do lead with a short prose summary of what stood out (e.g. a book that swept every tier, or a clear theme across this year's picks).

Before finishing, verify that all generated files are in `<workspace>/economics-book-reports/`, where `<workspace>` is the runtime workspace selected by Hermes, and that no generated data was written to the skill source directory.

## Copyright note

When extracting mentions from source pages, paraphrase any "why this book matters" blurbs in your own words — don't copy source text verbatim into `raw_mentions.json` or the final report. One short quoted phrase per source is the ceiling if a quote is genuinely needed.