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
import base64
import hashlib
import json
import os
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
    "ls-tree", "diff", "merge-base", "for-each-ref", "status",
    # `diff-tree` added by plan `git-native-security-foundations`, Chunk B, for
    # the range-review report's endpoint path set.  Safe here for reasons that
    # are checkable rather than assumed: it cannot write; it is invoked only
    # with `--name-only`, so no content is generated and neither a textconv
    # driver nor an external diff can run; `diff.external` is pinned empty and
    # `core.useReplaceRefs` false in `_STERILE_CONFIG` above; and `--no-renames`
    # is passed so rename detection cannot merge an add and a delete into one
    # entry the classifier never sees.  This is a *widening of a security
    # allowlist* and is recorded as such.
    "diff-tree",
    # `archive` was here and is deliberately gone: it is attribute-aware, so a
    # candidate `.gitattributes` could hide a tracked file from the materialized
    # tree (FUR3). `raw_tree` reads `ls-tree` + `cat-file` instead, and removing
    # the subcommand makes the archive path unreachable rather than merely
    # unused.
})

#: The signature backend, pinned by absolute path. ``gpg.ssh.program`` is an
#: ordinary repository-config key: pointing it at a script that answers
#: ``-Y find-principals`` with a rostered name and ``-Y verify`` with success
#: made a commit signed by a key **absent from the roster** report ``%G? = G``
#: and ``%GS = m@example``. Reproduced against these exact bytes; pinning this
#: restores ``U``. Used for verification *and* signing.
_SSH_KEYGEN = "/usr/bin/ssh-keygen"

#: Config forced onto **every** git invocation, read or write.
#:
#: CR1 found one instance of this class (the roster's *location*) and its
#: reviewer flagged the class as unswept. The previous fix pinned exactly one
#: sibling and declared the class closed; the first-use review then found four
#: more, each defeating a different asserted guarantee. Each entry below is
#: paired with the attack it was verified against, because "pinned a plausible
#: key" is not evidence:
#:
#: * ``core.useReplaceRefs`` -- ``refs/replace/<anchor>`` made ``show
#:   <anchor>:<path>`` return attacker bytes while ``rev-parse`` still reported
#:   the original SHA, so :func:`anchored_roster` read an attacker roster with
#:   every SHA looking correct (FUR1 probe 1).
#: * ``core.hooksPath`` -- a ``reference-transaction`` hook advanced a **third**
#:   ref while the two-ref transaction reported success (FUR2). ``/dev/null``
#:   disables the configured path *and* the default ``.git/hooks``.
#: * ``core.fsmonitor`` -- a configured monitor program executed during
#:   ``git status``, so ``check`` was never structurally free of
#:   candidate-configured execution (FUR2).
#: * ``gpg.format`` -- unpinned, a candidate selects a backend whose program
#:   key is not the one pinned below.
#: * ``core.quotePath`` -- non-ASCII frozen paths read back escaped and never
#:   match the glob (a false refusal, not a bypass, but the same shape).
#:
#: Command-line ``-c`` outranks system, global, repository **and worktree**
#: config; verified here that it also outranks ``GIT_CONFIG_KEY_n`` /
#: ``GIT_CONFIG_VALUE_n`` in the environment.
#:
#: **What this does not cover**, stated rather than left to be inferred: in-tree
#: ``.gitattributes`` has no config switch, so ``export-ignore`` and filter
#: drivers are addressed structurally instead -- see :func:`_tree_files` and
#: :func:`_install_blob_in_index`.
_STERILE_CONFIG: dict[str, str] = {
    "core.useReplaceRefs": "false",
    "core.hooksPath": os.devnull,
    "core.fsmonitor": "false",
    "core.quotePath": "false",
    "gpg.format": "ssh",
    "diff.external": "",
    "core.pager": "cat",
}

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

_RESOLVED: dict[str, str] = {}


def _resolved_binary(name: str, pinned: str | None = None) -> str:
    """Resolve an executable to an absolute path, once, and refuse a bad one.

    **This is not a containment control**, and the distinction matters after
    four rounds of claiming protections at the strength intended rather than
    delivered: ``PATH`` belongs to the operator, and the evidence stage's
    declared non-containment residual means escaped candidate code could write
    somewhere on it. What this does is resolve once instead of per invocation,
    and report the concrete path, so the operator can see what actually ran.

    Symlinks are **followed, not refused**. An earlier draft refused them and
    broke on an ordinary Homebrew install, where ``/opt/homebrew/bin/git`` is a
    symlink into the Cellar -- and refusing bought nothing, since exec follows
    the link either way. Resolving makes the reported path the true one.
    """
    if name not in _RESOLVED:
        found = pinned or shutil.which(name)
        if not found:
            raise PreflightError(f"{name} was not found on PATH")
        p = Path(found)
        if not p.is_absolute():
            raise PreflightError(f"the {name} path {found} is not absolute")
        p = p.resolve()
        if not p.is_file() or not os.access(p, os.X_OK):
            raise PreflightError(
                f"{found} resolves to {p}, which is not an executable regular "
                f"file; refusing rather than running an unexpected binary in "
                f"the ceremony")
        _RESOLVED[name] = str(p)
    return _RESOLVED[name]


