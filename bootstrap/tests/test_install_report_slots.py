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


def _core_slot_results(target: Path) -> list[tuple[Path, list[str], list[str], str]]:
    """One synthetic install result per core template, holding its slots."""
    results = []
    for path in sorted(CORE.rglob("*.md")):
        slots = re.findall(r"<!-- cairn:slot (\S+) -->", path.read_text("utf-8"))
        if slots:
            results.append(
                (target / path.relative_to(CORE), [], slots, "installed")
            )
    return results


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


def test_report_without_modules_argument_lists_every_slot_in_main_list(tmp_path):
    results = _core_slot_results(tmp_path)
    total = sum(len(r[2]) for r in results)
    out = _print_report_output(tmp_path, results)
    lists = _report_lists(out)

    assert lists["main_count"] == total
    assert len(lists["main"]) == total
    assert lists["second_count"] is None
    assert "did not install" not in out


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


def _placeholders_in_core_templates() -> set[tuple[str, str, str]]:
    """``(template path, slot, module)`` for each "Filled from the" slot.

    The placeholder normally sits inside its slot.  ``security-verification``
    keeps it in the prose just above an empty slot, so a placeholder outside
    every slot belongs to the next slot that opens after it.
    """
    found = set()
    for path in sorted(CORE.rglob("*.md")):
        text = path.read_text("utf-8")
        blocks = [
            (m.start(), m.end(), m.group(1))
            for m in re.finditer(
                r"<!-- cairn:slot (\S+) -->.*?<!-- cairn:end \1 -->", text, re.S
            )
        ]
        for m in re.finditer(r"Filled from the `([^`]+)`", text):
            inside = [b for b in blocks if b[0] <= m.start() < b[1]]
            if inside:
                slot = inside[0][2]
            else:
                after = re.search(r"<!-- cairn:slot (\S+) -->", text[m.end():])
                assert after, f"{path}: placeholder with no slot after it"
                slot = after.group(1)
            found.add((str(path.relative_to(CORE)), slot, m.group(1)))
    return found


def test_every_slot_that_says_filled_from_a_module_is_in_the_supplier_table(
    tmp_path,
):
    """The table is checked against the templates, never against itself.

    A scan that finds nothing would let every slot pass, so the scan must
    first find the six placeholders known to exist.  A placeholder that is
    re-wrapped across a line stops matching and fails this assertion.
    """
    expected = {
        ("AGENTS.md", "claim-check", "claim-check"),
        ("AGENTS.md", "security-verification", "security-verification"),
        ("AGENTS.md", "documentation-discipline", "documentation-plan"),
        ("dev/agent_collaboration.md", "reflections", "reflections"),
        ("dev/proposals/_template.md", "documentation-tier-home",
         "documentation-plan"),
        ("dev/plans/_template.md", "documentation-tier-home",
         "documentation-plan"),
    }
    found = _placeholders_in_core_templates()
    assert found == expected

    out = _print_report_output(
        tmp_path, _core_slot_results(tmp_path), modules=[]
    )
    second = {
        (p, s): rest for p, s, rest in _report_lists(out)["second"]
    }
    for path, slot, module in sorted(found):
        assert (path, slot) in second, f"{slot} in {path} is not in the table"
        named = re.findall(r"[a-z][a-z-]*[a-z]", second[(path, slot)])
        assert module in named, (
            f"{slot} says it is filled from {module}; report names {named}"
        )


def test_supplier_table_names_real_slots_and_real_modules(tmp_path):
    results = _core_slot_results(tmp_path)
    core_slots = {s for r in results for s in r[2]}
    assert SUPPLIED_SLOTS <= core_slots

    out = _print_report_output(tmp_path, results, modules=[])
    second = _report_lists(out)["second"]
    assert {s for _p, s, _r in second} == SUPPLIED_SLOTS

    shipped = {
        p.stem for p in MODULES_DIR.glob("*/*.md")
    }
    for _path, slot, rest in second:
        names = rest.split("supplied by:", 1)[1].split(",")
        assert names, f"{slot} names no module"
        for name in (n.strip() for n in names):
            assert name in shipped, f"{slot} names {name!r}, not a shipped module"


def test_no_ok_line_when_only_module_supplied_slots_are_present(tmp_path):
    """With no module installed and only slots a module fills, the main list is
    empty but the second list is not, so "[OK] No block slots detected." would be
    false.  An install with no slots at all still prints it."""
    only_supplied = [
        (tmp_path / "doc.md", [], sorted(SUPPLIED_SLOTS), "installed")
    ]
    out = _print_report_output(tmp_path, only_supplied, modules=[])
    lists = _report_lists(out)
    assert lists["main_count"] is None
    assert lists["second_count"] == len(SUPPLIED_SLOTS)
    assert "[OK] No block slots detected." not in out

    no_slots = [(tmp_path / "doc.md", [], [], "installed")]
    out = _print_report_output(tmp_path, no_slots, modules=[])
    assert "[OK] No block slots detected." in out


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
