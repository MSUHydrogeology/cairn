# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .config import load_config, proposals_dir, plans_dir, MetricsConfig, _REPO_ROOT
from .parse import (
    _header_field,
    _strip_role,
    _agent_of,
    _parse_date,
    _split_h2_sections,
    _stage_section_dates,
)
import importlib.util as _importlib_util
import sys as _sys

from .gitmeta import _resolve_stage_commits, _hour_delta, _day_delta, _stage_reliability
from .subsystems import (
    _load_all_annotations,
    _annotation_count_for_stem,
    _extract_response_models,
)
from . import events


# Per-proposal schema.  The v1 core lifecycle columns plus the folded-up
# measurement subsystem columns (annotation count, review-yield buckets,
# per-Response model captures).  ``human_review`` is deliberately ABSENT:
# a human/AI split needs a per-team roster a vendor-neutral tool cannot
# assume (see ``_agent_of``), so the tool surfaces the generic
# ``cross_agent_type_review`` signal instead.
PROPOSAL_COLUMNS = [
    'stem',
    'author',
    'date_opened',
    'status',
    'decision_date',
    'days_to_decision',
    'review_rounds',
    'reviewer_agents',
    'cross_agent_type_review',
    'external_tier_review',
    'revised',
    # Per-stage timestamps + deltas.  Header dates give day-level
    # precision; git commit timestamps add sub-day hour-level precision
    # when available (degrading to empty + Best-effort without git).
    'reviewed_date',
    'revised_date',
    'days_open_to_reviewed',
    'days_reviewed_to_revised',
    'days_revised_to_decision',
    'hours_open_to_reviewed',
    'hours_reviewed_to_revised',
    'hours_revised_to_decision',
    'stage_timestamp_reliability',
    # Annotation reader: number of ``<annotations_dir>/*.yml`` files
    # naming this proposal stem under ``affected_artifacts``.
    'proposal_annotation_count',
    # Per-Response ``**Model**:`` field captures, pipe-joined and
    # positionally aligned with ``reviewer_agents`` (empty token when a
    # Response carries no Model line).  The model-tier aggregators read
    # this column.
    'response_models',
]

# Per-plan schema.
PLAN_COLUMNS = [
    'stem',
    'status',
    'plan_review_rounds',
    'code_review_rounds',
    'paired_proposal',
    'paired_proposal_reliability',
]

# The enum tokens a plan status normalizes to.
#  The plan-status enum used to be declared here as a local tuple, and it
#  omitted ``awaiting-plan-review``.  It is now the planner's ``PLAN_STATES``,
#  read through the contained loader below (`lifecycle-status-vocabulary`, as
#  replaced).  See ``_plan_status_enum()``.


# --------------------------------------------------------------- corpus walk


def _iter_corpus_files(root: Path) -> List[Path]:
    """All ``.md`` files under ``root`` (live + ``archive/``,
    recursive), excluding ``_template.md``.  Returned unsorted; the
    row builders sort deterministically."""
    if not root.exists():
        return []
    return [p for p in root.rglob('*.md') if p.name != '_template.md']


def iter_proposal_files(root: Path) -> List[Path]:
    """Every non-template proposal file -- ``dev/proposals/*.md`` plus
    ``dev/proposals/archive/**/*.md``."""
    return _iter_corpus_files(proposals_dir(root))


def iter_plan_files(root: Path) -> List[Path]:
    """Every non-template plan file -- ``dev/plans/*.md`` plus
    ``dev/plans/archive/**/*.md``."""
    return _iter_corpus_files(plans_dir(root))


# ----------------------------------------------------------- proposal rows


def _vocabulary_states(attr_name: str) -> Optional[Tuple[str, ...]]:
    """``getattr(_vocabulary(), attr_name)``, or ``None`` when the
    vocabulary cannot be loaded at all (the template-source-location
    refusal, or any other ``VocabularyUnavailable`` cause) -- treated
    identically to unavailable git by every caller below: reconciliation
    cannot be attempted, so every act falls back to the pre-cutoff
    disposition rather than raising."""
    try:
        return tuple(getattr(_vocabulary(), attr_name))
    except VocabularyUnavailable:
        return None


