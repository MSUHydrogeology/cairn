# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
"""The cross-runner confidentiality sweep — Chunk D, the AW6/AW8 gate.

Every test here drives an **installed facade as a subprocess** against a
loopback fixture whose raw bytes the test authors, then sweeps *every* sink the
run can write: raw stdout bytes, raw stderr bytes, the complete report file, and
every byte of every file under a test-owned temporary root the child is pointed
at.  The oracle is a high-entropy marker the *test* invented and planted in a
fixture the runner does not read as configuration, so the independence is
structural: the runner has no way to know the marker is special.

Perturbations are applied to a **copy** of the runner in ``tmp_path`` and never
to the repository tree, so there is nothing to restore; each perturbation anchor
must match exactly once, so a mutant that silently stopped applying fails loudly
instead of passing as a green test.

Two measured corrections to D-2's stated instrument
---------------------------------------------------

**(1) The ``_CHANNEL_PASSTHROUGH`` seam cannot demonstrate liveness for any
channel.**  D-2 specifies phase (a) as *"suppress sanitization for that channel
only … assert the marker does appear"*, and the engine ships a seam built for
exactly that.  Measured: ``sanitize_channel`` has exactly **two** live call sites
in the shipped engine (``net.py`` writing ``Response.reason_withheld`` and
``Response.redirect_withheld``), and **both attributes are written and never
read** — no facade, check, finding, report field, summary line or child document
consumes either.  The other eleven ``CHANNEL_TOKENS`` entries have **no call site
at all**.  So suppression leaks nothing anywhere, and the seam is inert.
:func:`test_d2_the_channel_passthrough_seam_cannot_demonstrate_liveness` pins
that measurement, and fails the day a consumer is wired up.

**(2) The property is structural absence, not redaction — so phase (a) is a leak
injection.**  There is no shipped code path that writes a peer-supplied or
credential string to stdout, stderr or the report.  You cannot delete an absence.
Phase (a) therefore *adds* the emission at the site where the raw value is in
scope and requires the sweep to find the marker; phase (b) restores the pristine
runner and requires absence.  That proves both halves D-2 asks for — the runner
really reaches the channel, and the sweep really would catch a leak there — and
is a stronger liveness argument than a suppression nothing reads.

Every channel's disposition is recorded in :data:`CHANNEL_LEDGER` and
:data:`UNCOVERED_CHANNELS`, and :func:`test_d2_every_channel_token_has_a_recorded
_disposition` fails if a channel token is added to the engine without one.  A
channel with no available instrument is recorded as **uncovered**, per D-2, and
never as clean.

**One chokepoint does most of the work, and is tested as one.**
``SecurityRefusal.__init__`` clamps its ``reason`` to ``REASON_TOKENS`` and its
``code`` to ``ERROR_CODES``, so *no* refusal — from any handler, for any peer,
policy or exception input — can carry content.  That closes the exception-text,
timeout-diagnostic and TLS-failure channels as a **class** rather than one at a
time, and it is tested with a real deletion mutant (remove the clamp; the marker
arrives).  Recorded rather than hidden: this is why those three channels have no
per-channel injection row.

**A later addition: the activation dispatcher's own aggregate report.**
Everything above drives an installed facade directly and has nothing to do
with ``run_security_verification.py`` -- the child ``details`` document was a
JSON object until the fix this addition follows, and the dispatcher's own
``_evaluate_capability`` DEGRADED any real leg that reached it, so there was
no sink there to sweep.  With ``details`` now a single string built by
``_security_net/report.py``'s ``render_details``, it reaches the
dispatcher's OWN aggregate report for the first time, which makes that
report a NEW, previously-unswept sink.
:class:`TestTheDispatcherAggregateReportIsANewSweptSink` at the end of this
file covers it -- through a real subprocess chain (this file's own
hand-assembled dispatcher install spawning the real facade as its child,
never a synthetic ``RegistryEntry``), on the one leg reachable without a
credential or a trusted TLS peer (see that class's own docstring for why
that is the reachable leg, not a live FINDINGS run).
"""
from __future__ import annotations

import hashlib
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
)

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = REPO_ROOT / "templates" / "modules" / "team-gated"

API_FACADE_SRC = TEMPLATE_DIR / "api_access_security.py"
API_STUB_SRC = TEMPLATE_DIR / "api_access_policy_stub.json"
API_ENGINE_DST = "_api_access_security"
API_POLICY_REL = "dev/.cairn/api-access-policy.json"

HOSTING_FACADE_SRC = TEMPLATE_DIR / "web_hosting_security.py"
HOSTING_STUB_SRC = TEMPLATE_DIR / "web_hosting_policy_stub.json"
HOSTING_ENGINE_DST = "_web_hosting_security"
HOSTING_POLICY_REL = "dev/.cairn/web-hosting-policy.json"


# ---------------------------------------------------------------------------
# Markers — one per channel, planted independently (D1)
# ---------------------------------------------------------------------------
# High-entropy, ASCII, and free of HTTP structural bytes, so a marker can sit in
# a status line, a header value, a cookie, a JSON string or an environment
# variable without changing the shape of what the runner parses.  Distinct per
# channel, so a sweep hit names the channel that leaked rather than "something".

MARKERS: dict[str, str] = {
    "reason_phrase": "MkRSN7q4Zx1LpVn",
    "redirect_location": "MkRDR3w8Yc5TbQm",
    "response_header": "MkHDR9r2Fk6JdWs",
    "set_cookie": "MkCKI5t1Nb8HgZp",
    "response_body": "MkBDY2y7Qm4RvXc",
    "json_pointer_value": "MkJPV8u3Ld9KwTf",
    "collection_member": "MkCLM6i5Vp2MsYb",
    "credential": "MkCRD4o9Ws7BnLq",
    "policy_label": "MkLBL3d2Xh5QrWt",
    "exception_text": "MkEXC1a6Zt3GpRd",
    "timeout_diagnostic": "MkTMO7s4Cv8NkJm",
    "certificate_subject": "MkCRT9f7Bm1YvZn",
    "request_body": "MkREQ5g8Kp3TdLc",
}

#: Channels closed at the refusal chokepoint rather than by a per-channel
#: injection, with the measured reason.  Each is genuinely *covered* — by
#: :func:`test_d2_the_refusal_chokepoint_closes_the_diagnostic_channel_class`,
#: which carries its own deletion mutant — but not by an end-to-end row, and the
#: distinction is recorded rather than blurred.
CHOKEPOINT_CHANNELS: dict[str, str] = {
    "exception_text": (
        "every handler in net.py raises SecurityRefusal with a LITERAL token and "
        "`from None`; the constructor then clamps any reason outside "
        "REASON_TOKENS to 'unspecified'. Python's own exception messages on "
        "these paths (SSLCertVerificationError, socket.timeout, "
        "UnicodeEncodeError) carry no peer payload either, so no marker can be "
        "planted into one to begin with."
    ),
    "timeout_diagnostic": (
        "a timeout diagnostic is a fixed token pair (timeout:connect_timeout / "
        "timeout:read_timeout); socket.timeout's text is 'timed out', which "
        "carries nothing plantable. Closed by the same constructor clamp."
    ),
    "certificate_subject": (
        "no engine member calls getpeercert() or reads any certificate field, so "
        "the subject never enters the runner's data; and a TLS failure is "
        "reported by mapping OpenSSL's numeric verify CODE to a fixed token, "
        "never by reading the verification message. Pinned by "
        "test_d2_no_engine_member_reads_a_certificate_field."
    ),
}

#: Channels with **no** available instrument of either kind.  Recorded as
#: uncovered per D-2 — never as clean.  A channel leaves this map by a
#: measurement, not by an argument.
UNCOVERED_CHANNELS: dict[str, str] = {
    "request_body": (
        "a declared request body is policy-supplied and is written to the socket "
        "by net._build_request; no finding, report field, summary line or child "
        "document takes it as an argument, so there is no existing site at which "
        "to inject it without inventing one. It is covered only by the aggregate "
        "sweep (D-1), which plants the marker in a declared body and finds it in "
        "no sink -- an absence assertion whose liveness is unproven."
    ),
}


# ---------------------------------------------------------------------------
# Installed adopters, with per-copy perturbation
# ---------------------------------------------------------------------------


