"""The upgrade edit check runs no program a project's git settings name.

`upgrade --stage`, `--apply` and a bare `--finalize` ask whether the files they
are about to overwrite or hash have unsaved edits. Asking `git status` would run
whatever the project's `.git/config` names (a file-system monitor, a clean
filter, a pager), so the engine asks git only for the index and the last commit,
through one launcher that removes every route a project has to run a program, and
reads the working files itself.

The tests call the helpers directly where the property is local, and drive the
real `scaffold.py upgrade` entry point where it is the callers' behaviour. A
stand-in `git` first on `PATH` logs every call, so a test can say which commands
ran, and which did not.
"""

from __future__ import annotations

import hashlib
import os
import stat
import subprocess
import sys
import threading
import time
import warnings
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap._scaffold import upgrade as U  # noqa: E402

posix_only = pytest.mark.skipif(
    os.name == "nt", reason="needs POSIX modes, links and shell stand-ins")


@pytest.fixture(autouse=True)
def _forget_the_git_version(monkeypatch: pytest.MonkeyPatch) -> None:
    """Read `git --version` afresh in every node (it is cached per process)."""
    monkeypatch.setattr(U, "_GIT_FLOOR_MET", None)


def _blob_id(data: bytes, algorithm: str = "sha1") -> str:
    header = b"blob %d\0" % len(data)
    if algorithm == "sha1":
        return hashlib.sha1(header + data, usedforsecurity=False).hexdigest()
    return hashlib.sha256(header + data).hexdigest()


# ---------------------------------------------------------------------------
# The working-file comparison
# ---------------------------------------------------------------------------

BODY = b"print('shipped')\n"


def _differs(project: Path, name: str = "f.py", *, mode: str = "100644",
             data: bytes = BODY, check_mode: bool = True,
             fold_crlf: bool = False) -> bool:
    return U._working_file_differs(
        project.resolve(), name, mode, _blob_id(data), check_mode, fold_crlf)


def test_an_unchanged_file_does_not_differ_and_one_changed_byte_does(
    tmp_path: Path,
) -> None:
    (tmp_path / "f.py").write_bytes(BODY)
    assert _differs(tmp_path) is False
    (tmp_path / "f.py").write_bytes(BODY + b"#")
    assert _differs(tmp_path) is True
    (tmp_path / "f.py").unlink()
    assert _differs(tmp_path) is True, "a missing file is an edit"
    (tmp_path / "f.py").mkdir()
    assert _differs(tmp_path) is True, "a folder at the name is an edit"


@posix_only
def test_a_link_in_the_path_counts_as_edited_and_a_fifo_does_not_block(
    tmp_path: Path,
) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "f.py").write_bytes(BODY)
    project = tmp_path / "project"
    project.mkdir()
    # Every file below holds exactly the indexed bytes, so only the link or the
    # special file can make the answer "edited".
    (project / "real.py").write_bytes(BODY)
    (project / "f.py").symlink_to(project / "real.py")
    assert _differs(project, "f.py") is True, "a link at the name"
    (project / "linked").symlink_to(outside)
    assert _differs(project, "linked/f.py") is True, "a linked parent folder"
    assert (project / "linked" / "f.py").read_bytes() == BODY, "the control reads through"
    os.mkfifo(project / "pipe.py")
    answers: list[bool] = []
    reader = threading.Thread(
        target=lambda: answers.append(_differs(project, "pipe.py")), daemon=True)
    reader.start()
    reader.join(5)
    if reader.is_alive():
        # Free the blocked reader before failing, so the node does not hang the run.
        fd = os.open(project / "pipe.py", os.O_WRONLY | os.O_NONBLOCK)
        os.close(fd)
        reader.join(5)
        pytest.fail("reading a FIFO blocked")
    assert answers == [True]


def test_a_file_is_hashed_the_way_git_hashes_a_blob(tmp_path: Path) -> None:
    data = b"one\ntwo\r\nthree"
    for number, (algorithm, init) in enumerate(
            (("sha1", ["init", "-q"]),
             ("sha256", ["init", "-q", "--object-format=sha256"]))):
        repository = tmp_path / algorithm
        repository.mkdir()
        made = subprocess.run(["git", "-C", str(repository), *init],
                              capture_output=True, text=True)
        if made.returncode != 0:
            assert number == 1, made.stderr
            warnings.warn(
                "this git has no --object-format=sha256; the SHA-256 arm did not run",
                stacklevel=1)
            continue
        (repository / "f.bin").write_bytes(data)
        expected = subprocess.run(
            ["git", "-C", str(repository), "hash-object", "--no-filters", "f.bin"],
            capture_output=True, text=True, check=True).stdout.strip()
        assert len(expected) == (40 if algorithm == "sha1" else 64)
        assert U._working_file_differs(
            repository.resolve(), "f.bin", "100644", expected, True, False) is False
        assert U._working_file_differs(
            repository.resolve(), "f.bin", "100644", "0" * len(expected), True, False) is True


@posix_only
def test_a_mode_only_edit_counts_unless_filemode_is_off(tmp_path: Path) -> None:
    path = tmp_path / "f.py"
    path.write_bytes(BODY)

    def answer(mode: str, bits: int, check_mode: bool = True) -> bool:
        path.chmod(bits)
        return _differs(tmp_path, mode=mode, check_mode=check_mode)

    assert answer("100755", 0o644) is True, "the entry says executable, the file is not"
    assert answer("100644", 0o755) is True, "the file is executable, the entry says not"
    assert answer("100755", 0o755) is False
    assert answer("100644", 0o644) is False
    assert answer("100644", 0o654) is False, "only the owner bit counts"
    assert answer("100755", 0o064) is True
    assert answer("100755", 0o644, check_mode=False) is False, "filemode is off"
    assert answer("100644", 0o755, check_mode=False) is False


def test_line_endings_difference_counts_as_unchanged_only_when_asked(
    tmp_path: Path,
) -> None:
    lf = b"a\nb\n"
    path = tmp_path / "f.py"
    path.write_bytes(b"a\r\nb\r\n")
    assert _differs(tmp_path, data=lf, fold_crlf=False) is True
    assert _differs(tmp_path, data=lf, fold_crlf=True) is False
    path.write_bytes(b"a\r\nb\r\nc\r\n")
    assert _differs(tmp_path, data=lf, fold_crlf=True) is True, "a real edit still counts"
    path.write_bytes(b"a\rb\r")
    assert _differs(tmp_path, data=lf, fold_crlf=True) is True, "a lone CR is not CRLF"
    path.write_bytes(b"a\r\nb\r\n")
    assert _differs(tmp_path, data=b"a\r\nb\r\n", fold_crlf=False) is False, "equal bytes"


