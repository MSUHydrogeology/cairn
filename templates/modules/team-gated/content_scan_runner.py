#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""content_scan runner -- the adopter's self-audit advisory pass.

Decomposed, **standard-library-only** wrapper around ``content_scan.py``: it
resolves the deterministic audited text set, runs the scanner over it
in-process, compares each flag against a reviewed-residual baseline as a
multiset, and reports a fail-closed ``0/1/2/3`` exit. It is the content-scan
half of the security stack -- the Python ``run_security_audit.py`` orchestrator
(the ``python-security`` module) composes this pass with ``pip-audit`` + bandit;
this file runs standalone with no dev dependency, so a non-Python adopter still
gets the injection tripwire.

**Self-audit scope (read this first).** This is a drift / content-injection
tripwire on the adopter's **own trusted tree**, run in the adopter's own CI or
dev loop. The scanner *and its policy inputs* (this runner, ``content_scan.py``,
the allowlist, the reviewed-residual baseline, the audited-roots manifest, and
their lockfile records) are **trusted input**: committed, reviewed-as-code,
integrity-covered. It is **not** a reviewer for untrusted code that can modify
the apparatus itself. **Do not wire it into untrusted-PR / fork CI** -- a run
from an attacker's checkout executes the attacker's scanner. A clean result is
**a tripwire, not a proof** (see ``dev/modules/security-review.md`` > v1 scope).

Exit contract
-------------

* ``0`` -- clean: scanned a non-empty set, no flags.
* ``1`` -- tripwire findings surfaced; **advisory** (a composing orchestrator
  does NOT fail its aggregate on this alone -- a human-review signal).
* ``2`` -- the scan could not be trusted to have run: git unavailable, an
  empty / unresolvable audited set, a missing / malformed audited-roots
  manifest, a missing / sentinel-less reviewed baseline, a containment
  violation (symlink / escape), or a resource-budget breach. **Fails closed**
  -- "did not actually scan" must never read as "clean".
* ``3`` -- **STALE baseline authority**: a reviewed-residual entry has no live
  occurrence (it could preauthorize a replay). A distinct fail-closed class.

