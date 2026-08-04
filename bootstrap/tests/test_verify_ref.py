#!/usr/bin/env python3
"""Release-authenticity tests for ``bootstrap/container/verify-ref.sh`` and for
the out-of-band bootstrap block published in ``bootstrap/PROVENANCE.md``
(plan ``release-authenticity``).

Everything here drives the shell script **through its command line** via
``subprocess`` — never by sourcing a function — in throwaway repositories built
from ephemeral SSH keys generated per test session.  No key material belonging to
anybody is used, and nothing is written into the Cairn tree.

Three things this module is shaped to prevent, each learned from a landed defect:

* **Tag substitution.** A ref re-pointed at an *older, genuinely signed* tag
  object verifies with a real signature over the wrong release name.  The name
  binding is the control; :func:`test_substitution_attack_refused_naming_both_names`
  is its oracle, and the mutation nodes prove the oracle is not vacuous.
* **Negative assertions that pass for any refusal.**  Every refusal node asserts
  on the **exit code** and, where a second refusal path could satisfy it, on the
  **reason string** too.
* **A document that drifts away from the procedure it publishes.**  The
  bootstrap block is *extracted from* ``bootstrap/PROVENANCE.md`` and executed,
  so a change to the document that breaks the procedure fails here.

There are **no skip guards**: the suite's contract is 0 skipped / 0 xfailed, and
a host without ``git`` or ``ssh-keygen`` must fail this module rather than
silently record a pass.  :func:`test_verification_toolchain_is_present` is that
fail-closed check.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "bootstrap" / "container" / "verify-ref.sh"
ACCEPTANCE = REPO_ROOT / "bootstrap" / "container" / "acceptance.sh"
PROVENANCE_MD = REPO_ROOT / "bootstrap" / "PROVENANCE.md"
CONTAINER_DIR = REPO_ROOT / "bootstrap" / "container"
CAIRN_GATE_ROSTER = REPO_ROOT / "dev" / ".cairn" / "allowed_signers"

# The script's documented exit contract.  Named, because a bare ``1`` in an
# assertion says nothing about which of four outcomes was expected.
PROVENANCED = 0
REFUSED = 1
USAGE = 2
NOT_PROVENANCED = 3

GENUINE_PRINCIPAL = "maint@example.org"
ATTACKER_PRINCIPAL = "attacker@example.invalid"


# --------------------------------------------------------------------------- lab
class Lab:
    """A throwaway world: ephemeral keys, isolated git config, candidate repos."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.home = root / "home"
        self.home.mkdir(parents=True, exist_ok=True)
        # An EMPTY global/system config, so nothing the developer running the
        # suite has configured can influence a verification result.
        self._empty_cfg = root / "gitconfig-empty"
        self._empty_cfg.write_text("")
        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "GIT_CONFIG_GLOBAL": str(self._empty_cfg),
            "GIT_CONFIG_SYSTEM": str(self._empty_cfg),
            "GIT_AUTHOR_NAME": "lab",
            "GIT_AUTHOR_EMAIL": GENUINE_PRINCIPAL,
            "GIT_COMMITTER_NAME": "lab",
            "GIT_COMMITTER_EMAIL": GENUINE_PRINCIPAL,
        }
        self.env.pop("CAIRN_ALLOWED_SIGNERS", None)

    # -- primitives ---------------------------------------------------------
    def git(self, repo: Path, *args: str, check: bool = True, env_extra=None):
        env = dict(self.env)
        if env_extra:
            env.update(env_extra)
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, check=check, env=env,
        )

    def keypair(self, name: str) -> Path:
        """Generate an ephemeral ed25519 key; return the PRIVATE key path."""
        priv = self.root / f"key-{name}"
        subprocess.run(
            ["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-C", name, "-f", str(priv)],
            check=True, capture_output=True, text=True, env=self.env,
        )
        return priv

    def roster(self, name: str, *lines: str) -> Path:
        path = self.root / f"roster-{name}"
        path.write_text("".join(line.rstrip("\n") + "\n" for line in lines))
        return path

    def repo(self, name: str, signing_key: Path | None = None) -> Path:
        path = self.root / name
        path.mkdir(parents=True, exist_ok=True)
        self.git(path, "init", "-q", "-b", "master")
        self.git(path, "config", "user.email", GENUINE_PRINCIPAL)
        self.git(path, "config", "user.name", "lab")
        if signing_key is not None:
            self.git(path, "config", "gpg.format", "ssh")
            self.git(path, "config", "user.signingkey", str(signing_key))
        return path

    def commit(self, repo: Path, content: str = "x") -> str:
        (repo / "f.txt").write_text(content)
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-q", "-m", f"commit {content}")
        return self.git(repo, "rev-parse", "HEAD").stdout.strip()

    def sign_tag(self, repo: Path, tag: str, date: str | None = None) -> str:
        extra = {"GIT_COMMITTER_DATE": date} if date else None
        self.git(repo, "tag", "-s", tag, "-m", f"release {tag}", env_extra=extra)
        return self.git(repo, "rev-parse", f"refs/tags/{tag}").stdout.strip()

    # -- driving the script -------------------------------------------------
    def verify(self, *args: str, env_extra=None,
               cwd: Path | None = None) -> subprocess.CompletedProcess:
        env = dict(self.env)
        if env_extra:
            env.update(env_extra)
        return subprocess.run(
            ["bash", str(SCRIPT), *[str(a) for a in args]],
            capture_output=True, text=True, env=env,
            cwd=None if cwd is None else str(cwd),
        )


def _pub(priv: Path) -> str:
    return Path(str(priv) + ".pub").read_text().strip()


@pytest.fixture(scope="session")
def lab(tmp_path_factory) -> Lab:
    """The genuine world: one maintainer key, one rostered principal, one
    candidate repository carrying a genuine signed ``v0.3.0``."""
    world = Lab(tmp_path_factory.mktemp("verify_ref_lab"))
    world.maint = world.keypair("maint")
    world.attacker = world.keypair("attacker")
    world.good_roster = world.roster(
        "good", f"{GENUINE_PRINCIPAL} {_pub(world.maint)}")
    # Same principal string, WRONG key: the crypto check must still refuse.
    world.wrong_roster = world.roster(
        "wrong", f"{GENUINE_PRINCIPAL} {_pub(world.attacker)}")

    cand = world.repo("cand", signing_key=world.maint)
    world.commit(cand, "base")
    world.signed_obj = world.sign_tag(cand, "v0.3.0")
    world.git(cand, "tag", "lw", "HEAD")                       # ref -> commit
    world.git(cand, "tag", "-a", "unsigned", "-m", "annotated, unsigned")
    world.candidate = cand
    return world


@pytest.fixture()
def mirror(lab: Lab, tmp_path: Path) -> Path:
    """An attacker-controlled bare mirror — the shape a forge serves — with
    ``v0.4.0`` re-pointed at the genuinely signed ``v0.3.0`` tag object.  No
    signing key is needed to build this."""
    dest = tmp_path / "mirror.git"
    subprocess.run(
        ["git", "clone", "-q", "--bare", str(lab.candidate), str(dest)],
        check=True, capture_output=True, text=True, env=lab.env,
    )
    lab.git(dest, "update-ref", "refs/tags/v0.4.0", lab.signed_obj)
    return dest


# ------------------------------------------------------- fail-closed toolchain
def test_verification_toolchain_is_present():
    """No skip guard anywhere in this module: a host that cannot verify must
    FAIL, because a missing gate recorded as a pass is the failure this whole
    scope exists to prevent."""
    assert shutil.which("git"), "git is not on PATH; verification cannot be tested"
    assert shutil.which("ssh-keygen"), "ssh-keygen is not on PATH; SSH signature verification cannot be tested"


# ============================================================== Chunk A — A5/A6
def test_honest_signed_tag_is_provenanced(lab: Lab):
    """Case (b): the honest tag must still pass.  A fix that refuses everything
    is not a fix."""
    r = lab.verify("--signers", lab.good_roster, lab.candidate, "v0.3.0")
    assert r.returncode == PROVENANCED, r.stderr
    assert "PROVENANCED" in r.stdout
    assert "v0.3.0" in r.stdout
    assert GENUINE_PRINCIPAL in r.stdout