def _sterile_env(index: str | None = None) -> dict[str, str]:
    """The child environment for every git invocation.

    Every ``GIT_*`` variable is **dropped** rather than denylisted by name. The
    set that steers git is large -- ``GIT_DIR``, ``GIT_WORK_TREE``,
    ``GIT_INDEX_FILE``, ``GIT_CONFIG_*``, ``GIT_EXTERNAL_DIFF``,
    ``GIT_SSH_COMMAND``, ``GIT_REPLACE_REF_BASE``, the four pathspec flags --
    and grows between releases, so removing everything and putting back what the
    ceremony needs fails safe where an enumerated denylist does not.

    The rest of the environment is left alone: ``PATH``, ``HOME`` and
    ``SSH_AUTH_SOCK`` are the operator's, and signing needs them. That is a
    scope statement, not a trust claim -- the runbook's residual trust set is
    where the chain actually ends.
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_TERMINAL_PROMPT"] = "0"
    if index is not None:
        env["GIT_INDEX_FILE"] = index
    return env


def _run_git(args: tuple[str, ...], *, repo: Path,
             config: dict[str, str] | None = None,
             stdin: str | bytes | None = None, want_bytes: bool = False,
             index: str | None = None) -> subprocess.CompletedProcess:
    """The single sterile-Git launcher. Both allowlists route through here.

    Nothing else in this module may call ``subprocess`` with ``git``: the
    guarantees above hold only if there is exactly one place they are applied,
    and a second call site is how ``_blob_at`` once bypassed the read-only
    guard.
    """
    merged = {**_STERILE_CONFIG,
              "gpg.ssh.program": _resolved_binary("ssh-keygen", _SSH_KEYGEN),
              **(config or {})}
    overrides: list[str] = []
    for key, value in merged.items():
        overrides += ["-c", f"{key}={value}"]
    return subprocess.run(
        [_resolved_binary("git"), "-C", str(repo), *overrides, *args],
        input=stdin, capture_output=True, text=not want_bytes, check=False,
        env=_sterile_env(index))


def _git(*args: str, repo: Path = _REPO,
         config: dict[str, str] | None = None,
         want_bytes: bool = False,
         stdin: str | bytes | None = None) -> subprocess.CompletedProcess:
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
    return _run_git(args, repo=repo, config=config, want_bytes=want_bytes,
                    stdin=stdin)


def _require_worktree_root(repo: Path) -> Path:
    """Resolve the target repository, and refuse anything that is not its root.

    Two failures, one root cause: **the checker's own location is not the
    target.** The recorded anchored invocation extracts ``bootstrap/tests`` into
    a temp directory and runs the checker from there, so the ``_REPO`` default --
    computed from ``__file__`` -- names the *extraction* directory, not the
    checkout being blessed. Executing the runbook's exact steps refused with
    git's bare ``fatal: not a git repository`` before reaching the real checkout
    (first-use review FUR5): fail-closed, but undiagnosable, and it meant the
    recorded ceremony had never been run.

    The second failure is why "not a git repository" was luck rather than
    design. ``git -C <path>`` **discovers upward**. Had the extraction landed
    anywhere beneath a repository -- a ``$TMPDIR`` inside a checkout is enough --
    the identical invocation would have found *that* repository and blessed it,
    reporting success against a target the operator never named. So requiring
    *a* repository is not enough; the path must be the top level of the worktree
    it names, which is what makes the binding explicit rather than ambient.
    """
    resolved = Path(repo).resolve()
    p = _git("rev-parse", "--show-toplevel", repo=resolved)
    top = (p.stdout or "").strip()
    if p.returncode != 0 or not top:
        raise PreflightError(
            f"not a git repository: {resolved} -- name the checkout to bless "
            f"explicitly as `--repo <checkout>`. The anchored invocation runs "
            f"this checker from a temp extraction directory, so its own "
            f"location is never the target ({(p.stderr or '').strip()!r})")
    if Path(top).resolve() != resolved:
        raise PreflightError(
            f"{resolved} is not the top level of a git worktree -- git "
            f"discovered {Path(top).resolve()} by walking upward. Refusing "
            f"rather than operating on a repository the invocation did not name")
    return resolved


#: Object format -> full object-id width.  The one place a width is named.
#: Plan `git-native-security-foundations`, Chunk A5: three call sites required
#: a literal 40, so a SHA-256 repository -- which returns a valid 64-hex id --
#: was refused on the PUBLIC path before any helper could be reached.
_OBJECT_FORMAT_WIDTH = {"sha1": 40, "sha256": 64}


def _object_id_width(*, repo: Path = _REPO) -> int:
    """The repository's own object-id width.  No default, ever.

    A missing or unreadable format is a refusal rather than a fall back to
    SHA-1: assuming the algorithm is the defect this replaces.
    """
    p = _git("rev-parse", "--show-object-format", repo=repo)
    fmt = (p.stdout or "").strip()
    if p.returncode != 0 or fmt not in _OBJECT_FORMAT_WIDTH:
        raise PreflightError(
            f"could not establish the object format of {str(repo)!r} "
            f"({(p.stderr or '').strip() or fmt!r}); refusing rather than "
            f"assuming sha1")
    return _OBJECT_FORMAT_WIDTH[fmt]


def _resolve(ref: str, *, repo: Path = _REPO) -> str:
    p = _git("rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}",
             repo=repo)
    sha = (p.stdout or "").strip()
    if p.returncode != 0 or len(sha) != _object_id_width(repo=repo) or any(
            c not in "0123456789abcdef" for c in sha):
        raise PreflightError(
            f"ref does not resolve to a commit: {ref!r} "
            f"({(p.stderr or '').strip()})")
    return sha


def _tree_entries(commit: str, *,
                  repo: Path = _REPO) -> list[tuple[str, str, str]]:
    """Every blob in a commit's tree, read from the **raw object graph**.

    ``ls-tree -r -z`` walks tree objects and does no attribute processing, which
    is the whole point: ``git archive`` honours in-tree ``.gitattributes``, so a
    tracked file marked ``export-ignore`` was silently absent from the
    materialized tree. The candidate's producer never saw it, the manifest it
    emitted did not pin it, and the blessed commit's tree contained it anyway
    (FUR3, reproduced). ``-z`` also means paths arrive raw rather than quoted.
    """
    p = _git("ls-tree", "-r", "-z", "--full-tree", commit, repo=repo,
             want_bytes=True)
    if p.returncode != 0:
        raise PreflightError(
            f"could not list the tree of {commit[:12]}: "
            f"{(p.stderr or b'').decode('utf-8', 'replace').strip()}")
    entries: list[tuple[str, str, str]] = []
    for record in p.stdout.split(b"\0"):
        if not record:
            continue
        meta, _, path = record.partition(b"\t")
        mode, _, rest = meta.partition(b" ")
        _type, _, sha = rest.partition(b" ")
        entries.append((mode.decode(), sha.decode(),
                        path.decode("utf-8", "surrogateescape")))
    return entries


def _batch_blobs(shas: list[str], *, repo: Path = _REPO) -> list[bytes]:
    """Read many blobs in one ``cat-file --batch``.

    472 separate ``cat-file`` invocations would work and be unusably slow; the
    batch protocol is ``<sha> SP <type> SP <size> LF <contents> LF`` per request,
    in request order.
    """
    if not shas:
        return []
    p = _git("cat-file", "--batch", repo=repo, want_bytes=True,
             stdin="".join(f"{s}\n" for s in shas).encode())
    if p.returncode != 0:
        raise PreflightError(
            f"could not read {len(shas)} blob(s): "
            f"{(p.stderr or b'').decode('utf-8', 'replace').strip()}")
    out, pos, blobs = p.stdout, 0, []
    for sha in shas:
        nl = out.find(b"\n", pos)
        if nl < 0:
            raise PreflightError(f"truncated cat-file stream at {sha[:12]}")
        header = out[pos:nl].split()
        if len(header) != 3 or header[1] != b"blob":
            raise PreflightError(
                f"expected a blob record for {sha[:12]}, got {out[pos:nl]!r}")
        start = nl + 1
        blobs.append(out[start:start + int(header[2])])
        pos = start + int(header[2]) + 1
    return blobs


@contextlib.contextmanager
def raw_tree(commit: str, *, repo: Path = _REPO):
    """Materialize a commit's tree from raw objects, outside the repository.

    Replaces ``git archive``, which is attribute-aware and therefore
    candidate-steerable (FUR3). Non-regular entries refuse rather than being
    written: a symlink can redirect a write out of the destination, and a
    gitlink names content this repository does not hold.
    """
    entries = _tree_entries(commit, repo=repo)
    irregular = [(m, rel) for m, _s, rel in entries if m not in _REGULAR_MODES]
    if irregular:
        raise PreflightError(
            f"the tree of {commit[:12]} holds {len(irregular)} non-regular "
            f"entr(ies) -- e.g. {irregular[:3]} -- and materializing a symlink "
            f"or gitlink is refused rather than followed")
    dest = Path(tempfile.mkdtemp(prefix="cairn-raw-tree-"))
    try:
        blobs = _batch_blobs([sha for _m, sha, _rel in entries], repo=repo)
        root = dest.resolve()
        for (mode, _sha, rel), data in zip(entries, blobs):
            target = (dest / rel)
            if rel.startswith("/") or ".." in Path(rel).parts or \
                    root not in target.resolve().parents:
                raise PreflightError(
                    f"tree entry {rel!r} escapes the destination directory")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            if mode == "100755":
                target.chmod(0o755)
        yield dest
    finally:
        shutil.rmtree(dest, ignore_errors=True)


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
    # Resolve the epoch explicitly, and prove it sits on the history being
    # blessed, BEFORE enumerating anything (first-use review FUR4). Two distinct
    # failures hid behind the old implicit use of the raw constant:
    #   * absent object -- the epoch range came back empty via the fail-open
    #     `_rev_list`, so every commit read as grandfathered and `checked` was 0;
    #   * present but off the HEAD line -- "at or after the epoch" then names no
    #     range on the history under consideration, and the intersection below is
    #     empty for a reason that has nothing to do with the commits being safe.
    # Resolving also normalises the constant to a full SHA, so it compares
    # against `rev-list` output rather than relying on the literal being 40 hex.
    try:
        epoch = _resolve(_SIGNING_EPOCH, repo=repo)
    except PreflightError as exc:
        report.add("SIGNING", "refuse",
                   f"the signing epoch {_SIGNING_EPOCH[:12]} is not present in "
                   f"this repository ({exc}); the grandfathered range cannot be "
                   f"established, so no commit can be shown to be exempt")
        report.facts["signing"] = {"epoch": _SIGNING_EPOCH, "resolved": None}
        return
    if not _is_ancestor(epoch, head, repo=repo):
        report.add("SIGNING", "refuse",
                   f"the signing epoch {epoch[:12]} is not an ancestor of HEAD "
                   f"{head[:12]}; 'at or after the epoch' names no range on the "
                   f"history being blessed")
        report.facts["signing"] = {"epoch": _SIGNING_EPOCH, "resolved": epoch,
                                   "ancestor_of_head": False}
        return

    blessed = set(_rev_list(f"{anchor}..{head}", repo=repo))
    post_epoch = set(_rev_list(f"{epoch}..{head}", repo=repo))
    post_epoch.add(epoch)
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
        "resolved": epoch,
        "ancestor_of_head": True,
        "commits_in_range": len(blessed),
        "checked": len(to_check),
        "grandfathered": len(blessed - post_epoch),
        "principals": sorted(principals),
    }


def _rev_list(spec: str, *, repo: Path = _REPO) -> list[str]:
    """Enumerate commits, or raise. It **never** reports failure as emptiness.

    This used to ``return []`` on any git error, which silently converted "the
    signed range cannot be established" into "there is nothing to check". With
    the signing-epoch object absent -- a shallow or partial clone is enough --
    an unsigned commit inside ``anchor..HEAD`` was reported as *grandfathered*
    and :func:`check_signatures` emitted no finding at all (first-use review
    FUR4). An unestablishable range is not an empty one.
    """
    p = _git("rev-list", spec, repo=repo)
    if p.returncode != 0:
        raise PreflightError(
            f"could not enumerate commits for {spec!r}: "
            f"{(p.stderr or '').strip()!r} -- refusing rather than treating an "
            f"unestablishable range as empty")
    return [s for s in (p.stdout or "").split() if s]


def _is_ancestor(ancestor: str, descendant: str, *, repo: Path = _REPO) -> bool:
    """True iff ``ancestor`` is an ancestor of ``descendant``.

    ``merge-base --is-ancestor`` has *three* outcomes, not two: 0 yes, 1 no, and
    anything else a genuine error. Collapsing the third into "no" would be the
    same fail-open shape :func:`_rev_list` just lost.
    """
    p = _git("merge-base", "--is-ancestor", "--end-of-options",
             ancestor, descendant, repo=repo)
    if p.returncode not in (0, 1):
        raise PreflightError(
            f"could not decide whether {ancestor[:12]} is an ancestor of "
            f"{descendant[:12]}: {(p.stderr or '').strip()!r}")
    return p.returncode == 0


# --------------------------------------------------------------------------
# the canonical range-review report (Chunk B; proposal Revision 1, R1-A)
# --------------------------------------------------------------------------
#
# `_SIGNING_EPOCH` refused a ceremony whose range carried unsigned intermediate
# commits.  That control was *candidate-editable* -- the epoch lives in this
# file's own bytes -- and it blocked the ordinary agent-commit workflow, so
# operations disabled it.  A control the real workflow contradicts is not a
# control.
#
# The replacement is not three counts.  It is one **canonical, digest-bound
# report** of the exact state being authorized: every changed path from the
# anchor tree to the candidate tree, each in exactly one class, with the
# complete sorted list per class.  The Maintainer signs a checkpoint whose
# message carries that digest, so the signature binds the *reviewed report*,
# not merely the tip commit.
#
# It does not claim every intermediate commit was reviewed.  It makes the state
# being authorized bounded and inspectable.  Signature counts travel as
# **diagnostics**, never as an authorization verdict.

RANGE_REPORT_SCHEMA = "cairn-range-review/v1"

#: Exhaustive and mutually exclusive by construction.  A path in none of the
#: first four is `outside-coverage`, reported **in full** rather than counted:
#: "how many paths nobody classified" is not something a Maintainer can review.
_RANGE_CLASSES = ("frozen", "cascade-mutable", "phase-mutable",
                  "manifest-artifact", "outside-coverage")


def _display_path(raw: bytes) -> str:
    """A deterministic ASCII-only rendering of a raw path.

    Git path identity is **raw bytes**.  Every decoding step -- locale,
    filesystem encoding, `core.quotePath`, a terminal -- is a place two
    different paths can render alike, so the report binds the bytes and carries
    this only for a human to read.
    """
    out = []
    for b in raw:
        if 0x20 <= b < 0x7F and b != 0x5C:
            out.append(chr(b))
        else:
            out.append("\\x%02x" % b)
    return "".join(out)


def _verify_display(raw: bytes, display: str) -> None:
    """Refuse a report whose display is not a pure rendering of its bytes."""
    if _display_path(raw) != display:
        raise PreflightError(
            "range-report display is not a rendering of the bound bytes: "
            f"{display!r}")


def _resolve_tree(ref: str, *, repo: Path = _REPO) -> str:
    """The tree id of *ref*, validated at the repository's own id width."""
    p = _git("rev-parse", "--verify", "--end-of-options", f"{ref}^{{tree}}",
             repo=repo)
    tree = (p.stdout or "").strip()
    if p.returncode != 0 or len(tree) != _object_id_width(repo=repo) or any(
            c not in "0123456789abcdef" for c in tree):
        raise PreflightError(
            f"ref does not resolve to a tree: {ref!r} "
            f"({(p.stderr or '').strip()})")
    return tree


