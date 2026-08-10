"""Scaffold engine -- token / slot / module-merge templating leaf (scaffold-split Stage 2).

The pure templating mechanics: ``{{token}}`` substitution, ``cairn:slot`` block
parsing, and the module-into-slot merge helpers (Proposal B: scaffold-merge UX).
A near-leaf -- it imports only the stdlib plus the ``security`` containment leaf
(``_assert_safe_write``, used by ``merge_module_into_slot`` to refuse a write that
escapes the adopter root -- final Security Review P1 #1); a downward edge, no
cycle. install / upgrade / the 3-way merge engine depend on it, never the reverse.
The templating symbols are pure motion from the pre-split monolith (Stage 2);
``merge_module_into_slot`` gained its containment guards as an explicit post-motion
security hardening (its AST baseline entry was deliberately re-pinned for that one
change; the other 163 symbols remain unchanged).

The install-time orchestrator ``run_module_merge_pass`` is *not* here -- it stays
in the engine because it walks ``_MODULE_MAPPINGS`` / ``InstallSpec`` (config
trust-anchors migrating at Stage 4); it joins ``install.py`` at Stage 6. This
leaf provides the helpers it calls (``parse_module_merge_directives``,
``merge_module_into_slot``, ``check_slot_fidelity``).

Loaded via the engine's verifying finder, so this file's real path is confirmed
within the Cairn root before it executes.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .security import _assert_safe_write  # containment guard for module-merge writes (P1 #1)


# ---------------------------------------------------------------------------
# Token and slot patterns
# ---------------------------------------------------------------------------

#: Matches ``{{token_name}}`` tokens.
_TOKEN_RE = re.compile(r"\{\{(\w+)\}\}")

#: Matches the opening tag of a cairn block slot.
_SLOT_RE = re.compile(r"<!--\s*cairn:slot\s+(\S+)\s*-->", re.IGNORECASE)

#: Matches the closing tag of a cairn block slot.
_SLOT_END_RE = re.compile(r"<!--\s*cairn:end\s+(\S+)\s*-->", re.IGNORECASE)

# ---------------------------------------------------------------------------
# Module-merge helper (Proposal B: scaffold-merge UX -- audit gap #3)
# ---------------------------------------------------------------------------
#
# A module file may declare one or more **structured merge directives**:
#
#     <!-- cairn:merge-target: dst-rel-path > slot-name -->
#     <!-- cairn:merge-content-start -->
#     ... verbatim text to insert at the named slot ...
#     <!-- cairn:merge-content-end -->
#
# After modules install, ``merge_module_into_slot`` parses these
# directives and performs the merge against the named target template.
# Four behaviors per (target, slot, content) tuple:
#
# * Target slot empty -> insert + report ``inserted``.
# * Target slot non-empty AND matches verbatim -> ``already-current``.
# * Target slot carries ``<!-- cairn:customized -->`` marker
#   (Antigravity P2) -> ``customized`` (skip fidelity check).
# * Target slot non-empty AND differs -> conflict mode:
#   * Interactive (stdin is TTY): prompt a/b/c.
#   * Non-interactive: default to (c) defer -- write the merge to
#     ``<target>.cairn-merge-pending`` for human resolution.

#: Single-line directive naming the merge target.  Format:
#:     <!-- cairn:merge-target: <dst> > <slot-name> -->
_MERGE_TARGET_RE = re.compile(
    r"<!--\s*cairn:merge-target:\s*([^>]+?)\s*>\s*(\S+)\s*-->",
    re.IGNORECASE,
)

#: Block delimiters for the verbatim merge content.
_MERGE_CONTENT_START_RE = re.compile(
    r"<!--\s*cairn:merge-content-start\s*-->", re.IGNORECASE,
)
_MERGE_CONTENT_END_RE = re.compile(
    r"<!--\s*cairn:merge-content-end\s*-->", re.IGNORECASE,
)

#: Adopter marker (Antigravity P2): a slot carrying this comment is
#: intentionally customized; the fidelity check skips substring-match
#: and the merge helper preserves the existing content.
_CUSTOMIZED_MARKER_RE = re.compile(
    r"<!--\s*cairn:customized\s*-->", re.IGNORECASE,
)


class ModuleMergeError(Exception):
    """Raised on module-merge parse-time error (Antigravity P3:
    duplicate slot names within a template; module declares an
    unparseable directive)."""


class DuplicateSlotError(ModuleMergeError):
    """Parse-phase uniqueness validation failure: a target template
    carries two `<!-- cairn:slot NAME -->` anchors with the same NAME.
    Surfaced cleanly before any merge is attempted."""


def parse_module_merge_directives(
    module_text: str,
) -> list[tuple[str, str, str]]:
    """Parse a module file for ``cairn:merge-target`` directives +
    paired ``cairn:merge-content-start`` / ``cairn:merge-content-end``
    blocks.

    Returns a list of ``(target_path, slot_name, content)`` tuples.
    A module without any merge directives returns an empty list
    (the helper no-ops for that module).
    """
    out: list[tuple[str, str, str]] = []
    lines = module_text.splitlines(keepends=True)
    i = 0
    pending_target: tuple[str, str] | None = None
    while i < len(lines):
        line = lines[i]
        m_target = _MERGE_TARGET_RE.search(line)
        if m_target is not None:
            pending_target = (m_target.group(1), m_target.group(2))
            i += 1
            continue
        if (
            pending_target is not None
            and _MERGE_CONTENT_START_RE.search(line) is not None
        ):
            # Scan forward to the matching end marker.
            j = i + 1
            content_lines: list[str] = []
            while j < len(lines):
                if _MERGE_CONTENT_END_RE.search(lines[j]) is not None:
                    break
                content_lines.append(lines[j])
                j += 1
            else:
                raise ModuleMergeError(
                    f"unclosed cairn:merge-content block (target="
                    f"{pending_target[0]!r}, slot="
                    f"{pending_target[1]!r})"
                )
            content = "".join(content_lines).strip("\n")
            out.append((pending_target[0], pending_target[1], content))
            pending_target = None
            i = j + 1
            continue
        i += 1
    return out


def validate_unique_slot_names(template_text: str, src_label: str) -> None:
    """Antigravity P3: a `<!-- cairn:slot NAME -->` opener appearing
    twice in the same template is a structural error.  Raise
    ``DuplicateSlotError`` naming the template, slot name, and both
    line numbers BEFORE any merge is attempted.
    """
    seen: dict[str, int] = {}
    duplicates: list[tuple[str, int, int]] = []
    for ln_no, line in enumerate(template_text.splitlines(), start=1):
        m = _SLOT_RE.search(line)
        if m is None:
            continue
        name = m.group(1)
        if name in seen:
            duplicates.append((name, seen[name], ln_no))
        else:
            seen[name] = ln_no
    if duplicates:
        details = "; ".join(
            f"slot {name!r} at lines {first} and {second}"
            for name, first, second in duplicates
        )
        raise DuplicateSlotError(
            f"{src_label}: duplicate slot anchors detected -- {details}"
        )


def _slot_body_in_text(
    text: str, slot_name: str,
) -> tuple[int, int, str] | None:
    """Locate the body of the named slot in *text* and return
    ``(body_start, body_end, body)``.  None if the slot anchor pair
    is missing.
    """
    open_marker = f"<!-- cairn:slot {slot_name} -->"
    close_marker = f"<!-- cairn:end {slot_name} -->"
    o = text.lower().find(open_marker.lower())
    if o < 0:
        return None
    body_start = o + len(open_marker)
    c = text.lower().find(close_marker.lower(), body_start)
    if c < 0:
        return None
    return body_start, c, text[body_start:c]


def _slot_is_empty(body: str) -> bool:
    """A slot is "empty" if its body has no non-comment, non-blank
    content -- placeholder prose for adopter agents to fill is fine
    (it gets overwritten on merge)."""
    return body.strip() == ""


def _slot_is_customized(body: str) -> bool:
    """A slot is "customized" if it carries the
    ``<!-- cairn:customized -->`` marker (Antigravity P2 disposition).
    The helper preserves the existing content + the fidelity check
    skips substring-match for such slots.
    """
    return bool(_CUSTOMIZED_MARKER_RE.search(body))


def _normalize_for_compare(text: str) -> str:
    """Whitespace-collapsed + line-ending-normalized form for the
    ``already-current`` comparison.  Per Antigravity External code
    review B-P2: BOTH leading and trailing whitespace are stripped
    per-line so a slot nested inside a list item or blockquote
    (adopter file carries leading indentation; module's
    contributed text does not) doesn't false-positive as
    `stale-or-partial`.  Blank lines + LF/CRLF mix also tolerated.
    """
    return "\n".join(
        line.strip() for line in text.splitlines() if line.strip()
    )


def _write_slot_body(
    text: str, slot_name: str, new_body: str,
) -> str | None:
    """Replace the body of the named slot with *new_body* (sandwiched
    by a leading + trailing newline so the markers are on their own
    lines).  Returns the new text, or None if the slot is missing.
    """
    found = _slot_body_in_text(text, slot_name)
    if found is None:
        return None
    body_start, body_end, _ = found
    return (
        text[:body_start]
        + "\n" + new_body.strip("\n") + "\n"
        + text[body_end:]
    )


def resolve_slot_merge(
    text: str, slot_name: str, content: str,
) -> tuple[str, str | None, str]:
    """The **pure, text-level** decision for one module-into-slot merge.

    Returns ``(status, merged_text, body)``:

    * ``status`` -- ``missing-slot`` / ``customized`` / ``inserted`` /
      ``already-current`` / ``conflict``.
    * ``merged_text`` -- the post-merge text, non-``None`` **only** for
      ``inserted``, the one status that changes the target's bytes.
    * ``body`` -- the pre-merge slot body (``""`` when the anchor pair is
      absent); the conflict side-file needs it.

    **Single source of truth (module-merge lockfile divergence fix).**
    Both places that need to know what a merge does to a target file's
    bytes -- the live install (:func:`merge_module_into_slot`) and the
    lockfile's expected-clean-install computation (via
    :func:`apply_module_merges`, called by ``write_install_lockfile``) --
    call this one function, so they cannot silently drift apart on
    whether a given slot is inserted, preserved, or deferred. This is
    the same rule the ``dev/PLANNING.md`` onboarding overlay follows
    (see ``_rendered_onboarding_overlay``): a second implementation that
    "does the same thing" is exactly the failure mode being closed --
    when the two disagree, the writer's fail-closed divergence guard
    refuses to write ANY lockfile and the adopter silently ends up with
    no integrity baseline and no upgrade ancestor.

    Pure: reads no disk, writes nothing, raises nothing.
    """
    found = _slot_body_in_text(text, slot_name)
    if found is None:
        return "missing-slot", None, ""
    _, _, body = found
    if _slot_is_customized(body):
        return "customized", None, body
    if _slot_is_empty(body):
        return "inserted", _write_slot_body(text, slot_name, content), body
    if _normalize_for_compare(body) == _normalize_for_compare(content):
        return "already-current", None, body
    return "conflict", None, body


def apply_module_merges(
    text: str, merges: list[tuple[str, str]],
) -> str:
    """Replay an ordered ``(slot_name, content)`` merge sequence against
    *text* in memory and return the resulting text.

    The in-memory twin of the live merge pass's net effect on **one**
    target file: each merge sees the text as the previous merge left it,
    exactly as :func:`merge_module_into_slot` re-reads the file between
    merges, and only an ``inserted`` decision changes bytes. Every other
    status (``missing-slot`` / ``customized`` / ``already-current`` /
    ``conflict``) leaves the target untouched on the live path, so it
    leaves *text* untouched here.

    **Order is significant and is the caller's to fix.** Two merges
    naming the same slot with different content resolve first-wins (the
    second sees a non-empty body and becomes a deferred conflict), so
    this function is deterministic *for a given sequence* but not
    order-independent across sequences. The engine's one producer of that
    sequence is ``module_merge_directives``, which both callers use.

    Pure: no disk access, no side-file, no ``ModuleMergeResult``. The
    decision itself comes from :func:`resolve_slot_merge` -- the one
    function the live path also calls.
    """
    for slot_name, content in merges:
        status, merged_text, _body = resolve_slot_merge(
            text, slot_name, content,
        )
        if status == "inserted" and merged_text is not None:
            text = merged_text
    return text


@dataclass
class ModuleMergeResult:
    """Result of one (target, slot, content) merge attempt."""

    target_path: str
    slot_name: str
    status: str  # "inserted" / "already-current" / "customized" /
                 # "conflict-deferred" / "missing-slot" / "missing-target"
    side_file: str | None = None  # for "conflict-deferred"


def merge_module_into_slot(
    target_root: Path,
    target_rel: str,
    slot_name: str,
    content: str,
    *,
    non_interactive: bool,
    dry_run: bool = False,
) -> ModuleMergeResult:
    """Perform one module-to-slot merge against ``target_root/target_rel``.

    Behaviors:

    * Target file missing: status ``missing-target``.
    * Slot anchor pair missing in target: status ``missing-slot``.
    * Slot body customized (carries ``<!-- cairn:customized -->``):
      status ``customized`` (preserve existing content per
      Antigravity P2).
    * Slot body empty: insert + status ``inserted``.
    * Slot body matches *content* under whitespace-collapse:
      status ``already-current``.
    * Slot body differs: write the conflict to a per-slot side-file
      ``<target>.<slot-name>.cairn-merge-pending`` (Antigravity B-P1:
      per-slot path so two slots on the same target don't clobber
      each other) and return ``conflict-deferred``.

    The ``non_interactive`` parameter is reserved for the future
    interactive prompt branch (per the original Proposal B's
    a/b/c three-option prompt).  The current implementation always
    defers to a side-file (the safer default per the original
    Antigravity P1 disposition); the parameter is plumbed through
    so the interactive branch can be added without an API change
    (Antigravity B-P3 documentation note).

    The decision itself is NOT made here -- it comes from
    :func:`resolve_slot_merge`, the one function the lockfile writer's
    expected-clean-install computation also uses. This function owns only
    the I/O around that decision (containment guard, read, target write,
    side-file write) and the ``ModuleMergeResult`` reporting.
    """
    del non_interactive  # reserved for future interactive prompt branch
    dst = target_root / target_rel
    # Containment (SR6, final Security Review P1 #1): a module's merge-target
    # path is module-template-controlled, so an absolute / ``..`` / symlinked
    # target_rel could redirect the read or the write outside the adopter root.
    # Guard the destination before touching disk -- refuses a symlinked dst, a
    # symlinked parent, or any path resolving outside target_root.
    _assert_safe_write(dst, target_root)
    if not dst.is_file():
        return ModuleMergeResult(target_rel, slot_name, "missing-target")
    text = dst.read_text(encoding="utf-8")
    try:
        validate_unique_slot_names(text, target_rel)
    except DuplicateSlotError:
        raise

    status, merged_text, body = resolve_slot_merge(text, slot_name, content)
    if status == "missing-slot":
        return ModuleMergeResult(target_rel, slot_name, "missing-slot")
    if status == "customized":
        return ModuleMergeResult(target_rel, slot_name, "customized")
    if status == "inserted":
        if not dry_run and merged_text is not None:
            dst.write_text(merged_text, encoding="utf-8")
        return ModuleMergeResult(target_rel, slot_name, "inserted")
    if status == "already-current":
        return ModuleMergeResult(target_rel, slot_name, "already-current")
    # Conflict.  In this implementation, always defer to side-file
    # (non-interactive is the safe default per Antigravity P1's
    # author-modification: never silently keep, since that loses
    # the module's contributed prose without recording it).
    # Side-file path includes the slot name per Antigravity B-P1:
    # two conflicting slots on the same target file would otherwise
    # clobber the side-file when written sequentially.
    side_path = dst.with_name(
        f"{dst.name}.{slot_name}.cairn-merge-pending",
    )
    _assert_safe_write(side_path, target_root)  # the conflict side-file is a write too (P1 #1)
    if not dry_run:
        side_path.write_text(
            "<<<<<<< Cairn (module contribution)\n"
            + content.strip("\n") + "\n"
            "=======\n"
            + body.strip("\n") + "\n"
            ">>>>>>> existing (target slot)\n",
            encoding="utf-8",
        )
    return ModuleMergeResult(
        target_rel, slot_name, "conflict-deferred",
        side_file=str(side_path),
    )


def check_slot_fidelity(
    target_root: Path,
    expected_merges: list[tuple[str, str, str]],
) -> list[tuple[str, str, str]]:
    """For each expected (target, slot, content) declared by an
    installed module, verify the slot body **contains** the content
    (whitespace-collapsed substring match).  Returns a list of
    ``(target_rel, slot_name, reason)`` warnings -- empty list means
    every slot has its expected content.

    Reasons:

    * ``stale-or-partial`` -- slot non-empty + non-customized but
      doesn't contain the expected content.
    * ``empty`` -- slot still empty (the original audit-gap-#3
      failure mode).
    * ``missing-target`` / ``missing-slot`` -- target file or slot
      anchor pair missing.
    """
    warnings: list[tuple[str, str, str]] = []
    for target_rel, slot_name, content in expected_merges:
        dst = target_root / target_rel
        if not dst.is_file():
            warnings.append((target_rel, slot_name, "missing-target"))
            continue
        text = dst.read_text(encoding="utf-8")
        found = _slot_body_in_text(text, slot_name)
        if found is None:
            warnings.append((target_rel, slot_name, "missing-slot"))
            continue
        _, _, body = found
        if _slot_is_customized(body):
            continue  # marked intentionally customized; skip
        if _slot_is_empty(body):
            warnings.append((target_rel, slot_name, "empty"))
            continue
        if _normalize_for_compare(content) in _normalize_for_compare(body):
            continue  # contains the expected content
        warnings.append((target_rel, slot_name, "stale-or-partial"))
    return warnings


#: Document-author placeholders -- written as ``{{...}}`` but
#: intentionally *kept unfilled* in installed templates, to be filled
#: at write-time by a document author (e.g., a reviewer writing a
#: Review section).  The scaffold does not substitute these and the
#: post-scaffold "unfilled token" report excludes them.  Documented in
#: BOOTSTRAP.md Appendix A and templates/README.md.
_DOC_AUTHOR_TOKENS: frozenset[str] = frozenset(
    {
        "Maintainer",
        "author",
        "reviewer",
        "assessor",
    }
)


def substitute_tokens(text: str, tokens: dict[str, str]) -> str:
    """Replace ``{{key}}`` tokens found in *tokens*; leave others intact."""

    def _replace(m: re.Match[str]) -> str:
        return tokens.get(m.group(1), m.group(0))

    return _TOKEN_RE.sub(_replace, text)


def find_unfilled_tokens(text: str) -> list[str]:
    """Return token names that remain unfilled, excluding document-author
    placeholders that are intentionally kept unfilled at install time.
    """
    return [
        tok for tok in _TOKEN_RE.findall(text)
        if tok not in _DOC_AUTHOR_TOKENS
    ]


def find_block_slots(text: str) -> list[str]:
    """Return slot names found in *text* (open markers only)."""
    return _SLOT_RE.findall(text)


def find_unpaired_slots(text: str) -> list[str]:
    """Return slot names whose ``<!-- cairn:slot NAME -->`` opener has no
    matching ``<!-- cairn:end NAME -->`` closer, or vice versa.

    Useful for catching template-author errors at scaffold time rather
    than at customization time.
    """
    opens = _SLOT_RE.findall(text)
    closes = _SLOT_END_RE.findall(text)
    open_set = set(opens)
    close_set = set(closes)
    return sorted((open_set ^ close_set))
