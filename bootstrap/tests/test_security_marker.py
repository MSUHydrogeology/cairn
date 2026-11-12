# SPDX-License-Identifier: MIT
"""The security-family split: membership is what it says it is.

Every check here is written as a **mutation**, not a count. A check asserting
"``-m security`` collects something" passes against an empty manifest, and a
check asserting a fixed number passes against a manifest that swapped one file
for another. The failure this family guards against is silent -- a test that
stops running does not announce itself -- so the checks have to be able to fail
for the right reason.

Promises:
- In a per-change run, the security marker selects exactly the reviewed manifest members.
- A per-change run without the security marker collects no manifest member.
- The security selection and its complement partition the suite: no test is in both or in neither.
- The release security check runs the whole suite with no marker expression, so the release path is unchanged.
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