def _changed_paths(anchor_tree: str, candidate_tree: str, *,
                   repo: Path = _REPO) -> list[bytes]:
    """Raw changed paths between two exact trees.

    The option set is fixed and load-bearing: `--no-renames` so a rename cannot
    collapse an add and a delete into one entry the classifier never sees; `-z`
    so a path containing a newline cannot forge a record boundary.
    """
    p = _git("diff-tree", "-r", "--no-commit-id", "--name-only", "-z",
             "--no-renames", anchor_tree, candidate_tree,
             repo=repo, want_bytes=True)
    if p.returncode != 0:
        raise PreflightError(
            f"could not enumerate {anchor_tree}..{candidate_tree}: "
            f"{os.fsdecode(p.stderr or b'').strip()}")
    return [tok for tok in (p.stdout or b"").split(b"\0") if tok]


def _classify_path(rel: str, frozen: set, cascade: set, phase: set,
                   manifest_rel: str) -> str:
    """Exactly one class per path, from the **manifest's** own policy.

    B6: the source is `_gate_manifest`'s -- `_frozen_files()` plus the mutable
    registries plus the manifest artifact -- not a second definition here.  A
    report that partitions perfectly but disagrees with the policy that later
    decides HOLD would bind a misdescription with a perfect digest.
    """
    hits = [name for name, member in (
        ("manifest-artifact", rel == manifest_rel),
        ("cascade-mutable", rel in cascade),
        ("phase-mutable", rel in phase),
        ("frozen", rel in frozen),
    ) if member]
    if len(hits) > 1:
        raise PreflightError(f"path is multiply classified {hits!r}: {rel!r}")
    return hits[0] if hits else "outside-coverage"


