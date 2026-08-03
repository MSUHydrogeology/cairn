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
         config: dict[str, str] | None = None) -> subprocess.CompletedProcess:
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
                          capture_output=True, text=True, check=False)


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
    p = subprocess.run(["git", "-C", str(repo), "show", f"{sha}:{rel}"],
                       capture_output=True, check=False)
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
# orchestration
# --------------------------------------------------------------------------

def check(*, repo: Path = _REPO, evidence_path: str | None = None,
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

    if evidence_path is not None:
        evidence = parse_evidence(Path(evidence_path).read_text(encoding="utf-8"))
        check_evidence(evidence, head, report)
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
    args = ap.parse_args(argv)

    repo = Path(args.repo) if args.repo else _REPO
    try:
        report = check(repo=repo, evidence_path=args.evidence,
                       trusted_repo=args.trusted_repo,
                       trusted_ref=args.trusted_ref)
    except PreflightError as exc:
        sys.stderr.write(f"[REFUSE ] {exc}\n")
        return 2
    _render(report, sys.stderr)
    if report.blocked:
        sys.stderr.write("\nPRE-FLIGHT REFUSED -- do not bless this state.\n")
        return 1
    sys.stderr.write("\nPre-flight checks pass. The blessing remains the "
                     "Maintainer's act.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
