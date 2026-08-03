"""Pre-flight for the supervised gate re-anchor (``REANCHOR_RUNBOOK.md`` Phase 0).

Phase 0 is a **Maintainer-only** trust-root ceremony. The runbook states what to
verify; before this module, nothing verified it, and the gap was filled twice by a
disposable scratchpad script -- which returned a wrong answer on its second use,
and whose unsequenced handoff advanced ``refs/cairn/gate-anchor`` to a commit
containing no blessing. See the archived proposal
``dev/proposals/archive/2026-08-03-claude-gate-reanchor-preflight.md`` and its
plan for the three External Security Review rounds behind this design.

**This module decides nothing.** It computes, refuses, and reports. Every
repository-mutating step -- installing the manifest, committing it, advancing the
ref -- stays the Maintainer's act. There is no flag that turns a refusal into a
pass.

Read-only by construction, and structurally so: every git invocation goes through
:func:`_git`, which refuses any subcommand outside :data:`_READ_ONLY_GIT`. That is
the hook the read-only invariant test asserts against, rather than trusting a
before/after snapshot to notice (plan finding GPR4).

**Threat model** -- trusted-contributor, scoped to Cairn's own trust root,
single-maintainer, as of 2026-08-03, accepted by Maintainer Decision and amended
at the same. Candidate code in this repository is assumed non-adversarial. The
expiry tripwire is signature verification (:func:`check_signatures`), which
authenticates the **key holder** -- not the human, and not the process. Every
agent operating on this machine commits as the Maintainer and signs with the
Maintainer's key, so this detects a second *person*, not a second *process*.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

try:  # package import (pytest)
    from bootstrap.tests import _gate_manifest as G
    from bootstrap.tests import _gate_reanchor as R
except ImportError:  # script import (the anchored invocation)
    import _gate_manifest as G
    import _gate_reanchor as R

_REPO = Path(__file__).resolve().parents[2]

_ANCHOR_REF = "refs/cairn/gate-anchor"
_MANIFEST_REL = "bootstrap/tests/fixtures/gate_manifest.json"
_RUNBOOK_REL = "bootstrap/REANCHOR_RUNBOOK.md"
_ALLOWED_SIGNERS_REL = "dev/.cairn/allowed_signers"

#: The signing epoch (Maintainer-recorded, Decision amendment 2026-08-03).
#: Commits at or after this one must be signed by a pinned key; earlier commits
#: are grandfathered, because all 672 commits predating it are unsigned.
#: This constant lives in the checker's own bytes on purpose -- the authority
#: closure covers this file, so a candidate cannot advance the epoch to
#: grandfather its own unsigned commits without being caught.
_SIGNING_EPOCH = "a07fac88e6dcda08513cac28e6f1310999f1e577"

_CANONICAL_PY = (3, 13)

#: Evidence-artifact schema version. ``check`` refuses anything else.
EVIDENCE_SCHEMA = 1

#: Git subcommands this module is permitted to run. Anything else raises --
#: ``check`` must never be able to mutate the repository, and this is the
#: structural guarantee rather than a documented promise.
_READ_ONLY_GIT = frozenset({
    "rev-parse", "rev-list", "log", "show", "cat-file", "ls-files",
    "diff", "merge-base", "for-each-ref", "status",
    # `archive` reads objects and writes only to a caller-chosen path; callers
    # here always target a temp directory outside the repository. It mutates no
    # repository state, which is the property this allowlist encodes.
    "archive",
})

#: Config pinned on **every** git invocation, so the checker's reading of the
#: repository never depends on candidate-controlled `.git/config`. CR1 was one
#: instance of that class (the allowed-signers roster's *location*); its reviewer
#: flagged the class itself as unswept. `core.quotePath` is the sibling that
#: sweep found: it defaults to *true* and escapes non-ASCII paths in both
#: `ls-files --stage` and `status --porcelain`, so a frozen file named
#: `d/café.py` reads back as `"d/caf\303\251.py"` and never matches the glob --
#: a false refusal rather than a bypass, but the same failure shape. Pinning it
#: here closes the class for future call sites too, rather than one instance.
_PINNED_CONFIG: dict[str, str] = {"core.quotePath": "false"}

#: Index modes accepted for a frozen-surface member: regular file only.
#: 120000 is a symlink and 160000 a gitlink/submodule; both are refused, because
#: a symlink hashes through to its target and can pin bytes no committed blob
#: contains (security review SR5).
_REGULAR_MODES = frozenset({"100644", "100755"})


class PreflightError(RuntimeError):
    """Raised on a condition the checker must not paper over."""


@dataclass
class Finding:
    """One check result. ``refuse`` is fatal; ``review`` routes to the manual
    runbook; ``note`` is informational and never blocks."""
    code: str
    level: str          # "refuse" | "review" | "note"
    message: str

    @property
    def blocking(self) -> bool:
        return self.level in ("refuse", "review")


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    facts: dict = field(default_factory=dict)

    def add(self, code: str, level: str, message: str) -> None:
        self.findings.append(Finding(code, level, message))

    @property
    def blocked(self) -> bool:
        return any(f.blocking for f in self.findings)


# --------------------------------------------------------------------------
# git access -- read-only by construction
# --------------------------------------------------------------------------

def _git(*args: str, repo: Path = _REPO,
         config: dict[str, str] | None = None,
         want_bytes: bool = False) -> subprocess.CompletedProcess:
    """Run a **read-only** git subcommand. Refuses anything not allowlisted.

    This is the enforcement point for the read-only invariant: a future edit that
    tries to commit, checkout, or update a ref from inside the checker raises
    instead of running.

    ``config`` supplies ``-c key=value`` overrides ahead of the subcommand.
    Command-line ``-c`` outranks repository config, which is what lets a caller
    take a security-relevant setting **out of the candidate's hands** -- see
    :func:`check_signatures` and plan finding CR1.
    """
    if not args or args[0] not in _READ_ONLY_GIT:
        raise PreflightError(
            f"_gate_preflight may only run read-only git subcommands; "
            f"refused {(args[0] if args else '<none>')!r}")
    merged = {**_PINNED_CONFIG, **(config or {})}
    overrides: list[str] = []
    for key, value in merged.items():
        overrides += ["-c", f"{key}={value}"]
    return subprocess.run(["git", "-C", str(repo), *overrides, *args],
                          capture_output=True, text=not want_bytes, check=False)


def _resolve(ref: str, *, repo: Path = _REPO) -> str:
    p = _git("rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}",
             repo=repo)
    sha = (p.stdout or "").strip()
    if p.returncode != 0 or len(sha) != 40 or any(
            c not in "0123456789abcdef" for c in sha):
        raise PreflightError(
            f"ref does not resolve to a commit: {ref!r} "
            f"({(p.stderr or '').strip()})")
    return sha


def _blob_at(sha: str, rel: str, *, repo: Path = _REPO) -> bytes | None:
    """Read a blob from an immutable commit, as bytes.

    Routed through :func:`_git` rather than calling ``subprocess`` directly:
    an escape hatch here would quietly falsify the module's claim that *every*
    git invocation passes the read-only guard, which is the property the
    invariant test asserts.
    """
    p = _git("show", f"{sha}:{rel}", repo=repo, want_bytes=True)
    return p.stdout if p.returncode == 0 else None


def _sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


# --------------------------------------------------------------------------
# the preflight-authority closure (plan finding GPR1)
# --------------------------------------------------------------------------

def declared_authority_closure() -> list[str]:
    """Every artifact whose bytes decide **what may be blessed** or **what
    executes** at the next ceremony.

    The six Stage-B modules alone are not enough: after first use this checker
    decides what may be blessed, and the runbook holds the invocation deciding
    which bytes run. Neither is in that set, and ``REANCHOR_RUNBOOK.md`` and the
    allowed-signers file are not in ``_gate_manifest._frozen_files()`` **at all**,
    so the manifest cannot cover them. They are pinned here explicitly.
    """
    return [
        "bootstrap/tests/_gate_preflight.py",     # this checker
        "bootstrap/tests/_gate_manifest.py",      # its import closure, below
        "bootstrap/tests/_gate_reanchor.py",
        "bootstrap/tests/_gate_transition.py",
        "bootstrap/tests/_oracle_activation.py",
        "bootstrap/tests/_oracle.py",
        "bootstrap/tests/_oracle_trust.py",
        _RUNBOOK_REL,                             # canonical invocation source
        _ALLOWED_SIGNERS_REL,                     # pinned key set
    ]


def _imported_local_modules() -> set[str]:
    """Repo-relative paths of the ``bootstrap/tests`` modules this checker's own
    import graph actually reaches.

    Compared against the declared closure so a **new dependency** cannot slip in
    uncovered -- the "extra member" half of GPR1's satisfier. Walks this module's
    transitive module-valued globals rather than scanning ``sys.modules``, which
    under pytest also holds every ``conftest`` and ``test_*`` module and would
    report them as spurious extras.
    """
    import types  # noqa: PLC0415 -- local; not part of the authority closure

    seen: set[int] = set()
    found: set[str] = set()
    queue = [sys.modules[__name__]]
    while queue:
        mod = queue.pop()
        if id(mod) in seen:
            continue
        seen.add(id(mod))
        f = getattr(mod, "__file__", None)
        if f:
            try:
                rel = Path(f).resolve().relative_to(_REPO).as_posix()
            except (ValueError, OSError):
                rel = ""
            if rel.startswith("bootstrap/tests/") and rel.endswith(".py"):
                found.add(rel)
            elif rel:
                continue          # in-repo but outside the gate surface
            else:
                continue          # stdlib / site-packages -- not our concern
        for value in vars(mod).values():
            if isinstance(value, types.ModuleType):
                queue.append(value)
    return found


def check_authority_closure(anchor: str, report: Report, *,
                            repo: Path = _REPO) -> None:
    """Compare every closure member's working-tree bytes to the anchor's blob.

    Any member changed, missing, extra, symlinked, or absent from the index
    returns ``review`` -- non-zero, no bundle, routed to the manual exact-byte
    procedure. The old anchored checker must not be able to bless a candidate
    that changes its own successor or the next invocation.
    """
    declared = declared_authority_closure()
    index = _index_entries(repo=repo)

    for rel in declared:
        live = repo / rel
        if not live.is_file():
            report.add("CLOSURE", "review",
                       f"authority member missing from the worktree: {rel}")
            continue
        mode = index.get(rel)
        if mode is None:
            report.add("CLOSURE", "review",
                       f"authority member is not in the git index: {rel}")
            continue
        if mode not in _REGULAR_MODES:
            report.add("CLOSURE", "review",
                       f"authority member is not a regular blob (mode {mode}): "
                       f"{rel}")
            continue
        anchored = _blob_at(anchor, rel, repo=repo)
        if anchored is None:
            report.add("CLOSURE", "review",
                       f"authority member absent from the anchor -- first use "
                       f"requires the manual exact-byte bootstrap: {rel}")
            continue
        if _sha256_bytes(live.read_bytes()) != _sha256_bytes(anchored):
            report.add("CLOSURE", "review",
                       f"authority member differs from the anchor: {rel}")

    extra = sorted(_imported_local_modules() - set(declared))
    for rel in extra:
        report.add("CLOSURE", "review",
                   f"imported module is outside the declared authority "
                   f"closure: {rel}")

    report.facts["authority_closure"] = declared


# --------------------------------------------------------------------------
# index-validated frozen surface (security review SR5)
# --------------------------------------------------------------------------

def _index_entries(*, repo: Path = _REPO) -> dict[str, str]:
    """``{repo-relative path: index mode}`` for stage-0 entries."""
    p = _git("ls-files", "--stage", repo=repo)
    entries: dict[str, str] = {}
    for line in (p.stdout or "").splitlines():
        if not line.strip():
            continue
        meta, _, rel = line.partition("\t")
        parts = meta.split()
        if len(parts) != 3 or parts[2] != "0":
            continue                      # unmerged stage -- not a clean entry
        entries[rel] = parts[0]
    return entries


def check_frozen_surface(report: Report, *, repo: Path = _REPO) -> None:
    """Every discovered frozen path must be a stage-0 regular blob in the index.

    ``_frozen_files()`` discovers by filesystem glob and ``_sha256`` follows
    symlinks, so without this an **ignored** file gets hashed into the manifest
    while ``git ls-files --others --exclude-standard`` reports nothing, and a
    symlink pins its target's bytes. Both produce a manifest a fresh checkout
    cannot reproduce.
    """
    frozen = G._frozen_files(repo)
    index = _index_entries(repo=repo)
    for rel in frozen:
        mode = index.get(rel)
        if mode is None:
            report.add("SURFACE", "refuse",
                       f"frozen-surface file is absent from the git index "
                       f"(untracked or ignored): {rel}")
        elif mode not in _REGULAR_MODES:
            report.add("SURFACE", "refuse",
                       f"frozen-surface file is not a regular blob "
                       f"(mode {mode} -- symlink or submodule): {rel}")
    report.facts["frozen_surface_count"] = len(frozen)


# --------------------------------------------------------------------------
# the expiry tripwire -- signature verification (Decision amendment 2026-08-03)
# --------------------------------------------------------------------------

@contextlib.contextmanager
def anchored_roster(anchor: str, *, repo: Path = _REPO):
    """Materialize the pinned roster **from the trusted anchor object**, outside
    the candidate tree, and yield its path and text.

    Pointing ``-c gpg.ssh.allowedSignersFile`` at the candidate worktree's copy
    would only be safe *if* the closure comparison for that exact blob had
    already passed -- an ordering dependency, and a fragile one: findings
    accumulate rather than short-circuit, so a tampered roster is flagged by the
    closure check while this function would still have consulted it, and
    :func:`check_signatures` called on its own trusts the candidate outright.
    Reading the blob from the anchor removes the ordering question entirely: the
    candidate's copy is never trusted at any point.
    """
    blob = _blob_at(anchor, _ALLOWED_SIGNERS_REL, repo=repo)
    if blob is None:
        raise PreflightError(
            f"the pinned roster {_ALLOWED_SIGNERS_REL} is absent from the anchor "
            f"{anchor[:12]} -- first use requires the manual exact-byte "
            f"bootstrap (runbook steps M1-M5); the candidate's own copy is not "
            f"a substitute")
    tmpdir = tempfile.mkdtemp(prefix="cairn-preflight-roster-")
    path = Path(tmpdir) / "allowed_signers"
    path.write_bytes(blob)
    try:
        yield path, blob.decode("utf-8", "replace")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def parse_principals(text: str) -> set[str]:
    """Principals named by an ``allowed_signers`` document."""
    principals: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # The first field may carry several comma-separated principals
        # (`a@x,b@y ssh-ed25519 ...`), and `%GS` reports only the one that
        # matched. Splitting on whitespace alone would compare git's `a@x`
        # against the literal `a@x,b@y` and falsely refuse a legitimate signer.
        principals.update(p for p in line.split()[0].split(",") if p)
    if not principals:
        raise PreflightError(
            f"the pinned roster {_ALLOWED_SIGNERS_REL} names no principals")
    return principals


def check_signatures(anchor: str, head: str, report: Report, *,
                     repo: Path = _REPO) -> None:
    """Every commit being blessed, at or after the epoch, must be signed by a
    pinned key.

    This replaces the committer name/email equality check the Decision originally
    recorded. Those fields are supplied unauthenticated by the committing
    process: a second writer setting ``GIT_COMMITTER_NAME``/``EMAIL`` to the
    Maintainer's strings passed that check silently. Signature status does not
    forge: ``N`` (unsigned) and ``U`` (signed by an unpinned key) both refuse.
    """
    blessed = set(_rev_list(f"{anchor}..{head}", repo=repo))
    post_epoch = set(_rev_list(f"{_SIGNING_EPOCH}..{head}", repo=repo))
    post_epoch.add(_SIGNING_EPOCH)
    to_check = blessed & post_epoch

    # Supply the roster BY INVOCATION, never letting git resolve it through
    # `.git/config` (plan finding CR1). Verifying the roster's *contents* via the
    # authority closure is not enough while its *location* comes from a channel
    # the candidate controls and the read-only snapshot cannot observe: an
    # attacker who writes `gpg.ssh.allowedSignersFile` to a roster of their own
    # -- naming the same principal string with their own key -- gets `%G?` = `G`
    # and a rostered-looking `%GS` while `dev/.cairn/allowed_signers` sits
    # byte-identical and passes the closure check. Reproduced before this fix.
    # Command-line `-c` outranks repository config, so the trust chain reads:
    # anchor object -> closure-verified roster blob -> keys, with `.git/config`
    # off the path entirely.
    unsigned, foreign = [], []
    with anchored_roster(anchor, repo=repo) as (roster_path, roster_text):
        principals = parse_principals(roster_text)
        roster_cfg = {"gpg.ssh.allowedSignersFile": str(roster_path)}
        for sha in sorted(to_check):
            p = _git("log", "-1", "--format=%G?%x09%GS", sha, repo=repo,
                     config=roster_cfg)
            status, _, signer = (p.stdout or "").strip().partition("\t")
            if status != "G":
                unsigned.append((sha, status))
            elif signer not in principals:
                foreign.append((sha, signer))

    for sha, status in unsigned:
        report.add("SIGNING", "refuse",
                   f"commit {sha[:12]} at/after the signing epoch is not "
                   f"validly signed (status {status or '?'})")
    for sha, signer in foreign:
        report.add("SIGNING", "refuse",
                   f"commit {sha[:12]} is signed by an unpinned principal "
                   f"{signer!r}")

    report.facts["signing"] = {
        "epoch": _SIGNING_EPOCH,
        "commits_in_range": len(blessed),
        "checked": len(to_check),
        "grandfathered": len(blessed - post_epoch),
        "principals": sorted(principals),
    }


def _rev_list(spec: str, *, repo: Path = _REPO) -> list[str]:
    p = _git("rev-list", spec, repo=repo)
    if p.returncode != 0:
        return []
    return [s for s in (p.stdout or "").split() if s]


# --------------------------------------------------------------------------
# the remaining read-only checks
# --------------------------------------------------------------------------

def check_interpreter(report: Report) -> None:
    v = sys.version_info
    report.facts["interpreter"] = f"{v.major}.{v.minor}.{v.micro}"
    if (v.major, v.minor) != _CANONICAL_PY:
        report.add("INTERPRETER", "refuse",
                   f"running Python {v.major}.{v.minor}.{v.micro}; the manifest "
                   f"pins the collection set and is interpreter-minor sensitive, "
                   f"so it must be produced under "
                   f"{_CANONICAL_PY[0]}.{_CANONICAL_PY[1]}.x")


def check_tracked_clean(report: Report, *, repo: Path = _REPO) -> None:
    p = _git("status", "--porcelain", "--untracked-files=no", repo=repo)
    dirty = [ln for ln in (p.stdout or "").splitlines() if ln.strip()]
    if dirty:
        report.add("WORKTREE", "refuse",
                   "uncommitted tracked changes -- the blessed commit must "
                   "contain the bytes that were checked: "
                   + ", ".join(ln[3:] for ln in dirty[:5])
                   + (f" (+{len(dirty) - 5} more)" if len(dirty) > 5 else ""))


def check_anchor_position(anchor: str, head: str, report: Report, *,
                          repo: Path = _REPO) -> None:
    if anchor == head:
        report.add("ANCHOR", "refuse",
                   "anchor == HEAD: nothing to bless, or a half-run advanced the "
                   "ref without the manifest commit landing")
        return
    if _git("merge-base", "--is-ancestor", anchor, head,
            repo=repo).returncode != 0:
        report.add("ANCHOR", "refuse",
                   "the anchor is not an ancestor of HEAD -- a rebase or a bad "
                   "ref move has orphaned the trust root; resolve before "
                   "blessing")


def check_authority_modules(anchor: str, report: Report, *,
                            repo: Path = _REPO) -> None:
    """The six Stage-B modules, recorded and compared (Phase 0 step 1).

    A change is **not** a silent pass and **not** an ordinary refusal: it is
    ``review`` -- those bytes need genuine out-of-band human review, which no
    checker can perform, and no bundle may be emitted on that path.
    """
    recorded = {}
    for rel, abspath in R._authority_code_files():
        live = Path(abspath).read_bytes()
        recorded[rel] = _sha256_bytes(live)
        anchored = _blob_at(anchor, rel, repo=repo)
        if anchored is None:
            report.add("AUTHORITY", "review",
                       f"Stage-B authority module absent from the anchor: {rel}")
        elif _sha256_bytes(anchored) != recorded[rel]:
            report.add("AUTHORITY", "review",
                       f"Stage-B authority module changed since the anchor -- "
                       f"REVIEW REQUIRED, out-of-band: {rel}")
    report.facts["authority_hashes"] = recorded


# --------------------------------------------------------------------------
# the evidence artifact (plan finding GPR3) -- parsed fail-closed
# --------------------------------------------------------------------------

#: Printed by the evidence stage, every run. Deliberately not softened: the
#: proposal's Round-2 security review established that a repository-less tree
#: with a scrubbed environment is isolation from accidental relative writes, not
#: containment of Python, and the inherited helper's own docstring says
#: "contained, not hermetic". Claiming otherwise is the failure this whole
#: lifecycle kept repeating.
_EVIDENCE_RESIDUAL = """\
RESIDUAL -- this stage EXECUTES CANDIDATE CODE.
  The candidate tree is materialized without a .git directory, credential-shaped
  environment variables are dropped, HOME is redirected to a throwaway, and
  interactive git prompts are disabled.
  That is best-effort isolation and NOT containment: the executed code retains
  filesystem access outside this tree, process creation, and network access.
  Accepted by Maintainer Decision (trusted-contributor threat model, Cairn's own
  trust root, single-maintainer, as of 2026-08-03). This output is
  NON-AUTHORITATIVE evidence; `check` re-derives every static Git fact itself.
