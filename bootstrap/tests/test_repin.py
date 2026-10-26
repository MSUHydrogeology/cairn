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
import pty
import re
import select
import shutil
import signal
import subprocess
import sys
import tarfile
import time
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
        self.sign = False
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), "LC_ALL": "C",
                    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}

    def git(self, *args, check=True, input=None, text=True):
        r = subprocess.run(
            ["git", "-C", str(self.repo), "-c", "user.name=t", "-c", "user.email=t@t",
             "-c", f"commit.gpgsign={str(self.sign).lower()}", *args],
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


@pytest.mark.parametrize("verb", ["status", "package"])
@pytest.mark.parametrize("subdir", ["scripts", "bootstrap/tests", "."])
def test_a_committed_module_named_like_the_standard_library_does_not_run(bed, subdir, verb):
    # `tarfile` and `base64` are imported only after the extraction joins the
    # search path, so they are the names an inserted path would let win.
    names = ("hashlib", "json", "subprocess", "tarfile", "base64")
    for name in names:
        bed.write(f"{subdir}/{name}.py", marker_code(bed.marker(name)))
    bed.commit("shadow the standard library")
    ok(bed.run(verb))
    for name in names:
        assert not bed.marker(name).exists(), f"a committed {name}.py shadowed the standard library"
    # control: a bare `python` run from that folder does run the shadowing module
    bed.write(f"{subdir}/probe.py", "import hashlib\n")
    subprocess.run([PY, str(bed.repo / subdir / "probe.py")], cwd=bed.repo, env=bed.env, check=False)
    assert bed.marker("hashlib").exists()


@pytest.mark.parametrize("verb", ["status", "package", "ceremony"])
@pytest.mark.parametrize("shape,bare_import", [("bootstrap/__init__.py", "bootstrap"), ("scripts/__init__.py", "scripts"),
                                               ("scripts.py", "scripts"), ("bootstrap.py", "bootstrap")])
def test_a_committed_parent_package_or_module_does_not_run_and_cannot_hide(bed, shape, bare_import, verb):
    """`bootstrap` and `scripts` are plain folders in the commit.  Whatever a tracked
    `__init__.py` or same-named module holds runs only if the import system finds it, and
    `repin` never puts the extraction on its search path.  The payload also blanks its own
    `__file__`, the way a check that trusts the module's word about itself is beaten."""
    bed.write(shape, marker_code(bed.marker()) + "__file__ = None\n")
    bed.commit("add a parent package marker")
    args = {"status": [], "package": [],
            "ceremony": ["--values", str(bed.root / "values"), "--ceremony-dir", str(bed.root / "cd")]}[verb]
    r = bed.run(verb, *args)
    if verb == "ceremony":
        refused(r, "must both be a terminal")
    else:
        ok(r)
    assert not bed.marker().exists(), f"the committed {shape} ran inside the repin process"
    # control: a bare import from the checkout runs it, so the marker can fire
    subprocess.run([PY, "-c", f"import {bare_import}"], cwd=bed.repo, env=bed.env, check=False)
    assert bed.marker().exists(), "the control is wrong: importing it should write the marker"


@pytest.mark.parametrize("hide", ["__file__ = None", "__file__ = None\n__spec__ = None"])
def test_a_module_loaded_outside_the_list_is_refused_even_when_it_blanks_its_own_file_and_spec(bed, hide):
    """The post-import check reads where the import system loaded a module from, not what
    the module says about itself."""
    twin = "bootstrap/tests/_oracle_trust.py"
    bed.write("bootstrap/tests/planted.py", f"VALUE = 1\n{hide}\n")
    bed.write(twin, bed.read(twin) + "\nimport importlib.util as _u, sys as _s\n"
              "_sp = _u.spec_from_file_location('planted', __file__.replace('_oracle_trust.py', 'planted.py'))\n"
              "_m = _u.module_from_spec(_sp)\n_s.modules['planted'] = _m\n_sp.loader.exec_module(_m)\n")
    bed.pin()
    refused(bed.run("status"), "the module planted loaded from")


def tree_with(bed, extra):
    """Commit HEAD's root tree plus *extra* raw entries, built with `--literally` so that git
    itself does not refuse the ones `repin` must.  Each entry is (mode, name, object id)."""
    rows = [r for r in bed.git("ls-tree", "-z", "HEAD", text=False).stdout.split(b"\0") if r]
    raw = b""
    for row in rows:
        meta, _, name = row.partition(b"\t")
        mode, _kind, oid = meta.split()
        raw += mode + b" " + name + b"\0" + bytes.fromhex(oid.decode())
    for mode, name, oid in extra:
        raw += mode.encode() + b" " + name.encode() + b"\0" + bytes.fromhex(oid)
    tree = bed.git("hash-object", "-t", "tree", "-w", "--literally", "--stdin", input=raw, text=False).stdout.decode().strip()
    commit = bed.git("commit-tree", tree, "-p", "HEAD", "-m", "raw tree").stdout.strip()
    bed.git("update-ref", "refs/heads/main", commit)


def blob_id(bed, data=b"x\n"):
    return bed.git("hash-object", "-w", "--stdin", input=data, text=False).stdout.decode().strip()


def subtree_id(bed, name, oid):
    raw = b"100644 " + name.encode() + b"\0" + bytes.fromhex(oid)
    return bed.git("hash-object", "-t", "tree", "-w", "--literally", "--stdin", input=raw, text=False).stdout.decode().strip()


@pytest.mark.parametrize("kind", ["a symlink", "a submodule"])
def test_a_tracked_symlink_or_submodule_refuses_before_import(bed, kind):
    ok(bed.run("status"))
    entry = ("120000", "link", blob_id(bed, b"/etc/passwd")) if kind == "a symlink" else \
        ("160000", "sub", bed.git("rev-parse", "HEAD").stdout.strip())
    tree_with(bed, [entry])
    refused(bed.run("status"), "symlink or submodule")


@pytest.mark.parametrize("name,shape", [("..", "an escaping path"), (".GIT", "a git folder name")])
def test_an_unusable_tracked_path_refuses_and_writes_nothing_outside_the_extraction(bed, name, shape):
    scratch = bed.root / "scratch"
    scratch.mkdir()
    bed.env["TMPDIR"] = str(scratch)
    ok(bed.run("status"))
    leaf = blob_id(bed)
    tree_with(bed, [("40000", "..", subtree_id(bed, "escape.txt", leaf))] if name == ".." else [("100644", name, leaf)])
    refused(bed.run("status"), "unusable path")
    assert not list(scratch.glob("escape.txt")), "a file was written outside the extraction folder"


def test_an_extracted_file_that_reads_back_differently_refuses(bed):
    """A disk that stores other bytes than it was given must stop the run before anything is compared."""
    code = """
import builtins
R.D = lambda value: value
class Liar:
    def __init__(self, fh): self.fh = fh
    def __enter__(self): return self
    def __exit__(self, *exc): self.fh.close()
    def write(self, data): return self.fh.write(data + b"!")
R.open = lambda path, mode: Liar(builtins.open(path, mode))
head = R.git_text(REPO, "rev-parse", "HEAD")
outcome(lambda: R.extract(REPO, head, TMP / "x"))
"""
    out = snippet(bed, code)[1]
    assert "RESULT: refused: " in out and "read back from disk differs" in out, out


def test_the_repin_process_runs_isolated(bed):
    scratch = bed.root / "scratch"
    scratch.mkdir()
    bed.env["TMPDIR"] = str(scratch)
    out = ok(bed.run("status"))
    line = re.search(r"^process\s+isolated=(\w+)\s+compiled files go to (\S+)$", out, re.M)
    assert line and line.group(1) == "True"
    prefix = Path(line.group(2))
    assert prefix.parent.resolve() == scratch.resolve() and prefix.name.startswith("repin-pyc-"), \
        "the bytecode folder is not a fresh one under the temporary folder"
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
    """A tripwire, not a proof: no environment variable steers a check.  The reads are
    the filter that strips the environment for git, the agent socket the key check
    must ask about, and the terminal type handed to the signer."""
    reads = [ln for ln in (REAL / "scripts/repin.py").read_text().splitlines() if "os.environ" in ln]
    names = [("GIT_" if "GIT_" in ln else "SSH_AUTH_SOCK" if "SSH_AUTH_SOCK" in ln else "TERM" if "TERM" in ln else ln)
             for ln in reads]
    assert names == ["GIT_", "SSH_AUTH_SOCK", "TERM"], reads


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


# --------------------------------------------------------------------------
# the AST transaction and the one write
# --------------------------------------------------------------------------

def run_pty(argv, answers=(), *, env, cwd, timeout=120):
    """Run *argv* on a pseudo-terminal that is also its controlling terminal.

    *answers* is a list of (prompt text, reply).  A reply is typed once the
    prompt is on screen; None sends end-of-input; a callable runs first (so a
    test can change the world while the question is open) and returns the reply.
    Returns (exit code, everything the child printed).
    """
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(cwd)
        os.execve(argv[0], argv, env)
    buf, pos, todo = bytearray(), 0, list(answers)
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not select.select([fd], [], [], 0.2)[0]:
            continue
        try:
            chunk = os.read(fd, 65536)
        except OSError:
            break
        if not chunk:
            break
        buf += chunk
        if todo and todo[0][0].encode() in bytes(buf[pos:]):
            _prompt, reply = todo.pop(0)
            pos = len(buf)
            reply = reply() if callable(reply) else reply
            os.write(fd, b"\x04" if reply is None else reply.encode() + b"\n")
    else:
        os.kill(pid, signal.SIGKILL)
    _pid, status = os.waitpid(pid, 0)
    return os.waitstatus_to_exitcode(status), buf.decode("utf-8", "replace").replace("\r\n", "\n")


def run_mixed(argv, *, tty_in, tty_out, env, cwd):
    """Run *argv* with each of stdin and stdout either a terminal or a pipe."""
    master, slave = pty.openpty()
    proc = subprocess.Popen(argv, cwd=cwd, env=env, stdin=slave if tty_in else subprocess.PIPE,
                            stdout=slave if tty_out else subprocess.PIPE, stderr=subprocess.STDOUT,
                            start_new_session=True)
    os.close(slave)
    if not tty_in:
        proc.stdin.close()
    sources = {master: "tty"} | ({proc.stdout.fileno(): "pipe"} if not tty_out else {})
    chunks = []
    while sources:
        for fd in select.select(list(sources), [], [], 5)[0]:
            try:
                part = os.read(fd, 65536)
            except OSError:
                part = b""
            if part:
                chunks.append(part)
            else:
                sources.pop(fd)
    proc.wait()
    os.close(master)
    return proc.returncode, b"".join(chunks).decode("utf-8", "replace")


def prelude(bed):
    return f"""
import importlib.util, json, os, sys, tempfile
from pathlib import Path
sys.pycache_prefix = tempfile.mkdtemp()
spec = importlib.util.spec_from_file_location("repin", {str(bed.repo / 'scripts/repin.py')!r})
R = importlib.util.module_from_spec(spec); sys.modules["repin"] = R; spec.loader.exec_module(R)
REPO, CDIR, TMP = Path({str(bed.repo)!r}), Path({str(bed.root / 'ceremony')!r}), Path(tempfile.mkdtemp())
CDIR.mkdir(exist_ok=True)
def outcome(fn):
    try:
        fn()
        print("RESULT: ok")
    except R.Refuse as exc:
        print("RESULT: refused:", exc)
def packaged():
    ctx = R.boot(REPO, TMP)
    return ctx, R.package(ctx, CDIR)
"""


def snippet(bed, code, answers=(), **kw):
    """Run *code* in a fresh isolated interpreter that has imported `repin` as R."""
    return run_pty([PY, "-I", "-c", prelude(bed) + code], answers, env=bed.env, cwd=bed.repo, **kw)


YES = [("type the word yes", "yes")]
APPLY = "ctx, raw = packaged()\noutcome(lambda: R.apply_pin(ctx, CDIR, raw))\n"


def owe_a_pin(bed, text="def f():\n    return 2\n"):
    bed.write(ENGINE, text)
    bed.commit("change f")


def reads(bed, rel=BASELINE) -> bytes:
    return (bed.repo / rel).read_bytes()


def test_the_apply_step_makes_no_commit_and_stops(bed):
    owe_a_pin(bed)
    head, before = bed.git("rev-parse", "HEAD").stdout.strip(), reads(bed)
    code, out = snippet(bed, APPLY, YES)
    assert "RESULT: ok" in out, out
    assert bed.git("rev-parse", "HEAD").stdout.strip() == head
    assert reads(bed) != before and f"git commit {BASELINE}" in out
    assert "Written, not committed" in out and "run ceremony again" in out
    assert bed.git("status", "--porcelain").stdout.split() == ["M", BASELINE]
    stop = json.loads(next((bed.root / "ceremony").glob("ast-pin-stop-*.json")).read_text())
    assert stop["head"] == head and list(stop["paths"]) == [BASELINE]
    assert stop["paths"][BASELINE] == bed.git("hash-object", "--no-filters", BASELINE).stdout.strip()


def test_every_key_the_write_changes_is_on_screen_before_the_question(bed):
    bed.write(ENGINE, "def f():\n    return 2\n\ndef g():\n    return 3\n")
    bed.commit("change f, add g")
    before = json.loads(reads(bed)), json.loads(reads(bed, KNOWN_NEW))
    code, out = snippet(bed, APPLY, YES)
    assert "RESULT: ok" in out, out
    after = json.loads(reads(bed)), json.loads(reads(bed, KNOWN_NEW))
    changed = [k for b, a in zip(before, after) for k in set(a) | set(b) if a.get(k) != b.get(k)]
    assert changed
    screen = out[:out.index("Write these files?")]
    assert [k for k in changed if k not in screen] == []
    # control: with one row dropped from the screen the same check reports it
    dropped = "\n".join(ln for ln in screen.splitlines() if changed[0] not in ln)
    assert [k for k in changed if k not in dropped] == [changed[0]]


@pytest.mark.parametrize("reply", ["Yes", "y", "", "yes please", None])
def test_only_the_exact_word_yes_writes(bed, reply):
    owe_a_pin(bed)
    before = reads(bed)
    code, out = snippet(bed, APPLY, [("type the word yes", reply)])
    assert "RESULT: refused: no `yes` was typed" in out, out
    assert reads(bed) == before


def test_a_pipe_on_stdin_or_stdout_refuses(bed):
    owe_a_pin(bed)
    body = prelude(bed) + "ctx = R.boot(REPO, TMP)\noutcome(lambda: R.check_preconditions(ctx))\n"
    for tty_in, tty_out, wanted in [(True, True, "RESULT: ok"), (False, True, "must both be a terminal"),
                                    (True, False, "must both be a terminal"), (False, False, "must both be a terminal")]:
        _code, out = run_mixed([PY, "-I", "-c", body], tty_in=tty_in, tty_out=tty_out, env=bed.env, cwd=bed.repo)
        assert wanted in out, (tty_in, tty_out, out)


PRECONDITION = "ctx = R.boot(REPO, TMP)\noutcome(lambda: R.check_preconditions(ctx))\n"


def precondition_outcome(bed):
    return snippet(bed, PRECONDITION)[1]


def test_a_detached_head_refuses(bed):
    assert "RESULT: ok" in precondition_outcome(bed)
    bed.git("checkout", "-q", "--detach")
    assert "HEAD is detached" in precondition_outcome(bed)


def test_a_dirty_tracked_file_refuses_before_any_write(bed):
    owe_a_pin(bed)
    before = reads(bed)
    assert "RESULT: ok" in snippet(bed, APPLY, YES)[1]
    bed.write(BASELINE, before.decode())
    bed.write("scripts/reanchor_ceremony.py", bed.read("scripts/reanchor_ceremony.py") + "\n# local edit\n")
    out = snippet(bed, APPLY, YES)[1]
    assert "tracked files differ from HEAD: scripts/reanchor_ceremony.py" in out
    assert reads(bed) == before


def test_a_staged_change_refuses(bed):
    bed.write("dev/plans/widget-plan.md", "# Plan\n\n**Status**: done\n")
    bed.git("add", "dev/plans/widget-plan.md")
    assert "staged changes" in precondition_outcome(bed)


@pytest.mark.parametrize("flag", ["--assume-unchanged", "--skip-worktree"])
def test_an_index_bit_that_hides_changes_refuses(bed, flag):
    assert "RESULT: ok" in precondition_outcome(bed)
    bed.git("update-index", flag, "dev/plans/widget-plan.md")
    bed.write("dev/plans/widget-plan.md", "# Plan\n\n**Status**: hidden edit\n")
    assert bed.git("status", "--porcelain").stdout == "", "the instrument is wrong: git status shows it"
    assert "an index bit hides changes" in precondition_outcome(bed)


def test_a_different_interpreter_minor_refuses(bed):
    manifest = json.loads(bed.read(MANIFEST))
    manifest["interpreter"]["version_info"] = [3, 99, 0]
    bed.write(MANIFEST, _dump(manifest))
    bed.commit("pin another minor")
    bed.git("update-ref", "refs/cairn/gate-anchor", "HEAD")
    assert "the anchor pins 3.99" in precondition_outcome(bed)


def test_head_moving_between_package_and_write_refuses(bed):
    owe_a_pin(bed)
    before = reads(bed)

    def move_head():
        bed.git("commit", "-q", "--allow-empty", "-m", "move head")
        return "yes"
    code, out = snippet(bed, APPLY, [("type the word yes", move_head)])
    assert "HEAD moved" in out and reads(bed) == before
    assert not list((bed.repo / "bootstrap/tests/fixtures").glob("*.tmp"))


def test_a_file_changed_while_the_question_was_open_refuses(bed):
    owe_a_pin(bed)

    def edit_the_target():
        bed.write(BASELINE, bed.read(BASELINE) + "\n")
        return "yes"
    code, out = snippet(bed, APPLY, [("type the word yes", edit_the_target)])
    assert "changed while you were reading" in out
    assert reads(bed) == (bed.read(BASELINE)).encode()
    assert not list((bed.repo / "bootstrap/tests/fixtures").glob("*.tmp")), "a temporary file was left"


def test_a_transaction_naming_the_gate_manifest_or_any_other_path_refuses(bed):
    owe_a_pin(bed)
    for victim in (MANIFEST, "scripts/repin.py", "../outside.json"):
        code = f"""
ctx, raw = packaged()
txn = json.loads(raw)
txn["outputs"][{victim!r}] = dict(txn["outputs"][{BASELINE!r}])
raw = R.encode_txn(txn)
R.store_txn(CDIR, raw)
outcome(lambda: R.apply_pin(ctx, CDIR, raw))
"""
        _c, out = snippet(bed, code, YES)
        assert "names paths outside" in out, (victim, out)
    assert json.loads(reads(bed, MANIFEST))["schema"].endswith("v2")
    assert bed.git("status", "--porcelain").stdout == ""
    assert "RESULT: ok" in snippet(bed, APPLY, YES)[1]       # control: the baseline alone passes


def test_an_edited_output_byte_refuses(bed):
    owe_a_pin(bed)
    code = """
ctx, raw = packaged()
txn = json.loads((CDIR / R.TXN_NAME).read_bytes())
txn["outputs"][%r]["new_text"] = txn["outputs"][%r]["new_text"] + " "
(CDIR / R.TXN_NAME).write_bytes(R.encode_txn(txn))
outcome(lambda: R.apply_pin(ctx, CDIR, raw))
""" % (BASELINE, BASELINE)
    before = reads(bed)
    assert "transaction file changed after it was packaged" in snippet(bed, code, YES)[1]
    assert reads(bed) == before


def test_summary_one_is_rendered_from_the_bytes_and_not_from_the_transactions_stored_text(bed):
    """`package` prints the same rows, so only a transaction whose stored summary lies, handed
    straight to the apply step, shows which text the apply step puts on screen."""
    owe_a_pin(bed)
    code = """
ctx = R.boot(REPO, TMP)
txn = R.build_transaction(ctx)
txn["summary"] = ["  LYING ROW"]
raw = R.encode_txn(txn); R.store_txn(CDIR, raw)
outcome(lambda: R.apply_pin(ctx, CDIR, raw))
"""
    out = snippet(bed, code, YES)[1]
    screen = out[:out.index("Write these files?")]
    assert "RESULT: ok" in out and "LYING ROW" not in screen and "FunctionDef:f" in screen, out


@pytest.mark.parametrize("field", ["new_sha256", "preimage_sha256"])
def test_a_transaction_whose_stored_hash_does_not_match_its_bytes_refuses(bed, field):
    owe_a_pin(bed)
    code = f"""
ctx = R.boot(REPO, TMP)
txn = R.build_transaction(ctx)
txn["outputs"][{BASELINE!r}][{field!r}] = "0" * 64
raw = R.encode_txn(txn); R.store_txn(CDIR, raw)
outcome(lambda: R.apply_pin(ctx, CDIR, raw))
"""
    before = reads(bed)
    assert "differ from the transaction" in snippet(bed, code, YES)[1]
    assert reads(bed) == before
    assert "RESULT: ok" in snippet(bed, APPLY, YES)[1]                  # control: the honest transaction applies


def test_an_output_path_that_is_not_tracked_at_head_refuses(bed):
    """The lockfile is an allowed output only when HEAD tracks it; here it exists on disk, untracked."""
    owe_a_pin(bed)
    bed.write("dev/.cairn/cairn-lock.yml", "x\n")
    code = f"""
ctx = R.boot(REPO, TMP)
txn = R.build_transaction(ctx)
txn["outputs"]["dev/.cairn/cairn-lock.yml"] = dict(txn["outputs"][{BASELINE!r}], new_text="y\\n",
    new_sha256=R.sha(b"y\\n"), preimage_sha256=R.sha(b"x\\n"))
raw = R.encode_txn(txn); R.store_txn(CDIR, raw)
outcome(lambda: R.apply_pin(ctx, CDIR, raw))
"""
    out = snippet(bed, code, YES)[1]
    assert "not a tracked regular file with no link in its path" in out, out
    assert bed.read("dev/.cairn/cairn-lock.yml") == "x\n" and reads(bed) == reads(bed)


def test_a_clean_filter_cannot_hide_an_edit_from_the_tree_check(bed):
    bed.write(".gitattributes", "dev/plans/widget-plan.md filter=hide\n")
    bed.git("config", "filter.hide.clean", "cat >/dev/null; printf 'same\\n'")
    bed.write("dev/plans/widget-plan.md", "same\n")
    bed.pin()
    assert "RESULT: ok" in precondition_outcome(bed)                      # control: clean tree passes
    bed.write("dev/plans/widget-plan.md", "diff\n")        # same size: git trusts the stat and the filter
    assert bed.git("status", "--porcelain").stdout == "", "the instrument is wrong: git status shows it"
    assert "tracked files differ from HEAD: dev/plans/widget-plan.md" in precondition_outcome(bed)


def test_bytes_that_change_while_the_files_are_replaced_are_caught_after_the_write(bed):
    owe_a_pin(bed)
    code = """
real = R.os.replace
def sneaky(src, dst):
    real(src, dst)
    if str(dst).endswith("scaffold_ast_baseline.json"):
        Path(dst).write_bytes(b"other bytes\\n")
R.os.replace = sneaky
""" + APPLY
    out = snippet(bed, code, YES)[1]
    assert "not exactly the ones named, or their bytes differ from those shown" in out, out


def test_a_second_file_that_changes_between_the_first_replace_and_its_own_refuses(bed):
    bed.write(ENGINE, "def f():\n    return 2\n\ndef g():\n    return 3\n")
    bed.commit("change f, add g")
    code = """
real, seen = R.os.replace, []
def sneaky(src, dst):
    real(src, dst)
    if not seen and str(dst).endswith("scaffold_ast_baseline.json"):
        seen.append(dst)
        later = REPO / "bootstrap/tests/fixtures/scaffold_ast_known_new.json"
        later.write_bytes(later.read_bytes() + b" ")
R.os.replace = sneaky
""" + APPLY
    out = snippet(bed, code, YES)[1]
    assert "changed while it was being replaced" in out and "Already replaced:" in out, out
    assert reads(bed, KNOWN_NEW).endswith(b" ") and b"FunctionDef:g" not in reads(bed, KNOWN_NEW)


@pytest.mark.parametrize("how,needle", [("a symlink", "without following a link"),
                                        ("owned by someone else", "only this user can write"),
                                        ("writable by others", "only this user can write")])
def test_an_unsafe_transaction_file_refuses(bed, how, needle):
    owe_a_pin(bed)
    unsafe = {"a symlink": "tx = CDIR / R.TXN_NAME\nreal = CDIR / 'real.json'\ntx.rename(real)\ntx.symlink_to(real)\n",
              "owned by someone else": "R.os.getuid = lambda: 0\n",
              "writable by others": "os.chmod(CDIR / R.TXN_NAME, 0o666)\n"}[how]
    code = "ctx, raw = packaged()\n" + unsafe + "outcome(lambda: R.apply_pin(ctx, CDIR, raw))\n"
    before = reads(bed)
    out = snippet(bed, code, YES)[1]
    assert f"RESULT: refused: " in out and needle in out, out
    assert reads(bed) == before
    # control: the same transaction file, left alone, applies
    assert "RESULT: ok" in snippet(bed, APPLY, YES)[1]


def test_a_symlinked_target_or_parent_is_not_followed(bed):
    owe_a_pin(bed)
    outside = bed.root / "outside.json"
    outside.write_text("untouched")
    fixtures = bed.repo / "bootstrap/tests/fixtures"
    skip_checks = "R.check_preconditions = lambda ctx: None\n"
    original = reads(bed)
    # target is a symlink
    (fixtures / "scaffold_ast_baseline.json").rename(bed.root / "kept.json")
    (fixtures / "scaffold_ast_baseline.json").symlink_to(outside)
    out = snippet(bed, skip_checks + "ctx = R.boot(REPO, TMP)\nraw = R.package(ctx, CDIR)\noutcome(lambda: R.apply_pin(ctx, CDIR, raw))\n", YES)[1]
    assert "no link in its path" in out and outside.read_text() == "untouched"
    # a parent folder is a symlink
    (fixtures / "scaffold_ast_baseline.json").unlink()
    (bed.root / "kept.json").rename(fixtures / "scaffold_ast_baseline.json")
    shutil.move(str(fixtures), str(bed.root / "moved_fixtures"))
    (bed.repo / "bootstrap/tests/fixtures").symlink_to(bed.root / "moved_fixtures")
    out = snippet(bed, skip_checks + "ctx = R.boot(REPO, TMP)\nraw = R.package(ctx, CDIR)\noutcome(lambda: R.apply_pin(ctx, CDIR, raw))\n", YES)[1]
    assert "no link in its path" in out
    assert (bed.root / "moved_fixtures/scaffold_ast_baseline.json").read_bytes() == original


def test_a_planted_temporary_name_link_is_not_followed(bed):
    owe_a_pin(bed)
    outside = bed.root / "outside.json"
    outside.write_text("untouched")
    (bed.repo / (BASELINE + ".tmp")).symlink_to(outside)
    code, out = snippet(bed, "R.check_preconditions = lambda ctx: None\n" + APPLY, YES)
    assert "RESULT: ok" in out and outside.read_text() == "untouched"


def test_a_failed_second_replace_names_what_was_replaced_and_restores_nothing(bed):
    bed.write(ENGINE, "def f():\n    return 2\n\ndef g():\n    return 3\n")
    bed.commit("change f, add g")
    head = bed.git("rev-parse", "HEAD").stdout.strip()
    before = {rel: reads(bed, rel) for rel in (BASELINE, KNOWN_NEW)}
    code = """
real, calls = R.os.replace, []
def flaky(src, dst):
    if str(dst).endswith(".json") and "fixtures" in str(dst):
        calls.append(dst)
        if len(calls) == 2:
            raise OSError("disk full")
    real(src, dst)
R.os.replace = flaky
""" + APPLY
    out = snippet(bed, code, YES)[1]
    assert "Already replaced:" in out and f"git restore --source={head} --" in out
    assert reads(bed, BASELINE) != before[BASELINE] and reads(bed, KNOWN_NEW) == before[KNOWN_NEW]
    assert not list((bed.repo / "bootstrap/tests/fixtures").glob("*.tmp"))


def test_an_extra_changed_path_after_the_write_refuses_and_prints_the_undo_line(bed):
    owe_a_pin(bed)
    head = bed.git("rev-parse", "HEAD").stdout.strip()
    code = """
real = R.os.replace
def sneaky(src, dst):
    real(src, dst)
    if "fixtures" in str(dst):
        Path(REPO / "dev/plans/widget-plan.md").write_text("changed behind the write")
R.os.replace = sneaky
""" + APPLY
    out = snippet(bed, code, YES)[1]
    assert "not exactly the ones named" in out and f"To undo: git restore --source={head}" in out
    assert "dev/plans/widget-plan.md" in bed.git("status", "--porcelain").stdout, "repin must not undo it"


def test_a_pin_that_adds_or_drops_a_baseline_key_refuses(bed):
    owe_a_pin(bed)
    code = """
ctx, raw = packaged()
txn = json.loads(raw)
out = txn["outputs"][%r]
new = json.loads(out["new_text"]); new["Assign:extra"] = {"digest": "0", "span": [1, 1], "type": "Assign"}
out["new_text"] = (json.dumps(new, indent=2, sort_keys=True) + "\\n")
out["new_sha256"] = R.sha(out["new_text"].encode())
raw = R.encode_txn(txn); R.store_txn(CDIR, raw)
outcome(lambda: R.apply_pin(ctx, CDIR, raw))
""" % BASELINE
    before = reads(bed)
    assert "add or drop a baseline key" in snippet(bed, code, YES)[1]
    assert reads(bed) == before


@pytest.mark.parametrize("break_it", ["missing", "duplicate"])
def test_a_missing_or_duplicated_symbol_is_a_review_item_never_a_pin(bed, break_it):
    if break_it == "missing":
        owe_a_pin(bed, "def renamed():\n    return 1\n")
    else:
        owe_a_pin(bed)
        bed.write("bootstrap/_scaffold/second.py", "def f():\n    return 1\n")
        bed.commit("define f twice")
    out = bed.run("package")
    assert out.returncode == 2 and "missing or defined twice" in out.stderr, out.stdout + out.stderr


def test_a_pin_owed_to_a_plain_change_packages(bed):
    out = ok(bed.run("package"))
    assert "No pin is owed" in out
    owe_a_pin(bed)
    assert re.search(r"transaction digest [0-9a-f]{64}", ok(bed.run("package")))


def test_a_closure_member_change_refuses_an_ast_pin(bed):
    for rel, text in [("bootstrap/REANCHOR_RUNBOOK.md", "# runbook\n"), ("bootstrap/reanchor.sh", "#!/bin/sh\n"),
                      ("dev/.cairn/allowed_signers", "x ssh-ed25519 AAAA\n")]:
        bed.write(rel, text)
    bed.pin("closure files appear")
    owe_a_pin(bed)
    assert "differ" not in ok(bed.run("package")).split("closure")[0]
    bed.write("bootstrap/REANCHOR_RUNBOOK.md", "# runbook, edited\n")
    bed.commit("edit the runbook")
    r = bed.run("package")
    assert r.returncode == 2 and "transition ceremony, not an AST pin" in r.stderr


def test_two_trees_that_differ_only_in_a_kept_record_give_different_digests(bed, tmp_path):
    bed.write(ENGINE, "def f():\n    return 1\n\ndef g():\n    return 1\n")
    bed.write(BASELINE, _dump(A.digest_module(bed.repo / ENGINE)))
    bed.pin("two symbols")
    twin_root = tmp_path / "twin"
    shutil.copytree(bed.root, twin_root, symlinks=True)
    twin = Bed(twin_root)
    owe_a_pin(bed, "def f():\n    return 2\n\ndef g():\n    return 1\n")
    owe_a_pin(twin, "def f():\n    return 2\n\ndef g():\n    return 1\n")
    kept = json.loads(twin.read(BASELINE))
    kept["FunctionDef:g"]["span"] = [9, 9]
    twin.write(BASELINE, _dump(kept))
    twin.commit("a kept record differs")
    digest = lambda b: re.search(r"transaction digest (\w{64})", ok(b.run("package"))).group(1)
    assert digest(bed) != digest(twin)
    assert digest(bed) == digest(bed)


def test_package_in_a_detached_checkout_gives_one_digest(bed, tmp_path):
    owe_a_pin(bed)
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", str(bed.repo), str(clone)], env=bed.env, check=True)
    for ref in ("refs/cairn/gate-anchor",):
        subprocess.run(["git", "-C", str(clone), "fetch", "-q", str(bed.repo), f"+{ref}:{ref}"], env=bed.env, check=True)
    subprocess.run(["git", "-C", str(clone), "checkout", "-q", "--detach"], env=bed.env, check=True)
    twin = Bed(tmp_path)
    twin.repo = clone
    digest = lambda b: re.search(r"transaction digest (\w{64})", ok(b.run("package"))).group(1)
    assert digest(twin) == digest(bed)


def test_the_known_new_file_is_named_as_a_frozen_gate_file_only_when_it_changes(bed):
    owe_a_pin(bed)
    assert "owes a re-anchor" not in ok(bed.run("package"))
    bed.write(ENGINE, bed.read(ENGINE) + "\ndef g():\n    return 3\n")
    bed.commit("add g")
    out = ok(bed.run("package"))
    assert "scaffold_ast_known_new.json  FunctionDef:g" in out and "owes a re-anchor" in out


def test_package_writes_only_into_the_ceremony_folder(bed):
    owe_a_pin(bed)
    before = bed.tree_hash()
    cdir = bed.root / "ceremony"
    cdir.mkdir()
    ok(bed.run("package"))
    assert bed.tree_hash() == before
    ok(bed.run("package", "--ceremony-dir", str(cdir)))
    assert bed.tree_hash() == before and (cdir / "ast-pin-transaction.json").is_file()


# --------------------------------------------------------------------------
# the lockfile as a third output
# --------------------------------------------------------------------------

LOCKFILE = "dev/.cairn/cairn-lock.yml"
CONFIG = "bootstrap/_scaffold/config.py"


def lock_bed(bed, *, marker=None, template_text="verbatim\n", installed_text="verbatim\n"):
    """A tree with a lockfile that has one stale record, a mapping with no record, and a config.py
    holding `_SKILLS_MAPPINGS` as a literal."""
    guard = f"open({str(marker)!r}, 'w').close()\n" if marker else ""
    bed.write(CONFIG, guard + "_SKILLS_MAPPINGS = ((\"skills/x.md\", \"tools/x.md\", True),)\n")
    bed.write("templates/skills/x.md", template_text)
    bed.write("tools/x.md", installed_text)
    body = {"cairn_version": "0", "files": [{"base_hash": "sha256:0", "dst": "gone/old.md", "hash": "sha256:0",
                                              "src": "old.md", "verbatim": True},
                                             {"base_hash": "sha256:1", "dst": "tools/kept.md", "hash": "sha256:1",
                                              "src": "kept.md", "verbatim": True}]}
    bed.write("tools/kept.md", "kept\n")
    bed.write(LOCKFILE, "# cairn-lock.yml -- header kept byte for byte\n# second line\n" + _dump(body))
    bed.write(BASELINE, _dump({**A.digest_module(bed.repo / ENGINE), **A.digest_module(bed.repo / CONFIG)}))
    bed.pin("lockfile bed")


def test_the_lockfile_adapter_does_not_import_candidate_code(bed):
    lock_bed(bed, marker=bed.marker())
    out = ok(bed.run("package"))
    assert not bed.marker().exists(), "config.py was executed"
    assert "cairn-lock.yml" in out                      # the correction was still computed
    subprocess.run([PY, str(bed.repo / CONFIG)], cwd=bed.repo, check=False)
    assert bed.marker().exists(), "the control is wrong: running config.py should write the marker"


def test_a_stale_record_is_dropped_and_a_missing_verbatim_record_added(bed):
    lock_bed(bed)
    out = ok(bed.run("package"))
    assert '"dst": "gone/old.md"' in out and "(absent)" in out              # the stale record leaves
    assert "tools/x.md" in out and '"verbatim": true' in out                # the mapping gains a record
    assert "tools/kept.md" not in out                                        # a record that holds stays


def test_a_verbatim_record_over_a_file_that_differs_from_its_template_refuses(bed):
    lock_bed(bed, installed_text="edited locally\n")
    r = bed.run("package")
    assert r.returncode == 2 and "not byte-identical to its template" in r.stderr


def test_the_lockfile_is_written_with_the_other_outputs_and_its_header_is_kept(bed):
    lock_bed(bed)
    owe_a_pin(bed, "def f():\n    return 3\n")
    before = reads(bed, LOCKFILE)
    code, out = snippet(bed, APPLY, YES)
    assert "RESULT: ok" in out, out
    after = reads(bed, LOCKFILE)
    assert after.startswith(before.split(b"{")[0]) and after != before
    doc = json.loads(after.decode().split("\n", 2)[2])
    assert [r["dst"] for r in doc["files"]] == ["tools/kept.md", "tools/x.md"]
    assert sorted(bed.git("status", "--porcelain").stdout.split()[1::2]) == sorted([BASELINE, LOCKFILE])


def test_a_failed_second_of_three_replaces_names_what_was_replaced(bed):
    lock_bed(bed)
    bed.write(ENGINE, "def f():\n    return 2\n\ndef g():\n    return 3\n")
    bed.commit("change f, add g")
    head = bed.git("rev-parse", "HEAD").stdout.strip()
    before = {rel: reads(bed, rel) for rel in (BASELINE, KNOWN_NEW, LOCKFILE)}
    code = """
real, calls = R.os.replace, []
def flaky(src, dst):
    if "fixtures" in str(dst) or str(dst).endswith("cairn-lock.yml"):
        calls.append(dst)
        if len(calls) == 2:
            raise OSError("disk full")
    real(src, dst)
R.os.replace = flaky
""" + APPLY
    out = snippet(bed, code, YES)[1]
    assert "Already replaced:" in out and f"git restore --source={head} --" in out
    changed = [rel for rel in before if reads(bed, rel) != before[rel]]
    assert len(changed) == 1
    assert not list(bed.repo.rglob("*.tmp"))
