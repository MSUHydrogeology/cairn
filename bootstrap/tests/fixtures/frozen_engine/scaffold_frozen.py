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
    # External-dependency upstream issue drafts (core-dev-folder-set).
    # archive/ is tracked via the .gitkeep installed by _CORE_MAPPINGS;
    # the dir itself must exist before the installer writes it.
    "dev/upstream",
    "dev/upstream/archive",
    # Project-owned agent-discipline detail (core-dev-folder-set).
    # Ships empty at adoption; the README is installed by _CORE_MAPPINGS.
    "dev/rules",
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
    # Self-instrumentation home (measurement-folder standard): a core dir
    # carried by its README, which states the membership rule.  Same shape as
    # proposals/ + plans/ (a core dir installed via its content file).
    ("core/dev/measurement/README.md",              "dev/measurement/README.md"),
    # External-dependency upstream channel (core-dev-folder-set proposal):
    # draft issue reports for external OSS deps, distinct from the
    # methodology fold-back ledger (dev/.cairn/cairn_foldback.md).
    # archive/.gitkeep is verbatim (an empty placeholder, not a template).
    ("core/dev/upstream/README.md",                 "dev/upstream/README.md"),
    ("core/dev/upstream/_template.md",              "dev/upstream/_template.md"),
    ("core/dev/upstream/archive/.gitkeep",          "dev/upstream/archive/.gitkeep"),
    # Project-owned agent-discipline detail folder: the folder + README
    # ship from Cairn; the rule files inside are entirely the adopter's own
    # (Cairn never templates them).  Empty at adoption by design.
    ("core/dev/rules/README.md",                    "dev/rules/README.md"),
    # Stage-0 strategy space: the README (lifecycle + status vocabulary)
    # and the note template.  Shipped default-on; the strategy/ dir and
    # archive/ placeholder are created by create_dev_tree (see install.py).
    ("core/dev/strategy/README.md",                 "dev/strategy/README.md"),
    ("core/dev/strategy/_template.md",              "dev/strategy/_template.md"),
)

#: Lifecycle-routine skills install **unconditionally, like core/** -- the
#: session routines are invariant kernel (every adoption runs them), so they
#: are not a conditional ``templates/modules/*`` module.  ``(src relative to
#: templates/, dst relative to the repo root, verbatim)``.  The CLI is a script
#: -> ``verbatim`` (byte-for-byte, hash-only upgrade policy); the ``SKILL.md``
#: sources are markdown -> substituted (so they get a base-template cache entry
#: and a token-/slot-aware 3-way merge on upgrade, exactly like ``core/`` docs).
_SKILLS_MAPPINGS: tuple[tuple[str, str, bool], ...] = (
    ("skills/_lib/lifecycle.py",         "tools/lifecycle.py",                       True),
    ("skills/_lib/lifecycle_planner.py", "tools/lifecycle_planner.py",               True),
    ("skills/_data/vendor_targets.yml",  ".agents/skills/_data/vendor_targets.yml",  True),
    ("skills/session-start/SKILL.md",   ".agents/skills/session-start/SKILL.md",    False),
    ("skills/session-end/SKILL.md",     ".agents/skills/session-end/SKILL.md",      False),
)

#: Machine-local lifecycle state the skills write into ``dev/.cairn/`` -- the
#: untracked interpreter binding (resolve-don't-bake, Decision 6) and the
#: full-handoff lock.  Seeded into ``.gitignore`` unconditionally (the skills
#: always install).  ``dev/.cairn/base/`` itself stays tracked (the lockfile
#: base cache); only these machine-state members are ignored.
_SKILLS_GITIGNORE: tuple[str, ...] = (
    "dev/.cairn/local-env.json",
    "dev/.cairn/handoff.lock",
)

