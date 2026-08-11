#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Cross-principal API authorization evidence — require the denial, then execute it.

This runner does **not** implement an authorization model and does not infer
one.  It requires the project to *state* its intended allow/deny facts in
`dev/.cairn/api-access-policy.json` and then executes them, so that CLEAN means
one narrow thing: *the declared denial matrix held at the named target and time,
no more.*

Two subcommands, and the split between them is the whole safety design:

* **``local``** — the agent-facing leg.  It can reach **loopback only**: the
  policy's host must be a loopback literal or the exact name ``localhost``, every
  resolved address must be loopback, and the *connected peer* is verified after
  connect.  Mutation methods are permitted here because the target is a
  disposable project-owned fixture.  It reads only the local section's derived
  credential variables; the deployed section's names are never looked up on this
  path.
* **``deployed-passive``** — the Maintainer's leg.  It sends only ``GET`` and
  ``HEAD``, refuses unless ``--authorize-base-url`` is **byte-for-byte** the
  policy's normalized base URL, and is not reachable from the activation
  dispatcher's registry at all.  Typing that argument is a human act; an agent
  that types it has defeated the control.  This is **structural command
  separation, not actor authentication** — a shell process cannot prove who
  invoked it.

Nothing observed ever reaches an output channel.  Findings carry fixed check,
operation, case and assertion identifiers, ordinal principal ids, a status
*class*, and a five-value magnitude bucket — never a value, a length, a member
count, a header, a body fragment, or a credential.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

CAPABILITY = "api-access-security"
CAPABILITY_CONTRACT = "1"
POLICY_RELATIVE = "dev/.cairn/api-access-policy.json"

#: Where the engine package is looked for, in order.  Exactly two names, both
#: siblings of this file: the installed layout (``scripts/_api_access_security``,
#: the facade-engine convention ``_facade_engine_dir`` already recognises) and
#: the shared template layout this source is reviewed in.  Neither is
#: adopter-supplied, ``sys.path`` is never consulted, and both are containment
#: checked below.
_ENGINE_DIRNAMES = ("_api_access_security", "_security_net")

_FACADE = Path(__file__).resolve()


def _load_engine():
    """Load the sibling engine package fail-closed, never via ``sys.path``."""
    facade_dir = _FACADE.parent
    for name in _ENGINE_DIRNAMES:
        engine_dir = facade_dir / name
        init = engine_dir / "__init__.py"
        if not init.is_file():
            continue
        # Parity with bootstrap/scaffold.py's launcher: a real directory inside
        # this file's own directory, never a symlink and never out of tree, so
        # the loader cannot be pointed at code from somewhere else.
        if (engine_dir.is_symlink() or init.is_symlink()
                or engine_dir.resolve().parent != facade_dir):
            continue
        canonical = f"cairn_security_engine_{name}"
        spec = importlib.util.spec_from_file_location(
            canonical, init, submodule_search_locations=[str(engine_dir)]
        )
        if spec is None or spec.loader is None:  # pragma: no cover
            return None, "member_absent"
        module = importlib.util.module_from_spec(spec)
        sys.modules[canonical] = module
        try:
            spec.loader.exec_module(module)
        except BaseException as exc:  # noqa: BLE001
            # The engine package verifies its own members AT IMPORT, so the
            # failure this catches is the ordinary incomplete-install case --
            # and it arrives before the name `EngineIncomplete` exists to be
            # caught by name, because the class is defined in the module being
            # loaded.  Caught broadly and reduced to a FIXED reason on purpose:
            # a traceback is an uncontrolled output channel (it carries
            # absolute paths, and for a different failure could carry a value),
            # and criterion A-10 requires exit 20 / DEGRADED here, not a crash.
            sys.modules.pop(canonical, None)
            reason = getattr(exc, "reason", None)
            return None, reason if isinstance(reason, str) else "member_absent"
        return module, ""
    # The FIRST candidate whose __init__.py exists is the engine; a failure in
    # it is fatal rather than a reason to try the next name, so a broken
    # install can never be masked by falling through to the other layout.
    return None, "member_absent"


