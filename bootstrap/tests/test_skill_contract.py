"""Contract tests for the canonical SKILL.md sources (Chunk 3 of the executing
plan `2026-06-01-claude-cairn-vendor-neutral-skills`).

Every lifecycle SKILL.md must:

* carry the agentskills.io frontmatter floor -- ``name`` + ``description`` --
  with ``name`` matching its directory;
* carry ``disable-model-invocation: true`` (Layer-1 best-effort manual-only);
* carry a canonical pointer to ``doctrine/session-routines.md`` (the body
  orchestrates the doctrine, it does not restate it -- the VENDOR.md drift-guard
  applied to procedures);
* keep its body under the 200-line threshold (II4a) -- a body that restated the
  routine's rationale would blow this budget, so the threshold *is* the
  enforceable half of the no-restate guard;
* carry a dry, anti-semantic ``description`` -- it names the routine as
  manual and explicitly *not* a conversational helper, so a harness that
  auto-triggers by description does not fire the lifecycle from chatter.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_skill_contract.py
"""
from __future__ import annotations

from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
SKILLS_ROOT = CAIRN_ROOT / "templates" / "skills"

#: The body-length ceiling (frontmatter excluded), per plan obligation II4a.
BODY_LINE_THRESHOLD = 200

EXPECTED_SKILLS = {"session-start", "session-end"}

pytestmark = pytest.mark.skipif(
    not SKILLS_ROOT.exists(), reason="templates/skills not available"
)


def _skill_files() -> list[Path]:
    return sorted(SKILLS_ROOT.glob("*/SKILL.md"))


def _split_frontmatter(text: str) -> tuple[dict, str]:
    """Parse the leading ``---`` YAML-ish frontmatter without a yaml dep.

    Returns (mapping, body).  Only the flat ``key: value`` floor is needed for
    the contract; values keep their raw string form.
    """
    lines = text.splitlines()
    assert lines and lines[0].strip() == "---", "missing opening frontmatter fence"
    meta: dict[str, str] = {}
    body_start = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            body_start = i + 1
            break
        if ":" in lines[i]:
            key, value = lines[i].split(":", 1)
            meta[key.strip()] = value.strip()
    assert body_start is not None, "missing closing frontmatter fence"
    body = "\n".join(lines[body_start:])
    return meta, body


def test_expected_skills_present():
    found = {p.parent.name for p in _skill_files()}
    assert EXPECTED_SKILLS <= found, f"missing skills: {EXPECTED_SKILLS - found}"


@pytest.mark.parametrize("skill", sorted(_skill_files()), ids=lambda p: p.parent.name)
def test_skill_contract(skill: Path):
    meta, body = _split_frontmatter(skill.read_text(encoding="utf-8"))

    # Frontmatter floor + name matches the directory.
    assert meta.get("name") == skill.parent.name
    assert meta.get("description", "").strip(), "description must be non-empty"

    # Manual-only Layer-1 flag.
    assert meta.get("disable-model-invocation", "").lower() == "true"

    # Canonical doctrine pointer (orchestrates, does not restate).
    assert "doctrine/session-routines.md" in body

    # Project-owned routine-customization pointer (the custom_session_routines.md
    # convention). A literal-string well-formedness contract for THIS pointer:
    # catches a typo'd path that an installed==template integrity check would pass
    # consistently -- the failure class the convention itself was created to fix.
    assert "dev/rules/custom_session_routines.md" in body, (
        f"{skill.parent.name} must carry the project-owned routine-customization "
        "pointer 'dev/rules/custom_session_routines.md'"
    )

    # Body under threshold (the enforceable half of the no-restate drift-guard).
    body_lines = len(body.splitlines())
    assert body_lines < BODY_LINE_THRESHOLD, (
        f"{skill.parent.name} body is {body_lines} lines "
        f"(>= {BODY_LINE_THRESHOLD}); it may be restating doctrine."
    )

    # Anti-semantic description: names itself manual + not-conversational so
    # a description-triggering harness does not fire it from chatter.
    desc = meta["description"].lower()
    assert "manual" in desc
    assert "not a conversational helper" in desc


@pytest.mark.parametrize("skill", sorted(_skill_files()), ids=lambda p: p.parent.name)
def test_no_dead_alias_prose(skill: Path):
    # #51: a "Friendly alias: /goodnight" line is non-functional prose -- only
    # the skill's directory name registers a command. It misleads operators into
    # typing a command that does not exist, so it must not ship.
    _meta, body = _split_frontmatter(skill.read_text(encoding="utf-8"))
    assert "Friendly alias" not in body, (
        f"{skill.parent.name}: ships a non-functional '/...' alias in prose")


def test_session_end_plumbs_arguments():
    # #51: $ARGUMENTS in the body routes flags (e.g. /session-end --handoff) to
    # the CLI deterministically; without it, the flag is silently dropped.
    _meta, body = _split_frontmatter(
        (SKILLS_ROOT / "session-end" / "SKILL.md").read_text(encoding="utf-8"))
    assert "$ARGUMENTS" in body, (
        "session-end must $ARGUMENTS-plumb so /session-end --handoff routes "
        "the flag to tools/lifecycle.py")
