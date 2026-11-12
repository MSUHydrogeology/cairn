# Proposal: Meter install footprint for v0.7

**Author**: Terra (ordinary proposal author, Medium)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**Target release**: v0.7
**In brief**: Decide whether to make the existing cost meter an optional installation while preserving its current users and dependent workflows.

## Decision summary

Offer an opt-in meter module for new v0.7 installs, provided an upgrade
preserves existing adopters' meter and its dependent workflows. The alternative
is to keep installing it in core for everyone. Moving it saves non-users an
installed executable, but adds a module, upgrade and compatibility work; the
net cost is not yet measured, so retain core installation until a comparison
justifies changing it. The opt-in contract below is the alternative for the
Maintainer to choose, not an automatic default change. This proposal does not
stop, shrink or replace
the active meter implementation, or authorize private data collection.

## Context

The [v0.7 weight review](../strategy/2026-11-06-claude-v07-weight-review.md)
recommendation 4 proposes an optional module and a later question about a
smaller meter. The [board](../PLANNING.md) row 13 calls for a separate Decision;
the active [meter plan](../plans/2026-11-04-metered-cost.md) owns the existing
collector and remains in implementation. Its delivery contract installs the
meter alongside session and board. The pending [layout proposal](2026-11-09-claude-repository-layout.md)
also treats meter as core; reconcile the two before implementation, not by
assuming either has decided the other.

Measured in this checkout on 2026-11-12, `tools/meter.py` and its shipped
source `templates/skills/_lib/meter.py` are each 6,218 lines and 294,762 bytes
(`wc -l -c`). That is source size, not installed runtime, user burden or a
measurement of private usage. The weight review's earlier counts are historical.
The meter plan's comparisons and conditional Tokens retirement remain open;
the board places the private, separately opted-in comparisons in v0.9.

## Proposal

If the Maintainer chooses the opt-in alternative for v0.7, make the existing
meter optional for new installs without changing capability or collection
consent. Otherwise retain core installation and its accepted plan unchanged;
no migration or smaller replacement is implied. An existing
adopter's upgrade must preserve its installed meter, configuration, data and
working behavior; choosing a module for a new project must not silently remove
or disable an existing user's capability. The implementation must establish
how existing installs are recognized and retained, including modified files,
before any install-contract change ships. Previously implicit selection in a
valid tracked core install becomes retained module selection during upgrade;
a local executable's presence alone is not installation evidence. Ambiguous
provenance refuses affected migration without deleting files or data.
Do not assume how many adopters use
it, or infer consent from installation.

Preserve the accepted meter plan and coordinate timing with its owner. Trace
session handoff, claims preservation, meter refresh and report consumers,
including their absent, disabled and failure behavior, through the actual
installed paths. An install without the module must still support normal
session work without falsely reporting collection or losing claims. A validated
meter-unselected install permits normal guarded full-handoff pruning without
meter refresh, reporting "not selected", not "refreshed" or "passed". This is
distinct from selected-but-disabled collection, which uses its validated
disabled receipt. A selected collector unexpectedly missing or failing keeps
the existing failure result and preserves claims by skipping pruning. No
private source is read merely to determine module selection. Existing
enabled users must retain the accepted refresh and reporting guarantees. Keep
manual Tokens and Elapsed and all outstanding comparison and retirement
conditions; this proposal does not authorize a smaller replacement, retirement,
new source access or changes to data governance.

Before a plan is ready, map the current install, upgrade and module contracts,
dependencies and tests; quantify bytes/files avoided for representative new
installs and the added implementation, migration and maintenance cost. Report
unknowns and non-passes rather than treating missing evidence as compatibility.
If preserving the contracts requires a new trust-boundary design or a change
to accepted scope, stop for High design and the Maintainer's separate
direction; this proposal specifies no new security primitive. The Maintainer
may instead retain core installation if the measured tradeoff or compatibility
cannot justify the module.

## Rationale

An optional install can reduce the executable footprint for projects that do
not choose metering while retaining it for projects that do. The tradeoff is
real: another module and upgrade path must be maintained and verified, and
session and reporting behavior must remain coherent in both configurations.
Source bytes alone do not establish that the savings outweigh that cost.

## Alternatives considered

Keep the meter in core: no new selection or migration path, and the active
delivery contract stays simple, but every new adopter receives the executable
even without using it. This is the strongest alternative if compatibility or
module costs outweigh the measured saving. A smaller meter is a separate
question; replacing the current one here would silently narrow accepted work.

## Documentation / doctrine surface

Deliberation stays in `dev/`; implementation would update the installed module
inventory and meter usage guidance, install/upgrade contract and descriptive
documentation as needed. Governing prescription changes, if needed, belong in
the governing layer, not only in descriptive docs. Identify exact surfaces in
the plan after tracing the actual install and consumers.

## Evidence / verification plan