#: Common filenames an adopter renames the thin vendor wrapper
#: (``core/VENDOR.md``) to -- their AI tool's instruction file.  Used by
#: ``--init-lock`` to follow that rename so the wrapper stays tracked + 3-way
#: merges on later upgrades (foldback #45).  Distinctly vendor-specific names
#: only (``AGENTS.md`` is the shared file, deliberately excluded).
_KNOWN_VENDOR_WRAPPERS: tuple[str, ...] = (
    "CLAUDE.md", "GEMINI.md", "CODEX.md", "CURSOR.md", "COPILOT.md", "QWEN.md",
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
        # lifecycle-metrics fold-up (phase C, 2026-06): lifecycle_metrics.py is
        # now a thin launcher/facade over an owned `_lifecycle_metrics/` engine
        # package; the nine package files install verbatim beside the facade so
        # `python tools/lifecycle_metrics.py` resolves its sibling engine at
        # runtime (parity with the _intent/ + _onboarding/ splits).  Byte-for-byte code.
        InstallSpec("default-on/_lifecycle_metrics/__init__.py",
                    "tools/_lifecycle_metrics/__init__.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/config.py",
                    "tools/_lifecycle_metrics/config.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/parse.py",
                    "tools/_lifecycle_metrics/parse.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/gitmeta.py",
                    "tools/_lifecycle_metrics/gitmeta.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/report.py",
                    "tools/_lifecycle_metrics/report.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/subsystems.py",
                    "tools/_lifecycle_metrics/subsystems.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/extract.py",
                    "tools/_lifecycle_metrics/extract.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/snapshot.py",
                    "tools/_lifecycle_metrics/snapshot.py", verbatim=True),
        InstallSpec("default-on/_lifecycle_metrics/cli.py",
                    "tools/_lifecycle_metrics/cli.py", verbatim=True),
    ],
    "reflections": [
        InstallSpec("default-on/reflections.md", "dev/modules/reflections.md"),
        # A tracked directory guide so dev/reflections/ materializes on a
        # fresh scaffold (the reflection entries themselves stay untracked
        # via the .gitignore seed below) -- fold-back #42.
        InstallSpec("default-on/reflections-README.md",
                    "dev/reflections/README.md", verbatim=True),
        # Fold 2 (foldback-drain-tooling): explicit prune tool the reflections
        # module doctrine prescribes.
        InstallSpec("default-on/prune_reflections.py",
                    "tools/prune_reflections.py", verbatim=True),
    ],
    "claim-check": [
        InstallSpec("default-on/claim-check.md",
                    "dev/modules/claim-check.md"),
        InstallSpec("default-on/claim_check.py",
                    "scripts/claim_check.py", verbatim=True),
        # Fold 1 (foldback-drain-tooling): stem-resolution checker.
        InstallSpec("default-on/verify_stems.py",
                    "scripts/verify_stems.py", verbatim=True),
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
        # The deterministic, zero-token rate-limit-gate evaluator +
        # fold-up-backlog checker (self-evolution-loop Part B). Reads the
        # trackers + the fold-back ledger and emits suggestions only.
        InstallSpec("default-on/evolution_infer.py",
                    "tools/evolution_infer.py", verbatim=True),
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
    # ledger artifact into dev/.cairn/, the active-surfacing prompt asset
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
                    "dev/.cairn/cairn_foldback.md"),
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
        # intent-split (phase A, 2026-06): intent.py is a thin facade over an owned
        # `_intent/` engine package; the seven package files install verbatim beside it.
        InstallSpec("team-gated/_intent/__init__.py",
                    "tools/_intent/__init__.py", verbatim=True),
        InstallSpec("team-gated/_intent/shared.py",
                    "tools/_intent/shared.py", verbatim=True),
        InstallSpec("team-gated/_intent/record_io.py",
                    "tools/_intent/record_io.py", verbatim=True),
        InstallSpec("team-gated/_intent/identity.py",
                    "tools/_intent/identity.py", verbatim=True),
        InstallSpec("team-gated/_intent/conflict.py",
                    "tools/_intent/conflict.py", verbatim=True),
        InstallSpec("team-gated/_intent/hooks.py",
                    "tools/_intent/hooks.py", verbatim=True),
        InstallSpec("team-gated/_intent/cli.py",
                    "tools/_intent/cli.py", verbatim=True),
        # Fold 2 (foldback-drain-tooling): the prune-intents goodnight compaction tool.
        InstallSpec("team-gated/prune_intents.py",
                    "tools/prune_intents.py", verbatim=True),
    ],
    "security-review": [
        InstallSpec("team-gated/security-review.md",
                    "dev/modules/security-review.md"),
    ],
    "issue-capture": [
        InstallSpec("team-gated/issue-capture.md",
                    "dev/modules/issue-capture.md"),
        InstallSpec(
            "team-gated/issue-capture/bootstrap_gitlab_labels.py",
            "scripts/bootstrap_gitlab_labels.py",
            verbatim=True,
        ),
        InstallSpec(
            "team-gated/issue-capture/bootstrap_github_labels.py",
            "scripts/bootstrap_github_labels.py",
            verbatim=True,
        ),
    ],
    "model-selection": [
        InstallSpec("team-gated/model-selection.md",
                    "dev/modules/model-selection.md"),
        InstallSpec(
            "team-gated/model_selection_mapping_stub.yml",
            "dev/.cairn/model-selection-mapping.yml",
        ),
        InstallSpec(
            "team-gated/check_model_selection.py",
            "scripts/check_model_selection.py",
            verbatim=True,
        ),
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
    # Architecture-review (modflow_tools doctrine-parity fold, 2026-06-01):
    # a triggered remediation / on-ramp module for an adopter whose
    # architecture accreted rather than was deliberately designed.  Ships
    # the module doctrine + a forkable rubric frame the adopter fills
    # (the incident-trackers / documentation-plan 2-spec pattern, both
    # substituted not verbatim).  Team-gated, opt-in -- not in any
    # default-on set or governance preset.
    "architecture-review": [
        InstallSpec("team-gated/architecture-review.md",
                    "dev/modules/architecture-review.md"),
        InstallSpec("team-gated/architecture_review_template.md",
                    "dev/architecture_review.md"),
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
    # file pattern under `dev/.cairn/` before invoking the scanner.
    # The draft file is intentionally never committed -- the durable
    # record is the filed Cairn issue / PR + the ledger row's
    # status transition.  Seeded by default so an adopter does not
    # have to remember the pattern themselves.
    "fold-back-ledger": ("dev/.cairn/.foldback-draft-*.md",),
    # Reflections are per-agent + ephemeral (gitignored); only the tracked
    # README.md guide survives, so the dir materializes on a fresh scaffold
    # without committing reflection content (fold-back #42).  Order matters:
    # ignore-all then un-ignore the README.
    "reflections": ("dev/reflections/*", "!dev/reflections/README.md"),
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

#: Per-module team-staffing gate: the ``agent_team`` axis values that staff
#: each module.  These are the ONLY part of the I-5 gate evaluated as runtime
#: code; the non-axis gate conditions (trust boundary, issue tracker, domain
#: partitioning, legacy readiness) are baked into each preset's authored
#: baseline below (the "gate-table encoding" split from the P4 plan).
#:
#: The two modules gate **differently** (fold-back #40): ``coordination-tiers``
#: serves any *concurrent* team -- multiple same-type agents collide on shared
#: files exactly as a multi-type team does, and the work-intent mechanism is
#: what prevents it -- so it staffs both ``concurrent-multi-type`` and
#: ``concurrent-single-type``.  ``dual-review`` needs a second agent *type* to
#: fill its External tier with structural independence, which a same-type team
#: lacks, so it stays ``concurrent-multi-type`` only.
_TEAM_STAFFING_GATES: dict[str, frozenset[str]] = {
    "dual-review": frozenset({"concurrent-multi-type"}),
    "coordination-tiers": frozenset(
        {"concurrent-multi-type", "concurrent-single-type"}
    ),
}

#: All team-staffing-gated module names (membership tests; staffability is
#: per-module via :func:`_can_staff_module`).
_TEAM_STAFFING_GATED: tuple[str, ...] = tuple(_TEAM_STAFFING_GATES)


def _can_staff_module(name: str, axes: dict[str, str]) -> bool:
    """True when the resolved agent-team axis staffs the given team-staffing
    module, per the per-module gate (fold-back #40)."""
    return axes.get("agent_team", "") in _TEAM_STAFFING_GATES.get(
        name, frozenset()
    )


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
    for mod in _TEAM_STAFFING_GATED:
        if _can_staff_module(mod, resolved_axes):
            baseline.add(mod)

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
        if name in _TEAM_STAFFING_GATED and not _can_staff_module(
            name, resolved_axes
        ):
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


def install_skills(
    templates_root: Path,
    target: Path,
    tokens: dict[str, str],
    *,
    dry_run: bool = False,
    force: bool = False,
) -> list[InstallResult]:
    """Install the lifecycle-routine skills **unconditionally** (like core).

    A sibling to :func:`install_core` (kept separate rather than folded into
    it): the skills install to distinct destinations (``.agents/skills/`` +
    ``tools/lifecycle.py``) and carry per-file verbatim/substituted rules that
    differ from core docs, so a dedicated installer keeps each surface's rules
    legible.  Because the routines are invariant kernel they are not a
    conditional module.  ``verbatim`` is read per spec from
    :data:`_SKILLS_MAPPINGS` (the CLI script is byte-for-byte; the SKILL.md
    sources are substituted so they ride the base-cache + 3-way-merge path).
    """
    results: list[InstallResult] = []
    for src_rel, dst_rel, verbatim in _SKILLS_MAPPINGS:
        src = templates_root / src_rel
        if not src.exists():
            print(f"  [warn] skill template missing: {src_rel}", file=sys.stderr)
            continue
        dst = target / dst_rel
        results.append(
            _install_one(
                src, dst, tokens, target,
                dry_run=dry_run, force=force, verbatim=verbatim,
            )
        )
    return results


def write_local_env(
    target: Path, *, dry_run: bool = False, force: bool = False,
) -> InstallResult:
    """Write the untracked ``dev/.cairn/local-env.json`` interpreter binding.

    Resolve-don't-bake (Decision 6 / R3): record the bootstrap interpreter's
    **fully-resolved** absolute path (``Path.resolve()`` dereferences every
    symlink component, so the strict tamper-aware schema the lifecycle CLI
    enforces is satisfied) so the wrapper invokes it directly instead of relying
    on shell-level conda activation.  The file is **gitignored**, so an absolute
    path here never enters a commit -- it is forbidden only in tracked
    artifacts.  Non-clobber: an existing adopter binding is preserved unless
    ``force``.
    """
    import json

    dst = target / "dev" / ".cairn" / "local-env.json"
    if dst.exists() and not force:
        return (dst, [], [], "skipped-exists")
    if dry_run:
        return (dst, [], [], "dry-run")
    # Seed the ignore entries FIRST (Codex P1#2): otherwise a failure between
    # this write and the later unconditional gitignore seed would leave an
    # unignored local-env.json carrying a local absolute path, exposed to a
    # broad `git add`. Seeding first makes it ignored the instant it exists.
    seed_gitignore(target, _SKILLS_GITIGNORE)
    interpreter = str(Path(sys.executable).resolve())
    _assert_safe_write(dst, target)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(
        json.dumps({"interpreter": interpreter}) + "\n", encoding="utf-8"
    )
    return (dst, [], [], "installed")


def load_vendor_targets(templates_root: Path) -> list[dict[str, Any]]:
    """Load the data-driven vendor fan-out table (``skills/_data/
    vendor_targets.yml``).  JSON-encoded (valid YAML 1.2) so it parses
    stdlib-only, like the lockfile.  A vendor refresh is a row edit here."""
    import json

    path = templates_root / "skills" / "_data" / "vendor_targets.yml"
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data.get("targets", []))


def render_compatibility_matrix(templates_root: Path) -> str:
    """Render the skills compatibility matrix from the vendor-targets table.

    Generated, never hand-authored (II3 / Decision 8): the published level for
    each target is the table's, and the table's levels are claimed-pending-
    fixture until Chunk 7's harness proves a target into ``native-tested``.  The
    ``auto_suppress`` column makes the R4 gap visible per target rather than
    buried in prose.  Deterministic (sorted by target) so the drift gate is
    stable."""
    rows = sorted(load_vendor_targets(templates_root), key=lambda r: r["target"])
    out = [
        "# Skills compatibility matrix",
        "",
        "<!-- GENERATED from templates/skills/_data/vendor_targets.yml by",
        "     bootstrap.scaffold.render_compatibility_matrix; hand edits are",
        "     replaced on the next render.  Levels are CLAIMED-pending-fixture",
        "     (II3): a target is `native-tested` only once a fixture proves",
        "     install + invoke on it. -->",
        "",
        "| Target | Tier | Format | Install/invoke level | Auto-suppress |",
        "|--------|------|--------|----------------------|---------------|",
    ]
    for r in rows:
        out.append(
            f"| {r['target']} | {r['tier']} | {r.get('format', '-')} "
            f"| {r.get('level', '-')} | {r.get('auto_suppress', '-')} |"
        )
    out += [
        "",
        "## Runtime self-heal",
        "",
        "A **symlink**-tier target's read-path is fanned out from the canonical",
        "`.agents/skills/` source at install time. It is *also* re-ensured at",
        "**session-start** by the lifecycle backend (`tools/lifecycle.py",
        "session-start`), so an adopter established by lockfile-copy -- or whose",
        "symlink-tier harness was not present at install -- self-heals on first",
        "run instead of silently having no skills in that harness. The self-heal",
        "is idempotent and carries the installer's writer-safety contract:",
        "path-containment, a copy fallback where symlinks are unavailable (with a",
        "`.gitignore` seed), and a refuse-or-quarantine guard that never clobbers",
        "a divergent existing target. **alias**-tier targets read `.agents/skills/`",
        "directly and need no fan-out (nothing is emitted for them).",
    ]
    return "\n".join(out) + "\n"


def _symlinks_available(target: Path) -> bool:
    """Probe whether ``os.symlink`` works in *target* (False on Windows without
    Developer Mode / Administrator -- the copy-fallback trigger, R2)."""
    import os

    probe = target / ".cairn-symlink-probe"
    try:
        if probe.is_symlink() or probe.exists():
            probe.unlink()
        os.symlink(".", probe)
        ok = probe.is_symlink()
        probe.unlink()
        return ok
    except (OSError, NotImplementedError):
        return False


def _assert_fanout_contained(dst: Path, target: Path) -> None:
    """Containment for a fan-out destination (S3).

    Like :func:`_assert_safe_write` but permits ``dst`` *itself* to be a symlink
    (the symlink we are about to (re)create): it still refuses a **symlinked
    parent** and any path resolving **outside** *target*."""
    tr = target.resolve()
    for ancestor in dst.parents:
        if ancestor == tr:
            break
        try:
            ancestor.relative_to(tr)
        except ValueError:
            break
        if ancestor.is_symlink():
            raise ScaffoldSecurityError(
                f"refusing fan-out through a symlinked parent: {ancestor}"
            )
    final = dst.parent.resolve() / dst.name
    try:
        final.relative_to(tr)
    except ValueError:
        raise ScaffoldSecurityError(
            f"refusing fan-out outside the target directory: {final}"
        )


def _emit_skill_symlink(dst: Path, canonical: Path) -> str:
    """Create / verify a relative symlink ``dst`` -> the canonical skills dir."""
    import os

    rel = os.path.relpath(canonical, dst.parent)
    if dst.is_symlink():
        if os.readlink(dst) == rel:
            return "linked"  # idempotent
        dst.unlink()
    elif dst.exists():
        print(
            f"  [warn] {dst} exists as a non-symlink; leaving it untouched "
            "(remove it to enable the skills symlink).",
            file=sys.stderr,
        )
        return "exists-nonsymlink"
    dst.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(rel, dst, target_is_directory=True)
    return "linked"


def _emit_skill_copy_fallback(
    dst: Path, canonical: Path, target: Path,
) -> str:
    """Regenerate gitignored copies of the canonical skills under *dst*.

    The generated copy is a **vendor-read supply-chain artifact**, not an
    author-owned file (the canonical ``.agents/skills/`` source is the single
    editable copy).  So a diverged copy must NOT stay the active read-path
    (Codex code review P1#1, refining EP3's "never clobber", which applied to
    author-owned files, not this generated tier): the vendor harness would
    otherwise ingest stale / locally-edited / tampered instructions while the
    install reports success and the lockfile/security tests describe only the
    canonical bytes.

    Fail-safe-for-the-supply-chain: a diverged copy is **quarantined** (moved
    aside to ``<file>.diverged.bak`` -- the stray bytes are preserved for
    recovery, never silently destroyed) and then **regenerated from canonical**,
    so the active vendor-read path always carries the safe, already-scanned
    canonical bytes.  The divergence is still surfaced loudly."""
    import shutil

    quarantined: list[str] = []
    for src_file in sorted(canonical.rglob("*")):
        if not src_file.is_file():
            continue
        rel = src_file.relative_to(canonical)
        out = dst / rel
        _assert_fanout_contained(out, target)
        if out.is_file() and out.read_bytes() != src_file.read_bytes():
            # Quarantine the stray bytes (preserve, don't destroy), then
            # regenerate the canonical bytes as the active read-path.
            bak = out.with_name(out.name + ".diverged.bak")
            _assert_fanout_contained(bak, target)
            shutil.move(str(out), str(bak))
            quarantined.append(str(rel))
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_file, out)
    if quarantined:
        print(
            f"  [warn] copy-fallback divergence under {dst}: "
            f"{', '.join(quarantined)} differed from the canonical "
            ".agents/skills/ source. Each was quarantined to "
            "*.diverged.bak and the canonical bytes regenerated as the active "
            "vendor-read path -- edit the canonical source, not the generated "
            "copy. Recover any intended change from the .bak.",
            file=sys.stderr,
        )
        return "diverged-quarantined"
    return "copied"


