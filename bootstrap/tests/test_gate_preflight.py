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

import json
import re
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

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


class TestSigningTripwire:
    """Committer name/email are supplied unauthenticated by the committing
    process, so the original equality check could be defeated by a second writer
    exporting the Maintainer's strings. Signature status cannot be forged."""

    def test_signed_by_a_pinned_key_is_silent(self, tmp_path, monkeypatch):
        repo, _key, _signers = _signing_repo(tmp_path)
        epoch = _signed_commit(repo, "epoch")
        monkeypatch.setattr(P, "_SIGNING_EPOCH", epoch)
        head = _signed_commit(repo, "work")
        report = P.Report()
        P.check_signatures(epoch, head, report, repo=repo)
        assert _findings(report, "SIGNING") == []
        assert report.facts["signing"]["checked"] >= 1

    def test_unsigned_commit_after_the_epoch_refuses(self, tmp_path, monkeypatch):
        repo, _key, _signers = _signing_repo(tmp_path)
        epoch = _signed_commit(repo, "epoch")
        monkeypatch.setattr(P, "_SIGNING_EPOCH", epoch)
        head = _commit(repo, "unsigned work")
        report = P.Report()
        P.check_signatures(epoch, head, report, repo=repo)
        assert any("not validly signed" in f.message and f.level == "refuse"
                   for f in _findings(report, "SIGNING"))

    def test_key_absent_from_the_pinned_roster_refuses(self, tmp_path,
                                                       monkeypatch):
        """A key git's own config would accept must still refuse.

        History worth keeping: the first version of this test was caught **vacuous**
        by mutation testing -- with the outsider key simply missing from git's
        roster, `%G?` was `U` and the check fired on signature *status*, leaving
        the principal comparison unexercised. It was rewritten to give git a
        roster containing both keys. The CR1 fix then changed the picture again:
        now that the roster is supplied *by invocation* from the closure-verified
        file, a key outside it can no longer reach `G` at all, so refusal comes
        through the status branch by design. That is the stronger arrangement --
        the principal comparison became defence-in-depth against roster-parse
        divergence rather than the primary control -- and this test asserts the
        security property (refusal) rather than which branch delivers it.
        """
        repo, key, signers = _signing_repo(tmp_path)
        epoch = _signed_commit(repo, "epoch")
        monkeypatch.setattr(P, "_SIGNING_EPOCH", epoch)

        outsider = _keypair(tmp_path, "outsider")
        maint_line = " ".join(key.with_suffix(".pub").read_text().split()[:2])
        out_line = " ".join(outsider.with_suffix(".pub").read_text().split()[:2])
        signers.write_text(f"m@example {maint_line}\noutsider@example {out_line}\n",
                           encoding="utf-8")          # git would accept both
        _write(repo, "dev/.cairn/allowed_signers", f"m@example {maint_line}\n")
        _run("git", "config", "user.signingkey",
             str(outsider.with_suffix(".pub")), cwd=repo)
        _run("git", "config", "user.email", "outsider@example", cwd=repo)
        head = _signed_commit(repo, "signed by a key the repo does not pin")

        assert _run("git", "log", "-1", "--format=%G?", cwd=repo
                    ).stdout.startswith("G"), (
            "setup must produce a signature git's own config accepts, so the "
            "refusal below is attributable to the pinned roster")

        report = P.Report()
        P.check_signatures(epoch, head, report, repo=repo)
        assert _findings(report, "SIGNING")

    def test_comma_separated_roster_principals_are_parsed(self, tmp_path):
        """`allowed_signers` permits `a@x,b@y <key>`; `%GS` reports only the
        matched principal. Parsing the field whole compared git's `a@x` against
        the literal `a@x,b@y` and **falsely refused a legitimate signer** --
        fail-closed, so not a hole, but a real correctness defect found while
        re-deriving which branch CR1's fix left reachable."""
        assert P.parse_principals(
            "a@x,b@y ssh-ed25519 AAAAKEY\n# comment\nc@z ssh-ed25519 AAAA2\n"
        ) == {"a@x", "b@y", "c@z"}

    def test_spoofed_committer_metadata_does_not_defeat_it(self, tmp_path,
                                                           monkeypatch):
        """The exact GPR2 attack: a second writer setting the Maintainer's
        committer strings. The old equality check passed; this must not."""
        repo, _key, _signers = _signing_repo(tmp_path)
        epoch = _signed_commit(repo, "epoch")
        monkeypatch.setattr(P, "_SIGNING_EPOCH", epoch)
        env = {**dict(__import__("os").environ),
               "GIT_COMMITTER_NAME": "M", "GIT_COMMITTER_EMAIL": "m@example"}
        _run("git", "-c", "user.name=Attacker", "-c", "user.email=evil@example",
             "commit", "-q", "--allow-empty", "-m", "spoofed", cwd=repo, env=env)
        head = _run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
        report = P.Report()
        P.check_signatures(epoch, head, report, repo=repo)
        assert _findings(report, "SIGNING"), (
            "an unsigned commit carrying spoofed committer metadata must still "
            "refuse -- this is the finding that falsified the original design")

    def test_roster_location_cannot_be_redirected_via_git_config(
            self, tmp_path, monkeypatch):
        """Plan finding CR1, as a regression guard.

        Verifying the roster's *contents* through the authority closure is not
        enough while its *location* is resolved through `.git/config` -- a
        channel the candidate controls and the read-only snapshot cannot observe.
        The attack never touches `dev/.cairn/allowed_signers`: it points git at a
        roster of its own that names **the same principal string** with the
        attacker's key, so `%G?` is `G` and `%GS` looks rostered while the pinned
        file stays byte-identical and the closure check passes.

        This test failed against the first implementation of `check_signatures`,
        which let git resolve the roster itself.
        """
        repo, _key, signers = _signing_repo(tmp_path)
        epoch = _signed_commit(repo, "epoch")
        monkeypatch.setattr(P, "_SIGNING_EPOCH", epoch)

        pinned_before = (repo / "dev/.cairn/allowed_signers").read_bytes()

        attacker = _keypair(tmp_path, "attacker")
        rogue = tmp_path / "attacker_roster"
        rogue.write_text(
            "m@example " + " ".join(
                attacker.with_suffix(".pub").read_text().split()[:2]) + "\n",
            encoding="utf-8")
        _run("git", "config", "gpg.ssh.allowedSignersFile", str(rogue), cwd=repo)
        _run("git", "config", "user.signingkey",
             str(attacker.with_suffix(".pub")), cwd=repo)
        head = _signed_commit(repo, "signed by an unrostered key")

        # The pinned roster is untouched, so the authority closure is satisfied.
        assert (repo / "dev/.cairn/allowed_signers").read_bytes() == pinned_before
        # And git, left to itself, reports this as a good, rostered signature.
        assert _run("git", "log", "-1", "--format=%G?%x09%GS",
                    cwd=repo).stdout.startswith("G\tm@example")

        report = P.Report()
        P.check_signatures(epoch, head, report, repo=repo)
        assert _findings(report, "SIGNING"), (
            "a commit signed by a key absent from the PINNED roster must refuse, "
            "even when .git/config points git at a roster that accepts it")

    def test_pre_epoch_commits_are_grandfathered(self, tmp_path, monkeypatch):
        """All 672 commits predating the epoch are unsigned; they must not fire."""
        repo, _key, _signers = _signing_repo(tmp_path)
        anchor = _commit(repo, "old unsigned")
        epoch = _signed_commit(repo, "epoch")
        monkeypatch.setattr(P, "_SIGNING_EPOCH", epoch)
        report = P.Report()
        P.check_signatures(anchor, epoch, report, repo=repo)
        assert _findings(report, "SIGNING") == []
        assert report.facts["signing"]["grandfathered"] == 0  # anchor..epoch

    def test_roster_absent_from_the_anchor_is_fail_closed(self, tmp_path):
        """The candidate's own copy is never a substitute for the anchor's."""
        repo = _repo(tmp_path)
        anchor = _commit(repo)
        _write(repo, "dev/.cairn/allowed_signers", "m@example ssh-ed25519 AAAA\n")
        _commit(repo, "candidate adds a roster after the anchor")
        with pytest.raises(P.PreflightError, match="absent from the anchor"):
            with P.anchored_roster(anchor, repo=repo):
                pass

    def test_roster_naming_no_principals_is_fail_closed(self):
        with pytest.raises(P.PreflightError, match="no principals"):
            P.parse_principals("# only a comment\n")

    def test_roster_is_read_from_the_anchor_not_the_worktree(self, tmp_path):
        """The ordering subtlety: a candidate that appends its own key to the
        worktree roster must not influence which keys count."""
        repo = _repo(tmp_path)
        _write(repo, "dev/.cairn/allowed_signers", "m@example ssh-ed25519 AAAA\n")
        anchor = _commit(repo, "anchor pins the roster")
        _write(repo, "dev/.cairn/allowed_signers",
               "m@example ssh-ed25519 AAAA\nevil@example ssh-ed25519 BBBB\n")
        _commit(repo, "candidate appends its own key")
        with P.anchored_roster(anchor, repo=repo) as (_path, text):
            assert P.parse_principals(text) == {"m@example"}


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
        epoch = _signed_commit(repo, "epoch")
        monkeypatch.setattr(P, "_SIGNING_EPOCH", epoch)

        outsider = _keypair(tmp_path, "outsider")
        _run("git", "config", "user.signingkey",
             str(outsider.with_suffix(".pub")), cwd=repo)
        head = _signed_commit(repo, "signed by an outsider")
        _run("git", "config", "gpg.ssh.program",
             str(_fake_ssh_keygen(tmp_path / "fake-keygen")), cwd=repo)

        # The attack is live: git itself now reports a good signature.
        assert _run("git", "log", "-1", "--format=%G?",
                    cwd=repo).stdout.strip() == "G"

        report = P.Report()
        P.check_signatures(epoch, head, report, repo=repo)
        assert any(f.level == "refuse" for f in _findings(report, "SIGNING")), (
            "a forged verifier must not let an unrostered key through")

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
        assert src.count("subprocess.run(") == 2, (
            "expected exactly two: the launcher, and the evidence stage's "
            "explicitly non-authoritative producer call")

    def test_git_env_channels_are_dropped(self, monkeypatch):
        monkeypatch.setenv("GIT_DIR", "/somewhere/else/.git")
        monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
        monkeypatch.setenv("GIT_EXTERNAL_DIFF", "/bin/sh")
        env = P._sterile_env()
        assert not [k for k in env if k.startswith("GIT_")
                    and k != "GIT_TERMINAL_PROMPT"]

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


