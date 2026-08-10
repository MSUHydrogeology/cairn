# Claim-check exemption hygiene: preserve the check, retire the header landfill

**Author**: Codex (Strategy)
**Model**: GPT-5 (Codex)
**Date opened**: 2026-08-10
**Status**: proposed
**Amends**: `review-efficient-lifecycle`
**Touches**: `scripts/claim_check.py`, its installed twin,
`bootstrap/tests/test_claim_check_module.py`, the self-hosted and shipped
claim-check module prose, proposal/plan authoring templates, lifecycle doctrine,
and a bounded migration of active proposal/plan header metadata
**Related**: `review-efficient-lifecycle`, the claim-marker-maintenance rule,
and commit `29e9076`
**Plan review**: required(**External, security lens**) -- the change narrows an
author-controlled validation exemption and ships to adopters; it should join
the eventual `review-efficient-lifecycle` plan after acceptance.

## Context

`review-efficient-lifecycle` was accepted to make rigorous review consume less
irrelevant material. Its current contract does not touch claim checking, but
the proposal and plan records expose the same failure shape in miniature:
exception declarations accumulate faster than they are retired, historical
lifecycle moves look like broken claims, and a green check can mean either
"all paths resolve" or "a header comment silenced them."

The mechanism is not worthless. A clean-tree scan at commit `857c216` on
2026-08-10 found eight active proposal/plan artifacts with
`claim-check-allow`, containing 64 configured globs. Removing those directives
in memory exposed 124 unresolved-path reports across seven artifacts. The
reports include legitimate future paths, historical references whose exact
files moved into `archive/`, and heuristic false positives. The exemption
therefore carries real load.

The maintenance state is nevertheless poor:

* 22 of the 64 configured globs suppress no current report;
* `fork-advisory-semantics` carries an entirely unused directive;
* every one of the 11 active proposal/plan artifacts at the measured commit
  carries a
  `cairn-internal-ref-allow` header, although `scripts/check_cairn.py` applies
  that mechanism only when the scanned path begins with `templates/`;
* `release-security-bar` suppresses references to lifecycle files that now
  exist under `archive/`, allowing claim-check to print clean without resolving
  the record's current location; and
* the existing `Proposed paths:` / `Untracked paths:` /
  `External-repo paths:` markers exempt only their compact local blocks, so an
  author who discusses a declared path later must add a document-wide HTML
  directive as well.

The recent claim-marker-maintenance doctrine correctly permits a mechanical
marker insertion when an append-only record develops a false positive. It is a
repair channel, not a reason to make archive moves and stale declarations
permanent manual work.

## Proposal

Amend `review-efficient-lifecycle` with a bounded claim-exemption-hygiene
contract. Keep claim-check's hard path and line-bound checks. Replace routine
header suppression with exact lifecycle resolution, typed path declarations,
and liveness validation.

The separate `link-check-allow` mechanism is out of scope. Markdown links must
continue to name their current target, including its `archive/` location; this
proposal changes only how claim-check interprets backticked path assertions.

### 1. Resolve exact lifecycle archive moves

When a backticked token names a missing active lifecycle file in exactly one of
these forms:

* `dev/proposals/<filename>.md`; or
* `dev/plans/<filename>.md`,

claim-check also tests the corresponding exact sibling path under `archive/`.
If that exact file exists, it is the resolution target for claim checking.

This is an identity rule, not a fuzzy search:

* it never searches by partial stem, date, author, or similar name;
* it never crosses from proposals to plans;
* it never applies outside the two lifecycle directories;
* it does not alter Markdown-link resolution; links still name their real
  current target; and
* a `path:N` or `path:N-M` citation is checked against the archived file's
  actual line count. Moving a file does not waive stale line bounds.

The direct path remains authoritative when it exists. A duplicate active and
archived identity is not silently normalized; the implementation must surface
the lifecycle-state violation through an existing or explicit invariant check.

### 2. Make typed path declarations document-wide and exact

The existing marker vocabulary remains:

* `Proposed paths:` for files the accepted work will create;
* `Untracked paths:` for intentionally local or ignored files; and
* `External-repo paths:` for paths resolved in a named sibling repository.

A compact marker block becomes a document registry. Each exact backticked path
listed in the block may recur elsewhere in that document without requiring a
second HTML directive. Registry entries are literal paths, not globs. Each
entry carries a short reason in prose, and claim-check reports every token it
exempts together with the declaration that authorized it.

A declaration is live only when it exempts at least one occurrence outside its
own marker block. A `Proposed paths:` entry becomes stale when the local path
materializes. `Untracked` and `External-repo` entries remain unresolved by
design, but still become stale when nothing in the document cites them.
Malformed or duplicate declarations fail closed.

This changes the marker from a fragile adjacency trick into a small,
human-readable registry. It does not infer paths from plan prose or chunk
tables, and it does not let one declared path exempt a sibling or descendant.

### 3. Retain `claim-check-allow` as the last resort, with liveness

The document-scoped HTML directive remains available for a genuine heuristic
false positive that cannot be expressed as one of the typed path declarations.
Its current narrow-glob validation and exact exemption reporting remain.

