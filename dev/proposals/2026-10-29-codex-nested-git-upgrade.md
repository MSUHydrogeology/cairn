# Protect nested Git data during upgrade

**Author**: Codex GPT-6
**Status**: revising
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Refuse upgrade paths into nested Git data so a staged upgrade cannot plant a Git hook.

## Context

The project path guard in `bootstrap/_scaffold/upgrade.py` rejects `.git` only as the first path component. The independent review in `dev/plans/archive/2026-10-26-code-review-lockfile-path-findings.md` F2 reports that a crafted review area applied `sub/.git/hooks/post-merge`, and a lockfile destination `sub/.git/description` was replaced. A hook is a program Git can run. The same review measured an any-component guard against its owner tests; its Windows trailing-dot and space concern was reasoned, not run. `dev/PLANNING.md` records the queued issue. Existing guidance in `bootstrap/UPGRADE.md` promises root `.git` protection, so this is a contract expansion.

## Proposal

For project paths supplied by the lockfile or staged review metadata, refuse any path component equivalent to `.git` after case folding and stripping trailing ASCII dots and spaces. Apply the rule at the existing project-path guard, including destination and base-cache paths and staged names, before reads or writes. Keep the Cairn source-tree rule unchanged. Preserve legitimate lookalikes such as `.gitignore`, `.github`, and `.git-notes.md`. Refuse with an actionable diagnostic; recovery is to remove or correct the offending lockfile record or discard the untrusted stage and create a fresh one, without modifying Git data. Do not claim protection against a concurrent hostile filesystem writer.

## Rationale

A nested repository's Git data is as sensitive as the root's. One guard covers its existing project-path callers, including the independently demonstrated staged and lockfile paths, rather than protecting only a hook spelling. Normalizing trailing dots and spaces also addresses names treated as equivalent on Windows; the implementation must verify the rule without claiming a Windows run that did not happen.

## Alternatives considered

Doing nothing retains the demonstrated hook write. Rejecting only hooks leaves configuration and other Git data exposed. Rejecting only exact lowercase `.git` leaves case variants and Windows aliases; rejecting all names beginning `.git` would unnecessarily block ordinary files.

## Documentation / doctrine surface

Update `bootstrap/UPGRADE.md` to describe the expanded refusal and recovery. This is descriptive software guidance; deliberation remains in `dev/`, following `docs/DOCUMENTATION_PLAN.md`. No doctrine change is proposed.

## Evidence / verification plan

### Tests required

Add behavioral coverage in `bootstrap/tests/test_upgrade_lockfile_path_containment.py` and its owning upgrade tests. Through public upgrade commands, exercise lockfile `dst` and `base_cache` and crafted review-area names, including nested hooks and Git data, case variants, trailing-dot and space variants, unchanged protected data and metadata on refusal, and recovery with a fresh stage. Test valid lookalikes and source-tree behavior. Search all project-path guard callers and cover each relevant public entry point; preserve existing containment and link refusals. The plan maps owning tests, consumers and standing gates and records wide Boundary B on the final implementation commit; certification is separate.

### Examples / smoke checks

Exercise public commands in scratch projects and run applicable claim, link, snippet and neutrality checks and `python scripts/check_cairn.py` for changed prose. Engine changes require the existing Maintainer-run AST re-anchor; this proposal does not authorize it.

#### Security preflight — five questions

* **S1:** The adopter supplies lockfile and review-area path names and the project filesystem; Cairn supplies its source tree. The object being checked supplies the names.
* **S2:** Removing the any-component check, case folding, or trailing-character normalization must cause corresponding tests to fail. These mutations have not been run for the proposed implementation.
* **S3:** Public upgrade commands select lockfile records and staged metadata; the guard checks project names at its callers. The current guidance says a record inside `.git/` is refused (`bootstrap/UPGRADE.md`); revise it to match the expanded set and test each caller.
* **S4:** A matching component refuses before access, granting less authority. Invalid shapes and existing containment and link errors retain refusal; normalization must not turn a nonmatching path into an allowed Git alias.
* **S5:** An attacker who can supply a lockfile or stage can choose names, but should not use these paths to access nested Git data. An attacker who can race filesystem operations after checks may still succeed; this does not claim arbitrary concurrent-writer protection.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A nested Git path is read or written through an upgrade, refusal changes Git data or metadata, a valid lookalike is blocked, or normal recovery cannot produce a usable stage.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance


## Review -- Codex gpt-6.1-sol -- 2026-10-29

