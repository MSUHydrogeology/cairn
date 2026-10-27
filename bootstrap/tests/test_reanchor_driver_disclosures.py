"""What the re-anchor ceremony driver tells the operator about trust.

`scripts/reanchor_ceremony.py` does not decide anything. It prints the closure
three ways, checks that the packet and the launcher are a pair, and rehearses
the read-only checks. What it prints is the only warning an operator gets before
spending an authorization package, so a line that quietly stopped printing, or
that printed while the driver still said all was well, would leave the operator
believing something false.

Each node below builds a small scratch repository (the real launcher template
at a candidate commit, stub members, and a gate-anchor ref), calls the driver's
`compare`, `check_packet_pair` or `rehearse`, and asserts two things: the
return value or recorded problem that a caller acts on, and one stable phrase
of the printed line. The phrase is a fragment, not the whole sentence, so a
reword does not fail a node but a deleted line does. A node that failed only
on rewording would be pinning wording rather than the disclosure.

The driver is loaded from this file's own checkout, not imported by name, so a
copy of the tree in a separate worktree tests its own driver.
"""
from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_DRIVER_PATH = _REPO / "scripts" / "reanchor_ceremony.py"
_TEMPLATE_REL = "bootstrap/reanchor-launcher.template.sh"
_SLOT = "@PACKET_SHA256@"
_GIT = ["git", "-c", "user.email=t@t", "-c", "user.name=t",
        "-c", "commit.gpgsign=false"]


