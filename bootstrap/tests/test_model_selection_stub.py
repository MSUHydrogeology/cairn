"""Tests for the Fold 5 model-selection stub mapping + fidelity gate.

Covers:
* Stub file is installed on scaffold of ``model-selection`` module.
* Check script is installed verbatim.
* Fidelity check: exits 0 on a filled (no ``FILL ME``) mapping.
* Fidelity check: exits 1 (non-zero) on an unfilled (``FILL ME``) mapping.
* Fidelity check: exits 2 when the mapping file is missing entirely.
* Seed-vs-gate: a fresh scaffold installs a stub that passes the gate.

Run from the cairn repo root::

    python -m pytest bootstrap/tests/test_model_selection_stub.py
"""
from __future__ import annotations

import builtins
import io
import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
_TEAM_GATED = TEMPLATES_ROOT / "modules" / "team-gated"
_CHECKER_SRC = _TEAM_GATED / "check_model_selection.py"
_STUB_SRC = _TEAM_GATED / "model_selection_mapping_stub.yml"

sys.path.insert(0, str(CAIRN_ROOT))
from bootstrap.scaffold import _MODULE_MAPPINGS, main as scaffold_main  # noqa: E402
from bootstrap._scaffold.install import (  # noqa: E402
    _mapping_is_unfilled,
    capture_model_selection_mapping,
    model_selection_notice_lines,
)
from bootstrap._scaffold.security import ScaffoldSecurityError  # noqa: E402

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _load_checker(name: str = "_cairn_check_model_sel_under_test") -> ModuleType:
    if not _CHECKER_SRC.exists():
        pytest.skip("check_model_selection.py template not available")
    spec = importlib.util.spec_from_file_location(name, _CHECKER_SRC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _run_bare_checker(checker: ModuleType, mapping: Path, monkeypatch) -> int:
    real_import = builtins.__import__

    def _no_yaml(name, *args, **kwargs):
        if name == "yaml":
            raise ImportError("simulated: PyYAML not installed")
        return real_import(name, *args, **kwargs)

    with monkeypatch.context() as mp:
        mp.setattr(builtins, "__import__", _no_yaml)
        return checker.check_mapping(mapping, quiet=True)


def _scaffold(target: Path) -> int:
    cfg = target / "profile.yml"
    cfg.write_text(
        "project_name: ModelSelTest\ntest_command: pytest\nmodules:\n"
        "  - model-selection\n"
    )
    return scaffold_main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
    )


# ---------------------------------------------------------------------------
# Module registration
# ---------------------------------------------------------------------------

class TestModuleRegistration:
    def test_stub_registered(self) -> None:
        specs = _MODULE_MAPPINGS["model-selection"]
        dsts = {s.dst: s for s in specs}
        assert "dev/.cairn/model-selection-mapping.yml" in dsts, (
            "model-selection-mapping.yml stub not registered under "
            "'model-selection' module"
        )
        # The stub is a YAML template (substituted, not verbatim).
        assert dsts["dev/.cairn/model-selection-mapping.yml"].verbatim is False

    def test_checker_registered(self) -> None:
        specs = _MODULE_MAPPINGS["model-selection"]
        dsts = {s.dst: s for s in specs}
        assert "scripts/check_model_selection.py" in dsts, (
            "check_model_selection.py not registered under 'model-selection' module"
        )
        assert dsts["scripts/check_model_selection.py"].verbatim is True


# ---------------------------------------------------------------------------
# Install-path
# ---------------------------------------------------------------------------

class TestInstallPath:
    def test_stub_installed_on_scaffold(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path) == 0
        stub = tmp_path / "dev" / ".cairn" / "model-selection-mapping.yml"
        assert stub.is_file(), "model-selection-mapping.yml not installed"

    def test_checker_installed_on_scaffold(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path) == 0
        checker = tmp_path / "scripts" / "check_model_selection.py"
        assert checker.is_file(), "check_model_selection.py not installed"
        assert checker.read_bytes() == _CHECKER_SRC.read_bytes(), (
            "Installed check_model_selection.py differs from template"
        )


# ---------------------------------------------------------------------------
# Seed-vs-gate sequencing: fresh install passes the gate
# ---------------------------------------------------------------------------

class TestSeedVsGate:
    """A fresh scaffold seeds an unfilled FILL-ME stub that FAILS the gate
    (forced, not silent) — while the scaffold install itself succeeds."""

    def test_fresh_scaffold_install_succeeds(self, tmp_path: Path) -> None:
        # "Not instantly red" = the install is not blocked.
        assert _scaffold(tmp_path) == 0
        stub = tmp_path / "dev" / ".cairn" / "model-selection-mapping.yml"
        assert stub.is_file()

    def test_fresh_scaffold_fails_gate_until_filled(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path) == 0
        stub = tmp_path / "dev" / ".cairn" / "model-selection-mapping.yml"
        assert stub.is_file()

        checker = _load_checker()
        # A fresh, unfilled mapping carries FILL ME -> the gate FAILS,
        # forcing the adopter to record their assignments (not silent-empty).
        rc = checker.check_mapping(stub, quiet=True)
        assert rc == 1, (
            f"Fresh scaffold stub is unfilled (carries FILL ME) and MUST fail "
            f"the gate to force the adopter to complete it; got exit code {rc}"
        )


