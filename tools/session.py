#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Cairn session kernel -- the mechanizable half of the two session routines.

`session-start` gathers orientation state and performs one idempotent write
(the skills fan-out self-heal); `session-end` scaffolds a reflection, offers a
non-destructive handoff preparation path, and runs the destructive prune only
behind an explicit marker and a fail-closed lock. The skills' `SKILL.md` bodies
carry the judgment steps; the mechanical ones live here, because a deterministic
tool beats a prose checklist an agent can misread or skip.

Two safety properties are load-bearing and are not negotiable defaults:

* **No network.** The surface is local git state, the reflections / handoff
  files, and the intents log. Preparation only reads these surfaces; the
  guarded full handoff runs the opted-in Meter refresh before either prune, then
  prunes released pairs from the intents log (`_prune_intents`).
* **Reflection-only by default.**  `session-end` performs only non-destructive
  work; the destructive full-handoff path is gated behind `--handoff` plus a
  maintainer-designation marker and a concurrent-handoff lock.  So even if a
  harness auto-fires `session-end`, the worst case is a stray reflection file,
  never a roadmap scrub.

**Every write is contained.**  A checkout is data the operator did not write -- a
link, a folder, a row in the vendor table -- so no write this module makes may
follow a link or leave the project, whatever those say.  The destination is
checked first (`_assert_not_linked`), and the write itself cannot follow a link
(`_write_replacing`, `_create_text_exclusive`), so a link that appears after the
check is replaced, not followed.  The writes, listed from the tree: the symlink
probe, the skills fan-out (`_heal_skill_symlink`, `_heal_skill_copy`, the
`.gitignore` seed), the reflection scaffold and prune, and the handoff lock.
A race between the check and a write that needs a parent folder swapped for a
link (only a process already on the machine can do that) is the one gap left.
Where the platform has no `O_NOFOLLOW` (Windows), `_read_regular_bytes` compares
the file it opened with the one it checked, by device and inode, instead of
relying on the flag; that platform has not been run.

**This module is a trust root, and that is why it is separate.**
`_resolve_interpreter` reads a per-worktree Git-administration binding and the
caller then *executes* the path it returns. It is a strict
shape validator -- absoluteness, schema, symlink-freedom, the executable bit --
and deliberately not an authenticator: it establishes nothing about Python
identity or provenance. Git supplies the binding location through a scrubbed
environment, and linked or reparse-point paths are refused. The named
interpreter is still refused when git tracks it (see `_binding_untrusted`).
Changes to its schema,
validation order, fallback disposition, warning visibility, or subprocess use
take a Security Review.

It also owns `encode_display`, the single terminal encoder for externally
sourced values.  There is no second escape table in this tree; a fallback would
be a weaker path that engages exactly when something is already wrong.

`session-end` honors `--dry-run`: it prints the planned writes and exits
writing nothing. `session-start` has no `--dry-run` -- it performs one
idempotent write (the skills fan-out self-heal) and there is nothing to
preview, so the flag would promise a preview it cannot give.

Standard-library only, vendor-neutral.  Usage:

    python tools/session.py session-start
    python tools/session.py session-end \
        [--prepare-handoff | --handoff] [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import locale
import os
import re
import secrets
import signal
import socket
import stat
import subprocess
import sys
import threading
import time
import types
import unicodedata
from pathlib import Path
from typing import List, Optional, Tuple


# --- tunable windows (adopter-overridable via flags) -------------------------

#: Reflections older than this are pruned at full-handoff (`session-routines.md`
#: makes reflections ephemeral; durable observations migrate out before then).
_REFLECTION_GRACE_DAYS = 14

#: Released claim/release *pairs* older than this are pruned from the work-intent
#: coordination surface at full handoff.  Independent of the reflection window on
#: purpose: a reflection is a document, a claim is a lock.  Never applied to an
#: *unreleased* claim -- that is a session that died holding a lock, so it is
#: reported instead (proposal 2026-08-11-claude-intent-ledger-pruning).
_INTENT_GRACE_DAYS = 30


#: The compact projection's syntax.  A field value that contained one of these
#: raw could add a column or a row.  They are escaped by the same
#: encoder as everything else, so there is no second escaping rule to keep in
#: step.  (`\n`/`\r`/`\t` are already non-printable, hence redundant with clause
#: 1; naming them here makes the delimiter property assertable on its own.)
_BOARD_FIELD_DELIMITER = "|"

_BOARD_ROW_DELIMITER = "\n"


# --- the terminal encoder ----------------------------------------------------

_DISPLAY_SYNTAX_CHARS = frozenset(
    (_BOARD_FIELD_DELIMITER, _BOARD_ROW_DELIMITER, "\\", "\r", "\t"))


#: The board's serialization guard, **not** a detector policy.  Its population
#: covers the union represented by content scan's `_ZERO_WIDTH`, `_BIDI`,
#: `_LINE_SEPARATORS`, `_IGNORABLE_RANGES`, `_NONCHARACTER_RANGES`, `_TAG_RANGE`
#: and `_ASCII_GUARD` -- duplicated deliberately, because the board must not
#: import the *conditional* content scanner at runtime (it is not installed in
#: every adopter tree).  The duplication is admitted only with the **one-way**
#: drift guard in `bootstrap/tests/test_session_kernel.py`
#: (`TestDirectionalDriftGuard`): the board may escape
#: more than the scanner flags, and may never emit raw a code point the scanner
#: recognizes.  So a newly added printable invisible reddens that test until this
#: table follows it, and narrowing a detector cannot quietly weaken this output.
#:
#: **Numeric endpoints only -- no invisible source character is embedded raw.**
#: That is a contract clause, not a style preference: a table written with
#: literal members would make this file carry the very code points it exists to
#: escape (the same reason content scan holds its own ranges numerically).
#:
#: Rows mirror the scanner's own row identities rather than being merged into the
#: fewest possible spans, so a reader can check coverage row-against-row.
_DISPLAY_UNSAFE_RANGES: Tuple[Tuple[int, int], ...] = (
    (0x00AD, 0x00AD),      # SOFT HYPHEN -- also content scan's _ASCII_GUARD
    (0x034F, 0x034F),      # COMBINING GRAPHEME JOINER (Mn -- printable!)
    (0x061C, 0x061C),      # ARABIC LETTER MARK
    (0x115F, 0x1160),      # HANGUL CHOSEONG / JUNGSEONG FILLER (Lo -- printable!)
    (0x17B4, 0x17B5),      # KHMER VOWEL INHERENT AQ / AA
    (0x180B, 0x180F),      # MONGOLIAN free variation selectors + vowel separator
    (0x200B, 0x200F),      # ZWSP..RLM (zero-width set + LRM/RLM)
    (0x2028, 0x2029),      # LINE / PARAGRAPH SEPARATOR
    (0x202A, 0x202E),      # bidi embeddings / overrides
    (0x2060, 0x206F),      # WORD JOINER, invisible operators, isolates
    (0x3164, 0x3164),      # HANGUL FILLER (Lo -- printable!)
    (0xFDD0, 0xFDEF),      # noncharacters in Arabic Presentation Forms-A
    (0xFE00, 0xFE0F),      # VARIATION SELECTOR-1..16 (Mn -- printable!)
    (0xFEFF, 0xFEFF),      # ZERO WIDTH NO-BREAK SPACE / BOM
    (0xFFA0, 0xFFA0),      # HALFWIDTH HANGUL FILLER (Lo -- printable!)
    (0xFFF0, 0xFFF8),      # reserved
    (0xFFFE, 0xFFFF),      # plane-0 noncharacters
    (0x1BCA0, 0x1BCA3),    # SHORTHAND FORMAT letters
    (0x1D173, 0x1D17A),    # MUSICAL SYMBOL BEGIN BEAM..END PHRASE
    (0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF), (0x3FFFE, 0x3FFFF),
    (0x4FFFE, 0x4FFFF), (0x5FFFE, 0x5FFFF), (0x6FFFE, 0x6FFFF),
    (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF), (0x9FFFE, 0x9FFFF),
    (0xAFFFE, 0xAFFFF), (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF),
    (0xDFFFE, 0xDFFFF),
    (0xE0000, 0xE0FFF),    # the Tag block (a shadow ASCII alphabet) + VS-17..256
    (0xEFFFE, 0xEFFFF), (0xFFFFE, 0xFFFFF), (0x10FFFE, 0x10FFFF),
)


#: Derived from the table, never written as a literal, so it cannot go stale:
#: every covered code point is at or above this, so the range walk below is
#: skipped for anything under it with an identical hit set.
_DISPLAY_UNSAFE_FLOOR = min(lo for lo, _hi in _DISPLAY_UNSAFE_RANGES)


def _display_unsafe_code_point(code_point: int) -> bool:
    """Is *code_point* in `_DISPLAY_UNSAFE_RANGES`?"""
    if code_point < _DISPLAY_UNSAFE_FLOOR:
        return False
    for low, high in _DISPLAY_UNSAFE_RANGES:
        if low <= code_point <= high:
            return True
    return False


def _escape_code_point(char: str) -> str:
    """One printable-ASCII code-point escape.  ANSI ESC never survives raw."""
    code_point = ord(char)
    if code_point < 0x100:
        return f"\\x{code_point:02x}"
    if code_point < 0x10000:
        return f"\\u{code_point:04x}"
    return f"\\U{code_point:08x}"


def encode_display(value: str) -> str:
    """The **one** terminal encoder.

    For each represented code point emit a printable ASCII code-point escape
    when any of these is true:

    1. ``str.isprintable()`` is false;
    2. the code point belongs to `_DISPLAY_UNSAFE_RANGES`; or
    3. it is a row delimiter, field delimiter, backslash, or other syntax
       character whose raw form could alter the compact representation.

    Clause 1 alone was the *rejected* design: the
    combining grapheme joiner, the Hangul fillers and the variation selectors are
    `Mn`/`Lo`, so ``isprintable()`` calls them printable while they are invisible
    on a terminal.  Clause 2 is what closes that residual, and it is why the
    range table exists at all rather than a category sweep.

    Filenames, lifecycle metadata, Git labels and optional intent fields all pass
    through here -- one encoder, so there is no second path with a weaker rule.
    Ordinary printable scientific text is untouched: ASCII space, precomposed
    accented letters, Greek and CJK all survive readable.
    """
    out: List[str] = []
    for char in value:
        if (not char.isprintable()
                or char in _DISPLAY_SYNTAX_CHARS
                or _display_unsafe_code_point(ord(char))):
            out.append(_escape_code_point(char))
        else:
            out.append(char)
    return "".join(out)


def _decode_child_output(value: bytes | str) -> str:
    """Decode a captured child stream like text-mode subprocess, without newline conversion."""
    if isinstance(value, str):
        return value
    return value.decode(locale.getpreferredencoding(False), errors="strict")


def _encode_child_output(value: str, *, terminate: bool = False) -> str:
    """Encode child text while reserving report line breaks to the parent."""
    framed = "\n".join(encode_display(part) for part in value.split("\n"))
    if terminate and framed and not framed.endswith("\n"):
        framed += "\n"
    return framed


#: A handoff lease is considered *expired* after this many seconds without a
#: heartbeat refresh.  Expiry alone never reclaims a lock -- it is one of two
#: conditions; the other is affirmative proof the holder is dead.
_HANDOFF_LEASE_SECONDS = 900


#: Where machine-local lifecycle state lives (gitignored members).  Mirrors the
#: tracked ``dev/.cairn/base/`` cache convention -- ``dev/.cairn/`` is the
#: deployment's machine-state home.
_CAIRN_STATE_DIR = ("dev", ".cairn")


#: The canonical lifecycle-skills source (read directly by the alias-tier
#: harnesses).  Symlink-tier harnesses (the ``tier: symlink`` rows of the
#: routing table; today ``.claude/skills``) fan out to this dir; the
#: session-start self-heal keeps those read-paths in sync.
_AGENTS_SKILLS_DIR = (".agents", "skills")


#: The installed vendor fan-out table the self-heal reads at runtime (the
#: single source of which harness paths are eligible) -- propagated to adopters
#: alongside the canonical skills, so the routine never needs a sibling Cairn
#: checkout to know its targets.  A vendor refresh is a row edit there.
_VENDOR_TARGETS_REL = (".agents", "skills", "_data", "vendor_targets.yml")


_PREFIX = "lifecycle:"


def _emit(message: str) -> None:
    """Print a normal progress line to stdout."""
    print(f"{_PREFIX} {message}")


#: How many *encoded* characters one field may contribute before the tail is
#: elided.  Counted after encoding, never before: the marker is unauthenticated
#: and a source-length cap would let one crafted character buy 10 columns.
_FIELD_LIMIT = 200


def _safe_field(value, *, limit=_FIELD_LIMIT):
    """Render one externally sourced single-line value inert for the stream.

    **The escaping rule is `encode_display`, above, and this function does not
    own one.**  `_safe_field` translates nothing itself: it encodes, then
    truncates.  An earlier version applied a fixed escape table and neither
    `str.isprintable()` nor a code-point range check, which is why it was
    replaced rather than wrapped.

    What that fixed table missed is not hypothetical: the combining grapheme
    joiner, the Hangul fillers, the variation selectors and the whole Tag block
    are `Mn`/`Lo`, so `str.isprintable()` calls them printable and the old table
    listed none of them -- they reached a terminal raw.  One encoder means there
    is no second, weaker path, and the board's directional drift test
    (`bootstrap/tests/test_session_kernel.py`, `TestDirectionalDriftGuard`)
    is what keeps the range table
    ahead of the content scanner for **both** consumers at once.

    **Elision is layered OUTSIDE the encoder, not folded into it** (the same
    cell).  It is a display concern with its own oracle -- a hostile
    4,000-character `**Status**:` value must not own the terminal -- and folding
    a length rule into a code-point rule is how one of them comes to be
    reasoned about as if it were the other.  So the encoder runs first over the
    whole value and the cut is taken from its output, which also makes the cut
    unable to split a *source* character into a half-escape that reads as
    something else.

    **The encoder lives in this module, beside its only two callers.**  It was
    reached through the planner's vocabulary loader while the planner still
    existed; that indirection is gone, and with it the failure mode where a
    session could not start because a *different* tool would not load.  What has
    not changed is the rule the indirection protected: there is exactly one
    encoder and no local escape table anywhere, because a fallback table is a
    second, weaker path that appears precisely when something is already wrong.
    """
    text = encode_display(str(value))
    if limit is not None and len(text) > limit:
        return text[:limit] + "...[+%d chars elided]" % (len(text) - limit)
    return text


def _safe_stream(text: str) -> str:
    """Render a multi-line relay inert while preserving its real line breaks."""
    # split("\n"), never splitlines(): the latter recognizes the separators
    # this helper escapes and would turn attacker-controlled data into lines.
    return "\n".join(_safe_field(line, limit=None) for line in text.split("\n"))


def _emit_section(title: str) -> None:
    """Print a section header so the relayed output is legibly grouped."""
    print(f"\n{_PREFIX} == {title} ==")


def _warn(message: str) -> None:
    """Print a non-fatal advisory to stderr (a skipped optional step, etc.)."""
    print(f"{_PREFIX} NOTE: {message}", file=sys.stderr)


_STALE_WARNED = False


def _warn_stale_once(message: str) -> None:
    """Emit a stale-interpreter warning at most once per process.

    The interpreter resolver is reached up to four times in one
    ``session-end --handoff`` (measured chain: ``_intent_whoami``,
    ``cmd_session_start``, ``_do_reflection``, ``_do_full_handoff``).
    Without this guard an adopter would see the remedy repeated up to four
    times, aggravating alarm fatigue on the one remaining detection signal
    for an absent-path tamper.
    """
    global _STALE_WARNED
    if _STALE_WARNED:
        return
    _STALE_WARNED = True
    _warn(message)


class LifecycleError(RuntimeError):
    """A fatal, *actionable* failure -- never a silent skip.

    Raised when a step cannot proceed and the operator must act (e.g. the
    command is run outside a git repository).  `main` turns it into a non-zero
    exit with the message, not a stack trace.
    """


_GIT_READ_SHA256 = "20bf6ee480e386c84f04f128467b00e35900bd7a34f9fef31f8c5f9b80dbf076"
_GIT_READ_MAX_BYTES = 256 * 1024
_GIT_READ_MODULE = None


def _load_git_read_helper():
    """Read and execute this delivery's literal sibling helper buffer on demand."""
    global _GIT_READ_MODULE
    if _GIT_READ_MODULE is not None:
        return _GIT_READ_MODULE
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "git_read.py"))
    chain = []
    current = os.path.splitdrive(path)[0] + os.sep
    try:
        for part in path[len(current):].split(os.sep):
            if not part:
                continue
            current = os.path.join(current, part)
            info = os.lstat(current)
            attrs = getattr(info, "st_file_attributes", 0)
            if (stat.S_ISLNK(info.st_mode)
                    or attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)):
                raise LifecycleError("Git read helper binding failed")
            if current != path and not stat.S_ISDIR(info.st_mode):
                raise LifecycleError("Git read helper binding failed")
            chain.append((current, info))
        before = chain[-1][1]
        if (not stat.S_ISREG(before.st_mode) or before.st_size < 0
                or before.st_size > _GIT_READ_MAX_BYTES):
            raise LifecycleError("Git read helper binding failed")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        fd = os.open(path, flags)
        try:
            opened = os.fstat(fd)
            key = lambda row: (row.st_dev, row.st_ino, row.st_mode, row.st_size,
                               row.st_mtime_ns, row.st_ctime_ns)
            if not stat.S_ISREG(opened.st_mode) or key(opened) != key(before):
                raise LifecycleError("Git read helper binding failed")
            chunks = []
            remaining = _GIT_READ_MAX_BYTES + 1
            while remaining:
                part = os.read(fd, min(65536, remaining))
                if not part:
                    break
                chunks.append(part)
                remaining -= len(part)
            source = b"".join(chunks)
            after = os.fstat(fd)
            after_chain = [(name, os.lstat(name)) for name, _row in chain]
            if (key(after) != key(opened)
                    or tuple((name, key(row)) for name, row in after_chain)
                    != tuple((name, key(row)) for name, row in chain)
                    or len(source) != opened.st_size
                    or len(source) > _GIT_READ_MAX_BYTES):
                raise LifecycleError("Git read helper binding failed")
        finally:
            os.close(fd)
    except LifecycleError:
        raise
    except (OSError, IndexError):
        raise LifecycleError("Git read helper binding failed") from None
    if hashlib.sha256(source).hexdigest() != _GIT_READ_SHA256:
        raise LifecycleError("Git read helper binding failed")
    module = types.ModuleType("_cairn_verified_session_git_read")
    module.__file__ = "<verified sibling git_read.py buffer>"
    module.__verified_source__ = source
    module.__verified_sha256__ = _GIT_READ_SHA256
    try:
        exec(compile(source, module.__file__, "exec", dont_inherit=True), module.__dict__)
        module.bind_verified_source(source, _GIT_READ_SHA256)
    except Exception:
        raise LifecycleError("Git read helper binding failed") from None
    _GIT_READ_MODULE = module
    return module


