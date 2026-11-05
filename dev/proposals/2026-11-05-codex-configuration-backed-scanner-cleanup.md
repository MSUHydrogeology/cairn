# Configuration-backed scanner cleanup

**Author**: Codex GPT-5 (Medium)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Move scanner exemptions into validated configuration and warn when temporary review finding IDs reach published material.

## Decision summary

Checker directives currently interrupt source documents, including material
shipped to adopters. Move the two remaining file-level exemption types into
validated configuration, then use existing scanning machinery to warn about
temporary review finding IDs in shipped modules, documentation and release
notes. Configuration and warnings add maintenance; neither should weaken an
existing check or turn an advisory finding into a release blocker.

## Context

[Board item 9](../PLANNING.md) combines both outcomes and specifies their
order. The [August strategy](../strategy/2026-08-21-claude-nimbleness-recovery.md#5-finish-the-two-remaining-cleanup-items-from-the-august-sweep)
identifies the two inline directives; the [delivery sequence](../strategy/2026-11-02-codex-v07-delivery-sequence.md)
calls for reuse. `scripts/claim_check.py` already reads document-scoped JSON
exemptions and falls back to no configured exemptions on read or shape error.
`scripts/link_check.py` and `scripts/check_cairn.py` still parse the two
inline forms. Inline internal-reference markers also occur in shipped
templates, so migration affects generated material and upgrades.

## Proposal

Deliver both outcomes for v0.7 in one coordinated implementation, with
configuration and migration before the new scan. Reuse the current scanners
and configuration approach, not a separate scanning service or ledger.

1. Define a documented, standard-library-readable configuration contract for
   document-scoped link and internal-reference exceptions: exact source and
   target scope, reason where currently required, validation, diagnostics,
   and behavior for missing, unreadable, malformed, duplicate, broad, stale
   or unused entries. Invalid input must never grant additional exemptions.
   Preserve each existing check's matching, coverage and reporting protections;
   do not conflate its namespace with claim-check exemptions. Inventory and
   migrate the live directives and their reasons without expanding their effect.
   Preserve inline compatibility where existing adopters need it; document
   precedence and a migration path rather than silently invalidating their
   checkouts. Preserve inline reference annotations that are not file-level
   exemptions.
2. Extend an existing appropriate scanner to report transient finding IDs in
   shipped modules, docs and release notes. Define the ID pattern and selected
   paths from actual review records and release inputs, with examples and
   explicit exclusions for legitimate historical discussion. Findings are
   warnings, with location and actionable context, and do not change exit
   status or suppress other findings. Reuse the validated configuration for
   justified exceptions without turning it into a general suppression bypass.
   Review and resolve existing hits, recording deliberate exceptions.

Coordinate shared file edits and checks once. The plan must inventory actual
readers, installed copies and upgrade behavior before choosing configuration
placement and compatibility details; do not change a trust root or install
contract incidentally. A needed boundary change returns for reassessment.

## Rationale

Moving exceptions makes reader-facing text cleaner while keeping exceptions
inspectable. A warning catches references such as a review finding number
that may be meaningless to a future reader, without claiming to interpret
prose or enforcing a new coordinate rule. Configuration is itself an input
capable of hiding defects, so scope and refusal behavior matter.

## Alternatives considered

Doing nothing costs no migration but leaves both the directives and the
board's missing warning. A new standalone scanner or exemption database adds
another interface and maintenance surface without an identified need. A hard
failure for finding IDs would create false-positive release blockers and is
outside the requested warning-only outcome.

## Documentation / doctrine surface

Describe configuration, warning scope, limitations and adopter migration in
the appropriate software documentation and shipped instructions where
affected; route any cross-cutting prescription to `AGENTS.md`, deliberation
to `dev/`, and software description to `docs/`. Do not add a new governing
rule for coordinates.

## Evidence / verification plan

### Tests required

Map affected readers and callers during planning. Extend the existing
`bootstrap/tests/integration/test_link_check_exclusions.py` directive tests,
`bootstrap/tests/integration/test_claim_check_allow_config.py` configuration
checks, and relevant `bootstrap/tests/test_check_cairn_content.py` or owning
tests for internal references and the selected scanner. Exercise actual
checker entry points: migrated listed exceptions remain equivalent; unlisted
broken links and references still report; malformed and overbroad entries do
not suppress; old adopter directives behave as documented. Test positive and
negative ID examples, all three selected surface classes, locations, exceptions,
and unchanged exit behavior. Compare a representative installed and upgraded
adopter tree with its pre-migration behavior. A hidden unrelated finding,
missed selected positive, or warning that changes status falsifies delivery.

### Examples / smoke checks

Run affected iteration tests and prose gates, then the required wide Boundary B
on the reviewed final commit, including real checker entry points and the
adopter workflow. Full certification remains a separate authorized operation.

#### Security preflight

1. **Inputs:** repository documents and configuration may be supplied by the
   same contributor whose text is checked; exemption configuration can suppress
   findings and must be reviewed as such.
2. **Failure evidence:** implementation must mutate an exception's target,
   malformed configuration, and a known positive finding separately and show
   the relevant real entry point detects each; these mutations are not yet run.
3. **Trigger and scope:** the plan must name the actual checker commands,
   selectors, exact path inventory and adopter-facing wording after mapping
   the existing entry points. No new coverage claim is made before that evidence.
4. **Failure direction:** absent or invalid configuration grants no configured
   exemption and produces a diagnostic; it must not silently broaden scope.
   Compatibility parsing must not override invalid configuration to add scope.
5. **Residual:** a contributor who can alter both content and approved
   configuration can seek an unjustified exception; review remains necessary.
   Pattern matching also misses hostile or misleading text without the pattern.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Migration loses a justified exception, hides an unrelated defect, breaks an
adopter upgrade, or warning noise exceeds the value of the references found.
Reconsider the design rather than quietly weakening the check.

## Scope delta

Preserved: both board outcomes and their ordering.

## Assurance path

**Assurance path**: high-assurance. Configuration controls checker exemptions
and migration touches shipped material; heavy review protects those boundaries.

## Review -- Codex GPT-5 (Medium) -- 2026-11-05

Reviewed commit: 686fe791ee9a5b0c7bb9c837e708f756d666b7bc

**Tier**: usual
**Findings**: raised
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the ordered migration and advisory scan preserve both board outcomes while treating exemptions as a risk -- `dev/PLANNING.md` item 9; proposal sections 1-2.
2. **Best alternative.** Keep the current inline markers and omit the warning; it avoids migration cost but leaves both board outcomes unmet -- `scripts/link_check.py` and `scripts/check_cairn.py` directive parsers; `dev/PLANNING.md` item 9.
3. **What would show it wrong?** A real checker entry point suppressing an unlisted broken reference after migration, or an ID warning changing exit status, would invalidate the design -- proposal Tests required.

The configuration contract makes exceptions inspectable without granting a
general bypass; installed and upgraded trees remain part of the comparison.

**Non-blocking:** The security preflight names future mutations but does not
show a run against existing checks, and defers command, selector and input-set
details to planning. The template asks for actual failure evidence and the
trigger at this stage. Run a small existing-check positive/negative probe where
feasible, or identify precisely which evidence cannot exist until design and
implementation, and carry that gap into the plan -- proposal Security preflight;
`dev/proposals/_template.md` S2-S3.

Coverage: compared the committed proposal with board item 9, the proposal
template, the cited August strategy and the named checker parsers/config loader.
The strategy section also covers a separate gauge item; it supports the inline
directive history, not the complete board scope. I did not run mutations,
inspect every installed/upgrade path, or perform the separate Security Review.
