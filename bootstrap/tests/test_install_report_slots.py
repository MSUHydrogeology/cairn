"""The install report sorts unfilled block slots by whether the profile
installed a module that fills them.

A slot that a module fills (for example ``coordination-additions``, filled
by ``coordination-tiers``) is work for the adopter only when that module is
installed.  When the profile left the module out, the slot moves from the
main list to a second list that says which module would have filled it and
how to mark it ``N/A``.  Nothing is dropped: both lists together hold every
slot the install wrote.

The report is stdout only.  These tests run the real ``scaffold.py`` for the
behaviour a profile produces, and call ``print_report`` directly only where
the case cannot reach it any other way: no ``modules`` argument, and a scan
of every core template against the report's supplier table.

Promises:
- A slot that a module left out of the profile fills moves to a second list
  that names that module and says to mark the slot N/A.
- The main list and the second list together hold every slot the install
  wrote, each slot once.
- A slot with at least one installed supplier module stays in the main list.
- A team profile keeps the slots of its installed modules in the main list.
- A module name from the profile never appears in the report when it contains
  a bidirectional control character.
- The report shows control characters in slot names as visible escapes.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_install_report_slots.py
"""
from __future__ import annotations

import io
import re
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap._scaffold.install import print_report  # noqa: E402

SCAFFOLD = CAIRN_ROOT / "bootstrap" / "scaffold.py"
PROFILES = CAIRN_ROOT / "bootstrap" / "profiles"
CORE = CAIRN_ROOT / "templates" / "core"
MODULES_DIR = CAIRN_ROOT / "templates" / "modules"

MAIN_HEADING = re.compile(
    r"^Block slots requiring agent attention \((\d+)\):$", re.M
)
SECOND_HEADING = re.compile(
    r"^Slots for modules this profile did not install \((\d+)\):$", re.M
)
SLOT_LINE = re.compile(r"^  (\S+)  \[cairn:slot (\S+)\](.*)$")
CLOSING_LINE = "Mark each `N/A: <reason>`"

# Every slot a module fills, as the report must treat them.
SUPPLIED_SLOTS = {
    "claim-check",
    "reflections",
    "documentation-discipline",
    "documentation-tier-home",
    "security-verification",
    "coordination-additions",
    "role-roster-additions",
}
ROLE_ROSTER_SUPPLIERS = {
    "domain-agents",
    "legacy-agent",
    "security-review",
    "issue-capture",
    "model-selection",
}


def _install(tmp_path: Path, profile_text: str) -> subprocess.CompletedProcess:
    target = tmp_path / "target"
    target.mkdir()
    cfg = tmp_path / "profile.yml"
    cfg.write_text(profile_text, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCAFFOLD), "--config", str(cfg),
         "--target", str(target)],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )


def _profile(name: str) -> str:
    return (PROFILES / name).read_text(encoding="utf-8")


def _report_lists(out: str) -> dict:
    """Split the slot part of a report into its two lists.

    Returns the two headings' counts (None when the list is absent), the
    ``(path, slot, rest-of-line)`` rows of each list and the number of times
    the closing instruction line printed.
    """
    lines = out.splitlines()
    main_at = next(
        (i for i, ln in enumerate(lines) if MAIN_HEADING.match(ln)), None
    )
    second_at = next(
        (i for i, ln in enumerate(lines) if SECOND_HEADING.match(ln)), None
    )

    def rows(start: int | None) -> list[tuple[str, str, str]]:
        found: list[tuple[str, str, str]] = []
        if start is None:
            return found
        for ln in lines[start + 1:]:
            m = SLOT_LINE.match(ln)
            if not m:
                if found:
                    break
                continue
            found.append(m.groups())
        return found

    return {
        "main_count": int(MAIN_HEADING.match(lines[main_at]).group(1))
        if main_at is not None else None,
        "second_count": int(SECOND_HEADING.match(lines[second_at]).group(1))
        if second_at is not None else None,
        "main": rows(main_at),
        "second": rows(second_at),
        "closing": out.count(CLOSING_LINE),
    }


def _print_report_output(target: Path, results, **kwargs) -> str:
    buf = io.StringIO()
    with redirect_stdout(buf):
        print_report(target, [], results, **kwargs)
    return buf.getvalue()


