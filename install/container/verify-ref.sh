#!/usr/bin/env bash
#
# Phase 1 (acquire + verify) release-provenance gate for the contained-kernel
# recipe.
#
# The recipe runs the WRITE-CAPABLE engine offline in Phase 2; the only defence
# against baking a tampered engine is to establish, in a SEPARATE earlier step,
# that the Cairn source being baked is what Cairn's maintainer signed — and, when
# no signature is available, to say so in those words rather than to imply an
# approval nobody gave (Codex S5 / proposal F1 / proposal `release-authenticity`).
#
# THIS SCRIPT IS A CONVENIENCE, NOT THE TRUST ROOT (residual RA4). It lives in
# the candidate checkout, so running it is ALREADY executing candidate bytes. The
# primary documented path is the out-of-band bootstrap in bootstrap/PROVENANCE.md,
# which an adopter runs with system `git` from a workspace they created, against
# a fingerprint they compared on at least two independent channels. Run this
# script DOWNSTREAM of that bootstrap, never instead of it.
#
# Usage:
#   verify-ref.sh [--signers <roster>] <cairn-repo> <tag>
#   verify-ref.sh --unprovenanced <cairn-repo> [ref]
#
# Provenance mode is the DEFAULT. It requires a signed, name-bound annotated tag
# and a trusted roster (an OpenSSH `allowed_signers` file) supplied from OUTSIDE
# the candidate — `--signers <path>` or $CAIRN_ALLOWED_SIGNERS. There is NO
# fallback to repository config, to the candidate's files, or to the adopter's
# global git config: the artifact under verification never supplies the material
# it is verified against.
#
# The integrity-pin path is reachable only under an explicit --unprovenanced
# flag. It checks that a ref names an immutable object; it checks NO signature,
# and it says so in its own output and in its exit code.
#
# Exit contract:
#   0  PROVENANCED      — annotated tag object, signed by a rostered principal,
#                         and its SIGNED name equals the ref that was asked for
#   3  NOT PROVENANCED  — accepted integrity pin under --unprovenanced; no
#                         signature was checked
#   1  REFUSED          — some control failed (the reason names which)
#   2  usage error / not a git repository

set -euo pipefail

refuse() { printf 'verify-ref: REFUSED — %s\n' "$1" >&2; exit 1; }
usage()  { printf 'verify-ref: %s\n' "$1" >&2; exit 2; }

# --- argument parsing -------------------------------------------------------
# Scalars rather than arrays: this script runs under whatever bash the host
# offers, and bash 3.2 (the macOS system bash) errors on an empty-array
# expansion under `set -u`.
SIGNERS="${CAIRN_ALLOWED_SIGNERS:-}"
PROVENANCE=1
REPO=""
REF=""
NPOS=0
ENDOPTS=0
while [ "$#" -gt 0 ]; do
  if [ "$ENDOPTS" -eq 0 ]; then
    case "$1" in
      --signers)
        [ "$#" -ge 2 ] || usage "--signers needs a path"
        SIGNERS="$2"; shift 2; continue ;;
      --signers=*) SIGNERS="${1#--signers=}"; shift; continue ;;
      --unprovenanced) PROVENANCE=0; shift; continue ;;
      --) ENDOPTS=1; shift; continue ;;
      -?*) usage "unknown option '$1'" ;;
    esac
  fi
  NPOS=$((NPOS + 1))
  case "$NPOS" in
    1) REPO="$1" ;;
    2) REF="$1" ;;
    *) usage "too many arguments" ;;
  esac
  shift
done
[ "$NPOS" -ge 1 ] || usage \
  "usage: verify-ref.sh [--signers <roster>] <cairn-repo> <tag> | --unprovenanced <cairn-repo> [ref]"
[ "$NPOS" -ge 2 ] || REF="HEAD"

# --- toolchain: refuse, never degrade (B3) ----------------------------------
# This MUST precede the first git invocation. Sitting the check inside
# provenance mode left it dead code: with git off PATH the repository probe
# below failed and the script reported `not a git repository: <a valid
# repository>` and exit 2 — a misdiagnosis of a missing toolchain as a bad
# argument. `ssh-keygen` is checked further down, in provenance mode, which is
# the only mode that uses it.
command -v git >/dev/null 2>&1 || refuse "git is not on PATH; verification cannot be performed"

