#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Sanitized output layer for the shared security-network engine.

This module is the **only** place a peer-supplied byte is allowed to be turned
into something a human or a machine reads, and its whole job is to refuse to do
that.  Three properties it exists to hold, each of which has a named test in
``bootstrap/tests/test_security_net.py`` or
``bootstrap/tests/test_security_finding_confidentiality.py``:

1. **No observed content crosses any channel.**  There is no ``str(exc)``, no
   ``repr``, no traceback, no peer-supplied reason phrase, no certificate
   string, no response header, no cookie, no redirect URL and no body fragment
   in any output this module produces.  Every diagnostic is a **fixed token**
   drawn from a closed vocabulary declared here.
2. **No exact value-derived cardinality crosses any channel.**  A finding never
   carries a byte length, a character length, a member count or an index.  It
   carries a five-value :func:`magnitude_bucket` instead, chosen so that
   formatted national IDs, phone numbers, dates, ordinary names and most email
   addresses all collapse into ``short`` and therefore carry no width signal.
   Structurally: **a finding contains no integer value at all**, which closes
   the cardinality question as a *class* rather than field by field.
3. **Evidence cannot land in a commit.**  The report is written into a freshly
   created private temporary directory verified to resolve outside the
   repository.

Deliberately absent, because each is an authority this engine must not have:
no environment override, no plugin path, no verbosity switch that widens output,
and no way to reach the raw value of anything observed.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import shutil
import tempfile
from pathlib import Path

#: Engine contract version.  Every engine member declares it and
#: ``verify_engine_complete()`` refuses a package whose members disagree.
ENGINE_CONTRACT = "1"

# ---------------------------------------------------------------------------
# Fixed error-code enumeration
# ---------------------------------------------------------------------------
# Every refusal in this engine names one of these.  They are the *complete*
# vocabulary: nothing derived from a peer, an exception, or a policy value ever
# becomes a code.
#
# E_POLICY_REFUSED and E_CREDENTIAL_ABSENT are two DISTINCT codes on purpose.
# Criterion A-8(c) is "every refusal precedes any credential lookup", and that
# is only observable from outside the process if a policy/target/actor refusal
# and an absent-credential outcome report differently.  Collapsing them would
# make the ordering claim unfalsifiable.

E_POLICY_REFUSED = "policy_refused"
E_CREDENTIAL_ABSENT = "credential_absent"
E_PEER_ADDRESS = "peer_address_refused"
E_REDIRECT_REFUSED = "redirect_refused"
E_TLS_REFUSED = "tls_refused"
E_RESPONSE_CAP = "response_cap_exceeded"
E_TIMEOUT = "timeout"
E_MALFORMED_RESPONSE = "malformed_response"
E_TRANSPORT_FAILED = "transport_failed"
E_REPORT_DIR_REFUSED = "report_dir_refused"
E_ENGINE_INCOMPLETE = "engine_incomplete"
E_RANDOMNESS_UNAVAILABLE = "randomness_unavailable"
E_INVENTORY_REFUSED = "inventory_refused"

ERROR_CODES = frozenset({
    E_POLICY_REFUSED,
    E_CREDENTIAL_ABSENT,
    E_PEER_ADDRESS,
    E_REDIRECT_REFUSED,
    E_TLS_REFUSED,
    E_RESPONSE_CAP,
    E_TIMEOUT,
    E_MALFORMED_RESPONSE,
    E_TRANSPORT_FAILED,
    E_REPORT_DIR_REFUSED,
    E_ENGINE_INCOMPLETE,
    E_RANDOMNESS_UNAVAILABLE,
    E_INVENTORY_REFUSED,
})

# ---------------------------------------------------------------------------
# Fixed reason vocabulary
# ---------------------------------------------------------------------------
# A refusal may carry ONE reason token beside its code, to make a refusal
# actionable without describing what was observed.  Closed set; a token outside
# it is a programming error and is replaced by ``unspecified``.

