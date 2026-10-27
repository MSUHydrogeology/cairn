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
import sys
from pathlib import Path

import pytest

from bootstrap.tests import _gate_preflight as P
from bootstrap.tests.test_repin import a_copy_of_this_interpreter

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


#: The artifact commands that take the thirteen recorded values.
VALUE_COMMANDS = ("validate", "stage1", "stage2", "show-report", "hash-package")


def _values_args(path) -> list[str]:
    """The thirteen values of a CLEAN values file, in the schema's order.

    This is what the launcher does for the artifact: it reads the file once and
    hands the values over as arguments. A file with a missing or repeated key is
    never handed over -- the launcher refuses it first -- so a test that needs
    one goes through the launcher, and this helper asserts rather than guesses.
    """
    found: dict[str, str] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            key, _, value = line.partition(" ")
            assert key not in found, f"{key} repeated: use the launcher"
            found[key] = value
    assert sorted(found) == sorted(SCHEMA_KEYS), (
        f"{sorted(set(SCHEMA_KEYS) ^ set(found))} differ: use the launcher")
    return [found[k] for k in SCHEMA_KEYS]


def _artifact_argv(args) -> list[str]:
    """`command <values-file> ...` becomes `command <13 values> ...`."""
    args = list(args)
    if len(args) >= 2 and args[0] in VALUE_COMMANDS and os.path.isfile(args[1]):
        args[1:2] = _values_args(args[1])
    return args


def _run(*args: str, env: dict | None = None,
         cwd=None) -> subprocess.CompletedProcess:
    """Invoke the artifact the way the launcher does: `/bin/sh <artifact>`, the
    values as its first arguments.

    Literally `/bin/sh`, as everywhere else in this ceremony -- a
    non-interactive `/bin/sh` reads no startup file, which is what makes the
    child clean.
    """
    return subprocess.run(["/bin/sh", str(_ARTIFACT), *_artifact_argv(args)],
                          capture_output=True, text=True, check=False,
                          env=env, cwd=cwd)


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

    # An ANCHORED ROSTER naming this key, because stage 1 now refuses a signing
    # key the anchor does not name. The fixture has to model that: a bed with no
    # anchor would test a state no real ceremony can be in, and the refusal it
    # produced would look like a fixture bug rather than the control working.
    pub = key.with_suffix(".pub").read_text().split()
    roster = checkout / "dev" / ".cairn" / "allowed_signers"
    roster.parent.mkdir(parents=True, exist_ok=True)
    roster.write_text(f"reanchor-test {pub[0]} {pub[1]}\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(checkout), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(checkout), "-c", "user.email=t@t",
                    "-c", "user.name=t", "commit", "-qm", "roster"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(checkout), "update-ref",
                    "refs/cairn/gate-anchor", "HEAD"], check=True,
                   capture_output=True)

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
# one node per refusal in the closed schema -- the launcher is the only reader
# --------------------------------------------------------------------------

class TestTheLauncherRefusesTheGrammar:
    """The values file is read once, by the launcher, before any candidate byte
    runs. Every node asserts the refusal AND that no candidate code started."""

    def test_an_unknown_key_refuses(self, ceremony):
        """The schema is closed. An unrecognised key is not an extra setting,
        it is a values file this contract did not review."""
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"], extra_lines=("candidate_oid deadbeef",)))
        _assert_no_candidate_code_ran(ceremony, r, "unknown key")

    def test_a_duplicate_key_refuses(self, ceremony):
        """Last-wins and first-wins are both silent answers to a disagreement
        the operator has not noticed they wrote."""
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"], extra_lines=("git /bin/sh",)))
        _assert_no_candidate_code_ran(ceremony, r, "duplicate key")

    @pytest.mark.parametrize("key", SCHEMA_KEYS)
    def test_every_missing_key_refuses(self, ceremony, key):
        """No ambient fallback, proven key by key rather than in general."""
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"], drop=(key,), name=f"values-drop-{key}"))
        _assert_no_candidate_code_ran(
            ceremony, r, f"missing required key '{key}'")

    def test_a_key_with_no_value_refuses(self, ceremony):
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"], extra_lines=("home",)))
        _assert_no_candidate_code_ran(ceremony, r, "key and no value")

    def test_a_relative_path_refuses(self, ceremony):
        """A relative path names a different file depending on where the
        ceremony was started."""
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"], override={"git": "bin/git"}))
        _assert_no_candidate_code_ran(ceremony, r, "not an absolute path")

    def test_leading_whitespace_refuses(self, ceremony):
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"], extra_lines=(" home /tmp",)))
        _assert_no_candidate_code_ran(ceremony, r, "begins with whitespace")

    def test_trailing_whitespace_refuses_rather_than_being_trimmed(
            self, ceremony):
        """Trimming would silently change a path into a different path that
        happens to exist."""
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"],
            override={"home": str(ceremony["dir"]) + " "}))
        _assert_no_candidate_code_ran(ceremony, r, "ends with whitespace")

    def test_a_control_character_refuses(self, ceremony):
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"],
            override={"home": str(ceremony["dir"]) + "\tx"}))
        _assert_no_candidate_code_ran(ceremony, r, "control character")

    def test_crlf_endings_refuse(self, ceremony):
        """The contract says LF. A CR at the end of every line is what a file
        edited on the wrong platform looks like, and it would otherwise turn
        every path into a path with an invisible byte on the end."""
        path = Path(_write_values(ceremony["bed"]))
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        r = _launch(ceremony, values=str(path))
        _assert_no_candidate_code_ran(ceremony, r, "control character")

    def test_a_hash_after_column_zero_is_part_of_the_value(self, ceremony):
        """`#` is a comment marker only at column 0. Anywhere else it is a
        legal character in a path, and treating it as a comment would silently
        truncate one."""
        odd = ceremony["dir"] / "ho#me"
        odd.mkdir()
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"], override={"home": f"{odd} # trailing note"}))
        _assert_no_candidate_code_ran(
            ceremony, r, "not an existing directory")

    def test_an_over_long_line_refuses(self, ceremony):
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"], extra_lines=("home /" + "a" * 5000,)))
        _assert_no_candidate_code_ran(ceremony, r, "exceeds 4096 bytes")

    def test_an_over_large_file_refuses(self, ceremony):
        """Bounded before it is trusted. The comment lines below are individually
        legal, so only the file bound can stop this one."""
        filler = tuple(f"# {'x' * 200}" for _ in range(400))
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"], extra_lines=filler))
        _assert_no_candidate_code_ran(ceremony, r, "exceeds 65536 bytes")

    def test_a_wrong_schema_version_refuses(self, ceremony):
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"],
            override={"schema": "cairn-ceremony-values/v2"}))
        _assert_no_candidate_code_ran(ceremony, r, "and nothing else")


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
    contract, it is a second script nobody reviewed. The launcher reads the
    file; the artifact takes the values as arguments and must treat each one
    as text just the same.
    """

    def test_the_launcher_takes_every_expansion_literally(self, ceremony):
        """Each hostile value would leave a marker if the reader expanded it.
        The launcher is the only reader, so it is held to the same four
        properties as the artifact's argument checks below."""
        for label, payload in (
                ("substitution", f"$(touch {ceremony['dir']}/SUB)"),
                ("backtick", f"`touch {ceremony['dir']}/TICK`"),
                ("glob", str(ceremony["dir"] / "*")),
                ("variable", "$HOME")):
            r = _launch(ceremony, values=_write_values(
                ceremony["bed"], override={"git": payload},
                name=f"values-{label}"))
            _assert_no_candidate_code_ran(ceremony, r, "git:")
        assert not (ceremony["dir"] / "SUB").exists()
        assert not (ceremony["dir"] / "TICK").exists()

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

    def test_neither_the_artifact_nor_the_launcher_contains_eval_or_source(
            self):
        """A source-level statement of the same property. The behavioural nodes
        above prove the reader as written does not expand; this one fails the
        moment someone adds a construct that could."""
        for path in (_ARTIFACT, _LAUNCHER_TEMPLATE):
            text = path.read_text(encoding="utf-8")
            code = "\n".join(l for l in text.splitlines()
                             if not l.lstrip().startswith("#"))
            for banned in ("eval ", "eval\t", "source ", ". \""):
                assert banned not in code, (
                    f"{path.name} contains {banned!r}; the values file must "
                    f"be parsed, never executed")

    def test_the_source_scan_would_notice_a_real_eval(self):
        """Mutation check for the node above: if the comment stripper ate
        everything, 'no match' would mean 'nothing was searched'."""
        text = _ARTIFACT.read_text(encoding="utf-8") + '\neval "$V_home"\n'
        code = "\n".join(l for l in text.splitlines()
                         if not l.lstrip().startswith("#"))
        assert "eval " in code


class TestThereIsNoAmbientFallback:

    def test_an_absent_field_is_not_filled_from_an_EXPORTED_L_VARIABLE(
            self, ceremony):
        """The reader's own variable name, exported, is a second channel.

        The schema check asks `[ -n "${L_key+s}" ]` -- *is this variable set* --
        and an exported environment variable answers exactly as a values-file
        line does. Before the reader zeroed its outputs, an exported `L_shasum`
        satisfied the missing-key refusal for a values file that never named
        shasum, and that program then ran inside the pre-candidate window.
        Every one of the thirteen is checked, because the reader's unset list
        is what makes each of them true.
        """
        assert Path("/bin/echo").is_file(), (
            "this node is vacuous unless the injected value would pass the "
            "executable check that follows the schema check")
        for key in SCHEMA_KEYS:
            env = dict(os.environ)
            env[f"L_{key}"] = "/bin/echo"
            r = _launch(ceremony, values=_write_values(
                ceremony["bed"], drop=(key,), name=f"values-no-{key}"),
                env=env)
            _assert_no_candidate_code_ran(
                ceremony, r, f"missing required key '{key}'")

    def test_an_absent_executable_field_is_not_filled_from_PATH(self, ceremony):
        """The field is dropped while PATH still resolves the tool perfectly
        well. Refusing anyway is the whole point: ambient discovery is what let
        a replacement utility vouch for bytes it had just rewritten."""
        env = dict(os.environ)
        env["PATH"] = "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"
        assert shutil.which("git", path=env["PATH"]), (
            "this node is vacuous unless PATH really could supply git")
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"], drop=("git",)), env=env)
        _assert_no_candidate_code_ran(ceremony, r, "missing required key 'git'")

    def test_an_absent_home_field_is_not_filled_from_the_environment(
            self, ceremony):
        env = dict(os.environ)
        env["HOME"] = str(ceremony["dir"])
        r = _launch(ceremony, values=_write_values(
            ceremony["bed"], drop=("home",)), env=env)
        _assert_no_candidate_code_ran(ceremony, r, "missing required key 'home'")


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

    def test_validate_requires_exactly_the_thirteen_values(self, bed):
        r = _run("validate")
        assert r.returncode != 0
        assert "13 recorded values" in r.stderr
        r = _run("validate", *_values_args(_write_values(bed)), "extra")
        assert r.returncode != 0 and "13 recorded values" in r.stderr

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
record = {"argv": sys.argv[1:], "env": dict(os.environ),
          "flags": {"no_site": sys.flags.no_site,
                    "ignore_environment": sys.flags.ignore_environment,
                    "no_user_site": sys.flags.no_user_site}}
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
    r = subprocess.run(["/bin/sh", str(staged["artifact"]),
                        *_artifact_argv(args)],
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

    @pytest.mark.parametrize("via_launcher", (False, True))
    def test_the_next_step_it_prints_starts_stage_two_under_a_short_environment(
            self, bed, staged, via_launcher):
        """The signer must not inherit the key socket, so every place that tells him how to start
        stage 2 shows the short environment, with the home the values file names."""
        env = {k: v for k, v in os.environ.items() if not k.startswith("CAIRN_")}
        if via_launcher:
            env.update(CAIRN_LAUNCHER="/x/launcher.sh", CAIRN_PACKET="/x/packet.txt",
                       CAIRN_VALUES="/x/values", CAIRN_CANDIDATE="c" * 40)
        r, _inv = _run_staged(staged, "stage1", _write_values(bed), env=env)
        assert r.returncode == 0, r.stderr
        text = " ".join((r.stdout + r.stderr).replace("\\\n", " ").split())
        short = f'env -i HOME={bed["values"]["home"]} PATH=/usr/bin:/bin TERM="$TERM" LANG=C /bin/sh'
        assert short in text, text[-900:]
        if via_launcher:
            assert f"{short} /x/launcher.sh /x/packet.txt /x/values {'c' * 40} --stage2" in text

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
             *_values_args(_write_values(bed))],
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


