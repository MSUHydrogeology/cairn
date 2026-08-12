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
expiry tripwire is the **checkpoint** signature -- verified against the anchored
roster in :func:`apply_now`, not a per-commit census over the range, which
:func:`check_signatures` records as retired. It authenticates the **key
holder** -- not the human, and not the process. Every agent operating on this
machine commits as the Maintainer and signs with the Maintainer's key, so this
detects a second *person*, not a second *process*.
"""
from __future__ import annotations

import argparse
import contextlib
import base64
import hashlib
import json
import os
import shutil
import stat
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

#: The one reflog reason every gate-anchor transaction writes, on **both** refs.
#: Fixed here rather than passed in, so a ceremony cannot be mislabelled. Read
#: by operators recovering a prior value; read by **no** decision predicate.
_CEREMONY_REFLOG_REASON = "cairn: supervised gate re-anchor"

_MANIFEST_REL = "bootstrap/tests/fixtures/gate_manifest.json"
_RUNBOOK_REL = "bootstrap/REANCHOR_RUNBOOK.md"
_ALLOWED_SIGNERS_REL = "dev/.cairn/allowed_signers"

#: **There is deliberately no signing epoch here.** A `_SIGNING_EPOCH` constant
#: used to sit at this line and decide which commits were exempt from a
#: per-commit signature requirement. It was retired by Chunk B of plan
#: `git-native-security-foundations`, and the absence is load-bearing rather
#: than incidental: the constant lived in the checker's own bytes, *inside the
#: tree being blessed*, so a candidate could move it to grandfather its own
#: unsigned commits. The old comment argued the authority closure caught that;
#: it catches the edit, not the design -- an epoch a candidate can name at all
#: is a self-grandfathering surface, so the fix is that no epoch exists.
#: See :func:`check_signatures` for where authorization actually lives now.

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
    # Security review [S1]. `gpg.ssh.defaultKeyCommand` names a program Git runs
    # to obtain a signing key when `user.signingKey` is unset -- so a repository
    # under candidate control could name a script and have Git EXECUTE it, in
    # stage 2, after `seal_candidate_execution`. Reproduced: the script ran and
    # wrote a marker; construction then failed on the invalid key it returned,
    # but the execution had already happened. Pinned empty, alongside the
    # selector itself (`user.signingKey`, set per-invocation at the one call
    # site that signs).
    "gpg.ssh.defaultKeyCommand": "",
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
    # Security review [M2-4]. `_READ_ONLY_GIT` keeps content- and ref-writing
    # subcommands behind `_git_write`, but "read-only" was a claim about
    # subcommands, not about the repository: `git status` refreshes cached stat
    # data through an *optional* index lock, so a public `check` changed
    # `.git/index` bytes and mtime while leaving the worktree clean. Measured,
    # not theorised. Optional locks off makes the read boundary read-only in
    # fact; git skips the refresh write rather than failing.
    env["GIT_OPTIONAL_LOCKS"] = "0"
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


#: The key-load phase boundary (proposal R1-F steps 4-5; acceptance criterion 8).
#:
#: The ceremony runs in two phases and the order is the whole protection. While
#: the signing key is unavailable, candidate code runs freely -- pytest
#: collection, the candidate's own manifest producer, every candidate-executing
#: check. The Maintainer then confirms against a hard marker, and only then is
#: the key loaded. After that point **no candidate code may execute or be
#: imported**, because a key that is loadable while candidate code runs is a key
#: that candidate code may be able to use.
#:
#: This is a *sequencing* control, not containment, and the plan says so
#: plainly: candidate code that ran earlier on the same uncompartmented machine
#: may have left persistence that a later signing process cannot detect. What
#: the boundary removes is **simultaneous intentional availability**. A separate
#: evidence host or a hardware-presence key is the strengthening path, and
#: neither exists today.
_PHASE_CANDIDATE = "candidate-execution-permitted"
_PHASE_SEALED = "sealed-key-may-load"

#: Module state, not a parameter, deliberately: every candidate-executing entry
#: point must observe the same boundary without the caller having to thread it,
#: and a caller-supplied phase could simply be passed as "not sealed".
_phase = _PHASE_CANDIDATE


def seal_candidate_execution(*, out=sys.stderr) -> None:
    """Cross the key-load boundary. Irreversible within a process.

    There is deliberately **no unseal**. A reversible boundary is not a
    boundary: the failure this exists to prevent is precisely a later stage
    deciding it needs one more collection.
    """
    global _phase
    _phase = _PHASE_SEALED
    out.write(
        "\n=== KEY-LOAD PHASE MARKER ==========================================\n"
        "Candidate execution is now SEALED. No operation after this point may\n"
        "execute or import candidate code -- not collection, not imports, not\n"
        "hooks or filters, not a subprocess. The signing key may now load.\n"
        "This is sequencing, NOT containment: code that ran before this line\n"
        "shared this machine with the key that is about to load.\n"
        "====================================================================\n")


def refuse_if_sealed(operation: str) -> None:
    """Guard every candidate-executing entry point.

    Named operations rather than a bare flag check, so the refusal says *what*
    tried to cross rather than only that something did.
    """
    if _phase == _PHASE_SEALED:
        raise PreflightError(
            f"{operation} would execute or import candidate code after the "
            f"key-load phase marker; refusing. The ceremony seals candidate "
            f"execution before the signing key loads, and that boundary does "
            f"not reopen")


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


def _sha256_hex(data: bytes) -> str:
    """Bare lowercase hex -- the review manifest's digest format.

    Kept distinct from :func:`_sha256_bytes` rather than stripping its prefix at
    each site. The manifest's rows are produced by `shasum -a 256` in the fixed
    loader and parsed under A3's "64 lowercase hex digits" rule, so bare hex is
    that artifact's format and the prefixed form is this module's internal one.
    Comparing across the two silently never matches, which is exactly what
    `revalidate_transition` did to every member it checked.
    """
    return hashlib.sha256(data).hexdigest()


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
                            repo: Path = _REPO,
                            admitted_authority: dict | None = None) -> None:
    """Compare every closure member's working-tree bytes to the anchor's blob.

    Any member changed, missing, extra, symlinked, or absent from the index
    returns ``review`` -- non-zero, no bundle, routed to the manual exact-byte
    procedure. The old anchored checker must not be able to bless a candidate
    that changes its own successor or the next invocation.

    ``admitted_authority`` is the **revalidated** reviewed-authority transition
    set, and it is the one thing that makes a changed member acceptable.

    **Why this parameter has to exist.** Without it the transition was
    unreachable end to end, by construction rather than by accident:
    :func:`revalidate_transition` refuses when the closure is *unchanged*
    ([S3]), and this function refused whenever it *changed*. The two conditions
    are complements, so every real transition died here -- at the checks, with a
    CLOSURE finding -- and the transition machinery Chunks A and B built could
    never run. It is the [M2-1] shape once more: built, unit-tested, and dead to
    the governing path.

    The admission is deliberately narrow. A member is admitted only when its
    **live bytes** hash to the digest the reviewed manifest names *for that
    path*; anything else still returns ``review``. That digest was independently
    checked against the candidate's anchored blob in `revalidate_transition`, so
    two separate bindings have to agree before a byte change passes, and the set
    is written into the checkpoint message (D7) rather than merely consulted.
    """
    admitted = admitted_authority or {}
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
        # Bare hex, to compare against the review manifest's own format.
        live_sha = _sha256_hex(live.read_bytes())
        if anchored is not None and live_sha == _sha256_hex(anchored):
            continue
        # Changed, or new to the closure. Either is admissible ONLY against the
        # revalidated reviewed set, and only byte-for-byte.
        if admitted.get(rel) == live_sha:
            report.add("CLOSURE", "note",
                       f"authority member admitted by the reviewed transition: "
                       f"{rel} ({live_sha[:12]})")
            continue
        if anchored is None:
            report.add("CLOSURE", "review",
                       f"authority member absent from the anchor -- first use "
                       f"requires the manual exact-byte bootstrap: {rel}")
            continue
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
            f"the pinned roster {_ALLOWED_SIGNERS_REL} is absent from the "
            f"anchor {anchor[:12]}. This is a HARD REFUSAL, not a fallback: "
            f"continuity means the OLD anchor's roster verifies a transition, "
            f"and an anchor without one is a distinct bootstrap case requiring "
            f"a separately reviewed Maintainer procedure "
            f"(REANCHOR_RUNBOOK.md > 'Phase 0 transition mode'). Neither the "
            f"candidate's own roster nor the out-of-band review manifest is a "
            f"substitute -- both are the thing being authorized.")
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


REVIEW_MANIFEST_SCHEMA = "cairn-review-manifest/v1"


class ReviewManifestError(PreflightError):
    """The out-of-band review manifest is malformed or does not match."""


def authority_closure_delta(anchor: str, candidate: str, *,
                            repo: Path = _REPO) -> dict[str, tuple]:
    """Which authority-closure members differ between anchor and candidate.

    The transition exists **because** the closure changed. With no delta there
    is nothing for an external review to have reviewed, and running the mode
    anyway would make it a flag rather than a ceremony -- plan finding [S3].
    """
    delta: dict[str, tuple] = {}
    for rel in sorted(declared_authority_closure()):
        old = _blob_at(anchor, rel, repo=repo)
        new = _blob_at(candidate, rel, repo=repo)
        if old != new:
            delta[rel] = (None if old is None else _sha256_bytes(old),
                          None if new is None else _sha256_bytes(new))
    return delta


def parse_review_manifest(text: str) -> dict:
    """Re-parse the Maintainer's out-of-band review manifest.

    **This is defence in depth and never the establishing control.** The
    complete source-selection predicate lives in the fixed loader
    (`REANCHOR_RUNBOOK.md`, *Phase 0 transition mode*), which runs *before* any
    Python — including this function — exists in the process. By the time this
    executes, the bytes it would judge have already been selected and are
    already running. Plan review finding **[E3]**: a Python re-check cannot
    establish which Python was safe to run.

    It is kept because a second, independent implementation of the same
    predicate catches a loader that was edited to be laxer than its recorded
    text, and because the parsed values are what the checkpoint message binds.
    """
    reviewed_oid = provenance = None
    schema_seen = False
    members: list[tuple[str, str]] = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if any(ch not in "\t" and (ord(ch) < 32 or ord(ch) == 127)
               for ch in raw):
            raise ReviewManifestError("control character in the review manifest")
        # Code review [C4]: the two parsers of this one artifact disagreed here.
        # `raw.split()` ignores leading whitespace, so an indented row was
        # classified by its first word -- but `provenance` is then taken by
        # slicing `raw` at a fixed offset, which on an indented row yields a
        # different string than the loader's `${line#provenance }` produces.
        # Rejecting the row outright is the fix that cannot drift: the format is
        # declared "one concrete, bounded format" (A2), and an indented row is
        # not in it. The loader rejects it identically.
        if raw[:1].isspace():
            raise ReviewManifestError(
                f"review manifest row has leading whitespace: {raw!r}")
        parts = raw.split()
        kind = parts[0]
        if kind == "schema":
            if len(parts) != 2 or parts[1] != REVIEW_MANIFEST_SCHEMA:
                raise ReviewManifestError(f"unknown manifest schema: {raw!r}")
            schema_seen = True
        elif kind == "candidate":
            if reviewed_oid is not None:
                raise ReviewManifestError("duplicate candidate row")
            if len(parts) != 2 or len(parts[1]) not in (40, 64) \
                    or any(c not in "0123456789abcdef" for c in parts[1]):
                raise ReviewManifestError(f"malformed candidate row: {raw!r}")
            reviewed_oid = parts[1]
        elif kind == "provenance":
            if provenance is not None:
                raise ReviewManifestError("duplicate provenance row")
            provenance = raw[len("provenance "):]
            if not provenance or len(provenance) > 120:
                raise ReviewManifestError("provenance is empty or over 120 chars")
        elif kind == "member":
            if len(parts) != 3 or len(parts[1]) != 64 \
                    or any(c not in "0123456789abcdef" for c in parts[1]):
                raise ReviewManifestError(f"malformed member row: {raw!r}")
            rel = parts[2]
            if rel.startswith("/") or ".." in rel:
                raise ReviewManifestError(f"member path is not relative: {rel!r}")
            members.append((parts[1], rel))
        else:
            raise ReviewManifestError(f"unknown row type {kind!r}")

    if not schema_seen:
        raise ReviewManifestError("no schema row")
    if reviewed_oid is None:
        raise ReviewManifestError("no candidate row")
    if provenance is None:
        raise ReviewManifestError("no provenance row")
    if not members:
        raise ReviewManifestError("no member rows")

    paths = [rel for _, rel in members]
    if paths != sorted(paths):
        raise ReviewManifestError("member paths are not in sorted order")
    if len(set(paths)) != len(paths):
        raise ReviewManifestError("duplicate member paths")

    return {"schema": REVIEW_MANIFEST_SCHEMA, "candidate": reviewed_oid,
            "provenance": provenance, "members": dict(
                (rel, digest) for digest, rel in members)}


def read_review_manifest(path: str | Path) -> tuple[dict, str]:
    """Read the out-of-band review manifest and digest **the file's bytes**.

    The digest is taken here, over the raw bytes, and not inside
    :func:`parse_review_manifest` over a re-encoded string. The Maintainer
    confirms this artifact with `shasum -a 256 <file>`; a digest computed over
    anything but the file's own bytes would be a different number from the one
    they hold, and a provenance value nobody can reproduce is worse than none --
    it reads as verified.

    [E4]/D7: the checkpoint binds this digest, so the durable record names
    *which* review admitted the authority set, not merely that some review did.
    """
    raw = Path(path).read_bytes()
    return parse_review_manifest(raw.decode("utf-8")), _sha256_bytes(raw)


def revalidate_transition(manifest: dict, reviewed_candidate: str, head: str,
                          *, anchor: str, repo: Path = _REPO) -> dict:
    """Re-check the loader's own conclusions. Defence in depth; see above.

    Three facts, each of which the loader already established and each of which
    is cheap to state again from inside: the reviewed candidate is the commit
    being blessed, the declared member set is exactly the authority closure, and
    every member's anchored-candidate bytes hash to the reviewed digest.
    """
    if reviewed_candidate != head:
        raise ReviewManifestError(
            f"the reviewed candidate {reviewed_candidate[:12]} is not the "
            f"commit being blessed ({head[:12]})")
    if manifest["candidate"] != reviewed_candidate:
        raise ReviewManifestError(
            "the review manifest names a different candidate than the loader "
            "resolved")

    delta = authority_closure_delta(anchor, reviewed_candidate, repo=repo)
    if not delta:
        raise ReviewManifestError(
            "the authority closure is identical at the anchor and the "
            "candidate, so there is no reviewed transition to perform. This "
            "mode is not a flag: it exists only to carry a closure change that "
            "an external review has approved. Use the steady-state loader.")

    declared = set(declared_authority_closure())
    named = set(manifest["members"])
    if named != declared:
        missing, extra = sorted(declared - named), sorted(named - declared)
        raise ReviewManifestError(
            f"the review manifest is not the authority closure: "
            f"{len(missing)} missing {missing[:3]}, "
            f"{len(extra)} unexpected {extra[:3]}")

    for rel, expected in sorted(manifest["members"].items()):
        blob = _blob_at(reviewed_candidate, rel, repo=repo)
        if blob is None:
            raise ReviewManifestError(f"candidate has no blob at {rel}")
        # Bare hex on both sides: the manifest's rows come from `shasum -a 256`.
        actual = _sha256_hex(blob)
        if actual != expected:
            raise ReviewManifestError(
                f"{rel} is {actual[:12]} in the candidate, review manifest "
                f"names {expected[:12]}")
    return manifest


def check_signatures(anchor: str, head: str, report: Report, *,
                     repo: Path = _REPO) -> None:
    """**Retired.** Kept as an explicit no-op record, not as a check.

    This used to refuse any commit at or after a `_SIGNING_EPOCH` constant that
    was not signed by a pinned key. Chunk B retired both, and the retirement is
    the *point* rather than a relaxation:

    * The epoch was **candidate-editable** -- it lived in this file's own bytes,
      inside the tree being blessed -- so a candidate could move the line that
      decided which of its commits were exempt. That is self-grandfathering, and
      renaming the constant would not have removed it.
    * It **contradicted the real workflow.** Unsigned agent commits are the
      normal format (proposal R1-A); a range check refusing them refuses every
      ordinary ceremony, so operations disable it, and a control that is
      routinely disabled is not a control.

    Authorization now happens in exactly one place: the Maintainer's signature
    on a checkpoint whose message binds the canonical range-review report digest
    (:func:`range_review_report`). That says *which state* was authorized, which
    is the question a per-commit signature census never answered. The census
    itself survives as **diagnostics** inside the report
    (:func:`_signature_census`) and is never a verdict.

    What it still does is **report the census**, and that is deliberate rather
    than vestigial. Retiring a verdict must not retire the information: `check`
    is the preview a Maintainer reads before authorizing, and dropping the
    counts outright would have left that preview silent about signatures
    altogether. `range_review_report` carries the same census into the digest a
    checkpoint binds; this is the human-facing half.

    The function stays so this docstring stays: the reasoning above is the sort
    that gets silently re-litigated into a "restored" check by a later reader who
    finds an absence and assumes an oversight.
    """
    report.facts["signing"] = {
        "epoch": None,
        "retired": "Chunk B -- authorization is the signed checkpoint binding "
                   "the range-report digest; see the docstring",
        # Diagnostics. Never read by a decision predicate, and deliberately not
        # a finding: a `note` would still print as a check result.
        "census": _signature_census(anchor, head, repo=repo),
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
                        expected_old: str, repo: Path = _REPO,
                        prospective_manifest: bytes | None = None) -> dict:
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
    # [E2]/C5, and the live defect security review [S2] found in `2df83d2`:
    # this read the manifest **already in the worktree**, while `apply` commits
    # `authoritative_manifest(...)` -- a different artifact with a different
    # digest. So the report faithfully bound the wrong manifest identity, and
    # `rederive_and_bind` reconfirmed it. The prospective bytes are passed in by
    # the caller that knows them; falling back to the worktree copy is retained
    # only for the read-only preview, and is labelled where it happens.
    if prospective_manifest is not None:
        manifest_bytes = prospective_manifest
    else:
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
                            repo: Path = _REPO,
                            admitted_authority: dict | None = None) -> None:
    """The six Stage-B modules, recorded and compared (Phase 0 step 1).

    A change is **not** a silent pass and **not** an ordinary refusal: it is
    ``review`` -- those bytes need genuine out-of-band human review, which no
    checker can perform, and no bundle may be emitted on that path.

    ``admitted_authority`` is that out-of-band human review, in the one form
    this module can check: a reviewed manifest naming the exact bytes. It is
    honoured here for the same reason as in :func:`check_authority_closure`, and
    it has to be honoured in **both** -- these two checks read the same files and
    either one refusing is enough to make a reviewed transition impossible.
    Admitting in one and not the other is how a mode ends up half-reachable,
    which is worse than unreachable: it looks like it works until the check that
    still refuses is the one that fires.
    """
    admitted = admitted_authority or {}
    recorded = {}
    for rel, abspath in R._authority_code_files():
        live = Path(abspath).read_bytes()
        recorded[rel] = _sha256_bytes(live)
        anchored = _blob_at(anchor, rel, repo=repo)
        if anchored is not None and _sha256_bytes(anchored) == recorded[rel]:
            continue
        if admitted.get(rel) == _sha256_hex(live):
            report.add("AUTHORITY", "note",
                       f"Stage-B authority module admitted by the reviewed "
                       f"transition: {rel}")
            continue
        if anchored is None:
            report.add("AUTHORITY", "review",
                       f"Stage-B authority module absent from the anchor: {rel}")
        else:
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
    refuse_if_sealed("the evidence stage")
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
            # Guarded again at the launch, not only at the function entry:
            # the entry check protects the documented path, this protects the
            # actual capability. A future caller reaching the producer by any
            # other route still stops here.
            refuse_if_sealed("launching the candidate's manifest producer")
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


def _entry_base(entry) -> dict:
    """Normalize a candidate manifest entry to the v2 dict shape.

    **The v1 scalar is the live shape, not a legacy one.** `gather_evidence`
    runs `produce` from a materialized raw tree with no repository, so it emits
    `rel -> "<sha256>"` for every frozen file -- v2-labelled and v1-shaped, as
    [IC2] recorded.

    Losing this is what the first cut of :func:`authoritative_manifest` did:
    it built the entry from `{}` whenever the candidate's side was not already a
    dict and then overlaid only the checker-derived sub-keys, so **every**
    committed entry read `{"mode": ..., "oid": ...}` and the content digest --
    the field the gate actually compares -- was dropped from the artifact
    anchored into the trust root. The end-to-end test could not see it: it
    asserted `blessed == authoritative_manifest(...)`, the same function on both
    sides of the equals sign, so it agreed with whatever the function did.

    `sha256` stays the candidate's on purpose. It is not checker-derived; it is
    checker-*compared*, and `check_static_manifest` has already refused the run
    unless it equals the independent re-derivation.
    """
    if isinstance(entry, dict):
        return dict(entry)
    if isinstance(entry, str):
        return {"sha256": entry}
    return {}


def authoritative_manifest(theirs: dict, ours: dict) -> dict:
    """The manifest the ceremony actually commits: the candidate's, with every
    checker-derived field **replaced** by the checker's own re-derivation.

    Code review **[IC2]**. `apply` used to commit ``evidence["manifest"]``
    verbatim, so the re-derivation was computed, compared, and then discarded --
    not one Git-native field reached the anchored artifact. Because
    `gather_evidence` runs `produce` from a materialized raw tree with no
    ``.git``, the committed manifest was v2-labelled and v1-shaped, and every
    mode/oid check Chunk D added was dead against it.

    Replacing rather than skipping is the point. "Derived by the trusted side
    and never accepted from the candidate" has to be true of the **artifact**,
    not only of the comparison -- a value that is merely un-compared still ends
    up inside the signed checkpoint.

    What stays the candidate's is what only the candidate can know: the pytest
    collection. That is the reason the evidence stage exists at all.
    """
    merged = dict(theirs)
    for field in _CHECKER_DERIVED_FIELDS:
        if field in ours:
            merged[field] = ours[field]
        else:
            merged.pop(field, None)
    for field in ("frozen_files", "cascade_mutable", "phase_mutable"):
        ours_field = ours.get(field)
        if not isinstance(ours_field, dict):
            continue
        theirs_field = theirs.get(field)
        theirs_field = theirs_field if isinstance(theirs_field, dict) else {}
        rebuilt = {}
        for rel, entry in ours_field.items():
            if isinstance(entry, dict):
                base = _entry_base(theirs_field.get(rel))
                for sk in _CHECKER_DERIVED_SUBKEYS:
                    if sk in entry:
                        base[sk] = entry[sk]
                    else:
                        base.pop(sk, None)
                rebuilt[rel] = base
            else:
                rebuilt[rel] = theirs_field.get(rel, entry)
        merged[field] = rebuilt
    return merged


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
            # raw tree with no repository, so it has no oids to offer.
            #
            # Skipping the comparison is safe only because
            # :func:`authoritative_manifest` **replaces** these fields in the
            # bytes `apply` commits ([IC2]). Before that, skipping meant a
            # candidate-supplied value was neither compared nor overwritten, so
            # it rode into the signed artifact unexamined. Refusing the mere
            # presence of a value was tried and is wrong: `produce` legitimately
            # emits full v2 when it runs inside a repository, so the assertion
            # is not by itself evidence of anything. Replacement is what makes
            # the provenance claim true, not refusal.
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


#: The exact strings the admitted-authority block is delimited by. They are
#: constants because :func:`parse_admitted_authority` reads them back, and a
#: record whose writer and reader disagree about its framing is not a record.
_ADMITTED_HEADER = "  admitted authority  : "
_ADMITTED_ROW = "    "
_ADMITTED_NONE = "  admitted authority  : (steady state -- no closure change)"


def _admitted_rows(admitted: dict | None, provenance: str | None,
                   review_digest: str | None) -> str:
    """The complete admitted authority set, as ordered `path -> sha256` rows.

    Plan review [E4] and opening outcome A3. The digest alone binds
    cryptographically and is **unreadable**: a later reader could verify *that*
    a set was admitted without being able to see *which bytes*, because the
    review manifest is an out-of-band artifact that may not survive. Nine rows
    is a reasonable audit cost for a trust root, and it is the difference
    between a durable record and a durable pointer to one.

    D7 binds the **review-manifest digest** alongside them, which answers the
    other half: the rows say what was admitted, the digest says which reviewed
    artifact admitted it. Rows without the digest would let two different
    reviews of the same bytes be indistinguishable in the record.
    """
    if not admitted:
        return _ADMITTED_NONE
    # The digest line comes BEFORE the header so that the member rows are the
    # unbroken block immediately following it. `parse_admitted_authority` reads
    # rows until the first non-row line; anything interleaved would truncate the
    # set it recovers, and a set that reads back short is worse than one that
    # fails to read at all.
    rows = [f"  review manifest     : {review_digest or '(not bound)'}",
            f"{_ADMITTED_HEADER}{len(admitted)} members, "
            f"review: {provenance or '(unrecorded)'}"]
    for rel, digest in sorted(admitted.items()):
        rows.append(f"{_ADMITTED_ROW}{digest}  {rel}")
    return "\n".join(rows)


def parse_admitted_authority(message: str) -> dict | None:
    """Read the admitted authority set back out of a checkpoint message.

    D8. The claim the rows exist to support is that a later reader can recover
    *which bytes* were admitted from the anchored record alone -- so that claim
    has to be executable, not merely plausible from looking at the text. If the
    set can only be recovered by a human squinting at a commit message, it is a
    durable pointer again, just a longer one.

    Returns ``None`` for a steady-state checkpoint, which is a distinct answer
    from an empty set: nothing was admitted because nothing changed.
    """
    lines = message.splitlines()
    for i, line in enumerate(lines):
        if line == _ADMITTED_NONE:
            return None
        if not line.startswith(_ADMITTED_HEADER):
            continue
        declared = line[len(_ADMITTED_HEADER):].split(" members,", 1)[0]
        try:
            count = int(declared)
        except ValueError:
            raise PreflightError(
                f"admitted-authority header does not declare a count: {line!r}")
        members: dict[str, str] = {}
        for row in lines[i + 1:]:
            if not row.startswith(_ADMITTED_ROW):
                break
            digest, _, rel = row[len(_ADMITTED_ROW):].partition("  ")
            if not rel:
                raise PreflightError(f"malformed admitted row: {row!r}")
            if rel in members:
                raise PreflightError(f"duplicate admitted row for {rel}")
            members[rel] = digest
        # The declared count is checked against the rows recovered. A truncated
        # block would otherwise read back as a smaller set that looks complete.
        if len(members) != count:
            raise PreflightError(
                f"the checkpoint declares {count} admitted members and carries "
                f"{len(members)} rows")
        if sorted(members) != list(members):
            raise PreflightError("admitted rows are not in sorted path order")
        return members
    return None


def draft_message(*, observed_anchor: str, checked_head: str,
                  manifest_sha256: str, authority_hashes: dict,
                  scope: dict, last_legitimate_anchor: str | None = None,
                  erroneous_ref: str | None = None,
                  range_report_digest: str | None = None,
                  candidate_tree: str | None = None,
                  admitted_authority: dict | None = None,
                  review_provenance: str | None = None,
                  review_digest: str | None = None) -> str:
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
    message = f"""\
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
{_admitted_rows(admitted_authority, review_provenance, review_digest)}
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
    # Code review [C1]: the writer must be able to read its own record back.
    #
    # The admitted set is written as delimited rows, so a member path carrying a
    # newline forges an extra row -- and the forged message still signs, still
    # verifies, and only fails to parse LATER, when an auditor tries to read the
    # anchored checkpoint. Checking the round trip here turns every framing
    # failure (forged row, truncation, a path that mimics the header) into a
    # refusal BEFORE a signature exists, which is the only point at which it is
    # still cheap.
    if parse_admitted_authority(message) != (admitted_authority or None):
        raise PreflightError(
            "the admitted authority set does not read back out of the message "
            "this ceremony would sign; the durable record would not be "
            "recoverable from the checkpoint")
    return message


