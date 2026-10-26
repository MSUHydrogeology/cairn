"""`upgrade --plan` and `--stage` name the slots an upgrade adds, and print every
note it holds as terminal-safe text.

A slot is a block in a template (`<!-- cairn:slot NAME -->` ... `<!-- cairn:end
NAME -->`) that the adopter fills or marks `N/A`.  When a new Cairn release adds
a slot to a file the adopter has already filled in, the merge keeps the adopter's
text and says nothing, so the new slot is easy to miss.  The upgrade report now
prints one `[new slot]` line per such file.

What the tests hold the code to:

* **Which slots.**  A name is printed when it is in the new template, not in the
  saved old template, and not in the adopter's file.  A slot the adopter deleted
  or already added is not "new".  Only `clean`, `clean-locally-modified` and
  `conflict` files carry names; a file new in the upgrade, a tree with no saved
  old template, a renamed filled slot, a file that needs a token value and a file
  that fails to merge carry none.
* **Where the names are read.**  From the template as shipped, before the
  project's token values are filled in.  A token value is project data, so a
  value that carries a slot pair must not add a name.
* **How much is printed.**  At most 10 names of at most 80 characters, then
  `(and N more)`.  A 1 MB name or 1,000 new slots cannot flood the terminal.
* **What reaches the terminal.**  Every `detail` the report prints goes through
  `ascii()`, so a slot name holding an ESC byte or a right-to-left override prints
  as an escape, not as the byte.  This covers the older `[flag]` and review-only
  lines too, which printed raw before.
* **A malformed adopter file stays an error.**  Reading names must never turn an
  unparseable adopter file into a clean merge.

The tests run the real command line (`bootstrap/scaffold.py upgrade`) over a real
install, with a second copy of `templates/` as the new Cairn release.  Two cases
cannot reach the code that way and call it directly: the merge function's own
result, and the review-only line, whose text is fixed in a real run.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_upgrade_added_slots.py
"""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Callable, NamedTuple

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap._scaffold import merge as merge_module  # noqa: E402
from bootstrap._scaffold.merge import merge_file  # noqa: E402
from bootstrap._scaffold.upgrade import FilePlan, _print_upgrade_report  # noqa: E402

SCAFFOLD = CAIRN_ROOT / "bootstrap" / "scaffold.py"
TEMPLATES_ROOT = CAIRN_ROOT / "templates"
LOCK_REL = "dev/.cairn/cairn-lock.yml"
README_DST = "dev/README.md"
README_SRC = Path("core") / "dev" / "README.md"
HEADING = "# dev/ — the development coordination space\n"
NEW_SLOT_TAIL = " -- new in this upgrade. Fill it, or write N/A: <reason>."

pytestmark = pytest.mark.skipif(
    not TEMPLATES_ROOT.exists(), reason="Cairn templates not available"
)


# --- slot text -----------------------------------------------------------------


def slot_block(name: str, body: str = "Body.\n") -> str:
    return f"<!-- cairn:slot {name} -->\n{body}<!-- cairn:end {name} -->\n"


def with_slot_after_heading(text: str, name: str, body: str = "Body.\n") -> str:
    assert HEADING in text, "the README template's heading changed; update HEADING"
    return text.replace(HEADING, HEADING + "\n" + slot_block(name, body), 1)


# --- a real install, and a second copy of the templates as the new release -----


class Install(NamedTuple):
    cairn_root: Path   # the release the project was installed from
    project: Path


class Scenario(NamedTuple):
    cairn_root: Path   # the release the project was installed from
    project: Path
    tmp: Path

    def new_release(self, edit: Callable[[str], str]) -> Path:
        """A second copy of the templates whose README text *edit* has changed."""
        root = self.tmp / "release_b"
        shutil.copytree(self.cairn_root / "templates", root / "templates")
        copy_citation(root)
        readme = root / "templates" / README_SRC
        readme.write_text(edit(readme.read_text(encoding="utf-8")), encoding="utf-8")
        return root


