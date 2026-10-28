#!/bin/bash
# Phase 5 of the runbook: ONE atomic push of both refs, then read them back from
# the remote. This PUBLISHES: it updates origin's 0.5-dev branch and creates
# origin's refs/cairn/gate-anchor. It is yours to run. It never forces.
#   usage: bash push.sh [values-file]
set -u
CER=$(cd "$(dirname "$0")" && pwd -P)
. "$CER/ceremony.env"
VALUES=${1:-/Users/kendal30/cairn-ceremony-values}
val() { awk -v k="$1" '$1==k { print substr($0, length(k)+2); exit }' "$VALUES"; }
GIT=$(val git); CHECKOUT=$(val checkout)

N=$("$GIT" -C "$CHECKOUT" rev-parse refs/cairn/gate-anchor)
PAR=$("$GIT" -C "$CHECKOUT" rev-list --parents -n1 "$N" | cut -d" " -f2)
[ "$PAR" = "$CAND" ] || { echo "STOP: the new anchor's parent is $PAR, not the candidate $CAND. Do not push."; exit 1; }
echo "New anchor $N has the candidate as its parent."
echo "Local refs (both must be $N):"
"$GIT" -C "$CHECKOUT" rev-parse refs/heads/0.5-dev refs/cairn/gate-anchor
[ "$("$GIT" -C "$CHECKOUT" rev-parse refs/heads/0.5-dev)" = "$N" ] && [ "$("$GIT" -C "$CHECKOUT" rev-parse refs/cairn/gate-anchor)" = "$N" ] || { echo "STOP: a local ref is not $N. Do not push."; exit 1; }

echo
echo "== push --atomic (both refs, explicit refspecs, no force)"
"$GIT" -C "$CHECKOUT" push --atomic origin refs/heads/0.5-dev:refs/heads/0.5-dev refs/cairn/gate-anchor:refs/cairn/gate-anchor || { echo "STOP: the atomic push was rejected. Do not push ref by ref, do not force. Tell Claude what printed above."; exit 1; }

echo
echo "== read both refs back from the remote (must be exactly two lines, both $N)"
out=$("$GIT" -C "$CHECKOUT" ls-remote origin refs/heads/0.5-dev refs/cairn/gate-anchor)
echo "$out"
n=$(printf '%s\n' "$out" | grep -c "^$N")
if [ "$n" -eq 2 ] && [ "$(printf '%s\n' "$out" | wc -l | tr -d ' ')" -eq 2 ]; then echo "PUBLISHED: both refs on the remote name $N."; else echo "STOP: incomplete publication (not two matching lines). Tell Claude."; exit 1; fi
