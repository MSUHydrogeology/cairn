"""Contract for the gate-integrity manifest tool (six-proposal superplan pre-run
gate-control prerequisite).

Pins: produce() captures the frozen gate surface + cascade-mutable set + the
collection identity; the frozen set excludes cascade-mutable files and the
manifest artifact itself; and verify() HOLDs on every tampering class
(frozen-file edit, dropped node, new skip/xfail marker, interpreter-minor
mismatch, broken external anchor) while allowing additions. Stdlib only.

Promises:
- Producing a manifest records the frozen gate files and the collected test identities, and excludes cascade-mutable files and the manifest itself.
- Verification passes a clean tree and holds on a modified or deleted frozen file.
- Verification holds on a dropped test, a new skip or xfail marker, and an interpreter minor-version mismatch.
- Verification allows an added test and reports ordinary changes without holding.
- Verification holds when a required anchor is missing, and refuses a present but null roster.
- With a trusted repository, a target tree cannot mint its own anchor, and tampering in a separate target tree holds.
- Omitting the roster keeps the broad test policy, and a roster narrows only test globs.
- The verifier's git reads ignore the operator's GIT_ environment variables.
"""
from __future__ import annotations

import copy
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from bootstrap.tests import _gate_manifest as G

_REPO = Path(__file__).resolve().parents[2]


def _write_manifest(tmp_path, manifest: dict) -> Path:
    p = tmp_path / "gate_manifest.json"
    p.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return p


@pytest.fixture(scope="session")
def produced() -> dict:
    """Produce once (a full collection subprocess) and share across tests."""
    roster_bytes = (_REPO / G._PROTECTED_ROSTER_REL).read_bytes()
    roster = G._roster_from_bytes(roster_bytes, require_initial_approval=True)
    return G.produce(_REPO, roster)


def test_produce_has_the_expected_shape(produced):
    assert produced["schema"] == G.SCHEMA
    for key in ("interpreter", "gate_commands", "collection", "frozen_files",
                "protected_roster", "ordinary_test_files",
                "cascade_mutable", "mapping_symbols"):
        assert key in produced
    assert produced["collection"]["node_count"] == len(produced["collection"]["node_ids"])
    assert produced["collection"]["node_count"] > 100  # the real suite is large
    for sym in ("_MODULE_MAPPINGS", "_SKILLS_MAPPINGS", "_CORE_MAPPINGS"):
        assert produced["mapping_symbols"][sym]["baseline_digest"]


#: Gate files that did not exist when the roster was approved: a roster must not
#: let any of them out of the frozen set.
_FUTURE_NON_TEST_FILES = (
    "bootstrap/tests/helpers.py",
    "bootstrap/tests/fixtures/new_fixture.py",
    "scripts/new_script.py",
    "templates/modules/new_module.py",
    "bootstrap/new_engine.py",
)


def _candidate_repo(tmp_path: Path) -> Path:
    """A tree holding a protected and an ordinary test file, the future non-test
    files, a planted roster that protects nothing, and what `produce` needs to
    collect and pin it."""
    repo = tmp_path / "candidate"
    tests = repo / "bootstrap" / "tests"
    (tests / "fixtures").mkdir(parents=True)
    (tests / "__init__.py").write_text("", encoding="utf-8")
    shutil.copy(Path(G.__file__), tests / "_gate_manifest.py")
    shutil.copy(_REPO / "bootstrap/tests/fixtures/scaffold_ast_baseline.json",
                tests / "fixtures" / "scaffold_ast_baseline.json")
    for rel in ("bootstrap/tests/test_protected.py", "bootstrap/tests/test_ordinary.py"):
        (repo / rel).write_text("def test_x(): pass\n", encoding="utf-8")
    for rel in _FUTURE_NON_TEST_FILES:
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("VALUE = 1\n", encoding="utf-8")
    (tests / "fixtures" / "protected_test_roster.json").write_text(
        json.dumps({"protected_python_paths": []}), encoding="utf-8")
    return repo


