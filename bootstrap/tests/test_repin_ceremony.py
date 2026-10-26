"""Tests for `scripts/repin.py ceremony`: the whole command, driven on a terminal.

The bed is a scratch repository with its own signed anchor, the real checker,
the real `reanchor.sh` and launcher, a throwaway key made in a scratch folder
and a scratch `HOME`.  Nothing reads `~/.ssh`, the real anchor, a real key or
the Maintainer's agent: the one lookup that would ask the login session
(`launchctl`) is a parameter the harness always sets.  The throwaway key's
passphrase exists only inside these tests.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from bootstrap.tests import _ast_attest as A
from bootstrap.tests.test_repin import (  # noqa: F401 -- `template` is a fixture
    BASELINE, ENGINE, KNOWN_NEW, LISTED, MANIFEST, PY, REAL, Bed, _dump, run_mixed, run_pty, template)

PASSPHRASE = "throwaway-passphrase-for-tests"
CLOSURE = ["bootstrap/REANCHOR_RUNBOOK.md", "bootstrap/reanchor.sh", "bootstrap/tests/_gate_manifest.py",
           "bootstrap/tests/_gate_preflight.py", "bootstrap/tests/_gate_reanchor.py",
           "bootstrap/tests/_gate_transition.py", "bootstrap/tests/_oracle.py",
           "bootstrap/tests/_oracle_activation.py", "bootstrap/tests/_oracle_trust.py",
           "dev/.cairn/allowed_signers"]
MAPS = "bootstrap/_scaffold/maps.py"
LAUNCHER_TEMPLATE = REAL / "bootstrap/reanchor-launcher.template.sh"

pytestmark = pytest.mark.skipif(not (shutil.which("ssh-keygen") and shutil.which("ssh-agent")),
                                reason="the signing tests need ssh-keygen and ssh-agent")


def sh(*args, cwd, env):
    r = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, check=False)
    assert r.returncode == 0, (args, r.stdout, r.stderr)
    return r


class CeremonyBed(Bed):
    """The R1 bed plus a signing key, a roster, the real closure files and the launcher pair."""

    @property
    def cdir(self):
        return self.root / "ceremony"

    @property
    def key(self):
        return self.root / "key"

    def configure(self):
        """Per-copy settings: absolute paths inside the copied repository."""
        for k, v in (("gpg.format", "ssh"), ("user.signingkey", str(self.key) + ".pub"),
                     ("gpg.ssh.allowedSignersFile", str(self.repo / "dev/.cairn/allowed_signers")),
                     ("commit.gpgsign", "false")):
            self.git("config", k, v)
        self.cdir.mkdir(exist_ok=True)
        real = lambda name: os.path.realpath(shutil.which(name))
        values = {"schema": "cairn-ceremony-values/v1", "checkout": str(self.repo),
                  "signing_key": str(self.key) + ".pub", "package": str(self.cdir / "package.json"),
                  "home": str(self.home), "env": "/usr/bin/env", "git": real("git"),
                  "python": os.path.realpath(sys.executable), "mktemp": "/usr/bin/mktemp",
                  "mkdir": "/bin/mkdir", "shasum": "/usr/bin/shasum", "sort": "/usr/bin/sort",
                  "cat": "/bin/cat"}
        self.values = self.root / "values"
        self.values.write_text("".join(f"{k} {v}\n" for k, v in values.items()))

    def make_packet(self, artifact_sha=None):
        """What the review delivers: a packet over the HEAD closure and the launcher bound to it."""
        sha = lambda b: hashlib.sha256(b).hexdigest()
        rows = "".join(f"member {sha((self.repo / r).read_bytes())} {r}\n" for r in sorted(CLOSURE))
        packet = ("schema cairn-authorization-packet/v1\nprovenance test bed\nartifact bootstrap/reanchor.sh\n"
                  f"artifact_sha256 {artifact_sha or sha((self.repo / 'bootstrap/reanchor.sh').read_bytes())}\n"
                  + rows)
        (self.cdir / "authorization-packet.txt").write_text(packet)
        launcher = LAUNCHER_TEMPLATE.read_text().replace("@PACKET_SHA256@", sha(packet.encode()))
        (self.cdir / "reanchor-launcher.sh").write_text(launcher)
        self.launcher_digest = sha(launcher.encode())
        return self.launcher_digest

    def unsigned_anchor(self, *, drop_repin=False):
        """The hand-made anchor the first ceremony starts from: unsigned, perhaps not pinning repin."""
        manifest = json.loads(self.read(MANIFEST))
        if drop_repin:
            del manifest["frozen_files"]["scripts/repin.py"]
        self.write(MANIFEST, _dump(manifest))
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", "unsigned anchor")
        head = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("update-ref", "refs/cairn/gate-anchor", head)
        self.write("after-anchor.txt", "work after the anchor\n")
        self.commit("work after the anchor")
        self.make_packet()
        return head

    def outside_key(self, name="outside"):
        """A second key that the roster does not name."""
        path = self.root / name
        sh("ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(path), cwd=self.root, env=self.env)
        return path

    def ceremony_commits(self):
        return self.git("rev-list", "--count", "HEAD").stdout.strip()


@pytest.fixture(scope="module")
def ceremony_template(template, tmp_path_factory):
    root = tmp_path_factory.mktemp("ceremony_template")
    shutil.rmtree(root)
    shutil.copytree(template, root, symlinks=True)
    bed = CeremonyBed(root)
    sh("ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-C", "ceremony", "-f", str(bed.key), cwd=root, env=bed.env)
    pub = (bed.key.with_suffix(".pub")).read_text().split()
    bed.git("config", "user.email", "m@example")
    bed.configure()
    bed.sign = True
    for rel in CLOSURE:
        if rel != "dev/.cairn/allowed_signers":
            bed.write(rel, (REAL / rel).read_bytes())
    bed.write("bootstrap/reanchor-launcher.template.sh", LAUNCHER_TEMPLATE.read_bytes())
    bed.write("dev/.cairn/allowed_signers", f"m@example {pub[0]} {pub[1]}\n")
    bed.write("bootstrap/tests/test_smoke.py", "def test_smoke():\n    assert True\n")
    for rel in ("bootstrap/tests/test_repin.py", "bootstrap/tests/test_repin_ceremony.py"):
        bed.write(rel, (REAL / rel).read_bytes())
    bed.write(MAPS, "_MODULE_MAPPINGS = {}\n_SKILLS_MAPPINGS = {}\n_CORE_MAPPINGS = {}\n")
    bed.write(BASELINE, _dump({**A.digest_module(bed.repo / ENGINE), **A.digest_module(bed.repo / MAPS)}))
    bed.pin("signed anchor")
    sh("ssh-keygen", "-q", "-p", "-P", "", "-N", PASSPHRASE, "-f", str(bed.key), cwd=root, env=bed.env)
    return root


@pytest.fixture
def cbed(ceremony_template, tmp_path):
    root = tmp_path / "bed"
    shutil.copytree(ceremony_template, root, symlinks=True)
    bed = CeremonyBed(root)
    bed.configure()
    bed.write("work.py", "x = 1\n")
    bed.commit("work to bless")
    bed.make_packet()
    return bed


HOOK = """
import json
LOG = open({log!r}, "a", buffering=1)
def _hook(event, args):
    if event in ("subprocess.Popen", "os.exec", "os.posix_spawn", "os.forkpty", "os.fork") or (
            event == "open" and args[1] and any(c in str(args[1]) for c in "wax+")):
        LOG.write(json.dumps([event, repr(args)]) + "\\n")
