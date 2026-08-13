"""Tests for the monitoring-evidence engine in the lifecycle CLI (Chunk P6a).

Plan: ``dev/plans/review-efficient-lifecycle.md`` > the ``P6a`` row, as revised
by that plan's "Maintainer-directed contract revision -- 2026-08-11" (cell
``P6-R``: the machinery is **monitoring evidence**, and "No reader or writer may
treat absent monitoring activation as disabling the review policy").

**Which copy is under test, named rather than assumed.**  These tests load
``templates/skills/_lib/lifecycle.py`` -- the shipped template, the same copy
``test_lifecycle_cli.py`` and ``test_lifecycle_failsafe.py`` load.  Its
byte-identical installed twin is ``tools/lifecycle.py``, and
:func:`test_the_two_lifecycle_copies_are_byte_identical` is what makes reasoning
about "the" implementation legitimate.  A mutation applied to only one copy is
invisible to this file except through that one node, so a mutation run applies
to **both** and restores both.

Four groups:

1. ``TestVocabularyLoader`` -- the contained loader for the third consumer of
   the one runtime status vocabulary (the A3/A5 contract), and the fail-closed
   behavior of the counting rule while the vocabulary has no counted state.
2. ``TestActivationRecord`` -- the immutable activation record: derived enabling
   commit and activation date, the machinery binding, and every malformed /
   tampered / redirected shape refusing rather than reading as "inactive".
3. ``TestEventLedger`` -- the append-only ledger: bounded closed schema,
   duplicate and conflicting stems, altered or removed prior events, the
   expected-old append, and the writer's git bindings.
4. ``TestDerivedReport`` -- counts, pauses, window arithmetic on the boundary
   days, the monitoring boundary, and the direction rule: an absent activation
   record reports "no evidence yet" and never "policy disabled".

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_pilot_evidence.py
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]
#: The copy the suite LOADS.  Named explicitly: mutating the other one proves
#: nothing about these assertions.
MODULE_PATH = CAIRN_ROOT / "templates" / "skills" / "_lib" / "lifecycle.py"
TWIN_PATH = CAIRN_ROOT / "tools" / "lifecycle.py"
PLANNER_PATH = CAIRN_ROOT / "templates" / "skills" / "_lib" / "lifecycle_planner.py"
LEDGER_PATH = CAIRN_ROOT / "dev" / "measurement" / "pilot-events.md"

pytestmark = pytest.mark.skipif(
    not (MODULE_PATH.exists() and PLANNER_PATH.exists()),
    reason="lifecycle.py / lifecycle_planner.py templates not available",
)

#: The fixed private name this consumer's loader registers its planner under.
_PRIVATE_PLANNER_NAME = "_lifecycle_cli_lifecycle_planner"

#: The plan state the six-plan rule counts.  Written here as an independent
#: oracle -- the subject reads it from the planner, this file does not import the
#: subject's constant, so a rename in the subject is a visible failure.
COUNTED_STATE = "ready-to-archive"


#: The minimal planner surface `_REQUIRED_EXPORTS` names.  P2 added three
#: names to it ([CF1]: a counted plan's resolved assurance path), so a stub
#: that declares only `PLAN_STATES` is now legitimately "missing an export"
#: -- which is what `test_a_planner_missing_a_required_export_is_purged_not_
#: cached` asserts.  These two nodes are about *other* loader properties, so
#: they get a complete stub.
#:
#: **Chunk P4 added six more**, and the two nodes that use this stub reddened the
#: day it landed -- correctly, which is the point: the completeness check is what
#: makes a partially-exporting planner a refusal rather than an `AttributeError`
#: at the first counted plan.  Kept in step here rather than loosened there.
def _stub_vocabulary(state: str = COUNTED_STATE) -> str:
    return (f"PLAN_STATES = ('open', {state!r})\n"
            "ASSURANCE_PATHS = ('standard', 'high-assurance')\n"
            "ASSURANCE_NOT_INHERITED = 'not-inherited'\n"
            "def resolve_plan_assurance_path(path):\n"
            "    return 'standard', []\n"
            "def encode_display(value):\n"
            "    return value\n"
            "def read_artifact(path):\n"
            "    return None\n"
            "def status_evidence_violations(art, state):\n"
            "    return []\n"
            "def review_record_violations(art, state):\n"
            "    return []\n"
            "def blocked_by_violations(art):\n"
            "    return []\n"
            "def plan_inheritance_violations(art):\n"
            "    return []\n")


def _load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lifecycle = _load(MODULE_PATH, "cairn_lifecycle_pilot")


@pytest.fixture(autouse=True)
def _clean_private_planner_module():
    """Purge the fixed private planner key before and after every test.

    The name is fixed, so a module cached by one test's loader leaks into the
    next test's ``existing = sys.modules.get(...)`` check through the shared
    process ``sys.modules``.
    """
    def _purge() -> None:
        for key in [k for k in sys.modules
                    if k == _PRIVATE_PLANNER_NAME
                    or k.startswith(_PRIVATE_PLANNER_NAME + ".")]:
            sys.modules.pop(key, None)
    _purge()
    yield
    _purge()


@pytest.fixture(scope="module")
def lifecycle_ready(tmp_path_factory) -> ModuleType:
    """The same subject beside a planner whose vocabulary HAS the counted state.

    A copy of the real planner with one appended line, not a hand-written stub:
    the counting rule has to be exercised against the real vocabulary module.

    **Chunk E landed the token, so this fixture is now the same shape as the real
    tree** (the appended line is a harmless duplicate -- the counting rule tests
    membership).  It is kept rather than replaced by the plain module for one
    reason: it is the fixture the ~15 window/count/pause nodes below already use,
    and rewriting them to the plain module would be churn that touches every one
    of them while changing nothing they assert.  The pair that *does* the work
    post-E is this one and `lifecycle_without_counted_state` below.
    """
    tools = tmp_path_factory.mktemp("ready_tools")
    shutil.copy(MODULE_PATH, tools / "lifecycle.py")
    (tools / "lifecycle_planner.py").write_text(
        PLANNER_PATH.read_text(encoding="utf-8")
        + f"\n\n# test-only: the Chunk E token, appended to the real vocabulary\n"
        f"PLAN_STATES = PLAN_STATES + ({COUNTED_STATE!r},)\n",
        encoding="utf-8",
    )
    return _load(tools / "lifecycle.py", "cairn_lifecycle_pilot_ready")


@pytest.fixture(scope="module")
def lifecycle_without_counted_state(tmp_path_factory) -> ModuleType:
    """The subject beside a planner whose vocabulary LACKS the counted state.

    **The inverse of `lifecycle_ready`, and the reason the fail-closed path did
    not become dead code when Chunk E landed.**

    Before Chunk E the real vocabulary had no `ready-to-archive`, so the
    fail-closed branch -- `MonitoringIncomplete`, the ``UNAVAILABLE / 6`` report
    line, `pilot-record`'s refusal -- was exercised by the real tree and the
    *positive* path needed a fixture.  Chunk E inverted that.  Deleting those
    nodes would have left three live code paths in ``lifecycle.py`` with no test,
    which is exactly the silent-tool defect `AGENTS.md` forbids; so the fixture is
    inverted instead and every assertion is preserved verbatim.

    It is not a hypothetical.  Chunk H1 edits these same tuples (it moves `open` /
    `executing` / `review` into the historical sets), and a future rename or a
    partially-applied vocabulary migration is precisely the condition the branch
    exists to survive.  A copy of the real planner with the token filtered out --
    not a stub -- so what is under test is the real module minus one entry.
    """
    tools = tmp_path_factory.mktemp("unready_tools")
    shutil.copy(MODULE_PATH, tools / "lifecycle.py")
    (tools / "lifecycle_planner.py").write_text(
        PLANNER_PATH.read_text(encoding="utf-8")
        + "\n\n# test-only: the counted state REMOVED from the real vocabulary,\n"
        "# so the fail-closed counting path keeps a witness after Chunk E.\n"
        f"PLAN_STATES = tuple(s for s in PLAN_STATES if s != {COUNTED_STATE!r})\n",
        encoding="utf-8",
    )
    return _load(tools / "lifecycle.py", "cairn_lifecycle_pilot_unready")


# --- scratch repository helpers ----------------------------------------------


def _git(root: Path, *args: str, date: str | None = None) -> str:
    env = None
    if date is not None:
        env = dict(os.environ)
        env["GIT_AUTHOR_DATE"] = f"{date}T12:00:00+00:00"
        env["GIT_COMMITTER_DATE"] = f"{date}T12:00:00+00:00"
    out = subprocess.run(["git", *args], cwd=str(root), check=True,
                         capture_output=True, text=True, env=env)
    return out.stdout.strip()


def _init_repo(root: Path) -> None:
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _git(root, "config", "commit.gpgsign", "false")


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _commit(root: Path, subject: str, *rels: str, date: str | None = None) -> str:
    _git(root, "add", "--", *rels)
    _git(root, "commit", "-q", "-m", subject, date=date)
    return _git(root, "rev-parse", "HEAD")


ACTIVATION_REL = "dev/measurement/pilot-activation.md"
EVENTS_REL = "dev/measurement/pilot-events.md"
B2_SECTION = "Implementation verification -- test -- 2026-01-01"


def _activation_text(machinery: str, *, schema: str = "cairn-pilot-activation/1",
                     record_path: str = "dev/plans/p.md",
                     section: str = B2_SECTION,
                     extra: str = "", drop: str = "") -> str:
    rows = [
        f"schema: {schema}",
        f"machinery_sha: {machinery}",
        f"machinery_record_path: {record_path}",
        f"machinery_record_section: {section}",
    ]
    rows = [r for r in rows if not (drop and r.startswith(drop + ":"))]
    if extra:
        rows.append(extra)
    body = "\n".join(rows)
    return (
        "# Monitoring-evidence activation\n\nProse a human reads.\n\n"
        f"```cairn-pilot-activation\n{body}\n```\n"
    )


def _event_text(*blocks: str) -> str:
    header = "# Event ledger\n\nProse a human reads.\n\n## Events\n\n"
    return header + "\n".join(blocks)


#: The schema the subject reads, written here as an INDEPENDENT oracle -- these
#: helpers do not import the subject's `_EVENT_SCHEMA`, so a version bump in the
#: subject is a visible failure in this file rather than a silent agreement.
#: Bumped to /2 by Chunk P2, which added the `assurance_path` key ([CF1]).
EVENT_SCHEMA = "cairn-pilot-event/2"

#: The eligible assurance path, and the closed set an event may carry -- likewise
#: independent oracles.  The subject reads all three tokens from the planner
#: through its contained loader; this file types them, so a fork or a rename in
#: either place is a visible failure.
ELIGIBLE_ASSURANCE = "standard"
ASSURANCE_VALUES = ("standard", "high-assurance", "not-inherited")


def _counted_block(subject: str, date: str, commit: str, *,
                   artifact: str = "dev/plans/p.md",
                   state: str = COUNTED_STATE,
                   assurance: str | None = ELIGIBLE_ASSURANCE,
                   schema: str = EVENT_SCHEMA,
                   high: int = 0, low: int = 0, prompts: int = 0,
                   bytes_: int = 100, removed: int = 1) -> str:
    """One `plan-counted` block.  `assurance=None` OMITS the key, which is how
    the /2 mandatory-key nodes exercise the refusal."""
    assurance_row = "" if assurance is None else f"assurance_path: {assurance}\n"
    return (
        "```cairn-pilot-event\n"
        f"schema: {schema}\n"
        "kind: plan-counted\n"
        f"date: {date}\n"
        f"subject: {subject}\n"
        f"source_artifact: {artifact}\n"
        f"source_commit: {commit}\n"
        f"plan_state: {state}\n"
        f"{assurance_row}"
        f"review_input_bytes: {bytes_}\n"
        f"transitions_removed: {removed}\n"
        f"escaped_findings_high: {high}\n"
        f"escaped_findings_low: {low}\n"
        f"maintainer_prompts: {prompts}\n"
        "```\n"
    )


def _pause_block(subject: str, date: str, commit: str, *, kind: str = "pause-set",
                 severity: str = "high", artifact: str = "dev/plans/p.md") -> str:
    rows = [
        f"schema: {EVENT_SCHEMA}",
        f"kind: {kind}",
        f"date: {date}",
        f"subject: {subject}",
        f"source_artifact: {artifact}",
        f"source_commit: {commit}",
    ]
    if kind == "pause-set":
        rows.append(f"severity: {severity}")
    return "```cairn-pilot-event\n" + "\n".join(rows) + "\n```\n"


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """A scratch repo with a machinery commit and a Boundary-B2 evidence record.

    Three commits, in the order the real contract requires:
    ``machinery`` -> the plan carrying the B2 section that names it -> (the test
    adds the activation record, which becomes the derived enabling commit).
    """
    root = tmp_path.resolve()
    _init_repo(root)
    _write(root, "README.md", "base\n")
    machinery = _commit(root, "the reviewed machinery", "README.md",
                        date="2026-01-01")
    _write(root, "dev/plans/p.md",
           "# Plan\n\n**Status**: executing\n\n"
           f"## {B2_SECTION}\n\n"
           f"Tested SHA {machinery}, canonical interpreter, clean tree.\n\n"
           "## Another section\n\nnot the evidence.\n")
    _commit(root, "the B2 evidence record", "dev/plans/p.md", date="2026-01-02")
    (root / "dev" / "measurement").mkdir(parents=True, exist_ok=True)
    _MACHINERY[str(root)] = machinery
    return root


#: The machinery commit per scratch repo, held in memory rather than in a file:
#: an untracked helper file in the scratch tree would make
#: `test_the_report_stores_nothing`'s clean-tree assertion untrue for a reason
#: that has nothing to do with the subject.
_MACHINERY: dict = {}


def _machinery(repo: Path) -> str:
    return _MACHINERY[str(repo)]


def _head(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD")


def _activate(repo: Path, *, date: str = "2026-02-01", **kwargs) -> str:
    """Land the activation record; return the derived enabling commit."""
    _write(repo, ACTIVATION_REL, _activation_text(_machinery(repo), **kwargs))
    return _commit(repo, "P6d: activate the evidence window", ACTIVATION_REL,
                   date=date)


# ---------------------------------------------------------------------------
# 1. the contained loader + the counting-rule dependency
# ---------------------------------------------------------------------------


class TestVocabularyLoader:
    """A3/A5's contained-loader contract, restated for this third consumer."""

    def test_the_planner_is_the_sibling_of_the_unresolved_module_path(self) -> None:
        path = lifecycle._validated_planner_path()
        assert path == MODULE_PATH.absolute().parent / "lifecycle_planner.py"
        assert path.is_file()

    def test_no_tools_package_shortcut_exists(self) -> None:
        # The loader must not be reachable by manufacturing a package; the
        # contract forbids `tools/__init__.py` outright.
        assert not (CAIRN_ROOT / "tools" / "__init__.py").exists()

    def test_a_symlinked_planner_leaf_refuses(self, tmp_path) -> None:
        tools = tmp_path / "tools"
        tools.mkdir()
        shutil.copy(MODULE_PATH, tools / "lifecycle.py")
        real = tmp_path / "elsewhere.py"
        real.write_text("PLAN_STATES = ('open',)\n", encoding="utf-8")
        (tools / "lifecycle_planner.py").symlink_to(real)
        module = _load(tools / "lifecycle.py", "lc_leaf_symlink")
        with pytest.raises(module.VocabularyUnavailable, match="is a symlink"):
            module._validated_planner_path()

    def test_a_symlinked_containing_directory_refuses(self, tmp_path) -> None:
        real_tools = tmp_path / "real_tools"
        real_tools.mkdir()
        shutil.copy(MODULE_PATH, real_tools / "lifecycle.py")
        (real_tools / "lifecycle_planner.py").write_text(
            "PLAN_STATES = ('open',)\n", encoding="utf-8")
        link = tmp_path / "tools"
        link.symlink_to(real_tools, target_is_directory=True)
        # Loaded THROUGH the symlink, so __file__ is unresolved and the guard is
        # live -- the defect fixed at 94bda8b was resolving first, which makes
        # this question unaskable.
        module = _load(link / "lifecycle.py", "lc_dir_symlink")
        with pytest.raises(module.VocabularyUnavailable,
                           match="containing directory .* is a symlink"):
            module._validated_planner_path()

    def test_an_absent_planner_refuses_rather_than_falling_back(self, tmp_path) -> None:
        tools = tmp_path / "tools"
        tools.mkdir()
        shutil.copy(MODULE_PATH, tools / "lifecycle.py")
        module = _load(tools / "lifecycle.py", "lc_absent_planner")
        with pytest.raises(module.VocabularyUnavailable,
                           match="no status vocabulary beside this tool"):
            module._vocabulary()

    def test_a_planner_missing_a_required_export_is_purged_not_cached(
            self, tmp_path) -> None:
        tools = tmp_path / "tools"
        tools.mkdir()
        shutil.copy(MODULE_PATH, tools / "lifecycle.py")
        (tools / "lifecycle_planner.py").write_text(
            "SOMETHING_ELSE = 1\n", encoding="utf-8")
        module = _load(tools / "lifecycle.py", "lc_missing_export")
        with pytest.raises(module.VocabularyUnavailable, match="is missing"):
            module._vocabulary()
        assert _PRIVATE_PLANNER_NAME not in sys.modules
        assert module._planner_cache is None

    def test_a_planner_that_raises_is_purged_and_retried_cleanly(
            self, tmp_path) -> None:
        tools = tmp_path / "tools"
        tools.mkdir()
        shutil.copy(MODULE_PATH, tools / "lifecycle.py")
        planner = tools / "lifecycle_planner.py"
        planner.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
        module = _load(tools / "lifecycle.py", "lc_raising_planner")
        with pytest.raises(module.VocabularyUnavailable, match="failed to load"):
            module._vocabulary()
        assert _PRIVATE_PLANNER_NAME not in sys.modules
        # Clean retry: the same loader succeeds once the planner is repaired.
        planner.write_text(_stub_vocabulary(), encoding="utf-8")
        assert module._counted_plan_state() == COUNTED_STATE

    def test_a_poisoned_preexisting_sys_modules_entry_is_not_trusted(
            self, tmp_path) -> None:
        tools = tmp_path / "tools"
        tools.mkdir()
        shutil.copy(MODULE_PATH, tools / "lifecycle.py")
        (tools / "lifecycle_planner.py").write_text(
            _stub_vocabulary(), encoding="utf-8")
        module = _load(tools / "lifecycle.py", "lc_poisoned_entry")
        poison = ModuleType(_PRIVATE_PLANNER_NAME)
        poison.PLAN_STATES = ("whatever-the-attacker-wants",)
        poison.__file__ = "/not/the/planner.py"
        sys.modules[_PRIVATE_PLANNER_NAME] = poison
        # No sentinel and the wrong __file__: replaced, never believed.
        assert module._counted_plan_state() == COUNTED_STATE
        assert sys.modules[_PRIVATE_PLANNER_NAME] is not poison

    def test_the_counting_rule_resolves_against_the_landed_vocabulary(self) -> None:
        """**The positive node the red-by-construction one asked for.**

        Its predecessor asserted `COUNTED_STATE not in planner.PLAN_STATES` and
        was red-by-construction the day Chunk E landed, with the remedy in its own
        docstring: *"Chunk E has landed: replace this node with the positive one."*
        This is that replacement, and it is the stronger direction -- it exercises
        the counting rule against the REAL vocabulary module the shipped tool
        loads, not against a fixture.
        """
        planner = _load(PLANNER_PATH, "planner_for_dependency_check")
        assert COUNTED_STATE in planner.PLAN_STATES, (
            "Chunk E's vocabulary regressed: the six-plan counting rule keys on "
            f"{COUNTED_STATE!r} and the single runtime vocabulary no longer "
            "declares it")
        assert lifecycle._counted_plan_state() == COUNTED_STATE

    def test_the_counting_rule_still_fails_closed_if_the_token_ever_goes_away(
            self, lifecycle_without_counted_state) -> None:
        """The fail-closed branch, kept under test rather than left to rot.

        Every assertion is the predecessor node's, verbatim; only the subject
        changed, from the real planner (which lacked the token before Chunk E) to
        a copy with the token filtered out.  Chunk H1 edits these same tuples, so
        "the vocabulary lost a token the engine needs" stays a reachable state --
        and an unavailable count must never quietly read as zero.
        """
        with pytest.raises(lifecycle_without_counted_state.MonitoringIncomplete) \
                as excinfo:
            lifecycle_without_counted_state._counted_plan_state()
        message = str(excinfo.value)
        assert COUNTED_STATE in message
        assert "Chunk E" in message
        assert "not the same as zero" in message

    def test_the_counted_state_is_never_substituted_by_another_state(self) -> None:
        """`review` was the pre-`archived` state before Chunk E and would have
        made the count *run* against a different rule.  The engine must key on the
        contract's own state and no neighbour -- asserted against an independent
        oracle (`COUNTED_STATE` is written in this file, never imported from the
        subject), so a rename in the subject is a visible failure."""
        planner = _load(PLANNER_PATH, "planner_for_substitution_check")
        assert lifecycle._COUNTED_PLAN_STATE == COUNTED_STATE
        assert lifecycle._COUNTED_PLAN_STATE != "review"
        assert lifecycle._COUNTED_PLAN_STATE != "archived"
        # And the neighbours it must not have drifted onto are still distinct
        # states, so the assertion above is a real discrimination.
        assert {"review", "archived"} <= set(planner.PLAN_STATES)


