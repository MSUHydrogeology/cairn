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

## Implementation progress -- Codex GPT-6.1 Terra (Low) -- 2026-11-05

C1 is incomplete. Added an unwired, standard-library configuration reader to
the byte-identical repository and shipped link checkers, with focused parser
tests. It does not yet affect exemptions, legacy parsing, scanner output or
adopter installs. No config is installed by this change.
The config path is `dev/.cairn/scanner-check-allow.json`.

Mapping: `check_cairn.py` imports the shipped link checker; `security_check.py`
invokes that entry point. The doc-drift module installs the checker verbatim;
upgrade classifies its installed copy as verbatim. Relevant owners include
`test_link_check_exclusions.py`, `test_doc_drift_tools.py`,
`test_reference_scripts.py`, `test_check_cairn_content.py` and
`test_claim_check_allow_config.py`. Full migration still needs the installer
and upgraded-adopter comparison, real-entry-point cases, warning work and
all plan verification. In particular, removing a shipped directive requires
proving equivalent installed behavior without an incidental install-contract
change.

Iteration: Python 3.12.9, `python -m pytest -q -p no:cacheprovider
bootstrap/tests/integration/test_link_check_exclusions.py`: 33 passed in
0.09 seconds. Canonical Python 3.13 verification has not yet run.
Elapsed: unknown; tokens: unknown.

At commit `e71ca18b`, the seven-file `test_tiers.py for` selection for this
component ran in a separate clone under Python 3.12.9: 261 passed and three
`test_security_check.py` tests skipped because Bandit was not installed, in
41.33 seconds. A repeat with `-rs --durations=0` gave the same counts in
39.64 seconds. The 30-second iteration target was missed;
`test_gate_manifest.py` accounted for 25.16 seconds on the repeat and is
reported to the coordinator for the consolidation list. The skipped checks,
canonical interpreter and remaining plan-specific checks remain open.

Coordination: active claims overlap the live directives in
`templates/modules/team-gated/legacy-agent.md`, `model-selection.md` and
`security-review.md`. Those files remain untouched; their migration and C1
completion await coordination. C2 remains behind the C1 gate.

## Implementation progress -- Codex GPT-6.1 Terra (Low) -- 2026-11-05

Wired the existing configuration reader into both link-check entry points and
the internal-reference gate. Missing or valid configuration retains legacy
directives; valid configured entries match an exact source and target; invalid
configuration disables configured and legacy exemptions and reports a
diagnostic. No directives were migrated. C1 remains open: configuration
inventory and migration, stale/unused diagnostics, adopter instructions and
install/upgrade comparisons, plan mutations and complete verification remain
due. C2 and independent reviews remain behind C1. The three claimed template
files above remain untouched. Elapsed and tokens: unknown.

Iteration at `8a44578a` on an isolated clone, Python 3.13.13
(`/Users/kendal30/conda_envs/lhm/bin/python3.13`): the 13 files selected by
`tools/test_tiers.py for` for this commit's six changed paths ran with
`python -m pytest -q -p no:cacheprovider -rs --durations=20`: 509 passed,
three dependency deprecation warnings, no skips, 59.42 seconds. The selection
was `test_check_cairn_counts.py`, `test_deleted_tracked_markdown.py`,
`test_link_check_exclusions.py`, `test_check_cairn_content.py`,
`test_content_scan.py`, `test_doc_drift_tools.py`, `test_gate_manifest.py`,
`test_loop_fidelity_gate.py`, `test_notice_install.py`,
`test_practice_modules.py`, `test_reference_scripts.py`,
`test_security_check.py` and `test_security_lint.py` in their existing test
homes. Claim, link, snippet and neutrality gates passed on the plan; the link
checker reported the expected missing configuration. The 30-second target
was missed. `test_gate_manifest.py` took at least 24.32 seconds from its four
longest reported tests; a separate `test_security_check.py` run passed 114
tests in 21.50 seconds. Both are reported to the coordinator for the
consolidation list, in that order. This is not Boundary B or a review.

## Implementation progress -- Codex GPT-6.1 Terra (Low) -- 2026-11-05

Added advisory stale-source and unused-entry diagnostics and adopter link
exception documentation. Unused entries are assessed only for scanned source
files; a missing source is reported even when not selected. Migrated the
high-rigor onboarding file's citation and original reason into config; the
directive is outside the installer-extracted seed blocks. C1 remains open.
The documentation-plan link directive also appears in an installed module:
removing it without delivering an adopter-side exception would break an
explicit `--include-modules` check. Its migration needs a demonstrated
equivalent that does not change the installer contract, or reassessment.
An isolated high-rigor install returned 0 with the installed directive, then
returned 1 for `docs/DOCUMENTATION_PLAN.md` after removing only that comment;
the entry-point mutation is retained in `test_link_check_exclusions.py`.
Other migration, install and upgrade comparisons, required checks and C2
remain open. Elapsed and tokens: unknown.

Iteration on isolated commit `cda1f37c`, Python 3.13.13: the 15-file
`test_tiers.py for` selection for that commit's changed paths ran with
`python -m pytest -q -p no:cacheprovider -rs --durations=20`: 1,073 passed,
no skips and three dependency deprecation warnings in 64.37 seconds. The
selection contains the 13 files named in the previous iteration plus
`test_model_selection_stub.py` and `test_review_stance_in_shipped_files.py`.
Claim, link, snippet and neutrality prose gates passed. The 30-second target
was missed; `test_gate_manifest.py` took at least 24.43 seconds from its four
longest reported tests, and `test_security_check.py` remains on the
consolidation report from the preceding run. The seed extractor produced the
same 11 blocks at `1aa4df86` and `cda1f37c`. This is not Boundary B or review.
The coordinator reported the prior template claims released; they no longer
prevent migration. The installed documentation-module behavior above remains
the unresolved boundary and stops C1 pending an equivalent within the plan
or Maintainer reassessment.