def _repo_root(start: Optional[Path] = None) -> Path:
    """Return the git repository root containing `start` (default: cwd).

    Resolved via `git rev-parse` so it is correct regardless of where the
    installed `tools/session.py` sits relative to the working directory.
    """
    cwd = start if start is not None else Path.cwd()
    git_read = _load_git_read_helper()
    result = git_read.run_git(str(cwd), ("rev-parse", "--show-toplevel"))
    if result.state == "absent":
        raise LifecycleError(
            "git was not found on PATH; the lifecycle routines need git to "
            "gather session state.")
    if result.state != "completed" or result.returncode != 0:
        raise LifecycleError(
            "not inside a git repository -- run the lifecycle routines from "
            "within the project checkout.")
    try:
        return Path(result.stdout.decode("utf-8", "strict").strip())
    except UnicodeError:
        raise LifecycleError("Git returned an unreadable repository root") from None


def _git_env() -> dict:
    """A noninteractive, no-pager, no-remote-prompt git environment.

    Keeps git from blocking on a pager or a credential prompt inside a
    non-interactive agent subshell.  (The full subprocess allowlist + network
    block is a security-chunk concern; this is the minimal hygiene the gather
    steps need.)
    """
    env = dict(os.environ)
    env["GIT_PAGER"] = "cat"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def _git(args: List[str], root: Path) -> str:
    """Run a read-only git command at `root` and return its stdout.

    Raises `LifecycleError` (actionable) rather than leaking a traceback.
    """
    result = _load_git_read_helper().run_git(str(root), tuple(args),
                                             output_limit=64 * 1024 * 1024)
    if result.state != "completed" or result.returncode != 0:
        raise LifecycleError("Git read failed; session state is unavailable")
    text = result.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    return _safe_stream(text)


def _intent_whoami(root: Path, *, session_token: bool = False) -> Optional[str]:
    """Return ``intent.py whoami`` output, or ``None`` if unavailable.

    The coordination/intent tool is **optional** (team-gated): a missing or
    unusable tool is a clean ``None``, never a crash -- the default-on lifecycle
    skill must not hard-require it.  With ``session_token=True`` the bare
    per-session digest is returned (``whoami --session-token``); otherwise the
    full ``<tool_tag>-<digest>`` identity.
    """
    intent_tool = _sibling_tool("intent.py")
    if intent_tool is None:
        return None
    try:
        interpreter, _ = _resolve_interpreter(root)
    except LifecycleError as exc:
        _warn(
            f"interpreter binding refused ({exc}); running the optional "
            f"intent tool under the current interpreter instead."
        )
        interpreter = sys.executable
    cmd = [interpreter, str(intent_tool), "whoami"]
    if session_token:
        cmd.append("--session-token")
    try:
        proc = subprocess.run(
            cmd, cwd=str(root), capture_output=True, text=True,
            check=False, env=_git_env(),
        )
    except OSError:
        return None  # intent tool unusable -> caller falls back
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def _resolve_agent(root: Path) -> str:
    """Resolve the agent identifier used in the reflection filename.

    Resolution order, parallel to ``_resolve_session`` so the
    ``<agent>-<session>`` tail reconstructs the intent log's identity:

    1. an explicit ``CAIRN_AGENT`` override;
    2. else the coordination/intent identity -- ``intent.py whoami`` -- with its
       trailing ``-<session_digest>`` stripped to leave the tool tag (so e.g.
       ``claude-e84b19df`` -> ``claude``), when that tool is installed;
    3. else the neutral default ``agent``.

    The value becomes part of a filename, so it is **sanitized to a safe slug**
    (`[A-Za-z0-9._-]` only): an unsanitized value such as ``../../etc/x`` must
    not be able to redirect the reflection write outside ``dev/reflections/``
    (path-containment).  An empty / fully-stripped value falls back to
    ``agent``.
    """
    raw = os.environ.get("CAIRN_AGENT", "").strip()
    if not raw:
        identity = _intent_whoami(root)
        if identity:
            # intent identity is "<tool_tag>-<8-hex digest>"; strip a genuine
            # digest suffix so <agent> is the tool tag and <agent>-<session>
            # reconstructs the identity.  Strip only an exact 8-hex tail, so a
            # hyphenated tool tag or a digest-less identity is left intact.
            head, _, tail = identity.rpartition("-")
            raw = head if head and re.fullmatch(r"[0-9a-f]{8}", tail) else identity
    slug = re.sub(r"[^A-Za-z0-9._-]", "-", raw).strip(".-")
    return slug or "agent"