# ---------------------------------------------------------------------------
# Fidelity check: pass / fail / missing
# ---------------------------------------------------------------------------

class TestFidelityCheck:
    @pytest.fixture(scope="class")
    def checker(self) -> ModuleType:
        return _load_checker()

    def test_filled_mapping_passes(self, tmp_path: Path, checker) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "# Model selection mapping\n"
            "mapping:\n"
            "  - tier: high\n"
            "    model: vendor-a/flagship\n"
            "    date_verified: 2025-01-01\n"
            "    task_family: strategy\n"
            "    source: benchmark-jan-2025\n"
        )
        rc = checker.check_mapping(mapping, quiet=True)
        assert rc == 0, f"Fully filled mapping should pass; got {rc}"

    def test_unfilled_mapping_fails_nonzero(self, tmp_path: Path, checker) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "mapping:\n"
            "  - tier: high\n"
            "    model: FILL ME\n"
            "    date_verified: FILL ME\n"
            "    task_family: strategy\n"
            "    source: FILL ME\n"
        )
        rc = checker.check_mapping(mapping, quiet=True)
        assert rc != 0, "Mapping with FILL ME should fail the gate"
        assert rc == 1, f"Expected exit code 1, got {rc}"

    def test_missing_mapping_exits_2(self, tmp_path: Path, checker) -> None:
        missing = tmp_path / "no-such.yml"
        rc = checker.check_mapping(missing, quiet=True)
        assert rc == 2, f"Missing mapping file should exit 2, got {rc}"

    def test_partial_fill_still_fails(self, tmp_path: Path, checker) -> None:
        """A partially filled mapping that still contains one FILL ME fails."""
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "mapping:\n"
            "  - tier: high\n"
            "    model: vendor-a/flagship\n"
            "    date_verified: 2025-01-01\n"
            "    task_family: strategy\n"
            "    source: FILL ME\n"  # still unfilled
        )
        rc = checker.check_mapping(mapping, quiet=True)
        assert rc == 1, f"Partial fill with FILL ME should fail; got {rc}"

    def test_cli_failure_message_mentions_fill_me(
        self, tmp_path: Path, checker, capsys
    ) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text("mapping:\n  - tier: high\n    model: FILL ME\n")
        rc = checker.main(["--mapping", str(mapping)])
        assert rc == 1
        err = capsys.readouterr().err
        assert "FILL ME" in err

    def test_cli_success_no_error_output(
        self, tmp_path: Path, checker, capsys
    ) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "mapping:\n"
            "  - tier: high\n"
            "    model: vendor/flagship\n"
            "    date_verified: 2025-01-01\n"
            "    task_family: strategy\n"
            "    source: benchmark\n"
        )
        rc = checker.main(["--mapping", str(mapping)])
        assert rc == 0
        err = capsys.readouterr().err
        assert err == ""


# ---------------------------------------------------------------------------
# Full-line comments are not placeholders
# ---------------------------------------------------------------------------

class TestCommentsAreNotPlaceholders:
    """Full-line comments (leading spaces then ``#``) are skipped so the seeded
    stub's explanatory comments do not fail a hand-filled mapping, while
    trailing comments and value lines still fail."""

    @pytest.fixture(scope="class")
    def checker(self) -> ModuleType:
        return _load_checker()

    def test_hand_filled_stub_with_comments_kept_passes(
        self, tmp_path: Path, checker, monkeypatch
    ) -> None:
        stub_text = _STUB_SRC.read_text(encoding="utf-8")
        filled = (
            stub_text.replace("tier: FILL ME", "tier: high")
            .replace("model: FILL ME", "model: vendor-a/flagship-family")
            .replace("date_verified: FILL ME", "date_verified: 2026-10-18")
            .replace("task_family: FILL ME", "task_family: strategy")
            .replace("source: FILL ME", "source: maintainer")
        )
        assert "# " in filled and "FILL ME" in filled
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(filled, encoding="utf-8")
        assert checker.check_mapping(mapping, quiet=True) == 0
        assert _run_bare_checker(checker, mapping, monkeypatch) == 0

    def test_shipped_stub_fails(
        self, tmp_path: Path, checker, monkeypatch
    ) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(_STUB_SRC.read_text(encoding="utf-8"), encoding="utf-8")
        assert checker.check_mapping(mapping, quiet=True) == 1
        assert _run_bare_checker(checker, mapping, monkeypatch) == 1

    def test_trailing_comment_with_fill_me_on_value_line_fails(
        self, tmp_path: Path, checker, monkeypatch
    ) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "mapping:\n"
            "  - tier: high\n"
            "    model: vendor-a/flagship  # FILL ME\n",
            encoding="utf-8",
        )
        assert checker.check_mapping(mapping, quiet=True) == 1
        assert _run_bare_checker(checker, mapping, monkeypatch) == 1

    def test_todo_fill_me_full_line_comment_above_filled_rows_passes(
        self, tmp_path: Path, checker, monkeypatch
    ) -> None:
        """The check attests shape, not intent: a full-line ``# TODO: FILL ME``
        comment above filled rows passes because full-line comments are skipped
        so the stub's own header comments can remain in place."""
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "# TODO: FILL ME -- add medium-tier model here\n"
            "mapping:\n"
            "  - tier: high\n"
            "    model: vendor-a/flagship-family\n"
            "    date_verified: 2026-10-18\n"
            "    task_family: strategy\n"
            "    source: maintainer\n",
            encoding="utf-8",
        )
        assert checker.check_mapping(mapping, quiet=True) == 0
        assert _run_bare_checker(checker, mapping, monkeypatch) == 0


