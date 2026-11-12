"""The profile loader's closed line grammar (`profile-parse-fail-open`).

Every NEW node this plan adds lives here, in a module carrying **no
module-level marker** — the gate manifest records a module-level ``pytestmark``
skipif against every node in the file, so a node added to a marked module reads
as ``SKIP-XFAIL-NEW`` (plan *Gate accounting* item (ii)).

Promises:
- A profile line the reader cannot read refuses with the file, the line number and a rewrite, and never yields a partial profile. (BOOTSTRAP.md Appendix B, "Schema rules")
- The reader accepts the profile forms the docs and shipped profiles use and reads them as a standard YAML reader would. (bootstrap/profiles/*.yml; BOOTSTRAP.md)
- A "#" followed by a space starts a comment, "#" inside a value is kept, and LF, CRLF and CR line endings read the same.
- Invisible Unicode whitespace is never silently removed from a key or value; the reader refuses it or keeps it. (production code: bootstrap/_scaffold/config.py)
- An unknown profile key refuses before anything is written, names the key, and prints the recognized keys. (production code: bootstrap/_scaffold/config.py)
- A profile declaring schema 2 or later is refused with a version message; schema 1 or no schema is accepted. (BOOTSTRAP.md Appendix B, "Schema rules")
- An upgrade that cannot use the committed profile says why on stderr and keeps the lockfile's profile; a readable profile stays silent. (production code: bootstrap/_scaffold/upgrade.py)
- Install and summary produce the same tree with or without PyYAML, and importing the engine does not import PyYAML. (production code: bootstrap/_scaffold/config.py)

Four properties are under test:

* **Chunk A** — ``upgrade --plan``'s lockfile fallback is *audible*:
  it names what it swallowed on stderr and still plans under the lockfile
  profile.
* **Chunk B** — the profile reader is a **recognizer**: every non-blank
  line matches one of the eight accepted forms or the profile is refused with
  ``<path>:<line>: <reason>`` and a rewrite.  Totality is asserted through
  ``--summary`` and a real install (every refused profile exits non-zero and
  leaves the target empty); soundness against PyYAML is Chunk D.
* **Chunk C** — an unrecognized profile key **refuses before any write**; the
  recognized set is *derived*, never hand-maintained; a reserved ``schema`` key
  is read first so a future engine can say "this profile declares schema N".
* **Chunk D** — a drift gate over a **marker-defined corpus** of everything
  Cairn ships, writes or documents, read through ``load_config`` with LF, CRLF
  and CR line endings and asserted equal to ``yaml.safe_load``, with an
  oracle-identity canary and a divergence canary so the gate cannot pass
  vacuously.

**The oracle arrives by a channel that is not the artifact.** Every parity
assertion imports ``yaml`` directly.  ``_yaml_load`` is **banned as an
oracle**: since the Maintainer amendment of 2026-08-03 it is a compatibility
alias for the in-tree recognizer, so ``_yaml_load(x) == _minimal_yaml_parse(x)``
compares the function under test to itself.  The two former self-oracles in
``bootstrap/tests/test_presets.py`` are gone; no ``_yaml_load`` oracle remains
there.

**PyYAML absent is a failure, not a skip** (Maintainer amendment: *"make an
absent PyYAML oracle an explicit non-green condition rather than a skipped
test"*).  A skipped parity node takes both canaries with it and nothing in the
suite notices.
"""
from __future__ import annotations

import contextlib
import io
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parents[2]
if str(CAIRN_ROOT) not in sys.path:
    sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap._scaffold.config import (  # noqa: E402
    ProfileGrammarError,
    load_config,
)
from bootstrap.scaffold import main  # noqa: E402


# ---------------------------------------------------------------------------
# Chunk A -- the upgrade-path fallback stops swallowing
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def installed_project(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A solo-greenfield project installed once, then copied per case."""
    root = tmp_path_factory.mktemp("installed")
    cfg = root / "install-profile.yml"
    cfg.write_text(
        "project_name: Demo\ntest_command: pytest\npreset: solo-greenfield\n",
        encoding="utf-8",
    )
    target = root / "project"
    target.mkdir()
    assert main([
        "--config", str(cfg), "--target", str(target),
        "--cairn-root", str(CAIRN_ROOT), "--allow-dev",
    ]) == 0
    return target


def _upgrade_plan(target: Path) -> tuple[int, str, str]:
    """``upgrade --plan`` on *target*: exit status, stdout, stderr."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = main(["upgrade", "--plan", "--target", str(target),
                   "--cairn-root", str(CAIRN_ROOT)])
    return rc, out.getvalue(), err.getvalue()


