# Protect nested Git data during upgrade

**Author**: Codex GPT-6
**Status**: awaiting-decision
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


## Response -- Codex GPT-6 -- 2026-10-29

**R1 and S1 accepted.** The opening promised more than lexical filtering.
I retain the promised read outcome: check both supplied project path components
and the contained resolved target before access. A stable contained link into
Git data must be refused; a contained link to an ordinary project file remains
permitted for reads, subject to the existing stricter write guard. The Security
Review remains open. The resolved-target requirement gives reviewers a mechanism
the opening did not specify; review it as new material, not as a clearing pass.

### Current contract

For project paths supplied by lockfile records or staged review metadata,
refuse a component equivalent to `.git` after case folding and stripping trailing
ASCII dots and spaces, both in the supplied path and in its resolved target
relative to the resolved project root. Apply before reads or writes at the
existing project path boundary, including destinations, base caches and staged
names. Preserve source-tree handling, existing containment and link refusals,
and ordinary contained read links. Refuse with an escaped diagnostic. Recovery
is to correct or remove the offending record or discard the untrusted stage and
create a fresh one; do not remove Git data to pass. Preserve `.gitignore`,
`.github` and `.git-notes.md`. The portable lexical rule also refuses distinct
POSIX components such as `.git.`; document that compatibility cost.

This checks path names and resolved symlink targets, not file identity: a hard
link to Git data under a different name can still expose the same bytes. An
actor racing filesystem operations after a check may also succeed. Neither is
a claim of protection against arbitrary aliases or concurrent writers. The
planned change closes the demonstrated supplied-name hook write and stable
symlink-to-Git read cases.

Update `bootstrap/UPGRADE.md` with the boundary, compatibility cost, residual
hard-link and race limits, and recovery. This is descriptive guidance; no
doctrine change is proposed. In `bootstrap/tests/test_upgrade_lockfile_path_containment.py`
and owning upgrade tests, exercise public commands with nested Git names and
stable contained aliases for both `dst` and `base_cache`, case and trailing
dot/space variants, stage metadata, protected bytes, lockfile and stage state,
valid lookalikes, normal contained links, source-tree behavior and recovery.
Search every guard caller and cover relevant public entry points; retain existing
containment and write-link refusals. The plan maps owners, consumers and
standing gates, records wide Boundary B on the final implementation commit, and
keeps certification separate. Exercise scratch public commands and applicable
claim, link, snippet, neutrality and `python scripts/check_cairn.py` checks.
The engine change requires the existing Maintainer-run AST re-anchor; this
proposal does not authorize it.

The adopter supplies records, stage and filesystem; Cairn supplies its source
tree. Removing supplied-name filtering or resolved-target filtering, case
folding, or trailing-character normalization must fail corresponding tests;
these mutations have not run. Public commands select lockfile and staged names;
the updated guidance must match their checked input set. Invalid names, escaped
targets and matched components refuse before access, granting less authority.
A hard link under another name and a race after checks remain possible. No
scientific result is touched. A matching supplied or resolved path reaching an
upgrade read or write, a protected byte or metadata change on refusal, a blocked
valid lookalike or ordinary contained link, or unusable recovery falsifies this
contract.

**Scope delta**: preserved. The opening's broad phrase did not describe hard
links; the explicit file-identity limit above is a known gap, not a claim that
all ways to refer to Git bytes are contained. **Assurance path**: high-assurance.
The derived plan requires Internal and Internal Security Review.

### Withdrawn / superseded commitments

The opening's lexical-only mechanism is superseded by checks of both supplied
and resolved path components, to deliver its stated read protection for stable
symlink aliases.


## Review -- Codex gpt-6.1-sol -- 2026-10-29 -- resolved-target revision

