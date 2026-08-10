#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Deployed-site HTTP/TLS posture evidence — passive observations, never a grade.

Every check here is **passive**: a declared ``GET`` or ``HEAD``, no attack
payload, no crawl, no link following, no ID inference.  What it reports is a
per-check ``present`` / ``missing`` / ``invalid`` observation against a
*reviewed expectation* the project wrote down, and it **refuses to issue a
letter grade** — a grade invites reading a summary instead of the observations,
and the observations are the evidence.

The same two-leg split as the API capability, for the same reason:

* **``local``** contacts a controlled loopback HTTP/TLS fixture only.
* **``deployed-passive --authorize-base-url``** is unauthenticated in v1, sends
  only ``GET``/``HEAD``, and requires the operator to restate the exact
  normalized base URL. That restatement is a human act and is **structural
  command separation, not actor authentication**.

**A local CLEAN is not a deployed CLEAN**, and this runner says so in the
summary, in the report, and in the dispatcher child document's
``evidence_mode``.  A fixture you configured to be correct tells you your
expectations parse; it tells you nothing about the site your users reach.

No observed header, cookie value, certificate subject, body, redirect URL or
query crosses any output channel.  Where a check needs to name what it looked
for, it names a **normalized token from the policy's own reviewed expectation
set** — never what the peer actually sent.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

CAPABILITY = "web-hosting-security"
CAPABILITY_CONTRACT = "1"
POLICY_RELATIVE = "dev/.cairn/web-hosting-policy.json"

#: Installed layout first, shared template layout second.  See the identical
#: note in ``api_access_security.py``: two fixed sibling names, containment
#: checked, ``sys.path`` never consulted.
_ENGINE_DIRNAMES = ("_web_hosting_security", "_security_net")

_FACADE = Path(__file__).resolve()

#: Headers every site type must carry, as fixed check ids.
_BASE_HEADERS = (
    ("hsts", "Strict-Transport-Security"),
    ("nosniff", "X-Content-Type-Options"),
    ("referrer-policy", "Referrer-Policy"),
    ("permissions-policy", "Permissions-Policy"),
)

#: Additional headers a site type requires.  ``data-api`` is not framed and does
#: not run scripts, so a CSP is not required of it; a browser-app is both.
_SITE_TYPE_HEADERS = {
    "static": (("csp", "Content-Security-Policy"),),
    "browser-app": (
        ("csp", "Content-Security-Policy"),
        ("cross-origin-opener", "Cross-Origin-Opener-Policy"),
    ),
    "data-api": (("cross-origin-resource", "Cross-Origin-Resource-Policy"),),
}

#: Cookie attributes that must be present on every observed cookie.
_COOKIE_ATTRIBUTES = ("secure", "httponly", "samesite")


def _load_engine():
    facade_dir = _FACADE.parent
    for name in _ENGINE_DIRNAMES:
        engine_dir = facade_dir / name
        init = engine_dir / "__init__.py"
        if not init.is_file():
            continue
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
    sys.stdout.write("cairn-security-result: DEGRADED\n")
    sys.stdout.write(f"  engine_incomplete:{reason}\n")
    return 20


# ---------------------------------------------------------------------------
# Observations
# ---------------------------------------------------------------------------


def _directive_names(value: str) -> "frozenset[str]":
    """Directive *names* from a policy-style header.  Values are discarded here.

    Discarding the values at the parse boundary is deliberate: a CSP value can
    carry hostnames, nonces and report endpoints, and none of those may reach an
    output channel.  What survives is the set of directive names, which is what
    the reviewed expectation set is written in.
    """
    names = set()
    for part in str(value).split(";"):
        token = part.strip().split(" ", 1)[0].strip().lower()
        if token:
            names.add(token)
    return frozenset(names)


def _cookie_attributes(value: str) -> "frozenset[str]":
    """Attribute names on one ``Set-Cookie``.  The cookie's name and value are
    both dropped before this returns."""
    attributes = set()
    for part in str(value).split(";")[1:]:
        token = part.strip().split("=", 1)[0].strip().lower()
        if token:
            attributes.add(token)
    return frozenset(attributes)


def _observe(engine_report, *, check_id, target_id, method, response,
             observation, detail, token=None):
    finding = engine_report.build_finding(
        check_id=check_id, target_id=target_id, method=method,
        status=response.status if response is not None else None,
        observation=observation, detail=detail,
    )
    if token is not None:
        # A normalized token from the policy's own reviewed expectation set --
        # written by the project, not observed from the peer.
        finding["detail"] = engine_report.scrub_terminal(f"{detail} [{token}]")
    return finding


