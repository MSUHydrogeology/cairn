# SPDX-License-Identifier: MIT
"""The security-family split: membership is what it says it is.

Every check here is written as a **mutation**, not a count. A check asserting
"``-m security`` collects something" passes against an empty manifest, and a
check asserting a fixed number passes against a manifest that swapped one file
for another. The failure this family guards against is silent -- a test that
stops running does not announce itself -- so the checks have to be able to fail
for the right reason.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
CAIRN_ROOT = TESTS_DIR.parents[1]


def _manifest():
    spec = importlib.util.spec_from_file_location(
        "_cairn_security_manifest_probe", TESTS_DIR / "security_manifest.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _collect(*marker_args: str, cwd: Path | None = None) -> set[str]:
    """Node ids pytest collects under *marker_args*, as a set."""
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "bootstrap/tests", "--collect-only",
         "-q", "-p", "no:cacheprovider", *marker_args],
        cwd=str(cwd or CAIRN_ROOT), capture_output=True, text=True,
        env={**_child_env()}, check=False,
    )
    ids = set()
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line.startswith("bootstrap/tests/") and "::" in line:
            ids.add(line)
    assert ids or "error" not in proc.stdout.lower(), proc.stdout[-2000:]
    return ids


def _child_env() -> dict:
    import os
    env = dict(os.environ)
    env["CAIRN_FULL_SUITE"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def _files_of(ids) -> set[str]:
    return {i.split("::", 1)[0].rsplit("/", 1)[-1] for i in ids}


def test_the_manifest_is_not_empty() -> None:
    """The degenerate case every other check here would silently pass against.
    An empty manifest deselects nothing, so the split does nothing and looks
    like it works."""
    assert len(_manifest().SECURITY_FAMILY) >= 10


def test_every_manifest_member_exists_on_disk() -> None:
    """A member naming a file that no longer exists marks nothing, so its tests
    quietly rejoin the per-change loop -- or, worse, a renamed file leaves the
    family without anyone noticing. Named individually so the failure says which
    one."""
    missing = [name for name in _manifest().SECURITY_FAMILY
               if not (TESTS_DIR / name).is_file()]
    assert not missing, f"manifest names files that do not exist: {missing}"


def test_every_member_carries_an_owner_and_a_reason() -> None:
    """The manifest's whole value over a per-file marker is that it says *why*.
    A blank reason is a member nobody can argue with later."""
    thin = [name for name, (owner, reason) in _manifest().SECURITY_FAMILY.items()
            if not owner.strip() or len(reason.strip()) < 20]
    assert not thin, f"members with no usable owner or reason: {thin}"


def test_the_marker_selects_exactly_the_manifest() -> None:
    """The membership property itself. Compares the *set of files* collected
    under ``-m security`` against the manifest -- not a count, which a manifest
    that swapped one file for another would still satisfy."""
    assert _files_of(_collect("-m", "security")) == set(
        _manifest().SECURITY_FAMILY)


def test_not_security_collects_no_member() -> None:
    """The complement, and the one that matters for the per-change loop: if a
    member leaks through, the split silently buys nothing for that file."""
    leaked = _files_of(_collect("-m", "not security")) & set(
        _manifest().SECURITY_FAMILY)
    assert not leaked, f"security members collected in the per-change loop: {leaked}"


def test_the_two_selections_partition_the_suite() -> None:
    """Neither overlapping nor losing anything. A test in neither half would be
    a test that never runs again, which is exactly the silent failure this
    family is about."""
    marked = _collect("-m", "security")
    unmarked = _collect("-m", "not security")
    everything = _collect()
    assert not (marked & unmarked), "a test is in both halves"
    assert marked | unmarked == everything, (
        "a test is in neither half: "
        f"{sorted(everything - (marked | unmarked))[:5]}")


def test_unmarking_a_member_is_detected(tmp_path) -> None:
    """**The directed mutation the accepted contract names.** Drop one member
    from the manifest and the membership property must fail.

    Without this, every check above passes against a manifest that has quietly
    lost a file: the marker would still select exactly what the (shrunken)
    manifest names, and the dropped file would rejoin the per-change loop
    unremarked. Run against a scratch copy of the manifest so the repository's
    own is never mutated.
    """
    manifest = _manifest()
    victim = "test_gate_preflight.py"
    assert victim in manifest.SECURITY_FAMILY, "fixture drifted from the manifest"

    shrunken = dict(manifest.SECURITY_FAMILY)
    shrunken.pop(victim)

    # The property under test, evaluated against the mutant: the live marker
    # still selects the real family, which no longer equals the shrunken one.
    live_files = _files_of(_collect("-m", "security"))
    assert live_files != set(shrunken), (
        "removing a member from the manifest did not change what the "
        "membership property compares -- the check cannot fail")
    assert victim in live_files


def test_the_release_entry_point_is_not_deselected() -> None:
    """§5's load-bearing promise: the release path does not change.
    ``bootstrap/security_check.py`` runs the entire suite with no marker
    expression, so the split cannot reach it. Pinned because the whole argument
    for moving 1,328 tests out of the per-change loop rests on them still
    running somewhere."""
    source = (CAIRN_ROOT / "bootstrap" / "security_check.py").read_text(
        encoding="utf-8")
    assert "-m security" not in source
    assert "not security" not in source


#: The manifest's exact membership as reviewed for Chunk E's Security Review
#: (2026-08-24) -- see ``dev/plans/convergent-lifecycle.md``, "## Security
#: review (Internal)". Every check above is differential against the *live*
#: manifest, so a member added (or dropped, unless it happens to be the one
#: hardcoded victim above) alongside a plausible owner/reason passes every one
#: of them: the expected set and the observed set are both read from the same
#: edited file. Measured during this review: adding one unrelated, well-formed
#: entry to ``SECURITY_FAMILY`` left the other eight checks in this file green
#: while its tests silently left the per-change loop -- exactly the failure
#: mode this family exists to catch. This is the one check with an oracle
#: outside the manifest.
_REVIEWED_MEMBERS = frozenset({
    "test_api_access_security.py",
    "test_ast_attest.py",
    "test_default_security_stance.py",
    "test_gate_preflight.py",
    "test_gate_reanchor.py",
    "test_portable_security_sweeps.py",
    "test_reanchor.py",
    "test_security_capability_install.py",
    "test_security_check.py",
    "test_security_finding_confidentiality.py",
    "test_security_leaf.py",
    "test_security_lint.py",
    "test_security_net.py",
    "test_security_stack.py",
    "test_security_verification.py",
    "test_skills_security.py",
    "test_web_hosting_security.py",
})


def test_the_manifest_still_names_exactly_the_reviewed_set() -> None:
    """A member added or dropped alongside a plausible owner/reason passes
    every check above, because each is differential against the live manifest
    rather than against any fact outside it. Pinning the reviewed set here
    means a future change to ``SECURITY_FAMILY``'s membership is a diff
    against this line, not a manifest edit that passes on its own say-so.
    """
    assert set(_manifest().SECURITY_FAMILY) == _REVIEWED_MEMBERS
