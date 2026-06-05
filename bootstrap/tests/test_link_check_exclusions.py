"""`link_check` source exclusions + `file://` skip (fold-up from the
modflow_tools retire-verify-doc-links arc, Part A).

Three behavior changes, each verified here:

* **`dev/modules/` excluded by default** -- vendored Cairn module docs whose
  links target the Cairn-install layout (always false-positive in an adopter);
  re-included with ``--include-modules``.
* **`dev/.cairn/` excluded by default** -- tool-owned machinery + the ``base/``
  upgrade-ancestor template cache; re-included with ``--include-cairn``.
* **`file://` link targets skipped** -- machine-specific reviewer links, not
  portably checkable (symmetric to the existing ``http(s)`` skip).

Both exclusions are **root-anchored** (ER1): a ``modules/`` dir nested elsewhere
(e.g. ``<package>/modules/``) is NOT over-excluded.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_link_check_exclusions.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
MODULE_PATH = CAIRN_ROOT / "templates" / "modules" / "team-gated" / "link_check.py"

pytestmark = pytest.mark.skipif(
    not MODULE_PATH.exists(), reason="link_check.py template not available"
)


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("cairn_link_check_uut", MODULE_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    # Register before exec so @dataclass can resolve cls.__module__.
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


lk = _load()


# --- filter_sources: root-anchored exclusions + opt-ins ----------------------

_ROOT = Path("/repo")
_FILES = [
    _ROOT / "dev" / "modules" / "claim-check.md",
    _ROOT / "dev" / "modules" / "onboarding" / "tour.md",
    _ROOT / "dev" / ".cairn" / "base" / "dev" / "modules" / "claim-check.md",
    _ROOT / "dev" / ".cairn" / "cairn_foldback.md",
    _ROOT / "dev" / "plans" / "archive" / "old.md",
    _ROOT / "pkg" / "modules" / "user_authored.md",   # ER1: nested elsewhere
    _ROOT / "docs" / "guide.md",
    _ROOT / "AGENTS.md",
]


def _kept(**kw):
    return set(lk.filter_sources(list(_FILES), _ROOT, **kw))


def test_dev_modules_and_cairn_excluded_by_default():
    kept = _kept()
    assert _ROOT / "dev" / "modules" / "claim-check.md" not in kept
    assert _ROOT / "dev" / "modules" / "onboarding" / "tour.md" not in kept
    assert _ROOT / "dev" / ".cairn" / "cairn_foldback.md" not in kept
    assert _ROOT / "dev" / ".cairn" / "base" / "dev" / "modules" / "claim-check.md" not in kept
    assert _ROOT / "dev" / "plans" / "archive" / "old.md" not in kept  # archive unchanged


def test_root_anchored_does_not_over_exclude_nested_modules():
    # ER1: a `modules/` dir that is NOT dev/modules must stay scanned.
    assert _ROOT / "pkg" / "modules" / "user_authored.md" in _kept()
    assert _ROOT / "docs" / "guide.md" in _kept()
    assert _ROOT / "AGENTS.md" in _kept()


def test_include_opt_ins_re_include():
    assert _ROOT / "dev" / "modules" / "claim-check.md" in _kept(include_modules=True)
    assert _ROOT / "dev" / ".cairn" / "cairn_foldback.md" in _kept(include_cairn=True)
    # opt-ins are independent: --include-modules does not re-include .cairn
    assert _ROOT / "dev" / ".cairn" / "cairn_foldback.md" not in _kept(include_modules=True)


# --- file:// skip ------------------------------------------------------------


def _check(md: Path, root: Path):
    text = md.read_text(encoding="utf-8")
    flags, _n = lk.check_links(md, root, lk.scannable_lines(text), {})
    return flags


def test_file_scheme_target_is_skipped(tmp_path):
    md = tmp_path / "doc.md"
    md.write_text(
        "A reviewer link [src](file:///Users/someone/Code/x/scripts/y.py) here.\n",
        encoding="utf-8",
    )
    assert _check(md, tmp_path) == []  # not portably checkable -> skipped


def test_relative_links_stay_checked_alongside_file_scheme(tmp_path):
    md = tmp_path / "doc.md"
    md.write_text(
        "[ok](file:///Users/x/abs.py) but [rot](./does-not-exist.md) is real.\n",
        encoding="utf-8",
    )
    flags = _check(md, tmp_path)
    assert len(flags) == 1 and "does-not-exist.md" in flags[0].message