def _apply_edits(path: Path, replacements) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        count = text.count(old)
        assert count == 1, (
            f"perturbation anchor is not unique in {path.name}: {old!r} occurs "
            f"{count} times"
        )
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def install(tmp_path: Path, kind: str, policy: "dict | None", *,
            engine_edits=None, facade_edits=None, name: str = "adopter") -> Path:
    """Lay a capability out at its real install destinations.

    Copied to the destinations ``_MODULE_MAPPINGS`` declares rather than run
    through the scaffold, matching the sibling suites: a facade defect cannot be
    masked by an installer defect or vice versa.
    """
    if kind == "api":
        facade_src, engine_dst = API_FACADE_SRC, API_ENGINE_DST
        stub_src, policy_rel = API_STUB_SRC, API_POLICY_REL
    else:
        facade_src, engine_dst = HOSTING_FACADE_SRC, HOSTING_ENGINE_DST
        stub_src, policy_rel = HOSTING_STUB_SRC, HOSTING_POLICY_REL

    root = tmp_path / name
    scripts = root / "scripts"
    engine = scripts / engine_dst
    engine.mkdir(parents=True)
    (root / "dev" / ".cairn").mkdir(parents=True)

    facade = scripts / facade_src.name
    shutil.copy(facade_src, facade)
    if facade_edits:
        _apply_edits(facade, facade_edits)

    for member in sorted(ENGINE_SRC.glob("*.py")):
        shutil.copy(member, engine / member.name)
    for member_name, replacements in (engine_edits or {}).items():
        _apply_edits(engine / member_name, replacements)

    target = root / policy_rel
    if policy is None:
        shutil.copy(stub_src, target)
    else:
        target.write_text(json.dumps(policy, indent=2), encoding="utf-8")
    return root


class Run:
    """One completed run, plus every sink it could have written to."""

    def __init__(self, proc: subprocess.CompletedProcess, tmproot: Path) -> None:
        self.proc = proc
        self.tmproot = tmproot

    @property
    def returncode(self) -> int:
        return self.proc.returncode

    @property
    def result(self) -> str:
        for line in self.proc.stdout.decode("utf-8", "replace").splitlines():
            if line.startswith("cairn-security-result:"):
                return line.split(":", 1)[1].strip()
        return (
            f"<no result line> rc={self.proc.returncode} "
            f"stdout={self.proc.stdout!r} stderr={self.proc.stderr!r}"
        )

    def temp_files(self) -> "list[Path]":
        if not self.tmproot.exists():
            return []
        return sorted(p for p in self.tmproot.rglob("*") if p.is_file())

    def report_path(self) -> Path:
        reports = [p for p in self.temp_files() if p.name == "report.json"]
        assert len(reports) == 1, f"expected one report.json, got {reports}"
        return reports[0]

    def report(self) -> dict:
        return json.loads(self.report_path().read_text(encoding="utf-8"))

    def sinks(self) -> "list[tuple[str, bytes]]":
        """Every sink as raw **bytes**.

        Bytes, not text: a decode step can normalize away exactly the sequence a
        terminal-integrity assertion looks for, and a marker that survived as
        latin-1 in a header would be invisible to a ``str`` comparison that
        replaced it.
        """
        out: list[tuple[str, bytes]] = [
            ("stdout", self.proc.stdout),
            ("stderr", self.proc.stderr),
        ]
        for path in self.temp_files():
            out.append(
                (f"tmp:{path.relative_to(self.tmproot)}", path.read_bytes())
            )
        return out

    def occurrences(self, needle: str) -> "list[str]":
        """Sinks carrying ``needle``.  Empty means it leaked nowhere."""
        raw = needle.encode("utf-8")
        return [name for name, blob in self.sinks() if raw in blob]


def run(root: Path, kind: str, argv: "list[str]", *, tmproot: Path,
        env_extra=None, ca: "Path | None" = None) -> Run:
    """Run the installed facade with an explicitly constructed environment.

    ``TMPDIR`` is pointed at a **test-owned** directory, so "scan the whole
    temporary directory" is a scan of a bounded tree this test created rather
    than of the platform temporary root shared with every other process.  It is
    a *sibling* of the adopter, so the runner's own containment check — which
    refuses a report directory inside the repository — still passes.

    The environment is built here in full rather than derived from
    ``os.environ``: an expectation derived from the parent cannot be compared
    against a child the interpreter may have added variables to.
    """
    tmproot.mkdir(parents=True, exist_ok=True)
    script = (
        "api_access_security.py" if kind == "api" else "web_hosting_security.py"
    )
    env = {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONDONTWRITEBYTECODE": "1",
        "HOME": os.environ.get("HOME", ""),
        "TMPDIR": str(tmproot),
    }
    if ca is not None:
        env["SSL_CERT_FILE"] = str(ca)
    env.update(env_extra or {})
    proc = subprocess.run(
        [sys.executable, str(root / "scripts" / script), *argv],
        capture_output=True, env=env, timeout=120,
    )
    return Run(proc, tmproot)


@pytest.fixture()
def tmproot(tmp_path):
    path = tmp_path / "tmproot"
    path.mkdir()
    return path


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


# ---------------------------------------------------------------------------
# Policies and fixtures the test owns (D1)
# ---------------------------------------------------------------------------

API_CREDS = {
    "CAIRN_API_P1_CREDENTIAL": MARKERS["credential"] + "p1",
    "CAIRN_API_P2_CREDENTIAL": MARKERS["credential"] + "p2",
}


def api_policy(port: int, *, host: str = "127.0.0.1", body: "str | None" = None,
               role: "str | None" = None, configured: bool = True) -> dict:
    authority = f"[{host}]" if ":" in host else host
    operation: dict = {
        "id": "read-order", "method": "GET", "path": "/orders/1",
        "kind": "object",
        "cases": [
            {"id": "owner-reads", "principal": "p1", "expect": "allow",
             "status": [200], "require_present": ["/id"],
             "require_absent": ["/internal_note", "/tags", "/free_text"]},
            {"id": "other-denied", "principal": "p2", "expect": "deny",
             "status": [403, 404]},
        ],
    }
    if body is not None:
        operation["method"] = "POST"
        operation["body"] = body
    principals: list = [{"id": "p1", "role": role or "owner"}, {"id": "p2"}]
    return {
        "schema": "cairn.security.api-access-policy.v1",
        "configured": configured,
        "local": {
            "base_url": f"http://{authority}:{port}",
            "environment": "local",
            "principals": principals,
            "operations": [operation],
        },
    }


def api_responder(*, reason: str = "OK", overexpose: "str | None" = None,
                  tags: "list | None" = None, cookie: "str | None" = None,
                  header: "str | None" = None, location: "str | None" = None,
                  free_text: "str | None" = None, deny: bool = True):
    """A fixture API in which every channel can carry a planted marker."""

    def _responder(record):
        if location is not None:
            return (
                f"HTTP/1.1 302 {reason}\r\nLocation: {location}\r\n"
                f"Content-Length: 0\r\nConnection: close\r\n\r\n"
            ).encode("iso-8859-1")
        auth = record.header("Authorization") or ""
        is_owner = API_CREDS["CAIRN_API_P1_CREDENTIAL"] in auth
        if deny and not is_owner:
            blob = b'{"error":"forbidden"}'
            head = [f"HTTP/1.1 403 {reason}", "Content-Type: application/json",
                    f"Content-Length: {len(blob)}", "Connection: close"]
            return ("\r\n".join(head) + "\r\n\r\n").encode("iso-8859-1") + blob
        payload: dict = {"id": "1", "owner": "p1"}
        if overexpose is not None:
            payload["internal_note"] = overexpose
        if tags is not None:
            payload["tags"] = tags
        if free_text is not None:
            payload["free_text"] = free_text
        blob = json.dumps(payload).encode("utf-8")
        lines = [f"HTTP/1.1 200 {reason}", "Content-Type: application/json"]
        if cookie is not None:
            lines.append(f"Set-Cookie: {cookie}")
        if header is not None:
            lines.append(f"X-Diagnostic: {header}")
        lines += [f"Content-Length: {len(blob)}", "Connection: close"]
        return ("\r\n".join(lines) + "\r\n\r\n").encode("iso-8859-1") + blob

    return _responder


HOSTING_HEADERS = {
    "hsts": ("Strict-Transport-Security", "max-age=63072000"),
    "nosniff": ("X-Content-Type-Options", "nosniff"),
    "referrer-policy": ("Referrer-Policy", "no-referrer"),
    "permissions-policy": ("Permissions-Policy", "geolocation=()"),
    "csp": ("Content-Security-Policy",
            "default-src 'self'; frame-ancestors 'none'"),
    "cross-origin-opener": ("Cross-Origin-Opener-Policy", "same-origin"),
}


