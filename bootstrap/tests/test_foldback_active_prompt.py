"""Structure + invocation-pattern presence tests for the
active-surfacing agent prompt + the Cairn-side GitHub templates.

The prompt's per-class scrub coverage lives in
`test_foldback_export_scan.py` (the scanner's own fixture tests);
this file pins the PROMPT'S structure -- that it carries the right
checklist taxonomy, names the right scanner invocation, points at
the right GitHub templates, and respects the export-boundary
bright-line on which the entire active-surfacing protocol depends.

These are presence-style tests over the prompt as a textual
artifact: parse-as-Markdown smoke + substring-presence assertions
on the load-bearing pieces.  Phrasing may evolve; the load-bearing
concepts (5+2 checklist, scrub command, --body-file invocation,
filed/pr status transitions, agent-does-not-submit bright-line)
cannot silently disappear.
"""
from __future__ import annotations

from pathlib import Path

import pytest

CAIRN_ROOT = Path(__file__).resolve().parent.parent.parent
PROMPT_PATH = (
    CAIRN_ROOT / "templates" / "modules" / "default-on"
    / "fold-back-active-prompt.md"
)
ISSUE_TEMPLATE_PATH = (
    CAIRN_ROOT / ".github" / "ISSUE_TEMPLATE" / "foldback.md"
)
PR_TEMPLATE_PATH = (
    CAIRN_ROOT / ".github" / "PULL_REQUEST_TEMPLATE" / "foldback.md"
)

pytestmark = pytest.mark.skipif(
    not PROMPT_PATH.exists(),
    reason="active-surfacing prompt asset not available",
)


@pytest.fixture(scope="module")
def prompt_text() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def issue_template_text() -> str:
    return ISSUE_TEMPLATE_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def pr_template_text() -> str:
    return PR_TEMPLATE_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Prompt: structure + load-bearing content
# ---------------------------------------------------------------------------


class TestPromptStructure:
    def test_prompt_parses_as_markdown(self, prompt_text):
        # Smoke: the file is non-empty and starts with a Markdown
        # heading (we treat that as the "parses" check -- the prompt
        # is read as Markdown by the agent reading it).
        assert prompt_text.strip(), "prompt is empty"
        assert prompt_text.lstrip().startswith("# "), (
            "prompt does not start with a top-level Markdown heading"
        )

    def test_prompt_carries_six_step_protocol(self, prompt_text):
        # All six protocol steps must be present as headings, in order.
        # Match the heading shape (`### Step N -- <Name>`) rather than
        # bare label text -- the prompt mentions step labels in the
        # narrative ahead of the headings (e.g. the export-boundary
        # section forward-references "Step 4 (Scrub)").
        steps = [
            ("### Step 1", "Recap"),
            ("### Step 2", "Choose"),
            ("### Step 3", "Compose"),
            ("### Step 4", "Scrub"),
            ("### Step 5", "Submit"),
            ("### Step 6", "Record"),
        ]
        positions = []
        for heading, name in steps:
            assert heading in prompt_text and name in prompt_text, (
                f"protocol step heading missing: {heading} -- {name}"
            )
            pos = prompt_text.find(heading)
            positions.append(pos)
        # Step headings appear in order.
        assert positions == sorted(positions), (
            "protocol step headings appear out of order"
        )


class TestNoExportChecklist:
    """The 5+2 no-export class taxonomy must enumerate every class
    distinctly -- matching the scanner's coverage and the manual-
    affirmation tier the template surfaces."""

    def test_machine_gated_classes_enumerated(self, prompt_text):
        for class_name in (
            "Credentials", "Private filesystem paths",
            "IP addresses", "Internal hostnames",
            "Adopter-configurable proprietary tokens",
        ):
            assert class_name in prompt_text, (
                f"machine-gated class missing from prompt checklist: "
                f"{class_name}"
            )

    def test_manual_affirmation_classes_enumerated(self, prompt_text):
        for class_name in (
            "Unpublished data hints",
            "Proprietary domain detail",
        ):
            assert class_name in prompt_text, (
                f"manual-affirmation class missing from prompt checklist: "
                f"{class_name}"
            )

    def test_checklist_acknowledges_5_plus_2_split(self, prompt_text):
        # The split is the load-bearing taxonomy decision.
        assert "Machine-gated" in prompt_text
        assert "Manual-affirmation" in prompt_text

    def test_ip_bright_line_covers_both_deployment_and_remote(
        self, prompt_text,
    ):
        # Per maintainer bright-line directive: BOTH deployment-internal
        # AND remote-repo IPs are no-export.
        # Look for the conjunction shape (BOTH ... AND ...).
        assert "BOTH" in prompt_text and "deployment-internal" in prompt_text \
               and "remote-repo" in prompt_text, (
            "IP bright-line should explicitly cover BOTH deployment-internal "
            "AND remote-repo IPs"
        )

    def test_documentation_ip_allowlist_noted(self, prompt_text):
        # The RFC 5737 / 3849 allowlist is part of the checklist's
        # honest framing (documentation IPs do not trigger).
        assert "RFC 5737" in prompt_text or "192.0.2" in prompt_text


