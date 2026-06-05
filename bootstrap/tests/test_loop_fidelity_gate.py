"""
The #58 loop-fidelity gate in check_cairn (cairn-loop-fidelity-verification).

An adopter-facing ``templates/`` surface that references a Cairn-internal-only
path (``doctrine/*``) dangles once installed in an adopter tree -- the
implementation->adoption failure (#57, the 9-lens roster). The gate fails
closed on such a reference unless it is transplanted or marked a deliberate
citation.

Pins: (1) a planted dangling ref in a templates/ surface flags; (2) BOTH a
backticked token and a raw Markdown link target flag (N1 -- a relative
``[x](doctrine/..)`` link that link_check passes in-source but breaks on
adoption); (3) the ``cairn-internal-ref-allow`` / ``cairn-internal-ref``
markers exempt; (4) the scan-allowlist -- a non-``templates/`` file is not
scanned; (5) sharpness -- a marker for one doctrine path does not exempt a
*different* one; (6) end-to-end, check_cairn exits non-zero (fail-closed).

Run from the cairn repo root:
    python -m pytest bootstrap/tests/
"""

from __future__ import annotations

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
        md = _tmpl(tmp_path, "See the roster in `doctrine/dual-review.md`.\n")
        assert _loop_flags(check_cairn.check_tree(tmp_path, [md])), \
            "a backticked doctrine/ reference in a template must flag"

    def test_markdown_link_target_flags(self, tmp_path: Path) -> None:
        """N1: a raw Markdown relative link target to doctrine/ flags --
        link_check passes it in-source but it breaks on adoption."""
        md = _tmpl(tmp_path, "See [the sweep](../../doctrine/dual-review.md).\n")
        flags = _loop_flags(check_cairn.check_tree(tmp_path, [md]))
        assert flags, "a Markdown link target to doctrine/ must flag (N1)"

    def test_file_level_allow_marker_exempts(self, tmp_path: Path) -> None:
        body = (
            "<!-- cairn-internal-ref-allow: doctrine/dual-review.md "
            "reason=citation convention -->\n"
            "See the roster in `doctrine/dual-review.md`.\n"
        )
        md = _tmpl(tmp_path, body)
        assert not _loop_flags(check_cairn.check_tree(tmp_path, [md])), \
            "a cairn-internal-ref-allow marker must exempt the named path"

    def test_inline_marker_exempts_filewide(self, tmp_path: Path) -> None:
        """The inline marker is collected file-wide, so it exempts even when
        it does not sit on the same wrapped line as the reference."""
        body = (
            "See the roster in `doctrine/dual-review.md` >\n"
            '"the clean-pass trap".'
            " <!-- cairn-internal-ref: doctrine/dual-review.md reason=why -->\n"
        )
        md = _tmpl(tmp_path, body)
        assert not _loop_flags(check_cairn.check_tree(tmp_path, [md]))

    def test_non_template_file_not_scanned(self, tmp_path: Path) -> None:
        """Scan-allowlist (F3): only adopter-facing templates/ surfaces are
        scanned; a doctrine/ file referencing its siblings is not."""
        md = tmp_path / "doctrine" / "x.md"
        md.parent.mkdir(parents=True)
        md.write_text("See `doctrine/dual-review.md`.\n", encoding="utf-8")
        assert not _loop_flags(check_cairn.check_tree(tmp_path, [md]))

    def test_marker_is_path_specific(self, tmp_path: Path) -> None:
        """Sharpness: a marker naming one doctrine path does not exempt a
        reference to a *different* doctrine path (a new dangling ref still
        fails closed)."""
        body = (
            "<!-- cairn-internal-ref-allow: doctrine/dual-review.md "
            "reason=citation -->\n"
            "See `doctrine/dual-review.md` and `doctrine/lifecycle.md`.\n"
        )
        md = _tmpl(tmp_path, body)
        flags = _loop_flags(check_cairn.check_tree(tmp_path, [md]))
        assert len(flags) == 1, "only the unlisted doctrine/lifecycle.md flags"
        assert "doctrine/lifecycle.md" in flags[0].message

    def test_check_cairn_exits_nonzero_on_dangling_ref(self, tmp_path: Path) -> None:
        """End-to-end fail-closed: the CLI returns non-zero (1) when an
        adopter-facing surface carries an un-exempted dangling reference."""
        md = _tmpl(tmp_path, "See `doctrine/dual-review.md`.\n")
        rc = check_cairn.main([str(md), "--root", str(tmp_path)])
        assert rc != 0, "check_cairn must fail closed on a dangling ref"
