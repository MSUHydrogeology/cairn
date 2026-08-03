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
        assert "core.quotePath" in P._PINNED_CONFIG
        # and it is not overridden away by a per-call config dict
        _write(repo, "d/naïve.txt", "y\n")
        _run("git", "add", "-A", cwd=repo)
        assert "d/naïve.txt" in P._index_entries(repo=repo)


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
# Chunks C + D -- the bundle, and the application transaction
# --------------------------------------------------------------------------

_MANIFEST = {"frozen_files": {"a.py": "sha256:aa"},
             "collection": {"node_count": 2, "node_ids": ["a::t", "b::t"]}}


def _manifest_bytes(manifest=None):
    return (json.dumps(manifest or _MANIFEST, indent=2, sort_keys=True)
            .encode() + b"\n")


def _anchored_repo(tmp_path: Path):
    """A repo with an anchor ref and a later HEAD -- enough for `apply`."""
    repo = _repo(tmp_path)
    _write(repo, "bootstrap/tests/fixtures/gate_manifest.json", "{}\n")
    anchor = _commit(repo, "anchor")
    _run("git", "update-ref", P._ANCHOR_REF, anchor, cwd=repo)
    _write(repo, "code.py", "x = 1\n")
    head = _commit(repo, "work to bless")
    return repo, anchor, head


def _bundle_for(repo: Path, anchor: str, head: str, manifest=None,
                last_legitimate: str | None = None) -> dict:
    report = P.Report()
    report.facts.update({
        "anchor": anchor, "head": head,
        "authority_hashes": {f"bootstrap/tests/_m{i}.py": f"sha256:{i:064d}"
                             for i in range(6)},
    })
    body = _manifest_bytes(manifest)
    evidence = {"schema": P.EVIDENCE_SCHEMA, "candidate_sha": head,
                "interpreter": "3.13.13", "manifest": manifest or _MANIFEST,
                "manifest_sha256": P._sha256_bytes(body)}
    return P.build_bundle(report, evidence, repo=repo,
                          last_legitimate_anchor=last_legitimate)


