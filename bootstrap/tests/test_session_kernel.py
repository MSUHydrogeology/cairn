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
import sys
import tempfile
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]
KERNEL = CAIRN_ROOT / "tools" / "session.py"
_CONTENT_SCAN = CAIRN_ROOT / "scripts" / "content_scan.py"
TWIN = CAIRN_ROOT / "templates" / "skills" / "_lib" / "session.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader, path
    module = importlib.util.module_from_spec(spec)
    # Registered before exec: a module defining a dataclass looks itself up in
    # sys.modules while the decorator runs, and finds None if it is absent.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


kernel = _load(KERNEL, "cairn_session_kernel_under_test")
scan = _load(_CONTENT_SCAN, "cairn_content_scan_for_kernel")


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
        "\u034f",  # combining grapheme joiner
        "\u115f",  # Hangul choseong filler
        "\ufe0f",  # variation selector-16
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


# the terminal encoder, and its DIRECTIONAL drift oracle
# =============================================================================


def _scanner_display_unsafe_population() -> set[str]:
    """Expand **every** member and **every code point** of the reviewed
    content-scan inventory.

    *"It imports the Cairn content scanner in the test
    environment, expands every member of the three sets, every code point in
    `_IGNORABLE_RANGES` and `_NONCHARACTER_RANGES`, the complete `_TAG_RANGE`,
    and `_ASCII_GUARD`."*  Not a hand-copied sample: the sets are read from the
    scanner, so a member added there enters this population automatically.
    """
    population: set[str] = set()
    population |= set(scan._ZERO_WIDTH)
    population |= set(scan._BIDI)
    population |= set(scan._LINE_SEPARATORS)
    for low, high in tuple(scan._IGNORABLE_RANGES) + tuple(
            scan._NONCHARACTER_RANGES):
        population |= {chr(code) for code in range(low, high + 1)}
    low, high = scan._TAG_RANGE
    population |= {chr(code) for code in range(low, high + 1)}
    population.add(scan._ASCII_GUARD)
    return population


class TestDirectionalDriftGuard:
    """The one-way coupling, stated as an assertion:

        expanded content-scan display-unsafe population <= board escaped population

    The board may escape more than the scanner flags.  It may never emit raw a
    code point the scanner recognizes.  So a newly added printable invisible
    reddens this class until `_DISPLAY_UNSAFE_RANGES` follows it, and narrowing a
    detector cannot silently weaken terminal output.
    """

    def test_the_population_under_test_is_not_a_token_sample(self):
        """A guard on the guard.  Raised because a three-set population
        *could not contain* its own counterexamples; if this population ever
        shrinks to a handful, the subset assertion below goes quietly green."""
        population = _scanner_display_unsafe_population()
        assert len(population) > 4000, (
            f"the expanded scanner population is only {len(population)} code "
            "points -- it must expand every range, not sample them")
        # The rows that make it big are the ones a category sweep misses.
        assert chr(0xE0041) in population, "the Tag block must be expanded"
        assert chr(0xFDD0) in population, "noncharacters must be expanded"
        assert chr(0x034F) in population, "the Mn residual must be present"

    def test_every_scanner_recognized_code_point_is_escaped(self):
        survivors = [
            char for char in sorted(_scanner_display_unsafe_population())
            if kernel.encode_display(char) == char
        ]
        assert survivors == [], (
            f"{len(survivors)} scanner-recognized code point(s) survive raw "
            f"through the kernel encoder, first={survivors[:5]!r}")

    def test_the_range_table_covers_the_scanner_population_by_code_point(self):
        """The subset assertion at the *table* level, not only through the
        encoder: clause 2 must carry the population on its own, so a future
        change to clause 1 cannot silently become the only thing holding it."""
        uncovered = [
            char for char in sorted(_scanner_display_unsafe_population())
            if not kernel._display_unsafe_code_point(ord(char))
        ]
        assert uncovered == [], (
            f"{len(uncovered)} scanner code point(s) are outside "
            f"_DISPLAY_UNSAFE_RANGES, first={uncovered[:5]!r}")

    def test_neither_kernel_source_embeds_a_represented_invisible_raw(self):
        """The encoder's own sources must not carry the characters it exists to
        escape -- a Trojan-source carrier that escapes Trojan source is the
        weakest possible position."""
        population = _scanner_display_unsafe_population()
        for path in (KERNEL, TWIN):
            text = path.read_text(encoding="utf-8")
            present = sorted({char for char in population if char in text})
            assert present == [], (
                f"{path} embeds {len(present)} represented invisible(s) raw, "
                f"first={present[:5]!r}")


    def test_this_test_module_embeds_none_either(self):
        """The same property for the oracle, so the file that proves the planner
        clean is not itself a Trojan-source carrier."""
        population = _scanner_display_unsafe_population()
        text = Path(__file__).read_text(encoding="utf-8")
        assert sorted({char for char in population if char in text}) == []