def _reconcile_artifact(
    path: Path, repo_root: Optional[Path], template_path: Path,
    valid_states: Optional[Sequence[str]],
) -> 'Optional[events.Reconciliation]':
    """Best-effort reconciliation for one artifact.  Returns ``None`` --
    which every caller treats as "cannot prove past cutoff, fall back to
    pre-cutoff behavior" (Chunk 5's Activation section: unavailable git
    gets the same disposition a tree with no marker at all already
    gets) -- when there is no ``repo_root``, the vocabulary could not be
    resolved, ``path`` does not live under ``repo_root`` at all, or git
    itself is unavailable.  A genuine structural defect (a mutated
    block, an orphaned block, a merge-smuggled block, a malformed
    grammar) is NOT swallowed here -- it propagates, because those are
    unconditional refusals independent of the cutoff."""
    if repo_root is None or valid_states is None:
        return None
    try:
        root_res = repo_root.resolve()
        relpath = str(path.resolve().relative_to(root_res))
        template_relpath = str(template_path.resolve().relative_to(root_res))
    except ValueError:
        return None
    try:
        reconciliation = events.reconcile(
            repo_root, relpath, valid_states=valid_states,
            template_relpath=template_relpath,
        )
    except events.GitUnavailable:
        return None
    # A measurement never refuses.  An act with no matching event block means
    # this artifact's structured series cannot be computed -- so the fields
    # derived from it go empty, exactly as they do when git is unavailable
    # above, and every other row in the corpus is still produced.
    #
    # This deliberately reverses an earlier design in which the missing block
    # raised and took the whole run's exit code with it.  An instrument that can
    # halt what it observes has stopped being an instrument: the first thing it
    # caught was an ordinary status flip, and the failure was unrecoverable
    # without rewriting published history, because a block is only ever paired
    # with an act in its own introducing commit.  Empty fields are honest about
    # what is unknown; a refused corpus is not more honest, only less usable.
    if reconciliation.incomplete:
        return None
    return reconciliation


def _reconciled_kind(
    reconciliation: 'Optional[events.Reconciliation]', kind: str,
) -> 'Tuple[bool, List[events.ReconciledEvent]]':
    """``(is_empty, matched_post_cutoff_events)`` for one event kind.

    Empty whenever reconciliation could not be attempted at all, OR a
    pre-cutoff (or unprovable-cutoff) act of this kind exists anywhere in
    the artifact's history -- reporting a count that silently omits the
    pre-cutoff act would be exactly the "travelling wrong number" shape
    the Decision retired the prose-parsing path to stop
    (``code_review_rounds`` reading 0 on 28/38 artifacts is the named
    precedent).  Not empty -- 0, or the real count -- only when
    reconciliation succeeded and there is genuinely nothing of this kind
    anywhere in the artifact's history.  This mixed-history disposition
    is this module's own resolution of a genuine ambiguity in the
    accepted text (Chunk 6's own paragraph describes an artifact
    carrying "an empty value... and a populated... value" without
    saying how one row reconciles the two for a single scalar column);
    recorded here and in the implementing commit body rather than
    silently picked.

    A never-activated artifact (``reconciliation.activation is None``)
    is checked directly, ahead of ``pre_cutoff_acts`` -- ``reconcile()``
    takes a fast path for that case and does not populate
    ``pre_cutoff_acts`` at all (every act is pre-cutoff by definition
    there, so walking history to enumerate them one by one buys nothing
    a corpus-wide call would want to pay for)."""
    if reconciliation is None or reconciliation.activation is None:
        return True, []
    if any(act.kind == kind for act in reconciliation.pre_cutoff_acts):
        return True, []
    matched = [e for e in reconciliation.post_cutoff_events if e.kind == kind]
    return False, matched


