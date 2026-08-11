"""Contract for the gate-integrity manifest tool (six-proposal superplan pre-run
gate-control prerequisite; Codex S2 / R2-2).

Pins: produce() captures the frozen gate surface + cascade-mutable set + the
collection identity; the frozen set excludes cascade-mutable files and the
manifest artifact itself; and verify() HOLDs on every tampering class
(frozen-file edit, dropped node, new skip/xfail marker, interpreter-minor
mismatch, broken external anchor) while allowing additions. Stdlib only.
"""
from __future__ import annotations

import ast
import copy
import json
import sys
from pathlib import Path

import pytest

from bootstrap.tests import _gate_manifest as G

_REPO = Path(__file__).resolve().parents[2]


def _write_manifest(tmp_path, manifest: dict) -> Path:
    p = tmp_path / "gate_manifest.json"
    p.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return p


@pytest.fixture(scope="module")
def produced() -> dict:
    """Produce once (a full collection subprocess) and share across tests."""
    return G.produce(_REPO)


def test_produce_has_the_expected_shape(produced):
    assert produced["schema"] == G.SCHEMA
    for key in ("interpreter", "gate_commands", "collection", "frozen_files",
                "cascade_mutable", "mapping_symbols"):
        assert key in produced
    assert produced["collection"]["node_count"] == len(produced["collection"]["node_ids"])
    assert produced["collection"]["node_count"] > 100  # the real suite is large
    for sym in ("_MODULE_MAPPINGS", "_SKILLS_MAPPINGS", "_CORE_MAPPINGS"):
        assert produced["mapping_symbols"][sym]["baseline_digest"]


def test_frozen_set_boundary(produced):
    frozen = produced["frozen_files"]
    # known gate files are pinned
    assert "bootstrap/tests/test_ast_attest.py" in frozen
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
    # the three phase-split facade targets are NOT frozen — they are phase_mutable
    assert "templates/modules/team-gated/intent.py" not in frozen
    assert "templates/modules/default-on/onboarding_activate.py" not in frozen
    assert "templates/modules/default-on/lifecycle_metrics.py" not in frozen
    assert set(produced["phase_mutable"]) == set(G.PHASE_SPLIT_TARGETS)


def test_verify_clean_tree_is_ok(produced, tmp_path, capsys):
    mp = _write_manifest(tmp_path, produced)
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 0
    assert "OK — gate integrity intact" in capsys.readouterr().err


def test_verify_holds_on_frozen_file_modification(produced, tmp_path, capsys):
    tampered = copy.deepcopy(produced)
    # pretend a pinned gate file was edited (wrong sha)
    tampered["frozen_files"]["bootstrap/tests/test_ast_attest.py"] = "0" * 64
    mp = _write_manifest(tmp_path, tampered)
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 1
    assert "FROZEN-MODIFIED" in capsys.readouterr().err


def test_verify_holds_on_dropped_node(produced, tmp_path, capsys):
    tampered = copy.deepcopy(produced)
    # pin a node-ID that collection will NOT produce -> reduced collection
    tampered["collection"]["node_ids"].append(
        "bootstrap/tests/test_does_not_exist.py::test_phantom")
    mp = _write_manifest(tmp_path, tampered)
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 1
    assert "COLLECTION-DROPPED" in capsys.readouterr().err


def test_verify_holds_on_interpreter_minor_mismatch(produced, tmp_path, capsys):
    tampered = copy.deepcopy(produced)
    tampered["interpreter"]["version_info"] = [3, 11, 0]
    mp = _write_manifest(tmp_path, tampered)
    assert G.verify(mp, anchor_ref=None, repo=_REPO) == 1
    assert "INTERPRETER" in capsys.readouterr().err


def test_verify_holds_on_new_skip_marker(produced, tmp_path, capsys, monkeypatch):
    mp = _write_manifest(tmp_path, produced)
    ids = produced["collection"]["node_ids"]
    pinned_marked = set(produced["collection"]["skip_xfail_marked"])
    # simulate the run adding a skip/xfail marker to a currently-UNMARKED test
    fresh = next(i for i in ids if i not in pinned_marked)
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
    assert "COLLECTION-ADDED" in capsys.readouterr().err


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


def test_anchor_from_trusted_repo_refuses_target_owned_forge(tmp_path):
    """A target that can edit itself must NOT be able to mint its own anchor: with
    --trusted-repo, the expected manifest comes from the trusted repo and the
    anchor must be reachable from a trusted ref there (Codex cross-phase #1)."""
    real = '{"gate": "real"}\n'
    forged = '{"gate": "FORGED-by-target"}\n'
    trusted = tmp_path / "trusted"
    target = tmp_path / "target"
    trusted_anchor = _init_repo_with_manifest(trusted, real)
    target_anchor = _init_repo_with_manifest(target, forged)

    # 1. A target-only anchor is NOT reachable from the trusted ref -> HOLD.
    holds, _ = G._check_anchor(target_anchor, forged, repo=target,
                               trusted_repo=trusted, trusted_ref="HEAD")
    assert holds and any("not reachable" in h.lower() for h in holds)

    # 2. The trusted anchor is honored, but a forged working-tree manifest differs
    #    from the immutable trusted object -> HOLD.
    holds, _ = G._check_anchor(trusted_anchor, forged, repo=target,
                               trusted_repo=trusted, trusted_ref="HEAD")
    assert holds and any("differs from the immutable" in h for h in holds)

    # 3. Legit: the trusted anchor + a matching manifest -> no holds.
    holds, _ = G._check_anchor(trusted_anchor, real, repo=target,
                               trusted_repo=trusted, trusted_ref="HEAD")
    assert holds == []

    # 4. No --trusted-repo: falls back to the target with a loud NOTE (documented
    #    residual: a target-owned object comparison, not external anchoring).
    holds, notes = G._check_anchor(target_anchor, forged, repo=target,
                                   trusted_repo=None, trusted_ref="HEAD")
    assert holds == [] and any("TARGET repo" in n for n in notes)