@pytest.fixture(scope="module")
def plan_without_a_profile(installed_project: Path) -> str:
    """The plan for the installed project, which has no committed profile."""
    assert not (installed_project / "dev" / ".cairn" / "profile.yml").exists()
    rc, plan, _err = _upgrade_plan(installed_project)
    assert rc == 0
    return plan


#: ``(label, bytes of the committed profile, what stderr must name)``.  The
#: last row is a profile the upgrade can use: it must stay silent.
_COMMITTED_PROFILES = (
    ("not-utf-8", b"project_name: \xff\xfe not utf-8\n",
     ("UnicodeDecodeError",)),
    ("nested-mapping", b"parent:\n  child: val\n", ("profile.yml:2:",)),
    ("missing-and-invalid-axes",
     b"project_name: Demo\ntest_command: pytest\nage: greenfield\n"
     b"size: not-a-real-size\n", ("size", "complexity")),
    ("readable",
     b"project_name: Demo\ntest_command: pytest\npreset: solo-greenfield\n",
     ()),
)


@pytest.mark.parametrize(
    "content,causes", [pytest.param(c, k, id=i) for i, c, k in _COMMITTED_PROFILES],
)
def test_an_upgrade_that_cannot_use_the_committed_profile_says_why_and_carries_on(
    tmp_path: Path, installed_project: Path, plan_without_a_profile: str,
    content: bytes, causes: tuple[str, ...],
) -> None:
    """``upgrade --plan`` falls back to the lockfile's profile, so its plan is
    the one it prints with no committed profile at all; it names the profile
    and the cause on stderr when it fell back, and says nothing when it did
    not.  (The plan text does not change with the profile, so "plan
    unchanged" only shows the fallback does not disturb it.)"""
    target = tmp_path / "project"
    shutil.copytree(installed_project, target)
    (target / "dev" / ".cairn" / "profile.yml").write_bytes(content)

    rc, plan, err = _upgrade_plan(target)

    assert {
        "rc": rc,
        "silent": err == "",
        "profile named": "dev/.cairn/profile.yml" in err,
        "causes missing": [c for c in causes if c not in err],
        "plan unchanged": plan == plan_without_a_profile,
    } == {
        "rc": 0,
        "silent": not causes,
        "profile named": bool(causes),
        "causes missing": [],
        "plan unchanged": True,
    }


# ---------------------------------------------------------------------------
# Shared helper -- the independent oracle
# ---------------------------------------------------------------------------

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


#: Every codepoint Python calls whitespace, enumerated **from the running
#: interpreter's Unicode tables** rather than listed -- **29** of them on
#: CPython 3.13.13 (``as_of 2026-08-04``; the number is the interpreter's, and
#: that it is the interpreter's is the point).
#:
#: YAML's own whitespace is only SPACE (``U+0020``) and TAB (``U+0009``), which
#: leaves **27** others -- but they are *not* one homogeneous class, and the
#: difference is what the hidden-whitespace sweep below has to survive.  Measured by probing
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
#:   tokenizer holds these; a separate control-character scan does, so they are
#:   refused with their codepoint named like the rest.
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


# ---------------------------------------------------------------------------
# A profile that cannot be read or honoured is refused before any write
# ---------------------------------------------------------------------------

#: ``(label, text, expected line number)``.  Contains every row from the
#: four families that broke earlier parsers: empty / indented lines,
#: comments, the writers' own output shapes, and truncation / folded
#: blocks.  Each row is named, so a failure says which family regressed.
_MALFORMED_ROWS: tuple[tuple[str, str, int], ...] = (
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
    # the invisible-whitespace sweep below.
    ("I4 BOM", "\ufeffproject_name: X\n", 1),
    ("I4 NUL", "project_name: a\x00b\n", 1),
    ("I4 ESC", "project_name: a\x1bb\n", 1),
    ("I4 backspace", "project_name: a\x08b\n", 1),
    ("I4 trailing text after quote", "project_name: 'a' junk\n", 1),
    ("I4 dedented key", "  project_name: X\npreset: solo\n", 2),
    ("I4 bare word line", "project_name: X\njust-a-word\n", 2),
)

