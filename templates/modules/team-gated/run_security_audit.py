#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Python security-audit orchestrator -- the python-security self-audit gate.

Composes the adopter's self-audit passes into one standalone, **standard-
library-only** command (no pytest, no dev dependency required to run it):

1. **integrity preflight (SR-1)** -- before any pass, verify this apparatus and
   its policy inputs against the install lockfile. A self-audit launched from a
   tree whose scanner / runner / allowlist / baseline / roots-manifest / gate
   scripts are not lockfile-clean **refuses** rather than runs.
2. **content-scan** (the content-security module's ``content_scan_runner.py``)
   -- only when content-security is an installed module; loud NOT-APPLICABLE
   otherwise, never a silent clean.
3. **bandit** -- static analysis over the adopter's ``python_package``.
4. **pip-audit** -- dependency CVE check (network egress is OPT-IN; off by
   default; a denied / offline lookup is reported unavailable, not clean).
5. **adopted-executable source gate** -- bandit over the lockfile-recorded
   ``.py`` files this install adopted (binary provenance is out of scope).

Self-audit scope (read this first)
----------------------------------

This is a drift / content-injection tripwire on the adopter's **own trusted
tree**, run in the adopter's own CI or dev loop. The apparatus *and its policy
inputs* are trusted input: committed, reviewed-as-code, integrity-covered. It
is **not** a reviewer for untrusted code that can modify the apparatus itself.
**Do not wire it into untrusted-PR / fork CI** -- a run from an attacker's
checkout executes the attacker's audit. A clean result is **a tripwire, not a
proof**.

Aggregate exit table (a DISTINCT space; never collides with a
component's 0/1/2/3 or 127). Each component's raw outcome is printed
separately; the aggregate is the worst tier, precedence
degraded > findings > incomplete > clean:

* ``0``  -- clean: every applicable pass ran and found nothing blocking
  (content-scan *advisory* findings may be present; they are printed and do
  NOT fail the aggregate).
* ``5``  -- INCOMPLETE COVERAGE: no findings, but a selected pass did not run
  or could not establish what it covered -- content-security not installed
  (injection NOT APPLICABLE), pip-audit network egress off **while the tool
  itself is present** (lookup UNAVAILABLE), or a dependency-coverage set the
  run could not establish (UNKNOWN). Distinct from clean so automation cannot
  read "a pass did not run" as "scan ran clean"; enable the pass (or narrow
  scope) for a clean 0. Dominates clean.
* ``10`` -- FINDINGS: bandit or pip-audit found issues. Dominates incomplete.
* ``20`` -- DEGRADED / UNAVAILABLE / TAMPER: a pass could not be trusted to
  run -- integrity preflight failed, ``python_package`` is missing/invalid, a
  selected content-scan returned scan-failure (2) or stale (3), a required
  tool was absent (**including pip-audit itself: an absent tool is DEGRADED
  and dominates an egress-off lookup, so a run with both conditions reports
  20, not 5**), a tool timed out / flooded / emitted undecodable output, or
  pip-audit hit a tool/network error. Dominates findings.

Every blocking reason a pass finds is reported, not just the first; the pass's
tier is the **worst applicable** reason under the precedence above.

The injection pass being NOT-APPLICABLE (content-security not installed) is
printed loudly as its own line; it never silently reads as a clean scan.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import NamedTuple

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent
_LOCKFILE = _REPO_ROOT / "dev" / ".cairn" / "cairn-lock.yml"
_RUNNER = _HERE / "content_scan_runner.py"

# Aggregate exit tiers -- a DISTINCT space (never collides with a component's
# 0/1/2/3 or 127). Precedence: degraded > findings > incomplete > clean.
_AGG_CLEAN = 0
_AGG_INCOMPLETE = 5     # ran, no findings, but a selected pass did not fully run
_AGG_FINDINGS = 10
_AGG_DEGRADED = 20

# The apparatus + policy files each installed security module ships (relative to
# the repo root). The SR-1 preflight derives the REQUIRED set from the installed
# module roster: every file an installed module ships must be
# lockfile-recorded AND present AND hash-matched -- a missing record is a
# failure, not a skip (else a surviving clean record would let an unrecorded,
# tampered sibling load).
_MODULE_APPARATUS = {
    "content-security": (
        "scripts/content_scan.py",
        "scripts/content_scan_runner.py",
        "scripts/content_scan_roots.txt",
        "scripts/content_scan_residuals.txt",
        "scripts/content_scan_allowlist.txt",
    ),
    "python-security": (
        "scripts/run_security_audit.py",
    ),
}


class AuditDegraded(Exception):
    """A fail-closed condition that maps to the aggregate DEGRADED tier."""


# --------------------------------------------------------------------------
# Lockfile (read-only, stdlib JSON; the lockfile is JSON-encoded YAML)
# --------------------------------------------------------------------------

def load_lockfile(path: Path = _LOCKFILE) -> dict:
    """Parse the install lockfile (JSON after its ``#`` comment header).

    Fail-closed: a missing / unparseable lockfile is a DEGRADED condition --
    the orchestrator cannot establish authoritative installed state without
    it."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise AuditDegraded(
            f"install lockfile unavailable ({exc}); cannot establish "
            "authoritative installed state") from exc
    # Strip the leading comment lines, then JSON-parse the object.
    brace = text.find("{")
    if brace < 0:
        raise AuditDegraded("install lockfile has no JSON object")
    try:
        return json.loads(text[brace:])
    except json.JSONDecodeError as exc:
        raise AuditDegraded(f"install lockfile is unparseable: {exc}") from exc


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# --------------------------------------------------------------------------
# SR-1 -- integrity preflight over the apparatus + policy inputs
# --------------------------------------------------------------------------

def required_apparatus_dsts(lock: dict) -> list[str]:
    """The complete apparatus file set the INSTALLED security modules require
    Derived from the lockfile module roster, not from whichever
    records happen to exist -- so a dropped record cannot shrink the checked
    set."""
    modules = set(lock.get("modules", []))
    required: list[str] = []
    for module, dsts in _MODULE_APPARATUS.items():
        if module in modules:
            required.extend(dsts)
    return required


def integrity_preflight(repo_root: Path, lock: dict) -> None:
    """Verify the COMPLETE apparatus + policy file set the installed security
    modules require, against the lockfile.

    Standalone stdlib reimplementation of the lockfile-integrity check scoped
    to the security apparatus (Cairn's ``verify_integrity`` is an engine tool,
    not shipped to adopters). For every file an installed security module ships,
    a lockfile record MUST exist and the on-disk file MUST be present, a regular
    file, and hash-match. A **missing record fails closed** (it is not skipped):
    otherwise a surviving clean record would let an unrecorded, tampered sibling
    (e.g. content_scan_runner.py) load. Any failure -> DEGRADED; a self-audit
    must not run from an unverified apparatus.
    """
    by_dst = {rec.get("dst"): rec for rec in lock.get("files", [])}
    required = required_apparatus_dsts(lock)
    if not required:
        raise AuditDegraded(
            "no security modules are recorded as installed; cannot run a "
            "verified self-audit (is this an installed Cairn tree with "
            "content-security / python-security?)")
    for dst in required:
        rec = by_dst.get(dst)
        if rec is None:
            raise AuditDegraded(
                f"required apparatus file {dst!r} for an installed module has "
                "no lockfile record (incomplete / tampered apparatus); "
                "refusing to self-audit")
        abs_p = repo_root / dst
        if abs_p.is_symlink() or not abs_p.is_file():
            raise AuditDegraded(
                f"required apparatus file {dst!r} is recorded but missing / "
                "not a regular file on disk (tamper)")
        want = str(rec.get("hash", ""))
        got = "sha256:" + _sha256_hex(abs_p.read_bytes())
        if want != got:
            raise AuditDegraded(
                f"apparatus file {dst!r} does not match its lockfile hash "
                "(tamper / drift); refusing to self-audit from an unverified "
                "apparatus")


# --------------------------------------------------------------------------
# single contained python_package validation
# --------------------------------------------------------------------------

def validate_python_package(repo_root: Path, lock: dict) -> Path:
    """Resolve + validate the ``python_package`` token from the lockfile.

    v1 contract: exactly one repo-relative package directory. Validated
    fail-closed: present, repo-relative (no ``..`` / absolute), not the repo
    root (``.``), an existing directory, and symlink-contained within the repo.
    Multi-package coverage is a documented v2 limitation."""
    token = (lock.get("tokens") or {}).get("python_package")
    if not token or not str(token).strip():
        raise AuditDegraded(
            "python_package token is unfilled in the lockfile; cannot scan "
            "(the install preflight should have prevented this)")
    rel = str(token).strip()
    p = Path(rel)
    if p.is_absolute() or ".." in p.parts:
        raise AuditDegraded(
            f"python_package {rel!r} is not a contained repo-relative path")
    if rel in (".", "./", ""):
        raise AuditDegraded(
            f"python_package {rel!r} is the repo root; v1 requires a single "
            "package directory, not the whole repo")
    repo_resolved = repo_root.resolve()
    target = (repo_resolved / p)
    if target.is_symlink():
        raise AuditDegraded(f"python_package {rel!r} is a symlink; refusing")
    resolved = target.resolve()
    if repo_resolved not in resolved.parents and resolved != repo_resolved:
        raise AuditDegraded(
            f"python_package {rel!r} resolves outside the repo root (escape)")
    if not resolved.is_dir():
        raise AuditDegraded(
            f"python_package {rel!r} is not an existing directory (v1 supports "
            "a single package directory; multi-package layouts are a v2 gap)")
    return resolved


# --------------------------------------------------------------------------
# Crit #2 / SR-3 -- trusted subprocess boundary
# --------------------------------------------------------------------------

def _safe_target_args(paths: list[Path]) -> list[str]:
    """Return path arguments guarded against argv injection (SR-3): an
    explicit ``--`` terminator precedes the file arguments, and any path whose
    final component begins with ``-`` is refused (it could be read as an
    option). Paths are passed resolved + absolute."""
    args: list[str] = ["--"]
    for p in paths:
        name = p.name
        if name.startswith("-"):
            raise AuditDegraded(
                f"refusing option-shaped path argument {name!r} (argv "
                "injection guard)")
        args.append(str(p))
    return args


#: The CLOSED allowlist of environment variables a security tool inherits.
#: A denylist strips the names someone thought of; completeness is the property
#: under test, and a denylist cannot have it -- a future tool that honours a
#: variable nobody has heard of would still be steerable. Only these names (and
#: the ``LC_`` prefix below) reach a child; **everything else is dropped**,
#: including ``PYTHON*``, ``PIPAPI_PYTHON_LOCATION``, every ``PIP_*`` /
#: ``PIP_AUDIT_*``, ``*_PROXY``, ``REQUESTS_CA_BUNDLE`` and ``SSL_CERT_FILE``.
#: Interpreter selection, vulnerability service, endpoint, proxy and trust
#: store are then argv decisions, not ambient ones.
_ENV_ALLOWLIST = (
    "PATH", "HOME", "LANG",
    "TMPDIR", "TEMP", "TMP",
    # Windows minimum for an interpreter to start at all.
    "SYSTEMROOT", "SystemRoot", "COMSPEC", "PATHEXT", "USERPROFILE",
    "APPDATA", "LOCALAPPDATA", "NUMBER_OF_PROCESSORS", "PROCESSOR_ARCHITECTURE",
)
#: Name prefixes the allowlist also admits (locale only).
_ENV_ALLOWLIST_PREFIXES = ("LC_",)

#: Wall-clock ceiling for one security-tool subprocess, and the ceiling on the
#: bytes retained from it. Both are **module constants and deliberately NOT
#: environment-configurable**: the environment is the attack surface this
#: boundary closes, so a knob there would re-open it.
_TOOL_TIMEOUT_S = 900
_TOOL_OUTPUT_CAP_BYTES = 8 * 1024 * 1024
#: Poll interval for the bounded wait, and the grace given to each kill signal.
_TOOL_POLL_S = 0.05
_TOOL_KILL_GRACE_S = 5.0

_POSIX = (os.name == "posix")
_SIGKILL = getattr(signal, "SIGKILL", signal.SIGTERM)

#: Control characters kept verbatim when rendering tool output (TAB, LF).
_CONTROL_KEEP = frozenset((0x09, 0x0A))


class ToolRun(NamedTuple):
    """The outcome of one security-tool subprocess at the trusted boundary.

    ``status`` is the **boundary's** verdict and is distinct from the tool's
    own exit ``code``. Only ``"ran"`` licenses a caller to classify from
    ``code``; ``"tool-absent"``, ``"timeout"``, ``"truncated"``,
    ``"undecodable"`` and any ``"...+cleanup-failed"`` variant are DEGRADED,
    because output that could not be completed, bounded or read is output that
    cannot be parsed. ``stdout`` / ``stderr`` are the decoded text; they are
    rendered through :func:`escape_controls`, never raw."""

    code: int
    status: str
    stdout: str
    stderr: str


def escape_controls(text: str) -> str:
    """Neutralise terminal control characters in tool output.

    Tool output is relayed to the operator's terminal and is the evidence for a
    security decision. Left raw, a crafted filename carrying ``ESC [ 2K`` +
    ``CR`` can erase the current line and **forge a report line** -- including
    a clean verdict. C0 (except TAB / LF), DEL and C1 are rendered as ``\\xNN``;
    every other character passes through **verbatim**. This sanitizes control
    characters only -- it does not rewrite, truncate or re-encode the text."""
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


def build_child_env(passthrough: tuple[str, ...] = ()) -> dict[str, str]:
    """Build a security tool's child environment from the CLOSED allowlist.

    ``passthrough`` names variables the operator opted into explicitly (the
    ``--pass-env`` flag); they are added on top of the allowlist and are always
    **named in the report** (see :func:`describe_child_env`) -- inheritance is
    never silent. A closed allowlist can break a tool that legitimately needs
    an unlisted variable (a corporate trust store is the realistic case); that
    is the release valve, and the failure mode is loud (the tool errors ->
    DEGRADED), never a quiet mis-scan."""
    env = {
        name: value for name, value in os.environ.items()
        if name in _ENV_ALLOWLIST or name.startswith(_ENV_ALLOWLIST_PREFIXES)
    }
    for name in passthrough:
        value = os.environ.get(name)
        if value is not None:
            env[name] = value
    return env


def describe_child_env(passthrough: tuple[str, ...] = ()) -> str:
    """The one report line stating the child-environment policy for a pass.

    Every explicitly passed-through variable is **named here**, in the report
    the operator reads, so an inherited proxy or trust store is a visible,
    risk-accepted decision rather than an ambient one."""
    if not passthrough:
        return ("child environment: CLOSED allowlist -- nothing is inherited "
                "beyond the named minimum, and no variable was passed through.")
    return ("child environment: CLOSED allowlist PLUS explicit, risk-accepted "
            "pass-through of: " + ", ".join(sorted(passthrough)))


def _combined_size(*paths: Path) -> int:
    total = 0
    for path in paths:
        try:
            total += path.stat().st_size
        except OSError:
            pass
    return total


def _wait_bounded(proc, out_p: Path, err_p: Path, timeout_s: float,
                  cap: int) -> tuple[bool, bool]:
    """Wait for the child, bounded in **both** wall clock and captured bytes.

    Returns ``(timed_out, overflowed)``."""
    deadline = time.monotonic() + timeout_s
    while True:
        try:
            proc.wait(timeout=_TOOL_POLL_S)
        except subprocess.TimeoutExpired:
            pass
        else:
            return False, _combined_size(out_p, err_p) > cap
        if _combined_size(out_p, err_p) > cap:
            return False, True
        if time.monotonic() >= deadline:
            return True, False


def _process_group_alive(process_group: int) -> bool:
    """Return whether a POSIX process group still has a live member."""
    try:
        os.killpg(process_group, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _wait_process_group_exit(process_group: int, deadline: float) -> bool:
    while time.monotonic() < deadline:
        if not _process_group_alive(process_group):
            return True
        time.sleep(_TOOL_POLL_S)
    return not _process_group_alive(process_group)


def _kill_tree(proc, process_group: int | None = None) -> bool:
    """Terminate, then kill, the child **and its descendants**.

    On POSIX the child is started in its own session/process group, so the
    signal reaches a grandchild the tool spawned; a tool that outlives its own
    timeout through a detached helper is the failure this closes. Windows has
    no equivalent here and is a **named residual**, not a claim. Returns
    ``False`` if cleanup could not be completed -- reported, never silent."""
    if not _POSIX:  # pragma: no cover -- Windows residual
        try:
            proc.kill()
            proc.wait(timeout=_TOOL_KILL_GRACE_S)
            return True
        except ProcessLookupError:
            return True
        except (OSError, subprocess.TimeoutExpired):
            return False

    group = proc.pid if process_group is None else process_group
    try:
        os.killpg(group, signal.SIGTERM)
    except ProcessLookupError:
        return True
    except OSError:
        return False

    # The leader may exit immediately while a descendant ignores SIGTERM.
    # Group existence, not leader status, decides whether escalation is owed.
    if _wait_process_group_exit(
            group, time.monotonic() + _TOOL_KILL_GRACE_S):
        try:
            proc.wait(timeout=0)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            pass
        return True

    try:
        os.killpg(group, _SIGKILL)
    except ProcessLookupError:
        return True
    except OSError:
        return False
    try:
        proc.wait(timeout=_TOOL_KILL_GRACE_S)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        pass
    return _wait_process_group_exit(
        group, time.monotonic() + _TOOL_KILL_GRACE_S)


def _read_capped(path: Path, cap: int) -> tuple[bytes, bool]:
    try:
        size = path.stat().st_size
        with path.open("rb") as handle:
            data = handle.read(cap)
    except OSError:
        return b"", False
    return data, size > cap


def _decode_tool_bytes(raw: bytes) -> tuple[str, bool]:
    """Decode captured bytes, reporting whether replacement was needed."""
    try:
        return raw.decode("utf-8"), False
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace"), True


def _run_tool(argv: list[str], *, label: str,
              env: dict[str, str] | None = None,
              timeout: float | None = None,
              output_cap: int | None = None) -> ToolRun:
    """Run a security tool with a trusted boundary:

    * ``shell=False`` + a fixed argument vector (no shell, no word-splitting);
    * the child interpreter runs in **isolated mode** (``python -I``: no cwd /
      no ``PYTHONPATH`` / no user-site on ``sys.path``) so a repo-local
      ``bandit/`` or ``pip_audit/`` package cannot shadow the real tool;
    * a **neutral temporary working directory** off the candidate tree (so the
      cwd that ``-m`` would otherwise add is empty);
    * a **closed-allowlist environment** (:func:`build_child_env`) -- not a
      denylist: only named variables reach the child.

    Four further guarantees, each of which maps a violation to DEGRADED rather
    than to a clean or parseable result:

    1. **Timeout.** ``_TOOL_TIMEOUT_S`` bounds the wall clock. On expiry the
       child is terminated, then killed, and the status is ``"timeout"``. A
       timeout is never clean.
    2. **Bytes, not text.** Output is captured as **bytes** and decoded with an
       explicit policy at render time. A decode that needed replacement is
       recorded (``"undecodable"``): output that could not be read is output
       that cannot be parsed. Previously a single invalid byte raised
       ``UnicodeDecodeError`` out of this function, out of ``main()``, and the
       process died with a traceback and exit 1 -- a code inside the
       *component* space the aggregate exit table promises never to collide
       with.
    3. **Bounded capture.** ``_TOOL_OUTPUT_CAP_BYTES`` caps the combined
       stdout+stderr retained; exceeding it kills the child and yields
       ``"truncated"``.
    4. **Control-character escaping.** Output is rendered through
       :func:`escape_controls`, so a crafted filename cannot forge a report
       line.

    **Two named residuals, stated rather than discovered.** (a) The byte cap
    bounds *this process's* memory -- it does **not** bound what the child
    writes to its own disk. (b) Descendant cleanup uses a POSIX process group;
    **Windows is untested here**.

    Target paths are passed by the caller as resolved + contained absolutes, so
    a neutral cwd does not lose them. ``argv`` MUST begin
    ``[sys.executable, "-I", "-m", ...]``."""
    child_env = build_child_env() if env is None else env
    limit = _TOOL_OUTPUT_CAP_BYTES if output_cap is None else output_cap
    budget = _TOOL_TIMEOUT_S if timeout is None else timeout
    popen_kwargs = {"start_new_session": True} if _POSIX else {}
    try:
        with tempfile.TemporaryDirectory(prefix="cairn-audit-") as neutral:
            out_p = Path(neutral) / "stdout.bin"
            err_p = Path(neutral) / "stderr.bin"
            handle_out = out_p.open("wb")
            handle_err = err_p.open("wb")
            try:
                proc = subprocess.Popen(  # noqa: S603 -- fixed argv, shell=False
                    argv, cwd=neutral, shell=False, env=child_env,
                    stdin=subprocess.DEVNULL,
                    stdout=handle_out, stderr=handle_err, **popen_kwargs,
                )
                process_group = proc.pid if _POSIX else None
            finally:
                handle_out.close()
                handle_err.close()
            timed_out, overflowed = _wait_bounded(proc, out_p, err_p,
                                                  budget, limit)
            cleanup_ok = True
            if timed_out or overflowed:
                cleanup_ok = _kill_tree(proc, process_group)
            else:
                proc.wait()
            out_raw, out_over = _read_capped(out_p, limit)
            err_raw, err_over = _read_capped(err_p, limit)
    except FileNotFoundError:
        print(f"[{label}] NOT INSTALLED in the active interpreter "
              f"({sys.executable}); cannot run this pass.", file=sys.stderr)
        return ToolRun(127, "tool-absent", "", "")

    out_text, out_replaced = _decode_tool_bytes(out_raw)
    err_text, err_replaced = _decode_tool_bytes(err_raw)
    if timed_out:
        status = "timeout"
    elif overflowed or out_over or err_over:
        status = "truncated"
    elif out_replaced or err_replaced:
        status = "undecodable"
    else:
        status = "ran"
    if not cleanup_ok:
        status = f"{status}+cleanup-failed"

    if out_text:
        print(escape_controls(out_text))
    if err_text:
        print(escape_controls(err_text), file=sys.stderr)
    if status != "ran":
        print(f"[{label}] BOUNDARY STATUS {status!r} -- this tool's output "
              "cannot be trusted as evidence; the pass is DEGRADED, not clean.",
              file=sys.stderr)
    code = proc.returncode if proc.returncode is not None else 127
    return ToolRun(code, status, out_text, err_text)


# --------------------------------------------------------------------------
# Passes
# --------------------------------------------------------------------------

def _load_runner():
    spec = importlib.util.spec_from_file_location("content_scan_runner", _RUNNER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def run_injection_pass(repo_root: Path, lock: dict) -> tuple[str, int]:
    """Content-scan pass, gated on authoritative installed state.

    Returns ``(status, tier_contribution)``. content-security NOT in the
    installed roster -> ``("not-applicable", 0)`` (printed loudly, never a
    silent clean). Selected but the runner is absent -> DEGRADED. Selected +
    present -> the runner's 0/1/2/3 mapped to a tier (advisory findings (1)
    contribute 0; scan-failure (2) / stale (3) contribute DEGRADED)."""
    if "content-security" not in lock.get("modules", []):
        # A not-applicable injection pass is INCOMPLETE coverage,
        # a distinct non-clean tier -- automation must not read it as a scan
        # that ran clean.
        print("\n[injection] NOT APPLICABLE -- content-security is not an "
              "installed module; the injection pass did NOT run (incomplete "
              "coverage, not a clean scan).")
        return "not-applicable", _AGG_INCOMPLETE
    if not _RUNNER.is_file():
        print("\n[injection] content-security is selected but "
              "content_scan_runner.py is missing -- FAILING closed.",
              file=sys.stderr)
        return "missing-runner", _AGG_DEGRADED
    runner = _load_runner()
    code, files, all_flags, new_flags, stale = runner.audit(repo_root)
    runner._print_summary(code, files, all_flags, new_flags, stale)
    if code in (0, 1):
        return f"content-scan:{code}", _AGG_CLEAN     # advisory findings
    return f"content-scan:{code}", _AGG_DEGRADED      # 2 scan-fail / 3 stale


def run_bandit_pass(pkg: Path, repo_root: Path) -> tuple[str, int]:
    """bandit over the validated python_package (Crit #2 trusted boundary)."""
    if shutil.which("bandit") is None and \
            importlib.util.find_spec("bandit") is None:
        print("\n[bandit] NOT INSTALLED -- cannot run the static-analysis pass.",
              file=sys.stderr)
        return "tool-absent", _AGG_DEGRADED
    argv = [sys.executable, "-I", "-m", "bandit", "-r", "-q",
            *_safe_target_args([pkg])]
    run = _run_tool(argv, label="bandit")
    code, status = run.code, run.status
    if status == "tool-absent":
        return "tool-absent", _AGG_DEGRADED
    if status != "ran":
        # A timed-out / flooded / undecodable tool has produced no evidence.
        return f"bandit:{status}", _AGG_DEGRADED
    if code == 0:
        return "bandit:clean", _AGG_CLEAN
    if code == 1:
        return "bandit:findings", _AGG_FINDINGS
    return "bandit:error", _AGG_DEGRADED  # usage/parse error -> degraded


def run_adopted_executable_gate(repo_root: Path, lock: dict) -> tuple[str, int]:
    """The Cairn-adopted-executable **source gate**: confirm every ``.py``
    this install adopted (the lockfile-recorded ``dst``s) is byte-for-byte the
    vetted, lockfile-recorded source. It is an *integrity* gate, not a re-lint:
    Cairn's shipped scripts are already Cairn-bandit-gated and trusted, so the
    adopter-side concern is *tamper* -- has an adopted executable source drifted
    from what was vetted? A mismatched / missing adopted ``.py`` fails closed
    (DEGRADED). Binary provenance (downloaded solver / compiler executables and
    their behavior) is explicitly **out of scope** -- this gate covers adopted
    Python *sources* only."""
    py_recs = [rec for rec in lock.get("files", [])
               if str(rec.get("dst", "")).endswith(".py")]
    if not py_recs:
        return "no-adopted-py", _AGG_CLEAN
    tampered: list[str] = []
    for rec in py_recs:
        dst = rec["dst"]
        abs_p = repo_root / dst
        if abs_p.is_symlink() or not abs_p.is_file():
            tampered.append(f"{dst} (missing / not a regular file)")
            continue
        want = str(rec.get("hash", ""))
        got = "sha256:" + _sha256_hex(abs_p.read_bytes())
        if want != got:
            tampered.append(f"{dst} (hash mismatch)")
    if tampered:
        print("\n[adopted-exec] adopted Python source(s) drifted from their "
              "vetted lockfile record -- FAILING closed:", file=sys.stderr)
        for t in tampered:
            print(f"  TAMPER {t}", file=sys.stderr)
        return "adopted-exec:tamper", _AGG_DEGRADED
    print(f"\n[adopted-exec] {len(py_recs)} adopted Python source(s) verified "
          "against the lockfile (integrity gate; binary provenance out of "
          "scope).")
    return "adopted-exec:clean", _AGG_CLEAN


# --------------------------------------------------------------------------
# The dependency leg's coverage contract
# --------------------------------------------------------------------------

#: The three accepted dispositions for a distribution in the audited set.
#: NO-MATCH-IN-PINNED-SOURCES names every source and version queried and is
#: **accepted non-coverage, not evidence of safety** -- it asserts nothing
#: about the world, only about what these sources hold.
_DISPOSITION_SCANNED = "SCANNED"
_DISPOSITION_NO_MATCH = "NO-MATCH-IN-PINNED-SOURCES"
_DISPOSITION_UNKNOWN = "UNKNOWN"

#: The pip-audit version whose ``--format json`` schema this parser was
#: established against. **A version bump re-opens the measurement**: the schema
#: below is a property of *that* release's formatter, not a contract the tool
#: publishes, so a different version is a re-measurement rather than an
#: assumption. The parser therefore also validates the *shape* at runtime and
#: fails closed (UNKNOWN, never CLEAN) when it does not match.
_PIP_AUDIT_SCHEMA_VERSION = "2.10.1"

#: Whether pip-audit's ``--format json`` schema has been established against a
#: pinned tool version. It **has**, at 2.10.1, by reading that release's own
#: formatter (``pip_audit/_format/json.py`` -- ``JsonFormat.format`` and
#: ``_format_dep``); a shape is a property of the formatter, so the warrant is
#: the formatter's source rather than a guess:
#:
#:     top level              {"dependencies": [...], "fixes": [...]}
#:     resolved distribution  {"name", "version", "vulns": [...]}
#:     skipped  distribution  {"name", "skip_reason"}
#:
#: **The load-bearing fact.** The skipped set is exposed **inline in**
#: ``dependencies`` with **no separate top-level key**, discriminated only by
#: carrying ``skip_reason`` in place of ``version``/``vulns``. An implementation
#: that reads a top-level ``skipped`` array finds nothing, reports **zero
#: UNKNOWN**, and makes CLEAN reachable on a run where the tool silently failed
#: to resolve part of the dependency set. The UNKNOWN count is therefore derived
#: by partitioning ``dependencies`` on the presence of ``skip_reason``.
_PIP_AUDIT_SCHEMA_ESTABLISHED = True
_PIP_AUDIT_SCHEMA_NOTE = (
    "pip-audit's --format json schema is treated as NOT established for this "
    "run, so the child's enumeration cannot be read. The audited set is "
    "therefore UNKNOWN and this leg cannot return CLEAN.")

#: Advisory sources this leg pins, named in the NO-MATCH disposition so the
#: disposition states what was queried rather than asserting a universal
#: negative.
_PINNED_ADVISORY_SOURCES = ("osv.dev (pip-audit --vulnerability-service osv)",)

#: **NO-MATCH-IN-PINNED-SOURCES is not observable at the established schema
#: version, and that is reported rather than printed as a zero.** A resolved
#: entry carries ``"vulns": []`` both when the pinned source holds a record with
#: no vulnerabilities *and* when it holds no record for that name at all; the
#: schema exposes no field distinguishing the two. So the count would be a
#: structural zero, and a printed ``NO-MATCH 0`` reads as "every distribution
#: had a record", which is the universal negative that was withdrawn. It does not
#: move any tier -- NO-MATCH never gated the verdict, only UNKNOWN does -- so
#: what is lost is report precision, not fail-closed behaviour. Stated here and
#: in the run's own output so a reader cannot mistake the silence for coverage.
_NO_MATCH_NOT_OBSERVABLE = (
    "NOT OBSERVABLE at pip-audit " + _PIP_AUDIT_SCHEMA_VERSION + ": a resolved "
    "entry reports an empty vulnerability list both when the pinned source "
    "holds a record with no vulnerabilities and when it holds no record for "
    "that name, and the schema exposes no field separating them. A SCANNED "
    "disposition here therefore means 'the pinned sources were queried and "
    "returned no vulnerabilities for this name' -- it does NOT establish that "
    "those sources carry a record for it")

#: Bounds on the conda-metadata enumeration. The directory is derived from
#: ``sys.prefix`` and its records are package-controlled input, so the read is
#: capped in both record count and per-record size.
_CONDA_META_MAX_RECORDS = 20000
_CONDA_META_MAX_RECORD_BYTES = 4 * 1024 * 1024


class Coverage(NamedTuple):
    """What the dependency leg established about the set it audited.

    ``established`` is the load-bearing field: it is ``True`` only when the
    **child's own reported enumeration** could be read. The orchestrator never
    counts distributions itself and assumes the child saw the same ones -- a
    parent-derived denominator is an assumption, not evidence."""

    established: bool
    scanned: int
    no_match: int
    unknown: int
    note: str
    #: The distribution names **the child reported**, in report order. This is
    #: the denominator itself rather than a count of it, so a parent-side
    #: enumeration substituted for it is visible by name and not only by
    #: arithmetic.
    names: tuple[str, ...] = ()
    #: Count of validated vulnerability entries in the child's structured
    #: report. CLEAN requires this to be zero independently of the exit code.
    vulnerabilities: int = 0


class LocalBuilds(NamedTuple):
    """The per-run residual classification. **No baseline is stored.**"""

    residual: int
    not_residual: int
    unknown: int
    residual_names: tuple[str, ...]


class CondaScope(NamedTuple):
    """Quantified non-coverage: what this leg did **not** audit."""

    applicable: bool
    records: int
    conda_only: int
    unknown: int


def pip_audit_argv(*, cache_dir: Path) -> list[str]:
    """The **fixed** argument vector for the pip-audit pass.

    Every element is a literal or a path this function was handed; **no element
    is derived from ``os.environ``**. The vulnerability service, the output
    format, the output destination (stdout -- never a path from the
    environment), the cache location and the progress renderer are all pinned
    here, in argv, because a narrowed claim over an ambient environment is
    exactly as false as a wide one.

    **What is verified, and how.** Every flag above was confirmed to exist, with
    the value used among its accepted choices, against **pip-audit 2.10.1** by
    reading that version's own ``--help``; the *shape of the JSON* it emits was
    established against the same version by reading its formatter's source (see
    ``_PIP_AUDIT_SCHEMA_ESTABLISHED``). Both are purely local reads of an
    installed package -- no index fetch, no audit run. A flag a *different*
    version rejects surfaces as a tool usage error -> DEGRADED, and a JSON shape
    a different version changes fails closed to UNKNOWN; both are loud.

    **One thing is not pinned here, and it is named rather than implied.** The
    OSV *endpoint* is not in this argv: ``--osv-url`` exists in 2.10.1 and is
    deliberately unused, so the endpoint falls to the tool's own default
    constant. What keeps that safe is the closed allowlist in
    :func:`build_child_env` -- ``PIP_AUDIT_OSV_URL`` is an argparse *default* in
    pip-audit's CLI, so an ambient value would silently redirect the lookup, and
    the allowlist stops it without having to know its name. The pinned-sources
    claim is therefore exactly as wide as the flag pinned above
    (``--vulnerability-service osv``) and no wider: it names the service this
    argv selects, not a URL this argv fixes.

    ``--strict`` is deliberately **not** pinned, and that version's help text
    confirms the reason rather than merely suggesting it: it *"fail[s] the
    entire audit if dependency collection fails on any dependency"*, which
    makes an unresolvable dependency share an exit code with a vulnerability
    report -- conflating non-coverage with findings, the precise confusion this
    leg exists to prevent. Non-coverage is reported through the disposition
    counts instead. ``-o/--output`` exists and is deliberately unused: the
    destination is stdout, never a path."""
    return [
        sys.executable, "-I", "-m", "pip_audit",
        "--format", "json",
        "--vulnerability-service", "osv",
        "--progress-spinner", "off",
        "--cache-dir", str(cache_dir),
    ]


def active_pip_audit_version() -> str | None:
    """Return pip-audit's version in the interpreter used by ``-m``.

    The console script on ``PATH`` is deliberately irrelevant: the fixed argv
    executes ``sys.executable -I -m pip_audit``, so the matching distribution
    metadata must come from that same interpreter.
    """
    try:
        return importlib.metadata.version("pip-audit")
    except (importlib.metadata.PackageNotFoundError, OSError, ValueError):
        return None


def _valid_pip_audit_vulnerability(value: object) -> bool:
    """Validate the 2.10.1 JSON fields needed to count a finding."""
    if not isinstance(value, dict):
        return False
    vuln_id = value.get("id")
    fix_versions = value.get("fix_versions")
    return (isinstance(vuln_id, str) and bool(vuln_id.strip())
            and isinstance(fix_versions, list)
            and all(isinstance(item, str) for item in fix_versions))


def classify_pip_audit_output(
    text: str, *, schema_established: bool | None = None,
) -> Coverage:
    """Classify the child's report into the three accepted dispositions.

    **The denominator is the distribution set the child reported** -- the
    ``dependencies`` array of pip-audit's own ``--format json`` output. The
    orchestrator never enumerates distributions itself and assumes the child saw
    the same ones; a parent-derived denominator is an assumption, not evidence.

    **The partition is on ``skip_reason``, and that choice is the whole point.**
    A skipped distribution is one pip-audit could not resolve, so nothing about
    it was looked up: it is UNKNOWN. It appears **inline in ``dependencies``**
    with no separate top-level key (see ``_PIP_AUDIT_SCHEMA_ESTABLISHED``), so a
    reader that looks for a ``skipped`` collection finds none, counts zero
    UNKNOWN, and reaches CLEAN on a run where part of the set was never audited.

    Where the enumeration cannot be read -- an unestablished schema, non-JSON,
    truncated or decode-replaced output, or a top-level shape that is not the
    established one -- it is *not established*, which is UNKNOWN, which is never
    CLEAN. Individual entries that match neither the resolved nor the skipped
    shape count UNKNOWN rather than being dropped. The alternative (assume clean
    on parse failure) is the single defect this contract exists to prevent."""
    established = (_PIP_AUDIT_SCHEMA_ESTABLISHED if schema_established is None
                   else schema_established)
    if not established:
        return Coverage(False, 0, 0, 0, _PIP_AUDIT_SCHEMA_NOTE)
    try:
        report = json.loads(text)
    except (json.JSONDecodeError, ValueError) as exc:
        return Coverage(
            False, 0, 0, 0,
            f"the tool's report is not parseable JSON ({exc}); the enumeration "
            "is NOT established, so the audited set is UNKNOWN -- a parse "
            "failure is never read as a clean scan.")
    entries = report.get("dependencies") if isinstance(report, dict) else None
    if not isinstance(entries, list):
        return Coverage(
            False, 0, 0, 0,
            "the tool's report parsed, but its top level does not carry the "
            "'dependencies' array the schema established against pip-audit "
            f"{_PIP_AUDIT_SCHEMA_VERSION} requires, so which distributions the "
            "child enumerated is UNKNOWN. A shape this parser was not measured "
            "against fails closed rather than being read optimistically. "
            f"(top level seen: {sorted(report)[:8] if isinstance(report, dict) else type(report).__name__})")
    scanned = unknown = vulnerabilities = 0
    names: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            unknown += 1
            names.append("<malformed>")
            continue
        name = entry.get("name")
        names.append(name if isinstance(name, str) and name.strip()
                     else "<unnamed>")
        if "skip_reason" in entry:
            # Reported by the child as unresolved: nothing was looked up.
            unknown += 1
        elif isinstance(entry.get("version"), str) \
                and isinstance(entry.get("vulns"), list):
            vulns = entry["vulns"]
            if all(_valid_pip_audit_vulnerability(vuln) for vuln in vulns):
                scanned += 1
                vulnerabilities += len(vulns)
            else:
                # A malformed vulnerability entry makes the distribution's
                # disposition unknown; it is never silently counted as clean.
                unknown += 1
        else:
            # Neither established shape -- counted, never dropped.
            unknown += 1
    return Coverage(
        True, scanned, 0, unknown,
        f"the child reported {len(entries)} distribution(s); {scanned} resolved "
        f"and queried, {unknown} UNKNOWN (unresolved by the tool or not matching "
        f"the schema established against pip-audit {_PIP_AUDIT_SCHEMA_VERSION}). "
        f"{_DISPOSITION_NO_MATCH} is {_NO_MATCH_NOT_OBSERVABLE}.",
        tuple(names), vulnerabilities)


def local_build_disposition(raw: str | None) -> str:
    """PEP 610 disposition of one distribution's ``direct_url.json`` payload.

    Returns ``"residual"``, ``"not-residual"`` or ``"unknown"``. A distribution
    qualifies as locally built **iff** its ``dir_info`` carries ``editable``
    true, **or** it carries ``vcs_info``. A non-editable local path does not
    qualify, and neither does ``archive_info`` with a ``file://`` URL: read
    literally, "installed from a local path" admits every conda-forge build
    artifact -- 241 public packages on the environment this was measured on --
    which is exactly the drift the rule exists to prevent.

    ``raw`` is **package-controlled input**, the same trust class as tool
    output. An unreadable, undecodable or unparseable payload classifies
    ``"unknown"`` -- never ``"not-residual"``, never silently skipped -- and
    UNKNOWN gates CLEAN."""
    if raw is None:
        return "not-residual"
    try:
        record = json.loads(raw)
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        return "unknown"
    if not isinstance(record, dict):
        return "unknown"
    if record.get("vcs_info"):
        return "residual"
    dir_info = record.get("dir_info")
    if isinstance(dir_info, dict) and dir_info.get("editable") is True:
        return "residual"
    return "not-residual"


def survey_local_builds(dists=None) -> LocalBuilds:
    """Apply :func:`local_build_disposition` across the installed set.

    This is a **parent-side** read, and legitimate only because the child is
    pinned to this interpreter by the fixed argv and the closed-allowlist
    environment. Remove that pin and this silently describes a different
    environment. Nothing is stored: v1 computes the residual per run and
    reports it, because a committed baseline derived from one mutable local
    environment would make an unrepresentative classification look like a
    portable security fact."""
    residual = not_residual = unknown = 0
    names: list[str] = []
    source = importlib.metadata.distributions() if dists is None else dists
    for dist in source:
        try:
            raw = dist.read_text("direct_url.json")
        except OSError:
            unknown += 1
            continue
        disposition = local_build_disposition(raw)
        if disposition == "residual":
            residual += 1
            names.append(_dist_name(dist) or "<unnamed>")
        elif disposition == "unknown":
            unknown += 1
        else:
            not_residual += 1
    return LocalBuilds(residual, not_residual, unknown, tuple(sorted(names)))


def _dist_name(dist) -> str | None:
    try:
        return dist.metadata["Name"]
    except (KeyError, TypeError, OSError):
        return None


def _canonical_name(name: str) -> str:
    """PEP 503 canonical form, so ``scikit_learn`` and ``scikit-learn`` are one
    name across the two inventories."""
    return re.sub(r"[-_.]+", "-", name).strip("-").lower()


def installed_distribution_names() -> set[str]:
    names = set()
    for dist in importlib.metadata.distributions():
        name = _dist_name(dist)
        if name:
            names.add(_canonical_name(name))
    return names


def conda_non_coverage(
    prefix: Path, python_dist_names: set[str], *,
    max_records: int = _CONDA_META_MAX_RECORDS,
    max_record_bytes: int = _CONDA_META_MAX_RECORD_BYTES,
) -> CondaScope:
    """Count -- and **only** count -- the conda-managed packages this leg did
    not audit.

    **Enumeration for reporting, never a lookup.** Not one of these names is
    queried against any advisory source; the count states what was *not*
    audited, so it can never be read as coverage. Conda / native advisory
    coverage is outside this module's declared scope.

    Bounded and fail-closed: ``conda-meta/*.json`` **only** (the directory also
    holds non-JSON ``history`` and ``state`` entries, on which an unguarded
    glob-plus-parse raises); a symlinked ``conda-meta`` is refused; the record
    count and each record's size are capped; and a malformed, oversized or
    unreadable record contributes **UNKNOWN** and is reported, never silently
    dropped."""
    try:
        meta = Path(prefix).resolve() / "conda-meta"
        if meta.is_symlink() or not meta.is_dir():
            return CondaScope(False, 0, 0, 0)
        records = sorted(meta.glob("*.json"))
    except OSError:
        return CondaScope(False, 0, 0, 0)
    if len(records) > max_records:
        # Over the bound: report the whole set UNKNOWN rather than parse it.
        return CondaScope(True, len(records), 0, len(records))
    names: set[str] = set()
    unknown = 0
    for record in records:
        try:
            if record.is_symlink() or not record.is_file():
                unknown += 1
                continue
            if record.stat().st_size > max_record_bytes:
                unknown += 1
                continue
            payload = json.loads(record.read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeDecodeError):
            unknown += 1
            continue
        name = payload.get("name") if isinstance(payload, dict) else None
        if not isinstance(name, str) or not name.strip():
            unknown += 1
            continue
        names.add(_canonical_name(name))
    conda_only = names - {_canonical_name(n) for n in python_dist_names}
    return CondaScope(True, len(records), len(conda_only), unknown)


def run_pip_audit_pass(repo_root: Path, *, allow_egress: bool,
                       passthrough_env: tuple[str, ...] = ()) -> tuple[str, int]:
    """pip-audit over the active interpreter's Python distributions.

    **Declared scope.** This leg audits the Python distributions discoverable
    in the audited environment. It does **not** audit conda-managed native
    packages, system packages, or vendored / statically-linked libraries; the
    count of what it did not audit is reported as a number, not as a caveat.

    **Every blocking reason is reported, not the first.** Tool availability,
    egress disposition and the interpreter observation are evaluated
    independently and all printed; the tier is the **worst applicable** reason
    under the module's own precedence. An absent tool is DEGRADED (the exit
    table already assigns "a required tool was absent" to 20); egress off with
    the tool present is INCOMPLETE.

    **Network egress is OPT-IN** (Imp #5 / SR-5): unconfigured runs do NOT
    egress. Without ``--allow-network`` the lookup **does not run at all** --
    the pass returns before pip-audit is invoked, so it does not "run against
    its local cache", and a denied / offline / failed lookup is reported
    **unavailable, not clean**. ``--allow-network`` authorizes the *documented*
    service pinned in :func:`pip_audit_argv`, never an ambient one.

    **CLEAN requires zero UNKNOWN.** Findings dominate clean; degraded
    dominates both. A NO-MATCH-IN-PINNED-SOURCES count is reported alongside a
    clean result and never folded into it."""
    print("\n[pip-audit] DECLARED SCOPE -- Python distributions discoverable "
          "in the audited environment. Conda-managed native packages, system "
          "packages and vendored / statically-linked libraries are NOT "
          "audited by this leg.")
    print(f"[pip-audit] OBSERVATION: interpreter {sys.executable} "
          f"(Python {sys.version_info.major}.{sys.version_info.minor}"
          f".{sys.version_info.micro}) -- recorded as an observation of the "
          "environment this run audited, not as an assertion that it matches "
          "any project record.")
    print(f"[pip-audit] {describe_child_env(passthrough_env)}")

    scope = conda_non_coverage(Path(sys.prefix), installed_distribution_names())
    if scope.applicable:
        print(f"[pip-audit] NOT AUDITED: {scope.conda_only} conda-managed "
              f"package(s) in this environment fall outside the declared scope "
              "and were NOT looked up in any advisory source (enumerated for "
              f"reporting only, never queried); {scope.unknown} conda record(s) "
              "could not be read and count as UNKNOWN.")
    else:
        print("[pip-audit] NOT AUDITED: no conda metadata under the "
              "interpreter prefix, so the conda non-coverage count does not "
              "apply here; the declared scope above still holds.")

    # Both blockers are evaluated INDEPENDENTLY and both are reported; the
    # early return on the first one is what made an egress-off run never
    # mention that the tool was absent. The egress disposition is evaluated
    # first **deliberately**: it is the lower tier, so a first-wins regression
    # is visible in the tier rather than masked by an ordering that happens to
    # find the worst reason first.
    blockers: list[tuple[str, int]] = []
    if not allow_egress:
        print("\n[pip-audit] network egress OFF (default). Re-run with "
              "--allow-network to enable the remote CVE lookup; package names "
              "+ versions (only) would then be sent to the pinned "
              "vulnerability service. The lookup did NOT run -- reporting "
              "UNAVAILABLE (incomplete coverage), not clean.", file=sys.stderr)
        blockers.append(("egress-off-unavailable", _AGG_INCOMPLETE))
    if shutil.which("pip-audit") is None and \
            importlib.util.find_spec("pip_audit") is None:
        print("\n[pip-audit] NOT INSTALLED -- the dependency CVE tool is "
              "absent, so this pass cannot run at all. A required tool that "
              "was absent is DEGRADED, not incomplete.", file=sys.stderr)
        blockers.append(("tool-absent", _AGG_DEGRADED))
    if blockers:
        print("\n[pip-audit] blocking reason(s): "
              + ", ".join(name for name, _ in blockers))
        return ("+".join(name for name, _ in blockers),
                max(tier for _, tier in blockers))

    observed_version = active_pip_audit_version()
    if observed_version != _PIP_AUDIT_SCHEMA_VERSION:
        seen = observed_version if observed_version is not None else "unreadable"
        print("\n[pip-audit] COVERAGE NOT ESTABLISHED -- the active "
              f"interpreter provides pip-audit {seen}, but this parser was "
              f"established against {_PIP_AUDIT_SCHEMA_VERSION}. The lookup "
              "will not run and this pass cannot return CLEAN.",
              file=sys.stderr)
        return "pip-audit:schema-version-unestablished", _AGG_INCOMPLETE
    print(f"[pip-audit] schema binding: active interpreter distribution "
          f"matches established pip-audit {_PIP_AUDIT_SCHEMA_VERSION}.")

    with tempfile.TemporaryDirectory(prefix="cairn-pip-audit-cache-") as cache:
        run = _run_tool(pip_audit_argv(cache_dir=Path(cache)),
                        label="pip-audit",
                        env=build_child_env(passthrough_env))
    if run.status == "tool-absent":
        return "tool-absent", _AGG_DEGRADED
    if run.status != "ran":
        return f"pip-audit:{run.status}", _AGG_DEGRADED
    if run.code not in (0, 1):
        # ONLY exit 1 is a valid vulnerability report (findings); any
        # other non-zero (usage / malformed-env / network/service error) is a
        # tool failure -> DEGRADED, never reported as vulnerabilities.
        return "pip-audit:error", _AGG_DEGRADED

    coverage = classify_pip_audit_output(run.stdout)
    builds = survey_local_builds()
    unknown_total = coverage.unknown + builds.unknown + scope.unknown
    print(f"\n[pip-audit] coverage over the {len(coverage.names)} "
          f"distribution(s) THE TOOL ITSELF REPORTED: {_DISPOSITION_SCANNED} "
          f"{coverage.scanned}, VULNERABILITIES {coverage.vulnerabilities}, "
          f"{_DISPOSITION_UNKNOWN} {unknown_total} "
          f"(sources queried: {', '.join(_PINNED_ADVISORY_SOURCES)} -- accepted "
          "non-coverage, NOT evidence of safety).")
    print(f"[pip-audit] {_DISPOSITION_NO_MATCH}: {_NO_MATCH_NOT_OBSERVABLE}.")
    if not coverage.established:
        print(f"[pip-audit] COVERAGE NOT ESTABLISHED -- {coverage.note}",
              file=sys.stderr)
    print(f"[pip-audit] locally-built distributions (editable or VCS): "
          f"{builds.residual}"
          + (f" ({', '.join(builds.residual_names)})" if builds.residual_names
             else "")
          + f"; {builds.unknown} unreadable metadata record(s) count as UNKNOWN."
          " No residual baseline is stored: a baseline derived from one mutable"
          " local environment would make an unrepresentative classification"
          " look like a portable security fact.")

    if coverage.vulnerabilities:
        if run.code == 0:
            print("[pip-audit] EXIT/REPORT CONTRADICTION -- exit 0 accompanied "
                  "a structured report containing vulnerabilities; the report "
                  "is authoritative for the positive finding.", file=sys.stderr)
        return "pip-audit:findings", _AGG_FINDINGS
    if run.code == 1:
        print("[pip-audit] EXIT/REPORT CONTRADICTION -- exit 1 reported "
              "findings but the established structured report contains none; "
              "refusing to classify contradictory evidence.", file=sys.stderr)
        return "pip-audit:contradictory-report", _AGG_DEGRADED
    if not coverage.established or unknown_total:
        return "pip-audit:coverage-unknown", _AGG_INCOMPLETE
    return "pip-audit:clean", _AGG_CLEAN


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def aggregate_tier(tiers: list[int]) -> int:
    """The aggregate is the **worst** tier any pass contributed.

    Precedence is degraded > findings > incomplete > clean, which -- because
    the constants ascend 0 < 5 < 10 < 20 -- is exactly ``max``. Extracted from
    ``main`` so the precedence half of the "aggregate space is unchanged" fence
    is checkable by a test rather than promised: swapping ``max`` for ``min``,
    or for last-tier-wins, changes **no constant** and would otherwise pass
    unnoticed."""
    return max([_AGG_CLEAN, *tiers])


def _banner(text: str) -> None:
    print(f"\n{'=' * (len(text) + 8)}\n=== {text} ===\n{'=' * (len(text) + 8)}")


def parse_pass_env(args: list[str]) -> tuple[str, ...]:
    """Parse ``--pass-env NAME`` / ``--pass-env=NAME`` (repeatable).

    The **only** way a variable outside the closed allowlist reaches a security
    tool. It is an argv decision, taken by the operator, and every name is
    printed in the report -- inheritance is never silent."""
    names: list[str] = []
    for index, arg in enumerate(args):
        if arg == "--pass-env" and index + 1 < len(args):
            names.append(args[index + 1])
        elif arg.startswith("--pass-env="):
            names.append(arg.split("=", 1)[1])
    return tuple(name for name in names if name)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    allow_egress = ("--allow-network" in args)
    passthrough_env = parse_pass_env(args)

    _banner("Cairn python-security self-audit (tripwire, not proof)")
    print(f"interpreter: {sys.executable}\nrepo root:  {_REPO_ROOT}")
    print("Self-audit of a TRUSTED tree only -- not an untrusted-PR reviewer; "
          "a clean result is a tripwire, not a proof.")

    statuses: list[tuple[str, str]] = []
    tiers: list[int] = []

    # SR-1 integrity preflight + installed-state -- DEGRADED short-circuits.
    try:
        lock = load_lockfile()
        integrity_preflight(_REPO_ROOT, lock)
        pkg = validate_python_package(_REPO_ROOT, lock)
    except AuditDegraded as exc:
        print(f"\n[preflight] DEGRADED -- {exc}", file=sys.stderr)
        _banner("summary")
        print("preflight: DEGRADED (fail-closed; no passes ran)")
        return _AGG_DEGRADED
    statuses.append(("preflight", "ok"))
    print(f"\n[preflight] OK -- apparatus verified against the lockfile; "
          f"python_package = {pkg.relative_to(_REPO_ROOT.resolve())}")

    for label, fn in (
        ("injection", lambda: run_injection_pass(_REPO_ROOT, lock)),
        ("bandit", lambda: run_bandit_pass(pkg, _REPO_ROOT)),
        ("adopted-exec", lambda: run_adopted_executable_gate(_REPO_ROOT, lock)),
        ("pip-audit", lambda: run_pip_audit_pass(
            _REPO_ROOT, allow_egress=allow_egress,
            passthrough_env=passthrough_env)),
    ):
        _banner(label)
        try:
            status, tier = fn()
        except AuditDegraded as exc:
            print(f"[{label}] DEGRADED -- {exc}", file=sys.stderr)
            status, tier = f"{label}:degraded", _AGG_DEGRADED
        statuses.append((label, status))
        tiers.append(tier)

    _banner("summary")
    for label, status in statuses:
        print(f"  {label:14s} {status}")
    aggregate = aggregate_tier(tiers)
    tier_name = {_AGG_CLEAN: "CLEAN (tripwire, not proof)",
                 _AGG_INCOMPLETE: "INCOMPLETE COVERAGE -- no findings, but a "
                                  "selected pass did not run (enable it or "
                                  "narrow scope for a clean 0)",
                 _AGG_FINDINGS: "FINDINGS (blocking)",
                 _AGG_DEGRADED: "DEGRADED / UNAVAILABLE / TAMPER"}[aggregate]
    print(f"\naggregate exit {aggregate}: {tier_name}")
    return aggregate


if __name__ == "__main__":
    raise SystemExit(main())
