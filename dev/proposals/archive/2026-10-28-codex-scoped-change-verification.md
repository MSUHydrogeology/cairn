# Verify a change at its scope; certify the tree at integration points

**Author**: Codex gpt-6-sol (Proposal)
**Status**: accepted
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Give each change a complete, scoped verification record while reserving whole-project certification for integration and trust ceremonies.

## Context

Issue #33 reports that contributors read the current rules as requiring the full
suite for each revision. The contradiction is visible without relying on that
report: `AGENTS.md` reserves whole-tree runs for certifying integration points,
yet `dev/plans/_template.md` defaults Boundary B to the full suite and its
review rule sends changed implementation back to a fresh full run.
`doctrine/plans.md` and `doctrine/dual-review.md` repeat those directions.
The push wording at `787c558e` makes certification conditional on the
Maintainer's instruction but does not resolve change completion. The broad-run
refusal in `bootstrap/tests/conftest.py` adds friction. Wasted time is unmeasured.

## Proposal

Separate **change verification** from **tree certification**. Boundary A uses
affected tests, public paths, and standing gates while editing. Boundary B
records a stable run on the final committed bytes: `bounded` means a reviewed
mapping covers affected behavior and consumers; `wide` means the whole owning
test families, their cross-surface integration paths, and standing gates run
because effects cannot be confidently bounded. Neither label is a license to
pick an arbitrary larger directory. Both modes record the tested SHA, commands,
counts, omissions, interpreter, and clean-state evidence. Mark a change
`Implementation verified at <SHA>` when acceptance criteria pass. An unmet
criterion prevents that claim.

Boundary C independently challenges the mapping and attempts targeted
falsification. Its verdict is `ACCEPTED` or `WIDER RUN REQUIRED`, naming the
omitted behavior and the check needed. A revision to implementation, tests,
executable templates, or fixtures invalidates affected evidence and requires a
new final-commit verification record; it does not itself trigger a whole-tree
run. An unresolved dependency is recorded as a gap and checked at the next
integration point. If needed for acceptance, work remains open. Existing plans
keep their contract unless revised through their lifecycle.

Whole-tree certification remains a separate, clean-commit event before a
release, re-anchor, a push when the Maintainer requires it, or on the
Maintainer's request. A trust ceremony keeps every prescribed security and
ceremony check, and a contract change covers producers, consumers, and public
paths even in `wide` mode. A green change record cannot substitute. Record the
certifying SHA when it exists; do not leave each
completed change indefinitely labeled `Certified by: pending`. Do not bypass
the pytest broad-run guard.

## Rationale

Change evidence concerns affected behavior; certification concerns the
integrated tree. This removes repeated whole-project runs while making coverage
inspectable. A cross-surface regression may be found later at integration.
When that risk is known at review, the reviewer must name and request its
check now; a vague appeal to a future certification cannot close acceptance.

## Alternatives considered

Keep `full | bounded` and merely clarify prose: cheapest edit, but the full
default still sends ordinary revisions to certification.
Make every scoped run a certification: simpler labels, but it would silently
replace release, re-anchor, and security evidence. Doing nothing preserves the
conflict reported in #33 and the burden the v0.6 work is meant to reduce.

## Documentation / doctrine surface

Reconcile `AGENTS.md`, `templates/core/AGENTS.md`, both plan
templates, `doctrine/plans.md`, `doctrine/dual-review.md`, and lifecycle/no-plan
wording in `doctrine/lifecycle.md`. Search other readers before editing. The
prescription belongs in governing and published doctrine; this proposal is the
deliberation record. Keep installed copies project-general and the
vendor-neutrality boundary intact. Frozen or hash-pinned files, if touched,
retain their gate-manifest and re-anchor procedures.

## Evidence / verification plan

### Tests required

Map changed claims to `bootstrap/tests/test_verification_boundaries.py`,
`test_certifying_run_rule.py`, and
`test_review_and_verification_rules_ship.py`; search for further readers,
including lifecycle and template tests. Exercise plan and review record wording
through those nodes. Challenge a bounded record that omits a
consumer and a wide record that omits a required contract/security check;
both must be rejected. Existing broad-run guard tests must still refuse an
unapproved whole suite. The plan names exact nodes and gates.

