#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""URL normalization, address classification, and one hardened HTTP client.

**Addressing and transport live in the same module on purpose.**  The property
this engine exists to hold is that *the address actually connected to* is
validated, not merely the address that was resolved — and that check has to sit
inside the connect path.  A module seam between "classify" and "connect" is an
invitation to a caller that skips one of them, so there is no such seam here:
:func:`open_validated_connection` resolves, validates every answer, connects,
and verifies the connected peer as one indivisible act, and nothing else in
this package opens a socket.

The properties, each with a named criterion in
``bootstrap/tests/test_security_net.py``:

* **One resolution per connection.**  The DNS answer is taken once and the
  connection is made to a *literal address* from that answer set.  There is no
  second lookup between validation and connection, so there is no window for a
  changed answer to be believed (A-1, A-11).
* **The connected peer is verified against the validated set and the permitted
  address classes.**  A peer outside either is refused and the socket is closed
  before a single application byte is written (A-2).
* **Redirects are never followed.**  A ``3xx`` is classified and returned; the
  caller decides.  Nothing authenticating is carried anywhere, because there is
  nowhere to carry it to (A-3, A-4, A-5).
* **Every read is capped and every wait is bounded** (A-6).
* **TLS is validated through the platform trust store**, with no code path that
  can weaken it: no ``CERT_NONE``, no ``check_hostname = False``, and no policy
  field that reaches either (A-7).

