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

import builtins
import importlib.util
import os
import shutil
import subprocess
import sys
import time
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


# ---------------------------------------------------------------------------
# Chunk B -- content-security: the atomic stdlib-only injection apparatus.
# The content_scan_runner contract: audited-roots manifest (P1 #2), per-file
# symlink/special-file containment (Imp #3), resource budgets (Imp #4), the
# 0/1/2/3 exit contract, multiset NEW/STALE, sentinel/version validation,
# RV4 host-still-flagged, RV5 narrow homoglyph allowance, tripwire output.
# ---------------------------------------------------------------------------

_TEAM_GATED = TEMPLATES_ROOT / "modules" / "team-gated"
_RUNNER_SRC = _TEAM_GATED / "content_scan_runner.py"
_SCAN_SRC = _TEAM_GATED / "content_scan.py"

_HAS_GIT = shutil.which("git") is not None
#: Bandit availability -- real-tool tests gate on this so Cairn's base suite
#: never silently requires Bandit (re-review P2 #1).
_HAS_BANDIT = (shutil.which("bandit") is not None
               or importlib.util.find_spec("bandit") is not None)
#: pip-audit availability. Cairn does NOT install it (adopter dependency,
#: DEPENDENCY_BUDGET Exception 1), so the end-to-end expectation is derived
#: from presence rather than assumed -- an absent required tool is DEGRADED.
_HAS_PIP_AUDIT = (shutil.which("pip-audit") is not None
                  or importlib.util.find_spec("pip_audit") is not None)


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def csr():
    return _load("content_scan_runner", _RUNNER_SRC)


@pytest.fixture(scope="module")
def cscan():
    return _load("content_scan", _SCAN_SRC)


def _git_repo(root: Path) -> None:
    subprocess.run(["git", "-C", str(root), "init", "-q", "-b", "main"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "t@t.t"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "t"], check=True)


def _git_commit_all(root: Path) -> None:
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "x"], check=True,
                   capture_output=True)


def _read_lock(root: Path) -> dict:
    """Parse an installed adopter lockfile (JSON after its comment header)."""
    import json
    text = (root / "dev" / ".cairn" / "cairn-lock.yml").read_text(encoding="utf-8")
    return json.loads(text[text.find("{"):])


def _seed_apparatus(root: Path) -> None:
    """A minimal scanned repo: the apparatus under scripts/, a manifest naming
    dev/, a sentinel-bearing empty baseline, and one tracked dev/*.md file."""
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "dev").mkdir(parents=True, exist_ok=True)
    shutil.copy(_SCAN_SRC, root / "scripts" / "content_scan.py")
    shutil.copy(_TEAM_GATED / "content_scan_allowlist.txt",
                root / "scripts" / "content_scan_allowlist.txt")
    (root / "scripts" / "content_scan_roots.txt").write_text(
        "# content-scan-roots v1\ndev\n", encoding="utf-8")
    (root / "scripts" / "content_scan_residuals.txt").write_text(
        "# content-scan-residual-baseline v1\n", encoding="utf-8")
    (root / "dev" / "doc.md").write_text("# A clean doc\n", encoding="utf-8")


class TestAuditRootsManifest:
    def test_valid_roots_parse(self, csr, tmp_path):
        # P1 #5: load_audit_roots returns (rel, required) tuples; `!` => required.
        m = tmp_path / "roots.txt"
        m.write_text("# content-scan-roots v1\n!dev\ndocs\n", encoding="utf-8")
        assert csr.load_audit_roots(m, tmp_path) == [("dev", True), ("docs", False)]

    def test_escape_dotdot_refused(self, csr, tmp_path):
        m = tmp_path / "roots.txt"
        m.write_text("# content-scan-roots v1\n../outside\n", encoding="utf-8")
        with pytest.raises(csr.AuditError):
            csr.load_audit_roots(m, tmp_path)

    def test_absolute_path_refused(self, csr, tmp_path):
        m = tmp_path / "roots.txt"
        m.write_text("# content-scan-roots v1\n/etc\n", encoding="utf-8")
        with pytest.raises(csr.AuditError):
            csr.load_audit_roots(m, tmp_path)

    def test_missing_sentinel_refused(self, csr, tmp_path):
        m = tmp_path / "roots.txt"
        m.write_text("dev\n", encoding="utf-8")
        with pytest.raises(csr.AuditError):
            csr.load_audit_roots(m, tmp_path)

    def test_empty_roots_refused(self, csr, tmp_path):
        m = tmp_path / "roots.txt"
        m.write_text("# content-scan-roots v1\n", encoding="utf-8")
        with pytest.raises(csr.AuditError):
            csr.load_audit_roots(m, tmp_path)

    def test_missing_manifest_refused(self, csr, tmp_path):
        with pytest.raises(csr.AuditError):
            csr.load_audit_roots(tmp_path / "nope.txt", tmp_path)


class TestResidualBaselineSentinel:
    def test_v1_empty_sentinel_ok(self, csr, tmp_path):
        b = tmp_path / "res.txt"
        b.write_text("# content-scan-residual-baseline v1\n", encoding="utf-8")
        ok, counts, _why = csr.load_residual_baseline_checked(b)
        assert ok and len(counts) == 0

    def test_unsupported_version_refused(self, csr, tmp_path):
        b = tmp_path / "res.txt"
        b.write_text("# content-scan-residual-baseline v2\n", encoding="utf-8")
        ok, _c, why = csr.load_residual_baseline_checked(b)
        assert not ok and "unsupported" in why

    def test_zero_byte_refused(self, csr, tmp_path):
        b = tmp_path / "res.txt"
        b.write_text("", encoding="utf-8")
        ok, _c, _why = csr.load_residual_baseline_checked(b)
        assert not ok

    def test_missing_refused(self, csr, tmp_path):
        ok, _c, _why = csr.load_residual_baseline_checked(tmp_path / "nope.txt")
        assert not ok


class TestHomoglyphAllowanceRV5:
    def test_scientific_units_cleared(self, cscan):
        assert cscan._is_scientific_unit("µs")      # MICRO SIGN + s
        assert cscan._is_scientific_unit("μmol")    # GREEK MU + mol
        assert cscan._is_scientific_unit("kΩ")      # k + OMEGA

    def test_credential_homoglyph_still_flags(self, cscan):
        # Latin + Cyrillic spoof ('pаypal' has a Cyrillic 'а') is NOT a unit.
        assert not cscan._is_scientific_unit("pаypal")
        # an over-long micro-prefixed token is not a unit either.
        assert not cscan._is_scientific_unit("µsecretword")

    def test_unit_not_flagged_credential_flagged_in_scan(self, cscan):
        flags = list(cscan.scan_text("a µs reading and a pаypal token\n"))
        homoglyph = [f for f in flags if f.pattern_id == "homoglyph"]
        # Exactly one homoglyph flag (the Cyrillic-spoofed credential), and the
        # µs scientific unit is NOT among the flagged tokens (RV5 cleared it).
        assert len(homoglyph) == 1
        assert "ypal" in homoglyph[0].message  # the credential token (Latin tail)
        assert not any("µs" in f.message for f in homoglyph)


