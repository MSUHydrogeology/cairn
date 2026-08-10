# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
"""Public-path tests for ``scripts/api_access_security.py``.

Every test here drives the **installed command line as a subprocess** against a
two-principal loopback fixture API, and every "what arrived" assertion reads the
*fixture's* request log — a different process's record — rather than the runner's
own bookkeeping. No transport call is mocked anywhere in this file.

The recording-server machinery is imported from ``test_security_net`` rather than
copied, so the two suites cannot drift into disagreeing about what the fixture
recorded.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from bootstrap.tests.test_security_net import (  # noqa: E402
    ENGINE_SRC,
    Fixture,
    wait_for,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = REPO_ROOT / "templates" / "modules" / "team-gated"
FACADE_SRC = TEMPLATE_DIR / "api_access_security.py"
STUB_SRC = TEMPLATE_DIR / "api_access_policy_stub.json"

#: The installed engine directory name for this capability, per its
#: ``_MODULE_MAPPINGS`` group.  Named here so these tests exercise the *installed*
#: layout rather than the template layout the facade also tolerates.
ENGINE_DST = "_api_access_security"

MARKER_P1 = "cred-Zq7Wp1-A91f"
MARKER_P2 = "cred-Zq7Wp2-B52g"
MARKER_DEPLOYED = "cred-Zq7Wp3-DEPLOYED-C63h"


# ---------------------------------------------------------------------------
# An installed adopter tree
# ---------------------------------------------------------------------------


def install_adopter(tmp_path: Path, policy: "dict | None",
                    *, drop_member: "str | None" = None) -> Path:
    """Lay the capability out at its real install destinations.

    Copied to the destinations ``_MODULE_MAPPINGS`` declares, rather than run
    through the scaffold, so a facade defect cannot be masked by an installer
    defect and vice versa.
    """
    root = tmp_path / "adopter"
    scripts = root / "scripts"
    engine = scripts / ENGINE_DST
    engine.mkdir(parents=True)
    (root / "dev" / ".cairn").mkdir(parents=True)
    shutil.copy(FACADE_SRC, scripts / "api_access_security.py")
    for member in sorted(ENGINE_SRC.glob("*.py")):
        if drop_member is not None and member.name == drop_member:
            continue
        shutil.copy(member, engine / member.name)
    target = root / "dev" / ".cairn" / "api-access-policy.json"
    if policy is None:
        shutil.copy(STUB_SRC, target)
    else:
        target.write_text(json.dumps(policy, indent=2), encoding="utf-8")
    return root


def run_facade(root: Path, argv: "list[str]", *, env_extra=None,
               credentials=True) -> subprocess.CompletedProcess:
    """Run the installed facade with an **explicitly constructed** environment.

    The child environment is built here, in full, from a fixed base plus what a
    test asks for. It is deliberately *not* derived from the parent
    ``os.environ``: an expectation derived from the parent cannot be compared
    against a child the interpreter may have added variables to, and asserting
    on a set measured at a different boundary than the one under test is how a
    sibling suite produced a failure nobody could reproduce.
    """
    env = {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONDONTWRITEBYTECODE": "1",
        "HOME": os.environ.get("HOME", ""),
        "TMPDIR": os.environ.get("TMPDIR", "/tmp"),
    }
    if credentials:
        env["CAIRN_API_P1_CREDENTIAL"] = MARKER_P1
        env["CAIRN_API_P2_CREDENTIAL"] = MARKER_P2
    env.update(env_extra or {})
    return subprocess.run(
        [sys.executable, str(root / "scripts" / "api_access_security.py"), *argv],
        capture_output=True, env=env, timeout=120,
    )


# ---------------------------------------------------------------------------
# The fixture API
# ---------------------------------------------------------------------------


def _json_response(status: int, payload: dict, reason: str = "OK") -> bytes:
    body = json.dumps(payload).encode("utf-8")
    return (
        f"HTTP/1.1 {status} {reason}\r\nContent-Type: application/json\r\n"
        f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n"
    ).encode("iso-8859-1") + body


def api_responder(*, leak: bool = False, overexpose: bool = False,
                  authorize_everything: bool = False):
    """A two-principal fixture API.

    ``leak`` is the BOLA hazard: principal 2's credential receives principal 1's
    object. ``authorize_everything`` is criterion B-1's hazard: every request
    succeeds regardless of who asked.
    """

    def _responder(record):
        auth = record.header("Authorization") or ""
        is_owner = MARKER_P1 in auth
        payload = {"id": "1", "owner": "p1"}
        if overexpose:
            payload["internal_note"] = "acquisition pending"
        if authorize_everything or is_owner or leak:
            return _json_response(200, payload)
        return _json_response(403, {"error": "forbidden"}, reason="Forbidden")

    return _responder


def api_policy(port: int, *, host: str = "127.0.0.1", deployed=None,
               environment: "str | None" = None, configured: bool = True) -> dict:
    authority = f"[{host}]" if ":" in host else host
    local: dict = {
        "base_url": f"http://{authority}:{port}",
        "principals": [{"id": "p1", "role": "owner"}, {"id": "p2"}],
        "operations": [{
            "id": "read-order", "method": "GET", "path": "/orders/1",
            "kind": "object",
            "cases": [
                {"id": "owner-reads", "principal": "p1", "expect": "allow",
                 "status": [200], "require_present": ["/id"],
                 "require_absent": ["/internal_note"]},
                {"id": "other-denied", "principal": "p2", "expect": "deny",
                 "status": [403, 404]},
            ],
        }],
    }
    if environment is not None:
        local["environment"] = environment
    document = {
        "schema": "cairn.security.api-access-policy.v1",
        "configured": configured,
        "local": local,
    }
    if deployed is not None:
        document["deployed"] = deployed
    return document


def deployed_section(base_url: str) -> dict:
    return {
        "base_url": base_url,
        "principals": [{"id": "p3"}, {"id": "p4"}],
        "operations": [{
            "id": "probe", "method": "GET", "path": "/health",
            "kind": "function",
            "cases": [
                {"id": "up", "principal": "p3", "expect": "allow",
                 "status": [200]},
                {"id": "denied", "principal": "p4", "expect": "deny",
                 "status": [401]},
            ],
        }],
    }


@pytest.fixture()
def serve():
    started: list[Fixture] = []

    def _start(responder, **kwargs):
        fixture = Fixture(responder, **kwargs)
        started.append(fixture)
        return fixture

    try:
        yield _start
    finally:
        for fixture in started:
            fixture.close()


def result_of(proc) -> str:
    text = proc.stdout.decode("utf-8", "replace")
    for line in text.splitlines():
        if line.startswith("cairn-security-result:"):
            return line.split(":", 1)[1].strip()
    return f"<no result line> rc={proc.returncode} {text!r}"


# ---------------------------------------------------------------------------
# B-2 -- the ownership swap actually catches BOLA
# ---------------------------------------------------------------------------


def test_b2_the_swap_catches_bola_and_a_correct_fixture_is_clean(
    tmp_path, serve
):
    """B-2: CLEAN means the declared denial held; FINDINGS names what failed."""
    leaky = serve(api_responder(leak=True))
    root = install_adopter(tmp_path, api_policy(leaky.port))
    proc = run_facade(root, ["local"])
    assert proc.returncode == 10, result_of(proc)
    assert result_of(proc) == "FINDINGS"
    text = proc.stdout.decode()
    assert "read-order" in text and "other-denied" in text
    assert "cross-principal-denial" in text
    # Both halves of the swap were actually sent -- one credential each.
    assert wait_for(lambda: len(leaky.records) == 2)
    seen = {r.header("Authorization") for r in leaky.records}
    assert seen == {MARKER_P1, MARKER_P2}

    correct = serve(api_responder(leak=False))
    root2 = install_adopter(tmp_path / "b", api_policy(correct.port))
    proc2 = run_facade(root2, ["local"])
    assert proc2.returncode == 0, result_of(proc2)
    assert result_of(proc2) == "CLEAN"


def test_b2_a_fixture_that_authorizes_everything_is_not_clean(tmp_path, serve):
    """B-1's hazard at the public path: an API that authorizes everything
    cannot produce CLEAN against a matrix that declares a denial."""
    permissive = serve(api_responder(authorize_everything=True))
    root = install_adopter(tmp_path, api_policy(permissive.port))
    proc = run_facade(root, ["local"])
    assert proc.returncode == 10, result_of(proc)


def test_b2_an_overexposed_property_is_a_finding_without_its_value(
    tmp_path, serve
):
    fixture = serve(api_responder(overexpose=True))
    root = install_adopter(tmp_path, api_policy(fixture.port))
    proc = run_facade(root, ["local"])
    assert proc.returncode == 10, result_of(proc)
    text = proc.stdout.decode()
    assert "overexposed-property" in text
    # The bucket survives; the value does not.
    assert "observed_magnitude=short" in text
    assert "acquisition" not in text


# ---------------------------------------------------------------------------
# B-3 -- non-loopback is unreachable from `local`, under every policy shape
# ---------------------------------------------------------------------------

_NON_LOOPBACK_HOSTS = (
    "example.test", "10.0.0.7", "192.168.1.5", "169.254.1.1", "224.0.0.1",
    "0.0.0.0", "240.0.0.1", "fd00::1", "fe80::1", "::", "2001:db8::1",
    "example.test.",
)


@pytest.mark.parametrize("host", _NON_LOOPBACK_HOSTS)
@pytest.mark.parametrize("environment", (None, "staging", "production"))
def test_b3_local_refuses_every_non_loopback_shape(tmp_path, host, environment):
    """B-3: refused for every host shape and under every environment *label*.

    The label is carried for the adopter's reading and is never an authority;
    running each row under all three values is what makes that testable rather
    than asserted.
    """
    policy = api_policy(8099, host=host, environment=environment)
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"])
    assert proc.returncode == 20, result_of(proc)
    text = proc.stdout.decode()
    assert "DEGRADED" in text
    assert ("non_loopback_target" in text or "url_userinfo" in text
            or "host_refused" in text), text


def test_b3_a_userinfo_url_is_refused_by_the_schema(tmp_path):
    policy = api_policy(8099)
    policy["local"]["base_url"] = "http://user:pw@127.0.0.1:8099"
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"])
    assert proc.returncode == 20
    assert "url_userinfo" in proc.stdout.decode()


def test_b3_a_non_default_loopback_port_is_accepted(tmp_path, serve):
    """The row this criterion must **not** refuse, recorded deliberately.

    B-3's table lists "a non-default port" among its refusal rows. Measured, that
    row belongs to B-5's *deployed* near-miss table, not here: a disposable
    loopback fixture is bound to an arbitrary high port by definition, so
    refusing a non-default port on ``local`` would refuse every correct use of
    this capability. Pinned as an accepted shape so the discrepancy is visible
    rather than silently resolved one way or the other.
    """
    fixture = serve(api_responder())
    root = install_adopter(tmp_path, api_policy(fixture.port))
    proc = run_facade(root, ["local"])
    assert proc.returncode == 0, result_of(proc)


# ---------------------------------------------------------------------------
# B-4 / A-8(b) -- credential confidentiality and namespace isolation
# ---------------------------------------------------------------------------


def test_b4_local_never_reads_or_emits_a_deployed_credential(tmp_path, serve):
    """B-4: the deployed marker reaches no request and no output channel."""
    fixture = serve(api_responder())
    policy = api_policy(
        fixture.port, deployed=deployed_section("https://api.example.test")
    )
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], env_extra={
        "CAIRN_API_P3_CREDENTIAL": MARKER_DEPLOYED,
        "CAIRN_API_P4_CREDENTIAL": MARKER_DEPLOYED + "-4",
    })
    assert proc.returncode == 0, result_of(proc)
    assert wait_for(lambda: len(fixture.records) == 2)
    for record in fixture.records:
        assert MARKER_DEPLOYED not in record.raw.decode("iso-8859-1")
    assert MARKER_DEPLOYED.encode() not in proc.stdout
    assert MARKER_DEPLOYED.encode() not in proc.stderr


def test_a8b_no_populated_credential_reaches_any_channel(tmp_path, serve):
    """A-8(b): every credential marker absent from stdout, stderr, the report,
    and every file in the temporary directory."""
    fixture = serve(api_responder())
    root = install_adopter(tmp_path, api_policy(fixture.port))
    proc = run_facade(root, ["local"])
    assert proc.returncode == 0, result_of(proc)
    for marker in (MARKER_P1, MARKER_P2):
        assert marker.encode() not in proc.stdout
        assert marker.encode() not in proc.stderr
    report_path = None
    for line in proc.stdout.decode().splitlines():
        if line.strip().startswith("report:"):
            report_path = Path(line.split("report:", 1)[1].strip())
    assert report_path is not None and report_path.is_file()
    directory = report_path.parent
    try:
        assert sorted(p.name for p in directory.iterdir()) == ["report.json"]
        blob = report_path.read_bytes()
        for marker in (MARKER_P1, MARKER_P2):
            assert marker.encode() not in blob
        # The report is off-tree by construction; assert it, since a report
        # inside a checkout is one `git add -A` from a commit.
        assert REPO_ROOT not in directory.resolve().parents
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def test_a8c_a_refusal_precedes_the_credential_lookup(tmp_path):
    """A-8(c): the ordering oracle no access idiom can route around.

    Run in a subprocess whose environment **does not contain the credential
    variables at all**, over a policy that must be refused. The requirement is
    the *policy-refusal* code, never the absent-credential code -- which is only
    checkable because those are two distinct fixed codes.
    """
    policy = api_policy(8099, host="10.0.0.7")
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], credentials=False)
    assert proc.returncode == 20
    text = proc.stdout.decode()
    assert "policy_refused" in text, text
    assert "credential_absent" not in text, text


def test_a8c_an_absent_credential_reports_the_other_code(tmp_path, serve):
    """The discriminating half of A-8(c): with a *valid* policy and no
    credentials, the absent-credential code is what appears. Without this row,
    "policy_refused and not credential_absent" could hold because the
    credential code is unreachable."""
    fixture = serve(api_responder())
    root = install_adopter(tmp_path, api_policy(fixture.port))
    proc = run_facade(root, ["local"], credentials=False)
    assert proc.returncode == 20
    text = proc.stdout.decode()
    assert "credential_absent" in text, text
    assert fixture.records == []


# ---------------------------------------------------------------------------
# B-5 -- exact re-authorization
# ---------------------------------------------------------------------------

_NEAR_MISSES = (
    "https://api.example.test/",
    "https://API.EXAMPLE.TEST",
    "https://api.example.test:443",
    "http://api.example.test",
    "https://api.example.test?x=1",
    "https://api.example.test/v1",
    " https://api.example.test",
)


@pytest.mark.parametrize("supplied", _NEAR_MISSES)
def test_b5_deployed_refuses_every_near_miss_before_any_request(
    tmp_path, supplied
):
    """B-5: byte-for-byte, and refused before a credential is looked up.

    No row here contacts a real host: the refusal precedes DNS, so the declared
    origin is never resolved.
    """
    policy = api_policy(
        8099, deployed=deployed_section("https://api.example.test")
    )
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["deployed-passive", "--authorize-base-url", supplied],
                      credentials=False)
    assert proc.returncode == 20, result_of(proc)
    text = proc.stdout.decode()
    assert "authorization_mismatch" in text, text
    assert "credential_absent" not in text


def test_b5_the_exact_normalized_url_gets_past_the_authorization_check(
    tmp_path
):
    """The positive control. Without it, every near-miss row above could be
    "the deployed leg refuses everything", and the check would be untested.

    The run still fails -- it stops at the absent deployed credential, because
    no test in this plan supplies one and none contacts a real host. That the
    failure *moved past* the authorization check is the assertion.
    """
    policy = api_policy(
        8099, deployed=deployed_section("https://api.example.test")
    )
    root = install_adopter(tmp_path, policy)
    proc = run_facade(
        root, ["deployed-passive", "--authorize-base-url",
               "https://api.example.test"],
        credentials=False,
    )
    assert proc.returncode == 20
    text = proc.stdout.decode()
    assert "authorization_mismatch" not in text, text
    assert "credential_absent" in text, text


def test_b7_a_mutating_deployed_method_is_a_schema_refusal(tmp_path):
    """B-7: there is no v1 route to a non-loopback write, and the refusal is at
    schema level so it precedes every other consideration."""
    section = deployed_section("https://api.example.test")
    section["operations"][0]["method"] = "POST"
    policy = api_policy(8099, deployed=section)
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], credentials=False)
    assert proc.returncode == 20
    assert "deployed_method_refused" in proc.stdout.decode()


def test_b7_the_facade_exposes_exactly_two_subcommands_and_no_mutation_flag(
    tmp_path
):
    root = install_adopter(tmp_path, None)
    proc = run_facade(root, ["--help"], credentials=False)
    text = proc.stdout.decode()
    assert "local" in text and "deployed-passive" in text
    assert "allow-mutation" not in text
    source = FACADE_SRC.read_text(encoding="utf-8")
    assert "allow_mutation" not in source and "allow-mutation" not in source
    bad = run_facade(root, ["staging"], credentials=False)
    assert bad.returncode != 0


# ---------------------------------------------------------------------------
# B-6 -- the two output modes cannot be confused
# ---------------------------------------------------------------------------


def test_b6_the_dispatcher_document_and_the_human_summary_are_disjoint(
    tmp_path, serve
):
    fixture = serve(api_responder())
    root = install_adopter(tmp_path, api_policy(fixture.port))
    human = run_facade(root, ["local"])
    child = run_facade(root, ["local", "--child-document"])
    assert human.returncode == child.returncode == 0

    document = json.loads(child.stdout.decode())
    assert set(document) == {
        "schema", "capability", "contract", "evidence_mode", "result", "details",
    }
    assert document["schema"] == "cairn.security.capability-result.v1"
    assert document["evidence_mode"] == "loopback"
    assert document["result"] == "CLEAN"
    # The child document carries no human summary...
    assert "cairn-security-result:" not in child.stdout.decode()
    # ...and the human summary does not parse as the child document.
    with pytest.raises(ValueError):
        json.loads(human.stdout.decode())
    assert "cairn-security-result: CLEAN" in human.stdout.decode()


def test_c5_local_evidence_says_it_is_not_deployed_evidence(tmp_path, serve):
    fixture = serve(api_responder())
    root = install_adopter(tmp_path, api_policy(fixture.port))
    human = run_facade(root, ["local"])
    child = run_facade(root, ["local", "--child-document"])
    assert "not a deployed CLEAN" in human.stdout.decode()
    document = json.loads(child.stdout.decode())
    assert document["evidence_mode"] == "loopback"
    assert any("not a deployed CLEAN" in n for n in document["details"]["notes"])


# ---------------------------------------------------------------------------
# E-1 / E-2 -- the stub, and A-10's facade half
# ---------------------------------------------------------------------------


def test_e1_the_untouched_stub_is_incomplete_not_clean(tmp_path):
    root = install_adopter(tmp_path, None)
    proc = run_facade(root, ["local"], credentials=False)
    assert proc.returncode == 5, result_of(proc)
    assert result_of(proc) == "INCOMPLETE"
    assert "unconfigured" in proc.stdout.decode()


def test_e1_deletion_mutant_makes_unconfigured_stop_being_exit_five(
    tmp_path, serve
):
    """E-1's mutant: treat ``configured: false`` as a warning and the exit stops
    being 5, which is the state a CLEAN over an empty matrix comes from."""
    fixture = serve(api_responder())
    root = install_adopter(tmp_path, api_policy(fixture.port, configured=False))
    facade = root / "scripts" / "api_access_security.py"
    text = facade.read_text(encoding="utf-8")
    anchor = "        if not policy_obj.configured:\n"
    assert text.count(anchor) == 1
    facade.write_text(
        text.replace(anchor, "        if False:\n"), encoding="utf-8"
    )
    proc = run_facade(root, ["local"])
    assert proc.returncode != 5, result_of(proc)


def test_e2_configured_true_over_an_empty_matrix_is_a_schema_refusal(tmp_path):
    policy = api_policy(8099)
    policy["configured"] = True
    policy["local"]["operations"] = []
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], credentials=False)
    assert proc.returncode == 20
    assert "no_operations" in proc.stdout.decode()


@pytest.mark.parametrize("member", ("net.py", "policy.py", "report.py"))
def test_a10_a_missing_engine_member_exits_twenty_with_no_policy_read(
    tmp_path, member
):
    """A-10's facade half: DEGRADED before any policy read.

    The policy on disk is deliberately one the schema would refuse for a
    *different* reason, so "no policy read" is observable: an
    ``engine_incomplete`` refusal proves the facade stopped before reaching it.
    """
    policy = api_policy(8099, host="10.0.0.7")
    root = install_adopter(tmp_path, policy, drop_member=member)
    proc = run_facade(root, ["local"], credentials=False)
    assert proc.returncode == 20, proc.stdout
    text = proc.stdout.decode()
    assert "engine_incomplete" in text, text
    assert "non_loopback_target" not in text


def test_a10_a_complete_engine_does_not_report_engine_incomplete(
    tmp_path, serve
):
    fixture = serve(api_responder())
    root = install_adopter(tmp_path, api_policy(fixture.port))
    proc = run_facade(root, ["local"])
    assert "engine_incomplete" not in proc.stdout.decode()


# ---------------------------------------------------------------------------
# The redirect refusal, at the public path
# ---------------------------------------------------------------------------


def test_a_redirect_on_the_local_leg_is_degraded_not_evidence(tmp_path, serve):
    def responder(_record):
        return (
            b"HTTP/1.1 302 Found\r\nLocation: http://127.0.0.1:9/next\r\n"
            b"Content-Length: 0\r\nConnection: close\r\n\r\n"
        )

    fixture = serve(responder)
    root = install_adopter(tmp_path, api_policy(fixture.port))
    proc = run_facade(root, ["local"])
    assert proc.returncode == 20, result_of(proc)
    text = proc.stdout.decode()
    assert "redirect" in text
    assert "CLEAN" not in text
