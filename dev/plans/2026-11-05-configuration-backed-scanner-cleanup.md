# Plan: Configuration-backed scanner cleanup

**Source proposal**: [Configuration-backed scanner cleanup](../proposals/archive/2026-11-05-codex-configuration-backed-scanner-cleanup.md), Decision `92954c29`
**Author**: Codex GPT-5 (Medium)
**Status**: revising-code
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

## Strategy reassessment -- Sol (gpt-6.1-sol, High) -- 2026-11-05

**Conclusion.** Reuse the existing module-owned, editable-file installation
mechanism. No new installer algorithm is needed. Adding an installed
suppression file nevertheless changes the delivered file set; this is a
bounded install-contract addition, not permission inferred from the earlier
Decision. This record proposes it only. The current request authorizes
reassessment, not crossing that boundary. No production engine, mapping,
template, manifest, baseline or trust state was changed in this pass.

Basis: accepted proposal Decision and both reviews; this plan's Scope, C1-C3
and both plan reviews; source snapshot
`e923b3dd7bbafd2bdf2e1b639d310ba3a1bb4801`. The installed module's three
paste-at-root examples use a relative link that is intentionally unresolved
from `dev/modules/`. Removing the comment alone loses the promised adopter
behavior; excluding modules or rewriting the examples would lose coverage or
change their paste behavior.

### Options and recommendation

- Retain the comment: no build or recurring cost, preserves current checks,
  but does not finish the accepted file-level cleanup. Doing nothing is not
  completion and requires an explicit scope concession if chosen permanently.
- Deliver one narrow editable JSON seed through the existing mapping: one
  template and one mapping entry, with existing install, lock/base-cache,
  collision and upgrade behavior. Maintainers curate the already-accepted
  exception; there is no new service or command. Estimate one focused work
  window for this addition and its targeted evidence, with upgrade conflicts
  and review turnaround uncertain; this does not estimate all remaining C1-C3.
- Add a special installer merge/writer or built-in checker exception: more
  code and suppression precedence to understand and secure, without a needed
  outcome. Not recommended or authorized.

**Recommendation:** the second option, because it preserves the complete
cleanup and adopter behavior with existing machinery and one explicit owner.

### Precise proposed contract and delegation

Proposed path: `templates/modules/default-on/scanner-check-allow.json`

After explicit Maintainer allowance, add one non-verbatim `InstallSpec` to
`documentation-plan` in `bootstrap/_scaffold/config.py`, from
`templates/modules/default-on/scanner-check-allow.json` to
`dev/.cairn/scanner-check-allow.json`. Non-verbatim means editable text with
the existing raw base cache and three-way upgrade, not forced replacement.
This module owns the destination once; do not add a second owner for
`doc-drift-prevention`. The seed accompanies documentation-plan even when a
profile does not install the optional link checker, so a later checker has
the same exception available.

Seed only the exact `links` pair `dev/modules/documentation-plan.md` ->
`docs/DOCUMENTATION_PLAN.md`, with the original paste-at-root explanation as
its reason, and an empty `internal_refs` list. No Cairn-only source paths,
wildcards or broader defaults enter the adopter seed. Migrate the template
comment and corresponding self-hosted instances into the repository config
using their actual source paths; finish the full live-directive inventory,
including any other installed consumers, before declaring equivalence. Keep
legacy parsing for old adopter content as accepted. Do not resolve this one
blocker by dropping another migration, C2, review or check.

An absent destination installs normally. An existing unlocked destination
must block upgrade unchanged, using the current reconciliation procedure;
never merge arbitrary adopter JSON automatically or force overwrite it.
Tracked customizations use existing text merge/conflict handling. Invalid
merged JSON must still grant no exemptions. Explicit-ref upgrades already
block pending module additions; document running from the target tree rather
than bypassing that guard. Ordinary reinstall retains existing files unless
the operator separately invokes the existing force option.

Risk: an installed configuration can hide a missing target for this exact
source/target pair. The checked-in seed is therefore reviewable suppression
policy. Existing validation must continue rejecting invalid input without
legacy fallback; unrelated targets, anchors and containment checks stay live.
JSON text merges can conflict or become invalid: failure must be visible and
closed to exemptions, never interpreted as permission to broaden them.

