"""Unit coverage for the ``verify_counts`` registry verifier (Arm 3 of the
numeric-claim-verification fold-up).

Loads the shipped ``scripts/verify_counts.py`` + ``scripts/measurements.py``
by file path (the house ``spec_from_file_location`` pattern) so the tests
exercise the real files, not a re-implementation.

Pins the proposal/plan provisions:

* same-line annotation window; registry-authoritative ``as_of``;
  a ``Snapshot`` is never re-measured.
* an absent ``Invariant`` root degrades to a *visible* skip (exit 3),
  never a silent pass or a hard failure.
* Refusal -- an unregistered verify key is refused (exit 1), no silent pass.
* (Security) the ``count_*`` functions cannot escape their code-given
  ``root`` via a symlink, and ``git_commits_in_range`` rejects an unsafe
  rev-range and runs git ``shell=False``.

Run from the cairn repo root::

    python -m pytest bootstrap/tests/test_verify_counts.py
"""
from __future__ import annotations

import importlib.util
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
VERIFY_COUNTS_SRC = CAIRN_ROOT / "scripts" / "verify_counts.py"
MEASUREMENTS_SRC = CAIRN_ROOT / "scripts" / "measurements.py"

pytestmark = pytest.mark.skipif(
    not (VERIFY_COUNTS_SRC.exists() and MEASUREMENTS_SRC.exists()),
    reason="verify_counts / measurements scripts not available",
)


_BINDING_MUTATIONS = (
    "missing", "tampered", "oversized", "leaf-link", "parent-link",
    "wrong-pin", "cached-module",
)


def _seed_binding_repo(root: Path) -> None:
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_")}
    env.update({
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Cairn binding test",
        "GIT_AUTHOR_EMAIL": "binding-test@example.invalid",
        "GIT_COMMITTER_NAME": "Cairn binding test",
        "GIT_COMMITTER_EMAIL": "binding-test@example.invalid",
    })
    subprocess.run(["git", "-C", str(root), "init", "-q"], env=env,
                   check=True, capture_output=True)
    sample = root / "binding-seed.txt"
    sample.write_text("first\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "binding-seed.txt"],
                   env=env, check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "first"],
                   env=env, check=True, capture_output=True)
    sample.write_text("second\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "binding-seed.txt"],
                   env=env, check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "second"],
                   env=env, check=True, capture_output=True)


