"""Chunk P4 -- `review-brief`, `closeout --dry-run`, and the two fences around them.

Plan: ``dev/plans/review-efficient-lifecycle.md`` > the ``P4`` row.  Source
contract: ``dev/proposals/archive/2026-08-10-codex-review-efficient-lifecycle.md``
> **Revision 1** -- the operative revision, whose own opening words are *"This
section supersedes the operative requirements in the opening Proposal, Pilot,
Evidence, and Signals sections"*.  So the field lists asserted below are
Revision 1's ("Stable evidence and closeout", "Deterministic tool contract and
dependency order"), not the superseded opening ``### 5`` / ``### Tool support``.

**Which copy is under test, named rather than assumed.**  Every node here loads
``templates/skills/_lib/lifecycle.py`` -- the shipped template, the same copy
``test_lifecycle_cli.py``, ``test_lifecycle_failsafe.py``,
``test_skills_security.py`` and ``test_pilot_evidence.py`` load.  Its
byte-identical installed twin is ``tools/lifecycle.py``.  A mutation applied to
only the ``tools/`` copy is invisible to this file except through
:class:`TestTwinParity`, so a mutation run applies to **both** and restores both.

Six groups:

1. :class:`TestInterpreterFence` -- the plan's fence **M3**.  P4 does not modify
   ``_resolve_interpreter``, its schema, validation order, fallback disposition,
   warning visibility, or **any subprocess use of the resolved path**.  Pinned by
   exact function-source digests, AST-shape digests, and the exact call-site and
   argv-construction sets, on **both** copies.
2. :class:`TestTwinParity` -- byte identity for both installed twins P4 touches.
3. :class:`TestDisplayEncoder` -- ``_safe_field`` now *is* the planner's
   ``encode_display`` (F2's one terminal encoder), with elision layered outside
   it rather than folded into it.
4. :class:`TestReviewBrief` / 5. :class:`TestCloseout` -- the two commands:
   every field the operative contract names, determinism, read-only behavior,
   malformed records, control/invisible/delimiter injection, and the versioned
   ASCII-safe machine contract.
6. :class:`TestLoaderMatrixForThisConsumer` -- the A6 loader cases for this
   consumer that Chunk P6a did **not** already cover, named individually against
   the ones it did.
7. :class:`TestNoGrammarDrift` -- the heading/field rules this file's subject
   restates locally are compared against the planner's own over the live corpus.

Run from the cairn repo root:
    PYTHONDONTWRITEBYTECODE=1 python -m pytest bootstrap/tests/test_lifecycle_brief.py
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import types
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]
#: The copy the suite LOADS.
MODULE_PATH = CAIRN_ROOT / "templates" / "skills" / "_lib" / "lifecycle.py"
TWIN_PATH = CAIRN_ROOT / "tools" / "lifecycle.py"
PLANNER_PATH = CAIRN_ROOT / "templates" / "skills" / "_lib" / "lifecycle_planner.py"
PLANNER_TWIN_PATH = CAIRN_ROOT / "tools" / "lifecycle_planner.py"

pytestmark = pytest.mark.skipif(
    not (MODULE_PATH.exists() and PLANNER_PATH.exists()),
    reason="lifecycle.py / lifecycle_planner.py templates not available",
)

#: The fixed private name this consumer's loader registers its planner under.
_PRIVATE_PLANNER_NAME = "_lifecycle_cli_lifecycle_planner"


def _load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lifecycle = _load(MODULE_PATH, "cairn_lifecycle_brief")
planner = _load(PLANNER_PATH, "cairn_planner_for_brief")


@pytest.fixture(autouse=True)
def _clean_private_planner_module():
    """Purge the fixed private planner key before and after every test."""
    def _purge() -> None:
        for key in [k for k in sys.modules
                    if k == _PRIVATE_PLANNER_NAME
                    or k.startswith(_PRIVATE_PLANNER_NAME + ".")]:
            sys.modules.pop(key, None)
    _purge()
    yield
    _purge()


# ---------------------------------------------------------------------------
# 1. fence M3 -- the protected local interpreter binding
# ---------------------------------------------------------------------------
#
# `AGENTS.md` > *High-risk surfaces*: ``dev/.cairn/local-env.json``, its reader
# ``_resolve_interpreter``, "and every call site that executes the path it
# returns" are an untracked, gitignored, lockfile-uncovered **executable trust
# root**.  The P4 cell fences the chunk off all of it and routes any need to
# touch it to a new Security Review (fence **M3**).
#
# A fence nobody can observe is a promise.  These digests are the observation:
# they were derived at this chunk's implementation parent from the file's own
# bytes, and a one-character edit to any of the four pinned symbols reddens the
# byte digest; a semantics-preserving reformat still reddens the AST digest for
# any real change, and a pure comment edit is caught by the byte digest alone.
#
# **Four symbols, not one, because the fence names four things.**  The reader
# itself (`_resolve_interpreter`), its *validation order* classifier
# (`_probe_interpreter`), its *warning visibility* (`_warn_stale_once`), and the
# remedy text those warnings carry (`_REBIND_REMEDY`).  The *fallback
# disposition* and the *schema* live inside the reader and are covered by its
# own digest.

_INTERPRETER_SYMBOL_DIGESTS = {
    "_REBIND_REMEDY": (
        "55d9acf732ce90a4017d2501432a67e0c4ac18fa4ca1a4b901acd0bad75860c7",
        "ec8dd4027e858e06f71c9409b002a0bd38a6f70e1f28bf1bb51e8ab949469393",
    ),
    "_probe_interpreter": (
        "f9847b51110a413d678fa2782495d9bedbfcf6a8bd7e296911e39143d5028227",
        "b05ee00ec73ed677ea2c4924b6c4cbb0f328c83ca32f82e724cc57d0b02594c5",
    ),
    "_resolve_interpreter": (
        "dc2e88095353dfdbd41d46bcd122b4070e35aa497cac8262e7f1a57e1534d176",
        "419c0fa6d8cc8424d35a6f8e775b692dbdc9dc9343ae6a86c23316c1d5499431",
    ),
    "_warn_stale_once": (
        "d4868059458968a8470a5d02c1012d857661cba258284215816d236147e431ef",
        "160f48ecc9531a533c8c79c2dc6dba42675da6561fc9c6a6b21bcccba7ce08d6",
    ),
}

#: Every function that ASKS the resolver for a path.
_RESOLVER_CALLERS = ("_do_full_handoff", "_intent_whoami", "cmd_session_start")

#: Every function that RECEIVES a resolved interpreter path as a parameter.
_INTERPRETER_CONSUMERS = ("_prune_intents", "_run_evolution_infer",
                          "_run_lifecycle_metrics", "_surface_foldback_candidates",
                          "_surface_intents")

#: Every function that builds an argv list whose argv[0] is a resolved
#: interpreter -- i.e. every place the trust root is actually EXECUTED.
_INTERPRETER_SPAWN_SITES = ("_intent_whoami", "_prune_intents",
                            "_run_evolution_infer", "_run_lifecycle_metrics",
                            "_surface_foldback_candidates", "_surface_intents")

#: The two commands P4 adds.  Neither may reach any of the three sets above.
_P4_ENTRY_POINTS = ("cmd_review_brief", "cmd_closeout")


def _module_functions(tree: ast.Module):
    return {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}


def _named_node(tree: ast.Module, src: str, name: str):
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return node
    raise AssertionError(f"{name} is absent from the module -- the fenced "
                         f"surface must not be renamed or removed by P4")


def _digest_pair(tree: ast.Module, src: str, name: str):
    node = _named_node(tree, src, name)
    segment = ast.get_source_segment(src, node)
    assert segment is not None
    return (hashlib.sha256(segment.encode("utf-8")).hexdigest(),
            hashlib.sha256(
                ast.dump(node, include_attributes=False).encode("utf-8")
            ).hexdigest())


def _calls_named(func: ast.FunctionDef, name: str) -> bool:
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
               and n.func.id == name for n in ast.walk(func))


def _argv_starts_with_interpreter(func: ast.FunctionDef) -> bool:
    return any(isinstance(n, ast.List) and n.elts
               and isinstance(n.elts[0], ast.Name)
               and n.elts[0].id in ("interpreter", "interp")
               for n in ast.walk(func))


def _reachable(functions, roots):
    """Every module-level function reachable from `roots` by direct name call."""
    seen, stack = set(), list(roots)
    while stack:
        name = stack.pop()
        if name in seen or name not in functions:
            seen.add(name)
            continue
        seen.add(name)
        for node in ast.walk(functions[name]):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                stack.append(node.func.id)
    return seen


@pytest.mark.parametrize("path", [MODULE_PATH, TWIN_PATH],
                         ids=["template", "installed-twin"])
class TestInterpreterFence:
    """Fence M3, asserted on both copies."""

    def test_the_four_fenced_symbols_are_byte_and_ast_identical_to_the_pin(
            self, path: Path) -> None:
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src)
        actual = {name: _digest_pair(tree, src, name)
                  for name in _INTERPRETER_SYMBOL_DIGESTS}
        assert actual == _INTERPRETER_SYMBOL_DIGESTS, (
            "the protected local interpreter binding changed.  P4 is fenced off "
            "this surface (plan fence M3): a change to the resolver, its schema, "
            "validation order, fallback disposition or warning visibility STOPS "
            "for a new Security Review.  If the change is deliberate and "
            "authorized, re-derive these digests in that review's own commit."
        )

    def test_the_resolver_call_sites_are_exactly_the_pinned_set(
            self, path: Path) -> None:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        functions = _module_functions(tree)
        callers = tuple(sorted(
            name for name, node in functions.items()
            if _calls_named(node, "_resolve_interpreter")))
        assert callers == _RESOLVER_CALLERS

    def test_the_subprocess_uses_of_the_resolved_path_are_exactly_the_pinned_set(
            self, path: Path) -> None:
        """*"or any subprocess use of the resolved path"* -- the fence's own words.

        Two independent projections, because they fail differently: who *takes*
        a resolved interpreter, and who *builds an argv* that starts with one.  A
        new executor would have to evade both to land unseen.
        """
        tree = ast.parse(path.read_text(encoding="utf-8"))
        functions = _module_functions(tree)
        consumers = tuple(sorted(
            name for name, node in functions.items()
            if any(a.arg == "interpreter" for a in node.args.args)))
        spawn = tuple(sorted(
            name for name, node in functions.items()
            if _argv_starts_with_interpreter(node)))
        assert consumers == _INTERPRETER_CONSUMERS
        assert spawn == _INTERPRETER_SPAWN_SITES

    def test_neither_new_command_can_reach_the_interpreter_trust_root(
            self, path: Path) -> None:
        """The fence as a *reachability* claim, not only a byte claim.

        Pinning the resolver's bytes says P4 did not edit it.  This says P4 did
        not *wire* it: no call path from either new subcommand reaches the
        resolver, any consumer of a resolved path, or any argv that executes one.
        """
        tree = ast.parse(path.read_text(encoding="utf-8"))
        functions = _module_functions(tree)
        for entry in _P4_ENTRY_POINTS:
            assert entry in functions, f"{entry} is missing from {path.name}"
        reached = _reachable(functions, _P4_ENTRY_POINTS)
        forbidden = ({"_resolve_interpreter", "_probe_interpreter"}
                     | set(_INTERPRETER_CONSUMERS) | set(_INTERPRETER_SPAWN_SITES))
        assert reached & forbidden == set(), (
            f"a P4 command reaches the protected interpreter binding via "
            f"{sorted(reached & forbidden)} -- that is fence M3 and it stops for "
            f"a new Security Review"
        )

    def test_neither_new_command_opens_a_file_for_writing(self, path: Path) -> None:
        """*"It never edits, moves, commits, runs tests"* -- the read-only clause.

        Static, and scoped to the reachable call graph rather than the whole
        file, so `session-end`'s legitimate writes cannot mask a new one here.
        """
        tree = ast.parse(path.read_text(encoding="utf-8"))
        functions = _module_functions(tree)
        # `.replace` and `.move` are deliberately NOT in this list: `str.replace`
        # is everywhere and a static attribute name cannot tell it from
        # `Path.replace`, so including them would make this node a false alarm
        # that gets suppressed rather than read.  `open()` is judged on its MODE,
        # because the loader legitimately opens the planner `"rb"` to prove it is
        # readable before executing anything.
        writers = ("write_text", "write_bytes", "mkdir", "unlink", "rename",
                   "symlink_to", "touch", "rmtree", "copy", "copy2")
        offenders = []
        for name in sorted(_reachable(functions, _P4_ENTRY_POINTS)):
            node = functions.get(name)
            if node is None:
                continue
            for sub in ast.walk(node):
                if not (isinstance(sub, ast.Call)
                        and isinstance(sub.func, ast.Attribute)):
                    continue
                if sub.func.attr in writers:
                    offenders.append(f"{name}: .{sub.func.attr}()")
                if sub.func.attr == "open" and sub.args:
                    mode = sub.args[0]
                    if (isinstance(mode, ast.Constant)
                            and isinstance(mode.value, str)
                            and any(c in mode.value for c in "wax+")):
                        offenders.append(f"{name}: .open({mode.value!r})")
        assert offenders == [], (
            "a P4 command reaches a write primitive: " + ", ".join(offenders))

    def test_the_only_subprocess_either_command_reaches_is_read_only_git(
            self, path: Path) -> None:
        """*"deterministic, offline, standard-library-only extractors ... no LLM,
        API, telemetry, or network dependency"* -- Revision 1.

        Pinned as an exact set rather than a prohibition, so a NEW subprocess
        anywhere in the reachable graph reddens even if it looks harmless.
        """
        tree = ast.parse(path.read_text(encoding="utf-8"))
        functions = _module_functions(tree)
        spawners = sorted(
            name for name in _reachable(functions, _P4_ENTRY_POINTS)
            if name in functions and any(
                isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "run"
                and isinstance(n.func.value, ast.Name)
                and n.func.value.id == "subprocess"
                for n in ast.walk(functions[name])))
        assert spawners == ["_git", "_repo_root"], (
            f"a P4 command reaches an unexpected subprocess site: {spawners}")


# ---------------------------------------------------------------------------
# 2. twin parity
# ---------------------------------------------------------------------------


class TestTwinParity:
    """Both twins P4 touches, asserted in the same commit that changes either."""

    @pytest.mark.parametrize(
        "left,right",
        [(MODULE_PATH, TWIN_PATH), (PLANNER_PATH, PLANNER_TWIN_PATH)],
        ids=["lifecycle", "lifecycle_planner"],
    )
    def test_the_two_copies_are_byte_identical(self, left: Path, right: Path) -> None:
        assert left.read_bytes() == right.read_bytes(), (
            f"{left} and {right} have diverged -- the installed twin is what "
            f"adopters run, and reasoning about 'the' implementation is only "
            f"legitimate while they are byte-identical"
        )


# ---------------------------------------------------------------------------
# 3. the one terminal encoder
# ---------------------------------------------------------------------------


class TestDisplayEncoder:
    """P4: *"The existing `_safe_field` is not this rule ... replaced, not wrapped."*"""

    def test_safe_field_is_the_planners_encoder_and_not_a_second_table(self) -> None:
        source = MODULE_PATH.read_text(encoding="utf-8")
        assert "_FIELD_ESCAPES" not in source, (
            "the retired fixed escape table survives -- P4 replaces it with "
            "`encode_display`, and a second table is the second, weaker path"
        )
        assert "encode_display" in lifecycle._REQUIRED_EXPORTS

    @pytest.mark.parametrize("value", [
        "\u034f",            # COMBINING GRAPHEME JOINER -- Mn, isprintable() True
        "\u3164",            # HANGUL FILLER -- Lo, isprintable() True
        "\ufe0f",            # VARIATION SELECTOR-16 -- Mn, isprintable() True
        "\U000e0041",        # TAG LATIN CAPITAL LETTER A -- a shadow alphabet
        "\u200b",            # ZERO WIDTH SPACE
        "\u202e",            # RIGHT-TO-LEFT OVERRIDE
    ])
    def test_the_invisibles_the_old_table_missed_are_now_escaped(self, value) -> None:
        """Each of these reached a terminal RAW under the retired table.

        They are `Mn`/`Lo`/`Cf` code points the old escape map never listed, and
        four of the six are `str.isprintable() == True`, which is why clause 1
        alone was the rejected design.
        """
        rendered = lifecycle._safe_field(value)
        assert value not in rendered
        assert rendered == planner.encode_display(value)
        assert rendered.isascii() and rendered.isprintable()

    @pytest.mark.parametrize("value", ["a\x00b", "a\x1b[2Kb", "a\x7fb", "a\u2028b",
                                       "a\\b", "a|b", "a\tb", "a\rb"])
    def test_controls_delimiters_and_syntax_characters_are_escaped(self, value) -> None:
        rendered = lifecycle._safe_field(value)
        assert rendered == planner.encode_display(value)
        assert rendered.isascii() and rendered.isprintable()

    def test_ordinary_scientific_text_survives_readable(self) -> None:
        for value in ("café", "科学", "Δt", "café"):
            assert lifecycle._safe_field(value) == value

    def test_elision_is_layered_outside_the_encoder_not_folded_into_it(self) -> None:
        """The cut is taken from the ENCODED string, and the encoder never truncates.

        Both halves matter.  Cutting the source first would let one crafted
        character expand past the cap after encoding; folding a length rule into
        the code-point rule would make the encoder disagree with the board's,
        which is the single-encoder property this chunk exists to establish.
        """
        source = "\x1b" * 100                      # 100 chars -> 400 encoded
        rendered = lifecycle._safe_field(source)
        assert rendered.startswith("\\x1b" * 50)
        assert rendered.endswith("...[+200 chars elided]")
        assert len(rendered) == lifecycle._FIELD_LIMIT + len("...[+200 chars elided]")
        assert planner.encode_display(source) == "\\x1b" * 100  # no cap in there

    def test_a_truncated_escape_never_leaves_a_raw_unsafe_character(self) -> None:
        """Every reachable partial escape, over all three escape widths.

        The marker is unauthenticated and counts ENCODED characters, so a cut can
        land inside an escape sequence.  What must never survive is a raw control
        or invisible character; the prefix set is bounded by the three widths
        `\\xNN`, `\\uNNNN`, `\\UNNNNNNNN`.
        """
        samples = ["\x00", "\x1b", "\x7f", "\x9f", "\u200b", "\u2028", "\ufe0f",
                   "\U000e0041", "\U0010fffe"]
        widths, prefixes = set(), set()
        for source in samples:
            escaped = planner.encode_display(source)
            widths.add(len(escaped))
            for limit in range(1, len(escaped)):
                rendered = lifecycle._safe_field(source, limit=limit)
                prefix, marker = rendered.split("...", 1)
                prefixes.add(prefix)
                assert escaped.startswith(prefix)
                assert marker.startswith("[+") and marker.endswith(" chars elided]")
                assert rendered.isascii() and rendered.isprintable()
        assert widths == {4, 6, 10}
        assert all(p.startswith("\\") for p in prefixes)

    def test_an_unloadable_vocabulary_refuses_rather_than_falling_back(
            self, tmp_path) -> None:
        """No local escape table is kept in reserve for when the planner is gone.

        The alternative -- degrade to a weaker escaper exactly when something is
        already wrong with the install -- is the second path this chunk removes.
        """
        tools = tmp_path / "tools"
        tools.mkdir()
        shutil.copy(MODULE_PATH, tools / "lifecycle.py")
        module = _load(tools / "lifecycle.py", "lc_no_planner_for_safe_field")
        with pytest.raises(module.VocabularyUnavailable):
            module._safe_field("anything")


# ---------------------------------------------------------------------------
# scratch repositories for the two commands
# ---------------------------------------------------------------------------


def _git(root: Path, *args: str) -> str:
    out = subprocess.run(["git", *args], cwd=str(root), check=True,
                         capture_output=True, text=True)
    return out.stdout.strip()


def _init_repo(root: Path) -> None:
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _git(root, "config", "commit.gpgsign", "false")


_PROPOSAL = """# Proposal: a worked example

