#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Work-intent engine — CLI subsystem (intent-split phase A2).

The argparse command surface: claim / release / list / whoami / install-hook /
install-precommit / hooks-status / precommit-check / auto-release dispatch, plus
``main``. The top layer — imports downward from every other subsystem.
"""
from __future__ import annotations

import pathlib

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Optional

from .shared import INTENTS_LOG_PATH, _read_nul_delimited_paths, normalize_path
from .record_io import (
    DEFAULT_PRUNE_GRACE_DAYS,
    active_intents,
    conflict_check,
    prune_released_pairs,
    write_claim,
    write_release,
)
from .identity import (
    AGENT_ENV_VAR,
    _load_config,
    effective_harness_vars,
    resolve_agent_identity,
    resolve_session_token,
)
from .conflict import (
    _read_claim_ttl_hours,
    INVOKE_HINT,
    PRECOMMIT_SENTINEL_BEGIN,
    _format_conflict_warning,
    _precommit_check_impl,
    split_file_tokens,
)
from .hooks import (
    SENTINEL_BEGIN,
    _cmd_install_hook,
    _cmd_install_precommit,
    _hook_installed,
    _resolve_hooks_dir,
)


def _cmd_claim(args) -> int:
    """``intent claim`` -- append claim + emit conflict-warning."""
    log_path = (
        Path(args.log_path) if args.log_path is not None else INTENTS_LOG_PATH
    )
    agent = args.agent or resolve_agent_identity() or "unknown-agent"
    try:
        record = write_claim(
            agent=agent,
            files=split_file_tokens(args.files),
            action=args.action,
            stem=args.stem,
            log_path=log_path,
        )
    except ValueError as exc:
        sys.stderr.write(f"intent: {exc}\n")
        return 2
    overlap = [
        active for active in conflict_check(record.files, log_path=log_path)
        if active.get("id") != record.id
    ]
    if overlap:
        sys.stderr.write(_format_conflict_warning(record, overlap))
    else:
        sys.stderr.write(
            f"intent: claim recorded (id: {record.id}); no active overlaps "
            f"on your file set.\n"
        )
    sys.stdout.write(record.id + "\n")
    return 0


def _cmd_release(args) -> int:
    """``intent release`` -- append release record by id."""
    log_path = (
        Path(args.log_path) if args.log_path is not None else INTENTS_LOG_PATH
    )
    try:
        record = write_release(
            claim_id=args.id, commit=args.commit, log_path=log_path,
        )
    except ValueError as exc:
        sys.stderr.write(f"intent: {exc}\n")
        return 2
    sys.stderr.write(
        f"intent: release recorded (id: {record.id}"
        + (f", commit: {record.commit}" if record.commit else "")
        + ").\n"
    )
    return 0


#: The versioned machine contract for ``list --format json`` (Chunk F, B3
#: addition + B8).  **The schema string is the compatibility fence**: a consumer
#: reads this exact value or refuses, so widening the payload shape means bumping
#: the version rather than hoping every reader copes.  The derived lifecycle
#: board is the first consumer and refuses anything else outright.
LIST_JSON_SCHEMA = "cairn-intent-list/1"

#: The exact record fields the JSON form publishes, in a fixed order.  A closed,
#: enumerated projection rather than the raw log record: the log is append-only
#: and may carry fields a future version adds, and passing those through
#: unfiltered would make the "versioned" claim false the first time one appears.
_LIST_JSON_FIELDS = ("id", "agent", "ts", "action", "stem", "files")


def _cmd_list(args) -> int:
    """``intent list`` -- print active intents (optionally filtered).

    Two projections of **one** reduction: the long-standing human form, and
    ``--format json``, the versioned machine contract.  Both read the same
    ``active_intents`` / ``conflict_check`` result, so the JSON form cannot come
    to disagree with the human one about which claims are active -- and claim /
    release semantics, the conflict rules, the log schema, the hooks and module
    activation are all untouched by it (B8: this addition is *"solely to add the
    versioned JSON `list` output"*).

    The JSON form is deterministic and ASCII-safe: records sort by id, keys sort,
    and ``ensure_ascii=True`` means no raw non-ASCII byte reaches a consumer's
    terminal through this path.  An empty result is an empty ``claims`` list with
    the schema still present -- never the human "no active intents" sentence,
    which a machine reader would have to guess at.
    """
    log_path = (
        Path(args.log_path) if args.log_path is not None else INTENTS_LOG_PATH
    )
    if args.conflicts_with:
        actives = conflict_check(
            split_file_tokens(args.conflicts_with), log_path=log_path,
        )
    else:
        actives = active_intents(log_path=log_path)
    if getattr(args, "format", "text") == "json":
        return _emit_list_json(actives)
    if not actives:
        sys.stdout.write("intent: no active intents.\n")
        return 0
    for active in actives:
        sys.stdout.write(
            f"id={active.get('id')!r}\n"
            f"  agent={active.get('agent')!r}\n"
            f"  ts={active.get('ts')!r}\n"
            f"  files={active.get('files')!r}\n"
            f"  action={active.get('action')!r}\n"
        )
        if active.get("stem"):
            sys.stdout.write(f"  stem={active.get('stem')!r}\n")
    return 0


def _emit_list_json(actives) -> int:
    """Render the active set as the versioned ``cairn-intent-list/1`` payload.

    Every value is coerced to the type the schema promises -- text for the five
    scalar fields, a list of text for ``files`` -- because the log is a
    hand-appendable JSONL file and a reader that trusted its types would be
    trusting a file any editor can corrupt.  A record whose ``files`` is not a
    list contributes an empty list rather than a crash: the human form already
    tolerates that shape, and refusing here would make one malformed historical
    line hide every live claim.
    """
    claims = []
    for active in actives:
        files = active.get("files")
        claims.append({
            "id": str(active.get("id") or ""),
            "agent": str(active.get("agent") or ""),
            "ts": str(active.get("ts") or ""),
            "action": str(active.get("action") or ""),
            "stem": str(active.get("stem") or ""),
            "files": [str(entry) for entry in files]
            if isinstance(files, list) else [],
        })
    claims.sort(key=lambda claim: claim["id"])
    payload = {"schema": LIST_JSON_SCHEMA, "claims": claims}
    sys.stdout.write(
        json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    )
    return 0


def _cmd_prune(args) -> int:
    """Drop released claim/release PAIRS older than the grace window.

    The log is a coordination surface, not an archive.  This never deletes an
    unreleased claim (that is a bug signal -- a session died holding a lock) and
    never drops a line it could not parse; both are reported instead.

    Refuses while an **unreleased claim newer than the adopter's claim-TTL**
    exists, because a recent claim means a live session may still be appending to
    the file this command rewrites.  Not "while *any* claim is active": every
    unreleased claim is active by :func:`active_intents`, so that reading would
    refuse forever and make the never-released report unreachable.

    This command carries the liveness refusal but **not** the handoff owner
    marker or the concurrent-handoff lock.  The rewrite's quiet-window
    precondition -- the full handoff is the session-day's last act -- is an
    operating rule of the ``session-end`` path, so a hand-run prune during active
    sessions relies on the liveness refusal alone.  Prefer ``--dry-run`` there.
    """
    # CR3: single-source the liveness horizon.  `record_io` cannot import
    # `conflict` (conflict imports record_io -- the layering runs one way), so
    # the CLI, which imports both, resolves the ADOPTER-CONFIGURED
    # `claim_ttl_hours` and passes it in.  Without this, an adopter running a
    # 24h TTL would have prune treat a 5h claim as a dead appender while the
    # commit path still treated it as live.
    report = prune_released_pairs(
        older_than_days=args.older_than_days, dry_run=args.dry_run,
        live_within_hours=_read_claim_ttl_hours(pathlib.Path.cwd()),
    )
    if report["refused"]:
        sys.stdout.write(f"intent: prune refused -- {report['refused']}\n")
        return 0
    stale = report["stale_unreleased"]
    if stale:
        sys.stdout.write(
            f"intent: {len(stale)} claim(s) older than "
            f"{args.older_than_days}d were NEVER RELEASED -- reported, not "
            f"deleted (a session that died holding a lock):\n"
        )
        for entry in stale[:10]:
            files = entry.get("files") or []
            shown = ", ".join(files[:3]) + ("..." if len(files) > 3 else "")
            sys.stdout.write(
                f"  {entry['ts']}  {entry.get('agent')}  {shown}\n"
            )
    verb = "would prune" if report["dry_run"] else "pruned"
    sys.stdout.write(
        f"intent: {verb} {report['pruned_pairs']} released pair(s) "
        f"({report['pruned_lines']} line(s)); {report['kept_lines']} kept"
        + (f", {report['unparseable_kept']} unparseable preserved"
           if report["unparseable_kept"] else "")
        + "\n"
    )
    return 0


def _cmd_whoami(args) -> int:
    """``intent whoami`` -- print the resolved per-session agent identity.

    The default output is exactly the ``agent`` field stamped on every
    claim/release record in ``dev/intents.jsonl`` -- so it is the link
    anchor between the intent log and any other per-session surface.

    ``--session-token`` prints just the per-session token (the 8-hex
    ``sha256`` slice of the harness session id) -- the value a per-session
    surface outside the intent log reuses to link back to the same
    session.  Concretely, the reflections channel's filename
    ``<date>-<agent>-<session>.md`` sets ``<session>`` to this token, so
    its ``<agent>-<session>`` tail reconstructs this command's default
    output.  Exits non-zero with no stdout when no harness session id is
    exposed, signalling the caller to fall back to a random token.
    """
    if args.session_token:
        token = resolve_session_token()
        if token is None:
            sys.stderr.write(
                "intent whoami: no harness session id exposed -- no "
                "per-session token (fall back to a random token).\n"
            )
            return 1
        sys.stdout.write(token + "\n")
        return 0
    identity = resolve_agent_identity()
    if identity is None:
        sys.stderr.write(
            "intent whoami: agent identity unresolved (no $CAIRN_AGENT, "
            "harness session id, or config 'agent').\n"
        )
        return 1
    sys.stdout.write(identity + "\n")
    return 0


def _cmd_auto_release(args) -> int:
    """``intent _auto_release`` -- internal; called by the post-commit hook.

    Resolves identity (fail-soft), reads committed paths, and appends
    release records for the resolved agent's claims whose files
    intersect the commit.  Always exits 0 -- the commit has already
    landed; the hook must never be a nuisance.
    """
    log_path = (
        Path(args.log_path) if args.log_path is not None else INTENTS_LOG_PATH
    )
    try:
        # Read the log BEFORE resolving identity, so the unresolved-identity
        # warning below can be suppressed when there is provably nothing to
        # release.  A human committing from an ordinary terminal fails
        # resolution *by construction* -- the harness session vars exist only
        # inside an agent harness -- so warning them once per commit, and
        # once per replayed commit through a rebase, is exactly the nuisance
        # this command's contract forbids.  An absent log reads as []
        # (``read_log``), so a fresh adopter is silent here too.
        actives = active_intents(log_path=log_path)

        agent = resolve_agent_identity()
        if agent is None:
            # Retained for the case the warning was written for: live claims
            # that cannot be released because the holder cannot be named.
            if actives:
                sys.stderr.write(
                    "intent: agent identity not configured ($CAIRN_AGENT "
                    "unset, no harness session var, and ~/.cairn/agent.json "
                    "missing or unreadable); skipping auto-release for "
                    f"commit {(args.commit or '')[:8]}.\n"
                )
            return 0

        # Override-shadow warning: a global CAIRN_AGENT export shadows the
        # per-session derivation, collapsing concurrent same-tool sessions
        # to one identity and risking cross-release of another session's
        # claims.  Warn (don't block) when the override is set AND an
        # effective harness session var is also present.
        env_override = os.environ.get(AGENT_ENV_VAR)
        if env_override and env_override.strip():
            config = _load_config()
            shadowed = None
            for _tag, sv in effective_harness_vars(config):
                if os.environ.get(sv):
                    shadowed = sv
                    break
            if shadowed is not None:
                sys.stderr.write(
                    f"intent: WARNING -- {AGENT_ENV_VAR}="
                    f"{env_override.strip()!r} is shadowing the per-session "
                    f"identity that would derive from ${shadowed}. A global "
                    f"{AGENT_ENV_VAR} export collapses concurrent same-tool "
                    f"sessions to one identity and can cross-release other "
                    f"sessions' claims; unset it to use per-session "
                    f"derivation (it is an escape hatch, not a profile "
                    f"setting).\n"
                )

        if args.paths_from_file is None:
            sys.stderr.write(
                "intent: _auto_release called without --paths-from-file; "
                "nothing to release.\n"
            )
            return 0
        committed_paths = _read_nul_delimited_paths(args.paths_from_file)
        if not committed_paths:
            return 0

        committed_set = {normalize_path(p) for p in committed_paths}
        released_count = 0
        for active in actives:
            if active.get("agent") != agent:
                continue
            active_files = active.get("files") or []
            if not isinstance(active_files, list):
                continue
            active_set = {normalize_path(str(f)) for f in active_files}
            if active_set & committed_set:
                claim_id = active.get("id")
                if isinstance(claim_id, str):
                    try:
                        write_release(
                            claim_id=claim_id,
                            commit=args.commit,
                            log_path=log_path,
                        )
                        released_count += 1
                    except (OSError, ValueError) as inner:
                        sys.stderr.write(
                            f"intent: auto-release failed for claim "
                            f"{claim_id}: {inner}\n"
                        )
        if released_count > 0:
            sys.stderr.write(
                f"intent: auto-released {released_count} "
                f"{'claim' if released_count == 1 else 'claims'} on commit "
                f"{(args.commit or '')[:8]}.\n"
            )
    except Exception as exc:  # noqa: BLE001 -- never block commits
        sys.stderr.write(
            f"intent: _auto_release internal error (commit already landed; "
            f"ignoring): {exc}\n"
        )
    return 0


def _cmd_precommit_check(args) -> int:
    """``intent _precommit_check`` -- the pre-commit hook's worker.

    Emits classified warnings to stderr, then applies the configured enforce
    mode (#53): ``warn`` (exit 0), ``confirm`` (prompt; proceed on ack, else
    degrade to ``block`` with no TTY -- R2), ``block`` (exit non-zero; **the
    shipped default** -- foldback-drain Fold A) -- but a block only fires when a
    *different live session* holds a **fresh** (within-TTL) claim on a staged
    path **and** the committer has a per-session token. An unclaimed path still
    only warns; the bypass env var / solo mode always exempts. **Fail-open by
    construction:** any internal error returns 0 (the hook no longer carries
    ``|| true``, so a crash must not wedge commits)."""
    try:
        return _precommit_check_impl(args)
    except Exception as exc:  # noqa: BLE001 -- fail-open is the contract
        sys.stderr.write(
            f"intent: pre-commit check errored ({exc!r}); allowing the "
            "commit (fail-open).\n"
        )
        return 0


def _cmd_hooks_status(args) -> int:
    """``intent hooks-status`` -- report install state of BOTH the
    post-commit auto-release hook and the pre-commit work-intent check.

    Human-readable + parseable: each hook prints on its own line with a
    stable ``installed`` / ``not-installed`` token, so session-start (and
    any script) can point at one stable command."""
    hooks_dir = _resolve_hooks_dir()
    if hooks_dir is None:
        sys.stderr.write(
            "intent: not inside a git working tree; cannot report hook "
            "status.\n"
        )
        return 1
    post = _hook_installed(hooks_dir / "post-commit", SENTINEL_BEGIN)
    pre = _hook_installed(hooks_dir / "pre-commit", PRECOMMIT_SENTINEL_BEGIN)
    post_tok = "installed" if post else "not-installed"
    pre_tok = "installed" if pre else "not-installed"
    sys.stdout.write(
        "intent hooks-status:\n"
        f"  post-commit (auto-release): {post_tok}\n"
        f"  pre-commit (work-intent check): {pre_tok}\n"
    )
    if not post:
        sys.stdout.write(
            f"  -> install post-commit: {INVOKE_HINT} install-hook\n"
        )
    if not pre:
        sys.stdout.write(
            f"  -> install pre-commit:  {INVOKE_HINT} install-precommit\n"
        )
    return 0


def _build_parser():
    import argparse

    parser = argparse.ArgumentParser(
        prog=INVOKE_HINT,
        description=(
            "Work-intent helper: append-only JSONL substrate for pre-edit "
            "coordination signals. See the coordination-tiers module for "
            "the doctrine."
        ),
    )
    parser.add_argument(
        "--log-path",
        default=None,
        help=(
            "Override the active intent log path (default: "
            "dev/intents.jsonl in the repo root). Mainly for tests."
        ),
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_claim = sub.add_parser(
        "claim",
        help=(
            "Record a new claim. Runs an immediate conflict-check against "
            "active claims; warns to stderr on overlap. Prints the new "
            "claim id to stdout."
        ),
    )
    p_claim.add_argument(
        "--files", nargs="+", required=True,
        help=(
            "One or more files this claim covers. Space- or comma-separated "
            "(or a mix)."
        ),
    )
    p_claim.add_argument(
        "--action", required=True, help="Short verb-phrase naming the work.",
    )
    p_claim.add_argument(
        "--stem", default=None,
        help=(
            "Optional short topic key. Use when long --files lists + verbose "
            "--action would blow the 512-byte record cap."
        ),
    )
    p_claim.add_argument(
        "--agent", default=None,
        help=(
            "Override agent identity (default: $CAIRN_AGENT, a harness "
            "session id, ~/.cairn/agent.json, or 'unknown-agent')."
        ),
    )
    p_claim.set_defaults(func=_cmd_claim)

    p_release = sub.add_parser(
        "release", help="Record a release event for an existing claim.",
    )
    p_release.add_argument(
        "id", help="The claim id (as returned by `intent claim`).",
    )
    p_release.add_argument(
        "--commit", default=None,
        help=(
            "Optional short SHA of the releasing commit (populated by the "
            "post-commit hook; omit for manual release)."
        ),
    )
    p_release.set_defaults(func=_cmd_release)

    p_list = sub.add_parser(
        "list", help="Print active intents (claims without matching releases).",
    )
    p_list.add_argument(
        "--conflicts-with", nargs="+", default=None,
        help=(
            "Filter to active intents whose file sets intersect these paths. "
            "Space- or comma-separated (or a mix)."
        ),
    )
    p_list.add_argument(
        "--format", choices=("text", "json"), default="text",
        metavar="{text,json}",
        help=(
            f"'json' emits the versioned {LIST_JSON_SCHEMA} machine contract "
            "(deterministic, ASCII-safe); 'text' (default) is the unchanged "
            "human form."
        ),
    )
    p_list.set_defaults(func=_cmd_list)

    p_prune = sub.add_parser(
        "prune",
        help=(
            "Drop RELEASED claim/release pairs older than the grace window. "
            "Never deletes an unreleased claim or an unparseable line; "
            "refuses while any claim is active."
        ),
    )
    p_prune.add_argument(
        "--older-than-days", type=int, default=DEFAULT_PRUNE_GRACE_DAYS,
        help=f"Grace window in days (default: {DEFAULT_PRUNE_GRACE_DAYS}).",
    )
    p_prune.add_argument(
        "--dry-run", action="store_true",
        help="Report what would be pruned and write nothing.",
    )
    p_prune.set_defaults(func=_cmd_prune)

    p_whoami = sub.add_parser(
        "whoami",
        help=(
            "Print the resolved per-session agent identity (the intent "
            "log's `agent` field). --session-token prints just the "
            "per-session hash token, the value the reflections channel "
            "reuses as <session> so the two surfaces link."
        ),
    )
    p_whoami.add_argument(
        "--session-token", action="store_true",
        help=(
            "Print only the per-session token (8-hex sha256 of the harness "
            "session id), not the full <tool_tag>-<token> identity. Exits "
            "non-zero with no output when no harness session id is exposed."
        ),
    )
    p_whoami.set_defaults(func=_cmd_whoami)

    p_install = sub.add_parser(
        "install-hook",
        help=(
            "Install (or uninstall) the post-commit auto-release hook. "
            "Opt-in: the scaffold never runs this for you."
        ),
    )
    p_install.add_argument(
        "--uninstall", action="store_true",
        help="Remove the previously-installed sentinel block.",
    )
    p_install.add_argument(
        "--python", default=None,
        help=(
            "Interpreter to bake into the generated hook (default: "
            "$CAIRN_PYTHON or this run's interpreter). Never a bare 'python'."
        ),
    )
    p_install.set_defaults(func=_cmd_install_hook)

    p_install_pre = sub.add_parser(
        "install-precommit",
        help=(
            "Install (or uninstall) the opt-in pre-commit work-intent "
            "check (warn-by-default). The scaffold never runs this for you."
        ),
    )
    p_install_pre.add_argument(
        "--uninstall", action="store_true",
        help="Remove the previously-installed sentinel block.",
    )
    p_install_pre.add_argument(
        "--python", default=None,
        help=(
            "Interpreter to bake into the generated hook (default: "
            "$CAIRN_PYTHON or this run's interpreter). Never a bare 'python'."
        ),
    )
    p_install_pre.set_defaults(func=_cmd_install_precommit)

    p_status = sub.add_parser(
        "hooks-status",
        help=(
            "Report install state of BOTH the post-commit auto-release "
            "and the pre-commit work-intent-check hooks."
        ),
    )
    p_status.set_defaults(func=_cmd_hooks_status)

    p_precheck = sub.add_parser(
        "_precommit_check",
        help="Internal: called by the pre-commit work-intent-check hook.",
    )
    p_precheck.add_argument(
        "--paths-from-file", default=None,
        help="Path to a NUL-delimited file listing the staged paths.",
    )
    p_precheck.set_defaults(func=_cmd_precommit_check)

    p_auto = sub.add_parser(
        "_auto_release", help="Internal: called by the post-commit hook.",
    )
    p_auto.add_argument(
        "--commit", default=None, help="SHA of the just-landed commit.",
    )
    p_auto.add_argument(
        "--paths-from-file", default=None,
        help="Path to a NUL-delimited file listing the committed paths.",
    )
    p_auto.set_defaults(func=_cmd_auto_release)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