def _bound_member_run(base: Path, rel: str, mutation: str | None = None):
    """Run one copied first-importer in its shipped layout and hostile CWD."""
    delivery = base / "delivery"
    caller = delivery / rel
    caller.parent.mkdir(parents=True)
    shutil.copyfile(CAIRN_ROOT / rel, caller)
    tools = delivery / "tools"
    tools.mkdir(exist_ok=True)
    helper = tools / "git_read.py"
    helper_bytes = (CAIRN_ROOT / "tools/git_read.py").read_bytes() + (
        b"\nimport os as _binding_os\n"
        b"from pathlib import Path as _binding_Path\n"
        b"with _binding_Path(_binding_os.environ['CAIRN_TEST_HELPER_MARKER'])"
        b".open('a', encoding='utf-8') as _binding_marker:\n"
        b"    _binding_marker.write('helper-ran\\n')\n"
    )
    helper.write_bytes(helper_bytes)
    pin = hashlib.sha256(helper_bytes).hexdigest()
    source = caller.read_text(encoding="utf-8")
    source, count = re.subn(
        r'(?m)^_GIT_READ_SHA256 = "[0-9a-f]{64}"$',
        f'_GIT_READ_SHA256 = "{pin}"', source, count=1,
    )
    assert count == 1, f"{rel} lacks one fixed helper pin"
    caller.write_text(source, encoding="utf-8")
    _seed_binding_repo(delivery)

    outside = base / "outside"
    outside.mkdir()
    helper_marker = base / "helper-marker"
    cwd_marker = base / "cwd-marker"
    cache_marker = base / "cache-marker"
    if mutation == "missing":
        helper.unlink()
    elif mutation == "tampered":
        helper.write_bytes(helper.read_bytes() + b"\n# substituted bytes\n")
    elif mutation == "oversized":
        helper.write_bytes(helper.read_bytes() + b"x" * (256 * 1024 + 1))
    elif mutation == "leaf-link":
        target = outside / "git_read.py"
        shutil.copyfile(helper, target)
        helper.unlink()
        try:
            helper.symlink_to(target)
        except (OSError, NotImplementedError):
            pytest.skip("symlinks unavailable")
    elif mutation == "parent-link":
        linked_tools = outside / "tools"
        linked_tools.mkdir()
        shutil.copyfile(helper, linked_tools / "git_read.py")
        if rel.startswith("tools/"):
            shutil.copyfile(caller, linked_tools / caller.name)
        shutil.rmtree(tools)
        try:
            tools.symlink_to(linked_tools, target_is_directory=True)
        except (OSError, NotImplementedError):
            pytest.skip("directory symlinks unavailable")
    elif mutation == "wrong-pin":
        source = caller.read_text(encoding="utf-8")
        source, count = re.subn(
            r'(?m)^_GIT_READ_SHA256 = "[0-9a-f]{64}"$',
            '_GIT_READ_SHA256 = "' + "0" * 64 + '"', source, count=1,
        )
        assert count == 1
        caller.write_text(source, encoding="utf-8")
    elif mutation not in (None, "cached-module", "parent-link-postcapture"):
        raise AssertionError(f"unknown binding mutation {mutation}")

    cwd = outside / "cwd"
    decoy_tools = cwd / "tools"
    decoy_tools.mkdir(parents=True)
    decoy = decoy_tools / "git_read.py"
    decoy.write_text(
        "from pathlib import Path\n"
        f"Path({str(cwd_marker)!r}).write_text('decoy')\n",
        encoding="utf-8",
    )
    (decoy_tools / "git_read.py.sha256").write_text(
        hashlib.sha256(decoy.read_bytes()).hexdigest() + "\n", encoding="ascii",
    )
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_") and key != "PYTHONPATH"}
    env.update({
        "CAIRN_TEST_HELPER_MARKER": str(helper_marker),
        "CAIRN_TEST_CACHE_MARKER": str(cache_marker),
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
    })
    if rel == "scripts/measurements.py":
        action = (
            "import sys,importlib.util; from pathlib import Path; "
            f"spec=importlib.util.spec_from_file_location('binding_measurements',{str(caller)!r}); "
            "module=importlib.util.module_from_spec(spec); "
            "sys.modules[spec.name]=module; spec.loader.exec_module(module); "
            f"print(module.git_commits_in_range(Path({str(delivery)!r}), 'HEAD~1..HEAD'))"
        )
    else:
        action = (
            f"import runpy,sys; sys.argv=[{str(caller)!r},'--help']; "
            f"runpy.run_path({str(caller)!r},run_name='__main__')"
        )
    if mutation == "parent-link-postcapture":
        # Patch only the test driver: root resolution completes before this leaf.
        expected_leaf = str(helper.resolve())
        mutation_marker = base / "parent-mutation-ran"
        driver = f"""
import os, runpy, sys
_real_lstat = os.lstat
_triggered = False
def _mutating_lstat(path, *args, **kwargs):
    global _triggered
    if not _triggered and os.fspath(path) == {expected_leaf!r}:
        _triggered = True
        os.rename({str(tools)!r}, {str(outside / 'tools')!r})
        os.symlink({str(outside / 'tools')!r}, {str(tools)!r}, target_is_directory=True)
        with open({str(mutation_marker)!r}, 'w', encoding='utf-8') as marker:
            marker.write('mutation-ran')
    return _real_lstat(path, *args, **kwargs)
os.lstat = _mutating_lstat
try:
    sys.argv = [{str(caller)!r}, '--help']
    runpy.run_path({str(caller)!r}, run_name='__main__')
finally:
    os.lstat = _real_lstat
"""
        action = driver
    if mutation == "cached-module":
        action = (
            "import sys,types; poisoned=types.ModuleType('_cairn_verified_git_read'); "
            "exec(\"def __getattr__(name):\\n"
            f" from pathlib import Path; Path({str(cache_marker)!r}).write_text('cache')\\n"
            " raise AssertionError('cached helper used')\", poisoned.__dict__); "
            "sys.modules['_cairn_verified_git_read']=poisoned; " + action
        )
    result = subprocess.run(
        [sys.executable, "-c", action], cwd=cwd, env=env,
        text=True, capture_output=True, timeout=30,
    )
    return result, helper_marker, cwd_marker, cache_marker


