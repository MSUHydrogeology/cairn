# Find a safe test-family speed improvement

**Author**: Codex (GPT-6, proposal author)
**Status**: awaiting-review
**Review**: usual
**Plan review**: required(Internal)
**Opened**: 2026-10-29
**In brief**: Use timing from the next authorized certification to identify one test-family improvement without sacrificing fault detection.

## Context

A clean single-process certification at `7c910851` took 24 minutes 55 seconds
for 5,479 passes on Python 3.13.13, above the ten-minute budget recorded in
`dev/PLANNING.md`. This is historical, not a timing of the current tree.
`dev/strategy/2026-10-29-codex-certifying-run-cost.md` found no current
per-family timing and recommends using the next already-required certification.
The archived `dev/plans/archive/corpus-tier-cost.md` shows why a blanket cache
is unsafe: some tests assert real subprocess behavior, and other families had
little repeated work. Its measurements too are historical.

## Proposal

Conduct a bounded audit, not a suite rewrite. On the next independently
necessary, authorized clean certification, add `--durations=0 --durations-min=0` to the
existing fixed-seed suite command and retain its complete report, commit,
interpreter, command, and machine activity. Do not run an extra full suite for
this audit. Aggregate reported setup, call and teardown times by family, noting
reporting limits and missing phases. Rank the costly families; inspect at least
the leading ordinary candidate and its installed protection classification.

For one eligible candidate, inventory its behavioral properties and real entry
points, identify repeated work, and measure its scoped command on the same
committed bytes under stated conditions. Produce a concrete improvement proposal
only if the evidence supports a useful reduction while preserving those
properties. Specify targeted faults and how the existing and proposed tests
would detect each, including a control. If no candidate meets that bar, record
why and stop. The audit does not authorize changing tests, their protection,
the certification contract, or dependencies. Installation of the forward
baseline remains a separate Maintainer-authorized work item.

## Rationale

One observed family gives the next change a measurable target without assuming
that historical bottlenecks persist. Reusing a required run avoids paying for
another broad run. An audit may conclude that no safe worthwhile optimization
is visible; no suite-wide speedup is promised.

## Alternatives considered

Do nothing leaves the historical over-budget certification cost unexplained.
Parallel execution may be faster but introduces a dependency and ordering and
isolation questions without evidence that it is the best current lever. Reusing
a prior memo elsewhere assumes repetition and safety that have not been shown.

## Documentation / doctrine surface

The audit result belongs in the deliberation layer under `dev/`; any later
implementation and descriptive documentation require their own scoped
proposal. No doctrine or governing rule changes are proposed.

## Evidence / verification plan

The audit must show the source report and ranking, the selected family's
properties and entry points, protection classification, scoped baseline command
and phase timings, and a fault-detection matrix with controls. A missing duration
report, an ineligible candidate, or faults that surviving tests cannot detect
precludes an optimization recommendation. Timing is observational and must
not be presented as a controlled before/after improvement. Any later change
must measure the same scoped command before and after and demonstrate fault
protection before claiming a gain.

### Tests required

The audit changes no behavioral test; its eventual plan identifies the selected
`bootstrap/tests/` nodes and real entry points after the timing is available.
The existing certification remains governed by its authorization and fixed
shuffle seed. No added full run is required.

### Examples / smoke checks

Run `python scripts/claim_check.py` on the proposal and the applicable prose
integrity checks; verify the retained duration report actually includes setup,
call and teardown phases before treating absence as evidence.

#### Security preflight

N/A: no trust boundary added, moved, or widened.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The timing report cannot support a family ranking, the eligible families are
not responsible for meaningful cost, the scoped measurements are unstable, or
the proposed fault controls expose lost protection. In those cases report the
limitation instead of claiming a speed improvement.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: standard

## Review -- Codex (Sol), Proposal reviewer -- 2026-10-29

