#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Cairn lifecycle checker/planner -- the *read-only* lifecycle aid.

This is the read-only arm of the lifecycle-mechanization program
(`doctrine/lifecycle-contract.md`).  It is a **sibling** to
`tools/lifecycle.py` (the session-routine backend), deliberately NOT an
extension of it: `lifecycle.py` is itself a complexity-debt split
candidate, and the planner composes with -- rather than deepens -- it.

What it does:

* `next <artifact>` -- report an artifact's current lifecycle **state**,
  the **legal next transitions** from it, and, for each, the
  **preconditions** the artifact does or does not yet structurally
  satisfy.
* `next <artifact> --to <state>` -- emit a **proposed** house-format
  section **scaffold** plus a **mutation manifest** (what would change)
  for the chosen transition.
* `scan` -- run the structural conformance checks over the whole local
  `dev/proposals/` + `dev/plans/` corpus and report violations.  This is
  also the **adopter-side fidelity scan** (the same checker, double duty).
* `guard` -- an **advisory** pre-commit orientation pass: summarize the
  staged set, run `claim_check` on staged `dev/` docs if it is installed,
  and remind that the shipped work-intent hook is the *blocking* layer.

The authority contract -- the load-bearing safety boundary
=========================================================

The tool may **mechanize the assembly, the gates, and the formatting**;
it must **never mechanize the judgment**.  Concretely, and enforced by
construction here:

1. **Structural attestation, not authenticity.**  It attests the
   *structure and presence* of an authority-bearing artifact (a Decision
   blockquote is present and isolated; a Review section exists) and
   reports a *missing or malformed* one.  It **never certifies
   authenticity** -- a local tool has no access to the harness's chat or
   system logs, so it cannot know whether a quoted authorization was
   truly given.  The committing harness/operator remains the sole
   guarantor.
2. **Infer, validate, quote -- never invent.**  It infers structural
   state, validates the attestations committed artifacts carry, and
   quotes nothing it was not given.  A generated **review scaffold
   carries NO reviewer attribution**; a generated **Decision scaffold
   carries an empty verbatim-authorization blockquote** the operator
   must fill -- the tool never authors a disposition, a finding, or an
   authorization.
3. **A status flips only on a machine-verifiable precondition.**  When a
   transition's documentary precondition is structurally absent, the
   tool reports the **missing attestation** rather than presenting the
   transition as ready.
4. **No mutate, no commit.**  Every code path here is read-only: it
   reads files and emits text to stdout.  It never writes a file, never
   stages, never commits.  A test proves this invariant.

Read-only by construction
=========================

This module performs **no writes**.  It opens files only for reading,
runs git only with read-only subcommands, and emits every scaffold and
manifest to **stdout** -- the operator copies it into the artifact and
owns the transition.  The one consequence of a mis-run is text on the
terminal, never a changed tree.

Optional aid, not the minimum kernel
=========================================

The checker is **stdlib-only** and **vendor-neutral**, like the other
lifecycle tools.  It is an **optional aid outside the minimum mechanized
kernel** (per the stack-neutrality runtime contract): a team without a
Python runtime runs the lifecycle **manually** against
`doctrine/lifecycle-contract.md`, with no loss of the contract itself --
only of the mechanized convenience.  There is no fail-closed boot if
Python is absent and no heavy dependency.

Run:
    python tools/lifecycle_planner.py next dev/proposals/<file>.md
    python tools/lifecycle_planner.py next dev/plans/<file>.md --to executing
    python tools/lifecycle_planner.py scan
    python tools/lifecycle_planner.py guard
    python tools/lifecycle_planner.py board --compact
    python tools/lifecycle_planner.py board --format json
    python tools/lifecycle_planner.py board --explain <artifact-stem>
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# --- structured output (mirrors tools/lifecycle.py) --------------------------

_PREFIX = "lifecycle-planner:"


def _emit(message: str = "") -> None:
    """Print a normal line to stdout."""
    if message:
        print(f"{_PREFIX} {message}")
    else:
        print()


def _emit_section(title: str) -> None:
    """Print a section header so relayed output is legibly grouped."""
    print(f"\n{_PREFIX} == {title} ==")


def _warn(message: str) -> None:
    """Print a non-fatal advisory to stderr."""
    print(f"{_PREFIX} NOTE: {message}", file=sys.stderr)


class PlannerError(RuntimeError):
    """A fatal, *actionable* failure -- never a silent skip.

    Raised when a step cannot proceed and the operator must act (e.g. the
    artifact path does not exist).  `main` turns it into a non-zero exit
    with the message, not a stack trace.
    """


# --- environment resolution (read-only git, like tools/lifecycle.py) ---------


