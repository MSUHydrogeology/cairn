# Plan: Defect arc A, stale text

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: revising-plan
**Plan review**: required(Internal)
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/working-agreements.md, dev/rules/protected-surfaces.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: Docs and installed text that still name Cairn's old folders, give a command that fails in PowerShell, or break the prose check on a fresh clone are corrected, and the upgrade notes gain the 0.8 layout move.

## Build summary

After this plan, the quickstart's Windows steps work and list `RULES.md`; text that named the pre-0.8 folders names the real ones; the goodnight prune command is given for bash and for PowerShell; session start says what to run when `python` is not found; `python tests/check_cairn.py` exits 0 on a fresh clone; and `install/UPGRADE.md` describes the 0.7.0 to 0.8 layout move and the line-ending trap. The change is 35 exact replacements (42 applications) in 23 prose files, one changelog line and a refreshed install lock. No code, rule or status changes.

## Source proposal

The Maintainer accepted the defect arc at the heavy tier ("Go ahead on the defect arc.", chat, 2026-11-20). Plan A is its prose-only part and takes one usual plan review and one usual code review, with no Security Review pass. This plan executes it and reopens nothing. Opening it archives the proposal and its appendix, and repoints the live links: three in `dev/PLANNING.md`, and one citation in the archived one-round-reviews plan. The brief said the re-anchor plan also links to them; I found no link there.

## Scope

**Result.** Text an adopter or agent reads no longer sends them to a folder or command that fails. Items settled: #93; #97 fix 1; #98 part 4; the five prose-check failures; #99 part 2 and the stale-path item; the line-ending note for #95.

**Edit list.** The exact Find and Replace text is in `dev/plans/2026-11-20-defect-arc-a-stale-text-edits.md`, about 1,800 words, because a Low-tier implementer must design no wording. I checked each Find occurs exactly once in each target at `fea67042`, and applied the list to a scratch copy of that commit: all 42 applications matched, and `check_cairn.py` printed OK there. Shipped twins get identical text, and no shipped text names a model or vendor.

**Generated files.** The lock `dev/.cairn/cairn-lock.yml` is regenerated, not edited: `upgrade --finalize <paths>` advances four records (both session skills, `dev/modules/coordination-tiers.md`, `dev/plans/_template.md`). Cairn's own installed copies cannot be regenerated from their sources: a scratch `upgrade --plan` lists them review-only. So each takes the same exact edit as its source, as the one-round-reviews plan did. `dev/.cairn/base/` is never touched. `docs/code-map.md` is hand-written, and `sync_doc_snippets.py --check` is clean on the quickstart.

**Where the files contradict the brief.** (1) Issue #98 has four parts and #99 has four, so "#98.5" and "#99.5" are the arc's own items, not issue parts; close neither issue from this plan. (2) The shipped plan template already says `dev/tools/board.py`; only Cairn's own copy is stale (edit L19). (3) The PowerShell prune form ends with `Remove-Item Env:CAIRN_HANDOFF_OWNER`, which the issue's form lacks: it keeps the variable set for one run only, as bash does, so the guard keeps its meaning.

