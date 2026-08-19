#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""quality_gate.py -- consolidated pre-release quality-gate suite.

Sibling of ``scripts/check_cairn.py``: where ``check_cairn`` runs the
*every-commit* link / claim integrity gate, ``quality_gate`` runs the
*pre-cut + on-demand* deeper sweep.  Both stdlib-only.

Three sub-gates, dispatched via ``--sub <name>`` (default: all):

* **order-independence** (D-3) -- the test suite must pass under
  pytest collection-shuffling for a configured set of deterministic
  seeds.  Catches test interdependencies that hide under a stable
  alphabetical collection order.  Shuffling uses an in-tree
  ``conftest.py`` hook (stdlib ``random.Random``), so the sub-gate
  has zero external-dependency surface.

* **neutrality** (E-4) -- scan ``cairn/{doctrine,dimensions,bootstrap,
  scripts,on-ramp,docs,examples}/`` for vendor/project tokens (Claude,
  Codex, modflow_tools, ...) that don't belong in vendor-neutral
  framework prose.  Three sanctioned-exception directives keep the
  legitimate cases auditable: ``<!-- vendor-ok: reason -->`` exempts
  the same line or the line below; ``<!-- vendor-ok-begin: reason -->``
  / ``<!-- vendor-ok-end -->`` exempt a block; ``<!-- case-study -->``
  inside ``cairn/case-studies/`` exempts a whole file.  Exemption
  directives are **forbidden inside ``cairn/templates/``** (they
  would ship to adopters and silently propagate vendor leaks).

* **redundancy** (G R1 + R6) -- detect doc passages with high
  n-gram overlap (R1 shingle / Jaccard) and Python defs that no
  static reference exercises (R6 stdlib AST walk).  Both surface
  candidates for human disposition in
  ``doctrine/consolidation-review.md``.  R7 (capability necessity)
  and R1's layer-contract filter stay manual -- they need judgment
  the gate cannot honestly mechanize.

Usage::

    python scripts/quality_gate.py                       # run all sub-gates
    python scripts/quality_gate.py --sub neutrality      # one sub-gate
    python scripts/quality_gate.py --sub order-independence --seed-count 3
    python scripts/quality_gate.py --report              # machine-readable
    python scripts/quality_gate.py --root <dir>          # override repo root

Exit codes: ``0`` clean; ``1`` at least one ``fail`` finding;
``2`` usage error.