# ---------------------------------------------------------------------------
# 2. the immutable activation record
# ---------------------------------------------------------------------------


class TestActivationRecord:

    def test_absent_record_is_no_evidence_yet_not_a_disabled_policy(self, repo) -> None:
        assert lifecycle._read_activation(repo) is None

    def test_the_enabling_commit_and_date_are_derived_from_git(self, repo) -> None:
        enabling = _activate(repo, date="2026-02-01")
        record = lifecycle._read_activation(repo)
        assert record["enabling_commit"] == enabling
        assert record["activation_date"] == "2026-02-01"
        assert record["machinery_sha"] == _machinery(repo)
        # Nothing self-referential: neither derived fact is in the file.
        text = (repo / ACTIVATION_REL).read_text(encoding="utf-8")
        assert enabling not in text
        assert "2026-02-01" not in text

    def test_the_first_introduction_of_the_exact_bytes_is_the_activation(
            self, repo) -> None:
        """A later commit that restores the same bytes must not move the date."""
        first = _activate(repo, date="2026-02-01")
        text = (repo / ACTIVATION_REL).read_text(encoding="utf-8")
        (repo / ACTIVATION_REL).unlink()
        _git(repo, "add", "-A", "--", ACTIVATION_REL)
        _git(repo, "commit", "-q", "-m", "remove it", date="2026-03-01")
        _write(repo, ACTIVATION_REL, text)
        _commit(repo, "put the same bytes back", ACTIVATION_REL, date="2026-04-01")
        record = lifecycle._read_activation(repo)
        assert record["enabling_commit"] == first
        assert record["activation_date"] == "2026-02-01"

    def test_an_untracked_record_refuses(self, repo) -> None:
        _write(repo, ACTIVATION_REL, _activation_text(_machinery(repo)))
        with pytest.raises(lifecycle.LifecycleError, match="not tracked at HEAD"):
            lifecycle._read_activation(repo)

    def test_a_record_modified_in_place_refuses(self, repo) -> None:
        _activate(repo)
        path = repo / ACTIVATION_REL
        path.write_text(path.read_text(encoding="utf-8") + "\ntampered\n",
                        encoding="utf-8")
        with pytest.raises(lifecycle.LifecycleError,
                           match="differ from the bytes committed at HEAD"):
            lifecycle._read_activation(repo)

    def test_an_unknown_schema_version_refuses_and_never_reads_as_inactive(
            self, repo) -> None:
        _activate(repo, schema="cairn-pilot-activation/2")
        with pytest.raises(lifecycle.LifecycleError) as excinfo:
            lifecycle._read_activation(repo)
        message = str(excinfo.value)
        assert "unknown schema" in message
        assert "NOT an inactive monitoring window" in message

    def test_an_unknown_key_refuses(self, repo) -> None:
        _activate(repo, extra="window_days: 9999")
        with pytest.raises(lifecycle.LifecycleError, match="unknown key"):
            lifecycle._read_activation(repo)

    def test_a_missing_mandatory_key_refuses(self, repo) -> None:
        _activate(repo, drop="machinery_record_section")
        with pytest.raises(lifecycle.LifecycleError, match="missing mandatory key"):
            lifecycle._read_activation(repo)

    def test_two_activation_blocks_refuse(self, repo) -> None:
        text = _activation_text(_machinery(repo))
        _write(repo, ACTIVATION_REL, text + "\n" + text)
        _commit(repo, "two blocks", ACTIVATION_REL)
        with pytest.raises(lifecycle.LifecycleError,
                           match="expected exactly one"):
            lifecycle._read_activation(repo)

    def test_a_short_machinery_sha_refuses(self, repo) -> None:
        _write(repo, ACTIVATION_REL, _activation_text(_machinery(repo)[:12]))
        _commit(repo, "short sha", ACTIVATION_REL)
        with pytest.raises(lifecycle.LifecycleError,
                           match="full 40-character lowercase hex"):
            lifecycle._read_activation(repo)

    def test_a_machinery_sha_that_is_not_a_commit_refuses(self, repo) -> None:
        _write(repo, ACTIVATION_REL, _activation_text("0" * 40))
        _commit(repo, "absent sha", ACTIVATION_REL)
        with pytest.raises(lifecycle.LifecycleError, match="is not a commit"):
            lifecycle._read_activation(repo)

    def test_a_machinery_sha_that_is_not_an_ancestor_refuses(self, repo) -> None:
        """A commit on a divergent branch is reachable by id but is not in the
        enabling commit's history, so it cannot be the machinery that was
        reviewed before the window opened."""
        trunk = _git(repo, "rev-parse", "--abbrev-ref", "HEAD")
        _git(repo, "checkout", "-q", "-b", "side")
        _write(repo, "side.txt", "side\n")
        side = _commit(repo, "work on a divergent branch", "side.txt")
        _git(repo, "checkout", "-q", trunk)
        _write(repo, ACTIVATION_REL, _activation_text(side))
        _commit(repo, "bind to an unreachable commit", ACTIVATION_REL)
        with pytest.raises(lifecycle.LifecycleError,
                           match="not a strict ancestor"):
            lifecycle._read_activation(repo)

    def test_the_machinery_binding_oracle_refuses_an_unattested_commit(
            self, repo) -> None:
        """P6c's activation-binding oracle, in engine terms: `machinery_sha`
        must be the commit the named Boundary-B2 record actually attests."""
        _write(repo, "unrelated.txt", "u\n")
        unrelated = _commit(repo, "an ancestor the B2 record never names",
                            "unrelated.txt")
        _write(repo, ACTIVATION_REL, _activation_text(unrelated))
        _commit(repo, "bind to an unattested ancestor", ACTIVATION_REL)
        with pytest.raises(lifecycle.LifecycleError,
                           match="does not name machinery_sha"):
            lifecycle._read_activation(repo)

    def test_a_missing_evidence_section_refuses(self, repo) -> None:
        _activate(repo, section="Implementation verification -- nobody -- 1999-01-01")
        with pytest.raises(lifecycle.LifecycleError, match="no `## .*` section"):
            lifecycle._read_activation(repo)

    def test_an_absent_evidence_record_path_refuses(self, repo) -> None:
        _activate(repo, record_path="dev/plans/not-there.md")
        with pytest.raises(lifecycle.LifecycleError,
                           match="does not exist at the enabling commit"):
            lifecycle._read_activation(repo)

    def test_the_binding_reads_the_named_section_not_the_whole_file(
            self, repo) -> None:
        """A sha named in a *different* section of the same file is not
        attestation -- the record names one section and that section binds."""
        machinery = _machinery(repo)
        _write(repo, "dev/plans/p.md",
               "# Plan\n\n"
               f"## {B2_SECTION}\n\nno sha here.\n\n"
               f"## Another section\n\nTested SHA {machinery}.\n")
        _commit(repo, "move the sha out of the named section", "dev/plans/p.md")
        _activate(repo)
        with pytest.raises(lifecycle.LifecycleError,
                           match="does not name machinery_sha"):
            lifecycle._read_activation(repo)

    def test_a_symlinked_record_leaf_refuses(self, repo) -> None:
        real = repo / "elsewhere.md"
        real.write_text(_activation_text(_machinery(repo)), encoding="utf-8")
        (repo / ACTIVATION_REL).symlink_to(real)
        with pytest.raises(lifecycle.LifecycleError, match="reached through a symlink"):
            lifecycle._read_activation(repo)

    def test_a_symlinked_parent_directory_refuses(self, repo) -> None:
        measurement = repo / "dev" / "measurement"
        shutil.rmtree(measurement)
        real = repo / "real_measurement"
        real.mkdir()
        (real / "pilot-activation.md").write_text(
            _activation_text(_machinery(repo)), encoding="utf-8")
        measurement.symlink_to(real, target_is_directory=True)
        with pytest.raises(lifecycle.LifecycleError, match="reached through a symlink"):
            lifecycle._read_activation(repo)

    def test_a_checkout_under_a_symlinked_ancestor_is_not_falsely_refused(
            self, tmp_path) -> None:
        """The root-bounded symlink walk: what must not be a symlink is the part
        of the path the repository owns, not the path to the repository."""
        real = tmp_path / "real_root"
        real.mkdir()
        _init_repo(real)
        _write(real, "README.md", "x\n")
        _commit(real, "base", "README.md")
        (real / "dev" / "measurement").mkdir(parents=True)
        link = tmp_path / "linked_root"
        link.symlink_to(real, target_is_directory=True)
        assert lifecycle._has_symlink_component_below(
            link / "dev" / "measurement" / "pilot-events.md", link) is False


