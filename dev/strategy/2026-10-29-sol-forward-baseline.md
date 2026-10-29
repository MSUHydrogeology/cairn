# A reviewed baseline for forward trust

**Author**: Codex (Sol), Strategy
**Model**: Sol; runtime identifier is not independently exposed to this agent
**Date**: 2026-10-29
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: test-trust-boundary and ceremony-commands proposals/plans; bootstrap runbook

## The question / felt gap

Recommend exploring one independently reviewed, signed current baseline, replacing
both compatibility checkpoints. Preserve useful protection going forward without
requiring this single-developer project to reconcile every historical gate change.
The Maintainer authorized giving up comparison with the old anchor and deferred
actual re-anchoring until v0.6. No installation is authorized now.

Maintainer chat, 2026-10-29, relayed verbatim:

> I am completely fine with not checking any changes against an anchor. We can re-anchor now

> Or rather, at v0.6

These words settle the loss of historical comparison and timing; they do not
remove checks from existing tools or certify old commits.

The work has a visible opportunity cost in repeated implementation and review;
there is no measured time or token percentage here. The already-approved boundary
is the starting point: 90 protected Python paths, including 78 test files and 12
control modules, and 51 ordinary test files. Do not broaden it by default.

## Method

Read AGENTS.md, the strategy template, the trust plan, Decisions `cca436a9` and
`02a81d33`, exact-roster approval `3e9f8fc2`, dormant-preparation authorization
`6e3197f6`, and ceremony plan `23430733`. Inspected committed ceremony code at
`3b780b40` and raw installed anchor `443de20f81169fabe36c4ca3cc620206f7850254`.
No baseline, tests, signature, ref installation or certification was performed
for this exploration. Earlier narrow scratch probes are not evidence that this
proposed baseline command works.

## Findings

Two protections differ. Authenticating old commits establishes who signed their
bytes; it does not establish correctness. The current prior-anchor mechanism also
supplies trusted executable verifier/scanner code and the expected manifest
against which today's candidate is compared. Replacing P443 retires that second
comparison for the accumulated P443-to-C interval. Keeping Git history intact does
not preserve the assurance of that comparison.

The trust Decision accepted less protection for ordinary tests, including their
possible influence on protected execution. The approved roster's raw SHA-256 is
`188fa76d82744be571bdc7ca91a43d605776b9df5ba0ac729e2cf22af66b8cc4`.
Its recorded proposed frozen union was 147 paths, preserving 57 non-test frozen
paths and seven fixture mechanisms. Those are classification-source figures,
not a fresh census of the eventual baseline; recalculate the actual manifest.
The approved split still protects 78 test files versus 51 ordinary files. A new
baseline does not free additional files or make protected edits cheap. There is
no new classification evidence here supporting a further reduction; that is a
separate choice, not part of approving this baseline.
Sources: `bootstrap/tests/fixtures/protected_test_roster.json` and
`dev/plans/2026-10-28-test-trust-boundary.md`.

Existing machinery supplies most operations, but no examined public command
implements this replacement-root workflow. In
`bootstrap/tests/_gate_manifest.py`, `produce` collects the full candidate suite
and refuses failed or empty collection. In
`bootstrap/tests/_gate_preflight.py`, static re-derivation checks manifest fields;
`_construct_signed_commit`, `verify_constructed`, and `_advance_both_refs` provide
one signed manifest commit, exact verification, and atomic expected-old updates.
Ordinary stage 1 still depends on the old anchor. The dormant checker explicitly
refuses a narrowed prior manifest: the baseline candidate must contain the
reviewed active setting. Changing that setting is not authorized by the earlier
approval to prepare a dormant candidate.

## Options

| Option | Benefit | Cost or loss |
|---|---|---|
| Finish two transitions | Preserves the accepted old-anchor comparisons and separate installation evidence. | Two candidates, packages, reviews and human ceremonies; actual P443 compatibility still needs demonstration. |
| Review and install one current baseline | One initial installation; subsequent ordinary maintenance uses the approved narrow boundary. | Gives up historical protected-drift adjudication and needs a small reviewed bootstrap mode. |
| Keep the existing broad freeze / do nothing | No new root or installation now. | Ordinary test maintenance remains constrained; neither current plan is delivered. |

