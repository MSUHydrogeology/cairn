#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Local security-verification dispatcher -- the default-on evidence router.

Runs **no check itself**. It reads which security capabilities the adopter
has installed, looks each up in a **source-owned registry** (module-level
``_REGISTRY`` below -- no adopter file can add, steer, or widen an entry),
runs that capability's own ``local`` runner as a child process under a
hardened, minimal-environment, bounded invocation, validates what comes
back against the registry entry's own declared schema, and prints one
aggregate verdict. Standard library only; ships verbatim (byte-for-byte,
hash-pinned by the install lockfile) to an adopter's ``scripts/`` directory,
so it never imports Cairn's own ``bootstrap/`` engine tooling -- an adopter
tree never has one.

Deliberately NOT representable, by construction rather than by runtime
refusal: a ``deployed``, ``credentialed``, ``active``, or otherwise unknown
evidence mode. ``evidence_mode`` is a closed two-member set
(``{"offline", "loopback"}``); the CLI's own ``mode`` argument accepts only
``"local"``.

Exit ladder (reused from
``templates/modules/team-gated/run_security_audit.py``'s precedent,
precedence ``DEGRADED > FINDINGS > INCOMPLETE > CLEAN``, plus a fifth,
distinct state):

* ``0``  CLEAN -- every selected capability's local leg is admitted and
  reports no finding.
* ``5``  INCOMPLETE -- a selected capability has no admitted local registry
  entry (unsupported at this Cairn version), or a leg's own contract reports
  incomplete coverage.
* ``10`` FINDINGS -- an admitted leg reports a finding.
* ``20`` DEGRADED -- a binding check failed (missing/mismatched digest,
  symlinked runner or policy, unrecognized lockfile-record key, missing
  lockfile record), or a child could not be trusted to have run cleanly
  (timeout, output over the byte cap, invalid UTF-8/JSON, a result whose
  identifying fields disagree with the registry entry, an exit code that
  disagrees with its declared result).
* ``NOT_APPLICABLE`` (exit ``0``, a *distinct* state from CLEAN) -- no
  installed capability has an admitted local registry entry. It means "no
  security evidence was gathered", never "nothing is wrong", and the human
  and machine output are both contractually forbidden from using words that
  claim coverage (``CLEAN``, ``secure``, ``passed security``, ``verified``,
  ``no vulnerabilities``).

Command separation is not actor authentication (recorded in full in this
module's shipped doctrine, ``security-verification.md``, and in
``bootstrap/SAFETY.md``): a shell process cannot prove who invoked it, and an
agent with the operator's terminal and credentials could run any script
directly. This dispatcher's authority is strictly narrowing -- it can only
ever refuse or downgrade, never grant a capability an adopter file did not
already select and Cairn's own registry did not already admit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent
_LOCKFILE_REL = "dev/.cairn/cairn-lock.yml"
_LOCKFILE = _REPO_ROOT / _LOCKFILE_REL

# ---------------------------------------------------------------------------
# Aggregate exit ladder
# ---------------------------------------------------------------------------
CLEAN = 0
INCOMPLETE = 5
FINDINGS = 10
DEGRADED = 20
_AGGREGATE_LABELS: dict[int, str] = {
    CLEAN: "CLEAN", INCOMPLETE: "INCOMPLETE",
    FINDINGS: "FINDINGS", DEGRADED: "DEGRADED",
}
_AGGREGATE_EXIT: dict[str, int] = {v: k for k, v in _AGGREGATE_LABELS.items()}

_SCHEMA = "cairn.security_verification.dispatcher/v1"

#: Words a NOT_APPLICABLE (or any no-coverage) rendering must never contain
#: (T21): the absence of evidence must never read as a passing check.
_FORBIDDEN_COVERAGE_WORDS = (
    "CLEAN", "secure", "passed security", "no vulnerabilities", "verified",
)

# ---------------------------------------------------------------------------
# The binding-mode / evidence-mode closed vocabularies
# ---------------------------------------------------------------------------
_EVIDENCE_MODES: frozenset[str] = frozenset({"offline", "loopback"})
#: Deliberately ONE member: a future "living runner" cannot appear by
#: omission, only by a source edit widening this frozenset -- which is a
#: registry-schema change and therefore its own Security Review.
_RUNNER_BINDING_MODES: frozenset[str] = frozenset({"immutable_digest"})
_POLICY_BINDING_MODES: frozenset[str] = frozenset(
    {"none", "immutable_digest", "living_state"})

