# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
"""Public-path tests for ``scripts/web_hosting_security.py``.

Driven through the installed command line as subprocesses against local HTTP and
TLS fixtures whose headers, cookies, redirects and certificates the *test*
configures. Every "what was requested" assertion reads the fixture's own request
log, and the expectation table is authored outside the runner — so neither the
subject nor its oracle is derived from the other.

Certificates are generated into ``tmp_path`` and never committed.
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
    make_cert,
    tls_server_context,
    wait_for,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = REPO_ROOT / "templates" / "modules" / "team-gated"
FACADE_SRC = TEMPLATE_DIR / "web_hosting_security.py"
STUB_SRC = TEMPLATE_DIR / "web_hosting_policy_stub.json"
ENGINE_DST = "_web_hosting_security"

#: The complete set of headers a ``browser-app`` target must carry, and the
#: fixed check id each maps to.  Authored here, in the test, and compared with
#: what the runner reports -- not read from the runner's own table.
EXPECTED_HEADERS = {
    "hsts": ("Strict-Transport-Security", "max-age=63072000"),
    "nosniff": ("X-Content-Type-Options", "nosniff"),
    "referrer-policy": ("Referrer-Policy", "no-referrer"),
    "permissions-policy": ("Permissions-Policy", "geolocation=()"),
    "csp": ("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'"),
    "cross-origin-opener": ("Cross-Origin-Opener-Policy", "same-origin"),
}

BODY_WITH_LINKS = (
    b"<html><body><a href='/admin'>admin</a><a href='/secret'>s</a>"
    b"<form action='/login'></form><img src='/logo.png'></body></html>"
)


def install_adopter(tmp_path: Path, policy: "dict | None") -> Path:
    root = tmp_path / "adopter"
    scripts = root / "scripts"
    engine = scripts / ENGINE_DST
    engine.mkdir(parents=True)
    (root / "dev" / ".cairn").mkdir(parents=True)
    shutil.copy(FACADE_SRC, scripts / "web_hosting_security.py")
    for member in sorted(ENGINE_SRC.glob("*.py")):
        shutil.copy(member, engine / member.name)
    target = root / "dev" / ".cairn" / "web-hosting-policy.json"
    if policy is None:
        shutil.copy(STUB_SRC, target)
    else:
        target.write_text(json.dumps(policy, indent=2), encoding="utf-8")
    return root


def run_facade(root: Path, argv: "list[str]", *, ca: "Path | None" = None
               ) -> subprocess.CompletedProcess:
    """Run the facade with an explicitly constructed child environment.

    ``SSL_CERT_FILE`` is how the *platform trust store* is pointed at the test
    CA.  That is deliberate: it exercises the real
    ``ssl.create_default_context()`` path rather than weakening verification in
    the runner, which has no code path that could be weakened anyway.
    """
    env = {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONDONTWRITEBYTECODE": "1",
        "HOME": os.environ.get("HOME", ""),
        "TMPDIR": os.environ.get("TMPDIR", "/tmp"),
    }
    if ca is not None:
        env["SSL_CERT_FILE"] = str(ca)
    return subprocess.run(
        [sys.executable, str(root / "scripts" / "web_hosting_security.py"), *argv],
        capture_output=True, env=env, timeout=120,
    )


def https_responder(*, omit=(), cookies=(), body: bytes = b"ok"):
    """A fixture whose header table the test owns.

    ``omit`` names check ids to leave out, which is how criterion C-1 removes
    exactly one header per row.
    """

    def _responder(_record):
        lines = ["HTTP/1.1 200 OK"]
        for check_id, (header, value) in EXPECTED_HEADERS.items():
            if check_id in omit:
                continue
            lines.append(f"{header}: {value}")
        for cookie in cookies:
            lines.append(f"Set-Cookie: {cookie}")
        lines.append(f"Content-Length: {len(body)}")
        lines.append("Connection: close")
        return ("\r\n".join(lines) + "\r\n\r\n").encode("iso-8859-1") + body

    return _responder


def redirect_responder(location: str):
    def _responder(_record):
        return (
            f"HTTP/1.1 301 Moved\r\nLocation: {location}\r\n"
            f"Content-Length: 0\r\nConnection: close\r\n\r\n"
        ).encode("iso-8859-1")

    return _responder


def hosting_policy(*, https_origin: str, http_origin: "str | None" = None,
                   site_type: str = "browser-app",
                   redirect_hosts=("localhost", "127.0.0.1"),
                   csp=("default-src", "frame-ancestors"),
                   expect_cookies: bool = False,
                   configured: bool = True) -> dict:
    target: dict = {
        "id": "site", "https_origin": https_origin, "site_type": site_type,
        "permitted_redirect_hosts": list(redirect_hosts),
        "expected_csp_directives": list(csp),
        "expect_cookies": expect_cookies,
    }
    if http_origin is not None:
        target["http_origin"] = http_origin
    return {
        "schema": "cairn.security.web-hosting-policy.v1",
        "configured": configured,
        "local": {"targets": [target]},
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


@pytest.fixture()
def ca(tmp_path):
    cert, key = make_cert(tmp_path, "hosting", common_name="localhost")
    return cert, key


def result_of(proc) -> str:
    for line in proc.stdout.decode("utf-8", "replace").splitlines():
        if line.startswith("cairn-security-result:"):
            return line.split(":", 1)[1].strip()
    return f"<no result line> rc={proc.returncode}"


def observations(proc) -> "list[str]":
    return [
        line.strip() for line in proc.stdout.decode().splitlines()
        if line.strip().startswith("observation ")
    ]


# ---------------------------------------------------------------------------
# The positive control
# ---------------------------------------------------------------------------


def test_a_fully_conformant_local_target_is_clean(tmp_path, serve, ca):
    """Without this, every ``missing`` row below could be "nothing ever passes"."""
    cert, key = ca
    https = serve(https_responder(), tls=tls_server_context(cert, key))
    policy = hosting_policy(https_origin=f"https://localhost:{https.port}")
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], ca=cert)
    assert proc.returncode == 0, proc.stdout.decode() + proc.stderr.decode()
    assert result_of(proc) == "CLEAN"
    assert observations(proc) == []


# ---------------------------------------------------------------------------
# C-1 -- each check can fail for its own reason
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("check_id", sorted(EXPECTED_HEADERS))
def test_c1_removing_exactly_one_header_produces_exactly_that_observation(
    tmp_path, serve, ca, check_id
):
    """C-1: one header removed, one observation, and no other.

    ``and no other`` is the part that makes this table live: a runner that
    reported every check as missing whenever any was would pass a
    "the observation appears" assertion.
    """
    cert, key = ca
    https = serve(
        https_responder(omit=(check_id,)), tls=tls_server_context(cert, key)
    )
    policy = hosting_policy(https_origin=f"https://localhost:{https.port}")
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], ca=cert)
    assert proc.returncode == 10, result_of(proc)
    rows = observations(proc)
    seen = {
        part.split("=", 1)[1]
        for row in rows for part in row.split() if part.startswith("check_id=")
    }
    # Strictly one-to-one, including for ``csp``: an absent CSP header reports
    # the missing *header* and does **not** additionally report every reviewed
    # directive as missing, because the directive check is guarded on the header
    # being present. Measured, not predicted -- the first version of this test
    # expected the noisier behaviour and the runner was the better of the two.
    assert seen == {check_id}, rows


def test_c1_deletion_mutant_removing_a_check_makes_its_row_go_green(
    tmp_path, serve, ca
):
    """C-1's deletion mutant: with the HSTS row removed from the required set,
    the fixture that omits HSTS goes green -- which is the failure being
    prevented, so the test above must fail."""
    cert, key = ca
    https = serve(
        https_responder(omit=("hsts",)), tls=tls_server_context(cert, key)
    )
    policy = hosting_policy(https_origin=f"https://localhost:{https.port}")
    root = install_adopter(tmp_path, policy)
    facade = root / "scripts" / "web_hosting_security.py"
    text = facade.read_text(encoding="utf-8")
    anchor = '    ("hsts", "Strict-Transport-Security"),\n'
    assert text.count(anchor) == 1
    facade.write_text(text.replace(anchor, ""), encoding="utf-8")
    proc = run_facade(root, ["local"], ca=cert)
    assert proc.returncode == 0, result_of(proc)
    assert observations(proc) == []


def test_c1_a_cookie_missing_an_attribute_is_observed_without_its_value(
    tmp_path, serve, ca
):
    cert, key = ca
    https = serve(
        https_responder(cookies=("session=SECRETVALUE123; Path=/",)),
        tls=tls_server_context(cert, key),
    )
    policy = hosting_policy(
        https_origin=f"https://localhost:{https.port}", expect_cookies=True
    )
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], ca=cert)
    assert proc.returncode == 10, result_of(proc)
    text = proc.stdout.decode()
    assert "cookie-attribute" in text
    for attribute in ("secure", "httponly", "samesite"):
        assert f"[{attribute}]" in text
    # The cookie's value never crosses the boundary.
    assert "SECRETVALUE123" not in text
    assert "session" not in text


def test_c1_a_reviewed_csp_directive_that_is_absent_is_observed(
    tmp_path, serve, ca
):
    cert, key = ca
    headers = dict(EXPECTED_HEADERS)
    responder = https_responder()

    def weak_csp(_record):
        raw = responder(_record).decode("iso-8859-1")
        raw = raw.replace("; frame-ancestors 'none'", "")
        return raw.encode("iso-8859-1")

    https = serve(weak_csp, tls=tls_server_context(cert, key))
    policy = hosting_policy(https_origin=f"https://localhost:{https.port}")
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], ca=cert)
    assert proc.returncode == 10, result_of(proc)
    text = proc.stdout.decode()
    assert "csp-directive" in text
    assert "[frame-ancestors]" in text
    assert headers["csp"][1] not in text


# ---------------------------------------------------------------------------
# C-2 / C-3 -- redirect ordering and the exact allowlist
# ---------------------------------------------------------------------------


def test_c2_a_host_change_before_the_https_upgrade_is_a_finding(
    tmp_path, serve, ca
):
    """C-2: ``http://a`` -> ``http://b`` moves host over cleartext.

    Both hosts are loopback, so nothing leaves the machine; what the row tests
    is the *ordering*, which is independent of where the hosts point.
    """
    cert, key = ca
    https = serve(https_responder(), tls=tls_server_context(cert, key))
    http = serve(
        redirect_responder(f"http://localhost:{https.port}/"),
        host="127.0.0.1",
    )
    policy = hosting_policy(
        https_origin=f"https://localhost:{https.port}",
        http_origin=f"http://127.0.0.1:{http.port}",
    )
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], ca=cert)
    assert proc.returncode == 10, result_of(proc)
    text = proc.stdout.decode()
    assert "upgrade-before-host-change" in text
    assert "observation=invalid" in text


def test_c2_deletion_mutant_drops_the_ordering_assertion(tmp_path, serve, ca):
    cert, key = ca
    https = serve(https_responder(), tls=tls_server_context(cert, key))
    http = serve(
        redirect_responder(f"http://localhost:{https.port}/"), host="127.0.0.1"
    )
    policy = hosting_policy(
        https_origin=f"https://localhost:{https.port}",
        http_origin=f"http://127.0.0.1:{http.port}",
    )
    root = install_adopter(tmp_path, policy)
    facade = root / "scripts" / "web_hosting_security.py"
    text = facade.read_text(encoding="utf-8")
    anchor = '    if scheme == "http" and host is not None and host != origin.host:\n'
    assert text.count(anchor) == 1
    facade.write_text(
        text.replace(anchor, "    if False:\n"), encoding="utf-8"
    )
    proc = run_facade(root, ["local"], ca=cert)
    out = proc.stdout.decode()
    assert "upgrade-before-host-change" not in out


def test_c2_a_clean_upgrade_to_https_on_the_same_host_is_not_a_finding(
    tmp_path, serve, ca
):
    cert, key = ca
    https = serve(https_responder(), tls=tls_server_context(cert, key))
    http = serve(
        redirect_responder(f"https://localhost:{https.port}/"), host="localhost"
    )
    policy = hosting_policy(
        https_origin=f"https://localhost:{https.port}",
        http_origin=f"http://localhost:{http.port}",
    )
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], ca=cert)
    assert proc.returncode == 0, proc.stdout.decode()


def test_c2_an_http_origin_that_does_not_redirect_at_all_is_a_finding(
    tmp_path, serve, ca
):
    cert, key = ca
    https = serve(https_responder(), tls=tls_server_context(cert, key))
    http = serve(https_responder(), host="127.0.0.1")
    policy = hosting_policy(
        https_origin=f"https://localhost:{https.port}",
        http_origin=f"http://127.0.0.1:{http.port}",
    )
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], ca=cert)
    assert proc.returncode == 10, result_of(proc)
    assert "http-upgrade" in proc.stdout.decode()


def test_c3_a_redirect_outside_the_exact_allowlist_is_reported(
    tmp_path, serve, ca
):
    cert, key = ca
    https = serve(https_responder(), tls=tls_server_context(cert, key))
    http = serve(
        redirect_responder("https://elsewhere.test/"), host="127.0.0.1"
    )
    policy = hosting_policy(
        https_origin=f"https://localhost:{https.port}",
        http_origin=f"http://127.0.0.1:{http.port}",
        redirect_hosts=("127.0.0.1",),
    )
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], ca=cert)
    assert proc.returncode == 10, result_of(proc)
    text = proc.stdout.decode()
    assert "redirect-allowlist" in text
    # The redirect URL itself never crosses the boundary.
    assert "elsewhere.test" not in text


# ---------------------------------------------------------------------------
# C-4 -- no crawl, no payload
# ---------------------------------------------------------------------------


def test_c4_only_the_declared_requests_are_sent(tmp_path, serve, ca):
    """C-4: asserted against the *fixture's* log, not the runner's intent.

    The body is full of links, a form and an image. A crawler would follow at
    least one of them.
    """
    cert, key = ca
    https = serve(
        https_responder(body=BODY_WITH_LINKS), tls=tls_server_context(cert, key)
    )
    policy = hosting_policy(https_origin=f"https://localhost:{https.port}")
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], ca=cert)
    assert proc.returncode == 0, proc.stdout.decode()
    assert wait_for(lambda: len(https.records) == 1)
    record = https.records[0]
    assert (record.method, record.target) == ("GET", "/")
    assert [(r.method, r.target) for r in https.records] == [("GET", "/")]
    # No payload: the declared GET carries no body at all.
    assert record.body == b""


# ---------------------------------------------------------------------------
# C-5 -- local is not deployed
# ---------------------------------------------------------------------------


def test_c5_local_clean_never_presents_as_deployed_clean(tmp_path, serve, ca):
    cert, key = ca
    https = serve(https_responder(), tls=tls_server_context(cert, key))
    policy = hosting_policy(https_origin=f"https://localhost:{https.port}")
    root = install_adopter(tmp_path, policy)
    human = run_facade(root, ["local"], ca=cert)
    assert "not a deployed CLEAN" in human.stdout.decode()
    assert "deployed leg has not executed" in human.stdout.decode()

    child = run_facade(root, ["local", "--child-document"], ca=cert)
    document = json.loads(child.stdout.decode())
    assert document["evidence_mode"] == "loopback"
    assert document["result"] == "CLEAN"
    assert isinstance(document["details"], str), (
        "the activation dispatcher's _evaluate_capability requires "
        "isinstance(details, str); a nested object degrades every real leg"
    )
    assert "not a deployed CLEAN" in document["details"]

    report_path = None
    for line in human.stdout.decode().splitlines():
        if line.strip().startswith("report:"):
            report_path = Path(line.split("report:", 1)[1].strip())
    assert report_path is not None
    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        assert payload["evidence_mode"] == "loopback"
        assert payload["deployed_leg_executed"] is False
    finally:
        shutil.rmtree(report_path.parent, ignore_errors=True)


def test_c5_deletion_mutant_removes_the_not_deployed_statement(
    tmp_path, serve, ca
):
    cert, key = ca
    https = serve(https_responder(), tls=tls_server_context(cert, key))
    policy = hosting_policy(https_origin=f"https://localhost:{https.port}")
    root = install_adopter(tmp_path, policy)
    facade = root / "scripts" / "web_hosting_security.py"
    text = facade.read_text(encoding="utf-8")
    anchor = '''            notes=() if deployed else (
                "loopback evidence only: the deployed leg has not executed, "
                "and a local CLEAN is not a deployed CLEAN",
            ),'''
    assert text.count(anchor) == 1
    facade.write_text(text.replace(anchor, "            notes=(),"),
                      encoding="utf-8")
    proc = run_facade(root, ["local"], ca=cert)
    assert "not a deployed CLEAN" not in proc.stdout.decode()


# ---------------------------------------------------------------------------
# The actor boundary and the stub
# ---------------------------------------------------------------------------


def test_local_refuses_a_non_loopback_target(tmp_path):
    policy = hosting_policy(https_origin="https://example.test")
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"])
    assert proc.returncode == 20, result_of(proc)
    assert "non_loopback_target" in proc.stdout.decode()


def test_a_deployed_target_pointing_at_loopback_is_refused(tmp_path):
    """"deployed CLEAN" cannot be manufactured by aiming the deployed leg at a
    local fixture."""
    policy = hosting_policy(https_origin="https://localhost:9443")
    policy["deployed"] = {"targets": [{
        "id": "prod", "https_origin": "https://127.0.0.1:9443",
        "site_type": "static",
    }]}
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"])
    assert proc.returncode == 20
    assert "non_loopback_target" in proc.stdout.decode()


@pytest.mark.parametrize("supplied", (
    "https://example.test/", "HTTPS://EXAMPLE.TEST", "https://example.test:443",
    "http://example.test", "https://example.test?a=1",
))
def test_deployed_refuses_every_near_miss(tmp_path, supplied):
    policy = hosting_policy(https_origin="https://localhost:9443")
    policy["deployed"] = {"targets": [{
        "id": "prod", "https_origin": "https://example.test",
        "site_type": "static",
    }]}
    root = install_adopter(tmp_path, policy)
    proc = run_facade(
        root, ["deployed-passive", "--authorize-base-url", supplied]
    )
    assert proc.returncode == 20, result_of(proc)
    assert "authorization_mismatch" in proc.stdout.decode()


def test_the_untouched_stub_is_incomplete(tmp_path):
    root = install_adopter(tmp_path, None)
    proc = run_facade(root, ["local"])
    assert proc.returncode == 5, result_of(proc)
    assert result_of(proc) == "INCOMPLETE"


def test_configured_true_with_no_targets_is_a_schema_refusal(tmp_path):
    policy = hosting_policy(https_origin="https://localhost:9443")
    policy["local"]["targets"] = []
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"])
    assert proc.returncode == 20
    assert "no_targets" in proc.stdout.decode()


def test_no_grade_appears_anywhere_in_the_runner_or_its_output(
    tmp_path, serve, ca
):
    """The refusal to issue a grade, asserted rather than asserted-in-prose."""
    cert, key = ca
    https = serve(
        https_responder(omit=("hsts", "csp")), tls=tls_server_context(cert, key)
    )
    policy = hosting_policy(https_origin=f"https://localhost:{https.port}")
    root = install_adopter(tmp_path, policy)
    proc = run_facade(root, ["local"], ca=cert)
    text = proc.stdout.decode()
    for token in ("grade", "score", "A+", "rating"):
        assert token not in text.lower().replace("upgrade", ""), token


def test_the_facade_exposes_exactly_two_subcommands(tmp_path):
    root = install_adopter(tmp_path, None)
    proc = run_facade(root, ["--help"])
    text = proc.stdout.decode()
    assert "local" in text and "deployed-passive" in text
    assert "allow-mutation" not in text
    source = FACADE_SRC.read_text(encoding="utf-8")
    assert "allow_mutation" not in source