**Status**: accepted
**Author**: Someone
**Assurance path**: standard

## Proposal

Original text.

## Review -- Reviewer B -- 2026-01-02

**Tier**: External
**Findings**: raised
**Reviewed commit**: `{sha}`
**Target**: the opening Proposal
**Prior findings**: none
**Assurance path**: standard

[Q1] one thing.  [Q2] another thing.

## Response -- Someone -- 2026-01-03

[Q1] accepted.

## Revision 1 -- complete current contract

The operative contract.

### Withdrawn / superseded commitments

* None
"""

_PLAN = """# Plan: a worked example

**Source proposal**: [`worked-example`](../proposals/2026-01-01-someone-worked-example.md)
**Status**: executing
**Plan review**: required(Internal)

## Scope

Something.

## Plan review -- Reviewer C -- 2026-01-04

**Tier**: Internal
**Findings**: none
**Reviewed commit**: `{sha}`
**Target**: the operative plan sections
**Prior findings**: none
**Assurance path**: standard

## Implementation verification -- Someone -- 2026-01-05

**Boundary B mode**: bounded

## Code review -- Reviewer D -- 2026-01-06

**Model**: something
**Verdict**: SHIP.
**Findings**: none
**Reviewed commit**: `{sha}`
**Target**: the implementation range
**Prior findings**: none
**Assurance path**: standard
"""


@pytest.fixture
def repo(tmp_path) -> Path:
    """A scratch repository carrying one proposal and one plan, plus a commit."""
    root = tmp_path / "scratch"
    (root / "dev" / "proposals").mkdir(parents=True)
    (root / "dev" / "plans" / "archive").mkdir(parents=True)
    (root / "dev" / "proposals" / "archive").mkdir(parents=True)
    (root / "dev" / "PLANNING.md").write_text("# Boards\n", encoding="utf-8")
    _init_repo(root)
    (root / "seed.md").write_text("seed\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "seed")
    sha = _git(root, "rev-parse", "HEAD")
    (root / "dev" / "proposals" / "2026-01-01-someone-worked-example.md").write_text(
        _PROPOSAL.format(sha=sha), encoding="utf-8")
    (root / "dev" / "plans" / "worked-example.md").write_text(
        _PLAN.format(sha=sha), encoding="utf-8")
    (root / "later.md").write_text("later\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "artifacts")
    return root


def _run(root: Path, argv, monkeypatch, capsys):
    monkeypatch.chdir(root)
    code = lifecycle.main(argv)
    return code, capsys.readouterr()


def _run_json(root: Path, argv, monkeypatch, capsys):
    code, captured = _run(root, argv, monkeypatch, capsys)
    return code, json.loads(captured.out)


def _snapshot(root: Path):
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


# ---------------------------------------------------------------------------
# 4. review-brief
# ---------------------------------------------------------------------------


class TestReviewBrief:
    """Revision 1: *"`review-brief` reports the assurance path and tier,
    complete-current-contract span, last reviewed commit, unresolved finding ids,
    paths changed since that commit, and any Boundary B summary."*"""

    def test_every_field_the_operative_contract_names_is_present(
            self, repo, monkeypatch, capsys) -> None:
        code, payload = _run_json(
            repo, ["review-brief", "2026-01-01-someone-worked-example",
                   "--format", "json"], monkeypatch, capsys)
        assert code == 0
        # The six named fields, by name, so a silently dropped one reddens.
        for key in ("assurance_path", "tier", "current_contract",
                    "last_reviewed_commit", "findings", "changed_paths",
                    "boundary_b"):
            assert key in payload, f"the contract names {key} and it is absent"
        assert payload["schema"] == "cairn-review-brief/1"
        assert payload["kind"] == "proposal"
        assert payload["status"] == "accepted"
        assert payload["assurance_path"]["value"] == "standard"
        assert payload["tier"]["value"] == "External"
        assert payload["current_contract"][0]["heading"].startswith(
            "## Revision 1")
        assert payload["last_reviewed_commit"]["full"] is True
        assert payload["findings"]["raised"] == ["Q1", "Q2"]
        assert payload["findings"]["unanswered"] == ["Q2"]
        assert payload["changed_paths"]["available"] is True
        assert "later.md" in payload["changed_paths"]["paths"]

    def test_a_plans_assurance_path_comes_from_the_planners_chain(
            self, repo, monkeypatch, capsys) -> None:
        """A plan carries no declaration of its own -- P1 pinned that absence --
        so the value must come from P2's resolver, not from a local reading."""
        code, payload = _run_json(
            repo, ["review-brief", "worked-example", "--format", "json"],
            monkeypatch, capsys)
        assert code == 0
        assert payload["assurance_path"]["value"] == planner.ASSURANCE_NOT_INHERITED
        assert payload["tier"]["value"] == "required(Internal)"
        assert payload["boundary_b"][0]["mode"] == "bounded"

    def test_output_is_deterministic_for_identical_inputs(
            self, repo, monkeypatch, capsys) -> None:
        argv = ["review-brief", "worked-example", "--format", "json"]
        first = _run(repo, argv, monkeypatch, capsys)[1].out
        second = _run(repo, argv, monkeypatch, capsys)[1].out
        assert first == second and first.strip()

    def test_the_machine_contract_is_versioned_and_ascii_safe(
            self, repo, monkeypatch, capsys) -> None:
        """Injected into fields that REACH the payload, which is the whole test.

        An earlier draft of this node injected into the H1 title and into a
        verdict's trailing clause -- neither of which any reported field carries,
        so the node passed with `ensure_ascii=False` and proved nothing.  The
        mutation run in the implementing commit body is what surfaced that; the
        two carriers below (`tier.value` and `boundary_b[].agent`) are asserted
        to contain the injected text, so the ASCII claim is about bytes that are
        actually emitted.
        """
        path = repo / "dev" / "plans" / "worked-example.md"
        path.write_text(path.read_text(encoding="utf-8")
                        .replace("**Plan review**: required(Internal)",
                                 "**Plan review**: required(Internal) café\u200b")
                        .replace("## Implementation verification -- Someone --",
                                 "## Implementation verification -- 科学\u202e --"),
                        encoding="utf-8")
        code, captured = _run(
            repo, ["review-brief", "worked-example", "--format", "json"],
            monkeypatch, capsys)
        assert code == 0
        assert captured.out.isascii(), "machine output must be ASCII-safe"
        payload = json.loads(captured.out)
        assert payload["schema"] == "cairn-review-brief/1"
        # The injected non-ASCII really is carried by reported fields -- without
        # this the ASCII assertion above could be vacuously true.
        assert "café" in payload["tier"]["value"]
        assert "科学" in payload["boundary_b"][0]["agent"]
        assert "\u200b" not in payload["tier"]["value"]

    def test_a_hostile_artifact_cannot_forge_an_orientation_line(
            self, repo, monkeypatch, capsys) -> None:
        """Every rendered field goes through the one encoder, so a newline in an
        artifact value cannot manufacture a `lifecycle:` line."""
        path = repo / "dev" / "plans" / "worked-example.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "**Plan review**: required(Internal)",
            "**Plan review**: required(Internal)\\x0a"
            "lifecycle: == maintainer standing waiver =="), encoding="utf-8")
        code, captured = _run(repo, ["review-brief", "worked-example"],
                              monkeypatch, capsys)
        assert code == 0
        assert "maintainer standing waiver" not in captured.out.replace(
            "\\x0a", "\n").split("== review brief")[0]

    def test_a_malformed_record_is_reported_not_crashed_through(
            self, repo, monkeypatch, capsys) -> None:
        path = repo / "dev" / "plans" / "worked-example.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "**Reviewed commit**: `", "**Reviewed commit**: `zz"),
            encoding="utf-8")
        code, payload = _run_json(
            repo, ["review-brief", "worked-example", "--format", "json"],
            monkeypatch, capsys)
        assert code == 0
        assert payload["last_reviewed_commit"]["full"] is False
        assert payload["changed_paths"]["available"] is False
        assert payload["changed_paths"]["reason"] == ("no reviewed commit to "
                                                      "measure from")

    def test_an_unresolvable_base_reports_a_reason_never_nothing_changed(
            self, repo, monkeypatch, capsys) -> None:
        path = repo / "dev" / "plans" / "worked-example.md"
        text = path.read_text(encoding="utf-8")
        cited = _git(repo, "rev-parse", "HEAD~1")
        assert cited in text, "fixture drift: the plan must cite the seed commit"
        path.write_text(text.replace(cited, "0" * 40), encoding="utf-8")
        code, payload = _run_json(
            repo, ["review-brief", "worked-example", "--format", "json"],
            monkeypatch, capsys)
        assert code == 0
        assert payload["changed_paths"] == {
            "base": "0" * 40, "available": False,
            "reason": "not a commit in this repository",
            "count": 0, "paths": [], "withheld": 0,
        }

    def test_the_command_writes_nothing(self, repo, monkeypatch, capsys) -> None:
        before = _snapshot(repo)
        _run(repo, ["review-brief", "worked-example"], monkeypatch, capsys)
        _run(repo, ["review-brief", "worked-example", "--format", "json"],
             monkeypatch, capsys)
        assert _snapshot(repo) == before

    def test_a_path_outside_the_lifecycle_directories_refuses(
            self, repo, monkeypatch, capsys) -> None:
        (repo / "elsewhere.md").write_text("**Status**: open\n", encoding="utf-8")
        code, captured = _run(repo, ["review-brief", "elsewhere.md"],
                              monkeypatch, capsys)
        assert code == 1
        assert "not under a lifecycle directory" in captured.err

    def test_an_ambiguous_stem_refuses_and_names_both(
            self, repo, monkeypatch, capsys) -> None:
        shutil.copy(repo / "dev" / "plans" / "worked-example.md",
                    repo / "dev" / "plans" / "archive" / "worked-example.md")
        code, captured = _run(repo, ["review-brief", "worked-example"],
                              monkeypatch, capsys)
        assert code == 1
        assert "ambiguous" in captured.err
        assert "dev/plans/worked-example.md" in captured.err
        assert "dev/plans/archive/worked-example.md" in captured.err

    def test_a_symlinked_artifact_refuses(self, repo, monkeypatch, capsys) -> None:
        target = repo / "dev" / "plans" / "worked-example.md"
        link = repo / "dev" / "plans" / "redirected.md"
        link.symlink_to(target)
        code, captured = _run(repo, ["review-brief", "dev/plans/redirected.md"],
                              monkeypatch, capsys)
        assert code == 1
        assert "reached through a symlink" in captured.err