def _pin_epoch_in_checker(repo: Path, epoch: str) -> None:
    """Rewrite the fixture's *copy* of the checker to name a real in-repo epoch.

    The epoch constant lives in the checker's own bytes on purpose, and a fixture
    repository cannot contain Cairn's actual epoch commit. Since FUR4 an absent
    epoch is a refusal rather than a silent grandfathering, so the ceremony
    fixture pins its own. Exactly one 40-character constant differs from the real
    file; the copy is what these tests execute, which is *also* the real
    ceremony's shape -- the anchored bytes, not the checkout's.
    """
    rel = "bootstrap/tests/_gate_preflight.py"
    src = (repo / rel).read_text(encoding="utf-8")
    old = f'_SIGNING_EPOCH = "{P._SIGNING_EPOCH}"'
    assert src.count(old) == 1, "epoch constant moved; update this fixture"
    (repo / rel).write_text(src.replace(old, f'_SIGNING_EPOCH = "{epoch}"'),
                            encoding="utf-8")


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
    _pin_epoch_in_checker(repo, epoch)
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
    """CR1's structural answer: there is nothing to tamper with."""

    def test_apply_now_accepts_no_bundle_or_digest(self):
        import inspect
        params = set(inspect.signature(P.apply_now).parameters)
        assert params == {"repo", "confirmed", "out"}, (
            f"apply must take no handoff artifact; got {sorted(params)}")

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
        with pytest.raises(P.PreflightError, match="explicit Maintainer"):
            P.apply_now(repo=repo, confirmed=False)
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
        # In-process, the executing constant is the real one; the fixture pinned
        # only its own committed copy. The subprocess tests need no equivalent --
        # they execute the anchored bytes, which carry the fixture's epoch.
        monkeypatch.setattr(P, "_SIGNING_EPOCH", epoch)
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
        res = P.apply_now(repo=repo, confirmed=True,
                          out=__import__("io").StringIO())
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
            lambda r, h, mb, msg: real(r, h, mb, "a different message\n"))
        before = self._refs(repo)
        with pytest.raises(P.PreflightError, match="reviewed message"):
            P.apply_now(repo=repo, confirmed=True,
                        out=__import__("io").StringIO())
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
            lambda r, h, mb, msg: (P.R._construct_anchor_commit(
                r, h, P._MANIFEST_REL, mb), "0" * 40))
        before = self._refs(repo)
        with pytest.raises(P.PreflightError, match="not validly signed|message"):
            P.apply_now(repo=repo, confirmed=True,
                        out=__import__("io").StringIO())
        assert self._refs(repo) == before

    def test_blocked_checks_write_nothing(self, tmp_path, monkeypatch):
        repo, anchor, head = self._prepared(tmp_path, monkeypatch)
        _write(repo, "bootstrap/tests/_gate_preflight.py", "# tampered\n")
        before = self._refs(repo)
        with pytest.raises(P.PreflightError, match="refuse this state"):
            P.apply_now(repo=repo, confirmed=True,
                        out=__import__("io").StringIO())
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

    def test_apply_refuses_without_confirmation_through_the_cli(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        before = (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                  _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip())
        r = self._cli("apply", "--repo", str(repo))
        assert r.returncode == 2
        assert "explicit Maintainer confirmation" in r.stderr
        assert (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                _run("git", "rev-parse", P._ANCHOR_REF,
                     cwd=repo).stdout.strip()) == before

    def test_malformed_evidence_is_refused_through_the_cli(self, tmp_path):
        repo, _a, _h = _anchored_repo(tmp_path)
        bad = tmp_path / "bad.json"
        bad.write_text("{not json")
        r = self._cli("check", "--repo", str(repo), "--evidence", str(bad))
        assert r.returncode == 2 and "not valid JSON" in r.stderr


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

        # The signing check must have verified something. Before FUR4 this
        # fixture could not contain the real epoch, `_rev_list` swallowed the
        # resulting error, and `checked` was 0 -- so the tripwire this whole
        # integration test is supposed to exercise had never fired on a single
        # commit. Zero here is indistinguishable from a check that does nothing.
        checked = re.search(r'"checked": (\d+)', r2.stderr)
        assert checked and int(checked.group(1)) >= 1, r2.stderr[-2500:]

        r3 = self._cli(checker, "apply", "--repo", str(repo),
                       "--confirm-supervised-reanchor")
        assert r3.returncode == 0, r3.stderr[-2500:]
        result = json.loads(r3.stdout)

        new_head = _run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
        new_anchor = _run("git", "rev-parse", P._ANCHOR_REF,
                          cwd=repo).stdout.strip()
        assert new_head == new_anchor == result["new_anchor"]
        assert _run("git", "log", "-1", "--format=%G?",
                    cwd=repo).stdout.strip() == "G"
        assert "Authorized verifier-module hashes" in _run(
            "git", "log", "-1", "--format=%B", cwd=repo).stdout
        assert _run("git", "status", "--porcelain", cwd=repo).stdout == ""

        # And the blessed manifest is the one the evidence stage produced.
        blessed = json.loads(_run("git", "show",
                                  f"{result['new_anchor']}:{P._MANIFEST_REL}",
                                  cwd=repo).stdout)
        assert blessed == evidence["manifest"]

    def test_a_second_run_refuses_because_the_state_moved(self, tmp_path):
        """Replay, honestly: no nonce, but the bound state no longer holds."""
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        checker = _extract_anchored(repo, tmp_path / "extract")
        assert self._cli(checker, "apply", "--repo", str(repo),
                         "--confirm-supervised-reanchor").returncode == 0
        again = self._cli(checker, "apply", "--repo", str(repo),
                          "--confirm-supervised-reanchor")
        assert again.returncode == 2


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
_LOADED_MODULES = (
    "bootstrap/tests/_gate_preflight.py",
    "bootstrap/tests/_gate_manifest.py",
    "bootstrap/tests/_gate_reanchor.py",
    "bootstrap/tests/_gate_transition.py",
    "bootstrap/tests/_oracle_activation.py",
    "bootstrap/tests/_oracle.py",
    "bootstrap/tests/_oracle_trust.py",
)


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
    section = text.split("### Phase 0 pre-flight")[1].split("\n## ")[0]
    blocks = [b for i, b in enumerate(section.split("```")) if i % 2]
    matching = [b for b in blocks if containing in b]
    assert len(matching) == 1, (
        f"expected exactly one Phase 0 block containing {containing!r}, "
        f"found {len(matching)}")
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
        "<maintainer-recorded-home>": os.environ.get("HOME", "/nonexistent"),
    }
    missing = [k for k, v in values.items() if not v]
    assert not missing, f"cannot resolve recorded utilities: {missing}"
    return values


