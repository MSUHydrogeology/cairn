"""Every module the shipped roster advertises must actually exist.

`templates/modules/README.md` carries a table of modules an adopter can select.
It is curated, not exhaustive -- there are more module files than rows -- so the
checkable property runs one way only: **a row must name a module that ships.**

Nothing checked this before, and it drifted. When the subtraction sweep removed
the `lifecycle-metrics` and `fold-back-ledger` modules, their roster rows stayed
behind, so the table went on offering two modules whose files were gone. An
adopter reading it was being offered something they could not install, and the
install path answers a request for a missing module with `[warn] unknown module
... skipped` -- a warning, not a refusal, so the roster could lie indefinitely
without anything going red.
"""

from __future__ import annotations

import re
from pathlib import Path

_TEMPLATES = Path(__file__).resolve().parent.parent.parent / "templates"
_ROSTER = _TEMPLATES / "modules" / "README.md"

#: A roster row: `| <set> | `<module>` | <when selected> |`. The set column is
#: prose (it names tiers like `token-gated` that are not directories), so the
#: module is resolved against every module directory rather than against the
#: set the row claims.
_ROW = re.compile(r"^\|\s*[^|]+\|\s*`([a-z0-9-]+)`\s*\|")


def _advertised_modules() -> list[str]:
    return [m.group(1) for line in _ROSTER.read_text().splitlines()
            if (m := _ROW.match(line))]


def _shipped_modules() -> set[str]:
    return {p.stem for d in (_TEMPLATES / "modules").iterdir() if d.is_dir()
            for p in d.glob("*.md") if p.name != "README.md"}


def test_the_roster_names_only_modules_that_ship() -> None:
    """A row for a module whose file is gone offers an uninstallable module."""
    advertised = _advertised_modules()
    assert advertised, (
        "parsed no rows out of the roster -- the table's shape changed and this "
        "check has gone vacuous, which is worse than no check"
    )
    missing = sorted(set(advertised) - _shipped_modules())
    assert not missing, (
        f"the roster advertises {len(missing)} module(s) with no file: "
        f"{missing}. Either restore the module or drop its row -- an adopter "
        f"who selects one gets a skipped-with-warning install, not a refusal."
    )