# ---------------------------------------------------------------------------
# 5. closeout --dry-run
# ---------------------------------------------------------------------------


class TestCloseout:
    """Revision 1: *"reports plan/proposal state, accepted commit and assurance
    path, plan-review satisfaction, Boundary B binding, latest code-review
    result, unresolved findings, unhomed follow-ups, and the exact archive/board
    paths.  It never edits, moves, commits, runs tests, or decides whether
    evidence is competent."*"""

    def test_every_field_the_operative_contract_names_is_present(
            self, repo, monkeypatch, capsys) -> None:
        code, payload = _run_json(
            repo, ["closeout", "worked-example", "--dry-run", "--format", "json"],
            monkeypatch, capsys)
        assert code == 3  # outstanding, not clean -- see the preflight below
        for key in ("status", "source_proposal", "accepted_binding",
                    "assurance_path", "plan_review", "boundary_b",
                    "code_review", "unanswered_findings", "followups",
                    "archive_paths", "preflight"):
            assert key in payload, f"the contract names {key} and it is absent"
        assert payload["schema"] == "cairn-closeout/1"
        assert payload["source_proposal"]["path"] == (
            "dev/proposals/2026-01-01-someone-worked-example.md")
        assert payload["source_proposal"]["status"] == "accepted"
        assert payload["code_review"]["verdict"] == "SHIP"
        assert payload["code_review"]["classification"] == "clearing"
        assert payload["boundary_b"][0]["date"] == "2026-01-05"

    def test_the_preflight_IS_the_shared_predicate_not_a_second_reading(
            self, repo, monkeypatch, capsys) -> None:
        """R6: *"`scan`, `next`, and accepted closeout tooling consume shared
        predicates rather than implement three interpretations of readiness."*

        Asserted by equality against the planner's own predicate over the same
        artifact and the same target state -- so the day the predicate changes,
        this command changes with it, and there is nowhere else to tighten.
        """
        art = planner.read_artifact(repo / "dev" / "plans" / "worked-example.md")
        expected = planner.status_evidence_violations(art, "ready-to-archive")
        _code, payload = _run_json(
            repo, ["closeout", "worked-example", "--dry-run", "--format", "json"],
            monkeypatch, capsys)
        assert payload["target_state"] == "ready-to-archive"
        assert payload["preflight"]["violations"] == list(expected)
        assert expected, ("sanity: this fixture must have something outstanding, "
                          "or the equality above proves nothing")

    def test_a_clean_plan_exits_zero_and_an_outstanding_one_exits_three(
            self, repo, monkeypatch, capsys) -> None:
        path = repo / "dev" / "plans" / "worked-example.md"
        code, _ = _run(repo, ["closeout", "worked-example", "--dry-run"],
                       monkeypatch, capsys)
        assert code == 3
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n## Lasting-truth migration\n\nDispositions: none outstanding.\n"
              "\nLoop fidelity: fidelity sign-off against commit `"
            + "0" * 40 + "` and the accepted contract.\n",
            encoding="utf-8")
        code, captured = _run(repo, ["closeout", "worked-example", "--dry-run"],
                              monkeypatch, capsys)
        assert code == 0, captured.out
        assert "CLEAN" in captured.out

    def test_the_exact_archive_and_board_paths_are_reported(
            self, repo, monkeypatch, capsys) -> None:
        _code, payload = _run_json(
            repo, ["closeout", "worked-example", "--dry-run", "--format", "json"],
            monkeypatch, capsys)
        assert payload["archive_paths"] == [
            {"role": "move-from", "path": "dev/plans/worked-example.md",
             "exists": True},
            {"role": "move-to", "path": "dev/plans/archive/worked-example.md",
             "exists": False},
            {"role": "board-row", "path": "dev/PLANNING.md", "exists": True},
        ]

    def test_a_blocking_code_review_is_never_summarized_as_clearing(
            self, repo, monkeypatch, capsys) -> None:
        path = repo / "dev" / "plans" / "worked-example.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "**Verdict**: SHIP.", "**Verdict**: REVISE / NOT CLEARED."),
            encoding="utf-8")
        _code, payload = _run_json(
            repo, ["closeout", "worked-example", "--dry-run", "--format", "json"],
            monkeypatch, capsys)
        assert payload["code_review"]["classification"] == "blocking"

    def test_an_out_of_vocabulary_verdict_is_unreadable_never_either_class(
            self, repo, monkeypatch, capsys) -> None:
        path = repo / "dev" / "plans" / "worked-example.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "**Verdict**: SHIP.", "**Verdict**: SHIP but actually BLOCK"),
            encoding="utf-8")
        _code, payload = _run_json(
            repo, ["closeout", "worked-example", "--dry-run", "--format", "json"],
            monkeypatch, capsys)
        assert payload["code_review"]["classification"] == "unreadable"

    def test_closeout_without_dry_run_refuses(self, repo, monkeypatch, capsys) -> None:
        code, captured = _run(repo, ["closeout", "worked-example"],
                              monkeypatch, capsys)
        assert code == 1
        assert "has no writing mode" in captured.err

    def test_closeout_on_a_proposal_refuses(self, repo, monkeypatch, capsys) -> None:
        code, captured = _run(
            repo, ["closeout", "2026-01-01-someone-worked-example", "--dry-run"],
            monkeypatch, capsys)
        assert code == 1
        assert "is a proposal, not a plan" in captured.err

    def test_the_command_writes_nothing_and_moves_nothing(
            self, repo, monkeypatch, capsys) -> None:
        before = _snapshot(repo)
        head = _git(repo, "rev-parse", "HEAD")
        _run(repo, ["closeout", "worked-example", "--dry-run"], monkeypatch, capsys)
        _run(repo, ["closeout", "worked-example", "--dry-run", "--format", "json"],
             monkeypatch, capsys)
        assert _snapshot(repo) == before
        assert _git(repo, "rev-parse", "HEAD") == head

    def test_output_is_deterministic_for_identical_inputs(
            self, repo, monkeypatch, capsys) -> None:
        argv = ["closeout", "worked-example", "--dry-run", "--format", "json"]
        first = _run(repo, argv, monkeypatch, capsys)[1].out
        second = _run(repo, argv, monkeypatch, capsys)[1].out
        assert first == second and first.strip()

    def test_the_machine_contract_is_versioned_and_ascii_safe(
            self, repo, monkeypatch, capsys) -> None:
        """Same correction as the review-brief node: inject where it is CARRIED."""
        path = repo / "dev" / "plans" / "worked-example.md"
        path.write_text(path.read_text(encoding="utf-8")
                        .replace("**Verdict**: SHIP.",
                                 "**Verdict**: SHIP\u200b\u202e.café")
                        .replace("## Implementation verification -- Someone --",
                                 "## Implementation verification -- 科学\u202e --"),
                        encoding="utf-8")
        _code, captured = _run(
            repo, ["closeout", "worked-example", "--dry-run", "--format", "json"],
            monkeypatch, capsys)
        assert captured.out.isascii()
        payload = json.loads(captured.out)
        assert payload["schema"] == "cairn-closeout/1"
        assert "科学" in payload["boundary_b"][0]["agent"]
        assert "\u200b" not in payload["code_review"]["verdict"]
        assert "\u202e" not in payload["boundary_b"][0]["agent"]


