"""The review loop installs cleanly and stays upgradable.

Promises:
- Every install of each shipped profile carries the review sweep, as shipped,
  in its review-loop document.
- A fresh install of each shipped profile leaves no one-word double-brace
  placeholder the engine cannot fill, so upgrades can advance its files.
- The review sweep is body text, not a slot, so upgrades keep delivering its
  updates.

Checked on the real files and on a real install of every shipped profile.

What this file no longer does, since 2026-11-10: it does not pin the wording
of the sweep, the plan and proposal templates or `AGENTS.md`. Wording is
reviewed by readers; a test that fails on a reword is a development aid, not a
promise.

Run from the Cairn repo root:
    python -m pytest bootstrap/tests/test_review_sweep_ships.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
SCAFFOLD = CAIRN_ROOT / "bootstrap" / "scaffold.py"
PROFILES = sorted((CAIRN_ROOT / "bootstrap" / "profiles").glob("*.yml"))

#: The two source copies of the review-loop document.
SHIPPED_LOOP = "templates/core/dev/agent_collaboration.md"
OWN_LOOP = "dev/agent_collaboration.md"
_LOOP_IDS = {SHIPPED_LOOP: "shipped-loop", OWN_LOOP: "own-loop"}


def _sweep(text: str) -> str:
    """The raw text of the sweep: its heading to the next `## ` heading."""
    start = re.search(r"^## The review sweep$", text, re.M)
    assert start, "no '## The review sweep' heading"
    end = re.search(r"^## ", text[start.end():], re.M)
    stop = start.end() + end.start() if end else len(text)
    return text[start.start():stop]


@pytest.mark.parametrize("rel", sorted(_LOOP_IDS), ids=_LOOP_IDS.get)
def test_the_sweep_is_body_text_not_a_slot(rel: str) -> None:
    """A slot is frozen at its first fill, so the roster would stop updating."""
    text = (CAIRN_ROOT / rel).read_text(encoding="utf-8")
    assert "cairn:" not in _sweep(text)


@pytest.fixture(scope="session")
def installs(tmp_path_factory) -> dict[str, Path]:
    """Install each shipped profile once; return profile stem -> target tree.

    The profiles are globbed, so one added later is installed and checked
    without editing this file; the three that ship today must be among them,
    or a broken glob would pass by checking nothing.
    """
    assert {"solo-greenfield", "collaborative-team",
            "high-rigor-legacy"} <= {p.stem for p in PROFILES}
    out: dict[str, Path] = {}
    for profile in PROFILES:
        target = tmp_path_factory.mktemp(f"install-{profile.stem}")
        result = subprocess.run(
            [sys.executable, str(SCAFFOLD), "--config", str(profile),
             "--target", str(target)],
            capture_output=True, text=True, check=False,
            stdin=subprocess.DEVNULL,
        )
        assert result.returncode == 0, (
            f"installing {profile.name} exited {result.returncode}:\n"
            f"{result.stderr}")
        out[profile.stem] = target
    return out


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
def test_every_install_carries_the_sweep_as_shipped(
        installs: dict[str, Path], profile: Path) -> None:
    installed = installs[profile.stem] / "dev" / "agent_collaboration.md"
    source = (CAIRN_ROOT / SHIPPED_LOOP).read_text(encoding="utf-8")
    assert _sweep(installed.read_text(encoding="utf-8")) == _sweep(source)