class TestTheArtifactStartsEveryPythonWithoutSite:
    """The interpreter starts under `-E -s -S`. Stage 1 runs the candidate's
    own tests as the Maintainer, so a `.pth` file left in the interpreter's
    packages folder is code that the next start would otherwise run, with the
    key loaded in stage 2. `-S` skips the folder; the control shows the file
    is read without it."""

    @pytest.mark.parametrize("command", ["stage1", "stage2", "show-report"])
    def test_a_pth_file_in_the_packages_folder_runs_in_no_start(
            self, bed, staged, tmp_path, command):
        binary, marker = _interpreter_with_a_planted_pth_file(tmp_path)
        values = _write_values(bed, override={"python": str(binary)})
        if command == "show-report":
            Path(bed["values"]["package"]).write_text(__import__("json").dumps({
                "schema": "cairn-authorization-package/v1",
                "range_report": TestShowReport._minimal_report()}))
            r, _inv = _run_staged(staged, command, values)
            assert r.returncode == 0 and "bootstrap/tests/frozen_0.py" in r.stdout
        else:
            if command == "stage2":
                Path(bed["values"]["package"]).write_text('{"schema": "x"}\n')
            extra = (("--confirm-package-sha256", "abc123")
                     if command == "stage2" else ())
            r, inv = _run_staged(staged, command, values, *extra)
            assert r.returncode == 0, r.stderr
            assert inv["flags"] == {"no_site": 1, "ignore_environment": 1,
                                    "no_user_site": 1}
        assert not marker.exists(), "a .pth file ran in the ceremony's interpreter"


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

    def test_a_stage_given_fewer_than_thirteen_values_names_the_thirteen(
            self, bed, staged):
        values = _values_args(_write_values(bed))
        for stage in ("stage1", "stage2"):
            r, inv = _run_staged(staged, stage, *values[:12])
            _assert_refused(r, "13 recorded values")
            assert inv is None, "the checker ran on an incomplete value list"

    def test_hash_package_takes_exactly_the_thirteen_values(self, bed):
        r = _run("hash-package")
        assert r.returncode != 0
        assert "13 recorded values" in r.stderr


class TestShowReport:
    """A confirmed digest over an unread report authorizes something you have
    not seen. This is the command that makes the report readable."""

    @staticmethod
    def _minimal_report(paths_per_class=3, **over):
        """A report of the current schema, written by hand so a single field can
        be damaged; the real one is exercised through `_real_package`."""
        paths = []
        for cls, stem, role in (("frozen", "bootstrap/tests/frozen_%d.py", "pinned"),
                                ("outside-coverage", "docs/note_%d.md", "other")):
            for i in range(paths_per_class):
                paths.append({"bytes_b64": "", "display": stem % i,
                              "class": cls, "role": role, "change": "modified",
                              "mode": "100644", "scanned": False})
        scan = {"patterns": [n for n, _ in P.SCAN_PATTERNS],
                "counts": {n: 0 for n, _ in P.SCAN_PATTERNS},
                "hits": [], "listed": [], "scanned": [],
                "not_line_scanned": {"frozen": paths_per_class,
                                     "outside-coverage": paths_per_class}}
        report = {
            "schema": P.RANGE_REPORT_SCHEMA,
            "anchor": "a" * 40, "candidate_head": "b" * 40,
            "branch": "master", "expected_old": "c" * 40,
            "manifest_sha256": "d" * 64,
            "paths": paths,
            "counts": {"frozen": paths_per_class,
                       "outside-coverage": paths_per_class},
            "by_role": {"decides": [], "pinned": [p["display"] for p in paths
                                                  if p["role"] == "pinned"],
                        "other": [p["display"] for p in paths
                                  if p["role"] == "other"]},
            "role_counts": {"decides": 0, "pinned": paths_per_class,
                            "other": paths_per_class},
            "scan": scan, "scan_checker": "candidate",
            "signers": {"anchor": ["me@x ssh-ed25519 SHA256:AAA"],
                        "candidate": ["me@x ssh-ed25519 SHA256:AAA"]},
            "signatures": {"total": 3, "unsigned": 0},
        }
        report.update(over)
        return report

    def _package(self, bed, report=None, *, paths_per_class=3):
        pkg = Path(bed["values"]["package"])
        pkg.write_text(__import__("json").dumps({
            "schema": "cairn-authorization-package/v1",
            "range_report": report if report is not None
            else self._minimal_report(paths_per_class),
        }, indent=2))
        return _write_values(bed)

    def _real_package(self, bed, *, plant=True):
        """A package holding a report the real checker derived over a real
        range in the bed's checkout: a planted line, a new script, an
        executable, and a second key added to the roster."""
        import json
        checkout = Path(bed["values"]["checkout"])

        def git(*a):
            return subprocess.run(
                ["git", "-C", str(checkout), "-c", "user.email=t@t",
                 "-c", "user.name=t", "-c", "commit.gpgsign=false", *a],
                check=True, capture_output=True, text=True).stdout.strip()

        anchor = git("rev-parse", "HEAD")
        (checkout / "bootstrap/tests").mkdir(parents=True)
        (checkout / "bootstrap/tests/_oracle.py").write_text(
            "a = 1\n" + ("import subprocess\n" if plant else ""))
        (checkout / "scripts").mkdir()
        (checkout / "scripts/tool.sh").write_text("echo hi\n")
        (checkout / "scripts/tool.sh").chmod(0o755)
        second = Path(bed["dir"]) / "second_key"
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f",
                        str(second), "-C", "other"], check=True,
                       capture_output=True)
        fields = (Path(bed["dir"]) / "second_key.pub").read_text().split()
        roster = checkout / "dev/.cairn/allowed_signers"
        roster.write_text(roster.read_text()
                          + f"other@x {fields[0]} {fields[1]}\n")
        git("add", "-A")
        git("commit", "-qm", "range")
        head = git("rev-parse", "HEAD")
        report = P.range_review_report(
            anchor, head, branch="refs/heads/main", expected_old=head,
            repo=checkout, prospective_manifest=b"{}\n")
        Path(bed["values"]["package"]).write_text(json.dumps(
            {"schema": "cairn-authorization-package/v1", "range_report": report}))
        return _write_values(bed), report

    def test_the_report_renders_what_is_being_authorized(self, bed):
        r = _run("show-report", self._package(bed))
        assert r.returncode == 0, r.stderr
        for expected in ("a" * 40, "b" * 40, "master", "d" * 64,
                         "bootstrap/tests/frozen_0.py", "docs/note_0.md"):
            assert expected in r.stdout, f"{expected!r} missing:\n{r.stdout}"

    def test_the_counts_are_rendered(self, bed):
        r = _run("show-report", self._package(bed))
        assert "frozen" in r.stdout and "outside-coverage" in r.stdout

    def test_no_class_is_cut_however_long(self, bed):
        """Nothing a Maintainer authorizes is hidden behind a count. A cut list
        that does not say it was cut reads as 'that was all of it', and one
        that does say so still hides what it cut."""
        r = _run("show-report", self._package(bed, paths_per_class=120))
        assert r.returncode == 0, r.stderr
        assert "NOT SHOWN" not in r.stdout
        for i in (0, 39, 40, 119):
            assert f"bootstrap/tests/frozen_{i}.py" in r.stdout
            assert f"docs/note_{i}.md" in r.stdout

    def test_roles_modes_and_changes_are_shown_for_every_path(self, bed):
        values, report = self._real_package(bed)
        r = _run("show-report", values)
        assert r.returncode == 0, r.stderr
        assert "decides (2):" in r.stdout   # the oracle module and the roster
        decides_line = next(l for l in r.stdout.splitlines()
                            if l.endswith("bootstrap/tests/_oracle.py"))
        assert "added" in decides_line
        tool_line = next(l for l in r.stdout.splitlines()
                         if l.endswith("scripts/tool.sh"))
        assert "100755" in tool_line

    def test_every_scan_hit_is_shown_with_its_pattern_and_none_is_cut(self, bed):
        hits = [{"path": "bootstrap/tests/_oracle.py", "line": i,
                 "pattern": "process-start", "text": f"import subprocess  # {i}"}
                for i in range(1, 151)]
        report = self._minimal_report()
        report["scan"] = dict(report["scan"], hits=hits)
        r = _run("show-report", self._package(bed, report))
        assert r.returncode == 0, r.stderr
        assert "every scan hit (150)" in r.stdout
        for i in (1, 41, 150):
            assert (f"bootstrap/tests/_oracle.py:{i} [process-start] "
                    f"import subprocess  # {i}") in r.stdout

    def test_listed_blobs_and_unscanned_classes_are_named(self, bed):
        report = self._minimal_report()
        report["scan"] = dict(report["scan"], listed=[
            {"path": "scripts/link.py", "reason": "mode 120000"}])
        r = _run("show-report", self._package(bed, report))
        assert "scripts/link.py  mode 120000" in r.stdout
        assert "not line-scanned: frozen, 3" in r.stdout

    def test_the_page_says_what_the_scan_finds_and_what_it_does_not(self, bed):
        r = _run("show-report", self._package(bed))
        assert "what this finds: an added call, write, command or compiled file" in r.stdout
        assert "what it does not: a harmful change that matches no pattern, or a check that was removed." in " ".join(
            r.stdout.split())

    def test_the_package_digest_and_candidate_id_are_printed(self, bed):
        import hashlib
        values = self._package(bed)
        r = _run("show-report", values)
        digest = hashlib.sha256(Path(bed["values"]["package"]).read_bytes()
                                ).hexdigest()
        assert f"package sha256   {digest}" in r.stdout
        assert f"candidate id     {'b' * 40}" in r.stdout

    def test_every_roster_fingerprint_is_listed_and_a_change_is_flagged(self, bed):
        values, report = self._real_package(bed)
        r = _run("show-report", values)
        assert "ROSTER CHANGED" in r.stdout
        for line in report["signers"]["candidate"]:
            assert line in r.stdout
        added = [l for l in r.stdout.splitlines() if l.startswith("      added ")]
        assert len(added) == 1 and "other@x" in added[0]
        same = _run("show-report", self._package(bed))
        assert "roster unchanged" in same.stdout and "ROSTER CHANGED" not in same.stdout

    def test_each_tool_path_in_the_values_file_is_printed(self, bed):
        r = _run("show-report", self._package(bed))
        for tool in EXECUTABLE_KEYS:
            line = next((l for l in r.stdout.splitlines()
                         if l.split()[:1] == [tool]), None)
            assert line is not None, f"{tool} is not listed:\n{r.stdout}"
            assert line.split()[1] == bed["values"][tool], line

    def test_the_scan_digest_is_the_checkers_digest_of_the_reports_scan(self, bed):
        values, report = self._real_package(bed)
        r = _run("show-report", values)
        assert f"scan digest      {P.scan_digest(report['scan'])}" in r.stdout

    def test_a_scan_not_made_by_the_anchors_checker_is_not_computed(self, bed):
        r = _run("show-report", self._package(bed))
        line = next(l for l in r.stdout.splitlines() if "anchored scan" in l)
        assert "not computed" in line and "equal" not in line

    def test_a_report_that_does_not_say_who_scanned_is_not_computed(self, bed):
        report = self._minimal_report()
        del report["scan_checker"]
        r = _run("show-report", self._package(bed, report))
        assert r.returncode == 0, r.stderr
        line = next(l for l in r.stdout.splitlines() if "anchored scan" in l)
        assert "not computed" in line and "equal" not in line

    def test_a_scan_made_by_the_anchors_checker_says_so(self, bed):
        report = self._minimal_report(scan_checker="anchor")
        r = _run("show-report", self._package(bed, report))
        line = next(l for l in r.stdout.splitlines() if "anchored scan" in l)
        assert "SAYS the anchor" in line and "only your E7 command tests that" in line
        assert "E7 binds this digest, not the hits listed above" in line
        assert "not computed" not in line and "equal" not in line

    @pytest.mark.parametrize("n", (1, 2, 3, 4, 5))
    def test_each_question_is_a_numbered_yes_no_line(self, bed, n):
        r = _run("show-report", self._package(bed))
        assert any(l.startswith(f"  Y{n}  [yes/no]") for l in r.stdout.splitlines()), (
            r.stdout[-900:])

    @pytest.mark.parametrize("where", ("hit text", "path", "signer"))
    def test_unprintable_text_is_refused_and_nothing_is_shown(self, bed, where):
        report = self._minimal_report()
        if where == "hit text":
            report["scan"] = dict(report["scan"], hits=[
                {"path": "a.py", "line": 1, "pattern": "nosec",
                 "text": "x \x1b[31m red"}])
        elif where == "path":
            report["paths"][0]["display"] = "docs/\u202egnp.md"
        else:
            report["signers"]["candidate"] = ["me@x \x07 ssh-ed25519 SHA256:A"]
        r = _run("show-report", self._package(bed, report))
        assert r.returncode != 0
        assert "unprintable" in r.stderr
        assert r.stdout == "", "part of a refused report was shown"

    @staticmethod
    def _every_field_report():
        """A report with every kind of field filled in, so that each place the page could print
        candidate text holds some."""
        report = TestShowReport._minimal_report()
        report["paths"].append({"bytes_b64": "", "display": "bootstrap/tests/_oracle.py",
                                "class": "frozen", "role": "decides", "change": "added",
                                "mode": "100755", "scanned": True})
        report["role_counts"]["decides"] = 1
        report["counts"]["frozen"] += 1
        report["scan"] = dict(
            report["scan"], scanned=["bootstrap/tests/_oracle.py"],
            hits=[{"path": "bootstrap/tests/_oracle.py", "line": 7, "pattern": "nosec", "text": "x  # nosec"}],
            listed=[{"path": "scripts/link.py", "reason": "mode 120000"}])
        report["signers"] = {"anchor": ["me@x ssh-ed25519 SHA256:AAA", "old@x ssh-ed25519 SHA256:OLD"],
                             "candidate": ["me@x ssh-ed25519 SHA256:AAA", "new@x ssh-ed25519 SHA256:NEW"]}
        report["signatures"] = {"total": 3, "unsigned": 0, "bad": 1}
        return report

    @staticmethod
    def _positions(node, where=()):
        """Every place in a JSON value that holds a string or a number, as ("value", path); and every
        dictionary key, as ("key", path to the key)."""
        if isinstance(node, dict):
            for k, v in node.items():
                yield ("key", where + (k,))
                yield from TestShowReport._positions(v, where + (k,))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                yield from TestShowReport._positions(v, where + (i,))
        else:
            yield ("value", where)

    def test_no_field_of_the_report_can_put_unprintable_text_on_the_page(self, bed):
        """The page is what he reads before signing, and every field of the report is candidate
        bytes.  Whichever field carries an escape byte or a bidirectional override, the page
        refuses whole or never shows it; a field that prints raw would let a report redraw
        what he sees."""
        import copy
        hostile = "\x1b[31m\u202e"
        base = self._every_field_report()
        control = _run("show-report", self._package(bed, copy.deepcopy(base)))
        assert control.returncode == 0, control.stderr
        positions = list(self._positions(base))
        assert len(positions) > 100, "the report is too thin to cover every field"
        shown, refused = 0, 0
        for kind, where in positions:
            report = copy.deepcopy(base)
            holder = report
            for step in where[:-1]:
                holder = holder[step]
            if kind == "value":
                holder[where[-1]] = hostile
            else:
                holder[hostile] = holder.pop(where[-1])
            r = _run("show-report", self._package(bed, report))
            assert "\x1b" not in r.stdout + r.stderr and "\u202e" not in r.stdout + r.stderr, (
                kind, where, r.stdout)
            assert r.returncode == 0 or r.stdout == "", (kind, where, r.stdout)
            refused += r.returncode != 0
            shown += r.returncode == 0
        assert refused > 40 and shown > 0, (refused, shown)
        # a roster line both rosters share is printed on its own, not as an addition or a removal
        for name in ("anchor", "candidate"):
            base["signers"][name][0] = hostile
        r = _run("show-report", self._package(bed, base))
        assert r.returncode != 0 and r.stdout == "" and "\x1b" not in r.stderr
        # the eight tool paths come from the values file, not from the report: a real executable
        # whose folder name holds an escape byte is a path the launcher accepts and the page must not show
        folder = Path(bed["dir"]) / "bin\x1b[31m"
        folder.mkdir()
        wrapper = folder / "tool"
        wrapper.write_text(f'#!/bin/sh\nexec {sys.executable} "$@"\n')
        wrapper.chmod(0o755)
        for tool in EXECUTABLE_KEYS:
            self._package(bed, copy.deepcopy(self._every_field_report()))
            r = _run("show-report", _write_values(bed, override={tool: str(wrapper)}))
            assert r.returncode != 0 and r.stdout == "" and "unprintable" in r.stderr, (tool, r.stderr)

    def test_a_changed_path_with_a_role_the_page_does_not_list_is_refused_not_hidden(self, bed):
        report = self._every_field_report()
        report["paths"][0]["role"] = "elsewhere"
        r = _run("show-report", self._package(bed, report))
        assert r.returncode != 0 and "would not be shown" in r.stderr and r.stdout == ""

    def test_a_count_that_is_not_a_number_is_refused_by_name(self, bed):
        report = self._every_field_report()
        report["scan"]["counts"]["nosec"] = "7"
        r = _run("show-report", self._package(bed, report))
        assert r.returncode != 0 and "is not a count" in r.stderr and r.stdout == ""

    def test_a_report_of_another_schema_is_refused(self, bed):
        report = self._minimal_report(schema="cairn-range-review/v1")
        r = _run("show-report", self._package(bed, report))
        assert r.returncode != 0 and "cairn-range-review/v2" in r.stderr
        assert r.stdout == ""

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
                       "stage2", "steps", "step-ids")

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