REASON_TOKENS = frozenset({
    "unspecified",
    # policy / schema
    "unknown_key", "missing_key", "duplicate_id", "bad_type", "empty_section",
    "unsupported_method", "bad_url", "url_userinfo", "url_fragment",
    "url_query", "control_character", "embedded_credential", "secret_shaped",
    "bad_principal_ordinal", "principal_reused_across_sections",
    "credential_name_supplied", "bad_role_token", "not_configured",
    "no_denial_case", "no_operations", "no_targets", "bad_site_type",
    "bad_expectation", "label_too_long", "bad_schema_id",
    "policy_unreadable", "policy_not_regular_file", "policy_symlink",
    # target / actor
    "address_class_refused", "authorization_mismatch", "scheme_refused",
    "port_refused", "host_refused", "deployed_method_refused",
    "non_loopback_target", "resolution_failed", "no_usable_address",
    # transport
    "peer_not_validated", "peer_class_refused", "redirect_not_followed",
    "redirect_host_refused", "header_count_cap", "header_length_cap",
    "body_cap", "status_line_malformed", "header_malformed",
    "encoding_malformed", "json_malformed", "connect_timeout", "read_timeout",
    "connection_failed", "tls_handshake_failed", "tls_hostname_mismatch",
    "tls_chain_untrusted", "tls_expired", "tls_protocol",
    # report / engine
    "inside_repository", "symlink_component", "tempdir_unavailable",
    "report_exists", "report_unwritable", "member_absent",
    "contract_disagreement", "randomness_failed",
    # inventory
    "inventory_unreadable", "inventory_malformed",
})


class SecurityRefusal(Exception):
    """A refusal carrying a fixed code and one fixed reason token.

    The exception message is built from the closed vocabularies above and never
    from an observed value, so it is safe to print.  Nothing in this engine
    raises a refusal whose text is derived from a peer, a policy value, or
    another exception's ``str()``.
    """

    def __init__(self, code: str, reason: str = "unspecified") -> None:
        if code not in ERROR_CODES:
            code = E_TRANSPORT_FAILED
        if reason not in REASON_TOKENS:
            reason = "unspecified"
        self.code = code
        self.reason = reason
        super().__init__(f"{code}:{reason}")


# ``EngineIncomplete`` deliberately does NOT live here.  This module is one of
# the members that can be missing from a partial install, so the exception
# raised when it is missing has to be defined somewhere that is present by
# construction: the package's ``__init__.py``.  It carries the same
# ``code`` / ``reason`` pair as ``SecurityRefusal`` so the facades' refusal
# handler treats both uniformly.

# ---------------------------------------------------------------------------
# Aggregate results and process exits
# ---------------------------------------------------------------------------

RESULT_CLEAN = "CLEAN"
RESULT_FINDINGS = "FINDINGS"
RESULT_INCOMPLETE = "INCOMPLETE"
RESULT_DEGRADED = "DEGRADED"
RESULT_NOT_APPLICABLE = "NOT_APPLICABLE"

RESULTS = (
    RESULT_CLEAN, RESULT_FINDINGS, RESULT_INCOMPLETE,
    RESULT_DEGRADED, RESULT_NOT_APPLICABLE,
)

EXIT_FOR_RESULT = {
    RESULT_CLEAN: 0,
    RESULT_NOT_APPLICABLE: 0,
    RESULT_INCOMPLETE: 5,
    RESULT_FINDINGS: 10,
    RESULT_DEGRADED: 20,
}

#: Fixed prefix of the single human-readable result line.  A fixture-supplied
#: string shaped like this must never reach stdout; since no observed content
#: reaches stdout at all, that holds by construction and D-6 asserts it.
RESULT_LINE_PREFIX = "cairn-security-result:"

# ---------------------------------------------------------------------------
# Channel tokens — the value-omission seam
# ---------------------------------------------------------------------------
# Every peer-supplied or policy-supplied string that a diagnostic would like to
# quote goes through sanitize_channel(), which returns a FIXED token naming the
# channel rather than its content.  This is the single seam criterion D-1
# deletes to prove the confidentiality sweep is not decoration, and the seam
# criterion D-2 suppresses one channel at a time to prove each channel is
# actually reached by the runner.

CHANNEL_TOKENS = {
    "reason_phrase": "<reason-phrase-withheld>",
    "redirect_location": "<redirect-location-withheld>",
    "certificate_subject": "<certificate-subject-withheld>",
    "exception_text": "<exception-text-withheld>",
    "timeout_diagnostic": "<timeout-diagnostic-withheld>",
    "response_header": "<response-header-withheld>",
    "set_cookie": "<cookie-withheld>",
    "response_body": "<response-body-withheld>",
    "request_body": "<request-body-withheld>",
    "policy_label": "<policy-label-withheld>",
    "credential": "<credential-withheld>",
    "json_pointer_value": "<property-value-withheld>",
    "collection_member": "<collection-member-withheld>",
}

