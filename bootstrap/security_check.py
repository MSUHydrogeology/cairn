#!/usr/bin/env python3
"""Cairn release security check -- fail-closed (never skips).

The dev-time Bandit gate (``bootstrap/tests/test_security_lint.py``)
*skips* when Bandit is absent locally, so a contributor without dev-deps
is not blocked. That is the wrong posture for a **release**: "the security
gate may have skipped on the machine that cut the release" is not
acceptable evidence. This command is the release-facing counterpart -- it
**fails closed**. A missing Bandit, a scanner error, a requested file the
scanner could not open, or any unallowlisted MEDIUM+ finding is a non-zero
exit.

Run from the Cairn repo root, before cutting a release (and record its
output in the release notes / checklist):

    python bootstrap/security_check.py

**A repository-state preflight runs first and stops the command on failure**:
the invocation must name the checkout root, the worktree must be clean of
tracked *and untracked* changes, and ``HEAD`` must resolve to a full commit id.
A release security run is evidence about a *commit*; over a dirty tree it is
evidence about bytes nobody can fetch. The same state is re-checked after the
phases, and the full ``HEAD`` is printed in the summary so release notes can
bind the run to the tagged commit.

The checking phases do not execute from that operator checkout. The parent
creates a detached temporary worktree at the preflight commit, verifies every
leaf against the commit's Git blob id (and rejects extra ignored leaves), then
executes the committed checker there. The bytes are verified again before the
temporary worktree is removed. Thus an ignored pytest plugin or bytecode file
cannot influence the verdict, and repository-local checkout filters are never
executed while constructing the evidence tree.

**Four phases**, and every phase after the preflight is *attempted* even once
an earlier one has failed, so one run yields a complete repair list:

1. the repository-state preflight above;
2. Bandit over the derived shipped surface, plus the Markdown self-check
   (``scripts/check_cairn.py``);
3. the whole engine suite (``bootstrap/tests``) in **release mode** -- see
   :data:`RELEASE_GATE_ENV`: a skipped, xfailed or xpassed outcome is
   incomplete release evidence and makes the session non-zero;
4. ``scripts/quality_gate.py`` (order-independence + vendor-neutrality +
   redundancy).

``PASS`` requires both state checks and all three checking phases clean. A
phase that *failed*, *errored*, was *unavailable*, produced *incomplete
evidence*, or ran against a *changed candidate* is non-zero -- an absent tool
must never read as a pass.

The Bandit surface is the same **derived** one as the dev gate -- every
file the scaffold ships **byte-for-byte** as Python, derived from the
published install manifest (``install_manifest``, the same enumeration
behind ``scaffold.py --manifest``), plus Cairn's own dev scripts and the
scaffold engine. This module is the
single source of the scan-target set and the Bandit allowlist; the dev
gate imports them (no second drift-prone copy).

**What this command does not do**, stated rather than implied: the parent
process that establishes and launches the committed checkout is not
authenticated, and nothing cryptographically binds its output to a release
tag. Running it, reading it, and recording it in the release notes is the
Maintainer's act -- see ``SECURITY.md`` and ``bootstrap/PROVENANCE.md``.

Security-hardening Chunk 7 / R1; manifest derivation per the
``scan-coverage`` plan; four-phase orchestration per the
``release-security-orchestration`` plan.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from collections.abc import Callable, Mapping
from collections.abc import Iterator
from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap._scaffold.config import (  # noqa: E402  (trust anchor: narrowest owner, plan 0B.3 / Stage 4)
    _ALWAYS_ON_MAPPINGS,
    _MODULE_MAPPINGS,
)
from bootstrap._scaffold.install import install_manifest  # noqa: E402

_BLOCKING_SEVERITIES = {"MEDIUM", "HIGH"}

#: The **closed** set of severities a Bandit report may carry. Read from the
#: scanner's own source -- ``bandit.core.constants.RANKING`` under Bandit 1.9.4
#: -- not guessed, and hard-coded rather than imported because this module must
#: load on a machine with no Bandit installed (that is the whole point of the
#: fail-closed absence branch below).
#:
#: A value outside this set is **unclassifiable evidence**, not a
#: low-severity finding. Both severity predicates in this repository treat an
#: unknown value as "below MEDIUM", so a renamed or added Bandit severity would
#: be neither blocking nor liveness-confirming -- silently. Rejecting the report
#: at validation is one rule instead of teaching every predicate a fallback.
_KNOWN_SEVERITIES = frozenset({"UNDEFINED", "LOW", "MEDIUM", "HIGH"})

#: Fields every finding must carry for the rules below to mean anything.
_REQUIRED_FINDING_FIELDS = ("filename", "test_id", "issue_severity",
                            "line_number", "issue_text")
_REQUIRED_ERROR_FIELDS = ("filename", "reason")

#: The release-mode token, and its **one** recognized value (Binding
#: amendment R1). ``bootstrap/tests/conftest.py`` reads exactly this pair and
#: refuses skipped / xfailed / xpassed outcomes when it matches; any other
#: value -- including the variable being absent -- leaves ordinary contributor
#: behaviour untouched. The pair lives here because this command is the only
#: thing that sets it.
RELEASE_GATE_ENV = "CAIRN_RELEASE_GATE_ACTIVE"
RELEASE_GATE_VALUE = "1"

#: Triaged-acceptable Bandit findings, keyed by (repo-relative file,
#: test_id), each with a mandatory rationale. The single source of truth
#: for both this release command and the dev gate.
#:
#: **Self-retiring.** ``run_bandit`` fails closed on any key here that the
#: scan does not actually report at blocking severity. A suppression that no
#: longer suppresses anything is not harmless: it is a standing permission for
#: a *future* finding at that (file, test_id), granted by a rationale written
#: about code that has since changed, and nothing would say so. Rationale
#: stays mandatory; liveness is an **additional** condition, not a substitute.
#:
#: Empty as of 2026-08-05: the sole entry
#: (``templates/modules/team-gated/link_check.py``, ``B310``) was measured
#: absent from the report -- Bandit 1.9.4 under Python 3.13.13 reports only
#: LOW findings there -- and was deleted rather than left as a latch. Its
#: rationale (the opt-in, SSRF-guarded external-link probe) is preserved in
#: that module and in ``SECURITY.md``'s documented residual risks; it is not
#: lost by the deletion.
ALLOWLIST: dict[tuple[str, str], str] = {}


# ===========================================================================
# Phase 1 -- repository-state preflight / postflight
# ===========================================================================
#
# A release security run is evidence ABOUT A COMMIT. Run over a dirty tree it
# is evidence about nothing citable: the bytes that were scanned are not the
# bytes anyone can fetch. So the command establishes three facts before any
# scanner runs -- this invocation names the checkout root, the worktree is
# clean of tracked AND untracked changes, and HEAD resolves to a full commit
# id -- and re-establishes the first two afterwards, so a candidate that
# changed mid-run cannot be reported as clean.
#
# Untracked files are refused, not tolerated. Cairn's own tree reproduced the
# fail-open on 2026-08-05: an untracked `.py` under a scanned root is a file
# the release scan may open and no adopter can fetch.


class _RepoStateError(RuntimeError):
    """A repository fact the command could not establish.

    Never converted into "the fact does not hold" -- an unestablishable state
    is a fail-closed condition of its own, which is why every raiser reports
    the git stderr rather than returning a bare False.
    """


#: Git config forced onto every invocation below. Same posture -- and the
#: same reasons, each verified against a real attack in that module's review
#: rounds -- as ``bootstrap/tests/_gate_preflight._STERILE_CONFIG``: an
#: in-repo ``.git/config`` key must not be able to steer, or execute during,
#: the state check that decides whether a release may be cut. Command-line
#: ``-c`` outranks system, global, repository and worktree config.
#:
#: Deliberately a NARROW SECOND INSTANCE rather than an import. The trust-root
#: pattern lives in ``bootstrap/tests/`` and pulls in ``_gate_manifest`` and
#: ``_gate_reanchor``; importing the test package into the release command
#: would make Cairn's release gate depend on its own gate-ceremony tooling and
#: invert the dependency direction. What is reused is the pattern, named here
#: so the two can be compared by a reader.
_STERILE_GIT_CONFIG: dict[str, str] = {
    "core.useReplaceRefs": "false",   # refs/replace/<sha> forges `show` output
    "core.hooksPath": os.devnull,     # a hook is candidate-supplied execution
    "core.fsmonitor": "false",        # a monitor program runs during `status`
    "core.quotePath": "false",        # non-ASCII paths must read back raw
    "diff.external": "",
    "core.pager": "cat",
}


def _sterile_git_env() -> dict[str, str]:
    """The child environment for the state-check git calls.

    Every ``GIT_*`` variable is **dropped** rather than denylisted by name.
    The steering set is large (``GIT_DIR``, ``GIT_WORK_TREE``,
    ``GIT_INDEX_FILE``, ``GIT_CONFIG_*``, ``GIT_EXTERNAL_DIFF``,
    ``GIT_OBJECT_DIRECTORY``, the pathspec flags) and grows between releases,
    so dropping the prefix and putting back what is needed fails safe where an
    enumerated denylist does not. The rest of the environment is the
    operator's and is left alone -- a scope statement, not a trust claim.
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def _git_at(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    """Run one text-producing Git command against *repo_root*, sterilised."""
    git = shutil.which("git")
    if git is None:
        raise _RepoStateError("git was not found on PATH")
    overrides: list[str] = []
    for key, value in _STERILE_GIT_CONFIG.items():
        overrides += ["-c", f"{key}={value}"]
    try:
        return subprocess.run(
            [git, "-C", str(repo_root), *overrides, *args],
            capture_output=True, text=True, check=False,
            env=_sterile_git_env(),
        )
    except OSError as exc:
        raise _RepoStateError(f"could not run git ({exc})") from None


def _git(*args: str) -> subprocess.CompletedProcess:
    """Run one Git command against ``CAIRN_ROOT``."""
    return _git_at(CAIRN_ROOT, *args)


def _git_bytes_at(repo_root: Path, *args: str,
                  input_bytes: bytes | None = None) -> subprocess.CompletedProcess:
    """Binary-output counterpart used for NUL-delimited tree records."""
    git = shutil.which("git")
    if git is None:
        raise _RepoStateError("git was not found on PATH")
    overrides: list[str] = []
    for key, value in _STERILE_GIT_CONFIG.items():
        overrides += ["-c", f"{key}={value}"]
    try:
        return subprocess.run(
            [git, "-C", str(repo_root), *overrides, *args],
            capture_output=True, text=False, check=False,
            env=_sterile_git_env(), input=input_bytes,
        )
    except OSError as exc:
        raise _RepoStateError(f"could not run git ({exc})") from None


def _require_checkout_root() -> None:
    """Refuse unless ``CAIRN_ROOT`` is the top level of the worktree.

    ``git -C <path>`` **discovers upward**, so "a repository answered" is not
    "the repository this command names answered": run from a copy of the tree
    nested under some other checkout, every state check below would report on
    that outer repository and the run would pass against a commit the operator
    never named.
    """
    p = _git("rev-parse", "--show-toplevel")
    top = (p.stdout or "").strip()
    if p.returncode != 0 or not top:
        raise _RepoStateError(
            f"{CAIRN_ROOT} is not inside a git repository "
            f"({(p.stderr or '').strip() or 'git rev-parse failed'})")
    if Path(top).resolve() != CAIRN_ROOT.resolve():
        raise _RepoStateError(
            f"{CAIRN_ROOT} is not the top level of a git worktree -- git "
            f"discovered {Path(top).resolve()} by walking upward")


def _head_commit() -> str:
    """The full 40-hex id of ``HEAD``, or raise."""
    p = _git("rev-parse", "--verify", "--end-of-options", "HEAD^{commit}")
    sha = (p.stdout or "").strip()
    if p.returncode != 0 or len(sha) != 40 or any(
            c not in "0123456789abcdef" for c in sha):
        raise _RepoStateError(
            f"HEAD does not resolve to a full commit id "
            f"({(p.stderr or '').strip() or sha!r})")
    return sha


def _dirty_entries() -> list[str]:
    """Porcelain status lines for tracked **and untracked** changes."""
    p = _git("status", "--porcelain", "--untracked-files=all")
    if p.returncode != 0:
        raise _RepoStateError(
            f"could not read the worktree status "
            f"({(p.stderr or '').strip() or 'git status failed'})")
    return [ln for ln in (p.stdout or "").splitlines() if ln.strip()]


def _format_dirty(entries: list[str]) -> str:
    shown = ", ".join(ln[3:] for ln in entries[:5])
    more = f" (+{len(entries) - 5} more)" if len(entries) > 5 else ""
    return shown + more


def repo_state_preflight() -> tuple[int, str | None]:
    """Phase 1. Returns ``(rc, head)``; ``head`` is None on any refusal."""
    try:
        _require_checkout_root()
        head = _head_commit()
        dirty = _dirty_entries()
    except _RepoStateError as exc:
        print(f"security_check: repository state could not be established "
              f"({exc}) -- FAIL CLOSED. A release security run must name the "
              f"commit it is evidence about.", file=sys.stderr)
        return 1, None
    if dirty:
        print(f"security_check: worktree is not clean ({len(dirty)} tracked or "
              f"untracked change(s)) -- FAIL CLOSED. The bytes scanned must be "
              f"the bytes the tagged commit carries: "
              f"{_format_dirty(dirty)}", file=sys.stderr)
        return 1, None
    print(f"security_check: preflight OK -- clean worktree at {head}.")
    return 0, head


def repo_state_postflight(head: str) -> int:
    """Phase 1, second half: the candidate must not have moved mid-run."""
    try:
        now = _head_commit()
        dirty = _dirty_entries()
    except _RepoStateError as exc:
        print(f"security_check: repository state could not be re-established "
              f"after the phases ({exc}) -- FAIL CLOSED.", file=sys.stderr)
        return 1
    if now != head:
        print(f"security_check: HEAD moved during the run ({head} -> {now}) "
              f"-- FAIL CLOSED. The phases above measured a candidate that is "
              f"no longer checked out.", file=sys.stderr)
        return 1
    if dirty:
        print(f"security_check: the worktree was modified during the run "
              f"({len(dirty)} change(s)) -- FAIL CLOSED. "
              f"{_format_dirty(dirty)}", file=sys.stderr)
        return 1
    return 0


def _blob_oid(data: bytes, hex_length: int) -> str:
    """Hash one worktree payload with Git's blob framing."""
    framed = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    if hex_length == 40:
        # The repository's object format chooses this algorithm; this code is
        # reproducing an existing Git oid, not selecting SHA-1 for a new
        # security protocol.
        return hashlib.sha1(framed, usedforsecurity=False).hexdigest()
    if hex_length == 64:
        return hashlib.sha256(framed).hexdigest()
    raise _RepoStateError(
        f"unsupported Git object-id width {hex_length}; cannot verify checkout")


def _committed_blobs(repo_root: Path, head: str) -> dict[str, tuple[str, str]]:
    """Return ``path -> (mode, oid)`` for every committed blob at *head*."""
    proc = _git_bytes_at(repo_root, "ls-tree", "-r", "-z", "--full-tree", head)
    if proc.returncode != 0:
        detail = os.fsdecode(proc.stderr or b"").strip()
        raise _RepoStateError(
            f"could not enumerate committed tree {head} "
            f"({detail or 'git ls-tree failed'})")
    entries: dict[str, tuple[str, str]] = {}
    for record in (proc.stdout or b"").split(b"\0"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b"\t", 1)
            raw_mode, raw_kind, raw_oid = metadata.split(b" ", 2)
        except ValueError as exc:
            raise _RepoStateError(
                "git ls-tree returned a malformed NUL-delimited record") from exc
        rel = os.fsdecode(raw_path)
        path = Path(rel)
        if path.is_absolute() or not path.parts or ".." in path.parts:
            raise _RepoStateError(
                f"committed tree contains unsafe path {rel!r}")
        if raw_kind != b"blob":
            raise _RepoStateError(
                f"committed path {rel!r} is {os.fsdecode(raw_kind)!r}, not a "
                "self-contained blob (submodules are not release evidence)")
        if rel in entries:
            raise _RepoStateError(f"committed tree repeats path {rel!r}")
        entries[rel] = (raw_mode.decode("ascii"), raw_oid.decode("ascii"))
    if not entries:
        raise _RepoStateError("committed tree contains no blobs")
    return entries


def _checkout_leaf_paths(repo_root: Path) -> set[str]:
    """Enumerate every non-directory worktree object except Git metadata."""
    leaves: set[str] = set()
    try:
        for base, dirs, files in os.walk(repo_root, followlinks=False):
            base_path = Path(base)
            if base_path == repo_root:
                dirs[:] = [name for name in dirs if name != ".git"]
                files = [name for name in files if name != ".git"]
            for name in list(dirs):
                candidate = base_path / name
                if candidate.is_symlink():
                    leaves.add(str(candidate.relative_to(repo_root)))
                    dirs.remove(name)
            for name in files:
                leaves.add(str((base_path / name).relative_to(repo_root)))
    except OSError as exc:
        raise _RepoStateError(
            f"could not enumerate detached checkout bytes ({exc})") from None
    return leaves


def _read_committed_payloads(
        repo_root: Path,
        entries: Mapping[str, tuple[str, str]]) -> dict[str, bytes]:
    """Read every requested blob in one ``git cat-file --batch`` exchange."""
    ordered = list(entries.items())
    request = b"".join(oid.encode("ascii") + b"\n"
                       for _rel, (_mode, oid) in ordered)
    proc = _git_bytes_at(
        repo_root, "cat-file", "--batch", input_bytes=request)
    if proc.returncode != 0:
        detail = os.fsdecode(proc.stderr or b"").strip()
        raise _RepoStateError(
            f"could not read committed blobs ({detail or 'git cat-file failed'})")
    output = proc.stdout or b""
    cursor = 0
    payloads: dict[str, bytes] = {}
    for rel, (_mode, expected_oid) in ordered:
        line_end = output.find(b"\n", cursor)
        if line_end < 0:
            raise _RepoStateError("git cat-file returned a truncated header")
        header = output[cursor:line_end].split(b" ")
        if len(header) != 3:
            raise _RepoStateError(
                f"git cat-file returned a malformed header for {rel!r}")
        raw_oid, raw_kind, raw_size = header
        try:
            size = int(raw_size)
        except ValueError as exc:
            raise _RepoStateError(
                f"git cat-file returned a malformed size for {rel!r}") from exc
        cursor = line_end + 1
        end = cursor + size
        if end >= len(output) or output[end:end + 1] != b"\n":
            raise _RepoStateError(
                f"git cat-file returned a truncated payload for {rel!r}")
        if raw_oid.decode("ascii") != expected_oid or raw_kind != b"blob":
            raise _RepoStateError(
                f"git cat-file returned the wrong object for {rel!r}")
        payloads[rel] = output[cursor:end]
        cursor = end + 1
    if cursor != len(output):
        raise _RepoStateError("git cat-file returned unexpected trailing bytes")
    return payloads


def _materialize_committed_checkout(repo_root: Path, head: str) -> None:
    """Populate a ``--no-checkout`` worktree directly from committed blobs.

    Normal checkout invokes configured smudge filters before any verifier can
    inspect their result. Reading objects with ``cat-file`` avoids executing
    those repository-local programs at all.
    """
    entries = _committed_blobs(repo_root, head)
    payloads = _read_committed_payloads(repo_root, entries)
    root = repo_root.resolve(strict=True)
    for rel, (mode, _oid) in entries.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        data = payloads[rel]
        if mode == "120000":
            target = Path(os.fsdecode(data))
            if target.is_absolute():
                raise _RepoStateError(
                    f"committed symlink {rel!r} has an absolute target")
            resolved = (path.parent / target).resolve(strict=False)
            if resolved != root and root not in resolved.parents:
                raise _RepoStateError(
                    f"committed symlink {rel!r} resolves outside the detached "
                    "checkout")
            os.symlink(os.fsdecode(data), path)
        elif mode in {"100644", "100755"}:
            path.write_bytes(data)
            path.chmod(0o755 if mode == "100755" else 0o644)
        else:
            raise _RepoStateError(
                f"committed path {rel!r} has unsupported mode {mode!r}")


def _populate_committed_index(repo_root: Path, head: str) -> None:
    """Make Git's status baseline describe *head* without checking files out.

    ``worktree add --no-checkout`` creates an empty per-worktree index. The
    exact-byte materializer writes the committed files itself, so leaving that
    index empty makes the child preflight report every path as deleted. A plain
    ``read-tree`` updates only the index; it does not run checkout filters or
    replace the blob materialization and verification below.
    """
    proc = _git_at(repo_root, "read-tree", "--reset", head)
    if proc.returncode != 0:
        raise _RepoStateError(
            "could not populate detached checkout index "
            f"({(proc.stderr or '').strip() or 'git read-tree failed'})")


def _verify_committed_checkout(repo_root: Path, head: str) -> None:
    """Require the checkout to contain exactly *head*'s blob bytes.

    ``git worktree add`` can apply configured checkout filters, and ordinary
    status honors ignore rules. Neither is an exact-byte oracle. This verifier
    compares every leaf to the object id in ``ls-tree`` using Git's blob hash,
    rejects extra ignored leaves, and refuses symlinks that resolve outside the
    detached tree.
    """
    try:
        root = repo_root.resolve(strict=True)
    except OSError as exc:
        raise _RepoStateError(
            f"detached checkout root cannot be resolved ({exc})") from None
    expected = _committed_blobs(root, head)
    actual = _checkout_leaf_paths(root)
    expected_paths = set(expected)
    if actual != expected_paths:
        missing = sorted(expected_paths - actual)[:5]
        extra = sorted(actual - expected_paths)[:5]
        raise _RepoStateError(
            "detached checkout does not contain exactly the committed paths "
            f"(missing={missing}, extra={extra})")

    for rel, (mode, oid) in expected.items():
        path = root / rel
        try:
            metadata = path.lstat()
            if mode == "120000":
                if not stat.S_ISLNK(metadata.st_mode):
                    raise _RepoStateError(
                        f"committed symlink {rel!r} is not a symlink on disk")
                data = os.fsencode(os.readlink(path))
                resolved = path.resolve(strict=True)
                if resolved != root and root not in resolved.parents:
                    raise _RepoStateError(
                        f"committed symlink {rel!r} resolves outside the "
                        "detached checkout")
            elif mode in {"100644", "100755"}:
                if not stat.S_ISREG(metadata.st_mode):
                    raise _RepoStateError(
                        f"committed file {rel!r} is not a regular file on disk")
                is_executable = bool(metadata.st_mode & stat.S_IXUSR)
                if is_executable != (mode == "100755"):
                    raise _RepoStateError(
                        f"committed file {rel!r} has the wrong executable mode")
                data = path.read_bytes()
            else:
                raise _RepoStateError(
                    f"committed path {rel!r} has unsupported mode {mode!r}")
        except _RepoStateError:
            raise
        except (OSError, RuntimeError) as exc:
            raise _RepoStateError(
                f"could not read detached checkout path {rel!r} ({exc})") from None
        if _blob_oid(data, len(oid)) != oid:
            raise _RepoStateError(
                f"detached checkout path {rel!r} does not match commit {head}")


@contextmanager
def _detached_checkout(head: str) -> Iterator[Path]:
    """Yield an exact-byte detached worktree for *head*, then remove it."""
    with tempfile.TemporaryDirectory(prefix="cairn-release-") as parent:
        checkout = Path(parent) / "checkout"
        added = False
        try:
            proc = _git("worktree", "add", "--detach", "--no-checkout",
                        str(checkout), head)
            if proc.returncode != 0:
                raise _RepoStateError(
                    "could not create detached release checkout "
                    f"({(proc.stderr or '').strip() or 'git worktree add failed'})")
            added = True
            _populate_committed_index(checkout, head)
            _materialize_committed_checkout(checkout, head)
            _verify_committed_checkout(checkout, head)
            yield checkout
            _verify_committed_checkout(checkout, head)
        finally:
            if added:
                proc = _git("worktree", "remove", "--force", str(checkout))
                if proc.returncode != 0:
                    raise _RepoStateError(
                        "could not remove detached release checkout "
                        f"({(proc.stderr or '').strip() or 'git worktree remove failed'})")


def scan_targets() -> list[str]:
    """The executable surface to scan, derived from Cairn's source of truth:
    every **verbatim** (byte-for-byte, un-substituted) ``.py`` in the
    published install manifest -- the artifacts an adopter runs as code --
    plus Cairn's own dev executables (``scripts/*.py`` + the top-level
    ``bootstrap/`` tools) and the whole scaffold engine package, as explicit
    files. A newly-shipped script is covered automatically; there is no
    hand-maintained list to drift.

    The two registry loops below (``_MODULE_MAPPINGS``, ``_ALWAYS_ON_MAPPINGS``)
    are strictly redundant once the manifest union lands -- measured, their
    43 entries are a subset of the manifest's 45 (``as_of`` 2026-08-05; both
    are dated snapshots that move with every module registration, and no test
    pins either, so re-measure rather than trust them -- what is durable is
    the **subset relation**, not the pair of counts) -- and are **retained on
    purpose**: they are ``set.add`` calls into the same accumulator, so
    "this change cannot shrink the scanned surface" is true by inspection
    rather than by measurement. They are defence in depth, not a second
    guard: what actually catches a shipped ``.py`` falling out of this set is
    the on-disk oracle in ``bootstrap/tests/test_security_lint.py``, whose
    input this function never reads."""
    targets: set[str] = set()
    for specs in _MODULE_MAPPINGS.values():
        for spec in specs:
            if spec.verbatim and spec.src.endswith(".py"):
                targets.add(f"templates/modules/{spec.src}")
    # Always-on EXECUTABLE helpers (onboarding launcher + _onboarding/ engine):
    # the same shipped-verbatim-.py class as a module script, but delivered
    # unconditionally OUTSIDE _MODULE_MAPPINGS (install._ALWAYS_ON_MAPPINGS). They
    # were release-unscanned while side-door-delivered; including them here closes
    # that PRE-EXISTING Bandit blind spot, not just a new one (R1 / side-door
    # parity). Same `templates/modules/{src}` join as the module loop above.
    for spec in _ALWAYS_ON_MAPPINGS:
        if spec.verbatim and spec.src.endswith(".py"):
            targets.add(f"templates/modules/{spec.src}")
    # Cairn's own dev executables: scripts/*.py + the top-level bootstrap/
    # tools (scaffold, security_check, verify_integrity). Non-recursive, so
    # bootstrap/tests/ -- which carry intentional attack fixtures -- are not
    # scanned.
    for sub in ("scripts", "bootstrap"):
        targets.update(
            str(p.relative_to(CAIRN_ROOT))
            for p in (CAIRN_ROOT / sub).glob("*.py")
        )
    # The scaffold engine package (post-split; plan 2026-06-05-scaffold-split,
    # RR3/S4): RECURSE it -- every module under bootstrap/_scaffold/ is
    # privileged implementation, equal in authority to the old monolith, so the
    # non-recursive bootstrap/*.py glob above would leave the engine's guts
    # unscanned after the split. bootstrap/tests/ (intentional attack fixtures)
    # stays excluded. A no-op until the package exists (Stage 0B), so the Bandit
    # surface is unchanged today.
    engine_pkg = CAIRN_ROOT / "bootstrap" / "_scaffold"
    if engine_pkg.is_dir():
        targets.update(
            str(p.relative_to(CAIRN_ROOT))
            for p in engine_pkg.rglob("*.py")
        )
    # Every verbatim .py the scaffold ACTUALLY installs, from the published
    # install manifest -- the same enumeration adopters depend on through
    # `scaffold.py --manifest`. Two facts here are load-bearing:
    #   * `modules=None` means the FULL published catalog. A module subset
    #     would silently shrink the scanned surface, and nothing downstream
    #     would say so.
    #   * This is a UNION WITH the two registry loops above, never a
    #     replacement for them. That framing is what makes "coverage cannot
    #     shrink" checkable by inspection instead of by measurement.
    # It closes a real, 63-day-old miss: `_SKILLS_MAPPINGS` ships the two
    # session-lifecycle tools unconditionally to every adoption and no loop
    # above reaches them (scan-coverage plan, Chunk B / proposal items 1-2).
    for src, _dst, verbatim in install_manifest(modules=None):
        if verbatim and src.endswith(".py"):
            targets.add(f"templates/{src}")
    return sorted(targets)


def _rel(filename: str) -> str:
    try:
        return str(Path(filename).resolve().relative_to(CAIRN_ROOT))
    except ValueError:
        return filename


def is_blocking(finding: Mapping[str, object]) -> bool:
    """**The** blocking predicate over one Bandit finding.

    Exported and called by every consumer -- the release command's suppression
    filter and its allowlist-liveness set here, and (intended) the dev gate in
    ``bootstrap/tests/test_security_lint.py``, which today re-spells severity
    through its own ``_SEVERITY_RANK`` table. The single-sourcing comment on
    that import has always been true of the *data* (``ALLOWLIST``,
    ``scan_targets``) and silent about the *predicate*: two spellings of "is
    this finding blocking" that agree only by having been copied.
    """
    return finding.get("issue_severity") in _BLOCKING_SEVERITIES


def finding_key(finding: Mapping[str, object]) -> tuple[str, str]:
    """The allowlist key of one finding -- the other half of the rule that was
    spelled twice. Normalization lives here, once."""
    return (_rel(str(finding["filename"])), str(finding["test_id"]))


def validate_report(report: object, returncode: int) -> str | None:
    """Semantic validation of a Bandit report. ``None`` means usable.

    "Successfully parsed" must mean a *validated* report, not merely valid
    JSON. Measured against this module's own bytes at ``745c927``, five
    malformations all produced release evidence: ``{}`` with rc 0,
    ``{"errors": [], "results": []}`` with **rc 1**, and
    ``{"errors": [], "results": {}}`` with rc 0 each printed
    ``Bandit clean over 78 shipped file(s)`` and returned 0; ``[]`` and
    ``null`` raised ``AttributeError`` -- non-zero, but a traceback rather than
    a security message. A scanner failure or an incompatible Bandit could
    therefore become release ``PASS``.

    This is semantic checking of a shape the scanner already produces, not a
    schema dependency: nothing is imported to do it.
    """
    if not isinstance(report, dict):
        return (f"top-level JSON is {type(report).__name__}, not an object")
    for field in ("errors", "results"):
        if field not in report:
            return f"required key {field!r} is absent"
        if not isinstance(report[field], list):
            return (f"{field!r} is {type(report[field]).__name__}, not a list "
                    f"-- a mapping-valued {field!r} reads as 'nothing found'")
    for i, error in enumerate(report["errors"]):
        if not isinstance(error, dict):
            return f"errors[{i}] is {type(error).__name__}, not an object"
        missing = [k for k in _REQUIRED_ERROR_FIELDS if k not in error]
        if missing:
            return f"errors[{i}] is missing required field(s) {missing}"
        for field in _REQUIRED_ERROR_FIELDS:
            if not isinstance(error[field], str):
                return f"errors[{i}].{field} is not a string"
    for i, finding in enumerate(report["results"]):
        if not isinstance(finding, dict):
            return f"results[{i}] is {type(finding).__name__}, not an object"
        missing = [k for k in _REQUIRED_FINDING_FIELDS if k not in finding]
        if missing:
            return f"results[{i}] is missing required field(s) {missing}"
        for field in ("filename", "test_id", "issue_severity", "issue_text"):
            if not isinstance(finding[field], str):
                return f"results[{i}].{field} is not a string"
        if (not isinstance(finding["line_number"], int)
                or isinstance(finding["line_number"], bool)):
            return f"results[{i}].line_number is not an integer"
        severity = finding["issue_severity"]
        if severity not in _KNOWN_SEVERITIES:
            return (f"results[{i}] has issue_severity {severity!r}, outside "
                    f"the known set {sorted(_KNOWN_SEVERITIES)} -- "
                    f"unclassifiable evidence, not a low-severity finding")
    # An exit code that contradicts its own report. Bandit exits 1 when it has
    # findings to report, so 1 with nothing in `results` AND nothing in
    # `errors` means the exit code and the body disagree, and one of them is
    # wrong. Only this direction is refused: the converse (rc 0 with findings
    # present) is legitimate under Bandit's severity-threshold flags, and
    # refusing it would be a false refusal rather than a closed hole.
    if returncode == 1 and not report["results"] and not report["errors"]:
        return ("bandit exited 1 -- which it does when it has findings to "
                "report -- with zero results and zero errors; the exit code "
                "and the report contradict each other")
    return None


def run_bandit() -> int:
    """Run Bandit over the derived surface; fail closed on absence/error."""
    # `install_manifest` REFUSES a malformed mapping (duplicate destinations)
    # by raising ValueError. This wrapper is legibility, not new safety:
    # main() wraps run_bandit() in no handler, so an uncaught ValueError
    # already exits non-zero -- it buys a security message instead of a
    # traceback (scan-coverage plan, Chunk B / proposal item 2).
    try:
        scanned = scan_targets()
    except ValueError as exc:
        print("security_check: cannot enumerate the shipped surface "
              f"({exc}) -- FAIL CLOSED.", file=sys.stderr)
        return 1
    targets = [str(CAIRN_ROOT / t) for t in scanned]
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "bandit", "-q", "-f", "json", *targets],
            capture_output=True, text=True, check=False, cwd=str(CAIRN_ROOT),
        )
    except OSError as exc:
        print(f"security_check: cannot run bandit ({exc}) -- FAIL CLOSED.",
              file=sys.stderr)
        return 1
    if (proc.returncode == 127
            or "No module named bandit" in proc.stderr
            or "No module named 'bandit'" in proc.stderr):
        print("security_check: bandit is NOT installed -- FAIL CLOSED. A "
              "release security gate must not be skippable; install bandit "
              "(pip install bandit) and re-run.", file=sys.stderr)
        return 1
    if proc.returncode not in (0, 1):
        print(f"security_check: bandit error (rc={proc.returncode}) -- fail "
              f"closed.\n{proc.stderr[:800]}", file=sys.stderr)
        return 1
    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print("security_check: bandit output was not JSON -- fail closed.",
              file=sys.stderr)
        return 1
    # Validation comes BEFORE the errors check, liveness, and suppression --
    # every rule below reads fields this establishes are present and
    # classifiable. A report the command cannot validate is not a report that
    # came back clean.
    problem = validate_report(report, proc.returncode)
    if problem is not None:
        print(f"security_check: bandit output is not a usable report "
              f"({problem}) -- FAIL CLOSED. A report the command cannot "
              f"validate is not a report that came back clean.",
              file=sys.stderr)
        return 1
    # A file Bandit could not READ is not a file Bandit found clean. Bandit
    # records such a failure (missing file, unparseable source) in the JSON
    # `errors` array, scans the rest, and exits 0 -- so the rc branch above
    # never fires and the run reports clean over a file it never opened.
    # Fail closed here, BEFORE allowlist filtering, matching the scanner-error
    # posture above (scan-coverage plan, Chunk A / [I1]).
    errors = report.get("errors") or []
    if errors:
        detail = "\n".join(
            f"  {_rel(str(e.get('filename', '?')))}: {e.get('reason', '?')}"
            for e in errors
        )
        print("security_check: bandit could not scan "
              f"{len(errors)} requested file(s) -- fail closed. A file the "
              "scanner never opened is not a file it found clean.\n" + detail,
              file=sys.stderr)
        return 1
    # `results` is a list of field-complete findings with classifiable
    # severities: validate_report() established that above, so `.get(... ) or
    # []` defaulting -- which is what let a mapping-valued `results` read as
    # "nothing found" -- is gone.
    results = report["results"]
    blocking = [
        f"  [{f['test_id']} {f['issue_severity']}] {_rel(f['filename'])}:"
        f"{f['line_number']}  {f['issue_text']}"
        for f in results
        if is_blocking(f) and finding_key(f) not in ALLOWLIST
    ]
    # Allowlist liveness. Derived from the **successfully parsed** report only
    # -- every earlier fail-closed branch has already returned, so a partial or
    # unreadable scan can never retire an entry by making its finding "absent".
    #
    # The predicate and the key rule are the SAME functions suppression uses one
    # line above, not a second spelling of them: a liveness set that could
    # disagree with the filter it is meant to describe is how an entry gets
    # called live while suppressing nothing. Blocking severity only, because
    # that is the sole thing the allowlist filters.
    observed = {finding_key(f) for f in results if is_blocking(f)}
    stale = sorted(key for key in ALLOWLIST if key not in observed)
    rc = 0
    if blocking:
        print("security_check: unallowlisted MEDIUM+ Bandit finding(s):\n"
              + "\n".join(blocking), file=sys.stderr)
        rc = 1
    if stale:
        print("security_check: ALLOWLIST entr(ies) the scan does not report at "
              "MEDIUM+ -- fail closed. A suppression that suppresses nothing is "
              "a standing permission for a future finding, granted by a "
              "rationale written about code that has since changed. Delete "
              "it:\n"
              + "\n".join(f"  {path}  {test_id}" for path, test_id in stale),
              file=sys.stderr)
        rc = 1
    if rc:
        return rc
    print(f"security_check: Bandit clean over {len(targets)} shipped file(s) "
          f"({len(ALLOWLIST)} live allowlist entr(ies)).")
    return 0


