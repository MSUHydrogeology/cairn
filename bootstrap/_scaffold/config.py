"""Scaffold engine -- configuration / tokens / profile resolution (scaffold-split Stage 4).

The static install schema and configuration-resolution surface: the profile
**recognizer** (the sole runtime YAML reader), the inline-token vocabulary, the
template/skills/module mapping registries (including the trust anchor
``_MODULE_MAPPINGS`` the release-security scanner reads), and the governance
preset / six-axis resolution that derives a module roster + profile summary.

A **pure stdlib leaf**: it imports only the standard library and holds no
adopter-tree writes (the dev-tree / gitignore / fan-out writers stay in the
engine; they consume this module's data). **This module** owns no file writes and
no CLI/upgrade execution; importing it defines names only (import-purity).
Note this is an *ownership* property, not a runtime-loading boundary: importing
``bootstrap._scaffold.config`` runs the eager package facade
(``bootstrap._scaffold.__init__``) first, which loads the whole engine
(install / upgrade / cli included) -- see the ``test_trust_anchor_imports_are_
owner_specific_not_runtime_isolated`` regression. install / upgrade depend on it,
never the reverse.

Pure motion from the pre-split monolith (Stage 4): the symbols are unchanged;
only their home moved. ``_MODULE_MAPPINGS`` migrates here as its owning module
(plan 0B.3); ``bootstrap/security_check.py`` imports the trust anchor from this
narrow owner. Loaded via the engine's verifying finder, so this file's real path
is confirmed within the Cairn root before it executes.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, NamedTuple


#: **PyYAML is not a runtime parser.**  Until 2026-08-03 this module picked its
#: parser from whatever happened to be importable -- ``yaml.safe_load`` when
#: PyYAML was installed, the in-tree reader otherwise -- so an adopter's install
#: behaviour depended on an unrelated package being present.  Cairn's runtime
#: contract is **zero adopter dependencies**, which made the in-tree path the
#: one most adopters ran and the one Cairn least exercised.  The recognizer
#: below is now the **sole runtime parser**; PyYAML survives only as a
#: **test-only oracle** the suite compares against (see
#: ``bootstrap/tests/test_profile_grammar.py``).  ``_yaml`` stays bound to
#: ``None`` because the engine facade re-exports it.
_yaml = None  # type: ignore[assignment]


def _yaml_load(text: str) -> Any:
    """Compatibility alias for :func:`_minimal_yaml_parse`.

    Retained because the engine facade re-exports it and existing tests import
    it.  **Never use it as a parity oracle**: it *is* the function under test,
    so ``_yaml_load(x) == _minimal_yaml_parse(x)`` compares a function to
    itself.  Import ``yaml`` directly for an oracle."""
    return _minimal_yaml_parse(text)


#: The inline tokens the core and module templates currently use.  The
#: scaffold only substitutes tokens present in this set.  A profile key
#: outside ``RECOGNIZED_PROFILE_KEYS`` is **refused** before any write --
#: the profile schema is closed, and the reserved ``schema`` key (not a
#: silent tolerance for unknown keys) is what lets a future engine say
#: "this profile declares schema 2; this engine understands 1".
#: Documented in BOOTSTRAP.md Appendix A.
KNOWN_TOKENS: frozenset[str] = frozenset(
    {
        "project_name",
        "test_command",
        "claim_check_command",
        # The repo-relative Python package a python-security adopter scans
        # A *required*
        # token for that module -- see ``_MODULE_REQUIRED_TOKENS`` and the
        # selected-module required-token preflight that fails closed before
        # any write when a selected module's required token is unfilled.
        "python_package",
    }
)


#: Default-on modules installed when the profile YAML omits a
#: ``modules:`` key.  Matches the doctrine in BOOTSTRAP.md Act I-5
#: step 2 ("Default-on modules (installed *unless* a dimension removes
#: them)").
_DEFAULT_ON_MODULES: tuple[str, ...] = (
    "reflections",
    "claim-check",
    "incident-trackers",
    "documentation-plan",
    # Measured-zero install cost, with a loud modules_remove opt-out for an
    # adopter whose agents ingest only operator-attached content.
    "content-security",
    # security-verification-activation Chunk B: the local security-evidence
    # dispatcher becomes universal.  Its shipped registry admitted no entry
    # at activation-v1, so no evidence was gathered until a capability's own
    # proposal was accepted and its registry entry admitted; default-on is
    # what makes the *route* standard, not the evidence.
    #
    # RESOLVED (api-web-security-modules Chunk G, 2026-08-11): a stock
    # install's first `scripts/run_security_verification.py local` used to
    # exit 5 (INCOMPLETE) instead of the plan's intended 0 (NOT APPLICABLE),
    # because the dispatcher selected capabilities by the `-security` NAME
    # SUFFIX and `content-security` -- default-on since the sibling
    # default-security-stance scope -- matched it while having no admitted
    # registry entry. Chunk G replaced that heuristic with a source-owned
    # declared-capability set (`_DECLARED_CAPABILITY_MODULES` in
    # `run_security_verification.py`) that does not include
    # `content-security`, so a stock install now exits 0 with the NOT
    # APPLICABLE line, matching the plan's original intent.  Re-measured, not
    # carried forward: see `test_security_verification.py`'s
    # `test_the_dispatcher_runs_from_a_real_fresh_scaffold` (formerly the
    # characterization node) and `TestTheDeclaredCapabilitySetReplacesTheNameSuffixHeuristic`.
    "security-verification",
)


# ---------------------------------------------------------------------------
# The closed profile grammar (the sole runtime parser)
# ---------------------------------------------------------------------------
#
# The installer's only substantive input is the adopter's profile.  It used to
# be read best-effort: any line the reader did not understand was skipped, so a
# profile could install the wrong tree at exit 0.  The reader below is a
# **recognizer** instead -- it accepts exactly the eight line forms documented
# on ``_minimal_yaml_parse`` and refuses everything else with a file, a line
# number, and the rewrite.  There is no third outcome: for every profile text
# it either returns a value equal to ``yaml.safe_load``'s or raises.  (The
# equality half is verified against PyYAML as a test-only oracle over a finite
# corpus; the *totality* half -- no content line is ever silently dropped -- is
# structural, because the parse loop refuses any line matching no form.)


class ProfileGrammarError(ValueError):
    """A profile line the closed grammar does not accept.

    The message is ``<path>:<line>: <reason>`` and, wherever one exists, the
    **rewrite** that makes the line acceptable.  "Install PyYAML" is never an
    acceptable remedy in a zero-dependency project.  A ``ValueError`` subclass
    so callers already catching ``ValueError`` keep working."""


#: A profile key.  The ``:`` must be followed by end-of-line or whitespace, so
#: ``preset:solo-greenfield`` (which YAML reads as a *plain scalar document*,
#: not a mapping) is refused rather than silently read as a key.
_PROFILE_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_.-]*):(?: +(.*))?$")

#: The one numeric form whose meaning is unambiguous across YAML versions.
#: Anything else that *starts* like a number (``010``, ``1:30``, ``2024-01-01``,
#: ``1.5``) is refused with "write it quoted".
_PROFILE_INT_RE = re.compile(r"^-?(0|[1-9][0-9]*)$")

#: Characters that may not open a plain scalar: the YAML indicators, plus the
#: flow closers that cannot legally start one either.
_PROFILE_INDICATORS = "&*!|>[]{}@`%,"

#: Plain scalars YAML 1.1 reads as a boolean or null.  ``forge: no`` is
#: ``False``, not ``"no"`` -- refused with "write it quoted".  Also refused as
#: a **key**: ``on:`` is the mapping key ``True`` to PyYAML and the string
#: ``"on"`` to a textual reader, which is the same different-key hazard the
#: byte-order-mark rule closes.
_PROFILE_RESERVED_SCALARS: frozenset[str] = frozenset({
    "y", "Y", "yes", "Yes", "YES", "n", "N", "no", "No", "NO",
    "true", "True", "TRUE", "false", "False", "FALSE",
    "on", "On", "ON", "off", "Off", "OFF",
    "null", "Null", "NULL", "~",
})

#: Whole plain scalars YAML resolves to something that is not a string and not
#: a value at all: ``=`` is the YAML 1.1 *value* key and ``<<`` the *merge*
#: key, and ``safe_load`` raises ``ConstructorError`` on both.  ``?`` opens a
#: complex mapping key and raises ``ScannerError``.  Each is refused, because
#: a textual reader would otherwise hand back a plain string where the oracle
#: refuses -- the third outcome the contract denies.  (These are *tokens*, not
#: prefixes: ``==``, ``=x``, ``<<x`` and ``?x`` are ordinary plain scalars to
#: PyYAML and stay accepted.)
_PROFILE_RESOLVER_TOKENS: frozenset[str] = frozenset({"=", "<<", "?"})

#: C0 (minus tab / newline / carriage return), DEL, C1, the Unicode line/para
#: separators, and the byte-order mark.  ``project_name`` is rendered into the
#: generated adopter tree *and* printed by ``--summary``, so a control
#: character reaching it is a security question, not a tidiness one; a
#: BOM-prefixed key silently becomes a *different key*.
_PROFILE_CONTROL_RE = re.compile(
    "[\\x00-\\x08\\t\\x0b\\x0c\\x0e-\\x1f\\x7f-\\x9f"
    "\\u2028\\u2029\\ufeff]"
)

#: **YAML's only whitespace is SPACE and TAB.**  Python's no-argument
#: ``str.strip()`` removes every character for which ``str.isspace()`` is true
#: -- NBSP, the EN/EM quad family, the ideographic space -- so a reader built
#: on it *consumes* characters YAML treats as ordinary text.  An NBSP-prefixed
#: ``project_name`` is read as ``project_name`` by such a reader and as
#: ``"\xa0project_name"`` by PyYAML: a **different key**, exactly the
#: byte-order-mark hazard above, from a character ordinary copy-paste out of a
#: rendered page produces.  Refused with the codepoint named, because the
#: character is invisible in an editor and a generic "unrecognized line" would
#: point at a line that looks perfectly correct.
#:
#: This class is the **diagnostic**, not the guarantee.  The guarantee is that
#: the tokenizer below only ever strips ``" "`` -- ``line.strip(" ")``,
#: ``raw.lstrip(" ")`` and ``value.rstrip(" ")``, with tab, CR/LF and the
#: C0/C1 separators refused or consumed before it runs -- so a whitespace
#: character this class does not list cannot be silently eaten; it falls
#: through to a refusal.
#:
#: **Do not loosen any of those three to the no-argument form**, and do not
#: rely on this class to catch it if you do: the diagnostic runs *first*, so
#: while it is in place a loosened tokenizer is invisible.
#: ``TestInvisibleWhitespaceIsNotConsumed`` in ``test_profile_grammar.py``
#: therefore disables this class and re-asserts the contract over every
#: ``str.isspace()`` codepoint against the tokenizer alone -- which is what
#: makes the paragraph above a tested claim rather than a comment, and what
#: catches a future Unicode revision that adds a codepoint this class omits.
_PROFILE_UNICODE_SPACE_RE = re.compile(
    "[\\u00a0\\u1680\\u2000-\\u200a\\u202f\\u205f\\u3000]"
)

#: The profile schema version this engine understands.  ``schema:`` is
#: **reserved**: an absent or matching value is accepted and ignored, a
#: different one refuses with a version message.  It buys nothing today (it
#: rescues no engine already released) and everything later -- it is what lets
#: a future refusal say *"this profile declares schema 2; this engine
#: understands 1"* instead of *"unknown key"*.
_ENGINE_PROFILE_SCHEMA = 1


def _minimal_yaml_parse(text: str, source: str = "<profile>") -> dict[str, Any]:
    """Recognize the profile subset; refuse everything else.

    Eight accepted line forms -- every non-blank line matches exactly one, or
    the profile is refused:

    ==  ==========================================================
    -  a blank line, or a comment line (first non-space is ``#``)
    -  a single leading ``---`` document marker
    -  ``key: <plain scalar>``
    -  ``key: '<single-quoted>'`` (``''`` unescapes to ``'``)
    -  ``key: "<double-quoted>"`` (no backslash, no interior ``"``)
    -  ``key: []``
    -  a bare ``key:`` (value ``None`` unless list items follow)
    -  ``- <scalar>`` at a consistent indent under an open bare key
    ==  ==========================================================

    Plus two whole-document rules: a literal ``{}`` document is an empty
    mapping, and a document with **no content lines at all** (zero-byte,
    whitespace-only, comment-only) is refused rather than read as ``{}``.

    A ``#`` starts a comment **only** at the start of a value or when preceded
    by a space or tab, so ``project_name: issue#42-tracker`` keeps its hash
    while ``forge: gitlab   # gitlab | github`` loses its comment.

    *source* is the path quoted in refusals; :func:`load_config` passes the
    real profile path.  Raises :class:`ProfileGrammarError`.
    """
    def refuse(lineno: int, reason: str) -> None:
        raise ProfileGrammarError(f"{source}:{lineno}: {reason}")

    control = _PROFILE_CONTROL_RE.search(text)
    if control is not None:
        char = control.group(0)
        where = text.count("\n", 0, control.start()) + 1
        if char == "\ufeff":
            refuse(where, "a byte-order mark (U+FEFF) makes the key that "
                          "follows it a different key; save the file as UTF-8 "
                          "without a BOM")
        if char == "\t":
            refuse(where, "a tab character; YAML forbids tabs in indentation "
                          "and rejects them inside plain values -- indent and "
                          "separate a trailing comment with spaces")
        refuse(where, f"a control character (U+{ord(char):04X}) is not "
                      "allowed in a profile; remove it")

    space = _PROFILE_UNICODE_SPACE_RE.search(text)
    if space is not None:
        char = space.group(0)
        where = text.count("\n", 0, space.start()) + 1
        refuse(where, f"a Unicode space character (U+{ord(char):04X}) that is "
                      "not an ordinary space; YAML's only whitespace is SPACE "
                      "and TAB, so this character is part of the key or value "
                      "rather than a separator -- it is invisible in an editor "
                      "and typically arrives by copy-paste from a rendered "
                      "page.  Replace it with an ordinary space")

    def scalar(raw: str, lineno: int, allow_empty_list: bool) -> tuple[bool, Any]:
        """``(present, value)`` for the text after ``key:`` or ``- ``.

        ``present`` is False when the text is empty or only a comment -- the
        caller turns that into a bare key (``None``) or a refusal."""
        text_ = raw.lstrip(" ")
        if not text_ or text_.startswith("#"):
            return False, None

        def check_tail(rest: str) -> None:
            if rest and not (
                rest[0] == " " and rest.lstrip(" ").startswith("#")
            ):
                refuse(lineno, "trailing text after the value; a trailing "
                               "comment needs a space before its `#`")

        if text_[0] in ("'", '"'):
            quote = text_[0]
            out: list[str] = []
            index = 1
            closed = False
            while index < len(text_):
                char_ = text_[index]
                if quote == "'":
                    if char_ == "'":
                        if text_[index + 1:index + 2] == "'":
                            out.append("'")
                            index += 2
                            continue
                        closed = True
                        index += 1
                        break
                else:
                    if char_ == "\\":
                        refuse(lineno, "a backslash escape in a double-quoted "
                                       "value is not accepted; use the "
                                       "single-quoted form (`'...'`, doubling "
                                       "any embedded `'`)")
                    if char_ == '"':
                        closed = True
                        index += 1
                        break
                out.append(char_)
                index += 1
            if not closed:
                refuse(lineno, f"unterminated {quote}-quoted value; close the "
                               "quote")
            check_tail(text_[index:])
            return True, "".join(out)

        if text_[0] == "[":
            if not allow_empty_list or text_[:2] != "[]":
                refuse(lineno, "an inline `[a, b]` list is not accepted; write "
                               "`key:` on its own line followed by `  - a` "
                               "lines")
            check_tail(text_[2:])
            return True, []

        if text_[0] == "{":
            refuse(lineno, "an inline `{...}` mapping is not accepted; the "
                           "profile schema is flat (`key: value` lines only)")

        cut = None
        for index, char_ in enumerate(text_):
            if char_ == "#" and index > 0 and text_[index - 1] == " ":
                cut = index
                break
        value = (text_ if cut is None else text_[:cut]).rstrip(" ")
        if not value:
            return False, None
        if value[0] in _PROFILE_INDICATORS:
            refuse(lineno, f"a value starting with `{value[0]}` is a YAML "
                           "indicator; write the value quoted")
        if value in _PROFILE_RESOLVER_TOKENS or value.startswith("? "):
            refuse(lineno, f"`{value}` is a YAML indicator, not text: `=` and "
                           "`<<` are the value and merge keys and `?` opens a "
                           "complex mapping key, so a YAML reader refuses this "
                           'line rather than reading it as a string; write it '
                           f'quoted (`"{value}"`)')
        if value in _PROFILE_RESERVED_SCALARS:
            refuse(lineno, f"`{value}` reads as a YAML boolean or null, not as "
                           f'text; write it quoted (`"{value}"`)')
        if ": " in value or value.endswith(":"):
            refuse(lineno, "a plain value may not contain `: ` or end in `:`; "
                           "write it quoted")
        if '"' in value or "'" in value:
            refuse(lineno, "a plain value may not contain a quote character; "
                           "quote the whole value instead (a `'` doubles "
                           "inside single quotes: `'O''Brien Lab'`)")
        if value[0] in "0123456789-+.":
            if _PROFILE_INT_RE.match(value):
                return True, int(value)
            refuse(lineno, f"`{value}` may be read as a number, date or time; "
                           f'write it quoted (`"{value}"`)')
        return True, value

    result: dict[str, Any] = {}
    base_indent: int | None = None
    open_key: str | None = None
    item_indent: int | None = None
    seen_marker = False
    seen_content = False
    empty_mapping = False

    for lineno, line in enumerate(text.splitlines(), start=1):
        # ``strip(" ")``, never the no-argument ``strip()``: Python's default
        # strips every ``str.isspace()`` character, YAML's whitespace is only
        # SPACE and TAB, and TAB / CR / LF / C0 / C1 are already refused or
        # consumed above.  Stripping exactly one character class is what makes
        # the contract structural rather than enumerated -- any other
        # whitespace stays in the token and falls through to a refusal.
        stripped = line.strip(" ")
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))

        if stripped == "---":
            if seen_marker or seen_content:
                refuse(lineno, "a second document; a profile is one YAML "
                               "document -- delete the extra `---`")
            seen_marker = True
            continue
        if stripped == "..." or stripped.startswith("---") or stripped[0] == "%":
            refuse(lineno, "a YAML document marker or directive here is not "
                           "accepted; a profile is one plain document")
        if empty_mapping:
            refuse(lineno, "content after an empty `{}` document; write the "
                           "keys instead of `{}`")
        if stripped == "{}":
            if seen_content:
                refuse(lineno, "`{}` is accepted only as the whole document")
            empty_mapping = True
            seen_content = True
            continue

        matched = _PROFILE_KEY_RE.match(stripped)
        if matched is not None:
            if base_indent is None:
                base_indent = indent
            elif indent > base_indent:
                refuse(lineno, "a nested mapping; the profile schema is flat "
                               "-- every key sits at the same indentation")
            elif indent < base_indent:
                refuse(lineno, "this key is indented less than the first key; "
                               "every key sits at the same indentation")
            key = matched.group(1)
            if key in _PROFILE_RESERVED_SCALARS:
                refuse(lineno, f"`{key}` reads as a YAML boolean or null, not "
                               "as a key name -- PyYAML would make the mapping "
                               f"key `{key}` a non-string, so the two readers "
                               "would disagree on which key this is.  The "
                               "profile schema has no key by that name")
            if key in result:
                refuse(lineno, f"`{key}` is set twice; the later value would "
                               "silently replace the earlier one -- delete one")
            present, value = scalar(
                matched.group(2) or "", lineno, allow_empty_list=True,
            )
            result[key] = value if present else None
            open_key = None if present else key
            item_indent = None
            seen_content = True
            continue

        if stripped == "-" or stripped[:2] == "- ":
            if open_key is None:
                refuse(lineno, "a `- ` list item with no `key:` line open "
                               "above it; a profile is a mapping, so every "
                               "list belongs to a key")
            if item_indent is None:
                if base_indent is not None and indent < base_indent:
                    refuse(lineno, "a list item indented less than its key")
                item_indent = indent
            elif indent != item_indent:
                refuse(lineno, "a list item at a different indentation from "
                               "the item above it; keep every item of one "
                               "list at the same indent")
            present, value = scalar(
                stripped[1:], lineno, allow_empty_list=False,
            )
            if not present:
                refuse(lineno, "an empty list item; write a value after `- ` "
                               "or delete the line")
            if result[open_key] is None:
                result[open_key] = []
            result[open_key].append(value)
            seen_content = True
            continue

        refuse(lineno, "not a recognized profile line; write `key: value`, a "
                       "bare `key:` followed by `  - item` lines, or a "
                       "`#` comment")

    if not seen_content:
        refuse(1, "the profile has no content lines -- an empty, "
                  "whitespace-only or comment-only profile would install a "
                  "default tree silently; write the keys you mean")
    return result


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------
#
# ``RECOGNIZED_PROFILE_KEYS`` / :func:`unrecognized_profile_keys` are defined
# after ``_AXES`` (the recognized set is *derived* from the three source
# definitions, never hand-maintained); ``load_config`` resolves them at call
# time.

def load_config(config_path: Path) -> dict[str, Any]:
    """Load a profile config file, or refuse it.

    Three gates, in this order:

    1. the closed line grammar (:func:`_minimal_yaml_parse`);
    2. the reserved ``schema`` key -- read **first**, so a profile from a
       future engine refuses with *"this profile declares schema N"* rather
       than with an unknown-key list, which is the whole reason the key is
       reserved;
    3. the closed key set -- an unrecognized key refuses **before any write**,
       naming every unrecognized key and printing the recognized set.

    No third outcome: the returned mapping is equal to ``yaml.safe_load``'s, or
    a :class:`ProfileGrammarError` says which line and how to rewrite it."""
    text = config_path.read_text(encoding="utf-8")
    cfg = _minimal_yaml_parse(text, source=str(config_path))

    declared = cfg.get("schema")
    if declared is not None and declared != _ENGINE_PROFILE_SCHEMA:
        raise ProfileGrammarError(
            f"{config_path}: this profile declares schema {declared!r}; this "
            f"engine understands {_ENGINE_PROFILE_SCHEMA} -- upgrade Cairn, or "
            "remove the `schema:` line if it was set by mistake."
        )

    unrecognized = unrecognized_profile_keys(cfg)
    if unrecognized:
        raise ProfileGrammarError(
            f"{config_path}: unrecognized profile key(s): "
            f"{', '.join(unrecognized)}. The profile schema is closed -- a key "
            "outside the recognized set is refused rather than silently "
            "ignored, because a mis-typed key drops whatever it was meant to "
            f"set. Recognized keys: {', '.join(sorted(RECOGNIZED_PROFILE_KEYS))}."
        )
    return cfg


# ---------------------------------------------------------------------------
# Template installation
# ---------------------------------------------------------------------------

# Each entry is (source path relative to cairn/templates/, target path
# relative to repo root).
_CORE_MAPPINGS: tuple[tuple[str, str], ...] = (
    # repo root
    ("core/AGENTS.md",                              "AGENTS.md"),
    # Licensing notice: discharges the MIT
    # notice-retention + CC-BY attribution obligations for the whole
    # installed tree with one file. Installs unconditionally, like AGENTS.md.
    ("core/NOTICE.md",                              "NOTICE.md"),
    # Thin vendor wrapper (foldback #12): installed as VENDOR.md, a
    # vendor-neutral `@AGENTS.md` + harness-addendum template the
    # adopter renames to their tool's file (CLAUDE.md, etc.).  Core
    # ships no literal vendor name (R-G).
    ("core/VENDOR.md",                              "VENDOR.md"),
    # dev/ tree
    ("core/dev/README.md",                          "dev/README.md"),
    ("core/dev/PLANNING.md",                        "dev/PLANNING.md"),
    ("core/dev/agent_collaboration.md",             "dev/agent_collaboration.md"),
    ("core/dev/proposals/_template.md",             "dev/proposals/_template.md"),
    ("core/dev/plans/_template.md",                 "dev/plans/_template.md"),
    # Self-instrumentation home (measurement-folder standard): a core dir
    # carried by its README, which states the membership rule.  Same shape as
    # proposals/ + plans/ (a core dir installed via its content file).
    ("core/dev/measurement/README.md",              "dev/measurement/README.md"),
    # External-dependency upstream channel (core-dev-folder-set proposal):
    # draft issue reports for external OSS deps.
    # archive/.gitkeep is verbatim (an empty placeholder, not a template).
    ("core/dev/upstream/README.md",                 "dev/upstream/README.md"),
    ("core/dev/upstream/_template.md",              "dev/upstream/_template.md"),
    ("core/dev/upstream/archive/.gitkeep",          "dev/upstream/archive/.gitkeep"),
    # Project-owned agent-discipline detail folder: the folder + README
    # ship from Cairn; the rule files inside are entirely the adopter's own
    # (Cairn never templates them).  Empty at adoption by design.
    ("core/dev/rules/README.md",                    "dev/rules/README.md"),
    # Stage-0 strategy space: the README (lifecycle + status vocabulary)
    # and the note template.  Shipped default-on; the strategy/ dir and
    # archive/ placeholder are created by create_dev_tree (see install.py).
    ("core/dev/strategy/README.md",                 "dev/strategy/README.md"),
    ("core/dev/strategy/_template.md",              "dev/strategy/_template.md"),
)


#: Every file a release since v0.3.0 installed and the running tree no longer
#: ships: ``(src, dst, verbatim, digests)``.  ``src`` is the form the lockfile
#: records, ``dst`` the project path, and ``verbatim`` says whether the file was
#: copied byte for byte (a script) or rendered from a template (Markdown).  Each
#: digest is ``(sha256 of the raw template, the commit it was read at, the
#: template's git blob id)``, one per distinct version the releases carried.
#: ``upgrade --remove-retired`` may delete a project's copy only when its path
#: is on this list and its bytes match one of these digests.  A lockfile can
#: name a record but never add a row.  A file retired later needs a row here in
#: the same change that stops shipping it.
_RETIRED_INSTALLS: tuple[
    tuple[str, str, bool, tuple[tuple[str, str, str], ...]], ...
] = (
    ('modules/default-on/fold-back-ledger-template.md',
     'dev/.cairn/cairn_foldback.md',
     False,
     (
         ('4986ed7b601a47cc248c0bef680d6b8a645994a894bc6e09ebc3d4ec498575f9',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '244d1392893702f0d8cf10fc84f30c104075cf97'),
     )),
    ('core/dev/NEXT_SESSION.md',
     'dev/NEXT_SESSION.md',
     False,
     (
         ('957331ab34969855feaf6dd9d0d8c045b1f3cb6106e9ec885a1bbfee943e6bca',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '5e4066c1f2171e017dcb986d76c27401b6f2e7cb'),
     )),
    ('core/dev/collaboration_agreement.md',
     'dev/collaboration_agreement.md',
     False,
     (
         ('6dbfc2c8784e23c689b4a315bc674639e95fb2fa9fad9f211b700bfb2fd83bd2',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '5c5413bf987ad94beca8013b0a46761fc79350ff'),
         ('e389a24168232e213af0aa6d73ccfab7d00e4946f0e2aa01deebf9005a2d4d3e',
          'd3221054249026c30235c162e6048f65eb67d6bd',
          '6bf8eb13b5b45363c646ef78da8655f7822ce982'),
     )),
    ('modules/default-on/fold-back-active-prompt.md',
     'dev/modules/fold-back-active-prompt.md',
     False,
     (
         ('15675c8b693d0f3bb0a868d817cb3830876cc6213a71fabc886cc9c15d39e0f3',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '208214fbff30ab031d45cf0ec5f7576df077d548'),
     )),
    ('modules/default-on/fold-back-ledger.md',
     'dev/modules/fold-back-ledger.md',
     False,
     (
         ('1c8b1507fcc116de48b15d90b806b162fdd07dd41f7afe476bec5bbe437dc82c',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          'f835bc17e450daefba110fde1c6d28aadaa1bac5'),
     )),
    ('modules/default-on/foldback_export_scan.md',
     'dev/modules/foldback_export_scan.md',
     False,
     (
         ('e43e022eb9fbac5e0bb34bfd0536bfb36d1de08fd7870f23f87c3d0b451f9306',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '66b3f8f761c67f63b1339e36faefc6e647ea5b4a'),
     )),
    ('modules/default-on/lifecycle-metrics.md',
     'dev/modules/lifecycle-metrics.md',
     False,
     (
         ('37640b2022388b1115cbcca2a392672cd3f67f08e906b374a8f1c424092c57d0',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '03b16b695b3b760733271625c79ece27d7f9297e'),
         ('e225ea8bc3ce5446d28076ba6e900d3afc4b250975d02fc44349da02050a0a83',
          'e0b83b939355eb96b574d4ecf841529ecad8349e',
          'b75782cc4a92992dab3dac389a3aef115193b6cc'),
     )),
    ('modules/default-on/_onboarding/__init__.py',
     'scripts/_onboarding/__init__.py',
     True,
     (
         ('96ffbb4bb647cf964397e0a12b365300b150448c876bdc784622757a6d406d4f',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          'f09ab5ce909be90bfc0c7d15113ccc4a4017c401'),
         ('a870a4eb190548f450d8741310e09f57a91cdd81c75a8fcec02ceff115815adf',
          '012d5d9e1963a90889817685affd9774846f232c',
          '1da0df194e7fc5a8eef78d721cb1d4422b96aec9'),
     )),
    ('modules/default-on/_onboarding/activation.py',
     'scripts/_onboarding/activation.py',
     True,
     (
         ('c0c4678fdd6df56bc3c3d0568796ad2c115b8d8999cddb5625ec42c2eaf71d5d',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '59a39eef36dc3e91853251decd0cc14b3654c573'),
         ('dd62576cddf1afd72f823a8f13b118bd2b3d332b296d479334b7259ca87a305f',
          '012d5d9e1963a90889817685affd9774846f232c',
          'be07f90ac8787aeddd29024863d60c83b068a26a'),
     )),
    ('modules/default-on/_onboarding/cli.py',
     'scripts/_onboarding/cli.py',
     True,
     (
         ('cc5e399fbc7c1a5212a0af32481d5df559a43555356f7d901a4ccadcb768ca22',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '378697c2a2d30a42328b436607ce0920b56535ef'),
         ('470e7ff510bc9ce0ece1ecac26e08c3fb554db2560e7778b8598996f4f8f2d83',
          '012d5d9e1963a90889817685affd9774846f232c',
          '9afa5558988132dfb003c8063210fe0f0d7c0a47'),
     )),
    ('modules/default-on/_onboarding/prompts.py',
     'scripts/_onboarding/prompts.py',
     True,
     (
         ('d0b184798376b1c0547fb31716ad307aca3ac826a0ca2833af908912ed4a413b',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '73896cd1b34f55f933096a686a0f617224755d51'),
         ('790121fb3376cde651a7a662bb85800d3e01ef049c4e847fd1e38100a42504e3',
          '012d5d9e1963a90889817685affd9774846f232c',
          '7c3068d5dfcc3be717257238b96bcbfc688206cf'),
     )),
    ('modules/default-on/_onboarding/security.py',
     'scripts/_onboarding/security.py',
     True,
     (
         ('719598ff530db4ef235c7ddb68bc4aa0ff27ae9f593b2b67d2823df489501513',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '926dcc31153a985f169522e892afd42de3d47c11'),
         ('18680b45be60dfd7b4d2a364c0e192e5fb551e2eb45305d869172b2b276c794c',
          '012d5d9e1963a90889817685affd9774846f232c',
          '1ae0cf21a2eac952ec6ffa905fb96025d2aaf9cc'),
     )),
    ('modules/default-on/_onboarding/shared.py',
     'scripts/_onboarding/shared.py',
     True,
     (
         ('2df82aebc4889f7ac56086676d1937e7be38fff2c4cd556a07314eee33c3d1e2',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '01ba48cd3f2928babbc62ac090a09fb951935720'),
         ('8bc99ba39dfb4f0e4195cf6a9619dd8fd7eaafce33209cd81d776c1debcadee7',
          '012d5d9e1963a90889817685affd9774846f232c',
          'e362a8d115c50bffaeb7d62c575f026c887e7322'),
     )),
    ('modules/default-on/_onboarding/slotparse.py',
     'scripts/_onboarding/slotparse.py',
     True,
     (
         ('86dd6fea6d91e4c13c92a0a349f914890b33eb89b9ba2f002821792af9902437',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '0d19853baa3c19abc39e4ec7db04f7b005dbd7b7'),
         ('dbaa39faec64f3308d701de67ee67d697cf9d8d2424c7422f8b4775c1b88195f',
          '012d5d9e1963a90889817685affd9774846f232c',
          '01c36308ff871318791be9368fe4c03d891fe542'),
     )),
    ('modules/default-on/_onboarding/triggers.py',
     'scripts/_onboarding/triggers.py',
     True,
     (
         ('e7981225094ee2535ca15e1d30ff32c7934fa5bcb65405b6d5a031e6d1a79749',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '40b9094f4197ae77cdb3a526e1323fa97520cafe'),
         ('8a44af06c9345392001932758020747f43cff92eb5de2b9da862663e0756a707',
          '012d5d9e1963a90889817685affd9774846f232c',
          '2cca53e93157e7587ef8dc7a4452869b21e7be80'),
     )),
    ('modules/default-on/foldback_export_scan.py',
     'scripts/foldback_export_scan.py',
     True,
     (
         ('d241fb5c9c7733de355cf21b4608fbc5f9de69fe07a001af71b36fd6899adbb3',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '00d82465b5fe6f7118e58cfafa670579c536930e'),
         ('50335194f0f5556558d2e2f0dfe24d20f3a067f2ed63e6a364b2f4c200918e87',
          'f9f2483223dbefb29b32696b4795f159df557ead',
          '6e5a385f7e78aed744c52b0e14e8f4134798b2d4'),
     )),
    ('modules/default-on/foldback_suggest.py',
     'scripts/foldback_suggest.py',
     True,
     (
         ('b5f75d55813ff9a328a26594a6deac9119fa95d80b877d86de351e7df026ad1c',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '2295921aa5b8f970e8310e8e8863cd1d16d14f48'),
         ('675fc88f2e3ef421b56a2a761149c673ae3f6d64651a58ce5a0937b706cc3485',
          'f9f2483223dbefb29b32696b4795f159df557ead',
          '868e976a6a4c56a7f5beb708c0b0b0d8fd6b8d34'),
     )),
    ('modules/default-on/onboarding_activate.py',
     'scripts/onboarding_activate.py',
     True,
     (
         ('113cb1de3d738716ad1d758798ff2fd0485e71b036f5fe76945fd1b222e66e28',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          'b76e59bd8b1a972447a976ce959cc615bf888b41'),
         ('41d524aa54ae713bb95409504ca731aad858394e2d269124cddd98ee197c6f9b',
          '012d5d9e1963a90889817685affd9774846f232c',
          'f0a180787ba3d46e5f45ee922256ead5500b698c'),
     )),
    ('modules/default-on/_lifecycle_metrics/__init__.py',
     'tools/_lifecycle_metrics/__init__.py',
     True,
     (
         ('fb1c4d2657ba100fefd8aeb8d2834240c1dee422ec3e0da80b559e6d246af6cd',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '18d7ce1261db0054f7b3d03839dfd1bc8fcd5d4d'),
         ('2d6a73f37bf1d8dfab3743320872cd0163069bea8b9a43f1a08011e231264904',
          'e0b83b939355eb96b574d4ecf841529ecad8349e',
          '37f882452a985c59baa9fe72e2418a4385bb2451'),
     )),
    ('modules/default-on/_lifecycle_metrics/cli.py',
     'tools/_lifecycle_metrics/cli.py',
     True,
     (
         ('be790d5af8db385e9981656f8c1a0bd89efcdee5e7687c97256f7ee833327d73',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          'e57d51da62f4b7311c509546129fd16a40395a48'),
         ('883c2f21eddb809a69fcb41845ed6ff594b38cfdc02b8457a4e9f18c1c23e5c5',
          'e0b83b939355eb96b574d4ecf841529ecad8349e',
          'c79d7c6307a8ab66e2a4daa8904bf6ee718e220f'),
     )),
    ('modules/default-on/_lifecycle_metrics/config.py',
     'tools/_lifecycle_metrics/config.py',
     True,
     (
         ('80110f142ec5ec2f28889db25112839daf61fe1f5c9caec82ac337f7731e445a',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          'aefe4082cb62b0e094c79f7e7c3480e839a4fe8f'),
         ('2a833d5915ae76eb555ff83f6e1ecd674ec529ac7fc0c37da6aa49854b3c5641',
          'e0b83b939355eb96b574d4ecf841529ecad8349e',
          '642d64b00f17bf6028ae9c81452a3be76781c626'),
     )),
    ('modules/default-on/_lifecycle_metrics/extract.py',
     'tools/_lifecycle_metrics/extract.py',
     True,
     (
         ('ce5f7558c91c07f7c991aeba17274a7e345369f8c96a92565c4d08082a7f8476',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '0ba128016f0072e74603a7083b1f6e96f9dc850a'),
         ('255f01d38914aa99f7d2699649ddd684269cf60b99a9ce63c0b447a64c7a4993',
          'e0b83b939355eb96b574d4ecf841529ecad8349e',
          'cad065383193b03c73f1db09427fe7c3978cf007'),
     )),
    ('modules/default-on/_lifecycle_metrics/gitmeta.py',
     'tools/_lifecycle_metrics/gitmeta.py',
     True,
     (
         ('3d057d535389c44dc870f5f6ca5d4ebd481c8307cd5abc96dbac4c66875389e8',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '9b2c3ee146705f25aa5cfec5185528827991c30b'),
         ('dbb2d2506e6969a8970bc515739645cac62c99b9468b83a3549093541f308d5b',
          'e0b83b939355eb96b574d4ecf841529ecad8349e',
          '9f053836f43d2bd857365079612f88c595bd40c6'),
     )),
    ('modules/default-on/_lifecycle_metrics/parse.py',
     'tools/_lifecycle_metrics/parse.py',
     True,
     (
         ('d7c973e159acddfbae2825b3af6656519a884b7b5c7e5dc54838a4bd67bb1f04',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          'abdfd4d42c97536538f54af63a993ecbd77c163a'),
         ('161841e4a10a5896b28f0296f5009d69ebd690316eb8934e320881b5779dc141',
          'e0b83b939355eb96b574d4ecf841529ecad8349e',
          'f67df562d9e4544b0d9c2f9501bb312df52db545'),
     )),
    ('modules/default-on/_lifecycle_metrics/report.py',
     'tools/_lifecycle_metrics/report.py',
     True,
     (
         ('130217374d387438961cbbd0d8c44123831d8952fb5583029c7b81a85db0eca9',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '2f8cb213909f5a8f19e2188406569356839e433d'),
         ('44097a463944a794e6c7e9e21e0c1e87d955741c3f817814e07889d82fd8c07f',
          'e0b83b939355eb96b574d4ecf841529ecad8349e',
          '2ebc1270352639d36f6200656aebf242fa86d4c9'),
     )),
    ('modules/default-on/_lifecycle_metrics/snapshot.py',
     'tools/_lifecycle_metrics/snapshot.py',
     True,
     (
         ('3637757f5729e29bb07601eeb8ba8e5444d38775c4d6fb75337d234eb4387da8',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '41ed2c054e055ac466a6cf08a2f37ae3beafe53d'),
         ('5bdfbce95911b66987d042ab5e71b82c5ca69e81723f4e1c6435a677e82c6f51',
          'e0b83b939355eb96b574d4ecf841529ecad8349e',
          '54a8152ada602e4419da7479fe2772682636d96a'),
     )),
    ('modules/default-on/_lifecycle_metrics/subsystems.py',
     'tools/_lifecycle_metrics/subsystems.py',
     True,
     (
         ('a0489d7ab5b396156afdfd6d2b11887afd054b0fc4e9e606ba0473cf65355af3',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '62ee8860920a8b97c7b72a911749a5bcdce4fafe'),
         ('76d2b4f0b7377ba7eeabcf7ff342b4fc4b4a8ecfd1d6c202b25698e7674c98ab',
          'e0b83b939355eb96b574d4ecf841529ecad8349e',
          '50f783e904b1596af743c943b2d373042620df1e'),
     )),
    ('skills/_lib/lifecycle.py',
     'tools/lifecycle.py',
     True,
     (
         ('296ef88bda1e3e817734cc6cdb14e9571cd3a0ee0aada8d07dfa9e1f898839c9',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          'bf36967d95ecc3867a4eeaa8e1ed3f733818db13'),
         ('8d926f6764fb17dcf45c1bcc52faab8509e37dddc869ea16c3e498abdba861ee',
          '6558f3ff6d4888b397d0e7c8fbfa8b86d0b3c381',
          '504523c3a3ccce68ce26a5bcecaf49166fa68a5b'),
     )),
    ('modules/default-on/lifecycle_metrics.py',
     'tools/lifecycle_metrics.py',
     True,
     (
         ('01a323268b787a0579177a0cbb5b29c4d08456af7a4d68574854780d25ed05a0',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '4cca4d2dbb2c6df9ca789b7b9b772cc709a5bd0a'),
         ('86a64b0a9163ff65f56accad733a855c8db8c8c8a99c2a340542abdaf533ff18',
          'e0b83b939355eb96b574d4ecf841529ecad8349e',
          '250f08780120a73d3ec6028a34befe960736cc43'),
     )),
    ('skills/_lib/lifecycle_planner.py',
     'tools/lifecycle_planner.py',
     True,
     (
         ('2b30639e4bf7c97037d2ba851d2487003f62f31824a98894c9fe0ca5b8c17263',
          '12ec2ad28f22a7d3d9c19ce67e78d86cc625757a',
          '2f8e706801ae0bdb803d26714f5d74f584831cc4'),
         ('7d35f2e33e131d166fd34ce00d284e23608ed28b7d9925735aec870c3f2c6296',
          '6558f3ff6d4888b397d0e7c8fbfa8b86d0b3c381',
          '2dea13f37a9e46f4c35e6312fe3b1a9289ffbdfd'),
     )),
)

#: Lifecycle-routine skills install **unconditionally, like core/** -- the
#: session routines are invariant kernel (every adoption runs them), so they
#: are not a conditional ``templates/modules/*`` module.  ``(src relative to
#: templates/, dst relative to the repo root, verbatim)``.  The CLI is a script
#: -> ``verbatim`` (byte-for-byte, hash-only upgrade policy); the ``SKILL.md``
#: sources are markdown -> substituted (so they get a base-template cache entry
#: and a token-/slot-aware 3-way merge on upgrade, exactly like ``core/`` docs).
_SKILLS_MAPPINGS: tuple[tuple[str, str, bool], ...] = (
    ("skills/_lib/session.py",           "tools/session.py",                         True),
    ("skills/_lib/board.py",             "tools/board.py",                           True),
    ("skills/_data/vendor_targets.yml",  ".agents/skills/_data/vendor_targets.yml",  True),
    ("skills/session-start/SKILL.md",   ".agents/skills/session-start/SKILL.md",    False),
    ("skills/session-end/SKILL.md",     ".agents/skills/session-end/SKILL.md",      False),
)

#: Machine-local lifecycle state the skills write into ``dev/.cairn/`` -- the
#: untracked interpreter binding (resolve-don't-bake, Decision 6) and the
#: full-handoff lock.  Seeded into ``.gitignore`` unconditionally (the skills
#: always install).  ``dev/.cairn/base/`` itself stays tracked (the lockfile
#: base cache); only these machine-state members are ignored.
_SKILLS_GITIGNORE: tuple[str, ...] = (
    "dev/.cairn/local-env.json",
    "dev/.cairn/handoff.lock",
)

#: Common filenames an adopter renames the thin vendor wrapper
#: (``core/VENDOR.md``) to -- their AI tool's instruction file.  Used by
#: ``--init-lock`` to follow that rename so the wrapper stays tracked + 3-way
#: merges on later upgrades (foldback #45).  Distinctly vendor-specific names
#: only (``AGENTS.md`` is the shared file, deliberately excluded).
_KNOWN_VENDOR_WRAPPERS: tuple[str, ...] = (
    "CLAUDE.md", "GEMINI.md", "CODEX.md", "CURSOR.md", "COPILOT.md", "QWEN.md",
)

# Optional top-level templates, gated on a dimension axis.  Unlike
# modules (which land under ``dev/modules/``), these are project-root
# files an adopter's *human* contributors read.  Each entry is
# ``(src rel to templates/, dst rel to repo root, gate axis, selecting
# values)``: the template installs when the *resolved* profile value for
# that axis is in the selecting set.  An installed optional template is
# recorded under ``optional_templates:`` in the fidelity manifest so the
# gate is auditable (bootstrap/fidelity-check.md).
_OPTIONAL_TEMPLATES: tuple[tuple[str, str, str, frozenset[str]], ...] = (
    # CONTRIBUTING.md — the human-contributor entry (foldback #10),
    # installed when the repo expects human authors beyond a solo
    # maintainer: the human-team axis at small-multi or large-multi.
    (
        "optional/CONTRIBUTING.md",
        "CONTRIBUTING.md",
        "human_team",
        frozenset({"small-multi", "large-multi"}),
    ),
)


def select_optional_templates(axes: dict[str, object]) -> list[tuple[str, str]]:
    """Return ``(src, dst)`` for each optional template whose dimension
    gate the profile satisfies.

    *axes* is the **resolved** dimension profile — a preset's canonical
    point merged with the adopter's overrides (``resolve_axes``), or the
    raw profile when no ``preset:`` is used.  A profile that omits the
    gate axis, or sets it to a non-selecting value, gets no optional
    template — the conservative default.
    """
    selected: list[tuple[str, str]] = []
    for src, dst, axis, values in _OPTIONAL_TEMPLATES:
        if str(axes.get(axis, "")) in values:
            selected.append((src, dst))
    return selected


class InstallSpec(NamedTuple):
    """One file a module installs.

    ``src`` is relative to ``cairn/templates/modules/``; ``dst`` is
    relative to the target repo root.  ``verbatim`` marks an executable
    script (or any non-template asset) that is copied **byte-for-byte**:
    no ``{{token}}`` substitution runs over it, and it is not scanned for
    unfilled tokens / block slots (a code file's f-string braces or
    docstring would otherwise false-positive the post-scaffold report).
    """

    src: str
    dst: str
    verbatim: bool = False


def duplicate_destinations(
    entries: list[tuple[str, str]],
) -> dict[str, list[str]]:
    """Map each destination claimed by **more than one** owner to its owner
    labels; empty dict means every destination is uniquely owned.

    The shared destination-ownership preflight: a
    duplicate destination means one ``InstallSpec`` silently shadows another on a
    ``--force`` install, or the published manifest emits two rows for one path.
    Each entry is ``(owner_label, dst)``.  Pure leaf logic; the callers choose the
    failure (the upgrade planner fails closed before any write;
    ``install_manifest`` refuses)."""
    owners: dict[str, list[str]] = {}
    for label, dst in entries:
        owners.setdefault(dst, []).append(label)
    return {dst: who for dst, who in owners.items() if len(who) > 1}


# Module name → list of InstallSpec (1:many).  Most modules install a
# single substituted ``.md`` doctrine file; the two default-on
# discipline modules also install their reference *script* verbatim
# The script ``dst`` paths are the single source of
# truth for the command-token defaults below (see
# ``_REFERENCE_SCRIPT_TOKEN`` and ``reference_script_token_defaults``)
# so the doc's "run it via {{...}}" line and the install destination
# cannot desync.
_MODULE_MAPPINGS: dict[str, list[InstallSpec]] = {
    "reflections": [
        InstallSpec("default-on/reflections.md", "dev/modules/reflections.md"),
        # A tracked directory guide so dev/reflections/ materializes on a
        # fresh scaffold (the reflection entries themselves stay untracked
        # via the .gitignore seed below) -- fold-back #42.
        InstallSpec("default-on/reflections-README.md",
                    "dev/reflections/README.md", verbatim=True),
        # Fold 2 (foldback-drain-tooling): explicit prune tool the reflections
        # module doctrine prescribes.  Complements the simpler date-cutoff prune
        # inside tools/session.py session-end (which runs at full-handoff);
        # this standalone script allows independent invocation and offers a
        # keep-by-distinct-date window rather than a wall-clock cutoff.
        InstallSpec("default-on/prune_reflections.py",
                    "tools/prune_reflections.py", verbatim=True),
    ],
    "claim-check": [
        InstallSpec("default-on/claim-check.md",
                    "dev/modules/claim-check.md"),
        InstallSpec("default-on/claim_check.py",
                    "scripts/claim_check.py", verbatim=True),
        # Fold 1 (foldback-drain-tooling): stem-resolution checker.
        # Complements claim_check.py (repo-path/line-bounds) and link_check.py
        # (markdown links) -- verifies that every backticked date-prefixed stem
        # in PLANNING.md (and any other file a project scans) resolves to one
        # proposal or plan.
        # Default-on with the claim-check module family because both are
        # lifecycle-hygiene checkers.
        InstallSpec("default-on/verify_stems.py",
                    "scripts/verify_stems.py", verbatim=True),
    ],
    # The deployment-side measurement substrate the adaptive-doctrine
    # rate-limit gate (doctrine/rationale.md) evaluates against.
    # Ships the module doctrine + a forkable tracker template; adopters
    # fork the template to one or many live trackers (e.g.,
    # dev/incident_log.md or class-specific files), then the goodnight
    # migration sub-step feeds incident entries from reflections into
    # the trackers.  The canonical 7-column semantic-field schema is
    # the contract the eventual Goal 7 cross-adopter harvest reads.
    "incident-trackers": [
        InstallSpec("default-on/incident-trackers.md",
                    "dev/modules/incident-trackers.md"),
        InstallSpec("default-on/incident_log_template.md",
                    "dev/modules/incident_log_template.md"),
        # The deterministic, zero-token rate-limit-gate evaluator +
        # fold-up-backlog checker (self-evolution-loop Part B). Reads the
        # incident trackers and emits rate-limit suggestions only.
        InstallSpec("default-on/evolution_infer.py",
                    "tools/evolution_infer.py", verbatim=True),
    ],
    # The placement-decision procedure for documentation and doctrine.
    # Default-on: every adopter benefits from a four-layer routing
    # discipline (entry / governing / deliberation / descriptive).
    # Ships the module doctrine + a forkable DOCUMENTATION_PLAN.md the
    # adopter customizes for their own file inventory + tier vocabulary.
    # Three slot anchors land via the core templates --
    # `documentation-discipline` in AGENTS.md plus
    # `documentation-tier-home` in proposals + plans `_template.md` --
    # and are filled by **manual paste** from the module's
    # `Merged into:` Blocks 1/2/3 (the adopter copies the block matching
    # each target slot at install time, parallel to the existing
    # claim-check / lifecycle-metrics / reflections module pattern).
    # Mechanical merge via Proposal B's `cairn:merge-target` directives
    # is *deferred* pending the merge-pass / install-lockfile interaction
    # fix (the merge pass mutates files post-install, which the
    # lockfile's clean-install divergence guard rejects); see
    # `dev/PLANNING.md` (modflow_tools-side) > "Cairn-side merge-helper
    # / install-lockfile interaction fix".  The forkable's worked
    # examples are adopter-relative; Cairn's own self-hosted instance at
    # cairn/docs/DOCUMENTATION_PLAN.md uses cairn-prefixed paths and is
    # the methodology source-of-truth.
    "documentation-plan": [
        InstallSpec("default-on/documentation-plan.md",
                    "dev/modules/documentation-plan.md"),
        InstallSpec("default-on/documentation_plan_template.md",
                    "docs/DOCUMENTATION_PLAN.md"),
    ],
    # team-gated
    "dual-review": [
        InstallSpec("team-gated/dual-review.md", "dev/modules/dual-review.md"),
    ],
    "domain-agents": [
        InstallSpec("team-gated/domain-agents.md",
                    "dev/modules/domain-agents.md"),
    ],
    "legacy-agent": [
        InstallSpec("team-gated/legacy-agent.md",
                    "dev/modules/legacy-agent.md"),
    ],
    "dual-language-tests": [
        InstallSpec("team-gated/dual-language-tests.md",
                    "dev/modules/dual-language-tests.md"),
    ],
    "coordination-tiers": [
        InstallSpec("team-gated/coordination-tiers.md",
                    "dev/modules/coordination-tiers.md"),
        # The work-intent tool ships verbatim alongside the
        # doctrine (1:many, the claim-check / lifecycle-metrics pattern).
        InstallSpec("team-gated/intent.py",
                    "tools/intent.py", verbatim=True),
        # intent-split (phase A, 2026-06): intent.py is now a thin launcher/facade
        # over an owned `_intent/` engine package; the seven package files install
        # verbatim beside the facade so `python tools/intent.py` (the CLI + the git
        # hooks) resolves its sibling engine at runtime.  Each is byte-for-byte code.
        InstallSpec("team-gated/_intent/__init__.py",
                    "tools/_intent/__init__.py", verbatim=True),
        InstallSpec("team-gated/_intent/shared.py",
                    "tools/_intent/shared.py", verbatim=True),
        InstallSpec("team-gated/_intent/record_io.py",
                    "tools/_intent/record_io.py", verbatim=True),
        InstallSpec("team-gated/_intent/identity.py",
                    "tools/_intent/identity.py", verbatim=True),
        InstallSpec("team-gated/_intent/conflict.py",
                    "tools/_intent/conflict.py", verbatim=True),
        InstallSpec("team-gated/_intent/hooks.py",
                    "tools/_intent/hooks.py", verbatim=True),
        InstallSpec("team-gated/_intent/cli.py",
                    "tools/_intent/cli.py", verbatim=True),
        # Fold 2 (foldback-drain-tooling): the prune-intents goodnight compaction
        # tool.  Ships with coordination-tiers because the goodnight intent-hygiene
        # extension (coordination-tiers module doc) prescribes the prune-intents step.
        # Self-contained (no import from tools.intent); reads dev/intents.jsonl directly.
        InstallSpec("team-gated/prune_intents.py",
                    "tools/prune_intents.py", verbatim=True),
    ],
    "security-review": [
        InstallSpec("team-gated/security-review.md",
                    "dev/modules/security-review.md"),
    ],
    "issue-capture": [
        InstallSpec("team-gated/issue-capture.md",
                    "dev/modules/issue-capture.md"),
        # Fold 3 (foldback-drain-tooling): label-bootstrap helpers, one per
        # forge (GitLab + GitHub).  Generalise the per-adopter scripts into a
        # single Cairn-generic tool shipped with the module that prescribes
        # label-axis doctrine.  The additive-only flag absorbs the LHM
        # divergence (legacy-label note); no project-specific references.
        # Both scripts emit a clear "set GITLAB_PRIVATE_TOKEN /
        # GITHUB_TOKEN" error when no credential is found.
        InstallSpec(
            "team-gated/issue-capture/bootstrap_gitlab_labels.py",
            "scripts/bootstrap_gitlab_labels.py",
            verbatim=True,
        ),
        InstallSpec(
            "team-gated/issue-capture/bootstrap_github_labels.py",
            "scripts/bootstrap_github_labels.py",
            verbatim=True,
        ),
    ],
    "model-selection": [
        InstallSpec("team-gated/model-selection.md",
                    "dev/modules/model-selection.md"),
        # Fold 5 (foldback-drain-tooling): stub mapping file + fidelity checker.
        # The stub is seeded carrying a "FILL ME" placeholder, so the gate is
        # **red on a fresh, unfilled mapping** -- forcing the adopter to record
        # their real tier->model assignments (the silent-empty install is the
        # failure this module prevents; the install itself is never blocked).
        # An *interactive* install captures the bindings up front so the gate
        # ships green (foldback #2: capture_model_selection_mapping); a
        # non-interactive / CI install leaves the FILL ME stub as the fallback.
        # The checker is installed verbatim so adopters can invoke it directly
        # (`python scripts/check_model_selection.py`) or wire it into their CI.
        InstallSpec(
            "team-gated/model_selection_mapping_stub.yml",
            "dev/.cairn/model-selection-mapping.yml",
        ),
        InstallSpec(
            "team-gated/check_model_selection.py",
            "scripts/check_model_selection.py",
            verbatim=True,
        ),
    ],
    # Practice-discipline modules.  Team-gated -- a
    # governance preset turns them on per profile rather than
    # doubling the default-on auto-install set.  Doctrine-only (single
    # substituted .md each; no scripts).
    "testing-discipline": [
        InstallSpec("team-gated/testing-discipline.md",
                    "dev/modules/testing-discipline.md"),
    ],
    "doc-drift-prevention": [
        InstallSpec("team-gated/doc-drift-prevention.md",
                    "dev/modules/doc-drift-prevention.md"),
        # Cairn v0.2 foldback: the module flips from doctrine-only to
        # doctrine + stack-neutral runnable tooling (1:many, the
        # claim-check pattern).  Two verbatim stdlib-only scripts -- the
        # link half and the snippet-sync.  The claim half is NOT shipped
        # here: the default-on claim-check module already installs
        # scripts/claim_check.py, so the doc-drift gate composes with it
        # rather than duplicating a second checker.  The schema-doc
        # generator is deferred (an adopter slot/hook) -- it cannot ship
        # stack-neutrally.
        InstallSpec("team-gated/link_check.py",
                    "scripts/link_check.py", verbatim=True),
        InstallSpec("team-gated/sync_doc_snippets.py",
                    "scripts/sync_doc_snippets.py", verbatim=True),
    ],
    "examples-gallery": [
        InstallSpec("team-gated/examples-gallery.md",
                    "dev/modules/examples-gallery.md"),
    ],
    # Security hardening: the content-integrity scanner,
    # shipped to adopters so their agents can scan working-tree files /
    # incoming PRs for prompt-injection patterns before ingesting them. The
    # verbatim script is single-sourced here (Cairn's own check_cairn composes
    # the same file), the 1:many claim-check pattern.
    "content-security": [
        InstallSpec("team-gated/content-security.md",
                    "dev/modules/content-security.md"),
        InstallSpec("team-gated/content_scan.py",
                    "scripts/content_scan.py", verbatim=True),
        # Security-apparatus-enrichment Chunk B: the decomposed stdlib-only
        # advisory runner + its policy inputs (audited-roots manifest,
        # reviewed-residual baseline, URL allowlist).  All verbatim -- code +
        # policy data, not token-substituted templates.  The runner resolves
        # its policy siblings from its own scripts/ directory.
        InstallSpec("team-gated/content_scan_runner.py",
                    "scripts/content_scan_runner.py", verbatim=True),
        InstallSpec("team-gated/content_scan_roots.txt",
                    "scripts/content_scan_roots.txt", verbatim=True),
        InstallSpec("team-gated/content_scan_residuals.txt",
                    "scripts/content_scan_residuals.txt", verbatim=True),
        InstallSpec("team-gated/content_scan_allowlist.txt",
                    "scripts/content_scan_allowlist.txt", verbatim=True),
    ],
    # The Python security gate stack (
    # surface 3).  Team-gated + opt-in -- never default-on, and never
    # installed for a non-Python adopter.  v1 self-audit scope only (a
    # drift / content-injection tripwire on the adopter's *own trusted
    # tree*), explicitly NOT a reviewer for untrusted PRs that can modify
    # the apparatus itself.  This lands the module doctrine stub + its
    # required-token registration (``python_package``, below); Chunk C adds
    # the orchestrator (``run_security_audit.py``), the templated bandit
    # gate, and the adopted-executable source gate.  ``python_package`` has
    # no safe default, so it is a required token (the selected-module
    # required-token preflight refuses a fresh install / adopt / upgrade
    # that selects this module without a filled value -- fail closed before
    # any write).
    "python-security": [
        InstallSpec("team-gated/python-security.md",
                    "dev/modules/python-security.md"),
        # The standalone orchestrator (Chunk C): SR-1 integrity preflight +
        # content-scan (when content-security installed) + bandit over
        # {{python_package}} + the adopted-executable source gate + pip-audit
        # (egress opt-in).  Verbatim -- code, no token substitution; it reads
        # python_package + the installed roster from the lockfile at runtime.
        InstallSpec("team-gated/run_security_audit.py",
                    "scripts/run_security_audit.py", verbatim=True),
    ],
    # Portable offline security sweeps (portable-security-sweeps, 2026-08-05):
    # a team-gated, opt-in cross-language secret-exposure tripwire.  The module
    # **installs no scanner**: it ships a stdlib orchestrator + a strict JSON
    # policy and drives one host adapter (Gitleaks, offline, no network flag)
    # over two scan questions.  The scaffold executes no scanner during
    # installation -- that would move an executable trust root into the
    # installer.
    #
    # The three specs are **registered as one group and pinned as one group by
    # bootstrap/tests/test_portable_security_sweeps.py**.  The engine performs
    # no group-completeness refusal for _MODULE_MAPPINGS, so the pin is
    # test-side and the comment must not imply otherwise.
    #
    # The module declares **no required token** -- unlike the "python-security"
    # key one entry above, whose gate needs {{python_package}}.  Its doctrine
    # is substituted; the runner and the policy are verbatim assets (the policy
    # is the first .json Cairn ships under templates/).
    "portable-security-sweeps": [
        InstallSpec("team-gated/portable-security-sweeps.md",
                    "dev/modules/portable-security-sweeps.md"),
        InstallSpec("team-gated/run_portable_security_sweeps.py",
                    "scripts/run_portable_security_sweeps.py", verbatim=True),
        InstallSpec("team-gated/portable_security_policy.json",
                    "scripts/portable_security_policy.json", verbatim=True),
    ],
    # api-web-security-modules (2026-08-10): two narrow, independently
    # selectable network-security capabilities.  Team-gated and reachable only
    # through an explicit modules_add or an exact modules: list -- deliberately
    # absent from _PRESETS and _DEFAULT_ON_MODULES, because applicability is
    # not derivable from Cairn's six axes (a project either has a
    # cross-principal API / a hosted site or it does not).
    #
    # **One engine source tree, installed twice.**  The four
    # `team-gated/_security_net/*` members are listed in BOTH groups with
    # DIFFERENT destinations -- `scripts/_api_access_security/` and
    # `scripts/_web_hosting_security/`.  install_manifest refuses duplicate
    # *destinations* and only destinations, so one source feeding two
    # destinations is accepted; two sources feeding one destination is not.
    # The cost is that an adopter selecting both carries two byte-identical
    # copies, each independently hash-pinned; the alternative was two
    # hand-written TLS clients, and one security surface reviewed once is worth
    # more than a duplicated byte saved.  `scripts/<name>.py` +
    # `scripts/_<name>/` is also the facade-engine convention
    # `_facade_engine_dir` already recognises, so a forked facade gets the
    # existing advisory.
    #
    # Each group is COMPLETE by construction -- doctrine, facade, four engine
    # members, policy stub -- because install_modules warns and continues on a
    # missing source, so a partial group would install silently.  That fail-open
    # is closed from two ends that need no engine change: a Cairn-side test that
    # every src here exists under templates/, and the shipped runner's own
    # import self-check, which exits 20 / DEGRADED before any policy read.
    #
    # The policy stubs are substituted (adopter-filled configuration); the
    # facades and engine members are verbatim executables.
    "api-access-security": [
        InstallSpec("team-gated/api-access-security.md",
                    "dev/modules/api-access-security.md"),
        InstallSpec("team-gated/api_access_security.py",
                    "scripts/api_access_security.py", verbatim=True),
        InstallSpec("team-gated/_security_net/__init__.py",
                    "scripts/_api_access_security/__init__.py", verbatim=True),
        InstallSpec("team-gated/_security_net/policy.py",
                    "scripts/_api_access_security/policy.py", verbatim=True),
        InstallSpec("team-gated/_security_net/net.py",
                    "scripts/_api_access_security/net.py", verbatim=True),
        InstallSpec("team-gated/_security_net/report.py",
                    "scripts/_api_access_security/report.py", verbatim=True),
        InstallSpec("team-gated/api_access_policy_stub.json",
                    "dev/.cairn/api-access-policy.json"),
    ],
    "web-hosting-security": [
        InstallSpec("team-gated/web-hosting-security.md",
                    "dev/modules/web-hosting-security.md"),
        InstallSpec("team-gated/web_hosting_security.py",
                    "scripts/web_hosting_security.py", verbatim=True),
        InstallSpec("team-gated/_security_net/__init__.py",
                    "scripts/_web_hosting_security/__init__.py", verbatim=True),
        InstallSpec("team-gated/_security_net/policy.py",
                    "scripts/_web_hosting_security/policy.py", verbatim=True),
        InstallSpec("team-gated/_security_net/net.py",
                    "scripts/_web_hosting_security/net.py", verbatim=True),
        InstallSpec("team-gated/_security_net/report.py",
                    "scripts/_web_hosting_security/report.py", verbatim=True),
        InstallSpec("team-gated/web_hosting_policy_stub.json",
                    "dev/.cairn/web-hosting-policy.json"),
    ],
    # Architecture-review (modflow_tools doctrine-parity fold, 2026-06-01):
    # a triggered remediation / on-ramp module for an adopter whose
    # architecture accreted rather than was deliberately designed.  Ships
    # the module doctrine + a forkable rubric frame the adopter fills
    # (the incident-trackers / documentation-plan 2-spec pattern, both
    # substituted not verbatim).  Team-gated, opt-in -- not in any
    # default-on set or governance preset.
    "architecture-review": [
        InstallSpec("team-gated/architecture-review.md",
                    "dev/modules/architecture-review.md"),
        InstallSpec("team-gated/architecture_review_template.md",
                    "dev/architecture_review.md"),
    ],
    # security-verification-activation Chunk A: the default-on local
    # security-verification dispatcher.  Registered here (opt-in, via this
    # mapping only) BEFORE it becomes universal -- Chunk B appends the module
    # name to _DEFAULT_ON_MODULES separately, so every property is pinned
    # while the module is still selectable-not-automatic.  The shipped
    # registry inside the dispatcher itself is EMPTY at v1 (no capability is
    # admitted yet); this entry only wires the doctrine + the verbatim,
    # hash-pinned executable into the install/lockfile/manifest/Bandit
    # authorities -- it grants no runtime capability by itself.
    "security-verification": [
        InstallSpec("default-on/security-verification.md",
                    "dev/modules/security-verification.md"),
        InstallSpec("default-on/run_security_verification.py",
                    "scripts/run_security_verification.py", verbatim=True),
    ],
}

# Module → the inline command-token whose value should default to the
# module's installed reference script.  The default value is derived
# from the verbatim spec's ``dst`` (below), so the token the module doc
# resolves (``{{claim_check_command}}`` etc.) and the path the scaffold
# installs to are one source of truth.
_REFERENCE_SCRIPT_TOKEN: dict[str, str] = {
    "claim-check": "claim_check_command",
}

#: Module → ``.gitignore`` entries the scaffold seeds when the module is
#: selected.  The work-intent log is session-local
#: coordination state, never a tracked artifact, so selecting
#: ``coordination-tiers`` seeds the substrate path.  Seeding is
#: non-clobber + idempotent (see :func:`seed_gitignore`).
_GITIGNORE_SEEDS: dict[str, tuple[str, ...]] = {
    "coordination-tiers": ("dev/intents.jsonl",),
    # Reflections are per-agent + ephemeral (gitignored); only the tracked
    # README.md guide survives, so the dir materializes on a fresh scaffold
    # without committing reflection content (fold-back #42).  Order matters:
    # ignore-all then un-ignore the README.
    "reflections": ("dev/reflections/*", "!dev/reflections/README.md"),
}


#: Module → repo-relative **pre-module local surfaces** the module supersedes.
#: When an adopter adopts a module that now owns a concern, an older local doc /
#: config the adopter wrote *before* the module existed is left in place by the
#: install (the install writes only the module's own files).  The adopter is
#: then left with two canonical-looking sources per concern and must notice +
#: reconcile by hand -- the silent post-sync drift this flag turns into an
#: advisory (foldback rollup #1).  Listed names are Cairn's own pre-module
#: conventions (the most likely predecessor forms); the flag is **advisory** --
#: it never deletes or edits the local form, the adopter reconciles or retires.
_MODULE_SUPERSEDES: dict[str, tuple[str, ...]] = {
    "security-review": ("dev/security_review_protocols.md",),
    "model-selection": ("dev/model_tier_mapping.md",),
    "architecture-review": ("dev/architecture_review.md",),
}


def superseded_local_surfaces(module_name: str, target_root: Path) -> list[str]:
    """Repo-relative pre-module local surfaces *module_name* supersedes that
    actually exist under *target_root* -- the set worth flagging for the adopter
    to reconcile or retire.  Empty when the module declares no supersession or
    none of the declared surfaces are present (no false note)."""
    return [
        rel
        for rel in _MODULE_SUPERSEDES.get(module_name, ())
        if (target_root / rel).exists()
    ]


def reference_script_token_defaults(module_names: list[str]) -> dict[str, str]:
    """Default command-token values for the selected reference-script
    modules.

    For each selected module that ships a verbatim reference script, map
    its command token (``claim_check_command``) to
    ``python <dst>`` where ``<dst>`` is the exact path the scaffold
    installs the script to.  The caller injects these into the token set
    *without* overriding a value the profile already supplied
    (``setdefault`` semantics), so an adopter can still point the token
    at a custom invocation.
    """
    defaults: dict[str, str] = {}
    for name in module_names:
        token = _REFERENCE_SCRIPT_TOKEN.get(name)
        if token is None:
            continue
        for spec in _MODULE_MAPPINGS.get(name, []):
            if spec.verbatim:
                defaults[token] = f"python {spec.dst}"
                break
    return defaults


# ---------------------------------------------------------------------------
# Selected-module required-token preflight
# ---------------------------------------------------------------------------
#
# A few modules carry inline tokens that have **no safe default** -- the
# scaffold cannot render the module's files without a real adopter-supplied
# value.  ``python-security`` is the first: its gate scans the adopter's own
# ``{{python_package}}`` directory, so an unfilled token would install a
# partially-rendered, lockfile-recorded security stack still containing the
# literal ``{{python_package}}``.
#
# Adding such a token to ``KNOWN_TOKENS`` is **not** enough: the scaffold
# installs rendered files first and only *warns* about leftover inline tokens
# afterward.  So selecting a module whose required token is unfilled must
# **fail closed before any target-tree or lockfile write**.  The map below
# declares, per module, the tokens that must resolve to a real value; the
# install / adopt-module / upgrade paths run :func:`missing_required_tokens`
# as a pre-write gate (see ``cli.main`` and ``upgrade``).  This is generic --
# any future module declares its required tokens here and inherits the gate.
_MODULE_REQUIRED_TOKENS: dict[str, tuple[str, ...]] = {
    # python-security's bandit/source gate scans {{python_package}};
    # there is no safe default for an adopter's own package directory.
    "python-security": ("python_package",),
}

# Required tokens and token gates answer opposite questions and must remain
# separate. The table above says "if selected, this token must be filled";
# this one says "a filled token selects this module". Merging them would make
# every future required-token module install itself automatically.
_TOKEN_GATED_MODULES: dict[str, tuple[str, ...]] = {
    "python-security": ("python_package",),
}

#: An inline token whose *value* is still an unfilled ``{{placeholder}}`` --
#: a token resolved to another token is as unfilled as an absent one.
_UNFILLED_TOKEN_VALUE = re.compile(r"\{\{\s*[\w.-]+\s*\}\}")


def token_gated_modules(cfg: dict[str, object]) -> list[str]:
    """Return modules selected by fully populated profile tokens."""
    selected: list[str] = []
    for module, required in _TOKEN_GATED_MODULES.items():
        if all(
            (value := cfg.get(token)) is not None
            and bool(str(value).strip())
            and _UNFILLED_TOKEN_VALUE.fullmatch(str(value).strip()) is None
            for token in required
        ):
            selected.append(module)
    return selected


def missing_required_tokens(
    modules: list[str], tokens: dict[str, str],
) -> list[tuple[str, str]]:
    """Return ``(module, token)`` pairs for every required token of every
    *selected* module that is **not** filled with a real value.

    A required token counts as unfilled when it is absent from *tokens*, is
    empty / whitespace-only, or still carries a ``{{placeholder}}`` value.
    The caller turns a non-empty result into a fail-closed refusal **before
    any write** (no target-tree files, no lockfile / module-state mutation).
    This function is pure: it reads no filesystem and mutates nothing, so it
    is safe to call from every install path's pre-write gate.

    The check is deliberately generic -- token *presence + fill*, not
    module-specific *value validity* (e.g. python-security's containment +
    is-a-directory checks on ``python_package`` live in that module's own
    gate).  This only guarantees a required token reaches the renderer
    with a real value; the module validates what that value means.
    """
    missing: list[tuple[str, str]] = []
    for module in modules:
        for token in _MODULE_REQUIRED_TOKENS.get(module, ()):
            value = tokens.get(token)
            if (
                value is None
                or not str(value).strip()
                or _UNFILLED_TOKEN_VALUE.fullmatch(str(value).strip())
            ):
                missing.append((module, token))
    return missing


# ---------------------------------------------------------------------------
# Governance presets
# ---------------------------------------------------------------------------
#
# Presets are *named points in the six-axis dimension model*, not a parallel
# config system.  An adopter picks a preset (the fast path) instead of
# hand-deriving the module roster; the six-axis scoring + the BOOTSTRAP.md
# I-5 gate table remain the principled backing (the gate table is the
# canonical per-module rationale).  See BOOTSTRAP.md Act I and the
# the source ``cairn-v0.2-p4-governance-presets`` plan.

#: The six dimension axes -> allowed enum values (the BOOTSTRAP.md I-4 table).
#: An adopter overrides a preset's canonical axis by setting a flat top-level
#: key in the profile YAML; an unknown enum value is a hard error.
_AXES: dict[str, tuple[str, ...]] = {
    "age": ("greenfield", "legacy"),
    "size": ("small", "medium", "large"),
    "complexity": ("simple", "moderate", "complex"),
    "language": ("single", "multi"),
    "human_team": ("solo", "small-multi", "large-multi"),
    "agent_team": (
        "single", "concurrent-single-type", "concurrent-multi-type",
    ),
}

#: The keys that carry the profile's *structure* rather than a token value or
#: a dimension axis.  The one hand-written third of the recognized set; the
#: other two thirds are read off ``KNOWN_TOKENS`` and ``_AXES``.
_STRUCTURAL_PROFILE_KEYS: frozenset[str] = frozenset({
    "preset", "modules", "modules_add", "modules_remove", "forge",
})

#: Every key a profile may carry -- **derived**, never a fourth hand-maintained
#: list: the inline tokens, the six dimension axes, the structural keys, and
#: the reserved ``schema``.  A key outside this set refuses the install before
#: any write (``load_config``): a mis-typed key is not a harmless extra, it is
#: whatever the adopter meant to set, dropped.
RECOGNIZED_PROFILE_KEYS: frozenset[str] = (
    KNOWN_TOKENS
    | frozenset(_AXES)
    | _STRUCTURAL_PROFILE_KEYS
    | frozenset({"schema"})
)


def unrecognized_profile_keys(cfg: dict[str, Any]) -> list[str]:
    """The profile's keys that are not in :data:`RECOGNIZED_PROFILE_KEYS`,
    sorted.  Pure: no filesystem, no mutation -- so every caller can run it as
    a pre-write gate."""
    return sorted(str(k) for k in cfg if str(k) not in RECOGNIZED_PROFILE_KEYS)


#: Per-module team-staffing gate: the ``agent_team`` axis values that staff
#: each module.  These are the ONLY part of the I-5 gate evaluated as runtime
#: code; the non-axis gate conditions (trust boundary, issue tracker, domain
#: partitioning, legacy readiness) are baked into each preset's authored
#: baseline below (the "gate-table encoding" split).
#:
#: The two modules gate **differently** (fold-back #40): ``coordination-tiers``
#: serves any *concurrent* team -- multiple same-type agents collide on shared
#: files exactly as a multi-type team does, and the work-intent mechanism is
#: what prevents it -- so it staffs both ``concurrent-multi-type`` and
#: ``concurrent-single-type``. ``dual-review`` is optional staffing guidance
#: for a Maintainer-called read from another agent type. The base one-review
#: method also works for a same-type team, but the optional module stays
#: ``concurrent-multi-type`` only.
_TEAM_STAFFING_GATES: dict[str, frozenset[str]] = {
    "dual-review": frozenset({"concurrent-multi-type"}),
    "coordination-tiers": frozenset(
        {"concurrent-multi-type", "concurrent-single-type"}
    ),
}

#: All team-staffing-gated module names (membership tests; staffability is
#: per-module via :func:`_can_staff_module`).
_TEAM_STAFFING_GATED: tuple[str, ...] = tuple(_TEAM_STAFFING_GATES)


def _can_staff_module(name: str, axes: dict[str, str]) -> bool:
    """True when the resolved agent-team axis staffs the given team-staffing
    module, per the per-module gate (fold-back #40)."""
    return axes.get("agent_team", "") in _TEAM_STAFFING_GATES.get(
        name, frozenset()
    )


#: Named governance presets.  Each carries a **canonical six-axis point** and
#: a **baseline roster** of the *non-team-staffing* modules the I-5 gate table
#: yields at that point (axis-derivable rows resolved at the canonical scores,
#: plus the non-axis rows the preset's profile assumes).  The team-staffing
#: modules (``dual-review`` / ``coordination-tiers``) are NOT listed here --
#: they are added at expand time iff the *resolved* agent-team axis staffs
#: them, so an adopter's real team is ground truth.  ``_DEFAULT_ON_MODULES``
#: is always the floor.  Derivation is documented row-by-row in BOOTSTRAP.md.
_PRESETS: dict[str, dict[str, object]] = {
    "solo-greenfield": {
        "axes": {
            "age": "greenfield", "size": "small", "complexity": "simple",
            "language": "single", "human_team": "solo",
            "agent_team": "single",
        },
        # Minimal: default-on only; no axis fires a team-gated module.
        "baseline": (),
    },
    "collaborative-team": {
        "axes": {
            "age": "greenfield", "size": "medium", "complexity": "moderate",
            "language": "single", "human_team": "small-multi",
            "agent_team": "concurrent-multi-type",
        },
        # complexity=moderate -> model-selection + testing-discipline;
        # size=medium -> doc-drift-prevention.  Coordination modules come
        # from the team-staffing gate (agent_team=concurrent-multi-type).
        "baseline": (
            "model-selection", "testing-discipline", "doc-drift-prevention",
        ),
    },
    "high-rigor-legacy": {
        "axes": {
            "age": "legacy", "size": "large", "complexity": "complex",
            "language": "multi", "human_team": "large-multi",
            "agent_team": "concurrent-multi-type",
        },
        # age=legacy -> legacy-agent; complexity=complex -> model-selection
        # + testing-discipline; size=large/language=multi ->
        # doc-drift-prevention; language=multi -> dual-language-tests;
        # trust-boundary (non-axis, assumed for legacy/large) ->
        # security-review.  Coordination modules from the team-staffing gate.
        "baseline": (
            "legacy-agent", "security-review", "dual-language-tests",
            "model-selection", "testing-discipline", "doc-drift-prevention",
        ),
    },
}


class PresetError(ValueError):
    """Raised on an invalid preset / override config (unknown preset, unknown
    module, unknown axis enum, wrong-type value, or the ``modules:`` +
    ``preset:`` conflict).  A friendly hard error, surfaced by ``main()``."""


def _as_str_list(value: object, key: str) -> list[str]:
    """Coerce a YAML value for a list-typed key to ``list[str]``; a scalar
    where a list is expected is a friendly hard error."""
    if value is None:
        return []
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise PresetError(
            f"`{key}` must be a YAML list (e.g. `{key}:` with `- module` "
            f"lines), not a {type(value).__name__} ({value!r})."
        )
    return [str(v) for v in value]


def _canonical_order(modules: set[str]) -> list[str]:
    """Order a module set deterministically: default-on first (in
    ``_DEFAULT_ON_MODULES`` order), then the rest in ``_MODULE_MAPPINGS``
    order.  Stable, diffable output for the summary + tests."""
    ordered: list[str] = [m for m in _DEFAULT_ON_MODULES if m in modules]
    for name in _MODULE_MAPPINGS:
        if name in modules and name not in ordered:
            ordered.append(name)
    # Any module not in the known maps (shouldn't happen post-validation)
    # trails, sorted, so nothing is silently dropped.
    ordered.extend(sorted(modules - set(ordered)))
    return ordered


def resolve_axes(preset_name: str, cfg: dict[str, object]) -> dict[str, str]:
    """Resolve the six-axis point: the preset's canonical point overridden by
    any flat axis key the adopter supplied.  An unknown enum value is a hard
    error; an absent axis key falls back to the preset's value."""
    canonical = dict(_PRESETS[preset_name]["axes"])  # type: ignore[arg-type]
    resolved = dict(canonical)
    for axis, allowed in _AXES.items():
        if axis in cfg and cfg[axis] is not None:
            value = str(cfg[axis])
            if value not in allowed:
                raise PresetError(
                    f"axis `{axis}` value {value!r} is not one of "
                    f"{', '.join(allowed)}."
                )
            resolved[axis] = value
    return resolved


#: Matches a ``cairn:if`` open-marker or a ``cairn:endif`` close-marker.
#: Group 1 = AXIS, Group 2 = comma-separated value list (open-marker only).
_IF_RE = re.compile(
    r"^[ \t]*<!--\s+cairn:(?:"
    r"if\s+(\w+)\s+in\s+([^\-].*?)(?:\s*-->)"
    r"|"
    r"endif"
    r"\s*-->"
    r")\s*$",
    re.MULTILINE,
)


def strip_conditional_regions(text: str, axes: dict[str, object]) -> str:
    """Remove or keep ``<!-- cairn:if AXIS in val1,val2 --> ... <!-- cairn:endif -->``
    regions according to the resolved dimension profile.

    **Five load-bearing semantics** (implement exactly):

    1. **keep-on-match** — if ``str(axes.get(AXIS, ""))`` is in the
       directive's value set, remove only the two marker comment lines
       (and each marker's own trailing newline), leaving the inner content
       in place with no blank-line artifact.

    2. **remove-otherwise** — if AXIS is present in *axes* but its value is
       NOT in the directive's value set, remove the entire region (both
       markers AND the content between them, including the trailing newline
       of the closing marker), leaving no blank-line residue.

    3. **keep-on-missing-axis** — if AXIS is **absent** from *axes*,
       keep the inner content (conservative safety default: never silently
       drop a section because the profile was incomplete).  This is the
       OPPOSITE of ``select_optional_templates``, which omits on missing;
       stripping from an always-on file must default to keep.

    4. **raise-on-unbalanced** — an open ``cairn:if`` with no matching
       ``cairn:endif``, a stray ``cairn:endif``, or a nested ``cairn:if``
       (a second open before the first closes) → ``ValueError`` with a
       clear message.

    5. **identity** — text with no ``cairn:if`` directive is returned
       byte-identical (the common case; no global state, no side-effects).

    Pure function; deterministic: same ``(text, axes)`` → byte-identical
    output every call.
    """
    # Fast path: nothing to process (checks both markers so a stray
    # cairn:endif with no cairn:if still goes through the validator).
    if "cairn:if" not in text and "cairn:endif" not in text:
        return text

    # Walk lines, collecting regions using a simple state machine.
    # We re-scan with splitlines(keepends=True) so we can reconstruct
    # the output exactly.
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    # State: None = top-level, or dict with region info once inside a block.
    region: dict[str, object] | None = None

    for lineno, line in enumerate(lines, start=1):
        # Try to match either an open or close marker on this line.
        # The marker must occupy the whole line (anchored by MULTILINE ^ $).
        m = _IF_RE.match(line.rstrip("\n"))
        if m is None:
            if region is None:
                out.append(line)
            else:
                # Accumulate content inside an open region.
                region["body_lines"].append(line)  # type: ignore[union-attr]
            continue

        axis_grp = m.group(1)   # None for endif
        vals_grp = m.group(2)   # None for endif

        if axis_grp is not None:
            # Open marker.
            if region is not None:
                raise ValueError(
                    f"cairn:if directive at line {lineno} is nested inside "
                    f"another open cairn:if (axis={region['axis']!r}); "
                    "nesting is not supported."
                )
            values = frozenset(v.strip() for v in vals_grp.split(","))
            region = {
                "axis": axis_grp,
                "values": values,
                "open_lineno": lineno,
                "body_lines": [],
            }
        else:
            # Close marker (endif).
            if region is None:
                raise ValueError(
                    f"Stray cairn:endif at line {lineno} with no matching "
                    "cairn:if open."
                )
            axis = region["axis"]
            values = region["values"]  # type: ignore[assignment]
            body: list[str] = region["body_lines"]  # type: ignore[assignment]

            if axis not in axes:
                # Semantic 3: missing axis → keep content.
                out.extend(body)
            else:
                current_value = str(axes[axis])
                if current_value in values:
                    # Semantic 1: keep-on-match → keep body, strip both markers.
                    out.extend(body)
                else:
                    # Semantic 2: remove-otherwise → discard markers + body.
                    pass  # nothing appended; blank-line residue is avoided
                    # because we also don't append the close marker below.

            region = None  # region closed

    if region is not None:
        raise ValueError(
            f"Unclosed cairn:if at line {region['open_lineno']} "
            f"(axis={region['axis']!r}): no matching cairn:endif found."
        )

    return "".join(out)


def expand_preset(cfg: dict[str, object]) -> tuple[list[str], dict[str, object]]:
    """Expand a ``preset:``-bearing profile into a module roster + a summary.

    The pinned ordered merge:

    1. Resolve axes = preset canonical point overridden by adopter axis keys.
    2. Baseline = ``_DEFAULT_ON_MODULES`` (always) + the preset's authored
       non-team-staffing roster + the team-staffing modules iff the resolved
       agent-team axis staffs them.
    3. Apply ``modules_add`` then ``modules_remove`` -- **remove wins** on a
       same-module conflict; an explicit add of an unstaffable module installs
       it with a loud staffability warning.
    4. (Backward-compat for the no-preset cases is handled in ``main()``.)

    Returns ``(ordered_modules, summary)`` where ``summary`` carries the
    preset, resolved axes, roster, overrides, and any warnings (for the
    ``--summary`` acceptance artifact).
    """
    preset_name = str(cfg.get("preset") or "").strip()
    if preset_name not in _PRESETS:
        raise PresetError(
            f"unknown preset {preset_name!r}; choose one of "
            f"{', '.join(sorted(_PRESETS))}."
        )

    resolved_axes = resolve_axes(preset_name, cfg)

    # Step 2: baseline.
    baseline: set[str] = set(_DEFAULT_ON_MODULES)
    baseline |= set(_PRESETS[preset_name]["baseline"])  # type: ignore[arg-type]
    for mod in _TEAM_STAFFING_GATED:
        if _can_staff_module(mod, resolved_axes):
            baseline.add(mod)

    # Token gates join the baseline before explicit overrides so
    # modules_remove remains the final authority.
    token_selected = set(token_gated_modules(cfg))
    baseline |= token_selected

    # Step 3: explicit overrides (validate names first).
    adds = _as_str_list(cfg.get("modules_add"), "modules_add")
    removes = _as_str_list(cfg.get("modules_remove"), "modules_remove")
    known = set(_MODULE_MAPPINGS) | set(_DEFAULT_ON_MODULES)
    for name in adds + removes:
        if name not in known:
            raise PresetError(
                f"unknown module {name!r} in modules_add/modules_remove; "
                f"known modules: {', '.join(sorted(known))}."
            )

    warnings: list[str] = []
    # Adds first.  An add of a team-staffing module the resolved team can't
    # staff installs anyway (adopter intent wins) with a loud warning.
    for name in adds:
        if name in _TEAM_STAFFING_GATED and not _can_staff_module(
            name, resolved_axes
        ):
            warnings.append(
                f"`{name}` was explicitly added but the resolved agent-team "
                f"axis ({resolved_axes.get('agent_team')}) cannot staff it; "
                f"installing per your explicit request -- confirm the team "
                f"configuration can staff the module's coordination "
                f"requirements before relying on it."
            )
    roster = set(baseline) | set(adds)
    # Removes win on conflict.
    removed_default_on: list[str] = []
    for name in removes:
        roster.discard(name)
        if name in _DEFAULT_ON_MODULES:
            removed_default_on.append(name)

    ordered = _canonical_order(roster)
    summary: dict[str, object] = {
        "preset": preset_name,
        "axes": resolved_axes,
        "modules": ordered,
        "modules_add": adds,
        "modules_remove": removes,
        "removed_default_on": removed_default_on,
        "token_gated": _canonical_order(token_selected & roster),
        "staffability_warnings": warnings,
    }
    return ordered, summary


def format_profile_summary(cfg: dict[str, object]) -> str:
    """Render the Maintainer-facing Act I-6 profile summary for a
    ``preset:``-bearing profile (the ``--summary`` acceptance artifact, P-4).

    Shows the chosen preset, the resolved six-axis point, the expanded module
    roster, the explicit add/remove overrides, any default-on opt-outs, and
    any staffability warnings -- so the Maintainer sees *why* the roster came
    out this way before anything is installed."""
    _modules, s = expand_preset(cfg)
    lines: list[str] = []
    project = str(cfg.get("project_name") or "<project_name>")
    lines.append(f"## Dimension profile -- {project}")
    lines.append("")
    lines.append(f"Preset: {s['preset']}")
    lines.append("")
    lines.append("Six-axis point (resolved):")
    for axis in _AXES:
        lines.append(f"  {axis:12s} {s['axes'][axis]}")  # type: ignore[index]
    lines.append("")
    lines.append("Module roster (to install):")
    for m in s["modules"]:  # type: ignore[union-attr]
        lines.append(f"  - {m}")
    if s["modules_add"]:
        lines.append(f"\nExplicit add:    {', '.join(s['modules_add'])}")  # type: ignore[arg-type]
    if s["modules_remove"]:
        lines.append(f"Explicit remove: {', '.join(s['modules_remove'])}")  # type: ignore[arg-type]
    if s["removed_default_on"]:
        lines.append(
            f"Default-on opted out: {', '.join(s['removed_default_on'])}"  # type: ignore[arg-type]
        )
    if s["token_gated"]:
        lines.append(
            "Token-gated (selected by a declared token): "
            f"{', '.join(s['token_gated'])}"  # type: ignore[arg-type]
        )
    if s["staffability_warnings"]:
        lines.append("")
        # Same per-warning line format as the installer path in main()
        # (`[warn] staffability: ...`), so programmatic detection and the
        # user-facing presentation are consistent across both surfaces.
        for w in s["staffability_warnings"]:  # type: ignore[union-attr]
            lines.append(f"  [warn] staffability: {w}")
    lines.append("")
    lines.append("Does this profile look right before I install anything?")
    return "\n".join(lines) + "\n"
