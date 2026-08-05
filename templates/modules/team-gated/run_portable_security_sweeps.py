#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Portable offline security-sweep orchestrator -- the portable-security-sweeps
adapter runner.

**Standard-library only.**  Installs no scanner and bundles none.  It drives
exactly one adapter -- Gitleaks, offline, with no network flag -- over two scan
questions (the current tree, the committed history) and reports on the shared
aggregate exit space ``0 / 5 / 10 / 20`` with precedence ``20 > 10 > 5 > 0``.

Three properties are the contract, and every one of them is a refusal rather
than a best effort:

1. **A leg that did not run never renders as CLEAN.**  A missing binary is
   INCOMPLETE (5), loudly.  Absence is never clean.
2. **Candidate-tree content cannot choose the executable, its configuration,
   or a suppression.**  The adapter is resolved from the trusted host
   environment and refused if it lives inside the tree under check; the
   adapter config, the ignore file and the report path are runner-owned and
   materialized off-tree; reviewed suppressions come from the validated policy
   and from nowhere else.
3. **Full mode -- the only CLEAN-capable mode -- is reachable only when the
   resolved executable's SHA-256 matches a digest the admission ceremony
   recorded for this ``(version, platform, architecture)``.**  A recorded
   digest that does not match is a contradiction and degrades (20); no
   recorded digest for this platform is the ordinary *unadmitted* case and
   takes the reduced-provenance path, which can never reach 0.

A clean run is a **tripwire, not a proof**.

Chunk A of ``portable-security-sweeps`` lands the CLI, the strict policy
loader, the strict version parser, the admitted-artifact mode selector, the
aggregate and the deterministic summary.  The adapter-execution seam returns
INCOMPLETE with a named reason until the executable trust boundary lands; there
is deliberately **no** ``subprocess`` import in this file at that commit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, NamedTuple

# --- the shared aggregate exit space -----------------------------------------
# Reuses python-security's space (see templates/modules/team-gated/
# run_security_audit.py) so an adopter reads one exit vocabulary across every
# Cairn security module.  Precedence: degraded > findings > incomplete > clean.
_AGG_CLEAN = 0
_AGG_INCOMPLETE = 5
_AGG_FINDINGS = 10
_AGG_DEGRADED = 20

_PRECEDENCE = {_AGG_CLEAN: 0, _AGG_INCOMPLETE: 1, _AGG_FINDINGS: 2, _AGG_DEGRADED: 3}

#: A leg with no applicable input.  Distinct from INCOMPLETE, and it never
#: weakens another leg -- it contributes nothing to the aggregate at all.
_NOT_APPLICABLE = "NOT_APPLICABLE"

_CAPABILITY = "portable-security-sweeps"
_CONTRACT = "portable-security-sweeps/local-v1"
_EVIDENCE_MODE = "offline"
_SCHEMA = 1

#: The adapter this module supports.  OSV-Scanner, zizmor and Trivy are **not
#: supported adapters and not names the policy accepts**; each returns as its
#: own proposal with its own executable chain and ambient-config evidence.
_ADAPTER = "gitleaks"

# --- the source-owned admitted-artifact set ----------------------------------
#: Keyed by ``(version, system, machine)``; the value carries the SHA-256 of
#: the artifact the admission matrix was actually run against plus the
#: identifier of its evidence record in
#: ``dev/measurement/gitleaks-version-support.md``.
#:
#: **Not policy-controlled, not environment-controlled, and not adopter-
#: editable without editing reviewed code.**  The digest deliberately does not
#: live in the JSON policy: the policy is the adopter-editable document, and a
#: digest anything with write access to the adopter's tree could edit would let
#: a candidate *admit its own binary* -- strictly weaker than the self-reported
#: version string it replaces.
#:
#: **Initially empty.**  ``8.30.1`` enters only when the admission subcommand
#: emits a record against a Maintainer-supplied, checksum-verified binary.  An
#: empty set means the module ships reduced-provenance-only: useful current-tree
#: findings and an honest INCOMPLETE, never CLEAN.


class Admission(NamedTuple):
    """One admitted artifact: the digest measured, and where the evidence is."""

    sha256: str
    evidence: str


# CAIRN-ADMISSIONS-BEGIN (the admission ceremony edits exactly this block)
_ADMITTED_ARTIFACTS: dict[tuple[str, str, str], Admission] = {}
# CAIRN-ADMISSIONS-END

#: The one major this runner's argv, output schema and Git-invocation
#: expectations were derived against.  A different major is not "probably
#: fine"; it is unmeasured, and unmeasured means INCOMPLETE without execution.
_SUPPORTED_MAJOR = 8

# --- policy limits -----------------------------------------------------------
_POLICY_MAX_BYTES = 64 * 1024
_FINGERPRINT_MAX_LEN = 200
_FINGERPRINT_CHARSET = re.compile(r"\A[A-Za-z0-9._:/+=@-]+\Z")

#: Names a policy may never carry, checked *before* the closed-key check so the
#: refusal reason says which class was attempted.  The policy names no path, no
#: argv, no environment variable, no executable, no config file, no baseline,
#: and -- per the digest design above -- no digest, hash, checksum or admitted
#: artifact.
_FORBIDDEN_POLICY_NAME_PARTS = (
    "path", "arg", "argv", "env", "environment", "exec", "executable",
    "command", "cmd", "config", "toml", "baseline", "ignorefile",
    "digest", "hash", "checksum", "artifact", "admit", "admitted",
    "version", "mode", "versions", "binary", "url", "network",
)