@pytest.mark.parametrize("roster", [
    None,
    {"protected_python_paths": ["bootstrap/tests/test_protected.py"]},
], ids=["no-roster-though-the-tree-plants-one", "roster-names-one-test-file"])
def test_produce_freezes_future_non_test_files_and_a_roster_narrows_only_test_files(
        tmp_path, roster):
    """Without a trusted roster the broad policy holds, whatever roster the tree
    carries.  With one, only test files leave the frozen set; every other gate
    file, including one added later, stays in it."""
    frozen = set(G.produce(_candidate_repo(tmp_path), roster)["frozen_files"])
    required = {"bootstrap/tests/test_protected.py", *_FUTURE_NON_TEST_FILES}
    if roster is None:
        required.add("bootstrap/tests/test_ordinary.py")
    assert required <= frozen
    assert ("bootstrap/tests/test_ordinary.py" in frozen) == (roster is None)


def test_frozen_set_boundary(produced):
    frozen = produced["frozen_files"]
    # known gate files are pinned
    assert "bootstrap/tests/test_ast_attest.py" in frozen
    assert "bootstrap/tests/test_intents_tool.py" in frozen
    assert "bootstrap/tests/test_agreement_retired.py" not in frozen
    assert "bootstrap/tests/fixtures/protected_test_roster.json" in frozen
    assert "scripts/check_cairn.py" in frozen
    assert "bootstrap/tests/_ast_attest.py" in frozen
    assert "bootstrap/tests/_gate_manifest.py" in frozen  # self-pinned
    # top-level gate-defining engine modules MUST be frozen (Security review BLOCKER):
    # security_check.py is the single source of the Bandit allowlist + scan targets.
    assert "bootstrap/security_check.py" in frozen
    assert "bootstrap/verify_integrity.py" in frozen
    assert "bootstrap/check_module_body_coverage.py" in frozen
    # cascade-mutable files + the manifest artifact are NOT frozen-hashed
    assert "bootstrap/tests/fixtures/scaffold_ast_baseline.json" not in frozen
    assert "bootstrap/_scaffold/config.py" not in frozen
    # the differential oracle's frozen-engine fixture is RETIRED (git-ref baseline)
    assert not any("scaffold_frozen" in f for f in frozen)
    assert "bootstrap/tests/fixtures/frozen_engine/scaffold_frozen.py" not in G.CASCADE_MUTABLE
    assert G._MANIFEST_REL not in frozen
    # shipped scanner / security-gate implementations ARE frozen (Codex confirmation Finding 2)
    assert "templates/modules/team-gated/content_scan.py" in frozen
    assert "templates/modules/team-gated/content_scan_runner.py" in frozen
    assert "templates/modules/team-gated/run_security_audit.py" in frozen
    assert "templates/modules/team-gated/link_check.py" in frozen
    # the phase-split facade targets are NOT frozen — they are phase_mutable
    assert "templates/modules/team-gated/intent.py" not in frozen
    assert set(produced["phase_mutable"]) == set(G.PHASE_SPLIT_TARGETS)


def test_verify_clean_tree_is_ok(produced, tmp_path, capsys):
    mp = _write_manifest(tmp_path, produced)
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 0
    assert "OK — gate integrity intact" in capsys.readouterr().err


def test_verify_refuses_present_null_roster(produced, tmp_path, capsys):
    malformed = copy.deepcopy(produced)
    malformed["protected_roster"] = None
    mp = _write_manifest(tmp_path, malformed)
    assert G.verify(mp, anchor_ref=None, repo=_REPO, do_collect=False) == 1
    assert "ROSTER-MALFORMED" in capsys.readouterr().err


def test_verify_holds_on_frozen_file_modification(produced, tmp_path, capsys):
    tampered = copy.deepcopy(produced)
    # pretend a pinned gate file was edited (wrong sha)
    tampered["frozen_files"]["bootstrap/tests/test_ast_attest.py"] = "0" * 64
    mp = _write_manifest(tmp_path, tampered)
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 1
    assert "FROZEN-MODIFIED" in capsys.readouterr().err