# --------------------------------------------------------------------------
# the launcher: the packet, the closure, and what must not start
# --------------------------------------------------------------------------

_LAUNCHER_TEMPLATE = _REPO / "bootstrap/reanchor-launcher.template.sh"

#: The authority-closure members, in LC_ALL=C order. Retyped rather than
#: imported so the launcher, the runbook and the checker are three independent
#: statements of one set: importing would make this test agree with whatever
#: the code says, which is not a check.
CLOSURE = (
    "bootstrap/REANCHOR_RUNBOOK.md",
    "bootstrap/reanchor-launcher.template.sh",
    "bootstrap/reanchor.sh",
    "bootstrap/tests/_gate_manifest.py",
    "bootstrap/tests/_gate_preflight.py",
    "bootstrap/tests/_gate_reanchor.py",
    "bootstrap/tests/_gate_transition.py",
    "bootstrap/tests/_oracle.py",
    "bootstrap/tests/_oracle_activation.py",
    "bootstrap/tests/_oracle_trust.py",
    "dev/.cairn/allowed_signers",
)

#: THE MARKER INTERPRETER. The candidate's `reanchor.sh` writes a file and
#: stops. Its existence is the *only* evidence that candidate code ran -- an
#: absent traceback is not evidence, because a refusal and a crash both produce
#: one. Every refusal node below asserts the marker is ABSENT.
_MARKER_ARTIFACT = '''\
#!/bin/sh
# The first candidate byte that would execute. It records that it did.
printf 'candidate code ran\\n' > "@MARKER@"
'''


def _sha256_file(path) -> str:
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@pytest.fixture
def ceremony(bed, tmp_path):
    """A complete launcher bed: a candidate repository carrying every closure
    member, a packet composed over them, and a launcher instantiated with that
    packet's digest -- exactly the pair the review delivers."""
    repo = Path(bed["values"]["checkout"])
    marker = tmp_path / "CANDIDATE-CODE-RAN"

    for rel in CLOSURE:
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if rel == "bootstrap/reanchor.sh":
            p.write_text(_MARKER_ARTIFACT.replace("@MARKER@", str(marker)))
        else:
            p.write_text(f"stub for {rel}\n")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "-c", "user.email=t@t",
                    "-c", "user.name=t", "commit", "-qm", "candidate"],
                   check=True, capture_output=True)
    oid = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                         capture_output=True, text=True,
                         check=True).stdout.strip()

    state = {"repo": repo, "oid": oid, "marker": marker, "dir": tmp_path,
             "bed": bed}
    state["packet_path"] = tmp_path / "packet.txt"
    state["launcher"] = tmp_path / "launcher.sh"
    _instantiate(state, _compose_packet(state))
    return state


def _compose_packet(state, *, rows=None, artifact_rel="bootstrap/reanchor.sh",
                    artifact_sha=None, extra=(), schema=None,
                    provenance="builder and reader, test fixture"):
    repo = state["repo"]
    if rows is None:
        rows = [(_sha256_file(repo / rel), rel) for rel in CLOSURE]
    if artifact_sha is None:
        artifact_sha = _sha256_file(repo / "bootstrap/reanchor.sh")
    lines = [f"schema {schema or 'cairn-authorization-packet/v1'}",
             f"provenance {provenance}",
             f"artifact {artifact_rel}",
             f"artifact_sha256 {artifact_sha}"]
    lines += [f"member {sha} {rel}" for sha, rel in rows]
    lines += list(extra)
    return "\n".join(lines) + "\n"


def _instantiate(state, packet_text, *, packet_bytes=None, digest=None):
    """Write the packet and the launcher instantiated with its digest.

    This models what the review does: it reviews the launcher's text and the
    packet's bytes together, and the digest it fills is the one it reviewed.
    """
    import hashlib
    body = packet_bytes if packet_bytes is not None else packet_text.encode()
    Path(state["packet_path"]).write_bytes(body)
    if digest is None:
        digest = hashlib.sha256(body).hexdigest()
    template = _LAUNCHER_TEMPLATE.read_text(encoding="utf-8")
    assert template.count("@PACKET_SHA256@") == 1, (
        "the template must carry exactly ONE slot; reviewed bytes stay "
        "constant and late-bound values arrive as arguments")
    Path(state["launcher"]).write_text(
        template.replace("@PACKET_SHA256@", digest), encoding="utf-8")
    return digest


def _launch(state, *, ref=None, values=None, packet=None, mode=(), env=None,
            cwd=None):
    """The launcher, as the Maintainer runs it. `mode` is the optional fourth
    argument(s): `("--stage2", digest)`, `("--show-report",)`, and so on."""
    return subprocess.run(
        ["/bin/sh", str(state["launcher"]),
         str(packet or state["packet_path"]),
         values or _write_values(state["bed"]),
         ref or state["oid"], *mode],
        capture_output=True, text=True, check=False, env=env, cwd=cwd)


def _assert_no_candidate_code_ran(state, r, needle):
    assert r.returncode != 0, f"expected a refusal:\n{r.stdout}\n{r.stderr}"
    assert needle in r.stderr, f"refusal does not name {needle!r}:\n{r.stderr}"
    assert not state["marker"].exists(), (
        "CANDIDATE CODE RAN despite the refusal. The marker interpreter is "
        "the only evidence that matters here: an absent traceback proves "
        "nothing, because a refusal and a crash both produce one")


class TestTheLauncherRunsTheWholeCeremonyFromOneCommand:

    def test_the_happy_path_reaches_candidate_code(self, ceremony):
        """Every refusal node below is meaningless unless the clean path
        actually starts the artifact."""
        r = _launch(ceremony)
        assert r.returncode == 0, f"{r.stdout}\n{r.stderr}"
        assert ceremony["marker"].exists(), (
            "the clean path never reached the artifact, so every 'no candidate "
            "code ran' assertion below is vacuous")
        assert ceremony["oid"] in r.stdout

    def test_the_template_itself_refuses_unfilled(self, ceremony):
        """An unfilled template is not an operative launcher. The placeholder
        is not 64 hex characters, so the comparison cannot pass by accident."""
        raw = ceremony["dir"] / "raw-template.sh"
        raw.write_text(_LAUNCHER_TEMPLATE.read_text(encoding="utf-8"))
        r = subprocess.run(
            ["/bin/sh", str(raw), str(ceremony["packet_path"]),
             _write_values(ceremony["bed"]), ceremony["oid"]],
            capture_output=True, text=True, check=False)
        _assert_no_candidate_code_ran(ceremony, r, "UNFILLED TEMPLATE")

    def test_the_launcher_carries_no_candidate_oid(self):
        """Reviewed bytes stay constant; late-bound values arrive as arguments.
        A candidate OID literal would change the reviewed bytes every ceremony,
        and the review would be of something nobody ran."""
        text = _LAUNCHER_TEMPLATE.read_text(encoding="utf-8")
        import re as _re
        assert not _re.search(r"\b[0-9a-f]{40}\b", text), (
            "the launcher template carries something shaped like an OID")

    def test_the_launcher_passes_a_shell_syntax_check(self):
        r = subprocess.run(["/bin/sh", "-n", str(_LAUNCHER_TEMPLATE)],
                           capture_output=True, text=True, check=False)
        assert r.returncode == 0, r.stderr


class TestThePacketIsBoundIntoTheLauncher:

    def test_a_consistently_rewritten_packet_refuses(self, ceremony):
        """The attack the binding exists to stop, run rather than argued.

        Every row is rewritten to a self-consistent set: the digests match
        files that really exist, the paths are the real closure, the schema is
        right. Nothing INSIDE the packet is wrong. Only the launcher's embedded
        digest catches it -- which is the entire point of binding the two.
        """
        forged = ceremony["dir"] / "forged"
        forged.mkdir()
        rows = []
        for rel in CLOSURE:
            f = forged / rel.replace("/", "_")
            f.write_text(f"substituted bytes for {rel}\n")
            rows.append((_sha256_file(f), rel))
        Path(ceremony["packet_path"]).write_text(
            _compose_packet(ceremony, rows=rows))
        r = _launch(ceremony)
        _assert_no_candidate_code_ran(ceremony, r, "bound into this launcher")

    def test_a_single_flipped_byte_refuses(self, ceremony):
        body = Path(ceremony["packet_path"]).read_bytes()
        Path(ceremony["packet_path"]).write_bytes(
            body.replace(b"provenance ", b"provenance!", 1))
        r = _launch(ceremony)
        _assert_no_candidate_code_ran(ceremony, r, "bound into this launcher")

    def test_a_symlinked_packet_refuses(self, ceremony):
        real = ceremony["packet_path"]
        link = ceremony["dir"] / "packet-link.txt"
        link.symlink_to(real)
        r = _launch(ceremony, packet=link)
        _assert_no_candidate_code_ran(ceremony, r, "symbolic link")

    def test_a_missing_packet_refuses(self, ceremony):
        r = _launch(ceremony, packet=ceremony["dir"] / "no-such-packet.txt")
        _assert_no_candidate_code_ran(ceremony, r, "does not exist")


