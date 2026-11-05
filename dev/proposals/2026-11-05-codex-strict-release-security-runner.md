# Repair the strict release-security runner for v0.7

**Author**: Codex gpt-6-sol (Strategy, High)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Make the release security check finish on Mac and Windows without missing tests or running the whole suite twice.

## Decision summary

Repair the strict runner before v0.7. Run its full applicable suite once per
native platform and join Mac and Windows evidence for one commit before calling
release security passed. This costs two host runs and a reviewed rule for
platform-only tests. A local pass alone is not a release pass.

## Context

`dev/PLANNING.md` item 7a requires a corrected strict run on the final v0.7
candidate. The v0.6.1-only exception explicitly left this runner unpassed
(`dev/plans/archive/2026-11-03-baseline-checker-alignment.md`, Maintainer
dispositions). `bootstrap/security_check.py::run_suite` runs all
`bootstrap/tests` without an explicit shuffle seed. Its `run_quality_gate`
then invokes all sub-gates; `scripts/quality_gate.py` defaults to seed 0 and
starts another whole-suite pytest process. Both child processes inherit release
mode, where `bootstrap/tests/conftest.py` refuses actual skips, xfails and
xpasses. The tree has native-Windows junction and POSIX-only cases, so neither
host can pass every case. Earlier focused runs are not a strict runner pass at
the final v0.7 SHA. No full-suite reproduction ran for this proposal.

## Proposal

1. Preserve the clean committed candidate, detached exact-byte checkout,
   pre/post verification, Bandit over the derived shipped surface and live
   allowlist, and `check_cairn.py`. Preserve refusal on tool absence, scanner
   errors, malformed reports, changed bytes, test failures and incomplete
   outcomes. Do not alter trust records, configured suite members or security
   test assertions.
2. In `bootstrap/security_check.py`, run the release-mode suite with explicit
   `--quality-gate-shuffle-seed=0` and call `quality_gate.py` for **both**
   neutrality and redundancy only. The order-independence sub-gate remains
   available through its own public command; its seed-0 whole-suite behavior
   is fulfilled by the direct release suite, not silently deleted.
3. Define a narrow, reviewed platform-only outcome rule at the existing
   `bootstrap/tests/conftest.py` release boundary. Name the exact nodes or
   conditions eligible on each host from collection; all other
   skips, collection-time skips, xfails and xpasses still refuse. A member
   excused on one host must pass on its native host at the **same candidate
   SHA**. Each host's output names its platform, SHA, eligible non-runs and
   failures; neither local success is labelled complete release security.
   The existing release record may call the joined result passed only with
   both matching, passing outputs. Add no parallel evidence store or general
   skip switch.
4. Investigate Windows committed-path comparison: Git tree keys use `/`,
   whereas `_checkout_leaf_paths` currently stringifies native relative
   paths. Normalize only that representation if a nested-path Windows probe
   confirms the mismatch. Investigate whether the unconditional POSIX
   executable-bit comparison works on Windows; preserve meaningful mode
   detection or name an unresolved barrier. Neither is claimed as a proven
   fix by this proposal.

Coordinate node identities and fixtures with suite-consolidation 2a **before**
editing control flow. Its unfinished C1-C4, growth report and archive are not
prerequisites for #7a plan archive. The final strict run belongs to the
separate release point on the final candidate; no agent plan waits on human
signing, baseline installation or publication.

## Rationale

Local tests cannot hide unexpected non-runs; release cannot claim native
coverage without both hosts. Named quality sub-gates remove a duplicate suite
launch without changing `AGENTS.md`'s certifying pair or substituting ordinary
certification for strict security evidence.

## Alternatives considered

* **Do nothing:** no build or upkeep cost, but the v0.6.1 exception cannot
  renew and #7a stays unpassed; repeated full runs and platform skips remain.
* **Fixture-only/platform emulation:** simpler runner, but cannot prove native
  junction or POSIX behavior; it loses the native safeguard.
* **Keep both suite launches and join platform logs manually:** smaller
  control-flow edit, but costs another full run on each host and leaves the
  duplicate invocation. It can meet coverage only if the same-SHA join is
  still explicit.

**Recommendation:** the narrow two-host evidence rule and one suite launch.
The classification and release-record work buys native coverage without
another runner or database; review must challenge the roster and Windows path.

## Documentation / doctrine surface

Describe the behavior in `SECURITY.md` (one-command claim and phases),
`docs/release-process.md` (checks) and `bootstrap/PROVENANCE.md` (ordering).
Keep `AGENTS.md`'s certification commands and triggers unchanged; deliberation
stays in `dev/`. Update only affected source comments. No board or changelog
edit is proposed here.

## Evidence / verification plan

### Tests required

Use `tools/test_tiers.py for` on changed paths. Owning tests:
`bootstrap/tests/test_security_check.py` (phases, bytes, tools, platform
output), `test_broad_run_guard.py` (incomplete outcomes), and
`test_quality_gate_cli.py` / `test_quality_gate_order_independence.py`
(sub-gates, seed); resolve moved paths after 2a. Add native Windows path/mode
probes where absent. Unknown or falsely eligible skips, collection skips,
missing/wrong-SHA/failed native evidence and removed suite members must not
produce complete release success. Mutate each eligible native case in separate
copies to test its reach. Ordinary and Security code reviews precede wide
Boundary B on a clean Python 3.13.x commit.

### Examples / smoke checks

Through the real `security_check.py` entry point on committed fixtures, show
one suite process per host, seed 0, both quality sub-gates, Bandit,
`check_cairn` and byte-integrity refusal. Run prose claim/link/snippet and
neutrality gates for changed docs. At the authorized release point, require
native Mac and Windows outputs at one SHA and their joined record. The
certifying pair remains separately required; no full suite runs during this
proposal or routine iteration.