def _fail_engine_incomplete(reason: str) -> int:
    """Exit 20 / DEGRADED with no policy read, per criterion A-10."""
    sys.stdout.write("cairn-security-result: DEGRADED\n")
    sys.stdout.write(f"  engine_incomplete:{reason}\n")
    return 20


# ---------------------------------------------------------------------------
# Assertion helpers
# ---------------------------------------------------------------------------


def _resolve_pointer(document: object, pointer: str):
    """Walk a JSON pointer.  Returns ``(found, value)`` and never raises."""
    node = document
    for raw in pointer.lstrip("/").split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(node, dict):
            if token not in node:
                return False, None
            node = node[token]
        elif isinstance(node, list):
            try:
                index = int(token)
            except ValueError:
                return False, None
            if not 0 <= index < len(node):
                return False, None
            node = node[index]
        else:
            return False, None
    return True, node


def _decode_json(body: bytes):
    """Decode a response body, returning ``(ok, document)``.

    A body that is not strict UTF-8 or not JSON is a *finding input*, not a
    crash: the case that expected a readable object simply does not get one.
    """
    try:
        return True, json.loads(body.decode("utf-8", "strict"))
    except (UnicodeDecodeError, ValueError):
        return False, None


# ---------------------------------------------------------------------------
# The matrix
# ---------------------------------------------------------------------------


def _case_findings(engine_report, operation, case, response, decoded_ok,
                   document, fingerprinter):
    """Evaluate one declared case.  Returns a list of findings (often empty)."""
    findings = []
    common = {
        "operation_id": operation["id"],
        "case_id": case["id"],
        "principal_ids": (case["principal"],),
        "method": operation["method"],
        "status": response.status,
    }
    if case["status"] and response.status not in case["status"]:
        findings.append(engine_report.build_finding(
            check_id="declared-status", assertion_id="status",
            detail="observed status is outside the declared set for this case",
            **common,
        ))
    if case["expect"] == "deny":
        # A denial that returned a success status is the BOLA finding this
        # module exists to produce; the status set above already catches it, and
        # this row makes the *reason* explicit rather than leaving a reader to
        # infer it from a status class.
        if 200 <= response.status < 300:
            findings.append(engine_report.build_finding(
                check_id="cross-principal-denial", assertion_id="denied",
                detail=(
                    "a second principal received a success status for an "
                    "object the policy declares denied to it"
                ),
                **common,
            ))
        return findings

    # An ALLOW case is only satisfied by what it can *see*.  A status code alone
    # never satisfies a read case -- the schema refuses an allow case that
    # declares neither a status nor a property expectation, and the property
    # expectations are checked here.
    for pointer in case["require_present"]:
        found, _value = (False, None) if not decoded_ok else _resolve_pointer(
            document, pointer
        )
        if not found:
            findings.append(engine_report.build_finding(
                check_id="required-property", assertion_id="present",
                detail="a property the policy requires present was absent",
                **common,
            ))
    for pointer in case["require_absent"]:
        found, value = (False, None) if not decoded_ok else _resolve_pointer(
            document, pointer
        )
        if found:
            findings.append(engine_report.build_finding(
                check_id="overexposed-property", assertion_id="absent",
                detail="a property the policy requires absent was present",
                observed_value=value, fingerprinter=fingerprinter, **common,
            ))
    if operation["kind"] == "collection" and decoded_ok:
        foreign = operation.get("foreign_identifier")
        if foreign and foreign in json.dumps(document, ensure_ascii=True):
            findings.append(engine_report.build_finding(
                check_id="foreign-member", assertion_id="absent",
                detail=(
                    "a collection response carried an identifier belonging to "
                    "another principal's fixture object"
                ),
                observed_value=foreign, fingerprinter=fingerprinter, **common,
            ))
    return findings


