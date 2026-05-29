#!/usr/bin/env python3
"""
scaffold.py — Cairn bootstrap mechanical scaffold.

Creates the ``dev/`` directory tree in a target repository, copies
the core Cairn templates and the selected module files, and
substitutes inline ``{{placeholder}}`` tokens.  Block slots
(``<!-- cairn:slot ... -->`` regions) are left in place for a
reasoning agent and the Maintainer to fill.

Usage
-----
::

    python bootstrap/scaffold.py --config profile.yml --target /path/to/repo

Config YAML format
------------------
::

    # Inline token values (mechanical substitution)
    project_name: "MyProject"
    test_command: "pytest"

    # Issue forge (optional). When set and the issue-capture module is
    # installed, the scaffold copies that forge's issue-template +
    # labels.yml starter into the adopter root (non-clobber). Omit, or
    # use an unknown value, to keep the reference a manual-copy starter.
    forge: gitlab        # gitlab | github

    # Module selection
    modules:
      # Default-on (remove only with a documented reason):
      - lifecycle-metrics
      - reflections
      - claim-check
      # Team-gated (add as the dimensional profile warrants):
      # - dual-review
      # - domain-agents
      # - legacy-agent
      # - dual-language-tests
      # - coordination-tiers

The ``--cairn-root`` flag overrides the auto-detected Cairn repo
root (defaults to the directory two levels above this script's
location: ``bootstrap/scaffold.py`` → ``bootstrap/`` → ``cairn/``).

The ``--dry-run`` flag prints the plan without writing any files.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NamedTuple

try:
    import yaml as _yaml  # type: ignore[import]

    def _yaml_load(text: str) -> Any:
        return _yaml.safe_load(text)

except ImportError:  # pragma: no cover
    _yaml = None  # type: ignore[assignment]

    def _yaml_load(text: str) -> Any:
        return _minimal_yaml_parse(text)


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
    """
    del non_interactive  # reserved for future interactive prompt branch
    dst = target_root / target_rel
    if not dst.is_file():
        return ModuleMergeResult(target_rel, slot_name, "missing-target")
    text = dst.read_text(encoding="utf-8")
    try:
        validate_unique_slot_names(text, target_rel)
    except DuplicateSlotError:
        raise

    found = _slot_body_in_text(text, slot_name)
    if found is None:
        return ModuleMergeResult(target_rel, slot_name, "missing-slot")
    _, _, body = found
    if _slot_is_customized(body):
        return ModuleMergeResult(target_rel, slot_name, "customized")
    if _slot_is_empty(body):
        if not dry_run:
            new_text = _write_slot_body(text, slot_name, content)
            if new_text is not None:
                dst.write_text(new_text, encoding="utf-8")
        return ModuleMergeResult(target_rel, slot_name, "inserted")
    if _normalize_for_compare(body) == _normalize_for_compare(content):
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


def run_module_merge_pass(
    templates_root: Path,
    target_root: Path,
    installed_modules: list[str],
    *,
    non_interactive: bool,
    dry_run: bool = False,
) -> tuple[list[ModuleMergeResult], list[tuple[str, str, str]]]:
    """Walk all installed modules + perform the merge pass + the
    fidelity check.

    Returns ``(merge_results, fidelity_warnings)``.  Modules without
    structured merge directives are silently skipped (transitional
    period; not every module ships directives yet).
    """
    results: list[ModuleMergeResult] = []
    expected: list[tuple[str, str, str]] = []
    for name in installed_modules:
        specs = _MODULE_MAPPINGS.get(name, [])
        for spec in specs:
            if spec.verbatim:
                continue
            module_src = templates_root / "modules" / spec.src
            if not module_src.is_file():
                continue
            module_text = module_src.read_text(encoding="utf-8")
            for target_rel, slot_name, content in (
                parse_module_merge_directives(module_text)
            ):
                expected.append((target_rel, slot_name, content))
                results.append(
                    merge_module_into_slot(
                        target_root, target_rel, slot_name, content,
                        non_interactive=non_interactive,
                        dry_run=dry_run,
                    )
                )
    warnings = check_slot_fidelity(target_root, expected)
    return results, warnings

#: The inline tokens the core and module templates currently use.  The
#: scaffold only substitutes tokens present in this set; unknown keys
#: from the config are silently ignored so that future tokens do not
#: break old configs.  Documented in BOOTSTRAP.md Appendix A.
KNOWN_TOKENS: frozenset[str] = frozenset(
    {
        "project_name",
        "test_command",
        "claim_check_command",
        "metrics_command",
    }
)

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

