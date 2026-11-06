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

import ast
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]
KERNEL = CAIRN_ROOT / "tools" / "session.py"
_CONTENT_SCAN = CAIRN_ROOT / "scripts" / "content_scan.py"
TWIN = CAIRN_ROOT / "templates" / "skills" / "_lib" / "session.py"


def _binding_path(root: Path) -> Path:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True, capture_output=True)
    git_dir = subprocess.run(
        ["git", "rev-parse", "--absolute-git-dir"], cwd=root, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    path = Path(git_dir) / "cairn" / "local-env.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


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


def _critical_owner_forks(root: Path) -> list[str]:
    owners = {
        "encode_display": {"tools/session.py", "templates/skills/_lib/session.py"},
        "_read_regular_bytes": {
            "tools/session.py", "templates/skills/_lib/session.py",
            "bootstrap/_scaffold/security.py",
        },
    }
    forks = []
    for directory in ("tools", "templates/skills/_lib", "bootstrap/_scaffold"):
        for path in sorted((root / directory).rglob("*.py")):
            relative = path.relative_to(root).as_posix()
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
            for node in ast.walk(tree):
                if (isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                        and node.name in owners and relative not in owners[node.name]):
                    forks.append(f"{relative}:{node.lineno}:{node.name}")
    return forks


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

    def test_git_helper_is_loaded_lazily_from_the_fixed_sibling_buffer(
            self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        delivery = tmp_path / "delivery"
        delivery.mkdir()
        session_path = delivery / "session.py"
        helper_path = delivery / "git_read.py"
        session_path.write_bytes(TWIN.read_bytes())
        helper_bytes = (CAIRN_ROOT / "templates/skills/_lib/git_read.py").read_bytes()
        helper_path.write_bytes(helper_bytes)
        target = tmp_path / "target"
        target.mkdir()
        marker = target / "target-helper-ran"
        (target / "git_read.py").write_text(
            f"from pathlib import Path\nPath({str(marker)!r}).write_text('ran')\n",
            encoding="utf-8")
        loaded = _load(session_path, "cairn_session_lazy_git_reader")
        assert loaded.encode_display("plain") == "plain"
        assert not marker.exists()
        monkeypatch.chdir(target)
        verified = loaded._load_git_read_helper()
        assert hashlib.sha256(verified.__verified_source__).digest() == hashlib.sha256(
            helper_bytes).digest()
        assert verified.__verified_sha256__ == hashlib.sha256(helper_bytes).hexdigest()
        assert not marker.exists()

        # A pathname change after verification cannot substitute the already
        # compiled buffer for this process's current reads.
        bad = b"from pathlib import Path\nPath(" + repr(str(marker)).encode() \
            + b").write_text('ran')\n"
        helper_path.write_bytes(bad)
        assert loaded._load_git_read_helper() is verified
        fresh = _load(session_path, "cairn_session_tampered_git_reader")
        with pytest.raises(fresh.LifecycleError, match="Git read helper binding failed"):
            fresh._load_git_read_helper()
        assert not marker.exists()


class TestOneEncoderNoFallbackTable:
    """A second, weaker escape table is the failure this surface was built to
    remove: it engages exactly when something is already wrong. The encoder
    escapes by code-point range, not by a fixed table, so the characters a
    lookup table historically missed are covered."""

    def test_named_critical_helpers_stay_in_their_documented_homes(self) -> None:
        assert _critical_owner_forks(CAIRN_ROOT) == []

    @pytest.mark.parametrize("directory", [
        "tools", "templates/skills/_lib", "bootstrap/_scaffold",
    ])
    @pytest.mark.parametrize("name", ["encode_display", "_read_regular_bytes"])
    def test_named_fork_guard_catches_a_planted_weaker_reader(
        self, tmp_path: Path, directory: str, name: str,
    ) -> None:
        planted = tmp_path / directory / "weaker.py"
        planted.parent.mkdir(parents=True)
        planted.write_text(f"def {name}(value):\n    return value\n", encoding="utf-8")
        assert _critical_owner_forks(tmp_path) == [f"{directory}/weaker.py:1:{name}"]

    def test_fork_guard_allows_owner_copies_and_a_delegating_wrapper(
        self, tmp_path: Path,
    ) -> None:
        for relative in ("tools/session.py", "templates/skills/_lib/session.py"):
            owner = tmp_path / relative
            owner.parent.mkdir(parents=True)
            owner.write_text(
                "def encode_display(value): return value\n"
                "def _read_regular_bytes(path): return b''\n", encoding="utf-8")
        wrapper = tmp_path / "tools" / "display_wrapper.py"
        wrapper.write_text(
            "from tools import session\n"
            "def display(value): return session.encode_display(value)\n", encoding="utf-8")
        assert _critical_owner_forks(tmp_path) == []

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
            _binding_path(root).write_text(
                json.dumps(binding), encoding="utf-8")
            with pytest.raises(kernel.LifecycleError):
                kernel._resolve_interpreter(root)

    def test_a_vanished_interpreter_falls_back_audibly(self, capsys) -> None:
        """Falling back silently would leave a rebuilt environment running an
        interpreter nobody chose, with no signal that the binding is stale."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _binding_path(root).write_text(
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