def fan_out_skills(
    templates_root: Path,
    target: Path,
    *,
    dry_run: bool = False,
    force: bool = False,
    targets: list[dict[str, Any]] | None = None,
    allow_symlinks: bool | None = None,
) -> list[tuple[str, str, str]]:
    """Fan the canonical ``.agents/skills/`` source out to each vendor target by
    tier (Decision 4, revised).  Returns ``(target, tier_used, status)`` rows.

    * **alias** -- the harness reads ``.agents/skills/`` directly; nothing emitted.
    * **symlink** -- same SKILL.md format at a different path: a *verified*
      relative symlink to the canonical dir, emitted only when the vendor's
      parent dir already exists (a light "is this harness in use?" detection, so
      a fresh repo is not littered with empty vendor dirs).  Where symlinks are
      unavailable (Windows without Developer Mode) it degrades to the
      **gitignored generated copy** + divergence guard.
    * **manual** -- a different-format target (compiled artifact / documented
      manual fallback); never a symlink to incompatible files.

    Every destination is containment-checked **before** any write (S3); the
    divergence guard runs only after containment validates the target.
    """
    canonical = target / ".agents" / "skills"
    rows = targets if targets is not None else load_vendor_targets(templates_root)
    can_symlink = (
        _symlinks_available(target) if allow_symlinks is None else allow_symlinks
    )
    results: list[tuple[str, str, str]] = []
    advisory = False
    for row in rows:
        name = str(row.get("target", "?"))
        tier = row.get("tier")
        if tier == "alias":
            results.append((name, "alias", "noop"))
            continue
        if tier == "manual":
            results.append((name, "manual", "manual-fallback"))
            continue
        if tier != "symlink":
            results.append((name, str(tier), "unknown-tier"))
            continue
        path = str(row.get("path", ""))
        if not path or path.startswith("/") or ".." in Path(path).parts:
            raise ScaffoldSecurityError(
                f"vendor target {name!r}: unsafe fan-out path {path!r}"
            )
        dst = target / path
        if not dst.parent.exists():
            results.append((name, "symlink", "skipped-vendor-absent"))
            continue
        _assert_fanout_contained(dst, target)
        if dry_run:
            results.append((name, "symlink" if can_symlink else "copy", "dry-run"))
            continue
        if can_symlink:
            results.append((name, "symlink", _emit_skill_symlink(dst, canonical)))
        else:
            advisory = True
            status = _emit_skill_copy_fallback(dst, canonical, target)
            seed_gitignore(target, (path.rstrip("/") + "/",))
            results.append((name, "copy", status))
    if advisory:
        print(
            "  [advisory] symlinks unavailable (Windows without Developer "
            "Mode?) -- skills fanned out as gitignored generated copies. "
            "Enable Developer Mode for symlinked vendor targets.",
            file=sys.stderr,
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

#: The shared onboarding reference docs Cairn ships into an adopter when
#: a preset is selected (fold-back: onboarding-doc-delivery).  Sourced
#: from ``cairn/docs/`` (``templates_root.parent / "docs"``) and installed
#: under ``dev/modules/onboarding/``.  The presets' "walk this doc" task
#: refs point at the *installed* copies; without this write those refs
#: were dead links on first run (the bug this delivery fixes).
_ONBOARDING_DOC_NAMES = ("agent-team-onboarding.md", "dev-tour.md")
_ONBOARDING_DOC_DST_DIR_REL = "dev/modules/onboarding"


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
    E. Copy the shared onboarding reference docs
       (``docs/agent-team-onboarding.md`` + ``docs/dev-tour.md``) to
       ``<target>/dev/modules/onboarding/`` so the presets' "walk this
       doc" task refs resolve in the adopter (fold-back:
       onboarding-doc-delivery; without this they were dead links on
       first run).  Shared across presets -- shipped on any preset
       selection.

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

    # ----- Always: fan out the activation engine package (A2) -----------
    # Onboarding-split (phase B): onboarding_activate.py is now a thin
    # launcher/facade over a private ``_onboarding/`` engine package that
    # must install BESIDE it at ``scripts/_onboarding/`` for the facade to
    # import (parity with the team-gated ``tools/_intent/`` package install).
    # Sourced from the sibling ``_onboarding/`` dir next to the helper
    # source; each ``*.py`` copied verbatim through the containment guard.
    engine_src_dir = helper_src.parent / "_onboarding"
    engine_dst_dir = helper_dst.parent / "_onboarding"
    if engine_src_dir.is_dir():
        for engine_src in sorted(engine_src_dir.glob("*.py")):
            engine_dst = engine_dst_dir / engine_src.name
            if dry_run:
                results.append((engine_dst, [], [], "dry-run"))
            elif engine_dst.exists() and not force:
                print(
                    f"  [skip] {engine_dst}: already exists -- pass --force "
                    f"to overwrite",
                    file=sys.stderr,
                )
                results.append((engine_dst, [], [], "skipped-exists"))
            else:
                _assert_safe_write(engine_dst, target)
                engine_dst.parent.mkdir(parents=True, exist_ok=True)
                engine_dst.write_bytes(engine_src.read_bytes())
                results.append((engine_dst, [], [], "installed"))

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

    # Write E: ship the shared onboarding reference docs into the
    # installed-source dir so the presets' "walk this doc" refs resolve
    # in the adopter (fold-back: onboarding-doc-delivery).  Sourced from
    # cairn/docs/; same skip-unless-force guard as Write D.  Shared across
    # presets, so a preset selection ships both regardless of which one.
    docs_root = templates_root.parent / "docs"
    for doc_name in _ONBOARDING_DOC_NAMES:
        doc_src = docs_root / doc_name
        doc_dst = target / _ONBOARDING_DOC_DST_DIR_REL / doc_name
        if not doc_src.exists():
            print(
                f"  [warn] onboarding doc source missing: docs/{doc_name}",
                file=sys.stderr,
            )
            continue
        if dry_run:
            results.append((doc_dst, [], [], "dry-run"))
            continue
        if doc_dst.exists() and not force:
            print(
                f"  [skip] {doc_dst}: already exists -- pass --force to "
                f"overwrite",
                file=sys.stderr,
            )
            results.append((doc_dst, [], [], "skipped-exists"))
            continue
        _assert_safe_write(doc_dst, target)
        doc_dst.parent.mkdir(parents=True, exist_ok=True)
        doc_dst.write_text(
            doc_src.read_text(encoding="utf-8"), encoding="utf-8"
        )
        results.append((doc_dst, [], [], "installed"))

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
    # Skills install unconditionally (like core); always in the manifest.
    entries.extend(_SKILLS_MAPPINGS)
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
#   * ``dev/.cairn/cairn-lock.yml`` -- a *tracked* machine lockfile: the upgrade
#     ancestor + the install-side provenance record.  Tool-owned (only
#     ``scaffold.py`` reads/writes it), not a human-readable document, so it
#     lives with the other Cairn machinery under ``dev/.cairn/`` rather than at
#     the ``dev/`` root.  (Reverses the original R2 "visible at dev/ root"
#     placement: a ``.cairn/`` dotfolder does not hide the file from agents, and
#     keeping it out of the ``dev/`` listing leaves that listing human-meaningful.)
#   * ``dev/.cairn/base/`` -- a *tracked* cache of the **raw** upstream
#     templates for the mergeable ``.md`` installs (R1/I4): so the merge's
#     ``base`` is on disk under any distribution mode (no Cairn git history
#     needed) and only the mergeable set is shadow-copied.

_LOCKFILE_REL = "dev/.cairn/cairn-lock.yml"        # tracked machinery (in .cairn/ with its kin)
_BASE_CACHE_REL = "dev/.cairn/base"         # tracked raw-template cache (R1/I4)
_PROFILE_REL = "dev/.cairn/profile.yml"     # canonical committed install-config (BOOTSTRAP.md)
_LOCK_SCHEMA = 1

#: Directories searched (in order) for an adopter's fidelity manifest when
#: recovering ``cairn_commit`` / checking the citation.  ``dev/.cairn/`` is the
#: canonical home (the adoption-state-home convention); ``dev/strategy/`` is the
#: legacy home, kept indefinitely for un-migrated adopters with a migration
#: advisory at the call site.
_MANIFEST_SEARCH_DIRS = ("dev/.cairn", "dev/strategy")

