#!/bin/bash
# Ordinary re-anchor, the run that needs the reader's record. It prints the
# launcher digest FROM THE RECORD (the commit at HEAD), then starts
# `repin ceremony`, which asks you to paste that digest. If the pasted digest and
# the launcher file's digest agree, it checks the record, then (when an AST pin is
# owed) shows the pin, asks "Write these files?" and stops after writing it.
# It loads no key. If a passphrase prompt appears, press Return at once.
#   usage: bash repin2.sh [values-file]
set -u
VALUES=${1:-/Users/kendal30/cairn-ceremony-values}
CER2=/private/tmp/claude-501/-Users-kendal30-Code-cairn/66d87e18-52ca-44fc-b226-0817c96bdc10/scratchpad/ceremony2
val() { awk -v k="$1" '$1==k { print substr($0, length(k)+2); exit }' "$VALUES"; }
CHECKOUT=$(val checkout); PYBIN=$(val python); GIT=$(val git)
cd "$CHECKOUT" || exit 1
gg() { env -i HOME=/nonexistent GIT_NO_LAZY_FETCH=1 "$GIT" --no-pager --no-replace-objects -c core.useReplaceRefs=false -c core.hooksPath=/dev/null -c core.fsmonitor=false -C "$CHECKOUT" "$@"; }
echo "HEAD (the record commit): $(gg rev-parse HEAD)"
echo
echo "The launcher digest in the record. Copy this value and paste it at the prompt:"
gg cat-file blob HEAD:dev/ceremony-record.md | awk '$1=="launcher-sha256" { print "  " $2 }'
echo
"$PYBIN" scripts/repin.py ceremony --values "$VALUES" --ceremony-dir "$CER2"
echo "repin exit: $?"
echo
echo "Now run:  git -C $CHECKOUT status --short   and tell Claude what repin printed."
