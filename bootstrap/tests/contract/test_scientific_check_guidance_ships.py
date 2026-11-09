# SPDX-License-Identifier: MIT
"""Keep the acceptance-template machine slot available to the installer."""
from pathlib import Path

from bootstrap import scaffold


CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_PLAN_TEMPLATES = (
    "dev/plans/_template.md",
    "templates/core/dev/plans/_template.md",
)
_ACCEPTANCE_SLOT = "acceptance-doc-tooling"


def test_the_check_guidance_reaches_every_copy_and_promise_site() -> None:
    """The public slot parser finds one acceptance-doc-tooling slot per copy."""
    for rel in _PLAN_TEMPLATES:
        text = (CAIRN_ROOT / rel).read_text(encoding="utf-8")
        slots = scaffold.parse_slots(text)
        count = sum(slot.name == _ACCEPTANCE_SLOT for slot in slots)
        assert count == 1, (
            f"{rel} must contain one {_ACCEPTANCE_SLOT!r} slot; found {count}")
