# Plan: v0.6.1 adopter upgrade repairs

**Source proposal**: dev/proposals/archive/2026-11-03-codex-v061-upgrade-repairs.md
**Author**: Codex (inherited runtime model; identifier unavailable)
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-03
**In brief**: Repair changelog ownership, Windows upgrades and stale citations, then prepare v0.6.1 without performing the Maintainer's trust or publication steps.

## Source proposal

Decision `184dd877` accepts the complete grouped repair contract and review
clarifications. Changelog content becomes project-owned living state while
apparatus integrity, collision review and path refusals remain. No new command,
service or recurring operator step is introduced.

## Scope

Change the existing lockfile policy and upgrade engine, owning tests, shipped
sources with stale governing references and their self-hosted copies. Prepare
`CITATION.cff`, README version text and a separate patch changelog section.
Preserve released history and all v0.7/v0.8 work. No engine redesign, new
dependency, global encoding switch, trust-record edits or publication.

**Reuse:** searches for `_LIVING_STATE_DSTS`, `_record_fork_entry`,
`relative_to`, `_display_name` and citation readers found existing policy,
record builders, report display and documentation-test homes. Extend those;
do not introduce another registry, parser framework or release runner.

### Documentation / doctrine surface

Describe ownership/migration in `bootstrap/UPGRADE.md` and the changelog
template. Repair stale section citations in shipped sources, self-hosted
copies and directly corresponding methodology; do not resurrect removed rules.
Deliberation stays here; software description stays with existing docs.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Changelog living-state policy and record migration | Both plan reviews folded | Existing policy/record paths plus regressions |
| C2 | Windows filesystem comparisons and report display | Same review gate; separate hostile-name controls | POSIX-rendered filesystem keys, encoding-safe reports, tests |
| C3 | Governing-reference repair and regression inventory | Same review gate | Current citations, aligned twins and falsifiable doc test |
| C4 | Prior-release rehearsal and patch preparation | C1-C3 implemented; code and Security Reviews precede final Boundary B | Version/notes, migration evidence, outstanding-platform report |
| C5 | Native Windows evidence and trust/release completion | MAINTAINER-ONLY for host access, baseline/anchor correction, signing, tagging and publication | Applicable Windows result, prescribed trust correction and release evidence |

C1-C3 may share one implementation commit and fixture preparation. No extra
review between chunks. C5 is not authorized by the Decision; stop at its fence.

## Acceptance criteria

**C1.** Only root `CHANGELOG.md` joins the authoritative exemption set. Fresh
install, unchanged carried records, added records and collision adoption emit
the flag; scoped finalize migrates old records too. Independently constructed
unflagged fixtures become editable without recurring finalize. Existing history,
merge ancestors and repeat upgrade survive. Script edits and forged exemptions
still fail integrity. No change to verification policy for any other path.

**C2.** Genuine nested Windows filesystem paths compare to canonical manifest
keys, including discovery outputs. Backslash/traversal metadata, POSIX
literal-backslash stage names, missing/extra files and link escapes still
refuse. CP1252 label and filename-display cases succeed independently of UTF-8
content round-tripping; display escaping never changes actual file names.
Native Windows stage/apply remains required before declaring #44 closed.

**C3.** Inventory shipped sources from the install mappings and check explicit
governing-section citations against actual emitted sections. Include the
session, stem, plan and rules references; fix corresponding live twins.
A broken-heading mutation goes red through the same test. Keep genuine
slot-target metadata distinct from section references. Existing link/content
checks pass; no scanner opt-out or recreated doctrine.

**C4.** A disposable project installed from actual `v0.6.0` upgrades through
the patch CLI, retaining committed custom history and other local edits;
another changelog edit passes integrity while script mutation fails. Repeat
upgrade is safe. Version is 0.6.1 with preparation date, not a claim of release.
The patch notes contain only patch outcomes; released v0.6.0 history is
unchanged and v0.7 deliberation stays Unreleased. Reviews and wide Boundary B
record all non-passes without waivers.

**C5.** Native Windows public stage/apply and encoding evidence is recorded.
Maintainer performs any prescribed trust corrections and release checks on
reviewed bytes. Do not close issues, archive this plan, sign, tag, push or
publish before applicable evidence and authority exist.

