"""The profile loader's closed line grammar (`profile-parse-fail-open`).

Every NEW node this plan adds lives here, in a module carrying **no
module-level marker** — the gate manifest records a module-level ``pytestmark``
skipif against every node in the file, so a node added to a marked module reads
as ``SKIP-XFAIL-NEW`` (plan *Gate accounting* item (ii)).

Four properties are under test:

* **Chunk A** — ``_resolve_current_profile``'s lockfile fallback is *audible*:
  it names what it swallowed on stderr and still returns the lockfile profile.
* **Chunk B** — ``_minimal_yaml_parse`` is a **recognizer**: every non-blank
  line matches one of the eight accepted forms or the profile is refused with
  ``<path>:<line>: <reason>`` and a rewrite.  Soundness is asserted against
  PyYAML as an *independent oracle*; totality is asserted structurally (no
  input returns a partial dict).
* **Chunk C** — an unrecognized profile key **refuses before any write**; the
  recognized set is *derived*, never hand-maintained; a reserved ``schema`` key
  is read first so a future engine can say "this profile declares schema N".
* **Chunk D** — a drift gate over a **marker-defined corpus** of everything
  Cairn ships, writes or documents, parsed through the recognizer and asserted
  equal to ``yaml.safe_load``, with an oracle-identity canary and a divergence
  canary so the gate cannot pass vacuously.

**The oracle arrives by a channel that is not the artifact.** Every parity
assertion imports ``yaml`` directly.  ``_yaml_load`` is **banned as an
oracle**: since the Maintainer amendment of 2026-08-03 it is a compatibility
alias for the in-tree recognizer, so ``_yaml_load(x) == _minimal_yaml_parse(x)``
compares the function under test to itself.  Two live tests in
``bootstrap/tests/test_presets.py`` (lines 292 and 423) model the banned
pattern; they sit in a frozen file and are recorded as a residual rather than
repaired here.

**PyYAML absent is a failure, not a skip** (Maintainer amendment: *"make an
absent PyYAML oracle an explicit non-green condition rather than a skipped
test"*).  A skipped parity node takes both canaries with it and nothing in the
suite notices.
"""
from __future__ import annotations

import re
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]
if str(CAIRN_ROOT) not in sys.path:
    sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap._scaffold import config as _config  # noqa: E402
from bootstrap._scaffold.config import (  # noqa: E402
    ProfileGrammarError,
    _minimal_yaml_parse,
    load_config,
)
from bootstrap._scaffold.upgrade import (  # noqa: E402
    _PROFILE_REL,
    _resolve_current_profile,
)


# ---------------------------------------------------------------------------
# Chunk A -- the upgrade-path fallback stops swallowing
# ---------------------------------------------------------------------------

def _lock_with_profile() -> dict:
    return {
        "profile": {
            "preset": "solo-greenfield",
            "axes": {
                "age": "greenfield", "size": "small", "complexity": "simple",
                "language": "single", "human_team": "solo",
                "agent_team": "single",
            },
        },
    }


class TestResolveCurrentProfileIsAudible:
    """A2: an unreadable / ungrammatical committed profile makes
    ``_resolve_current_profile`` say so **and** still fall back.

    Both halves are asserted, so a future change that makes the fallback
    loud-and-fatal, or quiet-and-tolerant again, fails.  The oracle is the
    *stderr channel*, not any value the function returns; the fixture profile
    is written by the test, never produced by the engine.
    """

    def test_unreadable_profile_names_what_it_swallowed(
        self, tmp_path: Path, capsys,
    ) -> None:
        """An **unreadable** profile -- the one shape that raises out of
        ``load_config`` at HEAD too, so this node is independent of Chunk B."""
        profile = tmp_path / _PROFILE_REL
        profile.parent.mkdir(parents=True, exist_ok=True)
        # Invalid UTF-8: read_text(encoding="utf-8") raises UnicodeDecodeError.
        profile.write_bytes(b"project_name: \xff\xfe not utf-8\n")

        lock = _lock_with_profile()
        block, axes = _resolve_current_profile(tmp_path, lock)

        err = capsys.readouterr().err
        assert _PROFILE_REL in err, (
            "the swallowed failure must name the profile path; got:\n" + err
        )
        assert "UnicodeDecodeError" in err, (
            "the swallowed failure must name the exception type; got:\n" + err
        )
        # the disposition is unchanged -- still the lockfile's embedded profile
        assert block == lock["profile"]
        assert axes["human_team"] == "solo"

    def test_ungrammatical_profile_names_what_it_swallowed(
        self, tmp_path: Path, capsys,
    ) -> None:
        """The Chunk-B shape: a nested mapping the closed grammar refuses.
        A stricter ``load_config`` feeds this handler more exceptions, which is
        exactly why Chunk A lands first."""
        profile = tmp_path / _PROFILE_REL
        profile.parent.mkdir(parents=True, exist_ok=True)
        profile.write_text("parent:\n  child: val\n", encoding="utf-8")

        lock = _lock_with_profile()
        block, axes = _resolve_current_profile(tmp_path, lock)

        err = capsys.readouterr().err
        assert _PROFILE_REL in err, (
            "the swallowed failure must name the profile path; got:\n" + err
        )
        assert block == lock["profile"]
        assert axes["human_team"] == "solo"

    def test_a_readable_profile_stays_silent(self, tmp_path: Path, capsys) -> None:
        """The message fires on the swallow, not on every upgrade."""
        profile = tmp_path / _PROFILE_REL
        profile.parent.mkdir(parents=True, exist_ok=True)
        profile.write_text(
            textwrap.dedent("""\
                project_name: Demo
                test_command: pytest
                preset: high-rigor-legacy
            """),
            encoding="utf-8",
        )
        block, axes = _resolve_current_profile(tmp_path, _lock_with_profile())
        assert capsys.readouterr().err == ""
        assert block["preset"] == "high-rigor-legacy"
        assert axes["size"] == "large"


# ---------------------------------------------------------------------------
# Shared helper -- the recognizer refuses with a locatable message
# ---------------------------------------------------------------------------

def _refusal(text: str, source: str = "profile.yml") -> str:
    """Assert *text* is refused and return the refusal message."""
    with pytest.raises(ValueError) as exc:
        _minimal_yaml_parse(text, source=source)
    return str(exc.value)


def _oracle():
    """PyYAML, imported **directly** -- the independent oracle.

    An absent PyYAML is an explicit **non-green** condition, not a skip
    (Maintainer amendment 2026-08-03).  A skipped parity node takes the
    soundness sweep *and both canaries* with it, and nothing in the suite --
    no conftest hook, no CI job -- notices a non-zero skip count."""
    try:
        import yaml  # noqa: PLC0415
    except ImportError:  # pragma: no cover -- the non-green condition
        pytest.fail(
            "PyYAML absent: the parity sweep and both canaries did not run. "
            "PyYAML is a TEST-ONLY oracle (never a runtime parser), but "
            "without it nothing checks the recognizer against an independent "
            "implementation -- install it rather than skipping this node."
        )
    return yaml


