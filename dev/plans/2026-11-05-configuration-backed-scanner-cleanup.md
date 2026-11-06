# Plan: Configuration-backed scanner cleanup

**Source proposal**: [Configuration-backed scanner cleanup](../proposals/archive/2026-11-05-codex-configuration-backed-scanner-cleanup.md), Decision `92954c29`
**Author**: Codex GPT-5 (Medium)
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Move file-level scanner exceptions into validated configuration and warn about temporary review IDs in published material.

## Source proposal

The Maintainer accepted both outcomes in order, with legacy compatibility,
warning-only behavior and the proposal's verification obligations. Heavy
assurance applies; no new scanner service or release blocker is authorized.

## Scope

Deliver the configuration, migration and advisory scan together so published
text is cleaner without hiding unrelated defects or breaking adopter checks.
Inventory actual directive instances, readers, selections, installed copies,
release inputs and upgrade behavior before choosing configuration placement.
Preserve non-file-level annotations and avoid incidental install-contract or
trust-root changes; stop for reassessment if a boundary change is needed.

**Reuse.** Searches for `link_allow`, internal references and configuration in
`scripts/`, `templates/` and `bootstrap/_scaffold/` found the existing link
checker and its shipped copy, the `check_cairn.py` internal-reference check,
and the claim-check configuration pattern. The latter is a separate namespace,
not a validator to copy unchanged. `bootstrap/security_check.py` invokes the
repository checker; installer mappings place the shipped link and claim
checkers in adopter `scripts/`. Confirm their consumers and upgrade treatment
against the current tree before editing. Use existing checker and test homes;
add no standalone service or ledger.

### Documentation / doctrine surface

Describe the actual contract, diagnostics, warning limits and adopter migration
in existing software documentation and shipped instructions as needed. No new
cross-cutting doctrine or coordinate rule is planned. Update synced snippets
at their source if affected.

## Sequence

Available scanners, installer and integration tests provide the starting point;
no unfinished plan is a prerequisite. Estimate one to two focused workdays
including reviews and checks, with uncertainty in upgrade behavior, live
exception inventory and review turnaround; this is not a deadline.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inventory readers, paths, directives and adopter behavior; define and implement validated configuration and migrate live exceptions. | Both required plan reviews folded; reassess any newly discovered boundary. | Equivalent checking, compatibility and migration documentation. |
| C2 | Define and implement the finding-ID warning using an existing scanner; resolve existing hits and record justified exceptions. | C1 complete. | Advisory warning on the selected published surfaces. |
| C3 | Independent ordinary and Security code reviews, fixes and wide final verification. | C1 and C2 committed with iteration evidence. | Reviewed, verified work ready to archive. |

Routine human release or baseline operations are separate from plan completion;
archive does not authorize release. Any specifically required human operation
is tracked as a separate named board wait with owner and evidence at the
appropriate serialization point, and remains unpassed until performed.
Unexpected integrity failures and missing checks remain implementation work.

## Acceptance criteria

**C1.** Document exact source and target scope, required reasons, validation,
diagnostics and treatment of missing, unreadable, malformed, duplicate, broad,
stale and unused entries. Invalid configuration grants no configured exemptions
and cannot be used with compatibility parsing to add scope. Preserve each
check's matching, coverage and reports, and migrate every live file-level
directive and its reason without expanding its effect. Preserve old adopter
directives with documented precedence and migration. In particular, legacy
internal-reference parsing collects both marker forms file-wide, uses prefix
matching even for filename-shaped entries and accepts empty reasons: do not
silently tighten legacy behavior. New configuration must reject duplicate keys
and wrong types rather than inherit claim loader key overwrites or string
coercion. Preserve inline reference annotations.

**C2.** Derive the ID pattern, examples, selected paths and explicit historical
discussion exclusions from real review records and release inputs; document
them. Scan shipped modules, docs and release notes. Report actionable warnings
with locations, leaving exit status and other findings unchanged. Reuse the
validated configuration for justified, narrowly scoped exceptions, not general
suppression. Review existing hits and record their resolution or justification.

**C3.** Complete separate ordinary and Security code reviews by eligible
independent reviewers, address findings under the lifecycle rules, and pass
the required checks and wide Boundary B on the reviewed final commit. The
reviewed range includes all fixes; known unmet checks prevent archive.

## Scope delta

**Scope delta**: preserved. Both accepted outcomes and all verification remain
in this plan.

## Verification