#: ``=`` is the YAML value key, ``<<`` the merge key and ``?`` opens a complex
#: key: a YAML reader refuses all three, so a reader that took them for text
#: would hand back a value where the oracle refuses.  ``(label, text, line)``.
_RESOLVER_ROWS: tuple[tuple[str, str, int], ...] = (
    ("value key", "k: =\n", 1),
    ("merge key", "k: <<\n", 1),
    ("complex key opener", "k: ? x\n", 1),
    ("bare question mark", "k: ?\n", 1),
    ("value key in a list", "modules:\n  - =\n", 2),
    ("merge key in a list", "modules:\n  - <<\n", 2),
    ("complex key in a list", "modules:\n  - ? x\n", 2),
)

#: Well-formed lines that name something the engine does not have, or a scalar
#: where a list belongs.  ``(label, text, the word the refusal must name)``.
_UNHONOURABLE_ROWS: tuple[tuple[str, str, str], ...] = (
    ("unknown preset", "project_name: T\npreset: nonesuch\n", "nonesuch"),
    ("unknown module",
     "project_name: T\npreset: solo-greenfield\nmodules_add:\n  - no-such-mod\n",
     "no-such-mod"),
    ("unknown axis value",
     "project_name: T\npreset: solo-greenfield\nagent_team: bogus\n", "bogus"),
    ("scalar where a list belongs",
     "project_name: T\npreset: solo-greenfield\nmodules_add: security-review\n",
     "modules_add"),
)

#: SPACE and TAB are YAML's own whitespace, and the two line ends separate
#: lines; every OTHER whitespace codepoint is a hidden character.
_YAML_BLANKS = frozenset(" \t\n\r")


def _refusal_cases() -> list:
    """``(text, strings the refusal must name)`` pairs, grouped per param."""
    cases = [
        pytest.param(((text, (f"profile.yml:{line}:",)),), id=label)
        for label, text, line in (*_MALFORMED_ROWS, *_RESOLVER_ROWS)
    ]
    cases += [
        pytest.param(((text, (word,)),), id=label)
        for label, text, word in _UNHONOURABLE_ROWS
    ]
    for char in _ISSPACE_CODEPOINTS:
        if char in _YAML_BLANKS:
            continue
        codepoint = f"U+{ord(char):04X}"
        cases.append(pytest.param(tuple(
            (template.format(c=char),
             (f"profile.yml:{template.split('{c}')[0].count(chr(10)) + 1}:",
              codepoint))
            for _label, template in _INVISIBLE_POSITIONS
        ), id=f"hidden whitespace {codepoint}"))
    return cases


@pytest.mark.parametrize("pairs", _refusal_cases())
def test_a_profile_that_cannot_be_read_or_honoured_is_refused_before_any_write(
    tmp_path: Path, capsys, pairs: tuple,
) -> None:
    """Through ``--summary`` and through a real install, each profile text
    exits non-zero, names its line (and the codepoint, for hidden whitespace)
    or the offending word, and leaves the target empty."""
    wrong: list = []
    for number, (text, named) in enumerate(pairs):
        work = tmp_path / str(number)
        target = work / "target"
        target.mkdir(parents=True)
        cfg = work / "profile.yml"
        cfg.write_bytes(text.encode("utf-8"))
        seen: dict = {}
        for entry, argv in (
            ("summary", ["--summary", "--config", str(cfg)]),
            ("install", ["--config", str(cfg), "--target", str(target),
                         "--cairn-root", str(CAIRN_ROOT), "--allow-dev"]),
        ):
            capsys.readouterr()
            rc = main(argv)
            err = capsys.readouterr().err
            seen[entry] = (rc != 0, [n for n in named if n not in err])
        seen["target"] = [p.name for p in target.iterdir()]
        if seen != {"summary": (True, []), "install": (True, []), "target": []}:
            wrong.append((text, seen))
    assert wrong == []


# ---------------------------------------------------------------------------
# Chunk C -- the closed key set, the derived whitelist, the reserved `schema`
# ---------------------------------------------------------------------------


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
    """No profile key is honoured or discarded without being named."""

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
    """``schema`` is read **first**, so a profile from a future engine
    refuses with the version message rather than an unknown-key list.  Without
    that ordering the reserved key buys nothing."""

    def _load(self, tmp_path: Path, text: str):
        from bootstrap._scaffold.config import load_config  # noqa: PLC0415
        path = tmp_path / "profile.yml"
        path.write_text(text, encoding="utf-8")
        return load_config(path)


    def test_schema_2_refuses_with_the_version_message(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError) as exc:
            self._load(tmp_path, "schema: 2\nproject_name: T\n")
        message = str(exc.value)
        assert "declares schema 2" in message, message
        assert "understands 1" in message, message
        assert "unrecognized profile key" not in message, message


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