def test_an_index_entry_that_is_not_a_plain_file_is_edited(tmp_path: Path) -> None:
    (tmp_path / "f.py").write_bytes(BODY)
    assert _differs(tmp_path) is False, "the control"
    for mode in ("120000", "160000", "100664", "040000", ""):
        assert _differs(tmp_path, mode=mode) is True, mode


# ---------------------------------------------------------------------------
# A real project, and a stand-in `git` that logs what is asked of it
# ---------------------------------------------------------------------------

import shutil  # noqa: E402

from bootstrap import scaffold as s  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
REAL_GIT = shutil.which("git")
needs_git = pytest.mark.skipif(REAL_GIT is None, reason="needs a real git")
PROFILE = (
    "project_name: EditCheckTest\n"
    "test_command: pytest\n"
    "preset: solo-greenfield\n"
)
IDENTITY = ["-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"]


def _git(project: Path, *args: str, check: bool = True) -> str:
    done = subprocess.run(
        ["git", "-C", str(project), *IDENTITY, *args],
        capture_output=True, text=True, check=check)
    return done.stdout.strip()


def _commit_all(project: Path, message: str = "state") -> None:
    _git(project, "add", "-A")
    _git(project, "commit", "-q", "--allow-empty", "-m", message)


@pytest.fixture(scope="module")
def pristine_install(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A fresh install of this Cairn, committed in git; tests copy it."""
    base = tmp_path_factory.mktemp("pristine")
    target = base / "project"
    target.mkdir()
    profile = base / "profile.yml"
    profile.write_text(PROFILE, encoding="utf-8")
    assert s.main(["--config", str(profile), "--target", str(target),
                   "--cairn-root", str(ROOT), "--allow-dev"]) == 0
    _git(target, "init", "-q", "-b", "main")
    _commit_all(target, "install")
    return target


@pytest.fixture
def project(pristine_install: Path, tmp_path: Path) -> Path:
    copy = tmp_path / "project"
    shutil.copytree(pristine_install, copy, symlinks=True)
    return copy


def _upgrade(capsys: pytest.CaptureFixture[str], project: Path, *flags: str,
             ) -> tuple[int, str, str]:
    code = s.main(["upgrade", "--target", str(project), *flags,
                   "--cairn-root", str(ROOT)])
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def _diverge_agents(project: Path) -> None:
    """Edit AGENTS.md (and its cached base) so an upgrade stages a change to it.

    The file is then uncommitted: the write-set and the unsaved edit overlap."""
    base = project / "dev" / ".cairn" / "base" / "AGENTS.md"
    base.write_text(base.read_text().replace("# AGENTS.md", "# OLD", 1))
    agents = project / "AGENTS.md"
    agents.write_text(
        agents.read_text().replace("# AGENTS.md", "# OLD", 1) + "\n<!-- keep me -->\n")


def _stage(capsys: pytest.CaptureFixture[str], project: Path) -> None:
    code, out, err = _upgrade(capsys, project, "--stage")
    assert code == 0, (out, err)


def _stand_in_git(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *,
                  version: str = "git version 2.54.0 (Apple Git-157)",
                  answers: dict[str, str] | None = None,
                  ignore_lazy_fetch: bool = False,
                  name: str = "standin") -> Path:
    """Put a `git` first on `PATH` that logs every call, then runs the real git.

    *answers* maps a call, written `<subcommand> <first argument after it>` as a
    shell `case` pattern (for example `ls-files*` or `rev-parse --verify`), to a
    shell snippet that replaces the real git for that call. Each call writes
    `<n>.argv` and `<n>.env` under the returned folder; global options (`-C`,
    `-c`, `--literal-pathspecs`) are skipped to find the subcommand.
    *ignore_lazy_fetch* makes the stand-in behave like a git that does not know
    `GIT_NO_LAZY_FETCH`: the real git is run with it removed."""
    log = tmp_path / name / "log"
    log.mkdir(parents=True)
    bindir = tmp_path / name / "bin"
    bindir.mkdir()
    cases = "".join(f"  {pattern.replace(' ', chr(92) + ' ')}) {snippet};;\n"
                    for pattern, snippet in (answers or {}).items())
    script = bindir / "git"
    script.write_text(
        "#!/bin/sh\n"
        f"n=$(ls '{log}'/*.argv 2>/dev/null | wc -l | tr -d ' ')\n"
        f"for a in \"$@\"; do printf '%s\\n' \"$a\"; done > '{log}'/$n.argv\n"
        f"env > '{log}'/$n.env\n"
        f"[ \"$1\" = --version ] && {{ printf '%s\\n' '{version}'; exit 0; }}\n"
        "parse() {\n"
        "  while [ $# -gt 0 ]; do\n"
        "    case \"$1\" in\n"
        "      -C|-c) shift 2;;\n"
        "      -*) shift;;\n"
        "      *) SUB=\"$1\"; ARG1=\"$2\"; return;;\n"
        "    esac\n"
        "  done\n"
        "}\n"
        "parse \"$@\"\n"
        "case \"$SUB $ARG1\" in\n"
        f"{cases}"
        f"  *) {'unset GIT_NO_LAZY_FETCH; ' if ignore_lazy_fetch else ''}"
        f"exec '{REAL_GIT}' \"$@\";;\n"
        "esac\n",
        encoding="utf-8")
    script.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setattr(U, "_GIT_FLOOR_MET", None)
    return log


def _logged_calls(log: Path) -> list[list[str]]:
    return [argv.read_text(encoding="utf-8").splitlines()
            for argv in sorted(log.glob("*.argv"), key=lambda p: int(p.stem))]


def _subcommand(call: list[str]) -> str:
    """`<subcommand> <first argument after it>` of one logged call."""
    rest = list(call)
    while rest:
        if rest[0] in ("-C", "-c"):
            rest = rest[2:]
        elif rest[0].startswith("-"):
            rest = rest[1:]
        else:
            return " ".join(rest[:2])
    return ""


EDIT_CHECK_COMMANDS = ("ls-files", "diff-index", "status", "config", "rev-parse --verify",
                       "rev-parse --is-inside-work-tree")


def _edit_check_calls(log: Path) -> list[str]:
    return [_subcommand(c) for c in _logged_calls(log)
            if any(_subcommand(c).startswith(k) for k in EDIT_CHECK_COMMANDS)]


# ---------------------------------------------------------------------------
# "Could not tell" is stopped or advised, never read as clean
# ---------------------------------------------------------------------------

REASON = "git did not answer within the time allowed (a stand-in sentence)"


def _cannot_tell(*_args: object, **_kwargs: object) -> object:
    raise U._EditCheckCannotTell(REASON)


@needs_git
@posix_only
def test_each_caller_stops_or_advises_when_the_check_cannot_tell(
    project: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch,
) -> None:
    _commit_all(project)
    _diverge_agents(project)
    _stage(capsys, project)
    lock_before = (project / U._LOCKFILE_REL).read_bytes()
    agents_before = (project / "AGENTS.md").read_bytes()
    monkeypatch.setattr(U, "_dirty_tracked_paths", _cannot_tell)

    code, out, err = _upgrade(capsys, project, "--apply")
    assert code == 1, (out, err)
    assert REASON in err and "--force" in err
    assert (project / "AGENTS.md").read_bytes() == agents_before, "--apply wrote anyway"
    assert (project / U._STAGING_REL).exists(), "the stage was cleaned anyway"

    code, out, err = _upgrade(capsys, project, "--finalize")
    assert code == 1, (out, err)
    assert REASON in err and "--force" in err
    assert (project / U._LOCKFILE_REL).read_bytes() == lock_before, "--finalize wrote anyway"

    code, out, err = _upgrade(capsys, project, "--stage")
    assert code == 0, (out, err)
    assert "[advisory]" in err and REASON in err and "--force" in err
    assert (project / U._STAGING_REL / "files" / "AGENTS.md").exists()


@needs_git
@posix_only
def test_force_runs_no_git(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _commit_all(project)
    _diverge_agents(project)
    _stage(capsys, project)
    log = _stand_in_git(tmp_path, monkeypatch)
    # The control: without --force the same stop-before-writing run does ask.
    code, _out, _err = _upgrade(capsys, project, "--apply")
    assert code == 1
    assert _edit_check_calls(log), "the unforced check must ask git"
    after_control = len(_logged_calls(log))
    code, out, err = _upgrade(capsys, project, "--apply", "--force")
    assert code == 0, (out, err)
    code, out, err = _upgrade(capsys, project, "--finalize", "--force")
    assert code == 0, (out, err)
    asked = [_subcommand(c) for c in _logged_calls(log)[after_control:]
             if any(_subcommand(c).startswith(k) for k in EDIT_CHECK_COMMANDS)]
    assert asked == [], f"--force asked git: {asked}"


# ---------------------------------------------------------------------------
# The prelude: is there a repository, and what do its settings say
# ---------------------------------------------------------------------------

@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A repository with one commit, the smallest project the prelude can judge."""
    folder = tmp_path / "repo"
    folder.mkdir()
    _git(folder, "init", "-q", "-b", "main")
    (folder / "a.txt").write_text("one\n")
    _commit_all(folder, "first")
    return folder.resolve()


def _first_call_is_the_version(log: Path) -> None:
    assert _logged_calls(log)[0] == ["--version"], _logged_calls(log)


@needs_git
@posix_only
def test_git_that_will_not_start_is_no_guard_and_git_that_does_not_answer_is_cannot_tell(
    repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = os.environ["PATH"]
    # Control: the repository is there and git answers.
    assert U._edit_check_prelude(repo) == (True, False, True)
    # A `.git` is present, but there is no git to ask: nothing can be guarded.
    nowhere = tmp_path / "no-git-here"
    nowhere.mkdir()
    monkeypatch.setenv("PATH", str(nowhere))
    monkeypatch.setattr(U, "_GIT_FLOOR_MET", None)
    assert U._edit_check_prelude(repo) is None
    # A git that starts and then hangs at the work-tree question: not "no guard".
    monkeypatch.setenv("PATH", path)
    monkeypatch.setattr(U, "_GIT_TIMEOUT_SECONDS", 0.5)
    log = _stand_in_git(tmp_path, monkeypatch, answers={
        "rev-parse --is-inside-work-tree": "exec sleep 5"})
    started = time.monotonic()
    with pytest.raises(U._EditCheckCannotTell):
        U._edit_check_prelude(repo)
    assert time.monotonic() - started < 4, "the check must not wait for a hung git"
    _first_call_is_the_version(log)
    # The same hang at the version question.
    log = _stand_in_git(tmp_path, monkeypatch, name="slow-version")
    (tmp_path / "slow-version" / "bin" / "git").write_text(
        "#!/bin/sh\nexec sleep 5\n", encoding="utf-8")
    with pytest.raises(U._EditCheckCannotTell):
        U._edit_check_prelude(repo)


@needs_git
@posix_only
@pytest.mark.parametrize("step", ["rev-parse --is-inside-work-tree", "config",
                                  "rev-parse --verify"])
def test_git_that_cannot_start_or_does_not_answer_at_any_step_is_no_guard_or_cannot_tell(
    repo: Path, monkeypatch: pytest.MonkeyPatch, step: str,
) -> None:
    real = U._run_git_sterile

    def fails_at_the_step(outcome: str):
        def run(args: list[str], limit: int) -> object:
            return outcome if step in " ".join(args) else real(args, limit)
        return run

    assert U._edit_check_prelude(repo) == (True, False, True), "the control"
    monkeypatch.setattr(U, "_run_git_sterile", fails_at_the_step(U._GIT_NOT_STARTED))
    assert U._edit_check_prelude(repo) is None
    monkeypatch.setattr(U, "_run_git_sterile", fails_at_the_step(U._GIT_NO_ANSWER))
    with pytest.raises(U._EditCheckCannotTell):
        U._edit_check_prelude(repo)


@needs_git
@posix_only
def test_a_repository_git_will_not_confirm_is_cannot_tell_and_no_repository_is_no_guard(
    repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _git(repo, "config", "core.bare", "true")
    with pytest.raises(U._EditCheckCannotTell):
        U._edit_check_prelude(repo)
    _git(repo, "config", "core.bare", "false")
    assert U._edit_check_prelude(repo) == (True, False, True), "the control"
    log = _stand_in_git(tmp_path, monkeypatch, answers={
        "rev-parse --is-inside-work-tree": "exit 128"})
    with pytest.raises(U._EditCheckCannotTell):
        U._edit_check_prelude(repo)
    _first_call_is_the_version(log)
    plain = tmp_path / "plain"
    plain.mkdir()
    assert not any(os.path.lexists(folder / ".git") for folder in (plain, *plain.parents))
    before = len(_logged_calls(log))
    assert U._edit_check_prelude(plain.resolve()) is None
    assert len(_logged_calls(log)) == before, "with no .git anywhere git is not asked"


CONFIG_CASES = [
    ("no key at all", None, 1, (True, False, True)),
    ("filemode false", b"core.filemode\nfalse\0", 0, (False, False, True)),
    ("filemode valueless is true", b"core.filemode\0", 0, (True, False, True)),
    ("filemode zero", b"core.filemode\n0\0", 0, (False, False, True)),
    ("filemode non-zero number", b"core.filemode\n2\0", 0, (True, False, True)),
    ("filemode empty is false", b"core.filemode\n\0", 0, (False, False, True)),
    ("last filemode wins, true", b"core.filemode\nfalse\0core.filemode\ntrue\0", 0,
     (True, False, True)),
    ("last filemode wins, false", b"core.filemode\ntrue\0core.filemode\nOFF\0", 0,
     (False, False, True)),
    ("filemode banana", b"core.filemode\nbanana\0", "raises", None),
    ("autocrlf true", b"core.autocrlf\ntrue\0", 0, (True, True, True)),
    ("autocrlf valueless is true", b"core.autocrlf\0", 0, (True, True, True)),
    ("autocrlf input is not crlf", b"core.autocrlf\ninput\0", 0, (True, False, True)),
    ("autocrlf false", b"core.autocrlf\nfalse\0", 0, (True, False, True)),
    ("autocrlf maybe", b"core.autocrlf\nmaybe\0", "raises", None),
    ("eol crlf", b"core.eol\nCRLF\0", 0, (True, True, True)),
    ("eol lf", b"core.eol\nlf\0", 0, (True, False, True)),
    ("eol native follows the platform", b"core.eol\nnative\0", 0,
     (True, os.name == "nt", True)),
    ("eol unknown", b"core.eol\nweird\0", "raises", None),
    ("eol valueless", b"core.eol\0", "raises", None),
    ("autocrlf input with eol crlf", b"core.autocrlf\ninput\0core.eol\ncrlf\0", 0,
     (True, True, True)),
    ("the config call fails", None, 129, "raises"),
    ("the config call fails with 2", b"core.filemode\nfalse\0", 2, "raises"),
]


@needs_git
@posix_only
@pytest.mark.parametrize("label, output, code, expected", CONFIG_CASES,
                         ids=[c[0] for c in CONFIG_CASES])
def test_the_config_answer_is_read_as_git_reads_it(
    repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    label: str, output: bytes | None, code: int | str, expected: object,
) -> None:
    answer = tmp_path / "config-answer"
    answer.write_bytes(output or b"")
    exit_code = code if isinstance(code, int) else 0
    expected = "raises" if code == "raises" else expected
    log = _stand_in_git(tmp_path, monkeypatch, answers={
        "config*": f"cat '{answer}'; exit {exit_code}"})
    if expected == "raises" or expected is None and code not in (0, 1):
        with pytest.raises(U._EditCheckCannotTell):
            U._edit_check_prelude(repo)
    else:
        assert U._edit_check_prelude(repo) == expected
    _first_call_is_the_version(log)


def _treeless_clone(tmp_path: Path, name: str) -> Path:
    """A clone that holds the commits but not the folder listings, with no
    checkout: reading its last commit's tree makes git fetch from the origin."""
    origin = tmp_path / f"{name}-origin"
    origin.mkdir()
    _git(origin, "init", "-q", "-b", "main")
    _git(origin, "config", "uploadpack.allowFilter", "true")
    _git(origin, "config", "uploadpack.allowAnySHA1InWant", "true")
    (origin / "a.txt").write_text("one\n")
    _commit_all(origin, "first")
    clone = tmp_path / f"{name}-clone"
    subprocess.run(["git", "clone", "-q", "--filter=tree:0", "--no-checkout",
                    origin.as_uri(), str(clone)], check=True, capture_output=True)
    return clone.resolve()


def _fetch_marker(clone: Path, marker: Path) -> None:
    """Make the clone's remote run a program that leaves *marker* behind."""
    exec_path = subprocess.run(["git", "--exec-path"], capture_output=True, text=True,
                               check=True).stdout.strip()
    program = clone.parent / (clone.name + "-uploadpack.sh")
    program.write_text(
        f"#!/bin/sh\ntouch '{marker}'\nexec '{exec_path}/git-upload-pack' \"$@\"\n")
    program.chmod(0o755)
    _git(clone, "config", "remote.origin.uploadpack", str(program))


PARTIAL_CLONE_KEYS = [
    ("extensions.partialclone", "origin"),
    ("remote.origin.promisor", "true"),
    ("remote.origin.partialclonefilter", "tree:0"),
    ("core.partialclonefilter", "tree:0"),
]


@needs_git
@posix_only
@pytest.mark.parametrize("key, value", PARTIAL_CLONE_KEYS, ids=[k for k, _ in PARTIAL_CLONE_KEYS])
def test_below_the_floor_a_partial_clone_answers_cannot_tell_and_runs_no_program(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, key: str, value: str,
) -> None:
    clone = _treeless_clone(tmp_path, "case")
    own = {"extensions.partialclone", "remote.origin.promisor", "remote.origin.partialclonefilter"}
    for other in own - {key}:
        _git(clone, "config", "--unset", other, check=False)
    _git(clone, "config", key, value)
    marker = tmp_path / "program-ran"
    _fetch_marker(clone, marker)
    log = _stand_in_git(tmp_path, monkeypatch, version="git version 2.44.0",
                        ignore_lazy_fetch=True)
    with pytest.raises(U._EditCheckCannotTell):
        U._edit_check_prelude(clone)
    _first_call_is_the_version(log)
    later = [_subcommand(c) for c in _logged_calls(log)
             if _subcommand(c).split(" ")[0] in ("ls-files", "diff-index")
             or _subcommand(c).startswith("rev-parse --verify")]
    assert later == [], later
    assert not marker.exists(), "a program the project names ran"


@needs_git
@posix_only
def test_below_the_floor_a_project_with_no_partial_clone_setting_is_still_guarded(
    repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    log = _stand_in_git(tmp_path, monkeypatch, version="git version 2.44.0")
    assert U._edit_check_prelude(repo) == (True, False, True)
    _first_call_is_the_version(log)


@needs_git
@posix_only
def test_the_launcher_is_shared_with_the_committed_copy_check(
    repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "elsewhere"))
    monkeypatch.setenv("GIT_NO_LAZY_FETCH", "0")
    monkeypatch.setenv("git_ssh_command", "lower-case spelling")
    log = _stand_in_git(tmp_path, monkeypatch)
    assert U._committed_copy_matches(repo, "a.txt", b"one\n") is True
    assert U._edit_check_prelude(repo) == (True, False, True)
    _first_call_is_the_version(log)
    calls = _logged_calls(log)
    numbered = [(n, c) for n, c in enumerate(calls) if c != ["--version"]]
    cat_file = [(n, c) for n, c in numbered if "cat-file" in c]
    prelude = [(n, c) for n, c in numbered if "cat-file" not in c]
    assert len(cat_file) == 1 and len(prelude) >= 3

    def environment(n: int) -> dict[str, str]:
        lines = (log / f"{n}.env").read_text(encoding="utf-8").splitlines()
        return {k: v for k, v in (l.split("=", 1) for l in lines if "=" in l)
                if k.upper().startswith("GIT_")}

    prefix = cat_file[0][1][:8]
    assert prefix == ["-C", str(repo), "-c", "core.fsmonitor=false",
                      "-c", f"core.hooksPath={os.devnull}",
                      "-c", "core.useReplaceRefs=false"][:8]
    wanted = {"GIT_NO_LAZY_FETCH": "1", "GIT_TERMINAL_PROMPT": "0", "GIT_OPTIONAL_LOCKS": "0"}
    for n, call in [cat_file[0], *prelude]:
        assert call[:8] == prefix, call
        assert environment(n) == wanted, (call, environment(n))


# ---------------------------------------------------------------------------
# The check itself
# ---------------------------------------------------------------------------

def _write(path: Path, text: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))


def _edited_project(project: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Commit the install, edit AGENTS.md, and stage an upgrade that rewrites it."""
    _commit_all(project)
    _diverge_agents(project)
    _stage(capsys, project)


def _version_precedes_the_check(log: Path) -> None:
    """The version floor is read before the first question about the repository."""
    kinds = [_subcommand(c) or c[0] for c in _logged_calls(log)]
    asked = [n for n, kind in enumerate(kinds) if kind.split(" ")[0] in
             ("rev-parse", "config", "ls-files", "diff-index", "status")]
    assert asked and "--version" in kinds[:asked[0]], kinds


FAILURES = {
    "hang": "exec sleep 5",
    "over the cap": "head -c 3000000 /dev/zero; exit 0",
}
STEPS = {
    "settings": ("config*", 2),
    "last commit": ("rev-parse --verify", 2),
    "index": ("ls-files*", 1),
    "comparison": ("diff-index*", 1),
}


@needs_git
@posix_only
@pytest.mark.parametrize("failure", [*FAILURES, "non-zero exit"])
@pytest.mark.parametrize("step", list(STEPS))
def test_every_git_step_that_fails_is_cannot_tell(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch, step: str, failure: str,
) -> None:
    pattern, bad_exit = STEPS[step]
    snippet = FAILURES.get(failure, f"exit {bad_exit}")
    _edited_project(project, capsys)
    agents = (project / "AGENTS.md").read_bytes()
    monkeypatch.setattr(U, "_GIT_TIMEOUT_SECONDS", 0.5)
    log = _stand_in_git(tmp_path, monkeypatch, answers={pattern: snippet})
    code, out, err = _upgrade(capsys, project, "--apply")
    assert code == 1, (out, err)
    assert "could not tell" in err and "--force" in err, err
    assert (project / "AGENTS.md").read_bytes() == agents, "--apply wrote anyway"
    assert (project / U._STAGING_REL).exists()
    _version_precedes_the_check(log)


@needs_git
@posix_only
def test_the_unfailing_stand_in_lets_the_check_find_the_edit(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The control for the failing steps: the same stand-in, answering nothing
    itself, leaves the real refusal (the file named, no "could not tell")."""
    _edited_project(project, capsys)
    log = _stand_in_git(tmp_path, monkeypatch)
    code, out, err = _upgrade(capsys, project, "--apply")
    assert code == 1, (out, err)
    assert "AGENTS.md" in err and "could not tell" not in err
    _version_precedes_the_check(log)


@needs_git
@posix_only
@pytest.mark.parametrize("failure", ["non-zero exit", "over the cap", "hang"])
@pytest.mark.parametrize("step", ["index", "comparison"])
def test_a_failure_in_a_later_group_is_cannot_tell(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, step: str, failure: str,
) -> None:
    repository = tmp_path / "many"
    repository.mkdir()
    _git(repository, "init", "-q", "-b", "main")
    names = [f"f{n:03d}.txt" for n in range(150)]
    for name in names:
        _write(repository / name, name)
    _commit_all(repository)
    repository = repository.resolve()
    counter = tmp_path / "count"
    pattern = STEPS[step][0]
    fail = {"non-zero exit": "exit 1", **FAILURES}[failure]
    monkeypatch.setattr(U, "_GIT_TIMEOUT_SECONDS", 0.5)
    snippet = (f"n=$(cat '{counter}' 2>/dev/null || echo 0); echo $((n+1)) > '{counter}'; "
               f"if [ \"$n\" -ge 1 ]; then {fail}; fi; exec '{REAL_GIT}' \"$@\"")
    log = _stand_in_git(tmp_path, monkeypatch, answers={pattern: snippet})
    with pytest.raises(U._EditCheckCannotTell):
        U._dirty_tracked_paths(repository, names)
    assert int(counter.read_text()) == 2, "the first group must have answered"
    _version_precedes_the_check(log)


@needs_git
@posix_only
def test_apply_goes_on_with_no_git_and_stops_when_git_does_not_answer(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _edited_project(project, capsys)
    path = os.environ["PATH"]
    nowhere = tmp_path / "no-git-here"
    nowhere.mkdir()
    # A `.git` is there and the edit is real, but there is no git to ask.
    monkeypatch.setenv("PATH", str(nowhere))
    monkeypatch.setattr(U, "_GIT_FLOOR_MET", None)
    assert U._dirty_tracked_paths(project, ["AGENTS.md"]) is None
    # The same project, a git that hangs at the work-tree question.
    monkeypatch.setenv("PATH", path)
    monkeypatch.setattr(U, "_GIT_TIMEOUT_SECONDS", 0.5)
    log = _stand_in_git(tmp_path, monkeypatch, answers={
        "rev-parse --is-inside-work-tree": "exec sleep 5"})
    code, out, err = _upgrade(capsys, project, "--apply")
    assert code == 1 and "could not tell" in err and "--force" in err, (out, err)
    _version_precedes_the_check(log)


def _program(folder: Path, name: str, marker: Path, body: str = "") -> Path:
    """A program that leaves *marker* behind when it runs."""
    program = folder / name
    program.write_text(f"#!/bin/sh\ntouch '{marker}'\n{body}\n", encoding="utf-8")
    program.chmod(0o755)
    return program


@needs_git
@posix_only
def test_git_config_programs_never_run_during_stage_apply_or_finalize(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    programs = tmp_path / "programs"
    programs.mkdir()
    markers = {kind: tmp_path / f"ran-{kind}" for kind in
               ("monitor", "filter", "textconv", "external", "pager", "hook")}
    _write(project / ".gitattributes", "* filter=mark diff=mark\n")
    _commit_all(project)
    for kind, config in (
            ("monitor", ("core.fsmonitor", "{}")), ("filter", ("filter.mark.clean", "{} %f")),
            ("textconv", ("diff.mark.textconv", "{}")), ("external", ("diff.external", "{}")),
            ("pager", ("core.pager", "{}"))):
        body = "cat" if kind in ("filter", "textconv") else ""
        program = _program(programs, kind, markers[kind], body)
        _git(project, "config", config[0], config[1].format(program))
    hook = _program(programs, "hook", markers["hook"])
    _git(project, "config", "core.hooksPath", str(programs))
    for name in ("pre-commit", "post-checkout", "post-index-change"):
        (programs / name).write_bytes(hook.read_bytes())
        (programs / name).chmod(0o755)
    # The control: git's own `status` and `diff` do run the project's programs.
    _diverge_agents(project)
    subprocess.run(["git", "-C", str(project), "status", "--porcelain"],
                   capture_output=True, check=True)
    for flags in ([], ["--no-ext-diff"]):
        subprocess.run(["git", "-C", str(project), "diff", *flags, "HEAD"],
                       capture_output=True, check=True)
    ran = {kind for kind, marker in markers.items() if marker.exists()}
    assert {"monitor", "filter", "textconv", "external"} <= ran, ran
    for marker in markers.values():
        marker.unlink(missing_ok=True)
    assert _upgrade(capsys, project, "--stage")[0] == 0
    code, _out, err = _upgrade(capsys, project, "--apply")
    assert code == 1 and "AGENTS.md" in err, err
    code, _out, err = _upgrade(capsys, project, "--finalize")
    assert code == 1 and "AGENTS.md" in err, err
    assert [k for k, marker in markers.items() if marker.exists()] == []


def _subfolder_project(tmp_path: Path) -> tuple[Path, Path]:
    """A repository whose root is above the project: (root, project)."""
    root = tmp_path / "root"
    project = root / "sub" / "proj"
    project.mkdir(parents=True)
    _git(root, "init", "-q", "-b", "main")
    return root.resolve(), project.resolve()


@needs_git
@posix_only
def test_a_subfolder_project_sees_its_own_edits(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    root, project = _subfolder_project(tmp_path)
    for name in ("clean.txt", "worked.txt", "staged.txt", "d/inner.txt"):
        _write(project / name, name)
    _write(root / "outside.txt", "outside")
    _commit_all(root)
    _write(project / "worked.txt", "edited in the working tree")
    _write(project / "staged.txt", "edited and staged")
    _git(root, "add", "sub/proj/staged.txt")
    _write(root / "outside.txt", "an edit above the project")
    names = ["clean.txt", "worked.txt", "staged.txt", "d/inner.txt", "outside.txt"]
    assert U._dirty_tracked_paths(project, names) == {"worked.txt", "staged.txt"}


def _states_repository(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    """A repository with one file in each edit state `git status` tells apart.

    Returns the repository and a map from file name to the state it is in."""
    repository = tmp_path / "states"
    repository.mkdir()
    _git(repository, "init", "-q", "-b", "main")
    base = {name: f"{name}\n" for name in (
        "clean.txt", "modified.txt", "staged.txt", "reverted.txt", "deleted.txt",
        "staged_delete.txt", "typechange.txt", "a[b]*.txt", "pat.txt", ":(top)pat.txt",
        "conflict.txt", "decoy.txt")}
    for name, text in base.items():
        _write(repository / name, text)
    _write(repository / ".gitignore", "ignored.txt\n")
    _commit_all(repository, "base")
    _git(repository, "checkout", "-q", "-b", "other")
    _write(repository / "conflict.txt", "other side\n")
    _commit_all(repository, "other")
    _git(repository, "checkout", "-q", "main")
    _write(repository / "conflict.txt", "our side\n")
    _commit_all(repository, "ours")
    _git(repository, "merge", "-q", "other", check=False)
    # The working file is put back to the common ancestor's text: only the
    # unresolved index entries (and git's own bookkeeping) still say "conflict".
    _write(repository / "conflict.txt", base["conflict.txt"])
    states = {"conflict.txt": "conflict"}
    _write(repository / "modified.txt", "modified in the working tree\n")
    states["modified.txt"] = "modified"
    _write(repository / "staged.txt", "staged edit\n")
    _git(repository, "add", "--", "staged.txt")
    states["staged.txt"] = "staged"
    _write(repository / "reverted.txt", "staged edit\n")
    _git(repository, "add", "--", "reverted.txt")
    _write(repository / "reverted.txt", base["reverted.txt"])
    states["reverted.txt"] = "staged then reverted"
    (repository / "deleted.txt").unlink()
    states["deleted.txt"] = "deleted"
    _git(repository, "rm", "-q", "--", "staged_delete.txt")
    states["staged_delete.txt"] = "staged delete"
    _write(repository / "staged_add.txt", "new\n")
    _git(repository, "add", "--", "staged_add.txt")
    states["staged_add.txt"] = "staged add"
    (repository / "typechange.txt").unlink()
    (repository / "typechange.txt").symlink_to("clean.txt")
    states["typechange.txt"] = "type change to a link"
    _write(repository / "a[b]*.txt", "pattern characters, edited\n")
    states["a[b]*.txt"] = "pattern characters"
    _write(repository / ":(top)pat.txt", "magic prefix, edited\n")
    states[":(top)pat.txt"] = "magic prefix"
    _write(repository / "scratch.txt", "untracked\n")
    _write(repository / "ignored.txt", "ignored\n")
    return repository.resolve(), states


def _status_edited(repository: Path) -> set[str]:
    """What plain `git status` calls edited: everything but untracked and ignored."""
    done = subprocess.run(["git", "-C", str(repository), "status", "--porcelain", "-z"],
                          capture_output=True, check=True)
    names = set()
    for record in done.stdout.split(b"\0"):
        if record and record[:2] not in (b"??", b"!!"):
            names.add(record[3:].decode("utf-8"))
    return names


@needs_git
@posix_only
def test_the_check_agrees_with_git_status_on_each_edit_state(tmp_path: Path) -> None:
    repository, states = _states_repository(tmp_path)
    asked = ["clean.txt", "decoy.txt", "pat.txt", "scratch.txt", "ignored.txt", ".gitignore",
             "gone.txt", *states]
    expected = _status_edited(repository)
    assert expected == set(states), (expected, states)
    assert U._dirty_tracked_paths(repository, asked) == expected
    # No commit yet: every name in the index counts as staged, as `git status` says.
    fresh = tmp_path / "fresh"
    fresh.mkdir()
    _git(fresh, "init", "-q", "-b", "main")
    _write(fresh / "added.txt", "a")
    _write(fresh / "loose.txt", "b")
    _git(fresh, "add", "--", "added.txt")
    assert _status_edited(fresh.resolve()) == {"added.txt"}
    assert U._dirty_tracked_paths(fresh.resolve(), ["added.txt", "loose.txt"]) == {"added.txt"}


@needs_git
@posix_only
def test_pattern_characters_in_a_name_match_literally(tmp_path: Path) -> None:
    repository, _states = _states_repository(tmp_path)
    for name in ("a[b]*.txt", ":(top)pat.txt"):
        assert U._dirty_tracked_paths(repository, [name]) == {name}, name
    assert U._dirty_tracked_paths(repository, ["pat.txt"]) == set(), "the decoy stays clean"
    # Staged and left as staged: the working file now equals the index, so only the
    # comparison with the last commit can see the edit.
    for name in ("a[b]*.txt", ":(top)pat.txt"):
        subprocess.run(["git", "--literal-pathspecs", "-C", str(repository), "add", "--", name],
                       check=True, capture_output=True)
        assert U._dirty_tracked_paths(repository, [name]) == {name}, name


@needs_git
@posix_only
def test_a_staged_then_reverted_file_counts_as_edited(tmp_path: Path) -> None:
    repository = tmp_path / "r"
    repository.mkdir()
    _git(repository, "init", "-q", "-b", "main")
    for name in ("kept.txt", "staged.txt", "reverted.txt"):
        _write(repository / name, "committed\n")
    _commit_all(repository)
    _write(repository / "staged.txt", "staged\n")
    _write(repository / "reverted.txt", "staged\n")
    _git(repository, "add", "--", "staged.txt", "reverted.txt")
    _write(repository / "reverted.txt", "committed\n")
    names = ["kept.txt", "staged.txt", "reverted.txt"]
    assert U._dirty_tracked_paths(repository.resolve(), names) == {"staged.txt", "reverted.txt"}


@needs_git
@posix_only
def test_a_missing_or_untracked_name_is_handled_as_git_status_does(tmp_path: Path) -> None:
    repository = tmp_path / "r"
    repository.mkdir()
    _git(repository, "init", "-q", "-b", "main")
    _write(repository / "tracked.txt", "t")
    _write(repository / ".gitignore", "ignored.txt\n")
    _commit_all(repository)
    (repository / "tracked.txt").unlink()
    _write(repository / "untracked.txt", "u")
    _write(repository / "ignored.txt", "i")
    names = ["tracked.txt", "untracked.txt", "ignored.txt", "never-there.txt"]
    assert U._dirty_tracked_paths(repository.resolve(), names) == {"tracked.txt"}
    assert _status_edited(repository.resolve()) == {"tracked.txt"}


@needs_git
@posix_only
def test_names_not_in_git_normal_form_or_naming_a_folder_are_matched_exactly(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "r"
    repository.mkdir()
    _git(repository, "init", "-q", "-b", "main")
    for name in ("A.md", "d/b.md", "d/c.md"):
        _write(repository / name, name)
    _commit_all(repository)
    _write(repository / "A.md", "edited")
    _write(repository / "d" / "b.md", "edited")
    repository = repository.resolve()
    assert U._dirty_tracked_paths(repository, ["./A.md", "d//b.md", "d/c.md"]) == {
        "./A.md", "d//b.md"}
    assert U._dirty_tracked_paths(repository, ["d"]) == set(), "a folder is not its children"
    assert U._dirty_tracked_paths(repository, ["", "."]) == set()


@needs_git
@posix_only
def test_an_untracked_recorded_name_is_not_returned_and_no_lockfile_gives_an_empty_set(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "r"
    repository.mkdir()
    _git(repository, "init", "-q", "-b", "main")
    _write(repository / "a.txt", "a")
    _commit_all(repository)
    _write(repository / "stray.txt", "x")
    repository = repository.resolve()
    assert U._dirty_tracked_paths(repository, ["stray.txt"]) == set()
    assert U._dirty_tracked_paths(repository) == set(), "no lockfile, no names"


@needs_git
@posix_only
def test_with_no_names_the_lockfiles_recorded_names_are_asked_about(
    project: Path,
) -> None:
    _commit_all(project)
    assert U._dirty_tracked_paths(project) == set()
    _write(project / "AGENTS.md", (project / "AGENTS.md").read_text() + "\nedited\n")
    assert U._dirty_tracked_paths(project) == {"AGENTS.md"}


@needs_git
@posix_only
def test_names_go_in_groups_of_at_most_100(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = tmp_path / "r"
    repository.mkdir()
    _git(repository, "init", "-q", "-b", "main")
    names = [f"n{n:03d}.txt" for n in range(250)]
    for name in names:
        _write(repository / name, name)
    _commit_all(repository)
    log = _stand_in_git(tmp_path, monkeypatch)
    assert U._dirty_tracked_paths(repository.resolve(), names) == set()
    for command in ("ls-files", "diff-index"):
        calls = [c for c in _logged_calls(log) if _subcommand(c).startswith(command)]
        sizes = [len(c) - 1 - c.index("--") for c in calls]
        assert sizes == [100, 100, 50], (command, sizes)


@needs_git
@posix_only
def test_core_filemode_false_makes_a_mode_only_edit_not_count(tmp_path: Path) -> None:
    repository = tmp_path / "r"
    repository.mkdir()
    _git(repository, "init", "-q", "-b", "main")
    _write(repository / "run.sh", "echo hi\n")
    _commit_all(repository)
    (repository / "run.sh").chmod(0o755)
    repository = repository.resolve()
    assert U._dirty_tracked_paths(repository, ["run.sh"]) == {"run.sh"}
    assert _status_edited(repository) == {"run.sh"}
    _git(repository, "config", "core.filemode", "false")
    assert _status_edited(repository) == set()
    assert U._dirty_tracked_paths(repository, ["run.sh"]) == set()


@needs_git
@posix_only
@pytest.mark.parametrize("settings, folds", [
    ([], False),
    ([("core.autocrlf", "true")], True),
    ([("core.eol", "crlf")], True),
    ([("core.autocrlf", "input")], False),
    ([("core.autocrlf", "false"), ("core.eol", "lf")], False),
])
def test_line_endings_rule_applies_only_when_settings_ask_for_crlf(
    tmp_path: Path, settings: list[tuple[str, str]], folds: bool,
) -> None:
    repository = tmp_path / "r"
    repository.mkdir()
    _git(repository, "init", "-q", "-b", "main")
    _write(repository / "f.txt", "a\nb\n")
    _commit_all(repository)
    for key, value in settings:
        _git(repository, "config", key, value)
    _write(repository / "f.txt", b"a\r\nb\r\n")
    assert U._dirty_tracked_paths(repository.resolve(), ["f.txt"]) == (
        set() if folds else {"f.txt"})
    _write(repository / "f.txt", b"a\r\nb\r\nc\r\n")
    assert U._dirty_tracked_paths(repository.resolve(), ["f.txt"]) == {"f.txt"}


@needs_git
@posix_only
def test_a_replace_ref_cannot_hide_a_staged_edit(tmp_path: Path) -> None:
    repository = tmp_path / "r"
    repository.mkdir()
    _git(repository, "init", "-q", "-b", "main")
    _write(repository / "f.txt", "committed\n")
    _commit_all(repository, "first")
    first = _git(repository, "rev-parse", "HEAD")
    _git(repository, "checkout", "-q", "-b", "forge")
    _write(repository / "f.txt", "staged\n")
    _commit_all(repository, "forged")
    forged = _git(repository, "rev-parse", "HEAD")
    _git(repository, "checkout", "-q", "main")
    _write(repository / "f.txt", "staged\n")
    _git(repository, "add", "--", "f.txt")
    # With replace refs honoured, the last commit reads as the staged tree and the
    # staged edit disappears: git itself says the index is clean.
    _git(repository, "replace", first, forged)
    plain = subprocess.run(["git", "-C", str(repository), "diff-index", "--cached", "--raw",
                            "HEAD"], capture_output=True, text=True, check=True).stdout
    assert plain == "", "the replace ref must be live"
    assert U._dirty_tracked_paths(repository.resolve(), ["f.txt"]) == {"f.txt"}


@needs_git
@posix_only
def test_a_partial_clone_runs_no_upload_program_at_or_above_the_floor(
    tmp_path: Path,
) -> None:
    # A blobless clone with a checkout: everything the check needs is here.
    origin = tmp_path / "blob-origin"
    origin.mkdir()
    _git(origin, "init", "-q", "-b", "main")
    _git(origin, "config", "uploadpack.allowFilter", "true")
    _git(origin, "config", "uploadpack.allowAnySHA1InWant", "true")
    _write(origin / "a.txt", "one\n")
    _commit_all(origin, "first")
    blobless = tmp_path / "blobless"
    subprocess.run(["git", "clone", "-q", "--filter=blob:none", origin.as_uri(),
                    str(blobless)], check=True, capture_output=True)
    marker = tmp_path / "blobless-ran"
    _fetch_marker(blobless, marker)
    assert U._dirty_tracked_paths(blobless.resolve(), ["a.txt"]) == set()
    assert not marker.exists(), "a program the project names ran (blobless)"
    # A treeless clone with no checkout: git would have to fetch the last commit's
    # folder listings. With lazy fetch off it cannot, and the check says so.
    treeless = _treeless_clone(tmp_path, "tree")
    marker = tmp_path / "treeless-ran"
    _fetch_marker(treeless, marker)
    with pytest.raises(U._EditCheckCannotTell):
        U._dirty_tracked_paths(treeless, ["a.txt"])
    assert not marker.exists(), "a program the project names ran (treeless)"


# ---------------------------------------------------------------------------
# Bare `--finalize` asks about what it hashes, plus the lockfile
# ---------------------------------------------------------------------------

import copy  # noqa: E402

RETIRED_ROWS = {row[1]: row for row in U._RETIRED_INSTALLS}
RETIRED_SCRIPT = "scripts/onboarding_activate.py"
RETIRED_SCRIPT_2 = "scripts/foldback_suggest.py"
LIVING_STATE = "dev/PLANNING.md"


def _shipped_script(dst: str) -> bytes:
    """The last version of the retired script *dst* that Cairn shipped, from its
    git history by the blob id the engine's own list carries."""
    blob = RETIRED_ROWS[dst][3][-1][2]
    return subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob", blob],
                          capture_output=True, check=True).stdout


def _add_retired_script(project: Path, dst: str, data: bytes, *, write: bool = True) -> None:
    """Model a project from an older Cairn that still holds the retired script *dst*."""
    if write:
        _write(project / dst, data)
    digest = "sha256:" + hashlib.sha256(data).hexdigest()
    lock = s.read_lockfile(project)
    lock["files"].append({"dst": dst, "src": RETIRED_ROWS[dst][0], "verbatim": True,
                          "hash": digest, "base_hash": digest})
    (project / U._LOCKFILE_REL).write_text(s._emit_lock_yaml(lock), encoding="utf-8")


def _copy_of(project: Path, tmp_path: Path, name: str) -> Path:
    folder = tmp_path / name
    shutil.copytree(project, folder, symlinks=True)
    return folder


@needs_git
@posix_only
def test_bare_finalize_asks_about_the_records_it_hashes_and_the_lockfile(
    project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    shipped = _shipped_script(RETIRED_SCRIPT)
    _add_retired_script(project, RETIRED_SCRIPT, shipped)
    _add_retired_script(project, RETIRED_SCRIPT_2, _shipped_script(RETIRED_SCRIPT_2) + b"# mine\n")
    (project / "VENDOR.md").rename(project / "CLAUDE.md")
    _commit_all(project)

    def lets_finalize_run(name: str, edit) -> None:
        folder = _copy_of(project, tmp_path, name)
        edit(folder)
        code, out, err = _upgrade(capsys, folder, "--finalize")
        assert code == 0, (name, out, err)

    def refuses(name: str, edit, named: str) -> None:
        folder = _copy_of(project, tmp_path, name)
        edit(folder)
        lock = (folder / U._LOCKFILE_REL).read_bytes()
        code, out, err = _upgrade(capsys, folder, "--finalize")
        assert code == 1 and named in err, (name, out, err)
        assert "recorded file" in err and "tracked file" not in err
        assert (folder / U._LOCKFILE_REL).read_bytes() == lock, "a refused finalize wrote"

    def append(path: str):
        return lambda folder: (folder / path).write_text(
            (folder / path).read_text() + "\nan edit\n")

    lets_finalize_run("living-state", append(LIVING_STATE))
    lets_finalize_run("hand-deleted", lambda folder: (folder / RETIRED_SCRIPT).unlink())
    lets_finalize_run("kept-retired", lambda folder: (folder / RETIRED_SCRIPT_2).write_bytes(
        b"edited again, not committed\n"))
    refuses("hashed", append("NOTICE.md"), "NOTICE.md")
    refuses("renamed-wrapper", append("CLAUDE.md"), "CLAUDE.md")
    refuses("lockfile", lambda folder: (folder / U._LOCKFILE_REL).write_text(
        (folder / U._LOCKFILE_REL).read_text() + "# a note\n"), U._LOCKFILE_REL)

    lock = s.read_lockfile(project)
    lock["files"].append({"dst": "", "src": "core/NOTICE.md", "hash": "sha256:0"})
    lock["files"].append({"src": "core/NOTICE.md", "hash": "sha256:0"})
    before = copy.deepcopy(lock)
    names = U._finalize_hash_names(project, lock, {})
    assert lock == before, "naming the files wrote to the lock"
    assert "CLAUDE.md" in names and "VENDOR.md" not in names, "the wrapper by its on-disk name"
    assert U._LOCKFILE_REL in names and "" not in names
    assert LIVING_STATE not in names


@needs_git
@posix_only
@pytest.mark.parametrize("step", ["index", "comparison"])
def test_git_output_that_cannot_be_read_is_cannot_tell(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, step: str,
) -> None:
    repository = tmp_path / "r"
    repository.mkdir()
    _git(repository, "init", "-q", "-b", "main")
    _write(repository / "a.txt", "a")
    _commit_all(repository)
    _stand_in_git(tmp_path, monkeypatch, answers={
        STEPS[step][0]: "printf 'this is not what git prints'; exit 0"})
    with pytest.raises(U._EditCheckCannotTell):
        U._dirty_tracked_paths(repository.resolve(), ["a.txt"])