Audited set (P1 #2 -- the audited-roots manifest)
-------------------------------------------------

The roots come from an explicit, adopter-owned manifest
(``content_scan_roots.txt``), NOT a hardcoded list or a shell glob. The
manifest is repo-relative + containment-checked (no absolute paths, no ``..``
escape, no symlink escape, no option-shaped leading ``-``), ships with required
Cairn defaults plus project extensions, and is **itself in the audited set** (a
hostile edit to it is scanned). Git is resolved once outside the candidate tree
and invoked with ambient ``GIT_*`` steering removed, inert execution-bearing
config, literal pathspecs, and an option terminator. A missing / empty /
unresolvable required-root manifest fails closed (exit 2). The runner makes
**no profile-derived-completeness claim**: it scans exactly what the manifest
names.

URL-detector role boundary
--------------------------

``suspicious-url`` is enabled for instruction and unknown roles. Only the
known discussion roots ``dev/**`` and ``docs/**`` disable it; a new, misspelled
or otherwise unclassified path therefore defaults to the stricter posture.
Other detectors remain enabled everywhere. One residual is accepted and stated
plainly: a bare hostile URL in known discussion prose is detected by neither
``suspicious-url`` nor ``egress`` because egress requires a supported transfer
verb near the destination. This trusted-tree scanner is a human-review tripwire,
not a proof that prose is safe.
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent
_CONTENT_SCAN = _HERE / "content_scan.py"
_ROOTS_MANIFEST = _HERE / "content_scan_roots.txt"
_RESIDUAL_BASELINE = _HERE / "content_scan_residuals.txt"

_AUDIT_TEXT_EXTS = (".md", ".txt")
_DISCUSSION_ROOTS = frozenset({"dev", "docs"})

# Documented, NARROW exclusions (P1 #2): the vendored base-cache (scanned
# upstream in Cairn) and frozen archives. The live, project-authored
# instruction surface is never excluded.
_AUDIT_TEXT_EXCLUDE_PREFIXES = ("dev/.cairn/base/",)
_AUDIT_TEXT_EXCLUDE_SEGMENTS = ("/archive/",)

# --- Resource budgets (Important #4) --------------------------------------
# Hostile agent-loaded text must not turn the required check into an
# availability failure that *skips* or reads clean. A per-file or aggregate
# breach is a distinct LOUD failure (exit 2), never a skip.
_MAX_FILE_BYTES = 8 * 1024 * 1024          # 8 MiB per file
_MAX_TOTAL_BYTES = 128 * 1024 * 1024       # 128 MiB across the audited set
_MAX_WALL_SECONDS = 120.0                  # whole-run wall-clock ceiling

# The Git query decides which repository bytes are scanned. Its environment is
# therefore an input boundary, not harmless ambience: GIT_DIR outranks `-C` and
# can redirect `ls-files` to another repository. Keep only the host minimum,
# then put back the Git controls this launcher deliberately owns.
_GIT_ENV_NAMES = frozenset({
    "PATH", "HOME", "LANG", "TMPDIR", "TEMP", "TMP",
    "SYSTEMROOT", "SystemRoot", "COMSPEC", "PATHEXT", "USERPROFILE",
    "APPDATA", "LOCALAPPDATA",
})
_GIT_CONFIG = (
    ("core.useReplaceRefs", "false"),
    ("core.hooksPath", os.devnull),
    ("core.fsmonitor", "false"),
    ("core.quotePath", "false"),
    ("diff.external", ""),
    ("core.pager", "cat"),
)
_GIT_TIMEOUT_SECONDS = 60


class AuditError(Exception):
    """A fail-closed condition that maps to exit 2 (the scan cannot be
    trusted to have run)."""


# --------------------------------------------------------------------------
# Audited-roots manifest (P1 #2)
# --------------------------------------------------------------------------

_ROOTS_SENTINEL = "# content-scan-roots v1"
_ROOTS_SENTINEL_RE = re.compile(r"^#\s*content-scan-roots\s+v(\d+)\s*$")


def load_audit_roots(manifest_path: Path = _ROOTS_MANIFEST,
                     repo_root: Path = _REPO_ROOT) -> list[tuple[str, bool]]:
    """Parse the audited-roots manifest -> ``(repo-relative root, required)``.

    Each non-comment line is one repo-relative path (a file or a directory). A
    leading ``!`` marks the root **required** (P1 #5): a required root that is
    absent or contributes no tracked text is a coverage gap that fails the scan
    (enforced in :func:`audited_text_files`); an unmarked root is optional
    (scanned when present, silently absent otherwise). Validated fail-closed:
    the canonical sentinel must head the file; a root must not be absolute, must
    not contain a ``..`` segment, and must resolve *inside* the repo (no symlink
    escape). A missing / sentinel-less / empty / containment-violating manifest
    raises :class:`AuditError` (exit 2). Returns entries in file order.
    """
    try:
        text = manifest_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise AuditError(
            f"audited-roots manifest is missing: {manifest_path}") from exc
    except OSError as exc:
        raise AuditError(
            f"audited-roots manifest is unreadable: {exc}") from exc

    nonblank = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not nonblank or nonblank[0] != _ROOTS_SENTINEL:
        if nonblank and _ROOTS_SENTINEL_RE.match(nonblank[0]):
            raise AuditError(
                f"audited-roots manifest has an unsupported sentinel "
                f"{nonblank[0]!r}; only the exact {_ROOTS_SENTINEL!r} is "
                "accepted (no parser migration for other versions yet)")
        raise AuditError(
            "audited-roots manifest missing its canonical sentinel header "
            f"(first non-blank line must be exactly {_ROOTS_SENTINEL!r})")

    repo_resolved = repo_root.resolve()
    roots: list[tuple[str, bool]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        entry = line.split("#", 1)[0].strip()
        if not entry:
            continue
        required = entry.startswith("!")
        rel = entry[1:].strip() if required else entry
        if not rel:
            continue
        p = Path(rel)
        if p.is_absolute() or ".." in p.parts or rel.startswith("-"):
            raise AuditError(
                f"audited root {rel!r} is not a contained repo-relative path "
                "(absolute, contains '..', or begins with '-' and could be "
                "parsed as a Git option)")
        # Containment: the (possibly non-existent) target must resolve inside
        # the repo. A symlinked root that points outside is rejected here.
        resolved = (repo_resolved / p).resolve()
        if resolved != repo_resolved and repo_resolved not in resolved.parents:
            raise AuditError(
                f"audited root {rel!r} resolves outside the repo root "
                f"({resolved}) -- refusing (symlink / escape)")
        roots.append((rel, required))
    if not roots:
        raise AuditError(
            "audited-roots manifest declares no roots (an empty audited set "
            "is a failure, not a clean pass)")
    return roots


# --------------------------------------------------------------------------
# Audited file set (git-tracked, contained, budget-checked)
# --------------------------------------------------------------------------

def _git_child_env() -> dict[str, str]:
    """Closed environment for the audited-set Git query.

    Every ambient ``GIT_*`` value is absent; only the controls below are put
    back. Other names are admitted by an explicit host-minimum allowlist rather
    than inherited wholesale.
    """
    env = {
        name: value for name, value in os.environ.items()
        if name in _GIT_ENV_NAMES or name.startswith("LC_")
    }
    env.update({
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_OPTIONAL_LOCKS": "0",
    })
    return env


def _resolve_git(repo_root: Path) -> Path:
    """Resolve the operator's Git once; validate shape and containment only.

    This is not provenance authentication. Package-manager symlinks are fine
    when their resolved target is an executable regular file outside the tree
    being scanned.
    """
    found = shutil.which("git", path=os.environ.get("PATH"))
    if not found:
        raise AuditError("git is unavailable on the operator PATH")
    lexical = Path(found)
    if not lexical.is_absolute():
        raise AuditError(f"git resolved to a non-absolute path: {found!r}")
    try:
        resolved = lexical.resolve(strict=True)
        repo_resolved = repo_root.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise AuditError(f"git or repository path could not be resolved: {exc}") from exc
    if resolved == repo_resolved or repo_resolved in resolved.parents:
        raise AuditError(
            f"git resolves inside the repository under scan ({resolved}); "
            "candidate-tree content may not choose the executable")
    if not resolved.is_file() or not os.access(resolved, os.X_OK):
        raise AuditError(
            f"git at {resolved} is not an executable regular file")
    return resolved


def _git_tracked(repo_root: Path, roots: list[str],
                 git_executable: Path | None = None) -> list[str]:
    git = _resolve_git(repo_root) if git_executable is None else git_executable
    argv = [str(git), "--literal-pathspecs"]
    for key, value in _GIT_CONFIG:
        argv.extend(("-c", f"{key}={value}"))
    argv.extend(("-C", str(repo_root), "ls-files", "-z", "--", *roots))
    try:
        proc = subprocess.run(
            argv, capture_output=True, text=True, check=False,
            env=_git_child_env(), timeout=_GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise AuditError(
            f"git ls-files over the audited roots failed ({exc!r}); cannot "
            "resolve a trustworthy audited set") from exc
    if proc.returncode != 0:
        detail = (proc.stderr or "").strip()[:500]
        raise AuditError(
            f"git ls-files over the audited roots exited {proc.returncode} "
            f"({detail or 'no diagnostic'}); cannot resolve a trustworthy "
            "audited set")
    return [rel for rel in proc.stdout.split("\0") if rel]


def audited_text_files(repo_root: Path = _REPO_ROOT,
                       manifest_path: Path = _ROOTS_MANIFEST) -> list[Path]:
    """The deterministic audited text surface: git-tracked ``.md`` / ``.txt``
    under the manifest roots, plus the manifest itself, minus the documented
    exclusions, each contained (no symlink / escape) and within the per-file
    byte budget. Raises :class:`AuditError` (exit 2) on any untrustworthy
    condition, including a resolved-empty set.
    """
    root_entries = load_audit_roots(manifest_path, repo_root)
    roots = [rel for rel, _req in root_entries]
    required_roots = [rel for rel, req in root_entries if req]
    repo_resolved = repo_root.resolve()
    git_executable = _resolve_git(repo_root)
    print(f"content_scan: Git executable {git_executable} (shape and "
          "containment validated; provenance not authenticated).")

    def _passes_filters(rel: str) -> bool:
        if not rel.endswith(_AUDIT_TEXT_EXTS):
            return False
        if any(rel.startswith(p) for p in _AUDIT_TEXT_EXCLUDE_PREFIXES):
            return False
        if any(seg in ("/" + rel) for seg in _AUDIT_TEXT_EXCLUDE_SEGMENTS):
            return False
        return True

    # The roots' OWN contribution decides the empty-set failure: if the named
    # roots resolve to zero tracked text files, the scan did not actually scan
    # the declared surface -> fail closed (exit 2). This is checked BEFORE the
    # manifest self-add, so manifest-self-inclusion cannot mask empty roots.
    root_rels = {
        rel for rel in _git_tracked(repo_root, roots, git_executable)
        if _passes_filters(rel)
    }

    # P1 #5: every REQUIRED root must be present AND contribute >= 1 tracked
    # text file. A missing or empty required root silently shrinks coverage --
    # fail closed, naming the gap. (A file-root contributes itself; a dir-root
    # contributes anything beneath it.)
    for req in required_roots:
        prefix = req.rstrip("/") + "/"
        if not any(r == req or r.startswith(prefix) for r in root_rels):
            raise AuditError(
                f"required audited root {req!r} is absent or contributes no "
                "tracked .md/.txt file -- refusing (a missing required root "
                "silently reduces coverage; fix the tree or the manifest)")

    if not root_rels:
        raise AuditError(
            "the audited roots resolved to zero tracked text files -- an empty "
            "audited set is a failure, not a clean pass (the scanner did not "
            "actually scan the declared surface)")
    tracked = set(root_rels)
    # The manifest is itself in the audited set (P1 #2): a hostile edit to the
    # roots file must be scanned. Add it (when tracked under the repo) on top of
    # the roots' contribution.
    try:
        manifest_rel = str(manifest_path.resolve().relative_to(repo_resolved))
        if manifest_rel in set(_git_tracked(
                repo_root, [manifest_rel], git_executable)):
            tracked.add(manifest_rel)
    except ValueError:
        pass  # manifest outside the repo (unusual); roots-only set

    files: list[Path] = []
    for rel in sorted(tracked):
        if not _passes_filters(rel):
            continue
        abs_p = repo_root / rel
        # Per-file containment (Important #3): reject symlinks and non-regular
        # files, and confirm the real path stays inside the repo. A tracked
        # symlink beneath a valid root that points at a secret / huge file
        # outside the repo is refused here, not followed.
        if abs_p.is_symlink():
            raise AuditError(
                f"audited path {rel!r} is a symlink; refusing to follow it "
                "(containment)")
        if not abs_p.is_file():
            continue
        resolved = abs_p.resolve()
        if repo_resolved not in resolved.parents:
            raise AuditError(
                f"audited path {rel!r} resolves outside the repo root "
                f"({resolved}) -- refusing (containment)")
        try:
            size = abs_p.stat().st_size
        except OSError as exc:
            raise AuditError(f"cannot stat audited path {rel!r}: {exc}") from exc
        if size > _MAX_FILE_BYTES:
            raise AuditError(
                f"audited path {rel!r} is {size} bytes, over the per-file "
                f"budget ({_MAX_FILE_BYTES}); refusing (resource budget)")
        files.append(abs_p)

    if not files:
        raise AuditError(
            "the audited set resolved to zero files -- an empty set is a "
            "failure, not a clean pass (the scanner did not actually scan)")
    total = sum(p.stat().st_size for p in files)
    if total > _MAX_TOTAL_BYTES:
        raise AuditError(
            f"audited set totals {total} bytes, over the aggregate budget "
            f"({_MAX_TOTAL_BYTES}); refusing (resource budget)")
    return files


# --------------------------------------------------------------------------
# Reviewed-residual baseline (multiset trust anchor)
# --------------------------------------------------------------------------

_FINGERPRINT_RE = re.compile(r"^[^\s#]+:[a-z][a-z0-9-]*:[0-9a-f]{12}$")
_BASELINE_SENTINEL = "# content-scan-residual-baseline v1"
_BASELINE_SENTINEL_RE = re.compile(
    r"^#\s*content-scan-residual-baseline\s+v(\d+)\s*$")


def _flag_fingerprint(repo_root: Path, rel: str, line_no: int,
                      pattern_id: str) -> str:
    try:
        line = (repo_root / rel).read_text(
            encoding="utf-8", errors="replace").splitlines()[line_no - 1]
    except (OSError, IndexError):
        line = ""
    code_hash = hashlib.sha256(line.strip().encode("utf-8")).hexdigest()[:12]
    return f"{rel}:{pattern_id}:{code_hash}"


def _parse_baseline_text(text: str):
    counts: Counter = Counter()
    bad: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fp = line.split("#", 1)[0].strip()
        if _FINGERPRINT_RE.match(fp):
            counts[fp] += 1
        else:
            bad.append(line)
    return counts, bad


def load_residual_baseline_checked(path: Path = _RESIDUAL_BASELINE):
    """Availability-checked load -> ``(ok, Counter, reason)``.

    The reviewed baseline is the trust anchor separating NEW from known; its
    unavailability is an execution failure, not an advisory pass. Missing /
    unreadable / malformed / sentinel-less -> ``ok=False`` (exit 2). A
    deliberately-empty baseline is supported ONLY as a present file whose first
    non-blank line is exactly the canonical sentinel, matched by exact equality
    (an unsupported version fails closed, never a silent reinterpretation)."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return False, Counter(), f"reviewed baseline file is missing: {path}"
    except OSError as exc:
        return False, Counter(), f"reviewed baseline is unreadable: {exc}"
    nonblank = [ln.strip() for ln in text.splitlines() if ln.strip()]
    sentinel_shaped = [ln for ln in nonblank if _BASELINE_SENTINEL_RE.match(ln)]
    if not nonblank or nonblank[0] != _BASELINE_SENTINEL:
        if nonblank and _BASELINE_SENTINEL_RE.match(nonblank[0]):
            return (False, Counter(),
                    f"reviewed baseline has an unsupported sentinel "
                    f"{nonblank[0]!r}; only {_BASELINE_SENTINEL!r} is accepted")
        return (False, Counter(),
                "reviewed baseline missing its canonical sentinel header "
                f"(first non-blank line must be exactly {_BASELINE_SENTINEL!r})")
    if len(sentinel_shaped) != 1:
        return (False, Counter(),
                f"reviewed baseline has {len(sentinel_shaped)} sentinel-shaped "
                "lines (exactly one required)")
    counts, bad = _parse_baseline_text(text)
    if bad:
        return (False, counts,
                f"reviewed baseline has {len(bad)} malformed entr(y/ies); "
                f"first: {bad[0]!r}")
    return True, counts, ""


# --------------------------------------------------------------------------
# The scan
# --------------------------------------------------------------------------

def _scan_urls_for_adopter_rel(rel: str) -> bool:
    """Whether *rel* receives the strict URL detector in an adopter tree.

    The exception is deliberately narrower than the enabled class: only known
    discussion roots disable URL scanning. Everything else, including an
    unknown role, a typo such as ``doc/``, the roots manifest, and root-level
    instruction files, stays enabled. This mapping is adopter-layout-specific;
    Cairn's source-tree caller correctly keeps its separate ``templates/**``
    classifier.
    """
    parts = Path(rel).parts
    return not parts or parts[0] not in _DISCUSSION_ROOTS

def _load_content_scan():
    spec = importlib.util.spec_from_file_location("content_scan", _CONTENT_SCAN)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def run_content_scan(files: list[Path], repo_root: Path = _REPO_ROOT,
                     baseline_path: Path = _RESIDUAL_BASELINE,
                     deadline: float | None = None):
    """In-process injection scan over ``files``, compared as a multiset against
    the reviewed baseline.

    Returns ``(exit, all_flags, new_flags, stale)`` -- ``0`` clean / ``1``
    advisory findings / ``2`` scan failure or baseline unavailable / ``3``
    STALE baseline authority. ``deadline`` is an absolute ``time.monotonic``
    ceiling, checked **before and after each file** -- a COOPERATIVE budget
    (P2 #6): it cannot interrupt a single pathological file mid-scan (that would
    need a killable subprocess; out of v1 scope), but a one-file overrun is
    caught on the post-file check and fails closed (exit 2) rather than
    completing and reporting clean. Exceeding it is a resource-budget failure.

    URL scanning is disabled only for known ``dev/**`` and ``docs/**``
    discussion prose. Unknown roles fail closed to URL scanning enabled. The
    accepted bare-URL prose blind spot is stated in the module contract above.
    """
    baseline_ok, baseline, why = load_residual_baseline_checked(baseline_path)
    if not baseline_ok:
        print(f"content_scan: BASELINE UNAVAILABLE -- {why}. Failing the audit "
              "rather than treating every flag as advisory-NEW.", file=sys.stderr)
        return 2, [], [], []

    def _over_budget() -> bool:
        if deadline is not None and time.monotonic() > deadline:
            print("content_scan: WALL-CLOCK BUDGET EXCEEDED -- refusing "
                  "(cooperative resource budget); a partial / overrun scan must "
                  "not read clean.", file=sys.stderr)
            return True
        return False

    try:
        cs = _load_content_scan()
        allow = cs.load_url_allowlist()
        all_flags = []
        for p in files:
            if _over_budget():                       # before the file
                return 2, [], [], []
            rel = str(p.relative_to(repo_root))
            for fl in cs.scan_file(
                    p, scan_urls=_scan_urls_for_adopter_rel(rel),
                    url_allowlist=allow):
                fp = _flag_fingerprint(repo_root, rel, fl.line, fl.pattern_id)
                all_flags.append((rel, fl, fp))
            if _over_budget():                       # after the file (P2 #6)
                return 2, [], [], []
    except Exception as exc:  # noqa: BLE001 -- ANY scan error is a failure
        print(f"content_scan: SCAN FAILED ({exc!r}) -- treating as a scanner "
              "failure (exit 2).", file=sys.stderr)
        return 2, [], [], []

    current = Counter(fp for _r, _fl, fp in all_flags)
    seen: Counter = Counter()
    new_flags = []
    for rel, fl, fp in all_flags:
        seen[fp] += 1
        if seen[fp] > baseline.get(fp, 0):
            new_flags.append((rel, fl, fp))
    stale = sorted(
        (fp, baseline[fp] - current.get(fp, 0))
        for fp in baseline if baseline[fp] > current.get(fp, 0)
    )
    if stale:
        return 3, all_flags, new_flags, stale
    if all_flags:
        return 1, all_flags, new_flags, stale
    return 0, all_flags, new_flags, stale


def audit(repo_root: Path = _REPO_ROOT,
          manifest_path: Path = _ROOTS_MANIFEST,
          baseline_path: Path = _RESIDUAL_BASELINE):
    """Resolve the audited set and scan it. Returns
    ``(exit, files, all_flags, new_flags, stale)``. Any fail-closed condition
    in set resolution becomes exit 2 with an empty result."""
    deadline = time.monotonic() + _MAX_WALL_SECONDS
    try:
        files = audited_text_files(repo_root, manifest_path)
    except AuditError as exc:
        print(f"content_scan: AUDITED-SET FAILURE -- {exc} (exit 2).",
              file=sys.stderr)
        return 2, [], [], [], []
    code, all_flags, new_flags, stale = run_content_scan(
        files, repo_root, baseline_path, deadline=deadline)
    return code, files, all_flags, new_flags, stale


def _print_summary(code: int, files, all_flags, new_flags, stale) -> None:
    """Info #7: every output surface carries the audited-set identity, the
    trusted-apparatus identity, and the tripwire-not-proof qualifier. Never a
    bare PASS."""
    print(
        f"content_scan runner: scanned {len(files)} audited text file(s) "
        f"from {_ROOTS_MANIFEST.name}; apparatus = {_CONTENT_SCAN.name} + "
        f"{_RESIDUAL_BASELINE.name}.")
    print("This is a TRIPWIRE, NOT A PROOF: a clean result means the known "
          "patterns did not fire over the audited set, not that the content "
          "is safe. Self-audit of a trusted tree only -- not an untrusted-PR "
          "reviewer.")
    if code == 0:
        print("result: clean (no flags). Tripwire, not proof -- see above.")
    elif code == 1:
        print(f"result: {len(all_flags)} flag(s), {len(new_flags)} NEW -- "
              "ADVISORY (human-review tripwire, not a gate).")
        for rel, fl, _fp in new_flags:
            print(f"  NEW {rel}:{fl.line}: [{fl.pattern_id}] {fl.message}",
                  file=sys.stderr)
    elif code == 3:
        print(f"result: STALE baseline authority ({len(stale)} entr(y/ies)) "
              "-- FAILS (prune the residual baseline).", file=sys.stderr)
        for fp, surplus in stale:
            print(f"  STALE {fp} (x{surplus} no longer present)", file=sys.stderr)
    else:
        print("result: scan could not be trusted to have run -- FAILS "
              "(see the error above).", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    code, files, all_flags, new_flags, stale = audit()
    _print_summary(code, files, all_flags, new_flags, stale)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