#: Lockfile records for these dsts carry ``living_state: true`` and are
#: **tracked for upgrade but excluded from the ``verify_integrity`` hash
#: check**.  Rationale: ``verify_integrity`` exists so a cold adopter can
#: attest the *shipped Cairn apparatus* (scripts, module/core doctrine,
#: templates) was not swapped -- a supply-chain check.  These four files are
#: not apparatus: their content is **adopter-authored project state** (a living
#: roadmap, the per-goodnight handoff, the fold-back ledger, the signed
#: collaboration agreement) that merely starts from a thin Cairn template.
#: They are the highest-churn files in a mature adopter, so including them in
#: the strict integrity set means every routine edit reds the verifier until a
#: re-finalize -- friction that says nothing about whether the *scripts* are
#: trustworthy.  They keep ``base_cache`` / ``base_hash`` so ``upgrade`` still
#: 3-way-merges a Cairn template change into the adopter's customization; only
#: the tamper check skips them.  (Note this is deliberately NOT paired with a
#: goodnight auto-``--finalize``: blessing whatever is on disk on a schedule
#: would *launder* a real apparatus swap -- the very thing the check defends --
#: so ``--finalize`` stays an explicit, deliberate re-attestation.)
#:
#: **Conscious tradeoff (governance prose).**  ``dev/collaboration_agreement.md``
#: is the most delicate member: a signed agreement can govern review rights,
#: commit permissions, and trust boundaries, so excluding it from tamper
#: attestation is a real (accepted) tradeoff -- tampering with governance *prose*
#: is **outside ``verify_integrity``'s threat model** (which covers a swapped
#: *executable*) and is caught by git review + history, not by the
#: apparatus-integrity gate.  **This boundary is enforced by the verifier**, not
#: trusted from the lockfile: ``verify_integrity`` honors ``living_state`` only
#: for a ``dst`` in this set, and fails closed on any other record that asserts
#: it (so a modified script cannot hide by flipping the flag).
_LIVING_STATE_DSTS: frozenset[str] = frozenset({
    "dev/PLANNING.md",
    "dev/NEXT_SESSION.md",
    "dev/.cairn/cairn_foldback.md",
    "dev/collaboration_agreement.md",
    # Fold 5 (foldback-drain-tooling): the model-selection mapping is
    # adopter-local configuration that the adopter fills and re-fills as
    # their model lineup evolves.  Marking it living-state means
    # verify_integrity never flags an adopter edit as tampering, and the
    # lockfile divergence check does not prevent writing on first-fill.
    "dev/.cairn/model-selection-mapping.yml",
})

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


