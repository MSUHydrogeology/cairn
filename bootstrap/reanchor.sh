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
# bound into the launcher at review time. It never loads a key, and stage 1
# refuses if it finds it can sign.

LC_ALL=C
export LC_ALL

set -u

#: The exact schema token. An unknown version refuses rather than being
#: best-effort parsed: a values file written for a different contract is not a
#: values file with a problem, it is an unreviewed input.
SCHEMA_VERSION='cairn-ceremony-values/v1'

#: Grammar bounds, from the accepted contract. Byte-oriented, which is why
#: LC_ALL=C is set above -- under a UTF-8 locale `${#line}` counts characters
#: and the bound would silently be larger than it says.
MAX_LINE_BYTES=4096
MAX_FILE_BYTES=65536

refuse() {
    printf 'REFUSE: %s\n' "$*" >&2
    exit 1
}

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
# the values parser
# --------------------------------------------------------------------------
#
# PARSED, NEVER EXECUTED. The loop below uses shell builtins only: no `source`,
# no `eval`, no command substitution, and no expansion of any value it reads.
# Every read value reaches exactly one place -- a variable assignment from a
# quoted parameter -- and every dispatch is a literal `case` arm.
#
# The `case` IS the closed schema. There is no table lookup and no dynamic
# variable name, because both would need `eval`; the cost is one arm per key
# and the benefit is that an unknown key cannot reach anything but the `*`
# refusal.

dup_check() {
    if [ -n "$1" ]; then
        refuse "duplicate key '$2' at line $3; a values file states each" \
               "field once, so a second one is an unresolved disagreement"
    fi
}

