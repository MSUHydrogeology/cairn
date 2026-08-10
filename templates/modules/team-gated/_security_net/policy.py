#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Strict policy schema for the two network-security capabilities.

The schema is **closed and refusing**: an unknown key, a duplicate identifier,
an unsupported method, a malformed URL, a control character, an embedded
credential or a secret-shaped literal is a refusal *before* anything else
happens — before DNS, before socket creation, and before any credential is
looked up.  That ordering is criterion A-8 and it is the reason this module
does no I/O beyond reading the policy file itself.

Two schema decisions carry most of the security weight:

* **Principals are ordinals, never labels.**  ``p1``, ``p2``, … and nothing
  else.  The credential environment-variable name is **derived** from the
  ordinal as ``CAIRN_API_P<N>_CREDENTIAL`` and cannot be supplied by policy, so
  a policy file can neither name a variable the operator did not intend nor
  smuggle a person's identity into a finding.
* **The local and deployed sections use disjoint ordinal sets.**  An ordinal
  appearing in both is refused, which makes the two sections' derived
  credential namespaces disjoint by construction.  That is what lets criterion
  B-4 assert, and not merely assume, that the loopback-only agent-facing leg
  never resolves a deployed credential name.

A protected operation must declare **both** an allowed and a denied case.  A
matrix of positive cases alone cannot report CLEAN, because a fixture that
authorizes everything would satisfy it -- criterion B-1's hazard exactly.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from . import net
from .report import (
    E_POLICY_REFUSED,
    ENGINE_CONTRACT,
    SecurityRefusal,
    has_control_characters,
)

__all__ = [
    "ENGINE_CONTRACT",
    "API_SCHEMA_ID",
    "HOSTING_SCHEMA_ID",
    "Policy",
    "credential_env_name",
    "load_policy",
]

API_SCHEMA_ID = "cairn.security.api-access-policy.v1"
HOSTING_SCHEMA_ID = "cairn.security.web-hosting-policy.v1"

KIND_API = "api"
KIND_HOSTING = "hosting"

#: Methods the loopback leg may declare.  The target is a disposable
#: project-owned fixture, so mutation is permitted there and only there.
LOCAL_METHODS = ("GET", "HEAD", "POST", "PUT", "PATCH", "DELETE")
#: Methods the deployed leg may declare.  Enforced at **schema** level so the
#: refusal precedes every runtime consideration (criterion B-7).
DEPLOYED_METHODS = ("GET", "HEAD")

SITE_TYPES = ("static", "browser-app", "data-api")
CASE_EXPECTATIONS = ("allow", "deny")
OPERATION_KINDS = ("object", "function", "property", "collection")

_ORDINAL_RE = re.compile(r"^p[1-9][0-9]{0,2}$")
_ROLE_RE = re.compile(r"^[a-z][a-z0-9_-]{0,31}$")
_LABEL_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]{0,63}$")
_HEADER_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9-]{0,63}$")
_POINTER_RE = re.compile(r"^(/[A-Za-z0-9_.~-]{1,64}){1,8}$")
_TOKEN_RE = re.compile(r"^[a-z][a-z0-9-]{0,63}$")

#: Longest *label* this schema will carry -- an id, a role, a directive token.
#: A label longer than this is refused rather than truncated, so an oversized
#: label can never become an output-channel carrier.
MAX_LABEL_LEN = 64

#: Longest *wide* string this schema will carry -- a URL, repository path,
#: JSON pointer, or declared request body.  A separate, larger
#: cap because a legitimate base URL routinely exceeds a label's width and a
#: 64-byte limit would refuse ordinary correct policies -- a schema that cannot
#: express a real target is not a stricter one.  Still bounded: an unbounded
#: string is an unbounded output-channel carrier.
MAX_URL_LEN = 512

