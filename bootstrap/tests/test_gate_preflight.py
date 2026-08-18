"""Behavioural tests for `_gate_preflight` (plan `gate-reanchor-preflight`).

Every refusal here is proved **non-vacuous** by construction: each test builds the
state that must refuse and asserts the specific finding, and the accompanying
"clean" case asserts the same check stays silent. Two properties this file
deliberately does **not** assert, because the mechanism does not provide them and
a test claiming otherwise is worse than no test (security review SR7 / SR10):

* that candidate collection cannot reach the real repository -- the evidence stage
  is best-effort isolation under an accepted trusted-contributor residual;
* that a bundle is mechanically single-use.
"""
from __future__ import annotations

import ast
import contextlib
import io
import json
import re
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from bootstrap.tests import _gate_manifest as G
from bootstrap.tests import _gate_preflight as P

_REPO = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _run(*args: str, cwd: Path, env: dict | None = None):
    return subprocess.run(args, cwd=str(cwd), capture_output=True, text=True,
                          check=False, env=env)


def _repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    _run("git", "init", "-q", ".", cwd=r)
    _run("git", "config", "user.email", "m@example", cwd=r)
    _run("git", "config", "user.name", "M", cwd=r)
    return r


def _commit(repo: Path, message: str = "c") -> str:
    _run("git", "add", "-A", cwd=repo)
    _run("git", "commit", "-q", "--allow-empty", "-m", message, cwd=repo)
    return _run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()


def _write(repo: Path, rel: str, text: str = "x\n") -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _closure_repo(tmp_path: Path) -> tuple[Path, str]:
    """A repo holding every declared authority-closure member, committed."""
    repo = _repo(tmp_path)
    for rel in P.declared_authority_closure():
        _write(repo, rel, f"# {rel}\n")
    anchor = _commit(repo, "anchor")
    return repo, anchor


def _blob_sha(repo: Path, commit: str, rel: str) -> str:
    """The SHA-256 of a path's bytes at a commit, read from the object store."""
    import hashlib
    blob = subprocess.run(["git", "-C", str(repo), "cat-file", "blob",
                           f"{commit}:{rel}"], capture_output=True, check=True)
    return hashlib.sha256(blob.stdout).hexdigest()


def _findings(report: P.Report, code: str) -> list[P.Finding]:
    return [f for f in report.findings if f.code == code]


# --------------------------------------------------------------------------
# read-only invariant (plan finding GPR4)
# --------------------------------------------------------------------------

class TestReadOnlyByConstruction:
    """The invariant is enforced at the call site, not asserted by a snapshot.

    A `git status --porcelain` snapshot cannot see ignored files, `.git/config`,
    hooks, or arbitrary refs -- the same observability limitation that produced
    SR5. So the guarantee lives in `_git`'s allowlist instead.
    """

    @pytest.mark.parametrize("bad", ["commit", "update-ref", "checkout", "push",
                                     "add", "reset", "gc", "config"])
    def test_mutating_subcommands_are_refused(self, bad, tmp_path):
        repo = _repo(tmp_path)
        with pytest.raises(P.PreflightError, match="read-only"):
            P._git(bad, "--help", repo=repo)

    def test_readonly_subcommands_are_permitted(self, tmp_path):
        repo = _repo(tmp_path)
        _commit(repo)
        assert P._git("rev-parse", "HEAD", repo=repo).returncode == 0

    def test_empty_invocation_refused(self, tmp_path):
        with pytest.raises(P.PreflightError):
            P._git(repo=_repo(tmp_path))


# --------------------------------------------------------------------------
# index-validated frozen surface (security review SR5)
# --------------------------------------------------------------------------

class TestFrozenSurfaceIsIndexValidated:
    """`_frozen_files()` globs the filesystem and `_sha256` follows symlinks, so
    membership must be checked against the index, not against `git status`."""

    def _surface_report(self, repo: Path, monkeypatch, names: list[str]):
        monkeypatch.setattr(P.G, "_frozen_files", lambda r=None: names)
        report = P.Report()
        P.check_frozen_surface(report, repo=repo)
        return report

    def test_ignored_file_inside_the_surface_refuses(self, tmp_path, monkeypatch):
        repo = _repo(tmp_path)
        _write(repo, ".gitignore", "secret.py\n")
        _write(repo, "secret.py", "x = 1\n")
        _commit(repo)
        report = self._surface_report(repo, monkeypatch, ["secret.py"])
        assert any("absent from the git index" in f.message
                   for f in _findings(report, "SURFACE"))

    def test_tracked_symlink_inside_the_surface_refuses(self, tmp_path,
                                                        monkeypatch):
        repo = _repo(tmp_path)
        (repo / "target.py").write_text("real\n", encoding="utf-8")
        (repo / "link.py").symlink_to("target.py")
        _commit(repo)
        report = self._surface_report(repo, monkeypatch, ["link.py"])
        assert any("not a regular blob" in f.message
                   for f in _findings(report, "SURFACE"))

    def test_untracked_file_outside_the_surface_does_not_refuse(
            self, tmp_path, monkeypatch):
        """The 2026-08-03 defect, pinned: a whole-tree cleanliness test refused
        on `.claude/` and a measurement snapshot, neither of which can reach the
        manifest."""
        repo = _repo(tmp_path)
        _write(repo, "tracked.py", "x = 1\n")
        _commit(repo)
        _write(repo, "notes/scratch.txt", "untracked, outside the surface\n")
        report = self._surface_report(repo, monkeypatch, ["tracked.py"])
        assert _findings(report, "SURFACE") == []

    def test_clean_surface_is_silent(self, tmp_path, monkeypatch):
        repo = _repo(tmp_path)
        _write(repo, "ok.py", "x = 1\n")
        _commit(repo)
        assert self._surface_report(repo, monkeypatch, ["ok.py"]).findings == []


# --------------------------------------------------------------------------
# the preflight-authority closure (plan finding GPR1)
# --------------------------------------------------------------------------

class TestAuthorityClosure:
    """The old six modules do not cover the checker or the invocation source.
    Neither `REANCHOR_RUNBOOK.md` nor the allowed-signers file is in
    `_frozen_files()` at all, so the closure pins them explicitly."""

    def test_unchanged_closure_is_silent(self, tmp_path):
        repo, anchor = _closure_repo(tmp_path)
        report = P.Report()
        P.check_authority_closure(anchor, report, repo=repo)
        assert _findings(report, "CLOSURE") == []

    @pytest.mark.parametrize("member", [
        "bootstrap/tests/_gate_preflight.py",   # the checker itself
        "bootstrap/REANCHOR_RUNBOOK.md",        # the invocation source
        "dev/.cairn/allowed_signers",           # the pinned key set
    ])
    def test_a_changed_member_routes_to_review(self, tmp_path, member):
        """Each is mutated independently, per the finding's satisfier."""
        repo, anchor = _closure_repo(tmp_path)
        _write(repo, member, "# tampered\n")
        _commit(repo, "tamper")
        report = P.Report()
        P.check_authority_closure(anchor, report, repo=repo)
        assert any(member in f.message and f.level == "review"
                   for f in _findings(report, "CLOSURE"))

    def test_member_missing_from_the_index_routes_to_review(self, tmp_path):
        repo, anchor = _closure_repo(tmp_path)
        _write(repo, ".gitignore", "dev/.cairn/allowed_signers\n")
        _run("git", "rm", "--cached", "-q", "dev/.cairn/allowed_signers",
             cwd=repo)
        _commit(repo, "untrack")
        report = P.Report()
        P.check_authority_closure(anchor, report, repo=repo)
        assert any("not in the git index" in f.message
                   for f in _findings(report, "CLOSURE"))

    def test_symlinked_member_routes_to_review(self, tmp_path):
        repo, anchor = _closure_repo(tmp_path)
        member = repo / "dev/.cairn/allowed_signers"
        member.unlink()
        member.symlink_to("/etc/hosts")
        _commit(repo, "symlink the key set")
        report = P.Report()
        P.check_authority_closure(anchor, report, repo=repo)
        assert any("not a regular blob" in f.message
                   for f in _findings(report, "CLOSURE"))

    def test_an_undeclared_import_routes_to_review(self, tmp_path, monkeypatch):
        """The 'extra member' half: a new dependency must not slip in uncovered."""
        repo, anchor = _closure_repo(tmp_path)
        monkeypatch.setattr(
            P, "_imported_local_modules",
            lambda: set(P.declared_authority_closure())
            | {"bootstrap/tests/_sneaky_helper.py"})
        report = P.Report()
        P.check_authority_closure(anchor, report, repo=repo)
        assert any("outside the declared authority closure" in f.message
                   for f in _findings(report, "CLOSURE"))

    def test_the_real_closure_covers_the_real_import_graph(self):
        """Non-vacuity for the check above, against the live module: everything
        this checker actually imports is declared."""
        assert P._imported_local_modules() <= set(P.declared_authority_closure())


# --------------------------------------------------------------------------
# the expiry tripwire -- signature verification
# --------------------------------------------------------------------------

def _keypair(tmp_path: Path, name: str) -> Path:
    key = tmp_path / name
    subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-C",
                    f"{name}@example", "-f", str(key)], check=True)
    return key


def _signing_repo(tmp_path: Path):
    """A repo with SSH signing configured and one pinned principal."""
    repo = _repo(tmp_path)
    key = _keypair(tmp_path, "maint")
    signers = tmp_path / "allowed_signers"
    keydata = " ".join(key.with_suffix(".pub").read_text().split()[:2])
    signers.write_text(f"m@example {keydata}\n", encoding="utf-8")
    _write(repo, "dev/.cairn/allowed_signers", signers.read_text())
    for k, v in (("gpg.format", "ssh"),
                 ("user.signingkey", str(key.with_suffix(".pub"))),
                 ("gpg.ssh.allowedSignersFile", str(signers))):
        _run("git", "config", k, v, cwd=repo)
    return repo, key, signers


def _signed_commit(repo: Path, message: str) -> str:
    _run("git", "add", "-A", cwd=repo)
    _run("git", "commit", "-q", "-S", "--allow-empty", "-m", message, cwd=repo)
    return _run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()




class TestUnsignedRangeReachesACheckpoint:
    """Chunk C4 / acceptance criterion 1, which had no test until now.

    *"No range-signature refusal. Unsigned agent commits are the normal format;
    authorization occurs only at a signed checkpoint. Proven on the public path
    with a mixed range."*

    The suite used to pin the **opposite** behaviour (`TestSigningTripwire`,
    deleted with the epoch it tested), so criterion 1 could be unmet with the
    suite fully green -- and it was. These nodes are the criterion's proof, and
    the first is deliberately a *mixed* range: all-unsigned would also pass
    against a checker that simply skipped empty ranges.
    """

    def _mixed(self, tmp_path):
        """anchor -> unsigned -> signed -> unsigned, i.e. genuinely mixed."""
        repo, key, signers = _signing_repo(tmp_path)
        anchor = _signed_commit(repo, "anchor")
        _run("git", "commit", "-q", "--allow-empty", "-m", "agent work 1",
             cwd=repo)
        _signed_commit(repo, "an incidentally signed one")
        _run("git", "commit", "-q", "--allow-empty", "-m", "agent work 2",
             cwd=repo)
        head = _run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
        return repo, anchor, head

    def test_a_mixed_range_produces_no_signing_finding(self, tmp_path):
        repo, anchor, head = self._mixed(tmp_path)
        report = P.Report()

        P.check_signatures(anchor, head, report, repo=repo)

        assert _findings(report, "SIGNING") == [], (
            "an unsigned intermediate commit is the normal agent format; a "
            "range-signature finding is the retired behaviour")
        assert report.facts["signing"]["epoch"] is None

    def test_the_range_is_actually_mixed(self, tmp_path):
        """Non-vacuity. If the fixture were all-signed, the node above would
        pass against a checker that still refused unsigned commits."""
        repo, anchor, head = self._mixed(tmp_path)
        codes = _run("git", "log", "--format=%G?", f"{anchor}..{head}",
                     cwd=repo).stdout.split()
        assert "N" in codes and "G" in codes, codes

    def test_the_census_still_counts_them_as_diagnostics(self, tmp_path):
        """Retiring the verdict must not retire the information."""
        repo, anchor, head = self._mixed(tmp_path)
        census = P._signature_census(anchor, head, repo=repo)
        assert census["total"] == 3
        assert census["unsigned"] == 2
        assert census["good"] == 1

    def test_no_candidate_editable_epoch_constant_survives(self):
        """R1's proof obligation, worded precisely: *no* candidate-editable
        epoch exists after this change, so self-grandfathering is eliminated
        rather than renamed. Asserted on the module's executable bytes, since
        the retirement docstrings legitimately mention the old name."""
        import ast as _ast
        src = (P._REPO / "bootstrap/tests/_gate_preflight.py").read_text(
            encoding="utf-8")
        for node in _ast.walk(_ast.parse(src)):
            if isinstance(node, _ast.Name) and node.id == "_SIGNING_EPOCH":
                raise AssertionError(
                    f"a signing-epoch constant is live again at line "
                    f"{node.lineno}; it is candidate-editable by construction")
        assert not hasattr(P, "_SIGNING_EPOCH")


# --------------------------------------------------------------------------
# anchor position
# --------------------------------------------------------------------------

class TestAnchorPosition:
    def test_anchor_equal_to_head_refuses(self, tmp_path):
        repo = _repo(tmp_path)
        head = _commit(repo)
        report = P.Report()
        P.check_anchor_position(head, head, report, repo=repo)
        assert any("nothing to bless" in f.message
                   for f in _findings(report, "ANCHOR"))

    def test_orphaned_anchor_refuses(self, tmp_path):
        repo = _repo(tmp_path)
        base = _commit(repo, "base")
        _run("git", "checkout", "-q", "-b", "side", base, cwd=repo)
        orphan = _commit(repo, "side branch")
        _run("git", "checkout", "-q", "master", cwd=repo)
        head = _commit(repo, "main line")
        report = P.Report()
        P.check_anchor_position(orphan, head, report, repo=repo)
        assert any("not an ancestor" in f.message
                   for f in _findings(report, "ANCHOR"))

    def test_ancestor_anchor_is_silent(self, tmp_path):
        repo = _repo(tmp_path)
        anchor = _commit(repo, "anchor")
        head = _commit(repo, "later")
        report = P.Report()
        P.check_anchor_position(anchor, head, report, repo=repo)
        assert _findings(report, "ANCHOR") == []


# --------------------------------------------------------------------------
# the evidence artifact, parsed fail-closed (plan finding GPR3)
# --------------------------------------------------------------------------

def _evidence(candidate: str, manifest: dict | None = None,
              interpreter: str = "3.13.13", schema: int = P.EVIDENCE_SCHEMA):
    manifest = manifest if manifest is not None else {"frozen_files": {}}
    body = json.dumps(manifest, indent=2, sort_keys=True).encode() + b"\n"
    return json.dumps({
        "schema": schema,
        "candidate_sha": candidate,
        "interpreter": interpreter,
        "manifest": manifest,
        "manifest_sha256": P._sha256_bytes(body),
    })


class TestEvidenceIsUntrustedInput:
    _SHA = "a" * 40

    def test_wellformed_evidence_parses(self):
        assert P.parse_evidence(_evidence(self._SHA))["candidate_sha"] == self._SHA

    @pytest.mark.parametrize("text", ["", "not json", "[]", "null", "123"])
    def test_malformed_evidence_is_fail_closed(self, text):
        with pytest.raises(P.PreflightError):
            P.parse_evidence(text)

    def test_unknown_schema_is_fail_closed(self):
        with pytest.raises(P.PreflightError, match="schema"):
            P.parse_evidence(_evidence(self._SHA, schema=99))

    @pytest.mark.parametrize("missing", ["candidate_sha", "interpreter",
                                         "manifest", "manifest_sha256"])
    def test_missing_fields_are_fail_closed(self, missing):
        data = json.loads(_evidence(self._SHA))
        del data[missing]
        with pytest.raises(P.PreflightError, match=missing):
            P.parse_evidence(json.dumps(data))

    def test_short_candidate_sha_is_fail_closed(self):
        with pytest.raises(P.PreflightError, match="candidate_sha"):
            P.parse_evidence(_evidence("abc123"))

    def test_wrong_candidate_refuses(self):
        report = P.Report()
        P.check_evidence(P.parse_evidence(_evidence(self._SHA)), "b" * 40, report)
        assert any("wrong-candidate" in f.message
                   for f in _findings(report, "EVIDENCE"))

    def test_tampered_manifest_body_refuses(self):
        data = json.loads(_evidence(self._SHA))
        data["manifest"] = {"frozen_files": {"injected": "x"}}
        report = P.Report()
        P.check_evidence(P.parse_evidence(json.dumps(data)), self._SHA, report)
        assert any("digest does not match" in f.message
                   for f in _findings(report, "EVIDENCE"))

    def test_off_canon_interpreter_refuses(self):
        report = P.Report()
        P.check_evidence(P.parse_evidence(_evidence(self._SHA,
                                                    interpreter="3.12.9")),
                         self._SHA, report)
        assert any("3.12.9" in f.message for f in _findings(report, "EVIDENCE"))

    def test_matching_evidence_is_silent(self):
        report = P.Report()
        P.check_evidence(P.parse_evidence(_evidence(self._SHA)), self._SHA,
                         report)
        assert _findings(report, "EVIDENCE") == []


# --------------------------------------------------------------------------
# interpreter + worktree cleanliness
# --------------------------------------------------------------------------

class TestInterpreterAndWorktree:
    def test_canonical_interpreter_is_silent(self):
        report = P.Report()
        P.check_interpreter(report)
        expected = f"{P._CANONICAL_PY[0]}.{P._CANONICAL_PY[1]}"
        if sys.version_info[:2] == P._CANONICAL_PY:
            assert _findings(report, "INTERPRETER") == []
        else:  # the suite is pinned to the canonical minor; guard anyway
            assert any(expected in f.message
                       for f in _findings(report, "INTERPRETER"))

    def test_uncommitted_tracked_change_refuses(self, tmp_path):
        repo = _repo(tmp_path)
        _write(repo, "f.txt", "one\n")
        _commit(repo)
        _write(repo, "f.txt", "two\n")
        report = P.Report()
        P.check_tracked_clean(report, repo=repo)
        assert _findings(report, "WORKTREE")

    def test_untracked_file_alone_does_not_refuse(self, tmp_path):
        """Untracked state is the frozen-surface check's business, not this one."""
        repo = _repo(tmp_path)
        _write(repo, "f.txt", "one\n")
        _commit(repo)
        _write(repo, "untracked.txt", "new\n")
        report = P.Report()
        P.check_tracked_clean(report, repo=repo)
        assert _findings(report, "WORKTREE") == []


# --------------------------------------------------------------------------
# the CLI, exercised as a public path
# --------------------------------------------------------------------------

class TestPublicCli:
    def test_check_runs_against_the_live_repo_and_reports(self):
        """Public-path smoke: the CLI runs, and refuses rather than crashing.

        The live tree is expected to refuse until the Maintainer's first-use
        bootstrap anchors this checker, so this asserts a *reasoned* exit, not a
        pass."""
        r = subprocess.run(
            [sys.executable, str(_REPO / "bootstrap/tests/_gate_preflight.py"),
             "check"],
            capture_output=True, text=True, check=False, cwd=str(_REPO))
        assert r.returncode in (0, 1, 2), r.stderr[-2000:]
        assert "Traceback" not in r.stderr, "must refuse cleanly, not crash"
        assert "anchor" in r.stderr
        if r.returncode == 2:
            # The live tree's anchor predates the roster commit, so the
            # anchored-roster read fail-closes. That is the first-use bootstrap
            # condition, and it must say so rather than merely erroring.
            assert "bootstrap" in r.stderr

    def test_no_flag_can_turn_a_refusal_into_a_pass(self):
        """There is deliberately no suppression switch (security review SR3)."""
        r = subprocess.run(
            [sys.executable, str(_REPO / "bootstrap/tests/_gate_preflight.py"),
             "check", "--help"],
            capture_output=True, text=True, check=False, cwd=str(_REPO))
        lowered = r.stdout.lower()
        for banned in ("--force", "--allow", "--skip", "--ignore", "--no-verify"):
            assert banned not in lowered, f"suppression flag present: {banned}"


class TestGitConfigCannotSteerTheChecker:
    """CR1's *class*, not just its instance: the checker's reading of the
    repository must not depend on candidate-controlled `.git/config`."""

    def test_non_ascii_frozen_path_is_matched_despite_quotepath(
            self, tmp_path, monkeypatch):
        """`core.quotePath` defaults to true and escapes non-ASCII paths, so an
        unpinned invocation reads `d/café.py` back as `"d/caf\\303\\251.py"` and
        falsely refuses it as absent from the index."""
        repo = _repo(tmp_path)
        _run("git", "config", "core.quotePath", "true", cwd=repo)
        _write(repo, "d/café.py", "x = 1\n")
        _commit(repo)
        monkeypatch.setattr(P.G, "_frozen_files", lambda r=None: ["d/café.py"])
        report = P.Report()
        P.check_frozen_surface(report, repo=repo)
        assert _findings(report, "SURFACE") == [], (
            "a tracked non-ASCII frozen path must not be reported absent")

    def test_pinned_config_is_applied_to_every_invocation(self, tmp_path):
        repo = _repo(tmp_path)
        _commit(repo)
        assert "core.quotePath" in P._STERILE_CONFIG
        # and it is not overridden away by a per-call config dict
        _write(repo, "d/naïve.txt", "y\n")
        _run("git", "add", "-A", cwd=repo)
        assert "d/naïve.txt" in P._index_entries(repo=repo)


# --------------------------------------------------------------------------
# FUR1 / FUR2 -- the sterile-Git launcher
#
# `_PINNED_CONFIG` pinned exactly one key and the module claimed that "closes
# the class for future call sites too". It did not. Four more channels each
# defeated a different asserted guarantee, and the write path -- which signs the
# commit and moves the trust root -- was pinning *nothing at all*.
#
# Every test below reproduces the attack first and then asserts the launcher
# defeats it. An assertion that a config key is present proves nothing about
# whether the channel it names is actually closed.
# --------------------------------------------------------------------------

def _fake_ssh_keygen(path: Path, principal: str = "m@example") -> Path:
    """A verifier that vouches for anything.

    Git asks `-Y find-principals` first and only then `-Y verify`; a fake that
    answers only the second never gets consulted, which is why an earlier
    version of this probe failed to reproduce the attack at all. The `with
    <type> key <fingerprint>` suffix matters too -- git parses it, and without
    it the status comes back `B` rather than the forged `G`.
    """
    good = (f'Good "git" signature for {principal} '
            f'with ED25519 key SHA256:AAAAfake')
    path.write_text(
        "#!/bin/sh\n"
        "for a in \"$@\"; do\n"
        "  case \"$a\" in\n"
        f"    find-principals) echo '{principal}'; exit 0;;\n"
        f"    verify) echo '{good}' >&2; exit 0;;\n"
        "  esac\n"
        "done\n"
        "exec /usr/bin/ssh-keygen \"$@\"\n", encoding="utf-8")
    path.chmod(0o755)
    return path


class TestSterileGitLauncher:

    def test_replacement_objects_cannot_substitute_the_anchored_roster(
            self, tmp_path):
        """FUR1 probe 1. `refs/replace/<anchor>` makes every read of the anchor
        return attacker content while `rev-parse` still reports the real SHA --
        so the roster looks correctly sourced and is not."""
        repo, _key, _signers = _signing_repo(tmp_path)
        _write(repo, P._ALLOWED_SIGNERS_REL, "real@example ssh-ed25519 AAAAreal\n")
        anchor = _commit(repo, "anchor")
        _write(repo, P._ALLOWED_SIGNERS_REL,
               "attacker@example ssh-ed25519 AAAAevil\n")
        evil = _commit(repo, "attacker")
        _run("git", "update-ref", f"refs/replace/{anchor}", evil, cwd=repo)

        # The attack is live: an unpinned read returns the attacker's bytes.
        assert "attacker@example" in _run(
            "git", "show", f"{anchor}:{P._ALLOWED_SIGNERS_REL}",
            cwd=repo).stdout

        with P.anchored_roster(anchor, repo=repo) as (_path, text):
            assert "real@example" in text
            assert "attacker@example" not in text

    def test_a_configured_verifier_cannot_forge_a_signature(self, tmp_path,
                                                            monkeypatch):
        """FUR1 probe 2. `gpg.ssh.program` is ordinary repository config; a fake
        made a commit signed by an unrostered key report `%G? = G` with a
        rostered-looking `%GS`."""
        repo, key, signers = _signing_repo(tmp_path)
        head = _signed_commit(repo, "base")

        outsider = _keypair(tmp_path, "outsider")
        _run("git", "config", "user.signingkey",
             str(outsider.with_suffix(".pub")), cwd=repo)
        forged = _signed_commit(repo, "signed by an outsider")
        _run("git", "config", "gpg.ssh.program",
             str(_fake_ssh_keygen(tmp_path / "fake-keygen")), cwd=repo)

        # The attack is live: git itself now reports a good signature.
        assert _run("git", "log", "-1", "--format=%G?",
                    cwd=repo).stdout.strip() == "G"

        # Asserted on the LAUNCHER, which is this class's subject and is the
        # single place every signature read passes through -- `check_signatures`
        # was retired with the epoch (Chunk B), and routing this through
        # `verify_constructed` instead would have short-circuited on its parent
        # and changed-path checks and never reached a signature at all. A test
        # that raises for the wrong reason is worse than no test here.
        sig = P._git("log", "-1", "--format=%G?%x09%GS", forged, repo=repo,
                     config={"gpg.ssh.allowedSignersFile": str(signers)})
        status, _, signer = (sig.stdout or "").strip().partition("\t")
        assert status != "G", (
            f"the launcher honoured the candidate's gpg.ssh.program: "
            f"status={status!r} signer={signer!r}")

    def test_a_configured_fsmonitor_does_not_execute(self, tmp_path):
        """FUR2. A monitor program ran during `git status` while git returned
        success, so `check` was never structurally free of candidate-configured
        execution."""
        repo = _repo(tmp_path)
        _commit(repo)
        log = tmp_path / "fsmonitor.log"
        mon = tmp_path / "fsm.sh"
        mon.write_text(f"#!/bin/sh\necho ran >> {log}\nprintf '/\\0'\n",
                       encoding="utf-8")
        mon.chmod(0o755)
        _run("git", "config", "core.fsmonitor", str(mon), cwd=repo)

        # The attack is live under an unpinned invocation.
        _run("git", "status", "--porcelain", cwd=repo)
        assert log.exists() and log.read_text().strip(), (
            "the probe must actually execute, or this test proves nothing")
        log.unlink()

        P._git("status", "--porcelain", repo=repo)
        assert not log.exists(), "the launcher let a configured program run"

    def test_a_reference_transaction_hook_cannot_move_a_third_ref(self,
                                                                  tmp_path):
        """FUR2's sharpest case: the hook's committed phase advanced a THIRD ref
        while the two-ref transaction reported `ok=True`."""
        repo, anchor, head, _epoch = _ceremony_repo(tmp_path)
        hook = repo / ".git/hooks/reference-transaction"
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text(
            "#!/bin/sh\n"
            '[ -n "${CAIRN_HOOK_GUARD:-}" ] && exit 0\n'
            "export CAIRN_HOOK_GUARD=1\n"
            '[ "$1" = committed ] && git update-ref refs/heads/third HEAD\n'
            "exit 0\n", encoding="utf-8")
        hook.chmod(0o755)

        ok, _detail = P._advance_both_refs(
            repo, "refs/heads/master", head, branch_old=head, anchor_old=anchor)

        assert ok
        third = _run("git", "rev-parse", "--verify", "-q", "refs/heads/third",
                     cwd=repo)
        assert third.returncode != 0, (
            "the hook moved a third ref during the two-ref transaction")

    def test_the_hook_probe_is_live(self, tmp_path):
        """Guards the test above: if the hook silently never fires, that test
        passes while proving nothing. Here the same hook runs unpinned."""
        repo, anchor, head, _epoch = _ceremony_repo(tmp_path)
        hook = repo / ".git/hooks/reference-transaction"
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text(
            "#!/bin/sh\n"
            '[ -n "${CAIRN_HOOK_GUARD:-}" ] && exit 0\n'
            "export CAIRN_HOOK_GUARD=1\n"
            '[ "$1" = committed ] && git update-ref refs/heads/third HEAD\n'
            "exit 0\n", encoding="utf-8")
        hook.chmod(0o755)

        _run("git", "update-ref", "refs/heads/unpinned", head, cwd=repo)
        assert _run("git", "rev-parse", "--verify", "-q", "refs/heads/third",
                    cwd=repo).returncode == 0

    def test_the_write_path_is_pinned_too(self, tmp_path):
        """`_git_write` called subprocess directly with no config at all, so the
        path that signs the commit and moves the trust root was the least
        protected in the module."""
        repo = _repo(tmp_path)
        _commit(repo)
        p = P._git_write("hash-object", "-w", "--stdin", repo=repo, stdin="x\n")
        assert p.returncode == 0
        import inspect
        src = inspect.getsource(P._git_write)
        assert "_run_git" in src and "subprocess.run" not in src

    def test_only_the_launcher_starts_git(self):
        """The guarantees hold only if there is exactly one place they are
        applied; a second call site is how `_blob_at` once bypassed the
        read-only guard."""
        import inspect
        src = inspect.getsource(P)
        assert src.count("subprocess.run(") == 4, (
            "expected exactly four: the git launcher; the evidence stage's "
            "explicitly non-authoritative producer call; the key-channel "
            "signing probe (Chunk D); and the key-channel VALIDATION probe "
            "added by security review [S1], which runs `ssh-keygen -l` over "
            "the public half to derive the fingerprint that binds the two "
            "stages to one key. The last two run the pinned `ssh-keygen` and "
            "are both guarded by `refuse_if_sealed`. This count is an "
            "inventory, not a formality -- raise it only alongside the "
            "justification for the new launcher.")

    def test_git_env_channels_are_dropped(self, monkeypatch):
        monkeypatch.setenv("GIT_DIR", "/somewhere/else/.git")
        monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
        monkeypatch.setenv("GIT_EXTERNAL_DIFF", "/bin/sh")
        env = P._sterile_env()
        # The two GIT_* the ceremony sets on purpose. Named rather than
        # prefix-matched: the point of this test is that nothing INHERITED
        # survives, and a loose filter would let an inherited one through under
        # a plausible name. `GIT_OPTIONAL_LOCKS` was added for [M2-4].
        deliberate = {"GIT_TERMINAL_PROMPT", "GIT_OPTIONAL_LOCKS"}
        assert not [k for k in env
                    if k.startswith("GIT_") and k not in deliberate]
        assert env["GIT_OPTIONAL_LOCKS"] == "0"

    def test_the_index_is_threaded_not_exported(self, monkeypatch):
        """Mutating os.environ leaked the temporary index into every unrelated
        subprocess started while it was set."""
        assert P._sterile_env("/tmp/idx")["GIT_INDEX_FILE"] == "/tmp/idx"
        assert "GIT_INDEX_FILE" not in P._sterile_env()
        import inspect
        assert "os.environ[" not in inspect.getsource(P._construct_signed_commit)


# --------------------------------------------------------------------------
# the evidence stage (Chunk B) -- non-authoritative, and honest about it
# --------------------------------------------------------------------------