def run_check_cairn() -> int:
    """Run the Markdown self-check (link / claim / content integrity)."""
    script = CAIRN_ROOT / "scripts" / "check_cairn.py"
    if not script.is_file():
        print(f"security_check: {script} missing -- fail closed.",
              file=sys.stderr)
        return 1
    try:
        return subprocess.run([sys.executable, str(script)],
                              cwd=str(CAIRN_ROOT), check=False).returncode
    except OSError as exc:
        print(f"security_check: cannot run check_cairn ({exc}) -- fail "
              "closed.", file=sys.stderr)
        return 1


def _release_child_env() -> dict[str, str]:
    """The child environment for phases 3 and 4 (**R1.1**).

    Built from a **copy** of ``os.environ`` and passed **explicitly** to both
    subprocesses. Three properties, each load-bearing:

    * a *copy*, so setting the token cannot leak into this process or into a
      sibling phase that must not see it;
    * *explicit*, so the token's arrival does not depend on inheritance being
      left undisturbed by a future edit;
    * a *superset* of the operator's environment, because the quality gate's
      order-independence sub-gate launches pytest as a **grandchild** with no
      ``env=`` of its own (``scripts/quality_gate.py``, argv bound at the
      ``cmd`` assignment, ``subprocess.run`` immediately below). It reaches
      that grandchild by inheritance alone -- which is why the decisive
      regression in ``bootstrap/tests/test_security_check.py`` drives the real
      child path rather than reading this dict back.
    """
    env = dict(os.environ)
    env[RELEASE_GATE_ENV] = RELEASE_GATE_VALUE
    # The detached checkout is exact before phases and must stay exact between
    # them. Pytest's cache provider and Python bytecode are execution byproducts,
    # not release inputs; suppress them instead of teaching the verifier to
    # tolerate uncommitted files.
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTEST_ADDOPTS"] = "-p no:cacheprovider"
    return env