def extract_proposal_row(
    path: Path,
    *,
    include_git_timestamps: bool = True,
    repo_root: Optional[Path] = None,
    annotations: Optional[Sequence[Dict[str, object]]] = None,
) -> Dict[str, object]:
    """Parse one proposal file into a metrics row.

    Pure function of the file contents for the header-only columns.
    When ``include_git_timestamps`` is True (default), an additional
    read-only ``git log`` augments the per-stage data with commit
    timestamps for sub-day precision; disable it for pure-logic tests
    via ``include_git_timestamps=False``.

    ``annotations``: optional pre-loaded annotation list (via
    ``_load_all_annotations()``).  When ``None``, annotation lookup is
    skipped and ``proposal_annotation_count=0``.  Callers that emit many
    rows load the annotations once and pass them through."""
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    sections = _split_h2_sections(lines)

    author = _strip_role(_header_field(text, 'Author'))
    date_opened = _parse_date(_header_field(text, 'Date opened'))
    status = _header_field(text, 'Status').split()[:1]
    status_token = status[0].strip(' .,;:').lower() if status else ''

    stage_dates = _stage_section_dates(sections)
    decision_date: Optional[datetime.date] = stage_dates['decision']
    days_to_decision: object = ''
    if date_opened is not None and decision_date is not None:
        days_to_decision = (decision_date - date_opened).days

    # Part 3 (metrics-events-not-prose): review-pass / response fields are
    # sourced from reconciled cairn-event-v1 blocks post-activation-cutoff,
    # not from prose/heading parsing -- the retirement Round 7 makes.
    # Reconciliation is attempted only when a repo root is available and
    # git-timestamp augmentation is requested (the same gate the existing
    # git-derived fields below already use); when it cannot be attempted
    # at all, every act is treated as pre-cutoff (Chunk 5's Activation
    # section), which for a review-pass/response-kind field means empty,
    # never the retired heading-count value.
    reconciliation: 'Optional[events.Reconciliation]' = None
    if include_git_timestamps:
        root_for_events = repo_root if repo_root is not None else _REPO_ROOT
        proposal_states = _vocabulary_states('PROPOSAL_STATES')
        reconciliation = _reconcile_artifact(
            path, root_for_events, proposals_dir(root_for_events) / '_template.md',
            proposal_states,
        )

    review_empty, review_events = _reconciled_kind(reconciliation, events.KIND_REVIEW_PASS)
    if review_empty:
        reviewer_agents: List[str] = []
        external_tier_review: object = ''
        cross_agent_type_review: object = ''
    else:
        # Reviewer-identity normalization, pinned: the grammar's `reviewer`
        # key stores the name as written in the section heading, but
        # `reviewer_agents`/`cross_agent_type_review` are existing v1
        # columns whose semantics depend on the SAME normalized agent
        # token `_agent_of(h)` already applies to the heading itself.
        # Applying it here too keeps the `a != author` comparison
        # comparing like values and the emitted column shape unchanged
        # for post-cutoff rows: the block becomes the source, the value
        # shape does not.
        reviewer_agents = [_agent_of(e.block.reviewer) for e in review_events]
        block_tiers = [e.block.tier.lower() for e in review_events]
        if 'external' in block_tiers:
            external_tier_review = True
        elif 'internal' in block_tiers:
            external_tier_review = False
        else:
            external_tier_review = 'unknown'
        # Generic, vendor-neutral signal: a review round whose reviewer
        # identity differs from the author exists.  (A sharper human/AI
        # split would need a per-team roster, which a shipped tool cannot
        # assume -- so no ``human_review`` column here.)
        cross_agent_type_review = any(
            a and author and a != author for a in reviewer_agents
        )

    # `revised` stays prose-derived, pre- AND post-cutoff -- named as a
    # deliberate scope decision, not an oversight: a `transition` block
    # carries only from_state/to_state, with no field indicating "this
    # transition included an editorial revision", so there is no
    # grammar-supported way to source it from a block without inventing
    # a field Round 7 does not specify.
    revised = any(h.startswith('## Revised') for h, _ in sections)

    reviewed_date = stage_dates['reviewed']
    revised_date = stage_dates['revised']
    days_open_to_reviewed = _day_delta(date_opened, reviewed_date)
    days_reviewed_to_revised = _day_delta(reviewed_date, revised_date)
    days_revised_to_decision = _day_delta(revised_date, decision_date)

    if include_git_timestamps:
        stage_commits = _resolve_stage_commits(path, repo_root=repo_root)
    else:
        stage_commits = {
            'open': None, 'reviewed': None, 'revised': None, 'decision': None,
        }
    open_ts = stage_commits['open'][1] if stage_commits['open'] else None
    reviewed_ts = (
        stage_commits['reviewed'][1] if stage_commits['reviewed'] else None)
    revised_ts = (
        stage_commits['revised'][1] if stage_commits['revised'] else None)
    decision_ts = (
        stage_commits['decision'][1] if stage_commits['decision'] else None)
    hours_open_to_reviewed = _hour_delta(open_ts, reviewed_ts)
    hours_reviewed_to_revised = _hour_delta(reviewed_ts, revised_ts)
    hours_revised_to_decision = _hour_delta(revised_ts, decision_ts)
    stage_present = {s for s, d in stage_dates.items() if d is not None}
    stage_resolved = {
        s for s, ts in (
            ('open', open_ts), ('reviewed', reviewed_ts),
            ('revised', revised_ts), ('decision', decision_ts),
        ) if ts is not None
    }
    stage_timestamp_reliability = _stage_reliability(
        stage_present, stage_resolved)

    # Annotation count (subsystem fold-up).
    if annotations is None:
        proposal_annotation_count: int = 0
    else:
        proposal_annotation_count = _annotation_count_for_stem(
            path.stem, annotations)

    # Per-Response ``**Model**:`` captures, sourced from reconciled
    # `response` blocks post-cutoff (pipe-joined, positionally aligned
    # with ``reviewer_agents`` only in the legacy, pre-cutoff sense --
    # post-cutoff the two lists are independently sized by their own
    # kind's post-cutoff event count).
    response_empty, response_events = _reconciled_kind(reconciliation, events.KIND_RESPONSE)
    response_models: List[str] = (
        [] if response_empty else [e.block.model for e in response_events]
    )

    review_rounds: object = '' if review_empty else len(review_events)

    return {
        'stem': path.stem,
        'author': author,
        'date_opened': date_opened.isoformat() if date_opened else '',
        'status': status_token,
        'decision_date': decision_date.isoformat() if decision_date else '',
        'days_to_decision': days_to_decision,
        'review_rounds': review_rounds,
        'reviewer_agents': '|'.join(reviewer_agents),
        'cross_agent_type_review': cross_agent_type_review,
        'external_tier_review': external_tier_review,
        'revised': revised,
        'reviewed_date': reviewed_date.isoformat() if reviewed_date else '',
        'revised_date': revised_date.isoformat() if revised_date else '',
        'days_open_to_reviewed': days_open_to_reviewed,
        'days_reviewed_to_revised': days_reviewed_to_revised,
        'days_revised_to_decision': days_revised_to_decision,
        'hours_open_to_reviewed': hours_open_to_reviewed,
        'hours_reviewed_to_revised': hours_reviewed_to_revised,
        'hours_revised_to_decision': hours_revised_to_decision,
        'stage_timestamp_reliability': stage_timestamp_reliability,
        'proposal_annotation_count': proposal_annotation_count,
        'response_models': '|'.join(response_models),
    }


