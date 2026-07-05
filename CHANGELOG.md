# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Shared social card (`cdsl-card.png`), default `og:image` via `_config.yml`/jekyll-seo-tag,
  and project sitemaps advertised from the domain-root `robots.txt`.
- `tools/dict-pages/`: CDSL dictionary landing-page generator (`gen_dict_page.py`) +
  shared card generator + rollout scripts, used to roll SEO/UX landing pages out to all
  21+ dictionary repos.
- Org-root landing page (`index.html`): grouped directory of all dictionary landing pages
  plus the analysis/tool sites (app, guides, atlas, observatory), generated from the same
  `DICTS` table as the per-dictionary pages.
- Domain-root sitemap index (`sitemap.xml` + `dictionaries.xml`) covering the hub and all
  dictionary landing pages.
- Full dictionary coverage: 10 more repos (VCP, BHS, BOP, VEI, IEG, INM, MCI, ACC, KRM,
  FRI) added to the hub + sitemap under a new "Reference works, glossaries & indexes"
  group — 31 dictionaries + 4 tools total.

### Fixed
- Hub grid hardened against ultra-narrow (<300px) viewport overflow (folded phones) via
  `minmax(min(100%,260px),1fr)`.