# --- Chunk C: the checkpoint binds the reviewed report ---------------------


class RangeReportDrift(PreflightError):
    """The report changed between review and construction."""


def rederive_and_bind(anchor: str, head: str, *, branch: str,
                      expected_old: str, confirmed_digest: str,
                      repo: Path = _REPO,
                      prospective_manifest: bytes | None = None) -> dict:
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
                                expected_old=expected_old, repo=repo,
                                prospective_manifest=prospective_manifest)
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


# --------------------------------------------------------------------------
# the key channel (Chunk D; plan review [E1], proposal R4)
# --------------------------------------------------------------------------
#
# [E1] falsified the design this replaces. The proposal said stage 1 runs with
# "the signing key channel absent (`SSH_AUTH_SOCK` unset)". Reproduced with a
# disposable key: under `env -i`, `HOME=/nonexistent` and NO `SSH_AUTH_SOCK`,
# `ssh-keygen -Y sign -f key.pub` SUCCEEDED, because it found the private
# sibling next to the public key. This checkout's `user.signingkey` has exactly
# that shape.
#
# So an unset variable is **evidence, never the property**, and the property is
# not one code can establish: nothing a program does makes a readable
# unencrypted private key unavailable to another process running as the same
# user. The boundary is therefore a **Maintainer precondition (N4)** -- the
# ceremony key encrypted at rest and in no agent during stage 1 -- and what code
# does is *probe* it and refuse when the probe succeeds.
#
# This remains SEQUENCING, NOT CONTAINMENT. Candidate code that ran earlier on
# the same uncompartmented machine may persist and attack the later agent under
# the accepted residual.