def _signature_census(anchor: str, head: str, *, repo: Path = _REPO) -> dict:
    """Signed / unsigned / foreign-signed counts -- **diagnostics only**.

    Deliberately not a verdict.  Unsigned intermediate commits are the normal
    agent-work format under R1-A; the authorization is the Maintainer's
    signature on the checkpoint, not a property of the range.
    """
    p = _git("log", "--format=%G?", f"{anchor}..{head}", repo=repo)
    if p.returncode != 0:
        raise PreflightError(
            f"could not census signatures over {anchor}..{head}: "
            f"{(p.stderr or '').strip()}")
    codes = [ln.strip() for ln in (p.stdout or "").splitlines() if ln.strip()]
    return {
        "total": len(codes),
        "good": sum(1 for c in codes if c == "G"),
        "unsigned": sum(1 for c in codes if c == "N"),
        "other": sum(1 for c in codes if c not in ("G", "N")),
    }


def range_review_report(anchor: str, head: str, *, branch: str,
                        expected_old: str, repo: Path = _REPO) -> dict:
    """The one canonical report `apply` re-derives and the checkpoint binds."""
    frozen = set(G._frozen_files(repo))
    cascade = set(G.CASCADE_MUTABLE)
    phase = set(G.PHASE_SPLIT_TARGETS)
    manifest_rel = G._MANIFEST_REL

    anchor_tree = _resolve_tree(anchor, repo=repo)
    candidate_tree = _resolve_tree(head, repo=repo)

    entries: list[dict] = []
    seen: set = set()
    for raw in _changed_paths(anchor_tree, candidate_tree, repo=repo):
        if raw in seen:
            raise PreflightError(
                f"duplicate path in the changed set: {_display_path(raw)!r}")
        seen.add(raw)
        rel = raw.decode("utf-8", errors="surrogateescape")
        display = _display_path(raw)
        _verify_display(raw, display)
        entries.append({
            "bytes_b64": base64.b64encode(raw).decode("ascii"),
            "display": display,
            "class": _classify_path(rel, frozen, cascade, phase, manifest_rel),
        })

    # Ordering is by RAW BYTES, never the display or a decoded string: two
    # distinct byte sequences can render alike, and a digest over a
    # locale-dependent order is not canonical.
    entries.sort(key=lambda e: base64.b64decode(e["bytes_b64"]))

    by_class = {name: [e["display"] for e in entries if e["class"] == name]
                for name in _RANGE_CLASSES}
    manifest_bytes = (repo / manifest_rel).read_bytes()

    return {
        "schema": RANGE_REPORT_SCHEMA,
        "anchor": anchor,
        "candidate_head": head,
        "anchor_tree": anchor_tree,
        "candidate_tree": candidate_tree,
        "branch": branch,
        "expected_old": expected_old,
        "manifest_schema": G.SCHEMA,
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "paths": entries,
        "by_class": by_class,
        "counts": {name: len(by_class[name]) for name in _RANGE_CLASSES},
        "signatures": _signature_census(anchor, head, repo=repo),
    }


