# Clear guide navigation and homes for Cairn's own operating instructions

**Author**: Codex Sol (Strategy)
**Status**: revising
**Review**: usual
**Proposed tier**: light
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-09
**Target release**: v0.8
**In brief**: Keep Cairn's guides focused on using it, while placing its own release and maintenance instructions beside the tools they govern.

## Decision summary

For v0.8, make the guide index distinguish **Using Cairn**, **Reference** and
**Contributing to Cairn**. Move the authoritative release procedure beside the
release machinery, and separate Cairn-only count-maintenance instructions
from the adopter tool guide. Keep technical references useful to adopters in
`docs/`; technical content is not automatically contributor-only content.

Coordinate this small cleanup with the repository-layout change. No new guide
hierarchy, documentation framework, release requirement or review stage is
needed. Costs are updating links, navigation and affected path readers; no new
routine human operation or recurring report is introduced.

## Context

`docs/README.md` already groups guides by purpose and has a section titled
"Maintaining Cairn itself". That section links to `docs/release-process.md`,
which is a mandatory procedure for cutting Cairn releases, not an adopter
guide. `docs/tool-usage.md` mixes adopter tools with a section specifically
for Cairn maintainers using `verify_counts.py`.

`docs/DOCUMENTATION_PLAN.md` already distinguishes descriptive documentation
from operational authority and allows domain-local governance beside the
domain it governs. It is itself documentation governance, rather than an
ordinary user guide. `dev/rules/README.md` describes project-owned agent
discipline read on demand; it is not a catch-all developer manual.

The [repository-layout proposal](2026-11-09-claude-repository-layout.md)
would establish `release/` and move Cairn-only test/reporting tools. This
proposal clarifies the companion document destinations and audience, without
repeating or authorizing those executable moves.

## Proposal

Deliver in v0.8 once the layout's destination folders and tool homes exist:

1. Move the complete release procedure to `release/RELEASE_PROCESS.md`, beside
   its runbooks and tools. Preserve every release requirement, including the
   follow-up reconciliation, strategy retirement and board cleanup. Change
   only location, relative links and command paths required by the accepted
   layout. Do not leave a competing copy in `docs/`; keep a navigation link.
2. Move the "For Cairn maintainers" count-maintenance instructions from the
   general tool guide into the existing README or documentation at that
   tool's final internal home. If no such document exists, use one short
   README there rather than start a developer-guide tree. Keep a brief link
   in the tool guide and remove the duplicate explanation. The layout work
   owns the executable destination; this proposal does not choose a new one.
3. Reorganize `docs/README.md` under **Using Cairn**, **Reference** and
   **Contributing to Cairn**. Preserve its useful entry paths, including
   adoption, everyday use and published methodology. Place the documentation
   plan in the contributor navigation while retaining its current file home.
4. Retain skills compatibility, code-map reference, building a board view and
   published methodology under `docs/`: they explain capabilities or the
   method to people using Cairn. Do not move them merely because their
   readers are developers. Keep runnable mini-projects at root `examples/`,
   as the [examples proposal](2026-11-09-codex-worked-examples.md) explains.
5. Repair live inbound links, anchors, source claims and affected readers.
   Coordinate any protected path-reader changes with the layout work under
   its existing assurance. A protected-file change or new boundary needed
   beyond that authorized work requires reassessment before editing, not an
   assumption that this light proposal authorizes it.

Keep implementation on this proposal in the light lane, after the layout
capability is delivered; no plan is proposed. Do not open implementation while
its destination or authority is unavailable. Estimate: one agent work session
plus its required review and checks, with uncertainty in the inbound-link
inventory. This scheduling grants no implementation or review authorization.

## Rationale

Location should distinguish explanation from operating instructions, not
"nontechnical" from "technical" readers. Navigation can serve both adopters
and contributors without a second folder hierarchy. The release procedure
has a natural domain home; the documentation plan already lives in its own
domain and need not move.

## Alternatives considered

- **Only relabel the index.** Cheapest, but leaves the authoritative release
  procedure separated from the machinery it governs and preserves the mixed
  tool guide.
- **Move all technical pages to a developer guide.** Would hide useful
  adopter references and add another classification burden.
- **Put the release procedure in `dev/rules/`.** Possible for project-specific
  discipline, but less direct than the dedicated release domain already
  proposed. It would also split the procedure from its runbooks.

## Documentation / doctrine surface

Descriptive navigation and tool explanation remain in `docs/`. Operational
release authority moves intact with its domain. Deliberation stays in this
proposal. Do not alter `AGENTS.md`, shipped doctrine or templates under this
scope, and do not redefine documentation-layer rules.

## Evidence / verification plan

### Tests required

Use the existing path-reader mapping for moved or edited files and run the
focused release-membership contract tests that execute the documented release
command block. Compare the relocated procedure against the original: each
difference must be a declared path/link correction, not a changed requirement.
Do not run a release or full certification merely to relocate instructions.

### Examples / smoke checks

Inventory live inbound links before moving the procedure; verify every
inventoried reader resolves to the new location afterward. Run claim, link,
snippet and neutrality checks on changed documents, and manually follow each
of the three index routes. Record any unresolved external or historical link
limitations rather than rewriting archived deliberation. Perform the required
final change-verification selection on committed bytes.

#### Security preflight

N/A: no trust boundary added or widened. Release duties and command behavior
remain unchanged. If a move requires new executable or protected changes not
covered by the layout's accepted scope, reassess their assurance first.

### Independent scientific check

N/A: no scientific assumption, algorithm or result changes.

## Signals the change is wrong

A release duty disappears, a command changes beyond its required path update,
an adopter reference becomes harder to find, or old and new procedures both
remain authoritative.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: standard

Draft only; no review or Decision has been requested in this step.

Proposed paths:
- `release/RELEASE_PROCESS.md`

## Review -- Terra Medium -- 2026-11-12

Reviewed commit: be015399831b62898f10696191cd60b1b325a6c1

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**
1. **Should this happen as framed?** Yes, subject to resolving the existing map's conflicting classification: the move puts release duties by their machinery without hiding adopter references. -- Proposal items 1, 3-5; `docs/DOCUMENTATION_PLAN.md` > Governing layer
2. **Best alternative.** Relabel the index alone if the layout is not authorized; it retains the existing procedure and avoids a premature destination, but leaves maintenance instructions mixed into user guides. -- Proposal Alternatives; `docs/tool-usage.md` > For Cairn maintainers
3. **What would show it wrong.** Compare every release duty and follow each live route after the layout lands; a missing duty or unreachable authority would falsify the move. -- `docs/release-process.md` > Method, for every sweep; Proposal Evidence / verification plan

**F1 (non-blocking): Reconcile the documentation map.** The proposal calls the release procedure operational authority and forbids redefining layer rules, but `docs/DOCUMENTATION_PLAN.md` > Descriptive layer lists `release-process` as descriptive. A move and link repair alone can leave the map contradicting its new home. Close by explicitly updating that classification without changing the layer rules, or explain with evidence why it remains accurate.

**Rule loss and audience.** No loss is proposed: item 1 preserves the complete procedure and item 2 moves maintainer instructions, while adopter references remain in `docs/`. The comparison must check the actual moved text and commands, including the release-membership reader in `bootstrap/tests/contract/test_release_members_contract.py`.

**Coverage.** Read the committed proposal, layout proposal, release procedure, tool-guide section and documentation map; checked live path references including the contract reader. Did not execute a release, inventory every reader, inspect future layout changes, or perform Security Review; the destination and its authority remain contingent on that separate work.