# ---------------------------------------------------------------------------
# Row requirement
# ---------------------------------------------------------------------------

class TestAMappingNeedsAtLeastOneRow:
    @pytest.fixture(scope="class")
    def checker(self) -> ModuleType:
        return _load_checker()

    def test_empty_mapping_list_with_comments_fails_on_both_paths(
        self, tmp_path: Path, checker, monkeypatch, capsys
    ) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "# Header comment\n"
            "mapping: []\n",
            encoding="utf-8",
        )
        assert checker.check_mapping(mapping, quiet=False) == 1
        err_yaml = capsys.readouterr().err
        assert "no rows" in err_yaml
        assert "FILL ME" not in err_yaml

        assert _run_bare_checker(checker, mapping, monkeypatch) == 1

    def test_comments_only_file_exits_1_bare_and_3_with_yaml(
        self, tmp_path: Path, checker, monkeypatch
    ) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text("# Only comments here\n", encoding="utf-8")
        assert checker.check_mapping(mapping, quiet=True) == 3
        assert _run_bare_checker(checker, mapping, monkeypatch) == 1

    @pytest.mark.parametrize(
        "body",
        [
            "other_key: 1\n",
            "mapping: not-a-list\n",
            "mapping: {}\n",
        ],
    )
    def test_missing_or_non_list_mapping_exits_1_with_yaml(
        self, tmp_path: Path, checker, body: str
    ) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(body, encoding="utf-8")
        assert checker.check_mapping(mapping, quiet=True) == 1


# ---------------------------------------------------------------------------
# Parsed values scanned when PyYAML is present
# ---------------------------------------------------------------------------

class TestParsedValuesAreScannedWhenYamlIsPresent:
    @pytest.fixture(scope="class")
    def checker(self) -> ModuleType:
        return _load_checker()

    @pytest.mark.parametrize(
        "body",
        [
            "mapping:\n  - tier: high\n    model: |\n      # FILL ME\n",
            "mapping:\n  - tier: high\n    model: FILL\n      ME\n",
            'mapping:\n  - tier: high\n    model: "FILL\n      ME"\n',
            'mapping:\n  - tier: high\n    model: "FILL \\\n      ME"\n',
            'mapping:\n  - tier: high\n    model: "FILL\\x20ME"\n',
            "mapping:\n  - tier: high\n    model: !!binary RklMTCBNRQ==\n",
            'mapping:\n  - tier: high\n    extra: !!set {"FILL\\x20ME"}\n',
            'mapping:\n  - tier: high\n    "FILL\\x20ME": vendor-a/flagship\n',
        ],
    )
    def test_parsed_value_carrying_fill_me_fails(
        self, tmp_path: Path, checker, body: str
    ) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(body, encoding="utf-8")
        assert checker.check_mapping(mapping, quiet=True) == 1


# ---------------------------------------------------------------------------
# Merge keys refused and depth / aliasing bounds
# ---------------------------------------------------------------------------

