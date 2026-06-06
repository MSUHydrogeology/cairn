"""Unit coverage for the ``verify_counts`` registry verifier (Arm 3 of the
numeric-claim-verification fold-up).

Loads the shipped ``scripts/verify_counts.py`` + ``scripts/measurements.py``
by file path (the house ``spec_from_file_location`` pattern) so the tests
exercise the real files, not a re-implementation.

Pins the proposal/plan provisions:

* RR1 -- same-line annotation window; registry-authoritative ``as_of``;
  a ``Snapshot`` is never re-measured.
* RR2 -- an absent ``Invariant`` root degrades to a *visible* skip (exit 3),
  never a silent pass or a hard failure.
* Refusal -- an unregistered verify key is refused (exit 1), no silent pass.
* IR3 (Security) -- the ``count_*`` functions cannot escape their code-given
  ``root`` via a symlink, and ``git_commits_in_range`` rejects an unsafe
  rev-range and runs git ``shell=False``.

Run from the cairn repo root::

    python -m pytest bootstrap/tests/test_verify_counts.py
"""
from __future__ import annotations

import importlib.util
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
# RR1 -- annotation parsing (the same-line, immediately-preceding window).
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
        # registry is wrong), exit 1 -- distinct from RR2's absent-root skip.
        registry = {"k": m.Invariant(tmp_path, "count_lines", "gone.py")}
        results = vc.verify_text(
            "42 `<!-- verify: k -->`", tmp_path / "doc.md", registry, m,
        )
        assert [r.status for r in results] == ["error"]
        assert vc._exit_code(results) == 1


# ---------------------------------------------------------------------------
# RR2 -- absent root skips visibly.
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
# RR1 -- Snapshot is never re-measured.
# ---------------------------------------------------------------------------


class TestSnapshot:
    def test_snapshot_passes_on_value_and_iso_date(self, vc, m, tmp_path):
        # RR1: the annotation sits immediately after the number; the ISO
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
# IR3 (Security) -- root containment + no shell.
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

    def test_git_commits_in_range_counts(self, m, tmp_path):
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
        assert m.git_commits_in_range(env_repo, "HEAD~1..HEAD") == 1


# ---------------------------------------------------------------------------
# The seed registry + end-to-end main() over a real annotation.
# ---------------------------------------------------------------------------


class TestSeedRegistryAndMain:
    def test_seed_registry_keys_are_small_and_valid(self, m):
        # RR3 soft cap; every entry is an Invariant or Snapshot with an
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