def hosting_policy(*, https_origin: str,
                   csp=("default-src", "frame-ancestors")) -> dict:
    return {
        "schema": "cairn.security.web-hosting-policy.v1",
        "configured": True,
        "local": {"targets": [{
            "id": "site", "https_origin": https_origin,
            "site_type": "browser-app",
            "permitted_redirect_hosts": ["localhost", "127.0.0.1"],
            "expected_csp_directives": list(csp),
            "expect_cookies": False,
        }]},
    }


def hosting_responder(*, omit=("hsts",), cookies=(),
                      extra: "tuple[str, str] | None" = None):
    """A hosting fixture that always yields at least one finding.

    ``omit`` defaults to dropping HSTS so every run produces a finding: a
    confidentiality sweep over a run with no findings would be vacuous.
    """

    def _responder(_record):
        lines = ["HTTP/1.1 200 OK"]
        for check_id, (header, value) in HOSTING_HEADERS.items():
            if check_id in omit:
                continue
            lines.append(f"{header}: {value}")
        for cookie in cookies:
            lines.append(f"Set-Cookie: {cookie}")
        if extra is not None:
            lines.append(f"{extra[0]}: {extra[1]}")
        lines += ["Content-Length: 2", "Connection: close"]
        return ("\r\n".join(lines) + "\r\n\r\n").encode("iso-8859-1") + b"ok"

    return _responder


# ---------------------------------------------------------------------------
# Leak-injection perturbations, one per covered channel
# ---------------------------------------------------------------------------
# Each entry is the single edit that makes the named channel's raw value reach an
# output sink.  The anchor is asserted unique by _apply_edits, so an edit that
# stopped applying is a loud failure rather than a silent green.

#: ``build_finding`` keeps only a bucket of ``observed_value``; appending the
#: raw value to ``detail`` is the injection for every API channel that routes
#: through an observed value.
_LEAK_OBSERVED_VALUE = {
    "report.py": [(
        '    finding["detail"] = scrub_terminal(detail)',
        '    finding["detail"] = scrub_terminal(detail) + "|" + str(observed_value)',
    )],
}

#: ``_observe`` builds a hosting finding from a response whose header values it
#: never passes on; appending the whole header list is the injection for every
#: hosting response channel.
_LEAK_HOSTING_HEADERS = (
    (
        "    finding = engine_report.build_finding(\n"
        "        check_id=check_id, target_id=target_id, method=method,",
        "    detail = detail + \"|\" + repr(getattr(response, 'headers', None))\n"
        "    finding = engine_report.build_finding(\n"
        "        check_id=check_id, target_id=target_id, method=method,",
    ),
)

#: The reason phrase reaches ``sanitize_channel`` and stops there.  Writing it to
#: stdout at that exact site is the injection, and it doubles as the proof that
#: the runner parses a reason phrase at all.
_LEAK_REASON_PHRASE = {
    "net.py": [(
        '    response.reason_withheld = sanitize_channel(\n'
        '        "reason_phrase", pieces[2] if len(pieces) > 2 else ""\n'
        '    )',
        '    import sys as _leaksys\n'
        '    _leaksys.stdout.write("LEAK-REASON " + (pieces[2] if len(pieces) > 2 else "") + "\\n")\n'
        '    response.reason_withheld = sanitize_channel(\n'
        '        "reason_phrase", pieces[2] if len(pieces) > 2 else ""\n'
        '    )',
    )],
}

#: Likewise for the ``Location`` value on a 3xx.
_LEAK_REDIRECT_LOCATION = {
    "net.py": [(
        '        response.redirect_withheld = sanitize_channel("redirect_location", location)',
        '        import sys as _leaksys\n'
        '        _leaksys.stdout.write("LEAK-LOCATION " + str(location) + "\\n")\n'
        '        response.redirect_withheld = sanitize_channel("redirect_location", location)',
    )],
}

#: A credential value is in scope in the API facade's matrix runner and reaches
#: no sink; writing it is the injection.
_LEAK_CREDENTIAL = (
    (
        "    fingerprinter = engine_report.Fingerprinter()",
        "    import sys as _leaksys\n"
        "    _leaksys.stdout.write('LEAK-CRED ' + repr(sorted(credentials.values())) + '\\n')\n"
        "    fingerprinter = engine_report.Fingerprinter()",
    ),
)

#: A policy label refused for length: the offending text is in scope at the
#: refusal and reaches no sink.
_LEAK_POLICY_LABEL = {
    "policy.py": [(
        '    if len(text) > max_len:\n        _refuse("label_too_long")',
        '    if len(text) > max_len:\n'
        '        import sys as _leaksys\n'
        '        _leaksys.stdout.write("LEAK-LABEL " + text + "\\n")\n'
        '        _refuse("label_too_long")',
    )],
}


# ===========================================================================
# D-1 — the aggregate sweep, and the proof that it is not decoration
# ===========================================================================


def test_d1_no_planted_marker_reaches_any_sink(tmp_path, tmproot, serve):
    """D-1: eight markers planted independently and simultaneously leak nowhere.

    Channels planted in one run: the reason phrase, an overexposed JSON
    property, an array member, a ``Set-Cookie``, a response header, a body
    property, a policy-declared request body, and both credentials.  Sinks swept:
    raw stdout bytes, raw stderr bytes, the complete report file, and every byte
    of every file under the child's temporary root.
    """
    fixture = serve(api_responder(
        reason=MARKERS["reason_phrase"],
        overexpose=MARKERS["json_pointer_value"],
        tags=[MARKERS["collection_member"], "b", "c"],
        cookie=f"sid={MARKERS['set_cookie']}; Path=/",
        header=MARKERS["response_header"],
        free_text=MARKERS["response_body"],
        deny=False,
    ))
    root = install(tmp_path, "api", api_policy(fixture.port))
    result = run(root, "api", ["local"], tmproot=tmproot, env_extra=API_CREDS)

    # A sweep over a run that produced no evidence is the vacuous pass D-2
    # exists to forbid, so the run's own outcome is asserted first.
    assert result.result == "FINDINGS", result.result
    assert result.returncode == 10
    assert result.report()["findings"], "no findings -- the sweep would be vacuous"

    for channel in ("reason_phrase", "json_pointer_value", "collection_member",
                    "set_cookie", "response_header", "response_body"):
        assert result.occurrences(MARKERS[channel]) == [], channel
    for value in API_CREDS.values():
        assert result.occurrences(value) == []


def test_d1_the_sweep_reddens_when_the_value_omission_step_is_deleted(
    tmp_path, tmproot, serve
):
    """D-1's deletion mutant: ``build_finding`` keeps the raw observed value.

    A sweep that stays green with the value-omission step removed is decoration.
    """
    fixture = serve(api_responder(overexpose=MARKERS["json_pointer_value"],
                                 deny=False))
    policy = api_policy(fixture.port)
    leaky = install(
        tmp_path, "api", policy, name="leaky",
        engine_edits={"report.py": [(
            '        finding["observed_magnitude"] = value_magnitude(observed_value)',
            '        finding["observed_magnitude"] = str(observed_value)',
        )]},
    )
    result = run(leaky, "api", ["local"], tmproot=tmproot, env_extra=API_CREDS)
    assert result.result == "FINDINGS", result.result
    hits = result.occurrences(MARKERS["json_pointer_value"])
    assert hits, "the deletion mutant did not leak -- the sweep proves nothing"
    assert "stdout" in hits
    assert any(name.startswith("tmp:") for name in hits), hits

    clean = install(tmp_path, "api", policy, name="clean")
    after = run(clean, "api", ["local"], tmproot=tmproot / "b",
                env_extra=API_CREDS)
    assert after.result == "FINDINGS", after.result
    assert after.occurrences(MARKERS["json_pointer_value"]) == []


# ===========================================================================
# D-2 — per channel: liveness (a) first, then confidentiality (b)
# ===========================================================================
# Both phases run inside one test per channel, so they can never drift apart
# into "the absence assertion still passes because the runner stopped reaching
# the channel".