def _assert_bound_member_positive(base: Path, rel: str) -> None:
    result, helper_marker, cwd_marker, cache_marker = _bound_member_run(base, rel)
    assert result.returncode == 0, result.stderr
    if rel == "scripts/measurements.py":
        assert result.stdout.strip() == "1", result.stdout
    assert helper_marker.read_text(encoding="utf-8").splitlines() == [
        "helper-ran",
    ]
    assert not cwd_marker.exists()
    assert not cache_marker.exists()


def _assert_linked_caller_parent_positive(base: Path, rel: str) -> None:
    result, helper_marker, cwd_marker, cache_marker = _bound_member_run(
        base, rel, "parent-link",
    )
    assert result.returncode == 0, result.stderr
    assert helper_marker.read_text(encoding="utf-8").splitlines() == [
        "helper-ran",
    ]
    assert not cwd_marker.exists()
    assert not cache_marker.exists()


def _assert_bound_member_mutation(base: Path, rel: str, mutation: str) -> None:
    selected = ("parent-link-postcapture"
                if mutation == "parent-link" and rel.startswith("tools/")
                else mutation)
    result, helper_marker, cwd_marker, cache_marker = _bound_member_run(
        base, rel, selected,
    )
    if selected == "parent-link-postcapture":
        assert (base / "parent-mutation-ran").read_text(encoding="utf-8") == "mutation-ran"
    if mutation == "cached-module":
        assert result.returncode == 0, result.stderr
        if rel == "scripts/measurements.py":
            assert result.stdout.strip() == "1", result.stdout
        assert helper_marker.read_text(encoding="utf-8").splitlines() == [
            "helper-ran",
        ]
        assert not cache_marker.exists()
    else:
        assert result.returncode != 0, result.stdout
        assert "git-read-binding-failed" in result.stderr, result.stderr
        assert not helper_marker.exists(), "refused binding executed helper bytes"
    assert not cwd_marker.exists(), "external CWD helper became authoritative"
    assert not cache_marker.exists(), "cached helper became authoritative"


def _load(name: str, src: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, src)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def m() -> ModuleType:
    return _load("_cairn_measurements_under_test", MEASUREMENTS_SRC)


@pytest.fixture(scope="module")
def vc() -> ModuleType:
    return _load("_cairn_verify_counts_under_test", VERIFY_COUNTS_SRC)


def _file_of_n_lines(root: Path, name: str, n: int) -> Path:
    path = root / name
    path.write_text("\n".join(f"line {i}" for i in range(n)) + "\n")
    return path


# ---------------------------------------------------------------------------
# Annotation parsing (the same-line, immediately-preceding window).
# ---------------------------------------------------------------------------


class TestAnnotationParsing:
    def test_immediately_preceding_number_is_the_one(self, vc):
        out = vc.parse_annotations(
            "the file is 786 lines `<!-- verify: k -->`."
        )
        assert out == [(1, 786, "k")]

    def test_thousands_grouped_number(self, vc):
        out = vc.parse_annotations("size 1,294 `<!-- verify: k -->`")
        assert out == [(1, 1294, "k")]

    def test_last_number_before_annotation_wins(self, vc):
        # Two numbers on the line: the one immediately preceding the
        # annotation (10) is verified, not an earlier one (3).
        out = vc.parse_annotations(
            "3 modules, 10 files `<!-- verify: k -->`"
        )
        assert out == [(1, 10, "k")]

    def test_number_on_a_different_line_is_not_picked_up(self, vc):
        out = vc.parse_annotations("786\nplain `<!-- verify: k -->`")
        assert out == [(2, None, "k")]

    def test_no_preceding_number_yields_none(self, vc):
        out = vc.parse_annotations("plain prose `<!-- verify: k -->`")
        assert out == [(1, None, "k")]


