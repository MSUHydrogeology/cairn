# Share work-intent claims across a clone's worktrees

**Author**: Claude Opus 5.5 (Implementation investigation; Strategy)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy -- it changes the shipped coordination module, a named high-risk template surface
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-03
**In brief**: Make every checkout of one repository read and write the same claims log, so sessions in separate worktrees see each other's claims and the commit hooks check the right log.

## Decision summary

Cairn recommends separate worktrees as the cure for shared-tree collisions,
but its claims log is per checkout. A session claiming files in a second
checkout writes to that checkout's log. The commit hooks read the main
checkout's log, so they report "no active claim" and never auto-release the
claim. Sessions in different checkouts cannot see each other's claims at all.

Proposal: every checkout of one clone uses the main checkout's
`dev/intents.jsonl`. The tool finds that file by reading Git's own pointer
files, without running `git`.

Cost: a small change to the claims tool and its shipped copy, tests, and two
doctrine paragraphs. It changes a high-risk surface, so it needs a Security
Review.

## Context

- **Measured, 2026-11-03.** In the linked worktree
  `/private/tmp/cairn-v07-development` (branch `0.7-dev`), I ran
  `python tools/intent.py claim --files dev/proposals/2026-11-03-claude-leaner-reviews.md dev/PLANNING.md`.
  - The claim recorded with no overlap.
  - The commit of those paths then printed "staged path(s) with no active
    claim" and did not auto-release the claim; I released it by hand.
  - The two logs are different files: the main checkout's (about 1 MB) and
    the worktree's (about 3 KB).
- **Cause, read from code.**
  - The installed hooks run the installing checkout's tool by absolute path
    (`.git/hooks/pre-commit`, `.git/hooks/post-commit`). Git keeps hooks in
    the shared folder, so every worktree runs them.
  - The tool finds its log relative to its own location: `_REPO_ROOT =
    Path(__file__).resolve().parents[2]` in `tools/_intent/shared.py`.
    `tools/prune_intents.py` repeats that rule.
  - So the hooks always use the main log, and a command run inside a
    worktree uses the worktree's log.
- **Doctrine already names the gap.** `docs/methodology/coordination.md`,
  "Scope and limits":

  > "Untracked work-intent and event-log files are visible only within one
  > shared working tree. Multiple worktrees need a shared sidecar location
  > ... A concurrency ladder must not recommend per-domain worktrees and then
  > break the coordination mechanism it just introduced."

  Yet `templates/modules/team-gated/coordination-tiers.md` calls separate
  worktrees "the root-cause cure".

## Proposal

1. **One log per clone.** A single resolver in `tools/_intent/shared.py`,
   used by the claims tool, `tools/prune_intents.py` and their shipped
   copies, returns the shared log:
   - In the main checkout, nothing changes: `dev/intents.jsonl`.
   - In a linked worktree (its `.git` is a file), it reads `gitdir:` from
     that file and `commondir` from the worktree's administration folder.
     When the common folder is the main checkout's `.git` directory, the log
     is that checkout's `dev/intents.jsonl`.
   - Anything else falls back to the checkout's own log and prints a
     one-line note naming the reason. This covers a bare repository, an
     unreadable or malformed pointer, and a main checkout that is missing.
     Behavior is then exactly today's.
2. **No `git` subprocess.** The resolver reads two small text files, so
   repository-configured Git behavior (such as filesystem monitors or hooks)
   never runs.
3. **Refuse links.** If the resolved log, its `dev` folder or the pointer
   files are symbolic links, the resolver falls back and says so.
4. **Paths stay repository-relative.** Claims name files relative to the
   repository root, which is the same in every checkout, so claims compare
   across checkouts without translation.
5. **Doctrine and module text.** The worktree limit in `coordination.md`
   narrows to multiple clones and machines. `coordination-tiers.md` says
   that worktrees of one clone share claims.

Unchanged: the collision log `dev/measurement/collision_log.md` stays per
checkout, because it is measurement, not coordination. Readers that name
`dev/intents.jsonl` only as a path (the `.gitignore` entry, claim-check
exemptions, scaffold text) need no change. The plan confirms the reader in
`bootstrap/_scaffold/config.py` near line 1141.

## Rationale

The main checkout's log already holds the history, and its location is
documented. Pointing worktrees at it adds no new location, needs no
migration, and keeps the main checkout byte-for-byte as today. Reading Git's
pointer files instead of running `git` keeps the claims tool free of
repository-configured programs.

## Alternatives considered

- **A sidecar in Git's common folder** (for example
  `.git/cairn/intents.jsonl`). It is cleaner for bare repositories, but it
  moves the log, needs a migration, and changes every documented path.
- **Hooks call the committing checkout's own tool.** That makes each
  checkout consistent with itself, but sessions in different worktrees still
  cannot see each other: it fixes the warning and keeps the hazard.
- **Do nothing.** The doctrine keeps recommending worktrees while the
  mechanism silently splits, and hook warnings in worktrees stay false.

## Documentation / doctrine surface

- **Doctrine:** `docs/methodology/coordination.md`, Scope and limits.
- **Shipped module:** `templates/modules/team-gated/coordination-tiers.md`
  and the module's `_intent/` and `prune_intents.py` copies. The doctrine
  rate-limit gate applies.

## Evidence / verification plan

- **Tests**, with temporary repositories, each with a linked worktree:
  - a claim made in the worktree is seen by the main checkout's tool and by
    its pre-commit check;
  - the post-commit hook auto-releases it;
  - pruning works across both checkouts;
  - each fallback case keeps today's per-checkout log and prints its note;
  - linked pointer files or folders are refused.
- **Existing tests:** the plan maps the claims-tool families with `python
  tools/test_tiers.py for`, and the shipped-copy parity checks.
- **Security preflight:**
  - S1: the inputs are two Git pointer files inside the repository's own
    administration folder; nothing outside the clone supplies them.
  - S2: removing the link refusal must fail a test.
  - S3: the resolver runs on every claims-tool call; tests cover the
    main-checkout, worktree and fallback paths.
  - S4: every malformed input falls back to today's per-checkout log, which
    is no more authority than now.
  - S5: a process that can already write the `.git` folder can redirect the
    log within the filesystem. That is unchanged, because it can already
    rewrite hooks.
- **Independent scientific check:** N/A, no scientific assumption touched.

## Signals the change is wrong

- Claims made in a worktree still do not appear in the main checkout's
  list.
- Hooks still warn "no active claim" for paths claimed in a worktree.
- The fallback note appears on ordinary worktrees.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance -- it changes a shipped module and the
coordination doctrine.

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
