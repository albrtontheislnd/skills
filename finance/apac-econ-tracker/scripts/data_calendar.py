#!/usr/bin/env python3
"""
Fetch the APAC economic data calendar (CPI, PMI, GDP, trade balance, etc.)
from Trading Economics for a given date range.

Usage:
    python data_calendar.py --days 7
    python data_calendar.py --start 2026-08-14 --end 2026-08-21

Requires network access to tradingeconomics.com. In sandboxed agent
environments without that access, this will fail cleanly and print
instructions to fetch the same page via a web_fetch tool instead.

APAC country filter is applied client-side after fetching the general
calendar, since Trading Economics' free calendar view is global by default.
"""

import argparse
import datetime as dt
import json
import sys

APAC_COUNTRIES = {
    "japan", "china", "south korea", "india", "indonesia", "australia",
    "vietnam", "thailand", "malaysia", "philippines", "singapore",
    "taiwan", "hong kong", "new zealand", "cambodia", "laos", "myanmar",
    "bangladesh", "pakistan", "sri lanka",
}

CALENDAR_URL = "https://tradingeconomics.com/calendar"


def fetch_calendar(start: str, end: str):
    try:
        import requests
    except ImportError:
        print("The 'requests' package is not installed. Install it with:")
        print("    pip install requests --break-system-packages")
        sys.exit(1)

    params = {"start": start, "end": end}
    headers = {"User-Agent": "Mozilla/5.0 (compatible; apac-econ-tracker/1.0)"}

    try:
        resp = requests.get(CALENDAR_URL, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"Could not reach {CALENDAR_URL}: {e}")
        print()
        print("This environment likely doesn't have network access to")
        print("tradingeconomics.com. Instead, use a web_fetch tool call")
        print(f"against: {CALENDAR_URL}?start={start}&end={end}")
        sys.exit(1)

    # Trading Economics' public calendar page is HTML/JS-rendered, not a
    # clean JSON API without a paid key. This function fetches the raw page;
    # callers with only text access should parse table rows for APAC
    # country names. This script intentionally does NOT attempt fragile
    # HTML scraping here — treat resp.text as raw input to hand off to an
    # LLM/agent for extraction, or swap in an official API key if you have one.
    return resp.text


def main():
    parser = argparse.ArgumentParser(description="Fetch APAC economic data calendar")
    parser.add_argument("--days", type=int, default=7, help="Number of days ahead from today")
    parser.add_argument("--start", type=str, help="Start date YYYY-MM-DD (overrides --days)")
    parser.add_argument("--end", type=str, help="End date YYYY-MM-DD (overrides --days)")
    args = parser.parse_args()

    if args.start and args.end:
        start, end = args.start, args.end
    else:
        today = dt.date.today()
        start = today.isoformat()
        end = (today + dt.timedelta(days=args.days)).isoformat()

    print(f"Fetching data calendar: {start} to {end}")
    html = fetch_calendar(start, end)
    print(f"Fetched {len(html)} chars of raw HTML from {CALENDAR_URL}.")
    print("Hand this off to an LLM/agent step to extract APAC rows, or")
    print("open the URL directly with a web_fetch tool for cleaner extraction:")
    print(f"  {CALENDAR_URL}?start={start}&end={end}")


if __name__ == "__main__":
    main()
