#!/usr/bin/env python3
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
   ``.py`` files this install adopted (RV3; binary provenance is out of scope).

Self-audit scope (read this first)
----------------------------------

This is a drift / content-injection tripwire on the adopter's **own trusted
tree**, run in the adopter's own CI or dev loop. The apparatus *and its policy
inputs* are trusted input: committed, reviewed-as-code, integrity-covered. It
is **not** a reviewer for untrusted code that can modify the apparatus itself.
**Do not wire it into untrusted-PR / fork CI** -- a run from an attacker's
checkout executes the attacker's audit. A clean result is **a tripwire, not a
proof**.

Aggregate exit table (P1 #3 -- a DISTINCT space; never collides with a
component's 0/1/2/3 or 127). Each component's raw outcome is printed
separately; the aggregate is the worst tier, precedence degraded > findings >
clean:

* ``0``  -- clean: every applicable pass ran and found nothing blocking
  (content-scan *advisory* findings may be present; they are printed and do
  NOT fail the aggregate).
* ``10`` -- FINDINGS: bandit or pip-audit found issues, or the adopted-
  executable gate flagged a file. Blocking.
* ``20`` -- DEGRADED / UNAVAILABLE / TAMPER: a pass could not be trusted to
  run -- integrity preflight failed, ``python_package`` is missing/invalid, a
  selected content-scan returned scan-failure (2) or stale (3), a required
  tool was absent, or pip-audit was required but unavailable. Dominates 10.

The injection pass being NOT-APPLICABLE (content-security not installed) is
printed loudly as its own line; it never silently reads as a clean scan.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent
_LOCKFILE = _REPO_ROOT / "dev" / ".cairn" / "cairn-lock.yml"
_RUNNER = _HERE / "content_scan_runner.py"

# Aggregate exit tiers (distinct from component 0/1/2/3 / 127).
_AGG_CLEAN = 0
_AGG_FINDINGS = 10
_AGG_DEGRADED = 20

# The apparatus + policy files whose lockfile-integrity the SR-1 preflight
# checks (relative to the repo root). Only those actually recorded in the
# lockfile are checked; a recorded-but-mismatched file fails closed.
_APPARATUS_DSTS = (
    "scripts/content_scan.py",
    "scripts/content_scan_runner.py",
    "scripts/content_scan_roots.txt",
    "scripts/content_scan_residuals.txt",
    "scripts/content_scan_allowlist.txt",
    "scripts/run_security_audit.py",
)


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

def integrity_preflight(repo_root: Path, lock: dict) -> None:
    """Verify the apparatus + policy files against their lockfile hashes.

    This is the standalone, stdlib reimplementation of the lockfile-integrity
    check scoped to the security apparatus (Cairn's own ``verify_integrity`` is
    an engine tool, not shipped to adopters). Any apparatus file that is
    present but whose on-disk hash does not match its lockfile record -- or a
    recorded file missing on disk -- fails closed (DEGRADED): a self-audit must
    not run from a tampered apparatus and report results.
    """
    by_dst = {rec.get("dst"): rec for rec in lock.get("files", [])}
    checked = 0
    for dst in _APPARATUS_DSTS:
        rec = by_dst.get(dst)
        if rec is None:
            continue  # not part of this install (e.g. content-security absent)
        abs_p = repo_root / dst
        if abs_p.is_symlink() or not abs_p.is_file():
            raise AuditDegraded(
                f"apparatus file {dst!r} is recorded in the lockfile but "
                "missing / not a regular file on disk (tamper)")
        want = str(rec.get("hash", ""))
        got = "sha256:" + _sha256_hex(abs_p.read_bytes())
        if want != got:
            raise AuditDegraded(
                f"apparatus file {dst!r} does not match its lockfile hash "
                "(tamper / drift); refusing to self-audit from an unverified "
                "apparatus")
        checked += 1
    if not checked:
        raise AuditDegraded(
            "no security-apparatus files are lockfile-recorded; cannot run a "
            "verified self-audit (is this an installed Cairn tree?)")


# --------------------------------------------------------------------------
# P2 #5 -- single contained python_package validation
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


def _run_tool(argv: list[str], *, label: str, cwd: Path) -> tuple[int, str]:
    """Run a tool with a trusted boundary: ``shell=False``, a fixed argument
    vector, a neutral working directory off the candidate import path, and
    ``capture_output``. Returns ``(exit, status)``; a missing tool is 127
    (loud). The interpreter / cwd are recorded as audit evidence."""
    try:
        proc = subprocess.run(  # noqa: S603 -- fixed argv, shell=False, no input
            argv, cwd=str(cwd), shell=False,
            capture_output=True, text=True,
        )
    except FileNotFoundError:
        print(f"[{label}] NOT INSTALLED in the active interpreter "
              f"({sys.executable}); cannot run this pass.", file=sys.stderr)
        return 127, "tool-absent"
    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    return proc.returncode, "ran"


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
    """Content-scan pass, gated on authoritative installed state (P1 #4).

    Returns ``(status, tier_contribution)``. content-security NOT in the
    installed roster -> ``("not-applicable", 0)`` (printed loudly, never a
    silent clean). Selected but the runner is absent -> DEGRADED. Selected +
    present -> the runner's 0/1/2/3 mapped to a tier (advisory findings (1)
    contribute 0; scan-failure (2) / stale (3) contribute DEGRADED)."""
    if "content-security" not in lock.get("modules", []):
        print("\n[injection] NOT APPLICABLE -- content-security is not an "
              "installed module; the injection pass did NOT run (this is not a "
              "clean scan).")
        return "not-applicable", _AGG_CLEAN
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
    argv = [sys.executable, "-m", "bandit", "-r", "-q",
            *_safe_target_args([pkg])]
    code, status = _run_tool(argv, label="bandit", cwd=repo_root)
    if status == "tool-absent":
        return "tool-absent", _AGG_DEGRADED
    if code == 0:
        return "bandit:clean", _AGG_CLEAN
    if code == 1:
        return "bandit:findings", _AGG_FINDINGS
    return "bandit:error", _AGG_DEGRADED


def run_adopted_executable_gate(repo_root: Path, lock: dict) -> tuple[str, int]:
    """RV3 -- the Cairn-adopted-executable **source gate**: confirm every ``.py``
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


def run_pip_audit_pass(repo_root: Path, *, allow_egress: bool) -> tuple[str, int]:
    """pip-audit over the active interpreter's pip-visible distributions.

    Network egress is OPT-IN (Imp #5 / SR-5): unconfigured runs do NOT egress.
    Without ``--allow-network`` (or ``CAIRN_PIP_AUDIT_ALLOW_NETWORK=1``)
    pip-audit runs against its local cache only; a denied / offline / failed
    lookup is reported **unavailable, not clean**. Audits the *active
    interpreter's pip distributions only* -- conda-managed and
    locked-but-not-installed deps are documented blind spots; findings are
    advisory."""
    if not allow_egress:
        print("\n[pip-audit] network egress OFF (default). Re-run with "
              "--allow-network to enable the remote CVE lookup; package names "
              "+ versions (only) would then be sent to pip-audit's "
              "vulnerability service. Skipping the remote lookup -- reporting "
              "UNAVAILABLE, not clean.", file=sys.stderr)
        return "egress-off-unavailable", _AGG_CLEAN
    if shutil.which("pip-audit") is None and \
            importlib.util.find_spec("pip_audit") is None:
        print("\n[pip-audit] NOT INSTALLED -- dependency CVE pass unavailable.",
              file=sys.stderr)
        return "tool-absent", _AGG_DEGRADED
    argv = [sys.executable, "-m", "pip_audit"]
    code, status = _run_tool(argv, label="pip-audit", cwd=repo_root)
    if status == "tool-absent":
        return "tool-absent", _AGG_DEGRADED
    if code == 0:
        return "pip-audit:clean", _AGG_CLEAN
    return "pip-audit:findings", _AGG_FINDINGS


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def _banner(text: str) -> None:
    print(f"\n{'=' * (len(text) + 8)}\n=== {text} ===\n{'=' * (len(text) + 8)}")


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    allow_egress = ("--allow-network" in args)

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
        ("pip-audit", lambda: run_pip_audit_pass(_REPO_ROOT,
                                                 allow_egress=allow_egress)),
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
    aggregate = max([_AGG_CLEAN, *tiers])
    tier_name = {_AGG_CLEAN: "CLEAN (tripwire, not proof)",
                 _AGG_FINDINGS: "FINDINGS (blocking)",
                 _AGG_DEGRADED: "DEGRADED / UNAVAILABLE / TAMPER"}[aggregate]
    print(f"\naggregate exit {aggregate}: {tier_name}")
    return aggregate


if __name__ == "__main__":
    raise SystemExit(main())