def _api_channel(tmp_path, tmproot, port, *, responder_marker_kwargs,
                 engine_edits=None, facade_edits=None, policy_kwargs=None,
                 expect_leaky_result=None, expect_clean_result="FINDINGS"):
    policy = api_policy(port, **(policy_kwargs or {}))
    leaky = install(tmp_path, "api", policy, name="leaky",
                    engine_edits=engine_edits, facade_edits=facade_edits)
    clean = install(tmp_path, "api", policy, name="clean")
    a = run(leaky, "api", ["local"], tmproot=tmproot / "a", env_extra=API_CREDS)
    b = run(clean, "api", ["local"], tmproot=tmproot / "b", env_extra=API_CREDS)
    if expect_leaky_result is not None:
        assert a.result == expect_leaky_result, a.result
    if expect_clean_result is not None:
        assert b.result == expect_clean_result, b.result
    return a, b


CHANNEL_LEDGER: dict[str, str] = {
    "json_pointer_value": "leak injection: build_finding keeps observed_value",
    "collection_member": "leak injection: build_finding keeps observed_value",
    "response_body": "leak injection: build_finding keeps observed_value",
    "reason_phrase": "leak injection: net._read_response writes the raw reason",
    "redirect_location": "leak injection: net._read_response writes raw Location",
    "credential": "leak injection: the facade's matrix runner writes credentials",
    "policy_label": "leak injection: policy._clean_str writes the refused label",
    "response_header": "leak injection: hosting _observe carries raw headers",
    "set_cookie": "leak injection: hosting _observe carries raw headers",
}


def test_d2_every_channel_token_has_a_recorded_disposition():
    """No channel may be added to the engine without a disposition here.

    The three maps partition ``CHANNEL_TOKENS`` exactly.  A new channel token
    with no entry fails this test rather than silently reading as covered.
    """
    tokens = _shipped_channel_tokens()
    recorded = (set(CHANNEL_LEDGER) | set(CHOKEPOINT_CHANNELS)
                | set(UNCOVERED_CHANNELS))
    assert tokens == recorded, {
        "in engine, no disposition": sorted(tokens - recorded),
        "disposition for an absent channel": sorted(recorded - tokens),
    }
    # And the three maps do not overlap: a channel is covered one way only.
    assert not (set(CHANNEL_LEDGER) & set(CHOKEPOINT_CHANNELS))
    assert not (set(CHANNEL_LEDGER) & set(UNCOVERED_CHANNELS))
    assert not (set(CHOKEPOINT_CHANNELS) & set(UNCOVERED_CHANNELS))
    assert set(MARKERS) == tokens


def _shipped_channel_tokens() -> "set[str]":
    text = (ENGINE_SRC / "report.py").read_text(encoding="utf-8")
    start = text.index("CHANNEL_TOKENS = {")
    end = text.index("}", start)
    block = text[start:end]
    return {
        line.split('"')[1]
        for line in block.splitlines()[1:]
        if line.strip().startswith('"')
    }


def test_d2_the_channel_passthrough_seam_cannot_demonstrate_liveness(
    tmp_path, tmproot, serve
):
    """The first measured correction, pinned rather than left as prose.

    ``_CHANNEL_PASSTHROUGH`` is D-2's stated instrument.  Turning it on for
    ``reason_phrase`` leaks nothing, because ``Response.reason_withheld`` has no
    consumer.  This test fails the day one is wired up — which is the day the
    seam becomes usable and this module's docstring becomes stale.
    """
    fixture = serve(api_responder(reason=MARKERS["reason_phrase"], deny=False))
    root = install(
        tmp_path, "api", api_policy(fixture.port),
        engine_edits={"report.py": [(
            "_CHANNEL_PASSTHROUGH: frozenset = frozenset()",
            '_CHANNEL_PASSTHROUGH: frozenset = frozenset({"reason_phrase"})',
        )]},
    )
    result = run(root, "api", ["local"], tmproot=tmproot, env_extra=API_CREDS)
    assert result.result == "FINDINGS", result.result
    assert result.occurrences(MARKERS["reason_phrase"]) == [], (
        "the passthrough seam DID leak: reason_withheld has gained a consumer "
        "and this module's recorded measurement is now stale"
    )


def test_d2_reason_phrase(tmp_path, tmproot, serve):
    """Channel: the peer-supplied **reason phrase**.  Instrument: leak injection."""
    fixture = serve(api_responder(reason=MARKERS["reason_phrase"], deny=False))
    a, b = _api_channel(
        tmp_path, tmproot, fixture.port,
        responder_marker_kwargs=None,
        engine_edits=_LEAK_REASON_PHRASE,
    )
    assert a.occurrences(MARKERS["reason_phrase"]), (
        f"phase (a) did not leak; the runner may never parse a reason phrase. "
        f"result={a.result}"
    )
    assert b.occurrences(MARKERS["reason_phrase"]) == []


def test_d2_redirect_location(tmp_path, tmproot, serve):
    """Channel: a peer-chosen **``Location``** on a ``3xx``.

    A redirect is refused rather than followed, so the clean run is DEGRADED —
    which is the point: the refusal path is an output channel too, and the
    ``Location`` may not appear on it.
    """
    location = f"https://evil.example.org/{MARKERS['redirect_location']}?q=1"
    fixture = serve(api_responder(location=location))
    a, b = _api_channel(
        tmp_path, tmproot, fixture.port,
        responder_marker_kwargs=None,
        engine_edits=_LEAK_REDIRECT_LOCATION,
        expect_clean_result="DEGRADED",
    )
    assert a.occurrences(MARKERS["redirect_location"]), (
        f"phase (a) did not leak; the runner may never parse a Location. "
        f"result={a.result}"
    )
    assert b.occurrences(MARKERS["redirect_location"]) == []


def test_d2_json_pointer_value_and_collection_member(tmp_path, tmproot, serve):
    """Channels: an **overexposed JSON property** and an **array member**.

    One run, two independently-planted markers, one shared instrument — so a
    single green cannot cover for one of the two never being reached.
    """
    fixture = serve(api_responder(
        overexpose=MARKERS["json_pointer_value"],
        tags=[MARKERS["collection_member"], "b"],
        deny=False,
    ))
    a, b = _api_channel(
        tmp_path, tmproot, fixture.port,
        responder_marker_kwargs=None,
        engine_edits=_LEAK_OBSERVED_VALUE,
    )
    for channel in ("json_pointer_value", "collection_member"):
        assert a.occurrences(MARKERS[channel]), (
            f"phase (a) did not leak for {channel}; the runner may never "
            f"observe it. result={a.result}"
        )
        assert b.occurrences(MARKERS[channel]) == [], channel


def test_d2_response_body(tmp_path, tmproot, serve):
    """Channel: an **undeclared body property** the policy never asked about."""
    fixture = serve(api_responder(
        overexpose=MARKERS["response_body"], deny=False,
    ))
    a, b = _api_channel(
        tmp_path, tmproot, fixture.port,
        responder_marker_kwargs=None,
        engine_edits=_LEAK_OBSERVED_VALUE,
    )
    assert a.occurrences(MARKERS["response_body"]), a.result
    assert b.occurrences(MARKERS["response_body"]) == []


def test_d2_credential(tmp_path, tmproot, serve):
    """Channel: a **credential value** read from the environment."""
    fixture = serve(api_responder(deny=True))
    a, b = _api_channel(
        tmp_path, tmproot, fixture.port,
        responder_marker_kwargs=None,
        facade_edits=_LEAK_CREDENTIAL,
        expect_clean_result="CLEAN",
    )
    for value in API_CREDS.values():
        assert a.occurrences(value), (
            f"phase (a) did not leak the credential; the runner may never read "
            f"it. result={a.result}"
        )
        assert b.occurrences(value) == []


def test_d2_policy_label(tmp_path, tmproot, serve):
    """Channel: a **policy label refused for excessive length**.

    The label is adopter-authored and may carry anything; the refusal names the
    rule, never the text.  The clean run is DEGRADED at the schema boundary,
    before any network act.
    """
    fixture = serve(api_responder(deny=True))
    long_label = MARKERS["policy_label"] + "x" * 300
    a, b = _api_channel(
        tmp_path, tmproot, fixture.port,
        responder_marker_kwargs=None,
        engine_edits=_LEAK_POLICY_LABEL,
        policy_kwargs={"role": long_label},
        expect_clean_result="DEGRADED",
    )
    assert a.occurrences(MARKERS["policy_label"]), (
        f"phase (a) did not leak; the label may never reach _clean_str. "
        f"result={a.result}"
    )
    assert b.occurrences(MARKERS["policy_label"]) == []


