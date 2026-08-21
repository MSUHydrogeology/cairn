"""Tests for the single runtime status vocabulary and its two contained loaders.

``tools/lifecycle_planner.py`` (and its byte-identical twin
``templates/skills/_lib/lifecycle_planner.py``) is the single runtime owner of
the lifecycle status vocabulary.  Consumers read it, each through its own
CONTAINED loader -- deliberately duplicated rather than shared, because a
shared helper would need somewhere importable to live, which is the
ambient-import problem the contract exists to close:

* ``scripts/transition_lint.py`` -- ``_validated_planner_path`` /
  ``_vocabulary`` / ``_purge_planner_module``, private module name
  ``_transition_lint_lifecycle_planner``, path derived from this file's own
  resolved location (``_CAIRN_ROOT``, fixed once at import).
* ``tools/_lifecycle_metrics/extract.py`` (+ its byte-identical template twin
  ``templates/modules/default-on/_lifecycle_metrics/extract.py``) -- the same
  named functions, private module name
  ``_lifecycle_metrics_lifecycle_planner``, path derived as the *sibling*
  ``lifecycle_planner.py`` from ``Path(__file__).resolve().parents[1]``,
  RE-DERIVED on every call rather than cached.
* ``tools/lifecycle.py`` (+ its byte-identical template twin
  ``templates/skills/_lib/lifecycle.py``) -- added when the lifecycle CLI became a
  vocabulary consumer: its six-plan counting rule keys on one
  plan state, so it reads ``PLAN_STATES`` through the same contained-loader
  contract (private module name ``_lifecycle_cli_lifecycle_planner``, path
  derived as the *sibling* ``lifecycle_planner.py`` from the **unresolved**
  ``Path(__file__).absolute()``).  Its loader matrix and the counting rule's
  fail-closed behavior live in ``bootstrap/tests/test_pilot_evidence.py``; what
  lives *here* is its inclusion in the source audit below, because a local
  status literal in a file this audit does not scan is a vocabulary fork Chunk
  A's guarantee would not catch.

The extract.py difference is not cosmetic and this file's loader-matrix classes
document where it matters: ``transition_lint.py`` caches ``_CAIRN_ROOT`` once
at import, so a *later* symlinked ``tools/`` is a live, naturally
constructible refusal.  ``extract.py`` recomputes ``Path(__file__).resolve()``
fresh on every call, which eagerly resolves through any symlinked ancestor --
so its ``root.is_symlink()`` / out-of-root guard cannot be tripped by
constructing real symlinks (verified empirically: a chain of real symlinks
always resolves to the true underlying directory before the guard runs).
Those two nodes exercise the guard directly with a scoped ``monkeypatch`` of
``Path.is_symlink`` / ``Path.resolve`` instead, documented at each site as
simulating the TOCTOU window the guard defends -- never by weakening the
assertion.

**Four groups of nodes:**

1. ``TestSourceAudit`` -- AC bullet "no consumer-local status literal
   survives": an AST scan of the five real consumer sources, run against the
   live repository files.  Observed red by a real, temporary, restored
   reintroduction of a local enum (see the implementing commit body for the
   exact command transcript -- pytest cannot itself mutate and restore a
   tracked file across process boundaries as part of its own run).
2. ``TestShapeBSyntheticMatrix`` -- every ``SHAPE_B_STATUSES`` member detects
   a baked-in review at an added-file commit; every terminal state does not.
   Synthetic fixtures only: the pinned corpus contains no new token, so it
   cannot witness this class (plan > "Author-accounting").
3. ``TestTransitionLintLoader`` / ``TestMetricsLoader`` -- the ten-case
   containment matrix, per consumer, against copies of the real source files
   (never hand-rewritten stand-ins) so a mutation to the real file is what the
   test actually observes.
4. ``TestMetricsLocationCases`` -- the three metrics-location cases: the
   installed pair resolves and succeeds; the byte-identical template twin, AT
   ITS SOURCE TREE LOCATION, refuses cleanly because no planner is installed
   beside it; and the two ``extract.py`` copies are
   byte-identical, so the refusal is a location/environment fact and not code
   drift between them.
"""
from __future__ import annotations

import ast
import importlib.util
import itertools
import shutil
import sys
import types
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PLANNER_SRC = REPO_ROOT / "tools" / "lifecycle_planner.py"
PLANNER_TWIN_SRC = REPO_ROOT / "templates" / "skills" / "_lib" / "lifecycle_planner.py"
TL_SRC = REPO_ROOT / "scripts" / "transition_lint.py"
TL_WHITELIST_SRC = REPO_ROOT / "scripts" / "transition_lint_whitelist.py"
METRICS_PKG_SRC = REPO_ROOT / "tools" / "_lifecycle_metrics"
METRICS_PKG_TEMPLATE_SRC = (
    REPO_ROOT / "templates" / "modules" / "default-on" / "_lifecycle_metrics"
)
#: The third consumer: the lifecycle CLI, in both copies.
LIFECYCLE_CLI_SRC = REPO_ROOT / "tools" / "lifecycle.py"
LIFECYCLE_CLI_TEMPLATE_SRC = (
    REPO_ROOT / "templates" / "skills" / "_lib" / "lifecycle.py"
)

pytestmark = pytest.mark.skipif(
    not (PLANNER_SRC.exists() and TL_SRC.exists() and METRICS_PKG_SRC.exists()
         and METRICS_PKG_TEMPLATE_SRC.exists()),
    reason="lifecycle vocabulary sources not available",
)

#: The two fixed private names each consumer's loader registers its loaded
#: planner under.  Shared process-wide ``sys.modules`` state, so every test
#: that touches either loader must start and end clean.
_PRIVATE_PLANNER_NAMES = (
    "_transition_lint_lifecycle_planner",
    "_lifecycle_metrics_lifecycle_planner",
)

_counter = itertools.count()


def _unique(prefix: str) -> str:
    return f"{prefix}_{next(_counter)}"