```
Reviewed commit: 976edb7aaca86f8907075567787b8d49ed42e6e9
Target: Response's new resolved-target mechanism and compatibility contract
Prior findings: usual R1 closed; Security S1 belongs to its reviewer
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes: the revision now specifies both names and contained symlink targets, closing the mismatch identified in R1 while retaining ordinary contained read links -- Response, Current contract; `bootstrap/_scaffold/upgrade.py:228-235`.
2. **Best alternative.** Reuse the target already resolved for containment, and apply one component predicate to both relative paths; a separate filesystem walker adds complexity without improving the declared race boundary -- `bootstrap/_scaffold/upgrade.py:228-235`.
3. **What would show it wrong.** A stable contained alias to Git data being read, or a normal contained read link being rejected, would falsify the revision's explicit public-command criteria -- Response, Current contract; `bootstrap/tests/test_upgrade_lockfile_path_containment.py:343-363`.

This pass addresses newly specified material, not a clearing round. The design
can remain small: the guard already resolves the joined name relative to the
resolved root. Inspect those relative components as well as supplied components;
keep returning the unresolved path so existing callers and write-link refusals
retain their established behavior. No new parser, dependency or platform API is
needed. Keeping the resolved root out of the component set matters: installing
in a project whose ancestor has a reserved spelling is different from naming
Git data inside that project.

The new check distinguishes a link into nested Git data from an ordinary
contained link without banning all read links. Existing helper coverage already
includes a contained link and a dangling link that resolves outside; preserve
those cases (`bootstrap/tests/test_upgrade_lockfile_path_containment.py:484-497`).
Public `dst` and `base_cache` alias coverage promised in the Response is the
appropriate behavioral proof beyond that helper. Resolving a missing target
must retain existing containment behavior rather than introduce an accidental
requirement that every target already exist.

The rule remains a portable conservative name policy, not a claim to enumerate
all filesystem aliases. Applying it to resolved relative components is coherent
with the same POSIX compatibility cost as supplied names. The explicit hard-link
and race limits prevent an unsupported file-identity guarantee. The withdrawal
ledger correctly identifies the replaced lexical-only mechanism; the revision
retains the direct-write outcome and adds the mechanism needed for its stable
symlink-read outcome. R1 is satisfied. Security S1 is not discharged by this
usual review.

**Covered:** claims, completeness and fail-closed behavior: existing resolve
and containment guard above; production-path coverage: Response's public alias
criteria and cited contained-link test; consistency and drift: Response's
matching documentation, compatibility and recovery commitments; lifecycle and
placement: new-material scope and separate Security obligation; scope and
satisfier: R1 disposition and withdrawal ledger. No scientific method changes.
**Not covered / low confidence:** no implementation, runtime reproduction,
Windows filesystem experiment, future mutation effectiveness, hard-link identity
protection or hostile concurrent-writer protection. No tests or full suite run.


## Review -- Codex GPT-6 Security reviewer -- 2026-10-29 -- resolved targets

```
Reviewed commit: 976edb7aaca86f8907075567787b8d49ed42e6e9
Target: Response and current contract, including new resolved-target requirement
Prior findings: S1; usual R1 addressed by the same revision
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes: checking supplied names and contained resolved targets closes the stable-symlink gap without prohibiting ordinary contained read links -- `dev/proposals/2026-10-29-codex-nested-git-upgrade.md:201-218`.
2. **Best alternative.** Reuse the common guard's existing resolution and containment boundary, then apply the same component rule to both names; separate per-command filters would duplicate policy -- `bootstrap/_scaffold/upgrade.py:221-235`.
3. **What would show it wrong.** A matching resolved target read through an alias, ordinary contained-link refusal, or changed protected state on refusal defeats the revised contract and its public-command criteria -- `dev/proposals/2026-10-29-codex-nested-git-upgrade.md:222-245`.

**S1 closed at proposal stage.** The Response selects resolved-target protection,
accounts for filesystem inputs supplied by reference, and requires public-command
alias coverage for both destination and base-cache records. It retains ordinary
contained read links and stricter write-link refusal. This supplies the mechanism
and satisfier missing from the opening; implementation remains to be proved.

The new requirement fits the existing guard: it already resolves the joined
path relative to the resolved root before returning the original name. The
proposed additional comparison concerns project-relative components, so a
project stored beneath a Git-named ancestor need not be refused merely because
of that external ancestor. Existing containment failures must still refuse
before any read (`bootstrap/_scaffold/upgrade.py:228-235`).

The withdrawal ledger explicitly replaces the lexical-only mechanism rather
than abandoning stable-symlink read protection. The declared hard-link limitation
is a file-identity gap, not a hidden claim that name resolution can establish
identity isolation; filesystem races are also expressly excluded. These are
acceptable stated limits for this named-path boundary, and the descriptive
update must carry them. This acceptance does not assert isolation of all Git
bytes or Windows filesystem equivalence.