def test_d2_response_header_and_set_cookie(tmp_path, tmproot, serve, tmp_path_factory):
    """Channels: a **response header value** and a **``Set-Cookie``**.

    Driven through the hosting runner, which is the capability that examines
    headers and cookies; both markers are planted in one response.
    """
    certdir = tmp_path / "certs"
    certdir.mkdir()
    cert, key = make_cert(certdir, "hosting", common_name="localhost")
    fixture = serve(
        hosting_responder(
            cookies=(f"sid={MARKERS['set_cookie']}; Path=/",),
            extra=("X-Diagnostic", MARKERS["response_header"]),
        ),
        tls=tls_server_context(cert, key),
    )
    policy = hosting_policy(https_origin=fixture.origin("https", "localhost"))
    leaky = install(tmp_path, "hosting", policy, name="leaky",
                    facade_edits=_LEAK_HOSTING_HEADERS)
    clean = install(tmp_path, "hosting", policy, name="clean")
    a = run(leaky, "hosting", ["local"], tmproot=tmproot / "a", ca=cert)
    b = run(clean, "hosting", ["local"], tmproot=tmproot / "b", ca=cert)
    assert b.result == "FINDINGS", b.result
    for channel in ("response_header", "set_cookie"):
        assert a.occurrences(MARKERS[channel]), (
            f"phase (a) did not leak for {channel}. result={a.result}"
        )
        assert b.occurrences(MARKERS[channel]) == [], channel


def test_d2_the_refusal_chokepoint_closes_the_diagnostic_channel_class(
    tmp_path, tmproot, serve
):
    """The three chokepoint channels, closed as a class and shown non-vacuous.

    ``SecurityRefusal.__init__`` clamps ``reason`` to ``REASON_TOKENS``, so no
    handler can carry content out on a refusal however it is written.  Phase (a)
    deletes the clamp *and* has a handler pass a marker; phase (b) restores the
    clamp with the same handler edit still in place — which is what makes this a
    test of the clamp rather than of the handler.
    """
    fixture = serve(api_responder(deny=True))
    policy = api_policy(fixture.port)
    handler_edit = {"net.py": [(
        '        raise SecurityRefusal(E_POLICY_REFUSED, "non_loopback_target")',
        '        raise SecurityRefusal(E_POLICY_REFUSED, "non_loopback_target")',
    )]}
    del handler_edit  # the injection below is simpler and needs no net.py anchor

    # A handler that tries to smuggle the marker out as a reason token.
    smuggle = ('    if len(text) > max_len:\n        _refuse("label_too_long")',
               '    if len(text) > max_len:\n        _refuse(text)')
    long_label = MARKERS["policy_label"] + "y" * 300

    leaky = install(
        tmp_path, "api", api_policy(fixture.port, role=long_label), name="leaky",
        engine_edits={
            "policy.py": [smuggle],
            "report.py": [(
                '        if reason not in REASON_TOKENS:\n'
                '            reason = "unspecified"',
                '        if False:\n'
                '            reason = "unspecified"',
            )],
        },
    )
    clean = install(
        tmp_path, "api", api_policy(fixture.port, role=long_label), name="clean",
        engine_edits={"policy.py": [smuggle]},
    )
    a = run(leaky, "api", ["local"], tmproot=tmproot / "a", env_extra=API_CREDS)
    b = run(clean, "api", ["local"], tmproot=tmproot / "b", env_extra=API_CREDS)
    assert a.result == "DEGRADED", a.result
    assert b.result == "DEGRADED", b.result
    assert a.occurrences(MARKERS["policy_label"]), (
        "the clamp deletion did not leak -- this test proves nothing about the "
        f"clamp. result={a.result}"
    )
    assert b.occurrences(MARKERS["policy_label"]) == [], (
        "the clamp is in place and the marker still arrived"
    )
    assert b"policy_refused:unspecified" in b.proc.stdout
    del policy


def test_d2_no_engine_member_reads_a_certificate_field():
    """``certificate_subject``'s disposition, pinned at source level.

    The subject cannot leak because nothing reads it.  This assertion is
    falsifiable in the obvious way: add a ``getpeercert()`` call and it fails.
    """
    forbidden = ("getpeercert", "get_verified_chain", "get_unverified_chain",
                 "verify_message", "cert_store_stats")
    for member in sorted(ENGINE_SRC.glob("*.py")):
        text = member.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in text, f"{member.name} reads {token}"
    for facade in (API_FACADE_SRC, HOSTING_FACADE_SRC):
        text = facade.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in text, f"{facade.name} reads {token}"


def test_d2_no_handler_interpolates_an_exception_into_a_refusal():
    """``exception_text`` / ``timeout_diagnostic``, pinned at source level.

    Every ``SecurityRefusal`` raised in the engine takes a **literal** reason
    string.  An f-string or a ``str(exc)`` in that position is the defect this
    asserts against, and it would fail here before the clamp had to catch it.
    """
    import re

    # The hazard is *interpolation*, not indirection: `last_error or
    # "connection_failed"` is a local holding a literal and is fine, while
    # `str(exc)` or an f-string is the defect.  So the shapes that could carry
    # content are forbidden by name rather than literals being required -- which
    # is why the constructor clamp above remains the load-bearing control and
    # this is the earlier, cheaper signal.
    forbidden = ("str(", "repr(", 'f"', "f'", ".args", "exc", "%",
                 ".format(", "message")
    pattern = re.compile(r"SecurityRefusal\(\s*([A-Za-z_0-9.]+)\s*,\s*([^)]*)\)")
    checked = 0
    for member in sorted(ENGINE_SRC.glob("*.py")):
        text = member.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            reason = match.group(2).strip()
            if not reason:
                continue
            checked += 1
            for token in forbidden:
                assert token not in reason, (
                    f"{member.name}: refusal reason {reason!r} interpolates "
                    f"{token!r}"
                )
    # A pattern that matched nothing would pass vacuously.
    assert checked >= 20, checked


# ===========================================================================
# D-3 — the temporary directory contains only report.json
# ===========================================================================


@pytest.mark.parametrize("outcome", ["clean", "findings", "degraded",
                                     "incomplete"])
def test_d3_the_temporary_directory_holds_only_the_report(
    tmp_path, tmproot, serve, outcome
):
    """D-3: no raw-response artifact is created anywhere, at any exit path."""
    fixture = serve(api_responder(deny=True))
    if outcome == "clean":
        policy, argv = api_policy(fixture.port), ["local"]
        expected = {"report.json"}
    elif outcome == "findings":
        policy, argv = api_policy(fixture.port), ["local"]
        expected = {"report.json"}
    elif outcome == "incomplete":
        policy, argv = None, ["local"]
        expected = set()
    else:
        policy = api_policy(fixture.port, role="z" * 400)
        argv = ["local"]
        expected = set()
    if outcome == "findings":
        fixture2 = serve(api_responder(deny=False,
                                       overexpose="acquisition-pending"))
        policy = api_policy(fixture2.port)
    root = install(tmp_path, "api", policy)
    result = run(root, "api", argv, tmproot=tmproot, env_extra=API_CREDS)
    names = {p.name for p in result.temp_files()}
    assert names == expected, (result.result, sorted(names))
    # Nothing but the report directory, and nothing beside the report in it.
    for path in result.temp_files():
        assert path.parent.name.startswith("cairn-security-"), path
        assert path.stat().st_mode & 0o777 == 0o600, oct(path.stat().st_mode)


# ===========================================================================
# D-4 — bucket indistinguishability
# ===========================================================================


def test_d4_two_values_in_one_bucket_produce_identical_findings(
    tmp_path, tmproot, serve
):
    """D-4: 3 bytes and 31 bytes are both ``short`` and are indistinguishable.

    The two findings are compared **byte for byte** with the fingerprint removed
    (the fingerprint is keyed per run and is *meant* to differ), so what is
    asserted is that nothing else varies with the value's length.
    """
    def _finding_for(value: str, tag: str) -> dict:
        fixture = serve(api_responder(overexpose=value, deny=False))
        root = install(tmp_path, "api", api_policy(fixture.port), name=tag)
        result = run(root, "api", ["local"], tmproot=tmproot / tag,
                     env_extra=API_CREDS)
        assert result.result == "FINDINGS", result.result
        findings = [
            f for f in result.report()["findings"]
            if f["check_id"] == "overexposed-property"
        ]
        assert len(findings) == 1, result.report()["findings"]
        stripped = dict(findings[0])
        stripped.pop("observation_fingerprint", None)
        return stripped

    short_three = _finding_for("abc", "three")
    short_thirtyone = _finding_for("a" * 31, "thirtyone")
    assert short_three["observed_magnitude"] == "short"
    assert json.dumps(short_three, sort_keys=True) == json.dumps(
        short_thirtyone, sort_keys=True
    ), (short_three, short_thirtyone)


