"""
Cairn-dev-only Bandit gate (P2 Chunk 4, finding I3 + plan-review P3.7).

Runs ``python -m bandit`` over the scaffold + Cairn's scripts and fails
on any HIGH/MEDIUM finding not in a small, rationale'd allowlist.  This
is a **Cairn development dependency only** -- it is never installed into,
or required of, an adopter's repository, so it does not collide with the
stdlib-only invariant the *shipped* scripts (claim_check.py /
lifecycle_metrics.py) hold.

Environment behavior: a missing ``bandit`` ``pytest.skip``s with install
guidance, so a contributor without dev-deps is not blocked.  **Cairn has no
CI**, so the unskippable trigger is not an environment variable -- it is
``python bootstrap/security_check.py``, which fails closed on a missing
``bandit`` unconditionally and refuses this skip outright in release mode.
The ``CI`` / ``GITHUB_ACTIONS`` branch below is dormant provisioning for a CI
that does not exist; see :func:`_in_ci`.  A scanner *error* (rc not in {0,1})
fails closed, before any allowlist filtering.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap._scaffold.install import install_manifest  # noqa: E402
# The derived scan-target set and the Bandit allowlist are single-sourced in
# the release command (bootstrap/security_check.py); the dev gate imports
# them so the two never drift (security-hardening Chunk 2 / R2 + Chunk 7).
from bootstrap.security_check import (  # noqa: E402
    ALLOWLIST as _ALLOWLIST,
    _rel as _rel,
    finding_key as _finding_key,
    is_blocking as _is_blocking,
    scan_targets as _scan_targets,
)

# What used to live here: a `_SEVERITY_RANK` / `_BLOCKING_RANK` pair and a
# second, byte-identical `_rel`. The single-sourcing comment above was true of
# the DATA (`ALLOWLIST`, `scan_targets`) and silent about the PREDICATE -- both
# halves of the key rule were spelled twice, agreeing only by having been
# copied, and sharing a fail-open: an `issue_severity` in neither table read as
# "below MEDIUM", so it was neither blocking here nor liveness-confirming in the
# release command. `is_blocking` / `finding_key` are now imported like the data
# (release-security-orchestration, D4).

#: Declared exclusions from the on-disk oracle below: repo-relative path ->
#: MANDATORY rationale. **Empty today**, and it stays empty: disk and DISTINCT
#: manifest-verbatim sources agree at 52 (``as_of`` 2026-08-10; re-measure
#: rather than carrying this figure forward), so it costs nothing to introduce
#: and fires the moment they disagree. Note the counting rule this table does
#: **not** key on: manifest *rows* are 56, not 52, because
#: api-web-security-modules installs one engine source tree to two destination
#: trees. Rows and distinct files are different questions and only the second
#: one is this oracle's. Mirrors the ``ALLOWLIST`` +
#: ``test_allowlist_entries_have_rationale`` idiom already in this file rather
#: than inventing a second one, and is guarded harder than that idiom: an entry
#: must name a file that exists AND must not name a file the scan already
#: covers (a redundant exclusion is a latch that arms silently -- the
#: subtraction is a no-op until a later coverage regression, at which point it
#: absorbs the very failure this oracle exists to catch).
_SCAN_EXCLUSIONS: dict[str, str] = {}


def _templates_py_on_disk(root: Path) -> set[str]:
    """Every ``.py`` physically present under ``templates/``, repo-relative.

    ``Path.rglob`` does not descend symlinked directories in Python 3.13, so
    "physically present" is glob-scoped rather than filesystem-scoped. That is
    a deliberate choice, not a default: it is kept, and the condition under
    which it and the filesystem agree is asserted by
    ``test_templates_tree_contains_no_symlink`` below."""
    return {
        str(p.relative_to(root))
        for p in (root / "templates").rglob("*.py")
    }


def _unscanned_disk_py(root: Path) -> list[str]:
    """The on-disk ``.py`` files under ``templates/`` the release scan does
    not reach, minus declared exclusions. A helper (rather than an inline
    assertion) so the perturbation tests can call it directly instead of
    catching ``AssertionError``."""
    return sorted(
        _templates_py_on_disk(root)
        - set(_scan_targets())
        - set(_SCAN_EXCLUSIONS)
    )


def _in_ci() -> bool:
    """**Dormant provisioning.** Cairn has NO CI: no workflow file, no runner,
    nothing that sets ``CI`` or ``GITHUB_ACTIONS`` for this suite. This branch
    is provisioning for a CI that does not exist yet, kept so the posture is
    already correct if one is ever added -- it is not a trigger today.

    Today's fail-closed trigger for the Bandit gate is
    ``python bootstrap/security_check.py`` (``run_bandit``), a Maintainer-run
    release command: a missing Bandit is a non-zero exit there, unconditionally,
    with no environment variable involved. The local skip below is deliberate
    and stays -- a contributor without dev-deps is not blocked -- and it is the
    release command, not this variable, that makes the gate unskippable when it
    matters. In release mode (phase 3) the skip itself is refused by
    ``bootstrap/tests/conftest.py``, so it cannot reach a release either way.
    """
    return bool(os.getenv("CI") or os.getenv("GITHUB_ACTIONS"))


def _run_bandit() -> tuple[int, str, str]:
    cmd = [
        sys.executable, "-m", "bandit", "-q", "-f", "json",
        *[str(CAIRN_ROOT / t) for t in _scan_targets()],
    ]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(CAIRN_ROOT), check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def test_no_blocking_security_findings() -> None:
    try:
        rc, stdout, stderr = _run_bandit()
    except FileNotFoundError:
        rc, stdout, stderr = 127, "", "No module named bandit"

    bandit_absent = (
        rc == 127
        or "No module named bandit" in stderr
        or "No module named 'bandit'" in stderr
    )
    if bandit_absent:
        if _in_ci():
            pytest.fail(
                "bandit is not installed but a CI marker is set -- a skipped "
                "security gate is a missing one. Install dev deps "
                "(e.g. pip install bandit)."
            )
        pytest.skip(
            "bandit not installed locally; install it to run the security "
            "gate (pip install bandit). The unskippable trigger is "
            "`python bootstrap/security_check.py`, which fails closed on a "
            "missing bandit and refuses this skip in release mode."
        )

    # Scanner-failure semantics: rc 0 (clean) / 1 (findings) are normal;
    # anything else is a scanner/config error -- fail closed, before any
    # allowlist filtering.
    if rc not in (0, 1):
        pytest.fail(
            f"bandit failed (rc={rc}); allowlist NOT applied.\n"
            f"--- stderr ---\n{stderr}\n--- stdout (head) ---\n{stdout[:1500]}"
        )

    try:
        report = json.loads(stdout)
    except json.JSONDecodeError as exc:
        pytest.fail(f"bandit stdout not JSON (rc={rc}, {exc}):\n{stdout[:1500]}")

    # A file Bandit could not READ is not a file Bandit found clean: it lands
    # in the JSON `errors` array and the run still exits 0. The release command
    # (bootstrap/security_check.py) fails closed on it; the dev gate consumes
    # the same report and had the same hole, so it applies the same rule here
    # -- fixing one and not the other is how the two drift (scan-coverage
    # plan, Chunk A / [I1]).
    scan_errors = report.get("errors") or []
    if scan_errors:
        pytest.fail(
            f"bandit could not scan {len(scan_errors)} requested file(s); "
            "allowlist NOT applied. A file the scanner never opened is not a "
            "file it found clean.\n"
            + "\n".join(
                f"  {_rel(str(e.get('filename', '?')))}: {e.get('reason', '?')}"
                for e in scan_errors
            )
        )

    blocking: list[str] = []
    for f in report.get("results", []) or []:
        if not _is_blocking(f):
            continue
        key = _finding_key(f)
        if key in _ALLOWLIST:
            continue
        blocking.append(
            f"  [{f['test_id']} {f['issue_severity']}] {key[0]}:"
            f"{f['line_number']}  {f['issue_text']}"
        )

    if blocking:
        pytest.fail(
            f"bandit found {len(blocking)} blocking finding(s) "
            f"(severity >= MEDIUM) not in the allowlist:\n"
            + "\n".join(blocking)
            + "\nFix the code or add a rationale'd _ALLOWLIST entry."
        )


def test_allowlist_entries_have_rationale() -> None:
    """Every allowlist entry carries a non-empty rationale -- a
    suppression without a reason is how the discipline rots.

    Vacuous while ``ALLOWLIST`` is empty (it is, since D1's B310 retirement).
    Kept because it costs nothing and fires the moment an entry returns; the
    condition that is *not* vacuous today is liveness, in the release command.
    """
    for key, rationale in _ALLOWLIST.items():
        assert rationale.strip(), f"empty rationale for {key}"


def test_one_predicate_governs_both_allowlist_consumers() -> None:
    """D4. This gate and the release command are the two consumers of one
    ``ALLOWLIST``, and the release command's liveness rule is bound to *its*
    spelling of "blocking". A second spelling here could agree with the filter
    and disagree with liveness -- calling an entry live while suppressing
    nothing, or the reverse.

    So the object identity is the assertion: this module must be *calling the
    release command's functions*, not holding an equivalent copy. Behavioural
    equality would pass for a copy that later drifts, which is exactly the
    failure mode.

    **Identity of the imports is not enough**, and this was measured rather
    than reasoned: re-spelling the severity test *inline at the call site*
    (``f.get("issue_severity") in {"MEDIUM", "HIGH"}``) leaves the imports
    untouched and the namespace clean, and an identity-only version of this
    test stayed green against that mutation. So the gate's own AST is checked
    too."""
    import ast

    from bootstrap import security_check as sc

    assert _is_blocking is sc.is_blocking
    assert _finding_key is sc.finding_key
    assert _rel is sc._rel
    # And no second severity table survives in this module's namespace.
    module = sys.modules[__name__]
    leftovers = [n for n in vars(module)
                 if "SEVERITY" in n.upper() or "BLOCKING_RANK" in n.upper()]
    assert leftovers == [], (
        f"a second severity spelling reappeared in the dev gate: {leftovers}")

    # The call site itself: the gate must DECIDE by calling the imported
    # functions, with no inline re-spelling of severity beside them.
    gate = next(
        node for node in ast.parse(
            Path(__file__).read_text(encoding="utf-8")).body
        if isinstance(node, ast.FunctionDef)
        and node.name == "test_no_blocking_security_findings")
    called = {n.func.id for n in ast.walk(gate)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert {"_is_blocking", "_finding_key"} <= called, (
        f"the gate must decide via the imported predicate and key rule; the "
        f"names it calls are {sorted(called)}")
    inline = [ast.unparse(n) for n in ast.walk(gate)
              if isinstance(n, (ast.Set, ast.List, ast.Tuple, ast.Dict))
              and any(isinstance(c, ast.Constant)
                      and c.value in ("MEDIUM", "HIGH", "LOW")
                      for c in ast.walk(n))]
    assert inline == [], (
        f"an inline severity spelling reappeared at the gate's call site -- "
        f"the imports are single-sourced but the decision is not: {inline}")


def test_every_manifest_verbatim_py_is_scanned_by_some_path() -> None:
    """Every verbatim .py in the published install manifest is reached by
    SOME path in the scanned set, and Cairn's dev executables are covered too.

    **What this pins, and what it does not.** This is a *conformance* check,
    not an anti-drift one: its oracle is ``install_manifest()`` -- the same
    enumeration ``scan_targets()`` now reads -- so a gap that moves both moves
    the difference nowhere. Concretely (measured for the scan-coverage plan):
    delete the manifest union from ``scan_targets()`` and add a hand-written
    ``_SKILLS_MAPPINGS`` loop in its place and this test is still green, so it
    pins "scanned by some path", NOT "consumes the manifest". The guard that
    survives that refactor is the on-disk oracle below
    (``test_every_templates_py_on_disk_is_release_scanned``), whose oracle the
    subject never reads."""
    targets = set(_scan_targets())
    shipped = {
        f"templates/{src}"
        for src, _dst, verbatim in install_manifest(modules=None)
        if verbatim and src.endswith(".py")
    }
    assert shipped, "expected at least one verbatim .py reference script"
    missing = shipped - targets
    assert not missing, f"shipped scripts not scanned: {sorted(missing)}"
    for dev in ("bootstrap/scaffold.py", "scripts/check_cairn.py",
                # content_scan moved to the content-security module (single
                # source); it is now covered via the verbatim derivation.
                "templates/modules/team-gated/content_scan.py"):
        assert dev in targets, dev
    # No bare directory target (the no-`-r` footgun) -- every target is a file.
    for t in _scan_targets():
        assert t.endswith(".py"), f"non-file scan target: {t}"


_SKILLS_PY = (
    "templates/skills/_lib/lifecycle.py",
    "templates/skills/_lib/lifecycle_planner.py",
)


def test_every_templates_py_on_disk_is_release_scanned() -> None:
    """The durable guard: an oracle the code under test does not read.

    ``scan_targets()`` performs no filesystem read under ``templates/`` -- it
    joins strings from registry data and globs only ``scripts/``,
    ``bootstrap/`` and ``bootstrap/_scaffold/``. So the working tree under
    ``templates/`` is a channel the subject never consumes, which is what makes
    this an ANTI-DRIFT check where its manifest-derived sibling above is only a
    conformance one. Under a real perturbation (a delivery registry stops
    shipping a file that is still on disk) the sibling stays green and this
    goes red naming the file.

    **The oracle's boundary, stated rather than assumed.** It holds only while
    every delivery registry sources from under ``templates/`` (true as of the
    scan-coverage plan, 2026-08-03). A future registry sourcing from elsewhere
    ships code this test cannot see, and no mechanism here would say so."""
    on_disk = _templates_py_on_disk(CAIRN_ROOT)
    # (a) Non-emptiness: empty-minus-anything is empty, so a missing or renamed
    #     templates/ would make every assertion below vacuously true.
    assert on_disk, "no .py found under templates/ -- the oracle is vacuous"
    # (b) The claim itself.
    unscanned = _unscanned_disk_py(CAIRN_ROOT)
    assert unscanned == [], (
        "shipped .py present on disk but NOT release-scanned:\n  "
        + "\n  ".join(unscanned)
        + "\nEither extend scan_targets() or add a rationale'd "
          "_SCAN_EXCLUSIONS entry -- do not leave it unscanned."
    )
    # (c) The reverse direction: a manifest row naming a file absent from disk
    #     is a scan target Bandit cannot open. security_check fails closed on
    #     Bandit's `errors` array; this surfaces it here too, independently.
    manifest_py = {
        f"templates/{src}"
        for src, _dst, verbatim in install_manifest(modules=None)
        if verbatim and src.endswith(".py")
    }
    ghosts = sorted(manifest_py - on_disk)
    assert not ghosts, f"manifest rows naming files absent from disk: {ghosts}"
    # (d) An exclusion cannot outlive the file it excuses, and cannot be
    #     silent about why.
    for path, rationale in _SCAN_EXCLUSIONS.items():
        assert (CAIRN_ROOT / path).is_file(), (
            f"_SCAN_EXCLUSIONS names a file that no longer exists: {path}")
        assert rationale.strip(), f"empty _SCAN_EXCLUSIONS rationale for {path}"
    # (e) The other half of stale, and it does NOT follow from (d): an entry
    #     that is on disk, rationale'd AND already scanned passes (a)-(d)
    #     unchanged while the subtraction is a no-op -- until coverage for that
    #     file later regresses, at which point the entry silently absorbs it.
    #     A redundant exclusion is deleted, not left as a latch.
    redundant = sorted(set(_SCAN_EXCLUSIONS) & set(_scan_targets()))
    assert not redundant, (
        "_SCAN_EXCLUSIONS entries the scan already covers -- delete them; "
        f"left in place they latch a future coverage regression: {redundant}"
    )


def test_templates_py_count_is_pinned() -> None:
    """A growth tripwire, and the antidote to a fail-open exclusion table: the
    shipped .py surface cannot grow without a human looking at it. Same posture
    as ``assert scanned == 9`` for the always-on group in
    ``bootstrap/tests/test_upgrade_side_door_parity.py``."""
    on_disk = _templates_py_on_disk(CAIRN_ROOT)
    assert len(on_disk) == 52, (
        f"expected 52 .py under templates/, found {len(on_disk)} -- if this "
        "moved intentionally, update BOTH this pin and its sibling in "
        "bootstrap/tests/test_notice_install.py "
        "(test_manifest_has_the_expected_py_source_count) in the SAME commit. "
        "**The two no longer move to the same number, and must not be made to "
        "agree**: this pin counts DISTINCT .py files on disk, that one counts "
        "manifest ROWS, and api-web-security-modules installs one four-member "
        "engine tree to two destinations -- so 6 new files are 6 here and 10 "
        "there (52 vs 56). Moved 44 -> 45 by portable-security-sweeps "
        "Chunk A (run_portable_security_sweeps.py); moved 45 -> 46 by "
        "security-verification-activation Chunk A "
        "(run_security_verification.py); moved 46 -> 52 by "
        "api-web-security-modules (two facades + four engine members)."
    )


def test_templates_tree_contains_no_symlink() -> None:
    """Enforces the ``recurse_symlinks`` decision the on-disk oracle rests on
    rather than inheriting it as a default. ``Path.rglob`` does not descend
    symlinked directories in Python 3.13, so "physically present under
    templates/" is glob-scoped, not filesystem-scoped. The choice is to keep
    the default and assert the condition under which the two agree."""
    links = sorted(
        str(p.relative_to(CAIRN_ROOT))
        for p in (CAIRN_ROOT / "templates").rglob("*")
        if p.is_symlink()
    )
    assert not links, (
        "symlink(s) under templates/ -- the on-disk oracle globs without "
        f"descending them, so code behind these is unscanned: {links}"
    )


def test_the_on_disk_oracle_goes_red_when_a_registry_stops_delivering(monkeypatch) -> None:
    """Proves the oracle is not decoration: with a delivery registry patched to
    stop shipping the two session-lifecycle tools, the files stay on disk and
    the oracle names exactly them.

    **The patch target is load-bearing.** ``bootstrap/_scaffold/install.py``
    binds ``_SKILLS_MAPPINGS`` BY VALUE at import (``from ... import
    _SKILLS_MAPPINGS``), so patching ``bootstrap._scaffold.config`` -- the
    module that *defines* it -- is a silent no-op and this test would pass
    without perturbing anything. Patch the module that *reads* it. The same
    narrowest-owning-module rule for these trust anchors is documented in
    ``bootstrap/tests/test_scaffold_substrate.py``
    (``test_trust_anchor_imports_are_owner_specific_not_runtime_isolated``)."""
    import bootstrap._scaffold.install as install_mod

    stripped = tuple(
        row for row in install_mod._SKILLS_MAPPINGS
        if not row[0].endswith(".py")
    )
    assert len(stripped) == len(install_mod._SKILLS_MAPPINGS) - 2, (
        "expected exactly two .py rows in _SKILLS_MAPPINGS to strip")
    monkeypatch.setattr(install_mod, "_SKILLS_MAPPINGS", stripped)

    assert _unscanned_disk_py(CAIRN_ROOT) == list(_SKILLS_PY)


def test_a_templates_py_no_registry_delivers_is_reported_unscanned(tmp_path, monkeypatch) -> None:
    """A live delivery registry that never reaches the install manifest --
    ``_OPTIONAL_TEMPLATES`` is today's instance -- would ship a .py the
    manifest-derived guard cannot see. The on-disk oracle catches it, which is
    why no hand-maintained registry census is needed."""
    import bootstrap.security_check as sc

    (tmp_path / "templates" / "optional").mkdir(parents=True)
    (tmp_path / "templates" / "optional" / "rogue.py").write_text(
        "x = 1\n", encoding="utf-8")
    monkeypatch.setattr(sc, "CAIRN_ROOT", tmp_path)

    assert _unscanned_disk_py(tmp_path) == ["templates/optional/rogue.py"]


def test_the_two_session_lifecycle_tools_are_scanned_by_name() -> None:
    """Belt to the oracle's braces: this specific 63-day miss cannot recur
    silently even if the derivation is later refactored. Two path literals
    typed by a human -- no shared derivation with the subject."""
    targets = set(_scan_targets())
    for path in _SKILLS_PY:
        assert path in targets, path


def test_scan_targets_recurses_the_scaffold_engine_package(tmp_path, monkeypatch) -> None:
    """RR3/S4 (scaffold-split 0A.1): when the post-split engine package exists,
    EVERY .py under bootstrap/_scaffold/ is scanned recursively (the engine's
    guts can't fall out of the release Bandit gate), while bootstrap/tests/
    (intentional attack fixtures) stays excluded. A no-op until Stage 0B creates
    the package; this exercises the capability now against a throwaway tree."""
    import bootstrap.security_check as sc

    (tmp_path / "scripts").mkdir()
    (tmp_path / "bootstrap" / "_scaffold" / "sub").mkdir(parents=True)
    (tmp_path / "bootstrap" / "scaffold.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "bootstrap" / "_scaffold" / "engine.py").write_text("y = 1\n", encoding="utf-8")
    (tmp_path / "bootstrap" / "_scaffold" / "sub" / "deep.py").write_text("z = 1\n", encoding="utf-8")
    (tmp_path / "bootstrap" / "tests").mkdir()
    (tmp_path / "bootstrap" / "tests" / "attack_fixture.py").write_text("evil = 1\n", encoding="utf-8")
    monkeypatch.setattr(sc, "CAIRN_ROOT", tmp_path)

    targets = set(sc.scan_targets())
    assert "bootstrap/_scaffold/engine.py" in targets
    assert "bootstrap/_scaffold/sub/deep.py" in targets, "recursion must reach nested modules"
    assert "bootstrap/scaffold.py" in targets
    assert "bootstrap/tests/attack_fixture.py" not in targets, "attack fixtures must stay excluded"
