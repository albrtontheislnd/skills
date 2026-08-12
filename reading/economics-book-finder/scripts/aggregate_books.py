#!/usr/bin/env python3
"""
aggregate_books.py — dedupe and score raw (book, source) mentions into a
ranked prominence list.

INPUT SCHEMA (JSON array, one object per book-source mention):
    [
      {
        "title": "The Thinking Machine",
        "author": "Stephen Witt",
        "source": "FT & Standard Chartered Business Book of the Year",
        "source_tier": 1,
        "url": "https://...",
        "note": "2025/26 award winner"     # optional, short, your own words
      },
      ...
    ]

The same book named by three sources should appear as three separate
entries — this script does the merging. `source_tier` is an integer where
1 is the strongest signal and higher numbers are weaker. If you're using the tiers from
references/sources.md, pass 1-5.

SCORING
    Each mention contributes its tier's weight (see DEFAULT_TIER_WEIGHTS
    below, override with --weights). A book gets a small additional bonus
    for being named by *multiple distinct sources*, on top of the summed
    tier weights, so that broad agreement across sources is rewarded even
    beyond what the raw weight sum already gives it. This keeps one very
    high-tier source from single-handedly outranking a book that several
    mid-tier sources independently agree on.

        score = sum(tier_weight for each mention)
              + CROSS_SOURCE_BONUS * (num_distinct_sources - 1)

DEDUPING
    Titles are normalized (lowercased, punctuation stripped, leading
    articles dropped) and matched with difflib's SequenceMatcher. Two
    mentions merge if their normalized titles are a close match (ratio
    above --match-threshold, default 0.85) AND, when both have an author
    listed, the authors also match loosely. This catches subtitle/edition
    differences ("The Thinking Machine" vs "The Thinking Machine: Jensen
    Huang...") without merging unrelated books that happen to share a
    generic word.

    The matcher is not perfect — always eyeball ranked_books.json before
    rendering the final report.

USAGE
    python aggregate_books.py raw_mentions.json --output ranked_books.json
    python aggregate_books.py raw_mentions.json --min-sources 2   # drop singletons
"""

import argparse
import json
import re
import sys
from difflib import SequenceMatcher

DEFAULT_TIER_WEIGHTS = {1: 5.0, 2: 3.0, 3: 2.0, 4: 1.0, 5: 0.5}
CROSS_SOURCE_BONUS = 1.5
LEADING_ARTICLES = ("the ", "a ", "an ")


def normalize_title(title: str) -> str:
    t = title.lower().strip()
    t = re.sub(r"[:\-–—].*$", "", t)  # drop subtitle after a colon/dash
    t = re.sub(r"[^\w\s]", "", t)
    t = t.strip()
    for art in LEADING_ARTICLES:
        if t.startswith(art):
            t = t[len(art):]
            break
    return re.sub(r"\s+", " ", t).strip()


def titles_match(a: str, b: str, threshold: float) -> bool:
    na, nb = normalize_title(a), normalize_title(b)
    if na == nb:
        return True
    return SequenceMatcher(None, na, nb).ratio() >= threshold


def authors_compatible(a: str, b: str) -> bool:
    if not a or not b:
        return True  # can't contradict what we don't have
    na = re.sub(r"[^\w\s]", "", a.lower()).strip()
    nb = re.sub(r"[^\w\s]", "", b.lower()).strip()
    return SequenceMatcher(None, na, nb).ratio() >= 0.6


def cluster_mentions(mentions: list, threshold: float) -> list:
    clusters = []  # each: {"title", "author", "mentions": [...]}
    for m in mentions:
        placed = False
        for c in clusters:
            if titles_match(m["title"], c["title"], threshold) and authors_compatible(
                m.get("author", ""), c.get("author", "")
            ):
                c["mentions"].append(m)
                placed = True
                break
        if not placed:
            clusters.append({"title": m["title"], "author": m.get("author", ""), "mentions": [m]})
    return clusters


def score_cluster(cluster: dict, tier_weights: dict) -> dict:
    mentions = cluster["mentions"]
    distinct_sources = {m["source"] for m in mentions}
    raw_score = sum(tier_weights.get(int(m.get("source_tier", 5)), 0.5) for m in mentions)
    bonus = CROSS_SOURCE_BONUS * max(0, len(distinct_sources) - 1)
    return {
        "title": cluster["title"],
        "author": cluster["author"],
        "score": round(raw_score + bonus, 2),
        "num_sources": len(distinct_sources),
        "mentions": [
            {"source": m["source"], "url": m.get("url", ""), "note": m.get("note", "")}
            for m in mentions
        ],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="Path to raw_mentions.json")
    ap.add_argument("--output", default="ranked_books.json", help="Where to write the ranked list")
    ap.add_argument("--match-threshold", type=float, default=0.85, help="Title fuzzy-match threshold (0-1)")
    ap.add_argument("--min-sources", type=int, default=1, help="Drop books named by fewer than N distinct sources")
    ap.add_argument(
        "--weights",
        type=str,
        default=None,
        help='Override tier weights as JSON, e.g. \'{"1":5,"2":3,"3":2,"4":1,"5":0.5}\'',
    )
    args = ap.parse_args()

    with open(args.input) as f:
        mentions = json.load(f)

    if not mentions:
        print("No mentions found in input — nothing to aggregate.", file=sys.stderr)
        sys.exit(1)

    tier_weights = DEFAULT_TIER_WEIGHTS
    if args.weights:
        tier_weights = {int(k): float(v) for k, v in json.loads(args.weights).items()}

    clusters = cluster_mentions(mentions, args.match_threshold)
    scored = [score_cluster(c, tier_weights) for c in clusters]
    scored = [s for s in scored if s["num_sources"] >= args.min_sources]
    scored.sort(key=lambda s: (-s["score"], -s["num_sources"], s["title"].lower()))

    with open(args.output, "w") as f:
        json.dump(scored, f, indent=2)

    print(f"Aggregated {len(mentions)} mentions into {len(scored)} ranked books -> {args.output}")


if __name__ == "__main__":
    main()