def copy_citation(root: Path) -> None:
    cff = CAIRN_ROOT / "CITATION.cff"
    if cff.exists():
        shutil.copy2(cff, root / "CITATION.cff")


def run_scaffold(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCAFFOLD), *args],
        capture_output=True, text=True, encoding="utf-8", timeout=300, cwd=str(cwd),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


@pytest.fixture(scope="module")
def installed(tmp_path_factory) -> Install:
    """One real install, from a release whose README already carries one slot
    (`existing-slot`), so a test can delete, fill or rename it."""
    root = tmp_path_factory.mktemp("added_slots")
    release = root / "release_a"
    shutil.copytree(TEMPLATES_ROOT, release / "templates")
    copy_citation(release)
    readme = release / "templates" / README_SRC
    readme.write_text(
        readme.read_text(encoding="utf-8") + "\n" + slot_block("existing-slot"),
        encoding="utf-8",
    )
    project = root / "proj"
    project.mkdir()
    profile = root / "profile.yml"
    profile.write_text(
        "project_name: AddedSlots\ntest_command: pytest\npreset: solo-greenfield\n",
        encoding="utf-8",
    )
    proc = run_scaffold(
        "--config", str(profile), "--target", str(project),
        "--cairn-root", str(release), "--allow-dev", "--non-interactive",
        cwd=root,
    )
    assert proc.returncode == 0, proc.stderr
    assert "existing-slot" in (project / README_DST).read_text(encoding="utf-8")
    return Install(release, project)


@pytest.fixture
def scenario(installed, tmp_path) -> Scenario:
    project = tmp_path / "proj"
    shutil.copytree(installed.project, project, symlinks=True)
    return Scenario(installed.cairn_root, project, tmp_path)


def upgrade(sc: Scenario, release: Path, flag: str = "--plan"):
    return run_scaffold(
        "upgrade", flag, "--target", str(sc.project), "--cairn-root", str(release),
        cwd=sc.tmp,
    )


def read_readme(sc: Scenario) -> str:
    return (sc.project / README_DST).read_text(encoding="utf-8")


def write_readme(sc: Scenario, text: str) -> None:
    (sc.project / README_DST).write_text(text, encoding="utf-8")


def read_lock(project: Path) -> dict:
    lines = (project / LOCK_REL).read_text(encoding="utf-8").splitlines()
    return json.loads("\n".join(ln for ln in lines if not ln.lstrip().startswith("#")))


