#!/usr/bin/env python3
"""Add an empty .nojekyll to each dictionary repo's default branch so GitHub
Pages serves the landing page statically (the Jekyll build fails on the large
dictionary data files). Then trigger a Pages rebuild. Idempotent."""
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
OWNER = "sanskrit-lexicon"
REPOS = ["MWS", "PWG", "MW72", "PWK", "SCH", "ApteES", "SKD", "GRA", "WIL", "AP90",
         "BUR", "CAE", "CCS", "MD", "BEN", "BOR", "LRV", "AMAR", "AP", "SHS", "KOW"]
NL_B64 = "Cg=="  # base64 of "\n"


def run(args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout.strip(), r.stderr.strip()


for repo in REPOS:
    full = f"{OWNER}/{repo}"
    _, default, _ = run(["api", f"repos/{full}", "--jq", ".default_branch"])
    # already present?
    exists = subprocess.run(["gh", "api", f"repos/{full}/contents/.nojekyll?ref={default}"],
                            capture_output=True).returncode == 0
    if not exists:
        code, out, err = run(["api", "--method", "PUT", f"repos/{full}/contents/.nojekyll",
            "-f", "message=ci: add .nojekyll so Pages serves the landing page statically",
            "-f", f"content={NL_B64}", "-f", f"branch={default}"])
        state = "added" if code == 0 else f"ERR {err[:70]}"
    else:
        state = "present"
    # trigger rebuild
    rc, _, rerr = run(["api", "--method", "POST", f"repos/{full}/pages/builds"])
    print(f"{repo:8} nojekyll={state:20} rebuild={'queued' if rc==0 else rerr[:40]}")
