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
- The release security check runs the shipped-only selection with no marker expression.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
CAIRN_ROOT = TESTS_DIR.parent


def _manifest():
    spec = importlib.util.spec_from_file_location(
        "_cairn_security_manifest_probe", TESTS_DIR / "security_manifest.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _collect(*marker_args: str, cwd: Path | None = None,
             env: dict[str, str] | None = None) -> set[str]:
    """Node ids pytest collects under *marker_args*, as a set."""
    child_env = _child_env() if env is None else dict(env)
    child_env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", "--collect-only",
         "-q", "-p", "no:cacheprovider", *marker_args],
        cwd=str(cwd or CAIRN_ROOT), capture_output=True, text=True,
        env=child_env, check=False,
    )
    ids = set()
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line.startswith("tests/") and "::" in line:
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
    "test_portable_security_sweeps.py",
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


def test_release_exclusion_list_matches_the_reviewed_files() -> None:
    expected = {
        "tests/test_repin.py",
        "tests/test_repin_ceremony.py",
        "tests/test_reanchor.py",
        "tests/test_reanchor_driver_disclosures.py",
        "tests/test_gate_reanchor.py",
        "tests/test_gate_preflight.py",
        "tests/test_gate_manifest.py",
        "tests/test_gate_transition.py",
        "tests/test_oracle.py",
        "tests/test_oracle_activation.py",
        "tests/test_oracle_trust.py",
        "tests/test_ceremony_review_report.py",
        "tests/security/test_check_release_publication.py",
        "tests/test_quality_gate_cli.py",
        "tests/test_quality_gate_order_independence.py",
        "tests/integration/test_quality_gate_redundancy.py",
    }
    manifest = _manifest()
    assert manifest.release_excluded_files() == expected
    assert len(manifest.RELEASE_EXCLUDED_TESTS) == len(expected)


def test_release_required_files_are_pinned_and_tracked() -> None:
    expected = {
        "tests/test_ast_attest.py",
        "tests/test_quality_gate_neutrality.py",
        "tests/test_security_check.py",
        "tests/test_security_marker.py",
        "tests/contract/test_release_members_contract.py",
        "tests/test_session_binding_gate_and_printing_hold.py",
        "tests/test_manifest.py",
        "tests/test_verify_integrity.py",
        "tests/test_verify_ref.py",
        "tests/test_security_lint.py",
        "tests/test_loop_fidelity_gate.py",
    }
    manifest = _manifest()
    tracked = set(subprocess.run(
        ["git", "ls-files"], cwd=CAIRN_ROOT, capture_output=True, text=True,
        check=True,
    ).stdout.splitlines())
    assert manifest.RELEASE_REQUIRED_FILES == expected
    assert expected | manifest.release_excluded_files() <= tracked


def test_release_exclusions_select_each_file_from_its_subject() -> None:
    spec = importlib.util.spec_from_file_location(
        "_test_tiers_for_release_manifest", CAIRN_ROOT / "tests" / "tier_inventory.py")
    assert spec is not None and spec.loader is not None
    tiers = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tiers)
    files = tiers.find_test_files()
    for path, subjects, _reason in _manifest().RELEASE_EXCLUDED_TESTS:
        for subject in subjects:
            selected = tiers.tests_for_paths([subject], files, root=CAIRN_ROOT)
            assert CAIRN_ROOT / path in selected, (path, subject)


def test_no_release_excluded_file_has_a_native_roster_row() -> None:
    excluded = _manifest().release_excluded_files()
    roster = _manifest().NATIVE_ONLY_NODE_IDS
    assert not any(node_id.split("::", 1)[0] in excluded
                   for _host, node_id in roster)


@pytest.mark.skipif(sys.platform not in {"darwin", "win32"},
                    reason="strict native collection is supported on Mac and Windows")
