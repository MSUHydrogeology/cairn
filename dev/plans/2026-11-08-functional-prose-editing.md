# Plan: Protect functional prose during editing and review

**Source proposal**: dev/proposals/archive/2026-11-08-claude-functional-prose-editing.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-08
**In brief**: Make changes to agent instructions visible to reviewers and replace brittle wording tests with evidence from those changes.

## Build summary

Ship an exact replacer and a prose change report with the default content-security module. Add the editing rule and review question, then retire wording pins only after their surfaces and mutants are accounted for. Preserve copy parity, real installer behavior and the drain-mode safety test.

## Source proposal

The accepted heavy proposal chooses exact-match edits, a review question, a sentence report, and an atomic replacer in place of text pins. The Maintainer retained the drain-mode pin. Its Decision and review records remain in the archived source.

## Scope

Deliver all four outcomes together: Cairn and shipped `AGENTS.md`, shipped proposal/plan/code review sections, two standard-library tools and the extra roots list, install mapping and tests, and pin retirement. The scanner and its list remain unchanged. The separate promise-unit-testing proposal owns its pilot and other behavior families; this plan owns the text pins here. Preserve every actual copy-parity assertion and behavior check, including installer execution and output checks in hybrid nodes. The nine inventory owners, relative to `bootstrap/tests/`, are `test_review_stance_in_shipped_files.py`, `test_review_sweep_ships.py`, `contract/test_review_and_verification_rules_ship.py`, `contract/test_writing_rules_ship.py`, `contract/test_model_tier_rule_ships.py`, `contract/test_certifying_run_rule.py`, `contract/test_stewardship_rules_ship.py`, `contract/test_scientific_check_guidance_ships.py`, and `test_session_start_drain_rules.py`. The source counted 159 definitions, not 159 proven text-only checks. In particular the stewardship and scientific-guidance nodes mix concerns; preserve installer behavior and compare corresponding copies without preserving canonical wording pins. The drain node remains intact. Other non-pin checks, including figure parsing and template/installer behavior, stay.

**Reuse.** `scripts/content_scan_runner.py` supplies manifest lexical rules and read budgets; its disk parser does not accept the new empty list. `tools/git_read.py` supplies hardened Git access. `tools/prune_intents.py::_atomic_rewrite` and `tools/_intent/shared.py::_has_link_or_reparse` supply write and component-check patterns; do not import private intent modules into adopter tools. `bootstrap/_scaffold/config.py` owns the module mappings. These paths and existing contract tests were searched for near-duplicates; implement the distinct comparison and replacement operations rather than another scanner.

### Documentation / doctrine surface

Editing prescription belongs in both governing `AGENTS.md` files; review prompts in the corresponding shipped and self-hosted templates; tool behavior in docstrings and the content-security module. Deliberation stays in this plan and its source. No scanner doctrine changes.

Proposed paths:
- `scripts/prose_diff.py`
- `templates/modules/team-gated/prose_diff.py`
- `scripts/prose_roots.txt`
- `templates/modules/team-gated/prose_roots.txt`
- `scripts/exact_replace.py`
- `templates/modules/team-gated/exact_replace.py`

The installed twins are `scripts/prose_diff.py` and `templates/modules/team-gated/prose_diff.py`, `scripts/exact_replace.py` and `templates/modules/team-gated/exact_replace.py`, and `scripts/prose_roots.txt` and `templates/modules/team-gated/prose_roots.txt`.

## Sequence

Medium capability is available for semantic inventory and dispositions; High is available for security judgment, ordinary reviews are Medium, and Low can execute the reviewed mechanical work. Estimate three to five work windows for tools and installation, one to three for the per-pin audit and mutants, and one to two for reviews and verification; overlapping surfaces, mutant count and Windows availability make this uncertain. This is not a deadline. No other unfinished plan is a prerequisite.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Build report and replacer, coverage lists, install mappings, rule and review question. | Accepted source and design below. | Tools and rules before any pin retirement. |
| C2 | Medium inventories each node and its assertions, records per-pin dispositions and coverage, then Low executes specific mutants and retirements. | C1 committed; coverage and each pin's recorded disposition and successful mutant before that pin is removed. | Retired wording pins; retained parity, behavior and drain checks. |
| C3 | Complete ordinary and Security code reviews, targeted fixes, and wide Boundary B. | C1–C2 complete; required reviews. | Evidence and independently archivable work. |