def _behind_by_n(cairn_root: Path, lock_commit: str | None,
                 new_commit: str | None) -> str:
    """#54 adoption->canonical drift surfacing: a one-line message for how far
    the adopter's installed Cairn ref (*lock_commit*) is behind canonical
    (*new_commit*).

    **Degrades gracefully (R1).** If either ref is missing or the ``unknown``
    sentinel (a non-git / packaged-release source, per ``_cairn_commit``), or
    git is unavailable, it returns an explicit *unavailable* message rather
    than running a git compare on a bad ref. Informational only -- the caller
    surfaces it; it never blocks."""
    import subprocess
    if (not lock_commit or not new_commit
            or "unknown" in (lock_commit, new_commit)):
        return ("adoption drift: behind-by-N check unavailable "
                "(git metadata missing)")
    if lock_commit == new_commit:
        return "adoption drift: installed tree is current with canonical"
    try:
        r = subprocess.run(
            ["git", "-C", str(cairn_root), "rev-list", "--count",
             f"{lock_commit}..{new_commit}"],
            capture_output=True, text=True, timeout=10, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "adoption drift: behind-by-N check unavailable (git error)"
    if r.returncode != 0:
        return ("adoption drift: behind-by-N check unavailable "
                "(refs not comparable)")
    return ("adoption drift: installed tree is behind canonical by "
            f"{r.stdout.strip()} commit(s)")


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
    """Read ``<target>/dev/.cairn/cairn-lock.yml`` (or None if absent/unparseable).

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
    """Write ``dev/.cairn/cairn-lock.yml`` + the scoped base-template cache.

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
        if dst_rel in _LIVING_STATE_DSTS:
            # Adopter-authored project state: tracked for upgrade, excluded
            # from the verify_integrity tamper check (see _LIVING_STATE_DSTS).
            rec["living_state"] = True
        if not verbatim:
            cache_rel = f"{_BASE_CACHE_REL}/{dst_rel}"
            rec["base_cache"] = cache_rel
            rec["base_hash"] = "sha256:" + _sha256_hex(raw.encode("utf-8"))
            cache_writes.append((target / cache_rel, raw))
        else:
            # The as-shipped baseline for a verbatim file, kept distinct from
            # ``hash`` so ``hash`` can be advanced to the adopter's committed
            # on-disk content (``upgrade --finalize``) for integrity while
            # ``classify_verbatim`` still detects an adopter fork against the
            # upstream baseline.  At fresh install ``hash == base_hash``.
            rec["base_hash"] = "sha256:" + _sha256_hex(would)
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
    lock_path.parent.mkdir(parents=True, exist_ok=True)
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

    The ``ours == theirs`` check runs **first** (fold-back #48): a file an
    adopter hand-synced to *exactly* the new upstream before upgrading is
    ``up-to-date``, not a fork -- even when the lockfile hash is stale (it was
    recorded against an older Cairn). Were the stale-hash check first, such a
    file would be flagged a fork on every future upgrade. ``--apply`` heals the
    stale lock hash (see ``_write_stage``/``_apply_upgrade``: ``verbatim_rehash``).
    """
    if ours_bytes is None:
        return "missing"
    if ours_bytes == theirs_bytes:
        return "up-to-date"
    ours_h = "sha256:" + _sha256_hex(ours_bytes)
    if ours_h != lock_hash:
        return "locally-modified"
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
    {"clean", "clean-locally-modified", "conflict", "verbatim-update",
     "new-core"}
)

#: Display labels for the upgrade report.  Maps the internal kind to the
#: adopter-facing label; kinds not in this map render verbatim.
_KIND_DISPLAY_LABEL = {
    "clean": "clean (untouched)",
    "clean-locally-modified": "locally-modified (merged clean)",
    "new-core": "new core/skills (added)",
}


class FilePlan(NamedTuple):
    dst: str
    kind: str
    applied: str | None      # content written on --apply (advancing kinds); else None
    detail: str
    theirs_raw: str | None    # new upstream RAW template (mergeable) -> refreshed base cache
    base_cache: str | None    # lockfile base_cache rel path (mergeable) to refresh
    src: str | None = None    # new-core: source template rel-to-templates/ (to build the lockfile entry)
    verbatim: bool = False    # new-core: verbatim flag for the new lockfile entry


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
        # Renamed vendor wrapper (#45): the lockfile records the thin
        # wrapper under its canonical dst ``VENDOR.md`` (``write_install_
        # lockfile`` does not resolve the rename), but an adopter renames it
        # to their tool's file (``CLAUDE.md`` etc.).  If ``VENDOR.md`` is
        # absent on disk but a known wrapper is present, classify THAT file
        # -- the base cache stays keyed on VENDOR.md (``rec["base_cache"]``),
        # so the 3-way merge still recovers the clean ancestor.  Without this,
        # a renamed-wrapper adopter sees a spurious ``review-only`` "file
        # missing on disk" for VENDOR.md on every upgrade.
        if src_rel == "core/VENDOR.md" and not (target / dst).exists():
            resolved = _resolve_vendor_wrapper(
                target, {r["dst"] for r in lock.get("files", [])},
            )
            if resolved is not None:
                dst = resolved
        dst_abs = target / dst
        ours_bytes = dst_abs.read_bytes() if dst_abs.exists() else None
        theirs_b = _theirs_bytes(cairn_root, templates_root, src_rel, to_ref)
        if theirs_b is None:
            plans.append(FilePlan(dst, "removed-upstream", None,
                                  "no longer in upstream templates", None, None))
            continue
        if verbatim:
            # Use the as-shipped baseline (``base_hash``) for fork detection,
            # not ``hash`` (which ``--finalize`` advances to the adopter's
            # committed on-disk content). Fall back to ``hash`` for lockfiles
            # written before verbatim records carried ``base_hash``.
            kind = classify_verbatim(
                ours_bytes, rec.get("base_hash") or rec.get("hash", ""), theirs_b)
            plans.append(FilePlan(
                dst, f"verbatim-{kind}",
                theirs_b.decode("utf-8", "replace") if kind == "update" else None,
                "", None, None))
            continue
        # Mergeable .md.
        if ours_bytes is None:
            # File missing on disk (e.g. a default-on module slot that never
            # installed).  Carry theirs_raw so --stage can write the upstream
            # version into the review-only surface (there is no .ours to pair
            # it with -- nothing is on disk).
            plans.append(FilePlan(dst, "review-only", None,
                                  "file missing on disk",
                                  theirs_b.decode("utf-8"), None))
            continue
        ours = ours_bytes.decode("utf-8")
        theirs_raw = theirs_b.decode("utf-8")
        cache_rel = rec.get("base_cache")
        base_path = (target / cache_rel) if cache_rel else None
        if base_path is None or not base_path.exists():
            # No recoverable base (e.g. a --init-lock migrated tree, I3) ->
            # review-only diff, never a pretended 3-way merge.  Carry
            # theirs_raw so --stage can write the upstream version alongside
            # the on-disk copy for a by-hand merge.
            plans.append(FilePlan(dst, "review-only", None,
                                  "no recoverable base (review-only diff)",
                                  theirs_raw, None))
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

    # New core-like files (#47): core + skills install unconditionally, so a
    # core/skills file present upstream but absent from the lockfile (an
    # adopter whose lockfile predates it -- e.g. the lifecycle skills, added
    # after a pre-skills install) is brought in, not silently omitted. Modules
    # stay opt-in (the new_modules flow below); only the unconditional tier
    # auto-adds. Restricting to the known core/skills mapping set keeps --apply
    # from ever writing a path outside it (plan-review safety note).
    # Key on the *source* template, not the dst: an adopter may have installed a
    # core file under a renamed dst (the vendor wrapper VENDOR.md -> CLAUDE.md,
    # #45), so a src already tracked under any dst is NOT new -- keying on dst
    # would spuriously re-add VENDOR.md alongside the renamed CLAUDE.md.
    lock_srcs = {rec.get("src") for rec in lock.get("files", [])}
    core_like = [(s, d, False) for s, d in _CORE_MAPPINGS] + list(_SKILLS_MAPPINGS)
    seen_new: set[str] = set()
    for src_rel, dst_rel, verbatim in core_like:
        if src_rel in lock_srcs or dst_rel in seen_new:
            continue
        theirs_b = _theirs_bytes(cairn_root, templates_root, src_rel, to_ref)
        if theirs_b is None:
            continue
        seen_new.add(dst_rel)
        if verbatim:
            plans.append(FilePlan(
                dst_rel, "new-core", theirs_b.decode("utf-8", "replace"),
                "new core-like file (added)", None, None,
                src=src_rel, verbatim=True))
        else:
            theirs_raw = theirs_b.decode("utf-8")
            plans.append(FilePlan(
                dst_rel, "new-core", substitute_tokens(theirs_raw, tokens),
                "new core-like file (added)", theirs_raw,
                f"{_BASE_CACHE_REL}/{dst_rel}", src=src_rel, verbatim=False))

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
    current lockfile version/commit?  None if no manifest to check.  Uses the
    shared `_find_manifest_path` (dev/.cairn/ first, legacy dev/strategy/
    fallback) and emits the same migration advisory `init-lock` does."""
    found = _find_manifest_path(target)
    if found is None:
        return None
    manifest, is_legacy = found
    if is_legacy:
        _warn_legacy_manifest_home(manifest)
    text = manifest.read_text(encoding="utf-8", errors="replace")
    commit = str(lock.get("cairn_commit", ""))
    version = str(lock.get("cairn_version", ""))
    return (commit and commit in text) or (version and version in text)


def _print_upgrade_report(
    plans: list[FilePlan], structural: dict[str, Any],
    citation: bool | None, *, mode: str, drift: str | None = None,
) -> None:
    import collections
    by_kind: dict[str, list[str]] = collections.defaultdict(list)
    for fp in plans:
        by_kind[fp.kind].append(fp.dst)
    print(f"\nCairn upgrade -- {mode}\n" + "=" * 40)
    if drift:
        print(f"  {drift}")
    order = ["clean", "clean-locally-modified", "new-core",
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
    # Review-only files owe a by-hand merge: the upgrade is NOT complete until
    # each is reconciled against the new upstream.  Surface them per-file with
    # the reason (not just the summary count) + the concrete next step, so an
    # adopter cannot read "review-only: N" as "done".
    review_only = [fp for fp in plans if fp.kind == "review-only"]
    if review_only:
        print("\n  ⚠ manual merge owed -- the upgrade is NOT complete "
              "until these are reconciled against the new upstream:")
        for fp in review_only:
            print(f"      {fp.dst}: {fp.detail}")
        print(f"  next step: `upgrade --stage` writes each file's upstream "
              f"version (+ your current copy) under "
              f"{_STAGING_REL}/review-only/ for a by-hand merge; `--apply` "
              f"fail-closes until they are reconciled "
              f"(override: --ack-review-only).")


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
    # #47: per-file provenance for files NOT already in the lockfile (new-core),
    # so --apply can append correct lockfile records (refs only -- no file
    # bodies -- keeping stage-metadata.json lightweight, plan-review rec 4b).
    new_entries: dict[str, dict[str, Any]] = {}
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
        if fp.kind == "new-core":
            new_entries[fp.dst] = {
                "src": fp.src, "verbatim": fp.verbatim,
                "base_cache": fp.base_cache,
            }
        # Snapshot the on-disk *ours* hash at stage time (R7a: detect an
        # adopter edit made between --stage and --apply).
        if dst_abs.exists():
            ours_hashes[fp.dst] = "sha256:" + _sha256_hex(dst_abs.read_bytes())
        # Stage the new base-template content (mergeable files only).
        if fp.theirs_raw is not None and fp.base_cache:
            nb = stage / "new-base" / fp.dst
            nb.parent.mkdir(parents=True, exist_ok=True)
            nb.write_text(fp.theirs_raw, encoding="utf-8")
    # Review-only files (no recoverable base / missing on disk) get a by-hand
    # review pair in a SIBLING ``review-only/`` dir -- deliberately NOT under
    # ``files/``, which ``--apply`` swaps onto disk + checks for exactness
    # (placing side-files there would trip that safety gate).  ``.theirs`` is
    # the new upstream; ``.ours`` is the current on-disk copy, omitted when
    # the file is missing on disk (nothing to pair).  ``--apply`` never
    # advances these; the whole stage (incl. ``review-only/``) is rmtree'd on
    # apply.
    review_only_dsts: list[str] = []
    for fp in plans:
        if fp.kind != "review-only":
            continue
        review_only_dsts.append(fp.dst)
        if fp.theirs_raw is not None:
            theirs_out = stage / "review-only" / (fp.dst + ".theirs")
            theirs_out.parent.mkdir(parents=True, exist_ok=True)
            theirs_out.write_text(fp.theirs_raw, encoding="utf-8")
        dst_abs = target / fp.dst
        if dst_abs.exists():
            ours_out = stage / "review-only" / (fp.dst + ".ours")
            ours_out.parent.mkdir(parents=True, exist_ok=True)
            ours_out.write_text(
                dst_abs.read_text(encoding="utf-8"), encoding="utf-8")
    # #48: a verbatim file already byte-identical to the new upstream
    # (verbatim-up-to-date) but whose lockfile hash is stale -- the adopter
    # hand-synced it to a later Cairn before upgrading. Record it so --apply
    # heals the lock hash (no content swap; the file is already correct on
    # disk, so it never enters staged_files / the exactness gate).
    lock_by_dst = {r["dst"]: r for r in lock.get("files", [])}
    verbatim_rehash: list[str] = []
    for fp in plans:
        if fp.kind != "verbatim-up-to-date":
            continue
        rec = lock_by_dst.get(fp.dst)
        dst_abs = target / fp.dst
        if rec is None or not dst_abs.exists():
            continue
        if "sha256:" + _sha256_hex(dst_abs.read_bytes()) != rec.get("hash"):
            verbatim_rehash.append(fp.dst)
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
        # Outstanding by-hand merges: --apply fail-closes on a non-empty list
        # unless --ack-review-only is passed (#44 completion gate).
        "review_only": sorted(review_only_dsts),
        # #47 new core-like files to record in the lockfile on apply (refs only).
        "new_entries": new_entries,
        # #48 verbatim files whose stale lock hash --apply should heal.
        "verbatim_rehash": sorted(verbatim_rehash),
    }
    (stage / _STAGE_META).write_text(
        json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")
    _seed_staging_gitignore(target)
    return stage


def _resolve_vendor_wrapper(
    target: Path, mapped_dsts: set[str],
) -> str | None:
    """Resolve the adopter's renamed vendor wrapper (foldback #45).

    Cairn installs the thin wrapper as ``VENDOR.md`` and the adopter renames it
    to their tool's file (``CLAUDE.md`` etc.), so on a renamed tree the install
    dst ``VENDOR.md`` is missing and the wrapper would drop to untracked.  Two-
    tier resolution (plan-review S1), first hit wins:

    * **Tier 1 (name):** a repo-root file named in ``_KNOWN_VENDOR_WRAPPERS``
      that is not already a mapped core/module dst -> resolved, with **no
      content check** (a heavily customized wrapper may have dropped the
      ``@AGENTS.md`` import line, and the name alone is a strong signal).
    * **Tier 2 (content):** else a repo-root ``*.md`` (not already mapped)
      whose first few lines carry the ``@AGENTS.md`` import -> resolved (a
      custom-named wrapper).

    Returns the repo-root-relative dst, or ``None`` (the caller warns rather
    than silently skipping or recording a wrong file).  The not-already-mapped
    guard (both tiers) is the false-positive backstop."""
    # Tier 1: a known vendor filename at repo root.
    for name in _KNOWN_VENDOR_WRAPPERS:
        if name not in mapped_dsts and (target / name).is_file():
            return name
    # Tier 2: a custom-named root .md importing @AGENTS.md near the top.
    for md in sorted(target.glob("*.md")):
        if md.name in mapped_dsts or not md.is_file():
            continue
        head = md.read_text(encoding="utf-8", errors="replace").splitlines()[:5]
        if any("@AGENTS.md" in line for line in head):
            return md.name
    return None


def _find_manifest_path(target: Path) -> tuple[Path, bool] | None:
    """Locate the adopter's fidelity manifest, searching `dev/.cairn/` first
    (the canonical adoption-state home), then the legacy `dev/strategy/`. Returns
    ``(path, is_legacy)`` or ``None``. The single manifest-finder shared by the
    `cairn_commit` recovery (B1) and the R10 citation check, so the two cannot
    diverge on which file is the manifest."""
    for idx, rel in enumerate(_MANIFEST_SEARCH_DIRS):
        d = target / rel
        if not d.is_dir():
            continue
        cands = sorted(
            {c for c in list(d.glob("*fidelity*")) + list(d.glob("*manifest*"))
             if c.is_file()})
        if cands:
            return cands[0], idx > 0
    return None


def _warn_legacy_manifest_home(manifest: Path) -> None:
    """The shared migration advisory emitted whenever a manifest is found in the
    legacy `dev/strategy/` home (by either the citation check or `init-lock`)."""
    print(f"  [advisory] fidelity manifest found in the legacy `dev/strategy/` "
          f"home ({manifest.name}); move it to `dev/.cairn/` (the adoption-state "
          "home).", file=sys.stderr)


def _manifest_cairn_commit(target: Path) -> str:
    """Best-effort ``cairn_commit`` recovered from the fidelity manifest, or
    ``"unknown"`` (B1: `dev/.cairn/` first, legacy `dev/strategy/` fallback with
    a migration advisory)."""
    found = _find_manifest_path(target)
    if found is None:
        return "unknown"
    path, is_legacy = found
    if is_legacy:
        _warn_legacy_manifest_home(path)
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r'\s*cairn_commit\s*:\s*"?([0-9a-f]{7,40})"?', line)
        if m:
            return m.group(1)
    return "unknown"


def _infer_init_lock_axes(target: Path) -> dict[str, str]:
    """Structurally-inferable axis prefill for `init-lock` (R3 + S1): the axes a
    tree's installed modules / files determine. `size` / `complexity` are human
    judgments, left as placeholders."""
    def _mod(name: str) -> bool:
        return (target / "dev" / "modules" / f"{name}.md").is_file()
    axes: dict[str, str] = {}
    if _mod("dual-review"):
        axes["agent_team"] = "concurrent-multi-type"
    elif _mod("coordination-tiers"):
        axes["agent_team"] = "concurrent-single-type"
    else:
        axes["agent_team"] = "single"
    axes["human_team"] = (
        "small-multi" if (target / "CONTRIBUTING.md").is_file() else "solo")
    axes["language"] = "multi" if _mod("dual-language-tests") else "single"
    axes["age"] = "legacy" if _mod("legacy-agent") else "greenfield"
    return axes


#: Axes `init-lock` cannot structurally infer -- the operator fills these between
#: the two runs (R2). Each placeholder names its allowed values.
_AXIS_PLACEHOLDERS: dict[str, str] = {
    "size": "<small|medium|large>",
    "complexity": "<simple|moderate|complex>",
}
_INIT_LOCK_TOKEN_PLACEHOLDERS: dict[str, str] = {
    "project_name": "<your project name>",
    "test_command": "<your test command, e.g. pytest>",
}


def _resolve_lock_profile_fields(
    cfg: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, str], list[str], dict[str, str]]:
    """From a parsed profile config, build the lockfile ``profile`` block + token
    map, and report *missing* / *invalid* axes (validated against ``_AXES`` --
    S2). Mirrors the install path so a `init-lock`'d lockfile matches a
    `--config` one. Raises ``PresetError`` on an unknown preset."""
    tokens = {k: str(v) for k, v in cfg.items()
              if isinstance(k, str) and k in KNOWN_TOKENS and v}
    if cfg.get("preset"):
        resolved: dict[str, Any] = dict(resolve_axes(str(cfg["preset"]), cfg))
    else:
        resolved = {a: cfg.get(a) for a in _AXES if cfg.get(a) is not None}
    missing = [a for a in _AXES if not resolved.get(a)]
    invalid = {a: str(resolved[a]) for a in _AXES
               if resolved.get(a) is not None and str(resolved[a]) not in _AXES[a]}
    lock_profile: dict[str, Any] = {
        "preset": cfg.get("preset"),
        "axes": {a: resolved[a] for a in _AXES if resolved.get(a) is not None},
    }
    return lock_profile, tokens, missing, invalid


def _write_init_lock_profile_template(target: Path) -> int:
    """First `init-lock` run with no committed config: write a
    ``dev/.cairn/profile.yml`` prefilled with the structurally-inferable axes +
    placeholders for the rest, then **fail loud** (exit non-zero, no lockfile) so
    the operator completes it and re-runs (R2 step 1)."""
    profile_path = target / _PROFILE_REL
    inferred = _infer_init_lock_axes(target)
    modules = sorted(m for m in _MODULE_MAPPINGS
                     if (target / "dev" / "modules" / f"{m}.md").is_file())
    lines = [
        "# Cairn install-config (profile.yml).",
        "# Materialized by `upgrade --init-lock`: structurally-inferable axes are",
        "# prefilled; replace every <...> placeholder with a real value, then",
        "# re-run `upgrade --init-lock` to write the lockfile.",
        "",
        f'project_name: "{_INIT_LOCK_TOKEN_PLACEHOLDERS["project_name"]}"',
        f'test_command: "{_INIT_LOCK_TOKEN_PLACEHOLDERS["test_command"]}"',
        "",
        "# Six-axis dimension profile (all required):",
    ]
    for a in _AXES:
        if a in inferred:
            lines.append(f"{a}: {inferred[a]}")
        else:
            lines.append(f"{a}: {_AXIS_PLACEHOLDERS[a]}")
    lines += ["", "# Installed modules (inferred from dev/modules/):", "modules:"]
    lines += [f"  - {m}" for m in modules]
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    profile_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    n_ph = len(_AXIS_PLACEHOLDERS) + len(_INIT_LOCK_TOKEN_PLACEHOLDERS)
    print(
        f"Wrote {_PROFILE_REL}: {len(inferred)} axis(es) inferred, {n_ph} "
        "placeholder(s) to fill (project_name, test_command, "
        f"{', '.join(_AXIS_PLACEHOLDERS)}).\n"
        "  Replace every <...> value, then re-run `upgrade --init-lock`. "
        "No lockfile was written (fail-with-template).",
        file=sys.stderr,
    )
    return 2


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
    # Arm A (init-lock-full-profile): resolve the full six-axis profile + tokens
    # so the synthesized lockfile is never a gating-only stub. With no committed
    # config, fail-with-template (R2); with one, validate it (S2) before use.
    profile_path = target / _PROFILE_REL
    if not profile_path.is_file():
        return _write_init_lock_profile_template(target)
    try:
        cfg = load_config(profile_path)
    except Exception as exc:  # noqa: BLE001 -- surface any YAML/read error
        print(f"error loading {_PROFILE_REL}: {exc}", file=sys.stderr)
        return 1
    try:
        lock_profile, tokens, missing, invalid = _resolve_lock_profile_fields(cfg)
    except PresetError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    placeholder_tokens = sorted(
        k for k, v in tokens.items()
        if v.strip().startswith("<") and v.strip().endswith(">"))
    if missing or invalid or placeholder_tokens:
        parts: list[str] = []
        if missing:
            parts.append(f"missing axis(es): {', '.join(missing)}")
        if invalid:
            parts.append("invalid axis value(s): " + ", ".join(
                f"{a}={v!r} (allowed: {'/'.join(_AXES[a])})"
                for a, v in invalid.items()))
        if placeholder_tokens:
            parts.append(
                f"unfilled placeholder(s): {', '.join(placeholder_tokens)}")
        print(f"error: {_PROFILE_REL} is incomplete -- " + "; ".join(parts) +
              ".\n  Fill every value (axes validated against their allowed "
              "values), then re-run `upgrade --init-lock`.", file=sys.stderr)
        return 1
    # cairn_commit recovery (B1: dev/.cairn/ first, legacy dev/strategy/ fallback).
    commit = _manifest_cairn_commit(target)
    records: list[dict[str, Any]] = []
    classification: dict[str, list[str]] = {"verbatim": [], "unrecoverable-base": []}
    entries = _lock_file_list(list(_MODULE_MAPPINGS), [])
    mapped_dsts = {dst for _src, dst, _vb in entries}
    for src_rel, dst_rel, verbatim in entries:
        dst_abs = target / dst_rel
        if not dst_abs.exists():
            # The vendor wrapper installs as VENDOR.md but the adopter renames
            # it to their tool's file (#45).  Follow the rename so it stays
            # tracked + 3-way merges later, instead of dropping it to untracked.
            if src_rel == "core/VENDOR.md":
                resolved = _resolve_vendor_wrapper(target, mapped_dsts)
                if resolved is None:
                    print(f"  [warn] vendor wrapper {dst_rel} installed but no "
                          "renamed wrapper found at repo root (a known vendor "
                          f"filename {', '.join(_KNOWN_VENDOR_WRAPPERS)}, or a "
                          "root *.md importing @AGENTS.md) -- it will be "
                          "untracked. Rename it to a known vendor filename or "
                          "re-install from an upgrade-capable Cairn.",
                          file=sys.stderr)
                    continue
                dst_rel = resolved
                dst_abs = target / dst_rel
            else:
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
        "profile": lock_profile, "modules": sorted(
            m for m in _MODULE_MAPPINGS
            if (target / "dev" / "modules" / f"{m}.md").exists()),
        "optional_templates": [], "tokens": dict(tokens), "files": records,
    }
    lock_path = target / _LOCKFILE_REL
    lock_path.parent.mkdir(parents=True, exist_ok=True)
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


