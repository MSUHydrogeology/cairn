"""
Tests for the fold-back-ledger module (foldback-ledger-candidates plan,
Chunk C).

Covers:
* install-path: the module doctrine lands in dev/modules/; the forkable
  ledger lands in dev/.cairn/.
* default-on: the module is in _DEFAULT_ON_MODULES and a default install
  (no `modules:` key) includes it.
* omission path: a `modules:` list that omits it leaves the ledger
  uninstalled (the documented opt-out).
* security (Plan-review P2#3): the installed ledger carries the literal
  [SECURITY WARNING] export-safety language -- test-verified, not
  human-read-only.
* mechanism scaffolding: the ledger carries the status vocabulary +
  removal rule.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Allow tests to import scaffold without installing a package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap.scaffold import (  # noqa: E402
    _DEFAULT_ON_MODULES,
    _MODULE_MAPPINGS,
    main,
)

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_ROOT = CAIRN_ROOT / "templates"

MODULE = "fold-back-ledger"
MODULE_DOC_DST = "dev/modules/fold-back-ledger.md"
LEDGER_DST = "dev/.cairn/fold-back-ledger.md"

# The literal export-safety phrase the ledger template must carry
# verbatim (Plan-review P2#3).
SECURITY_PHRASE = (
    "no secrets, credentials, internal hostnames/IPs, local paths, "
    "or proprietary domain detail"
)

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


def _scaffold(target: Path, modules: list[str] | None) -> int:
    """Scaffold into *target* via the real CLI entry point.

    *modules* None -> omit the `modules:` key entirely (default-on set);
    a list -> pin that exact selection.
    """
    cfg = target / "profile.yml"
    body = "project_name: FoldbackTest\ntest_command: pytest\n"
    if modules is not None:
        body += "modules:\n" + "".join(f"  - {m}\n" for m in modules)
    cfg.write_text(body)
    return main(
        ["--config", str(cfg), "--target", str(target),
         "--cairn-root", str(CAIRN_ROOT)]
    )


class TestRegistration:
    def test_module_is_default_on(self) -> None:
        assert MODULE in _DEFAULT_ON_MODULES

    def test_module_mapping_targets(self) -> None:
        specs = _MODULE_MAPPINGS[MODULE]
        dsts = {s.dst for s in specs}
        assert MODULE_DOC_DST in dsts
        assert LEDGER_DST in dsts


class TestInstallPath:
    def test_default_install_includes_module(self, tmp_path: Path) -> None:
        """A profile that omits `modules:` installs the default-on set,
        which now includes the fold-back ledger."""
        assert _scaffold(tmp_path, None) == 0
        assert (tmp_path / MODULE_DOC_DST).is_file()
        assert (tmp_path / LEDGER_DST).is_file()

    def test_omission_path(self, tmp_path: Path) -> None:
        """A pinned `modules:` list without fold-back-ledger leaves it
        uninstalled -- the documented opt-out."""
        assert _scaffold(tmp_path, ["reflections"]) == 0
        assert not (tmp_path / LEDGER_DST).exists()
        assert not (tmp_path / MODULE_DOC_DST).exists()


class TestLedgerContent:
    def test_security_warning_verbatim(self, tmp_path: Path) -> None:
        """Plan-review P2#3: the installed ledger carries the literal
        [SECURITY WARNING] export-safety language."""
        assert _scaffold(tmp_path, [MODULE]) == 0
        text = (tmp_path / LEDGER_DST).read_text(encoding="utf-8")
        assert "[SECURITY WARNING]" in text
        assert SECURITY_PHRASE in text

    def test_mechanism_scaffolding(self, tmp_path: Path) -> None:
        """The ledger carries the status vocabulary + removal rule so an
        adopter has the working mechanism, not just a blank file."""
        assert _scaffold(tmp_path, [MODULE]) == 0
        text = (tmp_path / LEDGER_DST).read_text(encoding="utf-8")
        # Status vocabulary present (bare-word check: `scoped` ships as
        # `scoped -> <proposal>`, so match the word, not a fixed wrapping).
        for token in ("candidate", "queued", "scoped", "synced", "dropped"):
            assert f"`{token}" in text, f"status token {token!r} missing"
        assert "Removal rule" in text
        assert "Open candidates" in text
        assert "Already synced" in text


class TestDoctrineReferenceIsCairnSource:
    """Code-review P2: the scaffold does not install Cairn's `doctrine/`
    into adopters, so any `doctrine/fold-back.md` reference in the
    *installed* fold-back files must be explicitly qualified as a Cairn
    source reference -- never a bare adopter-local path that dangles at
    the cold-start surface."""

    def test_installed_docs_qualify_doctrine_ref(self, tmp_path: Path) -> None:
        assert _scaffold(tmp_path, [MODULE]) == 0
        for dst in (MODULE_DOC_DST, LEDGER_DST):
            text = (tmp_path / dst).read_text(encoding="utf-8")
            for line in text.splitlines():
                if "doctrine/fold-back.md" in line:
                    assert "Cairn" in line, (
                        f"{dst}: bare adopter-local reference to "
                        f"doctrine/fold-back.md (doctrine/ is not installed "
                        f"into adopters); qualify it as a Cairn-source "
                        f"reference. Offending line: {line!r}"
                    )