# ---------------------------------------------------------------------------
# 3. the append-only ledger
# ---------------------------------------------------------------------------


class TestEventLedger:

    def _ledger(self, repo: Path, *blocks: str, commit: bool = True) -> None:
        _write(repo, EVENTS_REL, _event_text(*blocks))
        if commit:
            _commit(repo, "ledger", EVENTS_REL)

    def test_the_shipped_ledger_parses_to_zero_events(self) -> None:
        """The documented example in the real ledger must be inert."""
        text = LEDGER_PATH.read_text(encoding="utf-8")
        assert lifecycle._parse_fenced_records(
            text, lifecycle._EVENT_FENCE, "shipped") == []
        assert lifecycle._parse_fenced_records(
            text, lifecycle._ACTIVATION_FENCE, "shipped") == []

    def test_a_documented_example_inside_another_fence_is_not_data(self) -> None:
        text = ("prose\n\n```text\n```cairn-pilot-event\n"
                "schema: cairn-pilot-event/1\nkind: plan-counted\n```\n```\n")
        assert lifecycle._parse_fenced_records(
            text, lifecycle._EVENT_FENCE, "doc") == []

    def test_an_unterminated_block_refuses(self) -> None:
        text = "```cairn-pilot-event\nschema: cairn-pilot-event/1\n"
        with pytest.raises(lifecycle.LifecycleError, match="unterminated"):
            lifecycle._parse_fenced_records(text, lifecycle._EVENT_FENCE, "x")

    @pytest.mark.parametrize("bad", ["a`b", "a|b", "a\\b", "a\x07b"])
    def test_a_value_outside_the_bounded_grammar_refuses(self, bad) -> None:
        text = f"```cairn-pilot-event\nschema: {bad}\n```\n"
        with pytest.raises(lifecycle.LifecycleError, match="bounded schema"):
            lifecycle._parse_fenced_records(text, lifecycle._EVENT_FENCE, "x")

    def test_an_overlong_value_refuses_rather_than_truncating(self) -> None:
        text = f"```cairn-pilot-event\nnote: {'x' * 201}\n```\n"
        with pytest.raises(lifecycle.LifecycleError, match="bounded schema"):
            lifecycle._parse_fenced_records(text, lifecycle._EVENT_FENCE, "x")

    def test_a_duplicate_key_in_one_block_refuses(self) -> None:
        text = ("```cairn-pilot-event\nschema: cairn-pilot-event/1\n"
                "schema: cairn-pilot-event/1\n```\n")
        with pytest.raises(lifecycle.LifecycleError, match="duplicate key"):
            lifecycle._parse_fenced_records(text, lifecycle._EVENT_FENCE, "x")

    def test_an_unknown_event_kind_refuses(self, lifecycle_ready) -> None:
        record = {"schema": EVENT_SCHEMA, "kind": "invented"}
        with pytest.raises(lifecycle_ready.LifecycleError, match="unknown event kind"):
            lifecycle_ready._validate_event(record, "x", counted_state=COUNTED_STATE)

    @pytest.mark.parametrize("schema", [
        "cairn-pilot-event/1",   # the RETIRED version, superseded by P2's bump
        "cairn-pilot-event/3",   # a future version this tool has never read
        "cairn-pilot-event",     # unversioned
        "cairn-pilot-activation/1",  # the other record's schema
    ])
    def test_an_unknown_event_schema_refuses(self, lifecycle_ready, schema) -> None:
        """**Including `/1`, and that inclusion is the point.**  P6a wrote that
        closing [CF1] *"is a `cairn-pilot-event/2` schema bump; the version field
        exists for that, and an unknown version refuses rather than being
        half-read."*  A `/1` block carries no `assurance_path`, so reading it as
        `/2` would mean reading a record that never recorded the field -- the
        half-read that provision exists to prevent."""
        record = {"schema": schema, "kind": "pause-set"}
        with pytest.raises(lifecycle_ready.LifecycleError, match="unknown or missing"):
            lifecycle_ready._validate_event(record, "x", counted_state=COUNTED_STATE)

    def test_a_plan_counted_event_refuses_while_the_vocabulary_is_silent(
            self, repo) -> None:
        """The direction that matters: no vocabulary means REFUSE, not admit."""
        block = _counted_block("stem-a", "2026-02-05", _head(repo))
        self._ledger(repo, block)
        with pytest.raises(lifecycle.LifecycleError,
                           match="cannot confirm it right now"):
            lifecycle._read_events(repo, counted_state=None)

    def test_a_plan_state_other_than_the_counted_state_refuses(
            self, repo, lifecycle_ready) -> None:
        block = _counted_block("stem-a", "2026-02-05", _head(repo),
                               state="archived")
        self._ledger(repo, block)
        with pytest.raises(lifecycle_ready.LifecycleError, match="plan_state must be"):
            lifecycle_ready._read_events(repo, counted_state=COUNTED_STATE)

    def test_a_duplicate_stem_refuses(self, repo, lifecycle_ready) -> None:
        head = _head(repo)
        self._ledger(repo,
                     _counted_block("stem-a", "2026-02-05", head),
                     _counted_block("stem-a", "2026-02-06", head))
        with pytest.raises(lifecycle_ready.LifecycleError,
                           match="already counted with the same source commit"):
            lifecycle_ready._read_events(repo, counted_state=COUNTED_STATE,
                                         assurance_values=ASSURANCE_VALUES)

    def test_a_conflicting_stem_refuses(self, repo, lifecycle_ready) -> None:
        head = _head(repo)
        _write(repo, "dev/plans/p.md",
               (repo / "dev/plans/p.md").read_text(encoding="utf-8") + "\nmore\n")
        other = _commit(repo, "a second commit carrying the same artifact",
                        "dev/plans/p.md")
        assert other != head
        self._ledger(repo,
                     _counted_block("stem-a", "2026-02-05", head),
                     _counted_block("stem-a", "2026-02-06", other))
        with pytest.raises(lifecycle_ready.LifecycleError,
                           match="already counted with a different source commit"):
            lifecycle_ready._read_events(repo, counted_state=COUNTED_STATE,
                                         assurance_values=ASSURANCE_VALUES)

    def test_a_duplicate_pause_set_refuses(self, repo) -> None:
        head = _head(repo)
        self._ledger(repo,
                     _pause_block("escaped-high", "2026-02-05", head),
                     _pause_block("escaped-high", "2026-02-06", head))
        with pytest.raises(lifecycle.LifecycleError, match="already active"):
            lifecycle._read_events(repo, counted_state=None)

    def test_clearing_a_pause_that_was_never_set_refuses(self, repo) -> None:
        self._ledger(repo, _pause_block("never-set", "2026-02-05",
                                        _head(repo), kind="pause-cleared"))
        with pytest.raises(lifecycle.LifecycleError, match="not active"):
            lifecycle._read_events(repo, counted_state=None)

    def test_an_altered_prior_event_refuses(self, repo) -> None:
        head = _head(repo)
        self._ledger(repo, _pause_block("escaped-high", "2026-02-05", head))
        path = repo / EVENTS_REL
        path.write_text(
            path.read_text(encoding="utf-8").replace("2026-02-05", "2026-02-09"),
            encoding="utf-8")
        with pytest.raises(lifecycle.LifecycleError, match="a prior event was altered"):
            lifecycle._read_events(repo, counted_state=None)

    def test_a_removed_event_refuses(self, repo) -> None:
        head = _head(repo)
        self._ledger(repo, _pause_block("escaped-high", "2026-02-05", head))
        _write(repo, EVENTS_REL, _event_text())
        with pytest.raises(lifecycle.LifecycleError, match="events were removed"):
            lifecycle._read_events(repo, counted_state=None)

    def test_prose_around_the_events_may_change(self, repo) -> None:
        """Append-only binds the events, not the human header."""
        head = _head(repo)
        self._ledger(repo, _pause_block("escaped-high", "2026-02-05", head))
        path = repo / EVENTS_REL
        path.write_text("# New title\n\nrewritten prose\n\n"
                        + _pause_block("escaped-high", "2026-02-05", head),
                        encoding="utf-8")
        events, _ = lifecycle._read_events(repo, counted_state=None)
        assert len(events) == 1

    def test_record_appends_one_event_and_binds_it_to_git(
            self, repo, lifecycle_ready, monkeypatch, capsys) -> None:
        self._ledger(repo)
        monkeypatch.chdir(repo)
        rc = lifecycle_ready.main([
            "pilot-record", "--kind", "plan-counted", "--subject", "stem-a",
            "--source-artifact", "dev/plans/p.md",
            "--source-commit", _head(repo),
            "--date", "2026-02-05", "--review-input-bytes", "1234",
            "--transitions-removed", "1", "--maintainer-prompts", "2",
        ])
        assert rc == 0, capsys.readouterr()
        text = (repo / EVENTS_REL).read_text(encoding="utf-8")
        events = lifecycle_ready._parse_fenced_records(
            text, lifecycle_ready._EVENT_FENCE, "x")
        assert len(events) == 1
        assert events[0]["subject"] == "stem-a"
        assert events[0]["plan_state"] == COUNTED_STATE
        assert events[0]["review_input_bytes"] == "1234"

    def test_record_dry_run_writes_nothing(
            self, repo, lifecycle_ready, monkeypatch, capsys) -> None:
        self._ledger(repo)
        before = (repo / EVENTS_REL).read_bytes()
        monkeypatch.chdir(repo)
        rc = lifecycle_ready.main([
            "pilot-record", "--kind", "pause-set", "--subject", "escaped-high",
            "--severity", "high", "--source-artifact", "dev/plans/p.md",
            "--source-commit", _head(repo), "--dry-run",
        ])
        assert rc == 0
        assert (repo / EVENTS_REL).read_bytes() == before
        assert "--dry-run: nothing written" in capsys.readouterr().out

    def test_record_refuses_a_source_commit_that_does_not_exist(
            self, repo, lifecycle_ready, monkeypatch, capsys) -> None:
        self._ledger(repo)
        monkeypatch.chdir(repo)
        rc = lifecycle_ready.main([
            "pilot-record", "--kind", "pause-set", "--subject", "escaped-high",
            "--severity", "high", "--source-artifact", "dev/plans/p.md",
            "--source-commit", "0" * 40,
        ])
        assert rc == 1
        # The *reason* is asserted, not only the exit code: with the
        # commit-existence check removed, the artifact lookup refuses too and a
        # bare `rc == 1` would keep passing over a removed guard.
        assert "is not a commit in this repository" in capsys.readouterr().err

    def test_record_refuses_an_artifact_absent_at_its_source_commit(
            self, repo, lifecycle_ready, monkeypatch) -> None:
        self._ledger(repo)
        monkeypatch.chdir(repo)
        rc = lifecycle_ready.main([
            "pilot-record", "--kind", "pause-set", "--subject", "escaped-high",
            "--severity", "high", "--source-artifact", "dev/plans/nope.md",
            "--source-commit", _head(repo),
        ])
        assert rc == 1

    def test_record_refuses_a_counted_plan_while_the_vocabulary_is_silent(
            self, repo, lifecycle_without_counted_state, monkeypatch,
            capsys) -> None:
        """Chunk E made the real vocabulary declare the state, so this refusal is
        now exercised against a planner that lacks it.  Every assertion is the
        pre-E node's -- including that the refusal writes NOTHING, which is the
        half that matters: a refusing writer that still appends is worse than one
        that fails loudly."""
        self._ledger(repo)
        monkeypatch.chdir(repo)
        rc = lifecycle_without_counted_state.main([
            "pilot-record", "--kind", "plan-counted", "--subject", "stem-a",
            "--source-artifact", "dev/plans/p.md",
            "--source-commit", _head(repo),
        ])
        assert rc == 1
        assert "refusing to record a counted plan" in capsys.readouterr().err
        assert lifecycle._parse_fenced_records(
            (repo / EVENTS_REL).read_text(encoding="utf-8"),
            lifecycle._EVENT_FENCE, "x") == []

    def test_record_now_accepts_a_counted_plan_against_the_landed_vocabulary(
            self, repo, monkeypatch, capsys) -> None:
        """The positive direction the refusal above cannot witness: with Chunk E
        landed, the real tool records a counted plan and stamps the state it
        resolved from the one runtime vocabulary."""
        self._ledger(repo)
        monkeypatch.chdir(repo)
        rc = lifecycle.main([
            "pilot-record", "--kind", "plan-counted", "--subject", "stem-a",
            "--source-artifact", "dev/plans/p.md",
            "--source-commit", _head(repo),
        ])
        assert rc == 0, capsys.readouterr().err
        assert f"plan_state: {COUNTED_STATE}" in capsys.readouterr().out
        records = lifecycle._parse_fenced_records(
            (repo / EVENTS_REL).read_text(encoding="utf-8"),
            lifecycle._EVENT_FENCE, "x")
        assert len(records) == 1
        assert records[0]["plan_state"] == COUNTED_STATE

    def test_a_lost_update_is_detected_and_writes_nothing(self, repo) -> None:
        """The expected-old check: a writer holding stale bytes never lands."""
        head = _head(repo)
        self._ledger(repo)
        path = repo / EVENTS_REL
        stale = path.read_text(encoding="utf-8")
        # Another writer got there first.
        path.write_text(stale + "\n" + _pause_block("first", "2026-02-05",
                                                    head), encoding="utf-8")
        winner = path.read_bytes()
        with pytest.raises(lifecycle.LifecycleError, match="another writer got there"):
            lifecycle._append_event(
                repo, path, stale,
                _pause_block("second", "2026-02-06", head))
        assert path.read_bytes() == winner

    def test_no_temp_file_survives_a_refused_append(self, repo) -> None:
        head = _head(repo)
        self._ledger(repo)
        path = repo / EVENTS_REL
        with pytest.raises(lifecycle.LifecycleError):
            lifecycle._append_event(repo, path, "stale bytes that never matched",
                                    _pause_block("x", "2026-02-06", head))
        assert sorted(p.name for p in path.parent.iterdir()) == ["pilot-events.md"]

    def test_a_symlinked_ledger_refuses_before_any_write(self, repo) -> None:
        real = repo / "elsewhere.md"
        real.write_text(_event_text(), encoding="utf-8")
        (repo / EVENTS_REL).symlink_to(real)
        with pytest.raises(lifecycle.LifecycleError, match="reached through a symlink"):
            lifecycle._evidence_path(
                repo, lifecycle._PILOT_EVENTS_REL, must_exist=True)

    def test_an_absent_measurement_directory_refuses_rather_than_creating_it(
            self, repo) -> None:
        shutil.rmtree(repo / "dev" / "measurement")
        with pytest.raises(lifecycle.LifecycleError, match="is not a directory"):
            lifecycle._evidence_path(
                repo, lifecycle._PILOT_EVENTS_REL, must_exist=False)


