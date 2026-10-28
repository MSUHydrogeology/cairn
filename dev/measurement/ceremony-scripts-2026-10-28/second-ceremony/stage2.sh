#!/bin/bash
# Stage 2: the SIGNING stage. This asks for your key's passphrase ONCE. Do not
# ssh-add the key. Run it only after compare.sh printed ALL COMPARISONS PASSED
# and you have given your authorization. It then checks the new anchor (V).
# It does NOT push: publishing both refs is yours, from the page's Phase 5.
#   usage: bash stage2.sh <digest-from-compare.sh> [values-file]
set -u
[ $# -ge 1 ] || { echo "usage: bash stage2.sh <package digest printed by compare.sh>"; exit 1; }
DIGEST=$1
case "$DIGEST" in *[!0-9a-f]*|"") echo "STOP: the digest must be 64 hex characters"; exit 1;; esac
[ "${#DIGEST}" -eq 64 ] || { echo "STOP: the digest must be 64 hex characters"; exit 1; }
CER=$(cd "$(dirname "$0")" && pwd -P)
. "$CER/ceremony.env"
PACKET=$CER/authorization-packet.txt; LAUNCHER=$CER/reanchor-launcher.sh
VALUES=${2:-/Users/kendal30/cairn-ceremony-values}
val() { awk -v k="$1" '$1==k { print substr($0, length(k)+2); exit }' "$VALUES"; }
GIT=$(val git); HOMEDIR=$(val home); CHECKOUT=$(val checkout)
g() { env -i HOME=/nonexistent GIT_NO_LAZY_FETCH=1 "$GIT" --no-pager --no-replace-objects -c core.useReplaceRefs=false -c core.hooksPath=/dev/null -c core.fsmonitor=false -C "$CHECKOUT" "$@"; }

echo "== stage 2: enter the passphrase when asked (once)"
env -i HOME="$HOMEDIR" PATH=/usr/bin:/bin TERM="$TERM" LANG=C /bin/sh "$LAUNCHER" "$PACKET" "$VALUES" "$CAND" --stage2 "$DIGEST" || { echo "STOP: stage 2 refused or failed. Do not push. Tell Claude what printed above."; exit 1; }

echo
echo "== V: the new anchor must carry a good signature by your key"
g -c gpg.format=ssh -c gpg.ssh.program=/usr/bin/ssh-keygen -c gpg.program=/usr/bin/false -c gpg.openpgp.program=/usr/bin/false -c gpg.x509.program=/usr/bin/false -c gpg.ssh.allowedSignersFile="$CHECKOUT/dev/.cairn/allowed_signers" verify-commit refs/cairn/gate-anchor
rc=$?
echo "verify-commit exit: $rc"
echo "Good = exit 0 and 'Good \"git\" signature for ... with' your key's fingerprint SHA256:8R549gtP0SJPaCWlQlausCtAbRBquXCIhbM6395ESsM."
echo "Anything else (an error, 'No principal matched', another fingerprint, no output): do NOT push."
