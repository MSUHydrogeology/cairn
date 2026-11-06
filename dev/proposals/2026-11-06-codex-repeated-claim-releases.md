# Releasing a claim twice should leave it closed

**Author**: Codex (ordinary proposal author; Medium floor; runtime model identifier unavailable)
**Status**: awaiting-review
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