def test_substitution_attack_refused_naming_both_names(lab: Lab, mirror: Path):
    """Case (a), and the [I1] BLOCKING finding: a ref re-pointed at an older,
    genuinely signed tag object.  The signature is real; the signed name is not
    the name that was asked about.

    Part B class table row: *tag ref whose object is an annotated tag object
    signed under a different name*.
    """
    r = lab.verify("--signers", lab.good_roster, mirror, "v0.4.0")
    assert r.returncode == REFUSED, f"substitution accepted: {r.stdout}{r.stderr}"
    assert "v0.4.0" in r.stderr, "the refusal must name the ref that was ASKED for"
    assert "v0.3.0" in r.stderr, "the refusal must name the SIGNED name it found"


def test_honest_tag_wrong_roster_is_refused(lab: Lab):
    """Case (c): the name binding must not become the only check.  Same
    principal string, wrong key."""
    r = lab.verify("--signers", lab.wrong_roster, lab.candidate, "v0.3.0")
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "did not verify" in r.stderr


def test_nested_unsigned_wrap_refuses_at_the_signature_half(lab: Lab, tmp_path: Path):
    """A6.  An attacker needs no key to write an *unsigned* tag object named
    ``v0.5.0`` whose target is the genuine signed tag object.  ``^{tag}`` does
    not peel through, so the NAME check passes and the SIGNATURE check refuses.
    Asserting *which* half refused is what keeps the two halves independently
    load-bearing.

    Part B class table row: *tag ref resolving to an unsigned tag object,
    including one wrapping a signed tag object*.
    """
    cand = tmp_path / "wrapper"
    shutil.copytree(lab.candidate, cand)
    lab.git(cand, "tag", "-a", "v0.5.0", "-m", "wrap", lab.signed_obj)
    r = lab.verify("--signers", lab.good_roster, cand, "v0.5.0")
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "carries NO SIGNATURE" in r.stderr, \
        "the SIGNATURE half must be the one that refused a correctly-named wrap"
    assert "SIGNED name" not in r.stderr, \
        "the name half must PASS here — if it refused, the wrap was not built as intended"


HOSTILE_TAG = "v0.6.0"


def _hostile_candidate(lab: Lab, root: Path) -> tuple[Path, Path]:
    """A candidate that supplies BOTH halves of a verification it would like to
    choose — the verifier program *and* the roster — over a tag that really is
    signed (by the attacker's key).

    Every one of those three properties is load-bearing, measured 2026-08-03
    under git 2.53.0:

    * **The tag must be SIGNED.**  git invokes no signature-verifier program at
      all for an unsigned tag (``error: no signature found``, and the program is
      never spawned), so a fixture built on an unsigned tag can never trip the
      witness — the assertion would hold no matter whose config was honoured.
      That was this node's own defect.
    * **``gpg.ssh.allowedSignersFile`` must be set too.**  With
      ``gpg.ssh.program`` alone, git stops at ``gpg.ssh.allowedSignersFile needs
      to be configured and exist`` *before* spawning the program.
    * **The signing key must be the ATTACKER's**, so the genuine roster refuses
      and the node's exit-code assertion still discriminates.

    Returns ``(candidate, witness_path)``.  The witness must not appear.
    """
    cand = root / "hostile"
    shutil.copytree(lab.candidate, cand)

    # Sign FIRST, with the attacker key and the real ssh-keygen: gpg.ssh.program
    # is used for signing as well as verifying, so the forger must not be
    # installed until after the tag exists.
    lab.git(cand, "config", "user.signingkey", str(lab.attacker))
    lab.sign_tag(cand, HOSTILE_TAG)

    witness = root / "forger-ran.witness"
    forger = root / "forger.sh"
    # The forger emits the principal on **stdout** deliberately: a forger that
    # wrote to stderr and exited 1 would make the node pass for the wrong reason.
    forger.write_text(
        "#!/usr/bin/env bash\n"
        f'echo ran > "{witness}"\n'
        f'echo \'Good "git" signature for {GENUINE_PRINCIPAL} with ED25519 key SHA256:forged\'\n'
        "exit 0\n"
    )
    forger.chmod(0o755)
    inside_roster = cand / "attacker-signers"
    inside_roster.write_text(f"{GENUINE_PRINCIPAL} {_pub(lab.attacker)}\n")
    lab.git(cand, "config", "gpg.format", "ssh")
    lab.git(cand, "config", "gpg.ssh.program", str(forger))
    lab.git(cand, "config", "gpg.ssh.allowedSignersFile", str(inside_roster))
    return cand, witness


def test_candidate_gpg_ssh_program_never_executes(lab: Lab, tmp_path: Path):
    """A7.  A hostile candidate names a forging verifier in its own config.  The
    verification runs in a workspace this script created with the verifier pinned
    by invocation, so the forger must never execute — proved by a witness file
    that must not appear.

    Non-vacuity is not asserted here, it is *demonstrated* by
    :func:`test_mutation_verifying_inside_the_candidate_runs_the_forger`, which
    replaces the pinned workspace verification with ``git -C "$REPO" verify-tag``
    and watches this exact fixture forge a good signature.
    """
    cand, witness = _hostile_candidate(lab, tmp_path)
    r = lab.verify("--signers", lab.good_roster, cand, HOSTILE_TAG)
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert not witness.exists(), \
        "the candidate's configured verifier EXECUTED — the candidate supplied verification material"
    assert "SHA256:forged" not in r.stdout + r.stderr, \
        "the forger's output reached the report"


# ------------------------------------------------------------------ Chunk A/A8
def test_resolver_names_the_non_tag_object_cause(lab: Lab):
    """A8, first half.  A ref that exists and points straight at a commit.

    Part B class table row: *tag ref resolving to a non-tag object (a commit, a
    tree)*.  C5's per-row sweep inherits this node rather than adding a second.

    The reason string is the assertion, not the exit code: a node asserting only
    "refused" passes equally against a script that simply could not find the tag
    (P3, oracle discrimination), and only the specific reason tells an adopter
    whose fork tagged with ``git tag`` something they can act on.
    """
    r = lab.verify("--signers", lab.good_roster, lab.candidate, "lw")
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "NON-TAG object" in r.stderr, r.stderr
    assert "no such tag ref" not in r.stderr, \
        "the two resolver causes must not collapse into one message"


def test_resolver_names_the_missing_ref_cause(lab: Lab):
    """A8, second half.  A ref that does not exist at all — a DIFFERENT reason
    from the non-tag-object case above, so one message cannot satisfy both."""
    r = lab.verify("--signers", lab.good_roster, lab.candidate, "no-such-tag")
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "no such tag ref" in r.stderr, r.stderr
    assert "NON-TAG object" not in r.stderr


def test_relative_candidate_path_reaches_the_candidate(lab: Lab):
    """A4's honest path, from a cwd that is not the candidate's parent.

    The top-level repository probe runs ``git -C "$REPO"`` from the CALLER's cwd,
    but the fetch runs ``git -C "$WORKSPACE"``.  A relative candidate path is
    therefore resolved against two different directories unless the script
    absolutises it — and the honest case fails closed with a *misleading* reason
    (``could not fetch``, for a tag that is present).  Fail-closed is not the
    same as correct: an adopter told the tag could not be fetched will go looking
    at the wrong thing.
    """
    r = lab.verify("--signers", lab.good_roster, ".", "v0.3.0", cwd=lab.candidate)
    assert r.returncode == PROVENANCED, f"{r.stdout}{r.stderr}"
    assert "v0.3.0" in r.stdout


