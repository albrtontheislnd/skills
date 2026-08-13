#!/usr/bin/env python3
"""
dedupe_rank.py

Gộp các bản ghi văn bản chính sách trùng lặp (thu thập từ nhiều nguồn) và
sắp xếp theo ngày ban hành giảm dần. Chỉ dùng Python stdlib.

Input: đường dẫn tới file JSON chứa một danh sách các object theo schema:
    {
        "title": "...",
        "doc_type": "...",
        "issuing_body": "...",
        "issue_date": "YYYY-MM-DD" (hoặc chuỗi ngày bất kỳ, sẽ cố gắng parse),
        "effective_date": "...",
        "status": "...",
        "summary": "...",
        "impact_areas": ["..."],
        "sources": ["url1", "url2"]
    }

Output: in ra stdout một JSON list đã gộp trùng lặp và sắp xếp theo issue_date
giảm dần (bản ghi không parse được ngày sẽ xếp cuối). Đồng thời in ra stderr
một bảng thống kê số lượng bản ghi theo từng domain nguồn (source_domain) —
dùng để kiểm tra xem có domain nào trong danh sách nguồn được giao mà KHÔNG
xuất hiện bản ghi nào không, để tránh bỏ sót nguồn khi thu thập.

Cách gộp trùng lặp:
  1. Chuẩn hoá "số hiệu văn bản" trích xuất từ title (vd "12/2026/NĐ-CP") -
     nếu hai bản ghi có cùng số hiệu chuẩn hoá -> gộp.
  2. Nếu không có số hiệu (vd đang là dự thảo chưa có số), so sánh độ tương
     đồng tiêu đề bằng difflib.SequenceMatcher; ngưỡng mặc định 0.82.

Khi gộp, trường "sources" của bản ghi được hợp nhất (union) chứ không mất đi
— nhờ vậy vẫn theo dõi được văn bản này từng xuất hiện ở (những) domain nào,
kể cả sau khi đã gộp trùng lặp giữa nhiều nguồn.

Usage:
    python3 dedupe_rank.py records.json > merged.json
    python3 dedupe_rank.py records.json --threshold 0.85
    python3 dedupe_rank.py records.json --expected-domains domains.txt
"""

import sys
import json
import re
import argparse
from difflib import SequenceMatcher
from datetime import datetime
from urllib.parse import urlparse
from collections import Counter


DOC_NUMBER_RE = re.compile(
    r"(\d{1,4}\s*/\s*\d{4}\s*/\s*[A-Za-zÀ-ỹĐđ\-]{2,15})", re.UNICODE
)

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"]


def normalize_doc_number(title: str):
    if not title:
        return None
    m = DOC_NUMBER_RE.search(title)
    if not m:
        return None
    return re.sub(r"\s+", "", m.group(1)).upper()


def normalize_title(title: str):
    if not title:
        return ""
    t = title.lower()
    t = re.sub(r"[^\w\sÀ-ỹĐđ]", " ", t, flags=re.UNICODE)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_title(a), normalize_title(b)).ratio()


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def extract_domain(url: str):
    try:
        netloc = urlparse(url).netloc.lower()
        return netloc[4:] if netloc.startswith("www.") else netloc
    except Exception:
        return None


def merge_two(a: dict, b: dict) -> dict:
    """Gộp bản ghi b vào bản ghi a: hợp nhất sources/impact_areas, giữ lại
    tóm tắt (summary) dài hơn, ưu tiên lấy giá trị không rỗng cho các
    trường còn thiếu."""
    merged = dict(a)
    for key in ("doc_type", "issuing_body", "issue_date", "effective_date", "status"):
        if not merged.get(key) and b.get(key):
            merged[key] = b[key]

    a_summary = a.get("summary") or ""
    b_summary = b.get("summary") or ""
    merged["summary"] = a_summary if len(a_summary) >= len(b_summary) else b_summary

    merged_sources = list(dict.fromkeys((a.get("sources") or []) + (b.get("sources") or [])))
    merged["sources"] = merged_sources

    merged_areas = list(dict.fromkeys((a.get("impact_areas") or []) + (b.get("impact_areas") or [])))
    merged["impact_areas"] = merged_areas

    merged["title"] = a.get("title") or b.get("title")
    return merged


