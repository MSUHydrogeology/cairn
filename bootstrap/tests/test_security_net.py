# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors
"""The adversarial transport suite for the shared ``_security_net`` engine.

This is the AW4 gate from ``dev/plans/api-web-security-modules.md``: the
evidence that the two capability runners sit on a client whose *connected peer*
is validated, whose redirects are never followed, whose reads are capped, and
whose TLS cannot be weakened.

**No transport call is mocked anywhere in this file.**  Every request crosses a
real socket to a real listening server in a real thread, and every assertion
about what arrived is read from *that server's* record rather than from the
client's own bookkeeping.  Two substitutions are used, both named in the plan's
*Channel note* as oracles rather than as stand-ins for transport:

* a **stub resolver** (``net._RESOLVER``), which decides what the client
  believes about an address; and
* a **socket layer that connects somewhere other than where it was asked**
  (``net._SOCKET_FACTORY``), which is how a DNS answer changing between
  validation and connection is reproduced deterministically.

The distinction matters and the plan insists on it: those two establish the
*decision*, and ``test_live_transport_*`` establishes that the implementation
obeyed it with nothing in the path substituted at all.
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import socket
import socketserver
import ssl
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE_SRC = REPO_ROOT / "templates" / "modules" / "team-gated" / "_security_net"

_ENGINE_SEQ = [0]


# ---------------------------------------------------------------------------
# Loading the engine, pristine or perturbed
# ---------------------------------------------------------------------------


def _import_engine_package(directory: Path, name: str):
    """Import ``directory`` as a package called ``name``.

    A fresh name per load is what makes a perturbed copy and the pristine
    original coexist in one interpreter, which is what a deletion mutant needs.
    """
    init = directory / "__init__.py"
    spec = importlib.util.spec_from_file_location(
        name, init, submodule_search_locations=[str(directory)]
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _drop_engine(name: str) -> None:
    for key in [k for k in sys.modules if k == name or k.startswith(name + ".")]:
        del sys.modules[key]


def load_engine(
    tmp_path: Path,
    *,
    edits: "dict[str, list[tuple[str, str]]] | None" = None,
    remove: "tuple[str, ...]" = (),
):
    """Copy the engine into ``tmp_path`` and import it under a unique name.

    ``edits`` maps a member filename to ``(old, new)`` literal replacements —
    the perturbation mechanism for every deletion mutant below.  Each
    replacement must match exactly once, so a mutant that silently stopped
    applying (because the source moved) fails loudly instead of passing as a
    green test.
    """
    _ENGINE_SEQ[0] += 1
    name = f"_security_net_u{_ENGINE_SEQ[0]}"
    target = tmp_path / name
    shutil.copytree(ENGINE_SRC, target)
    for member in remove:
        (target / member).unlink()
    for member, replacements in (edits or {}).items():
        path = target / member
        text = path.read_text(encoding="utf-8")
        for old, new in replacements:
            assert text.count(old) == 1, (
                f"perturbation anchor is not unique in {member}: {old!r} "
                f"occurs {text.count(old)} times"
            )
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")
    package = _import_engine_package(target, name)
    return package, name


@pytest.fixture()
def engine(tmp_path):
    """The pristine engine, loaded from a throwaway copy."""
    package, name = load_engine(tmp_path)
    try:
        yield package
    finally:
        _drop_engine(name)


@pytest.fixture()
def perturbed(tmp_path):
    """Factory for a perturbed engine copy, cleaned up at teardown."""
    loaded: list[str] = []

    def _make(**kwargs):
        package, name = load_engine(tmp_path, **kwargs)
        loaded.append(name)
        return package

    try:
        yield _make
    finally:
        for name in loaded:
            _drop_engine(name)


def submodule(package, leaf: str):
    return importlib.import_module(f"{package.__name__}.{leaf}")


# ---------------------------------------------------------------------------
# The recording server
# ---------------------------------------------------------------------------


class Recorded:
    """What one connection to the fixture actually delivered."""

    def __init__(self, peer, raw: bytes) -> None:
        self.peer = peer
        self.raw = raw
        head, _, body = raw.partition(b"\r\n\r\n")
        lines = head.decode("iso-8859-1").split("\r\n") if head else []
        self.request_line = lines[0] if lines else ""
        self.method = self.request_line.split(" ")[0] if self.request_line else ""
        parts = self.request_line.split(" ")
        self.target = parts[1] if len(parts) > 1 else ""
        self.headers: list[tuple[str, str]] = []
        for line in lines[1:]:
            if ":" in line:
                key, _, value = line.partition(":")
                self.headers.append((key.strip(), value.strip()))
        self.body = body

    def header(self, name: str) -> "str | None":
        for key, value in self.headers:
            if key.lower() == name.lower():
                return value
        return None


class _Handler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        server = self.server
        raw = b""
        sock = self.request
        sock.settimeout(2.0)
        try:
            while b"\r\n\r\n" not in raw and len(raw) < 65536:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                raw += chunk
            if b"\r\n\r\n" in raw:
                head, _, rest = raw.partition(b"\r\n\r\n")
                length = 0
                for line in head.decode("iso-8859-1").split("\r\n")[1:]:
                    if line.lower().startswith("content-length:"):
                        try:
                            length = int(line.split(":", 1)[1].strip())
                        except ValueError:
                            length = 0
                while len(rest) < length:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    rest += chunk
                raw = head + b"\r\n\r\n" + rest
        except OSError:
            pass
        record = Recorded(self.client_address, raw)
        with server.lock:
            server.records.append(record)
        try:
            payload = server.responder(record)
        except Exception:  # pragma: no cover - a broken responder is a test bug
            payload = b"HTTP/1.1 500 x\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
        if isinstance(payload, tuple):
            payload, delay = payload
        else:
            delay = 0.0
        if delay:
            time.sleep(delay)
        try:
            if payload:
                sock.sendall(payload)
        except OSError:
            pass


class _Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address, family, responder, tls) -> None:
        self.address_family = family
        self.responder = responder
        self.records: list[Recorded] = []
        self.lock = threading.Lock()
        self.accepted = 0
        self._tls = tls
        super().__init__(address, _Handler)

    def get_request(self):
        sock, addr = super().get_request()
        with self.lock:
            self.accepted += 1
        if self._tls is not None:
            try:
                return self._tls.wrap_socket(sock, server_side=True), addr
            except OSError:
                try:
                    sock.close()
                finally:
                    raise
        return sock, addr

    def handle_error(self, request, client_address):  # pragma: no cover
        # A handshake the client refuses is an expected outcome here, not a
        # traceback worth printing into the test log.
        pass


class Fixture:
    """A started recording server, with the client's view of its origin."""

    def __init__(self, responder, *, host="127.0.0.1", tls=None) -> None:
        family = socket.AF_INET6 if ":" in host else socket.AF_INET
        self._server = _Server((host, 0), family, responder, tls)
        self.host = host
        self.port = self._server.server_address[1]
        self._thread = threading.Thread(
            target=self._server.serve_forever, daemon=True
        )
        self._thread.start()

    @property
    def records(self):
        with self._server.lock:
            return list(self._server.records)

    @property
    def accepted(self) -> int:
        with self._server.lock:
            return self._server.accepted

    @property
    def sockaddr(self):
        return self._server.server_address

    def origin(self, scheme: str = "http", host: "str | None" = None) -> str:
        shown = host if host is not None else self.host
        authority = f"[{shown}]" if ":" in shown else shown
        return f"{scheme}://{authority}:{self.port}"

    def close(self) -> None:
        self._server.shutdown()
        self._server.server_close()


@pytest.fixture()
def serve():
    """Start recording servers and shut every one of them down at teardown."""
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


def ok_response(body: bytes = b"ok", *, status: int = 200, reason: str = "OK",
                extra: "tuple[tuple[str, str], ...]" = ()) -> bytes:
    lines = [f"HTTP/1.1 {status} {reason}"]
    for name, value in extra:
        lines.append(f"{name}: {value}")
    lines.append(f"Content-Length: {len(body)}")
    lines.append("Connection: close")
    return ("\r\n".join(lines) + "\r\n\r\n").encode("iso-8859-1") + body


def responder_ok(body: bytes = b"ok", **kwargs):
    def _responder(_record):
        return ok_response(body, **kwargs)

    return _responder


def responder_redirect(location: str, *, status: int = 302):
    def _responder(_record):
        return (
            f"HTTP/1.1 {status} Found\r\nLocation: {location}\r\n"
            f"Content-Length: 0\r\nConnection: close\r\n\r\n"
        ).encode("iso-8859-1")

    return _responder


# ---------------------------------------------------------------------------
# The substituted socket layer
# ---------------------------------------------------------------------------


class ConnectsElsewhere:
    """A socket that connects to ``destination``, whatever it is asked for.

    This is how "the DNS answer changed between validation and connection" is
    reproduced without a second resolution and without depending on a live
    rebinding lab.  Everything except ``connect`` (and, where a test says so,
    ``getpeername``) delegates to a real socket, so the bytes on the wire and
    the peer the *fixture* records are real.
    """

    def __init__(self, family, type_, destination, reported_peer=None) -> None:
        dest_family = socket.AF_INET6 if ":" in str(destination[0]) else socket.AF_INET
        self._real = socket.socket(dest_family, type_)
        self._destination = destination
        self._reported_peer = reported_peer
        self.connect_requests: list = []

    def connect(self, address):
        self.connect_requests.append(address)
        self._real.connect(self._destination)

    def getpeername(self):
        if self._reported_peer is not None:
            return self._reported_peer
        return self._real.getpeername()

    def __getattr__(self, name):
        return getattr(self._real, name)