class TestBundle:
    def test_round_trips(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        assert P.parse_bundle(json.dumps(b))["checked_head"] == head

    def test_message_carries_the_audit_trail(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        msg = b["message"]
        for h in b["authority_hashes"].values():
            assert h in msg, "every authority hash must be in the message"
        assert anchor in msg and head in msg

    def test_message_carries_no_self_referential_sha(self, tmp_path):
        """Security review SR4: a commit's SHA hashes its own message, so the
        message cannot contain it. The honest form is 'this commit'."""
        repo, anchor, head = _anchored_repo(tmp_path)
        msg = _bundle_for(repo, anchor, head)["message"]
        assert "new anchor P        : this commit" in msg

    def test_tampered_message_is_fail_closed(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        b["message"] += "\nand also bless everything else\n"
        with pytest.raises(P.PreflightError, match="does not match its recorded"):
            P.parse_bundle(json.dumps(b))

    @pytest.mark.parametrize("missing", ["checked_head", "observed_anchor",
                                         "manifest", "manifest_sha256",
                                         "message", "message_sha256"])
    def test_missing_fields_are_fail_closed(self, tmp_path, missing):
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        del b[missing]
        with pytest.raises(P.PreflightError, match=missing):
            P.parse_bundle(json.dumps(b))

    def test_unknown_schema_is_fail_closed(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        b["schema"] = 99
        with pytest.raises(P.PreflightError, match="schema"):
            P.parse_bundle(json.dumps(b))

    def test_recovery_mode_never_claims_to_have_inferred_legitimacy(self,
                                                                    tmp_path):
        """SR4's second half: nothing can derive the last legitimate anchor --
        custom refs carry no reflog -- so it is Maintainer-supplied, and the
        erroneous current ref is disclosed separately."""
        repo, anchor, head = _anchored_repo(tmp_path)
        legit = "b" * 40
        msg = _bundle_for(repo, anchor, head, last_legitimate=legit)["message"]
        assert "NOT inferred" in msg
        assert legit in msg
        assert anchor in msg, "the erroneous ref must still be disclosed"


class TestApplyTransaction:
    def _refs(self, repo: Path):
        return (_run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip(),
                _run("git", "rev-parse", P._ANCHOR_REF, cwd=repo).stdout.strip())

    def test_refuses_without_explicit_confirmation(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        before = self._refs(repo)
        with pytest.raises(P.PreflightError, match="explicit Maintainer"):
            P.apply_bundle(b, repo=repo, confirmed=False)
        assert self._refs(repo) == before

    def test_write_path_allowlist_refuses_anything_but_update_ref(self, tmp_path):
        repo, _a, _h = _anchored_repo(tmp_path)
        for bad in ("commit", "push", "checkout", "gc"):
            with pytest.raises(P.PreflightError, match="apply may only run"):
                P._git_write(bad, repo=repo)

    def test_head_moved_after_check_refuses(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        _commit(repo, "drift")
        before = self._refs(repo)
        with pytest.raises(P.PreflightError, match="HEAD moved"):
            P.apply_bundle(b, repo=repo, confirmed=True)
        assert self._refs(repo) == before

    def test_anchor_moved_after_check_refuses(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        _run("git", "update-ref", P._ANCHOR_REF, head, cwd=repo)
        with pytest.raises(P.PreflightError, match="anchor moved"):
            P.apply_bundle(b, repo=repo, confirmed=True)

    def test_manifest_body_digest_mismatch_refuses(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        b["manifest"] = {"frozen_files": {"injected": "x"}}
        b["message_sha256"] = P._sha256_bytes(b["message"].encode())
        with pytest.raises(P.PreflightError, match="does not match its digest"):
            P.apply_bundle(b, repo=repo, confirmed=True)

    def test_detached_head_refuses(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        _run("git", "checkout", "-q", "--detach", head, cwd=repo)
        with pytest.raises(P.PreflightError, match="detached"):
            P.apply_bundle(b, repo=repo, confirmed=True)

    def test_success_advances_both_refs_to_the_verified_commit(self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        out = P.apply_bundle(b, repo=repo, confirmed=True,
                             out=__import__("io").StringIO())
        new_head, new_anchor = self._refs(repo)
        assert new_head == new_anchor == out["new_anchor"]
        parents = _run("git", "rev-parse", f"{out['new_anchor']}^@",
                       cwd=repo).stdout.split()
        assert parents == [head], "the blessing commit's parent must be HEAD"
        changed = _run("git", "diff", "--name-only", f"{head}..{new_head}",
                       cwd=repo).stdout.split()
        assert changed == [P._MANIFEST_REL], "the diff must be the manifest only"

    def test_stale_anchor_aborts_leaving_BOTH_refs_unmoved(self, tmp_path):
        """Security review SR8, the core property.

        Creating the commit and *then* advancing the anchor would leave a
        blessing-shaped commit on the branch when the anchor CAS failed. One
        expected-old transaction aborts wholesale instead.

        The first version of this test was caught VACUOUS by mutation: it passed
        `new=head`, which makes the branch update a no-op that succeeds even
        under sequential single-ref updates, so it could not detect the very
        anti-pattern it names. It now advances to a genuinely different commit.
        """
        repo, anchor, head = _anchored_repo(tmp_path)
        target = P.R._construct_anchor_commit(
            repo, head, P._MANIFEST_REL, _manifest_bytes())
        assert target != head, "the transaction must actually move the branch"
        before = self._refs(repo)
        ok, detail = P._advance_both_refs(
            repo, "refs/heads/master", target,
            branch_old=head, anchor_old="c" * 40)   # stale anchor expectation
        assert not ok, "a stale expected-old must abort the transaction"
        assert self._refs(repo) == before, (
            "neither ref may move when the transaction aborts")
        assert detail

    def test_constructed_commit_touching_more_than_the_manifest_refuses(
            self, tmp_path, monkeypatch):
        """The pre-ref-move verification, exercised directly.

        Mutation testing found this guard entirely untested: removing it broke
        nothing, because no natural path produces a wrong constructed commit.
        Substituting the constructor is the honest way to reach it.
        """
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        _write(repo, "unrelated.py", "sneaky = True\n")
        rogue = _commit(repo, "extra content")
        _run("git", "update-ref", "refs/heads/master", head, cwd=repo)
        monkeypatch.setattr(P.R, "_construct_anchor_commit",
                            lambda *a, **k: rogue)
        before = self._refs(repo)
        with pytest.raises(P.PreflightError, match="changes"):
            P.apply_bundle(b, repo=repo, confirmed=True,
                           out=__import__("io").StringIO())
        assert self._refs(repo) == before, "no ref may move on a failed verify"

    def test_constructed_commit_with_the_wrong_parent_refuses(
            self, tmp_path, monkeypatch):
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        monkeypatch.setattr(P.R, "_construct_anchor_commit",
                            lambda *a, **k: anchor)   # parent is not HEAD
        before = self._refs(repo)
        with pytest.raises(P.PreflightError, match="parent"):
            P.apply_bundle(b, repo=repo, confirmed=True,
                           out=__import__("io").StringIO())
        assert self._refs(repo) == before

    def test_a_constructed_but_unblessed_commit_never_reaches_the_branch(
            self, tmp_path):
        repo, anchor, head = _anchored_repo(tmp_path)
        before = self._refs(repo)
        new = P.R._construct_anchor_commit(
            repo, head, P._MANIFEST_REL, _manifest_bytes())
        ok, _ = P._advance_both_refs(repo, "refs/heads/master", new,
                                     branch_old=head, anchor_old="d" * 40)
        assert not ok
        assert self._refs(repo) == before
        # the object exists but is unreferenced -- inspectable, not hidden
        assert _run("git", "cat-file", "-t", new, cwd=repo).stdout.strip() == \
            "commit"

    def test_replay_after_success_refuses_because_the_refs_moved(self, tmp_path):
        """SR10's real contract: revalidate-and-confirm, not mechanical
        single-use. There is no nonce; what stops a replay is that the bound
        state no longer holds."""
        repo, anchor, head = _anchored_repo(tmp_path)
        b = _bundle_for(repo, anchor, head)
        P.apply_bundle(b, repo=repo, confirmed=True,
                       out=__import__("io").StringIO())
        with pytest.raises(P.PreflightError, match="moved"):
            P.apply_bundle(b, repo=repo, confirmed=True,
                           out=__import__("io").StringIO())
