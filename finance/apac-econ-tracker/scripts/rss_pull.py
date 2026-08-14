#!/usr/bin/env python3
"""
Pull recent headlines from the RSS feeds listed in references/sources.md.

Usage:
    python rss_pull.py               # all feeds, 10 items each
    python rss_pull.py --limit 5      # fewer items per feed
    python rss_pull.py --json         # machine-readable output

Requires network access to the feed domains and the 'feedparser' package
(pip install feedparser --break-system-packages). In sandboxed environments
without outbound access to news domains, this will fail per-feed and report
which ones were unreachable — use web_fetch on the same URLs instead.
"""

import argparse
import json
import re
import sys
from pathlib import Path

FEEDS = {
    "Nikkei Asia": "https://asia.nikkei.com/rss/feed",
    "Reuters (Asia region)": "https://www.reutersagency.com/feed/?best-regions=asia&post_type=best",
}


def load_feeds_from_sources_md():
    """Optionally refresh FEEDS from references/sources.md so the script
    stays in sync if someone edits the markdown table instead of this file."""
    sources_path = Path(__file__).parent.parent / "references" / "sources.md"
    if not sources_path.exists():
        return FEEDS
    feeds = {}
    row_re = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(https?://\S+?)\s*\|\s*(https?://\S+?)\s*\|\s*$")
    for line in sources_path.read_text(encoding="utf-8").splitlines():
        m = row_re.match(line.strip())
        if m:
            name, _, _, rss = m.groups()
            feeds[name.strip()] = rss.strip()
    return feeds or FEEDS


def main():
    parser = argparse.ArgumentParser(description="Pull headlines from APAC econ RSS feeds")
    parser.add_argument("--limit", type=int, default=10, help="Max items per feed")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    args = parser.parse_args()

    try:
        import feedparser
    except ImportError:
        print("The 'feedparser' package is not installed. Install it with:")
        print("    pip install feedparser --break-system-packages")
        sys.exit(1)

    feeds = load_feeds_from_sources_md()
    results = {}
    unreachable = []

    for name, url in feeds.items():
        try:
            parsed = feedparser.parse(url)
            if parsed.bozo and not parsed.entries:
                raise RuntimeError(str(parsed.bozo_exception))
            items = [
                {"title": e.get("title", ""), "link": e.get("link", ""), "published": e.get("published", "")}
                for e in parsed.entries[: args.limit]
            ]
            results[name] = items
        except Exception as e:
            unreachable.append((name, url, str(e)))

    if args.json:
        print(json.dumps({"results": results, "unreachable": unreachable}, indent=2))
        return

    for name, items in results.items():
        print(f"\n## {name}")
        if not items:
            print("  (no items returned)")
        for item in items:
            print(f"  - {item['title']}" + (f" ({item['published']})" if item["published"] else ""))

    if unreachable:
        print("\n## Unreachable feeds (use web_fetch instead)")
        for name, url, err in unreachable:
            print(f"  - {name}: {url}  [{err}]")


if __name__ == "__main__":
    main()