def wait_for(predicate, *, timeout: float = 3.0) -> bool:
    """Poll ``predicate`` until true or ``timeout`` elapses.

    The fixture runs in its own threads, so "the server has recorded the
    connection" is an eventual fact.  Polling for it keeps the assertion about
    *what arrived* rather than about scheduler timing -- an assertion that
    raced would be a flaky gate, and a flaky gate gets deleted.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.01)
    return predicate()


def assert_connected_but_sent_nothing(fixture) -> None:
    """The connection happened and carried zero application bytes.

    Stronger than "the fixture recorded nothing", which is also true when the
    client never connected at all -- and that difference is the whole point of
    a peer-verification test.
    """
    assert wait_for(lambda: len(fixture.records) >= 1), (
        "the fixture never saw the connection, so this test proves nothing "
        "about what was sent over it"
    )
    assert [record.raw for record in fixture.records] == [b""]


def resolver_returning(*addresses, port_from=None, record=None):
    """A stub resolver that answers with exactly ``addresses``.

    ``record`` is a list the stub appends to, so a test can assert **how many
    times** the engine resolved.  One resolution per connection is itself a
    security property: a client that looks a name up twice has a window in
    which the second answer can differ from the validated one.
    """

    def _resolver(host, port, *_args, **_kwargs):
        if record is not None:
            record.append((host, port))
        out = []
        for address in addresses:
            family = socket.AF_INET6 if ":" in address else socket.AF_INET
            effective = port_from if port_from is not None else port
            sockaddr = (
                (address, effective or 0, 0, 0) if family == socket.AF_INET6
                else (address, effective or 0)
            )
            out.append((family, socket.SOCK_STREAM, 6, "", sockaddr))
        return out

    return _resolver


# ---------------------------------------------------------------------------
# A-1 / A-2 / A-11 -- the peer-address property
# ---------------------------------------------------------------------------


def _rebinding_attempt(engine, fixture, *, validated, allow, reported_peer=None):
    """Validate ``validated``, connect to ``fixture``, return the refusal."""
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    calls: list = []
    made: list[ConnectsElsewhere] = []

    def factory(family, type_):
        sock = ConnectsElsewhere(
            family, type_, fixture.sockaddr, reported_peer=reported_peer
        )
        made.append(sock)
        return sock

    net._RESOLVER = resolver_returning(
        *validated, port_from=fixture.port, record=calls
    )
    net._SOCKET_FACTORY = factory
    url = net.normalize_base_url(f"http://example.test:{fixture.port}")
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(url, method="GET", allow_classes=allow)
    return excinfo.value, calls, made


def test_a1_public_at_validation_loopback_at_connect_is_refused(engine, serve):
    """A-1: the deployed direction of a changed DNS answer cannot be reached.

    Validation is told the target is public (which the deployed leg permits);
    the socket layer then delivers a loopback peer.  The refusal is the
    post-connect peer check, and the fixture -- a different thread's record --
    confirms the connection carried **zero application bytes**.
    """
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    fixture = serve(responder_ok())
    refusal, calls, _made = _rebinding_attempt(
        engine, fixture, validated=("93.184.216.34",), allow=net.PUBLIC_ONLY
    )
    assert refusal.code == report.E_PEER_ADDRESS
    assert refusal.reason == "peer_not_validated"
    assert report.EXIT_FOR_RESULT[report.RESULT_DEGRADED] == 20
    # Resolved exactly once: there is no window between validation and connect
    # in which a second answer could be believed.
    assert len(calls) == 1
    assert_connected_but_sent_nothing(fixture)


_SET_GUARD = (
    "        if peer not in validated_addresses:\n"
    "            _close_quietly(sock)\n"
    '            raise SecurityRefusal(E_PEER_ADDRESS, "peer_not_validated")\n'
)
_CLASS_GUARD = (
    "        if classify_address(peer) not in allow_classes:\n"
    "            _close_quietly(sock)\n"
    '            raise SecurityRefusal(E_PEER_ADDRESS, "peer_class_refused")\n'
)


def test_a1_deletion_mutant_shows_which_guard_refuses(perturbed, serve):
    """A-1's deletion mutant, with its **measured** result rather than the
    predicted one.

    The plan predicts that deleting the post-connect peer check makes A-1 pass
    the request through.  Measured, it does not: the check is **two independent
    guards** -- "the peer is one of the validated addresses" and "the peer's
    class is permitted" -- and A-1's hazard trips both.  Deleting the set guard
    alone leaves the class guard to refuse a loopback peer on a public-only leg.

    That is a stronger result than the plan expected and it is recorded as such:
    each guard discriminates on its own, so the mutant that reaches the peer has
    to delete both, which the next test does.
    """
    engine = perturbed(edits={"net.py": [(_SET_GUARD, "")]})
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    fixture = serve(responder_ok(b"reached"))
    net._RESOLVER = resolver_returning("93.184.216.34", port_from=fixture.port)
    net._SOCKET_FACTORY = (
        lambda f, t: ConnectsElsewhere(f, t, fixture.sockaddr)
    )
    url = net.normalize_base_url(f"http://example.test:{fixture.port}")
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(url, method="GET", allow_classes=net.PUBLIC_ONLY)
    assert excinfo.value.reason == "peer_class_refused"
    assert_connected_but_sent_nothing(fixture)


def test_a1_deleting_both_peer_guards_reaches_the_unvalidated_peer(
    perturbed, serve
):
    """A-1's hazard with the whole check gone: the request is delivered.

    This is the failure A-1 exists to detect -- a client that validated a public
    address and then spoke to a loopback service, which is server-side request
    forgery in one step.
    """
    engine = perturbed(edits={"net.py": [(_SET_GUARD + _CLASS_GUARD, "")]})
    net = submodule(engine, "net")
    fixture = serve(responder_ok(b"reached"))
    net._RESOLVER = resolver_returning("93.184.216.34", port_from=fixture.port)
    net._SOCKET_FACTORY = (
        lambda f, t: ConnectsElsewhere(f, t, fixture.sockaddr)
    )
    url = net.normalize_base_url(f"http://example.test:{fixture.port}")
    response = net.perform_request(
        url, method="GET", allow_classes=net.PUBLIC_ONLY
    )
    assert response.status == 200
    assert response.body == b"reached"
    assert response.peer == "127.0.0.1"


def test_a2_peer_disagreeing_with_every_validated_address_is_refused(
    engine, serve
):
    """A-2: a genuinely different, genuinely real peer is refused.

    Nothing about the peer is reported by a stub here: validation is told
    ``127.0.0.1`` and the connection lands on a real ``::1`` listener, so
    ``getpeername()`` is the kernel's own answer.  Both addresses are loopback,
    which isolates "disagrees with the validated set" from "wrong class".
    """
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    fixture = serve(responder_ok(), host="::1")
    refusal, calls, _made = _rebinding_attempt(
        engine, fixture, validated=("127.0.0.1",), allow=net.LOOPBACK_ONLY
    )
    assert refusal.code == report.E_PEER_ADDRESS
    assert refusal.reason == "peer_not_validated"
    assert len(calls) == 1
    assert_connected_but_sent_nothing(fixture)


def test_a2_deletion_mutant_accepts_the_unvalidated_peer(perturbed, serve):
    """A-2's own deletion mutant, independent of A-1's."""
    engine = perturbed(edits={"net.py": [(_SET_GUARD, "")]})
    net = submodule(engine, "net")
    fixture = serve(responder_ok(b"v6"), host="::1")

    def factory(family, type_):
        return ConnectsElsewhere(family, type_, fixture.sockaddr)

    net._RESOLVER = resolver_returning("127.0.0.1", port_from=fixture.port)
    net._SOCKET_FACTORY = factory
    url = net.normalize_base_url(f"http://example.test:{fixture.port}")
    response = net.perform_request(
        url, method="GET", allow_classes=net.LOOPBACK_ONLY
    )
    assert response.body == b"v6"
    assert response.peer == "::1"


def test_a11_loopback_at_validation_non_loopback_at_connect_is_refused(
    engine, serve
):
    """A-11: the *agent-facing* direction, which is the plan's highest invariant.

    Validation is told ``127.0.0.1`` -- which the loopback-only leg permits --
    and the socket layer then reports a non-loopback peer.  This row substitutes
    the peer *report* rather than the peer itself, deliberately and for a stated
    reason: no non-loopback address is bindable on an arbitrary host (macOS
    refuses ``127.0.0.2``, and a machine may have no external interface at all),
    and a security criterion that only fires on a networked host is not a
    criterion.  ``getpeername()`` is the engine's sole peer oracle, so
    substituting it exercises exactly the branch under test.  A-2 covers the
    genuinely-real-second-peer case; the two rows together cover both branches
    of the check, each with its own mutant.
    """
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    fixture = serve(responder_ok())
    refusal, calls, _made = _rebinding_attempt(
        engine, fixture,
        validated=("127.0.0.1",),
        allow=net.LOOPBACK_ONLY,
        reported_peer=("203.0.113.7", fixture.port),
    )
    # Not in the validated set AND not loopback: the first guard fires, and the
    # class guard below is proven separately by the next test.
    assert refusal.code == report.E_PEER_ADDRESS
    assert refusal.reason == "peer_not_validated"
    assert len(calls) == 1
    assert_connected_but_sent_nothing(fixture)


def test_a11_class_guard_refuses_a_validated_but_non_loopback_peer(
    engine, serve
):
    """A-11, second branch: the class check refuses even a *validated* peer.

    The resolver validates a non-loopback address and the class check is what
    must stop it.  Without this row the ``peer_class_refused`` branch would
    never be exercised, and a criterion that never runs its own guard is the
    defect class this plan was written to prevent.
    """
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    fixture = serve(responder_ok())

    def factory(family, type_):
        return ConnectsElsewhere(
            family, type_, fixture.sockaddr,
            reported_peer=("203.0.113.7", fixture.port),
        )

    net._RESOLVER = resolver_returning("203.0.113.7", port_from=fixture.port)
    net._SOCKET_FACTORY = factory
    url = net.normalize_base_url(f"http://example.test:{fixture.port}")
    # The address-class validation refuses before a socket is created at all,
    # which is the stronger outcome: the loopback-only leg never reaches the
    # peer check because it never leaves policy validation.
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(url, method="GET", allow_classes=net.LOOPBACK_ONLY)
    assert excinfo.value.code == report.E_POLICY_REFUSED
    assert excinfo.value.reason == "address_class_refused"
    assert fixture.accepted == 0


def test_a11_deletion_mutant_is_its_own(perturbed, serve):
    """A-11's deletion mutant, not "as A-1": the two directions discriminate
    independently, which is only demonstrable by mutating for each."""
    engine = perturbed(edits={"net.py": [(_SET_GUARD, "")]})
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    fixture = serve(responder_ok(b"nonloop"))

    def factory(family, type_):
        return ConnectsElsewhere(
            family, type_, fixture.sockaddr,
            reported_peer=("203.0.113.7", fixture.port),
        )

    net._RESOLVER = resolver_returning("127.0.0.1", port_from=fixture.port)
    net._SOCKET_FACTORY = factory
    url = net.normalize_base_url(f"http://example.test:{fixture.port}")
    # With the set check gone the *class* check still fires -- so the mutant
    # does not silently succeed, it fails differently.  Recording the observed
    # code is the point: the two guards are independent.
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(url, method="GET", allow_classes=net.LOOPBACK_ONLY)
    assert excinfo.value.reason == "peer_class_refused"


def test_a11_deleting_both_peer_guards_reaches_the_non_loopback_peer(
    perturbed, serve
):
    """Both guards deleted: the agent-facing leg reaches a non-loopback peer.

    This is the whole invariant failing, and it is the mutant that proves the
    pair of guards -- not either one alone -- is what holds it.
    """
    engine = perturbed(edits={"net.py": [(_SET_GUARD + _CLASS_GUARD, "")]})
    net = submodule(engine, "net")
    fixture = serve(responder_ok(b"escaped"))

    def factory(family, type_):
        return ConnectsElsewhere(
            family, type_, fixture.sockaddr,
            reported_peer=("203.0.113.7", fixture.port),
        )

    net._RESOLVER = resolver_returning("127.0.0.1", port_from=fixture.port)
    net._SOCKET_FACTORY = factory
    url = net.normalize_base_url(f"http://example.test:{fixture.port}")
    response = net.perform_request(
        url, method="GET", allow_classes=net.LOOPBACK_ONLY
    )
    assert response.body == b"escaped"
    assert response.peer == "203.0.113.7"


# ---------------------------------------------------------------------------
# A-3 -- redirect address classes
# ---------------------------------------------------------------------------

_REDIRECT_ROWS = (
    ("loopback", "http://127.0.0.1:9/x"),
    ("loopback-v6", "http://[::1]:9/x"),
    ("private-v4", "http://10.1.2.3:9/x"),
    ("private-v6", "http://[fd00::1]:9/x"),
    ("link-local", "http://169.254.1.1:9/x"),
    ("link-local-v6", "http://[fe80::1]:9/x"),
    ("multicast", "http://224.0.0.1:9/x"),
    ("unspecified", "http://0.0.0.0:9/x"),
    ("unspecified-v6", "http://[::]:9/x"),
    ("reserved", "http://240.0.0.1:9/x"),
)


@pytest.mark.parametrize("label,location", _REDIRECT_ROWS, ids=[r[0] for r in _REDIRECT_ROWS])
def test_a3_redirect_to_each_refused_address_class(engine, serve, label, location):
    """A-3: every refused class is refused, and the redirect is never followed."""
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    fixture = serve(responder_redirect(location))
    url = net.normalize_base_url(fixture.origin())
    response = net.perform_request(
        url, method="GET", allow_classes=net.LOOPBACK_ONLY
    )
    assert response.is_redirect
    # The Location value never survives the boundary as content.
    assert response.redirect_withheld == report.CHANNEL_TOKENS["redirect_location"]
    refusal = net.classify_redirect(
        response, allow_classes=net.PUBLIC_ONLY, permitted_hosts=()
    )
    assert refusal.code == report.E_REDIRECT_REFUSED
    assert refusal.reason == "redirect_host_refused"
    # Exactly one connection: nothing was followed.
    assert fixture.accepted == 1


def test_a3_mixed_public_and_private_answer_set_is_refused(engine, serve):
    """A-3's mixed-answer row: one bad member refuses the whole set."""
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    fixture = serve(responder_ok())
    net._RESOLVER = resolver_returning(
        "93.184.216.34", "10.0.0.7", port_from=fixture.port
    )
    net._SOCKET_FACTORY = lambda f, t: ConnectsElsewhere(f, t, fixture.sockaddr)
    url = net.normalize_base_url(f"http://mixed.test:{fixture.port}")
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(url, method="GET", allow_classes=net.PUBLIC_ONLY)
    assert excinfo.value.reason == "address_class_refused"
    assert fixture.accepted == 0