#: How long the probe may take. A probe that hangs is a probe that has not
#: answered, and an interactive passphrase prompt is not a refusal -- it is the
#: ceremony waiting for a human to make the key available.
KEY_PROBE_TIMEOUT_S = 10


class KeyChannelError(PreflightError):
    """Stage 1 could sign, so the N4 precondition does not hold."""


def signing_key_path(recorded: str | None) -> str:
    """The supported key channel, **recorded, never discovered**.

    An earlier version read `user.signingkey` through the sterile launcher, and
    the read-only allowlist refused it -- correctly, since `git config` writes.
    Widening a security allowlist for a convenience read would have been the
    wrong trade; recording the path is the right one, and it is what the rest of
    this ceremony already does. The runbook's discipline is explicit that
    NOTHING is discovered: ambient discovery is how a substituted repository
    once answered for the named one.

    The key path is therefore an input to the ceremony, and it joins the
    residual trust set alongside the other recorded absolute paths.
    """
    return (recorded or "").strip()


def validate_signing_key(recorded: str | None) -> tuple[str, str]:
    """Resolve the recorded key to ``(absolute path, SHA256 fingerprint)``.

    Security review **[S1]**. Before this, a recorded path that did not exist
    was handed straight to :func:`probe_cannot_sign`, `ssh-keygen` failed with
    "no such file", and the failure was classified as **"stage 1 cannot sign"**.
    So the strongest-sounding control in the ceremony could be satisfied by
    aiming it at nothing — and stage 2, which received no key identity at all,
    then signed with whatever key Git found in repository configuration.

    A missing, non-absolute, symlinked, non-regular or unparseable key is
    therefore **unprobeable**, which is a third answer distinct from both
    "cannot sign" and "can sign": the question was never asked. It refuses.

    The fingerprint is what makes the two stages talk about the same key. It is
    derived from the public half only, so computing it neither needs nor touches
    private material.
    """
    # Guarded like the signing probe next to it. `ssh-keygen -l` reads a public
    # key at a pinned absolute path and is not candidate code, so an exemption
    # would have been arguable -- but the key-load sentinel's rule is that
    # *every* subprocess route refuses after the marker, and a rule with no
    # exemptions stays true more reliably than one with a growing list. Nothing
    # validates a key after the seal in any case: both stages do it first.
    refuse_if_sealed("the signing-key validation probe")
    key_path = signing_key_path(recorded)
    if not key_path:
        raise KeyChannelError(
            "no signing key was recorded (--signing-key), so the supported "
            "key channel is unnamed and the N4 precondition cannot be probed. "
            "It is recorded rather than discovered, deliberately.")
    p = Path(key_path)
    if not p.is_absolute():
        raise KeyChannelError(
            f"the recorded signing key {key_path!r} is not an absolute path; "
            f"a relative key path resolves against a working directory the "
            f"ceremony does not control")
    if p.is_symlink():
        raise KeyChannelError(
            f"the recorded signing key {key_path} is a symlink; the probed "
            f"channel and the signing channel must be the same file, and a "
            f"link can be repointed between the stages")
    if not p.is_file():
        raise KeyChannelError(
            f"the recorded signing key {key_path} does not exist or is not a "
            f"regular file, so the key channel is UNPROBEABLE. This is not "
            f"'stage 1 cannot sign': a probe aimed at a path that is not there "
            f"fails for the wrong reason and proves nothing about the key the "
            f"ceremony would actually use.")
    r = subprocess.run([_resolved_binary("ssh-keygen", _SSH_KEYGEN),
                        "-l", "-f", key_path],
                       capture_output=True, text=True, check=False,
                       stdin=subprocess.DEVNULL)
    fields = (r.stdout or "").split()
    fingerprint = next((f for f in fields if f.startswith("SHA256:")), None)
    if r.returncode != 0 or not fingerprint:
        raise KeyChannelError(
            f"the recorded signing key {key_path} does not parse as a public "
            f"key ({(r.stderr or '').strip()[:200]}), so the channel is "
            f"UNPROBEABLE")
    return key_path, fingerprint