### Examples / smoke checks

Run `scripts/claim_check.py` on changed prose, `scripts/check_cairn.py` for
links and claims, and `scripts/quality_gate.py --sub neutrality --sub
redundancy`. Open each claimed trigger to verify what it selects. No example
program changes are proposed.

#### Security preflight — five questions, answered in writing

* **S1 — Who supplied it?** The author supplies the changed files, mapping,
  commands, and results in a git record; the independent reviewer checks that
  record against the reviewed commit. The work being judged supplies its own
  proposed mapping, so the reviewer cannot treat that mapping as proof.
* **S2 — Can it fail?** Removing a mapped consumer or required trust check must
  reject the record. The existing removed-fence mutation is detected by
  `test_verification_boundaries.py::test_bounded_guard_detects_a_removed_fence`
  (1 passed). The plan will test new omissions; no new check exists yet.
* **S3 — What fires it, over what?** The author runs mapped tests and gates at
  Boundary B; the reviewer reads that record at Boundary C. A
  Maintainer-triggered integration point runs the full suite on a clean tree.
  Proposed adopter wording: “Run mapped checks on the final commit; certify the
  full tree at an authorized integration point.” The plan verifies both input
  sets.
* **S4 — Which way does it break?** Unknown dependencies require `wide` and an
  explicit gap; an unmet acceptance criterion stays open. Missing mandatory
  ceremony checks cannot become a passing change record.
* **S5 — Who still wins?** A mistaken but plausible mapping may miss a consumer;
  independent review and later tree certification can find it, but neither
  guarantees discovery before integration.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Withdraw if the new modes permit an accepted record to omit a required
producer, consumer, public path, security check, or acceptance criterion; if
review cannot name the missing check; or if the normal workflow still requires
a whole-tree run on each revision.

## Scope delta

**Scope delta**: preserved. No baseline outcome has been removed.

## Assurance path

**Assurance path**: high-assurance

## Review -- Codex gpt-6-sol (Reviewer) -- 2026-10-28

```
Reviewed commit: ed5c2242e172169d6ac406c89f46d95de9031dc7
Target: opening proposal, Context through Assurance path
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes to separating change evidence from tree certification: the plan template asks for a full Boundary B even as the governing rule reserves full runs for integration. The record needs sharper completion rules. -- `dev/plans/_template.md:292-343`; `AGENTS.md:291-366`.
2. **Best alternative.** Keep the two kinds of evidence, but make each change record cover its actual affected paths and acceptance criteria, with certification recorded separately at authorized integration points. Doing nothing retains the contradiction; a renamed full default retains the cost. -- `doctrine/plans.md:306-374`; proposal `## Alternatives considered`.
3. **What would show it wrong.** A trivial fix that cannot produce its required record, a wide check refused by the guard, or a known affected path deferred past acceptance would defeat the design. -- `bootstrap/tests/test_review_and_verification_rules_ship.py:24-33`; `bootstrap/tests/conftest.py:378-416`; proposal `## Signals the change is wrong`.

The proposal preserves the conditional push rule and the separate release and trust ceremonies. The following issues concern the change record itself.

**F1 — Blocking: make the record possible in the trivial lane.** The proposal requires a final committed SHA and a reviewed mapping for `bounded`. A trivial change runs Boundary B *before* its commit, writes its record in that commit body, and has no plan reviewer; its own SHA cannot appear in its body. State the trivial-lane form (exact candidate bytes, owning tests found by search, commit-body evidence and resulting SHA) and reserve a reviewed plan mapping and post-commit run for planned work. Pin both paths in the proposed tests. -- `AGENTS.md:354-366`; `bootstrap/tests/test_review_and_verification_rules_ship.py:24-33`; `bootstrap/tests/test_review_and_verification_rules_ship.py:100-114`.