_POLICY_TOP_KEYS = frozenset({"schema", "gitleaks"})
_POLICY_GITLEAKS_KEYS = frozenset({"fingerprints"})

#: Control characters refused in a fingerprint.  ``\n`` and ``\r`` are
#: deliberately **excluded** here: they are the ignore-file line-injection case
#: and carry their own dedicated refusal branch, so that deleting either branch
#: reddens exactly the node that names it.
_CTRL_OTHER = frozenset(
    [chr(c) for c in range(0x20) if chr(c) not in "\n\r"] + [chr(0x7F)]
)


class PolicyError(ValueError):
    """A policy document this runner refuses.  Refusal precedes every side
    effect: no executable is resolved and no temporary file is materialized."""


class _DuplicateKey(PolicyError):
    pass


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    for key, _value in pairs:
        if key in seen:
            raise _DuplicateKey(f"duplicate JSON key in policy: {key!r}")
        seen.add(key)
    return dict(pairs)


def _refuse_forbidden_names(keys: list[str]) -> None:
    """Refuse a policy key whose *name* attempts to reach a surface the policy
    does not own.  Runs before the closed-key check purely so the reason names
    the class -- the closed-key check would refuse these anyway."""
    for key in keys:
        low = key.lower()
        for part in _FORBIDDEN_POLICY_NAME_PARTS:
            if part in low:
                raise PolicyError(
                    f"policy key {key!r} names a surface the policy does not "
                    f"own ({part!r}); the policy carries reviewed fingerprint "
                    f"suppressions and nothing else"
                )


def parse_policy(text: str) -> dict[str, Any]:
    """Validate a policy *document* and return the accepted shape.

    Every refusal is its own branch so that a single deleted branch reddens the
    single node that names it."""
    try:
        doc = json.loads(text, object_pairs_hook=_no_duplicate_keys)
    except _DuplicateKey:
        raise
    except (ValueError, UnicodeDecodeError) as exc:
        raise PolicyError(f"policy is not valid JSON: {exc}") from None
    if not isinstance(doc, dict):
        raise PolicyError("policy top level must be a JSON object")

    _refuse_forbidden_names(list(doc))
    unknown = sorted(set(doc) - _POLICY_TOP_KEYS)
    if unknown:
        raise PolicyError(f"unknown top-level policy key(s): {unknown}")
    missing = sorted(_POLICY_TOP_KEYS - set(doc))
    if missing:
        raise PolicyError(f"missing top-level policy key(s): {missing}")

    if doc["schema"] != _SCHEMA:
        raise PolicyError(
            f"unsupported policy schema {doc['schema']!r}; this runner "
            f"accepts schema {_SCHEMA} only"
        )

    section = doc["gitleaks"]
    if not isinstance(section, dict):
        raise PolicyError("policy 'gitleaks' must be a JSON object")
    _refuse_forbidden_names(list(section))
    unknown = sorted(set(section) - _POLICY_GITLEAKS_KEYS)
    if unknown:
        raise PolicyError(f"unknown key(s) under 'gitleaks': {unknown}")
    if "fingerprints" not in section:
        raise PolicyError("policy 'gitleaks' must carry 'fingerprints'")

    raw = section["fingerprints"]
    if not isinstance(raw, list):
        raise PolicyError("policy 'gitleaks.fingerprints' must be a list")
    seen: set[str] = set()
    for item in raw:
        if not isinstance(item, str):
            raise PolicyError(f"fingerprint is not a string: {item!r}")
        if "\n" in item or "\r" in item:
            raise PolicyError(
                "fingerprint carries a newline; one fingerprint may never "
                "become two ignore-file lines"
            )
        if any(ch in _CTRL_OTHER for ch in item):
            raise PolicyError("fingerprint carries a control character")
        if not item:
            raise PolicyError("fingerprint is empty")
        if len(item) > _FINGERPRINT_MAX_LEN:
            raise PolicyError(
                f"fingerprint exceeds {_FINGERPRINT_MAX_LEN} characters"
            )
        if not _FINGERPRINT_CHARSET.match(item):
            raise PolicyError(f"fingerprint has a disallowed character: {item!r}")
        if item in seen:
            raise PolicyError(f"duplicate fingerprint: {item!r}")
        seen.add(item)
    return {"schema": _SCHEMA, "gitleaks": {"fingerprints": list(raw)}}


def load_policy(path: Path) -> dict[str, Any]:
    """Read and validate the policy at *path*.  Size is checked before the
    read, and the read is strict UTF-8."""
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise PolicyError(f"policy is unreadable: {exc}") from None
    if size > _POLICY_MAX_BYTES:
        raise PolicyError(
            f"policy exceeds {_POLICY_MAX_BYTES} bytes ({size}); refused "
            f"before it is read"
        )
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise PolicyError(f"policy is not readable strict UTF-8: {exc}") from None
    return parse_policy(text)


# --- version parsing and mode selection --------------------------------------

#: ``[0-9]`` and not ``\d``: ``\d`` matches Unicode decimal digits, so a
#: candidate reporting Devanagari or fullwidth digits would parse.
_VERSION_RE = re.compile(r"\A(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")


def parse_version(text: str) -> tuple[int, int, int] | None:
    """Parse an **exact** ``X.Y.Z``.  Anything else -- a ``v`` prefix, two
    components, a prerelease suffix, surrounding whitespace or a newline, a
    leading zero, a trailing character, a control character, non-ASCII digits
    -- returns ``None``, and ``None`` means *unmeasured*, not *probably fine*."""
    if not isinstance(text, str):
        return None
    match = _VERSION_RE.match(text)
    if match is None:
        return None
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def platform_key() -> tuple[str, str]:
    """The ``(system, machine)`` half of an admitted-artifact key."""
    return (platform.system().lower(), platform.machine().lower())


