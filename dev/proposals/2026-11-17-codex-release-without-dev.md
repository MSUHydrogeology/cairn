# Proposal: let a project leave Cairn out of a release

**Author**: Codex
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-17
**Rules that apply**: `dev/rules/protected-surfaces.md`, `dev/rules/conventions.md`
**In brief**: Help a project omit its development folder from a release without losing its own content or leaving misleading references.

## Decision summary

After the repository layout places Cairn's installed tools under `dev/`, give adopters guidance and an advisory report for a release that leaves that folder out. Keep the project's root `AGENTS.md`, its software and other chosen release content; mark its development pointers as applying to a development checkout. Add a small ignored scratch area and clear folder guidance, and support project tests under `dev/` without moving anyone's tests. The cost is a few installed files, a report and migration assurance. The report helps find problems; it does not decide what a project releases.

## Context

The Group 4 row in `dev/PLANNING.md` follows the accepted layout work. Issue [#67](https://github.com/MSUHydrogeology/cairn/issues/67) documents a real adopter whose Cairn-installed files were mixed with project tools; the layout plan inventories installed destinations, named root exceptions and an archive without `dev/`. Its final mapping is still under review. Issues [#68](https://github.com/MSUHydrogeology/cairn/issues/68), [#69](https://github.com/MSUHydrogeology/cairn/issues/69), [#71](https://github.com/MSUHydrogeology/cairn/issues/71), [#72](https://github.com/MSUHydrogeology/cairn/issues/72) and [#75](https://github.com/MSUHydrogeology/cairn/issues/75), including their comments, describe the remaining guidance. The accepted run-and-development-rules proposal keeps `AGENTS.md` at the root and makes run rules in root `RULES.md` opt-in. Its wider entry-file split was not selected.

## Proposal

Deliver these adopter-facing outcomes for v0.8, using the final reviewed layout paths. This proposal can be reviewed now; implementation waits for the layout's settled mapping.

1. In the collaboration guide, distinguish development-side material (the `dev/` tree, development guides and Cairn's development tooling) from project content a release keeps, including user and theory documentation, source, tests, examples, changelog and package metadata. Kept content should not cite `dev/` paths; cite plans and proposals by date and topic name instead. Reflect this in the plan, proposal and contributing guidance. Developer guides may cite development records. Retained `AGENTS.md` is the explicit exception for its `dev/` pointers, identified as development-checkout-only; preserve its existing duties and the accepted Operator stop when required development material is absent. An opt-in root `RULES.md` ships whole and run rules do not depend on `dev/`; the adopter removes its development-only pointer when using that convention. Do not rewrite existing adopter citations automatically.
2. Give agents a brief entry sentence in the kept README and first user-guide chapter, pointing to `AGENTS.md` and then the guide. Respect the optional run-rules convention; do not require `RULES.md` for projects that have not opted in.
3. Ship short README guidance for each installed `dev/` folder and require the same for project-added folders: purpose, suitable contents and what needs the Maintainer's permission. The top README lists permitted top-level folders. A README or listing records permission already given; it does not grant or delegate permission. A new folder under `dev/`, or committed briefs and reports used to evade length limits, needs that permission. Put this rule in the collaboration guide, not another always-loaded line. Add `dev/scratch/` for temporary briefs, drafts and notes, with its README and ignore file tracked, contents ignored; durable conclusions belong in their proper records. Git ignore only affects tracking, not secrecy; keep private evidence out of commits and releases. Nothing outside `dev/` cites scratch.
4. Extend the existing link checker with an advisory release-boundary report, invoked by the adopter from the development checkout before release. It identifies references from release-side files to `dev/` except retained `AGENTS.md` pointers; tracked `dev/` folders missing a README or omitted from the top-level list; and tracked scratch content other than its two installed files. Projects identify development-side guides and release-side files through a reviewed repository-relative scope. The report reads selected regular files within the project, offline and read-only, without executing project content or probing external links. Existing link or claim allowances and existing targets cannot suppress its findings; skipped, unreadable, out-of-tree or unclassified inputs are incomplete, never a clean result. Findings inform the Maintainer and never block a release or lifecycle transition by themselves. The plan names the final command, input formats and selection after layout.
5. Support project tests in `dev/tests/` as well as existing test locations; document configuration and repository-root-relative fixtures. Do not move existing tests or force a new location. Where code imports modules under `dev/`, use `dev.tools` or `dev.tests` qualified imports, not bare top-level `tools` or `tests`, to avoid the collision described in #72. Exercise existing test selection with both locations.

The v0.9 optional release module retains #75's committed keep list, cut script and associated check; this proposal adds no release packager or cut command. Project-owned release content and existing root exceptions are preserved. Layout owns tool placement and the omitted-folder archive check, not this proposal.

## Rationale

A clear boundary lets a recipient use the project without Cairn's development records. An advisory report exposes references for the project to judge, without imposing a new release gate or automatically rewriting its files.

## Alternatives considered

Keep current guidance: adopters must discover mixed paths and dead references themselves. A mandatory keep list and release script now would duplicate the separately queued v0.9 module and impose a release process on projects that do not need one.

## Documentation / doctrine surface

The installed collaboration guide owns the development rule; folder READMEs and plan, proposal and contributing templates carry local guidance. The project README and user guide carry the agent entry. Update Cairn's corresponding copies and descriptive documentation. The existing reporting tool and install mapping follow final layout homes; the latter is protected. No change to published methodology is needed.

## Evidence / verification plan

### Tests required

The plan maps changed promises and existing tests to final paths. Through the installed report entry point, use synthetic project trees to show a kept file's reference to an existing `dev/` target is reported even with a link allowance, while a development guide and retained `AGENTS.md` pointers are distinguished. Show out-of-tree and unknown inputs as incomplete, missing or unlisted folders and forced-tracked scratch files as findings, and a clean classified fixture as the negative control; findings do not become a gate. Test fresh installation and upgrade preserve project-owned content, the two tracked scratch files and ignore behavior. Run a fixture project with tests in both supported locations and colliding bare names to show qualified imports select the intended modules. Demonstrate the retained project can run its own tests with `dev/` omitted where those tests are release content; report missing prerequisites rather than claiming success.

### Examples / smoke checks

Run the prose gates and changed-file selections. In a disposable adopter fixture, inspect the final lock destinations and named root exceptions, omit `dev/`, and check kept content and the advisory report with a known positive. The fixture is not a real adopter release.

#### Security preflight

- **S1:** The project supplies file contents, classifications and paths; the installer supplies reviewed templates and mapping. Project input cannot authorize overwriting an unrelated file.
- **S2:** Exercise occupied or modified destinations through existing install and upgrade refusal tests; a forced tracked scratch file and forbidden reference are positive controls for the report.
- **S3:** The adopter invokes the link checker's release-boundary report before release; the plan identifies its final command, formats and selection after layout. Its documented advisory scope must match the tested entry point; it is not a release gate.
- **S4:** Missing, unreadable or unclassified inputs are visible as incomplete, not a clean report; existing install and upgrade collision protections remain in force.
- **S5:** The report is a static aid, not proof that a release is runnable or free of every indirect dependency. A project can misclassify its own files or disregard findings.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Dropping `dev/` breaks retained project work, reports miss the known examples, the guidance forces tests to move, or the installed additions cost more than the problems they prevent without a remedy preserving the outcome.

## Scope delta

**Scope delta**: preserved

Proposed paths:
- `dev/scratch/`
- `dev/tests/`

## Assurance path

**Assurance path**: high-assurance — installed files and their protected mapping change.

Elapsed: unknown. Tokens: unknown.

## Review -- Terra -- 2026-11-17

Reviewed commit: faa0a07528352101c97c16a9ac4a8f82affc8898

**Tier**: usual
**Model basis**: GPT-6.1 Terra, Medium
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown. **Tokens**: unknown.

The release boundary is useful, but the exception for the retained entry file conflicts with an accepted outcome.

**Foundations**

1. **Should this happen as framed?** The report and guidance cover the Group 4 outcomes, but the entry-file exception must preserve the earlier Decision. -- `dev/PLANNING.md`, Group 4; finding below.
2. **Best alternative.** Keep the advisory report and defer the keep list and cut script to the existing v0.9 release module. -- Proposal, items 4–5 and Rationale.
3. **What would show it wrong?** A disposable release missing `dev/` that loses project content or whose report misses a known forbidden reference would defeat the result. -- Proposal, Evidence / verification plan.

**Blocking:** Item 1 and the report permit only `AGENTS.md` pointers to development rules. The accepted run-and-development-rules proposal permits its `dev/` pointers generally and option (a) retains existing paragraphs. The shipped entry includes other references, such as `dev/reflections/README.md` and the `dev/` tree. Preserve the accepted exception and identify those references as development-checkout-only; do not require an adopter to remove or weaken the retained duties. -- `dev/proposals/2026-11-16-claude-run-and-development-rules.md`, items 3–4 and Decision; `templates/core/AGENTS.md`.

**Rule loss:** The proposal says to preserve project-wide rules, but the narrow exception above conflicts with retained references. Rewritten guidance is not yet available to assess.

**Audience and coverage:** The choice and report's advisory role are understandable. Compared the proposal with the Group 4 row, accepted option (a), template and protected-surface rule. The 1,248-word opening exceeds the 1,000-word target. No issue comments were read; no runtime tests, install, release, report scan or Security Review were run.

## Review -- Codex -- 2026-11-17

Reviewed commit: faa0a07528352101c97c16a9ac4a8f82affc8898

**Tier**: Security Review
**Model basis**: GPT-6.2 Sol, High
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** An advisory report fits, with its own rules for what gets reported and read. — Proposal items 4–5 and S3–S5.
2. **Best alternative.** Reuse local parsing in an adopter-invoked report from the development checkout and leave packaging to v0.9. — `dev/PLANNING.md`, Group 4 and the release-module row.
3. **What would show it wrong?** The installed command must flag a kept file's link to an existing `dev/` target despite a link-check allowance, and mark an out-of-tree input incomplete. — `templates/modules/team-gated/link_check.py`, `check_links`.

**Blocking finding.** Both scanners can accept existing targets or suppress findings (`check_path_token` and `_scan` in `templates/modules/default-on/claim_check.py`, `check_links` in the link checker). Specify that ordinary exemptions cannot suppress release findings and that the report reads only selected regular files within the project. It reports skipped or unclassified inputs as incomplete, works offline, and neither executes project content nor changes files. The plan should name the command, adopter trigger, formats and selection, with synthetic positive and negative controls.

**Rule preservation.** A folder's README or list entry records permission already granted by the Maintainer. Scratch guidance should explain that Git ignore only affects tracking and that private evidence stays out of commits and releases (`templates/core/AGENTS.md`, Working tree and commits). Preserve accepted option (a), including the Operator's stop when required development material is absent.

**Coverage.** Read the committed proposal, board, governing rules, accepted run-rules Decision, layout criteria and scanner paths. No issue comments, adopter files, tests or installs examined.

## Response -- Codex -- 2026-11-17

- **Usual, blocking:** Accepted. Item 1 preserves all retained `AGENTS.md` development pointers and duties, including the Operator stop.
- **Security, blocking:** Accepted. Item 4 specifies an offline, read-only, scoped link-checker report independent of ordinary allowances, with incomplete inputs visible; Tests required names positive and negative controls.
- **Security, rule preservation:** Accepted. Item 3 makes README permissions records rather than grants and distinguishes Git ignore from privacy.

### Withdrawn / superseded commitments

The proposed narrow rule-pointer exception is replaced by the accepted broader `AGENTS.md` pointer exception, preserving existing duties.

Elapsed: unknown. Tokens: unknown.
