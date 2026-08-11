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

1. **Structural attestation, not authenticity (R1).**  It attests the
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

Optional aid, not the minimum kernel (R2)
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


# --- the AI-vs-human identity model (R5) -------------------------------------
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
    # review block parsed to nothing (S7).  A document of exactly the shape
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

#: S2 -- the two attestation lines, full-line anchored inside a pass body.
_TIER_LINE_RE = re.compile(r"^\*\*Tier\*\*:\s*(?P<value>.*?)\s*$", re.M)
_FINDINGS_LINE_RE = re.compile(r"^\*\*Findings\*\*:\s*(?P<value>.*?)\s*$", re.M)

#: S2 -- the closed vocabularies.  Comparison is case-insensitive; these are
#: the canonical spellings.
_TIERS = ("Internal", "External")
_FINDINGS = ("none", "raised")

#: S5 -- total order, External > Internal.  `declared >= required` satisfies
#: the floor.  There is no third tier and no `Maintainer` tier: a human review
#: declares External.
_TIER_RANK = {"internal": 1, "external": 2}

#: S7 -- a Sharpening heading, matched positionally inside a pass body.
_SHARPENING_RE = re.compile(r"^###\s+Sharpening\b", re.M)

#: S6 step 1 -- the first parenthesised group of the `**Plan review**:` field.
_REQUIRED_TIER_RE = re.compile(r"^required\s*\(([^)]*)\)", re.I)

#: S6 step 3 -- the first alphabetic word inside that group.
_FIRST_WORD_RE = re.compile(r"^[A-Za-z][A-Za-z-]*")


def _parse_one_field(body: str, pattern: "re.Pattern[str]",
                     vocabulary: Tuple[str, ...], field: str
                     ) -> Tuple[Optional[str], Optional[str]]:
    """Read one S2 attestation line -> ``(canonical_value, violation)``.

    Implements S3's three fail-closed directions, and **no condition yields a
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
    raw = found[0].strip()
    for canonical in vocabulary:
        if raw.casefold() == canonical.casefold():
            return canonical, None
    return None, f"unrecognized {field} value: {raw!r}"


def _parse_pass_date(raw: str) -> Tuple[bool, Optional[str]]:
    """S1 -- the captured date must be a **real** date, not date-shaped.

    ``_HEADER_RE`` matches the *shape* ``\\d{4}-\\d{2}-\\d{2}``, which accepts
    ``2026-99-99``, ``2026-02-30`` and ``0000-00-00``.  ``date.fromisoformat``
    is strict and rejects all three while accepting a real leap date.  A shape
    match whose value does not parse is a violation, never a silent pass --
    and, under S9's enumerated legacy manifest, never an exemption either.
    """
    if not raw:
        return False, None
    try:
        _dt.date.fromisoformat(raw)
    except ValueError:
        return False, f"malformed date: {raw!r}"
    return True, None


def normalize_required_tier(field: str) -> Tuple[Optional[str], Optional[str]]:
    """S6 -- normalize the `**Plan review**:` field -> ``(tier, violation)``.

    Defined on the **first parenthesised group only**.  Text after the closing
    paren is ignored (every live plan has some); text after the first word
    *inside* the group is a **lens annotation** -- preserved in the record by
    the caller, ignored by the tier comparison.  Negations fail closed:
    ``required(not External)`` is a violation, not an External requirement.
    """
    m = _REQUIRED_TIER_RE.match(field.strip())
    if not m:
        return None, "tier not declared"
    group = m.group(1)
    for ch in "*_`":
        group = group.replace(ch, "")
    word = _FIRST_WORD_RE.match(group.strip())
    if not word:
        return None, "tier not declared"
    tier = word.group(0).casefold()
    if tier not in _TIER_RANK:
        return None, f"unrecognized required tier: {word.group(0)!r}"
    return tier, None


def tier_satisfies(declared: str, required: str) -> bool:
    """S5 -- ``declared >= required`` under the total order External > Internal."""
    return _TIER_RANK.get(declared.casefold(), 0) >= _TIER_RANK.get(
        required.casefold(), 0)


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
    authorization (R1)."""
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
#: a text scanner; the residual is recorded in ``dev/PLANNING.md`` **[SP8-9]**.
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
# vocabulary (`lifecycle-status-vocabulary` R5, as replaced by that proposal's
# "R5 replacement -- contained consumers and corpus boundary").  It mirrors
# `doctrine/lifecycle-contract.md`, which stays the human contract.
#
# Two consumers live OUTSIDE this file's package and read the names below by
# loading this file through a contained fixed-path loader -- never through
# ambient `sys.path`, and never by re-declaring a status literal of their own:
#
#   * `tools/_lifecycle_metrics/extract.py` + its installed twin
#     (`templates/modules/default-on/_lifecycle_metrics/extract.py`);
#   * `scripts/transition_lint.py` (repository-only).
#
# `bootstrap/tests/test_lifecycle_vocabulary.py` audits both consumers' source
# for local status enums and is observed red against a reintroduced one.
#
# Five declarations, each with exactly one job.  Keeping them as *data* is what
# makes the next vocabulary change (`ready-to-implement` / `implementing` /
# `awaiting-code-review` / `ready-to-archive`, which move `executing` and
# `review` into the historical sets) an edit to these tuples rather than a
# refactor of every consumer.

