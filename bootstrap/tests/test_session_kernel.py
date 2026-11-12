# SPDX-License-Identifier: MIT
"""The session kernel: the part of the lifecycle CLI that outlives it.

**Why this file does not skip.** Every other test of this surface loads its
module behind a ``pytest.mark.skipif`` guard, so when the file it loads goes
away those tests *skip rather than fail* -- silent, and invisible to a falling
test count. That is how a deletion sweep removes a live surface without anyone
noticing. This file imports the kernel unconditionally: if the kernel is gone,
these tests error, loudly, which is the whole point.

Promises:
- Display text from the project is escaped for non-printing and display-
  unsafe code points.
- A malformed or vanished interpreter binding refuses or falls back audibly,
  never silently.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
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


class TestTheKernelIsSelfContained:
    """The kernel must start without the lifecycle planner, because the planner
    is removed while the kernel is kept. Before extraction the session routines
    reached the terminal encoder through the planner's vocabulary loader, so a
    missing planner meant a session that could not start."""


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


class TestTheTwinIsByteIdentical:
    """The shipped copy is what an adopter actually runs. If it drifts from the
    self-hosted one, this repository stops testing what it distributes."""

    def test_both_copies_match(self) -> None:
        assert KERNEL.read_bytes() == TWIN.read_bytes()


# the terminal encoder, and its DIRECTIONAL drift oracle
# =============================================================================


_SESSION_ROUTE_OWNERS = (
    "tools/session.py",
    "templates/skills/_lib/session.py",
)
_SESSION_ROUTE_SPECS = (
    ("repo-root", "_repo_root", "run_git",
     ("rev-parse", "--show-toplevel"),
     "not inside a git repository -- run the lifecycle routines from within the project checkout."),
    ("history", "_git", "run_git",
     ("log", "--grep=^Handoff", "--format=%H", "-n", "1"),
     "Git read failed; session state is unavailable"),
    ("status", "_git", "run_git",
     ("-c", "core.quotePath=false", "status", "--short"),
     "Git read failed; session state is unavailable"),
    ("tracked-interpreter", "_binding_untrusted", "run_git",
     ("ls-files", "-z", "--cached", "--stage"),
     "could not verify whether the project tracks the selected interpreter; refusing to run a sub-tool. Check that git works in this folder."),
    ("binding-version", "_git_binding_path", "read_version", ("--version",),
     "git interpreter discovery failed"),
    ("binding-root", "_git_binding_path", "run_git",
     ("rev-parse", "--show-toplevel"),
     "git could not resolve the worktree root"),
    ("binding-gitdir", "_git_binding_path", "run_git",
     ("rev-parse", "--absolute-git-dir"),
     "git could not resolve the Git administration path"),
)
_SESSION_ROUTE_CASES = tuple(
    (owner, route, function, method, args, expected)
    for owner in _SESSION_ROUTE_OWNERS
    for route, function, method, args, expected in _SESSION_ROUTE_SPECS
)


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


def _session_route_source(source_bytes: bytes, route: str, function: str,
                          method: str, *, unsafe: bool) -> bytes:
    source = source_bytes.decode("utf-8")
    tree = ast.parse(source)
    owners = [node for node in ast.walk(tree)
              if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
              and node.name == function]
    assert len(owners) == 1, f"missing unique route owner {function}"
    calls = [node for node in ast.walk(owners[0])
             if isinstance(node, ast.Call)
             and isinstance(node.func, ast.Attribute)
             and node.func.attr == method]
    if route == "binding-root":
        calls = [node for node in calls
                 if ast.get_source_segment(source, node.args[1])
                 == '("rev-parse", "--show-toplevel")']
    elif route == "binding-gitdir":
        calls = [node for node in calls
                 if ast.get_source_segment(source, node.args[1])
                 == '("rev-parse", "--absolute-git-dir")']
    assert len(calls) == 1, f"{route} has {len(calls)} selected calls in {function}"
    call = calls[0]
    target_source = ast.get_source_segment(source, call.args[0])
    if method == "read_version":
        args_source = '("--version",)'
    else:
        args_source = ast.get_source_segment(source, call.args[1])
    call_source = ast.get_source_segment(source, call)
    assert target_source and args_source and call_source
    wrapper = "_cairn_test_session_unsafe_route" if unsafe else "_cairn_test_session_safe_route"
    replacement = (
        f"{wrapper}({route!r}, {target_source}, {args_source}, "
        f"lambda: {call_source})"
    )
    lines = source.splitlines(keepends=True)
    starts = [0]
    for line in lines:
        starts.append(starts[-1] + len(line))
    encoded = source.encode("utf-8")
    start_line, end_line = call.lineno - 1, call.end_lineno - 1
    start = len(source[:starts[start_line]].encode("utf-8")) + call.col_offset
    end = len(source[:starts[end_line]].encode("utf-8")) + call.end_col_offset
    instrumented = (encoded[:start] + replacement.encode("utf-8")
                    + encoded[end:]).decode("utf-8")
    helper_code = r'''
from types import SimpleNamespace


def _cairn_test_session_route(route, target, args, operation):
    if os.environ.get("CAIRN_TEST_SESSION_ROUTE") != route:
        return operation()
    selected = tuple(json.loads(os.environ["CAIRN_TEST_SESSION_ARGS"]))
    if tuple(args) != selected:
        return operation()
    Path(os.environ["CAIRN_TEST_SESSION_TRIGGER"]).write_text("reached")
    original_path = os.environ.get("PATH", "")
    os.environ["PATH"] = os.environ["CAIRN_TEST_SESSION_HOSTILE_PATH"]
    try:
        if os.environ.get("CAIRN_TEST_SESSION_UNSAFE") == "1":
            completed = subprocess.run(
                ["git", *args], cwd=target, capture_output=True, check=False,
                text=False,
            )
            return SimpleNamespace(
                state="completed", returncode=completed.returncode,
                stdout=completed.stdout, stderr=completed.stderr,
            )
        return operation()
    finally:
        os.environ["PATH"] = original_path

_cairn_test_session_safe_route = _cairn_test_session_route
_cairn_test_session_unsafe_route = _cairn_test_session_route
'''
    guard = 'if __name__ == "__main__":  # pragma: no cover'
    assert instrumented.count(guard) == 1
    instrumented = instrumented.replace(guard, helper_code + "\n\n" + guard)
    return instrumented.encode("utf-8")


def _session_route_repo(root: Path, git: str) -> tuple[str, str]:
    root.mkdir(parents=True)
    subprocess.run([git, "init", "-q"], cwd=root, check=True,
                   capture_output=True)
    subprocess.run([git, "config", "user.name", "Session Route"], cwd=root,
                   check=True, capture_output=True)
    subprocess.run([git, "config", "user.email", "session-route@example.test"],
                   cwd=root, check=True, capture_output=True)
    (root / "README.md").write_text("session route fixture\n", encoding="utf-8")
    subprocess.run([git, "add", "README.md"], cwd=root, check=True,
                   capture_output=True)
    subprocess.run([git, "commit", "-m", "Handoff"], cwd=root, check=True,
                   capture_output=True)
    handoff = subprocess.run([git, "rev-parse", "HEAD"], cwd=root, check=True,
                             capture_output=True, text=True).stdout.strip()
    gitdir = subprocess.run([git, "rev-parse", "--absolute-git-dir"], cwd=root,
                            check=True, capture_output=True, text=True).stdout.strip()
    env_path = Path(gitdir) / "cairn" / "local-env.json"
    env_path.parent.mkdir(parents=True, exist_ok=True)
    env_path.write_text(json.dumps({"interpreter": str(Path(sys.executable).resolve())}),
                        encoding="utf-8")
    return handoff, gitdir


def _session_route_command(entry: Path, cwd: Path, git: str, *, env: dict | None = None):
    command_env = dict(os.environ)
    command_env["PATH"] = str(Path(git).parent) + os.pathsep + "/usr/bin:/bin"
    if env:
        command_env.update(env)
    return subprocess.run([sys.executable, str(entry), "session-start"], cwd=cwd,
                          env=command_env, capture_output=True, text=True, check=False)


def _session_route_delivery(base: Path, owner: str, source: bytes, helper: bytes) -> Path:
    target = base / "delivery"
    target.mkdir(parents=True)
    entry = target / "session.py"
    entry.write_bytes(source)
    (target / "git_read.py").write_bytes(helper)
    return entry


def _session_route_call(entry: Path, repo: Path, git: str, expected_history: str) -> None:
    result = _session_route_command(entry, repo, git)
    assert result.returncode == 0, result.stderr
    assert expected_history in result.stdout
    assert "clean working tree" in result.stdout.lower()


def _session_route_exercise(tmp_path: Path, owner: str, route: str,
                            function: str, method: str, args: tuple[str, ...] | None,
                            expected: str, *, unsafe: bool = False) -> None:
    git = shutil.which("git")
    assert git and Path(git).is_absolute()
    owner_path = CAIRN_ROOT / owner
    source = owner_path.read_bytes()
    helper = (CAIRN_ROOT / "templates/skills/_lib/git_read.py").read_bytes()
    actual_repo = tmp_path / "project"
    handoff, _gitdir = _session_route_repo(actual_repo, git)
    if route == "history":
        args = ("log", f"{handoff}..HEAD", "--format=%h %an  %s")
    assert args is not None
    clean_entry = _session_route_delivery(tmp_path / "clean", owner, source, helper)
    _session_route_call(clean_entry, actual_repo, git, "no commits in range")

    safe_source = _session_route_source(source, route, function, method, unsafe=False)
    hostile_entry = _session_route_delivery(tmp_path / "hostile", owner, safe_source, helper)
    hostile_bin = actual_repo / ".fixture-bin"
    hostile_bin.mkdir()
    marker = tmp_path / "decoy-git-ran"
    wrapper = hostile_bin / "git"
    wrapper.write_text("#!/bin/sh\n" + f"echo ran > {shlex.quote(str(marker))}\n"
                       + f"exec {shlex.quote(git)} \"$@\"\n", encoding="utf-8")
    wrapper.chmod(0o755)
    trigger = tmp_path / "selected-route-reached"
    env = {
        "CAIRN_TEST_SESSION_ROUTE": route,
        "CAIRN_TEST_SESSION_ARGS": json.dumps(args),
        "CAIRN_TEST_SESSION_TRIGGER": str(trigger),
        "CAIRN_TEST_SESSION_HOSTILE_PATH": str(hostile_bin),
    }
    safe = _session_route_command(hostile_entry, actual_repo, git, env=env)
    assert trigger.exists(), f"{owner}:{route} selected call was not reached"
    assert not marker.exists(), f"safe {owner}:{route} invoked hostile Git"
    assert safe.returncode != 0 and expected in safe.stderr, safe.stderr

    unsafe_source = _session_route_source(source, route, function, method, unsafe=True)
    unsafe_entry = _session_route_delivery(tmp_path / "unsafe", owner, unsafe_source, helper)
    trigger.unlink()
    unsafe_env = dict(env, CAIRN_TEST_SESSION_UNSAFE="1")
    bypass = _session_route_command(unsafe_entry, actual_repo, git, env=unsafe_env)
    assert trigger.exists(), f"unsafe {owner}:{route} selected call was not reached"
    assert marker.exists(), f"unsafe {owner}:{route} failed to execute hostile Git"
    assert bypass.returncode == 0, bypass.stderr


@pytest.mark.parametrize(
    "owner,route,function,method,args,expected",
    _SESSION_ROUTE_CASES,
    ids=[f"{owner.replace('/', '-')}-{route}" for owner, route, *_ in _SESSION_ROUTE_CASES],
)
def test_session_start_git_routes_refuse_hostile_path_and_tripwire_bypass(
        tmp_path: Path, owner: str, route: str, function: str, method: str,
        args: tuple[str, ...] | None, expected: str) -> None:
    _session_route_exercise(tmp_path, owner, route, function, method, args, expected)
