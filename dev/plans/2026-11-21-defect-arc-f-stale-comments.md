# Plan: Defect arc F, stale comments in protected tools

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: awaiting-code-review
**Plan review**: required(Internal)
**Opened**: 2026-11-21
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/certifying-runs.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: Sixteen comment lines in eleven copies of seven tools still name folders that no longer exist, and this plan corrects only those comments, leaving every line of working code unchanged.

## Build summary

After this plan, no `#` comment in the seven tools names `bootstrap/`, `scripts/` or an old `tools/` folder. Only comment text changes. Each of the eleven files must parse to exactly the same syntax tree as before, so nothing the tools do can change. Cairn's own install lock is refreshed in a commit of its own. The Maintainer sees eleven more lines at the signing, one for each changed file.

## Source proposal

The accepted defect arc counts comment text in tool files among the stale paths of issue #99. Plans A to E left one group of such comments alone, because each file is frozen in the gate manifest and a correction adds a line for the Maintainer to approve. The roadmap entry "Comments in protected files" records the question. The Maintainer chose "Fix them all now" on 2026-11-21. This plan carries that out and ships in v0.8.1.

## Scope

**What changes.** Sixteen `#` comment lines in eleven file copies. I re-found them on 2026-11-21 with a text search (`git grep -nP` on comment lines naming `scripts/`, `bootstrap/` or `tools/` without a `dev/` or `install/` before it) and confirmed them with Python's tokenizer, which lists only comment tokens. The count matches the roadmap: sixteen lines, eleven copies. The old text and the corrected text of every line are in [the detail file](2026-11-21-defect-arc-f-stale-comments-detail.md); it is separate only because sixteen old-and-new pairs do not fit the opening body. The seven tools are `install/check_module_body_coverage.py`; `claim_check.py`, `content_scan.py`, `content_scan_runner.py` and `run_portable_security_sweeps.py`, each in `templates/modules/` and in `dev/tools/`; the shipped `run_security_verification.py`; and the shipped `api_access_security.py`.

**What does not change.** Any token that is not a `#` comment. Docstrings and string literals that name an old folder stay, because editing them changes the syntax tree. One comment is left alone on purpose: `_intent/shared.py` line 19 (both copies) names both the old and the current folder, and its code handles both. It is not one of the seven tools.

**Twins.** The four tools that have two copies are byte-identical today (`cmp` checked on 2026-11-21 for each pair) and must stay so. The shipped `run_security_verification.py` and `api_access_security.py` have no copy in `dev/tools/`. `install/check_module_body_coverage.py` is a single file.

