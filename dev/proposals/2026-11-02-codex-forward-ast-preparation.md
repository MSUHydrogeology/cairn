# Prepare the AST record for a new forward baseline

**Author**: Codex (Sol), Strategy
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Let agents prepare and review the current code record so the Maintainer can establish a new baseline with simple scripted approval and signing.

## Decision summary

Add an explicit forward-only preparation operation to the maintained baseline
script. It prepares a proposed correction to the code fingerprint records from
one committed candidate, for independent review and a scripted Maintainer apply
and commit. It never compares a historical trust anchor or signs anything.

This establishes current trust; it does not certify prior AST history. The Maintainer would accept that limited
loss explicitly. Security checks, functional checks, independent review and signing remain required.

## Context

The existing forward path refuses candidates with outstanding AST or lockfile
preparation (`scripts/repin.py`, `baseline_reader_inputs`). Its correction commands require historical-anchor setup, contrary to the
Maintainer’s requested forward-only path.

Measurement of committed `f8379e9` with Python 3.13.13, using
`ast_view` and `lockfile_correction` from committed `scripts/repin.py`, found
18 changed baseline symbols, four changed known-new symbols and 12 additions;
no missing, duplicate or dropped symbols and no lockfile correction. `bootstrap/AST_BASELINE_RUNBOOK.md` reserves the required nonallowlisted
correction to the Maintainer.

## Proposal

Extend the explicit forward-baseline path in `scripts/repin.py` to prepare an
AST transaction from the exact committed candidate without loading or
comparing a prior anchor. Reuse the existing AST classification, transaction,
hash binding and exact-path application machinery; add no trust store or
ledger. Preserve the baseline symbol set. Missing or duplicated baseline
symbols refuse; handling deletion is outside this change.

Preparation writes only to a new external evidence directory. Its packet names
the candidate, canonical interpreter, tool hashes, existing fixture hashes,
changed symbol bodies and locations, proposed digest replacements, known-new
delta and the explicit absence of historical certification. No baseline file
is rewritten during preparation. Any lockfile correction is reported and
refused for separate treatment; current measured debt requires none.

A fresh ordinary reviewer and Security Reviewer inspect current affected engine
behavior, record changes, protection machinery and automated check evidence.
They do not reconstruct prior review lineage. The prepared record must bind
both reviews and the exact transaction before application is offered.

A maintained command then asks the Maintainer to approve that concrete packet,
checks unchanged inputs and applies only its recorded fixture changes. A
separate exact-path commit confirmation follows the existing command pattern.
Agents prepare evidence and reviews. The only Maintainer steps are approving
the reviewed correction, confirming its exact-path commit, and the existing
final baseline approval/signing. A documented maintained script guides these
steps; no manual JSON edits or undocumented command sequence is acceptable.
Reuse the existing forward process rather than adding another review ceremony. Fresh baseline reader inputs and baseline installation follow on
the resulting commit under their existing requirements. This proposal alone authorizes no correction or installation.

## Rationale

Reuse keeps ordinary historical ceremonies unchanged. Current-state review and automated checks
provide useful assurance without asking the Maintainer to analyze code or
reconstruct history. They cannot prove that every historical change was
previously reviewed.

## Alternatives considered

* Do nothing: no new maintenance cost, but the release remains blocked.
* Use the ordinary historical correction: reuse all existing commands and keep
  historical accounting, but requires the reconstruction the Maintainer has
  rejected and additional analysis.
* Manually rewrite the fixtures: less implementation work, but transfers
  technical comparison and exact-input checking to the Maintainer and loses
  the reusable safeguards.

Recommendation: the explicit scripted operation; its continuing cost is one
maintained command path and focused tests, without another authority system.

## Documentation / doctrine surface

Update `bootstrap/AST_BASELINE_RUNBOOK.md` and
`bootstrap/REANCHOR_RUNBOOK.md` to describe the separate forward correction and
its assurance limits. Governing permission belongs in `AGENTS.md` if its
Maintainer-only correction rule needs clarification; deliberation stays here.
Ordinary correction and release certification rules remain unchanged.