# ---------------------------------------------------------------------------
# Chunk B -- grammar soundness (against the oracle) and totality (structural)
# ---------------------------------------------------------------------------

#: Seeds: the proposal's twelve-row divergence table plus the Internal
#: review's seven rows.  Seeds, not the whole test -- the generative node
#: below samples the eight forms in combination.
_SOUND_SEEDS: tuple[str, ...] = (
    "project_name: MyProject\n",
    "project_name: MyProject\ntest_command: pytest\n",
    '  project_name: X\n  preset: high-rigor-legacy\n',
    "forge: gitlab        # gitlab | github\n",
    "project_name: 'O''Brien Lab Model'\n",
    'project_name: "My Project"\n',
    "project_name: X\nmodules:\n",
    "modules: []\n",
    "modules:\n  - a\n  - b\n",
    "modules:\n- a\n- b\n",
    "modules:\n  - lifecycle-metrics  # always on\n",
    "---\nproject_name: X\n",
    "{}",
    "project_name: issue#42-tracker\n",
    "project_name: a#b\n",
    "test_command: pytest -k not-slow#fast\n",
    "size: 3\n",
    "size: -3\n",
    "size: 0\n",
    "age: <greenfield|legacy>\n",
    "# leading comment\n\nproject_name: X\n\n# trailing comment\n",
    "project_name: X\r\ntest_command: pytest\r\n",
    "project_name: A\rtest_command: B\n",
    "project_name: 'a  '\n",
    'test_command: "pytest --maxfail=1"\n',
)


def _generated_profiles() -> list[str]:
    """Inputs assembled from the eight accepted line forms in combination.

    Deterministic and stdlib-only (the amendment declines a new dev
    dependency): the cross-product of a key, a value form, a comment
    decoration, a list shape and a line ending."""
    keys = ("project_name", "test_command", "forge", "preset")
    values = (
        "plain-value", "'sq value'", "'it''s'", '"dq value"', "42", "-7",
        "<a|b>", "has#hash", "0",
    )
    tails = ("", "        # trailing note", " # short note")
    lists = ("", "modules:\n  - a\n  - b\n", "modules:\n- a\n- b\n",
             "modules: []\n", "modules:\n")
    heads = ("", "---\n", "# a comment\n")
    out: list[str] = []
    for index, key in enumerate(keys):
        for value in values:
            for tail in tails:
                head = heads[(index + len(value)) % len(heads)]
                block = lists[(index + len(tail) + len(value)) % len(lists)]
                out.append(f"{head}{key}: {value}{tail}\n{block}")
                # the same document, uniformly indented -- what a copy-paste
                # out of a rendered documentation page produces
                indented = "".join(
                    ("  " + line if line.strip() else line)
                    for line in f"{key}: {value}{tail}\n{block}".splitlines(True)
                )
                out.append(indented)
    return out


class TestGrammarSoundness:
    """B6: every input the grammar accepts parses to ``yaml.safe_load``'s
    value.  Verified over a finite corpus -- this samples the grammar, it does
    not prove that no accepted input diverges."""

    def test_seed_rows_parse_identically_to_the_oracle(self) -> None:
        yaml = _oracle()
        for text in _SOUND_SEEDS:
            assert _minimal_yaml_parse(text) == yaml.safe_load(text), text

    def test_generated_forms_parse_identically_to_the_oracle(self) -> None:
        yaml = _oracle()
        checked = 0
        for text in _generated_profiles():
            try:
                got = _minimal_yaml_parse(text)
            except ValueError:
                # A refusal is always contract-legal; only *acceptance* has to
                # agree with the oracle.  But it must not be a refusal of
                # something the oracle also happens to reject silently.
                continue
            assert got == yaml.safe_load(text), text
            checked += 1
        assert checked > 200, (
            f"only {checked} generated documents were accepted; the generator "
            "has stopped exercising the grammar"
        )

    def test_the_oracle_is_not_the_function_under_test(self) -> None:
        """The **oracle-identity canary**.  No stdlib recognizer can return a
        ``datetime.date``, so this cannot pass if the oracle has silently
        become the artifact.  Perturbation: route the oracle through
        ``_yaml_load`` (or set ``sys.modules['yaml'] = None`` before import)
        and this fails."""
        import datetime  # noqa: PLC0415

        yaml = _oracle()
        assert isinstance(yaml.safe_load("d: 2024-01-01")["d"], datetime.date)
        with pytest.raises(ValueError):
            _minimal_yaml_parse("d: 2024-01-01\n")

    def test_the_gate_can_still_see_a_disagreement(self) -> None:
        """The **divergence canary**: an input the oracle accepts and the
        grammar refuses.  A gate that can no longer *see* a difference is a
        gate that has stopped working."""
        yaml = _oracle()
        assert yaml.safe_load("modules: [a, b]\n") == {"modules": ["a", "b"]}
        assert "inline" in _refusal("modules: [a, b]\n")