class ModeChoice(NamedTuple):
    """The outcome of mode selection.  ``mode`` is ``"full"``, ``"reduced"`` or
    ``None``; ``None`` means *refuse without executing a scan leg*."""

    mode: str | None
    result: int | None
    reason: str


def select_mode(
    version_text: str,
    digest: str | None,
    key: tuple[str, str],
    admissions: dict[tuple[str, str, str], Admission] | None = None,
) -> ModeChoice:
    """Map a self-reported version plus a measured digest onto a mode.

    Two cases that must never collapse into one:

    * **digest MISMATCH** -- a digest *is* recorded for this
      ``(version, platform, architecture)`` and the resolved binary is not it.
      That is a contradiction: DEGRADED (20), no scan leg runs, never reduced,
      never full, never CLEAN.
    * **digest ABSENT** -- no digest is recorded for this
      ``(version, platform, architecture)``.  That is the ordinary *unadmitted*
      case: the reduced-provenance path, which can never reach 0.
    """
    admitted = _ADMITTED_ARTIFACTS if admissions is None else admissions
    parsed = parse_version(version_text)
    if parsed is None:
        return ModeChoice(
            None, _AGG_INCOMPLETE,
            f"adapter version {version_text!r} is not an exact X.Y.Z; the "
            f"version is unmeasured, so no scan leg was run",
        )
    if parsed[0] != _SUPPORTED_MAJOR:
        return ModeChoice(
            None, _AGG_INCOMPLETE,
            f"adapter major {parsed[0]} is outside the measured major "
            f"{_SUPPORTED_MAJOR}; no scan leg was run",
        )
    full_key = (version_text, key[0], key[1])
    admission = admitted.get(full_key)
    if admission is None:
        return ModeChoice(
            "reduced", None,
            f"no admitted artifact is recorded for {full_key}; reduced "
            f"provenance -- this run cannot report CLEAN",
        )
    if digest is None or digest != admission.sha256:
        return ModeChoice(
            None, _AGG_DEGRADED,
            f"admitted artifact digest mismatch for {full_key}: recorded "
            f"{admission.sha256[:12]}..., resolved "
            f"{(digest or 'unmeasured')[:12]}...; no scan leg was run",
        )
    return ModeChoice(
        "full", None,
        f"admitted artifact {full_key} matched digest "
        f"{admission.sha256[:12]}... (evidence {admission.evidence})",
    )


# --- the aggregate -----------------------------------------------------------


def aggregate(results: list[int]) -> int:
    """``20 > 10 > 5 > 0``.  A finding is never hidden by an incomplete
    sibling leg, which is the whole reason this is a precedence and not a
    minimum."""
    worst = _AGG_CLEAN
    for result in results:
        if _PRECEDENCE[result] > _PRECEDENCE[worst]:
            worst = result
    return worst


class LegOutcome(NamedTuple):
    """One scan question's answer.  ``result`` is ``None`` for a NOT
    APPLICABLE leg, which contributes nothing to the aggregate."""

    leg: str
    result: int | None
    status: str
    reason: str
    findings: tuple[dict[str, Any], ...] = ()


def _escape(value: Any) -> str:
    """Render *value* so it cannot become a terminal control or forge a report
    line.  ``ensure_ascii=True`` escapes C0/C1 controls, newlines, ANSI escapes
    and bidi code points into their ``\\uXXXX`` forms rather than emitting the
    raw byte."""
    return json.dumps(value, ensure_ascii=True, sort_keys=True)


# --- the executable trust boundary -------------------------------------------
#: The complete set of host executables this module trusts.  Enumerated rather
#: than generalized, so a reader can audit it: the adapter, and Git -- which the
#: runner invokes for the pre-execution configuration screen and which the
#: adapter invokes **transitively** for the history leg.
TRUST_ROOTS = ("gitleaks", "git")

#: Cap on the bytes hashed when digesting a resolved executable.
_DIGEST_MAX_BYTES = 512 * 1024 * 1024
_DIGEST_CHUNK = 1024 * 1024

#: Outer deadlines.  The adapter's own ``--timeout`` is set strictly shorter
#: than the outer scan deadline: equal deadlines make the inner timeout
#: unobservable.
_VERSION_TIMEOUT = 30
_SCAN_TIMEOUT = 900
_ADAPTER_TIMEOUT = _SCAN_TIMEOUT - 60
_SCREEN_TIMEOUT = 60


class MissingExecutable(Exception):
    """The executable is not on the trusted host path.  **INCOMPLETE (5)** --
    absence is never clean, and it is never DEGRADED either: *absent* versus
    *present but unsound* is the contract."""


class Degraded(Exception):
    """A refusal, or a result the runner cannot trust.  **DEGRADED (20)**."""


class Resolved(NamedTuple):
    name: str
    lexical: str
    resolved: str
    directory: str
    digest: str


def _is_inside(candidate: str, root: str) -> bool:
    try:
        return os.path.commonpath([candidate, root]) == root
    except ValueError:  # different roots, or relative-vs-absolute
        return False