def _check_https_target(engine, target, *, allow_classes):
    """Observe one target's HTTPS response.  Returns ``(findings, refusal)``."""
    net = importlib.import_module(f"{engine.__name__}.net")
    engine_report = importlib.import_module(f"{engine.__name__}.report")
    findings: list = []
    origin = target["https_origin"]
    try:
        response = net.perform_request(
            origin, method="GET", allow_classes=allow_classes
        )
    except engine_report.SecurityRefusal as exc:
        # A TLS refusal IS the certificate observation: chain, hostname and
        # expiry are validated by the platform trust store inside the engine,
        # and a failure there is reported as this check rather than swallowed.
        return findings, exc
    if response.is_redirect:
        return findings, net.classify_redirect(
            response, allow_classes=allow_classes,
            permitted_hosts=target["permitted_redirect_hosts"] or (origin.host,),
        )

    required = list(_BASE_HEADERS) + list(
        _SITE_TYPE_HEADERS.get(target["site_type"], ())
    )
    for check_id, header in required:
        present = response.header(header) is not None
        if not present:
            findings.append(_observe(
                engine_report, check_id=check_id, target_id=target["id"],
                method="GET", response=response, observation="missing",
                detail=f"the declared site type requires {header}",
            ))
    csp = response.header("Content-Security-Policy")
    if csp is not None:
        names = _directive_names(csp)
        for directive in target["expected_csp_directives"]:
            if directive not in names:
                findings.append(_observe(
                    engine_report, check_id="csp-directive",
                    target_id=target["id"], method="GET", response=response,
                    observation="missing",
                    detail="a reviewed CSP directive was absent",
                    token=directive,
                ))
    for raw in response.header_all("Set-Cookie"):
        attributes = _cookie_attributes(raw)
        for attribute in _COOKIE_ATTRIBUTES:
            if attribute not in attributes:
                findings.append(_observe(
                    engine_report, check_id="cookie-attribute",
                    target_id=target["id"], method="GET", response=response,
                    observation="missing",
                    detail="an observed cookie lacked a required attribute",
                    token=attribute,
                ))
    if target["expect_cookies"] and not response.header_all("Set-Cookie"):
        findings.append(_observe(
            engine_report, check_id="cookie-attribute",
            target_id=target["id"], method="GET", response=response,
            observation="missing",
            detail="the policy expects cookies and none were observed",
        ))
    return findings, None


def _check_http_upgrade(engine, target, *, allow_classes):
    """Observe the HTTP origin's upgrade behaviour, if one is declared."""
    net = importlib.import_module(f"{engine.__name__}.net")
    engine_report = importlib.import_module(f"{engine.__name__}.report")
    origin = target.get("http_origin")
    if origin is None:
        return [], None
    findings: list = []
    try:
        response = net.perform_request(
            origin, method="GET", allow_classes=allow_classes
        )
    except engine_report.SecurityRefusal as exc:
        return findings, exc
    if not response.is_redirect:
        findings.append(_observe(
            engine_report, check_id="http-upgrade", target_id=target["id"],
            method="GET", response=response, observation="missing",
            detail="the HTTP origin did not redirect to HTTPS",
        ))
        return findings, None
    host = response.redirect_host
    scheme = response.redirect_scheme
    permitted = target["permitted_redirect_hosts"]
    if permitted and host is not None and host not in permitted:
        findings.append(_observe(
            engine_report, check_id="redirect-allowlist",
            target_id=target["id"], method="GET", response=response,
            observation="invalid",
            detail="the redirect target host is outside the exact allowlist",
        ))
    # The ordering check: an HTTP origin must reach HTTPS **before** it changes
    # host.  A redirect that moves host while still on http:// has carried the
    # request over a channel an attacker on the path can rewrite, and arriving
    # at https:// afterwards does not undo that.
    if scheme == "http" and host is not None and host != origin.host:
        findings.append(_observe(
            engine_report, check_id="upgrade-before-host-change",
            target_id=target["id"], method="GET", response=response,
            observation="invalid",
            detail=(
                "the HTTP origin changed host before upgrading to HTTPS, so "
                "the host change happened over cleartext"
            ),
        ))
    elif scheme != "https":
        findings.append(_observe(
            engine_report, check_id="http-upgrade", target_id=target["id"],
            method="GET", response=response, observation="invalid",
            detail="the HTTP origin redirected somewhere other than HTTPS",
        ))
    return findings, None