# ---------------------------------------------------------------------------
# Plan `git-native-security-foundations`, Chunk A4: one guarded Git boundary.
# ---------------------------------------------------------------------------


def test_no_direct_git_subprocess_bypasses_the_launcher():
    """Every git call in this module routes through `_git`.

    Before Chunk A the anchor-reachability check and the manifest read ran bare
    `["git", ...]` with the operator's whole environment, so `GIT_DIR`,
    `GIT_CONFIG_GLOBAL` and `GIT_REPLACE_REF_BASE` could steer two decisions
    that gate a release.

    Perturbation: restore either call as a bare `subprocess.run(["git", ...])`.
    Red.
    """
    src = (Path(__file__).resolve().parent / "_gate_manifest.py").read_text(
        encoding="utf-8")
    tree = ast.parse(src)
    offenders = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "run"):
            continue
        if not node.args:
            continue
        first = node.args[0]
        if isinstance(first, ast.List) and first.elts:
            head = first.elts[0]
            if isinstance(head, ast.Constant) and head.value == "git":
                # The launcher itself is the one permitted site.
                fn = _enclosing_function(tree, node)
                if fn != "_git":
                    offenders.append((fn, node.lineno))
    assert not offenders, f"git subprocess outside the launcher: {offenders}"


def _enclosing_function(tree: ast.AST, target: ast.AST) -> str | None:
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for inner in ast.walk(fn):
                if inner is target:
                    return fn.name
    return None


def test_the_launcher_strips_every_git_environment_variable():
    """`GIT_*` is dropped wholesale, not denylisted by name."""
    src = (Path(__file__).resolve().parent / "_gate_manifest.py").read_text(
        encoding="utf-8")
    assert 'if not k.startswith("GIT_")' in src


# ---------------------------------------------------------------------------
# Chunk D4: the v1/v2 differential corpus.
#
# R1-C's gate: "Manifest v2 does not ship unless a differential corpus proves
# every v1 modification/deletion HOLD, addition disposition, cascade/phase
# exception, and collection rule remains at least as strict."  A disagreement
# stops the migration and retains v1 (fence M5).
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

    def test_a_clean_tree_passes_under_both(self, produced, tmp_path):
        target, man, sha = _target_tree(tmp_path, produced)
        assert _verdict(_as_v1(produced), target, man, sha) == 0
        assert _verdict(produced, target, man, sha) == 0

    def test_modification_holds_under_both(self, produced, tmp_path):
        target, man, sha = _target_tree(tmp_path, produced)
        victim = target / "bootstrap/security_check.py"
        victim.write_text(victim.read_text(encoding="utf-8") + "\n# tamper\n",
                          encoding="utf-8")
        assert _verdict(_as_v1(produced), target, man, sha) == 1
        assert _verdict(produced, target, man, sha) == 1

    def test_deletion_holds_under_both(self, produced, tmp_path):
        target, man, sha = _target_tree(tmp_path, produced)
        (target / "bootstrap/security_check.py").unlink()
        assert _verdict(_as_v1(produced), target, man, sha) == 1
        assert _verdict(produced, target, man, sha) == 1

    def test_v2_is_never_more_permissive_across_the_corpus(self, produced, tmp_path):
        """The gate R1-C actually names: no scenario where v1 HOLDs and v2 does not."""
        scenarios = {
            "clean": lambda t: None,
            "modified": lambda t: (t / "bootstrap/security_check.py").write_text(
                "# tamper\n", encoding="utf-8"),
            "deleted": lambda t: (t / "bootstrap/security_check.py").unlink(),
            "second-file-modified": lambda t: (
                t / "bootstrap/verify_integrity.py").write_text(
                    "# tamper\n", encoding="utf-8")
            if (_REPO / "bootstrap/verify_integrity.py").exists() else None,
        }
        regressions = []
        for name, mutate in scenarios.items():
            target, man, sha = _target_tree(tmp_path / name, produced)
            mutate(target)
            v1 = _verdict(_as_v1(produced), target, man, sha)
            v2 = _verdict(produced, target, man, sha)
            if v1 == 1 and v2 != 1:
                regressions.append(name)
        assert not regressions, (
            f"v2 is MORE PERMISSIVE than v1 for: {regressions}. R1-C stops the "
            f"migration and retains v1 (fence M5).")

    def test_v2_notices_a_mode_change_that_v1_cannot(self, produced, tmp_path):
        """The capability v2 adds, stated as a test rather than a claim."""
        target, man, sha = _target_tree(tmp_path, produced)
        victim = target / "bootstrap/security_check.py"
        victim.chmod(0o755)
        import subprocess
        subprocess.run(["git", "add", "-A"], cwd=target, check=True,
                       capture_output=True)
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t",
                        "commit", "-q", "-m", "chmod"], cwd=target, check=True,
                       capture_output=True)
        # v1 compares content only, so the executable bit is invisible to it.
        assert _verdict(_as_v1(produced), target, man, sha) == 0
        assert _verdict(produced, target, man, sha) == 1
