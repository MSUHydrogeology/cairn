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

Both exclusions are **root-anchored**: a ``modules/`` dir nested elsewhere
(e.g. ``<package>/modules/``) is NOT over-excluded.

**Parity exemptions (link-check-parity batch):**

* **(a) Balanced inline code spans** -- a Markdown file-link inside a balanced
  inline code span (backtick-delimited) is literal text and must NOT be flagged.
* **(b) ``link-check-allow`` directive** -- a listed missing target is exempted;
  an unlisted broken link in the SAME file is STILL flagged.
* **(c) Genuinely-broken local link still flags** -- protection preserved.
* **(d) Unmatched backtick safety** -- an UNMATCHED backtick line followed by a
  real broken link STILL flags (the balanced-strip safety contract).
* **(e) Fenced code blocks remain skipped; heading anchors unaffected.**

Promises:
- The scanner config grants only exact, reasoned entries; an invalid config grants nothing and disables legacy directives.
- Stale or unused config entries are reported only for sources the scan actually reads.
- dev/modules/ and dev/.cairn/ are excluded by default, and their opt-in flags re-include them.
- file:// link targets are skipped while relative links in the same file are still checked.
- A balanced inline code span hides link-like text, but an unmatched backtick never hides a real broken link.
- A link-check-allow directive exempts only the targets it lists.
- Links inside fenced code blocks are not checked.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/integration/test_link_check_exclusions.py
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MODULE_PATH = CAIRN_ROOT / "templates" / "modules" / "team-gated" / "link_check.py"
sys.path.insert(0, str(CAIRN_ROOT))
sys.path.insert(0, str(CAIRN_ROOT / 'scripts'))

from bootstrap.scaffold import main as scaffold_main  # noqa: E402
import check_cairn  # noqa: E402

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


def _write_scanner_config(root, value):
    path = root / 'dev' / '.cairn' / 'scanner-check-allow.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value if isinstance(value, str) else json.dumps(value),
                    encoding='utf-8')
    return path


def test_scanner_config_reads_exact_reasoned_entries(tmp_path):
    entry = {'source': 'docs/guide.md', 'target': '../other/guide.md',
             'reason': 'Published in a separate repository'}
    citation = {'source': 'templates/core/AGENTS.md',
                'target': 'docs/methodology/roles.md', 'reason': 'Citation'}
    _write_scanner_config(tmp_path, {'links': [entry], 'internal_refs': [citation]})
    config = lk.load_scanner_config(tmp_path)
    assert config.present and config.valid and not config.diagnostic
    assert config.links == (lk.ScannerExemption(**entry),)
    assert config.internal_refs == (lk.ScannerExemption(**citation),)


def test_scanner_config_optional_review_id_exceptions_are_exact(tmp_path):
    base = {'links': [], 'internal_refs': []}
    _write_scanner_config(tmp_path, base)
    legacy = lk.load_scanner_config(tmp_path)
    assert legacy.valid and legacy.review_ids == ()

    entry = {
        'source': 'docs/example.md', 'id': 'SR-C1',
        'context': 'Historical teaching example: (SR-C1).',
        'reason': 'The text demonstrates a review record label.',
    }
    _write_scanner_config(tmp_path, {**base, 'review_ids': [entry]})
    config = lk.load_scanner_config(tmp_path)
    assert config.valid
    assert config.review_ids == (lk.ScannerReviewIdException(**entry),)


def test_scanner_config_missing_and_unreadable_are_distinct(tmp_path):
    missing = lk.load_scanner_config(tmp_path)
    assert not missing.present and missing.valid and 'missing' in missing.diagnostic
    path = tmp_path / 'dev' / '.cairn' / 'scanner-check-allow.json'
    path.mkdir(parents=True)
    invalid = lk.load_scanner_config(tmp_path)
    assert invalid.present and not invalid.valid and invalid.diagnostic
    assert invalid.links == invalid.internal_refs == ()


def test_scanner_config_dangling_link_is_invalid(tmp_path):
    path = tmp_path / 'dev' / '.cairn' / 'scanner-check-allow.json'
    path.parent.mkdir(parents=True)
    path.symlink_to(path.parent / 'missing.json')
    config = lk.load_scanner_config(tmp_path)
    assert config.present and not config.valid and config.diagnostic
    assert config.links == config.internal_refs == ()