def range_report_digest(report: dict) -> str:
    """SHA-256 over the canonical JSON form.

    `sort_keys` + no whitespace + ASCII-only: the digest must not move because
    a dict was built in a different order or a path rendered under a different
    locale.
    """
    blob = json.dumps(report, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")
    return hashlib.sha256(blob).hexdigest()


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
  trust root, single-maintainer, as of 2026-08-03).
  AUTHORITY -- named exactly, because a blanket "NON-AUTHORITATIVE" was too
  strong: `check` re-derives every STATIC manifest field itself from raw commit
  objects and refuses on any difference. What this stage alone can supply, and
  what therefore remains trusted to it, is the pytest COLLECTION (and the
  interpreter it ran under) -- a suite cannot be collected from object bytes.
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

    # Materialized from raw objects, not `git archive`: the archive path honours
    # in-tree `.gitattributes`, so a tracked file marked `export-ignore` was
    # invisible to the producer while remaining in the blessed tree (FUR3).
    with raw_tree(candidate, repo=repo) as tree:
        out.write(f"materialized {candidate[:12]} at {tree} "
                  f"(no .git, raw objects)\n")
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

    v = sys.version_info
    body = json.dumps(manifest, indent=2, sort_keys=True).encode() + b"\n"
    return {
        "schema": EVIDENCE_SCHEMA,
        "candidate_sha": candidate,
        "interpreter": f"{v.major}.{v.minor}.{v.micro}",
        "manifest": manifest,
        "manifest_sha256": _sha256_bytes(body),
    }