def _git_env() -> dict:
    """A noninteractive, no-pager git environment."""
    env = dict(os.environ)
    env["GIT_PAGER"] = "cat"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def _repo_root(start: Optional[Path] = None) -> Path:
    """Return the git repository root containing `start` (default: cwd)."""
    cwd = str(start) if start is not None else None
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd, capture_output=True, text=True, check=True, env=_git_env(),
        )
    except FileNotFoundError as exc:
        raise PlannerError(
            "git was not found on PATH; the planner resolves the repo root via git."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise PlannerError(
            "not inside a git repository -- run the planner from within the "
            "project checkout."
        ) from exc
    return Path(out.stdout.strip())


def _git_readonly(args: List[str], root: Path) -> Optional[str]:
    """Run a **read-only** git command and return stdout, or None on failure.

    Used only by the advisory `guard` pass.  Never invoked with a mutating
    subcommand; a failure is a soft None (the guard is advisory)."""
    try:
        out = subprocess.run(
            ["git", *args], cwd=str(root), capture_output=True, text=True,
            check=False, env=_git_env(),
        )
    except OSError:
        return None
    return out.stdout if out.returncode == 0 else None


def _today() -> str:
    """Today's date as ``YYYY-MM-DD`` (local)."""
    return _dt.date.today().isoformat()


# --- the AI-vs-human identity model -----------------------------------------
#
# Several preconditions turn on *who* authored a section: a review is
# authored by a reviewer (an AI agent or a human), but a Decision is a
# *human Maintainer* authority.  The model is **three-way and positive**,
# never a denylist residual (a cross-phase review finding): an identity is
# **known-AI** (on the AI-agent registry), **known-human-Maintainer** (on a
# project-owned allowlist), or **unknown**.  A denylist alone cannot prove
# humanity -- a novel/renamed agent would launder into the human residual --
# so a terminal Decision authored by an **unknown** identity is a structural
# violation (configure the project's Maintainer allowlist), NOT a silent
# human.  Both lists are config-extensible (``dev/.cairn/agent-identities.json``),
# never a code edit.  None of this authenticates the quoted authorization --
# the tool attests *structure*, the committing operator guarantees the quote.
#
# What a roster entry IS -- the config's grammar, written down here because
# this comment is its only home:
#
#   * ``human_maintainers`` -- each entry is the **complete display name
#     exactly as it appears in the byline**, never a name fragment.  Matching
#     is whole-name and **exact** (tuple equality over folded words), so
#     ``["Anthony Kendall"]`` recognizes the byline ``Anthony Kendall`` and
#     nothing else.  The older fragment form ``["Anthony", "Kendall"]``
#     recognized any byline *containing* either word -- the privilege-widening
#     defect this grammar replaced.  Words are separated by **ASCII
#     whitespace** and compared separator-for-separator, so a display name
#     written with a non-ASCII space is rostered with that exact separator
#     (or typed with ASCII spaces).
#   * ``ai_agents`` -- each entry is a *token* matched as a **prefix** of any
#     byline word, so a versioned agent byline still resolves to its agent.
#
# Both lists fold through the same functions as the byline, at the two
# strengths ``_fold_word`` documents.  An entry that folds to nothing is
# **dropped**, never admitted as a wildcard that would match everything.

#: The built-in AI-agent identity registry: flagging-strength tokens, each
#: matched as a **prefix** of any word of the author name.  Extended -- never
#: replaced -- by an optional ``dev/.cairn/agent-identities.json`` (an
#: ``ai_agents`` list), so a future vendor (or a project's renamed agent) is a
#: data edit.
_AI_AGENT_REGISTRY: frozenset = frozenset({
    "codex", "claude", "gemini", "antigravity", "cursor", "copilot",
    "qwen", "aider", "devin", "gpt", "openai", "anthropic", "agent",
})

#: Where the optional identity-registry extension lives.
_AGENT_IDENTITIES_REL = ("dev", ".cairn", "agent-identities.json")

#: The word separator.  Deliberately an **explicit ASCII class**, not
#: ``str.split()`` and not a ``\s`` class in a ``str`` pattern: both of those
#: are Unicode-aware and would treat a ``Zs`` space separator (NO-BREAK
#: SPACE, IDEOGRAPHIC SPACE, NARROW NO-BREAK SPACE, ...) as a word break.
#: Here such a character stays *inside* its word, so it cannot act as an
#: invisible word break, and a display name that carries one is rostered
#: with that exact separator.  The mechanism is the requirement, not a
#: description of it.
_ASCII_WS_RE = re.compile(r"[ \t\n\r\f\v]+")

#: The fold's **allow-set** over ASCII: the only ASCII characters a folded
#: word keeps.  Written as an explicit set (rather than as a deletion
#: pattern) so that the rule and the code are the same statement -- the
#: previous ``re.sub(r"[^a-z0-9]", ...)`` named two deleted classes and
#: silently deleted three.  Case-folding runs first, so ASCII upper-case
#: letters survive as their lower-case selves.
_FOLD_KEEP_ASCII = frozenset("abcdefghijklmnopqrstuvwxyz0123456789")


def _fold_word(raw: str, form: str) -> str:
    """Fold one display-name word to the key actually compared.

    Case-fold (``str.casefold``, stronger than ``lower()``), normalize at
    `form` on both sides of the case-fold, drop combining marks, then keep a
    character only if it is **non-ASCII** or in ``_FOLD_KEEP_ASCII``.

    `form` is ``"NFKD"`` on the flagging leg and ``"NFD"`` on the granting
    leg; see ``_flag_words`` / ``_grant_words`` for why the two strengths
    differ.

    **Three classes are deleted, and all three are named** -- the superseded
    rule named two of them and silently deleted the third:

    1. ASCII punctuation **and symbols** (plus the ASCII space characters the
       tokenizer has already consumed);
    2. the **C0 control characters and DEL**, which the superseded rule
       deleted without saying so;
    3. **combining marks**, at whatever strength `form` decomposed to.

    Over ASCII, (1) and (2) together are exactly the complement of the
    allow-set: every ASCII character that is neither an ASCII letter nor an
    ASCII digit.  That equality is what makes the rule and the code one
    statement, and it is pinned by a test.

    **No letter and no digit, in any script, folds to nothing.** That is the
    invariant the accepted design turns on -- *dropping a character must
    never widen authority* -- and it is exactly what the superseded
    ``re.sub(r"[^a-z0-9]", "", raw.lower())`` violated: it deleted every
    non-ASCII letter, so a confusable letter (a Cyrillic character that
    renders identically to an ASCII one) could be *deleted into* a match on
    the human-Maintainer allowlist.  Deleting nothing that carries identity
    is what closes that."""
    d = unicodedata.normalize(form, unicodedata.normalize(form, raw).casefold())
    d = "".join(c for c in d if not unicodedata.combining(c))
    return "".join(c for c in d
                   if ord(c) > 0x7F or c in _FOLD_KEEP_ASCII)


def _fold_words(name: str, form: str) -> Tuple[str, ...]:
    """Split `name` on ASCII whitespace and fold each word at `form`.

    Words that fold to nothing (a lone hyphen, a bare parenthesis) are
    dropped, so the key of a punctuation-only name is the empty tuple."""
    return tuple(w for w in (_fold_word(p, form)
                             for p in _ASCII_WS_RE.split(name)) if w)


def _flag_words(name: str) -> Tuple[str, ...]:
    """The FLAGGING key: words folded at ``NFKD`` (compatibility).

    ``NFKD`` additionally collapses presentational variants -- mathematical
    alphanumerics, circled letters, full-width forms -- onto their plain
    letters, so a presentational disguise of a registry entry still resolves
    to it.  Over-folding **here** produces an over-flag: a spurious,
    human-reviewable violation, which is the SAFE direction for a fidelity
    scan.  Contrast ``_grant_words``, where over-folding would *grant*."""
    return _fold_words(name, "NFKD")


def _grant_words(name: str) -> Tuple[str, ...]:
    """The GRANTING key: words folded at ``NFD`` (canonical only).

    ``NFD`` separates a letter from its accents and does nothing else, so a
    presentational variant of a rostered name does **not** collapse onto it.
    Over-folding here would widen the set of strings that classify as the
    human Maintainer -- it would *grant* authority rather than flag -- which
    is why the granting leg is deliberately the weaker normalization.  The
    asymmetry is the one genuinely non-obvious choice in this model, so it is
    stated rather than left to be inferred."""
    return _fold_words(name, "NFD")


def _load_ai_registry(root: Path) -> frozenset:
    """Return the AI-agent registry, extended by the optional config.

    The config **adds** identities; it never shrinks the built-in set, so
    a malformed or hostile config cannot reclassify a known AI agent as
    the human Maintainer.  Absent / unreadable / wrong-shape -> the
    built-in registry unchanged (fail-safe, never a crash).

    Config entries fold through ``_flag_words`` -- the same function a byline
    word folds through -- so the extension mechanism is symmetric with the
    built-ins.

    **That symmetry is what creates the empty-token hazard, and the guard
    against it is part of the same change** -- the hazard is introduced here,
    not inherited.  The superseded loader did not fold at all
    (``{str(t).strip().lower() for t in extra if str(t).strip()}``), and a
    truthy ``.strip()`` guarantees a non-empty ``.lower()``, so it could not
    emit the empty token however malformed the entry was.  Folding can:
    ``"-"`` and ``"  .  "`` fold to nothing, and an admitted empty token is a
    *universal prefix* -- ``"anything".startswith("")`` is ``True`` -- which
    would classify **every** byline as AI.  The filter is therefore on the
    **folded** value, and it lives one level down in ``_fold_words``, which
    drops a word that folds to nothing."""
    path = root.joinpath(*_AGENT_IDENTITIES_REL)
    if not path.is_file():
        return _AI_AGENT_REGISTRY
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _AI_AGENT_REGISTRY
    extra = data.get("ai_agents") if isinstance(data, dict) else None
    if not isinstance(extra, list):
        return _AI_AGENT_REGISTRY
    # The folded-value filter lives in ``_fold_words``, which drops a word
    # that folds to nothing -- so an entry of ``"-"`` contributes no token at
    # all rather than the empty-string universal prefix.
    tokens = {tok for t in extra for tok in _flag_words(str(t))}
    return _AI_AGENT_REGISTRY | tokens


def _identity_token(name: str) -> str:
    """Normalize an author display name to its classification token.

    The **first** flagging-strength word of the name (``Sage (External
    Reviewer)`` -> ``sage``), or ``""`` for a name with no folding word.
    This preserves the *real* identity rather than collapsing it to a closed
    enum.  It shares ``_flag_words`` with the AI leg, so the independence
    comparator inherits ``NFKD`` and stops deleting non-ASCII letters."""
    words = _flag_words(name)
    return words[0] if words else ""


def _is_ai_agent(name: str, registry: frozenset) -> bool:
    """True if `name` matches a known AI agent (the AI leg of `IdentityModel`).

    A registry token matched as a **prefix** of any flagging-strength word
    classifies the name as AI, so version/build suffixes (``agent-3.5`` ->
    ``agent35``, ``agent-4o`` -> ``agent4o``, ``\U0001f916 Agent`` ->
    ``agent``) still resolve to their agent -- the exact evasions a
    first-token exact-match would miss.  The match deliberately **errs
    toward flagging**: a human whose word happens to begin with an agent
    name is over-flagged (a spurious, human-reviewable violation -- the SAFE
    direction for a fidelity scan), but a versioned agent byline is never
    laundered into the human residual (the unsafe direction that would let
    an AI author a Maintainer Decision unflagged)."""
    for tok in _flag_words(name):
        if any(tok.startswith(agent) for agent in registry):
            return True
    return False


def _load_human_maintainers(root: Path) -> frozenset:
    """Return the project's POSITIVE human-Maintainer allowlist from
    ``dev/.cairn/agent-identities.json`` (a ``human_maintainers`` list), as a
    frozenset of **granting-strength word tuples** -- one tuple per complete
    display name. Absent / unreadable / wrong-shape -> empty (fail-closed:
    with no configured Maintainer identity, NO byline can be confirmed human,
    so every terminal Decision surfaces as an unrecognized-identity violation
    until the project configures its Maintainer). This is the deliberate
    inverse of the AI registry's fail-safe: humanity must be *proved*, never
    assumed.

    The filter is on the **folded** value, not the raw entry. A blank-entry
    test is the wrong predicate here: under tuple equality ``() == ()`` is
    ``True``, so a punctuation-only typo (``"-"``) admitted as the empty
    tuple would make a punctuation-only byline the human Maintainer."""
    path = root.joinpath(*_AGENT_IDENTITIES_REL)
    if not path.is_file():
        return frozenset()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return frozenset()
    lst = data.get("human_maintainers") if isinstance(data, dict) else None
    if not isinstance(lst, list):
        return frozenset()
    keys = {_grant_words(str(t)) for t in lst}
    return frozenset(k for k in keys if k)


class IdentityModel:
    """Three-way author classification: known-AI / known-human / unknown.

    A denylist alone cannot prove humanity (a novel or renamed agent would
    launder into the human residual), so the human Maintainer is a **positive
    allowlist**, never the residual. ``classify`` returns ``"ai"`` /
    ``"human"`` / ``"unknown"``; the conformance check treats ``unknown`` at a
    terminal Decision as a structural violation, not a silent human.

    The human leg is **whole-name exact** -- tuple equality of the byline's
    granting key against the roster's key set -- not containment. A byline
    that *contains* a rostered name plus anything else no longer matches,
    whether the "anything else" is a disguised agent name, a misspelling, or
    a digit substitution."""

    def __init__(self, ai_registry: frozenset, human: frozenset) -> None:
        self.ai_registry = ai_registry
        self.human = human

    def classify(self, name: str) -> str:
        if _is_ai_agent(name, self.ai_registry):
            return "ai"
        if _grant_words(name) in self.human:
            return "human"
        return "unknown"


def _load_identity_model(root: Path) -> IdentityModel:
    """Load the three-way identity model from the project config."""
    return IdentityModel(_load_ai_registry(root), _load_human_maintainers(root))


def _ascii_hint(name: str) -> str:
    """An ``ascii()``-escaped rendering of `name`, or ``""`` if it is ASCII.

    ``repr()`` renders a confusable byline *indistinguishably* from the
    honest one, because ``repr()`` of a ``str`` leaves non-ASCII characters
    as-is.  ``ascii()`` spells the confusable out as its escape, so a reader
    can see that two identical-looking bylines are not the same string.  A
    flag the reader cannot interpret is half a flag."""
    if name.isascii():
        return ""
    return f", non-ASCII -- escaped: {ascii(name)}"


# --- artifact parsing --------------------------------------------------------

# Markdown, git, grep, and re.MULTILINE recognize CR, LF, and CRLF as line
# endings. str.splitlines() adds eight separators those readers do not, which
# can manufacture structural headings that no human-facing reader sees.
_LINE_ENDING_RE = re.compile(r"\r\n?|\n")


def _split_lines(text: str) -> List[str]:
    """Split on markdown line endings with ``str.splitlines`` tail semantics."""
    if not text:
        return []
    lines = _LINE_ENDING_RE.split(text)
    if lines[-1] == "":
        lines.pop()
    return lines


class Section:
    """A parsed ``##``/``###`` section header from an artifact.

    `kind` is the leading label (``Review`` / ``Response`` / ``Revised
    proposal`` / ``Decision`` / ``Plan review`` / ``Code review`` / ...);
    `name`, `role`, `date` are parsed from the ``-- <name> (<role>) --
    <date>`` tail when present; `has_blockquote` is set later for Decision
    sections; `body` is the raw text under the header."""

    def __init__(self, level: int, kind: str, name: str, role: str,
                 date: str, line_no: int) -> None:
        self.level = level
        self.kind = kind
        self.name = name
        self.role = role
        self.date = date
        self.line_no = line_no
        self.body = ""
        self.has_isolated_blockquote = False


class Artifact:
    """A parsed proposal or plan."""

    def __init__(self, path: Path, kind: str, text: str) -> None:
        self.path = path
        self.kind = kind  # "proposal" | "plan"
        self.text = text
        self.status: str = ""
        self.author: str = ""
        self.plan_review: str = ""  # "required(...)" | "not required(...)" | ""
        self.sections: List[Section] = []
        self.has_disposition_attestation = False
        self.has_fidelity_signoff = False
        self.has_code_review_marker = False


#: ``## Review -- Reviewer A (External Reviewer) -- 2026-06-08``.  The
#: name and the ``(role)`` and the date are each optional in the tail, so
#: a partially-formed header still parses (and the missing piece becomes a
#: reported gap rather than a crash).
_HEADER_RE = re.compile(
    r"^(?P<hashes>#{2,3})\s+(?P<kind>[A-Za-z][A-Za-z /-]*?)"
    r"(?:\s+--\s+(?P<name>[^()\n]+?)"
    r"(?:\s+\((?P<role>[^)\n]*)\))?"
    r"(?:\s+--\s+(?P<date>\d{4}-\d{2}-\d{2}))?"
    r"(?:\s+\(round\s+\d+\))?\s*)?$"
)

#: Section kinds whose first token we key transitions on (kept liberal so
#: ``Revised proposal``, ``Plan review``, ``Code review`` all match).
_KNOWN_KINDS = {
    "review", "response", "revised", "decision", "plan", "code",
    # `sharpening` was absent, which is why the scaffold's OWN emitted
    # review block parsed to nothing.  A document of exactly the shape
    # the planner emitted yielded [(2, 'Plan review')] -- the Sharpening
    # heading was discarded, so nothing could pair a raised finding with its
    # disposition.
    "sharpening",
}

# --- the review-pass record schema (S1-S7) -----------------------------------
#
# Parsing only.  Nothing here gates a transition: Chunk B reads the record,
# Chunk C decides on it.  The split is deliberate -- a parser that also gates
# cannot be landed green.

#: The two attestation lines, full-line anchored inside a pass body.
_TIER_LINE_RE = re.compile(r"^\*\*Tier\*\*:\s*(?P<value>.*?)\s*$", re.M)
_FINDINGS_LINE_RE = re.compile(r"^\*\*Findings\*\*:\s*(?P<value>.*?)\s*$", re.M)

#: The closed vocabularies.  Comparison is case-insensitive; these are
#: the canonical spellings.
_TIERS = ("Internal", "External")
_FINDINGS = ("none", "raised")

#: Total order, External > Internal.  `declared >= required` satisfies
#: the floor.  There is no third tier and no `Maintainer` tier: a human review
#: declares External.
_TIER_RANK = {"internal": 1, "external": 2}

#: A Sharpening heading, matched positionally inside a pass body.
_SHARPENING_RE = re.compile(r"^###\s+Sharpening\b", re.M)

#: Step 1 -- the first parenthesised group of the `**Plan review**:` field.
_REQUIRED_TIER_RE = re.compile(r"^required\s*\(([^)]*)\)", re.I)

#: Step 3 -- the first alphabetic word inside that group.
_FIRST_WORD_RE = re.compile(r"^[A-Za-z][A-Za-z-]*")


def _parse_one_field(body: str, pattern: "re.Pattern[str]",
                     vocabulary: Tuple[str, ...], field: str
                     ) -> Tuple[Optional[str], Optional[str]]:
    """Read one attestation line -> ``(canonical_value, violation)``.

    Three fail-closed directions, and **no condition yields a
    silent pass**: absent -> ``missing``, out-of-vocabulary ->
    ``unrecognized``, repeated -> ``duplicate`` *even when the occurrences
    agree*, because agreement is a judgement a conformance backstop must not
    make.  There is no default value for either field.
    """
    found = pattern.findall(body)
    if not found:
        return None, f"missing {field}"
    if len(found) > 1:
        return None, f"duplicate {field}"

    # **Emphasis is presentation, not vocabulary**, and the field NAME already
    # says so: `_code_review_field_re` is emphasis-optional on the label.  The
    # value was not, which made `**Assurance path**: **high-assurance**` -- the
    # documented house form -- refuse.  `_parse_verdict` already strips emphasis
    # for exactly this reason ("the house form in this tree wraps the label AND
    # the value in one bold span ... 30 of the 38 corpus passes"); two parsers in
    # one file disagreeing about one house style is the defect, and a real author
    # tripped it.
    raw = _EMPHASIS_RE.sub("", found[0]).strip()
    for canonical in vocabulary:
        if raw.casefold() == canonical.casefold():
            return canonical, None

    # **A trailing rationale is admitted, guarded in BOTH directions.**  Authors
    # write `high-assurance -- this changes a trust ceremony`, which is useful
    # information; refusing it teaches them to delete the reason rather than to
    # record it.  But truncating at a clause break alone would be *asymmetrically*
    # unsafe: `standard -- actually high-assurance` would read as `standard`,
    # the direction the contract explicitly forbids ("uncertainty resolves to
    # high-assurance").  So the remainder must name no OTHER vocabulary token --
    # the same guard `_parse_verdict` reaches for so `SHIP but actually BLOCK`
    # cannot clear.
    lead = _VALUE_CLAUSE_RE.match(raw).group(0).strip()
    for canonical in vocabulary:
        if lead.casefold() != canonical.casefold():
            continue
        rest = raw[len(lead):].casefold()
        contradicting = [v for v in vocabulary
                         if v.casefold() != canonical.casefold()
                         and v.casefold() in rest]
        if contradicting:
            return None, (
                f"contradictory {field} value: {raw!r} -- reads as "
                f"{canonical!r} but its rationale also names "
                f"{contradicting[0]!r}; state one value and argue for it in prose")
        return canonical, None

    return None, f"unrecognized {field} value: {raw!r}"


def _parse_pass_date(raw: str) -> Tuple[bool, Optional[str]]:
    """The captured date must be a **real** date, not date-shaped.

    ``_HEADER_RE`` matches the *shape* ``\\d{4}-\\d{2}-\\d{2}``, which accepts
    ``2026-99-99``, ``2026-02-30`` and ``0000-00-00``.  ``date.fromisoformat``
    is strict and rejects all three while accepting a real leap date.  A shape
    match whose value does not parse is a violation, never a silent pass --
    and, under the enumerated legacy manifest, never an exemption either.
    """
    if not raw:
        return False, None
    try:
        _dt.date.fromisoformat(raw)
    except ValueError:
        return False, f"malformed date: {raw!r}"
    return True, None


def _strip_emphasis_chars(raw: str) -> str:
    """Delete the Markdown emphasis characters, for tier/obligation comparison.

    **One helper, both sides of the match**, deliberately: the declared clause is
    read out of `**Plan review**: required(A + B)` and the pass's claim out of its
    `**Obligation**:` line, and the two are compared *"after the
    same emphasis and whitespace normalization"*.  Two copies of this three-line
    loop is exactly how one side ends up admitting a spelling the other refuses.
    """
    for ch in "*_`":
        raw = raw.replace(ch, "")
    return raw


def normalize_required_tier(field: str) -> Tuple[Optional[str], Optional[str]]:
    """Normalize the `**Plan review**:` field -> ``(tier, violation)``.

    Defined on the **first parenthesised group only**.  Text after the closing
    paren is ignored (every live plan has some); text after the first word
    *inside* the group is a **lens annotation** -- preserved in the record by
    the caller, ignored by the tier comparison.  Negations fail closed:
    ``required(not External)`` is a violation, not an External requirement.
    """
    m = _REQUIRED_TIER_RE.match(field.strip())
    if not m:
        return None, "tier not declared"
    group = _strip_emphasis_chars(m.group(1))
    word = _FIRST_WORD_RE.match(group.strip())
    if not word:
        return None, "tier not declared"
    tier = word.group(0).casefold()
    if tier not in _TIER_RANK:
        return None, f"unrecognized required tier: {word.group(0)!r}"
    return tier, None


def tier_satisfies(declared: str, required: str) -> bool:
    """``declared >= required`` under the total order External > Internal."""
    return _TIER_RANK.get(declared.casefold(), 0) >= _TIER_RANK.get(
        required.casefold(), 0)


def normalize_required_obligations(
        field: str) -> Tuple[Tuple[Tuple[str, str], ...], Optional[str]]:
    """The DECLARED OBLIGATION CLAUSES of a `**Plan review**:` field.

    ``required(A + B)`` means *"two obligations and two distinct review passes"*.
    Returns ``((clause, required_tier), ...)`` in declaration order, plus one
    violation string or ``None``.

    **This exists because the defect was live and silent.**  Measured at Chunk
    E's parent, `normalize_required_tier('required(**External** + **External
    Security Review**)')` returned ``('external', None)``: the second obligation
    was not merely unenforced, it was *discarded*, so today's tooling reported the
    floor satisfied by a single pass -- which is this module's own declared
    tier, so the rule is exercised by the artifact that states it.

    `normalize_required_tier` is deliberately left alone -- it answers "what is
    the tier CEILING", still resolves to exactly one tier for every live form
    (`test_c6_every_live_required_form_resolves_to_exactly_one_tier` pins that),
    and is a published name.  This function answers the different question "how
    many obligations are declared, and what tier does each name".

    Normalization is *the same* the tier parser uses -- the first parenthesised
    group, emphasis characters deleted -- plus ASCII-whitespace collapsing, so a
    clause wrapped across two source lines still matches the one-line
    ``**Obligation**:`` value a pass copies from it.

    Fail-closed in four directions, none of which yields a silent single
    obligation: no group at all, an empty clause (``required(External + )``), a
    clause naming no recognized tier, and a repeated clause -- two identical
    clauses cannot be told apart, so they cannot be distinctly cleared.
    """
    m = _REQUIRED_TIER_RE.match(field.strip())
    if not m:
        return (), "tier not declared"
    group = _strip_emphasis_chars(m.group(1))
    out: List[Tuple[str, str]] = []
    for raw in group.split("+"):
        clause = _ASCII_WS_RE.sub(" ", raw).strip()
        if not clause:
            return (), ("empty obligation clause in "
                        f"'required({m.group(1).strip()})' -- every '+'-joined "
                        "clause must name a tier")
        word = _FIRST_WORD_RE.match(clause)
        if not word or word.group(0).casefold() not in _TIER_RANK:
            return (), (f"unrecognized required tier in obligation {clause!r} "
                        f"-- the vocabulary is closed ({'/'.join(_TIERS)})")
        out.append((clause, word.group(0).casefold()))
    names = [clause for clause, _tier in out]
    if len(set(names)) != len(names):
        return (), ("duplicate obligation clause in "
                    f"'required({m.group(1).strip()})' -- two identical clauses "
                    "cannot be distinctly cleared; name each obligation once")
    return tuple(out), None


def _detect_kind(path: Path) -> str:
    """``proposal`` or ``plan`` from the path; else a PlannerError."""
    parts = {p.lower() for p in path.parts}
    if "proposals" in parts:
        return "proposal"
    if "plans" in parts:
        return "plan"
    raise PlannerError(
        f"cannot tell whether {path} is a proposal or a plan -- expected it "
        "under dev/proposals/ or dev/plans/."
    )


def _parse_status(text: str) -> str:
    """Best-effort read of the ``**Status**:`` / ``Status:`` line."""
    for line in _split_lines(text)[:60]:
        stripped = line.strip()
        low = stripped.lower()
        if low.startswith("**status**:") or low.startswith("status:"):
            value = stripped.split(":", 1)[1].strip().strip("*").strip()
            # Normalize "accepted -> plan" style annotations to the bare token.
            token = value.split()[0].lower() if value else ""
            return token
    return ""


def _parse_field(text: str, field: str) -> str:
    """Read a ``**<field>**:`` metadata line value (empty if absent)."""
    pat = re.compile(rf"^\s*\*?\*?{re.escape(field)}\*?\*?\s*:\s*(.+?)\s*$",
                     re.IGNORECASE)
    for line in _split_lines(text)[:60]:
        m = pat.match(line)
        if m:
            return m.group(1).strip()
    return ""


def _parse_sections(text: str) -> List[Section]:
    """Parse all ``##``/``###`` headers into Section records, with bodies."""
    lines = _split_lines(text)
    headers: List[Tuple[int, Section]] = []
    for i, line in enumerate(lines):
        m = _HEADER_RE.match(line)
        if not m:
            continue
        kind_raw = (m.group("kind") or "").strip()
        first = kind_raw.split()[0].lower() if kind_raw else ""
        if first not in _KNOWN_KINDS:
            continue
        sec = Section(
            level=len(m.group("hashes")),
            kind=kind_raw,
            name=(m.group("name") or "").strip(),
            role=(m.group("role") or "").strip(),
            date=(m.group("date") or "").strip(),
            line_no=i + 1,
        )
        headers.append((i, sec))
    # Attach bodies (text up to the next header of equal-or-shallower depth).
    for idx, (i, sec) in enumerate(headers):
        end = len(lines)
        for j, nxt in headers[idx + 1:]:
            if nxt.level <= sec.level:
                end = j
                break
        sec.body = "\n".join(lines[i + 1:end])
        sec.has_isolated_blockquote = _has_isolated_blockquote(sec.body)
    return [sec for _i, sec in headers]


def _has_isolated_blockquote(body: str) -> bool:
    """True if `body` contains a visually-isolated ``>`` blockquote.

    Visual isolation = at least one ``>`` line with a blank line (or the
    start of the body) immediately before it, **outside any fenced code
    block** -- a ``>`` inside ```` ``` ````/``~~~`` fences is a shell prompt,
    a diff, or a markdown example, not an authorization quote, and must not
    count.  This is a **structural** check -- presence and isolation --
    never a judgment about whether the quoted text is an authentic
    authorization."""
    in_fence = False
    prev_blank = True  # start-of-body counts as a preceding blank line
    for line in _split_lines(body):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            prev_blank = False
            continue
        if not in_fence and line.lstrip().startswith(">") and stripped != ">":
            if prev_blank:
                return True
        prev_blank = stripped == ""
    return False


def _read_artifact(path: Path) -> Artifact:
    """Read + parse a proposal/plan from disk (read-only)."""
    if not path.is_file():
        raise PlannerError(f"no such artifact: {path}")
    kind = _detect_kind(path)
    text = path.read_text(encoding="utf-8")
    art = Artifact(path, kind, text)
    art.status = _parse_status(text)
    art.author = _parse_field(text, "Author")
    art.plan_review = _parse_field(text, "Plan review")
    art.sections = _parse_sections(text)
    # Markdown emphasis is tolerated around the label.  The repository's own
    # house style writes ``**Dispositions:**``, which the original unbolded-only
    # pattern rejected -- so this precondition reported "no Dispositions block"
    # against 12 archived plans that each carried one, including the plan that
    # introduced the vocabulary.  A precondition that fails a correct record is
    # the same defect class as one that passes an empty one: it is not testing
    # the property it names.
    art.has_disposition_attestation = _has_disposition_attestation(text)
    art.has_fidelity_signoff = _has_fidelity_signoff(text)
    art.has_code_review_marker = _has_code_review_marker(text)
    return art


#: **PUBLIC alias, and the name is load-bearing.**
#:
#: `ASSURANCE_PATHS` was published for exactly this reason; this
#: is the same move for the parser.  The contract requires that *"`scan`, `next`, and
#: accepted closeout tooling consume shared predicates rather than implement
#: three interpretations of readiness"*, and the scan side of that
#: into this file by name (`status_evidence_violations`'s docstring: *"and, when
#: contract is `closeout --dry-run`"*).  `status_evidence_violations`,
#: `review_record_violations`, `blocked_by_violations` and
#: `plan_inheritance_violations` are all already public and all take an
#: `Artifact` -- so without a public way to *build* one, the only routes left to
#: `tools/lifecycle.py` were to reach into a private name or to grow a second
#: artifact parser.  Chunk P6a refused both for the assurance vocabulary and
#: deferred instead; there is no later chunk to defer to here, so the name is
#: published.
#:
#: Deliberately an ALIAS, not a wrapper: a wrapper is a second body that can
#: drift from the one every in-file call site uses.
read_artifact = _read_artifact


#: A ``## Code review`` section counts as *substantive* only if it carries one of
#: the two markers the plan template itself demands of a real reviewer: the
#: ``**Model**:`` identity line, or a dated ``Code review -- <reviewer> --
#: YYYY-MM-DD`` heading.  **Why this exists:** the archive precondition used to be
#: satisfied by the section's mere *presence*, and every plan scaffolded from
#: ``dev/plans/_template.md`` ships that section pre-written as a placeholder
#: ("*Filled in after implementation commits land*") -- so the gate could never
#: fail, and two plans archived on 2026-08-11 with no code review at all while it
#: reported success.  A check that returns success without testing the property it
#: names is worse than no check, because it is silent (``AGENTS.md`` > *Verifying
#: claims*).
#:
#: This tests for a *marker*, not for review quality -- an author who writes the
#: marker without reviewing still passes.  It moves the gate from "impossible to
#: fail" to "requires a deliberate false statement", which is the honest limit of
#: a text scanner; the residual is recorded in ``dev/PLANNING.md``.
#: ALL ``## Code review`` sections are examined, not just the first: a plan may
#: carry a placeholder section and a real reviewer's section further down.
_CODE_REVIEW_SECTION_RE = re.compile(
    r"^## Code review.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)
#: Inline-code spans are **masked before any label search**, preserving offsets.
#: This is the discriminator that separates a real block from prose *discussing*
#: one.  Measured over the 39-plan corpus: masking drops exactly 6 files, and
#: all six carry only backticked mentions -- e.g. `byline-classification.md:990`,
#: "carries the literal `Follow-ups migrated to:` block naming where each
#: deferred...".  A bolded mid-line block survives masking, which is what lets
#: the label search below drop its `^` anchor without re-admitting prose.
_INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


#: The label, emphasis-tolerant and **not** line-anchored.  Dropping `^` is
#: deliberate: `adopter-entry-doc-refresh.md:173` carries a real block as
#: ``Archived 2026-06-12. **Follow-ups migrated to:** `dev/PLANNING.md` > Queued``
#: which the anchored form rejected.
_DISPOSITION_LABEL_RE = re.compile(
    r"[*_]{0,2}\s*(?:Follow-ups migrated to|Dispositions)\s*[*_]{0,2}\s*:")

#: Substance, one of three shapes.  Presence of the label is never enough --
#: that is the defect this predicate exists to close.
_DISPOSITION_ENTRY_RE = re.compile(
    r"->\s*[*_`]{0,2}(?:accept|guard|wontfix|defer)\b", re.IGNORECASE)
_DISPOSITION_NONE_RE = re.compile(
    r"^\s*[*_]{0,2}\s*none\b", re.IGNORECASE | re.MULTILINE)

#: A commit id as the records actually write them, usually backticked.
_COMMIT_ID_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
#: The governing-section reference.  A *shape* test, not a semantic one: every
#: real sign-off in the archive names what it matches against in these terms.
_GOVERNING_REF_RE = re.compile(r"\b(?:accepted|Revised|Decision)\b")
_FIDELITY_PHRASE_RE = re.compile(r"fidelity sign-off|loop-fidelity", re.I)


def _mask_examples(text: str) -> str:
    """Blank inline-code spans, preserving length so offsets still line up.

    **Inline code only -- fenced blocks are NOT masked, and that is measured.**
    Masking fences looks principled (a fence is an illustration) and is wrong
    here: `board-drain-guards.md:1274` and `default-security-stance.md:2568`
    write their *real* disposition records inside a fence to hold the column
    alignment. Masking cost both of them their attestation -- a false fail,
    which this plan's own stop-conditions forbid.

    Documentation therefore illustrates the form with **inline** code
    (``write `Dispositions: none```), which is masked and so cannot be mistaken
    for the record it describes.
    """
    return _INLINE_CODE_RE.sub(
        lambda m: " " * len(m.group(0)), text)


def _lasting_truth_bodies(text: str) -> List[str]:
    """**Every** `## Lasting-truth migration` section body.

    Scoping matters: the old fidelity check searched the **whole file** for the
    phrase, so any plan merely mentioning "loop-fidelity" anywhere satisfied a
    gate that claims the sign-off names an implementing commit.

    All of them, not the first: a plan scaffolded from the template carries the
    empty stub, and the real dated section (``## Lasting-truth migration --
    YYYY-MM-DD``) is *appended below it* under the append-only rule. Reading
    only the first match reports the placeholder and rejects the real sign-off
    -- measured against 5 archived plans, including one written this session.
    """
    return [m.group(1) for m in re.finditer(
        r"^##\s+Lasting-truth migration\b(.*?)(?=^##\s|\Z)",
        text, re.MULTILINE | re.DOTALL)]


def _has_disposition_attestation(text: str) -> bool:
    """True when a disposition block is present **and carries substance**.

    Three accepted shapes: an explicit ``none``; at least one entry naming a
    disposition from the accepted vocabulary; or a legacy
    ``Follow-ups migrated to:`` label with a destination on its own line.
    An empty label refuses -- which is what the previous predicate accepted.
    """
    masked = _mask_examples(text)
    for m in _DISPOSITION_LABEL_RE.finditer(masked):
        tail = masked[m.end():]
        # Bound the search at the next H2 so a later section cannot lend
        # substance to an empty label above it.
        stop = re.search(r"^##\s", tail, re.MULTILINE)
        block = tail[: stop.start()] if stop else tail
        # Substring, not prefix: the label pattern's leading `\s*` absorbs
        # the preceding newlines, so a prefix test never reaches the word.
        legacy = "follow-ups" in m.group(0).lower()
        if legacy:
            # Legacy records predate the disposition vocabulary and write a
            # destination instead: `Follow-ups migrated to: dev/PLANNING.md`,
            # or `* the thing -> dev/PLANNING.md > Queued` on the lines below.
            # Any non-empty body is substance; only a bare label refuses.
            # (Prose *discussing* the phrase never reaches here -- it is
            # backticked, and inline code was masked above.)
            if block.strip():
                return True
        else:
            if _DISPOSITION_ENTRY_RE.search(block) or _DISPOSITION_NONE_RE.search(block):
                return True
    return False


def _has_fidelity_signoff(text: str) -> bool:
    """True when the lasting-truth section carries a real sign-off.

    Requires all three, together, inside that section: the phrase, at least one
    implementing commit id, and a reference identifying what it was matched
    against.  "Loop-fidelity sign-off is owed at archive." satisfies none of
    the last two and refuses.
    """
    for body in _lasting_truth_bodies(text):
        if (_FIDELITY_PHRASE_RE.search(body)
                and _COMMIT_ID_RE.search(body)
                and _GOVERNING_REF_RE.search(body)):
            return True
    return False


_REVIEW_MODEL_RE = re.compile(r"^\*\*Model\*\*:", re.MULTILINE)
_REVIEW_DATED_RE = re.compile(
    r"^#{2,3} Code review\s*--\s*\S+.*\d{4}-\d{2}-\d{2}", re.MULTILINE)


def _has_code_review_marker(text: str) -> bool:
    """True when some ``## Code review`` section carries a reviewer marker.

    **What this can and cannot say.** It attests a *record shape*: a section
    bearing a reviewer identity (``**Model**:``) or a dated
    ``Code review -- <reviewer> -- YYYY-MM-DD`` heading. It does **not** attest
    that a review occurred, that it was substantive, or that its reviewer was
    independent -- a text scanner reaches none of those. That assurance lives in
    ``AGENTS.md``'s rule that reviews are attributed and self-committed, which
    Git authorship enforces. The predicate was previously named
    ``_has_substantive_code_review``, which claimed the thing it cannot check.
    """
    for section in _CODE_REVIEW_SECTION_RE.findall(text):
        if _REVIEW_MODEL_RE.search(section) or _REVIEW_DATED_RE.search(section):
            return True
    return False


# === the ONE runtime status vocabulary =======================================
#
# This module is the **single runtime owner** of the lifecycle status
# vocabulary (`lifecycle-status-vocabulary`, under its accepted
# "contained consumers and corpus boundary" replacement).  It mirrors
# `doctrine/lifecycle-contract.md`, which stays the human contract.
#
# THREE consumers live OUTSIDE this file's package and read the names below by
# loading this file through a contained fixed-path loader -- never through
# ambient `sys.path`, and never by re-declaring a status literal of their own:
#
#   * `tools/_lifecycle_metrics/extract.py` + its installed twin
#     (`templates/modules/default-on/_lifecycle_metrics/extract.py`);
#   * `scripts/transition_lint.py` (repository-only);
#   * `tools/lifecycle.py` + its installed twin
#     (`templates/skills/_lib/lifecycle.py`) -- added by Chunk P6a at `8bf1154`,
#     which copied the loader contract rather than re-deriving it.  Its twin
#     sits under `templates/skills/_lib/` beside this file's own twin, not under
#     `templates/modules/default-on/` like the metrics consumer's; the two
#     consumers ship through different install families, and only the paths
#     differ, not the contract.
#
# `bootstrap/tests/test_lifecycle_vocabulary.py` audits all three consumers'
# source for local status enums and is observed red against a reintroduced one.
# Its `_AUDITED_CONSUMER_SOURCES` is **five paths**, not three: each consumer
# that ships as a twin is audited on BOTH sides, because editing one side and
# not the other is the drift the audit exists to catch.  The count is pinned by
# name in that module's own guard-on-the-guard, so this comment and the audit
# cannot silently disagree about how many consumers there are -- which they did,
# between the third landing and this correction.
#
# Five declarations, each with exactly one job.  Keeping them as *data* is what
# made Chunk E's vocabulary change an edit to these tuples rather than a refactor
# of every consumer -- which is exactly how it landed.
#
# === the accepted next-action vocabulary, now the ONLY one ====================
#
# `lifecycle-status-vocabulary` replaced the flat tokens with next-action
# states.  Chunk E made the new tokens legal *additively*, because three live
# artifacts still declared `executing` / `review` at the time and a hard
# replacement would have redded all three.  **The migration completed the
# replacement on 2026-08-13**: every active artifact was migrated first (blob-
# checked, refusing any row whose blob moved), the authoring templates were
# fixed so newly opened artifacts cannot reintroduce a retired token, and only
# then did the six tokens move into the historical tuples below.
#
# `open` / `executing` / `review` and `proposed` / `reviewed` / `revised` are
# now **historical**: never legal for an active artifact, never a transition
# target, and still recognized everywhere a consumer reads an archived artifact
# or longitudinal history.  Retiring a token removes it from the *current*
# vocabulary; it must never stop a consumer parsing a record that predates the
# migration.  Three consumers depend on exactly that distinction and are
# easy to break silently -- see `_plan_status_enum` in `_lifecycle_metrics`,
# `_PROPOSAL_POST_REVIEW_STATES`, and the two `*_NEXT_OWNERS` tables, each of
# which carries its own note.

#: The CURRENT vocabulary -- the only statuses an *active* artifact may declare.
#: In state-machine order.  Order is not semantic for membership, but
#: `_lifecycle_metrics`' `_normalize_plan_status` resolves a free-text status by
#: the FIRST enum the leading token starts with, so the current and historical
#: groups are kept separate and no current token is a prefix of a historical one
#: (checked: none of the eleven pairs collide).
PROPOSAL_STATES = ("awaiting-review", "revising", "awaiting-decision",
                   "accepted", "rejected", "superseded")
PLAN_STATES = ("awaiting-plan-review", "revising-plan", "ready-to-implement",
               "implementing", "awaiting-code-review", "revising-code",
               "ready-to-archive", "archived")

#: Terminal = no status flip leaves them.  A proposal's `accepted` IS terminal:
#: its archive move is a file operation, not a transition.
PROPOSAL_TERMINAL_STATES = ("accepted", "rejected", "superseded")
PLAN_TERMINAL_STATES = ("archived",)

PROPOSAL_NON_TERMINAL_STATES = tuple(
    s for s in PROPOSAL_STATES if s not in PROPOSAL_TERMINAL_STATES)
PLAN_NON_TERMINAL_STATES = tuple(
    s for s in PLAN_STATES if s not in PLAN_TERMINAL_STATES)

#: Legal next target states, as data.  `""` is the not-yet-created artifact.
#:
#: The proposal cycle, verbatim:
#:     awaiting-review --blocking review--> revising --Response/revision-->
#:     awaiting-review --clearing review--> awaiting-decision
#:     awaiting-decision --Maintainer Decision--> accepted/rejected/superseded
#: plus its explicit return arm: *"If it identifies a contract defect the
#: Maintainer wants corrected before Decision, the Maintainer returns the
#: proposal to `revising`."*
PROPOSAL_TRANSITIONS = {
    "": ("awaiting-review",),
    "awaiting-review": ("revising", "awaiting-decision"),
    "revising": ("awaiting-review",),
    "awaiting-decision": ("accepted", "rejected", "superseded", "revising"),
    "accepted": (),
    "rejected": (),
    "superseded": (),
}

#: The plan cycle, verbatim:
#:     awaiting-plan-review <-> revising-plan
#:               |
#:               v
#:     ready-to-implement -> implementing -> awaiting-code-review
#:                                                |
#:                                                v
#:                                           revising-code
#:                                                |
#:                                                +----> awaiting-code-review
#:
#:     awaiting-code-review -> ready-to-archive -> archived
PLAN_TRANSITIONS = {
    "": ("awaiting-plan-review",),
    "awaiting-plan-review": ("revising-plan", "ready-to-implement"),
    "revising-plan": ("awaiting-plan-review",),
    "ready-to-implement": ("implementing",),
    "implementing": ("awaiting-code-review",),
    "awaiting-code-review": ("revising-code", "ready-to-archive"),
    "revising-code": ("awaiting-code-review",),
    "ready-to-archive": ("archived",),
    "archived": (),
}

#: The statuses whose legal set depends on the artifact's own declaration rather
#: than on the state machine: a `not required(...)` plan skips the review wait.
#: Isolated and named so the conditionals are entries, not branches in a table.
#:
#: `""` is the *"Plan review is cleared, inherited, or not required"* opening,
#: plus the accepted fast path: *"the plan-open commit may record `implementing`
#: directly; it must contain the implementation evidence that makes the skipped
#: `ready-to-implement` state true."*  The fast path is offered ONLY here --
#: never from `awaiting-plan-review` -- because a plan that declares
#: `required(...)` and has not cleared it is exactly the refusal case.
PLAN_TRANSITIONS_REVIEW_NOT_REQUIRED = {
    "": ("ready-to-implement", "implementing"),
}

#: Historical tokens -- admitted ONLY for archived-artifact compatibility and
#: longitudinal metrics.  **Never** legal for an active artifact and never a
#: transition target: *"After migration, old non-terminal values are
#: invalid directly under active proposal and plan directories."*
#:
#: **Populated on 2026-08-13**, in the same change that migrated the
#: last active artifact off them -- the ordering matters in both directions.
#: Listing a token here while a live artifact declares it makes the planner
#: contradict the tree it scans; leaving it out of here after migration makes
#: every consumer that reads history call an archived artifact malformed.
#:
#: **These are not decoration -- three consumers read them and break silently
#: without them.** `_lifecycle_metrics._plan_status_enum` resolves a free-text
#: historical status by prefix and would regress `reviewed; ...` from `review`
#: to `reviewed`; `_conformance_violations` would report `unknown proposal
#: status` for an archived proposal; and `next_owner` would answer `unknown` for
#: a row the board can still render.  Membership here is what keeps a *retired*
#: token distinct from an *unrecognized* one.
HISTORICAL_PROPOSAL_STATES: Tuple[str, ...] = ("proposed", "reviewed", "revised")
HISTORICAL_PLAN_STATES: Tuple[str, ...] = ("open", "executing", "review")

#: The *opening* statuses -- an artifact still at or before its review floor.
#: `transition_lint`'s shape (b) asks whether an ADDED lifecycle file already
#: carried a landed review, which is only meaningful pre-review.
#:
#: `awaiting-review` and `awaiting-plan-review` are the accepted vocabulary's two
#: initial states; `proposed` and `open` are their
#: retired predecessors and stay listed for exactly the reason the filter below
#: exists -- the migration moved them into the historical tuples, and they must remain
#: shape-(b) eligible for the old commits that added files declaring them.
OPENING_STATES = ("awaiting-review", "awaiting-plan-review", "proposed", "open")

#: The added-artifact status set shape (b) consumes: every recognized current
#: non-terminal state, plus the historical opening states old commits need.
#:
#: Widened from `OPENING_STATES` alone (3 tokens) to every current non-terminal
#: state (7 originally, **16** once the accepted vocabulary became legal)
#: per the accepted replacement, then **16 -> 12 at the migration** as `reviewed`,
#: `revised`, `executing` and `review` stopped being *current* non-terminal
#: states.  `proposed` and `open` re-enter through the filter below.
#:
#: **The filter stays at historical OPENING statuses rather than all
#: historical tokens, and that is the accepted text, not a convenience**:
#: *"every recognized current non-terminal status plus the historical opening
#: statuses"*.  Widening it to all six would have held the set at 16 and made
#: the narrowing trivially corpus-neutral, but it would also have contradicted
#: the accepted contract, so the measurement was run instead of avoided.
#:
#: The narrowing is corpus-neutral **by measurement, not by argument**: every
#: added lifecycle file in both pinned windows declares `proposed`, `open` or
#: `awaiting-plan-review`, all of which survive here, so no shape-(b) finding
#: disappears.  A status that is recognized but outside this set takes a silent
#: `continue` in `_shape_b` -- never the `b?` advisory, which is reserved for
#: genuinely unrecognized tokens.  `test_transition_lint.py`'s corpus
#: expectations remain the witness, not this comment: if they ever move, that is
#: a finding to report, never a number to update.
SHAPE_B_STATUSES = tuple(dict.fromkeys(
    PROPOSAL_NON_TERMINAL_STATES
    + PLAN_NON_TERMINAL_STATES
    + tuple(s for s in OPENING_STATES
            if s in HISTORICAL_PROPOSAL_STATES + HISTORICAL_PLAN_STATES)
))

#: Every status any consumer may *recognize* without raising an advisory
#: malformed-status finding.  Unknown is not safe silence.
RECOGNIZED_STATES = tuple(dict.fromkeys(
    PROPOSAL_STATES + PLAN_STATES
    + HISTORICAL_PROPOSAL_STATES + HISTORICAL_PLAN_STATES
))

# === Chunk F: the `Next owner` column, as central data =======================
#
# The proposal and plan cycles each declare a `Next owner` per status, and the board's
# `owner` field to come from *"the central lifecycle vocabulary"*.  Nothing here
# read that column before, so the board would otherwise have had to carry a
# consumer-local role table -- the exact thing forbidden (*"contains no
# consumer-local status, role, tier, verdict, or closeout vocabulary"*).  It
# lives beside the state tuples for the same reason those are data: adding a
# state and forgetting its owner is then one missing dict key, not a silent
# fallback.
#
# **One spelling, not two.**  The tokens below are hyphenated rather than the cycles'
# prose ("independent proposal reviewer"), because the compact row and the JSON
# contract must carry the *same* value -- JSON carries "full field values" of
# the same projection, and two spellings of one vocabulary is the drift the
# single-source rule exists to prevent.  Each entry names its source phrase.
NEXT_OWNER_TERMINAL = "terminal"

#: A status whose only reading is a PENDING-RETIREMENT legacy token that
#: maps to **more than one** successor state, so its next owner is genuinely
#: not derivable.  Naming that is honest; picking one of the candidates would be
#: the board guessing, which is forbidden for `status` and no better here.
NEXT_OWNER_UNRESOLVED = "unresolved"

#: No `**Status**:` line, or a token outside `RECOGNIZED_STATES`.
NEXT_OWNER_UNKNOWN = "unknown"

PROPOSAL_NEXT_OWNERS = {
    "awaiting-review": "proposal-reviewer",   # independent proposal reviewer
    "revising": "proposal-author",            # proposal author
    "awaiting-decision": "maintainer",        # Human Maintainer
    "accepted": NEXT_OWNER_TERMINAL,
    "rejected": NEXT_OWNER_TERMINAL,
    "superseded": NEXT_OWNER_TERMINAL,
    # HISTORICAL (retired) -- RETAINED DELIBERATELY, and the reason is the
    # ACTIVE artifact, not the archived one.  Review falsified an
    # earlier version of this note: measured over the real corpus, ZERO archived
    # artifacts declare a historical token (40 archived plans are `archived`; 54
    # archived proposals `accepted`, 4 `superseded`), and `next_owner`'s only
    # call site is the board row builder, which reads direct children and never
    # the archive tree -- so no archived artifact can reach this table at all.
    #
    # The reachable reason: an artifact that is still ACTIVE and still declares
    # a retired token -- mid-migration, or hand-authored from an old copy -- is
    # exactly the case the board must stay useful for.  With these rows it
    # renders `proposal-reviewer` / `implementation` and the operator can act;
    # without them `next_owner` answers `unknown` and the board's whole point, saying
    # whose move it is, degrades precisely when someone needs telling.
    #
    # `proposed` had one successor (`awaiting-review`); `reviewed` mapped to
    # `revising|awaiting-decision` and `revised` to
    # `awaiting-review|awaiting-decision`, whose owners differ, so those two
    # report `unresolved` rather than guess.
    #
    # `TestOwnerVocabulary`'s general coverage iterates the CURRENT tuples and
    # no longer visits these rows, so they carry their own node --
    # `test_the_retained_historical_owner_rows_are_not_dead_weight`.
    "proposed": "proposal-reviewer",
    "reviewed": NEXT_OWNER_UNRESOLVED,
    "revised": NEXT_OWNER_UNRESOLVED,
}

PLAN_NEXT_OWNERS = {
    "awaiting-plan-review": "plan-reviewer",   # required plan reviewer
    "revising-plan": "plan-author",            # plan author
    "ready-to-implement": "implementation",    # Implementation
    "implementing": "implementation",          # Implementation
    "awaiting-code-review": "code-reviewer",   # independent code reviewer
    "revising-code": "implementation",         # Implementation
    "ready-to-archive": "implementation",      # Implementation
    "archived": NEXT_OWNER_TERMINAL,
    # HISTORICAL (retired) -- RETAINED DELIBERATELY, same reason as the
    # proposal table above: the reachable case is an ACTIVE
    # plan still declaring a retired token, NOT an archived one.  No archived
    # plan declares one (measured: all 40 are `archived`), and the archive tree
    # is not reachable from `next_owner`'s only call site.
    #
    # `open` -> `awaiting-plan-review` and `executing` -> `implementing` were
    # each one successor; `review` mapped to three
    # (`awaiting-code-review|revising-code|ready-to-archive`) whose owners are
    # not the same, so it reports `unresolved` rather than guess.
    "open": "plan-reviewer",
    "executing": "implementation",
    "review": NEXT_OWNER_UNRESOLVED,
}

#: The closed owner vocabulary -- what `board --owner` accepts and what any row
#: may carry.  Derived from the two tables so a new entry cannot be filterable
#: in one place and unknown in the other.
NEXT_OWNERS = tuple(dict.fromkeys(
    tuple(PROPOSAL_NEXT_OWNERS.values()) + tuple(PLAN_NEXT_OWNERS.values())
    + (NEXT_OWNER_UNKNOWN,)
))


def next_owner(kind: str, status: str) -> str:
    """The declared `Next owner` for one artifact kind + status.

    Fail-closed: an absent or unrecognized status is `unknown`, never the owner
    of some neighbouring state.  A recognized status missing from its table is
    also `unknown` -- that is a real gap in this file, and reporting it as a
    plausible owner would hide it.
    """
    table = PROPOSAL_NEXT_OWNERS if kind == "proposal" else PLAN_NEXT_OWNERS
    return table.get(status, NEXT_OWNER_UNKNOWN)


# Internal aliases, retained so this module's own call sites are unchanged.
_PROPOSAL_STATES = PROPOSAL_STATES
_PLAN_STATES = PLAN_STATES


def _legal_transitions(art: Artifact) -> List[str]:
    """The legal next target states from the artifact's current status."""
    s = art.status
    if art.kind == "proposal":
        return list(PROPOSAL_TRANSITIONS.get(s, ()))
    if not art.plan_review.lower().startswith("required"):
        override = PLAN_TRANSITIONS_REVIEW_NOT_REQUIRED.get(s)
        if override is not None:
            return list(override)
    return list(PLAN_TRANSITIONS.get(s, ()))


def _reviewers(art: Artifact) -> List[Section]:
    """Review-bearing sections (proposal ``Review``; plan ``Plan/Code review``)."""
    out = []
    for sec in art.sections:
        first = sec.kind.split()[0].lower() if sec.kind else ""
        if art.kind == "proposal" and first == "review":
            out.append(sec)
        elif art.kind == "plan" and (
            sec.kind.lower().startswith("plan review")
            or sec.kind.lower().startswith("code review")
        ):
            out.append(sec)
    return out


def _decisions(art: Artifact) -> List[Section]:
    return [s for s in art.sections if s.kind.split()[0:1] == ["Decision"]]


def _has_kind(art: Artifact, prefix: str) -> bool:
    return any(s.kind.lower().startswith(prefix.lower()) for s in art.sections)


#: The legacy population, ENUMERATED.  ``stem -> {heading digest: n}``.
#: Generated by ``scripts/gen_legacy_passes.py``; do not hand-edit.  A pass is
#: legacy iff its stem is here and it is the k-th occurrence of that digest with
#: ``k <= n``.  Occurrence *counts* close the duplicate-append hole: re-appending
#: a heading byte-identical to an admitted one is occurrence ``n + 1`` and is not
#: admitted.  A dated cutoff was the earlier design and was refused on review --
#: the date lives in the heading, which is text inside the artifact the gate
#: judges, so a smaller number bought a permanent exemption.
_LEGACY_PASSES: Dict[str, Dict[str, int]] = {
    "adopter-licensing-compliance": {"bb271ae22a28bfb6": 1},
    "agent-context-scrub": {"1e2359f6aa2ef3e2": 1},
    "api-web-security-modules": {"01bf85bb1d9a5d18": 1, "813c6e7adc2ea5c7": 1, "9dbdc92cd75b9c62": 1},
    "ast-known-new-repin": {"5f0d8dc934a8182f": 1},
    "byline-classification": {"1e2359f6aa2ef3e2": 1},
    "content-scan-detectors": {"01bf85bb1d9a5d18": 1, "813c6e7adc2ea5c7": 1, "9dbdc92cd75b9c62": 1},
    "default-security-stance": {"01bf85bb1d9a5d18": 1, "813c6e7adc2ea5c7": 1, "9dbdc92cd75b9c62": 1},
    "dependency-advisory-coverage": {"813c6e7adc2ea5c7": 1, "9dbdc92cd75b9c62": 1},
    "first-session-survivability": {"bb271ae22a28bfb6": 1},
    "fork-advisory-semantics": {"1e2359f6aa2ef3e2": 1},
    "gate-claims-vs-enforcement": {"e008594fcf7799a3": 1},
    "gate-reanchor-preflight": {"385181ef1bafc259": 1, "e008594fcf7799a3": 1},
    "interpreter-trust-root-fallback": {"5f0d8dc934a8182f": 1, "97b0881c99b62ce0": 1},
    "lockfile-provenance-fields": {"5f0d8dc934a8182f": 1, "97b0881c99b62ce0": 1, "b174014fd666ade4": 1, "fcfcab56046bef61": 1},
    "planner-line-semantics": {"d2ace8bfee5d936c": 1, "e008594fcf7799a3": 1},
    "portable-security-sweeps": {"01bf85bb1d9a5d18": 1, "813c6e7adc2ea5c7": 1, "9dbdc92cd75b9c62": 1},
    "profile-parse-fail-open": {"1e2359f6aa2ef3e2": 1},
    "record-corrections": {"bb271ae22a28bfb6": 1},
    "release-authenticity": {"1e2359f6aa2ef3e2": 1},
    "release-security-bar": {"01bf85bb1d9a5d18": 2, "9dbdc92cd75b9c62": 1},
    "release-security-orchestration": {"0cbae87e9ca7d20d": 1},
    "review-gate-enforcement": {"01bf85bb1d9a5d18": 2, "26f5c121f879971d": 1},
    "review-record-integrity": {"7e9a4f87e3290f60": 1},
    "scan-coverage": {"1e2359f6aa2ef3e2": 1},
    "security-preflight-checklist": {"9dbdc92cd75b9c62": 1},
    "security-verification-activation": {"01bf85bb1d9a5d18": 1, "813c6e7adc2ea5c7": 1, "9dbdc92cd75b9c62": 1},
    "separator-detection": {"01bf85bb1d9a5d18": 1, "813c6e7adc2ea5c7": 1, "9dbdc92cd75b9c62": 1},
    "solo-legacy-adopter-path": {"5f0d8dc934a8182f": 1},
    "stage-commit-patterns": {"9dbdc92cd75b9c62": 1},
    "transition-lint": {"e008594fcf7799a3": 1},
    "verification-evidence-boundaries": {"0cbae87e9ca7d20d": 1, "1540b27f70d3c240": 1},
}


#: The exact raw-heading grammar the review-pass record schema
#: defines.  Authored independently of ``scripts/gen_legacy_passes.py``'s own
#: ``_PASS_RE`` -- the two must never become each other's oracle, even
#: though both implement the same published grammar and therefore read
#: alike.
#:
#: The earlier ``_pass_headings`` selected *Sections* the older,
#: more permissive ``_HEADER_RE`` had already accepted, and never checked the
#: raw line against the grammar itself.  ``_HEADER_RE`` is a strict superset of this
#: shape -- it tolerates arbitrary whitespace after ``##``, around ``--``,
#: and before end-of-line -- so three shapes that must NOT be passes cleared
#: the gate anyway: extra spaces after ``##``, doubled ``--`` separators, and
#: trailing spaces after the date. The inverse also reproduced: a reviewer
#: field containing literal parentheses (``Jane (Lab) Smith``) matches the grammar's
#: permissive ``[^\n]+?`` reviewer group, but ``_HEADER_RE``'s
#: ``(?P<role>[^)\n]*)`` machinery cannot parse the line at all, so
#: ``_parse_sections`` produced no Section for it and a conforming pass was
#: silently invisible. This regex is now the sole authority on what counts.
_S1_PASS_RE = re.compile(
    r"^## Plan review -- (?P<reviewer>[^\n]+?) -- "
    r"(?P<date>\d{4}-\d{2}-\d{2})(?: \(round (?P<round>\d+)\))?$"
)


def _pass_body(lines: List[str], line_no: int, boundaries: List[int]) -> str:
    """The body of the pass whose heading is at *line_no*.

    **One ordered boundary set, used for every pass body of either record
    kind.**  A boundary is a level-<=2 Section *or* a raw S1-conforming pass
    line, so a pass heading the looser ``_HEADER_RE`` could not parse still
    terminates the pass above it.

    Why this is not merely tidier: before this, only *synthesized* sections were
    sliced this way, and a recognized pass kept the body ``_parse_sections``
    gave it.  ``_parse_sections`` knows nothing about raw pass lines, so a later
    unparseable pass heading -- a reviewer field with parentheses outside the
    ``(<role>)`` position is enough -- was invisible to it.  The earlier pass's
    body then ran straight through the later heading and **swallowed its
    ``**Tier**`` and ``**Findings**`` lines**, which surfaced as *the earlier
    pass* carrying "duplicate Tier" / "duplicate Findings".  Reproduced before
    the fix; pinned by
    ``test_lifecycle_contract.py``'s later-pass-body mutation.

    This can only ever *narrow* a body, never widen one: the boundary set is a
    superset of the section boundaries ``_parse_sections`` already used, so the
    computed end is always at or before the previous one.  That monotonicity is
    what makes applying it to already-recognized sections safe.

    The ceiling half falls out of the same set rather than needing its own
    rule: since ``286f07d`` the only surviving positional ceiling is
    ``### Sharpening``, which is scoped to a pass *body* -- so a correct body is
    a correct ceiling.
    """
    end = len(lines)
    for b in boundaries:
        if b > line_no:
            end = b - 1
            break
    return "\n".join(lines[line_no:end])


def _synthesize_pass_section(lines: List[str], line_no: int,
                             m: "re.Match[str]",
                             boundaries: List[int]) -> Section:
    """A Section for a pass line ``_HEADER_RE`` could not parse.

    Only reached when a raw line matches `_S1_PASS_RE` but has no entry in
    ``art.sections`` -- e.g. a reviewer field carrying literal parentheses
    outside the ``(<role>)`` position, which ``_HEADER_RE`` rejects outright.
    The body comes from :func:`_pass_body`, the single boundary rule every pass
    now shares.
    """
    body = _pass_body(lines, line_no, boundaries)
    sec = Section(level=2, kind="Plan review", name=m.group("reviewer"),
                 role="", date=m.group("date"), line_no=line_no)
    sec.body = body
    sec.has_isolated_blockquote = _has_isolated_blockquote(body)
    return sec


def _pass_headings(art: Artifact) -> List[Tuple[Section, str]]:
    """Every S1-conforming pass in `art`, paired with its heading digest.

    Matches the **raw heading line** against `_S1_PASS_RE` directly --
    never derives a pass from a Section the looser `_HEADER_RE` happened to
    produce. Most S1-conforming lines already have a Section (`_HEADER_RE`
    is a superset of that shape), and that Section is reused so its
    precomputed body stays identical to every other parsed section's. A raw
    line that matches the grammar but that `_HEADER_RE` could not parse at all gets a
    Section synthesized by `_synthesize_pass_section`, so it is not silently
    dropped.

    The digest is taken from the **raw heading line** itself, read directly
    off the file -- never from a heading *rebuilt* out of parsed fields.
    That distinction is load-bearing and was found by a falsifier rather
    than by reading: ``_HEADER_RE`` captures ``name`` and ``role``
    separately, so rebuilding ``f"## Plan review -- {name} -- {date}"``
    silently drops the ``(<role>)`` parenthetical.  For a real heading like

        ## Plan review -- Reviewer A (External, security lens) -- 2026-08-03

    the rebuilt string differs from the line the generator hashed, so **every**
    digest comparison missed and the legacy enumeration was inert -- it would
    have refused all 55 admitted passes while appearing to admit them.  The
    generator hashes the line; the gate must hash the same line.
    """
    lines = art.text.split("\n")
    by_line = {sec.line_no: sec for sec in art.sections}
    matches: List[Tuple[int, str, "Optional[re.Match[str]]"]] = [
        (i + 1, raw, _S1_PASS_RE.match(raw)) for i, raw in enumerate(lines)
    ]
    # ONE canonical boundary set, of BOTH record kinds.  Defined below
    # with the Code-review schema (Chunk C) because it needs that block's
    # heading grammar; resolved at call time, so the reading order is the only
    # thing that differs from defining it here.
    boundaries = _record_boundaries(art)
    out: List[Tuple[Section, str]] = []
    for line_no, raw, m in matches:
        if not m:
            continue
        sec = by_line.get(line_no)
        if sec is None:
            sec = _synthesize_pass_section(lines, line_no, m, boundaries)
        else:
            body = _pass_body(lines, line_no, boundaries)
            if body != sec.body:
                # A recognized pass gets the SAME boundary rule as a
                # synthesized one.  Re-sliced into a **copy** -- `art.sections`
                # is shared with every other consumer (`_has_disposition`,
                # `_reviewers`, the Decision predicates), and narrowing a body
                # in place would silently change what they see for reasons none
                # of them asked about.  Only the pass view is corrected here.
                resliced = Section(level=sec.level, kind=sec.kind,
                                   name=sec.name, role=sec.role,
                                   date=sec.date, line_no=sec.line_no)
                resliced.body = body
                resliced.has_isolated_blockquote = _has_isolated_blockquote(body)
                sec = resliced
        out.append((sec, hashlib.sha256(
            raw.encode("utf-8")).hexdigest()[:16]))
    return out


def _has_disposition(art: Artifact, pass_sec: Section) -> bool:
    """Does a disposition follow `pass_sec`, in either house form?

    Cairn disposition sections come in two shapes and the tree uses **both**,
    measured `as_of` 2026-08-05 across ``dev/plans`` + ``dev/plans/archive``:
    **28** ``## Response to plan review`` against **25** ``### Sharpening``.
    Neither is the convention.  A gate that accepted only one would redden
    roughly half the existing dispositions while enforcing a house style the
    project does not actually hold, so this accepts either:

    * a ``### Sharpening`` **inside this pass's own body**, or
    * a ``## Response to plan review`` section positioned **anywhere after this
      pass**.

    The second form is the **group rule**: one Response dispositions every pass
    above it and after the previous Response.  Because the *first* Response
    after a pass is by definition the one with no other Response in between,
    "some Response exists later" and "the Response closing this pass's group"
    are the same predicate, so the rule needs no new field or syntax.

    This replaces an earlier next-pass ceiling.  That ceiling made a routine and
    unavoidable shape permanently non-conforming: when two review obligations
    are answered in one Response -- the normal case for a plan declaring
    ``required(A + B)`` -- the first pass of every pair is overtaken by the
    second before the Response lands, and append-only forbids inserting a
    disposition between two landed reviews.  The artifact could then never
    conform, with no author action able to fix it.

    The property survives, because it was about a *neighbouring round's*
    disposition standing in for this one: a ``### Sharpening`` is still scoped
    to its own pass's body and never reaches a sibling, and a pass with **no**
    Response after it at all is still unsatisfied.  What is now allowed is the
    author saying, in one section, "these are answered" -- which is what the
    section already meant.

    The documented second house form is specifically
    ``## Response to plan review``, but the earlier check matched any kind
    whose text merely *started with* ``response`` -- so an unrelated
    ``## Response -- Author -- date`` or ``## Response to proposal review --
    Author -- date`` cleared a raised finding it never addressed. The kind
    comparison below is exact (case-insensitive), never a prefix.
    """
    if _SHARPENING_RE.search(pass_sec.body):
        return True
    # The group rule.  Exactness is retained: the kind comparison is
    # exact (case-insensitive), never a prefix, so `## Response -- ...` and
    # `## Response to proposal review -- ...` still do not discharge it.
    return any(
        sec.level == 2
        and sec.kind.strip().lower() == "response to plan review"
        and sec.line_no > pass_sec.line_no
        for sec in art.sections
    )


# === Code-review disposition -- exact `Answers:` binding =====================
#
# **The two record types take deliberately OPPOSITE rules, and that is the
# point of splitting the two predicates.**
#
#   * a *Plan* review is answered as a **round**, so one Response dispositions
#     the whole group of passes above it (the group rule landed at `286f07d`,
#     preserved verbatim above);
#   * a *Code* review's findings are answered **individually**, so each Response
#     must name exactly which pass it answers.
#
# Collapsing these into one generic "a disposition after the later pass may
# satisfy the earlier" assertion is what produced the contradiction the plan's
# Chunk B records: an implementer following the collapsed sentence would have
# restored the false ceiling the Maintainer had just directed away.  So the two
# predicates are separate functions with separate tests, and the contract requires a
# falsifier in each direction so neither can be weakened *into* the other
# unnoticed.
#
# Contract: accepted `code-review-blindness`, its exact-grammar clause
# (replacing the earlier ordering and binding clauses) as sharpened by that
# proposal's Revision 3 -- the binding must resolve to **exactly one** prior raw
# heading; zero or multiple matches refuse.

#: A conforming Code-review pass heading, matched against the **raw line**.
_CODE_REVIEW_PASS_RE = re.compile(
    r"^## Code review -- (?P<reviewer>[^\n]+?) -- "
    r"(?P<date>\d{4}-\d{2}-\d{2})(?: \(round (?P<round>\d+)\))?$")

#: A Response that carries a binding.
_RESPONSE_TO_CODE_REVIEW_RE = re.compile(
    r"^## Response to code review -- (?P<author>[^\n]+?) -- "
    r"(?P<date>\d{4}-\d{2}-\d{2})(?: \(round (?P<round>\d+)\))?$")

#: **One full-line anchored field**.  Anchored on purpose -- an
#: ``Answers:`` appearing mid-sentence in prose is not a field, and treating it
#: as one would let a Response discharge a pass by talking about answering it.
_ANSWERS_LINE_RE = re.compile(r"^Answers:[ \t]*(?P<value>\S.*?)[ \t]*$", re.M)

#: The binding value's own shape.  Checked separately from matching so a
#: malformed value refuses **as malformed** rather than silently failing to match
#: any heading -- the two are different defects and the second reads as "the
#: reviewer never existed", which sends a reader looking in the wrong place.
_ANSWERS_VALUE_RE = re.compile(
    r"^(?P<reviewer>.+?) -- (?P<date>\d{4}-\d{2}-\d{2})"
    r"(?: \(round (?P<round>\d+)\))?$")


def _code_review_pass_lines(art: Artifact) -> List[Tuple[int, str, str, Optional[str]]]:
    """``(line_no, reviewer, date, round_or_None)`` per conforming pass heading.

    Read off the **raw lines**, for the same reason `_pass_headings` does it:
    a heading rebuilt from parsed fields silently drops a ``(<role>)``
    parenthetical, and every comparison against it then misses.
    """
    out: List[Tuple[int, str, str, Optional[str]]] = []
    for i, raw in enumerate(art.text.split("\n")):
        m = _CODE_REVIEW_PASS_RE.match(raw)
        if m:
            out.append((i + 1, m.group("reviewer"), m.group("date"),
                        m.group("round")))
    return out


def _response_to_code_review_lines(art: Artifact) -> List[Tuple[int, int]]:
    """``(line_no, end_line)`` per Response-to-code-review section.

    Bounded by the next level-<=2 heading, which is the same boundary rule
    unified for pass bodies -- so a Response cannot reach into the section below
    it to find a binding it does not carry.
    """
    lines = art.text.split("\n")
    starts = [i + 1 for i, raw in enumerate(lines)
              if _RESPONSE_TO_CODE_REVIEW_RE.match(raw)]
    h2 = sorted({i + 1 for i, raw in enumerate(lines)
                 if raw.startswith("## ") or raw.startswith("# ")})
    out: List[Tuple[int, int]] = []
    for start in starts:
        end = len(lines)
        for b in h2:
            if b > start:
                end = b - 1
                break
        out.append((start, end))
    return out


def code_review_binding_violations(
        art: Artifact,
        skip_lines: Optional[Set[int]] = None) -> List[str]:
    """Every ``Answers:`` binding defect in *art*.

    Six refusal directions, each named separately in the message so a reader is
    sent to the right place: **missing**, **duplicate**, **malformed**,
    **unmatched**, **ambiguous**, and **precedes its target**.  The grammar lists the
    first four; Revision 3 adds *ambiguous* by requiring exactly one match; the
    last is *"A Response positioned before its target refuses"*.

    *skip_lines* (Chunk C) names Response headings admitted by
    `_LEGACY_CODE_REVIEW_RECORDS`.  The ``Answers:`` field is **newer than every
    Response in this tree** -- 2 exist corpus-wide and neither carries it -- so
    without the exemption the gate reddens on a real archived record the moment
    The accepted blast radius says *"no existing artifact
    violates"*.  Default `None` keeps the signature callable, which is how
    the forward contract is expressed: a Response written after the baseline has
    no exemption to pass.
    """
    lines = art.text.split("\n")
    passes = _code_review_pass_lines(art)
    exempt = skip_lines or set()
    v: List[str] = []
    for start, end in _response_to_code_review_lines(art):
        if start in exempt:
            continue
        label = f"'{lines[start - 1].lstrip('# ').strip()}'"
        body = "\n".join(lines[start:end])
        found = _ANSWERS_LINE_RE.findall(body)
        if not found:
            v.append(f"{label}: missing 'Answers:' binding -- a Code-review "
                     "Response must name the exact pass it answers")
            continue
        if len(found) > 1:
            v.append(f"{label}: duplicate 'Answers:' binding "
                     f"({len(found)} lines) -- exactly one is required")
            continue
        value = found[0]
        m = _ANSWERS_VALUE_RE.match(value)
        if not m:
            v.append(f"{label}: malformed 'Answers:' value {value!r} -- "
                     "expected '<reviewer> -- <YYYY-MM-DD>[ (round N)]'")
            continue
        # `(round N)` omitted iff the target omits it: a value carrying no round
        # matches only unnumbered passes, and vice versa.  Anything looser would
        # let one Response bind to a pass it does not name.
        targets = [
            ln for ln, reviewer, date, rnd in passes
            if reviewer == m.group("reviewer")
            and date == m.group("date")
            and rnd == m.group("round")
        ]
        if not targets:
            v.append(f"{label}: 'Answers: {value}' matches no Code-review pass "
                     "in this artifact")
            continue
        if len(targets) > 1:
            v.append(f"{label}: 'Answers: {value}' is ambiguous -- it matches "
                     f"{len(targets)} Code-review passes (lines "
                     f"{', '.join(str(t) for t in targets)})")
            continue
        if targets[0] > start:
            v.append(f"{label}: 'Answers: {value}' targets a pass at line "
                     f"{targets[0]}, which is AFTER this Response at line "
                     f"{start} -- a Response cannot answer a later pass")
    return v


def code_review_pass_is_dispositioned(art: Artifact, pass_line: int) -> bool:
    """Is the Code-review pass at *pass_line* answered by an exact binding?

    **Not** the plan-review group rule: a Response bound to a *later* pass never
    satisfies an earlier one, which is the asymmetry pinned in both directions.
    A Response with any binding defect dispositions nothing -- refusing is the
    fail-closed direction, since the alternative is a malformed binding clearing
    a pass it may not even name.
    """
    if code_review_binding_violations(art):
        return False
    lines = art.text.split("\n")
    passes = _code_review_pass_lines(art)
    for start, end in _response_to_code_review_lines(art):
        found = _ANSWERS_LINE_RE.findall("\n".join(lines[start:end]))
        if len(found) != 1:
            continue
        m = _ANSWERS_VALUE_RE.match(found[0])
        if not m:
            continue
        for ln, reviewer, date, rnd in passes:
            if (ln == pass_line and reviewer == m.group("reviewer")
                    and date == m.group("date") and rnd == m.group("round")
                    and ln < start):
                return True
    return False


# === Chunk C: the Code-review record schema ==================================
#
# Contract: accepted proposal `2026-08-10-claude-code-review-blindness`, whose
# **The original archive clause is superseded**.  The operative clauses are:
#
#   * the archive rule -- the latest applicable pass must CLEAR.  There is
#         no disposition branch: a Response records the implementer's answer and
#         does not clear archive; eligibility comes from a later independent
#         pass.  (Letting an author's own Response convert `REVISE`
#         into archive eligibility would weaken the accepted parent's
#         correction-review boundary, which this amendment exists to *supply*.)
#   * the exact grammar -- document-order recency, the `(round N)` rules,
#         and the full-line `Answers:` binding (implemented above).
#   * legacy, keyed non-replayably -- digest + occurrence count, pinned to
#         one named baseline commit.
#   * one predicate, evaluating an explicit EFFECTIVE STATE, reached by both
#         callers regardless of whether Plan review was required.
#
# **Why the effective state and not the status.**  Review executed the bypass:
# `review_record_violations` sat behind `requires_review`, so a plan declaring
# `Plan review: not required(doc-only)` never reached it, and deleting the weak
# `_has_kind` presence check would have made such a plan archive *clean* instead
# of replacing the weak check with the strong one -- "the same governing failure
# the proposal exists to close, reached through a common legitimate plan
# declaration."  So the Code-review half is keyed on the effective state alone,
# and only the Plan-review half consults the declaration.

#: The effective states at which the Code-review record is evaluated.
#: `scan` supplies the current status; `next`/closeout supplies the requested
#: target.  `ready-to-archive` is named here **before** it exists in
#: `PLAN_STATES`: the accepted status-vocabulary change introduces it, and the predicate
#: names both tokens, so wiring it now makes that change a data edit rather than
#: a second search for every archive-effective branch.
CODE_REVIEW_EFFECTIVE_STATES = ("ready-to-archive", "archived")

#: The closed verdict vocabulary, two classes.  Chosen to cover what this
#: tree already writes rather than to impose a new dialect: every value below
#: appears in `dev/plans/`'s real Code-review sections.
CODE_REVIEW_CLEARING_VERDICTS = ("SHIP", "Accept", "Accept-with-followups",
                                 "PASS")
CODE_REVIEW_BLOCKING_VERDICTS = ("REVISE", "Request changes", "BLOCK")

#: The three free-text fields of the review basis -- the ones whose *presence*
#: is the whole contract, with no closed vocabulary to check the value against.
#: `Assurance path` is the fourth and is handled by `_parse_one_field`, because
#: it alone has a vocabulary (`ASSURANCE_PATHS`).
#:
#: Chunk C introduced these as `_CODE_REVIEW_BASIS_FIELDS`, wired to the
#: Code-review record only.  Renamed because the accepted parent's
#: "Bounded current contracts" is explicit that the basis is *not* Code-review
#: property: *"Every proposal, plan, and code review records"* these four lines.
#: One tuple, three record kinds, one shared checker (`_review_basis_violations`)
#: -- so a future field cannot be added to one kind and forgotten in the others.
#: Order is the reported order.
_REVIEW_BASIS_FREE_FIELDS = ("Reviewed commit", "Target", "Prior findings")

#: The closed assurance vocabulary -- **PUBLIC, and the name is load-bearing.**
#:
#: This was declared privately, then published without changing a value, because
#: a *fourth* consumer now needs it: `tools/lifecycle.py`'s monitoring report must
#: record a counted plan's resolved assurance path
#: (`review-efficient-lifecycle` > `## Carried-forward obligations`),
#: and P6a deliberately refused to close that early precisely because the only
#: two ways available were to reach into a private name or to re-declare the two
#: tokens in the CLI -- the second vocabulary Chunk A exists to prevent.  Its own
#: record says so: *"The assurance split additionally needs a **public** single
#: source for the assurance-path vocabulary."*  So this is that source, read
#: through the same contained loader the status vocabulary is read through.
ASSURANCE_PATHS = ("standard", "high-assurance")

#: The complete four-field basis, in the order the accepted parent writes it.
#: Used for the refusal message, so a reader is told the whole contract rather
#: than only the one field they happened to omit.
_REVIEW_BASIS_FIELDS = _REVIEW_BASIS_FREE_FIELDS + ("Assurance path",)


def _code_review_field_re(name: str) -> "re.Pattern[str]":
    """One full-line field matcher, **emphasis-optional**.

    The field NAME is the contract; the emphasis is not, and admitting only one
    spelling would refuse correct records for no contract reason.  Both spellings
    are live text: the accepted parent writes the basis unbolded --

        Reviewed commit: <full commit id>

    -- while every real review in `dev/plans/` writes the same lines bolded
    (`**Reviewed commit**:`), and the schema specifies `**Model**:`,
    `**Verdict**:`, `**Findings**:` with the bold.  Full-line anchored, so an
    ``Answers``-style prose mention cannot become a field.
    """
    return re.compile(
        r"^(?:\*\*|__)?" + re.escape(name) + r"(?:\*\*|__)?:[ \t]*"
        r"(?P<value>.*?)[ \t]*$", re.M)


#: One matcher per field name, from the one matcher factory.  Three
#: names here rather than compiling a fourth pattern of its own: `Contract
#: non-expansion` and `Basis` are read from a Code-review pass's field scope, and
#: `Inherited proposal basis` from a plan header, but all three are the same
#: emphasis-optional full-line field shape, so they are the same matcher.
_REVIEW_FIELD_RE = {
    name: _code_review_field_re(name)
    for name in _REVIEW_BASIS_FIELDS + (
        "Model", "Verdict", "Findings",
        "Contract non-expansion", "Basis", "Inherited proposal basis",
        # P2-R: the proposal-side readiness declaration, the plan-side
        # expansion/reduction declarations, and the plan's pointer at the
        # proposal whose readiness it inherits.  Same emphasis-optional
        # full-line shape, so the same matcher factory.
        "Plan readiness", "Contract expansion", "Scope delta",
        "Source proposal",
        # The per-pass obligation binding, the orthogonal blocker, and
        # `Tier` -- which the Plan-review pass reads through the bold-only
        # `_TIER_LINE_RE`, but the PROPOSAL review record needs in the same
        # emphasis-optional shape as its basis fields.  Same
        # full-line shape, so the same matcher factory rather than a fourth regex.
        "Obligation", "Blocked by", "Tier")
}

#: Emphasis markers, deleted before the verdict line is read.  The house form in
#: this tree wraps the label **and** the value in one bold span --
#: ``**Verdict: SHIP.**``, 30 of the 38 corpus passes -- not just the label, so a
#: matcher anchored on ``**Verdict**:`` alone would miss almost every real
#: record while appearing to work on the three that use the other spelling.
_EMPHASIS_RE = re.compile(r"\*\*|__")

#: The verdict VALUE, once emphasis is gone: everything up to the first clause
#: break.  ``**Verdict: REVISE / NOT CLEARED TO ARCHIVE.**`` and
#: ``**Verdict: Accept-with-followups**, applying to the four commits ...`` are
#: both real, so trailing prose must be tolerated -- but only *after* a break
#: character, never inside the token, so `SHIP but actually BLOCK` is
#: out-of-vocabulary and refuses rather than parsing as `SHIP`.
_VERDICT_CLAUSE_RE = re.compile(r"^[^.,;(/]*")

#: The leading clause of a closed-vocabulary field value.  Wider than
#: `_VERDICT_CLAUSE_RE` by the two dash forms this project actually writes --
#: an em dash and `--` are Cairn's normal clause break, and the author whose
#: proposal exposed this wrote `**high-assurance** -- <reason>`.  Truncation is
#: only half the rule; see `_parse_one_field` for the contradiction guard that
#: makes it safe in both directions.
_VALUE_CLAUSE_RE = re.compile(r"^[^.,;(/—]*?(?=\s+--\s|\s*[.,;(/—]|$)")

#: The mandatory fields sit **before the pass's first H3**.  Not decoration:
#: real passes carry a `### 4. Verdict & Archive Readiness` subsection that
#: repeats the verdict, and reading the whole body would report the pass's own
#: summary as a *duplicate field*.
_FIRST_H3_RE = re.compile(r"^###\s", re.M)

#: The Code-review record's legacy population, ENUMERATED.
#: ``stem -> {raw-heading digest: n}``, the same shape as `_LEGACY_PASSES`, so
#: `_is_legacy`'s k-th-occurrence anti-replay rule applies unchanged.
#:
#: **Baseline commit `4ca44eb8d1b378a0214019270e1a2d83976c7bb0`.**  The rule requires
#: the baseline pinned to one named commit and recorded in the manifest; the
#: generator, `scripts/gen_legacy_code_review_passes.py`, reads *that commit's*
#: tree rather than the working tree, so the population is reproducible by
#: anyone.  A record appearing after it conforms to the forward schema or
#: violates -- the contract is forward-only.
#:
#: Authored **independently of the generator** (the separation the Plan-review
#: manifest already requires of itself): this literal was derived through a
#: second, unrelated path -- `git ls-tree` / `git show` / `grep -E` /
#: `shasum -a 256` at the shell, with the heading patterns typed from the
#: published grammar -- and the two derivations agreed byte-for-byte.  Two
#: independent producers agreeing is the oracle; a manifest checked only by its
#: own generator has none.
#:
#: The population is three admission rules, and rule 3's restriction is a
#: **safety** boundary rather than tidiness -- see the generator's docstring:
#: conforming passes and Response headings from a plan of any status, but a
#: NON-conforming ``## Code review`` container heading only from a plan already
#: `archived`.  Every live plan ships that bare heading as a template
#: placeholder, and admitting one would let a placeholder satisfy the archive
#: presence obligation -- the exact defect `archive-precondition-substance`
#: closed after two plans archived with no code review while the gate reported
#: success.
_LEGACY_CODE_REVIEW_RECORDS: Dict[str, Dict[str, int]] = {
    "adopter-entry-doc-refresh": {"da0d3a494e6c2399": 1},
    "adopter-licensing-compliance": {"b6d076f60c9256a0": 1},
    "agent-context-scrub": {"1f5b17996546874b": 1, "3710ab6ae7910816": 1},
    "api-web-security-modules": {"19c404c4ed5669d6": 1, "3710ab6ae7910816": 1},
    "archive-precondition-substance": {"bff67e0bf923a268": 1, "e08f6cbd1145cce3": 1},
    "ast-known-new-repin": {"3710ab6ae7910816": 1, "dad784757d072aaa": 1},
    "board-drain-guards": {"3710ab6ae7910816": 1},
    "byline-classification": {"3710ab6ae7910816": 1, "a2e2e2d01b4c4b84": 1},
    "content-scan-detectors": {"3710ab6ae7910816": 2},
    "content-scan-url-classification": {"3710ab6ae7910816": 1},
    "corpus-tier-cost": {"3710ab6ae7910816": 1, "953182b8d0c88a33": 1},
    "default-security-stance": {"2f1ed5f4a6030e9a": 1, "3710ab6ae7910816": 1},
    "deferral-discipline": {"3710ab6ae7910816": 1},
    "dependency-advisory-coverage": {"3710ab6ae7910816": 2},
    "first-session-survivability": {"b6d076f60c9256a0": 1},
    "fork-advisory-semantics": {"1f5b17996546874b": 1, "a2e2e2d01b4c4b84": 1},
    "gate-claims-vs-enforcement": {"3710ab6ae7910816": 1, "a2e2e2d01b4c4b84": 1},
    "gate-reanchor-preflight": {"3710ab6ae7910816": 1},
    "interpreter-trust-root-fallback": {"3710ab6ae7910816": 1, "dad784757d072aaa": 1},
    "lockfile-provenance-fields": {"3710ab6ae7910816": 1, "dad784757d072aaa": 1},
    "planner-line-semantics": {"1f5b17996546874b": 1, "3710ab6ae7910816": 1},
    "portable-security-sweeps": {"133b1b1bada928a1": 1, "3710ab6ae7910816": 1, "4d0d177eaa09cd1a": 1},
    "profile-parse-fail-open": {"1f5b17996546874b": 1, "a2e2e2d01b4c4b84": 1},
    "record-corrections": {"3710ab6ae7910816": 1, "b6d076f60c9256a0": 1},
    "release-authenticity": {"1f5b17996546874b": 1, "a2e2e2d01b4c4b84": 1},
    "release-security-bar": {"613fd1047ac9437e": 1, "953182b8d0c88a33": 1},
    "release-security-orchestration": {"3710ab6ae7910816": 1, "9095c6aaeb9010af": 1},
    "review-gate-enforcement": {"133b1b1bada928a1": 1, "3710ab6ae7910816": 1, "4d0d177eaa09cd1a": 1},
    "review-record-integrity": {"d6bb6fb023fccc3b": 1},
    "scan-coverage": {"3710ab6ae7910816": 1, "a2e2e2d01b4c4b84": 1},
    "scope-reduction-trap": {"8d164c71a3d3304a": 1},
    "security-preflight-checklist": {"133b1b1bada928a1": 1, "1f5b17996546874b": 1, "3710ab6ae7910816": 1},
    "security-verification-activation": {"19c404c4ed5669d6": 1, "3710ab6ae7910816": 1},
    "separator-detection": {"3710ab6ae7910816": 1, "4d0d177eaa09cd1a": 1, "583870e04dc21873": 1},
    "solo-legacy-adopter-path": {"3710ab6ae7910816": 1, "dad784757d072aaa": 1},
    "stage-commit-patterns": {"133b1b1bada928a1": 1, "3710ab6ae7910816": 1},
    "transition-lint": {"133b1b1bada928a1": 1, "3710ab6ae7910816": 1},
    "verification-evidence-boundaries": {"3710ab6ae7910816": 1},
}

#: For a legacy pass whose verdict BLOCKS, the manifest
#: *"additionally names the specific admitted disposition heading that completes
#: each record."*  ``stem -> {pass digest: disposition-heading digest}``.
#:
#: This is a **check, not a comment**: the named heading must appear as a raw
#: line positioned after that pass, or the record is not admitted.  Naming it
#: without checking it would be the failure mode `AGENTS.md` > *Verifying claims*
#: describes -- a claim whose only trigger is a reader believing it.
#:
#: **Why a digest rather than the heading text, which would read better.**  This
#: file ships as a template, and `scripts/quality_gate.py --sub neutrality`
#: refuses an AI-vendor name anywhere under `templates/` with **no exemption
#: path**.  Every real disposition heading in this repository carries its
#: author's byline, and those bylines are vendor names -- so the literal form
#: fails that gate by construction (measured: 4 new failures, 93 -> 97).  A
#: digest names exactly one heading, in the same currency `_LEGACY_PASSES`
#: already uses for the same reason, and
#: ``gen_legacy_code_review_passes.py --report`` resolves it back to text.
#:
#: **The population is four, not the two the vocabulary names.**  It names
#: `record-corrections` and `release-security-orchestration`, measured
#: `as_of 2026-08-10`.  Re-derived at the baseline commit
#: (`gen_legacy_code_review_passes.py --report`): `release-security-bar` and
#: `scope-reduction-trap` also carry a blocking latest pass, both landing after
#: that measurement.  Naming only the proposal's two would grant two *unnamed*
#: blocking exemptions, which is the opposite of what the clause is for.
_LEGACY_CODE_REVIEW_DISPOSITIONS: Dict[str, Dict[str, str]] = {
    "record-corrections": {"b6d076f60c9256a0": "1e1cbf1ba07bf9ff"},
    "release-security-bar": {"953182b8d0c88a33": "6cbb16665ede606e"},
    "release-security-orchestration": {"9095c6aaeb9010af": "97aae64e391a75c6"},
    "scope-reduction-trap": {"8d164c71a3d3304a": "30861d65bf98a5b5"},
}


def _record_boundaries(art: Artifact) -> List[int]:
    """The ONE canonical ordered boundary set, of **both** record kinds.

    Level-<=2 Sections, unioned with every raw conforming pass line of either
    kind.  This was built from `_S1_PASS_RE` alone because the Code-review
    grammar did not exist yet; both kinds are needed, and this completes it.

    Widening a boundary set can only ever **narrow** a body, never widen one, so
    applying it to already-recognized sections stays safe -- the property
    `_pass_body` relies on.  What it fixes: a Code-review heading whose reviewer
    field carries parentheses outside the ``(<role>)`` position is invisible to
    `_HEADER_RE`, so before this it did not terminate the Plan-review pass above
    it, and that pass's body ran straight through it -- swallowing its
    attestation lines and reporting them as the *earlier* pass's duplicates.

    The proposal `## Review` record is a third kind, on the same
    argument and with the same measured safety: those lines occur only in
    proposals and plan passes only in plans, so no plan pass body changes by a
    byte -- and where a proposal review heading *is* parseable by `_HEADER_RE` it
    was already a level-2 Section and already a boundary.  What it adds is the
    heading `_HEADER_RE` cannot parse (a `(Round 2)` with a capital R is enough),
    which before this did not terminate the record above it.
    """
    lines = art.text.split("\n")
    return sorted(
        {sec.line_no for sec in art.sections if sec.level <= 2}
        | {i + 1 for i, raw in enumerate(lines) if _S1_PASS_RE.match(raw)}
        | {i + 1 for i, raw in enumerate(lines)
           if _CODE_REVIEW_PASS_RE.match(raw)}
        | {i + 1 for i, raw in enumerate(lines)
           if _PROPOSAL_REVIEW_RECORD_RE.match(raw)})


#: Any ``## Code review`` H2 heading at all.  The set difference against
#: `_CODE_REVIEW_PASS_RE` is the *container* population -- the bare heading the
#: plan template ships, and decorated variants like
#: ``## Code review — the brief (no review has landed)``.
_CODE_REVIEW_ANY_RE = re.compile(r"^## Code review(?:[^0-9A-Za-z].*)?$")


def _code_review_records(art: Artifact) -> List[Tuple[int, str, str]]:
    """Every Code-review record heading in *art*, in document order.

    ``(line_no, raw_heading, kind)`` with *kind* one of ``pass`` (conforming per
    the grammar), ``container`` (a ``## Code review`` heading that is not a pass), or
    ``response``.  One ordered stream, because the legacy fence counts
    occurrences and the count must be taken over the same sequence the generator
    walked.
    """
    out: List[Tuple[int, str, str]] = []
    for i, raw in enumerate(art.text.split("\n")):
        if _CODE_REVIEW_PASS_RE.match(raw):
            out.append((i + 1, raw, "pass"))
        elif _CODE_REVIEW_ANY_RE.match(raw):
            out.append((i + 1, raw, "container"))
        elif _RESPONSE_TO_CODE_REVIEW_RE.match(raw):
            out.append((i + 1, raw, "response"))
    return out


def _code_review_pass_body(art: Artifact, line_no: int) -> str:
    """The field scope of the pass at *line_no*: its body up to its first H3."""
    body = _pass_body(art.text.split("\n"), line_no, _record_boundaries(art))
    cut = _FIRST_H3_RE.search(body)
    return body[:cut.start()] if cut else body


def _parse_verdict(body: str) -> Tuple[Optional[str], Optional[str]]:
    """``(clearing|blocking, violation)`` from one pass's field scope."""
    found = _REVIEW_FIELD_RE["Verdict"].findall(_EMPHASIS_RE.sub("", body))
    if not found:
        return None, "missing Verdict"
    if len(found) > 1:
        return None, "duplicate Verdict"
    raw = _VERDICT_CLAUSE_RE.match(found[0]).group(0).strip()
    for value in CODE_REVIEW_CLEARING_VERDICTS:
        if raw.casefold() == value.casefold():
            return "clearing", None
    for value in CODE_REVIEW_BLOCKING_VERDICTS:
        if raw.casefold() == value.casefold():
            return "blocking", None
    return None, (
        f"unrecognized Verdict value: {raw!r} -- the vocabulary is closed: "
        f"clearing {'/'.join(CODE_REVIEW_CLEARING_VERDICTS)}; "
        f"blocking {'/'.join(CODE_REVIEW_BLOCKING_VERDICTS)}")


def _code_review_ordering_violations(
        passes: List[Tuple[int, str, str, Optional[str]]]) -> List[str]:
    """The ordering rules, over passes **sharing a date**.

    Document order is authoritative, and `(round N)` exists only to make round
    order and document order agree.  So among passes sharing one date: a round
    must be unique and strictly increasing down the file, and an unnumbered pass
    may not share a date with a numbered one.  "Ties refuse" was reaching for
    exactly this and never defined it; there is no other tie case.

    Two *unnumbered* passes sharing a date are **allowed** -- one archived plan
    has them, from two different reviewers on one day -- and the ambiguity that
    creates is answered where it actually bites, in the `Answers:` binding's
    exactly-one-match rule, not by refusing the passes.
    """
    v: List[str] = []
    by_date: Dict[str, List[Tuple[int, Optional[str]]]] = {}
    for line_no, _reviewer, date, rnd in passes:
        by_date.setdefault(date, []).append((line_no, rnd))
    for date, group in sorted(by_date.items()):
        rounds = [(ln, rnd) for ln, rnd in group if rnd is not None]
        bare = [ln for ln, rnd in group if rnd is None]
        if rounds and bare:
            v.append(
                f"Code-review passes dated {date} mix an unnumbered pass (line "
                f"{bare[0]}) with a '(round N)' pass (line {rounds[0][0]}) -- "
                "on one date, either every pass carries a round or none does")
            continue
        previous: Optional[int] = None
        for line_no, rnd in rounds:
            number = int(rnd or 0)
            if previous is not None and number <= previous:
                v.append(
                    f"Code-review pass at line {line_no} declares '(round "
                    f"{number})' after '(round {previous})' on the same date "
                    f"({date}) -- rounds must be unique and strictly increasing "
                    "in document order")
            previous = number
    return v


def _code_review_violations(art: Artifact) -> List[str]:
    """The Code-review record contract over one artifact.

    **Not a public entry point and not a second predicate.**  It folds
    Code-review evaluation *into* `review_record_violations`, which already
    declares itself the one predicate (S12); this is that function's
    Code-review half, factored out for reading only, and it has exactly one
    caller.  A sibling public predicate would recreate the
    two-interpretations problem S12 exists to prevent.
    """
    stem = art.path.stem
    records = _code_review_records(art)
    v: List[str] = []

    # The legacy fence, walked over the ordered stream so occurrence k is the
    # k-th appearance of that digest in the file (the anti-replay component).
    seen: Dict[str, int] = {}
    legacy: Dict[int, bool] = {}
    for line_no, raw, _kind in records:
        dig = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
        seen[dig] = seen.get(dig, 0) + 1
        legacy[line_no] = _is_legacy(stem, dig, seen,
                                     _LEGACY_CODE_REVIEW_RECORDS)

    passes = _code_review_pass_lines(art)
    v.extend(_code_review_ordering_violations(passes))

    # The binding, with legacy Responses exempt.  A Response is a record about
    # a pass, so its defects are reported whether or not a pass is the latest.
    v.extend(code_review_binding_violations(
        art, skip_lines={line_no for line_no, _raw, kind in records
                         if kind == "response" and legacy[line_no]}))

    if not passes:
        # Presence.  "Absent Code review on an `archived` plan remains the
        # existing violation."  A legacy container satisfies it, but only with a
        # reviewer marker somewhere: grandfathering reaches records written
        # before the schema, not records with no reviewer identity at all.
        container = any(kind == "container" and legacy[line_no]
                        for line_no, _raw, kind in records)
        if container and art.has_code_review_marker:
            return v
        v.append(
            "no conforming '## Code review -- <reviewer> -- YYYY-MM-DD"
            "[ (round N)]' pass is present, and this state requires one. The "
            "section's PRESENCE is not evidence a review happened: the plan "
            "template ships '## Code review' pre-written, so a presence test "
            "is impossible to fail (two plans archived on 2026-08-11 with no "
            "code review while it reported success).")
        return v

    line_no, reviewer, date, _round = passes[-1]   # document order
    label = f"'## Code review -- {reviewer} -- {date}'"
    ok_date, date_violation = _parse_pass_date(date)
    if date_violation:
        # Checked BEFORE the legacy fence, for the reason the Plan-review path
        # states: an exemption keyed on the heading would otherwise swallow the
        # date contract, which is how the replaced dated epoch failed.
        v.append(f"{label}: {date_violation}")
    # Also BEFORE the fence, and for the same reason the basis check sits
    # before `_LEGACY_PASSES`' `continue`.  `_LEGACY_CODE_REVIEW_RECORDS`
    # grandfathers records written before the Code-review schema existed; a plan
    # declaring `Inherited proposal basis:` necessarily post-dates P2-R, so no
    # legacy record can honestly claim this exemption and placing the check
    # first costs nothing while removing a laundering path from the file.
    v.extend(_non_expansion_violations(art, line_no, label))
    if legacy[line_no]:
        return v + _legacy_disposition_violations(art, stem, line_no, label)

    body = _code_review_pass_body(art, line_no)
    # The four-field basis is ONE shared checker across all three record
    # kinds (`_review_basis_violations`).  `**Model**:` stays here because it is
    # A Code-review-only attestation, not part of the parent's basis.
    v.extend(_review_basis_violations(body, label))
    v.extend(_single_field_violations(body, "Model", label))
    _find, findings_violation = _parse_one_field(
        body, _REVIEW_FIELD_RE["Findings"], _FINDINGS, "Findings")
    verdict, verdict_violation = _parse_verdict(body)
    for problem in (findings_violation, verdict_violation):
        if problem:
            v.append(f"{label}: {problem}")
    if verdict == "blocking":
        # The whole point: no disposition branch.  A `## Response to code
        # review` records the implementer's answer and does NOT clear archive --
        # eligibility comes from a later pass by an independent correction
        # reviewer, which is the accepted parent's boundary this amendment was
        # written to supply rather than weaken.
        v.append(
            f"{label} carries a BLOCKING verdict, so this state is refused. A "
            "'## Response to code review' does not clear it: correct the "
            "findings, land a replacement Boundary B record over the corrected "
            "range, and have an independent correction reviewer append a new "
            "pass. Archive eligibility comes from THAT pass's clearing verdict.")
    # 'Findings: raised' with a clearing verdict is a COMPLETE record and does
    # not block -- the common case; a schema must not criminalise it.
    return v


def _legacy_disposition_violations(art: Artifact, stem: str, line_no: int,
                                   label: str) -> List[str]:
    """A blocking legacy pass needs its named disposition.

    Silent when the pass carries no verdict line (15 of the 38 corpus passes do
    not) or a clearing one: grandfathering exempts a legacy record from the
    *schema*, and the only thing this adds back is the completion the accepted
    clause requires of the blocking cases specifically.
    """
    lines = art.text.split("\n")
    verdict, _violation = _parse_verdict(_code_review_pass_body(art, line_no))
    if verdict != "blocking":
        return []
    dig = hashlib.sha256(lines[line_no - 1].encode("utf-8")).hexdigest()[:16]
    wanted = _LEGACY_CODE_REVIEW_DISPOSITIONS.get(stem, {}).get(dig)
    if wanted is None:
        return [f"{label} is a legacy pass with a BLOCKING verdict and no "
                "admitted disposition named for it in "
                "'_LEGACY_CODE_REVIEW_DISPOSITIONS' -- the enumeration admits "
                "such a pass only by naming the heading that completes it"]
    for i, raw in enumerate(lines):
        if i + 1 > line_no and hashlib.sha256(
                raw.strip().encode("utf-8")).hexdigest()[:16] == wanted:
            return []
    return [f"{label} is admitted as legacy on the disposition heading "
            f"digested {wanted}, which is not present after it "
            "(resolve the digest with "
            "'scripts/gen_legacy_code_review_passes.py --report')"]


# === the four-field basis across all three record kinds ======================
#
# The accepted `review-efficient-lifecycle` parent, "Bounded current contracts":
#
#     Every proposal, plan, and code review records:
#         Reviewed commit: <full commit id>
#         Target: <complete current-contract section, operative plan sections,
#                  or code range>
#         Prior findings: <ids being closed, or none>
#         Assurance path: <standard | high-assurance>
#
# Chunk C wired all four for the **Code-review** record.  This block extends the
# identical requirement to the **Plan-review** pass and the proposal
# **`## Review`** record, and adds the artifact-level `Assurance path:`
# declaration from the parent's "Assurance paths" section.
#
# What the tool does and does not claim (restated because
# this block is where a reader will look for it): it checks that the record
# EXISTS and BINDS.  It never checks that the declared assurance path is the
# *true* classification of the change -- the five high-assurance triggers are
# **author declarations, not inferences**, taught in the authoring templates.  A
# scanner cannot know whether a change touches a scientific assumption.


#: Any proposal `## Review` record heading.
#:
#: **Deliberately permissive where `_S1_PASS_RE` is strict, and the asymmetry is
#: the safety property.**  A strict `-- <reviewer> -- YYYY-MM-DD` grammar would
#: turn every other review heading into a *near miss*: invisible to this check,
#: yet still counted by `_reviewers()`, which is what satisfies the "status is
#: 'reviewed' but no '## Review' section is present" floor.  That combination is
#: an escape hatch -- write the heading slightly off-grammar and the basis
#: obligation disappears while the presence floor stays satisfied.  So **any**
#: H2 heading opening `## Review -- ` is a record and owes the basis.  Live
#: proof that the strict shape would under-reach: this repository's own review
#: headings include `(External)` role parentheticals, `(Round 2)` with a capital
#: R, and `(round 4, closure read)`; none matches an `_S1_PASS_RE`-shaped rule.
#:
#: The required ` -- ` is what keeps `## Reviewer brief` (a real heading in three
#: proposals here) out, and `## Response to ...` never begins `## Review`.
_PROPOSAL_REVIEW_RECORD_RE = re.compile(r"^## Review -- \S.*$")


#: **Grandfathering follows immutability, not directory.**  This is the shape
#: The same rule landed in `scripts/claim_check.py` for the same problem, reused here
#: rather than re-invented -- its accepted contract
#: (`claim-check-exemption-hygiene`) states it as: any file under
#: `dev/proposals/archive/` or `dev/plans/archive/`; a proposal whose strictly
#: parsed status is `accepted` / `rejected` / `superseded`; or a plan whose
#: strictly parsed status is `archived`.
#:
#: **Why immutability rather than an enumeration of the whole corpus.**  The
#: basis fields did not exist when any existing record was written, and every
#: one of those records is append-only: they *cannot* be retrofitted, so a
#: requirement that reaches them is a permanent red on text nobody may edit.
#: `scan` (live-only) is the enforcement surface and is kept at "all artifacts
#: sound"; `scan --include-archive` is a strict historical audit that already
#: reports most of the corpus as violating and never was a clean surface.
#: Demanding the basis of archived material would add noise to the audit and
#: require rewriting immutable history, which the lifecycle forbids outright.
def _is_archived_by_location(path: Path) -> bool:
    """``dev/{proposals,plans}/archive/<name>.md`` -- immutable by location.

    Checked on the two path components rather than on a repo-relative string, so
    it holds for a fixture under a `tmp_path` root exactly as it holds here.
    """
    return (path.parent.name == "archive"
            and path.parent.parent.name in ("proposals", "plans"))


#: A STRICT status line: exactly the bolded header field, one bare token.
#: Deliberately narrower than `_parse_status`, which is documented as
#: "best-effort" and takes the first of up to 60 lines.  The two are not
#: redundant and must not be merged: `_parse_status` answers "what does this
#: artifact declare", and every conformance check depends on its tolerance.  This
#: one answers "may this artifact be rewritten", where tolerance is a hazard --
#: so it can only ever *refuse* to grandfather, never wrongly grant.
_STRICT_STATUS_LINE_RE = re.compile(
    r"^\*\*Status\*\*:[ \t]*(?P<status>[A-Za-z][A-Za-z-]*)[ \t]*$")


def _strict_header_status(text: str) -> Optional[str]:
    """The artifact's strictly parsed header status, or ``None``.

    Strict means **exactly one** `**Status**: <token>` line in the *header* --
    the region above the first `##` heading, which is where both authoring
    templates put the field.  A `**Status**:` line inside an appended revision
    section is a historical restatement, not the artifact's current status, so it
    is not a candidate; zero or several candidates in the header yield ``None``.

    ``None`` means "not grandfathered".  A missing, duplicate, or unrecognized
    status therefore falls through *into* the requirement rather than silently
    inheriting the exemption -- the fail-closed direction that contract names.
    """
    found: List[str] = []
    for line in _split_lines(text):
        if line.startswith("## "):
            break
        m = _STRICT_STATUS_LINE_RE.match(line.strip())
        if m is not None:
            found.append(m.group("status").lower())
    return found[0] if len(found) == 1 else None


def _is_immutable(art: Artifact) -> bool:
    """True when nobody may rewrite *art* -- archived, or terminal by status."""
    if _is_archived_by_location(art.path):
        return True
    terminal = (PROPOSAL_TERMINAL_STATES if art.kind == "proposal"
                else PLAN_TERMINAL_STATES)
    return _strict_header_status(art.text) in terminal


#: The commit at which the two enumerations below were derived, pinned and named
#: so a reader can reproduce the population instead of trusting the literals.
#: Records appearing after it conform to the forward schema or violate -- the
#: contract is forward-only, exactly as the accepted rule requires of the manifest.
_BASIS_BASELINE_COMMIT = "50a32237c54cbce437b0834c48bd9c5645b9cd7a"

#: The legacy population for the **basis requirement specifically**.
#: ``stem -> {raw-heading digest: occurrence count}`` -- `_LEGACY_PASSES`' shape,
#: so `_is_legacy`'s k-th-occurrence anti-replay rule applies unchanged: an
#: appended heading byte-identical to an admitted one is occurrence ``n + 1`` and
#: is refused.
#:
#: **This is deliberately NOT `_LEGACY_PASSES`.**  That enumeration exempts a
#: pass on Tier, Findings and disposition.  Every record below already
#: satisfies all three today, so folding them into `_LEGACY_PASSES` would *weaken*
#: the gate for those records while appearing to do nothing but grandfather. A
#: separate manifest, scoped to the one obligation it grandfathers, is what keeps
#: each exemption saying only what it means.
#:
#: **Why it is eight entries and not seventy-two.**  A whole-corpus measurement
#: gives ~72 non-conforming records; the immutability predicate above removes
#: every archived and terminal one, because they are unrewritable history rather
#: than ongoing evidence.  What remains is the live, still-mutable population:
#: three artifacts, eight records.  The enumeration is small **by design, not by
#: omission** -- `_is_immutable` is the predicate that does the rest of the work,
#: and it is tested directly.
#:
#: **Hand-authored, and no generator.**  A generator over a named
#: baseline for its 38 records, plus an independently-typed second derivation as
#: the oracle, because nobody can eyeball a 38-entry table.  Eight entries in
#: three artifacts is not that problem: a second shipped script, a
#: baseline-drift test and a re-derivation oracle would be more machinery than
#: the thing they guard. The derivation is instead reproducible by hand --
#: `sha256(raw heading line)[:16]` for each heading a reader can see in the three
#: named artifacts -- and `test_lifecycle_contract.py` pins every entry against
#: the live tree, so a fabricated or stale entry reddens.
#:
#: The exemption is **per record, not per field**: it covers the whole basis for
#: that record, matching `_is_legacy`'s existing all-or-nothing semantics for
#: `_LEGACY_PASSES`.  Splitting it per field would need per-field manifest data
#: to grandfather records whose bytes are append-only and will not change.
_LEGACY_UNDECLARED_BASIS: Dict[str, Dict[str, int]] = {
    # Empty, and legitimately so. `git-native-security-foundations` was removed
    # on 2026-08-13 and `review-efficient-lifecycle` on 2026-08-19, each when it
    # archived: an archived artifact is already covered by `_is_immutable`, so
    # the entry became dead weight and the contract test says so. This set only
    # ever shrinks, and archiving is one of the two ways it does.
    #
    # An empty table is not a defect here -- it is the predicate above having
    # absorbed the whole population. Every record this once grandfathered is now
    # unrewritable history. A future live record that needs the exemption adds
    # its own entry; until then the enumeration holds nothing because there is
    # nothing live left for it to hold.
}

#: The artifact-level counterpart: live proposals that carried no
#: `**Assurance path**:` header declaration at `_BASIS_BASELINE_COMMIT`.
#:
#: **A stem set, not digest+count, and the divergence is the point.**  The
#: obligation here is a property of the *artifact*, not of a heading, so there is
#: no heading to digest and no occurrence to count -- forcing the record shape
#: onto it would be shape-matching rather than design.  A stem cannot be replayed
#: for the reason a digest can: a stem is a file path, and claiming this
#: exemption for new work would mean authoring it *as* one of these artifacts.
#:
#: This set only ever **shrinks**.  Adding the header line to a live proposal is
#: legal (the header is mutable metadata -- `**Status**:` already flips in
#: place), so each entry becomes dead the moment its artifact declares, and
#: deleting it then is the maintenance.  It grandfathers **absence only**: a
#: declaration that is present but duplicated or out-of-vocabulary refuses here
#: exactly as it would anywhere else.
_LEGACY_UNDECLARED_ASSURANCE_PATH = frozenset({
})


def _single_field_violations(body: str, field: str, label: str) -> List[str]:
    """Presence / uniqueness / non-emptiness of one field, as three violations.

    Factored out of the Code-review loop so the basis checker and the
    Code-review-only `**Model**:` check cannot drift into reporting the same
    defect in two different sentences.
    """
    found = _REVIEW_FIELD_RE[field].findall(body)
    if not found:
        return [f"{label}: missing '{field}:' -- the four-field review basis "
                f"({' / '.join(_REVIEW_BASIS_FIELDS)}) is mandatory before the "
                "record's first H3"]
    if len(found) > 1:
        return [f"{label}: duplicate '{field}:' ({len(found)} lines)"]
    if not found[0].strip():
        return [f"{label}: empty '{field}:' value"]
    return []


def _review_basis_violations(body: str, label: str) -> List[str]:
    """The four-field review basis over ONE record's field scope.

    *body* is already narrowed to the field scope by the caller (the record body
    up to its first H3 -- see `_record_field_scope`).  Every one of the three
    fail-closed directions `_parse_one_field` documents applies: absent,
    out-of-vocabulary, and repeated **even when the repeated values agree**.
    """
    v: List[str] = []
    for field in _REVIEW_BASIS_FREE_FIELDS:
        v.extend(_single_field_violations(body, field, label))
    _path, problem = _parse_one_field(
        body, _REVIEW_FIELD_RE["Assurance path"], ASSURANCE_PATHS,
        "Assurance path")
    if problem:
        v.append(f"{label}: {problem}")
    return v


def _pass_obligation(field_scope: str,
                     declared: Tuple[Tuple[str, str], ...]) -> Optional[str]:
    """The ONE declared clause a Plan-review pass binds itself to.

    *field_scope* is the pass body up to its first H3 (`_record_field_scope`),
    because the field sits *"before its first H3"* -- the same scope the
    four-field basis uses, so a field parked under a subsection does not count.

    ``None`` is returned for every one of the four fail-closed conditions --
    *"Missing, duplicate, undeclared, or repeated-obligation values do not clear
    the floor"* -- and ``None`` means exactly that: the pass clears nothing.  It
    is deliberately not a per-pass violation, because the contract states the consequence as
    a floor consequence, and because the failure direction is the safe one: a
    typo'd obligation makes the floor *harder* to satisfy, never easier.

    Comparison is case-insensitive after `_strip_emphasis_chars` and ASCII
    whitespace collapsing -- the same normalization the declaration went through,
    so `**External Security Review**` in the declaration and `External Security
    Review` in the pass are the same clause.
    """
    found = _REVIEW_FIELD_RE["Obligation"].findall(field_scope)
    if len(found) != 1:
        return None
    value = _ASCII_WS_RE.sub(" ", _strip_emphasis_chars(found[0])).strip()
    for clause, _tier in declared:
        if value.casefold() == clause.casefold():
            return clause
    return None


def _record_field_scope(lines: List[str], line_no: int,
                        boundaries: List[int]) -> str:
    """One record's body, cut at its first H3 -- the declared field scope.

    The H3 cut is not tidiness and was measured on real records: a review pass
    routinely carries a `### 4. Verdict & Archive Readiness` or `### Coverage`
    subsection that *repeats* its own attestations, so reading the whole body
    reports a pass's own summary as a **duplicate field**.  It also means a field
    parked below an H3 does not count, which is what makes the scope a contract
    rather than a search.
    """
    body = _pass_body(lines, line_no, boundaries)
    cut = _FIRST_H3_RE.search(body)
    return body[:cut.start()] if cut else body


def _proposal_review_records(art: Artifact) -> List[Tuple[int, str]]:
    """``(line_no, raw_heading)`` per proposal `## Review` record, in document
    order.

    Read off the **raw lines** for the reason `_pass_headings` documents at
    length: a heading rebuilt out of parsed fields silently drops a `(<role>)`
    parenthetical, and then every digest comparison misses -- which would leave
    the enumeration inert while appearing to work.
    """
    return [(i + 1, raw) for i, raw in enumerate(art.text.split("\n"))
            if _PROPOSAL_REVIEW_RECORD_RE.match(raw)]


def proposal_review_basis_violations(art: Artifact) -> List[str]:
    """The review basis over a proposal's `## Review` records.

    Public because **both** gate surfaces consume it: `_conformance_violations`
    (what `scan` reports) and `_gating_preconditions` (what `next --to <target>`
    reports).  Wiring only the first is the exact defect executed on the
    Code-review half -- one surface tightens, the other stays presence-only, and
    the loose one is the one an author drives.
    """
    if _is_immutable(art):
        return []
    stem = art.path.stem
    lines = art.text.split("\n")
    boundaries = _record_boundaries(art)
    seen: Dict[str, int] = {}
    v: List[str] = []
    for line_no, raw in _proposal_review_records(art):
        dig = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
        seen[dig] = seen.get(dig, 0) + 1
        if _is_legacy(stem, dig, seen, _LEGACY_UNDECLARED_BASIS):
            continue
        v.extend(_review_basis_violations(
            _record_field_scope(lines, line_no, boundaries),
            f"'{raw.strip()}'"))
    return v


def assurance_declaration_violations(art: Artifact) -> List[str]:
    """The proposal's artifact-level `Assurance path:` declaration.

    The accepted parent's "Assurance paths": *"A proposal-worthy change declares
    `standard` or `high-assurance`."*  It is the **proposal** that declares --
    the plan carries the inheritance metadata instead.

    **It never defaults to `standard`.**  Missing, duplicated and
    out-of-vocabulary all refuse; the parent is explicit that *"Uncertainty
    resolves to `high-assurance`"*, so a silent `standard` default would invert
    the contract at precisely the point it was written to protect.

    Order is load-bearing: the field is parsed FIRST, and grandfathering is
    consulted only for the **absence** case.  A grandfathered artifact that later
    adds a malformed declaration is reporting a defect in text it just wrote, not
    inheriting a legacy absence -- and the header is mutable, so that case is
    reachable.
    """
    if art.kind != "proposal":
        return []
    header = "\n".join(
        line for line in _iter_header_lines(art.text))
    pattern = _REVIEW_FIELD_RE["Assurance path"]
    _value, problem = _parse_one_field(
        header, pattern, ASSURANCE_PATHS, "Assurance path")
    if problem is None:
        return []
    if not pattern.search(header):
        # ABSENCE -- the only condition grandfathering reaches.
        if _is_immutable(art) \
                or art.path.stem in _LEGACY_UNDECLARED_ASSURANCE_PATH:
            return []
        return [
            "no '**Assurance path**:' declaration in the header -- a "
            "proposal-worthy change declares 'standard' or 'high-assurance' "
            "(add '**Assurance path**: standard' or '**Assurance path**: "
            "high-assurance' beside '**Status**:'). There is NO default: "
            "uncertainty about whether a high-assurance trigger applies "
            "resolves to 'high-assurance', so an absent declaration cannot be "
            "read as 'standard'."]
    return [f"'**Assurance path**:' {problem} -- the vocabulary is closed "
            f"({' | '.join(ASSURANCE_PATHS)}) and has no default; uncertainty "
            "resolves to 'high-assurance'."]


def _iter_header_lines(text: str):
    """The header region: every line above the first `##` heading.

    Both authoring templates put the metadata block there, and bounding the read
    is what stops a `**Assurance path**:` line quoted inside an appended review
    or revision section from being read as the artifact's own declaration.
    """
    for line in _split_lines(text):
        if line.startswith("## "):
            return
        yield line


def _near_miss_headings(art: Artifact) -> List[str]:
    """Every heading that begins `Plan review` but is **not** a conforming pass.

    The refusal must *quote* these: an author who wrote
    ``### Plan review -- R -- 2026-05-01`` (H3), ``## Plan review -- R``
    (undated), a bare ``## Plan review`` container, or ``## Plan reviewers``
    is told which heading did not count, instead of being left to guess which
    of the near-miss shapes they hit.  A pass that *is* S1-conforming but
    declares too low a tier is **not** a near miss -- it counted, and the
    floor sentence covers it.
    """
    lines = art.text.split("\n")
    pass_lines = {sec.line_no for sec, _dig in _pass_headings(art)}
    out: List[str] = []
    for sec in art.sections:
        if not sec.kind.strip().lower().startswith("plan review"):
            continue
        if sec.line_no in pass_lines:
            continue
        out.append(lines[sec.line_no - 1].strip())
    return out


def _is_legacy(stem: str, dig: str, seen: Dict[str, int],
               manifest: Optional[Dict[str, Dict[str, int]]] = None) -> bool:
    """Is this the k-th occurrence of `dig`, with k <= manifest count?

    **One k-th-occurrence rule, two manifests.**  Chunk C adds a second
    enumeration (`_LEGACY_CODE_REVIEW_RECORDS`) for the Code-review record, and
    the accepted `code-review-blindness` requires that it match
    `_LEGACY_PASSES`' shape *"so ``_is_legacy``'s k-th-occurrence rule applies
    unchanged"*.  A default argument is how that stays literally true: writing a
    sibling `_is_legacy_code_review` would put two implementations of one
    anti-replay rule in the file, and the next person to fix a bug in one of
    them would not know to fix the other.

    A **third** enumeration goes through the same argument
    (`_LEGACY_UNDECLARED_BASIS`), which is what the default argument was built
    for: one anti-replay rule, now three scoped populations.
    """
    table = _LEGACY_PASSES if manifest is None else manifest
    admitted = table.get(stem, {}).get(dig, 0)
    return seen.get(dig, 0) <= admitted


# === the `Contract non-expansion` attestation ================================
#
# The accepted `review-efficient-lifecycle` parent, "Standard-path
# plan-readiness inheritance":
#
#     For an inherited plan, code review must include this exercised backstop:
#
#         Contract non-expansion: VERIFIED | NOT VERIFIED
#         Basis: proposal=<accepted full commit>; plan=<reviewed full commit>;
#                changed-paths=<reviewed range or manifest>
#
#     `VERIFIED` attests that the plan and implementation introduced no
#     undeclared scope item, invariant, public path, failure disposition, trust
#     boundary, or ceremony.  `NOT VERIFIED` is blocking.  This remains a
#     semantic human/agent review; the parser validates the record and bindings
#     but does not pretend to prove prose equivalence.
#
# The amendment (`code-review-blindness`, "Contract non-expansion") bounds what
# this chunk may do: it *"validates its **presence and binding shape** when the
# plan declares inheritance, and treats `NOT VERIFIED` as blocking. It does not
# attempt to validate the semantic claim"*, and it lists "Semantic
# verification of `Contract non-expansion`" as a deliberate exclusion.
#
# So the whole of it is: PRESENCE, the closed VOCABULARY, and the three
# bindings' SHAPE.  Nothing here reads the plan's prose, compares contracts, or
# forms an opinion about whether the attested claim is true -- and no future
# widening of this block may, without returning to the proposal boundary.
#
# **What this deliberately does NOT do, and where it lives instead.**  It does not
# check that `Basis: proposal=<X>` *equals* the commit the plan's own
# `Inherited proposal basis` names.  That cross-artifact equality is a real
# check and it is **P2-R's and P8-R's** ("changed review or accepted-proposal
# SHA refuses" -- the Maintainer-directed contract revision's required test
# matrix), which own the inheritance field's value grammar.  This landed *before*
# that field existed, so hard-coding a second, earlier reading of the grammar
# here is how the two would come to disagree.  It therefore keys on the field's
# PRESENCE and never parses its value.


#: The plan-side declaration that makes a plan *inherited* -- the ONE trigger
#: for everything in this block.
#:
#: **This name is the Maintainer-directed contract revision's, not the accepted
#: parent's, and the difference is load-bearing.**  The parent folded the whole
#: fact into the plan-review field:
#:
#:     Plan review: inherited(<review commit>; proposal=<accepted commit>)
#:
#: The 2026-08-11 revision split it in two, so the plan "carries both facts
#: separately":
#:
#:     Plan review: required(Internal)
#:     Inherited proposal basis: review=<full External-review commit>;
#:                                 proposal=<full accepted commit>
#:
#: The field is implemented elsewhere; this keys on it by name so the two meet at
#: one key rather than inventing a second spelling of "this plan is inherited";
#: `Plan review: inherited(...)` is NOT a trigger here, because the revision
#: removed it and a plan under the current contract declares `required(Internal)`
#: instead -- which is indistinguishable from an ordinary non-inherited plan.
_INHERITANCE_FIELD = "Inherited proposal basis"

#: The attestation and its binding line, both read from the Code-review pass's
#: field scope (`_code_review_pass_body` -- the body above the pass's first H3,
#: the same scope every other mandatory field is read from).
_NON_EXPANSION_FIELD = "Contract non-expansion"
_NON_EXPANSION_BASIS_FIELD = "Basis"

#: Closed, two values, and **no default**: an absent attestation is a violation
#: rather than an implied `VERIFIED`, for the reason `assurance_declaration_
#: violations` states about its own vocabulary -- a silent default inverts the
#: contract at exactly the point it was written to protect.
_NON_EXPANSION_VALUES = ("VERIFIED", "NOT VERIFIED")
_NON_EXPANSION_BLOCKING = "NOT VERIFIED"

#: The three bindings, in the parent's order (which is the reported order).
_NON_EXPANSION_BINDINGS = ("proposal", "plan", "changed-paths")

#: A **full** commit id, which is what the parent asks for twice ("accepted full
#: commit", "reviewed full commit").  Deliberately stricter than `_COMMIT_ID_RE`
#: (`[0-9a-f]{7,40}`, which admits an abbreviation): an abbreviated id is the one
#: thing a *binding* may not be, because abbreviations collide and a colliding
#: binding names two commits.  Lowercase only -- git emits lowercase, and the
#: file's existing commit-id pattern is lowercase for the same reason.
_FULL_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")

#: Where one binding starts.  Read with `finditer` rather than by splitting on
#: `;`, so `proposal=X; plan=Y changed-paths=Z` -- a missing separator at a line
#: fold, the likeliest real typo -- still parses into three bindings instead of
#: reporting `changed-paths` as absent.  `\b` cannot match inside
#: `changed-paths=` (it contains no `plan=` or `proposal=` substring).
_BASIS_BINDING_KEY_RE = re.compile(r"\b(proposal|plan|changed-paths)=")

#: A **folded continuation** of the `Basis:` line: the parent's own rendering of
#: the contract wraps, putting `changed-paths=` on an indented second line, and a
#: reviewer who copies that block verbatim must not be refused by the tool that
#: quotes it.  Maximally tight, so the fold can only ever absorb what it is for:
#: the line must be indented AND begin with one of the three binding keys, so no
#: other field, heading, or prose line can be swallowed into the value.
_BASIS_FOLD_RE = re.compile(r"^[ \t]+(?:proposal|plan|changed-paths)=")


def _declares_inheritance(art: Artifact) -> bool:
    """Does this plan declare an inherited proposal basis?  **Presence only.**

    Three deliberate narrownesses, each of which is a safety property:

    * **Plans only.**  The parent's clause is "for an inherited plan"; a
      proposal has no plan-review basis to inherit.

    * **Header-bounded** (`_iter_header_lines`, the same bound
      `assurance_declaration_violations` uses).  Not tidiness: the plan that
      *specifies* this field quotes it inside an appended revision section, so a
      whole-text search would make that plan declare inheritance about itself and
      fire this gate on the artifact that defines it.  A field is a header
      declaration or it is prose.

    * **Presence, not well-formedness.**  A malformed or empty declaration still
      triggers -- which is the fail-closed direction, because the alternative
      (requiring a parseable value before the attestation is owed) lets a
      half-written declaration buy silence on the backstop.  The value's own
      grammar is the field owner's obligation and refuses there; this does not read it.
    """
    if art.kind != "plan":
        return False
    header = "\n".join(_iter_header_lines(art.text))
    return _REVIEW_FIELD_RE[_INHERITANCE_FIELD].search(header) is not None


def _basis_value(body: str, *, field: str = _NON_EXPANSION_BASIS_FIELD,
                 fold_re: "re.Pattern[str]" = _BASIS_FOLD_RE
                 ) -> Tuple[Optional[str], Optional[str]]:
    """One binding line's value from a text region -> ``(value, violation)``.

    Presence, uniqueness and non-emptiness -- the three directions
    `_single_field_violations` reports -- and then the fold (`_BASIS_FOLD_RE`).
    Uniqueness is over the region, so a second line refuses as a
    duplicate rather than being silently ignored: two bindings in one record is
    an ambiguity a backstop must not resolve by picking one.

    *field* / *fold_re* are parameters for the reason
    `_basis_binding_violations` takes its keys as parameters: P2-R's
    `Inherited proposal basis` is the same read over a different field name and
    a different fold vocabulary, and one implementation of "read a foldable
    binding line" is what keeps the two from drifting.
    """
    pattern = _REVIEW_FIELD_RE[field]
    lines = _split_lines(body)
    hits = [i for i, line in enumerate(lines) if pattern.match(line)]
    if not hits:
        return None, f"missing '{field}:' line"
    if len(hits) > 1:
        return None, (f"duplicate '{field}:' line "
                      f"({len(hits)} lines)")
    i = hits[0]
    value = pattern.match(lines[i]).group("value").strip()
    for continuation in lines[i + 1:]:
        if not fold_re.match(continuation):
            break
        value += " " + continuation.strip()
    if not value:
        return None, f"empty '{field}:' value"
    return value, None


def _basis_binding_violations(
        value: str, label: str, *,
        field: str = _NON_EXPANSION_BASIS_FIELD,
        keys: Tuple[str, ...] = _NON_EXPANSION_BINDINGS,
        key_re: "re.Pattern[str]" = _BASIS_BINDING_KEY_RE,
        free_text: Tuple[str, ...] = ("changed-paths",),
        found_out: Optional[Dict[str, str]] = None) -> List[str]:
    """One `key=value; key=value` binding line's **shape**, already folded.

    Shape means: each declared key appears exactly once, carries a non-empty
    value, and -- for every key the contract calls a *full commit* (anything not
    in *free_text*) -- that value is 40 lowercase hex digits.  It does **not**
    mean the commits exist, are reachable, or say what the record claims: this
    function never touches git, and the parent is explicit that the semantic
    claim stays human.

    `changed-paths` is free text on purpose -- the parent admits "reviewed range
    or manifest", two different notations, and a pattern narrow enough to
    validate one would refuse the other.

    **One rule, two fields.**  This was written for the Code-review `Basis:` line's
    three bindings; P2-R's `Inherited proposal basis` is the same grammar with two
    keys and no free-text member, so it is passed in rather than given a second
    implementation -- the shape `_is_legacy` already uses for its three manifests.
    A sibling copy would put two implementations of one binding rule in this file,
    and the next person to fix a bug in one of them would not know to fix the
    other.  *found_out*, when supplied, receives the parsed bindings so a caller
    can check EQUALITY (P2-R) without re-parsing what this function just read.
    """
    matches = list(key_re.finditer(value))
    expected = ", ".join(f"{k}=" for k in keys)
    count = {2: "two", 3: "three"}.get(len(keys), str(len(keys)))
    if not matches:
        return [f"{label}: '{field}: {value}' names none "
                f"of the {count} required bindings ({expected})"]
    v: List[str] = []
    if value[:matches[0].start()].strip():
        v.append(f"{label}: '{field}:' carries text before "
                 f"its first binding ({value[:matches[0].start()].strip()!r}) "
                 f"-- the value is exactly the {count} bindings ({expected})")
    found: Dict[str, str] = {}
    for n, match in enumerate(matches):
        end = matches[n + 1].start() if n + 1 < len(matches) else len(value)
        key = match.group(1)
        if key in found:
            v.append(f"{label}: duplicate '{key}=' binding in "
                     f"'{field}:' -- exactly one is "
                     "required, even when the two agree")
            continue
        found[key] = value[match.end():end].strip().strip(";").strip()
    for key in keys:
        if key not in found:
            v.append(f"{label}: '{field}:' names no "
                     f"'{key}=' binding -- all {count} are required ({expected})")
            continue
        raw = found[key]
        if not raw:
            v.append(f"{label}: empty '{key}=' binding value")
        elif key not in free_text \
                and not _FULL_COMMIT_RE.match(raw.strip("`")):
            v.append(f"{label}: '{key}={raw}' is not a FULL commit id -- the "
                     "binding is 40 lowercase hex digits (an abbreviation can "
                     "collide, and a colliding binding names two commits)")
    if found_out is not None:
        found_out.update(found)
    return v


def _non_expansion_violations(art: Artifact, line_no: int,
                              label: str) -> List[str]:
    """The backstop over the latest Code-review pass of an *inherited* plan.

    Silent for every plan that does not declare inheritance, which today is
    **every plan in this tree** (measured: zero `Inherited proposal basis`
    declarations corpus-wide).  That is the honest state of a rule whose trigger
    P2-R has not yet shipped, and it is exactly the condition under which a rule
    that does nothing is indistinguishable from a rule that works
    (`AGENTS.md` > *Verifying claims*: "a tool that returns success without
    testing the claimed property is a worse defect than no tool, because it is
    silent").  The answer is not to weaken the trigger but to prove the rule
    fires: `bootstrap/tests/test_lifecycle_contract.py` carries synthetic
    inheritance-declaring fixtures that exercise every refusal direction below.

    **Emphasis is stripped from the field scope first**, which is
    `_parse_verdict`'s rule and is applied here for its reason: this tree's house
    form wraps the label *and* the value in one bold span (`**Verdict: SHIP.**`,
    30 of the 38 corpus passes), and the reviewer writing this attestation is the
    same author writing that line four lines above it.  `_VERDICT_CLAUSE_RE`
    likewise tolerates trailing prose after a clause break, but only after one,
    so `VERIFIED but actually NOT VERIFIED` is out of vocabulary and refuses.
    """
    if not _declares_inheritance(art):
        return []
    body = _EMPHASIS_RE.sub("", _code_review_pass_body(art, line_no))
    v: List[str] = []
    owed = (f"an inherited plan (one declaring '{_INHERITANCE_FIELD}:') owes "
            f"the exercised backstop: '{_NON_EXPANSION_FIELD}: "
            f"{' | '.join(_NON_EXPANSION_VALUES)}' plus its "
            f"'{_NON_EXPANSION_BASIS_FIELD}:' line")
    found = _REVIEW_FIELD_RE[_NON_EXPANSION_FIELD].findall(body)
    if not found:
        v.append(f"{label}: missing '{_NON_EXPANSION_FIELD}:' -- {owed}")
    elif len(found) > 1:
        v.append(f"{label}: duplicate '{_NON_EXPANSION_FIELD}:' "
                 f"({len(found)} lines) -- exactly one is required, even when "
                 "the values agree")
    else:
        raw = _VERDICT_CLAUSE_RE.match(found[0]).group(0).strip()
        canonical = next(
            (value for value in _NON_EXPANSION_VALUES
             if raw.casefold() == value.casefold()), None)
        if canonical is None:
            v.append(f"{label}: unrecognized '{_NON_EXPANSION_FIELD}' value: "
                     f"{raw!r} -- the vocabulary is closed "
                     f"({' | '.join(_NON_EXPANSION_VALUES)}) and has no default")
        elif canonical == _NON_EXPANSION_BLOCKING:
            v.append(
                f"{label} attests '{_NON_EXPANSION_FIELD}: "
                f"{_NON_EXPANSION_BLOCKING}', which is BLOCKING: the plan or "
                "implementation introduced an undeclared scope item, invariant, "
                "public path, failure disposition, trust boundary or ceremony. "
                "Inheritance is invalid -- return the change to the proposal "
                "boundary (or obtain the distinct plan review the proposal's "
                "readiness names) before this state.")
    value, problem = _basis_value(body)
    if problem:
        v.append(f"{label}: {problem} -- {owed}, bound as "
                 f"'{_NON_EXPANSION_BASIS_FIELD}: "
                 f"{'; '.join(k + '=<...>' for k in _NON_EXPANSION_BINDINGS)}'")
    else:
        v.extend(_basis_binding_violations(value, label))
    return v


# === P2-R -- plan-readiness inheritance, the two-field shape =================
#
# The accepted `review-efficient-lifecycle` parent, "Standard-path
# plan-readiness inheritance":
#
#     A proposal reviewer may record:
#
#         Plan readiness: READY | DISTINCT REVIEW REQUIRED
#         Basis: <full reviewed proposal commit and complete-current-contract
#                heading>
#
#     `READY` means that exact contract fixes scope and exclusions; invariants;
#     failure dispositions; public paths; omissions; test homes and standing
#     gates; documentation and release-note surfaces; implementation areas and
#     sequence; and any Maintainer fences or ceremonies. ...
#     The Maintainer's Decision binds the same proposal commit without changing
#     its contract. ... A new scope item, invariant, public path, failure
#     disposition, trust boundary, or ceremony invalidates inheritance.  The
#     metadata becomes `required(<tier>)`, and implementation stops until a
#     distinct plan review lands.
#
# FOUR divergences from that text govern this block.  Each comes from a landed,
# append-only section of `dev/plans/review-efficient-lifecycle.md`, and each is
# named here because a reader comparing this code with the accepted proposal
# alone would otherwise read a faithful implementation as a drifted one:
#
# 1. **The plan-side shape is TWO fields, not one** (`## Maintainer-directed
#    contract revision -- 2026-08-11`).  The parent folded the whole fact into
#    the plan-review field -- `Plan review: inherited(<review commit>;
#    proposal=<accepted commit>)`.  That spelling is retired; a plan under the
#    current contract "carries both facts separately":
#
#        Plan review: required(Internal)
#        Inherited proposal basis: review=<full External-review commit>;
#                                    proposal=<full accepted commit>
#
# 2. **The automatic high-assurance refusal is REMOVED** (same section):
#    *"Standard and high-assurance proposals may both receive `READY` when their
#    External review settled the complete contract."*  That is a Maintainer
#    decision, quoted verbatim there.  There is therefore deliberately **no**
#    assurance-path branch below, and re-adding one would restore a refusal the
#    Maintainer removed.
#
# 3. **A SEVENTH trigger** (that plan's 2026-08-11 `## Response to plan
#    review`, Amendment B): *"a scope reduction or removed accepted outcome relative to
#    the proposal's committed scope, absent a Maintainer-recorded `Scope delta`
#    allowance per `AGENTS.md` > Git and commit workflow"*.  The parent's six all
#    guard a translation that ADDS; narrowing was unguarded, and the Internal
#    reviewer's charter ("it does not reopen the accepted design") is exactly the
#    posture in which a quiet narrowing reads as faithful translation.
#
# 4. **Malformed never means READY** (same section, Amendment D): a partial or
#    unparseable `Inherited proposal basis` refuses.
#
# WHICH COMMIT `proposal=` NAMES -- decided rather than left ambiguous.  The
# parent calls it "<accepted commit>", which reads two ways: the commit that
# LANDED the Decision, or the proposal commit the Decision BINDS.  The parent's
# own next sentence settles it -- *"The Maintainer's Decision binds the same
# proposal commit without changing its contract"* -- and only that reading is
# checkable from repository bytes, because a commit cannot contain its own id, so
# a binding to the Decision commit could never be more than a shape.  So
# `proposal=` is the reviewed-and-accepted proposal commit, which every
# conforming `## Review` record already carries as its `Reviewed commit:`, and
# the equality below is what makes the binding *exact* rather than well-formed.
#
# WHY THE PARENT'S `Basis:` LINE ON THE READINESS RECORD IS NOT A THIRD FIELD.
# The parent asks the readiness record to carry "<full reviewed proposal commit
# and complete-current-contract heading>".  Both of those already land as
# mandatory fields of every review record -- `Reviewed commit:` ("full commit
# id") and `Target:` ("complete current-contract section") -- so requiring a
# second spelling of the same two facts would fork a vocabulary, which is the
# defect Chunk A exists to prevent.  The readiness record's basis IS its
# four-field basis.
#
# WHAT IS NOT CHECKED.  Stated where a reader will look for it, because a gate
# whose reach is over-read is worse than a narrow one (`AGENTS.md` > *Verifying
# claims*: a check that returns success without testing the claimed property is
# silent, and silence is the expensive failure):
#
#   * **That `review=` names the commit the External review landed in.**  No
#     repository byte carries it: the review cannot name its own commit, and this
#     block reaches no git at all -- `scan` runs over the whole corpus and a
#     per-artifact `git cat-file` would be both slow and, worse, *silently
#     degrading* wherever git is unavailable (this file's read-only git helper
#     returns `None` on failure, and a gate that quietly stops checking is the
#     same defect class).  `review=` therefore gets shape, uniqueness, full-hex
#     form and distinctness from `proposal=` -- a real invariant, since a review
#     lands *after* the commit it reviews -- and nothing more.  A source fence
#     pins the absence (`test_the_p2_block_reaches_no_git`), so a later widening
#     has to add the reach explicitly rather than arrive by edit.
#   * **Whether the plan's chunks really translate the accepted contract**, in
#     either direction.  Both delta declarations below are AUTHOR DECLARATIONS,
#     exactly as that field requires: *"Semantic triggers are author
#     declarations, not inferences ... the tooling checks that the record exists
#     and binds, never the truth of the classification."*  An UNDECLARED
#     expansion or reduction is invisible here.  For the reduction direction that
#     limit is already doctrine in its own words (`doctrine/dual-review.md` >
#     "The counterweight": *"A formal check could confirm that a declaration
#     exists; it could not confirm that it is true ... would catch forgetting and
#     not evading"*), which is also why an ABSENT or unrecognized `Scope delta`
#     value is not a refusal here.
#   * **That the Internal plan review was performed in a FRESH context.**  No
#     repository byte distinguishes a fresh session from a continued one.

#: The proposal-side declaration, its closed vocabulary, and the tier that may
#: supply it.  `READY` is a finding a proposal REVIEWER records; the plan then
#: names it.  Only an External pass can supply the inherited basis -- the
#: revision's default is "an External proposal review ... records `Plan
#: readiness: READY`", and the required test matrix states the negative directly:
#: *"an Internal proposal review cannot supply the inherited External basis"*.
_PLAN_READINESS_FIELD = "Plan readiness"
_PLAN_READINESS_READY = "READY"
_PLAN_READINESS_DISTINCT = "DISTINCT REVIEW REQUIRED"
_PLAN_READINESS_VALUES = (_PLAN_READINESS_READY, _PLAN_READINESS_DISTINCT)
_PLAN_READINESS_TIER = "External"

#: The two sub-fields of the plan-side declaration, in the revision's order
#: (which is the reported order).  **No free-text member**, unlike the
#: Code-review `Basis:` line's `changed-paths`: both of these are full commit ids.
_INHERITANCE_BINDINGS = ("review", "proposal")
_INHERITANCE_KEY_RE = re.compile(r"\b(review|proposal)=")

#: The fold, for the reason `_BASIS_FOLD_RE` exists: the revision's own rendering
#: of the field wraps, putting `proposal=` on an indented second line, and an
#: author who copies that block verbatim must not be refused by the tool that
#: quotes it.  Indented AND opening with a binding key, so nothing else is
#: swallowed.
_INHERITANCE_FOLD_RE = re.compile(r"^[ \t]+(?:review|proposal)=")

#: The plan-side EXPANSION declaration and the parent's six dimensions, verbatim
#: from *"A new scope item, invariant, public path, failure disposition, trust
#: boundary, or ceremony invalidates inheritance"*.  Header-bounded for the reason
#: `_declares_inheritance` is: this very plan quotes the dimension names in prose,
#: and a whole-text search would fire the gate on the artifact that defines it.
_CONTRACT_EXPANSION_FIELD = "Contract expansion"
_EXPANSION_NONE = "none"
_EXPANSION_DIMENSIONS = ("scope item", "invariant", "public path",
                         "failure disposition", "trust boundary", "ceremony")

#: Amendment B's seventh trigger, expressed in the vocabulary that **already
#: exists** rather than a new one.  `**Scope delta**: preserved | degraded | lost`
#: is the concurrently-landed `scope-reduction-trap` grammar (`doctrine/
#: dual-review.md` > "The outcome test"; both authoring templates and both
#: planner scaffolds already print it), and Amendment B names that exact record
#: as the thing whose allowance admits a reduction.  Inventing a second spelling
#: of "this narrowed" would fork it.
#:
#: **Read whole-text, not header-bounded, and that asymmetry is forced**: the
#: landed grammar places the declaration inside a `### Sharpening` or `##
#: Response` -- the record where a narrowing is decided -- not in the header.
_SCOPE_DELTA_FIELD = "Scope delta"
_SCOPE_DELTA_PRESERVED = "preserved"
_SCOPE_DELTA_REDUCTIONS = ("degraded", "lost")

#: The plan's pointer at the proposal whose readiness it inherits.  Every one of
#: the 41 plans in this tree carries this field (measured 2026-08-12), in half a
#: dozen spellings -- a bare stem, a backticked stem, a backticked path, a
#: markdown link with `../` or `../../`.  Only the *path* spellings resolve, and
#: for an inheritance-declaring plan that is a requirement rather than a
#: limitation: the refusal below says so, and no plan in the tree declares
#: inheritance today.
_SOURCE_PROPOSAL_FIELD = "Source proposal"
_ARTIFACT_FILE_RE = re.compile(r"([A-Za-z0-9][A-Za-z0-9._-]*)\.md")

#: Any markdown heading, for bounding the record a `Scope delta` declaration sits
#: in.  Levels 1-6, because the declaration may sit under an H3 `### Sharpening`.
_ANY_HEADING_RE = re.compile(r"^#{1,6} ")

#: **Amendment D's third shape: a WRONG FIELD NAME.**  A header field whose label
#: speaks of inheriting but is not the exact field name is a *near miss* -- and a
#: near miss here is silent by construction, because a plan that fails to declare
#: inheritance is simply not an inherited plan.  Amendment D requires it to
#: refuse, so it is detected the way a near-miss review heading already is
#: heading: recognize the neighbourhood, then quote the line that did not count.
#: Deliberately keyed on the word `inherit`, which is what every plausible
#: misspelling of this field retains (`Inherited basis`, `Inherited proposal`,
#: `inherited proposal basis` in the wrong case, `Proposal basis inherited`).
_INHERITANCE_NEAR_MISS_RE = re.compile(
    r"^(?:\*\*|__)?(?P<label>[^:\n]*inherit[^:\n]*?)(?:\*\*|__)?:", re.I)

#: The RETIRED parent spelling, refused at the `**Plan review**:` field.  Filed
#: this gap explicitly at P2-R (`test_the_retired_parent_spelling_is_not_the_
#: trigger`: *"Refusing the retired spelling AT the `Plan review:` field is the
#: `Plan review` vocabulary's business (P2-R / Chunk E), not this block's"*), and
#: it is a live bypass rather than a tidiness item: `review_record_violations`
#: evaluates the plan-review floor only for a value beginning `required`, so an
#: author who used the accepted parent's own wording -- `Plan review:
#: inherited(<review commit>; proposal=<accepted commit>)` -- got **no**
#: plan-review obligation checked at all.
_RETIRED_INHERITED_PLAN_REVIEW_RE = re.compile(r"^\s*inherited\s*\(", re.I)

#: The third value the monitoring ledger's `assurance_path` field may
#: carry, and it is NOT an assurance path: it is the resolved fact that a plan
#: declares no inheritance chain, so there is no proposal declaration to inherit.
#: A positive answer, not a default -- the two real tokens stay exactly
#: `ASSURANCE_PATHS`, so no second vocabulary is created.
ASSURANCE_NOT_INHERITED = "not-inherited"


def _dev_root(path: Path) -> Optional[Path]:
    """The `dev/` directory containing this plan, from its own path.

    Walks the parents for a directory named `plans`, so it holds for a live plan
    (`dev/plans/<stem>.md`), an archived one (`dev/plans/archive/<stem>.md`) and
    a fixture under a `tmp_path` root alike -- the property
    `_is_archived_by_location` gets the same way, and for the same reason.
    """
    for parent in path.parents:
        if parent.name == "plans":
            return parent.parent
    return None


def _resolve_source_proposal(art: Artifact
                             ) -> Tuple[Optional[Artifact], Optional[str]]:
    """The plan's source proposal, read from this tree -> ``(art, violation)``.

    Read-only, no globbing, and bounded to the two locations a proposal may live
    in (`dev/proposals/` and `dev/proposals/archive/`).  Every failure direction
    is a *refusal*, never a fallthrough: an unresolvable pointer means the
    inheritance chain cannot be checked, and Amendment D's rule -- never default
    to `READY` -- applies to the whole chain, not only to the field's shape.
    """
    header = "\n".join(_iter_header_lines(art.text))
    found = _REVIEW_FIELD_RE[_SOURCE_PROPOSAL_FIELD].findall(header)
    if not found:
        return None, (
            f"no '**{_SOURCE_PROPOSAL_FIELD}**:' line in the header -- an "
            f"inherited plan's readiness comes from a specific proposal, so the "
            f"pointer at it is what makes the inheritance checkable")
    if len(found) > 1:
        return None, (
            f"duplicate '**{_SOURCE_PROPOSAL_FIELD}**:' ({len(found)} header "
            f"lines) -- two source proposals may disagree about readiness, and "
            f"there is no rule to choose between them")
    names = _ARTIFACT_FILE_RE.findall(found[0])
    if not names:
        return None, (
            f"'**{_SOURCE_PROPOSAL_FIELD}**: {found[0].strip()}' names no "
            f"'<stem>.md' file -- an inherited plan cites its proposal by PATH "
            f"(e.g. `../proposals/archive/<stem>.md`), because a bare stem is "
            f"not resolvable and this chain is checked, not trusted")
    stem = names[0]
    dev = _dev_root(art.path)
    if dev is None:
        return None, (
            f"cannot locate the 'dev/' root from {art.path.name} -- an inherited "
            f"plan must sit under 'dev/plans/' so its proposal can be resolved")
    try:
        for candidate in (dev / "proposals" / f"{stem}.md",
                          dev / "proposals" / "archive" / f"{stem}.md"):
            if candidate.is_symlink():
                return None, (
                    f"{candidate.name} is reached through a symlink -- refusing "
                    f"to resolve an inheritance chain through one")
            if candidate.is_file():
                return _read_artifact(candidate), None
    except OSError as exc:
        return None, (f"cannot resolve the source proposal {stem}.md: {exc} -- "
                      f"an unreadable chain is a refusal, never a pass")
    return None, (
        f"'**{_SOURCE_PROPOSAL_FIELD}**:' names {stem}.md, which is in neither "
        f"'dev/proposals/' nor 'dev/proposals/archive/' -- the inherited "
        f"readiness cannot be read from a proposal that is not there")


def _readiness_records(art: Artifact) -> List[Dict[str, object]]:
    """Every proposal `## Review` record that declares `Plan readiness:`.

    Read from the record's **field scope** (`_record_field_scope`) -- the body
    above the pass's first H3, the same scope every other mandatory field of
    every other record kind is read from, so a readiness line parked under a
    subsection does not count.  Emphasis is stripped first, for the reason
    `_non_expansion_violations` strips it: this tree's house form bolds label and
    value in one span.
    """
    lines = art.text.split("\n")
    boundaries = _record_boundaries(art)
    out: List[Dict[str, object]] = []
    for line_no, raw in _proposal_review_records(art):
        scope = _EMPHASIS_RE.sub(
            "", _record_field_scope(lines, line_no, boundaries))
        values = [v.strip() for v in
                  _REVIEW_FIELD_RE[_PLAN_READINESS_FIELD].findall(scope)]
        if not values:
            continue
        tier, _problem = _parse_one_field(
            scope, _REVIEW_FIELD_RE["Tier"], _TIERS, "Tier")
        commits = [c.strip().strip("`") for c in
                   _REVIEW_FIELD_RE["Reviewed commit"].findall(scope)]
        out.append({"line": line_no, "heading": raw.strip(), "values": values,
                    "tier": tier, "commits": commits})
    return out


def _canonical_readiness(raw: str) -> Optional[str]:
    """One readiness value against the closed vocabulary, or ``None``.

    Case-insensitive and tolerant of a trailing clause after a break character
    (`_VERDICT_CLAUSE_RE`'s rule), because the reviewer writing this line is the
    same author writing `**Verdict: SHIP.**` -- but only *after* a break, so
    `READY but actually DISTINCT REVIEW REQUIRED` is out of vocabulary and
    refuses rather than parsing as `READY`.
    """
    clause = _VERDICT_CLAUSE_RE.match(raw).group(0).strip()
    for canonical in _PLAN_READINESS_VALUES:
        if clause.casefold() == canonical.casefold():
            return canonical
    return None


def plan_readiness_violations(art: Artifact) -> List[str]:
    """P2-R -- the proposal-side `Plan readiness:` declaration's SHAPE.

    Public because both gate surfaces consume it, the rule the two predicates
    already follow: wiring only `scan` leaves `next` presence-only, and the loose
    surface is the one an author drives.

    Shape only: presence is optional (a reviewer *may* record readiness -- the
    parent's word), a duplicate within one record refuses, and a value outside
    the closed vocabulary refuses.  Whether `READY` is *warranted* is the
    reviewer's judgement and no scanner's.
    """
    if art.kind != "proposal" or _is_immutable(art):
        return []
    v: List[str] = []
    for rec in _readiness_records(art):
        label = f"'{rec['heading']}'"
        values = rec["values"]
        if len(values) > 1:
            v.append(
                f"{label}: duplicate '{_PLAN_READINESS_FIELD}:' "
                f"({len(values)} lines) -- exactly one is required, even when "
                f"the values agree; a derived plan inherits ONE finding")
            continue
        if _canonical_readiness(values[0]) is None:
            v.append(
                f"{label}: unrecognized '{_PLAN_READINESS_FIELD}' value: "
                f"{values[0]!r} -- the vocabulary is closed "
                f"({' | '.join(_PLAN_READINESS_VALUES)}) and has NO default; an "
                f"unreadable finding cannot be read as '{_PLAN_READINESS_READY}'")
    return v


def _declared_expansion(art: Artifact) -> Tuple[List[str], List[str]]:
    """The plan header's `Contract expansion:` -> ``(dimensions, violations)``.

    Absent is legal and yields ``([], [])`` -- the contract's words are *"any
    **declared** expansion refuses"*, and a mandatory third field is not what the
    revision specified.  Present-but-unreadable is a violation, because a
    declaration nobody can parse is the one shape that must not buy silence.
    """
    header = "\n".join(_iter_header_lines(art.text))
    found = _REVIEW_FIELD_RE[_CONTRACT_EXPANSION_FIELD].findall(header)
    if not found:
        return [], []
    if len(found) > 1:
        return [], [f"duplicate '**{_CONTRACT_EXPANSION_FIELD}**:' "
                    f"({len(found)} header lines) -- exactly one is required, "
                    f"even when the values agree"]
    raw = _strip_emphasis_chars(found[0]).strip()
    if not raw:
        return [], [f"empty '**{_CONTRACT_EXPANSION_FIELD}**:' value -- omit the "
                    f"line entirely when the translation added nothing, or name "
                    f"'{_EXPANSION_NONE}' explicitly; a present-but-empty field "
                    f"declares neither"]
    if raw.casefold() == _EXPANSION_NONE:
        return [], []
    named: List[str] = []
    unknown: List[str] = []
    for token in raw.split(";"):
        token = token.split("--")[0].strip().rstrip(".").strip()
        if not token:
            continue
        match = next((d for d in _EXPANSION_DIMENSIONS
                      if token.casefold() == d or token.casefold() == d + "s"),
                     None)
        if match is None:
            unknown.append(token)
        else:
            named.append(match)
    if unknown:
        return named, [
            f"'**{_CONTRACT_EXPANSION_FIELD}**:' names {unknown!r}, which is "
            f"outside the declared dimensions ({' | '.join(_EXPANSION_DIMENSIONS)}"
            f" | {_EXPANSION_NONE}) -- an unrecognized dimension is refused, not "
            f"ignored, because ignoring it is how an expansion becomes invisible"]
    return named, []


def _declaration_record(lines: List[str], index: int) -> str:
    """The heading-bounded region containing line *index* (0-based).

    "The record the declaration sits in" made concrete: from the nearest
    preceding markdown heading through the line before the next one.  That is
    where the landed `Scope delta` grammar puts the whole block -- the
    declaration, its `Removed scope` list, its `Disposition/home` line -- so it
    is also where a quoted Maintainer allowance for it must sit.
    """
    start = 0
    for i in range(index, -1, -1):
        if _ANY_HEADING_RE.match(lines[i]):
            start = i
            break
    end = len(lines)
    for j in range(index + 1, len(lines)):
        if _ANY_HEADING_RE.match(lines[j]):
            end = j
            break
    return "\n".join(lines[start:end])


def _declared_reduction(art: Artifact) -> List[Tuple[int, str, bool]]:
    """Every `Scope delta:` declaring a REDUCTION -> ``(line, value, allowed)``.

    *allowed* is Amendment B's *"Maintainer-recorded ... allowance"* made
    structural: the record carrying the declaration also carries a
    visually-isolated authorization blockquote -- the identical idiom, and the
    identical predicate (`_has_isolated_blockquote`), that a `## Decision` uses
    for the Maintainer's verbatim words under `AGENTS.md`'s scribing guard-rail.
    As there, the tool attests **structure, never authenticity**: the
    committing operator remains the guarantor that the quoted words were said.

    A `preserved`, absent, or unrecognized value yields nothing.  That is not an
    oversight -- it is `doctrine/dual-review.md` > "The counterweight" applied
    verbatim (*"No tool refuses a transition on a missing or malformed
    declaration"*), and it keeps a scaffolded plan carrying the template's own
    unfilled `preserved | degraded | lost` prompt from refusing.
    """
    lines = _split_lines(art.text)
    pattern = _REVIEW_FIELD_RE[_SCOPE_DELTA_FIELD]
    out: List[Tuple[int, str, bool]] = []
    for i, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        raw = _strip_emphasis_chars(match.group("value")).strip().rstrip(".")
        value = next((r for r in _SCOPE_DELTA_REDUCTIONS
                      if raw.casefold() == r), None)
        if value is None:
            continue
        out.append((i + 1, value,
                    _has_isolated_blockquote(_declaration_record(lines, i))))
    return out


def plan_inheritance_violations(art: Artifact) -> List[str]:
    """P2-R -- the whole inheritance chain over one plan.  **Refusal-first.**

    Silent for every plan that does not declare inheritance, which today is
    **every plan in this tree** (measured 2026-08-12: zero of 94 artifacts carry
    a header `Inherited proposal basis:`).  The trigger is `_declares_inheritance`
    -- deliberately the *same* predicate, so the two meet at one key
    rather than at two spellings of "this plan is inherited".

    Every direction below is a refusal and **none defaults to `READY`**
    (Amendment D).  The order is: the field's own shape first, because with an
    unparseable binding there is nothing left to compare; then the plan's own
    plan-review declaration; then the chain out to the proposal; then the two
    delta declarations.
    """
    if art.kind != "plan":
        return []
    v: List[str] = []
    # The retired spelling, refused UNCONDITIONALLY -- it is not gated on the
    # trigger below, because its whole hazard is that it *replaces* the trigger.
    if _RETIRED_INHERITED_PLAN_REVIEW_RE.match(art.plan_review):
        v.append(
            f"'**Plan review**: {art.plan_review.strip()}' uses the RETIRED "
            f"spelling from the accepted parent.  The 2026-08-11 "
            f"Maintainer-directed revision split that one field in two: write "
            f"'**Plan review**: required(Internal)' AND "
            f"'**{_INHERITANCE_FIELD}**: "
            f"{'; '.join(k + '=<full commit>' for k in _INHERITANCE_BINDINGS)}'. "
            f"Left as written this declares NO plan-review obligation at all -- "
            f"the floor is evaluated only for a 'required(...)' value -- so the "
            f"retired spelling silently buys a plan no independent read.")
    if not _declares_inheritance(art):
        # Amendment D's wrong-field-name shape.  Only reached when the exact
        # field is absent, so a correct declaration can never be reported as its
        # own near miss.
        for line in _iter_header_lines(art.text):
            match = _INHERITANCE_NEAR_MISS_RE.match(line.strip())
            if match is None:
                continue
            v.append(
                f"header line {line.strip()!r} names a field that speaks of "
                f"inheriting but is not the exact "
                f"'**{_INHERITANCE_FIELD}**:' -- a near miss declares nothing, "
                f"and this one is reported rather than ignored because Amendment "
                f"D requires a wrong field name to REFUSE, never to read as "
                f"'{_PLAN_READINESS_READY}'.  Correct the spelling, or delete "
                f"the line if this plan takes a distinct plan review.")
        return v
    label = f"'**{_INHERITANCE_FIELD}**:'"
    never = ("; a malformed or partial declaration REFUSES and never defaults "
             f"to '{_PLAN_READINESS_READY}'")
    header = "\n".join(_iter_header_lines(art.text))
    value, problem = _basis_value(header, field=_INHERITANCE_FIELD,
                                  fold_re=_INHERITANCE_FOLD_RE)
    if problem:
        return v + [f"{problem} -- an inherited plan declares "
                    f"'{_INHERITANCE_FIELD}: "
                    f"{'; '.join(k + '=<full commit>' for k in _INHERITANCE_BINDINGS)}'"
                    + never]
    bindings: Dict[str, str] = {}
    shape = _basis_binding_violations(
        value, label, field=_INHERITANCE_FIELD, keys=_INHERITANCE_BINDINGS,
        key_re=_INHERITANCE_KEY_RE, free_text=(), found_out=bindings)
    if shape:
        return v + [s + never for s in shape]
    review_sha = bindings["review"].strip("`")
    proposal_sha = bindings["proposal"].strip("`")
    if review_sha == proposal_sha:
        v.append(
            f"{label} binds review= and proposal= to the SAME commit "
            f"({review_sha[:12]}) -- an External review lands after the commit "
            f"it reviews, so one commit cannot be both; one of the two bindings "
            f"is wrong")
    # The revision's own shape: `Plan review: required(Internal)` **and** the
    # inheritance field.  Inheritance reallocates the plan review from External
    # to Internal; it never removes it, so `not required(...)` beside an
    # inheritance declaration is the one combination that would buy a plan no
    # independent read at all.
    if not art.plan_review.lower().startswith("required"):
        v.append(
            f"a plan declaring '{_INHERITANCE_FIELD}:' also declares "
            f"'**Plan review**: required(Internal)'"
            f" -- inheritance REALLOCATES the plan review to a fresh-context "
            f"Internal pass, it does not remove it, and "
            f"{art.plan_review.strip()!r} would leave the plan with no "
            f"independent read")
    proposal, problem = _resolve_source_proposal(art)
    if problem:
        return v + [problem + never]
    records = _readiness_records(proposal)
    where = f"{proposal.path.name}"
    if not records:
        return v + [
            f"{where} records no '{_PLAN_READINESS_FIELD}:' in any '## Review' "
            f"-- inheritance rests on a reviewer's explicit finding, and an "
            f"absent finding is not '{_PLAN_READINESS_READY}'" + never]
    # The LAST declaring record is operative.  A later review supersedes an
    # earlier one (the parent: "A later review does not silently inherit an
    # earlier" basis), so resurrecting an early `READY` after a later pass is
    # exactly what this ordering forbids.
    rec = records[-1]
    at = f"{where} '{rec['heading']}'"
    values = rec["values"]
    if len(values) > 1:
        return v + [f"{at} declares '{_PLAN_READINESS_FIELD}:' {len(values)} "
                    f"times -- a derived plan inherits ONE finding, and "
                    f"agreement is not a judgement this chain may make" + never]
    canonical = _canonical_readiness(values[0])
    if canonical is None:
        return v + [f"{at} declares an unrecognized "
                    f"'{_PLAN_READINESS_FIELD}' value {values[0]!r} -- the "
                    f"vocabulary is closed "
                    f"({' | '.join(_PLAN_READINESS_VALUES)})" + never]
    if canonical == _PLAN_READINESS_DISTINCT:
        return v + [
            f"{at} declares '{_PLAN_READINESS_FIELD}: "
            f"{_PLAN_READINESS_DISTINCT}' -- that finding is the reviewer saying "
            f"consequential design remains for planning, so this plan takes a "
            f"DISTINCT plan review at the tier the proposal/Decision names and "
            f"cannot inherit.  A fresh-context Internal pass does not satisfy it."]
    if rec["tier"] != _PLAN_READINESS_TIER:
        v.append(
            f"{at} declares '{_PLAN_READINESS_FIELD}: {_PLAN_READINESS_READY}' "
            f"at tier {rec['tier']!r} -- only an {_PLAN_READINESS_TIER} proposal "
            f"review can supply the inherited basis, because what is being "
            f"inherited IS the different-agent-type read")
    commits = rec["commits"]
    if len(commits) != 1:
        v.append(
            f"{at} carries {len(commits)} readable 'Reviewed commit:' values -- "
            f"the accepted-proposal binding is checked against exactly one, and "
            f"P1 already requires exactly one of every review record")
    elif commits[0] != proposal_sha:
        v.append(
            f"{label} binds proposal={proposal_sha} but {at} reviewed "
            f"{commits[0]!r} -- the binding must name the EXACT proposal commit "
            f"whose contract the readiness finding fixed (the Decision binds "
            f"that same commit without changing it), so a mismatch means the "
            f"plan inherits readiness for bytes nobody declared ready")
    dimensions, problems = _declared_expansion(art)
    v.extend(problems)
    if dimensions:
        v.append(
            f"the plan declares '**{_CONTRACT_EXPANSION_FIELD}**: "
            f"{'; '.join(dimensions)}' -- a new "
            f"{' / '.join(_EXPANSION_DIMENSIONS)} INVALIDATES inheritance.  "
            f"Return the change to the proposal boundary, or set '**Plan "
            f"review**: required(<tier>)', drop the "
            f"'{_INHERITANCE_FIELD}:' line and land a distinct plan review "
            f"before implementation continues.")
    for line_no, reduction, allowed in _declared_reduction(art):
        if allowed:
            continue
        v.append(
            f"line {line_no} declares '**{_SCOPE_DELTA_FIELD}**: {reduction}' "
            f"with no Maintainer allowance in that record -- accepted scope is a "
            f"FLOOR, so a removed or partly-delivered accepted outcome "
            f"invalidates inheritance exactly as a new one does (Amendment B).  "
            f"A reviewer cannot create that authority by calling the remainder "
            f"'out of scope': record the Maintainer's verbatim allowance as an "
            f"isolated blockquote in the same record, beside the grouped "
            f"'Removed scope' entry and its 'Disposition/home'.")
    return v


def resolve_plan_assurance_path(path: Path) -> Tuple[Optional[str], List[str]]:
    """The assurance path a PLAN carries, through the inheritance chain.

    Returns ``(value, [])`` where *value* is one of `ASSURANCE_PATHS` or
    `ASSURANCE_NOT_INHERITED`, or ``(None, problems)``.  **Never guesses**: a plan
    that declares inheritance whose chain does not resolve yields `None` and the
    reasons, so the caller refuses loudly instead of recording a default.

    This exists because a plan has no artifact-level assurance declaration of its
    own -- that absence is pinned deliberately
    (`test_a_plan_carries_no_artifact_level_declaration`: *"the plan carries the
    inheritance metadata instead"*) -- so the only honest way to answer "what
    assurance path did this plan run under" is to follow the chain to the
    proposal that declared one.  `tools/lifecycle.py`'s monitoring report is the
    caller, and it reaches this function through the same contained loader it
    reads `PLAN_STATES` through, so no second vocabulary is created.
    """
    try:
        art = _read_artifact(path)
    except (PlannerError, OSError) as exc:
        return None, [f"cannot read {path.name}: {exc}"]
    if art.kind != "plan":
        return None, [f"{path.name} is not a plan -- only a plan inherits an "
                      f"assurance path"]
    if not _declares_inheritance(art):
        return ASSURANCE_NOT_INHERITED, []
    problems = plan_inheritance_violations(art)
    if problems:
        return None, problems
    proposal, problem = _resolve_source_proposal(art)
    if problem:
        return None, [problem]
    header = "\n".join(_iter_header_lines(proposal.text))
    value, problem = _parse_one_field(
        header, _REVIEW_FIELD_RE["Assurance path"], ASSURANCE_PATHS,
        "Assurance path")
    if value is None:
        return None, [f"{proposal.path.name}: {problem} -- a plan's assurance "
                      f"path is INHERITED from its proposal's declaration, and "
                      f"there is no default"]
    return value, []


# === the complete current contract and its withdrawal ledger ==================
#
# The accepted `review-efficient-lifecycle` parent, "Bounded current contracts"
# (`dev/proposals/archive/2026-08-10-codex-review-efficient-lifecycle.md`,
# Revision 1 -- the operative revision; no later section replaces it):
#
#     After a proposal review Response, the author appends one complete current
#     contract containing scope, exclusions, invariants, failure dispositions,
#     public paths, evidence, omissions, deferred work, and the heading below:
#
#         ### Withdrawn / superseded commitments
#         * <earlier commitment, replacement or withdrawal, and reason>
#
#     The heading is mandatory even when its value is `None`.  A reviewer
#     compares the complete revision to the previously reviewed contract and
#     verifies this ledger.  The newest reviewed complete revision is operative
#     for Decision and implementation; all earlier sections remain immutable
#     history.
#
# TWO obligations, and they are checked separately because they fail separately:
#
#   A. a proposal that carries a `## Response` carries a complete current-contract
#      revision at all; and
#   B. every such revision carries the ledger heading, with a written value.
#
# WHY B IS PER-REVISION AND A IS NOT PAIRED PER-RESPONSE.  The contract attaches
# the heading to the revision -- "one complete current contract ... and the
# heading below" -- so B is a property of each revision and is checked there.  A
# is deliberately *not* a 1:1 Response-to-revision pairing, and that restraint is
# measured rather than lazy: across the 39 proposals in this tree that carry a
# revision, the revision sits ABOVE its Response in 6 of them and below in the
# rest (the proposal template's own instruction is *"write a short `## Revised
# proposal` section above this"*), and the counts diverge -- `resp=2 rev=1` is the
# single most common shape.  The contract fixes neither an order nor a ratio, so a
# per-Response pairing rule would be this checker inventing a contract clause,
# which is the drift `AGENTS.md` > *Verifying claims* forbids in the other
# direction.  Position-agnostic presence is what the accepted text supports.
#
# WHAT IS NOT CHECKED, stated where a reader will look for it, because a gate
# whose reach is over-read is worse than a narrow one:
#
#   * **That the contract is COMPLETE.**  Whether the revision really states
#     scope, exclusions, invariants, failure dispositions, public paths, evidence,
#     omissions and deferred work is a reading, not a pattern.  The contract
#     assigns it: *"A reviewer compares the complete revision to the previously
#     reviewed contract."*
#   * **That the ledger is TRUE.**  A revision that silently drops a commitment
#     and writes `* None` passes here.  The ledger's job is to make a drop
#     *visible to the reviewer who compares*; no scanner can compare two prose
#     contracts, and pretending otherwise would be the silent tool.
#   * **Which revision is operative.**  "Newest reviewed" depends on which
#     revision a review pass read, which no repository byte records.
#
# GRANDFATHERING IS `_is_immutable`, AND NEEDS NO ENUMERATION.  Measured at this
# chunk's implementation parent (`6f2b01c`): 53 proposals carry a `## Response` or
# a revision section, 1 carries the ledger, and **all 52 that do not are already
# immutable** -- 51 by archive location and `2026-08-11-claude-metrics-events-not-
# prose.md` by its terminal `accepted` status.  The 15 archived proposals with a
# Response and no revision section at all are likewise immutable to the last one.
# So unlike its siblings, this obligation ships with **no legacy manifest**: there is
# nothing live for one to hold, and a manifest with no entries is a maintenance
# burden pretending to be a control.  The consequence is that the live trigger set
# is EMPTY, which is why every refusal below is proven on a synthetic fixture and
# `test_the_live_corpus_owes_no_ledger_today` records the emptiness as a
# measurement that reddens the day it stops being true.


#: A real (unfenced) ATX heading: hashes at column 0, then the text.  Column 0 is
#: markdown's own rule and it is load-bearing here -- both authoring templates
#: teach every field and heading in a 4-space indented block, which is a code
#: block, not a heading, so the scaffold cannot satisfy the requirement it
#: teaches.
_ATX_HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})[ \t]+(?P<text>.*?)[ \t]*$")

