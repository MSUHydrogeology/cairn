"""
Tests for the Layer-1 install manifest + provenance warning (P2 Chunk 2).

* The emitted manifest matches what an actual all-modules scaffold writes
  (no drift) and every manifest source exists under templates/.
* git_provenance_warning warns on a non-tagged / dirty Cairn source,
  is silenced by --allow-dev, and degrades silently on a non-git source.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import (  # noqa: E402
    _CORE_MAPPINGS,
    _MODULE_MAPPINGS,
    format_manifest,
    git_provenance_warning,
    install_manifest,
    main,
)

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(cwd), *args],
                   check=True, capture_output=True)


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------

class TestInstallManifest:
    def test_manifest_covers_core_and_all_modules(self) -> None:
        manifest = install_manifest()  # all modules
        dsts = {dst for _src, dst, _v in manifest}
        # Every core destination is present.
        for _src, dst in _CORE_MAPPINGS:
            assert dst in dsts, f"core dst missing from manifest: {dst}"
        # Every module's every spec destination is present.
        for specs in _MODULE_MAPPINGS.values():
            for spec in specs:
                assert spec.dst in dsts, f"module dst missing: {spec.dst}"

    def test_manifest_sources_all_exist(self) -> None:
        for src, dst, _v in install_manifest():
            assert (TEMPLATES_ROOT / src).is_file(), (
                f"manifest source does not exist under templates/: {src} "
                f"(-> {dst})"
            )

    def test_manifest_matches_actual_install(self, tmp_path: Path) -> None:
        """Scaffolding every module writes exactly the manifest's
        destinations -- the no-drift guarantee."""
        all_modules = sorted(_MODULE_MAPPINGS)
        cfg = tmp_path / "profile.yml"
        cfg.write_text(
            "project_name: ManifestTest\ntest_command: pytest\nmodules:\n"
            + "".join(f"  - {m}\n" for m in all_modules)
        )
        rc = main([
            "--config", str(cfg), "--target", str(tmp_path),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
        ])
        assert rc == 0
        for _src, dst, _v in install_manifest(all_modules):
            assert (tmp_path / dst).is_file(), (
                f"manifest lists {dst} but the scaffold did not write it"
            )

    def test_manifest_cli_needs_no_config(self) -> None:
        """`--manifest` is a read-only emit -- it must not require
        --config / --target."""
        rc = main(["--manifest", "--cairn-root", str(CAIRN_ROOT)])
        assert rc == 0

    def test_format_manifest_is_stable_and_tabbed(self) -> None:
        text = format_manifest()
        body = [ln for ln in text.splitlines() if not ln.startswith("#")]
        assert body, "manifest body is empty"
        for line in body:
            parts = line.split("\t")
            assert len(parts) == 3, f"bad manifest row: {line!r}"
            assert parts[2] in ("verbatim", "substituted")
        # Sorted by destination (column 0) for diff stability.
        dsts = [ln.split("\t")[0] for ln in body]
        assert dsts == sorted(dsts)


# ---------------------------------------------------------------------------
# Provenance warning
# ---------------------------------------------------------------------------

class TestProvenanceWarning:
    def _has_git(self) -> bool:
        try:
            subprocess.run(["git", "--version"], check=True,
                           capture_output=True)
            return True
        except (OSError, subprocess.SubprocessError):
            return False

    def test_non_git_source_is_silent(self, tmp_path: Path) -> None:
        # A plain directory (no .git) must degrade silently.
        assert git_provenance_warning(tmp_path) is None

    def test_dirty_untagged_source_warns(self, tmp_path: Path) -> None:
        if not self._has_git():
            pytest.skip("git not available")
        _git(tmp_path, "init", "-q", "-b", "main")
        (tmp_path / "f.txt").write_text("hi\n")
        _git(tmp_path, "add", "-A")
        _git(tmp_path, "-c", "user.email=t@t.t", "-c", "user.name=t",
             "commit", "-qm", "init")
        # Now make it dirty (uncommitted change) -- and it has no tag.
        (tmp_path / "f.txt").write_text("changed\n")
        warning = git_provenance_warning(tmp_path)
        assert warning is not None
        assert "uncommitted changes" in warning
        assert "not a tagged release commit" in warning

    def test_clean_tagged_source_is_silent(self, tmp_path: Path) -> None:
        if not self._has_git():
            pytest.skip("git not available")
        _git(tmp_path, "init", "-q", "-b", "main")
        (tmp_path / "f.txt").write_text("hi\n")
        _git(tmp_path, "add", "-A")
        _git(tmp_path, "-c", "user.email=t@t.t", "-c", "user.name=t",
             "commit", "-qm", "release")
        _git(tmp_path, "tag", "v9.9.9")
        assert git_provenance_warning(tmp_path) is None

    def test_allow_dev_silences_warning_in_main(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """--allow-dev suppresses the warning even from a dirty/untagged
        cairn-root (the real Cairn dev tree this test runs in qualifies)."""
        target = tmp_path / "tgt"
        target.mkdir()
        cfg = tmp_path / "profile.yml"
        cfg.write_text("project_name: T\ntest_command: pytest\nmodules: []\n")
        rc = main([
            "--config", str(cfg), "--target", str(target),
            "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
        ])
        assert rc == 0
        err = capsys.readouterr().err
        assert "provenance:" not in err
