# SPDX-License-Identifier: MIT
"""Keep own and shipped template sections aligned and their slot intact."""
from pathlib import Path


CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent.parent

_SECTION_COPIES = (
    (
        "## Security preflight",
        "dev/proposals/_template.md",
        "templates/core/dev/proposals/_template.md",
    ),
    (
        "## Acceptance criteria",
        "dev/plans/_template.md",
        "templates/core/dev/plans/_template.md",
    ),
)

_ACCEPTANCE_SLOT = (
    "<!-- cairn:slot acceptance-doc-tooling -->",
    "<!-- cairn:end acceptance-doc-tooling -->",
)


def _section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line == heading), None)
    assert start is not None, f"missing template section {heading!r}"
    end = next(
        (i for i in range(start + 1, len(lines))
         if lines[i].startswith("## ")),
        len(lines),
    )
    return chr(10).join(lines[start:end])


def test_the_check_guidance_reaches_every_copy_and_promise_site() -> None:
    """Paired sections stay equal without fixing their human-facing wording."""
    sections: dict[str, tuple[str, str]] = {}
    for heading, own_rel, shipped_rel in _SECTION_COPIES:
        own = _section((CAIRN_ROOT / own_rel).read_text(encoding="utf-8"), heading)
        shipped = _section(
            (CAIRN_ROOT / shipped_rel).read_text(encoding="utf-8"), heading)
        assert own == shipped, f"{heading} differs between own and shipped copies"
        sections[heading] = own, shipped

    for section in sections["## Acceptance criteria"]:
        for marker in _ACCEPTANCE_SLOT:
            assert section.count(marker) == 1, (
                f"acceptance template must retain one {marker!r} marker")
    assert (
        sections["## Acceptance criteria"][0].index(_ACCEPTANCE_SLOT[0])
        < sections["## Acceptance criteria"][0].index(_ACCEPTANCE_SLOT[1])
    )
