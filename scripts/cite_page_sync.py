#!/usr/bin/env python3
"""H7887 — generate/verify the standalone Cite & DOI page (cite.html).

Single source of truth is index.html's `#cite` table: this script extracts the
DOI rows and the umbrella DOI from it and renders cite.html deterministically.
`--check` regenerates and byte-compares, failing loud when the two surfaces
drift (the uni-koeln PR #28 -> clobbered-by-819eba7 regression class, guarded
on the hub side too). No generator for the table existed before this (H6121
built it ad-hoc); keep cite.html in sync by re-running this script after any
index.html `#cite` edit.
"""
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = f"{HERE}/../index.html"
PAGE = f"{HERE}/../cite.html"
BASE = "https://sanskrit-lexicon.github.io"
UMBRELLA_HINT = "10.5281/zenodo.21319331"
DOI_RE = re.compile(r"10\.5281/zenodo\.\d+")


def extract():
    with open(INDEX, encoding="utf-8") as f:
        html = f.read()
    m = re.search(r'<h2 id="cite">.*?<tbody>(.*?)</tbody>', html, re.S)
    if not m:
        raise SystemExit("no #cite table tbody found in index.html")
    tbody = m.group(1)
    rows = re.findall(r"<tr>.*?</tr>", tbody, re.S)
    href_re = re.compile(r'href="https://doi\.org/(10\.5281/zenodo\.\d+)"')
    umbrellas = href_re.findall(rows[0])
    if not umbrellas or umbrellas[0] != UMBRELLA_HINT:
        raise SystemExit(f"first #cite row is not the umbrella row: {umbrellas[:1]}")
    dois = [d for r in rows for d in href_re.findall(r)]
    if len(dois) != len(rows):
        raise SystemExit("every #cite row must carry exactly one DOI")
    return rows, dois


