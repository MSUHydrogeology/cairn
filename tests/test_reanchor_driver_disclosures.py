"""What the re-anchor ceremony driver tells the operator about trust.

Promises:
- The printed closure names every member that changed and counts them; an unchanged closure is reported as unchanged.
- A changed closure is announced as a transition ceremony.
- A packet that disagrees with the candidate refuses the pair, and the refusal names the member at fault.
- An absent or unfilled launcher, or one bound to another packet or lacking the environment fix, refuses the pair.
- The rehearsal says it executes candidate code before it loads any candidate module.
- The driver runs no stage and refuses a run option as unknown; printed commands run the reviewed launcher, never the working-tree artifact.
- `release/repin.py` shows the net change of the three pinned files key by key (a key on one side only as `(absent)`, old fixture paths mapped to the new ones, every key and value escaped for a terminal) and refuses a pinned file the candidate lacks or that cannot be read, or a file that repeats a JSON key or a lock that repeats a destination, since the display would show one copy; after a passing `--check-only` it prints the command it was given, without that flag.
Sources: release/reanchor_ceremony.py module docstring (the banner and "IT RUNS NO STAGE"); release/reanchor_ceremony.py --help; release/repin.py `net_change_lines`.


`release/reanchor_ceremony.py` does not decide anything. It prints the closure
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

from tests._repo_root import repository_root

_REPO = repository_root(Path(__file__))
_DRIVER_PATH = _REPO / "release" / "reanchor_ceremony.py"
_TEMPLATE_REL = "release/reanchor-launcher.template.sh"
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
                 "artifact release/reanchor.sh",
                 f"artifact_sha256 {self.digest_at_candidate('release/reanchor.sh')}"]
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
    return Scratch(tmp_path, change=("release/reanchor.sh",))


def _printed(capsys) -> str:
    return capsys.readouterr().out


class TestTheClosureTableNamesWhatDiffers:


    def test_a_changed_member_is_starred_and_counted(
            self, driver, scratch, capsys):
        state = driver.compare(scratch.repo, scratch.candidate, None)
        out = _printed(capsys)
        starred = [line for line in out.splitlines() if line.startswith(" *")]
        assert len(starred) == 1 and "release/reanchor.sh" in starred[0]
        assert f"1 of {len(scratch.members)} members changed" in out
        assert state["changed"] == ["release/reanchor.sh"]

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
        packet = scratch.packet(drop="tests/_oracle.py")
        state, table, ok, pair = self._pair(driver, scratch, packet, capsys)
        assert "MISSING" in table
        assert any("the packet has no row for this member" in p
                   for p in state["packet_problems"])
        assert "the packet has no row for this member" in pair
        assert ok is False

    def test_a_packet_row_that_differs_from_the_candidate_is_refused(
            self, driver, scratch, capsys):
        packet = scratch.packet(wrong="tests/_oracle.py")
        state, table, ok, pair = self._pair(driver, scratch, packet, capsys)
        assert "0" * 12 + " !!" in table
        assert any("packet says" in p for p in state["packet_problems"])
        assert "packet says" in pair
        assert ok is False

    def test_a_packet_naming_a_member_the_closure_does_not_is_refused(
            self, driver, scratch, capsys):
        packet = scratch.packet(extra=("tests/_smuggled.py",))
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
        module = scratch.repo / "tests/_gate_preflight.py"
        module.write_text(f"open({str(marker)!r}, 'w').close()\n")
        state = driver.compare(scratch.repo, scratch.candidate, None)
        capsys.readouterr()

        if load_path == "the real checker's directory on sys.path":
            monkeypatch.syspath_prepend(str(_REPO / "tests"))
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


# ---------------------------------------------------------------------------
# `release/repin.py`: the net change a transition shows before Summary 2
# ---------------------------------------------------------------------------

import json  # noqa: E402

_BASELINE = "tests/fixtures/scaffold_ast_baseline.json"
_KNOWN_NEW = "tests/fixtures/scaffold_ast_known_new.json"
_LOCK = "dev/.cairn/cairn-lock.yml"
_OLD_BASELINE = "bootstrap/tests/fixtures/scaffold_ast_baseline.json"
_OLD_KNOWN_NEW = "bootstrap/tests/fixtures/scaffold_ast_known_new.json"


@pytest.fixture(scope="module")
def repin():
    spec = importlib.util.spec_from_file_location("repin_under_test", _REPO / "release" / "repin.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _lock(*dsts: str) -> str:
    records = [{"dst": dst, "hash": "sha256:" + dst} for dst in dsts]
    return "# header\n" + json.dumps({"files": records}, indent=2, sort_keys=True) + "\n"


def _record(dst: str, digest: str) -> dict:
    return {"dst": dst, "hash": "sha256:" + digest}


def _lock_records(*records: dict) -> str:
    """A lock whose records are exactly those given, in that order, repeats included."""
    return "# header\n" + json.dumps({"files": list(records)}, indent=2) + "\n"


def _pinned(baseline: dict, known_new: dict | None = None, lock: str | None = None) -> dict:
    files = {_BASELINE: json.dumps(baseline), _KNOWN_NEW: json.dumps(known_new or {})}
    if lock is not None:
        files[_LOCK] = lock
    return files


def _two_commits(root: Path, before: dict, after: dict, **ctx) -> dict:
    """A repository whose first commit holds *before* and whose second holds *after* (a path
    absent from *after* is removed), as the context `net_change_lines` reads."""
    repo = root / "pinned"
    repo.mkdir()
    _git(repo, "init", "-q")
    for files, message in ((before, "anchor"), (after, "candidate")):
        for path in list(repo.rglob("*")):
            if path.is_file() and ".git" not in path.parts:
                path.unlink()
        for rel, text in files.items():
            target = repo / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        _git(repo, "add", "-A")
        _git(repo, "commit", "-qm", message)
        if message == "anchor":
            anchor = _git(repo, "rev-parse", "HEAD")
    return {"repo": repo, "anchor": anchor, "head": _git(repo, "rev-parse", "HEAD"), **ctx}


class TestTheNetChangeOfThePinnedFilesIsShownKeyByKey:

    def test_a_key_on_one_side_only_prints_absent_on_the_other_and_is_not_refused(self, repin, tmp_path):
        ctx = _two_commits(tmp_path, _pinned({"a": 1, "b": 2}, lock=_lock("x")),
                           _pinned({"a": 1, "c": 3}, lock=_lock("x")))
        lines = repin.net_change_lines(ctx)
        assert f"{_BASELINE}: 2 changed" in lines and f"{_KNOWN_NEW}: no change" in lines
        assert any("b:  2  ->  (absent)" in line for line in lines)
        assert any("c:  (absent)  ->  3" in line for line in lines)
        with pytest.raises(repin.Refuse):          # the default refusal of a write that adds or drops a key stays
            repin.render_changes(_BASELINE, json.dumps({"a": 1, "b": 2}).encode(),
                                 json.dumps({"a": 1, "c": 3}).encode())

    def test_a_file_the_anchor_lacks_shows_every_key_as_new_and_old_fixture_paths_are_mapped(
            self, repin, tmp_path):
        before = {_OLD_BASELINE: json.dumps({"a": 1}), _OLD_KNOWN_NEW: "{}"}
        after = _pinned({"a": 2}, lock=_lock("x", "y"))
        ctx = _two_commits(tmp_path, before, after, layout_evidence="0" * 64)
        lines = repin.net_change_lines(ctx)
        assert f"{_BASELINE}: 1 changed (the anchor holds it at {_OLD_BASELINE})" in lines
        assert f"{_KNOWN_NEW}: no change (the anchor holds it at {_OLD_KNOWN_NEW})" in lines
        assert f"{_LOCK}: not at the anchor, so every key is new" in lines
        assert sum("(absent)  ->" in line for line in lines if line.startswith("  cairn-lock.yml")) >= 2
        unmapped = repin.net_change_lines(dict(ctx, layout_evidence=None))   # no layout move: the old paths are not read
        assert f"{_BASELINE}: not at the anchor, so every key is new" in unmapped

    def test_every_key_and_value_is_escaped_for_a_terminal(self, repin, tmp_path):
        hostile = "\x1b[31mred\nnext line"
        ctx = _two_commits(tmp_path, _pinned({}, lock=_lock()),
                           _pinned({hostile: hostile}, lock=_lock()))
        lines = repin.net_change_lines(ctx)
        text = "\n".join(lines)
        assert len(lines) == 4, lines              # three headings and the one changed key: no key split a line
        assert "\x1b" not in text and "\\x1b" in text

    @pytest.mark.parametrize("what,after,needle", [
        ("a pinned file the candidate lacks", _pinned({"a": 1}), "has no " + _LOCK),
        ("a pinned file that is not JSON", {**_pinned({"a": 1}, lock=_lock()), _BASELINE: "not json"},
         "cannot be read as keys and values"),
    ])
    def test_a_pinned_file_the_candidate_lacks_or_cannot_be_read_refuses(
            self, repin, tmp_path, what, after, needle):
        ctx = _two_commits(tmp_path, _pinned({"a": 1}, lock=_lock()), after)
        with pytest.raises(repin.Refuse) as exc:
            repin.net_change_lines(ctx)
        assert needle in str(exc.value), what

    @pytest.mark.parametrize("what,before,after,needle", [
        ("a candidate lock that repeats a destination, the last copy equal to the anchor's",
         _pinned({"a": 1}, lock=_lock_records(_record("x", "A"))),
         _pinned({"a": 1}, lock=_lock_records(_record("x", "B"), _record("x", "A"))),
         "lists the destination x more than once"),
        ("an anchor lock that repeats a destination",
         _pinned({"a": 1}, lock=_lock_records(_record("x", "A"), _record("x", "B"))),
         _pinned({"a": 1}, lock=_lock_records(_record("x", "B"))),
         "lists the destination x more than once"),
        ("a baseline file that repeats a JSON key",
         _pinned({"a": 1}, lock=_lock()),
         {**_pinned({"a": 1}, lock=_lock()), _BASELINE: '{"a": 1, "a": 2}'},
         "repeats a JSON key"),
        ("a lock record that repeats a JSON key",
         _pinned({"a": 1}, lock=_lock_records(_record("x", "A"))),
         _pinned({"a": 1}, lock='# header\n{"files": [{"dst": "x", "hash": "sha256:B", "hash": "sha256:A"}]}\n'),
         "repeats a JSON key"),
    ])
    def test_a_repeated_lock_destination_or_json_key_refuses_because_the_display_would_hide_a_copy(
            self, repin, tmp_path, what, before, after, needle):
        ctx = _two_commits(tmp_path, before, after)
        with pytest.raises(repin.Refuse) as exc:
            repin.net_change_lines(ctx)
        assert needle in str(exc.value) and "Nothing was run" in str(exc.value), what

    def test_a_lock_with_distinct_destinations_still_shows_its_net_change(self, repin, tmp_path):
        before = _pinned({"a": 1}, lock=_lock_records(_record("a", "A"), _record("b", "B"), _record("c", "C")))
        after = _pinned({"a": 1}, lock=_lock_records(_record("a", "A2"), _record("b", "B"), _record("d", "D")))
        lines = repin.net_change_lines(_two_commits(tmp_path, before, after))
        assert f"{_LOCK}: 3 changed" in lines and f"{_BASELINE}: no change" in lines
        assert sum(line.startswith("  cairn-lock.yml") for line in lines) == 3, lines    # a changed, c dropped, d added


class TestThePrintedCeremonyCommandIsTheOneYouWereGiven:

    @pytest.mark.parametrize("flag", ["--check-only", "--check", "--check-o"])
    def test_check_only_is_removed_and_everything_else_is_kept(self, repin, flag):
        given = ["ceremony", "--transition", "--expected-fingerprint", "SHA256:x", flag,
                 "--values", "v", "--ceremony-dir", "c"]
        command = repin.ceremony_command(given)
        assert command == [sys.executable, "-I", str(_REPO / "release" / "repin.py"), "ceremony", "--transition",
                           "--expected-fingerprint", "SHA256:x", "--values", "v", "--ceremony-dir", "c"]

