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
    cases = "".join(f"  {pattern}) {snippet};;\n" for pattern, snippet in (answers or {}).items())
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