def file_digest(path: str) -> str:
    """SHA-256 of *path*, streamed and bounded.  A file larger than the cap is
    a refusal, never a truncated hash."""
    digest = hashlib.sha256()
    read = 0
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(_DIGEST_CHUNK)
            if not chunk:
                break
            read += len(chunk)
            if read > _DIGEST_MAX_BYTES:
                raise Degraded(
                    f"executable {path!r} exceeds {_DIGEST_MAX_BYTES} bytes; "
                    f"refusing rather than hashing a prefix"
                )
            digest.update(chunk)
    return digest.hexdigest()


def resolve_executable(name: str, target: Path, path_env: str | None) -> Resolved:
    """Resolve *name* from the **trusted host environment** and validate its
    shape and containment.

    Validated: absolute; a regular file; the executable bit set; and **neither
    the lexical nor the resolved path inside the tree under check**.  A
    package-manager symlink is fine when both paths are outside; a symlink
    whose target resolves into the candidate tree is refused -- exactly the case
    the lexical check alone lets through.

    This is **shape and containment validation, not provenance**."""
    found = shutil.which(name, path=path_env)
    if not found:
        raise MissingExecutable(
            f"{name!r} was not found on the trusted host path; the scan did "
            f"not run"
        )
    lexical = os.path.abspath(found)
    resolved = os.path.realpath(lexical)
    roots = {os.path.realpath(str(target)), os.path.abspath(str(target))}
    for label, candidate in (("lexical", lexical), ("resolved", resolved)):
        if not os.path.isabs(candidate):
            raise Degraded(f"{name!r} {label} path is not absolute: {candidate!r}")
        for root in roots:
            if _is_inside(candidate, root):
                raise Degraded(
                    f"{name!r} {label} path {candidate!r} is inside the tree "
                    f"under check ({root!r}); the candidate tree may not "
                    f"choose the executable"
                )
    if not os.path.isfile(resolved):
        raise Degraded(
            f"{name!r} resolves to {resolved!r}, which is not a regular file"
        )
    if not os.access(resolved, os.X_OK):
        raise Degraded(f"{name!r} at {resolved!r} carries no executable bit")
    return Resolved(name, lexical, resolved, os.path.dirname(resolved),
                    file_digest(resolved))


def revalidate(exe: Resolved, target: Path) -> None:
    """Re-validate immediately before invocation.

    The accepted residual is a **same-user race on a trusted checkout** between
    this moment and ``exec``, not a containment claim -- and it is narrower than
    the residual it replaces, because a swapped binary must also reproduce a
    measured digest."""
    again = resolve_executable(exe.name, target, os.path.dirname(exe.lexical))
    if again.resolved != exe.resolved:
        raise Degraded(
            f"{exe.name!r} path drifted between validation and invocation: "
            f"{exe.resolved!r} -> {again.resolved!r}"
        )
    if again.digest != exe.digest:
        raise Degraded(
            f"{exe.name!r} content drifted between validation and invocation: "
            f"{exe.digest[:12]}... -> {again.digest[:12]}..."
        )