def test_a3_deletion_mutant_removes_the_redirect_classifier(perturbed, serve):
    """A-3's deletion mutant: with the class test gone, every row goes benign."""
    engine = perturbed(edits={"net.py": [(
        "    if is_address_literal(host):\n"
        "        if classify_address(host) not in allow_classes:\n"
        "            return SecurityRefusal(E_REDIRECT_REFUSED, \"redirect_host_refused\")\n"
        "        return SecurityRefusal(E_REDIRECT_REFUSED, \"redirect_not_followed\")\n",
        "    if is_address_literal(host):\n"
        "        return SecurityRefusal(E_REDIRECT_REFUSED, \"redirect_not_followed\")\n",
    )]})
    net = submodule(engine, "net")
    observed = []
    for _label, location in _REDIRECT_ROWS:
        fixture = serve(responder_redirect(location))
        url = net.normalize_base_url(fixture.origin())
        response = net.perform_request(
            url, method="GET", allow_classes=net.LOOPBACK_ONLY
        )
        refusal = net.classify_redirect(
            response, allow_classes=net.PUBLIC_ONLY, permitted_hosts=()
        )
        observed.append(refusal.reason)
    # Every row now reports the generic "not followed" instead of naming the
    # refused class: the classifier is what discriminated.
    assert set(observed) == {"redirect_not_followed"}


# ---------------------------------------------------------------------------
# A-4 -- no credential or cookie carry-over
# ---------------------------------------------------------------------------

_MARKER = "Zq7WmarkerCRED4a91"


def _naive_follow(net, url, *, credential, allow_classes):
    """A client that *does* follow the redirect, carrying its credential.

    This is criterion A-4's liveness half.  Without it, "the second server saw
    no credential" and "the second server is unreachable by this fixture" are
    indistinguishable -- the exact vacuity the plan's standard forbids.
    """
    first = net.perform_request(
        url, method="GET", allow_classes=allow_classes, credential=credential
    )
    assert first.is_redirect
    location = None
    for name, value in first.headers:
        if name.lower() == "location":
            location = value
    assert location is not None
    second_url = net.normalize_base_url(location)
    return net.perform_request(
        second_url, method="GET", allow_classes=allow_classes,
        credential=credential,
    )


def test_a4_liveness_a_following_client_does_leak_the_credential(engine, serve):
    """A-4 phase (a): the second fixture records the credential when followed."""
    net = submodule(engine, "net")
    second = serve(responder_ok(b"second"))
    first = serve(responder_redirect(second.origin() + "/next"))
    url = net.normalize_base_url(first.origin())
    response = _naive_follow(
        net, url, credential=f"Bearer {_MARKER}",
        allow_classes=net.LOOPBACK_ONLY,
    )
    assert response.body == b"second"
    assert second.accepted == 1
    assert _MARKER in (second.records[0].header("Authorization") or "")


def test_a4_the_engine_carries_nothing_to_a_redirect_target(engine, serve):
    """A-4 phase (b): the engine never reaches the second fixture at all."""
    net = submodule(engine, "net")
    second = serve(responder_ok(b"second"))
    first = serve(responder_redirect(second.origin() + "/next"))
    url = net.normalize_base_url(first.origin())
    response = net.perform_request(
        url, method="GET", allow_classes=net.LOOPBACK_ONLY,
        credential=f"Bearer {_MARKER}",
        headers=(("Cookie", f"session={_MARKER}"),),
    )
    assert response.is_redirect
    # The intended target did receive the credential -- that is the request the
    # policy declared, and asserting it keeps this test from passing merely
    # because nothing was ever sent anywhere.
    assert _MARKER in (first.records[0].header("Authorization") or "")
    # The redirect target received nothing: no connection, no byte, no header.
    assert second.accepted == 0
    assert second.records == []


# ---------------------------------------------------------------------------
# A-5 -- redirect loops, method changes, connection isolation
# ---------------------------------------------------------------------------


def test_a5_self_referential_redirect_chain_produces_one_request(engine, serve):
    net = submodule(engine, "net")
    holder: dict = {}

    def responder(_record):
        return (
            f"HTTP/1.1 302 Found\r\nLocation: {holder['origin']}/loop\r\n"
            f"Content-Length: 0\r\nConnection: close\r\n\r\n"
        ).encode("iso-8859-1")

    fixture = serve(responder)
    holder["origin"] = fixture.origin()
    url = net.normalize_base_url(fixture.origin())
    response = net.perform_request(
        url, method="GET", allow_classes=net.LOOPBACK_ONLY
    )
    assert response.is_redirect
    assert fixture.accepted == 1


def test_a5_a_post_is_not_turned_into_a_get_by_a_redirect(engine, serve):
    net = submodule(engine, "net")
    fixture = serve(responder_redirect("/elsewhere"))
    url = net.normalize_base_url(fixture.origin())
    response = net.perform_request(
        url, method="POST", allow_classes=net.LOOPBACK_ONLY, body=b"{}"
    )
    assert response.is_redirect
    methods = [record.method for record in fixture.records]
    assert methods == ["POST"]
    assert "GET" not in methods


