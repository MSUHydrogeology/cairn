#!/usr/bin/env bash
#
# Phase 1 (acquire + verify) provenance gate for the contained-kernel recipe.
#
# The recipe runs the WRITE-CAPABLE engine offline in Phase 2; the only defence
# against baking a tampered engine is to verify, in a SEPARATE earlier step, that
# the Cairn source being baked is a PINNED, immutable reference — a release tag or
# a specific commit SHA — and to REFUSE a mutable branch ref (whose tip can be
# moved out from under the pin). This is that gate (Codex S5 / proposal F1).
#
# It composes with bootstrap/PROVENANCE.md: a clean install from a tagged release
# pinned by the lockfile is the fully-provenanced state; a mutable-branch build is
# not, and is refused here before the engine ever runs.
#
# Usage:  verify-ref.sh <cairn-repo> [ref]      (ref default: HEAD)
# Exit:   0 = verified pin (tag or commit);  1 = refused;  2 = usage / not-a-repo.

set -euo pipefail

REPO="${1:?usage: verify-ref.sh <cairn-repo> [ref]}"
REF="${2:-HEAD}"

git -C "$REPO" rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
  echo "verify-ref: REFUSED — not a git repository: $REPO" >&2; exit 2; }

# A branch name is a MUTABLE ref — its tip can move. Refuse it as a trust pin,
# however it is spelled (`foo`, `heads/foo`, `refs/heads/foo` all resolve to the
# same full refname). Resolve to the FULL symbolic name and reject anything under
# refs/heads/. `HEAD` is exempt: it names "the current commit", an immutable pin
# (classified as a commit pin below), not a request to track a moving branch tip.
if [ "$REF" != "HEAD" ]; then
  FULL="$(git -C "$REPO" rev-parse --symbolic-full-name "$REF" 2>/dev/null || true)"
  case "$FULL" in
    refs/heads/*)
      echo "verify-ref: REFUSED — '$REF' resolves to a mutable branch ($FULL); pin a" >&2
      echo "            release tag or a commit SHA instead (a branch tip can move)." >&2
      exit 1 ;;
  esac
fi

COMMIT="$(git -C "$REPO" rev-parse --verify "${REF}^{commit}" 2>/dev/null)" || {
  echo "verify-ref: REFUSED — '$REF' is not a resolvable commit or tag." >&2; exit 1; }

if TAG="$(git -C "$REPO" describe --exact-match --tags "$COMMIT" 2>/dev/null)"; then
  echo "verify-ref: OK — release tag '$TAG' -> $COMMIT"
elif [ "$REF" = "HEAD" ] || [ "$(printf '%s' "$REF" | tr 'A-F' 'a-f')" = "$(printf '%s' "$COMMIT" | cut -c1-${#REF})" ]; then
  # HEAD, or an explicit (full/abbreviated) commit SHA that matches the resolved
  # commit: an immutable, Maintainer-approved commit pin (no tag).
  echo "verify-ref: OK — commit pin $COMMIT (no exact tag; Maintainer-approved commit)"
else
  echo "verify-ref: REFUSED — '$REF' did not resolve to a tag or an immutable commit pin." >&2
  exit 1
fi

# REFUSE a dirty build surface (Codex cross-phase F#2). The recipe materializes
# the build context from the COMMIT OBJECT (acceptance.sh uses `git archive
# <commit>`), so the baked bytes match the emitted commit label by construction —
# but a tracked-dirty OR untracked build surface still means the operator is
# building something other than the pinned commit, so we **fail closed** rather
# than emit a misleading "commit pin" identity. The build surface is exactly the
# recipe's COPY set (Dockerfile): scaffold.py + _scaffold/ + templates/ + CITATION.cff.
BUILD_SURFACE="bootstrap/scaffold.py bootstrap/_scaffold templates CITATION.cff"
# shellcheck disable=SC2086  # word-splitting is intentional: multiple pathspecs
DIRTY="$(git -C "$REPO" status --porcelain -- $BUILD_SURFACE 2>/dev/null || true)"
if [ -n "$DIRTY" ]; then
  echo "verify-ref: REFUSED — the build surface has uncommitted or untracked changes;" >&2
  echo "            a built image would NOT match the pin $COMMIT. Commit or stash them," >&2
  echo "            or build from a clean checkout of the pinned ref. Offending paths:" >&2
  printf '%s\n' "$DIRTY" | sed 's/^/              /' >&2
  exit 1
fi