def test_d4_emitting_the_exact_length_breaks_the_identity(
    tmp_path, tmproot, serve
):
    """D-4's deletion mutant: emit the exact length; identity must break."""
    def _finding_for(value: str, tag: str) -> dict:
        fixture = serve(api_responder(overexpose=value, deny=False))
        root = install(
            tmp_path, "api", api_policy(fixture.port), name=tag,
            engine_edits={"report.py": [(
                '        finding["observed_magnitude"] = value_magnitude(observed_value)',
                '        finding["observed_magnitude"] = str(len(str(observed_value)))',
            )]},
        )
        result = run(root, "api", ["local"], tmproot=tmproot / tag,
                     env_extra=API_CREDS)
        assert result.result == "FINDINGS", result.result
        findings = [
            f for f in result.report()["findings"]
            if f["check_id"] == "overexposed-property"
        ]
        stripped = dict(findings[0])
        stripped.pop("observation_fingerprint", None)
        return stripped

    assert _finding_for("abc", "m3") != _finding_for("a" * 31, "m31")


# ===========================================================================
# D-5 — exact cardinality is closed as a class, on the parsed schema
# ===========================================================================


def _integers_in(obj, path="") -> "list[str]":
    found: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            found += _integers_in(value, f"{path}/{key}")
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            found += _integers_in(value, f"{path}/{index}")
    elif isinstance(obj, bool):
        pass
    elif isinstance(obj, int):
        found.append(f"{path}={obj}")
    return found


def test_d5_a_parsed_finding_carries_no_integer_at_all(tmp_path, tmproot, serve):
    """D-5: parsed, not text-searched.

    A text search for a decimal collides with legitimate statuses and stable
    ids, so the assertion is over the **parsed** structure: no byte length, no
    character length, no member count, no index count, no exact value-derived
    cardinality of any kind — because there is no integer at all.
    """
    fixture = serve(api_responder(
        overexpose="acquisition pending",
        tags=["one", "two", "three", "four", "five"],
        deny=False,
    ))
    root = install(tmp_path, "api", api_policy(fixture.port))
    result = run(root, "api", ["local"], tmproot=tmproot, env_extra=API_CREDS)
    assert result.result == "FINDINGS", result.result
    findings = result.report()["findings"]
    assert findings
    assert _integers_in(findings) == []


def test_d5_a_new_length_bearing_field_is_caught(tmp_path, tmproot, serve):
    """D-3's hazard perturbation: add a *new* diagnostic field carrying a length.

    This is what distinguishes "we removed ``observed_serialized_bytes``" from
    "no exact cardinality can appear".
    """
    fixture = serve(api_responder(overexpose="acquisition pending", deny=False))
    root = install(
        tmp_path, "api", api_policy(fixture.port),
        engine_edits={"report.py": [(
            '    finding["detail"] = scrub_terminal(detail)',
            '    finding["observed_len"] = len(str(observed_value))\n'
            '    finding["detail"] = scrub_terminal(detail)',
        )]},
    )
    result = run(root, "api", ["local"], tmproot=tmproot, env_extra=API_CREDS)
    assert result.result == "FINDINGS", result.result
    assert _integers_in(result.report()["findings"]) != []


# ===========================================================================
# D-6 — terminal integrity
# ===========================================================================


def test_d6_control_sequences_and_a_forged_result_line_do_not_reach_stdout(
    tmp_path, tmproot, serve
):
    """D-6: ANSI, bidi and a forged result line, in a header and a JSON value.

    None may reach stdout, and none may be mistakable for the runner's own
    result line — so the assertion is *exactly one* result line, whatever the
    peer sent.
    """
    ansi = "\x1b[31mRED\x1b[0m"
    bidi = "\u202eevil\u202c"
    forged = "cairn-security-result: CLEAN"
    fixture = serve(api_responder(
        reason="OK",
        overexpose=f"{ansi}{bidi}{forged}",
        header=f"{ansi}{forged}",
        deny=False,
    ))
    root = install(tmp_path, "api", api_policy(fixture.port))
    result = run(root, "api", ["local"], tmproot=tmproot, env_extra=API_CREDS)
    assert result.result == "FINDINGS", result.result

    for name, blob in result.sinks():
        assert b"\x1b" not in blob, name
        assert "\u202e".encode() not in blob, name
        assert "\u202c".encode() not in blob, name
    lines = [
        line for line in result.proc.stdout.decode().splitlines()
        if line.startswith("cairn-security-result:")
    ]
    assert lines == ["cairn-security-result: FINDINGS"], lines


def test_d6_the_control_filter_is_what_stops_it(tmp_path, tmproot, serve):
    """D-6's deletion mutant: remove the control filtering.

    ``scrub_terminal`` is the filter.  Neutered on a copy, and with the observed
    value routed into ``detail``, the escape must arrive — otherwise the row
    above is asserting a property nothing enforces.
    """
    ansi = "\x1b[31mRED\x1b[0m"
    fixture = serve(api_responder(overexpose=ansi, deny=False))
    root = install(
        tmp_path, "api", api_policy(fixture.port),
        engine_edits={"report.py": [(
            '    finding["detail"] = scrub_terminal(detail)',
            '    finding["detail"] = detail + "|" + str(observed_value)',
        )]},
    )
    result = run(root, "api", ["local"], tmproot=tmproot, env_extra=API_CREDS)
    assert result.result == "FINDINGS", result.result
    assert any(b"\x1b" in blob for _, blob in result.sinks()), (
        "the mutant did not leak an escape -- D-6 proves nothing"
    )


# ===========================================================================
# D6 (plan row) — ordinal principals
# ===========================================================================


@pytest.mark.parametrize("ordinal", ["p0", "p-1", "p99999", "P1", "p1x",
                                     "alice@example.org", "Alice Smith",
                                     "acct-4471"])
def test_d6row_a_non_ordinal_principal_is_refused(tmp_path, tmproot, serve,
                                                  ordinal):
    """Only ``p1``, ``p2``, … are principals: no name, no email, no account id.

    This is why no finding can name a person — there is no name in the system to
    name.

    **The case reference is renamed too, deliberately.**  An earlier version
    renamed only the principal, and measurement showed the refusal then came from
    the *unknown-principal-reference* guard rather than the ordinal shape — so a
    mutant that relaxed ``_ORDINAL_RE`` left every row green.  Renaming both
    keeps the policy internally consistent, which makes the ordinal shape the
    only thing left that can refuse.

    **Measured: relaxing ``_ORDINAL_RE`` to ``^.*$`` reddens exactly one row,
    ``P1``.**  The other seven are still refused, one guard downstream: the
    credential variable name is *derived* from the id, so ``p0`` / ``p-1`` /
    ``p99999`` / ``p1x`` / an email / a name / an account id all derive a name
    that is not set and refuse with ``credential_absent``.  Only ``P1`` derives
    ``CAIRN_API_P1_CREDENTIAL`` — a name that *is* set — so only ``P1`` isolates
    the ordinal shape.  Recorded rather than pruned: every row still asserts the
    two things this test is for (the run refuses, and the label reaches no
    sink), and the narrowness of the mutant is a property of the design, not of
    the test.
    """
    fixture = serve(api_responder(deny=True))
    policy = api_policy(fixture.port)
    policy["local"]["principals"][0]["id"] = ordinal
    policy["local"]["operations"][0]["cases"][0]["principal"] = ordinal
    root = install(tmp_path, "api", policy)
    result = run(root, "api", ["local"], tmproot=tmproot, env_extra=API_CREDS)
    assert result.returncode == 20, result.result
    assert result.result == "DEGRADED"
    assert result.occurrences(ordinal) == [], (
        f"the refused principal label {ordinal!r} reached an output channel"
    )


def test_d6row_a_duplicate_ordinal_is_refused(tmp_path, tmproot, serve):
    fixture = serve(api_responder(deny=True))
    policy = api_policy(fixture.port)
    policy["local"]["principals"][1]["id"] = "p1"
    root = install(tmp_path, "api", policy)
    result = run(root, "api", ["local"], tmproot=tmproot, env_extra=API_CREDS)
    assert result.returncode == 20, result.result