"""


def gather_evidence(candidate_ref: str = "HEAD", *, repo: Path = _REPO,
                    out=sys.stderr) -> dict:
    """Produce the evidence artifact by running the **candidate's** manifest
    producer over a materialized copy of the candidate tree.

    Separated from :func:`check` on purpose (plan finding GPR3): producing a
    manifest requires a pytest collection, which imports the candidate's
    ``conftest.py`` and test modules. ``check`` promises to be read-only, and a
    stage that executes host-capable code cannot make that promise. So this is a
    distinct, explicitly non-authoritative command, and everything it emits is
    treated by ``check`` as untrusted input.
    """
    out.write(_EVIDENCE_RESIDUAL + "\n")
    candidate = _resolve(candidate_ref, repo=repo)

    workdir = Path(tempfile.mkdtemp(prefix="cairn-evidence-tree-"))
    try:
        tarball = workdir / "candidate.tar"
        arc = _git("archive", "--format=tar", "-o", str(tarball), candidate,
                   repo=repo)
        if arc.returncode != 0:
            raise PreflightError(
                f"could not materialize the candidate tree: "
                f"{(arc.stderr or '').strip()}")
        tree = workdir / "tree"
        tree.mkdir()
        with tarfile.open(tarball) as tf:
            # ``filter="data"`` refuses absolute paths, ``..`` traversal, and
            # special files -- the extraction itself must not be the weak point.
            tf.extractall(tree, filter="data")
        tarball.unlink()

        out.write(f"materialized {candidate[:12]} at {tree} (no .git)\n")
        with R._scrubbed_environ():
            # Drop the invoking process's import path so the producer cannot
            # resolve `bootstrap.tests` from *another* checkout and measure a
            # tree other than the one being blessed. Hardening on its own
            # merits -- it was added while chasing an unrelated fixture bug
            # (a root-level `code.py` shadowing the stdlib module), and did not
            # fix that, so it is kept for the reason stated and not the one it
            # was reached for.
            import os as _os  # noqa: PLC0415 -- local, not a closure dep
            env = {k: v for k, v in _os.environ.items()
                   if k not in ("PYTHONPATH", "PYTHONHOME")}
            proc = subprocess.run(
                [sys.executable, "-E", "-s",
                 "bootstrap/tests/_gate_manifest.py", "produce"],
                cwd=str(tree), capture_output=True, text=True, check=False,
                env=env)
        if proc.returncode != 0:
            raise PreflightError(
                f"the candidate's manifest producer failed "
                f"(exit {proc.returncode}): {(proc.stderr or '')[-800:]}")
        try:
            manifest = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise PreflightError(
                f"the candidate's manifest producer emitted invalid JSON: "
                f"{exc}") from None
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    v = sys.version_info
    body = json.dumps(manifest, indent=2, sort_keys=True).encode() + b"\n"
    return {
        "schema": EVIDENCE_SCHEMA,
        "candidate_sha": candidate,
        "interpreter": f"{v.major}.{v.minor}.{v.micro}",
        "manifest": manifest,
        "manifest_sha256": _sha256_bytes(body),
    }


def parse_evidence(text: str) -> dict:
    """Parse an evidence artifact, refusing anything unexpected.

    ``check`` never produces this -- candidate collection executes host-capable
    code, and ``check`` is read-only. The producer is a separate, explicitly
    non-authoritative stage. Everything here is treated as untrusted input:
    every static Git fact is re-derived by ``check`` rather than believed.
    """
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise PreflightError(f"evidence is not valid JSON: {exc}") from None
    if not isinstance(data, dict):
        raise PreflightError("evidence must be a JSON object")
    if data.get("schema") != EVIDENCE_SCHEMA:
        raise PreflightError(
            f"evidence schema {data.get('schema')!r} != expected "
            f"{EVIDENCE_SCHEMA}")
    for key, typ in (("candidate_sha", str), ("interpreter", str),
                     ("manifest", dict), ("manifest_sha256", str)):
        if not isinstance(data.get(key), typ):
            raise PreflightError(
                f"evidence field {key!r} missing or not {typ.__name__}")
    sha = data["candidate_sha"]
    if len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
        raise PreflightError(f"evidence candidate_sha is not a full sha: {sha!r}")
    return data


def check_evidence(evidence: dict, head: str, report: Report) -> None:
    """Bind the evidence to the state ``check`` actually observed."""
    if evidence["candidate_sha"] != head:
        report.add("EVIDENCE", "refuse",
                   f"evidence was produced for {evidence['candidate_sha'][:12]} "
                   f"but HEAD is {head[:12]} -- stale or wrong-candidate "
                   f"evidence")
    recomputed = _sha256_bytes(
        json.dumps(evidence["manifest"], indent=2, sort_keys=True).encode()
        + b"\n")
    if recomputed != evidence["manifest_sha256"]:
        report.add("EVIDENCE", "refuse",
                   "evidence manifest digest does not match its manifest body")
    interp = evidence["interpreter"]
    if not interp.startswith(f"{_CANONICAL_PY[0]}.{_CANONICAL_PY[1]}."):
        report.add("EVIDENCE", "refuse",
                   f"evidence was produced under Python {interp}, not "
                   f"{_CANONICAL_PY[0]}.{_CANONICAL_PY[1]}.x")
    report.facts["evidence"] = {
        "candidate_sha": evidence["candidate_sha"],
        "interpreter": interp,
        "manifest_sha256": evidence["manifest_sha256"],
    }


# --------------------------------------------------------------------------
# Chunk C -- the digest-bound bundle
# --------------------------------------------------------------------------

#: Bundle schema version. ``apply`` refuses anything else.
BUNDLE_SCHEMA = 1

#: The enumerated write operations ``apply`` needs -- object writes, the real
#: index/worktree transition, and the two-direct-ref transaction. Deliberately a
#: *separate* allowlist from :data:`_READ_ONLY_GIT`, so `check` has no path to
#: any repository writer while `apply`'s capability is stated rather than
#: implied (security code review CR4).
_WRITE_GIT = frozenset({
    "update-ref",     # the two-direct-ref transaction, --stdin only
    "hash-object",    # write the manifest blob
    "read-tree",      # build the prospective tree in a TEMP index
    "update-index",   # insert the blob there, and refresh the real index
    "write-tree",
    "commit-tree",    # construct the signed commit
    "add",            # the post-transaction worktree/index sync
})


def draft_message(*, observed_anchor: str, checked_head: str,
                  manifest_sha256: str, authority_hashes: dict,
                  scope: dict, last_legitimate_anchor: str | None = None,
                  erroneous_ref: str | None = None) -> str:
    """The commit message, built from values the checker computed.

    The runbook's audit trail requires the authorized verifier hashes, both
    anchor SHAs, and the derived scope. Those are mechanical facts; asking a
    human to retype six sha256 strings mid-ceremony is how the 2026-07-31 run
    lost its audit trail entirely.

    It does **not** contain the resulting ``P`` SHA (security review SR4): a
    commit's SHA hashes its own message, so a message cannot carry it. The real
    ``e5ecaa5`` / ``bf08f62`` messages say "this commit", which is the honest
    form and the one used here.
    """
    hashes = "\n".join(f"  {v}  {k}" for k, v in sorted(authority_hashes.items()))
    recovery = ""
    if last_legitimate_anchor:
        recovery = (
            f"\nRECOVERY -- the superseded anchor recorded below is the "
            f"Maintainer-supplied last legitimately blessed anchor,\n"
            f"{last_legitimate_anchor}. It was NOT inferred: nothing in this "
            f"repository can derive it, because\ncustom refs carry no reflog.\n")
        if erroneous_ref:
            recovery += (
                f"The ref currently reads {erroneous_ref}, which this run "
                f"treats as erroneous rather than\nas the prior state.\n")
    return f"""\