def write_lock(project: Path, lock: dict) -> None:
    path = project / LOCK_REL
    header = [ln for ln in path.read_text(encoding="utf-8").splitlines()
              if ln.lstrip().startswith("#")]
    path.write_text(
        "\n".join(header) + "\n" + json.dumps(lock, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def readme_record(project: Path) -> dict:
    return next(r for r in read_lock(project)["files"] if r["dst"] == README_DST)


# --- reading the report --------------------------------------------------------


def new_slot_lines(out: str) -> list[str]:
    return [ln for ln in out.splitlines() if ln.startswith("  [new slot] ")]


def flag_lines(out: str) -> list[str]:
    return [ln for ln in out.splitlines() if ln.startswith("  [flag] ")]


def names_in(line: str) -> tuple[list[str], int]:
    """The names a `[new slot]` line lists, and the N of `(and N more)` (0 when
    absent).  The line is `  [new slot] <dst>: <names> -- new in this upgrade...`."""
    assert line.endswith(NEW_SLOT_TAIL), line[-200:]
    body = line[len("  [new slot] "):-len(NEW_SLOT_TAIL)]
    _dst, _, names = body.partition(": ")
    more = 0
    m = re.search(r" \(and (\d+) more\)$", names)
    if m:
        more = int(m.group(1))
        names = names[:m.start()]
    return names.split(", "), more


def is_printable_ascii(text: str) -> bool:
    return all(0x20 <= ord(ch) <= 0x7E for ch in text)


def summary_has(out: str, label: str, dst: str) -> bool:
    return re.search(rf"^  {re.escape(label)} +\d+: .*{re.escape(dst)}", out, re.M) is not None


# --- which slots are named -----------------------------------------------------


@pytest.mark.parametrize("flag", ["--plan", "--stage"])
def test_plan_and_stage_name_a_slot_the_upgrade_adds(scenario, flag):
    release = scenario.new_release(lambda t: with_slot_after_heading(t, "fresh-slot"))
    proc = upgrade(scenario, release, flag)
    assert proc.returncode == 0, proc.stderr
    assert new_slot_lines(proc.stdout) == [
        "  [new slot] dev/README.md: fresh-slot" + NEW_SLOT_TAIL
    ], proc.stdout


def test_file_without_added_slot_prints_no_new_slot_line(scenario):
    """Pins today's silence: a prose-only upstream change names nothing."""
    release = scenario.new_release(lambda t: t + "\nOne more sentence upstream.\n")
    proc = upgrade(scenario, release)
    assert proc.returncode == 0, proc.stderr
    assert "Cairn upgrade -- plan" in proc.stdout
    assert new_slot_lines(proc.stdout) == []


def test_new_core_file_names_no_slot(scenario):
    """Pins today's silence: a file the lockfile does not track yet is added
    whole, so its slots are not "new in this upgrade"."""
    lock = read_lock(scenario.project)
    lock["files"] = [r for r in lock["files"] if r["dst"] != README_DST]
    write_lock(scenario.project, lock)
    (scenario.project / README_DST).unlink()
    release = scenario.new_release(lambda t: with_slot_after_heading(t, "fresh-slot"))
    proc = upgrade(scenario, release)
    assert proc.returncode == 0, proc.stderr
    assert summary_has(proc.stdout, "new core/skills (added)", README_DST), proc.stdout
    assert new_slot_lines(proc.stdout) == []


def test_slot_the_adopter_deleted_is_not_named(scenario):
    """`existing-slot` is in the old template and in the new one, but the adopter
    removed it.  Only the slot the release adds is named."""
    text = read_readme(scenario)
    assert slot_block("existing-slot") in text
    write_readme(scenario, text.replace(slot_block("existing-slot"), ""))
    release = scenario.new_release(lambda t: with_slot_after_heading(t, "fresh-slot"))
    proc = upgrade(scenario, release)
    assert proc.returncode == 0, proc.stderr
    assert new_slot_lines(proc.stdout) == [
        "  [new slot] dev/README.md: fresh-slot" + NEW_SLOT_TAIL
    ], proc.stdout


def test_slot_the_adopter_already_has_is_not_named(scenario):
    """The adopter added the same slot the release now adds."""
    write_readme(scenario, with_slot_after_heading(read_readme(scenario), "fresh-slot"))
    release = scenario.new_release(lambda t: with_slot_after_heading(t, "fresh-slot"))
    proc = upgrade(scenario, release)
    assert proc.returncode == 0, proc.stderr
    assert "Cairn upgrade -- plan" in proc.stdout
    assert new_slot_lines(proc.stdout) == []


# --- what merge_file returns ---------------------------------------------------

BASE = "head\n" + slot_block("kept") + "tail\n"


def _merge(theirs: str, ours: str = BASE, base: str = BASE, tokens=None):
    return merge_file(base, theirs, ours, tokens or {})


def test_detail_is_empty_or_exactly_the_name_list_on_clean_and_conflict():
    added = "head\n" + slot_block("kept") + slot_block("added-one") \
        + slot_block("added-two") + "tail\n"

    clean = _merge(added)
    assert (clean.status, clean.detail) == ("clean", "added-one, added-two")

    quiet = _merge(BASE)
    assert (quiet.status, quiet.detail) == ("clean", "")

    ours_edit = BASE.replace("head\n", "ours head\n")
    conflict = _merge(added.replace("head\n", "theirs head\n", 1), ours=ours_edit)
    assert (conflict.status, conflict.detail) == ("conflict", "added-one, added-two")

    quiet_conflict = _merge(
        BASE.replace("head\n", "theirs head\n"), ours=ours_edit)
    assert (quiet_conflict.status, quiet_conflict.detail) == ("conflict", "")


def test_needs_value_slot_removed_and_error_carry_no_names(monkeypatch):
    added = slot_block("added-one")

    needs_value = _merge("head\n{{new_token}}\n" + slot_block("kept") + added + "tail\n")
    assert needs_value.status == "needs-value"
    assert "new_token" in needs_value.detail
    assert "added-one" not in needs_value.detail

    # `kept` is filled by the adopter and gone upstream: slot-removed returns first.
    filled = "head\n" + slot_block("kept", "Adopter text.\n") + "tail\n"
    removed = _merge("head\n" + added + "tail\n", ours=filled)
    assert removed.status == "slot-removed"
    assert "kept" in removed.detail
    assert "added-one" not in removed.detail

    def refuse(*_args, **_kwargs):
        raise RuntimeError("git merge-file unavailable: test")

    monkeypatch.setattr(merge_module, "_three_way_merge", refuse)
    errored = _merge("head\n" + slot_block("kept") + added + "tail\n")
    assert errored.status == "error"
    assert errored.detail == "git merge-file unavailable: test"


def test_lockfile_token_value_carrying_a_slot_pair_adds_no_name(scenario):
    """A token value is project data.  Used only in the new template, one that
    holds a slot pair would add a name if names were read after the fill."""
    lock = read_lock(scenario.project)
    lock["tokens"]["inj_tok"] = (
        "<!-- cairn:slot injected-slot -->\n<!-- cairn:end injected-slot -->")
    write_lock(scenario.project, lock)

    def edit(text: str) -> str:
        return with_slot_after_heading(text, "fresh-slot") + "\n{{inj_tok}}\n"

    release = scenario.new_release(edit)
    proc = upgrade(scenario, release)
    assert proc.returncode == 0, proc.stderr
    # The real slot is named (the instrument works); the injected one is not.
    assert new_slot_lines(proc.stdout) == [
        "  [new slot] dev/README.md: fresh-slot" + NEW_SLOT_TAIL
    ], proc.stdout


def test_lockfile_token_value_in_the_old_template_hides_no_name(scenario):
    """The saved old template is read as shipped too.  If its names were read
    after the token fill, a value holding a slot pair could hide a real new slot
    by putting its name into the "already there" set."""
    lock = read_lock(scenario.project)
    lock["tokens"]["inj_tok"] = (
        "<!-- cairn:slot fresh-slot -->\n<!-- cairn:end fresh-slot -->")
    write_lock(scenario.project, lock)
    base = scenario.project / readme_record(scenario.project)["base_cache"]
    base.write_text(base.read_text(encoding="utf-8") + "\n{{inj_tok}}\n",
                    encoding="utf-8")
    release = scenario.new_release(lambda t: with_slot_after_heading(t, "fresh-slot"))
    proc = upgrade(scenario, release)
    assert proc.returncode == 0, proc.stderr
    assert new_slot_lines(proc.stdout) == [
        "  [new slot] dev/README.md: fresh-slot" + NEW_SLOT_TAIL
    ], proc.stdout


def test_token_value_that_breaks_the_new_text_still_reports_error(scenario):
    """The new template, token values filled in, is parsed strictly, outside the
    step that reads names.  A value that leaves a slot unclosed must give `error`,
    not an empty slot set that would flag the adopter's slot as removed."""
    lock = read_lock(scenario.project)
    lock["tokens"]["inj_tok"] = "<!-- cairn:slot unclosed -->"
    write_lock(scenario.project, lock)
    release = scenario.new_release(lambda t: t + "\n{{inj_tok}}\n")
    proc = upgrade(scenario, release)
    assert proc.returncode == 0, proc.stderr
    assert summary_has(proc.stdout, "error", README_DST), proc.stdout
    (flag,) = [ln for ln in flag_lines(proc.stdout) if README_DST in ln]
    assert "malformed slots:" in flag, flag


# --- how much is printed -------------------------------------------------------


def test_new_slot_line_names_at_most_ten_names_of_at_most_eighty_characters(scenario):
    release = scenario.new_release(
        lambda t: with_slot_after_heading(t, "x" * 1_000_000))
    proc = upgrade(scenario, release)
    assert proc.returncode == 0, proc.stderr
    (line,) = new_slot_lines(proc.stdout)
    names, more = names_in(line)
    assert names == ["x" * 77 + "..."] and more == 0
    assert len(line) < 1200


def test_new_slot_line_states_how_many_more_slots_it_left_out(scenario):
    def edit(text: str) -> str:
        blocks = "".join(slot_block(f"slot-{i:04d}") for i in range(1000))
        return text.replace(HEADING, HEADING + "\n" + blocks, 1)

    proc = upgrade(scenario, scenario.new_release(edit))
    assert proc.returncode == 0, proc.stderr
    (line,) = new_slot_lines(proc.stdout)
    names, more = names_in(line)
    assert names == [f"slot-{i:04d}" for i in range(10)]
    assert more == 990
    assert len(line) < 1200


def test_new_slot_line_stays_within_its_bound_for_names_that_escape_longest(scenario):
    """A character outside the Basic Multilingual Plane prints as 10 characters
    (`\\U0001f600`).  Ten names of 80 such characters are the longest line the cap
    allows: 10 x 800 plus nine separators."""
    def edit(text: str) -> str:
        blocks = "".join(slot_block(chr(0x1F600 + i) * 80) for i in range(11))
        return text.replace(HEADING, HEADING + "\n" + blocks, 1)

    proc = upgrade(scenario, scenario.new_release(edit))
    assert proc.returncode == 0, proc.stderr
    (line,) = new_slot_lines(proc.stdout)
    names, more = names_in(line)
    assert len(names) == 10 and more == 1
    assert len(", ".join(names)) <= 8018
    assert is_printable_ascii(line)


# --- what reaches the terminal -------------------------------------------------

ESC_NAME = "gone\x1b[2Jslot‮"


def _hostile_adopter_slot(sc: Scenario) -> None:
    """A filled slot the new release does not have: the merge flags it."""
    write_readme(sc, read_readme(sc) + "\n" + slot_block(ESC_NAME, "Adopter text.\n"))


def _hostile_new_slot(sc: Scenario) -> Path:
    name = "new\x1b[31m\U0001F600slot"
    return sc.new_release(lambda t: with_slot_after_heading(t, name))


def _hostile_malformed_adopter(sc: Scenario) -> None:
    write_readme(sc, read_readme(sc) + "\n<!-- cairn:slot bad\x1b[2Jone‮ -->\n")


@pytest.mark.parametrize("flag", ["--plan", "--stage"])
@pytest.mark.parametrize("case, expected", [
    ("removed-filled-slot", "  [flag] dev/README.md: upstream removed slot(s)"),
    ("added-slot", "  [new slot] dev/README.md: "),
    ("malformed-adopter-file", "  [flag] dev/README.md: malformed slots:"),
], ids=["removed-filled-slot", "added-slot", "malformed-adopter-file"])
def test_every_flag_and_new_slot_line_is_printable_ascii(scenario, flag, case, expected):
    release = scenario.cairn_root
    if case == "removed-filled-slot":
        _hostile_adopter_slot(scenario)
    elif case == "added-slot":
        release = _hostile_new_slot(scenario)
    else:
        _hostile_malformed_adopter(scenario)
    proc = upgrade(scenario, release, flag)
    out = proc.stdout
    # The line is there before its bytes are judged: an absent line proves nothing.
    wanted = [ln for ln in out.splitlines() if ln.startswith(expected)]
    assert len(wanted) == 1, out
    for ln in flag_lines(out) + new_slot_lines(out):
        assert is_printable_ascii(ln), ascii(ln)
    # `--stage` prints its report after it writes the stage; read all of stdout.
    assert "\x1b" not in out and "‮" not in out


def test_review_only_detail_is_escaped_when_printed():
    """A real run prints fixed text on this line, so no hostile byte reaches it;
    the print site is still guarded, and only a direct call can show it."""
    plan = FilePlan("x.md", "review-only", None, "why\x1b[2J‮", "t", None)
    buf = io.StringIO()
    with redirect_stdout(buf):
        _print_upgrade_report(
            [plan], {"new_modules": [], "removed_modules": []}, None, mode="plan")
    out = buf.getvalue()
    lines = [ln for ln in out.splitlines() if ln.startswith("      x.md: ")]
    assert lines == ["      x.md: why\\x1b[2J\\u202e"], out
    assert "\x1b" not in out and "‮" not in out


# --- cases that must stay as they are ------------------------------------------


def test_malformed_adopter_file_still_reports_error_never_clean(scenario):
    write_readme(scenario, read_readme(scenario) + "\n<!-- cairn:slot broken -->\n")
    release = scenario.new_release(lambda t: with_slot_after_heading(t, "fresh-slot"))
    proc = upgrade(scenario, release)
    assert proc.returncode == 0, proc.stderr
    assert summary_has(proc.stdout, "error", README_DST), proc.stdout
    (flag,) = [ln for ln in flag_lines(proc.stdout) if README_DST in ln]
    assert "malformed slots:" in flag, flag
    assert new_slot_lines(proc.stdout) == []


def test_malformed_old_base_keeps_its_status_and_prints_no_name(scenario):
    """Pins the status.  An old template with an unclosed slot cannot be parsed
    for names, so none are printed; the merge goes on as it did before, and
    reports a conflict."""
    base = scenario.project / readme_record(scenario.project)["base_cache"]
    closing = "<!-- cairn:end existing-slot -->\n"
    text = base.read_text(encoding="utf-8")
    assert closing in text
    base.write_text(text.replace(closing, ""), encoding="utf-8")
    # The new slot sits next to the broken one, where the two versions meet.
    release = scenario.new_release(lambda t: t.replace(
        slot_block("existing-slot"),
        slot_block("existing-slot") + slot_block("fresh-slot")))
    proc = upgrade(scenario, release)
    assert proc.returncode == 0, proc.stderr
    assert summary_has(proc.stdout, "conflict", README_DST), proc.stdout
    assert new_slot_lines(proc.stdout) == []


def test_tree_without_base_copy_names_nothing(scenario):
    base = scenario.project / readme_record(scenario.project)["base_cache"]
    base.unlink()
    release = scenario.new_release(lambda t: with_slot_after_heading(t, "fresh-slot"))
    proc = upgrade(scenario, release)
    assert proc.returncode == 0, proc.stderr
    assert summary_has(proc.stdout, "review-only", README_DST), proc.stdout
    assert new_slot_lines(proc.stdout) == []


def test_renamed_filled_slot_stays_slot_removed_and_names_no_new_slot(scenario):
    text = read_readme(scenario)
    write_readme(scenario, text.replace(
        slot_block("existing-slot"), slot_block("existing-slot", "Adopter text.\n")))
    release = scenario.new_release(
        lambda t: t.replace("existing-slot", "renamed-slot"))
    proc = upgrade(scenario, release)
    assert proc.returncode == 0, proc.stderr
    assert summary_has(proc.stdout, "slot-removed", README_DST), proc.stdout
    (flag,) = [ln for ln in flag_lines(proc.stdout) if README_DST in ln]
    assert "existing-slot" in flag
    assert new_slot_lines(proc.stdout) == []