@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
class TestRunnerExitContract:
    def _run(self, csr, root):
        return csr.audit(
            root,
            root / "scripts" / "content_scan_roots.txt",
            root / "scripts" / "content_scan_residuals.txt",
        )

    def test_clean_is_zero(self, csr, tmp_path):
        _git_repo(tmp_path); _seed_apparatus(tmp_path); _git_commit_all(tmp_path)
        code, files, *_ = self._run(csr, tmp_path)
        assert code == 0
        # P1 #2: the manifest itself is in the audited set.
        rels = {str(p.relative_to(tmp_path)) for p in files}
        assert "scripts/content_scan_roots.txt" in rels

    def test_finding_is_advisory_one(self, csr, tmp_path):
        _git_repo(tmp_path); _seed_apparatus(tmp_path)
        (tmp_path / "dev" / "bad.md").write_text(
            "token pаypal\n", encoding="utf-8")
        _git_commit_all(tmp_path)
        code, _files, all_flags, new_flags, _stale = self._run(csr, tmp_path)
        assert code == 1 and new_flags

    def test_empty_set_is_failure_two(self, csr, tmp_path):
        # A manifest root with no tracked text -> zero files -> exit 2.
        _git_repo(tmp_path)
        (tmp_path / "scripts").mkdir()
        shutil.copy(_SCAN_SRC, tmp_path / "scripts" / "content_scan.py")
        (tmp_path / "scripts" / "content_scan_roots.txt").write_text(
            "# content-scan-roots v1\ndocs\n", encoding="utf-8")  # docs/ absent
        (tmp_path / "scripts" / "content_scan_residuals.txt").write_text(
            "# content-scan-residual-baseline v1\n", encoding="utf-8")
        _git_commit_all(tmp_path)
        code, *_ = self._run(csr, tmp_path)
        assert code == 2

    def test_symlink_is_refused_two(self, csr, tmp_path):
        _git_repo(tmp_path); _seed_apparatus(tmp_path)
        outside = tmp_path.parent / "secret.txt"
        outside.write_text("secret\n", encoding="utf-8")
        (tmp_path / "dev" / "evil.md").symlink_to(outside)
        _git_commit_all(tmp_path)
        code, *_ = self._run(csr, tmp_path)
        assert code == 2

    def test_per_file_budget_is_refused_two(self, csr, tmp_path, monkeypatch):
        _git_repo(tmp_path); _seed_apparatus(tmp_path)
        (tmp_path / "dev" / "big.md").write_text("x" * 4096, encoding="utf-8")
        _git_commit_all(tmp_path)
        monkeypatch.setattr(csr, "_MAX_FILE_BYTES", 1024)
        code, *_ = self._run(csr, tmp_path)
        assert code == 2

    def test_stale_baseline_is_three(self, csr, tmp_path):
        _git_repo(tmp_path); _seed_apparatus(tmp_path)
        # A reviewed entry for content that does not exist -> STALE -> exit 3.
        (tmp_path / "scripts" / "content_scan_residuals.txt").write_text(
            "# content-scan-residual-baseline v1\n"
            "dev/gone.md:homoglyph:0123456789ab  # [sci-unit] not present\n",
            encoding="utf-8")
        _git_commit_all(tmp_path)
        code, _files, _all, _new, stale = self._run(csr, tmp_path)
        assert code == 3 and stale

    def test_rv4_multitenant_host_still_flags(self, csr, tmp_path):
        _git_repo(tmp_path); _seed_apparatus(tmp_path)
        # A multi-tenant code host is NOT allowlisted -> stays a finding.
        (tmp_path / "dev" / "urls.md").write_text(
            "see https://github.com/evil/x for details\n", encoding="utf-8")
        _git_commit_all(tmp_path)
        code, _files, all_flags, _new, _stale = self._run(csr, tmp_path)
        assert code == 1
        assert any(fl.pattern_id == "suspicious-url" for _r, fl, _fp in all_flags)

    def test_missing_required_root_fails_even_with_a_healthy_root(self, csr, tmp_path):
        # P1 #5: a manifest with a required root that is absent must FAIL even
        # when an optional/healthy root contributes files (a missing required
        # root silently shrinks coverage otherwise).
        _git_repo(tmp_path); _seed_apparatus(tmp_path)
        (tmp_path / "scripts" / "content_scan_roots.txt").write_text(
            "# content-scan-roots v1\ndev\n!MISSING_REQUIRED.md\n",
            encoding="utf-8")
        _git_commit_all(tmp_path)
        code, *_ = self._run(csr, tmp_path)
        assert code == 2

    def test_required_root_present_passes(self, csr, tmp_path):
        # The healthy counterpart: a required root that exists + contributes.
        _git_repo(tmp_path); _seed_apparatus(tmp_path)
        (tmp_path / "scripts" / "content_scan_roots.txt").write_text(
            "# content-scan-roots v1\n!dev\n", encoding="utf-8")
        _git_commit_all(tmp_path)
        code, *_ = self._run(csr, tmp_path)
        assert code == 0

    def test_wall_clock_overrun_fails_closed(self, csr, tmp_path):
        # P2 #6: an exceeded wall-clock deadline fails closed (exit 2) -- a
        # partial / overrun scan must never read clean.
        import time  # noqa: PLC0415
        _git_repo(tmp_path); _seed_apparatus(tmp_path); _git_commit_all(tmp_path)
        files = csr.audited_text_files(
            tmp_path, tmp_path / "scripts" / "content_scan_roots.txt")
        code, *_ = csr.run_content_scan(
            files, tmp_path,
            tmp_path / "scripts" / "content_scan_residuals.txt",
            deadline=time.monotonic() - 1.0)
        assert code == 2


# ---------------------------------------------------------------------------
# Chunk C -- python-security: the orchestrator (run_security_audit.py).
# SR-1 integrity preflight, P1 #4 authoritative installed-state, P2 #5
# single-package validation, Crit #2/SR-3 trusted subprocess boundary, Imp #5
# egress-off-by-default, the P1 #3 distinct-space exit table.
# ---------------------------------------------------------------------------

_ORCH_SRC = _TEAM_GATED / "run_security_audit.py"


@pytest.fixture(scope="module")
def orch():
    return _load("run_security_audit", _ORCH_SRC)


