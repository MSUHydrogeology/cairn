"""The selected-module required-token
preflight.

A module may declare inline tokens that have no safe default (the first is
``python-security``'s ``{{python_package}}``).  Selecting such a module without
a filled value must **fail closed before any write** -- no target-tree files, no
lockfile / module-state mutation -- on all three install paths: a fresh install,
``upgrade --adopt-module``, and the writing ``upgrade`` paths (``--stage`` /
``--apply``).  The read-only ``upgrade --plan`` stays available so an adopter can
diagnose the gap.

Contracts pinned here:

* ``missing_required_tokens`` flags absent / empty / placeholder-valued required
  tokens and only for *selected* modules (pure, side-effect-free).
* fresh install / dry-run refuse (exit 2) and write nothing when a selected
  module's required token is unfilled; they succeed once it is supplied.
* ``adopt-module`` refuses (exit 2) and leaves the lockfile + tree untouched.
* the writing upgrade paths refuse (exit 2); ``--plan`` still returns 0.

Promises:
- A selected module whose required token is unfilled makes fresh install,
  dry run, adopt-module and writing upgrades exit 2 and change nothing;
  read-only plan still runs.
- A filled required token lets the selected module install.
- The content-scan runner exits 0 when clean, 1 for an advisory finding, 2
  when it cannot give a trustworthy result, and 3 for a stale residual
  baseline.
- The dispatcher mode prints one JSON result document, and an empty, failed
  or stale audit never reads as clean.
- A roots manifest that escapes the project, is absolute, names a Git
  option, or lacks its sentinel is refused.
- A redirected Git directory in the environment cannot change which files
  the audit covers.
- The installed audit reports incomplete, never clean, when pip-audit egress
  is off, and degraded when a required tool is absent or apparatus is
  altered.
- A scan that runs past its wall-clock limit fails closed with exit 2.
- The scan also exits 2 when a file is over the per-file budget or Git cannot list the audited set.
- Each tool that pins a Git helper, run as its own command, refuses a helper that misses its pin or sits in the wrong place, and the helper never runs.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_security_stack.py
"""
from __future__ import annotations

import builtins
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import types
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
#: A stub module, so the gate is exercised end-to-end against a real
#: registration, not a synthetic monkeypatch.
_REQ_MODULE = "python-security"
_REQ_TOKEN = "python_package"


# ---------------------------------------------------------------------------
# The stub registration is real
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# missing_required_tokens -- the pure check
# ---------------------------------------------------------------------------


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

    def test_angle_bracket_placeholder_dry_run_refuses(self, tmp_path):
        # Defect 19: a `<...>` placeholder is unfilled, as `{{...}}` is.
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            'project_name: T\ntest_command: pytest\n'
            f'{_REQ_TOKEN}: "<my package>"\n'
            f"modules:\n  - {_REQ_MODULE}\n",
            encoding="utf-8",
        )
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
# plus the v1 self-audit trust-model statement.  A doctrine-presence
# contract so the load-bearing wording cannot silently regress, and a
# generalization guard so the modflow_tools-specific tool names do not leak up.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Chunk B -- content-security: the atomic stdlib-only injection apparatus.
# The content_scan_runner contract: audited-roots manifest, per-file
# symlink/special-file containment (Imp #3), resource budgets (Imp #4), the
# 0/1/2/3 exit contract, multiset NEW/STALE, sentinel/version validation,
# host-still-flagged, the narrow homoglyph allowance, tripwire output.
# ---------------------------------------------------------------------------

_TEAM_GATED = TEMPLATES_ROOT / "modules" / "team-gated"
_RUNNER_SRC = _TEAM_GATED / "content_scan_runner.py"
_SCAN_SRC = _TEAM_GATED / "content_scan.py"

_HAS_GIT = shutil.which("git") is not None
#: Bandit availability -- real-tool tests gate on this so Cairn's base suite
#: never silently requires Bandit.
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


@pytest.fixture(scope="session")
def csr():
    return _load("content_scan_runner", _RUNNER_SRC)


@pytest.fixture(scope="session")
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


def _write_installed_lock(root: Path, lock: dict) -> None:
    (root / _LOCKFILE_REL).write_text(_emit_lock_yaml(lock), encoding="utf-8")


def _set_installed_digest(lock: dict, destination: str, data: bytes) -> None:
    record = next(row for row in lock["files"]
                  if row.get("dst") == destination)
    record["hash"] = "sha256:" + hashlib.sha256(data).hexdigest()


def _install_audit_entry_tripwires(root: Path, helper_marker: Path,
                                   injection_marker: Path) -> None:
    """Give the isolated adopter's verified helper and injection leg markers.

    The marker code is admitted by the fixture's own fixed helper pin and
    install records, so the real audit command proves both tripwires work
    before its physical mutation is applied.
    """
    helper_rel = "tools/git_read.py"
    runner_rel = "scripts/content_scan_runner.py"
    helper = root / helper_rel
    helper_bytes = helper.read_bytes() + (
        "\nimport pathlib as _audit_marker_pathlib\n"
        f"_audit_marker_pathlib.Path({str(helper_marker)!r}).write_text("
        "'verified-helper-ran', encoding='utf-8')\n"
    ).encode("utf-8")
    helper.write_bytes(helper_bytes)
    helper_digest = hashlib.sha256(helper_bytes).hexdigest()

    runner = root / runner_rel
    runner_text = runner.read_text(encoding="utf-8")
    pin = re.search(r'(?m)^_GIT_READ_SHA256 = "([0-9a-f]{64})"$',
                    runner_text)
    assert pin, "installed content runner has no helper pin"
    runner_text = (runner_text[:pin.start(1)] + helper_digest
                   + runner_text[pin.end(1):])
    loader = "_GIT_READ = _load_verified_git_read()\n"
    assert runner_text.count(loader) == 1, "helper load site changed"
    runner_text = runner_text.replace(
        loader,
        loader +
        f"Path({str(injection_marker)!r}).write_text("
        "'injection-started', encoding='utf-8')\n",
        1,
    )
    runner_bytes = runner_text.encode("utf-8")
    runner.write_bytes(runner_bytes)

    lock = _read_lock(root)
    _set_installed_digest(lock, helper_rel, helper_bytes)
    _set_installed_digest(lock, runner_rel, runner_bytes)
    _write_installed_lock(root, lock)