C2 records dispositions in this plan before deletion, with each pin's node, read files, retire/keep and one-line reason. Default retire; only the drain pin is kept as a pin, per the Maintainer's choice. A non-pin assertion is retained as behavior or parity, not an exception to retirement. Split hybrids without discarding successful real installs. For each retiree, establish that every file it reads is covered by the two base lists; add Cairn's pinned template paths to its extra list. Apply its dropped-obligation, removal, or negative-term mutant as applicable in a separate copy and show before/after in the report; have a reviewer answer the question from that output. Missing coverage, an unsupported file, or a mutant the tool cannot show stops that retirement and remains implementation work; do not call it passed. Record the precise result and resolve it without silently narrowing accepted scope. Retain repeatable mutants in existing test homes. No per-node review pass is added.

## Acceptance criteria

**C1 — rule and report.** The two governing files define functional prose as the union of base-revision scanner roots and extra prose roots; require exact replacement or patch, list deliberate rule changes in commit bodies, and require the report in trivial commits, where a removed or changed rule makes the edit non-trivial. Each review stage asks whether a rule weakened or disappeared as a reading question. The new list has `# prose-roots v1`, allows no roots, uses scanner lexical containment rules, rejects `!`, and is read from Git at base. Changes to either list or report tool appear first. The scanner is unchanged.

The report CLI is `prose_diff.py [BASE [HEAD]]`, HEAD defaulting to HEAD. Without BASE use merge base with `refs/remotes/origin/HEAD`; `--default-branch REF` supplies a local ref when metadata is absent. Refuse unavailable or ambiguous metadata, never guess or fetch. Reject option-shaped revisions; resolve commits with `rev-parse --verify --end-of-options`, use object IDs thereafter and find exactly one merge base through `rev-parse --revs-only --end-of-options A...B` and its `^OID` record. Git access uses the hardened helper only, no textconv. Enumerate both trees with bounded `ls-tree -r -z`, compare their union under base roots, and read blobs through `cat-file`; no rename inference. Missing lists, invalid manifests or incomplete enumeration report incomplete coverage, never clean. PR-merge use runs the merger's trusted tool.

Normalize whitespace within typed units; headings, list items, table rows, sentence-split paragraphs and fence lines retain their types. Compare Python string constants of at least six words, docstrings and implicitly joined literals; visit each f-string once with `{}` for expressions. Report skipped short-constant counts and runtime/`+` construction gaps. Pair replace blocks in order using `difflib.SequenceMatcher(autojunk=False)` on typed normalized units, reporting leftovers as removed or added; retain duplicates. This is textual alignment, not a semantic equivalence claim. Report parse/decode/recursion failures, links, gitlinks and unsupported suffixes as not compared. Reflow-only requires changed bytes and equal normalized units and structure. Escape repository-derived paths and text, including controls, bidirectional and zero-width characters. Cap files at 8 MiB, aggregate reads at 128 MiB, manifests at 64 KiB each, execution at 120 seconds, units at 2,048 per side and rendered output at 8 MiB; an exceeded cap names incomplete scope and omissions. Exit 0 for completed advisory output, 2 for input/read/coverage failure; findings do not fail it.