def _resolve_session(root: Path) -> str:
    """Resolve the per-session token in the reflection filename (fold-back #46).

    Without a session-distinct segment, two concurrent same-agent sessions
    scaffold the *same* ``<date>-<agent>.md`` and clobber each other -- the
    collision #46 fixed in the reflections doctrine but that this CLI had not
    yet honored (#50).  Resolution order, per the reflections doctrine:

    1. an explicit ``CAIRN_SESSION`` override (parallels ``CAIRN_AGENT``);
    2. else the coordination/intent per-session token -- ``intent.py whoami
       --session-token`` (the 8-hex digest of the harness session id) when that
       tool is installed, so the ``<agent>-<session>`` tail reconstructs the
       intent log's ``agent`` field;
    3. else a short **random** token.

    The fallback is random -- never a shared or persisted value -- so two
    concurrent same-agent sessions never resolve the same token (a persisted
    per-checkout token would re-introduce the very collision).  The trade is
    that re-running in one session may scaffold a *second* reflection rather
    than re-opening the first; a new file is recoverable, a clobber is not.
    Sanitized to a filename-safe slug (path-containment).
    """
    raw = os.environ.get("CAIRN_SESSION", "").strip()
    if not raw:
        token = _intent_whoami(root, session_token=True)
        if token:
            raw = token
    if not raw:
        raw = secrets.token_hex(4)
    slug = re.sub(r"[^A-Za-z0-9._-]", "-", raw).strip(".-")
    return slug or secrets.token_hex(4)


def _today() -> str:
    """Today's date as ``YYYY-MM-DD`` (local)."""
    return _dt.date.today().isoformat()


def _sibling_tool(name: str) -> Optional[Path]:
    """Return an installed sibling tool (e.g. ``intent.py``) if present.

    The lifecycle CLI orchestrates other Cairn tools that may or may not be
    installed (they are separate modules).  A missing optional tool is a
    skip-with-note, never a crash -- the default-on lifecycle skill must not
    hard-require a team-gated module.
    """
    candidate = Path(__file__).resolve().parent / name
    return candidate if candidate.is_file() else None


def _state_dir(root: Path) -> Path:
    return root.joinpath(*_CAIRN_STATE_DIR)


def _assert_within(path: Path, base: Path) -> None:
    """Fail closed if `path` would resolve outside `base` (path-containment).

    Defense in depth behind the agent-slug sanitization: every reflection /
    handoff write the CLI performs must land inside its declared surface, so a
    crafted input can never redirect a write elsewhere in (or out of) the repo.
    """
    resolved = (path.parent.resolve() / path.name)
    try:
        resolved.relative_to(base.resolve())
    except ValueError:
        raise LifecycleError(
            f"refusing to write outside {encode_display(str(base))}: "
            f"{encode_display(str(path))}"
        )


_LINK_REFUSAL = "refusing to write through a link: "
_OUTSIDE_REFUSAL = "refusing to write outside the project: "


def _link_refusal(name: str, replace_with: str) -> str:
    """The refusal for a link at *name* (project-relative): which one it is, and
    what to do about it.  The name is passed through ``encode_display``."""
    return (f"{_LINK_REFUSAL}{encode_display(name)} is a link; replace it with a "
            f"real {replace_with} inside the project")


#: Open flags that make the OS refuse a link at the last path component, where
#: the platform has them; ``O_BINARY`` stops newline translation on Windows.
_OPEN_NO_LINK = getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_BINARY", 0)


def _assert_not_linked(dst: Path, root: Path) -> None:
    """Fail closed unless writing *dst* stays inside *root* without crossing a link.

    Three checks, all before anything is written: no folder between *root* and
    *dst* is a link; *dst* itself is not a link (a link to a file inside the
    project is refused too -- the check does not try to judge where a link ends);
    and *dst*, with its folder resolved, is inside *root*.  *dst* must be built
    from *root* (``root / ...``).

    The message names the first link it finds (the project-relative name, passed
    through ``encode_display``) and what to replace it with: a name in a checkout
    is not ours to print raw, and where a link points is never printed.  Callers
    may print the message as is.
    """
    root_real = root.resolve()
    try:
        rel = dst.relative_to(root)
    except ValueError:
        raise LifecycleError(_OUTSIDE_REFUSAL + encode_display(str(dst))) from None
    folder = root
    for part in rel.parts[:-1]:
        folder = folder / part
        if folder.is_symlink():
            raise LifecycleError(
                _link_refusal(folder.relative_to(root).as_posix(), "folder"))
    if dst.is_symlink():
        raise LifecycleError(_link_refusal(rel.as_posix(), "file or folder"))
    try:
        (dst.parent.resolve() / dst.name).relative_to(root_real)
    except ValueError:
        raise LifecycleError(_OUTSIDE_REFUSAL + encode_display(rel.as_posix())) from None


def _write_replacing(dst: Path, data: bytes) -> None:
    """Put *data* at *dst* without ever opening *dst* itself for writing.

    The bytes go to a fresh sibling that is created exclusively, then one rename
    puts it in place.  ``O_EXCL`` fails on any existing name, links included, and
    a rename replaces a link instead of following it, so a link that appears
    after the caller's check is overwritten as a link, never written through.  A
    hard link is replaced the same way, which leaves the other name's bytes alone.
    The permission bits of a regular file being replaced are kept.
    """
    kept_mode = None
    try:
        before = os.lstat(dst)
        if stat.S_ISREG(before.st_mode):
            kept_mode = stat.S_IMODE(before.st_mode)
    except OSError:
        pass
    tmp = dst.with_name(".cairn-write-" + secrets.token_hex(8))
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | _OPEN_NO_LINK, 0o666)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            if kept_mode is not None and hasattr(os, "fchmod"):
                # on the open descriptor, not by name: a name can be swapped for
                # a link, a descriptor cannot
                handle.flush()
                try:
                    os.fchmod(handle.fileno(), kept_mode)
                except OSError:
                    pass
        os.replace(tmp, dst)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _read_regular_bytes(path: Path) -> bytes:
    """Read *path*, refusing a link at the last component and anything that is not
    a regular file (``OSError`` in both cases; a missing file raises
    ``FileNotFoundError``).

    The name is looked at first (``lstat`` does not follow a link), the file is
    opened without following a link and without waiting for a writer (a named
    pipe would otherwise hang the open), and the opened file must be the one that
    was looked at, by device and inode.  That last comparison is what holds where
    the platform has no ``O_NOFOLLOW``."""
    before = os.lstat(path)
    if not stat.S_ISREG(before.st_mode):
        raise OSError("not a regular file")
    fd = os.open(path, os.O_RDONLY | _OPEN_NO_LINK | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(fd, "rb") as handle:
        opened = os.fstat(handle.fileno())
        if (not stat.S_ISREG(opened.st_mode)
                or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)):
            raise OSError("not the file that was checked")
        return handle.read()


def _create_text_exclusive(path: Path, text: str) -> None:
    """Create *path* with *text*; fail (``FileExistsError``) on any existing name,
    a link included, instead of writing through it."""
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | _OPEN_NO_LINK, 0o666)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)


def _has_symlink_component(path: Path) -> bool:
    """True if `path` or any of its parents is a symlink.

    The interpreter trust root must not be reachable through a symlink (leaf or
    parent), since a symlink can be retargeted out-of-band to redirect which
    binary runs.
    """
    cur = path
    while True:
        if cur.is_symlink():
            return True
        if cur.parent == cur:
            return False
        cur = cur.parent


_REBIND_REMEDY = (
    "To refresh it, delete local-env.json under this worktree's Git "
    "administration, then re-run the Cairn scaffold install."
)


def _probe_interpreter(interp: Path) -> str:
    """Classify a recorded path: "symlinked" / "absent" / "present".

    Every inspection step lives here so the caller wraps the whole
    classification in one ``except OSError``.  The symlink walk itself raises
    on an unreadable parent, so guarding only the ``stat()`` probe would leave
    that case an uncaught traceback.
    """
    if _has_symlink_component(interp):        # may raise OSError
        return "symlinked"
    try:
        interp.stat()
    except (FileNotFoundError, NotADirectoryError):
        return "absent"
    return "present"


_INTERPRETER_TRACKED = (
    "the interpreter named by the Git administration binding is inside the project and "
    "tracked by git, so a checkout can replace it.  It was not used: this run uses "
    "the current interpreter.  To fix it: name an interpreter that git does not "
    "track (then re-run the Cairn scaffold install "
    "from the interpreter you want)."
)
_BINDING_UNVERIFIED = (
    "could not verify whether the project tracks the selected interpreter; "
    "refusing to run a sub-tool. Check that git works in this folder."
)

#: How long the question to git may take before it counts as "could not ask".
_BINDING_GIT_TIMEOUT_SECONDS = 30

def _canonical_caseless(text: str) -> str:
    """Fold *text* the way a case- and normalization-insensitive volume does
    (Unicode "canonical caseless matching"): decompose, fold case, decompose,
    fold case, decompose.  ``\u017f`` (long s) becomes ``s`` and a composed letter
    equals its decomposed form -- two spellings git keeps apart and such a volume
    opens as one file.  Compatibility look-alikes (full-width letters) are
    deliberately not folded: no volume treats them as the same name."""
    if text.isascii():
        return text.lower()
    folded = unicodedata.normalize("NFD", text)
    folded = unicodedata.normalize("NFD", folded.casefold())
    return unicodedata.normalize("NFD", folded.casefold())


def _binding_untrusted(root: Path, cfg: Path,
                       interpreter: Optional[Path] = None) -> Optional[str]:
    """Refuse a binding that names an executable tracked in the project."""
    interpreter_target: Optional[str] = None
    if interpreter is not None:
        try:
            root_prefix = _canonical_caseless(root.resolve().as_posix()).rstrip("/") + "/"
        except (OSError, ValueError):
            root_prefix = None
        folded_interpreter = _canonical_caseless(Path(interpreter).as_posix())
        if root_prefix is not None and folded_interpreter.startswith(root_prefix):
            interpreter_target = folded_interpreter[len(root_prefix):]
    try:
        proc = _load_git_read_helper().run_git(
            str(root), ("ls-files", "-z", "--cached", "--stage"),
            timeout=_BINDING_GIT_TIMEOUT_SECONDS, output_limit=64 * 1024 * 1024)
    except LifecycleError:
        return _BINDING_UNVERIFIED
    if proc.state != "completed" or proc.returncode != 0:
        return _BINDING_UNVERIFIED
    interpreter_hit = False
    for record in proc.stdout.split(b"\0"):
        if not record:
            continue
        head, tab, raw_path = record.partition(b"\t")
        if not tab or not head:
            return _BINDING_UNVERIFIED
        entry = raw_path.decode("utf-8", "replace")
        folded = _canonical_caseless(entry)
        gitlink = head.split(b" ", 1)[0] == b"160000"
        if interpreter_target is not None and (
                folded == interpreter_target
                or (gitlink and interpreter_target.startswith(folded + "/"))):
            interpreter_hit = True
    return _INTERPRETER_TRACKED if interpreter_hit else None


def _identity(st: os.stat_result) -> Tuple[int, int]:
    """What the disk calls one file: device and inode."""
    return (st.st_dev, st.st_ino)


def _has_identity(path: Path, identity: Tuple[int, int]) -> bool:
    """True if *path* (not followed, if it is a link) is the file *identity*.

    An inode of 0 is no answer (some disks report it for every file), so it never
    matches: the names are then the only test."""
    if identity[1] == 0:
        return False
    try:
        return _identity(os.lstat(path)) == identity
    except (OSError, ValueError):
        return False


_UNTRUSTED_WARNED = False
_MISSING_BINDING_WARNED = False


def _warn_untrusted_once(message: str) -> None:
    """Say once per process that the binding was not used (the resolver is
    reached several times in one run; `_warn_stale_once` does the same)."""
    global _UNTRUSTED_WARNED
    if _UNTRUSTED_WARNED:
        return
    _UNTRUSTED_WARNED = True
    _warn(message)


