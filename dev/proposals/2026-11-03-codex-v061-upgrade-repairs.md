# Repair v0.6 adopter upgrades in v0.6.1

**Author**: Codex (inherited runtime model; identifier unavailable)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy -- integrity policy, scaffold engine and shipped files
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-03
**In brief**: Let projects edit their changelogs normally, repair Windows upgrade failures and replace stale governing-section citations in a small v0.6.1 patch.

## Decision summary

Fix the three new adopter reports together, before v0.7 implementation.
Treat the root changelog as project-owned history, not protected Cairn code;
ordinary release-note edits should not require another lockfile update.
Preserve upgrade collision review and protection of executable and governing
files. Repair Windows path comparisons and console output, and stale citations.
Use existing upgrade, test and release procedures; add no command or service.

## Context

At `c3b9a1c1`, the starting commit of `0.61-dev`, independent probes under
Python 3.13.13 reproduced these reports:

- [#43](https://github.com/MSUHydrogeology/cairn/issues/43): adopting existing
  changelog history, staging and applying preserves it; integrity returns 0.
  An ordinary changelog edit then returns 1 with a hash mismatch.
- [#44](https://github.com/MSUHydrogeology/cairn/issues/44): seven staged
  nested paths rendered as Windows paths cause apply to refuse its manifest;
  the same POSIX stage applies. A CP1252 output stream separately raises
  `UnicodeEncodeError` on the report's warning symbol. These are simulations,
  not Windows-host evidence. Staged text I/O already explicitly uses UTF-8.
- [#45](https://github.com/MSUHydrogeology/cairn/issues/45): the session tool,
  stem checker, plan template and rules README cite absent governing headings.
  Existing headings supply positive controls for the lookup.

Closed reports remain regression inputs; larger open feature requests stay
on their existing tracks.

## Proposal

1. **Changelog ownership.** Add exactly `CHANGELOG.md` to the existing
   authoritative living-state destination set: tracked for upgrade, exempt
   from content-hash comparison. New installs, unchanged carried records,
   upgrade-added records and collision-adopted records acquire the flag during
   their normal operation. Scoped finalization also migrates old records.
   No recurring release-time re-pinning. Preserve history,
   merge ancestors and collision authorization. Do not expand the exemption
   to scripts, governing files or arbitrary lockfile assertions. Changelog
   bytes remain Git-reviewed, not integrity-attested; document that tradeoff.
2. **Windows compatibility.** Render filesystem-derived relative names with
   forward slashes before comparing them to canonical manifest names, including
   the discovery-update lookup. Do not reinterpret untrusted manifest names
   or weaken traversal/link refusals. Replace the fixed unencodable warning
   symbol with an ASCII label. Report filenames unencodable on the output
   stream as escapes, without changing actual paths. Test labels, filename
   display and UTF-8 file-content preservation separately; no global encoding
   override.
3. **Current citations.** Repoint stale section references throughout the
   shipped sources and their self-hosted twins to actual current sections or
   published methodology. Do not recreate removed rules merely to satisfy a
   reference. Check the shipped citation inventory in an existing
   documentation-test home; a broken-reference control must fail. No new
   release command.
4. **Patch preparation.** Prepare version metadata and a distinct v0.6.1
   changelog section without relabeling v0.7 deliberation entries as delivered
   features or altering released v0.6.0 history. Rehearse real v0.6.0-to-patch
   installs/upgrades on disposable projects, retaining local history/edits.
   Use the existing release process. The Maintainer alone performs required
   baseline/anchor corrections, signing, tag and publication steps.

## Rationale

One batch shares upgrade fixtures and release work without new options or
routine steps. The cost is a narrower integrity claim for history and targeted
regression tests. No upgrade-engine redesign or v0.7 implementation.

## Alternatives considered

Keeping the present behavior needs no code but imposes scoped finalization
after every changelog edit and retains both other upgrade defects. Removing
the changelog from Cairn tracking avoids hash checks but also loses its upgrade
history and collision/merge handling. Recommend the existing living-state
mechanism instead. A wholesale path rewrite costs more and risks weakening
safe-name checks; normalize only filesystem-derived comparisons.

## Documentation / doctrine surface

Update `bootstrap/UPGRADE.md`, the changelog template and affected section
citations, with self-hosted copies kept aligned. Repair references, not review
or verification policy. Roadmap and release metadata describe patch status.

## Evidence / verification plan

### Tests required

Extend existing living-state and changelog-upgrade cases in
`bootstrap/tests/test_upgrade.py` and
`bootstrap/tests/test_upgrade_module_additions.py`: new, adopted and old
records (independently constructed without the new flag); edit after upgrade;
script-edit and illegal-exemption refusals;
history preservation and repeat upgrade. Exercise real stage/apply for Windows
relative rendering, non-ASCII files, CP1252 reports and changed/extra staged
paths. Separately refuse backslash/traversal metadata and POSIX literal-backslash
stage entries while accepting genuine Windows nested paths. Add citation controls.
Map affected tests with the existing tier tool. Native Windows evidence is
owed before claiming the Windows bug closed. Record platform gaps honestly.

### Examples / smoke checks

Run existing prose/neutrality gates, fidelity/twin checks and a fresh install
plus prior-release upgrade. Wide Boundary B and required trust checks precede
release; full certification occurs at its existing release trigger, not per fix.

#### Security preflight

S1: templates are upstream inputs; project files and lock/stage records are
untrusted inputs. Exemption authority remains the source-owned exact path set.
S2: the unchanged-source probes fail as described above. Required regression
controls also alter a script, forge its exemption and corrupt a staged set;
these implementation controls have not yet run.
S3: existing install and integrity CLIs, and upgrade's stage/apply/adopt/finalize
paths govern output; the plan binds commands to the cases above.
Intended adopter wording: "Changelog content is project-owned living state;
executable and governing Cairn files retain integrity checks."
S4: normalize filesystem display only; unsafe names and stage mismatches
remain refusals. A missing migration must fail the changelog regression.
S5: someone who edits project history can change its meaning undetected by
integrity checking. Git review remains the history-review channel; this does
not authenticate changelog content or contain hostile code on the host.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Routine history still fails integrity; history is overwritten; another file
can claim the exemption; corrupt stages apply; or Windows compatibility
requires relaxing path containment. Any one prevents release readiness.

## Scope delta

Preserved: the three reported upgrade repairs and patch preparation.

## Assurance path

**Assurance path**: high-assurance.

**Elapsed**: approximately 12 minutes including orientation and issue triage.
**Tokens**: unknown.

## Review -- Codex (inherited runtime; exact model identifier unavailable) -- 2026-11-03

**Foundations**

1. **Should this happen as framed?** Yes: one patch repairs adopter friction without new machinery; exact-path exemptions and stage-set refusals already exist -- `bootstrap/_scaffold/lockfile.py:83`, `bootstrap/_scaffold/upgrade.py:3500`.
2. **Best alternative.** Repeated scoped finalization avoids changing exemption policy but adds work after every history edit and leaves Windows failures; removing tracking loses merge/collision protection -- `bootstrap/_scaffold/upgrade.py:2723`, `bootstrap/UPGRADE.md:532`.
3. **What would show it wrong?** Lost history, accepted corrupt stages, or exempted apparatus would defeat the patch; existing collision, corrupt-stage and illegal-exemption tests exercise those promises -- `bootstrap/tests/test_upgrade.py:2313`, `bootstrap/tests/test_upgrade_module_additions.py:792`.

```
Reviewed commit: 0f15b2791d15082bbe2889affdb9834c648ef24f
Target: whole proposal and current executable upgrade/integrity contracts
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: ACCEPT
**Elapsed**: approximately 5 minutes
**Tokens**: unknown

The batch preserves project history while retaining apparatus checks and
Maintainer-only trust/release fences.

**R1 -- non-blocking.** Make the migration branches explicit in the plan.
Apply carries old records unchanged, while new-entry creation and collision
adoption also omit the flag; set membership alone is insufficient
(`bootstrap/_scaffold/upgrade.py:1880`, `bootstrap/_scaffold/upgrade.py:3753`).
A scratch entry-point probe confirmed old records remain unflagged after
stage/apply, then migrate through scoped finalization. Close with branch-specific
criteria/tests and exact commands/input sets in S3; no new mechanism is needed.

**Covered:** committed code, citation sources and release procedure; Python
3.13.5: 12 targeted tests passed (3.44s), four scratch probes passed (1.44s),
reproducing changelog-edit, Windows-rendering and CP1252 failures with controls.
One probe-fixture error was corrected.
**Not covered:** native Windows, real prior-tag rehearsal, implementation,
full certification, release ceremonies or the separate Security Review obligation.

## Security Review -- Codex (inherited runtime; exact model identifier unavailable) -- 2026-11-03

**Foundations**

1. **Should this happen as framed?** Yes: exempt project history, not apparatus; `verify()` independently enforces the source-owned set -- `bootstrap/verify_integrity.py:450`.
2. **Best alternative.** Scoped finalization retains policy but requires recurring history-edit work -- `bootstrap/_scaffold/upgrade.py:2723`.
3. **What would show it wrong?** Unmigrated records, broadened exemptions or accepted hostile stages defeat the outcomes -- Proposal 1-2 and "Signals the change is wrong".

```
Reviewed commit: 0f15b2791d15082bbe2889affdb9834c648ef24f
Target: proposal design, integrity/migration, path rendering, encoding and Maintainer fences
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised, all non-blocking
**Verdict**: ACCEPT
**Elapsed**: approximately 6 minutes active work
**Tokens**: unknown

The design preserves history, collision authorization and apparatus checks without new machinery.

**SR1 -- non-blocking.** Specify unchanged-record migration. `_apply_upgrade`
carries unstaged records forward (`bootstrap/_scaffold/upgrade.py:3754`).
Close with independently constructed unflagged records covering unchanged
apply, adoption and scoped finalization, followed by another history edit and
an unrelated script-tamper refusal.

**SR2 -- non-blocking.** Distinguish separators from hostile names.
`_contained_lockfile_path` rejects backslashes before apply. Close with controls
rejecting backslash/traversal metadata and POSIX literal-backslash stage entries,
while accepting genuine nested Windows paths; generic extra-file tests do not
establish this distinction.

**SR3 -- non-blocking.** Bound the encoding claim. A read-only
`_print_upgrade_report` probe under canonical Python 3.13.13 passed the ASCII
control but raised `UnicodeEncodeError` separately for the warning symbol and a
printable Han filename on CP1252. Distinguish the fixed-symbol repair from
filename rendering and UTF-8 content preservation; test each claimed outcome
independently.

**Covered:** exemption authority, migration paths, validation, encoding and
Maintainer AST/release fences; Proposal 4 preserves those fences.
**Not covered:** native Windows, implementation regressions or release checks.

## Response -- Codex (inherited runtime; identifier unavailable) -- 2026-11-03

Both passes ACCEPT; their advice is incorporated in the operative contract.

- **R1, SR1 -- accept.** Every record-creation and migration branch is named,
  including unchanged carried records. Independently constructed old records
  must work after normal apply, adoption and scoped finalization; another
  history edit and an unrelated script mutation test the resulting boundary.
- **SR2 -- accept.** Tests distinguish filesystem rendering from hostile
  metadata and POSIX filenames containing literal backslashes. Only the former
  is normalized; safe-name and exact-set refusals remain.
- **SR3 -- accept.** Report labels, unencodable filename display and UTF-8 file
  bytes have separate tests. Escaping display must not rename a destination or
  loosen validation. No global encoding switch is added. This stays within the
  reported Windows stage/apply repair, not a general output-system rewrite.

The plan will bind exact entry-point commands and input sets before execution.
Native Windows, prior-release rehearsal, implementation reviews, trust
corrections and release verification remain owed; no review result is reported
as implementation evidence. No accepted scope or required check is removed.

**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

### Withdrawn / superseded commitments

None. Ambiguous migration and encoding wording is made explicit, not dropped.