def test_real_tree_strict_collection_removes_only_the_reviewed_files(
        tmp_path: Path) -> None:
    manifest = _manifest()
    report_dir = tmp_path / "strict-reports"
    report_dir.mkdir()
    env = dict(os.environ)
    env.pop("CAIRN_FULL_SUITE", None)
    env["CAIRN_RELEASE_GATE_ACTIVE"] = "1"
    env["CAIRN_NATIVE_RUN_NONCE"] = "a" * 64
    env["CAIRN_NATIVE_RUN_HEAD"] = "b" * 40
    env["CAIRN_NATIVE_RUN_POLICY_ID"] = manifest.NATIVE_ONLY_POLICY_ID
    env["CAIRN_NATIVE_RUN_DEFAULT_REPORT"] = str(report_dir / "default.json")
    env["CAIRN_NATIVE_RUN_SEED0_REPORT"] = str(report_dir / "seed-0.json")

    plain = _collect()
    strict = _collect(env=env)
    excluded = manifest.release_excluded_files()
    removed = {node for node in plain
               if node.split("::", 1)[0] in excluded}
    assert strict == plain - removed
    assert {node.split("::", 1)[0] for node in removed} == excluded
    collected_files = {node.split("::", 1)[0] for node in strict}
    assert manifest.RELEASE_REQUIRED_FILES <= collected_files


@pytest.mark.parametrize("rows, expected", [
    pytest.param([], None, id="not-a-tuple"),
    pytest.param((("tests/test_ok.py", ("subject.py",)),), None, id="two-item-row"),
    pytest.param(((1, ("subject.py",), "reason"),), None, id="non-string-path"),
    pytest.param((("/tests/test_ok.py", ("subject.py",), "reason"),), None, id="absolute"),
    pytest.param((("tests/../test_ok.py", ("subject.py",), "reason"),), None, id="parent-segment"),
    pytest.param((("bootstrap\\tests\\test_ok.py", ("subject.py",), "reason"),), None, id="backslash"),
    pytest.param((("tests/test_ok/", ("subject.py",), "reason"),), None, id="directory"),
    pytest.param((("tests/_x.py", ("subject.py",), "reason"),), None, id="helper-name"),
    pytest.param((("scripts/repin.py", ("subject.py",), "reason"),), None, id="outside-tree"),
    pytest.param((("tests/test_ok.py", (), "reason"),), None, id="empty-subjects"),
    pytest.param((("tests/test_ok.py", ["subject.py"], "reason"),), None, id="subjects-not-tuple"),
    pytest.param((("tests/test_ok.py", ("subject.py",), ""),), None, id="empty-reason"),
    pytest.param((("tests/test_ok.py", ("subject.py",), "reason"),
                  ("tests/test_ok.py", ("other.py",), "reason")), None, id="duplicate"),
    pytest.param((("tests/test_ok.py", (1,), "reason"),), None, id="non-string-subject"),
    pytest.param((("tests/test_ok.py", ("",), "reason"),), None, id="empty-subject-value"),
    pytest.param((("tests/test_ok.py", ("subject.py",), 1),), None, id="non-string-reason"),
    pytest.param((("tests/test_security_leaf.py", ("subject.py",), "reason"),), None, id="family-file"),
    pytest.param((("tests/test_security_marker.py", ("subject.py",), "reason"),), None, id="required-file"),
    pytest.param((("tests/test_fixture.py", ("scripts/example.py",), "Fixture."),),
                 frozenset({"tests/test_fixture.py"}), id="valid-row"),
    pytest.param((), frozenset(), id="empty-list"),
])
def test_release_exclusion_accessor_validates_its_contract(
    monkeypatch: pytest.MonkeyPatch, rows, expected,
) -> None:
    manifest = _manifest()
    monkeypatch.setattr(manifest, "RELEASE_EXCLUDED_TESTS", rows)
    if expected is None:
        with pytest.raises(ValueError):
            manifest.release_excluded_files()
    else:
        assert manifest.release_excluded_files() == expected
