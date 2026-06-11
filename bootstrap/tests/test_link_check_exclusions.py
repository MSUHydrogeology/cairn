"""`link_check` source exclusions + `file://` skip (fold-up from the
modflow_tools retire-verify-doc-links arc, Part A), plus the two
parity-with-claim_check exemptions added in the link-check-parity batch:

* **`dev/modules/` excluded by default** -- vendored Cairn module docs whose
  links target the Cairn-install layout (always false-positive in an adopter);
  re-included with ``--include-modules``.
* **`dev/.cairn/` excluded by default** -- tool-owned machinery + the ``base/``
  upgrade-ancestor template cache; re-included with ``--include-cairn``.
* **`file://` link targets skipped** -- machine-specific reviewer links, not
  portably checkable (symmetric to the existing ``http(s)`` skip).

Both exclusions are **root-anchored** (ER1): a ``modules/`` dir nested elsewhere
(e.g. ``<package>/modules/``) is NOT over-excluded.

**Parity exemptions (link-check-parity batch):**

* **(a) Balanced inline code spans** -- a Markdown file-link inside a balanced
  inline code span (backtick-delimited) is literal text and must NOT be flagged.
* **(b) ``link-check-allow`` directive** -- a listed missing target is exempted;
  an unlisted broken link in the SAME file is STILL flagged.
* **(c) Genuinely-broken local link still flags** -- protection preserved.
* **(d) Unmatched backtick safety** -- an UNMATCHED backtick line followed by a
  real broken link STILL flags (balanced-strip safety contract R2).
* **(e) Fenced code blocks remain skipped; heading anchors unaffected.**

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


# --- Parity exemptions: balanced code-span strip + link-check-allow ----------


def _check_with_text(md: Path, root: Path, text: str):
    """Helper: run check_links with link-check-allow directive support."""
    link_allow = lk.parse_link_allow_directives(text)
    flags, _n = lk.check_links(
        md, root, lk.scannable_lines(text), {}, link_allow=link_allow
    )
    return flags


# (a) A backticked Markdown file-link (balanced inline span) is NOT flagged.
def test_backtick_balanced_code_span_link_not_flagged(tmp_path):
    """A [link](missing.md) inside a balanced code span is literal -- not checked."""
    md = tmp_path / "doc.md"
    # The link target missing.md does not exist; it is inside a balanced
    # code span so it must NOT be flagged.
    md.write_text(
        "See `[example](missing.md)` for details.\n",
        encoding="utf-8",
    )
    assert _check(md, tmp_path) == []


def test_double_backtick_balanced_code_span_link_not_flagged(tmp_path):
    """Double-backtick balanced span also suppresses the link check."""
    md = tmp_path / "doc.md"
    md.write_text(
        "Use ``[foo](also-missing.md)`` syntax.\n",
        encoding="utf-8",
    )
    assert _check(md, tmp_path) == []


# (b) link-check-allow-listed cross-repo/missing link is NOT flagged;
#     an UN-listed broken local link in the same file IS still flagged.
def test_link_allow_directive_exempts_listed_target(tmp_path):
    """A link-check-allow-listed missing target is exempted."""
    md = tmp_path / "doc.md"
    md.write_text(
        "<!-- link-check-allow: ../other-repo/README.md -->\n"
        "\n"
        "See [cross-repo](../other-repo/README.md) for context.\n",
        encoding="utf-8",
    )
    flags = _check_with_text(md, tmp_path, md.read_text(encoding="utf-8"))
    assert flags == []


def test_link_allow_directive_unlisted_broken_link_still_flags(tmp_path):
    """An un-listed broken link in the SAME file is still flagged."""
    md = tmp_path / "doc.md"
    md.write_text(
        "<!-- link-check-allow: ../other-repo/README.md -->\n"
        "\n"
        "See [cross-repo](../other-repo/README.md) for context.\n"
        "But [this](unlisted-missing.md) is not exempted.\n",
        encoding="utf-8",
    )
    text = md.read_text(encoding="utf-8")
    flags = _check_with_text(md, tmp_path, text)
    assert len(flags) == 1
    assert "unlisted-missing.md" in flags[0].message


def test_link_allow_multiple_targets_comma_separated(tmp_path):
    """Multiple comma-separated targets in one directive are all exempted."""
    md = tmp_path / "doc.md"
    md.write_text(
        "<!-- link-check-allow: cross-a.md, cross-b.md -->\n"
        "\n"
        "[A](cross-a.md) and [B](cross-b.md) are both exempted.\n",
        encoding="utf-8",
    )
    text = md.read_text(encoding="utf-8")
    flags = _check_with_text(md, tmp_path, text)
    assert flags == []


# (c) A genuinely-broken LOCAL link in a live doc STILL flags (protection preserved).
def test_genuinely_broken_local_link_still_flags(tmp_path):
    """A real broken local link with NO link-check-allow directive is still caught."""
    md = tmp_path / "doc.md"
    md.write_text(
        "This [broken link](nonexistent-local.md) should be flagged.\n",
        encoding="utf-8",
    )
    flags = _check(md, tmp_path)
    assert len(flags) == 1
    assert "nonexistent-local.md" in flags[0].message


# (d) An UNMATCHED-backtick line followed by a real broken link STILL flags
#     (the balanced-strip safety -- an unmatched backtick must leave the
#     rest of the line intact, not silently eat the real link).
def test_unmatched_backtick_does_not_suppress_real_broken_link(tmp_path):
    """An unmatched opening backtick must NOT silently swallow a broken link."""
    md = tmp_path / "doc.md"
    # One opening backtick with no closing counterpart.  The balanced-strip
    # regex must NOT match this (there is no `\1` match), so the remainder
    # of the line -- including [broken](ghost.md) -- is still checked.
    md.write_text(
        "Here is ` unmatched and [broken](ghost.md) should flag.\n",
        encoding="utf-8",
    )
    flags = _check(md, tmp_path)
    assert len(flags) == 1, (
        "Unmatched backtick must not suppress the broken link; "
        f"got flags: {flags}"
    )
    assert "ghost.md" in flags[0].message


def test_unmatched_backtick_mismatched_run_does_not_suppress(tmp_path):
    """A double-open backtick closed by a single backtick is NOT balanced."""
    md = tmp_path / "doc.md"
    # `` opens a double-backtick span, ` closes with single -- NOT balanced.
    # The real link after should still be flagged.
    md.write_text(
        "Text ``unbalanced` and then [broken](vanished.md) should flag.\n",
        encoding="utf-8",
    )
    flags = _check(md, tmp_path)
    # vanished.md does not exist; must be flagged
    messages = [f.message for f in flags]
    assert any("vanished.md" in m for m in messages), (
        f"Expected vanished.md to be flagged; got: {messages}"
    )


# (e) Fenced code blocks remain skipped; heading-anchor checks are unaffected.
def test_fenced_code_block_links_remain_skipped(tmp_path):
    """Links inside fenced code blocks are NOT checked (pre-existing behaviour)."""
    md = tmp_path / "doc.md"
    md.write_text(
        "Normal prose.\n"
        "\n"
        "```\n"
        "[inside fence](totally-missing.md)\n"
        "```\n"
        "\n"
        "More prose.\n",
        encoding="utf-8",
    )
    assert _check(md, tmp_path) == []


def test_heading_anchor_check_unaffected_by_code_span_strip(tmp_path):
    """The heading-anchor check is unaffected by the code-span strip."""
    md = tmp_path / "doc.md"
    # The anchor #real-heading exists; #ghost-anchor does not.
    md.write_text(
        "## Real heading\n"
        "\n"
        "A [good anchor link](#real-heading) and a "
        "[bad anchor](#ghost-anchor) in prose.\n",
        encoding="utf-8",
    )
    flags = _check(md, tmp_path)
    assert len(flags) == 1
    assert "ghost-anchor" in flags[0].message


def test_valid_link_not_suppressed_by_code_span_strip(tmp_path):
    """A real link that exists is NOT suppressed by the code-span stripping."""
    md = tmp_path / "doc.md"
    target = tmp_path / "real.md"
    target.write_text("# Real\n", encoding="utf-8")
    md.write_text(
        "Prose `code span` and [real link](real.md) side by side.\n",
        encoding="utf-8",
    )
    assert _check(md, tmp_path) == []
