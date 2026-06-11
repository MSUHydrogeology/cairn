"""Contract for the differential-oracle harness (scaffold-split 0A.3 / P2#5/#7).

Two halves:

* **Non-vacuity (teeth).** The diff/normalization engine (`_compare` /
  `_normalize`) must catch a changed byte, a missing file, and an added file —
  and the provenance normalization must be **narrow**: it tolerates a
  ``cairn_commit`` / ``cairn_version`` difference but **not** a per-file content
  hash difference (a broad normalization that hid content would defeat the gate).
* **Soundness (tautology).** At Stage 0A the current engine *is* the frozen
  engine, so a full run over the fixture matrix must report OK with substantive
  file counts — proving the harness installs cleanly and the enumerated
  location-dependent exclusion set is complete (no spurious diffs).

Stdlib only.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

from bootstrap.tests import _oracle as O

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent

_LOCK = O._LOCKFILE_REL


def _lockfile(commit: str = "abc1234", version: str = "0.2.0",
              agents_hash: str = "sha256:deadbeef") -> bytes:
    return (
        f'cairn_version: "{version}"\n'
        f"cairn_commit: {commit}\n"
        f"files:\n"
        f"  AGENTS.md:\n"
        f'    hash: "{agents_hash}"\n'
        f'    base_hash: "sha256:cafef00d"\n'
    ).encode("utf-8")


# --- teeth: the diff engine must not be vacuous --------------------------------

def test_compare_detects_a_changed_byte():
    frozen = {"AGENTS.md": b"hello\n"}
    current = {"AGENTS.md": b"hellp\n"}
    diffs = O._compare(frozen, current)
    assert [d["kind"] for d in diffs] == ["bytes_differ"]
    assert diffs[0]["path"] == "AGENTS.md"


def test_compare_detects_missing_and_added_files():
    frozen = {"a.md": b"x", "gone.md": b"y"}
    current = {"a.md": b"x", "extra.md": b"z"}
    kinds = {(d["path"], d["kind"]) for d in O._compare(frozen, current)}
    assert ("gone.md", "only_in_frozen") in kinds
    assert ("extra.md", "only_in_current") in kinds


def test_identical_trees_have_no_diffs():
    snap = {"a.md": b"x", "b.md": b"y"}
    assert O._compare(dict(snap), dict(snap)) == []


# --- narrow normalization: provenance tolerated, content hashes are NOT --------

def test_provenance_difference_is_normalized_away():
    frozen = {_LOCK: _lockfile(commit="abc1234", version="0.2.0")}
    current = {_LOCK: _lockfile(commit="zzz9999", version="9.9.9")}
    assert O._compare(frozen, current) == [], (
        "a commit/version difference must not register as a behavior diff"
    )


def test_per_file_content_hash_difference_is_NOT_normalized():
    """The crucial guard (P2#5): the normalization must be narrow enough that a
    real content change — surfacing as a changed per-file hash — still fails."""
    frozen = {_LOCK: _lockfile(agents_hash="sha256:deadbeef")}
    current = {_LOCK: _lockfile(agents_hash="sha256:00000000")}
    diffs = O._compare(frozen, current)
    assert [d["kind"] for d in diffs] == ["bytes_differ"]


def test_normalize_only_touches_the_lockfile():
    # A non-lockfile file is returned unchanged even if it mentions a key name.
    body = b"cairn_commit: not-a-lockfile-line\n"
    assert O._normalize("AGENTS.md", body) == body
    # In the lockfile, the top-level provenance value is pinned...
    pinned = O._normalize(_LOCK, _lockfile(commit="abc1234")).decode()
    assert "cairn_commit: <pinned>" in pinned
    # ...but the indented per-file hash is left intact.
    assert "sha256:deadbeef" in pinned


# --- presence parity for location-dependent exclusions -------------------------

def test_location_dependent_file_excluded_from_bytes_but_presence_required():
    rel = next(iter(O._LOCATION_DEPENDENT))
    # Different bytes but present in both -> tolerated (location-bound content).
    assert O._compare({rel: b"A"}, {rel: b"B"}) == []
    # Absent from one side -> still a presence-parity failure.
    assert O._compare({rel: b"A"}, {}) == [{"path": rel, "kind": "only_in_frozen"}]


# --- soundness: a full run is OK at 0A (frozen == current) ---------------------

def _engines(tmp_path):
    """The (baseline, current) engine pair from the trusted git ref HEAD — the
    baseline materialized into its own extracted tree."""
    base_engine, base_root = O.materialize_baseline("HEAD", "HEAD", tmp_path)
    return [("baseline", base_engine, base_root), ("current", O.CURRENT_ENGINE, O.CAIRN_ROOT)]


@pytest.mark.skipif(
    not (CAIRN_ROOT / "templates" / "skills").exists(),
    reason="templates/skills not available",
)
def test_oracle_matrix_behavior_preserved(tmp_path):
    """End-to-end soundness: with baseline = current HEAD, a full run over the
    fixture matrix reports OK with substantive counts — proving the harness is
    sound (git-ref materialization installs cleanly, the exclusion set is
    complete). Its teeth bite when baseline and current diverge across a refactor."""
    report = O.run_oracle(tmp_path, baseline_ref="HEAD", trusted_ref="HEAD",
                          include_privileged=False)
    assert report["schema"] == O.REPORT_SCHEMA
    assert report["status"] == "ran"
    assert report["ok"] is True, report
    for fx in report["fixtures"]:
        assert fx["status"] == "match", fx
        assert fx["baseline_file_count"] > 20, "expected a substantive install, not an empty tree"
        assert fx["baseline_file_count"] == fx["current_file_count"]


def test_oracle_baseline_runs_from_extracted_tree(tmp_path):
    """Isolation (plan 1.1): the baseline engine is materialized under the run's
    own tree, NOT CAIRN_ROOT — so it imports its own (old) `_scaffold`."""
    base_engine, _ = O.materialize_baseline("HEAD", "HEAD", tmp_path)
    assert str(base_engine).startswith(str(tmp_path))
    assert base_engine.is_file() and base_engine.name == "scaffold.py"


def test_oracle_dormant_without_baseline(tmp_path):
    """Refactor-scoped: with no baseline configured the oracle is not applicable
    and reports a clean skip — a change-time tool, not a permanent gate."""
    report = O.run_oracle(tmp_path)
    assert report["status"] == "not_applicable" and report["ok"] is True


def test_oracle_fails_closed_on_untrusted_baseline(tmp_path):
    """A configured baseline with no out-of-band trusted ref fails closed (never
    a silent skip)."""
    with pytest.raises(O.OracleError):
        O.run_oracle(tmp_path, baseline_ref="HEAD")   # trusted_ref omitted


@pytest.mark.skipif(
    not (CAIRN_ROOT / "templates" / "skills").exists(),
    reason="templates/skills not available",
)
def test_oracle_privileged_workflows_preserved(tmp_path):
    """F3: the privileged workflows — upgrade stage/apply, containment refusal,
    dirty-tree refusal — are behaviorally identical between the materialized
    baseline engine and the current launcher+engine."""
    if not O._git_available():
        pytest.skip("git unavailable; privileged upgrade/dirty scenarios need it")
    results = O.run_privileged(tmp_path / "p", _engines(tmp_path))   # gate mode
    assert len(results) == len(O._PRIVILEGED_SCENARIOS)
    for r in results:
        assert r["status"] == "match", r


def test_oracle_gate_does_not_silently_skip_required_scenarios(tmp_path, monkeypatch):
    """R2: with git unavailable the gate must FAIL closed (a required scenario
    becomes `error`), not pass after running only containment."""
    engines = _engines(tmp_path)
    monkeypatch.setattr(O, "_git_available", lambda: False)
    gate = O.run_privileged(tmp_path / "gate", engines, require_git=True)
    assert any(r["status"] == "error" for r in gate), "gate must error, not skip, without git"
    assert any(r.get("name") == "containment_refusal" and r["status"] == "match" for r in gate)
    explore = O.run_privileged(tmp_path / "explore", engines, require_git=False)
    assert any(r["status"] == "skipped" for r in explore)
    assert not any(r["status"] == "error" for r in explore)


# --- P1.2: trusted verifier measures the TARGET, not itself --------------------

def _copy_target(dst: Path) -> Path:
    shutil.copytree(O.CAIRN_ROOT, dst,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    return dst


@pytest.mark.skipif(
    not (CAIRN_ROOT / "templates" / "skills").exists(),
    reason="templates/skills not available",
)
def test_oracle_measures_target_not_verifier(tmp_path):
    """The CURRENT engine + templates come from target_root (the evaluated tree),
    not where the verifier code runs. target = copy of HEAD still matches the
    HEAD baseline, and the report names the target as current."""
    target = _copy_target(tmp_path / "target")
    report = O.run_oracle(tmp_path / "wd", baseline_ref="HEAD", trusted_ref="HEAD",
                          repo=O.CAIRN_ROOT, target_root=target, include_privileged=False)
    assert report["status"] == "ran" and report["ok"] is True, report
    assert report["target_root"] == str(target)
    assert str(target) in report["current_engine"]


@pytest.mark.skipif(
    not (CAIRN_ROOT / "templates" / "skills").exists(),
    reason="templates/skills not available",
)
def test_oracle_teeth_target_engine_diverges(tmp_path):
    """Teeth (P1.2): the target's current engine is behaviorally changed (writes a
    sentinel into every install) while the trusted baseline is unchanged — the
    trusted-checkout invocation must report a diff."""
    target = _copy_target(tmp_path / "target")
    launcher = target / "bootstrap" / "scaffold.py"
    inject = (
        "\nimport sys as _sys\nfrom pathlib import Path as _P\n"
        "_orig_main = _engine.main\n"
        "def _teeth(*a, **k):\n"
        "    rc = _orig_main(*a, **k)\n"
        "    av = _sys.argv[1:]\n"
        "    if '--target' in av:\n"
        "        _P(av[av.index('--target') + 1], 'TEETH_SENTINEL').write_text('diverged\\n')\n"
        "    return rc\n"
        "_engine.main = _teeth\n"
    )
    text = launcher.read_text()
    text = text.replace("_engine = _load_engine()", "_engine = _load_engine()" + inject, 1)
    launcher.write_text(text)
    report = O.run_oracle(tmp_path / "wd", baseline_ref="HEAD", trusted_ref="HEAD",
                          repo=O.CAIRN_ROOT, target_root=target, include_privileged=False)
    assert report["ok"] is False, "a behaviorally-changed target engine must diff"
    paths = {d["path"] for fx in report["fixtures"] for d in fx.get("diffs", [])}
    assert any("TEETH_SENTINEL" in p for p in paths), report


# --- F2 (re-review): the shipped CLI gates a TARGET, never itself -----------------

def _git_init_target(root: Path) -> str:
    """Make ``root`` a one-commit git checkout so gate mode can pin its candidate
    SHA; return that SHA."""
    import subprocess
    for args in (("init", "-q"), ("add", "-A"),
                 ("-c", "user.email=o@t", "-c", "user.name=o", "commit", "-q", "-m", "c")):
        subprocess.run(["git", "-C", str(root), *args], check=True,
                       capture_output=True, text=True)
    return subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()


def test_oracle_cli_gate_refuses_self_target(tmp_path):
    """F2: the shipped CLI in --gate mode refuses target == trusted checkout — the
    default-self self-measurement a trusted-checkout caller would otherwise get."""
    import subprocess
    proc = subprocess.run(
        [sys.executable, str(O.CAIRN_ROOT / "bootstrap" / "tests" / "_oracle.py"),
         "run", "--gate", "--repo", str(O.CAIRN_ROOT), "--target-root", str(O.CAIRN_ROOT),
         "--baseline-ref", "HEAD", "--trusted-ref", "HEAD", "--workdir", str(tmp_path / "wd")],
        capture_output=True, text=True)
    assert proc.returncode != 0, proc.stdout
    assert "self-measurement" in (proc.stdout + proc.stderr)


def test_oracle_cli_gate_requires_target_root(tmp_path):
    """F2: --gate without an explicit --target-root is a usage error (no silent
    default-self)."""
    import subprocess
    proc = subprocess.run(
        [sys.executable, str(O.CAIRN_ROOT / "bootstrap" / "tests" / "_oracle.py"),
         "run", "--gate", "--baseline-ref", "HEAD", "--trusted-ref", "HEAD"],
        capture_output=True, text=True)
    assert proc.returncode != 0
    assert "--target-root" in (proc.stdout + proc.stderr)


@pytest.mark.skipif(
    not (CAIRN_ROOT / "templates" / "skills").exists(),
    reason="templates/skills not available",
)
def test_oracle_cli_gate_teeth_subprocess(tmp_path):
    """Teeth via the SHIPPED CLI (F2, not only the in-process function): a
    behaviorally-changed evaluated target, gated from a trusted checkout, makes the
    CLI exit non-zero and pins the target's candidate SHA in the report."""
    import json as _json
    import subprocess
    target = _copy_target(tmp_path / "target")
    launcher = target / "bootstrap" / "scaffold.py"
    text = launcher.read_text().replace(
        "_engine = _load_engine()",
        "_engine = _load_engine()\nimport sys as _s\nfrom pathlib import Path as _P\n"
        "_om = _engine.main\n"
        "def _t(*a, **k):\n"
        "    rc = _om(*a, **k)\n"
        "    _av = _s.argv[1:]\n"
        "    if '--target' in _av:\n"
        "        _P(_av[_av.index('--target')+1], 'TEETH_SENTINEL').write_text('x\\n')\n"
        "    return rc\n"
        "_engine.main = _t\n", 1)
    launcher.write_text(text)
    candidate = _git_init_target(target)
    report_path = tmp_path / "report.json"
    proc = subprocess.run(
        [sys.executable, str(O.CAIRN_ROOT / "bootstrap" / "tests" / "_oracle.py"),
         "run", "--gate", "--repo", str(O.CAIRN_ROOT), "--target-root", str(target),
         "--baseline-ref", "HEAD", "--trusted-ref", "HEAD",
         "--workdir", str(tmp_path / "wd"), "--report", str(report_path)],
        capture_output=True, text=True)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    report = _json.loads(report_path.read_text())
    assert report["candidate_sha"] == candidate
    assert str(target) in report["current_engine"]
    paths = {d["path"] for fx in report["fixtures"] for d in fx.get("diffs", [])}
    assert any("TEETH_SENTINEL" in p for p in paths), report