def probe_cannot_sign(key_path: str, *, env: dict | None = None) -> tuple:
    """Attempt a real signing operation. **Success is the failure case.**

    Non-interactive and timeout-bounded: `ssh-keygen` prompts for a passphrase
    on an encrypted key, and a prompt is not a refusal -- left interactive, the
    ceremony would sit waiting for the operator to supply exactly the thing the
    probe exists to prove is unavailable. `< /dev/null` plus a timeout turns
    that into a definite negative.

    Returns ``(cannot_sign, detail, timed_out)``. This is a probe of a
    precondition, not an enforcement of one. ``timed_out`` is separate from
    ``cannot_sign`` because a hung probe answered **neither** question, and
    reporting it as either one tells the operator something this run did not
    establish ([D4]).
    """
    # Guarded like every other launcher in this module. The probe runs `ssh-keygen`
    # at a pinned absolute path, not candidate code, so exempting it would have
    # been defensible -- but a rule with one exemption stays true more reliably
    # than a rule with a growing list, and the probe has no business running
    # after the key-load seal in any case.
    refuse_if_sealed("the key-channel signing probe")
    child = dict(env or os.environ)
    child.pop("SSH_AUTH_SOCK", None)          # evidence, not the property
    child["SSH_ASKPASS_REQUIRE"] = "never"    # no GUI prompt path either
    child["DISPLAY"] = ""
    with tempfile.TemporaryDirectory(prefix="cairn-keyprobe-") as td:
        payload = Path(td) / "probe"
        payload.write_bytes(b"cairn key-channel probe\n")
        try:
            r = subprocess.run(
                [_SSH_KEYGEN, "-Y", "sign", "-f", key_path, "-n", "git",
                 str(payload)],
                stdin=subprocess.DEVNULL, capture_output=True, text=True,
                timeout=KEY_PROBE_TIMEOUT_S, env=child, check=False)
        except subprocess.TimeoutExpired:
            # [D4]: reported as its own outcome, not folded into "can sign".
            # The caller still refuses -- an unanswered probe is not a pass --
            # but it no longer tells the operator the channel is open when
            # nothing established that.
            return (False, "the signing probe timed out; a probe that hangs "
                           "has not answered, and a passphrase prompt is not "
                           "a refusal", True)
        # Code review [C5]: exit 0 alone means the key channel is OPEN.
        #
        # This used to require a locatable `.sig` as well, so an `ssh-keygen`
        # that succeeded while writing its output somewhere this code did not
        # look was reported as "cannot sign" -- fail-OPEN, on the probe whose
        # entire job is to refuse. The safe reading of a successful signing
        # command is that signing succeeded; where the artifact landed is a
        # detail, not the verdict.
        if r.returncode == 0:
            found = (payload.with_suffix(".sig").exists()
                     or Path(str(payload) + ".sig").exists())
            return (False, "a signature was produced" if found else
                    "ssh-keygen reported success; no .sig was found where "
                    "expected, which is treated as signing having worked",
                    False)
        return (True, (r.stderr or "").strip()[-300:] or "signing failed",
                False)


def require_stage1_cannot_sign(recorded_key: str | None = None, *,
                               out=sys.stderr) -> dict:
    """Stage 1's gate on the N4 precondition. Refuses if signing succeeds.

    Security review [S1]: the key is **validated before it is probed**, and the
    fingerprint returned here is what binds stage 2 to this same key.
    """
    key_path, fingerprint = validate_signing_key(recorded_key)
    cannot, detail, timed_out = probe_cannot_sign(key_path)
    if timed_out:
        # [D4]: a hung probe answered nothing, so saying "CAN SIGN" asserts
        # something this run did not establish. Refusing is still right --
        # an unanswered question about the key channel is not a pass.
        raise KeyChannelError(
            f"the key-channel probe through {key_path} did not answer within "
            f"{KEY_PROBE_TIMEOUT_S}s ({detail}). A probe that hangs has "
            f"established nothing in either direction, so the ceremony stops "
            f"rather than assuming the answer it did not get.")
    if not cannot:
        raise KeyChannelError(
            f"STAGE 1 CAN SIGN through {key_path} ({detail}). The N4 "
            f"precondition -- the ceremony key encrypted at rest and loaded "
            f"into no agent -- does not hold, so this stage would run candidate "
            f"code while the key is reachable. Code cannot make a readable "
            f"private key unavailable to a same-user process; the ceremony "
            f"stops here.")
    out.write(f"key-channel probe: stage 1 cannot sign through {key_path}\n"
              f"key fingerprint (bound into the package): {fingerprint}\n")
    return {"key_path": key_path, "fingerprint": fingerprint, "probe": detail}