Delegate implementation only after allowance. Add permanent cases in existing
link-exclusion and install/upgrade test homes for fresh high-rigor install,
unmodified upgrade, occupied destination, customized tracked config,
reinstall, explicit-ref refusal, malformed/duplicate JSON, changed target,
unlisted missing link, bad anchor and escaping target. Exercise the installed
checker CLI with `--include-modules` as well as an explicit module path.
Check profile ownership and seed contents without importing Cairn-only
exceptions. Map affected checks with `tools/test_tiers.py for`; run its
selection under canonical 3.13, plus required prose gates. Retain the separate
ordinary and Security code reviews and wide final Boundary B. Newly expanded
engine behavior returns for reassessment; no full suite, push or trust
ceremony is authorized here. Existing required integrity checks remain due.

### Measured evidence and limits

In a separate archive of the source snapshot, a temporary synthetic pytest
probe supplied the candidate seed and appended an in-memory mapping, restoring
the template and mapping afterward. No candidate production patch was applied
to this shared tree. Python 3.13.13,
`/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q -p no:cacheprovider
test_scanner_delivery_probe.py`: **1 passed in 2.58 seconds**. It exercised
fresh high-rigor installation, editable lock/base-cache classification,
upgrade stage/apply/finalize, and the installed checker CLI. Separately on
both fresh and upgraded trees, changing the exception target, corrupting the
JSON and adding an unrelated missing link each returned 1; restored config
returned 0. An occupied unlocked config classified `new-module-blocked`,
refused apply and retained its bytes. The existing link-exclusion test file
also passed: **37 passed in 0.19 seconds**, same interpreter and isolated
snapshot, `python -m pytest -q -p no:cacheprovider
bootstrap/tests/integration/test_link_check_exclusions.py`.

Probe location for delegation: `/private/tmp/cairn-scanner-reassess.e0jtko/`;
it is temporary evidence, not a permanent regression test or shipped source.
The probe used runtime mapping injection, not an AST-baseline or install-
manifest update. Not measured: customized tracked JSON upgrade, all profiles,
reinstall, explicit-ref execution, whole-tree `--include-modules`, exhaustive
directive migration, the new ID warning or final integration. Those remain
implementation obligations, not passes. No certification run.

**Authority remaining:** the Maintainer must explicitly allow this one
installed-file/mapping addition within the existing heavy plan. No new plan
or outcome concession is requested. This strategy record clears no review
obligation and makes no Decision. Elapsed: unknown; tokens: unknown.

Record checks, Python 3.13.13: claim, link and snippet checks on this plan,
and `scripts/quality_gate.py --sub neutrality`, passed (neutrality: zero
failures). Claim checking first rejected the proposed nonexistent path,
then a misplaced declaration; the correctly separated typed declaration
passed on the second correction. No checker was weakened. This is a strategy
record, not implementation verification or Boundary B.

## Maintainer scope allowance -- Codex (coordination) -- 2026-11-05

The Maintainer answered **"Allow the settings file (Recommended)"** to the
coordinator's chat question permitting one small editable scanner settings
file, delivered by an existing installation mapping, to preserve installed
documentation checks while removing embedded exception comments.

This explicitly allows the second option in the preceding Sol reassessment:
one narrow seed and one non-verbatim `documentation-plan` mapping, using the
existing collision, lock/base-cache and text-upgrade behavior. Its precise
source, destination, seed pair, compatibility and refusal contract remain as
specified there. No new installer algorithm, broader exemption, lost cleanup
scope, trust operation or waiver of checks/reviews is authorized. C1-C3 remain
implementation work. Elapsed: unknown; tokens: unknown.

## Implementation progress -- Codex GPT-6 Luna (Low) -- 2026-11-05

C1 implementation is committed in `1790fb2d`, `edf9b96d` and `32b89220`.
The active scanner set is `templates/**`; a full live-file scan found no
remaining file-level `link-check-allow:` or `cairn-internal-ref-allow:`
directive there. The documentation-plan link is represented for both its
template and Cairn-installed source paths in the repository settings; the
adopter seed contains only `dev/modules/documentation-plan.md` to
`docs/DOCUMENTATION_PLAN.md`, with its paste-at-root reason. Three existing
directory-token annotations remain inline in `templates/README.md`,
`templates/codebase-readiness-report.md` and `templates/core/AGENTS.md`:
they describe namespace/citation behavior, target directories rather than
files, and keep their exact prior narrow scope. A template inline annotation
also remains unchanged. File-level markers outside the checker’s template
set are inert for this reader; the archived proposal marker is historical and
untouched.