def run_suite() -> int:
    """Phase 3: the whole engine suite, in release mode.

    Output is not captured: the operator records this run in the release
    notes, so the evidence has to be visible while it happens.
    """
    tests = CAIRN_ROOT / "bootstrap" / "tests"
    if not tests.is_dir():
        print(f"security_check: {tests} is missing -- fail closed. A release "
              f"cannot be cut on a suite that is not there.", file=sys.stderr)
        return 1
    print(f"security_check: running the engine suite in release mode "
          f"({RELEASE_GATE_ENV}={RELEASE_GATE_VALUE}) -- skipped, xfailed and "
          f"xpassed outcomes are incomplete release evidence.")
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "bootstrap/tests", "-q"],
            cwd=str(CAIRN_ROOT), env=_release_child_env(), check=False,
        )
    except OSError as exc:
        print(f"security_check: cannot run the suite ({exc}) -- fail closed.",
              file=sys.stderr)
        return 1
    # Every non-zero pytest exit is a refusal, including the ones that are not
    # test failures: 4 (usage error) and 5 (no tests collected) are absent
    # evidence, and absent evidence must not read as a clean gate.
    if proc.returncode != 0:
        print(f"security_check: the release-mode suite exited "
              f"{proc.returncode} -- fail closed.", file=sys.stderr)
        return 1
    return 0


