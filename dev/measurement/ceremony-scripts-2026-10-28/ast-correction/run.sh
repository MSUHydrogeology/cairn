#!/bin/bash
# The Maintainer-run AST correction: checks the script's hash, shows the dry run,
# asks for a typed "yes", then applies. It writes ONLY the two AST fixture files
# in the repository and does not commit; it prints the commit command.
#   usage: bash run.sh
set -u
HERE=$(cd "$(dirname "$0")" && pwd -P)
SCRIPT=$HERE/ast_pin.py
WANT=d7a14e8e54a817498ab432ebaf620f5e95104b655527fd6d3ba143b8506ba51e
PY=/Users/kendal30/conda_envs/lhm/bin/python3.13
REPO=/Users/kendal30/Code/cairn
got=$(shasum -a 256 "$SCRIPT" | cut -c1-64)
if [ "$got" != "$WANT" ]; then echo "STOP: the script's hash is $got, not the reviewed $WANT. Do not run it."; exit 1; fi
echo "script hash matches the reviewed one."
cd "$REPO" || exit 1
if [ -n "$(git status --short | grep -v '^??')" ]; then echo "STOP: the working tree is not clean:"; git status --short | grep -v '^??'; exit 1; fi
echo
echo "================ DRY RUN (writes nothing) ================"
"$PY" -I "$SCRIPT" || { echo "STOP: the dry run refused. Tell Claude what printed above."; exit 1; }
echo
echo "================ If the dry run reads right, type  yes  to apply ================"
echo "(it should say 4 deletions, 21 changed, known-new 23 added / 7 rekeyed / 4 dropped, same as repin status)"
printf "apply? "; read -r ans
[ "$ans" = "yes" ] || { echo "Not applied."; exit 0; }
"$PY" -I "$SCRIPT" --apply || { echo "STOP: apply failed. Run: git -C $REPO restore -- bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/tests/fixtures/scaffold_ast_known_new.json  and tell Claude."; exit 1; }