def _cmd_adopt_module(
    target: Path, name: str, cairn_root: Path, templates_root: Path,
) -> int:
    """`upgrade --adopt-module <name>` (#49): record an already-on-disk opt-in
    module into the lockfile so it 3-way-merges on later upgrades.

    Explicit, never automatic (modules are a deliberate choice -- the opt-in
    contrast to #47's auto-add of the unconditional core/skills tier). For each
    of the module's ``InstallSpec``s it records a lockfile ``files`` entry
    exactly as ``init`` would (``src``/``dst``/``verbatim``, on-disk ``hash``;
    non-verbatim -> ``base_cache`` raw template + ``base_hash``), installing a
    spec's ``dst`` from the template first only if it is missing on disk. Adds
    the module to ``modules`` and seeds its ``.gitignore`` entries. Fail-closed
    on an unknown name; a no-op if the module is already locked."""
    lock = read_lockfile(target)
    if lock is None:
        print(f"error: no {_LOCKFILE_REL} in the target; run "
              "`upgrade --init-lock` (or a clean install) first.",
              file=sys.stderr)
        return 1
    if name not in _MODULE_MAPPINGS:
        print(f"error: unknown module {name!r}. Known modules: "
              f"{', '.join(sorted(_MODULE_MAPPINGS))}.", file=sys.stderr)
        return 1
    if name in lock.get("modules", []):
        print(f"  [info] module {name!r} is already recorded in "
              f"{_LOCKFILE_REL}; nothing to adopt.", file=sys.stderr)
        return 0

    tokens = {str(k): str(v) for k, v in (lock.get("tokens") or {}).items()}
    lock_dsts = {rec["dst"] for rec in lock.get("files", [])}
    new_files = [dict(rec) for rec in lock.get("files", [])]
    added: list[str] = []
    for spec in _MODULE_MAPPINGS[name]:
        src_rel = f"modules/{spec.src}"        # lockfile src convention
        dst_rel = spec.dst
        if dst_rel in lock_dsts:
            continue  # already tracked under another roster entry; skip the file
        theirs_b = _theirs_bytes(cairn_root, templates_root, src_rel, None)
        if theirs_b is None:
            print(f"error: upstream template {src_rel!r} for module {name!r} "
                  "not found.", file=sys.stderr)
            return 1
        dst_abs = target / dst_rel
        if not dst_abs.exists():
            # Adoption is for an already-present module; install a missing spec
            # dst from the template (substituted for mergeable, raw for verbatim)
            # exactly as `init` would, so a partially-placed module completes.
            _assert_safe_write(dst_abs, target)
            dst_abs.parent.mkdir(parents=True, exist_ok=True)
            content = (theirs_b.decode("utf-8", "replace") if spec.verbatim
                       else substitute_tokens(theirs_b.decode("utf-8"), tokens))
            dst_abs.write_text(content, encoding="utf-8")
        rec: dict[str, Any] = {
            "src": src_rel, "dst": dst_rel, "verbatim": bool(spec.verbatim),
            "hash": "sha256:" + _sha256_hex(dst_abs.read_bytes()),
        }
        if not spec.verbatim:
            base_rel = f"{_BASE_CACHE_REL}/{dst_rel}"
            base_abs = target / base_rel
            _assert_safe_write(base_abs, target)
            base_abs.parent.mkdir(parents=True, exist_ok=True)
            base_abs.write_bytes(theirs_b)     # raw template (pre-substitution)
            rec["base_cache"] = base_rel
            rec["base_hash"] = "sha256:" + _sha256_hex(theirs_b)
        new_files.append(rec)
        added.append(dst_rel)

    lock["files"] = new_files
    lock["modules"] = sorted(set(lock.get("modules", [])) | {name})
    (target / _LOCKFILE_REL).parent.mkdir(parents=True, exist_ok=True)
    (target / _LOCKFILE_REL).write_text(_emit_lock_yaml(lock), encoding="utf-8")
    seeded = seed_gitignore(target, _GITIGNORE_SEEDS.get(name, ()))
    note = f"; seeded .gitignore: {', '.join(seeded)}" if seeded else ""
    print(f"Adopted module {name!r}: recorded {len(added)} file(s) in "
          f"{_LOCKFILE_REL}{note}.")
    return 0


