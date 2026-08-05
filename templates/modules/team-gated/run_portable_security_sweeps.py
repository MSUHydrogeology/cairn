#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Portable offline security-sweep orchestrator -- the portable-security-sweeps
adapter runner.

**Standard-library only.**  Installs no scanner and bundles none.  It drives
exactly one adapter -- Gitleaks, offline, with no network flag -- over two scan
questions (the current tree, the committed history) and reports on the shared
aggregate exit space ``0 / 5 / 10 / 20`` with precedence ``20 > 10 > 5 > 0``.

Three properties are the contract, and every one of them is a refusal rather
than a best effort:

1. **A leg that did not run never renders as CLEAN.**  A missing binary is
   INCOMPLETE (5), loudly.  Absence is never clean.
2. **Candidate-tree content cannot choose the executable, its configuration,
   or a suppression.**  The adapter is resolved from the trusted host
   environment and refused if it lives inside the tree under check; the
   adapter config, the ignore file and the report path are runner-owned and
   materialized off-tree; reviewed suppressions come from the validated policy
   and from nowhere else.
3. **Full mode -- the only CLEAN-capable mode -- is reachable only when the
   resolved executable's SHA-256 matches a digest the admission ceremony
   recorded for this ``(version, platform, architecture)``.**  A recorded
   digest that does not match is a contradiction and degrades (20); no
   recorded digest for this platform is the ordinary *unadmitted* case and
   takes the reduced-provenance path, which can never reach 0.

A clean run is a **tripwire, not a proof**.

