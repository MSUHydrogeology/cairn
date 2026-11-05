# Repair the strict release-security runner for v0.7

**Author**: Codex gpt-6-sol (Strategy, High)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Make the strict release security check account for every native Mac and Windows test at one commit without weakening its two test orderings.

## Decision summary

Repair the strict runner before v0.7. Keep its default-order suite and its
separate seed-0 quality-gate suite; they test different orders, not a duplicate
observation. A fixed, reviewed list of platform-only test nodes and a reader in
the existing runner must join native Mac and Windows outcomes at one commit.
Each local run is incomplete until that join passes. The cost is two full
suite runs on each host, a bounded node list, and a narrow evidence reader.

## Context

`dev/PLANNING.md` item 7a requires a corrected strict run on the final v0.7
candidate. The v0.6.1-only exception explicitly left this runner unpassed
(`dev/plans/archive/2026-11-03-baseline-checker-alignment.md`, Maintainer
dispositions). `bootstrap/security_check.py::run_suite` runs all
`bootstrap/tests` in default collection order. Its `run_quality_gate` invokes
the order-independence sub-gate, whose default seed 0 starts a second
whole-suite pytest process. Both child processes inherit release
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
2. Preserve both existing suite launches: direct default order and the
   quality gate's seed 0, plus its neutrality and redundancy sub-gates. Do
   not claim duplicate-run savings. Do not change the separate authorized
   certifying pair in `AGENTS.md`.
3. Put a bounded expected Mac-only and Windows-only **node-ID set** in
   `bootstrap/security_check.py`, fixed from independently reviewed test
   source and protected collection records, not generated from either host's
   observed collection. Coordinate exact identities with 2a before editing.
   The runner supplies this set to the existing release hook in
   `bootstrap/tests/conftest.py`. Only a skip of a named opposite-platform
   node may be locally eligible; unexpected skips, collection skips, xfails,
   xpasses and failures still refuse. Eligibility never removes a node from
   either full-suite selection.
4. For **each** suite order, the hook emits exact node-ID/outcome evidence to
   an external temporary report path supplied by the runner; no report file
   may enter the byte-verified checkout. `bootstrap/security_check.py` reads
   and validates both reports, comparing the fixed expected native IDs with
   actual collected and passed outcomes. A deselected or otherwise absent
   required native node therefore fails even when pytest exits 0. It emits a
   structured local record naming full SHA, host platform, Python 3.13,
   roster identity, phase results and each expected node's outcome in both
   orders. Local success prints **INCOMPLETE** and exits 5, never `PASS`.
5. An explicit join mode in the **same** `bootstrap/security_check.py` reads
   the two local records against its fixed roster and clean final `HEAD`.
   It rejects missing, duplicate, malformed, wrong-platform or wrong-SHA
   records; failed phases; a roster mismatch; and any expected native node
   without exactly one pass in **each** order on its native host. Only this
   reader emits the joined release-security `PASS`, with the full SHA. The
   Maintainer runs the join at the final release point and places its output
   and both host records in the existing release notes. These are release
   evidence attachments, not a second standing ledger; the runner does not
   authenticate a person who supplies a record, preserving the existing
   human-transcription residual.
6. Investigate Windows committed-path comparison: Git tree keys use `/`,
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

Local tests cannot hide unexpected non-runs; a native node absent from
collection is caught against an independent expectation; and no release pass
exists without both hosts. Keeping both suite orders preserves the evidence
the current command actually collects. The two-host join adds a small reader
and roster-upkeep cost but no recurring full-suite invocation beyond the
existing two per host.

## Alternatives considered

* **Do nothing:** no build or upkeep cost, but the v0.6.1 exception cannot
  renew and #7a stays unpassed; repeated full runs and platform skips remain.
* **Fixture-only/platform emulation:** simpler runner, but cannot prove native
  junction or POSIX behavior; it loses the native safeguard.
* **Replace default order with seed 0:** saves one whole-suite run per host,
  but loses default-order fault detection. This loss needs the Maintainer's
  explicit allowance; elapsed time alone does not establish equivalence.
* **Manual join in the existing release notes:** avoids a new parser but puts
  absent, duplicate and malformed node outcomes on a person to detect across
  two long logs. It cannot honestly support an automatic strict `PASS`.

**Recommendation:** keep both suite orders and use the bounded roster plus
the runner's join reader. Compared with manual joining, its extra format and
parser cost is justified by the observed silent omission case. Review must
challenge the roster's independent source and Windows path behavior.

## Documentation / doctrine surface

Describe the behavior in `SECURITY.md` (one-command claim and phases),
`docs/release-process.md` (checks) and `bootstrap/PROVENANCE.md` (ordering).
Replace the one-machine `PASS` claim with local `INCOMPLETE` and the exact
two-record join command, result and responsible Maintainer step.
Keep `AGENTS.md`'s certification commands and triggers unchanged; deliberation
stays in `dev/`. Update only affected source comments. No board or changelog
edit is proposed here.