**C1 — trusted bindings (SR1).** Both CLI entry points reuse the scanner's verified-buffer
first-import gate, not ordinary Python import. From the fixed caller layout, `scripts/` binds
`tools/git_read.py`; `templates/modules/team-gated/` binds
`templates/skills/_lib/git_read.py`. Each caller carries a literal reviewed SHA-256 and a 256
KiB helper cap. Check every absolute component with `lstat`, refusing links and reparse
points; open fixed paths without following links, nonblocking and binary, and compare
descriptor and path metadata before and after reading, including the existing Windows
birth/ctime mapping. Execute only the captured hash-matching buffer in a fresh `ModuleType`
with `compile(dont_inherit=True)`. Never reopen it, use bytecode or `sys.modules`, or derive a
path from the current directory, target, lockfile source or existence fallback. The replacer
uses the same gate and cap with a literal pin for its same-directory report sibling; the
report imports no sibling or target code and receives the verified helper for delegated
operations. This forms a helper → report → replacer binding chain. Template-source mode uses
those fixed canonical buffers without installed lock records. Installed mode requires exactly
one valid fixed-destination helper lock record and, for the replacer, one sibling report
record, each hash matching the caller's literal pin; missing, duplicate or invalid records
refuse. Never use a record's `src` as path authority. Use existing `InstallSpec` verbatim
mappings and bounded JSON lock ownership, without a new registry or schema. Pin parity tests
cover both twin bytes and literals.

Use Git 2.45 or later: obtain root with `rev-parse --show-toplevel`, default ref with
`rev-parse --symbolic-full-name --verify --end-of-options refs/remotes/origin/HEAD`, resolve
`REV^{commit}` with the stated verify form, and enumerate with `ls-tree -r -z OID` and
`cat-file blob OID`. Unsupported Git is unavailable, not an empty comparison. Contract tests
through source/template and installed CLIs substitute missing, wrong, oversized and
linked/reparse helper or sibling, poisoned module/bytecode caches and target-directory
lookalikes; each must refuse before a marker executes. A path swap after verification executes
only the captured buffer. Bind both before any write: binding failure exits 2 unchanged with
no temp; a later report failure retains exit 3.

**C1 — replacer.** `exact_replace.py TARGET --old-file FILE --new-file FILE` accepts `-` for only one source; alternatively `--batch FILE` is a UTF-8 JSON array of objects with exactly `old` and `new` strings. Read bytes without newline or Unicode normalization; reject empty batches and old strings, bound reads, and apply pairs to the running result all-or-none. Count overlapping start positions. Refuse zero or multiple matches with count and line numbers. Require repository-root-relative target; reject traversal, colon, case-insensitive `.git`, `GIT~<digits>`, links or reparse points in every component, nonregular targets, multiple hard links and invalid UTF-8. Verify real-path containment. Create an exclusive sibling temporary file with `O_NOFOLLOW` where available, preserve mode, flush and fsync, re-walk components and check identity, mode and SHA-256 immediately before replace; clean the temporary on failure. A refusal leaves the original untouched. The accepted residual race after the final check and through an already-open handle remains documented; Windows open/read-only replacement failure is refusal. Exit 0 applied, 1 match-count failure, 2 refused without write, 3 applied but report failed. Use sibling report functions on in-memory old/new text for membership from committed HEAD lists; list edits get notice first, parse failures get not-compared. Escape output as above.

**C1 — bounded replacer (SR2).** A monotonic 120-second invocation deadline starts before
binding and input. Cap target, each replacement source and each result at 8 MiB; JSON at 16
MiB and 256 pairs; cumulative target, raw inputs and UTF-8 encoded decoded batch strings at 64
MiB. Charge matching work in advance as `2 * (len(old) + len(current_target))` per pair, with
a 128 MiB limit. Count overlapping matches using linear KMP and an `array('I')` prefix table,
checking the deadline at least every 64 KiB of work. Retain at most 2,048 positions for line
numbers; report the full match count and omitted-position count. Reject an oversized result
before allocation or write. Validate exact batch keys, strings, pair count and byte charges
before application; UTF-8, JSON, recursion and memory failures refuse. No temporary file
exists before all reads, validation, matching, work and result checks pass. Check deadline at
each write phase and immediately before replacement. Postwrite deadline or report failure is
exit 3.

