# Plan: Defect arc A, stale text

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: archived
**Plan review**: required(Internal)
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/working-agreements.md, dev/rules/protected-surfaces.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: Docs and installed text that still name Cairn's old folders, give a command that fails in PowerShell, or break the prose check on a fresh clone are corrected, and the upgrade notes gain the 0.8 layout move.

## Build summary

After this plan, the quickstart's Windows steps work and list `RULES.md`; text that named the pre-0.8 folders names the real ones; the goodnight prune command is given for bash and for PowerShell; session start says what to run when `python` is not found; `python tests/check_cairn.py` exits 0 on a fresh clone; and `install/UPGRADE.md` describes the 0.7.0 to 0.8 layout move and the line-ending trap. The change is 59 exact replacements (81 applications) in 32 files, one changelog line and a refreshed install lock. No code, rule or status changes.

## Source proposal

The Maintainer accepted the defect arc at the heavy tier ("Go ahead on the defect arc.", chat, 2026-11-20). Plan A is its prose-only part and takes one usual plan review and one usual code review, with no Security Review pass. This plan executes it and reopens nothing. Opening it archives the proposal and its appendix, and repoints the live links: three in `dev/PLANNING.md`, and one citation in the archived one-round-reviews plan. The brief said the re-anchor plan also links to them; I found no link there.

## Scope

**Result.** Text an adopter or agent reads no longer sends them to a folder or command that fails. Items settled: #93; #97 fix 1; #98 part 4; the five prose-check failures; #99 part 2 and the stale-path item; the line-ending note for #95.

**Edit list.** The exact Find and Replace text is in `dev/plans/archive/2026-11-20-defect-arc-a-stale-text-edits.md`, about 2,300 words, because a Low-tier implementer must design no wording. I checked each Find occurs exactly once in each target at `fea67042`, and applied the list to a scratch copy of that commit: all 42 applications matched, and `check_cairn.py` printed OK there. The plan review added 20 entries; the whole list, applied by script to a scratch copy of `3d7f3334`, gives 55 entries and 77 applications, each Find matching once, and `check_cairn.py` prints OK there. Shipped twins get identical text, and no shipped text names a model or vendor.

**Generated files.** The lock `dev/.cairn/cairn-lock.yml` is regenerated, not edited: `upgrade --finalize <paths>` advances seven records (both session skills, `dev/modules/coordination-tiers.md`, `dev/plans/_template.md`, `dev/modules/claim-check.md`, `dev/modules/content-security.md`, `dev/modules/doc-drift-prevention.md`). Cairn's own installed copies cannot be regenerated from their sources: a scratch `upgrade --plan` lists them review-only. So each takes the same exact edit as its source, as the one-round-reviews plan did. `dev/.cairn/base/` is never touched. `docs/code-map.md` is hand-written, and `sync_doc_snippets.py --check` is clean on the quickstart.

**Where the files contradict the brief.** (1) Issue #98 has four parts and #99 has four, so "#98.5" and "#99.5" are the arc's own items, not issue parts; close neither issue from this plan. (2) The shipped plan template already says `dev/tools/board.py`; only Cairn's own copy is stale (edit L19). (3) The PowerShell prune form ends with `Remove-Item Env:CAIRN_HANDOFF_OWNER`, which the issue's form lacks: it keeps the variable set for one run only, as bash does, so the guard keeps its meaning.

**Found, not fixed.** Python comments in about 34 files naming old folders go to plans B and C, and so does the bash-only hint in the refusal message at `dev/tools/session.py` line 2309 (plan C). `docs/DOCUMENTATION_PLAN.md` goes to plan E. A stale `test_command` in `dev/.cairn/profile.yml` is functional and goes to plan B, whose author was told. The `cairn/templates/` paths in the documentation-plan module and the contribution templates are correct, since a Cairn clone has `templates/`, and stay. The licence file named folders that no longer exist; the Maintainer settled that on 2026-11-20 (the next paragraph). The plan template's tooling slot and one profile comment, first left alone, are now fixed (T1 to T3, P1).

**Scope the Maintainer added (2026-11-20).** The licence notes `LICENSE-CC-BY.md` and `LICENSE-CC-BY-ND.md` say what kind of content each licence covers instead of listing folders, four of which no longer exist. Asked whether to correct the folder names, he wrote: "Instead of listing folders, say what the content is", and then chose the wording "By content, same licences". The licences do not change. Entries N1 to N4 are at the end of the edit list; they are applied after C5 as one more commit. Neither file is in the install lock or the gate manifest, and the selector names no test for them (measured). This addition gets one limited review of the added text, as "Review rules" says.