#: Words that make a literal header value a refusal on sight.  This is a
#: coarse net and it is meant to be: a policy file is a tracked, reviewed
#: document and has no business carrying authentication material at all.
_SECRET_WORDS = (
    "bearer", "secret", "password", "passwd", "apikey", "api_key", "api-key",
    "token", "credential", "authorization", "private_key", "privatekey",
    "-----begin",
)
_SECRET_SHAPED_RE = re.compile(r"^[A-Za-z0-9+/_=-]{24,}$")

_CREDENTIAL_ENV_TEMPLATE = "CAIRN_API_P{ordinal}_CREDENTIAL"


def credential_env_name(principal_id: str) -> str:
    """Derive the credential variable name for an ordinal principal.

    Policy cannot supply this name: it is a pure function of the ordinal, and
    a policy key that tries to supply one is refused by the schema.
    """
    if not _ORDINAL_RE.match(str(principal_id)):
        raise SecurityRefusal(E_POLICY_REFUSED, "bad_principal_ordinal")
    return _CREDENTIAL_ENV_TEMPLATE.format(ordinal=str(principal_id)[1:])


def _refuse(reason: str) -> None:
    raise SecurityRefusal(E_POLICY_REFUSED, reason)


def _require_mapping(value: object) -> dict:
    if not isinstance(value, dict):
        _refuse("bad_type")
    return value  # type: ignore[return-value]


def _require_list(value: object) -> list:
    if not isinstance(value, list):
        _refuse("bad_type")
    return value  # type: ignore[return-value]


def _closed_keys(mapping: dict, allowed: tuple[str, ...]) -> None:
    for key in mapping:
        if not isinstance(key, str):
            _refuse("bad_type")
        if key not in allowed:
            _refuse("unknown_key")


def _clean_str(
    value: object, *, pattern: "re.Pattern[str] | None" = None,
    max_len: int = MAX_LABEL_LEN,
) -> str:
    if not isinstance(value, str):
        _refuse("bad_type")
    text = value  # type: ignore[assignment]
    if has_control_characters(text):
        _refuse("control_character")
    if len(text) > max_len:
        _refuse("label_too_long")
    if pattern is not None and not pattern.match(text):
        _refuse("bad_expectation")
    return text


def _clean_wide(value: object) -> str:
    """A string bounded by the wider cap: a URL, a repository path, a JSON
    pointer, or a declared request body.  Every other string in this schema is
    a *label* and takes the narrow cap."""
    return _clean_str(value, max_len=MAX_URL_LEN)


def _label(value: object) -> str:
    text = _clean_str(value)
    if not _LABEL_RE.match(text):
        _refuse("bad_expectation")
    return text


def _reject_secret_shaped(text: str) -> None:
    lowered = text.lower()
    for word in _SECRET_WORDS:
        if word in lowered:
            _refuse("embedded_credential")
    if _SECRET_SHAPED_RE.match(text):
        _refuse("secret_shaped")


def _headers(raw: object) -> tuple[tuple[str, str], ...]:
    mapping = _require_mapping(raw)
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for name, value in mapping.items():
        if not isinstance(name, str) or not _HEADER_NAME_RE.match(name):
            _refuse("header_malformed")
        lowered = name.lower()
        if lowered in seen:
            _refuse("duplicate_id")
        seen.add(lowered)
        for word in _SECRET_WORDS:
            if word in lowered:
                _refuse("embedded_credential")
        text = _clean_str(value)
        _reject_secret_shaped(text)
        out.append((name, text))
    return tuple(out)