To bound blocked input on all platforms, start a daemon reader before potentially blocking
open or read. The worker opens file sources binary, no-follow and nonblocking, verifies
regular-file identity and returns captured metadata and data; stdin uses a duplicated
descriptor and `os.read` in at most 64 KiB chunks. On Windows set the duplicate to binary mode
to preserve CRLF. A bounded queue of two chunks carries data; both queue writes and the main
thread's reads use remaining deadline. The main thread alone may mutate the target; the worker
never writes target, temp or output. Signal a stop on refusal, never wait indefinitely or join
a blocked reader, and do not close its descriptor from another thread. A blocked daemon cannot
keep the CLI alive; the OS closes its descriptor at exit. Use bounded raw best-effort
diagnostics, with an abandonable daemon writer if output blocks, and no buffered
stdin/stdout/stderr locks in workers. The tools are CLI-scoped: no repeated in-process `main`
calls while an abandoned worker remains. Test short injected deadlines at the internal seam
and a real subprocess whose input pipe remains open, plus oversized target/source/stdin/JSON,
decoded aggregate, pair, work, result and deadline breaches. Every prewrite breach must exit 2
with identical original and no temp. Native Windows tests include raw CRLF and a retained-open
pipe.

**C1 — install and tests.** Default-on content-security installs both scripts and the empty-header list verbatim. Contract tests exercise every accepted input, output, failure, cap, safety property and real CLI, including list/tool notices, overlaps, raw stdin/CRLF, batch atomicity, links, hard links, paths, changed-before-replace, cleanup, mode, report failure and hidden characters. Test install and twin parity, scanner's existing checks, `python scripts/check_cairn.py`, and `python bootstrap/scaffold.py --dry-run`. Run Windows contract cases over SSH on an isolated implementation copy using `cairn-windows` and `C:\ProgramData\miniconda3\python.exe` 3.13.17, including actual junction/reparse, hard-link and open/read-only cases. If unavailable, leave Windows unclaimed and `bootstrap/SAFETY.md` unchanged, record the missing measurement and revival condition; do not weaken checks.

**C2.** The plan contains an individual disposition and reason for every actual pin before its deletion, each read file is covered first, and each specified independent-copy mutant is visible to the reviewer. All actual copy-parity, real install and other behavior checks survive and pass, as does the protected drain node. The tools and rules precede this work in committed history. No assertion is treated as a pin solely because it shares a test node.

**C3.** Independent ordinary and Security code review challenge implementation and dispositions. Wide Boundary B on the clean final commit covers affected owners, consumers, integration/public paths, standing gates and all acceptance commands. A failed required check remains open. An independent scientific check is N/A: no scientific assumption or result touched.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A uses `python tools/test_tiers.py for <changed paths>` and its named tests, plus applicable claim, link, snippet and neutrality gates. Trace callers, install mappings, list readers and all pinned surfaces to tests; document omissions and add tests for plausible uncovered faults. Run the source proposal's named CLI contract, per-pin mutant, scanner, parity, install and smoke checks. Boundary C is independent targeted falsification, not a suite. After review and fixes, Boundary B is **wide**, under `/Users/kendal30/conda_envs/lhm/bin/python3.13` on a clean unchanged final commit; record SHA/range, clean pre/post state, command counts, elapsed time, tokens, non-passes, omissions and timing misses as the template requires. Tree certification and any Maintainer re-anchor remain separate ceremonies, not completion prerequisites; unexpected integrity failure remains implementation work.

## Plan review -- GPT-6.1 Terra (Reviewer) -- 2026-11-08

Reviewed commit: a288d4a5ca07fbb57e303b1510a8bd387a0f58cc

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: READY
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes: C1 delivers the rule and both installed tools before C2 retires pins; C2 preserves parity, real installs and the drain node, and C3 finishes the required reviews and verification -- plan Scope, Sequence and acceptance criteria; source Outcomes 1–4 and Decision.
2. **Best alternative.** The existing scanner and hardened Git helper are the useful reuse; replacing the new report with the scanner would lose revision comparison and the extra list's empty state -- plan Reuse and C1; `scripts/content_scan_runner.py` and `tools/git_read.py`.
3. **What would show it wrong?** A covered pin's specified mutant that the report cannot show, or an install or parity check that fails after splitting a hybrid, would leave the retirement open -- plan C2 and Verification.

