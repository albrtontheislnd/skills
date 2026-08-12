#!/usr/bin/env python3
"""
render_report.py — turn ranked_books.json (from aggregate_books.py) into a
readable markdown report.

USAGE
    python render_report.py ranked_books.json --year 2026 --output economics_books_2026.md
    python render_report.py ranked_books.json --year 2026 --top 15
"""

import argparse
import json


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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="Path to ranked_books.json")
    ap.add_argument("--year", default="", help="Year label for the report title")
    ap.add_argument("--output", default="economics_books_report.md", help="Output markdown path")
    ap.add_argument("--top", type=int, default=0, help="Only include the top N books (0 = all)")
    args = ap.parse_args()

    with open(args.input) as f:
        books = json.load(f)

    report = render(books, args.year or "This Year", args.top)

    with open(args.output, "w") as f:
        f.write(report)

    print(f"Wrote report for {len(books) if not args.top else min(args.top, len(books))} books -> {args.output}")


if __name__ == "__main__":
    main()