Security preflight S1/S4/S5 are unchanged from the proposal. S2 mutations occur
in owning tests: script/exemption, stage corruption and stale-heading controls.
S3 public paths are `bootstrap/scaffold.py` install and upgrade
`--stage`, `--apply`, `--adopt-collisions` and scoped `--finalize CHANGELOG.md`,
followed by `bootstrap/verify_integrity.py --target` on each disposable target.
The plan record binds filled-in arguments and input trees to results.
No scientific assumption or result is touched.

## Scope delta

Preserved: all accepted outcomes, including native Windows and release/trust
evidence. Outstanding fences are not deferrals or authority to waive checks.

## Verification

Canonical Python: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13).
Boundary A uses `tools/test_tiers.py for` on the actual changed paths; retain
the selected union in batches of at most 40 files, with no broad-run override.
The initial source mapping selects 86 test files; re-derive after edits.
Principal homes: existing upgrade, module-addition, integrity, lockfile,
documentation-plan, session and stem tests. Add controls only for uncovered
faults. Collect and run the selected union once after the grouped edits,
rather than repeating it per chunk. Run scoped claim/link/content checks and
`scripts/quality_gate.py --sub neutrality --sub redundancy` for prose.

Boundary C is independent usual code review plus separate Security Review,
using tight falsification probes, not suites. Then wide Boundary B on a clean
committed copy covers the selected union, mapped integrations, twin fidelity,
real prior-tag rehearsal and relevant trust checks. Record SHA/range, clean
states, interpreter, commands, counts, elapsed time, token uncertainty and
omissions. Unmet trust/platform checks keep the plan open at C5; no baseline
or frozen-file alteration by the implementer. Full certification stays at its
existing release/re-anchor trigger, not during iteration or review.

**Elapsed**: approximately 6 minutes. **Tokens**: unknown.

## Plan review -- Codex (inherited runtime; exact model identifier unavailable) -- 2026-11-03

**Foundations**

1. **Should this happen as framed?** Yes: C1-C5 retain migration, Windows, citation and patch outcomes, including outstanding platform/trust evidence -- Decision `184dd877`, plan Acceptance criteria.
2. **Best alternative.** Extend the existing exact-path policy, record builders and display helper; no additional mechanism is needed -- `bootstrap/_scaffold/lockfile.py:83`, `bootstrap/_scaffold/upgrade.py:1880`, `bootstrap/_scaffold/install.py:41`.
3. **What would show it wrong?** An unflagged carried record, accepted hostile stage or undetected stale citation would defeat C1-C3; the named owning tests provide extension points -- `bootstrap/tests/test_upgrade.py:1090`, `bootstrap/tests/test_upgrade_module_additions.py:792`, `bootstrap/tests/test_documentation_plan_module.py:135`.

```
Reviewed commit: 4001192bac05c507a1fbd8c360c7eab6fd212d69
Target: whole plan against accepted Decision 184dd877
Prior findings: none
Assurance path: high-assurance (accepted source)
```

**Tier**: Internal
**Obligation**: usual plan review
**Findings**: raised, non-blocking
**Verdict**: ACCEPT

**PR1 -- non-blocking.** Bind commands to cases before execution, not only
afterward in the results record. The accepted source Response promises exact
commands/input sets before execution; plan S3 currently lists operation names
and postpones filled arguments. Close by naming each independent old-record
fixture and its stage/apply, adoption or scoped-finalize command, followed by
the history-edit/integrity and script-tamper controls. Existing test fixtures
can supply these bindings; no new runner is needed.

**Elapsed**: approximately 6 minutes. **Tokens**: unknown.

**Covered:** committed migration branches, filesystem-versus-metadata
normalization, mapped citation sources, verification scope and C5 fences;
scratch manifest/selector probes and scoped prose checks passed under Python
3.13.13. The plan retains wide Boundary B after both implementation reviews.
**Not covered:** implementation, native Windows, prior-tag rehearsal, mutations,
full suite, trust ceremonies or the separate Security Review obligation.