def test_a5_each_request_uses_its_own_connection(engine, serve):
    """A-5's connection-isolation row.

    **This row carries a hazard perturbation and no deletion mutant, and the
    reason is stated rather than left as an absence:** there is no connection
    pool in this engine to delete.  Isolation is structural -- ``perform_request``
    opens a socket, sends ``Connection: close``, and closes it in a ``finally``
    -- so the available evidence is that a keep-alive-capable fixture still sees
    two distinct connections from two distinct client ports.
    """
    net = submodule(engine, "net")
    first = serve(responder_ok(b"a"))
    second = serve(responder_ok(b"b"))
    r1 = net.perform_request(
        net.normalize_base_url(first.origin()), method="GET",
        allow_classes=net.LOOPBACK_ONLY,
    )
    r2 = net.perform_request(
        net.normalize_base_url(second.origin()), method="GET",
        allow_classes=net.LOOPBACK_ONLY,
    )
    assert (r1.body, r2.body) == (b"a", b"b")
    assert first.accepted == 1 and second.accepted == 1
    assert r1.local_port != r2.local_port
    assert first.records[0].header("Connection") == "close"


# ---------------------------------------------------------------------------
# A-6 -- caps, malformed input, timeouts
# ---------------------------------------------------------------------------


def test_a6_content_length_over_the_cap_refuses_before_reading(engine, serve):
    net = submodule(engine, "net")
    report = submodule(engine, "report")

    def responder(_record):
        return (
            b"HTTP/1.1 200 OK\r\nContent-Length: 999999999\r\n"
            b"Connection: close\r\n\r\n"
        )

    fixture = serve(responder)
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(fixture.origin()), method="GET",
            allow_classes=net.LOOPBACK_ONLY,
        )
    assert (excinfo.value.code, excinfo.value.reason) == (
        report.E_RESPONSE_CAP, "body_cap"
    )


def test_a6_body_one_byte_over_the_cap_refuses(engine, serve):
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    oversize = net.MAX_RESPONSE_BYTES + 1

    def responder(_record):
        return (
            b"HTTP/1.1 200 OK\r\nConnection: close\r\n\r\n" + b"x" * oversize
        )

    fixture = serve(responder)
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(fixture.origin()), method="GET",
            allow_classes=net.LOOPBACK_ONLY,
        )
    assert excinfo.value.reason == "body_cap"


def test_a6_deletion_mutant_removing_the_body_cap_accepts_the_oversized_body(
    perturbed, serve
):
    engine = perturbed(edits={"net.py": [
        ("MAX_RESPONSE_BYTES = 262_144", "MAX_RESPONSE_BYTES = 100_000_000"),
    ]})
    net = submodule(engine, "net")
    payload = b"x" * (262_144 + 1)

    def responder(_record):
        return b"HTTP/1.1 200 OK\r\nConnection: close\r\n\r\n" + payload

    fixture = serve(responder)
    response = net.perform_request(
        net.normalize_base_url(fixture.origin()), method="GET",
        allow_classes=net.LOOPBACK_ONLY,
    )
    assert len(response.body) == len(payload)


def test_a6_header_count_over_the_cap_refuses(engine, serve):
    net = submodule(engine, "net")
    report = submodule(engine, "report")

    def responder(_record):
        extra = "".join(f"X-Pad-{i}: v\r\n" for i in range(200))
        return (
            "HTTP/1.1 200 OK\r\n" + extra
            + "Content-Length: 0\r\nConnection: close\r\n\r\n"
        ).encode("iso-8859-1")

    fixture = serve(responder)
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(fixture.origin()), method="GET",
            allow_classes=net.LOOPBACK_ONLY,
        )
    assert excinfo.value.reason == "header_count_cap"


def test_a6_deletion_mutant_removing_the_header_count_cap(perturbed, serve):
    engine = perturbed(edits={"net.py": [
        ("MAX_HEADER_COUNT = 64", "MAX_HEADER_COUNT = 100_000"),
    ]})
    net = submodule(engine, "net")

    def responder(_record):
        extra = "".join(f"X-Pad-{i}: v\r\n" for i in range(200))
        return (
            "HTTP/1.1 200 OK\r\n" + extra
            + "Content-Length: 0\r\nConnection: close\r\n\r\n"
        ).encode("iso-8859-1")

    fixture = serve(responder)
    response = net.perform_request(
        net.normalize_base_url(fixture.origin()), method="GET",
        allow_classes=net.LOOPBACK_ONLY,
    )
    assert len(response.headers) > 64


def test_a6_header_line_over_the_cap_refuses(engine, serve):
    net = submodule(engine, "net")
    report = submodule(engine, "report")

    def responder(_record):
        return (
            b"HTTP/1.1 200 OK\r\nX-Long: " + b"y" * 20000
            + b"\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
        )

    fixture = serve(responder)
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(fixture.origin()), method="GET",
            allow_classes=net.LOOPBACK_ONLY,
        )
    assert excinfo.value.reason == "header_length_cap"


def test_a6_deletion_mutant_removing_the_header_length_cap(perturbed, serve):
    engine = perturbed(edits={"net.py": [
        ("MAX_HEADER_LINE = 8_192", "MAX_HEADER_LINE = 1_000_000"),
    ]})
    net = submodule(engine, "net")

    def responder(_record):
        return (
            b"HTTP/1.1 200 OK\r\nX-Long: " + b"y" * 20000
            + b"\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
        )

    fixture = serve(responder)
    response = net.perform_request(
        net.normalize_base_url(fixture.origin()), method="GET",
        allow_classes=net.LOOPBACK_ONLY,
    )
    assert len(response.header("X-Long") or "") == 20000


def test_a6_chunked_response_is_read(engine, serve):
    net = submodule(engine, "net")

    def responder(_record):
        return (
            b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n"
            b"Connection: close\r\n\r\n"
            b"4\r\nabcd\r\n3\r\nefg\r\n0\r\n\r\n"
        )

    fixture = serve(responder)
    response = net.perform_request(
        net.normalize_base_url(fixture.origin()), method="GET",
        allow_classes=net.LOOPBACK_ONLY,
    )
    assert response.body == b"abcdefg"


def test_a6_malformed_chunk_size_refuses(engine, serve):
    net = submodule(engine, "net")
    report = submodule(engine, "report")

    def responder(_record):
        return (
            b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n"
            b"Connection: close\r\n\r\nzz\r\nabcd\r\n"
        )

    fixture = serve(responder)
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(fixture.origin()), method="GET",
            allow_classes=net.LOOPBACK_ONLY,
        )
    assert excinfo.value.reason == "encoding_malformed"


def test_a6_partial_body_refuses(engine, serve):
    net = submodule(engine, "net")
    report = submodule(engine, "report")

    def responder(_record):
        return b"HTTP/1.1 200 OK\r\nContent-Length: 100\r\nConnection: close\r\n\r\nshort"

    fixture = serve(responder)
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(fixture.origin()), method="GET",
            allow_classes=net.LOOPBACK_ONLY,
        )
    assert excinfo.value.reason == "encoding_malformed"


def test_a6_malformed_status_line_refuses(engine, serve):
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    fixture = serve(lambda _r: b"NOT-HTTP AT ALL\r\n\r\n")
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(fixture.origin()), method="GET",
            allow_classes=net.LOOPBACK_ONLY,
        )
    assert excinfo.value.reason == "status_line_malformed"


def test_a6_invalid_utf8_body_is_carried_as_bytes_not_crashed_through(
    engine, serve
):
    net = submodule(engine, "net")
    fixture = serve(lambda _r: (
        b"HTTP/1.1 200 OK\r\nContent-Length: 4\r\nConnection: close\r\n\r\n"
        b"\xff\xfe\xfd\xfc"
    ))
    response = net.perform_request(
        net.normalize_base_url(fixture.origin()), method="GET",
        allow_classes=net.LOOPBACK_ONLY,
    )
    assert response.body == b"\xff\xfe\xfd\xfc"


def test_a6_duplicate_headers_are_all_retained(engine, serve):
    net = submodule(engine, "net")
    fixture = serve(responder_ok(extra=(
        ("Set-Cookie", "a=1"), ("Set-Cookie", "b=2"),
    )))
    response = net.perform_request(
        net.normalize_base_url(fixture.origin()), method="GET",
        allow_classes=net.LOOPBACK_ONLY,
    )
    assert response.header_all("Set-Cookie") == ("a=1", "b=2")


def test_a6_a_stalled_response_hits_the_read_timeout(engine, serve):
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    fixture = serve(lambda _r: (ok_response(b"late"), 1.5))
    started = time.monotonic()
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(fixture.origin()), method="GET",
            allow_classes=net.LOOPBACK_ONLY, read_timeout=0.25,
        )
    assert excinfo.value.code == report.E_TIMEOUT
    assert excinfo.value.reason == "read_timeout"
    assert time.monotonic() - started < 1.4


def test_a6_204_and_head_carry_no_body(engine, serve):
    net = submodule(engine, "net")
    fixture = serve(lambda _r: b"HTTP/1.1 204 No Content\r\nConnection: close\r\n\r\n")
    response = net.perform_request(
        net.normalize_base_url(fixture.origin()), method="GET",
        allow_classes=net.LOOPBACK_ONLY,
    )
    assert (response.status, response.body) == (204, b"")

    head = serve(responder_ok(b"ignored"))
    response = net.perform_request(
        net.normalize_base_url(head.origin()), method="HEAD",
        allow_classes=net.LOOPBACK_ONLY,
    )
    assert response.body == b""
    assert head.records[0].method == "HEAD"


def test_a6_an_oversized_request_body_refuses_before_connecting(engine, serve):
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    fixture = serve(responder_ok())
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(fixture.origin()), method="POST",
            allow_classes=net.LOOPBACK_ONLY,
            body=b"z" * (net.MAX_REQUEST_BYTES + 1),
        )
    assert excinfo.value.reason == "body_cap"
    assert fixture.accepted == 0


# ---------------------------------------------------------------------------
# A-7 -- TLS
# ---------------------------------------------------------------------------


