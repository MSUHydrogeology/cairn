# Make installed Cairn materials findable

**Author**: Terra (Implementation)
**Status**: awaiting-decision
**Review**: usual
**Proposed tier**: light
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-18
**Elapsed**: unknown
**Tokens**: unknown
**Rules that apply**: `dev/rules/conventions.md`, `dev/rules/working-agreements.md`
**In brief**: Give people using Cairn a practical route to every installed template, guide and tool.

## Decision summary

Some installed materials are difficult to find from the guidance people actually read. Audit the current installed roster and add concise navigation in existing installed guides or folder inventories where a useful route is missing. Module inventory rows and seeded tasks already give routes to selected modules; skill discovery and human-facing documents can also stand alone when their context makes them findable. This adds a small amount of navigation to maintain, but no new discovery tool or recurring wording test. If an installed item appears too costly to retain, bring its full scope to the Maintainer for a separate Decision rather than quietly omitting it.

## Context

The Group 4 row in `dev/PLANNING.md` records an older name screen, not a current inventory. The repository layout has since changed. The installer maps files in `install/_scaffold/config.py`, and `templates/core/dev/modules/README.md` plus seeded tasks route readers to selected modules. `tests/test_onboarding_seed_roster.py` checks that existing module roster behavior. Navigation should be judged on the current install and actual reader journeys, not the old counts.

## Proposal

For v0.8, inventory every installed template, guide and executable tool across the current supported selections, using the published install manifest and actual install mappings. Make a one-off development inventory that records each item and a concrete route a reader can follow from installed entry guidance, a relevant folder inventory, a selected-module row or task, or the normal skill and human-document discovery context. Include supporting tools with a meaningful user-facing use; distinguish implementation-only helper files and configuration from tools a user invokes, while accounting for them in the inventory. Check routes in an actual representative install and against the selection-dependent mapping.

For each item lacking a practical route, add the smallest useful direction to an existing installed guide or folder README. Explain a tool's purpose where needed, not merely its filename. Preserve existing duties and the always-loaded word cap; do not add pointers solely to satisfy name matching. Do not remove installed items under this proposal. If a genuinely unused item seems expensive to retain, present its use, cost and full proposed removal scope to the Maintainer for a separate Decision. Do not change installer behavior or add a permanent test of wording or link absence; if those become necessary, stop and reassess the tier.

## Rationale

An inventory grounded in what ships covers more than a search for old names, while existing module and skill discovery avoids duplicate navigation. A one-off audit has no continuing automation cost.

## Alternatives considered

Leave discovery to directory browsing: no documentation maintenance, but an adopter may never learn that a useful tool exists. Add a permanent navigation test: it adds maintenance and cannot judge whether a route is useful.

## Documentation / doctrine surface

Change only the applicable installed guide and README prose under `templates/`, and corresponding descriptive navigation in `docs/` where needed. Preserve agent duties in their installed authoritative homes; no new governing rule or installer contract is proposed.

## Evidence / verification plan

### Tests required

No new behavioral test is proposed: the deliverable is navigable prose, not a new runtime promise. Reuse the existing module inventory and seeded-task checks when they name changed files; select other affected checks with `tests/tier_inventory.py`.

### Examples / smoke checks

Inspect the one-off inventory against actual installed destinations and trace a sample of routes in a fresh install, including a selected module, a template and a previously unnamed tool. Check any negative search against a known positive. Run applicable prose gates and claim checks. A shipped item with neither a usable route nor justified discovery context falsifies completion.

#### Security preflight — five questions, answered in writing

N/A: no trust boundary added or widened; prose navigation changes no installer behavior.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Readers still cannot find an installed item when they need it, or navigation adds more noise than useful direction.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: standard. The work changes prose navigation only; installer structure and executable behavior are outside scope. Light review is proportionate and needs no plan.

## Review -- Terra (Reviewer) -- 2026-11-18

Reviewed commit: cebffc71e4afc6251a76d5b3efefc797ec26560a

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: tracing the current installed roster serves readers after the layout change without adding a permanent wording gate; selection-dependent mappings are the right starting point. -- `install/_scaffold/config.py`
2. **Best alternative.** Directory browsing costs no navigation maintenance but can leave useful material undiscovered; existing selected-module rows and seeded tasks reduce the need for duplicate pointers. -- `templates/core/dev/modules/README.md`, `tests/test_onboarding_seed_roster.py`
3. **What would show it wrong.** A fresh installed selection containing an item with no usable route or justified discovery context would falsify completion; trace the inventory and sample routes as proposed. -- Proposal, Evidence / verification plan

The proposal retains the board's practical discovery outcome and lets skills and human documents stand on their own where their context works. Light review is proportionate because the proposed work changes navigation prose and does not change the installer or introduce a new boundary. Applicable agent duties must remain in their installed authoritative homes; the proposal explicitly preserves them. -- `dev/PLANNING.md`, Proposal, Documentation / doctrine surface

Coverage: read the board, installer mappings, module inventory route and proposal; did not execute an install, enumerate every installed item, or verify future prose. No test suite was run.

## Response -- Terra (Implementation) -- 2026-11-18

The ordinary review found no issues requiring a change. The proposal remains as reviewed and is ready for the Maintainer’s decision.

**Elapsed**: unknown
**Tokens**: unknown

### Withdrawn / superseded commitments

None.
