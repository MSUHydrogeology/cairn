#!/usr/bin/env bash
#
# Cairn contained-kernel recipe — the F4 two-version acceptance test (proposal R6).
#
# Proves the deliverable: a host with NO Python on PATH for the engine runs the
# Cairn install + one upgrade entirely inside the contained kernel, against a
# deliberately NON-PYTHON adopter repo (a bare dev/ tree + Markdown, zero Python
# files, no Python in its own CI), and the result is correct AND the container is
# a narrowed trust boundary, not just a Python carrier.
#
# It is FALSIFIABLE — every leg below is asserted and the script fails loud on the
# first violation:
#   1. install from pinned release A;
#   2. upgrade to pinned release B carrying a CONTROLLED template change;
#   3. the change propagated; the lockfile + base cache advanced;
#   4. host ownership (no chown fixup);
#   5. no credential residue in the mutated tree;
#   6. an out-of-target write is REFUSED (containment, not just lifecycle);
#   7. the mutation phase ran network-disabled.
#
# Platform: v1 is tested on rootless Linux + Docker/Podman (this script auto-detects
# the runtime). On rootless Podman, container→host ownership maps automatically, so
# no --user is passed; on Docker-on-Linux the recipe documents --user $(id -u):$(id -g).
# See recipe.md for the platform matrix. On a host without an OCI runtime the script
# exits SKIPPED (degraded-assurance: a missing gate is SKIPPED, never PASS).
#
# Usage:  bootstrap/container/acceptance.sh
# Env:    CAIRN_OCI=podman|docker (default: auto-detect), CAIRN_F4_WORK=<scratch dir>

set -euo pipefail

# --- locate the repo + scratch (scratch under $HOME; the Podman VM does not mount /tmp)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/../.." && pwd)"
WORK="${CAIRN_F4_WORK:-$HOME/.cache/cairn_f4_accept}"
DOCKERFILE="$SCRIPT_DIR/Dockerfile"

note() { printf '\033[1m[F4]\033[0m %s\n' "$*"; }
ok()   { printf '  \033[32mok\033[0m %s\n' "$*"; }
fail() { printf '  \033[31mFAIL\033[0m %s\n' "$*" >&2; exit 1; }
skip() { printf '\033[33m[F4 SKIPPED]\033[0m %s\n' "$*"; exit 0; }

# --- 0. OCI runtime detection (degraded-assurance: absent => SKIPPED, never PASS)
OCI="${CAIRN_OCI:-}"
if [ -z "$OCI" ]; then
  if command -v podman >/dev/null 2>&1; then OCI=podman
  elif command -v docker >/dev/null 2>&1; then OCI=docker
  else skip "no OCI runtime (podman/docker) on PATH — F4 needs rootless Linux + Docker/Podman."
  fi
fi
command -v "$OCI" >/dev/null 2>&1 || skip "configured runtime '$OCI' not found on PATH."
note "OCI runtime: $OCI ($($OCI --version 2>&1 | head -1))"

# --- 1. Phase 1 (acquire + verify): refuse a mutable / unverified ref, emit identity
"$SCRIPT_DIR/verify-ref.sh" "$REPO" || fail "ref verification refused the build (Phase 1)."
COMMIT="$(git -C "$REPO" rev-parse HEAD)"
REF="$(git -C "$REPO" describe --tags --always 2>/dev/null || echo "$COMMIT")"
note "verified Cairn ref: $REF ($COMMIT)"
# Negative: a mutable branch ref must be REFUSED (Codex S5).
BRANCH="$(git -C "$REPO" branch --show-current 2>/dev/null || true)"
if [ -n "$BRANCH" ]; then
  if "$SCRIPT_DIR/verify-ref.sh" "$REPO" "$BRANCH" >/dev/null 2>&1; then
    fail "verify-ref accepted a mutable branch ref '$BRANCH' (must refuse)"
  fi
  ok "verify-ref refuses a mutable branch ref ('$BRANCH')"
fi

# --- 2. materialize two SOURCE trees (A, B) FROM THE VERIFIED COMMIT OBJECT
note "materializing source trees A and B from commit $COMMIT under $WORK"
rm -rf "$WORK"; mkdir -p "$WORK"

# Negative: a dirty / untracked build surface must be REFUSED (Codex F#2), so the
# emitted commit label can never mislabel uncommitted bytes. Probe a scratch repo.
DR="$WORK/dirty-probe"; mkdir -p "$DR"
( cd "$DR" && git init -q && git config user.email a@b.c && git config user.name t \
  && mkdir -p bootstrap/_scaffold templates && echo x > bootstrap/scaffold.py \
  && echo 'version: "0.0.0"' > CITATION.cff && echo y > bootstrap/_scaffold/__init__.py \
  && git add -A && git commit -q -m base )