# ---------------------------------------------------------------------------
# 4. the derived report
# ---------------------------------------------------------------------------


class TestDerivedReport:

    def _ledger(self, repo: Path, *blocks: str) -> None:
        _write(repo, EVENTS_REL, _event_text(*blocks))
        _commit(repo, "ledger", EVENTS_REL)

    def test_absent_activation_reports_no_evidence_and_never_a_disabled_policy(
            self, repo, monkeypatch, capsys) -> None:
        monkeypatch.chdir(repo)
        rc = lifecycle.main(["pilot-report"])
        out = capsys.readouterr().out
        assert rc == 3
        assert "review policy: ACTIVE" in out
        assert "no monitoring evidence window has opened yet" in out
        assert "NOT meaning: the review policy is disabled" in out
        # The prohibited reading, in every spelling the report could produce.
        assert "policy: DISABLED" not in out
        assert "policy: INACTIVE" not in out

    def test_an_unavailable_count_is_reported_as_unavailable_not_zero(
            self, repo, lifecycle_without_counted_state, monkeypatch,
            capsys) -> None:
        """The distinction the report exists to preserve, still under test after
        Chunk E: an uncomputable count reads ``UNAVAILABLE``, never ``0``, because
        a zero from a broken rule is indistinguishable from a working rule that
        found nothing.  Exercised against a planner lacking the token, since the
        real one now has it."""
        _activate(repo)
        self._ledger(repo)
        monkeypatch.chdir(repo)
        rc = lifecycle_without_counted_state.main(["pilot-report"])
        out = capsys.readouterr().out
        assert rc == 3
        assert "counted plan stems: UNAVAILABLE / 6" in out
        assert "It is NOT zero" in out
        assert "counted plan stems: 0 / 6" not in out

    def test_the_landed_vocabulary_makes_the_count_computable_and_zero_is_real(
            self, repo, monkeypatch, capsys) -> None:
        """**What Chunk E changed in the report, asserted rather than described.**

        With the token in the vocabulary the same repository and the same empty
        ledger produce ``counted plan stems: 0 / 6``, the Chunk-E INCOMPLETE reason
        is gone, and the zero now MEANS zero -- the rule ran and found no counted
        plan.  The report still exits INCOMPLETE here, on the *other* reason (no
        activation record in this fixture's window), which is why the exit code is
        not the thing this node reads."""
        _activate(repo)
        self._ledger(repo)
        monkeypatch.chdir(repo)
        lifecycle.main(["pilot-report"])
        out = capsys.readouterr().out
        assert f"counted plan stems: 0 / 6 (distinct stems reaching " \
               f"'{COUNTED_STATE}')" in out
        assert "UNAVAILABLE" not in out
        assert "Chunk E of review-efficient-lifecycle introduces it" not in out

    def test_the_window_is_sixty_days_inclusive_of_the_activation_date(
            self, repo, lifecycle_ready) -> None:
        first, last = lifecycle_ready._window_bounds("2026-01-01")
        assert first.isoformat() == "2026-01-01"
        assert last.isoformat() == "2026-03-01"      # day 60, inclusive
        assert (last - first).days == 59

    @pytest.mark.parametrize("date,counted", [
        ("2026-01-31", False),   # the day before the activation date
        ("2026-02-01", True),    # day 1, the activation date itself
        ("2026-04-01", True),    # day 60, the last in-window day
        ("2026-04-02", False),   # day 61, past the deadline
    ])
    def test_boundary_day_arithmetic(self, repo, lifecycle_ready, date,
                                     counted) -> None:
        _activate(repo, date="2026-02-01")
        self._ledger(repo, _counted_block("stem-a", date, _head(repo)))
        lines, _ = lifecycle_ready._derive_report(
            repo, today=dt.date(2026, 4, 3))
        report = "\n".join(lines)
        if counted:
            assert "counted plan stems: 1 / 6" in report
            assert "events outside the window" not in report
        else:
            assert "counted plan stems: 0 / 6" in report
            assert "events outside the window (excluded from every count): 1" in report

    def test_distinct_stems_are_what_the_quota_counts(
            self, repo, lifecycle_ready) -> None:
        _activate(repo, date="2026-02-01")
        head = _head(repo)
        self._ledger(repo, *[
            _counted_block(f"stem-{n}", "2026-02-05", head)
            for n in range(1, 7)
        ])
        lines, incomplete = lifecycle_ready._derive_report(
            repo, today=dt.date(2026, 2, 6))
        report = "\n".join(lines)
        assert "counted plan stems: 6 / 6" in report
        assert "monitoring boundary: REACHED via six distinct plan stems" in report
        assert "retain | revise | retire" in report
        assert "`promote` is a retired token" in report
        assert incomplete == []

    def test_the_deadline_reaches_the_boundary_without_six_plans(
            self, repo, lifecycle_ready) -> None:
        _activate(repo, date="2026-02-01")
        self._ledger(repo, _counted_block("stem-a", "2026-02-05",
                                          _head(repo)))
        lines, _ = lifecycle_ready._derive_report(
            repo, today=dt.date(2026, 4, 2))
        report = "\n".join(lines)
        assert "monitoring boundary: REACHED via the 60-day deadline" in report
        assert "counted plan stems: 1 / 6" in report

    def test_an_open_window_is_not_a_reached_boundary(
            self, repo, lifecycle_ready) -> None:
        _activate(repo, date="2026-02-01")
        self._ledger(repo)
        lines, _ = lifecycle_ready._derive_report(
            repo, today=dt.date(2026, 2, 10))
        report = "\n".join(lines)
        assert "monitoring boundary: not reached" in report
        assert "window: 2026-02-01 .. 2026-04-01" in report
        assert "OPEN" in report

    def test_a_pause_is_derived_from_the_ledger_and_cleared_by_it(
            self, repo, lifecycle_ready) -> None:
        _activate(repo, date="2026-02-01")
        head = _head(repo)
        self._ledger(repo, _pause_block("escaped-high", "2026-02-05", head))
        lines, _ = lifecycle_ready._derive_report(
            repo, today=dt.date(2026, 2, 10))
        assert any("PAUSE ACTIVE: escaped-high" in line for line in lines)

        _write(repo, EVENTS_REL, _event_text(
            _pause_block("escaped-high", "2026-02-05", head),
            _pause_block("escaped-high", "2026-02-07", head,
                         kind="pause-cleared")))
        _commit(repo, "clear it", EVENTS_REL)
        lines, _ = lifecycle_ready._derive_report(
            repo, today=dt.date(2026, 2, 10))
        assert any("pauses: none active" in line for line in lines)

    def test_recorded_findings_that_meet_a_pause_condition_are_surfaced(
            self, repo, lifecycle_ready) -> None:
        _activate(repo, date="2026-02-01")
        self._ledger(repo, _counted_block("stem-a", "2026-02-05",
                                          _head(repo), high=1))
        lines, incomplete = lifecycle_ready._derive_report(
            repo, today=dt.date(2026, 2, 10))
        assert any("escaped findings high 1" in line for line in lines)
        assert any("meet a pause condition" in reason for reason in incomplete)

    def test_the_measures_the_revision_still_requires_are_all_reported(
            self, repo, lifecycle_ready) -> None:
        _activate(repo, date="2026-02-01")
        self._ledger(repo, _counted_block(
            "stem-a", "2026-02-05", _head(repo),
            bytes_=4096, removed=2, prompts=3))
        lines, _ = lifecycle_ready._derive_report(
            repo, today=dt.date(2026, 2, 10))
        report = "\n".join(lines)
        for fragment in ("review-input bytes 4096", "transitions removed 2",
                         "escaped findings high 0 / low 0",
                         "Maintainer prompts 3"):
            assert fragment in report

    def test_the_report_stores_nothing(self, repo, lifecycle_ready,
                                       monkeypatch) -> None:
        _activate(repo, date="2026-02-01")
        self._ledger(repo, _counted_block("stem-a", "2026-02-05",
                                          _head(repo)))
        before = {p: p.read_bytes() for p in (repo / "dev").rglob("*")
                  if p.is_file()}
        monkeypatch.chdir(repo)
        lifecycle_ready.main(["pilot-report"])
        after = {p: p.read_bytes() for p in (repo / "dev").rglob("*")
                 if p.is_file()}
        assert before == after
        assert _git(repo, "status", "--porcelain") == ""