Compare new core-only and meter-selected installs and upgrades from an existing
meter install, including modified files, against the current contract. Measure
actual installed files and bytes and record the added ongoing module and
migration obligations. Trace the layout proposal and active meter plan at the
implementation baseline. A lost existing capability, broken handoff or report,
unconsented collection, or an unsubstantiated saving falsifies the proposal's
delivery claim.

### Tests required

Map exact public-entry test nodes in the plan, including the existing
`bootstrap/tests/test_skills_install.py`, `bootstrap/tests/test_skills_upgrade.py`
and `bootstrap/tests/integration/test_meter.py` homes and session and reporting
consumers. Exercise real scaffold install/upgrade and installed session and
meter entry points for absent, selected, existing, modified, disabled and
failure cases; add or extend tests for uncovered faults. Preserve the active
meter plan's required checks, including platform-specific evidence. Exact nodes,
platform coverage and migration fixtures are not yet established.

### Examples / smoke checks

Exercise scaffold summary, dry-run and manifest for both selections and an
upgrade in a disposable project; run the applicable prose gates. No private
sources or real adopter data are needed or authorized for these checks.

#### Security preflight

- **S1 -- Inputs:** The installer reads the project-selected profile, installed
  module/lock records and tracked file provenance. They establish installation
  state, not collection consent. Private collection still needs its separate
  project/root opt-in, under the accepted meter contract; executable presence
  or module selection supplies no such authorization.
- **S2 -- Falsifiers:** Through real install/upgrade/handoff entry points,
  contrast intentional nonselection, selected-disabled, enabled-missing,
  enabled-failing and ambiguous upgrade records. Plant a modified tracked meter
  and an occupied destination. Nonselection must not masquerade as refreshed;
  failures must not prune claims or erase modified files. No such future-path
  controls have run yet.
- **S3 -- Triggers:** The accepted plan's implementation mapping owns focused
  install, upgrade, session and reporting checks in both module configurations,
  then independent ordinary/Security code reviews and final wide verification.
  It must cover existing installations before the default can change, not
  merely demonstrate a clean new install. No extra suite trigger is proposed.
- **S4 -- Failure:** Unvalidated selection/provenance cannot authorize the
  meter-free pruning path. Unexpected missing or failed selected collectors
  retain their refusal and claims. Unknown usage remains unknown; no optional
  module failure is reported as successful collection. If compatibility fails,
  retain core installation rather than silently remove capability.
- **S5 -- Residual:** Module and consent records are cooperating-user local
  state, not cryptographic proof of actor identity. A compromised host remains
  outside the meter's containment claim. Optional installation changes disk
  footprint, not model billing or collection safety by itself. Further trust
  design beyond this contract still requires High reassessment.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Withdraw the recommendation if a compatible upgrade cannot be demonstrated,
if the module's measured and continuing costs exceed its useful savings, or if
dependent workflows cannot retain their accepted guarantees without a further
unapproved change.

## Scope delta

The alternatives and accepted meter capabilities are preserved. After review,
the recommendation changes from conditional opt-in to retaining core until
the comparative evidence supports migration. The opt-in contract is retained
for the Maintainer's choice; no implementation outcome is silently removed.

## Assurance path

**Assurance path**: high-assurance

The proposed install contract and adopter-executed tool require this path.

**Elapsed**: unknown. **Tokens**: unknown.

## Review -- Terra (ordinary Reviewer, Medium) -- 2026-11-12

Reviewed commit: 59e01102b500d2429af72b500f7539c0147847dd

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

The strongest case is letting non-users avoid an executable without taking
capability or consent choices away from existing users.

**Foundations**

1. **Should this happen as framed?** Conditional exploration is reasonable, but changing the default is not yet justified by measured benefit or a complete absent-meter contract. -- Proposal; `tools/session.py` lines 1915-1924 and 2319-2321.
2. **Best alternative.** Retain the disabled-by-default core executable for v0.7; this avoids another selection/migration path but retains 294,762 installed source bytes. -- `bootstrap/_scaffold/config.py:917`; committed meter bytes.
3. **What would show it wrong?** Real installed handoffs must distinguish intentional nonselection from a missing enabled collector, preserve claims on failure, and retain refresh/reporting for existing users. -- Meter plan C2; `bootstrap/tests/test_session_writes_contained.py`.