None has a defensible elapsed-time estimate from this exploration. The baseline
replaces two installations with one; it does not eliminate implementation,
independent review or required verification. No extra future feature is proposed.

## Recommendation

Carry the authorized direction into the plans: one current baseline at v0.6,
with no historical comparison or individual old-HOLD reconciliation as a
prerequisite for continuing work:

1. Select a clean committed C containing the final reviewed verifier, active
   checker, reusable commands and exact approved roster. Current `3b780b40` is
   inspected source, not the proposed final C: its baseline mode is unbuilt and
   its checker is dormant. Finish only the functions needed for this route.
2. Have independent ordinary and Security reviewers assess the present control
   surface and its evidence: all approved protected membership, controlling
   helpers, retained script/module/fixture protection, signer configuration and
   baseline loader. Reviewers need not reconstruct every old commit. They must
   identify coverage gaps rather than call a green suite independent authority.
3. A maintained preparation command extracts exact C from raw objects, checks
   containment and file membership, and runs collection with the key away. It
   builds the roster-bound manifest, independently re-derives static fields, and
   binds C, tool/interpreter hashes, collection, manifest and reader record into
   one reviewable package. Required tests challenge protected edits/deletions and
   markers, ordinary notes, roster substitution, stale packages and signing
   identity. Use the reviewed owning families in the two plans, not another
   blanket mutation exercise. Run required canonical certification before the
   actual re-anchor; none is authorized or claimed by this note.
4. The Maintainer compares script/package/manifest hashes and signer fingerprint
   with the independent reader's record and approves the exact baseline and
   stated assurance loss. A maintained install command rechecks that package
   and C, runs no candidate tests, signs once, verifies N has parent C and only
   the reviewed manifest change, and atomically updates branch and gate anchor
   using observed old values. Preserve the old anchor ID in the record. This is
   explicitly authorized C4 work performed by the Maintainer; pushing is separate.

Afterward N supplies trusted code and membership for future comparisons. Protected
byte changes, protected node loss and new skip/xfail markers still HOLD; ordinary
changes remain visible notes. New trust tests require deliberate admission.
Signing does not prove the baseline harmless: independent review establishes the
initial judgment, and signatures identify the approved bytes. Host-capable
candidate collection can influence execution, tests or writable tools; these
checks neither contain it nor repair a compromised machine.

The reported 83 pending old-P HOLDs are **not cleared** or individually
reconciled. Their current complete contents were not remeasured here. The
Maintainer has authorized retiring reliance on that comparison; retain the report
as unresolved historical evidence. Independent inspection of the v0.6 baseline
replaces per-item historical authorization. This does not prove those changes
benign: unnoticed earlier weakening may be incorporated into C. Work can proceed
without historical reconciliation; the existing scripts still enforce their
current checks until reviewed changes implement this direction.

## Open questions

Record the authorized substitution in the trust plan's
C2–C5 and ceremony plan's C1–C4 obligations, including old-P verification/E7 and
two bridges **for initial installation only**. Record the scope change through
their lifecycle; changed high-risk design requires independent plan and ordinary/
Security code review. Retain future signed-prior checks. Preserve meaningful
no-signed-predecessor support through the explicitly reviewed baseline mode,
rather than fabricating a predecessor or silently invoking the old first-run path.
Prepare and test the revised commands before release; perform the actual
Maintainer-only baseline installation at v0.6, not now. Final authorization binds
the exact release candidate, package and signer. No push is implied.

**Strongest falsifier:** after the real public installation command creates N in
a scratch repository, a protected-file change or protected-node/marker loss passes
the authenticated N verifier, or substituted candidate code executes during its
signing phase. An ordinary edit that still demands another root installation
would also defeat the intended nimbleness.

## Fold-up note

No methodology change is proposed. A local trust-root replacement must name its
lost comparison and its new source of authority plainly.
