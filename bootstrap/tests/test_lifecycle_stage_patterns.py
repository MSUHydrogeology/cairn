"""Behavioural tests for the repaired lifecycle-stage commit vocabulary.

Source proposal stem ``stage-commit-patterns``
(``dev/proposals/2026-07-22-claude-stage-commit-patterns.md``); plan stem
``stage-commit-patterns``.  The defect: ``_STAGE_COMMIT_PATTERNS`` in the
default-on ``lifecycle-metrics`` module matched **zero** of Cairn's real
commit subjects, so every stage-timing metric came back empty at
``Best-effort`` while the tool exited 0.  The repair adds a second,
**scope-gated** vocabulary consulted only when the shipped one declines,
and makes classification a pure function of the subject.

**The oracle rule, binding on every test in this file.** Every expected
value below is a **hand-written literal**.  No expectation is derived from
``_SCOPED_STAGE_PATTERNS``, ``_STAGE_COMMIT_PATTERNS``,
``_stage_for_subject``, or any other object the code under test owns.  A
test whose expected set is the subject's own data structure is green
forever and proves nothing.  The two non-literal oracles here (T9, T10,
T12) are real ``git`` histories this file builds in ``tmp_path``, which
the subject also does not own.

**Loading.** These tests reach the classifier through the **template**
launcher ``templates/modules/default-on/lifecycle_metrics.py`` -- the same
``importlib`` idiom, and for the same recorded reason, as
``bootstrap/tests/test_lifecycle_metrics_config.py``.  This is a NEW test
file (FROZEN-NEW to the gate manifest, its node IDs COLLECTION-ADDED), so
it adds coverage without a gate re-anchor; ``test_reference_scripts.py``
is in ``frozen_files`` and is deliberately not edited.  Nothing here is
marked ``skip`` or ``xfail`` -- git is a hard requirement of this suite's
environment, and a skip guard is exactly the kind of check that gets
disarmed by the condition it was not designed to distinguish.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import List, Optional, Tuple

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
_LM_PATH = (
    CAIRN_ROOT / "templates" / "modules" / "default-on" / "lifecycle_metrics.py"
)


def _load_lm() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "cairn_lm_stage_patterns", _LM_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["cairn_lm_stage_patterns"] = module
    spec.loader.exec_module(module)
    return module


# The lifecycle-metrics template is a required, always-present source
# artifact in this repo, so it is loaded unconditionally -- its absence is a
# real failure to surface, not a skip.
_lm = _load_lm()


def _classify(subject: str) -> Optional[str]:
    return _lm._stage_for_subject(subject)


# ---------------------------------------------------------------------------
# T1 -- corpus regression
# ---------------------------------------------------------------------------

#: Real subjects, copied by hand out of ``git log --follow`` over the
#: proposal corpus, each paired with the stage a human reader judges
#: correct for it.  This is a **snapshot**, not a live log: it cannot catch
#: a *future* Cairn subject style drifting away from the vocabulary (only a
#: re-measurement can), and a live-history test would rot on every commit
#: and would not run in an adopter's tree at all.
_T1_CORPUS_VECTORS: List[Tuple[str, Optional[str]]] = [
    # -- open: the scope prefix plus a head-anchored `open` --------------
    ("dev/proposals: open stage-commit-patterns "
     "(reader fix; defect in shipped default-on code)", "open"),
    ("dev/proposals: open transition-lint "
     "(Part C split from review-record-integrity)", "open"),
    ("dev/proposals: open separator-detection", "open"),
    ("dev/proposals: open portable security sweeps", "open"),
    ("dev/proposals: open identity-not-name "
     "-- the same binding defect on three shipped surfaces", "open"),
    ("dev/proposals: open review-record-integrity "
     "(Phase A, proposal 1 of the broad-look tighten-up)", "open"),
    ("dev/proposals: open automated-review-committer doctrine proposal "
     "(R6 follow-up)", "open"),
    ("dev/proposals: open agent-context-scrub "
     "(attacker text reaching orientation)", "open"),
    ("dev/proposals: open yaml-parser-divergence", "open"),
    # -- decision: `Maintainer Decision` at the head of the body ---------
    ("dev/proposals: Maintainer Decision -- ACCEPT stage-commit-patterns",
     "decision"),
    ("dev/proposals: Maintainer Decision -- ACCEPT licensing", "decision"),
    ("dev/proposals: Maintainer Decision "
     "-- SUPERSEDE identity-not-name into four scopes", "decision"),
    ("dev/proposals: Maintainer Decision -- SUPERSEDE contributor-entry",
     "decision"),
    ("dev/proposals: Maintainer Decision AMENDMENT "
     "-- gate-reanchor-preflight expiry mechanism", "decision"),
    ("dev/proposals: Maintainer Decision -- accept adopter-entry doc-refresh",
     "decision"),
    # -- revised: a `response` / `revised` token in the stage phrase -----
    ("dev/proposals: stage-commit-patterns "
     "-- Response to Gemini External review", "revised"),
    ("dev/proposals: stage-commit-patterns "
     "-- Response + Revised (status: revised)", "revised"),
    ("dev/proposals: licensing -- Response to Gemini External review",
     "revised"),
    ("dev/proposals: dependency-advisory-coverage -- Revised (scope narrowed)",
     "revised"),
    ("dev/proposals: gate-reanchor-preflight "
     "-- Revised proposal Round 5 (expiry mechanics)", "revised"),
    ("dev/proposals: automated-review-committer "
     "-- Response (recommend supersede)", "revised"),
    ("dev/proposals: contributor-entry "
     "-- Response to Internal review (tier raised)", "revised"),
    ("dev/proposals: adopter-entry doc-refresh "
     "-- Internal review panel + Response + Revised", "revised"),
    ("dev/proposals: author responses to two SHIP re-reviews "
     "(Decision-ready)", "revised"),
    ("dev/proposals: author Response + Revised proposal "
     "(check_cairn self-host-compat)", "revised"),
    # -- reviewed: a `review` token in the stage phrase ------------------
    ("dev/proposals: stage-commit-patterns "
     "-- Internal review (fresh-context panel) + in-tree source", "reviewed"),
    ("dev/proposals: automated-review-committer "
     "-- Internal review (fresh-context panel)", "reviewed"),
    ("dev/proposals: interpreter-trust-root "
     "-- Internal review (tailored fresh-context panel) + in-tree source",
     "reviewed"),
    ("dev/proposals: add Gemini External Code Review to self-host-compat",
     "reviewed"),
    # -- None: no scope prefix ------------------------------------------
    ("Append Gemini External Review of stage-commit-patterns proposal", None),
    ("Append Gemini Flash External Security Review of scan-coverage proposal",
     None),
    ("fork-advisory-semantics: Response to Internal review", None),
    ("content-scan-detectors: Internal security review (BLOCKING findings)",
     None),
    ("claim-marker maintenance: transition-lint citations "
     "to the archived licensing plan", None),
    ("proposal-review: revise review-gate enforcement", None),
    ("dev/PLANNING: home the conda advisory gap as a deferred follow-up",
     None),
    ("check_cairn: resolve dev/ self-host claim-path findings "
     "(implements 2026-06-12 proposal)", None),
    ("Update status to reviewed in release-security-bar proposal", None),
    # -- None: scoped, but no stage token the vocabulary reads ----------
    ("dev/proposals: stage-commit-patterns "
     "-- reword header comment to clear the content scanner", None),
    ("dev/proposals: transition-lint "
     "-- record Maintainer sequencing direction (not a Decision)", None),
    ("dev/proposals: dependency-advisory-coverage "
     "-- amendment 2 (the binary was defective)", None),
    ("dev/proposals: gate-reanchor-preflight "
     "-- Amendment (incident + threat-model correction)", None),
    ("dev/proposals: contributor-entry "
     "-- Revision after I2 (scope does not survive)", None),
    ("dev/proposals: contributor-entry "
     "-- Maintainer direction on I2 (scope drops CONTRIBUTING.md)", None),
    ("dev/proposals: Maintainer ruling -- Class C assigned to scope 3", None),
    ("dev/proposals: archive the superseded contributor-entry", None),
    # `reviewed` (not `review`) has no word boundary before the trailing
    # `ed`, so a status-flip subject reads as nothing.
    ("dev/proposals: agent-context-scrub -- Status: proposed -> reviewed",
     None),
    ("dev/proposals: fork-advisory-semantics -- Status: proposed -> reviewed",
     None),
    # `reviews` is plural, so `\\breview\\b` fails on the trailing `s`.
    # Cairn's corpus is clean here by that coincidence, not by a guard.
    ("proposals: repair four check_cairn issues "
     "introduced by the landed reviews", None),
    ("proposal: split local security verification activation", None),
]


@pytest.mark.parametrize("subject,expected", _T1_CORPUS_VECTORS)
def test_t1_live_corpus_subjects_classify_as_judged(
    subject: str, expected: Optional[str],
) -> None:
    """T1 -- the test that would have caught the original defect.

    Reverting ``gitmeta.py`` to its pre-fix state sends every scoped
    vector here to ``None`` (and removes ``_stage_for_subject``
    outright).  Expectations are this file's own literals, hand-judged
    against the subject text; none is read back from the classifier.
    """
    assert _classify(subject) == expected


#: A real corpus subject that the shipped vocabulary used to claim before
#: the scope gate was ever reached: ``^Review\\b`` matched
#: ``review-gate-enforcement:`` because ``\\b`` sits between ``w`` and
#: ``-``.  The commit is a *Response* -- its correct stage is ``revised``
#: -- so this was a genuine wrong-stage assignment on Cairn's own corpus,
#: and it shipped.
#:
#: **Repaired 2026-08-10** by adding the ``(?!-)`` hyphen guard to the
#: shipped ``reviewed`` arm -- the same ``(?<!-)`` / ``(?!-)`` idiom the
#: scoped patterns already use, applied one level up.  ``stage-commit-patterns``
#: deliberately left the shipped defaults byte-unchanged (to keep
#: it additive) and archived recording this as an accepted residual; the
#: Maintainer then directed the repair separately.  The subject now
#: classifies as ``None``: no scope prefix, so the gate declines it rather
#: than guessing -- which is the honest outcome, not a silent one.
_T1_HYPHEN_COMPOUND_STEM_SUBJECT = (
    "review-gate-enforcement: Response to the External review "
    "(status: revised)"
)


def test_t1b_a_hyphen_compound_stem_is_not_claimed_by_the_shipped_arm() -> None:
    """T1b -- the repaired shipped arm declines a hyphen-compound stem.

    A ``review-...``-prefixed subject is a *plan stem*, not a review, and the
    shipped ``^Review\\b(?!-)`` arm no longer claims it.  This is the node
    that would have caught the original defect: strip ``(?!-)`` and it flips
    back to ``reviewed``, which is the wrong stage for a Response.
    """
    assert _classify(_T1_HYPHEN_COMPOUND_STEM_SUBJECT) is None


# ---------------------------------------------------------------------------
# T2 -- no bare-subject fallback
# ---------------------------------------------------------------------------

#: The Internal panel's ten adopter-plausible subjects (a hydrogeology
#: codebase).  Nine go to ``None`` because they carry no scope prefix and
#: ``if match is None: return None`` disposes of them before the scoped
#: vocabulary is consulted.  The tenth is the **pre-existing shipped-pattern
#: behaviour** described below -- status quo this fix inherits, not a
#: choice it made.
_T2_ADOPTER_VECTORS: List[Tuple[str, Optional[str]]] = [
    ("Add response surface model for aquifer recharge", None),
    ("Add impulse response function to the transport solver", None),
    ("fix: revise the calibration constants for Darcy flux", None),
    ("literature review of contaminant transport models", None),
    ("open sourcing the transport module", None),
    ("Decision tree classifier for facies prediction", None),
    ("revise mesh resolution near the well screen", None),
    ("docs: review the API surface", None),
    ("docs: address reviewer comments", None),
    # Pre-existing shipped-pattern behaviour: `^Review\b` has claimed this
    # subject since before this fix existed. NOT a choice this change made.
    ("review: tighten the recharge bounds", "reviewed"),
]


@pytest.mark.parametrize("subject,expected", _T2_ADOPTER_VECTORS)
def test_t2_unscoped_adopter_subjects_do_not_reach_the_new_vocabulary(
    subject: str, expected: Optional[str],
) -> None:
    """T2 -- the ratified narrowing: no bare-subject fallback.

    Deleting ``if match is None: return None`` and falling through with
    ``body = text`` flips eight of the nine ``None`` expectations to
    ``revised`` / ``reviewed`` / ``open`` / ``decision``.  The ninth,
    ``docs: address reviewer comments``, stays ``None`` because
    ``\\breview\\b`` fails on ``reviewer``.
    """
    assert _classify(subject) == expected


# ---------------------------------------------------------------------------
# T2b -- the residual INSIDE the gate, which T2 structurally cannot reach
# ---------------------------------------------------------------------------

#: Scoped-but-not-a-lifecycle-transition subjects.  Ten of the fourteen
#: receive a stage.  **The scope gate is a proxy for "touched a proposal
#: file", not for "is a lifecycle transition."** Cairn's own corpus is
#: clean only because its non-lifecycle proposal-file commits happen not to
#: carry the prefix -- a convention kept by habit, which this fix's scope
#: fence explicitly declines to document, and which an adopter has no
#: reason to share.  The four ``None`` rows are real assertions; the ten
#: that classify are pinned as **accepted, documented misclassifications**,
#: exactly as T2 pins ``review: tighten the recharge bounds``.
_T2B_SCOPED_NON_TRANSITION_VECTORS: List[Tuple[str, Optional[str]]] = [
    ("dev/proposals: widget "
     "-- still awaiting the maintainer decision on scope", "decision"),
    ("dev/proposals: foo -- Maintainer Decision pending, do not merge",
     "decision"),
    ("dev/proposals: fix a typo in the review section heading", "reviewed"),
    ("dev/proposals: foo -- fix a broken link in the Review section",
     "reviewed"),
    ("dev/proposals: foo -- rename the file after the review", "reviewed"),
    ("dev/proposals: foo -- drop the stale review checklist", "reviewed"),
    ("dev/proposals: foo -- correct a claim-check finding in the review record",
     "reviewed"),
    ("dev/proposals: foo -- add the missing Response heading placeholder",
     "revised"),
    ("dev/proposals: foo -- update responses table formatting", "revised"),
    ("dev/proposals: opening statement rewritten for clarity", "open"),
    ("dev/proposals: reformat all tables -- no content change", None),
    ("dev/proposals: archive the superseded contributor-entry", None),
    ("dev/proposals: foo -- revert the accidental revision", None),
    ("proposals: repair four check_cairn issues "
     "introduced by the landed reviews", None),
]


@pytest.mark.parametrize("subject,expected", _T2B_SCOPED_NON_TRANSITION_VECTORS)
def test_t2b_scoped_non_transitions_are_a_priced_residual(
    subject: str, expected: Optional[str],
) -> None:
    """T2b -- the class T2 cannot reach, pinned as documented outcomes.

    Widening the scoped ``reviewed`` pattern to ``(?<!-)\\breviews?\\b(?!-)``
    drops the ``None`` expectations from four to three (the
    ``…landed reviews`` subject flips ``None -> reviewed``).  Deleting
    ``decision`` arm 2 flips both ``decision`` probes to ``None`` -- the
    measurement showing arm 2 is the widest of the literals with no live
    corpus constraint.
    """
    assert _classify(subject) == expected


# ---------------------------------------------------------------------------
# T3 -- `dev/plans:` never classifies (the ratified narrowing)
# ---------------------------------------------------------------------------

#: Every live ``dev/plans: open …`` subject in the proposal corpus.  Each
#: is a proposal's **archive** event; reading it as the proposal's
#: **opening** is what re-adding ``plans?`` to the scope prefix would do.
_T3_PLAN_OPEN_SUBJECTS: List[str] = [
    "dev/plans: open record-corrections (+ archive proposal)",
    "dev/plans: open review-record-integrity (+ archive proposal)",
    "dev/plans: open adopter-licensing-compliance (+ archive proposal)",
    "dev/plans: open first-session-survivability (+ archive proposal)",
    "dev/plans: open solo-legacy-adopter-path (+ archive proposal)",
    "dev/plans: open ast-known-new-repin (+ archive proposal)",
    "dev/plans: open interpreter-trust-root-fallback (+ archive proposal)",
    "dev/plans: open lockfile-provenance-fields (+ archive proposal)",
    "dev/plans: open agent-context-scrub (+ archive proposal)",
    "dev/plans: open byline-classification (+ archive proposal)",
    "dev/plans: open fork-advisory-semantics (+ archive proposal)",
    "dev/plans: open gate-reanchor-preflight (+ archive proposal)",
    "dev/plans: open profile-parse-fail-open (+ archive proposal)",
    "dev/plans: open release-authenticity (+ archive proposal)",
    "dev/plans: open scan-coverage (+ archive proposal)",
    "dev/plans: open adopter-entry-doc-refresh; archive the accepted proposal",
]

#: Two further `dev/plans:` forms.  **The archive vector is inert under
#: this test's own named perturbation** -- re-adding ``plans?`` alone
#: leaves it ``None``, and stripping the hyphen guard alone leaves it
#: ``None``; it falls only under the *conjunction* of both.  Labelled here
#: rather than left for a reader to infer, because that subject is the
#: hyphen guard's sole historical justification.  The Code-review vector
#: does flip (``None -> reviewed``) under the ``plans?`` re-add.
_T3_OTHER_PLAN_SUBJECTS: List[str] = [
    "dev/plans: archive review-record-integrity "
    "(Chunk C pointer + lifecycle close)",
    "dev/plans: <slug> -- Code review (fresh-context, disclosed scribe)",
]


@pytest.mark.parametrize(
    "subject", _T3_PLAN_OPEN_SUBJECTS + _T3_OTHER_PLAN_SUBJECTS)
def test_t3_plan_scoped_subjects_classify_as_nothing(subject: str) -> None:
    """T3 -- ``plans?`` stays out of the scope prefix.

    Re-adding it flips all sixteen ``dev/plans: open …`` subjects
    ``None -> open`` -- i.e. each proposal's archive event read as its
    opening -- and the Code-review probe ``None -> reviewed``.
    """
    assert _classify(subject) is None


# ---------------------------------------------------------------------------
# T4 / T4b / T4c -- the hyphen guard and priority order
# ---------------------------------------------------------------------------

_T4_HYPHEN_GUARD_PROBES: List[str] = [
    "dev/proposals: interpreter-trust-root -- add Security-Review section",
    "dev/proposals: foo -- close out the review-record-integrity thread",
]


@pytest.mark.parametrize("subject", _T4_HYPHEN_GUARD_PROBES)
def test_t4_a_stage_word_inside_a_hyphen_compound_does_not_classify(
    subject: str,
) -> None:
    """T4 -- the ``(?<!-)`` / ``(?!-)`` guards.

    **No live corpus subject discriminates this guard**: ablating both
    lookarounds from the scoped patterns flips zero of the corpus's
    distinct subjects, because the guard's sole historical justification
    (``dev/plans: archive review-record-integrity …``) is excluded by the
    scope gate before the guard is ever reached.  These are therefore
    **constructed** probes, not corpus evidence -- and they do
    discriminate: stripping the guards from the scoped ``reviewed``
    pattern flips both ``None -> reviewed``.
    """
    assert _classify(subject) is None


def test_t4b_priority_order_retained_weak_vector() -> None:
    """T4b -- retained for continuity with the proposal's test list, with
    its weakness stated rather than implied.

    **It does not pin the hyphen guard.** It is green with the guard and
    without it, and green with ``reviewed`` moved ahead of ``open``.  It
    falls only under the *conjunction*: remove the guard **and** reorder,
    and it flips ``open -> reviewed``.
    """
    subject = ("dev/proposals: open interpreter-trust-root-fallback "
               "(F2 split; Security-Review gated)")
    assert _classify(subject) == "open"


def test_t4c_head_anchored_open_beats_a_revised_token_in_the_phrase() -> None:
    """T4c -- priority order, actually discriminating.

    Moving ``revised`` ahead of ``open`` in ``_SCOPED_STAGE_PATTERNS``
    flips this ``open -> revised``.
    """
    assert _classify(
        "dev/proposals: open widget-thing -- respond to the review") == "open"


# ---------------------------------------------------------------------------
# T5 -- one stage per subject
# ---------------------------------------------------------------------------

_T5_MULTI_TOKEN_SUBJECTS: List[str] = [
    "dev/proposals: licensing -- Response to Gemini External review",
    "dev/proposals: adopter-entry doc-refresh "
    "-- Internal review panel + Response + Revised",
]


@pytest.mark.parametrize("subject", _T5_MULTI_TOKEN_SUBJECTS)
def test_t5_a_subject_carrying_two_stage_words_gets_exactly_one_stage(
    subject: str,
) -> None:
    """T5 -- ``revised`` outranks ``reviewed``.

    Both subjects carry a ``response``/``revised`` token *and* a
    ``review`` token.  Swapping the two entries in
    ``_SCOPED_STAGE_PATTERNS`` flips both ``revised -> reviewed``.
    """
    assert _classify(subject) == "revised"


# ---------------------------------------------------------------------------
# T6 -- the three Decision forms
# ---------------------------------------------------------------------------

#: One **observed** form and two **constructed** ones.  Only the head-first
#: form occurs in this repository's log; ``-- Maintainer Decision`` occurs
#: **zero** times anywhere in it, and arm 2 of the ``decision`` pattern
#: flips zero corpus subjects.  The two slug-first vectors are hand-built
#: probes and are labelled as such rather than described as real forms.
_T6_DECISION_FORMS: List[Tuple[str, Optional[str]]] = [
    # observed (36 occurrences of this shape) -- matched by arm 1
    ("dev/proposals: Maintainer Decision -- ACCEPT licensing", "decision"),
    # constructed -- reaches arm 2 only
    ("dev/proposals: licensing -- Maintainer Decision -- ACCEPT", "decision"),
    # constructed -- reaches arm 2 only; without it this reads `reviewed`,
    # which is the wrong-stage-at-`Exact` bug the arm exists to close.
    ("dev/proposals: transition-lint -- Maintainer Decision "
     "-- ACCEPT (post Internal review)", "decision"),
    # documented, accepted false negative: a Decision written without the
    # word. Consistent with the fence (`supersede` gets no stage) and it
    # fails safe to a `Good` tier rather than a wrong `Exact`.
    ("dev/proposals: foo -- SUPERSEDE bar", None),
]


@pytest.mark.parametrize("subject,expected", _T6_DECISION_FORMS)
def test_t6_decision_forms(subject: str, expected: Optional[str]) -> None:
    """T6 -- both arms of the ``decision`` pattern.

    Deleting arm 2 (``|(?<!-)\\bmaintainer\\s+decision\\b(?!-)``) sends the
    first constructed vector to ``None`` and the second to ``reviewed``.
    The observed head-first form is unmoved by that ablation.
    """
    assert _classify(subject) == expected


# ---------------------------------------------------------------------------
# T7 -- the `sharpening` exclusion lives in the shipped pattern only
# ---------------------------------------------------------------------------

def test_t7a_scoped_reviewed_has_no_sharpening_exclusion() -> None:
    """T7a -- the widening this design refuses.

    Adding ``(?!.*\\bsharpening\\b)`` to the **scoped** ``reviewed``
    pattern flips this ``reviewed -> None``.
    """
    subject = ("dev/proposals: stage-commit-patterns -- Internal review "
               "(fresh-context panel) + Sharpening")
    assert _classify(subject) == "reviewed"


def test_t7b_shipped_sharpening_exclusion_is_preserved() -> None:
    """T7b -- the shipped exclusion, unedited.

    Deleting ``(?!.*\\bsharpening\\b)`` from the **shipped** ``reviewed``
    pattern flips this ``None -> reviewed``.
    """
    assert _classify("Review sharpening pass") is None


# ---------------------------------------------------------------------------
# T8 -- legacy / quickstart forms
# ---------------------------------------------------------------------------

#: The twelve backward-compatibility strings, asserted verbatim.  Two are
#: live repository content: ``Open proposal: README tagline``
#: (``docs/quickstart.md``) and ``Open proposal alice thing``
#: (``bootstrap/tests/test_reference_scripts.py``).
_T8_LEGACY_VECTORS: List[Tuple[str, Optional[str]]] = [
    ("Open proposal: README tagline", "open"),
    ("Open proposal alice thing", "open"),
    ("opening proposal foo", "open"),
    ("proposal: open foo", "open"),
    ("Decision: accept foo", "decision"),
    ("Decision -- accept foo", "decision"),
    ("proposal: Decision on foo", "decision"),
    ("proposal: respond to review", "revised"),
    ("proposal: revise foo", "revised"),
    ("Revised proposal foo", "revised"),
    ("Review round 1 of foo", "reviewed"),
    ("Review sharpening pass", None),
]


@pytest.mark.parametrize("subject,expected", _T8_LEGACY_VECTORS)
def test_t8_legacy_forms_still_classify_identically(
    subject: str, expected: Optional[str],
) -> None:
    """T8 -- backward compatibility, with its limit stated.

    **Green before *and* after this plan's diff**: the shipped patterns are
    not edited, so backward compatibility is guaranteed by construction and
    this test cannot be red by the change it accompanies.  Its falsifying
    future state is a later author editing the shipped arms.

    **And it does not catch every such edit.** Because the scope prefix
    accepts the *singular* ``proposals?``, every legacy form beginning
    ``proposal:`` is re-matched by the new scoped vocabulary, so deleting
    the shipped pattern behind it is invisible here.  Measured per shipped
    pattern: ``open`` 3 of 4 vectors detect the deletion, ``revised``
    **1 of 3**, ``decision`` 1 of 2, ``reviewed`` 1 of 1.  T8 therefore
    pins the ``^Open proposal`` / ``opening proposal`` / ``^Decision[:-]``
    / ``Revised proposal`` / ``^Review`` arms **and nothing else**.
    """
    assert _classify(subject) == expected


# ---------------------------------------------------------------------------
# Synthetic-repository helpers (T9, T10, T12)
# ---------------------------------------------------------------------------

_SYNTHETIC_PROPOSAL = (
    "# Widget thing\n\n"
    "**Author**: Alice (Strategy)\n"
    "**Date opened**: 2026-05-01\n"
    "**Status**: accepted\n\n"
    "## Proposal\n\nBody.\n\n"
    "## Review -- Bob (Internal Reviewer) -- 2026-05-02\n\n"
    "* **[P1]** a finding\n\n"
    "## Revised proposal -- Alice -- 2026-05-03\n\n"
    "Revised body.\n\n"
    "## Decision -- Carol -- 2026-05-04\n\n"
    "Accept.\n"
)

_GIT_ENV = ["-c", "user.email=t@t.t", "-c", "user.name=t"]


def _init_repo(root: Path) -> None:
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)],
                   check=True, capture_output=True)


def _commit_all(root: Path, subject: str) -> None:
    subprocess.run(["git", "-C", str(root), "add", "-A"],
                   check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(root)] + _GIT_ENV + ["commit", "-q", "-m", subject],
        check=True, capture_output=True,
    )


def _write_proposal(root: Path, body: str) -> Path:
    proposals = root / "dev" / "proposals"
    proposals.mkdir(parents=True, exist_ok=True)
    path = proposals / "2026-05-01-alice-widget-thing.md"
    path.write_text(body, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# T9 -- classify once, no fall-through
# ---------------------------------------------------------------------------

def test_t9_a_second_open_commit_does_not_fall_through_to_revised(
    tmp_path: Path,
) -> None:
    """T9 -- classification is a pure function of the subject.

    The old loop tested the *filled/unfilled* state of a slot before
    deciding whether a pattern applied, so a subject whose correct stage
    was already filled fell through and was re-tested against the
    remaining stages.  Here commit 2 classifies ``open`` (already filled)
    and carries a ``respond to`` token in its stage phrase; under a
    restored fall-through loop ``revised`` takes commit 2.

    **This synthetic history is the only thing pinning the byte-unchanged
    defaults** -- running
    both loop shapes over the live corpus's per-file histories produced
    identical results for every proposal file, so the live tree does not
    exercise it.
    """
    path = _write_proposal(tmp_path, _SYNTHETIC_PROPOSAL)
    _init_repo(tmp_path)
    _commit_all(tmp_path, "dev/proposals: open widget-thing (first)")
    path.write_text(_SYNTHETIC_PROPOSAL + "\nMore.\n", encoding="utf-8")
    _commit_all(
        tmp_path,
        "dev/proposals: open widget-thing again -- respond to the review")

    resolved = _lm._resolve_stage_commits(path, repo_root=tmp_path)
    log = subprocess.run(
        ["git", "-C", str(tmp_path), "log", "--reverse", "--format=%h"],
        check=True, capture_output=True).stdout.decode().split()
    assert resolved["open"] is not None
    assert resolved["open"][0] == log[0], "open must take the FIRST commit"
    assert resolved["revised"] is None, (
        "commit 2 fell through to `revised` -- the P2 defect")
    assert resolved["reviewed"] is None
    assert resolved["decision"] is None


# ---------------------------------------------------------------------------
# T10 -- end-to-end through the public path
# ---------------------------------------------------------------------------

def test_t10_public_path_reports_exact_with_populated_hour_deltas(
    tmp_path: Path,
) -> None:
    """T10 -- ``proposal_rows`` on a synthetic four-commit history.

    Two spec conditions worth stating rather than rediscovering:

    1. **Never assert truthiness on an hour delta.** Four commits made in
       one test run share a committer timestamp, so all three deltas are
       exactly ``0.0`` -- a passing spec that a bare
       ``assert row['hours_open_to_reviewed']`` would fail.  That is the
       same fact the module's own degradation docstring records.
    2. **The synthetic proposal must carry dated stage sections.**
       ``stage_present`` is derived from the *document*, not from git, so
       a bare file yields ``Good`` even with four resolving commits.

    Never asserts a tier against the live Cairn corpus: a transient
    ``git log`` failure returns ``[]`` and silently degrades a row, so a
    run under concurrent load is not evidence.
    """
    _write_proposal(tmp_path, _SYNTHETIC_PROPOSAL)
    _init_repo(tmp_path)
    for subject in (
        "dev/proposals: open widget-thing",
        "dev/proposals: widget-thing -- Internal review (fresh-context panel)",
        "dev/proposals: widget-thing -- Response + Revised (status: revised)",
        "dev/proposals: Maintainer Decision -- ACCEPT widget-thing",
    ):
        (tmp_path / "dev" / "proposals"
         / "2026-05-01-alice-widget-thing.md").write_text(
            _SYNTHETIC_PROPOSAL + f"\n<!-- {subject} -->\n", encoding="utf-8")
        _commit_all(tmp_path, subject)

    rows = _lm.proposal_rows(tmp_path)
    assert len(rows) == 1
    row = rows[0]
    assert row["stage_timestamp_reliability"] == "Exact"
    for column in (
        "hours_open_to_reviewed",
        "hours_reviewed_to_revised",
        "hours_revised_to_decision",
    ):
        value = row[column]
        assert value != "", f"{column} is empty"
        assert isinstance(value, float), f"{column} is {type(value)!r}"
        assert value >= 0, f"{column} is negative: {value!r}"


# ---------------------------------------------------------------------------
# T11 -- the function never raises
# ---------------------------------------------------------------------------

_T11_HOSTILE_SUBJECTS: List[str] = [
    "",
    "   ",
    " -- ",
    "dev/proposals: ",
    "dev/proposals: ünïcödé revisé",
    "dev/proposals: " + "x" * 500,
]


@pytest.mark.parametrize("subject", _T11_HOSTILE_SUBJECTS)
def test_t11_classification_never_raises(subject: str) -> None:
    """T11 -- degrade, never raise.

    Perturbation: replace ``phrase = parts[1] if len(parts) > 1 else body``
    with an unconditional ``parts[1]``.  That raises ``IndexError`` on
    **three of these six** vectors -- the three carrying the scope prefix.
    ``''``, ``'   '`` and the separator-only subject return ``None`` at
    ``if match is None: return None``, *before* the split, so the
    perturbation's reach is narrower than "every separator-less subject";
    the test still reds.
    """
    result = _classify(subject)
    assert result is None or result in {
        "open", "reviewed", "revised", "decision"}


# ---------------------------------------------------------------------------
# T12 -- the degradation floor is preserved
# ---------------------------------------------------------------------------

def test_t12_a_target_with_no_git_still_degrades_to_best_effort(
    tmp_path: Path,
) -> None:
    """T12 -- no ``.git`` at all: ``Best-effort``, empty hour columns, no
    exception.

    Deliberately duplicates the guarantee
    ``bootstrap/tests/test_reference_scripts.py`` already holds, so it is
    local to the changed code.  **Stated honestly: no change in this
    plan's own diff can red T12** -- it re-asserts a pre-existing
    guarantee.  Its perturbation is a hypothetical future one: seeding a
    stage unconditionally in ``_resolve_stage_commits`` flips the tier to
    ``Exact`` on a repo with no history at all.
    """
    _write_proposal(tmp_path, _SYNTHETIC_PROPOSAL)
    assert not (tmp_path / ".git").exists()

    rows = _lm.proposal_rows(tmp_path)
    assert len(rows) == 1
    row = rows[0]
    assert row["stage_timestamp_reliability"] == "Best-effort"
    assert row["hours_open_to_reviewed"] == ""
    assert row["hours_reviewed_to_revised"] == ""
    assert row["hours_revised_to_decision"] == ""