@pytest.mark.parametrize('raw', [
    '{',
    '{"links": [], "links": [], "internal_refs": []}',
    '{"links": [{"source": "a.md", "source": "b.md", "target": "x.md", "reason": "r"}], "internal_refs": []}',
    '{"links": {}, "internal_refs": []}',
    '{"links": [], "internal_refs": [], "other": []}',
    '{"links": [{"source": 1, "target": "x.md", "reason": "r"}], "internal_refs": []}',
    '{"links": [{"source": "a.md", "target": "*.md", "reason": "r"}], "internal_refs": []}',
    '{"links": [{"source": "../a.md", "target": "x.md", "reason": "r"}], "internal_refs": []}',
    '{"links": [{"source": "a.md", "target": "x.md", "reason": " "}], "internal_refs": []}',
    '{"links": [], "internal_refs": [{"source": "a.md", "target": "docs/methodology/", "reason": "r"}]}',
    '{"links": [{"source": "a.md", "target": "x.md", "reason": "r"}, {"source": "a.md", "target": "x.md", "reason": "other"}], "internal_refs": []}',
    '{"links": [{"source": "a.md", "target": "x.md", "reason": "r"}], "internal_refs": [false]}',
])
def test_scanner_config_invalid_file_grants_nothing(tmp_path, raw):
    _write_scanner_config(tmp_path, raw)
    config = lk.load_scanner_config(tmp_path)
    assert config.present and not config.valid and config.diagnostic
    assert config.links == config.internal_refs == ()


@pytest.mark.parametrize('entry', [
    {'source': 'docs/example.md', 'id': 'R1', 'context': '[R1] [R1]',
     'reason': 'ID is repeated in context'},
    {'source': 'docs/example.md', 'id': 'II3', 'context': '(II3)',
     'reason': 'Not a finding ID'},
    {'source': 'docs/example.md', 'id': 'R1', 'context': '[R1]\nsecond line',
     'reason': 'Context must be one line'},
    {'source': '../docs/example.md', 'id': 'R1', 'context': '[R1]',
     'reason': 'Path traversal'},
    {'source': 'docs/example.md', 'id': 'R1', 'context': '[R1]', 'reason': ' '},
])
def test_scanner_config_invalid_review_id_exception_grants_nothing(tmp_path, entry):
    _write_scanner_config(tmp_path, {
        'links': [{'source': 'docs/guide.md', 'target': 'missing.md',
                   'reason': 'Valid old namespace entry'}],
        'internal_refs': [{'source': 'templates/core/AGENTS.md',
                           'target': 'docs/methodology/roles.md',
                           'reason': 'Valid old namespace entry'}],
        'review_ids': [entry],
    })
    config = lk.load_scanner_config(tmp_path)
    assert not config.valid
    assert config.links == config.internal_refs == config.review_ids == ()


def test_scanner_config_duplicate_review_id_key_fails_closed(tmp_path):
    _write_scanner_config(
        tmp_path,
        '{"links": [], "internal_refs": [], "review_ids": [], "review_ids": []}',
    )
    config = lk.load_scanner_config(tmp_path)
    assert not config.valid and config.review_ids == ()


