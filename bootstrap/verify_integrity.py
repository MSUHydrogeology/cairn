#!/usr/bin/env python3
"""Cairn install-integrity check -- on-disk files vs. the lockfile.

A Cairn install records every written file's SHA-256 in
``dev/.cairn/cairn-lock.yml`` (the module-upgrade arc owns that schema). This
command **verifies** an installed tree against it: it recomputes each
recorded file's hash and reports any **mismatch** (a file modified after
install -- e.g. a tampered shipped script) or **missing** file. It is a
**lockfile-backed preflight**, not an in-file self-verifier: the check lives
*outside* the files it verifies, so there is no bootstrapping problem (a
backdoored script cannot vouch for itself).

It **fails closed**: a missing / unparseable lockfile, a lockfile that
records no files, or any hash mismatch / missing file is a non-zero exit.

Run against an installed target before trusting its scripts:

    python bootstrap/verify_integrity.py --target <repo>

Standard-library only. Reuses the lockfile reader from ``scaffold.py`` so
the schema is single-sourced (this command never writes the lockfile;
``cairn-module-upgrade-3way-merge`` owns its schema + version).

Exit codes: ``0`` every recorded file matches; ``1`` an integrity violation
or a fail-closed condition; ``2`` usage error.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import stat
import sys
from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CAIRN_ROOT))

from bootstrap._scaffold.lockfile import (  # noqa: E402  (trust anchor: narrowest owner, plan 0B.3 / Stage 5)
    _LIVING_STATE_DSTS,
    _LOCKFILE_REL,
    format_forked_facade_warning,
    forked_facade_findings,
    read_lockfile,
)
from bootstrap._scaffold.install import trusted_upstream  # noqa: E402  (fork-advisory comparison source)


#: The slot markers and the customized marker an adopter adds inside a slot
#: they filled (``bootstrap/BOOTSTRAP.md``), matched the way the merge engine
#: reads them (``bootstrap/_scaffold/slotmerge.py``).  Inlined, so this trust
#: check imports nothing from the engine beyond the lockfile reader.  The slot
#: name is bounded so a crafted file cannot make a match backtrack far.
_MARKER_RE = re.compile(
    r"<!--\s*cairn:(?:(slot|end)\s+(\S{1,200}?)|(customized))\s*-->",
    re.IGNORECASE,
)


def _has_customized_slot(text: str) -> bool:
    """True when some slot body carries the customized marker.

    Only a marker inside a slot counts: a file that quotes the marker in
    prose has no filled slot, so its edit is not one ``--finalize`` explains.
    One pass over the markers: a modified file is untrusted input, and
    scanning ahead for each opener's end made a file of unclosed slots cost
    quadratic time.
    """
    open_name: str | None = None
    marked = False
    for m in _MARKER_RE.finditer(text):
        kind, name, customized = m.groups()
        if customized:
            marked = marked or open_name is not None
        elif kind.lower() == "slot":
            open_name, marked = name.lower(), False
        elif open_name is not None and name.lower() == open_name:
            if marked:
                return True
            open_name = None
    return False


#: The most the slot note reads from any one file, in bytes.
_NOTE_CAP = 256 * 1024

#: Where base copies live, relative to the target.  A record whose
#: ``base_cache`` points anywhere else is not read.
_BASE_CACHE_PARTS = ("dev", ".cairn", "base")

#: The reasons a file in scope is not checked, in the order the coverage line
#: reports them.
_NOT_CHECKED = (
    "no base copy", "failed the integrity check", "base hash mismatch",
    "unreadable",
)

#: The section of ``bootstrap/UPGRADE.md`` the note points to.  A test pins
#: that a heading of exactly this name exists there.
_RECORDING_SECTION = "Recording an edit you made"

#: The customized marker and the token pattern, as the merge engine reads
#: them (``bootstrap/_scaffold/slotmerge.py``).  Inlined, so this trust check
#: imports nothing more from the engine; a test pins both to the engine's.
_CUSTOMIZED_RE = re.compile(r"<!--\s*cairn:customized\s*-->", re.IGNORECASE)
_TOKEN_RE = re.compile(r"\{\{(\w+)\}\}")


class _Unreadable(Exception):
    """A file the slot note will not use.  It carries no message: paths and
    names in this check are tree-controlled text."""


def _read_bounded(target: Path, rel: object, under: tuple[str, ...] = ()) -> bytes:
    """The bytes of one file under *target*, or ``_Unreadable``.

    The one way the slot note opens a file.  *rel* must be a relative path
    with no ``..`` and no NUL, lying under *under* when that is given, and
    no part of it from *target* down may be a symlink.  The file is opened
    once, without following a link and without blocking, and read through
    that descriptor only if it is a regular file; at most the cap plus one
    byte is read, so a file larger than the cap is refused rather than
    truncated.  The open flags are built here, not at import time, so a
    platform that lacks one of them still imports the module.
    """
    if not isinstance(rel, str) or not rel or "\x00" in rel:
        raise _Unreadable
    path = Path(rel)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise _Unreadable
    if under and path.parts[:len(under)] != under:
        raise _Unreadable
    current = str(target)
    for part in path.parts:
        current = os.path.join(current, part)
        if stat.S_ISLNK(os.lstat(current).st_mode):
            raise _Unreadable
    flags = os.O_RDONLY
    for name in ("O_NOFOLLOW", "O_NONBLOCK", "O_NOCTTY", "O_BINARY"):
        flags |= getattr(os, name, 0)
    fd = os.open(current, flags)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise _Unreadable
        chunks: list[bytes] = []
        total = 0
        while total <= _NOTE_CAP:
            chunk = os.read(fd, _NOTE_CAP + 1 - total)
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
    finally:
        os.close(fd)
    if total > _NOTE_CAP:
        raise _Unreadable
    return b"".join(chunks)


def _usable_tokens(tokens: object) -> dict | None:
    """The lockfile's token mapping if it is a string-to-string mapping, else
    ``None``.  An unusable mapping is never read as "no tokens": that would
    make every templated slot look filled."""
    if tokens is None:
        return {}
    if not isinstance(tokens, dict):
        return None
    if not all(isinstance(k, str) and isinstance(v, str)
               for k, v in tokens.items()):
        return None
    return tokens


def _slots(text: str) -> dict[str, tuple[str, str]]:
    """The slots that open and close in *text*: lower-case name -> (name as
    written, body).

    One pass over the markers, keeping at most one slot open, so each
    character belongs to at most one body and a file of unclosed or repeated
    openers costs linear time.  A slot that never closes, or whose closer
    names another slot, is not returned; the first complete pair for a name
    wins.
    """
    found: dict[str, tuple[str, str]] = {}
    open_name: str | None = None
    written = ""
    body_start = 0
    for m in _MARKER_RE.finditer(text):
        kind, name, customized = m.groups()
        if customized:
            continue
        if kind.lower() == "slot":
            open_name, written, body_start = name.lower(), name, m.end()
        elif open_name is not None and name.lower() == open_name:
            found.setdefault(open_name, (written, text[body_start:m.start()]))
            open_name = None
    return found


def _squeeze(text: str) -> str:
    """Whitespace-normalized form for comparing two slot bodies: every line
    stripped, blank lines dropped (the merge engine's own rule)."""
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def _substituted(body: str, tokens: dict, limit: int = _NOTE_CAP) -> str | None:
    """*body* with the recorded tokens substituted and unknown ones left
    intact, or ``None`` if the result would be longer than *limit*.

    The length is worked out from the token matches first, so a result that
    large is never built: the lockfile's token values are read without a cap,
    and a small body of tokens can stand for hundreds of megabytes.  The caller
    passes what is left of the file's budget, so the cap bounds the whole file
    and not each slot in it.
    """
    total = len(body)
    for m in _TOKEN_RE.finditer(body):
        value = tokens.get(m.group(1))
        if value is not None:
            total += len(value) - len(m.group(0))
    if total > limit:
        return None
    return _TOKEN_RE.sub(lambda m: tokens.get(m.group(1), m.group(0)), body)


def _note_file(target: Path, rec: dict, installed: bytes | None,
               tokens: dict | None) -> tuple[str, int, list, int]:
    """One in-scope file: ``(bucket, slots checked, names still holding
    Cairn's text, empty slots)``.  The bucket is ``"checked"`` or a reason in
    ``_NOT_CHECKED``.  Any exception for a single record counts that record as
    unreadable and never reaches the rest of the note.

    A slot is listed when its body equals the base copy's after spacing is
    normalized and the recorded tokens are substituted, unless it carries the
    customized marker.  A slot that is blank in the base copy as well is
    counted, not listed: nothing was shipped in it to leave in place.
    """
    try:
        base_rel = rec.get("base_cache")
        if base_rel is None:
            return "no base copy", 0, [], 0
        base_bytes = _read_bounded(target, base_rel, _BASE_CACHE_PARTS)
        recorded = rec.get("base_hash")
        if not (isinstance(recorded, str) and recorded
                == "sha256:" + hashlib.sha256(base_bytes).hexdigest()):
            return "base hash mismatch", 0, [], 0
        if tokens is None:
            return "unreadable", 0, [], 0
        if installed is None:
            installed = _read_bounded(target, rec.get("dst"))
        elif len(installed) > _NOTE_CAP:
            return "unreadable", 0, [], 0
        held = _slots(installed.decode("utf-8"))
        checked = empty = 0
        budget = _NOTE_CAP
        listed: list[str] = []
        for key, (name, base_body) in _slots(base_bytes.decode("utf-8")).items():
            if key not in held:
                continue
            checked += 1
            installed_body = held[key][1]
            if _CUSTOMIZED_RE.search(installed_body):
                continue
            expected = _substituted(base_body, tokens, budget)
            if expected is None:
                return "unreadable", 0, [], 0
            budget -= len(expected)
            if _squeeze(expected) != _squeeze(installed_body):
                continue
            if base_body.strip():
                listed.append(name)
            else:
                empty += 1
        return "checked", checked, listed, empty
    except Exception:
        return "unreadable", 0, [], 0


def _say(message: str) -> None:
    print("slot note: " + message, file=sys.stderr)


def _slot_note(target: Path, accepted: list, living: list, tokens: object,
               failed: int) -> None:
    """Advisory note on the slots an install still holds in Cairn's text.

    It runs after the verdict is fixed and the report is printed, reads
    nothing the integrity pass did not accept (plus the legitimate
    living-state files), and writes to stderr only.  It receives the accepted
    non-verbatim records with the bytes the integrity pass already read, the
    legitimate living-state records, the lockfile's tokens, and how many
    in-scope records did not pass -- never the violation list, the skipped
    count or the exit code, so it has nothing to change them with.

    It prints no command of its own: it reports where a slot still holds
    Cairn's text and leaves the adopter to read the file and decide.  Every
    name and path it prints goes through ``ascii()``, which escapes control
    and non-ASCII characters but leaves other printable text alone, so a path
    or slot name from the tree is shown quoted and can spell any printable text.
    """
    usable = _usable_tokens(tokens)
    counts = dict.fromkeys(("checked",) + _NOT_CHECKED, 0)
    counts["failed the integrity check"] = (
        failed if isinstance(failed, int) and failed > 0 else 0)
    slots_checked = empty = 0
    held: list[tuple[object, str, bool]] = []
    work = [(rec, installed, False) for rec, installed in accepted]
    work += [(rec, None, True) for rec in living if not rec.get("verbatim")]
    for rec, installed, is_living in work:
        bucket, checked, names, blank = _note_file(target, rec, installed, usable)
        counts[bucket] += 1
        slots_checked += checked
        empty += blank
        held += [(rec.get("dst"), name, is_living) for name in names]
    for path, name, is_living in held:
        advice = ("This is project state: fill it in." if is_living else
                  "Write the content, or N/A: <reason>. To keep Cairn's text "
                  "on purpose, add <!-- cairn:customized --> inside the slot "
                  "instead.")
        _say(f"{ascii(path)} slot {ascii(name)} still holds the text Cairn "
             f"shipped. {advice}")
    _say(f"files in scope {sum(counts.values())}; "
         f"checked {counts['checked']}; slots checked {slots_checked}, "
         f"listed {len(held)}, "
         f"empty (filled when its module is installed) {empty}; "
         f"not checked: "
         + ", ".join(f"{name} {counts[name]}" for name in _NOT_CHECKED))
    if held or counts["failed the integrity check"]:
        _say("This check keeps only a hash of each file, not its text, so it "
             "cannot show you what changed. Before you record an edit, read "
             "the whole file and confirm your edit is the only change.")
        _say(f"See bootstrap/UPGRADE.md > {_RECORDING_SECTION}.")


def _stop_writing_to_stderr() -> None:
    """Point descriptor 2 at the null device.

    Called when a write to stderr has failed because whatever read it has gone
    (as ``grep -q`` and ``head`` go).  Python keeps the unwritten text and tries
    again when it exits, and that second failure turns the exit code of a run
    that passed into 120.  Redirecting the descriptor lets the exit-time flush
    succeed; nothing is read from stderr after this point anyway.
    """
    try:
        null = os.open(os.devnull, os.O_WRONLY)
        try:
            os.dup2(null, sys.stderr.fileno())
        finally:
            os.close(null)
    except Exception:
        return


def _run_slot_note(target: Path, files: list, accepted: list, living: list,
                   tokens: object) -> None:
    """Run the note inside a fence.  An exception, ``SystemExit`` included,
    becomes one line naming its type -- never its message, which can carry
    text from the tree.  ``KeyboardInterrupt`` is not caught.  The caller's
    exit code was fixed before this runs and is returned unchanged."""
    try:
        sys.stdout.flush()
        failed = (sum(1 for r in files if not r.get("verbatim"))
                  - len(accepted)
                  - sum(1 for r in living if not r.get("verbatim")))
        _slot_note(target, accepted, living, tokens, failed)
    except (Exception, SystemExit) as exc:
        if isinstance(exc, OSError):
            _stop_writing_to_stderr()
        name = re.sub(r"[^A-Za-z0-9_]", "?", type(exc).__name__)
        try:
            print(f"slot note: not run ({name})", file=sys.stderr)
        except Exception:
            return


def verify(target: Path) -> int:
    lock = read_lockfile(target)
    if lock is None:
        print(f"verify_integrity: no/unparseable {_LOCKFILE_REL} under "
              f"{target} -- FAIL CLOSED (cannot attest integrity without a "
              f"lockfile).", file=sys.stderr)
        return 1
    files = lock.get("files") or []
    if not files:
        print(f"verify_integrity: {_LOCKFILE_REL} records no files -- FAIL "
              f"CLOSED.", file=sys.stderr)
        return 1

    violations: list[str] = []
    customized: list[str] = []
    accepted: list[tuple[dict, bytes]] = []
    living: list[dict] = []
    skipped = 0
    target_resolved = target.resolve()
    for rec in files:
        dst_rel = rec.get("dst")
        recorded = rec.get("hash", "")
        # The lockfile is itself a tamper target, so fail closed on a
        # malformed record *before* reading anything OR honoring any opt-out: a
        # record must name a contained, repo-relative dst with a well-formed
        # sha256 hash.  Without this, a `dst: ../outside` could make the check
        # "attest" a file outside the installed tree and still print OK.
        if not isinstance(dst_rel, str) or not dst_rel:
            violations.append(f"  malformed record (no dst): {rec!r}")
            continue
        rel = Path(dst_rel)
        if rel.is_absolute() or ".." in rel.parts:
            violations.append(f"  unsafe dst (absolute / .. escape): {dst_rel}")
            continue
        if not (isinstance(recorded, str) and recorded.startswith("sha256:")):
            violations.append(f"  malformed hash for {dst_rel}: {recorded!r}")
            continue
        dst = (target / rel).resolve()
        if dst != target_resolved and target_resolved not in dst.parents:
            violations.append(f"  dst escapes the target tree: {dst_rel}")
            continue
        # Living-state opt-out is a *verifier policy*, not a self-asserted
        # lockfile escape hatch.  Adopter-authored project state (a living
        # roadmap, the per-goodnight handoff, the fold-back ledger, the signed
        # agreement) is tracked for upgrade but excluded from the tamper check:
        # it is not shipped apparatus, and its churn would red this check on
        # every edit while saying nothing about whether the scripts are
        # trustworthy.  But the flag is honored ONLY for the authoritative set:
        # a record outside it that carries ``living_state: true`` is a tamper
        # attempt (mark a modified script living-state to hide it) and fails
        # closed -- the integrity boundary is enforced here, not trusted from
        # the (itself-tamperable) lockfile.
        if rec.get("living_state"):
            if dst_rel in _LIVING_STATE_DSTS:
                skipped += 1
                living.append(rec)
                continue
            violations.append(
                f"  illegal living_state opt-out: {dst_rel} is not an "
                f"authoritative living-state path -- only "
                f"{sorted(_LIVING_STATE_DSTS)} may set living_state "
                f"(tamper / malformed lockfile)")
            continue
        if not dst.is_file():
            violations.append(f"  missing: {dst_rel}")
            continue
        on_disk = dst.read_bytes()
        actual = "sha256:" + hashlib.sha256(on_disk).hexdigest()
        if actual != recorded:
            violations.append(f"  modified (hash mismatch): {dst_rel}")
            if _has_customized_slot(on_disk.decode("utf-8", errors="replace")):
                customized.append(dst_rel)
        elif not rec.get("verbatim"):
            accepted.append((rec, on_disk[:_NOTE_CAP + 1]))

    # Advisory (rollup #4): a verbatim facade forked from upstream whose engine
    # package is installed-but-dormant passes the hash check above (on-disk ==
    # the finalized hash) yet runs an un-maintained fork. Surface it -- but
    # honor the per-record fork_acknowledged opt-out at verify time so a
    # deliberate long-term fork does not re-warn on every pre-commit / CI run.
    # Advisory only: it never adds a violation or changes the exit code.
    # The comparison bytes come from THIS checkout -- CAIRN_ROOT is resolved
    # from this script's own on-disk location, never from `target` and never
    # from the target's lockfile. The note means "differs from the upstream in
    # the verifier checkout you ran".
    for finding in forked_facade_findings(
            target, lock, upstream=trusted_upstream(CAIRN_ROOT)):
        if not finding["acknowledged"]:
            print(format_forked_facade_warning(finding, at_upgrade=False),
                  file=sys.stderr, end="")

    if violations:
        print(f"verify_integrity: {len(violations)} integrity violation(s) "
              f"vs. {_LOCKFILE_REL}:\n" + "\n".join(violations)
              + "\nThe on-disk tree no longer matches its recorded install. "
              "Do not trust the shipped scripts until this is resolved.",
              file=sys.stderr)
        if customized:
            # Named only for files with a slot marked customized: a filled
            # slot is an expected edit, and --finalize is how it is recorded.
            # Suggesting it for any other mismatch would invite an adopter to
            # bless a change nobody can explain.  --finalize records the whole
            # file and the marker vouches only for its slot, so the adopter
            # checks the rest before recording it.
            print("A modified file with a slot marked "
                  "`<!-- cairn:customized -->` is usually a slot you filled "
                  "on purpose. This check keeps only a hash, not the text, so "
                  "it cannot show you what changed: read the whole file in "
                  "your repository (history misses uncommitted edits) and "
                  "confirm that your fill is there and nothing outside its "
                  "slots changed (--finalize records the whole file). Then "
                  "record it: python bootstrap/scaffold.py "
                  "upgrade --target <repo> --finalize " + " ".join(customized),
                  file=sys.stderr)
        _run_slot_note(target, files, accepted, living, lock.get("tokens"))
        return 1
    checked = len(files) - skipped
    extra = (f" ({skipped} adopter-authored living-state file(s) tracked for "
             f"upgrade but excluded from the tamper check)" if skipped else "")
    print(f"verify_integrity: OK -- {checked} recorded file(s) match "
          f"{_LOCKFILE_REL}{extra}.")
    _run_slot_note(target, files, accepted, living, lock.get("tokens"))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="verify_integrity",
        description="Verify an installed Cairn tree against its lockfile "
                    "(fail-closed SHA-256 integrity check).")
    parser.add_argument("--target", type=Path, required=True,
                        help="The installed repository to verify.")
    args = parser.parse_args(argv)
    target = args.target.resolve()
    if not target.is_dir():
        print(f"verify_integrity: target is not a directory: {target}",
              file=sys.stderr)
        return 2
    return verify(target)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