The existing mapping delivers one editable settings seed. Valid settings use
exact source/target matching; malformed or duplicate-key JSON grants no
configured or legacy exemptions and reports a diagnostic. Old adopter
comments retain their prior parsing and precedence when settings are valid or
missing. The existing tests cover duplicate keys, wrong types, broad entries,
changed target, unlisted missing links, bad anchors, escaping targets, invalid
JSON, reinstall preservation, missing-seed upgrade, occupied destination,
customized tracked seed and explicit-ref refusal.

On a clean Git-backed copy at `32b89220`, Python 3.13.13: link-exclusion and
internal-reference tests passed (45); `test_check_cairn_content.py` passed
(9); `test_reference_scripts.py` passed (34); the generic upgrade collision
and explicit-ref controls passed (2). The real link checker passed on 223
Markdown files; `check_cairn.py --no-content-scan` passed on 205 files with
four expected unused-entry advisories. The latter checks were rerun after the
documentation self-check fix in `edf9b96d`. An earlier self-check failure was
fixed in that commit. The focused runs do not replace the mapped iteration.

The exact mapped-selection command over the three C1 commits is:

```sh
{ for commit in 1790fb2d edf9b96d 32b89220; do
    git show --format= --name-only --no-renames "$commit"
  done; } | sort -u | xargs python tools/test_tiers.py for \
    --range e71ca18b..32b89220
```
It selects 93 test files and reports 11 further AGENTS.md readers omitted by
its guard: `test_comprehension_floor.py`, `test_stewardship_rules_ship.py`,
`test_fork_advisory.py`, `test_generated_output_scan.py`,
`test_module_merge.py`, `test_notice_install.py`, `test_oracle.py`,
`test_quality_gate_neutrality.py`, `test_security_leaf.py`,
`test_slotmerge_leaf.py` and `test_test_tiers.py`. The selection has not run;
root coordination is pending for a batch window.
Accordingly C1 verification remains open, as do C2, both independent code
reviews and final wide Boundary B. No suite, Security Review, trust ceremony
or release operation was run. Elapsed and tokens: unknown.

## Implementation progress -- Codex GPT-6 Luna (Low) -- 2026-11-05

The joined mapped C1 iteration found one missed self-hosted copy: the shipped
model-selection template had its file-level reference migrated, while
`dev/modules/model-selection.md` retained the inert marker. The existing
contract node `test_model_tier_rule_ships.py::test_proposal_authoring_and_ordinary_review_are_medium`
requires exact equality between these copies. Commit `c8143ee2` removes that
marker; the exact template source/target allowance remains in the repository
settings, and the module prose is unchanged. A clean Git clone at `c8143ee2`,
Python 3.13.13, ran that node: 1 passed in 0.03 seconds. The mapped joined
selection continues in root-coordinated batches on its earlier candidate; its
remaining results and the correction’s inclusion in final mapped verification
are pending. C1 and C2 remain open. Elapsed and tokens: unknown.

## Implementation progress -- Codex GPT-6 Luna (Low) -- 2026-11-06

The joined iteration exposed two more existing equality contracts whose
self-hosted copies retained migrated file-level markers. Commit `2a704f74`
removed the marker from `.agents/skills/session-start/SKILL.md`; commit
`0922e0e7` removed it from `dev/modules/security-verification.md`. Their
shipped sources already carry the exact migrated configuration entries. Both
copies now match their shipped templates byte-for-byte, without changing
operative skill or module text. The existing security-verification test also
pins the module twin and its tamper-evident designation.

On a clean Git clone at `0922e0e7`, Python 3.13.13 ran the six owning equality
nodes across model-selection, session-start and security-verification:
6 passed in 0.40 seconds. C1's joined mapped selection still has ten
unclassified upgrade edit-check failures; the two missing-anchor clone
failures were separately rerun and passed. Root is obtaining Sol's disposition
before C1 closes. No C2 edit has started. Elapsed and tokens: unknown.

## Implementation verification -- Codex GPT-6 Luna (Low) -- 2026-11-06 -- C1 disposition

