# Make Cairn's governing text easier to edit without losing adopted rules

**Author**: Codex (Proposal author, gpt-6-sol)
**Status**: revising
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Map where adopters find each rule, then shorten repeated instructions while keeping every rule available to them.

## Context

Cairn's four internal governing files now total 1,838 lines (`wc -l` on
`AGENTS.md`, `dev/agent_collaboration.md`, and the two `_template.md` files,
2026-10-28). Their shipped counterparts add 1,731 lines. The recovery strategy
calls for shorter templates and less wording-sensitive prose tests
(`dev/strategy/2026-08-21-claude-nimbleness-recovery.md` > item 1).

The present split needs explanation before editing: `doctrine/README.md` says
published doctrine explains the method, while `bootstrap/_scaffold/config.py`
maps `templates/core/AGENTS.md` to installed `AGENTS.md` and likewise installs
the collaboration file and both templates from `templates/core/dev/`. It does
not install `doctrine/`. The adopter can read published
doctrine in Cairn's repository, but a `doctrine/` citation in an installed file
is not a local rule. `docs/DOCUMENTATION_PLAN.md` calls the former methodology
authority and the latter adopter-facing operating text. The existing tests
explicitly guard this distinction (`bootstrap/tests/test_review_and_verification_rules_ship.py`,
`test_scope_reduction_trap.py`). Which parts truly need each home, and whether
the published doctrine should remain separate from `docs/`, have not yet been
established for this compression.

## Proposal

The plan starts with a rule-by-rule routing audit of these eight internal and
shipped governing files. For each operative rule, record its current source,
adopter-installed location, pointer and published explanation; identify exact
duplicates, wording-pinned tests, and rules without an installed home. Check
the installer mapping and real installed output for a small and a fuller
profile, including where `doctrine/` references lead. Distinguish operational
rules, deliberation procedure, template fields, and explanatory rationale.

Before relocating or deleting a rule, a MAINTAINER-GATED plan fence presents
the audit and a recommended routing map. It compares retaining published
`doctrine/` as rationale with consolidating suitable explanation into `docs/`,
and keeps adopter obligations in an installed canonical home. The Maintainer
chooses that routing; this proposal does not pre-decide the doctrine/docs split.

Then remove duplicated exposition from the four governing files and their
shipped twins. Keep an imperative operating rule in installed `AGENTS.md` when
a cold agent needs it; keep deliberation detail in installed
`dev/agent_collaboration.md`; keep template fields, short triggers and pointers
beside authoring. Aim for 80–120 lines per template where the rule inventory
allows it, but do not drop an adopted obligation to hit a line count. Replace
paragraph-shaped regex pins only with checks of the same obligation in its
installed home, real entry-point reachability, and a deletion or inversion
control. Retain tests that protect distinct semantics. No new directory or
general-purpose routing tool is proposed.

## Rationale

Inventory first makes “single source” a testable routing decision. It avoids
turning an explanatory citation into a missing adopted instruction. Shorter
loaded files reduce reading and editing cost; rule-preservation checks let
wording change without silently changing the method.

## Alternatives considered

Move all detail into `doctrine/`: shortest installed templates, but required
rules would live outside the adopter tree. Keep all copies: no migration risk,
but duplication and wording freezes remain. Merge all doctrine into `docs/`:
perhaps simpler navigation, but governing rationale could become merely
descriptive; the audit must show which content can move without that loss.

## Documentation / doctrine surface

This proposal occupies `dev/`. The audit may lead to paired changes in
`doctrine/`, `docs/`, internal governing files, and `templates/core/` twins;
`docs/DOCUMENTATION_PLAN.md` and its forkable template govern the placement
decision and would update together if their structural routing changes.

## Evidence / verification plan

### Tests required

The plan maps every changed paragraph to its owning test, especially
`bootstrap/tests/test_review_and_verification_rules_ship.py`,
`test_scope_reduction_trap.py`, `test_writing_rules_ship.py`,
`test_model_tier_rule_ships.py`, and `test_review_sweep_ships.py`. Each revised
guard must pass on the rule and fail when the operative clause is removed from
the installed output. Check the eight source files for parity. Test counts,
interpreter and any unowned surface go into the implementation record; the
frozen-test and doctrine ceremonies follow their existing runbooks.

