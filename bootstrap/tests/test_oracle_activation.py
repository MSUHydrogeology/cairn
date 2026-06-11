#!/usr/bin/env python3
"""Phase 2 tests — the activation gate (plan
``2026-06-10-claude-cairn-differential-oracle-gitref-baseline``).

The load-bearing properties: conservative HOLD-by-default on the sensitive
roster, no self-labelling (the evaluated artifact is checked against the
externally-anchored trusted expectation), scope-narrowing / deletion / uncovered
all HOLD, and a reviewed exemption clears its exact paths until it expires.
"""
from __future__ import annotations

import pytest

from bootstrap.tests import _oracle_activation as A


# --------------------------------------------------------------------- roster
def test_roster_membership():
    assert A.is_sensitive("bootstrap/_scaffold/upgrade.py")
    assert A.is_sensitive("bootstrap/scaffold.py")
    assert A.is_sensitive("bootstrap/tests/_oracle.py")
    assert not A.is_sensitive("docs/whatever.md")
    assert not A.is_sensitive("bootstrap/tests/test_upgrade.py")


# ------------------------------------------------------------------- parsing
_YAML = """\
# an active refactor
baseline_sha: 1111111111111111111111111111111111111111
trusted_ref: refs/heads/master
nonce: abc-123
scope:
  - bootstrap/_scaffold/
  - bootstrap/tests/_oracle.py
required_scenarios:
  - solo-greenfield
  - upgrade_apply
"""


def test_parse_activation_roundtrip():
    act = A.parse_activation(_YAML)
    assert act.baseline_sha == "1" * 40
    assert act.trusted_ref == "refs/heads/master"
    assert act.nonce == "abc-123"
    assert act.scope == ["bootstrap/_scaffold/", "bootstrap/tests/_oracle.py"]
    assert act.required_scenarios == ["solo-greenfield", "upgrade_apply"]


def test_parse_activation_missing_field():
    with pytest.raises(A.ActivationError):
        A.parse_activation("trusted_ref: x\nnonce: y\n")     # no baseline_sha


# ------------------------------------------------------------ acceptance gate
def _act(scope, nonce="n1", sha="s1", trusted_ref="t", scenarios=("solo-greenfield",)):
    return A.Activation(baseline_sha=sha, trusted_ref=trusted_ref, nonce=nonce,
                        scope=scope, required_scenarios=list(scenarios))


def test_nonsensitive_change_is_ok_without_activation():
    ok, holds = A.acceptance_check(["docs/x.md", "README.md"], None, None)
    assert ok and holds == []


def test_sensitive_change_holds_by_default():
    ok, holds = A.acceptance_check(["bootstrap/_scaffold/upgrade.py"], None, None)
    assert not ok
    assert "HOLD-by-default" in holds[0]


def test_self_labelling_refused_without_trusted_expectation():
    """An activation the evaluated branch wrote, with no external anchor, cannot
    authorize a sensitive change."""
    act = _act(["bootstrap/_scaffold/"])
    ok, holds = A.acceptance_check(["bootstrap/_scaffold/upgrade.py"], act, None)
    assert not ok and "HOLD-by-default" in holds[0]


def test_nonce_mismatch_refused():
    evaluated = _act(["bootstrap/_scaffold/"], nonce="forged")
    trusted = _act(["bootstrap/_scaffold/"], nonce="real")
    ok, holds = A.acceptance_check(["bootstrap/_scaffold/upgrade.py"], evaluated, trusted)
    assert not ok and "self-labelling" in holds[0]


def test_authorized_covered_change_ok():
    act = _act(["bootstrap/_scaffold/"])
    ok, holds = A.acceptance_check(["bootstrap/_scaffold/upgrade.py"], act, act)
    assert ok and holds == []


def test_scope_narrowing_holds():
    """The evaluated artifact narrows scope below the trusted expectation — exact
    equality refuses it as a field mismatch (P1.4: no weakening of authority)."""
    trusted = _act(["bootstrap/_scaffold/", "bootstrap/scaffold.py"])
    evaluated = _act(["bootstrap/_scaffold/"])            # narrowed: drops scaffold.py
    ok, holds = A.acceptance_check(["bootstrap/scaffold.py"], evaluated, trusted)
    assert not ok and "self-labelling" in holds[0] and "scope" in holds[0]


def test_trusted_ref_redirect_refused():
    """P1.4 probe: an evaluated artifact that redirects trusted_ref + empties the
    required scenarios must REFUSE (it weakens authority)."""
    trusted = _act(["bootstrap/_scaffold/"], trusted_ref="TRUSTED", scenarios=("upgrade_apply",))
    evaluated = _act(["bootstrap/_scaffold/"], trusted_ref="ATTACKER", scenarios=())
    ok, holds = A.acceptance_check(["bootstrap/_scaffold/upgrade.py"], evaluated, trusted)
    assert not ok and "self-labelling" in holds[0]


def test_required_scenarios_must_match():
    trusted = _act(["bootstrap/_scaffold/"], scenarios=("a", "b"))
    evaluated = _act(["bootstrap/_scaffold/"], scenarios=("a",))      # dropped one
    ok, holds = A.acceptance_check(["bootstrap/_scaffold/upgrade.py"], evaluated, trusted)
    assert not ok and "required_scenarios" in holds[0]


def test_empty_required_scenarios_holds():
    act = _act(["bootstrap/_scaffold/"], scenarios=())
    ok, holds = A.acceptance_check(["bootstrap/_scaffold/upgrade.py"], act, act)
    assert not ok and "no required scenarios" in holds[0]


def test_unknown_field_rejected():
    with pytest.raises(A.ActivationError):
        A.parse_activation("baseline_sha: x\ntrusted_ref: y\nnonce: z\nattacker_field: 1\n")


def test_uncovered_sensitive_change_holds():
    act = _act(["bootstrap/_scaffold/"])                  # authorizes only _scaffold/
    ok, holds = A.acceptance_check(
        ["bootstrap/_scaffold/upgrade.py", "bootstrap/security_check.py"], act, act)
    assert not ok and any("security_check.py" in h for h in holds)


def test_deletion_of_activation_holds():
    """Trusted expectation says a refactor is active, but the evaluated artifact
    was deleted → HOLD (the evaluated branch cannot self-deactivate)."""
    trusted = _act(["bootstrap/_scaffold/"])
    ok, holds = A.acceptance_check(["bootstrap/_scaffold/upgrade.py"], None, trusted)
    assert not ok and "absent/deleted" in holds[0]


def test_reviewed_exemption_clears_its_paths():
    ex = A.Exemption(paths=["bootstrap/_scaffold/upgrade.py"], reason="bugfix", expired=False)
    ok, holds = A.acceptance_check(
        ["bootstrap/_scaffold/upgrade.py"], None, None, exemptions=[ex])
    assert ok and holds == []


def test_expired_exemption_does_not_clear():
    ex = A.Exemption(paths=["bootstrap/_scaffold/upgrade.py"], reason="bugfix", expired=True)
    ok, holds = A.acceptance_check(
        ["bootstrap/_scaffold/upgrade.py"], None, None, exemptions=[ex])
    assert not ok
