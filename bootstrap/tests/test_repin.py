"""Tests for `scripts/repin.py`: the reading order, `status` and the manifest view.

Every test runs against a scratch repository that has its own anchor
(`refs/cairn/gate-anchor`) pinning its own copies of the gate files, with
`HOME` pointed at a scratch folder.  Nothing here reads the real anchor, a real
key or `~/.ssh`.  Each refusal test has a control that passes when the
condition is fine, so a refusal is shown to be this check and not a broken bed.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

from bootstrap.tests import _ast_attest as A
from bootstrap.tests import _gate_manifest as GM

REAL = Path(__file__).resolve().parents[2]
PY = sys.executable

#: The files whose bytes must equal the anchor's before `repin` imports anything.
#: Retyped here so the test, not a shared constant, states the contract.
LISTED = ["bootstrap/tests/__init__.py", "bootstrap/tests/_ast_attest.py",
          "bootstrap/tests/_gate_manifest.py", "bootstrap/tests/_gate_preflight.py",
          "bootstrap/tests/_gate_reanchor.py", "bootstrap/tests/_gate_transition.py",
          "bootstrap/tests/_oracle.py", "bootstrap/tests/_oracle_activation.py",
          "bootstrap/tests/_oracle_trust.py", "scripts/reanchor_ceremony.py"]
SESSION = ["tools/session.py", "templates/skills/_lib/session.py"]
ENGINE = "bootstrap/_scaffold/mod.py"
BASELINE = "bootstrap/tests/fixtures/scaffold_ast_baseline.json"
KNOWN_NEW = "bootstrap/tests/fixtures/scaffold_ast_known_new.json"
MANIFEST = "bootstrap/tests/fixtures/gate_manifest.json"


def _dump(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True) + "\n"


class Bed:
    """A scratch repository with its own anchor, and the means to run `repin` in it."""

    def __init__(self, root: Path):
        self.root = root
        self.repo = root / "repo"
        self.home = root / "home"
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), "LC_ALL": "C",
                    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}

    def git(self, *args, check=True, input=None, text=True):
        r = subprocess.run(
            ["git", "-C", str(self.repo), "-c", "user.name=t", "-c", "user.email=t@t",
             "-c", "commit.gpgsign=false", *args],
            capture_output=True, text=text, input=input, env=self.env, check=False)
        assert r.returncode == 0 or not check, r.stderr
        return r

    def write(self, rel, data):
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        (path.write_bytes if isinstance(data, bytes) else path.write_text)(data)

    def read(self, rel) -> str:
        return (self.repo / rel).read_text()

    def commit(self, message="change"):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD").stdout.strip()

    def pin(self, message="anchor"):
        """Rewrite the manifest from the worktree, commit, and move the anchor."""
        frozen = {}
        for rel in GM._frozen_files(self.repo):
            raw = (self.repo / rel).read_bytes()
            oid = self.git("hash-object", "--no-filters", rel).stdout.strip()
            frozen[rel] = {"sha256": hashlib.sha256(raw).hexdigest(), "mode": "100644", "oid": oid}
        self.write(MANIFEST, _dump({
            "schema": "cairn-gate-manifest/v2", "object_format": "sha1",
            "interpreter": {"version_info": list(sys.version_info[:3])},
            "gate_commands": [], "collection": {"node_ids": [], "skip_xfail_marked": []},
            "frozen_files": frozen, "cascade_mutable": {}, "phase_mutable": {},
            "mapping_symbols": {}}))
        head = self.commit(message)
        self.git("update-ref", "refs/cairn/gate-anchor", head)
        return head

    def run(self, *args, cwd=None, stdin=subprocess.DEVNULL):
        return subprocess.run([PY, str(self.repo / "scripts/repin.py"), *args],
                              cwd=cwd or self.repo, env=self.env, stdin=stdin,
                              capture_output=True, text=True, check=False)

    def tree_hash(self) -> str:
        """One digest over every file and name under the repository, `.git` included."""
        h = hashlib.sha256()
        for path in sorted(self.repo.rglob("*")):
            h.update(str(path.relative_to(self.repo)).encode())
            if path.is_file() and not path.is_symlink():
                h.update(path.read_bytes())
        return h.hexdigest()

    def marker(self, name="marker") -> Path:
        return self.root / name


def marker_code(path: Path) -> str:
    return f"\nopen({str(path)!r}, 'w').close()\n"


@pytest.fixture(scope="module")
def template(tmp_path_factory):
    root = tmp_path_factory.mktemp("template")
    bed = Bed(root)
    (bed.repo).mkdir()
    (bed.home).mkdir()
    bed.git("init", "-q", "-b", "main")
    for rel in [*LISTED, *SESSION, "scripts/repin.py"]:
        bed.write(rel, (REAL / rel).read_bytes())
    bed.write(ENGINE, "def f():\n    return 1\n")
    bed.write(BASELINE, _dump(A.digest_module(bed.repo / ENGINE)))
    bed.write(KNOWN_NEW, _dump({}))
    bed.write("dev/plans/widget-plan.md", "# Plan\n\n**Status**: implementing\n")
    bed.write("dev/proposals/2026-10-01-someone-widget-slug.md", "# P\n\n**Status**: accepted\n")
    bed.pin()
    return root


@pytest.fixture
def bed(template, tmp_path):
    root = tmp_path / "bed"
    shutil.copytree(template, root, symlinks=True)
    return Bed(root)


def ok(r):
    assert r.returncode == 0, r.stderr + r.stdout
    return r.stdout


def refused(r, needle=None):
    assert r.returncode == 2, r.stderr + r.stdout
    assert "nothing was written" in r.stderr
    if needle:
        assert needle in r.stderr, r.stderr
    return r.stderr


# --------------------------------------------------------------------------
# the reading order: what is extracted, and what is compared before import
# --------------------------------------------------------------------------

def test_the_extraction_ignores_gitattributes(bed):
    """`git archive` would drop an export-ignore file and rewrite an export-subst
    one; the tree is read from raw objects, so neither can shrink what is checked."""
    control = ok(bed.run("status"))
    assert "over 1 committed engine modules" in control
    bed.write(".gitattributes", f"{ENGINE} export-ignore\nscripts/reanchor_ceremony.py export-subst\n")
    bed.write("scripts/reanchor_ceremony.py",
              bed.read("scripts/reanchor_ceremony.py") + "\n# $Format:%H$\n")
    bed.pin()
    archived = bed.git("archive", "HEAD", "--format=tar", text=False).stdout
    with tarfile.open(fileobj=io.BytesIO(archived)) as tar:
        assert ENGINE not in tar.getnames(), "the instrument is wrong: git archive kept the file"
    out = ok(bed.run("status"))
    assert "over 1 committed engine modules" in out


def test_a_case_colliding_tree_refuses_before_import(bed):
    """Two tree names that are one file on a case-insensitive disk leave the
    bytes written last under the imported name; the tree is refused."""
    twin = "bootstrap/tests/_GATE_MANIFEST.py"
    blob = bed.git("hash-object", "-w", "--stdin", input="x = 1\n").stdout.strip()
    bed.git("update-index", "--add", "--cacheinfo", f"100644,{blob},{twin}")
    bed.git("commit", "-q", "-m", "collide")
    refused(bed.run("status"), "are one name")
    bed.git("rm", "-q", "--cached", twin)
    bed.git("commit", "-q", "-m", "uncollide")
    ok(bed.run("status"))


@pytest.mark.parametrize("rel", LISTED)
def test_each_imported_file_is_byte_compared_with_the_anchor_before_import(bed, rel):
    bed.write(rel, bed.read(rel) + marker_code(bed.marker()))
    bed.commit("mutate a listed file")
    refused(bed.run("status"), rel)
    assert not bed.marker().exists(), "the mutated file ran before it was compared"
    bed.pin()
    ok(bed.run("status"))
    assert bed.marker().exists(), "the control is wrong: an anchored marker should run"


def test_a_tracked_compiled_file_refuses(bed):
    bed.write("scripts/__pycache__/stale.cpython-313.pyc", b"\0")
    bed.commit("track a compiled file")
    refused(bed.run("status"), "compiled file is tracked")
    bed.git("rm", "-q", "-r", "scripts/__pycache__")
    bed.git("commit", "-q", "-m", "untrack")
    ok(bed.run("status"))


def test_a_loaded_local_module_outside_the_list_refuses(bed):
    """A listed module that imports an unlisted local module is seen loaded and refused."""
    twin = "bootstrap/tests/_oracle_trust.py"
    bed.write("bootstrap/tests/planted.py", "VALUE = 1\n")
    bed.pin()
    ok(bed.run("status"))
    bed.write(twin, bed.read(twin) + "\nfrom bootstrap.tests import planted\n")
    bed.pin()
    refused(bed.run("status"), "bootstrap.tests.planted")


@pytest.mark.parametrize("subdir", ["scripts", "bootstrap/tests", "."])
def test_a_committed_module_named_like_the_standard_library_does_not_run(bed, subdir):
    # `tarfile` and `base64` are imported only after the extraction joins the
    # search path, so they are the names an inserted path would let win.
    names = ("hashlib", "json", "subprocess", "tarfile", "base64")
    for name in names:
        bed.write(f"{subdir}/{name}.py", marker_code(bed.marker(name)))
    bed.commit("shadow the standard library")
    ok(bed.run("status"))
    for name in names:
        assert not bed.marker(name).exists(), f"a committed {name}.py shadowed the standard library"
    # control: a bare `python` run from that folder does run the shadowing module
    bed.write(f"{subdir}/probe.py", "import hashlib\n")
    subprocess.run([PY, str(bed.repo / subdir / "probe.py")], cwd=bed.repo, env=bed.env, check=False)
    assert bed.marker("hashlib").exists()


def test_the_repin_process_runs_isolated(bed):
    out = ok(bed.run("status"))
    line = re.search(r"^process\s+isolated=(\w+)\s+compiled files go to (\S+)$", out, re.M)
    assert line and line.group(1) == "True"
    assert not line.group(2).startswith(str(bed.repo))
    assert re.search(r"AST child isolated=True, compiled files go to \S+/pyc-\S+", out)


def test_a_planted_compiled_file_in_the_working_tree_does_not_run(bed):
    """An unchecked .pyc beside a gate module runs under a bare import but never
    under `repin`, which imports from its own extraction with a fresh bytecode folder."""
    import py_compile
    src = bed.root / "evil.py"
    src.write_text(marker_code(bed.marker()))
    cache = bed.repo / "bootstrap/tests/__pycache__"
    cache.mkdir()
    py_compile.compile(str(src), cfile=str(cache / f"_gate_manifest.{sys.implementation.cache_tag}.pyc"),
                       invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)
    ok(bed.run("status"))
    assert not bed.marker().exists()
    subprocess.run([PY, "-c", "import sys; sys.path.insert(0, 'bootstrap/tests'); import _gate_manifest"],
                   cwd=bed.repo, env=bed.env, check=False)
    assert bed.marker().exists(), "the control is wrong: the planted file should run unprotected"


def test_an_edited_session_module_at_head_does_not_run(bed):
    """The encoder comes from the anchor's blob; HEAD's copies of the module never run."""
    for rel in SESSION:
        bed.write(rel, marker_code(bed.marker()) + bed.read(rel))
    bed.write(ENGINE, bed.read(ENGINE) + "\ndef g():\n    return 2\n")
    bed.commit("edit session.py\x1b[31m\rspoof")
    out = ok(bed.run("status"))
    assert not bed.marker().exists()
    assert "\x1b" not in out and "\r" not in out
    assert "\\x1b[31m\\x0dspoof" in out
    anchored = bed.git("rev-parse", "refs/cairn/gate-anchor:tools/session.py").stdout.strip()
    assert anchored in out, "the first screen does not name the anchor's encoder blob"


def test_an_ordinary_commit_subject_prints_unchanged(bed):
    bed.write(ENGINE, bed.read(ENGINE) + "\ndef g():\n    return 2\n")
    bed.commit("Plain subject, with punctuation: (ok)")
    assert "Plain subject, with punctuation: (ok)" in ok(bed.run("status"))


def test_a_tree_with_no_engine_module_refuses(bed):
    bed.git("rm", "-q", ENGINE)
    bed.commit("no engine")
    refused(bed.run("status"), "engine set is empty")
    bed.write(ENGINE, "def f():\n    return 1\n")
    bed.commit("engine back")
    ok(bed.run("status"))


def test_status_writes_nothing(bed):
    before = bed.tree_hash()
    ok(bed.run("status"))
    assert bed.tree_hash() == before


def test_an_untracked_engine_module_is_absent_until_committed(bed):
    bed.write("bootstrap/_scaffold/extra.py", "def extra():\n    return 3\n")
    assert "over 1 committed engine modules" in ok(bed.run("status"))
    bed.commit("add extra")
    out = ok(bed.run("status"))
    assert "over 2 committed engine modules" in out and "known-new ADDED  FunctionDef:extra" in out


def test_head_moving_during_a_run_refuses(bed):
    code = f"""