class TestHashedBytesAreParsedBytes:
    """What is verified and what is parsed must be the same bytes, or the
    verification describes a file that no longer exists by the time it matters.

    Step 3 -- re-hashing the in-memory snapshot -- is what makes the design
    work, and these are the nodes that attack it directly rather than through
    an abstract helper.
    """

    def test_a_trailing_newline_survives_the_snapshot(self, ceremony):
        """`$(...)` strips every trailing newline. Without the sentinel idiom
        the snapshot's digest would differ from the file's on a packet ending
        in a blank line, and a correct ceremony would refuse."""
        text = _compose_packet(ceremony) + "\n\n"
        _instantiate(ceremony, text)
        r = _launch(ceremony)
        assert r.returncode == 0, (
            f"a packet with trailing newlines was refused, so the "
            f"trailing-byte-preserving idiom is not working:\n{r.stderr}")
        assert ceremony["marker"].exists()

    def test_an_embedded_NUL_refuses_at_the_snapshot_comparison(self, ceremony):
        """A shell variable cannot carry a NUL, so the snapshot would be a
        SHORTER string that parsed cleanly. Step 3 is what detects it: the
        packet format is NUL-free by definition, and this is the enforcement."""
        body = _compose_packet(ceremony).encode()
        body = body.replace(b"provenance ", b"provenance\x00", 1)
        _instantiate(ceremony, "", packet_bytes=body)
        r = _launch(ceremony)
        _assert_no_candidate_code_ran(ceremony, r, "in memory")

    def test_a_packet_rewritten_between_the_two_reads_refuses(self, ceremony):
        """The same-user residual, measured rather than assumed. Steps 1 and 2
        read the file twice, so a writer can change it in between; step 3
        DETECTS that. It does not prevent it, and the launcher says so."""
        good = _compose_packet(ceremony)
        digest = _instantiate(ceremony, good)
        # Swap `cat` for one that returns different bytes than `shasum` saw.
        liar = ceremony["dir"] / "lying-cat"
        other = ceremony["dir"] / "other-packet.txt"
        other.write_text(good.replace("test fixture", "swapped mid-read"))
        liar.write_text(f'#!/bin/sh\nexec /bin/cat {other}\n')
        liar.chmod(0o755)
        values = _write_values(ceremony["bed"],
                               override={"cat": str(liar)}, name="values-liar")
        r = _launch(ceremony, values=values)
        _assert_no_candidate_code_ran(ceremony, r, "in memory")
        assert digest in r.stderr or "differ" in r.stderr


class TestTheClosureIsVerifiedAtTheResolvedOid:

    def test_a_member_that_differs_at_the_candidate_refuses(self, ceremony):
        """The packet says one thing, the candidate holds another. The launcher
        verifies EVERY blob at the OID it resolved, not a sample."""
        rows = [(_sha256_file(ceremony["repo"] / rel), rel) for rel in CLOSURE]
        rows[4] = ("a" * 64, rows[4][1])
        _instantiate(ceremony, _compose_packet(ceremony, rows=rows))
        r = _launch(ceremony)
        _assert_no_candidate_code_ran(ceremony, r, "does not match the reviewed")

    def test_a_launcher_template_that_changed_after_the_packet_refuses_before_candidate_code_runs(
            self, ceremony):
        """The packet was composed over the reviewed template. A candidate
        whose template differs by one byte must be refused through that row,
        before any candidate code can run: the launcher is the template with
        a slot filled, so a changed template is a different launcher."""
        repo = ceremony["repo"]
        template = repo / "bootstrap/reanchor-launcher.template.sh"
        template.write_text(template.read_text() + "#\n")
        subprocess.run(["git", "-C", str(repo), "-c", "user.email=t@t",
                        "-c", "user.name=t", "commit", "-qam",
                        "template changed after the packet"],
                       check=True, capture_output=True)
        changed = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()
        assert changed != ceremony["oid"]
        r = _launch(ceremony, ref=changed)
        _assert_no_candidate_code_ran(
            ceremony, r, "does not match the reviewed")
        assert "reanchor-launcher.template.sh" in r.stderr

    def test_a_dropped_member_refuses_against_the_fixed_set(self, ceremony):
        """Everything the packet says validates it against ITSELF. A packet
        with nine rows parses cleanly and hashes correctly -- it is a
        well-formed packet describing a different closure. Only the launcher's
        own fixed list catches that."""
        rows = [(_sha256_file(ceremony["repo"] / rel), rel)
                for rel in CLOSURE if rel != "bootstrap/tests/_oracle.py"]
        _instantiate(ceremony, _compose_packet(ceremony, rows=rows))
        r = _launch(ceremony)
        _assert_no_candidate_code_ran(ceremony, r, "not the authority closure")

    def test_an_added_member_refuses_against_the_fixed_set(self, ceremony):
        extra = ceremony["repo"] / "bootstrap/tests/_smuggled.py"
        extra.write_text("smuggled\n")
        subprocess.run(["git", "-C", str(ceremony["repo"]), "add", "-A"],
                       check=True, capture_output=True)
        rows = [(_sha256_file(ceremony["repo"] / rel), rel) for rel in CLOSURE]
        rows.append((_sha256_file(extra), "bootstrap/tests/_smuggled.py"))
        rows.sort(key=lambda r: r[1])
        _instantiate(ceremony, _compose_packet(ceremony, rows=rows))
        r = _launch(ceremony)
        _assert_no_candidate_code_ran(ceremony, r, "not the authority closure")

    def test_rows_out_of_order_refuse(self, ceremony):
        """LC_ALL=C order is canonical because it is independently derivable,
        so no hidden list decides what 'correct order' means."""
        rows = [(_sha256_file(ceremony["repo"] / rel), rel) for rel in CLOSURE]
        rows[0], rows[1] = rows[1], rows[0]
        _instantiate(ceremony, _compose_packet(ceremony, rows=rows))
        r = _launch(ceremony)
        _assert_no_candidate_code_ran(ceremony, r, "not the authority closure")

    def test_an_unresolvable_candidate_refuses(self, ceremony):
        r = _launch(ceremony, ref="refs/heads/no-such-branch")
        _assert_no_candidate_code_ran(ceremony, r, "cannot resolve")


class TestTheArtifactIsAClosureMemberByConstruction:
    """Two constraints. The artifact is IN the closure by construction,
    rather than being an executable the packet happens to name alongside it."""

    def test_an_artifact_path_matching_no_row_refuses(self, ceremony):
        _instantiate(ceremony, _compose_packet(
            ceremony, artifact_rel="bootstrap/not_a_member.sh"))
        r = _launch(ceremony)
        _assert_no_candidate_code_ran(ceremony, r, "matches 0 closure rows")

    def test_an_artifact_digest_disagreeing_with_its_row_refuses(self, ceremony):
        _instantiate(ceremony, _compose_packet(ceremony, artifact_sha="b" * 64))
        r = _launch(ceremony)
        _assert_no_candidate_code_ran(ceremony, r, "does not equal its closure")

    def test_an_artifact_row_naming_a_different_member_refuses(self, ceremony):
        """A packet could name a real closure member -- with a real digest --
        that is not the ceremony artifact, and the two constraints alone would
        be satisfied. The launcher starts one file and will not start another.
        """
        other = "bootstrap/tests/_oracle.py"
        _instantiate(ceremony, _compose_packet(
            ceremony, artifact_rel=other,
            artifact_sha=_sha256_file(ceremony["repo"] / other)))
        r = _launch(ceremony)
        _assert_no_candidate_code_ran(ceremony, r, "will not start another")


class TestThePacketCarriesNoAuthorityItShouldNot:

    def test_a_candidate_row_in_the_packet_refuses(self, ceremony):
        """OID-free BY DESIGN -- that is what lets the review produce the
        packet before the candidate commit exists. A packet naming an OID is a
        packet from a different contract."""
        _instantiate(ceremony, _compose_packet(
            ceremony, extra=(f"candidate {ceremony['oid']}",)))
        r = _launch(ceremony)
        _assert_no_candidate_code_ran(ceremony, r, "must carry NO candidate")

    def test_an_unknown_row_type_refuses(self, ceremony):
        _instantiate(ceremony, _compose_packet(
            ceremony, extra=("bless_anyway true",)))
        r = _launch(ceremony)
        _assert_no_candidate_code_ran(ceremony, r, "unknown row type")

    def test_a_wrong_schema_refuses(self, ceremony):
        _instantiate(ceremony, _compose_packet(
            ceremony, schema="cairn-authorization-packet/v2"))
        r = _launch(ceremony)
        _assert_no_candidate_code_ran(ceremony, r, "unknown schema")


class TestTheLauncherReaderRefusesBeforeAnyCandidateByte:
    """The launcher needs git, shasum, cat, mktemp, mkdir and env BEFORE it can
    verify the artifact, and it is the only reader of the values file. These
    nodes prove its reader refuses with the marker still absent."""

    @pytest.mark.parametrize("key", EXECUTABLE_KEYS)
    def test_a_malicious_executable_value_leaves_the_marker_absent(
            self, ceremony, key):
        """Not merely 'refuses' -- refuses BEFORE anything runs. A reader that
        validated after starting the artifact would be describing a boundary
        that had already been crossed."""
        evil = ceremony["dir"] / f"evil-{key}"
        evil.write_text(
            f'#!/bin/sh\nprintf "evil {key} ran\\n" > "{ceremony["marker"]}"\n')
        evil.chmod(0o644)          # present, but NOT executable
        values = _write_values(ceremony["bed"], override={key: str(evil)},
                               name=f"values-{key}")
        r = _launch(ceremony, values=values)
        _assert_no_candidate_code_ran(ceremony, r, "is not executable")

    @pytest.mark.parametrize("key", EXECUTABLE_KEYS)
    def test_an_absent_executable_value_leaves_the_marker_absent(
            self, ceremony, key):
        values = _write_values(
            ceremony["bed"], override={key: str(ceremony["dir"] / "nope")},
            name=f"values-absent-{key}")
        r = _launch(ceremony, values=values)
        _assert_no_candidate_code_ran(ceremony, r, "does not exist")


    def test_a_values_file_that_is_not_a_plain_absolute_regular_file_refuses(self, ceremony):
        """The path to the file the launcher reads is itself checked, before it is read: a link
        could be swapped for another file between the Maintainer's check and the run, and a
        relative path means whatever the working folder makes it."""
        good = Path(_write_values(ceremony["bed"], name="values-plain"))
        real_dir = ceremony["dir"] / "real"
        real_dir.mkdir()
        (real_dir / "values").write_text(good.read_text())
        (ceremony["dir"] / "linkdir").symlink_to(real_dir)
        (ceremony["dir"] / "link-values").symlink_to(good)
        ok = _launch(ceremony, values=str(good))
        assert ok.returncode == 0 and ceremony["marker"].exists(), ok.stderr       # the control
        cases = [("symbolic link", str(ceremony["dir"] / "link-values"), None),
                 ("symbolic link", str(ceremony["dir"] / "linkdir" / "values"), None),
                 ("not an absolute path", good.name, ceremony["dir"]),
                 ("not a regular file", str(real_dir), None),
                 ("does not exist", str(ceremony["dir"] / "nowhere"), None)]
        for needle, values, cwd in cases:
            ceremony["marker"].unlink(missing_ok=True)
            r = _launch(ceremony, values=values, cwd=cwd)
            _assert_no_candidate_code_ran(ceremony, r, needle)
            assert "values file" in r.stderr, (values, r.stderr)


def _logging_tools(bed, log) -> dict:
    """A stand-in for each of the eight programs: it records its own name and
    its arguments, then runs the real program. A program that starts leaves a
    line; one that never starts leaves none."""
    stand_ins = {}
    for key in EXECUTABLE_KEYS:
        stub = Path(bed["dir"]) / f"logging-{key}"
        stub.write_text(
            f'#!/bin/sh\nprintf "%s %s\\n" {key} "$*" >> "{log}"\n'
            f'exec "{bed["values"][key]}" "$@"\n')
        stub.chmod(0o755)
        stand_ins[key] = str(stub)
    return stand_ins


def _logged_programs(log) -> list[str]:
    return ([ln.split(" ", 1)[0] for ln in Path(log).read_text().splitlines()]
            if Path(log).exists() else [])


class TestHostileValuesStartNoProgram:
    """Every hostile values file is refused by the real launcher before ANY of
    the programs the file names has started. Each of the eight stand-ins logs a
    call; a refusal that came after one of them ran would show in the log."""

    #: One damaged file per rule, over every key it applies to.
    @staticmethod
    def _hostile(bed, tools):
        cases = []
        for key in SCHEMA_KEYS:
            cases.append((f"missing {key}", {"drop": (key,)}))
            value = tools.get(key, bed["values"][key])
            cases.append((f"duplicate {key}",
                          {"extra_lines": (f"{key} {value}",)}))
        for key in EXECUTABLE_KEYS:
            plain = Path(bed["dir"]) / f"plain-{key}"
            plain.write_text("#!/bin/sh\n")
            plain.chmod(0o644)
            cases += [(f"not executable {key}", {"override": {key: str(plain)}}),
                      (f"absent {key}", {"override": {
                          key: str(Path(bed["dir"]) / "nope")}}),
                      (f"directory {key}", {"override": {
                          key: str(bed["dir"])}})]
        cases += [
            ("unknown key", {"extra_lines": ("candidate_oid deadbeef",)}),
            ("no value", {"extra_lines": ("git",)}),
            ("leading whitespace", {"extra_lines": (" home /tmp",)}),
            ("control character", {"extra_lines": ("home /tmp\tx",)}),
            ("over long", {"extra_lines": ("home /" + "a" * 5000,)}),
            ("wrong schema", {"override": {
                "schema": "cairn-ceremony-values/v2"}}),
            ("package parent missing", {"override": {
                "package": str(Path(bed["dir"]) / "nodir" / "p.json")}}),
            ("not a worktree top level", {"override": {
                "checkout": str(Path(bed["values"]["checkout"]) / "sub")}}),
        ]
        (Path(bed["values"]["checkout"]) / "sub").mkdir(exist_ok=True)
        return cases

    def test_a_refusal_comes_before_any_program_starts(self, ceremony):
        log = ceremony["dir"] / "programs.log"
        tools = _logging_tools(ceremony["bed"], log)
        clean = _launch(ceremony, values=_write_values(
            ceremony["bed"], override=tools, name="values-clean"))
        assert clean.returncode == 0 and ceremony["marker"].exists(), (
            f"the clean file did not reach the artifact:\n{clean.stderr}")
        assert _logged_programs(log), (
            "the stand-ins logged nothing on the clean path, so an empty log "
            "below would prove nothing")
        ceremony["marker"].unlink()
        failures = []
        for label, kwargs in self._hostile(ceremony["bed"], tools):
            log.unlink(missing_ok=True)
            kwargs = dict(kwargs)
            kwargs["override"] = {**tools, **kwargs.get("override", {})}
            r = _launch(ceremony, values=_write_values(
                ceremony["bed"], name="values-hostile", **kwargs))
            if (r.returncode == 0 or _logged_programs(log)
                    or ceremony["marker"].exists()):
                failures.append((label, r.returncode, _logged_programs(log)))
        assert not failures, failures