def _openssl() -> str:
    found = shutil.which("openssl")
    # Deliberately a hard failure rather than a skip: the plan's acceptance
    # criteria require zero skipped nodes, and a TLS gate that quietly skips is
    # a TLS gate that does not exist.  Recorded as a portability omission.
    assert found, "openssl is required to generate the A-7 certificate fixtures"
    return found


def make_cert(
    directory: Path, name: str, *, common_name: str,
    sans: str = "DNS:localhost,IP:127.0.0.1",
    not_before: "str | None" = None, not_after: "str | None" = None,
) -> "tuple[Path, Path]":
    """Generate a self-signed certificate into ``directory``.

    Key material is generated into the test's ``tmp_path`` and never committed,
    which is criterion A-7's own fence.
    """
    cert = directory / f"{name}-cert.pem"
    key = directory / f"{name}-key.pem"
    argv = [
        _openssl(), "req", "-x509", "-newkey", "rsa:2048",
        "-keyout", str(key), "-out", str(cert), "-nodes",
        "-subj", f"/CN={common_name}", "-addext", f"subjectAltName={sans}",
    ]
    if not_before and not_after:
        argv += ["-not_before", not_before, "-not_after", not_after]
    else:
        argv += ["-days", "2"]
    subprocess.run(argv, check=True, capture_output=True)
    return cert, key


def tls_server_context(cert: Path, key: Path) -> ssl.SSLContext:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(str(cert), str(key))
    return context


def test_a7_untrusted_chain_refuses(engine, serve, tmp_path, monkeypatch):
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    cert, key = make_cert(tmp_path, "self", common_name="localhost")
    other, _ = make_cert(tmp_path, "other-ca", common_name="unrelated.invalid")
    monkeypatch.setenv("SSL_CERT_FILE", str(other))
    fixture = serve(responder_ok(), tls=tls_server_context(cert, key))
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(fixture.origin("https", "localhost")),
            method="GET", allow_classes=net.LOOPBACK_ONLY,
        )
    assert excinfo.value.code == report.E_TLS_REFUSED
    assert excinfo.value.reason == "tls_chain_untrusted"


def test_a7_hostname_mismatch_refuses(engine, serve, tmp_path, monkeypatch):
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    cert, key = make_cert(
        tmp_path, "wronghost", common_name="not-localhost.invalid",
        sans="DNS:not-localhost.invalid",
    )
    monkeypatch.setenv("SSL_CERT_FILE", str(cert))
    fixture = serve(responder_ok(), tls=tls_server_context(cert, key))
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(fixture.origin("https", "localhost")),
            method="GET", allow_classes=net.LOOPBACK_ONLY,
        )
    assert excinfo.value.code == report.E_TLS_REFUSED
    assert excinfo.value.reason == "tls_hostname_mismatch"


def test_a7_expired_certificate_refuses(engine, serve, tmp_path, monkeypatch):
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    cert, key = make_cert(
        tmp_path, "expired", common_name="localhost",
        not_before="20240101000000Z", not_after="20240201000000Z",
    )
    monkeypatch.setenv("SSL_CERT_FILE", str(cert))
    fixture = serve(responder_ok(), tls=tls_server_context(cert, key))
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(fixture.origin("https", "localhost")),
            method="GET", allow_classes=net.LOOPBACK_ONLY,
        )
    assert excinfo.value.code == report.E_TLS_REFUSED
    assert excinfo.value.reason == "tls_expired"


def test_a7_a_non_tls_peer_on_an_https_target_refuses(engine, serve):
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    fixture = serve(lambda _r: b"not a tls record at all\r\n")
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(fixture.origin("https", "localhost")),
            method="GET", allow_classes=net.LOOPBACK_ONLY,
        )
    assert excinfo.value.code == report.E_TLS_REFUSED
    assert excinfo.value.reason in ("tls_protocol", "tls_handshake_failed")


def test_a7_a_trusted_matching_certificate_is_accepted(
    engine, serve, tmp_path, monkeypatch
):
    """The positive control: without it, all four refusals above could be
    "TLS never works here" rather than "these four shapes are refused"."""
    net = submodule(engine, "net")
    cert, key = make_cert(tmp_path, "good", common_name="localhost")
    monkeypatch.setenv("SSL_CERT_FILE", str(cert))
    fixture = serve(responder_ok(b"secure"), tls=tls_server_context(cert, key))
    response = net.perform_request(
        net.normalize_base_url(fixture.origin("https", "localhost")),
        method="GET", allow_classes=net.LOOPBACK_ONLY,
    )
    assert (response.status, response.body, response.tls) == (200, b"secure", True)
    assert response.peer == "127.0.0.1"


def test_a7_deletion_mutant_cert_none_accepts_three_of_the_four(
    perturbed, serve, tmp_path, monkeypatch
):
    """A-7's deletion mutant, with its measured result recorded honestly.

    The plan predicts "all four must fail" under ``CERT_NONE``.  Three do: the
    untrusted chain, the hostname mismatch and the expired certificate all stop
    refusing.  **The fourth does not, and cannot** -- ``CERT_NONE`` does not make
    a peer that speaks no TLS speak TLS, so the protocol row still refuses.  The
    plan's expectation is over-broad by exactly that one row, and this test pins
    the accurate version.
    """
    engine = perturbed(edits={"net.py": [(
        "    context = ssl.create_default_context()\n"
        "    context.check_hostname = True\n"
        "    context.verify_mode = ssl.CERT_REQUIRED\n",
        "    context = ssl.create_default_context()\n"
        "    context.check_hostname = False\n"
        "    context.verify_mode = ssl.CERT_NONE\n",
    )]})
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    monkeypatch.delenv("SSL_CERT_FILE", raising=False)

    # rows 1-3: verification is what refused them, and it is gone.
    untrusted_cert, untrusted_key = make_cert(
        tmp_path, "m-self", common_name="localhost"
    )
    mismatch_cert, mismatch_key = make_cert(
        tmp_path, "m-host", common_name="nope.invalid", sans="DNS:nope.invalid"
    )
    expired_cert, expired_key = make_cert(
        tmp_path, "m-exp", common_name="localhost",
        not_before="20240101000000Z", not_after="20240201000000Z",
    )
    for cert, key in (
        (untrusted_cert, untrusted_key),
        (mismatch_cert, mismatch_key),
        (expired_cert, expired_key),
    ):
        fixture = serve(responder_ok(b"weak"), tls=tls_server_context(cert, key))
        response = net.perform_request(
            net.normalize_base_url(fixture.origin("https", "localhost")),
            method="GET", allow_classes=net.LOOPBACK_ONLY,
        )
        assert response.body == b"weak"

    # row 4: still refuses, for a reason CERT_NONE has no bearing on.
    plain = serve(lambda _r: b"not a tls record at all\r\n")
    with pytest.raises(report.SecurityRefusal) as excinfo:
        net.perform_request(
            net.normalize_base_url(plain.origin("https", "localhost")),
            method="GET", allow_classes=net.LOOPBACK_ONLY,
        )
    assert excinfo.value.code == report.E_TLS_REFUSED


# ---------------------------------------------------------------------------
# A-8(a) -- ordering: no refusal reaches DNS or a socket
# ---------------------------------------------------------------------------

_REFUSABLE_URLS = (
    "ftp://example.test/x",
    "http://user:pw@example.test/x",
    "https://example.test/x#frag",
    "https://example.test/x?q=1",
    "example.test/x",
    "http://example.test:0/x",
)


@pytest.mark.parametrize("raw", _REFUSABLE_URLS)
def test_a8a_a_refusable_target_never_reaches_dns_or_a_socket(engine, raw):
    """A-8(a): the two sound probes, asserted untouched.

    Both probes are on the standard library and neither is an accessor a caller
    can route around: an address cannot be resolved without ``getaddrinfo`` and
    a connection cannot be opened without a socket object.
    """
    net = submodule(engine, "net")
    report = submodule(engine, "report")
    resolver_calls: list = []
    socket_calls: list = []
    net._RESOLVER = lambda *a, **k: resolver_calls.append(a) or []
    net._SOCKET_FACTORY = lambda *a, **k: socket_calls.append(a)
    with pytest.raises(report.SecurityRefusal):
        net.normalize_base_url(raw)
    assert resolver_calls == []
    assert socket_calls == []


def test_a8a_a_refusable_policy_never_reaches_dns_or_a_socket(engine, tmp_path):
    net = submodule(engine, "net")
    policy = submodule(engine, "policy")
    report = submodule(engine, "report")
    resolver_calls: list = []
    socket_calls: list = []
    net._RESOLVER = lambda *a, **k: resolver_calls.append(a) or []
    net._SOCKET_FACTORY = lambda *a, **k: socket_calls.append(a)
    documents = (
        {"schema": policy.API_SCHEMA_ID, "configured": True, "surprise": 1},
        {"schema": "wrong.id", "configured": True},
        {"schema": policy.API_SCHEMA_ID, "configured": True,
         "local": {"base_url": "http://10.0.0.1", "principals": [],
                   "operations": []}},
    )
    for document in documents:
        with pytest.raises(report.SecurityRefusal):
            policy.parse_policy(document, kind=policy.KIND_API,
                                path=tmp_path / "p.json")
    assert resolver_calls == []
    assert socket_calls == []


def test_a8a_deletion_mutant_moving_validation_below_the_resolve_fires_the_probe(
    perturbed
):
    """A-8(a)'s deletion mutant: a class check moved after the resolve is seen."""
    engine = perturbed(edits={"net.py": [(
        '    if parts.query:\n'
        '        raise SecurityRefusal(E_POLICY_REFUSED, "url_query")\n',
        "",
    )]})
    net = submodule(engine, "net")
    resolver_calls: list = []
    net._RESOLVER = lambda *a, **k: resolver_calls.append(a) or []
    net._SOCKET_FACTORY = lambda *a, **k: (_ for _ in ()).throw(
        AssertionError("must not be reached")
    )
    # With the scheme check gone the URL parses far enough to be resolved,
    # which the probe records -- the ordering guarantee is what was deleted.
    try:
        net.perform_request(
            net.normalize_base_url("https://example.test/x?q=1"), method="GET",
            allow_classes=net.PUBLIC_ONLY,
        )
    except Exception:
        pass
    assert resolver_calls != [], "the probe must fire once validation moves"