Chunk A of ``portable-security-sweeps`` lands the CLI, the strict policy
loader, the strict version parser, the admitted-artifact mode selector, the
aggregate and the deterministic summary.  The adapter-execution seam returns
INCOMPLETE with a named reason until the executable trust boundary lands; there
is deliberately **no** ``subprocess`` import in this file at that commit.
"""
from __future__ import annotations

import argparse
import json
import platform
import re
import sys
from pathlib import Path
from typing import Any, NamedTuple

# --- the shared aggregate exit space -----------------------------------------
# Reuses python-security's space (see templates/modules/team-gated/
# run_security_audit.py) so an adopter reads one exit vocabulary across every
# Cairn security module.  Precedence: degraded > findings > incomplete > clean.
_AGG_CLEAN = 0
_AGG_INCOMPLETE = 5
_AGG_FINDINGS = 10
_AGG_DEGRADED = 20

_PRECEDENCE = {_AGG_CLEAN: 0, _AGG_INCOMPLETE: 1, _AGG_FINDINGS: 2, _AGG_DEGRADED: 3}

#: A leg with no applicable input.  Distinct from INCOMPLETE, and it never
#: weakens another leg -- it contributes nothing to the aggregate at all.
_NOT_APPLICABLE = "NOT_APPLICABLE"

_CAPABILITY = "portable-security-sweeps"
_CONTRACT = "portable-security-sweeps/local-v1"
_EVIDENCE_MODE = "offline"
_SCHEMA = 1

#: The adapter this module supports.  OSV-Scanner, zizmor and Trivy are **not
#: supported adapters and not names the policy accepts**; each returns as its
#: own proposal with its own executable chain and ambient-config evidence.
_ADAPTER = "gitleaks"

# --- the source-owned admitted-artifact set ----------------------------------
#: Keyed by ``(version, system, machine)``; the value carries the SHA-256 of
#: the artifact the admission matrix was actually run against plus the
#: identifier of its evidence record in
#: ``dev/measurement/gitleaks-version-support.md``.
#:
#: **Not policy-controlled, not environment-controlled, and not adopter-
#: editable without editing reviewed code.**  The digest deliberately does not
#: live in the JSON policy: the policy is the adopter-editable document, and a
#: digest anything with write access to the adopter's tree could edit would let
#: a candidate *admit its own binary* -- strictly weaker than the self-reported
#: version string it replaces.
#:
#: **Initially empty.**  ``8.30.1`` enters only when the admission subcommand
#: emits a record against a Maintainer-supplied, checksum-verified binary.  An
#: empty set means the module ships reduced-provenance-only: useful current-tree
#: findings and an honest INCOMPLETE, never CLEAN.


class Admission(NamedTuple):
    """One admitted artifact: the digest measured, and where the evidence is."""

    sha256: str
    evidence: str


# CAIRN-ADMISSIONS-BEGIN (the admission ceremony edits exactly this block)
_ADMITTED_ARTIFACTS: dict[tuple[str, str, str], Admission] = {}
# CAIRN-ADMISSIONS-END

#: The one major this runner's argv, output schema and Git-invocation
#: expectations were derived against.  A different major is not "probably
#: fine"; it is unmeasured, and unmeasured means INCOMPLETE without execution.
_SUPPORTED_MAJOR = 8

# --- policy limits -----------------------------------------------------------
_POLICY_MAX_BYTES = 64 * 1024
_FINGERPRINT_MAX_LEN = 200
_FINGERPRINT_CHARSET = re.compile(r"\A[A-Za-z0-9._:/+=@-]+\Z")

#: Names a policy may never carry, checked *before* the closed-key check so the
#: refusal reason says which class was attempted.  The policy names no path, no
#: argv, no environment variable, no executable, no config file, no baseline,
#: and -- per the digest design above -- no digest, hash, checksum or admitted
#: artifact.
_FORBIDDEN_POLICY_NAME_PARTS = (
    "path", "arg", "argv", "env", "environment", "exec", "executable",
    "command", "cmd", "config", "toml", "baseline", "ignorefile",
    "digest", "hash", "checksum", "artifact", "admit", "admitted",
    "version", "mode", "versions", "binary", "url", "network",
)

_POLICY_TOP_KEYS = frozenset({"schema", "gitleaks"})
_POLICY_GITLEAKS_KEYS = frozenset({"fingerprints"})

#: Control characters refused in a fingerprint.  ``\n`` and ``\r`` are
#: deliberately **excluded** here: they are the ignore-file line-injection case
#: and carry their own dedicated refusal branch, so that deleting either branch
#: reddens exactly the node that names it.
_CTRL_OTHER = frozenset(
    [chr(c) for c in range(0x20) if chr(c) not in "\n\r"] + [chr(0x7F)]
)


class PolicyError(ValueError):
    """A policy document this runner refuses.  Refusal precedes every side
    effect: no executable is resolved and no temporary file is materialized."""


class _DuplicateKey(PolicyError):
    pass


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    for key, _value in pairs:
        if key in seen:
            raise _DuplicateKey(f"duplicate JSON key in policy: {key!r}")
        seen.add(key)
    return dict(pairs)


def _refuse_forbidden_names(keys: list[str]) -> None:
    """Refuse a policy key whose *name* attempts to reach a surface the policy
    does not own.  Runs before the closed-key check purely so the reason names
    the class -- the closed-key check would refuse these anyway."""
    for key in keys:
        low = key.lower()
        for part in _FORBIDDEN_POLICY_NAME_PARTS:
            if part in low:
                raise PolicyError(
                    f"policy key {key!r} names a surface the policy does not "
                    f"own ({part!r}); the policy carries reviewed fingerprint "
                    f"suppressions and nothing else"
                )


def parse_policy(text: str) -> dict[str, Any]:
    """Validate a policy *document* and return the accepted shape.

    Every refusal is its own branch so that a single deleted branch reddens the
    single node that names it."""
    try:
        doc = json.loads(text, object_pairs_hook=_no_duplicate_keys)
    except _DuplicateKey:
        raise
    except (ValueError, UnicodeDecodeError) as exc:
        raise PolicyError(f"policy is not valid JSON: {exc}") from None
    if not isinstance(doc, dict):
        raise PolicyError("policy top level must be a JSON object")

    _refuse_forbidden_names(list(doc))
    unknown = sorted(set(doc) - _POLICY_TOP_KEYS)
    if unknown:
        raise PolicyError(f"unknown top-level policy key(s): {unknown}")
    missing = sorted(_POLICY_TOP_KEYS - set(doc))
    if missing:
        raise PolicyError(f"missing top-level policy key(s): {missing}")

    if doc["schema"] != _SCHEMA:
        raise PolicyError(
            f"unsupported policy schema {doc['schema']!r}; this runner "
            f"accepts schema {_SCHEMA} only"
        )

    section = doc["gitleaks"]
    if not isinstance(section, dict):
        raise PolicyError("policy 'gitleaks' must be a JSON object")
    _refuse_forbidden_names(list(section))
    unknown = sorted(set(section) - _POLICY_GITLEAKS_KEYS)
    if unknown:
        raise PolicyError(f"unknown key(s) under 'gitleaks': {unknown}")
    if "fingerprints" not in section:
        raise PolicyError("policy 'gitleaks' must carry 'fingerprints'")

    raw = section["fingerprints"]
    if not isinstance(raw, list):
        raise PolicyError("policy 'gitleaks.fingerprints' must be a list")
    seen: set[str] = set()
    for item in raw:
        if not isinstance(item, str):
            raise PolicyError(f"fingerprint is not a string: {item!r}")
        if "\n" in item or "\r" in item:
            raise PolicyError(
                "fingerprint carries a newline; one fingerprint may never "
                "become two ignore-file lines"
            )
        if any(ch in _CTRL_OTHER for ch in item):
            raise PolicyError("fingerprint carries a control character")
        if not item:
            raise PolicyError("fingerprint is empty")
        if len(item) > _FINGERPRINT_MAX_LEN:
            raise PolicyError(
                f"fingerprint exceeds {_FINGERPRINT_MAX_LEN} characters"
            )
        if not _FINGERPRINT_CHARSET.match(item):
            raise PolicyError(f"fingerprint has a disallowed character: {item!r}")
        if item in seen:
            raise PolicyError(f"duplicate fingerprint: {item!r}")
        seen.add(item)
    return {"schema": _SCHEMA, "gitleaks": {"fingerprints": list(raw)}}


def load_policy(path: Path) -> dict[str, Any]:
    """Read and validate the policy at *path*.  Size is checked before the
    read, and the read is strict UTF-8."""
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise PolicyError(f"policy is unreadable: {exc}") from None
    if size > _POLICY_MAX_BYTES:
        raise PolicyError(
            f"policy exceeds {_POLICY_MAX_BYTES} bytes ({size}); refused "
            f"before it is read"
        )
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise PolicyError(f"policy is not readable strict UTF-8: {exc}") from None
    return parse_policy(text)


# --- version parsing and mode selection --------------------------------------

#: ``[0-9]`` and not ``\d``: ``\d`` matches Unicode decimal digits, so a
#: candidate reporting Devanagari or fullwidth digits would parse.
_VERSION_RE = re.compile(r"\A(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")


def parse_version(text: str) -> tuple[int, int, int] | None:
    """Parse an **exact** ``X.Y.Z``.  Anything else -- a ``v`` prefix, two
    components, a prerelease suffix, surrounding whitespace or a newline, a
    leading zero, a trailing character, a control character, non-ASCII digits
    -- returns ``None``, and ``None`` means *unmeasured*, not *probably fine*."""
    if not isinstance(text, str):
        return None
    match = _VERSION_RE.match(text)
    if match is None:
        return None
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def platform_key() -> tuple[str, str]:
    """The ``(system, machine)`` half of an admitted-artifact key."""
    return (platform.system().lower(), platform.machine().lower())


class ModeChoice(NamedTuple):
    """The outcome of mode selection.  ``mode`` is ``"full"``, ``"reduced"`` or
    ``None``; ``None`` means *refuse without executing a scan leg*."""

    mode: str | None
    result: int | None
    reason: str


def select_mode(
    version_text: str,
    digest: str | None,
    key: tuple[str, str],
    admissions: dict[tuple[str, str, str], Admission] | None = None,
) -> ModeChoice:
    """Map a self-reported version plus a measured digest onto a mode.

    Two cases that must never collapse into one:

    * **digest MISMATCH** -- a digest *is* recorded for this
      ``(version, platform, architecture)`` and the resolved binary is not it.
      That is a contradiction: DEGRADED (20), no scan leg runs, never reduced,
      never full, never CLEAN.
    * **digest ABSENT** -- no digest is recorded for this
      ``(version, platform, architecture)``.  That is the ordinary *unadmitted*
      case: the reduced-provenance path, which can never reach 0.
    """
    admitted = _ADMITTED_ARTIFACTS if admissions is None else admissions
    parsed = parse_version(version_text)
    if parsed is None:
        return ModeChoice(
            None, _AGG_INCOMPLETE,
            f"adapter version {version_text!r} is not an exact X.Y.Z; the "
            f"version is unmeasured, so no scan leg was run",
        )
    if parsed[0] != _SUPPORTED_MAJOR:
        return ModeChoice(
            None, _AGG_INCOMPLETE,
            f"adapter major {parsed[0]} is outside the measured major "
            f"{_SUPPORTED_MAJOR}; no scan leg was run",
        )
    full_key = (version_text, key[0], key[1])
    admission = admitted.get(full_key)
    if admission is None:
        return ModeChoice(
            "reduced", None,
            f"no admitted artifact is recorded for {full_key}; reduced "
            f"provenance -- this run cannot report CLEAN",
        )
    if digest is None or digest != admission.sha256:
        return ModeChoice(
            None, _AGG_DEGRADED,
            f"admitted artifact digest mismatch for {full_key}: recorded "
            f"{admission.sha256[:12]}..., resolved "
            f"{(digest or 'unmeasured')[:12]}...; no scan leg was run",
        )
    return ModeChoice(
        "full", None,
        f"admitted artifact {full_key} matched digest "
        f"{admission.sha256[:12]}... (evidence {admission.evidence})",
    )


# --- the aggregate -----------------------------------------------------------


def aggregate(results: list[int]) -> int:
    """``20 > 10 > 5 > 0``.  A finding is never hidden by an incomplete
    sibling leg, which is the whole reason this is a precedence and not a
    minimum."""
    worst = _AGG_CLEAN
    for result in results:
        if _PRECEDENCE[result] > _PRECEDENCE[worst]:
            worst = result
    return worst


class LegOutcome(NamedTuple):
    """One scan question's answer.  ``result`` is ``None`` for a NOT
    APPLICABLE leg, which contributes nothing to the aggregate."""

    leg: str
    result: int | None
    status: str
    reason: str
    findings: tuple[dict[str, Any], ...] = ()


def _escape(value: Any) -> str:
    """Render *value* so it cannot become a terminal control or forge a report
    line.  ``ensure_ascii=True`` escapes C0/C1 controls, newlines, ANSI escapes
    and bidi code points into their ``\\uXXXX`` forms rather than emitting the
    raw byte."""
    return json.dumps(value, ensure_ascii=True, sort_keys=True)


def _adapter_seam(_context: dict[str, Any]) -> LegOutcome:
    """The adapter-execution seam.

    Chunk A ships this file with **no** ``subprocess`` import: the executable
    trust boundary is not yet in the tree, so the honest answer is INCOMPLETE
    with a named reason.  It is never CLEAN."""
    return LegOutcome(
        "adapter", _AGG_INCOMPLETE, "INCOMPLETE",
        "adapter execution not yet enabled",
    )


def summarize(
    target: Path,
    policy_path: Path,
    legs: list[LegOutcome],
    mode: str | None,
    mode_reason: str,
    adapter_facts: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """The deterministic summary.  The human report is a rendering of *this*
    validated structure and never of scanner text."""
    scored = [leg.result for leg in legs if leg.result is not None]
    return {
        "schema": _SCHEMA,
        "capability": _CAPABILITY,
        "contract": _CONTRACT,
        "evidence_mode": _EVIDENCE_MODE,
        "adapter": _ADAPTER,
        "target": str(target),
        "policy": str(policy_path),
        "mode": mode,
        "mode_reason": mode_reason,
        "adapter_facts": dict(adapter_facts or {}),
        "legs": [
            {
                "leg": leg.leg,
                "result": leg.result,
                "status": leg.status,
                "reason": leg.reason,
                "findings": list(leg.findings),
            }
            for leg in legs
        ],
        "result": aggregate(scored),
        "residuals": list(RESIDUALS),
    }


#: Residuals printed with every run.  A residual that lives only in a doctrine
#: file an adopter may never open is a shelf artifact.
RESIDUALS = (
    "This is a tripwire on a trusted checkout, not a proof and not a reviewer "
    "for untrusted changes.",
    "Host executables are validated for shape and containment, never for "
    "provenance: v1 does not authenticate them.",
    "The pre-execution screens (candidate ignore file, repository-local "
    "configuration) are snapshots; a same-user delete/create race between the "
    "screen and execution is accepted, not closed.",
    "The repository-local configuration screen bounds configuration only, and "
    "the counted Git config keys are defence in depth over the keys they name "
    "-- not a boundary.",
)


def render_report(summary: dict[str, Any]) -> str:
    """Render the validated summary.  Every interpolated string goes through
    ``_escape``; no child stdout or stderr is ever relayed."""
    lines = [
        f"[portable] adapter={_ADAPTER} mode={_escape(summary['mode'])}",
        f"[portable] target={_escape(summary['target'])}",
        f"[portable] mode-reason: {_escape(summary['mode_reason'])}",
    ]
    for leg in summary["legs"]:
        status = leg["status"]
        result = "n/a" if leg["result"] is None else str(leg["result"])
        lines.append(
            f"[portable] leg={_escape(leg['leg'])} status={status} "
            f"result={result} reason={_escape(leg['reason'])}"
        )
        for finding in leg["findings"]:
            lines.append(f"[portable]   finding {_escape(finding)}")
    for residual in summary["residuals"]:
        lines.append(f"[portable] residual: {residual}")
    lines.append(f"[portable] aggregate={summary['result']}")
    return "\n".join(lines)


def child_document(summary: dict[str, Any]) -> dict[str, Any]:
    """The ``security-verification`` child document -- one bounded strict-UTF-8
    JSON document, with ``details`` under its own bounded schema."""
    return {
        "schema": _SCHEMA,
        "capability": _CAPABILITY,
        "contract": _CONTRACT,
        "evidence_mode": _EVIDENCE_MODE,
        "result": summary["result"],
        "details": {
            "adapter": summary["adapter"],
            "mode": summary["mode"],
            "mode_reason": summary["mode_reason"],
            "legs": [
                {
                    "leg": leg["leg"],
                    "result": leg["result"],
                    "status": leg["status"],
                    "reason": leg["reason"],
                    "finding_count": len(leg["findings"]),
                }
                for leg in summary["legs"]
            ],
        },
    }


def _default_policy_path() -> Path:
    return Path(__file__).resolve().parent / "portable_security_policy.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_portable_security_sweeps.py",
        description=(
            "One measured offline security sweep over the current tree and the "
            "committed history.  Installs no scanner."
        ),
    )
    parser.add_argument("--target", default=".",
                        help="repository to sweep (default: the current directory)")
    parser.add_argument("--policy", default=None,
                        help="policy document (default: the runner's sibling)")
    parser.add_argument("--json", action="store_true",
                        help="emit the deterministic JSON summary")
    parser.add_argument(
        "--security-verification", action="store_true",
        help=("the local/offline security-verification entry point: emit the "
              "bounded child result document and nothing else"),
    )
    return parser


def run_sweep(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    """The ordinary sweep.  Policy refusal precedes every side effect."""
    target = Path(args.target).resolve()
    policy_path = (
        Path(args.policy).resolve() if args.policy else _default_policy_path()
    )
    try:
        load_policy(policy_path)
    except PolicyError as exc:
        legs = [LegOutcome("policy", _AGG_DEGRADED, "DEGRADED", str(exc))]
        return _AGG_DEGRADED, summarize(
            target, policy_path, legs, None, "policy refused before any side effect"
        )
    outcome = _adapter_seam({"target": target})
    summary = summarize(
        target, policy_path, [outcome], None,
        "mode selection is not reachable until the adapter seam executes",
    )
    return summary["result"], summary


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result, summary = run_sweep(args)
    if args.security_verification:
        sys.stdout.write(
            json.dumps(child_document(summary), ensure_ascii=True,
                       sort_keys=True) + "\n"
        )
    elif args.json:
        sys.stdout.write(
            json.dumps(summary, ensure_ascii=True, sort_keys=True) + "\n"
        )
    else:
        sys.stdout.write(render_report(summary) + "\n")
    return result


if __name__ == "__main__":  # pragma: no cover -- exercised by subprocess
    raise SystemExit(main())