class Policy:
    """A validated policy.  Every attribute is already schema-clean."""

    __slots__ = ("kind", "path", "schema_id", "configured", "sections",
                 "openapi_document")

    def __init__(
        self,
        *,
        kind: str,
        path: Path,
        schema_id: str,
        configured: bool,
        sections: dict,
        openapi_document: str | None,
    ) -> None:
        self.kind = kind
        self.path = path
        self.schema_id = schema_id
        self.configured = configured
        self.sections = sections
        self.openapi_document = openapi_document

    def section(self, name: str) -> dict:
        """Return the ``local`` or ``deployed`` section, refusing if absent."""
        try:
            return self.sections[name]
        except KeyError:
            raise SecurityRefusal(E_POLICY_REFUSED, "missing_key") from None

    def principal_ids(self, section_name: str) -> tuple[str, ...]:
        return tuple(
            p["id"] for p in self.section(section_name).get("principals", ())
        )

    def credential_names(self, section_name: str) -> tuple[str, ...]:
        """Derived variable names for one section only.

        The facades call this with exactly one section name.  Because the two
        sections' ordinal sets are disjoint by schema, the local leg's call can
        never return a name the deployed section would have used -- which is
        the structural half of criterion B-4.
        """
        return tuple(
            credential_env_name(pid) for pid in self.principal_ids(section_name)
        )


# ---------------------------------------------------------------------------
# Section parsing
# ---------------------------------------------------------------------------

_API_SECTION_KEYS = ("base_url", "environment", "principals", "operations",
                     "headers")
_HOSTING_SECTION_KEYS = ("targets", "headers")

_PRINCIPAL_KEYS = ("id", "role")
_OPERATION_KEYS = ("id", "method", "path", "kind", "cases",
                   "foreign_identifier")
_CASE_KEYS = ("id", "principal", "expect", "status", "require_present",
              "require_absent", "body")
_TARGET_KEYS = ("id", "http_origin", "https_origin", "site_type",
                "permitted_redirect_hosts", "expected_csp_directives",
                "expect_cookies")

_ENVIRONMENTS = ("local", "staging", "production")


def _principals(raw: object) -> tuple[dict, ...]:
    items = _require_list(raw)
    out: list[dict] = []
    seen: set[str] = set()
    for item in items:
        mapping = _require_mapping(item)
        # Checked BEFORE the generic closed-key sweep, so a policy that tries to
        # name its own credential variable is refused with the reason that says
        # so.  With the order reversed the specific token is unreachable and the
        # refusal reads as an ordinary typo -- a reason token that can never be
        # produced is a diagnostic that does not exist.
        for supplied in ("credential_env", "credential", "credential_name",
                         "credential_variable", "secret", "token"):
            if supplied in mapping:
                _refuse("credential_name_supplied")
        _closed_keys(mapping, _PRINCIPAL_KEYS)
        if "id" not in mapping:
            _refuse("missing_key")
        pid = _clean_str(mapping["id"])
        if not _ORDINAL_RE.match(pid):
            _refuse("bad_principal_ordinal")
        if pid in seen:
            _refuse("duplicate_id")
        seen.add(pid)
        entry: dict = {"id": pid}
        if "role" in mapping:
            role = _clean_str(mapping["role"])
            if not _ROLE_RE.match(role):
                _refuse("bad_role_token")
            # Retained for the adopter's own reading of their policy file and
            # deliberately NOT carried into any finding: criterion D-6 asserts
            # a role token appears in no output.
            entry["role"] = role
        out.append(entry)
    return tuple(out)


def _statuses(raw: object) -> tuple[int, ...]:
    items = _require_list(raw)
    if not items or len(items) > 8:
        _refuse("bad_expectation")
    out: list[int] = []
    for item in items:
        if not isinstance(item, int) or isinstance(item, bool):
            _refuse("bad_type")
        if not 100 <= item <= 599:
            _refuse("bad_expectation")
        out.append(item)
    return tuple(out)


def _pointers(raw: object) -> tuple[str, ...]:
    items = _require_list(raw)
    if len(items) > 16:
        _refuse("bad_expectation")
    out: list[str] = []
    for item in items:
        text = _clean_wide(item)
        if not _POINTER_RE.match(text):
            _refuse("bad_expectation")
        if text in out:
            _refuse("duplicate_id")
        out.append(text)
    return tuple(out)