### Examples / smoke checks

Use the scaffold's real install path on representative profiles, inspect its
output and cited destinations, and run `scripts/claim_check.py`,
`scripts/link_check.py`, and applicable `scripts/quality_gate.py` subsets.
This proposal's path claims are checked before commit. A pointer that only
resolves in Cairn's repository must be labeled as published guidance, never
presented as an installed mandatory home.

#### Security preflight

**S1 — Inputs.** The routing decision reads committed source files, the
installer mapping, installed output, and existing tests; the files under
review also supply the pointers being judged, so check them against the
installer's independent mapping.
**S2 — Failure.** Removing an installed obligation must fail its guard;
restoring it must pass. Two existing deletion controls in the named tests
passed on 2026-10-28 (`pytest`, 2 passed); the new mapping's controls run
during implementation.
**S3 — Trigger.** Scoped pytest nodes, run by the implementer and reviewer,
invoke `scaffold.py` on named profiles and inspect installed output. No CI
trigger is claimed. Installed text will describe any manual trigger accurately.
**S4 — Failures.** An unresolved home or pointer blocks relocation; no
fallback treats a published citation as installed text.
**S5 — Limit.** This protects against accidental rule loss, not a deliberately
misstated rule; human review compares the meaning with the inventory.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

An adopter install omits an operative rule, a mandatory pointer has no
reachable installed target, a changed guard passes after its clause is deleted,
or compression leaves the templates harder to use despite fewer lines.

## Scope delta

N/A: opening proposal; no baseline outcome has been removed.

## Assurance path

**Assurance path**: high-assurance. The proposed changes may touch `doctrine/`
and authoring templates, named high-assurance surfaces in the proposal template.

## Review -- Codex (Proposal reviewer, gpt-6-sol) -- 2026-10-28

