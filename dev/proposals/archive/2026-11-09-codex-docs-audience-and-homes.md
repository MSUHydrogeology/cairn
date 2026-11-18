# Clear guide navigation and homes for Cairn's own operating instructions

**Author**: Codex Sol (Strategy)
**Status**: accepted
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

The [repository-layout proposal](archive/2026-11-09-claude-repository-layout.md)
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
   Correct `docs/DOCUMENTATION_PLAN.md`'s inventory: remove `release-process`
   from the descriptive-layer examples and identify the relocated procedure
   as domain-local release governance. This applies the existing layer rules;
   it does not redefine them.
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
Confirm the documentation map classifies the relocated procedure as
domain-local governance and no longer lists it as descriptive content.
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

The ordinary review is answered below; the v0.8 proposal awaits the Maintainer's Decision.

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

## Response -- Terra (revising author) -- 2026-11-12

**F1 accepted.** Item 3 now explicitly corrects the documentation map's
inventory: the relocated release procedure is domain-local governance, not a
descriptive-layer example. Verification checks that classification alongside
the existing requirement-preservation comparison. This resolves the map's
contradiction by applying its current rules, without changing those rules or
widening the proposal.

Re-read the opening through Assurance path after revision: the v0.8 target,
light lane, layout prerequisite, complete release duties, adopter references
and protected-surface reassessment remain intact. The prior draft-only note is
updated to reflect the completed ordinary review. No further review is sought;
the next action is the Maintainer's Decision. This response does not verify
the future relocation, commands or inbound-link inventory.

**Elapsed**: unknown. **Tokens**: unknown.

### Withdrawn / superseded commitments

None.

## Decision -- Maintainer (scribed by Antigravity Gemini 4 Hydrogen) -- 2026-11-12

**Tier**: light

**ACCEPTED.**

> "Accept all four as revised, retaining core meter installation for v0.7"

This accepts the v0.8 guide navigation and Cairn-only instruction placement proposal as revised, to be executed in the light lane after the v0.8 repository layout lands. New recurring human operations: zero.

**Elapsed:** under 1 minute. **Tokens:** unknown.

## Implementation -- Terra (Implementation) -- 2026-11-18

Moved the release procedure byte-for-byte to `release/RELEASE_PROCESS.md`;
its duties and commands are unchanged. The guide index now offers the three
accepted routes, and count maintenance lives beside its tools in
`tests/README.md`. The documentation map identifies release governance in its
new home. Live links and the release-membership reader follow the move;
archived deliberation remains historical. The board's live references are
coordinated separately with the arc owner.

The release-membership sequence selection passed six cases under Python
3.12.9 (noncanonical; the arc will cover the committed change under 3.13); link, snippet, neutrality, claim and Cairn document checks passed on
the changed documents. The proposal's own claim check reports historical paths
in its context and review, preserved as evidence. The release procedure
compared equal to its original; no release or certification ran. Final
committed-byte change verification belongs to the arc's joined integration.

**Benefit versus cost**: unknown -- clearer audience routes and local authority;
cost and remaining burden unknown. Revisit if users cannot find a guide or
release duties drift. Elapsed: unknown. Tokens: unknown.

## Completion -- Codex (Implementation) -- 2026-11-18

The committed implementation `d43c31dc` passed the six release-membership
sequence cases under canonical Python 3.13.13 in 1.21 seconds. This covers
documented command order, omitted security results, pytest failure and refusal
to overwrite an existing report. It supplements the earlier Python 3.12.9
result; neither is a whole-tree certification. The release procedure moved
without byte changes. No release, signing or baseline operation ran.

The arc owner updates the live board routes and finalizes only the committed
documentation-map hash. No new tool, recurring check or follow-up is needed.

**Benefit versus cost**: worth it -- clearer guide routes and maintenance
instructions beside their tools; implementation changed 10 files, with 83
insertions and 52 deletions, and the canonical focused checks took 1.21 seconds.
Agent elapsed time and token use are unknown. No always-loaded instructions or
installed file count changed. Revisit if users cannot find the right guide.