# Declared exception (internal hook): Hook: G._collect monkeypatched to report a dropped test node; a real tamper needs a full collection run of a target tree.
def test_verify_holds_on_dropped_node(produced, tmp_path, capsys, monkeypatch):
    tampered = copy.deepcopy(produced)
    # Drop an actual node owned by a protected file.
    victim = next(n for n in tampered["collection"]["node_ids"]
                  if n.startswith("bootstrap/tests/test_ast_attest.py::"))
    mp = _write_manifest(tmp_path, tampered)
    ids = set(produced["collection"]["node_ids"]) - {victim}
    marked = produced["collection"]["skip_xfail_marked"]
    monkeypatch.setattr(G, "_collect", lambda repo=_REPO: (sorted(ids), marked, 0))
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 1
    assert "COLLECTION-DROPPED" in capsys.readouterr().err


def test_verify_holds_on_interpreter_minor_mismatch(produced, tmp_path, capsys):
    tampered = copy.deepcopy(produced)
    tampered["interpreter"]["version_info"] = [3, 11, 0]
    mp = _write_manifest(tmp_path, tampered)
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 1
    assert "INTERPRETER" in capsys.readouterr().err


# Declared exception (internal hook): Hook: G._collect monkeypatched to report a new skip marker; a real tamper needs a full collection run of a target tree.
def test_verify_holds_on_new_skip_marker(produced, tmp_path, capsys, monkeypatch):
    mp = _write_manifest(tmp_path, produced)
    ids = produced["collection"]["node_ids"]
    pinned_marked = set(produced["collection"]["skip_xfail_marked"])
    # simulate the run adding a skip/xfail marker to a currently-UNMARKED test
    fresh = next(i for i in ids if i not in pinned_marked
                 and i.startswith("bootstrap/tests/test_ast_attest.py::"))
    monkeypatch.setattr(G, "_collect", lambda repo=_REPO: (sorted(ids), [fresh], 0))
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 1
    assert "SKIP-XFAIL-NEW" in capsys.readouterr().err


def test_verify_allows_added_test(produced, tmp_path, capsys, monkeypatch):
    mp = _write_manifest(tmp_path, produced)
    ids = produced["collection"]["node_ids"]
    extra = "bootstrap/tests/test_newly_added.py::test_extra"
    # a superset of pinned (nothing dropped) + one new node, no new markers
    monkeypatch.setattr(G, "_collect", lambda repo=_REPO: (sorted(ids + [extra]), [], 0))
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 0
    output = capsys.readouterr().err
    assert "COLLECTION-ADDED" in output
    assert "UNPROTECTED-NEW: bootstrap/tests/test_newly_added.py" not in output


def test_node_added_to_existing_ordinary_file_is_not_unprotected_new(
        produced, tmp_path, capsys, monkeypatch):
    mp = _write_manifest(tmp_path, produced)
    ids = produced["collection"]["node_ids"]
    extra = "bootstrap/tests/test_agreement_retired.py::test_new_node"
    monkeypatch.setattr(G, "_collect", lambda repo=_REPO: (sorted(ids + [extra]), [], 0))
    G.verify(mp, anchor_ref=None, repo=_REPO)
    output = capsys.readouterr().err
    assert f"COLLECTION-ADDED: {extra}" in output
    assert "UNPROTECTED-NEW: bootstrap/tests/test_agreement_retired.py" not in output


def test_ordinary_file_and_node_deltas_are_notes(produced, tmp_path, capsys, monkeypatch):
    tampered = copy.deepcopy(produced)
    ordinary = "bootstrap/tests/test_agreement_retired.py"
    tampered["ordinary_test_files"][ordinary] = "0" * 64
    removed_file = "bootstrap/tests/test_removed_ordinary.py"
    tampered["ordinary_test_files"][removed_file] = "3" * 64
    mp = _write_manifest(tmp_path, tampered)
    original = G._ordinary_test_files(_REPO, produced["protected_roster"])
    monkeypatch.setattr(G, "_ordinary_test_files", lambda repo, roster: {
        **{k: v for k, v in original.items() if k != ordinary},
        ordinary: "1" * 64,
        "bootstrap/tests/test_new_ordinary.py": "2" * 64,
    })
    ids = set(produced["collection"]["node_ids"])
    removed = next(n for n in ids if n.startswith(ordinary + "::"))
    extra = "bootstrap/tests/test_new_ordinary.py::test_new"
    markers = set(produced["collection"]["skip_xfail_marked"])
    ordinary_marker = next(n for n in ids if n.startswith(ordinary + "::") and n not in markers)
    monkeypatch.setattr(G, "_collect", lambda repo=_REPO: (
        sorted((ids - {removed}) | {extra}), sorted(markers | {ordinary_marker}), 0))
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 0
    output = capsys.readouterr().err
    assert f"UNPROTECTED-CHANGED: {ordinary}" in output
    assert "UNPROTECTED-NEW: bootstrap/tests/test_new_ordinary.py" in output
    assert f"UNPROTECTED-REMOVED: {removed_file}" in output
    assert "COLLECTION-ORDINARY-DROPPED" in output
    assert "SKIP-XFAIL-ORDINARY" in output


