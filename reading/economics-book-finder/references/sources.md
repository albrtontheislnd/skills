# Suggested Sources

A starting list, organized by tier. Tier controls how much weight a mention from that source gets in `aggregate_books.py` (lower tier number = stronger signal). Replace or extend freely — this is a draft, not a fixed canon. If you supply your own sources, tell the skill so the tier weighting reflects how much you trust each one.

## Tier 1 — Major awards & "best of the year" panels
Strongest prominence signal: curated by editorial boards/judging panels, usually covers business-and-economics together.
- **Princeton University Press — Economics** — `press.princeton.edu/subjects/economics-finance`, `press.princeton.edu`
- **Harvard University Press — Economics** — `hup.harvard.edu/browse/economics-business`, `hup.harvard.edu/features`, `hup.harvard.edu`
- **University of Chicago Press — Economics** — `press.uchicago.edu`, `pressblog.uchicago.edu`, `stonecenter.uchicago.edu`
- **IMF Book Reviews** — `www.imf.org/en/publications/fandd/categories/book%20reviews`
- **LSE - The London School of Economics and Political Science** — `lse.ac.uk`, `blogs.lse.ac.uk/categories/book-reviews`
- **MIT Press** - `mitpress.mit.edu`, `mitpress.mit.edu/search-result-list/?category=BUS&collection=new-releases`

## Tier 2 — Major outlets' nonfiction/economics coverage
Broad readership, editorially curated, but not a formal award.
- **FT Book** — `ft.com/bookaward`, `ft.com/business-books`, `ft.com/non-fiction`
- **Axiom Business Book Awards — Economics category** — `axiomawards.com/medalists`
- **New York Times — Book Review, Nonfiction / Economics coverage** — `nytimes.com/section/books`
- **Bloomberg — Best Books** (annual roundup, has economics/finance titles) — bloomberg.com
- **Foreign Affairs — Recent Books (Economics, Social Issues section)** — `foreignaffairs.com/books-and-reviews`, `foreignaffairs.com/book-reviews/search?topic=Economics`
- **The Wall Street Journal — Business Bookshelf column** — `wsj.com`, `wsj.com/news/types/bookshelf`

## Tier 3 — Economist-run blogs & commentary sites
Prominence among the profession's own readers/practitioners; good for catching books that haven't hit mainstream press yet.
- **Marginal Revolution** (Tyler Cowen) — marginalrevolution.com
- **Project Syndicate** — project-syndicate.org
- **VoxEU / CEPR** — cepr.org/voxeu
- **Conversable Economist** (Timothy Taylor) — conversableeconomist.com

## Tier 4 — Open domain search (term-based)
Not a curated page like the tiers above — these are domains to run a general `web_search` term query against (e.g. `site:domain.com "economics book" [year]`), useful for outlets that don't publish one stable "best of" page but do write about notable books as ordinary articles. Weaker signal per hit than a curated tier, since a single mention is just one article, not an editorial selection — weight accordingly.
 
Search query templates to run per domain:
- `site:<domain> "economics book" of [year]`
- `site:<domain> "best economics books" of [year]`
- `site:<domain> notable economics books of [year]`

Domains:
- inomics.com
- blogs.cornell.edu
- london.edu
- library.hbs.edu
- economics.princeton.edu
- sites.lsa.umich.edu/mje
- theguardian.com/books
- npr.org
- brookings.edu
- aeaweb.org

## Tier 5 — Publisher catalogs (optional, for completeness rather than ranking)
Useful to catch new releases early in the year before award/bestseller signal exists yet; weight low since inclusion isn't selective. Publisher-catalog mentions should be logged as Tier 5 and should not be treated as editorial endorsements.