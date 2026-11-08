"""Every install receives a nine-lens reading aid, not only module teams.

The nine lenses as a reading aid, evidence and coverage rules, and concise falsification evidence
a clean code review must show used to live only in the `dual-review` module,
which installs for teams with two agent types. A solo team, and any team that did
not select the module, was asked for a coverage line it had never been shown.

They now sit in the review-loop document (`dev/agent_collaboration.md`), which
every install receives, under the heading "The review sweep" and ahead of the
scope-reduction trap that mirrors it. `AGENTS.md` carries a short pointer.

What is pinned, and why:

* **Through a real install, for every shipped profile.** The files an agent
  actually reads are the installed ones, so the check runs the scaffold CLI for
  each profile and reads what it wrote. A test that read only the template would
  stay green if an install path dropped or substituted the section.
* **The same obligations over both source copies.** The shipped file and Cairn's
  own copy must agree, so Cairn is bound by what it ships.
* **Nine lenses, in the doctrine's order, and no tenth.** A follower adds a
  sentence to one lens by its label, so the label and the count are an interface.
* **Evidence belongs in the review loop, not a second module.** The module
  supplies staffing guidance; repeatable probes stay in tests or scripts.
* **No reasoning from the doctrine leaks in.** The staged evidence bar, the
  going-through-the-motions signal and the do-not-telegraph rule are doctrine's
  reasoning; installed text states the rule, not the argument for it.
* **Body text, not a slot.** A slot is frozen at its first fill and never
  updates, so the roster would stop receiving upgrades.

Each obligation is an alternation matched against text with emphasis and code
markers removed and whitespace collapsed, so a rewording that keeps the
obligation passes and a deletion fails. Node IDs are the obligation labels,
never the patterns. Patterns are literals, not derived from the files they
check. A deliberate break (delete a lens, a coverage half, the scope sentence) is
made beside an unmutated control that must be green, and must turn a named check
red.

Run from the Cairn repo root:
    python -m pytest bootstrap/tests/test_review_sweep_ships.py
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
SCAFFOLD = CAIRN_ROOT / "bootstrap" / "scaffold.py"
PROFILES = sorted((CAIRN_ROOT / "bootstrap" / "profiles").glob("*.yml"))

SHIPPED_LOOP = "templates/core/dev/agent_collaboration.md"
OWN_LOOP = "dev/agent_collaboration.md"
SHIPPED_AGENTS = "templates/core/AGENTS.md"
OWN_AGENTS = "AGENTS.md"
_LOOP_FILES = (SHIPPED_LOOP, OWN_LOOP)
_AGENTS_FILES = (SHIPPED_AGENTS, OWN_AGENTS)
_FILE_IDS = {
    SHIPPED_LOOP: "shipped-loop", OWN_LOOP: "own-loop",
    SHIPPED_AGENTS: "shipped-agents", OWN_AGENTS: "own-agents",
}

_TRAP_OPENING = "The clean pass has a mirror: the scope-reduction trap"

#: label -> pattern. The nine lenses, in the doctrine's order and under its
#: names. A lens is written as where a review's evidence comes from.
_LENSES = {
    "lens-1-claims":
        r"1\. Claims — probe every load-bearing claim",
    "lens-2-production-path-exercised-by-tests":
        r"2\. Production path exercised by tests —",
    "lens-3-design-completeness":
        r"3\. Design completeness —",
    "lens-4-silent-failure-fail-closed":
        r"4\. Silent failure / fail-closed —",
    "lens-5-cross-document-consistency":
        r"5\. Cross-document consistency —",
    "lens-6-drift":
        r"6\. Drift —",
    "lens-7-lifecycle-process-placement":
        r"7\. Lifecycle / process placement —",
    "lens-8-domain-scientific-validity-and-scope":
        r"8\. Domain / scientific validity & scope —",
    "lens-9-name-the-satisfier":
        r"9\. Name the satisfier —",
}

#: label -> pattern, for the sweep section of a review-loop document.
_SWEEP_OBLIGATIONS = {
    **_LENSES,
    "a-clean-pass-is-treated-with-skepticism":
        r"A review that finds nothing on a complex change is treated with "
        r"skepticism, not relief",
    "the-roster-is-a-reading-aid-not-a-required-checklist":
        r"reading aid, not a required checklist or reporting format",
    "the-roster-does-not-require-lens-by-lens-reporting":
        r"without reporting every lens",
    "the-lenses-can-inform-review-stages":
        r"lenses can inform proposal, plan and code review",
    "cited-claims-name-evidence":
        r"A cited claim is credible only if it names the file path, test node, "
        r"line or command output",
    "a-bare-checked-is-an-incomplete-review":
        r"A bare .checked. is an incomplete review, not a pass",
    "coverage-line-covered-half":
        r"Covered — what the pass examined, with evidence for its answers",
    "coverage-line-not-covered-half":
        r"Not covered / low confidence — the negative space",
    "coverage-line-does-not-end-in-a-recommendation-for-more-review":
        r"does not end in a recommendation for more review",
    "the-reading-aid-does-not-downgrade-a-declared-tier":
        r"reading aid does not change or downgrade a declared required review tier",
    "a-project-adds-domain-probes":
        r"Projects may add probes for their domain and high-risk surfaces",
    "a-clean-code-review-shows-a-falsification-ledger":
        r"Code review tries to falsify the change",
    "ledger-surfaces-probed":
        r"Keep repeatable probes and mutation checks in tests or scripts",
    "ledger-negative-or-edge-case-attempt":
        r"When a claim says a value reaches every member of a set",
    "ledger-verification-run-or-consciously-not":
        r"Keep repeatable probes and mutation checks in tests or scripts",
    "ledger-residual-risk":
        r"names what remains uncertain",
    "ledger-mutation-when-a-claim-names-a-set":
        r"When a claim says a value reaches every member of a set",
    "ledger-mutation-summary-names-control-counts-and-exceptions":
        r"Report briefly whether the checks caught the breaks and whether any "
        r"mutation remains unresolved or unmeasured",
    "a-reviewer-who-tried-to-break-it-has-cleared-the-gate":
        r"A reviewer who tried to break the change and reports honestly that "
        r"they could not has cleared the gate; a reviewer who only read it "
        r"has not",
}

#: label -> pattern, for the pointer paragraph in `AGENTS.md`.
_POINTER_OBLIGATIONS = {
    "pointer-names-the-sweep-in-the-loop-document":
        r"dev/agent_collaboration\.md > .The review sweep.",
    "pointer-says-nine-lenses-are-a-reading-aid":
        r"nine-lens reading aid lives in dev/agent_collaboration\.md",
    "pointer-says-a-bare-checked-is-an-incomplete-review":
        r"[Aa] bare .checked. is an incomplete review",
    "pointer-says-the-coverage-line-names-what-was-not-covered":
        r"coverage line that ends the review says what the pass did not cover",
}

#: The pointer paragraph runs from its bold lead to the next blank line.
_POINTER_LEAD = "**Every review shows its evidence.**"

_PLAN_COMPLETION_SURFACES = {
    "AGENTS.md": {
        "patterns": {
            "agent-work-completes-the-plan":
                r"plan finishes after accepted agent-owned scope, required reviews",
            "human-operation-is-a-separate-board-wait":
                r"separate named standalone board wait with its owner and evidence",
            "no-human-operation-is-a-plan-chunk":
                r"Do not make a routine human-run trust or release operation a completion prerequisite",
            "pending-baseline-remains-unpassed":
                r"reviewed baseline awaiting a specifically named human operation remains unpassed",
            "functional-and-scientific-failures-stay-with-implementation":
                r"missing functional or scientific evidence, or required review remains implementation work",
            "integrity-failure-stays-with-implementation":
                r"unexplained integrity failure also remains implementation work, not a human operation",
            "archive-is-not-release-permission":
                r"Archive is not permission to activate or release",
            "fix-closes-at-fixing-commit":
                r"issue closes it at the fixing commit, not at release",
        },
        "mutation": ("integrity-failure-stays-with-implementation",
                     "An unexplained integrity failure"),
    },
    "dev/plans/_template.md": {
        "patterns": {
            "ready-to-archive-follows-agent-owned-delivery":
                r"plan reaches ready-to-archive after its agent-owned scope, required reviews, applicable checks and Boundary B are complete",
            "human-operation-is-a-separate-board-wait":
                r"separate, named standalone board wait with its owner, evidence and link to the implementation",
            "no-release-plan-or-human-final-chunk":
                r"not a routine human-run trust or release operation",
            "pending-operation-remains-unpassed":
                r"Keep its result unpassed until its evidence exists",
            "reviewed-baseline-remains-unpassed":
                r"reviewed baseline awaiting a specifically named human operation remains unpassed",
            "integrity-failure-stays-with-implementation":
                r"unexplained integrity failure remains implementation work",
            "failures-stay-with-implementation":
                r"Missing checks, defects and functional or scientific evidence stay in the implementation",
            "archive-is-not-release-permission":
                r"Archive is not permission to activate or release",
            "fix-closes-at-fixing-commit":
                r"issue closes at its fixing commit, not at release",
        },
        "mutation": ("failures-stay-with-implementation", "Missing checks, defects"),
    },
    "templates/core/dev/PLANNING.md": {
        "patterns": {
            "human-operation-has-evidence-and-owner":
                r"separate standalone waits, with an owner, evidence requirement and link to the completed implementation",
            "no-release-plan-or-human-final-chunk":
                r"They are not final plan chunks or a reason to open a release plan",
            "plans-finish-on-agent-owned-delivery":
                r"Plans finish after agent-owned scope, reviews and applicable checks, including change verification, are complete",
            "archive-is-not-release-permission":
                r"archive is not permission to activate or release",
            "pending-operation-remains-unpassed":
                r"Other outstanding operations remain blocked or unpassed until their evidence and authority exist",
            "reviewed-baseline-remains-unpassed":
                r"reviewed baseline awaiting a named human operation remains unpassed",
            "integrity-failure-stays-with-implementation":
                r"unexplained integrity failure remains implementation work",
        },
        "mutation": ("no-release-plan-or-human-final-chunk", "They are not final plan chunks"),
    },
    "docs/methodology/lifecycle.md": {
        "patterns": {
            "agent-owned-delivery-completes-the-plan":
                r"plan finishes when its accepted agent-owned scope, required reviews, applicable checks and change verification are complete",
            "human-operation-is-a-separate-roadmap-wait":
                r"separately in a named standalone roadmap wait with its owner, evidence requirement and link to the implementation",
            "no-release-plan-or-new-workflow":
                r"existing board mechanism, not a release plan or new workflow",
            "pending-operation-remains-unpassed":
                r"remains blocked or unpassed until its own evidence and authority exist",
            "failures-stay-with-implementation":
                r"defect, failed check, missing functional or scientific evidence, required review, or unexplained integrity failure remains implementation work",
            "baseline-is-not-green":
                r"reviewed baseline awaiting a specifically named human operation remains unpassed, not failed or green",
            "permission-stops-remain":
                r"Decision, scope and unexpected-boundary stops remain with the Maintainer",
            "archive-is-not-release-permission":
                r"does not authorize activation or release",
            "fix-closes-at-fixing-commit":
                r"issue is closed by its fixing commit, not by a later release",
        },
        "mutation": ("failures-stay-with-implementation", "A defect, failed check"),
    },
    "docs/methodology/plans.md": {
        "patterns": {
            "agent-owned-delivery-completes-the-plan":
                r"plan reaches ready-to-archive when accepted agent-owned scope, required reviews, applicable checks and change verification are complete",
            "human-operation-is-a-separate-roadmap-wait":
                r"separate named standalone roadmap wait with its owner, evidence requirement and link to the implementation",
            "no-release-plan":
                r"do not create a release plan",
            "pending-operation-remains-unpassed":
                r"operation remains blocked or unpassed until its own evidence and authority exist",
            "failures-stay-with-implementation":
                r"Do not move a defect, failed check, missing functional or scientific evidence, required review, or unexplained integrity failure to a human wait",
            "baseline-is-not-green":
                r"reviewed baseline awaiting a specifically named human operation remains unpassed, not failed or green",
            "permission-stops-remain":
                r"Decision, scope and unexpected-boundary stops remain with the Maintainer",
            "archive-is-not-release-permission":
                r"Archiving does not authorize activation or release",
            "fix-closes-at-fixing-commit":
                r"issue closes at its fixing commit, not at a later release",
        },
        "mutation": ("failures-stay-with-implementation", "Do not move a defect"),
    },
}

# New accepted finish and reading duties. Keep a separate literal and mutation
# per source copy: source parity alone would not catch an omission from both
# installed instructions or from a published method description.
_READABLE_WORK_RULES = {
    "AGENTS.md": {
        "finish-records-at-commit": (
            r"At the commit or archive that finishes work, update applicable roadmap and changelog records",
            "At the commit or archive that finishes work"),
        "session-end-checks-omissions": (
            r"Do not defer those entries to session end; the session-end routine checks for omissions",
            "Do not defer those entries to session end"),
        "assigned-tier-chunks-are-specified": (
            r"Plan review checks whether each chunk is specified for its assigned model tier without asking the implementer to make design decisions",
            "Plan review checks whether each chunk is specified"),
        "plan-review-returns-missing-design": (
            r"Name missing design in the existing three answers and return the chunk to its author for repair",
            "Name missing design in the existing three answers"),
        "cheap-follow-up-definition": (
            r"cheap follow-ups mean a few person-steps, no new Decision or public name beyond the plan, and a test in existing test files",
            "cheap follow-ups mean a few person-steps"),
        "cheap-follow-ups-fixed-or-authorized-deferral": (
            r"Code review identifies cheap findings and advice; before archive the response fixes each or uses an existing deferral reason with the Maintainer's verbatim authorization",
            "Code review identifies cheap findings and advice"),
        "cheapness-does-not-waive-checks": (
            r"Cheapness grants no scope, boundary or check waiver",
            "Cheapness grants no scope"),
        "non-cheap-advice-keeps-disposition": (
            r"Non-cheap advice keeps its existing disposition",
            "Non-cheap advice keeps its existing disposition"),
        "failed-required-check-stays-implementation-work": (
            r"Required failed checks remain implementation work",
            "Required failed checks remain implementation work"),
    },
    "templates/core/AGENTS.md": {
        "finish-records-at-commit": (
            r"At the commit or archive that finishes work, update applicable roadmap and changelog records",
            "At the commit or archive that finishes work"),
        "session-end-checks-omissions": (
            r"Do not defer those entries to session end; the session-end routine checks for omissions",
            "Do not defer those entries to session end"),
        "assigned-tier-chunks-are-specified": (
            r"Plan review checks whether each chunk is specified for its assigned model tier without asking the implementer to make design decisions",
            "Plan review checks whether each chunk is specified"),
        "plan-review-returns-missing-design": (
            r"Name missing design in the existing three answers and return the chunk to its author for repair",
            "Name missing design in the existing three answers"),
        "cheap-follow-up-definition": (
            r"cheap follow-ups mean a few person-steps, no new Decision or public name beyond the plan, and a test in existing test files",
            "cheap follow-ups mean a few person-steps"),
        "cheap-follow-ups-fixed-or-authorized-deferral": (
            r"Code review identifies cheap findings and advice; before archive the response fixes each or uses an existing deferral reason with the Maintainer's verbatim authorization",
            "Code review identifies cheap findings and advice"),
        "cheapness-does-not-waive-checks": (
            r"Cheapness grants no scope, boundary or check waiver",
            "Cheapness grants no scope"),
        "non-cheap-advice-keeps-disposition": (
            r"Non-cheap advice keeps its existing disposition",
            "Non-cheap advice keeps its existing disposition"),
        "failed-required-check-stays-implementation-work": (
            r"Required failed checks remain implementation work",
            "Required failed checks remain implementation work"),
    },
    "dev/agent_collaboration.md": {
        "proposal-cold-read": (
            r"For a proposal, read its title, one-line summary and Decision summary before the body or code",
            "For a proposal, read its title"),
        "proposal-gist-and-finding": (
            r"State the gist in one or two sentences; if understanding the top depends on the body, name that as a finding",
            "State the gist in one or two sentences"),
        "proposal-author-rereads-top": (
            r"After every proposal revision, the author rereads the top and revises it as a whole",
            "After every proposal revision"),
        "assigned-tier-chunks-are-specified": (
            r"Plan reviews use the same three questions to check whether every chunk can be executed at its assigned tier without implementer design decisions",
            "Plan reviews use the same three questions"),
        "plan-review-returns-missing-design": (
            r"Identify missing specification in the review and return it to the plan author",
            "Identify missing specification in the review"),
        "reviewer-disposes-non-cheap-advice": (
            r"Authors dispose of non-cheap advice in one line each",
            "Authors dispose of non-cheap advice"),
    },
    "templates/core/dev/agent_collaboration.md": {
        "proposal-cold-read": (
            r"For a proposal, read its title, one-line summary and Decision summary before the body or code",
            "For a proposal, read its title"),
        "proposal-gist-and-finding": (
            r"State the gist in one or two sentences; if understanding the top depends on the body, name that as a finding",
            "State the gist in one or two sentences"),
        "proposal-author-rereads-top": (
            r"After every proposal revision, the author rereads the top and revises it as a whole",
            "After every proposal revision"),
        "assigned-tier-chunks-are-specified": (
            r"Plan reviews use the same three questions to check whether every chunk can be executed at its assigned tier without implementer design decisions",
            "Plan reviews use the same three questions"),
        "plan-review-returns-missing-design": (
            r"Identify missing specification in the review and return it to the plan author",
            "Identify missing specification in the review"),
        "reviewer-disposes-non-cheap-advice": (
            r"Authors dispose of non-cheap advice in one line each",
            "Authors dispose of non-cheap advice"),
    },
    "dev/plans/_template.md": {
        "cheap-follow-up-definition": (
            r"Cheap follow-ups mean a few person-steps, no new Decision or public name beyond the plan, and a test that fits existing test files",
            "Cheap follow-ups mean a few person-steps"),
        "cheap-defect-exception-stays-narrow": (
            r"This is not the narrower cheap defect-fix exception in AGENTS.md",
            "not the narrower cheap defect-fix exception"),
        "cheap-follow-ups-fixed-or-authorized-deferral": (
            r"Code review identifies cheap findings and advice; in the code-review response, fix each before archive or use an existing deferral reason with the Maintainer's verbatim authorization",
            "Code review identifies cheap findings and advice"),
        "cheapness-does-not-waive-checks": (
            r"Cheapness grants no scope, boundary or required-check waiver",
            "Cheapness grants no scope"),
        "non-cheap-advice-keeps-disposition": (
            r"Non-cheap advice keeps its existing disposition",
            "Non-cheap advice keeps its existing disposition"),
        "failed-required-check-stays-implementation-work": (
            r"a required failed check remains implementation work",
            "a required failed check remains implementation work"),
    },
    "templates/core/dev/plans/_template.md": {
        "cheap-follow-up-definition": (
            r"Cheap follow-ups mean a few person-steps, no new Decision or public name beyond the plan, and a test that fits existing test files",
            "Cheap follow-ups mean a few person-steps"),
        "cheap-defect-exception-stays-narrow": (
            r"This is not the narrower cheap defect-fix exception in AGENTS.md",
            "not the narrower cheap defect-fix exception"),
        "cheap-follow-ups-fixed-or-authorized-deferral": (
            r"Code review identifies cheap findings and advice; in the code-review response, fix each before archive or use an existing deferral reason with the Maintainer's verbatim authorization",
            "Code review identifies cheap findings and advice"),
        "cheapness-does-not-waive-checks": (
            r"Cheapness grants no scope, boundary or required-check waiver",
            "Cheapness grants no scope"),
        "non-cheap-advice-keeps-disposition": (
            r"Non-cheap advice keeps its existing disposition",
            "Non-cheap advice keeps its existing disposition"),
        "failed-required-check-stays-implementation-work": (
            r"a required failed check remains implementation work",
            "a required failed check remains implementation work"),
    },
    "docs/methodology/proposals.md": {
        "proposal-cold-read": (
            r"Before the body or code, the reviewer reads the title, one-line summary and Decision summary",
            "Before the body or code"),
        "proposal-gist-and-finding": (
            r"then states the gist in one or two sentences. If the body is needed to understand the top, name that dependence as a finding",
            "then states the gist in one or two sentences"),
        "proposal-author-rereads-top": (
            r"After each revision, the author rereads the top and revises it as a whole",
            "After each revision"),
    },
    "docs/methodology/plans.md": {
        "assigned-tier-chunks-are-specified": (
            r"check that each chunk has enough design for its assigned model tier to execute without the implementer making design decisions",
            "check that each chunk has enough design"),
        "plan-review-returns-missing-design": (
            r"Name any missing specification and return the chunk to its author",
            "Name any missing specification"),
        "cheap-follow-up-definition": (
            r"A cheap follow-up is a few person-steps, needs no new Decision or public name beyond the plan, and has a test that fits existing test files",
            "A cheap follow-up is a few person-steps"),
        "cheap-follow-ups-fixed-or-authorized-deferral": (
            r"the author fixes each in the response before archive or uses an existing deferral reason with the Maintainer's verbatim authorization",
            "the author fixes each in the response"),
        "cheapness-does-not-waive-checks": (
            r"Cheapness grants no scope, boundary or required-check waiver",
            "Cheapness grants no scope"),
        "non-cheap-advice-keeps-disposition": (
            r"Non-cheap advice retains its existing disposition",
            "Non-cheap advice retains its existing disposition"),
        "failed-required-check-stays-implementation-work": (
            r"Required failed checks remain implementation work",
            "Required failed checks remain implementation work"),
    },
    "docs/methodology/session-routines.md": {
        "finish-records-at-commit": (
            r"Applicable roadmap and changelog entries belong at the commit or archive that finishes work",
            "Applicable roadmap and changelog entries belong"),
        "session-end-checks-omissions": (
            r"The session-end routine checks for omissions; it is not the normal time to rebuild entries due earlier",
            "The session-end routine checks for omissions"),
    },
    "templates/skills/session-end/SKILL.md": {
        "finish-records-at-commit": (
            r"Check that applicable roadmap and changelog entries were made at the commit or archive that finished the work",
            "Check that applicable roadmap and changelog entries"),
        "session-end-checks-omissions": (
            r"Session end checks for omissions; it is not the normal time to reconstruct entries that were due earlier",
            "Session end checks for omissions"),
    },
    ".agents/skills/session-end/SKILL.md": {
        "finish-records-at-commit": (
            r"Check that applicable roadmap and changelog entries were made at the commit or archive that finished the work",
            "Check that applicable roadmap and changelog entries"),
        "session-end-checks-omissions": (
            r"Session end checks for omissions; it is not the normal time to reconstruct entries that were due earlier",
            "Session end checks for omissions"),
    },
}

# The local AST disposition below is deliberately absent from the shipped copy.
_PLAN_COMPLETION_SURFACES["templates/core/AGENTS.md"] = {
    "patterns": dict(_PLAN_COMPLETION_SURFACES["AGENTS.md"]["patterns"]),
    "mutation": _PLAN_COMPLETION_SURFACES["AGENTS.md"]["mutation"],
}
_PLAN_COMPLETION_SURFACES["AGENTS.md"]["patterns"][
    "expected-ast-mismatch-is-release-only"] = (
        r"verified expected AST mismatch from reviewed planned engine changes "
        r"remains unpassed until the separate release baseline operation, "
        r"but alone does not block plan archive")
_PLAN_COMPLETION_SURFACES["AGENTS.md"]["patterns"][
    "unexpected-ast-drift-stays-implementation-work"] = (
        r"Unexpected AST drift remains implementation work")
_PLAN_COMPLETION_SURFACES["templates/core/dev/plans/_template.md"] = \
    _PLAN_COMPLETION_SURFACES["dev/plans/_template.md"]

_SMART_GOAL_SURFACES = {
    "AGENTS.md": {
        "patterns": {
            "scope-names-result-and-relevance":
                r"specific result and why it matters to the accepted objective",
            "criteria-make-delivery-observable":
                r"Acceptance criteria make delivery observable",
            "sequence-shows-capability-and-window":
                r"available capabilities and prerequisites.{0,90}realistic work-window estimate with uncertainty",
            "independently-finishable-without-splitting":
                r"independently finishable outcome.{0,120}do not wait on another unfinished plan",
            "proposal-retains-queued-outcomes":
                r"proposal may retain several outcomes across plans.{0,180}source and revival condition",
            "no-human-only-final-task":
                r"routine human-run trust or release operation a completion prerequisite or a final plan chunk",
        },
        "mutations": {
            "independent": "independently finishable outcome",
            "human": "final plan chunk",
        },
    },
    "dev/proposals/_template.md": {
        "patterns": {
            "proposal-names-outcomes-and-prerequisites":
                r"State each useful delivery outcome, its prerequisites and intended release or capability",
            "queued-work-retains-source-and-revival":
                r"existing board with this source and a condition for reviving each one",
            "independently-finishable-without-splitting":
                r"independently finishable outcome.{0,120}must not wait on another unfinished plan",
            "no-human-only-final-task":
                r"routine human operations as separately owned, evidenced waits, never as final plan tasks",
        },
        "mutations": {
            "independent": "must not wait on another unfinished plan",
            "human": "final plan tasks",
        },
    },
    "dev/plans/_template.md": {
        "patterns": {
            "scope-names-result-and-relevance":
                r"specific useful result and why it advances the accepted objective",
            "independently-finishable-without-splitting":
                r"coherent outcome whose implementation, required evidence, reviews and archive finish without another unfinished plan",
            "sequence-shows-capability-and-window":
                r"capabilities and prerequisites available to this plan.{0,120}realistic work-window estimate and name material uncertainty",
            "unavailable-goal-stays-queued":
                r"unavailable future plan stays queued on the existing board with its proposal source and revival condition",
            "criteria-measure-outcome":
                r"completion observable against the useful result in Scope",
            "no-human-only-final-task":
                r"routine human-run trust or release operation.{0,80}final plan chunk",
        },
        "mutations": {
            "independent": ["finish without another unfinished plan",
                             "another plan's future review"],
            "human": "final plan chunk",
        },
    },
    "docs/methodology/proposals.md": {
        "patterns": {
            "proposal-names-outcomes-and-prerequisites":
                r"name each useful delivery outcome, its prerequisites and intended release or capability",
            "queued-work-retains-source-and-revival":
                r"later outcomes queued on the existing board with their immutable source and a condition for revival",
            "independently-finishable-without-splitting":
                r"each plan's implementation, required checks, reviews and archive finish without another unfinished plan",
            "no-human-only-final-task":
                r"human-operation waits.{0,80}not final plan tasks",
        },
        "mutations": {
            "independent": "finish without another unfinished plan",
            "human": "not final plan tasks",
        },
    },
    "docs/methodology/plans.md": {
        "patterns": {
            "scope-names-result-and-relevance":
                r"Scope names the specific result and why it matters to the accepted objective",
            "criteria-make-delivery-observable":
                r"Acceptance criteria make completion observable",
            "sequence-shows-capability-and-window":
                r"Sequence shows available capabilities and prerequisites.{0,100}realistic work-window estimate with uncertainty",
            "independently-finishable-without-splitting":
                r"independently finishable.{0,140}finish without another unfinished plan",
            "no-human-only-final-task":
                r"routine human-run trust or release operation is not a final plan chunk or a condition of completion",
        },
        "mutations": {
            "independent": "finish without another unfinished plan",
            "human": "not a final plan chunk",
        },
    },
    "docs/methodology/lifecycle.md": {
        "patterns": {
            "scope-names-result-and-relevance":
                r"Scope states the specific result and its relevance to the accepted objective",
            "criteria-make-delivery-observable":
                r"Acceptance criteria state observable evidence",
            "sequence-shows-capability-and-window":
                r"available capabilities and prerequisites.{0,120}realistic work-window estimate and uncertainty",
            "independently-finishable-without-splitting":
                r"finish without another unfinished plan",
            "proposal-retains-queued-outcomes":
                r"proposal may carry several outcomes into later plans.{0,120}source and revival condition",
            "no-human-only-final-task":
                r"routine human-run trust or release operation its final chunk or a prerequisite",
        },
        "mutations": {
            "independent": "finish without another unfinished plan",
            "human": "final chunk",
        },
    },
}

_SMART_GOAL_SURFACES["templates/core/AGENTS.md"] = \
    _SMART_GOAL_SURFACES["AGENTS.md"]
_SMART_GOAL_SURFACES["templates/core/dev/proposals/_template.md"] = \
    _SMART_GOAL_SURFACES["dev/proposals/_template.md"]
_SMART_GOAL_SURFACES["templates/core/dev/plans/_template.md"] = \
    _SMART_GOAL_SURFACES["dev/plans/_template.md"]

_SMART_GOAL_IDS = {path: path.replace("/", "-") for path in _SMART_GOAL_SURFACES}
_INSTALLED_SMART_GOALS = {
    "AGENTS.md": "templates/core/AGENTS.md",
    "dev/proposals/_template.md": "templates/core/dev/proposals/_template.md",
    "dev/plans/_template.md": "templates/core/dev/plans/_template.md",
}

_INSTALLED_PLAN_COMPLETION = {
    "AGENTS.md": "AGENTS.md",
    "dev/plans/_template.md": "dev/plans/_template.md",
    "dev/PLANNING.md": "dev/PLANNING.md",
}

_INSTALLED_PLAN_COMPLETION_SOURCES = {
    "AGENTS.md": "templates/core/AGENTS.md",
    "dev/plans/_template.md": "templates/core/dev/plans/_template.md",
    "dev/PLANNING.md": "templates/core/dev/PLANNING.md",
}

def _missing_completion(text: str, patterns: dict[str, str]) -> list[str]:
    normalized = _normalize(text)
    return [label for label, pattern in patterns.items()
            if not re.search(pattern, normalized, re.I)]


@pytest.mark.parametrize("rel", sorted(_SMART_GOAL_SURFACES),
                         ids=lambda rel: _SMART_GOAL_IDS[rel])
def test_source_smart_goal_guidance(rel: str) -> None:
    text = _text(rel)
    missing = _missing_completion(text, _SMART_GOAL_SURFACES[rel]["patterns"])
    assert not missing, f"{rel} lost SMART-goal guidance: {missing}"


@pytest.mark.parametrize("mutation", ("independent", "human"))
def test_source_smart_goal_mutations_fail_entrypoint(
        tmp_path: Path, mutation: str) -> None:
    roots: dict[str, str] = {}
    for rel, spec in _SMART_GOAL_SURFACES.items():
        source = (CAIRN_ROOT / rel).read_text(encoding="utf-8")
        anchors = spec["mutations"][mutation]
        if not isinstance(anchors, list):
            anchors = [anchors]
        if mutation == "human":
            mutant = _replace_sentence(
                source, anchors[0],
                "A routine human-run operation may be the final plan task.")
        else:
            mutant = source
            for anchor in anchors:
                mutant = _delete_sentence(mutant, anchor)
        root = tmp_path / _SMART_GOAL_IDS[rel]
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(mutant, encoding="utf-8")
        roots[rel] = str(root)

    env = os.environ.copy()
    env["CAIRN_SMART_SOURCE_ROOTS"] = json.dumps(roots)
    result = subprocess.run(
        [sys.executable, "-m", "pytest",
         f"{Path(__file__)}::test_source_smart_goal_guidance", "-q"],
        cwd=CAIRN_ROOT, env=env, capture_output=True, text=True, check=False,
        stdin=subprocess.DEVNULL)
    assert result.returncode != 0, "source surface mutations survived"
    assert f"{len(_SMART_GOAL_SURFACES)} failed" in result.stdout, (
        "not every independently mutated source surface failed its owning "
        f"entry point:\n{result.stdout}\n{result.stderr}")


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
@pytest.mark.parametrize("surface", sorted(_INSTALLED_SMART_GOALS))
def test_installed_smart_goal_guidance(
        installs: dict[str, Path], profile: Path, surface: str) -> None:
    roots = json.loads(os.environ.get("CAIRN_SMART_INSTALLED_ROOTS", "{}"))
    key = f"{profile.stem}::{surface}"
    root = Path(roots[key]) if key in roots else installs[profile.stem]
    text = (root / surface).read_text(encoding="utf-8")
    source = _INSTALLED_SMART_GOALS[surface]
    missing = _missing_completion(text, _SMART_GOAL_SURFACES[source]["patterns"])
    assert not missing, (
        f"{profile.stem} installed {surface} lost SMART-goal guidance: {missing}")


@pytest.mark.parametrize("mutation", ("independent", "human"))
def test_installed_smart_goal_mutations_fail_entrypoint(
        installs: dict[str, Path], tmp_path: Path, mutation: str) -> None:
    roots: dict[str, str] = {}
    expected = len(PROFILES) * len(_INSTALLED_SMART_GOALS)
    for profile in PROFILES:
        for surface, source in _INSTALLED_SMART_GOALS.items():
            original_root = installs[profile.stem]
            clone_root = tmp_path / f"{profile.stem}-{surface.replace('/', '-') }"
            shutil.copytree(original_root, clone_root)
            target = clone_root / surface
            text = target.read_text(encoding="utf-8")
            anchors = _SMART_GOAL_SURFACES[source]["mutations"][mutation]
            if not isinstance(anchors, list):
                anchors = [anchors]
            if mutation == "human":
                mutant = _replace_sentence(
                    text, anchors[0],
                    "A routine human-run operation may be the final plan task.")
            else:
                mutant = text
                for anchor in anchors:
                    mutant = _delete_sentence(mutant, anchor)
            target.write_text(mutant, encoding="utf-8")
            roots[f"{profile.stem}::{surface}"] = str(clone_root)

    env = os.environ.copy()
    env["CAIRN_SMART_INSTALLED_ROOTS"] = json.dumps(roots)
    result = subprocess.run(
        [sys.executable, "-m", "pytest",
         f"{Path(__file__)}::test_installed_smart_goal_guidance", "-q"],
        cwd=CAIRN_ROOT, env=env, capture_output=True, text=True, check=False,
        stdin=subprocess.DEVNULL)
    assert result.returncode != 0, "installed surface mutations survived"
    assert f"{expected} failed" in result.stdout, (
        "not every independently mutated installed surface failed its owning "
        f"entry point:\n{result.stdout}\n{result.stderr}")


@pytest.mark.parametrize("rel", sorted(_PLAN_COMPLETION_SURFACES))
def test_source_plan_completion_rule_and_surface_mutation(rel: str) -> None:
    text = _text(rel)
    spec = _PLAN_COMPLETION_SURFACES[rel]
    assert _missing_completion(text, spec["patterns"]) == [], rel
    label, anchor = spec["mutation"]
    mutant = _delete_sentence(text, anchor)
    assert label in _missing_completion(mutant, spec["patterns"]), rel


def test_expected_ast_mismatch_disposition_is_cairn_local() -> None:
    local = _normalize(_text("AGENTS.md"))
    shipped = _normalize(_text("templates/core/AGENTS.md"))
    assert "expected-ast-mismatch-is-release-only" not in _missing_completion(
        local, _PLAN_COMPLETION_SURFACES["AGENTS.md"]["patterns"])
    assert "Unexpected AST drift remains implementation work" in local
    assert "verified expected AST mismatch from reviewed planned engine changes" \
        not in shipped


def _normalize(text: str) -> str:
    """Drop blockquote, emphasis and code markers; collapse whitespace."""
    text = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)
    text = text.replace("*", "").replace("`", "")
    return " ".join(text.split())

_LEGACY_INVENTORY_REQUIREMENT = re.compile(
    r"\b(?:code review (?:includes|carries|shows|requires) a "
    r"falsification ledger|clean code review (?:shows|carries) a "
    r"falsification ledger|ledger of five items|falsification ledger.{0,60}five items|"
    r"falsification ledger in code review|falsification ledger has "
    r"one line per probe|one line per probe|points? (?:at|to) the "
    r"falsification ledger|mutation summaries? name the unmutated control|"
    r"unmutated control.{0,120}each survivor)\b",
    re.IGNORECASE,
)


def _has_legacy_inventory_requirement(text: str) -> bool:
    return bool(_LEGACY_INVENTORY_REQUIREMENT.search(_normalize(text)))


def _text(rel: str) -> str:
    roots = json.loads(os.environ.get("CAIRN_SMART_SOURCE_ROOTS", "{}"))
    return (Path(roots.get(rel, CAIRN_ROOT)) / rel).read_text(encoding="utf-8")


def _sweep(text: str) -> str:
    """The raw text of the sweep: its heading to the scope-reduction trap."""
    start = re.search(r"^## The review sweep$", text, re.M)
    assert start, "no '## The review sweep' heading"
    end = text.find(f"**{_TRAP_OPENING}", start.end())
    assert end != -1, "the scope-reduction trap does not follow the sweep"
    return text[start.start():end]


def _pointer(text: str) -> str:
    """The pointer paragraph in the Review section of an `AGENTS.md`."""
    section = re.search(r"^## Review$(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert section, "no '## Review' section"
    body = section.group(1)
    lead = body.find(_POINTER_LEAD)
    assert lead != -1, "no pointer paragraph in Review"
    return body[lead:].split("\n\n", 1)[0]


def _missing(text: str, obligations: dict[str, str]) -> list[str]:
    normalized = _normalize(text)
    return [label for label, pattern in obligations.items()
            if not re.search(pattern, normalized)]


def _delete_sentence(text: str, anchor: str) -> str:
    """Delete the sentence containing the literal *anchor* (not a pattern)."""
    flat = " ".join(text.split())
    at = flat.find(anchor)
    assert at != -1, f"anchor {anchor!r} not found; the control is stale"
    start = max(flat.rfind(". ", 0, at) + 2, 0)
    end = flat.find(". ", at)
    end = len(flat) if end == -1 else end + 2
    return flat[:start] + flat[end:]


_READABLE_WORK_CASES = [
    (rel, label)
    for rel, obligations in _READABLE_WORK_RULES.items()
    for label in obligations
]


def _assert_readable_work_obligation(root: Path, rel: str, label: str) -> None:
    pattern, _ = _READABLE_WORK_RULES[rel][label]
    text = (root / rel).read_text(encoding="utf-8")
    missing = _missing_completion(text, {label: pattern})
    assert not missing, f"{root / rel} lost {label}: {missing}"


def _copy_readable_member(source_root: Path, rel: str, target_root: Path) -> Path:
    """Make a physical, isolated copy of one named instruction member."""
    source = source_root / rel
    target = target_root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return target


_INSTALLED_READABLE_WORK_SURFACES = {
    "AGENTS.md": "templates/core/AGENTS.md",
    "dev/agent_collaboration.md": "templates/core/dev/agent_collaboration.md",
    ".agents/skills/session-end/SKILL.md": "templates/skills/session-end/SKILL.md",
}
_INSTALLED_READABLE_WORK_CASES = [
    (dest, source, label)
    for dest, source in _INSTALLED_READABLE_WORK_SURFACES.items()
    for label in _READABLE_WORK_RULES[source]
]


@pytest.mark.parametrize("dest,source,label", _INSTALLED_READABLE_WORK_CASES,
                         ids=[f"{dest}-{label}" for dest, source, label
                              in _INSTALLED_READABLE_WORK_CASES])
@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
def test_installed_readable_work_obligation_and_mutation(
        installs: dict[str, Path], profile: Path, dest: str,
        source: str, label: str, tmp_path: Path) -> None:
    installed_root = installs[profile.stem]
    control_root = tmp_path / "control"
    control_file = _copy_readable_member(installed_root, dest, control_root)
    assert control_file.is_file()
    _assert_readable_work_obligation(control_root, dest, label)

    mutant_root = tmp_path / "mutant"
    mutant_file = _copy_readable_member(control_root, dest, mutant_root)
    _, anchor = _READABLE_WORK_RULES[source][label]
    mutant_file.write_text(
        _delete_sentence(mutant_file.read_text(encoding="utf-8"), anchor),
        encoding="utf-8",
    )
    assert mutant_file.read_text(encoding="utf-8") != control_file.read_text(
        encoding="utf-8")
    with pytest.raises(AssertionError, match=rf"lost {re.escape(label)}"):
        _assert_readable_work_obligation(mutant_root, dest, label)


def _replace_sentence(text: str, anchor: str, replacement: str) -> str:
    flat = " ".join(text.split())
    at = flat.find(anchor)
    assert at != -1, f"anchor {anchor!r} not found; the control is stale"
    start = max(flat.rfind(". ", 0, at) + 2, 0)
    end = flat.find(". ", at)
    end = len(flat) if end == -1 else end + 2
    return flat[:start] + replacement + " " + flat[end:]


def _delete_between(text: str, first: str, last: str) -> str:
    """Delete from the literal *first* up to, not including, the literal *last*."""
    flat = " ".join(text.split())
    a = flat.find(first)
    b = flat.find(last, a)
    assert a != -1 and b != -1, "anchors not found; the control is stale"
    return flat[:a] + flat[b:]


# --------------------------------------------------------------------------
# The two source copies of the review-loop document.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_the_sweep_precedes_the_scope_reduction_trap(rel: str) -> None:
    """The trap opens by calling itself the mirror of the clean pass."""
    text = _text(rel)
    heading = re.search(r"^## The review sweep$", text, re.M)
    assert heading, f"{rel} has no 'The review sweep' heading"
    trap = text.find(f"**{_TRAP_OPENING}.**")
    assert trap != -1, f"{rel} lost the scope-reduction trap opening"
    assert heading.start() < trap, (
        f"{rel}: the sweep follows the trap, so 'the mirror' has no referent.")


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_the_lens_roster_is_exactly_nine_in_the_doctrines_order(rel: str) -> None:
    sweep = _normalize(_sweep(_text(rel)))
    positions = []
    for label, pattern in _LENSES.items():
        found = re.search(pattern, sweep)
        assert found, f"{rel} lost {label!r}"
        positions.append(found.start())
    assert positions == sorted(positions), f"{rel}: the lenses are out of order"
    numbered = re.findall(r"(?m)^(\d+)\. ", _sweep(_text(rel)))
    assert numbered == [str(n) for n in range(1, 10)], (
        f"{rel} lists lenses {numbered}; the roster is exactly nine and a "
        f"follower pins nine.")


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_the_anchors_a_follower_writes_against_are_present(rel: str) -> None:
    """Later work adds a sentence to a lens by its label, and to the sentence
    that says a finding is blocking or not, so all three are an interface:
    the sweep heading, the lens label, and that sentence, unchanged.
    """
    text = _text(rel)
    assert "Cross-document consistency" in _sweep(text)
    assert ("A finding is blocking or non-blocking, and says what evidence "
            "would close it.") in _normalize(text)


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_the_ledger_is_defined_once_with_five_items(rel: str) -> None:
    text = _text(rel)
    sweep = _normalize(_sweep(text))
    assert "code review tries to falsify the change" in sweep.lower()
    assert "keep repeatable probes and mutation checks in tests or scripts" in sweep.lower()
    assert not _has_legacy_inventory_requirement(text), rel


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_the_sweep_leaves_the_doctrines_reasoning_out(rel: str) -> None:
    sweep = _sweep(_text(rel))
    leaked = re.findall(r"telegraph|ritual|evidence bar is staged", sweep, re.I)
    assert not leaked, (
        f"{rel}: the sweep restates doctrine reasoning {leaked}. Installed "
        f"text states the rule; the argument for it stays in the doctrine.")


def test_the_leak_pattern_matches_the_doctrine_it_guards_against() -> None:
    """Confirm the instrument: it reads above zero where the reasoning lives."""
    doctrine = _text("docs/methodology/dual-review.md")
    assert re.findall(r"telegraph|ritual|evidence bar is staged", doctrine, re.I)
    assert not re.findall(r"telegraph|ritual|evidence bar is staged",
                          _sweep(_text(SHIPPED_LOOP)), re.I)


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_the_sweep_is_body_text_not_a_slot(rel: str) -> None:
    """A slot is frozen at its first fill, so the roster would stop updating."""
    assert "cairn:" not in _sweep(_text(rel))


# --------------------------------------------------------------------------
# The pointer in both AGENTS.md copies.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
@pytest.mark.parametrize("label", sorted(_POINTER_OBLIGATIONS))
def test_agents_md_pointer_carries_the_obligation(label: str, rel: str) -> None:
    assert label not in _missing(_pointer(_text(rel)), _POINTER_OBLIGATIONS), (
        f"{rel} lost {label!r} from the pointer. The full text lives in the "
        f"review-loop document; this is how an agent that reads only "
        f"AGENTS.md finds it.")


@pytest.mark.parametrize("rel", _AGENTS_FILES, ids=_FILE_IDS.get)
def test_the_pointer_names_no_test_path(rel: str) -> None:
    """A shipped file must not name a Cairn-only path (the boundaries test)."""
    assert _missing(_pointer(_text(rel)), _POINTER_OBLIGATIONS) == []
    assert "bootstrap/tests" not in _pointer(_text(rel))


# --------------------------------------------------------------------------
# Through a real install, for every shipped profile.
# --------------------------------------------------------------------------

@pytest.fixture(scope="session")
def installs(tmp_path_factory) -> dict[str, Path]:
    """Install each shipped profile once; return profile stem -> target tree.

    The profiles are globbed, so one added later is installed and checked
    without editing this file; the three that ship today must be among them,
    or a broken glob would pass by checking nothing.
    """
    if os.environ.get("CAIRN_SMART_INSTALLED_ROOTS"):
        return {}
    assert {"solo-greenfield", "collaborative-team",
            "high-rigor-legacy"} <= {p.stem for p in PROFILES}
    out: dict[str, Path] = {}
    for profile in PROFILES:
        target = tmp_path_factory.mktemp(f"install-{profile.stem}")
        result = subprocess.run(
            [sys.executable, str(SCAFFOLD), "--config", str(profile),
             "--target", str(target)],
            capture_output=True, text=True, check=False,
            stdin=subprocess.DEVNULL,
        )
        assert result.returncode == 0, (
            f"installing {profile.name} exited {result.returncode}:\n"
            f"{result.stderr}")
        out[profile.stem] = target
    return out


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
@pytest.mark.parametrize("label", sorted(_SWEEP_OBLIGATIONS))
def test_installed_loop_document_carries_the_obligation(
        installs: dict[str, Path], profile: Path, label: str) -> None:
    text = (installs[profile.stem] / "dev" / "agent_collaboration.md").read_text(
        encoding="utf-8")
    assert not _has_legacy_inventory_requirement(text), profile.stem
    assert label not in _missing(_sweep(text), _SWEEP_OBLIGATIONS), (
        f"a {profile.stem} install lacks {label!r}. Everyone should get the "
        f"review sweep, whatever modules they selected.")


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
@pytest.mark.parametrize("label", sorted(_POINTER_OBLIGATIONS))
def test_installed_agents_md_carries_the_pointer(
        installs: dict[str, Path], profile: Path, label: str) -> None:
    text = (installs[profile.stem] / "AGENTS.md").read_text(encoding="utf-8")
    assert not _has_legacy_inventory_requirement(text), profile.stem
    assert label not in _missing(_pointer(text), _POINTER_OBLIGATIONS), (
        f"a {profile.stem} install's AGENTS.md lost {label!r} from its pointer.")


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
@pytest.mark.parametrize("surface", sorted(_INSTALLED_PLAN_COMPLETION))
def test_installed_plan_completion_and_surface_mutation(
        installs: dict[str, Path], profile: Path, surface: str) -> None:
    root = installs[profile.stem]
    text = (root / _INSTALLED_PLAN_COMPLETION[surface]).read_text(encoding="utf-8")
    source = _INSTALLED_PLAN_COMPLETION_SOURCES[surface]
    spec = _PLAN_COMPLETION_SURFACES[source]
    missing = _missing_completion(text, spec["patterns"])
    assert not missing, (
        f"{profile.stem} installed {surface} lost completion guidance: {missing}")
    label, anchor = spec["mutation"]
    mutant = _delete_sentence(text, anchor)
    assert label in _missing_completion(mutant, spec["patterns"]), (
        f"{profile.stem} installed {surface} mutation survived")


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
def test_an_install_without_the_sweep_is_reported(
        installs: dict[str, Path], profile: Path) -> None:
    """The install check can fail: drop the section and every item goes missing."""
    text = (installs[profile.stem] / "dev" / "agent_collaboration.md").read_text(
        encoding="utf-8")
    assert _missing(_sweep(text), _SWEEP_OBLIGATIONS) == [], (
        f"the unmutated {profile.stem} install is missing items; no control.")
    gutted = text.replace(_sweep(text), "## The review sweep\n\n")
    assert sorted(_missing(_sweep(gutted), _SWEEP_OBLIGATIONS)) == \
        sorted(_SWEEP_OBLIGATIONS)


# --------------------------------------------------------------------------
# Mutants: delete one thing from a copy and a named check must go red, beside
# an unmutated control that is green.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_deleting_lens_4_is_reported(rel: str) -> None:
    sweep = _sweep(_text(rel))
    assert _missing(sweep, _SWEEP_OBLIGATIONS) == []
    mutant = re.sub(r"(?s)\b4\. .*?(?=\b5\. )", "", " ".join(sweep.split()))
    assert "lens-4-silent-failure-fail-closed" in _missing(mutant, _SWEEP_OBLIGATIONS)


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_deleting_the_not_covered_half_is_reported(rel: str) -> None:
    sweep = _sweep(_text(rel))
    assert _missing(sweep, _SWEEP_OBLIGATIONS) == []
    mutant = _delete_between(sweep, "Not covered / low confidence",
                             "The line does not end")
    assert "coverage-line-not-covered-half" in _missing(mutant, _SWEEP_OBLIGATIONS)


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_deleting_the_scope_sentence_is_reported(rel: str) -> None:
    sweep = _sweep(_text(rel))
    assert _missing(sweep, _SWEEP_OBLIGATIONS) == []
    mutant = _delete_sentence(sweep, "lenses can inform")
    assert "the-lenses-can-inform-review-stages" in _missing(
        mutant, _SWEEP_OBLIGATIONS)


@pytest.mark.parametrize("rel", _LOOP_FILES, ids=_FILE_IDS.get)
def test_adding_a_sixth_ledger_item_is_reported(rel: str) -> None:
    text = _text(rel)
    assert not _has_legacy_inventory_requirement(text), "control: source is clear"
    mutant = f"{text}\n\nCode review includes a falsification ledger.\n"
    assert _has_legacy_inventory_requirement(mutant)


# --------------------------------------------------------------------------
# A fresh install must not leave a one-word `{{placeholder}}` the engine does
# not recognise: the next upgrade would plan the file as needing a value.
# --------------------------------------------------------------------------

def _installed_text_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*")
                  if p.is_file() and p.suffix in {".md", ".yml", ".txt"}
                  and ".git" not in p.parts)


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p.stem)
def test_an_install_leaves_no_placeholder_the_engine_cannot_fill(
        installs: dict[str, Path], profile: Path) -> None:
    sys.path.insert(0, str(CAIRN_ROOT))
    from bootstrap._scaffold.config import KNOWN_TOKENS
    from bootstrap._scaffold.slotmerge import find_unfilled_tokens
    root = installs[profile.stem]
    files = _installed_text_files(root)
    assert any(f.name == "agent_collaboration.md" for f in files), (
        "control: the installed tree was read")
    bad = {}
    for path in files:
        left = set(find_unfilled_tokens(path.read_text(encoding="utf-8",
                                                       errors="replace")))
        left -= set(KNOWN_TOKENS)
        if left:
            bad[path.relative_to(root).as_posix()] = sorted(left)
    assert not bad, (
        f"a {profile.stem} install carries one-word placeholders the engine "
        f"cannot fill: {bad}. An upgrade plans each such file as needing a "
        f"value and never advances it.")


# --------------------------------------------------------------------------
# The lens text exists once. The dual-review module supplies staffing guidance
# for a called read and does not duplicate review-loop instructions. A second copy of the
# roster in the module is how two definitions drift apart, and a team that
# selected the module would merge both into its loop document.
# --------------------------------------------------------------------------

SHIPPED_MODULE = "templates/modules/team-gated/dual-review.md"
OWN_MODULE = "dev/modules/dual-review.md"
_MODULE_FILES = (SHIPPED_MODULE, OWN_MODULE)
_MODULE_IDS = {SHIPPED_MODULE: "shipped-module", OWN_MODULE: "own-module"}

#: label -> pattern for the text only the review-loop document may carry.
_MODULE_ABSENT = {
    **{f"module-has-{label}": pattern for label, pattern in _LENSES.items()},
    "module-has-the-citation-rule":
        r"Falsifiable evidence|A cited claim is credible|bare .checked.",
    "module-has-review-evidence-guidance":
        r"Code review tries to falsify the change|Keep repeatable probes and mutation checks|"
        r"Code review includes a falsification ledger",
    "module-has-a-duplicate-scope-reduction-trap":
        r"scope-cut means claim correction|The scope-reduction trap — the "
        r"mirror of the clean pass|The outcome test\. Judge a narrowing",
}


def _module_carries(text: str) -> list[str]:
    normalized = _normalize(text)
    return [label for label, pattern in _MODULE_ABSENT.items()
            if re.search(pattern, normalized)]


def _sweep_part(rel: str, start: str, end: str) -> str:
    """A stretch of the sweep, between two literals, as the module once held it."""
    flat = _normalize(_sweep(_text(rel)))
    a = flat.index(start)
    return flat[a:flat.index(end, a)]


@pytest.mark.parametrize("rel", _MODULE_FILES, ids=_MODULE_IDS.get)
def test_the_module_carries_no_lens_citation_rule_or_ledger(rel: str) -> None:
    found = _module_carries(_text(rel))
    assert not found, (
        f"{rel} carries {found}. That text lives once, in the review-loop "
        f"document every install receives; a second copy drifts.")


@pytest.mark.parametrize("rel", _MODULE_FILES, ids=_MODULE_IDS.get)
def test_restoring_the_roster_into_the_module_is_reported(rel: str) -> None:
    assert _module_carries(_text(rel)) == [], "control: the module is clean"
    roster = _sweep_part(SHIPPED_LOOP, "1. Claims", "The lenses can inform")
    found = _module_carries(f"{_text(rel)}\n\n> {roster}\n")
    assert "module-has-lens-4-silent-failure-fail-closed" in found
    assert "module-has-lens-1-claims" in found


@pytest.mark.parametrize("rel", _MODULE_FILES, ids=_MODULE_IDS.get)
def test_restoring_the_citation_rule_into_the_module_is_reported(rel: str) -> None:
    assert _module_carries(_text(rel)) == [], "control: the module is clean"
    rule = _sweep_part(SHIPPED_LOOP, "Falsifiable evidence", "End with a two-part")
    assert "module-has-the-citation-rule" in _module_carries(
        f"{_text(rel)}\n\n> {rule}\n")


@pytest.mark.parametrize("rel", _MODULE_FILES, ids=_MODULE_IDS.get)
def test_restoring_the_ledger_into_the_module_is_reported(rel: str) -> None:
    assert _module_carries(_text(rel)) == [], "control: the module is clean"
    guidance = _sweep_part(SHIPPED_LOOP, "Code review tries to falsify the change",
                           "A reviewer who tried to break")
    found = _module_carries(f"{_text(rel)}\n\n> {guidance}\n")
    assert "module-has-review-evidence-guidance" in found
    restored = _module_carries(
        f"{_text(rel)}\n\n> Code review includes a falsification ledger.\n")
    assert "module-has-review-evidence-guidance" in restored
