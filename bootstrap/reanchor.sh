#!/bin/sh
#
# The Cairn re-anchor ceremony, as an artifact the Maintainer runs.
#
# WHY THIS FILE EXISTS. Every re-anchor before it was performed by pasting
# recorded shell blocks out of REANCHOR_RUNBOOK.md and filling thirteen
# placeholders by hand. In practice an assisting agent generated a script for
# each stage, which put the agent inside the trust path the ceremony's own
# fences exist to keep it out of -- and left the Maintainer authorizing a
# procedure they could not read end to end. A process that cannot be run by the
# person authorizing it is not secure, because the authorization is nominal.
#
# So the procedure is code: reviewed once, frozen into the authority closure,
# and driven by a values file the operator records once and edits rarely.
#
# WHAT THIS FILE IS NOT. It is not the trust root. It is candidate code, and it
# is started only after the launcher has verified its bytes against the digest
# bound into the launcher when the packet was built. It never loads a key, and stage 1
# refuses if it finds it can sign.

LC_ALL=C
export LC_ALL

set -u

#: The exact schema token. An unknown version refuses rather than being
#: best-effort accepted: values written for a different contract are not values
#: with a problem, they are an unreviewed input.
SCHEMA_VERSION='cairn-ceremony-values/v1'

refuse() {
    printf 'REFUSE: %s\n' "$*" >&2
    exit 1
}