class TestTheLauncherStartsSixProgramsAndNoMore:
    """`bootstrap/SAFETY.md` fixes the programs that run before the first
    candidate byte at six: env, git, shasum, mktemp, mkdir, cat. The values file
    now names eight, and the launcher is its only reader, so the two it reads
    for the artifact alone -- python and sort -- must never start here."""

    SIX = {"env", "git", "shasum", "mktemp", "mkdir", "cat"}

    @pytest.mark.parametrize("mode", [(), ("--validate",), ("--show-report",),
                                      ("--hash-package",)])
    def test_only_the_six_start_before_the_artifact(self, ceremony, mode):
        log = ceremony["dir"] / "programs.log"
        tools = _logging_tools(ceremony["bed"], log)
        values = _write_values(ceremony["bed"], override=tools)
        # A PATH that finds nothing: a program reached by bare name fails.
        r = _launch(ceremony, values=values, mode=mode,
                    env={"PATH": str(ceremony["dir"] / "no-such-bin")})
        assert r.returncode == 0 and ceremony["marker"].exists(), (
            f"the artifact was not reached:\n{r.stderr}")
        assert set(_logged_programs(log)) == self.SIX

    def test_a_trace_of_the_launcher_names_no_other_program(self, ceremony):
        """The log above sees only the eight values-file programs. A seventh
        reached by bare name (`date`, `sed`, `cut`) would leave no line there
        and, with an empty PATH, would fail without stopping the launcher. The
        shell's own trace lists every command it runs, so this reads that."""
        import re
        log = ceremony["dir"] / "programs.log"
        tools = _logging_tools(ceremony["bed"], log)
        values = _write_values(ceremony["bed"], override=tools)
        r = subprocess.run(
            ["/bin/sh", "-x", str(ceremony["launcher"]),
             str(ceremony["packet_path"]), values, ceremony["oid"]],
            capture_output=True, text=True, check=False,
            env={"PATH": str(ceremony["dir"] / "no-such-bin")})
        assert r.returncode == 0 and ceremony["marker"].exists(), r.stderr[-800:]
        source = _LAUNCHER_TEMPLATE.read_text(encoding="utf-8")
        functions = set(re.findall(r"^(\w+)\(\) \{", source, re.M))
        shell_words = {":", "[", "break", "case", "cd", "continue", "exec",
                       "exit", "export", "printf", "pwd", "read", "return",
                       "set", "shift", "unset"}
        programs = set()
        for line in r.stderr.splitlines():
            found = re.match(r"^\++ (\S+)", line)
            if not found:
                continue
            word = found.group(1).strip("'\"")
            if (re.match(r"[A-Za-z_][A-Za-z0-9_]*=", word)
                    or word in shell_words or word in functions):
                continue
            programs.add(word)
        # `git` is an argument of `env -i ...`, so the trace shows `env` start it.
        assert programs == {tools[k] for k in self.SIX - {"git"}}, sorted(programs)
        assert "git" in _logged_programs(log)

    def test_the_second_stage_starts_the_same_six(self, ceremony):
        log = ceremony["dir"] / "programs.log"
        tools = _logging_tools(ceremony["bed"], log)
        values = _write_values(ceremony["bed"], override=tools)
        r = _launch(ceremony, values=values, mode=("--stage2", "0" * 64),
                    env={"PATH": str(ceremony["dir"] / "no-such-bin")})
        assert r.returncode == 0 and ceremony["marker"].exists(), r.stderr
        assert set(_logged_programs(log)) == self.SIX


def _use_the_real_artifact(state, *, also=None):
    """Replace the stub artifact in the candidate with the shipped one (and
    any other candidate file in *also*), and re-issue the packet and launcher
    over it."""
    repo = state["repo"]
    (repo / "bootstrap/reanchor.sh").write_bytes(_ARTIFACT.read_bytes())
    for rel, text in (also or {}).items():
        (repo / rel).write_text(text)
    for args in (["add", "-A"],
                 ["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm",
                  "real artifact"]):
        subprocess.run(["git", "-C", str(repo), *args], check=True,
                       capture_output=True)
    state["oid"] = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True,
        text=True, check=True).stdout.strip()
    _instantiate(state, _compose_packet(state))
    return state


class TestTheReadingCommandsRunThroughTheLauncher:
    """`validate`, `show-report` and `hash-package` start the artifact only
    after the launcher has verified it, and hand it the values already checked."""

    def test_validate_prints_the_configuration_the_launcher_read(self, ceremony):
        _use_the_real_artifact(ceremony)
        r = _launch(ceremony, mode=("--validate",))
        assert r.returncode == 0, r.stderr
        assert "OK: the values satisfy the closed schema" in r.stdout
        for key, value in ceremony["bed"]["values"].items():
            assert value in r.stdout, f"{key} not shown"

    def test_hash_package_hashes_with_the_launchers_own_shasum(self, ceremony):
        import hashlib
        _use_the_real_artifact(ceremony)
        log = ceremony["dir"] / "programs.log"
        tools = _logging_tools(ceremony["bed"], log)
        package = Path(ceremony["bed"]["values"]["package"])
        payload = b'{"schema": "cairn-authorization-package/v1"}\n'
        package.write_bytes(payload)
        r = _launch(ceremony, mode=("--hash-package",), values=_write_values(
            ceremony["bed"], override=tools))
        assert r.returncode == 0, r.stderr
        assert hashlib.sha256(payload).hexdigest() in r.stdout
        assert f"shasum -a 256 {package}" in log.read_text().splitlines()

    @pytest.mark.parametrize("steady", [False, True])
    def test_the_stages_receive_the_values_the_launcher_read(
            self, ceremony, steady):
        """Both the transition path (the closure differs from the anchor) and
        the steady-state path start the artifact with the thirteen values."""
        import json
        repo = ceremony["repo"]
        record = ceremony["dir"] / "invocation.json"
        roster = subprocess.run(
            ["git", "-C", str(repo), "show",
             "refs/cairn/gate-anchor:dev/.cairn/allowed_signers"],
            capture_output=True, text=True, check=True).stdout
        _use_the_real_artifact(ceremony, also={
            "dev/.cairn/allowed_signers": roster,
            "bootstrap/tests/_gate_preflight.py":
                _RECORDING_CHECKER.replace("@RECORD@", str(record))})
        if steady:
            subprocess.run(["git", "-C", str(repo), "update-ref",
                            "refs/cairn/gate-anchor", ceremony["oid"]],
                           check=True, capture_output=True)
        values = ceremony["bed"]["values"]
        stage1 = _launch(ceremony)
        assert stage1.returncode == 0, stage1.stderr
        assert ("steady state" in stage1.stdout) == steady, stage1.stdout
        argv = json.loads(record.read_text())["argv"]
        assert argv[0] == "stage1"
        assert argv[argv.index("--repo") + 1] == values["checkout"]
        assert argv[argv.index("--package-out") + 1] == values["package"]
        assert argv[argv.index("--signing-key") + 1] == values["signing_key"]
        assert ("--reviewed-candidate" in argv) == (not steady)
        record.unlink()
        Path(values["package"]).write_text("{}\n")
        stage2 = _launch(ceremony, mode=("--stage2", "ab" * 32))
        assert stage2.returncode == 0, stage2.stderr
        argv = json.loads(record.read_text())["argv"]
        assert argv[0] == "stage2"
        assert argv[argv.index("--package") + 1] == values["package"]
        assert argv[argv.index("--confirm-package-sha256") + 1] == "ab" * 32

    def test_show_report_renders_through_the_launcher(self, ceremony):
        import json
        _use_the_real_artifact(ceremony)
        Path(ceremony["bed"]["values"]["package"]).write_text(json.dumps({
            "schema": "cairn-authorization-package/v1",
            "range_report": TestShowReport._minimal_report()}))
        r = _launch(ceremony, mode=("--show-report",))
        assert r.returncode == 0, r.stderr
        assert "bootstrap/tests/frozen_0.py" in r.stdout

    @pytest.mark.parametrize("mode", ["--validate", "--show-report",
                                      "--hash-package"])
    def test_a_packet_that_does_not_match_refuses_before_the_artifact(
            self, ceremony, mode):
        rows = [(_sha256_file(ceremony["repo"] / rel), rel) for rel in CLOSURE]
        rows[2] = ("a" * 64, rows[2][1])
        _instantiate(ceremony, _compose_packet(
            ceremony, rows=rows, artifact_sha="a" * 64))
        r = _launch(ceremony, mode=(mode,))
        _assert_no_candidate_code_ran(ceremony, r, "does not match the reviewed")

    def test_an_unknown_fourth_argument_is_a_usage_error(self, ceremony):
        r = _launch(ceremony, mode=("--bless-everything",))
        assert r.returncode == 2 and "usage:" in r.stderr
        assert not ceremony["marker"].exists()


def _git_out(repo, *args, env=None, data=None) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, input=data,
                          env=env).stdout.decode("utf-8", errors="replace")


def _move_the_anchor_onto(state, files: dict) -> str:
    """A new anchor commit holding *files* (path -> text) beside everything
    the old anchor held, made with plumbing only: the worktree, the index and
    the candidate commit are untouched.  Returns the new anchor's id."""
    repo = state["repo"]
    old = _git_out(repo, "rev-parse", "refs/cairn/gate-anchor").strip()
    index = str(Path(state["dir"]) / "scratch-index")
    env = {**os.environ, "GIT_INDEX_FILE": index}
    _git_out(repo, "read-tree", old, env=env)
    for rel, text in files.items():
        blob = _git_out(repo, "hash-object", "-w", "--stdin", data=text.encode()
                        if isinstance(text, str) else text).strip()
        mode = "100755" if rel.endswith(".sh") else "100644"
        _git_out(repo, "update-index", "--add", "--cacheinfo",
                 f"{mode},{blob},{rel}", env=env)
    tree = _git_out(repo, "write-tree", env=env).strip()
    new = _git_out(repo, "-c", "user.email=t@t", "-c", "user.name=t",
                   "commit-tree", tree, "-p", old, "-m", "the anchor").strip()
    _git_out(repo, "update-ref", "refs/cairn/gate-anchor", new)
    return new


#: Stands in for the anchor's checker: prints what it was asked and which
#: interpreter flags it ran under, so a test sees which bytes ran and how.
_ANCHOR_CHECKER = (
    "import sys, hashlib\n"
    "print('ANCHOR-CHECKER', 'no_site=%d' % sys.flags.no_site, "
    "'isolated=%d' % sys.flags.ignore_environment, *sys.argv[1:])\n")
_CHECKER_PATH = "bootstrap/tests/_gate_preflight.py"


def _interpreter_with_a_planted_pth_file(tmp_path):
    """The copy above with a `.pth` file planted in its packages folder.
    Returns (binary, marker): the marker file appears when the interpreter reads
    the `.pth` file, and the control inside shows that it does under `-E -s`
    alone."""
    binary, packages = a_copy_of_this_interpreter(tmp_path)
    marker = tmp_path / "pth-ran"
    (packages / "planted.pth").write_text(
        f"import pathlib; pathlib.Path({str(marker)!r}).write_text('ran')\n")
    subprocess.run([str(binary), "-E", "-s", "-c", "pass"], env={},
                   capture_output=True)
    assert marker.exists(), (
        "the control: under -E -s alone the planted .pth file runs")
    marker.unlink()
    return binary, marker