def _substitute(block: str, repo: Path, *, hashes: bool = True) -> str:
    for placeholder, value in _recorded(repo).items():
        if placeholder in block:
            block = block.replace(placeholder, shlex.quote(value))
    assert "<maintainer-recorded" not in block.replace(
        "<maintainer-recorded-first-use-hashes>", ""), (
        f"an unrecorded placeholder survived substitution:\n{block}")
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

        r = subprocess.run(["bash", "-c", script], cwd=str(repo),
                           capture_output=True, text=True, check=False)

        assert r.returncode == 0, f"{script}\n---\n{r.stderr[-2500:]}"
        new = _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip()
        assert new == _run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
        assert new != anchor, "the ceremony reported success without blessing"

    def test_the_extraction_directory_is_not_itself_a_repository(self, tmp_path):
        """The premise the FUR5 shape depends on: were `$T` a repository, the
        no-`--repo` default would have silently worked and hidden the defect."""
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        extract = tmp_path / "T"
        _extract_anchored(repo, extract)
        assert not (extract / ".git").exists()

    def test_omitting_repo_refuses_diagnosably_and_moves_nothing(self, tmp_path):
        """The exact FUR5 defect. It was fail-closed but undiagnosable: git's
        bare `fatal: not a git repository` names neither the cause nor the fix."""
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        checker = _extract_anchored(repo, tmp_path / "T")
        before = (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                  _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip())

        r = self._cli(checker, "apply", "--confirm-supervised-reanchor")

        assert r.returncode == 2
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