#: The admitted child-process argv vector(s) (api-web-security-modules /
#: a THIRD closed set alongside the two apparatus
#: bindings above, not a member of them. Deliberately ONE member: the
#: two api-web-security-modules facades' `local` subcommand takes the
#: dispatcher's bounded `--child-document` flag, and that is the only
#: admitted invocation shape. This is what makes a `deployed-passive` (or
#: any other) argv structurally unreachable from this dispatcher -- refused
#: here, at registry construction, never at the child process. Widening
#: this frozenset is a registry-schema change and carries its own Security
#: Review, exactly as widening `_RUNNER_BINDING_MODES` would.
_ARGV_MODES: frozenset[tuple[str, ...]] = frozenset({
    ("local", "--child-document"),
})

#: The lockfile-record keys this dispatcher recognizes for a runner or policy
#: destination it binds (shared contract with ``api-web-security-modules``
#: / ``security-verification-activation``). ``{src, dst, verbatim, hash}`` are
#: the install-time required fields; ``living_state`` / ``base_cache`` /
#: ``base_hash`` are the optional ones ``write_install_lockfile`` may add.
#: Any OTHER key on a record this dispatcher reads is refused -- DEGRADED,
#: naming the key -- never ignored. Recorded gap, not closed here:
#: ``bootstrap/verify_integrity.py:63-111`` reads the same record shape with
#: ``rec.get(...)`` and ignores an unrecognized key; that half is a
#: lasting truth neither plan in this pair closes (see this module's shipped
#: doctrine).
_ALLOWED_RECORD_KEYS: frozenset[str] = frozenset({
    "src", "dst", "verbatim", "hash", "living_state", "base_cache",
    "base_hash",
})

#: THIS dispatcher's own authoritative living-state destination set --
#: distinct from ``bootstrap/_scaffold/lockfile.py``'s ``_LIVING_STATE_DSTS``
#: (an engine-only constant this shipped, adopter-tree file cannot import; an
#: adopter checkout never has a ``bootstrap/`` directory). Carries exactly the
#: two policy destinations of the two ``policy_binding_mode: living_state``
#: entries admitted below,
#: added in the SAME commit as those registry entries, per this constant's
#: own standing rule: a future capability plan that earns living-state status
#: adds its policy destination here in the SAME commit that adds its
#: registry entry -- never before, never separately. The Maintainer ratified
#: the living-state narrowing before either landed; the policy row
#: (``701be3a``) added these same two destinations to the DIFFERENT,
#: engine-side ``_LIVING_STATE_DSTS`` in ``bootstrap/_scaffold/lockfile.py``
#: (what makes the install lockfile mark them ``living_state: true`` in the
#: first place) -- that landing does not, by itself, populate this
#: dispatcher's own set; each is a separate source edit, and this one is
#: this commit's.
_LIVING_STATE_DSTS: frozenset[str] = frozenset({
    "dev/.cairn/api-access-policy.json",
    "dev/.cairn/web-hosting-policy.json",
})

#: The CLOSED allowlist of environment variables a dispatched child inherits.
#: Mirrors ``templates/modules/team-gated/run_security_audit.py``'s
#: ``_ENV_ALLOWLIST`` rationale verbatim: a denylist cannot have the
#: completeness property under test -- only named variables ever reach a
#: child, no matter what a future proxy or credential variable is called.
_CHILD_ENV_ALLOWLIST: frozenset[str] = frozenset({
    "PATH", "HOME", "LANG",
    "TMPDIR", "TEMP", "TMP",
    # Windows minimum for an interpreter to start at all.
    "SYSTEMROOT", "SystemRoot", "COMSPEC", "PATHEXT", "USERPROFILE",
    "APPDATA", "LOCALAPPDATA", "NUMBER_OF_PROCESSORS",
    "PROCESSOR_ARCHITECTURE",
})
#: Name prefixes the allowlist also admits (locale only) -- the CPython
#: runtime itself may inject an ``LC_CTYPE`` into a child's own environment
#: under PEP 538 legacy-C-locale coercion, independent of anything this
#: dispatcher passes; excluding it would not stop it from appearing and
#: would only make this constant lie about what a child actually receives.
_CHILD_ENV_ALLOWLIST_PREFIXES: tuple[str, ...] = ("LC_",)

_CHILD_TIMEOUT_S = 60.0
_CHILD_OUTPUT_CAP_BYTES = 65536  # 64 KiB -- a JSON evidence report is small.
_CHILD_POLL_S = 0.02