#### Security preflight

* **S1 — Who supplied it?** The checked commit comes from the local Git
  checkout; suite membership, skip conditions, checker and test code come
  from that commit. Host OS, interpreter and subprocess outcomes come from
  each machine, and the Maintainer joins the two recorded outputs. Candidate
  code partly judges itself, as today.
* **S2 — Can it fail?** Mutation controls must make a non-platform skip,
  wrong SHA, omitted native node, stale allowlist, removed phase or changed
  checkout byte fail. None ran in this proposal-only turn.
* **S3 — What fires it, over what?** `python bootstrap/security_check.py`
  selects committed bytes, derived Bandit targets, all `bootstrap/tests` with
  seed 0, and both named quality sub-gates. The
  adopter-facing `SECURITY.md` says: "One command, and its output belongs in
  the release notes." The revised text must explain why two native outputs
  and their join are needed for a complete record.
* **S4 — Which way does it break?** Unknown platform, malformed or missing
  counterpart evidence, unclassified skip, failed subprocess or path/mode
  mismatch must prevent a release pass. Normalization cannot drop a leaf.
* **S5 — Who still wins?** A party able to change candidate checker and tests
  before review can weaken both; independent review and Maintainer judgment
  remain necessary. Exact-byte matching cannot detect malicious committed logic.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

One host reports complete release success without its counterpart; a
non-platform skip passes; a native case is absent from the collected suite;
seed 0 or a quality sub-gate is missing; Windows cannot verify committed
paths or modes; or the final two outputs refer to different SHAs. Any such
result keeps #7a open rather than becoming another release exception.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance.

## Review -- Codex Terra (Medium) -- 2026-11-05

Reviewed commit: bcafe539d40839f2ef1d72b86888be60f4ba737b

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Repair is needed, but the proposed equivalence and evidence join need a firmer contract before Decision -- PLANNING 7a; findings below.
2. **Best alternative.** Keep both orderings and explicitly reconcile native evidence; it costs two suite runs per host but preserves the existing default-order observation -- `security_check.py::run_suite`; `quality_gate.py::_run_order_independence`.
3. **What would show it wrong?** A default-order-only failure, or a missing, skipped, duplicated or wrong-SHA native node accepted by the join, would disprove preservation -- `conftest.py` shuffle and outcome hooks; proposal, Tests required.

**Blocking 1: Two orderings become one.** The direct suite currently uses default collection order; the quality gate separately runs seed 0. Seeding the direct suite replaces, rather than duplicates, the former observation. Identify that loss and its cost for Maintainer disposition, or preserve it; demonstrate equivalence only if supported by evidence.

**Blocking 2: The join is underspecified.** Host output promises eligible non-runs and failures, not evidence that each counterpart node was collected and passed. Specify the evidence fields, collection/outcome reconciliation, responsible reader and refusal procedure for absent, duplicate, malformed, wrong-platform or wrong-SHA results. Demonstrate negative cases through the real join, including xfail/xpass and collection skips. The current release command reports one machine-checkable PASS (`SECURITY.md`); a human join adds recurring review effort and omission risk that the Decision must be able to weigh.

**Advice:** Coordinate roster identities with 2a C1/C2 fault mapping and C3 moves without making unfinished work a prerequisite. Windows path and mode changes remain probes, not established fixes; report native results and unresolved barriers. Compare the cost of maintaining the roster and two-host evidence against the existing release record and 2g comparator before adding machinery.

**Coverage:** Read committed runner, quality gate, outcome guard, owning test references, proposal template, 2a plan and release documentation. No native execution, mutation, full suite or Security Review; timing and token use unavailable.

## Review -- Codex Sol (Security Review) -- 2026-11-05

Reviewed commit: `bcafe539d40839f2ef1d72b86888be60f4ba737b`

**Model**: gpt-6.1-sol (high). **Tier**: Security Review.
**Findings**: two blocking. **Verdict**: REVISE.
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Repair the strict runner, yes; do not call one seeded run equivalent to today's default-order plus seeded runs, or a local result a two-host pass -- `security_check.py::run_suite`; `quality_gate.py::_run_order_independence`.
2. **Best alternative.** Keep both orderings during the full ceremony and focus this change on platform evidence. It costs the second suite run but preserves the existing observation -- `conftest.py::pytest_collection_modifyitems`.
3. **What would show it wrong?** Exclude one native-required node while other tests pass, then require the joined release result to fail; a passing join would invalidate the assurance claim -- Proposal, S2/S4.

**SR1 (blocking, overlaps ordinary finding 1):** No seed leaves collection in default order; seed 0 shuffles it. Replacing the first with seed 0 loses an independent order observation. Preserve both, or present this exact loss for the Maintainer's Decision; do not describe it as duplicate execution of the same check.

**SR2 (blocking, sharpens ordinary finding 2):** The platform-only roster cannot be learned from the observed collection: a missing node produces no skip to classify. Under Python 3.13.13, a two-case disposable pytest selection with one required case deselected exited 0 and emitted XML containing only the other case. Name an independently supplied expected native-node set and the reader that compares actual pass outcomes at the same SHA, including absent/duplicate/malformed reports. Specify whether the local runner exits incomplete and exactly what human or command turns two local records into a release pass. Otherwise S2/S4's omitted-member and missing-counterpart refusals have no enforceable owner.

**Coverage:** Committed proposal, runner, quality gate, shuffle hook and a two-case omission probe. **Not covered:** native Mac/Windows strict runs, final roster, Windows path/mode behavior, full suite, release or trust operation.