gate-anchor: supervised trust-root re-establishment (REANCHOR_RUNBOOK Phase 0)

Regenerates {_MANIFEST_REL} over the reviewed tree at
{checked_head[:12]} and re-establishes it as the prior gate state P.
{recovery}
Authorized verifier-module hashes (Phase 0 step 1):

{hashes}

Scope blessed -- derived at check time from the observed state:

  superseded anchor P : {last_legitimate_anchor or observed_anchor}
  checked HEAD        : {checked_head}
  new anchor P        : this commit
  prospective manifest: {manifest_sha256}
  frozen gate files   : {scope.get('modified', '?')} modified, \
{scope.get('added', '?')} added, {scope.get('removed', '?')} removed
  pytest collection   : {scope.get('collection_before', '?')} -> \
{scope.get('collection_after', '?')}

Produced under the canonical interpreter. The pre-flight ran read-only from the
anchored checker; the review, the decision, this commit and the ref advance are
the Maintainer's own acts, per REANCHOR_RUNBOOK's Maintainer-only constraint.
"""


def blessing_plan(report: Report, evidence: dict, *, repo: Path = _REPO,
                  last_legitimate_anchor: str | None = None) -> dict:
    """The derived description of what a blessing would do.

    Formerly emitted as a handoff *bundle* that ``apply`` read back and trusted.
    Code review CR1 falsified that: value and digest sat in the same editable
    JSON, so re-hashing a tampered manifest was accepted. It is now built in
    memory by whichever command needs it, and `check` may write it out only as a
    **record for the operator to read** -- nothing consumes it as authority.
    """
    old = json.loads(_blob_at(report.facts["anchor"], _MANIFEST_REL,
                              repo=repo) or b"{}")
    new = evidence["manifest"]
    of, nf = old.get("frozen_files", {}), new.get("frozen_files", {})
    scope = {
        "modified": sum(1 for k in nf if k in of and nf[k] != of[k]),
        "added": sum(1 for k in nf if k not in of),
        "removed": sum(1 for k in of if k not in nf),
        "collection_before": old.get("collection", {}).get("node_count", "?"),
        "collection_after": new.get("collection", {}).get("node_count", "?"),
    }
    erroneous = (report.facts["anchor"]
                 if last_legitimate_anchor
                 and last_legitimate_anchor != report.facts["anchor"] else None)
    message = draft_message(
        observed_anchor=report.facts["anchor"],
        checked_head=report.facts["head"],
        manifest_sha256=evidence["manifest_sha256"],
        authority_hashes=report.facts["authority_hashes"],
        scope=scope, last_legitimate_anchor=last_legitimate_anchor,
        erroneous_ref=erroneous)
    return {
        "schema": BUNDLE_SCHEMA,
        "checked_head": report.facts["head"],
        "observed_anchor": report.facts["anchor"],
        "last_legitimate_anchor": last_legitimate_anchor,
        "manifest": evidence["manifest"],
        "manifest_sha256": evidence["manifest_sha256"],
        "message": message,
        "message_sha256": _sha256_bytes(message.encode()),
        "authority_hashes": report.facts["authority_hashes"],
        "scope": scope,
    }


# --------------------------------------------------------------------------
# Chunk D -- apply: revalidate, construct, verify, then one ref transaction
# --------------------------------------------------------------------------

def _git_write(*args: str, repo: Path = _REPO, stdin: str | None = None,
               want_bytes: bool = False) -> subprocess.CompletedProcess:
    """The **only** repository-writing path, with its own enumerated allowlist."""
    if not args or args[0] not in _WRITE_GIT:
        raise PreflightError(
            f"apply may only run {sorted(_WRITE_GIT)}; refused "
            f"{(args[0] if args else '<none>')!r}")
    return subprocess.run(["git", "-C", str(repo), *args], input=stdin,
                          capture_output=True, text=not want_bytes, check=False)


def _require_direct_ref(ref: str, *, repo: Path = _REPO) -> None:
    """Refuse a symbolic ref as a transaction target (code review CR4).

    ``update-ref`` follows a symbolic ref by default, so a gate anchor turned
    symbolic would silently advance a *third* logical ref -- the claimed two-ref
    transaction would then have three targets.
    """
    p = _git("rev-parse", "--symbolic-full-name", ref, repo=repo)
    resolved = (p.stdout or "").strip()
    if resolved != ref:
        raise PreflightError(
            f"{ref} is symbolic (points at {resolved!r}); the transaction "
            f"requires direct refs so it has exactly its two intended targets")


def _construct_signed_commit(repo: Path, head: str, manifest_bytes: bytes,
                             message: str) -> str:
    """Build ``N = HEAD's tree + the reviewed manifest``, with the reviewed
    message, **signed**.

    Written here rather than reusing ``_gate_reanchor._construct_anchor_commit``
    for two reasons: that helper hard-codes its own message and does not sign, so
    the audit trail never reached the commit and the most privileged commit in
    the repository was unsigned (code review CR2); and it is a FROZEN gate file,
    so editing it would force a re-anchor to fix a defect in this plan's work.

    A temporary index is used, so nothing touches the real index or worktree
    until the transaction has succeeded.
    """
    with tempfile.TemporaryDirectory(prefix="cairn-preflight-idx-") as td:
        idx = str(Path(td) / "index")

        def g(*args, **kw):
            kw.setdefault("repo", repo)
            return _git_write(*args, **kw)

        # The index-scoped steps need GIT_INDEX_FILE in the child environment;
        # _git_write does not thread env, so it is set around them and restored.
        import os as _os  # noqa: PLC0415 -- local, not an authority-closure dep
        saved = _os.environ.get("GIT_INDEX_FILE")
        _os.environ["GIT_INDEX_FILE"] = idx
        try:
            rt = g("read-tree", head)
            if rt.returncode != 0:
                raise PreflightError(f"read-tree failed: {rt.stderr.strip()}")
            ho = _git_write("hash-object", "-w", "--stdin", repo=repo,
                            stdin=manifest_bytes.decode("utf-8"))
            if ho.returncode != 0:
                raise PreflightError(f"hash-object failed: {ho.stderr.strip()}")
            blob = ho.stdout.strip()
            ui = g("update-index", "--add", "--cacheinfo",
                   f"100644,{blob},{_MANIFEST_REL}")
            if ui.returncode != 0:
                raise PreflightError(f"update-index failed: {ui.stderr.strip()}")
            wt = g("write-tree")
            tree = wt.stdout.strip()
            if wt.returncode != 0 or not tree:
                raise PreflightError(f"write-tree failed: {wt.stderr.strip()}")
            ct = _git_write("commit-tree", tree, "-p", head, "-S", "-F", "-",
                            repo=repo, stdin=message)
            new = ct.stdout.strip()
            if ct.returncode != 0 or len(new) != 40:
                raise PreflightError(
                    f"commit-tree failed (is signing configured?): "
                    f"{ct.stderr.strip()}")
            return new
        finally:
            if saved is None:
                _os.environ.pop("GIT_INDEX_FILE", None)
            else:
                _os.environ["GIT_INDEX_FILE"] = saved


def verify_constructed(repo: Path, new: str, head: str, *,
                       manifest_sha256: str, message: str,
                       principals: set, roster_path: Path) -> None:
    """Verify the constructed commit **from the commit object**, before any ref
    moves: exact parent, exact changed path, exact manifest blob digest, exact
    message, valid signature, pinned principal (code review CR2)."""
    parents = _git("rev-parse", f"{new}^@", repo=repo).stdout.split()
    if parents != [head]:
        raise PreflightError(
            f"constructed commit's parent is {parents}, expected [{head}]")

    changed = [f for f in _git("diff", "--name-only", f"{head}..{new}",
                               repo=repo).stdout.splitlines() if f.strip()]
    if changed != [_MANIFEST_REL]:
        raise PreflightError(
            f"constructed commit changes {changed}, expected only "
            f"[{_MANIFEST_REL}]")

    blob = _blob_at(new, _MANIFEST_REL, repo=repo)
    if blob is None or _sha256_bytes(blob) != manifest_sha256:
        raise PreflightError(
            "constructed commit's manifest blob does not carry the reviewed "
            "digest")

    body = _git("log", "-1", "--format=%B", new, repo=repo).stdout
    if body.strip() != message.strip():
        raise PreflightError(
            "constructed commit does not carry the reviewed message -- the "
            "audit trail would be lost")

    sig = _git("log", "-1", "--format=%G?%x09%GS", new, repo=repo,
               config={"gpg.ssh.allowedSignersFile": str(roster_path)})
    status, _, signer = (sig.stdout or "").strip().partition("\t")
    if status != "G":
        raise PreflightError(
            f"constructed commit is not validly signed (status {status or '?'})"
            f" -- it becomes the anchor, so later anchor..HEAD checks would "
            f"never see it")
    if signer not in principals:
        raise PreflightError(
            f"constructed commit is signed by an unpinned principal {signer!r}")


def _advance_both_refs(repo: Path, branch: str, new: str, *,
                       branch_old: str, anchor_old: str) -> tuple[bool, str]:
    """Advance the branch and the gate anchor in **one** expected-old transaction.

    ``--no-deref`` so a symbolic target cannot redirect an update (CR4), on top
    of the direct-ref precondition checked separately.
    """
    stdin = (f"start\n"
             f"update {branch} {new} {branch_old}\n"
             f"update {_ANCHOR_REF} {new} {anchor_old}\n"
             f"prepare\ncommit\n")
    p = _git_write("update-ref", "--no-deref", "--stdin", repo=repo, stdin=stdin)
    return p.returncode == 0, (p.stderr or p.stdout or "").strip()


def _sync_worktree(repo: Path, manifest_bytes: bytes) -> None:
    """Bring the real index and worktree in line with the new HEAD.

    Construction uses a temporary index, so before this the real index and
    worktree still carry the pre-blessing blob and ``git status`` reports the
    manifest as staged against the new trust root -- an immediate dirty state and
    a staged rollback waiting to ride a later commit (code review CR3). Because
    construction touched neither, an aborted transaction leaves **no** residue at
    all, which is stronger than reporting one.
    """
    (repo / _MANIFEST_REL).write_bytes(manifest_bytes)
    add = _git_write("add", "--", _MANIFEST_REL, repo=repo)
    if add.returncode != 0:
        raise PreflightError(
            f"the refs advanced but the worktree/index sync failed: "
            f"{add.stderr.strip()} -- the repository is left with the manifest "
            f"unstaged; reconcile before committing anything else")


def apply_now(*, repo: Path = _REPO, confirmed: bool = False,
              out=sys.stderr) -> dict:
    """Re-derive everything, then bless -- **no handoff artifact is trusted**.

    Code review CR1 established that a bundle carrying its own digests is a
    corruption check, not tamper evidence: both value and digest come from the
    same editable JSON, and an execution probe re-hashed a tampered manifest and
    had it anchored. External review then rejected both an out-of-band digest
    argument (file-write and terminal access are one practical authority domain
    on a single-user machine, and it burdens the operator with a 64-character
    provenance) and a signed check artifact (agents already hold the Maintainer's
    key, so a signature proves "someone could use this key", not "the anchored
    checker produced these bytes" -- the same key-holder-not-process limit
    :func:`check_signatures` documents).

    So there is no authority-bearing file. ``apply`` runs the evidence stage and
    the read-only checks itself, keeps the result in memory, and constructs from
    values it derived. ``check`` remains available as a non-mutating preview; its
    output is a record for the operator to read, never an input here.
    """
    if not confirmed:
        raise PreflightError(
            "apply requires explicit Maintainer confirmation "
            "(--confirm-supervised-reanchor); it moves the trust root")

    out.write("apply: re-deriving everything; no handoff artifact is trusted\n")
    evidence = gather_evidence("HEAD", repo=repo, out=out)
    report = check(repo=repo, evidence=evidence)
    _render(report, out)
    if report.blocked:
        raise PreflightError(
            "the read-only checks refuse this state; nothing was written")

    head, anchor = report.facts["head"], report.facts["anchor"]
    branch = _git("rev-parse", "--symbolic-full-name", "HEAD",
                  repo=repo).stdout.strip()
    if not branch.startswith("refs/heads/"):
        raise PreflightError(
            f"HEAD is not on a branch ({branch!r}); refusing to advance a "
            f"detached HEAD")
    _require_direct_ref(_ANCHOR_REF, repo=repo)

    plan = blessing_plan(report, evidence, repo=repo)
    manifest_bytes = (json.dumps(evidence["manifest"], indent=2, sort_keys=True)
                      .encode() + b"\n")

    with anchored_roster(anchor, repo=repo) as (roster_path, roster_text):
        principals = parse_principals(roster_text)
        new = _construct_signed_commit(repo, head, manifest_bytes,
                                       plan["message"])
        verify_constructed(repo, new, head,
                           manifest_sha256=evidence["manifest_sha256"],
                           message=plan["message"], principals=principals,
                           roster_path=roster_path)
    out.write(f"constructed, signed and verified {new[:12]}\n")

    ok, detail = _advance_both_refs(repo, branch, new, branch_old=head,
                                    anchor_old=anchor)
    if not ok:
        raise PreflightError(
            f"the ref transaction ABORTED -- neither {branch} nor {_ANCHOR_REF} "
            f"moved, and the real index and worktree were never touched, so "
            f"there is no residue to reconcile. {new[:12]} is an unreferenced "
            f"object left in place rather than deleted, so the state is "
            f"inspectable: {detail}")
    _sync_worktree(repo, manifest_bytes)
    out.write(f"advanced {branch} and {_ANCHOR_REF} to {new[:12]} in one "
              f"expected-old transaction; worktree and index synced\n")
    return {"new_anchor": new, "branch": branch, "previous_anchor": anchor,
            "previous_head": head}


# --------------------------------------------------------------------------
# orchestration
# --------------------------------------------------------------------------

def check(*, repo: Path = _REPO, evidence: dict | None = None,
          trusted_repo: str | None = None,
          trusted_ref: str = "HEAD") -> Report:
    """Run every read-only check. Returns a :class:`Report`; raises only on a
    condition that must not be summarised into a finding."""
    report = Report()
    check_interpreter(report)
    check_tracked_clean(report, repo=repo)

    anchor = _resolve(_ANCHOR_REF, repo=repo)
    head = _resolve("HEAD", repo=repo)
    report.facts["anchor"] = anchor
    report.facts["head"] = head

    check_anchor_position(anchor, head, report, repo=repo)
    check_authority_closure(anchor, report, repo=repo)
    check_authority_modules(anchor, report, repo=repo)
    check_frozen_surface(report, repo=repo)
    check_signatures(anchor, head, report, repo=repo)

    # Threaded through even though this repository passes neither -- the
    # Decision's constraint, so external anchoring stays a configuration change
    # rather than a retrofit.
    report.facts["external_anchor"] = {
        "trusted_repo": trusted_repo, "trusted_ref": trusted_ref,
        "note": ("no external anchor supplied; integrity is target-owned, not "
                 "externally anchored" if not trusted_repo else None),
    }

    if evidence is not None:
        check_evidence(evidence, head, report)
        report.facts["evidence_checked"] = True
    return report


def _render(report: Report, out) -> None:
    for f in report.findings:
        out.write(f"[{f.level.upper():7}] {f.code}: {f.message}\n")
    out.write("\n")
    json.dump(report.facts, out, indent=2, sort_keys=True)
    out.write("\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="gate_preflight",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="run the read-only pre-flight checks")
    c.add_argument("--repo", default=None)
    c.add_argument("--evidence", default=None,
                   help="path to an evidence artifact (produced by the separate, "
                        "non-authoritative evidence stage)")
    c.add_argument("--trusted-repo", default=None,
                   help="resolve the anchor object from THIS repository, not the "
                        "target (external anchoring)")
    c.add_argument("--trusted-ref", default="HEAD")
    c.add_argument("--bundle-out", default=None,
                   help="write the derived blessing plan here as a RECORD to "
                        "read (requires --evidence). It is not an input to "
                        "`apply`, which trusts no handoff artifact.")
    c.add_argument("--last-legitimate-anchor", default=None,
                   help="recovery only: the Maintainer-supplied last "
                        "legitimately blessed anchor. Nothing can derive this "
                        "-- custom refs carry no reflog -- so it is never "
                        "inferred, and the erroneous ref is disclosed apart "
                        "from it.")

    e = sub.add_parser(
        "evidence",
        help="produce the evidence artifact -- EXECUTES CANDIDATE CODE; "
             "non-authoritative, and deliberately not part of `check`")
    e.add_argument("--repo", default=None)
    e.add_argument("--candidate-ref", default="HEAD")
    e.add_argument("-o", "--output", default=None,
                   help="write the artifact here (default: stdout)")
    a = sub.add_parser(
        "apply",
        help="revalidate a bundle, construct and verify the commit, then move "
             "the branch and gate anchor in ONE transaction -- Maintainer-only")
    a.add_argument("--repo", default=None)
    a.add_argument("--confirm-supervised-reanchor", action="store_true",
                   dest="confirmed",
                   help="required; this is the only step that moves the trust "
                        "root")
    args = ap.parse_args(argv)

    repo = Path(args.repo) if args.repo else _REPO

    if args.cmd == "evidence":
        try:
            artifact = gather_evidence(args.candidate_ref, repo=repo)
        except PreflightError as exc:
            sys.stderr.write(f"[REFUSE ] {exc}\n")
            return 2
        text = json.dumps(artifact, indent=2, sort_keys=True) + "\n"
        if args.output:
            Path(args.output).write_text(text, encoding="utf-8")
            sys.stderr.write(f"evidence written to {args.output}\n")
        else:
            sys.stdout.write(text)
        return 0

    if args.cmd == "apply":
        try:
            result = apply_now(repo=repo, confirmed=args.confirmed)
        except PreflightError as exc:
            sys.stderr.write(f"[REFUSE ] {exc}\n")
            return 2
        json.dump(result, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0

    try:
        evidence = (parse_evidence(
                        Path(args.evidence).read_text(encoding="utf-8"))
                    if args.evidence else None)
        report = check(repo=repo, evidence=evidence,
                       trusted_repo=args.trusted_repo,
                       trusted_ref=args.trusted_ref)
    except PreflightError as exc:
        sys.stderr.write(f"[REFUSE ] {exc}\n")
        return 2
    _render(report, sys.stderr)
    if not report.blocked and args.bundle_out:
        if evidence is None:
            sys.stderr.write("[REFUSE ] --bundle-out requires --evidence\n")
            return 2
        plan = blessing_plan(report, evidence, repo=repo,
                             last_legitimate_anchor=args.last_legitimate_anchor)
        Path(args.bundle_out).write_text(
            json.dumps(plan, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        sys.stderr.write(
            f"preview record written to {args.bundle_out} -- this is a RECORD "
            f"for you to read, NOT an input to `apply`, which re-derives "
            f"everything itself\n")
    if report.blocked:
        sys.stderr.write("\nPRE-FLIGHT REFUSED -- do not bless this state.\n")
        return 1
    sys.stderr.write("\nPre-flight checks pass. The blessing remains the "
                     "Maintainer's act.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