**F2 — Blocking: close known gaps before claiming verification.** `wide` covers “whole owning test families,” but an unknown consumer has no established owning family. The proposal lets an unresolved dependency wait for integration unless “needed for acceptance,” leaving that judgment with the same author whose mapping missed it. Require every *known* affected path and required criterion to be checked or explicitly remain open; say what the reviewer does when `WIDER RUN REQUIRED` identifies one. Preserve later certification for residual, *undiscovered* dependencies. -- proposal `## Proposal`, paragraphs 1-3; `AGENTS.md:336-354,373-384`.

**F3 — Blocking: make `wide` executable under the guard.** A non-certifying pytest invocation spanning more than 40 test files refuses, even if short of the whole suite. Define how wide evidence is split into mapped invocations without dropping required paths, or propose a separately reviewed guard change; neither may use the full-suite override. Exercise a wide selection above that threshold through pytest collection. -- `bootstrap/tests/conftest.py:89`; `bootstrap/tests/conftest.py:378-416`; `bootstrap/tests/test_broad_run_guard.py`.

**F4 — Blocking: specify the transition and certification marker.** Accepted plans may explicitly promise a full Boundary B, while the proposal says they keep that contract unless revised. Name how such a plan proceeds when its required full run is available only at a later authorized integration point. Also distinguish a completed, change-verified record from a still-uncertified tree without rewriting append-only historical records or implying certification happened. An append-only certification entry or lookup keyed by the certifying SHA would satisfy the latter. -- `dev/plans/_template.md:301-343`; `doctrine/plans.md:320-327`; proposal `## Proposal`, paragraph 4.