# ---------------------------------------------------------------------------
# Invariant -- re-measure + drift.
# ---------------------------------------------------------------------------


class TestInvariant:
    def test_current_value_passes(self, vc, m, tmp_path):
        _file_of_n_lines(tmp_path, "watch.py", 42)
        registry = {"k": m.Invariant(tmp_path, "count_lines", "watch.py")}
        results = vc.verify_text(
            "the file is 42 lines `<!-- verify: k -->`",
            tmp_path / "doc.md", registry, m,
        )
        assert [r.status for r in results] == ["pass"]
        assert vc._exit_code(results) == 0

    def test_stale_value_drifts(self, vc, m, tmp_path):
        _file_of_n_lines(tmp_path, "watch.py", 42)
        registry = {"k": m.Invariant(tmp_path, "count_lines", "watch.py")}
        results = vc.verify_text(
            "the file is 99 lines `<!-- verify: k -->`",
            tmp_path / "doc.md", registry, m,
        )
        assert [r.status for r in results] == ["drift"]
        assert vc._exit_code(results) == 1

    def test_missing_target_is_error_not_skip(self, vc, m, tmp_path):
        # root present but target absent -> a measurement error (the
        # registry is wrong), exit 1 -- distinct from the absent-root skip.
        registry = {"k": m.Invariant(tmp_path, "count_lines", "gone.py")}
        results = vc.verify_text(
            "42 `<!-- verify: k -->`", tmp_path / "doc.md", registry, m,
        )
        assert [r.status for r in results] == ["error"]
        assert vc._exit_code(results) == 1


# ---------------------------------------------------------------------------
# An absent root skips visibly.
# ---------------------------------------------------------------------------


class TestAbsentRootSkip:
    def test_absent_root_is_visible_skip_exit_3(self, vc, m, tmp_path):
        missing = tmp_path / "no-such-sibling"
        registry = {"k": m.Invariant(missing, "count_lines", "x.py")}
        results = vc.verify_text(
            "42 `<!-- verify: k -->`", tmp_path / "doc.md", registry, m,
        )
        assert [r.status for r in results] == ["skipped"]
        assert "root absent" in results[0].message
        assert vc._exit_code(results) == 3  # non-clean, non-error

    def test_drift_dominates_skip_in_exit_code(self, vc, m, tmp_path):
        _file_of_n_lines(tmp_path, "watch.py", 42)
        missing = tmp_path / "no-such-sibling"
        registry = {
            "ok": m.Invariant(tmp_path, "count_lines", "watch.py"),
            "gone": m.Invariant(missing, "count_lines", "x.py"),
        }
        text = (
            "99 `<!-- verify: ok -->`\n"      # drift
            "42 `<!-- verify: gone -->`"      # skip
        )
        results = vc.verify_text(text, tmp_path / "doc.md", registry, m)
        assert vc._exit_code(results) == 1  # failure dominates


# ---------------------------------------------------------------------------
# Refusal -- unregistered key, no silent pass.
# ---------------------------------------------------------------------------


class TestRefusal:
    def test_unregistered_key_refused(self, vc, m, tmp_path):
        results = vc.verify_text(
            "5 `<!-- verify: nope -->`", tmp_path / "doc.md", {}, m,
        )
        assert [r.status for r in results] == ["refused"]
        assert vc._exit_code(results) == 1

    def test_annotation_without_number_is_error(self, vc, m, tmp_path):
        registry = {"k": m.Snapshot(5, "2026-01-01")}
        results = vc.verify_text(
            "prose only `<!-- verify: k -->`", tmp_path / "doc.md",
            registry, m,
        )
        assert [r.status for r in results] == ["error"]


# ---------------------------------------------------------------------------
# A Snapshot is never re-measured.
# ---------------------------------------------------------------------------


