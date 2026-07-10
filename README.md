# sanskrit-lexicon.github.io

_Created: 22-06-2026 · Last updated: 11-07-2026_

## Why this repo exists

Every GitHub organization needs an `<org>.github.io` repo to serve static content at a stable public URL. This is that repo for the [Sanskrit Lexicon organization](https://github.com/sanskrit-lexicon), and it plays two roles:

1. **Org-root landing hub.** [`index.html`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/index.html) is the public front door of the Cologne Digital Sanskrit Lexicon at [`https://sanskrit-lexicon.github.io/`](https://sanskrit-lexicon.github.io/) — a grouped directory of every dictionary landing page (31 dictionaries) plus the analysis/tool surfaces (app, guides, atlas, observatory). It is generated, not hand-authored (see [`tools/dict-pages/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/tools/dict-pages)).
2. **Shared publication host for one-off outputs.** Cologne dictionary research produces reports — a cross-reference table, an n-gram diff, a headword-normalization audit — that are useful to link from an issue or a paper but don't belong in any single dictionary's own repo. Commit an HTML report here and it is live at `https://sanskrit-lexicon.github.io/<subdirectory>/<file>` with no build step.

The repo holds no research scripts of its own — the code that produced each report lives in its source repo; only the rendered output is committed here. The one exception is the [`tools/dict-pages/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/tools/dict-pages) landing-page generator, which is Jekyll-excluded (via [`_config.yml`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/_config.yml)) so it is never published as part of the site.

## The landing hub

[`index.html`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/index.html), the domain-root sitemaps ([`sitemap.xml`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/sitemap.xml), [`dictionaries.xml`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/dictionaries.xml)), and every per-dictionary landing page (rolled out to the individual dictionary repos) are all generated from a single `DICTS` metadata table in [`tools/dict-pages/gen_dict_page.py`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/tools/dict-pages/gen_dict_page.py).

> Edit the `DICTS` table and regenerate — do not hand-edit the generated hub or sitemaps directly, or they drift out of sync on the next rollout. The per-repo rollout of individual dictionary landing pages is driven by the [`/cologne-pages-landing`](https://github.com/gasyoun/claude-config/blob/main/commands/cologne-pages-landing.md) skill (handoff H260).

Supporting files: [`cdsl-card.png`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/cdsl-card.png) (shared 1200×630 social card, applied site-wide as the default `og:image` via [`_config.yml`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/_config.yml) + jekyll-seo-tag), [`robots.txt`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/robots.txt), and [`gcse/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/gcse) (Google Custom Search Engine integration).

## Published reports

| Directory | Contents |
|---|---|
| [`cologne/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/cologne) | Syntax-highlighted code and data reports for the Cologne pipeline (e.g. [`cologne/highlighter/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/cologne/highlighter), a client-side text highlighter) |
| [`CORRECTIONS/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/CORRECTIONS) | HTML reports on correction analysis — [`abnormending/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/CORRECTIONS/abnormending) (abnormal word-ending audit), [`dhaval/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/CORRECTIONS/dhaval) (Dhaval Patel's correction analyses), [`ngram/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/CORRECTIONS/ngram) (pairwise n-gram diff reports across dictionary pairs) |
| [`PWK/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/PWK) | PWK dictionary cross-reference reports: [`cbisub.html`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/PWK/cbisub.html), [`cmbsub.html`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/PWK/cmbsub.html), [`pwis_notmw.html`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/PWK/pwis_notmw.html) |
| [`VCP/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/VCP) | VCP dictionary research outputs, e.g. [`vac-vcp-cmp2/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/VCP/vac-vcp-cmp2) (headword-diff and length-comparison reports) |
| [`hwnorm1/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/hwnorm1) | Headword normalization research reports (`conv3/`, `proberrors/`) |
| [`verbs/`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/tree/main/verbs) | Verb root comparison reports (`vcp_skd/`, `verbs01/`) |

## Usage example (verified)

Any file here is a static page — "running" it means opening the URL or the local file directly, no server. [`PWK/cbisub.html`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/PWK/cbisub.html) is a real, currently-published report: a self-contained table-based HTML page with inline CSS and no external dependencies, confirmed live at [`https://sanskrit-lexicon.github.io/PWK/cbisub.html`](https://sanskrit-lexicon.github.io/PWK/cbisub.html).

Publishing a new report is just: commit an HTML/data file to the right subdirectory and push to `main`; Pages serves it at the matching path with no separate deploy step.

## Conventions

- No CI or build pipeline for content in this repo — GitHub Pages serves the committed files directly from `main`. The [Cologne tooling runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-tooling-runbook.md) governs the org-wide GitHub Issue taxonomy this repo also follows.
- Domain labels here are scoped to build-meta concerns: `domain:ci`, `domain:packaging`, `domain:publishing`.
- Org Project: [Tooling Roadmap](https://github.com/orgs/sanskrit-lexicon/projects/9).
- Session state is tracked in [`.ai_state.md`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/.ai_state.md); notable changes are logged in [`CHANGELOG.md`](https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io/blob/main/CHANGELOG.md).

---

_Dr. Mārcis Gasūns_