def _cmd_finalize_lockfile(target: Path, lock: dict[str, Any]) -> int:
    """`upgrade --finalize`: advance each record's ``hash`` to the adopter's
    *committed on-disk* content, so ``verify_integrity`` attests the customized
    tree the adopter actually ships -- filled slots, the ``VENDOR.md ->
    CLAUDE.md`` wrapper rename, project-owned forks -- rather than the pristine
    clean-install state no real adopter keeps.  This is the step that makes a
    *customized* install verifiable (R10): without it, every slot fill and
    wrapper rename reads as integrity tampering.

    The upgrade ancestor is left untouched: ``base_cache`` / ``base_hash`` (the
    clean-install baseline the 3-way merge + ``classify_verbatim`` fork
    detection use) are preserved.  For a verbatim record predating ``base_hash``,
    the current ``hash`` (the as-shipped baseline) is copied into ``base_hash``
    *before* ``hash`` is advanced, so fork detection survives.  A renamed vendor
    wrapper's record ``dst`` is resolved to the on-disk wrapper (#45) so
    integrity checks the real file, not the absent ``VENDOR.md``.  Idempotent.
    Fail-closed: a tracked file missing on disk aborts (never silently drop a
    file from the integrity set)."""
    files = lock.get("files") or []
    mapped = {r.get("dst") for r in files}
    changed = 0
    missing: list[str] = []
    for rec in files:
        dst_rel = rec.get("dst")
        if not isinstance(dst_rel, str) or not dst_rel:
            continue
        # Resolve a renamed vendor wrapper: the lockfile records VENDOR.md but
        # the adopter renamed it (CLAUDE.md, ...).
        if rec.get("src") == "core/VENDOR.md" and not (target / dst_rel).is_file():
            resolved = _resolve_vendor_wrapper(target, mapped)
            if resolved is not None:
                rec["dst"] = dst_rel = resolved
        dst_abs = target / dst_rel
        if not dst_abs.is_file():
            missing.append(dst_rel)
            continue
        if dst_rel in _LIVING_STATE_DSTS:
            # Adopter-authored project state: tracked for upgrade but excluded
            # from the verify_integrity tamper check. Stamp the flag (this
            # migrates pre-living_state lockfiles) and skip the hash advance --
            # the hash is unused for these records, so don't churn it.
            rec["living_state"] = True
            continue
        # Preserve the as-shipped baseline before advancing hash, for verbatim
        # records that predate base_hash.
        if rec.get("verbatim") and not rec.get("base_hash"):
            rec["base_hash"] = rec.get("hash", "")
        new_hash = "sha256:" + _sha256_hex(dst_abs.read_bytes())
        if new_hash != rec.get("hash"):
            changed += 1
        rec["hash"] = new_hash
    if missing:
        print(f"error: {len(missing)} tracked file(s) missing on disk -- cannot "
              f"finalize (fix or re-install first):\n  " + "\n  ".join(missing),
              file=sys.stderr)
        return 1
    (target / _LOCKFILE_REL).parent.mkdir(parents=True, exist_ok=True)
    (target / _LOCKFILE_REL).write_text(_emit_lock_yaml(lock), encoding="utf-8")
    print(f"Finalized {_LOCKFILE_REL}: advanced {changed} hash(es) to the "
          f"committed on-disk content. `verify_integrity` now attests this tree "
          f"(the base cache / upgrade ancestor is unchanged).")
    return 0