def proposal_rows(root: Path) -> List[Dict[str, object]]:
    """Every proposal row under *root*, sorted by ``date_opened`` then
    ``stem`` (deterministic order)."""
    config = load_config(root)
    annotations = _load_all_annotations(config.annotations_dir)
    rows = [
        extract_proposal_row(p, repo_root=root, annotations=annotations)
        for p in iter_proposal_files(root)
    ]
    rows.sort(key=lambda r: (str(r['date_opened']), str(r['stem'])))
    return rows


# --------------------------------------------------------------- plan rows


# ---------------------------------------------------------------------------
# The one runtime status vocabulary -- contained loader
# ---------------------------------------------------------------------------
#
# `lifecycle-status-vocabulary`, as replaced by that proposal's "
# replacement -- contained consumers and corpus boundary".  The contract is
# restated here **per consumer** rather than inherited from the other consumer
# by implication, so a reader can check the containment without opening
# ``scripts/transition_lint.py``.
#
# The path is derived from THIS file's own resolved location as the *sibling*
# ``lifecycle_planner.py``.  Both files install into ``tools/``
# (``tools/_lifecycle_metrics/extract.py`` and ``tools/lifecycle_planner.py``),
# so in a real adopter tree the sibling exists.  **At this file's SOURCE
# location it does not** -- ``templates/modules/default-on/_lifecycle_metrics/``
# has no planner beside it -- so the byte-identical twin *refuses* there.  That
# refusal is the contract, not a defect: metrics is a tool that runs from an
# installed tree.
#
# Before execution: refuse a missing or unreadable planner, a symlinked planner,
# a symlinked containing directory, and any planner resolving outside the
# expected root.  A fixed private module name, registered only for the loader's
# duration.  Cache only a fully initialized module carrying our sentinel.  On
# execution failure, purge the module and every child under its private name.
# A pre-existing entry is never trusted for being present.  No ambient
# ``sys.path``, no ``tools/__init__.py``, no CLI side effect at import.


