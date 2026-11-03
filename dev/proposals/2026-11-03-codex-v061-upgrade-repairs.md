# Repair v0.6 adopter upgrades in v0.6.1

**Author**: Codex (inherited runtime model; identifier unavailable)
**Status**: awaiting-review
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

Recent closed reports #35, #38, #40 and #42 already have corresponding changes
in this base; they are regression inputs, not permission to reopen their scope.
Other open issues request larger features and remain on their existing tracks.

## Proposal

1. **Changelog ownership.** Add exactly `CHANGELOG.md` to the existing
   authoritative living-state destination set: tracked for upgrade, exempt
   from content-hash comparison. New installs and existing/adopted v0.6
   records must acquire that classification through normal upgrade or scoped
   finalization, without requiring an edit at every release. Preserve history,
   merge ancestors and collision authorization. Do not expand the exemption
   to scripts, governing files or arbitrary lockfile assertions. Changelog
   bytes remain Git-reviewed, not integrity-attested; document that tradeoff.
2. **Windows compatibility.** Render filesystem-derived relative names with
   forward slashes before comparing them to canonical manifest names, including
   the discovery-update lookup. Do not reinterpret untrusted manifest names
   or weaken traversal/link refusals. Replace the fixed unencodable warning
   symbol with an ASCII warning label. Retain explicit UTF-8 staged-file I/O;
   verify non-ASCII content survives.
3. **Current citations.** Repoint stale section references throughout the
   shipped sources and their self-hosted twins to actual current sections or
   published methodology. Do not recreate removed rules merely to satisfy a
   reference. Add regression coverage in an existing documentation-test home
   for the shipped citation inventory, with a deliberately broken reference
   proving detection. This is a test, not a new release command.
4. **Patch preparation.** Prepare version metadata and a distinct v0.6.1
   changelog section without relabeling v0.7 deliberation entries as delivered
   features or altering released v0.6.0 history. Rehearse real v0.6.0-to-patch
   installs/upgrades on disposable projects, retaining local history/edits.
   Use the existing release process. The Maintainer alone performs required
   baseline/anchor corrections, signing, tag and publication steps.

## Rationale

One repair batch shares upgrade fixtures and release work. Existing living-state
handling avoids new options or routine operator steps. The cost is a narrowly
weaker integrity claim for project history, plus targeted regression tests.
This is not an upgrade-engine redesign or v0.7 implementation.

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
records; edit after upgrade; script-edit and illegal-exemption refusals;
history preservation and repeat upgrade. Exercise real stage/apply for Windows
relative rendering, non-ASCII files, CP1252 reports and changed/extra staged
paths. Add citation controls in an existing documentation-test family.
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
S3: existing install, upgrade and integrity entry points govern actual output.
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
