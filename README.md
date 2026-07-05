# sanskrit-lexicon.github.io

_Created: 22-06-2026 · Last updated: 05-07-2026_

## Why this repo exists

Cologne dictionary research produces one-off outputs — a cross-reference table, an n-gram diff report, a headword-normalization audit — that are useful to link from an issue or a paper but don't belong in any single dictionary's own repo. GitHub Pages needs a `<org>.github.io` repo to serve static content at a stable public URL, so this repo is that shared publication host for the [Sanskrit Lexicon organization](https://github.com/sanskrit-lexicon): commit an HTML report here, and it is live at `https://sanskrit-lexicon.github.io/<subdirectory>/<file>` with no build step. It holds no scripts of its own — the code that produced each report lives in its source repo; only the rendered output is committed here.

## What's here

| Directory | Contents |
|---|---|
| [`cologne/`](cologne/) | Syntax-highlighted code and data reports for the Cologne pipeline (e.g. [`cologne/highlighter/`](cologne/highlighter/), a client-side text highlighter) |
| [`CORRECTIONS/`](CORRECTIONS/) | HTML reports on correction analysis — [`abnormending/`](CORRECTIONS/abnormending/) (abnormal word-ending audit), [`dhaval/`](CORRECTIONS/dhaval/) (Dhaval Patel's correction analyses), [`ngram/`](CORRECTIONS/ngram/) (pairwise n-gram diff reports across ~30 dictionary pairs, e.g. `allvsMW90_2.html`) |
| [`PWK/`](PWK/) | PWK dictionary cross-reference reports: [`cbisub.html`](PWK/cbisub.html), [`cmbsub.html`](PWK/cmbsub.html), [`pwis_notmw.html`](PWK/pwis_notmw.html) |
| [`VCP/`](VCP/) | VCP dictionary research outputs, e.g. [`vac-vcp-cmp2/`](VCP/vac-vcp-cmp2/) (headword-diff and length-comparison reports) |
| `hwnorm1/` | Headword normalization research reports (`conv3/`, `proberrors/`) |
| `verbs/` | Verb root comparison reports (`vcp_skd/`, `verbs01/`) |
| `gcse/` | Google Custom Search Engine integration |

## Usage example (verified)

Any file here is a static page — "running" it means opening the URL or the local file directly, no server. [`PWK/cbisub.html`](PWK/cbisub.html) is a real, currently-published report: opening its first bytes shows a self-contained table-based HTML page with inline CSS, no external dependencies:

```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" ...>
<html><head>
  <style>
    table.fixed {table-layout:fixed; width:100%; border:1px solid black;}
    ...
  </style>
```

Confirmed live at [`https://sanskrit-lexicon.github.io/PWK/cbisub.html`](https://sanskrit-lexicon.github.io/PWK/cbisub.html) — publishing a new report is just: commit an HTML/data file to the right subdirectory and push to `main`; Pages serves it at the matching path with no separate deploy step.

## Conventions

- No CI, no build pipeline for content in this repo — the [Cologne tooling runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-tooling-runbook.md) governs the org-wide GitHub Issue taxonomy this repo also follows (17 type labels, 4 severity levels, 5 milestones: API Stability, User Experience, Data Quality, Developer Experience, Community).
- Domain labels here are scoped to build-meta concerns: `domain:ci`, `domain:packaging`, `domain:publishing`.
- Org Project: [Tooling Roadmap](https://github.com/orgs/sanskrit-lexicon/projects/9).
- Issue snapshot (2026-05-29): 0 open, 0 closed across all 5 milestones — this repo currently accumulates published reports without an active issue backlog.

---

_Dr. Mārcis Gasūns_