def jsonld(dois):
    per_dict = [
        {"@type": "Dataset", "identifier": d, "url": f"https://doi.org/{d}"}
        for d in dois[1:]
    ]
    graph = [
        {
            "@type": "Organization",
            "@id": f"{BASE}/#organization",
            "name": "Cologne Digital Sanskrit Lexicon",
            "alternateName": ["CDSL", "sanskrit-lexicon"],
            "url": f"{BASE}/",
        },
        {
            "@type": "WebPage",
            "@id": f"{BASE}/cite.html#webpage",
            "url": f"{BASE}/cite.html",
            "name": "Cite & DOI — Cologne Digital Sanskrit Dictionaries",
            "inLanguage": "en",
            "isPartOf": {"@id": f"{BASE}/#website"},
            "about": {
                "@type": "Dataset",
                "name": "Cologne Digital Sanskrit Dictionaries (CDSL)",
                "identifier": dois[0],
                "url": f"https://doi.org/{dois[0]}",
                "hasPart": per_dict,
                "isAccessibleForFree": True,
            },
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      indent=2, ensure_ascii=False)


def render(rows, dois):
    tbody = "\n".join(f"      {r}" for r in rows)
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cite &amp; DOI — Cologne Digital Sanskrit Dictionaries</title>
<meta name="description" content="Zenodo concept DOIs for the Cologne Digital Sanskrit Lexicon (CDSL) dictionaries and the corpus umbrella DOI — deep-linkable citation page.">
<link rel="canonical" href="{BASE}/cite.html">
<meta name="theme-color" content="#1f78b4">
<meta name="robots" content="index,follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Cologne Digital Sanskrit Lexicon">
<meta property="og:locale" content="en">
<meta property="og:title" content="Cite &amp; DOI — Cologne Digital Sanskrit Dictionaries">
<meta property="og:description" content="Every CDSL dictionary carries a Zenodo concept DOI; the whole corpus is citable under the umbrella DOI {UMBRELLA_HINT}.">
<meta property="og:url" content="{BASE}/cite.html">
<style>
  :root {{ --ink:#1b2a38; --muted:#5a6b7a; --accent:#1f78b4; --bg:#f7f9fb; --card:#fff; --line:#e2e8ee; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; color:var(--ink); background:var(--bg); line-height:1.6; }}
  a {{ color:var(--accent); }}
  .wrap {{ max-width:960px; margin:0 auto; padding:0 20px; }}
  .hero {{ background:linear-gradient(160deg,#1e2f40,#2d4e6e); color:#f4f7fa; padding:48px 0 40px; }}
  .hero h1 {{ font-family:Georgia,"Times New Roman",serif; font-size:2rem; line-height:1.15; margin:0 0 .5rem; }}
  .hero p {{ color:#dbe6f0; margin:0; max-width:70ch; font-size:1.05rem; }}
  .hero .cite {{ display:block; margin-top:1.1rem; color:#dbe6f0; font-size:1.02rem; }}
  .hero .cite a {{ color:#8ecdf5; }}
  main {{ padding:36px 0 20px; }}
  h2 {{ font-size:1.25rem; margin:1.6rem 0 .3rem; }}
  .sub {{ color:var(--muted); margin:.1rem 0 1rem; }}
  .dotable {{ width:100%; border-collapse:collapse; background:var(--card); border:1px solid var(--line); font-size:.9rem; }}
  .dotable th, .dotable td {{ text-align:left; padding:.45rem .7rem; border-bottom:1px solid var(--line); vertical-align:top; }}
  .dotable th {{ background:#eaf3fa; color:#2d6a9a; font-size:.8rem; letter-spacing:.04em; }}
  .dotable .doi {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.82rem; white-space:nowrap; }}
  footer {{ border-top:1px solid var(--line); background:var(--card); margin-top:36px; }}
  footer .wrap {{ padding:22px 20px; color:var(--muted); font-size:.9rem; }}
  footer a {{ color:var(--muted); }}
  @media (max-width:520px) {{ .hero h1 {{ font-size:1.6rem; }} }}
</style>
<script type="application/ld+json">
{jsonld(dois)}
</script>
</head>
<body>
<div class="hero"><div class="wrap">
  <h1>Cite &amp; DOI</h1>
  <p>Citable identifiers for the Cologne Digital Sanskrit Lexicon. Every dictionary
  carries a Zenodo concept DOI that always resolves to its latest version.</p>
  <span class="cite">Cite the corpus: <a href="https://doi.org/{UMBRELLA_HINT}">DOI {UMBRELLA_HINT}</a></span>
</div></div>
<main><div class="wrap">
  <h2>Dictionary DOIs</h2>
  <p class="sub">Umbrella row first, then one concept DOI per dictionary. This page is
  generated from the hub's <code>#cite</code> table by
  <code>scripts/cite_page_sync.py</code> — edit the table there, then re-run it.</p>
  <table class="dotable">
    <thead><tr><th>Code</th><th>Dictionary</th><th>DOI</th></tr></thead>
    <tbody>
{tbody}
    </tbody>
  </table>
</div></main>
<footer><div class="wrap">
  <a href="{BASE}/">&larr; Cologne Digital Sanskrit Lexicon</a> ·
  <a href="https://www.sanskrit-lexicon.uni-koeln.de/">sanskrit-lexicon.uni-koeln.de</a> ·
  <a href="https://github.com/sanskrit-lexicon/sanskrit-lexicon.github.io">source</a>
</div></footer>
</body>
</html>
"""
    return page


def main():
    rows, dois = extract()
    page = render(rows, dois)
    if "--check" in sys.argv:
        with open(PAGE, encoding="utf-8") as f:
            current = f.read()
        if current != page:
            sys.exit(f"DRIFT: cite.html is out of sync with index.html #cite "
                     f"({len(dois)} DOI rows); re-run scripts/cite_page_sync.py")
        m = re.search(r'<script type="application/ld\+json">\n(.*?)\n</script>',
                      page, re.S)
        json.loads(m.group(1))  # well-formed by construction; belt and braces
        print(f"CHECK OK: cite.html in sync ({len(dois)} DOI rows, JSON-LD valid)")
        return
    with open(PAGE, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    print(f"wrote cite.html with {len(dois)} DOI rows (umbrella {dois[0]})")


if __name__ == "__main__":
    main()
