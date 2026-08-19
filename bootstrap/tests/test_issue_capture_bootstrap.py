"""Tests for the Fold 3 issue-capture label-bootstrap helpers (GitLab + GitHub).

Covers:
* Install-path: both scripts land verbatim under the ``issue-capture`` module.
* Dry-run smoke: no API calls made; output reports what would happen.
* Missing-token error: the script exits non-zero with a clear "set <VAR>"
  message when no credential is found.
* ``load_manifest`` validation: shape errors surface clearly.
* ``reconcile`` logic: create-new, exists-unchanged, drift-skip, drift-update.

Run from the cairn repo root::

    python -m pytest bootstrap/tests/test_issue_capture_bootstrap.py
"""
from __future__ import annotations

import importlib.util
import sys
import textwrap
from pathlib import Path
from types import ModuleType
from unittest import mock

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
_ISSUE_CAPTURE_DIR = TEMPLATES_ROOT / "modules" / "team-gated" / "issue-capture"
_GITLAB_SCRIPT = _ISSUE_CAPTURE_DIR / "bootstrap_gitlab_labels.py"
_GITHUB_SCRIPT = _ISSUE_CAPTURE_DIR / "bootstrap_github_labels.py"

sys.path.insert(0, str(CAIRN_ROOT))
from bootstrap.scaffold import _MODULE_MAPPINGS, main as scaffold_main  # noqa: E402

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _load(name: str, path: Path) -> ModuleType:
    if not path.exists():
        pytest.skip(f"Script not found: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Install-path: both scripts registered verbatim under issue-capture
# ---------------------------------------------------------------------------

class TestInstallPaths:
    """Both bootstrap scripts are registered verbatim in _MODULE_MAPPINGS."""

    def test_gitlab_script_registered(self) -> None:
        specs = _MODULE_MAPPINGS["issue-capture"]
        dsts = {s.dst: s for s in specs}
        assert "scripts/bootstrap_gitlab_labels.py" in dsts, (
            "bootstrap_gitlab_labels.py not registered under 'issue-capture' module"
        )
        assert dsts["scripts/bootstrap_gitlab_labels.py"].verbatim is True

    def test_github_script_registered(self) -> None:
        specs = _MODULE_MAPPINGS["issue-capture"]
        dsts = {s.dst: s for s in specs}
        assert "scripts/bootstrap_github_labels.py" in dsts, (
            "bootstrap_github_labels.py not registered under 'issue-capture' module"
        )
        assert dsts["scripts/bootstrap_github_labels.py"].verbatim is True

    def test_gitlab_script_installed_verbatim(self, tmp_path: Path) -> None:
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: TestLabels\ntest_command: pytest\nmodules:\n"
            "  - issue-capture\n"
        )
        rc = scaffold_main(
            ["--config", str(cfg), "--target", str(tmp_path),
             "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
        )
        assert rc == 0
        installed = tmp_path / "scripts" / "bootstrap_gitlab_labels.py"
        assert installed.is_file(), "bootstrap_gitlab_labels.py not installed"
        assert installed.read_bytes() == _GITLAB_SCRIPT.read_bytes(), (
            "Installed bootstrap_gitlab_labels.py differs from template"
        )

    def test_github_script_installed_verbatim(self, tmp_path: Path) -> None:
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: TestLabels\ntest_command: pytest\nmodules:\n"
            "  - issue-capture\n"
        )
        rc = scaffold_main(
            ["--config", str(cfg), "--target", str(tmp_path),
             "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]
        )
        assert rc == 0
        installed = tmp_path / "scripts" / "bootstrap_github_labels.py"
        assert installed.is_file(), "bootstrap_github_labels.py not installed"
        assert installed.read_bytes() == _GITHUB_SCRIPT.read_bytes(), (
            "Installed bootstrap_github_labels.py differs from template"
        )


# ---------------------------------------------------------------------------
# GitLab: dry-run smoke + missing-token error
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def gl():
    return _load("_cairn_gitlab_bootstrap_under_test", _GITLAB_SCRIPT)


class TestGitLabDryRun:
    """Dry-run: no subprocess calls; manifest-reading path works."""

    def _make_manifest(self, root: Path) -> Path:
        gitlab_dir = root / ".gitlab"
        gitlab_dir.mkdir(parents=True, exist_ok=True)
        mf = gitlab_dir / "labels.yml"
        mf.write_text(textwrap.dedent("""\
            - {name: bug, color: '#d73a4a', description: 'Something is broken.'}
            - {name: enhancement, color: '#a2eeef', description: 'A gap or wish.'}
        """))
        return mf

    def test_load_manifest_valid(self, tmp_path: Path, gl) -> None:
        mf = self._make_manifest(tmp_path)
        data = gl.load_manifest(mf)
        assert len(data) == 2
        assert data[0]["name"] == "bug"

    def test_load_manifest_missing(self, tmp_path: Path, gl) -> None:
        with pytest.raises(SystemExit) as exc_info:
            gl.load_manifest(tmp_path / "no-such.yml")
        assert exc_info.value.code == 2

    def test_load_manifest_not_a_list(self, tmp_path: Path, gl) -> None:
        bad = tmp_path / "bad.yml"
        bad.write_text("key: value\n")
        with pytest.raises(SystemExit) as exc_info:
            gl.load_manifest(bad)
        assert exc_info.value.code == 2

    def test_reconcile_dry_run_creates(self, tmp_path: Path, gl, capsys) -> None:
        """A label absent from the project is reported as would-create."""
        manifest = [{"name": "bug", "color": "#d73a4a", "description": "A bug."}]
        existing: list[dict] = []
        n_c, n_d, n_u = gl.reconcile(
            manifest, existing, project_id=1,
            dry_run=True, force_update=False,
        )
        out = capsys.readouterr().out
        assert n_c == 1
        assert "[dry-run] would create" in out
        assert "bug" in out

    def test_reconcile_exists_unchanged(self, tmp_path: Path, gl, capsys) -> None:
        manifest = [{"name": "bug", "color": "#d73a4a", "description": "A bug."}]
        existing = [{"name": "bug", "color": "#d73a4a", "description": "A bug.", "id": 1}]
        n_c, n_d, n_u = gl.reconcile(
            manifest, existing, project_id=1,
            dry_run=True, force_update=False,
        )
        assert n_u == 1
        assert n_c == 0
        assert n_d == 0

    def test_reconcile_drift_warn_and_skip(self, tmp_path: Path, gl, capsys) -> None:
        manifest = [{"name": "bug", "color": "#ff0000", "description": "Changed."}]
        existing = [{"name": "bug", "color": "#d73a4a", "description": "Original.", "id": 1}]
        n_c, n_d, n_u = gl.reconcile(
            manifest, existing, project_id=1,
            dry_run=True, force_update=False,
        )
        out = capsys.readouterr().out
        assert n_d == 1
        assert "WARN" in out
        assert "--force-update" in out

    def test_reconcile_force_update_dry_run(self, tmp_path: Path, gl, capsys) -> None:
        manifest = [{"name": "bug", "color": "#ff0000", "description": "Changed."}]
        existing = [{"name": "bug", "color": "#d73a4a", "description": "Original.", "id": 1}]
        n_c, n_d, n_u = gl.reconcile(
            manifest, existing, project_id=1,
            dry_run=True, force_update=True,
        )
        out = capsys.readouterr().out
        assert n_d == 1
        assert "[dry-run] would update" in out


class TestGitLabMissingToken:
    """When no glab credential exists, the script exits 2 with a clear message."""

    def test_check_auth_exits_on_missing_token(
        self, tmp_path: Path, gl, capsys, monkeypatch
    ) -> None:
        monkeypatch.delenv("GITLAB_PRIVATE_TOKEN", raising=False)
        monkeypatch.delenv("GITLAB_TOKEN", raising=False)
        # Stub out subprocess so `glab auth status` fails (simulates no credential).
        mock_result = mock.Mock()
        mock_result.returncode = 1
        with mock.patch("subprocess.run", return_value=mock_result):
            with pytest.raises(SystemExit) as exc_info:
                gl._check_auth()
        assert exc_info.value.code == 2
        err = capsys.readouterr().err
        assert "GITLAB_PRIVATE_TOKEN" in err

    def test_check_auth_passes_with_env_var(
        self, tmp_path: Path, gl, monkeypatch
    ) -> None:
        monkeypatch.setenv("GITLAB_PRIVATE_TOKEN", "test-token")
        # Should return without raising.
        gl._check_auth()

    def test_check_auth_passes_with_stored_credential(
        self, tmp_path: Path, gl, monkeypatch
    ) -> None:
        monkeypatch.delenv("GITLAB_PRIVATE_TOKEN", raising=False)
        monkeypatch.delenv("GITLAB_TOKEN", raising=False)
        mock_result = mock.Mock()
        mock_result.returncode = 0
        with mock.patch("subprocess.run", return_value=mock_result):
            # Should return without raising.
            gl._check_auth()


# ---------------------------------------------------------------------------
# GitHub: dry-run smoke + missing-token error
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def gh():
    return _load("_cairn_github_bootstrap_under_test", _GITHUB_SCRIPT)


class TestGitHubDryRun:
    """Dry-run: no subprocess calls; manifest-reading path works."""

    def _make_manifest(self, root: Path) -> Path:
        github_dir = root / ".github"
        github_dir.mkdir(parents=True, exist_ok=True)
        mf = github_dir / "labels.yml"
        mf.write_text(textwrap.dedent("""\
            - {name: bug, color: 'd73a4a', description: 'Something is broken.'}
            - {name: enhancement, color: 'a2eeef', description: 'A gap or wish.'}
        """))
        return mf

    def test_load_manifest_valid(self, tmp_path: Path, gh) -> None:
        mf = self._make_manifest(tmp_path)
        data = gh.load_manifest(mf)
        assert len(data) == 2
        assert data[0]["name"] == "bug"

    def test_reconcile_dry_run_creates(self, tmp_path: Path, gh, capsys) -> None:
        manifest = [{"name": "bug", "color": "d73a4a", "description": "A bug."}]
        existing: list[dict] = []
        n_c, n_d, n_u = gh.reconcile(
            manifest, existing, slug="owner/repo",
            dry_run=True, force_update=False,
        )
        out = capsys.readouterr().out
        assert n_c == 1
        assert "[dry-run] would create" in out

    def test_reconcile_color_normalization(self, tmp_path: Path, gh, capsys) -> None:
        """GitHub API may return color with or without '#'; normalize for comparison."""
        # Manifest uses '#' prefix; GitHub API returns without it.
        manifest = [{"name": "bug", "color": "#d73a4a", "description": "A bug."}]
        existing = [{"name": "bug", "color": "d73a4a", "description": "A bug.", "id": 1}]
        n_c, n_d, n_u = gh.reconcile(
            manifest, existing, slug="owner/repo",
            dry_run=True, force_update=False,
        )
        # After normalization these match -> unchanged.
        assert n_u == 1
        assert n_c == 0
        assert n_d == 0


class TestGitHubMissingToken:
    """When no gh credential exists, the script exits 2 with a clear message."""

    def test_check_auth_exits_on_missing_token(
        self, tmp_path: Path, gh, capsys, monkeypatch
    ) -> None:
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        mock_result = mock.Mock()
        mock_result.returncode = 1
        with mock.patch("subprocess.run", return_value=mock_result):
            with pytest.raises(SystemExit) as exc_info:
                gh._check_auth()
        assert exc_info.value.code == 2
        err = capsys.readouterr().err
        assert "GITHUB_TOKEN" in err

    def test_check_auth_passes_with_env_var(
        self, tmp_path: Path, gh, monkeypatch
    ) -> None:
        monkeypatch.setenv("GITHUB_TOKEN", "test-token")
        gh._check_auth()

    def test_check_auth_passes_with_stored_credential(
        self, tmp_path: Path, gh, monkeypatch
    ) -> None:
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        mock_result = mock.Mock()
        mock_result.returncode = 0
        with mock.patch("subprocess.run", return_value=mock_result):
            gh._check_auth()
