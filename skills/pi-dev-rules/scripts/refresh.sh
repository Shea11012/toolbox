#!/usr/bin/env bash
# Refresh references from the installed Pi version, without network access.
# Usage: bash scripts/refresh.sh [pi-package-root-or-docs-dir] [output-dir]
# With no source argument, resolve the installed package from pi on PATH.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build-references.py "$@"
printf '%s\n' \
  'Review git diff and align SKILL.md docVersion/docsRefreshed and README versions with the source.' \
  'The npm gallery is independent; refresh it separately with scripts/fetch-pi-packages.py.'
