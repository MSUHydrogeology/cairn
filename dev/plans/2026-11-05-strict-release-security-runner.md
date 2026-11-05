# Plan: Strict release-security runner

**Source proposal**: dev/proposals/2026-11-05-codex-strict-release-security-runner.md
**Author**: Codex GPT-5 (Plan author, Medium)
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Make the release security check join native Mac and Windows evidence without losing either test order.

## Source proposal

Decision `d042dd33` accepts the heavy proposal: preserve the existing checks
and both suite orders, independently fix the expected native-node roster, and
make the existing runner the sole reader that can join two same-commit host
records into a release-security pass. Local success remains incomplete.

## Scope

Deliver the runner, release hook, focused tests and release documentation as
one independently finishable outcome. Preserve clean committed input, exact
detached bytes and pre/post checks, Bandit over the derived shipped surface
and live allowlist, `check_cairn.py`, all configured suite members and security
assertions, and fail-closed handling. Investigate Windows paths and executable
mode with native probes; change path representation only if the nested-path
probe confirms the mismatch, and retain meaningful mode detection or record an
unresolved barrier. Do not change trust records or the separate certification
pair. Candidate-controlled checks and unauthenticated record suppliers remain
limits, not claims of authentication.

**Reuse.** `bootstrap/security_check.py` already owns detached execution,
phases and byte verification; `bootstrap/tests/conftest.py` owns release
outcome enforcement; `scripts/quality_gate.py` owns the seeded suite and
other quality sub-gates. A search for release, skip, checkout and quality
entry points in those files found these owners. Extend them and their existing
test homes rather than create a second runner or evidence ledger.

### Documentation / doctrine surface

Update `SECURITY.md`, `docs/release-process.md`, `bootstrap/PROVENANCE.md`
and affected source comments to describe two local incomplete results and the
exact join command and Maintainer step. No governing doctrine change.

## Sequence

The existing runner and test infrastructure are available. Estimate two to
four focused workdays, plus availability of native Windows for probes; roster
coordination, platform behavior and review fixes are uncertain. The estimate
does not limit accepted work. Before control-flow edits, coordinate exact node
identities and fixtures with 2a's owner, reconcile committed moves, and record
the independently reviewed source and protected collection evidence. Do not
wait for 2a's remaining chunks, growth report or archive.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Establish and review the fixed native roster; probe Windows path and mode behavior. | Both plan reviews folded; 2a coordination before control-flow edits. | Roster basis and native probe evidence, with any barrier named. |
| C2 | Implement per-order evidence, local validation and same-runner join; update docs and tests. | C1; retain every existing phase and test selection. | Fail-closed runner and documented operator path. |
| C3 | Complete ordinary and Security code reviews, fixes and wide Boundary B. | C2 committed with iteration evidence. | Reviewed, verified implementation ready to archive. |

The final v0.7 strict run is a separate named release follow-up: the Maintainer
obtains Mac and Windows records at the final candidate SHA, runs the join and
puts all three outputs in existing release notes. Track this as a standalone
board wait at the board's serialization point, with owner, evidence and a
link to this implementation; no board edit is part of this opening. It stays
unpassed until that evidence exists and does not gate plan archive. Archive
does not authorize release or a trust operation.

## Acceptance criteria

**C1.** List every expected Mac-only and Windows-only node from independently
reviewed committed test source and protected collection records, not host
observations. Reconcile 2a moves and fixtures before editing control flow.
On native Windows test a nested committed path and executable-mode handling;
preserve each leaf and meaningful mode detection. An unexplained failure or
unresolved Windows barrier remains implementation work, not a release pass.

