"""Contract tests for `bootstrap/reanchor.sh`, the re-anchor ceremony artifact.

The artifact exists because the ceremony was previously performed by pasting
recorded shell blocks and filling placeholders by hand, which in practice meant
an assisting agent generated a script for each stage. That put the agent inside
the trust path, and left the Maintainer authorizing a procedure they could not
read end to end.

So every node here drives the artifact **through its public command surface**,
never through a helper: a refusal that only a unit test can reach is a refusal
the ceremony does not have. Each refusal node also asserts that **nothing else
ran** -- the effective-configuration block and the success line are both absent
-- because a check that refuses *after* doing the work is not fail-closed.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_ARTIFACT = _REPO / "bootstrap/reanchor.sh"
_EXAMPLE = _REPO / "bootstrap/reanchor-values.example"

#: Every key in the closed schema, in the order the template presents them.
#: Retyped deliberately: this list is the *test's* statement of the contract,
#: so a key silently added to the artifact fails the closure node below rather
#: than being adopted by a shared constant.
SCHEMA_KEYS = ("schema", "checkout", "signing_key", "package", "home",
               "env", "git", "python", "mktemp", "mkdir", "shasum", "sort",
               "cat")

EXECUTABLE_KEYS = ("env", "git", "python", "mktemp", "mkdir", "shasum",
                   "sort", "cat")


def _run(*args: str, env: dict | None = None) -> subprocess.CompletedProcess:
    """Invoke the artifact the way the ceremony does: `/bin/sh <artifact>`.

    Literally `/bin/sh`, as everywhere else in this ceremony -- a
    non-interactive `/bin/sh` reads no startup file, which is what makes the
    child clean.
    """
    return subprocess.run(["/bin/sh", str(_ARTIFACT), *args],
                          capture_output=True, text=True, check=False,
                          env=env)


def _assert_refused(r: subprocess.CompletedProcess, needle: str) -> None:
    """A refusal is non-zero, names its reason, and leaves no work done."""
    assert r.returncode != 0, (
        f"expected a refusal, got success:\n{r.stdout}\n{r.stderr}")
    assert "REFUSE:" in r.stderr, r.stderr
    assert needle in r.stderr, (
        f"the refusal does not name {needle!r}:\n{r.stderr}")
    assert "OK:" not in r.stdout, (
        "the artifact reported success on a path that refused")
    assert "effective ceremony configuration" not in r.stdout, (
        "the configuration was printed before the refusal fired; a check that "
        "runs the work and then refuses is not fail-closed")


@pytest.fixture
def bed(tmp_path):
    """A minimal but genuine ceremony bed: a real worktree, a real public key,
    and real executables. Nothing here is a stub -- the artifact stats these
    paths and would refuse a placeholder."""
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    subprocess.run(["git", "init", "-q", str(checkout)], check=True,
                   capture_output=True)

    key = tmp_path / "cairn_signing"
    if not shutil.which("ssh-keygen"):
        pytest.skip("no ssh-keygen on this host")
    subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f",
                    str(key), "-C", "reanchor-test"], check=True,
                   capture_output=True)
    key.unlink()                       # only the public half is ever recorded

    tools = {}
    for name in EXECUTABLE_KEYS:
        real = shutil.which({"python": "python3"}.get(name, name))
        if not real:
            pytest.skip(f"no {name} on this host")
        # Recorded as a RESOLVED regular file: the schema refuses a symlink on
        # any component, and /usr/bin and /opt/homebrew/bin are full of them.
        tools[name] = os.path.realpath(real)

    return {
        "dir": tmp_path,
        "values": {
            "schema": "cairn-ceremony-values/v1",
            "checkout": str(checkout),
            "signing_key": str(tmp_path / "cairn_signing.pub"),
            "package": str(tmp_path / "authorization-package.json"),
            "home": str(tmp_path),
            **tools,
        },
    }


def _write_values(bed, *, drop=(), extra_lines=(), override=None,
                  name="values") -> str:
    """Render a values file from the bed, with surgical damage applied."""
    values = dict(bed["values"])
    if override:
        values.update(override)
    lines = [f"{k} {v}" for k, v in values.items() if k not in drop]
    lines.extend(extra_lines)
    path = Path(bed["dir"]) / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(path)


# --------------------------------------------------------------------------
# the clean case, first -- every refusal node below is only meaningful if the
# undamaged file passes
# --------------------------------------------------------------------------

class TestTheCleanCase:

    def test_a_complete_values_file_validates(self, bed):
        r = _run("validate", _write_values(bed))
        assert r.returncode == 0, r.stderr
        assert "OK:" in r.stdout

    def test_validate_prints_the_complete_effective_configuration(self, bed):
        """The contract's stop-point: the Maintainer sees what will be used
        while it is still free to stop. Every key must appear with its value,
        because a partial print invites trusting a field nobody saw."""
        r = _run("validate", _write_values(bed))
        assert r.returncode == 0, r.stderr
        assert "effective ceremony configuration" in r.stdout
        for key, value in bed["values"].items():
            assert key in r.stdout, f"{key} missing from the printed config"
            assert value in r.stdout, (
                f"{key}'s value is not printed, so it would be used unseen")

    def test_the_print_says_nothing_was_discovered(self, bed):
        """The print is only a stop-point if the operator can tell that what
        it shows is what was recorded, not what the host happened to have."""
        r = _run("validate", _write_values(bed))
        assert "nothing below was discovered" in r.stdout


# --------------------------------------------------------------------------
# one node per refusal in the closed schema
# --------------------------------------------------------------------------

class TestTheGrammarRefuses:

    def test_an_unknown_key_refuses(self, bed):
        """The schema is closed. An unrecognised key is not an extra setting,
        it is a values file this contract did not review."""
        _assert_refused(
            _run("validate", _write_values(
                bed, extra_lines=("candidate_oid deadbeef",))),
            "unknown key")

    def test_a_duplicate_key_refuses(self, bed):
        """Last-wins and first-wins are both silent answers to a disagreement
        the operator has not noticed they wrote."""
        _assert_refused(
            _run("validate", _write_values(bed, extra_lines=("git /bin/sh",))),
            "duplicate key")

    @pytest.mark.parametrize("key", SCHEMA_KEYS)
    def test_every_missing_key_refuses(self, bed, key):
        """No ambient fallback, proven key by key rather than in general."""
        _assert_refused(_run("validate", _write_values(bed, drop=(key,))),
                        f"missing required key '{key}'")

    def test_a_key_with_no_value_refuses(self, bed):
        _assert_refused(
            _run("validate", _write_values(bed, extra_lines=("home",))),
            "key and no value")

    def test_a_relative_path_refuses(self, bed):
        """A relative path names a different file depending on where the
        ceremony was started."""
        _assert_refused(
            _run("validate", _write_values(bed, override={"git": "bin/git"})),
            "not an absolute path")

    def test_leading_whitespace_refuses(self, bed):
        _assert_refused(
            _run("validate", _write_values(bed, extra_lines=(" home /tmp",))),
            "begins with whitespace")

    def test_trailing_whitespace_refuses_rather_than_being_trimmed(self, bed):
        """Trimming would silently change a path into a different path that
        happens to exist."""
        _assert_refused(
            _run("validate", _write_values(
                bed, override={"home": str(bed["dir"]) + " "})),
            "ends with whitespace")

    def test_a_control_character_refuses(self, bed):
        _assert_refused(
            _run("validate", _write_values(
                bed, override={"home": str(bed["dir"]) + "\tx"})),
            "control character")

    def test_crlf_endings_refuse(self, bed):
        """The contract says LF. A CR at the end of every line is what a file
        edited on the wrong platform looks like, and it would otherwise turn
        every path into a path with an invisible byte on the end."""
        path = Path(_write_values(bed))
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        _assert_refused(_run("validate", str(path)), "control character")

    def test_a_hash_after_column_zero_is_part_of_the_value(self, bed):
        """`#` is a comment marker only at column 0. Anywhere else it is a
        legal character in a path, and treating it as a comment would silently
        truncate one."""
        odd = bed["dir"] / "ho#me"
        odd.mkdir()
        _assert_refused(
            _run("validate", _write_values(
                bed, override={"home": f"{odd} # trailing note"})),
            "not an existing directory")

    def test_an_over_long_line_refuses(self, bed):
        _assert_refused(
            _run("validate", _write_values(
                bed, extra_lines=("home /" + "a" * 5000,))),
            "the bound is 4096")

    def test_an_over_large_file_refuses(self, bed):
        """Bounded before it is trusted. The comment lines below are individually
        legal, so only the file bound can stop this one."""
        filler = tuple(f"# {'x' * 200}" for _ in range(400))
        _assert_refused(
            _run("validate", _write_values(bed, extra_lines=filler)),
            "exceeds 65536 bytes")

    def test_a_wrong_schema_version_refuses(self, bed):
        _assert_refused(
            _run("validate", _write_values(
                bed, override={"schema": "cairn-ceremony-values/v2"})),
            "and nothing else")


class TestTheRequiredStatesRefuse:

    @pytest.mark.parametrize("key", EXECUTABLE_KEYS)
    def test_a_missing_executable_bit_refuses(self, bed, key):
        """Each of these is *executed*. A non-executable file at the recorded
        path is a values file describing a host that no longer exists."""
        plain = bed["dir"] / f"not-executable-{key}"
        plain.write_text("#!/bin/sh\n")
        plain.chmod(0o644)
        _assert_refused(
            _run("validate", _write_values(bed, override={key: str(plain)})),
            "is not executable")

    @pytest.mark.parametrize("key", EXECUTABLE_KEYS)
    def test_a_directory_where_an_executable_belongs_refuses(self, bed, key):
        d = bed["dir"] / f"dir-{key}"
        d.mkdir()
        _assert_refused(
            _run("validate", _write_values(bed, override={key: str(d)})),
            "is not a regular file")

    @pytest.mark.parametrize("key", EXECUTABLE_KEYS)
    def test_an_absent_executable_refuses(self, bed, key):
        _assert_refused(
            _run("validate", _write_values(
                bed, override={key: str(bed["dir"] / "no-such-tool")})),
            "does not exist")

    def test_a_symlink_at_the_leaf_refuses(self, bed):
        """The Homebrew case, and the reason the template tells the operator to
        record a resolved path: /opt/homebrew/bin/git is a symlink into a
        version-pinned Cellar path."""
        link = bed["dir"] / "git-link"
        link.symlink_to(bed["values"]["git"])
        _assert_refused(
            _run("validate", _write_values(bed, override={"git": str(link)})),
            "is a symbolic link")

    def test_a_symlink_at_a_PARENT_refuses(self, bed):
        """Checking only the leaf is the version that fails: a symlinked parent
        redirects the whole subtree while the leaf looks ordinary."""
        real = bed["dir"] / "realbin"
        real.mkdir()
        tool = real / "git"
        tool.write_text("#!/bin/sh\n")
        tool.chmod(0o755)
        link = bed["dir"] / "linkbin"
        link.symlink_to(real)
        _assert_refused(
            _run("validate", _write_values(
                bed, override={"git": str(link / "git")})),
            "is a symbolic link")

    def test_a_signing_key_that_is_a_directory_refuses(self, bed):
        d = bed["dir"] / "keydir"
        d.mkdir()
        _assert_refused(
            _run("validate", _write_values(
                bed, override={"signing_key": str(d)})),
            "is not a regular file")

    def test_a_checkout_that_is_not_a_worktree_top_level_refuses(self, bed):
        """`git -C` discovers UPWARD, so a path beneath a repository would
        otherwise bless a repository that was never named."""
        below = Path(bed["values"]["checkout"]) / "subdir"
        below.mkdir()
        _assert_refused(
            _run("validate", _write_values(
                bed, override={"checkout": str(below)})),
            "not a worktree top level")

    def test_a_package_parent_that_does_not_exist_refuses(self, bed):
        _assert_refused(
            _run("validate", _write_values(bed, override={
                "package": str(bed["dir"] / "no-such-dir" / "pkg.json")})),
            "is not an existing directory")

    def test_the_package_leaf_is_not_judged_at_validate_time(self, bed):
        """Stage-dependent by contract -- absent at stage 1, present at stage 2
        -- so `validate` reports its state without ruling on it. Judging it here
        would make one of the two stages unvalidatable."""
        for present in (False, True):
            pkg = Path(bed["values"]["package"])
            if present:
                pkg.write_text("{}\n")
            elif pkg.exists():
                pkg.unlink()
            r = _run("validate", _write_values(bed))
            assert r.returncode == 0, r.stderr
            expected = "PRESENT" if present else "ABSENT"
            assert f"package leaf: {expected}" in r.stdout, r.stdout


# --------------------------------------------------------------------------
# the properties that make it a *parser*
# --------------------------------------------------------------------------

class TestTheValuesFileIsParsedNeverExecuted:
    """No `source`, no `eval`, no command substitution, no shell expansion.

    These are the nodes that would catch the whole design being wrong rather
    than one rule being wrong: a values file that can execute is not a data
    contract, it is a second script nobody reviewed.
    """

    def test_a_command_substitution_in_a_value_is_taken_literally(self, bed):
        """If the value were expanded, the marker would not exist and the path
        would resolve to something. The marker existing IS the proof that the
        substitution never ran."""
        marker = bed["dir"] / "SUBSTITUTION-RAN"
        payload = f"$(touch {marker})"
        r = _run("validate", _write_values(bed, override={"home": payload}))
        assert not marker.exists(), (
            "the parser executed a command substitution out of the values file")
        _assert_refused(r, "not an absolute path")

    def test_a_backtick_in_a_value_is_taken_literally(self, bed):
        marker = bed["dir"] / "BACKTICK-RAN"
        r = _run("validate", _write_values(
            bed, override={"home": f"`touch {marker}`"}))
        assert not marker.exists(), "the parser executed a backtick expansion"
        _assert_refused(r, "not an absolute path")

    def test_a_glob_in_a_value_is_not_expanded(self, bed):
        """A path is the path that was recorded. Expanding `*` would silently
        select whichever file the directory happened to contain."""
        _assert_refused(
            _run("validate", _write_values(
                bed, override={"git": str(bed["dir"] / "*")})),
            "does not exist")

    def test_a_variable_reference_in_a_value_is_not_expanded(self, bed):
        env = dict(os.environ)
        env["CAIRN_TEST_INJECTED"] = bed["values"]["git"]
        r = _run("validate", _write_values(
            bed, override={"git": "$CAIRN_TEST_INJECTED"}), env=env)
        _assert_refused(r, "not an absolute path")

    def test_the_artifact_contains_no_eval_or_source(self):
        """A source-level statement of the same property. The behavioural nodes
        above prove the parser as written does not expand; this one fails the
        moment someone adds a construct that could."""
        text = _ARTIFACT.read_text(encoding="utf-8")
        code = "\n".join(l for l in text.splitlines()
                         if not l.lstrip().startswith("#"))
        for banned in ("eval ", "eval\t", "source ", ". \""):
            assert banned not in code, (
                f"the artifact contains {banned!r}; the values file must be "
                f"parsed, never executed")

    def test_the_source_scan_would_notice_a_real_eval(self):
        """Mutation check for the node above: if the comment stripper ate
        everything, 'no match' would mean 'nothing was searched'."""
        text = _ARTIFACT.read_text(encoding="utf-8") + '\neval "$V_home"\n'
        code = "\n".join(l for l in text.splitlines()
                         if not l.lstrip().startswith("#"))
        assert "eval " in code


class TestThereIsNoAmbientFallback:

    def test_an_absent_executable_field_is_not_filled_from_PATH(self, bed):
        """The field is dropped while PATH still resolves the tool perfectly
        well. Refusing anyway is the whole point: ambient discovery is what let
        a replacement utility vouch for bytes it had just rewritten."""
        env = dict(os.environ)
        env["PATH"] = "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"
        assert shutil.which("git", path=env["PATH"]), (
            "this node is vacuous unless PATH really could supply git")
        _assert_refused(
            _run("validate", _write_values(bed, drop=("git",)), env=env),
            "missing required key 'git'")

    def test_an_absent_home_field_is_not_filled_from_the_environment(self, bed):
        env = dict(os.environ)
        env["HOME"] = str(bed["dir"])
        _assert_refused(
            _run("validate", _write_values(bed, drop=("home",)), env=env),
            "missing required key 'home'")


# --------------------------------------------------------------------------
# the template and the artifact must describe one schema
# --------------------------------------------------------------------------

class TestTheTemplateMatchesTheSchema:
    """The template is what an operator copies. If it drifts from the parser,
    the first thing a new Maintainer meets is a refusal on a file the
    repository itself handed them."""

    def _template_keys(self) -> list[str]:
        keys = []
        for line in _EXAMPLE.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#"):
                continue
            keys.append(line.split(" ", 1)[0])
        return keys

    def test_the_template_carries_every_key_exactly_once(self):
        keys = self._template_keys()
        assert sorted(keys) == sorted(SCHEMA_KEYS), (
            f"template keys {sorted(keys)} != schema {sorted(SCHEMA_KEYS)}")
        assert len(keys) == len(set(keys)), "a key appears twice in the template"

    def test_the_template_does_not_carry_an_authority_value(self):
        """The reviewed candidate OID and the artifact digest travel the
        reviewed launcher, never this mutable file."""
        keys = self._template_keys()
        for forbidden in ("candidate", "candidate_oid", "artifact_digest",
                          "review_manifest"):
            assert forbidden not in keys, (
                f"'{forbidden}' is an authority value and must not sit in a "
                f"file the ceremony invites the operator to edit")

    def test_the_template_itself_refuses_because_its_paths_are_placeholders(
            self, tmp_path):
        """The shipped template must not be usable as-is. It carries
        `/absolute/path/to/...` placeholders, and a template that validated
        would mean the parser was not checking the filesystem at all."""
        copy = tmp_path / "values"
        copy.write_text(_EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
        r = _run("validate", str(copy))
        assert r.returncode != 0, (
            "the shipped template validated unedited, so nothing is checked")

    def test_the_template_tells_the_operator_how_to_refresh_stale_paths(self):
        """The recorded executable paths go stale at every toolchain upgrade,
        because a resolved Homebrew path is version-pinned. An operator who is
        not told that meets a correct refusal and reads it as a broken tool."""
        text = _EXAMPLE.read_text(encoding="utf-8")
        assert "upgrade" in text
        assert "validate" in text


class TestTheCommandSurface:

    def test_no_argument_is_a_usage_error_not_a_crash(self):
        r = _run()
        assert r.returncode == 2, (r.returncode, r.stdout, r.stderr)
        assert "usage:" in r.stderr

    def test_an_unknown_command_refuses(self):
        r = _run("bless-everything", "/dev/null")
        assert r.returncode != 0
        assert "unknown command" in r.stderr

    def test_validate_requires_exactly_one_values_file(self, bed):
        r = _run("validate")
        assert r.returncode != 0
        assert "exactly one argument" in r.stderr

    def test_the_artifact_passes_a_shell_syntax_check(self):
        """This repository has no shell standing gate, so the artifact carries
        its own. A syntax error here would surface *after* the key is loaded."""
        r = subprocess.run(["/bin/sh", "-n", str(_ARTIFACT)],
                           capture_output=True, text=True, check=False)
        assert r.returncode == 0, r.stderr

    def test_the_artifact_never_invokes_cat_by_bare_name(self):
        """`cat` is in the schema precisely so it is bound. Reaching for it by
        bare name would find it through ambient PATH -- the gap the recorded
        paths exist to close."""
        text = _ARTIFACT.read_text(encoding="utf-8")
        code = "\n".join(l for l in text.splitlines()
                         if not l.lstrip().startswith("#"))
        assert "cat <<" not in code, (
            "a heredoc into bare `cat` reintroduces an unbound executable")
        for line in code.splitlines():
            stripped = line.strip()
            assert not stripped.startswith("cat "), stripped


# --------------------------------------------------------------------------
# the operator command surface
# --------------------------------------------------------------------------

#: A stand-in for the checker that records exactly how it was invoked and then
#: exits cleanly. It is NOT a stub of the artifact: the values parsing, the
#: refusals, the argument assembly and the environment construction below are
#: all the real thing. Only the far end of the invocation is replaced, because
#: a genuine stage 1 needs a real gate anchor and a real ceremony -- which is
#: the end-to-end node's job, not this one's.
#: The record path is BAKED IN rather than passed through the environment.
#: It has to be: the artifact invokes the checker under `env -i`, so nothing
#: from the caller's environment survives -- which is the property
#: `test_stage1_runs_under_an_emptied_environment` exists to assert. A stub
#: that needed an inherited variable could only work by weakening it.
_RECORDING_CHECKER = '''\
import json, os, sys
record = {"argv": sys.argv[1:], "env": dict(os.environ)}
with open(r"@RECORD@", "w") as fh:
    json.dump(record, fh)
print("[stub] checker invoked")
'''


@pytest.fixture
def staged(bed, tmp_path):
    """The artifact placed as it is placed in a real ceremony: `reanchor.sh`
    beside `tests/_gate_preflight.py`.

    The artifact resolves the checker RELATIVE TO ITSELF, so this layout is the
    contract, not a convenience. Copying it here is also what lets the checker
    be a recorder without touching the repository's real one.
    """
    root = tmp_path / "extracted"
    (root / "tests").mkdir(parents=True)
    shutil.copy2(_ARTIFACT, root / "reanchor.sh")
    record = tmp_path / "invocation.json"
    (root / "tests" / "_gate_preflight.py").write_text(
        _RECORDING_CHECKER.replace("@RECORD@", str(record)))
    return {"artifact": root / "reanchor.sh", "record": record}


def _run_staged(staged, *args, env=None, record=True):
    child = dict(env or os.environ)
    r = subprocess.run(["/bin/sh", str(staged["artifact"]), *args],
                       capture_output=True, text=True, check=False, env=child)
    invocation = None
    if record and staged["record"].exists():
        import json as _json
        invocation = _json.loads(staged["record"].read_text())
    return r, invocation


class TestStage1RunsTheCheckerWithTheRecordedValues:

    def test_stage1_passes_every_recorded_value_through(self, bed, staged):
        r, inv = _run_staged(staged, "stage1", _write_values(bed))
        assert r.returncode == 0, r.stderr
        assert inv is not None, f"the checker was never invoked:\n{r.stderr}"
        argv = inv["argv"]
        assert argv[0] == "stage1"
        assert "--repo" in argv
        assert argv[argv.index("--repo") + 1] == bed["values"]["checkout"]
        assert argv[argv.index("--package-out") + 1] == bed["values"]["package"]
        assert argv[argv.index("--signing-key") + 1] == \
            bed["values"]["signing_key"]

    def test_stage1_prints_the_effective_configuration_before_running(
            self, bed, staged):
        """The contract puts the stop-point *before stage 1*, and the launcher
        invokes stage1 directly -- it never calls `validate`. A stop-point on a
        command nobody runs is not a stop-point."""
        r, _inv = _run_staged(staged, "stage1", _write_values(bed))
        assert "effective ceremony configuration" in r.stdout
        assert r.stdout.index("effective ceremony configuration") < \
            r.stdout.index("[stub] checker invoked"), (
                "the configuration must print BEFORE the checker runs, or the "
                "operator sees it only after the thing they might have stopped")

    def test_stage1_receives_no_agent_socket(self, bed, staged):
        """Chunk A's decision, enforced in the artifact as well as the runbook.

        Stage 1 runs candidate code. Handing it a live signing channel buys the
        stage nothing -- it cannot sign by contract -- and hands that candidate
        code exactly what the ceremony's boundary exists to withhold.
        """
        env = dict(os.environ)
        env["SSH_AUTH_SOCK"] = "/tmp/cairn-test-agent-socket"
        r, inv = _run_staged(staged, "stage1", _write_values(bed), env=env)
        assert r.returncode == 0, r.stderr
        assert "SSH_AUTH_SOCK" not in inv["env"], (
            "stage 1 was handed an agent socket; the channel is removed, not "
            "measured")

    def test_stage1_runs_under_an_emptied_environment(self, bed, staged):
        """Nothing is inherited. An ambient GIT_* variable can steer git at a
        repository nobody named, and an ambient PATH is what let a replacement
        utility vouch for bytes it had just rewritten."""
        env = dict(os.environ)
        env["GIT_DIR"] = "/tmp/somewhere-else/.git"
        env["CAIRN_LEAKED"] = "should-not-arrive"
        r, inv = _run_staged(staged, "stage1", _write_values(bed), env=env)
        assert r.returncode == 0, r.stderr
        assert "GIT_DIR" not in inv["env"]
        assert "CAIRN_LEAKED" not in inv["env"]
        assert inv["env"]["PATH"] == "/usr/bin:/bin"
        assert inv["env"]["HOME"] == bed["values"]["home"]

    def test_stage1_refuses_to_overwrite_an_existing_package(self, bed, staged):
        """An existing package is either a run already in progress or a stale
        one, and neither is safe to bless."""
        Path(bed["values"]["package"]).write_text("{}\n")
        r, inv = _run_staged(staged, "stage1", _write_values(bed))
        _assert_refused(r, "already exists")
        assert inv is None, "the checker ran despite the refusal"

    def test_stage1_refuses_when_the_checker_is_not_beside_it(self, bed,
                                                              tmp_path):
        """The artifact and the checker arrive in one verified extraction. A
        missing checker means this artifact is running somewhere it was not
        placed -- and the alternative, searching for one, is how a verified
        artifact ends up driving an unverified checker."""
        lonely = tmp_path / "lonely"
        lonely.mkdir()
        shutil.copy2(_ARTIFACT, lonely / "reanchor.sh")
        r = subprocess.run(
            ["/bin/sh", str(lonely / "reanchor.sh"), "stage1",
             _write_values(bed)],
            capture_output=True, text=True, check=False)
        _assert_refused(r, "not beside this artifact")


class TestStage2IsTheStageThatSigns:

    def _values(self, bed):
        Path(bed["values"]["package"]).write_text('{"schema": "x"}\n')
        return _write_values(bed)

    def test_stage2_forwards_the_agent_socket(self, bed, staged):
        """The deliberate asymmetry with stage 1. Without the socket
        `git commit-tree` invokes the signer with no controlling terminal,
        falls back to `ssh-askpass`, and dies naming a path that does not exist
        on a stock host."""
        env = dict(os.environ)
        env["SSH_AUTH_SOCK"] = "/tmp/cairn-test-agent-socket"
        r, inv = _run_staged(staged, "stage2", self._values(bed),
                             "--confirm-package-sha256", "abc123", env=env)
        assert r.returncode == 0, r.stderr
        assert inv["env"].get("SSH_AUTH_SOCK") == \
            "/tmp/cairn-test-agent-socket", (
                "stage 2 lost the agent socket; it is the stage that signs")

    def test_stage2_passes_the_confirmation_digest_through(self, bed, staged):
        r, inv = _run_staged(staged, "stage2", self._values(bed),
                             "--confirm-package-sha256", "abc123")
        assert r.returncode == 0, r.stderr
        argv = inv["argv"]
        assert argv[0] == "stage2"
        assert argv[argv.index("--confirm-package-sha256") + 1] == "abc123"
        assert argv[argv.index("--package") + 1] == bed["values"]["package"]

    def test_stage2_without_a_confirmation_digest_refuses(self, bed, staged):
        """The digest is the Maintainer's act. A stage 2 that defaulted it
        would be confirming on their behalf."""
        r, inv = _run_staged(staged, "stage2", self._values(bed),
                             "--review-manifest", "/x", "--reviewed-candidate",
                             "y")
        _assert_refused(r, "requires --confirm-package-sha256")
        assert inv is None

    def test_stage2_refuses_when_the_package_is_missing(self, bed, staged):
        r, inv = _run_staged(staged, "stage2", _write_values(bed),
                             "--confirm-package-sha256", "abc123")
        _assert_refused(r, "does not exist")
        assert inv is None


class TestTransitionModeTakesBothInputsOrNeither:
    """A manifest without the OID it was reviewed against, or an OID with no
    reviewed member set, is half an authority change."""

    def test_both_transition_inputs_reach_the_checker(self, bed, staged,
                                                      tmp_path):
        manifest = tmp_path / "review-manifest.txt"
        manifest.write_text("schema x\n")
        r, inv = _run_staged(staged, "stage1", _write_values(bed),
                             "--review-manifest", str(manifest),
                             "--reviewed-candidate", "deadbeef")
        assert r.returncode == 0, r.stderr
        argv = inv["argv"]
        assert argv[argv.index("--transition-from-review") + 1] == str(manifest)
        assert argv[argv.index("--reviewed-candidate") + 1] == "deadbeef"

    def test_a_manifest_without_a_candidate_refuses(self, bed, staged,
                                                    tmp_path):
        manifest = tmp_path / "review-manifest.txt"
        manifest.write_text("schema x\n")
        r, inv = _run_staged(staged, "stage1", _write_values(bed),
                             "--review-manifest", str(manifest))
        _assert_refused(r, "without --reviewed-candidate")
        assert inv is None

    def test_a_candidate_without_a_manifest_refuses(self, bed, staged):
        r, inv = _run_staged(staged, "stage1", _write_values(bed),
                             "--reviewed-candidate", "deadbeef")
        _assert_refused(r, "without --review-manifest")
        assert inv is None

    def test_a_symlinked_review_manifest_refuses(self, bed, staged, tmp_path):
        real = tmp_path / "real-manifest.txt"
        real.write_text("schema x\n")
        link = tmp_path / "linked-manifest.txt"
        link.symlink_to(real)
        r, inv = _run_staged(staged, "stage1", _write_values(bed),
                             "--review-manifest", str(link),
                             "--reviewed-candidate", "deadbeef")
        _assert_refused(r, "is a symbolic link")
        assert inv is None

    def test_an_unexpected_argument_refuses(self, bed, staged):
        r, inv = _run_staged(staged, "stage1", _write_values(bed),
                             "--bless-anyway")
        _assert_refused(r, "unexpected argument")
        assert inv is None


class TestHashPackage:
    """The step whose absence made the Maintainer improvise a command."""

    def test_the_digest_is_computed_over_the_bytes_on_disk(self, bed):
        import hashlib
        pkg = Path(bed["values"]["package"])
        payload = b'{"schema": "cairn-authorization-package/v1"}\n'
        pkg.write_bytes(payload)
        expected = hashlib.sha256(payload).hexdigest()
        r = _run("hash-package", _write_values(bed))
        assert r.returncode == 0, r.stderr
        assert expected in r.stdout, (
            f"expected {expected} over the file's bytes:\n{r.stdout}")

    def test_a_digest_inside_the_package_is_not_the_answer(self, bed):
        """A package can carry any digest it likes about itself. The confirmed
        digest is computed over the file, never read out of it."""
        import hashlib
        pkg = Path(bed["values"]["package"])
        lie = "0" * 64
        payload = ('{"self_sha256": "%s"}\n' % lie).encode()
        pkg.write_bytes(payload)
        r = _run("hash-package", _write_values(bed))
        assert r.returncode == 0, r.stderr
        assert hashlib.sha256(payload).hexdigest() in r.stdout
        assert r.stdout.count(lie) == 0 or "self_sha256" not in r.stdout, (
            "the command echoed a digest the package asserted about itself")

    def test_hash_package_refuses_when_the_package_is_absent(self, bed):
        r = _run("hash-package", _write_values(bed))
        _assert_refused(r, "does not exist")

    def test_hash_package_takes_exactly_one_argument(self, bed):
        r = _run("hash-package")
        assert r.returncode != 0
        assert "exactly one argument" in r.stderr


class TestShowReport:
    """A confirmed digest over an unread report authorizes something you have
    not seen. This is the command that makes the report readable."""

    def _package(self, bed, *, paths_per_class=3):
        pkg = Path(bed["values"]["package"])
        by_class = {
            "frozen": [f"bootstrap/tests/frozen_{i}.py"
                       for i in range(paths_per_class)],
            "outside_coverage": [f"docs/note_{i}.md"
                                 for i in range(paths_per_class)],
        }
        pkg.write_text(__import__("json").dumps({
            "schema": "cairn-authorization-package/v1",
            "range_report": {
                "anchor": "a" * 40,
                "candidate_head": "b" * 40,
                "branch": "master",
                "expected_old": "c" * 40,
                "manifest_sha256": "d" * 64,
                "by_class": by_class,
                "counts": {k: len(v) for k, v in by_class.items()},
                "signatures": {"total": 3, "unsigned": 0},
            },
        }, indent=2))
        return _write_values(bed)

    def test_the_report_renders_what_is_being_authorized(self, bed):
        r = _run("show-report", self._package(bed))
        assert r.returncode == 0, r.stderr
        for expected in ("a" * 40, "b" * 40, "master", "d" * 64,
                         "bootstrap/tests/frozen_0.py", "docs/note_0.md"):
            assert expected in r.stdout, f"{expected!r} missing:\n{r.stdout}"

    def test_the_counts_are_rendered(self, bed):
        r = _run("show-report", self._package(bed))
        assert "frozen" in r.stdout and "outside_coverage" in r.stdout

    def test_a_long_class_is_bounded_and_SAYS_it_was_bounded(self, bed):
        """Bounded, not silently truncated. A cut list that does not say it was
        cut reads as 'that was all of it' -- which is exactly the wrong thing to
        believe about a set of changes you are authorizing."""
        r = _run("show-report", self._package(bed, paths_per_class=120))
        assert r.returncode == 0, r.stderr
        assert "NOT SHOWN" in r.stdout, (
            "a bounded render must name what it dropped")
        assert "80 more" in r.stdout, r.stdout[-1500:]

    def test_a_package_with_no_report_refuses(self, bed):
        Path(bed["values"]["package"]).write_text('{"schema": "x"}\n')
        r = _run("show-report", _write_values(bed))
        assert r.returncode != 0
        assert "no range report" in r.stderr

    def test_show_report_refuses_when_the_package_is_absent(self, bed):
        r = _run("show-report", _write_values(bed))
        _assert_refused(r, "does not exist")


class TestEveryPublicCommandIsExercised:
    """The contract requires every public command to be exercised through its
    public path. This node fails if a command is added and never driven -- the
    'built, unit-tested, and never reached by the governing path' shape this
    repository keeps finding."""

    PUBLIC_COMMANDS = ("validate", "stage1", "show-report", "hash-package",
                       "stage2")

    def test_the_dispatch_knows_exactly_these_commands(self):
        text = _ARTIFACT.read_text(encoding="utf-8")
        dispatch = text.split("    case $_main_cmd in", 1)[1].split("\n    esac", 1)[0]
        arms = [l.strip().rstrip(")") for l in dispatch.splitlines()
                if l.strip().endswith(")") and not l.strip().startswith("#")]
        named = [a for a in arms if a not in ("*", "-h|--help|help")]
        assert sorted(named) == sorted(self.PUBLIC_COMMANDS), (
            f"the dispatch offers {sorted(named)}; this test knows "
            f"{sorted(self.PUBLIC_COMMANDS)}. A command with no test is a "
            f"command the ceremony has not been shown to have")

    def test_the_usage_text_documents_every_public_command(self):
        text = _ARTIFACT.read_text(encoding="utf-8")
        usage = text.split("usage() {", 1)[1].split("\n}", 1)[0]
        for cmd in self.PUBLIC_COMMANDS:
            assert cmd in usage, f"'{cmd}' is undocumented in usage"