#: The checker is located RELATIVE TO THIS ARTIFACT, never taken as an
#: argument and never found on PATH. Both files arrive in the same verified
#: extraction, so resolving one from the other keeps them a matched pair: a
#: checker path supplied from outside would let a verified artifact drive an
#: unverified checker, which is the whole hazard inverted.
case $0 in
    */*) ARTIFACT_DIR=${0%/*} ;;
    *)   ARTIFACT_DIR=. ;;
esac
CHECKER=$ARTIFACT_DIR/tests/_gate_preflight.py

# --------------------------------------------------------------------------
# path predicates
# --------------------------------------------------------------------------

#: Refuse if any component of the path -- the leaf or ANY parent -- is a
#: symbolic link. Checking only the leaf is the version that fails: a symlinked
#: parent redirects the whole subtree, and the leaf looks like an ordinary file
#: sitting in it.
no_symlink_on_path() {
    _nsp_what=$1
    _nsp_p=$2
    while : ; do
        if [ -L "$_nsp_p" ]; then
            refuse "$_nsp_what: '$_nsp_p' is a symbolic link; the ceremony" \
                   "resolves nothing, so a link anywhere on the path refuses"
        fi
        case $_nsp_p in
            /|'') break ;;
        esac
        _nsp_parent=${_nsp_p%/*}
        if [ -z "$_nsp_parent" ]; then
            _nsp_parent=/
        fi
        if [ "$_nsp_parent" = "$_nsp_p" ]; then
            break
        fi
        _nsp_p=$_nsp_parent
    done
}

require_absolute() {
    _ra_what=$1
    _ra_p=$2
    case $_ra_p in
        /*) ;;
        *) refuse "$_ra_what: '$_ra_p' is not an absolute path. Nothing is" \
                  "discovered and nothing is resolved against a working" \
                  "directory; a relative path names a different file" \
                  "depending on where the ceremony was started" ;;
    esac
}

#: An executable this ceremony will actually run. The bar is deliberately the
#: same for all of them, which is what makes the list auditable: absolute,
#: symlink-free on every component, an existing REGULAR file, and executable.
require_executable() {
    _re_what=$1
    _re_p=$2
    require_absolute "$_re_what" "$_re_p"
    no_symlink_on_path "$_re_what" "$_re_p"
    if [ ! -e "$_re_p" ]; then
        refuse "$_re_what: '$_re_p' does not exist"
    fi
    if [ ! -f "$_re_p" ]; then
        refuse "$_re_what: '$_re_p' is not a regular file"
    fi
    if [ ! -x "$_re_p" ]; then
        refuse "$_re_what: '$_re_p' is not executable"
    fi
}

require_regular_file() {
    _rf_what=$1
    _rf_p=$2
    require_absolute "$_rf_what" "$_rf_p"
    no_symlink_on_path "$_rf_what" "$_rf_p"
    if [ ! -e "$_rf_p" ]; then
        refuse "$_rf_what: '$_rf_p' does not exist"
    fi
    if [ ! -f "$_rf_p" ]; then
        refuse "$_rf_what: '$_rf_p' is not a regular file"
    fi
}

require_directory() {
    _rd_what=$1
    _rd_p=$2
    require_absolute "$_rd_what" "$_rd_p"
    if [ ! -d "$_rd_p" ]; then
        refuse "$_rd_what: '$_rd_p' is not an existing directory"
    fi
}

# --------------------------------------------------------------------------
# the thirteen values, handed in as arguments
# --------------------------------------------------------------------------
#
# THIS ARTIFACT READS NO VALUES FILE. The launcher is the only reader of that
# file: it checks every line and every path before any candidate byte runs, and
# starts this artifact with the thirteen checked values as its first arguments,
# in the schema's order:
#
#   schema checkout signing_key package home env git python mktemp mkdir
#   shasum sort cat
#
# The checks below are kept anyway, so a value handed to this artifact directly
# is refused when it is not a usable path. They are the same states the
# launcher's reader requires, and a test holds the two to the same refusals.

take_values() {
    [ "$#" -ge 13 ] || refuse "this command takes the 13 recorded values and" \
        "then its options; run it through the launcher, which supplies them" \
        "from your values file"

    V_schema=$1
    V_checkout=$2
    V_signing_key=$3
    V_package=$4
    V_home=$5
    V_env=$6
    V_git=$7
    V_python=$8
    V_mktemp=$9
    V_mkdir=${10}
    V_shasum=${11}
    V_sort=${12}
    V_cat=${13}

    if [ "$V_schema" != "$SCHEMA_VERSION" ]; then
        refuse "schema is '$V_schema'; this artifact reads" \
               "'$SCHEMA_VERSION' and nothing else"
    fi

    # --- required states, one per key, from the accepted schema table -------
    require_directory "checkout" "$V_checkout"
    no_symlink_on_path "checkout" "$V_checkout"
    if [ ! -e "$V_checkout/.git" ]; then
        refuse "checkout: '$V_checkout' is not a worktree top level (no" \
               ".git entry). git -C discovers UPWARD, so a path beneath a" \
               "repository would otherwise bless a repository never named"
    fi

    # `signing_key` is checked here for shape only. That it PARSES as a public
    # key is established at stage 1 by `validate_signing_key` in
    # bootstrap/tests/_gate_preflight.py, which runs `ssh-keygen -l -f` and
    # reports UNPROBEABLE when it does not. This artifact does not duplicate
    # that check, and does not claim to have made it.
    require_regular_file "signing_key" "$V_signing_key"

    # The package LEAF is stage-dependent -- absent at stage 1, present at
    # stage 2 -- so only its parent is judged here. The stage commands apply
    # their own leaf rule; `validate` reports the leaf's state without ruling
    # on it, because at validate time either state can be correct.
    _pv_pkg_parent=${V_package%/*}
    if [ -z "$_pv_pkg_parent" ]; then
        _pv_pkg_parent=/
    fi
    require_absolute "package" "$V_package"
    require_directory "package parent" "$_pv_pkg_parent"
    no_symlink_on_path "package parent" "$_pv_pkg_parent"

    require_directory "home" "$V_home"

    require_executable "env" "$V_env"
    require_executable "git" "$V_git"
    require_executable "python" "$V_python"
    require_executable "mktemp" "$V_mktemp"
    require_executable "mkdir" "$V_mkdir"
    require_executable "shasum" "$V_shasum"
    require_executable "sort" "$V_sort"
    require_executable "cat" "$V_cat"
}

# --------------------------------------------------------------------------
# the effective configuration
# --------------------------------------------------------------------------

#: Printed on EVERY command that takes the values, not only on `validate`.
#: The contract requires the Maintainer to see what will be used *before stage
#: 1*, and a stop-point on a command nobody runs is not a stop-point: the
#: launcher invokes `stage1` directly and never `validate`.
#:
#: Every field is printed because the values file carries no secret material --
#: no passphrase, no private key. "The complete effective non-secret
#: configuration" is therefore the whole file, and printing a subset would
#: imply a redaction that does not exist.
print_effective_configuration() {
    printf '%s\n' "== effective ceremony configuration =="
    printf '%s\n' "  (recorded in your values file, read once by the launcher --"
    printf '%s\n' "   nothing below was discovered)"
    printf '\n'
    printf '  %-12s %s\n' 'schema'      "$V_schema"
    printf '  %-12s %s\n' 'checkout'    "$V_checkout"
    printf '  %-12s %s\n' 'signing_key' "$V_signing_key"
    printf '  %-12s %s\n' 'package'     "$V_package"
    printf '  %-12s %s\n' 'home'        "$V_home"
    printf '\n'
    printf '%s\n' '  executables this ceremony will run:'
    printf '  %-12s %s\n' 'env'    "$V_env"
    printf '  %-12s %s\n' 'git'    "$V_git"
    printf '  %-12s %s\n' 'python' "$V_python"
    printf '  %-12s %s\n' 'mktemp' "$V_mktemp"
    printf '  %-12s %s\n' 'mkdir'  "$V_mkdir"
    printf '  %-12s %s\n' 'shasum' "$V_shasum"
    printf '  %-12s %s\n' 'sort'   "$V_sort"
    printf '  %-12s %s\n' 'cat'    "$V_cat"
    printf '\n'
    if [ -e "$V_package" ]; then
        printf '%s\n' "  package leaf: PRESENT (stage 2 expects this)"
    else
        printf '%s\n' "  package leaf: ABSENT (stage 1 expects this)"
    fi
    printf '\n'
}

# --------------------------------------------------------------------------
# the stage commands
# --------------------------------------------------------------------------

#: Both stages run the checker under a recorded, emptied environment. Nothing
#: is inherited: an ambient PATH is what once let a replacement `shasum` vouch
#: for bytes it had just rewritten, and an ambient GIT_* variable can steer git
#: at a repository nobody named.
#:
#: THE TWO STAGES DIFFER IN EXACTLY ONE ENVIRONMENT ENTRY, and the difference
#: is the boundary the ceremony exists to create:
#:
#:   stage 1 gets NO `SSH_AUTH_SOCK`. Its contract is that it cannot sign -- it
#:   runs candidate code to build an authorization package and exits -- so an
#:   agent socket buys it nothing while handing that candidate code a live
#:   signing channel. The channel is removed, not measured.
#:
#:   stage 2 forwards `SSH_AUTH_SOCK` if its caller has one, because stage 2 is
#:   the stage that signs. The runbook runs it with none: the key stays in no
#:   agent, and the signer asks for its passphrase on the terminal. A signer
#:   with neither a socket nor a terminal falls back to `ssh-askpass` and dies
#:   naming a path that does not exist on a stock host.
#:
#: A later cleanup that made these two blocks symmetric would break the
#: ceremony in one direction and the boundary in the other.

require_checker() {
    if [ ! -e "$CHECKER" ]; then
        refuse "the checker is not beside this artifact ($CHECKER). Both" \
               "arrive in one verified extraction; a missing one means this" \
               "artifact is running somewhere it was not placed"
    fi
    no_symlink_on_path "checker" "$CHECKER"
    if [ ! -f "$CHECKER" ]; then
        refuse "checker: '$CHECKER' is not a regular file"
    fi
}

#: Collect the optional transition arguments into the positional parameters.
#: `set --` is how POSIX sh builds an argument list without an array and
#: without `eval`; the alternative -- assembling a string and re-splitting it --
#: is word-splitting a path, which is how a path with a space becomes two
#: arguments.
TRANSITION_MANIFEST=''
TRANSITION_CANDIDATE=''

take_transition_options() {
    while [ "$#" -gt 0 ]; do
        case $1 in
        --review-manifest)
            [ "$#" -ge 2 ] || refuse "--review-manifest needs a value"
            TRANSITION_MANIFEST=$2
            shift 2 ;;
        --reviewed-candidate)
            [ "$#" -ge 2 ] || refuse "--reviewed-candidate needs a value"
            TRANSITION_CANDIDATE=$2
            shift 2 ;;
        *)
            refuse "unexpected argument '$1'" ;;
        esac
    done

    # Both or neither. A manifest without the OID it was reviewed against, or
    # an OID with no reviewed member set, is half a transition -- and half a
    # transition is an authority change with one of its two inputs missing.
    if [ -n "$TRANSITION_MANIFEST" ] && [ -z "$TRANSITION_CANDIDATE" ]; then
        refuse "--review-manifest without --reviewed-candidate"
    fi
    if [ -n "$TRANSITION_CANDIDATE" ] && [ -z "$TRANSITION_MANIFEST" ]; then
        refuse "--reviewed-candidate without --review-manifest"
    fi
    if [ -n "$TRANSITION_MANIFEST" ]; then
        require_regular_file "review manifest" "$TRANSITION_MANIFEST"
    fi
}

cmd_stage1() {
    take_values "$@"
    shift 13
    take_transition_options "$@"
    require_checker

    # THE SIGNING KEY MUST BE ONE THE ANCHORED ROSTER NAMES.
    #
    # Checked here, in the first second, because the alternative is what
    # happened on 2026-08-19: the ceremony ran a full stage 1, wrote a package,
    # loaded the key, signed, and only then refused with `status U` -- a
    # correct refusal arriving one stage and one authorization package too
    # late. The operator had no way to know until the most expensive step.
    #
    # This bites hardest during a KEY ROLLOVER, which is the one ceremony where
    # the obvious key is the wrong one: the transition must be signed by the
    # OLD anchored key, because the old roster is what verifies the commit that
    # installs the new one. Pointing `signing_key` at the shiny new key is the
    # natural mistake and this is where it gets caught.
    #
    # Compared as text -- `keytype keydata` from the .pub against the same two
    # fields of each roster line -- so no fingerprinting tool joins the trust
    # set for this check.
    _s1_keyfields=$("$V_cat" "$V_signing_key") || refuse "cannot read signing_key"
    _s1_keytype=${_s1_keyfields%% *}
    _s1_rest=${_s1_keyfields#* }
    _s1_keydata=${_s1_rest%% *}
    _s1_anchored=$("$V_env" -i HOME=/nonexistent GIT_NO_LAZY_FETCH=1 \
        "$V_git" --no-replace-objects -c core.useReplaceRefs=false \
                 -c core.hooksPath=/dev/null -c core.fsmonitor=false \
                 -C "$V_checkout" cat-file blob \
                 "refs/cairn/gate-anchor:dev/.cairn/allowed_signers" 2>/dev/null) \
        || refuse "cannot read the anchored roster; is refs/cairn/gate-anchor" \
                  "present? A fresh clone does not fetch it"
    _s1_found=''
    while IFS= read -r _s1_line || [ -n "$_s1_line" ]; do
        [ -n "$_s1_line" ] || continue
        case $_s1_line in '#'*) continue ;; esac
        _s1_r=${_s1_line#* }
        _s1_rtype=${_s1_r%% *}
        _s1_rrest=${_s1_r#* }
        _s1_rdata=${_s1_rrest%% *}
        if [ "$_s1_rtype" = "$_s1_keytype" ] && [ "$_s1_rdata" = "$_s1_keydata" ]; then
            _s1_found=yes
        fi
    done <<ROSTER
$_s1_anchored
ROSTER
    [ -n "$_s1_found" ] || refuse \
        "the signing key in your values file is NOT in the anchored roster," \
        "so stage 2 would build a checkpoint that cannot verify and refuse" \
        "AFTER the key is loaded. If this is a key ROLLOVER, point signing_key" \
        "at the OLD key: the old roster must verify the transition that" \
        "installs the new one. ($V_signing_key)"

    # The package is a handoff, not a scratch file. Refusing to overwrite is
    # what keeps stage 2 from confirming a digest over bytes some earlier run
    # left behind.
    if [ -e "$V_package" ]; then
        refuse "package: '$V_package' already exists. Stage 1 writes it and" \
               "must not overwrite: an existing file is either a run already" \
               "in progress or a stale one, and neither is safe to bless"
    fi

    # The stop-point, and it is a real one: everything that could refuse has
    # already refused, so what prints here is exactly what will run.
    print_effective_configuration

    set -- stage1 \
        --repo "$V_checkout" \
        --package-out "$V_package" \
        --signing-key "$V_signing_key"
    if [ -n "$TRANSITION_MANIFEST" ]; then
        set -- "$@" --transition-from-review "$TRANSITION_MANIFEST" \
                    --reviewed-candidate "$TRANSITION_CANDIDATE"
    fi

    printf '%s\n' "== stage 1: probing the key channel, then running the checks =="
    printf '%s\n' "   (this stage holds no key and must not be able to sign)"
    printf '%s\n' "   IF YOU ARE ASKED FOR A PASSPHRASE HERE: **DECLINE IT**."
    printf '%s\n' "   The prompt is this check working -- it is asking whether the"
    printf '%s\n' "   key is reachable, and typing it answers YES, which fails."
    printf '\n'

    # NO SSH_AUTH_SOCK. See the block comment above -- this is the control,
    # not an omission.
    "$V_env" -i \
        PATH=/usr/bin:/bin \
        HOME="$V_home" \
        "$V_python" -E -s "$CHECKER" "$@"
    _s1_status=$?

    # HAND THE OPERATOR THE NEXT COMMAND, exactly as it must be typed.
    #
    # Not a convenience. In transition mode stage 2 needs the review manifest
    # and the resolved candidate, and BOTH are things this run produced: the
    # manifest lives in a temporary directory the launcher created, and the
    # candidate is what the launcher resolved. An operator working from the
    # runbook alone would type the steady-state command and be refused, or --
    # worse -- go looking for a manifest to supply and hand-write one, which is
    # the exact act this whole design exists to remove.
    if [ "$_s1_status" -eq 0 ]; then
        _s1_via_launcher=''
        if [ -n "${CAIRN_LAUNCHER-}" ] && [ -n "${CAIRN_PACKET-}" ] \
           && [ -n "${CAIRN_VALUES-}" ]; then
            _s1_via_launcher=yes
        fi
        printf '\n%s\n' "== next: confirm, then sign =="
        printf '%s\n' "  1. read what you are authorizing:"
        if [ -n "$_s1_via_launcher" ]; then
            printf '%s\n' "       sh $CAIRN_LAUNCHER $CAIRN_PACKET $CAIRN_VALUES ${CAIRN_CANDIDATE-<candidate-ref>} --show-report"
        else
            printf '%s\n' "       re-run YOUR LAUNCHER with:  --show-report"
        fi
        printf '%s\n' "  2. compute the digest yourself:"
        if [ -n "$_s1_via_launcher" ]; then
            printf '%s\n' "       sh $CAIRN_LAUNCHER $CAIRN_PACKET $CAIRN_VALUES ${CAIRN_CANDIDATE-<candidate-ref>} --hash-package"
        else
            printf '%s\n' "       re-run YOUR LAUNCHER with:  --hash-package"
        fi
        printf '%s\n' "  3. check that no agent lists your key (ssh-add -l); do not load it"
        printf '%s\n' "  4. sign and move both refs (the signer asks for the passphrase):"
        # PRINT THE LAUNCHER COMMAND, NOT THIS ARTIFACT'S.
        #
        # Stage 2 must re-extract into a FRESH directory. Candidate code ran in
        # stage 1, as the same user, while this directory sat on disk -- so
        # telling the operator to run `$0 stage2` from here hands the signing
        # stage bytes the candidate had a window to rewrite. The launcher's
        # --stage2 path exists precisely to avoid that, and an earlier version
        # of this block printed the wrong one: the code had the property and
        # the instructions walked the operator around it.
        if [ -n "$_s1_via_launcher" ]; then
            printf '%s\n' "       sh $CAIRN_LAUNCHER \\"
            printf '%s\n' "         $CAIRN_PACKET \\"
            printf '%s\n' "         $CAIRN_VALUES \\"
            printf '%s\n' "         ${CAIRN_CANDIDATE-<candidate-ref>} \\"
            printf '%s\n' "         --stage2 <the digest from step 2>"
            printf '\n%s\n' "  Same launcher, same packet, same values -- plus"
            printf '%s\n'   "  --stage2. It verifies everything again into a new"
            printf '%s\n'   "  directory rather than trusting this one, and"
            printf '%s\n'   "  composes its own manifest, so you pass none."
        else
            printf '%s\n' "       re-run YOUR LAUNCHER with:  --stage2 <the digest from step 2>"
            printf '\n%s\n' "  Run the launcher, not this artifact: stage 2 must"
            printf '%s\n'   "  re-verify into a fresh directory rather than reuse"
            printf '%s\n'   "  the one candidate code just ran in."
        fi
    fi
    return "$_s1_status"
}

cmd_stage2() {
    take_values "$@"
    shift 13
    _s2_confirm=''
    _s2_rest_manifest=''
    _s2_rest_candidate=''
    while [ "$#" -gt 0 ]; do
        case $1 in
        --confirm-package-sha256)
            [ "$#" -ge 2 ] || refuse "--confirm-package-sha256 needs a value"
            _s2_confirm=$2
            shift 2 ;;
        --review-manifest)
            [ "$#" -ge 2 ] || refuse "--review-manifest needs a value"
            _s2_rest_manifest=$2
            shift 2 ;;
        --reviewed-candidate)
            [ "$#" -ge 2 ] || refuse "--reviewed-candidate needs a value"
            _s2_rest_candidate=$2
            shift 2 ;;
        *)
            refuse "unexpected argument '$1'" ;;
        esac
    done
    [ -n "$_s2_confirm" ] || refuse "stage2 requires --confirm-package-sha256." \
        "The digest is YOURS: compute it over the file with 'hash-package' and" \
        "compare it to what stage 1 printed. No digest inside the package can" \
        "satisfy this, because a package can carry its own digest"

    require_checker
    TRANSITION_MANIFEST=$_s2_rest_manifest
    TRANSITION_CANDIDATE=$_s2_rest_candidate
    take_transition_options

    require_regular_file "package" "$V_package"

    # SAY WHY THERE IS NO AGENT SOCKET, rather than letting it look like a fault.
    #
    # The key stays in no agent, so the stage is run with no socket and the
    # signer asks for the passphrase on the terminal. Without a terminal,
    # `git commit-tree` falls back to ssh-askpass and dies naming
    # `/usr/X11R6/bin/ssh-askpass` -- a path that does not exist on a stock
    # host and names nothing an operator can act on. Measured twice on
    # 2026-08-19, once per ceremony attempt.
    #
    # A note rather than a refusal: this stage's job is to sign, not to police
    # how the key is supplied.
    if [ -z "${SSH_AUTH_SOCK-}" ]; then
        printf '%s\n' "   NOTE: no agent socket, as intended: the key stays in no agent."
        printf '%s\n' "   If signing fails naming ssh-askpass, this stage had no terminal"
        printf '%s\n' "   to ask for the passphrase on; run it from a terminal."
        printf '\n'
    fi

    print_effective_configuration

    set -- stage2 \
        --repo "$V_checkout" \
        --package "$V_package" \
        --signing-key "$V_signing_key" \
        --confirm-package-sha256 "$_s2_confirm"
    if [ -n "$TRANSITION_MANIFEST" ]; then
        set -- "$@" --transition-from-review "$TRANSITION_MANIFEST" \
                    --reviewed-candidate "$TRANSITION_CANDIDATE"
    fi

    printf '%s\n' "== stage 2: confirm, sign, and move both refs in ONE transaction =="
    printf '%s\n' "   (the signer asks for the key's passphrase once, below)"
    printf '%s\n' "   IF YOU ARE ASKED FOR A PASSPHRASE HERE: **ENTER IT**."
    printf '%s\n' "   This is the opposite of stage 1. Same prompt, other stage,"
    printf '%s\n' "   other answer. Do not load the key into an agent."
    printf '\n'

    # SSH_AUTH_SOCK is forwarded here, and only here, when the caller has one.
    # See the block comment above.
    "$V_env" -i \
        PATH=/usr/bin:/bin \
        HOME="$V_home" \
        SSH_AUTH_SOCK="${SSH_AUTH_SOCK-}" \
        "$V_python" -E -s "$CHECKER" "$@"
}

# --------------------------------------------------------------------------
# the two steps that previously had no command at all
# --------------------------------------------------------------------------

cmd_hash_package() {
    [ "$#" -eq 13 ] || refuse "hash-package takes exactly the 13 recorded" \
                              "values and nothing else"
    take_values "$@"
    require_regular_file "package" "$V_package"

    # Over the BYTES ON DISK, with the recorded shasum. Never a digest read
    # out of the package: a file can carry any digest it likes about itself,
    # and confirming that one confirms nothing.
    printf '%s\n' "== the digest you confirm =="
    printf '%s\n' "   computed over the bytes at $V_package"
    printf '%s\n' "   compare it with what stage 1 printed, then pass it to"
    printf '%s\n' "   stage2 --confirm-package-sha256"
    printf '\n'
    "$V_shasum" -a 256 "$V_package"
}

cmd_show_report() {
    [ "$#" -eq 13 ] || refuse "show-report takes exactly the 13 recorded" \
                              "values and nothing else"
    take_values "$@"
    require_regular_file "package" "$V_package"

    # A confirmed digest over an unread report authorizes something you have
    # not seen. This is the command that makes the report readable -- the step
    # the runbook asked for and provided no way to perform.
    #
    # Rendered by the recorded interpreter rather than by shell string-cutting:
    # a JSON reader written in `sed` is a second parser of an authority
    # artifact, and the two would disagree eventually. The script below is part
    # of this reviewed artifact, exactly like the shell around it.
    # Nothing is printed until every field has been checked: a report with an
    # unprintable byte or a missing section is refused whole, never rendered
    # in part. The Python below holds no apostrophe, because it sits inside a
    # single-quoted shell string.
    "$V_python" -E -s -c '
import hashlib, json, sys

SCHEMA = "cairn-range-review/v2"
ROLES = ("decides", "pinned", "other")
TOOLS = ("env", "git", "python", "mktemp", "mkdir", "shasum", "sort", "cat")


def refuse(why):
    sys.stderr.write("REFUSE: " + why + chr(10))
    raise SystemExit(1)


def text(value, what):
    # Printable ASCII only. Every string in the report is meant to arrive
    # already escaped, so a byte outside this range is not text to show: it is
    # a report that could rewrite what the reader sees.
    if not isinstance(value, str):
        refuse("the report field " + what + " is not text")
    for ch in value:
        if not 0x20 <= ord(ch) < 0x7F:
            refuse("the report field " + what + " holds an unprintable"
                   " character; nothing was shown")
    return value


def need(container, key, kind, what):
    if not isinstance(container, dict) or not isinstance(container.get(key), kind):
        refuse("the report has no usable " + what)
    return container[key]


with open(sys.argv[1], "rb") as fh:
    raw = fh.read()
pkg = json.loads(raw)
package_digest = hashlib.sha256(raw).hexdigest()
tools = sys.argv[2:]
if len(tools) != len(TOOLS):
    refuse("show-report was not given the tool paths")

report = pkg.get("range_report")
if report is None:
    refuse("the package carries no range report")
if report.get("schema") != SCHEMA:
    refuse("this page reads " + SCHEMA + " and nothing else; the report says "
           + repr(report.get("schema")))

paths = need(report, "paths", list, "path list")
counts = need(report, "counts", dict, "class counts")
role_counts = need(report, "role_counts", dict, "role counts")
scan = need(report, "scan", dict, "line scan")
signers = need(report, "signers", dict, "signer list")
sig = report.get("signatures") or {}
hits = need(scan, "hits", list, "scan hits")
listed = need(scan, "listed", list, "scan list")
scanned = need(scan, "scanned", list, "scanned paths")
not_scanned = need(scan, "not_line_scanned", dict, "not-line-scanned counts")
scan_counts = need(scan, "counts", dict, "scan counts")
anchor_signers = need(signers, "anchor", list, "anchored signer list")
cand_signers = need(signers, "candidate", list, "candidate signer list")

out = []
add = out.append


def row(label, value, what):
    add("  %-16s %s" % (label, text(value, what)))


add("== what you are authorizing ==")
add("")
row("candidate id", report.get("candidate_head"), "candidate_head")
row("anchor", report.get("anchor"), "anchor")
row("branch", report.get("branch"), "branch")
row("expected old", report.get("expected_old"), "expected_old")
row("manifest sha256", report.get("manifest_sha256"), "manifest_sha256")
row("package sha256", package_digest, "package digest")
add("")

add("  allowed_signers fingerprints (compare yours with ssh-keygen -lf):")
for name, group in (("anchored", anchor_signers), ("candidate", cand_signers)):
    add("    " + name + " roster (" + str(len(group)) + "):")
    for line in group:
        add("      " + text(line, "signer"))
gone = [x for x in anchor_signers if x not in cand_signers]
came = [x for x in cand_signers if x not in anchor_signers]
if gone or came:
    add("    ROSTER CHANGED: a key signs later anchors only if it is listed here")
    for x in came:
        add("      added   " + text(x, "signer"))
    for x in gone:
        add("      removed " + text(x, "signer"))
else:
    add("    roster unchanged")
add("")

add("  tools this ceremony runs, from your values file (compare each with"
    " readlink -f of command -v):")
for tool, path in zip(TOOLS, tools):
    add("    %-8s %s" % (tool, text(path, "tool " + tool)))
add("")

add("  changed paths by class:")
for name in sorted(counts):
    add("    %-24s %d" % (text(name, "class"), counts[name]))
add("  changed paths by role:")
for name in ROLES:
    add("    %-24s %d" % (name, role_counts.get(name, 0)))
add("")

for role in ROLES:
    group = [e for e in paths if isinstance(e, dict) and e.get("role") == role]
    if not group:
        continue
    add("  %s (%d):" % (role, len(group)))
    for e in group:
        mode = e.get("mode") or "-"
        add("    %-8s %-6s %-16s %s" % (
            text(str(e.get("change")), "change"), text(str(mode), "mode"),
            text(str(e.get("class")), "class"), text(e.get("display"), "path")))
    add("")
if len(paths) != sum(role_counts.values()):
    refuse("the role counts do not add up to the path list")

add("  line scan: added lines in the paths that decide what runs, in the"
    " sensitive roster and in new files under scripts/ and bootstrap/")
add("    scanned paths: %d" % len(scanned))
for name in text(" ".join(map(str, scan.get("patterns", []))), "patterns").split():
    add("    %-14s %d hit(s)" % (name, scan_counts.get(name, 0)))
add("")
add("  every scan hit (%d), none cut:" % len(hits))
for h in hits:
    add("    %s:%s [%s] %s" % (text(h.get("path"), "hit path"), h.get("line"),
                               text(h.get("pattern"), "hit pattern"),
                               text(h.get("text"), "hit text")))
add("")
add("  listed, not line-scanned as text (%d):" % len(listed))
for x in listed:
    add("    %s  %s" % (text(x.get("path"), "listed path"),
                        text(x.get("reason"), "listed reason")))
for cls in sorted(not_scanned):
    add("  not line-scanned: %s, %d" % (text(cls, "class"), not_scanned[cls]))
add("")

canon = json.dumps(scan, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=True).encode("ascii")
add("  scan digest      " + hashlib.sha256(canon).hexdigest())
if report.get("scan_checker") == "anchor":
    add("  anchored scan    computed by the anchor own checker (equal by"
        " construction)")
else:
    add("  anchored scan    not computed here: a candidate checker made this"
        " scan. Run the anchored command and compare its digest with this one.")
add("")

if sig:
    add("  signatures over the range:")
    for k in sorted(sig):
        add("    %-24s %s" % (text(str(k), "signature key"), sig[k]))
    add("")

add("== your answers, yes or no ==")
add("  Y1  [yes/no]  The record says its author wrote nothing in this range.")
add("                (a statement; you cannot check it)")
add("  Y2  [yes/no]  The gate-file changes listed above are the ones the plan names.")
add("  Y3  [yes/no]  Every scan hit above has a one-line plain explanation in the record.")
add("  Y4  [yes/no]  Every scanner and the certifying run passed, or each failure")
add("                is named in an earlier allowance.")
add("  Y5  [yes/no]  This is your own machine and your signing key is not loaded.")
print(chr(10).join(out))
' "$V_package" "$V_env" "$V_git" "$V_python" "$V_mktemp" "$V_mkdir" "$V_shasum" "$V_sort" "$V_cat"
}

# --------------------------------------------------------------------------
# the procedure-step registry
# --------------------------------------------------------------------------
#
# A CLOSED, ORDERED registry of the ceremony's steps: stable ID, stage, the
# command that performs it, its inputs, and its security-relevant outcome.
#
# WHAT THIS DELIVERS, and what it does not. The runbook cites every ID exactly
# once and uses no unknown ID, and a test compares the two structures. That is a
# drift signal on the procedure's SHAPE -- a step added to the code and never
# documented, or documented and never implemented, fails. It attests NOTHING
# about whether the surrounding explanation is accurate. That prose is reviewed,
# not machine-checked, and this comment says so rather than letting the presence
# of a check imply more than the check does.
#
# The IDs are stable. Renumbering them silently rewrites every citation in the
# runbook, so a retired step keeps its ID and is marked retired.

print_steps() {
    printf '%s\n' '== the ceremony, step by step =='
    printf '\n'
    printf '%-8s %-13s %-14s %s\n' 'ID' 'STAGE' 'COMMAND' 'WHAT IT ESTABLISHES'
    printf '%s\n' '--------------------------------------------------------------------------'

    printf '%-8s %-13s %-14s %s\n' 'RA-01' 'pre-candidate' 'launcher' \
        'the values file parses under the closed schema; every executable the'
    printf '%-8s %-13s %-14s %s\n' '' '' '' \
        'launcher will run is a recorded, symlink-free, executable regular file'

    printf '%-8s %-13s %-14s %s\n' 'RA-02' 'pre-candidate' 'launcher' \
        'the packet on disk is the packet the builder bound into the launcher'
    printf '%-8s %-13s %-14s %s\n' 'RA-03' 'pre-candidate' 'launcher' \
        'the bytes parsed are the bytes hashed -- detects a lossy snapshot and a'
    printf '%-8s %-13s %-14s %s\n' '' '' '' \
        'same-user rewrite between the two reads (it detects; it does not prevent)'
    printf '%-8s %-13s %-14s %s\n' 'RA-04' 'pre-candidate' 'launcher' \
        'the packet names EXACTLY the authority closure fixed in the launcher'
    printf '%-8s %-13s %-14s %s\n' 'RA-05' 'pre-candidate' 'launcher' \
        'the ceremony artifact is a closure member by construction, not by'
    printf '%-8s %-13s %-14s %s\n' '' '' '' \
        'assertion: one row, matching digest, and the path the launcher starts'
    printf '%-8s %-13s %-14s %s\n' 'RA-06' 'pre-candidate' 'launcher' \
        'the candidate is resolved ONCE to a full object id'
    printf '%-8s %-13s %-14s %s\n' 'RA-07' 'pre-candidate' 'launcher' \
        'every closure blob at that id matches its reviewed digest'
    printf '%-8s %-13s %-14s %s\n' 'RA-08' 'pre-candidate' 'launcher' \
        'the extracted ceremony artifact matches its reviewed digest'
    printf '%-8s %-13s %-14s %s\n' 'RA-09' 'pre-candidate' 'launcher' \
        'the review manifest is COMPOSED from the packet and the resolution;'
    printf '%-8s %-13s %-14s %s\n' '' '' '' \
        'nothing in it is read from the candidate'

    printf '%-8s %-13s %-14s %s\n' 'RA-10' 'stage 1' 'stage1' \
        'THE FIRST CANDIDATE BYTE RUNS. Everything above ran on reviewed bytes'
    printf '%-8s %-13s %-14s %s\n' 'RA-11' 'stage 1' 'stage1' \
        'the complete effective configuration is shown while it is still free'
    printf '%-8s %-13s %-14s %s\n' '' '' '' \
        'to stop'
    printf '%-8s %-13s %-14s %s\n' 'RA-12' 'stage 1' 'stage1' \
        'the key channel is PROBED and the stage refuses if it can sign'
    printf '%-8s %-13s %-14s %s\n' 'RA-13' 'stage 1' 'stage1' \
        'the read-only checks pass and the authorization package is written.'
    printf '%-8s %-13s %-14s %s\n' '' '' '' \
        'No key is held and no ref moves'

    printf '%-8s %-13s %-14s %s\n' 'RA-14' 'between' 'show-report' \
        'what the digest binds is READ, not just confirmed'
    printf '%-8s %-13s %-14s %s\n' 'RA-15' 'between' 'hash-package' \
        'the digest is computed over the bytes on disk, by you'
    printf '%-8s %-13s %-14s %s\n' 'RA-16' 'between' '(Maintainer)' \
        'the key stays in no agent: you repeat the checks that bind what you sign'

    printf '%-8s %-13s %-14s %s\n' 'RA-17' 'stage 2' 'stage2' \
        'the confirmed package is validated against YOUR digest, re-extracted'
    printf '%-8s %-13s %-14s %s\n' '' '' '' \
        'and re-verified; no candidate code runs in this stage'
    printf '%-8s %-13s %-14s %s\n' 'RA-18' 'stage 2' 'stage2' \
        'the checkpoint is signed and branch and anchor move in ONE transaction'
    printf '%-8s %-13s %-14s %s\n' 'RA-19' 'after' '(Maintainer)' \
        'the two refs are published in one atomic push'
    printf '\n'
}

#: Just the IDs, one per line, in order. This is what the documentation-
#: agreement test consumes: it must read the registry rather than a retyped
#: list, or the test would be checking the runbook against itself.
print_step_ids() {
    print_steps | while IFS= read -r _psi_line; do
        case $_psi_line in
            RA-[0-9][0-9]*) printf '%s\n' "${_psi_line%% *}" ;;
        esac
    done
}

usage() {
    # NOT a heredoc into `cat`. `usage` runs before any value has been
    # checked, so the validated `cat` path does not exist yet -- and invoking
    # `cat` by bare name would reach for it through ambient PATH, which is the
    # unbound-executable gap this contract closes everywhere else. `printf` is
    # a shell builtin and reaches for nothing.
    printf '%s\n' \
        'usage: reanchor.sh <command> <the 13 recorded values> [options]' \
        '' \
        '  The launcher runs this and supplies the values, in the schema order' \
        '  of bootstrap/reanchor-values.example. Run it through the launcher:' \
        '  nothing has checked a copy you start by hand.' \
        '' \
        '  validate       refuse any value that is not a usable path, and' \
        '                 print the complete effective configuration' \
        '  stage1         probe the key channel, run the checks, write the' \
        '                 authorization package. Holds no key.' \
        '  show-report    render what the package authorizes, in bounded' \
        '                 human-readable form' \
        '  hash-package   the digest you confirm, over the bytes on disk' \
        '  stage2         confirm, sign, and move both refs in one' \
        '                 transaction. Needs --confirm-package-sha256.' \
        '  steps          the closed, ordered procedure-step registry' \
        '  step-ids       just the step IDs, in order' \
        '' \
        '  transition mode adds --review-manifest and --reviewed-candidate' \
        '  to stage1 and stage2; the launcher supplies both.' \
        '' \
        'The values file is documented in bootstrap/reanchor-values.example.'
}

main() {
    if [ "$#" -lt 1 ]; then
        usage >&2
        exit 2
    fi
    _main_cmd=$1
    shift

    case $_main_cmd in
    validate)
        if [ "$#" -ne 13 ]; then
            refuse "validate takes exactly the 13 recorded values and nothing" \
                   "else"
        fi
        take_values "$@"
        print_effective_configuration
        printf '%s\n' "OK: the values satisfy the closed schema."
        ;;
    stage1)
        cmd_stage1 "$@"
        ;;
    show-report)
        cmd_show_report "$@"
        ;;
    hash-package)
        cmd_hash_package "$@"
        ;;
    stage2)
        cmd_stage2 "$@"
        ;;
    steps)
        [ "$#" -eq 0 ] || refuse "steps takes no arguments"
        print_steps
        ;;
    step-ids)
        [ "$#" -eq 0 ] || refuse "step-ids takes no arguments"
        print_step_ids
        ;;
    -h|--help|help)
        usage
        ;;
    *)
        refuse "unknown command '$_main_cmd'"
        ;;
    esac
}

main "$@"
