# Plan: Share claims across worktrees

**Source proposal**: dev/proposals/archive/2026-11-03-claude-shared-claims-across-worktrees.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**In brief**: Share a clone's work-intent claims across its verified worktrees so contributors and commit hooks see the same claims.

## Source proposal

The accepted heavy Decision selects the main checkout's existing log for
verified linked worktrees, with a local fallback and reason for other layouts.
It retains guarded pruning, session containment, both reviews and the
Maintainer's separate repin.

## Scope

Change `tools/_intent/shared.py`, `tools/_intent/record_io.py`,
`tools/prune_intents.py`, `tools/session.py` and their shipped twins under
`templates/modules/team-gated/` and `templates/skills/_lib/session.py`.
Update `docs/methodology/coordination.md` and
`templates/modules/team-gated/coordination-tiers.md`; preserve the distinction
between claims and the separate event log. Extend existing test homes below.
No new shared framework, ledger, Git subprocess in the resolver, or trust
record is introduced. Human repinning of `protected_test_roster.json` is a
separate Maintainer operation, not a plan chunk or a substitute for owed
agent checks and Security Reviews.

**Reuse.** Inspection of `tools/_intent/`, `tools/prune_intents.py` and
`tools/session.py` found the existing path leaf, `prune_released_pairs` guards
and `_read_git_pointer` checks. Mirror the pointer checks in one self-contained
claims resolver; use it from both tools. Keep shipped copies byte-identical.

### Documentation / doctrine surface

Coordination doctrine narrows the worktree limit; the shipped module explains
the same-clone sharing and mixed-version limitation. No other doctrine is
changed.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Resolver and guarded pruning | Both plan reviews folded; low-tier execution | Live and shipped claims/prune tools, tests |
| C2 | Session containment and doctrine | C1; serialize session twins with the 2b meter and 8b continuation owners before inspection through commit | Session twins, documentation and tests |
| C3 | Verification and review | C1-C2 complete | Iteration evidence, independent ordinary and Security code reviews, then final wide Boundary B |

## Acceptance criteria

**C1.** A main checkout uses its existing log. For a `.git` file, share only
when its absolute or relative `gitdir:` names `<common>/worktrees/<name>`,
`commondir` resolves to that common directory, its `gitdir` points back to
this checkout's `.git`, common is the real main checkout's `.git`, main
`dev/` already exists, and no component is a link or reparse point. Normalize
comparisons, including Windows drive letters. Otherwise retain the local log
and print a reason; never create a folder in another checkout. Keep
`INTENTS_LOG_PATH` computed once and patchable. The standalone prune tool has
the existing live-claim refusal, size recheck and link-safe temporary-file
guards; correct the single-checkout note in `record_io.py`.

Extend `bootstrap/tests/test_intents_tool.py` and
`bootstrap/tests/test_prune_tools.py`: exercise real main and linked tool
entry points, claim visibility, pre-commit recognition and post-commit
auto-release with both hooks installed. Cover relative and absolute pointers,
Windows-normalized drives, copied or mismatched pointers, submodule,
separate Git directory, bare repository, moved or missing main, missing `dev/`,
and links/reparse points at each relevant chain component. Every fallback
reports a reason and creates no outside folder. Test live claims, changed size
and hostile temporary links. In separate copies, mutations removing the
back-pointer check, link check, and no-folder-creation rule must each fail a
behavior test through the real entry point; record outcomes and omissions.

**C2.** Session-end pruning runs only in a main checkout; linked worktrees
skip with a note and all session writes remain contained. Extend
`bootstrap/tests/test_session_routines.py` and
`bootstrap/tests/test_session_writes_contained.py` to exercise that behavior.
Document that separate clones and machines remain separate, event logs do not
gain sharing, and an older tool on any branch silently uses its own claims
log. Serialize both session copies with 2b/8b owners; re-read their committed
changes before editing and preserve them.

**C3.** The implementation and shipped copies match byte-for-byte; mapped
checks, mutations, ordinary and Security code review and final integration
evidence pass. No scientific check is applicable. Any newly discovered trust
boundary stops for high-tier reassessment; this plan adds no new security
policy.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A: before implementation run `python tools/test_tiers.py for` with
every changed path, then run its named iteration list and applicable prose
gates. The current mapping selects 38 files, including
`bootstrap/tests/test_intents_tool.py`, `test_prune_tools.py`,
`test_session_routines.py`, `test_session_writes_contained.py` and shipped
copy/install checks; recalculate after edits and map consumers and omissions.
Run `python -m pytest bootstrap/tests/test_intents_tool.py bootstrap/tests/test_prune_tools.py bootstrap/tests/test_session_routines.py bootstrap/tests/test_session_writes_contained.py`
for the named behavior tests, plus the three isolated mutation checks. Use
`python scripts/claim_check.py` on changed prose and the applicable link,
snippet and neutrality gates. Check parity with `cmp` for each changed twin.

Boundary C: independent ordinary and Security code reviewers read the
committed implementation and iteration evidence, run only targeted
falsification checks, and identify missing coverage. Review fixes beyond a
failing test return to the same reviewer for a targeted look.

Boundary B: after review, use a clean unchanged final commit and canonical
Python 3.13.x, mode **wide** for the shared contract and protected surfaces.
Run the reviewed-range iteration list, named integration/workflow selections
from the tier map, standing prose gates and all acceptance and mutation
commands. Record full SHA and range, interpreter, clean pre/post state,
commands, counts, elapsed and tokens, non-pass dispositions, omissions and
timing misses; place files over ten seconds on the consolidation list. A
missing required check keeps work open. Tree certification and Maintainer
repinning remain separate ceremonies, not requested by this plan.