**Found, not fixed (Maintainer's call).** Python comments in about 34 files naming old folders go to plans B and C. `docs/DOCUMENTATION_PLAN.md` goes to plan E. Left alone: the licence file's folder names, `cairn/templates/` paths in the documentation-plan module and the contribution templates, a stale `test_command` in `dev/.cairn/profile.yml` (functional, plan B), and `scripts/` names inside the plan template's tooling slot.

**Must not change.** What any rule says. Every edit is a path or a command; Security Review is not needed.

**Reuse.** N/A: no code added.

### Documentation / doctrine surface

Quickstart, upgrade notes, four methodology pages, installed skills and module text, profile comments, changelog. No doctrine rule changes.

## Sequence

Low-tier implementer, the model named at spawn, in a worktree the coordinator names, as in the one-round-reviews plan: claim files, apply each edit with `dev/tools/exact_replace.py` (stop on a count other than one), commit once per chunk with explicit paths, never push. Chunks are independent; run in order.

| # | Chunk | Gate | Ships (edits; issues) |
|---|---|---|---|
| C1 | Quickstart | plan review accepted | `docs/quickstart.md` (Q1-Q4; #97) |
| C2 | Pre-0.8 folder names | C1 | 3 profiles, 2 install and methodology pages, 1 case-study comment, 4 methodology pages, `docs/code-map.md`, both `security-verification.md`, `dev/plans/_template.md` (L1-L19; #97, stale-path item) |
| C3 | Prune command, missing `python` | C2 | both session skills, both `coordination-tiers.md`, `session-routines.md` (R1-R4; #93, #98.4) |
| C4 | Prose check | C3 | session-start skill pair, `custom_session_routines.md`, the measurement README template, one measurement note (M1-M4; prose-check item) |
| C5 | Upgrade notes, changelog, lock, tests | C4 | `install/UPGRADE.md` (U1-U4; #99.2, #95 note), `CHANGELOG.md` (CL1), the lock |

## Acceptance criteria

**C1.** `git diff -U0` shows only the four Find texts removed and Replace texts added. The PowerShell column names `install\` three times and the commit prompt and `git add` line both list `RULES.md`. Developmental check, deleted afterward: the PowerShell column run once in a scratch folder on this Windows host (profile copy, preview, install) exits 0 and `git status` then shows no untracked `RULES.md`. Not run at opening.

**C2.** The sweep in Verification prints nothing. Twin pairs (`security-verification.md`) have identical added and removed lines. No Replace changes a word other than a path.

**C3.** `git grep -l -F '$env:CAIRN_HANDOFF_OWNER'` lists the five prune sites. Twin pairs match. The skill still says the agent does not run the prune, and the bash form is unchanged. The session-start skill tells a Windows reader what to run when `python` is not found and where its path is saved. I did not reproduce the message here.

**C4.** `python tests/check_cairn.py` exits 0 on the working tree (exits 1 with five issues today), and again on a fresh clone of the final commit. No Replace names the untracked meter export by a full path.

**C5.** `install/UPGRADE.md` has the new section with its known limit, "four sections" (U1, U2) and the Cairn-checkout line-ending note. `CHANGELOG.md` has one entry. After `upgrade --finalize` on the four paths, `install/verify_integrity.py --target .` prints OK for 70 files. The lock is committed alone. The new section was written from `install/_scaffold/upgrade.py` and issue #99, and no upgrade was run; the code reviewer checks it against `_layout_command`. Plan B owes a re-read of the line-ending note, since it changes that error and adds a `.gitattributes`.

## Scope delta

**Scope delta**: preserved. Every outcome the proposal assigns to plan A is delivered. The three items under "Found, not fixed" were never in plan A.

## Verification

**Promises.** Readers get correct paths and commands; the prose check passes on a fresh clone. Entry points: `python tests/check_cairn.py` and the edited text.

**Selector.** `C:\ProgramData\Anaconda3\python.exe tests/tier_inventory.py for <the 24 edited paths>` selects 58 test files at `fea67042`; `AGENTS.md` is not edited, so no `--range` is needed. Run those files once at the starting commit and keep the failing list (126 failures preceded one earlier change on this host, one real among them). Run them once more after C5. A failure is a host failure only if it is on the first list; any other is reported. Never set `CAIRN_FULL_SUITE=1`.

**Prose gates**, per changed `.md` file after each chunk, one file per call: `dev/tools/claim_check.py`, `dev/tools/link_check.py`, `tests/check_cairn.py`, plus `git diff --check`. Baseline: `claim_check.py` already fails on `dev/modules/security-verification.md` for a missing `run_security_verification.py` (2 flags); that is not new.

**Sweep (C2).** Prints nothing:

```
git grep -n -E "bootstrap[/\\]|cairn/(dimensions|on-ramp|bootstrap)|python (-I )?tools/" -- docs/quickstart.md install/profiles install/dimensions/human-team.md docs/methodology/coordination.md docs/methodology/session-routines.md docs/methodology/rationale.md docs/code-map.md docs/case-studies/modflow_tools-fidelity-manifest.yml dev/modules/security-verification.md templates/modules/default-on/security-verification.md dev/plans/_template.md
```

Known positive: add `-c` and `<BASE>` after the pattern; it lists 13 files at `fea67042`. It passes on the scratch copy.

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