def test_verification_that_could_not_run_does_not_blame_the_roster(
        lab: Lab, tmp_path: Path):
    """P5, claim <= evidence, at the signature step.

    Any non-zero exit from ``git verify-tag`` used to be reported as *"the
    signature ... did not verify against the trusted roster"* — including
    failures where **no verification was performed at all**.  Measured
    2026-08-03, git 2.53.0: an unwritable ``TMPDIR`` yields ``error: could not
    create temporary file`` and a broken ``ssh-keygen`` yields its own loader
    error, neither of which is a signature verdict.

    The falsifier is not a hypothetical: a stub ``ssh-keygen`` that fails without
    reaching a verdict is portable and deterministic, where the ``TMPDIR`` route
    depends on whether the platform's ``mktemp -d`` honours ``TMPDIR`` (macOS
    does not; GNU does).
    """
    stub_dir = tmp_path / "broken-toolchain"
    stub_dir.mkdir()
    stub = stub_dir / "ssh-keygen"
    stub.write_text(
        "#!/usr/bin/env bash\n"
        'echo "ssh-keygen: /usr/lib/libcrypto.dylib: version mismatch" >&2\n'
        "exit 1\n"
    )
    stub.chmod(0o755)
    r = lab.verify("--signers", lab.good_roster, lab.candidate, "v0.3.0",
                   env_extra={"PATH": f"{stub_dir}:{lab.env['PATH']}"})
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "COULD NOT BE PERFORMED" in r.stderr, r.stderr
    assert "did not verify against the trusted roster" not in r.stderr, \
        "a failure where NOTHING was checked was reported as a roster failure"


def test_signature_failure_still_names_the_roster(lab: Lab):
    """The other side of the split above: when a verdict *was* reached, the
    stronger claim must still be made.  A fix that weakened every refusal to
    "could not be performed" would satisfy the node above and say less than the
    evidence supports — which is the same defect from the other direction."""
    r = lab.verify("--signers", lab.wrong_roster, lab.candidate, "v0.3.0")
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "did not verify against the trusted roster" in r.stderr, r.stderr
    assert "COULD NOT BE PERFORMED" not in r.stderr


def test_no_git_describe_on_the_provenance_path():
    """``git describe`` resolves a name FROM a commit — the shape that answered a
    question nobody asked.  It must not appear in the script at all.

    Scoped to ``verify-ref.sh`` because that is the provenance path;
    ``acceptance.sh`` still uses ``git describe`` to compute an OCI *label* for a
    repository it owns, which decides nothing.
    """
    assert "git describe" not in SCRIPT.read_text()


# ================================================================== Chunk B
def test_provenance_mode_requires_a_roster(lab: Lab):
    """B1.  No ``--signers`` and no ``CAIRN_ALLOWED_SIGNERS`` must refuse, not
    fall back to anything."""
    r = lab.verify(lab.candidate, "v0.3.0")
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "trusted roster" in r.stderr


def test_roster_may_arrive_by_environment(lab: Lab):
    """B1's second accepted channel, so the refusal above is about ABSENCE."""
    r = lab.verify(lab.candidate, "v0.3.0",
                   env_extra={"CAIRN_ALLOWED_SIGNERS": str(lab.good_roster)})
    assert r.returncode == PROVENANCED, f"{r.stdout}{r.stderr}"


def test_missing_roster_path_refused(lab: Lab, tmp_path: Path):
    r = lab.verify("--signers", tmp_path / "nope", lab.candidate, "v0.3.0")
    assert r.returncode == REFUSED
    assert "not found" in r.stderr


def test_empty_roster_refused(lab: Lab, tmp_path: Path):
    empty = tmp_path / "empty-roster"
    empty.write_text("")
    r = lab.verify("--signers", empty, lab.candidate, "v0.3.0")
    assert r.returncode == REFUSED
    assert "no principals" in r.stderr


def test_keyless_roster_refused(lab: Lab, tmp_path: Path):
    """B6's second half, and the ``$CAIRN_KEY``-unset copy-paste failure: the
    documented step 2 is ``printf '%s %s\\n' "$CAIRN_SIGNER" "$CAIRN_KEY"``, so an
    unset key writes a principal and nothing else.  That must land HERE, on a
    refusal that names the cause, not on an opaque signature failure."""
    keyless = tmp_path / "keyless-roster"
    keyless.write_text(f"{GENUINE_PRINCIPAL} \n")
    r = lab.verify("--signers", keyless, lab.candidate, "v0.3.0")
    assert r.returncode == REFUSED
    assert "no key" in r.stderr


def test_roster_that_is_a_directory_refused(lab: Lab, tmp_path: Path):
    d = tmp_path / "roster-dir"
    d.mkdir()
    r = lab.verify("--signers", d, lab.candidate, "v0.3.0")
    assert r.returncode == REFUSED
    assert "directory" in r.stderr


def test_roster_inside_the_candidate_refused(lab: Lab, tmp_path: Path):
    """B2.  A roster that lives in the thing being verified cannot authenticate
    the thing being verified."""
    cand = tmp_path / "cand-with-roster"
    shutil.copytree(lab.candidate, cand)
    inside = cand / "release-signers"
    inside.write_text(lab.good_roster.read_text())
    r = lab.verify("--signers", inside, cand, "v0.3.0")
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "inside the candidate tree" in r.stderr


def test_roster_symlinked_into_the_candidate_refused(lab: Lab, tmp_path: Path):
    """B2's symlink half: containment resolves symlinks BEFORE deciding."""
    cand = tmp_path / "cand-symlink"
    shutil.copytree(lab.candidate, cand)
    inside = cand / "release-signers"
    inside.write_text(lab.good_roster.read_text())
    link = tmp_path / "outside-looking-roster"
    link.symlink_to(inside)
    r = lab.verify("--signers", link, cand, "v0.3.0")
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "inside the candidate tree" in r.stderr


def test_self_consistent_attacker_pair_refused(lab: Lab, tmp_path: Path):
    """B5, the [IDN1] boundary test.  An attacker key, an attacker-committed
    roster naming the *genuine* principal string, and the attacker's own
    ``.git/config`` pointing git at it: internally consistent, and signed.  The
    unsigned-tag and unrostered-key tests do not reach this question at all —
    only this one asks whether the candidate can bootstrap its own trust."""
    cand = lab.repo("attacker-cand", signing_key=lab.attacker)
    lab.commit(cand, "attacker")
    inside = cand / "allowed_signers"
    inside.write_text(f"{GENUINE_PRINCIPAL} {_pub(lab.attacker)}\n")
    lab.git(cand, "config", "gpg.ssh.allowedSignersFile", str(inside))
    lab.git(cand, "add", "allowed_signers")
    lab.git(cand, "commit", "-q", "-m", "self-certify")
    lab.sign_tag(cand, "v9.9.9")

    # The adopter's OWN roster (genuine key) is the only thing consulted.
    r = lab.verify("--signers", lab.good_roster, cand, "v9.9.9")
    assert r.returncode == REFUSED, f"self-certifying candidate accepted: {r.stdout}{r.stderr}"
    assert "did not verify" in r.stderr


def test_comma_separated_principals_are_parsed_and_counted(lab: Lab, tmp_path: Path):
    """B6's first half — the parsing defect the sibling surface found at
    ``0c6d9de``.  ``a@x,b@y <keytype> <key>`` is ONE line naming TWO principals;
    a counter that splits on whitespace alone reports one and the hygiene warning
    never fires."""
    multi = tmp_path / "comma-roster"
    multi.write_text(f"{GENUINE_PRINCIPAL},second@example.org {_pub(lab.maint)}\n")
    r = lab.verify("--signers", multi, lab.candidate, "v0.3.0")
    assert r.returncode == PROVENANCED, f"{r.stdout}{r.stderr}"
    assert "names 2 principals" in r.stderr, r.stderr


def test_toolchain_absence_refuses_rather_than_degrades(lab: Lab, tmp_path: Path):
    """B3.  With ``ssh-keygen`` removed from PATH the script must REFUSE, not
    fall through to an unverified accept."""
    stub_path = tmp_path / "empty-path"
    stub_path.mkdir()
    # Keep bash and git reachable, drop everything else: the refusal must name
    # ssh-keygen, and must arrive before any verification is attempted.
    for tool in ("bash", "git"):
        (stub_path / tool).symlink_to(shutil.which(tool))
    r = lab.verify("--signers", lab.good_roster, lab.candidate, "v0.3.0",
                   env_extra={"PATH": str(stub_path)})
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "ssh-keygen" in r.stderr