# ---------------------------------------------------------------------------
# 6. the loader matrix for this consumer -- what P6a did NOT already cover
# ---------------------------------------------------------------------------
#
# Chunk P6a built `test_pilot_evidence.py::TestVocabularyLoader` for this same
# consumer.  Already covered THERE, and deliberately not duplicated here:
#
#   * the sibling-of-the-UNRESOLVED-path derivation
#     (`test_the_planner_is_the_sibling_of_the_unresolved_module_path`);
#   * no `tools/__init__.py` shortcut (`test_no_tools_package_shortcut_exists`);
#   * a symlinked planner LEAF (`test_a_symlinked_planner_leaf_refuses`);
#   * a symlinked containing DIRECTORY, loaded THROUGH the symlink so the guard
#     is live (`test_a_symlinked_containing_directory_refuses`);
#   * an absent planner (`test_an_absent_planner_refuses_rather_than_falling_back`);
#   * a missing required export, purged not cached;
#   * a planner that raises, purged and retried cleanly;
#   * a poisoned pre-existing `sys.modules` entry.
#
# The P4 cell names five cases: *"decoy path, leaf and parent symlink,
# out-of-root, partial-import cleanup, clean retry"*.  Leaf and parent symlink
# and the clean retry are the entries above.  The three below are what was thin:
# the ambient-`sys.path` decoy, out-of-root resolution, and partial-import
# cleanup of a registered CHILD module (P6a's retry node covers the parent only).