git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1 || {
  echo "verify-ref: not a git repository: $REPO" >&2; exit 2; }

# `git -C` accepted it, so $REPO is an existing local DIRECTORY (a clone URL
# never reaches here — `-C` cannot change into one). Make it ABSOLUTE now:
# the fetch below runs `git -C "$WS"` inside the temporary workspace, so a
# RELATIVE candidate path would be resolved against that workspace instead of
# against the caller's cwd. Measured 2026-08-03, git 2.53.0: from inside a valid
# candidate, `--signers ../roster . <tag>` refused with `could not fetch
# 'refs/tags/<tag>' from the candidate (.)` — fail-closed, but a misleading
# reason on an honest input.
REPO="$(cd -P "$REPO" 2>/dev/null && pwd -P)" || \
  refuse "could not resolve the candidate path to an absolute path: $REPO"

# --- a mutable branch is never a pin, in either mode ------------------------
# A branch name is a MUTABLE ref — its tip can move. Refuse it as a trust pin,
# however it is spelled (`foo`, `heads/foo`, `refs/heads/foo` all resolve to the
# same full refname). `HEAD` is exempt here: it names "the current commit", which
# provenance mode refuses below and --unprovenanced classifies as a commit pin.
if [ "$REF" != "HEAD" ]; then
  FULL="$(git -C "$REPO" rev-parse --symbolic-full-name "$REF" 2>/dev/null || true)"
  case "$FULL" in
    refs/heads/*)
      refuse "'$REF' resolves to a mutable branch ($FULL); pin a signed release tag (a branch tip can move)" ;;
  esac
fi

# --- the dirty-build-surface refusal, preserved unchanged (Codex F#2) -------
# The recipe materializes the build context from the COMMIT OBJECT (acceptance.sh
# uses `git archive <commit>`), so the baked bytes match the emitted commit label
# by construction — but a tracked-dirty OR untracked build surface still means the
# operator is building something other than the pinned ref, so we **fail closed**
# rather than emit a misleading identity. The build surface is exactly the
# recipe's COPY set (Dockerfile). A bare candidate has no working tree; there the
# probe is empty and the check is a no-op.
check_build_surface() {
  local surface="bootstrap/scaffold.py bootstrap/_scaffold templates CITATION.cff" dirty
  # shellcheck disable=SC2086  # word-splitting is intentional: multiple pathspecs
  dirty="$(git -C "$REPO" status --porcelain -- $surface 2>/dev/null || true)"
  if [ -n "$dirty" ]; then
    echo "verify-ref: REFUSED — the build surface has uncommitted or untracked changes;" >&2
    echo "            a built image would NOT match the pin. Commit or stash them, or" >&2
    echo "            build from a clean checkout of the pinned ref. Offending paths:" >&2
    printf '%s\n' "$dirty" | sed 's/^/              /' >&2
    exit 1
  fi
}

# ---------------------------------------------------------------------------
# --unprovenanced: an integrity pin, and nothing more
# ---------------------------------------------------------------------------
if [ "$PROVENANCE" -eq 0 ]; then
  COMMIT="$(git -C "$REPO" rev-parse --verify "${REF}^{commit}" 2>/dev/null)" || \
    refuse "'$REF' is not a resolvable commit or tag"
  if [ "$REF" != "HEAD" ] && \
     ! git -C "$REPO" rev-parse --verify --quiet "refs/tags/${REF#refs/tags/}" >/dev/null 2>&1; then
    # Not HEAD and not a tag name, so the only remaining pin is an object id.
    case "$REF" in
      *[!0-9a-fA-F]*) refuse "'$REF' did not resolve to a tag or an immutable commit pin" ;;
    esac
    # An ABBREVIATED prefix is not a pin — it can become ambiguous as the object
    # database grows — so refuse it always (it used to be accepted).
    if [ "${#REF}" -ne 40 ] && [ "${#REF}" -ne 64 ]; then
      refuse "'$REF' is an abbreviated commit SHA; pass the full object id"
    fi
    [ "$(printf '%s' "$REF" | tr 'A-F' 'a-f')" = "$COMMIT" ] || \
      refuse "'$REF' did not resolve to itself ($COMMIT); not an immutable commit pin"
  fi
  check_build_surface
  echo "verify-ref: NOT PROVENANCED — commit pin $COMMIT (integrity only; no signature checked)"
  exit 3
fi

# ---------------------------------------------------------------------------
# provenance mode (the default)
# ---------------------------------------------------------------------------

# The caller asks about a TAG NAME. `refs/tags/<name>` is accepted as a spelling
# of the same thing; any other fully-qualified ref is not a release tag. The name
# comparison below is on the full tag name, so `release/v0.7.0` works.
TAGNAME="$REF"
case "$TAGNAME" in
  refs/tags/*) TAGNAME="${TAGNAME#refs/tags/}" ;;
  refs/*) refuse "provenance mode takes a tag name (or refs/tags/<name>), not '$REF'" ;;
  HEAD) refuse "'HEAD' names a commit, not a signed release tag; pass a tag name, or pass --unprovenanced for an integrity pin only" ;;
esac
[ -n "$TAGNAME" ] || refuse "empty tag name"

# --- tooling: refuse, never degrade (B3) ------------------------------------
# `git` is checked at the top, ahead of the first git invocation. `ssh-keygen`
# is checked HERE because provenance mode is the only mode that uses it.
command -v ssh-keygen >/dev/null 2>&1 || refuse "ssh-keygen is not on PATH; SSH signature verification cannot be performed"

# --- the trusted roster: required, external, contained (B1/B2) --------------
[ -n "$SIGNERS" ] || refuse \
  "provenance mode needs a trusted roster: pass --signers <path> or set CAIRN_ALLOWED_SIGNERS. There is no default and no fallback — see bootstrap/PROVENANCE.md for how to build one out of band"

# Canonicalize an EXISTING path: follow a symlinked leaf, then resolve the
# parent directory with `cd -P`. Portable across the BSD and GNU userlands (no
# `realpath` dependency).
canon() {
  local p="$1" t n=0
  while [ -L "$p" ] && [ "$n" -lt 40 ]; do
    t="$(readlink "$p")"
    case "$t" in
      /*) p="$t" ;;
      *)  p="$(dirname "$p")/$t" ;;
    esac
    n=$((n + 1))
  done
  if [ -d "$p" ]; then (cd -P "$p" >/dev/null 2>&1 && pwd -P)
  else printf '%s/%s\n' "$(cd -P "$(dirname "$p")" >/dev/null 2>&1 && pwd -P)" "$(basename "$p")"
  fi
}

[ -e "$SIGNERS" ] || refuse "trusted roster not found: $SIGNERS"
[ ! -d "$SIGNERS" ] || refuse "trusted roster is a directory, not a file: $SIGNERS"
[ -f "$SIGNERS" ] || refuse "trusted roster is not a regular file: $SIGNERS"
[ -r "$SIGNERS" ] || refuse "trusted roster is not readable: $SIGNERS"
ROSTER="$(canon "$SIGNERS")"

# CONTAINMENT — the roster must not come from the tree being verified. Cairn's
# own dev/.cairn/allowed_signers is the INTERNAL gate roster and is never
# consulted for release verification; an adopter's roster lives outside every
# candidate. Symlinks are resolved first, so a link into the candidate is caught.
#
# RECORDED AS NOT ESTABLISHED: this is a PATH property, not a CONTENT property.
# A hardlinked roster, or one rewritten between this check and the read below,
# is NOT covered. Closing that needs a content-level anchor (read once, hash,
# verify against the hash), which this scope did not build.
CAND_TOP="$(git -C "$REPO" rev-parse --show-toplevel 2>/dev/null || true)"
CAND_GITDIR="$(git -C "$REPO" rev-parse --absolute-git-dir 2>/dev/null || true)"
for cand_root in "$CAND_TOP" "$CAND_GITDIR" "$REPO"; do
  [ -n "$cand_root" ] && [ -d "$cand_root" ] || continue
  cand_canon="$(canon "$cand_root")"
  case "$ROSTER" in
    "$cand_canon"|"$cand_canon"/*)
      refuse "the trusted roster ($SIGNERS) resolves inside the candidate tree ($cand_canon); the artifact under verification cannot supply the material it is verified against" ;;
  esac
done

# --- roster shape: refuse a roster that cannot express a trust decision ------
# An `allowed_signers` line is `principal[,principal] [options] <keytype> <key>`,
# so a usable line has at least three fields. A one-field line is the
# copy-paste failure where $CAIRN_KEY expanded to nothing.
PRINCIPALS=0
MALFORMED=""
while IFS= read -r line || [ -n "$line" ]; do
  case "$line" in ''|'#'*) continue ;; esac
  # Field count without globbing (`set -f`): a usable line is at least
  # `<principals> <keytype> <key>`.
  read -r f_principals f_two f_three _rest <<EOF
$line
EOF
  if [ -z "${f_two:-}" ] || [ -z "${f_three:-}" ]; then MALFORMED="$line"; break; fi
  # The first field may carry COMMA-SEPARATED principals; count them all. This
  # is the parsing defect the sibling surface found at 0c6d9de — a roster line
  # `a@x,b@y <key>` names two principals, not one.
  rest_principals="$f_principals"
  while [ -n "$rest_principals" ]; do
    part="${rest_principals%%,*}"
    [ -z "$part" ] || PRINCIPALS=$((PRINCIPALS + 1))
    case "$rest_principals" in
      *,*) rest_principals="${rest_principals#*,}" ;;
      *)   rest_principals="" ;;
    esac
  done
done < "$ROSTER"
[ -z "$MALFORMED" ] || refuse \
  "the trusted roster has a line with no key (a principal alone is not a trust decision): $MALFORMED"
[ "$PRINCIPALS" -gt 0 ] || refuse "the trusted roster names no principals: $SIGNERS"

# ADOPTER HYGIENE, not a Cairn-side control (residual RA1 (a)). This counts
# principals in a file the ADOPTER typed, in a script bootstrap/PROVENANCE.md
# demotes to a convenience, with no channel back to Cairn — a fork with two
# maintainers trips it on day one, which is why it WARNS rather than refuses.
# Cairn's own single-signer posture is pinned in Cairn's own suite instead
# (bootstrap/tests/test_verify_ref.py::test_cairn_roster_names_one_principal).
if [ "$PRINCIPALS" -gt 1 ]; then
  echo "verify-ref: NOTE — the trusted roster names $PRINCIPALS principals; any one of them" >&2
  echo "            can sign a release you will accept. Confirm that is what you meant." >&2
fi

# --- a throwaway workspace THIS SCRIPT creates (A4) -------------------------
# Verification never runs `git -C <candidate> verify-tag`: that would let the
# candidate's own config choose the verifier, the roster, or the signature
# format. We fetch exactly one ref into a bare repository we created, and every
# later git invocation runs there with the verification config PINNED by -c.
#
# STATED LIMIT: the fetch itself still runs `git upload-pack` inside the
# candidate, which reads the candidate's config. That class is closed for the
# VERIFICATION step by construction and is not swept (residual RA5); it is
# another reason this script is a convenience downstream of the out-of-band
# bootstrap, not the trust root.
WORKSPACE="$(mktemp -d 2>/dev/null)" || refuse \
  "could not create a temporary verification workspace; refusing rather than verifying in place"
trap 'rm -rf "$WORKSPACE"' EXIT
WS="$WORKSPACE/verify"

# Every workspace command runs with the ADOPTER's global/system git config
# neutralised: `-c` already pins the keys that decide the verification, and an
# empty config removes the rest. Scoped to these calls (a prefix assignment on a
# simple command) so the build-surface probe below still sees the operator's own
# core.excludesFile and reports what they would see.
# The workspace's sterility contract, stated rather than implied.
#
# `$WS` is created by THIS script, so its config is not candidate-controlled --
# that is the property the fetch-time object check below rests on, and it is
# why the check cannot be configured away by the repository being verified.
# `GIT_CONFIG_GLOBAL`/`SYSTEM` are neutralised so the operator's own config
# cannot relax it either. What is deliberately NOT relied on: pinning
# `fsck.*` on the command line. Those settings are read from the repository
# doing the checking, and `fsck.skipList` is multi-valued, so a `-c` pin
# accumulates rather than replaces -- a fresh workspace is the only mechanism
# that closes the family rather than chasing its members.
wsgit() { GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null git "$@"; }

wsgit init --quiet --bare "$WS" 2>/dev/null || refuse "could not initialise the verification workspace"
# Object validation at the acquisition boundary: incoming objects are checked
# as they arrive, before any tag-name or signature claim is made about them.
# `fsck` proves STRUCTURAL integrity only -- not authorship, not authorization.
if ! wsgit -C "$WS" -c fetch.fsckObjects=true -c transfer.fsckObjects=true \
     fetch --no-tags --quiet "$REPO" "+refs/tags/$TAGNAME:refs/tags/$TAGNAME" 2>/dev/null; then
  # Name the cause. A fetch of an absent source ref fails the same way a fetch
  # that could not run at all does, so re-probe the candidate for the ref: the
  # probe can only make the refusal MORE specific, never turn one into a pass.
  if ! git -C "$REPO" rev-parse --verify --quiet "refs/tags/$TAGNAME" >/dev/null 2>&1; then
    refuse "no such tag ref 'refs/tags/$TAGNAME' in the candidate ($REPO)"
  fi
  refuse "could not fetch 'refs/tags/$TAGNAME' from the candidate ($REPO)"
fi

# --- resolve the caller's ref to ONE tag object (A1) ------------------------
# `^{tag}` does NOT peel through a tag that wraps another tag, which is what
# makes the name check below meaningful against a nested wrap.
#
# Measured 2026-08-03, git 2.53.0: `rev-parse --verify 'refs/tags/<x>^{tag}'`
# exits 128 without --quiet and 1 with it, and --quiet does NOT suppress the
# `dereferences to tree type` line on stderr — so `2>/dev/null` is load-bearing,
# and the `|| ...` guard is too (under `set -euo pipefail` the non-zero exit
# would otherwise abort the script instead of refusing). Both failures return
# rc=1 with empty stdout, so the two causes are re-probed apart below rather
# than collapsed into one message.
if ! OBJ="$(wsgit -C "$WS" rev-parse --verify --quiet "refs/tags/$TAGNAME^{tag}" 2>/dev/null)"; then
  if wsgit -C "$WS" rev-parse --verify --quiet "refs/tags/$TAGNAME" >/dev/null 2>&1; then
    refuse "ref 'refs/tags/$TAGNAME' exists but points at a NON-TAG object (a commit or a tree), which cannot carry a signature; a signed release tag is created with 'git tag -s'"
  fi
  refuse "no such tag ref 'refs/tags/$TAGNAME' in the candidate ($REPO)"
fi

# --- bind the SIGNED name to the name that was asked for (A2) ---------------
# The tag-substitution attack: an attacker with forge write access and NO key
# re-points a NEW version name at an OLDER, genuinely signed tag object. The
# signature is real; the signed payload names the old release. Reading the name
# out of the SIGNED payload — and refusing unless it equals the ref asked for —
# is what turns a good signature into an answer to the question that was asked.
RAW="$(wsgit -C "$WS" cat-file -p "$OBJ" 2>/dev/null)" || \
  refuse "could not read the tag object $OBJ"
# Header-bounded: stop recording at the first blank line, so a `tag ` line in the
# tag MESSAGE (attacker-controlled free text) can never be read as the name.
SIGNED_NAME="$(printf '%s\n' "$RAW" | awk '
  /^$/ { stop = 1 }
  !stop && /^tag / && name == "" { name = substr($0, 5) }
  END { print name }')"
[ -n "$SIGNED_NAME" ] || refuse "tag object $OBJ carries no signed name"
[ "$SIGNED_NAME" = "$TAGNAME" ] || refuse \
  "ref '$TAGNAME' resolves to a tag object whose SIGNED name is '$SIGNED_NAME' — the signature does not answer the question that was asked"

# --- verify THE OBJECT ID against the trusted roster (A3) -------------------
# The roster is pinned by invocation, and the verifier program with it: a
# candidate that sets gpg.ssh.program in its own config never gets a vote,
# because the verification runs in the workspace this script created.
#
# JUDGE THE EXIT CODE, NEVER THE TEXT: measured 2026-08-03, git 2.53.0 prints a
# line beginning `Good "git" signature` on the wrong-roster and empty-roster
# refusals too, and exits 1. Only the exit code separates them.
set +e
VERIFY_OUT="$(wsgit -C "$WS" \
  -c gpg.format=ssh \
  -c gpg.ssh.allowedSignersFile="$ROSTER" \
  -c gpg.ssh.program=ssh-keygen \
  -c gpg.program=gpg \
  verify-tag "$OBJ" 2>&1)"
VERIFY_RC=$?
set -e

# CLAIM <= EVIDENCE (P5). A non-zero exit from `git verify-tag` collapses two
# different facts, and only ONE of them is about the signature:
#
#   * a VERDICT WAS REACHED — the signature was checked and rejected, or git
#     established there is none. Measured 2026-08-03, git 2.53.0:
#       wrong roster  -> `Good "git" signature with ED25519 key ...`
#                        `No principal matched.`
#       unsigned tag  -> `error: no signature found`
#       tampered      -> `Could not verify signature.`
#                        `Signature verification failed: incorrect signature`
#   * verification COULD NOT RUN — nothing about the signature was checked at
#     all. Measured, same git:
#       unwritable TMPDIR -> `error: could not create temporary file: ...`
#                            (macOS `mktemp -d` ignores TMPDIR, so the workspace
#                             above is created and only git's own temp file
#                             fails — the two do not fail together)
#       a broken ssh-keygen -> its own loader/link error, and no verdict text
#
# Reporting the second as "did not verify against the trusted roster" asserts a
# check that never happened. So the roster claim is made ONLY on POSITIVE
# evidence that a verdict was reached; with no such evidence the refusal states
# the weaker, true thing. Both are refusals — this changes what is CLAIMED, not
# whether the script fails closed.
# THREE classes, not two. `no signature found` IS a verdict — git looked and
# established there is nothing to check — but it is NOT a roster comparison:
# no signature existed, so none was measured against $SIGNERS. Folding it into
# the roster refusal asserts a comparison that never happened and points the
# adopter at a roster file that is not the problem. Measured 2026-08-03,
# git 2.53.0: an annotated UNSIGNED tag emits exactly `error: no signature
# found`, rc=1.
VERDICT_REACHED=0
NO_SIGNATURE=0
case "$VERIFY_OUT" in
  *'no signature found'*)            VERDICT_REACHED=1; NO_SIGNATURE=1 ;;
  *'Good "git" signature'*)          VERDICT_REACHED=1 ;;
  *'No principal matched'*)          VERDICT_REACHED=1 ;;
  *'Could not verify signature'*)    VERDICT_REACHED=1 ;;
  *'Signature verification failed'*) VERDICT_REACHED=1 ;;
esac
if [ "$VERIFY_RC" -ne 0 ] && [ "$NO_SIGNATURE" -eq 1 ]; then
  refuse "tag '$TAGNAME' (object $OBJ) carries NO SIGNATURE — nothing was compared against the roster ($SIGNERS), which is not the problem here"
fi
if [ "$VERIFY_RC" -ne 0 ] && [ "$VERDICT_REACHED" -eq 1 ]; then
  refuse "the signature on tag '$TAGNAME' (object $OBJ) did not verify against the trusted roster ($SIGNERS)"
fi
if [ "$VERIFY_RC" -ne 0 ]; then
  refuse "verification of tag '$TAGNAME' (object $OBJ) COULD NOT BE PERFORMED — git reached no signature verdict, so NOTHING is asserted here about the signature or the roster. git said: $(printf '%s' "$VERIFY_OUT" | tr '\n' ' ')"
fi

PRINCIPAL="$(printf '%s\n' "$VERIFY_OUT" | sed -n 's/^Good "git" signature for \([^ ]*\) with .*/\1/p' | head -1)"
[ -n "$PRINCIPAL" ] || PRINCIPAL="(principal not reported by git)"

check_build_surface

COMMIT="$(wsgit -C "$WS" rev-parse --verify --quiet "$OBJ^{commit}" 2>/dev/null || true)"
echo "verify-ref: PROVENANCED — annotated tag '$TAGNAME' signed by $PRINCIPAL -> $OBJ"
[ -z "$COMMIT" ] || echo "verify-ref: tag object $OBJ -> commit $COMMIT"
exit 0