import importlib.util, subprocess, sys, tempfile
from pathlib import Path
sys.pycache_prefix = tempfile.mkdtemp()
spec = importlib.util.spec_from_file_location("repin", {str(bed.repo / 'scripts/repin.py')!r})
R = importlib.util.module_from_spec(spec); sys.modules["repin"] = R; spec.loader.exec_module(R)
ctx = R.boot(Path({str(bed.repo)!r}), Path(tempfile.mkdtemp()))
R.check_head(ctx)
print("same head passes")
subprocess.run(["git", "-C", {str(bed.repo)!r}, "-c", "user.name=t", "-c", "user.email=t@t",
                "commit", "-q", "--allow-empty", "-m", "move"], check=True)
try:
    R.check_head(ctx)
except R.Refuse as exc:
    print("refused", exc)
"""
    r = subprocess.run([PY, "-I", "-c", code], capture_output=True, text=True, env=bed.env)
    assert "same head passes" in r.stdout and "refused" in r.stdout, r.stdout + r.stderr


def test_the_status_command_reads_only_the_fixed_environment_variables():
    """A tripwire, not a proof: no environment variable steers a check.  The one
    read of the environment filters it down for git."""
    reads = [ln for ln in (REAL / "scripts/repin.py").read_text().splitlines() if "os.environ" in ln]
    assert len(reads) == 1 and "GIT_" in reads[0], reads


# --------------------------------------------------------------------------
# what `status` shows
# --------------------------------------------------------------------------

def test_provenance_names_the_plan_a_commit_message_cites(bed):
    bed.write(ENGINE, bed.read(ENGINE) + "\ndef g():\n    return 2\n")
    bed.commit("Plan widget-plan C1: add g")
    bed.write(ENGINE, bed.read(ENGINE) + "\ndef h():\n    return 3\n")
    bed.commit("add h with no reference")
    out = ok(bed.run("status"))
    assert "the message names `widget-plan` (status `implementing`)" in out
    assert "the message names no plan or proposal" in out
    assert "Commits since the last pin that touched those files: 2" in out


@pytest.mark.parametrize("name,state", [("anchored", "scripts/repin.py: anchored"),
                                        ("edited", "scripts/repin.py: differs from the anchor"),
                                        ("unpinned", "scripts/repin.py: no anchored entry")])
def test_status_says_whether_repin_itself_is_anchored(bed, name, state):
    if name == "edited":
        bed.write("scripts/repin.py", bed.read("scripts/repin.py") + "\n# an edit\n")
        bed.commit("edit repin")
    if name == "unpinned":
        manifest = json.loads(bed.read(MANIFEST))
        del manifest["frozen_files"]["scripts/repin.py"]
        bed.write(MANIFEST, _dump(manifest))
        bed.commit("manifest without repin")
        bed.git("update-ref", "refs/cairn/gate-anchor", "HEAD")
    assert state in ok(bed.run("status"))


def test_status_shows_a_closure_member_that_differs_from_the_anchor(bed):
    assert "closure  0 of 10 authority files differ" in ok(bed.run("status"))
    bed.write("bootstrap/REANCHOR_RUNBOOK.md", "# runbook\n")
    bed.write("bootstrap/reanchor.sh", "#!/bin/sh\n")
    bed.write("dev/.cairn/allowed_signers", "x ssh-ed25519 AAAA\n")
    bed.pin("closure files appear")
    bed.write("bootstrap/REANCHOR_RUNBOOK.md", "# runbook, edited\n")
    bed.commit("edit the runbook")
    out = ok(bed.run("status"))
    assert "closure  1 of 10 authority files differ" in out and "bootstrap/REANCHOR_RUNBOOK.md" in out


def test_a_different_interpreter_minor_is_shown(bed):
    manifest = json.loads(bed.read(MANIFEST))
    manifest["interpreter"]["version_info"] = [3, 99, 0]
    bed.write(MANIFEST, _dump(manifest))
    bed.commit("pin another minor")
    bed.git("update-ref", "refs/cairn/gate-anchor", "HEAD")
    assert "DIFFERENT MINOR" in ok(bed.run("status"))


def test_an_ast_pin_owed_lists_every_changed_symbol(bed):
    assert "pin owed: no" in ok(bed.run("status"))
    bed.write(ENGINE, "def f():\n    return 2\n")
    bed.commit("change f")
    out = ok(bed.run("status"))
    assert re.search(r"CHANGED  FunctionDef:f  in bootstrap/_scaffold/mod.py  \w{16} -> \w{16}", out)
    assert "pin owed: yes" in out


# --------------------------------------------------------------------------
# manifest status
# --------------------------------------------------------------------------

def test_manifest_status_lists_drift_and_says_it_skips_collection(bed):
    out = ok(bed.run("status"))
    assert "FROZEN-MODIFIED: 0" in out and "FROZEN-MISSING: 0" in out and "FROZEN-NEW: 0" in out
    bed.write("scripts/old_check.py", "A = 1\n")
    bed.pin()
    bed.git("rm", "-q", "scripts/old_check.py")
    bed.write("bootstrap/tests/test_new_thing.py", "def test_x():\n    pass\n")
    bed.write("bootstrap/tests/fixtures/extra.json", "{}\n")
    bed.commit("drift")
    out = ok(bed.run("status"))
    assert "FROZEN-MISSING: 1" in out and "scripts/old_check.py" in out
    assert "FROZEN-NEW: 2" in out and "bootstrap/tests/test_new_thing.py" in out
    assert "does not check test collection" in out


def test_manifest_status_lists_a_modified_frozen_file(bed):
    bed.write("scripts/check_thing.py", "A = 1\n")
    bed.pin()
    bed.write("scripts/check_thing.py", "A = 2\n")
    bed.commit("edit a frozen file")
    out = ok(bed.run("status"))
    assert "FROZEN-MODIFIED: 1" in out and "scripts/check_thing.py" in out


def test_dropped_nodes_with_a_surviving_file_print_first(bed, tmp_path):
    saved = tmp_path / "verify.txt"
    saved.write_text("  COLLECTION-DROPPED: bootstrap/tests/gone_file.py::test_a (reduced)\n"
                     "  COLLECTION-DROPPED: bootstrap/tests/_gate_manifest.py::test_b (reduced)\n")
    out = ok(bed.run("status", "--dropped-from", str(saved)))
    tail = out[out.index("Dropped test nodes"):]
    assert tail.index("_gate_manifest.py::test_b") < tail.index("gone_file.py::test_a")
    assert "1 sit in a test file that still exists" in tail
