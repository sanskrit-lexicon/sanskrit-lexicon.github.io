# CDSL dictionary landing-page generator

<p align="right"><sub>Created: 2026-07-01 · Last updated: 2026-07-01</sub></p>

Tooling that gives every Cologne Digital Sanskrit Lexicon **dictionary repo** a
self-contained, SEO + UX optimised GitHub Pages landing page
(`https://sanskrit-lexicon.github.io/<REPO>/`).

Each generated `index.html` is dependency-free and carries: a canonical URL,
meta description, Open Graph + Twitter `summary_large_image` cards, JSON-LD
`Book` structured data, and a hero linking to the **live dictionary** on the
Cologne site, the **source repo**, and the **CDSL hub**. The `og:image` is the
shared card hosted at the org root:
[`cdsl-card.png`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/cdsl-card.png).

## Files

| File | Role |
|---|---|
| [`gen_dict_page.py`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/tools/dict-pages/gen_dict_page.py) | **Reusable.** One HTML template + a `DICTS` metadata table (abbr, title, author, year, direction, live Cologne URL). Writes `out/<REPO>/index.html`. |
| [`make_shared_card.py`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/tools/dict-pages/make_shared_card.py) | **Reusable.** Regenerates the shared 1200×630 `cdsl-card.png` (PIL). |
| [`rollout_prs.py`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/tools/dict-pages/rollout_prs.py) | One-off. Phase 1: per repo, create a branch, add `index.html`, open a PR (skips repos that already have a root `index.html`). |
| [`rollout_merge_pages.py`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/tools/dict-pages/rollout_merge_pages.py) | One-off. Phase 2: merge each PR and enable GitHub Pages (`source = default branch, path /`). |
| [`add_nojekyll.py`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/tools/dict-pages/add_nojekyll.py) | One-off fix: add an empty `.nojekyll` and rebuild — see gotcha below. |

## Add or update one dictionary page

1. Add/edit the repo's row in the `DICTS` table in `gen_dict_page.py`. The live
   `cologne=` URL follows `…/scans/<CODE>Scan/<YEAR>/web/webtc/indexcaller.php`;
   the authoritative code+year map is on the
   [CDSL homepage](https://www.sanskrit-lexicon.uni-koeln.de/) source. Leave
   `cologne=None` for dictionaries not yet published live (the page then links to
   the main site).
2. `python gen_dict_page.py <REPO>` → writes `out/<REPO>/index.html`.
3. Commit that `index.html` to the repo root (via PR) — see the rollout scripts
   for the automated path.

## Gotcha — `.nojekyll` is required

GitHub Pages' default **Jekyll** build *fails* on dictionary repos ("Page build
failed") because their large data files collide with Liquid/Jekyll processing.
Every dictionary repo needs an empty **`.nojekyll`** at its root so Pages serves
the static `index.html` directly. `add_nojekyll.py` does this for the whole set.

## Rolled out (2026-07-01)

21 dictionary repos: MWS, PWG, MW72, PWK, SCH, ApteES, SKD, GRA, WIL, AP90, BUR,
CAE, CCS, MD, BEN, BOR, LRV, AMAR, AP, SHS, KOW. The per-dictionary
author/year/title are compiled from standard scholarship — maintainers should
sanity-check the less-common entries.