class VocabularyUnavailable(RuntimeError):
    """The single vocabulary source could not be loaded *safely*.

    Raised instead of falling back to a local status tuple.  The fallback is
    the defect that removes: this module's own enum silently omitted
    ``awaiting-plan-review`` for as long as it was a separate declaration.
    """


_PLANNER_MODULE_NAME = "_lifecycle_metrics_lifecycle_planner"
_PLANNER_SENTINEL = "__cairn_vocabulary_loaded__"
#: ``PROPOSAL_STATES`` joined once ``events.py`` existed
#: (``metrics-events-not-prose`` Chunk 4): its closed grammar bounds a
#: `transition` block's `from_state`/`to_state` to "a declared lifecycle
#: status for that artifact type", and a proposal-hosted block needs the
#: planner's CURRENT proposal-status enum to check against.  The
#: historical variant (``HISTORICAL_PROPOSAL_STATES``) is deliberately
#: NOT added -- a freshly-authored event block only ever names a
#: currently-declared status, never a retired token, unlike the existing
#: plan-status prose-normalization path below, which reads archived
#: history and needs both groups.
_REQUIRED_EXPORTS = ('PLAN_STATES', 'HISTORICAL_PLAN_STATES', 'PROPOSAL_STATES')
_planner_cache = None


def _purge_planner_module() -> None:
    """Drop the private module and every child registered under its name."""
    prefix = _PLANNER_MODULE_NAME + '.'
    for name in [n for n in _sys.modules
                 if n == _PLANNER_MODULE_NAME or n.startswith(prefix)]:
        _sys.modules.pop(name, None)


def _validated_planner_path() -> Path:
    """The sibling planner path, or a clean refusal.  Never raises ``OSError``."""
    # Derived from the **unresolved** ``__file__`` on purpose.  An earlier
    # version resolved first and *then* asked whether the parent was a symlink
    # -- which can never be true of an already-resolved path.  That guard was
    # dead by construction: no real symlink could reach it, and the only way to
    # observe it firing was to monkeypatch ``Path.is_symlink``.  A guard
    # documented as live that cannot fire is worse than no guard, because it
    # reads as protection.  Found by the loader matrix, not by review.
    raw = Path(__file__).absolute()
    root = raw.parent.parent
    path = root / 'lifecycle_planner.py'
    try:
        if root.is_symlink():
            raise VocabularyUnavailable(
                f'the containing directory {root} is a symlink -- refusing to '
                f'load the status vocabulary through it')
        if path.is_symlink():
            raise VocabularyUnavailable(
                f'{path} is a symlink -- refusing to load the status '
                f'vocabulary through it')
        if not path.is_file():
            raise VocabularyUnavailable(
                f'no status vocabulary beside this module at {path} -- metrics '
                f'reads the lifecycle vocabulary from the planner and keeps no '
                f'local copy.  This is the expected refusal at the template '
                f'source location, where no planner is installed alongside.')
        # Containment compares **resolved forms on both sides**.  Comparing the
        # unresolved path against its own resolution would refuse any legitimate
        # checkout living under a symlinked ancestor -- macOS's
        # ``/tmp -> /private/tmp`` is exactly that shape -- which is a false
        # refusal dressed as a security check, not a protection.
        if path.resolve().parent != root.resolve():
            raise VocabularyUnavailable(
                f'{path} resolves outside the expected {root} root')
        with path.open('rb'):
            pass
    except OSError as exc:
        raise VocabularyUnavailable(
            f'cannot read the status vocabulary at {path}: {exc}') from None
    return path