_STUB_PRODUCER = '''\
import json, os, sys
json.dump({"frozen_files": {"a.py": "sha256:aa"},
           "collection": {"node_count": 1, "node_ids": ["a.py::t"]},
           "saw_dot_git": os.path.isdir(".git"),
           "saw_home": os.environ.get("HOME", "")},
          sys.stdout, indent=2, sort_keys=True)
sys.stdout.write("\\n")
'''


def _evidence_repo(tmp_path: Path, producer: str = _STUB_PRODUCER) -> Path:
    """A repo whose `_gate_manifest.py produce` is a fast stub.

    The real producer runs a full pytest collection; these tests exercise the
    stage's orchestration, not pytest.
    """
    repo = _repo(tmp_path)
    _write(repo, "bootstrap/tests/_gate_manifest.py", producer)
    _commit(repo, "stub producer")
    return repo


class TestEvidenceStage:
    def test_artifact_round_trips_and_binds_to_the_candidate(self, tmp_path):
        repo = _evidence_repo(tmp_path)
        head = _run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
        art = P.gather_evidence("HEAD", repo=repo, out=__import__("io").StringIO())
        assert art["candidate_sha"] == head
        assert art["schema"] == P.EVIDENCE_SCHEMA
        parsed = P.parse_evidence(json.dumps(art))
        report = P.Report()
        P.check_evidence(parsed, head, report)
        assert _findings(report, "EVIDENCE") == []

    def test_candidate_tree_is_materialized_without_a_git_directory(self,
                                                                    tmp_path):
        repo = _evidence_repo(tmp_path)
        art = P.gather_evidence("HEAD", repo=repo, out=__import__("io").StringIO())
        assert art["manifest"]["saw_dot_git"] is False, (
            "the producer must run against a repository-less tree")

    def test_environment_is_scrubbed_for_the_producer(self, tmp_path):
        repo = _evidence_repo(tmp_path)
        art = P.gather_evidence("HEAD", repo=repo, out=__import__("io").StringIO())
        assert art["manifest"]["saw_home"] != str(Path.home()), (
            "HOME must be redirected away from the real home directory")

    def test_residual_is_printed_and_claims_no_containment(self, tmp_path):
        repo = _evidence_repo(tmp_path)
        buf = __import__("io").StringIO()
        P.gather_evidence("HEAD", repo=repo, out=buf)
        printed = buf.getvalue()
        assert "EXECUTES CANDIDATE CODE" in printed
        assert "NOT containment" in printed
        for claim in ("filesystem access", "process creation", "network access"):
            assert claim in printed, f"residual must name {claim}"

    def test_producer_failure_is_fail_closed(self, tmp_path):
        repo = _evidence_repo(tmp_path, "import sys; sys.exit(3)\n")
        with pytest.raises(P.PreflightError, match="manifest producer failed"):
            P.gather_evidence("HEAD", repo=repo,
                              out=__import__("io").StringIO())

    def test_producer_emitting_non_json_is_fail_closed(self, tmp_path):
        repo = _evidence_repo(tmp_path, "print('not json')\n")
        with pytest.raises(P.PreflightError, match="invalid JSON"):
            P.gather_evidence("HEAD", repo=repo,
                              out=__import__("io").StringIO())

    def test_the_operator_facing_residual_makes_no_containment_claim(self):
        """Security review SR7, asserted where it actually bites.

        A file-wide prose lint was tried first and removed: it produced three
        false positives in a row -- on the ordinary verb "contain", on a wrapped
        comment that *denies* containment, and finally on this test's own name --
        and zero true positives. A grep over prose cannot distinguish a claim
        from a denial of one, and a guard that cries wolf gets bypassed, which is
        the failure mode this plan already lists under "Signals the change is
        wrong". So the property is asserted against the text the operator
        actually reads, which is where a false claim would do the damage.
        """
        residual = P._EVIDENCE_RESIDUAL
        assert "NOT containment" in residual
        assert "EXECUTES CANDIDATE CODE" in residual
        for named in ("filesystem access", "process creation", "network access"):
            assert named in residual, f"the residual must name {named}"
        # No sentence in the operator-facing text may assert containment.
        for sentence in re.split(r"(?<=[.:])\s+", residual):
            low = " ".join(sentence.lower().split())
            if "containment" in low or "contained" in low:
                assert "not containment" in low, (
                    f"residual sentence may read as a containment claim: "
                    f"{sentence.strip()!r}")


# --------------------------------------------------------------------------
# Chunks C + D -- the derived plan, and the application transaction
#
# Rewritten after the security code review. The handoff bundle is GONE as an
# authority path: `apply` re-derives everything in memory, because a bundle
# carrying its own digests is a corruption check and not tamper evidence (CR1 --
# a re-hashed tampered manifest was anchored). Both alternatives were rejected
# on external review: an out-of-band digest argument (file-write and terminal
# access are one practical authority domain on a single-user machine) and a
# signed check artifact (agents already hold the Maintainer's key, so it proves
# "someone could use this key", not "the checker produced these bytes").
# --------------------------------------------------------------------------

_CLOSURE_SRC = {rel: (_REPO / rel) for rel in P.declared_authority_closure()}




def _extract_anchored(repo: Path, dest: Path) -> Path:
    """The runbook's own extraction, run as the literal shell pipeline.

    `git archive <anchor> bootstrap/tests | tar -x -C "$T"` -- byte-for-byte the
    recorded ceremony's first step, so a change to the runbook's shape that this
    no longer matches shows up as a test edit rather than passing unnoticed.
    """
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        f"git -C {shlex.quote(str(repo))} archive {P._ANCHOR_REF} "
        f"bootstrap/tests | tar -x -C {shlex.quote(str(dest))}",
        shell=True, check=True)
    return dest / "bootstrap/tests/_gate_preflight.py"


def _ceremony_repo(tmp_path: Path):
    """A repo where the whole ceremony can actually run.

    Copies the *real* authority-closure files so the closure and authority-module
    checks compare like with like, configures SSH signing with a throwaway key,
    and pins that key in the roster at the anchor.
    """
    repo = _repo(tmp_path)
    key = _keypair(tmp_path, "maint")
    keydata = " ".join(key.with_suffix(".pub").read_text().split()[:2])

    for rel, src in _CLOSURE_SRC.items():
        if rel == P._ALLOWED_SIGNERS_REL:
            continue
        dst = repo / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
    _write(repo, "bootstrap/tests/__init__.py", "")
    _write(repo, P._ALLOWED_SIGNERS_REL, f"m@example {keydata}\n")
    _write(repo, P._MANIFEST_REL, "{}\n")
    # The REAL manifest producer runs in this fixture, so supply the two things
    # it refuses without: a non-empty pytest collection, and the AST baseline
    # keys it pins. That is what makes a true three-command integration test
    # possible (code review CR5).
    _write(repo, "bootstrap/tests/test_smoke.py",
           "def test_smoke():\n    assert True\n")
    _write(repo, "bootstrap/tests/fixtures/scaffold_ast_baseline.json",
           json.dumps({f"Assign:{sym}": {"digest": f"d{i}"}
                       for i, sym in enumerate(P.G.MAPPING_SYMBOLS_PHASES)},
                      indent=2) + "\n")

    for k, v in (("gpg.format", "ssh"),
                 ("user.signingkey", str(key.with_suffix(".pub"))),
                 ("gpg.ssh.allowedSignersFile",
                  str(repo / P._ALLOWED_SIGNERS_REL))):
        _run("git", "config", k, v, cwd=repo)
    _run("git", "config", "user.email", "m@example", cwd=repo)

    # The signing epoch has to be a commit this repository actually contains
    # (FUR4: an absent epoch now refuses instead of grandfathering everything),
    # so the fixture makes one and pins the checker copy to it before anchoring.
    epoch = _signed_commit(repo, "epoch")
    anchor = _signed_commit(repo, "anchor")
    _run("git", "update-ref", P._ANCHOR_REF, anchor, cwd=repo)
    # NOT `code.py`: a root-level module shadowing a stdlib name breaks
    # pytest's own imports inside the evidence collection.
    _write(repo, "work.py", "x = 1\n")
    head = _signed_commit(repo, "work to bless")
    return repo, anchor, head, epoch


_FAKE_MANIFEST = {"frozen_files": {"a.py": "sha256:aa"},
                  "collection": {"node_count": 2, "node_ids": ["a::t", "b::t"]}}


def _fake_evidence(head: str, manifest=None):
    manifest = manifest if manifest is not None else _FAKE_MANIFEST
    body = json.dumps(manifest, indent=2, sort_keys=True).encode() + b"\n"
    return {"schema": P.EVIDENCE_SCHEMA, "candidate_sha": head,
            "interpreter": "3.13.13", "manifest": manifest,
            "manifest_sha256": P._sha256_bytes(body)}


def _plan_for(repo, anchor, head):
    report = P.Report()
    report.facts.update({"anchor": anchor, "head": head,
                         "authority_hashes": {"bootstrap/tests/_m.py":
                                              "sha256:" + "1" * 64}})
    return P.blessing_plan(report, _fake_evidence(head), repo=repo)