# --------------------------------------------------------------------------
# the authorization package (Chunk C; plan review [E2], proposal R3)
# --------------------------------------------------------------------------

PACKAGE_SCHEMA = "cairn-authorization-package/v1"

#: The ONLY fields stage 2 may take from stage 1 rather than re-derive.
#: Closed and asserted: these are exactly what static re-derivation cannot
#: produce, which is the entire reason the evidence stage exists. A third
#: member appearing here without a matching change to
#: `rederive_static_manifest` means something derivable is being delegated.
PACKAGE_EXECUTABLE_ONLY = ("collection", "interpreter")

#: 8 MiB. The package is a handful of digests, a path list and one manifest;
#: a bounded read is what makes "hash the bytes, then parse them" affordable.
PACKAGE_MAX_BYTES = 8 * 1024 * 1024


class PackageError(PreflightError):
    """The authorization package is malformed, unconfirmed, or does not match."""


def _no_duplicate_keys(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise PackageError(f"duplicate key {key!r} in the package")
        seen[key] = value
    return seen


def package_bytes(pkg: dict) -> bytes:
    """Canonical serialization. Deterministic for the same content."""
    return json.dumps(pkg, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii") + b"\n"


def write_package(path: Path, pkg: dict) -> str:
    """Write the package atomically and exclusively; return the **external**
    digest over the exact bytes written.

    **The digest is external on purpose** ([E2]). An earlier design put a
    `package_digest` field *inside* the package it digests, which is either
    recursive or silently excludes a field nobody named -- and either way it is
    the adjacent self-digest CR1 falsified, one layer down. Authority comes from
    a digest the Maintainer carries out of band, computed over bytes that
    already exist.

    `O_EXCL` on a fresh path, a restrictive mode, and a refusal on a symlinked
    parent or leaf: a package written over something else, or through a link, is
    not a package this ceremony produced.
    """
    path = Path(path)
    if path.is_symlink():
        raise PackageError(f"package destination {path} is a symlink")
    if path.exists():
        raise PackageError(f"package destination {path} already exists")
    parent = path.parent
    if parent.is_symlink():
        raise PackageError(f"package parent {parent} is a symlink")

    body = package_bytes(pkg)
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(fd, body)
    finally:
        os.close(fd)
    # BARE lowercase hex, deliberately, not this module's `sha256:`-prefixed
    # form. The Maintainer carries this digest out of band and compares it by
    # eye against `shasum -a 256` output, which is bare. A prefix the operator
    # has to mentally strip mid-ceremony is a place to make a mistake, and the
    # ceremony's own recorded commands use `shasum` throughout.
    return hashlib.sha256(body).hexdigest()


def read_package(path: Path, *, confirmed_sha256: str) -> dict:
    """Read, hash, confirm, then parse -- in that order.

    Hashing before parsing is the point: what the Maintainer confirmed is a
    sequence of bytes, so the bytes are what must be measured. Parsing first
    and hashing a re-serialization would confirm a *rendering* of the file.

    ``O_NOFOLLOW`` because a symlinked package is a file substituted between
    the ceremony that wrote one and the ceremony that reads it; the size bound
    because an unbounded read into memory is its own denial surface; and a
    single read because a file re-read is a file that could change in between.
    """
    path = Path(path)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(str(path), flags)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise PackageError(f"package {path} is not a regular file")
        if st.st_size > PACKAGE_MAX_BYTES:
            raise PackageError(
                f"package {path} is {st.st_size} bytes, over the "
                f"{PACKAGE_MAX_BYTES} limit")
        body = os.read(fd, PACKAGE_MAX_BYTES + 1)
    finally:
        os.close(fd)
    if len(body) > PACKAGE_MAX_BYTES:
        raise PackageError("package exceeds the size limit")

    actual = hashlib.sha256(body).hexdigest()   # bare, matching `shasum`
    if actual != confirmed_sha256:
        raise PackageError(
            f"package digest {actual} does not match the confirmed "
            f"{confirmed_sha256}. The confirmation is over the exact bytes "
            f"stage 1 wrote; no digest inside the package can satisfy it.")

    try:
        pkg = json.loads(body.decode("utf-8"),
                         object_pairs_hook=_no_duplicate_keys)
    except json.JSONDecodeError as exc:
        raise PackageError(f"package is not valid JSON: {exc}") from None
    if not isinstance(pkg, dict):
        raise PackageError("package is not a JSON object")
    if pkg.get("schema") != PACKAGE_SCHEMA:
        raise PackageError(f"unknown package schema {pkg.get('schema')!r}")
    if "package_digest" in pkg or "sha256" in pkg:
        raise PackageError(
            "the package carries a self-digest field; authority comes from the "
            "externally confirmed digest, never from the artifact itself")

    expected = {"schema", "observed_anchor", "candidate_head", "candidate_tree",
                "branch", "expected_old", "range_report", "range_report_digest",
                "review_manifest", "prospective_manifest_b64",
                "prospective_manifest_sha256",
                "signing_key_fingerprint"} | set(PACKAGE_EXECUTABLE_ONLY)
    missing, extra = sorted(expected - set(pkg)), sorted(set(pkg) - expected)
    if missing or extra:
        raise PackageError(
            f"package fields do not match the schema: {len(missing)} missing "
            f"{missing}, {len(extra)} unexpected {extra}")

    # Code review [C1]: the INNER shape, which nothing checked.
    #
    # The top-level field set was validated and `review_manifest`'s contents
    # were not, so a non-dict reached `.get(...)` and surfaced as an uncaught
    # AttributeError -- a traceback rather than a `[REFUSE ]`, on the one code
    # path that moves the trust root. The values are no longer *trusted* (the
    # checkpoint is built from the revalidated transition), but a package that
    # is malformed must still be refused as malformed rather than crashing.
    rm = pkg["review_manifest"]
    if rm is not None:
        if not isinstance(rm, dict):
            raise PackageError(
                f"package review_manifest is {type(rm).__name__}, not an "
                f"object or null")
        rm_expected = {"provenance", "candidate", "digest", "members"}
        rm_missing = sorted(rm_expected - set(rm))
        rm_extra = sorted(set(rm) - rm_expected)
        if rm_missing or rm_extra:
            raise PackageError(
                f"package review_manifest fields do not match the schema: "
                f"{len(rm_missing)} missing {rm_missing}, "
                f"{len(rm_extra)} unexpected {rm_extra}")
        if not isinstance(rm["members"], dict) or not rm["members"]:
            raise PackageError(
                "package review_manifest carries no member set; a transition "
                "with nothing admitted is not a transition")
        for rel, digest in rm["members"].items():
            if not isinstance(rel, str) or not isinstance(digest, str):
                raise PackageError(
                    f"package review_manifest member {rel!r} is malformed")
            if len(digest) != 64 or any(c not in "0123456789abcdef"
                                        for c in digest):
                raise PackageError(
                    f"package review_manifest names a non-sha256 digest for "
                    f"{rel!r}")
            # Control characters -- a newline forges an extra row when the set
            # is written into the checkpoint message.
            if any(ord(c) < 0x20 or ord(c) == 0x7F for c in rel):
                raise PackageError(
                    f"package review_manifest member path contains a control "
                    f"character: {rel!r}")
        for field in ("provenance", "candidate", "digest"):
            if not isinstance(rm[field], str):
                raise PackageError(
                    f"package review_manifest {field} is not a string")
            if any(ord(c) < 0x20 or ord(c) == 0x7F for c in rm[field]):
                raise PackageError(
                    f"package review_manifest {field} contains a control "
                    f"character")
    return pkg


def blessing_plan(report: Report, evidence: dict, *, repo: Path = _REPO,
                  last_legitimate_anchor: str | None = None,
                  manifest: dict | None = None,
                  manifest_sha256: str | None = None,
                  branch: str | None = None,
                  expected_old: str | None = None,
                  prospective_manifest: bytes | None = None,
                  admitted_authority: dict | None = None,
                  review_provenance: str | None = None,
                  review_digest: str | None = None) -> dict:
    """The derived description of what a blessing would do.

    Formerly emitted as a handoff *bundle* that ``apply`` read back and trusted.
    Code review CR1 falsified that: value and digest sat in the same editable
    JSON, so re-hashing a tampered manifest was accepted. It is now built in
    memory by whichever command needs it, and `check` may write it out only as a
    **record for the operator to read** -- nothing consumes it as authority.
    """
    old = json.loads(_blob_at(report.facts["anchor"], _MANIFEST_REL,
                              repo=repo) or b"{}")
    new = manifest if manifest is not None else evidence["manifest"]
    bound_sha = (manifest_sha256 if manifest_sha256 is not None
                 else evidence["manifest_sha256"])
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
    # [M2-1]: derive the canonical report HERE, so the message that gets signed
    # binds it. This was the whole point of Chunks B and C, and neither reached
    # this line -- `range_report_digest` defaulted to None and every real
    # ceremony signed "range-report digest : (not bound)". The machinery existed,
    # was tested in isolation, and was dead to authorization.
    the_report = (range_review_report(
                      report.facts["anchor"], report.facts["head"],
                      branch=branch, expected_old=expected_old, repo=repo,
                      prospective_manifest=prospective_manifest)
                  if branch and expected_old else None)
    report_digest = range_report_digest(the_report) if the_report else None
    candidate_tree = (_resolve_tree(report.facts["head"], repo=repo)
                      if the_report else None)

    message = draft_message(
        observed_anchor=report.facts["anchor"],
        checked_head=report.facts["head"],
        manifest_sha256=bound_sha,
        authority_hashes=report.facts["authority_hashes"],
        scope=scope, last_legitimate_anchor=last_legitimate_anchor,
        erroneous_ref=erroneous,
        range_report_digest=report_digest,
        candidate_tree=candidate_tree,
        admitted_authority=admitted_authority,
        review_provenance=review_provenance,
        review_digest=review_digest)
    return {
        "schema": BUNDLE_SCHEMA,
        "checked_head": report.facts["head"],
        "observed_anchor": report.facts["anchor"],
        "last_legitimate_anchor": last_legitimate_anchor,
        "manifest": new,
        "manifest_sha256": bound_sha,
        "range_report": the_report,
        "range_report_digest": report_digest,
        "candidate_tree": candidate_tree,
        "message": message,
        "message_sha256": _sha256_bytes(message.encode()),
        "authority_hashes": report.facts["authority_hashes"],
        "scope": scope,
    }


# --------------------------------------------------------------------------
# Chunk D -- apply: revalidate, construct, verify, then one ref transaction
# --------------------------------------------------------------------------

def _git_write(*args: str, repo: Path = _REPO, stdin: str | None = None,
               want_bytes: bool = False, config: dict | None = None,
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
                    index=index, config=config)


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
                             message: str, *, signing_key: str) -> str:
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
        # [S1]: name the key EXPLICITLY. A bare `-S` makes Git choose the signer
        # from `user.signingKey`, which is repository configuration -- so the
        # commit that becomes the trust root was signed by whichever key the
        # candidate's own config named. Pinning it per-invocation puts the
        # selector out of the repository's reach, alongside
        # `gpg.ssh.defaultKeyCommand` in `_STERILE_CONFIG`.
        ct = _git_write("commit-tree", tree, "-p", head, "-S", "-F", "-",
                        repo=repo, stdin=message,
                        config={"user.signingKey": signing_key})
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
                       principals: set, roster_path: Path,
                       expected_fingerprint: str | None = None) -> None:
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

    sig = _git("log", "-1", "--format=%G?%x09%GS%x09%GF", new, repo=repo,
               config={"gpg.ssh.allowedSignersFile": str(roster_path)})
    status, _, rest = (sig.stdout or "").strip().partition("\t")
    signer, _, fingerprint = rest.partition("\t")
    if status != "G":
        raise PreflightError(
            f"constructed commit is not validly signed (status {status or '?'})"
            f" -- it becomes the anchor, so later anchor..HEAD checks would "
            f"never see it")
    if signer not in principals:
        raise PreflightError(
            f"constructed commit is signed by an unpinned principal {signer!r}")
    # [S1]: identity AND authorization, not one standing in for the other.
    #
    # The principal check asks "is this signer on the anchored roster"; it says
    # nothing about *which* rostered key signed. A second rostered key therefore
    # passed the whole verification triple. The fingerprint check asks the other
    # question: is this the key stage 1 probed and the package bound. Both are
    # needed -- a roster member who is not the probed key means the N4
    # precondition was established for a key that did not sign.
    if expected_fingerprint is not None and fingerprint != expected_fingerprint:
        actual = fingerprint or "(no fingerprint reported)"
        raise PreflightError(
            f"constructed commit is signed by {actual}, not by the key this "
            f"ceremony probed and bound into the package "
            f"({expected_fingerprint}). The probed channel and the signing "
            f"channel must be the same key.")


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
    # The reason is a module constant, not a caller argument, so both refs carry
    # the *same* identifying string and neither can be labelled to look like
    # something it was not. It is written by `-m`, which `update-ref` applies to
    # every update in the `--stdin` transaction.
    #
    # A reflog is a **local, mutable diagnostic** for recovery and sequencing.
    # It is never tamper evidence and never authentication: anyone who can write
    # the ref can write its reflog. No decision predicate in this module reads
    # reflog content, and none may.
    p = _git_write("update-ref", "--no-deref", "--create-reflog",
                   "-m", _CEREMONY_REFLOG_REASON, "--stdin",
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


def stage1(*, repo: Path = _REPO, package_out: Path,
           signing_key: str | None = None,
           review_manifest: str | None = None,
           reviewed_candidate: str | None = None,
           out=sys.stderr) -> dict:
    """**Stage 1**: everything that executes candidate code, with the key away.

    Proposal R4-a. This stage gathers evidence, runs the read-only checks,
    derives the canonical range report and the prospective authoritative
    manifest, writes one authorization package, prints the hard marker and the
    package's external digest, and exits. **It never holds the signing key.**

    Order is the contract: the key-channel probe runs FIRST, before any
    candidate code, because the whole point is that candidate code and the key
    are never simultaneously available. Probing afterwards would prove the
    boundary held at a moment that no longer matters.
    """
    repo = _require_worktree_root(repo)
    key = require_stage1_cannot_sign(signing_key, out=out)

    # The transition is revalidated BEFORE the checks, and before candidate code
    # runs. Both orderings are load-bearing.
    #
    # Before the checks, because the closure check has to know which byte
    # changes an external review admitted -- placed after, it refused every real
    # transition and the mode was unreachable (see `check_authority_closure`).
    # Before `gather_evidence`, because there is no reason to execute candidate
    # code for a transition whose manifest does not hold up.
    transition = review_digest = None
    if review_manifest is not None:
        parsed, review_digest = read_review_manifest(review_manifest)
        transition = revalidate_transition(
            parsed, reviewed_candidate, _resolve("HEAD", repo=repo),
            anchor=_resolve(_ANCHOR_REF, repo=repo), repo=repo)
        out.write(f"transition revalidated against the review manifest "
                  f"({transition['provenance']}, {len(transition['members'])} "
                  f"members, digest {review_digest[:12]})\n")

    evidence = gather_evidence("HEAD", repo=repo, out=out)
    report = check(repo=repo, evidence=evidence,
                   admitted_authority=(transition["members"] if transition
                                       else None))
    _render(report, out)
    if report.blocked:
        raise PreflightError(
            "the read-only checks refuse this state; nothing was written")

    head, anchor = report.facts["head"], report.facts["anchor"]

    branch = _git("rev-parse", "--symbolic-full-name", "HEAD",
                  repo=repo).stdout.strip()
    if not branch.startswith("refs/heads/"):
        raise PreflightError(f"HEAD is not on a branch ({branch!r})")
    branch_old = _resolve(branch, repo=repo)

    committed_manifest = authoritative_manifest(
        evidence["manifest"], rederive_static_manifest(head, repo=repo))
    manifest_bytes = (json.dumps(committed_manifest, indent=2, sort_keys=True)
                      .encode() + b"\n")
    the_report = range_review_report(anchor, head, branch=branch,
                                     expected_old=branch_old, repo=repo,
                                     prospective_manifest=manifest_bytes)

    pkg = {
        "schema": PACKAGE_SCHEMA,
        "observed_anchor": anchor,
        "candidate_head": head,
        "candidate_tree": _resolve_tree(head, repo=repo),
        "branch": branch,
        "expected_old": branch_old,
        "range_report": the_report,
        "range_report_digest": range_report_digest(the_report),
        "review_manifest": ({"provenance": transition["provenance"],
                             "candidate": transition["candidate"],
                             "digest": review_digest,
                             "members": transition["members"]}
                            if transition else None),
        "prospective_manifest_b64": base64.b64encode(manifest_bytes).decode(),
        "prospective_manifest_sha256": _sha256_bytes(manifest_bytes),
        # [S1]: the identity of the key stage 1 probed. Stage 2 re-derives this
        # from the key IT was given and refuses on any difference, which is what
        # makes "the probed key is the signing key" a checked property rather
        # than an assumption spanning two processes.
        "signing_key_fingerprint": key["fingerprint"],
        "collection": evidence["manifest"].get("collection"),
        "interpreter": evidence["manifest"].get("interpreter"),
    }
    digest = write_package(package_out, pkg)

    seal_candidate_execution(out=out)
    out.write(
        f"\nSTAGE 1 COMPLETE. Package written to {package_out}\n"
        f"  package sha256 : {digest}\n"
        f"  report digest  : {pkg['range_report_digest']}\n"
        f"  candidate tree : {pkg['candidate_tree']}\n\n"
        f"Confirm the package digest above by an independent `shasum -a 256`,\n"
        f"read the report it contains, THEN make the ceremony key available and\n"
        f"run stage 2 with --confirm-package-sha256 <that digest>.\n"
        f"Key channel probed unavailable in this stage: {key['key_path']}\n")
    return {"package": str(package_out), "package_sha256": digest,
            "range_report_digest": pkg["range_report_digest"]}


def apply_now(*, repo: Path = _REPO,
              package: str | None = None,
              confirmed_package_sha256: str | None = None,
              signing_key: str | None = None,
              review_manifest: str | None = None,
              reviewed_candidate: str | None = None,
              out=sys.stderr) -> dict:
    """Validate the confirmed package, re-derive everything derivable, then bless.

    **Security review [S2] retired the old claim in this docstring.** It used to
    say "no handoff artifact is trusted" and "there is no authority-bearing
    file". That described the removed single-process design, and it is false of
    this one: stage 2 necessarily consumes the authorization package and takes
    its ``collection`` and ``interpreter`` fields, which static Git reads cannot
    derive. Leaving it in place was worse than an ordinary stale comment --
    security documentation shipped inside the deciding executable, contradicting
    the protocol an operator is asked to trust. Chunk C10 required the
    retraction; this is it.

    **The invariant that is actually true**, and the one to hold this code to:

    * **No adjacent self-digest authenticates a file.** A digest carried inside
      the artifact it describes is a corruption check, not tamper evidence --
      value and digest come from the same editable JSON, which code review CR1
      falsified by re-hashing a tampered manifest and having it anchored.
    * **The Maintainer's out-of-band confirmation authenticates the exact
      package bytes.** ``--confirm-package-sha256`` is over the file stage 1
      wrote, computed independently by the operator. That is the authority
      boundary, and it is deliberately a human one.
    * **Stage 2 re-derives every derivable field** and compares exact bytes,
      so the package's contribution is bounded to the closed executable-only
      pair.

    What the confirmation cannot do is protect an operator who confirms an
    attacker-supplied digest without reading the report it covers. That is the
    boundary's nature, not a gap in it.

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

    That history is why the package's digest is **external** rather than
    adjacent. It is not why this paragraph used to conclude "there is no
    authority-bearing file" ([S2]) -- there is one, and it is the package; what
    it is not is *self*-authenticating.
    ``check`` remains available as a non-mutating preview, and its output is a
    record for the operator to read, never an input here.
    """
    if confirmed_package_sha256 is None:
        raise PreflightError(
            "the signing stage requires the Maintainer's confirmation of the "
            "exact stage-1 package digest (--confirm-package-sha256). The "
            "boolean --confirm-supervised-reanchor was REMOVED, not "
            "deprecated ([S4]/D4): a confirmation that cannot be wrong is not "
            "a confirmation, and an up-front flag confirms nothing about the "
            "state actually being authorized.")
    # Re-validated here and not only at the CLI boundary: this is the one
    # function that moves the trust root, so the repository it moves must be the
    # one the caller named, not one git discovered by walking upward (FUR5).
    repo = _require_worktree_root(repo)

    # ---- STAGE 2 ----------------------------------------------------------
    # Proposal R4-c. The package is read, hashed and confirmed BEFORE anything
    # else, and no candidate code runs in this process at all: the seal is set
    # up front rather than midway, so a candidate-executing operation anywhere
    # below refuses instead of merely being unreachable by inspection.
    pkg = read_package(Path(package), confirmed_sha256=confirmed_package_sha256)

    # [S1]: stage 2 is told WHICH KEY, and checks it is the one stage 1 probed.
    #
    # Stage 2 previously received no key identity at all and signed with a bare
    # `-S`, so Git selected the signer from repository `user.signingKey`. The
    # consequence was demonstrable: point stage 1 at a nonexistent path (which
    # `validate_signing_key` now refuses outright) and stage 2 would sign with a
    # different, usable key and pass the whole verification triple, because the
    # principal check asks only whether the signer is rostered.
    #
    # Validated here rather than trusted from the package: the fingerprint in
    # the package is a claim by stage 1, and this re-derivation from the file
    # stage 2 was handed is what turns it into an agreement between two
    # processes about one key.
    stage2_key, stage2_fpr = validate_signing_key(signing_key)
    if stage2_fpr != pkg["signing_key_fingerprint"]:
        raise PackageError(
            f"stage 2 was given a key with fingerprint {stage2_fpr}; the "
            f"package was authorized against {pkg['signing_key_fingerprint']}. "
            f"The key stage 1 probed and the key stage 2 would sign with must "
            f"be the same key.")
    seal_candidate_execution(out=out)
    out.write(f"stage 2: package confirmed {confirmed_package_sha256[:16]}...; "
              f"candidate execution sealed before any derivation\n")

    # R4-c, and it runs FIRST -- before the read-only checks, not after.
    #
    # A package authorizes ONE state. Every fact stage 1 recorded about where
    # the repository stood is re-resolved here and required to be unchanged; a
    # package is not a licence that follows the branch forward.
    #
    # The ordering is the finding. With this comparison placed after `check`,
    # every stale-package scenario refused -- but refused *at the checks*, on a
    # state that had already moved, so the comparison written to catch exactly
    # this never executed. That is the [M2-1] shape: a control built, tested in
    # isolation, and unreachable through the governing path. Here it is the
    # first thing stage 2 decides, so a stale package is rejected as a stale
    # package, with a diagnostic that says so.
    branch = _git("rev-parse", "--symbolic-full-name", "HEAD",
                  repo=repo).stdout.strip()
    if not branch.startswith("refs/heads/"):
        raise PreflightError(
            f"HEAD is not on a branch ({branch!r}); refusing to advance a "
            f"detached HEAD")
    for field, expected in (("observed_anchor", _resolve(_ANCHOR_REF, repo=repo)),
                            ("candidate_head", _resolve("HEAD", repo=repo)),
                            ("expected_old", _resolve(branch, repo=repo)),
                            ("branch", branch)):
        if pkg[field] != expected:
            raise PackageError(
                f"package {field} is {pkg[field]!r}; this repository is now "
                f"{expected!r}. A stale package cannot authorize a moved state.")

    # C7. Stage 2 rebuilds the manifest from its OWN static re-derivation plus
    # the two fields C6 declares candidate-only, and never from the candidate's
    # manifest -- which it does not have and must not need.
    #
    # This is what gives the exact-byte comparison below its teeth. Stage 1
    # built the package's bytes from the *candidate's* manifest; stage 2 builds
    # from a re-derivation with `collection` and `interpreter` grafted on. The
    # two agree byte-for-byte **only if** the candidate contributed nothing else
    # -- so C6's closed executable-only list stops being an assertion in a
    # comment and becomes a property re-tested on every real run. A third
    # candidate-only field appearing anywhere makes stage 2 refuse, which is the
    # answer the plan review asked for: it fails, it does not silently trust.
    static = rederive_static_manifest(pkg["candidate_head"], repo=repo)
    evidence = {
        "schema": EVIDENCE_SCHEMA,
        "candidate_sha": pkg["candidate_head"],
        "manifest": {**static,
                     "collection": pkg["collection"],
                     "interpreter": pkg["interpreter"]},
        "interpreter": pkg["interpreter"]["version"],
    }
    evidence["manifest_sha256"] = _sha256_bytes(
        json.dumps(evidence["manifest"], indent=2, sort_keys=True).encode()
        + b"\n")
    # Transition-mode revalidation, ahead of the checks for the same reason as
    # in stage 1: the closure check cannot admit a reviewed byte change it has
    # not been told about. Defence in depth ([E3]) -- the loader has already
    # selected and started these bytes, so this cannot establish that the
    # selection was sound. It restates the loader's conclusions from inside so a
    # loader edited laxer than its recorded text is caught, and so the parsed
    # values are available to bind into the checkpoint.
    transition = review_digest = None
    if review_manifest is not None:
        parsed, review_digest = read_review_manifest(review_manifest)
        if pkg["review_manifest"] is None:
            raise PackageError(
                "stage 2 was given a review manifest for a package stage 1 "
                "produced in steady state; the two stages disagree about "
                "whether this is a reviewed-authority transition")
        if review_digest != pkg["review_manifest"].get("digest"):
            raise PackageError(
                f"the review manifest here digests to {review_digest[:12]}; "
                f"the package was authorized against "
                f"{str(pkg['review_manifest'].get('digest'))[:12]}. Stage 2 "
                f"must be handed the same out-of-band artifact stage 1 saw.")
        transition = revalidate_transition(
            parsed, reviewed_candidate, _resolve("HEAD", repo=repo),
            anchor=_resolve(_ANCHOR_REF, repo=repo), repo=repo)

        # The two stages must agree about what is being admitted. The checkpoint
        # is built from `transition` regardless ([C1]), so a mismatch can no
        # longer forge the record -- but a package whose admitted set differs
        # from the one stage 2 just revalidated is tampered or stale, and
        # refusing says so instead of quietly overriding it.
        for field in ("members", "provenance", "candidate"):
            if pkg["review_manifest"][field] != transition[field]:
                raise PackageError(
                    f"the package's review_manifest {field} does not match "
                    f"what stage 2 revalidated from the out-of-band artifact; "
                    f"the two stages disagree about what is being admitted")
        out.write(f"transition revalidated against the review manifest "
                  f"({transition['provenance']})\n")
    elif pkg["review_manifest"] is not None:
        # The converse, and the one that actually matters. Stage 1 selected a
        # reviewed-authority transition; dropping the flag at stage 2 would
        # sign a checkpoint whose message records "steady state -- no closure
        # change" for a run that changed the closure. The admitted set would be
        # absent from the durable record while the ref moved anyway, which is
        # the [E4] failure with a signature on top.
        raise PackageError(
            "the package authorizes a reviewed-authority transition, but "
            "stage 2 was given no --transition-from-review. A transition "
            "cannot be signed as steady state.")

    report = check(repo=repo, evidence=evidence,
                   admitted_authority=(transition["members"] if transition
                                       else None))
    _render(report, out)
    if report.blocked:
        raise PreflightError(
            "the read-only checks refuse this state; nothing was written")

    head, anchor = report.facts["head"], report.facts["anchor"]
    if transition:
        report.facts["transition"] = {
            "candidate": transition["candidate"],
            "provenance": transition["provenance"],
            "members": len(transition["members"]),
            "changed": sorted(authority_closure_delta(
                anchor, reviewed_candidate, repo=repo)),
        }
    _require_direct_ref(_ANCHOR_REF, repo=repo)

    # [IC2]: commit the checker's Git-native identity, not the candidate's.
    # `evidence["manifest"]` used to go in verbatim, which made the whole
    # re-derivation ceremonial -- computed, compared, discarded. The digest and
    # the message follow the bytes, so the checkpoint binds what is anchored.
    committed_manifest = authoritative_manifest(
        evidence["manifest"], rederive_static_manifest(head, repo=repo))
    manifest_bytes = (json.dumps(committed_manifest, indent=2, sort_keys=True)
                      .encode() + b"\n")
    committed_sha256 = _sha256_bytes(manifest_bytes)

    # R3-a: rebuild independently and compare EXACT BYTES with the package's.
    # A field-by-field comparison would accept a re-serialization that differs
    # from what stage 1 measured, and the checkpoint binds bytes.
    staged = base64.b64decode(pkg["prospective_manifest_b64"])
    if staged != manifest_bytes:
        raise PackageError(
            "the prospective manifest rebuilt in stage 2 differs from the one "
            "the package carries; the confirmed digest covers bytes that are "
            "no longer what this ceremony would commit")
    if pkg["prospective_manifest_sha256"] != committed_sha256:
        raise PackageError("the package's prospective manifest digest is stale")
    # The state comparison itself ran up front, before the checks. This is the
    # value it established, re-resolved once and threaded onward so the
    # transaction's expected-old is the one that was compared.
    branch_old = _resolve(branch, repo=repo)
    plan = blessing_plan(report, evidence, repo=repo,
                         manifest=committed_manifest,
                         manifest_sha256=committed_sha256,
                         branch=branch, expected_old=branch_old,
                         prospective_manifest=manifest_bytes,
                         # Code review [C1]: the DURABLE RECORD comes from the
                         # revalidated transition, never from the package.
                         #
                         # These read `pkg["review_manifest"]` before, while the
                         # checks above were given `transition["members"]`. So
                         # enforcement was honest and the signed message was
                         # whatever the package said -- and `read_package`
                         # validates only the top-level field set, so the inner
                         # dict was entirely unchecked. A package re-digested
                         # after tampering (the confirmation then matches
                         # perfectly) signed nine false rows with every check
                         # green, and dropping the `members` key signed
                         # "steady state -- no closure change" over a real
                         # closure change -- verbatim the failure the refusal
                         # above exists to prevent.
                         #
                         # `transition` is the set that passed
                         # `revalidate_transition`: whole-closure match, each
                         # member's digest checked against the candidate's own
                         # blob. It was already in hand at this call site.
                         admitted_authority=(transition["members"]
                                             if transition else None),
                         review_provenance=(transition["provenance"]
                                            if transition else None),
                         review_digest=review_digest)

    # [M2-1], the governing path. Three separate obligations, none of which the
    # reviewed bytes performed:
    #
    #   PRESENT  -- the complete report, not a count. The Maintainer authorizes
    #               a state; a digest alone is not a state they can read.
    #   RE-DERIVE -- immediately before construction, from the same refs, and
    #               refuse on any drift. `rederive_and_bind` has done exactly
    #               this since Chunk C and had no caller.
    #   BIND     -- the digest and candidate tree must be in the exact signed
    #               message, checked before a signature exists.
    if plan["range_report_digest"] is None:
        raise PreflightError(
            "no range-review report was derived; the checkpoint would bind no "
            "reviewed classification, which is the state [M2-1] found")

    # CLOSE THE HANDSHAKE: what the Maintainer read must be what gets signed.
    #
    # The two-stage protocol's entire value is that a human reads the report in
    # the package and confirms its digest before the key is loaded. Stage 2
    # re-derives its own report -- correctly, since a package must not be
    # authority -- but re-deriving and then never comparing means the Maintainer
    # could authorize report R while stage 2 signs R'. In practice the state
    # comparison above makes them agree; "in practice" is exactly the reasoning
    # that produced [M2-1], where the machinery was right and unreached.
    #
    # Both halves are checked, because they fail differently. The package must
    # be internally consistent -- the body the Maintainer READ has to be the
    # body its stated digest covers, or the digest they confirmed described
    # something else. And the package's report must equal stage 2's own.
    if range_report_digest(pkg["range_report"]) != pkg["range_report_digest"]:
        raise PackageError(
            "the package's range report does not hash to the digest the "
            "package states; the report presented for reading and the digest "
            "confirmed against it are not the same object")
    if pkg["range_report_digest"] != plan["range_report_digest"]:
        raise PackageError(
            f"the report the Maintainer authorized digests to "
            f"{pkg['range_report_digest'][:12]}; stage 2 re-derives "
            f"{plan['range_report_digest'][:12]}. The checkpoint would bind a "
            f"state nobody read.")
    if pkg["candidate_tree"] != plan["candidate_tree"]:
        raise PackageError(
            f"the package names candidate tree {pkg['candidate_tree'][:12]}; "
            f"this commit's tree is {str(plan['candidate_tree'])[:12]}")

    out.write("\n--- range-review report (the authorized state) ---\n")
    out.write(json.dumps(plan["range_report"], indent=2, sort_keys=True) + "\n")
    out.write(f"range-report digest: {plan['range_report_digest']}\n")
    out.write(f"candidate tree     : {plan['candidate_tree']}\n")

    rederive_and_bind(report.facts["anchor"], report.facts["head"],
                      branch=branch, expected_old=branch_old,
                      confirmed_digest=plan["range_report_digest"], repo=repo,
                      prospective_manifest=manifest_bytes)

    verify_message_binds_report(
        plan["message"], digest=plan["range_report_digest"],
        tree=plan["candidate_tree"], head=report.facts["head"],
        anchor=report.facts["anchor"])

    with anchored_roster(anchor, repo=repo) as (roster_path, roster_text):
        principals = parse_principals(roster_text)
        new, manifest_blob = _construct_signed_commit(
            repo, head, manifest_bytes, plan["message"],
            signing_key=stage2_key)
        verify_constructed(repo, new, head,
                           manifest_sha256=committed_sha256,
                           message=plan["message"], principals=principals,
                           roster_path=roster_path,
                           expected_fingerprint=pkg["signing_key_fingerprint"])
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
          trusted_ref: str = "HEAD",
          admitted_authority: dict | None = None) -> Report:
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
    check_authority_closure(anchor, report, repo=repo,
                            admitted_authority=admitted_authority)
    check_authority_modules(anchor, report, repo=repo,
                            admitted_authority=admitted_authority)
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
                        "the signing stage, which takes its authorization "
                        "from a package confirmed by external digest ([S2]).")
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
    s1 = sub.add_parser(
        "stage1",
        help="STAGE 1 -- executes candidate code with the key channel probed "
             "unavailable; writes the authorization package and exits")
    s1.add_argument("--repo", default=None, help=_REPO_HELP)
    s1.add_argument("--signing-key", required=True,
                    help="the RECORDED path to the ceremony signing key's "
                         "public half. Recorded, never discovered -- the probe "
                         "must target the channel the Maintainer names.")
    s1.add_argument("--package-out", required=True,
                    help="where to write the authorization package; must not "
                         "already exist and must not be a symlink")
    s1.add_argument("--transition-from-review", default=None,
                    dest="review_manifest",
                    help="TRANSITION MODE: the Maintainer's out-of-band review "
                         "manifest (selection already happened in the loader)")
    s1.add_argument("--reviewed-candidate", default=None,
                    help="TRANSITION MODE: the commit OID the loader resolved")

    a = sub.add_parser(
        "stage2",
        help="STAGE 2 -- no candidate code; validates the confirmed package, "
             "constructs and verifies the checkpoint, then moves branch and "
             "anchor in ONE transaction -- Maintainer-only")
    a.add_argument("--repo", default=None, help=_REPO_HELP)
    a.add_argument("--package", required=True,
                   help="the authorization package stage 1 wrote")
    a.add_argument("--signing-key", required=True,
                   help="the SAME recorded public-key path stage 1 probed. "
                        "Stage 2 re-derives its fingerprint and refuses unless "
                        "it matches the one bound into the package ([S1]).")
    a.add_argument("--confirm-package-sha256", required=True,
                   dest="confirmed_package_sha256",
                   help="the Maintainer's confirmation of the EXACT bytes "
                        "stage 1 wrote. No digest inside the package can "
                        "satisfy this.")
    a.add_argument("--transition-from-review", default=None,
                   dest="review_manifest",
                   help="TRANSITION MODE: the Maintainer's out-of-band review "
                        "manifest. Selection already happened in the fixed "
                        "loader; this is defence-in-depth revalidation.")
    a.add_argument("--reviewed-candidate", default=None,
                   help="TRANSITION MODE: the commit OID the loader resolved "
                        "once and extracted by. Never re-resolved here.")
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

    if args.cmd in ("stage1", "stage2"):
        # Checked for BOTH stages. Each stage revalidates the transition
        # independently, so each can be given half a mode; a check on stage 1
        # alone would let stage 2 sign a steady-state checkpoint for a run the
        # loader selected in transition mode.
        if bool(args.review_manifest) != bool(args.reviewed_candidate):
            sys.stderr.write(
                "[REFUSE ] transition mode needs both --transition-from-review "
                "and --reviewed-candidate; one alone is not a mode\n")
            return 2

    if args.cmd == "stage1":
        try:
            result = stage1(repo=repo, package_out=Path(args.package_out),
                            signing_key=args.signing_key,
                            review_manifest=args.review_manifest,
                            reviewed_candidate=args.reviewed_candidate)
        except PreflightError as exc:
            sys.stderr.write(f"[REFUSE ] {exc}\n")
            return 2
        json.dump(result, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0

    if args.cmd == "stage2":
        try:
            result = apply_now(
                repo=repo, package=args.package,
                confirmed_package_sha256=args.confirmed_package_sha256,
                signing_key=args.signing_key,
                review_manifest=args.review_manifest,
                reviewed_candidate=args.reviewed_candidate)
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