def test_d6row_the_credential_name_is_derived_and_a_role_never_appears(
    tmp_path, tmproot, serve
):
    """The derived name is exactly ``CAIRN_API_P<N>_CREDENTIAL``.

    Asserted by *withholding* the derived name and supplying a plausible
    alternative: the run must fail for want of a credential, which proves the
    runner looks up the derived name and nothing else.  The role token is
    accepted by policy and appears in no finding.
    """
    fixture = serve(api_responder(deny=True))
    role = "quartermaster"
    policy = api_policy(fixture.port, role=role)
    root = install(tmp_path, "api", policy)

    wrong = {
        "CAIRN_API_P1_TOKEN": "x",
        "API_P1_CREDENTIAL": "x",
        "CAIRN_API_p1_CREDENTIAL": "x",
    }
    absent = run(root, "api", ["local"], tmproot=tmproot / "absent",
                 env_extra=wrong)
    assert absent.returncode == 20, absent.result
    assert b"credential_absent" in absent.proc.stdout

    present = run(root, "api", ["local"], tmproot=tmproot / "present",
                  env_extra=API_CREDS)
    assert present.result == "CLEAN", present.result
    assert present.occurrences(role) == [], "the role token reached an output"


# ===========================================================================
# D7 (plan row) — the ephemeral keyed fingerprint
# ===========================================================================


def _fingerprints(tmp_path, tmproot, serve, tag: str, value: str) -> "list[str]":
    # Two *distinct* declared-absent properties carrying the **same** value, so
    # the two findings are genuinely equal observations.  An earlier version used
    # an overexposed scalar plus an array and measured two different
    # fingerprints -- correctly, because a list and a string are not the same
    # observation.  Recorded here so the row is not "fixed" back to that shape.
    fixture = serve(api_responder(overexpose=value, free_text=value,
                                  deny=False))
    root = install(tmp_path, "api", api_policy(fixture.port), name=tag)
    result = run(root, "api", ["local"], tmproot=tmproot / tag,
                 env_extra=API_CREDS)
    assert result.result == "FINDINGS", result.result
    return [
        f["observation_fingerprint"] for f in result.report()["findings"]
        if "observation_fingerprint" in f
    ]


def test_d7_equal_observations_match_within_a_run_and_differ_across_runs(
    tmp_path, tmproot, serve
):
    """D-5 (plan): the fingerprint correlates, and is not an offline oracle."""
    value = "the-same-observed-value"
    first = _fingerprints(tmp_path, tmproot, serve, "run1", value)
    second = _fingerprints(tmp_path, tmproot, serve, "run2", value)
    assert first, "no fingerprint was emitted -- this row would be vacuous"
    assert len(set(first)) == 1, first
    assert set(first) != set(second), (
        "the same value fingerprinted identically across two runs: the key is "
        "not per-run and a pasted report is a dictionary oracle"
    )


def test_d7_a_constant_key_makes_the_cross_run_property_fail(
    tmp_path, tmproot, serve
):
    """D-5's deletion mutant: derive the key from a constant."""
    value = "the-same-observed-value"

    def _run(tag: str) -> "list[str]":
        fixture = serve(api_responder(overexpose=value, deny=False))
        root = install(
            tmp_path, "api", api_policy(fixture.port), name=tag,
            engine_edits={"report.py": [(
                "            key = secrets.token_bytes(32)",
                '            key = b"constant-key-of-exactly-32-bytes"',
            )]},
        )
        result = run(root, "api", ["local"], tmproot=tmproot / tag,
                     env_extra=API_CREDS)
        assert result.result == "FINDINGS", result.result
        return [
            f["observation_fingerprint"] for f in result.report()["findings"]
            if "observation_fingerprint" in f
        ]

    assert set(_run("c1")) == set(_run("c2")), (
        "the constant-key mutant did not make the cross-run property fail, so "
        "the property above is not testing the key"
    )


def test_d7_the_key_appears_in_no_sink(tmp_path, tmproot, serve):
    """The key is never printed, persisted, or written to a temporary file.

    Asserted by pinning the key to a known value on a copy and sweeping for it —
    the only way to look for a secret that is otherwise unobservable.
    """
    known = "constant-key-of-exactly-32-bytes"
    fixture = serve(api_responder(overexpose="v", deny=False))
    root = install(
        tmp_path, "api", api_policy(fixture.port),
        engine_edits={"report.py": [(
            "            key = secrets.token_bytes(32)",
            f'            key = b"{known}"',
        )]},
    )
    result = run(root, "api", ["local"], tmproot=tmproot, env_extra=API_CREDS)
    assert result.result == "FINDINGS", result.result
    assert result.occurrences(known) == []


def test_d7_absent_randomness_is_degraded_before_the_first_request(
    tmp_path, tmproot, serve
):
    """A failure to obtain randomness is DEGRADED, and no request is made."""
    fixture = serve(api_responder(deny=True))
    root = install(
        tmp_path, "api", api_policy(fixture.port),
        engine_edits={"report.py": [(
            "            key = secrets.token_bytes(32)",
            "            raise OSError('no randomness')",
        )]},
    )
    result = run(root, "api", ["local"], tmproot=tmproot, env_extra=API_CREDS)
    assert result.returncode == 20, result.result
    assert result.result == "DEGRADED"
    assert b"randomness_unavailable" in result.proc.stdout, result.proc.stdout
    assert fixture.accepted == 0, (
        "a connection was made before the fingerprint key existed"
    )


# ===========================================================================
# The activation dispatcher's own aggregate report -- a NEW swept sink
# ===========================================================================
# The child `details` document was a JSON object until the fix this section
# follows: `_security_net/report.py`'s `child_document(..., details: dict,
# ...)` and both facades' `_emit` always built it as `{"capability",
# "findings", "notes", ...}`, while `run_security_verification.py`'s own
# `_evaluate_capability` requires `isinstance(details, str)` and DEGRADES
# otherwise -- so `_safe_render(details)` was NEVER reached by a real leg,
# and the dispatcher's own aggregate report was not a sink anything could
# leak into. With `details` now a single string built by this engine's
# `render_details`, it reaches the dispatcher's aggregate report for the
# first time, through `_safe_render` -- which the dispatcher's own
# `_CONTROL_KEEP` comment names as "the ONLY channel a child's text ever
# reaches the report through". That makes the dispatcher's own stdout a NEW
# sink this file's Chunk D scope never swept (nothing above this section
# drives the dispatcher at all).
#
# **Why the reachable leg is the unfilled-policy-stub INCOMPLETE result,
# never a live FINDINGS run.** Measured directly against the dispatcher's
# own source:
#   * `_CHILD_ENV_ALLOWLIST` (T7, `run_security_verification.py`) is a
#     CLOSED set -- `PATH`, `HOME`, `LANG`, `TMPDIR`/`TEMP`/`TMP`, a handful
#     of Windows-minimum names, and an `LC_` prefix. It does not include
#     `CAIRN_API_P1_CREDENTIAL` / `CAIRN_API_P2_CREDENTIAL` or
#     `SSL_CERT_FILE`, and neither is a name a future entry could add
#     without its own Security Review (the registry section above the
#     allowlist says so explicitly).
#   * api-access-security's `local` mode reads both credentials from
#     `os.environ` BEFORE any network call (`_read_credentials`); through
#     the dispatcher those names are always absent, so the child always
#     refuses `credential_absent` before touching the fixture.
#   * web-hosting-security's `local` mode always performs a mandatory HTTPS
#     connection to `https_origin` using `ssl.create_default_context()`
#     (`_security_net/net.py`), which resolves trust from the platform
#     default store honoring `SSL_CERT_FILE`/`SSL_CERT_DIR` -- both
#     stripped by the same allowlist. A self-signed test certificate is
#     therefore never trusted, and the TLS handshake refuses before any
#     header or cookie is ever read.
# Both are the SAME reviewed property working as designed (the child a
# malicious dispatcher spawns cannot be handed a real credential or a real
# trust anchor), not a gap in this test's fixture. It forecloses a live,
# network-observed marker reaching the dispatcher for EITHER capability --
# D1/D2's own scenario included -- so this section instead drives the one
# leg that IS reachable through the real subprocess chain with no network
# and no credential at all: the unfilled policy stub's INCOMPLETE result.
# `render_details` runs on that leg exactly as it would on any other, so it
# is sufficient to exercise the property actually under test here: whether
# `render_details`'s OUTPUT survives to the dispatcher's aggregate report
# unscrubbed if compromised, not whether a peer response can be observed
# through the dispatcher at all.

