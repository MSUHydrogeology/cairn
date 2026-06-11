#!/usr/bin/env python3
"""Differential-oracle harness — **git-ref baseline** (refactor-scoped).

An engine refactor claims it preserves *behavior*. "Tests green" is not a
sufficient security gate for a large code-motion refactor: a semantic change can
hide in thousands of moved lines while every unit test still passes. This harness
is the **behavioral** guard (the AST attestation in ``_ast_attest.py`` is the
*source-motion* guard; both are required).

It is a **change-time** tool, not a permanent gate. The "before" engine is the
engine **immediately before the refactor**, materialized from a **trusted git
ref** at run time (``_oracle_trust``: verify trust → two-pass bounded extraction →
run the extracted old engine from its OWN tree) — not a checked-in frozen file.
Between refactors no baseline is configured and the oracle is **not applicable**.

What it does
------------
With a baseline ref + an **out-of-band trusted ref** configured, for each fixture
in a **fixed, recorded matrix**, it:

1. materializes the **baseline** engine from the trusted ref (refused before any
   extraction or execution if the baseline is not reachable from the trusted ref)
   and runs it alongside the **current** engine (``bootstrap/scaffold.py``), each
   as a subprocess installing into its own cloned adopter tree — the baseline
   runs from its extracted tree (old code) with **identical templates** (same
   ``--cairn-root``) and the **same profile**;
2. **byte-compares** every installed file between the two trees;
3. **normalizes only the enumerated provenance fields** (``cairn_version`` /
   ``cairn_commit`` in the lockfile) so a commit/version advancing *between* the
   two runs cannot masquerade as a behavior diff. A broad normalization that
   could hide a content diff is rejected (P2#5) — in particular **per-file
   content hashes are NOT normalized**: they are the content guard;
4. enumerates the **location-dependent** untracked files (the interpreter
   binding embeds each tree's own absolute path, so it differs by construction)
   — presence parity is still asserted, but bytes are not compared;
5. emits a **machine-readable JSON report** so the per-stage gate is bounded and
   auditable rather than a hand-recorded "green" (P2#7).

Coverage (substrate Security Review F3): the matrix is not only fresh install.
It also exercises the **privileged workflows** most likely to change when
subsystems move — ``upgrade --stage`` + ``--apply`` (the lockfile + base-cache
write path, via a real upstream template delta), the **containment refusal**
(symlink-trap → ``ScaffoldSecurityError``), and the **dirty-tree refusal** — each
run on both engines and compared (tree byte-compare for apply; normalized exit +
refusal signature for the guards). ``verify_integrity`` hard-imports
``bootstrap.scaffold`` so it is single-engine (suite-covered, not differential);
the report's ``non_differential_coverage`` enumerates exactly what is NOT in the
differential gate, so the gate is honest rather than over-claimed.

Soundness: with the baseline = current HEAD the run is a tautology that proves
the harness itself is sound; its teeth bite when baseline and current diverge
across a refactor (the baseline runs the OLD extracted code, never the current).

Run::

    python bootstrap/tests/_oracle.py run --baseline-ref <sha> --trusted-ref <ref> --report /tmp/oracle.json
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_TESTS_DIR = Path(__file__).resolve().parent
CAIRN_ROOT = _TESTS_DIR.parent.parent
CURRENT_ENGINE = CAIRN_ROOT / "bootstrap" / "scaffold.py"

# The "before" engine is no longer a checked-in frozen FILE — it is materialized
# from a **trusted git ref** at run time (plan: differential-oracle git-ref
# baseline). The trust verification + bounded extraction live in `_oracle_trust`.
try:  # package import (pytest)
    from bootstrap.tests import _oracle_trust as _trust
except ImportError:  # script mode: `python bootstrap/tests/_oracle.py`
    import _oracle_trust as _trust

REPORT_SCHEMA = "cairn.scaffold_split.oracle/v1"

# The fixed, recorded fixture matrix (P2#7: bounded + auditable). The three
# shipped presets span minimal -> rich module rosters, so the install path is
# exercised across core + skills + onboarding + the team-gated module set.
FIXTURES: tuple[dict[str, str], ...] = (
    {"name": "solo-greenfield", "preset": "solo-greenfield"},
    {"name": "collaborative-team", "preset": "collaborative-team"},
    {"name": "high-rigor-legacy", "preset": "high-rigor-legacy"},
)

# Enumerated provenance fields normalized in the lockfile before byte-compare
# (and NOTHING else). Per-file hashes are deliberately excluded from this set.
_PROVENANCE_KEYS: tuple[str, ...] = ("cairn_version", "cairn_commit")
_LOCKFILE_REL = "dev/.cairn/cairn-lock.yml"

# Enumerated location-dependent exclusions: untracked files that embed the
# adopter tree's own absolute path / interpreter binding, which differ by
# construction (the two runs install into different temp roots). Presence parity
# is asserted; bytes are not compared. Recorded so the surface is auditable.
_LOCATION_DEPENDENT: frozenset[str] = frozenset({"dev/.cairn/local-env.json"})


class OracleError(RuntimeError):
    """A fixture failed to install under one of the engines (a run error, not a diff)."""


def _profile_text(preset: str) -> str:
    return f'project_name: "OracleFixture"\ntest_command: "pytest"\npreset: {preset}\n'


def _engine(engine: Path, args: list[str], run_root: Path = CAIRN_ROOT):
    """Run an engine entry point with raw args; return the completed process. The
    subprocess runs with ``run_root`` as cwd so the BASELINE engine imports its
    *own* ``_scaffold`` package (from its extracted tree), not the current one
    (plan Phase 1.1 — old code, current templates via ``--cairn-root``)."""
    return subprocess.run(
        [sys.executable, str(engine), *args],
        capture_output=True, text=True, cwd=str(run_root), check=False,
    )


def _run_engine(engine: Path, target: Path, preset: str,
                cairn_root: Path = CAIRN_ROOT,
                run_root: Path = CAIRN_ROOT) -> "subprocess.CompletedProcess":
    """Fresh-install ``preset`` into ``target`` using ``engine``, reading templates
    from ``cairn_root`` (an editable copy for the upgrade scenarios). Raises on
    a non-zero exit."""
    target.mkdir(parents=True, exist_ok=True)
    cfg = target / "profile.yml"
    cfg.write_text(_profile_text(preset), encoding="utf-8")
    proc = _engine(engine, [
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(cairn_root), "--allow-dev", "--non-interactive",
    ], run_root=run_root)
    if proc.returncode != 0:
        raise OracleError(
            f"engine {engine.name} failed on preset {preset!r} (rc={proc.returncode})\n"
            f"--- stderr ---\n{proc.stderr[-2000:]}\n--- stdout ---\n{proc.stdout[-1000:]}"
        )
    return proc


def _snapshot(target: Path) -> dict[str, bytes]:
    """Map ``{relative_posix_path: bytes}`` for every file under ``target``,
    excluding the profile.yml we wrote in and any VCS dir."""
    out: dict[str, bytes] = {}
    for p in sorted(target.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(target).as_posix()
        if rel == "profile.yml" or rel.startswith(".git/"):
            continue
        out[rel] = p.read_bytes()
    return out


def _normalize(rel: str, data: bytes) -> bytes:
    """Normalize ONLY the enumerated provenance fields, ONLY in the lockfile."""
    if rel != _LOCKFILE_REL:
        return data
    text = data.decode("utf-8")
    for key in _PROVENANCE_KEYS:
        # Top-level YAML key only (column 0): per-file hash:/base_hash: are
        # indented under files: and are left untouched (they are the guard).
        text = re.sub(rf"(?m)^({re.escape(key)}:).*$", rf"\1 <pinned>", text)
    return text.encode("utf-8")


def _compare(frozen: dict[str, bytes], current: dict[str, bytes]) -> list[dict]:
    diffs: list[dict] = []
    for rel in sorted(set(frozen) - set(current)):
        diffs.append({"path": rel, "kind": "only_in_frozen"})
    for rel in sorted(set(current) - set(frozen)):
        diffs.append({"path": rel, "kind": "only_in_current"})
    for rel in sorted(set(frozen) & set(current)):
        if rel in _LOCATION_DEPENDENT:
            continue  # presence parity already proven above; bytes are location-bound
        if _normalize(rel, frozen[rel]) != _normalize(rel, current[rel]):
            diffs.append({
                "path": rel,
                "kind": "bytes_differ",
                "frozen_len": len(frozen[rel]),
                "current_len": len(current[rel]),
            })
    return diffs


# ---------------------------------------------------------------------------
# Privileged-workflow differential scenarios (substrate Security Review F3).
#
# Fresh-install parity (above) is necessary but not sufficient: the high-authority
# paths most likely to change when subsystems move are upgrade stage/apply (the
# lockfile + base-cache write path), the containment refusal, and the dirty-tree
# refusal. Each runs BOTH engines and compares the deterministic result.
#
# Honest coverage boundary (do not over-claim): `verify_integrity.py` hard-imports
# `bootstrap.scaffold`, so it cannot run against the frozen standalone engine --
# it is a SINGLE-engine tool covered by the unit suite, not this differential
# gate. `upgrade --init-lock` / `--finalize` are deterministic lockfile ops
# covered by the unit suite. The report enumerates exactly what is differential.
# ---------------------------------------------------------------------------

def materialize_baseline(baseline_ref: str, trusted_ref: str, workdir: Path,
                         repo: Path = CAIRN_ROOT, *, allow_fetch: bool = False,
                         trusted_remote: str | None = None) -> tuple[Path, Path]:
    """Verify trust, extract the baseline ref's tree, and return
    ``(baseline_engine, baseline_root)`` — the engine run from its own extracted
    tree (old code, current templates). **Refused before extraction or execution**
    if the baseline is not reachable from the out-of-band ``trusted_ref``
    (fail-closed)."""
    sha = _trust.verify_baseline_trust(baseline_ref, trusted_ref, repo,
                                       allow_fetch=allow_fetch, trusted_remote=trusted_remote)
    tree = workdir / "_baseline_tree"
    _trust.extract_ref_tree(sha, tree, repo)
    engine = tree / "bootstrap" / "scaffold.py"
    if not engine.is_file():
        raise OracleError(f"baseline ref {sha[:12]} has no bootstrap/scaffold.py")
    return engine, tree


def _git_available() -> bool:
    return shutil.which("git") is not None


def _git(target: Path, *args: str):
    return subprocess.run(["git", "-C", str(target), *args],
                          capture_output=True, text=True, check=False)


def _git_init_commit(target: Path) -> None:
    """Init + commit; raise (don't let a git setup failure flow silently into the
    later scenario, re-review R2)."""
    for args in (("init", "-q"), ("add", "-A"),
                 ("-c", "user.email=oracle@test", "-c", "user.name=oracle",
                  "commit", "-q", "-m", "init")):
        p = _git(target, *args)
        if p.returncode != 0:
            raise OracleError(
                f"git {args[0]} failed in {target} (rc={p.returncode}): {p.stderr[-400:]}"
            )


# Profile-conditional assembly (cairn-profile-sized-assembly) is a POST-split
# feature: the current engine resolves `cairn:if`/`cairn:endif` regions per the
# adopter's profile, while the frozen PRE-split engine predates the directive and
# would emit the raw markers verbatim -- a divergence that is a deliberate feature,
# NOT a behavioral regression. So this differential gate neutralizes the directive
# markers in the templates BOTH engines read (an enumerated, documented exclusion
# like `_LOCATION_DEPENDENT`); the feature itself is covered by the dedicated
# profile-sized-assembly tests (test_upgrade.py::TestProfileSizedAssembly /
# TestTemplateGatingSafety), not this pre-split parity check.
_PROFILE_IF_MARKER_RE = re.compile(
    r"(?m)^[ \t]*<!--\s*cairn:(?:if\b[^\n]*|endif)\s*-->\n")


def _neutralize_profile_directives(cairn_root: Path) -> None:
    """Strip `cairn:if`/`cairn:endif` MARKER lines (keeping the gated content) from
    every template under *cairn_root*, so both engines install a byte-identical,
    directive-free tree (see the note above)."""
    tdir = cairn_root / "templates"
    if not tdir.is_dir():
        return
    for md in tdir.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        if "cairn:if" in text:
            md.write_text(_PROFILE_IF_MARKER_RE.sub("", text), encoding="utf-8")


def _copy_cairn(dst: Path) -> None:
    """An editable copy of the Cairn tree (templates included) so an upstream
    template delta can be introduced for upgrade scenarios. .git is excluded.
    Profile-conditional directives are neutralized so the pre/post-split engines
    install byte-identically (the feature is covered by its own tests)."""
    shutil.copytree(CAIRN_ROOT, dst,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    _neutralize_profile_directives(dst)


def _refusal_signature(stderr: str) -> str:
    """The final error line, normalized so the two engines compare equal: drop
    the `bootstrap._scaffold.` module prefix (the frozen engine has none) and
    replace a trailing absolute path with `<path>`."""
    lines = [ln for ln in stderr.strip().splitlines() if ln.strip()]
    if not lines:
        return ""
    # Collapse any dotted module qualifier on the exception class to the bare
    # name: the frozen pre-split engine raises `ScaffoldSecurityError` (from
    # __main__), while the current engine raises it from whatever module owns it
    # -- `bootstrap._scaffold` pre-split, `bootstrap._scaffold.security` once the
    # containment leaf is extracted (Stage 1). The class identity + message +
    # exit are unchanged; only the traceback's module path moved.
    last = re.sub(r"[\w.]*ScaffoldSecurityError", "ScaffoldSecurityError", lines[-1])
    last = last.replace("bootstrap._scaffold.", "")
    return re.sub(r"(:\s)(/\S+)$", r"\1<path>", last)


def _error_block(stderr: str) -> str:
    """The refusal block from the first ``error:`` line to the end, module-prefix
    stripped -- deterministic across engines for the gated-refusal messages."""
    idx = stderr.find("error:")
    block = stderr[idx:] if idx >= 0 else stderr
    return block.replace("bootstrap._scaffold.", "").strip()


def _upgrade_apply_scenario(workdir: Path, engines) -> dict:
    """Install both trees, introduce a real upstream template delta, then
    `upgrade --stage` + `--apply` each with its own engine; byte-compare the
    resulting trees. ``engines`` = ``[(label, engine, run_root), ...]`` with
    ``engines[0]`` the baseline and ``engines[1]`` the current."""
    cairn_copy = workdir / "cc_apply"
    _copy_cairn(cairn_copy)
    trees: dict[str, Path] = {}
    for label, engine, root in engines:
        tgt = workdir / f"apply_{label}"
        _run_engine(engine, tgt, "solo-greenfield", cairn_root=cairn_copy, run_root=root)
        _git_init_commit(tgt)
        trees[label] = tgt
    # A real upstream delta on a mergeable core template (not a verbatim script).
    tpl = cairn_copy / "templates" / "core" / "AGENTS.md"
    tpl.write_text(tpl.read_text(encoding="utf-8") + "\n<!-- ORACLE UPSTREAM PROBE -->\n",
                   encoding="utf-8")
    for label, engine, root in engines:
        tgt = trees[label]
        for op in ("--stage", "--apply"):
            p = _engine(engine, ["upgrade", op, "--target", str(tgt),
                                 "--cairn-root", str(cairn_copy)], run_root=root)
            if p.returncode != 0:
                return {"name": "upgrade_apply", "status": "error",
                        "detail": f"{label} {op} rc={p.returncode}: {p.stderr[-600:]}"}
    base, cur = engines[0][0], engines[1][0]
    diffs = _compare(_snapshot(trees[base]), _snapshot(trees[cur]))
    return {"name": "upgrade_apply", "status": "match" if not diffs else "diff",
            "diffs": diffs}


def _containment_refusal_scenario(workdir: Path, engines) -> dict:
    """Plant a symlink trap at an install write target; both engines must refuse
    (exit 1) with the same normalized `ScaffoldSecurityError` signature."""
    sig: dict[str, tuple[int, str]] = {}
    for label, engine, root in engines:
        tgt = workdir / f"contain_{label}"
        tgt.mkdir(parents=True)
        (tgt / "profile.yml").write_text(_profile_text("solo-greenfield"), encoding="utf-8")
        (tgt / "AGENTS.md").symlink_to(workdir / "contain_outside_target")
        p = _engine(engine, ["--config", str(tgt / "profile.yml"), "--target", str(tgt),
                             "--cairn-root", str(CAIRN_ROOT), "--allow-dev", "--non-interactive"],
                    run_root=root)
        sig[label] = (p.returncode, _refusal_signature(p.stderr))
    base, cur = engines[0][0], engines[1][0]
    both_refused = sig[base][0] != 0 and sig[cur][0] != 0
    sigs_match = sig[base][1] == sig[cur][1] and "ScaffoldSecurityError" in sig[cur][1]
    ok = both_refused and sigs_match
    return {"name": "containment_refusal", "status": "match" if ok else "diff",
            "detail": {base: sig[base], cur: sig[cur]}}


def _dirty_tree_refusal_scenario(workdir: Path, engines) -> dict:
    """Install + commit, dirty a tracked write-set file, introduce an upstream
    delta, `--stage` then `--apply`; both engines must refuse the apply (exit 1)
    with the same dirty-tree message."""
    cairn_copy = workdir / "cc_dirty"
    _copy_cairn(cairn_copy)
    sig: dict[str, tuple] = {}
    for label, engine, root in engines:
        tgt = workdir / f"dirty_{label}"
        _run_engine(engine, tgt, "solo-greenfield", cairn_root=cairn_copy, run_root=root)
        _git_init_commit(tgt)
        # adopter dirties AGENTS.md (uncommitted), distinct from the upstream edit
        ag = tgt / "AGENTS.md"
        ag.write_text("<!-- ADOPTER LOCAL EDIT -->\n" + ag.read_text(encoding="utf-8"),
                      encoding="utf-8")
    tpl = cairn_copy / "templates" / "core" / "AGENTS.md"
    tpl.write_text(tpl.read_text(encoding="utf-8") + "\n<!-- ORACLE UPSTREAM PROBE -->\n",
                   encoding="utf-8")
    for label, engine, root in engines:
        tgt = workdir / f"dirty_{label}"
        _engine(engine, ["upgrade", "--stage", "--target", str(tgt), "--cairn-root", str(cairn_copy)], run_root=root)
        ap = _engine(engine, ["upgrade", "--apply", "--target", str(tgt), "--cairn-root", str(cairn_copy)], run_root=root)
        # Compare the whole refusal block (deterministic; only path is AGENTS.md),
        # module-prefix-stripped -- not just the trailing hint line.
        sig[label] = (ap.returncode, _error_block(ap.stderr))
    base, cur = engines[0][0], engines[1][0]
    both_refused = sig[base][0] != 0 and sig[cur][0] != 0
    blocks_match = sig[base][1] == sig[cur][1]
    marker = "refusing --apply" in sig[cur][1]
    ok = both_refused and blocks_match and marker
    return {"name": "dirty_tree_refusal", "status": "match" if ok else "diff",
            "detail": {base: sig[base], cur: sig[cur]}}


_PRIVILEGED_SCENARIOS = (
    _upgrade_apply_scenario,
    _containment_refusal_scenario,
    _dirty_tree_refusal_scenario,
)

#: Behaviors the plan's per-stage gate names that are NOT differential here, with
#: the reason -- enumerated so the gate's coverage is honest, not over-claimed.
_NON_DIFFERENTIAL = {
    "verify_integrity": "single-engine (hard-imports bootstrap.scaffold); covered by the unit suite",
    "upgrade --init-lock / --finalize": "deterministic lockfile ops; covered by the unit suite",
    "upgrade --plan": "read-only report; its write effects are exercised by upgrade_apply",
}


def run_privileged(workdir: Path, engines, *, require_git: bool = True) -> list[dict]:
    """Run the privileged-workflow differential scenarios over ``engines``
    (baseline + current). A git-dependent scenario that cannot run is an
    **error** in gate mode (``require_git=True``); only an explicit exploratory
    caller (``require_git=False``) records it as ``skipped``."""
    results: list[dict] = []
    git_ok = _git_available()
    for scn in _PRIVILEGED_SCENARIOS:
        needs_git = scn is not _containment_refusal_scenario
        if needs_git and not git_ok:
            results.append({
                "name": scn.__name__,
                "status": "error" if require_git else "skipped",
                "detail": "git unavailable — required privileged scenario could not run",
            })
            continue
        results.append(scn(workdir / scn.__name__, engines))
    return results


def run_oracle(workdir: Path, baseline_ref: str | None = None,
               trusted_ref: str | None = None, repo: Path = CAIRN_ROOT, *,
               allow_fetch: bool = False, trusted_remote: str | None = None,
               include_privileged: bool = True, allow_skips: bool = False) -> dict:
    """**Refactor-scoped** differential run. It executes only when a baseline ref
    *and* an out-of-band trusted ref are configured (an active refactor): with no
    baseline configured the oracle is **not applicable** and reports a clean skip
    (it is a change-time tool, not a permanent gate). A baseline that is
    configured but cannot be trust-verified **fails closed** (``materialize``
    raises before any extraction or execution)."""
    if not baseline_ref:
        return {"schema": REPORT_SCHEMA, "status": "not_applicable", "ok": True,
                "reason": "no baseline ref configured — oracle dormant between refactors",
                "fixtures": [], "privileged": []}
    if not trusted_ref:
        raise OracleError("baseline_ref set but no out-of-band trusted_ref — refusing (fail closed)")

    base_engine, base_root = materialize_baseline(
        baseline_ref, trusted_ref, workdir, repo,
        allow_fetch=allow_fetch, trusted_remote=trusted_remote)
    if not _trust.preflight(base_engine, base_root):
        return {"schema": REPORT_SCHEMA, "status": "baseline_not_runnable", "ok": False,
                "reason": "baseline engine does not run under the current environment",
                "fixtures": [], "privileged": []}
    engines = [("baseline", base_engine, base_root), ("current", CURRENT_ENGINE, CAIRN_ROOT)]

    # Both engines read templates from ONE neutralized copy (profile-conditional
    # directives stripped) so a deliberate post-baseline feature is not a diff.
    cairn_neutral = workdir / "_cairn_neutralized"
    _copy_cairn(cairn_neutral)
    fixtures_report: list[dict] = []
    for fx in FIXTURES:
        broot = workdir / fx["name"] / "baseline"
        croot = workdir / fx["name"] / "current"
        _run_engine(base_engine, broot, fx["preset"], cairn_root=cairn_neutral, run_root=base_root)
        _run_engine(CURRENT_ENGINE, croot, fx["preset"], cairn_root=cairn_neutral)
        bsnap, csnap = _snapshot(broot), _snapshot(croot)
        diffs = _compare(bsnap, csnap)
        fixtures_report.append({
            "name": fx["name"], "preset": fx["preset"],
            "status": "match" if not diffs else "diff",
            "baseline_file_count": len(bsnap), "current_file_count": len(csnap),
            "diffs": diffs,
        })
    privileged = (run_privileged(workdir / "privileged", engines, require_git=not allow_skips)
                  if include_privileged else [])
    fixtures_ok = all(f["status"] == "match" for f in fixtures_report)
    if allow_skips:
        privileged_ok = all(p["status"] in ("match", "skipped") for p in privileged)
    else:
        privileged_ok = all(p["status"] == "match" for p in privileged)
    return {
        "schema": REPORT_SCHEMA, "status": "ran",
        "baseline_ref": baseline_ref, "trusted_ref": trusted_ref,
        "current_engine": str(CURRENT_ENGINE.relative_to(CAIRN_ROOT)),
        "normalized_provenance_fields": list(_PROVENANCE_KEYS),
        "location_dependent_excluded": sorted(_LOCATION_DEPENDENT),
        "profile_conditional_neutralized": True,
        "fixtures": fixtures_report,
        "privileged": privileged,
        "non_differential_coverage": _NON_DIFFERENTIAL,
        "ok": fixtures_ok and privileged_ok,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="oracle", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run the differential oracle over the fixture matrix")
    r.add_argument("--report", default=None, help="write the machine-readable JSON report here")
    r.add_argument("--workdir", default=None, help="reuse a directory instead of a fresh tempdir")
    r.add_argument("--baseline-ref", default=None,
                   help="the pre-refactor baseline git ref/SHA (the 'before' engine). "
                        "Omit for the dormant/not-applicable state between refactors.")
    r.add_argument("--trusted-ref", default=None,
                   help="the OUT-OF-BAND trusted ref the baseline must be reachable from "
                        "(the authority — never derived from the evaluated branch).")
    r.add_argument("--allow-skips", action="store_true",
                   help="EXPLORATORY mode: tolerate a missing-git skip of a required "
                        "scenario. NOT a gate -- the default run fails closed on any skip.")
    args = parser.parse_args(argv)

    kw = dict(baseline_ref=args.baseline_ref, trusted_ref=args.trusted_ref,
              allow_skips=args.allow_skips)
    if args.workdir:
        report = run_oracle(Path(args.workdir), **kw)
    else:
        with tempfile.TemporaryDirectory(prefix="cairn-oracle-") as td:
            report = run_oracle(Path(td), **kw)

    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if report.get("status") in ("not_applicable", "baseline_not_runnable"):
        print(f"oracle: {report['status'].upper()} -- {report.get('reason', '')}")
        return 0 if report["ok"] else 1
    for fx in report["fixtures"]:
        line = f"  {fx['status'].upper():7}  install:{fx['name']:20}  {fx.get('baseline_file_count', 0)} file(s)"
        if fx["status"] != "match":
            line += f"  -- {len(fx['diffs'])} diff(s)"
        print(line)
    for pv in report["privileged"]:
        print(f"  {pv['status'].upper():7}  {pv['name']}")
    if report["ok"]:
        nfix = len(report["fixtures"])
        npv = sum(1 for p in report["privileged"] if p["status"] == "match")
        print(f"oracle: OK -- {nfix} fresh-install fixture(s) + {npv} privileged "
              f"workflow(s), behavior preserved.")
        return 0
    print("oracle: FAILED -- behavioral divergence between baseline and current engine:", file=sys.stderr)
    for fx in report["fixtures"]:
        for d in fx.get("diffs", []):
            print(f"  [install:{fx['name']}] {d['kind']}: {d['path']}", file=sys.stderr)
    for pv in report["privileged"]:
        if pv["status"] not in ("match", "skipped"):
            print(f"  [{pv['name']}] {pv['status']}: {pv.get('detail') or pv.get('diffs')}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