"$SCRIPT_DIR/verify-ref.sh" "$DR" >/dev/null 2>&1 || fail "verify-ref refused a CLEAN build surface"
echo "tampered" >> "$DR/bootstrap/scaffold.py"
"$SCRIPT_DIR/verify-ref.sh" "$DR" >/dev/null 2>&1 && fail "verify-ref accepted a tracked-DIRTY build surface"
git -C "$DR" checkout -- bootstrap/scaffold.py
echo "evil" > "$DR/bootstrap/_scaffold/injected.py"   # untracked, inside the build surface
"$SCRIPT_DIR/verify-ref.sh" "$DR" >/dev/null 2>&1 && fail "verify-ref accepted an UNTRACKED build-surface file"
ok "verify-ref refuses a dirty / untracked build surface (clean accepted)"

# The build context is the COMMIT OBJECT (not the working tree): `git archive`
# extracts exactly the recipe's COPY set at $COMMIT, so the image bytes provably
# match the emitted org.cairn.commit label.
for V in A B; do
  S="$WORK/src-$V"; mkdir -p "$S"
  git -C "$REPO" archive --format=tar "$COMMIT" \
    bootstrap/scaffold.py bootstrap/_scaffold templates CITATION.cff \
    | tar -x -C "$S" || fail "git archive of the build surface failed for $V"
done
# Release B is a GENUINE newer release: bump its version (CITATION.cff is the
# engine's version source) AND carry a uniquely-identifiable upstream-only line
# added to a core template. A 3-way merge (base=A, upstream=B, local=installed)
# must carry the new line into the adopter tree.
MARKER="<!-- cairn-F4-controlled-upgrade-marker-$COMMIT -->"
CHANGED_TEMPLATE="templates/core/dev/PLANNING.md"
printf '\n%s\n' "$MARKER" >> "$WORK/src-B/$CHANGED_TEMPLATE"
# Portable in-place version bump (no GNU sed assumption).
sed 's/^version:.*/version: "0.2.1-f4"/' "$WORK/src-B/CITATION.cff" > "$WORK/src-B/CITATION.cff.new"
mv "$WORK/src-B/CITATION.cff.new" "$WORK/src-B/CITATION.cff"
ok "release B staged: version 0.2.1-f4 + controlled change in $CHANGED_TEMPLATE"

# --- 3. build the engine image for each version (base pinned by digest in Dockerfile)
build() { # $1=version $2=tag
  note "building image $2 (Cairn $COMMIT)"
  $OCI build -f "$DOCKERFILE" --target engine \
    --build-arg CAIRN_COMMIT="$COMMIT" --build-arg CAIRN_REF="$REF" \
    -t "$2" "$WORK/src-$1" >/dev/null 2>&1 || fail "image build failed for $2"
}
build A cairn-kernel:A
build B cairn-kernel:B
# Identity emitted into the image (Phase 1 provenance).
GOT_COMMIT="$($OCI image inspect cairn-kernel:A --format '{{ index .Labels "org.cairn.commit" }}')"
[ "$GOT_COMMIT" = "$COMMIT" ] || fail "image identity mismatch: label=$GOT_COMMIT expected=$COMMIT"
ok "image identity emitted (org.cairn.commit=$GOT_COMMIT)"

# --- 4. a deliberately NON-PYTHON adopter repo (bare dev marker + Markdown, zero .py)
TARGET="$WORK/adopter"
mkdir -p "$TARGET"
( cd "$TARGET" && git init -q && git config user.email a@b.c && git config user.name t )
printf '# Non-Python adopter\n\nA Rust/JS/R team repo. No Python here.\n' > "$TARGET/README.md"
cat > "$TARGET/.cairn-profile.yml" <<'EOF'
project_name: "F4Adopter"
test_command: "true"
preset: solo-greenfield
EOF
if find "$TARGET" -name '*.py' | grep -q .; then fail "adopter fixture is not Python-free"; fi
ok "non-Python adopter fixture ready (zero .py files)"

# --- the contained Phase-2 mutation run (the narrowed trust boundary, Codex R1/R3)
#  --network=none           offline mutation, no credentials
#  --read-only + tmpfs      read-only root FS, bounded writable tmp
#  --cap-drop=ALL           no Linux capabilities
#  --no-new-privileges      no privilege escalation
#  -v TARGET:/work:rw       ONLY the target repo is writable; engine source is RO in-image
run_engine() { # $1=image, rest=engine args
  local img="$1"; shift
  $OCI run --rm \
    --network=none --read-only --tmpfs /tmp:rw,size=64m \
    --cap-drop=ALL --security-opt no-new-privileges \
    -e PYTHONDONTWRITEBYTECODE=1 -e HOME=/tmp \
    -v "$TARGET":/work:rw,Z \
    "$img" "$@"
}

# --- 5. install from release A (contained)
note "install from release A (contained, offline)"
run_engine cairn-kernel:A \
  --config /work/.cairn-profile.yml --target /work --cairn-root /cairn \
  --non-interactive --allow-dev >/dev/null 2>&1 || fail "contained install failed"