def test_missing_git_refuses_naming_git_not_the_repository(lab: Lab, tmp_path: Path):
    """B3's other half, and the reason the check had to move.

    ``command -v git || refuse`` sat inside provenance mode, *after* the
    unconditional ``git -C "$REPO" rev-parse --git-dir`` probe at the top had
    already run git.  With git off PATH that probe failed for the wrong reason
    and the script answered ``not a git repository: <a valid repository>`` with
    exit 2 — a usage error, for a repository that is perfectly valid.  The
    documented refusal was unreachable code.

    Asserted on the REASON and on the exit code: exit 1 alone would be satisfied
    by any refusal, and exit 2 is what the defect produced.
    """
    stub_path = tmp_path / "no-git-path"
    stub_path.mkdir()
    # git is the ONLY thing missing: ssh-keygen stays reachable, so a refusal
    # naming ssh-keygen would mean the node measured the wrong absence.
    for tool in ("bash", "ssh-keygen"):
        (stub_path / tool).symlink_to(shutil.which(tool))
    r = lab.verify("--signers", lab.good_roster, lab.candidate, "v0.3.0",
                   env_extra={"PATH": str(stub_path)})
    assert r.returncode == REFUSED, \
        f"expected the documented refusal (1), got {r.returncode}: {r.stdout}{r.stderr}"
    assert "git is not on PATH" in r.stderr, r.stderr
    assert "not a git repository" not in r.stderr, \
        "a missing toolchain was misdiagnosed as a bad argument"


# ================================================================== Chunk C
def test_bare_invocation_is_provenance_mode_and_refuses_head(lab: Lab):
    """C1.  ``verify-ref.sh <repo>`` used to mean "HEAD, and call it approved".
    It now means "provenance mode, and HEAD is not a signed release tag"."""
    r = lab.verify("--signers", lab.good_roster, lab.candidate)
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "HEAD" in r.stderr


def test_unprovenanced_and_provenanced_differ_by_exit_code_alone(lab: Lab):
    """C3.  A caller must be able to discriminate without matching message
    text."""
    provenanced = lab.verify("--signers", lab.good_roster, lab.candidate, "v0.3.0")
    pinned = lab.verify("--unprovenanced", lab.candidate)
    assert provenanced.returncode == PROVENANCED
    assert pinned.returncode == NOT_PROVENANCED
    assert provenanced.returncode != pinned.returncode


def test_unprovenanced_output_says_no_signature_was_checked(lab: Lab):
    """C2.  Claim <= evidence: the label must state what was NOT done."""
    r = lab.verify("--unprovenanced", lab.candidate)
    assert r.returncode == NOT_PROVENANCED, f"{r.stdout}{r.stderr}"
    assert "NOT PROVENANCED" in r.stdout
    assert "no signature checked" in r.stdout
    assert "release" not in r.stdout.lower()


def test_usage_error_exits_two(lab: Lab, tmp_path: Path):
    r = lab.verify("--signers", lab.good_roster, tmp_path / "not-a-repo", "v0.3.0")
    assert r.returncode == USAGE, f"{r.stdout}{r.stderr}"


def test_maintainer_approved_appears_nowhere_under_container(lab: Lab):
    """C6.  The phrase is deleted from the tool surface.  The walk is scoped to
    ``bootstrap/container/`` **deliberately**: the phrase legitimately survives in
    ``CHANGELOG.md`` and in the archived deliberation record, which the
    append-only rule forbids rewriting."""
    scanned = sorted(p for p in CONTAINER_DIR.rglob("*") if p.is_file())
    assert scanned, "the scan found no files — the scope constant is wrong"
    assert all(p.name != "CHANGELOG.md" for p in scanned), \
        "this check must not reach append-only history"
    offenders = [
        str(p.relative_to(REPO_ROOT))
        for p in scanned
        if "aintainer-approved" in p.read_text(errors="replace")
    ]
    assert offenders == [], f"retired claim still present: {offenders}"


def test_multi_tag_reports_only_the_tag_asked_about(lab: Lab, tmp_path: Path):
    """C7.  Three tags on one commit; asking about X must never print Y.

    Part B class table row: *several tags on one commit*.
    """
    cand = lab.repo("multi", signing_key=lab.maint)
    lab.commit(cand, "one-commit")
    lab.sign_tag(cand, "v1.0.0")
    lab.sign_tag(cand, "v1.0.1")
    lab.sign_tag(cand, "v1.0.2")
    r = lab.verify("--signers", lab.good_roster, cand, "v1.0.1")
    assert r.returncode == PROVENANCED, f"{r.stdout}{r.stderr}"
    assert "v1.0.1" in r.stdout
    assert "v1.0.0" not in r.stdout + r.stderr
    assert "v1.0.2" not in r.stdout + r.stderr


def test_slash_namespaced_tag_name_binds_on_the_full_name(lab: Lab):
    """Edge case: the comparison is on the full tag name, not a basename, so
    ``release/v0.7.0`` is not satisfied by a tag named ``v0.7.0``."""
    cand = lab.repo("namespaced", signing_key=lab.maint)
    lab.commit(cand, "ns")
    lab.sign_tag(cand, "release/v0.7.0")
    ok = lab.verify("--signers", lab.good_roster, cand, "release/v0.7.0")
    assert ok.returncode == PROVENANCED, f"{ok.stdout}{ok.stderr}"


def test_refspec_metacharacter_fails_closed(lab: Lab):
    """Edge case: ``REF='*'`` produces a VALID refspec and fetches every tag.
    It must then fail closed at the resolve step rather than report on whichever
    tag happened to land."""
    r = lab.verify("--signers", lab.good_roster, lab.candidate, "*")
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "PROVENANCED" not in r.stdout


# ------------------------------------------------- the Part B class table sweep
#
# One node per row, and each node NAMES its row.  Rows whose node lands in an
# earlier chunk are mapped to that node rather than given a second one.
CLASS_TABLE_ROWS = {
    "annotated tag, signed, key on the trusted roster":
        "test_honest_signed_tag_is_provenanced",
    "annotated tag, signed, key not on the trusted roster":
        "test_honest_tag_wrong_roster_is_refused",
    "annotated tag, unsigned":
        "test_row_unsigned_annotated_tag_refused",
    "tag ref whose object is an annotated tag object signed under a different name":
        "test_substitution_attack_refused_naming_both_names",
    "tag ref resolving to a non-tag object (a commit, a tree)":
        "test_resolver_names_the_non_tag_object_cause",
    "tag ref resolving to an unsigned tag object, including one wrapping a signed tag object":
        "test_nested_unsigned_wrap_refuses_at_the_signature_half",
    "several tags on one commit":
        "test_multi_tag_reports_only_the_tag_asked_about",
    "full 40-hex commit SHA":
        "test_row_full_sha_is_an_integrity_pin_only",
    "abbreviated SHA":
        "test_row_abbreviated_sha_refused_always",
    "HEAD":
        "test_row_head_refused_in_provenance_mode_pinned_under_unprovenanced",
    "branch ref (any spelling)":
        "test_row_mutable_branch_refused_naming_the_reason",
    "dirty/untracked build surface":
        "test_row_dirty_build_surface_refused_naming_the_reason",
}


def test_every_class_table_row_has_exactly_one_owning_node():
    """C5's coverage assertion: every row of the proposal's Part B class table
    has a test, each test names its row, and no row is claimed twice."""
    owners = list(CLASS_TABLE_ROWS.values())
    assert len(owners) == len(set(owners)), \
        f"a node claims two rows: {sorted({o for o in owners if owners.count(o) > 1})}"
    module = sys.modules[__name__]
    missing = [name for name in owners if not callable(getattr(module, name, None))]
    assert missing == [], f"class-table rows name nodes that do not exist: {missing}"


def test_row_unsigned_annotated_tag_refused(lab: Lab):
    """Part B class table row: *annotated tag, unsigned*.  This is what
    ``v0.3.0`` is in the real repository."""
    r = lab.verify("--signers", lab.good_roster, lab.candidate, "unsigned")
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "carries NO SIGNATURE" in r.stderr
    assert "did not verify against the trusted roster" not in r.stderr, \
        ("an unsigned tag must not be reported as a roster failure — git "
         "compared nothing against the roster, so naming it points the "
         "adopter at a file that is not the problem")


