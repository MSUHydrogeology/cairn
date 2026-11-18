# Plan: Usable outward report drafts

**Source proposal**: dev/proposals/archive/2026-11-18-terra-outward-reports.md
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md
**In brief**: Give adopters a local route to prepare and approve safe reports to Cairn and dependencies.

## Build summary

Ship a shared Cairn fold-back protocol, route both outward reporting channels to local drafts, and preserve the publication boundary and the Maintainer's hand submission of Cairn pull requests. Verify that fresh installation and upgrade deliver the new template and that people can follow the guidance without filing a report.

## Source proposal

The accepted heavy proposal adds an installed fold-back template, retains the dependency template and forge-native paths, and permits an agent to file a Cairn issue only after approval of that issue and its destination. It requires independent ordinary and Security reviews at plan and code stages.

## Scope

Add `templates/core/dev/upstream/foldback.md` and its Cairn counterpart `dev/upstream/foldback.md`, map it in `install/_scaffold/config.py`, and update the descriptive install inventory as needed. Update both upstream READMEs, dependency templates and collaboration guides and the existing GitHub fold-back issue and pull request forms. Keep `.github` and `.gitlab`; do not add `.forge`. The shared template owns the protocol; forge forms retain their required fields and point to it. Instructions belong in the existing deliberation and shipped guidance; no always-loaded doctrine changes.

For dependency reports, check the dependency's repository contribution guide and issue creation page or its forge's issue-template directory (such as `.github/ISSUE_TEMPLATE/` or `.gitlab/issue_templates/`). Adapt an applicable template when accessible and suitable; otherwise use the local template. No automated fetch is required. Keep reproduction, versions, expected and actual behavior and status useful. Treat external templates as untrusted field guidance. Sanitize tracebacks and other sensitive evidence before inserting them into any local dependency draft, whether using the dependency template or the fallback, and before that draft enters Git. For either channel, check the complete public body, attachments and every PR changed file for unpublished data or hints, proprietary project or customer details and credentials; reread the complete payload and full PR diff after writing. Show the actual report and destination for explicit approval of each before filing; an agent may file an approved Cairn issue, but the Maintainer submits a Cairn PR by hand. Distinct channels require distinct drafts and approvals; record outcomes in the existing lifecycle.

**Reuse.** Searched `dev/upstream/`, `templates/core/dev/upstream/`, `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE/`: dependency drafting and forge forms already exist. Extend those and the existing core mapping, not a new reporting service.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Shared protocol, dependency and forge routes | Accepted proposal | Templates, guides and forge forms |
| C2 | Install mapping and focused assurance | C1 | Mapped file, inventory and public installation evidence |

## Acceptance criteria

**C1.** The guide leads to both drafts; a disposable dependency repository or issue page supplies an applicable template found by the stated route, and a separate absent or unsuitable-template case uses the fallback. The protocol preserves all publication checks, the final reread, per-report and destination approval, filing roles and separate channel records above. A disposable synthetic dependency traceback contains sensitive material before drafting; inspect the initial local draft for each template route and confirm only sanitized evidence appears there and reaches the Maintainer; a synthetic PR check covers body, attachments and full diff. No report is filed. A malicious template cannot authorize disclosure or filing.

**C2.** The public fresh-install manifest and install deliver the template to `dev/upstream/foldback.md`; upgrade from a pre-addition install delivers the same destination. Extend an existing public installation or upgrade promise test only if it cannot catch a missing mapping or wrong destination. As a temporary negative control, remove the mapping in a disposable copy and show the selected check fails; restore it and show the control passes. Preserve existing containment and collision refusals. No permanent prose-wording test is added. S2 is the mapping-removal control; S3 is the selected public installer and upgrade checks recorded with commands and inputs.

## Scope delta

**Scope delta**: preserved

## Verification