# ---------------------------------------------------------------------------
# Prompt: invocation patterns (the verified-at-plan-time commands)
# ---------------------------------------------------------------------------


class TestInvocationPatterns:
    def test_prompt_invokes_export_scanner_via_install_path(
        self, prompt_text,
    ):
        # The agent runs the scanner from the deployment-repo root,
        # where the verbatim-install puts it at scripts/.
        assert "python scripts/foldback_export_scan.py" in prompt_text, (
            "prompt does not name the scanner's adopter-install "
            "invocation path"
        )

    def test_prompt_uses_body_file_for_gh_invocation(self, prompt_text):
        # Per VBA #25 + VBA #27: --body-file is the verified-correct
        # invocation; --dry-run does NOT exist on gh issue create.
        assert "--body-file" in prompt_text, (
            "prompt does not name the --body-file gh invocation pattern "
            "(VBA #25: --template takes a name, not a file)"
        )
        # And critically: the prompt must NOT suggest --dry-run.
        assert "--dry-run" not in prompt_text, (
            "prompt names --dry-run, which gh issue create does NOT "
            "support (VBA #27)"
        )

    def test_prompt_names_filed_and_pr_status_transitions(
        self, prompt_text,
    ):
        # Step 6 writes the row's status transition.
        assert "filed -> <#issue-number>" in prompt_text \
               or "filed -> <#" in prompt_text, (
            "prompt does not name the filed status transition"
        )
        assert "pr -> <#pr-number>" in prompt_text \
               or "pr -> <#" in prompt_text, (
            "prompt does not name the pr status transition"
        )

    def test_prompt_names_deferred_until_for_defer_path(self, prompt_text):
        assert "deferred-until" in prompt_text, (
            "prompt does not document the deferred-until snooze schema "
            "in Step 2's defer path"
        )


# ---------------------------------------------------------------------------
# Prompt: export-boundary bright-lines
# ---------------------------------------------------------------------------


class TestPRChangedFileScanning:
    """The PR template's
    affirmation covers BOTH the body AND every changed file in the
    diff.  The prompt's Step 4 must instruct the agent + maintainer
    to scan both -- otherwise the PR affirmation is a false
    security claim.
    """

    def test_prompt_names_pr_only_changed_file_scanning(self, prompt_text):
        # The Step 4 PR branch must explicitly enumerate changed files
        # via git diff and pass them to the scanner.
        assert "PR-shape" in prompt_text or "PR shape" in prompt_text, (
            "prompt does not call out the PR-shape filing branch"
        )
        assert "git diff --name-only" in prompt_text or \
               "gh pr diff --name-only" in prompt_text, (
            "prompt does not name a changed-file enumeration command"
        )

    def test_prompt_names_multi_file_scanner_invocation(self, prompt_text):
        # The scanner accepts multiple files; the prompt must show
        # the multi-arg form so the agent runs body + files in one
        # invocation.
        assert "<file1>" in prompt_text or "<file2>" in prompt_text \
               or "<file" in prompt_text, (
            "prompt does not show the multi-file invocation pattern "
            "(scanner accepts multiple positional args)"
        )

    def test_prompt_states_pr_fails_closed_on_any_file(self, prompt_text):
        # The bright-line: any fail-severity in ANY file fails the
        # gate for the whole filing.
        assert (
            "ANY fail-severity finding in ANY file" in prompt_text
            or "fail-severity finding in ANY file" in prompt_text
            or "any fail-severity" in prompt_text.lower()
        ), (
            "prompt does not state the any-file-fails-closed contract"
        )