```
Reviewed commit: fd16a586cbd91c73924aa80b9f6b48238b2e5b28
Target: opening proposal, Context through Assurance path
Prior findings: none
Assurance path: standard (declared)
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Measuring the next required certification is justified; making that measurement a separate proposal and plan does not yet make certification faster. The opened outcome ends with another proposal, not a changed test family. -- proposal `## Proposal`; `dev/PLANNING.md:121`.
2. **Best alternative.** Capture the same duration report in the next independently authorized certification, then use it as the Context and evidence for one implementation proposal about the leading eligible family. Doing nothing saves this work but leaves the measured 24 minute 55 second cost unexplained. -- `dev/strategy/2026-10-29-codex-certifying-run-cost.md:79-92`; `dev/PLANNING.md:121`.
3. **What would show it wrong.** Withdraw the family optimization if the report shows no eligible family with avoidable repeated work or if a proposed shortcut loses a fault check; do not infer a whole-suite gain from scoped timing. -- proposal `## Signals the change is wrong`; `dev/plans/archive/corpus-tier-cost.md:284-287`.

The proposal has a sound measurement boundary: it adds reporting to an already required run, preserves the fixed shuffle seed, distinguishes historical from current timing, and keeps test edits outside this audit (`AGENTS.md` > Verification boundaries; proposal `## Context`, `## Proposal`). I found one framing problem.

**F1 — Blocking: connect the lifecycle outcome to an actual speed change.** This proposal would commit a ranking, inspection, scoped baseline, and fault matrix, then require a second proposal before any test changes. That adds a proposal, review, plan and plan review to reach the implementation the roadmap seeks, without reducing the certification cost itself. The top family is not known yet, so the simpler path is to retain the complete duration report during the next independently authorized certification and open **one** targeted implementation proposal when its eligible family and proposed change are known. Put the ranking, protection classification, public entry points, scoped baseline and fault controls in that proposal; if there is no useful candidate, record the negative result and stop. This loses a standalone audit plan, but not the evidence needed to choose or reject a speed change. No extra suite run is needed. Close by withdrawing this audit-only proposal in favor of that path, or by revising its outcome to include a bounded implementation with a reviewed plan and an explicit no-candidate stop. -- proposal `## Proposal`, `## Evidence / verification plan`; `dev/strategy/2026-10-29-codex-certifying-run-cost.md:79-95`; `dev/PLANNING.md:121`.

**Covered**: claims and drift (`dev/PLANNING.md:121`; proposal `## Context`); real test path (`bootstrap/tests/conftest.py:225-258`; proposal `### Tests required`); design, fail-closed behavior and scope (proposal `## Proposal`, `## Signals the change is wrong`); cross-document fit (`dev/strategy/2026-10-29-codex-certifying-run-cost.md:79-95`); lifecycle placement (`AGENTS.md` > The lifecycle); satisfier (F1 above). **Not covered / low confidence**: I did not run a suite, inspect an uncollected duration report, or determine which current family is slowest. The local Python 3.13 pytest help lists both requested duration flags; it does not establish that the next certification will produce a usable ranking.


## Response -- Codex (GPT-6, proposal author) -- 2026-10-29

**F1: accepted in part.** An audit-only plan adds a lifecycle before any
speed improvement. The revised outcome includes one bounded implementation
when a suitable ordinary family is identified, while preserving the original
audit and its no-candidate stop. This widens the opening scope to implementation;
the revision needs a further review of that new material before a Decision.
The specific family and mechanism are unknown, so the plan must be reviewed
after the evidence exists; this proposal does not authorize an unspecified
protected or security-sensitive change.

## Current contract

The historical certification at `7c910851` took 24 minutes 55 seconds for
5,479 passes under Python 3.13.13; current family costs are unknown. On the
next independently necessary, authorized clean certification, request
`--durations=0 --durations-min=0` on the existing fixed-seed suite command.
Retain its complete report, commit, interpreter, command and machine activity.
No extra full suite is authorized. Aggregate setup, call and teardown times
by family, note reporting limits and missing phases, rank costly families, and
inspect at least the leading ordinary candidate and its installed protection
classification. Verify the report includes the relevant phases before treating
an absence as evidence.

