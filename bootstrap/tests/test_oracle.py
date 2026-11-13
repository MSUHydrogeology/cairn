"""Contract for the differential-oracle harness.

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

Promises:
- The gate fails with a diff report when an evaluated engine changes a file's bytes.
- The gate refuses to evaluate an engine that is itself the verifier, and requires a target root.
- The gate runs every required scenario and does not skip one silently.
- A content-only difference between engines (a rewritten installed file, a changed per-file hash in the lockfile) is reported, not normalized away.
- A file missing from or added to the evaluated engine is reported as a difference.
- An unchanged engine reports no differences across the fixture matrix.
- An untrusted baseline fails the gate closed.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

from bootstrap.tests import _oracle as O

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent

# --- teeth: the diff engine must not be vacuous --------------------------------


# --- presence parity for location-dependent exclusions -------------------------


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


def test_oracle_gate_does_not_silently_skip_required_scenarios(tmp_path, monkeypatch):
    """With git unavailable the gate must FAIL closed (a required scenario
    becomes `error`), not pass after running only containment."""
    engines = _engines(tmp_path)
    monkeypatch.setattr(O, "_git_available", lambda: False)
    gate = O.run_privileged(tmp_path / "gate", engines, require_git=True)
    assert any(r["status"] == "error" for r in gate), "gate must error, not skip, without git"
    assert any(r.get("name") == "containment_refusal" and r["status"] == "match" for r in gate)
    explore = O.run_privileged(tmp_path / "explore", engines, require_git=False)
    assert any(r["status"] == "skipped" for r in explore)
    assert not any(r["status"] == "error" for r in explore)


# --- The trusted verifier measures the TARGET, not itself ---------------------

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
    """Teeth: the target's current engine is behaviorally changed (writes a
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


@pytest.mark.skipif(
    not (CAIRN_ROOT / "templates" / "skills").exists(),
    reason="templates/skills not available",
)
def test_oracle_reports_a_target_engine_that_only_rewrites_existing_files(tmp_path):
    """A target engine that changes the bytes of files the baseline also writes (an
    installed file, and a per-file hash in the lockfile) is reported as differing
    in those files; the lockfile normalization does not hide a content change."""
    target = _copy_target(tmp_path / "target")
    launcher = target / "bootstrap" / "scaffold.py"
    inject = (
        "\nimport sys as _sys\nfrom pathlib import Path as _P\n"
        "_orig_main = _engine.main\n"
        "def _rewrite(*a, **k):\n"
        "    rc = _orig_main(*a, **k)\n"
        "    av = _sys.argv[1:]\n"
        "    if '--target' in av:\n"
        "        root = _P(av[av.index('--target') + 1])\n"
        "        agents = root / 'AGENTS.md'\n"
        "        agents.write_text(agents.read_text() + 'one more line\\n')\n"
        "        lock = root / 'dev' / '.cairn' / 'cairn-lock.yml'\n"
        "        lock.write_text(lock.read_text().replace("
        "'\"hash\": \"sha256:', '\"hash\": \"sha256:0', 1))\n"
        "    return rc\n"
        "_engine.main = _rewrite\n"
    )
    text = launcher.read_text()
    assert "_engine = _load_engine()" in text
    launcher.write_text(text.replace("_engine = _load_engine()", "_engine = _load_engine()" + inject, 1))
    report = O.run_oracle(tmp_path / "wd", baseline_ref="HEAD", trusted_ref="HEAD",
                          repo=O.CAIRN_ROOT, target_root=target, include_privileged=False)
    diffs = {(d["path"], d["kind"]) for fx in report["fixtures"] for d in fx.get("diffs", [])}
    assert report["ok"] is False
    assert {("AGENTS.md", "bytes_differ"), (O._LOCKFILE_REL, "bytes_differ")} <= diffs, report


