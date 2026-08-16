#!/usr/bin/env python3
"""
render_report.py — turn ranked_books.json (from aggregate_books.py) into a
readable markdown report.

USAGE
    python render_report.py ranked_books.json --year 2026 --output economics_books_2026.md
    # Writes economics_books_2026_YYYYMMDD-HHmm.md using local system time
    python render_report.py ranked_books.json --year 2026 --top 15
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def render(books: list, year: str, top: int) -> str:
    books = books[:top] if top else books
    lines = [f"# Prominent Economics Books — {year}", ""]
    lines.append(
        "Ranked by cross-source prominence: how many independent sources named the book, "
        "weighted by how authoritative each source is. Not a quality judgment on its own — "
        "check the linked sources for context."
    )
    lines.append("")

    for i, b in enumerate(books, start=1):
        author_str = f" — {b['author']}" if b.get("author") else ""
        lines.append(f"## {i}. {b['title']}{author_str}")
        lines.append(f"*Prominence score: {b['score']} · named by {b['num_sources']} source(s)*")
        lines.append("")
        for m in b["mentions"]:
            note = f" — {m['note']}" if m.get("note") else ""
            if m.get("url"):
                lines.append(f"- [{m['source']}]({m['url']}){note}")
            else:
                lines.append(f"- {m['source']}{note}")
        lines.append("")

    return "\n".join(lines)


TIMESTAMP_PATTERN = re.compile(r"_\d{8}-\d{4}$")


def timestamped_path(output: str) -> Path:
    """Insert a local-system-time YYYYMMDD-HHmm timestamp before the extension."""
    path = Path(output)
    if TIMESTAMP_PATTERN.search(path.stem):
        return path
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    suffix = path.suffix or ".md"
    return path.with_name(f"{path.stem}_{timestamp}{suffix}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="Path to ranked_books.json")
    ap.add_argument("--year", default="", help="Year label for the report title")
    ap.add_argument(
        "--output",
        default=None,
        help="Output path; a local-time YYYYMMDD-HHmm timestamp is inserted before the extension",
    )
    ap.add_argument("--top", type=int, default=0, help="Only include the top N books (0 = all)")
    args = ap.parse_args()
    if args.top < 0:
        ap.error("--top must be zero or greater")

    try:
        books = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Unable to read valid JSON from {args.input}: {exc}", file=sys.stderr)
        return 1
    if not isinstance(books, list) or any(not isinstance(book, dict) for book in books):
        print("Input must be a JSON array of ranked book objects.", file=sys.stderr)
        return 1

    report = render(books, args.year or "This Year", args.top)
    output = timestamped_path(args.output or "economics_books_report.md")

    try:
        output.write_text(report, encoding="utf-8")
    except OSError as exc:
        print(f"Unable to write {output}: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote report for {len(books) if not args.top else min(args.top, len(books))} books -> {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