The joined mapped iteration is dispositioned. On frozen clean clone
`/private/tmp/cairn-v07-c1-73aaf88d`, commit
`73aaf88df9000c6d5f850384c9d058cd9e7eb8ab`, canonical Python 3.13.13, the
coordinator selected 104 test files from 41 changed paths (29 scanner C1, nine
strict-runner and three continuation paths), in three serial batches of
35/35/34. Across the batches: 5,664 passed, nine skipped, and 18 initially
failed; pytest time 1,519.35 seconds, wall time 1,522.087 seconds. Eight skips
were Windows junction cases and one required a Windows drive; ten AGENTS-only
readers were omitted by the selector guard, not passed. These are coordinator-
reported results; the scanner implementer did not run the joined selection.

All 18 initial failures then passed narrow checks, without rerunning the joined
selection: six self-hosted-copy equality nodes passed at `0922e0e7` (Python
3.13.13, 0.40 seconds); two missing-anchor clone cases passed after importing
the exact local anchor; and the 12 injected edit-check fault parameters plus
their positive control passed at `23ded78f` with shuffle seeds zero and one
(13 passed in 13.15 seconds; 13 passed in 15.65 seconds). The edit-check
fixture's early timeout was repaired in `72194fea` and `23ded78f`; its focused
verification is recorded in the suite-consolidation plan. Together with the
15-file session-end copy promotion check at `41b6a3b5` (1,073 passed in 50.71
seconds), this closes C1's mapped functional-check obligation.

This supersedes the earlier implementation-progress notes that marked the
mapped run pending. It is iteration evidence, not C3 code review, final wide
Boundary B or tree certification. Both independent scanner code reviews and
final wide Boundary B remain due after C2. No release or trust operation was
run. Elapsed and tokens: coordinator batch times above; implementer tokens
unknown.

## Implementation progress -- Codex GPT-6 Luna (Low) -- 2026-11-06 -- C2

C2 is implemented at `ed7b5778`; the exact-context correction and C1 mapping
count follow-through are at `0a756bba`. The existing `check_cairn.py` prints
warning-only references on tracked Markdown in `docs/`, `templates/modules/`
and `CHANGELOG.md`, plus Python files in `templates/modules/`. Python inputs
are kept out of the Markdown link, claim and content gates. Recognized tokens
are bounded `R/F/N` IDs with one or two digits (optional `.rN`), and observed
`CR`/`SR` forms, inside square brackets or parentheses, or after `finding` or
`review`. Bare gate, method, lint and Roman identifiers remain unrecognized.
The scan is lexical and documents these limits.

The measured final inventory at `0a756bba` contains 100 files (70 Markdown,
30 Python) and 25 recognized occurrences. Twenty-five optional
`review_ids` entries each name an exact source, ID, literal context and reason;
zero warnings remain. They cover the plan/proposal teaching examples, one
historical changelog mention, explicit methodology examples, and three
historical criterion labels in the hash-pinned security runner. The runner
bytes and the documentation-plan install seed were not changed by C2. Missing
`review_ids` remains compatible; malformed or duplicate entries invalidate
the shared configuration. Tests exercise the mixed `(Imp #5 / SR-5)` form,
negative bare IDs including `(II3)` and `(F401)`, status preservation, a stray
same-source occurrence beyond an exact exception, and old and invalid config.

On clean clone `ed7b5778ec1b6046249526958ce03dc3113c5db2`, Python 3.13.13, the
mapped 14-file selection below ran 1,026 passed and one failed in 52.92
seconds. The sole failure was the installer manifest row pin: the accepted C1
settings-seed mapping makes the expected count 90. Commit `0a756bba` updates
that count and asserts the exact non-verbatim seed tuple. On clean clone
`0a756bbacaf38398a0d6914ae2d9ba5a074a1836`, Python 3.13.13 reran
`test_check_cairn_content.py` and the failed manifest-count node: 12 passed in
0.12 seconds. The all-Markdown `check_cairn.py` entry point then exited 0 on
203 files, with no review-ID warnings and four previously recorded unused C1
entries. The full 14-file selection was not rerun after the fix; it remains
owed once on the reviewed final range in Boundary B.

The first C2 focused run on clean `ed7b5778` passed 56 tests in 0.46 seconds,
including config compatibility/refusal, warning controls and the
documentation-plan verbatim install node. On that same commit, `link_check.py`
passed on 203 Markdown files; snippet sync passed on 570 documents; neutrality
reported zero failures and 43 informational findings; claim checks for both
changed documentation files passed. These do not replace the mapped
selection. No certification, Security Review, release or trust operation was
run.

