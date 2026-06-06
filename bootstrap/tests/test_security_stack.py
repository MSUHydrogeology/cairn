"""Security-apparatus-enrichment -- Chunk B0: the selected-module required-token
preflight.

A module may declare inline tokens that have no safe default (the first is
``python-security``'s ``{{python_package}}``).  Selecting such a module without
a filled value must **fail closed before any write** -- no target-tree files, no
lockfile / module-state mutation -- on all three install paths: a fresh install,
``upgrade --adopt-module``, and the writing ``upgrade`` paths (``--stage`` /
``--apply``).  The read-only ``upgrade --plan`` stays available so an adopter can
diagnose the gap.

Contracts pinned here (Codex External plan review P1 #1; the sharpening's
Chunk B0 + the SR follow-ins):

* ``missing_required_tokens`` flags absent / empty / placeholder-valued required
  tokens and only for *selected* modules (pure, side-effect-free).
* fresh install / dry-run refuse (exit 2) and write nothing when a selected
  module's required token is unfilled; they succeed once it is supplied.
* ``adopt-module`` refuses (exit 2) and leaves the lockfile + tree untouched.
* the writing upgrade paths refuse (exit 2); ``--plan`` still returns 0.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_security_stack.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap import scaffold as s  # noqa: E402
from bootstrap._scaffold.config import (  # noqa: E402
    _MODULE_REQUIRED_TOKENS,
    missing_required_tokens,
)
from bootstrap._scaffold.lockfile import _LOCKFILE_REL, _emit_lock_yaml  # noqa: E402

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)

#: A real module that declares a required token (python-security -> python_package);
#: B0 lands this stub module so the gate is exercised end-to-end against a real
#: registration, not a synthetic monkeypatch.
_REQ_MODULE = "python-security"
_REQ_TOKEN = "python_package"


# ---------------------------------------------------------------------------
# The stub registration is real
# ---------------------------------------------------------------------------

def test_python_security_declares_its_required_token():
    assert _MODULE_REQUIRED_TOKENS.get(_REQ_MODULE) == (_REQ_TOKEN,)
    assert _REQ_TOKEN in s.KNOWN_TOKENS
    assert _REQ_MODULE in s._MODULE_MAPPINGS


# ---------------------------------------------------------------------------
# missing_required_tokens -- the pure check
# ---------------------------------------------------------------------------

class TestMissingRequiredTokens:
    def test_absent_is_flagged(self):
        assert missing_required_tokens([_REQ_MODULE], {}) == [
            (_REQ_MODULE, _REQ_TOKEN)
        ]

    def test_empty_or_whitespace_is_flagged(self):
        assert missing_required_tokens([_REQ_MODULE], {_REQ_TOKEN: ""})
        assert missing_required_tokens([_REQ_MODULE], {_REQ_TOKEN: "   "})

    def test_unfilled_placeholder_value_is_flagged(self):
        # A token resolved to another {{token}} is as unfilled as an absent one.
        assert missing_required_tokens(
            [_REQ_MODULE], {_REQ_TOKEN: "{{python_package}}"}
        ) == [(_REQ_MODULE, _REQ_TOKEN)]

    def test_filled_value_passes(self):
        assert missing_required_tokens([_REQ_MODULE], {_REQ_TOKEN: "mypkg"}) == []

    def test_module_without_required_tokens_passes(self):
        assert missing_required_tokens(["claim-check"], {}) == []

    def test_only_selected_modules_are_checked(self):
        # python-security NOT selected -> its requirement does not apply.
        assert missing_required_tokens(["claim-check", "reflections"], {}) == []

    def test_is_pure_no_filesystem(self, tmp_path):
        before = sorted(tmp_path.iterdir())
        missing_required_tokens([_REQ_MODULE], {})
        assert sorted(tmp_path.iterdir()) == before


# ---------------------------------------------------------------------------
# Fresh install -- fail closed before any write
# ---------------------------------------------------------------------------

def _profile(target: Path, *, with_token: bool) -> Path:
    cfg = target / "profile.yml"
    lines = ["project_name: T", "test_command: pytest"]
    if with_token:
        lines.append(f"{_REQ_TOKEN}: mypkg")
    lines += ["modules:", f"  - {_REQ_MODULE}"]
    cfg.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return cfg


def _install_args(cfg: Path, target: Path, *extra: str) -> list[str]:
    return [
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev", *extra,
    ]


class TestFreshInstallPreflight:
    def test_missing_token_refuses_and_writes_nothing(self, tmp_path):
        cfg = _profile(tmp_path, with_token=False)
        rc = s.main(_install_args(cfg, tmp_path))
        assert rc == 2
        # Zero mutation: no dev tree, no lockfile, no module doc.
        assert not (tmp_path / "dev").exists()
        assert not (tmp_path / _LOCKFILE_REL).exists()
        assert not (tmp_path / "dev" / "modules" / "python-security.md").exists()
        # Only the profile we wrote is present.
        assert sorted(p.name for p in tmp_path.iterdir()) == ["profile.yml"]

    def test_dry_run_missing_token_also_refuses(self, tmp_path):
        cfg = _profile(tmp_path, with_token=False)
        rc = s.main(_install_args(cfg, tmp_path, "--dry-run"))
        assert rc == 2
        assert not (tmp_path / "dev").exists()

    def test_filled_token_installs(self, tmp_path):
        cfg = _profile(tmp_path, with_token=True)
        rc = s.main(_install_args(cfg, tmp_path))
        assert rc == 0
        assert (tmp_path / "dev" / "modules" / "python-security.md").is_file()
        lock = s.read_lockfile(tmp_path)
        assert lock is not None and _REQ_MODULE in lock.get("modules", [])


# ---------------------------------------------------------------------------
# upgrade --adopt-module -- fail closed, lockfile untouched
# ---------------------------------------------------------------------------

def test_adopt_module_missing_token_refuses_and_leaves_lockfile(tmp_path):
    # A normal install (no python-security); its lockfile has no python_package.
    cfg = tmp_path / "profile.yml"
    cfg.write_text(
        "project_name: T\ntest_command: pytest\npreset: solo-greenfield\n",
        encoding="utf-8",
    )
    assert s.main(_install_args(cfg, tmp_path)) == 0
    before = sorted(s.read_lockfile(tmp_path).get("modules", []))

    rc = s.main([
        "upgrade", "--target", str(tmp_path),
        "--adopt-module", _REQ_MODULE, "--cairn-root", str(CAIRN_ROOT),
    ])
    assert rc == 2
    after = sorted(s.read_lockfile(tmp_path).get("modules", []))
    assert after == before  # lockfile roster unchanged
    assert _REQ_MODULE not in after
    assert not (tmp_path / "dev" / "modules" / "python-security.md").exists()


# ---------------------------------------------------------------------------
# Writing upgrade paths -- fail closed; --plan stays available
# ---------------------------------------------------------------------------

def _tamper_drop_token(target: Path) -> None:
    """Drop python_package from a lockfile that records python-security --
    simulating drift/tamper that leaves an installed module's required token
    unfilled."""
    lock = s.read_lockfile(target)
    lock["tokens"].pop(_REQ_TOKEN, None)
    (target / _LOCKFILE_REL).write_text(_emit_lock_yaml(lock), encoding="utf-8")


@pytest.fixture()
def _tampered_tree(tmp_path):
    cfg = _profile(tmp_path, with_token=True)
    assert s.main(_install_args(cfg, tmp_path)) == 0
    _tamper_drop_token(tmp_path)
    return tmp_path


class TestUpgradePreflight:
    def test_plan_is_read_only_and_still_runs(self, _tampered_tree):
        rc = s.main([
            "upgrade", "--target", str(_tampered_tree), "--plan",
            "--cairn-root", str(CAIRN_ROOT),
        ])
        assert rc == 0

    def test_stage_refuses(self, _tampered_tree):
        rc = s.main([
            "upgrade", "--target", str(_tampered_tree), "--stage",
            "--cairn-root", str(CAIRN_ROOT),
        ])
        assert rc == 2

    def test_apply_refuses(self, _tampered_tree):
        rc = s.main([
            "upgrade", "--target", str(_tampered_tree), "--apply",
            "--cairn-root", str(CAIRN_ROOT),
        ])
        assert rc == 2


# ---------------------------------------------------------------------------
# Chunk A -- security-review doctrine: generalized injection-review procedure
# (S1/IR-B) + the v1 self-audit trust-model statement.  A doctrine-presence
# contract so the load-bearing wording cannot silently regress, and a
# generalization guard so the modflow_tools-specific tool names do not leak up.
# ---------------------------------------------------------------------------

class TestSecurityReviewDoctrine:
    _DOC = TEMPLATES_ROOT / "modules" / "team-gated" / "security-review.md"

    def _text(self) -> str:
        return self._DOC.read_text(encoding="utf-8")

    def test_injection_review_by_class_procedure_present(self):
        text = self._text()
        assert "Injection-review procedure — review by input class" in text
        # the load-bearing triage + the generalized, tool-agnostic input classes
        assert "trusted-input" in text and "user-controlled" in text
        for klass in (
            "Pickled state stores",
            "External simulator",
            "Data-fetch network calls",
        ):
            assert klass in text, f"missing generalized input class: {klass!r}"

    def test_v1_self_audit_scope_statement_present(self):
        text = self._text()
        assert "self-audit" in text
        # the Critical #1 operational guard, adopter-facing (not just a claim)
        assert "do not wire the audit stack into untrusted-PR / fork CI" in text.lower() \
            or "do not wire the audit stack into untrusted-pr / fork ci" in text.lower()
        assert "tripwire, not a proof" in text

    def test_no_modflow_tools_specific_tool_names_leaked(self):
        # The generalization is the whole point (S1/IR-B): the FloPy / PEST++ /
        # GDAL / nwisweb specifics stay modflow_tools-local, never folded up.
        text = self._text()
        for leaked in ("FloPy", "PEST++", "pestpp", "nwisweb", "GDAL", "rasterio",
                       "ModelStateStore"):
            assert leaked not in text, f"tool-specific name leaked into Cairn doctrine: {leaked!r}"