@pytest.fixture(scope="module")
def driver():
    spec = importlib.util.spec_from_file_location(
        "reanchor_ceremony_under_test", _DRIVER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(repo: Path, *args: str) -> str:
    done = subprocess.run([*_GIT, "-C", str(repo), *args], check=True,
                          capture_output=True, text=True)
    return done.stdout.strip()


def _members() -> list[str]:
    """The closure as the template states it: the driver reads it from there."""
    text = (_REPO / _TEMPLATE_REL).read_text(encoding="utf-8")
    block = text.split("EXPECTED_PATHS='", 1)[1].split("'", 1)[0]
    return [line for line in block.splitlines() if line.strip()]


class Scratch:
    """A repository holding the closure at an anchor and at a candidate."""

    def __init__(self, root: Path, change: tuple[str, ...]):
        self.root = root
        self.repo = root / "repo"
        self.members = _members()
        self.repo.mkdir()
        _git(self.repo, "init", "-q")
        for rel in self.members:
            self._write(rel, self._stub(rel))
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-qm", "anchor")
        _git(self.repo, "update-ref", "refs/cairn/gate-anchor", "HEAD")
        for rel in change:
            self._write(rel, self._stub(rel) + "changed\n")
        if change:
            _git(self.repo, "commit", "-qam", "candidate")
        self.candidate = _git(self.repo, "rev-parse", "HEAD")

    @staticmethod
    def _stub(rel: str) -> str:
        if rel == _TEMPLATE_REL:
            return (_REPO / _TEMPLATE_REL).read_text(encoding="utf-8")
        return f"stub of {rel}\n"

    def _write(self, rel: str, text: str) -> None:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def digest_at_candidate(self, rel: str) -> str:
        blob = subprocess.run(
            ["git", "-C", str(self.repo), "cat-file", "blob",
             f"{self.candidate}:{rel}"],
            check=True, capture_output=True).stdout
        return hashlib.sha256(blob).hexdigest()

    def packet(self, *, drop: str | None = None, wrong: str | None = None,
               extra: tuple[str, ...] = ()) -> Path:
        """A packet over the candidate's closure, with one deliberate fault."""
        lines = ["schema cairn-authorization-packet/v1",
                 "provenance scratch repository",
                 "artifact bootstrap/reanchor.sh",
                 f"artifact_sha256 {self.digest_at_candidate('bootstrap/reanchor.sh')}"]
        for rel in self.members:
            if rel == drop:
                continue
            digest = "0" * 64 if rel == wrong else self.digest_at_candidate(rel)
            lines.append(f"member {digest} {rel}")
        for rel in extra:
            lines.append(f"member {'1' * 64} {rel}")
        path = self.root / "packet.txt"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    def launcher(self, packet: Path, *, digest: str | None = None,
                 fill: bool = True, has_fix: bool = True) -> Path:
        """The template with its slot filled, as the review delivers it."""
        text = (_REPO / _TEMPLATE_REL).read_text(encoding="utf-8")
        if fill:
            text = text.replace(
                _SLOT, digest or hashlib.sha256(packet.read_bytes()).hexdigest())
        if not has_fix:
            text = text.replace("unset L_checkout", "")
        path = self.root / "launcher.sh"
        path.write_text(text, encoding="utf-8")
        return path


@pytest.fixture
def scratch(tmp_path):
    return Scratch(tmp_path, change=("bootstrap/reanchor.sh",))


def _printed(capsys) -> str:
    return capsys.readouterr().out


class TestTheClosureTableNamesWhatDiffers:

    def test_an_unchanged_closure_is_neither_starred_nor_called_a_transition(
            self, driver, tmp_path, capsys):
        """Control for the two disclosures below: with nothing changed the
        driver must say so, or the marker and the note carry no information."""
        same = Scratch(tmp_path, change=())
        driver.compare(same.repo, same.candidate, None)
        out = _printed(capsys)
        assert f"0 of {len(same.members)} members changed" in out
        template_digest = hashlib.sha256(
            (_REPO / _TEMPLATE_REL).read_bytes()).hexdigest()
        assert f"template    {template_digest[:12]}" in out
        assert "TRANSITION" not in out
        assert not any(line.startswith(" *") for line in out.splitlines())

    def test_a_changed_member_is_starred_and_counted(
            self, driver, scratch, capsys):
        state = driver.compare(scratch.repo, scratch.candidate, None)
        out = _printed(capsys)
        starred = [line for line in out.splitlines() if line.startswith(" *")]
        assert len(starred) == 1 and "bootstrap/reanchor.sh" in starred[0]
        assert f"1 of {len(scratch.members)} members changed" in out
        assert state["changed"] == ["bootstrap/reanchor.sh"]

    def test_a_changed_closure_is_announced_as_a_transition(
            self, driver, scratch, capsys):
        driver.compare(scratch.repo, scratch.candidate, None)
        assert "This is a TRANSITION ceremony" in _printed(capsys)


class TestAPacketThatDisagreesWithTheCandidateRefusesThePair:
    """The three ways a packet can describe a different closure than the
    candidate holds. Each is named in the table and recorded as a problem, and
    the pair check must carry the problem to the operator and refuse."""

    def _pair(self, driver, scratch, packet, capsys):
        state = driver.compare(scratch.repo, scratch.candidate, packet)
        table = _printed(capsys)
        launcher = scratch.launcher(packet)
        ok = driver.check_packet_pair(state, packet, launcher)
        return state, table, ok, _printed(capsys)

    def test_a_packet_with_no_row_for_a_member_is_refused(
            self, driver, scratch, capsys):
        packet = scratch.packet(drop="bootstrap/tests/_oracle.py")
        state, table, ok, pair = self._pair(driver, scratch, packet, capsys)
        assert "MISSING" in table
        assert any("the packet has no row for this member" in p
                   for p in state["packet_problems"])
        assert "the packet has no row for this member" in pair
        assert ok is False

    def test_a_packet_row_that_differs_from_the_candidate_is_refused(
            self, driver, scratch, capsys):
        packet = scratch.packet(wrong="bootstrap/tests/_oracle.py")
        state, table, ok, pair = self._pair(driver, scratch, packet, capsys)
        assert "0" * 12 + " !!" in table
        assert any("packet says" in p for p in state["packet_problems"])
        assert "packet says" in pair
        assert ok is False

    def test_a_packet_naming_a_member_the_closure_does_not_is_refused(
            self, driver, scratch, capsys):
        packet = scratch.packet(extra=("bootstrap/tests/_smuggled.py",))
        state, _, ok, pair = self._pair(driver, scratch, packet, capsys)
        assert any("the packet names a member the closure does not" in p
                   for p in state["packet_problems"])
        assert "the packet names a member the closure does not" in pair
        assert ok is False


class TestThePairCheck:

    NO_PROBLEMS = {"packet_problems": []}

    def test_a_matching_pair_is_accepted_and_says_so(
            self, driver, scratch, capsys):
        """Control for every refusal below: the same builder, with no fault,
        is accepted, so the refusals are about their fault and not the fixture."""
        packet = scratch.packet()
        launcher = scratch.launcher(packet)
        assert driver.check_packet_pair(self.NO_PROBLEMS, packet, launcher) is True
        out = _printed(capsys)
        assert f"sha256 {hashlib.sha256(packet.read_bytes()).hexdigest()}" in out
        assert f"sha256 {hashlib.sha256(launcher.read_bytes()).hexdigest()}" in out
        assert "comparison will hold" in out
        assert "carries the environment-injection fix" in out
        assert "!!" not in out

    def test_an_absent_packet_is_refused_and_named(
            self, driver, scratch, capsys):
        launcher = scratch.launcher(scratch.packet())
        absent = scratch.root / "no-such-packet.txt"
        assert driver.check_packet_pair(self.NO_PROBLEMS, absent, launcher) is False
        out = _printed(capsys)
        assert "ABSENT" in out
        assert "Without both, the ceremony cannot start" in out

    def test_an_absent_launcher_beside_a_present_packet_is_refused(
            self, driver, scratch, capsys):
        packet = scratch.packet()
        absent = scratch.root / "no-such-launcher.sh"
        assert driver.check_packet_pair(self.NO_PROBLEMS, packet, absent) is False
        assert "is ABSENT while the packet is present" in _printed(capsys)

    def test_a_launcher_with_an_unfilled_slot_is_refused(
            self, driver, scratch, capsys):
        packet = scratch.packet()
        launcher = scratch.launcher(packet, fill=False)
        assert driver.check_packet_pair(self.NO_PROBLEMS, packet, launcher) is False
        assert "still carries the unfilled" in _printed(capsys)

    def test_a_launcher_bound_to_another_packet_is_refused(
            self, driver, scratch, capsys):
        packet = scratch.packet()
        launcher = scratch.launcher(packet, digest="e" * 64)
        assert driver.check_packet_pair(self.NO_PROBLEMS, packet, launcher) is False
        assert "does not carry this packet's digest" in _printed(capsys)

    def test_a_launcher_without_the_environment_fix_is_refused(
            self, driver, scratch, capsys):
        packet = scratch.packet()
        launcher = scratch.launcher(packet, has_fix=False)
        assert driver.check_packet_pair(self.NO_PROBLEMS, packet, launcher) is False
        assert "DO NOT RUN THIS FILE" in _printed(capsys)


class TestTheRehearsalSaysItExecutesCandidateCode:
    """The banner is the operator's only notice that the rehearsal is not
    read-only. The node must stop right after the banner and run no candidate
    code, so it makes the import that follows the banner fail on every load
    path that could otherwise succeed. A marker written by the scratch
    candidate's own module is the evidence that nothing ran: an absent traceback
    is not, because a refusal and a crash both produce one."""

    @pytest.mark.parametrize("load_path", [
        "nothing else",
        "the real checker's directory on sys.path",
    ])
    def test_the_banner_is_printed_before_anything_candidate_owned_loads(
            self, driver, scratch, capsys, monkeypatch, tmp_path, load_path):
        marker = tmp_path / "CANDIDATE-CODE-RAN"
        module = scratch.repo / "bootstrap/tests/_gate_preflight.py"
        module.write_text(f"open({str(marker)!r}, 'w').close()\n")
        state = driver.compare(scratch.repo, scratch.candidate, None)
        capsys.readouterr()

        if load_path == "the real checker's directory on sys.path":
            monkeypatch.syspath_prepend(str(_REPO / "bootstrap" / "tests"))
        # None makes `import _gate_preflight` raise on every path, so the
        # rehearsal stops at the import that follows the banner. It also
        # replaces any module of that name an earlier test left behind, which
        # is why a "leftover module" case is not a separate parameter: it would
        # run the same statements as the first.
        monkeypatch.setitem(sys.modules, "_gate_preflight", None)

        with pytest.raises(SystemExit):
            driver.rehearse(scratch.repo, state)

        assert "THAT EXECUTES CANDIDATE CODE" in _printed(capsys)
        assert not marker.exists(), (
            "the scratch candidate's module was loaded: the rehearsal ran "
            "candidate code before this test could stop it")


# ---------------------------------------------------------------------------
# the driver runs no stage, and what it prints is typed commands that work
# ---------------------------------------------------------------------------

import re  # noqa: E402
import shlex  # noqa: E402


def _preflight_output(driver, scratch, capsys, monkeypatch, *, pair_ok):
    """Run the driver's `main` over the scratch repository with the two slow,
    separately tested halves stubbed, and return what it printed."""
    values = scratch.root / "values"
    values.write_text(f"checkout {scratch.repo}\nhome {scratch.root}/home\n", encoding="utf-8")
    monkeypatch.setattr(driver, "rehearse", lambda repo, state: True)
    monkeypatch.setattr(driver, "check_packet_pair",
                        lambda state, packet, launcher: pair_ok)
    monkeypatch.setattr(sys, "argv", [
        "reanchor_ceremony.py", "--values", str(values),
        "--ceremony-dir", str(scratch.root / "ceremony"),
        "--candidate", scratch.candidate])
    driver.main()
    return _printed(capsys), values


class TestTheDriverRunsNoStage:

    def test_nothing_under_scripts_runs_a_stage_or_names_the_retired_corrector(self):
        pattern = re.compile(r"def drive\b|--run\b|correct_pinned_digests")
        # the instrument can match: the pattern finds each of its three targets
        for sample in ("def drive(repo)", "add --run to go", "correct_pinned_digests.py"):
            assert pattern.search(sample), sample
        found = [f"{p.name}:{n}" for p in sorted((_REPO / "scripts").glob("*.py"))
                 for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1)
                 if pattern.search(line)]
        assert found == []

    def test_the_run_option_is_refused_as_unknown(self, driver, scratch, monkeypatch,
                                                  capsys):
        values = scratch.root / "values"
        values.write_text(f"checkout {scratch.repo}\n", encoding="utf-8")
        monkeypatch.setattr(sys, "argv", ["x", "--values", str(values),
                                          "--ceremony-dir", str(scratch.root),
                                          "--run"])
        with pytest.raises(SystemExit) as exc:
            driver.main()
        assert exc.value.code == 2
        assert "unrecognized arguments: --run" in capsys.readouterr().err