def run_quality_gate() -> int:
    """Phase 4: ``scripts/quality_gate.py`` -- in no release checklist before
    this plan, though it owns the vendor-neutrality gate that protects every
    adopter-facing template."""
    script = CAIRN_ROOT / "scripts" / "quality_gate.py"
    if not script.is_file():
        print(f"security_check: {script} missing -- fail closed.",
              file=sys.stderr)
        return 1
    try:
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(CAIRN_ROOT), env=_release_child_env(), check=False,
        )
    except OSError as exc:
        print(f"security_check: cannot run the quality gate ({exc}) -- fail "
              f"closed.", file=sys.stderr)
        return 1
    if proc.returncode != 0:
        print(f"security_check: quality_gate exited {proc.returncode} -- fail "
              f"closed.", file=sys.stderr)
        return 1
    return 0


def _phases() -> tuple[tuple[str, Callable[[], int]], ...]:
    """The phases attempted after the preflight passes, in order. Every one is
    attempted even after an earlier failure, so a single run yields a complete
    repair list rather than the first thing that broke.

    A **function**, not a module constant, on purpose: a module-level tuple
    binds each runner *by value at import*, so repointing
    ``security_check.run_suite`` -- the ordinary way to isolate one phase --
    would be a silent no-op. That exact trap is documented against
    ``_SKILLS_MAPPINGS`` in ``bootstrap/tests/test_security_lint.py``; the
    globals are resolved here at call time instead.
    """
    return (
        ("bandit", run_bandit),
        ("check_cairn", run_check_cairn),
        ("release-mode suite", run_suite),
        ("quality_gate", run_quality_gate),
    )


