# APAC Economics / Finance / Trade / Labor — Source List

Curated for daily-tracking use. Organized by category. Use `web_fetch` on the URLs directly, or `web_search` scoped to `site:<domain>` when you need something more specific than the homepage.

## 1. Wire services & aggregators (read first, daily)

| Source | Best for | URL | RSS |
|---|---|---|---|
| Nikkei Asia | Pan-Asia economic/political coverage, Japan/Korea/China supply chains | https://asia.nikkei.com | https://asia.nikkei.com/rss/feed |
| Reuters Asia Economy | Fastest on data releases, central bank moves, trade flows | https://www.reuters.com/world/asia-pacific/ | https://www.reutersagency.com/feed/?best-regions=asia&post_type=best |
| Bloomberg Asia | Markets-heavy, cross-market linkages (partial paywall; headlines/newsletters free) | https://www.bloomberg.com/asia | — (no public RSS; use web_search) |

## 2. Markets & finance

| Source | Best for | URL |
|---|---|---|
| Financial Times — Asia-Pacific | Capital flows, currency moves, cross-border investment | https://www.ft.com/asia-pacific |
| South China Morning Post — Business | China's economy and regional spillover | https://www.scmp.com/business |
| Trading Economics — APAC | Free real-time indicator calendars (CPI, PMI, trade balance) per country | https://tradingeconomics.com/calendar |

## 3. Trade & supply chain

| Source | Best for | URL |
|---|---|---|
| Asian Development Bank (ADB) | Regional trade/development statistics, policy briefs | https://www.adb.org/news | 
| ADB Data Portal | Structured regional statistics | https://data.adb.org |
| ASEAN Secretariat | RCEP/ASEAN trade agreement implementation updates | https://asean.org/news/ |
| The Diplomat — Economy | Geopolitics-inflected trade analysis, policy context | https://thediplomat.com/topics/economy/ |

## 4. Labor markets & structural economics

| Source | Best for | URL |
|---|---|---|
| ILO Asia-Pacific | Labor market reports, wage/employment data | https://www.ilo.org/asia |
| World Bank East Asia & Pacific Economic Update | Semi-annual deep dives on regional growth/labor structure | https://www.worldbank.org/en/region/eap/publication/east-asia-and-pacific-economic-update |

## 5. Central banks (primary sources — often move markets before wires catch up)

| Central bank | Country | URL |
|---|---|---|
| Bank of Japan (BOJ) | Japan | https://www.boj.or.jp/en/ |
| People's Bank of China (PBOC) | China | http://www.pbc.gov.cn/en/3688006/index.html |
| Bank of Korea (BOK) | South Korea | https://www.bok.or.kr/eng/main/main.do |
| Reserve Bank of India (RBI) | India | https://www.rbi.org.in |
| Bank Indonesia | Indonesia | https://www.bi.go.id/en |
| Reserve Bank of Australia (RBA) | Australia | https://www.rba.gov.au |
| State Bank of Vietnam (SBV) | Vietnam | https://www.sbv.gov.vn/webcenter/portal/en |

## 6. Cross-country standardized data

| Source | Best for | URL |
|---|---|---|
| IMF APAC Regional Economic Outlook | Standardized cross-country macro data & forecasts | https://www.imf.org/en/Publications/REO/APAC |
| CEIC | Granular historical indicator series (subscription; check free previews) | https://www.ceicdata.com |

---

See `vietnam-focus.md` for Vietnam-specific sources (GSO, local business press).

## Maintenance notes
- Keep this table-based format — it's what `rss_pull.py` and agents parse against.
- When adding a source, include: Source name, what it's best for (one line), URL, and RSS feed URL if one exists (else `—`).
- Don't add general news, entertainment, or non-econ geopolitics sources here — keep scope tight.