class TestBlessingPlan:
    def test_message_carries_the_audit_trail(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        plan = _plan_for(repo, anchor, head)
        assert "sha256:" + "1" * 64 in plan["message"]
        assert anchor in plan["message"] and head in plan["message"]

    def test_message_carries_no_self_referential_sha(self, tmp_path):
        """SR4: a commit's SHA hashes its own message."""
        repo, anchor, head = _anchored_repo(tmp_path)
        assert "new anchor P        : this commit" in _plan_for(
            repo, anchor, head)["message"]

    def test_recovery_mode_never_claims_to_have_inferred_legitimacy(self,
                                                                    tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        report = P.Report()
        report.facts.update({"anchor": anchor, "head": head,
                             "authority_hashes": {}})
        msg = P.blessing_plan(report, _fake_evidence(head), repo=repo,
                              last_legitimate_anchor="b" * 40)["message"]
        assert "NOT inferred" in msg and "b" * 40 in msg and anchor in msg


def _anchored_repo(tmp_path: Path):
    repo = _repo(tmp_path)
    _write(repo, P._MANIFEST_REL, "{}\n")
    anchor = _commit(repo, "anchor")
    _run("git", "update-ref", P._ANCHOR_REF, anchor, cwd=repo)
    # NOT `code.py`: a root-level module shadowing a stdlib name breaks
    # pytest's own imports inside the evidence collection.
    _write(repo, "work.py", "x = 1\n")
    head = _commit(repo, "work to bless")
    return repo, anchor, head


class TestApplyTakesNoArtifact:
    """CR1's structural answer, **narrowed** by security review [S2]/[E2].

    The original claim was "apply reads no handoff artifact". That cannot
    survive a signing stage which executes no candidate code: `collection` and
    `interpreter` are exactly the fields static re-derivation cannot produce, so
    a no-candidate-execution signer must consume stage-1 data. The claim was
    retracted rather than defended.

    What remains true, and is what CR1 actually falsified: **no adjacent
    self-digest authenticates a file.** A bundle carrying its own digest beside
    its own values is worthless -- re-hashing a tampered manifest agreed with
    itself. Authority comes from outside the artifact: for the review manifest,
    from a recorded external review; for the stage-1 package, from a digest the
    Maintainer confirms over the exact bytes written.
    """

    def test_apply_now_takes_only_the_closed_parameter_set(self):
        import inspect
        params = set(inspect.signature(P.apply_now).parameters)
        assert params == {"repo", "out", "package", "confirmed_package_sha256",
                          "signing_key",
                          "review_manifest", "reviewed_candidate"}, (
            f"stage 2's inputs are a closed set; got {sorted(params)}")
        # `signing_key` was added by security review [S1]. Stage 2 previously
        # received no key identity at all, so Git chose the signer from
        # repository configuration -- a closed input set that omits the identity
        # of the key that signs is closed around the wrong thing.

    def test_the_review_manifest_carries_no_self_digest(self):
        """The narrowed claim, mechanised. A `digest` or `sha256` row naming the
        manifest itself would be exactly the shape CR1 falsified, reappearing in
        the new artifact."""
        m = P.parse_review_manifest(
            "schema cairn-review-manifest/v1\n"
            "candidate " + "a" * 40 + "\n"
            "provenance external security review 2026-08-12\n"
            "member " + "b" * 64 + " bootstrap/tests/_gate_preflight.py\n")
        assert set(m) == {"schema", "candidate", "provenance", "members"}, (
            "the review manifest must carry no field that vouches for itself")

    def test_the_bundle_parser_is_gone(self):
        assert not hasattr(P, "parse_bundle"), (
            "a bundle parser would reintroduce the artifact CR1 falsified")

    def test_preview_record_is_labelled_as_a_record(self):
        r = subprocess.run(
            [sys.executable, str(_REPO / "bootstrap/tests/_gate_preflight.py"),
             "check", "--help"], capture_output=True, text=True, check=False)
        assert "not an input to" in r.stdout.replace("\n", " ")


class TestApplyTransaction:
    def _refs(self, repo: Path):
        return (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip())

    def _no_check(self, monkeypatch, repo, head):
        """Run apply's transaction path without re-running the full checks."""
        monkeypatch.setattr(P, "gather_evidence",
                            lambda *a, **k: _fake_evidence(head))
        monkeypatch.setattr(P, "check", lambda **k: _stub_report(repo, head))

    def test_refuses_without_explicit_confirmation(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        before = self._refs(repo)
        with pytest.raises(P.PreflightError,
                           match="confirmation of the exact stage-1 package"):
            P.apply_now(repo=repo)
        assert self._refs(repo) == before

    def test_write_path_allowlist_refuses_unenumerated_operations(self, tmp_path):
        repo, _a, _h = _anchored_repo(tmp_path)
        for bad in ("commit", "push", "checkout", "gc", "reset"):
            with pytest.raises(P.PreflightError, match="apply may only run"):
                P._git_write(bad, repo=repo)

    def test_symbolic_gate_anchor_refuses(self, tmp_path):
        """CR4: update-ref follows a symbolic ref, so the 'two-ref' transaction
        would silently change a third logical ref."""
        repo, anchor, head = _anchored_repo(tmp_path)
        _run("git", "symbolic-ref", P._ANCHOR_REF, "refs/heads/master", cwd=repo)
        with pytest.raises(P.PreflightError, match="symbolic"):
            P._require_direct_ref(P._ANCHOR_REF, repo=repo)

    def test_direct_gate_anchor_is_accepted(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        P._require_direct_ref(P._ANCHOR_REF, repo=repo)

    def test_stale_anchor_aborts_leaving_BOTH_refs_unmoved_and_no_residue(
            self, tmp_path):
        """SR8 plus CR3: an abort must move neither ref AND leave no residue,
        because construction never touches the real index or worktree."""
        repo, anchor, head = _anchored_repo(tmp_path)
        target = P.R._construct_anchor_commit(
            repo, head, P._MANIFEST_REL,
            json.dumps(_FAKE_MANIFEST, indent=2, sort_keys=True).encode() + b"\n")
        assert target != head
        before = self._refs(repo)
        ok, detail = P._advance_both_refs(repo, "refs/heads/master", target,
                                          branch_old=head, anchor_old="c" * 40)
        assert not ok and detail
        assert self._refs(repo) == before
        assert _run("git", "status", "--porcelain", cwd=repo).stdout == "", (
            "an aborted transaction must leave no index or worktree residue")




@contextlib.contextmanager
def _n4_precondition(key: Path):
    """Model the **N4** Maintainer precondition for a subprocess ceremony.

    Stage 1 probes whether it can sign and refuses if it can. In-process tests
    stub that probe; a test that executes the *recorded loader* cannot, because
    the loader runs in a child. So the fixture has to make the precondition
    genuinely true: the private half is moved aside for the duration of stage 1
    and restored afterwards, which is exactly what the ceremony asks a
    Maintainer to do -- key encrypted at rest or absent while candidate code
    runs, available again only for stage 2.

    Modelling it is the point. A fixture that left the private key readable
    would be testing the loader against a state the ceremony forbids.
    """
    stash = key.with_suffix(".withheld")
    key.rename(stash)
    try:
        yield
    finally:
        stash.rename(key)


def _stub_key(tmp_path: Path) -> dict:
    """Stub the key-channel PROBE while keeping the key IDENTITY real.

    Security review [S1] binds one validated fingerprint across both stages, so
    a stub that invented a key path would make every node using it blind to the
    binding. The probe is stubbed because in a test environment the key
    genuinely can sign -- that is [E1], covered by its own disposable-key nodes.
    """
    key_pub = str(Path(tmp_path) / "maint.pub")
    _path, fingerprint = P.validate_signing_key(key_pub)
    return {"key_path": key_pub, "fingerprint": fingerprint, "probe": "stubbed"}


def _recorded_stage1(repo: Path, tmp_path: Path, script: str, *,
                     env=None, prefix: str = ""):
    """Run the recorded loader end-to-end under a genuine N4 precondition.

    Every loader-boundary test drives the *runbook's own bytes* in a child
    shell, so none of them can stub the key probe -- and since Chunk D the
    recorded block ends at stage 1, which refuses outright if it can sign. The
    precondition is therefore modelled for real (`_n4_precondition`) rather than
    bypassed, which also keeps these nodes honest: they assert the loader's
    integrity properties against the state the ceremony actually runs in.

    Returns the completed process and the anchor as it stood before.
    """
    before = _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip()
    with _n4_precondition(tmp_path / "maint"):
        r = subprocess.run(["bash", "-c", prefix + script], cwd=str(repo),
                           capture_output=True, text=True, check=False,
                           env=env)
    return r, before


def _assert_stage1_completed(repo: Path, r, before: str):
    """What success means now that the recorded block stops at stage 1.

    The old assertion was "the anchor advanced". Asserting that today would be
    asserting that a stage holding no key had signed -- the exact inversion of
    D3. So success is: the loader ran clean, a package exists, and **no ref
    moved**.
    """
    assert r.returncode == 0, r.stderr[-2500:]
    pkg = Path(str(repo.parent / "authorization-package.json"))
    assert pkg.exists(), f"stage 1 wrote no package:\n{r.stderr[-1500:]}"
    assert _run("git", "rev-parse", P._ANCHOR_REF,
                cwd=repo).stdout.strip() == before, (
        "stage 1 moved a ref; it holds no key and must move nothing")


def _two_stage(repo: Path, monkeypatch, *, out=None, package_dir=None,
               review_manifest=None, reviewed_candidate=None):
    """Drive the real two-stage ceremony: stage 1 -> confirm -> stage 2.

    The key-channel probe is stubbed to "cannot sign" because in a test
    environment the ceremony key genuinely CAN sign -- that is [E1], and it has
    its own dedicated tests with disposable keys. Stubbing it here keeps these
    nodes about the protocol rather than about the host's key hygiene.

    The confirmation digest is taken from stage 1's **return value**, which is
    computed over the bytes it wrote -- never from inside the package.
    """
    # The PROBE is stubbed (in a test environment the key genuinely can sign --
    # that is [E1], with its own disposable-key nodes). The key IDENTITY is not:
    # security review [S1] binds one validated fingerprint across both stages,
    # so the stub reports the fixture key's real fingerprint and stage 2
    # re-derives it from the same file. Stubbing the identity too would make
    # every node here blind to the binding it exists to carry.
    key_pub = str(Path(repo).parent / "maint.pub")
    _path, fingerprint = P.validate_signing_key(key_pub)
    monkeypatch.setattr(P, "require_stage1_cannot_sign",
                        lambda *a, **k: {"key_path": key_pub,
                                         "fingerprint": fingerprint,
                                         "probe": "stubbed"})
    out = out if out is not None else io.StringIO()
    pkg_dir = Path(package_dir) if package_dir else Path(repo).parent
    pkg_path = pkg_dir / "authorization-package.json"
    if pkg_path.exists():
        pkg_path.unlink()
    one = P.stage1(repo=repo, package_out=pkg_path, out=out,
                   review_manifest=review_manifest,
                   reviewed_candidate=reviewed_candidate)
    P._phase = P._PHASE_CANDIDATE     # stage 2 is a fresh process in reality
    # The transition flags go to BOTH stages, as the runbook records them.
    # Stage 2 refuses a package that authorizes a transition when it is not
    # itself told about one -- otherwise it would sign a checkpoint recording
    # "steady state" for a run that changed the authority closure.
    return P.apply_now(repo=repo, package=str(pkg_path),
                       confirmed_package_sha256=one["package_sha256"], out=out,
                       signing_key=key_pub,
                       review_manifest=review_manifest,
                       reviewed_candidate=reviewed_candidate)


def _stub_report(repo, head):
    anchor = _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip()
    r = P.Report()
    r.facts.update({"anchor": anchor, "head": head,
                    "authority_hashes": {"bootstrap/tests/_m.py":
                                         "sha256:" + "1" * 64}})
    return r


class TestApplySuccessPath:
    """The full ceremony, in-process.

    `gather_evidence` is substituted here: the real manifest producer needs more
    of the repository than an integration fixture can carry (it fails outright in
    a minimal tree), and the evidence stage has its own tests above against a
    stub producer. Everything else is real -- the checks, the signed
    construction, the verification, the transaction, the worktree sync.
    """

    def _refs(self, repo):
        return (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip())

    def _prepared(self, tmp_path, monkeypatch):
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        # Only the *executable* half is stubbed. Since FUR3 the static fields
        # are re-derived from raw objects and compared, so a wholly invented
        # manifest is refused -- correctly. What the real producer supplies and
        # this cannot is the pytest collection; everything else must be the
        # truth about the tree.
        manifest = {**P.rederive_static_manifest(head, repo=repo),
                    "collection": {"node_count": 1, "node_ids": ["a.py::t"],
                                   "skip_xfail_marked": []},
                    "interpreter": {"version": "3.13.13"}}
        monkeypatch.setattr(P, "gather_evidence",
                            lambda *a, **k: _fake_evidence(head, manifest))
        return repo, anchor, head

    def test_success_signs_the_commit_and_leaves_a_clean_tree(
            self, tmp_path, monkeypatch):
        repo, anchor, head = self._prepared(tmp_path, monkeypatch)
        res = _two_stage(repo, monkeypatch)
        new_head, new_anchor = self._refs(repo)
        assert new_head == new_anchor == res["new_anchor"]

        # CR2: the blessed commit must carry the reviewed message AND a
        # signature. It becomes the anchor, so an unsigned one would be excluded
        # from every later anchor..HEAD signature check, permanently.
        sig = _run("git", "log", "-1", "--format=%G?", cwd=repo).stdout.strip()
        assert sig == "G", f"the trust-root commit must be signed, got {sig!r}"
        body = _run("git", "log", "-1", "--format=%B", cwd=repo).stdout
        assert "Authorized verifier-module hashes" in body
        assert "cairn: supervised gate re-anchor (N = C + manifest)" not in body

        # CR3: success must leave no staged or unstaged residue.
        assert _run("git", "status", "--porcelain", cwd=repo).stdout == ""
        assert _run("git", "diff", "--cached", "--name-only",
                    cwd=repo).stdout == ""

    def test_a_wrong_message_substitution_refuses_before_any_ref_moves(
            self, tmp_path, monkeypatch):
        repo, anchor, head = self._prepared(tmp_path, monkeypatch)
        real = P._construct_signed_commit
        monkeypatch.setattr(
            P, "_construct_signed_commit",
            lambda r, h, mb, msg, **kw: real(r, h, mb, "a different message\n",
                                            **kw))
        before = self._refs(repo)
        with pytest.raises(P.PreflightError, match="reviewed message"):
            _two_stage(repo, monkeypatch)
        assert self._refs(repo) == before

    def test_an_unsigned_commit_substitution_refuses(self, tmp_path,
                                                     monkeypatch):
        repo, anchor, head = self._prepared(tmp_path, monkeypatch)
        monkeypatch.setattr(
            P, "_construct_signed_commit",
            # Built from the SAME manifest bytes `apply` derived, so the parent
            # and blob-digest checks pass and the refusal comes from the
            # signature (and message) checks -- the ones under test. The
            # unsigned helper returns only a commit id; the real one now also
            # returns the manifest blob id for the direct index install.
            lambda r, h, mb, msg, **kw: (P.R._construct_anchor_commit(
                r, h, P._MANIFEST_REL, mb), "0" * 40))
        before = self._refs(repo)
        with pytest.raises(P.PreflightError, match="not validly signed|message"):
            _two_stage(repo, monkeypatch)
        assert self._refs(repo) == before

    def test_blocked_checks_write_nothing(self, tmp_path, monkeypatch):
        repo, anchor, head = self._prepared(tmp_path, monkeypatch)
        _write(repo, "bootstrap/tests/_gate_preflight.py", "# tampered\n")
        before = self._refs(repo)
        with pytest.raises(P.PreflightError, match="refuse this state"):
            _two_stage(repo, monkeypatch)
        assert self._refs(repo) == before


class TestPublicPathCli:
    """CR5: the recorded workflow exercised through real subprocesses.

    The refusal paths live here; the full three-command success case is in
    `TestThreeCommandIntegration`, which drives all three through subprocesses
    against a fixture running the real manifest producer. An earlier version of
    this docstring recorded a known gap -- no public-path `apply` success case --
    because the producer refuses a fixture that collects zero nodes or lacks the
    AST baseline. Supplying both closed it, so the gap is gone rather than
    merely documented.
    """

    def _cli(self, *args, cwd=None):
        return subprocess.run(
            [sys.executable, str(_REPO / "bootstrap/tests/_gate_preflight.py"),
             *args], capture_output=True, text=True, check=False,
            cwd=str(cwd) if cwd else None)

    def test_evidence_then_check_through_subprocesses(self, tmp_path):
        repo = _evidence_repo(tmp_path)
        _write(repo, P._MANIFEST_REL, "{}\n")
        _commit(repo, "manifest")
        ev = tmp_path / "ev.json"
        r1 = self._cli("evidence", "--repo", str(repo), "-o", str(ev))
        assert r1.returncode == 0, r1.stderr[-1500:]
        assert "EXECUTES CANDIDATE CODE" in r1.stderr
        artifact = json.loads(ev.read_text())
        assert artifact["schema"] == P.EVIDENCE_SCHEMA

        r2 = self._cli("check", "--repo", str(repo), "--evidence", str(ev))
        assert r2.returncode in (1, 2), "a fixture repo must not pass check"
        assert "Traceback" not in r2.stderr

    def test_the_single_stage_apply_and_its_boolean_are_gone_from_the_cli(
            self, tmp_path):
        """D5: **removed, not deprecated** -- and removed at the CLI surface.

        The old shape was one `apply --confirm-supervised-reanchor` that ran
        candidate code and signed in one process. A deprecation that still
        parses is a path an operator can still take, so the assertion is that
        argparse itself rejects both spellings. Whatever `apply_now` believes
        internally, an unreachable subcommand is what makes the removal real.
        """
        repo, anchor, head = _anchored_repo(tmp_path)
        before = (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                  _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip())

        gone = self._cli("apply", "--repo", str(repo))
        assert gone.returncode == 2
        assert "invalid choice: 'apply'" in gone.stderr
        assert "stage1" in gone.stderr and "stage2" in gone.stderr

        # The digest confirmation is supplied so that the boolean is the ONLY
        # thing argparse can object to -- otherwise the missing required flag
        # masks it and this node would pass without testing the removal.
        boolean = self._cli("stage2", "--repo", str(repo),
                            "--package", str(tmp_path / "nope.json"),
                            "--signing-key", str(tmp_path / "maint.pub"),
                            "--confirm-package-sha256", "0" * 64,
                            "--confirm-supervised-reanchor")
        assert boolean.returncode == 2
        assert "unrecognized arguments: --confirm-supervised-reanchor" in \
            boolean.stderr

        assert (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                _run("git", "rev-parse", P._ANCHOR_REF,
                     cwd=repo).stdout.strip()) == before

    def test_stage2_refuses_without_the_package_digest_confirmation(
            self, tmp_path):
        """The confirmation is required by argparse, and it is over BYTES.

        `required=True` is the mechanism, so the refusal happens before any
        repository work -- which is the point: a confirmation prompt that
        appears after the state has been read is a confirmation of nothing.
        """
        repo, anchor, head = _anchored_repo(tmp_path)
        before = (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                  _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip())
        r = self._cli("stage2", "--repo", str(repo),
                      "--package", str(tmp_path / "nope.json"))
        assert r.returncode == 2
        assert "--confirm-package-sha256" in r.stderr
        assert (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                _run("git", "rev-parse", P._ANCHOR_REF,
                     cwd=repo).stdout.strip()) == before

    def test_the_in_process_signing_entry_still_refuses_a_missing_confirmation(
            self, tmp_path):
        """Defence in depth: the CLI is not the only caller of `apply_now`.

        argparse enforces the flag for operators; this node enforces it for the
        function, so a future caller that bypasses `main` cannot sign without
        naming the exact bytes it is authorizing.
        """
        repo, anchor, head = _anchored_repo(tmp_path)
        with pytest.raises(P.PreflightError) as exc:
            P.apply_now(repo=repo, package=str(tmp_path / "nope.json"),
                        confirmed_package_sha256=None, out=io.StringIO())
        assert "--confirm-package-sha256" in str(exc.value)
        assert "REMOVED" in str(exc.value)

    def test_malformed_evidence_is_refused_through_the_cli(self, tmp_path):
        repo, _a, _h = _anchored_repo(tmp_path)
        bad = tmp_path / "bad.json"
        bad.write_text("{not json")
        r = self._cli("check", "--repo", str(repo), "--evidence", str(bad))
        assert r.returncode == 2 and "not valid JSON" in r.stderr


def _checker_cli(checker: Path, *args):
    """Invoke an extracted checker as the ceremony does: sterile, by path."""
    return subprocess.run(
        [sys.executable, "-E", "-s", str(checker), *args],
        capture_output=True, text=True, check=False)

def _subprocess_ceremony(checker: Path, repo: Path, tmp_path: Path, *,
              package=None):
    """Stage 1 -> external confirmation -> stage 2, as real subprocesses.

    The point of running it this way is that nothing can be stubbed. Stage 1
    genuinely probes the key channel, so the N4 precondition is genuinely
    established: the private half is withheld for the duration of stage 1
    and restored only for stage 2 -- which is the ceremony's own
    instruction, not a test convenience.

    The confirmation digest is read from **stage 1's stdout**, computed by
    stage 1 over the bytes it wrote. Taking it from inside the package would
    be the CR1 defect exactly: value and digest from one editable file.
    """
    pkg = Path(package) if package else tmp_path / "authorization-package.json"
    if pkg.exists():
        pkg.unlink()
    with _n4_precondition(tmp_path / "maint"):
        one = _checker_cli(checker, "stage1", "--repo", str(repo),
                           "--signing-key", str(tmp_path / "maint.pub"),
                           "--package-out", str(pkg))
    assert one.returncode == 0, one.stderr[-2500:]
    staged = json.loads(one.stdout)
    assert pkg.exists(), "stage 1 reported success and wrote no package"

    # Independently digest the file, the way the runbook tells the
    # Maintainer to: the confirmation must be over bytes on disk.
    import hashlib
    assert staged["package_sha256"] == hashlib.sha256(
        pkg.read_bytes()).hexdigest(), (
        "stage 1's reported digest is not the digest of what it wrote")

    two = _checker_cli(checker, "stage2", "--repo", str(repo),
                       "--package", str(pkg),
                       "--signing-key", str(tmp_path / "maint.pub"),
                       "--confirm-package-sha256", staged["package_sha256"])
    assert two.returncode == 0, two.stderr[-2500:]
    return json.loads(two.stdout)


class TestThreeCommandIntegration:
    """Chunk E: `evidence` -> `check` -> `apply` as one flow, all real.

    This is the coverage code review CR5 asked for. Nothing is substituted and
    nothing is imported: all three commands run as real subprocesses, the
    producer executes candidate code for real, and the transaction moves real
    refs in a temp repo. It took supplying the two things the real producer
    refuses without -- a non-empty collection and the AST baseline keys.

    Since FUR5 the executed bytes come from **the anchor**, extracted by the
    runbook's own pipeline, rather than from `_REPO`. That is what the ceremony
    actually does, and running it any other way is how a recorded invocation
    reached first use having never been executed once.
    """

    def _cli(self, checker: Path, *args):
        return subprocess.run(
            [sys.executable, "-E", "-s", str(checker), *args],
            capture_output=True, text=True, check=False)

    def test_the_whole_ceremony_end_to_end_through_subprocesses(self, tmp_path):
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        checker = _extract_anchored(repo, tmp_path / "extract")
        ev = tmp_path / "ev.json"

        r1 = self._cli(checker, "evidence", "--repo", str(repo), "-o", str(ev))
        assert r1.returncode == 0, r1.stderr[-1500:]
        evidence = json.loads(ev.read_text())
        assert evidence["candidate_sha"] == head
        assert evidence["manifest"]["collection"]["node_count"] >= 1

        r2 = self._cli(checker, "check", "--repo", str(repo),
                       "--evidence", str(ev))
        assert r2.returncode == 0, r2.stderr[-2500:]

        # The signature CENSUS must have counted something. The range check it
        # replaced is retired (Chunk B), so the old `"checked": >= 1` assertion
        # went with it -- but its reasoning transfers exactly: a census that
        # counted zero commits is indistinguishable from one that does nothing,
        # and this integration test exists to catch precisely that.
        assert '"retired"' in r2.stderr, r2.stderr[-2500:]
        total = re.search(r'"total": (\d+)', r2.stderr)
        assert total and int(total.group(1)) >= 1, r2.stderr[-2500:]

        result = _subprocess_ceremony(checker, repo, tmp_path)

        new_head = _run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
        new_anchor = _run("git", "rev-parse", P._ANCHOR_REF,
                          cwd=repo).stdout.strip()
        assert new_head == new_anchor == result["new_anchor"]
        assert _run("git", "log", "-1", "--format=%G?",
                    cwd=repo).stdout.strip() == "G"
        assert "Authorized verifier-module hashes" in _run(
            "git", "log", "-1", "--format=%B", cwd=repo).stdout
        assert _run("git", "status", "--porcelain", cwd=repo).stdout == ""

        # And the blessed manifest is the AUTHORITATIVE one -- the candidate's
        # collection with every checker-derived field replaced by the checker's
        # own re-derivation. This used to assert `blessed == evidence["manifest"]`,
        # which is the defect code review [IC2] found: the re-derivation was
        # computed, compared, and then discarded, so no Git-native field ever
        # reached the anchored artifact.
        blessed = json.loads(_run("git", "show",
                                  f"{result['new_anchor']}:{P._MANIFEST_REL}",
                                  cwd=repo).stdout)

        # Asserted as PROPERTIES of the committed bytes, not against a rebuild.
        #
        # The replacement for [IC2] was `blessed == authoritative_manifest(...)`
        # -- the same function on both sides of the equals sign, so it agreed
        # with whatever that function did and could not fail. It duly passed
        # while every committed entry was `{"mode":..., "oid":...}` with the
        # content digest dropped. A tautology is a worse defect than a missing
        # test: it reports success.
        prev = result["previous_head"]
        tree = {}
        for line in _run("git", "ls-tree", "-r", prev,
                         cwd=repo).stdout.splitlines():
            meta, rel = line.split("\t", 1)
            mode, _kind, oid = meta.split()
            tree[rel] = (mode, oid)
        cand = evidence["manifest"]["frozen_files"]
        assert blessed["frozen_files"], "the blessed manifest pins nothing"
        for rel, entry in blessed["frozen_files"].items():
            assert isinstance(entry, dict), f"{rel} is not a v2 entry: {entry!r}"
            assert set(entry) >= {"sha256", "mode", "oid"}, (
                f"{rel} is missing {sorted({'sha256', 'mode', 'oid'} - set(entry))}"
                f" -- the trust root would carry an entry the gate cannot compare")
            # The content digest is the CANDIDATE's, having survived the merge.
            expected_sha = cand[rel]
            expected_sha = (expected_sha["sha256"]
                            if isinstance(expected_sha, dict) else expected_sha)
            assert entry["sha256"] == expected_sha, rel
            # Mode and oid are the CHECKER's, read from the real tree.
            assert (entry["mode"], entry["oid"]) == tree[rel], rel
        # And the field only the checker can derive is present.
        assert blessed["object_format"] == G._object_format(repo)
        assert blessed["collection"] == evidence["manifest"]["collection"]

    def test_a_second_run_refuses_because_the_state_moved(self, tmp_path):
        """Replay, honestly: no nonce, but the bound state no longer holds."""
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        checker = _extract_anchored(repo, tmp_path / "extract")
        _subprocess_ceremony(checker, repo, tmp_path)

        with _n4_precondition(tmp_path / "maint"):
            again = self._cli(
                checker, "stage1", "--repo", str(repo),
                "--signing-key", str(tmp_path / "maint.pub"),
                "--package-out", str(tmp_path / "second.json"))
        assert again.returncode == 2
        assert not (tmp_path / "second.json").exists(), (
            "a refused stage 1 left an authorization package behind")

    def test_replaying_the_confirmed_package_after_the_state_moved_refuses(
            self, tmp_path):
        """The replay surface the two-stage split *creates*, closed.

        Splitting the ceremony makes the authorization a durable file that
        outlives the run that produced it -- something the single-stage shape
        never had. The digest confirmation cannot catch this: the bytes are
        untouched, so `--confirm-package-sha256` still passes. What must refuse
        is R4-c's re-resolution of the state the package names, and the only way
        to know it does is to replay a package whose digest is still perfectly
        valid.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        checker = _extract_anchored(repo, tmp_path / "extract")
        pkg = tmp_path / "authorization-package.json"
        _subprocess_ceremony(checker, repo, tmp_path, package=pkg)

        import hashlib
        digest = hashlib.sha256(pkg.read_bytes()).hexdigest()
        moved = _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip()

        replay = self._cli(checker, "stage2", "--repo", str(repo),
                           "--package", str(pkg),
                           "--signing-key", str(tmp_path / "maint.pub"),
                           "--confirm-package-sha256", digest)
        assert replay.returncode == 2
        assert "stale package cannot authorize a moved state" in replay.stderr
        assert _run("git", "rev-parse", P._ANCHOR_REF,
                    cwd=repo).stdout.strip() == moved, (
            "a replayed package moved the trust root a second time")


# --------------------------------------------------------------------------
# FUR5 -- the recorded anchored invocation, actually executed
#
# The runbook recorded a ceremony that had never been run once. It extracted
# `bootstrap/tests` into a temp directory and invoked the checker with no
# `--repo`, so the `_REPO` default -- derived from `__file__` -- named the
# extraction directory. Executing the recorded steps refused with git's bare
# `fatal: not a git repository` before reaching the checkout at all.
#
# These tests execute the runbook's literal shell pipeline against a separate
# target repository, which is the only thing that would have caught it.
# --------------------------------------------------------------------------

#: The first-use hash set the loader verifies against. Recorded by the
#: Maintainer at Chunk G step M2; the fixtures compute their own.
#:
#: **All nine authority-closure members, not the seven importable modules.**
#: Security review [M2-R1]: this helper carried only the Python modules while
#: M2's authority closure also contains `REANCHOR_RUNBOOK.md` and
#: `dev/.cairn/allowed_signers`, so the tests exercised a checklist narrower
#: than the artifact they claimed to test. Derived from
#: `declared_authority_closure()` rather than retyped, so the two cannot drift.
_LOADED_MODULES = tuple(sorted(P.declared_authority_closure()))


def _recorded_hashes(repo: Path, ref: str = P._ANCHOR_REF) -> str:
    """The `shasum -c` checklist for the loader, over the ANCHORED bytes."""
    import hashlib
    lines = []
    for rel in _LOADED_MODULES:
        blob = subprocess.run(
            ["git", "-C", str(repo), "cat-file", "blob", f"{ref}:{rel}"],
            capture_output=True, check=True).stdout
        lines.append(f"{hashlib.sha256(blob).hexdigest()}  {rel}")
    return "\n".join(lines)


def _runbook_block(containing: str) -> str:
    """The fenced block under Phase 0 pre-flight that contains `containing`.

    Selected by content, not by index: the section now holds both the
    acquisition command and the loader, and an index would silently start
    testing the wrong one the next time a block is added.
    """
    text = (_REPO / "bootstrap/REANCHOR_RUNBOOK.md").read_text(encoding="utf-8")
    # Bounded at the transition-mode subsection as well as the next `##`.
    # Chunk A added a SECOND loader that also contains `_gate_preflight.py`,
    # so without this bound the "exactly one" assertion below fires -- which is
    # the helper working correctly, and is why it is bounded rather than
    # loosened to "the first match".
    section = (text.split("### Phase 0 pre-flight")[1]
                   .split("\n### Phase 0 transition mode")[0]
                   .split("\n## ")[0])
    blocks = [b for i, b in enumerate(section.split("```")) if i % 2]
    matching = [b for b in blocks if containing in b]
    assert len(matching) == 1, (
        f"expected exactly one Phase 0 block containing {containing!r}, "
        f"found {len(matching)}")
    return matching[0]


def _transition_block() -> str:
    """The Chunk A transition loader, lifted verbatim from the runbook.

    Same discipline as `_runbook_block`: the recorded steps ARE the ceremony, so
    the script under test comes out of the document rather than being
    transcribed into Python where it could be written correct while the recorded
    steps stayed broken.
    """
    text = (_REPO / "bootstrap/REANCHOR_RUNBOOK.md").read_text(encoding="utf-8")
    section = text.split("### Phase 0 transition mode")[1].split("\n## ")[0]
    blocks = [b for i, b in enumerate(section.split("```")) if i % 2]
    matching = [b for b in blocks if "TRANSITION" in b]
    assert len(matching) == 1, (
        f"expected exactly one transition loader block, found {len(matching)}")
    return matching[0]


def _stage2_block() -> str:
    """The recorded stage-2 invocation, lifted verbatim from the runbook.

    Same discipline as every other recorded block: the document is the ceremony.
    A stage-2 script transcribed into Python could be written correct while the
    recorded one stayed broken, which is FUR5 exactly -- and stage 2 is the
    invocation that signs and moves the trust root, so it is the last place to
    accept a recorded-but-never-executed procedure.
    """
    text = (_REPO / "bootstrap/REANCHOR_RUNBOOK.md").read_text(encoding="utf-8")
    section = text.split("### Phase 0 stage 2")[1].split(
        "\n#### Stage 2 in transition mode")[0].split("\n## ")[0]
    blocks = [b for i, b in enumerate(section.split("```")) if i % 2]
    matching = [b for b in blocks if "STAGE2" in b]
    assert len(matching) == 1, (
        f"expected exactly one recorded stage-2 block, found {len(matching)}")
    return matching[0]


def _stage2_transition_block() -> str:
    """The transition's OWN complete stage-2 block.

    Selected separately because it *is* separate: code review [C2] found the
    runbook telling the operator to "replace the final command" of the
    steady-state block, which left the extraction reading
    `refs/cairn/gate-anchor`. Stage 1 then ran the candidate's checker and stage
    2 the old one -- the old authority vouching for its replacement, after the
    key was loaded.
    """
    text = (_REPO / "bootstrap/REANCHOR_RUNBOOK.md").read_text(encoding="utf-8")
    section = text.split("#### Stage 2 in transition mode")[1].split("\n### ")[0]
    blocks = [b for i, b in enumerate(section.split("```")) if i % 2]
    matching = [b for b in blocks if "STAGE2T" in b]
    assert len(matching) == 1, (
        f"expected exactly one transition stage-2 block, found {len(matching)}")
    return matching[0]


def _recorded(repo: Path) -> dict[str, str]:
    """The values a Maintainer records at first use. Nothing is discovered by
    the runbook itself -- that was FUR6 and FUR7 -- so the fixtures stand in for
    the Maintainer and supply them explicitly."""
    values = {
        "<absolute-path-of-the-checkout-to-bless>": str(repo),
        "<maintainer-recorded-interpreter>": sys.executable,
        "<maintainer-recorded-env>": shutil.which("env"),
        "<maintainer-recorded-git>": shutil.which("git"),
        "<maintainer-recorded-mktemp>": shutil.which("mktemp"),
        "<maintainer-recorded-mkdir>": shutil.which("mkdir"),
        "<maintainer-recorded-shasum>": shutil.which("shasum"),
        "<maintainer-recorded-sort>": shutil.which("sort"),
        # The fixture's own throwaway signing key. `_n4_precondition` withholds
        # its private half for the duration of a stage-1 run, which is what the
        # ceremony asks a Maintainer to do.
        "<maintainer-recorded-signing-key-public-path>":
            str(repo.parent / "maint.pub"),
        # Per-fixture and deliberately NOT inside the repo: the package is a
        # ceremony artifact, and writing it into the tree being blessed would
        # make it part of the state it authorizes.
        "<absolute-path-for-the-authorization-package-must-not-exist>":
            str(repo.parent / "authorization-package.json"),
        # Stage 2 names the same artifact, as an existing file this time.
        "<absolute-path-of-the-authorization-package>":
            str(repo.parent / "authorization-package.json"),
        "<maintainer-recorded-home>": os.environ.get("HOME", "/nonexistent"),
    }
    missing = [k for k, v in values.items() if not v]
    assert not missing, f"cannot resolve recorded utilities: {missing}"
    return values


def _substitute(block: str, repo: Path, *, hashes: bool = True,
                candidate: str | None = None) -> str:
    """Fill the Maintainer-recorded placeholders in a recorded block.

    ``candidate`` supplies the transition's own checklist: the reviewed
    candidate's bytes, recorded at that OID. It is a separate placeholder from
    the first-use set on purpose -- a transition's stage 2 extracts by the
    reviewed OID and must verify against **that** commit's hashes, and reusing
    the anchor's set is exactly the [C2] confusion in a different key.
    """
    for placeholder, value in _recorded(repo).items():
        if placeholder in block:
            block = block.replace(placeholder, shlex.quote(value))
    residual = block.replace("<maintainer-recorded-first-use-hashes>", "") \
                    .replace("<maintainer-recorded-reviewed-candidate-hashes>", "")
    assert "<maintainer-recorded" not in residual, (
        f"an unrecorded placeholder survived substitution:\n{block}")
    if candidate is not None:
        assert "<maintainer-recorded-reviewed-candidate-hashes>" in block
        block = block.replace("<maintainer-recorded-reviewed-candidate-hashes>",
                              _recorded_hashes(repo, candidate))
    if hashes:
        assert "<maintainer-recorded-first-use-hashes>" in block
        block = block.replace("<maintainer-recorded-first-use-hashes>",
                              _recorded_hashes(repo))
    return block


def _runbook_ceremony_script(repo: Path) -> str:
    """The Phase 0 pre-flight loader, lifted verbatim from the runbook.

    The recorded steps **are** the ceremony. A fix in code that the recorded
    steps do not exercise is not a fix -- which is exactly the shape FUR5 took,
    and FUR6 and FUR7 after it -- so the script under test comes out of the
    runbook rather than being transcribed into Python, where it could be written
    correct while the recorded steps stayed broken.

    Only the Maintainer-recorded values are substituted; every line of logic is
    the runbook's own.
    """
    return _substitute(_runbook_block("_gate_preflight.py"), repo)


def _runbook_acquisition_command(repo: Path) -> str:
    """The step-1 command that reads the runbook itself from the anchor.

    Under test because it claimed to be sterile and was not: it is the
    instruction source, so a substituted one can simply omit the loader (FUR7).
    """
    return _substitute(_runbook_block("REANCHOR_RUNBOOK.md"), repo,
                       hashes=False)


class TestAnchoredInvocationTargetsTheNamedCheckout:

    def _cli(self, checker: Path, *args, cwd=None):
        return subprocess.run(
            [sys.executable, "-E", "-s", str(checker), *args],
            capture_output=True, text=True, check=False,
            cwd=str(cwd) if cwd else None)

    def test_the_recorded_runbook_ceremony_actually_runs(self, tmp_path):
        """The runbook's own bytes, executed.

        This is the test whose absence *was* FUR5. The recorded ceremony had
        never been run once, and a Python transcription of it would not have
        caught that -- the transcription would have been written correct while
        the recorded steps stayed broken. So the script comes out of the runbook.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        script = _runbook_ceremony_script(repo)
        before = _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip()

        with _n4_precondition(tmp_path / "maint"):
            r = subprocess.run(["bash", "-c", script], cwd=str(repo),
                               capture_output=True, text=True, check=False)

        assert r.returncode == 0, f"{script}\n---\n{r.stderr[-2500:]}"
        # The recorded loader now ends at STAGE 1, so what success means has
        # changed: a package exists and NO ref moved. Asserting the old
        # "anchor advanced" would now be asserting that a stage which must not
        # sign had signed.
        pkg = Path(str(repo.parent / "authorization-package.json"))
        assert pkg.exists(), f"stage 1 wrote no package:\n{r.stderr[-1500:]}"
        assert _run("git", "rev-parse", P._ANCHOR_REF,
                    cwd=repo).stdout.strip() == before, (
            "stage 1 moved a ref; it holds no key and must move nothing")

    def test_the_recorded_two_stage_ceremony_runs_end_to_end(self, tmp_path):
        """Both recorded blocks, executed in order, with a real key handover.

        The FUR5 lesson applied to the protocol that replaced the one FUR5
        found: a recorded ceremony nobody has run is not a ceremony. Stage 1's
        block and stage 2's block are both lifted from the runbook, and the
        Maintainer's part between them -- confirm the digest independently, then
        make the key available -- is performed rather than assumed.
        """
        import hashlib
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        before = _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip()
        pkg = repo.parent / "authorization-package.json"
        if pkg.exists():
            pkg.unlink()

        # --- stage 1: key withheld, no ref may move -----------------------
        r1, _ = _recorded_stage1(repo, tmp_path, _runbook_ceremony_script(repo))
        assert r1.returncode == 0, r1.stderr[-2500:]
        assert pkg.exists(), "the recorded stage 1 wrote no package"
        assert _run("git", "rev-parse", P._ANCHOR_REF,
                    cwd=repo).stdout.strip() == before

        # --- the Maintainer's step between the stages ---------------------
        confirmed = hashlib.sha256(pkg.read_bytes()).hexdigest()
        assert confirmed in r1.stderr, (
            "stage 1 did not print the digest the operator is told to confirm")

        # --- stage 2: key available, and it extracts its OWN bytes --------
        script = _substitute(_stage2_block(), repo).replace(
            "<the-64-hex-digest-you-verified-in-step-1>", shlex.quote(confirmed))
        r2 = subprocess.run(["bash", "-c", script], cwd=str(repo),
                            capture_output=True, text=True, check=False)
        assert r2.returncode == 0, f"{script}\n---\n{r2.stderr[-2500:]}"

        new_anchor = _run("git", "rev-parse", P._ANCHOR_REF,
                          cwd=repo).stdout.strip()
        assert new_anchor != before, "the recorded stage 2 moved nothing"
        assert new_anchor == _run("git", "rev-parse", "HEAD",
                                  cwd=repo).stdout.strip()
        assert _run("git", "log", "-1", "--format=%G?",
                    cwd=repo).stdout.strip() == "G", "the checkpoint is unsigned"

    def test_the_recorded_transition_stage2_carries_both_flags(self):
        """E2. A transition's stage 2 has no recorded form without them.

        This is the shape of gap that keeps recurring here: the transition
        loader was updated to end at stage 1, and stage 2 got a recorded block
        -- but only the steady-state one. A Maintainer running a real transition
        would have reached the signing step with no recorded command for it, and
        the flags are now a refusal rather than an option, so improvising would
        have been a hard stop mid-ceremony with the key already loaded.
        """
        text = (_REPO / "bootstrap/REANCHOR_RUNBOOK.md").read_text(
            encoding="utf-8")
        section = text.split("#### Stage 2 in transition mode")[1].split(
            "\n### ")[0]
        assert "--transition-from-review" in section
        assert "--reviewed-candidate" in section
        assert "REVIEW_MANIFEST=" in section and "RESOLVED=" in section
        # And it must say where RESOLVED comes from: re-resolving a ref here
        # would defeat the transition loader's resolve-once discipline (A4).
        assert "never re-resolved here" in section

    def test_the_transition_stage2_extracts_from_the_candidate_not_the_anchor(
            self):
        """Code review [C2], as a property of the recorded text.

        A transition's stage 2 must extract by the reviewed candidate OID. The
        runbook previously said "replace the final command" of the steady-state
        block, whose extraction reads `refs/cairn/gate-anchor` -- so stage 1 ran
        the candidate's checker and stage 2 ran the old one. That is the old
        authority vouching for its replacement, and it fails closed only *after*
        the ceremony key has been loaded.
        """
        block = _stage2_transition_block()
        assert 'cat-file blob "$RESOLVED:$path"' in block, (
            "the transition's stage 2 does not extract by the reviewed OID")
        assert "refs/cairn/gate-anchor" not in block, (
            "the transition's stage 2 extracts from the anchor -- the old "
            "authority would vouch for its own replacement")
        # Its checklist must be the CANDIDATE's, not the first-use set: hashes
        # from the anchor would pass while the wrong bytes ran.
        assert "<maintainer-recorded-reviewed-candidate-hashes>" in block
        assert "<maintainer-recorded-first-use-hashes>" not in block
        assert '"$SHASUM" -a 256 -c RECORDED.sha256' in block

    def test_the_recorded_transition_ceremony_runs_end_to_end(self, tmp_path):
        """The transition's own two-stage ceremony, executed from the document.

        The steady-state node above proves the protocol runs; this proves the
        mode that actually motivated the plan runs, and that it runs *through
        the recorded text* rather than through Python that agrees with itself.
        """
        import hashlib
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        _write(repo, "bootstrap/tests/_oracle.py", "# a reviewed change\n")
        resolved = _signed_commit(repo, "reviewed authority change")
        manifest = tmp_path / "review-manifest.txt"
        manifest.write_text(_review_manifest(repo, resolved), encoding="utf-8")

        loader = _substitute(_transition_block(), repo, hashes=False)
        loader = loader.replace("<candidate-ref-or-oid-to-transition-to>",
                                shlex.quote(resolved))
        loader = loader.replace(
            "<absolute-path-of-the-maintainer-recorded-review-manifest>",
            shlex.quote(str(manifest)))

        pkg = repo.parent / "authorization-package.json"
        if pkg.exists():
            pkg.unlink()
        with _n4_precondition(tmp_path / "maint"):
            r1 = subprocess.run(["bash", "-c", loader], cwd=str(repo),
                                capture_output=True, text=True, check=False)
        assert r1.returncode == 0, f"{loader}\n---\n{r1.stderr[-3000:]}"
        assert pkg.exists(), "the recorded transition stage 1 wrote no package"

        confirmed = hashlib.sha256(pkg.read_bytes()).hexdigest()
        # The transition's OWN recorded block, verbatim -- not the steady-state
        # one with its last command edited. That edit was [C2].
        script = _substitute(_stage2_transition_block(), repo, hashes=False,
                             candidate=resolved)
        script = script.replace("<the-64-hex-digest-you-verified-in-step-1>",
                                shlex.quote(confirmed))
        script = script.replace(
            "<absolute-path-of-the-maintainer-recorded-review-manifest>",
            shlex.quote(str(manifest)))
        script = script.replace(
            "<the-full-commit-oid-the-transition-loader-resolved-and-printed>",
            shlex.quote(resolved))

        r2 = subprocess.run(["bash", "-c", script], cwd=str(repo),
                            capture_output=True, text=True, check=False)
        assert r2.returncode == 0, f"{script}\n---\n{r2.stderr[-3000:]}"

        message = _run("git", "log", "-1", "--format=%B", cwd=repo).stdout
        recovered = P.parse_admitted_authority(message)
        assert recovered == P.parse_review_manifest(
            manifest.read_text(encoding="utf-8"))["members"], (
            "the recorded transition ceremony did not record its admitted set")

    def test_a_transition_in_which_the_CHECKER_ITSELF_differs(self, tmp_path):
        """Code review [D2]: the case that motivates transition mode at all.

        Every other transition node changes `_oracle.py`. But the reason the
        mode exists is that a candidate may change **the checker that decides**
        — `_gate_preflight.py` — and the old anchor must not be the thing that
        vouches for its own replacement. No node ran that; the reviewer had to
        construct it by hand to find [C2], and the probe was not kept. This
        keeps it.

        The candidate's checker is modified in a way that is real (the bytes
        differ, the closure delta is real, both loaders' checklists must match
        the candidate) while staying executable, because the whole point is that
        the *candidate's* checker is what runs in both stages.
        """
        import hashlib
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        rel = "bootstrap/tests/_gate_preflight.py"
        original = (repo / rel).read_text(encoding="utf-8")
        (repo / rel).write_text(
            original + "\n# reviewed change to the checker itself ([D2])\n",
            encoding="utf-8")
        resolved = _signed_commit(repo, "a reviewed change to the checker")
        assert _blob_sha(repo, anchor, rel) != _blob_sha(repo, resolved, rel), (
            "the fixture must genuinely differ, or this proves nothing")

        manifest = tmp_path / "review.txt"
        manifest.write_text(_review_manifest(repo, resolved), encoding="utf-8")

        loader = _substitute(_transition_block(), repo, hashes=False)
        loader = loader.replace("<candidate-ref-or-oid-to-transition-to>",
                                shlex.quote(resolved))
        loader = loader.replace(
            "<absolute-path-of-the-maintainer-recorded-review-manifest>",
            shlex.quote(str(manifest)))
        pkg = repo.parent / "authorization-package.json"
        if pkg.exists():
            pkg.unlink()
        with _n4_precondition(tmp_path / "maint"):
            r1 = subprocess.run(["bash", "-c", loader], cwd=str(repo),
                                capture_output=True, text=True, check=False)
        assert r1.returncode == 0, f"{r1.stderr[-3000:]}"
        assert pkg.exists()

        confirmed = hashlib.sha256(pkg.read_bytes()).hexdigest()
        script = _substitute(_stage2_transition_block(), repo, hashes=False,
                             candidate=resolved)
        for placeholder, value in (
                ("<the-64-hex-digest-you-verified-in-step-1>", confirmed),
                ("<absolute-path-of-the-maintainer-recorded-review-manifest>",
                 str(manifest)),
                ("<the-full-commit-oid-the-transition-loader-resolved-and-printed>",
                 resolved)):
            script = script.replace(placeholder, shlex.quote(value))
        r2 = subprocess.run(["bash", "-c", script], cwd=str(repo),
                            capture_output=True, text=True, check=False)
        assert r2.returncode == 0, f"{r2.stderr[-3000:]}"

        new_anchor = _run("git", "rev-parse", P._ANCHOR_REF,
                          cwd=repo).stdout.strip()
        assert new_anchor != anchor
        assert _run("git", "log", "-1", "--format=%G?",
                    cwd=repo).stdout.strip() == "G"
        # And the newly anchored checker is the CANDIDATE's, not the old one.
        assert _blob_sha(repo, new_anchor, rel) == _blob_sha(repo, resolved, rel)
        recovered = P.parse_admitted_authority(
            _run("git", "log", "-1", "--format=%B", cwd=repo).stdout)
        assert rel in recovered, (
            "the checker's own change is not in the admitted set the "
            "checkpoint records")

    def test_the_recorded_stage2_extracts_and_verifies_its_own_bytes(self):
        """D4: stage 2 starts from **separately** hash-verified bytes.

        Reusing stage 1's temp directory would be the tempting simplification,
        and it is wrong for a specific reason: candidate code executed during
        stage 1, as the same user, while that directory sat on disk. The signing
        stage would then run bytes the candidate had a window to rewrite. So the
        recorded block must carry its own extraction and its own checklist --
        the duplication is the control.
        """
        block = _stage2_block()
        assert "<maintainer-recorded-first-use-hashes>" in block, (
            "stage 2 has no checklist of its own")
        assert 'cat-file blob "refs/cairn/gate-anchor:$path"' in block, (
            "stage 2 does not extract from the anchor itself")
        assert '"$SHASUM" -a 256 -c RECORDED.sha256' in block, (
            "stage 2 does not verify the bytes it is about to execute")
        # And it must not simply inherit stage 1's directory by name.
        assert "from-stage-1" not in block

    def test_the_extraction_directory_is_not_itself_a_repository(self, tmp_path):
        """The premise the FUR5 shape depends on: were `$T` a repository, the
        no-`--repo` default would have silently worked and hidden the defect."""
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        extract = tmp_path / "T"
        _extract_anchored(repo, extract)
        assert not (extract / ".git").exists()

    @pytest.mark.parametrize("stage", ["stage1", "stage2"])
    def test_omitting_repo_refuses_diagnosably_and_moves_nothing(self, tmp_path,
                                                                 stage):
        """The exact FUR5 defect. It was fail-closed but undiagnosable: git's
        bare `fatal: not a git repository` names neither the cause nor the fix.

        Both stages are covered because both are anchored invocations run from
        the extraction directory, and each would have its own way of guessing a
        target. The refusal happens before argument-specific work, so the
        required flags below are placeholders pointing nowhere.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        checker = _extract_anchored(repo, tmp_path / "T")
        before = (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                  _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip())

        flags = (["--signing-key", str(tmp_path / "maint.pub"),
                  "--package-out", str(tmp_path / "unwritten.json")]
                 if stage == "stage1"
                 else ["--package", str(tmp_path / "absent.json"),
                       "--signing-key", str(tmp_path / "maint.pub"),
                       "--confirm-package-sha256", "0" * 64])
        r = self._cli(checker, stage, *flags)

        assert r.returncode == 2
        assert not (tmp_path / "unwritten.json").exists()
        assert "--repo <checkout>" in r.stderr
        assert "not a git repository" in r.stderr
        assert (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                _run("git", "rev-parse", P._ANCHOR_REF,
                     cwd=repo).stdout.strip()) == before

    def test_an_extraction_nested_in_another_repo_refuses_that_repo(
            self, tmp_path):
        """Why "not a git repository" was luck, not design.

        `git -C <path>` discovers upward. Put the extraction anywhere beneath a
        repository -- a `$TMPDIR` inside a checkout is enough -- and the
        no-`--repo` invocation finds *that* repository and operates on it,
        reporting against a target the operator never named.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        (tmp_path / "outer").mkdir()
        outer = _repo(tmp_path / "outer")
        _commit(outer, "innocent bystander")
        checker = _extract_anchored(repo, outer / "T")

        r = self._cli(checker, "check")

        assert r.returncode == 2
        assert "not the top level of a git worktree" in r.stderr
        assert "walking upward" in r.stderr
        assert str(outer.resolve()) in r.stderr

    def test_the_loader_never_discovers_the_checkout_ambiently(self):
        """Properties of the recorded text that an execution test cannot see,
        because a substituted repository answers correctly right up until it
        doesn't (FUR6). Read raw -- no fixture substitution."""
        block = _runbook_block("_gate_preflight.py")
        # Comments are stripped first. An earlier version of this assertion
        # fired on the comment *explaining* why `git archive` is not used --
        # the same false-positive shape as the containment lint deleted in the
        # security code review, where every hit was prose and none was code.
        lines = [ln for ln in block.splitlines()
                 if ln.strip() and not ln.lstrip().startswith("#")]
        code = "\n".join(lines)

        assert "rev-parse --show-toplevel" not in code, (
            "the checkout must be recorded, not derived: `git -C` discovers "
            "upward, so discovery can answer with a repository never named")
        assert "git archive" not in code and "archive " not in code, (
            "`git archive` is attribute-aware; the loader reads raw blobs")
        assert "--no-replace-objects" in code and "core.hooksPath" in code

        def first(needle):
            return next(i for i, ln in enumerate(lines) if needle in ln)

        assert first("--no-replace-objects") < first("cat-file"), (
            "replacement must be disabled before the first object read")
        assert first('"$SHASUM"') < first('"$PY"'), (
            "the extracted bytes must be verified before Python executes them")


# --------------------------------------------------------------------------
# FUR4 -- signature-history enumeration must not fail open
#
# `_rev_list` returned `[]` on any git error, so "the signed range cannot be
# established" became "there is nothing to check". With the epoch object
# missing, an unsigned commit inside `anchor..HEAD` was reported as
# grandfathered and no finding was emitted.
# --------------------------------------------------------------------------



# --------------------------------------------------------------------------
# FUR3 -- static manifest authority is no longer delegated
#
# `apply` correctly ignored a tampered evidence FILE (the CR1 redesign holds).
# But it materialized the candidate tree with `git archive`, which honours
# in-tree `.gitattributes`, and validated only the candidate SHA, an adjacent
# digest, and the interpreter. A signed candidate that added a tracked module
# under the frozen directory plus a `.gitattributes` marking it `export-ignore`
# got a commit blessed whose tree held the file while its manifest did not pin
# it -- so "the evidence is non-authoritative" and "check re-derives every
# static Git fact" were both false for file identity.
# --------------------------------------------------------------------------

class TestRawTreeMaterialization:

    def test_export_ignore_cannot_hide_a_tracked_file(self, tmp_path):
        repo = _repo(tmp_path)
        _write(repo, "bootstrap/tests/normal.py", "x = 1\n")
        _write(repo, "bootstrap/tests/omitted.py", "hidden = True\n")
        _write(repo, ".gitattributes",
               "bootstrap/tests/omitted.py export-ignore\n")
        head = _commit(repo, "with an export-ignore")

        # The attack is live: `git archive` drops it while the tree keeps it.
        archived = subprocess.run(
            f"git -C {shlex.quote(str(repo))} archive --format=tar HEAD | tar -t",
            shell=True, capture_output=True, text=True)
        assert "bootstrap/tests/omitted.py" not in archived.stdout

        with P.raw_tree(head, repo=repo) as tree:
            assert (tree / "bootstrap/tests/omitted.py").exists()
            assert (tree / "bootstrap/tests/normal.py").exists()

    def test_a_tracked_symlink_refuses_rather_than_being_written(self, tmp_path):
        repo = _repo(tmp_path)
        (repo / "target.txt").write_text("real\n", encoding="utf-8")
        (repo / "link.txt").symlink_to("target.txt")
        head = _commit(repo, "with a symlink")
        with pytest.raises(P.PreflightError, match="non-regular"):
            with P.raw_tree(head, repo=repo):
                pass

    def test_executable_bits_survive_materialization(self, tmp_path):
        repo = _repo(tmp_path)
        script = repo / "run.sh"
        script.write_text("#!/bin/sh\n", encoding="utf-8")
        script.chmod(0o755)
        head = _commit(repo, "executable")
        with P.raw_tree(head, repo=repo) as tree:
            import os as _os
            assert _os.access(tree / "run.sh", _os.X_OK)


@pytest.fixture(autouse=True)
def _reset_key_load_phase():
    """Reset the key-load phase around **every** test in this file.

    The boundary is deliberately irreversible in production code -- `apply_now`
    seals module state and there is no unseal -- which is correct for a CLI that
    runs one ceremony per process, and leaks in a test session where many do.
    Without this, any node that completes a real `apply` seals the module and
    every later node inherits it.

    That is exactly the shared-mutable-fixture defect fixed in
    `test_verify_ref.py` the same day (`da26a88`), reintroduced here by the
    author of that fix within hours. Hence file-scoped and autouse rather than
    scoped to the sentinel class: the leak is caused by tests *elsewhere* in
    this file, so a guard living only in the class that noticed it would not
    hold.
    """
    P._phase = P._PHASE_CANDIDATE
    yield
    P._phase = P._PHASE_CANDIDATE


# ---------------------------------------------------------------------------
# Chunk H2: the key-load phase sentinel.
#
# Acceptance criterion 8 -- "no candidate execution after the key-load marker,
# **proven by sentinel, not by inspection**". R1-F steps 4-5 put the ceremony in
# two phases: candidate code runs freely while the signing key is unavailable,
# the Maintainer confirms against a hard marker, and only then does the key
# load. Nothing after that line may execute or import candidate code.
#
# THIS IS SEQUENCING, NOT CONTAINMENT, and these tests do not claim otherwise.
# Candidate code that ran before the marker shared an uncompartmented machine
# with the key that loads after it, and may have left persistence no later
# process can see. What the boundary removes is *simultaneous intentional*
# availability. A separate evidence host or a hardware-presence key is the
# strengthening path; neither exists.
# ---------------------------------------------------------------------------


class TestKeyLoadPhaseSentinel:

    def test_the_boundary_starts_open(self):
        assert P._phase == P._PHASE_CANDIDATE
        P.refuse_if_sealed("anything")          # must not raise

    def test_sealing_refuses_the_evidence_stage(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        P.seal_candidate_execution(out=io.StringIO())
        with pytest.raises(P.PreflightError) as exc:
            P.gather_evidence("HEAD", repo=repo, out=io.StringIO())
        assert "after the key-load phase marker" in str(exc.value)

    def test_every_candidate_executing_entry_point_is_guarded(self):
        """The criterion says *every* entry point, so this enumerates them from
        the source rather than trusting a list someone maintained by hand.

        A subprocess launch is the capability that matters: collection, imports,
        hooks and filters all reach candidate code through one. So every
        `subprocess.run` in this module that is **not** the sterile git launcher
        must sit behind `refuse_if_sealed`.
        """
        import ast
        src = (P._REPO / "bootstrap/tests/_gate_preflight.py").read_text(
            encoding="utf-8")
        tree = ast.parse(src)

        guarded, unguarded = [], []
        for fn in ast.walk(tree):
            if not isinstance(fn, ast.FunctionDef):
                continue
            launches = [n for n in ast.walk(fn)
                        if isinstance(n, ast.Call)
                        and getattr(n.func, "attr", "") == "run"
                        and getattr(getattr(n.func, "value", None), "id", "")
                        == "subprocess"]
            if not launches:
                continue
            if fn.name == "_run_git":
                continue          # the sterile git launcher: fixed plumbing
            calls = {getattr(n.func, "id", "") for n in ast.walk(fn)
                     if isinstance(n, ast.Call)}
            (guarded if "refuse_if_sealed" in calls else unguarded).append(
                fn.name)

        assert not unguarded, (
            f"these functions launch a subprocess with no key-load guard: "
            f"{unguarded}. Every route to candidate execution must refuse "
            f"after the marker, not merely the documented one.")
        assert guarded, "the enumeration found nothing; the walk is broken"

    def test_the_marker_is_printed_where_a_human_will_see_it(self):
        """The Maintainer confirms *against* the marker (R1-F step 4), so a
        silent seal would remove the thing being confirmed."""
        buf = io.StringIO()
        P.seal_candidate_execution(out=buf)
        printed = buf.getvalue()
        assert "KEY-LOAD PHASE MARKER" in printed
        assert "SEALED" in printed
        assert "NOT containment" in printed, (
            "the marker must not let a reader believe this contains anything")

    def test_the_boundary_does_not_reopen(self):
        """A reversible boundary is not one. The failure this exists to prevent
        is a later stage deciding it needs one more collection."""
        P.seal_candidate_execution(out=io.StringIO())
        assert not any(
            name for name in dir(P)
            if "unseal" in name.lower() or "reopen" in name.lower()), (
            "an unseal entry point exists; the boundary is reversible")
        with pytest.raises(P.PreflightError):
            P.refuse_if_sealed("a second collection")

    def test_apply_seals_before_the_key_loads_not_after(self):
        """Ordering is the whole control, so it is asserted on the source: the
        seal must precede the first operation that loads the signing key."""
        import ast
        src = (P._REPO / "bootstrap/tests/_gate_preflight.py").read_text(
            encoding="utf-8")
        fn = next(n for n in ast.walk(ast.parse(src))
                  if isinstance(n, ast.FunctionDef) and n.name == "apply_now")
        seal = signing = None
        for node in ast.walk(fn):
            if not isinstance(node, ast.Call):
                continue
            name = getattr(node.func, "id", "")
            if name == "seal_candidate_execution" and seal is None:
                seal = node.lineno
            if name == "_construct_signed_commit" and signing is None:
                signing = node.lineno
        assert seal is not None, "apply never seals candidate execution"
        assert signing is not None, "apply never constructs the signed commit"
        assert seal < signing, (
            f"the seal is at line {seal} and the key loads at {signing}; the "
            f"key must not be loadable while candidate code may still run")

    def test_stage1_never_reaches_a_signing_call_at_all(self):
        """D3: "it never holds the key" as a property of the source.

        The ordering node above is about `apply_now`, where a seal precedes the
        key. Stage 1 is a stronger claim -- not "seals first" but "does not
        sign, ever" -- and ordering cannot express it. Asserted on the AST
        because the runtime evidence for it is an *absence*, and a test that
        merely observes stage 1 not signing on one path proves nothing about
        the others.
        """
        import ast
        src = (P._REPO / "bootstrap/tests/_gate_preflight.py").read_text(
            encoding="utf-8")
        fn = next(n for n in ast.walk(ast.parse(src))
                  if isinstance(n, ast.FunctionDef) and n.name == "stage1")
        called = {getattr(n.func, "id", "") or getattr(n.func, "attr", "")
                  for n in ast.walk(fn) if isinstance(n, ast.Call)}
        for forbidden in ("_construct_signed_commit", "_sign", "apply_now",
                          "_transact"):
            assert forbidden not in called, (
                f"stage 1 calls {forbidden}; the stage that runs candidate code "
                f"must not be able to sign or move anything")
        assert "require_stage1_cannot_sign" in called, (
            "stage 1 does not probe the key channel; the refusal that makes "
            "the boundary real would be absent")

    def test_the_ordering_holds_through_a_REAL_apply(self, tmp_path,
                                                     monkeypatch):
        """Executed end to end, not read off the source.

        Uses the full-ceremony fixture, so the run really constructs and signs
        a checkpoint and moves both refs. The source-order node above can only
        prove the call sites are in the right order; this proves the ordering
        survives an actual ceremony -- and that the seal is reached at all,
        which an early return would silently skip.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        manifest = {**P.rederive_static_manifest(head, repo=repo),
                    "collection": {"node_count": 1, "node_ids": ["a.py::t"],
                                   "skip_xfail_marked": []},
                    "interpreter": {"version": "3.13.13"}}
        order = []
        real_seal = P.seal_candidate_execution

        def traced_gather(*a, **k):
            order.append("candidate-execution")
            return _fake_evidence(head, manifest)

        def traced_seal(*a, **k):
            order.append("seal")
            return real_seal(*a, **k)

        monkeypatch.setattr(P, "gather_evidence", traced_gather)
        monkeypatch.setattr(P, "seal_candidate_execution", traced_seal)

        result = _two_stage(repo, monkeypatch)

        # Two stages, so two seals -- and the shape carries the D3 contract.
        # Candidate code runs exactly once, in stage 1, and every seal follows
        # it; stage 2 seals with nothing executed in between. `_two_stage`
        # resets the phase between the stages because stage 2 is a fresh
        # process in reality, so the second seal is a real up-front seal and not
        # a leftover from the first.
        assert order == ["candidate-execution", "seal", "seal"], order
        assert order.count("candidate-execution") == 1, (
            f"candidate code executed more than once: {order}")
        assert "candidate-execution" not in order[order.index("seal"):], (
            f"candidate code ran after a seal: {order}")
        assert result["new_anchor"], "the ceremony did not complete"
        assert P._phase == P._PHASE_SEALED, (
            "apply returned with candidate execution still permitted")


# ---------------------------------------------------------------------------
# Chunk A: source selection lives in the LOADER, not in the code it selects.
#
# Plan review [E3]: `_gate_preflight.py` runs only AFTER the candidate bytes
# have been chosen and executed, so a Python check cannot establish which Python
# was safe to run. These nodes therefore execute the runbook's own transition
# block and assert on what happens BEFORE any interpreter starts.
# ---------------------------------------------------------------------------


def _review_manifest(repo: Path, oid: str, *, members=None,
                     schema="cairn-review-manifest/v1",
                     provenance="external security review 2026-08-12") -> str:
    """A well-formed manifest over the candidate's real closure bytes."""
    import hashlib
    rows = [f"schema {schema}", f"candidate {oid}", f"provenance {provenance}"]
    if members is None:
        members = []
        for rel in sorted(P.declared_authority_closure()):
            blob = subprocess.run(
                ["git", "-C", str(repo), "cat-file", "blob", f"{oid}:{rel}"],
                capture_output=True).stdout
            members.append((hashlib.sha256(blob).hexdigest(), rel))
    rows += [f"member {d} {r}" for d, r in members]
    return "\n".join(rows) + "\n"


class TestTransitionLoaderSelectsTheSource:

    def _script(self, repo: Path, manifest_path: Path, candidate: str) -> str:
        block = _transition_block()
        block = block.replace("<candidate-ref-or-oid-to-transition-to>",
                              shlex.quote(candidate))
        block = block.replace(
            "<absolute-path-of-the-maintainer-recorded-review-manifest>",
            shlex.quote(str(manifest_path)))
        return _substitute(block, repo, hashes=False)

    def _run(self, repo, manifest_text, candidate, tmp_path):
        mf = tmp_path / "review-manifest.txt"
        mf.write_text(manifest_text, encoding="utf-8")
        script = self._script(repo, mf, candidate)
        return subprocess.run(["bash", "-c", script], cwd=str(repo),
                              capture_output=True, text=True, check=False)

    def test_the_recorded_transition_loader_parses_a_good_manifest(
            self, tmp_path):
        """The loader's own bytes, executed. It will refuse later for ceremony
        reasons this fixture cannot satisfy; what this asserts is that it gets
        *past source selection* on a well-formed manifest."""
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        r = self._run(repo, _review_manifest(repo, head), head, tmp_path)
        assert "REFUSE:" not in r.stderr, (
            f"a well-formed manifest was refused at selection:\n{r.stderr[-1500:]}")

    @pytest.mark.parametrize("mutation,expect", [
        ("schema", "unknown manifest schema"),
        ("order", "sorted order"),
        ("duplicate", "sorted order"),
        ("digest_case", "lowercase hex"),
        ("digest_len", "64 characters"),
        ("control", "control character"),
        ("no_candidate", "no candidate row"),
        ("no_provenance", "no provenance row"),
        ("long_provenance", "120 characters"),
        ("absolute_path", "not repository-relative"),
        ("wrong_oid", "review manifest names"),
        ("bad_digest", "do not match the reviewed manifest"),
    ])
    def test_each_rejection_refuses_before_any_python_starts(
            self, tmp_path, mutation, expect):
        """[E3]'s core requirement. Every one of these is a *selection* failure,
        so the correct outcome is not "the checker refused" -- it is that **no
        interpreter ran at all**."""
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        rows = _review_manifest(repo, head).splitlines()

        def member_rows():
            return [i for i, r in enumerate(rows) if r.startswith("member ")]

        if mutation == "schema":
            rows[0] = "schema cairn-review-manifest/v2"
        elif mutation == "order":
            m = member_rows()
            rows[m[0]], rows[m[-1]] = rows[m[-1]], rows[m[0]]
        elif mutation == "duplicate":
            rows.append(rows[member_rows()[0]])
        elif mutation == "digest_case":
            i = member_rows()[0]
            parts = rows[i].split()
            rows[i] = f"member {parts[1].upper()} {parts[2]}"
        elif mutation == "digest_len":
            i = member_rows()[0]
            parts = rows[i].split()
            rows[i] = f"member {parts[1][:63]} {parts[2]}"
        elif mutation == "control":
            rows[2] = "provenance review\x07bell"
        elif mutation == "no_candidate":
            rows = [r for r in rows if not r.startswith("candidate ")]
        elif mutation == "no_provenance":
            rows = [r for r in rows if not r.startswith("provenance ")]
        elif mutation == "long_provenance":
            rows[2] = "provenance " + ("x" * 121)
        elif mutation == "absolute_path":
            i = member_rows()[0]
            parts = rows[i].split()
            rows[i] = f"member {parts[1]} /etc/passwd"
        elif mutation == "wrong_oid":
            rows[1] = "candidate " + ("a" * 40)
        elif mutation == "bad_digest":
            i = member_rows()[0]
            parts = rows[i].split()
            rows[i] = f"member {'0' * 64} {parts[2]}"

        text = "\n".join(rows) + "\n"
        if mutation == "control":
            text = text.replace("\\x07", "\x07")

        r = self._run(repo, text, head, tmp_path)

        assert r.returncode != 0, f"the mutation was accepted:\n{r.stdout[-800:]}"
        assert expect in r.stderr, (
            f"expected {expect!r} in the refusal, got:\n{r.stderr[-1200:]}")
        assert "Traceback" not in r.stderr, (
            "a Python interpreter started on a selection failure; selection "
            "must refuse before any interpreter runs")

    def test_the_loader_extracts_by_resolved_oid_not_by_a_moving_ref(self):
        """A ref read twice is two answers wearing one name. Asserted on the
        recorded text, since the property is which *expression* is used."""
        block = _transition_block()
        code = "\n".join(ln for ln in block.splitlines()
                          if ln.strip() and not ln.lstrip().startswith("#"))
        assert 'cat-file blob "$RESOLVED:$path"' in code, (
            "extraction must use the once-resolved OID")
        assert 'cat-file blob "$CANDIDATE' not in code, (
            "extraction must never read through the candidate ref")
        assert code.count("rev-parse --verify --end-of-options") == 1, (
            "the candidate is resolved exactly once")

    def test_both_parsers_reject_a_row_with_leading_whitespace(self, tmp_path):
        """Code review [C4]. One artifact, two parsers, two answers.

        `raw.split()` ignores leading whitespace so the Python side classified
        an indented row by its first word, then took `provenance` by slicing at
        a fixed offset -- while the loader's `${line#provenance }` does not
        match an indented prefix and kept the whole line. Two readings of one
        recorded artifact is the condition an out-of-band trust input cannot
        have, whichever value is "right".

        Both sides now refuse it, and both are checked here: the Python
        revalidation directly, and the recorded loader by execution.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        honest = _review_manifest(repo, head)

        # Code review [D1]: the first fix relocated the divergence instead of
        # removing it. The loader's check ran BEFORE its blank/comment case and
        # Python's ran after, so three shapes that are not rows at all -- an
        # indented comment, a whitespace-only line, a trailing line of spaces --
        # were refused by one side and accepted by the other. All six shapes are
        # pinned here, in both directions, so neither side can drift alone.
        cases = {
            "honest": (honest, True),
            "indented provenance": (
                honest.replace("provenance ", "   provenance ", 1), False),
            "tab-indented member": (
                honest.replace("\nmember ", "\n\tmember ", 1), False),
            "indented comment": (honest + "   # a note\n", True),
            "whitespace-only line": (honest + "   \n", True),
            "trailing line of spaces": (honest + "  ", True),
        }
        for name, (text, should_pass) in cases.items():
            if should_pass:
                P.parse_review_manifest(text)          # must not raise
            else:
                with pytest.raises(P.ReviewManifestError,
                                   match="leading whitespace"):
                    P.parse_review_manifest(text)

            r = self._run(repo, text, head, tmp_path)
            loader_ok = "review manifest" not in r.stderr \
                and "leading whitespace" not in r.stderr
            assert loader_ok == should_pass, (
                f"{name}: the loader and the Python revalidation disagree "
                f"about whether this is an acceptable manifest "
                f"(loader_ok={loader_ok}, python_ok={should_pass})\n"
                f"{r.stderr[-500:]}")

    def test_the_anchored_steady_state_loader_has_no_transition_mode(self):
        """[S1] as a test. The anchored checker cannot contain a mode added to
        its successor, so the steady-state block must not offer one -- if it
        did, the old authority would be vouching for its replacement."""
        steady = _runbook_block("_gate_preflight.py")
        assert "--transition-from-review" not in steady
        assert "REVIEW_MANIFEST" not in steady

    @pytest.mark.parametrize("stage", ["stage1", "stage2"])
    @pytest.mark.parametrize("half", ["candidate-only", "manifest-only"])
    def test_transition_mode_needs_both_flags_or_refuses(self, tmp_path, stage,
                                                        half):
        """One flag alone is not a mode -- **on both stages**.

        A half-specified transition must not fall back to steady state, which
        would run the ceremony with the selection predicate silently skipped.

        Both stages are covered because each revalidates the transition
        independently (D4 defence in depth). Checking stage 1 alone would leave
        stage 2 able to sign a *steady-state* checkpoint -- one whose message
        records "no closure change" -- for a run the loader selected in
        transition mode. The admitted authority set would simply be absent from
        the durable record, which is the [E4] failure with extra steps.
        """
        repo, anchor, head = _anchored_repo(tmp_path)
        checker = _REPO / "bootstrap/tests/_gate_preflight.py"
        manifest = tmp_path / "review.txt"
        manifest.write_text("unused -- the refusal precedes any read\n")
        flags = (["--reviewed-candidate", head] if half == "candidate-only"
                 else ["--transition-from-review", str(manifest)])
        required = (["--signing-key", str(tmp_path / "k.pub"),
                     "--package-out", str(tmp_path / "pkg.json")]
                    if stage == "stage1"
                    else ["--package", str(tmp_path / "pkg.json"),
                          "--signing-key", str(tmp_path / "maint.pub"),
                          "--confirm-package-sha256", "0" * 64])
        r = subprocess.run(
            [sys.executable, "-E", "-s", str(checker), stage,
             "--repo", str(repo), *required, *flags],
            capture_output=True, text=True, check=False)
        assert r.returncode == 2
        assert "one alone is not a mode" in r.stderr
        # The refusal must precede the work, not follow it: neither the key
        # probe nor the package read may have run.
        assert "STAGE 1 CAN SIGN" not in r.stderr
        assert not (tmp_path / "pkg.json").exists()

    @pytest.mark.parametrize("shape", ["extra-member", "missing-member"])
    def test_a_wrong_member_SET_starts_no_interpreter(self, tmp_path, shape):
        """Security review [M2-R1], with the evidence it asked for.

        The loader validated the manifest against *itself* — rows well-formed,
        paths sorted and unique, digests matching the bytes it extracted for
        those paths — and never compared the member set against a fixed list.
        A manifest that dropped a member or added one therefore parsed cleanly,
        extracted cleanly, and **started Python**; the first exact-set check was
        `revalidate_transition()` inside the candidate bytes the loader had
        already selected and run. Fail-closed for ref movement, and still wrong:
        a check performed by the candidate cannot establish that the candidate
        was safe to start.

        **The interpreter is replaced by a marker wrapper**, because the absence
        of a traceback is not evidence that no interpreter ran — that was
        precisely how this passed before. The manifests below are internally
        consistent: correctly sorted, uniquely pathed, and correctly hashed, so
        nothing but the fixed-set comparison can reject them.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        _write(repo, "bootstrap/tests/_oracle.py", "# a reviewed change\n")
        resolved = _signed_commit(repo, "reviewed authority change")

        marker = tmp_path / "PYTHON_STARTED"
        wrapper = tmp_path / "py-wrapper"
        wrapper.write_text(
            f"#!/bin/sh\ntouch {shlex.quote(str(marker))}\n"
            f"exec {shlex.quote(sys.executable)} \"$@\"\n")
        wrapper.chmod(0o755)

        import hashlib
        members = []
        for rel in sorted(P.declared_authority_closure()):
            blob = subprocess.run(
                ["git", "-C", str(repo), "cat-file", "blob", f"{resolved}:{rel}"],
                capture_output=True).stdout
            members.append((hashlib.sha256(blob).hexdigest(), rel))
        if shape == "extra-member":
            extra = "bootstrap/tests/_unreviewed_extra.py"
            _write(repo, extra, "SNEAKED = True\n")
            resolved = _signed_commit(repo, "an unreviewed extra member")
            # Re-hash against the new commit so only the SET is wrong.
            members = []
            for rel in sorted(set(P.declared_authority_closure()) | {extra}):
                blob = subprocess.run(
                    ["git", "-C", str(repo), "cat-file", "blob",
                     f"{resolved}:{rel}"], capture_output=True).stdout
                members.append((hashlib.sha256(blob).hexdigest(), rel))
        else:
            members = [m for m in members
                       if m[1] != "bootstrap/REANCHOR_RUNBOOK.md"]

        text = _review_manifest(repo, resolved, members=members)
        script = self._script(repo, tmp_path / "mf.txt", resolved)
        (tmp_path / "mf.txt").write_text(text, encoding="utf-8")
        script = script.replace(shlex.quote(sys.executable),
                                shlex.quote(str(wrapper)))
        assert str(wrapper) in script, "the marker interpreter was not injected"

        r = subprocess.run(["bash", "-c", script], cwd=str(repo),
                           capture_output=True, text=True, check=False)

        assert r.returncode != 0, "a wrong member set was accepted"
        assert not marker.exists(), (
            f"{shape}: candidate Python STARTED before the fixed member set was "
            f"checked -- the loader deferred the exact-set comparison to the "
            f"bytes it had already run\n{r.stderr[-800:]}")
        assert "not the authority closure" in r.stderr, r.stderr[-800:]

    def test_the_marker_interpreter_probe_is_live(self, tmp_path):
        """Guards the node above. If the wrapper were never invoked on an
        HONEST manifest either, that test would pass while proving nothing."""
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        _write(repo, "bootstrap/tests/_oracle.py", "# a reviewed change\n")
        resolved = _signed_commit(repo, "reviewed authority change")
        marker = tmp_path / "PYTHON_STARTED"
        wrapper = tmp_path / "py-wrapper"
        wrapper.write_text(
            f"#!/bin/sh\ntouch {shlex.quote(str(marker))}\n"
            f"exec {shlex.quote(sys.executable)} \"$@\"\n")
        wrapper.chmod(0o755)

        (tmp_path / "mf.txt").write_text(_review_manifest(repo, resolved),
                                         encoding="utf-8")
        script = self._script(repo, tmp_path / "mf.txt", resolved)
        script = script.replace(shlex.quote(sys.executable),
                                shlex.quote(str(wrapper)))
        with _n4_precondition(tmp_path / "maint"):
            subprocess.run(["bash", "-c", script], cwd=str(repo),
                           capture_output=True, text=True, check=False)

        assert marker.exists(), (
            "the marker interpreter never ran even on an honest manifest, so "
            "the probe above cannot distinguish 'refused early' from 'never "
            "wired up'")

    def test_stage2_actually_receives_the_transition_flags_it_declares(self):
        """A declared flag that no call site consumes is [M2-1] again.

        The `stage2` parser grew `--transition-from-review` and
        `--reviewed-candidate` before `apply_now` was given them, so the
        revalidation they exist to trigger was unreachable through the public
        path -- built, tested in isolation, dead to the governing route. This
        reads the dispatch source rather than the parser, because the parser
        declaring them is precisely the state that looked correct.
        """
        tree = ast.parse(
            (_REPO / "bootstrap/tests/_gate_preflight.py").read_text())
        main = next(n for n in tree.body
                    if isinstance(n, ast.FunctionDef) and n.name == "main")
        calls = [n for n in ast.walk(main)
                 if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Name) and n.func.id == "apply_now"]
        assert len(calls) == 1, (
            f"`main` should reach the signing stage through exactly one "
            f"`apply_now` call; found {len(calls)}")
        passed = {kw.arg for kw in calls[0].keywords}
        for flag in ("review_manifest", "reviewed_candidate"):
            assert flag in passed, (
                f"`stage2` declares --{flag.replace('_', '-')} but never passes "
                f"it to apply_now; the revalidation it exists to trigger is "
                f"unreachable through the public path")


class TestTheCheckpointCarriesTheAdmittedSet:
    """Chunk D7/D8 and plan review [E4].

    The opening A3 question was whether the checkpoint records the admitted
    authority set itself or only binds its digest. The Maintainer accepted the
    proposal with that open, and D6 required a decision rather than a lapse:
    **the set is written**. A digest binds cryptographically and is unreadable,
    and the review manifest is an out-of-band artifact that may not survive --
    so digest-only leaves a future reader able to prove that *a* set was
    admitted and unable to see which bytes.

    These nodes run entirely on the constructed message, before any ref moves.
    """

    _ADMITTED = {
        "bootstrap/tests/_gate_manifest.py": "a" * 64,
        "bootstrap/tests/_gate_preflight.py": "b" * 64,
        "bootstrap/tests/_oracle.py": "c" * 64,
    }

    def _message(self, admitted=None, *, digest="d" * 64, provenance="ESR 1"):
        return P.draft_message(
            observed_anchor="0" * 40, checked_head="1" * 40,
            manifest_sha256="e" * 64, authority_hashes={"x.py": "sha256:" + "f" * 64},
            scope={}, admitted_authority=(self._ADMITTED if admitted is None
                                          else admitted),
            review_provenance=provenance, review_digest=digest)

    def test_the_complete_set_reads_back_out_of_the_message(self):
        """The durability claim, executed. Not "the rows look right" -- the set
        is recovered from the message text and compared with what went in."""
        recovered = P.parse_admitted_authority(self._message())
        assert recovered == self._ADMITTED, (
            "the admitted set did not survive a round trip through the "
            "checkpoint message; the record is a pointer, not a record")

    def test_the_rows_are_written_in_sorted_path_order(self):
        """Order is part of the record: an unordered set read back by a future
        auditor cannot be compared against anything without re-sorting, and a
        stable order is what makes two checkpoints diffable."""
        message = self._message(dict(reversed(list(self._ADMITTED.items()))))
        rows = [ln for ln in message.splitlines() if ln.startswith("    ")
                and ln.strip().split("  ")[0].isalnum()]
        paths = [ln.strip().split("  ", 1)[1] for ln in rows]
        assert paths == sorted(self._ADMITTED), paths

    def test_the_review_manifest_digest_is_bound_alongside_the_rows(self):
        """D7. The rows say what was admitted; the digest says which reviewed
        artifact admitted it. Without it, two different reviews of the same
        bytes are indistinguishable in the durable record."""
        assert "d" * 64 in self._message()
        assert "(not bound)" in self._message(digest=None)

    @pytest.mark.parametrize("victim", sorted(_ADMITTED))
    def test_a_single_row_mutation_changes_the_message(self, victim):
        """D8. Every row is load-bearing, one at a time.

        A block that is signed as a whole can still be decorative: if the
        message were assembled from a count and a provenance string, mutating
        one member's digest would leave the signed bytes identical and the
        anchored record would attest to a set it does not describe. So each row
        is mutated on its own and required to move the message.
        """
        honest = self._message()
        tampered = dict(self._ADMITTED)
        tampered[victim] = "9" * 64
        mutated = self._message(tampered)

        assert mutated != honest, (
            f"changing the admitted digest for {victim} did not change the "
            f"message; that row is not covered by the signature")
        recovered = P.parse_admitted_authority(mutated)
        assert recovered[victim] == "9" * 64
        assert {k: v for k, v in recovered.items() if k != victim} == \
            {k: v for k, v in self._ADMITTED.items() if k != victim}, (
            "a single-row mutation disturbed the other rows")

    def test_dropping_a_row_is_caught_by_the_declared_count(self):
        """Truncation is the mutation that reads as success.

        A short block still parses: it just yields a smaller set that looks
        complete. The count is written in the header and checked against the
        rows recovered, so a dropped row is a refusal rather than a quieter
        answer.
        """
        message = self._message()
        lines = message.splitlines()
        victim = next(i for i, ln in enumerate(lines)
                      if ln.startswith("    a" * 1) and "  " in ln.strip())
        del lines[victim]
        with pytest.raises(P.PreflightError) as exc:
            P.parse_admitted_authority("\n".join(lines))
        assert "admitted members" in str(exc.value)

    def test_steady_state_is_a_distinct_answer_from_an_empty_set(self):
        """`None` means "nothing changed", not "nothing was admitted". A
        steady-state checkpoint that read back as `{}` would be indistinguishable
        from a transition that admitted no members -- which cannot happen, and
        must not be representable."""
        steady = self._message({}, digest=None, provenance=None)
        assert P.parse_admitted_authority(steady) is None
        assert "steady state -- no closure change" in steady

    def test_the_set_reaches_the_message_through_a_real_two_stage_run(
            self, tmp_path, monkeypatch):
        """The [M2-1] question asked of D7: what calls this?

        Every node above builds the message directly. That is exactly the shape
        that let a canonical range report be derived, digested, tested -- and
        never bound by the governing path. So this one drives the real ceremony
        in transition mode and reads the set back out of the **committed
        checkpoint**, which is the only place it counts.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        # A real closure change, or the transition refuses with no delta ([S3]).
        changed = {"bootstrap/tests/_oracle.py"}
        _write(repo, "bootstrap/tests/_oracle.py", "# a reviewed change\n")
        head = _signed_commit(repo, "authority change")
        manifest = tmp_path / "review.txt"
        manifest.write_text(_review_manifest(repo, head), encoding="utf-8")

        # The real producer needs more repository than this fixture carries; the
        # evidence stage has its own coverage. Everything the node is about --
        # the transition, the message, the committed checkpoint -- stays real.
        evidence_manifest = {
            **P.rederive_static_manifest(head, repo=repo),
            "collection": {"node_count": 1, "node_ids": ["a.py::t"],
                           "skip_xfail_marked": []},
            "interpreter": {"version": "3.13.13"}}
        monkeypatch.setattr(
            P, "gather_evidence",
            lambda *a, **k: _fake_evidence(head, evidence_manifest))

        result = _two_stage(repo, monkeypatch, review_manifest=str(manifest),
                            reviewed_candidate=head)

        message = _run("git", "log", "-1", "--format=%B",
                       cwd=repo).stdout
        recovered = P.parse_admitted_authority(message)
        assert recovered, "the committed checkpoint records no admitted set"
        import hashlib
        assert hashlib.sha256(manifest.read_bytes()).hexdigest() in message, (
            "the checkpoint does not bind the review manifest's digest")
        expected = P.parse_review_manifest(
            manifest.read_text(encoding="utf-8"))["members"]
        assert recovered == expected
        assert changed <= set(recovered), (
            "a file whose authority bytes changed is absent from the admitted "
            "set the checkpoint records")


class TestTheClosureCheckAdmitsOnlyTheReviewedSet:
    """The rule that makes the transition reachable, and its negatives.

    Before this, `check_authority_closure` refused on *any* closure change while
    `revalidate_transition` refused when the closure was *unchanged*. The two
    conditions are complements, so a reviewed-authority transition could never
    complete: every real one died at the checks with a CLOSURE finding, and the
    machinery Chunks A and B built was unreachable through the governing path.
    Nothing failed, because nothing had ever run a transition end to end.

    Making it reachable means relaxing a refusal on a high-risk surface, so the
    admission is asserted here directly rather than inferred from the ceremony
    passing: exact digest, right path, nothing else.
    """

    def _changed(self, tmp_path):
        """An anchor, and a worktree whose closure member genuinely differs."""
        repo, anchor = _closure_repo(tmp_path)
        rel = "bootstrap/tests/_oracle.py"
        _write(repo, rel, "# a reviewed change\n")
        _commit(repo, "authority change")
        live = (repo / rel).read_bytes()
        import hashlib
        return repo, anchor, rel, hashlib.sha256(live).hexdigest()

    def _closure(self, repo, anchor, admitted):
        report = P.Report()
        P.check_authority_closure(anchor, report, repo=repo,
                                  admitted_authority=admitted)
        return report

    def test_without_an_admitted_set_a_changed_member_refuses(self, tmp_path):
        """Steady state is unchanged: this is the control the relaxation must
        not have weakened, and it is asserted first for that reason."""
        repo, anchor, rel, _sha = self._changed(tmp_path)
        report = self._closure(repo, anchor, None)
        assert report.blocked
        assert any(rel in f.message and f.level == "review"
                   for f in _findings(report, "CLOSURE"))

    def test_the_exact_reviewed_digest_admits_the_member(self, tmp_path):
        repo, anchor, rel, sha = self._changed(tmp_path)
        report = self._closure(repo, anchor, {rel: sha})
        assert not report.blocked, [f.message for f in report.findings]
        noted = [f for f in _findings(report, "CLOSURE") if f.level == "note"]
        assert any(rel in f.message for f in noted), (
            "an admitted member must still be RECORDED, not silently passed")

    def test_a_wrong_digest_for_the_right_path_still_refuses(self, tmp_path):
        """The admission is over bytes, not over path membership. A reviewed set
        that names the file but not the bytes in front of us admits nothing."""
        repo, anchor, rel, _sha = self._changed(tmp_path)
        report = self._closure(repo, anchor, {rel: "9" * 64})
        assert report.blocked
        assert any(f.level == "review" for f in _findings(report, "CLOSURE"))

    def test_admitting_one_member_does_not_admit_another(self, tmp_path):
        """Per-path, not per-transition. A set that admits one changed member
        must leave every other member held to the anchor."""
        repo, anchor, rel, sha = self._changed(tmp_path)
        other = "bootstrap/tests/_oracle_trust.py"
        _write(repo, other, "# an unreviewed change\n")
        _commit(repo, "a second, unreviewed authority change")

        report = self._closure(repo, anchor, {rel: sha})

        assert report.blocked
        refused = [f.message for f in _findings(report, "CLOSURE")
                   if f.level == "review"]
        assert any(other in m for m in refused), refused
        assert not any(rel in m for m in refused), refused

    def test_a_prefixed_digest_is_not_accepted_as_a_bare_one(self, tmp_path):
        """The format bug that made this unreachable a second way.

        `revalidate_transition` compared `_sha256_bytes` -- which is
        `sha256:`-prefixed -- against the manifest's bare hex, so **no member
        ever matched** and the transition would have refused every closure it
        was handed. Two independent unreachability defects in one path is what
        happens when a mode is never executed end to end.
        """
        repo, anchor, rel, sha = self._changed(tmp_path)
        report = self._closure(repo, anchor, {rel: f"sha256:{sha}"})
        assert report.blocked, (
            "a prefixed digest must not match; the manifest format is bare hex")


class TestTheAuthorityModuleCheckAdmitsTheSameSet:
    """The second gate on the same bytes, and why it must agree with the first.

    `check_authority_closure` and `check_authority_modules` both refuse when a
    Stage-B module differs from the anchor. Admitting a reviewed transition in
    one and not the other leaves the mode **half**-reachable, which is worse
    than unreachable: the ceremony looks like it works right up to the check
    that still refuses, by which point stage 1 has run candidate code.

    That is not hypothetical -- it is what happened. The closure admission alone
    left the recorded transition ceremony refusing at AUTHORITY, and only
    executing the recorded blocks end to end surfaced it.
    """

    def _repo_whose_anchor_differs(self, tmp_path):
        """An anchor holding different bytes than the modules now executing."""
        repo, anchor = _closure_repo(tmp_path)   # writes `# <rel>\n` stubs
        return repo, anchor

    def _authority(self, repo, anchor, admitted):
        report = P.Report()
        P.check_authority_modules(anchor, report, repo=repo,
                                  admitted_authority=admitted)
        return report

    def _live_digests(self):
        import hashlib
        return {rel: hashlib.sha256(Path(p).read_bytes()).hexdigest()
                for rel, p in P.R._authority_code_files()}

    def test_a_changed_module_refuses_without_an_admitted_set(self, tmp_path):
        repo, anchor = self._repo_whose_anchor_differs(tmp_path)
        report = self._authority(repo, anchor, None)
        assert report.blocked
        assert all(f.level == "review" for f in _findings(report, "AUTHORITY"))

    def test_the_reviewed_set_admits_exactly_those_modules(self, tmp_path):
        repo, anchor = self._repo_whose_anchor_differs(tmp_path)
        report = self._authority(repo, anchor, self._live_digests())
        assert not report.blocked, [f.message for f in report.findings]
        assert _findings(report, "AUTHORITY"), (
            "an admitted module must still be recorded as a note")
        assert all(f.level == "note" for f in _findings(report, "AUTHORITY"))

    def test_a_wrong_digest_still_refuses(self, tmp_path):
        """Over bytes, not over path membership -- as in the closure check."""
        repo, anchor = self._repo_whose_anchor_differs(tmp_path)
        wrong = {rel: "9" * 64 for rel in self._live_digests()}
        assert self._authority(repo, anchor, wrong).blocked

    def test_admitting_one_module_leaves_the_others_refused(self, tmp_path):
        repo, anchor = self._repo_whose_anchor_differs(tmp_path)
        live = self._live_digests()
        one = sorted(live)[0]
        report = self._authority(repo, anchor, {one: live[one]})
        assert report.blocked
        refused = [f.message for f in _findings(report, "AUTHORITY")
                   if f.level == "review"]
        assert refused and not any(one in m for m in refused), refused

    def test_both_checks_take_the_admitted_set(self):
        """The property that keeps them from drifting apart again.

        Asserted on the signatures rather than on behaviour: a future check that
        reads the same files and forgets the parameter reintroduces exactly this
        defect, and the failure mode is a half-reachable mode rather than a
        visibly broken one.
        """
        import inspect
        for fn in (P.check_authority_closure, P.check_authority_modules):
            assert "admitted_authority" in inspect.signature(fn).parameters, (
                f"{fn.__name__} cannot honour a reviewed transition; it will "
                f"refuse every closure change the other check admits")


class TestTransitionRefusesWithoutADelta:
    """Chunk B / plan finding [S3]. "First use" was never mechanically one-time
    -- the delta condition recurs on every authority change -- so the mode is
    named the **reviewed-authority transition** and is gated on the delta
    itself, at the cost of a fresh external review each time."""

    def _closure_repo(self, tmp_path, change: bool):
        """An anchor and a candidate whose authority closures differ (or not).

        Deliberately NOT `_ceremony_repo()`: its pre-aligned closure is what hid
        [M2-2], so it is inadmissible for transition fixtures ([E4]/B4). This
        builds the old-anchor state explicitly.
        """
        repo, anchor_sha = _closure_repo(tmp_path)
        if change:
            _write(repo, "bootstrap/tests/_oracle.py", "# changed\n")
            head = _commit(repo, "authority change")
        else:
            _write(repo, "unrelated.txt", "x\n")
            head = _commit(repo, "no authority change")
        return repo, anchor_sha, head

    def test_a_closure_change_is_a_delta(self, tmp_path):
        repo, anchor, head = self._closure_repo(tmp_path, change=True)
        delta = P.authority_closure_delta(anchor, head, repo=repo)
        assert "bootstrap/tests/_oracle.py" in delta

    def test_no_closure_change_is_no_delta(self, tmp_path):
        repo, anchor, head = self._closure_repo(tmp_path, change=False)
        assert P.authority_closure_delta(anchor, head, repo=repo) == {}

    def test_the_transition_refuses_when_the_closure_is_unchanged(
            self, tmp_path):
        """The mode must not be available as a habitual flag."""
        repo, anchor, head = self._closure_repo(tmp_path, change=False)
        manifest = P.parse_review_manifest(
            _review_manifest(repo, head))
        with pytest.raises(P.ReviewManifestError) as exc:
            P.revalidate_transition(manifest, head, head,
                                    anchor=anchor, repo=repo)
        assert "no reviewed transition to perform" in str(exc.value)
        assert "not a flag" in str(exc.value)


class TestRosterContinuityIsAHardRefusal:
    """Chunk B3 / [E4]. Continuity means the OLD anchor's roster verifies a
    transition. An anchor without one is a distinct bootstrap case, and neither
    the candidate's roster nor the review manifest may stand in -- both are the
    thing being authorized."""

    def test_an_anchor_without_a_roster_refuses(self, tmp_path):
        repo = _repo(tmp_path)
        _write(repo, "x.txt", "x\n")
        anchor = _commit(repo, "anchor with no roster")
        with pytest.raises(P.PreflightError) as exc:
            with P.anchored_roster(anchor, repo=repo):
                pass
        msg = str(exc.value)
        assert "HARD REFUSAL" in msg and "not a fallback" in msg

    def test_the_refusal_names_a_route_that_exists(self, tmp_path):
        """`AGENTS.md`: a named trigger is checked by OPENING it. A refusal that
        points at a procedure which is not there is worse than a bare one."""
        repo = _repo(tmp_path)
        _write(repo, "x.txt", "x\n")
        anchor = _commit(repo, "anchor with no roster")
        with pytest.raises(P.PreflightError) as exc:
            with P.anchored_roster(anchor, repo=repo):
                pass
        runbook = (P._REPO / "bootstrap/REANCHOR_RUNBOOK.md").read_text(
            encoding="utf-8")
        assert "Phase 0 transition mode" in str(exc.value)
        assert "## Phase 0 transition mode" in runbook or \
               "### Phase 0 transition mode" in runbook, (
            "the refusal names a runbook section that does not exist")

    def test_a_worktree_roster_cannot_stand_in_for_a_missing_anchored_one(
            self, tmp_path):
        """The candidate's copy is not a substitute at any point -- including
        when the anchor's is missing, which is exactly when it is tempting.

        The roster is present and readable in the worktree throughout; the
        anchor commit predates it. A fallback would find the file and succeed.
        """
        repo = _repo(tmp_path)
        _write(repo, "x.txt", "x\n")
        anchor = _commit(repo, "anchor with no roster")

        _write(repo, "dev/.cairn/allowed_signers", "attacker AAAA\n")
        _commit(repo, "roster appears in the worktree, after the anchor")
        assert (repo / "dev/.cairn/allowed_signers").exists(), "precondition"

        with pytest.raises(P.PreflightError) as exc:
            with P.anchored_roster(anchor, repo=repo):
                pass
        assert "HARD REFUSAL" in str(exc.value)


class TestAuthorizationPackage:
    """Chunk C / plan review [E2]. A strict field schema alone does not stop a
    symlink target, a partial write, a replacement between hash and parse,
    duplicate JSON keys, or stage 2 confirming against a digest carried *inside*
    the artifact -- the adjacent self-digest CR1 falsified, one layer down."""

    def _pkg(self):
        return {
            "schema": P.PACKAGE_SCHEMA,
            "observed_anchor": "a" * 40, "candidate_head": "b" * 40,
            "candidate_tree": "c" * 40, "branch": "refs/heads/master",
            "expected_old": "b" * 40,
            "range_report": {"schema": P.RANGE_REPORT_SCHEMA},
            "range_report_digest": "d" * 64,
            "review_manifest": {"provenance": "review 2026-08-12",
                                "candidate": "b" * 40, "digest": "d" * 64,
                                "members": {"bootstrap/tests/_oracle.py":
                                            "a" * 64}},
            "prospective_manifest_b64": "e30=",
            "prospective_manifest_sha256": "e" * 64,
            "collection": {"node_count": 1},
            "interpreter": {"version": "3.13.13"},
            "signing_key_fingerprint": "SHA256:" + "A" * 43,
        }

    def test_round_trip(self, tmp_path):
        dest = tmp_path / "pkg.json"
        digest = P.write_package(dest, self._pkg())
        assert P.read_package(dest, confirmed_sha256=digest)["schema"] == \
            P.PACKAGE_SCHEMA

    def test_the_digest_is_over_the_bytes_written(self, tmp_path):
        dest = tmp_path / "pkg.json"
        digest = P.write_package(dest, self._pkg())
        import hashlib
        assert digest == hashlib.sha256(dest.read_bytes()).hexdigest()

    def test_a_self_digest_field_is_refused(self, tmp_path):
        """The [E2] shape stated directly: authority must never come from a
        value the artifact carries about itself."""
        dest = tmp_path / "pkg.json"
        pkg = self._pkg()
        pkg["package_digest"] = "f" * 64
        digest = P.write_package(dest, pkg)
        with pytest.raises(P.PackageError, match="self-digest"):
            P.read_package(dest, confirmed_sha256=digest)

    def test_a_wrong_confirmation_refuses(self, tmp_path):
        dest = tmp_path / "pkg.json"
        P.write_package(dest, self._pkg())
        with pytest.raises(P.PackageError, match="does not match the confirmed"):
            P.read_package(dest, confirmed_sha256="0" * 64)

    def test_replacement_between_write_and_read_refuses(self, tmp_path):
        """The substitution the external digest exists to catch."""
        dest = tmp_path / "pkg.json"
        digest = P.write_package(dest, self._pkg())
        tampered = self._pkg()
        tampered["candidate_head"] = "9" * 40
        dest.unlink()
        P.write_package(dest, tampered)
        with pytest.raises(P.PackageError, match="does not match the confirmed"):
            P.read_package(dest, confirmed_sha256=digest)

    def test_a_symlinked_package_refuses(self, tmp_path):
        real = tmp_path / "real.json"
        digest = P.write_package(real, self._pkg())
        link = tmp_path / "link.json"
        link.symlink_to(real)
        with pytest.raises(OSError):
            P.read_package(link, confirmed_sha256=digest)

    @pytest.mark.parametrize("field", sorted(
        {"schema", "observed_anchor", "candidate_head", "candidate_tree",
         "branch", "expected_old", "range_report", "range_report_digest",
         "review_manifest", "prospective_manifest_b64",
         "prospective_manifest_sha256", "collection", "interpreter"}))
    def test_every_package_field_is_mutation_tested_through_stage_2(
            self, tmp_path, monkeypatch, field):
        """Acceptance criterion 7, and deliberately the hard form.

        Each field is mutated **and the package re-digested**, so the
        Maintainer's `--confirm-package-sha256` matches the tampered bytes
        perfectly. That models the case the digest cannot help with: whoever
        rewrote the file also supplied the digest the operator confirmed. What
        must refuse is stage 2's own re-derivation of every field, one at a
        time -- so no field is decorative, and none is trusted merely because it
        arrived inside a confirmed artifact.

        Running it through the public stage-2 path rather than `read_package`
        is the [M2-1] discipline: a schema check that nothing consumes refuses
        nothing.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        manifest = {**P.rederive_static_manifest(head, repo=repo),
                    "collection": {"node_count": 1, "node_ids": ["a.py::t"],
                                   "skip_xfail_marked": []},
                    "interpreter": {"version": "3.13.13"}}
        monkeypatch.setattr(P, "gather_evidence",
                            lambda *a, **k: _fake_evidence(head, manifest))
        monkeypatch.setattr(P, "require_stage1_cannot_sign",
                            lambda *a, **k: _stub_key(tmp_path))

        pkg_path = tmp_path / "pkg.json"
        P.stage1(repo=repo, package_out=pkg_path, out=io.StringIO())
        honest = json.loads(pkg_path.read_bytes())
        before = (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                  _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip())

        tampered = dict(honest)
        value = honest[field]
        if isinstance(value, str):
            tampered[field] = ("9" * len(value)) if value else "x"
        elif isinstance(value, dict):
            tampered[field] = {**value, "injected": "x"}
        elif value is None:
            tampered[field] = {"provenance": "forged", "members": {},
                               "candidate": "9" * 40, "digest": "9" * 64}
        else:
            tampered[field] = "9" * 40
        assert tampered[field] != value, f"{field} was not actually mutated"

        pkg_path.unlink()
        import hashlib
        body = (json.dumps(tampered, indent=2, sort_keys=True) + "\n").encode()
        pkg_path.write_bytes(body)
        confirmed = hashlib.sha256(body).hexdigest()   # the operator's digest

        P._phase = P._PHASE_CANDIDATE
        with pytest.raises(P.PreflightError):
            P.apply_now(repo=repo, package=str(pkg_path),
                        confirmed_package_sha256=confirmed, out=io.StringIO(),
                        signing_key=str(tmp_path / "maint.pub"))
        assert (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                _run("git", "rev-parse", P._ANCHOR_REF,
                     cwd=repo).stdout.strip()) == before, (
            f"a package with a mutated {field!r} moved a ref")

    def test_a_substituted_prospective_manifest_moves_neither_ref(
            self, tmp_path, monkeypatch):
        """Criterion 7's named case: the bytes that become the trust root.

        `prospective_manifest_b64` is the one field whose contents are committed
        verbatim, so a substitution here is a substitution of the anchored
        artifact itself. Stage 2 rebuilds it independently and compares EXACT
        bytes; a field-by-field comparison would accept a re-serialization that
        differs from what stage 1 measured.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        manifest = {**P.rederive_static_manifest(head, repo=repo),
                    "collection": {"node_count": 1, "node_ids": ["a.py::t"],
                                   "skip_xfail_marked": []},
                    "interpreter": {"version": "3.13.13"}}
        monkeypatch.setattr(P, "gather_evidence",
                            lambda *a, **k: _fake_evidence(head, manifest))
        monkeypatch.setattr(P, "require_stage1_cannot_sign",
                            lambda *a, **k: _stub_key(tmp_path))
        pkg_path = tmp_path / "pkg.json"
        P.stage1(repo=repo, package_out=pkg_path, out=io.StringIO())
        honest = json.loads(pkg_path.read_bytes())
        before = (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                  _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip())

        # A manifest that is well-formed and internally consistent -- its own
        # digest field updated to match -- so only the independent rebuild can
        # catch it.
        import base64, hashlib
        swapped = json.loads(base64.b64decode(honest["prospective_manifest_b64"]))
        swapped["frozen_files"] = {}
        body_m = (json.dumps(swapped, indent=2, sort_keys=True)).encode() + b"\n"
        honest["prospective_manifest_b64"] = base64.b64encode(body_m).decode()
        honest["prospective_manifest_sha256"] = P._sha256_bytes(body_m)

        pkg_path.unlink()
        body = (json.dumps(honest, indent=2, sort_keys=True) + "\n").encode()
        pkg_path.write_bytes(body)

        P._phase = P._PHASE_CANDIDATE
        with pytest.raises(P.PreflightError):
            P.apply_now(repo=repo, package=str(pkg_path), out=io.StringIO(),
                        confirmed_package_sha256=hashlib.sha256(body).hexdigest(),
                        signing_key=str(tmp_path / "maint.pub"))
        assert (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                _run("git", "rev-parse", P._ANCHOR_REF,
                     cwd=repo).stdout.strip()) == before

    def _transition_ready(self, tmp_path, monkeypatch):
        """A package produced in TRANSITION mode, and the pieces to replay it.

        Code review [C1]: the parametrized mutation node above runs stage 1 in
        **steady state**, so `review_manifest` is `None` and only the
        `None -> dict` direction was ever exercised. Every field *inside* that
        dict -- the admitted set that the checkpoint writes down -- went
        unmutated, which is how a forged set reached a signed message.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        _write(repo, "bootstrap/tests/_oracle.py", "# a reviewed change\n")
        resolved = _signed_commit(repo, "reviewed authority change")
        manifest = tmp_path / "review.txt"
        manifest.write_text(_review_manifest(repo, resolved), encoding="utf-8")
        evidence_manifest = {
            **P.rederive_static_manifest(resolved, repo=repo),
            "collection": {"node_count": 1, "node_ids": ["a.py::t"],
                           "skip_xfail_marked": []},
            "interpreter": {"version": "3.13.13"}}
        monkeypatch.setattr(
            P, "gather_evidence",
            lambda *a, **k: _fake_evidence(resolved, evidence_manifest))
        monkeypatch.setattr(P, "require_stage1_cannot_sign",
                            lambda *a, **k: _stub_key(tmp_path))
        pkg_path = tmp_path / "pkg.json"
        P.stage1(repo=repo, package_out=pkg_path, out=io.StringIO(),
                 review_manifest=str(manifest), reviewed_candidate=resolved)
        return repo, resolved, manifest, pkg_path

    def _replay(self, repo, pkg_path, body, manifest, resolved):
        import hashlib
        pkg_path.unlink()
        pkg_path.write_bytes(body)
        P._phase = P._PHASE_CANDIDATE
        return P.apply_now(
            repo=repo, package=str(pkg_path), out=io.StringIO(),
            confirmed_package_sha256=hashlib.sha256(body).hexdigest(),
            signing_key=str(pkg_path.parent / "maint.pub"),
            review_manifest=str(manifest), reviewed_candidate=resolved)

    @pytest.mark.parametrize("tamper", [
        "falsify-digests", "drop-members", "members-not-a-dict",
        "newline-in-path", "forge-provenance",
    ])
    def test_the_admitted_set_inside_the_package_cannot_forge_the_record(
            self, tmp_path, monkeypatch, tamper):
        """[C1]. The package is re-digested, so the confirmation matches.

        This is the exact probe the code review ran. Before the fix, three of
        these signed a checkpoint: falsified digests wrote nine false rows with
        every check green, dropping `members` signed
        "steady state -- no closure change" over a real closure change, and a
        newline in a path forged an extra row. The fourth raised an uncaught
        AttributeError -- a traceback instead of a refusal, on the one path that
        moves the trust root.
        """
        repo, resolved, manifest, pkg_path = self._transition_ready(
            tmp_path, monkeypatch)
        before = (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                  _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip())
        pkg = json.loads(pkg_path.read_bytes())
        rm = pkg["review_manifest"]

        if tamper == "falsify-digests":
            rm["members"] = {k: "9" * 64 for k in rm["members"]}
        elif tamper == "drop-members":
            del rm["members"]
        elif tamper == "members-not-a-dict":
            rm["members"] = ["not", "a", "dict"]
        elif tamper == "newline-in-path":
            k = sorted(rm["members"])[0]
            rm["members"][f"{k}\n    {'0' * 64}  forged/path.py"] = \
                rm["members"].pop(k)
        elif tamper == "forge-provenance":
            rm["provenance"] = "an external review that never happened"

        body = (json.dumps(pkg, indent=2, sort_keys=True) + "\n").encode()
        with pytest.raises(P.PreflightError):
            self._replay(repo, pkg_path, body, manifest, resolved)
        assert (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                _run("git", "rev-parse", P._ANCHOR_REF,
                     cwd=repo).stdout.strip()) == before, (
            f"a package tampered with {tamper!r} moved a ref")

    def test_the_signed_record_is_the_revalidated_set_not_the_packages(
            self, tmp_path, monkeypatch):
        """The positive half of [C1]: which object actually reaches the message.

        Refusing a mismatch is good, but the load-bearing property is *whose*
        set gets written down. Asserted by reading the committed checkpoint of
        an honest run and comparing it with the out-of-band artifact, which is
        the only source stage 2 revalidated against.
        """
        repo, resolved, manifest, pkg_path = self._transition_ready(
            tmp_path, monkeypatch)
        body = pkg_path.read_bytes()
        self._replay(repo, pkg_path, body, manifest, resolved)

        message = _run("git", "log", "-1", "--format=%B", cwd=repo).stdout
        recovered = P.parse_admitted_authority(message)
        expected = P.parse_review_manifest(
            manifest.read_text(encoding="utf-8"))["members"]
        assert recovered == expected
        import hashlib
        assert hashlib.sha256(manifest.read_bytes()).hexdigest() in message

    def test_the_message_writer_refuses_a_set_it_cannot_read_back(self):
        """The writer-side guard, isolated from the package path.

        `draft_message` round-trips its own output before returning. A member
        path that forges a row makes the emitted record unrecoverable, and the
        only cheap moment to notice is before a signature exists -- afterwards
        the checkpoint is signed, verified, anchored, and unparseable.

        The refusal may come from either half of the round trip: the parser's
        own count check fires first on a forged row (two rows, one declared),
        and the equality comparison catches everything the parser accepts. What
        matters is that no message is returned.
        """
        with pytest.raises(P.PreflightError):
            P.draft_message(
                observed_anchor="0" * 40, checked_head="1" * 40,
                manifest_sha256="e" * 64, authority_hashes={}, scope={},
                admitted_authority={f"a.py\n    {'0' * 64}  forged.py": "b" * 64},
                review_provenance="ESR", review_digest="d" * 64)

    def test_the_retired_no_handoff_artifact_claim_cannot_return(self):
        """Security review [S2] / Chunk C10.

        `apply_now` claimed "no handoff artifact is trusted" and "there is no
        authority-bearing file" long after stage 2 began consuming the
        authorization package and taking its `collection` and `interpreter`
        fields. That is not stale history in a deliberation record -- it is
        security documentation shipped inside the deciding executable,
        describing a design that no longer exists and contradicting the protocol
        the operator is being asked to trust.

        Pinned over the module source AND the public `--help`, because the CLI
        help repeated it independently and a check scoped to one would pass
        while the other kept saying it.
        """
        src = (P._REPO / "bootstrap/tests/_gate_preflight.py").read_text(
            encoding="utf-8")
        retired = ("no handoff artifact is trusted",
                   "trusts no handoff artifact",
                   "there is no authority-bearing file")
        for phrase in retired:
            # Allowed only where the retraction itself is being explained.
            for i, line in enumerate(src.splitlines(), 1):
                if phrase in line:
                    window = "\n".join(src.splitlines()[max(0, i - 12):i + 12])
                    assert "[S2]" in window or "used to" in window, (
                        f"line {i} asserts {phrase!r} outside an explanation of "
                        f"its retraction")

        for cmd in ("check", "stage2"):
            r = subprocess.run(
                [sys.executable, "-E", "-s",
                 str(_REPO / "bootstrap/tests/_gate_preflight.py"), cmd, "-h"],
                capture_output=True, text=True, check=False)
            for phrase in retired:
                assert phrase not in r.stdout, (
                    f"`{cmd} --help` still tells the operator {phrase!r}")

    def test_no_boolean_confirmation_path_exists_anywhere_in_the_module(self):
        """Acceptance criterion 8, asserted on the module rather than the CLI.

        The CLI node proves argparse rejects the flag. This one proves there is
        nothing left for a future parser to re-expose: no parameter, no
        attribute, no constant. "Removed, not deprecated" is a claim about the
        module, and a check scoped to the command line would pass over a
        dormant keyword argument that one line of parser code would revive.
        """
        src = (P._REPO / "bootstrap/tests/_gate_preflight.py").read_text(
            encoding="utf-8")
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.arg):
                assert "confirm_supervised" not in node.arg, (
                    f"a boolean confirmation parameter survives: {node.arg}")
            if isinstance(node, ast.Name):
                assert "confirm_supervised" not in node.id, node.id
        # The flag string may appear only where the removal is explained.
        for i, line in enumerate(src.splitlines(), 1):
            if "confirm-supervised-reanchor" in line:
                assert "REMOVED" in src[max(0, src.index(line) - 400):
                                        src.index(line) + 400], (
                    f"line {i} mentions the removed flag outside an "
                    f"explanation of its removal")

    def test_writing_over_an_existing_path_refuses(self, tmp_path):
        dest = tmp_path / "pkg.json"
        dest.write_text("prior", encoding="utf-8")
        with pytest.raises(P.PackageError, match="already exists"):
            P.write_package(dest, self._pkg())

    def test_writing_through_a_symlink_refuses(self, tmp_path):
        target = tmp_path / "target.json"
        link = tmp_path / "link.json"
        link.symlink_to(target)
        with pytest.raises(P.PackageError, match="symlink"):
            P.write_package(link, self._pkg())

    def test_duplicate_json_keys_refuse(self, tmp_path):
        """A strict field set does not see duplicates -- the last value wins
        silently in an ordinary decoder, so two packages can hash differently
        and parse identically."""
        dest = tmp_path / "pkg.json"
        body = b'{"schema":"' + P.PACKAGE_SCHEMA.encode() + \
               b'","schema":"other"}\n'
        dest.write_bytes(body)
        import hashlib
        with pytest.raises(P.PackageError, match="duplicate key"):
            P.read_package(dest,
                           confirmed_sha256=hashlib.sha256(body).hexdigest())

    def test_an_oversize_package_refuses(self, tmp_path):
        dest = tmp_path / "pkg.json"
        dest.write_bytes(b"x" * (P.PACKAGE_MAX_BYTES + 1))
        import hashlib
        with pytest.raises(P.PackageError, match="over the"):
            P.read_package(dest, confirmed_sha256=hashlib.sha256(
                dest.read_bytes()).hexdigest())

    @pytest.mark.parametrize("field", [
        "observed_anchor", "candidate_head", "candidate_tree", "branch",
        "expected_old", "range_report", "range_report_digest",
        "review_manifest", "prospective_manifest_b64",
        "prospective_manifest_sha256", "collection", "interpreter",
    ])
    def test_every_missing_field_refuses(self, tmp_path, field):
        dest = tmp_path / "pkg.json"
        pkg = self._pkg()
        del pkg[field]
        digest = P.write_package(dest, pkg)
        with pytest.raises(P.PackageError, match="missing"):
            P.read_package(dest, confirmed_sha256=digest)

    def test_an_unknown_field_refuses(self, tmp_path):
        dest = tmp_path / "pkg.json"
        pkg = self._pkg()
        pkg["extra"] = 1
        digest = P.write_package(dest, pkg)
        with pytest.raises(P.PackageError, match="unexpected"):
            P.read_package(dest, confirmed_sha256=digest)

    def test_the_executable_only_list_is_closed(self):
        """C3/C6. These are exactly the fields static re-derivation cannot
        produce. A third member without a matching change to
        `rederive_static_manifest` means something derivable is being
        delegated to the candidate."""
        assert P.PACKAGE_EXECUTABLE_ONLY == ("collection", "interpreter")
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(P._REPO),
                              capture_output=True, text=True).stdout.strip()
        derived = set(P.rederive_static_manifest(head, repo=P._REPO))
        for name in P.PACKAGE_EXECUTABLE_ONLY:
            assert name not in derived, (
                f"{name} IS statically re-derivable; delegating it to the "
                f"candidate is unnecessary trust")


class TestReportBindsTheProspectiveManifest:
    """Chunk C5. The live defect security review [S2] found in `2df83d2`: the
    report bound the manifest already in the worktree while `apply` committed a
    different one, so `rederive_and_bind` reconfirmed the wrong identity."""

    def test_the_prospective_bytes_win_over_the_worktree_copy(self):
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(P._REPO),
                              capture_output=True, text=True).stdout.strip()
        anchor = subprocess.run(["git", "rev-parse", "HEAD~3"], cwd=str(P._REPO),
                                capture_output=True, text=True).stdout.strip()
        prospective = b'{"prospective": true}\n'
        import hashlib

        with_pros = P.range_review_report(
            anchor, head, branch="master", expected_old=head,
            prospective_manifest=prospective)
        without = P.range_review_report(
            anchor, head, branch="master", expected_old=head)

        assert with_pros["manifest_sha256"] == \
            hashlib.sha256(prospective).hexdigest()
        assert with_pros["manifest_sha256"] != without["manifest_sha256"], (
            "the prospective manifest must change the bound identity, or the "
            "parameter is decorative")


class TestKeyChannelProbe:
    """Chunk D / plan review [E1]. The probe must attempt a REAL signing
    operation and require failure. Observing `SSH_AUTH_SOCK` is the proxy
    failure the proposal warned against and then committed -- twice.

    Every key here is disposable and generated in `tmp_path`. **No ceremony key
    is ever touched.**
    """

    def _keypair(self, tmp_path, name="probe", passphrase=""):
        key = tmp_path / name
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", passphrase,
                        "-f", str(key), "-C", name], check=True,
                       capture_output=True)
        return key

    def test_a_successful_ssh_keygen_with_no_sig_file_counts_as_CAN_sign(
            self, tmp_path, monkeypatch):
        """Code review [C5]. The probe was fail-OPEN on its own success case.

        It required exit 0 **and** a `.sig` at one of two guessed paths. An
        `ssh-keygen` that signed but wrote its output elsewhere therefore
        reported *cannot sign* — the unsafe direction, from the one control
        whose entire purpose is to refuse. A signing command that returns
        success has signed; where the artifact landed is a detail.
        """
        import subprocess as _sp
        real = _sp.run

        def fake(cmd, *a, **k):
            if cmd and str(cmd[0]).endswith("ssh-keygen"):
                return _sp.CompletedProcess(cmd, 0, "", "")   # success, no .sig
            return real(cmd, *a, **k)

        monkeypatch.setattr(P.subprocess, "run", fake)
        P._phase = P._PHASE_CANDIDATE
        cannot, detail, _to = P.probe_cannot_sign(str(tmp_path / "k.pub"))
        assert cannot is False, (
            "ssh-keygen reported success and the probe called it a refusal")
        assert "success" in detail

    def test_a_locked_key_still_counts_as_cannot_sign(
            self, tmp_path, monkeypatch):
        """The other direction, so the [C5] fix did not invert into refusing
        every ceremony.

        Security review [S1] flagged the earlier version of this node: it used
        `"no such key"` as the failure text, which **codified the unsafe
        classification** — a key that is not there and a key whose private half
        is locked away produced the same verdict. Only the second is the N4
        precondition holding. The first is now refused upstream by
        `validate_signing_key` as *unprobeable*, and this node uses a real
        locked-key failure so it can no longer be read as blessing the other.
        """
        import subprocess as _sp
        real = _sp.run

        def fake(cmd, *a, **k):
            if cmd and str(cmd[0]).endswith("ssh-keygen"):
                return _sp.CompletedProcess(
                    cmd, 1, "", "Load key: incorrect passphrase supplied")
            return real(cmd, *a, **k)

        monkeypatch.setattr(P.subprocess, "run", fake)
        P._phase = P._PHASE_CANDIDATE
        cannot, detail, _to = P.probe_cannot_sign(str(tmp_path / "k.pub"))
        assert cannot is True and "passphrase" in detail

    @pytest.mark.parametrize("bad", ["missing", "relative", "symlink",
                                     "not-a-key", "directory"])
    def test_an_unprobeable_key_is_a_third_answer_and_refuses(
            self, tmp_path, bad):
        """Security review [S1]. "Unprobeable" is not "cannot sign".

        The reproduction: point stage 1 at a **nonexistent** public-key path.
        `ssh-keygen` fails with "no such file", the probe classified that as
        *cannot sign*, and the strongest-sounding control in the ceremony was
        satisfied by being aimed at nothing. Stage 2 — which then received no
        key identity at all — signed with whatever key repository config named.

        A probe that fails for the wrong reason has established nothing, so
        every input that cannot be probed is refused before probing.
        """
        real = tmp_path / "real.pub"
        target = {
            "missing": str(tmp_path / "nope.pub"),
            "relative": "relative/key.pub",
            "symlink": str(tmp_path / "link.pub"),
            "not-a-key": str(tmp_path / "junk.pub"),
            "directory": str(tmp_path),
        }[bad]
        if bad == "symlink":
            real.write_text("ssh-ed25519 AAAA test\n")
            Path(target).symlink_to(real)
        elif bad == "not-a-key":
            Path(target).write_text("this is not a public key\n")

        with pytest.raises(P.KeyChannelError) as exc:
            P.validate_signing_key(target)
        assert "UNPROBEABLE" in str(exc.value) or "absolute" in str(exc.value) \
            or "symlink" in str(exc.value), str(exc.value)

    def test_a_nonexistent_stage1_key_cannot_reach_construction(
            self, tmp_path, monkeypatch):
        """[S1] through the public path: the refusal precedes everything.

        The point is not merely that `validate_signing_key` raises — it is that
        the ceremony stops before candidate code runs, before a package exists,
        and therefore before anything stage 2 could act on.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        before = (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                  _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip())
        ran = []
        monkeypatch.setattr(P, "gather_evidence",
                            lambda *a, **k: ran.append("candidate") or {})

        with pytest.raises(P.KeyChannelError):
            P.stage1(repo=repo, package_out=tmp_path / "pkg.json",
                     signing_key=str(tmp_path / "absent.pub"),
                     out=io.StringIO())

        assert ran == [], "candidate code ran for an unprobeable key channel"
        assert not (tmp_path / "pkg.json").exists()
        assert (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                _run("git", "rev-parse", P._ANCHOR_REF,
                     cwd=repo).stdout.strip()) == before

    def test_stage_2_refuses_a_different_key_than_stage_1_probed(
            self, tmp_path, monkeypatch):
        """[S1]'s core: the two stages must be talking about one key.

        Stage 2 previously received no key identity, so a *different* key —
        rostered, and therefore passing the pinned-principal check — could sign
        the commit that becomes the trust root. The fingerprint bound into the
        package is what makes that a checked property rather than an assumption
        spanning two processes.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        manifest = {**P.rederive_static_manifest(head, repo=repo),
                    "collection": {"node_count": 1, "node_ids": ["a.py::t"],
                                   "skip_xfail_marked": []},
                    "interpreter": {"version": "3.13.13"}}
        monkeypatch.setattr(P, "gather_evidence",
                            lambda *a, **k: _fake_evidence(head, manifest))
        key_pub = str(tmp_path / "maint.pub")
        _p, fpr = P.validate_signing_key(key_pub)
        monkeypatch.setattr(P, "require_stage1_cannot_sign",
                            lambda *a, **k: {"key_path": key_pub,
                                             "fingerprint": fpr,
                                             "probe": "stubbed"})
        pkg_path = tmp_path / "pkg.json"
        P.stage1(repo=repo, package_out=pkg_path, out=io.StringIO())
        before = _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip()

        # A second, entirely valid key -- the shape that passed before.
        other = self._keypair(tmp_path, name="other")
        import hashlib
        body = pkg_path.read_bytes()
        P._phase = P._PHASE_CANDIDATE
        with pytest.raises(P.PackageError, match="same key"):
            P.apply_now(repo=repo, package=str(pkg_path), out=io.StringIO(),
                        confirmed_package_sha256=hashlib.sha256(body).hexdigest(),
                        signing_key=str(other.with_suffix(".pub")))
        assert _run("git", "rev-parse", P._ANCHOR_REF,
                    cwd=repo).stdout.strip() == before

    def test_a_repository_key_command_never_executes_after_the_seal(
            self, tmp_path):
        """[S1]'s second consequence: repository config could run a PROGRAM.

        `gpg.ssh.defaultKeyCommand` names a command Git executes to obtain a
        signing key when `user.signingKey` is unset. Under candidate control
        that is arbitrary execution inside stage 2, *after* the point the code
        declares candidate execution sealed. Codex reproduced it: the script ran
        and wrote a marker before construction failed on the key it returned.

        Both halves are now closed — the command is pinned empty in
        `_STERILE_CONFIG`, and the signer is named explicitly — so this asserts
        the marker is never written.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        marker = tmp_path / "KEYCMD_RAN"
        script = tmp_path / "keycmd.sh"
        script.write_text(f"#!/bin/sh\ntouch {shlex.quote(str(marker))}\n"
                          f"echo 'ssh-ed25519 AAAAinvalid'\n")
        script.chmod(0o755)
        _run("git", "config", "gpg.ssh.defaultKeyCommand", str(script), cwd=repo)
        _run("git", "config", "--unset", "user.signingkey", cwd=repo)

        P._phase = P._PHASE_CANDIDATE
        P.seal_candidate_execution(out=io.StringIO())
        with contextlib.suppress(P.PreflightError):
            P._construct_signed_commit(
                repo, head, b'{"m": 1}\n', "probe message\n",
                signing_key=str(tmp_path / "maint.pub"))

        assert not marker.exists(), (
            "repository configuration executed a program inside stage 2, after "
            "candidate execution was declared sealed")

    def test_a_readable_private_sibling_means_stage_1_CAN_sign(self, tmp_path):
        """[E1] reproduced as a regression. This is the state the old design
        called 'the key channel absent'."""
        key = self._keypair(tmp_path)
        assert key.exists(), "the private sibling is present and readable"

        cannot, detail, _to = P.probe_cannot_sign(
            str(key.with_suffix(".pub")),
            env={"HOME": "/nonexistent", "PATH": "/usr/bin:/bin"})

        assert cannot is False, (
            "the probe must report that signing SUCCEEDED here -- an unset "
            "agent socket does not make an adjacent private key unavailable")
        assert "signature was produced" in detail

    def test_without_the_private_key_stage_1_cannot_sign(self, tmp_path):
        """The precondition holding: the public key is present, the private
        half is not reachable."""
        key = self._keypair(tmp_path)
        pub = key.with_suffix(".pub")
        key.unlink()          # models 'encrypted at rest / not loaded'

        cannot, _d, _to = P.probe_cannot_sign(
            str(pub), env={"HOME": "/nonexistent", "PATH": "/usr/bin:/bin"})

        assert cannot is True

    def test_the_negative_control_refuses_rather_than_reporting_soundness(
            self, tmp_path, monkeypatch):
        """[E1]'s exact requirement: make the private sibling readable and
        require stage 1 to REFUSE THE ENVIRONMENT -- not to report the boundary
        sound."""
        key = self._keypair(tmp_path)
        monkeypatch.setattr(P, "signing_key_path",
                            lambda recorded=None: str(key.with_suffix(".pub")))

        with pytest.raises(P.KeyChannelError) as exc:
            P.require_stage1_cannot_sign("recorded", out=io.StringIO())

        msg = str(exc.value)
        assert "STAGE 1 CAN SIGN" in msg
        assert "the ceremony stops here" in msg
        assert "N4" in msg, "the refusal must name the precondition it enforces"

    def test_an_unnamed_key_channel_refuses(self, monkeypatch):
        """D2: the contract names the supported channel. An unnamed one cannot
        be probed, and an unprobeable precondition is not a precondition."""
        monkeypatch.setattr(P, "signing_key_path", lambda recorded=None: "")
        with pytest.raises(P.KeyChannelError, match="unnamed"):
            P.require_stage1_cannot_sign("recorded", out=io.StringIO())

    def test_the_probe_is_non_interactive_and_bounded(self):
        """A passphrase prompt is not a refusal -- left interactive, the
        ceremony waits for a human to supply the very thing being tested."""
        import inspect
        src = inspect.getsource(P.probe_cannot_sign)
        assert "stdin=subprocess.DEVNULL" in src
        assert "timeout=KEY_PROBE_TIMEOUT_S" in src
        assert "TimeoutExpired" in src, "a hang must be a definite negative"

    def test_a_timeout_is_not_treated_as_inability_to_sign(self, tmp_path,
                                                           monkeypatch):
        """The dangerous direction. A probe that times out has not proven the
        key unreachable; reporting `cannot_sign=True` there would turn a hang
        into a clean bill of health."""
        import subprocess as sp

        def hang(*a, **k):
            raise sp.TimeoutExpired(cmd="ssh-keygen", timeout=1)

        monkeypatch.setattr(P.subprocess, "run", hang)
        cannot, detail, _to = P.probe_cannot_sign("/nonexistent.pub")
        assert cannot is False, "a timeout must not read as 'cannot sign'"
        assert "timed out" in detail

    def test_the_probe_does_not_claim_containment(self):
        """The residual stays accurately described. This is sequencing."""
        import inspect
        src = inspect.getsource(P) if hasattr(P, "__file__") else ""
        text = (P._REPO / "bootstrap/tests/_gate_preflight.py").read_text(
            encoding="utf-8")
        marker = text.split("# the key channel (Chunk D")[1][:2000]
        assert "NOT CONTAINMENT" in marker.upper()


# --------------------------------------------------------------------------
# Chunk A ([R5] riders 1-2): stage 1 receives no agent socket
# --------------------------------------------------------------------------

#: The two heredoc delimiters that open a **stage-1** loader in the runbook, and
#: the two that open a **stage-2** one. The split is the control Chunk A
#: introduced: stage 1 must not be handed a signing channel, stage 2 must.
_STAGE1_DELIMS = ("LOADER", "TRANSITION")
_STAGE2_DELIMS = ("STAGE2", "STAGE2T")


def _stage1_blocks() -> dict[str, str]:
    """The two recorded stage-1 loader blocks, by heredoc delimiter."""
    return {"LOADER": _runbook_block("_gate_preflight.py"),
            "TRANSITION": _transition_block()}


def _stage2_blocks() -> dict[str, str]:
    """The two recorded stage-2 blocks, by heredoc delimiter."""
    return {"STAGE2": _stage2_block(), "STAGE2T": _stage2_transition_block()}


def _env_header(block: str, delim: str) -> str:
    """Everything up to and including the ``/bin/sh <<'DELIM'`` line.

    This is the part of a recorded block that decides **what environment the
    stage runs in**, which is the whole of what Chunk A changed. Lifting it out
    of the runbook rather than retyping it is the same FUR5 discipline every
    other recorded-block helper follows: an environment written correct in
    Python while the recorded one stayed wrong is the failure this repository
    keeps finding.
    """
    opener = f"/bin/sh <<'{delim}'"
    assert block.count(opener) == 1, (
        f"expected exactly one {opener!r} in the recorded block")
    head, _rest = block.split(opener, 1)
    return head + opener + "\n"


def _ssh_tooling() -> tuple[str, str, str]:
    """Absolute paths for the disposable-key machinery, or skip.

    Never the ceremony key and never the operator's agent: every node below
    generates its own ed25519 key in `tmp_path` and starts its own agent.
    """
    found = {n: shutil.which(n) for n in ("ssh-keygen", "ssh-agent", "ssh-add")}
    missing = [n for n, p in found.items() if not p]
    if missing:
        pytest.skip(f"no {' / '.join(missing)} on this host")
    return found["ssh-keygen"], found["ssh-agent"], found["ssh-add"]


@contextlib.contextmanager
def _scratch_agent(tmp_path: Path):
    """A private `ssh-agent` holding a disposable key whose private half is
    **deleted from disk**.

    Deleting the private file is what makes the node measure the right thing.
    With it present, `ssh-keygen -Y sign -f k.pub` signs from the file and the
    agent is irrelevant, so a "cannot sign" result would prove nothing about the
    socket. With it gone, the agent is the *only* route -- so signing succeeds
    exactly when the socket is reachable, which is the property Chunk A moved.

    Yields ``(socket_path, public_key_path)``.
    """
    keygen, agent, add = _ssh_tooling()
    key = tmp_path / "disposable"
    subprocess.run([keygen, "-q", "-t", "ed25519", "-N", "", "-f", str(key),
                    "-C", "cairn-stage1-boundary-probe"],
                   check=True, capture_output=True)
    r = subprocess.run([agent, "-s"], capture_output=True, text=True, check=True)
    sock = re.search(r"SSH_AUTH_SOCK=([^;]+);", r.stdout)
    pid = re.search(r"SSH_AGENT_PID=(\d+);", r.stdout)
    assert sock and pid, f"could not parse ssh-agent output: {r.stdout!r}"
    sock, pid = sock.group(1), pid.group(1)
    try:
        subprocess.run([add, str(key)], check=True, capture_output=True,
                       env={**os.environ, "SSH_AUTH_SOCK": sock},
                       stdin=subprocess.DEVNULL)
        key.unlink()                    # the agent is now the only route
        yield sock, key.with_suffix(".pub")
    finally:
        subprocess.run([agent, "-k"], capture_output=True,
                       env={**os.environ, "SSH_AUTH_SOCK": sock,
                            "SSH_AGENT_PID": pid})


def _signing_attempt_body(pub: Path, workdir: Path) -> str:
    """A heredoc body that tries to sign and reports which way it went.

    Deliberately **not** an `SSH_AUTH_SOCK` observation. Observing the variable
    is the proxy check plan review [E1] falsified: it is what the stage *was
    handed*, not what the stage *can do*. This body runs the real signing
    command, which is the only thing that answers the question.
    """
    keygen, _agent, _add = _ssh_tooling()
    payload = workdir / "payload"
    payload.write_bytes(b"cairn stage-1 boundary probe\n")
    return (
        f"SK={shlex.quote(keygen)}\n"
        f"PUB={shlex.quote(str(pub))}\n"
        f"PAYLOAD={shlex.quote(str(payload))}\n"
        'if [ -n "${SSH_AUTH_SOCK-}" ]; then\n'
        '    echo SOCKET_PRESENT\n'
        'else\n'
        '    echo SOCKET_ABSENT\n'
        'fi\n'
        'rm -f "$PAYLOAD.sig"\n'
        'if "$SK" -Y sign -f "$PUB" -n git "$PAYLOAD" >/dev/null 2>&1; then\n'
        '    echo SIGNED\n'
        'else\n'
        '    echo COULD_NOT_SIGN\n'
        'fi\n')


def _run_recorded_header(header: str, delim: str, body: str, *, sock: str,
                         repo: Path):
    """Run a recorded environment header with a substituted heredoc body.

    The **invoking** shell carries a live `SSH_AUTH_SOCK`, which is the case
    that matters: the question is not whether an absent variable stays absent,
    it is whether a header handed a real agent forwards it.
    """
    script = header + body + delim + "\n"
    return subprocess.run(
        ["bash", "-c", _substitute(script, repo, hashes=False)],
        capture_output=True, text=True, check=False, cwd=str(repo),
        env={**os.environ, "SSH_AUTH_SOCK": sock})


class TestStage1ReceivesNoAgentSocket:
    """Chunk A / [R5] riders 1-2, and acceptance criterion 5.

    Stage 1's contract is that it **cannot sign**: it runs candidate code to
    build an authorization package and exits. Forwarding an agent socket into it
    hands that candidate code a live signing channel in exchange for nothing, so
    Chunk A **removed the channel** instead of measuring it. Removing a channel
    beats measuring one -- the key probe cleared the probe's own environment,
    not the environment the candidate code beneath it ran in.

    Every key here is generated in `tmp_path` and every agent is started and
    killed by the test. **No ceremony key is ever touched, and the operator's
    own agent is never used.**
    """

    @pytest.mark.parametrize("delim", _STAGE1_DELIMS)
    def test_a_key_in_a_scratch_agent_cannot_sign_from_stage_1(
            self, delim, tmp_path):
        """The property, run rather than argued."""
        repo = tmp_path
        block = _stage1_blocks()[delim]
        with _scratch_agent(tmp_path) as (sock, pub):
            body = _signing_attempt_body(pub, tmp_path)
            r = _run_recorded_header(_env_header(block, delim), delim, body,
                                     sock=sock, repo=repo)
            assert r.returncode == 0, r.stderr[-2000:]
            assert "SOCKET_ABSENT" in r.stdout, (
                f"the recorded {delim} header forwarded an agent socket into "
                f"stage 1:\n{r.stdout}")
            assert "COULD_NOT_SIGN" in r.stdout, (
                f"stage 1 signed through the scratch agent; the {delim} "
                f"header's environment is not the boundary it claims:\n"
                f"{r.stdout}")

    @pytest.mark.parametrize("delim", _STAGE1_DELIMS)
    def test_restoring_the_forward_makes_the_same_stage_able_to_sign(
            self, delim, tmp_path):
        """The other side, so the node above cannot pass vacuously.

        If the signature failed for some reason unrelated to the socket -- a
        missing agent, an unusable key, a typo in the body -- the node above
        would pass while measuring nothing. Putting the forward back must make
        the *same* header, the *same* key and the *same* command **succeed**.
        This is the mutation check for acceptance criterion 5's two-sided form,
        expressed as a test rather than as a claim that one exists.
        """
        repo = tmp_path
        header = _env_header(_stage1_blocks()[delim], delim)
        restored = header.replace(
            f"    /bin/sh <<'{delim}'",
            f'    SSH_AUTH_SOCK="${{SSH_AUTH_SOCK-}}" \\\n'
            f"    /bin/sh <<'{delim}'")
        assert restored != header, "the forward was not re-inserted"
        with _scratch_agent(tmp_path) as (sock, pub):
            body = _signing_attempt_body(pub, tmp_path)
            r = _run_recorded_header(restored, delim, body, sock=sock,
                                     repo=repo)
            assert r.returncode == 0, r.stderr[-2000:]
            assert "SOCKET_PRESENT" in r.stdout, r.stdout
            assert "SIGNED" in r.stdout, (
                "with the forward restored the stage still could not sign, so "
                "the boundary node above is not measuring the forward:\n"
                f"{r.stdout}\n{r.stderr[-1500:]}")

    @pytest.mark.parametrize("delim", _STAGE2_DELIMS)
    def test_stage_2_still_receives_the_socket(self, delim, tmp_path):
        """The asymmetry is deliberate and must not be "tidied" symmetric.

        Stage 2 is the stage that signs. `git commit-tree` invokes the signer
        with no controlling terminal, so without a forwarded agent it falls back
        to `ssh-askpass` and dies naming a path that does not exist on a stock
        host. A later cleanup that removed *both* forwards would leave stage 1
        correct and the ceremony unrunnable.
        """
        repo = tmp_path
        header = _env_header(_stage2_blocks()[delim], delim)
        with _scratch_agent(tmp_path) as (sock, pub):
            body = _signing_attempt_body(pub, tmp_path)
            r = _run_recorded_header(header, delim, body, sock=sock, repo=repo)
            assert r.returncode == 0, r.stderr[-2000:]
            assert "SOCKET_PRESENT" in r.stdout, (
                f"the recorded {delim} header dropped the agent socket; stage "
                f"2 cannot sign without it:\n{r.stdout}")
            assert "SIGNED" in r.stdout, r.stdout


class TestTheRunbookSaysWhatItsLoadersDo:
    """Chunk A / [R5] rider 1's second half: **prose and loader cannot drift.**

    The behavioural nodes above execute the recorded headers, so they catch a
    loader that stops matching its contract. They do not catch the other
    direction -- a loader corrected while the paragraph above it still explains
    the old behaviour -- and that direction is the one an operator reads.
    """

    @staticmethod
    def _executable(header: str) -> str:
        """The header's shell lines, with its comments removed.

        The control is what the shell *runs*. The steady-state header also
        *explains* the removal in a comment, and a naive substring search over
        the whole header cannot tell the explanation from the thing it
        explains -- it would read "SSH_AUTH_SOCK IS NOT FORWARDED" as a
        forward.
        """
        return "\n".join(l for l in header.splitlines()
                          if not l.lstrip().startswith("#"))

    def test_no_stage_1_loader_forwards_the_agent_socket(self):
        for delim, block in _stage1_blocks().items():
            assert "SSH_AUTH_SOCK" not in \
                self._executable(_env_header(block, delim)), (
                    f"the recorded {delim} loader forwards SSH_AUTH_SOCK into "
                    f"stage 1, which is the channel Chunk A removed")

    def test_the_comment_stripper_does_not_hide_a_real_forward(self):
        """The node above would pass vacuously if `_executable` ate everything.

        Feeding it a header that *does* forward must still show the forward --
        otherwise "no match" would mean "nothing was searched".
        """
        delim = "LOADER"
        header = _env_header(_stage1_blocks()[delim], delim)
        forward = '    SSH_AUTH_SOCK="${SSH_AUTH_SOCK-}" \\\n'
        restored = header.replace(f"    /bin/sh <<'{delim}'",
                                  forward + f"    /bin/sh <<'{delim}'")
        assert "SSH_AUTH_SOCK" in self._executable(restored), (
            "the comment stripper removed a real forward, so the node above "
            "proves nothing")

    def test_both_stage_2_blocks_forward_the_agent_socket(self):
        for delim, block in _stage2_blocks().items():
            assert 'SSH_AUTH_SOCK="${SSH_AUTH_SOCK-}"' in \
                self._executable(_env_header(block, delim)), (
                    f"the recorded {delim} block no longer forwards the agent "
                    f"socket; stage 2 is the stage that signs")

    def test_the_prose_records_the_asymmetry_as_deliberate(self):
        """A reader who meets two blocks differing by one line must be told the
        difference is the control, or they will "fix" it."""
        text = (_REPO / "bootstrap/REANCHOR_RUNBOOK.md").read_text(
            encoding="utf-8")
        assert "IS NOT FORWARDED TO STAGE 1" in text, (
            "the runbook no longer states that stage 1 gets no agent socket")
        stage2 = text.split("### Phase 0 stage 2")[1]
        assert "opposite states" in stage2, (
            "the stage-2 section must name the asymmetry, or the two "
            "environment blocks read as a copying slip")

    def test_the_probe_docstring_does_not_call_itself_non_interactive(self):
        """[R5] rider 2. The docstring said "non-interactive"; `ssh-keygen`
        reads its passphrase from `/dev/tty`, so on a controlling terminal the
        probe **prompts**. An operator who trusted the old wording answered the
        prompt -- which is the probe succeeding, i.e. the refusal."""
        doc = P.probe_cannot_sign.__doc__ or ""
        assert "NOT non-interactive" in doc, (
            "the probe's own docstring must say it can prompt")
        assert "/dev/tty" in doc, (
            "the docstring must say WHY stdin=DEVNULL does not suppress it")
        assert "Decline" in doc or "decline" in doc, (
            "the docstring must tell the operator what to do at the prompt")

class TestReadBoundaryIsRepositoryReadOnly:
    """Security review [M2-4]. `_READ_ONLY_GIT` bounds *subcommands*; it said
    nothing about whether the repository is written. `git status` refreshes
    cached stat data through an optional index lock, so a public `check`
    changed `.git/index` bytes while leaving the worktree clean."""

    def test_a_read_invocation_does_not_mutate_the_index(self, tmp_path):
        repo = _repo(tmp_path)
        _write(repo, "a.txt", "x\n")
        _commit(repo, "base")
        index = repo / ".git" / "index"
        # Touch without changing bytes: exactly what provokes the stat refresh.
        (repo / "a.txt").touch()
        before = index.read_bytes()

        P._git("status", "--porcelain", repo=repo)

        assert index.read_bytes() == before, (
            "a documented read-only invocation rewrote .git/index")

    def test_the_pin_is_on_the_boundary_not_the_call_site(self):
        assert P._sterile_env().get("GIT_OPTIONAL_LOCKS") == "0", (
            "the pin must live in the shared child environment; a per-call "
            "flag is one forgotten call site away from the defect")


class TestManifestLauncherResistsSymlinkedStartPaths:
    """Security review [M2-5]. `GIT_CEILING_DIRECTORIES` is compared against the
    *logical* path, so a symlink to a nested non-repository directory escaped
    the ceiling and discovered the target repository -- the first fix for [IC6]
    set the ceiling from the unresolved parent and was evadable."""

    def test_a_symlinked_non_repository_does_not_discover_its_target(
            self, tmp_path):
        outer = tmp_path / "outer"
        outer.mkdir()
        _run("git", "init", "-q", ".", cwd=outer)
        nested = outer / "nested"
        nested.mkdir()
        link = tmp_path / "link"
        link.symlink_to(nested)

        assert G._object_format(link) is None, (
            "the symlinked start path escaped the ceiling and answered with "
            "the repository it points into")

    def test_a_real_repository_still_reports_its_format(self, tmp_path):
        repo = tmp_path / "real"
        repo.mkdir()
        _run("git", "init", "-q", ".", cwd=repo)
        assert G._object_format(repo) in G._OBJECT_FORMAT_WIDTH, (
            "resolving the start path must not break the honest case")


class TestRangeReportIsOnTheGoverningPath:
    """Security review [M2-1]. The range machinery existed, its isolated tests
    passed, and **nothing on the `apply` path called it** -- every real ceremony
    signed `range-report digest : (not bound)`.

    The review was explicit that helper-level mutation tests do not satisfy this
    finding, so these nodes replace the entry points with raisers and drive a
    **real** `apply`, which is the exact probe that found it.
    """

    def _prepared(self, tmp_path, monkeypatch):
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        manifest = {**P.rederive_static_manifest(head, repo=repo),
                    "collection": {"node_count": 1, "node_ids": ["a.py::t"],
                                   "skip_xfail_marked": []},
                    "interpreter": {"version": "3.13.13"}}
        monkeypatch.setattr(P, "gather_evidence",
                            lambda *a, **k: _fake_evidence(head, manifest))
        return repo, anchor, head

    def test_a_real_ceremony_signs_a_bound_digest(self, tmp_path, monkeypatch):
        repo, anchor, head = self._prepared(tmp_path, monkeypatch)

        result = _two_stage(repo, monkeypatch)

        body = _run("git", "log", "-1", "--format=%B", result["new_anchor"],
                    cwd=repo).stdout
        assert "(not bound)" not in body, (
            f"the signed checkpoint binds nothing:\n{body}")
        digest = re.search(r"range-report digest : ([0-9a-f]{64})", body)
        assert digest, f"no range-report digest in the signed message:\n{body}"
        tree = _run("git", "rev-parse", f"{head}^{{tree}}",
                    cwd=repo).stdout.strip()
        assert tree in body, "the candidate tree is not bound"

    @pytest.mark.parametrize("entry_point", [
        "range_review_report",
        "range_report_digest",
        "rederive_and_bind",
        "verify_message_binds_report",
    ])
    def test_removing_any_entry_point_fails_the_public_path(
            self, tmp_path, monkeypatch, entry_point):
        """The reviewer's own falsification, kept as a regression.

        Each of these was replaced with a raiser and a real `apply` still
        signed and advanced both refs. If that is ever true again, the report is
        decorative and the signature authorizes something narrower than the
        plan claims.
        """
        repo, anchor, head = self._prepared(tmp_path, monkeypatch)
        before = _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip()

        def raiser(*a, **k):
            raise AssertionError(f"{entry_point} must be on the apply path")

        monkeypatch.setattr(P, entry_point, raiser)

        with pytest.raises((AssertionError, P.PreflightError)):
            _two_stage(repo, monkeypatch)

        assert _run("git", "rev-parse", P._ANCHOR_REF,
                    cwd=repo).stdout.strip() == before, (
            "the anchor moved despite a missing binding entry point")

    def test_report_drift_between_confirmation_and_construction_refuses(
            self, tmp_path, monkeypatch):
        """`rederive_and_bind` is the control; this proves it is reachable and
        load-bearing rather than merely present."""
        repo, anchor, head = self._prepared(tmp_path, monkeypatch)
        real = P.rederive_and_bind

        def drifted(*a, **k):
            k["confirmed_digest"] = "0" * 64
            return real(*a, **k)

        monkeypatch.setattr(P, "rederive_and_bind", drifted)
        with pytest.raises(P.RangeReportDrift):
            _two_stage(repo, monkeypatch)

    def test_the_full_report_is_presented_not_just_its_digest(
            self, tmp_path, monkeypatch):
        """The Maintainer authorizes a *state*. A digest alone is not one."""
        repo, anchor, head = self._prepared(tmp_path, monkeypatch)
        buf = io.StringIO()

        _two_stage(repo, monkeypatch, out=buf)

        printed = buf.getvalue()
        assert "range-review report" in printed
        assert P.RANGE_REPORT_SCHEMA in printed, (
            "the complete report must be shown, not summarised")


class TestApplyCommitsTheAuthoritativeManifest:
    """Code review [IC2]. The shape of the manifest `apply` writes had no test,
    which is how "never accepted from the candidate" stayed true of the
    comparison and false of the artifact for a whole chunk."""

    def test_checker_derived_fields_come_from_the_checker(self):
        theirs = {"collection": ["a"], "object_format": "sha256",
                  "frozen_files": {"x.py": {"sha256": "c" * 64,
                                            "mode": "100755", "oid": "0" * 40}}}
        ours = {"object_format": "sha1",
                "frozen_files": {"x.py": {"sha256": "c" * 64,
                                          "mode": "100644", "oid": "a" * 40}}}

        merged = P.authoritative_manifest(theirs, ours)

        assert merged["object_format"] == "sha1", "the candidate's value won"
        entry = merged["frozen_files"]["x.py"]
        assert entry["mode"] == "100644" and entry["oid"] == "a" * 40
        assert merged["collection"] == ["a"], (
            "the collection is the one thing only the candidate can supply; "
            "replacing it would defeat the purpose of the evidence stage")

    def test_a_checker_derived_field_absent_from_ours_is_stripped(self):
        """The raw-tree path: `produce` runs with no repository, so the checker
        has no object format to offer. A candidate value must not survive by
        default -- absence has to win, or the fallback is the candidate's."""
        merged = P.authoritative_manifest(
            {"object_format": "sha256", "collection": []}, {"collection": []})
        assert "object_format" not in merged

    def test_a_candidate_asserted_subkey_cannot_survive(self):
        """The [IC2] probe, as a test: a hostile manifest inventing `mode` and
        `oid` for a frozen entry must not reach the committed bytes."""
        theirs = {"frozen_files": {"x.py": {"sha256": "c" * 64,
                                            "mode": "100755", "oid": "0" * 64}}}
        ours = {"frozen_files": {"x.py": {"sha256": "c" * 64}}}
        merged = P.authoritative_manifest(theirs, ours)
        entry = merged["frozen_files"]["x.py"]
        assert "mode" not in entry and "oid" not in entry

    def test_a_v1_scalar_entry_keeps_its_content_digest(self):
        """The shape the real evidence stage actually emits.

        Every other node in this class feeds a v2 dict, and that is precisely
        how this got through: `gather_evidence` runs `produce` from a raw tree
        with no repository, so it emits `rel -> "<sha256>"`, and the merge built
        each entry from `{}` and overlaid only mode and oid. The committed
        manifest carried no content digest for any frozen file -- the field the
        gate actually compares -- while every test here passed.

        A fixture that only exercises the shape the code finds convenient is not
        coverage; it is a mirror.
        """
        theirs = {"frozen_files": {"x.py": "c" * 64}}      # v1: the live shape
        ours = {"frozen_files": {"x.py": {"sha256": "c" * 64,
                                          "mode": "100644", "oid": "a" * 40}}}

        entry = P.authoritative_manifest(theirs, ours)["frozen_files"]["x.py"]

        assert entry["sha256"] == "c" * 64, (
            "the candidate's content digest was dropped; the anchored manifest "
            "would pin nothing the gate can compare")
        assert entry["mode"] == "100644" and entry["oid"] == "a" * 40

    def test_the_merge_agrees_whether_the_candidate_is_v1_or_v2(self):
        """C7's byte comparison depends on this and would silently fail without.

        Stage 1 merges the candidate's v1-shaped manifest; stage 2 merges its
        own v2-shaped re-derivation. The two must produce identical bytes or
        every real ceremony refuses itself at the exact-byte check.
        """
        ours = {"frozen_files": {"x.py": {"sha256": "c" * 64,
                                          "mode": "100644", "oid": "a" * 40}}}
        from_v1 = P.authoritative_manifest({"frozen_files": {"x.py": "c" * 64}},
                                           ours)
        from_v2 = P.authoritative_manifest(json.loads(json.dumps(ours)), ours)
        assert json.dumps(from_v1, sort_keys=True) == \
            json.dumps(from_v2, sort_keys=True)


