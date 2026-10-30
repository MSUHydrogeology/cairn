# Upgrade growth — stop listing hostile cases, let Git do the writing

**Author**: Claude Opus 5.5 (Strategy)
**Date**: 2026-10-30
**Status**: draft
**Type**: product-strategy
**Surfaces this would feed**: `bootstrap/_scaffold/upgrade.py`; `bootstrap/_scaffold/merge.py`; `bootstrap/_scaffold/security.py`; `bootstrap/UPGRADE.md`; `bootstrap/SAFETY.md`; the lockfile and fidelity manifest (install contract)

## Conclusion first

The upgrader grows because it keeps its own state in the adopter's working
tree and defends that state by listing hostile path cases one at a time. Each
case costs a refusal, a test module, a Security Review chain and a re-anchor
only the Maintainer can run. I recommend two things:

1. **Now:** no new upgrade refusal unless it names an attacker inside the
   threat model `bootstrap/SAFETY.md` already states. Cases outside it are
   recorded as accepted residual risk, one line each, not code.
2. **Next:** a short, measured trial of a Git-native upgrade, where Cairn
   commits each template version to a branch in the adopter's repository and
   the adopter merges it with `git merge`. If the trial holds up, a proposal
   follows.

## The question

The Maintainer asked how we feel about scaffold growth (chat, 2026-10-30),
after seeing that `0.6-dev` added more test lines than product lines.

## Measured, 2026-10-30

Engine lines (`bootstrap/_scaffold/` plus `bootstrap/scaffold.py`), from
`git show` at each tag:

| Version | Date | Lines |
|---|---|---|
| v0.2.0 | 2026-05-27 | 2,526 |
| v0.3.0 | 2026-06-12 | 7,526 |
| v0.4.0 | 2026-10-20 | 9,474 |
| v0.5.0 | 2026-10-28 | 10,665 |
| `0.6-dev` HEAD | 2026-10-30 | 11,792 |

- `upgrade.py` is 4,277 lines and 77 functions, 36% of the engine. Lines that
  refuse or raise went from 123 to 158 in two days.
- Five plans since 2026-10-28 hardened upgrade against path tricks: saved
  ancestor checks, nested Git data, directory collisions, planted links at
  `--init-lock`, and review-copy rendering (`CHANGELOG.md`).
- The engine's AST pin is owed now: `test_ast_attest.py` fails at HEAD after
  18 engine commits and two baseline updates since the branch began.
- The scattered-writer problem is already solved. One containment check,
  `_assert_safe_write` in `security.py`, is called at 50 sites. The growth
  is not from writers that skip it.
- The three-way merge is already Git's: `merge.py:150-172` runs
  `git merge-file`.

## Why it grows

**Upgrade's state lives where agents can edit it.** The lockfile, the base
cache, the staging area and the review copies are files in the adopter's tree.
Each one carries paths, so each is a parser of data that agents could have
changed. Nested-Git protection alone had to cover "lockfile destinations, base
caches and staged review metadata" (`CHANGELOG.md`).

**The threat is a confused deputy.** Agents write the working tree and could
be manipulated; a person runs upgrade with their own privileges. A planted
link could turn an upgrade into a write outside the project. That threat is
real and stays in scope.

**Listing cases never finishes.** `bootstrap/UPGRADE.md:775-793` states what
the nested-Git check cannot catch: hard links reached by another name, races,
authenticity. Each Security Review finds the next case, because the method
invites it.

**Every engine change spends the Maintainer.** An engine edit ends in an AST
re-anchor only the Maintainer runs (`AGENTS.md`, "AST attestation baseline").
The growth draws on the scarcest resource Cairn has.

## Options

**A. Keep going, with discipline.** Require each new refusal to name its
attacker. Cheap. Growth slows but never stops.

**B. Narrow the threat model.** `bootstrap/SAFETY.md:231-233` already accepts
risk under "no concurrent filesystem attacker; no untrusted code path". Apply
that model consistently: record out-of-model cases as accepted residuals
instead of building checks for them. This is the "now" step. It costs nothing,
but it only stops new growth.

**C. Git-native upgrade (a "vendor branch").** The adopter's repository keeps
a branch, say `cairn/template`, holding pure renders of each template version
with the adopter's tokens filled in. To upgrade:

1. Cairn renders the new version and commits it to that branch with Git's
   low-level commands (`hash-object`, a temporary index, `write-tree`,
   `commit-tree`). It writes nothing into the working tree.
2. The adopter runs `git merge cairn/template`. Git finds the previous render
   as the merge base, merges every file three ways, marks conflicts, refuses
   a dirty tree and writes through its own checkout.
3. Undo is `git merge --abort` before committing, or `git revert` after.

What disappears: the base cache, the staging area, the `.ours` and `.theirs`
review copies, the record-your-edit step, Cairn's dirty-tree refusal, and most
path refusals, because Git, not Cairn, writes the working tree. The merge is
already Git's, so this extends a choice Cairn has made, not a new dependency.

Precedent: Copier updates a project by regenerating it at the new template
version and re-applying the user's changes. It wants the project under Git and
offers inline conflict markers or `.rej` files (its documentation, read
2026-10-30). Cruft's page does not say how it applies changes.

What it costs:
- **Slot-aware merging becomes line merging.** `templates/core/AGENTS.md`
  has five `cairn:slot` markers; customized slots may conflict more often.
  The trial measures this.
- **The install contract changes.** The lockfile and fidelity manifest change
  meaning. That is a high-risk, adopter-facing proposal.
- **Existing adopters need a one-time migration.** Their recorded base cache
  already holds the bytes needed to seed the branch.
- **Git becomes required for upgrade.** It is already required for the merge;
  `merge.py` names a no-Git fallback only as a follow-up.
- **Git's own checkout must be trusted.** Git has had path-safety flaws, and
  they are fixed by a large community rather than by Cairn alone. Whether Git
  refuses to write through a link the adopter committed is an assumption to
  test, not a fact I checked.

**D. Declarative path policy.** Fold the refusals into one table of rules the
check reads. It tidies the code but keeps the same model and the same
re-anchor cost.

## Recommendation

1. **Adopt B now** as a working rule for upgrade reviews: a new refusal names
   its attacker against `SAFETY.md`'s model, or it becomes a one-line
   residual. This needs no engine change.
2. **Run a trial of C** in a scratch repository, time-boxed to one session:
   install v0.5.0, customize it like a real adopter, then upgrade to HEAD
   both ways. Measure conflicts per upgrade, the engine code each path
   exercises, and which tests in `test_upgrade_refuses_hostile_project_data.py`
   still apply. Include a planted link in the committed tree.
3. **If the trial holds,** write a heavy-tier proposal, since it changes the
   install contract.
4. **Batch the owed AST re-anchor** with the next Maintainer ceremony rather
   than running it alone.

## Signals this direction is wrong

- The trial shows many more conflicts than the slot-aware merge.
- Git writes through a planted link.
- Adopters exist who upgrade without Git.
- The migration from base cache to branch loses customizations.

## What to watch

Engine lines per release, refusal count in `upgrade.py`, and engine re-anchors
per week, all read from git.