#: Manifest fields that need the suite to *run*, and so are irreducibly the
#: evidence stage's to report. Everything else is re-derived by
#: :func:`rederive_static_manifest` and compared.
_EXECUTABLE_ONLY_FIELDS = frozenset({"collection", "interpreter"})

#: Fields the CHECKER derives and never compares against the candidate.
#: `produce` runs from a raw tree with no repository, so it cannot supply
#: these -- and the trusted side deriving them is the stronger arrangement.
_CHECKER_DERIVED_FIELDS = frozenset({"object_format"})

#: Git-native identity *inside* an entry.  Same rule, one level down: the
#: candidate produces its manifest from a raw tree with no repository, so it
#: cannot supply these -- and the trusted side deriving them means a candidate
#: cannot assert its own file modes or object ids.
_CHECKER_DERIVED_SUBKEYS = frozenset({"mode", "oid"})


def _candidate_comparable(value):
    """Strip checker-derived sub-keys so like is compared with like."""
    if not isinstance(value, dict):
        return value
    out = {}
    for k, v in value.items():
        if isinstance(v, dict):
            out[k] = {sk: sv for sk, sv in v.items()
                      if sk not in _CHECKER_DERIVED_SUBKEYS}
        elif isinstance(v, str):
            out[k] = v
        else:
            out[k] = v
    return out


def rederive_static_manifest(commit: str, *, repo: Path = _REPO) -> dict:
    """Recompute every statically derivable manifest field, independently.

    The evidence stage was labelled wholly "NON-AUTHORITATIVE" while ``check``
    validated only the candidate SHA, an adjacent digest, and the interpreter --
    so *file identity* was in fact delegated to a manifest the candidate's own
    process produced. A signed candidate that added a tracked module under the
    frozen directory and a ``.gitattributes`` marking it ``export-ignore`` got a
    commit blessed whose tree held the file while its manifest did not pin it
    (FUR3). The archive hole is closed in :func:`raw_tree`; this closes the
    delegation.

    Two deliberate choices. The tree is materialized from **raw objects**, so
    the bytes hashed here are the ones the commit actually carries. And the
    field derivations reuse ``_gate_manifest``'s own implementation rather than
    reimplementing its glob semantics -- that module is authority-closure
    covered and compared against the anchor, and a second copy of the globbing
    rules would drift into false refusals the first time either side changed.

    Only :data:`_EXECUTABLE_ONLY_FIELDS` are left to the candidate: a pytest
    collection cannot be derived from object bytes, which is exactly why the
    evidence stage exists.
    """
    # v2 shape.  Mode and oid come from the commit's tree via Git; SHA-256 is
    # computed here over the **materialized raw bytes** -- so the two halves are
    # derived by different means over the same object, which is the point of
    # this function existing at all.  A `raw_tree` directory is not a git
    # repository, so the oids cannot come from it.
    blobs = G._tree_blobs(repo, commit)
    object_format = G._object_format(repo)
    with raw_tree(commit, repo=repo) as tree:
        frozen = {}
        for rel in G._frozen_files(tree):
            mode_oid = blobs.get(rel)
            if mode_oid is None:
                # Unreachable in practice: a raw tree holds only tracked files.
                continue
            frozen[rel] = {"sha256": G._sha256(tree / rel),
                           "mode": mode_oid[0], "oid": mode_oid[1]}
        cascade = {
            rel: {"pre_run_sha256": G._sha256(tree / rel), "governed_by": why,
                  "mode": blobs.get(rel, (None, None))[0],
                  "oid": blobs.get(rel, (None, None))[1]}
            for rel, why in sorted(G.CASCADE_MUTABLE.items())
            if (tree / rel).is_file()
        }
        phase_mutable = {
            rel: {"pre_run_sha256": G._sha256(tree / rel), "governed_by": why,
                  "mode": blobs.get(rel, (None, None))[0],
                  "oid": blobs.get(rel, (None, None))[1]}
            for rel, why in sorted(G.PHASE_SPLIT_TARGETS.items())
            if (tree / rel).is_file()
        }
        baseline_rel = "bootstrap/tests/fixtures/scaffold_ast_baseline.json"
        try:
            baseline = json.loads(
                (tree / baseline_rel).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise PreflightError(
                f"cannot re-derive the mapping digests: {baseline_rel} is "
                f"unreadable in the raw tree of {commit[:12]} ({exc})") from None
        mappings = {}
        for sym, phases in G.MAPPING_SYMBOLS_PHASES.items():
            entry = baseline.get(f"Assign:{sym}")
            if entry is None:
                raise PreflightError(
                    f"mapping symbol Assign:{sym} is absent from the anchored "
                    f"AST baseline; the manifest cannot be re-derived")
            mappings[sym] = {"baseline_digest": entry["digest"],
                             "may_change_in_phases": phases}
    return {
        "schema": G.SCHEMA,
        "object_format": object_format,
        # `untracked_gate_files` is deliberately NOT re-derived. A `raw_tree`
        # contains only tracked files by construction, so the re-derivation
        # would always compute `[]` and every candidate carrying a real entry
        # would be refused for a difference that is an artifact of how the two
        # sides read the tree, not a disagreement about it. It is diagnostic
        # output from `produce`, not a statically verifiable field.
        "gate_commands": G.GATE_COMMANDS,
        "frozen_files": frozen,
        "cascade_mutable": cascade,
        "phase_mutable": phase_mutable,
        "mapping_symbols": mappings,
    }


def check_static_manifest(evidence: dict, head: str, report: Report, *,
                          repo: Path = _REPO) -> None:
    """Compare the candidate's manifest against the independent re-derivation."""
    ours = rederive_static_manifest(head, repo=repo)
    theirs = evidence.get("manifest") or {}
    for field, expected in sorted(ours.items()):
        got = theirs.get(field)
        if field in _CHECKER_DERIVED_FIELDS:
            # Git-native identity is derived HERE and never accepted from the
            # candidate: the evidence stage runs `produce` from a materialized
            # raw tree with no repository, so it has no oids to offer and must
            # not be trusted with any it did offer.
            continue
        if field == "frozen_files":
            # The candidate supplies content digests; compare exactly those.
            expected = {rel: (e["sha256"] if isinstance(e, dict) else e)
                        for rel, e in expected.items()}
            got = {rel: (e["sha256"] if isinstance(e, dict) else e)
                   for rel, e in (got or {}).items()}
        elif field in ("cascade_mutable", "phase_mutable"):
            expected = _candidate_comparable(expected)
            got = _candidate_comparable(got or {})
        if got == expected:
            continue
        detail = f"field {field!r} differs from the independent re-derivation"
        if isinstance(expected, dict) and isinstance(got, dict):
            missing = sorted(set(expected) - set(got))
            extra = sorted(set(got) - set(expected))
            changed = sorted(k for k in set(expected) & set(got)
                             if expected[k] != got[k])
            detail += (f" -- {len(missing)} missing, {len(extra)} unexpected, "
                       f"{len(changed)} altered")
            for label, items in (("missing", missing), ("unexpected", extra),
                                 ("altered", changed)):
                if items:
                    detail += f"; {label}: {items[:5]}"
        report.add("MANIFEST", "refuse", detail)
    report.facts["static_manifest"] = {
        "rederived_fields": sorted(ours),
        "trusted_to_the_evidence_stage": sorted(_EXECUTABLE_ONLY_FIELDS),
        "frozen_files_rederived": len(ours["frozen_files"]),
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
    # **No repository probe here, deliberately.**  This validates the *shape* of
    # an id recorded in an evidence file, not one resolved against a repository:
    # Stage-B runs from an extracted directory that is not a git repository at
    # all, so probing would refuse the ceremony for lack of a `.git`.  Accept
    # any legal object-id width; the repo-bound checks in `_resolve` and after
    # `commit-tree` are where the format is authoritative.
    if len(sha) not in _OBJECT_FORMAT_WIDTH.values() or any(
            c not in "0123456789abcdef" for c in sha):
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
    # `add` was here and is deliberately gone: it re-reads the worktree through
    # any configured `clean` filter, putting a candidate-controlled transform
    # between the verified bytes and the index (FUR2). The sync installs the
    # already-verified blob by id via `update-index --cacheinfo`, so removing
    # the subcommand makes the filtered path unreachable rather than unused.
})