#: The two H2 record kinds this block reads, matched on the NORMALIZED heading
#: text (emphasis stripped, ASCII whitespace collapsed, casefolded) rather than on
#: raw bytes, because the corpus writes both separators -- `## Response -- <author>
#: (author) -- <date>` and the same line with em-dashes are the same record kind,
#: and an em-dash is not a contract difference.
#:
#: `Response` covers every live spelling -- `## Response`, `## Response to review`,
#: `## Response to the External security review` (measured: 30 distinct heading
#: lines across the corpus, all of them opening with the word).  `Revised
#: proposal|Revision` likewise covers all 39 revision headings, including
#: `## Revised proposal, round 3 -- ...` and `## Revision after the
#: direction -- ...`.  Word-anchored, so `## Revisiting the loader` is not a
#: revision.
_RESPONSE_NORM_RE = re.compile(r"response\b")
_CURRENT_CONTRACT_NORM_RE = re.compile(r"(?:revised proposal|revision)\b")

#: The ledger heading, exactly as the accepted contract prints it, and the H3
#: level it prints it at.
_LEDGER_HEADING = "Withdrawn / superseded commitments"
_LEDGER_LEVEL = 3

#: Whitespace around the slash is normalized away before the comparison, so
#: `### Withdrawn/superseded commitments` conforms.  Tolerant on FORMATTING,
#: strict on WORDS and LEVEL: a word variant or a wrong level is reported as a
#: near miss with the offending line quoted, never silently
#: accepted and never left as a bare "missing" for the author to guess at.
_LEDGER_SLASH_RE = re.compile(r"[ \t]*/[ \t]*")

