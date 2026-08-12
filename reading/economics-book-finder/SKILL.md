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

### Phase 1 — Collect

1. Read `{HERMES_SKILL_DIR}/references/sources.md` for the suggested source list, organized by tier. **If the user has supplied their own list of websites, use those instead** (or merge — user-supplied sources are never overridden, only supplemented). Confirm the tier weighting for any user-supplied source with the user if it's not obvious (award page vs. casual blog vs. bestseller chart).
2. For each source, use `web_search` and/or `web_extract` to find its current economics-book content for the target year. Award/best-of pages usually need `web_extract` directly (search their site or fetch a known URL pattern, e.g. `ft.com/bookaward`). Bestseller charts and blogs are often better reached via `web_search` first to find the current live URL, since these pages move or get re-published each year.

For the Tier 4 "open domain search" list in `references/sources.md`, there's no single page to fetch — instead run each domain through `web_search` using the query templates given there (e.g. `site:domain.com "economics book" [year]`), then `web_fetch` whichever resulting articles look relevant. Treat each article as one mention at Tier 3's weight, same as any other source.

3. From each source, extract every distinct book mentioned: title, author, source name, source URL, and (if available) the date/edition. Do **not** copy long excerpts — a title, author, and one-line reason-for-inclusion is enough (see copyright guidance below).
4. Write everything you found into a single JSON file, one entry per (book, source) pair — the same book mentioned by three sources becomes three entries. See the schema in `{HERMES_SKILL_DIR}/scripts/aggregate_books.py --help` or the example below.

```json
[
  {"title": "The Thinking Machine", "author": "Stephen Witt", "source": "FT & Standard Chartered Business Book of the Year", "source_tier": 1, "url": "https://...", "note": "2025/26 award winner"},
  {"title": "The Thinking Machine", "author": "Stephen Witt", "source": "Amazon Business Bestsellers", "source_tier": 3, "url": "https://...", "note": "#4 in Economics"}
]
```

Save this as `<workspace>/raw_mentions.json`.

### Phase 2 — Aggregate

Run the aggregation script to dedupe titles (it fuzzy-matches on title+author so minor formatting differences don't split one book into two entries) and compute a prominence score:

```bash
python {HERMES_SKILL_DIR}/scripts/aggregate_books.py raw_mentions.json --output ranked_books.json
```

Scoring, in brief (full detail in the script's docstring): each mention contributes its source tier's weight; a book cited by more distinct sources gets a small additional cross-source bonus so agreement is rewarded beyond just summing weights. Ties are broken by number of distinct sources, then alphabetically.

Look at `ranked_books.json` before moving on — sanity-check that no two entries are obviously the same book that failed to merge (the fuzzy matcher isn't perfect on subtitles), and that nothing wildly off-topic slipped in (e.g. a personal-finance title from a bestseller chart that isn't really "economics").

### Phase 3 — Report

Render the final markdown report:

```bash
python {HERMES_SKILL_DIR}/scripts/render_report.py ranked_books.json --year 2026 --output economics_books_2026.md
```

This produces a ranked list with each book's title, author, prominence score, and the sources that named it (linked). Present this file to the user rather than re-typing the list into the chat response — but do lead with a short prose summary of what stood out (e.g. a book that swept every tier, or a clear theme across this year's picks).

## Copyright note

When extracting mentions from source pages, paraphrase any "why this book matters" blurbs in your own words — don't copy source text verbatim into `raw_mentions.json` or the final report. One short quoted phrase per source is the ceiling if a quote is genuinely needed.