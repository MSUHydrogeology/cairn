#!/bin/bash
# Builds the packet and launcher for candidate parent X from git objects only.
# Usage: bash build.sh <output-dir>   (default: the folder holding this script)
set -eu
export LC_ALL=C PYTHONDONTWRITEBYTECODE=1
umask 022
X=38965e4a378e1cd89e8a35e2e47614ca362f53c3
REPO=/Users/kendal30/Code/cairn
OUT=${1:-$(cd "$(dirname "$0")" && pwd)}
g() { env -i HOME=/nonexistent GIT_NO_LAZY_FETCH=1 git --no-pager --no-replace-objects \
        -c core.useReplaceRefs=false -c core.hooksPath=/dev/null -c core.fsmonitor=false \
        -C "$REPO" "$@"; }
blobsha() { g cat-file blob "$X:$1" | shasum -a 256 | cut -d' ' -f1; }

# The eleven closure members, in LC_ALL=C order (checked against the template below).
PATHS='bootstrap/REANCHOR_RUNBOOK.md
bootstrap/reanchor-launcher.template.sh
bootstrap/reanchor.sh
bootstrap/tests/_gate_manifest.py
bootstrap/tests/_gate_preflight.py
bootstrap/tests/_gate_reanchor.py
bootstrap/tests/_gate_transition.py
bootstrap/tests/_oracle.py
bootstrap/tests/_oracle_activation.py
bootstrap/tests/_oracle_trust.py
dev/.cairn/allowed_signers'

PROV='fresh-session build from git objects at 38965e4a; builder wrote nothing in the range; same vendor as reader'
[ ${#PROV} -le 120 ] || { echo "provenance too long" >&2; exit 1; }

{
  echo 'schema cairn-authorization-packet/v1'
  echo "provenance $PROV"
  echo 'artifact bootstrap/reanchor.sh'
  echo "artifact_sha256 $(blobsha bootstrap/reanchor.sh)"
  printf '%s\n' "$PATHS" | while IFS= read -r p; do
    echo "member $(blobsha "$p") $p"
  done
} > "$OUT/packet"

PSHA=$(shasum -a 256 "$OUT/packet" | cut -d' ' -f1)
g cat-file blob "$X:bootstrap/reanchor-launcher.template.sh" | sed "s/@PACKET_SHA256@/$PSHA/" > "$OUT/launcher.sh"
chmod 0644 "$OUT/packet" "$OUT/launcher.sh"
echo "packet   sha256 $PSHA"
echo "launcher sha256 $(shasum -a 256 "$OUT/launcher.sh" | cut -d' ' -f1)"