#: The near-miss key: the two words every plausible misspelling of this heading
#: retains.  Same trick as `_INHERITANCE_NEAR_MISS_RE` -- recognize the
#: neighbourhood, then quote the heading that did not count.
_LEDGER_NEAR_MISS_WORDS = ("withdrawn", "superseded")

#: The ledger's VALUE, one of two shapes: a written `None`, or at least one
#: entry.  A bare heading refuses -- `_has_disposition_attestation` closed exactly
#: this defect for the archive block (*"An empty label refuses -- which is what
#: the previous predicate accepted"*), and the contract's own words are that the
#: heading is mandatory *even when its value is `None`*, which requires the value
#: to be written rather than inferred from silence.
#:
#: Read over the span's lines with fence DELIMITERS skipped but fenced content
#: kept, which is the opposite tolerance from the heading search above and is the
#: safe direction for each: a heading inside a fence must not CLEAR the
#: requirement, while a real ledger a plan-author column-aligned inside a fence
#: must not FAIL it (`_mask_examples` records two archived records that do exactly
#: that).
_LEDGER_NONE_RE = re.compile(r"^[ \t]*(?:[-*+][ \t]+)?(?:\*\*|__)?none\b", re.I)
_LEDGER_ENTRY_RE = re.compile(r"^[ \t]*(?:[-*+][ \t]+|\d+[.)][ \t]+)\S")