class TestLoaderMatrixForThisConsumer:
    """A6's remaining loader cases for `tools/lifecycle.py`."""

    @staticmethod
    def _consumer(tmp_path: Path, name: str, *, with_planner: bool = True):
        tools = tmp_path / "tools"
        tools.mkdir()
        shutil.copy(MODULE_PATH, tools / "lifecycle.py")
        if with_planner:
            shutil.copy(PLANNER_PATH, tools / "lifecycle_planner.py")
        return _load(tools / "lifecycle.py", name), tools

    def test_no_ambient_sys_path_trust_even_with_a_decoy_present(
            self, tmp_path, monkeypatch) -> None:
        """A decoy `lifecycle_planner.py` first on `sys.path` is never consulted.

        The loader derives its path from this file's own location, so an
        importable module of the same name is irrelevant -- asserted on the
        returned module's `__file__` and on a value only the decoy could supply.
        """
        module, tools = self._consumer(tmp_path, "lc_decoy")
        decoy = tmp_path / "decoy_on_sys_path"
        decoy.mkdir()
        (decoy / "lifecycle_planner.py").write_text(
            "PLAN_STATES = ('DECOY',)\n"
            "ASSURANCE_PATHS = ('DECOY',)\n"
            "ASSURANCE_NOT_INHERITED = 'DECOY'\n"
            "def resolve_plan_assurance_path(path): return 'DECOY', []\n"
            "def encode_display(value): return 'DECOY'\n"
            "def read_artifact(path): return None\n"
            "def status_evidence_violations(a, s): return ['DECOY']\n"
            "def review_record_violations(a, s): return ['DECOY']\n"
            "def blocked_by_violations(a): return ['DECOY']\n"
            "def plan_inheritance_violations(a): return ['DECOY']\n",
            encoding="utf-8")
        monkeypatch.syspath_prepend(str(decoy))
        try:
            vocab = module._vocabulary()
            assert getattr(vocab, "__file__", None) == str(
                tools / "lifecycle_planner.py"), (
                "the loaded vocabulary is not the derived sibling -- an ambient "
                "sys.path decoy may have been consulted")
            assert tuple(vocab.PLAN_STATES) != ("DECOY",)
            assert module._safe_field("x") == "x"  # not the decoy's encoder
        finally:
            sys.modules.pop("lifecycle_planner", None)

    def test_out_of_root_resolution_refuses(self, tmp_path, monkeypatch) -> None:
        """`path.resolve().parent != root.resolve()` refuses.

        Stated honestly: this arm is **not** real-symlink-proved and cannot be.
        Once the two preceding checks have passed (the leaf is not a symlink and
        the containing directory is not a symlink), no real filesystem
        construction makes a resolved parent diverge from the root without an
        active TOCTOU race -- the same finding `test_lifecycle_vocabulary.py`
        records for both of its consumers.  So the exact `Path` method the guard
        calls is monkeypatched, scoped by path equality to the one object under
        test: a direct, minimal simulation of the window the guard closes, and
        the mutation run in the implementing commit body observed it red with the
        clause removed.
        """
        module, tools = self._consumer(tmp_path, "lc_out_of_root")
        planner_path = tools / "lifecycle_planner.py"
        real_resolve = Path.resolve

        def fake_resolve(self, *args, **kwargs):
            if self == planner_path:
                return tmp_path / "elsewhere" / "lifecycle_planner.py"
            return real_resolve(self, *args, **kwargs)

        monkeypatch.setattr(Path, "resolve", fake_resolve)
        with pytest.raises(module.VocabularyUnavailable,
                           match="resolves outside the expected"):
            module._vocabulary()

    def test_partial_child_cleanup_then_clean_retry(self, tmp_path) -> None:
        """A child registered mid-exec is purged with its parent, then retried.

        P6a's retry node proves the PARENT key is purged; this proves the child
        namespace is too.  A surviving `<private>.shared` is a mixed-graph risk:
        the next successful load would sit above a child from a failed one.
        """
        module, _tools = self._consumer(tmp_path, "lc_partial_child")
        private = module._PLANNER_MODULE_NAME
        real_spec_from = module._importlib_util.spec_from_file_location

        def boom_spec(name, location, **kw):
            spec = real_spec_from(name, location, **kw)

            def boom(mod):
                child = private + ".shared"
                sys.modules[child] = types.ModuleType(child)
                raise RuntimeError("boom-mid-exec")

            spec.loader.exec_module = boom
            return spec

        module._importlib_util.spec_from_file_location = boom_spec
        try:
            with pytest.raises(module.VocabularyUnavailable,
                               match="boom-mid-exec"):
                module._vocabulary()
            assert private not in sys.modules
            assert not any(n.startswith(private + ".") for n in sys.modules), (
                "a failed load left a registered child behind")
        finally:
            module._importlib_util.spec_from_file_location = real_spec_from
        module._planner_cache = None
        vocab = module._vocabulary()
        assert getattr(vocab, module._PLANNER_SENTINEL, False) is True
        assert not any(n.startswith(private + ".") for n in sys.modules)

    def test_a_checkout_under_a_symlinked_ancestor_is_not_falsely_refused(
            self, tmp_path) -> None:
        """The `94bda8b` lesson's other direction, with a REAL symlink.

        Derive from the unresolved path so the symlink guards are live; compare
        RESOLVED forms for containment so macOS's `/tmp -> /private/tmp` -- and
        the ancestor symlink built here -- is not a false refusal.
        """
        real = tmp_path / "real_checkout"
        (real / "tools").mkdir(parents=True)
        shutil.copy(MODULE_PATH, real / "tools" / "lifecycle.py")
        shutil.copy(PLANNER_PATH, real / "tools" / "lifecycle_planner.py")
        link = tmp_path / "via_symlinked_ancestor"
        link.symlink_to(real, target_is_directory=True)
        assert link.is_symlink()  # a genuine filesystem symlink, not a redirect
        module = _load(link / "tools" / "lifecycle.py", "lc_symlinked_ancestor")
        vocab = module._vocabulary()
        assert tuple(vocab.PLAN_STATES) == tuple(planner.PLAN_STATES)


