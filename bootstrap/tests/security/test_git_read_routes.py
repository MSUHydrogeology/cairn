"""Public-entry controls for the routes that read Git through the safe reader.

Every route here is run through its real command (or, for the meter, the one
function its command calls) against a disposable repository that carries its own
programs: a `git` wrapper inside the repository that records each call, and a
repository config that names a file-system monitor, a clean/smudge filter, a
text converter, a pager and an ssh command. Each program records itself in one
sentinel file. A control first shows plain Git does run the config programs, so
a quiet result means something.

Promises:
- A repository's own `git` program is never run by the content-scan runner, the prose report, the exact replacer's change report, the link and snippet checks, the portable sweep, the intent commands, the meter's project-remote read, install or upgrade.
- When the only `git` found sits inside the repository being read, each of those routes refuses or reports an incomplete read and never reports clean, unchanged, current or an empty result.
- Given a repository whose config names monitor, filter, converter, pager and ssh programs, those routes return their normal answer (the sweep refuses the config before it runs anything) and run none of those programs.
- Install and upgrade read the Cairn source and the target as separate repositories, so a program inside one is not run to read the other.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    os.name == "nt",
    reason=(
        "a `git` stand-in is an extensionless script, which only POSIX can run; "
        "no route-level native Windows control exists for these routes (the "
        "native worker controls in test_git_read.py cover the helper, not each "
        "caller), so this is a recorded Windows gap, not a Windows result"),
)

ROOT = Path(__file__).resolve().parents[3]
TEAM = ROOT / "templates" / "modules" / "team-gated"
INSTALLED_HELPER = ROOT / "tools" / "git_read.py"
SOURCE_HELPER = ROOT / "templates" / "skills" / "_lib" / "git_read.py"
SCAFFOLD = ROOT / "bootstrap" / "scaffold.py"
LAYOUTS = ("installed", "source")


def _real_git() -> str:
    found = shutil.which("git")
    if not found:
        pytest.skip("real Git unavailable")
    return str(Path(found).resolve())


class Lab:
    """One scratch area: a safe environment, a sentinel and a call log."""

    def __init__(self, base: Path) -> None:
        self.base = base.resolve()
        self.base.mkdir(parents=True, exist_ok=True)
        self.real_git = _real_git()
        self.sentinel = self.base / "program-ran"
        self.calls = self.base / "wrapper-calls"
        self.home = self.base / "home"
        self.home.mkdir(exist_ok=True)
        self.program = self.base / "program.py"
        self.program.write_text(
            "import pathlib, sys\n"
            f"pathlib.Path({str(self.sentinel)!r}).open('a').write('ran\\n')\n"
            "if '--cat' in sys.argv:\n"
            "    sys.stdout.buffer.write(sys.stdin.buffer.read())\n",
            encoding="utf-8")

    def env(self, hostile_bin: Path | None = None,
            extra_dirs: tuple[Path, ...] = ()) -> dict[str, str]:
        env = {key: value for key, value in os.environ.items()
               if not key.startswith("GIT_") and key not in ("PYTHONPATH", "PYTHONHOME")}
        dirs = [*map(str, extra_dirs), str(Path(self.real_git).parent), "/usr/bin", "/bin"]
        if hostile_bin is not None:
            dirs.insert(0, str(hostile_bin))
        env.update(
            PATH=os.pathsep.join(dirs), HOME=str(self.home),
            GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
            GIT_AUTHOR_NAME="route test", GIT_AUTHOR_EMAIL="route@example.invalid",
            GIT_COMMITTER_NAME="route test", GIT_COMMITTER_EMAIL="route@example.invalid")
        return env

    def git(self, repo: Path, *args: str) -> str:
        done = subprocess.run([self.real_git, "-C", str(repo), *args], env=self.env(),
                              check=True, capture_output=True, text=True)
        return done.stdout.strip()

    def repo(self, name: str, files: dict[str, bytes | str], *,
             copy: dict[str, Path] | None = None) -> Path:
        """Create and commit a repository holding *files* and copies of *copy*."""
        repo = self.base / name
        repo.mkdir(parents=True)
        for rel, content in files.items():
            target = repo / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, str):
                content = content.encode("utf-8")
            target.write_bytes(content)
            if rel.endswith((".py", ".sh")):
                target.chmod(0o755)
        for rel, source in (copy or {}).items():
            (repo / rel).parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, repo / rel)
            else:
                shutil.copy2(source, repo / rel)
        (repo / ".gitattributes").write_text(
            "*.dat filter=hostile diff=hostile\n", encoding="utf-8")
        (repo / "data.dat").write_bytes(b"aaaa\n")
        self.git(repo, "init", "-q", "-b", "main")
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-qm", "base")
        return repo

    def arm(self, repo: Path) -> Path:
        """Make *repo* hostile; return the directory holding its `git` stand-in.

        Run after the last setup commit: arming makes a plain `git status` run
        the programs below."""
        py = Path(sys.executable).as_posix()
        program = self.program.as_posix()
        quiet = f'"{py}" "{program}"'
        cat = f'"{py}" "{program}" --cat'
        for key, value in (
                ("core.fsmonitor", quiet), ("core.pager", quiet),
                ("core.sshCommand", quiet), ("filter.hostile.clean", cat),
                ("filter.hostile.smudge", cat), ("filter.hostile.required", "true"),
                ("diff.hostile.textconv", quiet)):
            self.git(repo, "config", key, value)
        (repo / "data.dat").write_bytes(b"bbbb\n")  # same length: status must hash it
        bin_dir = repo / "hostile-bin"
        bin_dir.mkdir()
        wrapper = bin_dir / "git"
        wrapper.write_text(
            "#!/bin/sh\n"
            f"printf '%s\\n' \"$*\" >> '{self.calls}'\n"
            f"exec '{self.real_git}' \"$@\"\n", encoding="utf-8")
        wrapper.chmod(0o755)
        # Control: the programs are live. Plain Git runs them; the route must not.
        subprocess.run([self.real_git, "-C", str(repo), "status", "--porcelain"],
                       env=self.env(), check=True, capture_output=True)
        assert self.sentinel.exists(), "the config programs are inert, so this proves nothing"
        self.sentinel.unlink()
        assert not self.calls.exists()
        return bin_dir

    def calls_about(self, repo: Path) -> list[str]:
        if not self.calls.exists():
            return []
        needle = f"-C {repo} "
        return [line for line in self.calls.read_text(encoding="utf-8").splitlines()
                if needle in line + " "]

    def assert_no_program_ran(self, repo: Path | None = None) -> None:
        assert not self.sentinel.exists(), "a program the repository's config names ran"
        if repo is None:
            assert not self.calls.exists(), "the repository's own git ran"
        else:
            assert self.calls_about(repo) == [], "the repository's own git ran"

    def run(self, argv: list[str], cwd: Path, *, hostile_bin: Path | None = None,
            extra_dirs: tuple[Path, ...] = (), extra_env: dict[str, str] | None = None,
            timeout: float = 60.0) -> subprocess.CompletedProcess:
        env = self.env(hostile_bin, extra_dirs)
        env.update(extra_env or {})
        return subprocess.run(argv, cwd=cwd, env=env, text=True,
                              capture_output=True, timeout=timeout)


def _source(layout: str, name: str) -> tuple[str, bytes]:
    """The delivery path and bytes of a team-gated tool in *layout*."""
    if layout == "installed":
        return f"scripts/{name}", (ROOT / "scripts" / name).read_bytes()
    return f"templates/modules/team-gated/{name}", (TEAM / name).read_bytes()


def _helper(layout: str) -> tuple[str, bytes]:
    if layout == "installed":
        return "tools/git_read.py", INSTALLED_HELPER.read_bytes()
    return "templates/skills/_lib/git_read.py", SOURCE_HELPER.read_bytes()


# --------------------------------------------------------------------------
# Content-scan runner
# --------------------------------------------------------------------------

@pytest.mark.parametrize("layout", LAYOUTS)
def test_content_scan_runner_refuses_a_git_inside_the_repository(
        tmp_path: Path, layout: str) -> None:
    # Positive control for: the runner running a repository-supplied `git` to list the audited set.
    lab = Lab(tmp_path)
    files: dict[str, bytes | str] = {"dev/doc.md": "# A clean doc\n"}
    for name in ("content_scan_runner.py", "content_scan.py", "content_scan_allowlist.txt"):
        rel, data = _source(layout, name)
        files[rel] = data
    runner_rel, _ = _source(layout, "content_scan_runner.py")
    folder = runner_rel.rsplit("/", 1)[0]
    files[f"{folder}/content_scan_roots.txt"] = "# content-scan-roots v1\ndev\n"
    files[f"{folder}/content_scan_residuals.txt"] = "# content-scan-residual-baseline v1\n"
    helper_rel, helper = _helper(layout)
    files[helper_rel] = helper
    repo = lab.repo("repo", files)
    hostile_bin = lab.arm(repo)
    command = [sys.executable, str(repo / runner_rel)]

    safe = lab.run(command, repo)
    assert safe.returncode == 0, safe.stdout + safe.stderr
    assert "content_scan: Git executable" in safe.stdout
    lab.assert_no_program_ran()

    refused = lab.run(command, repo, hostile_bin=hostile_bin)
    assert refused.returncode == 2, refused.stdout + refused.stderr
    assert "inside the repository" in refused.stderr, refused.stderr
    lab.assert_no_program_ran()


# --------------------------------------------------------------------------
# Prose report
# --------------------------------------------------------------------------

def _prose_repo(lab: Lab) -> tuple[Path, str]:
    """A repository holding both layouts of the prose tools, with a committed rule change.

    Returns the repository and the commit before the change."""
    helper = INSTALLED_HELPER.read_bytes()
    files: dict[str, bytes | str] = {
        "AGENTS.md": "Keep every tool output bounded. This protects the user.\n",
        "scripts/content_scan_roots.txt": "# content-scan-roots v1\n!AGENTS.md\n",
        "tools/git_read.py": helper,
        "templates/skills/_lib/git_read.py": SOURCE_HELPER.read_bytes(),
    }
    for name in ("prose_diff.py", "prose_roots.txt", "exact_replace.py"):
        files[f"scripts/{name}"] = (TEAM / name).read_bytes()
        files[f"templates/modules/team-gated/{name}"] = (TEAM / name).read_bytes()
    files["dev/.cairn/cairn-lock.yml"] = "# fixture\n" + json.dumps({"files": [
        {"dst": "tools/git_read.py", "verbatim": True,
         "hash": "sha256:" + hashlib.sha256(helper).hexdigest()},
        {"dst": "scripts/prose_diff.py", "verbatim": True,
         "hash": "sha256:" + hashlib.sha256((TEAM / "prose_diff.py").read_bytes()).hexdigest()},
    ]})
    repo = lab.repo("repo", files)
    base = lab.git(repo, "rev-parse", "HEAD")
    (repo / "AGENTS.md").write_text(
        "Keep every tool output available. This protects the user.\n", encoding="utf-8")
    lab.git(repo, "add", "AGENTS.md")
    lab.git(repo, "commit", "-qm", "change rule")
    return repo, base


@pytest.mark.parametrize("layout", LAYOUTS)
def test_prose_report_refuses_a_git_inside_the_repository(
        tmp_path: Path, layout: str) -> None:
    # Positive control for: the prose report running a repository-supplied `git` and printing "no changes".
    lab = Lab(tmp_path)
    repo, base = _prose_repo(lab)
    hostile_bin = lab.arm(repo)
    entry = repo / ("scripts" if layout == "installed" else "templates/modules/team-gated")
    command = [sys.executable, str(entry / "prose_diff.py"), base, "HEAD"]

    safe = lab.run(command, repo)
    assert safe.returncode == 0, safe.stdout + safe.stderr
    assert "CHANGED AGENTS.md" in safe.stdout
    lab.assert_no_program_ran()

    refused = lab.run(command, repo, hostile_bin=hostile_bin)
    assert refused.returncode == 2, refused.stdout + refused.stderr
    assert "INCOMPLETE" in refused.stderr and "CHANGED" not in refused.stdout
    lab.assert_no_program_ran()


@pytest.mark.parametrize("layout", LAYOUTS)
def test_exact_replacer_reports_an_unreadable_repository_as_a_failed_report(
        tmp_path: Path, layout: str) -> None:
    # Positive control for: the replacer's change report running a repository-supplied `git` and reporting success.
    lab = Lab(tmp_path)
    repo, _base = _prose_repo(lab)
    hostile_bin = lab.arm(repo)
    entry = repo / ("scripts" if layout == "installed" else "templates/modules/team-gated")
    sources = lab.base / "sources"
    sources.mkdir()

    def replace(old: str, new: str, hostile: bool) -> subprocess.CompletedProcess:
        (sources / "old.txt").write_text(old, encoding="utf-8")
        (sources / "new.txt").write_text(new, encoding="utf-8")
        return lab.run([sys.executable, str(entry / "exact_replace.py"), "AGENTS.md",
                        "--old-file", str(sources / "old.txt"),
                        "--new-file", str(sources / "new.txt")],
                       repo, hostile_bin=hostile_bin if hostile else None)

    refused = replace("available", "bounded", hostile=True)
    assert refused.returncode == 3, refused.stdout + refused.stderr  # edit made, report failed
    assert "Applied, but the change report failed" in refused.stdout
    assert "Applied exactly one replacement sequence" not in refused.stdout
    lab.assert_no_program_ran()

    safe = replace("bounded", "limited", hostile=False)
    assert safe.returncode == 0, safe.stdout + safe.stderr
    assert "Applied exactly one replacement sequence" in safe.stdout
    lab.assert_no_program_ran()


# --------------------------------------------------------------------------
# Link and snippet checks: root discovery and tracked-file discovery
# --------------------------------------------------------------------------

@pytest.mark.parametrize("tool,finding", [
    ("link_check.py", "broken link"), ("sync_doc_snippets.py", "snippet(s) drifted")])
@pytest.mark.parametrize("layout", LAYOUTS)
def test_markdown_checks_refuse_a_git_inside_the_repository_and_never_read_clean(
        tmp_path: Path, layout: str, tool: str, finding: str) -> None:
    # Positive control for: root discovery or file discovery running a repository-supplied `git`, or an unreadable repository reading as "no files, clean".
    lab = Lab(tmp_path)
    tool_rel, tool_bytes = _source(layout, tool)
    helper_rel, helper = _helper(layout)
    repo = lab.repo("repo", {
        "src.py": "# snippet-start: demo\nnew body\n# snippet-end: demo\n",
        "broken.md": ("# Broken\n\n[missing](missing.md)\n\n"
                      "<!-- snippet: src.py#demo -->\n```python\nstale body\n```\n"),
        tool_rel: tool_bytes, helper_rel: helper})
    hostile_bin = lab.arm(repo)
    command = [sys.executable, str(repo / tool_rel)]
    if tool == "sync_doc_snippets.py":
        command.append("--check")

    safe = lab.run(command, repo)
    assert safe.returncode == 1 and "broken.md" in safe.stderr and finding in safe.stderr, (
        safe.stdout + safe.stderr)
    lab.assert_no_program_ran()

    refused = lab.run(command, repo, hostile_bin=hostile_bin)
    assert refused.returncode != 0, refused.stdout + refused.stderr
    assert "tracked Markdown discovery failed" in refused.stderr, refused.stderr
    assert finding not in refused.stderr and "scanned" not in refused.stdout
    lab.assert_no_program_ran()


# --------------------------------------------------------------------------
# Portable sweep
# --------------------------------------------------------------------------

@pytest.mark.parametrize("layout", LAYOUTS)
def test_portable_sweep_refuses_a_git_inside_the_repository_and_a_hostile_config(
        tmp_path: Path, layout: str) -> None:
    # Positive control for: the sweep selecting and running a repository-supplied `git`, or scanning past a config that names programs.
    lab = Lab(tmp_path)
    tool_rel, tool_bytes = _source(layout, "run_portable_security_sweeps.py")
    folder = tool_rel.rsplit("/", 1)[0]
    helper_rel, helper = _helper(layout)
    repo = lab.repo("repo", {
        "README.md": "# readme\n", tool_rel: tool_bytes, helper_rel: helper,
        f"{folder}/portable_security_policy.json":
            (TEAM / "portable_security_policy.json").read_bytes()})
    hostile_bin = lab.arm(repo)
    stub_dir = lab.base / "stub-bin"
    stub_dir.mkdir()
    adapter_ran = lab.base / "adapter-ran"
    adapter = stub_dir / "gitleaks"
    adapter.write_text(f"#!/bin/sh\nprintf ran >> '{adapter_ran}'\nexit 0\n", encoding="utf-8")
    adapter.chmod(0o755)
    command = [sys.executable, str(repo / tool_rel), "--target", str(repo), "--json"]

    def legs(done: subprocess.CompletedProcess) -> dict[str, dict]:
        assert done.returncode == 20, done.stdout + done.stderr  # DEGRADED, never 0
        summary = json.loads(done.stdout)
        assert summary["result"] == 20 and summary["mode"] is None
        return {leg["leg"]: leg for leg in summary["legs"]}

    config_refused = legs(lab.run(command, repo, extra_dirs=(stub_dir,)))
    assert "core.fsmonitor" in config_refused["preflight"]["reason"]
    assert "git" not in config_refused
    lab.assert_no_program_ran()
    assert not adapter_ran.exists()

    path_refused = legs(lab.run(command, repo, hostile_bin=hostile_bin,
                                extra_dirs=(stub_dir,)))
    assert "git" in path_refused, "the sweep did not refuse the repository's own git"
    assert "inside the tree under check" in path_refused["git"]["reason"]
    assert "preflight" not in path_refused
    lab.assert_no_program_ran()
    assert not adapter_ran.exists()


# --------------------------------------------------------------------------
# Intent commands: repository-root discovery
# --------------------------------------------------------------------------

@pytest.mark.parametrize("layout", LAYOUTS)
def test_intent_commands_refuse_a_git_inside_the_repository(
        tmp_path: Path, layout: str) -> None:
    # Positive control for: the intent commands finding the repository root with a repository-supplied `git`, or an unreadable root reading as "nothing staged".
    lab = Lab(tmp_path)
    source = ROOT / "tools" if layout == "installed" else TEAM
    folder = "tools" if layout == "installed" else "templates/modules/team-gated"
    helper_rel, helper = _helper(layout)
    files: dict[str, bytes | str] = {
        f"{folder}/intent.py": (source / "intent.py").read_bytes(),
        helper_rel: helper, "dev/keep.md": "# keep\n"}
    for part in sorted((source / "_intent").glob("*.py")):
        files[f"{folder}/_intent/{part.name}"] = part.read_bytes()
    repo = lab.repo("repo", files)
    hostile_bin = lab.arm(repo)
    tool = [sys.executable, str(repo / folder / "intent.py")]
    session = {"CLAUDE_CODE_SESSION_ID": "route-test-session"}
    hooks = repo / ".git" / "hooks"

    def run(*args: str, hostile: bool) -> subprocess.CompletedProcess:
        return lab.run([*tool, *args], repo, extra_env=session,
                       hostile_bin=hostile_bin if hostile else None)

    for command in ("install-hook", "install-precommit"):
        refused = run(command, hostile=True)
        assert refused.returncode == 1 and "not inside a git working tree" in refused.stderr
    assert not (hooks / "post-commit").exists() and not (hooks / "pre-commit").exists()
    staged = run("_precommit_check", hostile=True)
    assert staged.returncode == 0 and "staged path discovery is unavailable" in staged.stderr
    released = run("_auto_release", hostile=True)
    assert released.returncode == 0
    assert "committed path discovery is unavailable" in released.stderr
    lab.assert_no_program_ran()

    for command in ("install-hook", "install-precommit"):
        done = run(command, hostile=False)
        assert done.returncode == 0, done.stdout + done.stderr
    assert (hooks / "post-commit").is_file() and (hooks / "pre-commit").is_file()
    for command in ("_precommit_check", "_auto_release"):
        done = run(command, hostile=False)
        assert done.returncode == 0 and "unavailable" not in done.stderr, done.stderr
    lab.assert_no_program_ran()


# --------------------------------------------------------------------------
# Install and upgrade: the Cairn source and the target are separate repositories
# --------------------------------------------------------------------------

def _cairn_source(lab: Lab, name: str) -> Path:
    """A committed, minimal Cairn source: templates, citation and the two renderer files."""
    return lab.repo(name, {}, copy={
        "templates": ROOT / "templates", "CITATION.cff": ROOT / "CITATION.cff",
        "bootstrap/_scaffold/config.py": ROOT / "bootstrap/_scaffold/config.py",
        "bootstrap/_scaffold/install.py": ROOT / "bootstrap/_scaffold/install.py"})


def _scaffold(lab: Lab, args: list[str], *, hostile_bin: Path | None = None,
              ) -> subprocess.CompletedProcess:
    return lab.run([sys.executable, str(SCAFFOLD), *args], lab.base,
                   hostile_bin=hostile_bin)


def _install_args(lab: Lab, target: Path, source: Path, *extra: str) -> list[str]:
    profile = lab.base / "profile.yml"
    profile.write_text("project_name: T\ntest_command: pytest\nmodules: []\n", encoding="utf-8")
    return ["--config", str(profile), "--target", str(target), "--cairn-root", str(source), *extra]


def _locked_commit(target: Path) -> str:
    text = (target / "dev/.cairn/cairn-lock.yml").read_text(encoding="utf-8")
    return json.loads(text[text.index("{"):])["cairn_commit"]


def test_install_never_runs_a_program_from_the_cairn_source(tmp_path: Path) -> None:
    # Positive control for: install reading the Cairn source (provenance status, commit stamp) with a source-supplied `git` or config program.
    lab = Lab(tmp_path)
    source = _cairn_source(lab, "cairn-source")
    hostile_bin = lab.arm(source)
    head = lab.git(source, "rev-parse", "HEAD")

    safe_target = lab.base / "safe-target"
    safe_target.mkdir()
    safe = _scaffold(lab, _install_args(lab, safe_target, source))
    assert safe.returncode == 0, safe.stdout + safe.stderr
    assert "its source tree has uncommitted changes" in safe.stdout + safe.stderr
    assert head.startswith(_locked_commit(safe_target))
    lab.assert_no_program_ran()

    refused_target = lab.base / "refused-target"
    refused_target.mkdir()
    refused = _scaffold(lab, _install_args(lab, refused_target, source),
                        hostile_bin=hostile_bin)
    assert refused.returncode == 0, refused.stdout + refused.stderr
    assert "Git verification is unavailable" in refused.stdout + refused.stderr
    assert "uncommitted changes" not in refused.stdout + refused.stderr
    assert _locked_commit(refused_target) == "unknown"
    lab.assert_no_program_ran(source)


def test_install_refuses_a_git_inside_the_target_repository(tmp_path: Path) -> None:
    # Positive control for: install resolving the target's Git administration directory with a target-supplied `git`.
    lab = Lab(tmp_path)
    source = _cairn_source(lab, "cairn-source")
    target = lab.repo("target", {"keep.txt": "x\n"})
    hostile_bin = lab.arm(target)

    refused = _scaffold(lab, _install_args(lab, target, source, "--allow-dev"),
                        hostile_bin=hostile_bin)
    assert refused.returncode == 2, refused.stdout + refused.stderr
    assert "interpreter binding refused" in refused.stderr
    assert not (target / "dev/.cairn/cairn-lock.yml").exists()
    assert not (target / ".git/cairn/local-env.json").exists()
    lab.assert_no_program_ran(target)

    safe = _scaffold(lab, _install_args(lab, target, source, "--allow-dev"))
    assert safe.returncode == 0, safe.stdout + safe.stderr
    assert (target / ".git/cairn/local-env.json").is_file()
    lab.assert_no_program_ran(target)


def test_upgrade_plan_never_runs_a_program_from_the_cairn_source(tmp_path: Path) -> None:
    # Positive control for: upgrade reading the Cairn source's HEAD, revision and file history with a source-supplied `git` or config program.
    lab = Lab(tmp_path)
    source = _cairn_source(lab, "cairn-source")
    (source / "CITATION.cff").write_text(
        (source / "CITATION.cff").read_text(encoding="utf-8") + "\n# second\n",
        encoding="utf-8")
    lab.git(source, "add", "CITATION.cff")
    lab.git(source, "commit", "-qm", "second")
    project = lab.base / "project"
    project.mkdir()
    lab.git(project, "init", "-q", "-b", "main")
    installed = _scaffold(lab, _install_args(lab, project, source, "--allow-dev"))
    assert installed.returncode == 0, installed.stdout + installed.stderr
    lab.git(project, "add", "-A")
    lab.git(project, "commit", "-qm", "installed")
    hostile_bin = lab.arm(source)
    plan = ["upgrade", "--plan", "--target", str(project), "--cairn-root", str(source)]

    safe = _scaffold(lab, plan)
    assert safe.returncode == 0, safe.stdout + safe.stderr
    assert "installed tree is current with canonical" in safe.stdout + safe.stderr
    lab.assert_no_program_ran()

    refused = _scaffold(lab, plan, hostile_bin=hostile_bin)
    assert refused.returncode == 0, refused.stdout + refused.stderr
    assert "behind-by-N check unavailable" in refused.stdout + refused.stderr
    assert "current with canonical" not in refused.stdout + refused.stderr
    lab.assert_no_program_ran(source)

    to_ref = _scaffold(lab, [*plan, "--to", "HEAD"], hostile_bin=hostile_bin)
    assert to_ref.returncode == 1, to_ref.stdout + to_ref.stderr
    assert "needs a git-checkout Cairn source" in to_ref.stderr
    lab.assert_no_program_ran(source)


def test_upgrade_to_a_ref_never_fetches_a_missing_object_through_a_source_program(
        tmp_path: Path) -> None:
    # Positive control for: `upgrade --to` reading a missing object of a blobless Cairn source and so running its `uploadpack` program.
    lab = Lab(tmp_path)
    origin = _cairn_source(lab, "origin")
    lab.git(origin, "config", "uploadpack.allowFilter", "true")
    lab.git(origin, "config", "uploadpack.allowAnySHA1InWant", "true")
    project = lab.base / "project"
    project.mkdir()
    lab.git(project, "init", "-q", "-b", "main")
    installed = _scaffold(lab, _install_args(lab, project, origin, "--allow-dev"))
    assert installed.returncode == 0, installed.stdout + installed.stderr
    source = lab.base / "blobless-source"
    subprocess.run([lab.real_git, "clone", "-q", "--no-checkout", "--filter=blob:none",
                    f"file://{origin}", str(source)],
                   env=lab.env(), check=True, capture_output=True)
    for rel in ("templates", "CITATION.cff", "bootstrap"):  # the clone has no checkout
        if (origin / rel).is_dir():
            shutil.copytree(origin / rel, source / rel)
        else:
            shutil.copy2(origin / rel, source / rel)
    program = f'"{Path(sys.executable).as_posix()}" "{lab.program.as_posix()}"'
    lab.git(source, "config", "remote.origin.uploadpack", program)
    # Control: with lazy fetch on, plain Git does run the program for a missing object.
    subprocess.run([lab.real_git, "-C", str(source), "cat-file", "-p", "HEAD:CITATION.cff"],
                   env=lab.env(), capture_output=True)
    assert lab.sentinel.exists(), "the upload-pack program is inert, so this proves nothing"
    lab.sentinel.unlink()

    done = _scaffold(lab, ["upgrade", "--plan", "--target", str(project), "--cairn-root",
                           str(source), "--to", "HEAD"])
    assert done.returncode != 0, done.stdout + done.stderr
    assert "could not be read" in done.stdout + done.stderr
    lab.assert_no_program_ran()


# --------------------------------------------------------------------------
# Meter: the approved project's remote
# --------------------------------------------------------------------------

@pytest.mark.parametrize("meter_rel", ["tools/meter.py", "templates/skills/_lib/meter.py"])
def test_meter_project_remote_read_refuses_a_git_inside_the_project(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, meter_rel: str) -> None:
    # Positive control for: the meter reading a project's remote through a project-supplied `git`, or returning a remote after an unreadable read.
    lab = Lab(tmp_path)
    remote = "https://example.test/org/repo.git"
    project = lab.repo("project", {"keep.txt": "x\n"})
    lab.git(project, "remote", "add", "origin", remote)
    (project / ".git").chmod(0o700)
    hostile_bin = lab.arm(project)
    spec = importlib.util.spec_from_file_location("_routes_meter", ROOT / meter_rel)
    assert spec is not None and spec.loader is not None
    meter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(meter)
    approved = {"alias": "project", "path": str(project), "remote": remote}
    for key in [name for name in os.environ if name.startswith("GIT_")]:
        monkeypatch.delenv(key)

    monkeypatch.setenv("PATH", lab.env()["PATH"])
    assert meter._verified_project_remote(approved, []) == (remote, None)
    lab.assert_no_program_ran()

    monkeypatch.setenv("PATH", lab.env(hostile_bin)["PATH"])
    answer, reason = meter._verified_project_remote(approved, [])
    assert answer is None and reason in {"git_untrusted", "git_parser_failed"}, (answer, reason)
    lab.assert_no_program_ran()
