# Share work-intent claims across a clone's worktrees

**Author**: Claude Opus 5.5 (Implementation investigation; Strategy)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy -- it changes the shipped coordination module, a named high-risk template surface
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-03
**In brief**: Make every checkout of one repository read and write the same claims log, so sessions in separate worktrees see each other's claims and the commit hooks check the right log.

## Decision summary

Cairn recommends separate worktrees to avoid shared-tree collisions, but its
claims log is per checkout. A session claiming files in a second checkout
writes to that checkout's log. The commit hooks read the main checkout's log,
so they report "no active claim" and never auto-release. Sessions in
different checkouts cannot see each other's claims.

Proposal: every linked worktree of one clone uses the main checkout's
`dev/intents.jsonl`, but only when Git's own pointers prove the worktree
belongs to that clone. Anything else keeps today's per-checkout log and says
so.

Cost:
- a resolver in the claims tool and its shipped copy;
- matching changes to pruning and the session routines;
- tests and two doctrine paragraphs;
- re-pinning the shipped files, which the Maintainer does;
- a Security Review, because it changes a high-risk surface.

## Context

- **Measured, 2026-11-03.** In the linked worktree
  `/private/tmp/cairn-v07-development`, a claim recorded with no overlap.
  The commit of those paths then printed "staged path(s) with no active
  claim" and did not auto-release. The two logs are different files. Both
  reviewers reproduced this; the usual review did so in a throwaway
  repository.
- **Cause, read from code.**
  - The hooks live in Git's shared folder and run the installing checkout's
    tool by absolute path.
  - The tool finds its log from its own location: `_REPO_ROOT` in
    `tools/_intent/shared.py`. `tools/prune_intents.py` repeats that.
  - `tools/session.py` prunes through the checkout's own tool and promises
    that "every write is contained" in that checkout.
  - Its goodnight lock is per checkout (`_state_dir(root)`).
- **Doctrine already names the gap.** `docs/methodology/coordination.md`,
  "Scope and limits":

  > "Untracked work-intent and event-log files are visible only within one
  > shared working tree. Multiple worktrees need a shared sidecar location
  > ... A concurrency ladder must not recommend per-domain worktrees and then
  > break the coordination mechanism it just introduced."

  Yet `templates/modules/team-gated/coordination-tiers.md` calls separate
  worktrees "the root-cause cure".
- **A careful pointer reader exists.** `tools/session.py`
  (`_read_git_pointer` and the check before it) already reads a `.git`
  pointer, refuses links anywhere in the path, and cross-checks the
  administration folder.

## Proposal

1. **One resolver**, used by the claims tool, `tools/prune_intents.py` and
   their shipped copies. `INTENTS_LOG_PATH` stays a module value computed
   once, so existing tests that patch it still work.
   - In a main checkout (`.git` is a directory), nothing changes:
     `dev/intents.jsonl`.
   - In a linked worktree, it uses the main checkout's log only if all of
     these hold:
     - the `.git` file's `gitdir:` (absolute or relative) names an
       administration folder at `<common>/worktrees/<name>`;
     - that folder's `commondir` resolves to `<common>`;
     - its `gitdir` file points back to this checkout's `.git`;
     - `<common>` is a real `.git` directory inside its parent, the main
       checkout;
     - the main checkout's `dev/` folder already exists, and the tool never
       creates folders there;
     - no part of any of these paths is a link or reparse point.

     Path forms are compared after normalization, including Windows drive
     letters.
   - Anything else falls back to today's per-checkout log and prints one
     note naming the reason. That includes submodules,
     `--separate-git-dir` checkouts, bare repositories, a moved or missing
     main checkout, a main checkout with no `dev/`, and any failed check.
2. **Mirror, don't import.** The resolver mirrors the `session.py` pointer
   checks inside the claims module, which stays self-contained. It adds no
   `git` subprocess, although the tool already runs `git` elsewhere.
3. **Pruning.**
   - Session-end pruning runs only in a main checkout. In a linked worktree,
     it skips with a note, which keeps the containment promise.
   - `tools/prune_intents.py` gains the same guards as `intent.py prune`:
     refuse while a claim is active, re-check the size, and never follow a
     link when writing its temporary file.
   - The "single-checkout file" note in `record_io.py` is corrected.
4. **Doctrine and module text.**
   - The worktree limit in `coordination.md` narrows to separate clones and
     machines.
   - `coordination-tiers.md` says that worktrees of one clone share claims,
     but only when every worktree's branch carries the updated tool. A branch
     with the older tool keeps its own log silently.

## Rationale