class TestStaticManifestIsRederived:

    def test_a_file_missing_from_the_manifest_refuses(self, tmp_path):
        """FUR3's exact shape: the blessed tree would contain a frozen-surface
        file that the manifest does not pin."""
        repo, anchor, head, _epoch = _ceremony_repo(tmp_path)
        honest = P.rederive_static_manifest(head, repo=repo)
        assert honest["frozen_files"], "the fixture must have a frozen surface"

        tampered = json.loads(json.dumps(honest))
        dropped = sorted(tampered["frozen_files"])[0]
        del tampered["frozen_files"][dropped]

        report = P.Report()
        P.check_static_manifest(_fake_evidence(head, tampered), head, report,
                                repo=repo)
        findings = _findings(report, "MANIFEST")
        assert any(f.level == "refuse" and "frozen_files" in f.message
                   for f in findings)
        assert any(dropped in f.message for f in findings)

    def test_an_altered_hash_refuses(self, tmp_path):
        repo, anchor, head, _epoch = _ceremony_repo(tmp_path)
        tampered = json.loads(json.dumps(
            P.rederive_static_manifest(head, repo=repo)))
        victim = sorted(tampered["frozen_files"])[0]
        tampered["frozen_files"][victim] = "0" * 64

        report = P.Report()
        P.check_static_manifest(_fake_evidence(head, tampered), head, report,
                                repo=repo)
        assert any("altered" in f.message
                   for f in _findings(report, "MANIFEST"))

    def test_the_honest_manifest_is_silent(self, tmp_path):
        """Non-vacuity for the two refusals above."""
        repo, anchor, head, _epoch = _ceremony_repo(tmp_path)
        honest = P.rederive_static_manifest(head, repo=repo)
        report = P.Report()
        P.check_static_manifest(_fake_evidence(head, honest), head, report,
                                repo=repo)
        assert _findings(report, "MANIFEST") == []

    def test_only_collection_and_interpreter_stay_delegated(self, tmp_path):
        """The boundary, asserted rather than described: everything the real
        producer emits is either re-derived here or explicitly named as needing
        the suite to run."""
        repo, anchor, head, _epoch = _ceremony_repo(tmp_path)
        checker = _extract_anchored(repo, tmp_path / "extract")
        ev = tmp_path / "ev.json"
        r = subprocess.run(
            [sys.executable, "-E", "-s", str(checker), "evidence",
             "--repo", str(repo), "-o", str(ev)],
            capture_output=True, text=True, check=False)
        assert r.returncode == 0, r.stderr[-1500:]

        produced = set(json.loads(ev.read_text())["manifest"])
        rederived = set(P.rederive_static_manifest(head, repo=repo))
        # Three-way split, which is what the boundary now is:
        #   candidate-only  -> needs the suite to run (collection, interpreter)
        #   checker-only    -> Git-native identity, derived on the trusted side
        #   both            -> compared field by field
        assert rederived - produced == P._CHECKER_DERIVED_FIELDS, (
            f"a checker-derived field leaked into the candidate's manifest, or "
            f"one stopped being derived: {sorted(rederived - produced)}")
        assert produced - rederived == P._EXECUTABLE_ONLY_FIELDS, (
            f"a manifest field is neither re-derived nor declared "
            f"executable-only: {sorted(produced - rederived - P._EXECUTABLE_ONLY_FIELDS)}")

    def test_the_rederivation_matches_the_real_producer(self, tmp_path):
        """If the two disagreed on an honest tree, every ceremony would refuse
        -- so this pins that the reuse of `_gate_manifest`'s own globbing is
        actually equivalent, not merely similar."""
        repo, anchor, head, _epoch = _ceremony_repo(tmp_path)
        checker = _extract_anchored(repo, tmp_path / "extract")
        ev = tmp_path / "ev.json"
        subprocess.run(
            [sys.executable, "-E", "-s", str(checker), "evidence",
             "--repo", str(repo), "-o", str(ev)],
            capture_output=True, text=True, check=False)
        produced = json.loads(ev.read_text())["manifest"]
        rederived = P.rederive_static_manifest(head, repo=repo)
        for field, expected in rederived.items():
            if field in P._CHECKER_DERIVED_FIELDS:
                # Derived HERE and never accepted from the candidate: the
                # evidence stage runs `produce` from a raw tree with no
                # repository, so it has no object format or oids to offer --
                # and must not be trusted with any it did offer.
                assert field not in produced, (
                    f"{field} is checker-derived; the candidate must not "
                    f"supply it")
                continue
            if field == "frozen_files":
                # The candidate supplies content digests. Mode and oid are
                # checker-derived within each entry, for the same reason.
                expected = {r: (e["sha256"] if isinstance(e, dict) else e)
                            for r, e in expected.items()}
                got = {r: (e["sha256"] if isinstance(e, dict) else e)
                       for r, e in produced[field].items()}
                assert got == expected, "frozen_files digests diverged"
                continue
            if field in ("cascade_mutable", "phase_mutable"):
                # Same rule one level down, and it must be applied here too --
                # asserting a boundary while comparing across it is how this
                # test passed for the wrong reason once already.
                assert (P._candidate_comparable(produced[field])
                        == P._candidate_comparable(expected)), f"{field} diverged"
                continue
            assert produced[field] == expected, f"{field} diverged"