#: **Empty in shipped source, and structurally inert.**  Nothing in this engine
#: writes to it: no environment variable, no policy field, no CLI flag and no
#: import hook can populate it, and
#: ``test_security_net.py::test_channel_passthrough_is_empty_in_shipped_source``
#: asserts it stays empty.  It exists so criterion D-2's per-channel *liveness*
#: phase can be executed as a genuine one-line source mutation applied to a
#: throwaway copy of this engine — the alternative being to assert
#: confidentiality over a channel the runner may never reach, which proves
#: nothing.  See D-2 in ``dev/plans/api-web-security-modules.md``.
_CHANNEL_PASSTHROUGH: frozenset = frozenset()


def sanitize_channel(channel: str, raw: object) -> str:
    """Return a fixed token for ``channel``, never ``raw``'s content."""
    if channel in _CHANNEL_PASSTHROUGH:
        return scrub_terminal(str(raw))
    return CHANNEL_TOKENS.get(channel, "<withheld>")


# ---------------------------------------------------------------------------
# Terminal integrity
# ---------------------------------------------------------------------------

#: Bidi and other directional-override codepoints, plus the interlinear
#: annotation set.  These do not print as themselves and can reorder a line.
#:
#: **Written as escapes, not as literals, deliberately.**  Spelling them
#: literally makes this very file a Trojan-Source carrier -- Bandit's ``B613``
#: reports exactly that, at HIGH, and it is right to: a reviewer reading the
#: source would see reordered text.  The set is identical either way; only the
#: file's own readability differs, and a security module that cannot be read
#: safely is not one that can be reviewed.
_BIDI = frozenset(
    # LRE, RLE, PDF, LRO, RLO
    "\u202a\u202b\u202c\u202d\u202e"
    # LRI, RLI, FSI, PDI
    "\u2066\u2067\u2068\u2069"
    # LRM, RLM, ALM
    "\u200e\u200f\u061c"
    # interlinear annotation anchor / separator / terminator
    "\ufff9\ufffa\ufffb"
)


def scrub_terminal(text: str) -> str:
    """Drop every control, escape and bidi codepoint from ``text``.

    Used on the few strings this engine emits that come from a *closed
    vocabulary* but are assembled dynamically (a fixed token joined to another
    fixed token).  It is defence in depth, not the primary control: the primary
    control is that observed content never reaches an output channel at all.
    """
    out = []
    for ch in str(text):
        if ch in _BIDI:
            continue
        code = ord(ch)
        if code < 0x20 or code == 0x7F:
            continue
        if 0x80 <= code <= 0x9F:
            continue
        out.append(ch)
    return "".join(out)


def has_control_characters(text: str) -> bool:
    """True when ``text`` carries a control, escape or bidi codepoint."""
    return scrub_terminal(text) != str(text)


# ---------------------------------------------------------------------------
# Magnitude buckets
# ---------------------------------------------------------------------------

MAGNITUDE_BUCKETS = ("empty", "short", "medium", "large", "oversized")

#: Byte/character thresholds.  ``short`` is deliberately wide enough that a
#: formatted national ID, a phone number, an ISO date, an ordinary personal
#: name and most email addresses are indistinguishable inside it.
_BYTE_THRESHOLDS = (0, 64, 1024, 65536)
#: Member-count thresholds for a collection.
_COUNT_THRESHOLDS = (0, 4, 32, 512)


def magnitude_bucket(size: int, kind: str = "bytes") -> str:
    """Map a size to one of five buckets.  The size itself is discarded."""
    thresholds = _COUNT_THRESHOLDS if kind == "count" else _BYTE_THRESHOLDS
    n = int(size)
    if n <= thresholds[0]:
        return "empty"
    if n <= thresholds[1]:
        return "short"
    if n <= thresholds[2]:
        return "medium"
    if n <= thresholds[3]:
        return "large"
    return "oversized"


def value_magnitude(value: object) -> str:
    """Bucket an observed scalar or collection without recording its size."""
    if value is None:
        return "empty"
    if isinstance(value, (list, tuple, set, frozenset, dict)):
        return magnitude_bucket(len(value), "count")
    if isinstance(value, bytes):
        return magnitude_bucket(len(value), "bytes")
    if isinstance(value, bool):
        return "short"
    return magnitude_bucket(len(str(value).encode("utf-8", "replace")), "bytes")