def _iter_unfenced_lines(text: str):
    """``(line_no, line)`` for every line OUTSIDE a fenced code block.

    A ``###`` inside a ```` ``` ````/``~~~`` fence is literal text, not a heading
    -- markdown's own rule -- and finding headings is this block's whole job.  It
    matters for a measured reason rather than a theoretical one: the accepted
    contract quotes the ledger heading inside a ```text fence **in the same
    section as its real one**, and both authoring templates now quote it too.  A
    raw search would read the specification as the record: a false CLEAR, which is
    the silent-tool defect `AGENTS.md` > *Verifying claims* names.

    **Deliberately not folded into `_has_isolated_blockquote`**, which walks
    fences with its own loop.  That predicate's `prev_blank` state machine treats
    the fence *delimiter* as a non-blank line, which a caller-side iterator cannot
    express, and rewriting a Decision-gating predicate is not this chunk's cell.
    """
    in_fence = False
    for i, line in enumerate(_split_lines(text)):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield i + 1, line


def _heading_records(text: str) -> List[Tuple[int, int, str, str]]:
    """``(line_no, level, raw_heading, normalized_text)`` per real heading.

    Read off the raw lines rather than `art.sections`, for two reasons that both
    bite: `_parse_sections` filters on `_KNOWN_KINDS`, which does not contain
    `revision`, so `## Revision 1 -- complete current contract` parses to nothing
    at all; and it is not fence-aware.  `_proposal_review_records` reads raw lines
    for the same class of reason.
    """
    out: List[Tuple[int, int, str, str]] = []
    for line_no, line in _iter_unfenced_lines(text):
        m = _ATX_HEADING_RE.match(line)
        if m is None:
            continue
        norm = _ASCII_WS_RE.sub(
            " ", _strip_emphasis_chars(m.group("text"))).strip().casefold()
        out.append((line_no, len(m.group("hashes")), line.strip(), norm))
    return out


def _is_ledger_heading(level: int, norm: str) -> bool:
    """True for a conforming ledger heading: H3, and the exact word sequence."""
    return (level == _LEDGER_LEVEL
            and _LEDGER_SLASH_RE.sub(" / ", norm) == _LEDGER_HEADING.casefold())


def _is_ledger_near_miss(norm: str) -> bool:
    """True for a heading in the ledger's neighbourhood that did not conform."""
    return all(word in norm for word in _LEDGER_NEAR_MISS_WORDS)


def _span_end(headings: List[Tuple[int, int, str, str]],
              line_no: int, level: int, floor: int) -> int:
    """The first line AFTER *line_no* that closes a heading's span.

    Closed by the next real heading of equal-or-shallower depth, or by *floor*
    (the enclosing span's end).  Same rule `_parse_sections` uses for bodies, on
    the fence-aware heading list.
    """
    for other_line, other_level, _raw, _norm in headings:
        if other_line > line_no and other_level <= level:
            return min(other_line, floor)
    return floor


def _ledger_value_is_written(text: str, start: int, end: int) -> bool:
    """True when the ledger's span carries a written value: `None`, or an entry.

    Fence delimiters are skipped and fenced content is kept -- the tolerance
    `_LEDGER_NONE_RE` documents.
    """
    for line in _split_lines(text)[start:end - 1]:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            continue
        if _LEDGER_NONE_RE.match(line) or _LEDGER_ENTRY_RE.match(line):
            return True
    return False