def _install_modules(target: Path, modules: list[str], *, python_package: str | None):
    cfg = target / "profile.yml"
    lines = ["project_name: T", "test_command: pytest"]
    if python_package is not None:
        lines.append(f"python_package: {python_package}")
    lines += ["modules:"] + [f"  - {m}" for m in modules]
    cfg.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return s.main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ])


@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
class TestOrchestrator:
    def _adopter(self, tmp_path) -> tuple[Path, dict]:
        _git_repo(tmp_path)
        (tmp_path / "mypkg").mkdir()
        (tmp_path / "mypkg" / "__init__.py").write_text("x = 1\n", encoding="utf-8")
        rc = _install_modules(tmp_path, ["content-security", "python-security"],
                              python_package="mypkg")
        assert rc == 0
        _git_commit_all(tmp_path)
        return tmp_path, _read_lock(tmp_path)

    def test_load_lockfile_parses_json_with_comment_header(self, orch, tmp_path):
        root, _ = self._adopter(tmp_path)
        lock = orch.load_lockfile(root / "dev" / ".cairn" / "cairn-lock.yml")
        assert "files" in lock and "python-security" in lock.get("modules", [])

    def test_integrity_preflight_ok_then_tamper_fails(self, orch, tmp_path):
        root, lock = self._adopter(tmp_path)
        orch.integrity_preflight(root, lock)  # clean -> no raise
        # Tamper a recorded apparatus file -> fail closed.
        (root / "scripts" / "content_scan.py").write_text("x=1\n", encoding="utf-8")
        with pytest.raises(orch.AuditDegraded):
            orch.integrity_preflight(root, lock)

    def test_python_package_validation(self, orch, tmp_path):
        root, lock = self._adopter(tmp_path)
        assert orch.validate_python_package(root, lock).name == "mypkg"
        # repo root '.' refused
        with pytest.raises(orch.AuditDegraded):
            orch.validate_python_package(root, {"tokens": {"python_package": "."}})
        # absent dir refused
        with pytest.raises(orch.AuditDegraded):
            orch.validate_python_package(root, {"tokens": {"python_package": "nope"}})
        # escape refused
        with pytest.raises(orch.AuditDegraded):
            orch.validate_python_package(root, {"tokens": {"python_package": "../x"}})
        # unfilled refused
        with pytest.raises(orch.AuditDegraded):
            orch.validate_python_package(root, {"tokens": {}})

    def test_safe_target_args_blocks_option_shaped(self, orch, tmp_path):
        # SR-3: a path whose name starts with '-' is refused (argv injection);
        # a normal path is prefixed with the '--' terminator.
        ok = orch._safe_target_args([tmp_path / "pkg"])
        assert ok[0] == "--"
        with pytest.raises(orch.AuditDegraded):
            orch._safe_target_args([tmp_path / "--evil"])

    def test_injection_not_applicable_is_incomplete_not_clean(self, orch, tmp_path):
        # P1 #3 / SR-4: content-security not installed -> injection NOT
        # APPLICABLE -> a DISTINCT incomplete tier, never a clean contribution.
        _git_repo(tmp_path)
        (tmp_path / "mypkg").mkdir()
        (tmp_path / "mypkg" / "__init__.py").write_text("x=1\n", encoding="utf-8")
        assert _install_modules(tmp_path, ["python-security"],
                                python_package="mypkg") == 0
        _git_commit_all(tmp_path)
        lock = _read_lock(tmp_path)
        status, tier = orch.run_injection_pass(tmp_path, lock)
        assert status == "not-applicable"
        assert tier == orch._AGG_INCOMPLETE and tier != orch._AGG_CLEAN

    def test_adopted_executable_gate_detects_tamper(self, orch, tmp_path):
        root, lock = self._adopter(tmp_path)
        # tamper a NON-apparatus adopted .py (tools/lifecycle.py) -> the source
        # gate flags it (the apparatus subset is caught by the preflight).
        lifecycle = root / "tools" / "lifecycle.py"
        assert lifecycle.is_file()
        lifecycle.write_text(lifecycle.read_text(encoding="utf-8") + "\n# x\n",
                             encoding="utf-8")
        status, tier = orch.run_adopted_executable_gate(root, lock)
        assert tier == orch._AGG_DEGRADED and "tamper" in status

    def test_pip_audit_egress_off_is_incomplete_not_clean(self, orch, tmp_path,
                                                          monkeypatch):
        # C-t2 (re-expression of the original egress-off contract). P1 #3 /
        # SR-5: egress off with the tool PRESENT -> the lookup did not run ->
        # UNAVAILABLE -> incomplete, never a clean contribution. The tool is
        # forced present so this pins the egress limb alone; the tool-absent
        # limb is C-t3's, and on a machine without pip-audit the unforced call
        # is now DEGRADED (an absent required tool dominates).
        root, _ = self._adopter(tmp_path)
        monkeypatch.setattr(orch.shutil, "which", lambda _n: "/usr/bin/pip-audit")
        status, tier = orch.run_pip_audit_pass(root, allow_egress=False)
        assert "unavailable" in status
        assert tier == orch._AGG_INCOMPLETE and tier != orch._AGG_CLEAN

    def test_pip_audit_tool_error_is_degraded_not_findings(self, orch, tmp_path,
                                                           monkeypatch):
        # P2 #7: only pip-audit exit 1 is a vuln report; any other non-zero
        # (usage / env / network error) is degraded, never reported as findings.
        # Force "tool present" so the classification (not the absent branch) runs.
        monkeypatch.setattr(orch.shutil, "which", lambda _n: "/usr/bin/pip-audit")
        monkeypatch.setattr(orch, "_run_tool",
                            lambda *a, **k: orch.ToolRun(2, "ran", "", ""))
        status, tier = orch.run_pip_audit_pass(tmp_path, allow_egress=True)
        assert tier == orch._AGG_DEGRADED and "error" in status
        monkeypatch.setattr(orch, "_run_tool",
                            lambda *a, **k: orch.ToolRun(1, "ran", "", ""))
        status2, tier2 = orch.run_pip_audit_pass(tmp_path, allow_egress=True)
        assert tier2 == orch._AGG_FINDINGS

    @pytest.mark.skipif(not _HAS_BANDIT,
                        reason="real bandit needed to prove the shadow did not run")
    def test_subprocess_runs_isolated_not_repo_shadow(self, orch, tmp_path):
        # P1 #1: a repo-local bandit/ shadow must NOT execute. _run_tool runs
        # `python -I` from a neutral cwd with a sanitized env, so the shadow is
        # invisible. Assert bandit over a clean pkg is CLEAN despite the shadow.
        root, lock = self._adopter(tmp_path)
        shadow = root / "bandit"
        shadow.mkdir()
        (shadow / "__main__.py").write_text(
            'print("SHADOWED_REPO_BANDIT"); raise SystemExit(0)\n',
            encoding="utf-8")
        pkg = orch.validate_python_package(root, lock)
        status, tier = orch.run_bandit_pass(pkg, root)
        # If the shadow had run, bandit would not have actually scanned -> the
        # real bandit (isolated) runs instead and reports clean over mypkg.
        assert status == "bandit:clean" and tier == orch._AGG_CLEAN

    def test_preflight_requires_complete_apparatus_for_installed_module(self, orch, tmp_path):
        # P1 #2: a lockfile that records python-security + content-security but
        # OMITS the content_scan_runner record, with a tampered unrecorded
        # runner on disk, must FAIL the preflight (not skip the missing record).
        root, lock = self._adopter(tmp_path)
        lock["files"] = [r for r in lock["files"]
                         if r["dst"] != "scripts/content_scan_runner.py"]
        (root / "scripts" / "content_scan_runner.py").write_text(
            "x = 1  # tampered, unrecorded\n", encoding="utf-8")
        with pytest.raises(orch.AuditDegraded):
            orch.integrity_preflight(root, lock)

    def test_end_to_end_clean_then_tamper(self, orch, tmp_path):
        root, _ = self._adopter(tmp_path)
        env = {**__import__("os").environ, "PYTHONPATH": ""}
        r = subprocess.run(
            [sys.executable, "scripts/run_security_audit.py"],
            cwd=str(root), capture_output=True, text=True, env=env)
        # A default both-modules run reports EVERY blocking reason (Chunk C).
        # With bandit AND pip-audit present it is INCOMPLETE (5): egress is off,
        # so the lookup is unavailable. With either tool ABSENT it is DEGRADED
        # (20) -- the shipped exit table already assigns "a required tool was
        # absent" to 20, and the pass no longer returns at the first blocker,
        # so it now reaches that branch. Gate on presence so the base suite
        # never silently requires either tool (P2 #8).
        expected = 5 if (_HAS_BANDIT and _HAS_PIP_AUDIT) else 20
        assert r.returncode == expected, r.stdout + r.stderr
        # Tamper an apparatus file -> preflight DEGRADED (exit 20), no bandit
        # needed (the preflight short-circuits before any pass).
        (root / "scripts" / "content_scan_runner.py").write_text(
            "x=1\n", encoding="utf-8")
        r2 = subprocess.run(
            [sys.executable, "scripts/run_security_audit.py"],
            cwd=str(root), capture_output=True, text=True, env=env)
        assert r2.returncode == 20, r2.stdout + r2.stderr