def test_verify_holds_when_anchor_object_absent(produced, tmp_path, capsys):
    # A ref that does not carry the manifest at the fixtures path -> git show fails -> HOLD.
    # Use a synthetic non-existent object (stable: post-commit, HEAD now DOES carry it —
    # Codex confirmation Finding 4).
    mp = _write_manifest(tmp_path, produced)
    assert G.verify(mp, anchor_ref="0" * 40, repo=_REPO, do_collect=False) == 1
    assert "ANCHOR" in capsys.readouterr().err


def test_anchor_skipped_note_when_no_ref(produced, tmp_path, capsys):
    mp = _write_manifest(tmp_path, produced)
    G.verify(mp, anchor_ref=None, repo=_REPO, do_collect=False)
    assert "ANCHOR: skipped" in capsys.readouterr().err


def test_require_anchor_holds_without_ref(produced, tmp_path, capsys):
    # Unattended verification mode: a missing anchor is a HOLD (Codex confirmation Finding 3).
    mp = _write_manifest(tmp_path, produced)
    assert G.verify(mp, anchor_ref=None, repo=_REPO, require_anchor=True, do_collect=False) == 1
    assert "ANCHOR: required" in capsys.readouterr().err


def test_trusted_verifier_detects_tamper_in_separate_target_tree(produced, tmp_path):
    # Codex confirmation Finding 3 + 4-positive: trusted verifier CODE (this process) targets
    # a SEPARATE worktree via repo=, with a real committed anchor. Clean -> OK; a frozen-file
    # tamper in the target -> HOLD. Static-only (do_collect=False) to avoid a full test tree.
    import os
    import shutil
    import subprocess
    target = tmp_path / "target"
    for rel in produced["frozen_files"]:
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(_REPO / rel, dst)
    man = target / G._MANIFEST_REL
    man.parent.mkdir(parents=True, exist_ok=True)
    man.write_text(json.dumps(produced, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    subprocess.run(["git", "init", "-q"], cwd=target, check=True, env=env)
    subprocess.run(["git", "add", "-A"], cwd=target, check=True, env=env)
    subprocess.run(["git", "commit", "-q", "-m", "seed"], cwd=target, check=True, env=env)
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=target, capture_output=True,
                         text=True, env=env).stdout.strip()
    # clean target, anchor matches -> OK
    assert G.verify(man, anchor_ref=sha, repo=target, require_anchor=True, do_collect=False) == 0
    # tamper a frozen gate file in the target tree -> trusted code HOLDs
    victim = target / "bootstrap/security_check.py"
    victim.write_text(victim.read_text(encoding="utf-8") + "\n# tamper\n", encoding="utf-8")
    assert G.verify(man, anchor_ref=sha, repo=target, require_anchor=True, do_collect=False) == 1


# --- Codex cross-phase finding #1: the anchor must be EXTERNALLY trusted --------


def _init_repo_with_manifest(root: Path, manifest_text: str) -> str:
    """Init a git repo carrying gate_manifest.json at _MANIFEST_REL; return HEAD sha."""
    import subprocess
    root.mkdir(parents=True, exist_ok=True)

    def _sub(*a):
        return subprocess.run(["git", *a], cwd=str(root), check=True,
                              capture_output=True, text=True)

    _sub("init", "-q"); _sub("config", "user.email", "a@b.c"); _sub("config", "user.name", "t")
    mpath = root / G._MANIFEST_REL
    mpath.parent.mkdir(parents=True, exist_ok=True)
    mpath.write_text(manifest_text, encoding="utf-8")
    _sub("add", "-A"); _sub("commit", "-q", "-m", "manifest")
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(root),
                          capture_output=True, text=True).stdout.strip()