The main checkout's log already holds the history, and its location is
documented. Pointing worktrees at it needs no migration and leaves the main
checkout as it is today. Requiring Git's back-pointer to match, and never
creating folders, keeps a copied or crafted pointer from sending claims into
another repository.

## Alternatives considered

- **A sidecar in Git's common folder**, as `session.py` already does for its
  binding file. It needs no main checkout, but it moves the log and needs a
  migration. It is reasonable if the Decision prefers one location
  everywhere.
- **Ask `git rev-parse --git-common-dir`.** Simpler code, but it runs
  repository-configured Git on every claims call, and it does not perform
  the back-pointer check.
- **Hooks call the committing checkout's tool.** That fixes the false
  warning, but sessions in different worktrees still cannot see each other.
- **Do nothing.** The doctrine keeps recommending worktrees while
  coordination silently splits.

## Documentation / doctrine surface

- **Doctrine:** `docs/methodology/coordination.md`. The rate-limit gate
  applies.
- **Shipped module:** `templates/modules/team-gated/coordination-tiers.md`,
  the module's `_intent/` and `prune_intents.py` copies.
- **Session reader:** the shipped copy of `tools/session.py`, for the
  worktree prune skip.
- **Pins:** the shipped files are hash-pinned in
  `protected_test_roster.json`. Re-pinning is the Maintainer's step.

## Evidence / verification plan

- **Tests**, using temporary repositories, each with a linked worktree:
  - a claim made in the worktree is seen by the main checkout's tool and by
    both hooks, which auto-release it;
  - relative pointers work;
  - each fallback prints its note: a submodule, `--separate-git-dir`, a bare
    repository, a moved main checkout, no `dev/`, a copied worktree folder
    whose back-pointer does not match, and a link anywhere in the chain;
  - no fallback creates a folder outside its checkout;
  - session-end prune skips in a worktree;
  - `prune_intents.py` refuses while a claim is active and does not follow a
    link.
- **Existing tests:** the plan maps the claims-tool families,
  `test_session_writes_contained.py`, `test_session_routines.py` and the
  shipped-copy parity checks with `python tools/test_tiers.py for`.
- **Security preflight:**
  - S1: the `.git` pointer sits in the working tree, so on its own it is not
    trusted. The resolver accepts it only when Git's back-pointer in the
    administration folder agrees.
  - S2: removing the back-pointer check, the link check or the
    no-folder-creation rule must each fail a test.
  - S3: the resolver runs on every claims-tool call; tests cover every path
    above.
  - S4: every check failure keeps today's per-checkout log, which is no more
    authority than now. A split remains possible when a branch carries the
    older tool, and it is documented.
  - S5: whoever can forge both pointers can already make Git run their
    hooks. `bootstrap/SAFETY.md` records that as accepted.
- **Independent scientific check:** N/A, no scientific assumption touched.

## Signals the change is wrong

- Claims made in a worktree still do not appear in the main checkout's list.
- The fallback note appears on ordinary worktrees.
- A prune is blocked by another worktree's claim.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance -- it changes a shipped module, a session
reader and the coordination doctrine.

## Review -- Claude Sonnet 5.5 -- 2026-11-03

```
Reviewed commit: 3ec48d63
Target: whole proposal
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: about 12 minutes
**Tokens**: about 120,000 (estimate)

**Foundations**

1. **Should this happen as framed?** Yes. Reproduced in a throwaway repository: a claim made in a linked worktree landed in the worktree's log, and the post-commit hook ran the other checkout's tool and left it unreleased -- `tools/_intent/shared.py` line 22.
2. **Best alternative.** A sidecar in Git's common folder; it needs no main checkout, and `tools/session.py` line 1060 already keeps a file under Git's `cairn/` folder. The main-checkout log stays lighter if the fallbacks below close.
3. **What would show it wrong.** A fallback note on an ordinary checkout, or a prune blocked by another worktree's claim.

**Findings** (none blocking)

- **F1. Session routines missing.** `tools/session.py` lines 1787-1820 (`_prune_intents`) is pinned to the root's own ledger, under a header promising contained writes (line 26). A worktree prune would rewrite the main log, and `prune` refuses while any claim is active. Close: name `session.py` and its two tests (`test_session_writes_contained.py`, `test_session_routines.py`); state how containment changes; say whether `INTENTS_LOG_PATH` stays constant.
- **F2. "No `git` subprocess" is overstated.** `conflict.py` line 179 and `hooks.py` line 141 already run `git`; `session.py` line 1068 already reads `.git` pointers and refuses links. Close: reword; reuse or mirror that reader.
- **F3. Trigger too wide.** Submodule and `--separate-git-dir` checkouts also have a `.git` file. Key on `commondir` and a `worktrees/` parent; cover relative `gitdir:` values and Windows drive paths.
- **F4. S1 overstated.** The `.git` file sits in the working tree, not Git's folder. Close: check the back-pointer `worktrees/<name>/gitdir`.
- **F5. Missing fallback.** Main checkout exists but lacks `dev/`; `record_io.py` line 147 would create it.

**Coverage.** No tests run; Windows and submodules unprobed.

## Review -- Claude Opus 5.5 (Security Review) -- 2026-11-03

```
Reviewed commit: 3ec48d63c0f07df1d575858179ad4649500e7529
Target: Proposal, Security preflight S1-S5
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: ~30 min
**Tokens**: ~100,000 (estimated)

