#!/usr/bin/env python3
"""Generate a self-contained, SEO + UX optimised landing page (index.html) for a
Cologne Digital Sanskrit Lexicon dictionary repository.

One template, one metadata row per dictionary. No external assets; the only
off-page reference is the shared og:image hosted at the org root.

    python gen_dict_page.py [<repo> ...]   # default: all
"""
import html
import sys
from pathlib import Path

ORG = "https://sanskrit-lexicon.github.io"
CARD = f"{ORG}/cdsl-card.png"
COLOGNE = "https://www.sanskrit-lexicon.uni-koeln.de"


def cologne(code, year):
    return f"{COLOGNE}/scans/{code}Scan/{year}/web/webtc/indexcaller.php"


# repo -> metadata. `cologne` = verified live reader URL (from the CDSL homepage
# code+year map); None where the dictionary is not yet published live.
DICTS = {
    "MWS": dict(abbr="MW", title="Monier-Williams Sanskrit–English Dictionary",
        author="Sir Monier Monier-Williams", year="1899", place="Oxford", lang="Sanskrit → English",
        cologne=cologne("MW", "2020"),
        desc="A Sanskrit–English Dictionary, etymologically and philologically arranged with special "
             "reference to cognate Indo-European languages (Oxford, 1899) — the most widely used "
             "Sanskrit–English reference work."),
    "MW72": dict(abbr="MW72", title="Monier-Williams Sanskrit–English Dictionary (1872)",
        author="Sir Monier Monier-Williams", year="1872", place="Oxford", lang="Sanskrit → English",
        cologne=cologne("MW72", "2020"),
        desc="The first edition (1872) of Monier-Williams's Sanskrit–English Dictionary, preceding the "
             "expanded 1899 edition — valuable for comparing the growth of the work."),
    "PWG": dict(abbr="PW", title="Sanskrit-Wörterbuch (Großes Petersburger Wörterbuch)",
        author="Otto Böhtlingk & Rudolph Roth", year="1855–1875", place="St. Petersburg", lang="Sanskrit → German",
        cologne=cologne("PWG", "2020"),
        desc="The “Großes Petersburger Wörterbuch” — Böhtlingk and Roth's seven-volume Sanskrit–German "
             "dictionary, the foundational scholarly Sanskrit lexicon from which later dictionaries drew."),
    "PWK": dict(abbr="pw", title="Sanskrit-Wörterbuch in kürzerer Fassung",
        author="Otto Böhtlingk", year="1879–1889", place="St. Petersburg", lang="Sanskrit → German",
        cologne=cologne("PW", "2020"),
        desc="The “kleines” Petersburger Wörterbuch — Böhtlingk's shorter recension of the great "
             "Sanskrit–German dictionary, without the full citation apparatus of the PWG."),
    "SCH": dict(abbr="SCH", title="Nachträge zum Sanskrit-Wörterbuch in kürzerer Fassung",
        author="Richard Schmidt", year="1928", place="Leipzig", lang="Sanskrit → German",
        cologne=cologne("SCH", "2020"),
        desc="Richard Schmidt's supplement (Nachträge) to Böhtlingk's shorter Petersburg dictionary, "
             "adding words and references gathered after its publication."),
    "AP": dict(abbr="AP", title="The Practical Sanskrit–English Dictionary (Revised & Enlarged)",
        author="Vaman Shivram Apte", year="1957", place="Poona", lang="Sanskrit → English",
        cologne=cologne("AP", "2020"),
        desc="The revised and enlarged edition (1957) of Apte's Practical Sanskrit–English Dictionary, "
             "a standard classroom and scholarly reference."),
    "AP90": dict(abbr="AP90", title="The Practical Sanskrit–English Dictionary (1890)",
        author="Vaman Shivram Apte", year="1890", place="Poona", lang="Sanskrit → English",
        cologne=cologne("AP90", "2020"),
        desc="The original 1890 edition of Apte's Practical Sanskrit–English Dictionary, before the "
             "later revision — a widely cited Sanskrit–English reference."),
    "ApteES": dict(abbr="AE", title="The Student's English–Sanskrit Dictionary",
        author="Vaman Shivram Apte", year="1884", place="Poona", lang="English → Sanskrit",
        cologne=cologne("AE", "2020"),
        desc="Apte's English–Sanskrit dictionary, giving Sanskrit equivalents for English words — the "
             "reverse-direction companion to his Sanskrit–English work."),
    "WIL": dict(abbr="WIL", title="A Dictionary in Sanscrit and English",
        author="Horace Hayman Wilson", year="1832", place="Calcutta", lang="Sanskrit → English",
        cologne=cologne("WIL", "2020"),
        desc="Wilson's Sanskrit–English dictionary (2nd edition, 1832), one of the earliest comprehensive "
             "Sanskrit–English lexicons in the European scholarly tradition."),
    "BEN": dict(abbr="BEN", title="A Sanskrit–English Dictionary",
        author="Theodor Benfey", year="1866", place="London", lang="Sanskrit → English",
        cologne=cologne("BEN", "2020"),
        desc="Benfey's Sanskrit–English dictionary (1866), with special reference to the older language "
             "and etymology."),
    "MD": dict(abbr="MD", title="A Practical Sanskrit Dictionary",
        author="Arthur Anthony Macdonell", year="1893", place="Oxford", lang="Sanskrit → English",
        cologne=cologne("MD", "2020"),
        desc="Macdonell's Practical Sanskrit Dictionary, with transliteration, accentuation, and "
             "etymological analysis — a concise reference for students of the classical language."),
    "CAE": dict(abbr="CAE", title="A Sanskrit–English Dictionary",
        author="Carl Cappeller", year="1891", place="Strassburg", lang="Sanskrit → English",
        cologne=cologne("CAE", "2020"),
        desc="Cappeller's Sanskrit–English dictionary (1891), based on the Petersburg lexicons and "
             "compiled for practical use."),
    "CCS": dict(abbr="CCS", title="Sanskrit-Wörterbuch",
        author="Carl Cappeller", year="1887", place="Strassburg", lang="Sanskrit → German",
        cologne=cologne("CCS", "2020"),
        desc="Cappeller's Sanskrit–German dictionary (1887), a compact scholarly lexicon drawing on the "
             "Petersburg tradition."),
    "GRA": dict(abbr="GRA", title="Wörterbuch zum Rig-Veda",
        author="Hermann Grassmann", year="1873", place="Leipzig", lang="Vedic Sanskrit → German",
        cologne=cologne("GRA", "2020"),
        desc="Grassmann's dictionary to the Ṛgveda (1873) — a complete concordance-dictionary of the "
             "Ṛgvedic vocabulary, indispensable for Vedic studies."),
    "SKD": dict(abbr="SKD", title="Śabdakalpadruma",
        author="Rājā Rādhākānta Deva", year="1822–1858", place="Calcutta", lang="Sanskrit → Sanskrit",
        cologne=cologne("SKD", "2020"),
        desc="The Śabdakalpadruma, Rādhākānta Deva's monumental Sanskrit encyclopaedic lexicon "
             "(kosha), defining Sanskrit terms in Sanskrit with copious textual citation."),
    "SHS": dict(abbr="SHS", title="The Śabda-Sāgara: A Comprehensive Sanskrit–English Lexicon",
        author="", year="1900", place="Calcutta", lang="Sanskrit → English",
        cologne=cologne("SHS", "2020"),
        desc="The Śabda-Sāgara, a comprehensive Sanskrit–English lexicon compiled from earlier "
             "dictionaries and native sources."),
    "LRV": dict(abbr="LRV", title="The Standard Sanskrit–English Dictionary",
        author="L. R. Vaidya", year="1889", place="Bombay", lang="Sanskrit → English",
        cologne=cologne("LRV", "2022"),
        desc="Vaidya's Standard Sanskrit–English Dictionary, compiled for students and containing "
             "grammatical and etymological notes."),
    "BOR": dict(abbr="BOR", title="A Practical English–Sanskrit Dictionary",
        author="Anundoram Borooah", year="1877–1887", place="Calcutta", lang="English → Sanskrit",
        cologne=cologne("BOR", "2020"),
        desc="Borooah's Practical English–Sanskrit Dictionary, giving Sanskrit renderings for English "
             "words with illustrative usage."),
    "BUR": dict(abbr="BUR", title="Dictionnaire classique sanscrit-français",
        author="Émile Burnouf & Leupol", year="1866", place="Paris", lang="Sanskrit → French",
        cologne=None,
        desc="Burnouf's classical Sanskrit–French dictionary (1866), a standard reference of the French "
             "Indological tradition. (Digitisation and correction in progress.)"),
    "AMAR": dict(abbr="AMAR", title="Amarakośa (Nāmaliṅgānuśāsana)",
        author="Amarasiṃha", year="c. 4th–6th c. CE", place="", lang="Sanskrit → Sanskrit",
        cologne=None,
        desc="The Amarakośa, Amarasiṃha's celebrated versified thesaurus of Sanskrit synonyms — the "
             "most influential of the indigenous koshas. (Conversion to CDSL format in progress.)"),
    "KOW": dict(abbr="KOW", title="Sanskrit–Russian Dictionary",
        author="Kaetan Kossowicz", year="1854–1856", place="St. Petersburg", lang="Sanskrit → Russian",
        cologne=None,
        desc="Kossowicz's Sanskrit–Russian dictionary, an early lexicon of the Russian Indological "
             "tradition. (Digitisation and correction in progress.)"),
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} ({abbr}) · Cologne Digital Sanskrit Lexicon</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#1f78b4">
<meta name="author" content="{author_attr}">
<meta name="robots" content="index,follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Cologne Digital Sanskrit Lexicon">
<meta property="og:locale" content="en">
<meta property="og:title" content="{title} ({abbr})">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{card}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Cologne Digital Sanskrit Lexicon">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} ({abbr})">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="{card}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Book","name":"{title}","alternateName":"{abbr}","inLanguage":"sa","publisher":{{"@type":"Organization","name":"Cologne Digital Sanskrit Lexicon"}},"url":"{canonical}","isAccessibleForFree":true,"license":"https://creativecommons.org/licenses/by-sa/4.0/"}}
</script>
<style>
  :root {{ --ink:#1b2a38; --muted:#5a6b7a; --accent:#1f78b4; --bg:#f7f9fb; --card:#fff; --line:#e2e8ee; }}
  * {{ box-sizing:border-box; }}
  html {{ -webkit-text-size-adjust:100%; }}
  body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    color:var(--ink); background:var(--bg); line-height:1.6; }}
  a {{ color:var(--accent); }}
  .wrap {{ max-width:760px; margin:0 auto; padding:0 20px; }}
  header.top {{ border-bottom:1px solid var(--line); background:var(--card); }}
  header.top .wrap {{ display:flex; align-items:center; gap:.5rem; height:56px; font-size:.95rem; }}
  header.top a {{ color:var(--muted); text-decoration:none; font-weight:600; }}
  .hero {{ background:linear-gradient(160deg,#1e2f40,#2d4e6e); color:#f4f7fa; padding:56px 0 48px; }}
  .badge {{ display:inline-block; font-weight:700; letter-spacing:.08em; font-size:.8rem;
    background:rgba(255,255,255,.14); color:#cfe3f2; padding:.35rem .7rem; border-radius:999px; }}
  .hero h1 {{ font-family:Georgia,"Times New Roman",serif; font-size:2.1rem; line-height:1.2; margin:.9rem 0 .5rem; }}
  .hero .sub {{ color:#b7cddf; font-size:1.05rem; margin:0 0 1.2rem; }}
  .hero p.desc {{ color:#dbe6f0; margin:0; max-width:62ch; }}
  .cta {{ display:flex; flex-wrap:wrap; gap:.7rem; margin:1.6rem 0 0; }}
  .btn {{ display:inline-block; padding:.7rem 1.1rem; border-radius:8px; text-decoration:none; font-weight:600; font-size:.95rem; }}
  .btn.primary {{ background:#4aa3df; color:#0b1b28; }}
  .btn.ghost {{ background:rgba(255,255,255,.10); color:#eaf2f8; border:1px solid rgba(255,255,255,.25); }}
  main {{ padding:40px 0 20px; }}
  .facts {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:1px;
    background:var(--line); border:1px solid var(--line); border-radius:10px; overflow:hidden; margin:0 0 28px; }}
  .facts div {{ background:var(--card); padding:14px 16px; }}
  .facts dt {{ font-size:.72rem; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); }}
  .facts dd {{ margin:.2rem 0 0; font-weight:600; }}
  section h2 {{ font-size:1.15rem; margin:1.8rem 0 .5rem; }}
  .note {{ color:var(--muted); font-size:.95rem; }}
  footer {{ border-top:1px solid var(--line); background:var(--card); margin-top:32px; }}
  footer .wrap {{ padding:22px 20px; color:var(--muted); font-size:.9rem; }}
  footer a {{ color:var(--muted); }}
  @media (max-width:520px) {{ .hero h1 {{ font-size:1.7rem; }} }}
</style>
</head>
<body>
<header class="top"><div class="wrap"><a href="{org}/">← Cologne Digital Sanskrit Lexicon</a></div></header>
<div class="hero"><div class="wrap">
  <span class="badge">{abbr}</span>
  <h1>{title_h}</h1>
  <p class="sub">{sub_h}</p>
  <p class="desc">{desc_h}</p>
  <div class="cta">
    {browse_btn}
    <a class="btn ghost" href="{repo}">Source &amp; corrections (GitHub)</a>
    <a class="btn ghost" href="{org}/">All dictionaries</a>
  </div>
</div></div>
<main><div class="wrap">
  <dl class="facts">
    <div><dt>Abbreviation</dt><dd>{abbr}</dd></div>
    <div><dt>Direction</dt><dd>{lang_h}</dd></div>
    <div><dt>First published</dt><dd>{year_h}</dd></div>
    <div><dt>Digitised by</dt><dd>CDSL</dd></div>
  </dl>
  <section>
    <h2>About this edition</h2>
    <p class="note">This is the digital home of the <strong>{title_h}</strong> ({abbr}) within the
    <a href="https://www.sanskrit-lexicon.uni-koeln.de/">Cologne Digital Sanskrit Lexicon</a> (CDSL),
    a volunteer project that digitises, corrects, and openly publishes the foundational Sanskrit
    dictionaries as citable, reproducible data. Corrections are tracked as change files in this
    repository; the searchable text is served on the Cologne site.</p>
    <h2>Use &amp; reuse</h2>
    <p class="note">Dictionary data is released under
    <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a> unless noted otherwise.
    Report errors or contribute corrections via the
    <a href="{repo}/issues">GitHub issue tracker</a>.</p>
  </section>
</div></main>
<footer><div class="wrap">
  Part of the <a href="{org}/">Cologne Digital Sanskrit Lexicon</a> ·
  <a href="https://www.sanskrit-lexicon.uni-koeln.de/">sanskrit-lexicon.uni-koeln.de</a> ·
  <a href="https://github.com/sanskrit-lexicon">GitHub</a>
</div></footer>
</body>
</html>
"""


def esc_attr(s):
    return html.escape(s or "", quote=True)


def esc_text(s):
    return html.escape(s or "", quote=False)


def build(repo):
    d = DICTS[repo]
    canonical = f"{ORG}/{repo}/"
    repo_url = f"https://github.com/sanskrit-lexicon/{repo}"
    # subtitle from available parts
    place_year = ", ".join(p for p in [d.get("place"), d.get("year")] if p)
    sub = " · ".join(p for p in [d.get("author"), place_year] if p)
    if d.get("cologne"):
        browse = f'<a class="btn primary" href="{d["cologne"]}">Browse the dictionary →</a>'
    else:
        browse = (f'<a class="btn primary" href="{COLOGNE}/">Browse on the Cologne site →</a>')
    ctx = dict(
        abbr=esc_attr(d["abbr"]), title=esc_attr(d["title"]), author_attr=esc_attr(d.get("author") or "CDSL"),
        meta_desc=esc_attr(d["desc"]), canonical=canonical, card=CARD, org=ORG, repo=repo_url,
        title_h=esc_text(d["title"]), sub_h=esc_text(sub), desc_h=esc_text(d["desc"]),
        lang_h=esc_text(d["lang"]), year_h=esc_text(d.get("year") or "—"), browse_btn=browse,
    )
    return TEMPLATE.format(**ctx)


# --- Org-root hub page (index.html linking every dictionary + the tool sites) ---

# Analysis / tool sites in the org, linked from the hub.
TOOLS = [
    ("csl-app", "Dictionary app", "Search 49 dictionaries in your browser — offline-capable, no install."),
    ("csl-guides", "Guides & docs", "User, contributor, and developer documentation for the CDSL."),
    ("csl-atlas", "Atlas", "Comparative microstructural analysis across the Cologne dictionaries."),
    ("csl-observatory", "Observatory", "Repository, contributor, and correction-quality metrics for the ecosystem."),
]


def _group_key(lang):
    if "→ English" in lang:
        return (0, "Sanskrit–English dictionaries")
    if "→ German" in lang:
        return (1, "Sanskrit–German dictionaries")
    if lang == "Sanskrit → Sanskrit":
        return (2, "Indigenous Sanskrit thesauri (kośa)")
    if lang.startswith("English →"):
        return (3, "English–Sanskrit dictionaries")
    return (4, "Other languages")


HUB = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cologne Digital Sanskrit Lexicon — the open Sanskrit dictionaries</title>
<meta name="description" content="The Cologne Digital Sanskrit Lexicon (CDSL): the open, canonical corpus of Sanskrit dictionaries — Monier-Williams, the Petersburg Wörterbücher, the koshas and more — digitised, corrected, and freely reusable.">
<link rel="canonical" href="{org}/">
<meta name="theme-color" content="#1f78b4">
<meta name="robots" content="index,follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Cologne Digital Sanskrit Lexicon">
<meta property="og:locale" content="en">
<meta property="og:title" content="Cologne Digital Sanskrit Lexicon">
<meta property="og:description" content="The open, canonical corpus of Sanskrit dictionaries — digitised, corrected, and freely reusable.">
<meta property="og:url" content="{org}/">
<meta property="og:image" content="{card}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Cologne Digital Sanskrit Lexicon">
<meta name="twitter:description" content="The open, canonical corpus of Sanskrit dictionaries — digitised, corrected, and freely reusable.">
<meta name="twitter:image" content="{card}">
<style>
  :root {{ --ink:#1b2a38; --muted:#5a6b7a; --accent:#1f78b4; --bg:#f7f9fb; --card:#fff; --line:#e2e8ee; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; color:var(--ink); background:var(--bg); line-height:1.6; }}
  a {{ color:var(--accent); }}
  .wrap {{ max-width:960px; margin:0 auto; padding:0 20px; }}
  .hero {{ background:linear-gradient(160deg,#1e2f40,#2d4e6e); color:#f4f7fa; padding:60px 0 52px; }}
  .hero h1 {{ font-family:Georgia,"Times New Roman",serif; font-size:2.3rem; line-height:1.15; margin:0 0 .5rem; }}
  .hero p {{ color:#dbe6f0; margin:0; max-width:64ch; font-size:1.08rem; }}
  .cta {{ display:flex; flex-wrap:wrap; gap:.7rem; margin:1.6rem 0 0; }}
  .btn {{ display:inline-block; padding:.7rem 1.1rem; border-radius:8px; text-decoration:none; font-weight:600; font-size:.95rem; }}
  .btn.primary {{ background:#4aa3df; color:#0b1b28; }}
  .btn.ghost {{ background:rgba(255,255,255,.10); color:#eaf2f8; border:1px solid rgba(255,255,255,.25); }}
  main {{ padding:44px 0 20px; }}
  h2 {{ font-size:1.3rem; margin:2.2rem 0 .3rem; }}
  h2:first-child {{ margin-top:0; }}
  .sub {{ color:var(--muted); margin:.1rem 0 1rem; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:12px; }}
  .dcard {{ display:block; background:var(--card); border:1px solid var(--line); border-radius:10px; padding:14px 16px; text-decoration:none; color:inherit; transition:border-color .15s,box-shadow .15s; }}
  .dcard:hover {{ border-color:#9cc3e0; box-shadow:0 2px 10px rgba(31,120,180,.08); }}
  .dabbr {{ display:inline-block; font-weight:700; font-size:.72rem; letter-spacing:.06em; color:#2d6a9a; background:#eaf3fa; padding:.15rem .5rem; border-radius:999px; }}
  .dtitle {{ display:block; font-weight:600; margin:.5rem 0 .15rem; }}
  .dmeta {{ display:block; color:var(--muted); font-size:.85rem; }}
  footer {{ border-top:1px solid var(--line); background:var(--card); margin-top:36px; }}
  footer .wrap {{ padding:22px 20px; color:var(--muted); font-size:.9rem; }}
  footer a {{ color:var(--muted); }}
  @media (max-width:520px) {{ .hero h1 {{ font-size:1.85rem; }} }}
</style>
</head>
<body>
<div class="hero"><div class="wrap">
  <h1>Cologne Digital Sanskrit Lexicon</h1>
  <p>The open, canonical corpus of Sanskrit dictionaries — Monier-Williams, the Petersburg
  Wörterbücher, the classical <em>kośa</em>s and more — digitised, corrected, and published as
  citable, reproducible open data.</p>
  <div class="cta">
    <a class="btn primary" href="https://www.sanskrit-lexicon.uni-koeln.de/">Search the dictionaries →</a>
    <a class="btn ghost" href="https://github.com/sanskrit-lexicon">GitHub organization</a>
  </div>
</div></div>
<main><div class="wrap">
{sections}
  <h2>Analysis &amp; tools</h2>
  <p class="sub">Apps and research surfaces built on the corpus.</p>
  <div class="grid">
{tools}
  </div>
</div></main>
<footer><div class="wrap">
  Cologne Digital Sanskrit Lexicon ·
  <a href="https://www.sanskrit-lexicon.uni-koeln.de/">sanskrit-lexicon.uni-koeln.de</a> ·
  <a href="https://github.com/sanskrit-lexicon">GitHub</a> ·
  data under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>
</div></footer>
</body>
</html>
"""


def build_hub():
    # bucket dictionaries by direction, preserving DICTS insertion order within groups
    groups = {}
    for repo, d in DICTS.items():
        order, label = _group_key(d["lang"])
        groups.setdefault((order, label), []).append(repo)
    sections = []
    for (order, label) in sorted(groups):
        cards = []
        for repo in groups[(order, label)]:
            d = DICTS[repo]
            py = ", ".join(p for p in [d.get("place"), d.get("year")] if p)
            meta = " · ".join(p for p in [d.get("author"), py] if p)
            cards.append(
                f'    <a class="dcard" href="{ORG}/{repo}/">'
                f'<span class="dabbr">{esc_text(d["abbr"])}</span>'
                f'<span class="dtitle">{esc_text(d["title"])}</span>'
                f'<span class="dmeta">{esc_text(meta)}</span></a>')
        sections.append(f'  <h2>{esc_text(label)}</h2>\n  <div class="grid">\n'
                        + "\n".join(cards) + "\n  </div>")
    tools = "\n".join(
        f'    <a class="dcard" href="{ORG}/{slug}/">'
        f'<span class="dtitle">{esc_text(name)}</span>'
        f'<span class="dmeta">{esc_text(desc)}</span></a>'
        for slug, name, desc in TOOLS)
    return HUB.format(org=ORG, card=CARD, sections="\n".join(sections), tools=tools)


if __name__ == "__main__":
    args = sys.argv[1:]
    base = Path(__file__).resolve().parent / "out"
    if args and args[0] == "--hub":
        base.mkdir(parents=True, exist_ok=True)
        (base / "index.html").write_text(build_hub(), encoding="utf-8")
        print(f"wrote {base / 'index.html'} (org-root hub)")
    else:
        for repo in (args or list(DICTS)):
            out = base / repo
            out.mkdir(parents=True, exist_ok=True)
            (out / "index.html").write_text(build(repo), encoding="utf-8")
            print(f"wrote {out / 'index.html'}")