def _vocabulary():
    """The planner module, loaded under containment and cached when complete."""
    global _planner_cache
    if _planner_cache is not None:
        return _planner_cache
    path = _validated_planner_path()

    existing = _sys.modules.get(_PLANNER_MODULE_NAME)
    if existing is not None:
        if (getattr(existing, _PLANNER_SENTINEL, False)
                and getattr(existing, '__file__', None) == str(path)
                and all(hasattr(existing, n) for n in _REQUIRED_EXPORTS)):
            _planner_cache = existing
            return existing
        _purge_planner_module()

    spec = _importlib_util.spec_from_file_location(_PLANNER_MODULE_NAME, path)
    if spec is None or spec.loader is None:
        raise VocabularyUnavailable(f'could not build an import spec for {path}')
    module = _importlib_util.module_from_spec(spec)
    _sys.modules[_PLANNER_MODULE_NAME] = module
    try:
        spec.loader.exec_module(module)
    except BaseException as exc:
        _purge_planner_module()
        raise VocabularyUnavailable(
            f'the status vocabulary at {path} failed to load: {exc!r}') from None
    missing = [n for n in _REQUIRED_EXPORTS if not hasattr(module, n)]
    if missing:
        _purge_planner_module()
        raise VocabularyUnavailable(
            f'the status vocabulary at {path} is missing {missing}')
    setattr(module, _PLANNER_SENTINEL, True)
    _planner_cache = module
    return module


def _plan_status_enum() -> Tuple[str, ...]:
    """The plan states metrics may resolve -- current **and historical**.

    Metrics read the whole corpus, most of which is archived and predates the
    vocabulary migration, so this enum is deliberately wider than the set an
    *active* artifact may declare.  Retiring a token
    from the current vocabulary must not stop longitudinal history parsing.

    The historical group comes last because `_normalize_plan_status` resolves by
    the FIRST enum the leading token starts with.  Order is load-bearing and the
    two groups do not prefix-collide (checked); current tokens must win.

    Dropping the historical half is a **silent** regression, not a loud one:
    every exact token still resolves to itself through the fall-through, and
    only the prefix cases move -- `'reviewed; ...'` would resolve `'reviewed'`
    instead of `'review'`, splitting one longitudinal bucket in two with the
    suite still green.  `test_metrics_status_normalization.py` is the guard.
    """
    vocab = _vocabulary()
    return tuple(vocab.PLAN_STATES) + tuple(vocab.HISTORICAL_PLAN_STATES)


def _normalize_plan_status(value: str) -> str:
    """Normalize a free-text status to its leading enum token.
    ``archived 2026-05-14 (...)`` -> ``archived``; ``reviewed; ...`` ->
    ``review``."""
    tokens = value.split()
    if not tokens:
        return ''
    lead = tokens[0].strip(' .,;:*').lower()
    for enum in _plan_status_enum():
        if lead.startswith(enum):
            return enum
    return lead


def _plan_status(text: str, sections: Sequence[Tuple[str, List[str]]]) -> str:
    """Read a plan's status from the ``**Status**:`` field, or the body
    of a ``## Status`` section for older plans."""
    field = _header_field(text, 'Status')
    if field:
        return _normalize_plan_status(field)
    for header, body in sections:
        if header.startswith('## Status'):
            for line in body:
                if line.strip():
                    return _normalize_plan_status(line.strip())
    return ''


def _proposal_slug(stem: str) -> str:
    """Drop the ``YYYY-MM-DD-<author>-`` prefix from a proposal stem,
    leaving the slug body for best-effort plan pairing.

    The author segment is a single dash-delimited token; it allows
    mixed case, digits, and underscores (``Alice``, ``Bob42``,
    ``mixedCase_2``) -- not lowercase-only -- so an upper/mixed-case
    author name does not silently defeat plan<->proposal pairing.  It stays
    dash-free so the match stops at the first dash and the slug body is
    captured intact."""
    m = re.match(r'\d{4}-\d{2}-\d{2}-[A-Za-z0-9_]+-(.+)', stem)
    return m.group(1) if m else stem


