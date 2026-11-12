"""Public-command and transport tests for the read-only Release check.

Promises:
- The public command reports a published release and its remote identity when the tag and gate commit agree.
- The public command refuses an absent, unpublished or wrong release, and mismatched or ambiguous remote refs.
- The public command reports a remote read failure, and refuses an invalid tag or invalid inputs before any remote read.
- The public command refuses an invalid gate commit before any git or API call, and help works without any read.
- The public command ignores hostile git configuration and proxy settings, and fails closed when git or the release read times out.
- The release read sends no credentials, encodes the tag, and refuses redirects, oversized replies, malformed fields and transport failures.
- The public command refuses a lightweight tag and malformed remote listing output.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "scripts" / "check_release_publication.py"
sys.path.insert(0, str(ROOT))

_SPEC = importlib.util.spec_from_file_location(
    "cairn_release_publication_check", SCRIPT)
assert _SPEC is not None and _SPEC.loader is not None
checker = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(checker)

OWNER = "example"
REPOSITORY = "repo"
TAG = "v1.2.3"
GATE_COMMIT = "a" * 40
TAG_OBJECT = "b" * 40
REMOTE_URL = "https://github.com/example/repo.git"


class FakeResponse:
    def __init__(self, body: bytes, status: int = 200) -> None:
        self.body = body
        self.status = status

    def getcode(self) -> int:
        return self.status

    def read(self, limit: int = -1) -> bytes:
        return self.body if limit < 0 else self.body[:limit]

    def __enter__(self):
        return self

    def __exit__(self, *_exc) -> None:
        return None


class FakeOpener:
    def __init__(self, response=None, error=None) -> None:
        self.response = response
        self.error = error
        self.calls: list[tuple[object, int]] = []

    def open(self, request, timeout: int):
        self.calls.append((request, timeout))
        if self.error is not None:
            raise self.error
        return self.response


def _release(tag: str = TAG, *, draft: object = False,
             published_at: object = "2026-10-30T12:00:00Z") -> dict:
    return {"tag_name": tag, "draft": draft,
            "published_at": published_at}


def _install_api(monkeypatch: pytest.MonkeyPatch, *, body: bytes | None = None,
                 status: int = 200, error=None) -> FakeOpener:
    if body is None:
        body = json.dumps(_release()).encode("utf-8")
    opener = FakeOpener(FakeResponse(body, status), error)
    captured_handlers: list[object] = []

    def build_opener(*handlers):
        captured_handlers[:] = handlers
        return opener

    monkeypatch.setattr(checker.urllib.request, "build_opener", build_opener)
    monkeypatch.setattr(
        checker, "_fetch_release", checker._fetch_release_in_process)
    opener.handlers = captured_handlers
    return opener


def _remote_output(tag: str = TAG, peeled: str = GATE_COMMIT,
                   tag_object: str = TAG_OBJECT) -> str:
    plain = f"refs/tags/{tag}"
    return f"{tag_object}\t{plain}\n{peeled}\t{plain}^{{}}\n"


def _stub_public_reads(monkeypatch: pytest.MonkeyPatch, *,
                       release: dict | None = None,
                       git_stdout: str | None = None,
                       git_returncode: int = 0,
                       git_stderr: str = "") -> list[list[str]]:
    _install_api(monkeypatch, body=json.dumps(
        release if release is not None else _release()).encode("utf-8"))
    seen: list[list[str]] = []
    monkeypatch.setattr(checker, "_resolve_git", lambda: Path("/test/git"))

    def fake_run_git(git, args, *, cwd, env):
        del git, cwd, env
        seen.append(list(args))
        if "check-ref-format" in args:
            return subprocess.CompletedProcess(args, 0, "", "")
        assert "ls-remote" in args
        return subprocess.CompletedProcess(
            args, git_returncode,
            _remote_output() if git_stdout is None else git_stdout,
            git_stderr,
        )

    monkeypatch.setattr(checker, "_run_git", fake_run_git)
    return seen


def _git(args: list[str], *, cwd: Path, env: dict[str, str] | None = None,
         check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=cwd, env=env, check=check,
        capture_output=True, text=True,
    )


def _local_repo(tmp_path: Path, *, annotated: bool = True,
                local_instead_of: str | None = None) -> tuple[Path, str, str]:
    tmp_path.mkdir(parents=True, exist_ok=True)
    repo = tmp_path / "remote"
    env = {
        "PATH": os.environ.get("PATH", ""),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
    }
    _git(["init", "-q", str(repo)], cwd=tmp_path, env=env)
    _git(["-C", str(repo), "config", "user.name", "Release test"],
         cwd=tmp_path, env=env)
    _git(["-C", str(repo), "config", "user.email", "release@example.invalid"],
         cwd=tmp_path, env=env)
    (repo / "README.md").write_text("local tag fixture\n", encoding="utf-8")
    _git(["-C", str(repo), "add", "README.md"], cwd=tmp_path, env=env)
    _git(["-C", str(repo), "commit", "-q", "-m", "fixture"],
         cwd=tmp_path, env=env)
    commit = _git(["-C", str(repo), "rev-parse", "HEAD"],
                  cwd=tmp_path, env=env).stdout.strip()
    if annotated:
        _git(["-C", str(repo), "tag", "-a", TAG, "-m", "fixture tag"],
             cwd=tmp_path, env=env)
    else:
        _git(["-C", str(repo), "tag", TAG], cwd=tmp_path, env=env)
    tag_object = _git(["-C", str(repo), "rev-parse", f"refs/tags/{TAG}"],
                      cwd=tmp_path, env=env).stdout.strip()
    if local_instead_of is not None:
        _git(["-C", str(repo), "config", "--local",
              f"url.{repo.as_uri()}.insteadOf", local_instead_of],
             cwd=tmp_path, env=env)
    return repo, commit, tag_object


def test_public_command_reports_published_release_and_remote_identity(
        monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    seen = _stub_public_reads(monkeypatch)
    result = checker.main([
        "--repository", f"{OWNER}/{REPOSITORY}", "--tag", TAG,
        "--expected-commit", GATE_COMMIT,
    ])
    captured = capsys.readouterr()
    assert result == 0
    assert "OK: published Release 'v1.2.3'" in captured.out
    assert f"{OWNER}/{REPOSITORY}" in captured.out
    assert GATE_COMMIT in captured.out
    assert captured.err == ""
    remote_args = seen[-1]
    assert remote_args[remote_args.index("ls-remote") + 3] == REMOTE_URL


def test_public_command_refuses_an_absent_release(
        monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    _install_api(monkeypatch, error=urllib.error.HTTPError(
        "https://api.github.com/", 404, "Not Found", None, None))
    monkeypatch.setattr(checker, "_resolve_git", lambda: Path("/test/git"))
    monkeypatch.setattr(
        checker, "_run_git",
        lambda *a, **kw: subprocess.CompletedProcess([], 0, "", ""))
    result = checker.main([
        "--repository", f"{OWNER}/{REPOSITORY}", "--tag", TAG,
        "--expected-commit", GATE_COMMIT,
    ])
    assert result == 1
    assert "HTTP 404" in capsys.readouterr().err


@pytest.mark.parametrize("release, diagnostic", [
    (_release(draft=True), "draft must be false"),
    (_release(tag="v9.9.9"), "tag_name does not match"),
    (_release(published_at=None), "published_at"),
])
def test_public_command_refuses_unpublished_or_wrong_release(
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str], release: dict,
        diagnostic: str) -> None:
    _install_api(monkeypatch, body=json.dumps(release).encode("utf-8"))
    monkeypatch.setattr(checker, "_resolve_git", lambda: Path("/test/git"))
    monkeypatch.setattr(
        checker, "_run_git",
        lambda *a, **kw: subprocess.CompletedProcess([], 0, "", ""))
    result = checker.main([
        "--repository", f"{OWNER}/{REPOSITORY}", "--tag", TAG,
        "--expected-commit", GATE_COMMIT,
    ])
    assert result == 1
    assert diagnostic in capsys.readouterr().err


@pytest.mark.parametrize("stdout, diagnostic", [
    (_remote_output(peeled="c" * 40), "does not peel to the expected commit"),
    (f"{TAG_OBJECT}\trefs/tags/{TAG}\n", "exactly one annotated tag ref"),
    (f"{TAG_OBJECT}\trefs/tags/{TAG}\n"
     f"{'d' * 40}\trefs/tags/{TAG}\n", "duplicate tag ref"),
    (f"{TAG_OBJECT}\trefs/tags/{TAG}\n"
     f"{GATE_COMMIT}\trefs/tags/other\n", "unexpected tag ref"),
    (f"not-an-object\trefs/tags/{TAG}\n{GATE_COMMIT}\trefs/tags/{TAG}^{{}}\n",
     "malformed object id"),
    (f"{GATE_COMMIT}\trefs/tags/{TAG}\n{GATE_COMMIT}\trefs/tags/{TAG}^{{}}\n",
     "lightweight, not annotated"),
])
def test_public_command_refuses_mismatched_or_ambiguous_remote_refs(
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str], stdout: str,
        diagnostic: str) -> None:
    _stub_public_reads(monkeypatch, git_stdout=stdout)
    result = checker.main([
        "--repository", f"{OWNER}/{REPOSITORY}", "--tag", TAG,
        "--expected-commit", GATE_COMMIT,
    ])
    assert result == 1
    assert diagnostic in capsys.readouterr().err


def test_public_command_reports_remote_read_failure(
        monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    _stub_public_reads(monkeypatch, git_returncode=2,
                       git_stderr="fatal: remote read failed")
    result = checker.main([
        "--repository", f"{OWNER}/{REPOSITORY}", "--tag", TAG,
        "--expected-commit", GATE_COMMIT,
    ])
    assert result == 1
    assert "Git remote tag read failed" in capsys.readouterr().err


def test_public_command_refuses_invalid_inputs_before_remote_reads(
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(
        checker, "_resolve_git",
        lambda: pytest.fail("Git must not be resolved for invalid input"))
    _install_api(monkeypatch)
    result = checker.main([
        "--repository", "../repo", "--tag", TAG,
        "--expected-commit", "not-a-full-sha",
    ])
    assert result == 1
    assert "safe GitHub path component" in capsys.readouterr().err


def test_public_command_refuses_invalid_gate_sha_before_git_or_api(
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(
        checker, "_resolve_git",
        lambda: pytest.fail("Git must not be resolved for invalid input"))
    monkeypatch.setattr(
        checker, "_fetch_release",
        lambda *a: pytest.fail("API must not be read for invalid input"))
    result = checker.main([
        "--repository", f"{OWNER}/{REPOSITORY}", "--tag", TAG,
        "--expected-commit", "not-a-full-sha",
    ])
    assert result == 1
    assert "full 40-hex object id" in capsys.readouterr().err


def test_public_help_and_missing_arguments_are_available_without_reads() -> None:
    help_result = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"],
        capture_output=True, text=True, check=False,
    )
    assert help_result.returncode == 0
    assert "--expected-commit FULL_SHA" in help_result.stdout
    assert "--_api-child" not in help_result.stdout
    usage_result = subprocess.run(
        [sys.executable, str(SCRIPT)], capture_output=True, text=True,
        check=False,
    )
    assert usage_result.returncode == 2
    assert "usage:" in usage_result.stderr


def test_invalid_git_tag_is_refused_before_release_api_read(
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str]) -> None:
    git = Path(shutil_which_git())
    monkeypatch.setattr(checker, "_resolve_git", lambda: git)
    monkeypatch.setattr(
        checker, "_fetch_release",
        lambda *a: pytest.fail("invalid tag must be rejected before API read"))
    result = checker.main([
        "--repository", f"{OWNER}/{REPOSITORY}", "--tag", "bad..tag",
        "--expected-commit", GATE_COMMIT,
    ])
    assert result == 1
    assert "not a valid Git tag name" in capsys.readouterr().err


def shutil_which_git() -> str:
    import shutil
    found = shutil.which("git")
    assert found is not None
    return found


# Declared exception (internal hook): Hook: checker._fetch_release called directly with urllib build_opener stubbed by _install_api; a malformed release reply cannot be produced without a .
@pytest.mark.parametrize("body, diagnostic", [
    (b"not json", "malformed JSON"),
    (b"[]", "JSON object"),
    (json.dumps(_release(draft=0)).encode(), "draft must be false"),
    (json.dumps(_release(published_at="  ")).encode(), "published_at"),
])
def test_release_api_rejects_malformed_fields(
        monkeypatch: pytest.MonkeyPatch, body: bytes,
        diagnostic: str) -> None:
    _install_api(monkeypatch, body=body)
    with pytest.raises(checker.CheckError, match=diagnostic):
        checker._fetch_release(OWNER, REPOSITORY, TAG)


# Declared exception (internal hook): Hook: checker._fetch_release called directly with urllib build_opener stubbed by _install_api; a redirect reply needs a stubbed opener.
@pytest.mark.parametrize("status", [301, 302, 307])
def test_release_api_refuses_redirects(
        monkeypatch: pytest.MonkeyPatch, status: int) -> None:
    url = checker._release_api_url(OWNER, REPOSITORY, TAG)
    error = urllib.error.HTTPError(url, status, "redirect", None, None)
    opener = _install_api(monkeypatch, error=error)
    with pytest.raises(checker.CheckError, match=f"HTTP {status}"):
        checker._fetch_release(OWNER, REPOSITORY, TAG)
    assert len(opener.calls) == 1


# Declared exception (internal hook): Hook: checker._fetch_release called directly with urllib build_opener stubbed by _install_api; oversized and failed replies need a stubbed opener.
def test_release_api_refuses_oversized_reply_and_transport_failure(
        monkeypatch: pytest.MonkeyPatch) -> None:
    _install_api(monkeypatch, body=b"x" * (checker._MAX_RELEASE_BYTES + 1))
    with pytest.raises(checker.CheckError, match="exceeded 1 MiB"):
        checker._fetch_release(OWNER, REPOSITORY, TAG)
    _install_api(monkeypatch, error=urllib.error.URLError("offline"))
    with pytest.raises(checker.CheckError, match="read failed"):
        checker._fetch_release(OWNER, REPOSITORY, TAG)


# Declared exception (internal hook): Hook: checker._fetch_release called directly with urllib build_opener stubbed to raise TimeoutError; a real timeout is not reproducible in test time.
def test_release_api_timeout_fails_closed(
        monkeypatch: pytest.MonkeyPatch) -> None:
    opener = _install_api(monkeypatch, error=TimeoutError("timed out"))
    with pytest.raises(checker.CheckError, match="read failed"):
        checker._fetch_release(OWNER, REPOSITORY, TAG)
    assert opener.calls[0][1] == 30


# Declared exception (internal hook): Hook: checker._api_child_command and checker._run_git replaced to force a slow resolver; also asserts private _api_child_env. No public route to a hun.
def test_public_command_bounds_slow_resolver_worker(
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(checker, "_HTTP_TIMEOUT_SECONDS", 0.15)
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.invalid")
    monkeypatch.setenv("GITHUB_TOKEN", "must-not-reach-worker")
    child_env = checker._api_child_env()
    assert set(child_env) <= {"SYSTEMROOT"}
    assert "PATH" not in child_env
    assert "HTTPS_PROXY" not in child_env
    assert "GITHUB_TOKEN" not in child_env

    monkeypatch.setattr(checker, "_resolve_git", lambda: Path("/test/git"))

    def fake_run_git(_git, args, *, cwd, env):
        del cwd, env
        if "check-ref-format" in args:
            return subprocess.CompletedProcess(args, 0, "", "")
        pytest.fail("Git remote must not be read after the API worker times out")

    monkeypatch.setattr(
        checker, "_run_git", fake_run_git)
    monkeypatch.setattr(
        checker, "_api_child_command",
        lambda *_args: [
            sys.executable, "-I", "-c",
            "import socket,time; "
            "socket.getaddrinfo=lambda *a,**k:time.sleep(5); "
            "socket.getaddrinfo('api.github.com',443)",
        ])
    started = time.monotonic()
    result = checker.main([
        "--repository", f"{OWNER}/{REPOSITORY}", "--tag", TAG,
        "--expected-commit", GATE_COMMIT,
    ])
    elapsed = time.monotonic() - started
    captured = capsys.readouterr()
    assert result == 1
    assert "request timed out after 0.15 seconds" in captured.err
    assert elapsed < 1.0


# Declared exception (internal hook): Hook: checker.subprocess.run replaced to raise TimeoutExpired, called through private _run_git; a hung git cannot be produced in test time.
def test_git_timeout_is_bounded_and_fails_closed(
        monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    def timed_out(argv, **kwargs):
        assert kwargs["shell"] is False
        assert kwargs["stdin"] is subprocess.DEVNULL
        assert kwargs["timeout"] == checker._GIT_TIMEOUT_SECONDS == 30
        raise subprocess.TimeoutExpired(argv, kwargs["timeout"])

    monkeypatch.setattr(checker.subprocess, "run", timed_out)
    with pytest.raises(checker.CheckError, match="Git command timed out after 30"):
        checker._run_git(Path("/host/git"), ["check-ref-format", "refs/tags/x"],
                         cwd=tmp_path, env=checker._git_child_env(tmp_path.parent))


def test_real_ls_remote_accepts_annotated_local_tag_and_refuses_lightweight(
        tmp_path: Path) -> None:
    annotated, commit, tag_object = _local_repo(tmp_path / "annotated")
    raw = subprocess.run(
        ["git", "-c", "protocol.file.allow=always", "ls-remote",
         "--exit-code", "--tags", str(annotated), f"refs/tags/{TAG}",
         f"refs/tags/{TAG}^{{}}"],
        cwd=tmp_path, capture_output=True, text=True, check=True,
    )
    checker._parse_remote_refs(raw.stdout, TAG, commit)
    assert tag_object != commit

    lightweight, light_commit, _ = _local_repo(
        tmp_path / "lightweight", annotated=False)
    light_raw = subprocess.run(
        ["git", "-c", "protocol.file.allow=always", "ls-remote",
         "--exit-code", "--tags", str(lightweight), f"refs/tags/{TAG}",
         f"refs/tags/{TAG}^{{}}"],
        cwd=tmp_path, capture_output=True, text=True, check=True,
    )
    with pytest.raises(checker.CheckError, match="exactly one annotated tag ref"):
        checker._parse_remote_refs(light_raw.stdout, TAG, light_commit)


def test_public_command_ignores_hostile_git_configuration_and_proxy(
        monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
        capsys: pytest.CaptureFixture[str]) -> None:
    repo, commit, _tag_object = _local_repo(
        tmp_path, local_instead_of=REMOTE_URL)
    git = Path(shutil_which_git()).resolve()
    uri = repo.as_uri()
    global_config = tmp_path / "global.gitconfig"
    system_config = tmp_path / "system.gitconfig"
    config_text = (f'[url "{uri}"]\n'
                   f'\tinsteadOf = {REMOTE_URL}\n'
                   '[http]\n\tfollowRedirects = true\n'
                   '[credential]\n\thelper = !echo unexpected-helper\n')
    global_config.write_text(config_text, encoding="utf-8")
    system_config.write_text(config_text, encoding="utf-8")
    home = tmp_path / "home"
    home.mkdir()
    (home / ".gitconfig").write_text(config_text, encoding="utf-8")
    monkeypatch.setenv("GIT_DIR", str(repo / ".git"))
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", str(system_config))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(global_config))
    monkeypatch.delenv("GIT_CONFIG_NOSYSTEM", raising=False)
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", f"url.{uri}.insteadOf")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", REMOTE_URL)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.invalid:9999")
    monkeypatch.setenv("HTTP_PROXY", "http://proxy.invalid:9999")
    monkeypatch.setenv("ALL_PROXY", "http://proxy.invalid:9999")
    _install_api(monkeypatch)

    # Prove the local insteadOf fixture is a real attack control: with the
    # hostile inputs enabled, Git rewrites the fixed GitHub URL to this tagged
    # local repository and returns the matching target without network access.
    poisoned = dict(os.environ)
    poisoned.update({
        "GIT_CONFIG_SYSTEM": str(system_config),
        "GIT_CONFIG_GLOBAL": str(global_config),
        "GIT_DIR": str(repo / ".git"),
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": f"url.{uri}.insteadOf",
        "GIT_CONFIG_VALUE_0": REMOTE_URL,
    })
    control = subprocess.run(
        [str(git), "-c", "protocol.file.allow=always", "ls-remote",
         "--exit-code", "--tags", REMOTE_URL, f"refs/tags/{TAG}",
         f"refs/tags/{TAG}^{{}}"],
        cwd=tmp_path, env=poisoned, capture_output=True, text=True, check=True,
    )
    assert commit in control.stdout

    real_run = subprocess.run
    observed: list[tuple[list[str], Path, dict[str, str]]] = []

    def observe_git(argv, **kwargs):
        normalized = [str(part) for part in argv]
        cwd = Path(kwargs["cwd"]).resolve()
        child_env = kwargs["env"]
        assert kwargs["stdin"] is subprocess.DEVNULL
        observed.append((normalized, cwd, child_env))
        assert Path(normalized[0]).resolve() == git
        assert cwd != repo.resolve() and repo.resolve() not in cwd.parents
        assert not (cwd / ".git").exists()
        expected_keys = {
            "PATH", "GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_SYSTEM",
            "GIT_CONFIG_GLOBAL", "GIT_TERMINAL_PROMPT",
            "GIT_CEILING_DIRECTORIES",
        }
        if os.name == "nt" and "SYSTEMROOT" in os.environ:
            expected_keys.add("SYSTEMROOT")
        assert set(child_env) == expected_keys
        assert child_env["GIT_CONFIG_NOSYSTEM"] == "1"
        assert child_env["GIT_CONFIG_SYSTEM"] == os.devnull
        assert child_env["GIT_CONFIG_GLOBAL"] == os.devnull
        assert child_env["GIT_TERMINAL_PROMPT"] == "0"
        assert child_env["GIT_CEILING_DIRECTORIES"] == str(cwd.parent)
        if "ls-remote" in normalized:
            assert REMOTE_URL in normalized
            for setting in checker._git_config_args():
                assert setting in normalized
            mapped = list(normalized)
            command_index = mapped.index("ls-remote")
            mapped[command_index:command_index] = [
                "-c", "protocol.file.allow=always"]
            mapped[mapped.index(REMOTE_URL)] = str(repo)
            return real_run(mapped, **kwargs)
        return real_run(normalized, **kwargs)

    monkeypatch.setattr(checker.subprocess, "run", observe_git)
    result = checker.main([
        "--repository", f"{OWNER}/{REPOSITORY}", "--tag", TAG,
        "--expected-commit", commit,
    ])
    assert result == 0, capsys.readouterr().err
    assert any("check-ref-format" in args for args, _cwd, _env in observed)
    query = next(args for args, _cwd, _env in observed if "ls-remote" in args)
    assert query[query.index("ls-remote") + 3] == REMOTE_URL
    assert "protocol.allow=never" in query
    assert "protocol.https.allow=always" in query
    assert "http.followRedirects=false" in query
    assert "credential.helper=" in query