# ---------------------------------------------------------------------------
# twin parity
# ---------------------------------------------------------------------------


def test_the_two_lifecycle_copies_are_byte_identical() -> None:
    """Everything above tests the template copy; this is what licenses the
    conclusion for the installed one."""
    assert MODULE_PATH.read_bytes() == TWIN_PATH.read_bytes(), (
        f"{MODULE_PATH} and {TWIN_PATH} have diverged -- the installed twin "
        f"must be byte-identical to the shipped template"
    )


# ---------------------------------------------------------------------------
# [CF1] -- the resolved assurance path on the event, and the eligible /
# ineligible split it makes derivable.
#
# Filed at `9d5cbea` in `dev/plans/review-efficient-lifecycle.md` >
# `## Carried-forward obligations` > **[CF1]**: P6a implements the five measures
# `P6-R` names, but the accepted parent's fuller list also has the report record
# *"eligible and ineligible plans"*, and P6a's derived report **cannot** split
# them -- no `plan-counted` event recorded the plan's assurance path, and a plan
# HAS none to read until P2-R's inheritance chain resolves one.  Chunk P2 closes
# it through the `cairn-pilot-event/2` bump P6a provisioned.
# ---------------------------------------------------------------------------


PROPOSAL_REL = "dev/proposals/2026-08-01-a-src.md"
INHERITED_PLAN_REL = "dev/plans/inherited.md"
FIXTURE_PROPOSAL_SHA = "1a" * 20
FIXTURE_REVIEW_SHA = "2b" * 20