**Boundary A.** Before edits map changed behavior through readers, callers,
configuration, installer, upgrade and release entry points; record owning
tests and consumers. Run `python tools/test_tiers.py for <paths>` for changed
files and its iteration selection, plus applicable claim, link, snippet and
neutrality prose gates. Extend the existing link exclusion and claim config
integration tests and the internal-reference/selected-scanner owning tests for
plausible uncovered faults. Record commands, outcomes, elapsed time and token
use or `unknown`.

Use real checker entry points to compare listed migrated exceptions and
unlisted broken links and references, including bad anchors, escaping targets,
duplicate keys, wrong types, prefix/sibling and wrapped-inline cases. Exercise
missing and invalid configuration, broad and unused entries, legacy directives
and precedence. Separately mutate an exception target, malformed configuration
and a known positive ID and show each is detected. Test ID positives and
negatives across all three surface classes, location, exceptions, unchanged
exit status and preservation of other findings. Compare a representative
installed and upgraded adopter tree with its pre-migration behavior. Record
the exact selection and triggering commands and reconcile them with the
adopter-facing wording. Sol's proposal baseline probes used Python 3.12.9;
they are not final verification.

**Boundary C.** After implementation, independent ordinary and Security code
reviewers read the committed work and iteration evidence and run tight
falsifying checks, not a suite. They name gaps and mutations not measured;
review fixes receive a targeted return look when required.

**Boundary B.** After reviews, run the wide selection on a clean, unchanged
final commit under canonical Python 3.13.x: the iteration list for the entire
reviewed range, mapped integration and workflow tests, standing gates and the
plan-specific real-entry-point and adopter checks above. Record full SHA and
range, interpreter, clean pre/post state, commands, counts, elapsed time,
tokens, non-pass dispositions, timing misses and omissions in the dated
implementation verification record. Full tree certification is separate and
is not authorized by this plan.

## Plan review -- Codex GPT-5 (Medium) -- 2026-11-05

Reviewed commit: b5a93048582be9510bd463181e2fbfcbac74d412

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the plan retains both accepted outcomes, their order, compatibility, warning-only behavior and required verification -- Acceptance criteria; source proposal Decision.
2. **Best alternative.** Reuse existing scanners and configuration as planned; a separate service adds maintenance without delivering a missing outcome -- Scope; source proposal Alternatives considered.
3. **What would show it wrong?** A real checker suppressing an unlisted defect, or an ID warning changing exit status, would falsify delivery -- Verification, Boundary A.

Coverage: compared the committed plan with the accepted proposal, AGENTS.md
and the committed plan template. Did not run implementation tests, inspect
every scanner or installer path, or perform the separate Security Review.

## Plan review -- Sol (High) -- 2026-11-05

Reviewed commit: 2ee80c60555e85aae4634333b36f7d847b0c2d98

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 5 minutes (estimated)
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: C1-C3 retain the accepted migration, compatibility and advisory outcomes without authorizing an incidental trust-root change -- archived source proposal Decision; Scope; Acceptance criteria.
2. **Best alternative.** Reuse the existing checker entry points with a narrowly validated configuration contract, as planned; a separate service adds an interface without improving these outcomes, while retaining directives loses the accepted cleanup -- Scope, Reuse; source proposal Alternatives considered.
3. **What would show it wrong?** Run migrated and legacy inputs through the real entry points with malformed configuration, an unlisted sibling, a bad anchor and an escaping target; a newly hidden finding or changed warning exit status falsifies delivery -- Verification, Boundary A; source proposal Tests required.

No blocking security finding. Contributor-controlled configuration remains a
suppression surface requiring review, not a safety proof. C1 rejects duplicate
keys and wrong types, grants no configured exemptions on invalid input, and
forbids compatibility parsing from adding scope in that case. It preserves
legacy file-wide, prefix and empty-reason behavior rather than copying it into
new configuration. These distinctions match the committed internal-reference
parser and claim loader; the link checker only exempts missing targets, leaving
anchor and containment protections important to the promised comparison.

The implementation inventory must still settle configuration placement,
precedence, exact warning selection and upgrade treatment before editing.
Boundary A requires those decisions, separate mutations and installed/upgraded
comparisons; C3 and wide Boundary B keep missing evidence open. The existing
release wrapper invokes the real repository checker, so helper-only tests
would not discharge the named entry-point obligations.

Coverage: compared the committed plan, accepted archived proposal, AGENTS.md,
plan template and review sweep; inspected committed checker parsers, claim
loader and release invocation, and located installer mappings. Not covered:
exhaustive directive inventory, implemented configuration or warning behavior,
upgrade execution, mutations or tests. No suite run. Model attribution is the
coordinator's explicit Sol assignment in this review request.
Over target to retain compatibility distinctions and entry-point coverage limits.