# ---------------------------------------------------------------------------
# Chunk D -- scaffold wiring + the three-combination install matrix (D2/RV7).
# The wiring (registration, python_package token, required-token gate,
# team-gated placement) landed in B0/B/C; this pins the matrix: each module
# combination installs the right surface, python-security is never auto-on for
# a non-Python adopter, src-layout works, and upgrade proceeds with a filled
# token.
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
class TestModuleMatrix:
    def test_content_security_alone_no_orchestrator(self, tmp_path):
        # content-security alone: the stdlib runner installs; the python
        # orchestrator does NOT (it is python-security's).
        assert _install_modules(tmp_path, ["content-security"],
                                python_package=None) == 0
        assert (tmp_path / "scripts" / "content_scan_runner.py").is_file()
        assert (tmp_path / "scripts" / "content_scan_roots.txt").is_file()
        assert not (tmp_path / "scripts" / "run_security_audit.py").exists()

    def test_python_security_alone_installs_orchestrator_not_runner(self, tmp_path):
        (tmp_path / "mypkg").mkdir()
        assert _install_modules(tmp_path, ["python-security"],
                                python_package="mypkg") == 0
        assert (tmp_path / "scripts" / "run_security_audit.py").is_file()
        # content-security not selected -> its runner is absent.
        assert not (tmp_path / "scripts" / "content_scan_runner.py").exists()

    def test_python_security_not_in_any_default_or_preset(self):
        # Capability-gated: never default-on, never in a preset baseline.
        from bootstrap._scaffold.config import _DEFAULT_ON_MODULES, _PRESETS  # noqa: PLC0415
        assert "python-security" not in _DEFAULT_ON_MODULES
        for name, spec in _PRESETS.items():
            roster = spec.get("modules_add", []) if isinstance(spec, dict) else []
            assert "python-security" not in roster, f"preset {name} adds python-security"

    def test_src_layout_python_package(self, tmp_path):
        # A nested src-layout package path validates + scans.
        (tmp_path / "src" / "mypkg").mkdir(parents=True)
        (tmp_path / "src" / "mypkg" / "__init__.py").write_text("x=1\n",
                                                                encoding="utf-8")
        assert _install_modules(tmp_path, ["python-security"],
                                python_package="src/mypkg") == 0
        _git_repo_if_needed = None  # install does not require git
        orch_mod = _load("run_security_audit_src", _ORCH_SRC)
        lock = _read_lock(tmp_path)
        pkg = orch_mod.validate_python_package(tmp_path, lock)
        assert pkg.name == "mypkg" and pkg.parent.name == "src"

    def test_upgrade_proceeds_with_filled_token(self, tmp_path):
        # The B0 upgrade preflight blocks an unfilled required token; with a
        # filled python_package, --plan proceeds.
        _git_repo(tmp_path)
        (tmp_path / "mypkg").mkdir()
        (tmp_path / "mypkg" / "__init__.py").write_text("x=1\n", encoding="utf-8")
        assert _install_modules(tmp_path, ["content-security", "python-security"],
                                python_package="mypkg") == 0
        _git_commit_all(tmp_path)
        rc = s.main(["upgrade", "--target", str(tmp_path), "--plan",
                     "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0


# ---------------------------------------------------------------------------
# dependency-advisory-coverage -- Chunks A/B/C/D.
#
# MODULE LEVEL, deliberately outside the git-gated TestOrchestrator class:
# these drive _run_tool, the child-environment builder, the argv builder and
# the coverage classifiers directly, so they need neither git nor an installed
# adopter tree and add no skip row to the gate manifest. None of them needs a
# real pip-audit either -- Cairn does not install it, and a test that required
# it would be silently skipped on the machine that ships this code.
#
# CHANNEL NOTE. Subject: the orchestrator. Oracles: a *separate child
# process's* observed behaviour (A-t1..A-t6, B-t1/B-t2), literal constants and
# raw bytes the test itself authors (A-t3..A-t5, B-t3, C-t4, D-t*), and
# synthetic metadata trees the test builds. No oracle is derived from the code
# under test, and no fixture is a schema this session invented and then parsed
# with a parser it also wrote (see D-t2b).
# ---------------------------------------------------------------------------

_orch_mod = _load("run_security_audit_boundary", _ORCH_SRC)


@pytest.fixture(scope="module")
def orchb():
    return _orch_mod


def _probe(source: str) -> list[str]:
    """A child argv that runs `source` under the same isolation real tools get."""
    return [sys.executable, "-I", "-c", source]


def _child_env_view(orch) -> dict:
    """What a child process ACTUALLY sees -- read from the child, not from the
    builder. A different process is the oracle; asking the builder what it
    built would be the artifact under verification supplying its own evidence."""
    import json as _json  # noqa: PLC0415
    run = orch._run_tool(
        _probe("import os,sys,json; sys.stdout.write(json.dumps(dict(os.environ)))"),
        label="env-probe")
    assert run.status == "ran", run.stderr
    return _json.loads(run.stdout)


# --- Chunk A: the shared runner boundary -----------------------------------

_AMBIENT_STEERING = {
    "PIPAPI_PYTHON_LOCATION": "/some/other/python",
    "PIP_AUDIT_VULNERABILITY_SERVICE": "osv",
    "PIP_AUDIT_OSV_URL": "http://127.0.0.1:7777/collect",
    "HTTPS_PROXY": "http://127.0.0.1:8888",
    "REQUESTS_CA_BUNDLE": "/tmp/evil.pem",
}


def test_a_t1_boundary_failure_status_is_degraded_never_clean(orchb, tmp_path,
                                                              monkeypatch):
    # A-t1. A boundary status other than "ran" means the tool produced no
    # trustworthy evidence -> DEGRADED at the pass, never CLEAN. Oracle: the
    # literal tier constants; the subject is the pass's status->tier mapping,
    # driven with a stubbed boundary so this node does not depend on the
    # deadline mechanism A-t2 owns.
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    for status in ("timeout", "truncated", "undecodable", "timeout+cleanup-failed"):
        monkeypatch.setattr(orchb, "_run_tool",
                            lambda *a, _s=status, **k: orchb.ToolRun(0, _s, "", ""))
        monkeypatch.setattr(orchb.shutil, "which", lambda _n: "/usr/bin/bandit")
        st, tier = orchb.run_bandit_pass(pkg, tmp_path)
        assert tier == orchb._AGG_DEGRADED, f"{status} mapped to {tier}"
        assert tier != orchb._AGG_CLEAN


def test_a_t2_timeout_is_enforced_and_bounded(orchb, monkeypatch):
    # A-t2. The timeout EXISTS: a child that sleeps far past the cap is killed,
    # the boundary reports "timeout", and the call returns inside a wall-clock
    # bound. Asserting the bound (rather than settling for a hang) keeps a
    # regression from turning this into an unbounded job.
    monkeypatch.setattr(orchb, "_TOOL_TIMEOUT_S", 1.5)
    started = time.monotonic()
    run = orchb._run_tool(_probe("import time; time.sleep(25)"), label="sleeper")
    elapsed = time.monotonic() - started
    assert run.status.startswith("timeout"), run.status
    assert elapsed < 10, f"timeout not enforced: {elapsed:.1f}s"


def test_a_t3_invalid_utf8_is_recorded_not_raised(orchb):
    # A-t3. One invalid byte used to raise UnicodeDecodeError out of _run_tool,
    # out of main(), and kill the process with exit 1 -- a code inside the
    # COMPONENT space the aggregate exit table promises never to collide with.
    # Bytes are captured, decoded with an explicit policy, and a decode that
    # needed replacement is recorded (-> DEGRADED via A-t1's mapping).
    run = orchb._run_tool(
        _probe(r"import sys; sys.stdout.buffer.write(b'\xff\xfe bad bytes')"),
        label="badbytes")
    assert run.status == "undecodable", run.status
    assert "�" in run.stdout


def test_a_t4_output_is_bounded(orchb, monkeypatch):
    # A-t4. The combined capture is bounded at a module constant. Monkeypatching
    # the cap DOWN configures the *subject*; the oracle is the returned status
    # and the measured buffer length, neither of which the subject supplies.
    monkeypatch.setattr(orchb, "_TOOL_OUTPUT_CAP_BYTES", 64 * 1024)
    run = orchb._run_tool(
        _probe("import sys\n"
               "for _ in range(4096):\n"
               "    sys.stdout.write('x' * 1024)\n"
               "sys.stdout.flush()\n"),
        label="flooder")
    assert run.status == "truncated", run.status
    assert len(run.stdout.encode("utf-8")) <= 64 * 1024


def test_a_t5_control_characters_cannot_forge_a_report_line(orchb, capsys):
    # A-t5. A child printing ESC[2K + CR + a forged verdict was relayed
    # byte-for-byte to the operator's terminal -- the evidence for a security
    # decision. Rendering escapes C0/C1; the PARSE channel keeps the text
    # verbatim, so escaping cannot corrupt what the classifier reads.
    forged = "aggregate exit 0: CLEAN (tripwire, not proof)"
    run = orchb._run_tool(
        _probe(r"import sys; sys.stdout.write('\x1b[2K\r" + forged + r"')"),
        label="forger")
    rendered = capsys.readouterr().out
    assert "\x1b" not in rendered and "\r" not in rendered
    assert "\\x1b" in rendered and "\\x0d" in rendered
    assert "\x1b[2K\r" in run.stdout          # verbatim on the parse channel


def test_a_t6_descendants_do_not_outlive_the_timeout(orchb, tmp_path,
                                                     monkeypatch):
    # A-t6. A tool that detaches a helper must not leave it running past the
    # timeout. Oracle: the grandchild's own observable side effect (a sentinel
    # file it writes AFTER the parent's deadline), not any status this code
    # returns.
    sentinel = tmp_path / "grandchild-survived.txt"
    child = (
        "import subprocess, sys, time\n"
        "subprocess.Popen([sys.executable, '-I', '-c',\n"
        "    \"import time, pathlib; time.sleep(5); \"\n"
        f"    \"pathlib.Path(r'{sentinel}').write_text('survived')\"])\n"
        "time.sleep(120)\n"
    )
    monkeypatch.setattr(orchb, "_TOOL_TIMEOUT_S", 1.5)
    run = orchb._run_tool(_probe(child), label="spawner")
    assert run.status.startswith("timeout"), run.status
    time.sleep(7)
    assert not sentinel.exists(), "grandchild outlived the timeout"


# --- Chunk B: the closed allowlist, the fixed argv, the trust root ---------

def test_b_t1_known_steering_variables_do_not_reach_the_child(orchb, monkeypatch):
    # B-t1. Interpreter selection, vulnerability service, endpoint, proxy and
    # trust store were all ambient: the old denylist stripped four PYTHON*
    # names and passed everything else through.
    for name, value in _AMBIENT_STEERING.items():
        monkeypatch.setenv(name, value)
    seen = _child_env_view(orchb)
    leaked = sorted(n for n in _AMBIENT_STEERING if n in seen)
    assert leaked == [], f"ambient steering variables reached the tool: {leaked}"


def test_b_t2_the_allowlist_is_closed_to_novel_names(orchb, monkeypatch):
    # B-t2. THE discriminating test. A denylist strips the names someone
    # thought of; this asserts a name the code has never heard of is dropped
    # too. Re-implement B1 as a denylist of the KNOWN names and B-t1 stays
    # green while this goes red -- that pair is the whole argument for the
    # allowlist shape.
    monkeypatch.setenv("PIP_AUDIT_FUTURE_KNOB", "1")
    monkeypatch.setenv("A_TOOL_NOBODY_HAS_HEARD_OF", "1")
    seen = _child_env_view(orchb)
    assert "PIP_AUDIT_FUTURE_KNOB" not in seen
    assert "A_TOOL_NOBODY_HAS_HEARD_OF" not in seen


def test_b_t3_pip_audit_argv_is_fixed_and_environment_free(orchb, monkeypatch,
                                                           tmp_path):
    # B-t3. Two halves. (a) every pinned flag is present. (b) NO element is
    # derived from os.environ -- every environment value is sentinel-stamped,
    # so an interpolated one is visible in argv. Oracle: literals typed here.
    for name in list(os.environ):
        monkeypatch.setenv(name, "CAIRN-ENV-SENTINEL-8f21")
    argv = orchb.pip_audit_argv(cache_dir=tmp_path)
    assert argv[:4] == [sys.executable, "-I", "-m", "pip_audit"]
    for flag, value in (("--format", "json"),
                        ("--vulnerability-service", "osv"),
                        ("--progress-spinner", "off"),
                        ("--cache-dir", str(tmp_path))):
        assert flag in argv, f"pinned flag {flag} missing"
        assert argv[argv.index(flag) + 1] == value
    assert "--output" not in argv          # stdout, never a path
    assert not any("CAIRN-ENV-SENTINEL-8f21" in element for element in argv)


def test_b_t4_environment_pass_through_is_never_silent(orchb, monkeypatch):
    # B-t4. A closed allowlist can break a tool that legitimately needs an
    # unlisted variable (a corporate trust store is the realistic case), so an
    # explicit opt-in exists -- and the report NAMES every variable it passed.
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", "/corp/ca.pem")
    line = orchb.describe_child_env(("REQUESTS_CA_BUNDLE",))
    assert "REQUESTS_CA_BUNDLE" in line
    assert "REQUESTS_CA_BUNDLE" not in orchb.describe_child_env(())
    assert orchb.build_child_env(("REQUESTS_CA_BUNDLE",))["REQUESTS_CA_BUNDLE"] \
        == "/corp/ca.pem"
    assert "REQUESTS_CA_BUNDLE" not in orchb.build_child_env(())
    assert orchb.parse_pass_env(["--pass-env", "REQUESTS_CA_BUNDLE"]) \
        == ("REQUESTS_CA_BUNDLE",)


def test_b_t5_no_local_env_trust_root_is_read(orchb, monkeypatch, tmp_path):
    # B-t5. DAC5's withdrawal, ENFORCED rather than intended: the orchestrator
    # creates no second reader of dev/.cairn/local-env.json, which AGENTS.md
    # calls an executable trust root. The DISCRIMINATING half intercepts the
    # open and asserts on the argument -- a source-text lint is evaded by any
    # assembled path, and "did not open it" is vacuous wherever the file is
    # absent, which makes a source lint an environment-dependent oracle.
    opened: list[str] = []
    real_open, real_path_open = builtins.open, Path.open

    def spy_open(file, *a, **k):
        opened.append(str(file))
        return real_open(file, *a, **k)

    def spy_path_open(self, *a, **k):
        opened.append(str(self))
        return real_path_open(self, *a, **k)

    monkeypatch.setattr(builtins, "open", spy_open)
    monkeypatch.setattr(Path, "open", spy_path_open)
    monkeypatch.setattr(orchb.shutil, "which", lambda _n: None)
    monkeypatch.setattr(orchb.importlib.util, "find_spec", lambda _n: None)
    orchb.run_pip_audit_pass(tmp_path, allow_egress=False)
    monkeypatch.undo()
    hits = [p for p in opened if p.endswith("local-env.json")]
    assert hits == [], f"the orchestrator read the local interpreter binding: {hits}"
    # Secondary signal only -- NOT the discriminating half.
    assert "local-env" not in _ORCH_SRC.read_text(encoding="utf-8")


# --- Chunk C: every blocking reason, and the worst-applicable tier ---------

def _force_tool_absent(orch, monkeypatch):
    monkeypatch.setattr(orch.shutil, "which", lambda _n: None)
    monkeypatch.setattr(orch.importlib.util, "find_spec", lambda _n: None)


def test_c_t1_every_blocking_reason_is_reported(orchb, tmp_path, monkeypatch,
                                                capsys):
    # C-t1. The pass used to return at the FIRST blocker, so an egress-off run
    # never mentioned that the tool was absent at all. Both reasons are now
    # evaluated independently, both printed, and both carried in the status.
    _force_tool_absent(orchb, monkeypatch)
    status, _ = orchb.run_pip_audit_pass(tmp_path, allow_egress=False)
    out = capsys.readouterr()
    text = out.out + out.err
    assert "tool-absent" in status and "egress-off-unavailable" in status
    assert "NOT INSTALLED" in text and "network egress OFF" in text


def test_c_t3_absent_tool_dominates_egress_off(orchb, tmp_path, monkeypatch):
    # C-t3. The tier is the WORST applicable reason, not the first one found.
    # The egress disposition is evaluated FIRST, so a first-wins implementation
    # returns 5 and this test discriminates -- an ordering where the worst
    # reason happens to be found first would make it unfalsifiable.
    _force_tool_absent(orchb, monkeypatch)
    status, tier = orchb.run_pip_audit_pass(tmp_path, allow_egress=False)
    assert status.split("+")[0] == "egress-off-unavailable"
    assert tier == orchb._AGG_DEGRADED
    assert tier != orchb._AGG_INCOMPLETE


def test_c_t4_aggregate_space_and_precedence_are_unchanged(orchb):
    # C-t4. A cheap tripwire making the "aggregate exit space untouched" fence
    # checkable rather than promised. (a) the space. (b) the PRECEDENCE --
    # replacing max with min, or with last-tier-wins, changes no constant and
    # would otherwise slip through.
    assert {orchb._AGG_CLEAN, orchb._AGG_INCOMPLETE,
            orchb._AGG_FINDINGS, orchb._AGG_DEGRADED} == {0, 5, 10, 20}
    assert orchb.aggregate_tier([]) == 0
    assert orchb.aggregate_tier([0, 5]) == 5
    assert orchb.aggregate_tier([20, 10, 5, 0]) == 20      # not last-wins
    assert orchb.aggregate_tier([0, 5, 10, 20]) == 20      # not min


def test_c_t5_interpreter_observation_is_reported(orchb, tmp_path, monkeypatch,
                                                  capsys):
    # C-t5. C1's third disposition. The interpreter is recorded as an
    # OBSERVATION of the environment audited -- never an assertion that it
    # matches a project record (DAC5).
    _force_tool_absent(orchb, monkeypatch)
    orchb.run_pip_audit_pass(tmp_path, allow_egress=False)
    text = capsys.readouterr().out
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    assert sys.executable in text and version in text
    assert "OBSERVATION" in text


# --- Chunk D: the denominator, the dispositions, and the CLEAN gate --------

# --- pip-audit report fixtures: WHAT SUPPLIES THE MATERIAL --------------------
#
# The three payloads below were **emitted by pip-audit's own JsonFormat**, not
# hand-written to match the parser. Method, reproducible and egress-free: build
# `pip_audit._service.ResolvedDependency` / `SkippedDependency` values, call
# `JsonFormat(output_desc=False, output_aliases=False).format(result, [])` on the
# canonical interpreter, and paste the returned bytes verbatim. pip-audit 2.10.1,
# as_of 2026-08-05. No audit ran and no network was contacted -- a JSON shape is
# a property of the formatter, so the formatter is the oracle.
#
# They are pasted as literals rather than generated at test time on purpose:
# Cairn does not install pip-audit, so a test that imported it would be silently
# skipped on the machines that ship this code.
_PA_ONE_SKIPPED = (
    '{"dependencies": [{"name": "requests", "version": "2.31.0", "vulns": []}, '
    '{"name": "jinja2", "version": "3.1.2", "vulns": []}, '
    '{"name": "modflow-tools", "skip_reason": "Dependency not found on PyPI '
    'and could not be audited: modflow-tools (0.1.0)"}], "fixes": []}')
_PA_ALL_RESOLVED = (
    '{"dependencies": [{"name": "requests", "version": "2.31.0", "vulns": []}, '
    '{"name": "jinja2", "version": "3.1.2", "vulns": []}], "fixes": []}')
_PA_ABSENT_NAMES = (
    '{"dependencies": ['
    '{"name": "cairn-probe-not-installed-a", "version": "0.0.1", "vulns": []}, '
    '{"name": "cairn-probe-not-installed-b", "version": "0.0.2", "vulns": []}, '
    '{"name": "cairn-probe-not-installed-c", "skip_reason": "Dependency not '
    'found on PyPI and could not be audited: cairn-probe-not-installed-c '
    '(0.0.3)"}], "fixes": []}')


def _only_child_reported_unknowns(orch, monkeypatch):
    """Zero the OTHER two UNKNOWN contributors -- the residual survey and the
    conda enumeration -- so a tier assertion is a statement about the child's
    reported enumeration alone. Both are *inputs* to the tier arithmetic here,
    never the oracle, and leaving them live would couple the central claim to
    whatever the machine running the suite happens to have installed."""
    monkeypatch.setattr(orch, "survey_local_builds",
                        lambda *a, **k: orch.LocalBuilds(0, 0, 0, ()))
    monkeypatch.setattr(orch, "conda_non_coverage",
                        lambda *a, **k: orch.CondaScope(False, 0, 0, 0))


def test_d_t1_a_skipped_distribution_is_never_scanned(orchb):
    # D-t1. A distribution pip-audit could not RESOLVE had nothing looked up
    # about it, so it is UNKNOWN -- never SCANNED. The hazard is not a rounding
    # error: fold the skipped partition into SCANNED and the UNKNOWN count drops
    # to zero, which makes CLEAN reachable on a run where part of the dependency
    # set was never audited.
    import json as _json  # noqa: PLC0415

    # The premise, pinned against the tool's own bytes rather than asserted:
    # there is NO top-level `skipped` key. The skipped set is inline in
    # `dependencies`, discriminated only by carrying skip_reason.
    report = _json.loads(_PA_ONE_SKIPPED)
    assert sorted(report) == ["dependencies", "fixes"]
    assert "skipped" not in report
    entries = report["dependencies"]
    assert sum("skip_reason" in e for e in entries) == 1

    # This node owns the PARTITION; D-t6 owns the names, so each has a mutation
    # that reddens it alone.
    coverage = orchb.classify_pip_audit_output(_PA_ONE_SKIPPED)
    assert coverage.established is True
    assert coverage.scanned == 2, "the two RESOLVED entries, and only those"
    assert coverage.unknown == 1, "the entry the tool reported it could not resolve"
    # The discriminator is the PRESENCE of skip_reason, not the absence of a
    # version: a skipped entry in the sibling `fixes` array carries name,
    # version AND skip_reason, so keying on "no version" mis-partitions.
    assert coverage.scanned + coverage.unknown == len(entries)


def test_d_t6_the_denominator_is_the_childs_not_the_parents(orchb):
    # D-t6. The denominator is the set the CHILD reported enumerating, never a
    # parent-side count the orchestrator took itself and assumed the child
    # shared. The fixture makes the two differ by construction: none of its
    # names is installed in this interpreter, so a parent-derived denominator
    # cannot coincidentally agree.
    #
    # HONEST LIMIT, restated from the plan: this is only *worth* having because
    # Chunk B pins the child to this interpreter (B-t1/B-t2). Remove that pin
    # and a child-reported denominator silently describes another environment.
    coverage = orchb.classify_pip_audit_output(_PA_ABSENT_NAMES)
    assert coverage.established is True
    assert coverage.names == ("cairn-probe-not-installed-a",
                              "cairn-probe-not-installed-b",
                              "cairn-probe-not-installed-c")

    installed = orchb.installed_distribution_names()
    assert len(installed) > len(coverage.names) + 10, (
        "this assertion only discriminates where the parent's inventory is "
        f"clearly larger than the fixture's; parent has {len(installed)}")
    assert not (set(coverage.names) & installed), (
        "the fixture must name nothing installed here, or a parent-derived "
        "denominator could agree by accident")


def test_d_t2_one_unknown_gates_clean(orchb, tmp_path, monkeypatch):
    # D-t2 -- THE CENTRAL CLAIM OF THE PROPOSAL. The tool ran, exited 0 and
    # reported no vulnerabilities at all; one distribution it could not resolve
    # is enough to deny CLEAN. Both halves are asserted, because the first alone
    # would also pass if the leg could never be CLEAN: an always-INCOMPLETE leg
    # is a test that cannot fail, not a gate.
    _only_child_reported_unknowns(orchb, monkeypatch)
    monkeypatch.setattr(orchb.shutil, "which", lambda _n: "/usr/bin/pip-audit")

    def _run(report):
        # NOTE: _run_tool is stubbed, so allow_egress=True egresses nothing.
        monkeypatch.setattr(orchb, "_run_tool",
                            lambda *a, **k: orchb.ToolRun(0, "ran", report, ""))
        return orchb.run_pip_audit_pass(tmp_path, allow_egress=True)

    status, tier = _run(_PA_ONE_SKIPPED)
    assert tier == orchb._AGG_INCOMPLETE and tier != orchb._AGG_CLEAN, status
    assert "unknown" in status
    status, tier = _run(_PA_ALL_RESOLVED)
    assert tier == orchb._AGG_CLEAN, f"the gate does not discriminate: {status}"


def test_d_t2b_an_unreadable_enumeration_fails_closed(orchb):
    # D-t2b. Two guards, each its own single-property falsifier. (i) a schema
    # treated as unestablished is UNKNOWN even for a perfectly well-formed
    # report -- the pre-decided fail-closed fallback, kept reachable now that
    # the schema IS established at a pinned version. (ii) a top level that is
    # not the measured shape fails closed instead of being read optimistically.
    unestablished = orchb.classify_pip_audit_output(_PA_ALL_RESOLVED,
                                                    schema_established=False)
    assert unestablished.established is False
    assert unestablished.scanned == 0 and unestablished.names == ()
    for hostile in ('{"fixes": []}',
                    '{"dependencies": {"requests": "2.31.0"}}',
                    '[]'):
        shape = orchb.classify_pip_audit_output(hostile, schema_established=True)
        assert shape.established is False, hostile
        assert "dependencies" in shape.note, hostile


def test_d_t3_malformed_output_is_never_clean(orchb):
    # D-t3. A parse failure fails CLOSED. The fallback this rules out --
    # "assume clean on parse failure" -- is a distinct code path from D-t2's
    # unpinned-schema path, so each has its own single-property falsifier.
    for hostile in ("not json at all",
                    '{"dependencies": [',                 # truncated
                    '{"dependencies": [�]}'):        # decode-replaced
        result = orchb.classify_pip_audit_output(hostile, schema_established=True)
        assert result.established is False, hostile
        assert "not parseable JSON" in result.note, hostile


def test_d_t4_residual_predicate_rejects_public_build_artifacts(orchb):
    # D-t4. Read literally -- "installed from a local path or a VCS checkout" --
    # the Decision's predicate admits every conda-forge build artifact: 241
    # public packages on the environment this was measured on, against 2 the
    # rule is actually for. The predicate is editable-or-VCS. Four PEP 610
    # shapes, including archive_info, whose file:// URL the literal reading
    # also admits.
    editable = '{"dir_info": {"editable": true}, "url": "file:///home/me/proj"}'
    conda_forge = ('{"dir_info": {}, "url": '
                   '"file:///home/conda/feedstock_root/build_artifacts/x"}')
    archive = ('{"archive_info": {"hash": "sha256=deadbeef"}, "url": '
               '"file:///Users/runner/miniforge3/conda-bld/x.tar.bz2"}')
    vcs = '{"vcs_info": {"vcs": "git", "commit_id": "abc"}, "url": "https://h/r"}'
    assert orchb.local_build_disposition(editable) == "residual"
    assert orchb.local_build_disposition(vcs) == "residual"
    assert orchb.local_build_disposition(conda_forge) == "not-residual"
    assert orchb.local_build_disposition(archive) == "not-residual"
    assert orchb.local_build_disposition(None) == "not-residual"


def test_d_t7_unreadable_direct_url_is_unknown_not_skipped(orchb):
    # D-t7. direct_url.json is package-controlled input -- the same trust class
    # as the tool output this plan hardens. An unparseable payload is UNKNOWN
    # (which gates CLEAN), never "does not qualify", never silently skipped.
    assert orchb.local_build_disposition('{"dir_info": {"edit') == "unknown"
    assert orchb.local_build_disposition("[1, 2, 3]") == "unknown"

    class _FakeDist:
        def __init__(self, payload):
            self._payload = payload
            self.metadata = {"Name": "fake"}

        def read_text(self, name):
            return self._payload if name == "direct_url.json" else None

    survey = orchb.survey_local_builds([_FakeDist('{"dir_info": {"edit')])
    assert survey.unknown == 1 and survey.residual == 0 and survey.not_residual == 0


def _conda_prefix(root: Path, records: dict) -> Path:
    meta = root / "conda-meta"
    meta.mkdir(parents=True)
    for filename, body in records.items():
        (meta / filename).write_text(body, encoding="utf-8")
    return root


def test_d_t5_non_coverage_is_the_set_difference_not_the_raw_count(orchb,
                                                                   tmp_path):
    # D-t5. Quantified non-coverage: the number reported is what this leg did
    # NOT audit -- conda names MINUS the Python distributions it did. Reporting
    # the raw conda count would overstate the gap and, worse, would make the
    # two inventories look like one.
    prefix = _conda_prefix(tmp_path / "env", {
        "numpy-2.0-py313.json": '{"name": "numpy", "version": "2.0"}',
        "libgeos-3.12-h1.json": '{"name": "libgeos", "version": "3.12"}',
        "krb5-1.21-h2.json": '{"name": "krb5", "version": "1.21"}',
    })
    scope = orchb.conda_non_coverage(prefix, {"numpy"})
    assert scope.applicable is True
    assert scope.records == 3
    assert scope.conda_only == 2, "expected the set difference, not the raw count"
    assert scope.unknown == 0


def test_d_t8_hostile_conda_meta_is_bounded_and_fails_closed(orchb, tmp_path):
    # D-t8. The directory is derived from sys.prefix and its records are
    # package-controlled. An unguarded glob-plus-parse raises on the non-JSON
    # `history` / `state` entries every conda prefix carries -- and an uncaught
    # JSONDecodeError escapes main() (the module has no broad handler) and
    # exits 1, into the COMPONENT code space the exit table promises the
    # aggregate never uses. Extension-scoped, size-capped, and every unreadable
    # record counted as UNKNOWN rather than dropped.
    prefix = _conda_prefix(tmp_path / "env", {
        "good-1.0-h0.json": '{"name": "good"}',
        "history": "==> 2026-08-05 <==\n+ not json\n",
        "state": "{not json either",
        "broken-1.0-h0.json": '{"name": "broken"',
        "big-1.0-h0.json": '{"name": "big", "pad": "' + "z" * 4096 + '"}',
    })
    scope = orchb.conda_non_coverage(prefix, set(), max_record_bytes=1024)
    assert scope.applicable is True
    assert scope.records == 3, "non-JSON siblings must not be enumerated at all"
    assert scope.unknown == 2, "the malformed and the oversized record are UNKNOWN"
    assert scope.conda_only == 1
    # A prefix that is not a conda environment is simply not applicable.
    assert orchb.conda_non_coverage(tmp_path / "nope", set()).applicable is False