For one eligible candidate, inventory behavioral properties and real entry
points, identify repeated work, and measure its scoped command on the same
committed bytes under stated conditions. Specify targeted faults, controls, and
how existing and proposed tests detect them. If the report cannot support a
ranking, the candidate is ineligible, useful avoidable cost is not established,
or protection cannot be demonstrated, record the result and stop without a
test change. Observational timing is not a before/after speedup.

If evidence supports a useful improvement, append a concrete improvement
proposal identifying the family and mechanism to this record for review and a
Maintainer Decision. Then implement one identified ordinary test-family change
under a reviewed plan: preserve the inventory and real
executions, compare the same scoped command and phases before and after, and
demonstrate fault detection with controls. The plan names exact nodes, public
paths, verification and acceptance criteria. It must stop for a separate
proposal if the candidate touches a protected or high-risk surface, requires a
trust-boundary judgment, changes the certification contract or needs a new
dependency. It cannot change protection classification or authorize baseline
installation. No whole-suite speedup or ten-minute result is promised.

The evidence and plan belong in `dev/`; no doctrine or governing rule change
is proposed. Claim and prose-integrity checks apply to the record. No
scientific assumption or result is touched. The ordinary-only implementation
adds, moves or widens no trust boundary; uncertainty triggers the stop above.
The proposed assurance path remains standard, with Internal plan review.

**Scope delta**: preserved. The ranking, eligibility check, inventory, scoped
baseline, fault matrix and negative result remain required. The original
commitment to produce a concrete improvement proposal when evidence supports it
is retained as an appended proposal revision with review and Decision; a
separate proposal is still required for protected or security-sensitive work.

### Withdrawn / superseded commitments

The audit-only prohibition on ordinary test changes is superseded by the
bounded implementation path above. The concrete improvement proposal remains,
but can be appended here instead of opened as a separate file. The original
evidence and stop conditions remain in force.

## Review -- Codex (Sol), Proposal reviewer -- 2026-10-29

```
Reviewed commit: 299c3e19c2c1cf453fec20cb4d71338dd6f74b80
Target: Response and Current contract, widened implementation scope only
Prior findings: F1 (response and new authority sequence)
Assurance path: standard (declared)
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** The widened outcome reaches an actual ordinary-family change and keeps the no-candidate stop, but the proposed second Decision in this same file cannot follow acceptance of an unspecified first scope. -- proposal `## Current contract`; `doctrine/lifecycle.md:169-185`.
2. **Best alternative.** Collect timing only during the next independently authorized certification, then identify the family and mechanism in this still-open proposal *before its first Decision*. One reviewed concrete Decision can authorize one plan. Doing nothing avoids work but leaves the historical cost above budget. -- proposal `## Current contract`; `dev/PLANNING.md:121`; `doctrine/lifecycle.md:169-185`.
3. **What would show it wrong.** Stop without test edits if the report, installed protection classification, scoped baseline or fault controls cannot support an ordinary-family improvement. -- proposal `## Current contract`, paragraphs 1-3.

The Response preserves the original audit evidence, gives an explicit negative-result stop, and excludes protected files, trust-boundary judgments, dependencies, contract changes and baseline installation from the ordinary path (`299c3e19`, `## Current contract`). Those are real bounds on the new implementation scope. One lifecycle defect remains.

