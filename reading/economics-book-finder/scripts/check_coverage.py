#!/usr/bin/env python3
"""
check_coverage.py — verify that every source listed in references/sources.md
has a corresponding entry in source_log.json before the sweep is considered
complete. This is a hard gate: Phase 2 (aggregate_books.py) should not run
until this script exits 0.

Why this exists: it's easy for an agent doing many sequential web_search /
web_fetch calls to quietly drop a source partway through (rate limit, a
confusing page, a task that "feels done" after the first several sources).
raw_mentions.json alone can't catch this, since a source that was *skipped*
looks identical to a source that was *checked and had nothing relevant* —
neither produces a book entry. source_log.json exists to make every source's
outcome explicit.

SOURCE_LOG SCHEMA (JSON array, one entry per source attempted):
    [
      {"source": "FT & Standard Chartered Business Book of the Year",
       "status": "ok", "mentions_found": 5},
      {"source": "Axiom Business Book Awards — Economics category",
       "status": "empty", "mentions_found": 0,
       "notes": "page loaded, no 2026 list published yet"},
      {"source": "reuters.com",
       "status": "failed",
       "notes": "web_fetch blocked, tried twice"}
    ]

status must be one of: "ok" (found mentions), "empty" (checked, nothing
relevant found), "failed" (could not access — must include a `notes`
reason). Every status is a legitimate outcome for the sweep to be
"complete" — the point is that every source got *looked at*, not that
every source produced results.

Source names must match references/sources.md exactly: the bold text for
Tier 1-3 entries, and the bare domain string for Tier 4 entries.

USAGE
    python check_coverage.py --sources references/sources.md --log source_log.json
Exit code 0 = full coverage. Exit code 1 = sources missing (printed to stderr).
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def parse_sources(md_text: str) -> list[str]:
    names: list[str] = []
    tier = None
    section = None  # for Tier 4: "templates" or "domains"
    for raw_line in md_text.splitlines():
        line = raw_line.strip()
        tier_match = re.match(r"^##\s*Tier\s*(\d+)", line)
        if tier_match:
            tier = int(tier_match.group(1))
            section = None
            continue
        if tier == 4:
            if line == "Search query templates to run per domain:":
                section = "templates"
                continue
            if line == "Domains:":
                section = "domains"
                continue
            if section == "domains" and line.startswith("- ") and not line.startswith("- `"):
                domain = line[2:].strip()
                if domain and not domain.startswith("*"):
                    names.append(domain)
            continue
        bold_match = re.match(r"^-\s+\*\*(.+?)\*\*", line)
        if bold_match:
            names.append(bold_match.group(1))
    return names


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", default="references/sources.md", help="Path to sources.md")
    ap.add_argument("--log", default="source_log.json", help="Path to source_log.json")
    args = ap.parse_args()

    try:
        expected = parse_sources(Path(args.sources).read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"Unable to read sources file {args.sources}: {exc}", file=sys.stderr)
        return 1

    try:
        log: Any = json.loads(Path(args.log).read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"No source_log.json found at {args.log} — sweep has not started.", file=sys.stderr)
        print(f"Expected {len(expected)} sources:", file=sys.stderr)
        for s in expected:
            print(f"  - {s}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Unable to read valid JSON from {args.log}: {exc}", file=sys.stderr)
        return 1

    if not isinstance(log, list) or any(not isinstance(entry, dict) for entry in log):
        print(f"{args.log} must contain a JSON array of objects.", file=sys.stderr)
        return 1

    logged = {entry.get("source") for entry in log}
    missing = [s for s in expected if s not in logged]
    duplicate_sources = sorted(source for source in logged if source and sum(1 for e in log if e.get("source") == source) > 1)
    invalid_entries = [e.get("source", "<missing source>") for e in log if not isinstance(e.get("source"), str) or not e.get("source")]
    invalid_status = [e.get("source", "<missing source>") for e in log if e.get("status") not in ("ok", "empty", "failed")]
    unreasoned_failures = [
        e.get("source", "<missing source>")
        for e in log
        if e.get("status") == "failed"
        and (not isinstance(e.get("notes"), str) or not e.get("notes"))
    ]

    problems = False
    if missing:
        problems = True
        print(f"MISSING — {len(missing)} of {len(expected)} sources not yet in {args.log}:", file=sys.stderr)
        for s in missing:
            print(f"  - {s}", file=sys.stderr)
    if invalid_status:
        problems = True
        print(f"INVALID STATUS on: {invalid_status} (must be ok/empty/failed)", file=sys.stderr)
    if invalid_entries:
        problems = True
        print(f"SOURCE LOG entries missing a non-empty `source`: {invalid_entries}", file=sys.stderr)
    if duplicate_sources:
        problems = True
        print(f"DUPLICATE SOURCE entries: {duplicate_sources}", file=sys.stderr)
    if unreasoned_failures:
        problems = True
        print(f"FAILED entries missing a `notes` reason: {unreasoned_failures}", file=sys.stderr)

    if problems:
        return 1

    ok = sum(1 for e in log if e["status"] == "ok")
    empty = sum(1 for e in log if e["status"] == "empty")
    failed = sum(1 for e in log if e["status"] == "failed")
    print(f"Full coverage: {len(expected)}/{len(expected)} sources logged ({ok} ok, {empty} empty, {failed} failed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