def test_row_full_sha_is_an_integrity_pin_only(lab: Lab):
    """Part B class table row: *full 40-hex commit SHA* — accepted only under
    ``--unprovenanced``, and only as an integrity pin."""
    head = lab.git(lab.candidate, "rev-parse", "HEAD").stdout.strip()
    pinned = lab.verify("--unprovenanced", lab.candidate, head)
    assert pinned.returncode == NOT_PROVENANCED, f"{pinned.stdout}{pinned.stderr}"
    assert head in pinned.stdout
    refused = lab.verify("--signers", lab.good_roster, lab.candidate, head)
    assert refused.returncode == REFUSED, "a bare SHA is not a signed release tag"


def test_row_abbreviated_sha_refused_always(lab: Lab):
    """Part B class table row: *abbreviated SHA* — refused in BOTH modes.  A
    4-character prefix used to be accepted."""
    short = lab.git(lab.candidate, "rev-parse", "--short", "HEAD").stdout.strip()
    pinned = lab.verify("--unprovenanced", lab.candidate, short)
    assert pinned.returncode == REFUSED, f"{pinned.stdout}{pinned.stderr}"
    assert "abbreviated" in pinned.stderr
    prov = lab.verify("--signers", lab.good_roster, lab.candidate, short)
    assert prov.returncode == REFUSED


def test_row_head_refused_in_provenance_mode_pinned_under_unprovenanced(lab: Lab):
    """Part B class table row: *HEAD*."""
    prov = lab.verify("--signers", lab.good_roster, lab.candidate, "HEAD")
    assert prov.returncode == REFUSED, f"{prov.stdout}{prov.stderr}"
    pinned = lab.verify("--unprovenanced", lab.candidate, "HEAD")
    assert pinned.returncode == NOT_PROVENANCED, f"{pinned.stdout}{pinned.stderr}"


def test_row_mutable_branch_refused_naming_the_reason(lab: Lab):
    """Part B class table row: *branch ref (any spelling)* — the Codex S5
    regression pin, asserted on its REASON so it cannot be satisfied by the
    provenance-mode refusal."""
    for spelling in ("master", "heads/master", "refs/heads/master"):
        r = lab.verify("--unprovenanced", lab.candidate, spelling)
        assert r.returncode == REFUSED, f"{spelling}: {r.stdout}{r.stderr}"
        assert "mutable branch" in r.stderr, f"{spelling}: {r.stderr}"


def test_row_dirty_build_surface_refused_naming_the_reason(lab: Lab, tmp_path: Path):
    """Part B class table row: *dirty/untracked build surface* — the cross-phase
    F#2 regression pin, asserted on its REASON."""
    dr = _build_surface_repo(lab, tmp_path / "dirty-probe")
    clean = lab.verify("--unprovenanced", dr)
    assert clean.returncode == NOT_PROVENANCED, f"{clean.stdout}{clean.stderr}"

    (dr / "bootstrap" / "scaffold.py").write_text("tampered\n")
    tracked = lab.verify("--unprovenanced", dr)
    assert tracked.returncode == REFUSED, f"{tracked.stdout}{tracked.stderr}"
    assert "uncommitted or untracked" in tracked.stderr

    lab.git(dr, "checkout", "--", "bootstrap/scaffold.py")
    (dr / "bootstrap" / "_scaffold" / "injected.py").write_text("evil\n")
    untracked = lab.verify("--unprovenanced", dr)
    assert untracked.returncode == REFUSED, f"{untracked.stdout}{untracked.stderr}"
    assert "uncommitted or untracked" in untracked.stderr


def _build_surface_repo(lab: Lab, path: Path) -> Path:
    """A repository shaped like the recipe's COPY set, so the build-surface
    pathspecs match something (the same fixture ``acceptance.sh`` builds)."""
    repo = path
    repo.mkdir(parents=True, exist_ok=True)
    lab.git(repo, "init", "-q", "-b", "master")
    lab.git(repo, "config", "user.email", GENUINE_PRINCIPAL)
    lab.git(repo, "config", "user.name", "lab")
    (repo / "bootstrap" / "_scaffold").mkdir(parents=True, exist_ok=True)
    (repo / "templates").mkdir(parents=True, exist_ok=True)
    (repo / "bootstrap" / "scaffold.py").write_text("x\n")
    (repo / "bootstrap" / "_scaffold" / "__init__.py").write_text("y\n")
    (repo / "templates" / ".keep").write_text("")
    (repo / "CITATION.cff").write_text('version: "0.0.0"\n')
    lab.git(repo, "add", "-A")
    lab.git(repo, "commit", "-q", "-m", "base")
    return repo


# ========================================== the mutation ledger, run in-suite
#
# "Every test shown non-vacuous by mutation": delete the control, confirm the
# test fails, restore the source byte-identical.  Doing it HERE rather than only
# in a commit body means the ledger is re-run on every suite run.
MUTATIONS = {
    "name-binding": (
        r'\[ "\$SIGNED_NAME" = "\$TAGNAME" \] \|\| refuse \\\n.*\n',
        "",
    ),
    "tag-object-resolver": (
        r'"refs/tags/\$TAGNAME\^\{tag\}"',
        '"refs/tags/$TAGNAME"',
    ),
    "roster-containment": (
        r'    "\$cand_canon"\|"\$cand_canon"/\*\)\n',
        '    "@@never-matches@@")\n',
    ),
    # Verification moved back INSIDE the candidate — the exact shape A4 forbids,
    # and the perturbation that makes A7's witness assertion falsifiable.
    "workspace-pinned-verification": (
        r'VERIFY_OUT="\$\(wsgit -C "\$WS" \\\n(?:  -c [^\n]*\n)+  verify-tag "\$OBJ" 2>&1\)"\n',
        'VERIFY_OUT="$(git -C "$REPO" verify-tag "$TAGNAME" 2>&1)"\n',
    ),
    # The candidate path left relative, so the fetch resolves it against the
    # temporary workspace instead of against the caller's cwd.
    "candidate-abspath": (
        r'REPO="\$\(cd -P "\$REPO" 2>/dev/null && pwd -P\)" \|\| \\\n  refuse [^\n]*\n',
        "",
    ),
    # The two verification-failure classes collapsed back into one claim, so a
    # failure where NOTHING was checked is reported as a roster failure.
    "verify-failure-classification": (
        r'VERDICT_REACHED=0\nNO_SIGNATURE=0\ncase "\$VERIFY_OUT" in\n(?:  \*[^\n]*\n)+esac\n'
        r'if \[ "\$VERIFY_RC" -ne 0 \] && \[ "\$NO_SIGNATURE" -eq 1 \]; then\n[^\n]*\nfi\n'
        r'if \[ "\$VERIFY_RC" -ne 0 \] && \[ "\$VERDICT_REACHED" -eq 1 \]; then\n[^\n]*\nfi\n'
        r'if \[ "\$VERIFY_RC" -ne 0 \]; then\n[^\n]*\nfi\n',
        '[ "$VERIFY_RC" -eq 0 ] || refuse '
        '"the signature on tag \'$TAGNAME\' (object $OBJ) did not verify '
        'against the trusted roster ($SIGNERS)"\n',
    ),
    # The toolchain check put back where it was dead code — after the first git
    # invocation rather than before it.
    "toolchain-git-precedence": (
        r'command -v git >/dev/null 2>&1 \|\| refuse "git is not on PATH[^\n]*\n',
        "",
    ),
}


def _mutant(tmp_path: Path, which: str) -> Path:
    """Write a copy of the script with ONE named control deleted.  The
    substitution is asserted to have changed the text, so a rename upstream
    cannot silently produce a no-op mutant that keeps the ledger green."""
    pattern, replacement = MUTATIONS[which]
    source = SCRIPT.read_text()
    mutated, n = re.subn(pattern, replacement, source, count=1)
    assert n == 1, f"mutation '{which}' matched nothing — the control was renamed or removed"
    assert mutated != source
    out = tmp_path / f"verify-ref.{which}.sh"
    out.write_text(mutated)
    out.chmod(0o755)
    return out