class TestGrammarTotality:
    """B7: part (b) of the invariant -- **no content line is ever silently
    dropped**.  Structural: the parse loop refuses any line matching no form,
    so every row below raises, with a line number, and returns nothing."""

    #: ``(label, text, expected line number)``.  Contains every row from the
    #: review findings [I1] (empty / indented), [I2] (comments), [I3] (the
    #: writers' own shapes) and [I4] (truncation / folded blocks) by name.
    ROWS: tuple[tuple[str, str, int], ...] = (
        ("I1 zero-byte", "", 1),
        ("I1 whitespace-only", "   \n \n", 1),
        ("I1 comment-only", "# nothing but a comment\n", 1),
        ("I4 flow sequence", "modules: [a, b]\n", 1),
        ("I4 flow mapping", "axes: {age: legacy}\n", 1),
        ("I1 nested mapping", "parent:\n  child: val\n", 2),
        ("I4 tab indent", "modules:\n\t- item\n", 2),
        ("I4 no space after colon", "preset:solo-greenfield\n", 1),
        ("I2 boolean", "forge: no\n", 1),
        ("I4 octal-looking", "schema: 010\n", 1),
        ("I4 sexagesimal", "project_name: 1:30\n", 1),
        ("I4 date", "project_name: 2024-01-01\n", 1),
        ("I4 float", "project_name: 1.5\n", 1),
        ("I3 mixed indent list", "modules:\n  - a\n- b\n", 3),
        ("I3 orphan list item", "- item1\n- item2\n", 1),
        ("I4 folded block", "test_command: >\n  a b\n", 1),
        ("I4 literal block", "test_command: |\n  a b\n", 1),
        ("I4 anchor", "project_name: &anchor X\n", 1),
        ("I4 alias", "project_name: *anchor\n", 1),
        ("I4 tag", "project_name: !!str X\n", 1),
        ("I4 truncated single quote", "project_name: 'unterminated\n", 1),
        ("I4 truncated double quote", 'project_name: "unterminated\n', 1),
        ("I4 backslash escape", 'test_command: "a\\nb"\n', 1),
        ("I2 interior double quote", 'project_name: a"b\n', 1),
        ("I2 interior apostrophe", "project_name: O'Brien\n", 1),
        ("I4 second document", "project_name: X\n---\npreset: solo\n", 2),
        ("I4 duplicate key", "project_name: A\nproject_name: B\n", 2),
        ("I4 empty list item", "modules:\n  - \n", 2),
        # Written as an escape, never as a literal: a bare U+FEFF in
        # source is invisible and any editor or transport may eat it,
        # silently retiring the row.  Same reasoning as
        # ``_SAMPLE_INVISIBLES`` below.
        ("I4 BOM", "\ufeffproject_name: X\n", 1),
        ("I4 NUL", "project_name: a\x00b\n", 1),
        ("I4 ESC", "project_name: a\x1bb\n", 1),
        ("I4 backspace", "project_name: a\x08b\n", 1),
        ("I4 trailing text after quote", "project_name: 'a' junk\n", 1),
        ("I4 dedented key", "  project_name: X\npreset: solo\n", 2),
        ("I4 bare word line", "project_name: X\njust-a-word\n", 2),
    )

    def test_every_malformed_row_refuses_with_a_line_number(self) -> None:
        for label, text, lineno in self.ROWS:
            message = _refusal(text)
            assert message.startswith(f"profile.yml:{lineno}:"), (
                f"{label}: expected a refusal at line {lineno}, got {message!r}"
            )

    def test_no_malformed_input_returns_a_partial_dict(self) -> None:
        """The property the whole change exists for: there is no third
        outcome.  A row that returned *anything* would be a silent drop."""
        for label, text, _lineno in self.ROWS:
            try:
                got = _minimal_yaml_parse(text)
            except ValueError:
                continue
            pytest.fail(f"{label}: returned {got!r} instead of refusing")

    def test_a_refusal_names_the_rewrite_not_a_dependency(self) -> None:
        """B3: "install PyYAML" is never an acceptable remedy in a
        zero-dependency project."""
        for _label, text, _lineno in self.ROWS:
            message = _refusal(text)
            assert "pyyaml" not in message.lower(), message
        assert "- a" in _refusal("modules: [a, b]\n")
        assert '"no"' in _refusal("forge: no\n")
        assert "quoted" in _refusal("size: 010\n")


class TestCommentConvention:
    """B8: a ``#`` opens a comment **only** at the start of a value or when
    preceded by a space -- both directions.  A **tab** is refused outright:
    PyYAML rejects a tab inside a plain scalar, so accepting one would break
    the equality half of the invariant."""

    def test_a_spaced_hash_is_a_comment(self) -> None:
        yaml = _oracle()
        for text in (
            "forge: gitlab   # gitlab | github\n",
            "modules:\n  - lifecycle-metrics  # always on\n",
            "project_name: X\nmodules:  # nothing selected\n",
        ):
            assert _minimal_yaml_parse(text) == yaml.safe_load(text), text

    def test_an_unspaced_hash_is_preserved(self) -> None:
        yaml = _oracle()
        for text in (
            "project_name: a#b\n",
            "project_name: issue#42-tracker\n",
            "test_command: pytest -k not-slow#fast\n",
            "modules:\n  - mod#1\n",
        ):
            parsed = _minimal_yaml_parse(text)
            assert parsed == yaml.safe_load(text), text
            assert "#" in str(list(parsed.values())[0]), text


class TestLineEndings:
    """B9: CRLF and a lone ``\\r`` introduce **no divergence class of their
    own** -- measured, not assumed.  Perturbation: split the grammar's lines
    with ``text.split("\\n")`` instead of ``text.splitlines()`` and the
    lone-``\\r`` row regresses."""

    SHAPES: tuple[str, ...] = (
        "project_name: X{eol}test_command: pytest{eol}",
        "forge: gitlab   # note{eol}project_name: X{eol}",
        'project_name: "My Project"{eol}',
        "project_name: 'O''Brien'{eol}",
        "modules:{eol}  - a{eol}  - b{eol}",
        "project_name: 'a  '{eol}",
    )

    def test_lf_crlf_and_lone_cr_all_agree_with_the_oracle(self) -> None:
        yaml = _oracle()
        for shape in self.SHAPES:
            for eol in ("\n", "\r\n", "\r"):
                text = shape.format(eol=eol)
                assert _minimal_yaml_parse(text) == yaml.safe_load(text), (
                    repr(text)
                )


#: Every codepoint Python calls whitespace, enumerated **from the running
#: interpreter's Unicode tables** rather than listed -- **29** of them on
#: CPython 3.13.13 (``as_of 2026-08-04``; the number is the interpreter's, and
#: that it is the interpreter's is the point).
#:
#: YAML's own whitespace is only SPACE (``U+0020``) and TAB (``U+0009``), which
#: leaves **27** others -- but they are *not* one homogeneous class, and the
#: difference is what the sweeps below have to survive.  Measured by probing
#: ``yaml.safe_load`` once per codepoint (``as_of 2026-08-04``, PyYAML on the
#: canonical interpreter), not reasoned from the spec:
#:
#: * **16 are ordinary text to the oracle** -- NBSP, OGHAM SPACE MARK, the
#:   ``U+2000``--``U+200A`` quad/em family, ``U+202F``, ``U+205F``, ``U+3000``.
#:   ``safe_load`` keeps them *inside* the scalar, so a reader built on the
#:   no-argument ``str.strip()`` *consumes* a character the oracle preserves.
#:   **This subset is the hazard**; it is the whole of what the tokenizer half
#:   of the contract is defending.
#: * **5 are YAML line breaks** -- ``U+000A``, ``U+000D``, ``U+0085``,
#:   ``U+2028``, ``U+2029``.  PyYAML ends the line at them and so does
#:   ``str.splitlines()``, so the two agree and no *different key* is reachable.
#: * **6 the oracle refuses outright** as non-printable (``ReaderError``) --
#:   ``U+000B``, ``U+000C`` and ``U+001C``--``U+001F``.  Nothing in the
#:   tokenizer holds these; ``_PROFILE_CONTROL_RE`` does, which is why deleting
#:   that scan is the one single-control mutation that turns
#:   ``..._refuses_or_equals_the_oracle`` red (see the class docstring).
#:
#: Enumerating rather than listing is what makes a future Unicode revision that
#: adds a codepoint show up as a failure instead of as an untested gap.
_ISSPACE_CODEPOINTS: tuple[str, ...] = tuple(
    chr(point) for point in range(0x110000) if chr(point).isspace()
)