class TestMergeKeysAreRefused:
    @pytest.fixture(scope="class")
    def checker(self) -> ModuleType:
        return _load_checker()

    def test_merge_key_chain_exits_3_within_timeout(self, tmp_path: Path) -> None:
        lines = ["l0: &l0 {k0: 1}"]
        for i in range(1, 25):
            prev = f"*l{i - 1}"
            lines.append(f"l{i}: &l{i} {{<<: [{prev}, {prev}], k{i}: 1}}")
        lines.append("mapping:\n  - tier: high\n    model: vendor-a/flagship\n")
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text("\n".join(lines), encoding="utf-8")

        proc = subprocess.run(
            [sys.executable, str(_CHECKER_SRC), "--mapping", str(mapping)],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        assert proc.returncode == 3
        assert "not valid YAML" in proc.stderr


class TestValueScanVisitsEachObjectOnce:
    def test_nested_alias_document_completes_quickly(self, tmp_path: Path) -> None:
        lines = ['a0: &a0 ["vendor-a/flagship", "vendor-a/flagship"]']
        for i in range(1, 23):
            prev = f"*a{i - 1}"
            lines.append(f"a{i}: &a{i} [{prev}, {prev}]")
        lines.append("mapping:\n  - tier: high\n    model: vendor-a/flagship\n")
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text("\n".join(lines), encoding="utf-8")

        proc = subprocess.run(
            [sys.executable, str(_CHECKER_SRC), "--mapping", str(mapping)],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        assert proc.returncode == 0

    def test_deep_flow_sequence_exits_3_without_traceback(
        self, tmp_path: Path, capsys
    ) -> None:
        checker = _load_checker()
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "mapping:\n  - tier: high\n    extra: " + ("[" * 5000) + ("]" * 5000) + "\n",
            encoding="utf-8",
        )
        rc = checker.main(["--mapping", str(mapping)])
        assert rc == 3
        err = capsys.readouterr().err
        assert "not valid YAML" in err
        assert "Traceback" not in err


# ---------------------------------------------------------------------------
# Checker messages carry no parsed value
# ---------------------------------------------------------------------------

class TestCheckerMessagesCarryNoParsedValue:
    def test_escape_sequences_in_values_never_reach_output(
        self, tmp_path: Path, capsys
    ) -> None:
        checker = _load_checker()
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            'mapping:\n  - tier: high\n    model: "\\e]0;PWNED\\aFILL\\x20ME"\n',
            encoding="utf-8",
        )
        assert checker.main(["--mapping", str(mapping)]) == 1
        captured = capsys.readouterr()
        assert "\x1b" not in captured.out and "\x1b" not in captured.err
        assert "\x07" not in captured.out and "\x07" not in captured.err

        no_row = tmp_path / "no-row.yml"
        no_row.write_text(
            'mapping: []\nnote: "\\e]0;PWNED\\a"\n',
            encoding="utf-8",
        )
        assert checker.main(["--mapping", str(no_row)]) == 1
        captured_no_row = capsys.readouterr()
        assert "\x1b" not in captured_no_row.out and "\x1b" not in captured_no_row.err
        assert "\x07" not in captured_no_row.out and "\x07" not in captured_no_row.err
        assert "FILL ME" not in captured_no_row.err


# ---------------------------------------------------------------------------
# Bare-path residual and docstring
# ---------------------------------------------------------------------------

class TestBarePathResidualIsPinned:
    def test_docstring_names_bare_path_residual_classes(self) -> None:
        doc = _load_checker().__doc__ or ""
        assert "not spelled out on one non-comment line" in doc
        assert "row-shaped line that is not an item" in doc

    def test_copies_are_byte_identical(self) -> None:
        installed = CAIRN_ROOT / "scripts" / "check_model_selection.py"
        assert _CHECKER_SRC.read_bytes() == installed.read_bytes()


# ---------------------------------------------------------------------------
# Repository's own mapping passes
# ---------------------------------------------------------------------------

class TestThisRepositorysMappingIsFilled:
    def test_cairn_mapping_passes_with_and_without_pyyaml(
        self, monkeypatch
    ) -> None:
        checker = _load_checker()
        repo_mapping = CAIRN_ROOT / "dev" / ".cairn" / "model-selection-mapping.yml"
        assert checker.check_mapping(repo_mapping, quiet=True) == 0
        assert _run_bare_checker(checker, repo_mapping, monkeypatch) == 0


# ---------------------------------------------------------------------------
# Corpus and named spelling table
# ---------------------------------------------------------------------------

_LEADS: tuple[tuple[str, str], ...] = (
    ("none", ""),
    ("space", "  "),
    ("tab", "\t"),
    ("nbsp", "\u00a0"),
    ("ff", "\x0c"),
    ("bom", "\ufeff"),
)

_BREAKS: tuple[tuple[str, str], ...] = (
    ("crlf", "\r\n"),
    ("lf", "\n"),
    ("cr", "\r"),
    ("nel", "\x85"),
    ("ls", "\u2028"),
    ("ps", "\u2029"),
)

_POSITIONS: tuple[str, ...] = ("comment", "value", "row")


def _build_generated_corpus() -> list[tuple[str, str, int]]:
    """Build 108 files: 6 leads x 6 breaks x 3 positions.
    Returns (case_id, text, expected_bare_rc) tuples."""
    cases: list[tuple[str, str, int]] = []
    for lead_name, lead in _LEADS:
        for brk_name, brk in _BREAKS:
            for pos in _POSITIONS:
                if pos == "comment":
                    text = (
                        f"{lead}# FILL ME{brk}"
                        f"mapping:{brk}"
                        f"  - tier: high{brk}"
                        f"    model: vendor-a/flagship{brk}"
                    )
                    # Only empty or ASCII spaces before '#' makes a comment.
                    expected_rc = 0 if lead in ("", "  ") else 1
                elif pos == "value":
                    text = (
                        f"# header{brk}"
                        f"mapping:{brk}"
                        f"  - tier: high{brk}"
                        f"{lead}model: FILL ME{brk}"
                    )
                    expected_rc = 1
                else:
                    text = (
                        f"# header{brk}"
                        f"mapping:{brk}"
                        f"{lead}- tier: high{brk}"
                        f"    model: vendor-a/flagship{brk}"
                    )
                    # Only empty or ASCII spaces before '- tier:' matches row regex.
                    expected_rc = 0 if lead in ("", "  ") else 1
                cases.append((f"{lead_name}-{brk_name}-{pos}", text, expected_rc))
    assert len(cases) == 108
    return cases


