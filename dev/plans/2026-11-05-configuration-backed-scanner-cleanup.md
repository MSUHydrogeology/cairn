# Plan: Configuration-backed scanner cleanup

**Source proposal**: [Configuration-backed scanner cleanup](../proposals/archive/2026-11-05-codex-configuration-backed-scanner-cleanup.md), Decision `92954c29`
**Author**: Codex GPT-5 (Medium)
**Status**: awaiting-plan-review
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