class TestStaticManifestIsWiredIntoCheck:
    """Mutation testing caught this gap: every FUR3 test above called
    `check_static_manifest` directly, so deleting its call site in `check()`
    broke nothing. A guard the real path does not invoke is not a guard -- which
    is precisely what FUR5 was."""

    def test_check_refuses_a_manifest_that_does_not_match_the_tree(self,
                                                                   tmp_path):
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        tampered = json.loads(json.dumps(
            P.rederive_static_manifest(head, repo=repo)))
        dropped = sorted(tampered["frozen_files"])[0]
        del tampered["frozen_files"][dropped]
        tampered["collection"] = {"node_count": 1, "node_ids": ["a::t"],
                                  "skip_xfail_marked": []}
        tampered["interpreter"] = {"version": "3.13.13"}

        # Internally consistent: `_fake_evidence` re-hashes, so the digest check
        # passes and the refusal must come from the re-derivation (CR1's lesson
        # -- a tampered artifact that re-hashes itself is not caught by a digest).
        report = P.check(repo=repo, evidence=_fake_evidence(head, tampered))

        assert report.blocked
        assert any(f.code == "MANIFEST" and f.level == "refuse"
                   for f in report.findings), [f.code for f in report.findings]

    def test_check_accepts_the_matching_manifest(self, tmp_path):
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        honest = P.rederive_static_manifest(head, repo=repo)
        honest["collection"] = {"node_count": 1, "node_ids": ["a::t"],
                                "skip_xfail_marked": []}
        honest["interpreter"] = {"version": "3.13.13"}
        report = P.check(repo=repo, evidence=_fake_evidence(head, honest))
        assert [f for f in report.findings if f.code == "MANIFEST"] == []

    def test_an_export_ignored_file_is_still_pinned_end_to_end(self, tmp_path):
        """FUR3's own probe, driven through the real flow.

        The property is **not** that this refuses -- a genuinely new frozen-surface
        file should be pinned, not rejected. It is that the blessed manifest
        covers what the blessed tree contains. Under `git archive` the producer
        never saw this file, so the commit was blessed with the file present and
        unpinned; that is the gap, and pinning it is the fix.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        sneaked = "bootstrap/tests/omitted.py"
        _write(repo, sneaked, "SNEAKED = True\n")
        _write(repo, ".gitattributes", f"{sneaked} export-ignore\n")
        _signed_commit(repo, "a file archive cannot see")
        checker = _extract_anchored(repo, tmp_path / "extract")

        # The hiding mechanism is still live -- otherwise this proves nothing.
        archived = subprocess.run(
            f"git -C {shlex.quote(str(repo))} archive --format=tar HEAD | tar -t",
            shell=True, capture_output=True, text=True)
        assert sneaked not in archived.stdout

        new = _subprocess_ceremony(checker, repo, tmp_path)["new_anchor"]
        blessed = json.loads(_run("git", "show", f"{new}:{P._MANIFEST_REL}",
                                  cwd=repo).stdout)
        assert sneaked in blessed["frozen_files"], (
            "the blessed tree contains a frozen-surface file its own manifest "
            "does not pin -- FUR3, unfixed")


# --------------------------------------------------------------------------
# FUR6 -- the loader is its own trust boundary
#
# The checker's sterile launcher cannot protect bytes that have not loaded yet.
# The recorded block obtained the checkout by ambient discovery and extracted
# with `git archive`, so repository-local object substitution made the literal
# runbook block execute substituted checker bytes while returning success --
# FUR1's failure one step earlier, outside everything FUR1 fixed.
# --------------------------------------------------------------------------

class TestLoaderTrustBoundary:

    _MARKER = "CAIRN_SUBSTITUTED_CHECKER_EXECUTED"

    def _substitute_the_checker(self, repo: Path, anchor: str) -> str:
        """Point `refs/replace/<anchor>` at a commit carrying a tampered checker.

        The tamper is loud on purpose: if the substituted bytes ever run, they
        leave a file behind, so the test cannot pass by accident.
        """
        rel = "bootstrap/tests/_gate_preflight.py"
        original = (repo / rel).read_text(encoding="utf-8")
        (repo / rel).write_text(
            f"import pathlib\n"
            f"pathlib.Path({str(repo / 'PWNED')!r}).write_text('{self._MARKER}')\n"
            + original, encoding="utf-8")
        evil = _signed_commit(repo, "substituted checker")
        _run("git", "update-ref", f"refs/replace/{anchor}", evil, cwd=repo)
        (repo / rel).write_text(original, encoding="utf-8")
        _signed_commit(repo, "restore the worktree copy")
        return evil

    def test_object_substitution_cannot_reach_the_executed_checker(self,
                                                                   tmp_path):
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        script = _runbook_ceremony_script(repo)      # hashes over the REAL anchor
        self._substitute_the_checker(repo, anchor)

        # The substitution is live: an ambient read returns the tampered bytes.
        ambient = _run("git", "show",
                       f"{anchor}:bootstrap/tests/_gate_preflight.py", cwd=repo)
        assert self._MARKER in ambient.stdout, (
            "the probe must actually substitute, or this proves nothing")

        r, before = _recorded_stage1(repo, tmp_path, script)

        assert not (repo / "PWNED").exists(), (
            "the loader executed substituted checker bytes")
        _assert_stage1_completed(repo, r, before)

    def test_a_tampered_recorded_hash_refuses_before_python_runs(self,
                                                                 tmp_path):
        """The decisive control, isolated: whatever route the bytes took, they
        must equal the reviewed set -- and the check must precede execution."""
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        script = _runbook_ceremony_script(repo)
        real = _recorded_hashes(repo)
        first = real.splitlines()[0]
        script = script.replace(first, "0" * 64 + first[64:])
        before = _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip()

        r = subprocess.run(["bash", "-c", script], cwd=str(repo),
                           capture_output=True, text=True, check=False)

        assert r.returncode != 0
        assert "do not match the reviewed first-use set" in r.stderr
        assert _run("git", "rev-parse", P._ANCHOR_REF,
                    cwd=repo).stdout.strip() == before

    def test_the_loader_covers_the_whole_authority_closure(self):
        """The recorded set is the AUTHORITY closure, not the import closure.

        A module missing from the recorded set would be absent at import time --
        fail-closed, but only if the set is complete. Security review [M2-R1]
        found the set narrower than that: it held the seven importable modules
        while the authority closure also contains `REANCHOR_RUNBOOK.md` (the
        instruction source, and FUR7's subject) and `dev/.cairn/allowed_signers`
        (the roster the checkpoint's signature is verified against). Neither is
        imported, and neither being imported is exactly why their absence would
        not have announced itself.
        """
        declared = set(P.declared_authority_closure())
        assert set(_LOADED_MODULES) == declared, (
            f"the loader's recorded set and the authority closure disagree: "
            f"{declared ^ set(_LOADED_MODULES)}")
        # The original property, kept: every importable member is still there.
        assert {r for r in declared if r.endswith(".py")} <= set(_LOADED_MODULES)

    def test_git_dir_in_the_environment_cannot_redirect_the_loader(self,
                                                                   tmp_path):
        """Mutation testing caught this gap: deleting the loader's `env -i`
        broke nothing, so the scrub was asserted nowhere.

        `GIT_DIR` is the channel that makes it matter. It names the object store
        outright and takes precedence over `-C`, so the loader would read the
        checker from a repository the operator never named -- the FUR6 failure
        by a different route.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        script = _runbook_ceremony_script(repo)

        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        _run("git", "init", "-q", ".", cwd=elsewhere)   # has no gate-anchor ref

        import os as _os
        r, before = _recorded_stage1(
            repo, tmp_path, script,
            env={**_os.environ, "GIT_DIR": str(elsewhere / ".git")})

        assert r.returncode == 0, (
            f"GIT_DIR redirected the loader away from the named checkout: "
            f"{r.stderr[-1500:]}")
        # The package is what proves the loader reached the NAMED checkout: it
        # can only be produced from a repository that has the gate-anchor ref,
        # and `elsewhere` has none. The old form asserted the anchor had moved,
        # which the recorded block no longer does -- and would now pass only if
        # a keyless stage had signed.
        _assert_stage1_completed(repo, r, before)

    def test_the_acquisition_command_resists_git_dir_redirection(self, tmp_path):
        """FUR7. The command that obtains the runbook is the instruction source:
        a substituted one can omit the loader entirely, so no later check can
        recover. It claimed to be sterile and had no environment scrub."""
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        marker = "THE-REAL-ANCHORED-RUNBOOK"
        _write(repo, P._RUNBOOK_REL, f"{marker}\n")
        real_anchor = _signed_commit(repo, "anchored runbook")
        _run("git", "update-ref", P._ANCHOR_REF, real_anchor, cwd=repo)

        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        _run("git", "init", "-q", ".", cwd=elsewhere)
        _run("git", "config", "user.email", "e@example", cwd=elsewhere)
        _run("git", "config", "user.name", "E", cwd=elsewhere)
        _write(elsewhere, P._RUNBOOK_REL, "AN ALTERNATE RUNBOOK WITH NO LOADER\n")
        _commit(elsewhere, "impostor")
        _run("git", "update-ref", P._ANCHOR_REF, "HEAD", cwd=elsewhere)

        command = _runbook_acquisition_command(repo)
        import os as _os
        r = subprocess.run(
            ["bash", "-c", command], cwd=str(repo), capture_output=True,
            text=True, check=False,
            env={**_os.environ, "GIT_DIR": str(elsewhere / ".git")})

        assert r.returncode == 0, r.stderr[-1500:]
        assert marker in r.stdout, (
            f"GIT_DIR redirected the acquisition command to another "
            f"repository's runbook: {r.stdout[:300]!r}")
        assert "ALTERNATE" not in r.stdout

    def test_a_replacement_shasum_on_path_cannot_vouch_for_rewritten_bytes(
            self, tmp_path):
        """FUR8. `PATH=/usr/bin:/bin` lived only inside the `env -i` child used
        for git; every other utility -- decisively `shasum` -- came from the
        operator's ambient environment. A replacement rewrote the extracted
        checker after extraction, reported success, and the rewritten checker
        ran, with the ceremony returning 0."""
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        script = _runbook_ceremony_script(repo)

        evil_bin = tmp_path / "evilbin"
        evil_bin.mkdir()
        fake = evil_bin / "shasum"
        fake.write_text(
            "#!/bin/sh\n"
            "for f in \"$@\"; do :; done\n"
            # rewrite the extracted checker, then vouch for it
            f"printf 'import pathlib\\n"
            f"pathlib.Path({str(repo / 'PWNED')!r}).write_text(\"x\")\\n' "
            f"> bootstrap/tests/_gate_preflight.py 2>/dev/null\n"
            "echo 'bootstrap/tests/_gate_preflight.py: OK'\n"
            "exit 0\n", encoding="utf-8")
        fake.chmod(0o755)

        import os as _os
        env = {**_os.environ, "PATH": f"{evil_bin}:{_os.environ['PATH']}"}

        # The replacement is live: a bare `shasum` in this environment is it.
        which = subprocess.run(["bash", "-c", "command -v shasum"], env=env,
                               capture_output=True, text=True)
        assert which.stdout.strip() == str(fake), which.stdout

        r, before = _recorded_stage1(repo, tmp_path, script, env=env)

        assert not (repo / "PWNED").exists(), (
            "a replacement shasum rewrote the checker and vouched for it")
        _assert_stage1_completed(repo, r, before)

    def test_the_loader_invokes_every_utility_by_absolute_path(self):
        """The property behind both tests above, asserted on the recorded text:
        a bare utility name is resolved through the operator's environment."""
        block = _runbook_block("_gate_preflight.py")
        code = "\n".join(ln for ln in block.splitlines()
                         if ln.strip() and not ln.lstrip().startswith("#"))
        for bare in ("mktemp -d", "mkdir -p", "shasum -a", "env -i"):
            assert bare not in code, (
                f"{bare!r} is invoked by bare name; an inherited function, "
                f"alias, or PATH entry can shadow it")
        for recorded in ('"$MKTEMP"', '"$MKDIR"', '"$SHASUM"', '"$ENV"',
                         '"$GIT"', '"$PY"'):
            assert recorded in code, f"{recorded} is not used"

    def test_an_inherited_shell_function_cannot_alter_the_checklist(self,
                                                                    tmp_path):
        """FUR9. Pinning the utilities left the loader *body* interpreted by the
        operator's shell. An inherited `echo` function rewrote the extracted
        checker and emitted the rewritten file's digest into RECORDED.sha256, so
        the pinned absolute `shasum` verified the wrong list and reported
        success. The rewritten checker then ran and the ceremony returned 0.

        Pinning `echo` would not have closed it -- `read`, `cd`, `[` and the
        redirections are the same class -- so the whole body is handed to a
        clean child shell instead.
        """
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        script = _runbook_ceremony_script(repo)
        pwned = repo / "PWNED"

        # An inherited definition in the shell that interprets the block. It
        # rewrites the checker, then emits the REWRITTEN file's digest so the
        # checklist agrees with the tampered bytes.
        hostile = (
            'echo() {\n'
            '  case "$1" in\n'
            '    *"  bootstrap/tests/_gate_preflight.py")\n'
            f'      printf %s\\\\n "import pathlib" '
            f'"pathlib.Path({str(pwned)!r}).write_text(\'x\')" '
            '        > "$T/bootstrap/tests/_gate_preflight.py"\n'
            '      set -- "$(/usr/bin/shasum -a 256 '
            '"$T/bootstrap/tests/_gate_preflight.py" '
            '| cut -d" " -f1)  bootstrap/tests/_gate_preflight.py"\n'
            '      ;;\n'
            '  esac\n'
            '  command echo "$@"\n'
            '}\n')

        r, before = _recorded_stage1(repo, tmp_path, script, prefix=hostile)

        assert not pwned.exists(), (
            "an inherited shell function rewrote the checker and forged its "
            "checklist entry past the pinned verifier")
        _assert_stage1_completed(repo, r, before)

    def test_the_hostile_function_probe_is_live(self, tmp_path):
        """Guards the test above. If the inherited definition never took effect,
        that test would pass while proving nothing -- so assert the same
        mechanism works against a shell that does not scrub."""
        marker = tmp_path / "PROVEN"
        hostile = (
            'echo() { command echo "REPLACED:$*"; }\n'
            f'echo hello > {shlex.quote(str(marker))}\n')
        subprocess.run(["bash", "-c", hostile], capture_output=True, text=True,
                       check=False)
        assert marker.read_text().startswith("REPLACED:"), (
            "the probe mechanism itself does not work")

    def test_the_loader_body_runs_in_a_clean_child_shell(self):
        """The structural property, on the recorded text."""
        block = _runbook_block("_gate_preflight.py")
        code = "\n".join(ln for ln in block.splitlines()
                         if ln.strip() and not ln.lstrip().startswith("#"))
        launch = code.splitlines()[0]
        assert "-i" in launch and "<maintainer-recorded-env>" in launch, (
            f"the loader must be launched through a recorded `env -i`: {launch}")
        assert "/bin/sh <<'LOADER'" in code, (
            "the body must be supplied to the literal /bin/sh")
        assert code.rstrip().endswith("LOADER"), (
            "the body must be fully enclosed by the clean-child heredoc")

    def test_the_operator_facing_shell_is_literally_bin_sh(self):
        """FUR10. The harness used to substitute `/bin/sh` for a recorded
        placeholder, so the tested property depended on a choice the runbook
        never told the operator to make. The value is now literal in the
        operator-facing text, and this asserts *that* text rather than the
        harness's substitution map."""
        block = _runbook_block("_gate_preflight.py")
        code = "\n".join(ln for ln in block.splitlines()
                         if ln.strip() and not ln.lstrip().startswith("#"))
        assert "/bin/sh <<'LOADER'" in code
        assert "<maintainer-recorded-shell>" not in block, (
            "the shell must not be an operator decision -- a wrong choice "
            "silently restores startup-file loading inside the clean child")

    @pytest.mark.skipif(not Path("/bin/zsh").exists(),
                        reason="needs /bin/zsh to demonstrate the hazard")
    def test_zsh_would_reopen_the_hole_under_the_same_environment(self,
                                                                  tmp_path):
        """Why the literal matters, demonstrated rather than asserted.

        `/bin/zsh` is the login default on this host, so a solo Maintainer could
        reasonably record it. Under the runbook's exact clean-child environment
        it still sources `$HOME/.zshenv`, which is where a pre-loader command
        definition would come back.
        """
        home = tmp_path / "home"
        home.mkdir()
        (home / ".zshenv").write_text(
            "echo() { command echo REPLACED; }\n", encoding="utf-8")
        env_bin, script = shutil.which("env"), "echo clean\n"

        zsh = subprocess.run(
            [env_bin, "-i", "PATH=/usr/bin:/bin", f"HOME={home}", "/bin/zsh"],
            input=script, capture_output=True, text=True, check=False)
        sh = subprocess.run(
            [env_bin, "-i", "PATH=/usr/bin:/bin", f"HOME={home}", "/bin/sh"],
            input=script, capture_output=True, text=True, check=False)

        assert "REPLACED" in zsh.stdout, (
            "if zsh no longer read .zshenv here, this hazard would be stale "
            "and the runbook note should be revisited")
        assert sh.stdout.strip() == "clean", (
            "/bin/sh must not read the startup file -- the whole basis for "
            "fixing the shell to it")


# ---------------------------------------------------------------------------
# Plan `git-native-security-foundations`, Chunks A5/A6: object-id width comes
# from the repository, and the evidence runs on the PUBLIC path.
# ---------------------------------------------------------------------------


class TestObjectFormatAwareWidth:
    """A fixed `len(sha) != 40` refuses a valid SHA-256 repository.

    The refusal happened in `_resolve`, which `check` and `apply` both call
    first -- so helper-level SHA-256 coverage could pass while the public path
    failed before ever reaching the helper. That is why A6 exercises `check`,
    not just `_blob_oid`-style internals.
    """

    @staticmethod
    def _repo(tmp_path: Path, object_format: str) -> Path:
        repo = tmp_path / object_format
        repo.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "-q",
                        f"--object-format={object_format}", "-b", "main",
                        str(repo)], check=True, capture_output=True)
        (repo / "seed.txt").write_text("seed\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "-A"],
                       check=True, capture_output=True)
        subprocess.run(["git", "-C", str(repo),
                        "-c", "user.name=T", "-c", "user.email=t@t.invalid",
                        "-c", "commit.gpgsign=false",
                        "commit", "-q", "-m", "seed"],
                       check=True, capture_output=True)
        return repo

    @pytest.mark.parametrize("object_format,width",
                             [("sha1", 40), ("sha256", 64)])
    def test_the_width_is_read_from_the_repository(self, tmp_path,
                                                   object_format, width):
        repo = self._repo(tmp_path, object_format)
        assert P._object_id_width(repo=repo) == width

    @pytest.mark.parametrize("object_format,width",
                             [("sha1", 40), ("sha256", 64)])
    def test_resolve_accepts_the_native_id_width(self, tmp_path,
                                                 object_format, width):
        # Perturbation: restore `len(sha) != 40`.  Red for sha256 -- git
        # returns a valid 64-hex HEAD and `_resolve` rejects it.
        repo = self._repo(tmp_path, object_format)
        sha = P._resolve("HEAD", repo=repo)
        assert len(sha) == width
        assert all(c in "0123456789abcdef" for c in sha)

    def test_a_non_repository_refuses_rather_than_assuming_sha1(self, tmp_path):
        plain = tmp_path / "plain"
        plain.mkdir()
        with pytest.raises(P.PreflightError) as exc:
            P._object_id_width(repo=plain)
        assert "refusing rather than assuming" in str(exc.value)