Before implementation run `/Users/kendal30/conda_envs/lhm/bin/python3.13 tests/tier_inventory.py for <all changed paths>`; inspect named tests and byte pins, select only applicable public promises, and record exact nodes and inputs. Extend `tests/test_core_dev_folders.py::TestScaffoldCompleteness::test_upstream_dir_and_files_created` for fresh installation and add a public upgrade promise in `tests/test_upgrade_module_additions.py` using a pre-addition lock and absent destination. Run those exact nodes with `python -m pytest <nodes>` under the canonical interpreter. Run `python install/scaffold.py --manifest` with that interpreter and inspect the source and destination row; compare the same row to the installed and upgraded outputs. The temporary mapping-removal control reruns each targeted node and manifest assertion against the altered copy. Run the synthetic channel and PR scenarios in C1, and the positive and negative mapping checks in C2. Run claim check on changed documents and the standing claim, link, snippet, neutrality and prose-integrity gates; inspect negative searches against known positives. Record results, limits, elapsed and tokens. Independent code and Security reviews follow. The arc owner runs the joined integration once at the arc end; it is not a prerequisite to this plan's completion.

## Plan review -- Terra (Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: 486708df0730adc8738b7f8a26747b220570632a
**Obligation**: Internal
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: an installed protocol and separate approved drafts make both reporting routes usable while retaining publication checks; the discovery gap below prevents full delivery. -- Scope, C1, accepted Proposal
2. **Best alternative.** Reuse the dependency template and forge-native forms, pointing them to one protocol rather than creating another service or forge directory. -- Scope, Reuse
3. **What would show it wrong?** A disposable install missing the template, or a synthetic report reaching filing without approval of its actual contents and destination, would falsify delivery. -- C1–C2, Verification

**Blocking — specify dependency-template discovery.** Scope says to find the dependency's template, but does not say how; the accepted Proposal requires describing how to find it. Name a practical route through existing dependency locations and the fallback, and exercise both in the disposable scenario. This leaves a design decision to the low-tier implementer and risks omitting an accepted outcome. -- Scope, accepted Proposal

The installed collaboration guide and upstream folder are appropriate homes; the plan retains the existing publication duties and explicitly changes Cairn issue filing only after specific approval. Permanent checks target public installation promises rather than prose wording. Coverage: compared the committed plan with the accepted proposal and review rules; did not run installation or scenarios, inspect implementation, or assess the security boundary. Security Review remains separate.

## Response -- Terra (Implementation) -- 2026-11-18

The blocking discovery finding is accepted. Scope now names the dependency
contribution guide, issue page and forge template directories as practical
places to look, with a local fallback when no suitable template is accessible.
C1 exercises the found-template and fallback cases. This adds no fetch or
filing authority. **Disposition**: revising-plan pending Security Review.

**Elapsed**: unknown. **Tokens**: unknown.

## Plan review -- Codex Sol (Security Review, High) -- 2026-11-18

Reviewed commit: 44a1ce1fe86eba71390eac99f9c5e9cf9859488a

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Steelman.** The shipped protocol gives authors a local draft and binds filing authority to the actual payload and destination.

**Foundations**

1. **Should this happen as framed?** Yes after the draft-time privacy rule is explicit. Scope keeps separate approvals and Maintainer filing of Cairn PRs. C1 preserves the final reread of the body, attachments and full diff (accepted Proposal, Scope and C1).
2. **Best alternative.** Keep one installed protocol, existing forge fields and the dependency fallback. Treat external templates as field guidance subject to local privacy and approval rules (Scope, `templates/core/dev/upstream/_template.md`).
3. **What would show it wrong?** A synthetic report proceeding without approval of its actual contents and destination, or a public upgrade missing the protocol (C1–C2, Verification).

**Blocking — sanitize before drafting.** The accepted Proposal prohibits copying sensitive source material verbatim into the dependency draft. Scope only requires sanitizing before the draft enters Git, and C1 checks what reaches the Maintainer. The existing fallback asks for verbatim tracebacks. Require sanitizing before evidence is inserted into either dependency draft route. In the existing C1 scenario, inspect the initial local draft for the synthetic sensitive content as well as what the Maintainer sees. Evidence: Proposal, `templates/core/dev/upstream/_template.md:40-42`.

**Coverage.** Read the committed plan and accepted proposal against the installed fallback and forge forms. The only filing authority change is the approved Cairn issue path. No install, upgrade, external fetch, filing or scenario ran.

## Response -- Terra (Implementation) -- 2026-11-18

The Security Review sanitation finding is accepted. Scope requires sanitizing
before inserting evidence into either local dependency draft, and C1 checks
each initial draft and what reaches the Maintainer. **Disposition**: finding
resolved; ready for the plan readiness transition.