@pytest.fixture(autouse=True)
def _clean_private_planner_modules():
    """Purge both consumers' fixed private planner keys before AND after every
    test.  Without this, a poisoned or stale entry planted by one test (or a
    prior test's real successful load) leaks into the next test's ``existing =
    sys.modules.get(_PLANNER_MODULE_NAME)`` check through the shared process
    ``sys.modules``, since the private name is fixed and identical across every
    differently-rooted copy this file loads.
    """
    def _purge() -> None:
        for base in _PRIVATE_PLANNER_NAMES:
            for name in [n for n in sys.modules
                         if n == base or n.startswith(base + ".")]:
                sys.modules.pop(name, None)
    _purge()
    yield
    _purge()


@pytest.fixture()
def planner() -> ModuleType:
    """The real, live ``tools/lifecycle_planner.py``, loaded standalone.

    Used only as a DATA oracle (the current ``RECOGNIZED_STATES`` /
    ``SHAPE_B_STATUSES`` membership and the proposal/plan partition) to build
    fixture inputs and the audit's detection vocabulary -- never as the source
    of an expected boolean outcome about the code actually under test in a
    given node.
    """
    return _load_module_from(PLANNER_SRC, _unique("cairn_lv_planner"))


# ---------------------------------------------------------------------------
# Generic loading helpers
# ---------------------------------------------------------------------------