1. **Non-blocking: specify intentional absence.** The proposal already requires tracing absent/disabled/failure behavior. State its observable outcome: does an intentionally meter-free full handoff succeed and prune, or preserve claims and return unavailable? Today missing meter returns false, skips both pruners and exits 5. Close with an explicit caller contract and real-entry coverage contrasting nonselection with accidental loss; do not silently weaken enabled-user retention. -- `tools/session.py` lines 1915-1924 and 2319-2321.
2. **Blocking: supply the required proposal preflight.** Security preflight defers all five answers, although this proposal already changes the install/executable contract. The template requires answers while design is movable. Close with proposal-level inputs, failure controls, triggers, fallback and residual assumptions; mark unrun evidence honestly and reserve new boundary design for High. -- `dev/proposals/_template.md`, Security preflight.
3. **Non-blocking: prefer core until savings justify migration.** One inactive file's source size is not recurring user cost. The proposed cost mapping is useful; bring its result to the Decision or recommend core pending evidence, rather than selecting a module first. -- Meter plan Delivery; Proposal's unmeasured net cost.

**Audience / rule loss:** The summary is understandable. No current duty is
removed here; finding 1 needs resolution before installed duties change.

**Coverage:** Verified both copies at 6,218 lines/294,762 bytes and opening at
1,028 words; read accepted scope/Decision, current plan, install mappings,
session receipt/pruning and Gauge's optional aggregate input. No runtime,
private data, historical strategy recount, suite or Security clearance.
Over 300 words to distinguish an unspecified contract from already-promised
dependency tracing and record the required preflight gap.

## Security Review -- Sol -- 2026-11-12

Reviewed commit: 59e01102b500d2429af72b500f7539c0147847dd

**Tier**: Security Review
**Model basis**: Sol High, explicitly assigned by the Maintainer through the coordinator.
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: read/probes unknown; recording/checks unknown.
**Tokens**: unknown

The strongest case is a smaller new-install footprint without taking capability,
consent controls or historical evidence away from existing users.

**Foundations**

1. **Should this happen as framed?** Potentially: consent and accepted scope are preserved explicitly, but required security accounting is deferred. -- Proposal, Security preflight.
2. **Best alternative.** Keep core installation if savings cannot justify compatibility work; collection already stays disabled without private opt-in. -- `tools/meter.py:3975`.
3. **What would show it wrong?** Allowing pruning after an enabled collector unexpectedly disappears falsifies claim preservation. Synthetic probes confirmed absent collector refuses pruning, while valid disabled receipts permit it. -- `tools/session.py:1883`, `tools/session.py:1915`.

1. **Blocking: answer the security preflight now.** The proposal defers all five answers unless implementation widens a boundary. The current template also requires them for named high-risk surfaces, including this install contract (`dev/proposals/_template.md`, Security preflight). Deliberately uninstalled, explicitly disabled and unexpectedly missing are different authority states. **Closure:** answer S1-S5 for adopter recognition, selection and absent-meter handling; distinguish installation evidence from collection consent, retain refusal for unexplained failures, and name falsifiable checks and triggers. Report unperformed checks honestly rather than conditionally postponing the obligation.

**Audience / rule loss:** The summary is clear. Existing scope, manual
Tokens/Elapsed and consent restrictions remain; rewritten installed instructions
were unavailable.

**Covered:** I read committed rules/template, upgrade, session, consent and
reporting consumers. Synthetic probes confirmed disabled/missing consent avoids
ledger access, current ledger round-trip and legacy conversion retaining unknown
history (`tools/meter.py:2462`). Both meter copies match 6,218 lines/294,762 bytes.
**Not covered:** private data, real migration, native Windows or suites. This
records the previously reported first pass after ordinary review serialization,
not an additional pass.

## Response -- Codex Sol (High), revising author -- 2026-11-12

1. **Ordinary 1:** Specify observable handoff behavior for validated module
   nonselection: guarded handoff may finish without refresh, reported as not
   selected. Selected-disabled still uses its disabled receipt; an unexpectedly
   absent or failed selected collector still preserves claims and refuses
   pruning. Missing executable bytes alone establish neither nonselection nor
   consent. Existing user capability, private opt-in and unknown data remain
   protected.
2. **Ordinary 2 / Security 1:** Replace deferred preflight with S1-S5, naming
   profile/installation provenance, separate consent, failure outcomes,
   existing check/review triggers and residual local-state assumptions.
   Future migration and module controls are explicit unrun implementation
   evidence, not represented by the Security review's current-code probes.
3. **Ordinary 3:** Agree. Retain core until comparative evidence justifies
   migration, rather than treat 294,762 source bytes as proven recurring
   burden. The Maintainer can choose the opt-in alternative with its stated
   preservation requirements and cost uncertainties. Neither choice authorizes
   shrinking the accepted all-three meter or private collection.

The summary was revised with the recommendation and v0.7 target. This is ready
for a Decision, not implementation; the active meter plan remains unchanged.

### Withdrawn / superseded commitments

The opening conditional opt-in recommendation is superseded by retaining core
pending comparative evidence. The opt-in alternative and all preservation
outcomes remain. Deferring the required S1-S5 answers is withdrawn. No accepted
meter capability, check or consent requirement is removed.

**Elapsed**: approximately 8 minutes. **Tokens**: unknown.