def _cases(raw: object, *, allowed_principals: set[str]) -> tuple[dict, ...]:
    items = _require_list(raw)
    out: list[dict] = []
    seen: set[str] = set()
    for item in items:
        mapping = _require_mapping(item)
        _closed_keys(mapping, _CASE_KEYS)
        for key in ("id", "principal", "expect"):
            if key not in mapping:
                _refuse("missing_key")
        cid = _label(mapping["id"])
        if cid in seen:
            _refuse("duplicate_id")
        seen.add(cid)
        principal = _clean_str(mapping["principal"])
        if not _ORDINAL_RE.match(principal):
            _refuse("bad_principal_ordinal")
        if principal not in allowed_principals:
            _refuse("bad_principal_ordinal")
        expect = _clean_str(mapping["expect"])
        if expect not in CASE_EXPECTATIONS:
            _refuse("bad_expectation")
        case: dict = {"id": cid, "principal": principal, "expect": expect}
        case["status"] = (
            _statuses(mapping["status"]) if "status" in mapping else ()
        )
        case["require_present"] = (
            _pointers(mapping["require_present"])
            if "require_present" in mapping else ()
        )
        case["require_absent"] = (
            _pointers(mapping["require_absent"])
            if "require_absent" in mapping else ()
        )
        if "body" in mapping:
            body = _clean_wide(mapping["body"])
            _reject_secret_shaped(body)
            case["body"] = body
        # A read case satisfied by a status code alone proves nothing about
        # authorization, so an ALLOW case must say what it expects to see.
        if expect == "allow" and not case["require_present"] and not case["status"]:
            _refuse("bad_expectation")
        if expect == "deny" and not case["status"]:
            _refuse("bad_expectation")
        out.append(case)
    return tuple(out)


def _operations(
    raw: object, *, methods: tuple[str, ...], allowed_principals: set[str]
) -> tuple[dict, ...]:
    items = _require_list(raw)
    out: list[dict] = []
    seen: set[str] = set()
    for item in items:
        mapping = _require_mapping(item)
        _closed_keys(mapping, _OPERATION_KEYS)
        for key in ("id", "method", "path", "kind", "cases"):
            if key not in mapping:
                _refuse("missing_key")
        oid = _label(mapping["id"])
        if oid in seen:
            _refuse("duplicate_id")
        seen.add(oid)
        method = _clean_str(mapping["method"])
        if method not in methods:
            _refuse(
                "deployed_method_refused" if methods == DEPLOYED_METHODS
                else "unsupported_method"
            )
        path = _clean_wide(mapping["path"])
        if not path.startswith("/") or "://" in path or "?" in path:
            _refuse("bad_url")
        kind = _clean_str(mapping["kind"])
        if kind not in OPERATION_KINDS:
            _refuse("bad_expectation")
        cases = _cases(mapping["cases"], allowed_principals=allowed_principals)
        expectations = {c["expect"] for c in cases}
        # Criterion B-1: a protected operation with only positive cases cannot
        # report CLEAN, because a fixture that authorizes everything satisfies
        # it.  The refusal is at schema level so it precedes every request.
        if "allow" not in expectations or "deny" not in expectations:
            _refuse("no_denial_case")
        if kind == "object":
            principals = {c["principal"] for c in cases}
            if len(principals) < 2:
                _refuse("no_denial_case")
        entry: dict = {
            "id": oid, "method": method, "path": path, "kind": kind,
            "cases": cases,
        }
        if "foreign_identifier" in mapping:
            entry["foreign_identifier"] = _clean_str(
                mapping["foreign_identifier"]
            )
        elif kind == "collection":
            _refuse("missing_key")
        out.append(entry)
    return tuple(out)