```
Reviewed commit: 21f7eef7c45c7476907a85f442e92db79cbc589b
Target: opening proposal and cited upgrade guard/callers
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes: protect nested Git names at the existing common guard, but align the read-protection claim with the proposed lexical boundary -- `bootstrap/_scaffold/upgrade.py:171-235`.
2. **Best alternative.** An any-component predicate in that guard is simpler than separate hook, stage and lockfile filters; doing nothing preserves the demonstrated write -- `dev/plans/archive/2026-10-26-code-review-lockfile-path-findings.md`, F2.
3. **What would show it wrong.** Refusal of an ordinary lookalike or a matching name reaching an upgrade consumer defeats the contract; an in-project link reaching Git data defeats the broader read claim -- `bootstrap/tests/test_upgrade_lockfile_path_containment.py:343-363`, `bootstrap/_scaffold/upgrade.py:664-668`.

The proposal addresses the cause rather than a single hook spelling. The
existing guard's callers are `_check_lockfile_paths` (project `dst` and
`base_cache`, source `src`), the two source readers, and `_apply_upgrade`'s
staged names. The staged-name set includes `staged_files`, `review_only`,
`module_blocked`, `expected_absent`, `kinds` and `new_entries`. The central
lockfile check precedes plan, stage, apply, finalize, collision adoption,
retired removal and module adoption dispatch; the existing tests' `_ACTIONS`
set omits module adoption, so the plan's promised caller search matters.
Source readers use a different tree label and should retain their behavior.

**R1 -- clarify named paths versus resolved read targets (blocking).** The
proposal says to reject matching supplied components, but its wrongness signal
says any nested Git path being read is failure. Those differ: the current
guard deliberately permits links that resolve inside the project, and
`_compute_upgrade` reads `dst_abs` through such a link. A plain name such as
an ordinary notes file linked to a nested Git description file contains no matching component.
No concurrent writer is needed. State whether the commitment protects supplied
names only or also resolved read targets. I recommend retaining the small
named-component change and explicitly documenting this residual read exposure
in the proposal and descriptive guidance, with a regression showing that
ordinary contained links remain compatible. That narrower claim loses a
blanket guarantee against Git reads through aliases, while still closing the
measured direct hook-write cause; it does not concede any accepted scope.
Alternatively, protecting resolved Git targets needs an explicit contract and
coverage preserving legitimate contained links. Satisfier: an appended Response
settling the boundary and matching tests/documentation criteria.

The dot/space rule is a conservative lexical restriction portable across
hosts; it intentionally refuses some distinct POSIX names. Preserve that
compatibility cost in the documentation rather than presenting a non-Windows
run as proof of Windows filesystem equivalence. The proposal already avoids
that measurement claim and preserves ordinary `.git`-prefixed lookalikes.

**Covered:** claims, completeness and fail-closed behavior: guard and callers
above; production-path coverage: containment tests' `_ACTIONS` and public
`upgrade` helper; consistency and drift: `bootstrap/UPGRADE.md:367`;
lifecycle and placement: proposal review headers and documentation section;
scope and satisfier: R1. No scientific method is changed.
**Not covered / low confidence:** no runtime reproduction, Windows filesystem
run, implementation or Security Review; source inspection cannot establish
future test effectiveness or protection against filesystem races.


## Review -- Codex GPT-6 Security reviewer -- 2026-10-29

```
Reviewed commit: 17dff8a2315ac6a67995f7f46d84d097cb161c46
Target: opening proposal, usual review R1, and cited upgrade path boundary
Prior findings: usual R1 remains open
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Close the demonstrated nested hook-write path, but settle the difference between names and actual read targets before approval -- `bootstrap/_scaffold/upgrade.py:171-235`.
2. **Best alternative.** Keep one project-name predicate at the common guard, with an accurately bounded promise; a blanket Git-data access guarantee needs additional target checks -- `bootstrap/_scaffold/upgrade.py:221-235`.
3. **What would show it wrong.** A stable contained link into Git data defeats the opening read guarantee without any filesystem race, while ordinary contained links are expressly compatible -- `bootstrap/_scaffold/upgrade.py:664-668`, `bootstrap/tests/test_upgrade_lockfile_path_containment.py:343-363`.

The direct write fix is justified: Git metadata includes executable hooks, not
merely descriptive files. Checking every supplied component closes the demonstrated
nested-name hole without inventing a second path parser. Existing write protection
separately rejects symlinks before destination writes; preserving it is necessary,
not evidence that reads reject the same links
(`bootstrap/_scaffold/upgrade.py:3178-3184`).

**S1 -- settle the access boundary (blocking; joins usual R1).** A harmless
supplied name can point to a nested repository's Git data while staying inside
the project. The guard returns the unresolved name; destination bytes and base
cache text are then read through it (`bootstrap/_scaffold/upgrade.py:228-235`,
`bootstrap/_scaffold/upgrade.py:664-668`,
`bootstrap/_scaffold/upgrade.py:708-709`). This is a pre-existing filesystem
arrangement, not the concurrent-writer capability excluded in S5. The opening
wrongness signal and S5 therefore promise more than the proposed mechanism.

I recommend the small lexical boundary for closing the measured direct-write
cause, with an explicit residual exposure: Git data can still be read through
contained aliases. That loses the opening blanket read outcome; record the
scope delta and obtain the Maintainer's allowance rather than silently treating
it as preserved. Alternatively retain that outcome and specify resolved-target
refusal while preserving ordinary contained links. Satisfier: an appended
Response carrying the complete chosen contract, matching wrongness signals,
S1/S5 accounting, documentation criteria and public-command tests for both
`dst` and `base_cache` aliases. This Security obligation remains open until the
boundary is settled.

The conservative dot/space and case rule also rejects distinct POSIX names;
name that compatibility cost in `bootstrap/UPGRADE.md`. Keep diagnostics escaped
and recovery limited to correcting records or replacing the untrusted stage:
Git data must not be removed to make an upgrade pass. Public refusal tests should
observe protected bytes, lockfile and stage state, rather than only an error code.

**Covered:** claims, completeness and fail-closed behavior: guard/read/write
sites above; public coverage and compatibility: cited containment test and
proposal verification criteria; consistency and drift: `bootstrap/UPGRADE.md:367`;
lifecycle, scope and satisfier: S1 and declared high-assurance path. No scientific
assumption changes.
**Not covered / low confidence:** source inspection only; no runtime reproduction,
Windows filesystem behavior, future implementation, mutation effectiveness,
hard-link aliases or concurrent filesystem writers. No suite was run.
