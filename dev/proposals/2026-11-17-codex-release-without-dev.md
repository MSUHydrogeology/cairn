# Proposal: let a project leave Cairn out of a release

**Author**: Codex
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-17
**Rules that apply**: `dev/rules/protected-surfaces.md`, `dev/rules/conventions.md`
**In brief**: Help a project omit its development folder from a release without losing its own content or leaving misleading references.

## Decision summary

After the repository layout places Cairn's installed tools under `dev/`, give adopters guidance and an advisory report for a release that leaves that folder out. Keep the project's root `AGENTS.md`, its software and other chosen release content; allow `AGENTS.md` to point to development rules marked for a development checkout. Add a small ignored scratch area and clear folder guidance, and support project tests under `dev/` without moving anyone's tests. The cost is a few installed files, a report and migration assurance. The report helps find problems; it does not decide what a project releases.

## Context

The Group 4 row in `dev/PLANNING.md` follows the accepted layout work. Issue [#67](https://github.com/MSUHydrogeology/cairn/issues/67) documents a real adopter whose Cairn-installed files were mixed with project tools; the layout plan inventories installed destinations, named root exceptions and an archive without `dev/`. Its final mapping is still under review. Issues [#68](https://github.com/MSUHydrogeology/cairn/issues/68), [#69](https://github.com/MSUHydrogeology/cairn/issues/69), [#71](https://github.com/MSUHydrogeology/cairn/issues/71), [#72](https://github.com/MSUHydrogeology/cairn/issues/72) and [#75](https://github.com/MSUHydrogeology/cairn/issues/75), including their comments, describe the remaining guidance. The accepted run-and-development-rules proposal keeps `AGENTS.md` at the root and makes run rules in root `RULES.md` opt-in. Its wider entry-file split was not selected.

## Proposal

Deliver these adopter-facing outcomes for v0.8, using the final reviewed layout paths. This proposal can be reviewed now; implementation waits for the layout's settled mapping.

1. In the collaboration guide, distinguish development-side material (the `dev/` tree, development guides and Cairn's development tooling) from project content a release keeps, including user and theory documentation, source, tests, examples, changelog and package metadata. Kept content should not cite `dev/` paths; cite plans and proposals by date and topic name instead. Reflect this in the plan, proposal and contributing guidance. Developer guides may cite development records. The retained `AGENTS.md` is the explicit exception: only pointers to development rules may cite `dev/`, identified as development-checkout-only. Preserve its project-wide rules. An opt-in root `RULES.md` ships whole and run rules do not depend on `dev/`; the adopter removes its development-only pointer when using that convention. Do not rewrite existing adopter citations automatically.
2. Give agents a brief entry sentence in the kept README and first user-guide chapter, pointing to `AGENTS.md` and then the guide. Respect the optional run-rules convention; do not require `RULES.md` for projects that have not opted in.
3. Ship short README guidance for each installed `dev/` folder and require the same for project-added folders: purpose, suitable contents and what needs the Maintainer's permission. The top README lists permitted top-level folders. A new folder under `dev/`, or committed briefs and reports used to evade length limits, needs that permission. Put this rule in the collaboration guide, not another always-loaded line. Add `dev/scratch/` for temporary briefs, drafts and notes, with its README and ignore file tracked, contents ignored; durable conclusions belong in their proper records. Nothing outside `dev/` cites scratch.
4. Provide an advisory report, reusing existing claim or link reporting where practical, identifying references from release-side files to `dev/` except the narrow `AGENTS.md` rule pointer; tracked `dev/` folders missing a README or omitted from the top-level list; and tracked scratch content other than its two installed files. Let projects identify development-side guides and release-side files; do not silently treat an unclassified file as safe. Findings inform the Maintainer and never block a release or lifecycle transition by themselves.
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

The plan maps changed promises and existing tests to final paths. Through the installed report entry point, use synthetic project trees to show a known forbidden reference is reported, a development guide and permitted `AGENTS.md` pointer are distinguished, an unrelated `AGENTS.md` reference is reported, and unknown classifications are visible. Show missing or unlisted folders and forced-tracked scratch files are reported without turning findings into a gate. Test fresh installation and upgrade preserve project-owned content, the two tracked scratch files and ignore behavior. Run a fixture project with tests in both supported locations and colliding bare names to show qualified imports select the intended modules. Demonstrate the retained project can run its own tests with `dev/` omitted where those tests are release content; report missing prerequisites rather than claiming success.

### Examples / smoke checks

Run the prose gates and changed-file selections. In a disposable adopter fixture, inspect the final lock destinations and named root exceptions, omit `dev/`, and check kept content and the advisory report with a known positive. The fixture is not a real adopter release.

#### Security preflight

- **S1:** The project supplies file contents, classifications and paths; the installer supplies reviewed templates and mapping. Project input cannot authorize overwriting an unrelated file.
- **S2:** Exercise occupied or modified destinations through existing install and upgrade refusal tests; a forced tracked scratch file and forbidden reference are positive controls for the report.
- **S3:** The plan identifies the real report command and input selection after layout; its documented advisory scope must match the tested entry point. It is not a release gate.
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
