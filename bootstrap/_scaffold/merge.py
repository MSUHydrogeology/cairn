"""Scaffold engine -- token- + slot-aware 3-way merge engine (scaffold-split Stage 3).

The upgrade-time text merge: strict (fail-closed) ``cairn:slot`` parsing, the
slot-transplant that holds adopter-owned bodies identical across the three inputs,
and the ``git merge-file`` 3-way merge that merges surrounding prose while leaving
slots and unfilled new-upstream tokens fail-closed. Depends only on the
``slotmerge`` leaf (token substitution + the slot regexes) and the stdlib --
install / upgrade depend on it, never the reverse.

The verbatim-script hash policy (``classify_verbatim``) is *not* here: it is a
hash check, never a text merge, and couples to ``_sha256_hex`` (the lockfile/hash
cluster migrating at Stage 5); it stays in the engine for now.

Pure motion from the pre-split monolith (Stage 3): the symbols are unchanged; only
their home moved. Loaded via the engine's verifying finder, so this file's real
path is confirmed within the Cairn root before it executes.
"""
from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

from .slotmerge import (
    _SLOT_END_RE,
    _SLOT_RE,
    find_unfilled_tokens,
    substitute_tokens,
)


# ---------------------------------------------------------------------------
# Fail-closed slot parsing -- the merge engine relies on slots being
# well-formed before it transplants adopter-owned bodies.  Stricter than the
# set-level ``find_unpaired_slots`` (which only computes open ^ close and is
# blind to ordering / nesting / duplicates).
# ---------------------------------------------------------------------------

class SlotError(ValueError):
    """Raised on a malformed ``cairn:slot`` structure (fail-closed)."""


class Slot(NamedTuple):
    """A parsed, marker-anchored slot region (line indices, 0-based)."""

    name: str
    open_line: int   # index of the `cairn:slot NAME` marker line
    close_line: int  # index of the `cairn:end NAME` marker line
    body: str        # text strictly between the markers (exclusive)


def parse_slots(text: str) -> list[Slot]:
    """Strictly parse ``cairn:slot`` / ``cairn:end`` regions; **fail closed**.

    Raises :class:`SlotError` on any malformation a merge must not silently
    mis-handle: a **nested** opener (a second slot opened before the
    current one closes), a **duplicate** slot name in one file, a
    ``cairn:end`` **before any** opener (end-before-start), a **mismatched**
    closer name, or an **unclosed** opener.  On success returns the slots in
    document order with their bodies (the lines strictly between markers).
    """
    lines = text.splitlines()
    slots: list[Slot] = []
    open_name: str | None = None
    open_idx: int | None = None
    seen: set[str] = set()
    for i, line in enumerate(lines):
        m_open = _SLOT_RE.search(line)
        m_close = _SLOT_END_RE.search(line)
        if m_open:
            name = m_open.group(1)
            if open_name is not None:
                raise SlotError(
                    f"nested slot: '{name}' opened inside still-open "
                    f"'{open_name}' (line {i + 1})"
                )
            if name in seen:
                raise SlotError(
                    f"duplicate slot name '{name}' in one file (line {i + 1})"
                )
            open_name, open_idx = name, i
        elif m_close:
            cname = m_close.group(1)
            if open_name is None:
                raise SlotError(
                    f"cairn:end '{cname}' before any cairn:slot (line {i + 1})"
                )
            if cname != open_name:
                raise SlotError(
                    f"mismatched closer: cairn:end '{cname}' closes "
                    f"cairn:slot '{open_name}' (line {i + 1})"
                )
            assert open_idx is not None
            body = "\n".join(lines[open_idx + 1:i])
            slots.append(Slot(open_name, open_idx, i, body))
            seen.add(open_name)
            open_name, open_idx = None, None
    if open_name is not None:
        raise SlotError(
            f"unclosed slot '{open_name}' (opened line {(open_idx or 0) + 1})"
        )
    return slots


# ---------------------------------------------------------------------------
# The token- + slot-aware 3-way merge engine
# ---------------------------------------------------------------------------

class MergeResult(NamedTuple):
    """Outcome of merging one substituted ``.md`` file."""

    status: str          # "clean" | "conflict" | "slot-removed" | "error"
    merged: str          # merged text (with conflict markers if conflicted)
    detail: str          # human-readable note (needs-value tokens, etc.)