#: Named spelling table: (name, text, bare_rc, yaml_rc, engine_unfilled, category).
_NAMED_SPELLINGS: tuple[tuple[str, str, int, int, bool, str], ...] = (
    (
        "block-scalar-hash-fill-me",
        "mapping:\n  - tier: high\n    model: |\n      # FILL ME\n",
        0,
        1,
        False,
        "stricter_with_yaml",
    ),
    (
        "folded-plain-fill-me",
        "mapping:\n  - tier: high\n    model: FILL\n      ME\n",
        0,
        1,
        False,
        "stricter_with_yaml",
    ),
    (
        "folded-quoted-fill-me",
        'mapping:\n  - tier: high\n    model: "FILL\n      ME"\n',
        0,
        1,
        False,
        "stricter_with_yaml",
    ),
    (
        "line-continuation-fill-me",
        'mapping:\n  - tier: high\n    model: "FILL \\\n      ME"\n',
        0,
        1,
        False,
        "stricter_with_yaml",
    ),
    (
        "hex-escape-fill-me",
        'mapping:\n  - tier: high\n    model: "FILL\\x20ME"\n',
        0,
        1,
        False,
        "stricter_with_yaml",
    ),
    (
        "repeated-empty-mapping-key",
        "mapping:\n  - tier: high\n    model: vendor-a/flagship\nmapping: []\n",
        0,
        1,
        False,
        "stricter_with_yaml",
    ),
    (
        "binary-tag-fill-me",
        "mapping:\n  - tier: high\n    model: !!binary RklMTCBNRQ==\n",
        0,
        1,
        False,
        "stricter_with_yaml",
    ),
    (
        "set-tag-fill-me",
        'mapping:\n  - tier: high\n    extra: !!set {"FILL\\x20ME"}\n',
        0,
        1,
        False,
        "stricter_with_yaml",
    ),
    (
        "row-under-other-key",
        "mapping: []\nother:\n  - tier: high\n",
        0,
        1,
        False,
        "stricter_with_yaml",
    ),
    (
        "row-inside-block-scalar",
        "mapping: []\nnote: |\n  - tier: high\n",
        0,
        1,
        False,
        "stricter_with_yaml",
    ),
    (
        "row-inside-multiline-quoted-value",
        'mapping: []\nnote: "hello\n  - tier: high"\n',
        0,
        1,
        False,
        "stricter_with_yaml",
    ),
    (
        "one-line-list-first-key-not-tier",
        "mapping: [{model: vendor-a/flagship, tier: high}]\n",
        1,
        0,
        True,
        "looser_with_yaml",
    ),
    (
        "mapping-item-without-tier-key",
        "mapping:\n  - model: vendor-a/flagship\n",
        1,
        0,
        True,
        "looser_with_yaml",
    ),
    (
        "list-of-non-mappings",
        "mapping:\n  - vendor-a/flagship\n",
        1,
        0,
        True,
        "looser_with_yaml",
    ),
    (
        "tier-colon-inside-another-value",
        'mapping:\n  - model: "tier: high"\n',
        1,
        0,
        True,
        "looser_with_yaml",
    ),
    (
        "double-quoted-tier-key",
        'mapping:\n  - "tier": high\n    model: vendor-a/flagship\n',
        0,
        0,
        False,
        "agreed_after_widening",
    ),
    (
        "single-quoted-tier-key",
        "mapping:\n  - 'tier': high\n    model: vendor-a/flagship\n",
        0,
        0,
        False,
        "agreed_after_widening",
    ),
    (
        "one-line-list-starting-with-tier",
        "mapping: [{tier: high, model: vendor-a/flagship}]\n",
        0,
        0,
        False,
        "agreed_after_widening",
    ),
    (
        "comments-only-file",
        "# only a comment\n",
        1,
        3,
        True,
        "comments_only",
    ),
)