The exact 14-file C2 mapped selection from `python tools/test_tiers.py for`:
`test_check_cairn_counts.py`, `test_deleted_tracked_markdown.py`,
`test_link_check_exclusions.py`, `test_check_cairn_content.py`,
`test_content_scan.py`, `test_doc_drift_tools.py`, `test_gate_manifest.py`,
`test_loop_fidelity_gate.py`, `test_notice_install.py`,
`test_practice_modules.py`, `test_reference_scripts.py`,
`test_review_stance_in_shipped_files.py`, `test_security_check.py` and
`test_security_lint.py`. The initial failure and its scoped correction are
both reported; no pass is inferred for the remaining tests after the fix. C3
ordinary and Security code reviews and final wide Boundary B remain due.
Elapsed time for authoring: unknown; tokens: unknown.

## Code review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

Reviewed source: `0a756bba`, plan and evidence: `16f6d7cf`; baseline
`9184c3ed`. **Verdict: REVISE.** Elapsed: approximately 2 minutes; tokens:
unknown.

**Foundations**

1. **Should this happen as framed?** Yes, once the refusal defect below is fixed: the exact configured targets and preserved legacy file-wide/prefix parsing support C1, while the separate advisory scan supports C2. Evidence: `scanner_targets`, `_check_dangling_internal_refs`, and `_review_id_warnings`.
2. **Best alternative.** Retaining inline directives avoids maintaining settings and 25 literal warning exceptions, but loses the accepted cleanup; the exceptions preserve teaching and historical contexts at a continuing curation cost. Evidence: seed mapping, root settings and C2 inventory above.
3. **What would show it wrong?** A real entry point hiding an unlisted broken link or accepting a malformed setting, or a same-file stray ID being silenced, falsifies the contract. Repeat those probes after the fix and include the final wide Boundary B.

**Blocking -- Wrong-type `review_ids` can leave exemptions active.**
`load_scanner_config` iterates `review_ids` without requiring an array;
empty object and empty string therefore pass validation. On an isolated copy
of `0a756bba`, the real `link_check.py --root` entry point returned 0 with
no diagnostic for each shape while a configured `source.md -> absent.md`
exemption hid a broken link. The same probe with `null` returned 1 and
reported the link. C1 requires wrong types to invalidate the whole config and
grant no exemptions. Require an array when present in both checker copies;
add entry-point regression cases for empty object and string with a live
exemption, and confirm invalid settings also disable legacy exemptions.

Coverage: read the accepted proposal, plan reviews and implementation records,
scanner and configuration changes, seed mapping and owning tests, including
legacy parsing, exception context, selected warning surfaces and upgrade
controls. The focused probe above used the isolated committed copy and the
available Python; no suite was run. I did not independently repeat installer
workflows, every migration or mutation, or final integration; separate Security
Review and wide Boundary B remain due. Over the word target to make the
fail-closed reproduction and closure precise.

## Response -- Codex GPT-6 Luna (Low) -- 2026-11-06 (ordinary code review)

**Disposition: accepted and addressed.** Commit `49abc575` requires the
optional `review_ids` value, when present, to be a JSON array in both
byte-identical checker copies. Missing settings remain compatible with an
empty default; a present empty array remains valid. Every explicit non-array
now invalidates the whole configuration, so neither configured link or
internal-reference exemptions nor legacy comment allowances remain active.

Added real-entry regressions for `{}`, `""`, `null`, integer, boolean and
float values. The fixture first proves a valid config exempts a configured
broken link and a Cairn-internal reference, then proves each malformed value
invalidates settings and reports both despite the configured entries and
legacy comments. Existing missing-namespace and list-valued parser controls
remain in place.

The first focused run exposed an independent claim-path failure because the
fixture cited a nonexistent `docs/methodology/roles.md`. Commit `764007ad`
adds only that fixture file, leaving the assertion unchanged. On a clean clone
at `764007ad7a2dae3b9e649979063482d9e624c668`, Python 3.13.13 ran the
optional/malformed config cases, valid and invalid entry-point controls, and
the documentation-plan twin-install node: 10 passed, 41 deselected, in 0.31
seconds. The first run's six fixture failures are retained as setup evidence;
the focused rerun after the fixture correction passed. This does not rerun the
14-file mapped selection. Return to the same ordinary reviewer for a targeted
look; separate Security Review and final wide Boundary B remain due. Elapsed
and tokens: unknown.
