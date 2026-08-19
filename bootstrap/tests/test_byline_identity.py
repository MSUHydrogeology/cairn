"""Byline classification -- the exact, character-preserving identity fold.

This module guards the security core of the planner's three-way identity
model (`byline-classification`): the fold that reduces a display name to the
key actually compared, and the whole-name exact match that consumes it.

The defect it closes, stated once so every test below has a reason: the
superseded fold was ``re.sub(r"[^a-z0-9]", "", raw.lower())``, which deleted
every character that is not an ASCII letter or digit -- **including every
non-ASCII letter**. A Cyrillic character that renders identically to an ASCII
one was therefore *deleted*, and a byline that renders as an AI agent's name
was reduced to a key that intersected the human-Maintainer allowlist. One
invisible character moved a byline from "AI agent, flagged" to "recognized
human Maintainer, silent". The invariant the fix serves is:

    dropping a character must never widen authority.

**Character convention** (binding, carried from the proposal and its plan):
no confusable or invisible character appears as a literal in this module --
every one is written ``chr(0x...)``. Visibly-distinct international
characters (``Lukasz``'s slashed L, ``Ngo``'s circumflex, Cyrillic and Han
names) *do* appear as literals: a reader can see exactly what they are and
they carry no spoofing risk.

**Channel discipline.** For every test below, the expected values come from
somewhere other than the code under test:

* the behaviour table is transcribed from the accepted proposal's committed
  Evidence table, written before the implementation existed;
* the deletion-set pin builds its expectation from a hand-written literal
  transcribed from ``_fold_word``'s docstring;
* the non-empty-fold invariant takes its character sample *and* its
  letter/digit classification from ``unicodedata``, a standard-library table
  shipped with the interpreter -- the planner supplies only the function
  under test;
* the anti-collision corpus is hand-written here and never harvested by
  running the fold;
* the expected content of the ``unknown`` violation message is transcribed
  from the recorded expectation, and is asserted against what the public ``scan``
  arm actually prints.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unicodedata
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
_PLANNER_PATH = (
    CAIRN_ROOT / "templates" / "skills" / "_lib" / "lifecycle_planner.py"
)


def _load_planner() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "cairn_lifecycle_planner_byline", _PLANNER_PATH
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["cairn_lifecycle_planner_byline"] = module
    spec.loader.exec_module(module)
    return module


planner = _load_planner()


# --- fixtures ----------------------------------------------------------------


def _identity_model(tmp_path: Path, *, humans=None, ai=None):
    """An `IdentityModel` loaded through `_load_identity_model` over a
    temporary config -- the real loader path, not a hand-built model."""
    root = tmp_path / "repo"
    cfg = root / "dev" / ".cairn"
    cfg.mkdir(parents=True, exist_ok=True)
    body = {}
    if humans is not None:
        body["human_maintainers"] = humans
    if ai is not None:
        body["ai_agents"] = ai
    (cfg / "agent-identities.json").write_text(
        json.dumps(body), encoding="utf-8")
    return planner._load_identity_model(root)


#: The roster every behaviour-table row is classified against.
_ROSTER = ["Anthony Kendall"]


# --- A13: the behaviour table ------------------------------------------------
#
# Transcribed from the accepted proposal's Evidence table (`Evidence /
# verification plan`, roster ``["Anthony Kendall"]``), which was committed
# before any implementation existed.  Only the *proposed* column is asserted;
# the *today* column is history and is recorded in the plan, not here.
#
# The three boundary rows at the end are this plan's additions -- the
# whitespace-only, punctuation-only and zero-width-only bylines the
# proposal's table does not carry.  The empty byline is proposal row 20.

_BEHAVIOUR_TABLE = [
    # (id, byline, expected)
    ("rostered-exact", "Anthony Kendall", "human"),
    ("first-fragment-only", "Anthony", "unknown"),
    ("last-fragment-plus-other", "Kendall Jenner", "unknown"),
    ("last-fragment-plus-other-2", "Kendall Smith", "unknown"),
    ("rostered-plus-suffix", "Anthony Kendall Jr", "unknown"),
    ("unrelated-human", "Jane Doe", "unknown"),
    ("agent-versioned", "Claude Opus 5", "ai"),
    ("agent-scribing", "Claude scribing for Anthony Kendall", "ai"),
    ("agent-scribing-cyrillic-spoof",
     "Cl" + chr(0x430) + "ude scribing for Anthony Kendall", "unknown"),
    ("agent-scribing-digit-spoof",
     "Cl4ude scribing for Anthony Kendall", "unknown"),
    ("agent-scribing-transposed",
     "Cluade scribing for Anthony Kendall", "unknown"),
    ("rostered-cyrillic-spoof",
     "Anthony" + chr(0x430) + " Kendall", "unknown"),
    ("rostered-line-separator",
     "Anthony" + chr(0x2028) + "Kendall", "unknown"),
    ("rostered-nbsp",
     "Anthony" + chr(0x00a0) + "Kendall", "unknown"),
    ("rostered-fullwidth",
     chr(0xff21) + "nthony " + chr(0xff2b) + "endall", "unknown"),
    ("agent-cyrillic-spoof-alone",
     "Cl" + chr(0x430) + "ude Opus 5", "unknown"),
    ("agent-precomposed-accent", "Cláude Opus 5", "ai"),
    ("agent-mathematical-bold", chr(0x1d402) + "laude Opus 5", "ai"),
    ("agent-circled-letter", chr(0x24b8) + "laude Opus 5", "ai"),
    ("empty-byline", "", "unknown"),
    # --- boundary rows added by this plan ---
    ("whitespace-only-byline", "   ", "unknown"),
    ("punctuation-only-byline", "...", "unknown"),
    ("zero-width-only-byline", chr(0x200b), "unknown"),
]


@pytest.mark.parametrize(
    "byline,expected",
    [(row[1], row[2]) for row in _BEHAVIOUR_TABLE],
    ids=[row[0] for row in _BEHAVIOUR_TABLE],
)
def test_behaviour_table(tmp_path, byline, expected):
    """Every row of the proposal's Evidence table, driven through `classify`.

    Fails in the future state where the fold stops preserving characters, or
    where the human leg goes back to containment instead of tuple equality:
    the four spoof rows and the two fragment rows would return to ``human``.
    """
    im = _identity_model(tmp_path, humans=_ROSTER)
    assert im.classify(byline) == expected


def test_behaviour_table_covers_the_original_exploit(tmp_path):
    """The named exploit, asserted on its own so it cannot be lost in a table.

    A byline that *renders* as an AI agent scribing for the Maintainer, with
    one Cyrillic character standing in for an ASCII one, must not classify as
    the human Maintainer.  Fails the moment the granting fold deletes a
    non-ASCII letter again."""
    im = _identity_model(tmp_path, humans=_ROSTER)
    spoof = "Cl" + chr(0x430) + "ude scribing for Anthony Kendall"
    honest = "Claude scribing for Anthony Kendall"
    assert im.classify(spoof) == "unknown"
    assert im.classify(honest) == "ai"
    # The two bylines render identically; they are not the same string.
    assert spoof != honest
    assert ascii(spoof) != ascii(honest)


# --- the loader guards -------------------------------------------------------


def test_punctuation_only_roster_entry_is_not_a_wildcard(tmp_path):
    """A punctuation-only roster entry must not make a punctuation-only
    byline the human Maintainer.

    The guard has to test the **folded** value, not the raw entry: under
    tuple equality ``() == ()`` is ``True``, so an entry admitted as the
    empty tuple would match every byline that folds to nothing.  Fails in the
    future state where `_load_human_maintainers` reverts to a blank-*entry*
    test."""
    im = _identity_model(tmp_path, humans=["Anthony Kendall", "-"])
    assert () not in im.human
    for byline in (".", "-", "", "   ", "!!!"):
        assert im.classify(byline) == "unknown"
    assert im.classify("Anthony Kendall") == "human"


def test_empty_folding_ai_registry_entry_is_not_a_wildcard(tmp_path):
    """An AI-registry entry that folds to the empty string must not classify
    **every** byline as AI.

    ``"anything".startswith("")`` is ``True``, so an admitted empty token is
    a universal prefix.

    **The falsifying future state, run.** The guard this node protects is the
    empty-word filter on the folded value -- the ``if w`` in `_fold_words`,
    which `_load_ai_registry` relies on by building its tokens out of
    `_flag_words`. Two perturbations turn this node red, both executed:
    dropping that ``if w`` (which also reddens the human-side guard above,
    since it is the shared home of both filters), and a `_load_ai_registry`
    that folds an entry but admits the result without checking it is
    non-empty -- e.g. ``{_fold_word(str(t), "NFKD") for t in extra}``, which
    reddens this node **alone**.

    **And the perturbation that does NOT falsify it, recorded because the
    obvious guess is wrong.** Reverting `_load_ai_registry` to the superseded
    raw-entry predicate, ``{str(t).strip().lower() for t in extra if
    str(t).strip()}``, leaves this node **green**: a truthy ``.strip()``
    guarantees a non-empty ``.lower()``, so the superseded loader could not
    emit the empty token at all. The empty-token hazard does not pre-date
    this change -- it is *introduced* by it, which is what made folding the
    config entry symmetric with folding a byline word. A future state that
    stops folding does not re-open this hole; a future state that folds
    without filtering does."""
    im = _identity_model(tmp_path, humans=_ROSTER, ai=["-"])
    assert "" not in im.ai_registry
    assert im.classify("Anthony Kendall") == "human"
    assert im.classify("Jane Doe") == "unknown"
    assert im.classify("Ольга Иванова") == "unknown"
    # The extension mechanism still works for a real token.
    im2 = _identity_model(tmp_path, humans=_ROSTER, ai=["newvendor"])
    assert im2.classify("Newvendor 2 (Reviewer)") == "ai"


# --- the `unknown` violation message -----------------------------------------
#
# Two **message-only** additions on the security-diagnostic path, and
# they are the one user-facing surface this change introduces:
#
#   1. the roster grammar -- an entry must be the COMPLETE display name as it
#      appears in the byline, not a name fragment;
#   2. an ``ascii()``-escaped rendering, appended whenever the byline holds a
#      character outside ASCII.
#
# Both are asserted through the **public** ``scan`` arm rather than at helper
# level: a diagnostic that never reaches the operator's terminal is not a
# diagnostic.  The expected content is transcribed from the recorded wording,
# written before the implementation existed; the code under test supplies only
# the string it actually prints.


def _git(args, cwd: Path) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), check=True,
                   capture_output=True, text=True)


def _scan_repo(tmp_path: Path, *, name: str, byline: str, humans) -> Path:
    """A minimal checkout holding one accepted proposal whose ``## Decision``
    is bylined `byline`, ready for ``planner.main(["scan"])``.

    ``scan`` resolves its root through ``git rev-parse``, so the checkout is a
    real (empty) repository."""
    repo = tmp_path / name
    repo.mkdir()
    _git(["init", "-q"], repo)
    _git(["config", "user.email", "t@example.com"], repo)
    _git(["config", "user.name", "Test"], repo)
    (repo / "dev" / "proposals").mkdir(parents=True)
    (repo / "dev" / "plans").mkdir(parents=True)
    cfg = repo / "dev" / ".cairn"
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / "agent-identities.json").write_text(
        json.dumps({"human_maintainers": humans}), encoding="utf-8")
    (repo / "dev" / "proposals" / "p.md").write_text(
        "# p.md\n\n"
        "**Author**: Claude (Strategy)\n"
        "**Date opened**: 2026-05-01\n"
        "**Status**: accepted\n"
        "**Plan review**: required(Internal)\n\n"
        "## Context\n\nx\n\n"
        "## Review -- Codex (External Reviewer) -- 2026-05-02\n\nx\n\n"
        f"## Decision -- {byline} (Maintainer) -- 2026-05-03\n\n"
        "Accepted.\n\n> a quoted authorization\n",
        encoding="utf-8")
    return repo


def test_unknown_identity_message_carries_the_roster_grammar_and_ascii_escape(
        tmp_path, monkeypatch, capsys):
    """Both message additions, through the public ``scan`` arm.

    The byline here is the sharpest case the change has: a ``## Decision``
    spelled ``Anthony Kend`` + CYRILLIC SMALL LETTER A + ``ll``, which renders
    character-for-character like the rostered ``Anthony Kendall`` in every
    editor, terminal, diff and web view. The classifier already refuses it
    (that is the behaviour table's job); what this node guards is that the
    *operator* can act on the refusal:

    * without the ``ascii()`` escape the report shows a ``repr()`` that
      *renders* as ``'Anthony Kendall'`` -- ``repr()`` of a ``str`` leaves
      non-ASCII characters as-is -- so the reader is told that a byline
      looking exactly right is unrecognized, and is given nothing to look at.
      A flag the reader cannot interpret is half a flag;
    * without the roster-grammar sentence a Maintainer with a genuinely
      unrostered name is told to configure a file but not what shape an entry
      now takes, which is the one thing this change altered about it.

    **Two falsifying future states, both run.** Delete ``_ascii_hint(d.name)``
    from the message and the escape assertion fails; delete the
    complete-display-name sentence and the grammar assertions fail. The
    ASCII-only leg below is the third: it fails if ``_ascii_hint`` stops
    checking ``str.isascii`` and appends an escape to every byline, which
    would bury the signal in noise on the ordinary path."""
    spoof = "Anthony Kend" + chr(0x430) + "ll"
    honest = "Anthony Kendall"
    # The premise, restated as an assertion: `repr()` leaves the confusable
    # raw (so the two reprs render alike), `ascii()` spells it out.
    assert spoof != honest
    assert chr(0x430) in repr(spoof)
    # The six ASCII characters `\u0430`, built numerically so that no
    # confusable appears as a bare literal here (the module convention).
    escape = "%su%04x" % ('\\', 0x430)
    assert escape in ascii(spoof) and escape not in ascii(honest)

    repo = _scan_repo(tmp_path, name="spoof", byline=spoof, humans=[honest])
    monkeypatch.chdir(repo)
    assert planner.main(["scan"]) == 1
    out = capsys.readouterr().out

    assert "UNRECOGNIZED identity" in out
    # Addition 2 -- the confusable is spelled out where a reader can see it.
    assert escape in out, (
        "the unknown-identity report does not escape the non-ASCII byline; "
        "the reader is shown a repr() that renders like the rostered name"
    )
    # Addition 1 -- the roster grammar, so the reader can act on the flag.
    assert "COMPLETE display name" in out
    assert "not a name fragment" in out

    # The ASCII leg: an ordinary unrecognized byline carries NO escape suffix.
    repo2 = _scan_repo(tmp_path, name="plain", byline="Sage", humans=[honest])
    monkeypatch.chdir(repo2)
    assert planner.main(["scan"]) == 1
    out2 = capsys.readouterr().out
    assert "UNRECOGNIZED identity" in out2 and "'Sage'" in out2
    assert "escaped:" not in out2
    assert "COMPLETE display name" in out2


# --- the non-empty-fold invariant --------------------------------------------
#
# The Decision's invariant is "dropping a character must never widen
# authority".  Its literal proposal wording -- "the fold preserves every
# input character" -- cannot hold: case folding and combining-mark stripping
# both *replace* letters.  The form below can both hold and fail: **no letter
# and no digit folds to nothing.**
#
# Channel: the character sample and the L*/N* classification come from
# ``unicodedata``, a table shipped with the interpreter.  The planner
# supplies only the function under test.

#: Transcribed by hand from ``_fold_word``'s docstring -- "keep a character
#: only if it is non-ASCII or in ``_FOLD_KEEP_ASCII``", where the allow-set
#: is the ASCII lower-case letters and the ASCII digits.  Written out here
#: rather than imported, so the pin compares the *stated* rule against the
#: *executed* one instead of comparing the code to itself.
_ALLOW_SET_ASCII = frozenset("abcdefghijklmnopqrstuvwxyz0123456789")


def _letters_and_digits():
    """Every codepoint whose Unicode general category begins ``L`` or ``N``.

    The whole codespace, not a sampled set of blocks -- the sample is cheap
    (about a third of a second) and a sampled invariant is exactly the kind
    of near-vacuous guard this module exists to replace."""
    for cp in range(0x110000):
        c = chr(cp)
        if unicodedata.category(c)[0] in "LN":
            yield c


def test_no_letter_or_digit_folds_to_nothing_on_the_granting_leg():
    """The granting leg (``NFD``) deletes **no** letter and **no** digit, in
    any script, anywhere in the codespace.

    This is the leg where a deletion would *grant* authority, so the
    invariant is unconditional there.  Fails in the future state where the
    granting fold reverts to an ASCII-deletion rule -- measured, that state
    deletes six figures' worth of letters to nothing."""
    empties = [c for c in _letters_and_digits() if planner._fold_word(c, "NFD") == ""]
    assert empties == [], (
        f"{len(empties)} letters/digits fold to nothing on the GRANTING leg; "
        f"first few: {[hex(ord(c)) for c in empties[:10]]}"
    )


def test_flagging_leg_empties_are_only_compatibility_marks():
    """The flagging leg (``NFKD``) has a characterized exception class, and
    the characterization -- not a codepoint list read off the fold -- is what
    is asserted.

    ``NFKD`` maps a handful of *isolated presentation forms* of combining
    marks (Arabic tashkil isolated forms, halfwidth katakana voiced-sound
    marks) onto a bare mark, or onto a space plus a mark. Those fold to
    nothing. Each is a mark wearing a letter's general category, not a
    letter, and the direction is safe: an empty *flagging* key can only
    under-flag a word made **entirely** of such characters -- it cannot
    grant, because the granting leg never sees ``NFKD``.

    The oracle is ``unicodedata`` plus the fold's documented allow-set: every
    character that folds to nothing at ``NFKD`` must decompose entirely into
    combining marks and ASCII characters outside the allow-set. Fails in the
    future state where the flagging fold starts deleting a real letter."""
    for c in _letters_and_digits():
        if planner._fold_word(c, "NFKD") != "":
            continue
        decomposed = unicodedata.normalize("NFKD", c)
        assert all(
            unicodedata.combining(x)
            or (x.isascii() and x.lower() not in _ALLOW_SET_ASCII)
            for x in decomposed
        ), (
            f"{hex(ord(c))} ({unicodedata.name(c, '?')}) folds to nothing at "
            f"NFKD but is not a compatibility mark"
        )


# --- the deletion-set pin -----------------------------------------------------
#
# The superseded rule named two deleted classes and deleted three.  The
# corrected rule is an explicit allow-set, and this pins it mechanically --
# the check the proposal's "Why this tier" section asked a reviewer to
# perform by hand, moved into the suite so it runs every time.  The allow-set
# literal it checks against is ``_ALLOW_SET_ASCII``, above.


@pytest.mark.parametrize("form", ["NFD", "NFKD"])
def test_fold_deletes_exactly_the_stated_ascii_set(form):
    """The ASCII characters the fold deletes are exactly the complement of
    the allow-set the docstring states.

    Case folding runs first, so an ASCII upper-case letter survives as its
    lower-case self and is **not** in the deleted set.  The three deleted
    classes are therefore one statement: every ASCII character that is
    neither an ASCII letter nor an ASCII digit -- which is ASCII punctuation
    and symbols, the ASCII space characters, the C0 controls and DEL.

    Fails in the future state where the fold's kept-character test widens
    (say, to ``c.isalnum()``, which admits nothing new in ASCII but would
    change the rule the docstring states) or narrows."""
    deleted = {cp for cp in range(0x80)
               if planner._fold_word(chr(cp), form) == ""}
    expected = {cp for cp in range(0x80)
                if chr(cp).lower() not in _ALLOW_SET_ASCII}
    assert deleted == expected
    # And the three classes the docstring names are each really in it.
    assert 0x00 in deleted and 0x1f in deleted and 0x7f in deleted  # C0 + DEL
    assert ord(" ") in deleted and ord("\t") in deleted             # spaces
    assert ord("-") in deleted and ord("+") in deleted              # punct/symbol
    assert ord("A") not in deleted and ord("z") not in deleted
    assert ord("0") not in deleted and ord("9") not in deleted


# --- the corpus, the anti-collisions, the pinned merges ----------------------
#
# The earlier roster-symmetry test was near-vacuous -- its oracle was
# the function under test, so it passes for every total function.  Its
# replacement is an **anti-collision** test over an adversarial corpus.
#
# The corpus is a deliverable, and dissimilarity gives it no power: a corpus
# of realistic-but-unrelated international names passes even against a fold
# that reduces each word to its first letter, because no two of those names
# share initials.  Every entry below is here because some *wrong* fold would
# merge it with its partner.

_CORPUS = [
    # shared initials + a prefix pair: catches a truncating or otherwise
    # destructive fold (a first-letter fold merges both pairs).
    "Anthony Kendall",
    "Amos Kim",
    "Jane Doe",
    "Jan Doe",
    # non-decomposing non-ASCII letters: catches a fold that deletes or
    # transliterates non-ASCII.  The slashed L and the slashed o have no
    # canonical decomposition, so these must stay distinct from their
    # ASCII-spelled partners.
    "Łukasz Nowak",
    "Lukasz Nowak",
    "Søren Dahl",
    "Soren Dahl",
    # decomposing accents: these are the DELIBERATE merges, pinned by the
    # node below rather than asserted apart.
    "Ana Ngô",
    "Ana Ngo",
    "Ibrahim Şahin",
    "Ibrahim Sahin",
    # single-character-apart non-Latin pairs: catches a fold that empties or
    # collapses a whole script (both members of a pair would become one key).
    "Иван Петров",
    "Иван Петрова",
    "张伟",
    "张军",
]

#: The pairs the accepted design deliberately merges -- canonical-
#: decomposition equivalence plus full case folding.  Every
#: OTHER pair in the corpus must stay distinct.
_PINNED_MERGES = {
    frozenset({"Ana Ngô", "Ana Ngo"}),
    frozenset({"Ibrahim Şahin", "Ibrahim Sahin"}),
}


def test_no_corpus_name_is_mistaken_for_another(tmp_path):
    """The anti-collision test that replaces the vacuous symmetry one.

    No corpus name classifies ``human`` against a roster holding a
    *different* corpus name, except for the pairs deliberately merged.

    Fails in the future state where the fold becomes lossy in any direction
    that merges two real names: measured, a first-letter-truncating fold
    fails here with ``Amos Kim`` / ``Anthony Kendall`` and ``Jan Doe`` /
    ``Jane Doe`` among the collisions."""
    collisions = []
    for rostered in _CORPUS:
        im = _identity_model(tmp_path, humans=[rostered])
        for byline in _CORPUS:
            if byline == rostered:
                continue
            if im.classify(byline) == "human":
                collisions.append((rostered, byline))
    unexpected = [pair for pair in collisions
                  if frozenset(pair) not in _PINNED_MERGES]
    assert unexpected == [], f"unexpected identity collisions: {unexpected}"


def test_ratified_r2_merges_still_occur(tmp_path):
    """The residual pin: the accent and case-fold classes still collide.

    These are **pinned, not fixed**. The rule accepts that canonical-decomposition
    equivalence plus full case folding widens the set of strings that
    classify ``human``; pinning the widening means a later narrowing of the
    granting fold is a deliberate, visible test change rather than a silent
    behaviour drift.

    Rows transcribed from the Internal review's measured output block, which
    was committed before this implementation existed. Two classes:

    * **[I1a] full case folding** puts ligature and long-s expansions on the
      granting path. ``chr(0x17f)`` renders as a long *s* and reads as an
      **f** to a modern eye, so a byline a reader sees as *"Kriften Long"*
      classifies as the rostered *"Kristen Long"* -- neither a case nor a
      diacritic variant.
    * **[I1b] combining-mark stripping** collapses marks that carry *letter
      identity* outside Latin: two Vietnamese tones, hiragana KA vs GA, the
      Devanagari nukta turning KA into QA, and Cyrillic YE vs YO. In each
      case a **different person's name** classifies as the rostered one.

    Fails in the future state where the granting fold stops stripping
    combining marks or stops case-folding -- which is the rule\'s own named
    recovery path, and should be a visible edit to this test."""
    pairs = [
        # (label, rostered name, byline that must still collide with it)
        ("[I1a] long s", "Kristen Long", "Kri" + chr(0x17f) + "ten Long"),
        ("[I1a] st-ligature", "Kristen Long", "Kri" + chr(0xfb05) + "en Long"),
        ("[I1b] Vietnamese tone",
         "Nguy" + chr(0x1ec5) + "n", "Nguy" + chr(0x1ebf) + "n"),
        ("[I1b] Japanese dakuten",
         chr(0x304b) + chr(0x3068) + chr(0x3046),
         chr(0x304c) + chr(0x3068) + chr(0x3046)),
        ("[I1b] Devanagari nukta",
         chr(0x915) + chr(0x93f) + chr(0x930),
         chr(0x915) + chr(0x93c) + chr(0x93f) + chr(0x930)),
        ("[I1b] Cyrillic YE/YO",
         chr(0x415) + chr(0x43b) + chr(0x43a) + chr(0x438) + chr(0x43d),
         chr(0x401) + chr(0x43b) + chr(0x43a) + chr(0x438) + chr(0x43d)),
    ]
    for label, rostered, byline in pairs:
        im = _identity_model(tmp_path, humans=[rostered])
        assert im.classify(byline) == "human", f"{label} no longer merges"


def test_roster_symmetry_smoke_check(tmp_path):
    """Kept and relabelled, and it carries **no** perturbation.

    ``classify(x)`` with roster ``[x]`` holds for *every* total fold, because
    both sides go through the same function: this cannot detect over-folding,
    and that is why. It is retained as what it actually
    is -- a smoke check that (a) no corpus name trips the AI leg and (b) no
    corpus name folds to the empty key and gets dropped by the loader guard.
    Claiming a falsifying perturbation for it would be the vacuity this
    module exists to remove.

    The one future state it does fail in: a fold that empties a whole script,
    which drops the roster entry and makes the name unrecognizable to
    itself. That is the case the anti-collision test cannot see, because an emptied roster
    produces no collisions at all."""
    for name in _CORPUS:
        im = _identity_model(tmp_path, humans=[name])
        assert im.classify(name) == "human", f"{name!r} not recognized as itself"


# --- the separator cost, with its exit ---------------------------------------


def test_non_ascii_space_separator_costs_a_false_positive(tmp_path):
    """A cost-recording test: it asserts the false positive **exists**,
    and asserts the remedy alongside it.

    Word splitting is ASCII-whitespace-only, so a display name written with a
    Unicode ``Zs`` separator does not tokenize into separate words: a CJK
    byline separated by IDEOGRAPHIC SPACE and a French byline separated by
    NARROW NO-BREAK SPACE both classify ``unknown`` against a roster typed
    with an ASCII space. Both are legitimate real-world spellings. The
    direction is safe -- it over-flags, it does not grant -- but it is a real
    false positive, and it is a **behaviour change**: the superseded
    tokenizer used a bare ``str.split()``, which is Unicode-aware, so those
    bylines are recognized today.

    The exit is rostering the exact separator, and it is asserted here so the
    cost is recorded with its way out rather than as a dead end.

    Fails in the future state where the tokenizer treats Unicode ``Zs`` as a
    word break -- which is exactly the signal that the optional design change
    landed, and at that point the false-positive half of this test inverts."""
    cjk_ascii, cjk_wide = "王 伟", "王" + chr(0x3000) + "伟"
    fr_ascii, fr_narrow = "Jean Dupont", "Jean" + chr(0x202f) + "Dupont"

    im_ascii = _identity_model(tmp_path, humans=[cjk_ascii, fr_ascii])
    assert im_ascii.classify(cjk_wide) == "unknown"
    assert im_ascii.classify(fr_narrow) == "unknown"
    assert im_ascii.classify(cjk_ascii) == "human"
    assert im_ascii.classify(fr_ascii) == "human"

    # The remedy: roster the name exactly as the byline spells it.
    im_exact = _identity_model(tmp_path, humans=[cjk_wide, fr_narrow])
    assert im_exact.classify(cjk_wide) == "human"
    assert im_exact.classify(fr_narrow) == "human"
    # Comparison is separator-for-separator in both directions.
    assert im_exact.classify(fr_ascii) == "unknown"

    # The flagging leg is unaffected: NFKD maps these separators onto an
    # ASCII space, which the allow-set then drops, so a separator cannot be
    # used to smuggle an agent byline past the AI leg.
    assert im_ascii.classify("Cl" + chr(0x202f) + "aude") == "ai"
    assert im_ascii.classify("Cl" + chr(0x3000) + "aude") == "ai"


# --- the homoglyph residual pin ----------------------------------------------


def test_independence_comparator_closes_three_of_four_variants():
    """The measured state, pinned as a **known residual**.

    The independence comparator (`_identity_token`) decides whether a Review
    was authored by the artifact's own author. It now folds at ``NFKD``, so
    three of the four measured disguise variants of an author byline are
    caught where none was before. The Cyrillic-homoglyph variant is **not**
    caught: a same-agent review spelled with a confusable still satisfies the
    ``independent_review`` gate.

    Not fixed here, and deliberately so: every sound fix needs a
    reviewer-identity contract that does not exist, and the only human list
    that does exist confers Decision authority. Pinning the 3-of-4 state
    means it cannot regress silently, and means closing it is a deliberate
    test change.

    Fails in the future state where the comparator gains a confusables
    mapping -- at which point the fourth variant is caught and this test
    should be rewritten to assert 4 of 4, not relaxed."""
    author = "Claude (Strategy)"
    flagged = {
        label: planner._identity_token(variant) == planner._identity_token(author)
        for label, variant in (
            ("precomposed accent", "Cláude (Internal Review)"),
            ("mathematical bold", chr(0x1d402) + "laude (Internal Review)"),
            ("circled letter", chr(0x24b8) + "laude (Internal Review)"),
            ("Cyrillic homoglyph", "Cl" + chr(0x430) + "ude (Internal Review)"),
        )
    }
    assert flagged == {
        "precomposed accent": True,
        "mathematical bold": True,
        "circled letter": True,
        "Cyrillic homoglyph": False,   # open residual
    }