DISPATCHER_SRC = (
    REPO_ROOT / "templates" / "modules" / "default-on"
    / "run_security_verification.py"
)

#: Planted at the RENDERING layer (report.py's `render_details`), never by a
#: peer -- distinct from every entry in `MARKERS` so a hit unambiguously
#: names this section's own mutation, not a coincidence with a fixture
#: channel.
_RENDER_LEAK_MARKER = "MkRDL8v2Tn6WgXq"

#: The single-line mutation the liveness test applies to a COPY of the
#: shared engine: drop nothing, just append an unscrubbed marker to
#: `render_details`'s return value -- "the rendering ... emits a raw value",
#: the exact hazard this sink coverage exists to catch.
_LEAK_RENDER_DETAILS = {
    "report.py": [(
        '    return scrub_terminal("\\n".join(lines))',
        '    return scrub_terminal("\\n".join(lines)) + "'
        + _RENDER_LEAK_MARKER + '"',
    )],
}


def _sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def install_dispatcher(root: Path, *, capability_dst: str, policy_dst: str,
                        modules: "list[str]") -> None:
    """Lay the REAL dispatcher and a matching, digest-consistent lockfile
    over an already-``install()``-ed capability root, so a subprocess run
    of ``root/scripts/run_security_verification.py local`` exercises the
    real activation seam end to end.

    Hand-assembled to the dispatcher's own documented lockfile contract (a
    JSON body -- ``_load_lockfile`` strips ``#``-prefixed lines and then
    calls ``json.loads`` -- shaped ``{"modules": [...], "files": [...]}``)
    rather than run through the scaffold engine, for the same reason
    ``install()`` above is: a facade OR dispatcher defect must not be
    maskable by an installer defect, or vice versa. The runner record's
    hash MUST be exact (``runner_binding_mode`` is ``immutable_digest``);
    the policy record's hash is unchecked (``policy_binding_mode`` is
    ``living_state`` for both admitted capabilities) but included anyway
    for a lockfile a human reader would not find suspicious.
    """
    scripts = root / "scripts"
    shutil.copy(DISPATCHER_SRC, scripts / "run_security_verification.py")
    lock = {
        "modules": modules,
        "files": [
            {"dst": capability_dst,
             "hash": _sha256_file(root / capability_dst)},
            {"dst": policy_dst,
             "hash": _sha256_file(root / policy_dst), "living_state": True},
        ],
    }
    lockdir = root / "dev" / ".cairn"
    lockdir.mkdir(parents=True, exist_ok=True)
    (lockdir / "cairn-lock.yml").write_text(
        json.dumps(lock, indent=2), encoding="utf-8")


def run_dispatcher(root: Path, *, tmproot: Path) -> subprocess.CompletedProcess:
    """Run the installed dispatcher as a real subprocess, ``TMPDIR`` pointed
    at a test-owned root -- forwarded to the child by the dispatcher's own
    closed allowlist, so the child's report directory lands inside it too."""
    tmproot.mkdir(parents=True, exist_ok=True)
    env = {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONDONTWRITEBYTECODE": "1",
        "HOME": os.environ.get("HOME", ""),
        "TMPDIR": str(tmproot),
    }
    return subprocess.run(
        [sys.executable, str(root / "scripts" / "run_security_verification.py"),
         "local"],
        capture_output=True, env=env, timeout=120,
    )


def _dispatcher_sinks(proc, tmproot: Path) -> "list[tuple[str, bytes]]":
    """Every sink the DISPATCHER's own run can write: its stdout, its
    stderr, and every file under its (and its child's) TMPDIR."""
    out: "list[tuple[str, bytes]]" = [
        ("dispatcher:stdout", proc.stdout),
        ("dispatcher:stderr", proc.stderr),
    ]
    if tmproot.exists():
        for path in sorted(p for p in tmproot.rglob("*") if p.is_file()):
            out.append((f"dispatcher:tmp:{path.relative_to(tmproot)}",
                        path.read_bytes()))
    return out


def _dispatcher_occurrences(proc, tmproot: Path, needle: str) -> "list[str]":
    raw = needle.encode("utf-8")
    return [name for name, blob in _dispatcher_sinks(proc, tmproot) if raw in blob]


def _dispatcher_aggregate(proc: subprocess.CompletedProcess) -> dict:
    lines = [ln for ln in proc.stdout.decode("utf-8", "replace").splitlines()
             if ln.startswith("{")]
    assert lines, proc.stdout + proc.stderr
    return json.loads(lines[-1])


class TestTheDispatcherAggregateReportIsANewSweptSink:
    """The dispatcher's OWN aggregate report, driven end to end through a
    real subprocess chain -- this section's own hand-assembled dispatcher
    install spawning the real, installed web-hosting-security facade as
    ITS child, never a synthetic ``RegistryEntry`` and never the facade
    invoked in place of the dispatcher. See this module's own docstring
    addition (top of file) and this section's header comment for why the
    unfilled-policy-stub INCOMPLETE leg is the one exercised here rather
    than a live, network-observed FINDINGS run."""

    def test_the_pristine_renderer_never_leaks_into_the_dispatcher_report(
        self, tmp_path, tmproot
    ):
        """Phase (b), the baseline: the shipped, unmutated
        ``render_details`` produces no marker on this leg (there being none
        planted anywhere on this leg to begin with), swept over the
        dispatcher's own stdout/stderr/tmp sinks -- established here as
        what the next test's mutation is compared against, and reusing the
        SAME ``MARKERS`` set D1/D2 sweep for, so this really is "the
        existing planted-marker assertions, re-checked against this new
        sink"."""
        root = install(tmp_path, "hosting", None, name="dispatcher-clean")
        install_dispatcher(
            root, capability_dst=f"scripts/{HOSTING_FACADE_SRC.name}",
            policy_dst=HOSTING_POLICY_REL,
            modules=["web-hosting-security"],
        )
        proc = run_dispatcher(root, tmproot=tmproot)
        assert proc.returncode == 5, proc.stdout + proc.stderr
        agg = _dispatcher_aggregate(proc)
        assert agg["aggregate"] == "INCOMPLETE"
        [leg] = agg["legs"]
        assert leg["module_id"] == "web-hosting-security"
        assert leg["aggregate_label"] == "INCOMPLETE"
        assert leg["child_launched"] is True
        assert "unconfigured" in leg["detail"]

        for name, marker in MARKERS.items():
            assert _dispatcher_occurrences(proc, tmproot, marker) == [], name
        assert _dispatcher_occurrences(proc, tmproot, _RENDER_LEAK_MARKER) == []

    def test_a_leaking_renderer_is_caught_at_the_dispatcher_report(
        self, tmp_path, tmproot
    ):
        """Phase (a), the liveness proof required alongside phase (b): the
        SAME reachable leg, but ``_security_net/report.py``'s
        ``render_details`` is mutated -- on a COPY, never the repository
        tree -- to append a marker to its returned string WITHOUT
        scrubbing it. The child's stdout stays valid JSON (the marker is
        embedded as an ordinary string value via ``json.dumps``), so the
        dispatcher parses it, ``_safe_render``s it (a no-op on plain
        ASCII), and prints it in its OWN aggregate report. A sweep that
        stayed green here would be exactly the vacuous-assertion trap this
        repository has already caught twice today."""
        root = install(
            tmp_path, "hosting", None, name="dispatcher-leaky",
            engine_edits=_LEAK_RENDER_DETAILS,
        )
        install_dispatcher(
            root, capability_dst=f"scripts/{HOSTING_FACADE_SRC.name}",
            policy_dst=HOSTING_POLICY_REL,
            modules=["web-hosting-security"],
        )
        proc = run_dispatcher(root, tmproot=tmproot)
        assert proc.returncode == 5, proc.stdout + proc.stderr
        agg = _dispatcher_aggregate(proc)
        [leg] = agg["legs"]
        assert leg["aggregate_label"] == "INCOMPLETE"
        assert _RENDER_LEAK_MARKER in leg["detail"], (
            "the mutant did not leak into the dispatcher's own aggregate "
            "report -- this sink assertion proves nothing"
        )
        hits = _dispatcher_occurrences(proc, tmproot, _RENDER_LEAK_MARKER)
        assert "dispatcher:stdout" in hits, (
            "the marker did not reach the dispatcher's OWN stdout sink -- "
            "the property this class exists to catch"
        )
