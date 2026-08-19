#!/bin/sh
#
# THE RE-ANCHOR LAUNCHER -- REVIEWED SOURCE, NOT THE OPERATIVE COPY.
#
# This file is the text an External Security review reads. The copy the
# Maintainer runs is produced by that review: it fills the ONE slot below with
# the SHA-256 of the authorization packet it reviewed alongside these bytes, and
# records the resulting launcher's own digest. The two travel together, out of
# band, directly to the Maintainer.
#
# WHY THE SLOT IS THE ONLY ONE. Reviewed bytes must stay constant while
# late-bound values arrive as arguments -- the same split the recorded hash set
# already uses. The candidate OID is an ARGUMENT, never a literal, which is what
# lets the review happen before the candidate commit exists. If it were a slot,
# the reviewed bytes would change every ceremony and the review would be of
# something nobody ran.
#
# WHAT THE MAINTAINER VERIFIES: the launcher's digest, which the review already
# records. That one comparison covers the packet too, because the packet's
# digest is bound into these bytes. Altering the launcher changes the digest the
# review recorded; altering the packet fails the comparison below.
#
# THE PACKET IS AN AUTHORITY INPUT, not a carrier -- its rows decide which
# candidate bytes may execute. What makes it safe is the binding, not its
# billing.

LC_ALL=C
export LC_ALL

set -u

#: Filled by the review that produced the operative launcher. An unfilled
#: template refuses: the placeholder is not 64 hex characters, so the comparison
#: below cannot pass by accident.
PACKET_SHA256='@PACKET_SHA256@'

PACKET_SCHEMA='cairn-authorization-packet/v1'
REVIEW_MANIFEST_SCHEMA='cairn-review-manifest/v1'
MAX_PACKET_BYTES=65536
MAX_VALUES_BYTES=65536
MAX_LINE_BYTES=4096

#: THE MEMBER SET IS FIXED HERE, in LC_ALL=C order, and compared before
#: anything else. Everything the packet says validates the packet against
#: ITSELF; none of it establishes WHICH FILES the authority closure consists of.
#: A packet that dropped a member or added one parses cleanly and hashes
#: correctly -- it is a well-formed packet describing a different closure. Only
#: a fixed, reviewed, out-of-band list can catch that, and it must be compared
#: by these bytes rather than by anything the candidate provides.
#:
#: Compared with the shell's own string equality -- no `cmp`, no `diff` -- so no
#: utility joins the pre-candidate trust set for this check.
EXPECTED_PATHS='bootstrap/REANCHOR_RUNBOOK.md
bootstrap/reanchor.sh
bootstrap/tests/_gate_manifest.py
bootstrap/tests/_gate_preflight.py
bootstrap/tests/_gate_reanchor.py
bootstrap/tests/_gate_transition.py
bootstrap/tests/_oracle.py
bootstrap/tests/_oracle_activation.py
bootstrap/tests/_oracle_trust.py
dev/.cairn/allowed_signers
'

ARTIFACT_REL='bootstrap/reanchor.sh'

#: The trust root this ceremony moves. Named here rather than taken as an
#: argument: which ref is the anchor is not the operator's to choose.
ANCHOR_REF='refs/cairn/gate-anchor'

die() {
    printf 'REFUSE: %s\n' "$*" >&2
    exit 1
}

usage() {
    printf '%s\n' \
        'usage: reanchor-launcher.sh <packet> <values-file> <candidate-ref>' \
        '' \
        '  packet         the authorization packet delivered with this' \
        '                 launcher. Its SHA-256 is bound into these bytes.' \
        '  values-file    your recorded ceremony values' \
        '  candidate-ref  the ref or OID to re-anchor to' \
        '' \
        '  add  --stage2 <digest>  to run the SIGNING stage. It repeats the' \
        '  whole verification into a fresh directory rather than reusing the' \
        '  one stage 1 left behind -- candidate code ran while that one sat' \
        '  on disk.' >&2
}

# --------------------------------------------------------------------------
# path predicates -- pre-candidate, builtins only
# --------------------------------------------------------------------------