class TestSnapshot:
    def test_snapshot_passes_on_value_and_iso_date(self, vc, m, tmp_path):
        # The annotation sits immediately after the number; the ISO
        # as_of date appears elsewhere on the line (here, after it).
        registry = {"k": m.Snapshot(728, "2026-05-11")}
        results = vc.verify_text(
            "the suite had 728 tests `<!-- verify: k -->` (as_of 2026-05-11)",
            tmp_path / "doc.md", registry, m,
        )
        assert [r.status for r in results] == ["pass"]

    def test_snapshot_missing_iso_date_drifts(self, vc, m, tmp_path):
        registry = {"k": m.Snapshot(728, "2026-05-11")}
        results = vc.verify_text(
            "the suite had 728 tests `<!-- verify: k -->`",
            tmp_path / "doc.md", registry, m,
        )
        assert [r.status for r in results] == ["drift"]
        assert "as_of" in results[0].message

    def test_snapshot_wrong_value_drifts(self, vc, m, tmp_path):
        registry = {"k": m.Snapshot(728, "2026-05-11")}
        results = vc.verify_text(
            "the count was 999 `<!-- verify: k -->` (as_of 2026-05-11)",
            tmp_path / "doc.md", registry, m,
        )
        assert [r.status for r in results] == ["drift"]

    def test_snapshot_is_not_remeasured(self, vc, m, tmp_path, monkeypatch):
        # A Snapshot must never call measure() -- re-running erases the
        # evidence the snapshot is.
        called = []
        monkeypatch.setattr(m, "measure", lambda inv: called.append(inv))
        registry = {"k": m.Snapshot(728, "2026-05-11")}
        vc.verify_text(
            "728 tests `<!-- verify: k -->` as_of 2026-05-11",
            tmp_path / "doc.md", registry, m,
        )
        assert called == []


# ---------------------------------------------------------------------------
# Security: root containment + no shell.
# ---------------------------------------------------------------------------


class TestContainment:
    def test_count_lines_refuses_symlink_escaping_root(self, m, tmp_path):
        root = tmp_path / "root"
        root.mkdir()
        outside = tmp_path / "outside.txt"
        outside.write_text("secret\n")
        link = root / "escape.txt"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            pytest.skip("symlinks unsupported on this platform")
        with pytest.raises(ValueError, match="escapes its root"):
            m.count_lines(root, "escape.txt")

    def test_count_files_refuses_symlinked_dir_escaping_root(
        self, m, tmp_path
    ):
        root = tmp_path / "root"
        root.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        (outside / "f.txt").write_text("x\n")
        link = root / "escape"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            pytest.skip("symlinks unsupported on this platform")
        with pytest.raises(ValueError, match="escapes its root"):
            m.count_files(root, "escape")

    def test_dotdot_target_refused(self, m, tmp_path):
        root = tmp_path / "root"
        root.mkdir()
        (tmp_path / "secret.txt").write_text("x\n")
        with pytest.raises(ValueError, match="escapes its root"):
            m.count_lines(root, "../secret.txt")

    def test_git_range_rejects_unsafe_chars(self, m, tmp_path):
        # A rev-range carrying anything outside ref chars + `..` is refused
        # before git ever runs (defence in depth; git is shell=False anyway).
        with pytest.raises(ValueError, match="unsafe rev-range"):
            m.git_commits_in_range(tmp_path, "HEAD; rm -rf /")
        with pytest.raises(ValueError, match="unsafe rev-range"):
            m.git_commits_in_range(tmp_path, "$(touch pwned)..HEAD")


# ---------------------------------------------------------------------------
# The measurement primitives (the four allowlisted fns).
# ---------------------------------------------------------------------------