def draft_message(*, observed_anchor: str, checked_head: str,
                  manifest_sha256: str, authority_hashes: dict,
                  scope: dict, last_legitimate_anchor: str | None = None,
                  erroneous_ref: str | None = None,
                  range_report_digest: str | None = None,
                  candidate_tree: str | None = None) -> str:
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
  candidate tree      : {candidate_tree or '(not bound)'}
  range-report digest : {range_report_digest or '(not bound)'}
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


# --- Chunk C: the checkpoint binds the reviewed report ---------------------


class RangeReportDrift(PreflightError):
    """The report changed between review and construction."""


def rederive_and_bind(anchor: str, head: str, *, branch: str,
                      expected_old: str, confirmed_digest: str,
                      repo: Path = _REPO) -> dict:
    """Re-derive the report **in memory** and refuse any drift.

    R1-A: `apply` neither reads nor trusts a handoff file.  The report the
    Maintainer confirmed is named by digest; this recomputes it from the same
    exact refs immediately before construction and compares.  A handoff artifact
    would be a second place the authorized state could be edited between the
    confirmation and the signature.

    Any ref, tree, manifest, path set, classification or report-byte drift
    invalidates the confirmation and requires a fresh derivation.
    """
    fresh = range_review_report(anchor, head, branch=branch,
                                expected_old=expected_old, repo=repo)
    actual = range_report_digest(fresh)
    if actual != confirmed_digest:
        raise RangeReportDrift(
            "the range-review report changed between confirmation and "
            f"construction: confirmed {confirmed_digest}, re-derived {actual}. "
            "Re-run the review; the confirmation is void.")
    return fresh