For active proposal and plan artifacts, every configured glob must suppress at
least one current would-be hard report. An unused glob is itself a hard
directive finding. The output names the stale glob and its directive line.

Archived proposals and plans are grandfathered: claim-check continues to parse
and report live exemptions there, but does not fail them merely because an old
glob has become unused. Archive immutability wins over cosmetic cleanup. Other
Markdown surfaces retain their existing behavior unless the implementation
plan measures them and a reviewed amendment explicitly expands the liveness
rule.

### 4. Stop emitting inert internal-reference headers

Remove `cairn-internal-ref-allow` from Cairn's self-hosted
`dev/proposals/_template.md` and `dev/plans/_template.md`. The dangling-internal-
reference checker intentionally scans only adopter-facing files under
`templates/`, so the directive has no effect in self-hosted `dev/` artifacts.

Retain the directive in shipped `templates/core/dev/` instruction files, where
doctrine citations would otherwise dangle in an adopter tree and the checker
does enforce it.

After acceptance, perform one bounded migration over non-archived proposals and
plans:

* remove inert top-level `cairn-internal-ref-allow` comments;
* remove unused `claim-check-allow` globs;
* replace live future/untracked/external globs with typed declarations where
  the new exact registry can express them; and
* leave archived artifacts untouched.

The migration changes only exemption metadata. It does not rewrite historical
prose, findings, Responses, Decisions, attribution, or path tokens.

### 5. One plan, not another implementation stream

If accepted, this proposal and `review-efficient-lifecycle` open one plan. The
claim-check work is a separately reviewable chunk with its own tests and commit,
but the plan has one current contract, one evidence boundary, and one archive
sequence. Rejection of this amendment does not invalidate the already accepted
parent proposal.

### Documentation / doctrine surface

The governing claim-marker rules in `doctrine/proposals.md` and
`doctrine/plans.md` will distinguish automatic archive identity from genuine
forward/external declarations and retain the bounded maintenance exception for
cases the checker cannot classify. `doctrine/lifecycle.md` needs only the
matching routing statement if the canonical rule remains there.

The self-hosted and shipped claim-check module prose will document exact
archive resolution, registry scope, liveness, and the immutable-archive
grandfather. Proposal and plan templates will show the concise registry form
and will no longer instruct authors to preserve fragile physical-line
adjacency throughout the document.

This clears the doctrine-evolution rate limit through recurrence rather than a
single annoyance: 64 configured globs across eight active artifacts, 22 already
unused, 11 inert copied headers, and a dedicated maintenance commit caused by
archive-move findings are repeated instances of the same exemption-lifecycle
failure.

## Rationale

Scientists should see a path check and understand what passed. Exact lifecycle
resolution removes false alarms caused by Cairn's own file-state machine.
Typed declarations make intended exceptions readable in the body of the work.
Liveness turns exemptions into temporary debt that retires itself instead of
quietly becoming the permanent preamble to every serious artifact.

The stable boundary remains intact: claim-check is a discipline aid, not an
authenticator. A contributor can still write a false reason or deliberately
declare a path that should have resolved. Independent review remains the
semantic check. This proposal improves the mechanical signal without claiming
authority the tool does not possess.

The timing is favorable because `review-efficient-lifecycle` is accepted but
has not opened its plan. A reviewed amendment can therefore join one coherent
implementation rather than forcing a later retrofit.

## Alternatives considered

**Delete `claim-check-allow`.** Rejected. The reproduced 124-report delta shows
that real forward-reference and heuristic cases remain. Removing the escape
hatch would trade header clutter for marker churn and pressure authors to avoid
precise path claims.

**Keep the mechanism and periodically clean headers by hand.** Rejected. The
22 unused globs demonstrate that optional cleanup does not happen reliably, and
manual maintenance does not solve archive moves or repeated future-path
references.

**Silently search the whole archive by stem.** Rejected. Fuzzy historical
resolution could turn a typo into a clean check. Only the exact active-to-
archive transformation is admitted.

**Edit archived records to current paths.** Rejected. That would spend review
integrity to improve presentation. The resolver should understand the
lifecycle, while archived bytes remain historical.

**Put this directly into the accepted parent proposal's plan.** Rejected. The
accepted contract does not name claim-check behavior, and a plan may fill in
implementation detail but may not enlarge a Decision. This amendment pays one
focused review and then shares the parent's plan.

## Evidence / verification plan

The implementation plan must preserve the measurement script or equivalent
fixture that classifies each active exemption as future, untracked, external,
archive-moved, heuristic false positive, or stale before migration. Aggregate
counts are dated evidence, not permanent acceptance criteria.

### Author-accounting -- invariants, failure modes, edge cases

| Invariant | Enforcement |
|---|---|
| A missing active lifecycle path resolves only to its exact same-family archive sibling. | Unit tests mutate filename, family, and archive location independently; each mutation must hard-flag. |
| Archive-aware line citations retain bounds checking. | A fixture cites the final valid line and then one line beyond it. |
| A typed declaration exempts only the exact registered path. | Tests cite the exact path, a sibling, a descendant, and a lookalike prefix. |
| Every active-file exemption is live. | Tests cover unused globs, unused declarations, materialized proposed paths, and archived grandfathering. |
| The installed checker remains byte-identical to Cairn's source checker. | Existing reference-script parity test plus an explicit comparison in the implementation commit. |
| Shipped template doctrine markers remain effective while self-host markers disappear. | A template-surface test runs `check_cairn` with and without the shipped marker and confirms self-host files are outside that check's class. |