#: The CURRENT vocabulary -- the only statuses an *active* artifact may declare.
PROPOSAL_STATES = ("proposed", "reviewed", "revised", "accepted",
                   "rejected", "superseded")
PLAN_STATES = ("open", "awaiting-plan-review", "executing", "review",
               "archived")

#: Terminal = no status flip leaves them.  A proposal's `accepted` IS terminal:
#: its archive move is a file operation, not a transition.
PROPOSAL_TERMINAL_STATES = ("accepted", "rejected", "superseded")
PLAN_TERMINAL_STATES = ("archived",)

PROPOSAL_NON_TERMINAL_STATES = tuple(
    s for s in PROPOSAL_STATES if s not in PROPOSAL_TERMINAL_STATES)
PLAN_NON_TERMINAL_STATES = tuple(
    s for s in PLAN_STATES if s not in PLAN_TERMINAL_STATES)

#: Legal next target states, as data.  `""` is the not-yet-created artifact.
PROPOSAL_TRANSITIONS = {
    "": ("proposed",),
    "proposed": ("reviewed",),
    "reviewed": ("revised", "accepted", "rejected", "superseded"),
    "revised": ("reviewed", "accepted", "rejected", "superseded"),
    "accepted": (),
    "rejected": (),
    "superseded": (),
}
PLAN_TRANSITIONS = {
    "": ("open",),
    "open": ("awaiting-plan-review",),
    "awaiting-plan-review": ("executing",),
    "executing": ("review",),
    "review": ("archived",),
    "archived": (),
}

#: The single status whose legal set depends on the artifact's own declaration
#: rather than on the state machine: a `not required(...)` plan skips the wait.
#: Isolated and named so the conditional is one entry, not a branch in a table.
PLAN_TRANSITIONS_REVIEW_NOT_REQUIRED = {"open": ("executing",)}

#: Historical tokens -- admitted ONLY for migration, archived-artifact
#: compatibility, and longitudinal metrics.  **Never** legal for an active
#: artifact and never a transition target.
#:
#: Both are empty today, and that is a measured statement rather than a
#: placeholder: the current vocabulary has never dropped a token, so every
#: status appearing in this repository's history is still current.  The seam
#: exists because the accepted vocabulary change *will* retire `executing` and
#: `review`, and metrics must keep parsing commits that used them.
HISTORICAL_PROPOSAL_STATES: Tuple[str, ...] = ()
HISTORICAL_PLAN_STATES: Tuple[str, ...] = ()

#: The *opening* statuses -- an artifact still at or before its review floor.
#: `transition_lint`'s shape (b) asks whether an ADDED lifecycle file already
#: carried a landed review, which is only meaningful pre-review.
OPENING_STATES = ("proposed", "open", "awaiting-plan-review")

#: The added-artifact status set shape (b) consumes: every recognized current
#: non-terminal state, plus the historical opening states old commits need.
#:
#: Widened here from `OPENING_STATES` alone (3 tokens -> 7) per the accepted R5
#: replacement.  The proposal records this as corpus-neutral at the reviewed
#: 2026-08-10 history because none of the newly admitted tokens occurs as the
#: status of an *added* file there.  That is a claim about a pinned corpus, so
#: `test_transition_lint.py`'s corpus expectations are the witness, not this
#: comment -- and a later widening to historical NON-opening tokens is
#: corpus-CHANGING and re-runs that measurement.
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


#: S9(a) -- the legacy population, ENUMERATED.  ``stem -> {heading digest: n}``.
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


#: S1 -- the exact raw-heading grammar the review-pass record schema
#: defines.  Authored independently of ``scripts/gen_legacy_passes.py``'s own
#: ``_PASS_RE`` -- the two must never become each other's oracle, even
#: though both implement the same published S1 grammar and therefore read
#: alike.
#:
#: **CR1.** The earlier ``_pass_headings`` selected *Sections* the older,
#: more permissive ``_HEADER_RE`` had already accepted, and never checked the
#: raw line against S1 itself.  ``_HEADER_RE`` is a strict superset of this
#: shape -- it tolerates arbitrary whitespace after ``##``, around ``--``,
#: and before end-of-line -- so three shapes that must NOT be passes cleared
#: the gate anyway: extra spaces after ``##``, doubled ``--`` separators, and
#: trailing spaces after the date. The inverse also reproduced: a reviewer
#: field containing literal parentheses (``Jane (Lab) Smith``) matches S1's
#: permissive ``[^\n]+?`` reviewer group, but ``_HEADER_RE``'s
#: ``(?P<role>[^)\n]*)`` machinery cannot parse the line at all, so
#: ``_parse_sections`` produced no Section for it and a conforming pass was
#: silently invisible. This regex is now the sole authority on what counts.
_S1_PASS_RE = re.compile(
    r"^## Plan review -- (?P<reviewer>[^\n]+?) -- "
    r"(?P<date>\d{4}-\d{2}-\d{2})(?: \(round (?P<round>\d+)\))?$"
)