**Must not change.** What any rule says. Every edit is a path or a command; Security Review is not needed.

**Reuse.** N/A: no code added.

### Documentation / doctrine surface

Quickstart, upgrade notes, four methodology pages, installed skills and module text, profile comments, changelog. No doctrine rule changes.

## Sequence

Low-tier implementer, the model named at spawn, in a worktree the coordinator names, as in the one-round-reviews plan: claim files, apply each edit with `dev/tools/exact_replace.py` (stop on a count other than one), commit once per chunk with explicit paths, never push. Chunks are independent; run in order. Write the text between the fences, with no final newline, to two scratch files outside the repo; run `C:\ProgramData\Anaconda3\python.exe dev/tools/exact_replace.py <target> --old-file <old> --new-file <new>` per target; a count other than one stops.

| # | Chunk | Gate | Ships (edits; issues) |
|---|---|---|---|
| C1 | Quickstart | plan review accepted | `docs/quickstart.md` (Q1-Q4; #97) |
| C2 | Pre-0.8 folder names | C1 | 3 profiles, 2 install and methodology pages, 1 case-study comment, 4 methodology pages, `docs/code-map.md`, both `security-verification.md`, `dev/plans/_template.md`, three more module pages with their Cairn copies, one profile comment (L1-L19, S1a-S4b, T1-T3, P1; #97, stale-path item) |
| C3 | Prune command, missing `python` | C2 | both session skills, both `coordination-tiers.md`, `session-routines.md` (R1-R4; #93, #98.4) |
| C4 | Prose check | C3 | session-start skill pair, `custom_session_routines.md`, the measurement README template, one measurement note (M1-M4; prose-check item) |
| C5 | Upgrade notes, changelog, lock, tests | C4 | `install/UPGRADE.md` (U1-U4; #99.2, #95 note), `CHANGELOG.md` (CL1), the lock |

## Acceptance criteria

**C1.** `git diff -U0` shows only the four Find texts removed and Replace texts added. The PowerShell column names `install\` three times and the commit prompt and `git add` line both list `RULES.md`. Developmental check, deleted afterward: the PowerShell column run once in a scratch folder on this Windows host (profile copy, preview, install) exits 0 and `git status` then shows no untracked `RULES.md`. Not run at opening.

**C2.** The module sweep in Verification prints nothing. The pre-0.8 sweep prints one line after C2, the prune command at line 272 of `docs/methodology/session-routines.md`, which entry R3 corrects in C3; it prints nothing after C3. (Amended 2026-11-20 during implementation: as reviewed, this cell expected both sweeps clean after C2, but the last stale line in a C2 file is fixed by a C3 entry. Only the timing of the check changes.) Twin pairs (`security-verification.md`) have identical added and removed lines. No Replace changes a word other than a path.

**C3.** `git grep -l -F '$env:CAIRN_HANDOFF_OWNER'` lists the five prune sites. Twin pairs match. The skill still says the agent does not run the prune, and the bash form is unchanged. The session-start skill tells a Windows reader what to run when `python` is not found and where its path is saved. I did not reproduce the message here.

**C4.** `python tests/check_cairn.py` exits 0 on the working tree (exits 1 with five issues today), and again on a fresh clone of the final commit: `git -c core.autocrlf=false clone --no-hardlinks <repo path> <scratch>/fresh`, check out the final commit, run `tests/check_cairn.py` there; delete it. (Amended 2026-11-20 during implementation: on a Windows host whose Git converts line endings by default, a plain clone stops on the pinned-helper hash before the prose check reads anything, at the starting commit as well as after this plan. That is #95, which plan B fixes.) No Replace names the untracked meter export by a full path.

**C5.** `install/UPGRADE.md` has the new section with its known limit, "four sections" (U1, U2) and the Cairn-checkout line-ending note. `CHANGELOG.md` has one entry. After `python install/scaffold.py upgrade --target . --finalize <paths>` on the seven paths, `install/verify_integrity.py --target .` prints OK for 70 files. The lock is committed alone. At archive, CL1's link to this plan is repointed to the plan's archive path. The new section was written from `install/_scaffold/upgrade.py` and issue #99, and no upgrade was run; the code reviewer checks it against `_layout_command`. Plan B owes a re-read of the line-ending note, since it changes that error and adds a `.gitattributes`.

## Scope delta

**Scope delta**: preserved. Every outcome the proposal assigns to plan A is delivered. The three items under "Found, not fixed" were never in plan A.

## Verification

**Promises.** Readers get correct paths and commands; the prose check passes on a fresh clone. Entry points: `python tests/check_cairn.py` and the edited text.

**Selector.** `C:\ProgramData\Anaconda3\python.exe tests/tier_inventory.py for <the 31 edited paths>` selects 86 test files at `3d7f3334` (58 for the 24 paths before the plan review); `AGENTS.md` is not edited, so no `--range` is needed. Run those files once at the starting commit and keep the failing list (126 failures preceded one earlier change on this host, one real among them). Run them once more after C5. Run both times as `C:\ProgramData\Anaconda3\python.exe -m pytest -q -rf --tb=line -p no:cacheprovider <files>`, selector re-run at the starting commit. A failure is a host failure only if its test id and message are both on the first list; a listed id with a new message, or a new id, is reported. Never set `CAIRN_FULL_SUITE=1`.

**Prose gates**, per changed `.md` file after each chunk, one file per call: `dev/tools/claim_check.py`, `dev/tools/link_check.py`, `tests/check_cairn.py`, plus `git diff --check`. Baseline: `claim_check.py` already fails on `dev/modules/security-verification.md` for a missing `run_security_verification.py` (2 flags); that is not new.

**Sweep (C2).** Prints nothing:

```
git grep -n -E "bootstrap[/\\]|cairn/(dimensions|on-ramp|bootstrap)|python (-I )?tools/" -- docs/quickstart.md install/profiles install/dimensions/human-team.md docs/methodology/coordination.md docs/methodology/session-routines.md docs/methodology/rationale.md docs/code-map.md docs/case-studies/modflow_tools-fidelity-manifest.yml dev/modules/security-verification.md templates/modules/default-on/security-verification.md dev/plans/_template.md
```

Known positive: add `-c` and `<BASE>` after the pattern; it lists 13 files at `fea67042`. It passes on the scratch copy.

**Module sweep (C2).** Prints nothing:

```
git grep -n -E "target's .scripts/" -- templates/modules dev/modules
```

Known positive: it prints 14 lines at `3d7f3334`. It prints nothing on the scratch copy.

**Issues, for the Maintainer.** Nobody closes or comments on any: #93; #97 (fixes 2 and 3 are not in this arc); #98 (part 4 only); #99 (part 2 only); #95 (note only).

**Does any rule weaken or disappear?** No. The word limits are unaffected: none of the six governed files (`AGENTS.md`, `CLAUDE.md`, `RULES.md` and the three under `templates/core/`) is edited; counts stay 1,592 of 2,000 and 1,497 of 1,500 (`wc -w`).

## Plan review -- Claude Sonnet 5.5 (`claude-sonnet-5-5`, usual reviewer) -- 2026-11-20

```
Reviewed commit: a471308fbb9bd2d2fd0f54c404db20f5c507eaca
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE

The plan makes the paths and commands adopters read true in the 0.8 layout, by exact swaps. Mostly it does: I applied all 41 entries (42 applications) to a copy of the reviewed commit; each Find matched once, `tests/check_cairn.py` printed OK, the C2 sweep printed nothing, and the selector gives 58 files.

**Foundations**

1. **Should this happen as framed?** Yes, but it drops stale-path work the proposal gave plan A (finding 1) -- `git grep -n "scripts/" -- templates/modules`.
2. **Best alternative.** None simpler than one exact-edit list; finding 3 keeps it low-tier-safe -- the edit list.
3. **What would show it wrong.** A shipped module still naming `scripts/` after C5, or a baseline test id failing with a new message -- `git grep -n "target's .scripts/" -- templates dev/modules`.

**Does any rule weaken or disappear?** No. Every entry swaps a path or command; the PowerShell prune form works as written, and R4 matches `install.py` (`.git/cairn/local-env.json`) and `session.py` (the `interpreter` key).

**Findings**

1. **Blocking.** Four shipped module pages and their Cairn copies still tell adopters their tools land in `scripts/`, and cite `scripts/check_cairn.py` (16 places). This is the appendix's stale-path item. Entries S1-S4, T1-T3 and P1 follow; add them to C2, and add the three lock-tracked copies to the C5 `--finalize` list.
2. **Blocking.** U3's order is wrong. `_layout_plan` (`upgrade.py:4282`) blocks an unmatched copy with "unproved ancestry; reconcile", so a plain `--stage` exits 2 with no receipt; reconcile comes first, as in #99. Replace U3's steps 1-5 with the block below.
3. **Blocking.** Low-tier gaps. (a) Replace "A failure is a host failure only if it is on the first list; any other is reported." with: "Run both times as `C:\ProgramData\Anaconda3\python.exe -m pytest -q -rf --tb=line -p no:cacheprovider <files>`, selector re-run at the starting commit. A failure is a host failure only if its test id and message are both on the first list; a listed id with a new message, or a new id, is reported." (b) Add to Sequence: "Write the text between the fences, with no final newline, to two scratch files outside the repo; run `C:\ProgramData\Anaconda3\python.exe dev/tools/exact_replace.py <target> --old-file <old> --new-file <new>` per target; a count other than one stops." (c) C5: `python install/scaffold.py upgrade --target . --finalize <paths>`. (d) Fresh clone: `git clone --no-hardlinks <repo path> <scratch>/fresh`, check out the final commit, run `tests/check_cairn.py` there; delete it.
4. Non-blocking. CL1 links the live plan path; archiving must repoint it.

**Found, not fixed.** Licence file: its `dimensions/`, `bootstrap/*.md`, `on-ramp/` names no longer exist, so what it covers under `install/` is unclear (Maintainer's). `cairn/templates/` paths are correct (a Cairn clone has `templates/`); leave. `test_command`: plan B, but the proposal's B list omits it; tell B. Tooling slot: plan A (T1-T3).

**Not covered.** No test suite, no Windows run of the PowerShell column. I could not use a worktree (denied) and applied the list to an archive copy. Over target (about 520 words) to carry the exact fixes. Elapsed about 40 minutes; tokens unknown.

### Replacement U3 steps 1-5 (finding 2)

Replace, in entry U3's Replace text, the numbered steps 1 to 5 with:

````text
1. `python install/scaffold.py upgrade --target <repo> --plan` lists each move
   as `action: old -> new`. It writes nothing. A line that starts `blocked:`
   (for example "unproved ancestry") means the installer could not match an
   old copy to a Cairn release: do step 2 first. Without one, go to step 3.
2. `upgrade --target <repo> --stage --reconcile-layout <REV>` compares the old
   copies with the Cairn revision `<REV>` (the release the project was
   installed from, for example its tag) and prints `Apply to the same project
   with --apply --migration-receipt <digest>`. Run that printed command
   exactly; it ends with `Layout reconciliation complete.` Then run `--plan`
   again.
3. `upgrade --target <repo> --stage` stages the move and prints the same kind
   of `Apply to the same project ...` line.
4. Run that printed command exactly. It ends with `Layout migration
   complete.`
5. Now follow [The workflow](#the-workflow).
````

### Added entries (findings 1; same form as the edit list)

Each Find occurs once in each target at the reviewed commit (checked by script). Replace changes only the quoted path.

**S1** Targets: `templates/modules/default-on/claim-check.md`; `dev/modules/claim-check.md`. Find and Replace pairs, each `scripts/` to `dev/tools/` or `scripts/check_cairn.py` to `tests/check_cairn.py`:

- `scaffold installs as `claim_check.py` in the target's `scripts/`` -> `... in the target's `dev/tools/``
- `writes `claim_check.py` into the target's `scripts/` directory` -> `... `dev/tools/` directory`
- `allow.json, scripts/check_cairn.py,` -> `allow.json, tests/check_cairn.py,`
- `cites Cairn's own `scripts/check_cairn.py`` -> `... `tests/check_cairn.py``
- `on itself: `scripts/check_cairn.py` imports` -> `on itself: `tests/check_cairn.py` imports`

**S2** Targets: `templates/modules/team-gated/content-security.md`; `dev/modules/content-security.md`:

- `in the target's `scripts/` directory.` -> `in the target's `dev/tools/` directory.`
- `writes `content_scan.py` into the target's `scripts/`` -> `... `dev/tools/``
- `(installed beside the runner in `scripts/`)` -> `(installed beside the runner in `dev/tools/`)`

**S3** Targets: `templates/modules/team-gated/doc-drift-prevention.md`; `dev/modules/doc-drift-prevention.md`:

- ``scripts/` directory — `link_check.py`` -> ``dev/tools/` directory — `link_check.py``
- ``scripts/` directory:` -> ``dev/tools/` directory:`
- `When Cairn runs `scripts/check_cairn.py`` -> `When Cairn runs `tests/check_cairn.py``
- `citations) into the target's `scripts/`.` -> `citations) into the target's `dev/tools/`.`
- ``render_schema_docs.py` under `scripts/`` -> ``render_schema_docs.py` under `dev/tools/``
- Template only (the Cairn copy has no such line): `docs/methodology/, scripts/check_cairn.py,` -> `docs/methodology/, tests/check_cairn.py,`

**S4** Targets: `templates/modules/default-on/security-verification.md`; `dev/modules/security-verification.md`:

- ``run_security_verification.py` in the target's `scripts/` directory` -> `... `dev/tools/` directory`
- `target's `scripts/` directory (copied` -> `target's `dev/tools/` directory (copied`

**T1-T3** Target: `dev/plans/_template.md` (Cairn's filled slot): `` `python scripts/sync_doc_snippets.py` `` -> `` `python dev/tools/sync_doc_snippets.py` ``; `` `python scripts/check_cairn.py` `` -> `` `python tests/check_cairn.py` ``; `` `python scripts/link_check.py` `` -> `` `python dev/tools/link_check.py` ``.

**P1** Target: `dev/.cairn/profile.yml`: Find `` lockfile with `python bootstrap/scaffold.py upgrade --init-lock --target .` `` Replace `` lockfile with `python install/scaffold.py upgrade --init-lock --target .` ``. Not tracked in the lock; `bootstrap/scaffold.py` now only prints "Cairn moved" and exits 2.

C5 `--finalize` then covers seven paths: the four named plus `dev/modules/claim-check.md`, `dev/modules/content-security.md`, `dev/modules/doc-drift-prevention.md`.

## Plan response -- Claude Fable 5.2 (Strategy, for the author) -- 2026-11-20

The review said REVISE. Every finding is accepted, and each blocking one is closed with the reviewer's own words.

1. Blocking, stale `scripts/` text in four module pages, the plan template's tooling slot and a profile comment: accepted. Entries S1a to S4b, T1 to T3 and P1 are in the edit list under C2. The review gave them as short pairs, so each was written out in full and checked. C5's finalize list has seven paths.
2. Blocking, the order of U3's steps: accepted, with the reviewer's steps 1 to 5, copied by script from the review.
3. Blocking, four gaps for a low-tier implementer: accepted, each with the reviewer's words: the baseline rule, the `exact_replace.py` command, the finalize command and the fresh-clone check.
4. CL1's link at archive: accepted; C5 says so.

Found, not fixed, as the review sorted them: the `cairn/templates/` paths are correct and stay; `test_command` goes to plan B, whose author was told; the licence file is the Maintainer's and was put to him.

Checked after folding, by script: the whole list applied to a scratch copy of `3d7f3334` gives 55 entries and 77 applications in 30 files, each Find matching once; `tests/check_cairn.py` prints OK there; both sweeps print nothing. The selector now picks 86 test files for the 31 paths.

Not checked: no test ran, and the quickstart's PowerShell column was not run.

**Elapsed**: about 30 minutes. **Tokens**: unknown. The harness reported 210,989 tokens for the author and 159,834 for the review.

## Implementation verification -- Claude Haiku 5.5 (Implementation, Low) -- 2026-11-20

**BASE**: 02f92d37. Branch arc-a-impl. Plan header set to `implementing` in 19b13cec.

**Commits**
- 19b13cec: plan status to implementing (plan file only).
- edef620b, C1 quickstart (Q1-Q4, 4 applications). Gates: diff check, claim_check, link_check, check_cairn OK. PowerShell check below.
- 2c30f054, C2 pre-0.8 paths (57 applications, 19 files). Gates OK except the known `run_security_verification.py` flags (lines 18, 174, unchanged from HEAD). Module sweep empty; twins match.
- a91261da, C3 prune command and python fallback (7 applications). Pre-0.8 sweep empty. Gates OK; session-start pair reports `meter.json` at line 115, the M1 item of C4 (present at HEAD, line 110).
- 131b543f, C4 prose check (5 applications). Gates OK. Whole-tree `tests/check_cairn.py` exit 0 (221 files).
- 031c00ba, C5 upgrade notes and CL1 (U1-U4 by driver: 4 applications; CL1 by hand under a new Minor changes heading). Gates OK.
- 508dfb55, lock only: `upgrade --finalize` on the seven paths.

**PowerShell check (C1)**, run once in a new scratch folder, Anaconda first on PATH, $CAIRN = worktree: copy profile (Copy-Item sets no exit code; profile.yml created); `python install/scaffold.py --config profile.yml --target . --summary` exit 0; `... --target .` exit 0; RULES.md installed; `git status` in the worktree showed only ` M docs/quickstart.md`. Scratch folder deleted.

**Sweeps**: pre-0.8 path sweep after C2 printed one line (session-routines.md:272, R3); after C3 it prints nothing. Module sweep: nothing.

**Lock step**: `verify_integrity` before finalize: 7 modified files, exactly the seven named. After finalize: OK, 70 files.

**Fresh clone (C4 criterion)**: FAILED as run with the default Git config on this host. The clone has `core.autocrlf=true`; `tests/check_cairn.py` then stops with `RuntimeError: git-read-binding-failed` in `templates/modules/team-gated/link_check.py`, because the checked-out `dev/tools/git_read.py` hash (b6fad392...) differs from the pinned `_GIT_READ_SHA256` (b67deb4e...), which is the blob hash. With `git -c core.autocrlf=false clone`, the same commit prints `check_cairn: OK -- 221 Markdown file(s) scanned`. The clone was deleted in both cases. The plan's UPGRADE note already says to clone with autocrlf false.

**Did not match the plan**: (1) the C2 sweep, corrected by the coordinator in 2a31f804; (2) claim-check and check_cairn on the session-start pair at C3 (M1, expected until C4); (3) the fresh-clone failure above under default config.

**Not run**: the 86 selected test files (the coordinator runs them); no test set `CAIRN_FULL_SUITE`.

**Claims**: C1's claim was released with `--commit HEAD`, which ran before its commit, so it records 19b13cec. Later claims cite the real commit.

**Elapsed**: about 60 minutes. **Tokens**: unknown.

## Limited review of scope the Maintainer added -- Claude Sonnet 5.5 (usual reviewer) -- 2026-11-20

```
Reviewed commit: 96cca0ac
```

**Verdict**: ACCEPT. Findings: non-blocking only.

1. Each Find (N1 to N4) occurs exactly once in its target on the branch (checked by script).
2. The licences are unchanged. Exception 1, Exception 2 and the second note's three families are untouched, and the README section says the same thing. "Every explanatory diagram" leaves the brand mark under Exception 2, which names it as not CC BY; the eight listed diagrams are the only other files in `docs/assets/`. No file loses a licence a reader could tell.
3. N4 matches N3's "shipped Python tools" and reads correctly in its sentence.
4. After N1 to N4, no stale folder name remains in either note (grep for `scripts/`, `bootstrap`, `dimensions/`, `case-studies/`, `on-ramp`).

Non-blocking: N1's "everything written for people to read or adapt" reads as a rule, so a reader could take it to cover files the old list never named (for example `AGENTS.md` or `dev/` records). That is for the Maintainer to read; I give no view on the licences.

**Not covered**: no legal reading; I did not check other files that cite the old folder names.

**Elapsed**: about 10 minutes. **Tokens**: unknown.

## Coordinator verification -- Claude Fable 5.2 (Strategy) -- 2026-11-20

The implementer applied the edit list and stopped twice, as briefed: once on a check the plan had timed wrong, once on the fresh-clone check. Strategy settled both (the amended cells C2 and C4 say how), applied the scope the Maintainer added (N1 to N4, at `dbe9ba0d`, after the limited review), and ran the tests.

- **The edits.** The 30 files the first 55 entries target are byte for byte what a script produces by applying those entries to the starting commit (77 applications, each Find matching once).
- **Fresh clone.** A default clone on this Windows host fails before the prose check runs, at the starting commit too (measured): its Git converts line endings, and the pinned-helper hash then refuses. That is #95. With `core.autocrlf=false` the check prints OK for 221 files. Home for the default clone: plan B, chunk C1.
- **Tests and the 40-file guard.** One call of the 86 selected files was refused by Cairn's guard (`tests/conftest.py`). By chunk the selector gives 1, 73, 15, 40 and 10 files. The four selections that fit ran at `02f92d37` and at `f55360c1`, and each failure was compared by test id and message. C1: 2 passed at both. C3: the same 95 failures. C4: the same 310. C5: 161 failures at the start and 160 after. The one difference is a control case of a timeout test (`tests/test_portable_security_sweeps.py`, case `control-adapter-answers`): it failed once in the loaded run at the start, and passed in four reruns alone, at the start and after. No test fails only after the change. Commits after `f55360c1` change only this plan's two files and the two licence notes, which no test names.
- **C2's 73 files were not run.** By the guard's own rule that is a broad run, and it was not split to get under the limit. In its place: both sweeps are clean, twin files match, and a search of all 164 test files found none that holds any of the 44 changed lines. Home: the arc's joined run (`dev/PLANNING.md`, section 1, "Accepted on 2026-11-20").

Machine time for one run: C3 11 minutes, C4 57, C5 27. **Elapsed**: about 3 hours, nearly all of it background test runs. **Tokens**: unknown.

## Code review -- Claude Sonnet 5.5 (`claude-sonnet-5-5`, usual reviewer) -- 2026-11-20

```
Reviewed commit: 142b1377321ca36bfca5497786557fd957c2766d
Range: 02f92d37..142b1377
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised, non-blocking only
**Verdict**: ACCEPT

The change makes paths and commands that adopters read true in the 0.8 layout, by exact swaps. It does that. I applied all 59 entries (81 applications) by script to a `git archive` copy of the base commit. All 32 target files match HEAD byte for byte, and each Find matched once. The other four changed files are the changelog, the lock and this plan's two files.

**Foundations**

1. **Should this happen as framed?** Yes; the edits equal the list, twins carry identical text, and no added shipped text names a model or vendor -- my apply-and-compare script; `git diff 02f92d37..HEAD -- templates .agents install`.
2. **Best alternative.** None simpler than an exact-edit list; the lock commit `508dfb55` is alone and changes seven hash lines -- `verify_integrity.py --target .` prints OK for 70 files.
3. **What would show it wrong.** A stale folder name in the licence notes or module pages, or a test among the 42 unrun files failing -- `git grep -n -E "scripts/|bootstrap/" -- LICENSE-CC-BY.md LICENSE-CC-BY-ND.md templates/modules/*/*.md dev/modules` prints nothing.

**Does any rule weaken or disappear?** No. The prune, `python` and path edits only add the PowerShell form or a path; the licences keep their three families.

**Findings** (all non-blocking)

1. UPGRADE.md step 1 overstates: `blocked:` has other causes (`upgrade.py:4321`, "unlisted copy requires reconciliation"), which step 2 does not fix. Replace "A line that starts `blocked:` (for example "unproved ancestry") means" with "A `blocked:` line that says "unproved ancestry" means"; add after "do step 2 first." the words "Any other `blocked:` line names its own problem; fix that first."
2. Steps 2 and 4 say "Run that printed command exactly", but `upgrade.py:4533` prints only the flags. Say: "Run `upgrade --target <repo> --apply --migration-receipt <digest>` with that digest."
3. The Build summary still says 55 replacements, 77 applications and 30 files; the total is 59, 81 and 32.
4. The Known limit comes from issue #99, not from code I could confirm.

**The amendments** are sound, and homed: C2's timing (R3 is a C3 entry), and the default Windows clone in plan B, chunk C1.

**Tests.** The record settles C1, C3, C4 and C5. C2's 73 files were not run. Of them, 42 are in none of the four run selections, among them `test_profile_grammar`, `test_profiles_smoke`, `test_claim_check_module`, `test_security_verification` and `test_session_routines`. "No test holds a changed line" does not show those pass. The joined run is enough, if it runs the C2 selection. Bounding: ACCEPTED.

**Not covered**: no tests run; the licences; UPGRADE.md was read, not run. Over target to carry exact words. Elapsed about 40 minutes; tokens unknown.

## Code-review response -- Claude Fable 5.2 (Strategy, acting as implementer) -- 2026-11-20

Strategy coordinated this plan and answers; the implementing session (Claude Haiku 5.5) had ended. The review raised no blocking finding. Its four notes are cheap, so each is settled here, before archive.

- **1, step 1 of the new upgrade section: fixed** (`b9174bb9`) with the reviewer's words. One more change is Strategy's: "Without one" became "With no `blocked:` line", because the added sentence made "one" unclear.
- **2, "Run that printed command exactly": fixed** (`b9174bb9`) with the reviewer's command, plus eight words of Strategy's: "adding `--to <id>` if the line shows it". The printed line carries `--to` when the stage was given one (`install/_scaffold/upgrade.py`, `_layout_command`), and an apply without it is refused because the receipt no longer matches (`install/_scaffold/layout_migration.py`, `Transaction.apply`). Without those words the fix would have dropped what "exactly" protected.
- **3, the counts: fixed** (`27d82896`). The Build summary says 59, 81 and 32. Entry U3 of the edit list holds the corrected section, so the list, applied by script to `02f92d37`, still equals this branch in all 32 files.
- **4, the Known limit: kept, and now confirmed from code.** A file with unproved ancestry is printed as `blocked:` and not as a move (`_layout_plan`, the `if not old_proved` branch); reconciling records it as "keep"; only the next `--plan` lists its move.

**Tests after the fix.** The ten files that name `install/UPGRADE.md` ran again at `27d82896`: 161 failed, 429 passed, 50 skipped, against 160, 430 and 50 at `f55360c1`. One id is new, `tests/test_portable_security_sweeps.py::test_full_mode_is_unreachable_without_a_digest_match[mismatched_digest]`. It passed three times alone at `27d82896`; other agents were loading the machine during the full run, and another case in the same file failed once in a loaded run earlier today. Every other failing id and message is unchanged. No file under `tests/` holds a phrase the fix changed (text search).

**The reviewer's condition is accepted.** Chunk C2's 73-file selection, with the 42 files no group covered, is owed by the arc's joined run. Home: `dev/PLANNING.md`, section 1, "What the joined run owes".

Not run after the fix: the quickstart's PowerShell column and `upgrade.py` itself. Not read by a second reviewer: the words Strategy added in 1 and 2. The reviewer wrote "about 40 minutes"; its commit followed the reviewed commit by under three minutes.

**Elapsed**: about 36 minutes, of which 27 were one background test run. **Tokens**: unknown.

## Implementation closeout -- Claude Fable 5.2 (Strategy) -- 2026-11-20

Every criterion held, two of them as amended during implementation. C1: the quickstart's PowerShell column ran once in a scratch folder (each installer command exit 0, `RULES.md` installed). C2, as amended: both sweeps print nothing after C3, and twin files match. C3: the PowerShell prune form is at the five sites, measured on the merged tree. C4, as amended: `tests/check_cairn.py` exits 0 on the merged tree (226 files) and on a fresh clone that keeps line endings (221 files at `f55360c1`). C5: the upgrade notes hold the layout section as corrected at code review; the lock was committed alone (`508dfb55`) and `verify_integrity` reports OK for 70 files on the merged tree; CL1's link is repointed in this commit. The licence notes the Maintainer added are in (`dbe9ba0d`, after the limited review `d3f5d179`). The branch, 18 commits changing 36 files, merged into `0.9-dev` at `d35243f1` with no conflict.

Not run: the 73 test files chunk C2 selects, 42 of them in no group that ran. Home: `dev/PLANNING.md`, section 1, "What the joined run owes".
Not run: the selected tests on the canonical runtime. Home: `dev/PLANNING.md`, section 1, "What the joined run owes".
Not covered: the default Windows clone, which stops on #95 before the prose check runs. Home: `dev/plans/2026-11-20-defect-arc-b-upgrading.md`, chunk C1.
Not covered: the tests that fail on the Windows Server host before and after (95, 310 and 160 in three groups), and two cases of `tests/test_portable_security_sweeps.py` that each failed once while the machine was loaded. Home: `dev/PLANNING.md`, section 1, "Windows".
Remaining: a re-read of the line-ending note in `install/UPGRADE.md`. Home: `dev/plans/2026-11-20-defect-arc-b-upgrading.md`, chunk C5.
Remaining: comments that name old folders. Home: `dev/plans/2026-11-20-defect-arc-b-upgrading.md` and `dev/plans/2026-11-20-defect-arc-c-first-session-and-tools.md` for the files they edit, and `dev/PLANNING.md`, section 1, "Comments in protected files", for the seven frozen tools.

Dispositions: the scope the Maintainer added is `accept`, with his words quoted in Scope. The code review's notes 1 to 3 are `accept` (fixed) and note 4 is `accept` (confirmed from code, no change). No follow-up is deferred.

**Benefit versus cost**: unknown -- readers of the quickstart, the upgrade notes and the installed text are no longer sent to a folder or command that fails (#93, #97 fix 1, #98 part 4, #99 part 2); cost: 18 commits and one merge, one plan review, one limited review of added scope and one code review with no return visit, about 0.81 million subagent tokens in five runs as the harness reported them (Strategy's own use is unknown), and about 3.6 hours of machine time in background test runs on one host; remaining burden: no code and no test added. Revisit at the D6 recount at the end of v0.9.

**Elapsed**: three hours from the plan's opening (15:53) to the merge (18:52). **Tokens**: unknown beyond the subagent figure above.