def test_a8_refusal_and_absent_credential_are_two_distinct_codes(engine):
    """A-8(c)'s precondition, asserted here because A-8(c) is unobservable
    otherwise.  The facade-level subprocess oracle lives in Chunk B's suite."""
    report = submodule(engine, "report")
    assert report.E_POLICY_REFUSED != report.E_CREDENTIAL_ABSENT
    assert {report.E_POLICY_REFUSED, report.E_CREDENTIAL_ABSENT} <= report.ERROR_CODES


# ---------------------------------------------------------------------------
# A-9 -- the off-tree report
# ---------------------------------------------------------------------------


def test_a9_report_directory_is_private_and_outside_the_repository(
    engine, tmp_path
):
    report = submodule(engine, "report")
    repo = tmp_path / "checkout"
    repo.mkdir()
    directory = report.create_report_dir(repo)
    try:
        assert directory.is_dir()
        assert repo.resolve() not in directory.resolve().parents
        assert oct(directory.stat().st_mode)[-3:] == "700"
        written = report.write_report(directory, {"schema": "x"})
        assert written.name == "report.json"
        assert oct(written.stat().st_mode)[-3:] == "600"
        assert [p.name for p in directory.iterdir()] == ["report.json"]
        with pytest.raises(report.SecurityRefusal) as excinfo:
            report.write_report(directory, {"schema": "y"})
        assert excinfo.value.reason == "report_exists"
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def hostile_tempdir(monkeypatch, path) -> None:
    """Point the process's temporary directory at ``path``.

    Set on ``tempfile.tempdir`` rather than on ``TMPDIR``, and the difference
    is load-bearing rather than cosmetic: ``gettempdir()`` caches its answer and
    **silently falls back** to the next writable candidate when ``TMPDIR`` is
    unusable, so a test that only set the variable would exercise the platform
    default and pass without ever presenting the hazard.  What the engine sees
    is identical either way -- it calls ``tempfile.mkdtemp``.
    """
    monkeypatch.setenv("TMPDIR", str(path))
    monkeypatch.setattr(tempfile, "tempdir", str(path))


def test_a9_tmpdir_inside_the_checkout_refuses(engine, tmp_path, monkeypatch):
    report = submodule(engine, "report")
    repo = tmp_path / "checkout"
    (repo / "inside").mkdir(parents=True)
    hostile_tempdir(monkeypatch, repo / "inside")
    with pytest.raises(report.SecurityRefusal) as excinfo:
        report.create_report_dir(repo)
    assert (excinfo.value.code, excinfo.value.reason) == (
        report.E_REPORT_DIR_REFUSED, "inside_repository"
    )


def test_a9_tmpdir_symlinked_into_the_checkout_refuses(
    engine, tmp_path, monkeypatch
):
    report = submodule(engine, "report")
    repo = tmp_path / "checkout"
    (repo / "evidence").mkdir(parents=True)
    link = tmp_path / "looks-outside"
    link.symlink_to(repo / "evidence", target_is_directory=True)
    hostile_tempdir(monkeypatch, link)
    with pytest.raises(report.SecurityRefusal) as excinfo:
        report.create_report_dir(repo)
    assert excinfo.value.reason == "inside_repository"


def test_a9_tmpdir_pointing_at_a_file_refuses(engine, tmp_path, monkeypatch):
    report = submodule(engine, "report")
    repo = tmp_path / "checkout"
    repo.mkdir()
    blocker = tmp_path / "not-a-directory"
    blocker.write_text("x", encoding="utf-8")
    hostile_tempdir(monkeypatch, blocker)
    with pytest.raises(report.SecurityRefusal) as excinfo:
        report.create_report_dir(repo)
    assert excinfo.value.reason == "tempdir_unavailable"


def test_a9_tmpdir_that_does_not_exist_refuses(engine, tmp_path, monkeypatch):
    report = submodule(engine, "report")
    repo = tmp_path / "checkout"
    repo.mkdir()
    hostile_tempdir(monkeypatch, tmp_path / "absent" / "deeper")
    with pytest.raises(report.SecurityRefusal) as excinfo:
        report.create_report_dir(repo)
    assert excinfo.value.reason == "tempdir_unavailable"


def test_a9_deletion_mutant_removing_containment_lets_the_report_land_in_the_repo(
    perturbed, tmp_path, monkeypatch
):
    engine = perturbed(edits={"report.py": [(
        "    for candidate in (created, real):\n"
        "        if candidate == root or root in candidate.parents:\n"
        '            _refuse("inside_repository")\n',
        "",
    )]})
    report = submodule(engine, "report")
    repo = tmp_path / "checkout"
    (repo / "inside").mkdir(parents=True)
    hostile_tempdir(monkeypatch, repo / "inside")
    directory = report.create_report_dir(repo)
    # Security evidence now sits inside the checkout, one `git add -A` from a
    # commit.  That is the failure A-9 exists to prevent.
    assert repo.resolve() in directory.resolve().parents


# ---------------------------------------------------------------------------
# A-10 -- engine completeness
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("member", ("policy.py", "net.py", "report.py"))
def test_a10_a_missing_engine_member_is_engine_incomplete(tmp_path, member):
    """A-10's engine half.  The facade-exit-20 half lands with the facades."""
    _ENGINE_SEQ[0] += 1
    name = f"_security_net_missing_{_ENGINE_SEQ[0]}"
    target = tmp_path / name
    shutil.copytree(ENGINE_SRC, target)
    (target / member).unlink()
    try:
        with pytest.raises(Exception) as excinfo:
            _import_engine_package(target, name)
        raised = excinfo.value
        assert type(raised).__name__ == "EngineIncomplete"
        assert getattr(raised, "code", None) == "engine_incomplete"
        assert getattr(raised, "reason", None) == "member_absent"
    finally:
        _drop_engine(name)


def test_a10_a_contract_disagreement_is_engine_incomplete(perturbed):
    engine = perturbed(edits={"report.py": [
        ('ENGINE_CONTRACT = "1"', 'ENGINE_CONTRACT = "99"'),
    ]})
    with pytest.raises(engine.EngineIncomplete) as excinfo:
        engine.verify_engine_complete()
    assert excinfo.value.reason == "contract_disagreement"


def test_a10_deletion_mutant_removing_the_self_check_runs_a_partial_engine(
    tmp_path
):
    _ENGINE_SEQ[0] += 1
    name = f"_security_net_nocheck_{_ENGINE_SEQ[0]}"
    target = tmp_path / name
    shutil.copytree(ENGINE_SRC, target)
    init = target / "__init__.py"
    text = init.read_text(encoding="utf-8")
    anchor = "_check_members_present()\n\n\ndef verify_engine_complete"
    assert text.count(anchor) == 1
    init.write_text(
        text.replace(anchor, "\n\ndef verify_engine_complete"), encoding="utf-8"
    )
    (target / "net.py").unlink()
    try:
        # Import now succeeds with a member missing: the package is importable
        # and a facade would proceed to read a policy on a partial engine.
        package = _import_engine_package(target, name)
        assert package.ENGINE_CONTRACT == "1"
    finally:
        _drop_engine(name)


def test_a10_the_member_list_matches_what_is_on_disk(engine):
    on_disk = sorted(p.name for p in ENGINE_SRC.iterdir() if p.suffix == ".py")
    assert sorted(engine.ENGINE_MEMBERS) == on_disk


# ---------------------------------------------------------------------------
# A-12 -- the live transport proof, engine level
# ---------------------------------------------------------------------------


def test_live_transport_nothing_stubbed_records_the_peer_out_of_process(
    engine, serve
):
    """A-12's engine-level half: no resolver stub, no patched socket, no ssl.

    The peer is read from the *listening fixture's* record -- a different
    thread's view of the connection -- and compared with what the engine
    believes.  The four-public-entry-point form of A-12 requires the facades and
    lands with them; this row is the transport half and it is the half A-1/A-2/
    A-11 cannot supply, because a stub cannot show that the socket obeyed the
    decision.
    """
    net = submodule(engine, "net")
    assert net._RESOLVER is socket.getaddrinfo
    assert net._SOCKET_FACTORY is socket.socket
    fixture = serve(responder_ok(b"live"))
    url = net.normalize_base_url(f"http://localhost:{fixture.port}")
    response = net.perform_request(
        url, method="GET", allow_classes=net.LOOPBACK_ONLY,
        credential=f"Bearer {_MARKER}",
    )
    assert (response.status, response.body) == (200, b"live")
    observed_peer = fixture.records[0].peer[0]
    assert net.canonical_ip(observed_peer) == response.peer
    assert net.classify_address(response.peer) == "loopback"
    assert response.resolutions == 1
    # The credential reached the declared target and nothing else about it is
    # retained by the engine's own record of the exchange.
    assert _MARKER in (fixture.records[0].header("Authorization") or "")
    assert _MARKER not in repr(sorted(response.headers))
    assert _MARKER not in response.body.decode("utf-8", "replace")


def test_live_transport_over_real_tls(engine, serve, tmp_path, monkeypatch):
    net = submodule(engine, "net")
    cert, key = make_cert(tmp_path, "live", common_name="localhost")
    monkeypatch.setenv("SSL_CERT_FILE", str(cert))
    fixture = serve(responder_ok(b"live-tls"), tls=tls_server_context(cert, key))
    url = net.normalize_base_url(f"https://localhost:{fixture.port}")
    response = net.perform_request(
        url, method="GET", allow_classes=net.LOOPBACK_ONLY
    )
    assert (response.status, response.body, response.tls) == (
        200, b"live-tls", True
    )
    assert net.canonical_ip(fixture.records[0].peer[0]) == response.peer


# ---------------------------------------------------------------------------
# The sanitization seam, and the constants that must not drift
# ---------------------------------------------------------------------------


