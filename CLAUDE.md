# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**sanskrit-lexicon.github.io** is the GitHub Pages repository for the [Sanskrit Lexicon organization](https://github.com/sanskrit-lexicon). It hosts static HTML reports, research outputs, and data summaries that are publicly accessible at `https://sanskrit-lexicon.github.io/`.

## Architecture

Each subdirectory corresponds to a project or dictionary and contains static HTML pages, data files, or reports published via GitHub Pages:

| Directory | Contents |
|---|---|
| `cologne/` | Syntax-highlighted code and data reports for the Cologne pipeline |
| `CORRECTIONS/` | HTML reports on correction analysis (abnormal endings, n-grams, Dhaval's analysis) |
| `PWK/` | PWK dictionary cross-reference reports (`cbisub.html`, `cmbsub.html`, `pwis_notmw.html`) |
| `VCP/` | VCP dictionary research outputs |
| `hwnorm1/` | Headword normalization research reports (`conv3/`, `proberrors/`) |
| `verbs/` | Verb root comparison reports (`vcp_skd/`, `verbs01/`) |
| `gcse/` | Google Custom Search Engine integration |

### GitHub Pages

Content is served directly from the `master`/`main` branch at `https://sanskrit-lexicon.github.io/<subdirectory>/<file>`. To publish a new report, commit HTML/data files to the appropriate subdirectory.

## Notes

This repo does not contain scripts — it is a static content host. Research scripts live in their respective dictionary or tool repos; outputs are committed here for publication.