# ---------------------------------------------------------------------------
# Ephemeral keyed fingerprint
# ---------------------------------------------------------------------------


class Fingerprinter:
    """HMAC-SHA-256 under a per-run key that is never printed or persisted.

    Two equal observations fingerprint equally *within one run*, which is what
    makes a report readable.  Across runs the key differs, so a pasted report
    cannot be dictionary-tested back to the value it fingerprints — which is
    why this replaced the salted digest the proposal started with.
    """

    #: Hex characters retained.  Enough to correlate within a run, far short of
    #: a value-recovery oracle.
    WIDTH = 16

    def __init__(self, key: bytes | None = None) -> None:
        if key is None:
            try:
                key = secrets.token_bytes(32)
            except Exception:  # pragma: no cover - platform randomness failure
                raise SecurityRefusal(
                    E_RANDOMNESS_UNAVAILABLE, "randomness_failed"
                ) from None
        if not key or len(key) < 32:
            raise SecurityRefusal(E_RANDOMNESS_UNAVAILABLE, "randomness_failed")
        self._key = key

    def fingerprint(self, value: object) -> str:
        material = value if isinstance(value, bytes) else str(value).encode(
            "utf-8", "replace"
        )
        digest = hmac.new(self._key, material, hashlib.sha256).hexdigest()
        return digest[: self.WIDTH]


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------

#: The complete key vocabulary of a finding.  A key outside this set is a
#: programming error; criterion D-5 asserts the parsed report honours it.
FINDING_KEYS = frozenset({
    "check_id", "target_id", "operation_id", "case_id", "assertion_id",
    "principal_ids", "method", "status_class", "observation",
    "observed_magnitude", "observation_fingerprint", "detail",
})

#: Observation verdicts a hosting check may report.
OBSERVATION_STATES = ("present", "missing", "invalid", "unexpected")


def status_class(status: object) -> str:
    """Reduce a status code to its class.  ``403`` and ``404`` both become 4xx."""
    try:
        n = int(status)
    except (TypeError, ValueError):
        return "unknown"
    if 100 <= n <= 599:
        return f"{n // 100}xx"
    return "unknown"


def build_finding(
    *,
    check_id: str,
    detail: str,
    target_id: str | None = None,
    operation_id: str | None = None,
    case_id: str | None = None,
    assertion_id: str | None = None,
    principal_ids: tuple[str, ...] = (),
    method: str | None = None,
    status: object = None,
    observation: str | None = None,
    observed_value: object = None,
    fingerprinter: "Fingerprinter | None" = None,
) -> dict:
    """Assemble one finding, dropping every observed value on the way in.

    ``observed_value`` is consumed and **never stored**: only its five-value
    bucket, and optionally an ephemeral keyed fingerprint, survive this call.
    Deleting the two lines that do that is criterion D-1's deletion mutant, and
    the confidentiality sweep must go red when they are gone.
    """
    finding: dict = {"check_id": scrub_terminal(check_id)}
    if target_id is not None:
        finding["target_id"] = scrub_terminal(target_id)
    if operation_id is not None:
        finding["operation_id"] = scrub_terminal(operation_id)
    if case_id is not None:
        finding["case_id"] = scrub_terminal(case_id)
    if assertion_id is not None:
        finding["assertion_id"] = scrub_terminal(assertion_id)
    if principal_ids:
        finding["principal_ids"] = [scrub_terminal(p) for p in principal_ids]
    if method is not None:
        finding["method"] = scrub_terminal(method)
    if status is not None:
        finding["status_class"] = status_class(status)
    if observation is not None:
        finding["observation"] = scrub_terminal(observation)
    if observed_value is not None:
        # --- the value-omission step (D-1's deletion mutant target) ---
        finding["observed_magnitude"] = value_magnitude(observed_value)
        if fingerprinter is not None:
            finding["observation_fingerprint"] = fingerprinter.fingerprint(
                observed_value
            )
        # --- end value-omission step ---
    finding["detail"] = scrub_terminal(detail)
    return finding


# ---------------------------------------------------------------------------
# Off-tree report
# ---------------------------------------------------------------------------