class TestMeasurePrimitives:
    def test_count_lines(self, m, tmp_path):
        _file_of_n_lines(tmp_path, "f.txt", 7)
        assert m.count_lines(tmp_path, "f.txt") == 7

    def test_count_files_excludes_dot_entries(self, m, tmp_path):
        target = tmp_path / "pkg"
        (target / "sub").mkdir(parents=True)
        (target / "a.py").write_text("x\n")
        (target / "sub" / "b.py").write_text("y\n")
        (target / ".hidden").mkdir()
        (target / ".hidden" / "c.py").write_text("z\n")
        assert m.count_files(tmp_path, "pkg") == 2  # .hidden/c.py excluded

    def test_count_defs(self, m, tmp_path):
        (tmp_path / "mod.py").write_text(
            "def a():\n    pass\n"
            "async def b():\n    pass\n"
            "class C:\n    def d(self):\n        pass\n"
        )
        # a, b, C, d = 4
        assert m.count_defs(tmp_path, "mod.py") == 4

    def test_count_defs_via_measure_allowlist(self, m, tmp_path):
        (tmp_path / "mod.py").write_text("def a():\n    pass\n")
        inv = m.Invariant(tmp_path, "count_defs", "mod.py")
        assert m.measure(inv) == 1

    def test_measure_refuses_fn_not_in_allowlist(self, m, tmp_path):
        inv = m.Invariant(tmp_path, "count_everything", "x")
        with pytest.raises(KeyError, match="allowlist"):
            m.measure(inv)

    def test_git_commits_in_range_counts(self, m, tmp_path, monkeypatch):
        env_repo = tmp_path / "repo"
        env_repo.mkdir()

        def _git(*args):
            subprocess.run(
                ["git", "-C", str(env_repo), *args],
                check=True, capture_output=True, text=True,
            )

        _git("init", "-q")
        _git("config", "user.email", "t@example.com")
        _git("config", "user.name", "t")
        (env_repo / "a").write_text("1\n")
        _git("add", "a")
        _git("commit", "-q", "-m", "c1")
        (env_repo / "a").write_text("2\n")
        _git("commit", "-q", "-am", "c2")
        calls = []
        reader = m._GIT_READ
        original = reader.run_git

        def observed(target, args, **kwargs):
            calls.append((target, args))
            return original(target, args, **kwargs)

        monkeypatch.setattr(reader, "run_git", observed)
        assert m.git_commits_in_range(env_repo, "HEAD~1..HEAD") == 1
        assert calls == [(str(env_repo.resolve()),
                          ("log", "--oneline", "HEAD~1..HEAD"))]

    def test_git_commits_in_range_failure_is_not_measured_zero(
            self, m, tmp_path, monkeypatch):
        class Failed:
            state = "failed"
            returncode = None
            stdout = b""

        monkeypatch.setattr(m._GIT_READ, "run_git", lambda *_a, **_k: Failed())
        with pytest.raises(RuntimeError, match="Git history unavailable"):
            m.git_commits_in_range(tmp_path, "HEAD~1..HEAD")


# ---------------------------------------------------------------------------
# The seed registry + end-to-end main() over a real annotation.
# ---------------------------------------------------------------------------


class TestSeedRegistryAndMain:
    def test_seed_registry_keys_are_small_and_valid(self, m):
        # Soft cap; every entry is an Invariant or Snapshot with an
        # allowlisted fn.
        assert len(m.REGISTRY) <= 10
        for entry in m.REGISTRY.values():
            if isinstance(entry, m.Invariant):
                assert entry.fn in m.MEASURE_FNS

    def test_main_passes_on_a_correct_annotation(
        self, vc, m, tmp_path, capsys
    ):
        # Use the live seed invariant against its real current measurement.
        key = "claim_check_watch_file_lines"
        if key not in m.REGISTRY or not isinstance(
            m.REGISTRY[key], m.Invariant
        ):
            pytest.skip("seed invariant not present")
        measured = m.measure(m.REGISTRY[key])
        doc = tmp_path / "doc.md"
        doc.write_text(f"the watch file is {measured} `<!-- verify: {key} -->`")
        rc = vc.main([str(doc)])
        assert rc == 0
        assert "matches" in capsys.readouterr().out

    def test_main_usage_error_on_missing_file(self, vc, tmp_path):
        assert vc.main([str(tmp_path / "nope.md")]) == 2


class TestMeasurementsPhysicalBinding:
    def test_public_api_executes_its_pinned_helper(self, tmp_path: Path) -> None:
        _assert_bound_member_positive(tmp_path, "scripts/measurements.py")

    @pytest.mark.parametrize("mutation", _BINDING_MUTATIONS)
    def test_public_api_refuses_each_binding_mutation(
            self, mutation: str, tmp_path: Path) -> None:
        _assert_bound_member_mutation(
            tmp_path, "scripts/measurements.py", mutation,
        )