parse_values() {
    _pv_file=$1

    require_absolute "values file" "$_pv_file"
    no_symlink_on_path "values file" "$_pv_file"
    if [ ! -f "$_pv_file" ]; then
        refuse "values file: '$_pv_file' is not an existing regular file"
    fi

    _pv_total=0
    _pv_lineno=0

    # `IFS=` and `-r` together are what make this verbatim: without them the
    # shell would strip surrounding whitespace and interpret backslashes, and a
    # path would silently stop being the path that was recorded.
    while IFS= read -r _pv_line || [ -n "$_pv_line" ]; do
        _pv_lineno=$((_pv_lineno + 1))
        _pv_len=${#_pv_line}
        _pv_total=$((_pv_total + _pv_len + 1))

        if [ "$_pv_len" -gt "$MAX_LINE_BYTES" ]; then
            refuse "line $_pv_lineno is $_pv_len bytes; the bound is" \
                   "$MAX_LINE_BYTES"
        fi
        if [ "$_pv_total" -gt "$MAX_FILE_BYTES" ]; then
            refuse "the values file exceeds $MAX_FILE_BYTES bytes"
        fi

        # Control characters refuse everywhere, which is also how LF endings
        # are enforced: a CRLF file carries a CR at the end of every line.
        case $_pv_line in
            *[[:cntrl:]]*)
                refuse "line $_pv_lineno contains a control character" ;;
        esac

        # Blank and comment first, so the leading-whitespace rule below reports
        # what it is actually about rather than firing on an indented comment
        # and sending the operator to look at the wrong rule.
        if [ -z "$_pv_line" ]; then
            continue
        fi
        case $_pv_line in
            '#'*) continue ;;
        esac

        case $_pv_line in
            ' '*)
                refuse "line $_pv_lineno begins with whitespace; a record" \
                       "starts at column 0 and a comment marker is only a" \
                       "comment at column 0" ;;
        esac
        case $_pv_line in
            *' ')
                refuse "line $_pv_lineno ends with whitespace. It is refused" \
                       "rather than trimmed: trimming would silently change" \
                       "a path" ;;
        esac
        case $_pv_line in
            *' '*) ;;
            *) refuse "line $_pv_lineno has a key and no value" ;;
        esac

        _pv_key=${_pv_line%% *}
        _pv_value=${_pv_line#* }

        case $_pv_key in
        schema)      dup_check "${V_schema+s}"      schema      "$_pv_lineno"; V_schema=$_pv_value ;;
        checkout)    dup_check "${V_checkout+s}"    checkout    "$_pv_lineno"; V_checkout=$_pv_value ;;
        signing_key) dup_check "${V_signing_key+s}" signing_key "$_pv_lineno"; V_signing_key=$_pv_value ;;
        package)     dup_check "${V_package+s}"     package     "$_pv_lineno"; V_package=$_pv_value ;;
        home)        dup_check "${V_home+s}"        home        "$_pv_lineno"; V_home=$_pv_value ;;
        env)         dup_check "${V_env+s}"         env         "$_pv_lineno"; V_env=$_pv_value ;;
        git)         dup_check "${V_git+s}"         git         "$_pv_lineno"; V_git=$_pv_value ;;
        python)      dup_check "${V_python+s}"      python      "$_pv_lineno"; V_python=$_pv_value ;;
        mktemp)      dup_check "${V_mktemp+s}"      mktemp      "$_pv_lineno"; V_mktemp=$_pv_value ;;
        mkdir)       dup_check "${V_mkdir+s}"       mkdir       "$_pv_lineno"; V_mkdir=$_pv_value ;;
        shasum)      dup_check "${V_shasum+s}"      shasum      "$_pv_lineno"; V_shasum=$_pv_value ;;
        sort)        dup_check "${V_sort+s}"        sort        "$_pv_lineno"; V_sort=$_pv_value ;;
        cat)         dup_check "${V_cat+s}"         cat         "$_pv_lineno"; V_cat=$_pv_value ;;
        *)
            refuse "unknown key '$_pv_key' at line $_pv_lineno. The schema is" \
                   "closed: an unrecognised key is not an extra setting, it" \
                   "is a values file this contract did not review" ;;
        esac
    done < "$_pv_file"

    # NO AMBIENT FALLBACK. An absent field refuses here. It is never filled
    # from PATH, HOME, Git config or any other ambient source -- ambient
    # discovery is what let a substituted repository answer for the named one,
    # and a replacement utility vouch for bytes it had just rewritten.
    [ -n "${V_schema+s}" ]      || refuse "missing required key 'schema'"
    [ -n "${V_checkout+s}" ]    || refuse "missing required key 'checkout'"
    [ -n "${V_signing_key+s}" ] || refuse "missing required key 'signing_key'"
    [ -n "${V_package+s}" ]     || refuse "missing required key 'package'"
    [ -n "${V_home+s}" ]        || refuse "missing required key 'home'"
    [ -n "${V_env+s}" ]         || refuse "missing required key 'env'"
    [ -n "${V_git+s}" ]         || refuse "missing required key 'git'"
    [ -n "${V_python+s}" ]      || refuse "missing required key 'python'"
    [ -n "${V_mktemp+s}" ]      || refuse "missing required key 'mktemp'"
    [ -n "${V_mkdir+s}" ]       || refuse "missing required key 'mkdir'"
    [ -n "${V_shasum+s}" ]      || refuse "missing required key 'shasum'"
    [ -n "${V_sort+s}" ]        || refuse "missing required key 'sort'"
    [ -n "${V_cat+s}" ]         || refuse "missing required key 'cat'"

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

#: Printed on EVERY path that reads the values file, not only on `validate`.
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
    printf '%s\n' "  (read from $1 -- nothing below was discovered)"
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

usage() {
    # NOT a heredoc into `cat`. `usage` runs before any values file has been
    # parsed, so the validated `cat` path does not exist yet -- and invoking
    # `cat` by bare name would reach for it through ambient PATH, which is the
    # unbound-executable gap this contract closes everywhere else. `printf` is
    # a shell builtin and reaches for nothing.
    printf '%s\n' \
        'usage: reanchor.sh <command> <values-file>' \
        '' \
        '  validate   parse the values file, refuse on any violation, and' \
        '             print the complete effective configuration' \
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
        if [ "$#" -ne 1 ]; then
            refuse "validate takes exactly one argument: the values file"
        fi
        parse_values "$1"
        print_effective_configuration "$1"
        printf '%s\n' "OK: the values file satisfies the closed schema."
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