def test_configured_link_entry_point_preserves_other_findings(tmp_path, capsys):
    root = tmp_path / 'repo'
    root.mkdir()
    (tmp_path / 'outside.md').write_text('# Outside\n', encoding='utf-8')
    (root / 'exists.md').write_text('# Existing\n', encoding='utf-8')
    doc = root / 'a.md'
    doc.write_text('[allowed](missing.md) [sibling](missing2.md)\n'
                   '[anchor](exists.md#bad) [escape](../outside.md)\n',
                   encoding='utf-8')
    _write_scanner_config(root, {'links': [
        {'source': 'a.md', 'target': 'missing.md', 'reason': 'External source'},
        {'source': 'a.md', 'target': 'exists.md', 'reason': 'No anchor bypass'},
        {'source': 'a.md', 'target': '../outside.md', 'reason': 'No escape bypass'},
    ], 'internal_refs': []})
    assert lk.main(['--root', str(root), str(doc)]) == 1
    err = capsys.readouterr().err
    assert 'missing2.md' in err and 'exists.md#bad' in err and '../outside.md' in err
    assert '`missing.md`' not in err
    other = root / 'b.md'
    other.write_text('[broken](missing.md)\n', encoding='utf-8')
    assert lk.main(['--root', str(root), str(other)]) == 1
    assert 'missing.md' in capsys.readouterr().err
    cfg = tmp_path / 'profile.yml'
    cfg.write_text(
        'project_name: LinkTest\ntest_command: pytest\nmodules:\n'
        '  - doc-drift-prevention\n', encoding='utf-8')
    assert scaffold_main(
        ['--config', str(cfg), '--target', str(root),
         '--cairn-root', str(CAIRN_ROOT), '--allow-dev']
    ) == 0
    installed = root / 'scripts' / 'link_check.py'
    result = subprocess.run(
        [sys.executable, str(installed), '--root', str(root), str(doc)],
        cwd=root, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 1
    assert 'missing2.md' in result.stderr and 'exists.md#bad' in result.stderr
    assert '../outside.md' in result.stderr and '`missing.md`' not in result.stderr


def test_invalid_config_disables_legacy_directive_at_entry_point(tmp_path, capsys):
    doc = tmp_path / 'a.md'
    doc.write_text('<!-- link-check-allow: missing.md -->\n[link](missing.md)\n',
                   encoding='utf-8')
    assert lk.main(['--root', str(tmp_path), str(doc)]) == 0
    assert 'missing' in capsys.readouterr().err
    _write_scanner_config(tmp_path, '{bad json')
    assert lk.main(['--root', str(tmp_path), str(doc)]) == 1
    err = capsys.readouterr().err
    assert 'scanner-check-allow.json' in err and 'missing.md' in err


@pytest.mark.parametrize('review_ids', [{}, '', None, 0, False, 1.5])
def test_nonarray_review_ids_disables_configured_and_legacy_exemptions(
    tmp_path, capsys, review_ids,
):
    root = tmp_path
    link_doc = root / 'docs/guide.md'
    link_doc.parent.mkdir(parents=True)
    link_doc.write_text(
        '<!-- link-check-allow: missing.md -->\n[allowed](missing.md)\n',
        encoding='utf-8')
    template = root / 'templates/core/AGENTS.md'
    template.parent.mkdir(parents=True)
    template.write_text(
        '<!-- cairn-internal-ref-allow: docs/methodology/roles.md -->\n'
        '`docs/methodology/roles.md`\n', encoding='utf-8')
    doctrine = root / 'docs/methodology/roles.md'
    doctrine.parent.mkdir(parents=True)
    doctrine.write_text('# Roles\n', encoding='utf-8')
    config = {
        'links': [{
            'source': 'docs/guide.md', 'target': 'missing.md',
            'reason': 'The destination is published separately.',
        }],
        'internal_refs': [{
            'source': 'templates/core/AGENTS.md',
            'target': 'docs/methodology/roles.md',
            'reason': 'This template cites the separately published method.',
        }],
    }

    _write_scanner_config(root, config)
    assert lk.load_scanner_config(root).valid
    assert lk.main(['--root', str(root), str(link_doc)]) == 0
    capsys.readouterr()
    assert check_cairn.main([
        '--root', str(root), '--no-content-scan', str(template),
    ]) == 0
    capsys.readouterr()

    config['review_ids'] = review_ids
    _write_scanner_config(root, config)
    invalid = lk.load_scanner_config(root)
    assert not invalid.valid
    assert invalid.links == invalid.internal_refs == invalid.review_ids == ()

    assert lk.main(['--root', str(root), str(link_doc)]) == 1
    link_err = capsys.readouterr().err
    assert 'scanner-check-allow.json' in link_err and 'missing.md' in link_err
    assert check_cairn.main([
        '--root', str(root), '--no-content-scan', str(template),
    ]) == 1
    ref_err = capsys.readouterr().err
    assert 'scanner-check-allow.json' in ref_err
    assert 'docs/methodology/roles.md' in ref_err


def test_config_reports_stale_and_unused_only_for_scanned_sources(tmp_path, capsys):
    doc = tmp_path / 'a.md'
    doc.write_text('[used](missing.md)\n', encoding='utf-8')
    (tmp_path / 'unselected.md').write_text('# Other\n', encoding='utf-8')
    _write_scanner_config(tmp_path, {'links': [
        {'source': 'a.md', 'target': 'missing.md', 'reason': 'Used'},
        {'source': 'a.md', 'target': 'old.md', 'reason': 'Unused'},
        {'source': 'gone.md', 'target': 'x.md', 'reason': 'Stale'},
        {'source': 'unselected.md', 'target': 'y.md', 'reason': 'Not scanned'},
    ], 'internal_refs': []})
    assert lk.main(['--root', str(tmp_path), str(doc)]) == 0
    err = capsys.readouterr().err
    assert 'unused links entry a.md -> old.md' in err
    assert 'stale source links entry gone.md -> x.md' in err
    assert 'unselected.md' not in err and 'missing.md' not in err


def test_installed_documentation_module_uses_editable_seed(tmp_path, capsys):
    root = tmp_path / 'adopter'
    root.mkdir()
    profile = root / 'profile.yml'
    profile.write_text(
        'project_name: ScannerTest\ntest_command: pytest\n'
        'preset: high-rigor-legacy\n', encoding='utf-8')
    assert scaffold_main([
        '--config', str(profile), '--target', str(root),
        '--cairn-root', str(CAIRN_ROOT),
    ]) == 0
    doc = root / 'dev/modules/documentation-plan.md'
    text = doc.read_text(encoding='utf-8')
    assert 'link-check-allow:' not in text
    settings_path = root / 'dev/.cairn/scanner-check-allow.json'
    settings = json.loads(settings_path.read_text(encoding='utf-8'))
    assert len(settings['links']) == 1
    assert settings['links'][0]['source'] == 'dev/modules/documentation-plan.md'
    assert settings['links'][0]['target'] == 'docs/DOCUMENTATION_PLAN.md'
    assert settings['links'][0]['reason'].strip()
    assert settings['internal_refs'] == []
    capsys.readouterr()
    assert lk.main(['--root', str(root), str(doc)]) == 0
    capsys.readouterr()

    # The whole-tree opt-in uses the same installed settings through the real CLI.
    subprocess.run(['git', 'init', '--quiet'], cwd=root, check=True)
    subprocess.run(['git', 'add', 'dev/modules/documentation-plan.md'],
                   cwd=root, check=True)
    assert lk.main(['--root', str(root), '--include-modules']) == 0
    capsys.readouterr()

    settings['links'][0]['target'] = 'docs/renamed-plan.md'
    settings_path.write_text(json.dumps(settings), encoding='utf-8')
    assert lk.main(['--root', str(root), str(doc)]) == 1
    assert 'broken link target: `docs/DOCUMENTATION_PLAN.md`' in capsys.readouterr().err


# --- filter_sources: root-anchored exclusions + opt-ins ----------------------

_ROOT = Path("/repo")
_FILES = [
    _ROOT / "dev" / "modules" / "claim-check.md",
    _ROOT / "dev" / "modules" / "onboarding" / "tour.md",
    _ROOT / "dev" / ".cairn" / "base" / "dev" / "modules" / "claim-check.md",
    _ROOT / "dev" / ".cairn" / "cairn_foldback.md",
    _ROOT / "dev" / "plans" / "archive" / "old.md",
    _ROOT / "pkg" / "modules" / "user_authored.md",   # nested elsewhere
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
    # A `modules/` dir that is NOT dev/modules must stay scanned.
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


def test_two_balanced_spans_flanking_link_lock_non_greedy_strip(tmp_path):
    """Locks the NON-greedy property (External-stance review gap): two same-length
    balanced spans with a real broken link between them. The non-greedy backreference
    strips each span independently, leaving the link checked -> it flags. A GREEDY
    regex would strip from the first backtick to the last, swallowing the link -> this
    test would fail. It is the only case that distinguishes greedy from non-greedy."""
    md = tmp_path / "doc.md"
    md.write_text(
        "Spans `one` and [broken](ghost.md) and `two` on one line.\n",
        encoding="utf-8",
    )
    flags = _check(md, tmp_path)
    assert len(flags) == 1, (
        "Two balanced spans must not let a greedy strip swallow the link between them; "
        f"got flags: {flags}"
    )
    assert "ghost.md" in flags[0].message


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


def test_longer_closing_backtick_run_does_not_suppress(tmp_path):
    """A closing run LONGER than the opening run is
    NOT a balanced span -- the backreference must not match a prefix of a longer
    closing run. ``2-open ... 3-close`` (and the reverse) must leave the real link
    checked. This is the false-negative the original ``(`+)(.*?)\\1`` permitted."""
    md = tmp_path / "doc.md"
    md.write_text(
        "Two then three ``[broken](missing.md)``` should still flag.\n"
        "Three then two ```[gone](vanished.md)`` should still flag.\n",
        encoding="utf-8",
    )
    messages = [f.message for f in _check(md, tmp_path)]
    assert any("missing.md" in m for m in messages), messages
    assert any("vanished.md" in m for m in messages), messages


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