def _hosts(raw: object) -> tuple[str, ...]:
    items = _require_list(raw)
    if len(items) > 8:
        _refuse("bad_expectation")
    out: list[str] = []
    for item in items:
        text = _clean_str(item)
        normalized = net.normalize_host(text)
        if normalized in out:
            _refuse("duplicate_id")
        out.append(normalized)
    return tuple(out)


def _tokens(raw: object) -> tuple[str, ...]:
    items = _require_list(raw)
    if len(items) > 16:
        _refuse("bad_expectation")
    out: list[str] = []
    for item in items:
        text = _clean_str(item)
        if not _TOKEN_RE.match(text):
            _refuse("bad_expectation")
        if text in out:
            _refuse("duplicate_id")
        out.append(text)
    return tuple(out)


def _targets(raw: object, *, deployed: bool) -> tuple[dict, ...]:
    items = _require_list(raw)
    out: list[dict] = []
    seen: set[str] = set()
    for item in items:
        mapping = _require_mapping(item)
        _closed_keys(mapping, _TARGET_KEYS)
        for key in ("id", "https_origin", "site_type"):
            if key not in mapping:
                _refuse("missing_key")
        tid = _label(mapping["id"])
        if tid in seen:
            _refuse("duplicate_id")
        seen.add(tid)
        https_origin = net.normalize_base_url(_clean_wide(mapping["https_origin"]))
        if https_origin.scheme != "https":
            _refuse("scheme_refused")
        entry: dict = {"id": tid, "https_origin": https_origin}
        if "http_origin" in mapping:
            http_origin = net.normalize_base_url(
                _clean_wide(mapping["http_origin"])
            )
            if http_origin.scheme != "http":
                _refuse("scheme_refused")
            entry["http_origin"] = http_origin
        site_type = _clean_str(mapping["site_type"])
        if site_type not in SITE_TYPES:
            _refuse("bad_site_type")
        entry["site_type"] = site_type
        entry["permitted_redirect_hosts"] = (
            _hosts(mapping["permitted_redirect_hosts"])
            if "permitted_redirect_hosts" in mapping else ()
        )
        entry["expected_csp_directives"] = (
            _tokens(mapping["expected_csp_directives"])
            if "expected_csp_directives" in mapping else ()
        )
        expect_cookies = mapping.get("expect_cookies", False)
        if not isinstance(expect_cookies, bool):
            _refuse("bad_type")
        entry["expect_cookies"] = expect_cookies
        if deployed and https_origin.address_class == "loopback":
            # A deployed target that points at loopback is a mis-filled policy,
            # not a deployed check.  Refused so "deployed CLEAN" cannot be
            # produced by pointing the deployed leg at a local fixture.
            _refuse("non_loopback_target")
        out.append(entry)
    return tuple(out)


def _api_section(raw: object, *, deployed: bool) -> dict:
    mapping = _require_mapping(raw)
    _closed_keys(mapping, _API_SECTION_KEYS)
    for key in ("base_url", "principals", "operations"):
        if key not in mapping:
            _refuse("missing_key")
    base_url = net.normalize_base_url(_clean_wide(mapping["base_url"]))
    if deployed and base_url.scheme != "https":
        _refuse("scheme_refused")
    if deployed and base_url.address_class == "loopback":
        _refuse("non_loopback_target")
    section: dict = {"base_url": base_url}
    if "environment" in mapping:
        environment = _clean_str(mapping["environment"])
        if environment not in _ENVIRONMENTS:
            _refuse("bad_expectation")
        # Carried for the adopter's reading only.  It is a LABEL and never an
        # authority: criterion B-3 drives every refusal row with the label set
        # to each of its three values, and the outcome must not change.
        section["environment"] = environment
    section["principals"] = _principals(mapping["principals"])
    allowed = {p["id"] for p in section["principals"]}
    section["operations"] = _operations(
        mapping["operations"],
        methods=DEPLOYED_METHODS if deployed else LOCAL_METHODS,
        allowed_principals=allowed,
    )
    section["headers"] = (
        _headers(mapping["headers"]) if "headers" in mapping else ()
    )
    return section