no_symlink_on_path() {
    _nsp_what=$1
    _nsp_p=$2
    while : ; do
        [ ! -L "$_nsp_p" ] || die "$_nsp_what: '$_nsp_p' is a symbolic link"
        case $_nsp_p in
            /|'') break ;;
        esac
        _nsp_parent=${_nsp_p%/*}
        [ -n "$_nsp_parent" ] || _nsp_parent=/
        [ "$_nsp_parent" != "$_nsp_p" ] || break
        _nsp_p=$_nsp_parent
    done
}

require_absolute() {
    case $2 in
        /*) ;;
        *) die "$1: '$2' is not an absolute path" ;;
    esac
}

require_regular_file() {
    require_absolute "$1" "$2"
    no_symlink_on_path "$1" "$2"
    [ -e "$2" ] || die "$1: '$2' does not exist"
    [ -f "$2" ] || die "$1: '$2' is not a regular file"
}

require_executable() {
    require_regular_file "$1" "$2"
    [ -x "$2" ] || die "$1: '$2' is not executable"
}

is_hex64() {
    case $1 in
        *[!0123456789abcdef]*) return 1 ;;
    esac
    [ ${#1} -eq 64 ]
}

# --------------------------------------------------------------------------
# THE LAUNCHER'S OWN VALUES READER -- pre-candidate
# --------------------------------------------------------------------------
#
# The artifact has a values parser, and this is deliberately a second one.
# It has to be: the launcher needs `git`, `shasum`, `cat`, `mktemp` and `mkdir`
# BEFORE it can verify the artifact, and the artifact's parser is candidate code
# it has not yet cleared. A launcher that used it would be running the thing it
# is about to check.
#
# So this reader implements the SAME closed grammar and the SAME refusals, with
# NO ambient fallback -- and a parity test asserts the two agree on every rule,
# in both directions: neither may accept a value the other refuses. Two parsers
# of one artifact that drift is a defect this repository has already had.

read_values() {
    _rv_file=$1
    require_regular_file "values file" "$_rv_file"

    _rv_total=0
    _rv_lineno=0
    while IFS= read -r _rv_line || [ -n "$_rv_line" ]; do
        _rv_lineno=$((_rv_lineno + 1))
        _rv_len=${#_rv_line}
        _rv_total=$((_rv_total + _rv_len + 1))
        [ "$_rv_len" -le "$MAX_LINE_BYTES" ] \
            || die "values line $_rv_lineno exceeds $MAX_LINE_BYTES bytes"
        [ "$_rv_total" -le "$MAX_VALUES_BYTES" ] \
            || die "the values file exceeds $MAX_VALUES_BYTES bytes"

        case $_rv_line in
            *[[:cntrl:]]*)
                die "values line $_rv_lineno contains a control character" ;;
        esac
        [ -n "$_rv_line" ] || continue
        case $_rv_line in
            '#'*) continue ;;
        esac
        case $_rv_line in
            ' '*) die "values line $_rv_lineno begins with whitespace" ;;
        esac
        case $_rv_line in
            *' ') die "values line $_rv_lineno ends with whitespace" ;;
        esac
        case $_rv_line in
            *' '*) ;;
            *) die "values line $_rv_lineno has a key and no value" ;;
        esac

        _rv_key=${_rv_line%% *}
        _rv_value=${_rv_line#* }

        # The launcher reads only the fields IT uses. Every other key belongs to
        # the artifact's own parser, which runs on the same file afterwards --
        # so an unknown key is not accepted here, it is simply not this
        # reader's business, and the artifact refuses it. Duplicates of the
        # fields below still refuse here, because this reader would otherwise
        # silently take one of two disagreeing values.
        case $_rv_key in
        checkout) [ -z "${L_checkout+s}" ] || die "duplicate key 'checkout'"
                  L_checkout=$_rv_value ;;
        git)      [ -z "${L_git+s}" ]      || die "duplicate key 'git'"
                  L_git=$_rv_value ;;
        shasum)   [ -z "${L_shasum+s}" ]   || die "duplicate key 'shasum'"
                  L_shasum=$_rv_value ;;
        mktemp)   [ -z "${L_mktemp+s}" ]   || die "duplicate key 'mktemp'"
                  L_mktemp=$_rv_value ;;
        mkdir)    [ -z "${L_mkdir+s}" ]    || die "duplicate key 'mkdir'"
                  L_mkdir=$_rv_value ;;
        cat)      [ -z "${L_cat+s}" ]      || die "duplicate key 'cat'"
                  L_cat=$_rv_value ;;
        env)      [ -z "${L_env+s}" ]      || die "duplicate key 'env'"
                  L_env=$_rv_value ;;
        esac
    done < "$_rv_file"

    # NO AMBIENT FALLBACK. Absent means refuse, never "find it on PATH".
    [ -n "${L_checkout+s}" ] || die "values file: missing required key 'checkout'"
    [ -n "${L_git+s}" ]      || die "values file: missing required key 'git'"
    [ -n "${L_shasum+s}" ]   || die "values file: missing required key 'shasum'"
    [ -n "${L_mktemp+s}" ]   || die "values file: missing required key 'mktemp'"
    [ -n "${L_mkdir+s}" ]    || die "values file: missing required key 'mkdir'"
    [ -n "${L_cat+s}" ]      || die "values file: missing required key 'cat'"
    [ -n "${L_env+s}" ]      || die "values file: missing required key 'env'"

    require_absolute "checkout" "$L_checkout"
    no_symlink_on_path "checkout" "$L_checkout"
    [ -d "$L_checkout" ] || die "checkout: '$L_checkout' is not a directory"
    require_executable "git" "$L_git"
    require_executable "shasum" "$L_shasum"
    require_executable "mktemp" "$L_mktemp"
    require_executable "mkdir" "$L_mkdir"
    require_executable "cat" "$L_cat"
    require_executable "env" "$L_env"
}

# --------------------------------------------------------------------------
# THE PACKET -- hashed before it is parsed, parsed only from what was hashed
# --------------------------------------------------------------------------
#
# What is verified and what is parsed must be the same bytes, or the
# verification describes a file that no longer exists by the time it matters.
#
# THE MECHANISM, in four steps and in this order:
#
#   1. hash the FILE and refuse unless it equals the digest bound into these
#      bytes;
#   2. snapshot it into memory with the trailing-byte-preserving idiom, through
#      the VALIDATED `cat` field -- never a bare `cat`, which would reach for an
#      unbound executable through ambient PATH;
#   3. re-hash the SNAPSHOT and refuse unless it equals step 1's digest;
#   4. parse ONLY the snapshot.
#
# STEP 3 IS WHAT MAKES THE DESIGN WORK. Steps 1 and 2 read the file twice, so a
# same-user writer can change it in between -- and the shell cannot carry a NUL
# through a variable, so a lossy snapshot is possible too. Step 3 DETECTS both:
# any byte the shell could not carry, and any byte that changed between the
# reads, makes the snapshot's digest differ and the launcher refuses.
#
# WHAT IT DOES NOT DO, stated rather than implied: step 3 detects, it does not
# prevent. That is the accepted same-user residual, unchanged and not enlarged.
# The single-buffer property is delivered for PARSING; the READING is two passes
# cross-checked, and this comment says so rather than claiming otherwise.
#
# The packet format is NUL-free by definition, and step 3 is what enforces it.

read_packet() {
    _rp_path=$1
    require_regular_file "packet" "$_rp_path"

    is_hex64 "$PACKET_SHA256" || die \
        "this launcher's embedded packet digest is not 64 hex characters" \
        "('$PACKET_SHA256'). An UNFILLED TEMPLATE is not an operative" \
        "launcher: the review that reviewed these bytes is what fills it"

    # --- step 1: hash the file --------------------------------------------
    _rp_d1=$("$L_SHASUM" -a 256 "$_rp_path") || die "cannot hash the packet"
    # `${d%% *}` rather than `cut`, so no utility joins the pre-candidate
    # trust set just to split one field.
    _rp_d1=${_rp_d1%% *}
    is_hex64 "$_rp_d1" || die "the packet digest is not 64 hex characters"
    [ "$_rp_d1" = "$PACKET_SHA256" ] || die \
        "the packet does not match the digest bound into this launcher." \
        "Expected $PACKET_SHA256, got $_rp_d1. Either these are not the two" \
        "artifacts the review delivered as a pair, or one of them changed"

    # --- step 2: snapshot, preserving trailing bytes -----------------------
    # `$(...)` strips every trailing newline; appending a sentinel and removing
    # it is what preserves them. Through the validated field, never bare `cat`.
    PACKET_TEXT=$("$L_CAT" "$_rp_path"; printf x) || die "cannot read the packet"
    PACKET_TEXT=${PACKET_TEXT%x}

    # --- step 3: re-hash the SNAPSHOT --------------------------------------
    _rp_d2=$(printf '%s' "$PACKET_TEXT" | "$L_SHASUM" -a 256) \
        || die "cannot re-hash the packet snapshot"
    _rp_d2=${_rp_d2%% *}
    [ "$_rp_d2" = "$_rp_d1" ] || die \
        "the packet's bytes and the bytes this launcher holds differ" \
        "($_rp_d1 on disk, $_rp_d2 in memory). Either the file changed" \
        "between the two reads, or it contains a byte a shell variable cannot" \
        "carry. Both are refusals: what was verified must be what is parsed"
}

# --------------------------------------------------------------------------
# parsing the packet -- from the snapshot ONLY
# --------------------------------------------------------------------------

parse_packet() {
    P_provenance=''
    P_artifact=''
    P_artifact_sha=''
    P_rows=''
    P_paths=''
    _pp_schema_seen=''
    _pp_lineno=0

    # The heredoc's source is the in-memory snapshot, NOT the path. This is the
    # POSIX way to feed a loop from a variable without a pipe -- a pipe would
    # run the loop in a subshell, where every assignment above is discarded and
    # the parse would silently produce nothing.
    while IFS= read -r _pp_line || [ -n "$_pp_line" ]; do
        _pp_lineno=$((_pp_lineno + 1))
        [ ${#_pp_line} -le "$MAX_LINE_BYTES" ] \
            || die "packet line $_pp_lineno exceeds $MAX_LINE_BYTES bytes"
        case $_pp_line in
            *[[:cntrl:]]*)
                die "packet line $_pp_lineno contains a control character" ;;
        esac
        [ -n "$_pp_line" ] || continue
        case $_pp_line in
            '#'*) continue ;;
        esac
        case $_pp_line in
            ' '*|'	'*) die "packet line $_pp_lineno has leading whitespace" ;;
        esac

        _pp_kind=${_pp_line%% *}
        case $_pp_kind in
        schema)
            [ "$_pp_line" = "schema $PACKET_SCHEMA" ] \
                || die "packet line $_pp_lineno: unknown schema"
            _pp_schema_seen=yes ;;
        provenance)
            [ -z "$P_provenance" ] || die "duplicate provenance row"
            P_provenance=${_pp_line#provenance }
            [ -n "$P_provenance" ] || die "provenance is empty"
            [ ${#P_provenance} -le 120 ] || die "provenance exceeds 120 chars" ;;
        artifact)
            [ -z "$P_artifact" ] || die "duplicate artifact row"
            P_artifact=${_pp_line#artifact } ;;
        artifact_sha256)
            [ -z "$P_artifact_sha" ] || die "duplicate artifact_sha256 row"
            P_artifact_sha=${_pp_line#artifact_sha256 }
            is_hex64 "$P_artifact_sha" \
                || die "artifact_sha256 is not 64 hex characters" ;;
        member)
            _pp_rest=${_pp_line#member }
            _pp_sha=${_pp_rest%% *}
            _pp_path=${_pp_rest#* }
            is_hex64 "$_pp_sha" \
                || die "packet line $_pp_lineno: digest is not 64 hex chars"
            case $_pp_path in
                /*|*..*|'') die "packet line $_pp_lineno: bad member path" ;;
            esac
            P_rows="$P_rows$_pp_sha $_pp_path
"
            P_paths="$P_paths$_pp_path
" ;;
        candidate)
            # NOT a schema mistake -- a contract violation. The packet is
            # OID-free BY DESIGN: that is what lets the review produce it
            # before the candidate commit exists. A packet naming an OID is a
            # packet from a different contract.
            die "packet line $_pp_lineno: the packet must carry NO candidate" \
                "OID. The OID is an argument to this launcher, resolved here" \
                "and never taken from a reviewed artifact that predates it" ;;
        *)
            die "packet line $_pp_lineno: unknown row type '$_pp_kind'" ;;
        esac
    done <<PACKET
$PACKET_TEXT
PACKET

    [ -n "$_pp_schema_seen" ] || die "the packet has no schema row"
    [ -n "$P_provenance" ]    || die "the packet has no provenance row"
    [ -n "$P_artifact" ]      || die "the packet has no artifact row"
    [ -n "$P_artifact_sha" ]  || die "the packet has no artifact_sha256 row"
    [ -n "$P_rows" ]          || die "the packet has no member rows"

    # --- THE FIXED SET, compared before anything is resolved or extracted ---
    [ "$P_paths" = "$EXPECTED_PATHS" ] || die \
        "the packet's member set is not the authority closure recorded in" \
        "this launcher. A packet that dropped a member or added one still" \
        "parses and still hashes; only this comparison catches it"

    # --- R10's two closure constraints -------------------------------------
    # The artifact is IN the closure by construction, rather than being an
    # executable the packet happens to name alongside it.
    _pp_match=''
    _pp_count=0
    while IFS= read -r _pp_row || [ -n "$_pp_row" ]; do
        [ -n "$_pp_row" ] || continue
        if [ "${_pp_row#* }" = "$P_artifact" ]; then
            _pp_match=${_pp_row%% *}
            _pp_count=$((_pp_count + 1))
        fi
    done <<ROWS
$P_rows
ROWS
    [ "$_pp_count" -eq 1 ] || die \
        "the artifact path '$P_artifact' matches $_pp_count closure rows;" \
        "it must identify exactly one"
    [ "$_pp_match" = "$P_artifact_sha" ] || die \
        "the artifact's stated digest does not equal its closure row's" \
        "($P_artifact_sha vs $_pp_match). They are the same file"

    # The artifact this launcher will start is the artifact these bytes name.
    [ "$P_artifact" = "$ARTIFACT_REL" ] || die \
        "the packet names '$P_artifact' as the ceremony artifact; this" \
        "launcher starts '$ARTIFACT_REL' and will not start another"
}

# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

# STAGE 2 RUNS THROUGH THIS LAUNCHER TOO, and that is a security property
# rather than a convenience.
#
# Stage 2 must not reuse stage 1's extraction. Candidate code RAN in stage 1 --
# that is what stage 1 is for -- so everything stage 1 left on disk sat there
# through a window in which candidate code was executing as the same user.
# Handing those bytes to the signing stage would let the candidate rewrite the
# verifier that is about to bless it, after the key is loaded.
#
# So a second invocation does the whole pre-candidate verification again, from
# the same reviewed packet, into a FRESH directory: re-resolve, re-verify every
# closure blob, re-extract, re-check the artifact digest. It costs one extra
# pass and removes the entire class.
STAGE2_CONFIRM=''
if [ "$#" -eq 5 ] && [ "$4" = "--stage2" ]; then
    STAGE2_CONFIRM=$5
    set -- "$1" "$2" "$3"
fi
[ "$#" -eq 3 ] || { usage; exit 2; }
PACKET_PATH=$1
VALUES_PATH=$2
CANDIDATE_REF=$3

read_values "$VALUES_PATH"
L_SHASUM=$L_shasum
L_CAT=$L_cat

read_packet "$PACKET_PATH"
parse_packet

# --- the sterile git child -------------------------------------------------
# Object replacement, hooks and monitors off BEFORE the first read, and the
# environment emptied so no GIT_* variable steers the loader.
sterile_git() {
    "$L_env" -i HOME=/nonexistent \
        "$L_git" --no-replace-objects \
                 -c core.useReplaceRefs=false \
                 -c core.hooksPath=/dev/null \
                 -c core.fsmonitor=false \
                 -C "$L_checkout" "$@"
}

# --- resolve the candidate ONCE --------------------------------------------
# To a full object id, and every later read uses that id. A moving ref read
# twice is two different answers wearing one name.
RESOLVED=$(sterile_git rev-parse --verify --end-of-options \
           "$CANDIDATE_REF^{commit}") \
    || die "cannot resolve the candidate ref '$CANDIDATE_REF'"
case $RESOLVED in
    *[!0123456789abcdef]*) die "the resolved candidate is not an object id" ;;
esac

T=$("$L_mktemp" -d) || die "cannot create a working directory"

# CANONICALISE $T, once, immediately. Found by running this launcher end to
# end: on a stock macOS host `mktemp -d` returns a path under `/var`, and
# `/var` is a symlink to `/private/var`. The artifact then refused its own
# launcher's review manifest -- correct by its own rule, and the ceremony
# unrunnable.
#
# Resolving HERE is not a hole in that rule, and the distinction is the whole
# argument: the no-symlink rule governs paths SUPPLIED to the ceremony, where a
# link is a target that can change between the check and the use. `$T` is not
# supplied -- this launcher created it seconds ago, empty, and every path
# beneath it is one this launcher writes. Canonicalising it means the artifact's
# check passes ON THE MERITS rather than by exemption, which is the outcome to
# want: the alternative fix, exempting the manifest from the rule, would leave
# a genuinely unchecked path behind a special case.
#
# `cd` and `pwd` are shell builtins, so no utility joins the pre-candidate
# trust set for this.
T=$(cd "$T" && pwd -P) || die "cannot canonicalise the working directory"
case $T in
    /*) ;;
    *) die "the canonicalised working directory is not absolute: '$T'" ;;
esac

# --- verify EVERY closure blob at that OID, then extract -------------------
# `cat-file blob` reads raw object bytes. `git archive` is attribute-aware, so
# a candidate `.gitattributes` could reshape what lands.
while IFS= read -r ROW || [ -n "$ROW" ]; do
    [ -n "$ROW" ] || continue
    WANT=${ROW%% *}
    REL=${ROW#* }
    case $REL in
        */*) "$L_mkdir" -p "$T/${REL%/*}" || die "cannot create $T/${REL%/*}" ;;
    esac
    sterile_git cat-file blob "$RESOLVED:$REL" > "$T/$REL" \
        || die "the candidate $RESOLVED has no blob at '$REL'"
    GOT=$("$L_SHASUM" -a 256 "$T/$REL") || die "cannot hash '$REL'"
    GOT=${GOT%% *}
    [ "$GOT" = "$WANT" ] || die \
        "closure member '$REL' at $RESOLVED does not match the reviewed" \
        "digest (expected $WANT, got $GOT)"
