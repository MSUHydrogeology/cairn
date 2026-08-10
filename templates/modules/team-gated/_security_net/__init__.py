#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Anthony Kendall and the Cairn contributors

"""Shared hardened-network engine for Cairn's two security capabilities.

One source tree, installed twice.  ``api-access-security`` installs it as
``scripts/_api_access_security/`` and ``web-hosting-security`` as
``scripts/_web_hosting_security/``; an adopter who selects both carries two
byte-identical copies, each independently hash-pinned in the install lockfile.
That cost is deliberate and is recorded in both modules' doctrine: the
alternative was two independently hand-written TLS clients, and a security
surface reviewed once is worth more than a duplicate byte saved.

**The import self-check is the runtime half of mapping-group completeness.**
Cairn's installer warns and continues when a module source is missing, so a
partial install is possible — a fail-open this engine closes from its own end.
Importing this package verifies that every member is present as a real regular
file, and :func:`verify_engine_complete` additionally verifies that every
member declares the same :data:`ENGINE_CONTRACT`.  Both raise
:class:`EngineIncomplete`, which the facades map to exit **20 / DEGRADED**
*before any policy is read* — so a partial engine reports degraded evidence
rather than partial evidence.
"""
from __future__ import annotations

from pathlib import Path

#: Engine contract version.  Every member declares it; a member that disagrees
#: is a partial or mixed install and is refused rather than run.
ENGINE_CONTRACT = "1"

#: The complete member set.  ``__init__.py`` is included because a copy of the
#: engine that lost its package marker is not importable at all, and naming it
#: keeps this list the single answer to "what does a complete engine contain".
ENGINE_MEMBERS = ("__init__.py", "policy.py", "net.py", "report.py")

_ENGINE_INCOMPLETE_CODE = "engine_incomplete"


class EngineIncomplete(RuntimeError):
    """A member is absent, is not a regular file, or declares a wrong contract.

    Carries the same ``code`` / ``reason`` pair as
    :class:`~._security_net.report.SecurityRefusal` so a facade's refusal
    handler treats the two uniformly.  It is defined here rather than in
    ``report.py`` for a load-bearing reason: ``report.py`` is itself one of the
    members that can be missing, so the exception raised when it is missing
    cannot live in it.
    """

    code = _ENGINE_INCOMPLETE_CODE

    def __init__(self, reason: str = "member_absent") -> None:
        self.reason = reason
        super().__init__(f"{_ENGINE_INCOMPLETE_CODE}:{reason}")


def _member_paths() -> "tuple[Path, ...]":
    here = Path(__file__).resolve().parent
    return tuple(here / name for name in ENGINE_MEMBERS)


def _check_members_present() -> None:
    """Presence check with no imports, so a missing member is still nameable."""
    for path in _member_paths():
        if path.is_symlink() or not path.is_file():
            raise EngineIncomplete("member_absent")


# Runs at import.  A facade that imports this package therefore cannot reach a
# policy read with an incomplete engine, whatever order its own imports take.
_check_members_present()


def verify_engine_complete() -> str:
    """Verify presence *and* contract agreement.  Returns the contract version.

    The facades call this as their first act, ahead of argument parsing, policy
    reading and every credential lookup.  Criterion A-10 executes a facade
    against a copy of the engine with one member removed and requires exit 20
    with no policy read.
    """
    _check_members_present()
    from . import net, policy, report

    for module in (net, policy, report):
        if getattr(module, "ENGINE_CONTRACT", None) != ENGINE_CONTRACT:
            raise EngineIncomplete("contract_disagreement")
    return ENGINE_CONTRACT