**C2.** Both full selections run: direct default order and the quality gate's
seed 0, along with neutrality and redundancy. Only named opposite-platform
skips are locally eligible; unexpected or collection skips, xfails, xpasses,
failures and missing nodes refuse. Each order writes exact collected outcomes
to an external temporary path; the runner validates them against the fixed
roster and emits a structured local record with full SHA, platform, Python
3.13, roster identity, phase results and each expected outcome in both orders.
Successful local execution says `INCOMPLETE` and exits 5; a child pytest exit
5 is failure. Only the same runner's explicit join against clean final HEAD
can print `PASS` and full SHA, after exactly one native pass per expected node
per order and validation of both records. Missing, duplicate, malformed,
wrong-platform, wrong-SHA, roster-mismatched or failed-phase evidence refuses.
No report enters the byte-verified checkout. Documentation gives the actual
command, result, Maintainer ownership and residual supplier limitation.

**C3.** Independent ordinary and Security code reviews cover the committed
implementation; findings are disposed and required targeted follow-up occurs
before wide Boundary B. All accepted checks and any Windows barrier are
resolved before archive. The final native release ceremony remains separate.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: before edits use `python tools/test_tiers.py for <paths>`; run the
listed tests for changed files during iteration, plus standing prose gates.
Map changed behavior, callers, configuration, readers and public paths to
their test owners. Resolve moved paths after 2a coordination; current owners
include `test_security_check.py`, `test_broad_run_guard.py`,
`test_quality_gate_cli.py` and `test_quality_gate_order_independence.py`.
Run `python scripts/claim_check.py` on changed documents, link and snippet
checks, and the neutrality gate. Search for readers and byte pins.

Exercise the real entry point on committed fixtures: both suite processes,
all quality sub-gates, Bandit, `check_cairn`, byte-integrity refusal, external
report paths, labelled local exit 5 and join-only pass. Include the tiny
positive control and omitted or deselected expected node, duplicate outcome,
bad JSON/schema, collection skip, wrong platform or SHA, roster drift, failed
phase, xfail, xpass and unexpected skip. Test stale allowlist, removed phase
and changed checkout bytes. List the roster from the tree and mutate each
eligible native case in its own copy; retain repeatable controls in tests or
scripts and report outcomes and omissions. These are implementation checks,
not claims that they ran during planning.

Boundary C: ordinary and Security reviewers read committed work and iteration
evidence and run targeted falsification, not a suite. A substantive review
fix returns to the same reviewer for a targeted look before final integration.
Boundary B: after reviews run the iteration list for the reviewed range plus
mapped integration/workflow tests and plan-specific checks on a clean,
unchanged final commit under canonical Python 3.13.x. Use **wide** for this
trust ceremony; name owning families, public paths and standing gates. Append
the prescribed record with SHA and range, interpreter, clean pre/post state,
commands, counts, elapsed and token use, non-pass dispositions and omissions;
record timing misses. A missing required check keeps work open. Do not run the
full certifying suite during routine implementation; the separate authorized
certifying pair and the final release run remain unchanged.

## Plan review -- Codex GPT-5 (Medium) -- 2026-11-05

Reviewed commit: 9dd17bbfd6c84761c9a8e27441da0339444e432b

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the chunks preserve both full orders, fixed native expectations and the same-runner join, while leaving the final release ceremony outside archive -- plan C1-C3; proposal Decision `d042dd33`.
2. **Best alternative.** Manual comparison avoids a reader but leaves missing native outcomes to human inspection; extending the existing runner better delivers the accepted automatic refusal -- proposal Alternatives; plan Scope and C2.
3. **What would show it wrong?** A deselected native node or wrong-SHA counterpart producing a joined pass would disprove the evidence join -- plan Verification; proposal Tests required.

The plan makes roster review and 2a coordination prerequisites to control-flow edits, and specifies the two per-order reports, local incomplete result, child exit distinction and join refusals. Its final release wait has an owner and evidence without making archive a release authorization. Native Windows barriers and missing checks remain implementation work.

**Coverage:** Read the committed plan, accepted proposal and Decision, and plan template against the requested ordinary-review questions. No implementation, native execution, mutation, full suite or Security Review was performed; the roster and reader remain unbuilt.