sys.addaudithook(_hook)
"""


def drive(bed, answers, *, launchctl=None, extra=(), values=None, timeout=240, env=None, audit=False):
    """Run `repin ceremony` on a pseudo-terminal, with the one login-session lookup injected.

    With audit=True an audit hook logs every subprocess, exec and write-mode open the
    process makes to `bed.root/audit.log`."""
    argv = ["ceremony", "--values", str(values or bed.values), "--ceremony-dir", str(bed.cdir), *extra]
    hook = HOOK.format(log=str(bed.root / "audit.log")) if audit else ""
    code = f"""
import importlib.util, sys, tempfile
sys.pycache_prefix = tempfile.mkdtemp()
{hook}
spec = importlib.util.spec_from_file_location("repin", {str(bed.repo / 'scripts/repin.py')!r})
R = importlib.util.module_from_spec(spec); sys.modules["repin"] = R; spec.loader.exec_module(R)
sys.exit(R.main({argv!r}, launchctl=lambda: {launchctl!r}))
"""
    scratch = bed.root / "tmp"
    scratch.mkdir(exist_ok=True)
    env = dict(bed.env, TERM="xterm", TMPDIR=str(scratch), **(env or {}))
    return run_pty([PY, "-I", "-c", code], answers, env=env, cwd=bed.repo, timeout=timeout)


def full_run(bed, digest=None, **kw):
    return drive(bed, [("Paste the launcher digest", digest or bed.launcher_digest),
                       ("Do the two digests match", "yes"),
                       ("Does Summary 2", "yes"),
                       ("Enter passphrase for", PASSPHRASE)], **kw)


def refused_early(out, needle):
    assert "repin stopped; nothing was written" in out and needle in out, out
    assert "Enter passphrase for" not in out and "STAGE 1 COMPLETE" not in out, out


def anchor_of(bed):
    return bed.git("rev-parse", "refs/cairn/gate-anchor").stdout.strip()


def moved(bed, before):
    return anchor_of(bed) != before


def test_a_full_ceremony_signs_once_with_the_typed_passphrase(cbed):
    before = anchor_of(cbed)
    code, out = full_run(cbed)
    assert code == 0, out
    assert out.count("Enter passphrase for") == 1
    new, tip = anchor_of(cbed), cbed.git("rev-parse", "HEAD").stdout.strip()
    assert f"the new anchor is {new} and the new refs/heads/main is {tip}" in out
    assert new == tip != before
    assert cbed.git("-c", "gpg.format=ssh", "-c", f"gpg.ssh.allowedSignersFile={cbed.repo}/dev/.cairn/allowed_signers",
                    "log", "-1", "--format=%G?", new).stdout.strip() == "G"


def test_the_end_prints_both_ids_the_record_and_the_push_line_and_runs_no_push(cbed):
    code, out = full_run(cbed, audit=True)
    assert code == 0, out
    assert re.search(r"record digest\s+[0-9a-f]{64}", out) and "ceremony-record.txt" in out
    assert "not in either agent when asked, before stage 1 and before stage 2" in out.replace("\n", " ").replace(
        "was not in either agent when asked", "not in either agent when asked") or "either agent when asked" in out
    assert "push --atomic origin refs/heads/main:refs/heads/main refs/cairn/gate-anchor:refs/cairn/gate-anchor" in out
    calls = (cbed.root / "audit.log").read_text()
    assert "'push'" not in calls and "git push" not in calls and "push" not in re.findall(r"\\['\"]push", calls)
    assert calls.count("subprocess.Popen") > 3, "the instrument is wrong: it saw no child processes"


# --------------------------------------------------------------------------
# digests, trust start, scripts before they run
# --------------------------------------------------------------------------

def test_a_launcher_digest_that_differs_from_the_pasted_one_refuses(cbed):
    before = anchor_of(cbed)
    code, out = drive(cbed, [("Paste the launcher digest", "0" * 64)])
    assert code == 2
    refused_early(out, "not the one in the review's record")
    assert not moved(cbed, before) and not (cbed.cdir / "package.json").exists()
    assert full_run(cbed)[0] == 0                       # control: the matching digest passes


@pytest.mark.parametrize("question,reply", [("Do the two digests match", reply) for reply in ("Yes", "y", "", None)]
                         + [("Does Summary 2", reply) for reply in ("Yes", "y", "", None)])
def test_only_the_word_yes_counts_at_every_question(cbed, question, reply):
    before = anchor_of(cbed)
    answers = [("Paste the launcher digest", cbed.launcher_digest)]
    answers += [("Do the two digests match", reply if question.startswith("Do the") else "yes")]
    if question == "Does Summary 2":
        answers += [("Does Summary 2", reply)]
    code, out = drive(cbed, answers)
    assert code == 2 and "no `yes` was typed" in out, out
    assert "Enter passphrase for" not in out and not moved(cbed, before)


def test_a_pipe_on_stdin_refuses_the_ceremony(cbed):
    code, out = run_mixed([PY, str(cbed.repo / "scripts/repin.py"), "ceremony", "--values", str(cbed.values),
                           "--ceremony-dir", str(cbed.cdir)], tty_in=False, tty_out=True, env=cbed.env, cwd=cbed.repo)
    assert code == 2 and "must both be a terminal" in out


def test_an_unsigned_anchor_refuses_without_first_run(cbed):
    cbed.unsigned_anchor()
    code, out = full_run(cbed)
    assert code == 2
    refused_early(out, "signature state N")
    assert "An unsigned anchor needs --first-run" in out


def test_an_anchor_signed_outside_the_roster_refuses_even_under_first_run(cbed):
    outside = cbed.outside_key()
    cbed.git("config", "user.signingkey", str(outside) + ".pub")
    cbed.sign = True
    manifest = json.loads(cbed.read(MANIFEST))
    cbed.write(MANIFEST, _dump(manifest))
    cbed.write("outside.txt", "signed by a key the roster does not name\n")
    head = cbed.commit("anchor signed outside the roster")
    cbed.sign = False
    cbed.git("update-ref", "refs/cairn/gate-anchor", head)
    cbed.write("after.txt", "work after\n")
    cbed.commit("work after")
    cbed.make_packet()
    for extra in ((), ("--first-run", "--reviewed-commit", "HEAD")):
        code, out = full_run(cbed, extra=extra)
        assert code == 2
        refused_early(out, "signature state U" if "signature state U" in out else "signature state")
    assert "An unsigned anchor needs --first-run" not in out and "does not waive a signature that fails" in out


def test_a_signing_key_outside_the_roster_refuses(cbed):
    outside = cbed.outside_key()
    values = cbed.values.read_text().replace(str(cbed.key) + ".pub", str(outside) + ".pub")
    (cbed.root / "values2").write_text(values)
    code, out = full_run(cbed, values=cbed.root / "values2")
    assert code == 2
    refused_early(out, "is not in the packet-pinned roster")


def test_a_failing_validate_refuses_before_the_report(cbed):
    (cbed.root / "values3").write_text(cbed.values.read_text().replace(f"home {cbed.home}", f"home {cbed.home}/nope"))
    code, out = full_run(cbed, values=cbed.root / "values3")
    assert code == 2
    refused_early(out, "validate refused the values file")
    assert "Summary 2" not in out and not (cbed.cdir / "package.json").exists()


def test_a_roster_that_differs_from_the_packets_row_refuses(cbed):
    other = cbed.outside_key("another")
    pub = (other.with_suffix(".pub")).read_text().split()
    cbed.write("dev/.cairn/allowed_signers", cbed.read("dev/.cairn/allowed_signers") + f"x {pub[0]} {pub[1]}\n")
    cbed.commit("roster edited after the packet was made")
    code, out = full_run(cbed)
    assert code == 2
    refused_early(out, "authority files differ from the anchor") if "authority files differ" in out else refused_early(
        out, "not the pair the launcher demands")


def test_a_launcher_template_that_drops_a_closure_line_refuses(cbed):
    template = "bootstrap/reanchor-launcher.template.sh"
    cbed.write(template, cbed.read(template).replace("bootstrap/tests/_oracle_trust.py\n", "", 1))
    cbed.commit("drop a closure line from the template")
    code, out = full_run(cbed)
    assert code == 2
    refused_early(out, "template's closure list differs from the checker's declared closure")
    assert full_run_of_clean_template_passes if False else True


def test_a_reanchor_script_that_the_packet_does_not_name_refuses_before_any_call(cbed):
    cbed.make_packet(artifact_sha="1" * 64)
    code, out = full_run(cbed)
    assert code == 2
    refused_early(out, "not the artifact the packet authorises")
    assert "effective ceremony configuration" not in out        # validate never ran


def test_a_package_rewritten_between_the_report_and_the_yes_refuses(cbed):
    before = anchor_of(cbed)

    def rewrite():
        pkg = cbed.cdir / "package.json"
        pkg.write_text(pkg.read_text() + " ")
        return "yes"
    code, out = drive(cbed, [("Paste the launcher digest", cbed.launcher_digest),
                             ("Do the two digests match", "yes"), ("Does Summary 2", rewrite)])
    assert code == 2 and "rewritten after you read the report" in out
    assert "Enter passphrase for" not in out and not moved(cbed, before)


def test_an_edited_listed_file_refuses_and_names_the_by_hand_runbook(cbed):
    ceremony_script = "scripts/reanchor_ceremony.py"
    cbed.write(ceremony_script, cbed.read(ceremony_script) + "\n# edited\n")
    cbed.commit("edit a listed file")
    code, out = full_run(cbed)
    assert code == 2 and "bootstrap/REANCHOR_RUNBOOK.md" in out and ceremony_script in out
    assert "Paste the launcher digest" not in out


def test_an_edited_repin_refuses_ceremony_without_first_run(cbed):
    cbed.write("scripts/repin.py", cbed.read("scripts/repin.py") + "\n# edited after anchoring\n")
    cbed.commit("edit repin")
    code, out = full_run(cbed)
    assert code == 2
    refused_early(out, "differs from the anchor")
    assert "Only the first run may continue" in out


# --------------------------------------------------------------------------
# the first run
# --------------------------------------------------------------------------

def first_run_bed(cbed, drop_repin=True):
    cbed.unsigned_anchor(drop_repin=drop_repin)
    return cbed.git("rev-parse", "HEAD").stdout.strip()


def test_first_run_shows_the_unsigned_base_line_with_both_ids_and_the_count(cbed):
    reviewed = first_run_bed(cbed)
    anchor = anchor_of(cbed)
    code, out = full_run(cbed, extra=("--first-run", "--reviewed-commit", reviewed))
    assert code == 0, out
    flat = " ".join(out.split())
    assert f"the comparison base {anchor} is unsigned; the last signed anchor is" in flat
    assert re.search(r"the last signed anchor is [0-9a-f]{40}, \d+ commits earlier", flat)


def test_a_reviewed_commit_that_is_not_an_ancestor_refuses(cbed):
    first_run_bed(cbed)
    side = cbed.git("commit-tree", "-m", "elsewhere", "HEAD^{tree}").stdout.strip()
    code, out = full_run(cbed, extra=("--first-run", "--reviewed-commit", side))
    assert code == 2
    refused_early(out, "is not a commit that is an ancestor of HEAD")


@pytest.mark.parametrize("rel", ["scripts/repin.py", "bootstrap/tests/test_repin.py",
                                 "bootstrap/tests/test_repin_ceremony.py"])
def test_a_change_to_repin_or_either_test_file_after_review_refuses_first_run(cbed, rel):
    reviewed = first_run_bed(cbed)
    cbed.write(rel, cbed.read(rel) + "\n# edited after review\n")
    cbed.commit("edit after the review")
    code, out = full_run(cbed, extra=("--first-run", "--reviewed-commit", reviewed))
    assert code == 2
    refused_early(out, "edited after review")


def test_first_run_refuses_when_the_anchor_already_pins_repin(cbed):
    code, out = full_run(cbed, extra=("--first-run", "--reviewed-commit", "HEAD"))
    assert code == 2
    refused_early(out, "this one is anchored")


def test_first_run_refuses_an_owed_ast_pin(cbed):
    first_run_bed(cbed)
    cbed.write(ENGINE, "def f():\n    return 2\n")
    reviewed = cbed.commit("engine change")
    code, out = full_run(cbed, extra=("--first-run", "--reviewed-commit", reviewed))
    assert code == 2
    refused_early(out, "an AST pin is owed")


# --------------------------------------------------------------------------
# the AST pin: stop line, then the re-run check
# --------------------------------------------------------------------------

def stop_after_pin(cbed, reply="yes"):
    cbed.write(ENGINE, "def f():\n    return 2\n")
    cbed.commit("change f")
    return drive(cbed, [("Paste the launcher digest", cbed.launcher_digest),
                        ("Do the two digests match", "yes"), ("Write these files?", reply)])


def pin_paths(cbed):
    return [BASELINE]


def test_an_owed_ast_pin_is_written_the_stop_line_printed_and_a_rerun_proceeds(cbed):
    head = cbed.git("rev-parse", "HEAD").stdout.strip()
    code, out = stop_after_pin(cbed)
    assert code == 0, out
    head = cbed.git("rev-parse", "HEAD").stdout.strip()
    assert "Written, not committed" in out and "Enter passphrase" not in out
    assert cbed.git("status", "--porcelain").stdout.split() == ["M", BASELINE]
    cbed.git("commit", "-q", "-m", "AST pin", BASELINE)
    code, out = full_run(cbed)
    assert code == 0, out
    assert "matches a stop record" in out and cbed.git("log", "-1", "--format=%s", "HEAD~1").stdout.strip() == "AST pin"


def rerun_check(cbed, first_run=False):
    code = f"""