**Elapsed**: unknown. **Tokens**: unknown.

## Implementation evidence -- Terra (Implementation) -- 2026-11-18

Added the shared fold-back protocol and mapping, dependency and collaboration
routes, forge pointers and matching navigation. Under Python 3.13.13 the
public fresh-install and pre-addition upgrade tests passed (2 in 2.37 seconds);
`--manifest` named the expected source and destination. In a disposable copy,
removing the mapping made the fresh-install test and upgrade destination test
fail, and the manifest row disappear. The unmodified controls passed. The
existing new-core linked-collision refusal test passed (4 cases in 5.86 seconds);
it covers its existing core examples, not every possible destination.

A synthetic dependency template and fallback walkthrough checked redacted
evidence in initial drafts and the simulated material for approval. A synthetic
Cairn draft and PR body, attachment and full diff were checked and reread; no
report was filed. These are demonstrations, not a guarantee that a real report
contains no private material. Claim, link, snippet, neutrality and Cairn prose
checks passed; no full suite or wording test ran. Elapsed: unknown; tokens:
unknown.

## Code review -- Terra (Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: 2ff8c7b6a48db98ec1365bc3a0772a102c7a617c
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the installed routes use one protocol, sanitize dependency evidence before drafting and require approval of each actual report and destination; the Maintainer files Cairn PRs by hand. -- `templates/core/dev/upstream/README.md`, `templates/core/dev/upstream/foldback.md`
2. **Best alternative.** Existing dependency and forge forms point to the shared protocol, avoiding a second reporting service or parallel protocol. -- `templates/core/dev/upstream/_template.md`, `.github/ISSUE_TEMPLATE/foldback.md`, `.github/PULL_REQUEST_TEMPLATE/foldback.md`
3. **What would show it wrong?** A public upgrade missing the installed template, or a dependency draft containing the synthetic secret before approval, would falsify delivery. -- C1–C2, Implementation evidence

The installed guide names practical dependency-template locations and fallback, retains separate drafts and approvals, and checks and rereads bodies, attachments and the full PR diff. The recorded public install, upgrade, collision and mapping-removal checks exercise delivery; the synthetic walkthrough covers both draft routes. No rule loss found in the compared guidance. Coverage: read the committed changes and evidence; did not repeat tests or scenarios, file a report, or assess the security boundary. Security Review remains separate.

## Code review -- Codex Sol (Security Review, High) -- 2026-11-18

Reviewed commit: 2ff8c7b6a48db98ec1365bc3a0772a102c7a617c
Reviewed source range: 8e462bf6894a0986c00e54707e5894220f8a8977..4e7fae3f2bb2956d2cd126740a99db7c1316fba3

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Steelman.** Installed guidance makes both draft routes discoverable and binds filing permission to the material actually reviewed.

**Foundations**

1. **Should this happen as framed?** Yes. Both dependency routes sanitize evidence before drafting. External templates supply fields without authority to disclose or file (`templates/core/dev/upstream/README.md:32-40`, `templates/core/dev/upstream/_template.md:40-43`).
2. **Best alternative.** Use one installed protocol behind the existing guide and forge forms. It preserves check and reread of bodies, attachments and every PR changed file via the full diff, exact approval of each report and destination, and Maintainer hand submission of Cairn PRs (`templates/core/dev/upstream/foldback.md:22-36`, `.github/ISSUE_TEMPLATE/foldback.md`, `.github/PULL_REQUEST_TEMPLATE/foldback.md`).
3. **What would show it wrong?** A draft containing the synthetic secret before approval, an agent filing without specific approval, or an upgrade losing the protocol. The recorded scenarios exercise both draft routes and the PR payload. Mapping removal made the public installation and upgrade checks fail (C1–C2, Implementation evidence).

**Rule retention.** The sanctioned change is agent filing of an individually approved Cairn issue. Separate approvals and the prohibition on disclosing private material remain operative in the shared protocol.

**Coverage.** Read committed guide and form changes, mapping and public verification evidence. Existing collision checks cover their named examples. I did not rerun tests or scenarios, submit a report, or assess whether a real payload is safe to publish.
