# Verify a change at its scope; certify the tree at integration points

**Author**: Codex gpt-6-sol (Proposal)
**Status**: revising
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