def _run_matrix(engine, section, *, allow_classes, credentials, deployed):
    """Execute every declared case.  Returns ``(findings, refusal)``."""
    net = importlib.import_module(f"{engine.__name__}.net")
    engine_report = importlib.import_module(f"{engine.__name__}.report")
    fingerprinter = engine_report.Fingerprinter()
    base = section["base_url"]
    findings: list = []
    for operation in section["operations"]:
        for case in operation["cases"]:
            credential = credentials.get(case["principal"])
            try:
                response = net.perform_request(
                    base, method=operation["method"], path=operation["path"],
                    allow_classes=allow_classes,
                    headers=section["headers"], credential=credential,
                    body=case.get("body", "").encode("utf-8") if case.get("body") else b"",
                )
            except engine_report.SecurityRefusal as exc:
                return findings, exc
            if response.is_redirect:
                # Never followed.  On either leg a redirect means the target is
                # not the target the policy declared, so the run is degraded
                # rather than reported as evidence about the declared target.
                return findings, net.classify_redirect(
                    response, allow_classes=allow_classes,
                    permitted_hosts=(base.host,),
                )
            decoded_ok, document = _decode_json(response.body)
            findings.extend(_case_findings(
                engine_report, operation, case, response, decoded_ok, document,
                fingerprinter,
            ))
    return findings, None


# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------


def _read_credentials(engine, policy_obj, section_name):
    """Read only ``section_name``'s derived variables.  Returns ``(map, missing)``.

    The names are derived from ordinals by the policy module and the two
    sections' ordinal sets are disjoint by schema, so this call structurally
    cannot return a name the other section would have used -- criterion B-4.
    """
    policy_mod = importlib.import_module(f"{engine.__name__}.policy")
    values: dict = {}
    missing: list = []
    for principal in policy_obj.principal_ids(section_name):
        name = policy_mod.credential_env_name(principal)
        value = os.environ.get(name)
        if not value:
            missing.append(principal)
        else:
            values[principal] = value
    return values, missing


# ---------------------------------------------------------------------------
# Target validation
# ---------------------------------------------------------------------------

#: The only non-literal host ``local`` accepts.  A name allowlist rather than a
#: post-resolution check, so a public hostname is refused **before DNS** --
#: criterion B-3's ordering requirement, which a resolve-then-classify design
#: cannot meet.
_LOCAL_HOST_NAMES = frozenset({"localhost"})


def _refuse_non_loopback_target(engine, base) -> object:
    """Return a refusal when ``base`` is not reachable-as-loopback, else None."""
    engine_report = importlib.import_module(f"{engine.__name__}.report")
    net = importlib.import_module(f"{engine.__name__}.net")
    if net.is_address_literal(base.host):
        if net.classify_address(base.host) != "loopback":
            return engine_report.SecurityRefusal(
                engine_report.E_POLICY_REFUSED, "non_loopback_target"
            )
        return None
    if base.host not in _LOCAL_HOST_NAMES:
        return engine_report.SecurityRefusal(
            engine_report.E_POLICY_REFUSED, "non_loopback_target"
        )
    return None


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def _emit(engine, *, result, findings, refusal, report_path, child, notes=()):
    engine_report = importlib.import_module(f"{engine.__name__}.report")
    scrubbed_notes = [engine_report.scrub_terminal(n) for n in notes]
    if child:
        details = engine_report.render_details(
            findings=findings, refusal=refusal,
            notes=scrubbed_notes, finding_label="finding",
        )
        document = engine_report.child_document(
            capability=CAPABILITY, contract=CAPABILITY_CONTRACT,
            result=result, details=details,
        )
        sys.stdout.write(json.dumps(document, sort_keys=True) + "\n")
    else:
        sys.stdout.write(engine_report.result_line(result) + "\n")
        for note in scrubbed_notes:
            sys.stdout.write(f"  {note}\n")
        if refusal is not None:
            sys.stdout.write(f"  {refusal.code}:{refusal.reason}\n")
        for finding in findings:
            sys.stdout.write(
                "  finding "
                + " ".join(f"{k}={finding[k]}" for k in sorted(finding))
                + "\n"
            )
        if report_path is not None:
            sys.stdout.write(f"  report: {report_path}\n")
    return engine_report.EXIT_FOR_RESULT[result]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="api_access_security.py",
        description=(
            "Execute a project's declared cross-principal API authorization "
            "matrix. `local` reaches loopback only; `deployed-passive` is the "
            "Maintainer's read-only leg and requires --authorize-base-url."
        ),
    )
    sub = parser.add_subparsers(dest="mode", required=True)
    local = sub.add_parser("local", help="loopback fixture evidence")
    local.add_argument(
        "--child-document", action="store_true",
        help="emit the activation dispatcher's bounded child JSON document",
    )
    deployed = sub.add_parser(
        "deployed-passive", help="Maintainer-invoked read-only deployed check"
    )
    deployed.add_argument("--authorize-base-url", required=True)
    return parser