def test_channel_passthrough_is_empty_in_shipped_source():
    """The D-2 liveness seam must be inert in what Cairn ships.

    It is a frozen empty set with no writer: no environment variable, policy
    field, CLI flag or import hook reaches it.  This test pins both the value
    and the literal, so a future edit that populated it goes red here.
    """
    source = (ENGINE_SRC / "report.py").read_text(encoding="utf-8")
    assert "_CHANNEL_PASSTHROUGH: frozenset = frozenset()" in source
    assert source.count("_CHANNEL_PASSTHROUGH") == 2
    sys.path.insert(0, str(ENGINE_SRC.parent))
    try:
        module = importlib.import_module("_security_net.report")
        assert module._CHANNEL_PASSTHROUGH == frozenset()
    finally:
        sys.path.remove(str(ENGINE_SRC.parent))
        for key in [k for k in sys.modules if k.startswith("_security_net")]:
            del sys.modules[key]


def test_the_shipped_engine_declares_no_verification_weakening():
    """No code path in the engine can turn certificate checking off.

    Asserted over the **parsed** source, not over its text: the docstrings name
    ``CERT_NONE`` in order to say it is absent, and a grep would flag its own
    prohibition.  What is checked is that no expression evaluates to
    ``ssl.CERT_NONE`` / ``_create_unverified_context`` and that
    ``check_hostname`` is never assigned a falsey constant.
    """
    import ast

    for member in sorted(ENGINE_SRC.glob("*.py")):
        tree = ast.parse(member.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                assert node.attr not in (
                    "CERT_NONE", "CERT_OPTIONAL", "_create_unverified_context"
                ), f"{member.name}: {node.attr}"
            if isinstance(node, ast.Name):
                assert node.id not in (
                    "CERT_NONE", "_create_unverified_context"
                ), f"{member.name}: {node.id}"
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    name = getattr(target, "attr", getattr(target, "id", ""))
                    if name == "check_hostname":
                        assert isinstance(node.value, ast.Constant)
                        assert node.value.value is True, f"{member.name}"
                    if name == "verify_mode":
                        assert isinstance(node.value, ast.Attribute)
                        assert node.value.attr == "CERT_REQUIRED"


def test_every_engine_member_is_standard_library_only(engine):
    """The adopter takes on zero runtime dependencies for these capabilities."""
    import ast

    stdlib = set(sys.stdlib_module_names)
    for member in ENGINE_SRC.glob("*.py"):
        tree = ast.parse(member.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[0] in stdlib, alias.name
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    continue
                assert node.module is not None
                assert node.module.split(".")[0] in stdlib, node.module


def test_magnitude_buckets_hide_exact_sizes(engine):
    report = submodule(engine, "report")
    assert report.magnitude_bucket(0) == "empty"
    assert report.magnitude_bucket(3) == report.magnitude_bucket(31) == "short"
    assert report.magnitude_bucket(64) == "short"
    assert report.magnitude_bucket(65) == "medium"
    assert report.magnitude_bucket(65537) == "oversized"
    assert report.value_magnitude("a" * 3) == report.value_magnitude("b" * 31)
    assert report.value_magnitude([1, 2]) == report.value_magnitude([1, 2, 3])


def test_fingerprints_are_stable_within_a_run_and_differ_across_keys(engine):
    report = submodule(engine, "report")
    first = report.Fingerprinter()
    assert first.fingerprint("x") == first.fingerprint("x")
    assert first.fingerprint("x") != first.fingerprint("y")
    second = report.Fingerprinter()
    assert first.fingerprint("x") != second.fingerprint("x")
    with pytest.raises(report.SecurityRefusal) as excinfo:
        report.Fingerprinter(key=b"tooshort")
    assert excinfo.value.code == report.E_RANDOMNESS_UNAVAILABLE


def test_a_finding_never_carries_an_integer_or_an_observed_value(engine):
    """The exact-cardinality class, closed structurally rather than field by
    field.  Criterion D-3's hazard -- adding ``len(value)`` -- breaks this."""
    report = submodule(engine, "report")
    finding = report.build_finding(
        check_id="c1", detail="d", operation_id="op", case_id="case",
        principal_ids=("p1", "p2"), method="GET", status=403,
        observed_value="a" * 4096,
        fingerprinter=report.Fingerprinter(),
    )
    assert set(finding) <= report.FINDING_KEYS
    assert finding["status_class"] == "4xx"
    assert finding["observed_magnitude"] == "large"
    assert "4096" not in repr(finding)
    for value in finding.values():
        assert not isinstance(value, int)
        if isinstance(value, list):
            assert all(isinstance(v, str) for v in value)


# ---------------------------------------------------------------------------
# A2 -- the strict policy schema
# ---------------------------------------------------------------------------


def _api_local(**overrides) -> dict:
    section = {
        "base_url": "http://127.0.0.1:8099",
        "principals": [{"id": "p1"}, {"id": "p2"}],
        "operations": [{
            "id": "read-order", "method": "GET", "path": "/orders/1",
            "kind": "object",
            "cases": [
                {"id": "owner", "principal": "p1", "expect": "allow",
                 "status": [200], "require_present": ["/id"],
                 "require_absent": ["/ssn"]},
                {"id": "other", "principal": "p2", "expect": "deny",
                 "status": [403, 404]},
            ],
        }],
    }
    section.update(overrides)
    return section


def _api_deployed(ordinals=("p3", "p4"), **overrides) -> dict:
    first, second = ordinals
    section = {
        "base_url": "https://api.example.org",
        "principals": [{"id": first}, {"id": second}],
        "operations": [{
            "id": "health", "method": "GET", "path": "/health",
            "kind": "function",
            "cases": [
                {"id": "up", "principal": first, "expect": "allow",
                 "status": [200]},
                {"id": "denied", "principal": second, "expect": "deny",
                 "status": [401]},
            ],
        }],
    }
    section.update(overrides)
    return section


def api_document(policy_mod, *, local=None, deployed=None, **top) -> dict:
    document = {
        "schema": policy_mod.API_SCHEMA_ID,
        "configured": True,
        "local": local if local is not None else _api_local(),
    }
    if deployed is not None:
        document["deployed"] = deployed
    document.update(top)
    return document


def test_a2_a_valid_policy_is_accepted_and_derives_its_credential_names(
    engine, tmp_path
):
    """The positive control for the schema.

    Without it, every refusal row below could be "this schema accepts nothing",
    and a policy language that cannot express a correct policy is not a
    stricter one -- it is a broken one.
    """
    policy = submodule(engine, "policy")
    document = api_document(
        policy, deployed=_api_deployed(), openapi_document="docs/openapi.json"
    )
    parsed = policy.parse_policy(
        document, kind=policy.KIND_API, path=tmp_path / "p.json"
    )
    assert parsed.configured is True
    assert parsed.section("local")["base_url"].normalized == "http://127.0.0.1:8099"
    # Derived from the ordinal, never supplied by policy, and disjoint across
    # the two sections by schema -- the structural half of criterion B-4.
    assert parsed.credential_names("local") == (
        "CAIRN_API_P1_CREDENTIAL", "CAIRN_API_P2_CREDENTIAL"
    )
    assert parsed.credential_names("deployed") == (
        "CAIRN_API_P3_CREDENTIAL", "CAIRN_API_P4_CREDENTIAL"
    )
    assert not set(parsed.credential_names("local")) & set(
        parsed.credential_names("deployed")
    )


def _api_refusal_rows(policy):
    """Each row: label, document, expected reason token."""
    return [
        ("unknown top-level key",
         api_document(policy, surprise=1), "unknown_key"),
        ("wrong schema id",
         {**api_document(policy), "schema": "cairn.security.other.v1"},
         "bad_schema_id"),
        ("configured is not a bool",
         {**api_document(policy), "configured": "yes"}, "bad_type"),
        ("no local section",
         {"schema": policy.API_SCHEMA_ID, "configured": False}, "missing_key"),
        ("configured true over an empty matrix",
         api_document(policy, local=_api_local(operations=[])),
         "no_operations"),
        ("only a positive case",
         api_document(policy, local=_api_local(operations=[{
             "id": "o", "method": "GET", "path": "/x", "kind": "object",
             "cases": [{"id": "a", "principal": "p1", "expect": "allow",
                        "status": [200]}]}])),
         "no_denial_case"),
        ("object operation with a single principal",
         api_document(policy, local=_api_local(operations=[{
             "id": "o", "method": "GET", "path": "/x", "kind": "object",
             "cases": [{"id": "a", "principal": "p1", "expect": "allow",
                        "status": [200]},
                       {"id": "d", "principal": "p1", "expect": "deny",
                        "status": [403]}]}])),
         "no_denial_case"),
        ("duplicate operation id",
         api_document(policy, local=_api_local(
             operations=_api_local()["operations"] * 2)),
         "duplicate_id"),
        ("duplicate principal ordinal",
         api_document(policy, local=_api_local(
             principals=[{"id": "p1"}, {"id": "p1"}])),
         "duplicate_id"),
        ("named principal rather than an ordinal",
         api_document(policy, local=_api_local(
             principals=[{"id": "alice@example.org"}, {"id": "p2"}])),
         "bad_principal_ordinal"),
        ("zero ordinal",
         api_document(policy, local=_api_local(
             principals=[{"id": "p0"}, {"id": "p2"}])),
         "bad_principal_ordinal"),
        ("oversized ordinal",
         api_document(policy, local=_api_local(
             principals=[{"id": "p1000"}, {"id": "p2"}])),
         "bad_principal_ordinal"),
        ("policy supplies a credential variable name",
         api_document(policy, local=_api_local(
             principals=[{"id": "p1", "credential_env": "MY_VAR"},
                         {"id": "p2"}])),
         "credential_name_supplied"),
        ("policy supplies a secret outright",
         api_document(policy, local=_api_local(
             principals=[{"id": "p1", "secret": "hunter2"}, {"id": "p2"}])),
         "credential_name_supplied"),
        ("role token out of shape",
         api_document(policy, local=_api_local(
             principals=[{"id": "p1", "role": "Owner Of Things"},
                         {"id": "p2"}])),
         "bad_role_token"),
        ("ordinal reused across sections",
         api_document(policy, deployed=_api_deployed(ordinals=("p1", "p4"))),
         "principal_reused_across_sections"),
        ("control character in a label",
         api_document(policy, local=_api_local(operations=[{
             "id": "bad\u202eid", "method": "GET", "path": "/x",
             "kind": "object", "cases": []}])),
         "control_character"),
        ("userinfo in the base url",
         api_document(policy, local=_api_local(
             base_url="http://user:pw@127.0.0.1:8099")),
         "url_userinfo"),
        ("query in the base url",
         api_document(policy, local=_api_local(
             base_url="http://127.0.0.1:8099?x=1")),
         "url_query"),
        ("fragment in the base url",
         api_document(policy, local=_api_local(
             base_url="http://127.0.0.1:8099#f")),
         "url_fragment"),
        ("no scheme in the base url",
         api_document(policy, local=_api_local(base_url="127.0.0.1:8099")),
         "bad_url"),
        ("unsupported local method",
         api_document(policy, local=_api_local(operations=[{
             "id": "o", "method": "TRACE", "path": "/x", "kind": "object",
             "cases": []}])),
         "unsupported_method"),
        ("mutating method in the deployed section",
         api_document(policy, deployed=_api_deployed(operations=[{
             "id": "w", "method": "POST", "path": "/x", "kind": "function",
             "cases": []}])),
         "deployed_method_refused"),
        ("non-https deployed base url",
         api_document(policy, deployed=_api_deployed(
             base_url="http://api.example.org")),
         "scheme_refused"),
        ("deployed base url pointing at loopback",
         api_document(policy, deployed=_api_deployed(
             base_url="https://127.0.0.1:8443")),
         "non_loopback_target"),
        ("secret-shaped literal header value",
         api_document(policy, local=_api_local(
             headers={"X-Trace": "AKIAIOSFODNN7EXAMPLEKEYMATERIAL"})),
         "secret_shaped"),
        ("authorization header named by policy",
         api_document(policy, local=_api_local(
             headers={"Authorization": "anything"})),
         "embedded_credential"),
        ("oversized label",
         api_document(policy, local=_api_local(operations=[{
             "id": "o" * 200, "method": "GET", "path": "/x",
             "kind": "object", "cases": []}])),
         "label_too_long"),
        ("path carrying a query",
         api_document(policy, local=_api_local(operations=[{
             "id": "o", "method": "GET", "path": "/x?y=1", "kind": "object",
             "cases": []}])),
         "bad_url"),
        ("allow case with neither a status nor a property expectation",
         api_document(policy, local=_api_local(operations=[{
             "id": "o", "method": "GET", "path": "/x", "kind": "object",
             "cases": [{"id": "a", "principal": "p1", "expect": "allow"},
                       {"id": "d", "principal": "p2", "expect": "deny",
                        "status": [403]}]}])),
         "bad_expectation"),
        ("collection operation with no foreign identifier",
         api_document(policy, local=_api_local(operations=[{
             "id": "o", "method": "GET", "path": "/x", "kind": "collection",
             "cases": [{"id": "a", "principal": "p1", "expect": "allow",
                        "status": [200]},
                       {"id": "d", "principal": "p2", "expect": "deny",
                        "status": [403]}]}])),
         "missing_key"),
    ]


def test_a2_every_declared_policy_refusal_fires_with_its_own_reason(
    engine, tmp_path
):
    """A2's refusal list, row by row, each pinned to its **reason token**.

    Pinning the reason rather than only the code is what stops this from being
    a test that any refusal satisfies: a schema that refused everything with
    one generic token would pass a code-only assertion and tell an adopter
    nothing about what is wrong with their file.
    """
    policy = submodule(engine, "policy")
    report = submodule(engine, "report")
    observed: list[tuple[str, str]] = []
    for label, document, expected in _api_refusal_rows(policy):
        try:
            policy.parse_policy(
                document, kind=policy.KIND_API, path=tmp_path / "p.json"
            )
        except report.SecurityRefusal as exc:
            observed.append((label, exc.reason))
            assert exc.code == report.E_POLICY_REFUSED, label
            assert exc.reason == expected, f"{label}: {exc.reason}"
        else:
            raise AssertionError(f"{label}: accepted, expected a refusal")
    assert len(observed) == len(_api_refusal_rows(policy))
    # Every reason this schema can produce is a member of the closed vocabulary.
    assert {reason for _label, reason in observed} <= report.REASON_TOKENS


def test_a2_a_symlinked_or_absent_policy_file_refuses(engine, tmp_path):
    policy = submodule(engine, "policy")
    report = submodule(engine, "report")
    real = tmp_path / "real.json"
    real.write_text("{}", encoding="utf-8")
    link = tmp_path / "link.json"
    link.symlink_to(real)
    with pytest.raises(report.SecurityRefusal) as excinfo:
        policy.load_policy(link, kind=policy.KIND_API)
    assert excinfo.value.reason == "policy_symlink"
    with pytest.raises(report.SecurityRefusal) as excinfo:
        policy.load_policy(tmp_path / "absent.json", kind=policy.KIND_API)
    assert excinfo.value.reason == "policy_unreadable"
    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    with pytest.raises(report.SecurityRefusal) as excinfo:
        policy.load_policy(broken, kind=policy.KIND_API)
    assert excinfo.value.reason == "json_malformed"


def test_a2_deletion_mutant_removing_the_denial_requirement(perturbed, tmp_path):
    """Criterion B-1's schema-level guard, mutated: a positive-only matrix is
    accepted, which is the state a fixture that authorizes everything reports
    CLEAN over."""
    engine = perturbed(edits={"policy.py": [(
        '        if "allow" not in expectations or "deny" not in expectations:\n'
        '            _refuse("no_denial_case")\n',
        "",
    )]})
    policy = submodule(engine, "policy")
    document = api_document(policy, local=_api_local(operations=[{
        "id": "o", "method": "GET", "path": "/x", "kind": "object",
        "cases": [{"id": "a", "principal": "p1", "expect": "allow",
                   "status": [200]},
                  {"id": "b", "principal": "p2", "expect": "allow",
                   "status": [200]}]}]))
    parsed = policy.parse_policy(
        document, kind=policy.KIND_API, path=tmp_path / "p.json"
    )
    assert parsed.configured is True


def test_a2_hosting_policy_accepts_a_reviewed_target_and_refuses_bad_ones(
    engine, tmp_path
):
    policy = submodule(engine, "policy")
    report = submodule(engine, "report")
    good = {
        "schema": policy.HOSTING_SCHEMA_ID, "configured": True,
        "local": {"targets": [{
            "id": "site", "http_origin": "http://127.0.0.1:9080",
            "https_origin": "https://localhost:9443",
            "site_type": "browser-app",
            "permitted_redirect_hosts": ["localhost", "127.0.0.1"],
            "expected_csp_directives": ["default-src", "frame-ancestors"],
            "expect_cookies": True,
        }]},
    }
    parsed = policy.parse_policy(
        good, kind=policy.KIND_HOSTING, path=tmp_path / "h.json"
    )
    assert [t["id"] for t in parsed.section("local")["targets"]] == ["site"]

    rows = [
        ("unknown site type",
         {"id": "s", "https_origin": "https://localhost", "site_type": "blog"},
         "bad_site_type"),
        ("http origin declared as https",
         {"id": "s", "https_origin": "https://localhost",
          "http_origin": "https://localhost", "site_type": "static"},
         "scheme_refused"),
        ("https origin that is not https",
         {"id": "s", "https_origin": "http://localhost", "site_type": "static"},
         "scheme_refused"),
        ("csp directive out of shape",
         {"id": "s", "https_origin": "https://localhost", "site_type": "static",
          "expected_csp_directives": ["Default-Src"]},
         "bad_expectation"),
        ("unknown target key",
         {"id": "s", "https_origin": "https://localhost", "site_type": "static",
          "grade": "A+"},
         "unknown_key"),
    ]
    for label, target, expected in rows:
        document = {
            "schema": policy.HOSTING_SCHEMA_ID, "configured": True,
            "local": {"targets": [target]},
        }
        with pytest.raises(report.SecurityRefusal) as excinfo:
            policy.parse_policy(
                document, kind=policy.KIND_HOSTING, path=tmp_path / "h.json"
            )
        assert excinfo.value.reason == expected, label


def test_a2_an_unconfigured_stub_validates_but_stays_unconfigured(
    engine, tmp_path
):
    """``configured: false`` is a valid document, not a malformed one.

    The stub has to parse -- an adopter must be able to install it and get
    INCOMPLETE rather than a schema error -- while an empty matrix under
    ``configured: true`` must refuse.  Criterion E-1/E-2 turn on that pair, and
    this is the schema half of it.
    """
    policy = submodule(engine, "policy")
    document = {
        "schema": policy.API_SCHEMA_ID, "configured": False,
        "local": {"base_url": "http://127.0.0.1:8099", "principals": [],
                  "operations": []},
    }
    parsed = policy.parse_policy(
        document, kind=policy.KIND_API, path=tmp_path / "stub.json"
    )
    assert parsed.configured is False
    assert parsed.section("local")["operations"] == ()


def test_control_and_bidi_sequences_never_survive_scrubbing(engine):
    report = submodule(engine, "report")
    hostile = "safe\x1b[31m\u202ered\x07\u2066x"
    # The ESC byte and both bidi codepoints are gone; "[31m" survives as inert
    # literal text, which is the correct outcome -- a CSI parameter run with no
    # introducer cannot move a cursor or recolour a line.
    assert report.scrub_terminal(hostile) == "safe[31mredx"
    assert "\x1b" not in report.scrub_terminal(hostile)
    assert report.has_control_characters(hostile) is True
    assert report.has_control_characters("plain") is False
