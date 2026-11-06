"""
The #58 loop-fidelity gate in check_cairn (cairn-loop-fidelity-verification).

An adopter-facing ``templates/`` surface that references a Cairn-internal-only
path (``docs/methodology/*``) dangles once installed in an adopter tree -- the
implementation->adoption failure (#57, the 9-lens roster). The gate fails
closed on such a reference unless it is transplanted or marked a deliberate
citation.

Pins: (1) a planted dangling ref in a templates/ surface flags; (2) BOTH a
backticked token and a raw Markdown link target flag (a relative
``[x](docs/methodology/..)`` link that link_check passes in-source but breaks on
adoption); (3) the ``cairn-internal-ref-allow`` / ``cairn-internal-ref``
markers exempt; (4) the scan-allowlist -- a non-``templates/`` file is not
scanned; (5) sharpness -- a marker for one doctrine path does not exempt a
*different* one; (6) end-to-end, check_cairn exits non-zero (fail-closed).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT / "scripts"))

import check_cairn  # noqa: E402


def _loop_flags(result) -> list:
    return [f for f in result.flags
            if f.kind == "path" and "loop-fidelity" in f.message]


def _tmpl(tmp_path: Path, body: str, rel: str = "templates/core/AGENTS.md") -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


class TestDanglingRefGate:
    def test_backticked_doctrine_ref_flags(self, tmp_path: Path) -> None:
        md = _tmpl(
            tmp_path,
            "See the roster in `docs/methodology/dual-review.md` and "
            "the retired `doctrine/dual-review.md` path.\n",
        )
        flags = _loop_flags(check_cairn.check_tree(tmp_path, [md]))
        assert any("docs/methodology/dual-review.md" in f.message for f in flags)
        assert any("doctrine/dual-review.md" in f.message for f in flags)

    def test_markdown_link_target_flags(self, tmp_path: Path) -> None:
        """A raw Markdown relative link target to docs/methodology/ flags --
        link_check passes it in-source but it breaks on adoption."""
        md = _tmpl(
            tmp_path,
            "See [the sweep](../../docs/methodology/dual-review.md) and "
            "the retired [path](../../doctrine/dual-review.md).\n",
        )
        flags = _loop_flags(check_cairn.check_tree(tmp_path, [md]))
        assert any("docs/methodology/dual-review.md" in f.message for f in flags)
        assert any("doctrine/dual-review.md" in f.message for f in flags)

    def test_file_level_allow_marker_exempts(self, tmp_path: Path) -> None:
        body = (
            "<!-- cairn-internal-ref-allow: docs/methodology/dual-review.md "
            "reason=citation convention -->\n"
            "See the roster in `docs/methodology/dual-review.md`.\n"
        )
        md = _tmpl(tmp_path, body)
        assert not _loop_flags(check_cairn.check_tree(tmp_path, [md])), \
            "a cairn-internal-ref-allow marker must exempt the named path"

    def test_inline_marker_exempts_filewide(self, tmp_path: Path) -> None:
        """The inline marker is collected file-wide, so it exempts even when
        it does not sit on the same wrapped line as the reference."""
        body = (
            "See the roster in `docs/methodology/dual-review.md` >\n"
            '"the clean-pass trap".'
            " <!-- cairn-internal-ref: docs/methodology/dual-review.md reason=why -->\n"
        )
        md = _tmpl(tmp_path, body)
        assert not _loop_flags(check_cairn.check_tree(tmp_path, [md]))

    def test_non_template_file_not_scanned(self, tmp_path: Path) -> None:
        """Scan-allowlist: only adopter-facing templates/ surfaces are
        scanned; a docs/methodology/ file referencing its siblings is not."""
        md = tmp_path / "docs" / "methodology" / "x.md"
        md.parent.mkdir(parents=True)
        md.write_text("See `docs/methodology/dual-review.md`.\n", encoding="utf-8")
        assert not _loop_flags(check_cairn.check_tree(tmp_path, [md]))

    def test_marker_is_path_specific(self, tmp_path: Path) -> None:
        """Sharpness: a marker naming one doctrine path does not exempt a
        reference to a *different* doctrine path (a new dangling ref still
        fails closed)."""
        body = (
            "<!-- cairn-internal-ref-allow: docs/methodology/dual-review.md "
            "reason=citation -->\n"
            "See `docs/methodology/dual-review.md` and `docs/methodology/lifecycle.md`.\n"
        )
        md = _tmpl(tmp_path, body)
        flags = _loop_flags(check_cairn.check_tree(tmp_path, [md]))
        assert len(flags) == 1, "only the unlisted docs/methodology/lifecycle.md flags"
        assert "docs/methodology/lifecycle.md" in flags[0].message

    def test_bare_prefix_marker_normalizes(self, tmp_path: Path) -> None:
        """A bare directory token matching a known internal prefix
        (``docs/methodology``, no trailing slash) is normalized to ``docs/methodology/`` and
        exempts, rather than being silently dropped."""
        body = (
            "<!-- cairn-internal-ref-allow: docs/methodology reason=blanket -->\n"
            "See `docs/methodology/dual-review.md` and `docs/methodology/lifecycle.md`.\n"
        )
        md = _tmpl(tmp_path, body)
        assert not _loop_flags(check_cairn.check_tree(tmp_path, [md]))

    def test_check_cairn_exits_nonzero_on_dangling_ref(self, tmp_path: Path) -> None:
        """End-to-end fail-closed: the CLI returns non-zero (1) when an
        adopter-facing surface carries an un-exempted dangling reference."""
        md = _tmpl(tmp_path, "See `docs/methodology/dual-review.md`.\n")
        rc = check_cairn.main([str(md), "--root", str(tmp_path)])
        assert rc != 0, "check_cairn must fail closed on a dangling ref"

    def test_config_is_exact_and_legacy_inline_stays_filewide(self, tmp_path, capsys):
        md = _tmpl(tmp_path, 'See `docs/methodology/roles.md` and\n'
                   '`docs/methodology/roles.md-extra` and\n'
                   '`docs/methodology/dual-review.md`.\n'
                   '<!-- cairn-internal-ref: docs/methodology/dual-review.md -->\n')
        cfg = tmp_path / 'dev/.cairn/scanner-check-allow.json'
        cfg.parent.mkdir(parents=True)
        cfg.write_text(json.dumps({'links': [], 'internal_refs': [
            {'source': 'templates/core/AGENTS.md',
             'target': 'docs/methodology/roles.md', 'reason': 'Citation'}]}))
        assert check_cairn.main(['--root', str(tmp_path), '--no-content-scan', str(md)]) == 1
        err = capsys.readouterr().err
        assert 'roles.md-extra' in err
        assert '`docs/methodology/roles.md`' not in err
        assert '`docs/methodology/dual-review.md`' not in err

    def test_invalid_config_disables_both_legacy_marker_forms(self, tmp_path, capsys):
        md = _tmpl(tmp_path, '<!-- cairn-internal-ref-allow: docs/methodology/roles.md -->\n'
                   '`docs/methodology/roles.md`\n'
                   '`docs/methodology/dual-review.md`\n'
                   '<!-- cairn-internal-ref: docs/methodology/dual-review.md -->\n')
        assert check_cairn.main(['--root', str(tmp_path), '--no-content-scan', str(md)]) == 0
        capsys.readouterr()
        cfg = tmp_path / 'dev/.cairn/scanner-check-allow.json'
        cfg.parent.mkdir(parents=True)
        cfg.write_text('{"links": [], "links": [], "internal_refs": []}')
        assert check_cairn.main(['--root', str(tmp_path), '--no-content-scan', str(md)]) == 1
        err = capsys.readouterr().err
        assert 'duplicate key' in err and 'roles.md' in err and 'dual-review.md' in err

    def test_internal_config_reports_unused_and_stale_without_failing(self, tmp_path, capsys):
        md = _tmpl(tmp_path, '`docs/methodology/roles.md`\n')
        cfg = tmp_path / 'dev/.cairn/scanner-check-allow.json'
        cfg.parent.mkdir(parents=True)
        def item(source, target):
            return {'source': source, 'target': target, 'reason': 'Citation'}
        cfg.write_text(json.dumps({'links': [], 'internal_refs': [
            item('templates/core/AGENTS.md', 'docs/methodology/roles.md'),
            item('templates/core/AGENTS.md', 'docs/methodology/unused.md'),
            item('templates/gone.md', 'docs/methodology/roles.md')]}))
        assert check_cairn.main(['--root', str(tmp_path), '--no-content-scan', str(md)]) == 0
        err = capsys.readouterr().err
        assert 'unused internal_refs entry templates/core/AGENTS.md' in err
        assert 'stale source internal_refs entry templates/gone.md' in err
        assert 'unused internal_refs entry templates/core/AGENTS.md -> docs/methodology/roles.md' not in err