#: ``(label, template)``.  ``{c}`` is the whitespace character under test.
#: Each position is one place a copy-paste out of a rendered page drops one.
_INVISIBLE_POSITIONS: tuple[tuple[str, str], ...] = (
    ("key-prefix",       "{c}project_name: X\n"),
    ("key-suffix",       "project_name{c}: X\n"),
    ("value-prefix",     "project_name:{c}X\n"),
    # Distinct from the row above, and the distinction is load-bearing: the
    # key pattern requires a real SPACE after the `:`, so only *this* shape
    # reaches the value-side tokenizer at all.  Without it the
    # ``raw.lstrip(" ")`` control has no input that exercises it and its
    # perturbation stays green -- measured.
    ("value-prefix-spaced", "project_name: {c}X\n"),
    ("value-suffix",     "project_name: X{c}\n"),
    ("value-interior",   "project_name: A{c}B\n"),
    ("indent",           "{c} project_name: X\n"),
    ("own-line",         "project_name: X\n{c}\n"),
    ("before-comment",   "project_name: X{c}# c\n"),
    ("list-item",        "modules:\n  - a{c}b\n"),
    ("list-value-spaced", "modules:\n  - {c}a\n"),
    ("list-indent",      "modules:\n {c}- a\n"),
    ("whole-document",   "{c}\n"),
)


#: A regex that matches nothing (``(?!)`` is the never-satisfiable assertion),
#: used to switch the Unicode-space **diagnostic** off inside a test so the
#: **tokenizer** can be measured on its own.  See
#: ``TestInvisibleWhitespaceIsNotConsumed`` for why that separation matters.
_NEVER_MATCHES = re.compile("(?!)")

#: A sample of the invisible characters, written as escapes rather than
#: literals: a test *about* characters an editor renders as a space must not
#: itself contain any.
_NBSP = "\u00a0"
_SAMPLE_INVISIBLES: tuple[str, ...] = (
    "\u00a0",  # NO-BREAK SPACE -- what a copy-paste out of a rendered page gives
    "\u1680",  # OGHAM SPACE MARK
    "\u2000",  # EN QUAD
    "\u2003",  # EM SPACE
    "\u2007",  # FIGURE SPACE
    "\u202f",  # NARROW NO-BREAK SPACE
    "\u205f",  # MEDIUM MATHEMATICAL SPACE
    "\u3000",  # IDEOGRAPHIC SPACE
)


def _invisible_corpus() -> list[tuple[str, str]]:
    """Every ``str.isspace()`` codepoint in every position, labelled."""
    return [
        (f"U+{ord(char):04X} {label}", template.format(c=char))
        for char in _ISSPACE_CODEPOINTS
        for label, template in _INVISIBLE_POSITIONS
    ]


def _third_outcomes(rows: list[tuple[str, str]], yaml) -> list[str]:
    """Rows where the recognizer neither refused nor returned the oracle's
    value -- the outcome the contract denies.

    A refusal is always contract-legal, and so is an equal return; only the
    *silent disagreement* is a violation.  Expressing the invariant directly
    (rather than asserting "refuses") is what keeps this from over-specifying:
    a control that makes an input merely *agree* instead of refusing is still
    correct, and this helper says so."""
    violations: list[str] = []
    for label, text in rows:
        try:
            oracle = yaml.safe_load(text)
            oracle_raised = False
        except Exception:  # noqa: BLE001 -- any oracle refusal is legal
            oracle, oracle_raised = None, True
        try:
            got = _minimal_yaml_parse(text, source="profile.yml")
        except ValueError as exc:
            assert str(exc).startswith("profile.yml:"), str(exc)
            continue
        if oracle_raised or got != oracle or type(got) is not type(oracle):
            violations.append(
                f"{label}: text={text!r} "
                f"oracle={'<raised>' if oracle_raised else repr(oracle)} "
                f"recognizer={got!r}"
            )
    return violations