class TestTheAnchorsOwnScanRunsBeforeAnyCandidateByte:
    """`--scan-digest` runs the checker the anchor holds.  The anchor's files
    are read as raw objects, so nothing the candidate repository carries in its
    own `.git` folder (a replace entry, an attributes file with a filter, a
    configuration key) can change the bytes that run, and the interpreter is
    told to read no environment, no user site and no `site` module."""

    @staticmethod
    def _scan(ceremony, files=None, *, values=None, env=None):
        _move_the_anchor_onto(ceremony, {_CHECKER_PATH: _ANCHOR_CHECKER,
                                         **(files or {})})
        return _launch(ceremony, mode=("--scan-digest",), values=values,
                       env=env)

    def test_the_anchors_checker_runs_over_the_resolved_range(self, ceremony):
        r = self._scan(ceremony)
        anchor = _git_out(ceremony["repo"], "rev-parse",
                          "refs/cairn/gate-anchor").strip()
        assert r.returncode == 0, r.stderr
        assert r.stdout.splitlines()[-1] == (
            f"ANCHOR-CHECKER no_site=1 isolated=1 scan-digest --repo "
            f"{ceremony['bed']['values']['checkout']} --anchor {anchor} "
            f"--candidate {ceremony['oid']}")
        assert not ceremony["marker"].exists(), "the candidate's artifact ran"

    def test_the_candidates_own_checker_is_never_the_one_that_runs(self, ceremony):
        """The candidate's copy is a stub that is not even Python; had it run,
        the mode would have failed instead of printing the anchor's line."""
        assert _git_out(ceremony["repo"], "show",
                        f"{ceremony['oid']}:{_CHECKER_PATH}").startswith("stub")
        assert "ANCHOR-CHECKER" in self._scan(ceremony).stdout

    def test_a_replace_entry_cannot_swap_the_anchors_checker(self, ceremony):
        repo = ceremony["repo"]
        self._scan(ceremony)
        anchor_blob = _git_out(repo, "rev-parse",
                               f"refs/cairn/gate-anchor:{_CHECKER_PATH}").strip()
        evil = _git_out(repo, "hash-object", "-w", "--stdin",
                        data=b"print('REPLACED-CHECKER')\n").strip()
        _git_out(repo, "replace", anchor_blob, evil)
        control = _git_out(repo, "cat-file", "blob",
                           f"refs/cairn/gate-anchor:{_CHECKER_PATH}")
        assert "REPLACED-CHECKER" in control, (
            "the control: plain git does return the substitute")
        r = _launch(ceremony, mode=("--scan-digest",))
        assert r.returncode == 0, r.stderr
        assert "REPLACED-CHECKER" not in r.stdout and "ANCHOR-CHECKER" in r.stdout

    def test_a_filter_in_the_repository_cannot_rewrite_the_anchors_checker(
            self, ceremony):
        repo = ceremony["repo"]
        marker = ceremony["dir"] / "filter-ran"
        info = repo / ".git/info"
        info.mkdir(exist_ok=True)
        (info / "attributes").write_text("bootstrap/** filter=evil\n")
        _git_out(repo, "config", "filter.evil.smudge",
                 f"sh -c 'echo ran > {marker}; echo print\\(1\\)'")
        _git_out(repo, "config", "filter.evil.clean", "cat")
        self._scan(ceremony)
        archive = subprocess.run(
            ["git", "-C", str(repo), "archive", "refs/cairn/gate-anchor",
             "bootstrap"], capture_output=True, check=True).stdout
        assert marker.exists(), (
            "the control: `git archive` does run the filter on this repository")
        marker.unlink()
        r = _launch(ceremony, mode=("--scan-digest",))
        assert r.returncode == 0, r.stderr
        assert not marker.exists(), "a filter ran while the anchor was written"
        assert "ANCHOR-CHECKER" in r.stdout and archive

    def test_an_environment_variable_cannot_put_code_before_the_checker(
            self, ceremony, tmp_path):
        marker = tmp_path / "path-ran"
        planted = tmp_path / "planted"
        planted.mkdir()
        (planted / "hashlib.py").write_text(
            f"open({str(marker)!r}, 'w').write('ran')\n")
        control = subprocess.run(
            [sys.executable, "-S", "-c", "import hashlib"], capture_output=True,
            env={"PYTHONPATH": str(planted)})
        assert marker.exists() and control.returncode == 0, (
            "the control: without -E the planted module is imported")
        marker.unlink()
        r = self._scan(ceremony, env={**os.environ, "PYTHONPATH": str(planted)})
        assert r.returncode == 0 and "ANCHOR-CHECKER" in r.stdout, r.stderr
        assert not marker.exists()

    def test_a_pth_file_in_the_interpreters_packages_folder_does_not_run(
            self, ceremony, tmp_path):
        binary, marker = _interpreter_with_a_planted_pth_file(tmp_path)
        values = _write_values(ceremony["bed"], override={"python": str(binary)})
        r = self._scan(ceremony, values=values)
        assert r.returncode == 0 and "ANCHOR-CHECKER" in r.stdout, r.stderr
        assert not marker.exists(), "a .pth file ran before the anchor's checker"

    @pytest.mark.parametrize("name,kind", [
        ("bootstrap/tests/has space.py", "file"),
        ("bootstrap/tests/quo\"te.py", "file"),
        ("bootstrap/tests/linked.py", "symlink")])
    def test_an_entry_that_is_not_a_plain_regular_file_refuses(
            self, ceremony, name, kind):
        repo = ceremony["repo"]
        old = _git_out(repo, "rev-parse", "refs/cairn/gate-anchor").strip()
        index = str(Path(ceremony["dir"]) / "scratch-index")
        env = {**os.environ, "GIT_INDEX_FILE": index}
        _git_out(repo, "read-tree", old, env=env)
        for rel, text in {_CHECKER_PATH: _ANCHOR_CHECKER, name: "../x"}.items():
            blob = _git_out(repo, "hash-object", "-w", "--stdin",
                            data=text.encode()).strip()
            mode = "120000" if kind == "symlink" and rel == name else "100644"
            _git_out(repo, "update-index", "--add", "--cacheinfo",
                     f"{mode},{blob},{rel}", env=env)
        tree = _git_out(repo, "write-tree", env=env).strip()
        new = _git_out(repo, "-c", "user.email=t@t", "-c", "user.name=t",
                       "commit-tree", tree, "-p", old, "-m", "odd").strip()
        _git_out(repo, "update-ref", "refs/cairn/gate-anchor", new)
        r = _launch(ceremony, mode=("--scan-digest",))
        assert r.returncode != 0 and "REFUSE:" in r.stderr, r.stdout
        assert "ANCHOR-CHECKER" not in r.stdout

    def test_an_anchor_with_no_checker_fails_and_prints_no_digest(self, ceremony):
        r = _launch(ceremony, mode=("--scan-digest",))
        assert r.returncode != 0
        assert "ANCHOR-CHECKER" not in r.stdout


class TestTheLauncherAndTheArtifactRefuseTheSameBadValues:
    """The launcher checks each value before the artifact exists; the artifact
    keeps the same state checks for a value handed to it directly. Two
    implementations of one set of rules: neither may accept a value the other
    refuses, for every key, and both accept the clean file."""

    @staticmethod
    def _bad_values(bed):
        dir_ = Path(bed["dir"])
        cases = []
        for key in EXECUTABLE_KEYS:
            plain = dir_ / f"plain-{key}"
            plain.write_text("#!/bin/sh\n")
            plain.chmod(0o644)
            link = dir_ / f"link-{key}"
            link.symlink_to(bed["values"][key])
            cases += [(f"relative {key}", {key: "bin/x"}),
                      (f"absent {key}", {key: str(dir_ / "nope")}),
                      (f"directory {key}", {key: str(dir_)}),
                      (f"not executable {key}", {key: str(plain)}),
                      (f"symlink {key}", {key: str(link)})]
        sub = Path(bed["values"]["checkout"]) / "sub"
        sub.mkdir(exist_ok=True)
        checkout_link = dir_ / "checkout-link"
        checkout_link.symlink_to(bed["values"]["checkout"])
        key_link = dir_ / "key-link.pub"
        key_link.symlink_to(bed["values"]["signing_key"])
        parent_link = dir_ / "parent-link"
        parent_link.symlink_to(dir_)
        cases += [
            ("relative checkout", {"checkout": "rel/path"}),
            ("checkout not a top level", {"checkout": str(sub)}),
            ("checkout a symlink", {"checkout": str(checkout_link)}),
            ("relative signing_key", {"signing_key": "rel/key.pub"}),
            ("signing_key a directory", {"signing_key": str(dir_)}),
            ("signing_key a symlink", {"signing_key": str(key_link)}),
            ("relative package", {"package": "rel/p.json"}),
            ("package parent missing", {"package": str(dir_ / "no" / "p.json")}),
            ("package parent a symlink",
             {"package": str(parent_link / "p.json")}),
            ("relative home", {"home": "rel/home"}),
            ("home not a directory", {"home": bed["values"]["signing_key"]}),
            ("wrong schema", {"schema": "cairn-ceremony-values/v2"}),
        ]
        return cases

    #: A relative path that EXISTS from where the command starts: only an
    #: absolute-path rule refuses it, because every other check finds it fine.
    @staticmethod
    def _relative_but_existing(bed):
        return [("relative checkout that exists from here",
                 {"checkout": "checkout"}, Path(bed["dir"]))]

    def test_both_refuse_the_same_values_and_accept_the_clean_file(
            self, ceremony):
        bed = ceremony["bed"]
        disagreements = []
        cases = [(label, override, None)
                 for label, override in self._bad_values(bed)]
        cases += self._relative_but_existing(bed)
        for label, override, cwd in cases:
            values = _write_values(bed, override=override, name="values-bad")
            artifact = _run("validate", values, cwd=cwd)
            launcher = _launch(ceremony, values=values, cwd=cwd)
            if artifact.returncode == 0 or launcher.returncode == 0:
                disagreements.append((label, artifact.returncode,
                                      launcher.returncode))
        assert not disagreements, (
            "a value one of them accepts and the other refuses (label, "
            f"artifact exit, launcher exit): {disagreements}")
        clean = _write_values(bed, name="values-clean")
        assert _run("validate", clean).returncode == 0
        assert _launch(ceremony, values=clean).returncode == 0
        assert ceremony["marker"].exists()


class TestTheLauncherMemberSetMatchesTheOtherTwo:
    """Three independent statements of one set: the launcher's literal list,
    the runbook's, and `declared_authority_closure()`. Any two agreeing while
    the third drifts is how a member gets admitted that nobody declared."""

    def test_the_launcher_list_matches_this_tests_own(self):
        text = _LAUNCHER_TEMPLATE.read_text(encoding="utf-8")
        block = text.split("EXPECTED_PATHS='", 1)[1].split("'\n", 1)[0]
        recorded = tuple(l for l in block.splitlines() if l)
        assert recorded == CLOSURE

    def test_the_runbook_no_longer_carries_a_rival_copy_of_the_list(self):
        """There used to be three statements of the member set and now there
        are two, which is the improvement.

        The runbook held a pasteable loader with its own literal list, so a
        member could be added to the closure and the code and still be missing
        from the document an operator was told to copy. The runbook now
        explains the procedure instead of holding it, and a rival list
        reappearing there would be a third source of truth for a set whose
        whole value is that it is stated out of band exactly once.
        """
        runbook = (_REPO / "bootstrap/REANCHOR_RUNBOOK.md").read_text(
            encoding="utf-8")
        assert "EXPECTED_PATHS='" not in runbook, (
            "the runbook carries its own copy of the authority closure again; "
            "it will drift from the launcher's, and the launcher's is the one "
            "that runs")

    def test_the_launcher_never_invokes_cat_by_bare_name(self):
        """`cat` is validated so it can be bound. Reaching for it by bare name
        would find it through ambient PATH -- the gap the recorded paths exist
        to close, reopened at the one place it matters most."""
        text = _LAUNCHER_TEMPLATE.read_text(encoding="utf-8")
        code = "\n".join(l for l in text.splitlines()
                         if not l.lstrip().startswith("#"))
        assert "$(cat " not in code and "`cat " not in code
        for line in code.splitlines():
            assert not line.strip().startswith("cat "), line


# --------------------------------------------------------------------------
# the procedure-step registry
# --------------------------------------------------------------------------

class TestTheStepRegistry:
    """A closed, ordered registry: stable ID, stage, command, and the
    security-relevant outcome each step establishes.

    **What this delivers is a drift signal on the procedure's SHAPE.** A step
    added to the code and never documented, or documented and never
    implemented, fails. It attests nothing about whether the surrounding
    explanation is accurate -- that prose is reviewed, not machine-checked --
    and these tests are named so they cannot be mistaken for the stronger
    claim, which the proposal withdrew for exactly that reason.
    """

    def _ids(self) -> list[str]:
        r = _run("step-ids")
        assert r.returncode == 0, r.stderr
        return r.stdout.split()

    def test_the_registry_is_ordered_and_has_no_duplicates(self):
        ids = self._ids()
        assert ids, "the registry is empty"
        assert ids == sorted(ids), f"the registry is not in order: {ids}"
        assert len(ids) == len(set(ids)), "a step ID appears twice"

    def test_every_id_is_reachable_through_the_public_command(self):
        """`step-ids` derives from `steps`, so the two cannot disagree. A test
        against a retyped list would be checking the registry against itself."""
        rendered = _run("steps")
        assert rendered.returncode == 0, rendered.stderr
        for sid in self._ids():
            assert sid in rendered.stdout

    def test_every_stage_of_the_ceremony_is_represented(self):
        """A registry that documented only the stages someone remembered would
        be a drift signal with a blind spot."""
        rendered = _run("steps").stdout
        for stage in ("pre-candidate", "stage 1", "between", "stage 2",
                      "after"):
            assert stage in rendered, f"no step is in stage {stage!r}"

    def test_the_registry_names_where_candidate_code_starts(self):
        """The single most important fact about the ordering. An operator who
        cannot find this line cannot tell which half of the procedure is
        running on reviewed bytes."""
        rendered = _run("steps").stdout
        assert "FIRST CANDIDATE BYTE" in rendered

    def test_the_registry_does_not_claim_the_prose_is_checked(self):
        """The withdrawn semantic claim must stay withdrawn. A registry that
        implied its citations were validated for meaning would be asserting
        the property the proposal removed."""
        text = _ARTIFACT.read_text(encoding="utf-8")
        block = text.split("# the procedure-step registry", 1)[1][:2500]
        assert "attests NOTHING" in block or "attests nothing" in block, (
            "the registry must state what it does not deliver, beside what it "
            "does")

    def test_steps_takes_no_arguments(self):
        r = _run("steps", "extra")
        assert r.returncode != 0
        assert "takes no arguments" in r.stderr