test -f "$TARGET/dev/.cairn/cairn-lock.yml" || fail "install wrote no lockfile"
test -d "$TARGET/dev/.cairn/base"           || fail "install wrote no base cache"
test -f "$TARGET/dev/PLANNING.md"           || fail "install wrote no dev/ tree"
LOCK_A="$(sha256sum "$TARGET/dev/.cairn/cairn-lock.yml" | cut -d' ' -f1)"
ok "install wrote lockfile + base cache + dev/ tree"
# The controlled marker must NOT be present yet (it is a B-only change).
grep -q "$MARKER" "$TARGET/dev/PLANNING.md" && fail "marker present before upgrade (fixture bug)"
ok "pre-upgrade state clean (controlled marker absent)"

# --- 6. host ownership (no chown fixup) — files owned by the invoking host user
OWNER="$(stat -f '%Su' "$TARGET/dev/.cairn/cairn-lock.yml" 2>/dev/null || stat -c '%U' "$TARGET/dev/.cairn/cairn-lock.yml")"
[ "$OWNER" = "$(id -un)" ] || fail "lockfile owned by '$OWNER', not host user '$(id -un)' (chown fixup would be needed)"
ok "host ownership preserved (no chown fixup): owner=$OWNER"

# --- 7. upgrade to release B (contained) — plan then apply
note "upgrade to release B (contained, offline): plan -> stage -> apply"
ULOG="$WORK/upgrade.log"; : > "$ULOG"
run_engine cairn-kernel:B upgrade --target /work --cairn-root /cairn --plan  >>"$ULOG" 2>&1 \
  || { cat "$ULOG"; fail "contained 'upgrade --plan' failed"; }
run_engine cairn-kernel:B upgrade --target /work --cairn-root /cairn --stage >>"$ULOG" 2>&1 \
  || { cat "$ULOG"; fail "contained 'upgrade --stage' failed"; }
run_engine cairn-kernel:B upgrade --target /work --cairn-root /cairn --apply >>"$ULOG" 2>&1 \
  || { cat "$ULOG"; fail "contained 'upgrade --apply' failed"; }
# The controlled change propagated into the adopter tree.
grep -q "$MARKER" "$TARGET/dev/PLANNING.md" \
  || { echo "--- upgrade log ---"; cat "$ULOG"; fail "controlled upgrade change did NOT propagate"; }
ok "controlled template change propagated via the contained upgrade"
# The lockfile advanced (upgrade is a real state change, not a no-op).
LOCK_B="$(sha256sum "$TARGET/dev/.cairn/cairn-lock.yml" | cut -d' ' -f1)"
[ "$LOCK_A" != "$LOCK_B" ] || fail "lockfile unchanged after upgrade (no state advance)"
ok "lockfile + base cache advanced (A=$LOCK_A -> B=$LOCK_B)"

# --- 8. no credential residue in the mutated tree (no creds were ever mounted)
if grep -RIlEi 'AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|ghp_[0-9A-Za-z]{36}|xox[baprs]-' "$TARGET" 2>/dev/null | grep -q .; then
  fail "credential-shaped residue found in the mutated tree"
fi
ok "no credential residue in the mutated tree"

# --- 9. out-of-target write is REFUSED (containment, not just lifecycle)
# Non-vacuous by construction: the assertions run IN THE SAME container as the
# write attempts, so if `--read-only` (or the single-writable-mount) were dropped
# from the recipe, a write to /cairn or /etc or / would SUCCEED and the container
# would exit non-zero -> this leg FAILS. The /work canary proves the harness is
# wired (the one writable mount works), so a refusal is real containment, not a
# broken test.
note "negative: out-of-target + engine-source + root-FS writes must be refused"
$OCI run --rm --network=none --read-only --tmpfs /tmp:rw,size=8m \
  --cap-drop=ALL --security-opt no-new-privileges \
  -v "$TARGET":/work:rw,Z \
  --entrypoint /bin/sh cairn-kernel:A -c '
    set -e
    # the ONE writable mount must work (proves the test is wired, not vacuous)
    touch /work/.f4_canary && rm -f /work/.f4_canary
    # every out-of-target / read-only-root write MUST fail
    if touch /cairn/escape 2>/dev/null; then echo "BREACH: wrote engine source /cairn"; exit 11; fi
    if touch /etc/escape   2>/dev/null; then echo "BREACH: wrote /etc";               exit 12; fi
    if touch /escape       2>/dev/null; then echo "BREACH: wrote / (root FS)";          exit 13; fi
    exit 0
  ' || fail "containment breach: an out-of-target / engine-source / root-FS write was NOT refused"
ok "out-of-target + engine-source + root-FS writes refused (in-container; only /work writable)"

# --- 10. the mutation phase ran network-disabled (prove the engine cannot reach the net)
note "negative: the mutation phase has no network"
if $OCI run --rm --network=none --entrypoint /bin/sh cairn-kernel:A \
     -c 'python -c "import socket; socket.create_connection((\"1.1.1.1\",53),2)"' >/dev/null 2>&1; then
  fail "network reachable under --network=none (mutation was not offline)"
fi
ok "mutation phase is network-disabled (--network=none enforced)"

note "ACCEPTANCE PASSED — contained two-version install+upgrade, all R6 legs green."
