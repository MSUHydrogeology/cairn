#!/bin/bash
# Ordinary re-anchor, first pass. It builds the packet and launcher with repin,
# then runs `repin ceremony`, which checks everything, WRITES the owed AST pin
# into the working tree, prints a stop line and stops. It loads no key and signs
# nothing. After it stops, tell Claude: the pin is committed and read next.
# If a passphrase prompt appears, press Return at once (decline it).
#   usage: bash repin1.sh [values-file]
set -u
VALUES=${1:-/Users/kendal30/cairn-ceremony-values}
CER2=/private/tmp/claude-501/-Users-kendal30-Code-cairn/66d87e18-52ca-44fc-b226-0817c96bdc10/scratchpad/ceremony2
val() { awk -v k="$1" '$1==k { print substr($0, length(k)+2); exit }' "$VALUES"; }
CHECKOUT=$(val checkout); PYBIN=$(val python)
[ -x "$PYBIN" ] || { echo "STOP: the values file's python is not executable: $PYBIN"; exit 1; }
cd "$CHECKOUT" || exit 1
mkdir -p "$CER2" || exit 1
echo "== repin packet (writes the packet and launcher into $CER2)"
"$PYBIN" scripts/repin.py packet --ceremony-dir "$CER2" || { echo "STOP: repin packet failed. Tell Claude what printed above."; exit 1; }
echo
echo "== repin ceremony, first pass (it stops after writing the AST pin)"
"$PYBIN" scripts/repin.py ceremony --values "$VALUES" --ceremony-dir "$CER2"
echo "repin exit: $?"
echo
echo "Now run:  git -C $CHECKOUT status --short   and tell Claude what repin printed above."
