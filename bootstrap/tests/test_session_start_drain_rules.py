"""The session-start skill passes the user's arguments on, so ``--drain`` reaches it.

``/session-start --drain`` lets an agent edit and commit while reading issue
text that anyone can write. The skill is instructions for an agent and no test
can drive one, so this file checks only what the harness reads mechanically:
the ``$ARGUMENTS`` placeholder. The other drain-safety rules (issue text is
data, no ``gh`` command that writes to an issue, a number names an issue, an
unknown target stops the run, the skill's own triage) are instruction prose;
review of the skill text protects them, not this test.

Promises:
- The session-start skill receives the arguments a user passes, so a --drain
  flag is never silently dropped.

Run from the cairn repo root:
    python -m pytest bootstrap/tests/test_session_start_drain_rules.py
"""
from __future__ import annotations

from pathlib import Path

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
SKILL = CAIRN_ROOT / "templates" / "skills" / "session-start" / "SKILL.md"


def test_the_skill_keeps_its_drain_safety_rules():
    text = SKILL.read_text(encoding="utf-8")

    assert "$ARGUMENTS" in text, (
        "without $ARGUMENTS the skill never sees --drain; the flag is dropped")