## Evidence / verification plan

### Tests required

Use `tools/test_tiers.py for` on changed paths. Owning tests:
`bootstrap/tests/test_security_check.py` (phases, bytes, report reader and
join), `test_broad_run_guard.py` (incomplete outcomes and exact node IDs), and
`test_quality_gate_cli.py` / `test_quality_gate_order_independence.py`
(default order versus seed 0); resolve moved paths after 2a. Add native
Windows path/mode probes where absent. At the real join entry point, test
absent/deselected native node (including the reviewer's tiny positive control),
duplicate outcome, bad JSON/schema, collection skip, wrong platform/SHA,
roster drift, failed phase, xfail/xpass and unexpected skip. Mutate each
eligible native case in separate copies to test its reach. Ordinary and
Security code reviews precede wide Boundary B on a clean Python 3.13.x commit.

### Examples / smoke checks

Through the real `security_check.py` entry point on committed fixtures, show
default-order and seed-0 suite processes, all quality sub-gates, Bandit,
`check_cairn`, byte-integrity refusal, local exit 5 and join-only `PASS`.
Check report paths outside the detached checkout and no silent acceptance of
absent expected nodes. Run prose claim/link/snippet and neutrality gates for
changed docs. At the authorized release point, require native Mac and Windows
outputs at one SHA and their joined record. The certifying pair remains
separately required; no full suite runs during proposal or routine iteration.

#### Security preflight

* **S1 — Who supplied it?** The checked commit comes from local Git; the
  fixed expected native-node roster is reviewed from committed test source
  and protected collection records, not either run's collection. Host OS,
  interpreter and outcomes come from each machine; the Maintainer supplies
  both records to the committed runner's join mode. Candidate code still
  partly judges itself, as today.
* **S2 — Can it fail?** Mutation controls must make a non-platform skip,
  wrong SHA, omitted/deselected native node, stale allowlist, removed phase
  or changed checkout byte fail. The independent fixed roster, not observed
  collection, must catch absence. None ran in this proposal-only turn.
* **S3 — What fires it, over what?** `python bootstrap/security_check.py`
  selects committed bytes, derived Bandit targets, all `bootstrap/tests` with
  default order plus seed 0, and all three quality sub-gates. The current
  `SECURITY.md` says: "One command, and its output belongs in the release
  notes." Revise it to name the two native invocations and explicit join;
  the Maintainer performs that join on the final candidate.
* **S4 — Which way does it break?** Unknown platform, malformed or missing
  counterpart, duplicate/missing node, unclassified skip, failed subprocess
  or path/mode mismatch refuses. A passing local check remains incomplete
  (exit 5); only the join may pass. Normalization cannot drop a leaf.
* **S5 — Who still wins?** A party able to change candidate checker and tests
  before review can weaken both; independent review and Maintainer judgment
  remain necessary. Exact-byte matching cannot detect malicious committed logic.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

One host reports release `PASS` alone; a non-platform skip passes; a native
node is absent without refusal; either suite order or a quality sub-gate is
missing; Windows cannot verify committed paths or modes; or joined records
name different SHAs. Any such result keeps #7a open.

## Scope delta

**Scope delta**: lost (opening-draft optimization only). The proposed
one-run-per-host saving is withdrawn because it would lose default-order
evidence. It was never accepted implementation scope; required suite and
security coverage remain intact. The Maintainer's Decision chooses whether
to accept this revised two-order design and its cost. No separate
pre-Decision waiver is requested.

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

## Response -- Codex gpt-6-sol (High) -- 2026-11-05

**Elapsed**: unknown. **Tokens**: unknown.

* **Ordinary blocking 1 -- accepted.** The direct run remains in default
  order and the quality gate retains seed 0. They are two distinct checks;
  no duplicate-removal saving is claimed. The opening one-run commitment is
  recorded as a Scope delta for Maintainer disposition, not waived here.
* **Ordinary blocking 2 -- accepted.** The operative proposal now names the
  fixed expected native-node set, exact per-order node outcomes, local
  `INCOMPLETE`/exit 5, and `security_check.py` as the join reader. It specifies
  malformed, missing, duplicate, wrong-platform and wrong-SHA refusals and
  keeps the final records in the existing release notes.
* **Ordinary advice -- accepted.** Coordinate node identity and fixture
  ownership with 2a without waiting for its archive; Windows path and mode
  fixes remain conditional on native probes. The manual-join alternative and
  maintenance cost are now explicit.
* **Security SR1 -- accepted.** Both full-suite orders remain in the release
  ceremony; the proposed equivalence claim is withdrawn.
* **Security SR2 -- accepted.** Expected native IDs come from reviewed source
  and protected collection records, not observed collection. The join compares
  exactly one native pass per expected ID in both orders at one SHA. A
  deselected native case must fail the join even if pytest exits 0 and omits
  it from its report; this is a named negative control, not a result claimed
  from this proposal turn.

No source implementation, suite, signing or trust operation ran in this
response. The proposal remains `revising` pending independent assessment and
the Maintainer's explicit disposition of the opening one-run commitment.

### Withdrawn / superseded commitments

The opening one-suite-launch-per-host proposal and its implied runtime saving
are withdrawn because they would lose default-order evidence. They are
replaced by the existing default-order plus seed-0 pair, subject to the
recorded Scope delta.

## Review -- Codex gpt-6-sol (ordinary second pass) -- 2026-11-05

Reviewed commit: 5fa0e5357590c164b3cdff10c2870a15bdf99267

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes, subject to Security Review and Maintainer disposition of the lost saving: operative items 2-5 retain both orders and specify the roster, reports and reader -- `security_check.py::run_suite`; `quality_gate.py::_run_order_independence`.
2. **Best alternative.** Manual joining avoids parser upkeep but risks missing an omitted node in long logs; the reader stays in the existing runner and release record -- proposal Alternatives and items 4-5.
3. **What would show it wrong?** A deselected native node or wrong-SHA counterpart yielding joined `PASS` -- proposal Tests required and S2/S4; `conftest.py` currently has no complete node census.

The first review's blockers are closed in operative text. Default order remains; the lost saving awaits Maintainer disposition. Comparing fixed expected IDs to per-order collected/pass records can reject an absent native node even when pytest exits 0. The join names missing, duplicate, malformed, platform, SHA and phase refusals. Upkeep is real: `security_manifest.py` covers protected files, not all platform nodes, and 2a C3 can move IDs. Source-review the roster and reconcile moves.

Local exit 5 means incomplete; pytest's exit 5 means no tests collected. The present parent treats any child nonzero as failure, so end-to-end tests must prove labelled local `INCOMPLETE`/5 and join-only `PASS`. Proposed release-doc edits name the changed Maintainer trigger. Windows path/mode remain investigation.

**Coverage:** Read committed proposal, prior reviews, runner, quality gate, conftest, manifest/tests, 2a and release docs. No native execution, mutation, full suite, Security second pass or release operation; roster and parser are unbuilt.

## Review -- Codex Sol (Security Review, second pass) -- 2026-11-05

Reviewed commit: `5fa0e5357590c164b3cdff10c2870a15bdf99267`

**Model**: gpt-6.1-sol (high). **Tier**: Security Review.
**Findings**: no remaining proposal-level blocker. **Verdict**: ACCEPT.
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the operative contract retains both existing order observations and makes a local result incomplete until a same-SHA native join passes -- Proposal items 2-5; `conftest.py` shuffle hook.
2. **Best alternative.** Keep manual release-log reconciliation, avoiding a parser and roster but leaving omitted native nodes to a person's comparison of long outputs -- Alternatives considered; ordinary review finding 2.
3. **What would show it wrong?** A deselected expected native node, failed child, wrong-SHA report or absent counterpart that produces joined `PASS` would invalidate the mechanism -- Tests required and S2/S4.

SR1 is closed by retaining default order and seed 0. SR2 is closed as a **design**: a fixed expected node set comes from reviewed source, never either observed collection; each host reports exact per-order outcomes; the same runner rejects missing or conflicting records and alone issues joined `PASS`. The earlier Python 3.13.13 omission probe still shows why that independent expectation is necessary. This does not validate the unbuilt roster or parser. The plan must make every expected native node's omission fail, distinguish a child pytest exit 5 from a successful local `INCOMPLETE` exit 5, and verify Windows path/mode behavior before any release claim. Candidate-controlled checker/test changes and unauthenticated record suppliers remain declared limits. The two-order cost is explicit for the Maintainer's Decision; the opening one-run draft was not an accepted implementation scope.

**Coverage:** Revised committed contract, prior findings, runner/quality-gate/shuffle behavior and omission probe. **Not covered:** final native roster, parser or join implementation, Windows execution, full suite, release or trust operations.

## Response to second reviews -- Codex gpt-6-sol (High) -- 2026-11-05

Both the ordinary review at `45467a6b` and Security Review at `21ff70d3`
accept the revised contract; neither has a remaining proposal-level blocker.
The ordinary review's nonblocking notes are accepted for the plan: review
the independently fixed roster against test source and 2a moves, distinguish
child pytest exit 5 from labelled local `INCOMPLETE`/5, and test the real join.
The Security Review's implementation cautions are also accepted: omitted
native nodes must refuse, Windows path/mode behavior needs native evidence,
and unauthenticated record suppliers remain a declared limit. These are
owed implementation checks, not claims of tests already run. The two-order
cost and withdrawn opening-draft optimization are explicit for the
Maintainer's Decision; no separate pre-Decision waiver is sought.

**Elapsed**: unknown. **Tokens**: unknown.

### Withdrawn / superseded commitments

No new withdrawal beyond the one-run optimization recorded in the prior
response and Scope delta.