#: Control characters kept verbatim when rendering a leg's ``detail`` text
#: (T11): TAB, LF. Everything else in C0/DEL/C1 is rendered as ``\xNN``, so a
#: crafted child ``details`` string cannot forge a terminal control sequence
#: (cursor moves, line erasure, OSC-8 hyperlinks) into the operator's
#: terminal. This sanitizes control characters only; it never truncates,
#: rewrites, or re-encodes the text, and it is the ONLY channel a child's
#: text ever reaches the report through -- raw stdout/stderr bytes are never
#: relayed, at any aggregate level (T12).
_CONTROL_KEEP = frozenset((0x09, 0x0A))

#: The child result JSON's exact, closed key set (T13's "unknown extra key"
#: row + the missing-key row, checked as a single set-equality assertion).
_REQUIRED_CHILD_KEYS = frozenset(
    {"schema", "capability", "contract", "evidence_mode", "result",
     "details"})


def _build_child_env() -> dict[str, str]:
    return {
        k: v for k, v in os.environ.items()
        if k in _CHILD_ENV_ALLOWLIST or k.startswith(_CHILD_ENV_ALLOWLIST_PREFIXES)
    }


def _safe_render(text: str) -> str:
    """Neutralize C0 (except TAB/LF) / DEL / C1 control characters in text
    that reaches the operator's terminal or the JSON report (T11)."""
    out: list[str] = []
    for ch in text:
        cp = ord(ch)
        if cp in _CONTROL_KEEP:
            out.append(ch)
        elif cp < 0x20 or cp == 0x7F or 0x80 <= cp <= 0x9F:
            out.append(f"\\x{cp:02x}")
        else:
            out.append(ch)
    return "".join(out)


# ---------------------------------------------------------------------------
# The registry entry -- a source-owned, closed-vocabulary, frozen record
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RegistryEntry:
    """One admitted local security-verification leg.

    Eleven fields, apparatus-level only: no ``principal``, no ``scope``
    -- those are child-policy semantics with no apparatus field, by decision.
    Every field is REQUIRED and has NO default (a defaulted binding mode is
    the *silently changed mode* failure a required field forecloses); the
    dataclass-generated ``__init__`` refuses a missing field and NAMES it
    (``TypeError: __init__() missing ... argument: '<field>'``) and refuses
    an unrecognized keyword and NAMES it too (``unexpected keyword argument
    '<name>'``) -- both are the constructor's own closed-vocabulary behavior
    rather than custom code layered on top. ``frozen=True`` additionally
    makes any post-construction assignment raise (T40) -- mode-immutability
    at the object level.
    """

    module_id: str
    runner_repository_path: str
    argv_mode: tuple[str, ...]
    policy_repository_path: str | None
    child_schema_version: str
    capability_contract_version: str
    evidence_mode: str
    accepted_process_exits: frozenset[int]
    result_to_aggregate_mapping: "dict[str, tuple[int, int]]"
    runner_binding_mode: str
    policy_binding_mode: str

    def __post_init__(self) -> None:
        if self.argv_mode not in _ARGV_MODES:
            raise ValueError(
                f"argv_mode {self.argv_mode!r} is not one of "
                f"{sorted(_ARGV_MODES)}")
        if self.evidence_mode not in _EVIDENCE_MODES:
            raise ValueError(
                f"evidence_mode {self.evidence_mode!r} is not one of "
                f"{sorted(_EVIDENCE_MODES)}")
        if self.runner_binding_mode not in _RUNNER_BINDING_MODES:
            raise ValueError(
                f"runner_binding_mode {self.runner_binding_mode!r} is not "
                f"one of {sorted(_RUNNER_BINDING_MODES)}")
        if self.policy_binding_mode not in _POLICY_BINDING_MODES:
            raise ValueError(
                f"policy_binding_mode {self.policy_binding_mode!r} is not "
                f"one of {sorted(_POLICY_BINDING_MODES)}")
        wants_path = self.policy_binding_mode != "none"
        has_path = self.policy_repository_path is not None
        if wants_path != has_path:
            raise ValueError(
                f"policy_binding_mode {self.policy_binding_mode!r} and "
                f"policy_repository_path {self.policy_repository_path!r} "
                "disagree: policy_binding_mode == 'none' iff "
                "policy_repository_path is None")