def _warn_missing_binding_once() -> None:
    """Surface missing worktree bindings once, with the install remedy."""
    global _MISSING_BINDING_WARNED
    if _MISSING_BINDING_WARNED:
        return
    _MISSING_BINDING_WARNED = True
    _warn(
        "no per-worktree Git interpreter binding -- using the current "
        "interpreter; initialize Git at the project root and rerun the "
        "scaffold install to record this environment."
    )


def _resolve_interpreter(root: Path) -> Tuple[str, str]:
    """Resolve the project interpreter the routines invoke sub-tools with.

    Resolve-don't-bake: the interpreter binding lives under this exact
    worktree's Git administration directory, outside checkout content.

    **The trust-root contract, corrected on the record.**
    The per-worktree ``cairn/local-env.json`` is an **operationally trusted
    executable binding**. It is mutable and not authenticated, so it carries no
    provenance or integrity signal. ``_resolve_interpreter`` is a strict
    **shape validator, not an authenticator**: it enforces absoluteness, a
    single-key schema, control-char rejection, no parent-traversal (``..``)
    segment, symlink-freedom, existence, and the executable bit -- but it
    checks **neither Python identity nor binary provenance**.  Any absolute,
    present, non-symlinked, executable regular file is accepted and
    executed.

    Git discovery uses a scrubbed environment and requires the supplied root
    to match the exact worktree root. Links and reparse points in `.git` or the
    binding path refuse. `_binding_untrusted` also refuses an executable inside
    the project if git tracks it. A copied Git administration directory or a
    delivered regular `.git` pointer can supply a binding; those origins remain
    trusted inputs (`bootstrap/SAFETY.md`).

    A structurally-valid-but-absent path **degrades** with a warning
    (``"fallback-stale"``, below).  Every other violation **refuses before
    running anything** (a `LifecycleError`) at every call site **except**
    ``_intent_whoami``'s optional-tool fallback, which surfaces the refusal
    as a warning and continues under the current interpreter (the intent
    tool is optional and repository-controlled).

    Returns ``(interpreter_path, source)`` where source is ``"local-env.json"``
    or ``"fallback"``. When the binding is absent or this is not the exact
    worktree root, the **runtime resolver
    fallback** is the interpreter currently running this CLI -- safe because
    *this* tool is standard-library only, a rationale scoped to this tool's
    own execution and not to whatever sub-tool the resolved interpreter is
    later used to run -- and the caller surfaces install guidance so the
    hidden binding is never silently assumed.
    """
    cfg = _git_binding_path(root)
    if cfg is None:
        _warn_missing_binding_once()
        return sys.executable, "fallback"
    if _path_has_link_or_reparse(cfg):
        raise LifecycleError("Git interpreter binding path contains a link or reparse point; refusing to run a sub-tool")
    try:
        cfg_stat = os.lstat(cfg)
    except FileNotFoundError:
        _warn_missing_binding_once()
        return sys.executable, "fallback"
    except OSError as exc:
        raise LifecycleError(f"Git interpreter binding could not be inspected: {encode_display(str(exc))}") from exc
    if not stat.S_ISREG(cfg_stat.st_mode):
        raise LifecycleError("Git interpreter binding is not a regular file; refusing to run a sub-tool")
    shown_cfg = encode_display(str(cfg))   # a folder name may be someone else's choice

    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:       # ValueError: bad UTF-8, bad JSON
        raise LifecycleError(
            f"{shown_cfg} is not readable JSON: {encode_display(str(exc))}.  It must be "
            '{{"interpreter": "/abs/path/to/python"}}.'
        ) from exc

    # Strict single-key schema: a tamper-aware trust root should not silently
    # accept extra attacker-controlled fields (review-crispness, finding 4).
    if not isinstance(data, dict) or set(data) != {"interpreter"}:
        raise LifecycleError(
            f'{shown_cfg} must be a JSON object with exactly one key, "interpreter".'
        )
    value = data["interpreter"]
    if not isinstance(value, str) or not value.strip():
        raise LifecycleError(f'{shown_cfg}: "interpreter" must be a non-empty string.')
    # Reject NUL / control characters only.  We invoke as an explicit argv list
    # (never a shell), so shell metacharacters in a path are inert, and spaces
    # are legitimate in real filesystem paths (`My Drive`, OneDrive, profile
    # dirs).  An appended-argument string like "/usr/bin/python -c ..." is not
    # a real path (nothing exists there), so under the revised classifier it
    # DEGRADES as an absent path -- it is never executed, only named in a
    # warning -- not "caught" by any fatal check.
    if any(ord(ch) < 0x20 or ch == "\x7f" for ch in value):
        raise LifecycleError(
            f'{shown_cfg}: "interpreter" must not contain control characters.'
        )
    interp = Path(value)
    # `value` is the binding's own text and only C0 controls and DEL were
    # rejected above, so everything printed from it goes through the encoder
    shown_interp = encode_display(str(interp))
    if not interp.is_absolute():
        raise LifecycleError(f'{shown_cfg}: "interpreter" must be an absolute path.')
    if ".." in interp.parts:
        raise LifecycleError(
            f'{shown_cfg}: "interpreter" must not contain a parent-traversal '
            f"(..) segment: {shown_interp}.  {_REBIND_REMEDY}"
        )
    try:
        shape = _probe_interpreter(interp)
    except (OSError, ValueError) as exc:       # EACCES / ELOOP / ENAMETOOLONG / a
        # string that cannot be a path (a lone surrogate)
        raise LifecycleError(
            f'{shown_cfg}: "interpreter" could not be inspected '
            f'({encode_display(str(exc))}): {shown_interp}.  '
            f"Refusing rather than guessing.  {_REBIND_REMEDY}"
        ) from exc
    if shape == "symlinked":
        raise LifecycleError(
            f'{shown_cfg}: "interpreter" must not be reached through a symlink '
            f"(leaf or parent).  {_REBIND_REMEDY}"
        )
    if shape == "absent":
        _warn_stale_once(
            f'{shown_cfg}: recorded interpreter "{shown_interp}" no longer exists -- your '
            f"environment was likely rebuilt.  Using the current interpreter "
            f"({encode_display(sys.executable)}) for this run.  {_REBIND_REMEDY}"
        )
        return sys.executable, "fallback-stale"
    if not interp.is_file() or not os.access(interp, os.X_OK):
        raise LifecycleError(
            f'{shown_cfg}: "interpreter" is not an executable file: {shown_interp}.  '
            f"{_REBIND_REMEDY}"
        )
    untrusted = _binding_untrusted(root, cfg, interp)
    if untrusted == _BINDING_UNVERIFIED:
        raise LifecycleError(untrusted)
    if untrusted is not None:
        _warn_untrusted_once(untrusted)
        return sys.executable, "fallback-untrusted"
    return str(interp), "local-env.json"


def _path_has_link_or_reparse(path: Path) -> bool:
    """Check each named component without following links or Windows junctions."""
    cur = Path(path.anchor)
    for part in path.parts[1:]:
        cur = cur / part
        try:
            if cur.is_symlink():
                return True
            isjunction = getattr(os.path, "isjunction", None)
            if isjunction and isjunction(cur):
                return True
        except OSError as exc:
            raise LifecycleError("Git interpreter binding path could not be inspected") from exc
    return False


def _git_binding_path(root: Path) -> Optional[Path]:
    """Return this exact worktree's Git-admin binding, or None outside its root."""
    root = root.resolve()
    dotgit = root / ".git"
    pointer_admin: Optional[Path] = None
    if dotgit.exists() or dotgit.is_symlink():
        if dotgit.is_symlink() or (getattr(os.path, "isjunction", None)
                                   and os.path.isjunction(dotgit)):
            raise LifecycleError(".git is a link or reparse point; refusing interpreter discovery")
        try:
            mode = os.lstat(dotgit).st_mode
        except OSError as exc:
            raise LifecycleError(".git could not be inspected") from exc
        if stat.S_ISREG(mode):
            pointer_admin = _read_git_pointer(root, dotgit)
        elif not stat.S_ISDIR(mode):
            raise LifecycleError(".git is not a directory or regular Git pointer file")
    git_read = _load_git_read_helper()
    version = git_read.read_version(str(root))
    if version.state != "completed" or version.returncode != 0:
        raise LifecycleError("git interpreter discovery failed")
    top = git_read.run_git(str(root), ("rev-parse", "--show-toplevel"),
                           timeout=_BINDING_GIT_TIMEOUT_SECONDS)
    if top.state != "completed" or top.returncode != 0:
        if not git_read.worktree_exclusions(str(root)) \
                and not (dotgit.exists() or dotgit.is_symlink()):
            return None
        raise LifecycleError("git could not resolve the worktree root")
    gitdir = git_read.run_git(str(root), ("rev-parse", "--absolute-git-dir"),
                              timeout=_BINDING_GIT_TIMEOUT_SECONDS)
    if gitdir.state != "completed" or gitdir.returncode != 0:
        raise LifecycleError("git could not resolve the Git administration path")
    try:
        top_path = Path(top.stdout.decode("utf-8", "strict").strip()).resolve()
        admin = Path(gitdir.stdout.decode("utf-8", "strict").strip())
    except (UnicodeError, OSError, ValueError) as exc:
        raise LifecycleError("git returned an unreadable interpreter location") from exc
    if top_path != root:
        return None
    if pointer_admin is not None:
        try:
            if pointer_admin.resolve(strict=True) != admin.resolve(strict=True):
                raise LifecycleError(".git pointer and Git administration path disagree")
        except OSError as exc:
            raise LifecycleError(".git pointer target could not be verified") from exc
    return admin / "cairn" / "local-env.json"


def _read_git_pointer(root: Path, dotgit: Path) -> Path:
    """Read a regular `.git` pointer and reject linked/reparse target components."""
    try:
        lines = dotgit.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise LifecycleError(".git pointer could not be read") from exc
    if len(lines) != 1 or not lines[0].startswith("gitdir: "):
        raise LifecycleError(".git is not a valid regular Git pointer file")
    value = lines[0][len("gitdir: "):]
    if not value:
        raise LifecycleError(".git pointer has no administration path")
    pointer = Path(value)
    if not pointer.is_absolute():
        pointer = dotgit.parent / pointer
    pointer = Path(os.path.abspath(pointer))
    if _path_has_link_or_reparse(pointer):
        raise LifecycleError(".git pointer target contains a link or reparse point")
    try:
        if not stat.S_ISDIR(os.stat(pointer).st_mode):
            raise LifecycleError(".git pointer target is not a directory")
    except OSError as exc:
        raise LifecycleError(".git pointer target could not be inspected") from exc
    return pointer


_LINE_ENDING_RE = re.compile(r"\r\n?|\n")


def _split_lines(text: str) -> List[str]:
    """Split on markdown line endings with ``str.splitlines`` tail semantics."""
    if not text:
        return []
    lines = _LINE_ENDING_RE.split(text)
    if lines[-1] == "":
        lines.pop()
    return lines


def _status_of(path: Path) -> str:
    """Best-effort read of a proposal/plan ``**Status**:`` line for the survey."""
    try:
        for line in _split_lines(path.read_text(encoding="utf-8"))[:40]:
            stripped = line.strip()
            low = stripped.lower()
            if low.startswith("**status**:") or low.startswith("status:"):
                value = stripped.split(":", 1)[1].strip().strip("*").strip()
                return value or "(unspecified)"
    except (OSError, UnicodeError):
        pass
    return "(no status line)"


#: The published status words, by artifact kind (AGENTS.md > Lifecycle and records;
#: docs/methodology/lifecycle.md for proposals, docs/methodology/plans.md for plans and change
#: notes). The board loads this table from here rather than keeping its own.
_STATUS_VOCABULARY = {
    "proposal": ("awaiting-review", "revising", "awaiting-decision",
                 "accepted", "rejected", "superseded"),
    "plan": ("awaiting-plan-review", "revising-plan", "ready-to-implement",
             "implementing", "awaiting-code-review", "revising-code",
             "ready-to-archive", "archived"),
}

