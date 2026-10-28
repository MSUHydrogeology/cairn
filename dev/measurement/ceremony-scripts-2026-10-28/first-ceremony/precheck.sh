#!/bin/bash
# Steps 0 and 1 of the runbook page as one script: the checks before stage 1.
# It runs no candidate code, loads no key, and writes nothing. Each check prints
# the raw result and PASS or FAIL. Any FAIL means stop.
#   usage: bash precheck.sh [values-file]
set -u
CAND=55d31f1e59a95c5185b08cb5242b7c23bd73debc
REV=38965e4a378e1cd89e8a35e2e47614ca362f53c3
CER=$(cd "$(dirname "$0")" && pwd -P)
PACKET=$CER/packet
LAUNCHER=$CER/launcher.sh
VALUES=${1:-/Users/kendal30/cairn-ceremony-values}

val() { awk -v k="$1" '$1==k { print substr($0, length(k)+2); exit }' "$VALUES"; }
GIT=$(val git); HOMEDIR=$(val home); CHECKOUT=$(val checkout); PYBIN=$(val python); SIGKEY=$(val signing_key); PKG=$(val package)
g() { env -i HOME=/nonexistent GIT_NO_LAZY_FETCH=1 "$GIT" --no-pager --no-replace-objects -c core.useReplaceRefs=false -c core.hooksPath=/dev/null -c core.fsmonitor=false -C "$CHECKOUT" "$@"; }

fails=0
ok()   { echo "PASS  $1"; }
bad()  { echo "FAIL  $1"; fails=$((fails+1)); }
chk()  { if [ "$2" = "$3" ]; then ok "$1"; else bad "$1"; echo "      got:      $2"; echo "      expected: $3"; fi; }

echo "values file: $VALUES"
echo "checkout=$CHECKOUT  git=$GIT  python=$PYBIN  home=$HOMEDIR"
echo "package leaf: $PKG"
for need in "$VALUES" "$PACKET" "$LAUNCHER" "$GIT" "$PYBIN"; do
  [ -f "$need" ] || { bad "missing file: $need"; }
done
[ -n "$GIT" ] && [ -n "$CHECKOUT" ] && [ -n "$HOMEDIR" ] && [ -n "$PYBIN" ] || { echo "STOP: the values file lacks git, checkout, home or python"; exit 1; }
[ -e "$PKG" ] && bad "the package leaf already exists (stage 1 refuses): $PKG" || ok "the package leaf does not exist"

chk "tree is clean (git status prints nothing)" "$(g status --short | grep -v '^??')" ""
chk "HEAD is the candidate" "$(g rev-parse HEAD)" "$CAND"

rec=$(g cat-file blob "$CAND:dev/ceremony-record.md")
chk "R0 read-commit"      "$(printf '%s\n' "$rec" | awk '$1=="read-commit"{print $2}')" "$REV"
chk "R0/E1 packet-sha256 equals the packet file"   "$(printf '%s\n' "$rec" | awk '$1=="packet-sha256"{print $2}')"   "$(shasum -a 256 "$PACKET" | cut -c1-64)"
chk "R0/E1 launcher-sha256 equals the launcher file" "$(printf '%s\n' "$rec" | awk '$1=="launcher-sha256"{print $2}')" "$(shasum -a 256 "$LAUNCHER" | cut -c1-64)"
chk "R1 candidate and its parent" "$(g rev-list --parents -n1 "$CAND")" "$CAND $REV"
chk "R2 the record is the only change" "$(g diff-tree --no-renames --name-only -r "$REV" "$CAND")" "dev/ceremony-record.md"
chk "R4 record members equal packet members" "$(printf '%s\n' "$rec" | grep '^member ' | sort)" "$(grep '^member ' "$PACKET" | sort)"
if g diff-tree --quiet --no-renames "$REV" "$CAND" -- bootstrap/reanchor-launcher.template.sh; then ok "E5a the template is unchanged since the commit the reader read"; else bad "E5a the template changed"; fi
if g cat-file blob "$CAND:bootstrap/reanchor-launcher.template.sh" | sed "s/@PACKET_SHA256@/$(shasum -a 256 "$PACKET" | cut -c1-64)/" | cmp -s - "$LAUNCHER"; then ok "E5b the launcher is the template with the one slot filled"; else bad "E5b the launcher differs from the template with the slot filled"; fi

ROSTER_FP=$(g cat-file blob "$CAND:dev/.cairn/allowed_signers" | grep -v '^#' | grep . | head -1 | { read -r _ rest; printf '%s\n' "$rest" | awk '{print $1, $2}' | ssh-keygen -lf - | awk '{print $2}'; })
echo "roster key fingerprint (the key stage 2 must sign with): $ROSTER_FP"
if [ -r "$SIGKEY" ]; then chk "E4 your public key is the roster key" "$(ssh-keygen -lf "$SIGKEY" | awk '{print $2}')" "$ROSTER_FP"; else echo "NOTE  could not read $SIGKEY: check E4 by hand (ssh-keygen -lf <that file> must print $ROSTER_FP)"; fi

echo "H  (write both digests down: step 3 must print the same two)"
shasum -a 256 "$VALUES" "$PYBIN"

echo "K  the agents' keys (yours, the ceremony key, must not be listed):"
a1=$(ssh-add -l 2>&1); a2=$(SSH_AUTH_SOCK=$(launchctl getenv SSH_AUTH_SOCK 2>/dev/null) ssh-add -l 2>&1)
printf '%s\n%s\n' "$a1" "$a2"
case "$a1 $a2" in *"$ROSTER_FP"*) bad "K the ceremony key is loaded in an agent: remove it (ssh-add -d) and run again";; *) ok "K the ceremony key is not in either agent";; esac

echo
if [ "$fails" -eq 0 ]; then echo "ALL CHECKS PASSED. E7 is skipped at the first ceremony. Next: stage 1."; else echo "STOP: $fails check(s) failed. Do not go on. Tell Claude what printed above."; exit 1; fi