def verify_message_binds_report(message: str, *, digest: str, tree: str,
                                head: str, anchor: str) -> None:
    """Check a **drafted** message carries every binding field, before signing.

    Deliberately *not* a second object read-back: `verify_constructed` below
    already re-parses the commit and compares the **exact** message, which is
    strictly stronger than looking for substrings. This runs earlier, on the
    draft, so a `draft_message` regression is caught before a commit is
    constructed and signed rather than after -- at which point the only remedy
    is to throw the signature away.
    """
    missing = [label for label, value in (
        ("range-report digest", digest),
        ("candidate tree", tree),
        ("checked HEAD", head),
        ("superseded anchor", anchor),
    ) if value not in message]
    if missing:
        raise PreflightError(
            f"drafted checkpoint message does not bind: {', '.join(missing)}. "
            f"Refusing before construction.")


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
               want_bytes: bool = False,
               index: str | None = None) -> subprocess.CompletedProcess:
    """The **only** repository-writing path, with its own enumerated allowlist.

    Routed through :func:`_run_git` since FUR1/FUR2. Before that it called
    ``subprocess`` directly with **no config pinning at all**, so the write path
    -- the one that signs the commit and moves the trust root -- was the *least*
    protected in the module: ``gpg.ssh.program`` chose the verifier and a
    ``reference-transaction`` hook could move a third ref during the very
    transaction whose two-ref atomicity was the claim.

    ``index`` supplies ``GIT_INDEX_FILE`` for this invocation only, replacing a
    mutate-and-restore of ``os.environ`` that leaked the temporary index into
    every other subprocess started while it was set.
    """
    if not args or args[0] not in _WRITE_GIT:
        raise PreflightError(
            f"apply may only run {sorted(_WRITE_GIT)}; refused "
            f"{(args[0] if args else '<none>')!r}")
    return _run_git(args, repo=repo, stdin=stdin, want_bytes=want_bytes,
                    index=index)


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

        # GIT_INDEX_FILE is threaded per invocation rather than exported into
        # this process: mutating os.environ leaked the temporary index into
        # every unrelated subprocess started while it was set, and left the
        # correctness of the restore load-bearing.
        def g(*args, **kw):
            kw.setdefault("repo", repo)
            kw.setdefault("index", idx)
            return _git_write(*args, **kw)

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
        if ct.returncode != 0 or len(new) != _object_id_width(repo=repo):
            raise PreflightError(
                f"commit-tree failed (is signing configured?): "
                f"{ct.stderr.strip()}")
        # The blob id travels with the commit id so the index sync can install
        # it directly rather than re-deriving it from the worktree through a
        # filter (FUR2).
        return new, blob


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
    # `--create-reflog` with a fixed reason: custom refs carry no reflog by
    # default, which is how a mis-set anchor once became unrecoverable -- the
    # prior value simply was not written down anywhere.
    #
    # A reflog is a **local, mutable diagnostic** for recovery and sequencing.
    # It is never tamper evidence and never authentication: anyone who can write
    # the ref can write its reflog. No decision predicate in this module reads
    # reflog content, and none may.
    p = _git_write("update-ref", "--no-deref", "--create-reflog", "--stdin",
                   repo=repo, stdin=stdin)
    return p.returncode == 0, (p.stderr or p.stdout or "").strip()


def _sync_worktree(repo: Path, manifest_bytes: bytes, blob: str) -> None:
    """Bring the real index and worktree in line with the new HEAD.

    Construction uses a temporary index, so before this the real index and
    worktree still carry the pre-blessing blob and ``git status`` reports the
    manifest as staged against the new trust root -- an immediate dirty state and
    a staged rollback waiting to ride a later commit (code review CR3). Because
    construction touched neither, an aborted transaction leaves **no** residue at
    all, which is stronger than reporting one.

    The index entry is installed **directly**, from the blob id already written
    and already verified inside the blessed commit. It used to go through ``git
    add``, which re-reads the worktree file through any configured ``clean``
    filter -- a candidate-controlled transform standing between the bytes that
    were verified and the bytes that land in the index (FUR2). ``update-index
    --cacheinfo`` names the object outright, so no filter is in the path.
    """
    (repo / _MANIFEST_REL).write_bytes(manifest_bytes)
    ui = _git_write("update-index", "--add", "--cacheinfo",
                    f"100644,{blob},{_MANIFEST_REL}", repo=repo)
    if ui.returncode != 0:
        raise PreflightError(
            f"the refs advanced but the worktree/index sync failed: "
            f"{ui.stderr.strip()} -- the repository is left with the manifest "
            f"unstaged; reconcile before committing anything else")
    # --cacheinfo writes the entry without stat information, so the file reads
    # as modified until the cache is refreshed. Without this `git status` is
    # dirty immediately after a successful blessing.
    _git_write("update-index", "--refresh", repo=repo)


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
    # Re-validated here and not only at the CLI boundary: this is the one
    # function that moves the trust root, so the repository it moves must be the
    # one the caller named, not one git discovered by walking upward (FUR5).
    repo = _require_worktree_root(repo)

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
        new, manifest_blob = _construct_signed_commit(
            repo, head, manifest_bytes, plan["message"])
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
    _sync_worktree(repo, manifest_bytes, manifest_blob)
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
        check_static_manifest(evidence, head, report, repo=repo)
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
    _REPO_HELP = ("the checkout to operate on. REQUIRED for the anchored\n"
                  "invocation: the checker runs from a temp extraction\n"
                  "directory there, so its own location is not the target.")
    c.add_argument("--repo", default=None, help=_REPO_HELP)
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
    e.add_argument("--repo", default=None, help=_REPO_HELP)
    e.add_argument("--candidate-ref", default="HEAD")
    e.add_argument("-o", "--output", default=None,
                   help="write the artifact here (default: stdout)")
    a = sub.add_parser(
        "apply",
        help="revalidate a bundle, construct and verify the commit, then move "
             "the branch and gate anchor in ONE transaction -- Maintainer-only")
    a.add_argument("--repo", default=None, help=_REPO_HELP)
    a.add_argument("--confirm-supervised-reanchor", action="store_true",
                   dest="confirmed",
                   help="required; this is the only step that moves the trust "
                        "root")
    args = ap.parse_args(argv)

    try:
        repo = _require_worktree_root(Path(args.repo) if args.repo else _REPO)
    except PreflightError as exc:
        sys.stderr.write(f"[REFUSE ] {exc}\n")
        return 2

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