def test_minimal_profile_lists_absent_module_slots_separately(tmp_path):
    proc = _install(tmp_path, _profile("solo-greenfield.yml"))
    assert proc.returncode == 0, proc.stderr
    lists = _report_lists(proc.stdout)

    assert lists["main_count"] == 19
    assert lists["main_count"] == len(lists["main"])
    assert lists["second_count"] == 2
    assert lists["second_count"] == len(lists["second"])
    assert lists["main_count"] + lists["second_count"] == 21

    assert {s for _p, s, _r in lists["second"]} == {
        "coordination-additions", "role-roster-additions",
    }
    assert not {
        "coordination-additions", "role-roster-additions",
    } & {s for _p, s, _r in lists["main"]}

    by_slot = {s: rest for _p, s, rest in lists["second"]}
    assert "coordination-tiers" in by_slot["coordination-additions"]
    for module in ROLE_ROSTER_SUPPLIERS:
        assert module in by_slot["role-roster-additions"]

    assert lists["closing"] == 1


def test_team_profile_keeps_live_module_slots_in_main_list(tmp_path):
    """Pins today's output: every module a team profile needs is installed."""
    proc = _install(tmp_path, _profile("collaborative-team.yml"))
    assert proc.returncode == 0, proc.stderr
    lists = _report_lists(proc.stdout)

    assert lists["main_count"] == 22
    assert lists["main_count"] == len(lists["main"])
    assert lists["second_count"] is None
    assert "did not install" not in proc.stdout
    main_slots = {s for _p, s, _r in lists["main"]}
    assert {"coordination-additions", "role-roster-additions"} <= main_slots


# Declared exception (internal hook): Injects bidi-control and backslash slot names straight into private print_report; shipped core templates cannot carry such names, so no public install.
def test_report_escapes_supplied_slot_names_and_distinguishes_backslashes(tmp_path):
    names = ["visible-slot", "slot\u202e-hidden", r"literal\u202e"]
    results = [(tmp_path / "AGENTS.md", [], names, "installed")]
    out = _print_report_output(tmp_path, results, modules=[])

    assert "visible-slot" in out
    assert "\u202e" not in out
    assert "\\u202e" in out
    assert r"literal\\u202e" in out


def test_removing_a_module_moves_every_slot_it_fills(tmp_path):
    proc = _install(
        tmp_path,
        _profile("solo-greenfield.yml")
        + "modules_remove:\n"
        "  - documentation-plan\n"
        "  - claim-check\n"
        "  - reflections\n"
        "  - security-verification\n",
    )
    assert proc.returncode == 0, proc.stderr
    lists = _report_lists(proc.stdout)

    second = {(p, s) for p, s, _r in lists["second"]}
    assert second >= {
        ("AGENTS.md", "claim-check"),
        ("AGENTS.md", "documentation-discipline"),
        ("AGENTS.md", "security-verification"),
        ("dev/agent_collaboration.md", "reflections"),
        ("dev/proposals/_template.md", "documentation-tier-home"),
        ("dev/plans/_template.md", "documentation-tier-home"),
    }
    assert second.isdisjoint({(p, s) for p, s, _r in lists["main"]})
    assert lists["main_count"] + lists["second_count"] == 21


def test_a_slot_with_any_installed_supplier_stays_in_main_list(tmp_path):
    """One of the five role-roster suppliers is enough to keep the slot live.

    A rule of "every supplier must be installed" would move it to the second
    list here, and this test is the one that notices.
    """
    proc = _install(
        tmp_path, _profile("solo-greenfield.yml") + "modules_add:\n  - legacy-agent\n"
    )
    assert proc.returncode == 0, proc.stderr
    lists = _report_lists(proc.stdout)

    assert "role-roster-additions" in {s for _p, s, _r in lists["main"]}
    assert "role-roster-additions" not in {s for _p, s, _r in lists["second"]}


def test_profile_module_name_with_bidi_character_is_absent_from_the_report(
    tmp_path,
):
    """The report prints module names from its own table, never the profile's.

    The profile loader refuses control characters, so an escape byte never
    reaches the report; a right-to-left override does, because the loader
    admits it.  Pins today's behaviour: no name from the profile is printed.
    """
    hostile = "zz-hostile\u202e"
    proc = _install(
        tmp_path, f"project_name: Hostile\ntest_command: pytest\nmodules:\n  - {hostile}\n"
    )
    assert proc.returncode == 0, proc.stderr
    assert "Cairn scaffold complete" in proc.stdout
    report = proc.stdout[proc.stdout.index("Cairn scaffold complete"):]
    assert "zz-hostile" not in report
    assert "\u202e" not in report