def _load_module_from(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _copy_tree_clean(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def _snapshot(root: Path) -> dict:
    """A cheap mutation witness: relative path -> (size, mtime_ns) for every
    file under *root*.  Used to prove an operation created or touched nothing.

    ``__pycache__`` is excluded.  CPython writes a ``.pyc`` on any import it has
    not cached, so counting those makes the witness measure *"did anything at all
    appear on disk"* rather than *"did the operation under test mutate the tree"*
    -- and the answer then depends on whether the operator happens to run with
    bytecode writing disabled.  Interpreter caching is not the property these
    tests pin; a loader manufacturing a real file (see the ``tools/__init__.py``
    case) is, and that is checked directly.
    """
    out = {}
    for p in root.rglob("*"):
        if p.is_file() and "__pycache__" not in p.parts:
            st = p.stat()
            out[str(p.relative_to(root))] = (st.st_size, st.st_mtime_ns)
    return out


# ---------------------------------------------------------------------------
# transition_lint.py tree builder + loader
# ---------------------------------------------------------------------------


def _make_tl_root(tmp_path: Path, *, with_planner: bool = True) -> Path:
    """``<root>/scripts/transition_lint.py`` (+ its whitelist),
    ``<root>/tools/lifecycle_planner.py`` (unless *with_planner* is False).
    Copies of the REAL files, never hand-rewritten stand-ins, so mutating the
    real source before a test run is what the test actually observes.
    """
    root = tmp_path / "tlroot"
    scripts_dir = root / "scripts"
    scripts_dir.mkdir(parents=True)
    shutil.copy2(TL_SRC, scripts_dir / "transition_lint.py")
    shutil.copy2(TL_WHITELIST_SRC, scripts_dir / "transition_lint_whitelist.py")
    tools_dir = root / "tools"
    tools_dir.mkdir()
    if with_planner:
        shutil.copy2(PLANNER_SRC, tools_dir / "lifecycle_planner.py")
    return root


def _load_tl(root: Path) -> ModuleType:
    return _load_module_from(
        root / "scripts" / "transition_lint.py", _unique("cairn_lv_tl"),
    )


# ---------------------------------------------------------------------------
# tools/_lifecycle_metrics/extract.py tree builder + loader
# ---------------------------------------------------------------------------


def _make_metrics_root(
    tmp_path: Path, *, with_planner: bool = True, source: Path = METRICS_PKG_SRC,
) -> Path:
    """``<root>/tools/_lifecycle_metrics/`` (a full copy -- relative imports
    inside ``extract.py`` need real package siblings), plus
    ``<root>/tools/lifecycle_planner.py`` unless *with_planner* is False.
    """
    root = tmp_path / "introot"
    tools_dir = root / "tools"
    engine_dir = tools_dir / "_lifecycle_metrics"
    _copy_tree_clean(source, engine_dir)
    if with_planner:
        tools_dir.mkdir(exist_ok=True)
        shutil.copy2(PLANNER_SRC, tools_dir / "lifecycle_planner.py")
    return root


def _load_metrics_pkg(root: Path) -> ModuleType:
    """Load ``<root>/tools/_lifecycle_metrics`` as a real package (so its
    ``.parse`` / ``.gitmeta`` / ``.config`` / ``.subsystems`` relative imports
    resolve), the same ``submodule_search_locations`` idiom the shipped
    launcher facade uses (``templates/modules/default-on/lifecycle_metrics.py``
    / ``bootstrap/tests/test_facade_loader_cleanup.py``).  Returns the package;
    ``pkg.extract`` is the submodule under test.
    """
    engine_dir = root / "tools" / "_lifecycle_metrics"
    name = _unique("cairn_lv_metrics")
    spec = importlib.util.spec_from_file_location(
        name, engine_dir / "__init__.py", submodule_search_locations=[str(engine_dir)],
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _load_metrics_extract(root: Path) -> ModuleType:
    return _load_metrics_pkg(root).extract


# ---------------------------------------------------------------------------
# Source audit -- no consumer-local status literal survives
# ---------------------------------------------------------------------------
#
# Plan Chunk A acceptance criterion: "No consumer-local status literal
# survives -- Chunk A's source audit is the enforcer, and it must be observed
# red against a deliberately reintroduced local enum."  This is the enforcer.
#
# Detection rule: a literal ``Tuple`` or ``List`` that is the DIRECT value of
# an ``Assign``/``AnnAssign`` (module scope or not -- a function-local
# reintroduction is exactly as much a violation), whose elements are ALL
# string constants, at least two of them, and every one of them a member of
# the planner's own ``RECOGNIZED_STATES``.  Restricting to a literal's direct
# assignment (rather than any nested tuple anywhere in the module) is
# deliberate and measured: an unrestricted walk over EVERY tuple/list literal
# in ``scripts/transition_lint.py`` false-positives on the pre-existing
# ``_CLAIM_TOKENS`` entry ``("review", "review")`` (a token/kind pair, not a
# vocabulary), because "review" is itself a recognized plan status.  Verified
# by direct AST inspection during the writing of this file: restricting to
# direct assignment targets eliminates that false positive while still
# catching a reintroduced ``_OPEN_STATUSES = (...)`` or ``_PLAN_STATUS_ENUM =
# (...)``, both of which the removed diffs (commits ``1c68926``, ``b0e92fd``)
# show were themselves direct module-level assignments.


def _status_literal_assignments(source: str, vocab: frozenset) -> list[tuple[int, list[str]]]:
    """``[(lineno, values), ...]`` for every direct tuple/list assignment in
    *source* whose values are >=2 string constants, all members of *vocab*.
    """
    tree = ast.parse(source)
    hits: list[tuple[int, list[str]]] = []
    for node in ast.walk(tree):
        value = None
        if isinstance(node, ast.Assign):
            value = node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            value = node.value
        if value is None or not isinstance(value, (ast.Tuple, ast.List)):
            continue
        vals: list[str] = []
        ok = True
        for elt in value.elts:
            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                vals.append(elt.value)
            else:
                ok = False
                break
        if ok and len(vals) >= 2 and set(vals) <= vocab:
            hits.append((node.lineno, vals))
    return hits


#: The five real consumer sources the audit scans: transition_lint.py, the
#: installed extract.py and its template twin, and -- since the lifecycle CLI
#: became a vocabulary consumer for the six-plan counting rule -- the
#: installed lifecycle.py and its template twin.  Never the planner itself,
#: which is the one file ALLOWED to declare the vocabulary.
#:
#: **Why lifecycle.py joined.**  The counting rule keys on one plan state.  A
#: status literal written locally there would be a vocabulary fork in a file
#: this audit did not scan -- the precise failure Chunk A exists to prevent, in
#: the one consumer whose absence from this tuple would have made the guarantee
#: quietly incomplete.  Its contained loader's own matrix lives in
#: ``bootstrap/tests/test_pilot_evidence.py`` (``TestVocabularyLoader``), which
#: is also where the counting rule's fail-closed behavior is pinned.
#: `events.py` joined once it existed (`metrics-events-not-prose` Chunk 4):
#: it is a new consumer of the runtime status vocabulary (the closed
#: grammar's `from_state`/`to_state` bound), so a local status literal
#: written there would be exactly the vocabulary fork this audit exists to
#: catch, in a file it did not yet scan.  It declares no local status
#: literal today (row 4-1's own design: the `valid_states` bound is a
#: parameter, not a loaded value), which makes THIS addition presently
#: vacuous against the literal-detection test below -- it is still
#: required, because the audit's purpose is to catch a *future* local
#: literal in a file it already scans, not only a present one.
_AUDITED_CONSUMER_SOURCES = (
    TL_SRC,
    METRICS_PKG_SRC / "extract.py",
    METRICS_PKG_TEMPLATE_SRC / "extract.py",
    LIFECYCLE_CLI_SRC,
    LIFECYCLE_CLI_TEMPLATE_SRC,
    METRICS_PKG_SRC / "events.py",
    METRICS_PKG_TEMPLATE_SRC / "events.py",
)


class TestSourceAudit:
    """AC: "No consumer-local status literal survives"."""

    def test_no_consumer_local_status_literal_survives(self, planner: ModuleType) -> None:
        vocab = frozenset(planner.RECOGNIZED_STATES)
        violations = []
        for path in _AUDITED_CONSUMER_SOURCES:
            source = path.read_text(encoding="utf-8")
            for lineno, vals in _status_literal_assignments(source, vocab):
                violations.append(f"{path}:{lineno}: {vals!r}")
        assert violations == [], (
            "consumer-local status literal(s) found -- the single vocabulary "
            "source rule (R5 replacement) is violated:\n" + "\n".join(violations)
        )

    def test_the_audit_actually_scans_all_seven_named_sources(self) -> None:
        # A guard on the guard: if a future edit narrows
        # _AUDITED_CONSUMER_SOURCES, the audit above would go quietly green
        # over fewer files without ever failing.  Pin the exact set by name.
        names = {p.name for p in _AUDITED_CONSUMER_SOURCES}
        assert names == {
            "transition_lint.py", "extract.py", "lifecycle.py", "events.py",
        }
        assert len(_AUDITED_CONSUMER_SOURCES) == 7
        assert len(set(_AUDITED_CONSUMER_SOURCES)) == 7, (
            "each installed file and its template twin must be two distinct "
            "paths, not the same file scanned twice"
        )
        assert _AUDITED_CONSUMER_SOURCES[1] != _AUDITED_CONSUMER_SOURCES[2], (
            "the installed extract.py and its template twin must be two "
            "distinct paths, not the same file scanned twice"
        )
        assert _AUDITED_CONSUMER_SOURCES[3] != _AUDITED_CONSUMER_SOURCES[4], (
            "the installed lifecycle.py and its template twin must be two "
            "distinct paths, not the same file scanned twice"
        )
        assert _AUDITED_CONSUMER_SOURCES[5] != _AUDITED_CONSUMER_SOURCES[6], (
            "the installed events.py and its template twin must be two "
            "distinct paths, not the same file scanned twice"
        )
        for path in _AUDITED_CONSUMER_SOURCES:
            assert path.is_file(), f"audited source does not exist: {path}"

    def test_detector_ignores_a_same_valued_pair_nested_in_a_larger_literal(
        self, planner: ModuleType,
    ) -> None:
        # The measured false-positive this detector was built to avoid:
        # scripts/transition_lint.py's real _CLAIM_TOKENS carries
        # ("review", "review") as a nested (token, kind) pair, and "review" is
        # itself a recognized plan status.  A naive "any tuple anywhere"
        # detector flags it; this one must not, because it is not a
        # vocabulary declaration.
        vocab = frozenset(planner.RECOGNIZED_STATES)
        source = (
            "_CLAIM_TOKENS = (\n"
            '    ("review", "review"),\n'
            '    ("response", "response"),\n'
            ")\n"
        )
        assert _status_literal_assignments(source, vocab) == []

    def test_detector_catches_a_direct_module_level_reintroduction(
        self, planner: ModuleType,
    ) -> None:
        # The positive control for the same detector: a direct assignment
        # naming >=2 recognized statuses IS flagged.  Exercises the detector
        # in isolation; the red-observed run against the real, temporarily
        # mutated file is recorded in the implementing commit body.
        vocab = frozenset(planner.RECOGNIZED_STATES)
        source = '_OPEN_STATUSES = ("proposed", "open", "awaiting-plan-review")\n'
        hits = _status_literal_assignments(source, vocab)
        assert len(hits) == 1
        assert hits[0][1] == ["proposed", "open", "awaiting-plan-review"]

    def test_detector_catches_a_function_local_reintroduction(
        self, planner: ModuleType,
    ) -> None:
        # A function-scoped re-declaration is exactly as much a violation as
        # a module-level one -- the AST walk is scope-blind by construction.
        vocab = frozenset(planner.RECOGNIZED_STATES)
        source = (
            "def _classify(s):\n"
            '    enum = ("open", "executing", "review", "archived")\n'
            "    return s in enum\n"
        )
        hits = _status_literal_assignments(source, vocab)
        assert len(hits) == 1
        assert hits[0][1] == ["open", "executing", "review", "archived"]


# ---------------------------------------------------------------------------
# Shape-(b) synthetic matrix -- every central state, real transition_lint.py
# ---------------------------------------------------------------------------
#
# Plan invariant (Author-accounting): "shape (b) fires for every current
# non-terminal opening state. Enforced by the synthetic matrix. Corpus tests
# are complementary and are NOT the oracle: the pinned corpus contains no new
# token, so it cannot witness this class."  Every fixture here is therefore
# synthetic (a throwaway git repo), never the pinned Cairn history window
# ``bootstrap/tests/test_transition_lint.py`` uses for its corpus nodes.
#
# Loads the REAL ``scripts/transition_lint.py`` (not a copy) via the same
# ``importlib`` idiom ``bootstrap/tests/test_transition_lint.py`` uses, so a
# mutation to the real file is exactly what these nodes observe.

_IDENTITY = (
    "-c", "user.name=Cairn Test",
    "-c", "user.email=test@cairn.invalid",
    "-c", "commit.gpgsign=false",
)


def _git(repo: Path, *args: str) -> str:
    import subprocess
    out = subprocess.run(
        ["git", *_IDENTITY, *args],
        cwd=str(repo), capture_output=True, check=True, text=True,
    )
    return out.stdout.strip()


def _write(repo: Path, rel: str, text: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _commit(repo: Path, subject: str) -> str:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", subject)
    return _git(repo, "rev-parse", "HEAD")


@pytest.fixture()
def tl() -> ModuleType:
    return _load_module_from(TL_SRC, _unique("cairn_lv_tl_real"))


@pytest.fixture()
def synth_repo(tmp_path: Path) -> Path:
    r = tmp_path / "synth"
    r.mkdir()
    _git(r, "init", "-q", "-b", "main")
    _write(r, "README.md", "seed\n")
    _commit(r, "seed")
    return r


#: A baked-in, dated review section that satisfies ``_shape_b``'s grammar
#: marker (``_REVIEW_MARKER_RE``) and dated-heading conjunct.
_BAKED_IN_REVIEW = (
    "## Review -- Internal -- 2026-01-01\n\n[R1] a finding baked in at open\n"
)


def _artifact_path(kind: str) -> str:
    return "dev/proposals/p.md" if kind == "proposal" else "dev/plans/p.md"


class TestShapeBSyntheticMatrix:
    """Every ``SHAPE_B_STATUSES`` member detects; every terminal state does not."""

    def test_every_shape_b_status_detects_a_baked_in_review(
        self, tl: ModuleType, synth_repo: Path, planner: ModuleType,
    ) -> None:
        statuses = list(planner.SHAPE_B_STATUSES)
        assert statuses, "SHAPE_B_STATUSES must not be empty for this matrix to mean anything"
        for status in statuses:
            kind = "proposal" if status in planner.PROPOSAL_STATES else "plan"
            path = _artifact_path(kind)
            base = _git(synth_repo, "rev-parse", "HEAD")
            _write(
                synth_repo, path,
                f"# p\n\n**Status**: {status}\n\nbody\n\n" + _BAKED_IN_REVIEW,
            )
            _commit(synth_repo, f"{kind} open (status={status})")
            _, _, findings = tl.scan(f"{base}..HEAD", synth_repo, whitelist={})
            b_findings = [f for f in findings if f.shape == "b"]
            assert len(b_findings) == 1, (
                f"status {status!r} (SHAPE_B_STATUSES member) did not "
                f"produce exactly one shape-(b) finding: {findings!r}"
            )
            # Clean up so the next status starts from an unmodified tree --
            # the loop reuses one repo rather than one per status (18 git
            # subprocess round-trips instead of ~50).
            _git(synth_repo, "rm", "-q", path)
            _commit(synth_repo, f"{kind} remove p (cleanup)")

    def test_every_terminal_status_does_not_detect(
        self, tl: ModuleType, synth_repo: Path, planner: ModuleType,
    ) -> None:
        terminal = list(planner.PROPOSAL_TERMINAL_STATES) + list(planner.PLAN_TERMINAL_STATES)
        assert terminal, "there must be at least one terminal state to matrix over"
        assert not (set(terminal) & set(planner.SHAPE_B_STATUSES)), (
            "a status cannot be both terminal and a shape-(b) candidate"
        )
        for status in terminal:
            kind = "proposal" if status in planner.PROPOSAL_STATES else "plan"
            path = _artifact_path(kind)
            base = _git(synth_repo, "rev-parse", "HEAD")
            _write(
                synth_repo, path,
                f"# p\n\n**Status**: {status}\n\nbody\n\n" + _BAKED_IN_REVIEW,
            )
            _commit(synth_repo, f"{kind} open (status={status})")
            _, _, findings = tl.scan(f"{base}..HEAD", synth_repo, whitelist={})
            assert findings == [], (
                f"terminal status {status!r} produced a finding: {findings!r}"
            )
            _git(synth_repo, "rm", "-q", path)
            _commit(synth_repo, f"{kind} remove p (cleanup)")


# ---------------------------------------------------------------------------
# The per-consumer containment matrix -- ten named cases, each consumer
# ---------------------------------------------------------------------------
#
# Both consumers expose the identical loader surface under the R5-replacement
# contract: ``_vocabulary()``, ``_validated_planner_path()``,
# ``_purge_planner_module()``, ``VocabularyUnavailable``,
# ``_PLANNER_MODULE_NAME``, ``_PLANNER_SENTINEL``, ``_REQUIRED_EXPORTS``, and
# ``_importlib_util`` (the ``importlib.util`` alias each file imports under,
# used below to inject a mid-exec failure).  Eight of the ten named cases
# share one implementation, parametrized over both consumers via
# ``ConsumerSpec``.  Two (symlinked parent directory, out-of-root resolution)
# are written per-consumer because the two loaders are only ACCIDENTALLY
# reachable the same way -- see the module docstring and each test's own
# comment for why.


class ConsumerSpec:
    """Everything the shared matrix needs to know about one loader."""

    def __init__(self, label, make_root, load, required_export):
        self.label = label
        self.make_root = make_root          # (tmp_path, with_planner=bool) -> root
        self.load = load                    # (root) -> module exposing the loader API
        #: One export this consumer actually requires, used to build a decoy
        #: planner that structurally satisfies ``_REQUIRED_EXPORTS`` for BOTH
        #: consumers regardless of which is under test.
        self.required_export = required_export

    def planner_path(self, root: Path) -> Path:
        return root / "tools" / "lifecycle_planner.py"

    def tools_dir(self, root: Path) -> Path:
        return root / "tools"


TL_SPEC = ConsumerSpec("transition_lint", _make_tl_root, _load_tl, "RECOGNIZED_STATES")
METRICS_SPEC = ConsumerSpec(
    "metrics_extract", _make_metrics_root, _load_metrics_extract, "PLAN_STATES",
)


@pytest.fixture(params=[TL_SPEC, METRICS_SPEC], ids=lambda s: s.label)
def consumer(request) -> ConsumerSpec:
    return request.param


#: A decoy planner satisfying every export EITHER consumer requires, but with
#: a value neither consumer's real vocabulary would ever produce -- used to
#: prove the decoy was never the module actually returned.  ``PROPOSAL_STATES``
#: joined once ``extract.py``'s ``_REQUIRED_EXPORTS`` grew a second export
#: (``metrics-events-not-prose`` Chunk 4, `events.py`'s `from_state`/
#: `to_state` grammar bound) -- omitting it here would make the decoy
#: structurally satisfy only the OLD required-exports contract, not the live
#: one.
_DECOY_PLANNER_SRC = (
    "RECOGNIZED_STATES = ('DECOY',)\n"
    "SHAPE_B_STATUSES = ('DECOY',)\n"
    "PLAN_STATES = ('DECOY',)\n"
    "PROPOSAL_STATES = ('DECOY',)\n"
)


class TestLoaderContainmentMatrix:
    """Cases 1, 2, 3, 6, 7, 8, 9, 10 of the ten -- shared across both consumers."""

    # -- 1. missing path -----------------------------------------------------
    def test_missing_planner_path_refuses(self, tmp_path: Path, consumer: ConsumerSpec) -> None:
        root = consumer.make_root(tmp_path, with_planner=False)
        module = consumer.load(root)
        # match= pins the SPECIFIC existence-check message, not merely the
        # exception type -- both consumers wrap "no status vocabulary" for a
        # missing planner and a DIFFERENT message ("cannot read") for an
        # unreadable one, so this distinguishes "the is_file() guard fired"
        # from "some other layer of the defence-in-depth also happened to
        # catch it and raise the same exception type."
        with pytest.raises(module.VocabularyUnavailable, match="no status vocabulary"):
            module._vocabulary()

    # -- 2. unreadable path ---------------------------------------------------
    def test_unreadable_planner_path_refuses(
        self, tmp_path: Path, consumer: ConsumerSpec,
    ) -> None:
        root = consumer.make_root(tmp_path, with_planner=True)
        module = consumer.load(root)
        planner_path = consumer.planner_path(root)
        original_mode = planner_path.stat().st_mode
        planner_path.chmod(0o000)
        try:
            with pytest.raises(module.VocabularyUnavailable, match="cannot read"):
                module._vocabulary()
        finally:
            planner_path.chmod(original_mode)

    # -- 3. symlinked leaf -----------------------------------------------------
    def test_symlinked_leaf_refuses(self, tmp_path: Path, consumer: ConsumerSpec) -> None:
        root = consumer.make_root(tmp_path, with_planner=False)
        module = consumer.load(root)
        # The real target lives INSIDE tools_dir under a different filename --
        # deliberately, so path.resolve().parent still equals tools_dir.resolve()
        # and the out-of-root check (case 5) cannot act as a silent backstop for
        # a disabled leaf-symlink check.  Verified while writing this file: a
        # target placed OUTSIDE tools_dir makes this node pass even with the
        # leaf-symlink check disabled, because the out-of-root check catches it
        # instead -- which proves nothing about the leaf-symlink check
        # specifically.
        real_planner = consumer.tools_dir(root) / "lifecycle_planner_real.py"
        shutil.copy2(PLANNER_SRC, real_planner)
        consumer.planner_path(root).symlink_to(real_planner)
        # match= the literal phrase, not the bare word "symlink" -- pytest's own
        # tmp_path directory name is derived from THIS test's function name
        # ("test_symlinked_leaf_refuses"), which itself contains the substring
        # "symlink".  Since the refusal message always embeds the full path, a
        # bare match="symlink" spuriously matches on the DIRECTORY NAME alone,
        # regardless of which check actually fired -- discovered empirically
        # while building this matrix (see the implementing commit body).
        with pytest.raises(module.VocabularyUnavailable, match="is a symlink"):
            module._vocabulary()

    # -- 6. poisoned sys.modules entry under the private name -----------------
    def test_poisoned_sys_modules_entry_is_never_trusted_merely_for_being_present(
        self, tmp_path: Path, consumer: ConsumerSpec,
    ) -> None:
        root = consumer.make_root(tmp_path, with_planner=True)
        module = consumer.load(root)
        real_path = consumer.planner_path(root).resolve()

        poisons = [
            # (a) a bare stub -- no sentinel, no exports at all.
            lambda: types.ModuleType(module._PLANNER_MODULE_NAME),
            # (b) sentinel set and required exports present, but __file__
            #     points somewhere else -- identity must be checked on the
            #     FILE, not merely on "has the sentinel".
            lambda: _fake_planner_module(
                module, sentinel=True, file=str(tmp_path / "somewhere_else.py"),
            ),
            # (c) sentinel set and __file__ correct, but missing a required
            #     export -- caching must check EVERY required export, not
            #     just the sentinel.
            lambda: _fake_planner_module(
                module, sentinel=True, file=str(real_path), omit_export=True,
            ),
        ]
        for build_poison in poisons:
            module._purge_planner_module()
            module._planner_cache = None
            sys.modules[module._PLANNER_MODULE_NAME] = build_poison()
            vocab = module._vocabulary()
            assert vocab is not sys.modules.get("__never_this__"), "sanity"
            assert getattr(vocab, module._PLANNER_SENTINEL, False) is True
            assert getattr(vocab, "__file__", None) == str(real_path)
            assert all(hasattr(vocab, n) for n in module._REQUIRED_EXPORTS)
            # The genuinely poisoned entry must have been replaced, not kept.
            assert sys.modules[module._PLANNER_MODULE_NAME] is vocab

    # -- 7. partial-child cleanup then successful retry ------------------------
    def test_partial_child_cleanup_then_successful_retry(
        self, tmp_path: Path, consumer: ConsumerSpec,
    ) -> None:
        root = consumer.make_root(tmp_path, with_planner=True)
        module = consumer.load(root)
        real_spec_from = module._importlib_util.spec_from_file_location
        private = module._PLANNER_MODULE_NAME

        def boom_spec(name, location, **kw):
            spec = real_spec_from(name, location, **kw)
            def boom(mod):
                # Simulate a child submodule registered mid-exec, then a
                # failure -- exactly what a planner whose own top-level code
                # imports a helper submodule under the private name would do.
                child = private + ".shared"
                sys.modules[child] = types.ModuleType(child)
                raise RuntimeError("boom-mid-exec")
            spec.loader.exec_module = boom
            return spec

        module._importlib_util.spec_from_file_location = boom_spec
        try:
            with pytest.raises(RuntimeError, match="boom-mid-exec"):
                module._vocabulary()
            assert private not in sys.modules, "failed load left the parent poisoned"
            assert not any(n.startswith(private + ".") for n in sys.modules), (
                "failed load left a registered child behind (mixed-graph risk)"
            )
        finally:
            module._importlib_util.spec_from_file_location = real_spec_from
        # Retry from clean: a fresh, fully successful load.
        module._planner_cache = None
        vocab = module._vocabulary()
        assert getattr(vocab, module._PLANNER_SENTINEL, False) is True
        assert not any(n.startswith(private + ".") for n in sys.modules)

    # -- 8. no ambient sys.path trust (decoy) -----------------------------------
    def test_no_ambient_sys_path_trust_even_with_a_decoy_present(
        self, tmp_path: Path, consumer: ConsumerSpec, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        root = consumer.make_root(tmp_path, with_planner=True)
        module = consumer.load(root)
        decoy_dir = tmp_path / "decoy_on_sys_path"
        decoy_dir.mkdir()
        (decoy_dir / "lifecycle_planner.py").write_text(_DECOY_PLANNER_SRC, encoding="utf-8")
        monkeypatch.syspath_prepend(str(decoy_dir))
        try:
            vocab = module._vocabulary()
            real_path = consumer.planner_path(root).resolve()
            assert getattr(vocab, "__file__", None) == str(real_path), (
                "the loaded vocabulary's __file__ is not the derived sibling "
                "path -- an ambient sys.path decoy may have been consulted"
            )
            assert getattr(vocab, consumer.required_export) != ("DECOY",), (
                "the decoy's value leaked into the returned vocabulary"
            )
        finally:
            sys.modules.pop("lifecycle_planner", None)

    # -- 9. no tools/__init__.py shortcut ---------------------------------------
    def test_no_tools_init_shortcut_created_or_required(
        self, tmp_path: Path, consumer: ConsumerSpec,
    ) -> None:
        root = consumer.make_root(tmp_path, with_planner=True)
        init_path = consumer.tools_dir(root) / "__init__.py"
        assert not init_path.exists(), "fixture must not pre-create tools/__init__.py"
        module = consumer.load(root)
        module._vocabulary()  # must succeed WITHOUT tools/__init__.py existing
        assert not init_path.exists(), (
            "the loader created tools/__init__.py as a side effect -- the "
            "contract forbids manufacturing a package to ease loading"
        )

    # -- 10. absence of import side effects --------------------------------------
    def test_loading_the_planner_causes_no_cli_action_or_repo_mutation(
        self, tmp_path: Path, consumer: ConsumerSpec, capsys: pytest.CaptureFixture,
    ) -> None:
        root = consumer.make_root(tmp_path, with_planner=True)
        module = consumer.load(root)
        before = _snapshot(root)
        capsys.readouterr()  # discard anything from module import/setup
        vocab = module._vocabulary()
        captured = capsys.readouterr()
        assert captured.out == "" and captured.err == "", (
            f"loading the planner printed output -- a CLI action ran: "
            f"out={captured.out!r} err={captured.err!r}"
        )
        after = _snapshot(root)
        assert after == before, "loading the planner mutated the working tree"
        assert callable(getattr(vocab, "main", None)), (
            "sanity: the planner's main() exists but must never have executed"
        )


def _fake_planner_module(
    module: ModuleType, *, sentinel: bool, file: str, omit_export: bool = False,
    omit: str | None = None,
) -> ModuleType:
    """``omit_export=True`` omits ``_REQUIRED_EXPORTS[0]`` (the original,
    single-omission case every consumer shares); ``omit=<name>`` omits a
    SPECIFIC named export instead, for a consumer whose required-exports
    tuple has grown past one entry and needs each half independently
    exercised (see ``test_missing_proposal_states_export_is_purged_not_cached``
    below)."""
    fake = types.ModuleType(module._PLANNER_MODULE_NAME)
    fake.__file__ = file
    if sentinel:
        setattr(fake, module._PLANNER_SENTINEL, True)
    target_omit = omit if omit is not None else (
        module._REQUIRED_EXPORTS[0] if omit_export else None
    )
    for name in module._REQUIRED_EXPORTS:
        if name == target_omit:
            continue
        setattr(fake, name, ("POISON",))
    return fake


# ---------------------------------------------------------------------------
# Cases 4 and 5 -- symlinked parent directory, out-of-root resolution
# ---------------------------------------------------------------------------
#
# NOT shared via ConsumerSpec.  ``transition_lint.py`` computes ``_CAIRN_ROOT
# = Path(__file__).resolve().parent.parent`` ONCE, at import time; its
# ``tools_dir = _CAIRN_ROOT / "tools"`` is then a plain string join checked
# fresh on every call, so a `tools/` REPLACED with a symlink AFTER import is a
# real, live, naturally constructible refusal (case 4, below, is a genuine
# filesystem construction -- no monkeypatch).
#
# ``tools/_lifecycle_metrics/extract.py`` instead recomputes
# ``here = Path(__file__).resolve()`` fresh on EVERY call, and ``.resolve()``
# unconditionally follows every symlink in the whole chain before the guard
# ever runs.  Empirically verified while building this file: constructing
# ``tools/`` as a real symlink and importing ``extract.py`` through it still
# yields ``root.is_symlink() == False``, because ``root`` (``here.parents[1]``)
# is already the fully-resolved real target directory by the time the check
# executes -- the symlink has already been dereferenced.  The same holds for
# the out-of-root check on BOTH consumers: once the two preceding symlink
# checks have passed (leaf not a symlink, parent not a symlink), there is no
# real-filesystem construction left that makes ``path.resolve().parent``
# diverge from ``root.resolve()`` without an active TOCTOU race. Both guards
# below are therefore exercised via a scoped ``monkeypatch`` of the exact
# ``Path`` method the guard calls, restricted by path-equality to the one
# object under test -- proven, by the accompanying mutation run (see the
# implementing commit body), to redden when the guard clause is removed. This
# is not a workaround for an untestable property; it is the direct, minimal
# simulation of the TOCTOU window each guard exists to close, stated exactly
# where a real symlink cannot reach it.


class TestSymlinkedParentDirectory:
    """Case 4."""

    def test_transition_lint_symlinked_tools_dir_refuses(self, tmp_path: Path) -> None:
        # Real filesystem construction: _CAIRN_ROOT is fixed at import, so
        # tools/ can be REPLACED with a symlink and the check still fires
        # live, on the actual filesystem, no monkeypatch involved.
        root = TL_SPEC.make_root(tmp_path, with_planner=False)
        real_tools = tmp_path / "real_tools_elsewhere"
        real_tools.mkdir()
        shutil.copy2(PLANNER_SRC, real_tools / "lifecycle_planner.py")
        shutil.rmtree(root / "tools")
        (root / "tools").symlink_to(real_tools, target_is_directory=True)
        module = TL_SPEC.load(root)
        # match= the literal phrase, not the bare word "symlink" -- see
        # TestLoaderContainmentMatrix.test_symlinked_leaf_refuses's comment for
        # why a bare substring collides with this test's own tmp_path name.
        with pytest.raises(module.VocabularyUnavailable, match="is a symlink"):
            module._vocabulary()

    def test_metrics_symlinked_tools_dir_refuses_via_toctou_simulation(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        # See the class-group comment: real symlink construction cannot reach
        # this guard for extract.py, because Path(__file__).resolve() is
        # recomputed fresh every call and always de-symlinks the chain first
        # (verified empirically).  Simulated directly instead.
        root = METRICS_SPEC.make_root(tmp_path, with_planner=True)
        module = METRICS_SPEC.load(root)
        engine_root = METRICS_SPEC.tools_dir(root).resolve()
        real_is_symlink = Path.is_symlink

        def fake_is_symlink(self):
            if self == engine_root:
                return True
            return real_is_symlink(self)

        monkeypatch.setattr(Path, "is_symlink", fake_is_symlink)
        with pytest.raises(module.VocabularyUnavailable, match="is a symlink"):
            module._vocabulary()


class TestOutOfRootResolution:
    """Case 5.  See ``TestSymlinkedParentDirectory``'s class-group comment for
    why this is a scoped ``Path.resolve`` monkeypatch on both consumers rather
    than a real-filesystem construction.
    """

    def _run(self, spec: ConsumerSpec, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        root = spec.make_root(tmp_path, with_planner=True)
        module = spec.load(root)
        target = spec.planner_path(root).resolve()
        elsewhere = tmp_path / "elsewhere_entirely" / "lifecycle_planner.py"
        real_resolve = Path.resolve

        def fake_resolve(self, *a, **kw):
            result = real_resolve(self, *a, **kw)
            if result == target:
                return elsewhere
            return result

        monkeypatch.setattr(Path, "resolve", fake_resolve)
        # match= the literal phrase for the same reason the symlink cases pin a
        # full phrase rather than a bare word -- avoid any chance collision
        # with a generated tmp_path segment.
        with pytest.raises(module.VocabularyUnavailable, match="resolves outside the expected"):
            module._vocabulary()

    def test_transition_lint_out_of_root_resolution_refuses(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self._run(TL_SPEC, tmp_path, monkeypatch)

    def test_metrics_out_of_root_resolution_refuses(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self._run(METRICS_SPEC, tmp_path, monkeypatch)


# ---------------------------------------------------------------------------
# The three metrics-location cases
# ---------------------------------------------------------------------------
#
# The three metrics-location cases.  Reading
# adopted here, stated explicitly per the task brief:
#
#   1. the INSTALLED location -- tools/_lifecycle_metrics/extract.py beside
#      tools/lifecycle_planner.py -- resolves and succeeds (this repository
#      self-hosts: dev/.cairn/cairn-lock.yml's install manifest names
#      modules/default-on/_lifecycle_metrics/*.py -> tools/_lifecycle_metrics/
#      and skills/_lib/lifecycle_planner.py -> tools/lifecycle_planner.py, so
#      Cairn's OWN tools/ tree already IS an installed adopter tree);
#   2. the byte-identical TEMPLATE TWIN, at its own SOURCE TREE location
#      (templates/modules/default-on/_lifecycle_metrics/extract.py), refuses
#      cleanly -- said explicitly and pinned here, because no
#      templates/modules/default-on/lifecycle_planner.py exists to be its
#      sibling;
#   3. the two extract.py files are BYTE-IDENTICAL -- proving case 2's
#      refusal is a location/environment fact, not a code difference between
#      the twins.  Without this, cases 1 and 2 alone would leave open whether
#      the template copy merely has a bug that happens to look like the
#      documented refusal.
#
# This is read as a genuine third case rather than restating case 2, because
# it is the one that closes the gap between "this copy behaves differently
# here" and "this copy IS the same code, running somewhere the contract says
# it must refuse."


class TestMetricsLocationCases:
    def test_installed_location_resolves_and_succeeds(self) -> None:
        # Case 1.  The REAL repository tree, not a copy: this repo's own
        # tools/_lifecycle_metrics/ + tools/lifecycle_planner.py IS the
        # installed pair (dev/.cairn/cairn-lock.yml install-manifest rows
        # confirm both dst locations), so loading it directly at its real
        # path is the faithful installed-location case.
        pkg = _load_metrics_pkg(REPO_ROOT)
        vocab = pkg.extract._vocabulary()
        assert Path(vocab.__file__).resolve() == (REPO_ROOT / "tools" / "lifecycle_planner.py").resolve()
        assert vocab.PLAN_STATES  # a real, non-empty vocabulary was loaded

    def test_template_source_location_refuses_cleanly(self) -> None:
        # Case 2.  templates/modules/default-on/_lifecycle_metrics/extract.py
        # at ITS OWN location: the sibling it derives is
        # templates/modules/default-on/lifecycle_planner.py, which does not
        # exist.  Fail-closed refusal is the documented CORRECT behaviour
        # -- not a defect -- pinned here so a later "fix" (a sys.path
        # fallback) would be a test failure, not a quiet improvement.
        assert not (METRICS_PKG_TEMPLATE_SRC.parent / "lifecycle_planner.py").exists(), (
            "fixture assumption broken: a planner now exists beside the "
            "template's source location, which would make this refusal "
            "assertion meaningless -- re-derive this case"
        )
        name = _unique("cairn_lv_metrics_template_loc")
        spec = importlib.util.spec_from_file_location(
            name, METRICS_PKG_TEMPLATE_SRC / "__init__.py",
            submodule_search_locations=[str(METRICS_PKG_TEMPLATE_SRC)],
        )
        assert spec is not None and spec.loader is not None
        pkg = importlib.util.module_from_spec(spec)
        sys.modules[name] = pkg
        spec.loader.exec_module(pkg)
        # match= pins the specific "no planner beside this module" message
        # (not merely the exception type), so a mutation that bypasses THIS
        # guard but still fails some other way -- e.g. an uncaught exec
        # failure the outer catch-all also wraps as VocabularyUnavailable --
        # is distinguishable from the real, intended refusal reason.
        with pytest.raises(
            pkg.extract.VocabularyUnavailable, match="no status vocabulary beside this module",
        ):
            pkg.extract._vocabulary()

    def test_the_two_extract_copies_are_byte_identical(self) -> None:
        # Case 3.  Twin parity, specific to the metrics consumer: proves
        # case 2's refusal is purely about WHERE the file sits, not a
        # divergent implementation between the installed copy and the
        # template it was installed from.
        installed = (METRICS_PKG_SRC / "extract.py").read_bytes()
        template = (METRICS_PKG_TEMPLATE_SRC / "extract.py").read_bytes()
        assert installed == template, (
            "tools/_lifecycle_metrics/extract.py and "
            "templates/modules/default-on/_lifecycle_metrics/extract.py have "
            "diverged -- the template-location refusal above would no longer "
            "be evidence about the shipped consumer's behaviour"
        )

    def test_missing_proposal_states_export_is_purged_not_cached(
        self, tmp_path: Path,
    ) -> None:
        """`metrics-events-not-prose` Chunk 4 widened `extract.py`'s
        `_REQUIRED_EXPORTS` from a 2-tuple to a 3-tuple
        (`PLAN_STATES`, `HISTORICAL_PLAN_STATES`, `PROPOSAL_STATES`) --
        the shared `TestLoaderContainmentMatrix` case 6 poison already
        exercises omitting `_REQUIRED_EXPORTS[0]` (`PLAN_STATES`) across
        both consumers, but that leaves the newly-required THIRD export
        unexercised: a poisoned cache entry present for every export
        except `PROPOSAL_STATES` must still be purged and reloaded, not
        mistaken for complete because the sentinel and the two
        already-required exports both happened to be present."""
        root = METRICS_SPEC.make_root(tmp_path, with_planner=True)
        module = METRICS_SPEC.load(root)
        real_path = METRICS_SPEC.planner_path(root).resolve()

        module._purge_planner_module()
        module._planner_cache = None
        sys.modules[module._PLANNER_MODULE_NAME] = _fake_planner_module(
            module, sentinel=True, file=str(real_path), omit="PROPOSAL_STATES",
        )
        vocab = module._vocabulary()
        assert all(hasattr(vocab, n) for n in module._REQUIRED_EXPORTS), (
            "the reloaded vocabulary is missing a required export"
        )
        assert vocab.PROPOSAL_STATES != ("POISON",), (
            "the poisoned cache entry was trusted instead of purged and "
            "reloaded"
        )
        assert sys.modules[module._PLANNER_MODULE_NAME] is vocab