def _run_mutant(lab: Lab, script: Path, *args: str, env_extra=None,
                cwd: Path | None = None) -> subprocess.CompletedProcess:
    env = dict(lab.env)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        ["bash", str(script), *[str(a) for a in args]],
        capture_output=True, text=True, env=env,
        cwd=None if cwd is None else str(cwd),
    )


def test_mutation_deleting_the_name_binding_lets_the_substitution_through(
        lab: Lab, mirror: Path, tmp_path: Path):
    """The important ledger line.  With the name binding removed, the
    substitution attack PASSES — which is what makes the negative test
    discriminating rather than decorative."""
    mutant = _mutant(tmp_path, "name-binding")
    r = _run_mutant(lab, mutant, "--signers", lab.good_roster, mirror, "v0.4.0")
    assert r.returncode == PROVENANCED, \
        f"the mutant refused anyway — the name binding is not the control under test: {r.stderr}"
    assert SCRIPT.read_text() != mutant.read_text(), "the mutant must live outside the repository"


def test_mutation_dropping_the_tag_peel_breaks_the_resolver_refusal(
        lab: Lab, tmp_path: Path):
    """Delete ``^{tag}`` and a ref pointing straight at a commit resolves — so
    the non-tag-object refusal stops firing."""
    mutant = _mutant(tmp_path, "tag-object-resolver")
    r = _run_mutant(lab, mutant, "--signers", lab.good_roster, lab.candidate, "lw")
    assert "NON-TAG object" not in r.stderr, \
        "the resolver refusal survived its own mutation — it is not the control under test"


def test_mutation_deleting_the_containment_check_admits_an_inside_roster(
        lab: Lab, tmp_path: Path):
    """Delete the containment comparison and a roster committed INSIDE the
    candidate is accepted — the circular-trust defect, restored on purpose."""
    cand = tmp_path / "cand-inside"
    shutil.copytree(lab.candidate, cand)
    inside = cand / "release-signers"
    inside.write_text(lab.good_roster.read_text())
    mutant = _mutant(tmp_path, "roster-containment")
    r = _run_mutant(lab, mutant, "--signers", inside, cand, "v0.3.0")
    assert r.returncode == PROVENANCED, \
        f"the mutant refused anyway — containment is not the control under test: {r.stderr}"


def test_mutation_verifying_inside_the_candidate_runs_the_forger(
        lab: Lab, tmp_path: Path):
    """A7's non-vacuity, demonstrated rather than asserted.

    Replace the pinned workspace verification with ``git -C "$REPO" verify-tag
    "$TAGNAME"`` — verification run *inside the candidate*, which is the exact
    defect A4/A7 exist to forbid — and the hostile candidate's own configured
    verifier EXECUTES: the witness appears, the forged ``Good "git" signature``
    is believed, and the mutant reports PROVENANCED under the genuine
    maintainer's principal over a tag signed by the attacker.

    Without this node A7's ``assert not witness.exists()`` could not fail: the
    fixture it used to run against was an *unsigned* tag, and git spawns no
    verifier program when there is no signature, so the witness stayed absent
    however the verification was wired.
    """
    cand, witness = _hostile_candidate(lab, tmp_path)
    mutant = _mutant(tmp_path, "workspace-pinned-verification")
    r = _run_mutant(lab, mutant, "--signers", lab.good_roster, cand, HOSTILE_TAG)
    assert witness.exists(), \
        "the forger did not run against the mutant — the A7 fixture cannot discriminate"
    assert r.returncode == PROVENANCED, \
        f"the mutant refused anyway — the pinned workspace is not the control under test: {r.stderr}"
    assert "SHA256:forged" in r.stdout + r.stderr or GENUINE_PRINCIPAL in r.stdout, \
        f"the forged verdict did not reach the report: {r.stdout}{r.stderr}"


def test_mutation_dropping_the_candidate_abspath_breaks_a_relative_path(
        lab: Lab, tmp_path: Path):
    """Delete the candidate-path absolutisation and a relative candidate is
    resolved against the temporary workspace, so the honest case refuses with a
    misleading ``could not fetch``."""
    mutant = _mutant(tmp_path, "candidate-abspath")
    r = _run_mutant(lab, mutant, "--signers", lab.good_roster, ".", "v0.3.0",
                    cwd=lab.candidate)
    assert r.returncode == REFUSED, \
        f"the mutant accepted anyway — absolutisation is not the control under test: {r.stdout}"
    assert "could not fetch" in r.stderr, r.stderr


def test_mutation_collapsing_the_verify_classes_blames_the_roster(
        lab: Lab, tmp_path: Path):
    """Collapse the two verification-failure classes back into one claim and a
    failure where NOTHING was checked is reported as a roster failure — which is
    what the P5 node above must be able to catch."""
    stub_dir = tmp_path / "broken-toolchain-mutant"
    stub_dir.mkdir()
    stub = stub_dir / "ssh-keygen"
    stub.write_text(
        "#!/usr/bin/env bash\n"
        'echo "ssh-keygen: /usr/lib/libcrypto.dylib: version mismatch" >&2\n'
        "exit 1\n"
    )
    stub.chmod(0o755)
    mutant = _mutant(tmp_path, "verify-failure-classification")
    r = _run_mutant(lab, mutant, "--signers", lab.good_roster, lab.candidate,
                    "v0.3.0", env_extra={"PATH": f"{stub_dir}:{lab.env['PATH']}"})
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "did not verify against the trusted roster" in r.stderr, \
        "the mutant did not restore the over-claim — the classification is not the control under test"


def test_mutation_collapsing_the_verify_classes_blames_the_roster_for_an_unsigned_tag(
        lab: Lab, tmp_path: Path):
    """The *third* class, kept falsifiable on its own.

    ``no signature found`` IS a verdict — git looked and established there is
    nothing to check — so it survives the ``VERDICT_REACHED`` gate and, before
    the split, was reported as a roster failure. But nothing was compared
    against the roster, because no signature existed. Collapsing the classes
    restores exactly that over-claim on an honest, unsigned tag, which is a
    different input from the no-verdict case the sibling node drives.
    """
    mutant = _mutant(tmp_path, "verify-failure-classification")
    r = _run_mutant(lab, mutant, "--signers", lab.good_roster, lab.candidate,
                    "unsigned")
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"
    assert "did not verify against the trusted roster" in r.stderr, \
        "the mutant did not restore the over-claim on an unsigned tag"
    assert "carries NO SIGNATURE" not in r.stderr, \
        "the mutant still distinguishes the classes — it is not the control under test"


def test_mutation_moving_the_git_check_back_misdiagnoses_a_missing_git(
        lab: Lab, tmp_path: Path):
    """Delete the relocated toolchain check and a missing git is once again
    reported as ``not a git repository`` with exit 2 — the misdiagnosis, restored
    on purpose."""
    stub_path = tmp_path / "no-git-path-mutant"
    stub_path.mkdir()
    for tool in ("bash", "ssh-keygen"):
        (stub_path / tool).symlink_to(shutil.which(tool))
    mutant = _mutant(tmp_path, "toolchain-git-precedence")
    r = _run_mutant(lab, mutant, "--signers", lab.good_roster, lab.candidate,
                    "v0.3.0", env_extra={"PATH": str(stub_path)})
    assert r.returncode == USAGE, \
        f"the mutant refused correctly — the check's PLACEMENT is not under test: {r.stdout}{r.stderr}"
    assert "not a git repository" in r.stderr, r.stderr


# ============================================ Chunk D — the shell-harness pins
def _extract_marked(text: str, marker: str) -> str:
    m = re.search(
        rf"^# --- BEGIN {re.escape(marker)} ---\n(.*?)^# --- END {re.escape(marker)} ---$",
        text, re.S | re.M,
    )
    assert m, f"acceptance.sh no longer carries the '{marker}' block"
    return m.group(1)