#: ``#`` opens a comment only at the start of a value or after a space; inside
#: a value it is kept.  (A tab is refused outright, which has its own row in
#: ``_MALFORMED_ROWS``.)
_HASH_PROFILES: tuple[str, ...] = (
    "forge: gitlab   # gitlab | github\n",
    "modules:\n  - lifecycle-metrics  # always on\n",
    "project_name: X\nmodules:  # nothing selected\n",
    "project_name: a#b\n",
    "project_name: issue#42-tracker\n",
    "test_command: pytest -k not-slow#fast\n",
    "modules:\n  - mod#1\n",
)

#: Quoting, comment and list shapes, to be read with every line ending.
_LINE_ENDING_PROFILES: tuple[str, ...] = (
    "project_name: X\ntest_command: pytest\n",
    "forge: gitlab   # note\nproject_name: X\n",
    'project_name: "My Project"\n',
    "project_name: 'O''Brien'\n",
    "modules:\n  - a\n  - b\n",
    "project_name: 'a  '\n",
)


@pytest.mark.parametrize("eol", ["\n", "\r\n", "\r"], ids=["lf", "crlf", "cr"])
def test_shipped_documented_and_written_profiles_read_as_yaml_reads_them(
    tmp_path: Path, eol: str,
) -> None:
    """``load_config`` returns exactly what ``yaml.safe_load`` returns for
    every profile Cairn ships, documents or writes, and for the ``#`` and
    quoting cases, with LF, CRLF and CR line endings."""
    yaml = _oracle()

    # Canaries, so the comparison below cannot pass vacuously: the oracle is
    # PyYAML (it turns a date into a date), and a form the oracle reads but
    # the reader does not accept is refused rather than read differently.
    import datetime  # noqa: PLC0415
    assert isinstance(yaml.safe_load("d: 2024-01-01")["d"], datetime.date), (
        "oracle-identity canary: yaml.safe_load no longer returns a "
        "datetime.date -- the oracle is not PyYAML"
    )
    flow = tmp_path / "flow.yml"
    flow.write_text("modules: [a, b]\n", encoding="utf-8")
    assert yaml.safe_load(flow.read_text(encoding="utf-8")) == {
        "modules": ["a", "b"]}
    with pytest.raises(ValueError):
        load_config(flow)

    bootstrap_md = _BOOTSTRAP_MD.read_text(encoding="utf-8")
    corpus: dict[str, str] = {
        "BOOTSTRAP.md:appendix-b-example":
            _marked_fence(bootstrap_md, "appendix-b-example"),
        "BOOTSTRAP.md:preset-example":
            _marked_fence(bootstrap_md, "preset-example"),
        "cli.__doc__:--help": _help_block(),
    }
    for path in sorted(CAIRN_ROOT.glob("bootstrap/profiles/*.yml")):
        corpus[f"profiles/{path.name}"] = path.read_text(encoding="utf-8")
    corpus.update(_writer_outputs(tmp_path / "writers"))
    for index, text in enumerate(_HASH_PROFILES):
        corpus[f"hash-case-{index}"] = text
    for index, text in enumerate(_LINE_ENDING_PROFILES):
        corpus[f"line-ending-case-{index}"] = text
    assert len(corpus) >= 8, sorted(corpus)

    differ: dict[str, str] = {}
    for index, (name, text) in enumerate(corpus.items()):
        text = text.replace("\n", eol)
        path = tmp_path / f"corpus-{index}.yml"
        path.write_bytes(text.encode("utf-8"))
        try:
            got = load_config(path)
        except ValueError as exc:
            differ[name] = f"refused: {exc}"
            continue
        if got != yaml.safe_load(text):
            differ[name] = f"read {got!r}, the oracle reads {yaml.safe_load(text)!r}"
    assert differ == {}


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


class TestNoRuntimeYamlDependency:
    """The engine takes the same path with and without PyYAML, because
    there is only one runtime parser."""

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