def _transplant_slots(target_text: str, ours_text: str) -> str:
    """Return *target_text* with each slot also present in *ours_text*
    replaced by **ours' exact slot lines** (slot-transplant).  Slots in
    the target but absent from ours (e.g. a slot newly added upstream) are
    left untouched.

    Copies the raw line ranges (``splitlines(keepends=True)``) rather than
    round-tripping through a joined string, so a slot whose body is a
    single empty line -- or zero lines -- transplants its exact line count
    and does not desync the three inputs."""
    try:
        tslots = parse_slots(target_text)
        our_slots = {s.name: s for s in parse_slots(ours_text)}
    except SlotError:
        return target_text  # caller validates ours separately
    ours_lines = ours_text.splitlines(keepends=True)
    lines = target_text.splitlines(keepends=True)
    for sl in sorted(tslots, key=lambda s: s.open_line, reverse=True):
        osl = our_slots.get(sl.name)
        if osl is None:
            continue
        lines[sl.open_line + 1:sl.close_line] = \
            ours_lines[osl.open_line + 1:osl.close_line]
    return "".join(lines)


def _three_way_merge(
    ours: str, base: str, theirs: str,
) -> tuple[str, bool]:
    """Run ``git merge-file`` (current=ours, base, other=theirs); return
    ``(merged_text, had_conflict)``.  Conflict markers are labelled
    ours/base/theirs.  Isolated behind this one function so a stdlib
    ``difflib`` fallback can replace it for no-git adoptions (a named
    follow-up).  Raises RuntimeError if git is unavailable / errors."""
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        (tdp / "ours").write_text(ours, encoding="utf-8")
        (tdp / "base").write_text(base, encoding="utf-8")
        (tdp / "theirs").write_text(theirs, encoding="utf-8")
        try:
            r = subprocess.run(
                ["git", "merge-file", "-p",
                 "-L", "ours", "-L", "base", "-L", "theirs",
                 str(tdp / "ours"), str(tdp / "base"), str(tdp / "theirs")],
                capture_output=True, text=True, timeout=30, check=False,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise RuntimeError(f"git merge-file unavailable: {exc}") from exc
    if r.returncode == 255 or r.returncode < 0:
        raise RuntimeError(
            f"git merge-file errored (rc={r.returncode}): {r.stderr.strip()}"
        )
    return r.stdout, r.returncode > 0


def merge_file(
    base_raw: str, theirs_raw: str, ours: str, tokens: dict[str, str],
) -> MergeResult:
    """Token- + slot-aware 3-way merge of one substituted ``.md`` file.

    * ``base`` = the recorded tokens substituted into the cached **raw**
      base template (so it equals what was written at install).
    * ``theirs`` = the same tokens substituted into the **new** upstream
      template; any upstream token with no recorded value stays as a raw
      ``{{token}}`` and is reported as *needs-value*.
    * **Slot-transplant**: ``ours``' slot bodies are copied into the
      same-named slots of ``base`` and ``theirs`` so all three inputs are
      identical inside slots -> ``git merge-file`` produces zero
      changes/conflicts there while the surrounding prose merges.
    * A slot **removed** upstream whose ``ours`` body is non-empty is a
      **fail-closed** flagged decision (status ``slot-removed``) -- the
      adopter's filled content would otherwise be orphaned.

    ``ours`` is parsed strictly; a malformed ``ours`` raises
    :class:`SlotError` to the caller (never silently mis-merged).
    """
    base = substitute_tokens(base_raw, tokens)
    theirs = substitute_tokens(theirs_raw, tokens)

    # New upstream tokens with no recorded value remain as {{token}}.
    needs_value = sorted(set(find_unfilled_tokens(theirs)))

    our_slots = parse_slots(ours)              # strict; may raise
    our_bodies = {s.name: s.body for s in our_slots}
    their_names = {s.name for s in parse_slots(theirs)}

    # Fail-closed: a slot removed upstream whose adopter body is non-empty.
    orphaned = sorted(
        name for name, body in our_bodies.items()
        if name not in their_names and body.strip()
    )
    if orphaned:
        return MergeResult(
            "slot-removed", ours,
            "upstream removed slot(s) with non-empty adopter content: "
            + ", ".join(orphaned)
            + " -- resolve by hand (the filled content would be orphaned).",
        )

    base_t = _transplant_slots(base, ours)
    theirs_t = _transplant_slots(theirs, ours)
    try:
        merged, had_conflict = _three_way_merge(ours, base_t, theirs_t)
    except RuntimeError as exc:
        return MergeResult("error", ours, str(exc))
    if had_conflict:
        return MergeResult("conflict", merged, "")
    # A clean merge that still carries an unfilled NEW upstream token is
    # NOT safe to apply (it would write a raw {{token}} into a tracked
    # doctrine file); surface it as a non-advancing "needs-value" status so
    # the upgrade neither stages nor applies it.
    if needs_value:
        return MergeResult(
            "needs-value", merged,
            "new upstream token(s) need a value before this file can "
            "advance: " + ", ".join(needs_value),
        )
    return MergeResult("clean", merged, "")