# ---------------------------------------------------------------------------
# HIGH-RISK SECURITY-REVIEW SURFACE -- verbatim, hash-pinned by the install
# lockfile (channel 3 of the three-channel designation carried by this
# module's shipped doctrine, ``security-verification.md``: channel 1 is the
# customizable ``AGENTS.md`` slot, channel 2 is ``dev/modules/security-
# verification.md``). This registry, this file's binding-mode schema
# (``RegistryEntry`` above), the child result schema this file validates, and
# EVERY entry added below are a high-risk Security-Review surface -- an entry
# cannot be added here without this comment (and the review it names) moving
# with it.
#
# The registry was EMPTY at activation v1 (Decision, api-web-security-modules
# / security-verification-activation, 2026-08-03): a dormant entry for an
# unaccepted or uninstalled capability is not permitted. Admission requires
# an accepted capability proposal, a reviewed plan with execution evidence
# for the exact evidence mode, a complete lockfile mapping group, schema and
# precedence tests, a Security Review of the registry change, and -- for a
# ``living_state`` policy binding -- execution evidence for the compensating
# controls that replace the digest (additionally gated on Maintainer
# ratification of the living-state narrowing). No entry met that bar until
# now.
#
# Two entries admitted:
# ``api-access-security`` and ``web-hosting-security``, the two capabilities
# this plan pair ships. Both clear every gate above: the accepted proposal,
# this reviewed plan (with both declared review rounds landed), the complete
# lockfile mapping group (Chunk F), this module's own schema and precedence
# tests (below), the Security Review of this registry change, and -- because
# both declare ``policy_binding_mode: living_state`` -- the Maintainer's
# ratification of the living-state narrowing plus execution evidence for
# its compensating controls (``_LIVING_STATE_DSTS`` above carries both policy
# destinations, added in this SAME commit). No other entry meets the bar; the
# registry admits exactly these two.
# ---------------------------------------------------------------------------
_REGISTRY: dict[str, RegistryEntry] = {
    "api-access-security": RegistryEntry(
        module_id="api-access-security",
        runner_repository_path="scripts/api_access_security.py",
        argv_mode=("local", "--child-document"),
        policy_repository_path="dev/.cairn/api-access-policy.json",
        child_schema_version="cairn.security.capability-result.v1",
        capability_contract_version="1",
        evidence_mode="loopback",
        accepted_process_exits=frozenset({0, 5, 10, 20}),
        result_to_aggregate_mapping={
            "CLEAN": (0, CLEAN),
            "INCOMPLETE": (5, INCOMPLETE),
            "FINDINGS": (10, FINDINGS),
            "DEGRADED": (20, DEGRADED),
        },
        runner_binding_mode="immutable_digest",
        policy_binding_mode="living_state",
    ),
    "web-hosting-security": RegistryEntry(
        module_id="web-hosting-security",
        runner_repository_path="scripts/web_hosting_security.py",
        argv_mode=("local", "--child-document"),
        policy_repository_path="dev/.cairn/web-hosting-policy.json",
        child_schema_version="cairn.security.capability-result.v1",
        capability_contract_version="1",
        evidence_mode="loopback",
        accepted_process_exits=frozenset({0, 5, 10, 20}),
        result_to_aggregate_mapping={
            "CLEAN": (0, CLEAN),
            "INCOMPLETE": (5, INCOMPLETE),
            "FINDINGS": (10, FINDINGS),
            "DEGRADED": (20, DEGRADED),
        },
        runner_binding_mode="immutable_digest",
        policy_binding_mode="living_state",
    ),
}


# ---------------------------------------------------------------------------
# Lockfile (read-only, stdlib JSON -- the lockfile is JSON-encoded YAML;
# ships as an adopter-tree file with no bootstrap/ engine to import, so this
# is a standalone re-implementation of ``read_lockfile``'s comment-stripping
# parse, not an import of it).
# ---------------------------------------------------------------------------

def _load_lockfile(path: Path | None = None) -> dict[str, Any] | None:
    """Parse the install lockfile. ``None`` on any missing/unparseable
    condition or non-object body; callers fail closed on ``None``.

    ``path`` defaults to the CURRENT module-level ``_LOCKFILE`` at CALL time
    (looked up in the function body, not bound as a parameter default) so a
    test can monkeypatch ``_LOCKFILE`` and have ``main()`` observe it --a
    parameter default is bound once at import time and would silently ignore
    a later monkeypatch."""
    if path is None:
        path = _LOCKFILE
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    body = "\n".join(
        ln for ln in text.splitlines() if not ln.lstrip().startswith("#")
    )
    try:
        data = json.loads(body)
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