def main(argv: "list[str] | None" = None) -> int:
    # First act, ahead of argument parsing, policy reading, and every credential
    # lookup: a partial engine reports degraded evidence, never partial evidence.
    engine, load_failure = _load_engine()
    if engine is None:
        return _fail_engine_incomplete(load_failure)
    try:
        engine.verify_engine_complete()
    except engine.EngineIncomplete as exc:
        return _fail_engine_incomplete(exc.reason)

    engine_report = importlib.import_module(f"{engine.__name__}.report")
    policy_mod = importlib.import_module(f"{engine.__name__}.policy")
    net = importlib.import_module(f"{engine.__name__}.net")

    args = build_arg_parser().parse_args(argv)
    child = bool(getattr(args, "child_document", False))
    repo_root = _FACADE.parent.parent
    deployed = args.mode == "deployed-passive"
    section_name = "deployed" if deployed else "local"

    report_dir = None
    report_path = None
    try:
        # Refused before any network or credential act, so a hostile TMPDIR
        # cannot make the runner do work first and fail afterwards (A-9).
        report_dir = engine_report.create_report_dir(repo_root)
        policy_obj = policy_mod.load_policy(
            repo_root / POLICY_RELATIVE, kind=policy_mod.KIND_API
        )
        if not policy_obj.configured:
            return _emit(
                engine, result=engine_report.RESULT_INCOMPLETE, findings=[],
                refusal=None, report_path=None, child=child,
                notes=("the installed policy stub is unconfigured; fill it "
                       "before this capability can report evidence",),
            )
        section = policy_obj.section(section_name)
        if deployed:
            # Byte-for-byte against the NORMALIZED policy value, and the
            # argument is deliberately not normalized: normalizing it would let
            # a trailing slash, an upper-case host or an explicit default port
            # match, which is exactly criterion B-5's near-miss table.
            if args.authorize_base_url != section["base_url"].normalized:
                raise engine_report.SecurityRefusal(
                    engine_report.E_POLICY_REFUSED, "authorization_mismatch"
                )
            allow_classes = net.PUBLIC_ONLY
        else:
            refusal = _refuse_non_loopback_target(engine, section["base_url"])
            if refusal is not None:
                raise refusal
            allow_classes = net.LOOPBACK_ONLY

        credentials, missing = _read_credentials(
            engine, policy_obj, section_name
        )
        if missing:
            raise engine_report.SecurityRefusal(
                engine_report.E_CREDENTIAL_ABSENT, "unspecified"
            )
        findings, refusal = _run_matrix(
            engine, section, allow_classes=allow_classes,
            credentials=credentials, deployed=deployed,
        )
        if refusal is not None:
            raise refusal
        result = (
            engine_report.RESULT_FINDINGS if findings
            else engine_report.RESULT_CLEAN
        )
        report_path = engine_report.write_report(report_dir, {
            "schema": "cairn.security.api-access-report.v1",
            "capability": CAPABILITY,
            "contract": CAPABILITY_CONTRACT,
            "evidence_mode": "deployed" if deployed else "loopback",
            "result": result,
            "findings": findings,
        })
        return _emit(
            engine, result=result, findings=findings, refusal=None,
            report_path=report_path, child=child,
            notes=() if deployed else (
                "loopback evidence only: a local CLEAN is not a deployed CLEAN",
            ),
        )
    except engine_report.SecurityRefusal as exc:
        return _emit(
            engine, result=engine_report.RESULT_DEGRADED, findings=[],
            refusal=exc, report_path=None, child=child,
        )


if __name__ == "__main__":
    raise SystemExit(main())