The sub-gates are intentionally heterogeneous in implementation
(pytest invocation wrapper, regex denylist scan, n-gram overlap +
AST walk), unified at the CLI + report surface.
Each sub-gate's failure mode is independent: a
neutrality regression does not block a redundancy report, and
vice versa.
"""
from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# Import the R6 whitelist as a sibling module by file path so the
# CLI can be invoked from any cwd without a package context.
import importlib.util as _importlib_util

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parent

_whitelist_spec = _importlib_util.spec_from_file_location(
    "_quality_gate_unused_def_whitelist",
    _HERE / "quality_gate_unused_def_whitelist.py",
)
assert _whitelist_spec is not None and _whitelist_spec.loader is not None
_whitelist_mod = _importlib_util.module_from_spec(_whitelist_spec)
_whitelist_spec.loader.exec_module(_whitelist_mod)
_UNUSED_DEF_WHITELIST: frozenset[str] = _whitelist_mod.WHITELIST


# ---------------------------------------------------------------------------
# Findings + report shape
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """One quality-gate finding.

    ``severity == "fail"`` contributes to the non-zero exit code;
    ``severity == "info"`` is reported but does not fail the gate
    (used for exemption-audit lines and the order-independence
    seed-echo summary).
    """

    sub_gate: str       # "order-independence" | "neutrality" | "redundancy"
    severity: str       # "fail" | "info"
    file: str           # repo-relative path; "" for sub-gate-level findings
    line: int           # 1-based; 0 if N/A
    message: str


@dataclass
class GateReport:
    """The cumulative result of one or more sub-gate runs."""

    findings: list[Finding] = field(default_factory=list)

    def add(self, *fs: Finding) -> None:
        self.findings.extend(fs)

    @property
    def failed(self) -> bool:
        return any(f.severity == "fail" for f in self.findings)

    def by_sub(self) -> dict[str, list[Finding]]:
        out: dict[str, list[Finding]] = defaultdict(list)
        for f in self.findings:
            out[f.sub_gate].append(f)
        return dict(out)


# ===========================================================================
# Sub-gate 1: order-independence (D-3)
# ===========================================================================
#
# Thin pytest-invocation wrapper.  The shuffle hook lives in
# ``cairn/bootstrap/tests/conftest.py`` (stdlib only); the sub-gate
# shells out to pytest with a ``--quality-gate-shuffle-seed=<int>``
# arg per requested seed and asserts each invocation passes.
#
# The seed contract (per plan-review finding #2):
#   * default seed list = ``[0]`` (one deterministic baseline run)
#   * ``--seed N``         -- override with a single seed
#   * ``--seed-count N``   -- run seeds ``[0, 1, ..., N-1]``
#   * ``--seed-list a,b,c`` -- explicit list (escape hatch)
# Every run echoes the exact seed used; first-failure reports its
# seed so the failure is reproducible.

_DEFAULT_TEST_DIR = "bootstrap/tests"


def _run_order_independence(
    seeds: list[int], repo_root: Path, test_dir: str,
) -> list[Finding]:
    """Run ``pytest <test_dir> --quality-gate-shuffle-seed=<seed>``
    for each seed; return one Finding per seed (severity ``fail`` on
    a non-zero pytest exit, ``info`` on a clean run).
    """
    findings: list[Finding] = []
    tests_path = (repo_root / test_dir).resolve()
    for seed in seeds:
        cmd = [
            sys.executable, "-m", "pytest", str(tests_path),
            f"--quality-gate-shuffle-seed={seed}",
            "-q", "--no-header", "--no-summary",
        ]
        # subprocess.run is the boundary; pytest's own exit code is
        # the contract here (no parsing of stdout for finding shape).
        proc = subprocess.run(
            cmd, cwd=str(repo_root), capture_output=True, text=True,
        )
        if proc.returncode == 0:
            findings.append(Finding(
                "order-independence", "info", test_dir, 0,
                f"seed={seed}: PASS",
            ))
        else:
            # First-failure summary lives in pytest's stderr; surface
            # the seed and the first 40 lines of stderr.
            err_head = "\n".join(proc.stderr.splitlines()[:40])
            findings.append(Finding(
                "order-independence", "fail", test_dir, 0,
                f"seed={seed}: pytest exit {proc.returncode}\n{err_head}",
            ))
    return findings


# ===========================================================================
# Sub-gate 2: neutrality (E-4)
# ===========================================================================
#
# Scan ``cairn/{doctrine,dimensions,bootstrap,scripts,on-ramp,docs,
# examples}/`` for vendor / project tokens.  Templates/ is scanned
# only for the directive-forbidden gate (any directive there is a
# leak risk).  Three sanctioned-exception directives keep audit
# trails surfaceable.

# Last updated: 2026-05-28.  Adding a vendor / model name: include
# it here and (when convenient) attach a brief Cairn-side commit
# message naming the vendor-launch / new-name signal that prompted
# the update.
_VENDOR_DENYLIST: frozenset[str] = frozenset({
    "Claude", "Codex",
    "Anthropic", "OpenAI", "Google", "DeepMind", "Microsoft", "Meta",
    "Gemini", "GPT", "Llama", "LLaMA",
    "Antigravity", "Cursor",
})
_PROJECT_DENYLIST: frozenset[str] = frozenset({
    "modflow_tools", "LHM",
})
_ALL_NEUTRALITY_TOKENS = _VENDOR_DENYLIST | _PROJECT_DENYLIST

_NEUTRALITY_SCAN_ROOTS = (
    "doctrine", "dimensions", "bootstrap", "scripts",
    "on-ramp", "docs", "examples",
)

_VENDOR_OK_BEGIN_RE = re.compile(
    r"<!--\s*vendor-ok-begin:\s*(?P<reason>.+?)\s*-->"
)
_VENDOR_OK_END_RE = re.compile(r"<!--\s*vendor-ok-end\s*-->")
_VENDOR_OK_LINE_RE = re.compile(
    r"<!--\s*vendor-ok:\s*(?P<reason>.*?)\s*-->"
)
_CASE_STUDY_RE = re.compile(r"<!--\s*case-study\s*-->")
_ANY_DIRECTIVE_RE = re.compile(
    r"<!--\s*(?:vendor-ok|vendor-ok-begin|vendor-ok-end|case-study)"
)


def _is_directive_only_line(line: str) -> bool:
    """True when *line* consists of only an HTML comment (after
    leading/trailing whitespace).  A directive-only line on the line
    above a token is what exempts that token (the line-exemption
    rule).  A directive appearing inside prose is NOT directive-only
    and does not exempt anything by itself.
    """
    stripped = line.strip()
    return stripped.startswith("<!--") and stripped.endswith("-->")


def _scan_neutrality_file(
    path: Path, repo_root: Path,
) -> list[Finding]:
    """Return the neutrality findings for one file.

    Templates path: scans only for the directive-forbidden rule.
    Outside templates: scans for unsanctioned vendor / project
    tokens, with line / block / file exemption directives applied.
    """
    rel = path.relative_to(repo_root).as_posix()
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    findings: list[Finding] = []

    # Rule: ANY exemption directive inside cairn/templates/ fails the
    # gate (those files ship to adopters and would propagate leaks).
    # AFTER the directive check, continue scanning for vendor / project
    # tokens -- since exemption directives are forbidden in templates,
    # any vendor token there is itself a fail (there's no honest way to
    # exempt it).  Returning early after the directive check would
    # silently let a token leak through unexamined.
    if rel.startswith("templates/"):
        for lineno, line in enumerate(lines, start=1):
            if _ANY_DIRECTIVE_RE.search(line) and _is_directive_only_line(line):
                findings.append(Finding(
                    "neutrality", "fail", rel, lineno,
                    "exemption directive forbidden inside cairn/templates/ "
                    "(templates ship to adopters; a leak would propagate)",
                ))
            # Scan the line for vendor / project tokens -- no exemption
            # path applies in templates, so any token is a fail.
            if _is_directive_only_line(line):
                continue  # directive lines carry no prose tokens
            for token in sorted(_ALL_NEUTRALITY_TOKENS):
                if re.search(rf"\b{re.escape(token)}\b", line):
                    findings.append(Finding(
                        "neutrality", "fail", rel, lineno,
                        f"unsanctioned vendor/project token `{token}` in "
                        f"cairn/templates/ (no exemption path; templates "
                        f"must stay clean by construction)",
                    ))
        return findings

    # Rule: <!-- case-study --> outside cairn/case-studies/ fails
    # (cannot silence prose elsewhere via a misplaced marker).
    # A case-study mention inside prose (backticks / mid-sentence) is
    # documentation of the syntax, not a live marker -- require the
    # whole line to be a directive-only HTML comment.
    case_study_exempt = False
    for lineno, line in enumerate(lines, start=1):
        if _CASE_STUDY_RE.search(line) and _is_directive_only_line(line):
            if rel.startswith("case-studies/"):
                case_study_exempt = True
            else:
                findings.append(Finding(
                    "neutrality", "fail", rel, lineno,
                    "case-study marker outside cairn/case-studies/ "
                    "(cannot exempt non-case-study files)",
                ))
    if case_study_exempt:
        # Whole-file exemption; record as info and stop scanning.
        findings.append(Finding(
            "neutrality", "info", rel, 1,
            "case-study (whole-file exemption)",
        ))
        return findings

    # Block-exemption + line-exemption + denylist scan.
    #
    # Block markers (vendor-ok-begin / vendor-ok-end) require the line
    # to be a directive-only HTML comment.  A vendor-ok-begin shown
    # mid-prose (inside backticks in a how-to doc) is documentation of
    # the syntax, not a live marker -- consistent with the
    # "shown-in-prose-not-parsed" rule the existing claim_check.py
    # directive surfaces apply.
    block_active = False
    block_reason = ""
    block_open_line = 0
    for lineno, line in enumerate(lines, start=1):
        directive_only = _is_directive_only_line(line)
        # Block-begin / block-end management (handle same-line edge
        # case too, though unusual: vendor-ok-begin and
        # vendor-ok-end on the same line collapse to a zero-width
        # block, exempting only that single line).
        m_begin = _VENDOR_OK_BEGIN_RE.search(line) if directive_only else None
        m_end = _VENDOR_OK_END_RE.search(line) if directive_only else None
        if m_begin and m_end:
            reason = m_begin.group("reason").strip()
            if not reason:
                findings.append(Finding(
                    "neutrality", "fail", rel, lineno,
                    "vendor-ok-begin: empty rationale (rationale required)",
                ))
            findings.append(Finding(
                "neutrality", "info", rel, lineno,
                f'vendor-ok (inline block) "{reason}"',
            ))
            continue
        if m_begin:
            reason = m_begin.group("reason").strip()
            if not reason:
                findings.append(Finding(
                    "neutrality", "fail", rel, lineno,
                    "vendor-ok-begin: empty rationale (rationale required)",
                ))
            block_active = True
            block_reason = reason
            block_open_line = lineno
            findings.append(Finding(
                "neutrality", "info", rel, lineno,
                f'vendor-ok-begin "{reason}"',
            ))
            continue
        if m_end:
            if not block_active:
                findings.append(Finding(
                    "neutrality", "fail", rel, lineno,
                    "vendor-ok-end without matching vendor-ok-begin",
                ))
            else:
                block_active = False
                block_reason = ""
            continue

        # Line-exemption: vendor-ok: REASON.  Applies if the
        # directive is on THIS line, OR on the line above AS A
        # DIRECTIVE-ONLY LINE (so a vendor-ok in mid-prose does NOT
        # silently exempt the next line of prose).
        line_exempt_reason: str | None = None
        m_line = _VENDOR_OK_LINE_RE.search(line)
        if m_line and not _VENDOR_OK_BEGIN_RE.search(line):
            reason = m_line.group("reason").strip()
            if not reason:
                findings.append(Finding(
                    "neutrality", "fail", rel, lineno,
                    "vendor-ok: empty rationale (rationale required)",
                ))
            line_exempt_reason = reason or "<empty>"
        if line_exempt_reason is None and lineno >= 2:
            prev = lines[lineno - 2]
            if (
                _VENDOR_OK_LINE_RE.search(prev)
                and not _VENDOR_OK_BEGIN_RE.search(prev)
                and _is_directive_only_line(prev)
            ):
                m_prev = _VENDOR_OK_LINE_RE.search(prev)
                # The above-line directive applies to THIS line.
                line_exempt_reason = (
                    m_prev.group("reason").strip() or "<empty>"
                ) if m_prev else None

        # Token scan.
        for token in sorted(_ALL_NEUTRALITY_TOKENS):
            # Skip directive-bearing comments to avoid double-flagging.
            # (A line that IS a directive doesn't carry prose tokens.)
            if _is_directive_only_line(line):
                continue
            if not re.search(rf"\b{re.escape(token)}\b", line):
                continue
            if block_active:
                findings.append(Finding(
                    "neutrality", "info", rel, lineno,
                    f'token `{token}` in vendor-ok-block "{block_reason}"',
                ))
            elif line_exempt_reason is not None:
                findings.append(Finding(
                    "neutrality", "info", rel, lineno,
                    f'token `{token}` exempted "{line_exempt_reason}"',
                ))
            else:
                findings.append(Finding(
                    "neutrality", "fail", rel, lineno,
                    f"unsanctioned vendor/project token `{token}`",
                ))

    if block_active:
        findings.append(Finding(
            "neutrality", "fail", rel, block_open_line,
            "orphan vendor-ok-begin without matching vendor-ok-end "
            f'(rationale "{block_reason}")',
        ))

    return findings


#: Per-root file-suffix scope for the neutrality lint.  Doctrine
#: prose and config templates carry vendor / project tokens that
#: would be real leaks; code legitimately names the reference
#: deployment in test fixtures, docstrings, and comments and is NOT
#: scanned.  ``templates/`` is the exception: every file under
#: ``templates/`` (including .py reference scripts) is scanned for the
#: directive-forbidden rule, since those files ship to adopter trees
#: and a leak would propagate.
_NEUTRALITY_FILE_SUFFIXES: dict[str, tuple[str, ...]] = {
    "doctrine": (".md",),
    "dimensions": (".md",),
    "on-ramp": (".md",),
    "docs": (".md",),
    "examples": (".md", ".yml", ".yaml"),
    "bootstrap": (".md",),  # BOOTSTRAP.md, SAFETY.md, etc.  Not bootstrap/tests/
    "scripts": (".md",),    # rare; scripts/*.md if any, NOT .py code
    "templates": (".md", ".yml", ".yaml", ".py", ".toml"),
}


def _walk_neutrality_files(repo_root: Path) -> list[Path]:
    """Yield the file paths the neutrality sub-gate scans.

    Doctrine + config files in the seven roots are scanned for
    vendor / project tokens; every file under ``templates/`` is
    scanned for the directive-forbidden rule (templates ship to
    adopters).  Code files (``.py``) outside ``templates/`` are NOT
    scanned -- test fixtures and docstrings legitimately name the
    reference deployment.
    """
    files: list[Path] = []
    for root, suffixes in _NEUTRALITY_FILE_SUFFIXES.items():
        d = repo_root / root
        if not d.is_dir():
            continue
        for path in d.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix in suffixes:
                files.append(path)
    return sorted(files)


def _run_neutrality(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in _walk_neutrality_files(repo_root):
        findings.extend(_scan_neutrality_file(path, repo_root))
    return findings


# ===========================================================================
# Sub-gate 3: redundancy (G R1 + R6)
# ===========================================================================
#
# R1 -- n-gram overlap detector across the .md corpus.  Two
# passages with shingle-Jaccard above the threshold surface as a
# candidate pair for human disposition (see
# doctrine/consolidation-review.md).
#
# R6 -- stdlib AST walk: for each .py file under cairn/scripts,
# cairn/bootstrap, and cairn/templates/modules/, collect top-level
# function / class names and all referenced names; flag any def
# whose name is never referenced (and not in the whitelist file).

_DEFAULT_SHINGLE_SIZE = 5
_DEFAULT_JACCARD_THRESHOLD = 0.75
_R1_SCAN_ROOTS = ("doctrine", "dimensions", "on-ramp", "docs")
#: R6 scans production code under these roots only.  ``bootstrap/tests/``
#: is excluded because pytest discovers test classes / functions by
#: name pattern (``Test*`` / ``test_*``), not by static reference --
#: scanning it would generate a wall of false positives on every
#: test class.  When code-review work surfaces an additional R6
#: false-positive class, add to ``_UNUSED_DEF_WHITELIST`` rather than
#: expanding this list.
_R6_SCAN_ROOTS = (
    "scripts", "bootstrap", "templates/modules",
)
_R6_EXCLUDE_DIRS = ("bootstrap/tests",)


def _word_shingles(text: str, size: int) -> set[tuple[str, ...]]:
    """Return the set of N-word shingles in *text*.

    Lower-cases + word-tokenizes; punctuation is discarded.  A
    document shorter than *size* words yields an empty set (it
    cannot meaningfully overlap on a per-shingle basis).
    """
    words = re.findall(r"[\w']+", text.lower())
    if len(words) < size:
        return set()
    return {tuple(words[i:i + size]) for i in range(len(words) - size + 1)}


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def _run_r1_redundancy(
    repo_root: Path, shingle_size: int, jaccard_threshold: float,
) -> list[Finding]:
    """Scan .md corpus for high-overlap passage pairs.

    Returns one **info** finding per surfaced pair (severity info,
    not fail: R1 surfaces candidates for human disposition per the
    consolidation-review doctrine; it does not adjudicate).
    """
    findings: list[Finding] = []
    files: list[tuple[str, set]] = []
    for root in _R1_SCAN_ROOTS:
        d = repo_root / root
        if not d.is_dir():
            continue
        for path in sorted(d.rglob("*.md")):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            shingles = _word_shingles(text, shingle_size)
            if shingles:
                files.append((path.relative_to(repo_root).as_posix(), shingles))
    for i, (a_rel, a_sh) in enumerate(files):
        for b_rel, b_sh in files[i + 1:]:
            j = _jaccard(a_sh, b_sh)
            if j >= jaccard_threshold:
                findings.append(Finding(
                    "redundancy", "info", a_rel, 0,
                    f"R1 overlap with {b_rel}: Jaccard={j:.2f} "
                    f"(shingle={shingle_size}, threshold>={jaccard_threshold:.2f})",
                ))
    return findings


def _collect_py_defs_and_refs(
    path: Path,
) -> tuple[list[tuple[str, int]], set[str]]:
    """Return ``([(name, lineno), ...], referenced_names)`` for one
    .py file.  Defs are top-level function / class definitions; refs
    are every ``ast.Name`` / ``ast.Attribute`` *target* name and every
    ``from X import Y`` imported symbol name seen anywhere in the file
    (including its own body, so a recursive helper counts as
    referenced).
    """
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except (OSError, SyntaxError):
        return [], set()
    defs: list[tuple[str, int]] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defs.append((node.name, node.lineno))
    refs: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            refs.add(node.id)
        elif isinstance(node, ast.Attribute):
            refs.add(node.attr)
        elif isinstance(node, ast.ImportFrom):
            # `from X import Y` binds Y as a reference to the def named
            # Y in module X.  The alias nodes are neither Name nor
            # Attribute, so without this branch a def whose only
            # in-corpus reference is a package-facade re-export reads
            # as dead.  `alias.name` only, not `alias.asname`: the def
            # being matched is named `alias.name`, and the local
            # rebinding is already an ast.Name at every use site.
            for alias in node.names:
                refs.add(alias.name)
        elif isinstance(node, ast.Call):
            # Direct ast.Name calls are already captured above; this
            # branch is here to make the intent explicit.
            pass
    return defs, refs


def _run_r6_redundancy(repo_root: Path) -> list[Finding]:
    """Stdlib AST unreferenced-def scan.

    For each .py file in the R6 scan roots, collect top-level def
    names + every referenced name in the *combined* corpus; flag
    each def name that the corpus never references AND is not in
    the whitelist.  This is a within-corpus check: a def used only
    by external callers via the file's CLI entry point (the
    ``__main__`` guard) is still seen as referenced because
    ``main`` is a referenced name in that guard.
    """
    files: list[Path] = []
    for root in _R6_SCAN_ROOTS:
        d = repo_root / root
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*.py")):
            rel = p.relative_to(repo_root).as_posix()
            if any(rel.startswith(ex + "/") or rel == ex
                   for ex in _R6_EXCLUDE_DIRS):
                continue
            files.append(p)
    all_defs: list[tuple[Path, str, int]] = []
    all_refs: set[str] = set()
    for path in files:
        defs, refs = _collect_py_defs_and_refs(path)
        for name, lineno in defs:
            all_defs.append((path, name, lineno))
        all_refs |= refs
    findings: list[Finding] = []
    for path, name, lineno in all_defs:
        if name in all_refs:
            continue
        if name in _UNUSED_DEF_WHITELIST:
            continue
        # Dunder methods on a class are referenced implicitly; skip.
        if name.startswith("__") and name.endswith("__"):
            continue
        # Pytest-discovery patterns (defense-in-depth -- the scan
        # excludes bootstrap/tests/ already, but a misplaced test file
        # under scripts/ or bootstrap/ outside tests/ would otherwise
        # trip on these patterns).
        if name.startswith("Test") or name.startswith("test_"):
            continue
        # Private helpers can be referenced in tests we don't scan
        # here; surface as info, not fail, so this stays informative
        # rather than hostile to common patterns.
        sev = "info" if name.startswith("_") else "fail"
        findings.append(Finding(
            "redundancy", sev,
            path.relative_to(repo_root).as_posix(), lineno,
            f"R6 def `{name}` is never referenced in the scanned "
            f"corpus (add to whitelist if it's a static-dispatch "
            f"target like an argparse callback, or delete it)",
        ))
    return findings


def _run_redundancy(
    repo_root: Path, shingle_size: int, jaccard_threshold: float,
) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(_run_r1_redundancy(repo_root, shingle_size, jaccard_threshold))
    findings.extend(_run_r6_redundancy(repo_root))
    return findings


# ===========================================================================
# Sub-gate dispatch + CLI
# ===========================================================================


_SUB_GATES = ("order-independence", "neutrality", "redundancy")


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="quality_gate",
        description=(
            "Consolidated Cairn quality-gate suite "
            "(order-independence + neutrality + redundancy)."
        ),
    )
    p.add_argument(
        "--root", type=Path, default=_REPO_ROOT,
        help=f"Repo root for path resolution. Default: {_REPO_ROOT}.",
    )
    p.add_argument(
        "--sub", action="append", choices=list(_SUB_GATES), default=None,
        help=(
            "Run a single sub-gate (repeatable). "
            f"Choices: {', '.join(_SUB_GATES)}. Default: run all."
        ),
    )
    p.add_argument(
        "--report", action="store_true",
        help="Emit a machine-readable report (one finding per line, "
             "TAB-separated: sub_gate\\tseverity\\tfile\\tline\\tmessage).",
    )
    # Order-independence seed contract.
    p.add_argument(
        "--seed", type=int, default=None,
        help="Order-independence: single seed for the shuffle hook.",
    )
    p.add_argument(
        "--seed-count", type=int, default=None,
        help="Order-independence: run seeds 0, 1, ..., N-1.",
    )
    p.add_argument(
        "--seed-list", type=str, default=None,
        help="Order-independence: comma-separated explicit seed list.",
    )
    p.add_argument(
        "--test-dir", type=str, default=_DEFAULT_TEST_DIR,
        help=f"Order-independence: test directory. Default: {_DEFAULT_TEST_DIR}.",
    )
    # R1 tuning.
    p.add_argument(
        "--shingle-size", type=int, default=_DEFAULT_SHINGLE_SIZE,
        help=f"R1 shingle word size. Default: {_DEFAULT_SHINGLE_SIZE}.",
    )
    p.add_argument(
        "--jaccard-threshold", type=float, default=_DEFAULT_JACCARD_THRESHOLD,
        help=f"R1 Jaccard threshold. Default: {_DEFAULT_JACCARD_THRESHOLD}.",
    )
    return p


def _resolve_seeds(args: argparse.Namespace) -> list[int]:
    """Resolve the seed list from the CLI args.

    Precedence: ``--seed-list`` > ``--seed-count`` > ``--seed`` >
    default ``[0]``.  Returns a list (possibly with one element).
    """
    if args.seed_list is not None:
        return [int(s.strip()) for s in args.seed_list.split(",") if s.strip()]
    if args.seed_count is not None:
        return list(range(int(args.seed_count)))
    if args.seed is not None:
        return [int(args.seed)]
    return [0]


def _print_report(
    report: GateReport, sub_gates: list[str], machine: bool,
) -> None:
    """Emit *report* on stdout.  Human format (default) prints a
    per-sub-gate header for every sub-gate that ran (whether or not
    it surfaced findings), then lists fails + infos.  Machine
    format emits TAB-separated one-per-line tuples for downstream
    tooling.
    """
    if machine:
        # Machine-mode contract: one finding per line, TAB-separated
        # (sub_gate, severity, file, line, message).  Multi-line
        # messages (e.g. order-independence failure echoes the first
        # 40 lines of pytest stderr) are flattened with `\\n` escapes
        # so downstream line-oriented tooling can parse cleanly.  A
        # consumer that wants the original line shape can replace
        # `\\n` -> newline.
        for f in report.findings:
            flat = f.message.replace("\\", "\\\\").replace("\n", "\\n")
            print(
                f"{f.sub_gate}\t{f.severity}\t{f.file}\t{f.line}\t{flat}"
            )
        return
    by = report.by_sub()
    print("Cairn quality_gate report")
    print("=" * 40)
    for sub in _SUB_GATES:
        if sub not in sub_gates:
            continue
        sub_findings = by.get(sub, [])
        fails = [f for f in sub_findings if f.severity == "fail"]
        infos = [f for f in sub_findings if f.severity == "info"]
        print(f"\n[{sub}]  fail={len(fails)}  info={len(infos)}")
        if not sub_findings:
            print("  (no findings)")
            continue
        for f in fails:
            where = f"{f.file}:{f.line}" if f.line else f.file or "(global)"
            print(f"  FAIL  {where}: {f.message}")
        for f in infos:
            where = f"{f.file}:{f.line}" if f.line else f.file or "(global)"
            print(f"  info  {where}: {f.message}")


def run_gates(
    sub_gates: list[str], repo_root: Path, *,
    seeds: list[int] | None = None,
    test_dir: str = _DEFAULT_TEST_DIR,
    shingle_size: int = _DEFAULT_SHINGLE_SIZE,
    jaccard_threshold: float = _DEFAULT_JACCARD_THRESHOLD,
) -> GateReport:
    """Run *sub_gates* against *repo_root* and return the report.

    Public entry point for tests; the CLI ``main`` wraps this.
    """
    report = GateReport()
    if "order-independence" in sub_gates:
        report.add(*_run_order_independence(
            seeds if seeds is not None else [0],
            repo_root, test_dir,
        ))
    if "neutrality" in sub_gates:
        report.add(*_run_neutrality(repo_root))
    if "redundancy" in sub_gates:
        report.add(*_run_redundancy(
            repo_root, shingle_size, jaccard_threshold,
        ))
    return report


def main(argv: list[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        print(
            f"quality_gate: --root is not a directory: {args.root}",
            file=sys.stderr,
        )
        return 2
    sub_gates = list(args.sub) if args.sub else list(_SUB_GATES)
    seeds = _resolve_seeds(args)
    report = run_gates(
        sub_gates, args.root,
        seeds=seeds,
        test_dir=args.test_dir,
        shingle_size=args.shingle_size,
        jaccard_threshold=args.jaccard_threshold,
    )
    _print_report(report, sub_gates, machine=args.report)
    return 1 if report.failed else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