REPORT_BASENAME = "report.json"
_REPORT_PREFIX = "cairn-security-"


def create_report_dir(repo_root: object) -> Path:
    """Create a private directory that provably resolves outside ``repo_root``.

    Refusal here precedes every network and credential act in both facades, so
    a hostile ``TMPDIR`` cannot be used to make the runner do work first and
    fail later.  Four hostile shapes are refused and each has a row in
    criterion A-9: a ``TMPDIR`` inside the checkout, one that reaches the
    checkout through a symlink, one that is an existing file, and one that is
    unreadable.
    """
    root = Path(repo_root).resolve()
    try:
        created = Path(tempfile.mkdtemp(prefix=_REPORT_PREFIX))
    except OSError:
        raise SecurityRefusal(
            E_REPORT_DIR_REFUSED, "tempdir_unavailable"
        ) from None

    def _refuse(reason: str) -> None:
        shutil.rmtree(created, ignore_errors=True)
        raise SecurityRefusal(E_REPORT_DIR_REFUSED, reason)

    # The directory mkdtemp handed back must be a real directory, not a
    # symlink someone can re-point between this check and the write.
    if created.is_symlink() or not created.is_dir():
        _refuse("symlink_component")

    real = created.resolve()

    # Containment: neither the literal path nor its resolution may be the
    # repository or sit inside it.  Checking BOTH is the point -- the literal
    # path catches a TMPDIR spelled inside the checkout, and the resolved path
    # catches a TMPDIR that reaches the checkout through a symlink hop.
    for candidate in (created, real):
        if candidate == root or root in candidate.parents:
            _refuse("inside_repository")

    # No component *inside* the temporary base may be a symlink.  The check
    # stops at the resolved system temporary root rather than walking to "/",
    # because platform temporary roots are legitimately reached through
    # symlinks (macOS resolves /var to /private/var), and refusing those would
    # refuse every default configuration rather than any hostile one.
    base = Path(tempfile.gettempdir())
    stop = {base, base.resolve(), Path(os.sep)}
    node = created
    while node not in stop and node != node.parent:
        if node.is_symlink():
            _refuse("symlink_component")
        node = node.parent

    try:
        os.chmod(created, 0o700)
    except OSError:
        _refuse("report_unwritable")
    return created


def write_report(report_dir: object, payload: dict) -> Path:
    """Write exactly one exclusively-created ``report.json`` at mode 0600.

    ``O_EXCL`` is load-bearing: a pre-existing ``report.json`` is a refusal,
    not an overwrite, so a run can never append its evidence to somebody
    else's file.  The 0600 mode is a POSIX property; module doctrine records
    that no Windows run has established the equivalent.
    """
    directory = Path(report_dir)
    path = directory / REPORT_BASENAME
    body = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise SecurityRefusal(E_REPORT_DIR_REFUSED, "report_exists") from None
    except OSError:
        raise SecurityRefusal(E_REPORT_DIR_REFUSED, "report_unwritable") from None
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(body + "\n")
    except OSError:
        raise SecurityRefusal(E_REPORT_DIR_REFUSED, "report_unwritable") from None
    return path


# ---------------------------------------------------------------------------
# Child result document (the dispatcher seam)
# ---------------------------------------------------------------------------

CHILD_SCHEMA = "cairn.security.capability-result.v1"

#: The complete key vocabulary of the dispatcher child document.  Criterion
#: B-6 asserts the dispatcher-mode stdout parses as exactly this and nothing
#: more, and that direct-mode stdout does not parse as it at all.
CHILD_KEYS = ("schema", "capability", "contract", "evidence_mode", "result",
              "details")


def child_document(
    *,
    capability: str,
    contract: str,
    result: str,
    details: dict,
    evidence_mode: str = "loopback",
) -> dict:
    """Build the bounded child result document the activation contract fixes."""
    if result not in RESULTS:
        result = RESULT_DEGRADED
    return {
        "schema": CHILD_SCHEMA,
        "capability": scrub_terminal(capability),
        "contract": scrub_terminal(contract),
        "evidence_mode": scrub_terminal(evidence_mode),
        "result": result,
        "details": details,
    }


def result_line(result: str) -> str:
    """The single human-readable result line, from a closed vocabulary."""
    if result not in RESULTS:
        result = RESULT_DEGRADED
    return f"{RESULT_LINE_PREFIX} {result}"