Failure is closed for malformed declarations, duplicate registry entries,
ambiguous lifecycle identity, stale active exemptions, and unresolved paths.
An exact archived identity and a declared future/untracked/external path are
intentional accepted resolutions and remain visible in output.

Edge cases include an empty registry, one and many entries, spaces or anchors
in tokens, duplicate declarations, a path that materializes during drafting,
active/archive duplication, proposal/plan name collision, line citations, and
an archived document whose old glob no longer suppresses anything. Absolute
paths and generalized rename history are out of scope.

Public path to test mapping:

* `scripts/claim_check.py` and its installed twin ->
  [`bootstrap/tests/test_claim_check_module.py`](../../bootstrap/tests/test_claim_check_module.py)
* installed-script execution ->
  [`bootstrap/tests/test_reference_scripts.py`](../../bootstrap/tests/test_reference_scripts.py)
* template-only internal-reference classification ->
  [`bootstrap/tests/test_cairn_prefix_links.py`](../../bootstrap/tests/test_cairn_prefix_links.py)

Known omission: the tool does not determine whether an author's declaration
reason is true. That remains review work.

#### Security preflight -- five questions

**S1 -- Who supplied it?** The candidate Markdown supplies both the path claim
and any declaration that exempts it; the repository supplies path existence and
archive state. The exemption is therefore self-declared evidence, not an
independent trust root, and must remain explicit in output and reviewable in the
diff.

**S2 -- Can it fail?** Yes. Removing the exact archive target, changing the
lifecycle family, citing beyond the archived file, changing one character of a
registered path, or leaving a glob unused must each produce a hard finding. The
plan records the mutation run rather than only the green case.

**S3 -- What fires it, over what?** `python scripts/claim_check.py <file>` runs
the standalone check, and `python scripts/check_cairn.py` composes it across the
selected Markdown tree. The installed claim-check module documents the same
scope for adopters.

**S4 -- Which way does it break?** Malformed, ambiguous, duplicate, and stale
metadata refuses. Archive resolution is narrowly additive only for an exact
lifecycle move. No fallback broadens to fuzzy matching or a whole directory.

**S5 -- Who still wins?** A trusted contributor can deliberately register a
plausible but false future or external path and write a false reason. This class
is not closed mechanically; structural review and the visible exemption report
remain the control.

### Tests required

The affected behavioral home is `bootstrap/tests/test_claim_check_module.py`,
with installed-path coverage in `bootstrap/tests/test_reference_scripts.py` and
template-classification coverage in `bootstrap/tests/test_cairn_prefix_links.py`.
The plan must map each invariant above to named nodes before implementation.

Run the affected nodes during the claim-check chunk. Run the canonical
`bootstrap/tests` suite once at the stable integration boundary under Python
3.13.x, following `verification-evidence-boundaries` and the accepted parent
proposal.

### Examples / smoke checks

Run claim-check directly over:

1. a fixture with an exact archived plan path and an in-bounds line citation;
2. the same fixture with a misspelled stem and an out-of-bounds citation;
3. an active proposal with one declared future path cited multiple times;
4. an active proposal with an unused declaration and unused allow-glob; and
5. an archived proposal carrying a now-unused historical glob.

Then run `python scripts/check_cairn.py` over the changed Markdown surfaces and
compare source/installed checker bytes. No example-gallery or scaffold smoke is
required because the existing installed-script test exercises the adopter entry
point directly.

## Signals the change is wrong

Pause or revise if archive resolution accepts a near match, line bounds stop
failing after a move, a registry entry exempts an undeclared sibling, the
migration requires editing archived prose, active authors still need both a
typed declaration and an HTML allow for the same exact path, or check output no
longer identifies which declaration suppressed which token.

Retire the document-wide registry if measured authoring shows it encourages
large speculative path inventories rather than paths actually used by the
proposal. Retain exact local markers and the narrow fallback in that case.

## Reviewer brief

This review should attack the new sources of false cleanliness rather than the
existence of header clutter alone:

* Can exact archive resolution ever turn a typo into a valid historical path?
* Is active/archive duplication handled by the right tool, or is requiring a
  claim-check refusal misplaced?
* Does document-wide registry scope make a declaration too powerful even when
  it is exact?
* Is hard-failing an unused active glob compatible with append-only review
  records and concurrent lifecycle moves?
* Does the grandfather boundary cover every immutable artifact without giving
  active non-lifecycle documentation a free pass?
* Does the combined-plan commitment preserve a genuinely separable code-review
  target?

Verify the `857c216` snapshot independently: 64 configured globs, 42 live, 22
unused, and 124 reports exposed when the directives are removed. Say whether
this amendment should join the accepted parent's one plan or remain separately
planned.