# ---------------------------------------------------------------------------
# Chunk B: the canonical range-review report.  B5 pins the report's own
# properties; B7 pins that its classes agree with the manifest policy.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def _live_report():
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(P._REPO),
                          capture_output=True, text=True).stdout.strip()
    anchor = subprocess.run(["git", "rev-parse", "HEAD~3"], cwd=str(P._REPO),
                            capture_output=True, text=True).stdout.strip()
    return P.range_review_report(anchor, head, branch="master",
                                 expected_old=head)


class TestRangeReviewReport:

    def test_the_digest_is_deterministic(self, _live_report):
        again = P.range_review_report(
            _live_report["anchor"], _live_report["candidate_head"],
            branch=_live_report["branch"],
            expected_old=_live_report["expected_old"])
        assert P.range_report_digest(again) == P.range_report_digest(_live_report)

    def test_every_path_is_in_exactly_one_class(self, _live_report):
        # Perturbation: let `_classify_path` return the first hit without the
        # multiply-classified guard, and add a path to two registries.  Red.
        assert sum(_live_report["counts"].values()) == len(_live_report["paths"])
        assert set(_live_report["by_class"]) == set(P._RANGE_CLASSES)

    def test_outside_coverage_is_listed_in_full_not_counted(self, _live_report):
        listed = _live_report["by_class"]["outside-coverage"]
        assert len(listed) == _live_report["counts"]["outside-coverage"]

    def test_path_identity_is_raw_bytes_round_tripped(self, _live_report):
        import base64
        for entry in _live_report["paths"]:
            raw = base64.b64decode(entry["bytes_b64"])
            assert P._display_path(raw) == entry["display"]

    def test_the_display_is_ascii_only(self, _live_report):
        for entry in _live_report["paths"]:
            entry["display"].encode("ascii")   # raises if it is not

    def test_a_display_that_is_not_a_rendering_of_its_bytes_refuses(self):
        with pytest.raises(P.PreflightError):
            P._verify_display(b"real/path.py", "something/else.py")

    @pytest.mark.parametrize("raw,expected", [
        (b"plain.py", "plain.py"),
        (b"with space.py", "with space.py"),
        (b"nl\nin-name", "nl\\x0ain-name"),
        (b"\xc3\xa9.py", "\\xc3\\xa9.py"),
        (b"back\\slash", "back\\x5cslash"),
    ])
    def test_the_escaping_is_total_and_reversible_in_shape(self, raw, expected):
        # A newline in a path must not be able to forge a record boundary in
        # anything a human reads, and a non-UTF-8 byte must not decode away.
        assert P._display_path(raw) == expected

    def test_ordering_is_by_raw_bytes(self, _live_report):
        import base64
        raws = [base64.b64decode(e["bytes_b64"]) for e in _live_report["paths"]]
        assert raws == sorted(raws)

    @pytest.mark.parametrize("field", [
        "anchor", "candidate_head", "anchor_tree", "candidate_tree",
        "branch", "expected_old", "manifest_schema", "manifest_sha256",
        "schema",
    ])
    def test_the_digest_moves_when_any_bound_field_moves(self, _live_report, field):
        import copy
        mutated = copy.deepcopy(_live_report)
        mutated[field] = str(mutated[field]) + "-mutated"
        assert P.range_report_digest(mutated) != P.range_report_digest(_live_report)

    def test_the_digest_moves_when_a_path_or_class_moves(self, _live_report):
        import copy
        mutated = copy.deepcopy(_live_report)
        assert mutated["paths"], "fixture must carry at least one path"
        mutated["paths"][0]["class"] = "frozen" if \
            mutated["paths"][0]["class"] != "frozen" else "outside-coverage"
        assert P.range_report_digest(mutated) != P.range_report_digest(_live_report)

    def test_signature_counts_are_diagnostics_not_a_verdict(self, _live_report):
        # R1-A: unsigned intermediate commits are the normal agent-work format.
        # Their presence must not be an authorization signal anywhere.
        sig = _live_report["signatures"]
        assert set(sig) == {"total", "good", "unsigned", "other"}
        assert sig["good"] + sig["unsigned"] + sig["other"] == sig["total"]