``_RESOLVER`` and ``_SOCKET_FACTORY`` are module attributes so the adversarial
suite can substitute a stub resolver or a socket layer that connects somewhere
other than where it was asked to.  They are the *oracle* for A-1/A-2/A-11 and
they are deliberately **not** used by criterion A-12, which runs the same code
against a real loopback socket with nothing in the transport path substituted.
"""
from __future__ import annotations

import ipaddress
import socket
import ssl
from urllib.parse import urlsplit

from .report import (
    E_MALFORMED_RESPONSE,
    E_POLICY_REFUSED,
    E_REDIRECT_REFUSED,
    E_RESPONSE_CAP,
    E_TIMEOUT,
    E_TLS_REFUSED,
    E_TRANSPORT_FAILED,
    E_PEER_ADDRESS,
    ENGINE_CONTRACT,
    SecurityRefusal,
    has_control_characters,
    sanitize_channel,
)

__all__ = [
    "ENGINE_CONTRACT",
    "ADDRESS_CLASSES",
    "NormalizedUrl",
    "Response",
    "classify_address",
    "normalize_base_url",
    "normalize_host",
    "open_validated_connection",
    "perform_request",
]

# ---------------------------------------------------------------------------
# Caps and timeouts
# ---------------------------------------------------------------------------

CONNECT_TIMEOUT = 5.0
READ_TIMEOUT = 10.0
MAX_REQUEST_BYTES = 65_536
MAX_RESPONSE_BYTES = 262_144
MAX_HEADER_COUNT = 64
MAX_HEADER_LINE = 8_192
MAX_STATUS_LINE = 512
_READ_CHUNK = 8_192

# ---------------------------------------------------------------------------
# Address classification
# ---------------------------------------------------------------------------

ADDRESS_CLASSES = (
    "loopback", "unspecified", "link_local", "multicast", "private",
    "reserved", "public",
)

#: The only classes the agent-facing leg may ever reach.
LOOPBACK_ONLY = frozenset({"loopback"})
#: The only classes the Maintainer-invoked deployed leg may reach.
PUBLIC_ONLY = frozenset({"public"})

_SCHEME_PORTS = {"http": 80, "https": 443}


def canonical_ip(text: object) -> str:
    """Canonical text form of an address, un-mapping IPv4-in-IPv6.

    Un-mapping matters: ``::ffff:127.0.0.1`` and ``127.0.0.1`` are the same
    peer, and a comparison that treats them as different would let a validated
    set be evaded by spelling.
    """
    try:
        ip = ipaddress.ip_address(str(text))
    except ValueError:
        raise SecurityRefusal(E_POLICY_REFUSED, "bad_url") from None
    mapped = getattr(ip, "ipv4_mapped", None)
    if mapped is not None:
        ip = mapped
    return str(ip)


def classify_address(text: object) -> str:
    """Classify an address literal into exactly one of :data:`ADDRESS_CLASSES`.

    Order is load-bearing, because ``ipaddress``' predicates overlap.  IPv4
    loopback and link-local are *also* private, and ``240.0.0.0/4`` is both
    reserved and private — so the narrower classes are tested first.  A
    classifier that checked ``is_private`` early would label ``127.0.0.1``
    "private" and the loopback-only leg would refuse its own fixture.  Nothing
    about *safety* rides on the ordering (every non-permitted class refuses
    identically); what rides on it is whether a class is ever *reported*
    accurately, and an inaccurate class in a finding is a misleading finding.
    """
    try:
        ip = ipaddress.ip_address(canonical_ip(text))
    except SecurityRefusal:
        raise
    if ip.is_loopback:
        return "loopback"
    if ip.is_unspecified:
        return "unspecified"
    if ip.is_link_local:
        return "link_local"
    if ip.is_multicast:
        return "multicast"
    if ip.is_reserved:
        return "reserved"
    if ip.is_private:
        return "private"
    return "public"


def is_address_literal(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return False
    return True


# ---------------------------------------------------------------------------
# URL normalization
# ---------------------------------------------------------------------------


def normalize_host(raw: object) -> str:
    """Lower-case, IDNA-encode, de-bracket and de-dot a host.

    A trailing-dot FQDN and its bare form normalize identically, so a policy
    cannot smuggle a second spelling of the same host past an exact allowlist.
    """
    text = str(raw).strip()
    if not text:
        raise SecurityRefusal(E_POLICY_REFUSED, "host_refused")
    if has_control_characters(text):
        raise SecurityRefusal(E_POLICY_REFUSED, "control_character")
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1]
        return canonical_ip(inner)
    if text.endswith("."):
        text = text[:-1]
    if is_address_literal(text):
        return canonical_ip(text)
    if not text.isascii():
        try:
            text = text.encode("idna").decode("ascii")
        except (UnicodeError, UnicodeDecodeError):
            raise SecurityRefusal(E_POLICY_REFUSED, "host_refused") from None
    text = text.lower()
    if not text or ".." in text or "/" in text or "@" in text:
        raise SecurityRefusal(E_POLICY_REFUSED, "host_refused")
    return text


class NormalizedUrl:
    """A canonical base URL, plus what is known about its address class."""

    __slots__ = ("scheme", "host", "port", "path", "normalized",
                 "address_class")

    def __init__(self, scheme: str, host: str, port: int, path: str) -> None:
        self.scheme = scheme
        self.host = host
        self.port = port
        self.path = path
        default = _SCHEME_PORTS[scheme]
        authority = f"[{host}]" if ":" in host else host
        if port != default:
            authority = f"{authority}:{port}"
        self.normalized = f"{scheme}://{authority}{path}"
        self.address_class = (
            classify_address(host) if is_address_literal(host) else None
        )

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        return f"NormalizedUrl({self.normalized!r})"


def normalize_base_url(raw: object) -> NormalizedUrl:
    """Canonicalize a base URL, refusing every shape a base URL must not have.

    Refused: a missing or non-HTTP(S) scheme, userinfo (an embedded
    credential), a fragment, a query, a control character, and a port outside
    1..65535.  The canonical form has its scheme and host lower-cased, its
    default port stripped, its trailing slash removed and no query or fragment
    — and ``--authorize-base-url`` is compared **byte-for-byte** against that
    canonical string, which is what makes each of criterion B-5's near-misses
    refuse instead of quietly matching.
    """
    text = str(raw).strip()
    if has_control_characters(text):
        raise SecurityRefusal(E_POLICY_REFUSED, "control_character")
    if "://" not in text:
        raise SecurityRefusal(E_POLICY_REFUSED, "bad_url")
    parts = urlsplit(text)
    scheme = parts.scheme.lower()
    if scheme not in _SCHEME_PORTS:
        raise SecurityRefusal(E_POLICY_REFUSED, "scheme_refused")
    if parts.fragment:
        raise SecurityRefusal(E_POLICY_REFUSED, "url_fragment")
    if parts.query:
        raise SecurityRefusal(E_POLICY_REFUSED, "url_query")
    if "@" in parts.netloc:
        raise SecurityRefusal(E_POLICY_REFUSED, "url_userinfo")
    if not parts.hostname:
        raise SecurityRefusal(E_POLICY_REFUSED, "host_refused")
    host = normalize_host(parts.hostname)
    try:
        port = parts.port
    except ValueError:
        raise SecurityRefusal(E_POLICY_REFUSED, "port_refused") from None
    if port is None:
        port = _SCHEME_PORTS[scheme]
    if not 1 <= port <= 65535:
        raise SecurityRefusal(E_POLICY_REFUSED, "port_refused")
    path = parts.path or ""
    if path == "/":
        path = ""
    if path and not path.startswith("/"):
        raise SecurityRefusal(E_POLICY_REFUSED, "bad_url")
    if path.endswith("/"):
        path = path[:-1]
    return NormalizedUrl(scheme, host, port, path)


# ---------------------------------------------------------------------------
# The atomic resolve -> connect -> verify-peer act
# ---------------------------------------------------------------------------

_RESOLVER = socket.getaddrinfo
_SOCKET_FACTORY = socket.socket


class Connection:
    """An open, peer-verified socket and the evidence about how it got there."""

    __slots__ = ("sock", "peer", "validated", "resolutions", "closed")

    def __init__(self, sock, peer: str, validated: tuple[str, ...],
                 resolutions: int) -> None:
        self.sock = sock
        self.peer = peer
        self.validated = validated
        self.resolutions = resolutions
        self.closed = False

    def close(self) -> None:
        if not self.closed:
            self.closed = True
            try:
                self.sock.close()
            except OSError:
                pass


def _close_quietly(sock) -> None:
    try:
        sock.close()
    except OSError:
        pass


def open_validated_connection(
    host: str,
    port: int,
    *,
    allow_classes: frozenset,
    connect_timeout: float = CONNECT_TIMEOUT,
) -> Connection:
    """Resolve once, validate every answer, connect, verify the peer.

    Indivisible by construction.  A caller cannot obtain a socket from this
    module without the peer check having run, because the socket only leaves
    this function after it.
    """
    resolutions = 0
    try:
        answers = _RESOLVER(host, port, 0, socket.SOCK_STREAM)
        resolutions += 1
    except OSError:
        raise SecurityRefusal(E_POLICY_REFUSED, "resolution_failed") from None
    if not answers:
        raise SecurityRefusal(E_POLICY_REFUSED, "no_usable_address")

    validated: list[tuple[int, tuple, str]] = []
    for entry in answers:
        family, _socktype, _proto, _canon, sockaddr = entry
        address = canonical_ip(sockaddr[0])
        # Refuse the WHOLE answer set when any member is out of class.  A
        # filter that merely skipped the bad members would accept a hostname
        # whose answer set mixes public and private addresses, which is
        # exactly criterion A-3's mixed-answer row.
        if classify_address(address) not in allow_classes:
            raise SecurityRefusal(E_POLICY_REFUSED, "address_class_refused")
        validated.append((family, sockaddr, address))

    validated_addresses = tuple(entry[2] for entry in validated)
    last_error: str | None = None
    for family, sockaddr, _address in validated:
        try:
            sock = _SOCKET_FACTORY(family, socket.SOCK_STREAM)
        except OSError:
            last_error = "connection_failed"
            continue
        try:
            sock.settimeout(connect_timeout)
            sock.connect(sockaddr)
        except (TimeoutError, socket.timeout):
            _close_quietly(sock)
            raise SecurityRefusal(E_TIMEOUT, "connect_timeout") from None
        except OSError:
            _close_quietly(sock)
            last_error = "connection_failed"
            continue

        # --- post-connect peer verification (A-1/A-2/A-11 deletion mutant) ---
        try:
            peer = canonical_ip(sock.getpeername()[0])
        except (OSError, IndexError, SecurityRefusal):
            _close_quietly(sock)
            raise SecurityRefusal(E_PEER_ADDRESS, "peer_not_validated") from None
        if peer not in validated_addresses:
            _close_quietly(sock)
            raise SecurityRefusal(E_PEER_ADDRESS, "peer_not_validated")
        if classify_address(peer) not in allow_classes:
            _close_quietly(sock)
            raise SecurityRefusal(E_PEER_ADDRESS, "peer_class_refused")
        # --- end post-connect peer verification ---

        return Connection(sock, peer, validated_addresses, resolutions)

    raise SecurityRefusal(E_TRANSPORT_FAILED, last_error or "connection_failed")


# ---------------------------------------------------------------------------
# TLS
# ---------------------------------------------------------------------------

#: OpenSSL verification codes mapped to fixed reason tokens.  The *code* is
#: read; the human-readable verification message never is, so a peer cannot
#: choose text that reaches an output channel.
_VERIFY_REASONS = {
    10: "tls_expired",           # X509_V_ERR_CERT_HAS_EXPIRED
    18: "tls_chain_untrusted",   # DEPTH_ZERO_SELF_SIGNED_CERT
    19: "tls_chain_untrusted",   # SELF_SIGNED_CERT_IN_CHAIN
    20: "tls_chain_untrusted",   # UNABLE_TO_GET_ISSUER_CERT_LOCALLY
    21: "tls_chain_untrusted",   # UNABLE_TO_VERIFY_LEAF_SIGNATURE
    62: "tls_hostname_mismatch",  # HOSTNAME_MISMATCH
}


def tls_context() -> ssl.SSLContext:
    """A default-verifying context over the platform trust store.

    There is no argument, policy field, environment override or CLI flag in
    this engine that reaches ``verify_mode`` or ``check_hostname``.  Criterion
    A-7's deletion mutant is to set ``CERT_NONE`` here, and all four TLS rows
    must go red when it is set.
    """
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    return context


def _wrap_tls(sock, hostname: str):
    context = tls_context()
    try:
        return context.wrap_socket(sock, server_hostname=hostname)
    except ssl.SSLCertVerificationError as exc:
        _close_quietly(sock)
        reason = _VERIFY_REASONS.get(
            getattr(exc, "verify_code", None), "tls_chain_untrusted"
        )
        raise SecurityRefusal(E_TLS_REFUSED, reason) from None
    except (ssl.SSLZeroReturnError, ssl.SSLEOFError):
        _close_quietly(sock)
        raise SecurityRefusal(E_TLS_REFUSED, "tls_handshake_failed") from None
    except ssl.SSLError:
        _close_quietly(sock)
        raise SecurityRefusal(E_TLS_REFUSED, "tls_protocol") from None
    except (TimeoutError, socket.timeout):
        _close_quietly(sock)
        raise SecurityRefusal(E_TIMEOUT, "connect_timeout") from None
    except OSError:
        _close_quietly(sock)
        raise SecurityRefusal(E_TLS_REFUSED, "tls_handshake_failed") from None


# ---------------------------------------------------------------------------
# One request, one socket, no redirect
# ---------------------------------------------------------------------------


class Response:
    """What a single request observed, already stripped of observed content.

    ``reason_withheld``, ``redirect_withheld`` and ``header_tokens`` are *tokens*:
    the peer-supplied reason phrase, ``Location`` value and header values went
    through :func:`~._security_net.report.sanitize_channel` on the way in and
    their content is not retained here.  ``headers`` keeps header *names* and
    the structured facts the checks need (a directive token, a cookie
    attribute's presence), never a raw value.
    """

    __slots__ = ("status", "reason_withheld", "headers", "header_names", "body",
                 "peer", "local_port", "redirect_withheld", "redirect_host",
                 "redirect_scheme", "resolutions", "tls")

    def __init__(self) -> None:
        self.status = 0
        self.reason_withheld = ""
        self.headers: list[tuple[str, str]] = []
        self.header_names: tuple[str, ...] = ()
        self.body = b""
        self.peer = ""
        self.local_port = 0
        self.redirect_withheld = ""
        self.redirect_host: str | None = None
        self.redirect_scheme: str | None = None
        self.resolutions = 0
        self.tls = False

    def header(self, name: str) -> str | None:
        """First value for ``name``, case-insensitively.

        The *value* is returned to the checks, which reduce it to a token from
        the reviewed expectation set before anything is reported.  Nothing here
        writes to an output channel.
        """
        lowered = name.lower()
        for key, value in self.headers:
            if key.lower() == lowered:
                return value
        return None

    def header_all(self, name: str) -> tuple[str, ...]:
        lowered = name.lower()
        return tuple(v for k, v in self.headers if k.lower() == lowered)

    @property
    def is_redirect(self) -> bool:
        return 300 <= self.status < 400


def _readline(sock, limit: int, buffer: bytearray) -> bytes:
    """Read one CRLF-terminated line, refusing past ``limit`` bytes."""
    while b"\r\n" not in buffer:
        if len(buffer) > limit:
            raise SecurityRefusal(E_RESPONSE_CAP, "header_length_cap")
        try:
            chunk = sock.recv(_READ_CHUNK)
        except (TimeoutError, socket.timeout):
            raise SecurityRefusal(E_TIMEOUT, "read_timeout") from None
        except ssl.SSLError:
            raise SecurityRefusal(E_TLS_REFUSED, "tls_protocol") from None
        except OSError:
            raise SecurityRefusal(E_TRANSPORT_FAILED, "connection_failed") from None
        if not chunk:
            raise SecurityRefusal(E_MALFORMED_RESPONSE, "status_line_malformed")
        buffer.extend(chunk)
    index = buffer.index(b"\r\n")
    line = bytes(buffer[:index])
    del buffer[: index + 2]
    if len(line) > limit:
        raise SecurityRefusal(E_RESPONSE_CAP, "header_length_cap")
    return line


def _read_exactly(sock, want: int, buffer: bytearray, cap: int) -> bytes:
    while len(buffer) < want:
        if len(buffer) > cap:
            raise SecurityRefusal(E_RESPONSE_CAP, "body_cap")
        try:
            chunk = sock.recv(_READ_CHUNK)
        except (TimeoutError, socket.timeout):
            raise SecurityRefusal(E_TIMEOUT, "read_timeout") from None
        except ssl.SSLError:
            raise SecurityRefusal(E_TLS_REFUSED, "tls_protocol") from None
        except OSError:
            raise SecurityRefusal(E_TRANSPORT_FAILED, "connection_failed") from None
        if not chunk:
            break
        buffer.extend(chunk)
    out = bytes(buffer[:want])
    del buffer[:want]
    return out


def _read_chunked(sock, buffer: bytearray, cap: int) -> bytes:
    body = bytearray()
    while True:
        line = _readline(sock, MAX_HEADER_LINE, buffer)
        token = line.split(b";", 1)[0].strip()
        try:
            size = int(token, 16)
        except ValueError:
            raise SecurityRefusal(
                E_MALFORMED_RESPONSE, "encoding_malformed"
            ) from None
        if size < 0:
            raise SecurityRefusal(E_MALFORMED_RESPONSE, "encoding_malformed")
        if size == 0:
            break
        if len(body) + size > cap:
            raise SecurityRefusal(E_RESPONSE_CAP, "body_cap")
        body.extend(_read_exactly(sock, size, buffer, cap))
        trailer = _read_exactly(sock, 2, buffer, cap)
        if trailer != b"\r\n":
            raise SecurityRefusal(E_MALFORMED_RESPONSE, "encoding_malformed")
    return bytes(body)


def _read_to_close(sock, buffer: bytearray, cap: int) -> bytes:
    body = bytearray(buffer)
    buffer.clear()
    while True:
        if len(body) > cap:
            raise SecurityRefusal(E_RESPONSE_CAP, "body_cap")
        try:
            chunk = sock.recv(_READ_CHUNK)
        except (TimeoutError, socket.timeout):
            raise SecurityRefusal(E_TIMEOUT, "read_timeout") from None
        except ssl.SSLError:
            raise SecurityRefusal(E_TLS_REFUSED, "tls_protocol") from None
        except OSError:
            raise SecurityRefusal(E_TRANSPORT_FAILED, "connection_failed") from None
        if not chunk:
            break
        body.extend(chunk)
    if len(body) > cap:
        raise SecurityRefusal(E_RESPONSE_CAP, "body_cap")
    return bytes(body)


def _build_request(
    method: str, target: str, host_header: str,
    headers: tuple[tuple[str, str], ...], body: bytes,
) -> bytes:
    lines = [f"{method} {target} HTTP/1.1", f"Host: {host_header}"]
    for name, value in headers:
        lines.append(f"{name}: {value}")
    # One connection per request, never reused across targets.  Sent
    # explicitly so the peer cannot keep the socket open and be handed a
    # second, differently-validated request on it (criterion A-5).
    lines.append("Connection: close")
    if body:
        lines.append(f"Content-Length: {len(body)}")
    try:
        head = ("\r\n".join(lines) + "\r\n\r\n").encode("ascii", "strict")
    except UnicodeEncodeError:
        # A non-ASCII header name, header value, or credential.  Refused with a
        # fixed code rather than allowed to escape as a UnicodeEncodeError,
        # whose message would carry the offending bytes -- and for a credential
        # that message is the credential.  This is the one place a raw
        # exception could have leaked a secret, so it is closed here.
        raise SecurityRefusal(E_POLICY_REFUSED, "header_malformed") from None
    raw = head + body
    if len(raw) > MAX_REQUEST_BYTES:
        raise SecurityRefusal(E_POLICY_REFUSED, "body_cap")
    return raw


def perform_request(
    url: NormalizedUrl,
    *,
    method: str,
    path: str = "",
    allow_classes: frozenset,
    headers: tuple[tuple[str, str], ...] = (),
    credential: str | None = None,
    body: bytes = b"",
    connect_timeout: float = CONNECT_TIMEOUT,
    read_timeout: float = READ_TIMEOUT,
    max_response_bytes: int = MAX_RESPONSE_BYTES,
) -> Response:
    """Perform exactly one request on exactly one freshly validated socket.

    No redirect is followed and no socket is reused.  ``credential``, if given,
    becomes the ``Authorization`` header value on **this** request only; since
    a ``3xx`` terminates the call, there is no second request for it to be
    carried to (criterion A-4).
    """
    if method not in ("GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"):
        raise SecurityRefusal(E_POLICY_REFUSED, "unsupported_method")
    target = (url.path + path) or "/"
    if not target.startswith("/") or has_control_characters(target):
        raise SecurityRefusal(E_POLICY_REFUSED, "bad_url")

    default = _SCHEME_PORTS[url.scheme]
    host_header = f"[{url.host}]" if ":" in url.host else url.host
    if url.port != default:
        host_header = f"{host_header}:{url.port}"

    sent_headers = list(headers)
    if credential is not None:
        sent_headers.append(("Authorization", credential))
    raw = _build_request(method, target, host_header, tuple(sent_headers), body)

    connection = open_validated_connection(
        url.host, url.port,
        allow_classes=allow_classes,
        connect_timeout=connect_timeout,
    )
    sock = connection.sock
    try:
        local_port = int(sock.getsockname()[1])
    except (OSError, IndexError, ValueError):
        local_port = 0
    if url.scheme == "https":
        sock = _wrap_tls(sock, url.host)
        connection.sock = sock
    try:
        sock.settimeout(read_timeout)
        try:
            sock.sendall(raw)
        except (TimeoutError, socket.timeout):
            raise SecurityRefusal(E_TIMEOUT, "read_timeout") from None
        except ssl.SSLError:
            raise SecurityRefusal(E_TLS_REFUSED, "tls_protocol") from None
        except OSError:
            raise SecurityRefusal(
                E_TRANSPORT_FAILED, "connection_failed"
            ) from None
        response = _read_response(
            sock, method=method, max_response_bytes=max_response_bytes
        )
    finally:
        connection.close()

    response.peer = connection.peer
    response.local_port = local_port
    response.resolutions = connection.resolutions
    response.tls = url.scheme == "https"
    return response


def _read_response(sock, *, method: str, max_response_bytes: int) -> Response:
    buffer = bytearray()
    response = Response()

    status_line = _readline(sock, MAX_STATUS_LINE, buffer)
    try:
        text = status_line.decode("iso-8859-1")
    except UnicodeDecodeError:  # pragma: no cover - iso-8859-1 never fails
        raise SecurityRefusal(
            E_MALFORMED_RESPONSE, "status_line_malformed"
        ) from None
    pieces = text.split(" ", 2)
    if len(pieces) < 2 or not pieces[0].startswith("HTTP/"):
        raise SecurityRefusal(E_MALFORMED_RESPONSE, "status_line_malformed")
    try:
        response.status = int(pieces[1])
    except ValueError:
        raise SecurityRefusal(
            E_MALFORMED_RESPONSE, "status_line_malformed"
        ) from None
    if not 100 <= response.status <= 599:
        raise SecurityRefusal(E_MALFORMED_RESPONSE, "status_line_malformed")
    # The reason phrase is peer-supplied text.  It is reduced to a fixed token
    # here, at the boundary, and its content is never retained.
    response.reason_withheld = sanitize_channel(
        "reason_phrase", pieces[2] if len(pieces) > 2 else ""
    )

    headers: list[tuple[str, str]] = []
    while True:
        line = _readline(sock, MAX_HEADER_LINE, buffer)
        if not line:
            break
        if len(headers) >= MAX_HEADER_COUNT:
            raise SecurityRefusal(E_RESPONSE_CAP, "header_count_cap")
        try:
            decoded = line.decode("iso-8859-1")
        except UnicodeDecodeError:  # pragma: no cover
            raise SecurityRefusal(
                E_MALFORMED_RESPONSE, "header_malformed"
            ) from None
        if ":" not in decoded:
            raise SecurityRefusal(E_MALFORMED_RESPONSE, "header_malformed")
        name, _, value = decoded.partition(":")
        name = name.strip()
        if not name:
            raise SecurityRefusal(E_MALFORMED_RESPONSE, "header_malformed")
        headers.append((name, value.strip()))
    response.headers = headers
    response.header_names = tuple(sorted({n.lower() for n, _ in headers}))

    if response.is_redirect:
        location = response.header("Location") or ""
        response.redirect_withheld = sanitize_channel("redirect_location", location)
        response.redirect_host, response.redirect_scheme = _redirect_authority(
            location
        )

    if method == "HEAD" or response.status in (204, 304):
        response.body = b""
        return response

    length = response.header("Content-Length")
    encoding = (response.header("Transfer-Encoding") or "").lower()
    if "chunked" in encoding:
        response.body = _read_chunked(sock, buffer, max_response_bytes)
    elif length is not None:
        try:
            want = int(length.strip())
        except ValueError:
            raise SecurityRefusal(
                E_MALFORMED_RESPONSE, "header_malformed"
            ) from None
        if want < 0:
            raise SecurityRefusal(E_MALFORMED_RESPONSE, "header_malformed")
        if want > max_response_bytes:
            raise SecurityRefusal(E_RESPONSE_CAP, "body_cap")
        response.body = _read_exactly(sock, want, buffer, max_response_bytes)
        if len(response.body) < want:
            raise SecurityRefusal(E_MALFORMED_RESPONSE, "encoding_malformed")
    else:
        response.body = _read_to_close(sock, buffer, max_response_bytes)
    return response


def _redirect_authority(location: str) -> tuple[str | None, str | None]:
    """Extract the host and scheme of a ``Location`` without resolving it.

    Returning ``(None, None)`` means the redirect is same-origin relative; the
    caller still refuses to follow it, and the distinction only decides which
    fixed reason token the refusal carries.
    """
    text = str(location).strip()
    if not text or has_control_characters(text):
        return None, None
    if "://" not in text:
        return None, None
    try:
        parts = urlsplit(text)
        if not parts.hostname:
            return None, None
        return normalize_host(parts.hostname), (parts.scheme or "").lower()
    except SecurityRefusal:
        return None, None


def classify_redirect(
    response: Response,
    *,
    allow_classes: frozenset,
    permitted_hosts: tuple[str, ...] = (),
) -> SecurityRefusal:
    """Return the refusal a ``3xx`` earns.  A redirect is never followed.

    Order is deliberate: a host outside the exact allowlist is refused
    **without a DNS lookup**, so an attacker-chosen ``Location`` cannot turn
    this engine into a resolver for a name of their choosing.  Only a host the
    policy already permits is resolved, and only to classify it.
    """
    host = response.redirect_host
    if host is None:
        return SecurityRefusal(E_REDIRECT_REFUSED, "redirect_not_followed")
    if permitted_hosts and host not in permitted_hosts:
        return SecurityRefusal(E_REDIRECT_REFUSED, "redirect_host_refused")
    if is_address_literal(host):
        if classify_address(host) not in allow_classes:
            return SecurityRefusal(E_REDIRECT_REFUSED, "redirect_host_refused")
        return SecurityRefusal(E_REDIRECT_REFUSED, "redirect_not_followed")
    if not permitted_hosts:
        return SecurityRefusal(E_REDIRECT_REFUSED, "redirect_host_refused")
    try:
        answers = _RESOLVER(host, None, 0, socket.SOCK_STREAM)
    except OSError:
        return SecurityRefusal(E_REDIRECT_REFUSED, "redirect_host_refused")
    for entry in answers:
        if classify_address(entry[4][0]) not in allow_classes:
            return SecurityRefusal(E_REDIRECT_REFUSED, "redirect_host_refused")
    return SecurityRefusal(E_REDIRECT_REFUSED, "redirect_not_followed")