class TestFoldbackAcceptMarkerDocumented:
    """The prompt's documented-false-positive
    disposition must point at the actual `foldback-accept:` marker
    grammar the scanner implements -- not at the abandoned
    `cairn-accept`-style placeholder.
    """

    def test_prompt_names_foldback_accept_marker(self, prompt_text):
        assert "foldback-accept" in prompt_text, (
            "prompt does not name the foldback-accept marker"
        )

    def test_prompt_requires_marker_rationale(self, prompt_text):
        # The rationale is required (empty rationale is itself a
        # finding).  The prompt must communicate this.
        assert "rationale" in prompt_text.lower() \
               and "required" in prompt_text.lower(), (
            "prompt does not state the marker rationale is required"
        )
        assert "silent waivers" in prompt_text.lower() \
               or "empty" in prompt_text.lower(), (
            "prompt does not state empty rationales are forbidden"
        )


class TestExportBoundaryBrightLines:
    def test_prompt_states_agent_does_not_submit(self, prompt_text):
        # The export-boundary structural guard.  Multiple phrasings
        # are acceptable; assert the load-bearing word "submit" + a
        # negation of agent agency.
        assert "agent does not submit" in prompt_text.lower() \
               or "never submit" in prompt_text.lower() \
               or "do not submit" in prompt_text.lower() \
               or "you do not execute" in prompt_text.lower(), (
            "prompt does not carry the agent-does-not-submit "
            "bright-line"
        )

    def test_prompt_specifies_fail_closed_scrub(self, prompt_text):
        # The machine gate is fail-closed.
        assert "fail-closed" in prompt_text.lower() \
               or "fail closed" in prompt_text.lower(), (
            "prompt does not characterize the scrub gate as fail-closed"
        )

    def test_prompt_disallows_bypass_of_scrub(self, prompt_text):
        # Anti-pattern: the agent does not negotiate the gate.
        assert "do not negotiate" in prompt_text.lower() \
               or "you do not decide" in prompt_text.lower() \
               or ("Bypass" in prompt_text and "scrub" in prompt_text), (
            "prompt does not warn against bypassing the scrub gate"
        )


# ---------------------------------------------------------------------------
# Prompt: cross-references to companion artifacts
# ---------------------------------------------------------------------------


class TestPromptCrossReferences:
    def test_prompt_references_foldback_doctrine(self, prompt_text):
        assert "fold-back.md" in prompt_text and \
               "Active surfacing" in prompt_text

    def test_prompt_references_issue_template(self, prompt_text):
        assert "ISSUE_TEMPLATE/foldback.md" in prompt_text

    def test_prompt_references_pr_template(self, prompt_text):
        assert "PULL_REQUEST_TEMPLATE/foldback.md" in prompt_text

    def test_prompt_references_export_scan_module(self, prompt_text):
        # The companion module doc for the scrub gate.
        assert "foldback_export_scan" in prompt_text


# ---------------------------------------------------------------------------
# GitHub templates: shape + affirmation
# ---------------------------------------------------------------------------


class TestIssueTemplate:
    def test_issue_template_has_yaml_frontmatter(self, issue_template_text):
        # `gh issue create --template <name>` requires YAML front-matter
        # with a `name:` field to be discoverable.
        lines = issue_template_text.splitlines()
        assert lines[0] == "---", (
            "issue template missing YAML front-matter opening `---`"
        )
        # Find the closing fence.
        closing = None
        for i, line in enumerate(lines[1:], start=1):
            if line == "---":
                closing = i
                break
        assert closing is not None, (
            "issue template YAML front-matter is not closed"
        )
        fm = "\n".join(lines[1:closing])
        assert "name:" in fm, "issue template front-matter missing `name:`"
        assert "about:" in fm, "issue template front-matter missing `about:`"

    def test_issue_template_has_export_safety_affirmation(
        self, issue_template_text,
    ):
        assert "Export-safety affirmation" in issue_template_text
        # Both manual classes called out.
        assert "unpublished data hints" in issue_template_text.lower()
        assert "proprietary domain detail" in issue_template_text.lower()
        # Machine-scrub mentioned as the companion half.
        assert "foldback_export_scan.py" in issue_template_text


class TestPRTemplate:
    def test_pr_template_has_export_safety_affirmation(
        self, pr_template_text,
    ):
        assert "Export-safety affirmation" in pr_template_text
        assert "unpublished data hints" in pr_template_text.lower()
        assert "proprietary domain detail" in pr_template_text.lower()
        assert "foldback_export_scan.py" in pr_template_text

    def test_pr_template_has_deployment_cross_link_section(
        self, pr_template_text,
    ):
        assert "Deployment-side cross-link" in pr_template_text
