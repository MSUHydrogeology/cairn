# SPDX-License-Identifier: MIT
"""Public board behavior for implementation closeout warnings and appendices."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from dev.tools import board


from tests._repo_root import repository_root

ROOT = repository_root(Path(__file__))


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _closeout_heading() -> str:
    template = (ROOT / "templates/core/dev/plans/_template.md").read_text(
        encoding="utf-8")
    return next(line for line in template.splitlines()
                if line.startswith("## Implementation closeout"))


def _plan(root: Path, *, status: str = "ready-to-archive", body: str,
          name: str = "2026-01-01-example.md") -> Path:
    return _write(root, f"dev/plans/{name}",
                  f"# Example plan\n\n**Status**: {status}\n\n"
                  f"{_closeout_heading()}\n\n{body}")


def _run(root: Path, *args: str, capsys):
    code = board.main(["--root", str(root), *args])
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def test_home_less_item_warns_without_changing_stdout(tmp_path, capsys):
    _plan(tmp_path, body="Not run: one check.\n")
    code, out, err = _run(tmp_path, capsys=capsys)
    assert code == 0
    assert "2026-01-01-example.md:7" in err
    _plan(tmp_path, body="Not run: one check.\nHome: roadmap row 7\n")
    code, home_out, home_err = _run(tmp_path, capsys=capsys)
    assert code == 0 and home_err == ""
    assert out == home_out


def test_home_placeholder_and_fenced_items(tmp_path, capsys):
    _plan(tmp_path, body="Not run: one check.\nHome: <roadmap row>\n")
    assert "has no Home" in _run(tmp_path, capsys=capsys)[2]
    _plan(tmp_path, body="```text\nNot run: fenced.\n```\n")
    assert _run(tmp_path, capsys=capsys)[2] == ""


def test_non_ready_and_archived_plans_are_silent(tmp_path, capsys):
    _plan(tmp_path, status="implementing", body="Not run: one check.\n")
    archived = tmp_path / "dev/plans/archive"
    archived.mkdir(parents=True)
    _plan(archived.parent.parent, body="Not run: archived check.\n",
          name="archive/2026-01-02-archived.md")
    assert _run(tmp_path, capsys=capsys)[2] == ""
    assert _run(tmp_path, "--archive", capsys=capsys)[2] == ""


def test_non_plain_modes_do_not_warn(tmp_path, capsys):
    _plan(tmp_path, body="Not covered: one check.\n")
    for mode in ("--json", "--maintainer", "--next"):
        code, out, err = _run(tmp_path, mode, capsys=capsys)
        assert code == 0 and err == ""
        if mode == "--json":
            assert json.loads(out)["schema"] == "cairn-board/1"


@pytest.mark.skipif(os.name == "nt", reason="Windows forbids control characters in filenames")
def test_warning_escapes_untrusted_name_and_never_shows_closeout(tmp_path, capsys):
    name = "2026-01-01-\x1b" + "x" * 105 + ".md"
    assert len(name) == 120
    _plan(tmp_path, body="Not run: PRIVATE\x1b\x01 text\n", name=name)
    code, out, err = _run(tmp_path, capsys=capsys)
    assert code == 0
    assert "\x1b" not in err and "\x01" not in err
    assert "board: warning -- 2026-01-01-\\x1b" in err
    assert "…:7 has no Home" in err
    assert len(err.splitlines()) == 1 and len(err.splitlines()[0]) < 100
    assert "PRIVATE" not in out + err


def test_warning_caps_output_at_five_plus_summary(tmp_path, capsys):
    items = "\n\n".join(f"Not run: check {i}." for i in range(12))
    _plan(tmp_path, body=items)
    warnings = _run(tmp_path, capsys=capsys)[2].splitlines()
    assert len(warnings) == 6
    assert warnings[-1] == "board: warning -- 7 more not shown"


def test_board_copies_are_byte_equal():
    assert (ROOT / "dev/tools/board.py").read_bytes() == (
        ROOT / "templates/skills/_lib/board.py").read_bytes()


def test_appendix_skip_is_narrow_and_header_sensitive(tmp_path, capsys):
    _write(tmp_path, "dev/proposals/2026-01-01-main.md",
           "# Main\n\n**Status**: awaiting-review\n")
    _write(tmp_path, "dev/proposals/2026-01-01-main--appendix.md",
           "# Appendix\n\nSupport text.\n")
    _, plain, _ = _run(tmp_path, capsys=capsys)
    _, data, _ = _run(tmp_path, "--json", capsys=capsys)
    assert "2026-01-01-main--appendix" not in plain
    assert "2026-01-01-main--appendix" not in data

    _write(tmp_path, "dev/proposals/2026-01-02-wait.md",
           "# Wait\n\n**Status**: awaiting-decision\n")
    _write(tmp_path, "dev/proposals/2026-01-02-wait--appendix.md",
           "# Appendix\n\n**Waiting on Maintainer**: x\n")
    _, waiting, _ = _run(tmp_path, "--maintainer", capsys=capsys)
    _, data, _ = _run(tmp_path, "--json", capsys=capsys)
    assert "2026-01-02-wait--appendix" in waiting
    assert "2026-01-02-wait--appendix" in data

    _write(tmp_path, "dev/proposals/2026-01-03-lone--appendix.md",
           "# Lone appendix\n\n**Status**: awaiting-review\n")
    _write(tmp_path, "dev/plans/2026-01-04-plan--appendix.md",
           "# Plan appendix\n\n**Status**: awaiting-code-review\n")
    _, data, _ = _run(tmp_path, "--json", capsys=capsys)
    assert "2026-01-03-lone--appendix" in data
    assert "2026-01-04-plan--appendix" in data


@pytest.mark.parametrize("failure", [OSError("read failed"), UnicodeDecodeError("utf-8", b"\xff", 0, 1, "bad byte")])
def test_advisory_read_failure_and_unsafe_source(tmp_path, capsys, monkeypatch, failure):
    path = _plan(tmp_path, body="Not run: check.\n")
    original = Path.read_text
    reads = 0

    def read_text(self, *args, **kwargs):
        nonlocal reads
        if self == path:
            reads += 1
            if reads == 2:
                raise failure
        return original(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_text)
    code, out, err = _run(tmp_path, capsys=capsys)
    assert code == 0 and "2026-01-01-example" in out
    assert "closeout check incomplete" in err

    path.unlink()
    path.mkdir()
    code, out, err = _run(tmp_path, capsys=capsys)
    assert code == 1 and "not a regular file" in err
