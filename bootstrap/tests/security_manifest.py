# SPDX-License-Identifier: MIT
"""The security test family, named file by file with an owner and a reason.

**Why a manifest rather than a marker written into each file.** A
``pytestmark = pytest.mark.security`` line in seventeen files has no single
place to read, no place to say *why* a file is a member, and no way to notice a
file that quietly stopped being one.  Worse, every one of those files is
gate-frozen, so marking them in place would put seventeen entries on the
re-anchor ceremony to express a fact about zero of them.  The membership lives
here; ``conftest.py`` applies the marker from it.

**What membership means.** A member does not run in the per-change loop.  It
runs in the release ceremony, where ``bootstrap/security_check.py`` executes the
*entire* suite under ``CAIRN_RELEASE_GATE_ACTIVE=1`` with skips and xfails
failing closed.  Nothing is deleted and nothing is weakened; what moves is
*when* it runs.

**The consequence of a wrong entry, stated plainly.** Adding a file here removes
it from every per-change run.  That failure is silent -- a test that stops
running does not announce itself -- which is why the membership check
(``test_security_marker.py``) is written as a mutation rather than a count: it
unmarks a member and requires the check to fail.  A check that merely asserted
"the marker collects something" would pass against an empty manifest.

A change to a security surface still runs the full canonical pair with no
deselection, per the accepted contract.  The carve-out is temporal for everyone
else and simply absent for the surface under test.
"""

from __future__ import annotations

#: ``filename -> (owner, reason)``.  Owner is the surface the file defends, not
#: a person: this repository has one maintainer, and naming them would date.
SECURITY_FAMILY: dict[str, tuple[str, str]] = {
    "test_api_access_security.py": (
        "api-access module",
        "Shipped module that mediates outbound API credentials in an adopter "
        "tree.",
    ),
    "test_ast_attest.py": (
        "scaffold engine attestation",
        "Pins the engine package against a committed AST baseline. A "
        "supply-chain control: it is what notices the engine changing shape "
        "without a re-anchor.",
    ),
    "test_default_security_stance.py": (
        "default posture",
        "Asserts what an adopter gets before they configure anything -- the "
        "stance that applies to every install that never tunes it.",
    ),
    "test_gate_preflight.py": (
        "differential-oracle gate",
        "The gate's own pre-run integrity check. Largest member at 318 tests, "
        "and the reason the split is worth making.",
    ),
    "test_gate_reanchor.py": (
        "gate anchor ceremony",
        "The supervised re-anchor. Governs how the gate's trust root moves.",
    ),
    "test_portable_security_sweeps.py": (
        "portable-sweep trust root",
        "Resolves and executes a host `gitleaks` binary; AGENTS.md names it a "
        "high-risk executable trust root.",
    ),
    "test_reanchor.py": (
        "gate anchor ceremony",
        "The re-anchor's mechanics and refusals, alongside test_gate_reanchor.",
    ),
    "test_security_capability_install.py": (
        "capability install",
        "What security capabilities the scaffold grants a target tree.",
    ),
    "test_security_check.py": (
        "release gate entry point",
        "bootstrap/security_check.py itself -- the command the release ceremony "
        "runs. Unchanged by the split, and the reason the split is safe.",
    ),
    "test_security_finding_confidentiality.py": (
        "finding disclosure",
        "Governs what a security finding may reveal in a shared record.",
    ),
    "test_security_leaf.py": (
        "leaf module",
        "Smallest shipped security surface; included so the family is defined "
        "by kind and not by size.",
    ),
    "test_security_lint.py": (
        "Bandit gate",
        "The Bandit scan over the engine package and the shipped .py surface.",
    ),
    "test_security_net.py": (
        "security-net engine",
        "The four-member engine tree installed under two destination trees.",
    ),
    "test_security_stack.py": (
        "composed stack",
        "How the security modules compose when more than one is installed.",
    ),
    "test_security_verification.py": (
        "verification activation",
        "run_security_verification.py -- whether the shipped verification "
        "actually runs in an adopter tree.",
    ),
    "test_skills_security.py": (
        "skills read-path",
        "The skills fan-out symlink self-heal, which writes into the adopter's "
        "tree.",
    ),
    "test_web_hosting_security.py": (
        "web-hosting module",
        "Shipped module governing an adopter's hosting surface.",
    ),
}

#: A gate-integrity judgement recorded where it can be argued with.
#:
#: ``test_ast_attest.py``, ``test_reanchor.py`` and ``test_gate_reanchor.py``
#: test *gate integrity* rather than a security property of shipped code -- 232
#: tests between them.  They are members because the gate anchor is a
#: supply-chain control: it exists so an unattended actor cannot weaken the
#: check that governs it, which is a release-ceremony concern rather than a
#: per-change one.  The opposite reading -- that the per-change loop should stay
#: honest about its own gate -- is coherent, and removing these three from the
#: manifest is the whole change if it is preferred.
GATE_INTEGRITY_MEMBERS = frozenset({
    "test_ast_attest.py",
    "test_reanchor.py",
    "test_gate_reanchor.py",
})