class TestReportAgreesWithManifestPolicy:
    """B7 -- the cross-contract corpus.

    B5 proves a *partition*.  It cannot prove the partition is **right**: a
    total-but-wrong classification would bind a misdescription with a perfect
    digest, and the Maintainer would sign an accurate-looking report of the
    wrong facts.
    """

    def test_the_classifier_consumes_the_manifest_source(self, _live_report):
        frozen = set(G._frozen_files(P._REPO))
        cascade = set(G.CASCADE_MUTABLE)
        phase = set(G.PHASE_SPLIT_TARGETS)
        for entry in _live_report["paths"]:
            rel = entry["display"]
            if entry["class"] == "frozen":
                assert rel in frozen, rel
            elif entry["class"] == "cascade-mutable":
                assert rel in cascade, rel
            elif entry["class"] == "phase-mutable":
                assert rel in phase, rel
            elif entry["class"] == "manifest-artifact":
                assert rel == G._MANIFEST_REL, rel
            else:
                assert rel not in frozen | cascade | phase, (
                    f"{rel} is in a manifest registry but reported "
                    f"outside-coverage -- the report and the policy disagree")

    def test_a_known_frozen_file_classifies_as_frozen(self):
        frozen = sorted(G._frozen_files(P._REPO))
        assert frozen, "the manifest must pin something"
        got = P._classify_path(frozen[0], set(frozen), set(G.CASCADE_MUTABLE),
                               set(G.PHASE_SPLIT_TARGETS), G._MANIFEST_REL)
        assert got == "frozen"

    def test_the_manifest_artifact_classifies_as_itself(self):
        got = P._classify_path(G._MANIFEST_REL, set(), set(), set(),
                               G._MANIFEST_REL)
        assert got == "manifest-artifact"

    def test_a_multiply_classified_path_refuses(self):
        # The dangerous case: a path in two registries would otherwise take
        # whichever branch happened to be first.
        with pytest.raises(P.PreflightError) as exc:
            P._classify_path("dup.py", {"dup.py"}, {"dup.py"}, set(), "m.json")
        assert "multiply classified" in str(exc.value)


