# Make outward report drafts usable

**Author**: Terra (Implementation, Medium)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy — a shipped file changes the install mapping
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md
**In brief**: Give adopters a findable place to draft reports to Cairn or a dependency and obtain approval before each public report.

## Decision summary

An agent finding a Cairn problem or dependency defect has a dependency draft template but no collaboration-guide route to it, and the Cairn fold-back form is not installed. Add one Cairn fold-back template in the existing `dev/upstream/` folder, improve the existing dependency workflow, and point the collaboration guide to both. Draft and check each report, show it to the Human Maintainer, and file only after approval of that particular report; exclude unpublished data and credentials. This addresses #80. It adds one installed file and the corresponding mapping and maintenance, with implementation and review effort not yet measured; it creates no service or automatic filing.

## Context

`dev/PLANNING.md` Group 4 records the 2026-11-10 direction and #80. The shipped `templates/core/dev/upstream/_template.md` supplies reproduction and filing fields; its README currently separates dependency drafts from Cairn fold-back. The Cairn issue and pull request forms at `.github/ISSUE_TEMPLATE/foldback.md` and `.github/PULL_REQUEST_TEMPLATE/foldback.md` contain the fold-back protocol, but are not shipped to adopters. Each forge reads its own fixed paths.

## Proposal

Ship `templates/core/dev/upstream/foldback.md` with the Cairn counterpart `dev/upstream/foldback.md`, and retain the existing dependency template. Make the shipped fold-back template the single protocol source; the Cairn forge forms point to it instead of restating the protocol, while keeping the fields needed by their forge. Keep `.github` and `.gitlab` fixed forge paths; add no `.forge` directory. Update the existing upstream README and collaboration guide, including their shipped counterparts, to route an agent who finds a Cairn problem or dependency defect to a local draft in `dev/upstream/`.

For a dependency, use its own issue template when available, adapting the local draft to its requested information; otherwise use the existing dependency template. Describe how to find that template without requiring an automated fetch or a new external service. Keep reproduction, versions, expected and actual behavior and status useful to a real upstream maintainer. For either channel, check the draft for unpublished data and credentials, show it to the Human Maintainer, and obtain explicit approval for each report before filing. No standing authorization, automatic external filing, or permission to disclose private material follows from this workflow. Record the outcome in the draft using the existing lifecycle. A finding spanning both channels gets distinct drafts and approvals.

## Rationale

A pointer at the point of work makes the existing folder useful; one protocol source prevents two forms from drifting. The extra installed file costs a mapping change but gives an adopter the form without requiring a network read.

## Alternatives considered

Keep only the forge forms: adopters may not have them, so discovery and drafting remain unreliable. A new generic forge directory would not be read by either forge and adds another home to maintain.

## Documentation / doctrine surface

Change `templates/core/dev/upstream/`, `templates/core/dev/agent_collaboration.md`, their Cairn counterparts, the existing forge forms, the install mapping and its descriptive inventory as needed. Route operative instructions through the collaboration guide and existing upstream folder; retain deliberation here and software description in its existing descriptive home. No always-loaded rule expansion is proposed.

Proposed paths:
- `templates/core/dev/upstream/foldback.md`
- `dev/upstream/foldback.md`

## Evidence / verification plan

A missing installed template, inaccessible pointer, contradictory protocol, or a route that files without per-report approval falsifies the outcome. Review the resulting draft instructions for both channels and public-data boundaries.

### Tests required

Exercise the public fresh-install manifest and installation for the new mapped file and its destination, and upgrade from an install that predates it; a missing mapping or wrong destination must fail. Select existing affected checks with `python tests/tier_inventory.py for <changed paths>` and extend an existing install or upgrade promise only where it cannot catch that fault. No test asserts prose wording.

### Examples / smoke checks

In a disposable installation, follow the guide to draft one synthetic Cairn report and one synthetic dependency report, including an upstream template and the fallback, and verify the human approval step precedes filing. Do not actually file. Run the project prose gates and claim check.

#### Security preflight

S1: The trusted install mapping selects a shipped template; project agents supply draft content and the Human approves each report. An external dependency's template is untrusted guidance, not authorization. S2: Installation checks must fail when the new mapping is removed; verify that negative control in the plan. S3: The public installer and upgrade exercise their selected mapping; the plan records exact commands and input sets and compares them with the shipped description. S4: Missing or unsuitable external templates fall back to the local template; missing approval means no filing. Existing installer containment and collision refusals remain in force. S5: A malicious external template can still ask for secrets or contain hostile instructions; human review and the no-private-data rule do not prove a draft safe.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Assurance path