# ---------------------------------------------------------------------------
# 7. no grammar drift between the subject's local rules and the planner's
# ---------------------------------------------------------------------------


class TestNoGrammarDrift:
    """The subject restates three of the planner's rules locally, to *locate*
    records rather than judge them.  A restatement that silently diverges is
    exactly the drift Chunk A's audit exists to prevent, so each is compared
    against the planner's own helper over every live artifact in this tree."""

    @staticmethod
    def _corpus():
        for folder in ("proposals", "plans"):
            base = CAIRN_ROOT / "dev" / folder
            for path in sorted(base.glob("*.md")) + sorted(
                    (base / "archive").glob("*.md")):
                if path.name != "_template.md":
                    yield path

    def test_the_corpus_is_not_empty(self) -> None:
        """A guard on the guard: an empty corpus makes every node below vacuous."""
        assert len(list(self._corpus())) > 30

    def test_heading_location_matches_the_planners(self) -> None:
        for path in self._corpus():
            text = path.read_text(encoding="utf-8")
            assert lifecycle._headings(text) == planner._heading_records(text), (
                f"heading grammar drifted on {path.name}")

    def test_the_header_region_bound_matches_the_planners(self) -> None:
        for path in self._corpus():
            text = path.read_text(encoding="utf-8")
            assert lifecycle._header_region(text) == "\n".join(
                planner._iter_header_lines(text)), (
                f"header-region bound drifted on {path.name}")

    def test_the_field_matcher_matches_the_planners(self) -> None:
        for name in ("Reviewed commit", "Target", "Prior findings",
                     "Assurance path", "Verdict", "Tier",
                     "Inherited proposal basis", "Source proposal"):
            assert (lifecycle._field_pattern(name).pattern
                    == planner._code_review_field_re(name).pattern), (
                f"field grammar drifted for {name!r}")

    def test_the_current_contract_rule_matches_the_planners(self) -> None:
        for path in self._corpus():
            text = path.read_text(encoding="utf-8")
            mine = [line for line, level, _raw, norm in lifecycle._headings(text)
                    if level == 2 and lifecycle._CONTRACT_NORM_RE.match(norm)]
            theirs = [line for line, level, _raw, norm
                      in planner._heading_records(text)
                      if level == 2 and planner._CURRENT_CONTRACT_NORM_RE.match(norm)]
            assert mine == theirs, f"revision-section rule drifted on {path.name}"

    def test_the_stable_evidence_and_code_review_patterns_match_the_planners(
            self) -> None:
        assert (lifecycle._STABLE_EVIDENCE_LINE_RE.pattern
                == planner._STABLE_EVIDENCE_RE.pattern)
        assert (lifecycle._CODE_REVIEW_LINE_RE.pattern
                == planner._CODE_REVIEW_PASS_RE.pattern)

    def test_the_verdict_clause_rule_matches_the_planners(self) -> None:
        """The one that actually drifted while this chunk was being written.

        A hand-rolled `split('.')[0].split(',')[0]` classified
        `REVISE / NOT CLEARED.` as *unreadable* where the planner reads `REVISE`
        -- i.e. a blocking pass silently lost its class.  The rule is the
        planner's expression, and this node is why the divergence is not
        available to be reintroduced.
        """
        assert (lifecycle._VERDICT_CLAUSE_SUB_RE.pattern
                == planner._VERDICT_CLAUSE_RE.pattern)
        assert (lifecycle._EMPHASIS_SUB_RE.pattern
                == planner._EMPHASIS_RE.pattern)
        assert lifecycle._HEADING_EMPHASIS_CHARS == "*_`"


# ---------------------------------------------------------------------------
# 8. the two commands run against this repository's own live tree
# ---------------------------------------------------------------------------


def test_both_commands_run_over_this_repositorys_own_artifacts() -> None:
    """A smoke oracle the synthetic fixtures cannot supply: real bytes.

    Runs the installed twin as a subprocess against Cairn's own tree, which is
    where the corpus's real shapes live (multi-line `Plan review:` values,
    backticked commit ids, nine rounds of appended reviews).  Accepts 0 or 3 --
    3 is "outstanding items", a legitimate answer for a plan mid-execution.
    """
    for argv, allowed in (
        (["review-brief", "review-efficient-lifecycle", "--format", "json"], {0}),
        (["closeout", "review-efficient-lifecycle", "--dry-run",
          "--format", "json"], {0, 3}),
    ):
        out = subprocess.run(
            [sys.executable, str(TWIN_PATH), *argv],
            cwd=str(CAIRN_ROOT), capture_output=True, text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        assert out.returncode in allowed, out.stderr
        payload = json.loads(out.stdout)
        assert payload["schema"].startswith("cairn-")
        assert out.stdout.isascii()
