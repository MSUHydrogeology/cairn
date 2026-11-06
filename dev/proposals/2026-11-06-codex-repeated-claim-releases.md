# Releasing a claim twice should leave it closed

**Author**: Codex (ordinary proposal author; Medium floor; runtime model identifier unavailable)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy -- shipped reader and protected test owner
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-06
**In brief**: Let the next-work advisory read valid repeated releases without weakening its checks for invalid or conflicting claims.
**Elapsed**: approximately 10 minutes
**Tokens**: unknown

## Decision summary

Change the existing board reader and its installed copy, with a regression in
the current intent tests. Releasing an already-closed work claim will keep it
closed, as the intent tool already defines. Invalid records and active conflicts
will still stop the advisory. This adds no tool, file format, cleanup task or
human operation.

## Context

`tools/board.py --next` currently stops with a claims-ledger error in Cairn,
although the intent tool can read that same ledger. Sol's read-only diagnosis
against source `308d53f3` found 6,432 valid records: 3,195 claims and 3,237
releases, with 44 repeated releases and no duplicate claim, orphan release or
release preceding its claim. The two active claims were unaffected. The log
did not change during that inspection; these counts are a dated observation,
not a current inventory.

The cause is specific. `tools/_intent/record_io.py` defines active claims as
claims lacking a released ID, while `_cmd_release` in `tools/_intent/cli.py`
can append another release. The board's `_next_claim_check` rejects an ID already
in its release set. The repeated releases differ in optional commit annotations,
so accepting only byte-identical repeats would not restore normal operation.

## Proposal

For v0.7, make release handling idempotent: repeating a release after its known
claim has no further effect. Preserve strict record parsing, duplicate-claim
refusal, orphan and release-before-claim refusal, trusted-reader loading, path
and identity checks, and all active-conflict checks. Neither release annotations
nor the advisory become authority to act.

Keep `tools/board.py` and `templates/skills/_lib/board.py` identical. Extend the
existing installed-entry test in `bootstrap/tests/test_intents_tool.py` to
exercise claim, release, second release and the real next-work command, including
differing optional annotations. Retain the neighboring refusal controls.

Recommend a named addition to the active heavy safe-Git plan after acceptance,
if its Decision explicitly authorizes that plan deviation: the protected intent
test owner is already in that plan's verification inventory, and the board's
trusted intent binding needs coordinated ownership. Preserve all original safe-Git
outcomes. This avoids parallel ownership and another plan solely for this small
repair; it does not waive proposal reviews, code reviews or checks. If this
cannot form a coherent addition, keep the accepted fix queued for its own plan.

## Rationale

One compatible reader fixes the cause. Rewriting history or changing release
writers adds work while leaving existing valid histories unreadable. No
continuing cleanup or operator judgment should be needed.

## Alternatives considered

Leave the advisory stopped: zero build work, but agents need manual routing.
Prune the ledger: current active claims prevent supported pruning, and the
default age would remove none of these repeats; a shorter age removes history
rather than just redundant releases. Change every writer to suppress repeats:
more coordination and still no repair for existing logs. Recommend the reader fix.

## Documentation / doctrine surface

No rule or schema change is proposed. The operative reader pair and its existing
test owner carry the fix; accepted reasoning stays in this proposal and the
implementation plan. Describe the restored advisory behavior in the changelog.

## Evidence / verification plan

### Tests required

Use `tools/test_tiers.py for` on all changed paths. Exercise the installed
claim/release/NEXT path with two releases, then test malformed records, duplicate
claims, orphan/pre-claim releases, active overlap and unavailable identity.
Source and shipped copies must agree. Preserve the protected owner's obligations
and final mapped verification; no implementation test has run for this repair.

### Examples / smoke checks

After synthetic tests, run Cairn's advisory read-only against its unchanged log.
It may still stop for another valid reason; success means it no longer calls
normal repeated releases invalid. Run scoped claim/link/snippet and neutrality
gates. Do not prune, rewrite or regenerate the actual ledger for the test.

### Security preflight

**S1.** Claims are project coordination data, not authenticated approval. The
existing trusted reader and record validator remain the authority for parsing.
**S2.** A second release currently reproduces the rejection; implementation must
show the real-entry regression fails before the fix and passes afterward, while
the invalid/conflict controls still refuse. Those synthetic checks have not run.
**S3.** The existing intent owner runs through mapped pytest selection and the
installed board entry point; there is no new checker or hook.
**S4.** Only a repeat after a validated existing claim is ignored. Unknown IDs,
invalid records, duplicate claims and active conflicts retain their stop behavior.
**S5.** A same-user writer can already forge a well-formed release; neither this
fix nor the claims system authenticates human decisions.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The advisory accepts an orphan release, overlooks an active conflict, or needs
manual history cleanup before it can use a normal repeated release.