def _write_inheritance_chain(root: Path, *, assurance: str) -> None:
    """A proposal declaring *assurance* plus a plan that inherits its readiness.

    Written as real files rather than mocked, because what [CF1] closes is a
    *derivation*: the CLI resolves the value from the plan through the planner,
    so a fixture that stubbed the answer would assert nothing about the chain.
    """
    _write(root, PROPOSAL_REL,
           "# src\n\n**Author**: Author A (Strategy)\n"
           "**Status**: accepted\n"
           f"**Assurance path**: {assurance}\n\n"
           "## Context\n\nx\n\n"
           "## Review -- Reviewer A (External) -- 2026-08-05\n\n"
           f"**Reviewed commit**: {FIXTURE_PROPOSAL_SHA}\n"
           "**Target**: the complete current contract\n"
           "**Prior findings**: none\n"
           f"**Assurance path**: {assurance}\n"
           "**Tier**: External\n**Findings**: none\n"
           "**Plan readiness**: READY\n\n"
           "## Decision -- Ada Lovelace (Maintainer) -- 2026-08-06\n\n"
           "**Accepted**.\n\n> Accept.\n")
    _write(root, INHERITED_PLAN_REL,
           "# inherited\n\n"
           f"**Source proposal**: [`src`](../proposals/2026-08-01-a-src.md)\n"
           "**Status**: implementing\n"
           "**Plan review**: required(Internal)\n"
           f"**Inherited proposal basis**: review={FIXTURE_REVIEW_SHA}; "
           f"proposal={FIXTURE_PROPOSAL_SHA}\n\n"
           "## Scope\n\nx\n")


