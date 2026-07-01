#!/usr/bin/env python3
"""Phase 2: merge each landing-page PR and enable GitHub Pages (source = default
branch, path /). User-authorised full rollout. Continue-on-error with a summary.
"""
import json
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
OWNER = "sanskrit-lexicon"
BRANCH = "codex/landing-page"
REPOS = ["MW72", "PWK", "SCH", "ApteES", "SKD", "GRA", "WIL", "AP90", "BUR",
         "CAE", "CCS", "MD", "BEN", "BOR", "LRV", "AMAR", "AP", "SHS", "KOW"]


def run(args, inp=None):
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", input=inp)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


results = []
for repo in REPOS:
    full = f"{OWNER}/{repo}"
    # 1. merge the PR
    code, out, err = run(["gh", "pr", "merge", BRANCH, "-R", full, "--merge", "--delete-branch"])
    merged = code == 0 or "not open" in (err.lower() + out.lower()) or "merged" in (err.lower() + out.lower())
    # confirm merge state
    _, st, _ = run(["gh", "pr", "view", BRANCH, "-R", full, "--json", "state", "--jq", ".state"])
    mstate = st or ("MERGED?" if merged else "FAILED")
    # 2. enable Pages (default branch, path /)
    _, default, _ = run(["gh", "api", f"repos/{full}", "--jq", ".default_branch"])
    body = json.dumps({"source": {"branch": default, "path": "/"}})
    pcode, pout, perr = run(["gh", "api", "--method", "POST", f"repos/{full}/pages", "--input", "-"], inp=body)
    if pcode == 0:
        pages = "ENABLED"
    elif "409" in perr or "already" in perr.lower() or "exists" in perr.lower():
        pages = "already-on"
    else:
        pages = f"PAGES-ERR {perr[:80]}"
    results.append((repo, mstate, pages))
    print(f"{repo:8} merge={mstate:8} pages={pages}")

print("\n=== SUMMARY ===")
for r, m, p in results:
    print(f"{r:8} {m:10} {p}")