class TestTheClosureListIsReadFromTheTemplate:

    def test_a_candidate_template_with_no_member_list_stops_naming_the_template(
            self, driver, scratch, capsys):
        """The message used to name a variable that did not exist, so the stop
        the operator needed was a NameError instead."""
        (scratch.repo / _TEMPLATE_REL).write_text("no list here\n", encoding="utf-8")
        _git(scratch.repo, "commit", "-qam", "template without a list")
        bare = _git(scratch.repo, "rev-parse", "HEAD")
        with pytest.raises(SystemExit):
            driver.closure_members(scratch.repo, bare)
        assert f"cannot find EXPECTED_PATHS in {_TEMPLATE_REL}" in _printed(capsys)

    def test_the_launcher_template_is_a_member_and_the_docstring_agrees(
            self, driver):
        members = _members()
        assert _TEMPLATE_REL in members
        assert "NOT itself a closure member" not in driver.closure_members.__doc__


class TestThePrintedCommandsAreTheOnesThatWork:

    def _commands(self, out):
        return [shlex.split(line) for line in out.splitlines()
                if line.startswith(("    /bin/sh ", "    env -i "))]

    def test_nothing_says_the_materials_come_from_outside(
            self, driver, scratch, capsys, monkeypatch):
        out, _ = _preflight_output(driver, scratch, capsys, monkeypatch,
                                   pair_ok=False)
        assert "out of band" not in out
        assert "repin" in out and "packet" in out

    def test_no_printed_command_runs_the_working_tree_copy_of_the_artifact(
            self, driver, scratch, capsys, monkeypatch):
        """Every file under the closure is candidate code until the launcher
        has checked it, so the driver must not tell a person to run one."""
        out, _ = _preflight_output(driver, scratch, capsys, monkeypatch,
                                   pair_ok=True)
        assert "reanchor.sh" not in "\n".join(
            line for line in out.splitlines() if line.startswith(("    /bin/sh ", "    env -i ")))

    def test_each_printed_launcher_form_is_accepted_by_the_real_launcher(
            self, driver, scratch, capsys, monkeypatch):
        """Run each printed form through the real launcher template: the
        arguments must parse (the launcher refuses later, on the absent packet,
        rather than printing its usage text)."""
        out, values = _preflight_output(driver, scratch, capsys, monkeypatch,
                                        pair_ok=True)
        forms = self._commands(out)
        assert len(forms) == 2, out
        launcher_forms = {"stage 1": forms[0], "stage 2": forms[1]}
        assert forms[0][:forms[0].index("/bin/sh")] == forms[1][:forms[1].index("/bin/sh")]
        assert "--stage2" in forms[1] and "--stage2" not in forms[0]
        real = scratch.root / "real-launcher.sh"
        real.write_text(
            (_REPO / _TEMPLATE_REL).read_text(encoding="utf-8").replace(
                _SLOT, "0" * 64), encoding="utf-8")
        for name, form in launcher_forms.items():
            argv = ["/bin/sh", str(real), *form[form.index("/bin/sh") + 2:]]
            if name == "stage 2":
                argv[argv.index("--stage2") + 1] = "f" * 64
            proc = subprocess.run(argv, capture_output=True, text=True,
                                  check=False)
            assert proc.returncode != 0
            assert "usage:" not in proc.stderr, (name, proc.stderr)
            assert "REFUSE:" in proc.stderr, (name, proc.stderr)
        # and each names the pieces in the launcher's own argument order
        ceremony = scratch.root / "ceremony"
        stage1 = ["/bin/sh", str(ceremony / "reanchor-launcher.sh"),
                  str(ceremony / "authorization-packet.txt"), str(values),
                  scratch.candidate]
        i = forms[0].index("/bin/sh")
        assert forms[0][i:] == stage1
        assert forms[1][forms[1].index("/bin/sh"):] == stage1 + ["--stage2", "<package-digest>"]
        # both start under the short environment the page shows, with the home from the values file
        for form in forms:
            assert form[:form.index("/bin/sh")] == ["env", "-i", f"HOME={scratch.root}/home",
                                                    "PATH=/usr/bin:/bin", "TERM=$TERM", "LANG=C"], form