class TestCF1AssurancePathOnTheEvent:
    """The /2 field: closed vocabulary, mandatory, derived, never typed."""

    def _ledger(self, repo: Path, *blocks: str) -> None:
        _write(repo, EVENTS_REL, _event_text(*blocks))
        _commit(repo, "ledger", EVENTS_REL)

    def test_the_closed_set_comes_from_the_planner_not_from_this_file(
            self, lifecycle_ready) -> None:
        """The whole reason P6a left this open: *"a second declaration in the CLI
        would fork a vocabulary the way the single-runtime-vocabulary rule forbids
        for statuses."*  So the CLI reads all three tokens through its contained
        loader, and its source carries no literal `'high-assurance'`."""
        assert lifecycle_ready._assurance_values() == ASSURANCE_VALUES
        src = MODULE_PATH.read_text(encoding="utf-8")
        assert "'high-assurance'" not in src
        assert '"high-assurance"' not in src
        assert "ASSURANCE_PATHS" in lifecycle_ready._REQUIRED_EXPORTS

    def test_the_field_is_mandatory_on_a_counted_event(
            self, repo, lifecycle_ready) -> None:
        self._ledger(repo, _counted_block("stem-a", "2026-02-05", _head(repo),
                                          assurance=None))
        with pytest.raises(lifecycle_ready.LifecycleError,
                           match="missing mandatory key|assurance_path"):
            lifecycle_ready._read_events(repo, counted_state=COUNTED_STATE,
                                         assurance_values=ASSURANCE_VALUES)

    @pytest.mark.parametrize("bad", ["medium", "standard-ish", "STANDARD",
                                     "not_inherited"])
    def test_a_value_outside_the_closed_set_refuses(
            self, repo, lifecycle_ready, bad) -> None:
        self._ledger(repo, _counted_block("stem-a", "2026-02-05", _head(repo),
                                          assurance=bad))
        with pytest.raises(lifecycle_ready.LifecycleError,
                           match="assurance_path must be one of"):
            lifecycle_ready._read_events(repo, counted_state=COUNTED_STATE,
                                         assurance_values=ASSURANCE_VALUES)

    def test_an_unconfirmable_vocabulary_refuses_rather_than_admitting(
            self, repo, lifecycle_ready) -> None:
        """The same direction the `plan_state` check takes: no vocabulary means
        REFUSE, never admit against an unchecked token."""
        self._ledger(repo, _counted_block("stem-a", "2026-02-05", _head(repo)))
        with pytest.raises(lifecycle_ready.LifecycleError,
                           match="cannot confirm it right now"):
            lifecycle_ready._read_events(repo, counted_state=COUNTED_STATE,
                                         assurance_values=None)

    def test_there_is_no_assurance_path_flag(self, lifecycle_ready) -> None:
        """DERIVED, not supplied.  A governance field a human types is an
        author's claim; the CLI being the only writer is what lets the claim be
        replaced by a derivation, exactly as it already is for `plan_state`."""
        parser = lifecycle_ready.build_parser()
        rendered = parser.format_help()
        for sub in ("pilot-record",):
            assert sub in rendered
        with pytest.raises(SystemExit):
            parser.parse_args(["pilot-record", "--kind", "plan-counted",
                               "--subject", "s", "--source-artifact", "a",
                               "--source-commit", "0" * 40,
                               "--assurance-path", "standard"])

    @pytest.mark.parametrize("assurance", ["standard", "high-assurance"])
    def test_the_writer_derives_the_value_from_the_chain(
            self, repo, lifecycle_ready, monkeypatch, capsys, assurance) -> None:
        _write_inheritance_chain(repo, assurance=assurance)
        head = _commit(repo, "the chain", PROPOSAL_REL, INHERITED_PLAN_REL)
        self._ledger(repo)
        monkeypatch.chdir(repo)
        rc = lifecycle_ready.main([
            "pilot-record", "--kind", "plan-counted", "--subject", "inherited",
            "--source-artifact", INHERITED_PLAN_REL, "--source-commit", head,
            "--date", "2026-02-05", "--review-input-bytes", "10",
            "--transitions-removed", "1", "--maintainer-prompts", "0",
        ])
        assert rc == 0, capsys.readouterr()
        events = lifecycle_ready._parse_fenced_records(
            (repo / EVENTS_REL).read_text(encoding="utf-8"),
            lifecycle_ready._EVENT_FENCE, "x")
        assert events[0]["assurance_path"] == assurance

    def test_a_plan_with_no_inheritance_chain_records_not_inherited(
            self, repo, lifecycle_ready, monkeypatch, capsys) -> None:
        """A POSITIVE resolved answer, not a default: the plan declares no chain,
        so there is no proposal declaration to inherit."""
        self._ledger(repo)
        monkeypatch.chdir(repo)
        rc = lifecycle_ready.main([
            "pilot-record", "--kind", "plan-counted", "--subject", "stem-a",
            "--source-artifact", "dev/plans/p.md", "--source-commit", _head(repo),
            "--date", "2026-02-05", "--review-input-bytes", "10",
            "--transitions-removed", "1", "--maintainer-prompts", "0",
        ])
        assert rc == 0, capsys.readouterr()
        events = lifecycle_ready._parse_fenced_records(
            (repo / EVENTS_REL).read_text(encoding="utf-8"),
            lifecycle_ready._EVENT_FENCE, "x")
        assert events[0]["assurance_path"] == "not-inherited"

    def test_a_broken_chain_refuses_the_write_and_records_nothing(
            self, repo, lifecycle_ready, monkeypatch, capsys) -> None:
        """The direction that matters: a plan that DECLARES a chain the planner
        cannot resolve refuses.  Recording `not-inherited` for it would be a quiet
        lie about which population the sample came from."""
        _write_inheritance_chain(repo, assurance="standard")
        _write(repo, PROPOSAL_REL,
               (repo / PROPOSAL_REL).read_text(encoding="utf-8").replace(
                   "**Plan readiness**: READY",
                   "**Plan readiness**: DISTINCT REVIEW REQUIRED", 1))
        head = _commit(repo, "the chain", PROPOSAL_REL, INHERITED_PLAN_REL)
        self._ledger(repo)
        before = (repo / EVENTS_REL).read_bytes()
        monkeypatch.chdir(repo)
        rc = lifecycle_ready.main([
            "pilot-record", "--kind", "plan-counted", "--subject", "inherited",
            "--source-artifact", INHERITED_PLAN_REL, "--source-commit", head,
            "--date", "2026-02-05", "--review-input-bytes", "10",
            "--transitions-removed", "1", "--maintainer-prompts", "0",
        ])
        assert rc == 1
        assert "cannot resolve the assurance path" in capsys.readouterr().err
        assert (repo / EVENTS_REL).read_bytes() == before

    def test_a_pause_event_carries_no_assurance_path(
            self, repo, lifecycle_ready, monkeypatch) -> None:
        """The field belongs to the counted-plan kind only -- the closed schema
        refuses a key outside a kind's set, so this is also the negative."""
        self._ledger(repo)
        monkeypatch.chdir(repo)
        rc = lifecycle_ready.main([
            "pilot-record", "--kind", "pause-set", "--subject", "escaped-high",
            "--severity", "high", "--source-artifact", "dev/plans/p.md",
            "--source-commit", _head(repo),
        ])
        assert rc == 0
        events = lifecycle_ready._parse_fenced_records(
            (repo / EVENTS_REL).read_text(encoding="utf-8"),
            lifecycle_ready._EVENT_FENCE, "x")
        assert "assurance_path" not in events[0]