class TestInvisibleWhitespaceIsNotConsumed:
    """Amendment 2's hazard class, closed on its **whitespace** flank.

    **Three controls, not two**, and naming them is what keeps this class's
    claims honest:

    1. **The tokenizer** strips exactly ``" "`` in three places
       (``line.strip(" ")``, ``raw.lstrip(" ")``, ``value.rstrip(" ")``), so
       any other whitespace stays inside the token and falls through to a
       refusal.  This is the *guarantee*, and it is structural rather than
       enumerated.
    2. **``_PROFILE_UNICODE_SPACE_RE``** is the **diagnostic** that names the
       codepoint in the refusal.  It is not the guarantee, and it runs *first*.
    3. **``_PROFILE_CONTROL_RE``** enumerates C0/C1, ``U+2028``/``U+2029`` and
       the BOM.  It carries the 6 ``str.isspace()`` codepoints the oracle
       refuses outright (``U+000B``, ``U+000C``, ``U+001C``--``U+001F``) --
       see ``_ISSPACE_CODEPOINTS`` for that three-way split.  Nothing in the
       tokenizer holds those 6.

    **The tokenizer and the diagnostic are tested separately, and the reason is
    the whole point.**  The diagnostic runs first, so while it is in place a
    loosened tokenizer is *invisible*: reverting ``line.strip(" ")`` to
    ``line.strip()`` on the shipped module leaves the shipped-configuration
    sweep green, because the enumeration refuses the input before the tokenizer
    ever sees it -- measured, not reasoned.  An enumeration is exactly what a
    future Unicode revision outdates, so a suite that exercised only the shipped
    pair would let the hole reopen silently the moment the enumeration went
    stale.  ``test_the_invariant_holds_without_the_diagnostic`` therefore
    switches the diagnostic off and re-asserts the invariant against the
    tokenizer alone.

    **Measured perturbation table.**  Each row applied to
    ``bootstrap/_scaffold/config.py``, ``__pycache__`` purged, the whole module
    run on CPython 3.13.13, and ``config.py`` restored byte-identically
    (sha256-verified).  ``as_of 2026-08-04``.  *Purging the bytecode cache is
    not ceremony*: the three tokenizer mutants each delete the same 3 bytes
    (``" "``), so all three files are byte-identical in length and CPython --
    which validates a cached ``.pyc`` on (mtime-seconds, size) -- silently
    reports the **first** mutant's result for the other two.  Reproduced
    deliberately: without a purge all three report 80 third outcomes; with one
    they report 80 / 32 / 16.  That is how an earlier round of this table
    shipped figures that did not reproduce.

    ===============================================  =========================================
    perturbation                                      node(s) that go red
    ===============================================  =========================================
    ``line.strip(" ")`` -> ``line.strip()``           ``..._holds_without_the_diagnostic`` +
                                                      ``..._never_eaten_from_a_value``
    ``value.rstrip(" ")`` -> ``value.rstrip()``       ``..._holds_without_the_diagnostic`` +
                                                      ``..._never_eaten_from_a_value``
    ``raw.lstrip(" ")`` -> ``raw.lstrip()``           ``..._holds_without_the_diagnostic``
    delete the ``_PROFILE_UNICODE_SPACE_RE`` scan     ``..._names_the_codepoint``
    delete the ``_PROFILE_CONTROL_RE`` scan           ``..._refuses_or_equals_the_oracle`` +
                                                      ``..._holds_without_the_diagnostic``
                                                      (+3 in ``TestGrammarTotality``)
    ``line.lstrip(" ")`` -> ``line.lstrip()``         **none** -- a genuine no-op, recorded
                                                      as such rather than given a
                                                      manufactured test
    ===============================================  =========================================

    **One node in this class is subsumed, and it says so itself.**
    ``test_every_isspace_codepoint_refuses_or_equals_the_oracle`` runs the same
    corpus as ``..._holds_without_the_diagnostic`` in the *shipped*
    configuration.  Disabling the diagnostic only removes a refusal path, and a
    refusal is contract-legal, so every third outcome visible with the
    diagnostic on is still one with it off: the shipped node's falsifier set is
    a strict **subset** of the diagnostic-off node's, and no mutation can turn
    it red alone.  It is kept as the delivered-configuration statement, not as
    any control's guard; each of the three controls has its own falsifier in the
    table above.
    """

    def test_the_enumeration_is_the_interpreters_not_a_list(self) -> None:
        """Guards the guard: if the codepoint set ever collapses to a handful,
        the two sweeps below stop meaning anything."""
        assert len(_ISSPACE_CODEPOINTS) >= 25, _ISSPACE_CODEPOINTS
        for expected in (*_SAMPLE_INVISIBLES, "\t", "\n", " "):
            assert expected in _ISSPACE_CODEPOINTS, repr(expected)
        assert len(_invisible_corpus()) >= 250

    def test_every_isspace_codepoint_refuses_or_equals_the_oracle(self) -> None:
        """The delivered contract over the whole whitespace class, in the
        **shipped** configuration: for every ``str.isspace()`` codepoint in
        every position, the recognizer either refuses with a line number or
        returns exactly ``yaml.safe_load``'s value.

        **This node is deliberately subsumed and guards no control on its
        own.**  It runs the same corpus as
        ``test_the_invariant_holds_without_the_diagnostic``, which runs it with
        one refusal path removed -- and since a refusal is contract-legal,
        removing one can only *add* third outcomes.  Its falsifier set is
        therefore a strict subset of that node's and it can never go red alone.
        The single-control mutation that does turn it red is deleting the
        ``_PROFILE_CONTROL_RE`` scan (the 6 codepoints the oracle refuses
        outright, which the tokenizer does not hold); the diagnostic-off node
        goes red there too.  Kept because it is the only node that states the
        guarantee for the configuration adopters actually run -- no
        monkeypatch."""
        violations = _third_outcomes(_invisible_corpus(), _oracle())
        assert not violations, (
            f"{len(violations)} input(s) returned a value the oracle does not "
            "return, without refusing -- the third outcome the contract "
            "denies:\n  " + "\n  ".join(violations)
        )

    def test_the_invariant_holds_without_the_diagnostic(
        self, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """**The structural claim, isolated.**

        With the Unicode-space enumeration switched off, the contract must
        still hold on the tokenizer alone -- which is exactly the sentence
        ``config.py`` writes above ``_PROFILE_UNICODE_SPACE_RE`` (*"this class
        is the diagnostic, not the guarantee"*), asserted rather than
        asserted-about.

        This is the node all **three** tokenizer perturbations turn red.
        Measured with this module's own ``_invisible_corpus()`` and
        ``_third_outcomes`` driven against a mutated
        ``bootstrap/_scaffold/config.py`` (CPython 3.13.13, ``__pycache__``
        purged per mutant, source restored byte-identically; ``as_of
        2026-08-04``) -- of the **377** inputs in the corpus, with the
        diagnostic disabled:

        * ``line.strip()`` puts **80** into the third-outcome class
          (``key-prefix``, ``value-suffix``, ``indent``, ``own-line``,
          ``list-indent`` x the 16 ordinary-text codepoints),
        * ``raw.lstrip()`` puts **32** there (``value-prefix-spaced``,
          ``list-value-spaced`` x 16),
        * ``value.rstrip()`` puts **16** there (``value-suffix`` x 16).

        In the shipped configuration, and with the diagnostic disabled but no
        mutation, the count is **0**."""
        monkeypatch.setattr(_config, "_PROFILE_UNICODE_SPACE_RE",
                            _NEVER_MATCHES)
        assert _config._PROFILE_UNICODE_SPACE_RE.search(_NBSP) is None, (
            "the diagnostic was not actually disabled, so this node would be "
            "measuring the enumeration all over again"
        )
        violations = _third_outcomes(_invisible_corpus(), _oracle())
        assert not violations, (
            f"with the Unicode-space diagnostic disabled, {len(violations)} "
            "input(s) fell into the third outcome -- the tokenizer is not "
            "holding the contract on its own, so the guarantee is an "
            "enumeration after all:\n  " + "\n  ".join(violations)
        )

    def test_an_nbsp_prefixed_key_is_a_different_key_to_the_oracle(self) -> None:
        """The single sharpest input, named.

        ``U+00A0`` is what a copy-paste out of a rendered documentation page
        produces.  To PyYAML the key is ``'\\xa0project_name'`` -- a *different
        key*, which is Amendment 2's own byte-order-mark sentence with a
        character an editor renders as an ordinary space."""
        yaml = _oracle()
        text = f"{_NBSP}project_name: X\n"
        assert yaml.safe_load(text) == {f"{_NBSP}project_name": "X"}
        assert "project_name" not in yaml.safe_load(text)
        _refusal(text)

    def test_a_trailing_invisible_space_is_never_eaten_from_a_value(
        self, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Pins ``value.rstrip(" ")``, with the diagnostic off so the
        assertion can reach it.

        ``project_name`` is rendered into the adopter's tree, so eating a
        trailing NBSP installs a *different* project name at exit 0.  The
        contract permits a refusal **or** the oracle's value; it forbids the
        stripped one, which is what the no-argument ``rstrip()`` returns."""
        monkeypatch.setattr(_config, "_PROFILE_UNICODE_SPACE_RE",
                            _NEVER_MATCHES)
        yaml = _oracle()
        for char in _SAMPLE_INVISIBLES:
            text = f"project_name: X{char}\n"
            assert yaml.safe_load(text) == {"project_name": f"X{char}"}
            try:
                got = _minimal_yaml_parse(text, source="profile.yml")
            except ValueError as exc:
                assert str(exc).startswith("profile.yml:"), str(exc)
                continue
            assert got == {"project_name": f"X{char}"}, (
                f"U+{ord(char):04X} was eaten off the end of the value: {got!r}"
            )

    def test_the_refusal_names_the_codepoint(self) -> None:
        """The **diagnostic** half, which the structural node deliberately does
        not cover: an invisible character needs its codepoint printed, because
        a generic "not a recognized profile line" points at a line that looks
        perfectly correct in an editor.  Perturbation: delete the
        ``_PROFILE_UNICODE_SPACE_RE`` search -- both sweeps stay green (the
        contract still holds) and this node fails."""
        for char in _SAMPLE_INVISIBLES:
            message = _refusal(f"{char}project_name: X\n")
            assert f"U+{ord(char):04X}" in message, message
            assert "SPACE and TAB" in message, message

    def test_an_ordinary_space_is_still_ordinary(self) -> None:
        """The other direction -- the rule must not refuse real profiles.
        Indentation, alignment padding and a padded trailing comment all use
        ``U+0020`` and stay accepted."""
        yaml = _oracle()
        for text in (
            "  project_name: X\n  preset: high-rigor-legacy\n",
            "forge: gitlab        # gitlab | github\n",
            "modules:\n  - a\n  - b\n",
            "project_name: 'a  '\n",
        ):
            assert _minimal_yaml_parse(text) == yaml.safe_load(text), text


class TestImplicitResolverTokens:
    """The plain-scalar admissibility rule against PyYAML's **implicit
    resolvers**, not just its scalar syntax.

    ``=`` is the YAML 1.1 *value* key and ``<<`` the *merge* key -- ``safe_load``
    raises ``ConstructorError`` on both -- and ``?`` opens a complex mapping
    key, which raises ``ScannerError``.  A textual reader that took them for
    plain strings would hand back a value where the oracle refuses: the same
    third-outcome shape as the whitespace hole, reached from the resolver side
    rather than the tokenizer side.

    Perturbation: delete the ``_PROFILE_RESOLVER_TOKENS`` branch from
    ``scalar()`` -- 7 of the rows below return a string and the first node
    fails, while the second stays green (which is what makes them separate
    nodes)."""

    REFUSED: tuple[tuple[str, str], ...] = (
        ("value key",           "k: =\n"),
        ("merge key",           "k: <<\n"),
        ("complex key opener",  "k: ? x\n"),
        ("bare question mark",  "k: ?\n"),
        ("value key in a list", "modules:\n  - =\n"),
        ("merge key in a list", "modules:\n  - <<\n"),
        ("complex key in list", "modules:\n  - ? x\n"),
    )

    #: The lookalikes.  These are ordinary plain scalars to PyYAML, so
    #: refusing them would be over-refusal -- a real profile broken to close a
    #: hazard it never had.
    ACCEPTED: tuple[str, ...] = (
        "k: ==\n", "k: =x\n", "k: <<x\n", "k: ?x\n",
        "k: a=b\n", "k: a<<b\n", "k: a?b\n",
    )

    def test_the_resolver_tokens_refuse_where_the_oracle_refuses(self) -> None:
        yaml = _oracle()
        for label, text in self.REFUSED:
            try:
                oracle = yaml.safe_load(text)
            except Exception:  # noqa: BLE001 -- ConstructorError / ScannerError
                oracle = "<raised>"
            message = _refusal(text)
            assert "profile.yml:" in message, (label, message)
            assert oracle in ("<raised>", {"modules": [{"x": None}]}), (
                f"{label}: the oracle now returns {oracle!r}; this row no "
                "longer models the hazard it was written for"
            )

    def test_the_lookalikes_stay_accepted(self) -> None:
        yaml = _oracle()
        for text in self.ACCEPTED:
            assert _minimal_yaml_parse(text) == yaml.safe_load(text), text


# ---------------------------------------------------------------------------
# Chunk C -- the closed key set, the derived whitelist, the reserved `schema`
# ---------------------------------------------------------------------------

class TestRecognizedProfileKeys:
    """C6: the recognized set is **derived**.  The expected value is rebuilt
    here from the three source definitions read independently -- asserting the
    constant against itself would be the oracle collapse in a different
    costume."""

    def test_the_set_is_the_union_of_its_three_sources_plus_schema(self) -> None:
        from bootstrap._scaffold.config import (  # noqa: PLC0415
            KNOWN_TOKENS, RECOGNIZED_PROFILE_KEYS, _AXES,
        )
        structural = {"preset", "modules", "modules_add", "modules_remove",
                      "forge"}
        expected = set(KNOWN_TOKENS) | set(_AXES) | structural | {"schema"}
        assert set(RECOGNIZED_PROFILE_KEYS) == expected
        # the three sources union to 16; with the reserved key, 17
        assert len(set(KNOWN_TOKENS) | set(_AXES) | structural) == 16
        assert len(RECOGNIZED_PROFILE_KEYS) == 17

    def test_unrecognized_profile_keys_is_pure_and_sorted(self) -> None:
        from bootstrap._scaffold.config import (  # noqa: PLC0415
            unrecognized_profile_keys,
        )
        cfg = {"project_name": "X", "zeta": 1, "alpha": 2, "preset": "p"}
        before = dict(cfg)
        assert unrecognized_profile_keys(cfg) == ["alpha", "zeta"]
        assert cfg == before, "the check must not mutate the config"
        assert unrecognized_profile_keys({"project_name": "X"}) == []


#: The four measured typo rows.  ``module_add:`` is the sharpest: at HEAD it
#: produced ``--summary`` output byte-identical to a correct run, and the
#: module it silently dropped was ``security-review``.
_TYPO_ROWS: tuple[tuple[str, str], ...] = (
    ("presets", 'project_name: "T"\npresets: solo-greenfield\n'),
    ("module_add",
     'project_name: "T"\npreset: high-rigor-legacy\nmodule_add:\n  - examples-gallery\n'),
    ("agent_teams",
     'project_name: "T"\npreset: solo-greenfield\nagent_teams: single\n'),
    ("project_nmae", 'project_nmae: "T"\npreset: solo-greenfield\n'),
)


class TestUnknownKeysRefuseBeforeAnyWrite:
    """C7: no profile key is honoured or discarded without being named."""

    def _run(self, args: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(CAIRN_ROOT / "bootstrap" / "scaffold.py"), *args],
            capture_output=True, text=True, cwd=str(CAIRN_ROOT),
        )

    @pytest.mark.parametrize("key,text", _TYPO_ROWS, ids=[r[0] for r in _TYPO_ROWS])
    def test_summary_refuses_and_names_the_key(
        self, tmp_path: Path, key: str, text: str,
    ) -> None:
        cfg = tmp_path / "profile.yml"
        cfg.write_text(text, encoding="utf-8")
        result = self._run(["--summary", "--config", str(cfg)])
        assert result.returncode != 0, result.stdout
        assert key in result.stderr, result.stderr
        assert "unrecognized profile key" in result.stderr, result.stderr

    @pytest.mark.parametrize("key,text", _TYPO_ROWS, ids=[r[0] for r in _TYPO_ROWS])
    def test_a_real_install_refuses_with_nothing_written(
        self, tmp_path: Path, key: str, text: str,
    ) -> None:
        cfg = tmp_path / "profile.yml"
        cfg.write_text(text, encoding="utf-8")
        target = tmp_path / "target"
        target.mkdir()
        result = self._run(["--config", str(cfg), "--target", str(target)])
        assert result.returncode != 0, result.stdout
        assert key in result.stderr, result.stderr
        assert list(target.iterdir()) == [], (
            "the refusal must land BEFORE any write; found "
            f"{[p.name for p in target.iterdir()]}"
        )

    def test_the_recognized_set_is_printed_with_the_refusal(
        self, tmp_path: Path,
    ) -> None:
        cfg = tmp_path / "profile.yml"
        cfg.write_text(_TYPO_ROWS[0][1], encoding="utf-8")
        result = self._run(["--summary", "--config", str(cfg)])
        for recognized in ("project_name", "preset", "modules_add", "schema"):
            assert recognized in result.stderr, result.stderr


class TestReservedSchemaKey:
    """C8: ``schema`` is read **first**, so a profile from a future engine
    refuses with the version message rather than an unknown-key list.  Without
    that ordering the reserved key buys nothing."""

    def _load(self, tmp_path: Path, text: str):
        from bootstrap._scaffold.config import load_config  # noqa: PLC0415
        path = tmp_path / "profile.yml"
        path.write_text(text, encoding="utf-8")
        return load_config(path)

    def test_schema_1_is_accepted_and_ignored(self, tmp_path: Path) -> None:
        cfg = self._load(tmp_path, "schema: 1\nproject_name: T\n")
        assert cfg == {"schema": 1, "project_name": "T"}

    def test_an_absent_schema_is_accepted(self, tmp_path: Path) -> None:
        assert self._load(tmp_path, "project_name: T\n") == {"project_name": "T"}

    def test_schema_2_refuses_with_the_version_message(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError) as exc:
            self._load(tmp_path, "schema: 2\nproject_name: T\n")
        message = str(exc.value)
        assert "declares schema 2" in message, message
        assert "understands 1" in message, message
        assert "unrecognized profile key" not in message, message

    def test_the_version_message_wins_over_the_unknown_key_message(
        self, tmp_path: Path,
    ) -> None:
        """The ordering is the whole point: a future profile carries both a
        future ``schema`` *and* keys this engine has never heard of."""
        with pytest.raises(ValueError) as exc:
            self._load(tmp_path, "schema: 2\nproject_name: T\nfuture_key: X\n")
        message = str(exc.value)
        assert "declares schema 2" in message, message
        assert "future_key" not in message, message


# ---------------------------------------------------------------------------
# Chunk D -- the drift gate: a marked corpus, both writers, and two canaries
# ---------------------------------------------------------------------------

_BOOTSTRAP_MD = CAIRN_ROOT / "bootstrap" / "BOOTSTRAP.md"
_CORPUS_MARKER = "<!-- cairn-parity-corpus: {name} -->"
#: The ``--help`` corpus entry anchors on an existing literal line inside
#: ``cli.__doc__`` -- **no adopter-visible marker is added to ``--help``**.
_HELP_ANCHOR = "# Inline token values (mechanical substitution)"


def _marked_fence(text: str, name: str) -> str:
    """The fenced ```yaml block immediately after the named corpus marker.

    The marker must appear **exactly once**: a corpus defined by an explicit
    marker cannot silently gain or lose a member the way a shape heuristic
    can, and a deleted marker fails here rather than quietly shrinking the
    corpus."""
    marker = _CORPUS_MARKER.format(name=name)
    assert text.count(marker) == 1, (
        f"expected exactly one {marker!r} in BOOTSTRAP.md, found "
        f"{text.count(marker)}"
    )
    rest = text[text.index(marker) + len(marker):]
    start = rest.index("```yaml") + len("```yaml")
    return rest[start:rest.index("```", start)].lstrip("\n")


def _help_block() -> str:
    """The profile example inside ``cli.__doc__``, at its **raw** four-space
    indentation -- which is exactly the copy-paste-out-of-a-rendered-page shape
    the grammar has to accept."""
    from bootstrap._scaffold import cli  # noqa: PLC0415
    doc = cli.__doc__ or ""
    assert doc.count(_HELP_ANCHOR) == 1, (
        f"expected exactly one {_HELP_ANCHOR!r} in cli.__doc__, found "
        f"{doc.count(_HELP_ANCHOR)}"
    )
    lines = doc.splitlines()
    start = next(i for i, line in enumerate(lines)
                 if line.strip() == _HELP_ANCHOR)
    out: list[str] = []
    for line in lines[start:]:
        if line.strip() and not line.startswith("    "):
            break
        out.append(line)
    return "\n".join(out).rstrip() + "\n"


def _writer_outputs(tmp_path: Path) -> dict[str, str]:
    """Both engine writers' **real** output, produced by calling them into a
    temp tree.  Never reconstructed by the test: the first revision of this
    scope verified the init-lock writer against a *synthesized* template and
    the claim was true of the synthesis and false of the writer."""
    from bootstrap._scaffold.upgrade import (  # noqa: PLC0415
        _PROFILE_REL, _self_heal_profile_config,
        _write_init_lock_profile_template,
    )
    out: dict[str, str] = {}

    # (1) init-lock template with ONE installed module ...
    one = tmp_path / "one"
    (one / "dev" / "modules").mkdir(parents=True)
    (one / "dev" / "modules" / "claim-check.md").write_text("x", encoding="utf-8")
    _write_init_lock_profile_template(one)
    out["init-lock:one-module"] = (one / _PROFILE_REL).read_text(encoding="utf-8")

    # (2) ... and with ZERO installed modules (a bare `modules:` with nothing
    # under it -- the shape whose old reading, `[]` rather than None, was the
    # writer's own divergence from PyYAML).
    zero = tmp_path / "zero"
    (zero / "dev" / "modules").mkdir(parents=True)
    _write_init_lock_profile_template(zero)
    out["init-lock:zero-modules"] = (zero / _PROFILE_REL).read_text(encoding="utf-8")

    # (3) self-heal, with an apostrophe in BOTH a project_name and a
    # test_command -- the single-quoted `''` doubling the writer emits.
    healed = tmp_path / "healed"
    healed.mkdir()
    assert _self_heal_profile_config(healed, {
        "profile": {
            "preset": "collaborative-team",
            "axes": {
                "age": "greenfield", "size": "medium", "complexity": "moderate",
                "language": "single", "human_team": "small-multi",
                "agent_team": "concurrent-multi-type",
            },
        },
        "tokens": {
            "project_name": "O'Brien Lab Model",
            "test_command": "pytest -k 'not slow'",
        },
        "modules": ["claim-check", "reflections"],
    })
    out["self-heal:apostrophes"] = (healed / _PROFILE_REL).read_text(
        encoding="utf-8")
    return out


class TestParityCorpusSweep:
    """D1-D4: everything Cairn ships, writes or documents, through the
    recognizer, against PyYAML as the oracle.

    This is the piece the 2026-07-11 prose-only remedy lacked, and the reason
    the identical defect was still shipping 23 days later.

    **Channel accounting, per input**: the documentation text arrives from the
    shipped Markdown and from ``cli.__doc__`` read at import; the writer
    entries arrive from **calling the real writers** into a temp tree; the
    oracle arrives from ``import yaml``.  None of the three is produced by the
    function under test.
    """

    def test_the_whole_corpus_parses_identically_to_the_oracle(
        self, tmp_path: Path,
    ) -> None:
        yaml = _oracle()

        # The canaries are checked FIRST, in this same node: a sweep run on an
        # interpreter where the oracle has collapsed would report "no
        # divergence" and the record would say the defect did not reproduce.
        import datetime  # noqa: PLC0415
        assert isinstance(yaml.safe_load("d: 2024-01-01")["d"], datetime.date), (
            "oracle-identity canary: yaml.safe_load no longer returns a "
            "datetime.date -- the oracle is not PyYAML"
        )
        assert yaml.safe_load("modules: [a, b]\n") == {"modules": ["a", "b"]}
        with pytest.raises(ValueError):
            _minimal_yaml_parse("modules: [a, b]\n")

        bootstrap_md = _BOOTSTRAP_MD.read_text(encoding="utf-8")
        corpus: dict[str, str] = {
            "BOOTSTRAP.md:appendix-b-example":
                _marked_fence(bootstrap_md, "appendix-b-example"),
            "BOOTSTRAP.md:preset-example":
                _marked_fence(bootstrap_md, "preset-example"),
            "cli.__doc__:--help": _help_block(),
        }
        for name in sorted(CAIRN_ROOT.glob("bootstrap/profiles/*.yml")):
            corpus[f"profiles/{name.name}"] = name.read_text(encoding="utf-8")
        corpus.update(_writer_outputs(tmp_path))

        assert len(corpus) >= 8, sorted(corpus)
        for name, text in corpus.items():
            assert _minimal_yaml_parse(text) == yaml.safe_load(text), (
                f"{name} parses differently under the recognizer and the "
                f"oracle:\n{text}"
            )

    def test_every_corpus_entry_survives_load_config(self, tmp_path: Path) -> None:
        """The corpus is not only *parseable* -- it passes the closed key set
        too, so the documentation Cairn ships is a profile an adopter can
        actually install."""
        from bootstrap._scaffold.config import load_config  # noqa: PLC0415

        bootstrap_md = _BOOTSTRAP_MD.read_text(encoding="utf-8")
        texts = [
            _marked_fence(bootstrap_md, "appendix-b-example"),
            _marked_fence(bootstrap_md, "preset-example"),
            _help_block(),
            *(p.read_text(encoding="utf-8")
              for p in sorted(CAIRN_ROOT.glob("bootstrap/profiles/*.yml"))),
            *_writer_outputs(tmp_path).values(),
        ]
        for index, text in enumerate(texts):
            path = tmp_path / f"corpus-{index}.yml"
            path.write_text(text, encoding="utf-8")
            load_config(path)

    def test_the_apostrophe_round_trip_is_the_writers_own(
        self, tmp_path: Path,
    ) -> None:
        """D3, sharpened: the value the writer wrote comes back **unchanged**.
        Perturbation: delete the ``''`` -> ``'`` unescape and this fails while
        the sweep above still passes on the other entries."""
        from bootstrap._scaffold.config import load_config  # noqa: PLC0415
        written = _writer_outputs(tmp_path)["self-heal:apostrophes"]
        path = tmp_path / "healed.yml"
        path.write_text(written, encoding="utf-8")
        cfg = load_config(path)
        assert cfg["project_name"] == "O'Brien Lab Model"
        assert cfg["test_command"] == "pytest -k 'not slow'"

    def test_the_zero_module_writer_emits_a_bare_key(self, tmp_path: Path) -> None:
        """The init-lock writer's zero-modules shape reads as ``None``, the
        faithful reading -- not ``[]``, which is the *explicit* opt-out."""
        yaml = _oracle()
        text = _writer_outputs(tmp_path)["init-lock:zero-modules"]
        assert _minimal_yaml_parse(text)["modules"] is None
        assert yaml.safe_load(text)["modules"] is None


class TestNoRuntimeYamlDependency:
    """D5: the engine takes the same path with and without PyYAML, because
    since the Maintainer amendment there is only one runtime parser."""

    _DRIVER = (
        "import sys\n"
        "sys.modules['yaml'] = None\n"
        "sys.path.insert(0, {root!r})\n"
        "from bootstrap.scaffold import main\n"
        "sys.exit(main({argv!r}))\n"
    )

    def _install(self, text: str, tmp_path: Path, name: str, block_yaml: bool):
        cfg = tmp_path / f"{name}.yml"
        cfg.write_text(text, encoding="utf-8")
        target = tmp_path / name
        target.mkdir()
        argv = ["--config", str(cfg), "--target", str(target)]
        if block_yaml:
            driver = self._DRIVER.format(root=str(CAIRN_ROOT), argv=argv)
            proc = subprocess.run([sys.executable, "-c", driver],
                                  capture_output=True, text=True,
                                  cwd=str(CAIRN_ROOT))
        else:
            proc = subprocess.run(
                [sys.executable,
                 str(CAIRN_ROOT / "bootstrap" / "scaffold.py"), *argv],
                capture_output=True, text=True, cwd=str(CAIRN_ROOT))
        assert proc.returncode == 0, proc.stderr
        return target

    def _tree(self, root: Path) -> dict[str, bytes]:
        return {
            str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()
        }

    @pytest.mark.parametrize("entry", ["help", "preset"])
    def test_both_parser_paths_install_byte_identical_trees(
        self, tmp_path: Path, entry: str,
    ) -> None:
        if entry == "help":
            text = _help_block()
        else:
            text = _marked_fence(
                _BOOTSTRAP_MD.read_text(encoding="utf-8"), "preset-example")
        with_yaml = self._install(text, tmp_path, f"{entry}-with", False)
        without = self._install(text, tmp_path, f"{entry}-without", True)
        assert self._tree(with_yaml) == self._tree(without)

    def test_importing_the_engine_never_imports_yaml(self) -> None:
        """The amendment, asserted directly: PyYAML is a **test-only** oracle,
        so importing the engine must not pull it in.  Perturbation: restore the
        ``try: import yaml`` selection in ``config.py`` and this fails."""
        driver = (
            "import sys\n"
            f"sys.path.insert(0, {str(CAIRN_ROOT)!r})\n"
            "import bootstrap.scaffold\n"
            "print('yaml' in sys.modules)\n"
        )
        proc = subprocess.run([sys.executable, "-c", driver],
                              capture_output=True, text=True,
                              cwd=str(CAIRN_ROOT))
        assert proc.returncode == 0, proc.stderr
        assert proc.stdout.strip() == "False", (
            "importing the engine imported PyYAML; the recognizer is supposed "
            "to be the sole runtime parser"
        )