def current_contract_violations(art: Artifact) -> List[str]:
    """The complete current-contract revision and its withdrawal ledger.

    Public because **both** gate surfaces consume it, the rule the sibling
    predicates already follow: wiring only `scan` leaves `next` presence-only, and
    the loose surface is the one an author drives.

    Silent for a plan (the contract's next paragraph gives the plan the opposite
    rule -- *"Its appended Response is a finding-disposition table that ... does
    not reproduce replacement cells in an amendment ledger"*), silent for an
    immutable proposal, and silent for a proposal with no Response yet: the
    obligation arrives with the Response, which is the transition that lands the
    revision.
    """
    if art.kind != "proposal" or _is_immutable(art):
        return []
    headings = _heading_records(art.text)
    responses = [(n, raw) for n, lvl, raw, norm in headings
                 if lvl == 2 and _RESPONSE_NORM_RE.match(norm)]
    if not responses:
        return []
    revisions = [(n, raw) for n, lvl, raw, norm in headings
                 if lvl == 2 and _CURRENT_CONTRACT_NORM_RE.search(norm)]
    if not revisions:
        return [
            f"'{responses[-1][1]}' has landed but the proposal carries no "
            f"complete current-contract revision -- after a proposal review "
            f"Response the author appends ONE complete current contract (scope, "
            f"exclusions, invariants, failure dispositions, public paths, "
            f"evidence, omissions, deferred work) as a '## Revised proposal' or "
            f"'## Revision <n>' section, because the newest reviewed complete "
            f"revision is what the Decision and the implementation bind.  A "
            f"Response that disposes findings without restating the contract "
            f"leaves the next reviewer to reassemble it from the history, which "
            f"is the repeated reading this contract exists to remove."]
    lines_total = len(_split_lines(art.text)) + 1
    v: List[str] = []
    for line_no, raw in revisions:
        end = _span_end(headings, line_no, 2, lines_total)
        found = [(n, lvl, h, norm) for n, lvl, h, norm in headings
                 if line_no < n < end]
        conforming = [(n, h) for n, lvl, h, norm in found
                      if _is_ledger_heading(lvl, norm)]
        if len(conforming) > 1:
            v.append(
                f"'{raw}': duplicate '### {_LEDGER_HEADING}' "
                f"({len(conforming)} headings, lines "
                f"{', '.join(str(n) for n, _h in conforming)}) -- one complete "
                f"contract carries ONE ledger; two cannot both be the complete "
                f"account of what this revision withdrew.")
            continue
        if not conforming:
            # The heading that CLOSED the span is a near-miss candidate too, and
            # it is the most likely mistake of all: `## Withdrawn / superseded
            # commitments` written at H2 both misses the level AND terminates the
            # revision it was meant to sit inside, so without this the author gets
            # a bare "missing" for a heading they can see on the page.
            closer = [(n, lvl, h, norm) for n, lvl, h, norm in headings
                      if n == end]
            near = [h for n, lvl, h, norm in found + closer
                    if _is_ledger_near_miss(norm) and not _is_ledger_heading(
                        lvl, norm)]
            hint = ("" if not near else
                    "  The nearest heading is " + "; ".join(
                        repr(h) for h in near) + f", which does not count: the "
                    f"ledger is an H3 ('### ') and its wording is exact.")
            v.append(
                f"'{raw}': no '### {_LEDGER_HEADING}' heading -- the ledger is "
                f"MANDATORY in every complete current-contract revision, and the "
                f"heading is required EVEN WHEN its value is 'None'.  Append "
                f"'### {_LEDGER_HEADING}' with one bullet per earlier commitment "
                f"(the replacement or withdrawal, and the reason), or a single "
                f"'* None'.  A revision that quietly drops a commitment is the "
                f"failure this ledger exists to make visible to the reviewer who "
                f"compares it with the previously reviewed contract." + hint)
            continue
        ledger_line = conforming[0][0]
        ledger_end = _span_end(headings, ledger_line, _LEDGER_LEVEL, end)
        if not _ledger_value_is_written(art.text, ledger_line, ledger_end):
            v.append(
                f"'{raw}': '### {_LEDGER_HEADING}' at line {ledger_line} carries "
                f"no written value -- the heading is mandatory even when the "
                f"value is 'None', which means 'None' is WRITTEN rather than "
                f"inferred from an empty section.  Give it one bullet per "
                f"withdrawn or superseded commitment, or a single '* None'.")
    return v


def review_record_violations(art: Artifact,
                             effective_state: Optional[str] = None
                             ) -> List[str]:
    """S1-S9 plus the Code-review record over one artifact.  **The one
    predicate (S12).**

    Both gate call sites -- ``_conformance_violations`` and
    ``_gating_preconditions`` -- go through this function, so the two cannot
    drift into disagreeing about the same record.  A pass that fails the grammar is
    **neither a pass nor a violation**: it can no longer clear anything, because
    clearing requires a grammar match, and near misses therefore fail closed as
    "no conforming pass has landed" rather than as "a pass with problems".

    *effective_state* is the state being asserted, **explicitly**: the
    current status for `scan`, the requested target for `next`/closeout.  It
    decides only the Code-review half; the Plan-review half is decided by the
    plan's own declaration.  `None` means "the artifact's current status", which
    is the conformance reading.

    **Two halves, two different keys, and that asymmetry is the finding.**
    Plan-review obligations are evaluated only when the plan declares
    `required(...)`; Code-review obligations are evaluated whenever the effective
    state is archive-effective, *regardless* of that declaration.  Keying the
    Code-review half on the declaration is the bypass review executed: a plan
    declaring `Plan review: not required(doc-only)` never reached this predicate
    at all, so deleting the weak `_has_kind` presence check would have made such
    a plan archive **clean**.
    """
    stem = art.path.stem
    state = art.status if effective_state is None else effective_state
    required, tier_violation = normalize_required_tier(art.plan_review)
    obligations, obligation_violation = normalize_required_obligations(
        art.plan_review)
    plan_review_required = art.plan_review.lower().startswith("required")
    v: List[str] = []
    if state in CODE_REVIEW_EFFECTIVE_STATES:
        v.extend(_code_review_violations(art))
    if not plan_review_required:
        return v
    if tier_violation:
        v.append(f"'**Plan review**:' {tier_violation}")
    if obligation_violation and obligation_violation != tier_violation:
        # A `+` declaration whose clauses cannot be resolved is reported
        # once against the DECLARATION.  It also leaves `obligations` empty, so
        # nothing below can clear a floor whose shape is unknown.
        v.append(f"'**Plan review**:' {obligation_violation}")
    # "`Plan review: required(A + B)` means two obligations and two
    # distinct review passes."  The one-obligation schema is unchanged, so the
    # per-pass `**Obligation**:` binding is required only under a `+`.
    multi = len(obligations) > 1
    cleared: Dict[str, bool] = {clause: False for clause, _tier in obligations}

    seen: Dict[str, int] = {}
    grandfathered = False
    immutable = _is_immutable(art)
    lines = art.text.split("\n")
    boundaries = _record_boundaries(art)
    for sec, dig in _pass_headings(art):
        seen[dig] = seen.get(dig, 0) + 1
        # THE GRAMMAR IS CHECKED BEFORE THE LEGACY FENCE, and the order is load-bearing.
        # The enumeration exempts a pass from Tier, Findings and disposition --
        # never from the grammar.  With the fence first, an exemption keyed on the heading
        # swallows the date contract, which is exactly how the replaced dated
        # epoch failed: `0000-00-00` sorts before every epoch, so the
        # impossible value bought the exemption *and* silenced the
        # malformed-date violation.  Checking the grammar first leaves no fence,
        # present or future, able to swallow it.
        ok_date, date_violation = _parse_pass_date(sec.date)
        if date_violation:
            v.append(f"'{sec.kind} -- {sec.name}': {date_violation}")
        # The four-field basis, checked BEFORE the `_LEGACY_PASSES` fence
        # below and against its OWN enumeration, for the same reason the grammar is.
        # `_LEGACY_PASSES` exempts the three field checks only; every pass this
        # requirement newly reaches already satisfies them, so letting that
        # fence's `continue` swallow the basis check would weaken the gate for
        # those records while looking like grandfathering.
        if not immutable and not _is_legacy(stem, dig, seen,
                                            _LEGACY_UNDECLARED_BASIS):
            v.extend(_review_basis_violations(
                _record_field_scope(lines, sec.line_no, boundaries),
                f"'{sec.kind} -- {sec.name} -- {sec.date}'"))
        if _is_legacy(stem, dig, seen):
            # Exempt from the three field checks; satisfies the floor by presence, as the
            # Maintainer accepted these records before the schema existed.
            #
            # **And it satisfies the floor AS A WHOLE, including a `+` floor.**
            # Measured, not assumed: three archived plans declare
            # `required(External + External Security Review)` with no
            # `**Obligation**:` line anywhere -- `api-web-security-modules`,
            # `release-security-orchestration`,
            # `verification-evidence-boundaries` -- and every one of their passes
            # is admitted by `_LEGACY_PASSES`.  Requiring the new binding of them
            # would red three immutable artifacts that are green today, for a
            # field that cannot be added to a record nobody may edit.  The contract assigns
            # exactly this population to migration, not here: *"Existing
            # multi-obligation passes are append-only.  Migration enumerates them
            # by artifact, raw-heading digest, and occurrence count, then records
            # which exact obligation each admitted pass satisfied."*  That
            # enumeration is the migration's, and it is the named residual of this
            # chunk.
            grandfathered = True
            continue
        tier, tv = _parse_one_field(sec.body, _TIER_LINE_RE, _TIERS, "Tier")
        find, fv = _parse_one_field(
            sec.body, _FINDINGS_LINE_RE, _FINDINGS, "Findings")
        for problem in (tv, fv):
            if problem:
                v.append(f"'{sec.kind} -- {sec.name} -- {sec.date}': {problem}")
        if find == "raised" and not _has_disposition(art, sec):
            # Positional, and it accepts EITHER house form.  See
            # _has_disposition: the tree uses both, roughly evenly, so a gate
            # that demanded one would redden half the existing dispositions
            # while enforcing a convention the project does not hold.
            v.append(
                f"'{sec.kind} -- {sec.name} -- {sec.date}' declares "
                "'**Findings**: raised' but no disposition follows it -- "
                "expected a '### Sharpening' inside its own body, or a "
                "'## Response to plan review' section before the next pass.")
        if not (ok_date and tier and find):
            continue
        if multi:
            # ONE pass binds itself to ONE clause, so one pass structurally
            # cannot clear two.  A pass whose `**Obligation**:` is missing,
            # duplicated, or undeclared clears nothing and is NOT reported here:
            # The consequence for those values is verbatim *"do not clear the
            # floor"*, and the floor's own message below is what surfaces it.
            # Reporting them per-pass instead would red this plan's own landed
            # Internal review, whose `**Obligation**:` names its authorizing
            # revision section rather than a declared clause -- an append-only
            # record that is not ours to rewrite, and whose non-clearing is
            # already the correct outcome.
            clause = _pass_obligation(
                _record_field_scope(lines, sec.line_no, boundaries),
                obligations)
            if clause is not None and tier_satisfies(tier, dict(obligations)[clause]):
                cleared[clause] = True
        elif obligations and tier_satisfies(tier, obligations[0][1]):
            cleared[obligations[0][0]] = True
    if grandfathered:
        return v
    near = _near_miss_headings(art)
    quoted = ("; near misses that do NOT count: "
              + ", ".join(repr(h) for h in near)) if near else ""
    if not multi:
        if required and not all(cleared.values()):
            v.append(
                f"'Plan review: required({required})' but no conforming pass "
                f"satisfies it. A heading that is not an exact "
                f"'## Plan review -- <reviewer> -- YYYY-MM-DD' is not a pass and "
                f"cannot clear the floor{quoted}.")
        return v
    for clause, tier_name in obligations:
        if cleared[clause]:
            continue
        v.append(
            f"'Plan review: required(... {clause} ...)' declares {len(obligations)} "
            f"obligations and no conforming pass satisfies it for {clause!r}: a "
            f"'+' declaration means one distinct pass per clause, each carrying "
            f"exactly one '**Obligation**: {clause}' line before its first H3 and "
            f"a '**Tier**:' that satisfies {tier_name!r}. One pass cannot clear "
            f"two clauses{quoted}.")
    return v


# === the status/evidence contradiction predicates =============================
#
# The contract lists eight contradictions `scan`, `next` and the accepted closeout command
# must refuse, and is explicit that they *"consume shared predicates"* -- so this
# is ONE function taking the state as a parameter, on the same S12 pattern
# `review_record_violations` already uses.  `scan` passes the current status,
# `next` the requested target, and `closeout --dry-run` will pass
# `ready-to-archive`; three call sites, one interpretation.
#
# **What these predicates can and cannot see.**  *"The tools verify record
# structure, not reviewer competence, authorization, or semantic truth."*  Each
# refusal below is a claim about a record's SHAPE.  Two limits are named where
# they bite rather than left for a reader to discover:
#
#   * a *proposal* review has no closed verdict vocabulary -- `code-review-
#     blindness` supplies one for the Code-review record only -- so "blocking"
#     and "clearing" are read from the pass's own `Findings: raised | none`
#     declaration, which is the only closed field the record carries.  A review
#     that declares neither is not readable as either, and fails closed.
#   * "every closeout precondition" is the two attestations the archive gate
#     already checks.  Whether the *content* of a disposition is honest is not
#     reachable and is not claimed.

#: The plan states that assert plan review has CLEARED.  Not
#: `awaiting-plan-review` and not `revising-plan`: at those two the review is
#: outstanding or blocking by definition, so demanding a clearing pass there
#: would make the two states unreachable.
PLAN_REVIEW_CLEARED_STATES = ("ready-to-implement", "implementing",
                              "awaiting-code-review", "revising-code")

#: The proposal states at or past the review floor -- where a `## Review` record
#: must exist and must not be the author's own.  Both vocabularies, because the
#: check is about the record and not about the token.
#:
#: **The migration deliberately did NOT narrow this tuple, departing from its own cost
#: list, because narrowing it disables a real check rather than merely changing
#: a message.**
#:
#: Review falsified the measurement an earlier version of this note
#: gave, and the corrected one is worse, not better. That version claimed the
#: narrowing leaves `unknown proposal status` behind and that *"scan still exits
#: 1 either way"*. It does not: it was taken against a partially-applied
#: retirement. On the finished state, for a self-reviewed **archived** proposal
#: declaring `reviewed`, narrowing this tuple yields **zero violations and exit
#: 0** -- because archived artifacts are correctly exempt from the status
#: check, so nothing at all remains to be non-zero about. The regression is
#: therefore fully silent for archived artifacts, not merely camouflaged.
#:
#: For an **active** proposal the narrowing is caught:
#: `test_scan_flags_review_authored_by_proposal_author` reddens. The archived
#: case is the unguarded one, and it is the case this tuple exists for -- the
#: comment above is the standing reason: the check is about the record, not the
#: token, and an archived record is still a record.
_PROPOSAL_POST_REVIEW_STATES = (
    "revising", "awaiting-decision",
    "reviewed", "revised",
    "accepted", "rejected", "superseded")

#: The one optional plan metadata line.  Read from the HEADER region only,
#: for the reason `assurance_declaration_violations` reads its field there: a
#: `**Blocked by**:` line quoted inside an appended review section is a historical
#: restatement, not the plan's own declaration.
_BLOCKED_BY_FIELD = "Blocked by"


def blocked_by_violations(art: Artifact) -> List[str]:
    """The orthogonal `**Blocked by**:` field's SHAPE, and nothing more.

    *"Absence means no recorded external blocker.  The field never changes the
    legal state machine and never substitutes for a status."*  So this returns
    ``[]`` for an absent field, and the two things it does check are the two that
    can make the field lie about itself: a duplicate (two lines that may disagree,
    with no rule to pick one) and an empty value (a field that records nothing
    while looking like a record).

    **What it deliberately does not check, because it cannot.**  The contract requires the
    value to *"name a falsifiable condition whose resolution is observable"* --
    that is a judgement about English, not a shape, and no scanner reaches it.  It
    also *"grants no authority and is not evidence that a gate passed"*: this
    predicate feeds `scan`'s conformance list and **no** gate, which is the
    orthogonality made structural rather than promised.  `_legal_transitions`
    never reads it.
    """
    if art.kind != "plan":
        return []
    header = "\n".join(_iter_header_lines(art.text))
    found = _REVIEW_FIELD_RE[_BLOCKED_BY_FIELD].findall(header)
    if not found:
        return []
    if len(found) > 1:
        return [f"duplicate '**{_BLOCKED_BY_FIELD}**:' ({len(found)} lines in the "
                "header) -- two blockers that may disagree, with no rule to "
                "choose between them; record one condition per line's worth of "
                "authority, or none"]
    if not found[0].strip():
        return [f"empty '**{_BLOCKED_BY_FIELD}**:' value -- omit the line "
                "entirely when nothing blocks (absence IS the 'no blocker' "
                "record); a present-but-empty field names no falsifiable "
                "condition"]
    return []

#: The record that makes `awaiting-code-review` true: Boundary B's stable
#: evidence section.  The house form, measured across `dev/plans/` +
#: `dev/plans/archive/` (18 records, 2026-08-12): every one is
#: `## Implementation verification -- <agent> -- YYYY-MM-DD` with an optional
#: trailing parenthetical.  Full-line anchored, so a prose mention is not a
#: record.
_STABLE_EVIDENCE_RE = re.compile(
    r"^## Implementation verification -- (?P<agent>[^\n]+?) -- "
    r"(?P<date>\d{4}-\d{2}-\d{2})(?P<rest>[^\n]*)$")


def _stable_evidence_records(art: Artifact) -> List[Tuple[int, str]]:
    """``(line_no, date)`` per conforming Boundary B record, in document order."""
    out: List[Tuple[int, str]] = []
    for i, raw in enumerate(art.text.split("\n")):
        m = _STABLE_EVIDENCE_RE.match(raw)
        if m and _parse_pass_date(m.group("date"))[0]:
            out.append((i + 1, m.group("date")))
    return out


def _independent_review(art: Artifact) -> bool:
    """Does any `## Review` carry a byline distinct from the proposal author?

    Factored out of `_gating_preconditions`, where it was a local comprehension,
    because the `awaiting-decision` predicate needs the same answer and a second
    copy is how the two surfaces come to disagree (S12).  It reads bylines: a
    review that IS independent but signed with the author's name reads as
    dependent, and a review signed with someone else's name reads as independent.
    Authorship is carried by attributed, self-committed authorship, never by this.
    """
    return any(
        r.name and (not art.author
                    or _identity_token(r.name) != _identity_token(art.author))
        for r in _reviewers(art)
    )


def _latest_proposal_review(art: Artifact) -> Tuple[Optional[int], Optional[str],
                                                    Optional[str], List[str]]:
    """The latest `## Review` record's disposition -- ``(line, tier, findings, v)``.

    Document order is authoritative, exactly as it is for the Code-review record
    the last record in the file is the current one.  *tier* and *findings*
    are read from that record's field scope through the same closed vocabularies
    the Plan-review pass uses, and *v* carries the fail-closed reasons when either
    cannot be resolved.
    """
    records = _proposal_review_records(art)
    if not records:
        return None, None, None, []
    line_no, raw = records[-1]
    scope = _record_field_scope(
        art.text.split("\n"), line_no, _record_boundaries(art))
    label = f"'{raw.strip()}'"
    tier, tier_problem = _parse_one_field(
        scope, _REVIEW_FIELD_RE["Tier"], _TIERS, "Tier")
    find, find_problem = _parse_one_field(
        scope, _REVIEW_FIELD_RE["Findings"], _FINDINGS, "Findings")
    problems = [f"{label}: {p}" for p in (tier_problem, find_problem) if p]
    return line_no, tier, find, problems


def _closeout_violations(art: Artifact, state: str) -> List[str]:
    """The two closeout preconditions, on ONE predicate.

    Bullet 8 is *"`archived` when the same closeout predicate would reject
    `ready-to-archive`"*, which is a statement about *sharing*, not about two
    rules: so the two states call this with their own name and get the identical
    verdict.  A plan cannot become `ready-to-archive` on evidence that would not
    let it become `archived`, or the reverse.
    """
    v: List[str] = []
    if not art.has_disposition_attestation:
        v.append(
            f"status is {state!r} but no 'Dispositions:' block "
            "(or the older 'Follow-ups migrated to:') is present "
            "(archive precondition).")
    if not art.has_fidelity_signoff:
        v.append(
            f"status is {state!r} but no loop-fidelity sign-off is "
            "present (names the implementing commit + governing section).")
    return v


def status_evidence_violations(art: Artifact, state: str) -> List[str]:
    """Every status/evidence contradiction for ONE explicit *state*.

    Public because three surfaces consume it: `_conformance_violations` (what
    `scan` reports for the current status), `_gating_preconditions` (what `next
    --to <target>` requires) and `closeout --dry-run`.  Wiring
    only one is the defect review executed on the Code-review half -- one surface
    tightens, the other stays loose, and the loose one is the one an author drives.

    Returns the contradiction violations.  It is not the whole conformance contract:
    the identity model's Decision checks, the `**Status**:`/`**Plan review**:`
    floors and the declaration checks are their own predicates and stay in
    `_conformance_violations`, which composes this one.

    **The status condition is deliberate, and the earlier note survives here.**
    The plan arm asserts that the ASSERTED state is structurally supported, so an
    `awaiting-plan-review` plan waiting for its review is not a violation -- and
    the evaluate-as-if-transitioning read is `next`'s, reached by passing
    the *target*.  That is exactly why the state is a parameter rather than read
    off `art.status` inside: one predicate cannot serve both readings unless the
    caller says which state it means.
    """
    v: List[str] = []
    if art.kind == "proposal":
        _line, tier, find, problems = _latest_proposal_review(art)
        if state == "revising":
            # "proposal `revising` without a blocking review
            # record".  `revising` says the author owes a Response to a critique;
            # a latest review declaring `Findings: none` is the contradiction.
            if _line is None:
                v.append(
                    "status is 'revising' but no '## Review' record is present "
                    "-- 'revising' asserts a reviewer raised a blocking "
                    "critique, so a review record must exist to have raised it.")
            elif find == "none":
                v.append(
                    "status is 'revising' but the latest '## Review' declares "
                    "'Findings: none' -- a clearing review sends a proposal to "
                    "'awaiting-decision', not into a revision loop.")
            elif find is None:
                v.extend(problems or [
                    "status is 'revising' but the latest '## Review' declares no "
                    "readable '**Findings**: none | raised' -- the field is what "
                    "makes a review blocking, and there is no default."])
        elif state == "awaiting-decision":
            # With the replacement text: "At least one proposal
            # review at the Internal floor or above has cleared the current
            # contract ... and no blocking proposal-review finding remains."
            if _line is None:
                v.append(
                    "status is 'awaiting-decision' but no '## Review' record is "
                    "present -- the Maintainer's next action rests on a cleared "
                    "independent read, which no record attests.")
            else:
                if not _independent_review(art):
                    v.append(
                        "status is 'awaiting-decision' but no '## Review' "
                        "carries a reviewer identity distinct from the proposal "
                        "author -- structural independence is the floor, and the "
                        "tool reads the byline, never the reviewer's identity.")
                if find == "raised":
                    v.append(
                        "status is 'awaiting-decision' but the latest '## "
                        "Review' declares 'Findings: raised' -- a blocking "
                        "finding sends the proposal to 'revising'; a Response "
                        "returns it to 'awaiting-review', never straight to a "
                        "Decision.")
                elif find is None or tier is None:
                    v.extend(problems or [
                        "status is 'awaiting-decision' but the latest '## "
                        "Review' does not declare a readable '**Tier**:' and "
                        "'**Findings**:' -- 'cleared at the Internal floor or "
                        "above' is a claim about those two closed fields."])
        return v
    # plan
    requires_review = art.plan_review.lower().startswith("required")
    if state in CODE_REVIEW_EFFECTIVE_STATES or (
            state in PLAN_REVIEW_CLEARED_STATES and requires_review):
        # `ready-to-implement` / `implementing` before every required
        # plan-review OBLIGATION clears, under the multi-obligation rule
        # and bullets 5-8's Code-review half, both through the one predicate.
        v.extend(review_record_violations(art, state))
    if state == "revising-plan":
        # "plan `revising-plan` without a blocking plan-review
        # pass".  Read off the latest S1-conforming pass's own `Findings:` field.
        passes = _pass_headings(art)
        if not passes:
            v.append(
                "status is 'revising-plan' but no conforming '## Plan review -- "
                "<reviewer> -- YYYY-MM-DD' pass is present -- the state asserts "
                "the latest pass requires correction, so a pass must exist.")
        else:
            sec, _dig = passes[-1]
            find, problem = _parse_one_field(
                sec.body, _FINDINGS_LINE_RE, _FINDINGS, "Findings")
            if find == "none":
                v.append(
                    "status is 'revising-plan' but the latest '## Plan review' "
                    "declares 'Findings: none' -- a pass that raises nothing "
                    "does not open a revision loop.")
            elif find is None:
                v.append(
                    f"status is 'revising-plan' but the latest '## Plan review' "
                    f"has no readable '**Findings**: none | raised' line "
                    f"({problem}).")
    if state == "awaiting-code-review":
        v.extend(_stable_evidence_contradictions(art))
    if state == "revising-code":
        # "`revising-code` without a latest blocking Code review".
        # The inverse of the archive rule: `review_record_violations` refuses
        # `ready-to-archive` when the latest pass BLOCKS, and this refuses
        # `revising-code` when it does not.
        passes = _code_review_pass_lines(art)
        if not passes:
            v.append(
                "status is 'revising-code' but no conforming '## Code review -- "
                "<reviewer> -- YYYY-MM-DD[ (round N)]' pass is present -- the "
                "state asserts the latest Code review blocks.")
        else:
            line_no, reviewer, date, _round = passes[-1]
            verdict, problem = _parse_verdict(_code_review_pass_body(art, line_no))
            if verdict == "clearing":
                v.append(
                    f"status is 'revising-code' but the latest '## Code review "
                    f"-- {reviewer} -- {date}' carries a CLEARING verdict -- a "
                    "cleared review sends the plan to 'ready-to-archive'.")
            elif verdict is None:
                v.append(
                    f"status is 'revising-code' but the latest '## Code review "
                    f"-- {reviewer} -- {date}' has no readable verdict "
                    f"({problem}) -- the state rests on that one field.")
    if state in CODE_REVIEW_EFFECTIVE_STATES:
        v.extend(_closeout_violations(art, state))
    return v


def _stable_evidence_contradictions(art: Artifact) -> List[str]:
    """`awaiting-code-review` without a valid stable evidence record.

    Two conditions, and the second is the word *"replacement"* made checkable:
    `revising-code` returns to `awaiting-code-review` on *"a replacement stable
    record"*, so a Boundary B record that predates the blocking Code review it is
    supposed to replace is stale, not evidence.  On the FIRST arrival at
    `awaiting-code-review` there is no Code-review pass and the ordering condition
    is vacuous, which is why it is expressed as an ordering rather than a count.

    **Structure only.**  A conforming heading with a real date is what this reads.
    Whether the record's own body names the tested range, the interpreter and a
    clean tree -- what `AGENTS.md` > *Verification boundaries* requires of Boundary
    B -- is not checked here and is not claimed to be.
    """
    records = _stable_evidence_records(art)
    if not records:
        return [
            "status is 'awaiting-code-review' but no conforming '## "
            "Implementation verification -- <agent> -- YYYY-MM-DD' record is "
            "present -- the state asserts stable bytes plus the applicable "
            "Boundary B evidence, and that record is the evidence."]
    passes = _code_review_pass_lines(art)
    if not passes:
        return []
    latest_pass = passes[-1][0]
    latest_record = records[-1][0]
    if latest_record < latest_pass:
        return [
            f"status is 'awaiting-code-review' but the latest '## "
            f"Implementation verification' record (line {latest_record}) "
            f"predates the latest '## Code review' pass (line {latest_pass}) -- "
            "returning from 'revising-code' takes a REPLACEMENT stable-evidence "
            "record over the corrected range, not the one the blocking review "
            "already read."]
    return []


# --- conformance checks (structural; used by `scan` and `next`) --------------
#
# These verify the *current* status is structurally supported by the
# documentary attestations the artifact carries -- the machine-verifiable
# half.  Each returned string is a violation; an empty list means the
# current state is structurally sound (NOT that the quotes are authentic --
# the tool never asserts authenticity).


def _conformance_violations(art: Artifact, identity: "IdentityModel") -> List[str]:
    v: List[str] = []
    s = art.status
    if art.kind == "proposal":
        if not s:
            # A proposal MUST carry a Status line. Without this floor a
            # status-less proposal short-circuits every check below and a real
            # violation (an AI-authored Decision, a missing blockquote) is
            # silently laundered -- a scan false-negative. Mirrors the
            # unconditional '**Plan review**:' floor plans carry.
            v.append(
                "no '**Status**:' line -- a proposal must carry a Status "
                "(awaiting-review/revising/awaiting-decision/accepted/rejected/"
                "superseded); a missing status hides every downstream "
                "conformance check."
            )
        elif s in HISTORICAL_PROPOSAL_STATES:
            # Retired, not unrecognized -- and the two must not be conflated.
            # An ARCHIVED proposal legitimately still declares one of these, so
            # reading history is never a violation; an ACTIVE one declaring it
            # is exactly what retirement refuses, and it gets the migration
            # target rather than a dead-end `unknown`.
            if not _is_immutable(art):
                v.append(
                    f"retired proposal status {s!r} -- the accepted vocabulary "
                    "replaced it (proposed -> awaiting-review; reviewed/revised "
                    "-> revising | awaiting-review | awaiting-decision, derived "
                    "from the latest review). Historical values stay legal on "
                    "archived artifacts only."
                )
        elif s not in _PROPOSAL_STATES:
            v.append(f"unknown proposal status {s!r}")
        # The artifact-level declaration and the review basis, on the same
        # predicates `_gating_preconditions` consumes (S12's one-predicate rule
        # applied to the proposal side).  Unconditional on status: the accepted
        # parent has a proposal-worthy change declare its assurance path, and a
        # review record owes its basis whenever it exists -- neither obligation
        # arrives at some later state.
        v.extend(assurance_declaration_violations(art))
        v.extend(proposal_review_basis_violations(art))
        # P2-R -- the readiness finding a derived plan may inherit.  Optional by
        # contract ("a proposal reviewer MAY record"), so this is silent unless
        # the field is present; what it refuses is a present one that cannot be
        # read as exactly one of the two closed values.
        v.extend(plan_readiness_violations(art))
        # The complete current-contract revision and its withdrawal ledger.
        # Unconditional on status for the same reason the sibling pair is: the obligation
        # arrives with the Response, not at some later state, and an author who
        # discovered the refusal only at the transition would already have asked a
        # reviewer to read a contract that was never restated.
        v.extend(current_contract_violations(art))
        # The proposal contradictions, on the shared predicate `next` and
        # `closeout` consume.  Placed here so a status/evidence
        # contradiction is reported beside the declarations it depends on.
        v.extend(status_evidence_violations(art, s))
        if s in _PROPOSAL_POST_REVIEW_STATES:
            revs = _reviewers(art)
            if not revs:
                # Chunk E: the two NEW post-review states report this absence in
                # their own words, from `status_evidence_violations` above.  Two
                # sentences for one fact is noise an operator has to reconcile, so
                # this message stays scoped to the PENDING-RETIREMENT tokens.
                if s not in ("revising", "awaiting-decision"):
                    v.append(
                        f"status is {s!r} but no '## Review' section is present "
                        "(reviewed/revised/decided states require a prior review)."
                    )
            else:
                for r in revs:
                    if art.author and r.name and _identity_token(r.name) \
                            == _identity_token(art.author):
                        v.append(
                            f"'## Review' at line {r.line_no} appears authored "
                            f"by the proposal author ({art.author!r}); a review "
                            "carries reviewer-authorship (independent reviewer)."
                        )
        if s == "revised" and not _has_kind(art, "Response"):
            v.append("status is 'revised' but no '## Response' section is present.")
        if s in ("accepted", "rejected", "superseded"):
            decs = _decisions(art)
            if not decs:
                v.append(
                    f"status is {s!r} but no '## Decision' section is present "
                    "(a terminal status requires a Maintainer Decision)."
                )
            for d in decs:
                if not d.has_isolated_blockquote:
                    v.append(
                        f"'## Decision' at line {d.line_no} carries no isolated "
                        "authorization blockquote (the verbatim authorization is "
                        "structurally absent)."
                    )
                cls = identity.classify(d.name) if d.name else "unknown"
                if cls == "ai":
                    v.append(
                        f"'## Decision' at line {d.line_no} appears authored by "
                        f"an AI agent ({d.name!r}); a Decision is a human "
                        "Maintainer authority."
                    )
                elif cls == "unknown":
                    v.append(
                        f"'## Decision' at line {d.line_no} is authored by an "
                        f"UNRECOGNIZED identity ({d.name!r}{_ascii_hint(d.name)}); "
                        "a terminal Decision requires a KNOWN human Maintainer. "
                        "Correct the byline to name the configured Maintainer "
                        "-- a trailing '(role)' parenthetical is stripped before "
                        "matching, so 'Ada Lovelace (Maintainer)' matches an "
                        "'Ada Lovelace' entry, while a bare role word is not a "
                        "name at all. Only if this identity genuinely IS a human "
                        "Maintainer, add it to dev/.cairn/agent-identities.json "
                        "('human_maintainers') -- an entry must be the COMPLETE "
                        "display name exactly as it appears in the byline, not a "
                        "name fragment and never a role word, which would let any "
                        "author claim Maintainer authority. An unrecognized author "
                        "cannot be confirmed human (the tool attests structure, "
                        "never authenticity)."
                    )
                # cls == "human": the byline is a recognized Maintainer. The tool
                # still does not authenticate the quoted authorization itself --
                # that remains the committing operator's guarantee.
    else:  # plan
        if s and s in HISTORICAL_PLAN_STATES:
            # See the proposal-side note above; archived plans keep theirs.
            if not _is_immutable(art):
                v.append(
                    f"retired plan status {s!r} -- the accepted vocabulary "
                    "replaced it (open -> awaiting-plan-review; executing -> "
                    "implementing; review -> awaiting-code-review | "
                    "revising-code | ready-to-archive, from the latest "
                    "Code-review verdict). Historical values stay legal on "
                    "archived artifacts only."
                )
        elif s and s not in _PLAN_STATES:
            v.append(f"unknown plan status {s!r}")
        if not art.plan_review:
            v.append(
                "no '**Plan review**:' line (mandatory: 'required(<tier>)' or "
                "'not required(<rationale>)'; a missing line is a finding)."
            )
        # The plan contradictions, ONE predicate, THREE call sites.  This
        # replaces the two status-keyed blocks that stood here (the
        # `review_record_violations` call for `executing`/`review`/archive-
        # effective states, and the two archive attestations for `archived`) --
        # both moved INTO `status_evidence_violations`, which takes the state as a
        # parameter.  Nothing about either check changed; what changed is that
        # `next --to <new state>` and `closeout` now reach the same code
        # instead of each growing its own opinion, which is the drift S12 exists
        # to prevent and which the contract requires by name: "`scan`, `next`, and accepted
        # closeout tooling consume shared predicates."
        v.extend(status_evidence_violations(art, s))
        # The optional `**Blocked by**:` metadata, checked UNCONDITIONALLY on
        # status.  That is the field's whole point: it is orthogonal to the state
        # machine, so it can neither be keyed on a state nor gate one.
        v.extend(blocked_by_violations(art))
        # P2-R -- the inheritance chain, also unconditional on status.  A plan's
        # readiness basis is either valid or it is not; the validity does not
        # begin at `ready-to-implement`, and an author who would discover the
        # refusal only at the transition would already have implemented against
        # an unbound contract.
        v.extend(plan_inheritance_violations(art))
    return v


# --- forward-transition recipes (preconditions a target needs) ---------------
#
# For each legal target, the *gating* preconditions: structural facts that
# must already hold for the transition to be valid, each reported met/unmet
# from the file.  When a gate is unmet the tool reports the missing
# attestation -- it never presents the transition as ready (contract
# clause 3).


def _r6_gate(art: Artifact, state: str, description: str) -> Tuple[bool, str]:
    """One gate whose predicate IS `status_evidence_violations` for *state*.

    The contract requires `scan`, `next` and closeout to *"consume shared predicates rather
    than implement three interpretations of readiness"*.  Routing every new
    target's gate through this one function is how that requirement is met
    structurally: there is no second place to tighten or loosen, and the gate
    reports the predicate's own sentences as its UNMET detail so an operator is
    never sent to `scan` to find out what was withheld.
    """
    problems = status_evidence_violations(art, state)
    detail = "" if not problems else "  UNMET: " + "; ".join(problems)
    return (not problems, description + detail)