def _pass_body(lines: List[str], line_no: int, boundaries: List[int]) -> str:
    """The body of the pass whose heading is at *line_no* (Chunk B, B1).

    **One ordered boundary set, used for every pass body of either record
    kind.**  A boundary is a level-<=2 Section *or* a raw S1-conforming pass
    line, so a pass heading the looser ``_HEADER_RE`` could not parse still
    terminates the pass above it.

    Why this is not merely tidier: before B1 only *synthesized* sections were
    sliced this way, and a recognized pass kept the body ``_parse_sections``
    gave it.  ``_parse_sections`` knows nothing about raw S1 lines, so a later
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

    The ceiling half of B1 falls out of the same set rather than needing its own
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
    """A Section for an S1 pass line ``_HEADER_RE`` could not parse (CR1).

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

    Matches the **raw heading line** against `_S1_PASS_RE` directly (CR1) --
    never derives a pass from a Section the looser `_HEADER_RE` happened to
    produce. Most S1-conforming lines already have a Section (`_HEADER_RE`
    is a superset of S1's shape), and that Section is reused so its
    precomputed body stays identical to every other parsed section's. A raw
    line that matches S1 but that `_HEADER_RE` could not parse at all gets a
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
    # R4 -- ONE canonical boundary set, of BOTH record kinds.  Defined below
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
                # B1: a recognized pass gets the SAME boundary rule as a
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
    """S7 -- does a disposition follow `pass_sec`, in either house form?

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

    `[E3]`'s property survives, because it was about a *neighbouring round's*
    disposition standing in for this one: a ``### Sharpening`` is still scoped
    to its own pass's body and never reaches a sibling, and a pass with **no**
    Response after it at all is still unsatisfied.  What is now allowed is the
    author saying, in one section, "these are answered" -- which is what the
    section already meant.

    **CR2.** The documented second house form is specifically
    ``## Response to plan review``, but the earlier check matched any kind
    whose text merely *started with* ``response`` -- so an unrelated
    ``## Response -- Author -- date`` or ``## Response to proposal review --
    Author -- date`` cleared a raised finding it never addressed. The kind
    comparison below is exact (case-insensitive), never a prefix.
    """
    if _SHARPENING_RE.search(pass_sec.body):
        return True
    # The group rule.  CR2's exactness is retained: the kind comparison is
    # exact (case-insensitive), never a prefix, so `## Response -- ...` and
    # `## Response to proposal review -- ...` still do not discharge S7.
    return any(
        sec.level == 2
        and sec.kind.strip().lower() == "response to plan review"
        and sec.line_no > pass_sec.line_no
        for sec in art.sections
    )


# === Chunk B, B3: Code-review disposition -- exact `Answers:` binding ========
#
# **The two record types take deliberately OPPOSITE rules, and that is the
# point of splitting B2 from B3.**
#
#   * a *Plan* review is answered as a **round**, so one Response dispositions
#     the whole group of passes above it (the group rule landed at `286f07d`,
#     preserved verbatim by B2 above);
#   * a *Code* review's findings are answered **individually**, so each Response
#     must name exactly which pass it answers.
#
# Collapsing these into one generic "a disposition after the later pass may
# satisfy the earlier" assertion is what produced the contradiction the plan's
# Chunk B records: an implementer following the collapsed sentence would have
# restored the false ceiling the Maintainer had just directed away.  So the two
# predicates are separate functions with separate tests, and B4 requires a
# falsifier in each direction so neither can be weakened *into* the other
# unnoticed.
#
# Contract: accepted `code-review-blindness` **R2''** ("the exact grammar",
# which replaces R2's ordering and binding clauses) as sharpened by that
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

#: R2'': **one full-line anchored field**.  Anchored on purpose -- an
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

    Bounded by the next level-<=2 heading, which is the same boundary rule B1
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
    """Every ``Answers:`` binding defect in *art* (B3).

    Six refusal directions, each named separately in the message so a reader is
    sent to the right place: **missing**, **duplicate**, **malformed**,
    **unmatched**, **ambiguous**, and **precedes its target**.  R2'' lists the
    first four; Revision 3 adds *ambiguous* by requiring exactly one match; the
    last is R2''s "A Response positioned before its target refuses".

    *skip_lines* (Chunk C) names Response headings admitted by
    `_LEGACY_CODE_REVIEW_RECORDS`.  The ``Answers:`` field is **newer than every
    Response in this tree** -- 2 exist corpus-wide and neither carries it -- so
    without the exemption the gate reddens on a real archived record the moment
    C1 wires it in, and R5's accepted blast radius says *"no existing artifact
    violates"*.  Default `None` keeps the B3 signature callable, which is how
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
    satisfies an earlier one, which is the asymmetry B4 pins in both directions.
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
# **R2 is superseded**.  The operative clauses are:
#
#   R2'   the archive rule -- the latest applicable pass must CLEAR.  There is
#         no disposition branch: a Response records the implementer's answer and
#         does not clear archive; eligibility comes from a later independent
#         pass.  ([R2-E1] -- letting an author's own Response convert `REVISE`
#         into archive eligibility would weaken the accepted parent's
#         correction-review boundary, which this amendment exists to *supply*.)
#   R2''  the exact grammar -- document-order recency, the `(round N)` rules,
#         and the full-line `Answers:` binding (implemented at B3 above).
#   R3'   legacy, keyed non-replayably -- digest + occurrence count, pinned to
#         one named baseline commit.
#   R5''  one predicate, evaluating an explicit EFFECTIVE STATE, reached by both
#         callers regardless of whether Plan review was required.
#
# **Why the effective state and not the status.**  [R3-E1] executed the bypass:
# `review_record_violations` sat behind `requires_review`, so a plan declaring
# `Plan review: not required(doc-only)` never reached it, and deleting the weak
# `_has_kind` presence check would have made such a plan archive *clean* instead
# of replacing the weak check with the strong one -- "the same governing failure
# the proposal exists to close, reached through a common legitimate plan
# declaration."  So the Code-review half is keyed on the effective state alone,
# and only the Plan-review half consults the declaration.

#: The effective states at which the Code-review record is evaluated (R5'').
#: `scan` supplies the current status; `next`/closeout supplies the requested
#: target.  `ready-to-archive` is named here **before** it exists in
#: `PLAN_STATES`: the accepted status-vocabulary change introduces it, and R5''
#: names both tokens, so wiring it now makes that change a data edit rather than
#: a second search for every archive-effective branch.
CODE_REVIEW_EFFECTIVE_STATES = ("ready-to-archive", "archived")

#: R2' -- the closed verdict vocabulary, two classes.  Chosen to cover what this
#: tree already writes rather than to impose a new dialect: every value below
#: appears in `dev/plans/`'s real Code-review sections.
CODE_REVIEW_CLEARING_VERDICTS = ("SHIP", "Accept", "Accept-with-followups",
                                 "PASS")
CODE_REVIEW_BLOCKING_VERDICTS = ("REVISE", "Request changes", "BLOCK")

#: The four-field review basis a Code-review pass inherits from the accepted
#: parent (`review-efficient-lifecycle` > "Every review names a bounded
#: target"), plus R2's three attestation lines.  Order is the reported order.
_CODE_REVIEW_BASIS_FIELDS = ("Reviewed commit", "Target", "Prior findings")
_ASSURANCE_PATHS = ("standard", "high-assurance")


def _code_review_field_re(name: str) -> "re.Pattern[str]":
    """One full-line field matcher, **emphasis-optional**.

    The field NAME is the contract; the emphasis is not, and admitting only one
    spelling would refuse correct records for no contract reason.  Both spellings
    are live text: the accepted parent writes the basis unbolded --

        Reviewed commit: <full commit id>

    -- while every real review in `dev/plans/` writes the same lines bolded
    (`**Reviewed commit**:`), and R2 itself specifies `**Model**:`,
    `**Verdict**:`, `**Findings**:` with the bold.  Full-line anchored, so an
    ``Answers``-style prose mention cannot become a field.
    """
    return re.compile(
        r"^(?:\*\*|__)?" + re.escape(name) + r"(?:\*\*|__)?:[ \t]*"
        r"(?P<value>.*?)[ \t]*$", re.M)


_CODE_REVIEW_FIELD_RE = {
    name: _code_review_field_re(name)
    for name in _CODE_REVIEW_BASIS_FIELDS
    + ("Assurance path", "Model", "Verdict", "Findings")
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

#: R2: the mandatory fields sit **before the pass's first H3**.  Not decoration:
#: real passes carry a `### 4. Verdict & Archive Readiness` subsection that
#: repeats the verdict, and reading the whole body would report the pass's own
#: summary as a *duplicate field*.
_FIRST_H3_RE = re.compile(r"^###\s", re.M)

#: S9(a) for the Code-review record -- the legacy population, ENUMERATED.
#: ``stem -> {raw-heading digest: n}``, the same shape as `_LEGACY_PASSES`, so
#: `_is_legacy`'s k-th-occurrence anti-replay rule applies unchanged (R3').
#:
#: **Baseline commit `4ca44eb8d1b378a0214019270e1a2d83976c7bb0`.**  R3' requires
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

#: R3', final bullet: for a legacy pass whose verdict BLOCKS, the manifest
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
#: **The population is four, not the two R2' names.**  R2' names
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
    """R4 -- the ONE canonical ordered boundary set, of **both** record kinds.

    Level-<=2 Sections, unioned with every raw conforming pass line of either
    kind.  B1 built this from `_S1_PASS_RE` alone because the Code-review
    grammar did not exist yet; R4 asks for both, and this completes it.

    Widening a boundary set can only ever **narrow** a body, never widen one, so
    applying it to already-recognized sections stays safe -- the property
    `_pass_body` relies on.  What it fixes: a Code-review heading whose reviewer
    field carries parentheses outside the ``(<role>)`` position is invisible to
    `_HEADER_RE`, so before this it did not terminate the Plan-review pass above
    it, and that pass's body ran straight through it -- swallowing its
    attestation lines and reporting them as the *earlier* pass's duplicates.
    """
    lines = art.text.split("\n")
    return sorted(
        {sec.line_no for sec in art.sections if sec.level <= 2}
        | {i + 1 for i, raw in enumerate(lines) if _S1_PASS_RE.match(raw)}
        | {i + 1 for i, raw in enumerate(lines)
           if _CODE_REVIEW_PASS_RE.match(raw)})


#: Any ``## Code review`` H2 heading at all.  The set difference against
#: `_CODE_REVIEW_PASS_RE` is the *container* population -- the bare heading the
#: plan template ships, and decorated variants like
#: ``## Code review — the brief (no review has landed)``.
_CODE_REVIEW_ANY_RE = re.compile(r"^## Code review(?:[^0-9A-Za-z].*)?$")


def _code_review_records(art: Artifact) -> List[Tuple[int, str, str]]:
    """Every Code-review record heading in *art*, in document order.

    ``(line_no, raw_heading, kind)`` with *kind* one of ``pass`` (conforming per
    R2''), ``container`` (a ``## Code review`` heading that is not a pass), or
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
    """R2' -- ``(clearing|blocking, violation)`` from one pass's field scope."""
    found = _CODE_REVIEW_FIELD_RE["Verdict"].findall(_EMPHASIS_RE.sub("", body))
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
    """R2'' -- the ordering rules, over passes **sharing a date**.

    Document order is authoritative, and `(round N)` exists only to make round
    order and document order agree.  So among passes sharing one date: a round
    must be unique and strictly increasing down the file, and an unnumbered pass
    may not share a date with a numbered one.  "Ties refuse" was reaching for
    exactly this and never defined it; there is no other tie case.

    Two *unnumbered* passes sharing a date are **allowed** -- one archived plan
    has them, from two different reviewers on one day -- and the ambiguity that
    creates is answered where it actually bites, in the `Answers:` binding's
    exactly-one-match rule ([R3-E2]), not by refusing the passes.
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
    """The Code-review record contract over one artifact (C1/C2/C4).

    **Not a public entry point and not a second predicate.**  R5'' folds
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
    # k-th appearance of that digest in the file (R3's anti-replay component).
    seen: Dict[str, int] = {}
    legacy: Dict[int, bool] = {}
    for line_no, raw, _kind in records:
        dig = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
        seen[dig] = seen.get(dig, 0) + 1
        legacy[line_no] = _is_legacy(stem, dig, seen,
                                     _LEGACY_CODE_REVIEW_RECORDS)

    passes = _code_review_pass_lines(art)
    v.extend(_code_review_ordering_violations(passes))

    # R2''s binding, with legacy Responses exempt.  A Response is a record about
    # a pass, so its defects are reported whether or not a pass is the latest.
    v.extend(code_review_binding_violations(
        art, skip_lines={line_no for line_no, _raw, kind in records
                         if kind == "response" and legacy[line_no]}))

    if not passes:
        # Presence.  R2: "Absent Code review on an `archived` plan remains the
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

    line_no, reviewer, date, _round = passes[-1]   # R2'': document order
    label = f"'## Code review -- {reviewer} -- {date}'"
    ok_date, date_violation = _parse_pass_date(date)
    if date_violation:
        # Checked BEFORE the legacy fence, for the reason the Plan-review path
        # states: an exemption keyed on the heading would otherwise swallow the
        # date contract, which is how the replaced dated epoch failed.
        v.append(f"{label}: {date_violation}")
    if legacy[line_no]:
        return v + _legacy_disposition_violations(art, stem, line_no, label)

    body = _code_review_pass_body(art, line_no)
    for field in _CODE_REVIEW_BASIS_FIELDS + ("Model",):
        found = _CODE_REVIEW_FIELD_RE[field].findall(body)
        if not found:
            v.append(f"{label}: missing '{field}:' -- the four-field review "
                     "basis plus '**Model**:' is mandatory before the pass's "
                     "first H3")
        elif len(found) > 1:
            v.append(f"{label}: duplicate '{field}:' ({len(found)} lines)")
        elif not found[0].strip():
            v.append(f"{label}: empty '{field}:' value")
    _path, path_violation = _parse_one_field(
        body, _CODE_REVIEW_FIELD_RE["Assurance path"], _ASSURANCE_PATHS,
        "Assurance path")
    _find, findings_violation = _parse_one_field(
        body, _CODE_REVIEW_FIELD_RE["Findings"], _FINDINGS, "Findings")
    verdict, verdict_violation = _parse_verdict(body)
    for problem in (path_violation, findings_violation, verdict_violation):
        if problem:
            v.append(f"{label}: {problem}")
    if verdict == "blocking":
        # R2', the whole point: no disposition branch.  A `## Response to code
        # review` records the implementer's answer and does NOT clear archive --
        # eligibility comes from a later pass by an independent correction
        # reviewer, which is the accepted parent's boundary this amendment was
        # written to supply rather than weaken ([R2-E1]).
        v.append(
            f"{label} carries a BLOCKING verdict, so this state is refused. A "
            "'## Response to code review' does not clear it: correct the "
            "findings, land a replacement Boundary B record over the corrected "
            "range, and have an independent correction reviewer append a new "
            "pass. Archive eligibility comes from THAT pass's clearing verdict.")
    # 'Findings: raised' with a clearing verdict is a COMPLETE record and does
    # not block ([A1] -- the common case; a schema must not criminalise it).
    return v


def _legacy_disposition_violations(art: Artifact, stem: str, line_no: int,
                                   label: str) -> List[str]:
    """R3', final bullet -- a blocking legacy pass needs its named disposition.

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


def _near_miss_headings(art: Artifact) -> List[str]:
    """Every heading that begins `Plan review` but is **not** an S1 pass.

    S8 requires the refusal to *quote* these: an author who wrote
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
    """S9(b) -- is this the k-th occurrence of `dig`, with k <= manifest count?

    **One k-th-occurrence rule, two manifests.**  Chunk C adds a second
    enumeration (`_LEGACY_CODE_REVIEW_RECORDS`) for the Code-review record, and
    the accepted `code-review-blindness` **R3'** requires that it match
    `_LEGACY_PASSES`' shape *"so ``_is_legacy``'s k-th-occurrence rule applies
    unchanged"*.  A default argument is how that stays literally true: writing a
    sibling `_is_legacy_code_review` would put two implementations of one
    anti-replay rule in the file, and the next person to fix a bug in one of
    them would not know to fix the other.
    """
    table = _LEGACY_PASSES if manifest is None else manifest
    admitted = table.get(stem, {}).get(dig, 0)
    return seen.get(dig, 0) <= admitted


def review_record_violations(art: Artifact,
                             effective_state: Optional[str] = None
                             ) -> List[str]:
    """S1-S9 plus the Code-review record over one artifact.  **The one
    predicate (S12).**

    Both gate call sites -- ``_conformance_violations`` and
    ``_gating_preconditions`` -- go through this function, so the two cannot
    drift into disagreeing about the same record.  A pass that fails S1 is
    **neither a pass nor a violation**: it can no longer clear anything, because
    clearing requires an S1 match, and near misses therefore fail closed as
    "no conforming pass has landed" rather than as "a pass with problems".

    *effective_state* (R5'') is the state being asserted, **explicitly**: the
    current status for `scan`, the requested target for `next`/closeout.  It
    decides only the Code-review half; the Plan-review half is decided by the
    plan's own declaration.  `None` means "the artifact's current status", which
    is the conformance reading.

    **Two halves, two different keys, and that asymmetry is the finding.**
    Plan-review obligations are evaluated only when the plan declares
    `required(...)`; Code-review obligations are evaluated whenever the effective
    state is archive-effective, *regardless* of that declaration.  Keying the
    Code-review half on the declaration is the bypass [R3-E1] executed: a plan
    declaring `Plan review: not required(doc-only)` never reached this predicate
    at all, so deleting the weak `_has_kind` presence check would have made such
    a plan archive **clean**.
    """
    stem = art.path.stem
    state = art.status if effective_state is None else effective_state
    required, tier_violation = normalize_required_tier(art.plan_review)
    plan_review_required = art.plan_review.lower().startswith("required")
    v: List[str] = []
    if state in CODE_REVIEW_EFFECTIVE_STATES:
        v.extend(_code_review_violations(art))
    if not plan_review_required:
        return v
    if tier_violation:
        v.append(f"'**Plan review**:' {tier_violation}")

    seen: Dict[str, int] = {}
    satisfied = False
    for sec, dig in _pass_headings(art):
        seen[dig] = seen.get(dig, 0) + 1
        # S1 IS CHECKED BEFORE THE S9 FENCE, and the order is load-bearing.
        # The enumeration exempts a pass from S2, S3 and S7 (S9(b)) -- never
        # from S1.  With the fence first, an exemption keyed on the heading
        # swallows the date contract, which is exactly how the replaced dated
        # epoch failed: `0000-00-00` sorts before every epoch, so the
        # impossible value bought the exemption *and* silenced the
        # malformed-date violation.  Checking S1 first leaves no fence,
        # present or future, able to swallow it.
        ok_date, date_violation = _parse_pass_date(sec.date)
        if date_violation:
            v.append(f"'{sec.kind} -- {sec.name}': {date_violation}")
        if _is_legacy(stem, dig, seen):
            # Exempt from S2/S3/S7; satisfies the floor by presence, as the
            # Maintainer accepted these records before the schema existed.
            satisfied = True
            continue
        tier, tv = _parse_one_field(sec.body, _TIER_LINE_RE, _TIERS, "Tier")
        find, fv = _parse_one_field(
            sec.body, _FINDINGS_LINE_RE, _FINDINGS, "Findings")
        for problem in (tv, fv):
            if problem:
                v.append(f"'{sec.kind} -- {sec.name} -- {sec.date}': {problem}")
        if find == "raised" and not _has_disposition(art, sec):
            # S7 -- positional, and it accepts EITHER house form.  See
            # _has_disposition: the tree uses both, roughly evenly, so a gate
            # that demanded one would redden half the existing dispositions
            # while enforcing a convention the project does not hold.
            v.append(
                f"'{sec.kind} -- {sec.name} -- {sec.date}' declares "
                "'**Findings**: raised' but no disposition follows it -- "
                "expected a '### Sharpening' inside its own body, or a "
                "'## Response to plan review' section before the next pass.")
        if ok_date and tier and find and required \
                and tier_satisfies(tier, required):
            satisfied = True
    if required and not satisfied:
        near = _near_miss_headings(art)
        quoted = ("; near misses that do NOT count: "
                  + ", ".join(repr(h) for h in near)) if near else ""
        v.append(
            f"'Plan review: required({required})' but no conforming pass "
            f"satisfies it. A heading that is not an exact "
            f"'## Plan review -- <reviewer> -- YYYY-MM-DD' is not a pass and "
            f"cannot clear the floor{quoted}.")
    return v


# --- conformance checks (structural; used by `scan` and `next`) --------------
#
# These verify the *current* status is structurally supported by the
# documentary attestations the artifact carries -- the machine-verifiable
# half.  Each returned string is a violation; an empty list means the
# current state is structurally sound (NOT that the quotes are authentic --
# the tool never asserts authenticity, R1).


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
                "(proposed/reviewed/revised/accepted/rejected/superseded); a "
                "missing status hides every downstream conformance check."
            )
        elif s not in _PROPOSAL_STATES:
            v.append(f"unknown proposal status {s!r}")
        if s in ("reviewed", "revised", "accepted", "rejected", "superseded"):
            revs = _reviewers(art)
            if not revs:
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
                # that remains the committing operator's guarantee (R1).
    else:  # plan
        if s and s not in _PLAN_STATES:
            v.append(f"unknown plan status {s!r}")
        if not art.plan_review:
            v.append(
                "no '**Plan review**:' line (mandatory: 'required(<tier>)' or "
                "'not required(<rationale>)'; a missing line is a finding)."
            )
        requires_review = art.plan_review.lower().startswith("required")
        if s in CODE_REVIEW_EFFECTIVE_STATES or (
                s in ("executing", "review") and requires_review):
            # S12 -- ONE predicate, BOTH call sites.  This was
            # `not _has_kind(art, "Plan review")`: a PREFIX PRESENCE test that
            # cleared on a bare `## Plan review` container, an undated heading,
            # an H3 pass, `## Plan reviewers`, and an `Internal`-only pass on an
            # `External` floor.  `_gating_preconditions(art, "executing")` calls
            # the same predicate on the same record, so `scan` cannot tighten
            # while `next --to executing` stays presence-only.
            #
            # The status condition is unchanged and deliberate: this arm asserts
            # that the CURRENT status is structurally supported, and an `open`
            # plan awaiting its review is not a violation.  The
            # evaluate-as-if-transitioning read ([E4]) is the other call site's,
            # reached from `open` / `awaiting-plan-review`.
            #
            # Conformance only: the record's shape is checked, never that the
            # review happened or that the declared tier is true (R1 / [E4]).
            v.extend(review_record_violations(art))
        if s == "archived":
            # R5'' -- the two weak Code-review opinions that stood here are
            # DELETED, not kept alongside the schema check.  They were
            # `_has_kind(art, "Code review")` (section presence, which the
            # shipped template satisfies by itself) and, added later,
            # `art.has_code_review_marker` (a `**Model**:`-or-dated-heading
            # marker).  Both asked "did a code review happen?" more weakly than
            # the schema now does, and the accepted proposal is explicit that
            # "presence becomes a consequence of the schema check rather than a
            # second, weaker opinion".  The marker predicate itself survives and
            # is still consulted -- but INSIDE the one predicate, as the
            # substance floor a legacy container heading must clear, which is the
            # only place it can still say something the schema cannot.
            if not art.has_disposition_attestation:
                v.append(
                    "status is 'archived' but no 'Dispositions:' block "
                    "(or the older 'Follow-ups migrated to:') is present "
                    "(archive precondition)."
                )
            if not art.has_fidelity_signoff:
                v.append(
                    "status is 'archived' but no loop-fidelity sign-off is "
                    "present (names the implementing commit + governing section)."
                )
    return v


# --- forward-transition recipes (preconditions a target needs) ---------------
#
# For each legal target, the *gating* preconditions: structural facts that
# must already hold for the transition to be valid, each reported met/unmet
# from the file.  When a gate is unmet the tool reports the missing
# attestation -- it never presents the transition as ready (R3 / contract
# clause 3).


def _gating_preconditions(art: Artifact, target: str,
                          identity: "IdentityModel") -> List[Tuple[bool, str]]:
    """Return (met, description) gates for a forward transition to `target`."""
    gates: List[Tuple[bool, str]] = []
    revs = _reviewers(art)
    independent_review = any(
        r.name and (not art.author
                    or _identity_token(r.name) != _identity_token(art.author))
        for r in revs
    )
    if art.kind == "proposal":
        if target == "reviewed":
            gates.append((True,
                          "append a '## Review' (reviewer fills their own "
                          "identity; not the proposal author); append-only."))
        elif target == "revised":
            gates.append((bool(revs),
                          "a prior '## Review' section exists"))
            gates.append((True,
                          "append a '## Response' (+ optional '## Revised "
                          "proposal'); append-only."))
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
        if target == "awaiting-plan-review":
            gates.append((requires_review,
                          "'Plan review: required(<tier>)' (else the plan goes "
                          "straight to executing)"))
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
        elif target == "review":
            gates.append((True,
                          "append a '## Code review' pass (reviewer is not the "
                          "implementing agent); append-only."))
        elif target == "archived":
            # S12 / R5'' -- the SAME predicate `_conformance_violations` uses,
            # on the requested TARGET as the effective state.  This replaces the
            # separate `art.has_code_review_marker` gate that stood here: two
            # surfaces asking one question in two strengths is the drift S12
            # exists to prevent, and the marker was the weaker of the two.
            # Called regardless of the `Plan review:` declaration -- [R3-E1]
            # executed the bypass a declaration-keyed call leaves open.
            problems = review_record_violations(art, "archived")
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
# a finding, or an authorization (R2 / contract clause 2).


def _scaffold(art: Artifact, target: str, date: str) -> Tuple[str, str, List[str]]:
    """Return (status_from, status_to_or_note, [scaffold_block, manifest...])."""
    k = art.kind
    if k == "proposal":
        if target == "reviewed":
            block = (
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
            manifest = [
                "Status: proposed -> reviewed",
                "append the '## Review' section above (append-only; prior "
                "sections untouched).",
                "THE REVIEWER fills their own <reviewer>/<role>/<Model> -- this "
                "tool attributes nothing.",
                "one commit for this transition.",
            ]
            return ("proposed", "reviewed", [block] + manifest)
        if target == "revised":
            block = (
                "## Response -- <author> -- " + date + "\n\n"
                "**Model**: <model or tier>\n\n"
                "For each numbered critique, one disposition token + a "
                "one-sentence rationale (proposal-Response grammar: accept / "
                "accept with modification / reject / defer):\n\n"
                "* **[R1]** <accept|accept with modification|reject|defer> -- "
                "<rationale>\n\n"
                "<If accepted critiques substantially change the proposal, add a "
                "'## Revised proposal' section and set Status: revised.>\n\n"
                "<Scope delta -- ONLY if this revision narrows what the "
                "proposal will deliver, judged against the scope AS OPENED. "
                "Omit entirely when every opened outcome is still delivered.>\n\n"
                "**Scope delta**: preserved | degraded | lost\n\n"
                "**Removed scope**\n\n"
                "* <unit> -- source section; reason; revival/closure "
                "condition.\n\n"
                "**Disposition/home**: <where the grouped remainder lives>"
            )
            manifest = [
                "Status: reviewed -> revised",
                "append '## Response' (+ optional '## Revised proposal'); "
                "append-only.",
                "the Scope-delta block is OMITTED unless the revision narrows "
                "an outcome the proposal opened with; declining a reviewer's "
                "proposed expansion is not a reduction. THE TOOL DOES NOT "
                "CHECK THIS -- no transition refuses on a missing or malformed "
                "declaration; review is the enforcement.",
                "one commit for this transition.",
            ]
            return ("reviewed/revised", "revised", [block] + manifest)
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
        if target in ("awaiting-plan-review", "executing"):
            if target == "awaiting-plan-review":
                manifest = [
                    "Status: open -> awaiting-plan-review",
                    "no section to append yet -- the plan waits for its "
                    "'## Plan review' section to land before implementation.",
                    "(in-place status edit; plans are execution artifacts.)",
                ]
                return ("open", "awaiting-plan-review", manifest)
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
                "outcome is a deviation under AGENTS.md.>\n\n"
                "**Scope delta**: preserved | degraded | lost\n\n"
                "**Removed scope**\n\n"
                "* <unit> -- source section; reason; revival/closure "
                "condition.\n\n"
                "**Disposition/home**: <where the grouped remainder lives>"
            )
            manifest = [
                "Status: -> executing",
                "accepted scope is a FLOOR: a Sharpening that removes an "
                "accepted outcome needs the Maintainer's explicit disposition "
                "under the deviation gate. A plan reviewer cannot create that "
                "authority by calling the remainder 'out of scope'. THE TOOL "
                "DOES NOT CHECK THIS.",
                "for a review-required plan, the '## Plan review' section (+ "
                "Sharpening if findings) must have landed first; plan-open and "
                "first-implementation commits stay distinct.",
                "review/Sharpening sections are append-only.",
            ]
            return ("open/awaiting-plan-review", "executing", [block] + manifest)
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
                "Status: review -> archived; move the file to dev/plans/archive/.",
                "the plan-archive commit is DISTINCT from the implementing "
                "commits (proves review happened).",
                "every deferred follow-up carries a recorded disposition, "
                "named in the 'Dispositions:' block, with any 'defer' carrying "
                "the Maintainer's quoted authorization; the fidelity sign-off "
                "names the implementing commit + governing section.",
            ]
            return ("review", "archived", [block] + manifest)
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

    # Surface any current-state structural violations up front (R1 honesty).
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


# --- subcommand: scan (also the adopter fidelity scan, R3) -------------------


def cmd_scan(args: argparse.Namespace) -> int:
    """Run structural conformance over the local dev/ corpus; report violations.

    This is the read-only checker doing double duty as the **adopter-side
    fidelity scan** (R3): the same structural checks `next` reports per
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


# --- subcommand: guard (advisory pre-commit orientation, R4) -----------------


def cmd_guard(args: argparse.Namespace) -> int:
    """Advisory pre-commit pass -- warns, never blocks (R4).

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