class TestEngineAndCheckerAgreeOnUnfilled:
    @pytest.fixture(scope="class")
    def checker(self) -> ModuleType:
        return _load_checker()

    def test_generated_108_corpus_on_bare_checker(
        self, tmp_path: Path, checker, monkeypatch
    ) -> None:
        corpus = _build_generated_corpus()
        for case_id, text, expected_rc in corpus:
            mapping = tmp_path / f"{case_id}.yml"
            mapping.write_bytes(text.encode("utf-8"))
            actual_rc = _run_bare_checker(checker, mapping, monkeypatch)
            assert actual_rc == expected_rc, (
                f"{case_id}: expected bare rc {expected_rc}, got {actual_rc}"
            )
            assert _mapping_is_unfilled(text) == (expected_rc == 1), case_id

    def test_named_spelling_table_on_bare_and_yaml_checker(
        self, tmp_path: Path, checker, monkeypatch
    ) -> None:
        for name, text, expected_bare, expected_yaml, _eng, category in _NAMED_SPELLINGS:
            mapping = tmp_path / f"{name}.yml"
            mapping.write_text(text, encoding="utf-8")
            bare_rc = _run_bare_checker(checker, mapping, monkeypatch)
            yaml_rc = checker.check_mapping(mapping, quiet=True)
            assert bare_rc == expected_bare, (
                f"{name}: expected bare rc {expected_bare}, got {bare_rc}"
            )
            assert yaml_rc == expected_yaml, (
                f"{name}: expected yaml rc {expected_yaml}, got {yaml_rc}"
            )
            assert _mapping_is_unfilled(text) == _eng, name
            if category == "stricter_with_yaml":
                assert bare_rc == 0 and yaml_rc == 1, name
            elif category == "looser_with_yaml":
                assert bare_rc == 1 and yaml_rc == 0, name
            elif category == "agreed_after_widening":
                assert bare_rc == 0 and yaml_rc == 0, name
            elif category == "comments_only":
                assert bare_rc == 1 and yaml_rc == 3, name
            else:
                pytest.fail(f"unexpected category {category} for {name}")


# ---------------------------------------------------------------------------
# Structural validity: yaml.safe_load + graceful
# degradation when PyYAML is absent.
# ---------------------------------------------------------------------------

class TestStructuralValidity:
    @pytest.fixture(scope="class")
    def checker(self) -> ModuleType:
        return _load_checker()

    def test_valid_filled_passes_structural(
        self, tmp_path: Path, checker
    ) -> None:
        """A filled, structurally valid mapping passes (the structural check
        runs and is satisfied)."""
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text(
            "mapping:\n"
            "  - tier: high\n"
            "    model: vendor-a/flagship\n"
            "    source: benchmark\n"
        )
        assert checker.check_mapping(mapping, quiet=True) == 0

    def test_malformed_yaml_filled_fails_3(
        self, tmp_path: Path, checker
    ) -> None:
        """A filled (no FILL ME) but malformed-YAML mapping passes the sentinel
        scan yet fails the structural check -- exit 3, not a silent pass that
        crashes the loader later."""
        mapping = tmp_path / "model-selection-mapping.yml"
        # Unbalanced flow sequence -> yaml.safe_load raises YAMLError. No
        # "FILL ME" present, so it clears the sentinel scan.
        mapping.write_text("mapping: [unclosed\n  - tier: high\n")
        rc = checker.check_mapping(mapping, quiet=True)
        assert rc == 3, f"Malformed YAML should exit 3, got {rc}"

    def test_non_mapping_top_level_fails_3(
        self, tmp_path: Path, checker
    ) -> None:
        """A filled file that parses but is not a top-level mapping (e.g. a bare
        list) fails structurally -- the loader expects a mapping."""
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text("- tier: high\n- tier: low\n")
        rc = checker.check_mapping(mapping, quiet=True)
        assert rc == 3, f"Non-mapping top level should exit 3, got {rc}"

    def test_malformed_message_is_clean(
        self, tmp_path: Path, checker, capsys
    ) -> None:
        mapping = tmp_path / "model-selection-mapping.yml"
        mapping.write_text("mapping: [unclosed\n")
        rc = checker.main(["--mapping", str(mapping)])
        assert rc == 3
        err = capsys.readouterr().err
        assert "not valid YAML" in err
        assert "Traceback" not in err

    def test_pyyaml_absent_degrades_gracefully(
        self, tmp_path: Path, checker, capsys, monkeypatch
    ) -> None:
        """With PyYAML unavailable, structural validation is skipped (a clean
        note, not a ModuleNotFoundError traceback) and the sentinel-only result
        stands -- the gate never crashes a dependency-bare CI."""
        real_import = builtins.__import__

        def _no_yaml(name, *args, **kwargs):
            if name == "yaml":
                raise ImportError("simulated: PyYAML not installed")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", _no_yaml)

        mapping = tmp_path / "model-selection-mapping.yml"
        # A filled mapping that is ALSO malformed YAML: with PyYAML absent the
        # structural check is skipped, so this still PASSES (sentinel-only) --
        # proving the dependency is genuinely optional, not silently enforced.
        mapping.write_text("mapping: [unclosed\n  - tier: high\n")
        rc = checker.check_mapping(mapping, quiet=False)
        assert rc == 0, "PyYAML-absent must degrade to sentinel-only pass"
        err = capsys.readouterr().err
        assert "structural validation skipped" in err
        assert "PyYAML not installed" in err


# ---------------------------------------------------------------------------
# Interactive capture (foldback #2): fill the stub at install so the gate ships
# green; non-interactive / CI keeps the FILL ME stub fallback.
# ---------------------------------------------------------------------------

def _seed_stub(target: Path) -> Path:
    """Seed the FILL-ME stub at its install destination under *target*."""
    mapping = target / "dev" / ".cairn" / "model-selection-mapping.yml"
    mapping.parent.mkdir(parents=True, exist_ok=True)
    mapping.write_text(_STUB_SRC.read_text(encoding="utf-8"), encoding="utf-8")
    return mapping


