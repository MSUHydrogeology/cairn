"""Neutrality sub-gate -- abuse-test coverage.

Promises:
- The neutrality sub-gate fails on a vendor or project name in scanned prose and passes clean prose.
- A vendor-ok directive exempts only its own line or the line below it, and its reason is printed for audit.
- A vendor-ok-begin and vendor-ok-end pair exempts the names inside it; an unmatched begin or end fails.
- Every exemption directive needs a non-empty rationale, or the gate fails.
- A case-study marker exempts a file only under the case-studies directory; elsewhere it fails.
- Exemption directives are refused under templates, and vendor or project names in templates fail even without one.
- Only the listed file types are scanned; a .py file outside templates is not scanned.
- Names match as whole words, and a directive shown in backticks or prose is not live.

Pins the seven recovery signals from plan-review finding #3:

* Sanctioned exceptions pass with rationale echoed in the report.
* Unsanctioned vendor / project tokens fail.
* A line exemption does NOT bleed to the line after the target line.
* A block exemption WITH matching end works; orphan begin fails.
* Empty rationale fails (rationale required on every directive).
* ``<!-- case-study -->`` exempts a file under ``case-studies/`` but
  FAILS when placed elsewhere.
* ANY exemption directive inside ``templates/`` fails (templates ship
  to adopters; a leak there would propagate).
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
QG_SRC = CAIRN_ROOT / "scripts" / "quality_gate.py"

pytestmark = pytest.mark.skipif(
    not QG_SRC.exists(), reason="quality_gate.py not available",
)


def _load_qg(name: str = "_quality_gate_neutrality_under_test") -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, QG_SRC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def qg() -> ModuleType:
    return _load_qg()


# The names and file types the gate must read, written out here and not read
# back from the checker: a name or type dropped from the checker's own list
# would otherwise leave every test green and the gate reading zero, because
# nothing in the tree uses it any more.
_LISTED_NAMES = (
    "Claude", "Codex", "Anthropic", "OpenAI", "Google", "DeepMind",
    "Microsoft", "Meta", "Gemini", "GPT", "Llama", "LLaMA", "Antigravity",
    "Cursor", "Copilot", "Windsurf", "Cline", "OpenCode",
    "modflow_tools", "LHM",
)
_TEMPLATE_FILE_TYPES = (".md", ".yml", ".yaml", ".py", ".toml", ".json", ".txt")


_EACH_FILE_ONCE = "every file written fails once, on line 1"


def _shipped_type_files() -> dict:
    """One vendor-naming file per file type the installer ships.  A new shipped
    type (a shell-script hook, say) must fail here, not pass the gate unread.
    An empty source file has nothing to scan, so it adds no type."""
    manifest = subprocess.run(
        [sys.executable, str(CAIRN_ROOT / "bootstrap" / "scaffold.py"),
         "--manifest"], capture_output=True, text=True, check=True,
        cwd=CAIRN_ROOT).stdout
    sources = [line.split("\t")[1] for line in manifest.splitlines()
               if line and not line.startswith("#")]
    assert len(sources) > 50
    suffixes = sorted({Path(src).suffix for src in sources
                       if (CAIRN_ROOT / "templates" / src).stat().st_size > 0})
    return {f"templates/core/x{suffix}": "Written with Claude.\n"
            for suffix in suffixes}


_MD = "docs/methodology/"
_TM = "templates/modules/x.md"

# One row per verdict the gate gives.  ``files`` maps a path under the repo
# root to its text (or is a function that builds that map when the test runs).
# ``fails`` lists the (path, line) of every failing finding, once per finding.
# ``printed`` lists the exemption reasons the report must echo for audit.
_VERDICTS = [
    pytest.param(
        {_MD + "leak.md": "Built first in modflow_tools, then ported.\n"},
        [(_MD + "leak.md", 1)], [], id="project-name-in-docs-fails"),
    pytest.param(
        {"bootstrap/tests/test_x.py": "# Ported from modflow_tools' test.\n"
                                      "# Reviewed by Codex.\n"},
        [], [], id="py-outside-templates-is-not-scanned"),
    pytest.param(
        {_MD + "ok.md": "The Claude assistant "
                        "<!-- vendor-ok: case study sentence -->\n"},
        [], ["case study sentence"], id="same-line-directive-exempts"),
    pytest.param(
        {_MD + "ok.md": "<!-- vendor-ok: documented reason -->\n"
                        "The Claude reference here is exempt.\n"},
        [], ["documented reason"], id="directive-above-exempts-next-line"),
    pytest.param(
        {_MD + "leak.md": "<!-- vendor-ok: only the next line -->\n"
                          "Claude exempted by directive above.\n"
                          "Claude on this line is NOT exempted.\n"},
        [(_MD + "leak.md", 3)], ["only the next line"],
        id="line-directive-does-not-bleed"),
    pytest.param(
        {_MD + "bad.md": "<!-- vendor-ok: -->\nClaude here.\n"},
        [(_MD + "bad.md", 1)], [], id="line-directive-needs-a-reason"),
    pytest.param(
        {_MD + "ok.md": "<!-- vendor-ok-begin: section quotes a vendor doc -->\n"
                        "Claude said X.  Codex said Y.\n"
                        "<!-- vendor-ok-end -->\n"
                        "Outside the block: Claude here is NOT exempted.\n"},
        [(_MD + "ok.md", 4)], ["section quotes a vendor doc"],
        id="block-exempts-only-inside"),
    pytest.param(
        {_MD + "orphan.md": "<!-- vendor-ok-begin: forgot to close -->\n"
                            "Claude here.\n"
                            "End of file with no vendor-ok-end.\n"},
        [(_MD + "orphan.md", 1)], [], id="block-begin-without-end-fails"),
    pytest.param(
        {_MD + "orphan.md": "Some prose.\n<!-- vendor-ok-end -->\n"
                            "More prose.\n"},
        [(_MD + "orphan.md", 2)], [], id="block-end-without-begin-fails"),
    pytest.param(
        {_MD + "bad.md": "<!-- vendor-ok-begin: -->\nClaude.\n"
                         "<!-- vendor-ok-end -->\n"},
        [(_MD + "bad.md", 1)], [], id="block-directive-needs-a-reason"),
    pytest.param(
        {"case-studies/modflow_tools.md": "<!-- case-study -->\n"
                                          "# modflow_tools as the reference.\n\n"
                                          "Built with Claude and Codex.\n"},
        [], [], id="case-study-marker-in-case-studies-exempts"),
    pytest.param(
        {_MD + "leak.md": "<!-- case-study -->\n"
                          "Claude here would be exempt if the marker held.\n"},
        [(_MD + "leak.md", 1), (_MD + "leak.md", 2)],
        [], id="case-study-marker-elsewhere-fails-and-exempts-nothing"),
    pytest.param(
        {"templates/modules/team-gated/x.md": "<!-- vendor-ok: docs example -->\n"
                                              "Adopter docs.\n"},
        [("templates/modules/team-gated/x.md", 1)], [],
        id="vendor-ok-directive-in-templates-fails"),
    pytest.param(
        {_TM: "<!-- case-study -->\nTemplated case study.\n"},
        [(_TM, 1)], [], id="case-study-marker-in-templates-fails"),
    pytest.param(
        {_TM: "# Clean template content\n\nNo directives, no names.\n"},
        [], [], id="clean-template-passes"),
    pytest.param(
        {"templates/core/AGENTS.md": "Claude should not ship in a template.\n"},
        [("templates/core/AGENTS.md", 1)], [],
        id="vendor-name-in-template-fails-without-a-directive"),
    pytest.param(
        {"templates/modules/leak.md": "Borrowed from modflow_tools' module.\n"},
        [("templates/modules/leak.md", 1)], [],
        id="project-name-in-template-fails-without-a-directive"),
    pytest.param(
        {_TM: "# A template\n<!-- reviewed by Claude -->\n"},
        [(_TM, 2)], [], id="name-in-a-template-html-comment-fails"),
    pytest.param(
        {_TM: "<!-- vendor-ok: Claude example -->\n"},
        [(_TM, 1), (_TM, 1)], [],
        id="template-directive-that-names-a-vendor-fails-twice"),
    pytest.param(
        {_MD + "howto.md": "# Syntax\n\n"
                           "Wrap a block in `<!-- vendor-ok-begin: ... -->` "
                           "and `<!-- vendor-ok-end -->` -- shown in backticks\n"
                           "so the gate does not treat it as live.\n",
         "docs/howto.md": "# Syntax\n\nA `<!-- case-study -->` marker at the "
                          "file head exempts the whole file.\n"},
        [], [], id="directives-shown-in-backticks-are-not-live"),
    pytest.param(
        {_MD + "ok.md": "<!-- vendor-ok: cite of a real review -->\n"
                        "Codex's pre-cut review was sharp.\n"},
        [], ["cite of a real review"], id="exemption-reason-is-printed"),
    pytest.param(
        {_TM: "Metadata about a Clinelike, Googled, GPTs-free thing.\n"},
        [], [], id="a-name-inside-a-longer-word-is-not-a-hit"),
    pytest.param(
        {_TM: "".join(f"Works with {name} too.\n" for name in _LISTED_NAMES)},
        [(_TM, line) for line in range(1, len(_LISTED_NAMES) + 1)], [],
        id="every-listed-name-is-read"),
    pytest.param(
        {f"templates/core/x{suffix}": "Written with Claude.\n"
         for suffix in _TEMPLATE_FILE_TYPES},
        _EACH_FILE_ONCE, [], id="every-listed-file-type-is-read-in-templates"),
    pytest.param(
        _shipped_type_files, _EACH_FILE_ONCE, [],
        id="every-file-type-the-installer-ships-is-read"),
]


@pytest.mark.parametrize("files, fails, printed", _VERDICTS)
def test_neutrality_gate_verdicts_through_its_cli(
    qg, tmp_path, capsys, files, fails, printed,
):
    """Names fail, exemptions are scoped and need a reason, and templates
    refuse every exemption.  Judged by the exit status, the failing
    (path, line) pairs and the exemption reasons the report echoes."""
    if callable(files):
        files = files()
    if fails == _EACH_FILE_ONCE:
        fails = [(path, 1) for path in files]
    for rel, text in files.items():
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
    code = qg.main(
        ["--sub", "neutrality", "--report", "--root", str(tmp_path)])
    rows = [line.split("\t", 4) for line in capsys.readouterr().out.splitlines()]
    failed = sorted((row[2], int(row[3])) for row in rows if row[1] == "fail")
    echoed = [reason for reason in printed
              if any(reason in row[4] for row in rows if row[1] == "info")]
    assert (code, failed, echoed) == (1 if fails else 0, sorted(fails), printed)