#: Default-on modules installed when the profile YAML omits a
#: ``modules:`` key.  Matches the doctrine in BOOTSTRAP.md Act I-5
#: step 2 ("Default-on modules (installed *unless* a dimension removes
#: them)").
_DEFAULT_ON_MODULES: tuple[str, ...] = (
    "lifecycle-metrics",
    "reflections",
    "claim-check",
    "fold-back-ledger",
    "incident-trackers",
    "documentation-plan",
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


# ---------------------------------------------------------------------------
# Minimal YAML fallback (no dependency on PyYAML)
# ---------------------------------------------------------------------------

def _minimal_yaml_parse(text: str) -> dict[str, Any]:
    """Very small YAML parser covering the subset scaffold.py needs.

    Handles::

        key: value
        key:
          - item

    Not a full YAML parser.  PyYAML is used when available.
    """
    result: dict[str, Any] = {}
    current_list_key: str | None = None

    def _list_item_text(stripped: str) -> str:
        """Strip leading ``- ``, an optional trailing ``# comment``, and
        surrounding quotes, returning the item value."""
        return stripped[2:].split("#")[0].strip().strip('"').strip("'")

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if line[:1] in (" ", "\t"):
            # Indented continuation -- list item under current_list_key.
            if current_list_key is not None and stripped.startswith("- "):
                item = _list_item_text(stripped)
                if item:
                    result.setdefault(current_list_key, []).append(item)
        elif stripped.startswith("- ") and current_list_key is not None:
            # Unindented list item under current_list_key.  PyYAML
            # accepts both ``key:\n  - a`` and ``key:\n- a`` shapes;
            # the minimal parser honors the second form too so a
            # PyYAML-free environment behaves the same way.
            item = _list_item_text(stripped)
            if item:
                result.setdefault(current_list_key, []).append(item)
        elif ":" in line:
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest and not rest.startswith("#"):
                # Recognize inline empty list/dict notations so e.g.
                # ``modules: []`` is honored as an explicit opt-out.
                if rest in ("[]", "{}"):
                    result[key] = []
                    current_list_key = None
                else:
                    result[key] = rest.strip('"').strip("'")
                    current_list_key = None
            else:
                current_list_key = key
                if key not in result:
                    result[key] = []

    return result


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_config(config_path: Path) -> dict[str, Any]:
    """Load a profile YAML config file."""
    text = config_path.read_text(encoding="utf-8")
    cfg = _yaml_load(text)
    if not isinstance(cfg, dict):
        raise ValueError(
            f"{config_path}: expected a YAML mapping at the top level, "
            f"got {type(cfg).__name__}"
        )
    return cfg


# ---------------------------------------------------------------------------
# dev/ directory tree
# ---------------------------------------------------------------------------

#: Relative paths (from repo root) that the scaffold always creates.
_DEV_DIRS: tuple[str, ...] = (
    "dev",
    "dev/proposals",
    "dev/proposals/archive",
    "dev/plans",
    "dev/plans/archive",
    # The strategy-doc lifecycle directory (Antigravity External
    # code review A-P3 on commit 96b7fba): scaffolded by default so
    # adopters who use the commit-permission exception extension's
    # `dev/strategy/` coverage don't have to `mkdir` manually.
    "dev/strategy",
    "dev/strategy/archive",
    "dev/modules",
    # Progressive-onboarding module's installed-source-file home.
    # Per plan 2026-05-28-claude-cairn-progressive-onboarding (Chunk
    # P1.1, Codex P1-1 disposition): scaffold inlines a preset's seed
    # tasks into `dev/PLANNING.md` and ALSO copies the full source
    # file here so the activation helper can discover deferred tasks
    # at goodnight.  The directory exists from install time onward.
    "dev/modules/onboarding",
    # Progressive-onboarding state-file directory (Chunk P1.2 per
    # Codex P2-5 disposition: tracked, parallel to dev/intents.jsonl).
    # The scaffold creates this dir + writes an empty activation log
    # (`onboarding-activated.jsonl`) at install time so the helper
    # never has to mkdir; the tracked state means multi-team profiles
    # share activation history through git.
    "dev/.cairn",
)


def create_dev_tree(target: Path, *, dry_run: bool = False) -> list[Path]:
    """Create the ``dev/`` directory tree under *target*.

    Returns the list of directories that were (or would be) created.
    """
    created: list[Path] = []
    for rel in _DEV_DIRS:
        d = target / rel
        if not d.exists():
            if not dry_run:
                d.mkdir(parents=True, exist_ok=True)
            created.append(d)
    return created


# ---------------------------------------------------------------------------
# Template installation
# ---------------------------------------------------------------------------

# Each entry is (source path relative to cairn/templates/, target path
# relative to repo root).
_CORE_MAPPINGS: tuple[tuple[str, str], ...] = (
    # repo root
    ("core/AGENTS.md",                              "AGENTS.md"),
    # Thin vendor wrapper (foldback #12): installed as VENDOR.md, a
    # vendor-neutral `@AGENTS.md` + harness-addendum template the
    # adopter renames to their tool's file (CLAUDE.md, etc.).  Core
    # ships no literal vendor name (R-G).
    ("core/VENDOR.md",                              "VENDOR.md"),
    # dev/ tree
    ("core/dev/README.md",                          "dev/README.md"),
    ("core/dev/PLANNING.md",                        "dev/PLANNING.md"),
    ("core/dev/NEXT_SESSION.md",                    "dev/NEXT_SESSION.md"),
    ("core/dev/collaboration_agreement.md",         "dev/collaboration_agreement.md"),
    ("core/dev/agent_collaboration.md",             "dev/agent_collaboration.md"),
    ("core/dev/proposals/_template.md",             "dev/proposals/_template.md"),
    ("core/dev/plans/_template.md",                 "dev/plans/_template.md"),
)

# Optional top-level templates, gated on a dimension axis.  Unlike
# modules (which land under ``dev/modules/``), these are project-root
# files an adopter's *human* contributors read.  Each entry is
# ``(src rel to templates/, dst rel to repo root, gate axis, selecting
# values)``: the template installs when the *resolved* profile value for
# that axis is in the selecting set.  An installed optional template is
# recorded under ``optional_templates:`` in the fidelity manifest so the
# gate is auditable (bootstrap/fidelity-check.md).
_OPTIONAL_TEMPLATES: tuple[tuple[str, str, str, frozenset[str]], ...] = (
    # CONTRIBUTING.md — the human-contributor entry (foldback #10),
    # installed when the repo expects human authors beyond a solo
    # maintainer: the human-team axis at small-multi or large-multi.
    (
        "optional/CONTRIBUTING.md",
        "CONTRIBUTING.md",
        "human_team",
        frozenset({"small-multi", "large-multi"}),
    ),
)


def select_optional_templates(axes: dict[str, object]) -> list[tuple[str, str]]:
    """Return ``(src, dst)`` for each optional template whose dimension
    gate the profile satisfies.

    *axes* is the **resolved** dimension profile — a preset's canonical
    point merged with the adopter's overrides (``resolve_axes``), or the
    raw profile when no ``preset:`` is used.  A profile that omits the
    gate axis, or sets it to a non-selecting value, gets no optional
    template — the conservative default.
    """
    selected: list[tuple[str, str]] = []
    for src, dst, axis, values in _OPTIONAL_TEMPLATES:
        if str(axes.get(axis, "")) in values:
            selected.append((src, dst))
    return selected


class InstallSpec(NamedTuple):
    """One file a module installs.

    ``src`` is relative to ``cairn/templates/modules/``; ``dst`` is
    relative to the target repo root.  ``verbatim`` marks an executable
    script (or any non-template asset) that is copied **byte-for-byte**:
    no ``{{token}}`` substitution runs over it, and it is not scanned for
    unfilled tokens / block slots (a code file's f-string braces or
    docstring would otherwise false-positive the post-scaffold report).
    """

    src: str
    dst: str
    verbatim: bool = False


# Module name → list of InstallSpec (1:many).  Most modules install a
# single substituted ``.md`` doctrine file; the two default-on
# discipline modules also install their reference *script* verbatim
# (Cairn v0.2 P1).  The script ``dst`` paths are the single source of
# truth for the command-token defaults below (see
# ``_REFERENCE_SCRIPT_TOKEN`` and ``reference_script_token_defaults``)
# so the doc's "run it via {{...}}" line and the install destination
# cannot desync.
_MODULE_MAPPINGS: dict[str, list[InstallSpec]] = {
    # default-on
    "lifecycle-metrics": [
        InstallSpec("default-on/lifecycle-metrics.md",
                    "dev/modules/lifecycle-metrics.md"),
        InstallSpec("default-on/lifecycle_metrics.py",
                    "tools/lifecycle_metrics.py", verbatim=True),
    ],
    "reflections": [
        InstallSpec("default-on/reflections.md", "dev/modules/reflections.md"),
    ],
    "claim-check": [
        InstallSpec("default-on/claim-check.md",
                    "dev/modules/claim-check.md"),
        InstallSpec("default-on/claim_check.py",
                    "scripts/claim_check.py", verbatim=True),
    ],
    # The deployment-side measurement substrate the adaptive-doctrine
    # rate-limit gate (doctrine/rationale.md) evaluates against.
    # Ships the module doctrine + a forkable tracker template; adopters
    # fork the template to one or many live trackers (e.g.,
    # dev/incident_log.md or class-specific files), then the goodnight
    # migration sub-step feeds incident entries from reflections into
    # the trackers.  The canonical 7-column semantic-field schema is
    # the contract the eventual Goal 7 cross-adopter harvest reads.
    "incident-trackers": [
        InstallSpec("default-on/incident-trackers.md",
                    "dev/modules/incident-trackers.md"),
        InstallSpec("default-on/incident_log_template.md",
                    "dev/modules/incident_log_template.md"),
    ],
    # The placement-decision procedure for documentation and doctrine.
    # Default-on: every adopter benefits from a four-layer routing
    # discipline (entry / governing / deliberation / descriptive).
    # Ships the module doctrine + a forkable DOCUMENTATION_PLAN.md the
    # adopter customizes for their own file inventory + tier vocabulary.
    # Three slot anchors land via the core templates --
    # `documentation-discipline` in AGENTS.md plus
    # `documentation-tier-home` in proposals + plans `_template.md` --
    # and are filled by **manual paste** from the module's
    # `Merged into:` Blocks 1/2/3 (the adopter copies the block matching
    # each target slot at install time, parallel to the existing
    # claim-check / lifecycle-metrics / reflections module pattern).
    # Mechanical merge via Proposal B's `cairn:merge-target` directives
    # is *deferred* pending the merge-pass / install-lockfile interaction
    # fix (the merge pass mutates files post-install, which the
    # lockfile's clean-install divergence guard rejects); see
    # `dev/PLANNING.md` (modflow_tools-side) > "Cairn-side merge-helper
    # / install-lockfile interaction fix".  The forkable's worked
    # examples are adopter-relative; Cairn's own self-hosted instance at
    # cairn/docs/DOCUMENTATION_PLAN.md uses cairn-prefixed paths and is
    # the methodology source-of-truth.
    "documentation-plan": [
        InstallSpec("default-on/documentation-plan.md",
                    "dev/modules/documentation-plan.md"),
        InstallSpec("default-on/documentation_plan_template.md",
                    "docs/DOCUMENTATION_PLAN.md"),
    ],
    # The deployment-side fold-back channel (doctrine: doctrine/fold-back.md).
    # Default-on but omittable: ships the module doctrine + the forkable
    # ledger artifact into dev/upstream/, the active-surfacing prompt asset
    # into dev/modules/, the export-scrub scanner doc into dev/modules/, and
    # the scanner itself verbatim into scripts/.  The ledger is a cross-repo
    # export surface, so its template carries a [SECURITY WARNING] header;
    # the scanner is the machine half of the active-surfacing protocol's
    # two-gate export boundary (the manual half is the maintainer-signed
    # affirmation field in the Cairn issue / PR template).
    "fold-back-ledger": [
        InstallSpec("default-on/fold-back-ledger.md",
                    "dev/modules/fold-back-ledger.md"),
        InstallSpec("default-on/fold-back-ledger-template.md",
                    "dev/upstream/fold-back-ledger.md"),
        # Active-surfacing additions (Chunks 4-6 of
        # 2026-05-28-claude-cairn-foldback-active-surfacing).
        InstallSpec("default-on/foldback_export_scan.md",
                    "dev/modules/foldback_export_scan.md"),
        InstallSpec("default-on/foldback_export_scan.py",
                    "scripts/foldback_export_scan.py", verbatim=True),
        InstallSpec("default-on/fold-back-active-prompt.md",
                    "dev/modules/fold-back-active-prompt.md"),
        # Optional helper (Chunk 8): lists open `candidate`-status
        # rows from the ledger eligible for active surfacing.  Ships
        # verbatim into adopter scripts/; invocation in the agent
        # prompt is `python scripts/foldback_suggest.py [--ledger
        # <path>] [--all]`.
        InstallSpec("default-on/foldback_suggest.py",
                    "scripts/foldback_suggest.py", verbatim=True),
    ],
    # team-gated
    "dual-review": [
        InstallSpec("team-gated/dual-review.md", "dev/modules/dual-review.md"),
    ],
    "domain-agents": [
        InstallSpec("team-gated/domain-agents.md",
                    "dev/modules/domain-agents.md"),
    ],
    "legacy-agent": [
        InstallSpec("team-gated/legacy-agent.md",
                    "dev/modules/legacy-agent.md"),
    ],
    "dual-language-tests": [
        InstallSpec("team-gated/dual-language-tests.md",
                    "dev/modules/dual-language-tests.md"),
    ],
    "coordination-tiers": [
        InstallSpec("team-gated/coordination-tiers.md",
                    "dev/modules/coordination-tiers.md"),
        # Cairn v0.2 P5: the work-intent tool ships verbatim alongside the
        # doctrine (1:many, the P1 claim-check/lifecycle-metrics pattern).
        InstallSpec("team-gated/intent.py",
                    "tools/intent.py", verbatim=True),
    ],
    "security-review": [
        InstallSpec("team-gated/security-review.md",
                    "dev/modules/security-review.md"),
    ],
    "issue-capture": [
        InstallSpec("team-gated/issue-capture.md",
                    "dev/modules/issue-capture.md"),
    ],
    "model-selection": [
        InstallSpec("team-gated/model-selection.md",
                    "dev/modules/model-selection.md"),
    ],
    # Practice-discipline modules (Cairn v0.2 P3).  Team-gated -- a
    # governance preset (P4) turns them on per profile rather than
    # doubling the default-on auto-install set.  Doctrine-only (single
    # substituted .md each; no scripts).
    "testing-discipline": [
        InstallSpec("team-gated/testing-discipline.md",
                    "dev/modules/testing-discipline.md"),
    ],
    "doc-drift-prevention": [
        InstallSpec("team-gated/doc-drift-prevention.md",
                    "dev/modules/doc-drift-prevention.md"),
        # Cairn v0.2 foldback: the module flips from doctrine-only to
        # doctrine + stack-neutral runnable tooling (1:many, the P1
        # claim-check pattern).  Two verbatim stdlib-only scripts -- the
        # link half and the snippet-sync.  The claim half is NOT shipped
        # here: the default-on claim-check module already installs
        # scripts/claim_check.py, so the doc-drift gate composes with it
        # rather than duplicating a second checker.  The schema-doc
        # generator is deferred (an adopter slot/hook) -- it cannot ship
        # stack-neutrally.
        InstallSpec("team-gated/link_check.py",
                    "scripts/link_check.py", verbatim=True),
        InstallSpec("team-gated/sync_doc_snippets.py",
                    "scripts/sync_doc_snippets.py", verbatim=True),
    ],
    "examples-gallery": [
        InstallSpec("team-gated/examples-gallery.md",
                    "dev/modules/examples-gallery.md"),
    ],
    # Cairn v0.2 security-hardening (R9): the content-integrity scanner,
    # shipped to adopters so their agents can scan working-tree files /
    # incoming PRs for prompt-injection patterns before ingesting them. The
    # verbatim script is single-sourced here (Cairn's own check_cairn composes
    # the same file), the 1:many claim-check pattern.
    "content-security": [
        InstallSpec("team-gated/content-security.md",
                    "dev/modules/content-security.md"),
        InstallSpec("team-gated/content_scan.py",
                    "scripts/content_scan.py", verbatim=True),
    ],
}

# Module → the inline command-token whose value should default to the
# module's installed reference script.  The default value is derived
# from the verbatim spec's ``dst`` (below), so the token the module doc
# resolves (``{{claim_check_command}}`` etc.) and the path the scaffold
# installs to are one source of truth (I5).
_REFERENCE_SCRIPT_TOKEN: dict[str, str] = {
    "claim-check": "claim_check_command",
    "lifecycle-metrics": "metrics_command",
}

#: Module → ``.gitignore`` entries the scaffold seeds when the module is
#: selected.  Cairn v0.2 P5: the work-intent log is session-local
#: coordination state, never a tracked artifact, so selecting
#: ``coordination-tiers`` seeds the substrate path.  Seeding is
#: non-clobber + idempotent (see :func:`seed_gitignore`).
_GITIGNORE_SEEDS: dict[str, tuple[str, ...]] = {
    "coordination-tiers": ("dev/intents.jsonl",),
    # Foldback active-surfacing (2026-05-28 arc): the protocol's Scrub
    # step writes the drafted issue / PR body to a gitignored temp
    # file pattern under `dev/upstream/` before invoking the scanner.
    # The draft file is intentionally never committed -- the durable
    # record is the filed Cairn issue / PR + the ledger row's
    # status transition.  Seeded by default so an adopter does not
    # have to remember the pattern themselves.
    "fold-back-ledger": ("dev/upstream/.foldback-draft-*.md",),
}


def seed_gitignore(
    target: Path,
    entries: tuple[str, ...] | list[str],
    *,
    dry_run: bool = False,
) -> list[str]:
    """Append *entries* to ``<target>/.gitignore`` if absent.

    Adopter-owned-file contract (Cairn v0.2 P5, C6): **non-clobber**
    (existing content preserved verbatim), **idempotent** (an entry
    already present -- exact-line match, ignoring surrounding
    whitespace -- is never re-added, so repeated scaffolds add no
    duplicate lines), and **``--dry-run`` aware** (returns what *would*
    be added without writing).  Returns the entries actually added (or
    that would be added under ``dry_run``); an empty list means the
    file already covered everything.
    """
    gitignore = target / ".gitignore"
    text = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    existing = {ln.strip() for ln in text.splitlines()}
    to_add = [e for e in entries if e not in existing]
    if not to_add or dry_run:
        return to_add
    prefix = text
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    block = "\n".join(to_add) + "\n"
    gitignore.write_text(prefix + block, encoding="utf-8")
    return to_add


def reference_script_token_defaults(module_names: list[str]) -> dict[str, str]:
    """Default command-token values for the selected reference-script
    modules.

    For each selected module that ships a verbatim reference script, map
    its command token (``claim_check_command`` / ``metrics_command``) to
    ``python <dst>`` where ``<dst>`` is the exact path the scaffold
    installs the script to.  The caller injects these into the token set
    *without* overriding a value the profile already supplied
    (``setdefault`` semantics), so an adopter can still point the token
    at a custom invocation.
    """
    defaults: dict[str, str] = {}
    for name in module_names:
        token = _REFERENCE_SCRIPT_TOKEN.get(name)
        if token is None:
            continue
        for spec in _MODULE_MAPPINGS.get(name, []):
            if spec.verbatim:
                defaults[token] = f"python {spec.dst}"
                break
    return defaults


# ---------------------------------------------------------------------------
# Governance presets (Cairn v0.2 P4)
# ---------------------------------------------------------------------------
#
# Presets are *named points in the six-axis dimension model*, not a parallel
# config system.  An adopter picks a preset (the fast path) instead of
# hand-deriving the module roster; the six-axis scoring + the BOOTSTRAP.md
# I-5 gate table remain the principled backing (the gate table is the
# canonical per-module rationale).  See BOOTSTRAP.md Act I and the
# the source ``cairn-v0.2-p4-governance-presets`` plan.

#: The six dimension axes -> allowed enum values (the BOOTSTRAP.md I-4 table).
#: An adopter overrides a preset's canonical axis by setting a flat top-level
#: key in the profile YAML; an unknown enum value is a hard error.
_AXES: dict[str, tuple[str, ...]] = {
    "age": ("greenfield", "legacy"),
    "size": ("small", "medium", "large"),
    "complexity": ("simple", "moderate", "complex"),
    "language": ("single", "multi"),
    "human_team": ("solo", "small-multi", "large-multi"),
    "agent_team": (
        "single", "concurrent-single-type", "concurrent-multi-type",
    ),
}

#: Modules whose staffability is a pure function of the team axes.  These are
#: the ONLY part of the I-5 gate evaluated as runtime code; the non-axis gate
#: conditions (trust boundary, issue tracker, domain partitioning, legacy
#: readiness) are baked into each preset's authored baseline below (the
#: "gate-table encoding" split from the P4 plan).  Both gate on
#: ``agent_team == concurrent-multi-type`` per the I-5 table.
_TEAM_STAFFING_GATED: tuple[str, ...] = ("dual-review", "coordination-tiers")


def _can_staff_team_modules(axes: dict[str, str]) -> bool:
    """True when the resolved agent-team axis can staff the team-staffing
    modules (concurrent-multi-type)."""
    return axes.get("agent_team") == "concurrent-multi-type"


#: Named governance presets.  Each carries a **canonical six-axis point** and
#: a **baseline roster** of the *non-team-staffing* modules the I-5 gate table
#: yields at that point (axis-derivable rows resolved at the canonical scores,
#: plus the non-axis rows the preset's profile assumes).  The team-staffing
#: modules (``dual-review`` / ``coordination-tiers``) are NOT listed here --
#: they are added at expand time iff the *resolved* agent-team axis staffs
#: them, so an adopter's real team is ground truth (F3).  ``_DEFAULT_ON_MODULES``
#: is always the floor.  Derivation is documented row-by-row in BOOTSTRAP.md.
_PRESETS: dict[str, dict[str, object]] = {
    "solo-greenfield": {
        "axes": {
            "age": "greenfield", "size": "small", "complexity": "simple",
            "language": "single", "human_team": "solo",
            "agent_team": "single",
        },
        # Minimal: default-on only; no axis fires a team-gated module.
        "baseline": (),
    },
    "collaborative-team": {
        "axes": {
            "age": "greenfield", "size": "medium", "complexity": "moderate",
            "language": "single", "human_team": "small-multi",
            "agent_team": "concurrent-multi-type",
        },
        # complexity=moderate -> model-selection + testing-discipline;
        # size=medium -> doc-drift-prevention.  Coordination modules come
        # from the team-staffing gate (agent_team=concurrent-multi-type).
        "baseline": (
            "model-selection", "testing-discipline", "doc-drift-prevention",
        ),
    },
    "high-rigor-legacy": {
        "axes": {
            "age": "legacy", "size": "large", "complexity": "complex",
            "language": "multi", "human_team": "large-multi",
            "agent_team": "concurrent-multi-type",
        },
        # age=legacy -> legacy-agent; complexity=complex -> model-selection
        # + testing-discipline; size=large/language=multi ->
        # doc-drift-prevention; language=multi -> dual-language-tests;
        # trust-boundary (non-axis, assumed for legacy/large) ->
        # security-review.  Coordination modules from the team-staffing gate.
        "baseline": (
            "legacy-agent", "security-review", "dual-language-tests",
            "model-selection", "testing-discipline", "doc-drift-prevention",
        ),
    },
}


class PresetError(ValueError):
    """Raised on an invalid preset / override config (unknown preset, unknown
    module, unknown axis enum, wrong-type value, or the ``modules:`` +
    ``preset:`` conflict).  A friendly hard error, surfaced by ``main()``."""


def _as_str_list(value: object, key: str) -> list[str]:
    """Coerce a YAML value for a list-typed key to ``list[str]``; a scalar
    where a list is expected is a friendly hard error."""
    if value is None:
        return []
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise PresetError(
            f"`{key}` must be a YAML list (e.g. `{key}:` with `- module` "
            f"lines), not a {type(value).__name__} ({value!r})."
        )
    return [str(v) for v in value]


def _canonical_order(modules: set[str]) -> list[str]:
    """Order a module set deterministically: default-on first (in
    ``_DEFAULT_ON_MODULES`` order), then the rest in ``_MODULE_MAPPINGS``
    order.  Stable, diffable output for the summary + tests."""
    ordered: list[str] = [m for m in _DEFAULT_ON_MODULES if m in modules]
    for name in _MODULE_MAPPINGS:
        if name in modules and name not in ordered:
            ordered.append(name)
    # Any module not in the known maps (shouldn't happen post-validation)
    # trails, sorted, so nothing is silently dropped.
    ordered.extend(sorted(modules - set(ordered)))
    return ordered


def resolve_axes(preset_name: str, cfg: dict[str, object]) -> dict[str, str]:
    """Resolve the six-axis point: the preset's canonical point overridden by
    any flat axis key the adopter supplied.  An unknown enum value is a hard
    error; an absent axis key falls back to the preset's value (F3 / P-2)."""
    canonical = dict(_PRESETS[preset_name]["axes"])  # type: ignore[arg-type]
    resolved = dict(canonical)
    for axis, allowed in _AXES.items():
        if axis in cfg and cfg[axis] is not None:
            value = str(cfg[axis])
            if value not in allowed:
                raise PresetError(
                    f"axis `{axis}` value {value!r} is not one of "
                    f"{', '.join(allowed)}."
                )
            resolved[axis] = value
    return resolved


def expand_preset(cfg: dict[str, object]) -> tuple[list[str], dict[str, object]]:
    """Expand a ``preset:``-bearing profile into a module roster + a summary.

    The pinned ordered merge (P4 Decision):

    1. Resolve axes = preset canonical point overridden by adopter axis keys.
    2. Baseline = ``_DEFAULT_ON_MODULES`` (always) + the preset's authored
       non-team-staffing roster + the team-staffing modules iff the resolved
       agent-team axis staffs them.
    3. Apply ``modules_add`` then ``modules_remove`` -- **remove wins** on a
       same-module conflict; an explicit add of an unstaffable module installs
       it with a loud staffability warning.
    4. (Backward-compat for the no-preset cases is handled in ``main()``.)

    Returns ``(ordered_modules, summary)`` where ``summary`` carries the
    preset, resolved axes, roster, overrides, and any warnings (for the
    ``--summary`` acceptance artifact).
    """
    preset_name = str(cfg.get("preset") or "").strip()
    if preset_name not in _PRESETS:
        raise PresetError(
            f"unknown preset {preset_name!r}; choose one of "
            f"{', '.join(sorted(_PRESETS))}."
        )

    resolved_axes = resolve_axes(preset_name, cfg)

    # Step 2: baseline.
    baseline: set[str] = set(_DEFAULT_ON_MODULES)
    baseline |= set(_PRESETS[preset_name]["baseline"])  # type: ignore[arg-type]
    staffable = _can_staff_team_modules(resolved_axes)
    if staffable:
        baseline |= set(_TEAM_STAFFING_GATED)

    # Step 3: explicit overrides (validate names first).
    adds = _as_str_list(cfg.get("modules_add"), "modules_add")
    removes = _as_str_list(cfg.get("modules_remove"), "modules_remove")
    known = set(_MODULE_MAPPINGS) | set(_DEFAULT_ON_MODULES)
    for name in adds + removes:
        if name not in known:
            raise PresetError(
                f"unknown module {name!r} in modules_add/modules_remove; "
                f"known modules: {', '.join(sorted(known))}."
            )

    warnings: list[str] = []
    # Adds first.  An add of a team-staffing module the resolved team can't
    # staff installs anyway (adopter intent wins) with a loud warning (I1).
    for name in adds:
        if name in _TEAM_STAFFING_GATED and not staffable:
            warnings.append(
                f"`{name}` was explicitly added but the resolved agent-team "
                f"axis ({resolved_axes.get('agent_team')}) cannot staff it; "
                f"installing per your explicit request -- confirm the team "
                f"configuration can staff the module's coordination "
                f"requirements before relying on it."
            )
    roster = set(baseline) | set(adds)
    # Removes win on conflict.
    removed_default_on: list[str] = []
    for name in removes:
        roster.discard(name)
        if name in _DEFAULT_ON_MODULES:
            removed_default_on.append(name)

    ordered = _canonical_order(roster)
    summary: dict[str, object] = {
        "preset": preset_name,
        "axes": resolved_axes,
        "modules": ordered,
        "modules_add": adds,
        "modules_remove": removes,
        "removed_default_on": removed_default_on,
        "staffability_warnings": warnings,
    }
    return ordered, summary


def format_profile_summary(cfg: dict[str, object]) -> str:
    """Render the Maintainer-facing Act I-6 profile summary for a
    ``preset:``-bearing profile (the ``--summary`` acceptance artifact, P-4).

    Shows the chosen preset, the resolved six-axis point, the expanded module
    roster, the explicit add/remove overrides, any default-on opt-outs, and
    any staffability warnings -- so the Maintainer sees *why* the roster came
    out this way before anything is installed."""
    _modules, s = expand_preset(cfg)
    lines: list[str] = []
    project = str(cfg.get("project_name") or "<project_name>")
    lines.append(f"## Dimension profile -- {project}")
    lines.append("")
    lines.append(f"Preset: {s['preset']}")
    lines.append("")
    lines.append("Six-axis point (resolved):")
    for axis in _AXES:
        lines.append(f"  {axis:12s} {s['axes'][axis]}")  # type: ignore[index]
    lines.append("")
    lines.append("Module roster (to install):")
    for m in s["modules"]:  # type: ignore[union-attr]
        lines.append(f"  - {m}")
    if s["modules_add"]:
        lines.append(f"\nExplicit add:    {', '.join(s['modules_add'])}")  # type: ignore[arg-type]
    if s["modules_remove"]:
        lines.append(f"Explicit remove: {', '.join(s['modules_remove'])}")  # type: ignore[arg-type]
    if s["removed_default_on"]:
        lines.append(
            f"Default-on opted out: {', '.join(s['removed_default_on'])}"  # type: ignore[arg-type]
        )
    if s["staffability_warnings"]:
        lines.append("")
        # Same per-warning line format as the installer path in main()
        # (`[warn] staffability: ...`), so programmatic detection and the
        # user-facing presentation are consistent across both surfaces.
        for w in s["staffability_warnings"]:  # type: ignore[union-attr]
            lines.append(f"  [warn] staffability: {w}")
    lines.append("")
    lines.append("Does this profile look right before I install anything?")
    return "\n".join(lines) + "\n"


#: Result record for one installed file.
#: ``status`` is ``"installed"`` (file written), ``"skipped-exists"``
#: (skipped because the file already existed and ``force`` was not
#: set), or ``"dry-run"`` (would have been written under
#: ``--dry-run``).
InstallResult = tuple[Path, list[str], list[str], str]
# (target_path, unfilled_token_names, block_slot_names, status)


class ScaffoldSecurityError(Exception):
    """Raised when an install would write through a symlink or escape the
    target directory (Layer-4 executable hardening).  Fail-closed: the
    scaffold refuses the write rather than following the redirect."""


def _assert_safe_write(dst: Path, target: Path) -> None:
    """Refuse to write through a symlink or outside *target* (Layer 4).

    Runs before **every** write (fresh or ``--force``), not only
    overwrites: ``Path.exists()`` follows symlinks and returns ``False``
    for a *dangling* symlink, so a guard scoped to the ``--force`` path
    would let a fresh install write through a planted symlink at ``dst``
    -- or through a **symlinked parent directory** -- and escape
    ``target``.  Three fail-closed checks:

    1. ``dst`` itself must not be a symlink.
    2. No existing directory **between** ``target`` and ``dst`` may be a
       symlink (a symlinked parent redirects the write even when ``dst``
       is a normal name).
    3. The resolved final write path must stay within ``target`` (defense
       in depth against an ``..`` / absolute ``dst``).

    ``target`` is already ``resolve()``-d by the caller.  The containment
    check is 3.8-safe (``try: relative_to; except ValueError``) -- it does
    **not** use ``Path.is_relative_to`` (3.9+).
    """
    target_resolved = target.resolve()

    # (1) dst must not itself be a symlink.
    if dst.is_symlink():
        raise ScaffoldSecurityError(
            f"refusing to write through a symlinked destination: {dst}"
        )

    # (2) no existing ancestor strictly inside target may be a symlink.
    for ancestor in dst.parents:
        if ancestor == target_resolved:
            break  # reached target itself; don't police above it
        try:
            ancestor.relative_to(target_resolved)
        except ValueError:
            break  # ancestor is at/above target -- stop walking
        if ancestor.is_symlink():
            raise ScaffoldSecurityError(
                f"refusing to write through a symlinked parent: {ancestor}"
            )

    # (3) the resolved final path must stay within target.
    final = dst.parent.resolve() / dst.name
    try:
        final.relative_to(target_resolved)
    except ValueError:
        raise ScaffoldSecurityError(
            f"refusing to write outside the target directory: {final} "
            f"is not under {target_resolved}"
        )


def _install_one(
    src: Path,
    dst: Path,
    tokens: dict[str, str],
    target: Path,
    *,
    dry_run: bool,
    force: bool = False,
    verbatim: bool = False,
) -> InstallResult:
    """Copy *src* to *dst*.  Returns an InstallResult.

    Token-substituted by default.  When ``verbatim`` is True the file is
    copied **byte-for-byte** -- no ``{{token}}`` substitution, no
    unpaired-slot warning, and the result's unfilled-token / block-slot
    lists are **empty** (a script's f-string braces or docstring must
    not be scanned as template tokens / slots, else the post-scaffold
    report false-positives on code).  This is the I4 contract for the
    1:many script-install path.

    Default-safe: if *dst* already exists and *force* is False, the
    file is **not** overwritten and the result's status is
    ``"skipped-exists"``.  Re-running the scaffold against an
    already-installed repo therefore preserves filled block slots and
    other customizations; pass ``--force`` to opt into overwriting.
    """
    text = src.read_text(encoding="utf-8")

    if verbatim:
        # No substitution, no slot/token scan -- code is not a template.
        unfilled: list[str] = []
        slots: list[str] = []
    else:
        # Pre-substitution: warn about template-author errors (unpaired
        # cairn:slot markers) before the file ships.  These would
        # manifest as a malformed installed file otherwise; cheaper to
        # catch here.
        unpaired = find_unpaired_slots(text)
        if unpaired:
            print(
                f"  [warn] {src.name}: unpaired slot marker(s): "
                f"{', '.join(unpaired)} (each open `cairn:slot NAME` needs "
                f"a matching `cairn:end NAME`)",
                file=sys.stderr,
            )
        text = substitute_tokens(text, tokens)
        unfilled = find_unfilled_tokens(text)
        slots = find_block_slots(text)

    if dry_run:
        return dst, unfilled, slots, "dry-run"

    if dst.exists() and not force:
        print(
            f"  [skip] {dst}: already exists -- pass --force to overwrite "
            f"(re-running the scaffold without --force preserves any "
            f"customizations the file already carries)",
            file=sys.stderr,
        )
        return (dst, unfilled, slots, "skipped-exists")

    # Layer-4 hardening: refuse to write through a symlink or outside
    # target -- on every write, fresh or --force (fail-closed).
    _assert_safe_write(dst, target)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
    return dst, unfilled, slots, "installed"


def install_core(
    templates_root: Path,
    target: Path,
    tokens: dict[str, str],
    *,
    dry_run: bool = False,
    force: bool = False,
) -> list[InstallResult]:
    """Copy core templates into *target*, substituting tokens."""
    results: list[InstallResult] = []
    for src_rel, dst_rel in _CORE_MAPPINGS:
        src = templates_root / src_rel
        if not src.exists():
            print(f"  [warn] core template missing: {src_rel}", file=sys.stderr)
            continue
        dst = target / dst_rel
        results.append(
            _install_one(src, dst, tokens, target, dry_run=dry_run, force=force)
        )
    return results


def install_optional(
    templates_root: Path,
    target: Path,
    tokens: dict[str, str],
    optional: list[tuple[str, str]],
    *,
    dry_run: bool = False,
    force: bool = False,
) -> list[InstallResult]:
    """Copy the dimension-selected optional templates into *target*.

    *optional* is the ``(src, dst)`` list from
    ``select_optional_templates``; source paths are relative to
    ``cairn/templates/`` (like ``_CORE_MAPPINGS``).
    """
    results: list[InstallResult] = []
    for src_rel, dst_rel in optional:
        src = templates_root / src_rel
        if not src.exists():
            print(
                f"  [warn] optional template missing: {src_rel}",
                file=sys.stderr,
            )
            continue
        dst = target / dst_rel
        results.append(
            _install_one(src, dst, tokens, target, dry_run=dry_run, force=force)
        )
    return results


# ---------------------------------------------------------------------------
# Progressive onboarding -- preset-keyed slot substitution
# ---------------------------------------------------------------------------

#: Three named preset onboarding files (under
#: ``templates/onboarding/<name>.md``).  An adopter's chosen preset
#: maps 1:1 to one of these files; the scaffold inlines the file's
#: seed tasks into ``dev/PLANNING.md``'s ``onboarding-tasks`` slot and
#: copies the full source file to ``dev/modules/onboarding/<name>.md``
#: as the authoritative reference for deferred-task discovery at
#: goodnight (Codex P1-1 / P2-4 disposition: seed-only PLANNING render
#: + tracked installed source).
_ONBOARDING_PRESETS: frozenset[str] = frozenset(
    {"solo-greenfield", "collaborative-team", "high-rigor-legacy"}
)

#: Matches ``* [seed; id: <name>]`` task lines in a preset onboarding
#: file.  The bracket payload syntax also accepts other ``key: value``
#: pairs (extension point); the parser keeps the whole bracketed
#: payload + task body together when rendering into the slot.
_ONBOARDING_SEED_RE = re.compile(
    r"^\*\s+\[seed;\s*id:\s*\S+[^\]]*\]\s*$",
)


def _extract_seed_tasks(preset_text: str) -> list[str]:
    """Extract seed-task entries from a preset onboarding file.

    Each seed task is a multi-line markdown list item:

        * [seed; id: read-lifecycle-doctrine]
          Read `doctrine/lifecycle.md` ...

    Returns the rendered list-item blocks (each block preserving the
    `[seed; ...]` header line + any indented continuation lines until
    the next top-level item or non-indented blank line).  Deferred
    tasks (``[trigger: ...]``) and non-task content (prose, doctrine
    headers, metadata blocks) are excluded by construction.
    """
    blocks: list[str] = []
    current: list[str] = []
    in_seed = False
    for line in preset_text.splitlines():
        if _ONBOARDING_SEED_RE.match(line):
            if current:
                blocks.append("\n".join(current).rstrip())
                current = []
            current.append(line)
            in_seed = True
            continue
        if not in_seed:
            continue
        # Continuation if indented (>= 2 spaces); otherwise close the
        # current seed block on first non-indented non-empty line.
        if line.startswith("  ") or line.startswith("\t"):
            current.append(line)
        elif line.strip() == "":
            current.append(line)
        else:
            blocks.append("\n".join(current).rstrip())
            current = []
            in_seed = False
    if current:
        blocks.append("\n".join(current).rstrip())
    return blocks


def _render_onboarding_slot(preset_name: str, seed_blocks: list[str]) -> str:
    """Build the slot content for ``dev/PLANNING.md``'s
    ``onboarding-tasks`` slot from the preset name + extracted seeds.

    The first line is the ``<!-- preset: <name> -->`` metadata
    comment the goodnight activation helper reads to resolve which
    installed source file
    (``<target>/dev/modules/onboarding/<name>.md``) carries the
    deferred tasks (Codex P2-4 disposition: the metadata-comment
    contract is established here at scaffold time so the helper's
    contract is uniform).
    """
    parts = [f"<!-- preset: {preset_name} -->", ""]
    parts.extend(seed_blocks)
    return "\n".join(parts).rstrip() + "\n"


def _substitute_slot(
    text: str, slot_name: str, replacement: str,
) -> tuple[str, bool]:
    """Replace the body BETWEEN ``<!-- cairn:slot NAME -->`` and
    ``<!-- cairn:end NAME -->`` markers with *replacement*.

    Returns ``(new_text, did_substitute)``.  If the slot is not
    found, returns ``(text, False)`` so the caller can warn.
    """
    open_marker = f"<!-- cairn:slot {slot_name} -->"
    close_marker = f"<!-- cairn:end {slot_name} -->"
    o = text.find(open_marker)
    if o < 0:
        return text, False
    c = text.find(close_marker, o + len(open_marker))
    if c < 0:
        return text, False
    body_start = o + len(open_marker)
    new_body = "\n" + replacement.strip("\n") + "\n"
    return text[:body_start] + new_body + text[c:], True


#: The activation helper script Cairn ships to every adopter (Chunk
#: P1.2 -- ALWAYS installed alongside any progressive-onboarding
#: deployment).  The source lives under templates/modules/default-on/
#: parallel to the foldback_suggest.py + claim_check.py precedent;
#: the destination is the adopter's scripts/ tree, invoked at
#: goodnight per doctrine/onboarding.md.
_ONBOARDING_HELPER_SRC_REL = "modules/default-on/onboarding_activate.py"
_ONBOARDING_HELPER_DST_REL = "scripts/onboarding_activate.py"

#: The activation log path the helper appends to (Chunk P1.2 per
#: Codex P2-5: tracked, parallel to dev/intents.jsonl).
_ONBOARDING_LOG_REL = "dev/.cairn/onboarding-activated.jsonl"

#: The header comment the scaffold writes into a freshly-seeded
#: activation log so a cold reader knows what it is + the schema.
_ONBOARDING_LOG_HEADER = (
    "# dev/.cairn/onboarding-activated.jsonl -- progressive-onboarding\n"
    "# activation log; one JSONL line per activation; append-only.\n"
    "# Schema: {task-id, activated-at, by-agent, source-preset, trigger}.\n"
    "# Managed by scripts/onboarding_activate.py at goodnight;\n"
    "# see doctrine/onboarding.md for the mechanism.\n"
)


def install_onboarding(
    templates_root: Path,
    target: Path,
    preset_name: str | None,
    *,
    dry_run: bool = False,
    force: bool = False,
) -> list[InstallResult]:
    """Install the progressive-onboarding artifacts (Chunk P1.1 +
    P1.2).

    Three categories of writes:

    **Always (regardless of preset selection)** -- per Chunk P1.2:

    A. Install the activation helper script to
       ``<target>/scripts/onboarding_activate.py`` (verbatim copy).
    B. Seed an empty activation log at
       ``<target>/dev/.cairn/onboarding-activated.jsonl`` (header-
       comment-only; the helper appends to it at goodnight).

    **Only when a named preset is selected** -- per Chunk P1.1:

    C. Inline seed tasks + the ``<!-- preset: <name> -->`` metadata
       comment into ``dev/PLANNING.md``'s ``onboarding-tasks`` slot.
       ONLY ``[seed; id: ...]`` items render into the slot; deferred
       tasks (``[trigger: X; id: ...]``) stay in the installed source
       file (write D).
    D. Copy the full preset source file
       ``templates/onboarding/<name>.md`` to
       ``<target>/dev/modules/onboarding/<name>.md`` byte-for-byte.
       This is the authoritative reference the goodnight activation
       helper reads to discover deferred tasks (Codex External
       Review P1-1).

    Returns the list of InstallResults for each write (the
    always-writes always present; the preset-conditional writes only
    when ``preset_name`` is one of the three named presets).

    Per plan 2026-05-28-claude-cairn-progressive-onboarding Chunks
    P1.1 (slot subst + preset source copy) + P1.2 (helper script
    install + activation log seed) + Codex External Review P1-1 /
    P2-4 / P2-5 dispositions.
    """
    results: list[InstallResult] = []

    # ----- Always: install the activation helper script (A) -------------
    helper_src = templates_root / _ONBOARDING_HELPER_SRC_REL
    helper_dst = target / _ONBOARDING_HELPER_DST_REL
    if helper_src.exists():
        if dry_run:
            results.append((helper_dst, [], [], "dry-run"))
        elif helper_dst.exists() and not force:
            print(
                f"  [skip] {helper_dst}: already exists -- pass --force "
                f"to overwrite",
                file=sys.stderr,
            )
            results.append((helper_dst, [], [], "skipped-exists"))
        else:
            _assert_safe_write(helper_dst, target)
            helper_dst.parent.mkdir(parents=True, exist_ok=True)
            helper_dst.write_bytes(helper_src.read_bytes())
            results.append((helper_dst, [], [], "installed"))
    else:
        print(
            f"  [warn] onboarding helper source missing: "
            f"templates/{_ONBOARDING_HELPER_SRC_REL}",
            file=sys.stderr,
        )

    # ----- Always: seed an empty activation log (B) ---------------------
    log_dst = target / _ONBOARDING_LOG_REL
    if dry_run:
        results.append((log_dst, [], [], "dry-run"))
    elif log_dst.exists() and not force:
        print(
            f"  [skip] {log_dst}: already exists -- pass --force to "
            f"overwrite",
            file=sys.stderr,
        )
        results.append((log_dst, [], [], "skipped-exists"))
    else:
        _assert_safe_write(log_dst, target)
        log_dst.parent.mkdir(parents=True, exist_ok=True)
        log_dst.write_text(_ONBOARDING_LOG_HEADER, encoding="utf-8")
        results.append((log_dst, [], [], "installed"))

    # ----- Preset-conditional: slot subst + source copy (C + D) ---------
    if not preset_name or preset_name not in _ONBOARDING_PRESETS:
        return results

    src = templates_root / "onboarding" / f"{preset_name}.md"
    if not src.exists():
        print(
            f"  [warn] onboarding preset source missing: "
            f"templates/onboarding/{preset_name}.md",
            file=sys.stderr,
        )
        return results

    preset_text = src.read_text(encoding="utf-8")
    seed_blocks = _extract_seed_tasks(preset_text)
    rendered = _render_onboarding_slot(preset_name, seed_blocks)

    # Write C: substitute into installed PLANNING.md's slot.
    planning_dst = target / "dev" / "PLANNING.md"
    if not planning_dst.exists():
        print(
            f"  [warn] onboarding: dev/PLANNING.md not yet installed -- "
            f"slot substitution skipped (run after install_core)",
            file=sys.stderr,
        )
    else:
        planning_text = planning_dst.read_text(encoding="utf-8")
        new_text, ok = _substitute_slot(
            planning_text, "onboarding-tasks", rendered,
        )
        if not ok:
            print(
                f"  [warn] onboarding: `onboarding-tasks` slot not found "
                f"in dev/PLANNING.md -- preset content not injected",
                file=sys.stderr,
            )
        elif new_text != planning_text:
            if dry_run:
                results.append((planning_dst, [], [], "dry-run"))
            else:
                _assert_safe_write(planning_dst, target)
                planning_dst.write_text(new_text, encoding="utf-8")
                results.append((planning_dst, [], [], "installed"))

    # Write D: copy source file verbatim to installed-source path.
    source_dst = target / "dev" / "modules" / "onboarding" / f"{preset_name}.md"
    if dry_run:
        results.append((source_dst, [], [], "dry-run"))
    else:
        if source_dst.exists() and not force:
            print(
                f"  [skip] {source_dst}: already exists -- pass --force to "
                f"overwrite",
                file=sys.stderr,
            )
            results.append((source_dst, [], [], "skipped-exists"))
        else:
            _assert_safe_write(source_dst, target)
            source_dst.parent.mkdir(parents=True, exist_ok=True)
            source_dst.write_text(preset_text, encoding="utf-8")
            results.append((source_dst, [], [], "installed"))

    return results


def install_modules(
    templates_root: Path,
    target: Path,
    tokens: dict[str, str],
    module_names: list[str],
    *,
    dry_run: bool = False,
    force: bool = False,
) -> list[InstallResult]:
    """Copy selected module templates into *target*.

    Module source paths in ``_MODULE_MAPPINGS`` are relative to
    ``templates_root / "modules"`` (i.e. ``cairn/templates/modules/``).
    """
    modules_root = templates_root / "modules"
    results: list[InstallResult] = []
    known = set(_MODULE_MAPPINGS)
    for name in module_names:
        if name not in known:
            print(
                f"  [warn] unknown module '{name}' — skipped. "
                f"Known modules: {', '.join(sorted(known))}",
                file=sys.stderr,
            )
            continue
        # 1:many -- a module installs its doctrine .md and (for the two
        # default-on discipline modules) its reference script verbatim.
        for spec in _MODULE_MAPPINGS[name]:
            src = modules_root / spec.src
            if not src.exists():
                print(
                    f"  [warn] module template missing: {spec.src}",
                    file=sys.stderr,
                )
                continue
            dst = target / spec.dst
            results.append(
                _install_one(
                    src, dst, tokens, target,
                    dry_run=dry_run, force=force, verbatim=spec.verbatim,
                )
            )
    return results


#: Forge name -> adopter-root reference directory (fold-back #38).  The
#: issue-capture module ships starter issue templates + a labels.yml per
#: forge under reference/<dir>/; when a forge is named in the profile and
#: issue-capture installs, that dir is copied into the adopter root.
_FORGE_REFERENCE_DIRS: dict[str, str] = {"gitlab": ".gitlab", "github": ".github"}


def install_issue_capture_reference(
    templates_root: Path,
    target: Path,
    forge: str,
    *,
    dry_run: bool = False,
    force: bool = False,
) -> list[InstallResult]:
    """Copy the issue-capture forge reference starter into *target*.

    For ``forge`` in ``_FORGE_REFERENCE_DIRS`` (gitlab/github), copies every
    file under ``templates/modules/team-gated/issue-capture/reference/<dir>/``
    to the matching adopter-root path (``.gitlab/...`` / ``.github/...``),
    verbatim (starter content; no token substitution).  Non-clobber:
    ``_install_one`` skips an existing file unless ``force`` -- so a
    Maintainer's customized templates survive a re-scaffold.  Fold-back #38.
    """
    forge_dir = _FORGE_REFERENCE_DIRS[forge]
    ref_root = (
        templates_root / "modules" / "team-gated"
        / "issue-capture" / "reference" / forge_dir
    )
    results: list[InstallResult] = []
    if not ref_root.is_dir():
        print(
            f"  [warn] issue-capture reference missing: {ref_root}",
            file=sys.stderr,
        )
        return results
    for src in sorted(p for p in ref_root.rglob("*") if p.is_file()):
        rel = src.relative_to(ref_root)
        dst = target / forge_dir / rel
        results.append(
            _install_one(
                src, dst, {}, target,
                dry_run=dry_run, force=force, verbatim=True,
            )
        )
    return results


# ---------------------------------------------------------------------------
# Post-scaffold report
# ---------------------------------------------------------------------------

def print_report(
    target: Path,
    dirs_created: list[Path],
    installed: list[InstallResult],
) -> None:
    """Print a human-readable post-scaffold report to stdout."""
    print()
    print("=" * 68)
    print("  Cairn scaffold complete")
    print("=" * 68)
    print(f"\nTarget repository : {target}")
    print(f"Directories created ({len(dirs_created)}):")
    for d in dirs_created:
        print(f"  {d.relative_to(target)}/")

    written = [r for r in installed if r[3] == "installed"]
    skipped = [r for r in installed if r[3] == "skipped-exists"]
    dry = [r for r in installed if r[3] == "dry-run"]

    if dry:
        print(f"\n[dry-run] Files that would be installed ({len(dry)}):")
        for dst, _u, _s, _st in dry:
            print(f"  {dst.relative_to(target)}")
    else:
        print(f"\nFiles installed ({len(written)}):")
        for dst, _u, _s, _st in written:
            print(f"  {dst.relative_to(target)}")
        if skipped:
            print(
                f"\nFiles skipped -- already exist, --force not set "
                f"({len(skipped)}):"
            )
            for dst, _u, _s, _st in skipped:
                print(f"  {dst.relative_to(target)}")
            print(
                "  -> These files already exist in the target.  The scaffold "
                "preserved their contents by default to protect filled\n"
                "     block slots and other customizations.  Pass --force to "
                "overwrite (back up first if you have customizations\n"
                "     you want to keep)."
            )

    # Unfilled inline tokens (only count files we actually wrote or
    # would write; skipped files keep their on-disk content untouched)
    accounted = written or dry
    all_unfilled = sorted(
        {tok for _d, unfilled, _s, _st in accounted for tok in unfilled}
    )
    if all_unfilled:
        print(f"\n[WARN] {len(all_unfilled)} unfilled token(s) remain:")
        for tok in all_unfilled:
            print(f"  {{{{ {tok} }}}}")
        print("  -> Add these to the profile config and re-run, or fill manually.")
    elif accounted:
        print("\n[OK] All inline tokens substituted.")

    # Block slots needing agent attention (only for written/dry files)
    all_slots = [
        (dst.relative_to(target), slot)
        for dst, _u, slots, _st in accounted
        for slot in slots
    ]
    if all_slots:
        print(f"\nBlock slots requiring agent attention ({len(all_slots)}):")
        for path, slot in all_slots:
            print(f"  {path}  [cairn:slot {slot}]")
        print("  -> See BOOTSTRAP.md Act II-4 for guidance.")
    else:
        print("\n[OK] No block slots detected.")

    print()
    print("Next steps (BOOTSTRAP.md Act II):")
    print("  3. Confirm the installed files match the accepted profile (II-3).")
    print("  4. Fill all block slots (II-4).")
    print("  5. Run the R-F acceptance gate (II-5).")
    print("  6. Dogfood one change through the lifecycle (II-6).")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def install_manifest(
    modules: list[str] | None = None,
) -> list[tuple[str, str, bool]]:
    """The ``(source, destination, verbatim)`` set the scaffold installs.

    Core templates always; modules per *modules* (or **all** known
    modules when ``None`` -- the published catalog).  ``source`` is
    relative to ``templates/``; ``destination`` is relative to the
    target repo root.  Derived from ``_CORE_MAPPINGS`` +
    ``_MODULE_MAPPINGS`` so the published manifest (Layer 1) cannot
    drift from what the scaffold actually writes.  Sorted by
    destination for a stable, diffable emission.
    """
    entries: list[tuple[str, str, bool]] = [
        (src_rel, dst_rel, False) for src_rel, dst_rel in _CORE_MAPPINGS
    ]
    names = sorted(_MODULE_MAPPINGS) if modules is None else modules
    for name in names:
        for spec in _MODULE_MAPPINGS.get(name, []):
            entries.append((f"modules/{spec.src}", spec.dst, spec.verbatim))
    entries.sort(key=lambda e: (e[1], e[0]))
    return entries


def format_manifest(modules: list[str] | None = None) -> str:
    """Render the install manifest as a stable, machine-readable table:
    one ``destination<TAB>source<TAB>{verbatim|substituted}`` line per
    file (Layer 1; ``scaffold.py --manifest``)."""
    lines = [
        "# Cairn install manifest "
        "(destination<TAB>source<TAB>verbatim|substituted)",
    ]
    for src, dst, verbatim in install_manifest(modules):
        kind = "verbatim" if verbatim else "substituted"
        lines.append(f"{dst}\t{src}\t{kind}")
    return "\n".join(lines) + "\n"


def git_provenance_warning(cairn_root: Path) -> str | None:
    """Layer-1 provenance nudge: return a warning when *cairn_root* is a
    git checkout whose ``HEAD`` is **not a tagged release commit** or has
    **uncommitted changes**; return ``None`` when it is a clean tagged
    release, or when git is unavailable / the path is not a checkout
    (degrade silently -- the warning never blocks an install).

    Read-only, fixed-argument ``git`` via ``subprocess`` (no shell, no
    input interpolation).  ``git`` is local VCS, not a network call, so
    SAFETY Rule 5 (the bootstrap does not read from the internet) is
    untouched.
    """
    import subprocess

    def _git(*args: str) -> subprocess.CompletedProcess[str] | None:
        try:
            return subprocess.run(
                ["git", "-C", str(cairn_root), *args],
                capture_output=True, text=True, timeout=10, check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return None

    inside = _git("rev-parse", "--is-inside-work-tree")
    if inside is None or inside.returncode != 0 \
            or inside.stdout.strip() != "true":
        return None  # not a checkout / git absent -- silent

    issues: list[str] = []
    tagged = _git("describe", "--exact-match", "--tags", "HEAD")
    if tagged is None or tagged.returncode != 0:
        issues.append("its HEAD is not a tagged release commit")
    dirty = _git("status", "--porcelain")
    if dirty is not None and dirty.stdout.strip():
        issues.append("its source tree has uncommitted changes")
    if not issues:
        return None
    return (
        f"provenance: scaffolding from a Cairn source where "
        f"{' and '.join(issues)} ({cairn_root}). Prefer a tagged release "
        f"(see bootstrap/PROVENANCE.md); pass --allow-dev to silence."
    )


def _find_cairn_root(script_path: Path) -> Path:
    """Locate the Cairn repo root as two directories above this script.

    ``bootstrap/scaffold.py`` → ``bootstrap/`` → ``<cairn root>``.
    """
    return script_path.resolve().parent.parent


# ---------------------------------------------------------------------------
# Upgrade capability -- install lockfile + scoped base-template cache
# ---------------------------------------------------------------------------
#
# The install-side ancestor anchor for ``scaffold.py upgrade`` (the
# token- + slot-aware 3-way merge).  See ``bootstrap/UPGRADE.md`` and the
# the source ``cairn-module-upgrade-3way-merge`` plan.
#
#   * ``dev/cairn-lock.yml`` -- a *visible*, *tracked* machine lockfile
#     (R2): the upgrade ancestor + the install-side provenance record.
#   * ``dev/.cairn/base/`` -- a *tracked* cache of the **raw** upstream
#     templates for the mergeable ``.md`` installs (R1/I4): so the merge's
#     ``base`` is on disk under any distribution mode (no Cairn git history
#     needed) and only the mergeable set is shadow-copied.

_LOCKFILE_REL = "dev/cairn-lock.yml"        # visible + tracked (R2)
_BASE_CACHE_REL = "dev/.cairn/base"         # tracked raw-template cache (R1/I4)
_LOCK_SCHEMA = 1

#: Token names that must never be recorded in the lockfile (R9): a
#: substitution token bearing a secret would leak it into a tracked file.
#: Matched as a **substring anywhere** in the token name (case-insensitive)
#: so camelCase / flatcase keys are caught too -- `apiKey`, `secretToken`,
#: `dbPassword`, `mysecret`, `passwdstr` all match, not only snake_case.
#: The allow-list makes false positives cheap; a silent secret leak is not.
_SECRET_TOKEN_RE = re.compile(
    r"password|passwd|secret|credential|token|key", re.IGNORECASE,
)


def _sha256_hex(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def _cairn_version(cairn_root: Path) -> str:
    """Read the Cairn version from ``CITATION.cff`` (``unknown`` if absent)."""
    cff = cairn_root / "CITATION.cff"
    if cff.exists():
        for line in cff.read_text(encoding="utf-8").splitlines():
            m = re.match(r'\s*version\s*:\s*"?([^"\s]+)"?\s*$', line)
            if m:
                return m.group(1)
    return "unknown"


def _cairn_commit(cairn_root: Path) -> str:
    """Short HEAD commit of the Cairn source, or ``unknown`` (no git)."""
    import subprocess
    try:
        r = subprocess.run(
            ["git", "-C", str(cairn_root), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return r.stdout.strip() if r.returncode == 0 else "unknown"


def _refuse_secret_tokens(
    tokens: dict[str, str], allow: tuple[str, ...] = (),
) -> None:
    """Raise PresetError if any token name looks secret-bearing (R9)."""
    allowed = {a.lower() for a in allow}
    offending = sorted(
        name for name in tokens
        if _SECRET_TOKEN_RE.search(name) and name.lower() not in allowed
    )
    if offending:
        raise PresetError(
            "refusing to record secret-like token name(s) in the lockfile: "
            + ", ".join(offending)
            + " -- Cairn templates must not introduce secret-bearing "
            "substitution tokens (bootstrap/SAFETY.md). If a token is "
            "genuinely public, add it to the writer's allow-list."
        )


def _emit_lock_yaml(data: dict[str, Any]) -> str:
    """Serialize the lockfile as deterministic JSON (valid YAML 1.2) so it
    round-trips **stdlib-only** (no PyYAML dependency) while staying a
    parseable ``.yml``.  Tool-owned: regenerate-only, do not hand-edit."""
    import json
    header = (
        "# cairn-lock.yml -- machine-generated install lockfile "
        "(tool-owned; regenerate-only; do not hand-edit).\n"
        "# JSON-encoded (valid YAML 1.2) so it round-trips without a YAML "
        "dependency.\n"
    )
    return header + json.dumps(data, indent=2, sort_keys=True) + "\n"


def read_lockfile(target: Path) -> dict[str, Any] | None:
    """Read ``<target>/dev/cairn-lock.yml`` (or None if absent/unparseable).

    Strips ``#`` comment lines, then parses the JSON body (the format
    :func:`_emit_lock_yaml` writes)."""
    import json
    p = target / _LOCKFILE_REL
    if not p.exists():
        return None
    body = "\n".join(
        ln for ln in p.read_text(encoding="utf-8").splitlines()
        if not ln.lstrip().startswith("#")
    )
    try:
        data = json.loads(body)
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def _lock_file_list(
    modules: list[str], optional: list[tuple[str, str]],
) -> list[tuple[str, str, bool]]:
    """The ``(src-rel-to-templates/, dst, verbatim)`` set a lockfile tracks:
    core + selected modules (via :func:`install_manifest`) + optional
    templates.  De-duplicated by destination, stable order."""
    entries = list(install_manifest(modules))
    for src_rel, dst_rel in optional:
        entries.append((src_rel, dst_rel, False))
    seen: set[str] = set()
    out: list[tuple[str, str, bool]] = []
    for src, dst, verbatim in entries:
        if dst in seen:
            continue
        seen.add(dst)
        out.append((src, dst, verbatim))
    return out


def write_install_lockfile(
    target: Path,
    cairn_root: Path,
    templates_root: Path,
    *,
    tokens: dict[str, str],
    modules: list[str],
    optional: list[tuple[str, str]],
    profile: dict[str, Any],
    allow_secret_tokens: tuple[str, ...] = (),
    onboarding_preset: str | None = None,
) -> dict[str, Any] | None:
    """Write ``dev/cairn-lock.yml`` + the scoped base-template cache.

    **Fail-closed (P-1)**: a lockfile must record a *clean* ancestor, so
    this refuses (returns ``None``, prints guidance) if any tracked file on
    disk differs from a clean install -- e.g. a ``skipped-exists`` file the
    adopter customized.  On a fresh install every file matches, so the
    lockfile + cache are written.  Token-secret guard runs first (R9).

    The base cache stores the **raw** (pre-substitution) template for each
    **non-verbatim** install only (I4: verbatim scripts use the hash policy,
    not a cached base).

    ``onboarding_preset`` (per plan 2026-05-28-claude-cairn-progressive-
    onboarding Chunk P1.1): when set, the lockfile's "clean install"
    computation for ``dev/PLANNING.md`` includes the post-install
    onboarding-slot substitution + preset metadata write, so the file's
    on-disk content matches the expected ``would`` despite
    ``install_onboarding`` having modified it after ``install_core``.
    """
    _refuse_secret_tokens(tokens, allow_secret_tokens)

    file_records: list[dict[str, Any]] = []
    cache_writes: list[tuple[Path, str]] = []
    diverged: list[str] = []

    # Pre-compute the onboarding overlay for PLANNING.md so the
    # `would` calculation in the loop below can apply the same slot
    # substitution `install_onboarding` did at install time.  If no
    # preset is selected, the overlay is empty and PLANNING.md is
    # checked against the token-substituted raw template (the
    # baseline behavior).
    onboarding_overlay: str | None = None
    if (
        onboarding_preset
        and onboarding_preset in _ONBOARDING_PRESETS
    ):
        preset_src = (
            templates_root / "onboarding" / f"{onboarding_preset}.md"
        )
        if preset_src.exists():
            seed_blocks = _extract_seed_tasks(
                preset_src.read_text(encoding="utf-8")
            )
            onboarding_overlay = _render_onboarding_slot(
                onboarding_preset, seed_blocks,
            )

    for src_rel, dst_rel, verbatim in _lock_file_list(modules, optional):
        src = templates_root / src_rel
        if not src.exists():
            continue
        raw = src.read_text(encoding="utf-8")
        if verbatim:
            would = src.read_bytes()
        else:
            substituted = substitute_tokens(raw, tokens)
            if (
                dst_rel == "dev/PLANNING.md"
                and onboarding_overlay is not None
            ):
                # Apply the same slot substitution `install_onboarding`
                # did so the lockfile sees a clean install.
                with_overlay, ok = _substitute_slot(
                    substituted, "onboarding-tasks", onboarding_overlay,
                )
                substituted = with_overlay if ok else substituted
            would = substituted.encode("utf-8")
        dst_abs = target / dst_rel
        on_disk = dst_abs.read_bytes() if dst_abs.exists() else None
        if on_disk is None or on_disk != would:
            diverged.append(dst_rel)
            continue
        rec: dict[str, Any] = {
            "src": src_rel, "dst": dst_rel, "verbatim": verbatim,
            "hash": "sha256:" + _sha256_hex(would),
        }
        if not verbatim:
            cache_rel = f"{_BASE_CACHE_REL}/{dst_rel}"
            rec["base_cache"] = cache_rel
            rec["base_hash"] = "sha256:" + _sha256_hex(raw.encode("utf-8"))
            cache_writes.append((target / cache_rel, raw))
        file_records.append(rec)

    if diverged:
        shown = ", ".join(diverged[:5]) + ("..." if len(diverged) > 5 else "")
        print(
            f"  [warn] {_LOCKFILE_REL} NOT written: {len(diverged)} installed "
            f"file(s) differ from a clean install ({shown}). A lockfile must "
            "record a clean ancestor; run `python bootstrap/scaffold.py "
            "upgrade --init-lock --target <repo>` to synthesize one from the "
            "current tree instead.",
            file=sys.stderr,
        )
        return None

    lock: dict[str, Any] = {
        "schema": _LOCK_SCHEMA,
        "cairn_version": _cairn_version(cairn_root),
        "cairn_commit": _cairn_commit(cairn_root),
        "profile": profile,
        "modules": sorted(modules),
        "optional_templates": sorted(dst for _, dst in optional),
        "tokens": dict(tokens),
        "files": file_records,
    }
    for cache_path, raw in cache_writes:
        _assert_safe_write(cache_path, target)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(raw, encoding="utf-8")
    lock_path = target / _LOCKFILE_REL
    _assert_safe_write(lock_path, target)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(_emit_lock_yaml(lock), encoding="utf-8")
    return lock


# ---------------------------------------------------------------------------
# Fail-closed slot parsing (R8) -- the merge engine relies on slots being
# well-formed before it transplants adopter-owned bodies.  Stricter than the
# set-level ``find_unpaired_slots`` (which only computes open ^ close and is
# blind to ordering / nesting / duplicates).
# ---------------------------------------------------------------------------

class SlotError(ValueError):
    """Raised on a malformed ``cairn:slot`` structure (R8, fail-closed)."""


class Slot(NamedTuple):
    """A parsed, marker-anchored slot region (line indices, 0-based)."""

    name: str
    open_line: int   # index of the `cairn:slot NAME` marker line
    close_line: int  # index of the `cairn:end NAME` marker line
    body: str        # text strictly between the markers (exclusive)


def parse_slots(text: str) -> list[Slot]:
    """Strictly parse ``cairn:slot`` / ``cairn:end`` regions; **fail closed**.

    Raises :class:`SlotError` on any malformation a merge must not silently
    mis-handle (R8): a **nested** opener (a second slot opened before the
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
# The token- + slot-aware 3-way merge engine (R4)
# ---------------------------------------------------------------------------

class MergeResult(NamedTuple):
    """Outcome of merging one substituted ``.md`` file."""

    status: str          # "clean" | "conflict" | "slot-removed" | "error"
    merged: str          # merged text (with conflict markers if conflicted)
    detail: str          # human-readable note (needs-value tokens, etc.)


def _transplant_slots(target_text: str, ours_text: str) -> str:
    """Return *target_text* with each slot also present in *ours_text*
    replaced by **ours' exact slot lines** (R4 slot-transplant).  Slots in
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
        return target_text  # caller validates ours separately (R8)
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
    * **Slot-transplant (R4)**: ``ours``' slot bodies are copied into the
      same-named slots of ``base`` and ``theirs`` so all three inputs are
      identical inside slots -> ``git merge-file`` produces zero
      changes/conflicts there while the surrounding prose merges.
    * A slot **removed** upstream whose ``ours`` body is non-empty is a
      **fail-closed** flagged decision (status ``slot-removed``) -- the
      adopter's filled content would otherwise be orphaned.

    ``ours`` is parsed strictly (R8); a malformed ``ours`` raises
    :class:`SlotError` to the caller (never silently mis-merged).
    """
    base = substitute_tokens(base_raw, tokens)
    theirs = substitute_tokens(theirs_raw, tokens)

    # New upstream tokens with no recorded value remain as {{token}}.
    needs_value = sorted(set(find_unfilled_tokens(theirs)))

    our_slots = parse_slots(ours)              # strict (R8); may raise
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


# ---------------------------------------------------------------------------
# Verbatim-script hash policy (Part 4) -- hash check, never a text merge
# ---------------------------------------------------------------------------

def classify_verbatim(
    ours_bytes: bytes | None, lock_hash: str, theirs_bytes: bytes,
) -> str:
    """Classify a verbatim script for upgrade (no text merge, hash only).

    Returns: ``"missing"`` (not on disk); ``"locally-modified"`` (on-disk
    hash != the lockfile's recorded base hash -> flag, never clobber);
    ``"up-to-date"`` (already equals the new upstream); or ``"update"``
    (unmodified vs base and differs from upstream -> safe to update).
    """
    if ours_bytes is None:
        return "missing"
    ours_h = "sha256:" + _sha256_hex(ours_bytes)
    if ours_h != lock_hash:
        return "locally-modified"
    if ours_bytes == theirs_bytes:
        return "up-to-date"
    return "update"


# ---------------------------------------------------------------------------
# The `upgrade` subcommand (Chunk 5/6): --plan / --stage / --apply / --init-lock
# ---------------------------------------------------------------------------

_STAGING_REL = "dev/.cairn-upgrade"          # ephemeral, gitignored (R3)
_STAGE_META = "stage-metadata.json"
_CONFLICT_MARKER = "<<<<<<< ours"


def _cairn_is_git(cairn_root: Path) -> bool:
    import subprocess
    try:
        r = subprocess.run(
            ["git", "-C", str(cairn_root), "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return r.returncode == 0 and r.stdout.strip() == "true"


def _theirs_text(
    cairn_root: Path, templates_root: Path, src_rel: str, to_ref: str | None,
) -> str | None:
    """The upstream template for *src_rel* at the target version: the
    currently-running tree (``to_ref is None``) or, **git-checkout-only**
    (P-4), ``git show <to_ref>:templates/<src_rel>``.  None if absent."""
    if to_ref is None:
        p = templates_root / src_rel
        return p.read_text(encoding="utf-8") if p.exists() else None
    import subprocess
    try:
        r = subprocess.run(
            ["git", "-C", str(cairn_root), "show",
             f"{to_ref}:templates/{src_rel}"],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout if r.returncode == 0 else None


def _theirs_bytes(
    cairn_root: Path, templates_root: Path, src_rel: str, to_ref: str | None,
) -> bytes | None:
    if to_ref is None:
        p = templates_root / src_rel
        return p.read_bytes() if p.exists() else None
    text = _theirs_text(cairn_root, templates_root, src_rel, to_ref)
    return text.encode("utf-8") if text is not None else None


#: Kinds that may be staged + applied (they advance the machine
#: authority).  Every other kind is report-only and is NEVER staged, so it
#: can never be applied: slot-removed, error,
#: review-only, needs-value, removed-upstream, verbatim-locally-modified,
#: verbatim-missing, verbatim-up-to-date, up-to-date.
#:
#: ``clean-locally-modified`` is the B-C-1 sub-classification of a clean
#: 3-way merge result: the adopter had customized the file locally
#: (``ours != base``) and the customization merged cleanly with the new
#: upstream.  Advances identically to ``clean``; reported separately so
#: the adopter sees their customizations were preserved across the merge
#: (vs. ``clean`` which means the file was untouched).
_ADVANCING_KINDS = frozenset(
    {"clean", "clean-locally-modified", "conflict", "verbatim-update"}
)

#: Display labels for the upgrade report.  Maps the internal kind to the
#: adopter-facing label; kinds not in this map render verbatim.
_KIND_DISPLAY_LABEL = {
    "clean": "clean (untouched)",
    "clean-locally-modified": "locally-modified (merged clean)",
}


class FilePlan(NamedTuple):
    dst: str
    kind: str
    applied: str | None      # content written on --apply (advancing kinds); else None
    detail: str
    theirs_raw: str | None    # new upstream RAW template (mergeable) -> refreshed base cache
    base_cache: str | None    # lockfile base_cache rel path (mergeable) to refresh


def _compute_upgrade(
    target: Path, cairn_root: Path, templates_root: Path,
    lock: dict[str, Any], to_ref: str | None,
) -> tuple[list[FilePlan], dict[str, Any]]:
    """Classify every lockfile-tracked file for upgrade + the structural
    drift.  Pure read-only -- no writes."""
    tokens = {str(k): str(v) for k, v in (lock.get("tokens") or {}).items()}
    plans: list[FilePlan] = []
    for rec in lock.get("files", []):
        dst = rec["dst"]
        verbatim = bool(rec.get("verbatim"))
        src_rel = rec["src"]
        dst_abs = target / dst
        ours_bytes = dst_abs.read_bytes() if dst_abs.exists() else None
        theirs_b = _theirs_bytes(cairn_root, templates_root, src_rel, to_ref)
        if theirs_b is None:
            plans.append(FilePlan(dst, "removed-upstream", None,
                                  "no longer in upstream templates", None, None))
            continue
        if verbatim:
            kind = classify_verbatim(ours_bytes, rec.get("hash", ""), theirs_b)
            plans.append(FilePlan(
                dst, f"verbatim-{kind}",
                theirs_b.decode("utf-8", "replace") if kind == "update" else None,
                "", None, None))
            continue
        # Mergeable .md.
        if ours_bytes is None:
            plans.append(FilePlan(dst, "review-only", None,
                                  "file missing on disk", None, None))
            continue
        ours = ours_bytes.decode("utf-8")
        theirs_raw = theirs_b.decode("utf-8")
        cache_rel = rec.get("base_cache")
        base_path = (target / cache_rel) if cache_rel else None
        if base_path is None or not base_path.exists():
            # No recoverable base (e.g. a --init-lock migrated tree, I3) ->
            # review-only diff, never a pretended 3-way merge.
            plans.append(FilePlan(dst, "review-only", None,
                                  "no recoverable base (review-only diff)",
                                  None, None))
            continue
        base_raw = base_path.read_text(encoding="utf-8")
        try:
            res = merge_file(base_raw, theirs_raw, ours, tokens)
        except SlotError as exc:
            plans.append(FilePlan(dst, "error", None,
                                  f"malformed slots: {exc}", None, None))
            continue
        # B-C-1: split `clean` into `clean (untouched)` vs.
        # `locally-modified (merged clean)` so the adopter sees their
        # customizations were preserved across the merge.  When the
        # merge resolved cleanly AND the on-disk file differs from the
        # *token-substituted* base, the adopter had customized this
        # file beyond the install-time substitution, and those
        # customizations rode through the merge.  The substituted
        # comparison is critical -- a plain ``ours != base_raw`` check
        # would flag every normally-installed file (where ours has
        # ``Demo`` for ``{{project_name}}`` but base_raw still has the
        # token) as "locally modified," which is the wrong signal.
        kind = res.status
        if kind == "clean" and ours != substitute_tokens(base_raw, tokens):
            kind = "clean-locally-modified"
        advancing = kind in _ADVANCING_KINDS
        plans.append(FilePlan(
            dst, kind,
            res.merged if advancing else None, res.detail,
            theirs_raw if advancing else None,
            cache_rel if advancing else None))

    # Structural reconciliation.
    lock_modules = set(lock.get("modules", []))
    current_modules = set(_MODULE_MAPPINGS)
    structural = {
        "new_modules": sorted(current_modules - lock_modules),
        "removed_modules": sorted(lock_modules - current_modules),
    }
    return plans, structural


def _citation_ok(target: Path, lock: dict[str, Any]) -> bool | None:
    """R10: if the target carries a fidelity manifest, does it cite the
    current lockfile version/commit?  None if no manifest to check."""
    candidates = list((target / "dev" / "strategy").glob("*fidelity*"))
    candidates += list((target / "dev" / "strategy").glob("*manifest*"))
    manifest = next((c for c in candidates if c.is_file()), None)
    if manifest is None:
        return None
    text = manifest.read_text(encoding="utf-8", errors="replace")
    commit = str(lock.get("cairn_commit", ""))
    version = str(lock.get("cairn_version", ""))
    return (commit and commit in text) or (version and version in text)


def _print_upgrade_report(
    plans: list[FilePlan], structural: dict[str, Any],
    citation: bool | None, *, mode: str,
) -> None:
    import collections
    by_kind: dict[str, list[str]] = collections.defaultdict(list)
    for fp in plans:
        by_kind[fp.kind].append(fp.dst)
    print(f"\nCairn upgrade -- {mode}\n" + "=" * 40)
    order = ["clean", "clean-locally-modified",
             "conflict", "slot-removed", "review-only",
             "verbatim-update", "verbatim-locally-modified",
             "verbatim-up-to-date", "verbatim-missing", "up-to-date",
             "removed-upstream", "error"]
    # Column width sized for the longest display label ("locally-modified
    # (merged clean)" = 31 chars) plus a 2-space pad.
    label_width = max(len(_KIND_DISPLAY_LABEL.get(k, k)) for k in order) + 2
    for kind in order + [k for k in by_kind if k not in order]:
        if kind in by_kind:
            label = _KIND_DISPLAY_LABEL.get(kind, kind)
            print(f"  {label:{label_width}s} {len(by_kind[kind])}: "
                  f"{', '.join(by_kind[kind][:6])}"
                  f"{'...' if len(by_kind[kind]) > 6 else ''}")
    if structural["new_modules"]:
        print(f"\n  new modules available (opt-in): "
              f"{', '.join(structural['new_modules'])}")
    if structural["removed_modules"]:
        print(f"  modules removed upstream (flagged): "
              f"{', '.join(structural['removed_modules'])}")
    if citation is False:
        print("\n  [warn] the fidelity manifest does NOT cite the current "
              "lockfile version/commit (R10) -- update its citation.")
    conflicts = [fp.dst for fp in plans if fp.kind == "conflict"]
    flags = [fp for fp in plans if fp.kind in
             ("slot-removed", "verbatim-locally-modified", "error")]
    if conflicts:
        print(f"\n  {len(conflicts)} file(s) need conflict resolution before "
              "--apply.")
    for fp in flags:
        print(f"  [flag] {fp.dst}: {fp.detail}")


def _seed_staging_gitignore(target: Path) -> None:
    seed_gitignore(target, (_STAGING_REL + "/",))


def _write_stage(
    target: Path, plans: list[FilePlan], lock: dict[str, Any],
    to_ref: str | None, cairn_root: Path,
) -> Path:
    """Write the staged review surface into the ephemeral, gitignored
    staging dir; return its path.

    Stages **only advancing kinds** (clean / conflict / verbatim-update) --
    a flagged/non-advancing file is reported but never staged, so it can
    never be applied.  Also stages the **new
    base-template** for each advancing mergeable file (under ``new-base/``)
    + the new version/commit in metadata, so ``--apply`` can advance the
    lockfile + base cache without needing the Cairn source again."""
    import json
    import shutil
    stage = target / _STAGING_REL
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True, exist_ok=True)
    staged_files: list[str] = []
    ours_hashes: dict[str, str] = {}
    kinds: dict[str, str] = {}
    for fp in plans:
        if fp.kind not in _ADVANCING_KINDS or fp.applied is None:
            continue
        dst_abs = target / fp.dst
        # Skip a genuine no-op (the applied content already on disk).
        if dst_abs.exists() and \
                dst_abs.read_text(encoding="utf-8") == fp.applied:
            continue
        out = stage / "files" / fp.dst
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(fp.applied, encoding="utf-8")
        staged_files.append(fp.dst)
        kinds[fp.dst] = fp.kind
        # Snapshot the on-disk *ours* hash at stage time (R7a: detect an
        # adopter edit made between --stage and --apply).
        if dst_abs.exists():
            ours_hashes[fp.dst] = "sha256:" + _sha256_hex(dst_abs.read_bytes())
        # Stage the new base-template content (mergeable files only).
        if fp.theirs_raw is not None and fp.base_cache:
            nb = stage / "new-base" / fp.dst
            nb.parent.mkdir(parents=True, exist_ok=True)
            nb.write_text(fp.theirs_raw, encoding="utf-8")
    meta = {
        "lock_commit": lock.get("cairn_commit"),
        "lock_version": lock.get("cairn_version"),
        "to_ref": to_ref,
        "tokens": lock.get("tokens"),
        "modules": lock.get("modules"),
        "new_version": _cairn_version(cairn_root),
        "new_commit": to_ref or _cairn_commit(cairn_root),
        "staged_files": sorted(staged_files),
        "kinds": kinds,
        "ours_hashes": ours_hashes,
    }
    (stage / _STAGE_META).write_text(
        json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")
    _seed_staging_gitignore(target)
    return stage


def _cmd_init_lock(
    target: Path, cairn_root: Path, templates_root: Path,
) -> int:
    """`upgrade --init-lock` (R6/I3): synthesize a lockfile for a
    pre-lockfile tree from on-disk content + the fidelity manifest.

    Token-substituted files have **no recoverable token values** (the
    manifest records names, not values, I3) -> classified
    *unrecoverable-base* and handled review-only on later upgrades, never a
    pretended 3-way merge.  Verbatim scripts record their on-disk hash."""
    if read_lockfile(target) is not None:
        print(f"  [info] {_LOCKFILE_REL} already exists; nothing to migrate.",
              file=sys.stderr)
        return 0
    # Best-effort cairn_commit from a fidelity manifest, if present.
    commit = "unknown"
    for c in list((target / "dev" / "strategy").glob("*")):
        if c.is_file():
            for line in c.read_text(encoding="utf-8", errors="replace").splitlines():
                m = re.match(r'\s*cairn_commit\s*:\s*"?([0-9a-f]{7,40})"?', line)
                if m:
                    commit = m.group(1)
                    break
    records: list[dict[str, Any]] = []
    classification: dict[str, list[str]] = {"verbatim": [], "unrecoverable-base": []}
    for src_rel, dst_rel, verbatim in _lock_file_list(list(_MODULE_MAPPINGS), []):
        dst_abs = target / dst_rel
        if not dst_abs.exists():
            continue
        h = "sha256:" + _sha256_hex(dst_abs.read_bytes())
        rec: dict[str, Any] = {"src": src_rel, "dst": dst_rel,
                               "verbatim": verbatim, "hash": h}
        if verbatim:
            classification["verbatim"].append(dst_rel)
        else:
            # No token values -> base not reconstructable (I3); no base_cache.
            rec["unrecoverable_base"] = True
            classification["unrecoverable-base"].append(dst_rel)
        records.append(rec)
    lock = {
        "schema": _LOCK_SCHEMA, "migrated": True,
        "cairn_version": _cairn_version(cairn_root), "cairn_commit": commit,
        "profile": {}, "modules": sorted(
            m for m in _MODULE_MAPPINGS
            if (target / "dev" / "modules" / f"{m}.md").exists()),
        "optional_templates": [], "tokens": {}, "files": records,
    }
    lock_path = target / _LOCKFILE_REL
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(_emit_lock_yaml(lock), encoding="utf-8")
    print(f"Wrote migrated {_LOCKFILE_REL} ({len(records)} files).")
    print(f"  verbatim scripts (hash-tracked): "
          f"{len(classification['verbatim'])}")
    print(f"  token-substituted files (no recoverable base -> review-only "
          f"on upgrade, per I3): {len(classification['unrecoverable-base'])}")
    print("  NOTE: a migrated lockfile cannot 3-way-merge token-substituted "
          "files (the install token values were never recorded); those "
          "upgrade as a review-only diff. Re-install from an "
          "upgrade-capable Cairn for clean merges.")
    return 0


def _apply_upgrade(target: Path, lock: dict[str, Any]) -> int:
    """`--apply` (R7): consume the staged result under the safety contract,
    swap the originals, **advance the lockfile + base cache** to the new
    version, and clean the stage.  Fail-closed at every gate."""
    import json
    import shutil
    stage = target / _STAGING_REL
    meta_path = stage / _STAGE_META
    if not meta_path.exists():
        print("error: no staged upgrade found; run `upgrade --stage` first.",
              file=sys.stderr)
        return 1
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    files_dir = stage / "files"
    staged_meta = sorted(meta.get("staged_files", []))

    # (a) the stage was produced from the current lockfile + tokens + roster.
    if meta.get("lock_commit") != lock.get("cairn_commit") or \
            meta.get("tokens") != lock.get("tokens") or \
            meta.get("modules") != lock.get("modules"):
        print("error: staged upgrade is stale (lockfile/tokens/roster changed "
              "since --stage); re-run `upgrade --stage`.", file=sys.stderr)
        return 1
    # (b) staged-manifest exactness: the files on disk under the
    #     stage must be EXACTLY the metadata's staged set -- no missing, no
    #     extra (a corrupted/hand-edited stage must not apply a subset).
    on_disk = sorted(
        str(f.relative_to(files_dir)) for f in files_dir.rglob("*")
        if f.is_file()
    ) if files_dir.exists() else []
    if on_disk != staged_meta:
        print("error: staged file set does not match the stage manifest "
              "(corrupted/edited stage); re-run `upgrade --stage`.\n"
              f"  manifest: {staged_meta}\n  on disk:  {on_disk}",
              file=sys.stderr)
        return 1
    # (c) every staged file is an advancing kind (defense-in-depth;
    #     non-advancing kinds were never staged).
    kinds = meta.get("kinds", {})
    non_adv = [d for d in staged_meta if kinds.get(d) not in _ADVANCING_KINDS]
    if non_adv:
        print(f"error: staged non-advancing file(s) {non_adv} cannot be "
              "applied; re-run `upgrade --stage`.", file=sys.stderr)
        return 1
    # (d) no residual conflict markers (P-5: only a resolved tree applies).
    for staged in staged_meta:
        if _CONFLICT_MARKER in (files_dir / staged).read_text(
                encoding="utf-8", errors="replace"):
            print(f"error: staged file {staged} still has conflict markers; "
                  "resolve them, then re-run --apply.", file=sys.stderr)
            return 1
    # (e) the on-disk originals are unchanged *since --stage* (R7a),
    #     compared to the stage-time snapshot (NOT the clean-install hash --
    #     a customized file differs from that by design).
    ours_hashes = meta.get("ours_hashes", {})
    for staged in staged_meta:
        dst_abs = target / staged
        snap = ours_hashes.get(staged)
        if snap is not None and dst_abs.exists():
            if "sha256:" + _sha256_hex(dst_abs.read_bytes()) != snap:
                print(f"error: {staged} changed on disk since --stage; "
                      "re-run `upgrade --stage`.", file=sys.stderr)
                return 1

    # Swap staged files into place.
    for staged in staged_meta:
        dst_abs = target / staged
        _assert_safe_write(dst_abs, target)
        dst_abs.parent.mkdir(parents=True, exist_ok=True)
        dst_abs.write_text(
            (files_dir / staged).read_text(encoding="utf-8"), encoding="utf-8")
    # Advance the base cache to the new upstream raw templates (the next
    # upgrade's ancestor).
    new_base = stage / "new-base"
    if new_base.exists():
        for nb in new_base.rglob("*"):
            if not nb.is_file():
                continue
            cache_abs = target / _BASE_CACHE_REL / nb.relative_to(new_base)
            _assert_safe_write(cache_abs, target)
            cache_abs.parent.mkdir(parents=True, exist_ok=True)
            cache_abs.write_text(nb.read_text(encoding="utf-8"), encoding="utf-8")

    # Advance the lockfile: bump version/commit;
    # recompute each applied file's hash from the NOW-on-disk content (so a
    # resolved conflict is recorded correctly) + refresh the base_hash from
    # the swapped-in base cache.  Non-applied records carry over unchanged.
    new_lock = dict(lock)
    new_lock["cairn_version"] = meta.get("new_version", lock.get("cairn_version"))
    new_lock["cairn_commit"] = meta.get("new_commit", lock.get("cairn_commit"))
    new_files: list[dict[str, Any]] = []
    staged_set = set(staged_meta)
    for rec in lock.get("files", []):
        rec = dict(rec)
        if rec["dst"] in staged_set:
            rec["hash"] = "sha256:" + _sha256_hex((target / rec["dst"]).read_bytes())
            if rec.get("base_cache"):
                cache_abs = target / rec["base_cache"]
                if cache_abs.exists():
                    rec["base_hash"] = \
                        "sha256:" + _sha256_hex(cache_abs.read_bytes())
        new_files.append(rec)
    new_lock["files"] = new_files
    (target / _LOCKFILE_REL).write_text(_emit_lock_yaml(new_lock), encoding="utf-8")

    shutil.rmtree(stage)
    print(f"Applied {len(staged_meta)} file(s); advanced {_LOCKFILE_REL} + the "
          f"base cache to {new_lock['cairn_commit']}.")
    return 0


def cmd_upgrade(argv: list[str] | None = None) -> int:
    """`scaffold.py upgrade` -- the adopter upgrade path (Chunk 5/6)."""
    import argparse
    p = argparse.ArgumentParser(prog="scaffold.py upgrade")
    p.add_argument("--target", required=True)
    p.add_argument("--to", default=None,
                   help="Upgrade to this Cairn git ref (git-checkout source "
                        "only); default = the currently-running tree.")
    p.add_argument("--cairn-root", default=None)
    p.add_argument("--init-lock", action="store_true",
                   help="Synthesize a lockfile for a pre-lockfile tree (R6).")
    p.add_argument("--plan", action="store_true",
                   help="Read-only: classify drift, write nothing (default).")
    p.add_argument("--stage", action="store_true",
                   help="Write the staged review surface (no swap).")
    p.add_argument("--apply", action="store_true",
                   help="Apply a previously-staged, resolved upgrade.")
    args = p.parse_args(argv)

    target = Path(args.target).resolve()
    if not target.exists():
        print(f"error: target not found: {target}", file=sys.stderr)
        return 1
    cairn_root = (Path(args.cairn_root).resolve() if args.cairn_root
                  else _find_cairn_root(Path(__file__)))
    templates_root = cairn_root / "templates"

    if args.init_lock:
        return _cmd_init_lock(target, cairn_root, templates_root)

    lock = read_lockfile(target)
    if lock is None:
        print(f"error: no {_LOCKFILE_REL} in the target. Run "
              "`upgrade --init-lock --target <repo>` to migrate a "
              "pre-lockfile tree first.", file=sys.stderr)
        return 1

    if args.to is not None and not _cairn_is_git(cairn_root):
        print("error: --to <ref> needs a git-checkout Cairn source; a "
              "packaged release can upgrade only to the currently-running "
              "tree (omit --to).", file=sys.stderr)
        return 1

    if args.apply:
        return _apply_upgrade(target, lock)

    plans, structural = _compute_upgrade(
        target, cairn_root, templates_root, lock, args.to)
    citation = _citation_ok(target, lock)

    if args.stage:
        _write_stage(target, plans, lock, args.to, cairn_root)
        _print_upgrade_report(plans, structural, citation, mode="stage")
        print(f"\nStaged under {_STAGING_REL}/ . Resolve any conflicts, then "
              "`upgrade --apply --target <repo>`.")
        return 0

    # Default: --plan (strictly read-only).
    _print_upgrade_report(plans, structural, citation, mode="plan (read-only)")
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="scaffold.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--config",
        required=False,
        metavar="PROFILE_YAML",
        help="Path to the profile YAML config (see Appendix B in BOOTSTRAP.md). "
             "Required for an install; not needed with --manifest.",
    )
    p.add_argument(
        "--target",
        required=False,
        metavar="REPO_ROOT",
        help="Path to the target repository root. Required for an install; "
             "not needed with --manifest.",
    )
    p.add_argument(
        "--cairn-root",
        default=None,
        metavar="CAIRN_ROOT",
        help=(
            "Path to the Cairn repo root.  Auto-detected from this script's "
            "location if omitted."
        ),
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without writing any files.",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help=(
            "Overwrite existing files in the target.  Default (no --force) "
            "skips files that already exist and prints a skip warning, so "
            "re-running the scaffold preserves any filled block slots and "
            "other customizations the existing files carry."
        ),
    )
    p.add_argument(
        "--non-interactive",
        action="store_true",
        help=(
            "Force the module-merge pass into non-interactive mode "
            "(any merge conflict defers to a `<target>.cairn-merge-pending` "
            "side-file).  Auto-detected from `sys.stdin.isatty()` when not "
            "explicitly set."
        ),
    )
    p.add_argument(
        "--manifest",
        action="store_true",
        help=(
            "Emit the install manifest (the destination<TAB>source<TAB>kind "
            "set the scaffold would install, all modules) and exit.  The "
            "Layer-1 published manifest; needs no --config / --target."
        ),
    )
    p.add_argument(
        "--summary",
        action="store_true",
        help=(
            "Print the resolved Act I-6 dimension profile (preset + resolved "
            "six-axis point + module roster + add/remove overrides + "
            "staffability warnings) and exit WITHOUT installing.  The "
            "pre-install acceptance artifact (P4); needs --config, not "
            "--target."
        ),
    )
    p.add_argument(
        "--allow-dev",
        action="store_true",
        help=(
            "Silence the Layer-1 provenance warning when scaffolding from a "
            "non-tagged / dirty Cairn source (i.e. when developing Cairn "
            "itself)."
        ),
    )
    return p


def main(argv: list[str] | None = None) -> int:
    """Entry point.  Returns an exit code (0 = success, 1 = error)."""
    raw = sys.argv[1:] if argv is None else argv
    # `scaffold.py upgrade ...` routes to the adopter upgrade path, which has
    # its own argument parser (isolated from the install CLI).
    if raw and raw[0] == "upgrade":
        return cmd_upgrade(raw[1:])

    parser = build_arg_parser()
    args = parser.parse_args(argv)

    # --manifest is a read-only emit; it needs neither --config nor
    # --target (it is the published catalog of all installable files).
    if args.manifest:
        sys.stdout.write(format_manifest())
        return 0

    # --summary is the pre-install acceptance artifact (P4): resolve the
    # profile and print it WITHOUT installing.  Needs --config, not --target.
    if args.summary:
        if not args.config:
            print("error: --summary requires --config.", file=sys.stderr)
            return 1
        summary_config_path = Path(args.config).resolve()
        if not summary_config_path.exists():
            print(
                f"error: config not found: {summary_config_path}",
                file=sys.stderr,
            )
            return 1
        try:
            summary_cfg = load_config(summary_config_path)
        except Exception as exc:
            print(f"error loading config: {exc}", file=sys.stderr)
            return 1
        if "preset" in summary_cfg and "modules" in summary_cfg:
            print(
                "error: a profile may not set both `preset:` and `modules:` "
                "-- use `preset:` with `modules_add:` / `modules_remove:`, or "
                "`modules:` alone.",
                file=sys.stderr,
            )
            return 1
        try:
            if summary_cfg.get("preset"):
                sys.stdout.write(format_profile_summary(summary_cfg))
            else:
                # No preset: the modules: list (or the default-on set) is the
                # literal install -- summarize it plainly.
                mods = (
                    _as_str_list(summary_cfg.get("modules"), "modules")
                    if "modules" in summary_cfg
                    else list(_DEFAULT_ON_MODULES)
                )
                project = str(summary_cfg.get("project_name") or "<project_name>")
                out = [f"## Dimension profile -- {project}", "",
                       "Preset: (none -- literal module list)", "",
                       "Module roster (to install):"]
                out.extend(f"  - {m}" for m in mods)
                out.append("")
                out.append(
                    "Does this profile look right before I install anything?"
                )
                sys.stdout.write("\n".join(out) + "\n")
        except PresetError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        return 0

    if not args.config or not args.target:
        print(
            "error: --config and --target are required for an install "
            "(omit them only with --manifest).",
            file=sys.stderr,
        )
        return 1

    config_path = Path(args.config).resolve()
    target = Path(args.target).resolve()

    if not config_path.exists():
        print(f"error: config not found: {config_path}", file=sys.stderr)
        return 1
    if not target.exists():
        print(f"error: target directory not found: {target}", file=sys.stderr)
        return 1

    cairn_root = (
        Path(args.cairn_root).resolve()
        if args.cairn_root
        else _find_cairn_root(Path(__file__))
    )
    templates_root = cairn_root / "templates"
    if not templates_root.exists():
        print(
            f"error: templates/ not found under Cairn root: {cairn_root}",
            file=sys.stderr,
        )
        return 1

    # Layer-1 provenance nudge: warn (never block) when scaffolding from a
    # non-tagged / dirty Cairn source, unless --allow-dev.
    if not args.allow_dev:
        warning = git_provenance_warning(cairn_root)
        if warning:
            print(f"  [warn] {warning}", file=sys.stderr)

    # Load config
    try:
        cfg = load_config(config_path)
    except Exception as exc:
        print(f"error loading config: {exc}", file=sys.stderr)
        return 1

    tokens: dict[str, str] = {
        k: str(v)
        for k, v in cfg.items()
        if isinstance(k, str) and k in KNOWN_TOKENS and v
    }
    # Module selection (BOOTSTRAP.md Act I-5).  Three mutually-exclusive
    # shapes, plus the P4 preset fast path:
    #   * `preset:` (P4) -> expand to a roster via the pinned ordered merge
    #     (resolve axes -> gate-derived baseline -> add/remove); `resolved_axes`
    #     is the preset point + adopter overrides.
    #   * `modules:` alone -> today's exact-list semantics (`modules: []` opts
    #     out of all non-core modules).
    #   * `modules:` + `preset:` together -> a hard error (no replace-vs-merge
    #     guessing).
    #   * neither -> the default-on set, with an opt-out hint.
    # `resolved_axes` is the feed for axis-driven selection below (optional
    # templates): the preset-resolved point when a preset is used, else the
    # raw profile.
    resolved_axes: dict[str, object]
    if "preset" in cfg and "modules" in cfg:
        print(
            "error: a profile may not set both `preset:` and `modules:` -- "
            "use `preset:` with `modules_add:` / `modules_remove:` to "
            "compose, or `modules:` alone for an exact list.",
            file=sys.stderr,
        )
        return 1
    if cfg.get("preset"):
        try:
            modules, _preset_summary = expand_preset(cfg)
        except PresetError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        resolved_axes = dict(_preset_summary["axes"])  # type: ignore[arg-type]
        print(
            f"  [info] preset `{_preset_summary['preset']}` -> modules: "
            f"{', '.join(modules) or '(none)'}.",
            file=sys.stderr,
        )
        for warn in _preset_summary["staffability_warnings"]:  # type: ignore[union-attr]
            print(f"  [warn] staffability: {warn}", file=sys.stderr)
        if _preset_summary["removed_default_on"]:  # type: ignore[index]
            print(
                "  [info] default-on opted out via modules_remove: "
                f"{', '.join(_preset_summary['removed_default_on'])}.",  # type: ignore[arg-type]
                file=sys.stderr,
            )
    elif "modules" in cfg:
        try:
            modules: list[str] = _as_str_list(cfg.get("modules"), "modules")
        except PresetError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        resolved_axes = cfg
    else:
        modules = list(_DEFAULT_ON_MODULES)
        resolved_axes = cfg
        print(
            "  [info] profile omits `modules:` and `preset:`; installing the "
            f"default-on set ({', '.join(_DEFAULT_ON_MODULES)}).  Set "
            "`modules: []` to opt out explicitly, pick a `preset:`, or list a "
            "specific selection.",
            file=sys.stderr,
        )

    # Optional top-level templates (foldback #10): selected by the
    # dimension axes — e.g. the human-team axis selects CONTRIBUTING.md
    # at small-multi / large-multi.  Fed the RESOLVED axes (preset point +
    # overrides when a `preset:` is used, else the raw profile) per the
    # seam foldback #10 left for P4.
    optional = select_optional_templates(resolved_axes)
    if optional:
        names = ", ".join(dst for _, dst in optional)
        print(
            f"  [info] dimension profile selects optional template(s): "
            f"{names}.  Record each under `optional_templates:` in the "
            "fidelity manifest (bootstrap/fidelity-check.md) so the gate "
            "is auditable.",
            file=sys.stderr,
        )

    # Default the reference-script command tokens to the exact paths the
    # scaffold installs the scripts to (I5), unless the profile already
    # supplied a value.  This makes the shipped scripts immediately
    # runnable via the documented {{claim_check_command}} /
    # {{metrics_command}} line, and keeps the doc's invocation and the
    # install destination from desyncing.
    for token, value in reference_script_token_defaults(modules).items():
        tokens.setdefault(token, value)

    if args.dry_run:
        print("[dry-run] Would install to:", target)
        print("[dry-run] Tokens:          ", tokens)
        print("[dry-run] Modules:         ", modules)
        print(
            "[dry-run] Optional:        ",
            ", ".join(dst for _, dst in optional) or "(none)",
        )
        dry_preset = str(cfg.get("preset") or "").strip()
        if dry_preset and dry_preset in _ONBOARDING_PRESETS:
            print(
                f"[dry-run] Onboarding:      "
                f"templates/onboarding/{dry_preset}.md (seeds -> "
                f"dev/PLANNING.md slot; full source -> "
                f"dev/modules/onboarding/{dry_preset}.md)"
            )
        for mod in modules:
            for entry in _GITIGNORE_SEEDS.get(mod, ()):  # C6 dry-run
                would = seed_gitignore(target, (entry,), dry_run=True)
                if would:
                    print(f"[dry-run] Would seed .gitignore: {entry}")
        return 0

    # Create directory tree
    print(f"\nScaffolding Cairn into: {target}")
    if args.force:
        print("  (--force: existing files will be overwritten)")
    dirs_created = create_dev_tree(target)

    # Install core templates
    print("Installing core templates ...")
    core_results = install_core(
        templates_root, target, tokens, force=args.force
    )

    # Install progressive-onboarding content.  Must run AFTER
    # install_core because it edits the just-installed
    # dev/PLANNING.md's `onboarding-tasks` slot.  Always installs the
    # helper script + seeds the activation log (Chunk P1.2); only
    # populates the slot + copies the preset source file when a
    # `preset:` is selected (Chunk P1.1).
    preset_name = str(cfg.get("preset") or "").strip() or None
    label = (
        f"progressive onboarding ({preset_name})"
        if preset_name
        else "progressive onboarding (helper + log only; no preset)"
    )
    print(f"Installing {label} ...")
    onboarding_results = install_onboarding(
        templates_root, target, preset_name, force=args.force
    )

    # Install module templates
    print(f"Installing modules: {', '.join(modules) or '(none)'} ...")
    module_results = install_modules(
        templates_root, target, tokens, modules, force=args.force
    )

    # Issue-capture forge reference (fold-back #38): when issue-capture
    # installs and the profile names a forge, copy that forge's reference
    # starter (.gitlab/ or .github/) into the adopter root.  Non-clobber
    # (skip-unless --force).  Absent/unknown forge -> skipped; the
    # reference then stays a manual-copy starter under the module.
    reference_results: list[InstallResult] = []
    forge = str(cfg.get("forge") or "").strip().lower() or None
    if forge and forge not in _FORGE_REFERENCE_DIRS:
        print(
            f"  [warn] unknown forge '{forge}' (known: "
            f"{', '.join(sorted(_FORGE_REFERENCE_DIRS))}); issue-capture "
            f"reference not auto-copied.",
            file=sys.stderr,
        )
        forge = None
    if forge and "issue-capture" in modules:
        print(f"Installing issue-capture {forge} reference ...")
        reference_results = install_issue_capture_reference(
            templates_root, target, forge, force=args.force
        )

    # Install dimension-selected optional templates (foldback #10).
    optional_results: list[InstallResult] = []
    if optional:
        print(
            f"Installing optional templates: "
            f"{', '.join(dst for _, dst in optional)} ..."
        )
        optional_results = install_optional(
            templates_root, target, tokens, optional, force=args.force
        )

    print_report(
        target, dirs_created,
        core_results + onboarding_results + module_results
        + reference_results + optional_results,
    )

    # Module-merge pass (Proposal B / audit gap #3).  Each installed
    # module's `cairn:merge-target` / `cairn:merge-content-*`
    # directives drive a mechanical merge into the named target
    # template's `cairn:slot` anchor.  Modules without structured
    # directives are silently skipped (transitional; not every
    # module ships directives yet).  Non-interactive defer is the
    # safe default; explicit --non-interactive or non-TTY stdin
    # forces it (Antigravity P1 disposition).
    non_interactive = args.non_interactive or not sys.stdin.isatty()
    try:
        merge_results, fidelity_warnings = run_module_merge_pass(
            templates_root, target, modules,
            non_interactive=non_interactive,
        )
    except DuplicateSlotError as exc:
        print(f"error: module-merge parse phase: {exc}", file=sys.stderr)
        return 2
    if merge_results or fidelity_warnings:
        print("\nModule-merge pass:")
        for r in merge_results:
            tag = f"  [{r.status}]"
            extra = (
                f" -> {r.side_file}" if r.side_file else ""
            )
            print(f"{tag} {r.target_path} > {r.slot_name}{extra}")
        for target_rel, slot_name, reason in fidelity_warnings:
            print(
                f"  [slot-content-{reason}] {target_rel} > {slot_name} "
                f"(fidelity check)"
            )

    # Seed adopter-owned .gitignore for selected modules (Cairn v0.2 P5,
    # C6: non-clobber + idempotent), and print the OPT-IN hook command --
    # the scaffold never mutates .git/hooks itself (C2).
    for mod in modules:
        entries = _GITIGNORE_SEEDS.get(mod, ())
        if not entries:
            continue
        added = seed_gitignore(target, entries)
        if added:
            print(f"\nSeeded .gitignore ({mod}): {', '.join(added)}")
        else:
            print(
                f"\n.gitignore already covers the {mod} entr"
                f"{'y' if len(entries) == 1 else 'ies'}: "
                f"{', '.join(entries)}"
            )
    if "coordination-tiers" in modules:
        print(
            "\nRECOMMENDED (concurrent team) -- enable the work-intent git\n"
            "hooks. They are opt-in: the scaffold never mutates .git/hooks,\n"
            "so this is a one-time Day-1 step you run. Without them,\n"
            "dev/intents.jsonl stays empty even on a concurrent team -- the\n"
            "coordination signal this module exists for. Run:\n"
            "  python tools/intent.py install-hook        "
            "# post-commit auto-release\n"
            "  python tools/intent.py install-precommit   "
            "# pre-commit work-intent check (warn-only)\n"
            "  python tools/intent.py hooks-status        "
            "# confirm both are installed\n"
            "Opt out (now or later): re-run either install command with\n"
            "--uninstall. Your onboarding tasks include this step."
        )

    # Write the install lockfile + base-template cache: the upgrade
    # ancestor anchor (dev/cairn-lock.yml + dev/.cairn/base/).  Fail-closed
    # if the tree diverges from a clean install (P-1) -- then it points the
    # user at `upgrade --init-lock` and the install still succeeds.
    lock_profile: dict[str, Any] = {"preset": cfg.get("preset")}
    lock_profile["axes"] = {
        axis: resolved_axes.get(axis)
        for axis in _AXES
        if isinstance(resolved_axes, dict) and resolved_axes.get(axis)
    }
    try:
        lock = write_install_lockfile(
            target, cairn_root, templates_root,
            tokens=tokens, modules=modules, optional=optional,
            profile=lock_profile,
            onboarding_preset=preset_name,
        )
    except PresetError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if lock is not None:
        print(
            f"\nWrote {_LOCKFILE_REL} (upgrade ancestor) + the base-template "
            f"cache under {_BASE_CACHE_REL}/."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