# ---------------------------------------------------------------------------
# Chunk C: the checkpoint binds the reviewed report, and drift voids it.
# ---------------------------------------------------------------------------


class TestCheckpointBindsTheReport:

    def test_the_message_carries_the_digest_tree_and_head(self):
        msg = P.draft_message(
            observed_anchor="a" * 40, checked_head="b" * 40,
            manifest_sha256="c" * 64, authority_hashes={"x.py": "d" * 64},
            scope={}, range_report_digest="e" * 64, candidate_tree="f" * 40)
        assert "e" * 64 in msg
        assert "f" * 40 in msg
        assert "b" * 40 in msg

    def test_an_unbound_message_says_so_rather_than_looking_bound(self):
        # Perturbation: default the digest to "" instead of "(not bound)".  The
        # message then reads as though a digest were present but empty.
        msg = P.draft_message(
            observed_anchor="a" * 40, checked_head="b" * 40,
            manifest_sha256="c" * 64, authority_hashes={}, scope={})
        assert "(not bound)" in msg

    def test_rederivation_refuses_a_stale_confirmation(self):
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(P._REPO),
                              capture_output=True, text=True).stdout.strip()
        anchor = subprocess.run(["git", "rev-parse", "HEAD~3"], cwd=str(P._REPO),
                                capture_output=True, text=True).stdout.strip()
        with pytest.raises(P.RangeReportDrift) as exc:
            P.rederive_and_bind(anchor, head, branch="master",
                                expected_old=head, confirmed_digest="0" * 64)
        assert "confirmation is void" in str(exc.value)

    def test_rederivation_accepts_the_matching_digest(self):
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(P._REPO),
                              capture_output=True, text=True).stdout.strip()
        anchor = subprocess.run(["git", "rev-parse", "HEAD~3"], cwd=str(P._REPO),
                                capture_output=True, text=True).stdout.strip()
        good = P.range_report_digest(P.range_review_report(
            anchor, head, branch="master", expected_old=head))
        fresh = P.rederive_and_bind(anchor, head, branch="master",
                                    expected_old=head, confirmed_digest=good)
        assert P.range_report_digest(fresh) == good

    def test_a_draft_missing_a_binding_field_refuses_before_construction(self):
        """Caught on the draft, not after signing.

        `verify_constructed` re-parses the object and compares the exact
        message, which is stronger -- but by then a signature exists and the
        only remedy is to discard it.
        """
        msg = P.draft_message(
            observed_anchor="a" * 40, checked_head="b" * 40,
            manifest_sha256="c" * 64, authority_hashes={}, scope={},
            range_report_digest="e" * 64, candidate_tree="f" * 40)
        P.verify_message_binds_report(msg, digest="e" * 64, tree="f" * 40,
                                      head="b" * 40, anchor="a" * 40)
        with pytest.raises(P.PreflightError) as exc:
            P.verify_message_binds_report(msg, digest="9" * 64, tree="f" * 40,
                                          head="b" * 40, anchor="a" * 40)
        assert "does not bind" in str(exc.value)


# ---------------------------------------------------------------------------
# Chunk F: reflogs, and the atomic publication contract.
#
# Two failure shapes, one theme -- a partial result that reports as a whole one.
#
#   * A gate anchor that moves wrongly used to be UNRECOVERABLE, because custom
#     refs carry no reflog by default: the prior value simply was not written
#     down anywhere, so "put it back" had nothing to put back. `--create-reflog`
#     with a fixed reason closes that, and these tests hold it closed on the
#     *abort* path too -- an aborted transaction that leaves a reflog entry is
#     a record of something that did not happen.
#   * A non-atomic publication leaves the remote carrying a moved branch and a
#     stale anchor, and `git push` reports the parts that worked. Every fetcher
#     then verifies new code against an anchor that never blessed it.
#
# The reflog is a LOCAL, MUTABLE DIAGNOSTIC throughout. It is asserted here as
# recovery and sequencing information, never as tamper evidence: anyone who can
# write a ref can write its reflog. No decision predicate reads reflog content,
# and the tests below assert none of them do.
# ---------------------------------------------------------------------------


def _reflog(repo: Path, ref: str) -> list[str]:
    """The ref's reflog, newest first; `[]` when the ref has none.

    Read with `log -g` rather than `reflog show` so a missing reflog is an
    empty list instead of an error, which is the state the abort path must
    leave behind.
    """
    r = _run("git", "log", "-g", "--format=%gs", ref, cwd=repo)
    return r.stdout.splitlines() if r.returncode == 0 else []


class TestCeremonyReflogs:
    """F1/F4. Both refs record the ceremony on success; an abort records
    nothing, because it did nothing."""

    def _refs(self, repo: Path):
        return (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip())

    def _fresh(self, tmp_path):
        """An anchored repo with both reflogs cleared, so what the transaction
        writes is the only thing present afterwards."""
        repo, anchor, head = _anchored_repo(tmp_path)
        _run("git", "reflog", "expire", "--expire=all", "--all", cwd=repo)
        return repo, anchor, head

    def test_a_successful_transaction_identifies_the_ceremony_in_BOTH_reflogs(
            self, tmp_path):
        """The recovery property. A mis-set anchor is recoverable only if the
        prior value was written down, and only if the entry that wrote it is
        distinguishable from ordinary ref movement."""
        repo, anchor, head = self._fresh(tmp_path)
        target = P.R._construct_anchor_commit(
            repo, head, P._MANIFEST_REL,
            json.dumps(_FAKE_MANIFEST, indent=2, sort_keys=True).encode() + b"\n")

        ok, detail = P._advance_both_refs(repo, "refs/heads/master", target,
                                          branch_old=head, anchor_old=anchor)

        assert ok, detail
        for ref in ("refs/heads/master", P._ANCHOR_REF):
            entries = _reflog(repo, ref)
            assert entries, f"{ref} carries no reflog after the ceremony"
            assert entries[0] == P._CEREMONY_REFLOG_REASON, (
                f"{ref}@{{0}} is {entries[0]!r}, not the fixed ceremony reason")

    def test_the_prior_anchor_is_recoverable_from_the_reflog(self, tmp_path):
        """What the reflog is *for*, stated as a test rather than a comment:
        the value the ceremony overwrote is still readable afterwards."""
        repo, anchor, head = self._fresh(tmp_path)
        target = P.R._construct_anchor_commit(
            repo, head, P._MANIFEST_REL,
            json.dumps(_FAKE_MANIFEST, indent=2, sort_keys=True).encode() + b"\n")
        P._advance_both_refs(repo, "refs/heads/master", target,
                             branch_old=head, anchor_old=anchor)

        prior = _run("git", "rev-parse", f"{P._ANCHOR_REF}@{{1}}",
                     cwd=repo).stdout.strip()
        assert prior == anchor

    def test_a_stale_expected_old_abort_writes_NEITHER_ref_NOR_either_reflog(
            self, tmp_path):
        """An abort that leaves a reflog entry records something that did not
        happen -- and it is the reflog an operator reads when reconstructing
        what the ceremony did.
        """
        repo, anchor, head = self._fresh(tmp_path)
        target = P.R._construct_anchor_commit(
            repo, head, P._MANIFEST_REL,
            json.dumps(_FAKE_MANIFEST, indent=2, sort_keys=True).encode() + b"\n")
        before = self._refs(repo)

        ok, detail = P._advance_both_refs(repo, "refs/heads/master", target,
                                          branch_old=head, anchor_old="c" * 40)

        assert not ok and detail
        assert self._refs(repo) == before
        for ref in ("refs/heads/master", P._ANCHOR_REF):
            assert P._CEREMONY_REFLOG_REASON not in _reflog(repo, ref), (
                f"the aborted transaction left a ceremony entry on {ref}")

    def test_the_reason_is_fixed_by_the_module_not_chosen_by_the_caller(self):
        """A caller-supplied reason could label one ceremony as another, and
        both refs would then disagree about what moved them."""
        import inspect
        sig = inspect.signature(P._advance_both_refs)
        assert "reason" not in sig.parameters and "message" not in sig.parameters

    def test_git_reflog_is_in_neither_allowlist(self):
        """The cheapest half of the constraint, and the load-bearing one.

        Every git invocation in the module is funnelled through `_git` or
        `_git_write`, each gated on an enumerated subcommand set. `reflog` in
        neither set means `git reflog` cannot run at all -- not by oversight, by
        construction.
        """
        assert "reflog" not in P._READ_ONLY_GIT
        assert "reflog" not in P._WRITE_GIT

    def test_no_git_call_passes_a_reflog_reading_argument(self):
        """The other half: `git log -g` and an `@{N}` revision read reflog data
        through subcommands that *are* allowed.

        Walked with `ast` rather than grepped, because the module's prose is
        full of the word -- an earlier version of this test read the source as
        text and fired on the help string that tells an operator custom refs
        carry no reflog. Only argument expressions of an actual git call count.
        """
        import ast
        src = (P._REPO / "bootstrap/tests/_gate_preflight.py").read_text(
            encoding="utf-8")
        helpers = {"_git", "_git_write", "_run_git"}
        needles = ("-g", "--walk-reflogs", "@{")

        def literals(node):
            """Every string this expression can contribute, statically.

            Code review [IC4]: the first version inspected `ast.Constant` args
            only. Measured over this module, 25 of the 29 argument expressions
            in git calls are *not* constant strings -- 17 `Name`, 7 `JoinedStr`,
            1 `Starred` -- and the f-string is the module's normal way of
            writing a revision (`f"{ref}^{{commit}}"`). `@{` is one character
            from `^{`, so the guard covered exactly the shape nobody uses and
            missed the shape everybody uses. A placeholder-free `f"-g"` evaded
            it too, being a `JoinedStr`.

            Unresolvable expressions (a bare `Name`) cannot be judged here; the
            allowlist is what bounds those, since `reflog` is in neither.
            """
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                yield node.value
            elif isinstance(node, ast.JoinedStr):
                for part in node.values:
                    yield from literals(part)
            elif isinstance(node, ast.FormattedValue):
                # The format spec and conversion cannot carry `@{`, but the
                # surrounding JoinedStr parts can and are walked above.
                return
            elif isinstance(node, ast.BinOp):
                yield from literals(node.left)
                yield from literals(node.right)
            elif isinstance(node, ast.Starred):
                yield from literals(node.value)

        offenders = []
        for node in ast.walk(ast.parse(src)):
            if not isinstance(node, ast.Call):
                continue
            fn = node.func
            name = fn.id if isinstance(fn, ast.Name) else getattr(fn, "attr", "")
            if name not in helpers:
                continue
            for arg in node.args:
                for text in literals(arg):
                    if text in ("-g", "--walk-reflogs") or "@{" in text:
                        offenders.append((node.lineno, text))
        assert not offenders, (
            f"a git call reads reflog data: {offenders}. The ceremony writes "
            f"reflogs and must never let a predicate consume one -- whoever "
            f"can write a ref can write its reflog.")


class TestAtomicPublication:
    """F4. The publication contract, exercised against a real bare remote.

    Necessary but **not sufficient** to close [TRU-7]: a local bare remote
    accepts what a real forge might refuse (hooks, protected branches, ref
    namespace policy). M4 records a probe or the first supervised push against
    the real remote. These tests establish the mechanism, not the capability.
    """

    def _publish(self, tmp_path):
        """A repo with both ceremony refs advanced, and a bare remote behind."""
        repo = _repo(tmp_path)
        base = _commit(repo, "base")
        _run("git", "update-ref", P._ANCHOR_REF, base, cwd=repo)

        remote = tmp_path / "remote.git"
        _run("git", "init", "-q", "--bare", str(remote), cwd=tmp_path)
        _run("git", "remote", "add", "origin", str(remote), cwd=repo)
        _run("git", "push", "-q", "origin",
             "refs/heads/master:refs/heads/master",
             f"{P._ANCHOR_REF}:{P._ANCHOR_REF}", cwd=repo)

        new = _commit(repo, "candidate")
        _run("git", "update-ref", P._ANCHOR_REF, new, cwd=repo)
        return repo, remote, base, new

    def _remote_refs(self, remote: Path):
        return {ref: _run("git", "rev-parse", ref, cwd=remote).stdout.strip()
                for ref in ("refs/heads/master", P._ANCHOR_REF)}

    def _push(self, repo: Path, *extra: str):
        return _run("git", "push", "--atomic", "origin",
                    "refs/heads/master:refs/heads/master",
                    f"{P._ANCHOR_REF}:{P._ANCHOR_REF}", *extra, cwd=repo)

    def test_the_atomic_push_publishes_both_refs(self, tmp_path):
        repo, remote, base, new = self._publish(tmp_path)
        r = self._push(repo)
        assert r.returncode == 0, r.stderr
        assert self._remote_refs(remote) == {"refs/heads/master": new,
                                             P._ANCHOR_REF: new}

    def test_one_rejected_ref_moves_NEITHER_remote_ref(self, tmp_path):
        """The property `--atomic` exists for.

        The anchor is made non-fast-forward on the remote while the branch stays
        perfectly pushable. Without `--atomic` git publishes the branch, reports
        the anchor's rejection, and exits non-zero -- and the remote is left
        with new code under the previous trust root. An operator reading only
        "one ref failed" would then re-push the anchor and call it recovered,
        having never seen that the split state existed.
        """
        repo, remote, base, new = self._publish(tmp_path)
        divergent = _run("git", "commit-tree", f"{base}^{{tree}}", "-p", base,
                         "-m", "remote-side divergence",
                         cwd=repo).stdout.strip()
        _run("git", "push", "-q", "-f", "origin",
             f"{divergent}:{P._ANCHOR_REF}", cwd=repo)
        before = self._remote_refs(remote)
        assert before[P._ANCHOR_REF] == divergent

        r = self._push(repo)

        assert r.returncode != 0, "a non-fast-forward anchor must be rejected"
        assert self._remote_refs(remote) == before, (
            "the branch was published while the anchor was rejected: the "
            "remote now carries new code under the previous trust root")

    def test_without_atomic_the_split_state_is_real(self, tmp_path):
        """The counterfactual, so the flag is not cargo.

        Identical setup, `--atomic` dropped: the branch lands, the anchor does
        not, and git exits non-zero having already published half the ceremony.
        """
        repo, remote, base, new = self._publish(tmp_path)
        divergent = _run("git", "commit-tree", f"{base}^{{tree}}", "-p", base,
                         "-m", "remote-side divergence",
                         cwd=repo).stdout.strip()
        _run("git", "push", "-q", "-f", "origin",
             f"{divergent}:{P._ANCHOR_REF}", cwd=repo)

        r = _run("git", "push", "origin",
                 "refs/heads/master:refs/heads/master",
                 f"{P._ANCHOR_REF}:{P._ANCHOR_REF}", cwd=repo)

        assert r.returncode != 0
        after = self._remote_refs(remote)
        assert after["refs/heads/master"] == new
        assert after[P._ANCHOR_REF] == divergent, (
            "this test encodes the hazard; if it ever fails, git's non-atomic "
            "semantics changed and the runbook's rationale needs rereading")

    def test_a_clone_does_not_carry_the_anchor_without_an_explicit_refspec(
            self, tmp_path):
        """Why the runbook spells out the fetch refspec.

        `git clone` fetches `refs/heads/*` and `refs/tags/*`. A clone that looks
        complete has no anchor at all, so the gate has nothing to verify
        against -- and the failure surfaces later, as a missing ref, far from
        the clone that caused it.
        """
        repo, remote, base, new = self._publish(tmp_path)
        assert self._push(repo).returncode == 0

        clone = tmp_path / "clone"
        _run("git", "clone", "-q", str(remote), str(clone), cwd=tmp_path)
        assert _run("git", "rev-parse", P._ANCHOR_REF,
                    cwd=clone).returncode != 0

        _run("git", "fetch", "origin", f"+{P._ANCHOR_REF}:{P._ANCHOR_REF}",
             cwd=clone)
        assert _run("git", "rev-parse", P._ANCHOR_REF,
                    cwd=clone).stdout.strip() == new

    def test_the_authorization_ref_is_deleted_by_its_expected_old_value(
            self, tmp_path):
        """F3. A bare `-d` deletes whatever the ref points at, which is a
        different operation whenever that is not what this ceremony left."""
        repo, remote, base, new = self._publish(tmp_path)
        auth = "refs/cairn/gate-authorization"
        _run("git", "update-ref", auth, base, cwd=repo)

        stale = _run("git", "update-ref", "-d", auth, new, cwd=repo)
        assert stale.returncode != 0, "a stale expected-old deletion must fail"
        assert _run("git", "rev-parse", auth, cwd=repo).stdout.strip() == base

        exact = _run("git", "update-ref", "-d", auth, base, cwd=repo)
        assert exact.returncode == 0, exact.stderr
        assert _run("git", "rev-parse", auth, cwd=repo).returncode != 0

    def test_the_authorization_ref_is_never_published(self, tmp_path):
        """It authorizes one promotion. Published, it is a standing grant."""
        repo, remote, base, new = self._publish(tmp_path)
        auth = "refs/cairn/gate-authorization"
        _run("git", "update-ref", auth, base, cwd=repo)

        assert self._push(repo).returncode == 0

        assert _run("git", "rev-parse", auth, cwd=remote).returncode != 0, (
            "the ceremony's explicit refspecs published a ref outside them")


# ---------------------------------------------------------------------------
# F5. The runbook's publication text, tested as the recorded procedure.
#
# Same discipline as the Phase 0 loader tests above: a fix in code that the
# recorded steps do not carry is not a fix. Phase 5 is not executable here --
# it pushes to a real remote and that is M4's, not a test's -- so what is
# asserted is the *text*: the contract a Maintainer reads off the page.
# ---------------------------------------------------------------------------


def _runbook_section(heading: str) -> str:
    text = (P._REPO / "bootstrap/REANCHOR_RUNBOOK.md").read_text(
        encoding="utf-8")
    parts = text.split(heading)
    assert len(parts) == 2, f"expected exactly one {heading!r} section"
    return parts[1].split("\n## ")[0]


def _fenced(section: str) -> list[str]:
    return [b for i, b in enumerate(section.split("```")) if i % 2]


class TestRunbookPublicationText:

    def test_the_anchor_is_created_with_a_reflog_and_the_fixed_reason(self):
        """The runbook's own `update-ref` is where the anchor's reflog begins.

        Custom refs carry no reflog by default, so the *creating* command is the
        one place where omitting the flag means the ref has none for its whole
        life -- every later transaction appends to a log that starts there. This
        was a real gap: the recorded command was bare while the code it hands off
        to was careful, which is the FUR shape (a fix the recorded steps do not
        carry is not a fix).

        The reason is compared against the module constant rather than a literal,
        so the recorded command and the checker cannot drift into labelling the
        same anchor two different ways.
        """
        section = _runbook_section("\n### Phase 0 pre-flight")
        creations = [b for b in _fenced(section)
                     if "update-ref" in b and P._ANCHOR_REF in b]
        assert len(creations) == 1, (
            f"expected one recorded anchor-creation command, found "
            f"{len(creations)}")
        create = creations[0]
        assert "--create-reflog" in create
        assert P._CEREMONY_REFLOG_REASON in create, (
            f"the recorded command must label the anchor with "
            f"{P._CEREMONY_REFLOG_REASON!r}, the reason the checker writes")

    def test_the_authorization_ref_is_created_without_a_reflog(self):
        """The deliberate asymmetry, asserted so it reads as a decision rather
        than an oversight: `update-ref -d` removes a ref's reflog with it, so a
        log on a ref that is always deleted buys nothing."""
        section = _runbook_section("\n## Phase 4")
        creations = [b for b in _fenced(section)
                     if "update-ref" in b and "gate-authorization" in b
                     and " -d " not in b]
        assert len(creations) == 1
        assert "--create-reflog" not in creations[0]
        assert "ceremony-local" in section

    def test_publication_is_one_atomic_push_with_explicit_refspecs(self):
        blocks = _fenced(_runbook_section("\n## Phase 5"))
        pushes = [b for b in blocks if "push" in b]
        assert len(pushes) == 1, (
            f"Phase 5 records {len(pushes)} push commands; the contract is one")
        push = pushes[0]
        assert "--atomic" in push
        assert "refs/heads/<branch>:refs/heads/<branch>" in push
        assert f"{P._ANCHOR_REF}:{P._ANCHOR_REF}" in push
        for ambient in ("--all", "--mirror", "--tags"):
            assert ambient not in push, (
                f"{ambient} publishes a set the ceremony does not name")

    def test_no_partial_push_fallback_is_offered(self):
        """Scoped to the whole file, not to Phase 5.

        Code review [IC5]: this read only Phase 5 while its sibling
        `test_the_authorization_ref_appears_in_NO_push_or_fetch_block`
        deliberately reads the whole file and says why -- *"a later-added block
        is exactly where that would reappear."* That reasoning applies verbatim
        here and had not been applied: a `## Recovery appendix` with a
        ref-by-ref two-push passed all eleven of these tests, and a Maintainer
        following the recorded steps would reproduce by hand the split state
        `--atomic` exists to prevent.
        """
        section = _runbook_section("\n## Phase 5")
        assert "no two-push fallback" in section.lower()
        assert "incomplete publication" in section.lower()

        text = (P._REPO / "bootstrap/REANCHOR_RUNBOOK.md").read_text(
            encoding="utf-8")
        for block in _fenced(text):
            pushes = [ln for ln in block.splitlines()
                      if "push" in ln and not ln.lstrip().startswith("#")]
            assert len(pushes) <= 1, (
                f"a recorded block issues {len(pushes)} pushes; publishing the "
                f"two refs separately is the split state --atomic prevents:\n"
                f"{block}")
            for ln in pushes:
                assert "--force" not in ln and " -f " not in ln, (
                    f"a forced push in the recorded steps is a recovery that "
                    f"reproduces the hazard by hand:\n{ln}")
                assert "--atomic" in ln, (
                    f"every recorded push publishes both refs atomically:\n{ln}")

    def test_publication_is_verified_by_reading_the_remote_back(self):
        section = _runbook_section("\n## Phase 5")
        blocks = _fenced(section)
        assert any("ls-remote" in b for b in blocks), (
            "the push's exit status is the client's belief; the contract "
            "verifies against the remote")
        assert "availability, not authenticity" in section

    def test_the_fresh_clone_instructions_fetch_the_anchor_explicitly(self):
        blocks = _fenced(_runbook_section("\n## Phase 5"))
        fetches = [b for b in blocks if "fetch" in b]
        assert fetches, "no fetch instructions for a fresh clone"
        assert any(f"{P._ANCHOR_REF}:{P._ANCHOR_REF}" in b for b in fetches), (
            "clone fetches refs/heads/* and refs/tags/* only; without an "
            "explicit refspec a complete-looking clone has no anchor")

    def test_the_authorization_ref_is_retired_by_expected_old_value(self):
        section = _runbook_section("\n## Phase 4")
        deletions = [b for b in _fenced(section)
                     if "update-ref -d" in b and "gate-authorization" in b]
        assert len(deletions) == 1, "expected one recorded retirement command"
        assert "<A-sha>" in deletions[0], (
            "a bare -d deletes whatever the ref points at")
        assert "unresolved ceremony residue" in section.lower()

    def test_the_authorization_ref_appears_in_NO_push_or_fetch_block(self):
        """The absence property, over the whole runbook rather than one phase.

        It is ceremony-local. Any push or fetch block that names it publishes a
        standing authorization -- and a later-added block is exactly where that
        would reappear, which is why this reads every block in the file.
        """
        text = (P._REPO / "bootstrap/REANCHOR_RUNBOOK.md").read_text(
            encoding="utf-8")
        for block in _fenced(text):
            if any(verb in block for verb in ("push", "fetch", "clone",
                                              "ls-remote")):
                assert "gate-authorization" not in block, (
                    f"a publication block names the authorization ref:\n"
                    f"{block}")

    def test_phase_5_is_marked_maintainer_only(self):
        section = _runbook_section("\n## Phase 5")
        assert "M4" in section
        assert "Maintainer" in section
        text = (P._REPO / "bootstrap/REANCHOR_RUNBOOK.md").read_text(
            encoding="utf-8")
        assert "Phase 5" in text.split("---")[0], (
            "the header enumerates the phases an implementing agent must not "
            "perform; Phase 5 is one of them")