# --------------------------------------------------------------------------
# Chunk G: the gate, not the edit
# --------------------------------------------------------------------------

class TestTheCeremonyClosureCarriesNoUnexplainedTag:
    """Chunk G2. The finding-tag pass over this repository is owned by
    `dev/plans/comprehension-outlives-the-artifact.md`, not by this plan --
    both plans would otherwise edit the same closure members and collide.

    **That plan owns the edit; this plan owns the gate.** So this node is not a
    duplicate of their check: it is the evidence that the outcome was delivered
    *for the ceremony's own surface*, whoever made the edit. If their pass ever
    regresses on these files, this fails here, in the plan that depends on it.

    What counts as unexplained: a bare finding label with no reason beside it.
    `[FUR5]` alone tells a reader nothing -- it points into a deliberation they
    cannot open. The same label followed by what it means is fine, because the
    sentence now carries its own reason.

    **Live domain vocabulary is not a finding tag and is not swept.** `N4`
    names a Maintainer fence in the series N4-N8 that the plan's intervention
    table, the runbook and an operator-facing refusal all still resolve; `R1`
    and `R6` name live gate rules. The distinction that governs here, and the
    one the owning plan's ledger records: a coordinate that still resolves to
    something live is domain vocabulary and stays; a coordinate that points
    into a closed deliberation goes.
    """

    #: The ceremony's own surface -- the files this plan is responsible for.
    #: Not the whole closure: the other members belong to other work, and a
    #: gate that failed on somebody else's file would be this plan reaching
    #: past its own scope.
    CEREMONY_FILES = (
        "bootstrap/reanchor.sh",
        "bootstrap/reanchor-launcher.template.sh",
        "bootstrap/reanchor-values.example",
        "bootstrap/tests/test_reanchor.py",
    )

    #: A bare finding label: `[FUR5]`, `[S1]`, `[M2-R1]`, `[R2-E2]`, `[X7]`.
    TAG = r"\[(?:[A-Z]{1,4}\d{1,2}(?:-[A-Z]?\d{1,2})?|FUR\d{1,2})\]"

    #: LIVE COORDINATES, exempted by name rather than by pattern.
    #:
    #: This list exists because the pattern above cannot tell them apart, and
    #: the two-sided node below caught exactly that: `[N4]` matched, so a sweep
    #: driven by this detector would have removed a Maintainer fence that the
    #: plan's intervention table, the runbook and an operator-facing refusal
    #: all still resolve. Shape does not distinguish a live coordinate from a
    #: dead citation -- only knowing what still points at it does -- so the
    #: exemption is a named list a reviewer can audit, never a cleverer regex.
    LIVE = frozenset({"N4", "N5", "N6", "N7", "N8",   # Maintainer fences
                      "R1", "R6"})                     # live gate rules

    def _offenders(self, path):
        import re
        text = (_REPO / path).read_text(encoding="utf-8")
        out = []
        for n, line in enumerate(text.splitlines(), 1):
            for m in re.finditer(self.TAG, line):
                if m.group(0).strip("[]") in self.LIVE:
                    continue
                # A tag is EXPLAINED when the same line carries prose beyond
                # the label itself. A line that is only a label -- or a label
                # and a bare noun -- is the shape that tells a reader nothing.
                rest = (line[:m.start()] + line[m.end():]).strip(" #*-:.")
                if len(rest.split()) < 4:
                    out.append(f"{path}:{n}: {line.strip()[:100]}")
        return out

    def test_no_ceremony_file_carries_a_bare_finding_label(self):
        offenders = []
        for path in self.CEREMONY_FILES:
            offenders += self._offenders(path)
        assert not offenders, (
            "these lines cite a finding and give no reason beside it, so a "
            "reader who cannot open the deliberation learns nothing:\n  "
            + "\n  ".join(offenders))

    def test_the_detector_would_actually_catch_one(self):
        """Mutation check. A tag scan that matches nothing would pass the node
        above while proving nothing -- which is the exact failure shape this
        whole plan keeps finding."""
        import re
        assert re.search(self.TAG, "    # [FUR5]"), "the pattern matches nothing"
        assert re.search(self.TAG, "see [M2-R1]")
        assert re.search(self.TAG, "per [S1]")

    def test_live_domain_vocabulary_is_not_swept(self):
        """The other direction, and the one that took a correction between two
        sessions to get right: N4 names a live Maintainer fence, and a sweep
        that removed it would break the runbook, the plan's intervention table
        and an operator-facing refusal string."""
        import re
        for keeper in ("N4", "N5", "R1", "R6"):
            assert keeper in self.LIVE, (
                f"{keeper!r} is live vocabulary and is not exempted")
        # `RA-nn` step IDs are exempt by SHAPE, not by the list: letters must be
        # followed immediately by digits to match, and a hyphen intervenes.
        assert not re.search(self.TAG, "[RA-01]")
        # And the exemption must be narrow -- a real finding label must still
        # be caught even though it is the same shape as an exempted one.
        assert re.search(self.TAG, "[S1]") and "S1" not in self.LIVE


# --------------------------------------------------------------------------
# the runbook and the registry describe one procedure
# --------------------------------------------------------------------------

_RUNBOOK = _REPO / "bootstrap/REANCHOR_RUNBOOK.md"


class TestTheRunbookAndTheRegistryAgree:
    """The documentation-agreement check.

    A step that exists in the code and not in the document, or in the document
    and not in the code, is drift the next operator pays for -- they follow a
    procedure that is missing a step, or look for one that no longer runs.

    **What this delivers is a signal on the procedure's SHAPE only.** It
    compares two structures; it establishes nothing about whether the prose
    around each citation is accurate. That prose is reviewed, not
    machine-checked. This paragraph is here because a check whose strength is
    assumed rather than stated is how a reader ends up trusting more than was
    measured.
    """

    def _registry_ids(self) -> list[str]:
        r = _run("step-ids")
        assert r.returncode == 0, r.stderr
        return r.stdout.split()

    def test_the_runbook_cites_every_registry_id_exactly_once(self):
        text = _RUNBOOK.read_text(encoding="utf-8")
        wrong = {sid: text.count(sid) for sid in self._registry_ids()
                 if text.count(sid) != 1}
        assert not wrong, (
            "these registry steps are not cited exactly once in the runbook "
            f"(id: count): {wrong}. A step cited twice has two explanations "
            "that can disagree; a step cited zero times is one the operator "
            "will not know to perform")

    def test_the_runbook_cites_no_unknown_step_id(self):
        """The other direction. A citation with no step behind it sends the
        reader to `steps` to look for something that is not there."""
        import re
        text = _RUNBOOK.read_text(encoding="utf-8")
        unknown = set(re.findall(r"RA-\d{2}", text)) - set(self._registry_ids())
        assert not unknown, f"the runbook cites steps that do not exist: {unknown}"

    def test_the_runbook_answers_where_the_review_manifest_comes_from(self):
        """One of the two questions the runbook previously left unanswered. An
        operator who cannot find this writes the manifest by hand, which is the
        exact failure the launcher exists to remove."""
        text = _RUNBOOK.read_text(encoding="utf-8")
        assert "Where does the review manifest come from?" in text
        assert "launcher composes it" in text

    def test_the_runbook_answers_how_to_read_the_report(self):
        """The other one. A confirmed digest over an unread report authorizes
        something the Maintainer has not seen, and until now no command
        rendered it."""
        text = _RUNBOOK.read_text(encoding="utf-8")
        assert "How do I read the report?" in text
        assert "show-report" in text

    def test_the_runbook_lists_the_prerequisites(self):
        """Every prerequisite is something the ceremony refuses without, and
        discovering that at stage 2 costs a full authorization package."""
        text = _RUNBOOK.read_text(encoding="utf-8")
        assert "### Prerequisites" in text
        for needed in ("instantiated launcher", "authorization packet",
                       "values file", "ceremony key", "candidate ref"):
            assert needed in text, f"the prerequisites omit {needed!r}"

    def test_the_runbook_tells_the_operator_the_values_file_goes_stale(self):
        """A version-pinned executable path breaks at the next toolchain
        upgrade. An operator who is not told that reads a correct refusal as a
        broken tool -- and the tempting fix is to relax the rule."""
        text = _RUNBOOK.read_text(encoding="utf-8")
        assert "goes stale, and that is not a malfunction" in text

    def test_the_runbook_says_the_agreement_check_is_shape_only(self):
        """The withdrawn semantic claim must stay withdrawn in the document as
        well as in the code. A runbook that implied its citations were
        validated for meaning would reinstate it where an operator reads."""
        text = _RUNBOOK.read_text(encoding="utf-8")
        assert "attests nothing" in text and "reviewed, not\nmachine-checked" in text, (
            "the runbook must state the limit of its own agreement check")


class TestTheRunbookHoldsNoLauncherCopy:
    """The runbook explains the launcher by the step registry and does not
    reproduce it. A pasteable copy is a second implementation of the ceremony
    that nobody runs and nothing tests -- which is how recorded steps once went
    stale while the code was correct."""

    def test_no_ceremony_loader_block_survives_in_the_runbook(self):
        runbook = _RUNBOOK.read_text(encoding="utf-8")
        assert "/bin/sh <<'" not in runbook, (
            "an executable loader block is back in the runbook")
        for delim in ("LOADER", "TRANSITION", "STAGE2", "STAGE2T"):
            assert f"<<'{delim}'" not in runbook

    def test_the_runbook_does_not_reproduce_the_launchers_member_list(self):
        runbook = _RUNBOOK.read_text(encoding="utf-8")
        assert "EXPECTED_PATHS" not in runbook


# --------------------------------------------------------------------------
# the whole ceremony, end to end
# --------------------------------------------------------------------------
#
# The ceremony bed is imported rather than rebuilt. Duplicating it would create
# two beds that drift, and a drifting fixture is worse than an import: the copy
# that stops resembling a real ceremony keeps passing.
from bootstrap.tests.test_gate_preflight import (        # noqa: E402
    _ceremony_repo as _build_ceremony_repo,
    _n4_precondition as _key_withheld,
)


