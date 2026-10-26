"""`upgrade --remove-retired`: the engine's list of retired files, and what it removes.

Cairn deletes a project's copy of a file it stopped shipping only when two things
agree: the path is on the engine's own list (`_RETIRED_INSTALLS`), and the bytes
are a version Cairn shipped (a SHA-256 digest on that row). The project supplies
the file and the lockfile, so neither can add a name or vouch for the bytes.

The tests drive the real `scaffold.py` entry point over a real install, as
`test_agreement_retired.py` does. A project from an older Cairn is modelled by
adding the former records and files to a fresh scratch install; the bytes come
from Cairn's own git history, by the blob ids the list carries.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bootstrap import scaffold as s  # noqa: E402
from bootstrap._scaffold import config as C  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
EMPTY_FILE_DIGEST = hashlib.sha256(b"").hexdigest()
HEX64 = re.compile(r"[0-9a-f]{64}")
HEX40 = re.compile(r"[0-9a-f]{40}")


# ---------------------------------------------------------------------------
# The list
# ---------------------------------------------------------------------------

def _shipped_destinations() -> set[str]:
    """Every destination the running tree can install, optional files included."""
    shipped = {dst for _src, dst, _verbatim in s.install_manifest(modules=None)}
    shipped.update(dst for _src, dst, _axis, _values in C._OPTIONAL_TEMPLATES)
    return shipped


def _row_problems(rows: object) -> list[str]:
    """What is wrong with a list of retired rows; empty when it is sound."""
    shipped = _shipped_destinations()
    shipped_sources = {src for src, _dst, _verbatim in s.install_manifest(modules=None)}
    problems: list[str] = []
    seen: set[str] = set()
    for src, dst, verbatim, digests in rows:  # type: ignore[attr-defined]
        if (ROOT / "templates" / src).exists() or src in shipped_sources:
            problems.append(f"{dst}: source {src} is still shipped")
        if dst in shipped:
            problems.append(f"{dst}: destination is still shipped")
        if dst in seen:
            problems.append(f"{dst}: listed twice")
        seen.add(dst)
        if not isinstance(verbatim, bool):
            problems.append(f"{dst}: verbatim is not a boolean")
        if not digests:
            problems.append(f"{dst}: no digest")
        for digest, commit, blob in digests:
            if not HEX64.fullmatch(digest):
                problems.append(f"{dst}: {digest!r} is not 64 lowercase hex")
            if digest == EMPTY_FILE_DIGEST:
                problems.append(f"{dst}: a digest is the empty file's")
            if not HEX40.fullmatch(commit) or not HEX40.fullmatch(blob):
                problems.append(f"{dst}: provenance is not full object ids")
    return problems


def test_no_retired_row_is_still_shipped_and_every_row_has_digests() -> None:
    assert _row_problems(C._RETIRED_INSTALLS) == []
    assert len(C._RETIRED_INSTALLS) > 0


def test_the_row_check_flags_a_shipped_row_and_a_renamed_template() -> None:
    # Instrument check: the same function must see both planted defects.
    src, dst, verbatim = s.install_manifest(modules=None)[0]
    digest = ("a" * 64, "b" * 40, "c" * 40)
    shipped = (src, dst, verbatim, (digest,))
    assert _row_problems((shipped,)), "a row for a shipped file went unnoticed"
    renamed = ("modules/default-on/a-template-nobody-ships.md", dst, False, (digest,))
    assert any("destination is still shipped" in p for p in _row_problems((renamed,)))
    empty = ("modules/default-on/gone.md", "dev/gone.md", False,
             ((EMPTY_FILE_DIGEST, "b" * 40, "c" * 40),))
    assert _row_problems((empty,)), "the empty file's digest went unnoticed"


def _git_blob(blob: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "blob", blob],
        capture_output=True, check=False, timeout=60,
    )


def test_every_retired_digest_recomputes_from_git_history() -> None:
    # Fails, never skips, when a blob is missing: a skip would hide a lost
    # object for good. The commit id is a label and is never read, so a
    # re-anchor that rewrites commit ids cannot turn this red.
    wrong: list[str] = []
    for _src, dst, _verbatim, digests in C._RETIRED_INSTALLS:
        for digest, _commit, blob in digests:
            result = _git_blob(blob)
            if result.returncode != 0:
                wrong.append(f"{dst}: git has no blob {blob}")
            elif hashlib.sha256(result.stdout).hexdigest() != digest:
                wrong.append(f"{dst}: blob {blob} does not hash to {digest}")
    assert wrong == []