class TestSigningRangeFailsClosed:

    def test_rev_list_raises_rather_than_returning_empty(self, tmp_path):
        repo = _repo(tmp_path)
        _commit(repo, "c")
        with pytest.raises(P.PreflightError) as exc:
            P._rev_list("nosuchref..HEAD", repo=repo)
        assert "unestablishable range" in str(exc.value)

    def test_is_ancestor_raises_on_error_rather_than_reporting_no(self,
                                                                  tmp_path):
        repo = _repo(tmp_path)
        head = _commit(repo, "c")
        with pytest.raises(P.PreflightError) as exc:
            P._is_ancestor("d" * 40, head, repo=repo)
        assert "could not decide" in str(exc.value)

    def test_missing_epoch_refuses_instead_of_grandfathering(self, tmp_path,
                                                             monkeypatch):
        """FUR4's reproduction, pinned: a missing epoch plus an unsigned commit
        inside the blessed range reported `checked=0` and emitted no finding."""
        repo, _key, _signers = _signing_repo(tmp_path)
        anchor = _signed_commit(repo, "anchor")
        head = _commit(repo, "unsigned work")          # inside anchor..HEAD
        monkeypatch.setattr(P, "_SIGNING_EPOCH", "c" * 40)   # absent object

        report = P.Report()
        P.check_signatures(anchor, head, report, repo=repo)

        assert any(f.level == "refuse" and "not present in this repository"
                   in f.message for f in _findings(report, "SIGNING"))
        assert report.facts["signing"]["resolved"] is None

    def test_epoch_off_the_head_line_refuses(self, tmp_path, monkeypatch):
        """Present but unrelated: "at or after the epoch" then names no range
        on the history being blessed, and the intersection is empty for a
        reason that has nothing to do with the commits being safe."""
        repo, _key, _signers = _signing_repo(tmp_path)
        base = _signed_commit(repo, "base")
        _run("git", "checkout", "-q", "-b", "side", cwd=repo)
        sidelined = _signed_commit(repo, "sidelined")
        _run("git", "checkout", "-q", "-", cwd=repo)
        anchor = _signed_commit(repo, "anchor")
        head = _commit(repo, "unsigned work")
        monkeypatch.setattr(P, "_SIGNING_EPOCH", sidelined)

        report = P.Report()
        P.check_signatures(anchor, head, report, repo=repo)

        assert any(f.level == "refuse" and "not an ancestor of HEAD"
                   in f.message for f in _findings(report, "SIGNING"))
        assert report.facts["signing"]["ancestor_of_head"] is False

    def test_a_resolvable_epoch_still_reports_its_resolution(self, tmp_path,
                                                             monkeypatch):
        """The clean case, so the two refusals above are not vacuous."""
        repo, _key, _signers = _signing_repo(tmp_path)
        epoch = _signed_commit(repo, "epoch")
        monkeypatch.setattr(P, "_SIGNING_EPOCH", epoch)
        head = _signed_commit(repo, "work")

        report = P.Report()
        P.check_signatures(epoch, head, report, repo=repo)

        assert _findings(report, "SIGNING") == []
        assert report.facts["signing"]["resolved"] == epoch
        assert report.facts["signing"]["ancestor_of_head"] is True


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

        r = subprocess.run(
            [sys.executable, "-E", "-s", str(checker), "apply",
             "--repo", str(repo), "--confirm-supervised-reanchor"],
            capture_output=True, text=True, check=False)
        assert r.returncode == 0, r.stderr[-2500:]

        new = json.loads(r.stdout)["new_anchor"]
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

        r = subprocess.run(["bash", "-c", script], cwd=str(repo),
                           capture_output=True, text=True, check=False)

        assert not (repo / "PWNED").exists(), (
            "the loader executed substituted checker bytes")
        assert r.returncode == 0, r.stderr[-2500:]

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

    def test_the_loader_covers_the_whole_import_closure(self, tmp_path):
        """A module missing from the recorded set would be absent at import
        time -- fail-closed, but only if the set is actually complete."""
        repo, anchor, head, epoch = _ceremony_repo(tmp_path)
        declared = {r for r in P.declared_authority_closure()
                    if r.endswith(".py")}
        assert declared == set(_LOADED_MODULES), (
            f"the loader's recorded set and the authority closure disagree: "
            f"{declared ^ set(_LOADED_MODULES)}")

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
        r = subprocess.run(
            ["bash", "-c", script], cwd=str(repo), capture_output=True,
            text=True, check=False,
            env={**_os.environ, "GIT_DIR": str(elsewhere / ".git")})

        assert r.returncode == 0, (
            f"GIT_DIR redirected the loader away from the named checkout: "
            f"{r.stderr[-1500:]}")
        assert _run("git", "rev-parse", P._ANCHOR_REF,
                    cwd=repo).stdout.strip() != anchor, "nothing was blessed"

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

        r = subprocess.run(["bash", "-c", script], cwd=str(repo), env=env,
                           capture_output=True, text=True, check=False)

        assert not (repo / "PWNED").exists(), (
            "a replacement shasum rewrote the checker and vouched for it")
        assert r.returncode == 0, r.stderr[-2500:]

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

        r = subprocess.run(["bash", "-c", hostile + script], cwd=str(repo),
                           capture_output=True, text=True, check=False)

        assert not pwned.exists(), (
            "an inherited shell function rewrote the checker and forged its "
            "checklist entry past the pinned verifier")
        assert r.returncode == 0, r.stderr[-2500:]

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