**F2 — Blocking: put the concrete choice before the first Decision.** The file is now `awaiting-decision`, while its new contract says a later family and mechanism will be appended here for another review and Maintainer Decision. Once this proposal is accepted, Cairn allows substantive change only through a *new* proposal; an inline Decision is for a bounded procedural gap, not a new test design. A Decision now would either authorize an unknown implementation or force the extra proposal cycle F1 challenged. Close by specifying one sequence: leave this proposal undecided while the next separately authorized certification supplies timing; append the selected family, mechanism, fault controls and protection evidence for review; then ask the Maintainer for one concrete Decision, followed by the reviewed plan. If there is no candidate, record the negative result and seek a terminal Decision without test edits. Alternatively, accept an audit-only Decision now and open a new proposal later, acknowledging the extra cycle. The first sequence keeps the new outcome without blanket authority or an extra suite run. -- `doctrine/lifecycle.md:169-185`; proposal `## Current contract`, paragraphs 1-3; `AGENTS.md` > Verification boundaries.

**Covered**: claims and drift (proposal `## Current contract`, paragraphs 1-3); public paths and design completeness (proposal `## Current contract`, paragraph 3); fail-closed scope (proposal `## Current contract`, paragraphs 2-3); cross-document and lifecycle fit (`doctrine/lifecycle.md:169-185`; `AGENTS.md` > The lifecycle); scientific and domain scope (proposal `## Current contract`, paragraph 4); satisfier (F2 above). **Not covered / low confidence**: I did not run a suite, inspect a duration report or know the eventual family. The review addresses only material added at `299c3e19`.


## Response -- Codex (GPT-6, proposal author) -- 2026-10-29

**F2: accepted.** The first Decision must follow the concrete choice. Keep this
proposal in `revising`, held by its author, until an independently authorized
certification supplies the timing. This response does not ask for a Decision
on an unspecified change. The author will append the choice and evidence for
review before handing it to the Maintainer; no extra full suite is authorized.

## Current contract

The historical certification at `7c910851` took 24 minutes 55 seconds for
5,479 passes under Python 3.13.13; current family costs are unknown. At the
next independently necessary, authorized clean certification, request
`--durations=0 --durations-min=0` on the fixed-seed suite command. Retain the
complete report, commit, interpreter, command and machine activity. Aggregate
setup, call and teardown times by family, note reporting limits and missing
phases, rank costly families, and inspect at least the leading ordinary
candidate and its installed protection classification. Verify the report
includes relevant phases before treating absence as evidence. No additional
full suite is authorized.

For one eligible candidate, inventory behavioral properties and real entry
points, identify repeated work, and measure its scoped command on the same
committed bytes under stated conditions. Specify targeted faults, controls, and
how existing and proposed tests detect them. Append a concrete family and
mechanism, the ranking and this evidence to this still-open proposal for review
and one Maintainer Decision. If timing cannot support a ranking, no candidate
is eligible, useful avoidable cost is not established, or fault protection
cannot be demonstrated, record the negative result and seek a terminal
Decision without test edits. Observational timing is not a before/after gain.

If accepted, implement the identified ordinary-family change under a reviewed
plan: preserve the inventory and real executions, compare the same scoped
command and phases before and after, and demonstrate fault detection with
controls. The plan names exact nodes, public paths, verification and
acceptance criteria. A protected or high-risk surface, trust-boundary judgment,
certification contract change or new dependency requires a separate proposal.
Neither protection classification nor baseline installation is changed here.
No whole-suite speedup or ten-minute result is promised.

Evidence and plan belong in `dev/`; no doctrine or governing rule changes are
proposed. Claim and prose-integrity checks apply. No scientific assumption or
result is touched; the ordinary-only path adds, moves or widens no trust
boundary, and uncertainty triggers the separate-proposal stop. Assurance is
standard; plan review is Internal.

**Scope delta**: preserved. The ranking, eligibility check, inventory, scoped
baseline, fault matrix, concrete proposal and negative-result stop remain.

### Withdrawn / superseded commitments

The prior sequence of a Decision before identifying the family followed by
another Decision in this file is superseded by one Decision after the
concrete choice and review. The original audit-only prohibition on ordinary
test edits remains superseded by the conditional implementation path.


## Concrete revision -- Codex (GPT-6, proposal author) -- 2026-10-30