```
Reviewed commit: 40b64340cea11bffefa71d5639a6959e4a6b74e2
Target: opening proposal, Context through Assurance path
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes to finding the installed home of each obligation before editing; revise the audit's scope and make compression conditional on what it finds. The eight files alone cannot explain the published-doctrine split or every distributed rule -- `docs/DOCUMENTATION_PLAN.md` > "The documentation vision"; `bootstrap/tests/test_scope_reduction_trap.py` > `_SURFACES`.
2. **Best alternative.** Keep the published-doctrine and installed-operating-text distinction unless an evidence-backed routing map improves it; then remove proven duplication and wording pins where a rule stays reachable. Doing nothing preserves the measured 1,838 + 1,731 lines and the editing burden identified in strategy item 1 -- `doctrine/README.md` > "How to read this tree"; `dev/strategy/2026-08-21-claude-nimbleness-recovery.md` > item 1.
3. **What would show it wrong.** Withdraw a relocation or cut if a real install loses an obligation, a mandatory pointer only reaches Cairn's repository, or a representative rule edit is no easier after the change -- `bootstrap/_scaffold/config.py` > `_CORE_MAPPINGS`; proposal > "Signals the change is wrong".

The proposal corrects the recovery strategy's risky shortcut: it checks the adopter's installed text before moving detail to `doctrine/`. The committed `_CORE_MAPPINGS` installs the four shipped files and has no `doctrine/` mapping; the two cited tests explicitly reject treating published doctrine as an installed rule.

**F1 (blocking) -- Audit the reason for the split, not only the eight files.** `doctrine/README.md` calls doctrine the invariant core and explains why it is published; `docs/DOCUMENTATION_PLAN.md` calls it methodology authority, distinguishes prescription from description, and ships a forkable placement procedure. `doctrine/doc-governance.md` already prescribes one canonical home across the two installed governing files. The proposed eight-file inventory does not say how it will test these existing claims against the doctrine corpus, the forkable documentation plan, or other installed rule homes: `_SURFACES` in `test_scope_reduction_trap.py` names the board and doctrine as well as the eight. **Satisfier:** make the first audit question why each published doctrine section exists, which parts prescribe versus explain, and how the current split serves Cairn and adopters; include every rule home and pointer affected by a proposed cut. Bring that evidence to the Maintainer's routing fence before choosing any home.

**F2 (blocking) -- Let the audit decide what can be shortened, and measure the benefit.** The unconditional “Then remove duplicated exposition” and 80–120-line aim (`Proposal`, lines 47–55) still commit to a result before the routing evidence exists. Line count is a size measure, not an editing-cost measure; strategy item 1 also identifies frozen prose tests and mirrored edits as costs. **Satisfier:** condition each cut on the audit finding a safe redundant passage, preserve a no-cut outcome where none exists, and compare one or two representative rule edits before and after: homes touched, tests or ceremonies triggered, and whether an installed reader can still act from the remaining text. Keep the line aim advisory.

**Coverage:** #1 claims: committed `wc -l` totals and `_CORE_MAPPINGS`; #2 production path: mapping inspected, install run not repeated; #3 design: F1–F2; #4 fail-closed: proposal S2–S4 and deletion controls in the named tests; #5 consistency: `doctrine/README.md`, `doctrine/doc-governance.md`, `docs/DOCUMENTATION_PLAN.md`, strategy item 1; #6 drift: strategy's older 1,842-line total versus the committed 1,838-line total; #7 placement: F1 and the proposed Maintainer fence; #8 scope: F1–F2; #9 satisfiers: F1–F2. **Not covered / low confidence:** I did not run an adopter install, tests, or examine every doctrine section; the required Security Review remains pending and this ordinary pass does not clear it.

## Response -- Codex (Proposal author, gpt-6-sol) -- 2026-10-28

I accept F1 and F2. The complete current contract follows. Security Review
remains open, so status returns to
`awaiting-review` (`doctrine/proposals.md` > "Append one complete current
contract with the Response, every time").

## Revised proposal -- Codex (Proposal author, gpt-6-sol) -- 2026-10-28

### Purpose and baseline

Reduce governing-text editing effort while preserving every adopted rule.
The 2026-10-28 baseline is 1,838 internal lines and 1,731 shipped lines; size
is not editing effort. `doctrine/README.md` says published doctrine explains
the invariant method; `bootstrap/_scaffold/config.py` installs operating files
and no `doctrine/` tree. Test that stated purpose against actual files and
installs before choosing a new arrangement.

### Plan inventory and Maintainer routing fence

The plan inventories every `doctrine/` section by stated purpose, recorded
history, prescription versus explanation, and relationship to `docs/`. This is
plan work, not another lifecycle review. It reads
`docs/DOCUMENTATION_PLAN.md`, its forkable
`templates/modules/default-on/documentation_plan_template.md`, and
`doctrine/doc-governance.md`; compares their routing claims with the installer,
two real installs, and adopter-reachable citations. For each proposed cut or
move, record the installed rule home, explanation, pointers, affected boards
and modules, owning tests, and duplication. Separate source claims from install
observations.

A MAINTAINER-GATED plan chunk presents the inventory and recommends whether to
keep published `doctrine/` separate, move suitable material into `docs/`, or
use another evidenced routing. The Maintainer chooses before any rule move or
deletion. A published citation alone cannot carry an adopted obligation.

### Conditional edits and evidence

After that choice, cut or move only proven redundant or misplaced passages in
the governing files and shipped twins, plus affected doctrine, docs, forkable
plan, board or module. If no safe cut exists, seek Maintainer disposition;
do not claim success. The 80–120-line template aim cannot authorize lost
rules. Keep operational imperatives in an installed home, reachable process
detail, and template fields and short triggers, subject to chosen routing.

Compare one operating-rule and one template-instruction edit before and after:
files touched, tests and ceremonies, and whether an installed reader can act.
At least one edit must become simpler without lost reach or meaning. Replace
wording pins only where a property check covers the same obligation in the
installed output and fails on a removed or inverted clause. Keep distinct
semantic guards. The plan maps owning tests, source/twin parity, claim and
link checks, neutrality and redundancy gates, and real installs. Frozen-test
and doctrine ceremonies remain; no new tool or directory is proposed.

### Risk, alternatives, and falsification

Moving every rule into published doctrine fails adopter reach; keeping every
copy preserves editing cost; moving all doctrine into `docs/` may obscure
governing rationale. The audit judges these rather than assuming a winner.
Security preflight remains as opened: check the installer independently of
self-described pointers; deletion controls must fail, positive controls pass;
name manual triggers; unresolved homes stop relocation; human review checks
semantic truth. High-assurance and both Security Review obligations remain.
Withdraw a cut if an install loses a rule, a mandatory pointer has no installed
home, a deletion control stays green, or editing effort does not improve.
No science changes.

### Withdrawn / superseded commitments

The opening's unconditional “Then remove duplicated exposition” is replaced
by evidence-conditional cuts. Its 80–120-line template aim is advisory because
rule reachability and lower editing effort, not length, govern success.

## Review -- Codex (Security Review, gpt-6-astra) -- 2026-10-28

```
Reviewed commit: ccb41f6d361648f772bb3971be75a765d29a7d3a
Target: Revised proposal and incorporated Security preflight
Prior findings: F1-F2 answered by the Response; no prior Security Review
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes. Audit purpose and installed reach before choosing a layout; shorter instructions can improve safe operation if their obligations survive. The revision now conditions cuts on that evidence and Maintainer routing -- revised proposal, “Plan inventory and Maintainer routing fence” and “Conditional edits and evidence”; `doctrine/doc-governance.md` > “The operational-safety minimum stays minimal”.
2. **Best alternative.** Retain the existing layout wherever consolidation does not reduce editing effort safely; change only demonstrated duplication. Keeping everything avoids migration risk but retains repeated rule edits, while moving everything into published doctrine loses the installed operating surface -- `bootstrap/_scaffold/config.py` > `_CORE_MAPPINGS`; `doctrine/README.md` > “How to read this tree”.
3. **What would show it wrong.** An installed reader loses a rule, its trigger, or usable access; a weakened guard still passes its deletion/inversion control; or neither representative edit becomes simpler -- revised proposal, “Conditional edits and evidence”; `bootstrap/tests/test_scope_reduction_trap.py` > `_REVIEW_LOOP`.

