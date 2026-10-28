#!/bin/bash
# Step 2 of the runbook page: stage 1, with no key. This RUNS CANDIDATE CODE on
# your machine (the checker's evidence run). It never loads your key. If a
# passphrase prompt ever appears, DECLINE it by pressing Return AT ONCE, within 10 seconds, typing nothing (not Ctrl-C): the prompt is the
# ceremony asking whether your key is reachable, and answering it makes the
# check fail.
#   usage: bash stage1.sh [values-file]
# The report is also saved to report.txt next to this script, so you can paste
# it to Claude.
set -u
CER=$(cd "$(dirname "$0")" && pwd -P)
. "$CER/ceremony.env"
PACKET=$CER/authorization-packet.txt
LAUNCHER=$CER/reanchor-launcher.sh
VALUES=${1:-/Users/kendal30/cairn-ceremony-values}
HOMEDIR=$(awk '$1=="home" { print substr($0, 6); exit }' "$VALUES")
L() { env -i HOME="$HOMEDIR" PATH=/usr/bin:/bin TERM="$TERM" LANG=C /bin/sh "$LAUNCHER" "$PACKET" "$VALUES" "$@"; }

echo "== 1/3  L \$CAND --validate   (checks your values file; no candidate code)"
L "$CAND" --validate || { echo "STOP: --validate refused. Fix the value it names (a stale path is the usual cause), then run again."; exit 1; }

echo
echo "== 2/3  L \$CAND   (stage 1: runs the candidate's checker; can take several minutes)"
L "$CAND" || { echo "STOP: stage 1 refused or failed. Do not go on. Paste what printed above to Claude."; exit 1; }

echo
echo "== 3/3  L \$CAND --show-report   (the report you answer Y1 to Y5 on)"
L "$CAND" --show-report | tee "$CER/report.txt"
echo
echo "Read the report. Answer Y1 to Y5. Any 'no' stops here."