def _dirty_tracked_paths(target: Path) -> set[str] | None:
    """The set of **tracked, uncommitted** paths in ``target`` (repo-root
    relative), or ``None`` when ``target`` is not a git work tree / git is
    absent (fail-soft: no guard when the tree cannot be read).

    Untracked (``??``) and ignored (``!!``) entries are **excluded** -- the
    Layer-3 dirty-tree guard (#56) is keyed on the upgrade write-set, and a
    guard that tripped on scratch or gitignored files would false-positive
    (the proposal's "signals wrong"). Both sides of a rename
    (``R  old -> new``) are reported -- either colliding with the write-set
    is a real overwrite hazard.
    """
    import subprocess

    def _git(*args: str) -> subprocess.CompletedProcess[str] | None:
        try:
            return subprocess.run(
                ["git", "-C", str(target), *args],
                capture_output=True, text=True, timeout=10, check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return None

    inside = _git("rev-parse", "--is-inside-work-tree")
    if inside is None or inside.returncode != 0 \
            or inside.stdout.strip() != "true":
        return None  # not a checkout / git absent -- no guard
    status = _git("status", "--porcelain")
    if status is None or status.returncode != 0:
        return None

    def _unquote(p: str) -> str:
        return p[1:-1] if len(p) >= 2 and p[0] == '"' and p[-1] == '"' else p

    dirty: set[str] = set()
    for line in status.stdout.splitlines():
        if len(line) < 4:
            continue
        code = line[:2]
        if code in ("??", "!!"):
            continue  # untracked / ignored -- benign dirt
        path = line[3:]
        if " -> " in path:  # rename / copy: both sides count
            old, new = path.split(" -> ", 1)
            dirty.add(_unquote(old))
            dirty.add(_unquote(new))
        else:
            dirty.add(_unquote(path))
    return dirty


def _writeset_dirty_collisions(
    target: Path, staged_files: list[str],
) -> list[str]:
    """The sorted intersection of the upgrade write-set (``staged_files``) with
    the target's tracked-uncommitted paths. Empty when the tree is clean, the
    write-set is disjoint from the dirt, or the tree is unreadable
    (fail-soft)."""
    dirty = _dirty_tracked_paths(target)
    if not dirty:
        return []
    return sorted(set(staged_files) & dirty)


def _apply_upgrade(
    target: Path, lock: dict[str, Any], cairn_root: Path, templates_root: Path,
    *, ack_review_only: bool = False, force: bool = False,
) -> int:
    """`--apply` (R7): consume the staged result under the safety contract,
    swap the originals, **advance the lockfile + base cache** to the new
    version, and clean the stage.  Fail-closed at every gate.

    ``ack_review_only`` (the ``--ack-review-only`` flag) is the explicit
    override for the #44 completion gate: ``--apply`` refuses to advance the
    lockfile while files still owe a by-hand merge unless the adopter
    acknowledges them.

    ``force`` (the ``--force`` flag) overrides the Layer-3 dirty-tree guard
    (#56): ``--apply`` refuses when its write-set would overwrite a tracked
    file the adopter has uncommitted edits in (a concurrent session's
    in-flight work)."""
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
    # (d2) #44 completion gate: outstanding review-only files owe a by-hand
    #      merge.  Fail-closed (mirrors the conflict-marker gate) unless the
    #      adopter explicitly acknowledges with --ack-review-only -- so a
    #      --stage -> --apply cannot advance the lockfile to the new version
    #      while customized doctrine silently never landed (the LHM failure).
    review_only = meta.get("review_only", [])
    if review_only and not ack_review_only:
        print("error: the upgrade is not complete -- "
              f"{len(review_only)} file(s) owe a by-hand merge and were not "
              "reconciled:\n  " + "\n  ".join(review_only) +
              f"\n  review the .theirs/.ours pair under {_STAGING_REL}/"
              "review-only/, merge by hand into the original, then re-run "
              "`--apply --ack-review-only` to acknowledge.", file=sys.stderr)
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

    # (f) Layer-3 dirty-tree guard (#56): refuse to overwrite a tracked path
    #     the adopter has uncommitted edits in -- applying would clobber a
    #     concurrent session's in-flight work. Scoped to tracked paths (benign
    #     untracked / gitignored dirt does not trip it); --force overrides.
    if not force:
        collide = _writeset_dirty_collisions(target, staged_meta)
        if collide:
            print(
                f"error: refusing --apply: it would overwrite {len(collide)} "
                "tracked file(s) with uncommitted changes:\n  "
                + "\n  ".join(collide) +
                "\n  commit or stash them first, or re-run `--apply --force` "
                "to overwrite.", file=sys.stderr)
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
    rehash_set = set(meta.get("verbatim_rehash", []))
    for rec in lock.get("files", []):
        rec = dict(rec)
        # Renamed vendor wrapper (#45): _compute_upgrade staged the *resolved*
        # wrapper (e.g. CLAUDE.md), but this record still names the canonical
        # VENDOR.md. Rewrite the dst to the on-disk wrapper so the advanced
        # lockfile points at the file that exists -- otherwise --apply leaves a
        # dangling VENDOR.md record and verify_integrity fails.
        if rec.get("src") == "core/VENDOR.md" and rec["dst"] not in staged_set \
                and not (target / rec["dst"]).is_file():
            resolved = _resolve_vendor_wrapper(
                target, {r["dst"] for r in lock.get("files", [])})
            if resolved is not None:
                rec["dst"] = resolved
        if rec["dst"] in staged_set:
            rec["hash"] = "sha256:" + _sha256_hex((target / rec["dst"]).read_bytes())
            if rec.get("base_cache"):
                cache_abs = target / rec["base_cache"]
                if cache_abs.exists():
                    rec["base_hash"] = \
                        "sha256:" + _sha256_hex(cache_abs.read_bytes())
        elif rec["dst"] in rehash_set and (target / rec["dst"]).exists():
            # #48: heal a stale verbatim hash whose on-disk content already
            # equals the new upstream (no content swap -- recompute on disk).
            rec["hash"] = "sha256:" + _sha256_hex((target / rec["dst"]).read_bytes())
        new_files.append(rec)
    # #47: append lockfile records for new core-like files added this upgrade
    # (auto-added; src/verbatim/base_cache carried through stage metadata).
    new_entries = meta.get("new_entries", {})
    added_dsts = [d for d in sorted(new_entries) if d in staged_set]
    for dst in added_dsts:
        info = new_entries[dst]
        rec = {"src": info["src"], "dst": dst,
               "verbatim": bool(info.get("verbatim")),
               "hash": "sha256:" + _sha256_hex((target / dst).read_bytes())}
        if info.get("base_cache"):
            rec["base_cache"] = info["base_cache"]
            cache_abs = target / info["base_cache"]
            if cache_abs.exists():
                rec["base_hash"] = "sha256:" + _sha256_hex(cache_abs.read_bytes())
        new_files.append(rec)
    new_lock["files"] = new_files
    (target / _LOCKFILE_REL).parent.mkdir(parents=True, exist_ok=True)
    (target / _LOCKFILE_REL).write_text(_emit_lock_yaml(new_lock), encoding="utf-8")

    # #47: a newly-added skill needs its vendor fan-out (e.g. .claude/skills ->
    # the canonical .agents/skills) + its machine-state .gitignore seeds, just
    # as a fresh install does. Fan-out is best-effort: a containment refusal
    # warns rather than aborting the already-applied upgrade.
    added_skills = [d for d in added_dsts if d.startswith(".agents/skills/")]
    if added_skills:
        try:
            fan_out_skills(templates_root, target)
        except Exception as exc:  # noqa: BLE001 -- containment/vendor edge
            print(f"  [warn] skills fan-out skipped: {exc}", file=sys.stderr)
        seeded = seed_gitignore(target, _SKILLS_GITIGNORE)
        if seeded:
            print(f"  Seeded .gitignore (skills): {', '.join(seeded)}")

    shutil.rmtree(stage)
    added_note = f" (+{len(added_dsts)} new core-like)" if added_dsts else ""
    print(f"Applied {len(staged_meta)} file(s){added_note}; advanced "
          f"{_LOCKFILE_REL} + the base cache to {new_lock['cairn_commit']}.")
    return 0


def _yaml_sq(v: str) -> str:
    """A YAML single-quoted scalar (doubling any embedded single quote) --
    always valid, and safe for values carrying double quotes / shell syntax
    (e.g. a `test_command`)."""
    return "'" + str(v).replace("'", "''") + "'"


def _self_heal_profile_config(target: Path, lock: dict[str, Any]) -> bool:
    """R1: if `dev/.cairn/profile.yml` is absent but the lockfile carries a
    non-empty profile, materialize the committed config from the lockfile --
    **merging the lockfile `tokens` (project_name, test_command, ...) with the
    `profile` axes/preset (B1)** so the written config is complete and
    re-loadable. Only-when-absent (never clobbers an existing config). Returns
    True iff it wrote one.

    Called on ``--apply`` only -- never ``--stage`` (a non-mutating preview).
    The materialized file is a single new path outside the upgrade's staged
    write-set, so the #56 dirty-tree guard never refuses it."""
    profile_path = target / _PROFILE_REL
    if profile_path.exists():
        return False
    profile = lock.get("profile") or {}
    axes = profile.get("axes") or {}
    if not axes:
        return False  # gating-only / empty lockfile profile -- nothing to heal
    tokens = lock.get("tokens") or {}
    lines = [
        "# Cairn install-config (profile.yml).",
        "# Self-healed by `upgrade` from the lockfile profile: this adopter was",
        "# init-lock'd before profile.yml was materialized. Edit THIS file to",
        "# change the profile, then regenerate the lockfile.",
        "",
    ]
    for key in ("project_name", "test_command", "claim_check_command",
                "metrics_command"):
        if tokens.get(key):
            lines.append(f"{key}: {_yaml_sq(tokens[key])}")
    lines.append("")
    if profile.get("preset"):
        lines.append(f"preset: {profile['preset']}")
    for a in _AXES:
        if axes.get(a):
            lines.append(f"{a}: {axes[a]}")
    modules = lock.get("modules") or []
    if modules:
        lines += ["", "modules:"] + [f"  - {m}" for m in modules]
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    profile_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  [self-heal] materialized {_PROFILE_REL} from the lockfile profile "
          "(this adopter predates the committed config; edit it to change the "
          "profile, then regenerate the lockfile).", file=sys.stderr)
    return True


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
    p.add_argument("--finalize", action="store_true",
                   help="Advance each record's hash to the committed on-disk "
                        "content so verify_integrity attests a *customized* "
                        "install (filled slots, wrapper rename, forks). The "
                        "base cache / upgrade ancestor is left unchanged.")
    p.add_argument("--plan", action="store_true",
                   help="Read-only: classify drift, write nothing (default).")
    p.add_argument("--stage", action="store_true",
                   help="Write the staged review surface (no swap).")
    p.add_argument("--apply", action="store_true",
                   help="Apply a previously-staged, resolved upgrade.")
    p.add_argument("--ack-review-only", action="store_true",
                   help="Acknowledge outstanding review-only files so --apply "
                        "proceeds (the #44 completion gate is fail-closed "
                        "without this).")
    p.add_argument("--force", action="store_true",
                   help="Override the Layer-3 dirty-tree guard (#56): apply "
                        "even when the write-set overlaps tracked files with "
                        "uncommitted changes (they will be overwritten).")
    p.add_argument("--adopt-module", default=None, metavar="NAME",
                   help="Record an already-on-disk opt-in module NAME into the "
                        "lockfile so it 3-way-merges on later upgrades (#49). "
                        "Explicit, never automatic -- a module is a deliberate "
                        "choice.")
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

    if args.adopt_module:
        return _cmd_adopt_module(
            target, args.adopt_module, cairn_root, templates_root)

    lock = read_lockfile(target)
    if lock is None:
        print(f"error: no {_LOCKFILE_REL} in the target. Run "
              "`upgrade --init-lock --target <repo>` to migrate a "
              "pre-lockfile tree first.", file=sys.stderr)
        return 1

    if args.finalize:
        return _cmd_finalize_lockfile(target, lock)

    if args.to is not None and not _cairn_is_git(cairn_root):
        print("error: --to <ref> needs a git-checkout Cairn source; a "
              "packaged release can upgrade only to the currently-running "
              "tree (omit --to).", file=sys.stderr)
        return 1

    # R1 self-heal (--apply only -- NOT --stage, which is a non-mutating preview
    # that writes solely to the gitignored review surface; and never on the
    # read-only --plan): an already-init-lock'd adopter may carry a populated
    # lockfile profile but no committed dev/.cairn/profile.yml. Materialize it
    # from the lockfile so the config you edit exists. Only-when-absent;
    # composes with the #56 guard.
    if args.apply:
        _self_heal_profile_config(target, lock)

    if args.apply:
        return _apply_upgrade(target, lock, cairn_root, templates_root,
                              ack_review_only=args.ack_review_only,
                              force=args.force)

    plans, structural = _compute_upgrade(
        target, cairn_root, templates_root, lock, args.to)
    citation = _citation_ok(target, lock)
    # #54 adoption->canonical drift surfacing (informational; never blocks).
    drift = _behind_by_n(
        cairn_root, lock.get("cairn_commit"),
        args.to or _cairn_commit(cairn_root))

    if args.stage:
        stage = _write_stage(target, plans, lock, args.to, cairn_root)
        _print_upgrade_report(plans, structural, citation, mode="stage",
                              drift=drift)
        # (R1) --stage writes only the gitignored review surface, so it
        # *completes* even on a dirty tree -- but advise when the write-set
        # overlaps a tracked uncommitted path so the eventual --apply refusal
        # is no surprise.
        try:
            import json as _json
            _meta = _json.loads(
                (stage / _STAGE_META).read_text(encoding="utf-8"))
            _collide = _writeset_dirty_collisions(
                target, _meta.get("staged_files", []))
        except (OSError, ValueError):
            _collide = []
        if _collide:
            print(
                f"\n  [advisory] {len(_collide)} staged file(s) overlap "
                "tracked uncommitted changes; --apply will refuse until they "
                "are committed/stashed (or pass --force):\n    "
                + "\n    ".join(_collide), file=sys.stderr)
        print(f"\nStaged under {_STAGING_REL}/ . Resolve any conflicts, then "
              "`upgrade --apply --target <repo>`.")
        return 0

    # Default: --plan (strictly read-only).
    _print_upgrade_report(plans, structural, citation,
                          mode="plan (read-only)", drift=drift)
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
        print(
            "[dry-run] Skills:          "
            "tools/lifecycle.py + .agents/skills/{session-start,session-end}/"
            "SKILL.md (+ untracked dev/.cairn/local-env.json)"
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

    # Install lifecycle-routine skills (unconditional, like core) + write the
    # untracked interpreter binding (resolve-don't-bake).
    print("Installing lifecycle skills ...")
    skills_results = install_skills(
        templates_root, target, tokens, force=args.force
    )
    _n_skills = sum(
        1 for _s, d, _v in _SKILLS_MAPPINGS if d.endswith("/SKILL.md")
    )
    print(
        f"  Installed {_n_skills} lifecycle skill(s) -> .agents/skills/ "
        f"(+ the tools/lifecycle.py CLI). Try `session-start` (/good-morning)."
    )
    env_result = write_local_env(target, force=args.force)
    if env_result[3] == "installed":
        print(f"  Wrote interpreter binding: {env_result[0]} (untracked)")
    # Fan the canonical skills out to in-use vendor read-paths (symlink, or a
    # gitignored generated copy where symlinks are unavailable).  A containment
    # violation here is reported as a crisp non-zero exit, not a traceback
    # (Codex P1#2); local-env.json is already gitignored by this point.
    try:
        fanout = fan_out_skills(templates_root, target, force=args.force)
    except ScaffoldSecurityError as exc:
        print(f"error: skills fan-out refused (containment): {exc}",
              file=sys.stderr)
        return 2
    for name, tier, status in fanout:
        if status not in ("noop", "skipped-vendor-absent"):
            print(f"  Skills fan-out [{tier}] {name}: {status}")

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
        core_results + skills_results + onboarding_results + module_results
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

    # Seed the lifecycle skills' machine-state .gitignore entries
    # (unconditional -- the skills always install): the untracked interpreter
    # binding + the full-handoff lock.
    skills_ignored = seed_gitignore(target, _SKILLS_GITIGNORE)
    if skills_ignored:
        print(f"\nSeeded .gitignore (skills): {', '.join(skills_ignored)}")

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
    # ancestor anchor (dev/.cairn/cairn-lock.yml + dev/.cairn/base/).  Fail-closed
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
