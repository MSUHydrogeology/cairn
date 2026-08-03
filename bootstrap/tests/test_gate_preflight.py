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
