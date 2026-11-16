#!/usr/bin/env bash
# Read-only ancestry audit of official AROS against the current checkout.
set -euo pipefail
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Run this script from an AROS git checkout." >&2; exit 2
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Working tree has changes; aborting for reproducibility." >&2; exit 2
fi
if ! git remote get-url official >/dev/null 2>&1; then
  git remote add official https://github.com/aros-development-team/AROS.git
fi
if ! git remote get-url deadwood >/dev/null 2>&1; then
  git remote add deadwood https://github.com/deadwood2/AROS.git
fi
git fetch --no-tags official master
git fetch --no-tags deadwood master
echo "HEAD: $(git rev-parse HEAD)"
echo "official/master: $(git rev-parse refs/remotes/official/master)"
echo "deadwood/master: $(git rev-parse refs/remotes/deadwood/master)"
for ref in official/master deadwood/master; do
  if base=$(git merge-base HEAD "$ref"); then
    echo "$ref merge-base: $base"
    git rev-list --left-right --count HEAD..."$ref"
  else
    echo "$ref has no known common ancestor in fetched history"
  fi
done
echo "Candidate official commits (up to 80; not applied):"
git log --format='%h %an %s' --no-merges --max-count=80 HEAD..official/master || true
echo "Audit only: no cherry-pick, merge, reset or checkout performed."