done <<ROWS
$P_rows
ROWS

# --- the artifact's own digest, checked separately -------------------------
ART_GOT=$("$L_SHASUM" -a 256 "$T/$ARTIFACT_REL") || die "cannot hash the artifact"
ART_GOT=${ART_GOT%% *}
[ "$ART_GOT" = "$P_artifact_sha" ] || die \
    "the extracted ceremony artifact does not match the reviewed digest"

# --- COMPOSE the review manifest -------------------------------------------
# Composed, not sourced. Every value here comes from the packet -- the review's
# out-of-band output -- or from the resolution this launcher performed itself.
# NOTHING is read from the candidate. This is what removes the last point where
# a human or an agent had to assemble an authority input.
MANIFEST=$T/review-manifest.txt
{
    printf 'schema %s\n' "$REVIEW_MANIFEST_SCHEMA"
    printf 'candidate %s\n' "$RESOLVED"
    printf 'provenance %s\n' "$P_provenance"
    printf '%s' "$P_rows" | while IFS= read -r ROW || [ -n "$ROW" ]; do
        [ -n "$ROW" ] || continue
        printf 'member %s %s\n' "${ROW%% *}" "${ROW#* }"
    done
} > "$MANIFEST" || die "cannot write the review manifest"

# --- WHICH CEREMONY IS THIS? -----------------------------------------------
# The runbook this launcher replaces had TWO loaders, and a launcher that
# implemented only one would be narrower than the procedure it replaces --
# which the objective forbids in the same breath as it asks for one command.
#
# The distinction is not a flag and must not become one: transition mode exists
# ONLY to carry a closure change an external review approved, and the checker
# refuses it when there is nothing to carry. So the mode is MEASURED, not
# chosen: every closure member is compared at the anchor and at the resolved
# candidate, and a single difference makes this a transition.
#
# Measuring beats asking. An operator who picks the mode can pick wrong in the
# unsafe direction -- declaring "steady state" over a real closure change is
# exactly the substitution the reviewed-transition path exists to prevent.
CLOSURE_CHANGED=''
while IFS= read -r ROW || [ -n "$ROW" ]; do
    [ -n "$ROW" ] || continue
    REL=${ROW#* }
    ANCHORED=$(sterile_git cat-file blob "$ANCHOR_REF:$REL" 2>/dev/null \
               | "$L_SHASUM" -a 256) || ANCHORED=''
    ANCHORED=${ANCHORED%% *}
    if [ "$ANCHORED" != "${ROW%% *}" ]; then
        CLOSURE_CHANGED=yes
    fi
done <<ROWS
$P_rows
ROWS

printf '%s\n' "== launcher: candidate resolved and closure verified =="
printf '  candidate    %s\n' "$RESOLVED"
printf '  provenance   %s\n' "$P_provenance"
printf '  artifact     %s\n' "$ARTIFACT_REL"
printf '  manifest     %s\n' "$MANIFEST"
if [ -n "$CLOSURE_CHANGED" ]; then
    printf '  mode         TRANSITION -- the authority closure differs at the\n'
    printf '               candidate, so this ceremony carries a reviewed\n'
    printf '               closure change\n'
else
    printf '  mode         steady state -- the authority closure is identical\n'
    printf '               at the anchor and the candidate\n'
fi
printf '\n'

# --- ONLY NOW does candidate code start ------------------------------------
# Everything above ran on reviewed bytes: this launcher, the packet bound into
# it, and the values file its own reader validated. The artifact below is the
# first candidate byte to execute, and it executes only because its digest
# matched the reviewed one.
# `/bin/sh` LITERALLY, not a recorded field and not a preference: a
# non-interactive `/bin/sh` reads no startup file, which is the entire
# reason the child is clean. The obvious alternative on a macOS host is the
# login default `/bin/zsh`, and zsh sources `$HOME/.zshenv` even
# non-interactively -- which puts the operator's own command definitions
# straight back inside the supposedly clean child.
#
# `exec` rather than a call: nothing in this launcher runs after candidate
# code starts, so there is no post-candidate step for candidate code to
# influence. It also means $T is not cleaned up here -- it cannot be, the
# artifact is running out of it.
if [ -n "$STAGE2_CONFIRM" ]; then
    # Same verified extraction discipline, a different stage. The manifest is
    # composed afresh above from the same packet and the same resolution, so
    # stage 2 revalidates against bytes this invocation produced -- not against
    # a file left behind by the invocation that ran candidate code.
    if [ -n "$CLOSURE_CHANGED" ]; then
        exec /bin/sh "$T/$ARTIFACT_REL" stage2 "$VALUES_PATH" \
            --confirm-package-sha256 "$STAGE2_CONFIRM" \
            --review-manifest "$MANIFEST" \
            --reviewed-candidate "$RESOLVED"
    fi
    exec /bin/sh "$T/$ARTIFACT_REL" stage2 "$VALUES_PATH" \
        --confirm-package-sha256 "$STAGE2_CONFIRM"
fi

if [ -n "$CLOSURE_CHANGED" ]; then
    exec /bin/sh "$T/$ARTIFACT_REL" stage1 "$VALUES_PATH" \
        --review-manifest "$MANIFEST" \
        --reviewed-candidate "$RESOLVED"
fi
exec /bin/sh "$T/$ARTIFACT_REL" stage1 "$VALUES_PATH"