def _replay_pin(lab: Lab, pin: str, script_dir: Path, tmp_path: Path,
                repo: Path, dirty_probe: Path) -> subprocess.CompletedProcess:
    """Run ONE of acceptance.sh's negative pins, verbatim, against a chosen
    ``verify-ref.sh``.  The pin text and its helper are extracted from
    acceptance.sh itself, so a pin that is weakened there is weakened here."""
    body = ACCEPTANCE.read_text()
    harness = tmp_path / f"replay-{pin}.sh"
    harness.write_text(
        "set -euo pipefail\n"
        f'SCRIPT_DIR="{script_dir}"\n'
        f'REPO="{repo}"\n'
        f'DR="{dirty_probe}"\n'
        'BRANCH="master"\n'
        "note() { :; }\n"
        "ok() { :; }\n"
        'fail() { printf "PIN-FAIL: %s\\n" "$*" >&2; exit 1; }\n'
        + _extract_marked(body, "PIN-HELPERS")
        + _extract_marked(body, f"PIN {pin}")
    )
    return subprocess.run(["bash", str(harness)], capture_output=True, text=True,
                          env=lab.env)


ACCEPTANCE_PIN_MUTATIONS = {
    "mutable-branch": (
        r'      refuse "\'\$REF\' resolves to a mutable branch.*\n',
        "      : ;;\n",
    ),
    "dirty-build-surface": (
        r'  if \[ -n "\$dirty" \]; then\n',
        "  if false; then\n",
    ),
}


@pytest.mark.parametrize("pin", sorted(ACCEPTANCE_PIN_MUTATIONS))
def test_acceptance_pin_passes_against_the_real_script(lab: Lab, pin: str, tmp_path: Path):
    """D4, the control half: the pin as it stands in ``acceptance.sh`` passes
    against the shipped script."""
    dr = _build_surface_repo(lab, tmp_path / "dr")
    r = _replay_pin(lab, pin, CONTAINER_DIR, tmp_path, lab.candidate, dr)
    assert r.returncode == 0, f"{r.stdout}{r.stderr}"


@pytest.mark.parametrize("pin", sorted(ACCEPTANCE_PIN_MUTATIONS))
def test_acceptance_pin_fails_against_a_stub_with_its_control_deleted(
        lab: Lab, pin: str, tmp_path: Path):
    """D4, the discriminating half.  Three of ``acceptance.sh``'s assertions used
    to pass on ANY refusal, so once provenance mode became the default they went
    green against a script with both controls deleted.  Each pin must now FAIL
    when its named control is removed.

    The stub lives in the scratch directory, never in the repository.
    """
    pattern, replacement = ACCEPTANCE_PIN_MUTATIONS[pin]
    source = SCRIPT.read_text()
    mutated, n = re.subn(pattern, replacement, source, count=1)
    assert n == 1, f"pin mutation '{pin}' matched nothing — the control was renamed"
    stub_dir = tmp_path / f"stub-{pin}"
    stub_dir.mkdir()
    stub = stub_dir / "verify-ref.sh"
    stub.write_text(mutated)
    stub.chmod(0o755)

    dr = _build_surface_repo(lab, tmp_path / "dr-stub")
    r = _replay_pin(lab, pin, stub_dir, tmp_path, lab.candidate, dr)
    assert r.returncode != 0, \
        f"pin '{pin}' passed against a stub with its control deleted: {r.stdout}{r.stderr}"
    assert "PIN-FAIL" in r.stderr, r.stderr


def test_provenance_path_is_exercised_without_acceptance_sh(lab: Lab):
    """D5, and the limit it mitigates.  ``acceptance.sh`` now runs permanently in
    ``--unprovenanced`` mode, so Cairn's container harness never smoke-checks the
    mode this scope added.  This node builds its own signed tag and roster and
    drives the provenance path end to end instead.

    RECORDED AS NOT ESTABLISHED: this mitigates; it does not restore end-to-end
    coverage of the provenance path *through the container recipe*.
    """
    assert "--unprovenanced" in ACCEPTANCE.read_text()
    r = lab.verify("--signers", lab.good_roster, lab.candidate, "v0.3.0")
    assert r.returncode == PROVENANCED, f"{r.stdout}{r.stderr}"


# ================== Chunk E — the document's own block, extracted and executed
BOOTSTRAP_BLOCK_RE = re.compile(
    r"<!-- cairn:bootstrap-block start -->\s*```sh\n(.*?)```\s*<!-- cairn:bootstrap-block end -->",
    re.S,
)


def _extract_bootstrap_block(markdown: str) -> str:
    m = BOOTSTRAP_BLOCK_RE.search(markdown)
    assert m, "bootstrap/PROVENANCE.md no longer publishes a marked bootstrap block"
    return m.group(1)


def _run_bootstrap_block(lab: Lab, block: str, tmp_path: Path, *,
                         tag: str, candidate: Path | str, roster: Path,
                         name: str = "block",
                         cwd: Path | None = None) -> subprocess.CompletedProcess:
    path = tmp_path / f"{name}.sh"
    path.write_text(block)
    return subprocess.run(
        ["bash", str(path)], capture_output=True, text=True,
        env={**lab.env, "CAIRN_TAG": tag, "CAIRN_CANDIDATE": str(candidate),
             "CAIRN_ROSTER": str(roster)},
        cwd=None if cwd is None else str(cwd),
    )


def test_documented_bootstrap_block_verifies_an_honest_tag(lab: Lab, tmp_path: Path):
    """E8.  The block that RUNS is the block the document PUBLISHES: a private
    copy could not detect that the document still tells adopters something
    unsafe."""
    block = _extract_bootstrap_block(PROVENANCE_MD.read_text())
    r = _run_bootstrap_block(lab, block, tmp_path, tag="v0.3.0",
                             candidate=lab.candidate, roster=lab.good_roster)
    assert r.returncode == 0, f"{r.stdout}{r.stderr}"
    assert "PROVENANCED" in r.stdout


def test_documented_bootstrap_block_refuses_the_substitution(lab: Lab, mirror: Path,
                                                             tmp_path: Path):
    block = _extract_bootstrap_block(PROVENANCE_MD.read_text())
    r = _run_bootstrap_block(lab, block, tmp_path, tag="v0.4.0",
                             candidate=mirror, roster=lab.good_roster)
    assert r.returncode == 1, f"{r.stdout}{r.stderr}"
    assert "REFUSED" in r.stderr
    assert "v0.3.0" in r.stderr


def test_documented_bootstrap_block_accepts_a_relative_candidate_path(
        lab: Lab, tmp_path: Path):
    """The document says ``$CAIRN_CANDIDATE`` is *"the clone URL, or the local
    path"*.  Its step 2 fetch runs ``git -C "$CAIRN_WS/verify"``, so a relative
    local path was resolved against the workspace and the honest case died on
    ``couldn't find remote ref`` — the same defect the script carried, published
    to adopters."""
    block = _extract_bootstrap_block(PROVENANCE_MD.read_text())
    r = _run_bootstrap_block(lab, block, tmp_path, tag="v0.3.0", candidate=".",
                             roster=lab.good_roster, name="relative-candidate",
                             cwd=lab.candidate)
    assert r.returncode == 0, f"{r.stdout}{r.stderr}"
    assert "PROVENANCED" in r.stdout


def test_documented_bootstrap_block_leaves_a_url_candidate_alone(
        lab: Lab, tmp_path: Path):
    """The other side of the same step: a URL must NOT be run through the
    local-path resolution, or the documented clone-URL form stops working.  The
    assertion is that the block reaches the *network*, not that it succeeds
    there — this node makes no network claim of its own."""
    block = _extract_bootstrap_block(PROVENANCE_MD.read_text())
    r = _run_bootstrap_block(lab, block, tmp_path, tag="v0.3.0",
                             candidate="https://example.invalid/cairn.git",
                             roster=lab.good_roster, name="url-candidate")
    assert r.returncode != 0
    assert "is not a directory" not in r.stderr, \
        "a URL was mistaken for a local path"