The plan gives Medium the semantic classification and requires each disposition, coverage and mutant result before deletion; it does not depend on another unfinished plan. Its C1 specifies the main input, alignment, failure, write and installation choices for execution, while C3 reserves independent ordinary and Security code reviews.

**Coverage**: Read the committed plan, accepted proposal and review responses, plan template, Git helper command set and install mapping. Did not audit every pin, run implementation tests, or assess the detailed security of the future implementation; those remain C2 and the separate Security reviews' work.

## Plan review -- Codex GPT-6.1 Sol (High) -- 2026-11-08

Reviewed commit: a288d4a5ca07fbb57e303b1510a8bd387a0f58cc

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE before implementation.

**Foundations**

1. **Should this happen as framed?** Yes: C1–C3 preserve all accepted outcomes, per-pin evidence, behavior/parity and drain checks; two boundary mechanisms need specification before Low execution -- accepted source Outcomes 1–4; plan Acceptance criteria.
2. **Best alternative.** Reuse the already-implemented verified Git-loader pattern and existing test homes, with explicit replacer budgets; this delivers the same scope without waiting for the unfinished Safe Git plan or adding human operations -- `scripts/content_scan_runner.py::_load_verified_git_read`; `dev/plans/2026-11-06-safe-git-reads.md`, C0.
3. **What would show it wrong?** A real CLI executing a substituted helper/import marker, writing after a prewrite budget breach, hiding a base-covered mutant, or misreporting a Windows refusal disproves delivery -- plan C1/C2 contracts and native Windows cases.

**SR1 -- blocking: bind code before importing it.** “Uses the hardened helper” does not specify either new caller's trusted helper delivery/import mechanism. The Safe Git C0 record specifies fixed source/installed layouts, caller-pinned verified-buffer execution, component checks, cache exclusion and applicable lock records; the scanner already implements that seam. Specify reuse for both tools, fixed trusted sibling report loading, refusal policy and real-entry substitution tests. Otherwise Low must design a security boundary, and a helper import can execute code before hardened Git access begins. This needs no whole-plan prerequisite.

**SR2 -- blocking: specify replacer budgets.** “Bound reads” leaves target, source files, raw stdin and JSON batch limits undefined; the report paragraph's caps do not clearly govern them. Specify byte/aggregate limits, pair/work or execution limits and enforcement before replacement, including oversized/blocked input and batch/deadline cases. Test exit 2, unchanged original and temporary cleanup on each prewrite breach; preserve exit 3 for postwrite report failure.

**Coverage:** Read committed plan/source, template, Git helper, scanner loader, atomic-write precedent and Safe Git C0. Path/reparse/short-name/stream/hard-link checks, concurrent-replacement residual, escaping, base lists, fixed Git forms, caps and Windows measurement are addressed in design apart from SR1/SR2. No implementation checks, suite, mutants or Windows execution; runtime correctness remains unmeasured. Over target to identify both missing mechanisms. **Elapsed:** approximately 12 minutes; **tokens:** unknown.

## Response -- GPT-6.1 Terra (Implementation) -- 2026-11-08

**Elapsed**: approximately 10 minutes. **Tokens**: unknown.

- **SR1, accepted.** C1 now specifies fixed, pinned verified-buffer bindings, installed lock records, refusal and real-entry substitution tests. High design reused the scanner's existing loader and verified the named Git forms on a synthetic repository; no other plan is a prerequisite.
- **SR2, accepted.** C1 now specifies bounded input, matching and deadline work, a nonblocking CLI escape from blocked readers and output, prewrite refusal tests and Windows measurement. High design measured a retained-open pipe timeout in an owned smoke; native Windows behavior remains to be measured.
- **Ordinary review:** no findings. Both reviews' accepted scope and required checks remain intact.
