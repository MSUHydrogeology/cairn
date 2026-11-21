# Plan: Defect arc F, stale comments in protected tools

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
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

**Frozen, not protected.** Protected-surfaces names `run_portable_security_sweeps.py` and its shipped copy as high-risk. All eleven copies are frozen in `tests/fixtures/gate_manifest.json` (the manifest lists Cairn's own four under their pre-layout `scripts/` paths and the check-coverage tool under `bootstrap/`). None is in its `protected_roster`. Changing any of them makes the manifest's recorded hash stale; the Maintainer's signing refreshes it, and no agent does. The signing's one sentence is: "Eleven frozen tool files changed only in comments naming old folders; each parses to the same syntax tree as before." Cairn's own lock (`dev/.cairn/cairn-lock.yml`) records the four `dev/tools/` copies, so those four hashes go stale too; the Implementation agent refreshes them in C2.

**Review.** Protected-surfaces gives the heavy tier to a change that alters what a high-risk surface does or accepts, and says "when in doubt, take the Security Review". A comment cannot alter what a tool does, so the lighter tier would be defensible. I take the heavier one: four of the seven tools are security tools, one is named high-risk, and the Maintainer signs for them. The Security Review pass is narrow: it re-runs the syntax-tree check and the stale-comment search, and reads the diff for any non-comment token. Code review carries the same pair.

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
