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

@pytest.mark.skipif(
    not (CAIRN_ROOT / "templates" / "skills").exists(),
    reason="templates/skills not available",
)
def test_oracle_matrix_behavior_preserved(tmp_path):
    """End-to-end: install all fixtures under both engines and prove parity.
    At 0A this is a tautology (the engines are byte-identical) whose value is
    proving the harness itself is sound -- it installs cleanly and the exclusion
    set is complete. Its teeth bite at Stages 1-8 when the engines diverge."""
    report = O.run_oracle(tmp_path, include_privileged=False)
    assert report["schema"] == O.REPORT_SCHEMA
    assert report["normalized_provenance_fields"] == list(O._PROVENANCE_KEYS)
    assert report["ok"] is True, report
    for fx in report["fixtures"]:
        assert fx["status"] == "match", fx
        assert fx["frozen_file_count"] > 20, "expected a substantive install, not an empty tree"
        assert fx["frozen_file_count"] == fx["current_file_count"]


@pytest.mark.skipif(
    not (CAIRN_ROOT / "templates" / "skills").exists(),
    reason="templates/skills not available",
)
def test_oracle_privileged_workflows_preserved(tmp_path):
    """F3 (substrate Security Review): the privileged workflows — upgrade
    stage/apply, containment refusal, dirty-tree refusal — are behaviorally
    identical between the frozen pre-split engine and the current launcher+engine.
    Runs the real subprocess scenarios (slower); skips the git-dependent ones if
    git is unavailable rather than dropping them silently."""
    if not O._git_available():
        pytest.skip("git unavailable; privileged upgrade/dirty scenarios need it")
    results = O.run_privileged(tmp_path)   # gate mode (require_git=True)
    assert len(results) == len(O._PRIVILEGED_SCENARIOS)
    for r in results:
        assert r["status"] == "match", r   # gate mode: every required scenario MATCH


def test_oracle_gate_does_not_silently_skip_required_scenarios(tmp_path, monkeypatch):
    """R2: with git unavailable the gate must FAIL closed (a required scenario
    becomes `error`), not pass after running only containment. An explicit
    exploratory caller may record `skipped` instead."""
    monkeypatch.setattr(O, "_git_available", lambda: False)
    gate = O.run_privileged(tmp_path / "gate", require_git=True)
    assert any(r["status"] == "error" for r in gate), "gate must error, not skip, without git"
    # containment needs no git -- it still runs and matches in both modes.
    assert any(r.get("name") == "containment_refusal" and r["status"] == "match" for r in gate)
    explore = O.run_privileged(tmp_path / "explore", require_git=False)
    assert any(r["status"] == "skipped" for r in explore)
    assert not any(r["status"] == "error" for r in explore)


def test_frozen_engine_snapshot_present():
    assert O.FROZEN_ENGINE.is_file(), (
        "the frozen pre-split engine snapshot is missing -- the oracle has no reference"
    )