def _run_bound_phases(head: str) -> int:
    """Run every checking phase and the checkout postflight.

    Ordinary phase exceptions become labelled failures so later phases still
    produce a repair list. ``KeyboardInterrupt`` and ``SystemExit`` are not
    ``Exception`` subclasses and retain their control-flow semantics.
    """
    rc = 0
    for label, phase in _phases():
        try:
            phase_rc = phase()
        except Exception as exc:  # noqa: BLE001 -- phase failure is evidence
            print(f"security_check: phase {label} raised "
                  f"{type(exc).__name__}: {exc} -- FAIL CLOSED; continuing "
                  "the remaining phases.", file=sys.stderr)
            rc = 1
            continue
        if phase_rc != 0:
            print(f"security_check: phase {label} did not pass.",
                  file=sys.stderr)
            rc = 1
    if repo_state_postflight(head) != 0:
        rc = 1
    return rc


_BOUND_HEAD_ARG = "--_cairn-bound-head"


def _bound_main(expected_head: str) -> int:
    """Internal child entry: run phases only in the detached checkout."""
    rc, head = repo_state_preflight()
    if rc or head is None:
        print("security_check: detached checkout preflight failed -- FAIL "
              "CLOSED.", file=sys.stderr)
        return 1
    if head != expected_head:
        print(f"security_check: detached checkout resolved {head}, expected "
              f"{expected_head} -- FAIL CLOSED.", file=sys.stderr)
        return 1
    rc = _run_bound_phases(head)
    if rc == 0:
        print(f"security_check: committed-checkout phases clean at {head}.")
    return rc