def _gating_preconditions(art: Artifact, target: str,
                          identity: "IdentityModel") -> List[Tuple[bool, str]]:
    """Return (met, description) gates for a forward transition to `target`."""
    gates: List[Tuple[bool, str]] = []
    revs = _reviewers(art)
    independent_review = _independent_review(art)
    if art.kind == "proposal":
        # The SAME two predicates `_conformance_violations` uses, so the
        # two gate surfaces cannot drift.  Reported on every forward transition
        # because neither obligation begins at some later state, and because a
        # gate wired to only one surface is the defect review executed on the
        # Code-review half: the loose surface is the one an author drives.
        for problems, name in (
                (assurance_declaration_violations(art),
                 "the header declares '**Assurance path**: standard | "
                 "high-assurance' (no default; uncertainty resolves high)"),
                (proposal_review_basis_violations(art),
                 "every '## Review' record carries the four-field review basis "
                 "(Reviewed commit / Target / Prior findings / Assurance path) "
                 "before its first H3"),
                (plan_readiness_violations(art),
                 "any '## Review' record's 'Plan readiness:' finding reads as "
                 "exactly one of READY | DISTINCT REVIEW REQUIRED (optional "
                 "field; no default)"),
                (current_contract_violations(art),
                 "a proposal that has answered a review carries a complete "
                 "current-contract revision, and every such revision carries its "
                 f"mandatory '### {_LEDGER_HEADING}' ledger with a written value "
                 "(even when that value is 'None')")):
            detail = "" if not problems else "  UNMET: " + "; ".join(problems)
            gates.append((not problems, name + detail))
        if target in ("awaiting-review", "reviewed"):
            # `awaiting-review` is the initial state AND the state a
            # Response returns the proposal to, so the return arm gets its own
            # gate while the opening arm has nothing to attest yet.
            if art.status == "revising":
                gates.append((_has_kind(art, "Response"),
                              "a '## Response' (+ the complete current-contract "
                              "revision) has landed -- that record is what returns "
                              "a revising proposal to its reviewer"))
            gates.append((True,
                          "append a '## Review' (reviewer fills their own "
                          "identity; not the proposal author); append-only."))
        elif target in ("revising", "revised"):
            gates.append((bool(revs),
                          "a prior '## Review' section exists"))
            if target == "revising":
                # Contradiction 1, on the shared predicate.
                gates.append(_r6_gate(
                    art, "revising",
                    "the LATEST '## Review' declares '**Findings**: raised' -- a "
                    "revision loop opens on a blocking critique, and the field is "
                    "the only closed one a proposal review carries (conformance "
                    "only: the tool reads the declaration, never the critique)"))
            gates.append((True,
                          "append a '## Response' AND the complete "
                          "current-contract revision it owes (with its "
                          f"'### {_LEDGER_HEADING}' ledger); append-only."))
        elif target == "awaiting-decision":
            # Contradiction 2 with the replacement text.  No instruction gate:
            # this transition appends nothing -- the clearing REVIEW is what
            # selects it, and that record already landed.
            gates.append(_r6_gate(
                art, "awaiting-decision",
                "the LATEST '## Review' is a clearing pass: an independent "
                "byline, a '**Tier**:' in the closed vocabulary, and "
                "'**Findings**: none' -- with no blocking finding outstanding "
                "(conformance only -- the tool attests the record's shape)"))
        elif target in ("accepted", "rejected", "superseded"):
            gates.append((independent_review,
                          "an independent '## Review' section is present, "
                          "bearing a reviewer identity and date (the record "
                          "shape; whether the review occurred is carried by "
                          "attributed, self-committed authorship)"))
            gates.append((True,
                          "append a '## Decision' (Human Maintainer) quoting the "
                          "authorization verbatim in an isolated blockquote; the "
                          "commit is Decision-only."))
            if target in ("rejected", "superseded"):
                gates.append((True,
                              "the Decision commit also moves the file to "
                              "archive/."))
    else:  # plan
        requires_review = art.plan_review.lower().startswith("required")
        # P2-R -- the SAME predicate `_conformance_violations` uses, reported on
        # every forward transition for the reason the proposal-side pair is: a
        # gate wired to only one surface is the defect executed, and the loose
        # surface is the one an author drives.  Silent for a plan that declares
        # no inheritance.
        inheritance = plan_inheritance_violations(art)
        if _declares_inheritance(art):
            detail = ("" if not inheritance
                      else "  UNMET: " + "; ".join(inheritance))
            gates.append((
                not inheritance,
                "the inherited proposal basis binds: two full commit ids, a "
                "resolvable source proposal whose LATEST 'Plan readiness:' "
                "finding is READY at an External tier, 'proposal=' equal to that "
                "review's 'Reviewed commit', and no declared contract expansion "
                "or unallowed scope reduction" + detail))
        if target == "awaiting-plan-review":
            gates.append((requires_review,
                          "'Plan review: required(<tier>)' (else the plan goes "
                          "straight to ready-to-implement)"))
        elif target == "revising-plan":
            # Contradiction 3, on the shared predicate.
            gates.append(_r6_gate(
                art, "revising-plan",
                "the LATEST conforming '## Plan review' pass declares "
                "'**Findings**: raised' -- a pass that raises nothing does not "
                "open a revision loop"))
            gates.append((True,
                          "append a '## Response to plan review'; append-only. "
                          "The author cannot self-clear: returning to "
                          "'awaiting-plan-review' is the author's move, and "
                          "clearing the floor stays the reviewer's."))
        elif target == "executing":
            if requires_review:
                # S12 -- the SAME predicate `_conformance_violations` uses, so
                # the two gate surfaces cannot drift.  Was
                # `_has_kind(art, "Plan review")`, which cleared on presence.
                problems = review_record_violations(art)
                detail = "" if not problems else "  UNMET: " + "; ".join(problems)
                gates.append((not problems,
                              "a CONFORMING '## Plan review' pass has landed: an "
                              "exact '## Plan review -- <reviewer> -- YYYY-MM-DD' "
                              "heading with a calendar-valid date, carrying one "
                              "'**Tier**:' and one '**Findings**:' line, a "
                              "disposition when it declares findings raised, and a "
                              "declared tier that meets the required floor "
                              "(conformance only -- the tool attests that a tier "
                              "was DECLARED, never that it was true)" + detail))
                gates.append((True,
                              "the plan-open and first-implementation commits "
                              "stay distinct."))
            else:
                gates.append((True,
                              "'Plan review: not required' -- execution may "
                              "combine with plan-open."))
        elif target in ("ready-to-implement", "implementing"):
            # BOTH states assert every required plan-review
            # obligation has cleared, and under the `+` rule "cleared" means one
            # distinct pass per declared clause.  Reached through `_r6_gate`, so
            # `next` cannot be looser than `scan` about the same record.
            if requires_review:
                gates.append(_r6_gate(
                    art, target,
                    "every declared plan-review obligation is cleared by its own "
                    "CONFORMING '## Plan review -- <reviewer> -- YYYY-MM-DD' pass. "
                    "Under a 'required(A + B)' declaration that is one pass per "
                    "clause, each naming its clause in one '**Obligation**:' line "
                    "-- one pass cannot clear two (conformance only -- the tool "
                    "attests that a tier was DECLARED, never that it was true)"))
            else:
                gates.append((True,
                              "'Plan review: not required' -- execution may "
                              "combine with plan-open."))
            if target == "implementing":
                gates.append((True,
                              "the plan-open and first-implementation commits "
                              "stay distinct, UNLESS this is the accepted combined "
                              "fast path -- in which case the plan-open commit "
                              "must itself carry the implementation evidence that "
                              "makes the skipped 'ready-to-implement' true."))
        elif target in ("awaiting-code-review", "review"):
            if target == "awaiting-code-review":
                # Contradiction 5, and the word "replacement" made checkable.
                gates.append(_r6_gate(
                    art, "awaiting-code-review",
                    "a conforming '## Implementation verification -- <agent> -- "
                    "YYYY-MM-DD' record is present, and -- when a Code-review pass "
                    "has already landed -- it comes AFTER that pass, because "
                    "returning from 'revising-code' takes a replacement record "
                    "over the corrected range (the heading and its date are what "
                    "is checked, never the evidence inside it)"))
            gates.append((True,
                          "append a '## Code review' pass (reviewer is not the "
                          "implementing agent); append-only."))
        elif target == "revising-code":
            # Contradiction 6 -- the exact inverse of the archive rule below.
            gates.append(_r6_gate(
                art, "revising-code",
                "the LATEST '## Code review' pass carries a BLOCKING "
                "'**Verdict**:' (REVISE / Request changes / BLOCK) -- a clearing "
                "verdict sends the plan to 'ready-to-archive' instead"))
        elif target in ("ready-to-archive", "archived"):
            # The SAME predicate `_conformance_violations` uses,
            # on the requested TARGET as the effective state.  This replaces the
            # separate `art.has_code_review_marker` gate that stood here: two
            # surfaces asking one question in two strengths is the drift S12
            # exists to prevent, and the marker was the weaker of the two.
            # Called regardless of the `Plan review:` declaration -- review
            # executed the bypass a declaration-keyed call leaves open.
            #
            # **One branch for BOTH states, which is contradiction 8 stated
            # as code.**  "`archived` when the same closeout predicate would
            # reject `ready-to-archive`" is not two rules -- it is one rule
            # required to be shared.  A plan therefore cannot reach
            # `ready-to-archive` on evidence that would not let it reach
            # `archived`, or the reverse, and there is no second place to soften
            # one of the two.
            problems = review_record_violations(art, target)
            detail = "" if not problems else "  UNMET: " + "; ".join(problems)
            gates.append((not problems,
                          "the review record conforms for archive: a CONFORMING "
                          "'## Code review -- <reviewer> -- YYYY-MM-DD' pass "
                          "whose LATEST instance carries the four-field review "
                          "basis, '**Model**:', '**Findings**:', and a CLEARING "
                          "'**Verdict**:' (SHIP / Accept / "
                          "Accept-with-followups / PASS). A blocking verdict is "
                          "answered by a later independent pass, never by a "
                          "'## Response to code review'. Conformance only -- "
                          "the tool attests the record shape, never that a "
                          "review took place" + detail))
            gates.append((art.has_disposition_attestation,
                          "every deferred follow-up carries a recorded "
                          "disposition: an explicit 'none', or an entry naming "
                          "accept / guard / wontfix / defer. An empty "
                          "'Dispositions:' label does not count."))
            gates.append((art.has_fidelity_signoff,
                          "the loop-fidelity sign-off, inside '## Lasting-truth "
                          "migration', names at least one implementing commit "
                          "id and the governing accepted/Revised section. "
                          "Promising it is owed does not count."))
    return gates


# --- scaffolds (the proposed section + mutation manifest) --------------------
#
# Each scaffold is emitted to STDOUT.  It carries placeholders the
# operator fills; the tool NEVER fills a reviewer identity, a disposition,
# a finding, or an authorization (contract clause 2).


#: "Status and evidence move together" -- for each new-vocabulary
#: state, the record whose commit carries the flip.  Most new transitions append
#: **nothing**: the accepted contract is explicit that *"Do not create empty
#: commits merely to advance a label"* and that the review, Response,
#: implementation, verification, Code-review or archive commit is the one that
#: moves the status.  So the scaffold for these is a manifest saying *whose*
#: commit does it -- not a section to paste, which would invite exactly the empty
#: transition commit the contract forbids.  `awaiting-code-review` is the one exception: its
#: evidence record is a section, and it gets one.
_STATUS_MOVES_WITH: Dict[str, str] = {
    "awaiting-review": "the author's '## Response' + complete current-contract "
                       "revision commit (returning from 'revising'), or the "
                       "proposal-open commit",
    "revising": "the REVIEWER's own '## Review' commit -- the reviewer who "
                "raises a blocking critique selects this state; the author does "
                "not move the proposal into their own revision loop",
    "awaiting-decision": "the clearing REVIEWER's '## Review' commit -- the pass "
                         "that clears the floor selects this state",
    "revising-plan": "the plan REVIEWER's '## Plan review' commit -- the author "
                     "cannot self-clear, and cannot self-assign the loop either",
    "ready-to-implement": "the clearing plan REVIEWER's commit, when their pass "
                          "satisfies the FINAL outstanding obligation",
    "implementing": "the first implementation commit (or, on the accepted "
                    "combined fast path, the plan-open commit that carries that "
                    "implementation)",
    "revising-code": "the CODE REVIEWER's blocking '## Code review' commit",
    "ready-to-archive": "the CODE REVIEWER's clearing '## Code review' commit, "
                        "once every closeout precondition already holds",
}


def _status_move_manifest(art: Artifact, target: str) -> List[str]:
    """The manifest for a transition that appends no new section."""
    return [
        f"Status: {art.status or '(none)'} -> {target}",
        f"NO new section is appended for this flip. It rides on "
        f"{_STATUS_MOVES_WITH[target]}.",
        "R4: 'Do not create empty commits merely to advance a label' -- if you "
        "have nothing else to commit, you are at the wrong state or the record "
        "that justifies it has not landed.",
        "(in-place status edit inside that commit; prior sections untouched.)",
    ]


def _review_template(date: str) -> str:
    """The reviewer's `## Review` section, re-homed by the vocabulary migration.

    Emitted for the two arms a landing review selects (`revising` on a
    blocking pass, `awaiting-decision` on a clearing one). Before the migration this
    lived on the retired `-> reviewed` arm and would otherwise have been
    lost: it is the only place the tool states that THE REVIEWER fills their
    own identity, which is the anti-attribution property this protects.
    """
    return (
            "## Review -- <reviewer> (<role>) -- " + date + "\n\n"
            "**Model**: <model or tier when known; 'unknown' if not>\n\n"
            "<one-paragraph orientation: who asked, what triggered the pass>\n\n"
            "**Structural-independence stance.** <author / reviewer "
            "identities; tier choice and why>\n\n"
            "**Verification done before drafting:**\n\n"
            "* <file:line reads, empirical reproducers, grep counts>\n\n"
            "**Steelman:**\n\n* <what the proposal got right>\n\n"
            "**Findings:**\n\n"
            "* **[R1] -- <title>.** <body with citations>\n\n"
            "**Covered** -- <lenses swept, each with a citation>\n"
            "**Not covered / low confidence** -- <the negative space>\n\n"
            "**Second-round recommendation**: <recommended / not, with reasons>"
    )


def _response_template(date: str) -> str:
    """The author's `## Response` + complete-current-contract revision.

    Carries the `**Scope delta**` declaration. Emitted on the return arm out
    of `revising`. Before the migration this lived on the retired `-> revised` arm; it
    is the ONLY user-reachable surface that teaches the scope-reduction
    grammar while an author is typing, so it re-homes rather than
    deletes it.
    """
    return (
            "## Response -- <author> -- " + date + "\n\n"
            "**Model**: <model or tier>\n\n"
            "For each numbered critique, one disposition token + a "
            "one-sentence rationale (proposal-Response grammar: accept / "
            "accept with modification / reject / defer):\n\n"
            "* **[R1]** <accept|accept with modification|reject|defer> -- "
            "<rationale>\n\n"
            "<Scope delta -- ONLY if this revision narrows what the "
            "proposal will deliver, judged against the scope AS OPENED. "
            "State `preserved` if you want the record to show you "
            "checked; only `degraded` and `lost` require the block "
            "below.>\n\n"
            "**Scope delta**: preserved | degraded | lost\n\n"
            "**Removed scope**\n\n"
            "* <unit> -- source section; reason; disposition (accept | "
            "guard | wontfix | defer); revival/closure condition. EACH "
            "entry needs its OWN disposition -- a shared home is a "
            "location, not a decision.\n\n"
            "**Disposition/home**: <where the grouped remainder lives>\n\n"
            "## Revised proposal -- " + date + "\n\n"
            "<ONE complete current contract, MANDATORY with every Response "
            "-- not only when the critiques were substantial. "
            "Self-contained rather than a delta: scope and exclusions, "
            "invariants, failure dispositions, public paths, evidence, "
            "omissions, deferred work. The NEWEST reviewed revision is what "
            "the Decision and the implementation bind; every earlier "
            "section stays as immutable history.>\n\n"
            "### " + _LEDGER_HEADING + "\n\n"
            "* <earlier commitment, the replacement or withdrawal, and the "
            "reason -- or a single '* None'. The heading is MANDATORY even "
            "when its value is None: only a written None distinguishes "
            "'nothing was withdrawn' from 'nobody checked'.>"
    )


def _scaffold(art: Artifact, target: str, date: str) -> Tuple[str, str, List[str]]:
    """Return (status_from, status_to_or_note, [scaffold_block, manifest...]).

    **A status-move target may still carry a section template, and two must.**
    These flips append no section *of their own* -- they ride on someone
    else's commit.  But the author writing that commit still needs its grammar,
    and before the migration the only place it existed was the retired `-> reviewed` and
    `-> revised` arms.  Retiring those without re-homing their templates would
    have deleted, from every user-reachable path, the one surface that teaches
    the `**Scope delta**` declaration while an author is typing -- which is
    `scope-reduction-trap`'s whole mechanism, and another plan's accepted scope.
    So the templates move to the live arms that carry the same authorial moment:
    the reviewer's `## Review` to the two arms a review selects, and the
    author's `## Response` + revision (carrying `Scope delta`) to the return arm
    out of `revising`.  See the re-homing notes in
    `dev/plans/review-efficient-lifecycle.md`.
    """
    k = art.kind
    if target in _STATUS_MOVES_WITH:
        manifest = _status_move_manifest(art, target)
        if k == "proposal" and target in ("revising", "awaiting-decision"):
            return (art.status, target, [_review_template(date)] + manifest)
        if (k == "proposal" and target == "awaiting-review"
                and art.status == "revising"):
            # Only the RETURN arm. The proposal-open arm has nothing to revise.
            #
            # The caveat below travelled with the retired `-> revised` arm's
            # MANIFEST, not with its block, so re-homing the template alone
            # dropped it -- caught by `test_scope_reduction_trap.py`, which
            # exists to fail on exactly this silent-deletion shape rather than
            # on a rewording. It is doctrine, not decoration: the tool must say
            # that it does not enforce the declaration, or an author may read
            # a green transition as the declaration having been checked.
            return (art.status, target, [_response_template(date)] + manifest + [
                "accepted scope is a FLOOR. NO TRANSITION REFUSES ON A MISSING "
                "OR MALFORMED DECLARATION -- review is the enforcement, "
                "including for whether a declaration is TRUE.",
            ])
        return (art.status, target, manifest)
    if k == "proposal":
        if target in ("accepted", "rejected", "superseded"):
            block = (
                "## Decision -- <Maintainer> -- " + date + "\n\n"
                f"**{target.capitalize()}**, <one-line disposition>.\n\n"
                "*Maintainer authorization (verbatim):*\n\n"
                "> <paste the Maintainer's verbatim authorization here -- this "
                "tool cannot certify it; the committing operator is the sole "
                "guarantor of authenticity>\n\n"
                "*Scribed by <agent> at the Maintainer's explicit instruction; "
                "this is a Decision-only commit -- Status flips and this section "
                "is appended, nothing else.*"
            )
            archive_note = (
                "this Decision commit also moves the file to archive/."
                if target in ("rejected", "superseded")
                else "an accepted proposal stays in dev/proposals/ (archive moves "
                     "later, at plan-open or the trivial-implementing commit)."
            )
            manifest = [
                f"Status: -> {target}",
                "append the '## Decision' section above; Decision-only commit "
                "(touches nothing but this section).",
                "the verbatim-authorization blockquote MUST be filled by the "
                "operator -- the tool emits an empty placeholder and never "
                "invents an authorization.",
                archive_note,
            ]
            return ("reviewed/revised", target, [block] + manifest)
    else:  # plan
        if target == "awaiting-plan-review":
            if target == "awaiting-plan-review" and art.status != "revising-plan":
                # The plan-OPEN arm: nothing to revise yet.
                manifest = [
                    f"Status: {art.status or '(none)'} -> awaiting-plan-review",
                    "no section to append yet -- the plan waits for its "
                    "'## Plan review' section to land before implementation.",
                    "(in-place status edit; plans are execution artifacts.)",
                ]
                return (art.status, "awaiting-plan-review", manifest)
            # The author's Sharpening RETURN arm, `revising-plan ->
            # awaiting-plan-review`.  The migration re-homed the plan-side `Scope delta`
            # surface here: it previously lived only on `-> executing`, which
            # the retirement made unreachable, and losing it would have deleted
            # the plan half of scope-reduction-trap's mechanism.  Exactly
            # parallel to the proposal side, where the same declaration sits on
            # `revising -> awaiting-review`: both are the arm on which an AUTHOR
            # answers a review, which is the moment scope can quietly narrow.
            block = (
                "## Plan review -- <reviewer> -- " + date + "\n\n"
                "**Tier**: <Internal|External>\n"
                "**Findings**: <none|raised>\n\n"
                "**Model**: <model or tier>\n\n"
                "<orientation> **Findings:** ... **Coverage + second-round "
                "recommendation:** ...\n\n"
                "### Sharpening -- <author> -- " + date + "\n\n"
                "<dispositions on the findings, if any>\n\n"
                "<Scope delta -- ONLY if a disposition here narrows what the "
                "plan will deliver, judged against the scope AS ACCEPTED. "
                "Sequencing between chunks owes nothing; removing an accepted "
                "outcome is a deviation under AGENTS.md. State `preserved` if "
                "you want the record to show you checked; only `degraded` and "
                "`lost` require the block below.>\n\n"
                "**Scope delta**: preserved | degraded | lost\n\n"
                "**Removed scope**\n\n"
                "* <unit> -- source section; reason; disposition (accept | "
                "guard | wontfix | defer); revival/closure condition. EACH "
                "entry needs its OWN disposition -- a shared home is a "
                "location, not a decision.\n\n"
                "**Disposition/home**: <where the grouped remainder lives>"
            )
            manifest = [
                "Status: revising-plan -> awaiting-plan-review",
                "accepted scope is a FLOOR: a Sharpening that removes an "
                "accepted outcome needs the Maintainer's explicit disposition "
                "under the deviation gate. A plan reviewer cannot create that "
                "authority by calling the remainder 'out of scope'. NO "
                "TRANSITION REFUSES ON A MISSING OR MALFORMED DECLARATION -- "
                "review is the enforcement, including for whether a declaration "
                "is TRUE.",
                "for a review-required plan, the '## Plan review' section (+ "
                "Sharpening if findings) must have landed first; plan-open and "
                "first-implementation commits stay distinct.",
                "review/Sharpening sections are append-only.",
            ]
            return ("revising-plan", "awaiting-plan-review", [block] + manifest)
        if target == "awaiting-code-review":
            block = (
                "## Implementation verification -- <agent> -- " + date + "\n\n"
                "**Boundary B mode**: full | bounded\n\n"
                "* **Range**: <tested SHA or range>   **Interpreter**: "
                "<python X.Y.Z>\n"
                "* **Clean tree**: <pre/post state, verified not assumed>\n"
                "* **Commands + outcomes**: <each command, its raw result, "
                "timing>\n"
                "* **Non-pass disposition**: <every non-pass outcome, or 'none'>\n"
                "* **Known omissions**: <what was NOT run, and why>\n\n"
                "<On 'bounded': name the touched surfaces, the reviewed mapping "
                "and gates run, why the effects are bounded, and the explicit "
                "absence of any contract or trust-ceremony surface.>"
            )
            manifest = [
                f"Status: {art.status or '(none)'} -> awaiting-code-review",
                "append the '## Implementation verification' record above -- THAT "
                "record is what makes this state true, so the flip rides on its "
                "commit (R4).",
                "returning here from 'revising-code' takes a REPLACEMENT record "
                "over the corrected range: one that comes after the blocking "
                "'## Code review' pass, not the one that pass already read.",
                "the tool checks the heading and its date. It does not read the "
                "evidence inside, and cannot: whether the suite really ran is "
                "carried by the committing operator.",
            ]
            return (art.status, "awaiting-code-review", [block] + manifest)
        if target == "review":
            block = (
                "## Code review -- <reviewer> -- " + date + "\n\n"
                "**Model**: <model or tier>\n\n"
                "<the reviewer is NOT the implementing agent.> Findings as a "
                "numbered list with accept(commit <sha>)/defer/wontfix "
                "dispositions. A clean final review carries a falsification "
                "ledger. End with the coverage line + recommendation."
            )
            manifest = [
                "Status: executing -> review",
                "append the '## Code review' section; append-only.",
            ]
            return ("executing", "review", [block] + manifest)
        if target == "archived":
            block = (
                "## Lasting-truth migration -- " + date + "\n\n"
                "Dispositions:\n"
                "* <item> -> accept | guard (<path>::<node>) | wontfix (<why>)\n"
                "* <item> -> defer -> dev/PLANNING.md > <section>"
                "   [Maintainer: \"<quote>\"]\n\n"
                "  (no follow-ups? write `Dispositions: none` -- the gate "
                "requires an attestation either way)\n\n"
                "**Evidence shipped** / **Evidence deferred** / **Deferred "
                "evidence home**: ...\n\n"
                "**Fidelity sign-off** -- the landed implementation commit(s) "
                "<sha> match the accepted Revised section <name>."
            )
            manifest = [
                f"Status: {art.status or 'ready-to-archive'} -> archived; move "
                "the file to dev/plans/archive/.",
                "the plan-archive commit is DISTINCT from the implementing "
                "commits (proves review happened).",
                "every deferred follow-up carries a recorded disposition, "
                "named in the 'Dispositions:' block, with any 'defer' carrying "
                "the Maintainer's quoted authorization; the fidelity sign-off "
                "names the implementing commit + governing section.",
            ]
            return (art.status or "ready-to-archive", "archived",
                    [block] + manifest)
    # Fallback (should be unreachable given _legal_transitions gating).
    return (art.status, target, [f"no scaffold defined for -> {target}."])


# --- subcommand: next --------------------------------------------------------


def cmd_next(args: argparse.Namespace) -> int:
    """Report state + legal transitions (+ unmet preconditions), or scaffold."""
    root = _repo_root()
    path = Path(args.artifact)
    if not path.is_absolute():
        path = (Path.cwd() / path)
    art = _read_artifact(path)
    identity = _load_identity_model(root)
    date = args.date or _today()

    _emit_section(f"{art.kind}: {art.path.name}")
    _emit(f"current state: {art.status or '(no status line)'}")

    # Surface any current-state structural violations up front.
    violations = _conformance_violations(art, identity)
    if violations:
        _emit_section("structural conformance (current state)")
        for msg in violations:
            _emit(f"VIOLATION: {msg}")
    else:
        _emit("structural conformance: current state is structurally sound.")

    legal = _legal_transitions(art)

    if not args.to:
        _emit_section("legal next transitions")
        if not legal:
            _emit("(terminal state -- no status transition; any archive move is a "
                  "file operation, not a status flip.)")
            return 0
        for target in legal:
            _emit(f"-> {target}")
            for met, desc in _gating_preconditions(art, target, identity):
                mark = "ok " if met else "MISSING"
                _emit(f"     [{mark}] {desc}")
        _emit("")
        _emit("re-run with --to <state> to emit a proposed scaffold + manifest.")
        return 0

    # --to <state>: validate legality, report gates, emit scaffold + manifest.
    target = args.to
    if target not in legal:
        _emit_section("requested transition is not legal")
        _emit(f"-> {target} is not a legal next transition from "
              f"{art.status or '(none)'}.")
        _emit(f"legal targets: {', '.join(legal) if legal else '(none)'}")
        return 1

    gates = _gating_preconditions(art, target, identity)
    unmet = [desc for met, desc in gates if not met]
    _emit_section(f"transition -> {target}: gating preconditions")
    for met, desc in gates:
        _emit(f"[{'ok ' if met else 'MISSING'}] {desc}")
    if unmet:
        _emit("")
        _emit("NOTE: one or more gating preconditions are structurally MISSING. "
              "This scaffold prepares the transition, but the tool does NOT "
              "present it as ready -- supply the missing attestation first.")

    status_from, status_to, blocks = _scaffold(art, target, date)
    _emit_section("proposed section scaffold (copy into the artifact)")
    # The scaffold block is the first element; manifest lines follow.
    print(blocks[0])
    _emit_section("mutation manifest (what would change -- you apply it)")
    for line in blocks[1:]:
        _emit(f"- {line}")
    _emit("")
    _emit("read-only: this tool emitted text only. It wrote nothing and "
          "committed nothing. You own the edit and the commit.")
    return 0


# --- subcommand: scan (also the adopter fidelity scan) -----------------------


def cmd_scan(args: argparse.Namespace) -> int:
    """Run structural conformance over the local dev/ corpus; report violations.

    This is the read-only checker doing double duty as the **adopter-side
    fidelity scan**: the same structural checks `next` reports per
    artifact, run across `dev/proposals/` + `dev/plans/` (live files).  Exit
    code is non-zero when any violation is found, so an adopter test wrapper
    can assert a clean corpus.

    **Two modes, and the default is deliberately live-only.**

    * *default* -- live `dev/proposals/` + `dev/plans/`.  These are artifacts
      someone can still fix, so a violation here is actionable.
    * `--include-archive` -- adds `dev/plans/archive/` and
      `dev/proposals/archive/`.  This is the **explicit strict historical
      audit**, not the routine gate.  Archived records are immutable history:
      most predate the rules they are now measured against, and a gate that
      reds permanently on records nobody may edit is one people learn to
      ignore -- which is the failure this checker exists to prevent, one level
      up.  Its findings are a **drainable backlog**, recorded dated in the
      plan that measured them, never suppressed into a baseline.

    Exit semantics are the same in both modes: non-zero when anything is
    flagged.  `--include-archive` is louder by design, and that is why it is
    opt-in rather than silently folded into the default.

    **Nothing invokes `--include-archive`, and that is correct.**  No CI job,
    no script, no gate runs it; its only trigger is an operator typing it.  It
    is named here rather than left implied, because a check whose trigger is a
    human remembering must be described that way.

    It is a **development-time instrument for validating a predicate**, not a
    recurring audit.  Run it when a predicate changes: a large movement in the
    flagged count means the predicate moved, which is what you want to know
    *before* shipping it.  Every defect this checker's own archive sweeps have
    caught was a fact about the code -- a false pass, a false fail, a bad
    measuring oracle -- and none was a request to edit a historical record.

    **Enforcement is forward-only.**  Archived records are immutable and are
    not retro-fitted; the pre-transition gates above are what prevent new
    instances.  So the flagged count is a measurement, never a debt, and
    nothing should be built that re-scans history on a schedule -- a
    permanently-red recurring gate over records nobody may edit is the failure
    this checker exists to prevent, one level up."""
    root = _repo_root()
    identity = _load_identity_model(root)
    total = 0
    flagged = 0
    bases = []
    for kind_dir in ("proposals", "plans"):
        base = root / "dev" / kind_dir
        if base.is_dir():
            bases.append(base)
    _emit_section("lifecycle conformance scan")
    for base in bases:
        globs = sorted(base.glob("*.md"))
        if args.include_archive and (base / "archive").is_dir():
            globs += sorted((base / "archive").glob("*.md"))
        for path in globs:
            if path.name in ("_template.md", "README.md"):
                continue
            total += 1
            try:
                art = _read_artifact(path)
            except PlannerError as exc:
                flagged += 1
                _emit(f"{path.relative_to(root)}: UNREADABLE -- {exc}")
                continue
            violations = _conformance_violations(art, identity)
            if violations:
                flagged += 1
                rel = path.relative_to(root)
                for msg in violations:
                    _emit(f"{rel}: {msg}")
    _emit("")
    if flagged:
        _emit(f"{flagged} of {total} artifact(s) carry structural violations.")
        return 1
    _emit(f"all {total} artifact(s) structurally sound (no contract violations).")
    return 0


# --- subcommand: guard (advisory pre-commit orientation) --------------------


def cmd_guard(args: argparse.Namespace) -> int:
    """Advisory pre-commit pass -- warns, never blocks.

    Summarizes the staged set, runs `claim_check` on staged `dev/` docs if
    it is installed, and reminds that the **shipped work-intent hook** is
    the *blocking* layer (this tool adds no new blocking enforcement, and
    promoting `claim_check` to a fail-closed gate is a separate, gated
    decision -- out of scope here)."""
    root = _repo_root()
    _emit_section("advisory pre-commit guard (warns; never blocks)")

    staged = _git_readonly(["diff", "--cached", "--name-only"], root)
    if staged is None:
        _warn("could not read the staged set (git unavailable?) -- skipping.")
        return 0
    files = [f for f in staged.splitlines() if f.strip()]
    if not files:
        _emit("no staged changes.")
        return 0
    _emit(f"staged paths ({len(files)}):")
    for f in files:
        _emit(f"  {f}")

    # Path-scope sanity: a single mixed-purpose commit is the failure class
    # the exact-diff protocol guards against -- surface it, do not block.
    top = {f.split("/", 1)[0] for f in files}
    if len(top) > 1:
        _emit(f"NOTE: staged paths span multiple top-level areas ({', '.join(sorted(top))}); "
              "confirm this is one coherent transition, not a bundled commit.")

    # claim_check on staged dev/ docs, if the tool is installed (advisory).
    dev_docs = [f for f in files if f.startswith("dev/") and f.endswith(".md")]
    claim_check = root / "tools" / "claim_check.py"
    if dev_docs and claim_check.is_file():
        _emit("running claim_check on staged dev/ docs (advisory)...")
        proc = subprocess.run(
            [sys.executable, str(claim_check), *dev_docs],
            cwd=str(root), capture_output=True, text=True, check=False,
            env=_git_env(),
        )
        if proc.stdout.strip():
            for line in proc.stdout.splitlines():
                _emit(f"  claim_check: {line}")
        if proc.returncode != 0:
            _emit("NOTE: claim_check reported flags above (advisory -- not a "
                  "block here; resolve or mark before committing).")
    elif dev_docs:
        _warn("tools/claim_check.py not installed -- skipping the staged-doc "
              "claim check (advisory step).")

    _emit("")
    _emit("the *blocking* layer is the shipped work-intent pre-commit hook "
          "(cross-claim enforcement); this guard adds no new blocking.")
    return 0


# =============================================================================
# the derived orientation board
# =============================================================================
#
# **What the board IS**: a read-only projection over the same parser and
# predicates `scan`, `next` and closeout use.  **What it is NOT**: a roadmap, a
# queue, a priority engine, a review attestation, or a source of lifecycle
# truth.  Nothing is written and nothing is cached; every invocation derives
# fresh output and names the HEAD it observed.
#
# Five properties are load-bearing, and each is enforced below rather than
# asserted here:
#
#   * one row per active artifact, including its active work-intent;
#   * `--format json`, filters and `--explain`, so the view is scriptable;
#   * **one parser, one pass, no cache** -- a second reading of the corpus is
#     how a derived view comes to disagree with the thing it derives from;
#   * the work-intent provider is *optional* and stacked on top of that rule,
#     never a second parse and never a hard dependency;
#   * one terminal encoder, because a row that can move the cursor or add a
#     column is a row that can misrepresent the corpus on a terminal.

# --- the one terminal encoder -------------------------------------------------

#: The board's serialization guard, **not** a detector policy.  Its population
#: covers the union represented by content scan's `_ZERO_WIDTH`, `_BIDI`,
#: `_LINE_SEPARATORS`, `_IGNORABLE_RANGES`, `_NONCHARACTER_RANGES`, `_TAG_RANGE`
#: and `_ASCII_GUARD` -- duplicated deliberately, because the board must not
#: import the *conditional* content scanner at runtime (it is not installed in
#: every adopter tree).  The duplication is admitted only with the **one-way**
#: drift guard in `bootstrap/tests/test_lifecycle_board.py`: the board may escape
#: more than the scanner flags, and may never emit raw a code point the scanner
#: recognizes.  So a newly added printable invisible reddens that test until this
#: table follows it, and narrowing a detector cannot quietly weaken this output.
#:
#: **Numeric endpoints only -- no invisible source character is embedded raw.**
#: That is a contract clause, not a style preference: a table written with
#: literal members would make this file carry the very code points it exists to
#: escape (the same reason content scan holds its own ranges numerically).
#:
#: Rows mirror the scanner's own row identities rather than being merged into the
#: fewest possible spans, so a reader can check coverage row-against-row.
_DISPLAY_UNSAFE_RANGES: Tuple[Tuple[int, int], ...] = (
    (0x00AD, 0x00AD),      # SOFT HYPHEN -- also content scan's _ASCII_GUARD
    (0x034F, 0x034F),      # COMBINING GRAPHEME JOINER (Mn -- printable!)
    (0x061C, 0x061C),      # ARABIC LETTER MARK
    (0x115F, 0x1160),      # HANGUL CHOSEONG / JUNGSEONG FILLER (Lo -- printable!)
    (0x17B4, 0x17B5),      # KHMER VOWEL INHERENT AQ / AA
    (0x180B, 0x180F),      # MONGOLIAN free variation selectors + vowel separator
    (0x200B, 0x200F),      # ZWSP..RLM (zero-width set + LRM/RLM)
    (0x2028, 0x2029),      # LINE / PARAGRAPH SEPARATOR
    (0x202A, 0x202E),      # bidi embeddings / overrides
    (0x2060, 0x206F),      # WORD JOINER, invisible operators, isolates
    (0x3164, 0x3164),      # HANGUL FILLER (Lo -- printable!)
    (0xFDD0, 0xFDEF),      # noncharacters in Arabic Presentation Forms-A
    (0xFE00, 0xFE0F),      # VARIATION SELECTOR-1..16 (Mn -- printable!)
    (0xFEFF, 0xFEFF),      # ZERO WIDTH NO-BREAK SPACE / BOM
    (0xFFA0, 0xFFA0),      # HALFWIDTH HANGUL FILLER (Lo -- printable!)
    (0xFFF0, 0xFFF8),      # reserved
    (0xFFFE, 0xFFFF),      # plane-0 noncharacters
    (0x1BCA0, 0x1BCA3),    # SHORTHAND FORMAT letters
    (0x1D173, 0x1D17A),    # MUSICAL SYMBOL BEGIN BEAM..END PHRASE
    (0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF), (0x3FFFE, 0x3FFFF),
    (0x4FFFE, 0x4FFFF), (0x5FFFE, 0x5FFFF), (0x6FFFE, 0x6FFFF),
    (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF), (0x9FFFE, 0x9FFFF),
    (0xAFFFE, 0xAFFFF), (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF),
    (0xDFFFE, 0xDFFFF),
    (0xE0000, 0xE0FFF),    # the Tag block (a shadow ASCII alphabet) + VS-17..256
    (0xEFFFE, 0xEFFFF), (0xFFFFE, 0xFFFFF), (0x10FFFE, 0x10FFFF),
)

#: Derived from the table, never written as a literal, so it cannot go stale:
#: every covered code point is at or above this, so the range walk below is
#: skipped for anything under it with an identical hit set.
_DISPLAY_UNSAFE_FLOOR = min(lo for lo, _hi in _DISPLAY_UNSAFE_RANGES)

#: The compact projection's syntax.  A field value that contained one of these
#: raw could add a column or a row.  They are escaped by the same
#: encoder as everything else, so there is no second escaping rule to keep in
#: step.  (`\n`/`\r`/`\t` are already non-printable, hence redundant with clause
#: 1; naming them here makes the delimiter property assertable on its own.)
_BOARD_FIELD_DELIMITER = "|"
_BOARD_ROW_DELIMITER = "\n"
_DISPLAY_SYNTAX_CHARS = frozenset(
    (_BOARD_FIELD_DELIMITER, _BOARD_ROW_DELIMITER, "\\", "\r", "\t"))


