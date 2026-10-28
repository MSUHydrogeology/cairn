# Verify a change at its scope; certify the tree at integration points

**Author**: Codex gpt-6-sol (Proposal)
**Status**: awaiting-review
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