def _minimal_manifest_text(**extra) -> str:
    """A manifest that pins nothing, so only its anchor can make `verify` hold."""
    manifest = {
        "schema": G.SCHEMA,
        "interpreter": {"version_info": list(sys.version_info[:3])},
        "collection": {"node_ids": [], "skip_xfail_marked": []},
        "frozen_files": {}, "cascade_mutable": {}, "phase_mutable": {},
        "mapping_symbols": {}, **extra,
    }
    return json.dumps(manifest, indent=2, sort_keys=True) + "\n"


def _commit_in(repo: Path, manifest_text: str) -> str:
    """Commit ``manifest_text`` as the gate manifest in ``repo``; return the commit."""
    (repo / G._MANIFEST_REL).write_text(manifest_text, encoding="utf-8")
    for args in (("add", "-A"), ("commit", "-q", "-m", "manifest")):
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True,
                          capture_output=True, text=True).stdout.strip()


@pytest.mark.parametrize("attack", [
    "anchor-only-the-target-has",
    "anchor-only-the-target-has-with-a-GIT_DIR-decoy",
    "anchor-on-a-branch-the-trusted-ref-does-not-contain",
    "forged-manifest-under-the-trusted-anchor",
])
def test_verify_with_a_trusted_repo_holds_when_the_target_mints_its_own_anchor(
        tmp_path, monkeypatch, attack):
    """A target that can edit itself cannot make its own forged manifest pass:
    the expected manifest comes from the trusted repository, and the anchor has
    to be reachable from the trusted ref there.  A `GIT_DIR` pointing at the
    target's own repository (which holds the forged anchor) must not redirect
    those reads."""
    real_text = _minimal_manifest_text()
    forged_text = _minimal_manifest_text(forged_by_target=True)
    trusted = tmp_path / "trusted"
    trusted_anchor = _init_repo_with_manifest(trusted, real_text)
    target = tmp_path / "target"
    _init_repo_with_manifest(target, real_text)
    manifest = target / G._MANIFEST_REL

    def verdict(anchor: str) -> int:
        return G.verify(manifest, anchor_ref=anchor, repo=target, trusted_repo=trusted,
                        require_anchor=True, do_collect=False, out=io.StringIO())

    assert verdict(trusted_anchor) == 0, "precondition: a legitimate anchor passes"

    manifest.write_text(forged_text, encoding="utf-8")
    anchor = trusted_anchor
    if attack.startswith("anchor-only-the-target-has"):
        anchor = _commit_in(target, forged_text)
    elif attack.startswith("anchor-on-a-branch"):
        subprocess.run(["git", "checkout", "-q", "-b", "side"], cwd=trusted, check=True,
                       capture_output=True)
        anchor = _commit_in(trusted, forged_text)
        subprocess.run(["git", "checkout", "-q", "-"], cwd=trusted, check=True,
                       capture_output=True)
    if attack.endswith("with-a-GIT_DIR-decoy"):
        monkeypatch.setenv("GIT_DIR", str(target / ".git"))
    assert verdict(anchor) == 1


# ---------------------------------------------------------------------------
# The v1/v2 differential corpus.
#
# R1-C's gate: "Manifest v2 does not ship unless a differential corpus proves
# every v1 modification/deletion HOLD, addition disposition, cascade/phase
# exception, and collection rule remains at least as strict."  A disagreement
# stops the migration and retains v1.
# ---------------------------------------------------------------------------