#: The declared, source-owned set of module IDs this dispatcher treats as a
#: security capability (api-web-security-modules / Chunk G, replacing the
#: prior ``-security`` NAME-SUFFIX heuristic, which was wrong in both
#: directions: ``content-security`` is default-on, matches the suffix, has
#: no admitted registry entry, and made a stock install exit 5 INCOMPLETE
#: with nothing wrong -- measured, not hypothetical, at
#: ``bootstrap/_scaffold/config.py``'s prior ``_DEFAULT_ON_MODULES`` comment
#: and ``test_security_verification.py``'s prior T33 characterization; and a
#: capability named without the suffix would have been missed entirely.
#:
#: Deliberately kept SEPARATE from `_REGISTRY` -- never narrow this set to
#: `installed & set(_REGISTRY)`. The fail-closed signal this dispatcher must
#: preserve is: a module that is DECLARED here, IS installed, but has NO
#: admitted `_REGISTRY` entry (an unsupported capability at this Cairn
#: version) is still SELECTED and still reports INCOMPLETE.
#: Filtering on registry membership instead would make that exact case
#: silently invisible -- no leg, no INCOMPLETE, nothing -- which is the
#: property this set exists to protect. Do not "simplify" this to a registry
#: intersection.
_DECLARED_CAPABILITY_MODULES: frozenset[str] = frozenset({
    "api-access-security", "web-hosting-security",
})


def _selected_capability_ids(lock: dict[str, Any]) -> list[str]:
    """The installed-module roster, narrowed to `_DECLARED_CAPABILITY_MODULES`
    -- this dispatcher's declared security-capability set, not a name-suffix
    guess and not `_REGISTRY` membership (see that constant's own comment).
    Sorted for a deterministic evaluation order."""
    modules = lock.get("modules") or []
    installed = {m for m in modules if isinstance(m, str)}
    return sorted(installed & _DECLARED_CAPABILITY_MODULES)