class TestInteractiveCapture:
    def test_capture_fills_stub_and_greens_gate(self, tmp_path: Path) -> None:
        checker = _load_checker()
        mapping = _seed_stub(tmp_path)
        # high tier filled; medium + low skipped (blank model).
        answers = iter(["vendor-a/flagship", "2025-06-01", "strategy",
                        "bench Jun 2025", "", ""])
        wrote = capture_model_selection_mapping(
            tmp_path, prompt=lambda _p: next(answers), interactive=True,
            today="2025-06-12")
        assert wrote is True
        assert "FILL ME" not in mapping.read_text()
        assert checker.check_mapping(mapping, quiet=True) == 0, (
            "captured mapping must pass the fidelity gate (green)"
        )

    def test_non_interactive_keeps_stub(self, tmp_path: Path) -> None:
        mapping = _seed_stub(tmp_path)
        assert capture_model_selection_mapping(
            tmp_path, interactive=False) is False
        assert "FILL ME" in mapping.read_text(), "non-interactive must keep stub"

    def test_idempotent_on_already_filled(self, tmp_path: Path) -> None:
        mapping = _seed_stub(tmp_path)
        answers = iter(["vendor/x", "2025-01-01", "general", "src", "", ""])
        assert capture_model_selection_mapping(
            tmp_path, prompt=lambda _p: next(answers), interactive=True) is True
        before = mapping.read_text()
        # Second run sees no FILL ME -> no-op, never clobbers a real mapping.
        assert capture_model_selection_mapping(
            tmp_path, prompt=lambda _p: "unused", interactive=True) is False
        assert mapping.read_text() == before

    def test_skip_every_tier_keeps_stub(self, tmp_path: Path) -> None:
        mapping = _seed_stub(tmp_path)
        assert capture_model_selection_mapping(
            tmp_path, prompt=lambda _p: "", interactive=True) is False
        assert "FILL ME" in mapping.read_text()

    def test_missing_stub_is_noop(self, tmp_path: Path) -> None:
        # No stub seeded -- capture must no-op (never create one from nothing).
        assert capture_model_selection_mapping(
            tmp_path, prompt=lambda _p: "x", interactive=True) is False

    def test_special_chars_quoted_and_valid(self, tmp_path: Path) -> None:
        """A model / source carrying YAML-special characters (':') is
        double-quoted, so the written mapping still parses + passes the
        structural gate."""
        checker = _load_checker()
        mapping = _seed_stub(tmp_path)
        answers = iter(["vendor:flagship-v2", "2025-06-01", "strategy: review",
                        "price: $15/1M", "", ""])
        wrote = capture_model_selection_mapping(
            tmp_path, prompt=lambda _p: next(answers), interactive=True,
            today="2025-06-12")
        assert wrote is True
        assert checker.check_mapping(mapping, quiet=True) == 0

    def test_full_noninteractive_scaffold_keeps_stub(self, tmp_path: Path) -> None:
        """The CLI wiring: a full scaffold install in a non-TTY test run leaves
        the FILL ME stub (the gate then flags it)."""
        assert _scaffold(tmp_path) == 0
        mapping = tmp_path / "dev" / ".cairn" / "model-selection-mapping.yml"
        assert mapping.is_file() and "FILL ME" in mapping.read_text()


class TestNoticeOnEveryInstallPath:
    def test_missing_filled_and_stub(self, tmp_path: Path, capsys) -> None:
        assert model_selection_notice_lines(tmp_path) == []
        mapping = _seed_stub(tmp_path)
        notice = "\n".join(model_selection_notice_lines(tmp_path))
        assert "NOTE (model-selection)" in notice
        assert "Name the family, never a version" in notice
        mapping.write_text("mapping:\n  - tier: high\n    model: vendor/family\n")
        assert model_selection_notice_lines(tmp_path) == []

    def test_noninteractive_install_prints_notice(self, tmp_path: Path, capsys) -> None:
        assert _scaffold(tmp_path) == 0
        assert "NOTE (model-selection)" in capsys.readouterr().out

    def test_plan_stage_and_apply_print_after_success(self, tmp_path: Path, capsys) -> None:
        assert _scaffold(tmp_path) == 0
        capsys.readouterr()
        base = ["upgrade", "--target", str(tmp_path),
                "--cairn-root", str(CAIRN_ROOT)]
        for action in ("--plan", "--stage", "--apply"):
            assert scaffold_main(base + [action]) == 0
            out = capsys.readouterr().out
            assert "NOTE (model-selection)" in out, action
            assert out.rstrip().endswith("Mapping-record schema\"."), action

    def test_other_module_does_not_print_notice(self, tmp_path: Path, capsys) -> None:
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: Demo\ntest_command: pytest\npreset: solo-greenfield\n",
            encoding="utf-8",
        )
        assert scaffold_main([
            "--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
        ]) == 0
        assert "NOTE (model-selection)" not in capsys.readouterr().out
        assert scaffold_main([
            "upgrade", "--target", str(tmp_path), "--cairn-root",
            str(CAIRN_ROOT), "--plan",
        ]) == 0
        assert "NOTE (model-selection)" not in capsys.readouterr().out

    def test_refused_apply_prints_no_notice(self, tmp_path: Path, capsys) -> None:
        assert _scaffold(tmp_path) == 0
        capsys.readouterr()
        assert scaffold_main([
            "upgrade", "--target", str(tmp_path), "--cairn-root",
            str(CAIRN_ROOT), "--apply",
        ]) != 0
        assert "NOTE (model-selection)" not in capsys.readouterr().out

    def test_adopting_mapping_module_prints_notice(self, tmp_path: Path, capsys) -> None:
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: Demo\ntest_command: pytest\npreset: solo-greenfield\n",
            encoding="utf-8",
        )
        assert scaffold_main([
            "--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
        ]) == 0
        capsys.readouterr()
        assert scaffold_main([
            "upgrade", "--target", str(tmp_path), "--cairn-root",
            str(CAIRN_ROOT), "--adopt-module", "model-selection",
        ]) == 0
        out = capsys.readouterr().out
        assert "Adopted module 'model-selection'" in out
        assert "NOTE (model-selection)" in out


