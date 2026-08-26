# SPDX-License-Identifier: MIT
"""The session kernel: the part of the lifecycle CLI that outlives it.

**Why this file does not skip.** Every other test of this surface loads its
module behind a ``pytest.mark.skipif`` guard, so when the file it loads goes
away those tests *skip rather than fail* -- silent, and invisible to a falling
test count. That is how a deletion sweep removes a live surface without anyone
noticing. This file imports the kernel unconditionally: if the kernel is gone,
these tests error, loudly, which is the whole point.
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]
KERNEL = CAIRN_ROOT / "tools" / "session.py"
TWIN = CAIRN_ROOT / "templates" / "skills" / "_lib" / "session.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


kernel = _load(KERNEL, "cairn_session_kernel_under_test")


class TestTheKernelIsSelfContained:
    """The kernel must start without the lifecycle planner, because the planner
    is removed while the kernel is kept. Before extraction the session routines
    reached the terminal encoder through the planner's vocabulary loader, so a
    missing planner meant a session that could not start."""

    def test_the_kernel_names_no_planner_module(self) -> None:
        source = KERNEL.read_text(encoding="utf-8")
        assert "lifecycle_planner" not in source

    def test_the_encoder_lives_here_and_needs_no_loader(self) -> None:
        assert callable(kernel.encode_display)
        assert kernel.encode_display("plain") == "plain"


class TestOneEncoderNoFallbackTable:
    """A second, weaker escape table is the failure this surface was built to
    remove: it engages exactly when something is already wrong. The encoder
    escapes by code-point range, not by a fixed table, so the characters a
    lookup table historically missed are covered."""

    @pytest.mark.parametrize("hostile", [
        "͏",      # combining grapheme joiner
        "ᅟ",      # Hangul choseong filler
        "️",      # variation selector-16
    ])
    def test_printable_but_display_unsafe_code_points_are_escaped(self, hostile) -> None:
        assert hostile.isprintable(), "fixture no longer exercises the gap"
        assert hostile not in kernel.encode_display(hostile)

    def test_non_printable_code_points_are_escaped_too(self) -> None:
        """The Tag block is `Cf`, so `str.isprintable()` already rejects it. It
        still must not reach a terminal raw -- printability and the code-point
        range are two rules and neither subsumes the other."""
        tag = "\U000e0041"
        assert not tag.isprintable()
        assert tag not in kernel.encode_display(tag)

    def test_elision_is_layered_outside_the_encoder(self) -> None:
        """A hostile 4,000-character value must not own the terminal, and the
        cut is taken from encoded output so it cannot split a source character
        into a half-escape that reads as something else."""
        out = kernel._safe_field("A" * 4000)
        assert len(out) < 4000 and "elided" in out


class TestTheInterpreterBindingIsAShapeValidator:
    """The caller executes the path this returns, so a malformed binding must
    refuse rather than resolve. It validates shape -- absoluteness, schema,
    symlink-freedom, the executable bit -- and deliberately establishes nothing
    about Python identity or provenance."""

    @pytest.mark.parametrize("binding", [
        {"interpreter": "python3"},          # not absolute
        {},                                  # no interpreter key
        {"interpreter": "/etc/hosts"},       # not executable
        {"interpreter": "/tmp"},             # a directory
    ])
    def test_a_malformed_binding_refuses(self, binding) -> None:
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "dev" / ".cairn").mkdir(parents=True)
            (root / "dev" / ".cairn" / "local-env.json").write_text(
                json.dumps(binding), encoding="utf-8")
            with pytest.raises(kernel.LifecycleError):
                kernel._resolve_interpreter(root)

    def test_a_vanished_interpreter_falls_back_audibly(self, capsys) -> None:
        """Falling back silently would leave a rebuilt environment running an
        interpreter nobody chose, with no signal that the binding is stale."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "dev" / ".cairn").mkdir(parents=True)
            (root / "dev" / ".cairn" / "local-env.json").write_text(
                json.dumps({"interpreter": "/nonexistent/python3"}), encoding="utf-8")
            interpreter, _source = kernel._resolve_interpreter(root)
            assert interpreter
            assert "no longer exists" in capsys.readouterr().err


class TestTheTwinIsByteIdentical:
    """The shipped copy is what an adopter actually runs. If it drifts from the
    self-hosted one, this repository stops testing what it distributes."""

    def test_both_copies_match(self) -> None:
        assert KERNEL.read_bytes() == TWIN.read_bytes()
