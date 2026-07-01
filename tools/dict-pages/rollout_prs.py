#!/usr/bin/env python3
"""Phase 1 of the dictionary-landing-page rollout: for each repo, create a
branch, add the generated index.html, and open a PR. Non-destructive (no merge,
no Pages enable). Skips repos that already have a root index.html. Idempotent-ish:
reuses the branch if it already exists.
"""
import base64
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
OWNER = "sanskrit-lexicon"
BRANCH = "codex/landing-page"
OUT = Path(__file__).resolve().parent / "out"
REPOS = ["MW72", "PWK", "SCH", "ApteES", "SKD", "GRA", "WIL", "AP90", "BUR",
         "CAE", "CCS", "MD", "BEN", "BOR", "LRV", "AMAR", "AP", "SHS", "KOW"]

PR_TITLE = "Add SEO/UX landing page for GitHub Pages"
PR_BODY = ("Adds a self-contained, mobile-friendly landing page (`index.html`) with full SEO "
           "(canonical, Open Graph, Twitter `summary_large_image`, JSON-LD `Book`) and a clean hero "
           "linking to the live dictionary on the Cologne site, the source repo, and the CDSL hub. "
           "`og:image` is the shared card at the org root. No dependencies, no build step.\n\n"
           "Part of an org-wide pass giving every dictionary repo an optimised landing page. "
           "GitHub Pages will be enabled on merge.\n\n"
           "🤖 Generated with [Claude Code](https://claude.com/claude-code)")


def gh(args, check=True):
    r = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode != 0:
        return None, r.stderr.strip()
    return r.stdout.strip(), r.stderr.strip()


def path_exists(full, path, ref):
    """True only when the contents endpoint returns HTTP 200 (file present)."""
    r = subprocess.run(["gh", "api", f"repos/{full}/contents/{path}?ref={ref}"],
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode == 0


results = []
for repo in REPOS:
    full = f"{OWNER}/{repo}"
    out, err = gh(["api", f"repos/{full}", "--jq", "{d:.default_branch,p:.has_pages}"])
    if out is None:
        results.append((repo, "ERR repo", err)); print(repo, "ERR repo", err); continue
    meta = json.loads(out)
    default = meta["d"]
    # skip if a root index.html already exists (don't clobber)
    if path_exists(full, "index.html", default):
        results.append((repo, "SKIP index exists", "")); print(repo, "SKIP index exists"); continue
    sha, err = gh(["api", f"repos/{full}/git/refs/heads/{default}", "--jq", ".object.sha"])
    if not sha:
        results.append((repo, "ERR sha", err)); print(repo, "ERR sha", err); continue
    # create branch (ignore 'already exists')
    gh(["api", "--method", "POST", f"repos/{full}/git/refs",
        "-f", f"ref=refs/heads/{BRANCH}", "-f", f"sha={sha}"], check=False)
    # put index.html on the branch
    content = (OUT / repo / "index.html").read_text(encoding="utf-8")
    b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")
    put, err = gh(["api", "--method", "PUT", f"repos/{full}/contents/index.html",
        "-f", "message=seo: add SEO/UX-optimised landing page for GitHub Pages",
        "-f", f"content={b64}", "-f", f"branch={BRANCH}"], check=False)
    if put is None or ('"content"' not in (put or "") and "commit" not in (put or "")):
        # verify it actually landed
        chk, _ = gh(["api", f"repos/{full}/contents/index.html?ref={BRANCH}", "--jq", ".sha"], check=False)
        if not chk:
            results.append((repo, "ERR put", err)); print(repo, "ERR put", err); continue
    # open PR
    pr, err = gh(["pr", "create", "-R", full, "--base", default, "--head", BRANCH,
                  "--title", PR_TITLE, "--body", PR_BODY], check=False)
    if pr and pr.startswith("http"):
        results.append((repo, "PR", pr)); print(repo, "PR", pr)
    else:
        # maybe PR already exists
        existing, _ = gh(["pr", "view", BRANCH, "-R", full, "--json", "url", "--jq", ".url"], check=False)
        results.append((repo, "PR?", existing or err)); print(repo, "PR?", existing or err)

print("\n=== SUMMARY ===")
for r, status, info in results:
    print(f"{r:8} {status:20} {info}")