class TestNoticeTextIgnoresFileContent:
    def test_unfilled_content_is_not_echoed(self, tmp_path: Path) -> None:
        mapping = _seed_stub(tmp_path)
        first = model_selection_notice_lines(tmp_path)
        mapping.write_text("mapping:\n  - tier: high\n    model: FILL ME\x1b\x07\n")
        assert model_selection_notice_lines(tmp_path) == first

    def test_unreadable_shapes_have_one_fixed_text(self, tmp_path: Path) -> None:
        mapping = _seed_stub(tmp_path)
        mapping.write_bytes(b"\xff")
        unreadable = model_selection_notice_lines(tmp_path)
        assert "could not read" in unreadable[0]
        mapping.unlink()
        mapping.symlink_to(tmp_path / "distinctive-target")
        assert model_selection_notice_lines(tmp_path) == unreadable
        mapping.unlink()
        mapping.mkdir()
        assert model_selection_notice_lines(tmp_path) == unreadable


class TestCaptureWritesByReplacing:
    def test_hardlinked_mapping_does_not_change_other_name(self, tmp_path: Path) -> None:
        mapping = _seed_stub(tmp_path)
        victim = tmp_path / "other-name"
        os.link(mapping, victim)
        before = victim.read_bytes()
        answers = iter(["vendor/family", "", "", "", "", ""])
        assert capture_model_selection_mapping(
            tmp_path, prompt=lambda _: next(answers), today="2026-01-01"
        )
        assert victim.read_bytes() == before
        assert mapping.stat().st_nlink == 1

    def test_linked_mapping_refused_before_prompt(self, tmp_path: Path, capsys) -> None:
        mapping = _seed_stub(tmp_path)
        victim = tmp_path / "victim"
        victim.write_bytes(mapping.read_bytes())
        mapping.unlink()
        mapping.symlink_to(victim)
        with pytest.raises(ScaffoldSecurityError):
            capture_model_selection_mapping(
                tmp_path, prompt=lambda _: pytest.fail("prompt reached")
            )
        assert capsys.readouterr().out == ""
        assert b"FILL ME" in victim.read_bytes()

    def test_link_swapped_during_answers_refused(self, tmp_path: Path) -> None:
        mapping = _seed_stub(tmp_path)
        victim = tmp_path / "victim"
        victim.write_bytes(b"outside")
        def swap(_prompt: str) -> str:
            mapping.unlink()
            mapping.symlink_to(victim)
            return "vendor/family"
        with pytest.raises(ScaffoldSecurityError):
            capture_model_selection_mapping(tmp_path, prompt=swap)
        assert victim.read_bytes() == b"outside"

    def test_real_interactive_install_refuses_link_without_leaking_target(
        self, tmp_path: Path, monkeypatch, capsys
    ) -> None:
        from bootstrap._scaffold import cli

        class Terminal(io.StringIO):
            def isatty(self) -> bool:
                return True

        monkeypatch.setattr(cli.sys, "stdin", Terminal())
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: Demo\ntest_command: pytest\nmodules:\n"
            "  - model-selection\n", encoding="utf-8"
        )
        mapping = tmp_path / "dev/.cairn/model-selection-mapping.yml"
        mapping.parent.mkdir(parents=True)
        victim = tmp_path / "distinctive-outside-file"
        victim.write_bytes(_STUB_SRC.read_bytes())
        mapping.symlink_to(victim)
        before = victim.read_bytes()
        assert scaffold_main([
            "--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
        ]) == 2
        captured = capsys.readouterr()
        assert "error: model-selection capture refused (containment)" in captured.err
        assert "Replace it with a regular file" in captured.err
        assert "distinctive-outside-file" not in captured.err
        assert victim.read_bytes() == before
        assert not (tmp_path / "dev/.cairn/cairn-lock.yml").exists()
