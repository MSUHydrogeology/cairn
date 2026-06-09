#!/usr/bin/env bash
#
# Cairn contained-kernel recipe — the Move-3 FLOOR GATE (proposal F3 / Codex R8).
#
# Runs in CAIRN's CI (not adopter CI). Two legs, because a compile-only check is
# too weak (R8) — it proves syntax, not that invoked stdlib APIs / filesystem /
# subprocess behaviour actually work at the floor:
#
#   1. `vermin` over the engine — the detected minimum Python must NOT exceed the
#      declared floor (3.11, doctrine/runtime-contract.md). vermin runs in the
#      floor/compat image's separate dev stage, so the shipped `engine` image
#      stays pip-clean. vermin UNRESOLVABLE => explicit FAILURE, never a silent
#      skip-as-pass (Antigravity R2): this is the release gate, not the unit suite.
#   2. a runtime CONFORMANCE SLICE at the floor (Python 3.11): CLI --help, a clean
#      install, and a controlled upgrade — so a runtime-only incompatibility fails
#      too, not just raised syntax.
#
# Plus a raised-syntax PROBE: 3.12-only syntax must be detected as above-floor.
#
# Usage:  bootstrap/container/floor-gate.sh
# Env:    CAIRN_OCI=podman|docker (default auto), CAIRN_FLOOR_WORK=<scratch>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/../.." && pwd)"
WORK="${CAIRN_FLOOR_WORK:-$HOME/.cache/cairn_floor_gate}"
DOCKERFILE="$SCRIPT_DIR/Dockerfile"
DECLARED_FLOOR="3.11"

note() { printf '\033[1m[floor]\033[0m %s\n' "$*"; }
ok()   { printf '  \033[32mok\033[0m %s\n' "$*"; }
fail() { printf '  \033[31mFAIL\033[0m %s\n' "$*" >&2; exit 1; }

OCI="${CAIRN_OCI:-}"
if [ -z "$OCI" ]; then
  if command -v podman >/dev/null 2>&1; then OCI=podman
  elif command -v docker >/dev/null 2>&1; then OCI=docker
  else fail "no OCI runtime (podman/docker) — the floor gate needs one (release gate, not skippable)."
  fi
fi
note "OCI runtime: $OCI"

COMMIT="$(git -C "$REPO" rev-parse HEAD)"
rm -rf "$WORK"; mkdir -p "$WORK"
SRC="$WORK/src"; mkdir -p "$SRC/bootstrap"
cp "$REPO/bootstrap/scaffold.py" "$SRC/bootstrap/scaffold.py"
cp -R "$REPO/bootstrap/_scaffold" "$SRC/bootstrap/_scaffold"
cp -R "$REPO/templates" "$SRC/templates"
cp "$REPO/CITATION.cff" "$SRC/CITATION.cff"

note "building floor/compat image (Python ${DECLARED_FLOOR}, +vermin dev stage)"
$OCI build -f "$DOCKERFILE" --target floor \
  --build-arg CAIRN_COMMIT="$COMMIT" -t cairn-floor:gate "$SRC" >/dev/null 2>&1 \
  || fail "floor image build failed"

floor_run() { # run a command in the floor image (override entrypoint)
  $OCI run --rm --network=none --entrypoint /bin/sh cairn-floor:gate -c "$1"
}

# --- leg 1: vermin over the engine; unresolvable => FAILURE (not skip) --------
note "leg 1: vermin floor detection over the engine"
floor_run 'command -v vermin >/dev/null 2>&1' \
  || fail "vermin unresolvable in the gate image — release gate FAILS (never skip-as-pass)."
VERMIN_OUT="$(floor_run 'vermin --backport dataclasses --backport typing /cairn/bootstrap/_scaffold 2>&1' || true)"
DETECTED="$(printf '%s' "$VERMIN_OUT" | grep -oE 'Minimum required versions:[[:space:]]*[0-9]+\.[0-9]+' | grep -oE '[0-9]+\.[0-9]+' | tail -1)"
[ -n "$DETECTED" ] || fail "vermin produced no 'Minimum required versions' line (output: $VERMIN_OUT)"
# detected floor must be <= declared floor (3.11)
if [ "$(printf '%s\n%s\n' "$DETECTED" "$DECLARED_FLOOR" | sort -V | tail -1)" != "$DECLARED_FLOOR" ]; then
  fail "engine detected floor $DETECTED EXCEEDS declared floor $DECLARED_FLOOR"
fi
ok "vermin: engine minimum $DETECTED <= declared floor $DECLARED_FLOOR"

# --- raised-syntax probe: 3.12-only syntax must read as above-floor -----------
note "raised-syntax probe: PEP 695 (3.12) syntax must be flagged above-floor"
# PEP 695 type-alias statement parses only on >=3.12.
floor_run 'printf "type IntAlias = int\n" > /tmp/probe.py; python -c "import ast,sys; ast.parse(open(\"/tmp/probe.py\").read())" 2>/dev/null' \
  && fail "the 3.11 floor image PARSED 3.12-only syntax (floor image is not at the floor)" \
  || ok "3.11 floor image rejects 3.12-only syntax (raised-syntax probe fails closed)"

# --- leg 2: runtime conformance slice at the floor ----------------------------
note "leg 2: runtime conformance slice at Python ${DECLARED_FLOOR}"
# (a) CLI help
floor_run 'python /cairn/bootstrap/scaffold.py --help >/dev/null 2>&1' \
  || fail "CLI --help failed at the floor"
ok "CLI --help runs at the floor"

# (b) clean install + (c) controlled upgrade, contained
T="$WORK/target"; mkdir -p "$T"
( cd "$T" && git init -q && git config user.email a@b.c && git config user.name t )
printf '# floor probe\n' > "$T/README.md"
cat > "$T/.cairn-profile.yml" <<'EOF'
project_name: "FloorProbe"
test_command: "true"
preset: solo-greenfield
EOF
run_floor_engine() { # contained run, target mounted writable
  $OCI run --rm --network=none --read-only --tmpfs /tmp:rw,size=64m \
    --cap-drop=ALL --security-opt no-new-privileges \
    -e PYTHONDONTWRITEBYTECODE=1 -e HOME=/tmp \
    -v "$T":/work:rw,Z cairn-floor:gate "$@"
}
run_floor_engine --config /work/.cairn-profile.yml --target /work --cairn-root /cairn \
  --non-interactive --allow-dev >/dev/null 2>&1 || fail "clean install failed at the floor"
test -f "$T/dev/.cairn/cairn-lock.yml" || fail "floor install wrote no lockfile"
ok "clean install runs at the floor (lockfile written)"
run_floor_engine upgrade --target /work --cairn-root /cairn --plan  >/dev/null 2>&1 \
  || fail "upgrade --plan failed at the floor"
run_floor_engine upgrade --target /work --cairn-root /cairn --stage >/dev/null 2>&1 \
  || fail "upgrade --stage failed at the floor"
run_floor_engine upgrade --target /work --cairn-root /cairn --apply >/dev/null 2>&1 \
  || fail "upgrade --apply failed at the floor"
ok "controlled upgrade runs at the floor (plan -> stage -> apply)"

note "FLOOR GATE PASSED — vermin <= ${DECLARED_FLOOR}; raised syntax rejected; runtime slice green at the floor."