## Evidence / verification plan

### Tests required

Extend `bootstrap/tests/test_repin.py` and
`bootstrap/tests/test_repin_ceremony.py` through the real commands: preparation
with no prior anchor, unchanged ordinary-path refusal, candidate and transaction
mutation refusal, missing/duplicate refusal, lockfile-debt refusal, unreviewed
packet refusal, no repository writes during preparation, and apply/commit
limited to reviewed paths. Use `bootstrap/tests/test_ast_attest.py` to verify
unchanged baseline membership and resulting accounted-for digests.

The plan must map affected consumers with `tools/test_tiers.py`; final Boundary
B is wide because this touches a trust ceremony. Required independent Security
Review and release certification remain separate obligations.

### Examples / smoke checks

Run claim, link, snippet and neutrality gates for changed prose. Exercise the
complete preparation, independent-review binding and Maintainer correction
workflow in disposable repositories; never sign or move real refs in tests.

#### Security preflight — five questions, answered in writing

S1: Candidate bytes supply code and proposed fingerprints; they do not supply
review approval. Separate reviewer records and Maintainer confirmation authorize
application, all bound to exact hashes.

S2: Hash equality proves identity, not safety. Planned negative controls alter
the candidate, packet, review binding and target fixtures separately; each must
refuse. These implementation controls have not yet been run.

S3: The explicit forward operation selects one commit and its complete engine
module set. Runbook wording will say it prepares current-state fingerprints
without certifying prior history; ordinary commands never infer this mode.

S4: Missing inputs, invalid records, unknown deltas, changed inputs or missing
reviews refuse without writing. No fallback grants historical authority or
selects the forward path automatically.

S5: An attacker may control candidate code and fixtures. Independent review and
checks can still miss a malicious but plausible implementation; signatures
attest the chosen candidate, not its correctness. Compromised host/reviewer
credentials remain outside this change's protection.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The Maintainer must interpret code deltas manually; preparation consults a
historical anchor; ordinary correction becomes less strict; a mutated packet
can write; or the resulting record implies historical review completeness.

## Scope delta

None; opening scope. No historical certification is promised.

## Assurance path

**Assurance path**: high-assurance

**Authoring elapsed**: approximately 12 minutes, including diagnosis.
**Tokens**: unknown.

## Proposal review -- Codex (GPT-6), Reviewer -- 2026-11-02

**Verdict: proceed as framed.** The forward record makes a current-state claim and explicitly gives up historical certification; the Maintainer must accept that loss in the Decision. The proposed tests cover the main functional refusal and write boundaries. This is a recommendation, not a Decision.

**Foundations.** (1) Should it happen? Yes: `baseline_reader_inputs` refuses an owed transaction, and `build_transaction` already constructs the record and checks membership (`scripts/repin.py`, lines 422–429 and 978–1018 at `0c4d925e`). The proposal supplies the missing forward path while keeping independent review and signing. (2) Best alternative: extend the existing transaction and apply commands with an explicit forward mode, reusing their existing record format where feasible. The proposal permits that; it avoids a second authority system. Doing nothing costs less but leaves the measured 18 changed baseline symbols, four changed known-new symbols and 12 additions unresolved and the forward path blocked. (3) What would show this wrong? A disposable-repository run that needs an old anchor, writes before approval, accepts a changed packet or unreviewed record, or fails to produce a usable next baseline would falsify the approach. The proposed negative controls and end-to-end exercise address these cases.

**Advice:** In the plan, prefer existing record and command mechanisms when they satisfy both independent reviews; identify any new fields and checks needed so the Maintainer sees only the promised approvals. This is nonblocking design advice, not a request for another ceremony.

**Coverage:** Read the committed proposal and the named transaction, forward-reader, and apply/commit entry points. Did not execute checks, validate the author's measured counts independently, or assess the complete hostile-input and signing threat model; the separate Security Review covers that boundary. Elapsed: approximately 3 minutes. Tokens: unknown.