@pytest.mark.skipif(
    not (CAIRN_ROOT / "templates" / "skills").exists(),
    reason="templates/skills not available",
)
def test_oracle_normalizes_only_valid_lock_provenance_in_public_workflow(tmp_path):
    """A real oracle run tolerates only the two lock provenance value changes."""
    target = _copy_target(tmp_path / "target")
    launcher = target / "bootstrap" / "scaffold.py"
    inject = (
        "\nimport json as _json\nimport sys as _sys\n"
        "from pathlib import Path as _P\n"
        "_orig_main = _engine.main\n"
        "def _provenance(*a, **k):\n"
        "    rc = _orig_main(*a, **k)\n"
        "    av = _sys.argv[1:]\n"
        "    if '--target' in av:\n"
        "        root = _P(av[av.index('--target') + 1])\n"
        "        lock = root / 'dev' / '.cairn' / 'cairn-lock.yml'\n"
        "        lines = lock.read_text(encoding='utf-8').splitlines(keepends=True)\n"
        "        values = {'cairn_version': 'different-version', "
        "'cairn_commit': '0' * 40}\n"
        "        found = set()\n"
        "        for i, line in enumerate(lines):\n"
        "            for key, value in values.items():\n"
        "                prefix = '  ' + _json.dumps(key) + ': '\n"
        "                if line.startswith(prefix):\n"
        "                    suffix = ',\\n' if line.endswith(',\\n') else '\\n'\n"
        "                    lines[i] = prefix + _json.dumps(value) + suffix\n"
        "                    found.add(key)\n"
        "        if found != set(values): raise RuntimeError('lock provenance fields missing')\n"
        "        lock.write_text(''.join(lines), encoding='utf-8')\n"
        "    return rc\n"
        "_engine.main = _provenance\n"
    )
    text = launcher.read_text()
    assert "_engine = _load_engine()" in text
    launcher.write_text(text.replace(
        "_engine = _load_engine()", "_engine = _load_engine()" + inject, 1))
    report = O.run_oracle(
        tmp_path / "wd", baseline_ref="HEAD", trusted_ref="HEAD",
        repo=O.CAIRN_ROOT, target_root=target, include_privileged=False)
    assert report["ok"] is True, report


@pytest.mark.skipif(
    not (CAIRN_ROOT / "templates" / "skills").exists(),
    reason="templates/skills not available",
)
def test_oracle_rejects_identical_malformed_lock_from_both_engines(tmp_path):
    """Both engines write the same malformed lock; equality cannot hide it."""
    trusted = tmp_path / "trusted"
    O._copy_cairn(trusted, CAIRN_ROOT)
    launcher = trusted / "bootstrap" / "scaffold.py"
    inject = (
        "\nimport sys as _sys\nfrom pathlib import Path as _P\n"
        "_orig_main = _engine.main\n"
        "def _same_bad_lock(*a, **k):\n"
        "    rc = _orig_main(*a, **k)\n"
        "    av = _sys.argv[1:]\n"
        "    if '--target' in av:\n"
        "        root = _P(av[av.index('--target') + 1])\n"
        "        (root / 'dev' / '.cairn' / 'cairn-lock.yml').write_bytes(b'{')\n"
        "    return rc\n"
        "_engine.main = _same_bad_lock\n"
    )
    text = launcher.read_text(encoding="utf-8")
    assert "_engine = _load_engine()" in text
    launcher.write_text(text.replace(
        "_engine = _load_engine()", "_engine = _load_engine()" + inject, 1),
        encoding="utf-8")
    O._git_init_commit(trusted)
    report = O.run_oracle(
        tmp_path / "wd", baseline_ref="HEAD", trusted_ref="HEAD",
        repo=trusted, target_root=trusted, include_privileged=False)
    assert report["ok"] is False
    for fixture in report["fixtures"]:
        assert (O._LOCKFILE_REL, "bytes_differ") in {
            (diff["path"], diff["kind"]) for diff in fixture["diffs"]
        }, fixture


# --- The shipped CLI gates a TARGET, never itself --------------------------------

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
    """The shipped CLI in --gate mode refuses target == trusted checkout — the
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
    """--gate without an explicit --target-root is a usage error (no silent
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
    """Teeth via the SHIPPED CLI, not only the in-process function: a
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