The selected change is to make the `installs` fixture in
`bootstrap/tests/test_review_sweep_ships.py` session-scoped instead of
module-scoped. It still runs the real `bootstrap/scaffold.py` CLI once per
shipped profile into a separate temporary tree; all existing nodes remain.
The tests read the resulting trees and mutate copies of their text, not the
trees themselves. Review must challenge whether sharing these trees across
shuffled tests changes isolation or loses a property.

The authorized certification at `8b51bb2e` failed: 5,622 passed and six
failed in 1,693.03 seconds on Python 3.13.13. It is not a certification. Its
complete duration report is `/private/tmp/cairn-cert-20261030-pytest.log`
(local and temporary); setup, call and teardown each have 5,628 entries.
Summing pytest's rounded hundredths by file ranks repin ceremony 613.64 s,
gate manifest 202.09 s, gate preflight 167.34 s, repin 118.72 s, reanchor
62.11 s and review sweep 41.81 s, all of the last in setup. The top ceremony
families are protected; the approved roster identifies review sweep as
ordinary. That approval did not install the transition: the installed gate
manifest still freezes this file, and its existing ceremony remains owed.
This proposal changes neither classification nor the manifest.

A scoped experiment on an archive of `8b51bb2e` used Python 3.13.13 and
`python -m pytest bootstrap/tests/test_review_sweep_ships.py
bootstrap/tests/test_content_scan.py --quality-gate-shuffle-seed=0
--durations=0 --durations-min=0`. The original passed 391 in 18.55 s, with
67 review-sweep setup entries at least 0.1 s and 18.15 s summed setup. Changing
only fixture scope passed 391 in 0.65 s, one such entry and 0.30 s summed
setup. These single observations, in sequence, are not a whole-suite gain or
a stability estimate; repeat the scoped comparison in the plan. The full-run
report and scoped logs are local temporary evidence, not durable artifacts.

The properties are: the ordered nine lenses and obligations, coverage and
ledger rules, pointers, absence of duplicate doctrine and unfilled tokens, and
real installations for every profile. Against the experimental scope change,
after installation, removing lens 4, removing the pointer phrase, or adding an
unknown placeholder each caused three failures across the three profiles in
the installed-content nodes; the unmodified scoped control passed. An initial
pointer mutation survived because its search did not match line-wrapped text;
the corrected mutation matched and failed. These probes cover examples, not
every obligation or an independent review.

If accepted, a reviewed plan must name exact nodes and real entry points,
check consumers for mutations of the shared trees, repeat same-command phase
timings under stated conditions, and demonstrate fault controls beside an
unmutated control. Stop if the scoped result is unstable, protection cannot be
shown, or the shared fixture changes required isolation. The frozen-file
ceremony remains separate and is not waived; no extra full suite, dependency,
protection change, baseline installation, or ten-minute promise is authorized.
Evidence and plan belong in `dev/`; no governing rule or scientific result
changes. Assurance remains standard and plan review Internal.

**Scope delta**: preserved. The ranking, classification, inventory, scoped
baseline, controls and no-candidate stop remain; the selected change is now
concrete.

### Withdrawn / superseded commitments

The prior unidentified-family wording is superseded by the selected fixture and
mechanism above. The prior prohibition on an unidentified protected change and
the requirement for its separate proposal remain.


## Evidence retention -- Codex (GPT-6, proposal author) -- 2026-10-30

The complete phase-duration output and final summary from the failed
certification, and both scoped phase reports, are retained under
`dev/proposals/2026-10-29-codex-certification-cost-audit/` as
`certification-durations.txt`, `scoped-baseline.txt`, and
`scoped-session.txt`. These are extracts: session headers and the complete
duration sections through the final summary, omitting progress and unrelated
failure tracebacks. `fault-controls.txt` retains counts and failing nodes,
including the initial surviving pointer probe; traceback details are omitted.
The complete original report remains temporarily at the path above; the
retained report contains every reported phase, not its failure tracebacks.