def _display_unsafe_code_point(code_point: int) -> bool:
    """Is *code_point* in `_DISPLAY_UNSAFE_RANGES`?"""
    if code_point < _DISPLAY_UNSAFE_FLOOR:
        return False
    for low, high in _DISPLAY_UNSAFE_RANGES:
        if low <= code_point <= high:
            return True
    return False


def _escape_code_point(char: str) -> str:
    """One printable-ASCII code-point escape.  ANSI ESC never survives raw."""
    code_point = ord(char)
    if code_point < 0x100:
        return f"\\x{code_point:02x}"
    if code_point < 0x10000:
        return f"\\u{code_point:04x}"
    return f"\\U{code_point:08x}"


def encode_display(value: str) -> str:
    """The **one** terminal encoder.

    For each represented code point emit a printable ASCII code-point escape
    when any of these is true:

    1. ``str.isprintable()`` is false;
    2. the code point belongs to `_DISPLAY_UNSAFE_RANGES`; or
    3. it is a row delimiter, field delimiter, backslash, or other syntax
       character whose raw form could alter the compact representation.

    Clause 1 alone was the *rejected* design: the
    combining grapheme joiner, the Hangul fillers and the variation selectors are
    `Mn`/`Lo`, so ``isprintable()`` calls them printable while they are invisible
    on a terminal.  Clause 2 is what closes that residual, and it is why the
    range table exists at all rather than a category sweep.

    Filenames, lifecycle metadata, Git labels and optional intent fields all pass
    through here -- one encoder, so there is no second path with a weaker rule.
    Ordinary printable scientific text is untouched: ASCII space, precomposed
    accented letters, Greek and CJK all survive readable.
    """
    out: List[str] = []
    for char in value:
        if (not char.isprintable()
                or char in _DISPLAY_SYNTAX_CHARS
                or _display_unsafe_code_point(ord(char))):
            out.append(_escape_code_point(char))
        else:
            out.append(char)
    return "".join(out)


# --- the optional work-intent provider ---------------------------------------

#: The versioned machine contract `tools/_intent/cli.py` emits for `list
#: --format json`.  The board consumes **only** this; it never scrapes the human
#: form, and a mismatch is a provider error rather than a best-effort parse.
INTENT_LIST_SCHEMA = "cairn-intent-list/1"

#: The launcher the board looks for beside itself.  Never imported: the intent
#: engine is a *team-gated* module and the board is default-on, so an import
#: would make the default-on planner depend on an optional module (forbidden
#: exactly that).  A bounded subprocess keeps the dependency one-way.
_INTENT_LAUNCHER_NAME = "intent.py"

#: One bounded query per board, under a wall-clock ceiling.  A hung provider
#: must degrade to a labelled `error` row, never wedge an orientation command.
_INTENT_QUERY_TIMEOUT = 10.0

INTENT_AVAILABLE = "available"
INTENT_NOT_INSTALLED = "not-installed"
INTENT_ERROR = "error"

#: Stable reason codes.  Each named failure mode in the accepted contract gets
#: its **own** code -- "the provider broke" is not a disposition an operator can
#: act on, and collapsing them is how a timeout comes to look like a schema bug.
INTENT_REASON_CODES = (
    "launcher-symlink",          # the leaf is a symlink (any target)
    "launcher-out-of-directory",  # resolves outside the expected tools/ dir
    "launcher-not-regular",      # present but not a regular file
    "no-interpreter",            # sys.executable is unusable
    "spawn-failed",              # OSError starting the child
    "timeout",                   # exceeded _INTENT_QUERY_TIMEOUT
    "nonzero-exit",              # the provider exited non-zero
    "malformed-json",            # stdout is not JSON, or not an object
    "schema-mismatch",           # wrong or absent schema version
    "invalid-record",            # a missing or wrongly-typed field
    "duplicate-id",              # two records share a claim id
    "invalid-path",              # a file entry is not a safe relative path
)

_INTENT_RECORD_TEXT_FIELDS = ("id", "agent", "ts", "action")


def _intent_launcher() -> Tuple[Optional[Path], Optional[str], str]:
    """Locate the provider launcher -> ``(path, reason_code, detail)``.

    The full accepted containment clause: *"The planner locates only a regular,
    non-symlinked `tools/intent.py` beside itself, refuses an out-of-directory
    resolution"*.

    **The candidate is derived from the UNRESOLVED ``__file__``**, and that is
    the load-bearing part (the lesson of `94bda8b`): a resolved path is never a
    symlink, so deriving from `Path(__file__).resolve()` would make the symlink
    refusal below **dead by construction** -- it would be a guard that can never
    fire, which is worse than no guard because it reads as protection.
    Containment is then compared between **resolved** forms, so a symlinked
    *ancestor* -- macOS's `/tmp -> private/tmp` is the one every test run hits --
    is not a false refusal.

    A missing launcher is `not-installed` (``(None, None, ...)``), which is not
    an error: the coordination module is optional by contract.  Everything else
    that is *present but wrong* is an error with its own code.
    """
    here = Path(__file__).parent
    candidate = here / _INTENT_LAUNCHER_NAME
    # Order matters: `is_symlink` is the only check that sees a *broken* symlink,
    # and it must run before `is_file` (which follows the link and would report a
    # broken one as simply absent -- laundering a planted symlink into
    # `not-installed`).
    if candidate.is_symlink():
        return None, "launcher-symlink", (
            f"{_INTENT_LAUNCHER_NAME} beside the planner is a symlink; the "
            "provider launcher must be a regular file in the expected directory")
    if not candidate.exists():
        return None, None, "no work-intent launcher beside the planner"
    if not candidate.is_file():
        return None, "launcher-not-regular", (
            f"{_INTENT_LAUNCHER_NAME} beside the planner is not a regular file")
    try:
        resolved = candidate.resolve()
        expected = here.resolve()
    except OSError as exc:
        return None, "launcher-out-of-directory", f"cannot resolve: {exc}"
    if resolved.parent != expected:
        return None, "launcher-out-of-directory", (
            f"{_INTENT_LAUNCHER_NAME} resolves to {resolved} whose parent is not "
            f"the expected directory {expected}")
    return candidate, None, str(candidate)


def _intent_argv(launcher: Path) -> List[str]:
    """The **fixed** argv, isolated mode, versioned JSON.  No shell, ever.

    ``-I`` is Python's isolated mode: no `sys.path[0]` injection, no user site
    directory, and `PYTHON*` environment variables ignored -- so the child cannot
    be redirected by ambient state into importing something else.  The subcommand
    and format are literals; no artifact content, filename, or filter value ever
    reaches this list, so there is nothing for a crafted artifact to influence.
    """
    return [sys.executable, "-I", str(launcher), "list", "--format", "json"]


def _intent_valid_relative_path(value: object) -> bool:
    """Is *value* a safe repo-relative POSIX path, as the engine normalizes?

    Refuses: a non-string, an empty string, a NUL, a backslash, an absolute or
    drive-qualified path, and any empty / `.` / `..` component.  A path is the
    **key** the board joins claims to artifacts on, so a traversal component here
    is a wrong-row hazard, not a cosmetic defect.  Display safety is *not* this
    predicate's job -- `encode_display` owns that, and one rule per concern is
    what keeps either from being weakened to satisfy the other.
    """
    if not isinstance(value, str) or not value:
        return False
    if "\x00" in value or "\\" in value:
        return False
    if value.startswith("/"):
        return False
    if len(value) > 1 and value[1] == ":":
        return False
    return all(part not in ("", ".", "..") for part in value.split("/"))


def _intent_validate(payload: object) -> Tuple[Optional[str], str,
                                               List[Dict[str, object]]]:
    """Validate the whole payload BEFORE any record is used.

    *"Complete field, type and path validation of every record before any is
    used"* -- so this returns either a reason code and no records, or no reason
    code and every record.  A partial accept would let one crafted entry poison
    the rows that validated, which is the shape the contract forbids by
    requiring the all-or-nothing form.
    """
    if not isinstance(payload, dict):
        return "malformed-json", "provider output is not a JSON object", []
    if payload.get("schema") != INTENT_LIST_SCHEMA:
        return "schema-mismatch", (
            f"provider declares schema {payload.get('schema')!r}; this board "
            f"reads {INTENT_LIST_SCHEMA!r} only"), []
    claims = payload.get("claims")
    if not isinstance(claims, list):
        return "invalid-record", "'claims' is not a list", []
    out: List[Dict[str, object]] = []
    seen_ids: Set[str] = set()
    for index, record in enumerate(claims):
        if not isinstance(record, dict):
            return "invalid-record", f"claim {index} is not an object", []
        for field in _INTENT_RECORD_TEXT_FIELDS:
            value = record.get(field)
            if not isinstance(value, str) or not value:
                return "invalid-record", (
                    f"claim {index} field {field!r} is missing or not a "
                    "non-empty string"), []
        stem = record.get("stem", "")
        if stem is not None and not isinstance(stem, str):
            return "invalid-record", f"claim {index} field 'stem' is not text", []
        files = record.get("files")
        if not isinstance(files, list) or not files:
            return "invalid-record", (
                f"claim {index} field 'files' is missing or not a non-empty "
                "list"), []
        for entry in files:
            if not _intent_valid_relative_path(entry):
                return "invalid-path", (
                    f"claim {index} carries an unsafe file entry {entry!r}"), []
        claim_id = str(record.get("id"))
        if claim_id in seen_ids:
            return "duplicate-id", (
                f"two active claims share id {claim_id!r}; the provider's "
                "reduction is not authoritative"), []
        seen_ids.add(claim_id)
        out.append({
            "id": claim_id,
            "agent": str(record.get("agent")),
            "ts": str(record.get("ts")),
            "action": str(record.get("action")),
            "stem": str(stem or ""),
            "files": [str(entry) for entry in files],
        })
    return None, "", out


def query_intent_provider(root: Path) -> Dict[str, object]:
    """**One** bounded query for the whole board.

    Returns ``{"state", "reason", "detail", "claims", "calls"}``.  `state` is one
    of `available` / `not-installed` / `error`; `calls` is the number of
    subprocesses actually started, which is what the board's
    one-subprocess-per-board property is asserted against.

    Every distinct failure mode in the accepted contract gets its own reason
    code, and **no** failure mode is allowed to read as "nobody holds a claim":
    that is the one inference the board must never make, because it would turn a
    broken provider into a green light to edit a file another session owns.
    """
    result: Dict[str, object] = {
        "state": INTENT_NOT_INSTALLED, "reason": None, "detail": "",
        "claims": [], "calls": 0,
    }
    launcher, reason, detail = _intent_launcher()
    if reason is not None:
        result.update(state=INTENT_ERROR, reason=reason, detail=detail)
        return result
    if launcher is None:
        result["detail"] = detail
        return result
    if not sys.executable:
        result.update(state=INTENT_ERROR, reason="no-interpreter",
                      detail="the running interpreter is not resolvable, so the "
                             "provider cannot be invoked in isolated mode")
        return result
    try:
        result["calls"] = 1
        proc = subprocess.run(
            _intent_argv(launcher), cwd=str(root), capture_output=True,
            text=True, check=False, shell=False, env=_git_env(),
            timeout=_INTENT_QUERY_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        result.update(state=INTENT_ERROR, reason="timeout",
                      detail=f"provider exceeded {_INTENT_QUERY_TIMEOUT:g}s")
        return result
    except OSError as exc:
        result.update(state=INTENT_ERROR, reason="spawn-failed",
                      detail=f"cannot start the provider: {exc}")
        return result
    if proc.returncode != 0:
        result.update(state=INTENT_ERROR, reason="nonzero-exit",
                      detail=f"provider exited {proc.returncode}")
        return result
    try:
        payload = json.loads(proc.stdout)
    except ValueError as exc:
        result.update(state=INTENT_ERROR, reason="malformed-json",
                      detail=f"provider stdout is not JSON: {exc}")
        return result
    reason, detail, claims = _intent_validate(payload)
    if reason is not None:
        result.update(state=INTENT_ERROR, reason=reason, detail=detail)
        return result
    result.update(state=INTENT_AVAILABLE, claims=claims)
    return result


def _intent_index(claims: List[Dict[str, object]]) -> Dict[str, List[Dict]]:
    """``normalized path -> claims touching it``, built once for the whole board."""
    index: Dict[str, List[Dict]] = {}
    for claim in claims:
        for entry in claim.get("files", []):  # type: ignore[union-attr]
            index.setdefault(str(entry), []).append(claim)
    return index


# --- the row contract --------------------------------------------------------

#: The versioned top-level JSON schema.  Bumped, never widened silently.
BOARD_SCHEMA_VERSION = "cairn-lifecycle-board/1"

#: The documented stable field order, verbatim and in order.  `owner` and
#: `active_intent` are two fields and never collapse into one: a claim is
#: *someone is editing this*, an owner is *whose move it is*, and merging them
#: would let a claim read as authority.
BOARD_FIELDS = ("kind", "artifact", "status", "owner", "active_intent",
                "review", "evidence", "blocked_by", "validity", "source")

#: Rows sort by artifact kind then filename stem.  Kind order is declared
#: rather than alphabetical so it matches the order `scan` walks the tree in.
BOARD_KIND_ORDER = ("proposal", "plan")

BOARD_ABSENT = "-"
BOARD_VALID = "valid"

#: `validity`'s stable reason codes.  Classification is by **condition**, not by
#: matching the wording of a violation message: a message-matching classifier
#: silently degrades to "unrecognized" the moment a predicate rewords itself,
#: and the fail-safe direction has to be preserved deliberately.  Whether a row
#: is invalid at all is decided by `_conformance_violations` alone, so a
#: predicate this classifier does not know about still lands the row on `other`
#: -- never on `valid`.
BOARD_REASON_CODES = (
    BOARD_VALID,
    "unreadable",          # the parser refused the file outright
    "status-vocabulary",   # missing status, or a token outside the vocabulary
    "status-evidence",     # a status/evidence contradiction
    "declaration",         # a declaration or binding defect
    "blocked-by",          # the optional blocker field, malformed
    "review-floor",        # the mandatory '**Plan review**:' line is absent
    "other",               # flagged by a predicate this table does not name
)

BOARD_SOURCE_HEAD = "HEAD"
BOARD_SOURCE_DIRTY = "WT-dirty"
BOARD_SOURCE_UNTRACKED = "WT-untracked"

#: *"The board treats a Git failure as an explicit unbound-source condition;
#: it does not silently label working-tree content as HEAD."*  This is a label,
#: not an exit condition -- an unborn HEAD is a legitimate repository state, and
#: the honest report is "I cannot bind these bytes to a commit", loudly, in every
#: row.
BOARD_SOURCE_UNBOUND = "WT-unbound"

BOARD_SOURCES = (BOARD_SOURCE_HEAD, BOARD_SOURCE_DIRTY, BOARD_SOURCE_UNTRACKED,
                 BOARD_SOURCE_UNBOUND)

_BOARD_SKIP_NAMES = ("_template.md", "README.md")


def _board_artifact_paths(root: Path) -> List[Tuple[str, Path]]:
    """``(kind, path)`` for every active direct child, excluding templates.

    Direct children only, and no archive tree: the board is scoped to *"active
    direct child of `dev/proposals/` and `dev/plans/`, excluding templates and
    archived trees"*.  Archived records are immutable history; a board that
    listed them would be an audit, which `scan --include-archive` already is.
    """
    out: List[Tuple[str, Path]] = []
    for kind, folder in (("proposal", "proposals"), ("plan", "plans")):
        base = root / "dev" / folder
        if not base.is_dir():
            continue
        for path in sorted(base.glob("*.md")):
            if path.name in _BOARD_SKIP_NAMES:
                continue
            out.append((kind, path))
    return sorted(out, key=lambda item: (BOARD_KIND_ORDER.index(item[0])
                                         if item[0] in BOARD_KIND_ORDER else 99,
                                         item[1].stem))


def _board_git_state(root: Path) -> Tuple[Optional[str], bool, Set[str], Set[str]]:
    """Repository state in a **bounded batch** -> ``(head, bound, dirty, new)``.

    *"Repository state is obtained in a bounded batch, not through one Git
    subprocess per row."*  Two invocations, whatever the row count: one
    ``rev-parse`` for the observed HEAD and one pathspec-limited ``status`` for
    the difference set.  Machine-delimited (`-z`) so no filename needs unquoting,
    and fixed arguments so no artifact content reaches the command line.

    `bound` is False when either call fails; the caller then labels every row
    `WT-unbound` rather than asserting HEAD.
    """
    head_out = _git_readonly(["rev-parse", "HEAD"], root)
    if head_out is None:
        return None, False, set(), set()
    head = head_out.strip()
    status = _git_readonly(
        ["status", "--porcelain", "-z", "--untracked-files=all", "--",
         "dev/proposals", "dev/plans"], root)
    if status is None:
        return head, False, set(), set()
    dirty: Set[str] = set()
    new: Set[str] = set()
    entries = status.split("\x00")
    index = 0
    while index < len(entries):
        entry = entries[index]
        index += 1
        if len(entry) < 4:
            continue
        code, path = entry[:2], entry[3:]
        # A rename/copy entry is followed by its source path as a separate
        # NUL-terminated field; consume it so it is not misread as a status code.
        if "R" in code or "C" in code:
            index += 1
        if code == "??":
            new.add(path)
        else:
            dirty.add(path)
    return head, True, dirty, new


def _board_source_label(rel: str, bound: bool, dirty: Set[str],
                        new: Set[str]) -> str:
    if not bound:
        return BOARD_SOURCE_UNBOUND
    if rel in new:
        return BOARD_SOURCE_UNTRACKED
    if rel in dirty:
        return BOARD_SOURCE_DIRTY
    return BOARD_SOURCE_HEAD


def _board_declaration_violations(art: Artifact) -> List[str]:
    """The three declaration predicates for *art*, through their own names.

    No new predicate and no copied rule -- this is a call list, so the board's
    `declaration` reason code cannot drift away from what `scan` reports.
    """
    if art.kind == "proposal":
        return (assurance_declaration_violations(art)
                + proposal_review_basis_violations(art)
                + plan_readiness_violations(art)
                + current_contract_violations(art))
    return plan_inheritance_violations(art)


def _board_validity(art: Artifact,
                    identity: "IdentityModel") -> Tuple[str, List[str]]:
    """``(reason_code, every violation)`` for one artifact.

    Two separable jobs, deliberately: *whether* the row is invalid comes from
    `_conformance_violations` -- the same predicate `scan` prints -- and the
    *code* comes from re-asking the constituent predicates by name.  A new
    predicate therefore cannot make a row read `valid`; the worst it can do is
    land it on `other`, which is a visible "look at this" rather than silence.
    """
    violations = _conformance_violations(art, identity)
    if not violations:
        return BOARD_VALID, []
    states = PROPOSAL_STATES if art.kind == "proposal" else PLAN_STATES
    if art.status not in states and not (art.kind == "plan" and not art.status):
        return "status-vocabulary", violations
    if status_evidence_violations(art, art.status):
        return "status-evidence", violations
    if _board_declaration_violations(art):
        return "declaration", violations
    if blocked_by_violations(art):
        return "blocked-by", violations
    if art.kind == "plan" and not art.plan_review:
        return "review-floor", violations
    return "other", violations


def _board_review_summary(art: Artifact) -> str:
    """`review` -- *"declared obligations and mechanically supported
    completion"*.

    A plan's obligations come from `normalize_required_obligations`, and
    "mechanically supported" is asked of the **shared** predicate, not of a
    second reading: `review_record_violations(art, "implementing")` evaluates the
    Plan-review half only, because that function keys its Code-review half on
    `CODE_REVIEW_EFFECTIVE_STATES` and `implementing` is not one.  So this
    isolates the half it needs without a private copy of the clearing rule.

    A proposal declares no obligations of its own -- its readiness rests
    on *"at least one proposal review at the Internal floor or above"* -- so the
    field reports that record's own two closed fields.  `flagged` is deliberately
    not `blocking`: compressing a finding into a verdict is forbidden, and the
    board is reporting that the predicate said something, not judging what.
    """
    if art.kind == "proposal":
        line_no, tier, findings, _problems = _latest_proposal_review(art)
        if line_no is None:
            return "no-review"
        if tier is None or findings is None:
            return "fields-unreadable"
        return f"{tier}/{findings}"
    if not art.plan_review:
        return "undeclared"
    if not art.plan_review.lower().startswith("required"):
        return "not-required"
    obligations, problem = normalize_required_obligations(art.plan_review)
    if problem:
        return "declaration-invalid"
    flagged = review_record_violations(art, "implementing")
    return (f"required({len(obligations)})/"
            + ("flagged" if flagged else "clear"))


def _board_evidence_summary(art: Artifact) -> str:
    """`evidence` -- latest applicable review / Boundary B / Code review /
    closeout, as short ``key=value`` tokens.

    Every value is read from a record that exists; an absent record contributes
    no token rather than a reassuring default.  `cr=` carries the shared
    `_parse_verdict` classification, so a blocking pass reads `blocking` here and
    cannot be summarized into a clearing one.
    """
    parts: List[str] = []
    if art.kind == "proposal":
        reviews = _reviewers(art)
        if reviews:
            parts.append("rev=" + (reviews[-1].date or "undated"))
        decisions = _decisions(art)
        if decisions:
            parts.append("dec=" + (decisions[-1].date or "undated"))
        return " ".join(parts) if parts else BOARD_ABSENT
    passes = _pass_headings(art)
    if passes:
        parts.append("plan-rev=" + (passes[-1][0].date or "undated"))
    stable = _stable_evidence_records(art)
    if stable:
        parts.append("bnd=" + stable[-1][1])
    code_passes = _code_review_pass_lines(art)
    if code_passes:
        line_no, _reviewer, date, _round = code_passes[-1]
        verdict, _problem = _parse_verdict(_code_review_pass_body(art, line_no))
        parts.append(f"cr={verdict or 'unreadable'}@{date}")
    elif any(kind == "container" for _l, _r, kind in _code_review_records(art)):
        parts.append("cr=container-only")
    parts.append("close="
                 + ("ok" if not _closeout_violations(art, art.status) else "unmet"))
    return " ".join(parts) if parts else BOARD_ABSENT


def _board_blocked_by(art: Artifact) -> str:
    """The exact optional blocker metadata, or `-`.  Never a state transition.

    Read from the header region through the same field pattern
    `blocked_by_violations` uses, so the board displays exactly what that
    predicate judges.  A duplicated field shows as `ambiguous` rather than
    picking one of two lines that may disagree.
    """
    if art.kind != "plan":
        return BOARD_ABSENT
    header = "\n".join(_iter_header_lines(art.text))
    found = _REVIEW_FIELD_RE[_BLOCKED_BY_FIELD].findall(header)
    if not found:
        return BOARD_ABSENT
    if len(found) > 1:
        return "ambiguous"
    return found[0].strip() or BOARD_ABSENT


def _board_active_intent(rel: str, provider: Dict[str, object],
                         index: Dict[str, List[Dict]]) -> str:
    """`active_intent`: a claimant summary, `-`, `multiple:<n>`, or a state.

    *"It never turns missing intent coverage into an assertion that no one holds
    a claim."*  So `not-installed` and `error` are their own values and are
    **not** collapsed into `-`; only a working provider that found nothing may
    say `-`.  Multiple claims stay visible as a count rather than
    last-writer-wins.
    """
    state = provider.get("state")
    if state == INTENT_NOT_INSTALLED:
        return INTENT_NOT_INSTALLED
    if state == INTENT_ERROR:
        return INTENT_ERROR
    hits = index.get(rel, [])
    if not hits:
        return BOARD_ABSENT
    if len(hits) > 1:
        return f"multiple:{len(hits)}"
    return str(hits[0].get("agent"))


def board_rows(root: Path, identity: "IdentityModel",
               provider: Dict[str, object]) -> Tuple[List[Dict[str, str]],
                                                     Dict[str, object]]:
    """Every board row plus the header facts.  One parse per artifact, no cache.

    Returns ``(rows, header)``.  Each row's values are the **full** field values
    (the automation contract); the compact renderer is what escapes them for a
    terminal.  Structural trouble never removes a row: an unreadable artifact
    still appears, with `validity` = `unreadable`, because *"one malformed record
    cannot hide the rest of the board"*.
    """
    head, bound, dirty, new = _board_git_state(root)
    index = _intent_index(provider.get("claims") or [])  # type: ignore[arg-type]
    rows: List[Dict[str, str]] = []
    details: Dict[str, List[str]] = {}
    for kind, path in _board_artifact_paths(root):
        rel = path.relative_to(root).as_posix()
        source = _board_source_label(rel, bound, dirty, new)
        active_intent = _board_active_intent(rel, provider, index)
        try:
            art = _read_artifact(path)
        except (PlannerError, OSError, ValueError) as exc:
            # **Three exception families, and the widening is deliberate.**
            # `_read_artifact` raises `PlannerError` for an absent file, but it
            # also calls `read_text`, which raises `UnicodeDecodeError` (a
            # `ValueError`) on a file that is not valid UTF-8 and `OSError` on an
            # unreadable one.  Catching only `PlannerError` let a single
            # undecodable artifact abort the whole command with a traceback --
            # exactly the *"one malformed record cannot hide the rest of the
            # board"* failure that forbids.  Found by this module's own test, not
            # reasoned about afterwards.
            rows.append({
                "kind": kind, "artifact": path.stem, "status": BOARD_ABSENT,
                "owner": NEXT_OWNER_UNKNOWN, "active_intent": active_intent,
                "review": BOARD_ABSENT, "evidence": BOARD_ABSENT,
                "blocked_by": BOARD_ABSENT, "validity": "unreadable",
                "source": source,
            })
            details[path.stem] = [str(exc)]
            continue
        validity, violations = _board_validity(art, identity)
        details[path.stem] = violations
        rows.append({
            "kind": kind,
            "artifact": path.stem,
            "status": art.status or BOARD_ABSENT,
            "owner": next_owner(kind, art.status),
            "active_intent": active_intent,
            "review": _board_review_summary(art),
            "evidence": _board_evidence_summary(art),
            "blocked_by": _board_blocked_by(art),
            "validity": validity,
            "source": source,
        })
    header = {
        "head": head,
        "source_bound": bound,
        "worktree_differs": bool(dirty or new),
        "intent_provider": provider.get("state"),
        "intent_reason": provider.get("reason"),
        "intent_detail": provider.get("detail"),
        "details": details,
    }
    return rows, header


# --- filters, compact rendering, JSON, and focused inspection ----------------


def _board_usage(message: str) -> int:
    """Fail closed on an unusable filter, with the accepted vocabulary named."""
    print(f"{_PREFIX} USAGE ERROR: {message}", file=sys.stderr)
    return 2


def _board_filter(rows: List[Dict[str, str]],
                  args: argparse.Namespace) -> List[Dict[str, str]]:
    out = rows
    if args.status is not None:
        out = [row for row in out if row["status"] == args.status]
    if args.owner is not None:
        out = [row for row in out if row["owner"] == args.owner]
    if args.invalid_only:
        out = [row for row in out if row["validity"] != BOARD_VALID]
    return out


def _board_compact(rows: List[Dict[str, str]], header: Dict[str, object]) -> None:
    """The human- and token-efficient projection.  Every value is encoded."""
    _emit_section("lifecycle board")
    _emit("head: " + encode_display(str(header["head"] or "unavailable"))
          + " | source: "
          + ("bound" if header["source_bound"] else "UNBOUND (git unavailable)")
          + " | lifecycle files differ from HEAD: "
          + ("yes" if header["worktree_differs"] else "no"))
    intent_line = "intent coverage: " + encode_display(
        str(header["intent_provider"]))
    if header["intent_reason"]:
        intent_line += (" (" + encode_display(str(header["intent_reason"])) + ": "
                        + encode_display(str(header["intent_detail"])) + ")")
    elif header["intent_provider"] == INTENT_NOT_INSTALLED:
        intent_line += " -- no claim is authoritative from this board"
    _emit(intent_line)
    _emit(_BOARD_FIELD_DELIMITER.join(BOARD_FIELDS))
    for row in rows:
        _emit(_BOARD_FIELD_DELIMITER.join(
            encode_display(row[field]) for field in BOARD_FIELDS))
    _emit("")
    _emit(f"{len(rows)} row(s). The artifact is authoritative; this is a derived "
          "view. Read the row you need, then that artifact and its cited "
          "evidence -- not every active record.")


def _board_json(rows: List[Dict[str, str]], header: Dict[str, object]) -> None:
    """The automation contract: versioned, ASCII-safe, never string-interpolated.

    `ensure_ascii=True` and `sort_keys=True` make the payload byte-deterministic
    for a given tree, and the standard-library encoder is the only thing that
    ever touches the syntax -- no field value is formatted into JSON by hand.
    """
    payload = {
        "schema": BOARD_SCHEMA_VERSION,
        "head": header["head"],
        "source_bound": header["source_bound"],
        "worktree_differs": header["worktree_differs"],
        "intent_provider": header["intent_provider"],
        "intent_reason": header["intent_reason"],
        "intent_detail": header["intent_detail"],
        "fields": list(BOARD_FIELDS),
        "rows": rows,
        "invalid_count": sum(1 for row in rows
                             if row["validity"] != BOARD_VALID),
    }
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2))


def _board_explain(stem: str, rows: List[Dict[str, str]],
                   header: Dict[str, object], root: Path,
                   identity: "IdentityModel",
                   provider: Dict[str, object]) -> int:
    """Expand ONE row into the evidence and unmet predicates `next`/`scan`
    already have.

    *"An absent or ambiguous stem refuses rather than selecting the nearest
    name."*  Both refusals are here and neither guesses: nothing matched, or more
    than one thing did.  It cites headings and field values, never a review body.
    """
    matches = [row for row in rows if row["artifact"] == stem]
    if not matches:
        raise PlannerError(
            f"no active artifact has the stem {stem!r} -- the board refuses to "
            "select the nearest name. Run the board without --explain and copy "
            "an exact 'artifact' value.")
    if len(matches) > 1:
        kinds = ", ".join(sorted(row["kind"] for row in matches))
        raise PlannerError(
            f"the stem {stem!r} is ambiguous ({len(matches)} rows: {kinds}) -- "
            "the board refuses rather than choosing one.")
    row = matches[0]
    _emit_section(f"board --explain {encode_display(stem)}")
    for field in BOARD_FIELDS:
        _emit(f"{field}: {encode_display(row[field])}")

    details = header["details"]  # type: ignore[index]
    problems = details.get(stem, []) if isinstance(details, dict) else []
    _emit_section("conformance (the same predicates `scan` reports)")
    if problems:
        for message in problems:
            _emit(f"VIOLATION: {encode_display(message)}")
    else:
        _emit("current state is structurally sound.")

    path = None
    for kind, candidate in _board_artifact_paths(root):
        if candidate.stem == stem and kind == row["kind"]:
            path = candidate
            break
    if path is not None:
        try:
            art = _read_artifact(path)
        except (PlannerError, OSError, ValueError):
            art = None
        if art is not None:
            _emit_section("cited records (headings and declared fields only)")
            _emit(f"artifact: {encode_display(str(path.relative_to(root)))}")
            for section in _reviewers(art) + _decisions(art):
                _emit(f"  {encode_display(section.kind)} -- "
                      f"{encode_display(section.name or '(unattributed)')} -- "
                      f"{encode_display(section.date or '(undated)')} "
                      f"(line {section.line_no})")
            for line_no, date in _stable_evidence_records(art):
                _emit(f"  Implementation verification -- {encode_display(date)} "
                      f"(line {line_no})")
            _emit_section("unmet predicates per legal next transition")
            legal = _legal_transitions(art)
            if not legal:
                _emit("(terminal state -- no status transition)")
            for target in legal:
                _emit(f"-> {target}")
                for met, description in _gating_preconditions(art, target,
                                                              identity):
                    _emit(f"     [{'ok ' if met else 'MISSING'}] "
                          f"{encode_display(description)}")

    _emit_section("intersecting work-intent claims")
    state = provider.get("state")
    if state != INTENT_AVAILABLE:
        _emit(f"provider {encode_display(str(state))}"
              + (f" ({encode_display(str(provider.get('reason')))}: "
                 f"{encode_display(str(provider.get('detail')))})"
                 if provider.get("reason") else "")
              + " -- no claim is authoritative from this board; it does NOT mean "
                "nobody holds one.")
    else:
        rel = None
        if path is not None:
            rel = path.relative_to(root).as_posix()
        hits = _intent_index(
            provider.get("claims") or [])   # type: ignore[arg-type]
        for claim in (hits.get(rel, []) if rel else []):
            _emit(f"  id={encode_display(str(claim.get('id')))}")
            _emit(f"    agent={encode_display(str(claim.get('agent')))}")
            _emit(f"    ts={encode_display(str(claim.get('ts')))}")
            _emit(f"    action={encode_display(str(claim.get('action')))}")
            _emit("    files="
                  + ", ".join(encode_display(str(f))
                              for f in claim.get("files", [])))
        if not (hits.get(rel, []) if rel else []):
            _emit("  (no active claim intersects this artifact)")
        _emit("")
        _emit("a claim is not authority: it changes no status, owner, validity, "
              "priority, or review readiness.")
    return 0


def cmd_board(args: argparse.Namespace) -> int:
    """The derived orientation board.  Read-only, uncached, HEAD-labelled.

    Exit status: non-zero when any rendered row is structurally invalid or the
    optional provider is in `error`, **after** rendering every safely renderable
    row -- *"one malformed record cannot hide the rest of the board"*.  A
    Git-unavailable tree is labelled `WT-unbound` in every row and is not by
    itself an error: an unborn HEAD is a legitimate state, and the honest report
    is the label.
    """
    if args.compact and args.format == "json":
        return _board_usage(
            "--compact and '--format json' name different projections; pass one")
    fmt = "json" if args.format == "json" else "compact"
    if args.status is not None and args.status not in RECOGNIZED_STATES:
        return _board_usage(
            f"unknown --status {args.status!r}; the vocabulary is closed: "
            + ", ".join(RECOGNIZED_STATES))
    if args.owner is not None and args.owner not in NEXT_OWNERS:
        return _board_usage(
            f"unknown --owner {args.owner!r}; the vocabulary is closed: "
            + ", ".join(NEXT_OWNERS))

    root = _repo_root()
    identity = _load_identity_model(root)
    provider = query_intent_provider(root)
    rows, header = board_rows(root, identity, provider)
    selected = _board_filter(rows, args)

    if args.explain is not None:
        status = _board_explain(args.explain, rows, header, root, identity,
                               provider)
    elif fmt == "json":
        _board_json(selected, header)
        status = 0
    else:
        _board_compact(selected, header)
        status = 0

    if status:
        return status
    if any(row["validity"] != BOARD_VALID for row in selected):
        return 1
    if provider.get("state") == INTENT_ERROR:
        return 1
    return 0


# --- argument parsing --------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lifecycle_planner",
        description=(
            "Read-only Cairn lifecycle checker/planner. Reports artifact state, "
            "legal transitions, and unmet preconditions; emits proposed "
            "scaffolds + mutation manifests. Never mutates, never commits."
        ),
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_next = sub.add_parser(
        "next",
        help="Report an artifact's state + legal transitions (+ unmet "
             "preconditions); with --to, emit a scaffold + mutation manifest.",
    )
    p_next.add_argument("artifact", help="Path to a dev/proposals/ or "
                        "dev/plans/ artifact.")
    p_next.add_argument("--to", default=None, metavar="STATE",
                        help="Target transition state to scaffold (R6). Without "
                             "it, the legal next transitions are listed.")
    p_next.add_argument("--date", default=None, metavar="YYYY-MM-DD",
                        help="Date to stamp into the scaffold (default: today).")
    p_next.set_defaults(func=cmd_next)

    p_scan = sub.add_parser(
        "scan",
        help="Structural conformance scan over the local dev/ corpus (also the "
             "adopter fidelity scan). Non-zero exit when violations are found.",
    )
    p_scan.add_argument("--include-archive", action="store_true",
                        help="Also scan dev/proposals/archive/ + "
                             "dev/plans/archive/.")
    p_scan.set_defaults(func=cmd_scan)

    p_guard = sub.add_parser(
        "guard",
        help="Advisory pre-commit orientation (staged set, claim_check on "
             "staged dev/ docs). Warns; never blocks.",
    )
    p_guard.set_defaults(func=cmd_guard)

    p_board = sub.add_parser(
        "board",
        help="Derived orientation board over the active lifecycle artifacts: "
             "one compact row each (or --format json). Read-only, uncached, "
             "and never a source of lifecycle truth.",
    )
    p_board.add_argument(
        "--compact", action="store_true",
        help="The human- and token-efficient projection (the default).",
    )
    p_board.add_argument(
        "--format", choices=("compact", "json"), default="compact",
        metavar="{compact,json}",
        help="'json' emits the versioned automation contract with full field "
             "values; 'compact' (default) is the terminal projection.",
    )
    p_board.add_argument(
        "--status", default=None, metavar="STATE",
        help="Exact declared-status filter. An unrecognized value is a usage "
             "error, never an empty board.",
    )
    p_board.add_argument(
        "--owner", default=None, metavar="OWNER",
        help="Exact next-owner filter. An unrecognized value is a usage error.",
    )
    p_board.add_argument(
        "--invalid-only", action="store_true",
        help="Only rows whose validity is not 'valid'.",
    )
    p_board.add_argument(
        "--explain", default=None, metavar="ARTIFACT",
        help="Expand one row (by exact filename stem) into its cited records "
             "and unmet predicates. An absent or ambiguous stem refuses.",
    )
    p_board.set_defaults(func=cmd_board)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except PlannerError as exc:
        print(f"{_PREFIX} ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
