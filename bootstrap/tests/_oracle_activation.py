#!/usr/bin/env python3
"""Activation gate for the differential oracle (plan Phase 2).

A behavior-preserving refactor of the engine **cannot turn its oracle off**, and
a change classification **cannot be self-labelled** by the evaluated branch. This
module is the data-only logic for that:

* an enumerated **refactor-sensitive roster** (exact paths/globs — confirming-2
  Finding 3) of behavior-preservation-sensitive code;
* an **activation artifact** (``dev/.cairn/active-refactor.yml``) recording the
  baseline SHA, the trusted ref, the exact scope, the required scenarios, and a
  single-use nonce;
* a **conservative-default acceptance check**: any diff touching the sensitive
  roster **HOLDs** unless an **externally-anchored** prerequisite authorizes it —
  an active-refactor artifact whose scope covers the change *and matches the
  trusted expectation*, **or** a reviewed intentional-change exemption (exact
  path scope + bounded lifetime). Neither classification may be authored solely
  by the evaluated branch (the artifact is checked **against** the externally
  supplied trusted expectation — deletion, scope-narrowing, nonce/baseline
  mismatch, and uncovered sensitive changes all HOLD).

The *external anchoring itself* (the pre-pinned transition checker, the
path/promotion manifests) is the supervised Phase 0/4 machinery; this module
consumes the trusted expectation as an input — it never self-authorizes.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path

# Exact paths/globs (a trailing "/" is a directory prefix). Roster ADDITIONS are
# themselves gate-control changes and require the same external authorization.
SENSITIVE_ROSTER: tuple[str, ...] = (
    # the engine
    "bootstrap/scaffold.py",
    "bootstrap/_scaffold/",
    # the trust machinery itself
    "bootstrap/tests/_oracle.py",
    "bootstrap/tests/_oracle_trust.py",
    "bootstrap/tests/_oracle_activation.py",
    "bootstrap/tests/_gate_transition.py",
    "bootstrap/tests/_gate_reanchor.py",
    "bootstrap/tests/_gate_manifest.py",
    "bootstrap/verify_integrity.py",
    "bootstrap/security_check.py",
)


def is_sensitive(path: str, roster: tuple[str, ...] = SENSITIVE_ROSTER) -> bool:
    p = path.replace("\\", "/").lstrip("./")
    for entry in roster:
        if entry.endswith("/"):
            if p == entry.rstrip("/") or p.startswith(entry):
                return True
        elif p == entry:
            return True
    return False


def covers(scope: list[str], path: str) -> bool:
    """Does an authorized *scope* (exact paths/globs) cover *path*?"""
    p = path.replace("\\", "/").lstrip("./")
    for entry in scope:
        if entry.endswith("/"):
            if p == entry.rstrip("/") or p.startswith(entry):
                return True
        elif p == entry:
            return True
    return False


@dataclass
class Activation:
    baseline_sha: str
    trusted_ref: str
    nonce: str
    scope: list[str] = field(default_factory=list)
    required_scenarios: list[str] = field(default_factory=list)


@dataclass
class Exemption:
    paths: list[str]
    reason: str
    expired: bool = False        # the verifier is handed the already-evaluated lifetime


class ActivationError(ValueError):
    """The activation artifact is malformed."""


def parse_activation(text: str) -> Activation:
    """Parse the minimal `active-refactor.yml` schema (stdlib only): top-level
    ``key: value`` scalars plus ``key:`` followed by indented ``- item`` lists.
    Raises ``ActivationError`` on a missing required field."""
    scalars: dict[str, str] = {}
    lists: dict[str, list[str]] = {}
    cur: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.lstrip().startswith("- "):
            if cur is None:
                raise ActivationError(f"list item with no key: {line!r}")
            lists.setdefault(cur, []).append(line.lstrip()[2:].strip().strip('"\''))
            continue
        if ":" not in line:
            raise ActivationError(f"unparseable line: {line!r}")
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip('"\'')
        if val == "":
            cur = key                       # a list/section header
            lists.setdefault(key, [])
        else:
            scalars[key] = val
            cur = None
    known = {"baseline_sha", "trusted_ref", "nonce", "scope", "required_scenarios"}
    unknown = (set(scalars) | set(lists)) - known
    if unknown:                                       # reject injected fields
        raise ActivationError(f"activation has unknown field(s): {sorted(unknown)}")
    try:
        return Activation(
            baseline_sha=scalars["baseline_sha"],
            trusted_ref=scalars["trusted_ref"],
            nonce=scalars["nonce"],
            scope=lists.get("scope", []),
            required_scenarios=lists.get("required_scenarios", []),
        )
    except KeyError as e:
        raise ActivationError(f"activation missing required field: {e}") from e


def acceptance_check(
    changed_paths: list[str],
    activation: Activation | None,
    trusted_expectation: Activation | None,
    *,
    exemptions: list[Exemption] | None = None,
    roster: tuple[str, ...] = SENSITIVE_ROSTER,
) -> tuple[bool, list[str]]:
    """Return ``(ok, holds)``. **Conservative default:** any sensitive-roster path
    HOLDs unless externally authorized.

    * *activation* — the artifact as found in the **evaluated** tree (or ``None``
      if absent/deleted).
    * *trusted_expectation* — the externally-anchored authority (supplied from
      outside the evaluated branch; ``None`` when no refactor is authorized).

    The evaluated artifact is checked **against** the trusted expectation, so the
    evaluated branch cannot self-authorize by writing/deleting/narrowing it.
    """
    exemptions = exemptions or []
    sensitive = [p for p in changed_paths if is_sensitive(p, roster)]
    if not sensitive:
        return True, []                     # no sensitive change → nothing to authorize

    holds: list[str] = []

    # An exemption (externally reviewed, unexpired, exact scope) clears its paths.
    def exempted(path: str) -> bool:
        return any(covers(ex.paths, path) and not ex.expired for ex in exemptions)

    unexempted = [p for p in sensitive if not exempted(p)]
    if not unexempted:
        return True, []

    # Beyond exemptions, an active-refactor artifact is required — and it must
    # match the externally-anchored trusted expectation (no self-labelling).
    if trusted_expectation is None:
        holds.append("sensitive change with NO externally-anchored authorization (HOLD-by-default)")
        return False, holds
    if activation is None:
        holds.append("activation artifact absent/deleted while a refactor is authorized (HOLD)")
        return False, holds
    # EVERY authority-bearing field must match the trusted expectation exactly
    # not just nonce + baseline_sha, but trusted_ref, scope, AND
    # required_scenarios — and ordered (a reordered/missing/extra scenario or a
    # redirected trusted_ref must refuse). Activation is a dataclass, so `!=`
    # compares all fields; there are no mutable result/report fields.
    if activation != trusted_expectation:
        diff = [f for f in ("baseline_sha", "trusted_ref", "nonce", "scope", "required_scenarios")
                if getattr(activation, f) != getattr(trusted_expectation, f)]
        holds.append(f"activation does not match the trusted expectation "
                     f"(self-labelling refused; differing fields: {diff})")
        return False, holds
    if not trusted_expectation.required_scenarios:
        holds.append("authorized activation declares no required scenarios (HOLD)")
        return False, holds
    # In-scope: every unexempted sensitive change must be covered by the (now
    # exactly-matched) authorized scope.
    for p in unexempted:
        if not covers(trusted_expectation.scope, p):
            holds.append(f"sensitive change not covered by the authorized scope: {p}")
    return (not holds), holds


def _changed_sensitive(repo: Path, prior_anchor: str, candidate: str,
                       is_sensitive_fn=is_sensitive,
                       roster: tuple[str, ...] = SENSITIVE_ROSTER) -> list[str]:
    """**Independently** derive the changed sensitive files: the acceptance
    command discovers the diff itself rather than trusting a caller-supplied set."""
    out = subprocess.run(
        ["git", "-C", str(repo), "diff", "--name-only", f"{prior_anchor}..{candidate}"],
        capture_output=True, text=True, check=False)
    if out.returncode != 0:
        raise ActivationError(f"git diff {prior_anchor[:12]}..{candidate} failed: {out.stderr.strip()}")
    return sorted(f for f in out.stdout.splitlines()
                  if f.strip() and is_sensitive_fn(f.strip(), roster))


def run_acceptance(
    repo: Path,
    prior_anchor: str,
    candidate: str,
    *,
    trusted_expectation: Activation | None,
    evaluated_activation_path: Path | str,
    is_sensitive_fn=is_sensitive,
    roster: tuple[str, ...] = SENSITIVE_ROSTER,
    exemptions: list[Exemption] | None = None,
) -> tuple[bool, list[str], list[str]]:
    """**The authoritative acceptance command**. It is the
    production caller of :func:`acceptance_check` — the gate an uncovered sensitive
    change must fail. It (1) **independently discovers** the changed sensitive set
    from ``prior_anchor..candidate``, (2) loads the **evaluated** activation
    artifact from the target (``None`` if absent/deleted), and (3) HOLDs via
    :func:`acceptance_check` against the externally supplied ``trusted_expectation``
    on deletion / field-mismatch / uncovered change / missing-or-empty scenarios.

    Returns ``(ok, holds, changed_sensitive)``.
    """
    changed = _changed_sensitive(repo, prior_anchor, candidate, is_sensitive_fn, roster)
    evaluated: Activation | None = None
    p = Path(evaluated_activation_path)
    if p.is_file():
        evaluated = parse_activation(p.read_text(encoding="utf-8"))
    ok, holds = acceptance_check(changed, evaluated, trusted_expectation,
                                 exemptions=exemptions, roster=roster)
    return ok, holds, changed