def _run_in_detached_checkout(head: str) -> int:
    """Execute this checker from an exact-byte detached checkout of *head*."""
    try:
        with _detached_checkout(head) as checkout:
            checker = checkout / "bootstrap" / "security_check.py"
            env = dict(os.environ)
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            try:
                proc = subprocess.run(
                    [sys.executable, str(checker), _BOUND_HEAD_ARG, head],
                    cwd=str(checkout), env=env, check=False,
                )
            except OSError as exc:
                print("security_check: cannot launch the detached committed "
                      f"checker ({exc}) -- FAIL CLOSED.", file=sys.stderr)
                return 1
            if proc.returncode != 0:
                print("security_check: detached committed-checkout phases did "
                      f"not pass (rc={proc.returncode}).", file=sys.stderr)
                return 1
    except _RepoStateError as exc:
        print("security_check: detached committed checkout could not be "
              f"established or preserved ({exc}) -- FAIL CLOSED.",
              file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    args = [] if argv is None else list(argv)
    if args:
        if len(args) == 2 and args[0] == _BOUND_HEAD_ARG:
            return _bound_main(args[1])
        print("security_check: unexpected argument(s) -- FAIL CLOSED.",
              file=sys.stderr)
        return 1

    rc, head = repo_state_preflight()
    # `head is None` is unreachable on an rc == 0 path; folded into the same
    # branch so the narrowing is a fail-closed guard rather than an assert
    # (which `python -O` strips out of the one command that must not skip).
    if rc or head is None:
        print("security_check: FAIL -- resolve the above before release.",
              file=sys.stderr)
        return rc or 1
    if _run_in_detached_checkout(head) != 0:
        rc = 1
    if repo_state_postflight(head) != 0:
        rc = 1
    if rc == 0:
        print(f"security_check: PASS -- release security gate clean at {head}. "
              f"Record this commit id with the run in the release notes.")
    else:
        print("security_check: FAIL -- resolve the above before release.",
              file=sys.stderr)
    return rc


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