**Foundations**:

1. **Should this happen as framed?** Yes. Hooks miss worktree claims, and doctrine names the gap -- `tools/_intent/shared.py:22`; `coordination.md` "Scope and limits".
2. **Best alternative.** Ask Git (`git rev-parse --git-common-dir`). The engine already runs `git` on the hook path, so point 2 buys less than stated -- `tools/_intent/conflict.py` lines 183 and 738.
3. **What would show it wrong.** A well-formed pointer sending appends into another repository, or one checkout's prune dropping another's claim -- F1, F3.

None blocks (all reversible); F1 and F3 should be fixed before the plan.

- **F1.** S4 covers malformed pointers, not well-formed wrong ones. A copied worktree folder, or `commondir` naming another repository's `.git`, resolves cleanly, and `append_record` then creates `dev/` there (`record_io.py:147`). Close: require the administration folder at `<common>/worktrees/<name>`, its `gitdir` back-pointer equal to this `.git`, `<common>` the main checkout's real `.git`, and `<main>/dev` already present; check links on every path component, as `_read_git_pointer` does (`tools/session.py:1063`); test each.
- **F2.** Fallback still splits silently where a worktree's branch carries an older tool. Close: state that limit in `coordination-tiers.md`; test relative pointers (git 2.53.0 writes them under `worktree.useRelativePaths`, measured) and submodules, so ordinary layouts print no note.
- **F3.** The handoff lock is per checkout (`session.py:1655`), so it no longer serializes prune against other worktrees' appends. `prune_intents.py` lacks the live-claim refusal and size re-check, and its `.tmp` open follows links (`:192`). Close: retire it or add `prune_released_pairs`' guards; correct the "single-checkout file" docstring (`record_io.py:343`).
- **F4.** S1 is inaccurate: the `.git` file sits in the working tree. S5 still holds: a forged pointer already makes Git run attacker hooks (`bootstrap/SAFETY.md`, "Git administration ... trusted inputs").

Append contention adds no new kind: same `O_APPEND` write, 512-byte cap. The plan should name repinning `protected_test_roster.json`.

**Coverage**: not checked: resolver code (none yet), Windows junctions, network or container filesystems.

## Response -- Claude Opus 5.5 -- 2026-11-03

All findings accepted; operative text revised in place.

- **Usual F1 (session routines):** session-end pruning runs only in a main
  checkout and skips with a note in a worktree, which keeps `session.py`'s
  containment promise. The tests are named. `INTENTS_LOG_PATH` stays a
  patchable module value.
- **Usual F2 (subprocess claim):** reworded. The resolver mirrors the
  `session.py` pointer checks; the tool already runs `git` elsewhere.
- **Usual F3 (trigger too wide):** the trigger keys on
  `<common>/worktrees/<name>` plus `commondir`. Submodules and
  `--separate-git-dir` fall back. Relative pointers and Windows drives are
  covered.
- **Usual F4 and Security F4 (S1):** S1 is corrected. The back-pointer must
  match, and S5 cites `SAFETY.md`.
- **Usual F5 and Security F1 (wrong pointer):** all five resolver conditions
  are required, each with a test. A missing `dev/` falls back, and the tool
  never creates folders in another checkout.
- **Security F2 (silent split):** documented in `coordination-tiers.md`,
  with tests that the note does not fire on ordinary layouts.
- **Security F3 (pruning):** `prune_intents.py` gains the claim, size and
  no-link guards. The `record_io.py` note is corrected.
- **Security plan cost:** re-pinning `protected_test_roster.json` is named
  as the Maintainer's step.

**Elapsed**: about 20 minutes. **Tokens**: unknown.

### Withdrawn / superseded commitments

- "No `git` subprocess" as a benefit, replaced by "mirrors `session.py`; adds
  no new `git` call" (usual F2).
- S1's claim that the pointer files sit in Git's administration folder
  (usual F4, Security F4).