def _normalize_slug(slug: str) -> str:
    """Canonicalize a slug for matching: lowercase, ``_`` -> ``-``,
    trailing ``-plan`` stripped."""
    s = re.sub(r'_', '-', slug.lower())
    return re.sub(r'-?plan$', '', s)


def extract_plan_row(
    path: Path, proposal_stems: Sequence[str] = (),
    *, repo_root: Optional[Path] = None, include_git_timestamps: bool = True,
) -> Dict[str, object]:
    """Parse one plan file into a metrics row.

    ``proposal_stems`` feeds the slug-match fallback for
    ``paired_proposal``; pass the proposal corpus stems for the real
    walk, or a small set in unit tests.  ``repo_root``/
    ``include_git_timestamps`` mirror :func:`extract_proposal_row`'s
    shape (Chunk 6 widens this function to source
    ``plan_review_rounds``/``code_review_rounds`` from reconciled event
    blocks, which needs the same git access those two parameters
    already gate for the proposal schema)."""
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    sections = _split_h2_sections(lines)

    status = _plan_status(text, sections)

    # Part 3: plan_review_rounds/code_review_rounds are retained
    # event-derived fields Round 6's taxonomy names explicitly ("## Plan
    # review" / "## Code review" both map to review-pass) -- sourced
    # from reconciled blocks post-cutoff, classified by
    # `ReconciledEvent.section_kind` (which `events._section_kind_of`
    # derives from the matched HEADING line via
    # `_CODE_REVIEW_HEADING_RE`/`_PLAN_REVIEW_HEADING_RE`), not the
    # block's own self-reported `tier` field: the reconciler already
    # inspected the matched heading line to confirm the act exists at
    # all (Round 7 SS2 step 4), so this repurposes those two regexes
    # from direct heading-counters into a section-kind classifier of an
    # already-reconciled act, rather than depending on a block author
    # correctly setting `tier: Code`.  Empty (not the retired
    # heading-count) pre-cutoff, exactly like the proposal schema.
    reconciliation: 'Optional[events.Reconciliation]' = None
    if include_git_timestamps:
        root_for_events = repo_root if repo_root is not None else _REPO_ROOT
        plan_states = _vocabulary_states('PLAN_STATES')
        reconciliation = _reconcile_artifact(
            path, root_for_events, plans_dir(root_for_events) / '_template.md',
            plan_states,
        )
    review_empty, review_events = _reconciled_kind(reconciliation, events.KIND_REVIEW_PASS)
    if review_empty:
        plan_review_rounds: object = ''
        code_review_rounds: object = ''
    else:
        plan_review_rounds = sum(
            1 for e in review_events
            if e.section_kind == events.SECTION_KIND_PLAN_REVIEW
        )
        code_review_rounds = sum(
            1 for e in review_events
            if e.section_kind == events.SECTION_KIND_CODE_REVIEW
        )

    paired_proposal = ''
    reliability = 'none'
    source_line = _header_field(text, 'Source proposal')
    link_match = re.search(
        r'(\d{4}-\d{2}-\d{2}-[a-z0-9.-]+?)\.md', source_line)
    if link_match:
        paired_proposal = link_match.group(1)
        reliability = 'link'
    elif proposal_stems:
        slug_index = {
            _normalize_slug(_proposal_slug(s)): s for s in proposal_stems
        }
        match = slug_index.get(_normalize_slug(path.stem))
        if match:
            paired_proposal = match
            reliability = 'slug'

    return {
        'stem': path.stem,
        'status': status,
        'plan_review_rounds': plan_review_rounds,
        'code_review_rounds': code_review_rounds,
        'paired_proposal': paired_proposal,
        'paired_proposal_reliability': reliability,
    }


def plan_rows(root: Path) -> List[Dict[str, object]]:
    """Every plan row under *root*, sorted by ``stem``."""
    proposal_stems = [p.stem for p in iter_proposal_files(root)]
    rows = [
        extract_plan_row(p, proposal_stems, repo_root=root)
        for p in iter_plan_files(root)
    ]
    rows.sort(key=lambda r: str(r['stem']))
    return rows