## Scope delta

**Scope delta**: preserved as opened. No reader safeguard or safe-Git outcome
may be removed to include this repair.

## Assurance path

**Assurance path**: high-assurance. Both proposal reviews, an explicitly
authorized implementation home, independent usual and Security code reviews,
and mapped final checks remain required. No trust-ref operation is authorized.

## Response -- Codex (Medium floor; runtime model identifier unavailable) -- 2026-11-06

Both reviews proceed without findings (`0474a341`, `7fc41ea4`); no operative
revision is needed. Their implementation falsifiers remain required, including
an invalid second release and a duplicate claim after release, alongside the
before/after installed-entry test and active-conflict checks. No actual ledger
cleanup is authorized. Incorporation into the active safe-Git plan still needs
the explicit delegated Decision and named scope addition; overlapping files
alone do not grant that authority. Scoped prose gates passed on the committed
opening; implementation checks have not run. **Elapsed**: approximately 2 minutes.
**Tokens**: unknown.

### Withdrawn / superseded commitments

None.

## Review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Reviewed commit**: `f2c4615018f71e30c88165f8d5a5f15d27f7b3cf`
**Tier**: Internal

**Foundations**:

1. **Should this happen as framed?** Yes. The board rejects a second release even when its claim is known, whereas the intent reader treats any released ID as closed; the proposal confines compatibility to validated histories and retains the stricter invalid and active-conflict stops. -- `tools/board.py::_next_claim_check`; `tools/_intent/record_io.py::active_intents`; Proposal and Security preflight S4.
2. **Best alternative.** Repair the existing reader and mirror its shipped copy, using the installed-entry test. Leaving the stop costs no build work but loses the advisory; changing writers alone leaves existing repeated releases unreadable. The proposed safe-Git plan addition needs explicit authority and coherent scope; otherwise a separate plan preserves delivery. -- Alternatives; `bootstrap/tests/test_intents_tool.py::test_next_installed_plan_review_and_identity_stops`; Proposal.
3. **What would show it wrong?** The real installed entry must pass a claim followed by two valid releases, including different annotations, and still refuse orphan or pre-claim releases, duplicate claims, malformed records, unavailable identity and active overlap. A before-fix failure and after-fix pass would establish the regression; any weakened refusal or need to rewrite history falsifies the approach. -- Tests required and Security preflight S2–S4.

**Findings**: none. **Verdict**: PROCEED to author response after the separate Security Review.

**Coverage**: Read the committed proposal, template, board reader, intent release/active-set logic, installed test home and safe-Git plan scope and verification. Did not inspect the live ledger, reproduce the reported count, run synthetic tests, decide the implementation home or perform Security Review. **Elapsed**: approximately 3 minutes. **Tokens**: unknown.

## Security proposal review -- Codex GPT-6.1 Sol (High) -- 2026-11-06

**Reviewed commit**: `0474a34186c1c17ba18a186015b9670928b1c686` (operative proposal `f2c46150`).
**Obligation**: Internal Security Review
**Tier**: Internal Security Review

**Foundations**:

1. **Should this happen as framed?** Yes. Releasing a known, validated claim twice should leave it closed; strict parsing and active-conflict refusal must remain independent. The writer permits repeats and `active_intents` uses a released-ID set, while the board rejects repeats. Claims remain coordination data, not authenticated approval. -- `tools/_intent/cli.py::_cmd_release`, `record_io.py::active_intents`, `tools/board.py::_next_claim_check`; S1/S4/S5.
2. **Best alternative.** Fix the existing reader pair and installed-entry regression as proposed. Leaving the advisory stopped needs manual routing; changing writers alone cannot repair existing histories, and pruning adds history loss and coordination risk. Combining this with safe-Git work is reasonable only after an explicit Decision authorizes the named scope addition and preserves its outcomes; otherwise retain the separate-plan route. -- Alternatives; Proposal; safe-Git plan Scope and Scope delta.
3. **What would show it wrong?** The installed command must reject an invalid second release, an orphan/pre-claim release, a duplicate claim even after release, or another agent's active overlap despite valid repeated releases. Show the valid different-annotation sequence failing before and passing after the fix, while retaining identity, path and trusted-loader stops. Validate each record before applying idempotent reduction. -- Proposal Tests/S2–S4; `record_io.py::_strict_record`; installed identity/conflict and malformed-ledger tests in `test_intents_tool.py`.

**Findings**: none. **Verdict**: PROCEED to author response and the existing Decision process.
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Coverage**: Read committed proposal/template, usual review, reader/writer/validator contracts, installed test home and safe-Git scope. Did not inspect the actual ledger, verify reported counts, run tests, implement or select the implementation home. Mirrored delivery, protected-test obligations, usual/Security code reviews and mapped final verification remain due.