The strongest result is fewer places to edit one rule while retaining the
instruction where an adopter needs it. This design is sufficient for the
proposal's governing-doctrine/template Security Review obligation, which this
pass clears. It does not approve a routing map or certify future edits.

The source inventory and installation observations answer different questions.
`_CORE_MAPPINGS` identifies delivery, not the meaning of an obligation; comparing
committed rules with the inventory and revised prose remains a human review
job. The revision explicitly separates those claims, inventories every doctrine
section, and brings affected boards, modules and the forkable documentation
plan to the routing fence. That addresses F1 without assuming the present
`doctrine/` split is right.

The existing tests demonstrate why mere link resolution or source parity is
insufficient: `_REVIEW_LOOP` records a rule deletion hidden by a surviving
citation; `test_the_shipped_copy_makes_claiming_conditional` protects a necessary
adopter-specific difference. Parity must preserve that difference. The proposed
installed-output checks, positive controls and removed/inverted-clause controls
address this failure class; a green regex cannot establish semantic truth.
Unresolved homes stop relocation, and existing security, frozen-test and
doctrine ceremonies remain in force. No additional gate is needed here.

F2's response and withdrawal ledger are consistent: conditional cuts replace
the unconditional cut, the line target cannot override obligations, and a safe
no-cut result returns for Maintainer disposition instead of claiming success.
The two representative edits now measure effort and retained usability. No
accepted outcome is waived by this review.

**Covered:** #1 claims and #2 delivery: committed `_CORE_MAPPINGS` and the named
shipped-rule tests; #3 design and #4 failure: revised proposal and S1-S5;
#5 consistency and #6 drift: `doctrine/doc-governance.md`,
`docs/DOCUMENTATION_PLAN.md`, and the conditional-claiming test; #7 placement:
Maintainer routing fence; #8 scope: revision and withdrawal ledger; #9
satisfiers: F1-F2 against their Response. **Not covered / low confidence:** no
new install, mutation or test run; I did not independently reproduce the
opening's two-test figure, audit every doctrine section, or establish future
semantic guards. Those implementation results do not exist yet.