def _emit(engine, *, result, findings, refusal, report_path, child, notes=()):
    engine_report = importlib.import_module(f"{engine.__name__}.report")
    details = {
        "capability": CAPABILITY,
        "findings": findings,
        "notes": [engine_report.scrub_terminal(n) for n in notes],
    }
    if refusal is not None:
        details["refusal"] = {"code": refusal.code, "reason": refusal.reason}
    if child:
        document = engine_report.child_document(
            capability=CAPABILITY, contract=CAPABILITY_CONTRACT,
            result=result, details=details,
        )
        sys.stdout.write(json.dumps(document, sort_keys=True) + "\n")
    else:
        sys.stdout.write(engine_report.result_line(result) + "\n")
        for note in details["notes"]:
            sys.stdout.write(f"  {note}\n")
        if refusal is not None:
            sys.stdout.write(f"  {refusal.code}:{refusal.reason}\n")
        for finding in findings:
            sys.stdout.write(
                "  observation "
                + " ".join(f"{k}={finding[k]}" for k in sorted(finding))
                + "\n"
            )
        if report_path is not None:
            sys.stdout.write(f"  report: {report_path}\n")
    return engine_report.EXIT_FOR_RESULT[result]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="web_hosting_security.py",
        description=(
            "Observe a site's HTTP/TLS posture against reviewed expectations. "
            "`local` contacts a loopback fixture only; `deployed-passive` is "
            "the Maintainer's read-only leg and requires --authorize-base-url."
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


#: The only non-literal host ``local`` accepts; see the identical note in
#: ``api_access_security.py``.  A name allowlist refuses a public hostname
#: before DNS, which a resolve-then-classify design cannot do.
_LOCAL_HOST_NAMES = frozenset({"localhost"})


def _refuse_non_loopback_target(engine, url) -> object:
    engine_report = importlib.import_module(f"{engine.__name__}.report")
    net = importlib.import_module(f"{engine.__name__}.net")
    if net.is_address_literal(url.host):
        if net.classify_address(url.host) != "loopback":
            return engine_report.SecurityRefusal(
                engine_report.E_POLICY_REFUSED, "non_loopback_target"
            )
        return None
    if url.host not in _LOCAL_HOST_NAMES:
        return engine_report.SecurityRefusal(
            engine_report.E_POLICY_REFUSED, "non_loopback_target"
        )
    return None


def main(argv: "list[str] | None" = None) -> int:
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

    try:
        report_dir = engine_report.create_report_dir(repo_root)
        policy_obj = policy_mod.load_policy(
            repo_root / POLICY_RELATIVE, kind=policy_mod.KIND_HOSTING
        )
        if not policy_obj.configured:
            return _emit(
                engine, result=engine_report.RESULT_INCOMPLETE, findings=[],
                refusal=None, report_path=None, child=child,
                notes=("the installed policy stub is unconfigured; fill it "
                       "before this capability can report evidence",),
            )
        section = policy_obj.section(section_name)
        targets = section["targets"]
        if deployed:
            authorized = {t["https_origin"].normalized for t in targets}
            if args.authorize_base_url not in authorized:
                raise engine_report.SecurityRefusal(
                    engine_report.E_POLICY_REFUSED, "authorization_mismatch"
                )
            targets = [
                t for t in targets
                if t["https_origin"].normalized == args.authorize_base_url
            ]
            allow_classes = net.PUBLIC_ONLY
        else:
            for target in targets:
                for key in ("https_origin", "http_origin"):
                    url = target.get(key)
                    if url is None:
                        continue
                    refusal = _refuse_non_loopback_target(engine, url)
                    if refusal is not None:
                        raise refusal
            allow_classes = net.LOOPBACK_ONLY

        findings: list = []
        for target in targets:
            for checker in (_check_http_upgrade, _check_https_target):
                produced, refusal = checker(
                    engine, target, allow_classes=allow_classes
                )
                findings.extend(produced)
                if refusal is not None:
                    raise refusal
        result = (
            engine_report.RESULT_FINDINGS if findings
            else engine_report.RESULT_CLEAN
        )
        evidence_mode = "deployed" if deployed else "loopback"
        report_path = engine_report.write_report(report_dir, {
            "schema": "cairn.security.web-hosting-report.v1",
            "capability": CAPABILITY,
            "contract": CAPABILITY_CONTRACT,
            "evidence_mode": evidence_mode,
            "deployed_leg_executed": deployed,
            "result": result,
            "findings": findings,
        })
        return _emit(
            engine, result=result, findings=findings, refusal=None,
            report_path=report_path, child=child,
            notes=() if deployed else (
                "loopback evidence only: the deployed leg has not executed, "
                "and a local CLEAN is not a deployed CLEAN",
            ),
        )
    except engine_report.SecurityRefusal as exc:
        return _emit(
            engine, result=engine_report.RESULT_DEGRADED, findings=[],
            refusal=exc, report_path=None, child=child,
        )


if __name__ == "__main__":
    raise SystemExit(main())