def test_documented_bootstrap_block_refuses_unset_inputs(lab: Lab, tmp_path: Path):
    """The block's step 0 is fail-closed: an adopter who pastes it without
    setting the three inputs gets a refusal, never a default candidate."""
    block = _extract_bootstrap_block(PROVENANCE_MD.read_text())
    path = tmp_path / "unset.sh"
    path.write_text(block)
    r = subprocess.run(["bash", str(path)], capture_output=True, text=True,
                       env={k: v for k, v in lab.env.items()
                            if not k.startswith("CAIRN_")})
    assert r.returncode != 0
    assert "CAIRN_TAG" in r.stderr


def test_mutating_the_documented_block_breaks_its_own_test(lab: Lab, mirror: Path,
                                                           tmp_path: Path):
    """E8's acceptance criterion, demonstrated rather than asserted: delete the
    name-binding step from a SCRATCH COPY of the document and the extracted block
    accepts the substitution attack.  That is what makes the two nodes above
    controls over the document's text, not decoration."""
    doc = PROVENANCE_MD.read_text()
    mutated, n = re.subn(
        r'\[ "\$CAIRN_SIGNED_NAME" = "\$CAIRN_TAG" \] \|\| \{.*?\n  rm -rf "\$CAIRN_WS"; exit 1; \}\n',
        "", doc, count=1, flags=re.S,
    )
    assert n == 1, "the document's name-binding step was renamed or removed"
    scratch = tmp_path / "PROVENANCE.mutated.md"
    scratch.write_text(mutated)

    block = _extract_bootstrap_block(scratch.read_text())
    r = _run_bootstrap_block(lab, block, tmp_path, tag="v0.4.0", candidate=mirror,
                             roster=lab.good_roster, name="mutated-block")
    assert r.returncode == 0, \
        f"the mutated block refused anyway — the name-binding step is not the control: {r.stderr}"


def test_two_candidates_publishing_the_same_tag_name(lab: Lab, tmp_path: Path):
    """E9.  Nothing persists between runs: the workspace is created and discarded
    per run, so a second run against a DIFFERENT candidate publishing the same
    tag name can never pass on the first run's cached object."""
    block = _extract_bootstrap_block(PROVENANCE_MD.read_text())

    first = lab.repo("same-name-a", signing_key=lab.maint)
    lab.commit(first, "candidate-a")
    obj_a = lab.sign_tag(first, "v9.9.8")

    second = tmp_path / "same-name-b"
    second.mkdir()
    lab.git(second, "init", "-q", "-b", "master")
    lab.git(second, "config", "user.email", GENUINE_PRINCIPAL)
    lab.git(second, "config", "user.name", "lab")
    lab.git(second, "config", "gpg.format", "ssh")
    lab.git(second, "config", "user.signingkey", str(lab.maint))
    lab.commit(second, "candidate-b")
    obj_b = lab.sign_tag(second, "v9.9.8")
    assert obj_a != obj_b

    run_a = _run_bootstrap_block(lab, block, tmp_path, tag="v9.9.8",
                                 candidate=first, roster=lab.good_roster, name="cand-a")
    assert run_a.returncode == 0, f"{run_a.stdout}{run_a.stderr}"
    assert obj_a in run_a.stdout

    run_b = _run_bootstrap_block(lab, block, tmp_path, tag="v9.9.8",
                                 candidate=second, roster=lab.good_roster, name="cand-b")
    assert obj_a not in run_b.stdout + run_b.stderr, \
        "the second run reported the FIRST candidate's object — state leaked between runs"
    assert run_b.returncode != 0 or obj_b in run_b.stdout


# --------------------------------------------------------------- E10, rotation
ROTATION_BOUNDARY = "20260101"
BEFORE_BOUNDARY = "2025-06-01T12:00:00Z"
AFTER_BOUNDARY = "2026-06-01T12:00:00Z"


@pytest.fixture()
def rotation(lab: Lab, tmp_path: Path):
    """A candidate carrying one tag dated before the retirement boundary and one
    dated after it, plus a roster retiring the key at that boundary."""
    repo = tmp_path / "rotation"
    repo.mkdir()
    lab.git(repo, "init", "-q", "-b", "master")
    lab.git(repo, "config", "user.email", GENUINE_PRINCIPAL)
    lab.git(repo, "config", "user.name", "lab")
    lab.git(repo, "config", "gpg.format", "ssh")
    lab.git(repo, "config", "user.signingkey", str(lab.maint))
    lab.commit(repo, "rotation-base")
    lab.sign_tag(repo, "dated-before", date=BEFORE_BOUNDARY)
    lab.sign_tag(repo, "dated-after", date=AFTER_BOUNDARY)
    retired = tmp_path / "roster-retired"
    retired.write_text(
        f'{GENUINE_PRINCIPAL} valid-before="{ROTATION_BOUNDARY}" {_pub(lab.maint)}\n')
    return repo, retired


def test_retired_key_refuses_a_tag_dated_after_retirement(lab: Lab, rotation):
    """E10.  A ``valid-before`` window must actually be enforced."""
    repo, retired = rotation
    r = lab.verify("--signers", retired, repo, "dated-after")
    assert r.returncode == REFUSED, f"{r.stdout}{r.stderr}"


def test_retired_key_still_verifies_a_tag_dated_before_retirement(lab: Lab, rotation):
    """E10, and the git-floor probe.  This node and the one above together
    establish, by BEHAVIOUR rather than by parsing a version string, that git
    judges the window against the **tagger timestamp inside the signed payload**
    and not against the current clock: 'now' is after both boundaries, so a git
    that judged against 'now' would refuse this one too, and the failure would
    surface here at execution rather than in an adopter's install.
    """
    repo, retired = rotation
    r = lab.verify("--signers", retired, repo, "dated-before")
    assert r.returncode == PROVENANCED, f"{r.stdout}{r.stderr}"


def test_backdated_tag_from_a_retired_key_still_verifies(lab: Lab, rotation, tmp_path):
    """E10's residual-pinning test (RA2).  The tagger timestamp is INSIDE the
    signed payload, so whoever holds a compromised key can set it and back-date a
    tag past a ``valid-before`` boundary.  This node exists so nobody later reads
    a validity window as revocation: **it asserts the attack succeeds.**"""
    repo, retired = rotation
    lab.sign_tag(repo, "backdated-forgery", date=BEFORE_BOUNDARY)
    r = lab.verify("--signers", retired, repo, "backdated-forgery")
    assert r.returncode == PROVENANCED, (
        "a back-dated tag from a retired key was refused — if git gained real "
        "revocation, bootstrap/PROVENANCE.md's 'hygiene, not revocation' "
        "sentence and residual RA2 both need revisiting"
    )


# ============================================ Chunk G — the Cairn-side tripwire
def _count_principals(roster_text: str) -> int:
    """Count principals in an ``allowed_signers`` file, splitting the first field
    on commas — the parsing defect found at ``0c6d9de``."""
    total = 0
    for line in roster_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        first = line.split()[0]
        total += len([p for p in first.split(",") if p])
    return total


def test_principal_counter_splits_on_commas():
    """G2's own non-vacuity demonstration: the counter must see a second
    principal however it is spelled, or the tripwire below cannot fire."""
    assert _count_principals("a@x ssh-ed25519 AAA\n") == 1
    assert _count_principals("a@x,b@y ssh-ed25519 AAA\n") == 2
    assert _count_principals("a@x ssh-ed25519 AAA\nb@y ssh-ed25519 BBB\n") == 2
    assert _count_principals("# comment\n\na@x ssh-ed25519 AAA\n") == 1


def test_cairn_roster_names_one_principal():
    """G2.  The genuinely mechanical half of residual RA1, on **Cairn's** side:
    Cairn's own internal gate roster names exactly one principal (`as_of
    2026-08-03`).  It fires in Cairn's suite, where Cairn will see it — unlike
    the adopter-facing warning in the script, which counts principals in a file
    the adopter typed and has no channel back here.

    When this fails, Cairn's signing authority has widened and the
    single-signer posture stated in the deliberation record needs re-deciding.
    """
    assert CAIRN_GATE_ROSTER.is_file(), f"{CAIRN_GATE_ROSTER} is missing"
    assert _count_principals(CAIRN_GATE_ROSTER.read_text()) == 1
