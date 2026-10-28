#!/bin/bash
# Step 3 of the runbook page, before signing: the comparisons E1, E2, E3, E4, E6,
# then H and K again, and a look for anything stage 1 left running. It loads no
# key and signs nothing. Running --hash-package runs the candidate's checker once
# more, as you, with no key (the page's E3 does the same).
#   usage: bash compare.sh [values-file]
set -u
CAND=55d31f1e59a95c5185b08cb5242b7c23bd73debc
CER=$(cd "$(dirname "$0")" && pwd -P)
PACKET=$CER/packet; LAUNCHER=$CER/launcher.sh; REPORT=$CER/report.txt
VALUES=${1:-/Users/kendal30/cairn-ceremony-values}
# the two digests you wrote down at step 1 (H)
H_VALUES=af85b488e77a7521fc5113d035b8b63a1effaa88c76c9c5458e7c351b60a742b
H_PYTHON=a0e58d65114a537560a551b09d5a3c2d06f6c3a199d9ed819138080cd58ddf3e
val() { awk -v k="$1" '$1==k { print substr($0, length(k)+2); exit }' "$VALUES"; }
GIT=$(val git); HOMEDIR=$(val home); CHECKOUT=$(val checkout); PYBIN=$(val python); SIGKEY=$(val signing_key)
g() { env -i HOME=/nonexistent GIT_NO_LAZY_FETCH=1 "$GIT" --no-pager --no-replace-objects -c core.useReplaceRefs=false -c core.hooksPath=/dev/null -c core.fsmonitor=false -C "$CHECKOUT" "$@"; }
L() { env -i HOME="$HOMEDIR" PATH=/usr/bin:/bin TERM="$TERM" LANG=C /bin/sh "$LAUNCHER" "$PACKET" "$VALUES" "$@"; }
fails=0
ok()  { echo "PASS  $1"; }
bad() { echo "FAIL  $1"; fails=$((fails+1)); }
chk() { if [ "$2" = "$3" ]; then ok "$1"; else bad "$1"; echo "      got:      $2"; echo "      expected: $3"; fi; }
rep() { awk -v k="$1" '{ line=$0; sub(/^ +/, "", line); if (index(line, k)==1) { sub(k, "", line); sub(/^ +/, "", line); print line; exit } }' "$REPORT"; }

[ -f "$REPORT" ] || { echo "STOP: no report.txt next to this script; run stage1.sh first"; exit 1; }
REC=$(g cat-file blob "$CAND:dev/ceremony-record.md")
chk "E1 launcher file equals launcher-sha256 in the record" "$(shasum -a 256 "$LAUNCHER" | cut -c1-64)" "$(printf '%s\n' "$REC" | awk '$1=="launcher-sha256"{print $2}')"
chk "R3 packet file equals packet-sha256 in the record"     "$(shasum -a 256 "$PACKET" | cut -c1-64)"   "$(printf '%s\n' "$REC" | awk '$1=="packet-sha256"{print $2}')"
chk "E2 HEAD equals the report's candidate id" "$(g rev-parse HEAD)" "$(rep 'candidate id')"
echo "E3  running: L \$CAND --hash-package"
E3=$(L "$CAND" --hash-package | tail -1 | awk '{print $1}')
chk "E3 the package digest equals the report's package sha256" "$E3" "$(rep 'package sha256')"
ROSTER_FP=$(g cat-file blob "$CAND:dev/.cairn/allowed_signers" | grep -v '^#' | grep . | head -1 | { read -r _ rest; printf '%s\n' "$rest" | awk '{print $1, $2}' | ssh-keygen -lf - | awk '{print $2}'; })
if [ -r "$SIGKEY" ]; then chk "E4 your public key's fingerprint is on the report's roster" "$(ssh-keygen -lf "$SIGKEY" | awk '{print $2}')" "$(rep 'kendal30@msu.edu ssh-ed25519' | head -1)"; else bad "E4 cannot read $SIGKEY"; fi
echo "E6  each tool in your values file against what your shell resolves (python may differ; see the note)"
for pair in env:env git:git python:python3.13 mktemp:mktemp mkdir:mkdir shasum:shasum sort:sort cat:cat; do
  key=${pair%%:*}; name=${pair##*:}; want=$(val "$key"); found=$(command -v "$name" 2>/dev/null); got=""; [ -n "$found" ] && got=$(readlink -f "$found")
  if [ "$got" = "$want" ]; then ok "E6 $key $want"
  elif [ "$key" = "python" ]; then echo "NOTE  E6 python: values file says $want; your shell's $name resolves to ${got:-nothing}. Confirm the values file names the Python you mean."
  else bad "E6 $key: values file says $want; your shell resolves $name to ${got:-nothing}"; fi
done
chk "H values file unchanged since step 1" "$(shasum -a 256 "$VALUES" | cut -c1-64)" "$H_VALUES"
chk "H python unchanged since step 1"      "$(shasum -a 256 "$PYBIN"  | cut -c1-64)" "$H_PYTHON"
a1=$(ssh-add -l 2>&1); a2=$(SSH_AUTH_SOCK=$(launchctl getenv SSH_AUTH_SOCK 2>/dev/null) ssh-add -l 2>&1)
case "$a1 $a2" in *"$ROSTER_FP"*) bad "K the ceremony key is loaded in an agent (remove it with ssh-add -d)";; *) ok "K the ceremony key is not in either agent";; esac
echo "ps  anything stage 1 left running (a look, not proof):"
ps -axo pid,command | grep -E 'reanchor|launcher\.sh|stage1|pytest|gather_evidence' | grep -v -E 'grep|compare\.sh' || echo "   nothing matching"
echo
if [ "$fails" -eq 0 ]; then echo "ALL COMPARISONS PASSED. The digest to give stage 2 is:"; echo "$E3"; echo "Next: authorize in your own words (in chat), then run stage2.sh with that digest."; else echo "STOP: $fails comparison(s) failed. Do not sign. Tell Claude what printed above."; exit 1; fi