def _write_cwd_helper_decoy(root: Path, marker: Path) -> None:
    tools = root / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    helper = tools / "git_read.py"
    helper.write_text(
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('cwd-helper-ran', "
        "encoding='utf-8')\n",
        encoding="utf-8",
    )
    digest = hashlib.sha256(helper.read_bytes()).hexdigest()
    (tools / "git_read.py.sha256").write_text(digest + "\n",
                                                encoding="ascii")


def _run_installed_audit(root: Path, cwd: Path, *, cache_marker: Path | None = None):
    env = {**os.environ, "PYTHONPATH": ""}
    script = root / "scripts" / "run_security_audit.py"
    if cache_marker is None:
        argv = [sys.executable, str(script)]
    else:
        wrapper = (
            "import importlib.machinery, pathlib, runpy, sys, types\n"
            "script, marker = sys.argv[1:3]\n"
            "runner = pathlib.Path(script).with_name('content_scan_runner.py')\n"
            "original_get_data = importlib.machinery.SourceFileLoader.get_data\n"
            "def forbid_runner_read(loader, path):\n"
            "    if pathlib.Path(loader.path) == runner:\n"
            "        pathlib.Path(marker).write_text('runner-code-reopened')\n"
            "        raise RuntimeError('runner source or bytecode reopened')\n"
            "    return original_get_data(loader, path)\n"
            "importlib.machinery.SourceFileLoader.get_data = forbid_runner_read\n"
            "cached = types.ModuleType('_cairn_verified_git_read')\n"
            "def tripwire(name):\n"
            "    pathlib.Path(marker).write_text('cached-module-ran', "
            "encoding='utf-8')\n"
            "    raise AttributeError(name)\n"
            "cached.__getattr__ = tripwire\n"
            "sys.modules[cached.__name__] = cached\n"
            "sys.argv = [script]\n"
            "runpy.run_path(script, run_name='__main__')\n"
        )
        argv = [sys.executable, "-c", wrapper, str(script), str(cache_marker)]
    return subprocess.run(argv, cwd=str(cwd), env=env, capture_output=True,
                          text=True, timeout=180)


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
        # load_audit_roots returns (rel, required) tuples; `!` => required.
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

    @pytest.mark.parametrize("entry", ["--others", "!--others"])
    def test_option_shaped_root_refused(self, csr, tmp_path, entry):
        m = tmp_path / "roots.txt"
        m.write_text(
            f"# content-scan-roots v1\n{entry}\n", encoding="utf-8")
        with pytest.raises(csr.AuditError, match="Git option"):
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


    def test_unit_not_flagged_credential_flagged_in_scan(self, cscan):
        flags = list(cscan.scan_text("a µs reading and a pаypal token\n"))
        homoglyph = [f for f in flags if f.pattern_id == "homoglyph"]
        # Exactly one homoglyph flag (the Cyrillic-spoofed credential), and the
        # µs scientific unit is NOT among the flagged tokens (the unit allowance cleared it).
        assert len(homoglyph) == 1
        assert "ypal" in homoglyph[0].message  # the credential token (Latin tail)
        assert not any("µs" in f.message for f in homoglyph)


@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
class TestRunnerExitContract:

    def test_dispatcher_mode_emits_one_closed_result_document(
            self, csr, capsys, monkeypatch):
        monkeypatch.setattr(
            csr, "audit", lambda: (1, [Path("a.md")], [object()], [], []))
        assert csr.main(["--dispatcher"]) == 10
        out = capsys.readouterr().out
        assert len(out.splitlines()) == 1
        result = json.loads(out)
        assert set(result) == {
            "schema", "capability", "contract", "evidence_mode",
            "result", "details"}
        assert result["result"] == "FINDINGS"
        assert result["capability"] == "content-security"
        assert result["evidence_mode"] == "offline"
        assert "including 0 new" in result["details"]

    def test_empty_audit_cannot_become_clean_dispatcher_evidence(
            self, csr, capsys, monkeypatch):
        monkeypatch.setattr(csr, "audit", lambda: (0, [], [], [], []))
        assert csr.main(["--dispatcher"]) == 20
        result = json.loads(capsys.readouterr().out)
        assert result["result"] == "DEGRADED"

    @pytest.mark.parametrize("failure_code", [2, 3])
    def test_failed_or_stale_audit_cannot_become_clean_dispatcher_evidence(
            self, csr, capsys, monkeypatch, failure_code):
        monkeypatch.setattr(
            csr, "audit", lambda: (failure_code, [], [], [], [("stale", 1)]))
        assert csr.main(["--dispatcher"]) == 20
        result = json.loads(capsys.readouterr().out)
        assert result["result"] == "DEGRADED"

    def test_direct_runner_rejects_unknown_mode_without_changing_no_arg_path(
            self, csr, capsys, monkeypatch):
        monkeypatch.setattr(
            csr, "audit", lambda: (0, [Path("a.md")], [], [], []))
        assert csr.main([]) == 0
        assert "content_scan runner: scanned 1" in capsys.readouterr().out
        with pytest.raises(SystemExit):
            csr.main(["--unknown"])
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
        # The manifest itself is in the audited set.
        rels = {p.relative_to(tmp_path).as_posix() for p in files}
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
        # A multi-tenant code host is NOT allowlisted -> stays a finding on an
        # instruction surface. Discussion prose intentionally disables this
        # one detector under content-scan-url-classification.
        (tmp_path / "AGENTS.md").write_text(
            "see https://github.com/evil/x for details\n", encoding="utf-8")
        (tmp_path / "scripts" / "content_scan_roots.txt").write_text(
            "# content-scan-roots v1\ndev\nAGENTS.md\n", encoding="utf-8")
        _git_commit_all(tmp_path)
        code, _files, all_flags, _new, _stale = self._run(csr, tmp_path)
        assert code == 1
        assert any(fl.pattern_id == "suspicious-url" for _r, fl, _fp in all_flags)

    def test_missing_required_root_fails_even_with_a_healthy_root(self, csr, tmp_path):
        # A manifest with a required root that is absent must FAIL even
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

    # Declared exception (internal hook): hook: run_content_scan(deadline=...) with a past deadline; a real overrun needs the 120 s ceiling _MAX_WALL_SECONDS.
    def test_wall_clock_overrun_fails_closed(self, csr, tmp_path):
        # An exceeded wall-clock deadline fails closed (exit 2) -- a
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


class TestStaleBaselineMessageScope:
    """The exit-3 message names the set it audited, and instructs accordingly.

    The runner concludes over the roots its manifest names, but the reviewed
    residual baseline it compares against has several consumers. On a tree
    where two of those consumers disagree, the old wording -- a bare "prune the
    residual baseline" -- told an operator to delete live entries from a shared
    reviewed security artifact on evidence that covered only this runner's own
    set. One did, and was saved by a contract test they happened to have.
    """

    _STALE = [("dev/gone.md:homoglyph:0123456789ab", 1)]

    def _summary_stderr(self, csr, capsys) -> str:
        csr._print_summary(3, [], [], [], self._STALE)
        return capsys.readouterr().err


    # Declared exception (internal hook): hooks: csr.load_audit_roots and csr.audit monkeypatched; no public route makes the manifest unreadable at message time while the audit still returns 3.
    def test_unresolvable_roots_degrade_the_message_without_changing_exit_three(
            self, csr, capsys, monkeypatch):
        """The message's own input can fail. It must then say so and still
        report exit 3 -- a summary that raised would convert a fail-closed
        detection into a crash on the one path this wording exists to fix."""
        def _boom(*_a, **_k):
            raise csr.AuditError("manifest unreadable")

        monkeypatch.setattr(csr, "load_audit_roots", _boom)
        monkeypatch.setattr(
            csr, "audit", lambda *_a, **_k: (3, [], [], [], self._STALE))
        assert csr.main() == 3
        err = capsys.readouterr().err
        assert csr._ROOTS_MANIFEST.name in err
        assert "could NOT be resolved" in err
        assert "STALE baseline authority" in err


@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
class TestRunnerGitBoundary:
    def test_ambient_git_dir_cannot_redirect_the_audited_set(
            self, csr, tmp_path, monkeypatch):
        target = tmp_path / "target"
        other = tmp_path / "other"
        target.mkdir(); other.mkdir()
        _git_repo(target); _seed_apparatus(target); _git_commit_all(target)
        _git_repo(other)
        (other / "dev").mkdir()
        (other / "dev" / "redirected.md").write_text(
            "wrong repository\n", encoding="utf-8")
        _git_commit_all(other)

        monkeypatch.setenv("GIT_DIR", str(other / ".git"))
        files = csr.audited_text_files(
            target, target / "scripts" / "content_scan_roots.txt")
        rels = {path.relative_to(target).as_posix() for path in files}
        assert "dev/doc.md" in rels
        assert "dev/redirected.md" not in rels


    def test_resolved_git_is_reported_once(self, csr, tmp_path, capsys):
        _git_repo(tmp_path); _seed_apparatus(tmp_path); _git_commit_all(tmp_path)
        csr.audited_text_files(
            tmp_path, tmp_path / "scripts" / "content_scan_roots.txt")
        out = capsys.readouterr().out
        assert out.count("content_scan: Git executable ") == 1
        assert "provenance not authenticated" in out


# The failing Git is a shell script, so that row exists only where one can run.
@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
@pytest.mark.parametrize(
    "hostile",
    ["file-over-the-budget"] + ([] if os.name == "nt" else ["git-cannot-list"]))
def test_scan_exits_two_when_it_cannot_vouch_for_its_set(tmp_path, hostile):
    """The shipped runner, run as a command, exits 2 and not 0 when a file is
    over the per-file budget or Git cannot list the audited set.  The same
    tree scans clean (exit 0) before the hostile setup is applied."""
    root = tmp_path / "delivery"
    root.mkdir()
    _git_repo(root); _seed_apparatus(root)
    shutil.copy(_RUNNER_SRC, root / "scripts" / "content_scan_runner.py")
    (root / "tools").mkdir()
    shutil.copy(TEMPLATES_ROOT / "skills" / "_lib" / "git_read.py",
                root / "tools" / "git_read.py")
    _git_commit_all(root)
    env = {**os.environ, "PYTHONPATH": ""}

    def scan() -> int:
        return subprocess.run(
            [sys.executable, str(root / "scripts" / "content_scan_runner.py")],
            cwd=tmp_path, env=env, capture_output=True, text=True,
            timeout=120).returncode

    clean = scan()
    if hostile == "file-over-the-budget":
        (root / "dev" / "big.md").write_text("x" * (9 * 1024 * 1024))
        _git_commit_all(root)
    else:
        bin_dir = tmp_path / "failing-git-bin"
        bin_dir.mkdir()
        fake = bin_dir / "git"
        fake.write_text(
            "#!/bin/sh\n"
            'for arg in "$@"; do [ "$arg" = ls-files ] && exit 128; done\n'
            f'exec "{shutil.which("git")}" "$@"\n')
        fake.chmod(0o755)
        env["PATH"] = str(bin_dir) + os.pathsep + env["PATH"]
    assert (clean, scan()) == (0, 2)


@pytest.mark.skipif(not _HAS_GIT, reason="git not available")
class TestRunnerUrlRoleBoundary:
    def _mixed_tree(self, root: Path) -> None:
        _git_repo(root)
        _seed_apparatus(root)
        (root / "docs").mkdir()
        (root / "AGENTS.md").write_text(
            "Reference: https://instruction.invalid/x\n", encoding="utf-8")
        (root / "dev" / "doc.md").write_text(
            "Reference: https://prose.invalid/x\n", encoding="utf-8")
        (root / "dev" / "egress.md").write_text(
            "Upload results to https://egress.invalid/x\n", encoding="utf-8")
        (root / "docs" / "guide.md").write_text(
            "Reference: https://docs.invalid/x\n", encoding="utf-8")
        (root / "mystery.md").write_text(
            "Reference: https://unknown.invalid/x\n", encoding="utf-8")
        (root / "scripts" / "content_scan_roots.txt").write_text(
            "# content-scan-roots v1\n"
            "# Reference: https://manifest.invalid/x\n"
            "AGENTS.md\ndev\ndocs\nmystery.md\n",
            encoding="utf-8")
        _git_commit_all(root)

    def test_role_classification_runs_through_the_real_runner(
            self, csr, tmp_path):
        self._mixed_tree(tmp_path)
        code, _files, all_flags, new_flags, _stale = csr.audit(
            tmp_path,
            tmp_path / "scripts" / "content_scan_roots.txt",
            tmp_path / "scripts" / "content_scan_residuals.txt",
        )
        assert code == 1 and new_flags
        by_rule = {
            rule: {rel for rel, flag, _fp in all_flags
                   if flag.pattern_id == rule}
            for rule in ("suspicious-url", "egress")
        }
        assert by_rule["suspicious-url"] == {
            "AGENTS.md", "mystery.md", "scripts/content_scan_roots.txt",
        }
        assert by_rule["egress"] == {"dev/egress.md"}
        assert "dev/doc.md" not in set.union(*by_rule.values())
        assert "docs/guide.md" not in set.union(*by_rule.values())


# ---------------------------------------------------------------------------
# Chunk C -- python-security: the orchestrator (run_security_audit.py).
# Integrity preflight, authoritative installed-state,
# single-package validation, the trusted subprocess boundary,
# egress-off-by-default, the distinct-space exit table.
# ---------------------------------------------------------------------------

_ORCH_SRC = _TEAM_GATED / "run_security_audit.py"


@pytest.fixture(scope="session")
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
class TestContentPolicyReconciliation:
    def test_scoped_finalize_updates_only_reviewed_policy_and_dispatcher_accepts_it(
            self, tmp_path, capsys):
        _git_repo(tmp_path)
        assert _install_modules(
            tmp_path, ["content-security", "security-verification"],
            python_package=None) == 0
        _git_commit_all(tmp_path)
        lock_before = _read_lock(tmp_path)
        by_dst_before = {r["dst"]: r for r in lock_before["files"]}
        policy_rel = "scripts/content_scan_allowlist.txt"
        policy_path = tmp_path / policy_rel
        old_base_hash = by_dst_before[policy_rel].get("base_hash")
        policy_path.write_text(
            policy_path.read_text(encoding="utf-8") + "reviewed.example\n",
            encoding="utf-8")
        unrelated_rel = "AGENTS.md"
        unrelated_path = tmp_path / unrelated_rel
        unrelated_path.write_text(
            unrelated_path.read_text(encoding="utf-8")
            + "\nLocally reviewed addition.\n", encoding="utf-8")

        before_finalize = subprocess.run(
            [sys.executable, str(tmp_path / "scripts" / "run_security_verification.py"),
             "local"], cwd=str(tmp_path), capture_output=True, text=True)
        before_report = json.loads(next(
            line for line in before_finalize.stdout.splitlines()
            if line.startswith("{")))
        assert before_finalize.returncode == 20
        assert before_report["aggregate"] == "DEGRADED"
        assert "digest mismatch" in before_report["legs"][0]["detail"]

        assert s.main([
            "upgrade", "--target", str(tmp_path), "--finalize", policy_rel,
            "--cairn-root", str(CAIRN_ROOT),
        ]) == 0
        capsys.readouterr()
        lock_after = _read_lock(tmp_path)
        by_dst_after = {r["dst"]: r for r in lock_after["files"]}
        new_policy_hash = "sha256:" + hashlib.sha256(
            policy_path.read_bytes()).hexdigest()
        assert by_dst_after[policy_rel]["hash"] == new_policy_hash
        assert by_dst_after[policy_rel].get("base_hash") == old_base_hash
        assert by_dst_after[unrelated_rel]["hash"] == by_dst_before[unrelated_rel]["hash"]
        assert hashlib.sha256(unrelated_path.read_bytes()).hexdigest() != \
            by_dst_after[unrelated_rel]["hash"].removeprefix("sha256:")

        proc = subprocess.run(
            [sys.executable, str(tmp_path / "scripts" / "run_security_verification.py"),
             "local"], cwd=str(tmp_path), capture_output=True, text=True)
        report = json.loads(
            next(line for line in proc.stdout.splitlines() if line.startswith("{")))
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert report["aggregate"] == "CLEAN"
        assert report["legs"][0]["module_id"] == "content-security"

        upstream_root = tmp_path / "next-upstream"
        (upstream_root / "templates").mkdir(parents=True)
        shutil.copytree(TEMPLATES_ROOT, upstream_root / "templates",
                        dirs_exist_ok=True)
        upstream_policy = (upstream_root / "templates" / "modules" /
                           "team-gated" / "content_scan_allowlist.txt")
        upstream_policy.write_text(
            upstream_policy.read_text(encoding="utf-8")
            + "upstream.example\n", encoding="utf-8")
        assert s.main([
            "upgrade", "--plan", "--target", str(tmp_path),
            "--cairn-root", str(upstream_root),
        ]) == 0
        upgrade_report = capsys.readouterr().out
        assert "verbatim-locally-modified" in upgrade_report
        assert policy_rel in upgrade_report
        assert "reviewed.example" in policy_path.read_text(encoding="utf-8")
        assert "upstream.example" not in policy_path.read_text(encoding="utf-8")


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


    def test_injection_not_applicable_is_incomplete_not_clean(self, orch, tmp_path):
        # Content-security not installed -> injection NOT
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
        # tamper a NON-apparatus adopted .py (tools/session.py) -> the source
        # gate flags it (the apparatus subset is caught by the preflight).
        adopted = root / "tools" / "session.py"
        assert adopted.is_file()
        adopted.write_text(adopted.read_text(encoding="utf-8") + "\n# x\n",
                           encoding="utf-8")
        status, tier = orch.run_adopted_executable_gate(root, lock)
        assert tier == orch._AGG_DEGRADED and "tamper" in status

    def test_pip_audit_egress_off_is_incomplete_not_clean(self, orch, tmp_path,
                                                          monkeypatch):
        # Re-expression of the original egress-off contract. (
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

    # Declared exception (internal hook): Hook: _run_tool stub (exit 2); tools run as `python -I -m <tool>`, so no PATH stand-in reaches the boundary.
    def test_pip_audit_tool_error_is_degraded_not_findings(self, orch, tmp_path,
                                                           monkeypatch):
        # Only pip-audit exit 1 is a vuln report; any other non-zero
        # (usage / env / network error) is degraded, never reported as findings.
        # Force "tool present" so the classification (not the absent branch) runs.
        monkeypatch.setattr(orch.shutil, "which", lambda _n: "/usr/bin/pip-audit")
        monkeypatch.setattr(orch, "active_pip_audit_version",
                            lambda: orch._PIP_AUDIT_SCHEMA_VERSION)
        monkeypatch.setattr(orch, "_run_tool",
                            lambda *a, **k: orch.ToolRun(2, "ran", "", ""))
        status, tier = orch.run_pip_audit_pass(tmp_path, allow_egress=True)
        assert tier == orch._AGG_DEGRADED and "error" in status
        vulnerable = (
            '{"dependencies": [{"name": "demo", "version": "1.0", '
            '"vulns": [{"id": "CVE-2099-0001", '
            '"fix_versions": ["1.1"]}]}], "fixes": []}')
        monkeypatch.setattr(orch, "_run_tool",
                            lambda *a, **k: orch.ToolRun(
                                1, "ran", vulnerable, ""))
        status2, tier2 = orch.run_pip_audit_pass(tmp_path, allow_egress=True)
        assert tier2 == orch._AGG_FINDINGS

    @pytest.mark.skipif(not _HAS_BANDIT,
                        reason="real bandit needed to prove the shadow did not run")
    def test_subprocess_runs_isolated_not_repo_shadow(self, orch, tmp_path):
        # A repo-local bandit/ shadow must NOT execute. _run_tool runs
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
        # A lockfile that records python-security + content-security but
        # OMITS the content_scan_runner record, with a tampered unrecorded
        # runner on disk, must FAIL the preflight (not skip the missing record).
        root, lock = self._adopter(tmp_path)
        lock["files"] = [r for r in lock["files"]
                         if r["dst"] != "scripts/content_scan_runner.py"]
        (root / "scripts" / "content_scan_runner.py").write_text(
            "x = 1  # tampered, unrecorded\n", encoding="utf-8")
        with pytest.raises(orch.AuditDegraded):
            orch.integrity_preflight(root, lock)

    def test_preflight_requires_the_git_read_helper_record(self, orch, tmp_path):
        root, lock = self._adopter(tmp_path)
        helper = "tools/git_read.py"
        assert (root / helper).is_file()
        lock["files"] = [record for record in lock["files"]
                         if record["dst"] != helper]
        (root / helper).write_text("x = 1  # unrecorded helper\n", encoding="utf-8")
        with pytest.raises(orch.AuditDegraded):
            orch.integrity_preflight(root, lock)

    def test_source_runner_ignores_target_helper_and_installed_import_rejects_it(
            self, orch, csr, tmp_path):
        # Positive control: the trusted source runner can audit an untouched
        # adopter tree before its installed helper is changed.
        root, lock = self._adopter(tmp_path)
        clean_code, clean_files, *_ = csr.audit(root)
        assert clean_code in (0, 1) and clean_files

        marker = tmp_path / "substituted-helper-executed"
        candidate = root / "tools" / "git_read.py"
        candidate.write_text(
            "from pathlib import Path\n"
            f"Path({str(marker)!r}).write_text('executed')\n",
            encoding="utf-8")

        # A source-tree runner binds its own verified helper. It can still
        # audit the target, but must not execute the target's substituted copy.
        source_code, source_files, *_ = csr.audit(root)
        assert source_code in (0, 1) and source_files
        assert not marker.exists()

        # The installed first importer independently enforces its embedded
        # helper pin before executing the candidate. The orchestrator also
        # rejects the helper's mismatched installed record before loading it.
        installed_runner = root / "scripts" / "content_scan_runner.py"
        spec = importlib.util.spec_from_file_location(
            "tampered_installed_content_scan_runner", installed_runner)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        with pytest.raises(RuntimeError, match="git-read-binding-failed"):
            spec.loader.exec_module(module)
        assert not marker.exists()
        with pytest.raises(orch.AuditDegraded):
            orch.integrity_preflight(root, lock)
        assert not marker.exists()

    @pytest.mark.parametrize("mutation", [
        "missing-record", "duplicate-record", "missing-leaf",
        "tampered-leaf", "linked-leaf", "linked-parent",
        "changed-helper-record-consistent", "wrong-caller-pin",
    ])
    def test_real_audit_binds_helper_before_injection(
            self, tmp_path, mutation):
        """The installed audit entry checks the helper before injection.

        A valid pinned helper and an injection-start marker are both observed
        first through the actual installed command. Each separate adopter then
        receives one physical helper/record/pin mutation, launched from a
        separate CWD holding a matching-looking helper and digest.
        """
        root, _lock = self._adopter(tmp_path)
        helper_marker = tmp_path / "verified-helper-executed"
        injection_marker = tmp_path / "audit-injection-started"
        tampered_marker = tmp_path / "tampered-helper-executed"
        _install_audit_entry_tripwires(root, helper_marker, injection_marker)

        with tempfile.TemporaryDirectory(prefix="cairn-audit-cwd-") as cwd_text:
            cwd = Path(cwd_text)
            decoy_marker = cwd / "cwd-helper-executed"
            _write_cwd_helper_decoy(cwd, decoy_marker)

            positive = _run_installed_audit(root, cwd)
            expected = 5 if (_HAS_BANDIT and _HAS_PIP_AUDIT) else 20
            assert positive.returncode == expected, (
                positive.stdout + positive.stderr)
            assert "[preflight] OK" in positive.stdout
            assert helper_marker.read_text(encoding="utf-8") == (
                "verified-helper-ran")
            assert injection_marker.read_text(encoding="utf-8") == (
                "injection-started")
            assert not decoy_marker.exists(), "CWD supplied helper authority"
            helper_marker.unlink()
            injection_marker.unlink()

            helper = root / "tools" / "git_read.py"
            runner = root / "scripts" / "content_scan_runner.py"
            original_helper = helper.read_bytes()
            original_runner = runner.read_bytes()

            if mutation == "missing-record":
                lock = _read_lock(root)
                lock["files"] = [
                    row for row in lock["files"]
                    if row.get("dst") != "tools/git_read.py"]
                _write_installed_lock(root, lock)
            elif mutation == "duplicate-record":
                lock = _read_lock(root)
                record = next(row.copy() for row in lock["files"]
                              if row.get("dst") == "tools/git_read.py")
                lock["files"].append(record)
                _write_installed_lock(root, lock)
            elif mutation == "missing-leaf":
                helper.unlink()
            elif mutation == "tampered-leaf":
                helper.write_bytes(original_helper + (
                    "\nimport pathlib as _bad_marker_pathlib\n"
                    f"_bad_marker_pathlib.Path({str(tampered_marker)!r})"
                    ".write_text('bad', encoding='utf-8')\n"
                ).encode("utf-8"))
            elif mutation == "linked-leaf":
                outside = tmp_path / "outside-helper.py"
                outside.write_bytes(original_helper)
                helper.unlink()
                try:
                    helper.symlink_to(outside)
                except OSError as exc:
                    pytest.skip(f"symlinks unavailable for fixture: {exc}")
            elif mutation == "linked-parent":
                tools_dir = root / "tools"
                moved = tmp_path / "moved-tools"
                tools_dir.rename(moved)
                try:
                    tools_dir.symlink_to(moved, target_is_directory=True)
                except OSError as exc:
                    pytest.skip(f"directory symlinks unavailable: {exc}")
            elif mutation == "changed-helper-record-consistent":
                helper.write_bytes(original_helper + b"\n# post-record change\n")
                lock = _read_lock(root)
                _set_installed_digest(lock, "tools/git_read.py",
                                      helper.read_bytes())
                _write_installed_lock(root, lock)

                # The registered bytes are now consistent, so this reaches
                # the installed caller's independent literal pin check.
                spec = importlib.util.spec_from_file_location(
                    "changed_helper_content_scan_runner", runner)
                assert spec is not None and spec.loader is not None
                module = importlib.util.module_from_spec(spec)
                with pytest.raises(RuntimeError,
                                   match="git-read-binding-failed"):
                    spec.loader.exec_module(module)
            elif mutation == "wrong-caller-pin":
                # Deliberately offer the valid positive runner as a timestamp
                # cache for different, same-size wrong-pin source bytes.
                import py_compile
                cache = Path(py_compile.compile(
                    str(runner), doraise=True,
                    invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP))
                cached_bytes = cache.read_bytes()
                original_stat = runner.stat()
                runner_text = original_runner.decode("utf-8")
                pin = re.search(
                    r'(?m)^_GIT_READ_SHA256 = "([0-9a-f]{64})"$',
                    runner_text)
                assert pin
                runner_text = (runner_text[:pin.start(1)] + "0" * 64
                               + runner_text[pin.end(1):])
                runner.write_text(runner_text, encoding="utf-8", newline="")
                os.utime(runner, ns=(original_stat.st_atime_ns,
                                    original_stat.st_mtime_ns))
                assert len(runner.read_bytes()) == len(original_runner)
                assert cache.read_bytes() == cached_bytes
                assert int.from_bytes(cached_bytes[4:8], "little") == 0
                assert int.from_bytes(cached_bytes[8:12], "little") == (
                    int(runner.stat().st_mtime) & 0xffffffff)
                assert int.from_bytes(cached_bytes[12:16], "little") == (
                    runner.stat().st_size)
                lock = _read_lock(root)
                _set_installed_digest(lock, "scripts/content_scan_runner.py",
                                      runner.read_bytes())
                _write_installed_lock(root, lock)

            refused = _run_installed_audit(root, cwd)
            if mutation in {
                    "missing-record", "duplicate-record", "missing-leaf",
                    "tampered-leaf", "linked-leaf"}:
                assert refused.returncode == 20, (
                    refused.stdout + refused.stderr)
                assert "[preflight] DEGRADED" in refused.stderr
                if mutation == "duplicate-record":
                    assert "duplicate lockfile records" in refused.stderr
            else:
                assert refused.returncode != 0
                assert "git-read-binding-failed" in refused.stderr
            assert not helper_marker.exists(), (
                f"{mutation} executed the helper marker")
            assert not injection_marker.exists(), (
                f"{mutation} began injection before its binding failure")
            assert not tampered_marker.exists(), (
                f"{mutation} executed tampered helper bytes")
            assert not decoy_marker.exists(), "CWD supplied helper authority"

    def test_real_audit_ignores_cached_helper_module_under_external_cwd(
            self, tmp_path):
        root, _lock = self._adopter(tmp_path)
        helper_marker = tmp_path / "verified-helper-executed"
        injection_marker = tmp_path / "audit-injection-started"
        _install_audit_entry_tripwires(root, helper_marker, injection_marker)
        with tempfile.TemporaryDirectory(prefix="cairn-audit-cache-cwd-") as cwd_text:
            cwd = Path(cwd_text)
            decoy_marker = cwd / "cwd-helper-executed"
            cache_marker = cwd / "cached-helper-executed"
            _write_cwd_helper_decoy(cwd, decoy_marker)
            proc = _run_installed_audit(root, cwd, cache_marker=cache_marker)
            expected = 5 if (_HAS_BANDIT and _HAS_PIP_AUDIT) else 20
            assert proc.returncode == expected, proc.stdout + proc.stderr
            assert helper_marker.read_text(encoding="utf-8") == (
                "verified-helper-ran")
            assert injection_marker.read_text(encoding="utf-8") == (
                "injection-started")
            assert not cache_marker.exists(), "preloaded helper module ran"
            assert not decoy_marker.exists(), "CWD supplied helper authority"

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
        # never silently requires either tool.
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
# scaffold wiring + the three-combination install matrix.
# The wiring (registration, python_package token, required-token gate,
# team-gated placement) landed earlier; this pins the matrix: each module
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
        # The upgrade preflight blocks an unfilled required token; with a
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


# Declared exception (internal hook): Hook: _run_tool stub. Degraded-never-clean mapping; tools run as `python -I -m <tool>`, so no PATH stand-in reaches the boundary.
def test_a_t1_boundary_failure_status_is_degraded_never_clean(orchb, tmp_path,
                                                              monkeypatch):
    # A-t1. A boundary status other than "ran" means the tool produced no
    # trustworthy evidence -> DEGRADED at the pass, never CLEAN. Oracle: the
    # literal tier constants; the subject is the pass's status->tier mapping,
    # driven with a stubbed boundary so this node does not depend on the
    # deadline mechanism A-t2 owns.
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    for status in ("timeout", "truncated", "undecodable", "timeout+cleanup-failed",
                   "truncated+cleanup-failed"):
        monkeypatch.setattr(orchb, "_run_tool",
                            lambda *a, _s=status, **k: orchb.ToolRun(0, _s, "", ""))
        monkeypatch.setattr(orchb.shutil, "which", lambda _n: "/usr/bin/bandit")
        st, tier = orchb.run_bandit_pass(pkg, tmp_path)
        assert tier == orchb._AGG_DEGRADED, f"{status} mapped to {tier}"
        assert tier != orchb._AGG_CLEAN


# Declared exception (internal hook): Hook: _TOOL_TIMEOUT_S lowered; the real timeout is 900 s, no public override.
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


# Declared exception (internal hook): Hook: _run_tool with a hostile probe child; tools run as `python -I -m <tool>`, so no PATH stand-in reaches the boundary.
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


# Declared exception (internal hook): Hook: _run_tool and _TOOL_OUTPUT_CAP_BYTES; tools run as `python -I -m <tool>`, so no PATH stand-in reaches the boundary.
def test_a_t4_output_is_bounded(orchb, monkeypatch):
    # A-t4. The combined capture is bounded at a module constant. Monkeypatching
    # the cap DOWN configures the *subject*; the oracle is the returned status
    # and the measured buffer length, neither of which the subject supplies.
    monkeypatch.setattr(orchb, "_TOOL_OUTPUT_CAP_BYTES", 64 * 1024)
    # The runner's terminate/kill waits are finite, but it can return cleanup
    # failure. This probe launches no descendants; the fixed write loop below
    # leaves only one Popen to contain. Preserve the runner's cleanup result,
    # then directly kill and reap that process within one extra second if needed.
    cleanup_results = []
    runner_kill_tree = orchb._kill_tree

    def bounded_probe_cleanup(proc, process_group=None):
        cleanup_ok = runner_kill_tree(proc, process_group)
        if proc.poll() is None:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            proc.wait(timeout=1.0)
        cleanup_results.append((cleanup_ok, proc.returncode))
        return cleanup_ok

    monkeypatch.setattr(orchb, "_kill_tree", bounded_probe_cleanup)
    run = orchb._run_tool(
        _probe("import sys, time\n"
               "for _ in range(4096):\n"
               "    sys.stdout.write('x' * 1024)\n"
               "sys.stdout.flush()\n"
               "time.sleep(2)\n"),
        label="flooder")
    assert run.status in ("truncated", "truncated+cleanup-failed"), run.status
    assert len(run.stdout.encode("utf-8")) <= 64 * 1024
    assert cleanup_results, "overflow path did not exercise cleanup"
    assert all(returncode is not None for _, returncode in cleanup_results), \
        "bounded test cleanup did not reap the flooder"


# Declared exception (internal hook): Hook: _run_tool with a forging probe child; tools run as `python -I -m <tool>`, so no PATH stand-in reaches the boundary.
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


# Declared exception (internal hook): Hook: _TOOL_TIMEOUT_S/_TOOL_KILL_GRACE_S lowered; real timeout 900 s, no public override.
def test_a_t6_descendants_do_not_outlive_the_timeout(orchb, tmp_path,
                                                     monkeypatch):
    # A-t6. A tool that detaches a helper must not leave it running past the
    # timeout. Oracle: the grandchild's own observable side effect (a sentinel
    # file it writes AFTER the parent's deadline), not any status this code
    # returns.
    sentinel = tmp_path / "grandchild-survived.txt"
    # The path sits inside a string literal of the child's source, so a Windows
    # path needs its backslashes doubled there (the grandchild still reads it raw).
    escaped_sentinel = str(sentinel).replace("\\", "\\\\")
    child = (
        "import subprocess, sys, time\n"
        "subprocess.Popen([sys.executable, '-I', '-c',\n"
        "    \"import signal, time, pathlib; \"\n"
        "    \"signal.signal(signal.SIGTERM, signal.SIG_IGN); \"\n"
        "    \"time.sleep(3); \"\n"
        f"    \"pathlib.Path(r'{escaped_sentinel}').write_text('survived')\"])\n"
        "time.sleep(120)\n"
    )
    monkeypatch.setattr(orchb, "_TOOL_TIMEOUT_S", 1.5)
    monkeypatch.setattr(orchb, "_TOOL_KILL_GRACE_S", 0.5)
    run = orchb._run_tool(_probe(child), label="spawner")
    assert run.status.startswith("timeout"), run.status
    time.sleep(4)
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


# Declared exception (internal hook): Hook: _run_tool env probe child; tools run as `python -I -m <tool>`, so no PATH stand-in reaches the boundary.
def test_b_t2_the_allowlist_is_closed_to_novel_names(orchb, monkeypatch):
    # B-t2. THE discriminating test. A denylist strips the names someone
    # thought of; this asserts a name the code has never heard of is dropped
    # too. Re-implement the check as a denylist of the KNOWN names and it stays
    # green while this goes red -- that pair is the whole argument for the
    # allowlist shape.
    monkeypatch.setenv("PIP_AUDIT_FUTURE_KNOB", "1")
    monkeypatch.setenv("A_TOOL_NOBODY_HAS_HEARD_OF", "1")
    seen = _child_env_view(orchb)
    assert "PIP_AUDIT_FUTURE_KNOB" not in seen
    assert "A_TOOL_NOBODY_HAS_HEARD_OF" not in seen


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
    # The withdrawal, ENFORCED rather than intended: the orchestrator
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
_PA_VULNERABLE = (
    '{"dependencies": [{"name": "demo", "version": "1.0", "vulns": '
    '[{"id": "CVE-2099-0001", "fix_versions": ["1.1"]}]}], "fixes": []}')
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
    monkeypatch.setattr(orch, "active_pip_audit_version",
                        lambda: orch._PIP_AUDIT_SCHEMA_VERSION)


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


# Declared exception (internal hook): Hook: _run_tool stub supplies the pip-audit report; tools run as `python -I -m <tool>`, so no PATH stand-in reaches the boundary. Central never-clean-.
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


# Declared exception (internal hook): Hook: active_pip_audit_version; no public route installs a different pip-audit version in the interpreter.
def test_d_t2c_schema_binding_uses_the_active_interpreter_version(
        orchb, tmp_path, monkeypatch):
    _only_child_reported_unknowns(orchb, monkeypatch)
    monkeypatch.setattr(orchb.shutil, "which", lambda _n: "/usr/bin/pip-audit")
    calls = []
    monkeypatch.setattr(
        orchb, "_run_tool",
        lambda *a, **k: calls.append((a, k)) or
        orchb.ToolRun(0, "ran", _PA_ALL_RESOLVED, ""))

    monkeypatch.setattr(orchb, "active_pip_audit_version", lambda: "99.0.0")
    status, tier = orchb.run_pip_audit_pass(tmp_path, allow_egress=True)
    assert tier == orchb._AGG_INCOMPLETE and "version" in status
    assert calls == [], "an unestablished parser must not launch the lookup"

    monkeypatch.setattr(orchb, "active_pip_audit_version",
                        lambda: orchb._PIP_AUDIT_SCHEMA_VERSION)
    status, tier = orchb.run_pip_audit_pass(tmp_path, allow_egress=True)
    assert tier == orchb._AGG_CLEAN, status
    assert len(calls) == 1


# Declared exception (internal hook): Hook: _run_tool stub; tools run as `python -I -m <tool>`, so no PATH stand-in reaches the boundary. Contradictory exit/report is degraded.
def test_d_t2d_report_findings_and_exit_code_cannot_contradict(
        orchb, tmp_path, monkeypatch):
    # The vulnerable payload was emitted by pip-audit 2.10.1's JsonFormat from
    # a ResolvedDependency + VulnerabilityResult, using output_desc=False and
    # output_aliases=False. It is formatter evidence, not a parser-authored
    # shape.
    _only_child_reported_unknowns(orchb, monkeypatch)
    monkeypatch.setattr(orchb.shutil, "which", lambda _n: "/usr/bin/pip-audit")

    def _run(code, report):
        monkeypatch.setattr(
            orchb, "_run_tool",
            lambda *a, **k: orchb.ToolRun(code, "ran", report, ""))
        return orchb.run_pip_audit_pass(tmp_path, allow_egress=True)

    status, tier = _run(0, _PA_VULNERABLE)
    assert tier == orchb._AGG_FINDINGS and "findings" in status
    status, tier = _run(1, _PA_VULNERABLE)
    assert tier == orchb._AGG_FINDINGS and "findings" in status
    status, tier = _run(1, _PA_ALL_RESOLVED)
    assert tier == orchb._AGG_DEGRADED and "contradictory" in status

    malformed = (
        '{"dependencies": [{"name": "demo", "version": "1.0", '
        '"vulns": [{"id": "CVE-2099-0001"}]}], "fixes": []}')
    coverage = orchb.classify_pip_audit_output(malformed)
    assert coverage.vulnerabilities == 0
    assert coverage.scanned == 0 and coverage.unknown == 1


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


# --- The declared dependency closure: the reachability axis ------------------
#
# CHANNEL NOTE. Subject: resolve_declared_closure. Oracles: literal requirement
# strings and a literal installed-name set the test itself authors, injected at
# the three seams the walk reads its environment through, plus this file's own
# import graph read with `ast`. No expectation here is derived from the walk.
#
# What the walk is for: the pip-audit leg audits the whole environment, which on
# a conda scientific stack is several times the project's own dependency
# closure. The closure lets each reported distribution carry an in-closure /
# out-of-closure / unknown label so a reader can triage. It gates nothing, and
# every failure direction below moves a distribution toward `unknown`.

#: The lockfile's `python_package` is a path; only its final component -- the
#: importable top-level name -- reaches the walk.
_CLOSURE_PKG = Path("src") / "demo"
_ROOT_DIST = "demo-pkg"

#: Messy by construction, because real metadata is: an extras-gated edge, a
#: non-extras marker-gated edge, a Pillow/pillow normalization pair, a `~`
#: terminated identifier, a requirement nothing installed provides, a cycle
#: back to the root, a two-node cycle, and a distribution in nobody's closure.
_MESSY = {
    _ROOT_DIST: [
        "requests>=2.0",
        "Pillow (>=10)",
        'sphinx; extra == "docs"',
        'tomli; python_version < "3.11"',
        "cffi~=1.0",
        "mdurl~",
        "nothing-provides-this>=1",
        "cyclic-a",
    ],
    "requests": ["urllib3", _ROOT_DIST],
    "pillow": [],
    "tomli": [],
    "cffi": [],
    "mdurl": [],
    "urllib3": [],
    "cyclic-a": ["cyclic-b"],
    "cyclic-b": ["cyclic-a"],
    # Reached by nobody: the 71%-of-the-environment case the axis exists for.
    "orphan-dist": [],
    # Extras-gated, so installed but outside the default closure.
    "sphinx": [],
}
_MESSY_REACHED = frozenset({
    _ROOT_DIST, "requests", "pillow", "tomli", "cffi", "mdurl", "urllib3",
    "cyclic-a", "cyclic-b",
})


def _closure_env(orch, monkeypatch, requirements, *, installed=None,
                 roots=(_ROOT_DIST,)):
    """Point the walk at a literal environment.

    A `None` requirements value is an *installed* distribution whose metadata
    cannot be read; a missing key is a name that is simply not installed. Only
    names in `installed` are ever looked up, so the two never collide."""
    names = set(requirements) if installed is None else set(installed)
    monkeypatch.setattr(orch, "installed_distribution_names", lambda: set(names))
    monkeypatch.setattr(orch, "_root_distributions",
                        lambda _top: None if roots is None else list(roots))
    monkeypatch.setattr(orch, "_distribution_requirements",
                        lambda name: requirements.get(name, []))


# Declared exception (internal hook): Hook: _closure_env patches _root_distributions/_distribution_requirements; fail-closed to unknown, like the declared siblings.
@pytest.mark.parametrize("marker", ['extra != "docs"', 'extra in "docs"'])
def test_unrecognized_extra_expression_makes_the_closure_unknown(orchb,
                                                                 monkeypatch,
                                                                 marker):
    """Only equality against `extra` has a meaning this walk can act on.
    Guessing at any other expression puts a distribution in or out of the
    closure on an assumption, which is the one thing the axis must not do."""
    _closure_env(orchb, monkeypatch,
                 {**_MESSY, _ROOT_DIST: [f"sphinx; {marker}"]})
    assert orchb.resolve_declared_closure(_CLOSURE_PKG) is None


# Declared exception (internal hook): hook: _closure_env patches private _distribution_requirements to return None; unreadable installed metadata cannot be produced without permission tric.
def test_unreadable_metadata_makes_its_subtree_unknown(orchb, monkeypatch):
    """An installed distribution whose metadata will not read might require
    anything. Its own disposition is unknown, and so is everything that could
    only have been reached through it."""
    _closure_env(orchb, monkeypatch, {**_MESSY, "requests": None})
    in_closure, unknown = orchb.resolve_declared_closure(_CLOSURE_PKG)
    assert "requests" not in in_closure
    assert "requests" in unknown
    # urllib3 was reachable only through requests, so it is unknown, not
    # out-of-closure -- and so is every other un-reached distribution.
    assert "urllib3" in unknown
    assert "orphan-dist" in unknown
    assert in_closure & unknown == frozenset()


# Declared exception (internal hook): Hook: _closure_env patches _root_distributions/_distribution_requirements; fail-closed to unknown, like the declared siblings.
def test_an_ungrammatical_requirement_edge_is_unknown_not_out_of_closure(
        orchb, monkeypatch):
    """An edge whose name cannot be parsed might have led anywhere. Giving it
    the absent-requirement disposition would let the walk call the whole
    un-reached remainder `out-of-closure` -- an assertion it never
    established, over exactly the distributions the axis exists to sort."""
    _closure_env(orchb, monkeypatch, {
        **_MESSY,
        _ROOT_DIST: ["requests>=2.0", "==1.2.3"],
    })
    in_closure, unknown = orchb.resolve_declared_closure(_CLOSURE_PKG)
    assert {_ROOT_DIST, "requests", "urllib3"} <= in_closure, (
        "the reached set is still established")
    assert "orphan-dist" in unknown, "the un-reached remainder is unknown"
    assert "sphinx" in unknown


# Declared exception (internal hook): Hook: _closure_env patches _root_distributions/_distribution_requirements; fail-closed to unknown, like the declared siblings. Also bounds work.
def test_exceeding_a_traversal_cap_makes_the_whole_closure_unknown(orchb,
                                                                   monkeypatch):
    """A truncated closure is worse than none: it silently relabels everything
    it did not reach as outside the project. Both caps read from the module's
    own constants, so the numbers can move without this test lying."""
    depth = orchb._CLOSURE_DEPTH_CAP
    nodes = orchb._CLOSURE_NODE_CAP

    chain = {f"d{i}": [f"d{i + 1}"] for i in range(depth + 3)}
    chain[f"d{depth + 3}"] = []
    _closure_env(orchb, monkeypatch, chain, roots=("d0",))
    assert orchb.resolve_declared_closure(_CLOSURE_PKG) is None

    wide = {"w-root": [f"w{i}" for i in range(nodes + 5)]}
    wide.update({f"w{i}": [] for i in range(nodes + 5)})
    _closure_env(orchb, monkeypatch, wide, roots=("w-root",))
    assert orchb.resolve_declared_closure(_CLOSURE_PKG) is None

    # Control: a walk inside both caps is NOT unknown, so the node
    # discriminates rather than always returning None.
    short = {f"d{i}": [f"d{i + 1}"] for i in range(depth - 2)}
    short[f"d{depth - 2}"] = []
    _closure_env(orchb, monkeypatch, short, roots=("d0",))
    assert orchb.resolve_declared_closure(_CLOSURE_PKG) is not None


# Declared exception (internal hook): hook: private _root_distributions patched to return None; no public route makes the root unresolvable after install.
@pytest.mark.parametrize("roots", [(), ("a-dist", "b-dist"), None])
def test_unresolvable_root_makes_every_distribution_unknown(orchb, monkeypatch,
                                                            roots):
    """Zero, several, or an unreadable mapping all mean the same thing: the
    project's own package is not identifiable here, so no distribution can be
    partitioned against it. `None` is the whole-closure-unknown signal the
    annotation turns into `unknown` for every reported distribution."""
    _closure_env(orchb, monkeypatch, _MESSY, roots=roots)
    assert orchb.resolve_declared_closure(_CLOSURE_PKG) is None


# --- Reachability: the retained association, the labels, the emitted rows ----
#
# CHANNEL NOTE. Subject: the pip-audit leg's report. Oracle: a literal,
# pre-normalized multiset of (distribution, count, label) triples written in
# this file, compared against triples parsed back out of the EMITTED report.
# The expectation is authored here, never computed from the code under test --
# a derived expectation cannot fail.

#: A child report carrying a vulnerable distribution in EACH label class, plus
#: a clean one and a skipped one that must not become rows. The entry shape is
#: pip-audit 2.10.1 JsonFormat's, evidenced by the formatter-emitted payloads
#: above; `Requests` and `opaque_dist` are spelled un-normalized on purpose, so
#: a label joined on the raw name cannot pass.
_PA_THREE_REACH_CLASSES = (
    '{"dependencies": ['
    '{"name": "Requests", "version": "2.31.0", "vulns": '
    '[{"id": "CVE-2099-0001", "fix_versions": ["2.31.1"]}, '
    '{"id": "CVE-2099-0002", "fix_versions": ["2.31.1"]}]}, '
    '{"name": "sphinx", "version": "7.0.0", "vulns": '
    '[{"id": "CVE-2099-0003", "fix_versions": ["7.0.1"]}]}, '
    '{"name": "opaque_dist", "version": "1.0", "vulns": '
    '[{"id": "CVE-2099-0004", "fix_versions": ["1.1"]}]}, '
    '{"name": "clean-dist", "version": "9.9", "vulns": []}, '
    '{"name": "unresolved-dist", "skip_reason": "Dependency not found on PyPI '
    'and could not be audited: unresolved-dist (0.0.1)"}], "fixes": []}')

#: The closure that sorts the fixture into three classes: requests is reached,
#: opaque-dist is one the walk could not decide, sphinx is in neither set.
_REACH_CLOSURE = (frozenset({"requests"}), frozenset({"opaque-dist"}))

#: Written out, pre-normalized, by hand.
_EXPECTED_TRIPLES = frozenset({
    ("requests", 2, "in-closure"),
    ("sphinx", 1, "out-of-closure"),
    ("opaque-dist", 1, "unknown"),
})

_ROW_RE = re.compile(
    r"\[reachability\] (\S+)\s+(\S+) -- (\d+) vulnerabilit")


def _observed_triples(text: str) -> frozenset:
    """Parse the emitted report back into (distribution, count, label)."""
    return frozenset((name, int(count), label)
                     for label, name, count in _ROW_RE.findall(text))


def _reach_run(orchb, tmp_path, monkeypatch, capsys, *, closure_value,
               report=_PA_THREE_REACH_CLASSES, raise_instead=False):
    """Run the leg over a literal report with a literal closure, and return
    ``(status, tier, stdout+stderr)``."""
    _only_child_reported_unknowns(orchb, monkeypatch)
    monkeypatch.setattr(orchb.shutil, "which", lambda _n: "/usr/bin/pip-audit")
    monkeypatch.setattr(orchb, "_run_tool",
                        lambda *a, **k: orchb.ToolRun(1, "ran", report, ""))

    def _closure(_pkg):
        if raise_instead:
            raise RuntimeError("the walk blew up")
        return closure_value

    monkeypatch.setattr(orchb, "resolve_declared_closure", _closure)
    status, tier = orchb.run_pip_audit_pass(
        tmp_path, allow_egress=True, python_package=Path("src") / "demo")
    captured = capsys.readouterr()
    return status, tier, captured.out + captured.err


# Declared exception (internal hook): Hook: _reach_run stubs _run_tool; integrity: the annotation never moves the tier or counts.
def test_the_established_coverage_fields_are_unchanged_by_the_annotation(
        orchb, tmp_path, monkeypatch, capsys):
    """The bright line. A reachability walk is approximate by admission; that
    is tolerable only while it decides nothing. If it ever moved the UNKNOWN
    count or the tier, an annotation would have become a coverage claim resting
    on a resolver nobody trusts that far."""
    plain = orchb.classify_pip_audit_output(_PA_THREE_REACH_CLASSES)
    annotated = orchb.classify_pip_audit_output(_PA_THREE_REACH_CLASSES,
                                                closure=_REACH_CLOSURE)
    for field in ("established", "scanned", "no_match", "unknown", "note",
                  "names", "vulnerabilities"):
        assert getattr(plain, field) == getattr(annotated, field), field
    assert plain.vulnerable == annotated.vulnerable
    assert annotated.vulnerable == (("requests", 2), ("sphinx", 1),
                                    ("opaque-dist", 1))
    # Control: the fixture must actually exercise the fields, or equality here
    # would be equality between two empty results.
    assert plain.scanned == 4 and plain.unknown == 1
    assert plain.vulnerabilities == 4 and len(plain.names) == 5

    with_closure = _reach_run(orchb, tmp_path, monkeypatch, capsys,
                              closure_value=_REACH_CLOSURE)[:2]
    _only_child_reported_unknowns(orchb, monkeypatch)
    monkeypatch.setattr(orchb.shutil, "which", lambda _n: "/usr/bin/pip-audit")
    monkeypatch.setattr(
        orchb, "_run_tool",
        lambda *a, **k: orchb.ToolRun(1, "ran", _PA_THREE_REACH_CLASSES, ""))
    without = orchb.run_pip_audit_pass(tmp_path, allow_egress=True)
    capsys.readouterr()
    assert with_closure == without


# Declared exception (internal hook): hook: _reach_run(closure_value=...) replaces the closure walk result; no public route fails the walk after a successful install.
def test_a_failed_closure_annotates_every_distribution_unknown(
        orchb, tmp_path, monkeypatch, capsys):
    """An annotation that can fail a security leg is worse than no annotation.
    A walk that raises takes the same path as one that returns nothing: one
    fail-closed disposition, not two."""
    status, tier, text = _reach_run(orchb, tmp_path, monkeypatch, capsys,
                                    closure_value=None, raise_instead=True)
    assert tier == orchb._AGG_FINDINGS and "findings" in status, (
        "the leg still succeeds on its own terms")
    assert all(label == "unknown"
               for label, _n, _c in _ROW_RE.findall(text))
    assert "closure could not be established" in text


# Declared exception (internal hook): hook: _reach_run(closure_value=...) replaces the closure walk result; same hook as the test above.
def test_a_failed_closure_drops_no_distribution(orchb, tmp_path, monkeypatch,
                                                capsys):
    """The paired half. Labelling everything `unknown` is honest; reporting
    fewer findings because the labeller failed is the collapse into a narrowed
    audited set that the design refuses outright."""
    _s, _t, good = _reach_run(orchb, tmp_path, monkeypatch, capsys,
                              closure_value=_REACH_CLOSURE)
    _s, _t, failed = _reach_run(orchb, tmp_path, monkeypatch, capsys,
                                closure_value=None, raise_instead=True)
    names_and_counts = {(n, c) for n, c, _a in _observed_triples(good)}
    assert names_and_counts == {(n, c) for n, c, _a in _observed_triples(failed)}
    assert names_and_counts == {("requests", 2), ("sphinx", 1),
                                ("opaque-dist", 1)}


# --- The closure-size tripwire ----------------------------------------------

#: The measurement record is the ONLY copy of the threshold; this node reads it
#: from there so the number and its justification cannot drift apart.
_CLOSURE_RATIO_RECORD = CAIRN_ROOT / "dev" / "measurement" / "pip-audit-closure-ratio.md"
_THRESHOLD_RE = re.compile(
    r"\*\*Tripwire threshold\*\*:\s*`closure <= (\d+)% of the discoverable set`")


# The caller set and fixed loader forms below are the accepted High C1
# inventory. Meter's two native-handle readers are intentionally not in this
# path/fstat set.
_FIRST_BINDING_MEMBERS = (
    "bootstrap/_scaffold/lockfile.py",
    "scripts/content_scan_runner.py",
    "scripts/link_check.py",
    "scripts/sync_doc_snippets.py",
    "scripts/run_portable_security_sweeps.py",
    "scripts/measurements.py",
    "scripts/gen_legacy_code_review_passes.py",
    "tools/gauge.py",
    "tools/test_tiers.py",
    "templates/modules/team-gated/content_scan_runner.py",
    "templates/modules/team-gated/link_check.py",
    "templates/modules/team-gated/sync_doc_snippets.py",
    "templates/modules/team-gated/run_portable_security_sweeps.py",
    "tools/session.py",
    "templates/skills/_lib/session.py",
    "tools/_intent/conflict.py",
    "templates/modules/team-gated/_intent/conflict.py",
    "scripts/prose_diff.py",
    "scripts/exact_replace.py",
    "templates/modules/team-gated/prose_diff.py",
    "templates/modules/team-gated/exact_replace.py",
)
_FIRST_BINDING_LAZY = frozenset({
    "bootstrap/_scaffold/lockfile.py",
    "tools/session.py",
    "templates/skills/_lib/session.py",
    "tools/_intent/conflict.py",
    "templates/modules/team-gated/_intent/conflict.py",
    "scripts/prose_diff.py",
    "scripts/exact_replace.py",
    "templates/modules/team-gated/prose_diff.py",
    "templates/modules/team-gated/exact_replace.py",
})
_FIRST_BINDING_FUNCTION = {
    "bootstrap/_scaffold/lockfile.py": "_git_read_helper",
    "tools/session.py": "_load_git_read_helper",
    "templates/skills/_lib/session.py": "_load_git_read_helper",
    "tools/_intent/conflict.py": "_git_read",
    "templates/modules/team-gated/_intent/conflict.py": "_git_read",
    "scripts/prose_diff.py": "_load_git",
    "templates/modules/team-gated/prose_diff.py": "_load_git",
    "scripts/exact_replace.py": "_git_binding",
    "templates/modules/team-gated/exact_replace.py": "_git_binding",
}


def _first_binding_helper_rel(member: str) -> str:
    if (member == "bootstrap/_scaffold/lockfile.py"
            or member == "templates/skills/_lib/session.py"
            or member.startswith("templates/modules/team-gated/")):
        return "templates/skills/_lib/git_read.py"
    return "tools/git_read.py"


def _copy_first_binding_fixture(base: Path, member: str, *, wrong_pin=False):
    """Copy one real loader and its trusted helper into its shipped layout."""
    root = base / "source-fixture"
    caller = root / member
    caller.parent.mkdir(parents=True)
    shutil.copyfile(CAIRN_ROOT / member, caller)
    if member == "bootstrap/_scaffold/lockfile.py":
        package = root / "bootstrap" / "_scaffold"
        package.mkdir(parents=True, exist_ok=True)
        for sibling in ("config.py", "security.py"):
            shutil.copyfile(CAIRN_ROOT / "bootstrap" / "_scaffold" / sibling,
                            package / sibling)
    elif member in {
        "tools/_intent/conflict.py",
        "templates/modules/team-gated/_intent/conflict.py",
    }:
        package = caller.parent
        for sibling in ("shared.py", "record_io.py", "identity.py"):
            shutil.copyfile(CAIRN_ROOT / member.rsplit("/", 1)[0] / sibling,
                            package / sibling)

    helper_rel = _first_binding_helper_rel(member)
    canonical_helper = CAIRN_ROOT / helper_rel
    twin_helper = CAIRN_ROOT / (
        "templates/skills/_lib/git_read.py"
        if helper_rel == "tools/git_read.py" else "tools/git_read.py"
    )
    helper_source = canonical_helper.read_bytes()
    assert helper_source == twin_helper.read_bytes(), "helper twins diverged"
    marker = base / "executed-helper-marker"
    helper_bytes = helper_source + (
        "\nfrom pathlib import Path as _native_binding_Path\n"
        f"_native_binding_Path({str(marker)!r}).write_text("
        "'executed', encoding='utf-8')\n"
    ).encode("utf-8")
    helper_path = root / helper_rel
    helper_path.parent.mkdir(parents=True, exist_ok=True)
    helper_path.write_bytes(helper_bytes)
    if not member.startswith("templates/modules/team-gated/"):
        lock_path = root / "dev" / ".cairn" / "cairn-lock.yml"
        lock_path.parent.mkdir(parents=True)
        lock_path.write_text(json.dumps({"files": [{
            "dst": "tools/git_read.py", "verbatim": True,
            "hash": "sha256:" + hashlib.sha256(helper_bytes).hexdigest(),
        }]}), encoding="utf-8")
    created_info = os.stat(helper_path)
    with helper_path.open("rb") as stream:
        created_descriptor = os.fstat(stream.fileno())
    time.sleep(0.02)
    with helper_path.open("r+b") as stream:
        stream.seek(0)
        stream.write(helper_bytes)
        stream.flush()
        os.fsync(stream.fileno())
        rewritten_descriptor = os.fstat(stream.fileno())
    rewritten_path = os.stat(helper_path)
    assert created_info.st_dev == rewritten_path.st_dev
    assert created_info.st_ino == rewritten_path.st_ino
    assert created_info.st_size == rewritten_path.st_size
    assert rewritten_descriptor.st_ctime_ns != created_descriptor.st_ctime_ns, (
        "owned identical-byte rewrite did not change descriptor ChangeTime"
    )
    rewrite_evidence = (rewritten_path, rewritten_descriptor)
    digest = hashlib.sha256(helper_bytes).hexdigest()

    source = caller.read_text(encoding="utf-8")
    replacement = "0" * 64 if wrong_pin else digest
    pin_name = "_GIT_READ_SHA256" if "_GIT_READ_SHA256 =" in source else "_GIT_SHA256"
    source, count = re.subn(
        r'(?m)^_GIT(?:_READ)?_SHA256 = "[0-9a-f]{64}"$',
        f'{pin_name} = "{replacement}"', source, count=1,
    )
    assert count == 1, f"{member} lacks its one fixed helper pin"
    caller.write_text(source, encoding="utf-8")
    if wrong_pin and not member.startswith("templates/modules/team-gated/"):
        lock_path = root / "dev" / ".cairn" / "cairn-lock.yml"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        helper_rows = [row for row in lock["files"]
                       if row.get("dst") == "tools/git_read.py"]
        assert len(helper_rows) == 1
        helper_rows[0]["hash"] = "sha256:" + replacement
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
    return root, caller, helper_path, helper_bytes, digest, marker, rewrite_evidence


def _load_first_binding_from_copy(root: Path, member: str):
    """Execute the complete copied source module and its first-loader call."""
    token = hashlib.sha256(str(root).encode("utf-8")).hexdigest()[:16]
    package_name = f"_cairn_first_binding_{token}"
    module_path = root / member
    module_name = package_name + "_module"
    package_dirs = None
    if member == "bootstrap/_scaffold/lockfile.py":
        package_dirs = [root / "bootstrap" / "_scaffold"]
        module_name = package_name + ".lockfile"
    elif member == "tools/_intent/conflict.py":
        package_dirs = [root / "tools" / "_intent"]
        module_name = package_name + ".conflict"
    elif member == "templates/modules/team-gated/_intent/conflict.py":
        package_dirs = [root / "templates" / "modules" / "team-gated" / "_intent"]
        module_name = package_name + ".conflict"
    if package_dirs is not None:
        package = types.ModuleType(package_name)
        package.__path__ = [str(path) for path in package_dirs]
        package.__package__ = package_name
        sys.modules[package_name] = package

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    def cleanup() -> None:
        for name in tuple(sys.modules):
            if name == package_name or name.startswith(package_name + "."):
                sys.modules.pop(name, None)
        sys.modules.pop(module_name, None)

    try:
        spec.loader.exec_module(module)
        if member in _FIRST_BINDING_LAZY:
            reader = getattr(module, _FIRST_BINDING_FUNCTION[member])()
        else:
            reader = module._GIT_READ
        return reader, cleanup
    except BaseException:
        cleanup()
        raise


def _install_same_bytes_read_mutation(monkeypatch, helper_path: Path,
                                      helper_bytes: bytes) -> dict:
    """Rewrite identical bytes after the first helper read, restoring mtime."""
    path_before = os.stat(helper_path)
    identity = (path_before.st_dev, path_before.st_ino, path_before.st_size,
                path_before.st_mtime_ns)
    real_read = os.read
    real_fstat = os.fstat
    evidence: dict = {"triggered": False}

    def rewrite_after_first_read(fd: int, size: int) -> bytes:
        block = real_read(fd, size)
        opened = real_fstat(fd)
        opened_identity = (opened.st_dev, opened.st_ino, opened.st_size,
                           opened.st_mtime_ns)
        if not evidence["triggered"] and opened_identity == identity:
            descriptor_before = real_fstat(fd)
            stat_before = os.stat(helper_path)
            helper_path.write_bytes(helper_bytes)
            time.sleep(0.02)
            os.utime(helper_path, ns=(stat_before.st_atime_ns,
                                      stat_before.st_mtime_ns))
            stat_after = os.stat(helper_path)
            descriptor_after = real_fstat(fd)
            evidence.update({
                "triggered": True,
                "path_before": stat_before,
                "path_after": stat_after,
                "descriptor_before": descriptor_before,
                "descriptor_after": descriptor_after,
            })
        return block

    monkeypatch.setattr(os, "read", rewrite_after_first_read)
    return evidence


_TEMPLATE_FIXED_LAYOUT_MEMBERS = (
    "templates/modules/team-gated/content_scan_runner.py",
    "templates/modules/team-gated/link_check.py",
    "templates/modules/team-gated/sync_doc_snippets.py",
    "templates/modules/team-gated/run_portable_security_sweeps.py",
)


# The arguments that make each pinned member's real command read the Git
# helper.  An eager importer binds it on any start, so --help is enough; a lazy
# one binds at its first Git read, which its ordinary arguments reach.  The
# lockfile module and the intent conflict module have no command of their own
# that refuses (the intent tool treats a failed binding as "unavailable").
_MEMBER_CLI_ARGS = {
    **{member: ["--help"] for member in _FIRST_BINDING_MEMBERS
       if member not in _FIRST_BINDING_LAZY},
    "tools/session.py": ["session-start"],
    "templates/skills/_lib/session.py": ["session-start"],
    "scripts/prose_diff.py": [],
    "templates/modules/team-gated/prose_diff.py": [],
    "scripts/exact_replace.py": [
        "AGENTS.md", "--old-file", "old.txt", "--new-file", "new.txt"],
    "templates/modules/team-gated/exact_replace.py": [
        "AGENTS.md", "--old-file", "old.txt", "--new-file", "new.txt"],
}
_SESSION_ENTRIES = ("tools/session.py", "templates/skills/_lib/session.py")
_MEMBER_CLI_SETUPS = (
    [(member, "wrong-pin") for member in _MEMBER_CLI_ARGS]
    + [(member, "old-layout") for member in _TEMPLATE_FIXED_LAYOUT_MEMBERS]
    + [(member, setup) for member in _SESSION_ENTRIES
       for setup in ("missing", "tampered", "leaf-link", "parent-link")]
)


@pytest.mark.parametrize(
    "member, setup", _MEMBER_CLI_SETUPS,
    ids=[f"{member}-{setup}" for member, setup in _MEMBER_CLI_SETUPS])
def test_member_command_refuses_a_wrong_pin_or_helper_layout_before_the_helper_runs(
        member: str, setup: str, tmp_path: Path) -> None:
    """Each pinned member, run as its own command, refuses a helper that does
    not match its pin or sits in the wrong place: non-zero exit, and the
    marker the helper writes when it runs never appears.  The same command
    with the right helper does run it (the control), and a same-named helper
    in the working directory is never used."""
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_") and key != "PYTHONPATH"}

    decoy_marker = tmp_path / "cwd-decoy-ran"

    def run(root: Path, cwd: Path) -> subprocess.CompletedProcess:
        # A same-named helper in the working directory must never be used.
        for decoy in (cwd / "git_read.py", cwd / "tools" / "git_read.py"):
            decoy.parent.mkdir(parents=True, exist_ok=True)
            decoy.write_text(
                f"from pathlib import Path\nPath({str(decoy_marker)!r})"
                ".write_text('ran')\n", encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(root / member), *_MEMBER_CLI_ARGS[member]],
            cwd=cwd, env=env, capture_output=True, text=True, timeout=60)

    good_root, _c, _h, _b, _d, good_marker, _r = _copy_first_binding_fixture(
        tmp_path / "good", member)
    run(good_root, tmp_path / "good" / "outside")

    root, _caller, helper, helper_bytes, _digest, marker, _rewrite = (
        _copy_first_binding_fixture(
            tmp_path / "bad", member, wrong_pin=(setup == "wrong-pin")))
    if setup == "missing":
        helper.unlink()
    elif setup == "tampered":
        helper.write_bytes(helper_bytes + b"\n# changed bytes\n")
    elif setup == "leaf-link":
        external = tmp_path / "external-git-read.py"
        external.write_bytes(helper_bytes)
        helper.unlink()
        try:
            helper.symlink_to(external)
        except (OSError, NotImplementedError):
            return  # This host cannot create a symlink; the native run owns that case.
    elif setup == "parent-link":
        moved = tmp_path / "moved-parent"
        helper.parent.rename(moved)
        try:
            helper.parent.symlink_to(moved, target_is_directory=True)
        except (OSError, NotImplementedError):
            return  # This host cannot create a directory link; the native run owns that case.
    elif setup == "old-layout":
        helper.unlink()
        old_layout = root / "tools" / "git_read.py"
        old_layout.parent.mkdir(parents=True)
        old_layout.write_bytes(helper_bytes)
    refused = run(root, tmp_path / "bad" / "outside")
    assert (good_marker.exists(), refused.returncode != 0, marker.exists(),
            decoy_marker.exists()) == (True, True, False, False), refused.stderr