def _as_v1(manifest: dict) -> dict:
    """The same manifest expressed in the v1 schema.

    v1 stored a bare digest per frozen path and had no object_format, so it
    could not compare mode or oid at all.  Deriving v1 *from* v2 keeps the two
    arms over identical content -- the only difference is what each schema is
    able to notice.
    """
    v1 = copy.deepcopy(manifest)
    v1["schema"] = G.SCHEMA_V1
    v1.pop("object_format", None)
    v1.pop("untracked_gate_files", None)
    v1["frozen_files"] = {rel: e["sha256"] if isinstance(e, dict) else e
                          for rel, e in manifest["frozen_files"].items()}
    return v1


def _target_tree(tmp_path: Path, manifest: dict) -> tuple[Path, Path, str]:
    """A committed target tree holding exactly the manifest's frozen files."""
    import os
    import shutil
    import subprocess
    target = tmp_path / "t"
    for rel in manifest["frozen_files"]:
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(_REPO / rel, dst)
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    subprocess.run(["git", "init", "-q"], cwd=target, check=True, env=env)
    subprocess.run(["git", "add", "-A"], cwd=target, check=True, env=env)
    subprocess.run(["git", "commit", "-q", "-m", "seed"], cwd=target, check=True,
                   env=env)
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=target,
                         capture_output=True, text=True, env=env).stdout.strip()
    return target, target / G._MANIFEST_REL, sha


def _verdict(manifest: dict, target: Path, man_path: Path, sha: str) -> int:
    man_path.parent.mkdir(parents=True, exist_ok=True)
    man_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    return G.verify(man_path, anchor_ref=None, repo=target,
                    require_anchor=False, do_collect=False)


class TestV1V2Differential:
    """v2 must be at least as strict as v1 on every disposition v1 had."""


    def test_deletion_holds_under_both(self, produced, tmp_path):
        target, man, sha = _target_tree(tmp_path, produced)
        (target / "bootstrap/security_check.py").unlink()
        assert _verdict(_as_v1(produced), target, man, sha) == 1
        assert _verdict(produced, target, man, sha) == 1


    def test_v2_notices_a_mode_change_that_v1_cannot(self, produced, tmp_path):
        """The capability v2 adds, stated as a test rather than a claim."""
        target, man, sha = _target_tree(tmp_path, produced)
        import subprocess
        subprocess.run(["git", "add", "-A"], cwd=target, check=True,
                       capture_output=True)
        subprocess.run(["git", "update-index", "--chmod=+x",
                        "bootstrap/security_check.py"], cwd=target, check=True,
                       capture_output=True)
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t",
                        "commit", "-q", "-m", "chmod"], cwd=target, check=True,
                       capture_output=True)
        tree_mode = subprocess.run(
            ["git", "ls-tree", "HEAD", "--", "bootstrap/security_check.py"],
            cwd=target, check=True, capture_output=True, text=True).stdout
        assert tree_mode.startswith("100755 blob ")
        # v1 compares content only, so the executable bit is invisible to it.
        assert _verdict(_as_v1(produced), target, man, sha) == 0
        assert _verdict(produced, target, man, sha) == 1

    def test_the_same_mode_change_HOLDs_when_git_cannot_be_asked(
            self, produced, tmp_path):
        """The silent-skip case, as a test.

        Same tree, same tampering, `.git` removed. `_object_format` returns
        None, and this used to reach *neither* branch: `live_blobs` stayed
        empty, every mode/oid comparison was skipped, and `verify` printed
        "OK -- gate integrity intact" over the exact state the node above HOLDs
        on. Absence was treated more leniently than strangeness -- an
        *unrecognised* format already HOLDs.

        `AGENTS.md`: "a tool that returns success without testing the claimed
        property is a worse defect than no tool, because it is silent."
        """
        import shutil, subprocess
        target, man, sha = _target_tree(tmp_path, produced)
        subprocess.run(["git", "add", "-A"], cwd=target, check=True,
                       capture_output=True)
        subprocess.run(["git", "update-index", "--chmod=+x",
                        "bootstrap/security_check.py"], cwd=target, check=True,
                       capture_output=True)
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t",
                        "commit", "-q", "-m", "chmod"], cwd=target, check=True,
                       capture_output=True)
        tree_mode = subprocess.run(
            ["git", "ls-tree", "HEAD", "--", "bootstrap/security_check.py"],
            cwd=target, check=True, capture_output=True, text=True).stdout
        assert tree_mode.startswith("100755 blob ")
        assert _verdict(produced, target, man, sha) == 1, "precondition"

        shutil.rmtree(target / ".git")

        assert _verdict(produced, target, man, sha) == 1, (
            "with the manifest pinning an object format and the target's "
            "unreadable, the pinned half of the contract is unverifiable -- "
            "that is a HOLD, not an OK")