Usual and Security proposal review, a heavy plan with internal and Security review, then implementation and independent code and Security review. No external report is filed for verification. Elapsed: unknown; tokens: unknown.

## Review -- Terra (ordinary Reviewer) -- 2026-11-18

Reviewed commit: `73c2a6c5723c6d6b1b50767ec97b54417b67e04e`

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: a local draft and per-report approval make both channels usable without automatic publication; the installed mapping makes heavy assurance appropriate. Evidence: `dev/PLANNING.md` Group 4, outward-report row; `dev/rules/protected-surfaces.md`.
2. **Best alternative.** A pointer to existing forge forms costs less but leaves adopters without the form; reuse the dependency template and fixed forge paths as proposed. Evidence: `dev/upstream/README.md`; `.github/ISSUE_TEMPLATE/foldback.md`.
3. **What would show it wrong?** A disposable fresh install or upgrade missing the draft, or a synthetic report reaching filing without its own approval, would falsify the route. Evidence: proposal, Evidence / verification plan.

**Steelman and audience.** The summary gives a person the choice without translation; the collaboration guide is the right agent-facing route. Costs of the new installed file, mapping and maintenance are identified but unmeasured.

**Blocking — preserve the full export boundary.** The proposal replaces the forms' protocol with a new source but names only unpublished data and credentials. Both existing forms also prohibit proprietary project or customer detail; the PR form applies the check to every changed file as well as its body. Preserve those duties and the final reread in the shared protocol and relevant forge fields, with a synthetic PR example covering its diff. The direction permits an agent to file after specific approval, so explain that intentional change from the forms' current human-submission rule. Evidence: `.github/ISSUE_TEMPLATE/foldback.md`, Export-safety affirmation; `.github/PULL_REQUEST_TEMPLATE/foldback.md`, Export-safety affirmation; `dev/PLANNING.md` Group 4, outward-report row.

**Coverage.** Read the proposal, board row, existing draft and both forms; did not execute installation, file a report, or independently assess the security boundary. Security Review remains separate.

## Review -- Sol (Security Review, High) -- 2026-11-18

```text
Reviewed commit: 73c2a6c5723c6d6b1b50767ec97b54417b67e04e
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Give adopters one installed protocol and an agent-facing route, with the full export boundary written into scope. Adding a core install row warrants the heavy lane. `install/_scaffold/config.py:559-565`, `dev/rules/protected-surfaces.md`.
2. **Best alternative.** Keep each forge's native fields and point to one protocol from both forms and the installed collaboration guide. Use the dependency's form as field guidance after checking it against the local approval and privacy rules. `install/SAFETY.md:90-96`, `templates/core/dev/upstream/_template.md:40-54`.
3. **What would show it wrong?** A public upgrade that writes through a linked destination, a broken forge pointer, or a synthetic report that reaches filing without approval of its recipient and contents would falsify delivery. `tests/test_upgrade_module_additions.py:1109-1141`, `install/SAFETY.md:90-96`.

- **Blocking — name who files each report.** The current Cairn forms require the Maintainer to submit by hand. The board's #80 entry proposes an agent filing an individually approved issue. Write that distinction into the proposal and retain hand submission for Cairn pull requests unless a Decision changes it. Apply the approval to the actual report and destination before filing. `dev/PLANNING.md:99`, `.github/ISSUE_TEMPLATE/foldback.md:13-17`, `.github/PULL_REQUEST_TEMPLATE/foldback.md:8-12`.
- **Blocking — preserve the publication check end to end.** Explicitly carry forward the final reread, proprietary-detail and unpublished-data checks, including the PR's full diff. Replace the fallback template's verbatim-traceback instruction with sanitized evidence before a draft enters Git. In the disposable smoke check, include synthetic sensitive content and verify the sanitized version is what reaches the Maintainer. `.github/ISSUE_TEMPLATE/foldback.md:69-83`, `.github/PULL_REQUEST_TEMPLATE/foldback.md:53-70`, `templates/core/dev/upstream/_template.md:40-42`.

Coverage: committed workflow, mappings and named test paths. No installer, forge, filing, platform or suite execution.