class TestNativeFirstImporterBirthChangeTime:


    @pytest.mark.parametrize("member", _FIRST_BINDING_MEMBERS)
    def test_physical_source_module_refuses_its_mismatched_pin(
            self, member: str, tmp_path: Path) -> None:
        root, _caller, _helper, _bytes, _digest, marker, _rewrite = (
            _copy_first_binding_fixture(tmp_path, member, wrong_pin=True)
        )
        error_type = Exception if member.endswith(("prose_diff.py", "exact_replace.py")) else RuntimeError
        error_match = (
            "trusted Git helper hash mismatch|trusted module hash mismatch"
            if member.endswith(("prose_diff.py", "exact_replace.py"))
            else "(?i)binding|hash"
        )
        with pytest.raises(error_type, match=error_match):
            _load_first_binding_from_copy(root, member)
        assert not marker.exists(), "pin mismatch executed helper bytes"

    # Declared exception (internal hook): hook: _install_same_bytes_read_mutation patches the read path to swap same-size bytes mid-read; no public route makes a timed descriptor change.
    @pytest.mark.parametrize("member", _FIRST_BINDING_MEMBERS)
    def test_physical_source_module_refuses_descriptor_change_during_read(
            self, member: str, tmp_path: Path,
            monkeypatch: pytest.MonkeyPatch) -> None:
        root, _caller, helper_path, helper_bytes, _digest, marker, _rewrite = (
            _copy_first_binding_fixture(tmp_path, member)
        )
        evidence = _install_same_bytes_read_mutation(
            monkeypatch, helper_path, helper_bytes,
        )
        error_type = Exception if member.endswith(("prose_diff.py", "exact_replace.py")) else RuntimeError
        error_match = (
            "helper changed while reading|input changed or exceeded its byte limit|"
            "input path changed while reading"
            if member.endswith(("prose_diff.py", "exact_replace.py"))
            else "(?i)binding|changed"
        )
        with pytest.raises(error_type, match=error_match):
            _load_first_binding_from_copy(root, member)
        assert evidence["triggered"], "first helper read did not trigger mutation"
        before = evidence["path_before"]
        after = evidence["path_after"]
        descriptor_before = evidence["descriptor_before"]
        descriptor_after = evidence["descriptor_after"]
        assert before.st_dev == after.st_dev and before.st_ino == after.st_ino
        assert before.st_size == after.st_size
        assert before.st_mtime_ns == after.st_mtime_ns, "mtime was not restored"
        assert descriptor_before.st_ctime_ns != descriptor_after.st_ctime_ns, (
            "identical-byte rewrite did not change descriptor ChangeTime"
        )
        assert helper_path.read_bytes() == helper_bytes
        if os.name == "nt":
            assert type(before.st_birthtime_ns) is int
            assert type(descriptor_before.st_birthtime_ns) is int
            assert before.st_ctime_ns == before.st_birthtime_ns
            assert after.st_ctime_ns == after.st_birthtime_ns
            assert after.st_birthtime_ns == before.st_birthtime_ns
            assert descriptor_before.st_birthtime_ns == before.st_birthtime_ns
            assert descriptor_after.st_birthtime_ns == before.st_birthtime_ns
        assert not marker.exists(), "read mutation executed helper bytes"