class TestCF1TheEligibilitySplit:
    """The report line the accepted parent asked for and P6a could not derive."""

    def _activate(self, repo: Path, date: str = "2026-02-01") -> None:
        _write(repo, ACTIVATION_REL, _activation_text(_machinery(repo)))
        _commit(repo, "activate", ACTIVATION_REL, date=date)

    def _ledger(self, repo: Path, *blocks: str) -> None:
        _write(repo, EVENTS_REL, _event_text(*blocks))
        _commit(repo, "ledger", EVENTS_REL)

    def test_the_report_splits_eligible_from_ineligible(
            self, repo, lifecycle_ready, monkeypatch, capsys) -> None:
        self._activate(repo)
        head = _head(repo)
        self._ledger(
            repo,
            _counted_block("stem-a", "2026-02-05", head, assurance="standard"),
            _counted_block("stem-b", "2026-02-06", head,
                           assurance="high-assurance"),
            _counted_block("stem-c", "2026-02-07", head,
                           assurance="not-inherited"))
        monkeypatch.chdir(repo)
        lifecycle_ready.main(["pilot-report"])
        out = capsys.readouterr().out
        assert "eligible (standard): 1 [stem-a]" in out
        assert "ineligible / outside the sample: 2 [stem-b, stem-c]" in out
        assert "high-assurance: stem-b" in out
        assert "not-inherited: stem-c" in out

    def test_each_counted_row_names_its_assurance_path(
            self, repo, lifecycle_ready, monkeypatch, capsys) -> None:
        self._activate(repo)
        self._ledger(repo, _counted_block("stem-a", "2026-02-05", _head(repo),
                                          assurance="high-assurance"))
        monkeypatch.chdir(repo)
        lifecycle_ready.main(["pilot-report"])
        rows = [l for l in capsys.readouterr().out.splitlines()
                if "- stem-a" in l]
        assert len(rows) == 1
        assert rows[0].rstrip().endswith("high-assurance")

    def test_an_all_eligible_sample_prints_no_tension_note(
            self, repo, lifecycle_ready, monkeypatch, capsys) -> None:
        self._activate(repo)
        self._ledger(repo, _counted_block("stem-a", "2026-02-05", _head(repo)))
        monkeypatch.chdir(repo)
        lifecycle_ready.main(["pilot-report"])
        out = capsys.readouterr().out
        assert "eligible (standard): 1 [stem-a]" in out
        assert "NOTE: the quota above counts DISTINCT stems" not in out

    def test_the_quota_denominator_is_unchanged_and_the_tension_is_printed(
            self, repo, lifecycle_ready, monkeypatch, capsys) -> None:
        """**The restraint, asserted as behavior.**  The accepted parent says
        high-assurance work "does not fill the sample"; the 2026-08-11 revision
        lets high-assurance proposals inherit, which makes their plans part of the
        population the policy affects.  Those two texts pull opposite ways on
        WHOSE plans fill the six, and [CF1] asked only for the split -- so the
        counted-stem quota stays exactly as P6a landed it and the tension is
        PRINTED rather than resolved by an implementer."""
        self._activate(repo)
        head = _head(repo)
        self._ledger(
            repo,
            _counted_block("stem-a", "2026-02-05", head, assurance="standard"),
            _counted_block("stem-b", "2026-02-06", head,
                           assurance="high-assurance"))
        monkeypatch.chdir(repo)
        lifecycle_ready.main(["pilot-report"])
        out = capsys.readouterr().out
        assert "counted plan stems: 2 / 6" in out
        assert "NOTE: the quota above counts DISTINCT stems" in out
        assert "a Maintainer's call" in out

    def test_the_report_still_stores_nothing(
            self, repo, lifecycle_ready, monkeypatch) -> None:
        self._activate(repo)
        self._ledger(repo, _counted_block("stem-a", "2026-02-05", _head(repo)))
        monkeypatch.chdir(repo)
        lifecycle_ready.main(["pilot-report"])
        assert _git(repo, "status", "--porcelain") == ""