def dedupe(records, threshold=0.82):
    merged = []
    for rec in records:
        doc_num = normalize_doc_number(rec.get("title", ""))
        match_idx = None

        for i, existing in enumerate(merged):
            existing_num = normalize_doc_number(existing.get("title", ""))
            if doc_num and existing_num and doc_num == existing_num:
                match_idx = i
                break
            if not doc_num and not existing_num:
                sim = title_similarity(rec.get("title", ""), existing.get("title", ""))
                if sim >= threshold:
                    match_idx = i
                    break

        if match_idx is not None:
            merged[match_idx] = merge_two(merged[match_idx], rec)
        else:
            merged.append(rec)

    return merged


def sort_by_date_desc(records):
    def sort_key(r):
        d = parse_date(r.get("issue_date"))
        # Bản ghi không parse được ngày sẽ xếp cuối danh sách
        return (d is None, -(d.timestamp()) if d else 0)

    return sorted(records, key=sort_key)


def domain_coverage_report(records, expected_domains=None):
    """Đếm số bản ghi theo từng domain nguồn (dựa trên trường 'sources'),
    và nếu có danh sách expected_domains thì báo rõ domain nào KHÔNG có bản
    ghi nào — để phát hiện sớm việc bỏ sót nguồn khi thu thập."""
    counter = Counter()
    for rec in records:
        for url in rec.get("sources") or []:
            domain = extract_domain(url)
            if domain:
                counter[domain] += 1

    lines = ["[dedupe_rank] Số bản ghi theo domain nguồn:"]
    for domain, count in sorted(counter.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"  - {domain}: {count}")

    if expected_domains:
        covered = set(counter.keys())
        missing = [d for d in expected_domains if not any(d in c or c in d for c in covered)]
        if missing:
            lines.append("[dedupe_rank] CẢNH BÁO — các domain được giao thu thập nhưng KHÔNG thấy bản ghi nào:")
            for d in missing:
                lines.append(f"  - {d}")
        else:
            lines.append("[dedupe_rank] Đã có ít nhất 1 bản ghi cho mỗi domain trong danh sách được giao.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Gộp các bản ghi chính sách Việt Nam bị trùng lặp và sắp xếp theo ngày."
    )
    parser.add_argument("input_json", help="Đường dẫn tới file JSON chứa danh sách bản ghi chính sách")
    parser.add_argument(
        "--threshold", type=float, default=0.82,
        help="Ngưỡng tương đồng tiêu đề để gộp các bản ghi không có số hiệu văn bản (0-1, mặc định 0.82)",
    )
    parser.add_argument(
        "--expected-domains", type=str, default=None,
        help="Đường dẫn file text liệt kê mỗi domain một dòng — để kiểm tra domain nào chưa có bản ghi nào (tránh bỏ sót nguồn)",
    )
    args = parser.parse_args()

    with open(args.input_json, "r", encoding="utf-8") as f:
        records = json.load(f)

    if not isinstance(records, list):
        print("File JSON đầu vào phải là một danh sách (list) các bản ghi.", file=sys.stderr)
        sys.exit(1)

    merged = dedupe(records, threshold=args.threshold)
    result = sort_by_date_desc(merged)

    print(json.dumps(result, ensure_ascii=False, indent=2))

    print(
        f"[dedupe_rank] {len(records)} bản ghi đầu vào -> {len(result)} bản ghi sau khi gộp trùng lặp",
        file=sys.stderr,
    )

    expected_domains = None
    if args.expected_domains:
        with open(args.expected_domains, "r", encoding="utf-8") as f:
            expected_domains = [line.strip() for line in f if line.strip()]

    print(domain_coverage_report(result, expected_domains), file=sys.stderr)


if __name__ == "__main__":
    main()