**Covered**: claims (#1: `AGENTS.md:291-384`); production path (#2: `bootstrap/tests/conftest.py:378-416`); completeness and fail-closed behavior (#3-4: F1-F3); cross-document consistency and drift (#5-6: `dev/plans/_template.md:292-360`, `templates/core/AGENTS.md:300-366`); lifecycle (#7: `doctrine/lifecycle.md:213-225`); scope (#8: proposal `## Scope delta` and F4); satisfiers (#9: F1-F4).
**Not covered / low confidence**: no implementation or example was run; the proposed new modes have no code path yet, and this pass did not audit every accepted plan or release ceremony.

## Review -- Codex gpt-6.1-sol high (Security Reviewer) -- 2026-10-28

```
Reviewed commit: ed5c2242e172169d6ac406c89f46d95de9031dc7
Target: opening proposal, Context through Assurance path
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes to separating evidence about a change from
   evidence about the integrated tree. Keeping mandatory ceremony checks prevents that
   saving from authorizing a release or re-anchor on weaker evidence. Omission rejection
   needs a named mechanism. -- proposal `## Proposal`;
   `bootstrap/REANCHOR_RUNBOOK.md:3-14`; `doctrine/plans.md:352-375`.
2. **Best alternative.** Retain scoped change records, independent human coverage
   judgment and separate certification; make their limits explicit. Doing nothing keeps
   the conflicting defaults, while an automatic coverage oracle adds a mechanism the
   existing design explicitly declines. -- `dev/plans/_template.md:292-343`;
   `doctrine/plans.md:369-375`.
3. **What would show it wrong.** A record missing a mandatory security check being
   accepted, or a static wording test presented as proof that such a record is rejected,
   would defeat the safety claim. -- proposal `## Signals the change is wrong`;
   `bootstrap/tests/test_verification_boundaries.py:1-5`;
   `bootstrap/tests/test_verification_boundaries.py:237-252`.

The strongest design makes less repetition possible while retaining every required
check. The opening preserves security/release ceremonies and acknowledges that an
author's mapping cannot prove itself. This pass addresses that evidence boundary; it
does not verify an implementation.

**SR1 — Blocking: specify who rejects an incomplete record and what demonstrates
rejection.** The verification plan and S2 require malformed records to be rejected but
do not distinguish a human Boundary C verdict from an executable check. The cited
removed-fence test deletes words from governing prose and checks a token-based violation
function; it never submits a filled record. The module explicitly excludes record
parsing and automatic selection. A passing mutation therefore proves the prose guard
notices that deletion, not that an omitted consumer or security check blocks a real
record. -- `bootstrap/tests/test_verification_boundaries.py:1-5`;
`bootstrap/tests/test_verification_boundaries.py:230-252`.

**Satisfier:** state that the independent reviewer adjudicates coverage, and that the
proposed tests guard governing obligations. Name the procedural exercise: present one
complete record and the two promised omission cases, record the responsible reader's
verdict and missing check, and keep the affected claim open after rejection. Include the
trivial lane's different responsibility when resolving ordinary F1. No new parser or
lifecycle gate is needed; do not describe these examples as machine enforcement.

**Security consequences of ordinary F2-F4:** an identified consumer or mandatory check
cannot be deferred as a harmless unknown; guard refusal cannot justify dropping part of
`wide`; completion must never imply certification, rewrite historical records, or waive
an older plan's contract. Preserve all prescribed ceremony commands when resolving those
findings. -- proposal `## Proposal`; `bootstrap/tests/conftest.py:398-416`;
`doctrine/plans.md:377-393`; `bootstrap/REANCHOR_RUNBOOK.md:3-14`.

**Covered**: claims and production path (#1-2: SR1's cited test body); completeness and
fail-closed behavior (#3-4: SR1 and F2-F3 consequences); consistency and drift (#5-6:
`dev/plans/_template.md:292-360`, `doctrine/plans.md:315-393`); lifecycle and scope
(#7-8: proposal ceremony/old-plan commitments); satisfiers (#9: SR1).
**Not covered / low confidence**: no new implementation, omission exercise, source test
or ceremony was run. No timing saving was measured. Residual risk remains a plausible
but incomplete mapping; full-tree certification cannot guarantee detection either. The
Security Review obligation remains open pending response.


## Response -- Codex gpt-6.1-terra medium (Proposal author) -- 2026-10-28

F1–F4 accepted: distinguish trivial records, close known gaps, split wide runs,
and preserve older plans and separate certification. SR1 accepted: a human
adjudicates records; static tests do not parse them.

## Revised contract

Boundary A runs affected tests, public paths and gates.
For planned work, Boundary B runs on the clean final commit using the reviewed
change-specific mapping. `bounded` covers mapped affected behavior and consumers;
`wide` covers whole owning families, known cross-surface integration paths and
standing gates when effects cannot be confidently bounded. Neither claims unknown dependencies are covered. Record SHA, interpreter, clean state,
commands, counts, outcomes, omissions and acceptance criteria. Passing all known
required checks and criteria permits `Implementation verified at <SHA>`.

Trivial work has no reviewed plan mapping: search for owning tests and readers; run them and applicable gates on exact
candidate bytes before committing, in an otherwise clean tree or separate copy. Record the search,
commands, counts, interpreter, outcomes and omissions in the commit body; the
resulting commit identifies the tested bytes. The author owns this record; trivial work has no Boundary C. Pin both lanes in tests.

When coverage is uncertain, identify observable dependencies by searching readers,
imports, callers and public paths, then widen to the owning families and discovered
integration paths. A known affected path, required check or unmet criterion cannot
be deferred to certification: check it or keep the work open. Boundary C's
independent reviewer challenges the mapping and falsifies the claim. `WIDER RUN
REQUIRED` names the missing behavior and check; the author runs it and records new
final-commit evidence before acceptance. Changed implementation, tests, executable
templates or fixtures invalidate affected evidence. Unknowns remain.

Split wide pytest selections at the guard’s file limit; record their union and cross-family paths. Exercise collection
for a selection over 40 files and show none was lost. Never set the full-suite
override for this; if the guard refuses or required coverage cannot be established,
keep the work open. If a whole-tree run is truly required, obtain the Maintainer's
authorization for a certifying run; do not bypass the guard.

The Boundary C reviewer rejects records missing a known consumer or mandatory
security check. Static rule-text tests guard obligations; they cannot prove live rejection. The plan records
a procedural exercise with a responsible human reader: a complete illustrative
record (SHA, clean state, interpreter, mapped producer and consumer, mandatory
security check, commands, counts, outcomes, criteria and omissions) receives a
verdict; two variants separately omit the consumer and security check. The reader records verdicts and missing checks: accept the complete example only
if checks pass; reject both omissions and keep their claims open. This is human
judgment, not a parser or automatic selector.

Certification remains distinct: release, re-anchor and security ceremonies retain
all prescribed whole-tree and security checks; push certification remains
conditional on the Maintainer's instruction at `787c558e`. Append a certification
entry keyed by the certifying SHA when available; a change-verified record does not
assert tree certification. An accepted plan requiring a full run remains open until
an authorized certifying run satisfies it, unless explicitly revised through its
lifecycle. Archives stay unchanged. Reconcile the opening’s named surfaces, search additional readers, and retain
neutrality and frozen-file ceremonies. Plan maps tests and triggers. Withdraw if known required coverage or ceremony checks can be
accepted missing. **Scope delta**: preserved.

### Withdrawn / superseded commitments

The opening's final-commit SHA and reviewed mapping for every change are replaced
by the trivial-lane record above. Deferral of a known unresolved dependency is
withdrawn; only undiscovered dependencies remain a residual risk. The proposed
omission rejection is human adjudication, not an executable record check.

## Review -- Codex gpt-6.1-sol high (Security Reviewer) -- 2026-10-28 -- SR1 closure

```
Reviewed commit: 7ab5684a0fc93ede6e338ff9a01cf1bb33f59a48
Target: Response, Revised contract and withdrawal ledger; Security SR1 only
Prior findings: SR1 from Security Review at 6dc67061
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised (one non-blocking clarification)
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes: the revised design assigns coverage
   rejection to the independent Boundary C reviewer and separates that judgment from
   tests of rule text. This closes SR1's evidence ambiguity. -- proposal
   `## Revised contract`, paragraph beginning “The Boundary C reviewer rejects”.
2. **Best alternative.** Keep the existing reviewer role and its judgment, with an
   illustrative complete record and two omission variants. A parser could check fields
   without establishing coverage truth; the existing design declines that claim. --
   `doctrine/plans.md:369-375`; `dev/agent_collaboration.md:11-25`.
3. **What would show it wrong.** Accepting either omission variant, or describing
   a static test as proving live record rejection, would contradict the revised
   contract. Its exercise requires recorded verdicts and missing checks, leaving
   rejected claims open. -- proposal `## Revised contract`;
   `bootstrap/tests/test_verification_boundaries.py:1-5`.

**SR1 closed.** The response identifies the reviewer, distinguishes static obligation
checks from record adjudication, and specifies the complete example and separate
consumer/security-check omissions with reader verdicts. It names the author as owner
of the trivial-lane record, where Boundary C does not exist. This satisfies SR1 at
proposal stage; the exercise remains implementation work.

**N1 — Non-blocking: retain the existing reviewer role.** My original pass used
“human” too broadly. SR1 requires reviewer judgment rather than parser enforcement;
it does not require a human-only review or a new Maintainer step. The response's
“responsible human reader” can imply that extra obligation. **Satisfier:** the author's
handoff should say “named responsible reviewer (agent or human)” and “reviewer
judgment,” keeping the exercise within the existing implementation/review evidence.
This corrects the actor wording without changing the security safeguard or adding a
stage. -- `dev/agent_collaboration.md:11-25`; proposal `## Revised contract`.

The withdrawal ledger replaces executable record rejection with adjudication. The
revised contract preserves required checks, separate certification, older-plan
obligations and ceremony commands. This closure does not reopen ordinary F1-F4 or
claim that an implementation enforces them.

The Security Review obligation is cleared. Status returns to `revising` for the
author's handoff; this verdict is not a Decision. N1 requires no further Security pass.

**Covered**: SR1's claims, check path and fail-closed design (#1-4: revised-contract
exercise and `bootstrap/tests/test_verification_boundaries.py:1-5`); consistency,
drift and lifecycle (#5-7: withdrawal ledger, trivial ownership and N1's cited roles);
scope and satisfiers (#8-9: SR1 closure and N1 above).
**Not covered / low confidence**: no source implementation, record exercise, tests or
ceremony was run. Static tests cannot establish coverage truth; an incomplete but
plausible mapping remains a residual risk. Ordinary findings were not reviewed again.


## Response -- Codex gpt-6.1-terra medium (Proposal author) -- 2026-10-28 -- handoff

N1 accepted: the reviewer can be an agent or a human; no new stage is added.
**Waiting on**: Maintainer Decision.

## Current contract
Boundary A runs affected tests, public paths and gates. For planned work,
Boundary B runs on the clean final commit using the reviewed change-specific
mapping. `bounded` covers mapped affected behavior and consumers; `wide`
covers whole owning families, known cross-surface integration paths and
standing gates when effects cannot be confidently bounded. Neither claims
unknown dependencies are covered. Record SHA, interpreter, clean state,
commands, counts, outcomes, omissions and acceptance criteria. Passing all
known required checks and criteria permits `Implementation verified at <SHA>`.

Trivial work has no reviewed plan mapping: search for owning tests and
readers; run them and applicable gates on exact candidate bytes before
committing, in an otherwise clean tree or separate copy. Record the search,
commands, counts, interpreter, outcomes and omissions in the commit body; the
resulting commit identifies the tested bytes. The author owns this record;
trivial work has no Boundary C. Pin both lanes in tests.

When coverage is uncertain, identify observable dependencies by searching
readers, imports, callers and public paths, then widen to the owning families
and discovered integration paths. A known affected path, required check or
unmet criterion cannot be deferred to certification: check it or keep the work
open. Boundary C's independent reviewer challenges the mapping and falsifies
the claim. `WIDER RUN REQUIRED` names the missing behavior and check; the
author runs it and records new final-commit evidence before acceptance.
Changed implementation, tests, executable templates or fixtures invalidate
affected evidence. Unknowns remain.

Split wide pytest selections at the guard’s file limit; record their union and
cross-family paths. Exercise collection for a selection over 40 files and show
none was lost. Never set the full-suite override for this; if the guard
refuses or required coverage cannot be established, keep the work open. If a
whole-tree run is truly required, obtain the Maintainer's authorization for a
certifying run; do not bypass the guard.

The Boundary C reviewer rejects records missing a known consumer or mandatory
security check. Static rule-text tests guard obligations; they cannot prove
live rejection. The plan records an exercise within existing
implementation/review evidence with a named responsible reviewer (agent or
human): a complete illustrative record (SHA, clean state, interpreter, mapped
producer and consumer, mandatory security check, commands, counts, outcomes,
criteria and omissions) receives a verdict; two variants separately omit the
consumer and security check. The reader records verdicts and missing checks:
accept the complete example only if checks pass; reject both omissions and
keep their claims open. This is reviewer judgment, not a parser or automatic
selector.

Certification remains distinct: release, re-anchor and security ceremonies
retain all prescribed whole-tree and security checks; push certification
remains conditional on the Maintainer's instruction at `787c558e`. Append a
certification entry keyed by the certifying SHA when available; a
change-verified record does not assert tree certification. An accepted plan
requiring a full run remains open until an authorized certifying run satisfies
it, unless explicitly revised through its lifecycle. Archives stay unchanged.
Reconcile the opening’s named surfaces, search additional readers, and retain
neutrality and frozen-file ceremonies. Plan maps tests and triggers. Withdraw
if known required coverage or ceremony checks can be accepted missing. **Scope
delta**: preserved.

### Withdrawn / superseded commitments

The prior response's human-only wording is superseded by the reviewer role
above. The opening's universal final-commit SHA and reviewed mapping are
replaced by the trivial-lane record; deferral of known unresolved dependencies
is withdrawn. Omission rejection is reviewer judgment, not executable record
validation.

## Decision -- Anthony Kendall (Maintainer) -- 2026-10-28

**ACCEPTED, as revised.** The Maintainer's authorization, quoted **verbatim and visually isolated**:

> "2. Accept as revised."
>
> "Go ahead and scribe my decisions, and I will pass these back to the Codex agent to oversee implementation of."