def _records_by_dst(lock: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for rec in lock.get("files") or []:
        if isinstance(rec, dict) and isinstance(rec.get("dst"), str):
            out[rec["dst"]] = rec
    return out


# ---------------------------------------------------------------------------
# Parent-computed binding (T16-T19, T36-T39): the parent verifies the
# runner's and (per mode) the policy's on-disk state against the lockfile
# and computes every digest itself -- it never reads a digest, a runner path,
# or an argv/env value from anything a child says or from any adopter file
# outside the registry entry.
# ---------------------------------------------------------------------------

class _Degraded(Exception):
    """A binding check failed closed. ``reason`` is operator-facing text
    authored by this module -- never a raw child byte."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def _sha256_of(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _record_keys_ok(rec: dict[str, Any]) -> str | None:
    unknown = sorted(set(rec) - _ALLOWED_RECORD_KEYS)
    if unknown:
        return f"unrecognized lockfile-record key(s): {', '.join(unknown)}"
    return None


def _is_regular_and_unsymlinked(path: Path, root: Path) -> bool:
    """True iff every path component from ``root`` down to and including
    ``path`` is a real (non-symlink) entry and ``path`` is a regular file.
    Refuses BOTH a symlinked leaf and a symlinked parent directory (T18); the
    third T18 row -- a same-user race between this check and the later
    read/launch -- is a named, accepted residual (this module's doctrine),
    not something this check (or any check performed once, before use) can
    close."""
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    cur = root
    for part in rel.parts:
        cur = cur / part
        if cur.is_symlink():
            return False
    return path.is_file()


def _bind_runner(entry: RegistryEntry, records: dict[str, Any],
                  repo_root: Path) -> Path:
    rec = records.get(entry.runner_repository_path)
    if rec is None:
        raise _Degraded(
            f"no lockfile record for runner "
            f"{entry.runner_repository_path!r}")
    bad = _record_keys_ok(rec)
    if bad:
        raise _Degraded(
            f"runner record for {entry.runner_repository_path!r}: {bad}")
    path = repo_root / entry.runner_repository_path
    if not _is_regular_and_unsymlinked(path, repo_root):
        raise _Degraded(
            f"runner {entry.runner_repository_path!r} is missing, not a "
            "regular file, or reached through a symlink (tamper)")
    if rec.get("living_state"):
        raise _Degraded(
            f"runner {entry.runner_repository_path!r} record declares "
            "living_state; runner_binding_mode is immutable_digest-only")
    digest = _sha256_of(path)
    if digest != rec.get("hash"):
        raise _Degraded(
            f"runner {entry.runner_repository_path!r} digest mismatch "
            "(tamper / drift)")
    return path


def _bind_policy(entry: RegistryEntry, records: dict[str, Any],
                  repo_root: Path) -> dict[str, Any] | None:
    if entry.policy_binding_mode == "none":
        return None
    path_rel = entry.policy_repository_path
    if path_rel is None:
        # Unreachable given __post_init__'s agreement rule (policy_binding_
        # mode != "none" iff policy_repository_path is not None); guarded
        # explicitly rather than with `assert` (stripped under -O) so this
        # stays a real refusal in every build.
        raise _Degraded(
            "policy_binding_mode is not 'none' but policy_repository_path "
            "is None (unreachable via RegistryEntry's own construction "
            "rule; refusing rather than trusting it)")
    rec = records.get(path_rel)
    if rec is None:
        raise _Degraded(f"no lockfile record for policy {path_rel!r}")
    bad = _record_keys_ok(rec)
    if bad:
        raise _Degraded(f"policy record for {path_rel!r}: {bad}")
    path = repo_root / path_rel
    if not _is_regular_and_unsymlinked(path, repo_root):
        raise _Degraded(
            f"policy {path_rel!r} is missing, not a regular file, or "
            "reached through a symlink (tamper)")
    if entry.policy_binding_mode == "immutable_digest":
        if rec.get("living_state"):
            raise _Degraded(
                f"policy {path_rel!r} record declares living_state under "
                "immutable_digest binding (misdeclaration, not a pass)")
        digest = _sha256_of(path)
        if digest != rec.get("hash"):
            raise _Degraded(
                f"policy {path_rel!r} digest mismatch (tamper / drift)")
        return {"path": path_rel, "binding": "immutable_digest"}
    # policy_binding_mode == "living_state"
    if not rec.get("living_state"):
        raise _Degraded(
            f"policy {path_rel!r} binding_mode is living_state but its "
            "lockfile record lacks living_state: true")
    if path_rel not in _LIVING_STATE_DSTS:
        raise _Degraded(
            f"policy {path_rel!r} is not in this dispatcher's authoritative "
            "living-state set")
    return {"path": path_rel, "binding": "living_state",
            "digest_not_compared": True}


# ---------------------------------------------------------------------------
# Trusted child invocation -- fixed 4-element argv, closed-allowlist env, a
# neutral temp cwd, bounded wall clock AND bounded captured bytes on both
# streams (T6-T10).
# ---------------------------------------------------------------------------

def _combined_size(*paths: Path) -> int:
    total = 0
    for p in paths:
        try:
            total += p.stat().st_size
        except OSError:
            pass
    return total


def _read_capped(path: Path, cap: int) -> bytes:
    try:
        with path.open("rb") as handle:
            return handle.read(cap)
    except OSError:
        return b""


def _kill(proc: subprocess.Popen) -> None:
    try:
        proc.kill()
        proc.wait(timeout=5.0)
    except (ProcessLookupError, subprocess.TimeoutExpired, OSError):
        pass


def _wait_bounded(proc: subprocess.Popen, out_p: Path, err_p: Path,
                   timeout_s: float, cap: int) -> tuple[bool, bool]:
    """Wait for the child, bounded in both wall clock and captured bytes.
    Returns ``(timed_out, overflowed)``; kills the child on either."""
    deadline = time.monotonic() + timeout_s
    while True:
        try:
            proc.wait(timeout=_CHILD_POLL_S)
        except subprocess.TimeoutExpired:
            pass
        else:
            return False, _combined_size(out_p, err_p) > cap
        if _combined_size(out_p, err_p) > cap:
            _kill(proc)
            return False, True
        if time.monotonic() >= deadline:
            _kill(proc)
            return True, False


def _run_child(
    entry: RegistryEntry, runner_path: Path,
) -> tuple[int | None, bytes, bool, bool]:
    """Launch the admitted child. Returns ``(exit_code, stdout_bytes,
    timed_out, overflowed)``. The child's argv is EXACTLY the registry
    vector; its environment is EXACTLY the closed allowlist; its
    stdout/stderr are captured to a neutral temp directory, never a pipe an
    unbounded child could fill before being read; it is killed on
    timeout or byte-cap overflow."""
    argv = [sys.executable, "-I", str(runner_path), *entry.argv_mode]
    env = _build_child_env()
    with tempfile.TemporaryDirectory(prefix="cairn-secver-") as td:
        cwd = Path(td)
        out_p = cwd / "stdout.bin"
        err_p = cwd / "stderr.bin"
        with out_p.open("wb") as out_f, err_p.open("wb") as err_f:
            proc = subprocess.Popen(  # noqa: S603 -- fixed argv, shell=False
                argv, stdout=out_f, stderr=err_f, stdin=subprocess.DEVNULL,
                cwd=str(cwd), env=env, shell=False,
            )
            timed_out, overflowed = _wait_bounded(
                proc, out_p, err_p, _CHILD_TIMEOUT_S, _CHILD_OUTPUT_CAP_BYTES)
        code = proc.poll()
        out_bytes = _read_capped(out_p, _CHILD_OUTPUT_CAP_BYTES)
    return code, out_bytes, timed_out, overflowed


# ---------------------------------------------------------------------------
# Child result validation (T10, T13, T14) -- strict UTF-8, strict JSON,
# closed key set, exact identity match against the registry entry, and the
# process-exit / declared-result agreement.
# ---------------------------------------------------------------------------

def _decode_strict(raw: bytes) -> str | None:
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _parse_child_object(text: str) -> dict[str, Any] | None:
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def _degraded_leg(entry: RegistryEntry, reason: str, *,
                   child_launched: bool,
                   runner_digest: str | None = None,
                   policy: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "module_id": entry.module_id, "aggregate": DEGRADED,
        "aggregate_label": "DEGRADED", "detail": _safe_render(reason),
        "evidence_mode": entry.evidence_mode,
        "child_launched": child_launched,
        "runner_digest": runner_digest, "policy": policy,
    }


def _evaluate_capability(module_id: str, repo_root: Path,
                          records: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one selected capability's local leg end to end. Never
    raises: every failure mode maps to a leg dict carrying an ``aggregate``
    int."""
    entry = _REGISTRY.get(module_id)
    if entry is None:
        return {
            "module_id": module_id, "aggregate": INCOMPLETE,
            "aggregate_label": "INCOMPLETE",
            "detail": _safe_render(
                f"{module_id!r} is selected but has no admitted local "
                "security-verification registry entry"),
            "evidence_mode": None, "child_launched": False,
            "runner_digest": None, "policy": None,
        }

    try:
        runner_path = _bind_runner(entry, records, repo_root)
    except _Degraded as exc:
        return _degraded_leg(entry, exc.reason, child_launched=False)
    runner_digest = _sha256_of(runner_path)  # parent-computed (T16)

    try:
        policy_report = _bind_policy(entry, records, repo_root)
    except _Degraded as exc:
        return _degraded_leg(entry, exc.reason, child_launched=False,
                              runner_digest=runner_digest)

    code, out_bytes, timed_out, overflowed = _run_child(entry, runner_path)

    if timed_out:
        return _degraded_leg(entry, "child timed out", child_launched=True,
                              runner_digest=runner_digest,
                              policy=policy_report)
    if overflowed:
        return _degraded_leg(
            entry, "child output exceeded the byte cap", child_launched=True,
            runner_digest=runner_digest, policy=policy_report)

    text = _decode_strict(out_bytes)
    if text is None:
        return _degraded_leg(
            entry, "child stdout is not valid UTF-8", child_launched=True,
            runner_digest=runner_digest, policy=policy_report)
    obj = _parse_child_object(text)
    if obj is None:
        return _degraded_leg(
            entry, "child stdout is not a single valid JSON object",
            child_launched=True, runner_digest=runner_digest,
            policy=policy_report)

    if set(obj) != _REQUIRED_CHILD_KEYS:
        extra = sorted(set(obj) - _REQUIRED_CHILD_KEYS)
        missing = sorted(_REQUIRED_CHILD_KEYS - set(obj))
        return _degraded_leg(
            entry,
            f"child result schema mismatch (extra={extra}, "
            f"missing={missing})",
            child_launched=True, runner_digest=runner_digest,
            policy=policy_report)

    id_checks = (
        ("schema", entry.child_schema_version),
        ("capability", entry.module_id),
        ("contract", entry.capability_contract_version),
        ("evidence_mode", entry.evidence_mode),
    )
    for key, expected in id_checks:
        if obj.get(key) != expected:
            return _degraded_leg(
                entry, f"child {key} does not match the registry entry",
                child_launched=True, runner_digest=runner_digest,
                policy=policy_report)

    result = obj.get("result")
    details = obj.get("details")
    if not isinstance(result, str) or \
            result not in entry.result_to_aggregate_mapping:
        return _degraded_leg(
            entry, "child result is not a recognized state",
            child_launched=True, runner_digest=runner_digest,
            policy=policy_report)
    if not isinstance(details, str):
        return _degraded_leg(
            entry, "child details is not a string", child_launched=True,
            runner_digest=runner_digest, policy=policy_report)

    expected_exit, aggregate = entry.result_to_aggregate_mapping[result]
    if code not in entry.accepted_process_exits or code != expected_exit:
        return _degraded_leg(
            entry, f"child exit code and declared result disagree "
            f"(exit={code!r}, result={result!r})",
            child_launched=True, runner_digest=runner_digest,
            policy=policy_report)

    return {
        "module_id": module_id, "aggregate": aggregate,
        "aggregate_label": _AGGREGATE_LABELS[aggregate],
        "detail": _safe_render(details),
        "evidence_mode": entry.evidence_mode, "child_launched": True,
        "runner_digest": runner_digest, "policy": policy_report,
    }


# ---------------------------------------------------------------------------
# Aggregation + report assembly (T15, T20, T32)
# ---------------------------------------------------------------------------

def _build_report(legs: list[dict[str, Any]]) -> dict[str, Any]:
    aggregate = max((leg["aggregate"] for leg in legs), default=CLEAN)
    return {
        "schema": _SCHEMA,
        "status": "evaluated",
        "ok": aggregate == CLEAN,
        "aggregate": _AGGREGATE_LABELS[aggregate],
        "evidence_count": len(legs),
        "legs": legs,
        "reason": "",
    }


def _not_applicable_report(reason: str) -> dict[str, Any]:
    return {
        "schema": _SCHEMA,
        "status": "not_applicable",
        "ok": True,
        "aggregate": "NOT_APPLICABLE",
        "evidence_count": 0,
        "legs": [],
        "reason": reason,
    }


def _print_not_applicable(reason: str) -> int:
    print("NOT APPLICABLE: no selected local security capability")
    print(json.dumps(_not_applicable_report(reason), sort_keys=True))
    return 0


def _print_result(report: dict[str, Any]) -> int:
    print(f"{report['aggregate']}: {report['evidence_count']} capability "
          "leg(s) evaluated")
    for leg in report["legs"]:
        print(f"  [{leg['aggregate_label']}] {leg['module_id']}: "
              f"{leg.get('detail', '')}")
    print(json.dumps(report, sort_keys=True))
    return _AGGREGATE_EXIT[report["aggregate"]]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_security_verification.py",
        description="Local security-verification dispatcher.")
    parser.add_argument(
        "mode", choices=("local",),
        help="Evidence mode to run. Only 'local' is a valid choice at v1 -- "
             "'deployed' is not representable, by construction, not by "
             "runtime refusal.")
    return parser


def main(argv: list[str] | None = None) -> int:
    build_arg_parser().parse_args(argv)  # validates 'local'; unused further

    lock = _load_lockfile()
    if lock is None:
        if not _REGISTRY:
            # Nothing could be admitted regardless of the lockfile's state
            # (the shipped registry is empty at v1) -- NOT_APPLICABLE, not a
            # spurious DEGRADED, matching the Decision's "the no-capability
            # runtime effect is nil."
            return _print_not_applicable(
                "no selected local security capability (install lockfile "
                "unavailable; the shipped registry is empty regardless)")
        return _print_result(_build_report([{
            "module_id": None, "aggregate": DEGRADED,
            "aggregate_label": "DEGRADED",
            "detail": "install lockfile unavailable; cannot establish the "
                      "installed capability roster",
            "evidence_mode": None, "child_launched": False,
            "runner_digest": None, "policy": None,
        }]))

    capability_ids = _selected_capability_ids(lock)
    if not capability_ids:
        return _print_not_applicable("no selected local security capability")

    records = _records_by_dst(lock)
    legs = [
        _evaluate_capability(module_id, _REPO_ROOT, records)
        for module_id in capability_ids
    ]
    return _print_result(_build_report(legs))


if __name__ == "__main__":  # pragma: no cover -- exercised via main()
    sys.exit(main())