def probe_version(exe: Resolved, env: dict[str, str]) -> str:
    """Record the adapter's ``--version`` output.

    A ``--version`` that fails, times out or emits nothing is **present but
    unsound**: DEGRADED (20), not INCOMPLETE."""
    try:
        proc = subprocess.run(
            [exe.resolved, "--version"], capture_output=True, env=env,
            timeout=_VERSION_TIMEOUT, check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise Degraded(f"{exe.name!r} --version could not be run: {exc}") from None
    if proc.returncode != 0:
        raise Degraded(
            f"{exe.name!r} --version exited {proc.returncode}; the adapter is "
            f"present but unsound"
        )
    try:
        text = proc.stdout.decode("utf-8")
    except UnicodeDecodeError:
        raise Degraded(f"{exe.name!r} --version output is not valid UTF-8") from None
    first = text.splitlines()[0].strip() if text.strip() else ""
    if not first:
        raise Degraded(f"{exe.name!r} --version emitted nothing")
    return first


def child_env(
    mode: str, git: Resolved | None, empty_dir: str,
    empty_config: str | None = None,
) -> dict[str, str]:
    """Build the child environment from an **allowlist**, never a denylist.

    Because the base is an allowlist, **every** inherited ``GIT_*``,
    ``GITLEAKS_*``, proxy, Python-import, pager and prompt variable is dropped
    by construction rather than by name -- a denylist that misses one is the
    failure mode this shape removes.

    **Full mode** gets a minimal ``PATH`` containing *only* the verified Git
    directory -- the adapter needs Git for the history leg and nothing else.
    **Reduced mode** gets an **off-tree empty directory**, so Git is neither
    resolved nor reachable: that is what makes reduced mode structurally unable
    to answer the history question rather than merely declining to."""
    if mode == "full" and git is not None:
        path = git.directory
    else:
        path = empty_dir
    env = {
        "PATH": path,
        "HOME": empty_dir,
        "LC_ALL": "C",
        "TZ": "UTC",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": empty_config or os.devnull,
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_CONFIG_COUNT": str(len(_COUNTED_GIT_CONFIG)),
    }
    for index, (key, value) in enumerate(_COUNTED_GIT_CONFIG):
        env[f"GIT_CONFIG_KEY_{index}"] = key
        env[f"GIT_CONFIG_VALUE_{index}"] = value
    return env


# --- the candidate-configuration boundary ------------------------------------
#: Counted Git config keys forced onto every child.  ``GIT_CONFIG_COUNT``
#: entries behave like ``-c`` and outrank repository-local config, which matters
#: precisely because *the adapter* spawns Git, so the runner cannot pass ``-c``
#: itself.
#:
#: **This is defence in depth over the keys it names.  It is NOT a boundary.**
#: Measured: a candidate steps around it with one ``include.path`` line, or one
#: ``includeIf``, needing no new Git version and no exotic key; and Git offers
#: **no** way to disable the repository-local tier -- there is no
#: ``GIT_CONFIG_LOCAL``, and ``GIT_CONFIG_NOSYSTEM`` + ``GIT_CONFIG_GLOBAL`` +
#: ``GIT_CONFIG_SYSTEM`` together leave it live.  What bounds the configuration
#: surface is :func:`screen_local_config`.
_COUNTED_GIT_CONFIG: tuple[tuple[str, str], ...] = (
    ("core.useReplaceRefs", "false"),   # refs/replace/<sha> forges history
    ("core.hooksPath", os.devnull),     # a hook is candidate-supplied execution
    ("core.fsmonitor", "false"),        # a monitor program runs during status
    ("core.pager", "cat"),
    ("core.quotePath", "false"),
    ("diff.external", ""),
    ("protocol.allow", "never"),
    ("protocol.file.allow", "never"),
)

#: The screen's own command.  ``--includes`` is load-bearing: **measured**, a
#: listing without it shows ``include.path=...`` and *neither* injected key, so
#: a screen written the obvious way is silently defeated.
_SCREEN_ARGV_TAIL = (
    "config", "--list", "--local", "--includes", "--show-origin", "-z",
)
_SCREEN_MAX_BYTES = 256 * 1024

#: The **source-owned** inert allowlist for repository-local configuration.
#: Deny-by-default: anything not named here refuses before execution.  Not
#: policy-controlled.
_INERT_LOCAL_KEYS = frozenset({
    "core.repositoryformatversion", "core.filemode", "core.bare",
    "core.logallrefupdates", "core.ignorecase", "core.precomposeunicode",
    "core.symlinks", "core.sharedrepository",
})
#: Inert key *families* an ordinary repository carries.  Refusing these would
#: make the screen unusable on real trees, which is the over-refusal failure
#: mode that gets a security control switched off.  None of them is a program
#: reference: transport is pinned inert by ``protocol.allow=never`` and no leg
#: fetches.
_INERT_LOCAL_PATTERNS = (
    re.compile(r"\Aextensions\.[a-z0-9]+\Z"),
    re.compile(r"\Aremote\.[^.]+\.(url|fetch|pushurl|mirror|tagopt)\Z"),
    re.compile(r"\Abranch\.[^.]+\.(remote|merge|rebase)\Z"),
)

_IGNORE_FILENAME = ".gitleaksignore"


def _key_is_inert(key: str) -> bool:
    if key in _INERT_LOCAL_KEYS:
        return True
    return any(pattern.match(key) for pattern in _INERT_LOCAL_PATTERNS)


def refuse_candidate_ignore_files(target: Path) -> None:
    """Refuse **before execution** when the candidate tree carries a
    ``.gitleaksignore`` anywhere -- regular file or symlink, at any depth.

    Required because the adapter loads the target's ignore file *even when*
    ``--gitleaks-ignore-path`` names a trusted empty file, and exposes no
    observed switch to disable that.  The walk does **not** follow symlinks."""
    for root, dirnames, filenames in os.walk(str(target), followlinks=False):
        for name in list(dirnames) + list(filenames):
            if name == _IGNORE_FILENAME:
                raise Degraded(
                    f"the candidate tree carries {os.path.join(root, name)!r}; "
                    f"the adapter loads it even when a trusted empty ignore "
                    f"path is named, so the run is refused before execution"
                )


def parse_screen_output(raw: bytes) -> list[tuple[str, str]]:
    """Parse ``git config --list --local --includes --show-origin -z`` into
    ``(origin, key)`` pairs.  An unexpected shape is a refusal, never a
    best-effort parse."""
    if not raw:
        return []
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise Degraded("the configuration listing is not valid UTF-8") from None
    fields = text.split("\0")
    if fields and fields[-1] == "":
        fields.pop()
    if len(fields) % 2 != 0:
        raise Degraded(
            f"the configuration listing has an unexpected shape "
            f"({len(fields)} fields); refusing rather than guessing"
        )
    pairs: list[tuple[str, str]] = []
    for index in range(0, len(fields), 2):
        origin = fields[index]
        key = fields[index + 1].split("\n", 1)[0]
        pairs.append((origin, key))
    return pairs


def screen_local_config(
    git: Resolved, target: Path, env: dict[str, str]
) -> list[tuple[str, str]]:
    """**Deny-by-default pre-execution screen** over the candidate's
    *include-expanded* repository-local configuration.

    Refuses on any key outside the source-owned inert allowlist, on any origin
    file that resolves outside the candidate's ``.git/`` directory (which is how
    an ``include.path`` or ``includeIf`` injection presents), and on a listing
    that fails, times out or exceeds a byte cap.

    Runs under the **same** sterilized child environment the legs get.
    Measured: run this way a hostile ``core.pager`` does **not** execute, so the
    screen's own Git call does not hand control to candidate configuration.

    The residual is the same **snapshot** race the ignore-file refusal accepts,
    and the screen bounds *configuration* -- not everything a candidate
    repository controls."""
    git_dir = (target / ".git").resolve()
    argv = [git.resolved, "-C", str(target), *_SCREEN_ARGV_TAIL]
    try:
        proc = subprocess.run(argv, capture_output=True, env=env,
                              timeout=_SCREEN_TIMEOUT, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise Degraded(f"the configuration screen could not run: {exc}") from None
    if proc.returncode != 0:
        raise Degraded(
            f"the configuration screen exited {proc.returncode}; refusing "
            f"rather than running with an unscreened configuration"
        )
    if len(proc.stdout) > _SCREEN_MAX_BYTES:
        raise Degraded(
            f"the configuration listing exceeds {_SCREEN_MAX_BYTES} bytes; "
            f"refused"
        )
    pairs = parse_screen_output(proc.stdout)
    for origin, key in pairs:
        if not origin.startswith("file:"):
            raise Degraded(
                f"configuration key {key!r} has a non-file origin {origin!r}"
            )
        origin_path = origin[len("file:"):]
        candidate = Path(origin_path)
        if not candidate.is_absolute():
            candidate = target / origin_path
        resolved_origin = candidate.resolve()
        if not _is_inside(str(resolved_origin), str(git_dir)):
            raise Degraded(
                f"configuration key {key!r} comes from {str(resolved_origin)!r}, "
                f"outside the candidate's .git/ directory -- an include or "
                f"includeIf injection; refused before execution"
            )
        if not _key_is_inert(key):
            raise Degraded(
                f"repository-local configuration key {key!r} is not on the "
                f"reviewed inert allowlist; refused before execution"
            )
    return pairs


def _adapter_seam(context: dict[str, Any]) -> list[LegOutcome]:
    """Execute the adapter's legs.

    Chunk B lands the execution boundary; the **output contract** -- parsing,
    validation, escaping, the aggregate -- lands in Chunk D, so a leg that runs
    reports INCOMPLETE with a named reason until then.  It is never CLEAN."""
    exe: Resolved = context["adapter"]
    target: Path = context["target"]
    env: dict[str, str] = context["env"]
    legs: list[LegOutcome] = []
    for leg, argv in context["legs"]:
        try:
            revalidate(exe, target)
        except Degraded as exc:
            legs.append(LegOutcome(leg, _AGG_DEGRADED, "DEGRADED", str(exc)))
            continue
        try:
            subprocess.run(argv, capture_output=True, env=env,
                           cwd=context["cwd"], timeout=_SCAN_TIMEOUT,
                           check=False)
        except (OSError, subprocess.SubprocessError) as exc:
            legs.append(LegOutcome(leg, _AGG_DEGRADED, "DEGRADED",
                                   f"adapter invocation failed: {exc}"))
            continue
        legs.append(LegOutcome(
            leg, _AGG_INCOMPLETE, "INCOMPLETE",
            "adapter output contract not yet validated",
        ))
    return legs


def summarize(
    target: Path,
    policy_path: Path,
    legs: list[LegOutcome],
    mode: str | None,
    mode_reason: str,
    adapter_facts: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """The deterministic summary.  The human report is a rendering of *this*
    validated structure and never of scanner text."""
    scored = [leg.result for leg in legs if leg.result is not None]
    return {
        "schema": _SCHEMA,
        "capability": _CAPABILITY,
        "contract": _CONTRACT,
        "evidence_mode": _EVIDENCE_MODE,
        "adapter": _ADAPTER,
        "target": str(target),
        "policy": str(policy_path),
        "mode": mode,
        "mode_reason": mode_reason,
        "adapter_facts": dict(adapter_facts or {}),
        "legs": [
            {
                "leg": leg.leg,
                "result": leg.result,
                "status": leg.status,
                "reason": leg.reason,
                "findings": list(leg.findings),
            }
            for leg in legs
        ],
        "result": aggregate(scored),
        "residuals": list(RESIDUALS),
    }


#: Residuals printed with every run.  A residual that lives only in a doctrine
#: file an adopter may never open is a shelf artifact.
RESIDUALS = (
    "This is a tripwire on a trusted checkout, not a proof and not a reviewer "
    "for untrusted changes.",
    "Host executables are validated for shape and containment, never for "
    "provenance: v1 does not authenticate them.",
    "The pre-execution screens (candidate ignore file, repository-local "
    "configuration) are snapshots; a same-user delete/create race between the "
    "screen and execution is accepted, not closed.",
    "The repository-local configuration screen bounds configuration only, and "
    "the counted Git config keys are defence in depth over the keys they name "
    "-- not a boundary.",
)


def render_report(summary: dict[str, Any]) -> str:
    """Render the validated summary.  Every interpolated string goes through
    ``_escape``; no child stdout or stderr is ever relayed."""
    lines = [
        f"[portable] adapter={_ADAPTER} mode={_escape(summary['mode'])}",
        f"[portable] target={_escape(summary['target'])}",
        f"[portable] mode-reason: {_escape(summary['mode_reason'])}",
    ]
    for name in sorted(summary["adapter_facts"]):
        lines.append(
            f"[portable] fact {name}={_escape(summary['adapter_facts'][name])}"
        )
    for leg in summary["legs"]:
        status = leg["status"]
        result = "n/a" if leg["result"] is None else str(leg["result"])
        lines.append(
            f"[portable] leg={_escape(leg['leg'])} status={status} "
            f"result={result} reason={_escape(leg['reason'])}"
        )
        for finding in leg["findings"]:
            lines.append(f"[portable]   finding {_escape(finding)}")
    for residual in summary["residuals"]:
        lines.append(f"[portable] residual: {residual}")
    lines.append(f"[portable] aggregate={summary['result']}")
    return "\n".join(lines)


def child_document(summary: dict[str, Any]) -> dict[str, Any]:
    """The ``security-verification`` child document -- one bounded strict-UTF-8
    JSON document, with ``details`` under its own bounded schema."""
    return {
        "schema": _SCHEMA,
        "capability": _CAPABILITY,
        "contract": _CONTRACT,
        "evidence_mode": _EVIDENCE_MODE,
        "result": summary["result"],
        "details": {
            "adapter": summary["adapter"],
            "mode": summary["mode"],
            "mode_reason": summary["mode_reason"],
            "legs": [
                {
                    "leg": leg["leg"],
                    "result": leg["result"],
                    "status": leg["status"],
                    "reason": leg["reason"],
                    "finding_count": len(leg["findings"]),
                }
                for leg in summary["legs"]
            ],
        },
    }


def _default_policy_path() -> Path:
    return Path(__file__).resolve().parent / "portable_security_policy.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_portable_security_sweeps.py",
        description=(
            "One measured offline security sweep over the current tree and the "
            "committed history.  Installs no scanner."
        ),
    )
    parser.add_argument("--target", default=".",
                        help="repository to sweep (default: the current directory)")
    parser.add_argument("--policy", default=None,
                        help="policy document (default: the runner's sibling)")
    parser.add_argument("--json", action="store_true",
                        help="emit the deterministic JSON summary")
    parser.add_argument(
        "--security-verification", action="store_true",
        help=("the local/offline security-verification entry point: emit the "
              "bounded child result document and nothing else"),
    )
    return parser


#: The history leg's fixed ``--log-opts``.  ``--text`` defeats a tracked
#: ``.gitattributes`` ``binary`` rule that otherwise made a committed token
#: invisible; ``--no-textconv`` and ``--no-ext-diff`` keep Git diff drivers from
#: extending the scan into executable helpers.
_LOG_OPTS = "--all --full-history --text --no-textconv --no-ext-diff"


class Workspace(NamedTuple):
    """The runner-owned, **off-tree** files one run materializes.  Nothing here
    is ever copied from, or written into, the candidate tree."""

    config: str
    ignore: str
    report_dir: str
    empty_dir: str
    empty_config: str


def materialize_workspace(workdir: str, fingerprints: list[str]) -> Workspace:
    """Write the runner-owned adapter config and the reviewed-suppression
    ignore file **off-tree**.

    The config extends the binary's built-in rules and carries no
    policy-supplied TOML.  Reviewed fingerprints go in one per line; a
    fingerprint carrying a newline was already refused by the policy validator,
    because one fingerprint may never become two ignore-file lines."""
    empty_dir = os.path.join(workdir, "empty")
    os.makedirs(empty_dir, exist_ok=True)
    report_dir = os.path.join(workdir, "reports")
    os.makedirs(report_dir, exist_ok=True)
    config = os.path.join(workdir, "cairn-adapter.toml")
    with open(config, "w", encoding="utf-8") as handle:
        handle.write(
            'title = "cairn-portable-security-sweeps"\n\n'
            "[extend]\nuseDefault = true\n"
        )
    ignore = os.path.join(workdir, "cairn-reviewed.gitleaksignore")
    with open(ignore, "w", encoding="utf-8") as handle:
        for fingerprint in fingerprints:
            handle.write(fingerprint + "\n")
    empty_config = os.path.join(workdir, "empty.gitconfig")
    with open(empty_config, "w", encoding="utf-8"):
        pass
    return Workspace(config, ignore, report_dir, empty_dir, empty_config)


def _leg_argv(
    exe: Resolved, leg: str, target: Path, work: Workspace,
) -> tuple[list[str], str]:
    """The **runner-owned** argv for one leg, and that leg's report path.

    The policy contributes **no** argv element, ever.  Every path the adapter
    is told to read or write is off-tree."""
    report = os.path.join(work.report_dir, f"{leg}.json")
    argv = [exe.resolved, "dir" if leg == "current-tree" else "git", str(target)]
    if leg == "history":
        argv += ["--log-opts", _LOG_OPTS]
    else:
        # The current-tree leg does not follow symlinks, and adds no
        # .gitignore filter: a .gitignore'd ordinary file is still scanned.
        argv += ["--follow-symlinks=false"]
    argv += [
        "--config", work.config,
        "--gitleaks-ignore-path", work.ignore,
        "--ignore-gitleaks-allow",
        "--redact=100",
        "--no-color",
        "--no-banner",
        "--report-format", "json",
        "--report-path", report,
        "--max-archive-depth=0",
        "--max-decode-depth=0",
        f"--timeout={_ADAPTER_TIMEOUT}s",
    ]
    return argv, report


def run_sweep(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    """The ordinary sweep, in the order the contract requires.

    Policy refusal precedes every side effect.  Executable resolution and
    containment precede any execution.  The identifying ``--version`` probe is
    the only adapter invocation that precedes mode selection; **no scan leg
    runs** until a mode is selected."""
    target = Path(args.target).resolve()
    policy_path = (
        Path(args.policy).resolve() if args.policy else _default_policy_path()
    )
    facts: dict[str, Any] = {}

    # 1. Policy -- before any executable is resolved and before any temporary
    #    file is materialized.
    try:
        policy = load_policy(policy_path)
    except PolicyError as exc:
        legs = [LegOutcome("policy", _AGG_DEGRADED, "DEGRADED", str(exc))]
        return _AGG_DEGRADED, summarize(
            target, policy_path, legs, None,
            "policy refused before any side effect", facts,
        )

    # 2. The two trust roots -- resolution and containment only, no execution.
    try:
        adapter = resolve_executable("gitleaks", target, os.environ.get("PATH"))
    except MissingExecutable as exc:
        legs = [LegOutcome("adapter", _AGG_INCOMPLETE, "INCOMPLETE", str(exc))]
        return _AGG_INCOMPLETE, summarize(
            target, policy_path, legs, None,
            "the adapter is absent; absence is never clean", facts,
        )
    except Degraded as exc:
        legs = [LegOutcome("adapter", _AGG_DEGRADED, "DEGRADED", str(exc))]
        return _AGG_DEGRADED, summarize(
            target, policy_path, legs, None,
            "the adapter failed shape or containment validation", facts,
        )
    facts["adapter_lexical"] = adapter.lexical
    facts["adapter_resolved"] = adapter.resolved
    facts["adapter_digest"] = adapter.digest

    git: Resolved | None = None
    git_reason = ""
    try:
        git = resolve_executable("git", target, os.environ.get("PATH"))
        facts["git_lexical"] = git.lexical
        facts["git_resolved"] = git.resolved
    except MissingExecutable as exc:
        git_reason = str(exc)
    except Degraded as exc:
        legs = [LegOutcome("git", _AGG_DEGRADED, "DEGRADED", str(exc))]
        return _AGG_DEGRADED, summarize(
            target, policy_path, legs, None,
            "the transitive Git trust root failed validation", facts,
        )

    with tempfile.TemporaryDirectory(prefix="cairn-portable-") as workdir:
        work = materialize_workspace(
            workdir, policy["gitleaks"]["fingerprints"]
        )
        empty_dir = work.empty_dir
        facts["adapter_config"] = work.config
        facts["reviewed_ignore_file"] = work.ignore

        # 3. Two pre-execution refusals, BEFORE any adapter invocation --
        #    including the identifying --version probe -- so that "refused
        #    before execution" is literally true of the adapter.
        try:
            refuse_candidate_ignore_files(target)
        except Degraded as exc:
            legs = [LegOutcome("preflight", _AGG_DEGRADED, "DEGRADED", str(exc))]
            return _AGG_DEGRADED, summarize(
                target, policy_path, legs, None,
                "a candidate suppression file refused the run before execution",
                facts,
            )
        if git is not None and (target / ".git").exists():
            screen_env = child_env("reduced", None, empty_dir, work.empty_config)
            try:
                pairs = screen_local_config(git, target, screen_env)
            except Degraded as exc:
                legs = [LegOutcome("preflight", _AGG_DEGRADED, "DEGRADED", str(exc))]
                return _AGG_DEGRADED, summarize(
                    target, policy_path, legs, None,
                    "the repository-local configuration screen refused the run "
                    "before execution", facts,
                )
            facts["screened_local_config_keys"] = sorted({key for _o, key in pairs})

        # 4. The identifying probe, then the digest gate and mode selection.
        probe_environment = child_env("reduced", None, empty_dir, work.empty_config)
        try:
            version_text = probe_version(adapter, probe_environment)
        except Degraded as exc:
            legs = [LegOutcome("adapter", _AGG_DEGRADED, "DEGRADED", str(exc))]
            return _AGG_DEGRADED, summarize(
                target, policy_path, legs, None,
                "the adapter is present but unsound", facts,
            )
        facts["adapter_version_output"] = version_text

        choice = select_mode(version_text, adapter.digest, platform_key())
        if choice.mode is None:
            status = "DEGRADED" if choice.result == _AGG_DEGRADED else "INCOMPLETE"
            legs = [LegOutcome("adapter", choice.result, status, choice.reason)]
            return choice.result, summarize(
                target, policy_path, legs, None, choice.reason, facts,
            )

        # 5. The legs.  Reduced mode cannot reach Git, so it asks only the
        #    current-tree question and reports the history question INCOMPLETE.
        environment = child_env(choice.mode, git, empty_dir, work.empty_config)
        facts["child_path"] = environment["PATH"]
        facts["empty_path_dir"] = empty_dir
        current_argv, current_report = _leg_argv(
            adapter, "current-tree", target, work
        )
        facts["current_tree_report"] = current_report
        legs_to_run = [("current-tree", current_argv)]
        pending: list[LegOutcome] = []
        if choice.mode == "full" and git is not None:
            history_argv, history_report = _leg_argv(
                adapter, "history", target, work
            )
            facts["history_report"] = history_report
            legs_to_run.append(("history", history_argv))
        elif git is None:
            pending.append(LegOutcome(
                "history", _AGG_INCOMPLETE, "INCOMPLETE",
                git_reason or "git is absent; the history question was not asked",
            ))
        else:
            pending.append(LegOutcome(
                "history", _AGG_INCOMPLETE, "INCOMPLETE",
                "reduced provenance: Git is unreachable from the child "
                "environment, so the history question was not asked",
            ))
        outcomes = _adapter_seam({
            "adapter": adapter, "target": target, "env": environment,
            "cwd": workdir, "legs": legs_to_run,
        })
        summary = summarize(
            target, policy_path, outcomes + pending, choice.mode,
            choice.reason, facts,
        )
    return summary["result"], summary


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result, summary = run_sweep(args)
    if args.security_verification:
        sys.stdout.write(
            json.dumps(child_document(summary), ensure_ascii=True,
                       sort_keys=True) + "\n"
        )
    elif args.json:
        sys.stdout.write(
            json.dumps(summary, ensure_ascii=True, sort_keys=True) + "\n"
        )
    else:
        sys.stdout.write(render_report(summary) + "\n")
    return result


if __name__ == "__main__":  # pragma: no cover -- exercised by subprocess
    raise SystemExit(main())