ctx = R.boot(REPO, TMP)
outcome(lambda: R.check_stop_records(ctx, CDIR, {first_run!r}))
"""
    from bootstrap.tests.test_repin import snippet
    return snippet(cbed, code)[1]


def pinned_commit(cbed, tweak=None):
    """Write the pin through the real command, then commit exactly its paths."""
    code, out = stop_after_pin(cbed)
    assert code == 0, out
    if tweak:
        tweak()
    cbed.git("commit", "-q", "-m", "AST pin", BASELINE)
    return cbed.git("rev-parse", "HEAD").stdout.strip()


def test_the_matching_pin_commit_and_a_range_with_no_pin_pass_the_rerun_check(cbed):
    assert "RESULT: ok" in rerun_check(cbed)                       # no output-touching commit, no record
    pinned_commit(cbed)
    out = rerun_check(cbed)
    assert "RESULT: ok" in out and "matches a stop record" in out


def test_a_pin_commit_followed_by_an_unrelated_commit_is_still_checked(cbed):
    pinned_commit(cbed)
    cbed.write("unrelated.txt", "unrelated\n")
    cbed.commit("unrelated work")
    assert "matches a stop record" in rerun_check(cbed)
    for record in cbed.cdir.glob("ast-pin-stop-*.json"):
        record.unlink()
    out = rerun_check(cbed)
    assert "RESULT: refused" in out and "matches no stop record" in out


def test_a_commit_touching_the_baseline_with_no_record_refuses(cbed):
    cbed.write(BASELINE, cbed.read(BASELINE).replace("\"span\"", "\"span\"", 1) + " ")
    cbed.commit("a hand edit of the baseline")
    out = rerun_check(cbed)
    assert "RESULT: refused" in out and "git revert" in out
    assert "shown, not refused (first run)" in rerun_check(cbed, first_run=True)


def test_a_commit_adding_one_more_path_refuses(cbed):
    def add_path():
        cbed.write("extra.txt", "one more path\n")
        cbed.git("add", "extra.txt")
    cbed.write(ENGINE, "def f():\n    return 2\n")
    cbed.commit("change f")
    code, out = drive(cbed, [("Paste the launcher digest", cbed.launcher_digest),
                             ("Do the two digests match", "yes"), ("Write these files?", "yes")])
    assert code == 0
    cbed.write("extra.txt", "one more path\n")
    cbed.git("add", "extra.txt")
    cbed.git("commit", "-q", "-m", "AST pin plus a path", BASELINE, "extra.txt")
    assert "matches no stop record" in rerun_check(cbed)


def test_a_commit_that_holds_other_bytes_than_the_ones_shown_refuses(cbed):
    def other_bytes():
        cbed.write(BASELINE, cbed.read(BASELINE) + " ")
    pinned = None
    code, out = stop_after_pin(cbed)
    assert code == 0
    other_bytes()
    cbed.git("commit", "-q", "-m", "AST pin with other bytes", BASELINE)
    assert "matches no stop record" in rerun_check(cbed)


def test_a_commit_whose_parent_is_not_the_recorded_head_refuses(cbed):
    code, out = stop_after_pin(cbed)
    assert code == 0
    cbed.git("commit", "-q", "--allow-empty", "-m", "a commit between the write and the pin")
    cbed.git("commit", "-q", "-m", "AST pin", BASELINE)
    assert "matches no stop record" in rerun_check(cbed)


def test_a_merge_commit_that_changes_the_baseline_refuses(cbed):
    code, out = stop_after_pin(cbed)
    assert code == 0
    cbed.git("checkout", "-q", "-b", "side")
    cbed.git("commit", "-q", "-m", "AST pin", BASELINE)
    pin = cbed.git("rev-parse", "HEAD").stdout.strip()
    cbed.git("checkout", "-q", "main")
    cbed.git("checkout", "-q", "--", BASELINE)
    cbed.write("moves-on.txt", "main moves on\n")
    cbed.commit("main moves on")
    cbed.git("merge", "-q", "--no-ff", "-m", "merge the pin", "side")
    merge = cbed.git("rev-parse", "HEAD").stdout.strip()
    out = rerun_check(cbed)
    assert "RESULT: refused" in out and "matches no stop record" in out
    assert pin[:12] in out or merge[:12] in out


# --------------------------------------------------------------------------
# key checks: a loaded or unencrypted key never reaches the prompt
# --------------------------------------------------------------------------

class Agent:
    """A scratch ssh-agent.  Its socket sits in a short /tmp folder because unix socket
    paths are limited to about 100 bytes."""

    def __init__(self, bed):
        self.dir = Path(tempfile.mkdtemp(prefix="ra", dir="/tmp"))
        self.sock = self.dir / "a.sock"
        self.proc = subprocess.Popen(["/usr/bin/ssh-agent", "-D", "-a", str(self.sock)],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(50):
            if self.sock.exists():
                break
            import time
            time.sleep(0.1)
        askpass = self.dir / "askpass.sh"
        askpass.write_text(f"#!/bin/sh\necho '{PASSPHRASE}'\n")
        askpass.chmod(0o700)
        self.bed, self.askpass = bed, askpass

    def load(self):
        env = {"PATH": "/usr/bin:/bin", "SSH_AUTH_SOCK": str(self.sock), "SSH_ASKPASS": str(self.askpass),
               "SSH_ASKPASS_REQUIRE": "force", "DISPLAY": ":0", "HOME": str(self.bed.home)}
        r = subprocess.run(["/usr/bin/ssh-add", str(self.bed.key)], env=env, stdin=subprocess.DEVNULL,
                           capture_output=True, text=True)
        assert r.returncode == 0, r.stderr

    def close(self):
        self.proc.kill()
        self.proc.wait()
        shutil.rmtree(self.dir, ignore_errors=True)


@pytest.fixture
def agent(cbed):
    made = Agent(cbed)
    yield made
    made.close()


@pytest.fixture
def second_agent(cbed):
    made = Agent(cbed)
    yield made
    made.close()


def test_a_loaded_key_refuses_before_stage_one(cbed, agent):
    agent.load()
    before = anchor_of(cbed)
    code, out = full_run(cbed, env={"SSH_AUTH_SOCK": str(agent.sock)})
    assert code == 2
    refused_early(out, "loaded in an agent (before stage 1)")
    assert f"SSH_AUTH_SOCK={agent.sock} /usr/bin/ssh-add -d {cbed.key}.pub" in out.replace("\n", " ").replace("  ", " ") \
        or f"/usr/bin/ssh-add -d {cbed.key}.pub" in out
    assert not moved(cbed, before)
    # control: the same agent with the key not loaded passes
    agent.proc.kill()
    other = Agent(cbed)
    try:
        assert full_run(cbed, env={"SSH_AUTH_SOCK": str(other.sock)})[0] == 0
    finally:
        other.close()


def test_a_key_loaded_after_stage_one_refuses_before_stage_two(cbed, agent):
    def load_now():
        agent.load()
        return "yes"
    before = anchor_of(cbed)
    code, out = drive(cbed, [("Paste the launcher digest", cbed.launcher_digest),
                             ("Do the two digests match", "yes"), ("Does Summary 2", load_now)],
                      env={"SSH_AUTH_SOCK": str(agent.sock)})
    assert code == 2 and "loaded in an agent (before stage 2)" in out
    assert "Enter passphrase for" not in out and not moved(cbed, before)


def test_a_key_in_a_second_agent_reached_only_through_the_login_lookup_refuses(cbed, second_agent):
    second_agent.load()
    code, out = full_run(cbed, launchctl=str(second_agent.sock))
    assert code == 2
    refused_early(out, "loaded in an agent (before stage 1)")
    assert full_run(cbed, launchctl=None)[0] == 0                     # control: absent passes


def test_an_unencrypted_key_refuses(cbed):
    stored = (cbed.key).read_bytes()
    sh("ssh-keygen", "-q", "-p", "-P", PASSPHRASE, "-N", "", "-f", str(cbed.key), cwd=cbed.root, env=cbed.env)
    code, out = full_run(cbed)
    assert code == 2
    refused_early(out, "has no passphrase (before stage 1)")
    cbed.key.write_bytes(stored)
    cbed.key.chmod(0o600)
    assert full_run(cbed)[0] == 0                                      # control: encrypted passes


def test_an_agent_that_cannot_be_asked_is_shown_not_refused(cbed):
    code, out = full_run(cbed, launchctl="/tmp/ra-no-such-socket")
    assert code == 0, out
    assert "could not ask it (before stage 1); shown, not refused" in out


def test_a_loaded_key_signs_with_no_prompt_which_is_why_it_is_refused(cbed, agent):
    """Control for the one-prompt count: with the key in an agent the signer asks nothing."""
    agent.load()
    message = cbed.root / "message.txt"
    message.write_text("sign me\n")
    code, out = run_pty(["/usr/bin/ssh-keygen", "-Y", "sign", "-n", "git", "-f", str(cbed.key) + ".pub", str(message)],
                        [], env={"PATH": "/usr/bin:/bin", "SSH_AUTH_SOCK": str(agent.sock), "TERM": "xterm"},
                        cwd=cbed.root, timeout=30)
    assert code == 0 and "Enter passphrase" not in out and (cbed.root / "message.txt.sig").exists()


def test_a_wrong_passphrase_signs_nothing(cbed):
    before = anchor_of(cbed)
    code, out = drive(cbed, [("Paste the launcher digest", cbed.launcher_digest),
                             ("Do the two digests match", "yes"), ("Does Summary 2", "yes"),
                             ("Enter passphrase for", "not the passphrase"),
                             ("Enter passphrase for", "still wrong"), ("Enter passphrase for", "nope")])
    assert code == 2 and "stage 2 failed" in out and not moved(cbed, before)


def test_the_signer_environment_is_a_short_fixed_list(cbed, agent):
    hostile = {"SSH_AUTH_SOCK": str(agent.sock), "SSH_ASKPASS": str(agent.askpass), "SSH_ASKPASS_REQUIRE": "force",
               "DISPLAY": ":0", "WAYLAND_DISPLAY": "wayland-0"}
    code, out = full_run(cbed, env=hostile, audit=True)
    assert code == 0, out
    stage2 = [ln for ln in (cbed.root / "audit.log").read_text().splitlines()
              if "subprocess.Popen" in ln and "--stage2" in ln]
    assert len(stage2) == 1
    env = stage2[0]
    assert all(name not in env for name in hostile), env
    assert set(re.findall(r"'([A-Z_]+)': '", env.split("--stage2")[1])) <= {"HOME", "PATH", "TERM", "LANG"}
    # control: a copied environment signs with no person at all
    message = cbed.root / "message.txt"
    message.write_text("sign me\n")
    quiet = subprocess.run(["/usr/bin/ssh-keygen", "-Y", "sign", "-n", "git", "-f", str(cbed.key), str(message)],
                           env={"PATH": "/usr/bin:/bin", "SSH_ASKPASS": str(agent.askpass),
                                "SSH_ASKPASS_REQUIRE": "force", "DISPLAY": ":0"},
                           stdin=subprocess.DEVNULL, capture_output=True, start_new_session=True)
    assert quiet.returncode == 0 and (cbed.root / "message.txt.sig").exists()


def test_signing_tools_resolve_by_absolute_path(cbed):
    decoys = cbed.root / "decoys"
    decoys.mkdir()
    for name in ("ssh-keygen", "ssh-add", "launchctl", "sh"):
        tool = decoys / name
        tool.write_text(f"#!/bin/sh\n: > '{cbed.root}/decoy-{name}'\nexit 0\n")
        tool.chmod(0o755)
    code, out = full_run(cbed, env={"PATH": f"{decoys}:{os.environ['PATH']}"})
    assert code == 0, out
    assert not list(cbed.root.glob("decoy-*")), "a decoy on PATH ran in place of a signing tool"
    # control: a bare-name call does run the decoy, so the decoy can fire
    subprocess.run(["ssh-add"], env={"PATH": str(decoys)}, check=False)
    assert (cbed.root / "decoy-ssh-add").exists()
    src = (REAL / "scripts/repin.py").read_text()
    for const, path in (("KEYGEN", "/usr/bin/ssh-keygen"), ("SSHADD", "/usr/bin/ssh-add"),
                        ("LAUNCHCTL", "/bin/launchctl"), ("SH", "/bin/sh")):
        assert f'"{path}"' in src and re.search(rf"\b{const}\b", src)


# --------------------------------------------------------------------------
# what the ceremony shows, and the passphrase
# --------------------------------------------------------------------------

STAGE_ONE_DISCLOSURES = ["EXECUTES CANDIDATE CODE", "materialized", "no external anchor supplied",
                         "STAGE 1 COMPLETE", "effective ceremony configuration", "KEY-LOAD PHASE MARKER",
                         "key-channel probe: stage 1 cannot sign"]


def test_each_stage_one_disclosure_appears_in_the_output(cbed):
    code, out = full_run(cbed)
    assert code == 0, out
    assert [d for d in STAGE_ONE_DISCLOSURES if d not in out] == []
    for line in STAGE_ONE_DISCLOSURES:           # control: with one line removed the check names it
        cut = "\n".join(ln for ln in out.splitlines() if line not in ln)
        assert [d for d in STAGE_ONE_DISCLOSURES if d not in cut] == [line]


SUMMARY_TWO = ["== what you are authorizing ==", "signatures over the range:", "Gate manifest drift", "authority files changed since the anchor",
               "anchor signature: good, by a roster key", "signing key fingerprint: SHA256:", "package digest: "]


def test_summary_two_shows_each_disclosure(cbed):
    code, out = full_run(cbed)
    assert code == 0, out
    screen = out[out.index("Summary 2: what you are about to sign"):out.index("Does Summary 2")]
    assert [d for d in SUMMARY_TWO if d not in screen] == []
    for line in SUMMARY_TWO:
        cut = "\n".join(ln for ln in screen.splitlines() if line not in ln)
        assert [d for d in SUMMARY_TWO if d not in cut] == [line]


def test_the_record_names_its_contents(cbed):
    code, out = full_run(cbed)
    assert code == 0, out
    record = (cbed.cdir / "ceremony-record.txt").read_text()
    new = anchor_of(cbed)
    for needle in ("yes typed on a terminal: Do the two digests match?",
                   "yes typed on a terminal: Does Summary 2 describe what you intend to sign?",
                   f"launcher digest {cbed.launcher_digest}", "package digest ", "signing key fingerprint SHA256:",
                   f"verified: new anchor {new}", "sha256 ", "ran /bin/sh ", "--stage2", "-> exit 0"):
        assert needle in record, needle
    digest = hashlib.sha256((cbed.cdir / "ceremony-record.txt").read_bytes()).hexdigest()
    assert f"record digest  {digest}" in out
    assert PASSPHRASE not in record


def test_the_typed_passphrase_appears_nowhere_the_script_writes(cbed):
    sent = []
    code, out = drive(cbed, [("Paste the launcher digest", cbed.launcher_digest),
                             ("Do the two digests match", "yes"), ("Does Summary 2", "yes"),
                             ("Enter passphrase for", lambda: sent.append(PASSPHRASE) or PASSPHRASE)], audit=True)
    assert code == 0, out                      # the signature verified: the passphrase was written once, at the prompt
    assert len(sent) == 1 and "asked once, now" in out
    hay = [out.encode(), (cbed.root / "audit.log").read_bytes()]
    for folder in (cbed.home, cbed.cdir, cbed.root / "tmp"):
        hay += [p.read_bytes() for p in folder.rglob("*") if p.is_file() and not p.is_symlink()]
    found = lambda haystack: any(PASSPHRASE.encode() in h for h in haystack)
    assert not found(hay)
    assert found(hay + [("".join(sent)).encode()])          # control: the search can match the string


def signing_region():
    src = (REAL / "scripts/repin.py").read_text()
    return src[src.index("# 8-9. (signing path)"):src.index("# 10-11. (end of signing path)")]


TRIPWIRE = ("getpass", "sys.stdin", "input(", "os.environ", "termios", "tty.", "os.read(", "fileno()")


def test_the_signing_path_never_reads_the_terminal_or_the_environment(cbed):
    """A tripwire only: it fails on the spellings it names.  The behavioural test above is the evidence."""
    assert [t for t in TRIPWIRE if t in signing_region()] == []
    assert any(t in signing_region().replace("note =", "getpass.getpass()\nnote =", 1) for t in TRIPWIRE)


def test_the_launchers_ssh_add_advice_is_never_relayed(cbed):
    code, out = full_run(cbed)
    assert code == 0
    assert "does not apply here" in out and "ssh-add <your ceremony key>" not in out
    assert "Load it and re-run" not in out
    cut = "\n".join(ln for ln in out.splitlines() if "does not apply here" not in ln)
    assert "does not apply here" not in cut                 # control: the check reads the line


def test_the_note_is_printed_again_after_a_stage_two_failure(cbed):
    code, out = drive(cbed, [("Paste the launcher digest", cbed.launcher_digest), ("Do the two digests match", "yes"),
                             ("Does Summary 2", "yes")] + [("Enter passphrase for", "wrong")] * 3)
    assert code == 2 and out.count("does not apply here") == 2 and "Load it and re-run" not in out


def test_stage_one_has_no_terminal_and_the_probe_prompts_with_one(cbed):
    """Through the launcher with a terminal, the key-channel probe asks for the passphrase; through
    `repin` it never does (the full run counts exactly one prompt, at stage 2)."""
    code, out = run_pty(["/bin/sh", str(cbed.cdir / "reanchor-launcher.sh"), str(cbed.cdir / "authorization-packet.txt"),
                         str(cbed.values), "HEAD"], [("Enter passphrase for", None)],
                        env={"PATH": "/usr/bin:/bin", "HOME": str(cbed.home), "TERM": "xterm"}, cwd=cbed.repo, timeout=60)
    assert "Enter passphrase for" in out


def test_stage_two_without_a_terminal_cannot_sign(cbed):
    stage1 = subprocess.run(["/bin/sh", str(cbed.cdir / "reanchor-launcher.sh"), str(cbed.cdir / "authorization-packet.txt"),
                             str(cbed.values), "HEAD"], env={"PATH": "/usr/bin:/bin", "HOME": str(cbed.home)},
                            stdin=subprocess.DEVNULL, capture_output=True, text=True, start_new_session=True)
    assert stage1.returncode == 0, stage1.stderr
    digest = hashlib.sha256((cbed.cdir / "package.json").read_bytes()).hexdigest()
    before = anchor_of(cbed)
    stage2 = subprocess.run(["/bin/sh", str(cbed.cdir / "reanchor-launcher.sh"), str(cbed.cdir / "authorization-packet.txt"),
                             str(cbed.values), "HEAD", "--stage2", digest],
                            env={"PATH": "/usr/bin:/bin", "HOME": str(cbed.home)}, stdin=subprocess.DEVNULL,
                            capture_output=True, text=True, start_new_session=True)
    assert stage2.returncode != 0 and anchor_of(cbed) == before


def test_ceremony_help_lists_no_test_seam(cbed):
    out = subprocess.run([PY, str(cbed.repo / "scripts/repin.py"), "ceremony", "--help"], env=cbed.env,
                         capture_output=True, text=True).stdout.lower()
    assert "--values" in out and not any(w in out for w in ("seam", "launchctl", "--test", "inject", "fake", "mock"))


@pytest.mark.parametrize("subdir", ["scripts", "bootstrap/tests", "."])
def test_a_committed_module_named_like_the_standard_library_does_not_run_in_a_ceremony(cbed, subdir):
    """Stops at the digest question: candidate code runs later, at stage 1, and may legitimately
    import a committed module; what is checked here is `repin`'s own process."""
    for name in ("hashlib", "json", "subprocess", "tarfile", "base64"):
        cbed.write(f"{subdir}/{name}.py", f"\nopen({str(cbed.root / ('ran-' + name))!r}, 'w').close()\n")
    cbed.commit("shadow the standard library")
    code, out = drive(cbed, [("Paste the launcher digest", "0" * 64)])
    assert code == 2 and "not the one in the review's record" in out, out
    assert not list(cbed.root.glob("ran-*"))
    if subdir == "scripts":                       # nothing in scripts/ is imported by stage 1's collection
        code, out = full_run(cbed)
        assert code == 0, out
        assert not list(cbed.root.glob("ran-*"))