class TestTheMaintainerCanPerformTheWholeCeremony:
    """**Acceptance criterion 1's evidence producer.**

    The objective this plan is measured against:

        The re-anchor ceremony must be performable, end to end, by the
        Maintainer alone -- without an agent generating a script, retyping a
        digest, or improvising a reader -- and without any control being weaker
        than it was before.

    This node starts from **only** what the builder delivers (the
    instantiated launcher and the packet bound into it) plus a values file
    the Maintainer wrote once, and runs the ceremony to the two-ref
    transaction. Nothing here fills a placeholder, composes an authority input,
    or reads a digest out of the artifact that carries it.

    **What it cannot establish**, said plainly rather than left for a reviewer
    to notice: that a *human* finds this usable. A test can show the commands
    compose into a working ceremony; it cannot show anyone can follow them.
    That half of the criterion is established at the real ceremony and nowhere
    else.
    """

    def _values(self, repo):
        """The one thing the Maintainer authors, and it is data."""
        import shutil as _shutil
        tools = {}
        for key, binary in (("env", "env"), ("git", "git"), ("mktemp", "mktemp"),
                            ("mkdir", "mkdir"), ("shasum", "shasum"),
                            ("sort", "sort"), ("cat", "cat")):
            found = _shutil.which(binary)
            assert found, f"no {binary} on this host"
            tools[key] = os.path.realpath(found)
        values = {
            "schema": "cairn-ceremony-values/v1",
            "checkout": str(repo),
            "signing_key": str(repo.parent / "maint.pub"),
            "package": str(repo.parent / "authorization-package.json"),
            "home": str(repo.parent),
            "python": os.path.realpath(sys.executable),
            **tools,
        }
        path = repo.parent / "ceremony-values"
        path.write_text("".join(f"{k} {v}\n" for k, v in values.items()),
                        encoding="utf-8")
        return str(path)

    def _review_delivers(self, repo, oid):
        """What the builder hands over: a packet
        and a launcher instantiated with that packet's digest.

        Composed here the way the review composes it -- from the closure at the
        candidate -- because the alternative is a fixture that invents an
        authority artifact, which is the act this whole plan removes.
        """
        import hashlib
        members = []
        for rel in sorted(P.declared_authority_closure()):
            blob = subprocess.run(
                ["git", "-C", str(repo), "cat-file", "blob", f"{oid}:{rel}"],
                capture_output=True, check=True).stdout
            members.append((hashlib.sha256(blob).hexdigest(), rel))
        artifact_sha = dict((rel, sha) for sha, rel in members)[
            "bootstrap/reanchor.sh"]
        packet_text = "\n".join(
            ["schema cairn-authorization-packet/v1",
             "provenance builder and reader, end-to-end node",
             "artifact bootstrap/reanchor.sh",
             f"artifact_sha256 {artifact_sha}"]
            + [f"member {sha} {rel}" for sha, rel in members]) + "\n"

        packet = repo.parent / "authorization-packet.txt"
        packet.write_bytes(packet_text.encode())
        template = _LAUNCHER_TEMPLATE.read_text(encoding="utf-8")
        launcher = repo.parent / "reanchor-launcher.sh"
        launcher.write_text(
            template.replace("@PACKET_SHA256@",
                             hashlib.sha256(packet_text.encode()).hexdigest()),
            encoding="utf-8")
        return launcher, packet

    def _sh(self, *args, cwd):
        return subprocess.run(["/bin/sh", *[str(a) for a in args]],
                              capture_output=True, text=True, check=False,
                              cwd=str(cwd))

    def test_from_the_review_outputs_to_the_two_ref_transaction(self, tmp_path):
        import hashlib
        repo, anchor, head, _epoch = _build_ceremony_repo(tmp_path)
        values = self._values(repo)
        launcher, packet = self._review_delivers(repo, head)
        package = Path(repo.parent / "authorization-package.json")
        if package.exists():
            package.unlink()

        before_head = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()
        before_anchor = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", P._ANCHOR_REF],
            capture_output=True, text=True, check=True).stdout.strip()

        # --- ONE command, with the key genuinely unavailable ----------------
        with _key_withheld(tmp_path / "maint"):
            r1 = self._sh(launcher, packet, values, head, cwd=repo)
        assert r1.returncode == 0, f"stage 1 failed:\n{r1.stdout}\n{r1.stderr}"
        assert package.exists(), "stage 1 wrote no authorization package"
        assert subprocess.run(
            ["git", "-C", str(repo), "rev-parse", P._ANCHOR_REF],
            capture_output=True, text=True, check=True).stdout.strip() == \
            before_anchor, "stage 1 moved a ref; it holds no key and moves nothing"

        # --- the two steps that are the Maintainer's judgement --------------
        report = self._sh(launcher, packet, values, head, "--show-report",
                          cwd=repo)
        assert report.returncode == 0, report.stderr
        assert before_anchor in report.stdout and before_head in report.stdout, (
            "the report does not name the state being authorized")

        digest_out = self._sh(launcher, packet, values, head, "--hash-package",
                              cwd=repo)
        assert digest_out.returncode == 0, digest_out.stderr
        confirmed = next(w for w in digest_out.stdout.split()
                         if len(w) == 64 and all(c in "0123456789abcdef"
                                                 for c in w))
        # The digest the operator confirms is over the bytes on disk. Computing
        # it here independently is the point: a node that reused the artifact's
        # own answer would be checking the artifact against itself.
        assert confirmed == hashlib.sha256(package.read_bytes()).hexdigest(), (
            "hash-package did not report the digest of the bytes on disk")

        # --- the key becomes available, and only now ------------------------
        r2 = self._sh(launcher, packet, values, head, "--stage2", confirmed,
                      cwd=repo)
        assert r2.returncode == 0, f"stage 2 failed:\n{r2.stdout}\n{r2.stderr}"

        # --- the two-ref transaction ---------------------------------------
        after_head = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()
        after_anchor = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", P._ANCHOR_REF],
            capture_output=True, text=True, check=True).stdout.strip()
        assert after_anchor != before_anchor, "the anchor did not move"
        assert after_anchor == after_head, (
            "branch and anchor did not land on the same commit; the two-ref "
            "transaction is what makes them one act rather than two")
        signed = subprocess.run(
            ["git", "-C", str(repo), "log", "-1", "--format=%G?"],
            capture_output=True, text=True, check=True).stdout.strip()
        assert signed == "G", (
            f"the checkpoint is not signed by a roster key (%G? = {signed!r})")

    def test_no_step_of_that_ceremony_needed_an_authored_script(self):
        """The objective's first clause, asserted on the node above rather than
        claimed in prose.

        Every command in that test is either the reviewed launcher or a named
        subcommand of the reviewed artifact. If a future change makes the
        ceremony need a `bash -c` or a generated file again, this fails -- which
        is the whole failure the plan exists to remove, and it would otherwise
        reappear silently inside a passing end-to-end test.
        """
        import inspect
        src = inspect.getsource(
            self.test_from_the_review_outputs_to_the_two_ref_transaction)
        assert "bash -c" not in src and 'bash", "-c' not in src, (
            "the ceremony needs a shell one-liner again")
        for command in ("show-report", "hash-package", "--stage2"):
            assert command in src, (
                f"the end-to-end node no longer exercises {command!r}")


class TestLazyFetchCannotRunAnUnlistedTransportHelper:
    """**[M2-X1]**, found by exact-byte security review and reproduced here.

    `sterile_git` empties the environment and pins replacement objects, hooks
    and the filesystem monitor. It did not stop Git's **automatic lazy fetch**.

    A blob-filtered checkout carries a *promisor remote* in its own local
    config, and that config is candidate-controlled input. Point the promisor at
    `ext::<program>` and Git runs `<program>` the first time it reads an object
    the checkout does not hold locally -- an executable outside the six recorded
    in `SAFETY.md` Rule 13, executing before any candidate artifact byte.

    **The refusal that follows does not restore the boundary.** Git fails, the
    launcher refuses, and the helper has already run. A control that fires after
    the thing it was guarding has happened is a report, not a boundary.

    **`env -i` is what left it open**, which is the part worth remembering.
    Emptying the environment is correct for every variable that *steers* git,
    because absent is the safe value for those. For `GIT_NO_LAZY_FETCH` absent
    means *enabled*. An emptied environment is not a safe environment when the
    safe state requires a variable to be **present**.
    """

    def _promisor_checkout(self, tmp_path, marker):
        """A checkout with a genuinely missing object and a hostile promisor.

        The object has to be really absent -- an earlier version of this fixture
        proved nothing because a probe lazily fetched the blob from the real
        origin before the promisor was repointed, leaving it local. The
        `--missing=print` assertion below is what stops that recurring.
        """
        git = shutil.which("git")
        assert git, "no git on this host"
        helper = tmp_path / "transport-helper.sh"
        helper.write_text(
            "#!/bin/sh\n"
            f"printf 'ran\\n' > {marker}\n"
            "exit 1\n")
        helper.chmod(0o755)

        origin = tmp_path / "origin"
        origin.mkdir()
        run = lambda *a, **k: subprocess.run(a, check=True, capture_output=True, **k)
        run(git, "init", "-q", str(origin))
        (origin / "blob.txt").write_text("payload\n")
        run(git, "-C", str(origin), "add", "-A")
        run(git, "-C", str(origin), "-c", "user.email=t@t", "-c", "user.name=t",
            "commit", "-qm", "one")
        # The origin must permit filtering or the clone silently takes the blob
        # and the fixture tests nothing.
        run(git, "-C", str(origin), "config", "uploadpack.allowfilter", "true")

        work = tmp_path / "work"
        run(git, "clone", "-q", "--no-local", "--no-checkout",
            "--filter=blob:none", f"file://{origin}", str(work))

        missing = subprocess.run(
            [git, "-C", str(work), "rev-list", "--objects", "--all",
             "--missing=print"], capture_output=True, text=True)
        assert any(l.startswith("?") for l in missing.stdout.splitlines()), (
            "no object is promisor-deferred, so this fixture cannot trigger a "
            "lazy fetch and would pass without testing anything")

        run(git, "-C", str(work), "config", "remote.origin.url",
            f"ext::{helper} %S")
        run(git, "-C", str(work), "config", "protocol.ext.allow", "always")
        return work

    def _read_blob(self, work, marker, *, extra_env):
        git = shutil.which("git")
        env = {"HOME": "/nonexistent", **extra_env}
        subprocess.run(
            [git, "--no-replace-objects", "-c", "core.useReplaceRefs=false",
             "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false",
             "-C", str(work), "cat-file", "blob", "HEAD:blob.txt"],
            capture_output=True, env=env)
        return marker.exists()

    def test_an_emptied_environment_alone_lets_the_helper_run(self, tmp_path):
        """The non-vacuity half, and the finding itself.

        Without this the repair node below would pass on a fixture that could
        never have triggered a fetch, which is how a security test comes to
        report success while testing nothing.
        """
        marker = tmp_path / "HELPER-RAN"
        work = self._promisor_checkout(tmp_path, marker)
        assert self._read_blob(work, marker, extra_env={}), (
            "the fixture did not trigger the transport helper, so the repair "
            "node proves nothing")

    def test_GIT_NO_LAZY_FETCH_stops_it(self, tmp_path):
        marker = tmp_path / "HELPER-RAN"
        work = self._promisor_checkout(tmp_path, marker)
        assert not self._read_blob(
            work, marker, extra_env={"GIT_NO_LAZY_FETCH": "1"}), (
            "the transport helper ran despite GIT_NO_LAZY_FETCH=1")

    def test_the_launcher_binds_it(self):
        """Set, not inherited: the launcher runs under `env -i`, so a value the
        operator happens to export does not survive."""
        text = _LAUNCHER_TEMPLATE.read_text(encoding="utf-8")
        block = text.split("sterile_git() {", 1)[1].split("}", 1)[0]
        assert "GIT_NO_LAZY_FETCH=1" in block, (
            "sterile_git does not bind GIT_NO_LAZY_FETCH; a promisor checkout "
            "can run an unlisted transport helper before candidate code")

    def test_the_checker_binds_it_too(self):
        """The review found this in the launcher. The checker's own git
        environment had the identical gap, and in stage 2 that helper would run
        after the ceremony key is loaded."""
        assert P._sterile_env().get("GIT_NO_LAZY_FETCH") == "1"


class TestStage1RefusesAKeyTheAnchorDoesNotName:
    """The check that turns a rollover mistake from expensive into instant.

    Measured on 2026-08-19: a ceremony ran a full stage 1, wrote a 1.6 MB
    authorization package, loaded the key, signed a commit, and *then* refused
    with `status U` -- a correct refusal arriving one stage and one package too
    late, at the only step that costs the operator anything.

    The cause is structural, not carelessness. **A key rollover is the one
    ceremony where the obvious key is the wrong one**: the transition must be
    signed by the OLD anchored key, because the old roster is what verifies the
    commit that installs the new one. Pointing `signing_key` at the newly
    created key is the natural reading of "we are rolling over to this key",
    and nothing upstream contradicted it.
    """

    def _anchored_roster_of(self, bed):
        return Path(bed["values"]["checkout"]) / "dev/.cairn/allowed_signers"

    def test_a_key_absent_from_the_anchored_roster_refuses(self, bed, tmp_path):
        """The rollover mistake, caught in the first second."""
        other = tmp_path / "some_other_key"
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f",
                        str(other), "-C", "not-in-roster"], check=True,
                       capture_output=True)
        r = _run("stage1", _write_values(
            bed, override={"signing_key": str(other.with_suffix(".pub"))}))
        _assert_refused(r, "NOT in the anchored roster")
        assert "OLD key" in r.stderr, (
            "the refusal must name the rollover case, which is the reason an "
            "operator most often lands here")

    def test_it_refuses_BEFORE_a_package_is_written(self, bed, tmp_path):
        """The whole value of the check is where it sits. A refusal after the
        package exists is the behaviour this replaces."""
        other = tmp_path / "other2"
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f",
                        str(other), "-C", "x"], check=True, capture_output=True)
        package = Path(bed["values"]["package"])
        if package.exists():
            package.unlink()
        _run("stage1", _write_values(
            bed, override={"signing_key": str(other.with_suffix(".pub"))},
            name="values-early"))
        assert not package.exists(), (
            "a package was written before the key was checked; the refusal "
            "then costs what it is meant to save")

    def test_the_roster_key_is_accepted(self, bed):
        """The other direction, so the node above is not passing because every
        key refuses."""
        r = _run("validate", _write_values(bed))
        assert r.returncode == 0, r.stderr

    def test_the_check_reads_the_ANCHORED_roster_not_the_worktree_copy(
            self, bed, tmp_path):
        """The distinction that makes the check meaningful.

        During a rollover the worktree roster holds the NEW key and the anchor
        holds the OLD one -- that is what a rollover *is*. A check against the
        worktree copy would accept exactly the key that cannot verify, which is
        the failure it exists to prevent, with extra steps.
        """
        checkout = Path(bed["values"]["checkout"])
        roster = checkout / "dev/.cairn/allowed_signers"
        new_key = tmp_path / "rolled_to"
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f",
                        str(new_key), "-C", "new"], check=True,
                       capture_output=True)
        pub = new_key.with_suffix(".pub").read_text().split()
        # The worktree now names ONLY the new key; the anchor still names the old.
        roster.write_text(f"rolled {pub[0]} {pub[1]}\n", encoding="utf-8")

        r_new = _run("stage1", _write_values(
            bed, override={"signing_key": str(new_key.with_suffix(".pub"))},
            name="values-new"))
        _assert_refused(r_new, "NOT in the anchored roster")

        # And the OLD key -- absent from the worktree copy, present at the
        # anchor -- must still be accepted.
        r_old = _run("validate", _write_values(bed, name="values-old"))
        assert r_old.returncode == 0, (
            "the old key was rejected; the check is reading the worktree copy "
            f"rather than the anchor:\n{r_old.stderr}")