@pytest.mark.parametrize("change, expected", [
    ("edit", "UNPROTECTED-CHANGED"),
    ("addition", "UNPROTECTED-NEW"),
    ("deletion", "UNPROTECTED-REMOVED"),
    ("rename", "UNPROTECTED-REMOVED"),
    ("marker", "SKIP-XFAIL-ORDINARY"),
])
def test_ordinary_changes_are_individually_reported_without_hold(
        produced, tmp_path, monkeypatch, change, expected):
    """Each ordinary change remains visible without blocking verification."""
    ordinary = "bootstrap/tests/test_agreement_retired.py"
    other = "bootstrap/tests/test_new_ordinary_matrix.py"
    node = next(n for n in produced["collection"]["node_ids"]
                if n.startswith(ordinary + "::")
                and n not in produced["collection"]["skip_xfail_marked"])
    manifest = copy.deepcopy(produced)
    current = G._ordinary_test_files(_REPO, produced["protected_roster"])
    ids = set(produced["collection"]["node_ids"])
    marks = set(produced["collection"]["skip_xfail_marked"])
    if change == "edit":
        current[ordinary] = "0" * 64
    elif change == "addition":
        current[other] = "1" * 64
        ids.add(other + "::test_new")
    elif change == "deletion":
        del current[ordinary]
        ids = {n for n in ids if not n.startswith(ordinary + "::")}
    elif change == "rename":
        current[other] = current.pop(ordinary)
        ids = {n.replace(ordinary + "::", other + "::", 1) for n in ids}
    else:
        marks.add(node)
    monkeypatch.setattr(G, "_ordinary_test_files", lambda repo, roster: current)
    monkeypatch.setattr(G, "_collect", lambda repo=_REPO: (sorted(ids), sorted(marks), 0))
    output = io.StringIO()
    assert G.verify(_write_manifest(tmp_path, manifest), repo=_REPO, out=output) == 0
    assert expected in output.getvalue()
    if change == "rename":
        assert "UNPROTECTED-NEW" in output.getvalue()


# Declared exception (internal hook): Hook: G._collect monkeypatched to report protected changes; a real tamper needs a full collection run of a target tree.
@pytest.mark.parametrize("change, expected", [
    ("edit", "FROZEN-MODIFIED"),
    ("addition", "FROZEN-MODIFIED"),
    ("deletion", "COLLECTION-DROPPED"),
    ("rename", "COLLECTION-DROPPED"),
    ("marker", "SKIP-XFAIL-NEW"),
])
def test_protected_changes_individually_hold(
        produced, tmp_path, monkeypatch, change, expected):
    """A protected byte change, node loss or new marker blocks verification."""
    manifest = copy.deepcopy(produced)
    protected = "bootstrap/tests/test_ast_attest.py"
    ids = set(produced["collection"]["node_ids"])
    marks = set(produced["collection"]["skip_xfail_marked"])
    node = next(n for n in ids if n.startswith(protected + "::") and n not in marks)
    if change in ("edit", "addition"):
        # The manifest pins the old bytes; a mismatch models either edit.
        entry = manifest["frozen_files"][protected]
        if isinstance(entry, dict):
            entry["sha256"] = "0" * 64
        else:
            manifest["frozen_files"][protected] = "0" * 64
        if change == "addition":
            ids.add(protected + "::test_new")
    elif change in ("deletion", "rename"):
        ids.remove(node)
        if change == "rename":
            ids.add(node + "_renamed")
    else:
        marks.add(node)
    monkeypatch.setattr(G, "_collect", lambda repo=_REPO: (sorted(ids), sorted(marks), 0))
    output = io.StringIO()
    assert G.verify(_write_manifest(tmp_path, manifest), repo=_REPO, out=output) == 1
    assert expected in output.getvalue()