#: Old words that stay readable on archived records and are named "retired"
#: on an active one. `proposed`, `reviewed` and `revised` are the three the
#: lifecycle doctrine names (docs/methodology/lifecycle.md, the paragraph on the
#: earlier flat tokens). `open`, `executing` and `review` were the plan states
#: retired with them (commit 3defdb78, "retire the legacy status vocabulary").
_RETIRED_STATUSES = ("proposed", "reviewed", "revised",
                     "open", "executing", "review")

#: The word a status line opens with, before any note (`awaiting-decision --
#: ...`, `implementing (round 2)`). Underscores, digits and hyphens stay inside
#: the word, so `awaiting-decision2` and `awaiting-decision-x` are different
#: words from `awaiting-decision`. The word must end at the end of the text, a
#: space or tab, or ASCII punctuation: a non-ASCII or invisible character
#: right after it (`awaiting-decision` plus a zero-width space) makes the word
#: something else rather than being silently dropped.
_STATUS_WORD_RE = re.compile(
    r"^`?(?P<word>[A-Za-z][A-Za-z0-9_-]*)(?=\Z|[ \t]|[!-,./:-@\[-^`{-~])")

#: Most names one advisory line spells out; the rest are counted.
_ADVISORY_NAME_LIMIT = 10


def _status_problem(kind: str, status: str) -> str:
    """`""` if `status` opens with an allowed word for `kind` ("proposal" or
    "plan"), else `"retired"` or `"unknown"`. A blank status, or this survey's
    own placeholder for a line it could not read, has nothing to judge. Bold or
    italic asterisks around the value are not part of the word (the board hands
    over its raw header value; session-start has already stripped them)."""
    text = status.strip().strip("*").strip()
    if not text or text in ("(unspecified)", "(no status line)"):
        return ""
    match = _STATUS_WORD_RE.match(text)
    word = match.group("word") if match else ""
    if word in _STATUS_VOCABULARY[kind]:
        return ""
    return "retired" if word in _RETIRED_STATUSES else "unknown"


def _status_advisory(items: List[Tuple[str, str, str]], encode) -> str:
    """One advisory line naming active artifacts whose status is outside the
    vocabulary, or `""` when there are none. `items` is `(name, kind, status)`;
    `encode` renders an untrusted value inert for the terminal, and the caller
    adds its own line prefix. This only warns: every artifact stays listed. The
    line spells out the first ten and counts the rest."""
    found = []
    total = 0
    for name, kind, status in items:
        problem = _status_problem(kind, status)
        if problem:
            total += 1
            if len(found) < _ADVISORY_NAME_LIMIT:
                found.append(
                    f"{encode(name)} ({encode(status.split()[0])}: {problem})")
    if not total:
        return ""
    noun = "artifact carries" if total == 1 else "artifacts carry"
    listing = ", ".join(found)
    if total > len(found):
        listing += f", and {total - len(found)} more"
    return (f"advisory -- {total} active {noun} a status outside the "
            f"vocabulary: {listing}. The allowed statuses are in "
            f"AGENTS.md > Lifecycle and records.")


def _in_flight_items(root: Path) -> List[Tuple[str, str, str]]:
    """`(kind, file name, status)` for each open proposal and plan under
    `root`, `kind` being `"proposal"` or `"plan"`. The one walk behind the
    in-flight list and the status advisory, so they cannot disagree about which
    files count."""
    items: List[Tuple[str, str, str]] = []
    for kind in ("proposal", "plan"):
        base = root / "dev" / f"{kind}s"
        if not base.is_dir():
            continue
        for path in sorted(base.glob("*.md")):
            if path.name != "_template.md":
                items.append((kind, path.name, _status_of(path)))
    return items


def _in_flight_status_advisory(root: Path) -> str:
    """The advisory line for the open proposals and plans under `root`."""
    return _status_advisory(
        [(f"{kind}s/{name}", kind, status)
         for kind, name, status in _in_flight_items(root)], _safe_field)


def _in_flight(root: Path) -> List[str]:
    """List open proposals/plans (live `dev/` files, excluding archives).

    These are the live multi-agent threads the session-start move surfaces and
    the reflection-only goodnight notes as open work.
    """
    return [f"{kind}s/{_safe_field(name)} -- {_safe_field(status)}"
            for kind, name, status in _in_flight_items(root)]


def _load_vendor_targets(root: Path) -> List[dict]:
    """Read the installed vendor fan-out table.  JSON-encoded (valid YAML 1.2)
    so it parses stdlib-only, like the lockfile.  Absent / unreadable / wrong
    shape -> ``[]`` (the self-heal simply does nothing -- it never crashes the
    orientation gather)."""
    path = root.joinpath(*_VENDOR_TARGETS_REL)
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    targets = data.get("targets") if isinstance(data, dict) else None
    return [r for r in targets if isinstance(r, dict)] if isinstance(targets, list) else []


def _skill_symlinks_available(root: Path) -> bool:
    """Probe whether ``os.symlink`` works under *root* (False on Windows
    without Developer Mode / Administrator -- the copy-fallback trigger).

    The probe name is new on every call.  A fixed name can be taken by a folder
    the project ships, which made the cleanup fail, read as "no symlinks", and
    let a project choose the copy path on any operating system."""
    probe = root / (".cairn-skill-symlink-probe-" + secrets.token_hex(4))
    try:
        os.symlink(".", probe)
    except (OSError, NotImplementedError):
        return False
    try:
        return probe.is_symlink()
    finally:
        try:
            probe.unlink()
        except OSError:
            pass


#: One folder name in a harness read-path.  Narrow on purpose: the text becomes a
#: path and a line in ``.gitignore``, and the project chooses it, so nothing with
#: meaning to a shell, a glob, a comment or a negation, and no newline, gets in.
_VENDOR_PART_RE = re.compile(r"[A-Za-z0-9._-]+")


def _vendor_path_parts(path: str) -> Optional[Tuple[str, ...]]:
    """The folder names of *path* if it is a safe harness read-path, else ``None``.

    Safe means: relative; at least two names, because the read-path sits inside a
    harness folder and the "is that harness in use?" test looks at that folder;
    the last name is ``skills`` -- a row names a harness's folder of skills, and a
    row that named anything else (the user's ``.venv/bin/python`` link, their
    ``dev/reflections`` link) would have it replaced by a link or, in copy mode,
    filled with the project's files; every name matches `_VENDOR_PART_RE` and is
    not ``.`` or ``..``; and the path does not enter ``.git`` or the
    machine-local state folder.  Copy mode puts every canonical file under the
    row's folder, so a row that named ``.git`` would replace ``.git/config`` and
    one that named ``dev/.cairn`` would write the interpreter binding -- places
    the project's own files must not fill.  Names are compared
    case-insensitively and without trailing dots, because some filesystems treat
    ``.GIT`` and ``.git.`` as ``.git``.
    """
    if not isinstance(path, str) or not path:
        return None
    parts = tuple(path.rstrip("/").split("/"))
    if len(parts) < 2 or parts[-1] != "skills":
        return None
    for part in parts:
        if part in ("", ".", "..") or not _VENDOR_PART_RE.fullmatch(part):
            return None
    shown = tuple(part.rstrip(".").casefold() for part in parts)
    if ".git" in shown or shown[:len(_CAIRN_STATE_DIR)] == _CAIRN_STATE_DIR:
        return None
    return parts


def _assert_fanout_contained(dst: Path, target: Path) -> None:
    """Refuse a fan-out destination reached through a **symlinked parent** or
    resolving **outside** *target*.  ``dst`` itself may be the symlink we
    are about to (re)create, so only its parents are symlink-checked."""
    tr = target.resolve()
    for ancestor in dst.parents:
        if ancestor == tr:
            break
        try:
            ancestor.relative_to(tr)
        except ValueError:
            break
        if ancestor.is_symlink():
            raise LifecycleError(
                "refusing skills fan-out through a symlinked parent: "
                + encode_display(str(ancestor))
            )
    final = dst.parent.resolve() / dst.name
    try:
        final.relative_to(tr)
    except ValueError:
        raise LifecycleError(
            "refusing skills fan-out outside the repo: " + encode_display(str(final))
        )


_GITIGNORE_UNREADABLE = (
    "refusing to change .gitignore: it is not a readable regular UTF-8 text file"
)
_GITIGNORE_READ_ONLY = (
    "refusing to change .gitignore: it is read-only, which is the owner's mark "
    "that no tool should edit it; make it writable, or add this line yourself: "
)


def _seed_skill_gitignore(root: Path, entry: str) -> None:
    """Append *entry* to ``<root>/.gitignore`` if absent (idempotent,
    non-clobber).  Copy-mode fan-out copies are generated, gitignored
    supply-chain artifacts -- the canonical ``.agents/skills/`` is the only
    tracked, editable copy.

    A **directory** ignore is matched ignoring a trailing slash, so an existing
    ``.claude/skills`` and a seeded ``.claude/skills/`` are the same entry -- a
    repo that already ignores the path (either spelling) is left byte-for-byte
    untouched, so session-start never dirties a tree it just reported clean.

    A checkout can make ``.gitignore`` a link to a file that something else runs
    or reads as configuration (a shell startup file, ``.git/config``), and can
    choose the text of *entry*.  So *entry* must be a safe read-path
    (`_vendor_path_parts`), the file must be a plain file and not a link
    (`_assert_not_linked`) and writable, and the new bytes replace it by rename
    (`_write_replacing`), never an open of the old name.  Existing bytes,
    including line endings, are kept as they are.  ``LifecycleError`` on any
    refusal; nothing is written first."""
    if _vendor_path_parts(entry) is None:
        raise LifecycleError(
            "refusing to write an unsafe ignore entry: " + encode_display(entry)
        )
    gitignore = root / ".gitignore"
    _assert_not_linked(gitignore, root)
    existed = True
    try:
        raw = _read_regular_bytes(gitignore)
    except FileNotFoundError:
        raw = b""
        existed = False
    except OSError:
        raise LifecycleError(_GITIGNORE_UNREADABLE) from None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise LifecycleError(_GITIGNORE_UNREADABLE) from None
    norm = entry.rstrip("/")
    if norm in {ln.strip().rstrip("/") for ln in text.splitlines()}:
        return
    if existed and not os.access(gitignore, os.W_OK):
        # a rename needs only a writable folder, so it would replace the file
        # anyway; the owner's read-only mark is respected instead
        # `entry` passed `_vendor_path_parts` above: letters, digits and `._-/` only
        raise LifecycleError(_GITIGNORE_READ_ONLY + entry)
    eol = "\r\n" if "\r\n" in text else "\n"
    gap = "" if (not text or text.endswith(("\n", "\r"))) else eol
    _write_replacing(gitignore, (text + gap + entry + eol).encode("utf-8"))


def _heal_skill_symlink(dst: Path, canonical: Path) -> str:
    """Create / verify a relative symlink ``dst`` -> the canonical skills dir.
    Idempotent (``already-linked``); a wrong symlink is re-pointed
    (``relinked``); a non-symlink existing target is left untouched
    (``exists-nonsymlink``) -- never clobbered."""
    rel = os.path.relpath(canonical, dst.parent)
    if dst.is_symlink():
        if os.readlink(dst) == rel:
            return "already-linked"
        dst.unlink()
        dst.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(rel, dst, target_is_directory=True)
        return "relinked"
    if dst.exists():
        _warn(
            f"{encode_display(str(dst))} exists as a non-symlink; leaving it untouched "
            "(remove it to enable the skills symlink)."
        )
        return "exists-nonsymlink"
    dst.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(rel, dst, target_is_directory=True)
    return "linked"


