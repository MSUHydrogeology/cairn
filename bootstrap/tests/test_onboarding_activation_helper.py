"""Tests for ``scripts/onboarding_activate.py``: the
progressive-onboarding activation helper (Chunk P1.2).

Plan: 2026-05-28-claude-cairn-progressive-onboarding.

Covers per Codex External Review P2-4 + P2-5 + the plan's helper
contract:

* Schema: ``ActivationRecord`` round-trips through JSONL (write +
  read, single line per activation; key set + order stable).
* Atomic-append behavior: each ``append_activation_log`` call
  preserves the existing file content + adds the new line(s); no
  partial-line truncation under stat.
* Idempotency on unchanged state: a fresh ``activate()`` run when
  no new triggers fire is a no-op (no PLANNING edit; no log append).
* Preset-metadata resolution: helper reads
  ``<!-- preset: <name> -->`` from the slot body to find the
  installed source file (Codex P2-4 contract).  Helper given a slot
  WITHOUT the metadata errors with a recoverable
  ``OnboardingError`` whose message names ``--seed --preset``.
* Helper activates eligible deferred tasks (those whose trigger
  fired AND id is not in the log) when injected with a fired-set.
* Scaffold installs the helper script + seeds an empty activation
  log at install time per Codex P2-5 (always-installed; not
  preset-conditional).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_onboarding_activation_helper.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import main  # noqa: E402

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
HELPER_SRC = (
    CAIRN_ROOT
    / "templates"
    / "modules"
    / "default-on"
    / "onboarding_activate.py"
)

pytestmark = pytest.mark.skipif(
    not HELPER_SRC.exists(), reason="onboarding_activate.py source missing",
)


def _load_helper(name: str = "_onboarding_activate_under_test") -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, HELPER_SRC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def helper() -> ModuleType:
    return _load_helper()


def _scaffold(target: Path, preset: str | None) -> int:
    cfg = target / "profile.yml"
    body = "project_name: ActivationTest\ntest_command: pytest\n"
    if preset is None:
        body += "modules:\n  - reflections\n"
    else:
        body += f"preset: {preset}\n"
    cfg.write_text(body)
    return main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT)]
    )


# ---------------------------------------------------------------------------
# Schema + JSONL round-trip
# ---------------------------------------------------------------------------


class TestActivationRecordSchema:
    def test_round_trip(self, helper: ModuleType) -> None:
        rec = helper.ActivationRecord(
            task_id="dev-tour-walkthrough",
            activated_at="2026-05-29T11:00:00Z",
            by_agent="claude-abc123",
            source_preset="solo-greenfield",
            trigger="first-proposal-archived",
        )
        line = rec.to_jsonl()
        parsed = helper.ActivationRecord.from_jsonl_line(line)
        assert parsed == rec

    def test_skip_blank_and_comment_lines(self, helper: ModuleType) -> None:
        assert helper.ActivationRecord.from_jsonl_line("") is None
        assert helper.ActivationRecord.from_jsonl_line("# comment") is None
        assert (
            helper.ActivationRecord.from_jsonl_line("   \n") is None
        )

    def test_malformed_json_returns_none(self, helper: ModuleType) -> None:
        assert helper.ActivationRecord.from_jsonl_line("not json {") is None

    def test_missing_keys_returns_none(self, helper: ModuleType) -> None:
        assert (
            helper.ActivationRecord.from_jsonl_line('{"task-id": "x"}')
            is None
        )


# ---------------------------------------------------------------------------
# Atomic-append behavior
# ---------------------------------------------------------------------------


class TestAtomicAppend:
    def test_append_preserves_prior_content(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        log = tmp_path / "log.jsonl"
        log.write_text(helper._ONBOARDING_LOG_HEADER if hasattr(
            helper, "_ONBOARDING_LOG_HEADER",
        ) else "# header\n", encoding="utf-8")
        rec_a = helper.ActivationRecord(
            "a", "2026-05-29T00:00:00Z", "agent-1", "solo-greenfield", "t1",
        )
        rec_b = helper.ActivationRecord(
            "b", "2026-05-30T00:00:00Z", "agent-2", "solo-greenfield", "t2",
        )
        helper.append_activation_log(log, [rec_a])
        helper.append_activation_log(log, [rec_b])
        # Both records present + the header preserved.
        text = log.read_text(encoding="utf-8")
        assert "# header" in text or "onboarding-activated.jsonl" in text
        # Reading back returns both records in order.
        records = helper.read_activation_log(log)
        assert [r.task_id for r in records] == ["a", "b"]

    def test_append_empty_is_noop(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        log = tmp_path / "log.jsonl"
        log.write_text("# header\n", encoding="utf-8")
        before = log.read_text(encoding="utf-8")
        helper.append_activation_log(log, [])
        after = log.read_text(encoding="utf-8")
        assert before == after


# ---------------------------------------------------------------------------
# Preset metadata resolution
# ---------------------------------------------------------------------------


class TestPresetResolution:
    def test_extracts_preset_name_from_slot(self, helper: ModuleType) -> None:
        planning = (
            "Some prose.\n"
            "<!-- cairn:slot onboarding-tasks -->\n"
            "<!-- preset: solo-greenfield -->\n"
            "\n"
            "* [seed; id: x]\n"
            "<!-- cairn:end onboarding-tasks -->\n"
            "After.\n"
        )
        assert helper.extract_preset_from_slot(planning) == "solo-greenfield"

    def test_returns_none_when_no_metadata(
        self, helper: ModuleType,
    ) -> None:
        planning = (
            "<!-- cairn:slot onboarding-tasks -->\n"
            "(Empty slot.)\n"
            "<!-- cairn:end onboarding-tasks -->\n"
        )
        assert helper.extract_preset_from_slot(planning) is None

    def test_returns_none_when_slot_missing(
        self, helper: ModuleType,
    ) -> None:
        assert helper.extract_preset_from_slot("no slot here") is None


# ---------------------------------------------------------------------------
# activate() end-to-end (using injected fired_triggers_override)
# ---------------------------------------------------------------------------


class TestActivateFlow:
    def test_no_fired_triggers_is_noop(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        assert _scaffold(tmp_path, "solo-greenfield") == 0
        outcome = helper.activate(
            tmp_path, fired_triggers_override=set(),
        )
        assert outcome.pending == []
        assert outcome.planning_updated is False
        assert outcome.log_records == []

    def test_fired_trigger_activates_deferred_task(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        assert _scaffold(tmp_path, "solo-greenfield") == 0
        # The solo-greenfield placeholder has a deferred task whose
        # trigger is `first-proposal-archived`.  Force that trigger
        # to fire via the override.
        outcome = helper.activate(
            tmp_path,
            by_agent="claude-test",
            fired_triggers_override={"first-proposal-archived"},
        )
        assert len(outcome.pending) == 1
        assert outcome.pending[0].trigger == "first-proposal-archived"
        assert outcome.planning_updated is True
        assert len(outcome.log_records) == 1
        # The PLANNING slot now carries the activated task's body.
        planning = (tmp_path / "dev" / "PLANNING.md").read_text(
            encoding="utf-8",
        )
        assert "[trigger: first-proposal-archived;" in planning
        # The log file has the activation record.
        log_text = (
            tmp_path / "dev" / ".cairn" / "onboarding-activated.jsonl"
        ).read_text(encoding="utf-8")
        assert "first-proposal-archived" in log_text

    def test_idempotent_rerun_after_activation(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        assert _scaffold(tmp_path, "solo-greenfield") == 0
        # First run: activate.
        helper.activate(
            tmp_path,
            by_agent="claude-test",
            fired_triggers_override={"first-proposal-archived"},
        )
        # Second run with same trigger: no-op because the id is now
        # in the log.
        outcome = helper.activate(
            tmp_path,
            by_agent="claude-test",
            fired_triggers_override={"first-proposal-archived"},
        )
        assert outcome.pending == []
        assert outcome.planning_updated is False
        assert outcome.log_records == []

    def test_dry_run_does_not_write(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        assert _scaffold(tmp_path, "solo-greenfield") == 0
        planning_path = tmp_path / "dev" / "PLANNING.md"
        log_path = tmp_path / "dev" / ".cairn" / "onboarding-activated.jsonl"
        before_planning = planning_path.read_text(encoding="utf-8")
        before_log = log_path.read_text(encoding="utf-8")
        outcome = helper.activate(
            tmp_path,
            by_agent="claude-test",
            dry_run=True,
            fired_triggers_override={"first-proposal-archived"},
        )
        # Pending was computed + log_records prepared, but neither
        # file was actually modified.
        assert len(outcome.pending) == 1
        assert outcome.planning_updated is False
        assert planning_path.read_text(encoding="utf-8") == before_planning
        assert log_path.read_text(encoding="utf-8") == before_log

    def test_missing_preset_metadata_raises_recoverable(
        self, helper: ModuleType, tmp_path: Path,
    ) -> None:
        """Helper given an adopter tree whose PLANNING slot has no
        preset metadata raises ``OnboardingError`` with a message
        naming the ``--seed`` recovery path."""
        assert _scaffold(tmp_path, None) == 0  # explicit-modules path
        with pytest.raises(helper.OnboardingError) as excinfo:
            helper.activate(
                tmp_path,
                fired_triggers_override={"first-proposal-archived"},
            )
        assert "--seed" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Scaffold integration: helper + log seeded at install time (P2-5)
# ---------------------------------------------------------------------------


class TestScaffoldSeedsAlways:
    def test_scaffold_with_preset_installs_helper_and_log(
        self, tmp_path: Path,
    ) -> None:
        assert _scaffold(tmp_path, "solo-greenfield") == 0
        assert (tmp_path / "scripts" / "onboarding_activate.py").is_file()
        assert (
            tmp_path / "dev" / ".cairn" / "onboarding-activated.jsonl"
        ).is_file()

    def test_scaffold_without_preset_still_installs_helper_and_log(
        self, tmp_path: Path,
    ) -> None:
        """The helper + log are always-installed -- Codex P2-5.
        Even an adopter using the explicit-modules path gets them, so
        opt-in via --seed (Chunk P1.11) can succeed later."""
        assert _scaffold(tmp_path, None) == 0
        assert (tmp_path / "scripts" / "onboarding_activate.py").is_file()
        assert (
            tmp_path / "dev" / ".cairn" / "onboarding-activated.jsonl"
        ).is_file()

    def test_seeded_log_is_header_only(self, tmp_path: Path) -> None:
        """The seeded log carries only the header comment -- no
        activation records on a fresh install."""
        assert _scaffold(tmp_path, "solo-greenfield") == 0
        log = (
            tmp_path / "dev" / ".cairn" / "onboarding-activated.jsonl"
        ).read_text(encoding="utf-8")
        # Every line is either blank or a `#`-comment.
        for line in log.splitlines():
            assert line == "" or line.startswith("#"), (
                f"non-comment line in freshly-seeded log: {line!r}"
            )