**Frozen, not protected.** Protected-surfaces names `run_portable_security_sweeps.py` and its shipped copy as high-risk. All eleven copies are frozen in `tests/fixtures/gate_manifest.json` (the manifest lists Cairn's own four under their pre-layout `scripts/` paths and the check-coverage tool under `bootstrap/`). Each is also listed in the manifest's `protected_roster` under `preserved_non_test_frozen_paths`; none is in `protected_python_paths`. Changing any of them makes the manifest's recorded hash stale; the Maintainer's signing refreshes it, and no agent does. The signing's one sentence is: "Eleven frozen tool files changed only in comments naming old folders; each parses to the same syntax tree as before." Cairn's own lock (`dev/.cairn/cairn-lock.yml`) records the four `dev/tools/` copies, so those four hashes go stale too; the Implementation agent refreshes them in C2.

**Review.** Protected-surfaces gives the heavy tier to a change that alters what a high-risk surface does or accepts, and says that merely touching a surface does not. A comment cannot alter what a tool does, and the syntax-tree check below proves for every copy that no code changed. So this plan takes the usual review at each stage: one plan review and one code review. The code reviewer re-runs the syntax-tree check and the stale-comment search, and reads the diff for any token that is not a comment. The author first took the heavier tier, as its brief told it to wherever the rules left a choice; Strategy set this one on 2026-11-21, because the rule leaves none here. The Maintainer still sees each changed frozen file at the signing.

No new script, option or test file is added (Maintainer, chat, 2026-11-21: "Yeah no new tooling unless it's needed!"). **Reuse**: N/A: no code added.

Doctrine surface: none.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Edit the sixteen lines in the eleven files; check trees, twins and the search | plan review | one commit, eleven files |
| C2 | Refresh Cairn's own lock with the installer | C1 | one commit holding only the lock |

## Acceptance criteria

**C1.** For every changed copy, `ast.dump(ast.parse(old text))` equals `ast.dump(ast.parse(new text))`. Run, with `BASE` the commit before C1 and the eleven paths after it:

`python -c "import ast,subprocess,sys;b=sys.argv[1];bad=[p for p in sys.argv[2:] if ast.dump(ast.parse(subprocess.check_output(['git','show',b+':'+p]).decode('utf-8')))!=ast.dump(ast.parse(open(p,encoding='utf-8').read()))];print(bad or 'same tree');sys.exit(bool(bad))" BASE <paths>`

It must print `same tree`. The search `git grep -nP '^\s*#.*(?<![A-Za-z0-9_./-])(scripts|bootstrap|tools)/'` over the eleven paths returns nothing. `cmp` reports the four pairs identical. `git diff --stat BASE` names exactly the eleven paths, and the roadmap edit is the only other change in the opening commit.

**C2.** The installer command, run from Cairn's root, is `python install/scaffold.py upgrade --target . --finalize dev/tools/claim_check.py dev/tools/content_scan.py dev/tools/content_scan_runner.py dev/tools/run_portable_security_sweeps.py`. Before it, `python install/verify_integrity.py --target .` names those four as modified. After it, the same command reports OK, and the commit holds only `dev/.cairn/cairn-lock.yml`. Before C1 it reported OK for 70 recorded files (run 2026-11-21).

## Scope delta

**Scope delta**: preserved. The Maintainer's choice covers all sixteen lines and none is dropped.

## Verification

`python tests/tier_inventory.py for <the eleven paths>` selects 29 test files (run 2026-11-21), under Cairn's 40-file guard, so the run is not split. It includes `tests/test_portable_security_sweeps.py` (the sweep copies must match, line 3079), `tests/test_content_scan.py` (installed copy equals the template, line 171), `tests/test_doc_drift_tools.py` (line 250), the upgrade and lock tests, and `tests/test_gate_manifest.py`. The last uses a built-up sample, not the committed hashes, so a stale manifest is caught only at the signing, which is why the sentence above is recorded. Run the 29 once at BASE and once after C1 with `-rf --tb=line`, and treat only a failure new at the second run as a finding. The arc's joined run repeats these with everything else; that is safe because the trees are identical, so only a twin mismatch, a stale lock hash or a test that reads comment text could fail, and C1 and C2 check each directly. Not run: the full suite, the signing verifier, the AST baseline (nothing under `install/_scaffold/` changes).

## Plan review -- Claude Sonnet 5.5 (usual reviewer) -- 2026-11-21

Reviewed commit: d095d3614c4638ec259664f3d32f120644ecb9ce

**Obligation**: the usual plan review, the only pass at this stage.
**Tier**: Internal
**Findings**: raised (two, both non-blocking)

The plan delivers the Maintainer's "Fix them all now" with the smallest change: comment text only, in eleven copies, proved by a syntax-tree comparison. I found it sound.

**Foundations**

1. **Should this happen as framed?** Yes. All 16 old lines match the files exactly at the stated line numbers, and each corrected path exists (`tests/integration`, `tests/quality_gate.py`, `install/verify_integrity.py`, `install/_scaffold/lockfile.py`, `install/scaffold.py`; the installed name of `run_security_audit.py` is under `dev/tools/` in an adopter tree, per `install/_scaffold/layout_catalog.py` line 90) -- `sed -n` on each line.
2. **Best alternative.** Deferring each fix to the file's next edit is cheaper but was declined by the Maintainer; no lighter route delivers the outcome -- `dev/PLANNING.md` line 80.
3. **What would show it wrong.** A comment a program reads, or a tree that differs. A tokenizer pass found no marker (`noqa`, pragma, type, encoding) among the 16; the tree command takes `ast.dump` of each file, which drops comments and keeps every string, so a changed code token or docstring fails it -- tokenizer search over the seven tools, plus `tests/tier_inventory.py for <paths>` (29 files, confirmed).

**Findings**

1. Non-blocking. The plan says none of the eleven is in the manifest's `protected_roster`. All the frozen entries are listed there, under `preserved_non_test_frozen_paths`; the manifest's `protected_python_paths` holds only test files. The signing count of eleven is still right. Replace "None is in its `protected_roster`." with "Each is also listed in the manifest's `protected_roster` under `preserved_non_test_frozen_paths`; none is in `protected_python_paths`." The manifest names Cairn's own four copies by their pre-layout `scripts/` paths, as the plan already says.

2. Non-blocking. The docstrings and strings left stale (for example `content_scan.py` lines 12 to 38, the `scripts/` fallback in `run_security_verification.py`) have no home on the roadmap: the entry covers comments only. Add one sentence to that entry saying the docstrings and strings that name old folders remain and are left for the file's next edit.

**Checked and found right.** My own search (Python's tokenizer, run on the seven tools) finds exactly the 16 listed lines, so it works. It also flags `run_portable_security_sweeps.py` line 2629 ("The bootstrap executes..."), which is the word used as a noun, rightly left. `_intent/shared.py` line 19 is rightly left. No comment names another pre-0.8 folder. Twins are byte-identical today; the edit is the same in both. Cairn's lock records the four `dev/tools/` copies, and `--finalize` takes paths. The 29-file selection is under the 40-file guard. No script, option or test file is added.

**Review obligation.** Protected-surfaces gives the heavy tier to a change that "alters what a high-risk surface does or accepts"; a comment-only change with an identical tree alters neither, so the usual review is a sound reading. "When in doubt" does not apply, because the tree check removes the doubt. No Security Review is required.

**Not covered.** I ran no test, no tree command, no lock command and no signing step. I did not read the code review's future diff. The tree command shows no code changed; it does not show a new comment is accurate.

**Verdict**: ACCEPT. Elapsed time: unknown. Tokens: unknown.

## Plan response -- Claude Fable 5.2 (Strategy, for the author) -- 2026-11-21

The review accepted the plan with no blocking finding and confirmed that the usual review is the right obligation. Both non-blocking findings are taken; status is now `ready-to-implement`.

1. Finding 1 (the manifest's roster): taken, with the reviewer's exact words, in Scope.
2. Finding 2 (docstrings and strings have no home): taken on the roadmap, in the entry "Comments in protected files", with a count Strategy made on 2026-11-21: 16 strings, 42 lines, in ten of the eleven copies name an old folder (8 docstrings and 8 other strings; a text search, so some may be there on purpose). They are code, not comments, so this plan leaves them, and whether to correct them is the Maintainer's to say.

Edited directly by Strategy, by exact replacement. Not run: any test or the syntax-tree command.

**Elapsed**: unknown. **Tokens**: unknown.

## Implementation record -- Claude Sonnet 5.5 (Implementation; edits by a Haiku execution agent) -- 2026-11-21

**Conclusion**: C1 and C2 held. Sixteen comment lines changed in eleven copies; every copy parses to the same syntax tree as before, the four twin pairs are identical, and the lock check reports OK. No test was run, by the Maintainer's direction (below).

**C1 (edit commit 4b1ceeb3)**: the diff against the commit before it (a216c969) names exactly the eleven paths, 18 lines added and 16 removed (pair 3's one line became two, in two copies). I read the diff line by line: each changed line is a `#` comment with the text in the detail file. Measured:
- Syntax tree: the plan's command, run once over all eleven paths with BASE a216c969, printed `same tree`, so each of the eleven copies has an equal `ast.dump` before and after.
- `cmp`: `claim_check.py`, `content_scan.py`, `content_scan_runner.py` and `run_portable_security_sweeps.py` are each identical between `dev/tools/` and `templates/modules/`.
- Stale-comment search (the plan's `git grep -nP`) over the eleven paths returned nothing (exit 1). The line the plan leaves alone, `dev/tools/_intent/shared.py` line 19, still matches a loose search, as intended.
- The Haiku agent also saw old folder names in docstrings (for example `content_scan.py` line 12, `check_module_body_coverage.py` lines 13, 32, 67, `run_security_verification.py` lines 15 and 50); the plan leaves those, since they are code, not comments.
- The edit commit carried no intent claim: a claim naming eleven files was refused because its record was over 512 bytes.

**C2 (lock commit c02edfd4)**: before it, `install/verify_integrity.py --target .` named the four `dev/tools/` copies as modified. The plan's `scaffold.py upgrade --finalize` command advanced four hashes. After it, the same check reported OK for 70 recorded files, and the commit holds only `dev/.cairn/cairn-lock.yml`.

**Tests: not run.** The plan's 29-file before-and-after run was stopped by Strategy on the Maintainer's standing direction (chat, 2026-11-21): "Just do all of the changes we need. Then run the fewest tests possible to make sure it was right. Then we re-anchor, certify on all three platforms, and cut." For a comment-only change the syntax-tree check replaces the tests; `cmp` covers the twins and the integrity check covers the lock. The whole suite runs at certification. Other agents' test runs held the machine during the wait, so no run was started beside them.

**Gate manifest**: `tests/fixtures/gate_manifest.json` records hashes of all eleven frozen files, so its hash checks fail until the Maintainer's signing refreshes them; the only reason is these comment edits. I did not run the signing check (not read, not measured).

Not run: the plan's 29-file selection at base and after. Home: the Maintainer's direction quoted above.
Not run: the full suite and the signing verifier. Home: the certification the Maintainer named above.
Not covered: that each new comment is accurate beyond the detail file's wording; the code review reads that. Home: the code review.
Dispositions: none.

**Elapsed**: unknown. **Tokens**: unknown.