def _heal_skill_copy(dst: Path, canonical: Path, target: Path) -> str:
    """Regenerate gitignored copies of the canonical skills under *dst* (used
    where symlinks are unavailable).  Idempotent: a copy already byte-equal to
    canonical is left alone; a **divergent** copy is quarantined to
    ``*.diverged.bak`` (preserved, never destroyed) and regenerated, so the
    active vendor-read path always carries the canonical, already-scanned
    bytes.  Returns ``current`` / ``copied`` / ``diverged-quarantined``.

    Every destination -- each copy and each quarantine name -- is checked first
    (`_assert_not_linked`), for the whole set, before the first file is touched,
    so a refusal leaves nothing half-done.  Each file is then written by
    `_write_replacing` and moved with `os.replace`, which neither follows a link
    nor moves a file *into* a folder that happens to hold the quarantine name."""
    plan: List[Tuple[Path, Path, Optional[Path], bytes]] = []
    for src_file in sorted(canonical.rglob("*")):
        if not src_file.is_file():
            continue
        rel = src_file.relative_to(canonical)
        out = dst / rel
        _assert_not_linked(out, target)
        for folder in out.parents:
            # `exists()` is False under a file, so without this a file where a
            # folder must go passes the plan and fails halfway through the writes
            if folder.exists() and not folder.is_dir():
                raise LifecycleError(
                    "refusing to use something that is not a folder as a folder: "
                    + encode_display(folder.relative_to(target).as_posix())
                )
            if folder == dst:
                break
        data = src_file.read_bytes()
        bak: Optional[Path] = None
        if out.exists():
            if not out.is_file():
                raise LifecycleError(
                    "refusing to replace something that is not a plain file: "
                    + encode_display(out.relative_to(target).as_posix())
                )
            if out.read_bytes() == data:
                continue  # already current -- idempotent, no rewrite
            bak = out.with_name(out.name + ".diverged.bak")
            _assert_not_linked(bak, target)
            if bak.exists() and not bak.is_file():
                raise LifecycleError(
                    "refusing to replace something that is not a plain file: "
                    + encode_display(bak.relative_to(target).as_posix())
                )
        plan.append((rel, out, bak, data))

    quarantined: List[str] = []
    copied = 0
    for rel, out, bak, data in plan:
        if bak is not None:
            os.replace(out, bak)
            quarantined.append(rel.as_posix())
        out.parent.mkdir(parents=True, exist_ok=True)
        _write_replacing(out, data)
        copied += 1
    if quarantined:
        _warn(
            f"copy-fallback divergence under {encode_display(str(dst))}: "
            f"{encode_display(', '.join(quarantined))} "
            "differed from the canonical .agents/skills/ source; each was "
            "quarantined to *.diverged.bak and the canonical bytes regenerated. "
            "Edit the canonical source, not the generated copy."
        )
        return "diverged-quarantined"
    return "copied" if copied else "current"


def _heal_skills_fanout(root: Path) -> List[Tuple[str, str, str]]:
    """Ensure every eligible, in-use symlink-tier skills read-path exists.

    Returns ``(target, tier_used, status)`` rows (empty when there is nothing
    to do).  Mirrors the symlink-tier path of ``scaffold.fan_out_skills``: an
    *alias*-tier harness reads ``.agents/skills/`` directly (skipped here); a
    *symlink*-tier harness gets a verified relative symlink (or, where symlinks
    are unavailable, a gitignored generated copy), emitted only when that
    harness's parent dir already exists -- the same light "is this harness in
    use?" gate the installer uses, so a repo is never littered with empty
    vendor dirs.  Every destination is containment-checked before any write."""
    canonical = root.joinpath(*_AGENTS_SKILLS_DIR)
    if not canonical.is_dir():
        return []  # no canonical source to fan out from -- not a skills adopter
    can_symlink = _skill_symlinks_available(root)
    results: List[Tuple[str, str, str]] = []
    for row in _load_vendor_targets(root):
        if row.get("tier") != "symlink":
            continue  # alias tier reads .agents/skills directly; manual is documented
        name = str(row.get("target", "?"))
        path = str(row.get("path", ""))
        if _vendor_path_parts(path) is None:
            _warn(
                "skills self-heal: unsafe vendor path for "
                f"'{encode_display(name)}': '{encode_display(path)}'; skipped (a symlink-tier "
                "row's path needs at least two folders, the last one named skills, none "
                "named .git, none under dev/.cairn, and only letters, digits, dots, dashes "
                "and underscores)."
            )
            continue
        dst = root / path
        if not dst.parent.is_dir():
            continue  # harness not in use here -- light detection, no empty dirs
        _assert_fanout_contained(dst, root)
        if can_symlink:
            results.append((name, "symlink", _heal_skill_symlink(dst, canonical)))
        else:
            # the ignore entry first: a refusal there leaves no copies behind
            _seed_skill_gitignore(root, path.rstrip("/") + "/")
            status = _heal_skill_copy(dst, canonical, root)
            results.append((name, "copy", status))
    return results


def cmd_session_start(args: argparse.Namespace) -> int:
    """Orientation gather (read-only) + idempotent skills fan-out self-heal.

    The gather is purely informational -- commits, tree state, threads,
    intents, resolved interpreter.  The one write the routine performs is the
    **skills fan-out self-heal**: it ensures every eligible, in-use
    symlink-tier read-path (e.g. the ``.claude/skills`` link) points at
    the canonical ``.agents/skills/`` source, idempotently and under the
    installer's writer-safety contract (a no-op when already linked; never
    clobbers a divergent target).  The skill body then performs the judgment
    steps (role confirmation, deciding which thread to pick up).
    """
    root = _repo_root()
    marker = args.handoff_marker
    fallback_n = args.fallback_commits

    # Skills fan-out self-heal FIRST -- the one write the routine performs.
    # Ensure every eligible, in-use symlink-tier read-path (e.g. .claude/skills)
    # points at the canonical .agents/skills/ source.  Idempotent + fail-soft (a
    # containment refusal warns and continues; it never aborts the gather).  It
    # runs *before* the working-tree status below so a copy-mode .gitignore seed
    # is reflected in the reported state -- the routine never dirties a tree it
    # has already reported clean.
    _emit_section("skills fan-out self-heal")
    try:
        healed = _heal_skills_fanout(root)
    except LifecycleError as exc:
        _warn(f"skills self-heal refused: {exc}")
        healed = None
    if healed is None:
        pass  # the refusal above is the whole story; "nothing to fan out" would contradict it
    elif not healed:
        _emit("no symlink-tier harness in use here (nothing to fan out).")
    elif all(st in ("already-linked", "current") for _n, _t, st in healed):
        _emit("symlink-tier skills read-paths already current (no change).")
    else:
        for name, tier, st in healed:
            _emit(f"{_safe_field(name)}: {tier} -> {st}")

    _emit_section(f"commits since last '{marker}' handoff")
    last_handoff = _git(
        ["log", f"--grep=^{marker}", "--format=%H", "-n", "1"], root
    ).strip()
    if last_handoff:
        rng = f"{last_handoff}..HEAD"
        log = _git(["log", rng, "--format=%h %an  %s"], root).strip()
        _emit(f"range {rng}")
    else:
        # A freshly-bootstrapped repo has no handoff commit yet -- fall
        # back to a sensible window rather than crashing on an empty range.
        log = _git(["log", f"-n{fallback_n}", "--format=%h %an  %s"], root).strip()
        _warn(
            f"no '{marker}' commit found in history; showing the last "
            f"{fallback_n} commits instead (likely a freshly-bootstrapped repo)."
        )
    print(log if log else f"{_PREFIX} (no commits in range)")

    _emit_section("working-tree state (git status --short)")
    status = _git(["-c", "core.quotePath=false", "status", "--short"], root).strip()
    print(status if status else f"{_PREFIX} (clean working tree)")

    _emit_section("in-flight threads (open proposals / plans)")
    threads = _in_flight(root)
    if threads:
        for line in threads:
            print(f"{_PREFIX}   {line}")
        advisory = _in_flight_status_advisory(root)
        if advisory:
            print(f"{_PREFIX} {advisory}")
    else:
        print(f"{_PREFIX} (no open proposals or plans)")

    # Resolve the project interpreter (resolve-don't-bake); a tampered
    # Git administration binding refuses here, before any sub-tool runs.
    interpreter, interp_source = _resolve_interpreter(root)

    _surface_intents(root, interpreter)

    # Make the (otherwise hidden) interpreter trust root visible.
    _emit_section("resolved project interpreter")
    _emit(f"interpreter: {encode_display(interpreter)}  (from {interp_source})")
    _emit("session-start gather complete.")
    return 0


def _designation_marker_present(root: Path) -> bool:
    """Whether the maintainer-designation marker is set.

    The marker is an **anti-accidental-run / operating-mode gate, not an
    authorization boundary** -- it is trivially self-set, so it never proves the
    maintainer authorized the run; it only stops a routine full-handoff from
    firing unbidden.  Honored forms: ``CAIRN_HANDOFF_OWNER`` truthy, or a
    maintainer-created ``dev/.cairn/handoff-owner`` state file.
    """
    env = os.environ.get("CAIRN_HANDOFF_OWNER", "").strip()
    if env and env not in ("0", "false", "False", "no"):
        return True
    return (_state_dir(root) / "handoff-owner").exists()


def _pid_alive(pid: int) -> bool:
    """Best-effort host-local liveness check.

    ``os.kill(pid, 0)`` raising ``ProcessLookupError`` is the only affirmative
    proof of death.  ``PermissionError`` (exists, not ours) and any other error
    are treated as *alive* -- the conservative choice, so uncertainty never
    licenses a steal.  This is host-local only: a pid from another host says
    nothing, which is why cross-host locks are never reclaimed automatically.
    """
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except (OSError, OverflowError, ValueError):
        # PermissionError (exists, not ours) or an unrepresentable pid: treat as
        # alive so uncertainty never licenses a steal.
        return True
    return True


class HandoffLock:
    """A fail-closed, single-owner lock for the destructive full-handoff path.

    A local atomic lockfile -- the only
    race-free mutual-exclusion primitive (an intents-log read carries a TOCTOU
    race).  The stale-lock escape is **not age-only**: a held lock is
    reclaimed *only* when the lease has expired **and** the holder is provably
    dead (same host, pid gone).  Cross-host locks, live holders, and fresh
    leases all **fail closed**; a genuinely stuck lock needs manual cleanup.

    Used as a context manager so the lockfile is removed on **both clean exit
    and unexpected exception**.
    """

    def __init__(self, root: Path, agent: str) -> None:
        self.path = _state_dir(root) / "handoff.lock"
        self.agent = agent
        self._root = root
        self._fd: Optional[int] = None

    def _payload(self) -> dict:
        now = time.time()
        return {
            "pid": os.getpid(),
            "host": socket.gethostname(),
            "agent": self.agent,
            "acquired_at": now,
            "heartbeat_at": now,
        }

    def acquire(self) -> "HandoffLock":
        # a linked dev/ or dev/.cairn would put the lock (and the folder) elsewhere
        _assert_not_linked(self.path, self._root)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._fd = os.open(
                self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644
            )
        except FileExistsError:
            self._reclaim_or_refuse()
        os.write(self._fd, json.dumps(self._payload()).encode("utf-8"))
        return self

    def _reclaim_or_refuse(self) -> None:
        try:
            existing = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            existing = {}
        holder_pid = existing.get("pid")
        holder_host = existing.get("host")
        agent = existing.get("agent", "?")
        heartbeat = float(existing.get("heartbeat_at") or 0)

        same_host = holder_host == socket.gethostname()
        lease_expired = (time.time() - heartbeat) > _HANDOFF_LEASE_SECONDS
        provably_dead = (
            same_host and isinstance(holder_pid, int)
            and not _pid_alive(holder_pid)
        )

        if provably_dead and lease_expired:
            # The only sanctioned reclaim: proof of death AND an expired lease.
            _warn(
                f"reclaiming a stale handoff lock (dead pid {holder_pid}, agent "
                f"{encode_display(str(agent))}, lease expired)."
            )
            try:
                self.path.unlink()
            except OSError:
                pass
            self._fd = os.open(
                self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644
            )
            return

        raise LifecycleError(
            f"a full handoff is already in progress (agent "
            f"{encode_display(str(agent))}, pid {encode_display(str(holder_pid))} on "
            f"{encode_display(str(holder_host))}) -- refusing a concurrent handoff to "
            "protect the single-owner roadmap-scrub invariant. If you are "
            f"certain the holder is dead, remove {encode_display(str(self.path))} manually and retry."
        )

    def heartbeat(self) -> None:
        """Refresh the lease so a long-running handoff is not deemed stale.

        Written through the descriptor the lock opened exclusively, not through
        the path, so a link put at the path afterwards cannot redirect it."""
        if self._fd is not None:
            os.lseek(self._fd, 0, os.SEEK_SET)
            os.ftruncate(self._fd, 0)
            os.write(self._fd, json.dumps(self._payload()).encode("utf-8"))

    def release(self) -> None:
        if self._fd is not None:
            try:
                os.close(self._fd)
            finally:
                self._fd = None
            try:
                self.path.unlink()
            except OSError:
                pass

    def __enter__(self) -> "HandoffLock":
        return self.acquire()

    def __exit__(self, *exc_info) -> bool:
        self.release()  # released on clean exit AND exception
        return False


