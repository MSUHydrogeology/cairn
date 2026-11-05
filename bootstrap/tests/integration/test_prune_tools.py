"""Tests for ``prune_reflections.py`` and ``prune_intents.py`` (Fold 2).

These two goodnight compaction tools are shipped with the ``reflections``
and ``coordination-tiers`` modules respectively.  This module covers:

* Install-path: each script lands verbatim under its module.
* ``prune_reflections`` dry-run smoke: no files deleted, correct report.
* ``prune_intents`` dry-run smoke: no file mutations, correct report.
* Deduplication check: the prune_reflections tool here is NOT a duplicate
  of the ``session.py`` session-end ``_prune_reflections`` -- it is a
  complementary standalone tool (keep-by-distinct-date vs. wall-clock cutoff).

Run from the cairn repo root::

    python -m pytest bootstrap/tests/integration/test_prune_tools.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
_DEFAULT_ON = TEMPLATES_ROOT / "modules" / "default-on"
_TEAM_GATED = TEMPLATES_ROOT / "modules" / "team-gated"

sys.path.insert(0, str(CAIRN_ROOT))
from bootstrap.scaffold import _MODULE_MAPPINGS, main as scaffold_main  # noqa: E402

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _scaffold(target: Path, modules: list[str]) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: PruneTest\ntest_command: pytest\nmodules:\n"
        + "".join(f"  - {m}\n" for m in modules)
    )
    return scaffold_main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
    )


# ---------------------------------------------------------------------------
# Install paths
# ---------------------------------------------------------------------------

class TestInstallPaths:
    """Both prune tools land verbatim under their respective modules."""

    def test_prune_reflections_in_reflections_module(self) -> None:
        specs = _MODULE_MAPPINGS["reflections"]
        dsts = {s.dst: s for s in specs}
        assert "tools/prune_reflections.py" in dsts, (
            "prune_reflections.py not registered under 'reflections' module"
        )
        assert dsts["tools/prune_reflections.py"].verbatim is True

    def test_prune_intents_in_coordination_tiers_module(self) -> None:
        specs = _MODULE_MAPPINGS["coordination-tiers"]
        dsts = {s.dst: s for s in specs}
        assert "tools/prune_intents.py" in dsts, (
            "prune_intents.py not registered under 'coordination-tiers' module"
        )
        assert dsts["tools/prune_intents.py"].verbatim is True

    def test_prune_reflections_installed_verbatim(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path, ["reflections"]) == 0
        installed = tmp_path / "tools" / "prune_reflections.py"
        assert installed.is_file(), "tools/prune_reflections.py not installed"
        src = _DEFAULT_ON / "prune_reflections.py"
        assert installed.read_bytes() == src.read_bytes(), (
            "Installed prune_reflections.py differs from template"
        )

    def test_prune_intents_installed_verbatim(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path, ["coordination-tiers"]) == 0
        installed = tmp_path / "tools" / "prune_intents.py"
        assert installed.is_file(), "tools/prune_intents.py not installed"
        src = _TEAM_GATED / "prune_intents.py"
        assert installed.read_bytes() == src.read_bytes(), (
            "Installed prune_intents.py differs from template"
        )


# ---------------------------------------------------------------------------
# prune_reflections -- dry-run smoke
# ---------------------------------------------------------------------------

class TestPruneReflectionsDryRun:
    """Dry-run: nothing is deleted; report is correct."""

    PRUNE_REFL_SRC = _DEFAULT_ON / "prune_reflections.py"

    @pytest.fixture(scope="class")
    def pr(self) -> ModuleType:
        if not self.PRUNE_REFL_SRC.exists():
            pytest.skip("prune_reflections.py template not available")
        return _load("_cairn_prune_refl_under_test", self.PRUNE_REFL_SRC)

    def _make_refl_dir(self, root: Path) -> Path:
        refl = root / "dev" / "reflections"
        refl.mkdir(parents=True)
        (refl / "README.md").write_text("# Reflections\n")
        # Two old dates + one current date.
        for date, time, agent_role in [
            ("2020-01-01", "120000", "claude-implementer"),
            ("2020-01-02", "130000", "codex-reviewer"),
            ("2026-06-06", "150000", "claude-strategy"),
        ]:
            (refl / f"{date}-{time}-{agent_role}.md").write_text(
                f"# Reflection {date}\n"
            )
        return refl

    def test_dry_run_deletes_nothing(self, tmp_path: Path, pr) -> None:
        refl = self._make_refl_dir(tmp_path)
        before = sorted(p.name for p in refl.iterdir())
        deleted = pr.prune_reflections(refl, keep=1, dry_run=True)
        after = sorted(p.name for p in refl.iterdir())
        assert before == after, "dry-run must not delete any files"
        # Two old dates should be in the 'would prune' list.
        assert len(deleted) == 2, (
            f"dry-run should report 2 files to prune (2 old dates); got {len(deleted)}"
        )

    def test_dry_run_never_touches_readme(self, tmp_path: Path, pr) -> None:
        refl = self._make_refl_dir(tmp_path)
        pr.prune_reflections(refl, keep=1, dry_run=True)
        assert (refl / "README.md").is_file(), "README.md must survive dry-run"

    def test_keep_positive_required(self, tmp_path: Path, pr) -> None:
        refl = self._make_refl_dir(tmp_path)
        with pytest.raises(ValueError, match="keep must be >= 1"):
            pr.prune_reflections(refl, keep=0, dry_run=True)

    def test_main_dry_run_exits_zero(self, tmp_path: Path, pr, capsys) -> None:
        refl = self._make_refl_dir(tmp_path)
        rc = pr.main(["--dir", str(refl), "--keep", "1", "--dry-run"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "would prune" in out

    def test_real_prune_deletes_old_dates(self, tmp_path: Path, pr) -> None:
        refl = self._make_refl_dir(tmp_path)
        deleted = pr.prune_reflections(refl, keep=1, dry_run=False)
        assert len(deleted) == 2, (
            f"expected 2 files deleted (2 old dates), got {len(deleted)}"
        )
        # The current date's reflection must still exist.
        assert (refl / "2026-06-06-150000-claude-strategy.md").is_file()
        # Old ones gone.
        assert not (refl / "2020-01-01-120000-claude-implementer.md").exists()
        assert not (refl / "2020-01-02-130000-codex-reviewer.md").exists()
        # README untouched.
        assert (refl / "README.md").is_file()


# ---------------------------------------------------------------------------
# prune_intents -- dry-run smoke
# ---------------------------------------------------------------------------

class TestPruneIntentsDryRun:
    """Dry-run: no file mutation; report is correct."""

    PRUNE_INTENTS_SRC = _TEAM_GATED / "prune_intents.py"

    @pytest.fixture(scope="class")
    def pi(self) -> ModuleType:
        if not self.PRUNE_INTENTS_SRC.exists():
            pytest.skip("prune_intents.py template not available")
        return _load("_cairn_prune_intents_under_test", self.PRUNE_INTENTS_SRC)

    def _write_log(self, path: Path, records: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\n".join(json.dumps(r, separators=(',', ':')) for r in records) + "\n"
        )

    def test_dry_run_does_not_mutate_log(self, tmp_path: Path, pi) -> None:
        log = tmp_path / "dev" / "intents.jsonl"
        now = __import__('datetime').datetime(2026, 6, 6, 12, 0, 0)
        old_ts = "2026-06-05T08:00:00"  # > 24h before now
        records = [
            {"event": "claim", "id": "abc", "ts": old_ts, "agent": "claude", "action": "edit x"},
            {"event": "release", "id": "abc", "ts": old_ts, "agent": "claude"},
        ]
        self._write_log(log, records)
        before = log.read_bytes()

        result = pi.compact(log_path=log, grace_hours=24, dry_run=True, now=now)
        assert log.read_bytes() == before, "dry-run must not modify the log"
        assert result["dry_run"] is True
        # Old released pair should be in the prune count.
        assert result["pruned_count"] > 0, (
            f"dry-run should report released pairs past grace as would-prune; "
            f"got pruned_count={result['pruned_count']}"
        )

    def test_dry_run_reports_stale_active(self, tmp_path: Path, pi) -> None:
        log = tmp_path / "dev" / "intents.jsonl"
        now = __import__('datetime').datetime(2026, 6, 6, 12, 0, 0)
        old_ts = "2026-06-05T08:00:00"  # > 24h before now -- never released
        records = [
            {"event": "claim", "id": "stale-1", "ts": old_ts,
             "agent": "codex", "action": "working on y"},
        ]
        self._write_log(log, records)
        result = pi.compact(log_path=log, grace_hours=24, dry_run=True, now=now)
        assert result["stale_active"], (
            "An unreleased claim older than the grace window must appear in stale_active"
        )
        assert result["stale_active"][0].get("id") == "stale-1"

    def test_main_dry_run_exits_zero(self, tmp_path: Path, pi) -> None:
        log = tmp_path / "dev" / "intents.jsonl"
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text("")  # empty log
        rc = pi.main(["--log-path", str(log), "--dry-run"])
        assert rc == 0

    def test_missing_log_returns_zero_counts(self, tmp_path: Path, pi) -> None:
        log = tmp_path / "dev" / "no-such.jsonl"
        result = pi.compact(log_path=log, dry_run=True)
        assert result["kept_active_count"] == 0
        assert result["pruned_count"] == 0

    def test_partition_pair_tolerance(self, tmp_path: Path, pi) -> None:
        """A released pair within the grace window is kept, not pruned."""
        import datetime
        now = datetime.datetime(2026, 6, 6, 12, 0, 0)
        recent_ts = "2026-06-06T11:30:00"  # within 24h
        records = [
            {"event": "claim", "id": "r1", "ts": recent_ts, "agent": "a"},
            {"event": "release", "id": "r1", "ts": recent_ts, "agent": "a"},
        ]
        keep, stale = pi.partition_records(records, now=now)
        assert len(stale) == 0, "recent released pair must not be stale"
        assert len(keep) == 2, "recent released pair must be kept"

    def test_live_claim_refuses_and_keeps_the_original_log(self, tmp_path: Path, pi) -> None:
        import datetime
        log = tmp_path / "dev" / "intents.jsonl"
        log.parent.mkdir(parents=True)
        log.write_text(json.dumps({
            "event": "claim", "id": "live", "ts": datetime.datetime.now().astimezone().isoformat(),
        }) + "\n", encoding="utf-8")
        before = log.read_bytes()
        result = pi.compact(log_path=log, grace_hours=0)
        assert result["refused"]
        assert "live claim" in result["refused"]
        assert log.read_bytes() == before

    @pytest.mark.parametrize("claim_offset,now_offset", [(-10, 14), (14, -10), (None, None)])
    @pytest.mark.parametrize("age_hours", [0, 5])
    def test_live_guard_compares_instants_across_offsets(
        self, tmp_path: Path, pi, claim_offset, now_offset, age_hours,
    ) -> None:
        import datetime
        utc = datetime.timezone.utc
        instant = datetime.datetime(2026, 11, 4, 12, tzinfo=utc)
        claim_time = instant - datetime.timedelta(hours=age_hours)
        claim_time = (claim_time.replace(tzinfo=None) if claim_offset is None else
                      claim_time.astimezone(datetime.timezone(datetime.timedelta(hours=claim_offset))))
        now = (instant.replace(tzinfo=None) if now_offset is None else
               instant.astimezone(datetime.timezone(datetime.timedelta(hours=now_offset))))
        log = tmp_path / "dev" / "intents.jsonl"
        self._write_log(log, [
            {"event": "claim", "id": "released", "ts": "2020-01-01T00:00:00"},
            {"event": "release", "id": "released", "ts": "2020-01-01T00:00:00"},
            {"event": "claim", "id": "held", "ts": claim_time.isoformat()},
        ])
        before = log.read_bytes()
        result = pi.compact(log_path=log, now=now)
        if age_hours == 0:
            assert "live claim" in result["refused"]
            assert log.read_bytes() == before
        else:
            assert not result.get("refused")
            assert result["pruned_count"] == 2
            assert [json.loads(line)["id"] for line in log.read_text().splitlines()] == ["held"]

    def test_changed_size_after_read_refuses_prune(self, tmp_path: Path, pi, monkeypatch) -> None:
        import datetime
        log = tmp_path / "dev" / "intents.jsonl"
        old = "2020-01-01T00:00:00"
        self._write_log(log, [
            {"event": "claim", "id": "old", "ts": old},
            {"event": "release", "id": "old", "ts": old},
        ])
        before = log.read_text(encoding="utf-8")
        appended = '{"event":"claim","id":"racer"}\n'
        original_iter = pi._iter_log

        def append_after_snapshot(path):
            records = list(original_iter(path))
            with path.open("a", encoding="utf-8") as stream:
                stream.write(appended)
            yield from records

        monkeypatch.setattr(pi, "_iter_log", append_after_snapshot)
        result = pi.compact(log_path=log, grace_hours=0,
                            now=datetime.datetime(2026, 1, 1))
        assert result["refused"] and "changed" in result["refused"]
        assert log.read_text(encoding="utf-8") == before + appended

    def test_hostile_temp_symlink_is_not_followed(self, tmp_path: Path, pi, monkeypatch) -> None:
        import datetime
        log = tmp_path / "dev" / "intents.jsonl"
        old = "2020-01-01T00:00:00"
        self._write_log(log, [
            {"event": "claim", "id": "old", "ts": old},
            {"event": "release", "id": "old", "ts": old},
        ])
        outside = tmp_path / "outside.txt"
        outside.write_text("keep\n", encoding="utf-8")
        monkeypatch.setattr(pi.secrets, "token_hex", lambda _n: "fixed")
        hostile = log.with_name(f"{log.name}.prune-{__import__('os').getpid()}-fixed.tmp")
        hostile.symlink_to(outside)
        before = log.read_bytes()
        result = pi.compact(log_path=log, grace_hours=0,
                            now=datetime.datetime(2026, 1, 1))
        assert result["refused"] and "temporary path" in result["refused"]
        assert log.read_bytes() == before
        assert outside.read_text(encoding="utf-8") == "keep\n"


@pytest.mark.parametrize("alias", [False, True], ids=["direct", "checkout-alias"])
@pytest.mark.parametrize("live", [False, True], ids=["compact-old", "live-refusal"])
def test_prune_and_claim_cli_choose_same_log_in_real_worktree(
    tmp_path: Path, alias: bool, live: bool,
) -> None:
    import os
    import shutil
    import subprocess

    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("GIT_", "CAIRN_", "CODEX_", "CLAUDE_", "PYTHON"))}
    env.update(CAIRN_AGENT="prune-origin", GIT_CONFIG_NOSYSTEM="1",
               GIT_CONFIG_GLOBAL=os.devnull)
    main = tmp_path / "main"
    linked = tmp_path / "linked"
    (main / "dev").mkdir(parents=True)
    (main / "dev" / "seed").write_text("seed\n", encoding="utf-8")
    for args in (["init", "-q"], ["add", "dev/seed"],
                 ["-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                  "commit", "-qm", "seed"],
                 ["worktree", "add", "-qb", "linked", str(linked)]):
        subprocess.run(["git", *args], cwd=main, env=env, check=True,
                       capture_output=True, text=True)
    tools = linked / "tools"
    tools.mkdir()
    for name in ("intent.py", "prune_intents.py"):
        shutil.copy2(_TEAM_GATED / name, tools / name)
    shutil.copytree(_TEAM_GATED / "_intent", tools / "_intent")
    root = linked
    if alias:
        root = tmp_path / "linked-alias"
        try:
            root.symlink_to(linked, target_is_directory=True)
        except OSError as exc:
            pytest.skip(f"symlinks unavailable: {exc}")
    logs = [main / "dev" / "intents.jsonl", linked / "dev" / "intents.jsonl"]
    for index, log in enumerate(logs):
        log.write_text("".join(json.dumps({"event": event, "id": f"old-{index}",
                                          "ts": "2020-01-01T00:00:00+00:00"}) + "\n"
                               for event in ("claim", "release")), encoding="utf-8")
    target, untouched = (logs[1], logs[0]) if alias else (logs[0], logs[1])
    untouched_before = untouched.read_bytes()
    if live:
        claim = subprocess.run(
            [sys.executable, str(root / "tools" / "intent.py"), "claim",
             "--files", "x", "--action", "origin check"],
            cwd=linked, env=env, capture_output=True, text=True,
        )
        assert claim.returncode == 0, claim.stderr
        assert ("using checkout-local claims log" in claim.stderr) == alias
        assert json.loads(target.read_text(encoding="utf-8").splitlines()[-1])["event"] == "claim"
    target_before = target.read_bytes()
    result = subprocess.run(
        [sys.executable, str(root / "tools" / "prune_intents.py")],
        cwd=linked, env=env, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert untouched.read_bytes() == untouched_before
    assert ("using checkout-local claims log" in result.stderr) == alias
    assert target.read_bytes() == (target_before if live else b"")
    assert ("live claim" in result.stderr) == live
    if alias:
        # A prior import from the direct path must not supply the alias context.
        code = '''
import importlib.util
from pathlib import Path
import sys
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
direct = load('direct_prune', sys.argv[1])
alias = load('alias_prune', sys.argv[2])
assert direct.INTENTS_LOG_PATH == Path(sys.argv[3])
assert alias.INTENTS_LOG_PATH == Path(sys.argv[4])
'''
        imported = subprocess.run(
            [sys.executable, "-c", code, str(tools / "prune_intents.py"),
             str(root / "tools" / "prune_intents.py"), str(logs[0]), str(logs[1])],
            cwd=linked, env=env, capture_output=True, text=True,
        )
        assert imported.returncode == 0, imported.stderr