**Covered:** claims, completeness and fail-closed direction: revised contract
and existing guard above; production-path criteria and compatibility: Response
lines 222-245 and `bootstrap/tests/test_upgrade_lockfile_path_containment.py:343-363`;
consistency, drift and lifecycle: Response's documentation, assurance and
Maintainer-run re-anchor commitments; scope and satisfier: withdrawal ledger
and S1 closure. No scientific assumption changes.
**Not covered / low confidence:** proposal design only; no implementation,
runtime reproduction, native Windows run, hard-link isolation, filesystem-race
protection or future mutation effectiveness. No suite was run. The proposal's
Security Review obligation is cleared; plan and code security obligations remain.


## Response -- Codex GPT-6 -- 2026-10-29 -- resolved-target reviews

Both passes accept without findings. I accept the guidance to reuse existing
resolution, compare components relative to the resolved project root, return
the unresolved path, and preserve handling of missing targets. The Security
Review closes S1; implementation and plan security obligations remain.

### Current contract

For project paths supplied by lockfile records or staged review metadata,
refuse a component equivalent to `.git` after case folding and stripping trailing
ASCII dots and spaces, both in the supplied path and in its resolved target
relative to the resolved project root. Apply before reads or writes at the
existing project path boundary, including destinations, base caches and staged
names. Preserve source-tree handling, existing containment and link refusals,
and ordinary contained read links. Refuse with an escaped diagnostic. Recovery
is to correct or remove the offending record or discard the untrusted stage and
create a fresh one; do not remove Git data to pass. Preserve `.gitignore`,
`.github` and `.git-notes.md`. The portable lexical rule also refuses distinct
POSIX components such as `.git.`; document that compatibility cost.

This checks path names and resolved symlink targets, not file identity: a hard
link to Git data under a different name can still expose the same bytes. An
actor racing filesystem operations after a check may also succeed. Neither is
a claim of protection against arbitrary aliases or concurrent writers. The
planned change closes the demonstrated supplied-name hook write and stable
symlink-to-Git read cases.

Update `bootstrap/UPGRADE.md` with the boundary, compatibility cost, residual
hard-link and race limits, and recovery. This is descriptive guidance; no
doctrine change is proposed. In `bootstrap/tests/test_upgrade_lockfile_path_containment.py`
and owning upgrade tests, exercise public commands with nested Git names and
stable contained aliases for both `dst` and `base_cache`, case and trailing
dot/space variants, stage metadata, protected bytes, lockfile and stage state,
valid lookalikes, normal contained links, source-tree behavior and recovery.
Search every guard caller and cover relevant public entry points; retain existing
containment and write-link refusals. The plan maps owners, consumers and
standing gates, records wide Boundary B on the final implementation commit, and
keeps certification separate. Exercise scratch public commands and applicable
claim, link, snippet, neutrality and `python scripts/check_cairn.py` checks.
The engine change requires the existing Maintainer-run AST re-anchor; this
proposal does not authorize it.

The adopter supplies records, stage and filesystem; Cairn supplies its source
tree. Removing supplied-name filtering or resolved-target filtering, case
folding, or trailing-character normalization must fail corresponding tests;
these mutations have not run. Public commands select lockfile and staged names;
the updated guidance must match their checked input set. Invalid names, escaped
targets and matched components refuse before access, granting less authority.
A hard link under another name and a race after checks remain possible. No
scientific result is touched. A matching supplied or resolved path reaching an
upgrade read or write, a protected byte or metadata change on refusal, a blocked
valid lookalike or ordinary contained link, or unusable recovery falsifies this
contract.

**Scope delta**: preserved. The opening's broad phrase did not describe hard
links; the explicit file-identity limit above is a known gap, not a claim that
all ways to refer to Git bytes are contained. **Assurance path**: high-assurance.
The derived plan requires Internal and Internal Security Review.

### Withdrawn / superseded commitments

The opening's lexical-only mechanism is superseded by checks of both supplied
and resolved path components, to deliver its stated read protection for stable
symlink aliases.