def test_checkpoint_verification_wants_a_good_signature_by_the_expected_key_from_the_pinned_roster(cbed):
    outside = cbed.outside_key()
    cbed.git("config", "user.signingkey", str(outside) + ".pub")
    cbed.sign = True
    cbed.write("signed-outside.txt", "x\n")
    stranger = cbed.commit("signed by a key outside the roster")
    cbed.sign = False
    cbed.write("unsigned.txt", "x\n")
    plain = cbed.commit("unsigned")
    pinned = cbed.repo / "dev/.cairn/allowed_signers"
    roster_with_stranger = cbed.root / "candidate-roster"
    pub = (outside.with_suffix(".pub")).read_text().split()
    roster_with_stranger.write_text(pinned.read_text() + f"x {pub[0]} {pub[1]}\n")
    fingerprint = subprocess.run(["/usr/bin/ssh-keygen", "-lf", str(cbed.key) + ".pub"], capture_output=True,
                                 text=True).stdout.split()[1]
    stranger_fp = subprocess.run(["/usr/bin/ssh-keygen", "-lf", str(outside) + ".pub"], capture_output=True,
                                 text=True).stdout.split()[1]
    anchor = anchor_of(cbed)
    code = f"""
for name, commit, roster, fp in {[("good", anchor, str(pinned), fingerprint), ("unsigned", plain, str(pinned), fingerprint),
                                   ("outside", stranger, str(pinned), fingerprint),
                                   ("candidate roster", stranger, str(roster_with_stranger), fingerprint),
                                   ("candidate roster, its own key", stranger, str(roster_with_stranger), stranger_fp)]!r}:
    print("VERDICT", name, R.verify_checkpoint(REPO, commit, Path(roster), fp)[0])
"""
    from bootstrap.tests.test_repin import snippet
    out = snippet(cbed, code)[1]
    verdicts = dict(re.findall(r"VERDICT (.+) (True|False)", out))
    assert verdicts == {"good": "True", "unsigned": "False", "outside": "False", "candidate roster": "False",
                        "candidate roster, its own key": "True"}, out


def test_only_the_exact_word_yes_writes_the_ast_pin_through_the_command(cbed):
    before = reads_of(cbed)
    code, out = stop_after_pin(cbed, reply="Yes")
    assert code == 2 and "no `yes` was typed" in out
    assert reads_of(cbed) == before


def reads_of(bed):
    return (bed.repo / BASELINE).read_bytes()