def _reflection_prune_candidates(root: Path, days: int) -> List[Path]:
    """List dated reflections older than `days` without changing any file."""
    refl_dir = _reflections_dir(root)
    # A linked reflections folder could send the preview somewhere unexpected;
    # refuse before listing, just as the destructive path does.
    _assert_not_linked(refl_dir, root)
    if not refl_dir.is_dir():
        return []
    candidates: List[Path] = []
    cutoff = _dt.date.today() - _dt.timedelta(days=days)
    for path in sorted(refl_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        try:
            file_date = _dt.date.fromisoformat(path.name[:10])
        except ValueError:
            continue  # not a dated reflection
        if file_date < cutoff:
            candidates.append(path)
    return candidates


def _prune_reflections(root: Path, days: int, *, dry_run: bool) -> List[Path]:
    """Prune old reflections, or report the same candidates under `dry_run`."""
    candidates = _reflection_prune_candidates(root, days)
    if not dry_run:
        for path in candidates:
            try:
                path.unlink()
            except OSError as exc:
                _warn(f"could not prune {encode_display(path.name)}: "
                      f"{encode_display(str(exc))}")
    return candidates


_METER_REFRESH_TIMEOUT_SECONDS = 300
_METER_REFRESH_STDOUT_LIMIT = 16 * 1024
_METER_REFRESH_STDERR_LIMIT = 4 * 1024


def _stop_meter_child(proc: subprocess.Popen) -> bool:
    """Stop only the process tree started for this Meter refresh, boundedly."""
    if proc.poll() is not None:
        return True
    try:
        if os.name == "posix":
            os.killpg(proc.pid, signal.SIGTERM)
        else:
            proc.terminate()
    except (OSError, ProcessLookupError):
        pass
    try:
        proc.wait(timeout=1.0)
        return True
    except subprocess.TimeoutExpired:
        try:
            if os.name == "posix":
                os.killpg(proc.pid, signal.SIGKILL)
            else:
                proc.kill()
        except (OSError, ProcessLookupError):
            pass
        try:
            proc.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            return False
        return proc.poll() is not None


def _meter_refresh_receipt(stdout: bytes, returncode: int) -> bool:
    """Validate the closed Meter receipt without relaying child output."""
    if (returncode != 0 or not isinstance(stdout, bytes)
            or not stdout.endswith(b"\n") or b"\r" in stdout
            or stdout.count(b"\n") != 1):
        return False

    def unique_pairs(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError
            value[key] = item
        return value

    def reject_constant(_text):
        raise ValueError

    try:
        value = json.loads(stdout[:-1].decode("ascii"), object_pairs_hook=unique_pairs,
                           parse_constant=reject_constant)
    except (UnicodeError, ValueError, TypeError):
        return False
    if not isinstance(value, dict) or set(value) != {"schema", "status", "reason", "coverage"}:
        return False
    if value["schema"] != "cairn-meter-refresh/1" or value["coverage"] != "unknown":
        return False
    return ((value["status"] == "ok" and value["reason"] == "none")
            or (value["status"] == "disabled"
                and value["reason"] in {"disabled", "config_missing"}))


def _meter_refresh_before_prune(root: Path, interpreter: str) -> bool:
    """Run the fixed sibling Meter helper and require its exact closed receipt."""
    meter_tool = root / "tools" / "meter.py"
    try:
        if (_path_has_link_or_reparse(meter_tool)
                or not stat.S_ISREG(os.lstat(meter_tool).st_mode)):
            return False
    except (OSError, LifecycleError):
        return False
    argv = [interpreter, str(meter_tool), "refresh", "--json"]
    options = {
        "cwd": str(root), "stdin": subprocess.DEVNULL,
        "stdout": subprocess.PIPE, "stderr": subprocess.PIPE,
        "env": _git_env(), "close_fds": True,
    }
    if os.name == "posix":
        options["start_new_session"] = True
    else:
        options["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    try:
        proc = subprocess.Popen(argv, **options)
    except (OSError, ValueError, TypeError):
        return False

    captured = {}
    failures = []

    def drain(name, pipe, limit):
        data = bytearray()
        try:
            while True:
                block = pipe.read(4096)
                if not block:
                    break
                room = limit + 1 - len(data)
                if room > 0:
                    data.extend(block[:room])
            captured[name] = bytes(data)
        except (OSError, ValueError):
            failures.append(name)
            captured[name] = b""

    readers = [
        threading.Thread(target=drain, args=("stdout", proc.stdout,
                                             _METER_REFRESH_STDOUT_LIMIT), daemon=True),
        threading.Thread(target=drain, args=("stderr", proc.stderr,
                                             _METER_REFRESH_STDERR_LIMIT), daemon=True),
    ]
    try:
        for reader in readers:
            reader.start()
        timed_out = False
        try:
            proc.wait(timeout=_METER_REFRESH_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            timed_out = True
            if not _stop_meter_child(proc):
                return False
        for reader in readers:
            reader.join(timeout=1.0)
        if any(reader.is_alive() for reader in readers):
            if os.name == "posix":
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except (OSError, ProcessLookupError):
                    pass
                for reader in readers:
                    reader.join(timeout=1.0)
            if any(reader.is_alive() for reader in readers):
                return False
        if timed_out or failures or proc.returncode != 0:
            return False
        stdout = captured.get("stdout", b"")
        stderr = captured.get("stderr", b"")
        if (len(stdout) > _METER_REFRESH_STDOUT_LIMIT
                or len(stderr) > _METER_REFRESH_STDERR_LIMIT):
            return False
        return _meter_refresh_receipt(stdout, proc.returncode)
    except (OSError, ValueError, TypeError, RuntimeError):
        _stop_meter_child(proc)
        return False
    finally:
        for stream in (proc.stdout, proc.stderr):
            if stream is not None:
                try:
                    stream.close()
                except OSError:
                    pass


def _prune_intents(root: Path, interpreter: str, days: int, *,
                   dry_run: bool) -> None:
    """Prune released claim/release pairs from the intent log, if installed.

    Full-handoff only.  The intent log is a coordination surface, not an
    archive, and the tool that owns it does the pruning -- invoked as a
    subprocess exactly like :func:`_surface_intents`, so this module never
    imports the intent engine.  The command refuses on its own if any claim is
    still active, and it never deletes an unreleased claim or an unparseable
    line; both are reported.
    """
    _emit_section("pruning the work-intent surface")
    dotgit = root / ".git"
    try:
        main_checkout = (
            not _path_has_link_or_reparse(dotgit)
            and stat.S_ISDIR(os.lstat(dotgit).st_mode)
        )
    except OSError:
        main_checkout = False
    if not main_checkout:
        _emit("skipping intent prune: this is not a verified main checkout")
        return
    # Resolve against *root*, not via
    # _sibling_tool -- which returns the copy beside THIS file regardless of the
    # target root.  That distinction is invisible in an adopter tree (the CLI is
    # installed in the tree it operates on) but it matters here: the intent
    # engine computes its ledger path from its OWN location, so a root-blind
    # lookup would rewrite the installing tree's ledger while reporting on the
    # target.  It also made this wiring untestable, which is why review could
    # replace the call with `pass` and see every suite stay green.
    intent_tool = root / "tools" / "intent.py"
    if not intent_tool.is_file():
        intent_tool = _sibling_tool("intent.py")
    if intent_tool is None or not intent_tool.is_file():
        _warn("intent.py (coordination-tiers) not installed -- skipping.")
        return
    argv = [interpreter, str(intent_tool), "prune", "--older-than-days",
            str(days)]
    if dry_run:
        argv.append("--dry-run")
    try:
        proc = subprocess.run(
            argv, cwd=str(root), capture_output=True, check=False,
            env=_git_env(),
        )
        stdout = _decode_child_output(proc.stdout)
        stderr = _decode_child_output(proc.stderr)
        sys.stdout.write(_encode_child_output(stdout, terminate=True))
        if proc.returncode != 0 and stderr:
            _warn(_encode_child_output(stderr.strip()))
    except OSError as exc:  # pragma: no cover -- defensive
        _warn(f"intent prune failed to run: {encode_display(str(exc))}")


def _surface_intents(root: Path, interpreter: str) -> None:
    """Read-only surface of active work-intents, if intent.py is installed.

    Used by both `session-start` (who holds which paths before the first edit)
    and the full handoff (a coordination-safety check: whether another session
    still has claimed work).  Skip-with-note when the optional coordination
    tool is absent -- the default-on skill never hard-requires it.  Invoked as
    an explicit argv list under the resolved interpreter, never a shell string
    (the interpreter-binding contract).
    """
    _emit_section("active work-intents")
    intent_tool = _sibling_tool("intent.py")
    if intent_tool is None:
        _warn(
            "intent.py (coordination-tiers) not installed -- skipping the "
            "active-intent read; if your team uses work-intents, install it."
        )
        return
    try:
        proc = subprocess.run(
            [interpreter, str(intent_tool), "list"],
            cwd=str(root),
            capture_output=True,
            check=False,
            env=_git_env(),
        )
        stdout = _decode_child_output(proc.stdout)
        stderr = _decode_child_output(proc.stderr)
        sys.stdout.write(_encode_child_output(stdout, terminate=True))
        if proc.returncode != 0 and stderr:
            _warn(f"intent list reported: {_encode_child_output(stderr.strip())}")
    except OSError as exc:
        _warn(f"could not run intent.py list: {encode_display(str(exc))}")




def _run_evolution_infer(root: Path, interpreter: str) -> None:
    """Run the deterministic rate-limit-gate / fold-up-backlog checker
    (``evolution_infer.py``) read-only, if installed.

    Zero-token, deterministic decision-support (self-evolution-loop Part B):
    surfaces rate-limit suggestions + a fold-up-backlog alarm. Skip-with-note
    when absent; never fails the handoff. The checker emits suggestions only --
    it mutates nothing. A non-zero exit (a fail-closed tracker) is surfaced as a
    note, not a failure."""
    tool = _sibling_tool("evolution_infer.py")
    if tool is None:
        _warn(
            "evolution_infer.py not installed -- skipping the rate-limit-gate "
            "/ backlog check."
        )
        return
    try:
        proc = subprocess.run(
            [interpreter, str(tool)],
            cwd=str(root),
            capture_output=True,
            check=False,
            env=_git_env(),
        )
        stdout = _decode_child_output(proc.stdout)
        stderr = _decode_child_output(proc.stderr)
        if stdout:
            sys.stdout.write(_encode_child_output(stdout, terminate=True))
        if proc.returncode != 0 and stderr:
            _warn(f"evolution_infer reported: {_encode_child_output(stderr.strip())}")
    except OSError as exc:
        _warn(f"could not run evolution_infer.py: {encode_display(str(exc))}")




_REFLECTION_SKELETON = """\
# Session reflection -- {agent} -- {date} (session {session})

<!-- Per-agent, ephemeral, pruned. Migrate durable observations into the
     project's governing files or roadmap before pruning. See AGENTS.md for
     the local session-start and goodnight duties. -->

## What shipped

## What went well

## What went wrong -- and the lesson

## Open threads / handoffs
"""


def _reflections_dir(root: Path) -> Path:
    return root / "dev" / "reflections"


def _do_reflection(root: Path, dry_run: bool) -> None:
    """Scaffold the per-session reflection file (non-destructive; both modes)."""
    refl_dir = _reflections_dir(root)
    agent = _resolve_agent(root)
    session = _resolve_session(root)
    # <date>-<agent>-<session>.md (#46/#50): the <session> segment keeps
    # concurrent same-agent sessions from clobbering one reflection; the
    # goodnight reader globs <date>-*.md to gather every session.
    target = refl_dir / f"{_today()}-{agent}-{session}.md"
    _assert_not_linked(target, root)  # no link on the way, none at the file
    _assert_within(target, refl_dir)  # never write outside dev/reflections/

    _emit_section("reflection scaffold")
    if target.exists():
        _emit(
            f"reflection already exists: {target.relative_to(root)} "
            "-- leaving it untouched; edit it directly."
        )
    elif dry_run:
        _emit(f"[dry-run] would create reflection scaffold: "
              f"{target.relative_to(root)}")
    else:
        if not refl_dir.is_dir():
            # The reflections dir is normally seeded at scaffold time; create it
            # defensively rather than failing the goodnight on a missing dir.
            refl_dir.mkdir(parents=True, exist_ok=True)
            _warn(f"created missing reflections directory: "
                  f"{refl_dir.relative_to(root)}")
        try:
            _create_text_exclusive(
                target,
                _REFLECTION_SKELETON.format(
                    agent=agent, date=_today(), session=session),
            )
        except FileExistsError:
            _emit(
                f"reflection already exists: {target.relative_to(root)} "
                "-- leaving it untouched; edit it directly."
            )
            return
        _emit(f"wrote reflection scaffold: {target.relative_to(root)} "
              "-- fill in what you shipped and learned.")


def _do_thread_survey(root: Path) -> None:
    _emit_section("open threads to note in your reflection")
    threads = _in_flight(root)
    if threads:
        for line in threads:
            print(f"{_PREFIX}   {line}")
    else:
        print(f"{_PREFIX} (no open proposals or plans)")


def _do_handoff_preparation(root: Path, args: argparse.Namespace) -> int:
    """Gather handoff evidence and prompts without invoking either pruner."""
    interpreter, _ = _resolve_interpreter(root)

    _emit_section("full-handoff preparation manifest")
    would_prune = _reflection_prune_candidates(
        root, args.reflection_grace_days
    )
    names = encode_display(", ".join(p.name for p in would_prune)) or "(none)"
    _emit(f"would prune {len(would_prune)} reflection(s) older than "
          f"{args.reflection_grace_days}d: {names}")
    _surface_intents(root, interpreter)
    _emit(f"would prune released work-intent pairs older than "
          f"{args.intent_grace_days}d (never an unreleased claim) if installed")
    _emit("would run the rate-limit gate (read-only) if installed")

    _emit(
        "scan today's doctrine activity for portable improvements worth "
        "filing upstream? (capture stays judgment -- an empty capture is "
        "success; never manufacture marginal candidates)"
    )
    _emit_section("rate-limit gate + fold-up backlog")
    _run_evolution_infer(root, interpreter)

    _emit(
        "handoff preparation complete. This intent listing is a snapshot; it "
        "cannot prove that no session is appending or that the log will stay "
        "quiet. Complete the reflection, roadmap scrub, next-session note, "
        "custom steps, and handoff commit; then check recent claims and confirm "
        "no session is appending before the user runs the guarded prune."
    )
    return 0


def cmd_session_end(args: argparse.Namespace) -> int:
    """Goodnight.  Reflection-only by default; full handoff under `--handoff`.

    Reflection-only (the safe default, the portable Layer-2 guarantee): scaffold
    the reflection + survey open threads -- both non-destructive, so even if a
    harness ignores `disable-model-invocation` and auto-fires this,
    the worst case is a stray reflection file, never a roadmap scrub.

    Handoff preparation (`--prepare-handoff`): the evidence, previews and
    prompts are gathered without pruning. Full handoff (`--handoff`): the
    mechanizable steps (prune reflections and released intents, surface active
    intents, run metrics) run **only** behind (1) a mutation manifest, (2) the
    maintainer-designation marker, and (3) the fail-closed concurrent-handoff
    lock. The roadmap scrub, next-session note, custom steps and handoff commit
    are the owner's judgment steps before the user runs the prune.
    """
    root = _repo_root()

    # Reflection-only work runs in BOTH modes -- every agent reflects.
    _do_reflection(root, args.dry_run)
    _do_thread_survey(root)

    if args.prepare_handoff:
        return _do_handoff_preparation(root, args)

    if not args.handoff:
        _emit(
            "reflection-only goodnight complete. The designated owner can use "
            "--prepare-handoff to gather full-handoff evidence and prompts; "
            "only the guarded --handoff path prunes."
        )
        return 0

    return _do_full_handoff(root, args)


def _do_full_handoff(root: Path, args: argparse.Namespace) -> int:
    """The guarded destructive path: manifest -> marker -> lock -> steps."""
    grace = args.reflection_grace_days

    # Always emit the mutation manifest before any real run.
    _emit_section("full-handoff mutation manifest")
    would_prune = _prune_reflections(root, grace, dry_run=True)
    names = encode_display(", ".join(p.name for p in would_prune)) or "(none)"
    _emit(f"would prune {len(would_prune)} reflection(s) older than {grace}d: "
          f"{names}")
    _emit("would surface active intents (read-only) if installed")
    _emit(f"would prune released work-intent pairs older than "
          f"{args.intent_grace_days}d (never an unreleased claim) if installed")
    _emit("would run the rate-limit gate (read-only) if installed")

    if args.dry_run:
        _emit("[dry-run] manifest only -- nothing mutated, no marker required.")
        return 0

    # The marker is an anti-accidental-run gate (not an authorization
    # control).  Refuse non-interactively -- never block on input.
    if not _designation_marker_present(root):
        raise LifecycleError(
            "refusing the full handoff: no maintainer-designation marker. Set "
            "CAIRN_HANDOFF_OWNER=1 (or create dev/.cairn/handoff-owner) to run "
            "as the designated single owner. This is an anti-accidental-run "
            "gate, not an authorization control -- run with --dry-run to "
            "preview the manifest first."
        )

    interpreter, _ = _resolve_interpreter(root)

    # Fail-closed concurrent-handoff lock; released on clean exit AND
    # exception (the context manager's __exit__).
    with HandoffLock(root, _resolve_agent(root)) as lock:
        # Surface active claims before Meter refresh and both destructive steps.
        # The Meter persists claim attribution before intent pruning can remove it.
        _surface_intents(root, interpreter)
        lock.heartbeat()

        _emit_section("refreshing Meter before pruning")
        if not _meter_refresh_before_prune(root, interpreter):
            _warn("Meter refresh was unavailable; both prune steps were skipped.")
            return 5
        lock.heartbeat()

        _emit_section("pruning reflections")
        pruned = _prune_reflections(root, grace, dry_run=False)
        _emit(f"pruned {len(pruned)} reflection(s) older than {grace}d.")
        lock.heartbeat()

        # Destructive, and deliberately AFTER the read-only surface above so the
        # operator sees the live state before anything is removed.  Runs under
        # the handoff lock: the prune rewrites a file whose concurrent-append
        # atomicity is best-effort, so a live appender could otherwise lose a
        # claim (and a lost claim is a lost lock).
        _prune_intents(root, interpreter, args.intent_grace_days, dry_run=False)
        lock.heartbeat()

        # Fold-back surfacing -- gated behind --handoff: fires
        # only in the full-handoff path, never in the reflection-only goodnight.
        lock.heartbeat()

        # Standing capture prompt.  The practice survives the ledger that
        # used to hold its output: a candidate is filed as an issue upstream
        # rather than staged locally, so there is nothing here to drain later.
        _emit(
            "scan today's doctrine activity for portable improvements worth "
            "filing upstream? (capture stays judgment -- an empty capture is "
            "success; never manufacture marginal candidates)"
        )

        # Rate-limit-gate check -- deterministic, zero-token,
        # read-only decision-support (it emits suggestions only, mutates nothing).
        _emit_section("rate-limit gate + fold-up backlog")
        _run_evolution_infer(root, interpreter)

    _emit(
        "guarded pruning complete. This command does not fill in the "
        "reflection or perform the roadmap scrub, next-session note, custom "
        "steps, or handoff commit."
    )
    return 0

# --- argument parsing --------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="session",
        description=(
            "Deterministic backend for Cairn's session-start / session-end "
            "skills.  Orientation gather (plus one idempotent skills-fan-out "
            "self-heal write) and reflection-only goodnight; no network."
        ),
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_start = sub.add_parser(
        "session-start",
        help="Orientation gather (commits, tree state, threads, intents) "
             "plus one idempotent skills-fan-out self-heal write.",
    )
    p_start.add_argument(
        "--handoff-marker",
        default="Handoff",
        help="Commit-subject prefix marking the last handoff. "
             "Default: 'Handoff'.",
    )
    p_start.add_argument(
        "--fallback-commits",
        type=int,
        default=15,
        help="How many recent commits to show when no handoff marker exists "
             "in history (EP4 graceful fallback). Default: 15.",
    )
    p_start.set_defaults(func=cmd_session_start)

    p_end = sub.add_parser(
        "session-end",
        help="Goodnight.  Reflection-only by default; the full handoff is "
             "prepared non-destructively with --prepare-handoff; pruning "
             "requires --handoff + designation marker + concurrent-handoff "
             "lock.",
    )
    handoff_mode = p_end.add_mutually_exclusive_group()
    handoff_mode.add_argument(
        "--prepare-handoff",
        action="store_true",
        help="Scaffold and survey, surface intents, and emit prompts and a "
             "prune preview without pruning. A snapshot does not establish "
             "future quiet.",
    )
    handoff_mode.add_argument(
        "--handoff",
        action="store_true",
        help="Run the guarded user-prune path after the designated owner "
             "finishes judgment steps: emits a mutation manifest, then -- "
             "with the designation marker and concurrent-handoff lock -- "
             "refreshes Meter before pruning eligible records. Missing or "
             "unavailable Meter skips both prune steps. Refuses non-interactively "
             "without the marker.",
    )
    p_end.add_argument(
        "--reflection-grace-days",
        type=int,
        default=_REFLECTION_GRACE_DAYS,
        help=f"Full-handoff prune horizon for reflections. "
             f"Default: {_REFLECTION_GRACE_DAYS}.",
    )
    p_end.add_argument(
        "--intent-grace-days",
        type=int,
        default=_INTENT_GRACE_DAYS,
        help=f"Full-handoff prune horizon for RELEASED work-intent pairs. Never "
             f"applies to an unreleased claim. Default: {_INTENT_GRACE_DAYS}.",
    )
    p_end.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned writes or a handoff manifest and exit without "
             "writing or pruning.",
    )
    p_end.set_defaults(func=cmd_session_end)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except LifecycleError as exc:
        print(f"{_PREFIX} ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