def _hosting_section(raw: object, *, deployed: bool) -> dict:
    mapping = _require_mapping(raw)
    _closed_keys(mapping, _HOSTING_SECTION_KEYS)
    if "targets" not in mapping:
        _refuse("missing_key")
    section: dict = {"targets": _targets(mapping["targets"], deployed=deployed)}
    section["headers"] = (
        _headers(mapping["headers"]) if "headers" in mapping else ()
    )
    return section


_TOP_KEYS = ("schema", "configured", "local", "deployed", "openapi_document",
             "comment")


def parse_policy(document: object, *, kind: str, path: Path) -> Policy:
    """Validate an already-decoded policy document.

    Split from :func:`load_policy` so the schema can be exercised without
    touching the filesystem, and so every refusal below provably precedes any
    network or credential act.
    """
    mapping = _require_mapping(document)
    _closed_keys(mapping, _TOP_KEYS)
    expected_schema = API_SCHEMA_ID if kind == KIND_API else HOSTING_SCHEMA_ID
    if mapping.get("schema") != expected_schema:
        _refuse("bad_schema_id")
    configured = mapping.get("configured")
    if not isinstance(configured, bool):
        _refuse("bad_type")
    if "comment" in mapping:
        # A stub ships a prose pointer here, so this field takes the wide cap.
        # It is validated and then discarded: nothing reads a policy comment,
        # which is why it cannot become an output-channel carrier.
        _clean_wide(mapping["comment"])
    if "local" not in mapping:
        _refuse("missing_key")

    build = _api_section if kind == KIND_API else _hosting_section
    sections: dict = {"local": build(mapping["local"], deployed=False)}
    if "deployed" in mapping:
        sections["deployed"] = build(mapping["deployed"], deployed=True)

    # Ordinal namespaces must be disjoint across sections, so the two legs'
    # derived credential variable names are disjoint by construction.
    if kind == KIND_API and "deployed" in sections:
        local_ids = {p["id"] for p in sections["local"]["principals"]}
        deployed_ids = {p["id"] for p in sections["deployed"]["principals"]}
        if local_ids & deployed_ids:
            _refuse("principal_reused_across_sections")

    openapi_document = None
    if "openapi_document" in mapping:
        if kind != KIND_API:
            _refuse("unknown_key")
        openapi_document = _clean_wide(mapping["openapi_document"])
        if not openapi_document.endswith(".json"):
            _refuse("bad_expectation")
        if openapi_document.startswith("/") or ".." in openapi_document:
            _refuse("bad_url")

    if configured:
        # Criterion E-2: "configured" cannot buy a CLEAN over an empty matrix.
        for name, section in sections.items():
            if kind == KIND_API and not section["operations"]:
                _refuse("no_operations")
            if kind == KIND_HOSTING and not section["targets"]:
                _refuse("no_targets")

    return Policy(
        kind=kind,
        path=path,
        schema_id=expected_schema,
        configured=configured,
        sections=sections,
        openapi_document=openapi_document,
    )


def load_policy(path: object, *, kind: str) -> Policy:
    """Read and validate a policy file.

    The file must be a real regular file, not a symlink.  That is the same
    property the activation dispatcher binds for a living-state policy record,
    checked here as well so the runner does not depend on the dispatcher having
    run first.
    """
    candidate = Path(path)
    if candidate.is_symlink():
        _refuse("policy_symlink")
    if not candidate.is_file():
        _refuse("policy_unreadable")
    try:
        raw = candidate.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        raise SecurityRefusal(E_POLICY_REFUSED, "policy_unreadable") from None
    try:
        document = json.loads(raw)
    except ValueError:
        raise SecurityRefusal(E_POLICY_REFUSED, "json_malformed") from None
    return parse_policy(document, kind=kind, path=candidate)
