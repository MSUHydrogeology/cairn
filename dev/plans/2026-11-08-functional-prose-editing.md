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

## Implementation verification -- GPT-6 Luna LowImplementation -- 2026-11-08

**C1 checkpoint, not completion.** Source work is committed in `a61af064`,
with the Git helper tree-read correction in `c252d44e` and the 256 KiB report
binding correction in `28c975f1`. Python was
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13). The code test runs
used those committed feature bytes. Tokens: unknown; elapsed: approximately
35 minutes through this checkpoint.

| Command | Result | Elapsed | Tokens |
|---|---|---:|---|
| `pytest bootstrap/tests/security/test_prose_tools.py bootstrap/tests/test_content_scan.py bootstrap/tests/test_reference_scripts.py` at `a61af064` | 240 collected; 237 passed, 3 failed because `ls-tree` requested 128 MiB from a helper capped at 64 MiB per read. | 27.16 s | unknown |
| The 3 failed CLI nodes at `c252d44e` | 3 passed after each tree read was capped at 64 MiB; aggregate report reads remain capped at 128 MiB. | 2.16 s | unknown |
| Oversized report binding CLI node at `28c975f1` | 1 passed; refusal occurred before the target or a temporary file changed. | 0.15 s | unknown |
| `scaffold.py` dry-run with a temporary `content-security` profile and target | Exit 0; target remained empty. | <1 s | unknown |
| Changed-document `link_check.py`, `sync_doc_snippets.py --check`, and `quality_gate.py --sub neutrality` | Link check: 7 documents, no issues, 3 external links unprobed. Snippets: 7 documents, no drift. Neutrality: 0 failures, 43 informational notices. | <2 s | unknown |
| `scripts/check_cairn.py` | Failed on two unrelated unresolved paths in the 2026-11-05 architecture plan and 2026-10-27 strategy. It also reported four unused older allow entries. The six stale C1 `Proposed paths` declarations were removed before this run. | <2 s | unknown |

`tools/test_tiers.py for` mapped all changed C1 paths to 74 test files and
reported 19 additional AGENTS readers omitted above its guard. This worker ran
the three direct C1 owners, not that broad list; Root owns the deduplicated
feature selection. No full suite, Boundary B, Windows run, pin disposition, or
mutation run is claimed.

**Still unpassed in C1:** the remaining report default-ref/ambiguous-ref and
base-list mutations; list/tool first-notice and hidden-character cases; the
full Python constant/f-string and incomplete-coverage cases; replacer cap
breaches for target, sources, JSON, aggregate bytes, pairs, match work and
result size; traversal/colon/`.git`/short-name and hard-link cases; changed-
before-replace, mode-preservation and post-write report-failure cases; and
native Windows junction, hard-link, CRLF and retained-open/read-only cases.
These remain implementation work and are not waived by this checkpoint.

**Boundary B mode**: wide, pending code review and the final committed range.

## C2 partial classification -- GPT-6.1 Terra (Implementation) -- 2026-11-08

**Evidence**: committed C1 `a9f752e6`. This is an author classification, not a review or Decision. The nine owners contain 159 test definitions (80, 31, 14, 13, 11, 7, 1, 1, 1); parametrization expands cases and mixed nodes prevent treating that count as removals. The entries below are partial; all other nodes remain unclassified and none is deletion-eligible from this record. RETIRE identifies a text assertion subject to C2's per-file coverage, mutant and reviewer gates, not authorization to delete now. KEEP preserves the indicated behavior, parity or Maintainer-retained pin. Installed paths below are outputs of real scaffold runs.

| Owner and node (`bootstrap/tests/`) | Read files | Disposition and reason |
|---|---|---|
| `contract/test_certifying_run_rule.py::test_every_verification_surface_says_the_full_suite_is_a_certifying_run` | `AGENTS.md`, `templates/core/AGENTS.md`, `docs/methodology/plans.md`, `docs/methodology/dual-review.md`, `dev/plans/_template.md`, `templates/core/dev/plans/_template.md` | RETIRE positive and negative phrase pins: wording of certification and a forbidden marker. |
| `contract/test_certifying_run_rule.py::test_cairn_governing_rule_names_integration_points_and_ancestor_claim` | `AGENTS.md` | RETIRE trigger and ancestor-claim phrase pins. |
| `contract/test_certifying_run_rule.py::test_adopter_certification_limits_claim_and_reopens_contradictions` | `templates/core/AGENTS.md`, `docs/methodology/plans.md` | RETIRE positive and negative phrase pins about the certification claim. |
| `contract/test_certifying_run_rule.py::test_reviewers_are_told_never_to_run_the_full_suite` | `AGENTS.md`, `templates/core/AGENTS.md` | RETIRE exact sentence pin. |
| `contract/test_certifying_run_rule.py::test_the_shipped_rule_names_no_cairn_only_command` | `templates/core/AGENTS.md` | RETIRE negative token pins; prove each relevant reintroduced term is reported. |
| `contract/test_certifying_run_rule.py::test_the_broad_run_refusal_no_longer_offers_the_override` | `bootstrap/tests/conftest.py` | RETIRE source-message wording pins only after Python string coverage and the changed-message mutant are proved. KEEP actual broad-run refusal behavior if independently exercised; this node reads source rather than executing the guard. Short and constructed Python strings are a stated report gap. |
| `contract/test_certifying_run_rule.py::test_cairn_keeps_its_own_certification_pair_and_triggers` | `AGENTS.md` | RETIRE exact command and trigger wording pins after mutants show their loss. |
| `contract/test_stewardship_rules_ship.py::test_small_fix_rule_and_capture_pointer_reach_install` | `bootstrap/scaffold.py` and its install inputs; installed `AGENTS.md`, installed `dev/modules/issue-capture.md`; `docs/methodology/lifecycle.md`, `docs/methodology/plans.md` | RETIRE positive and negative canonical-wording pins. KEEP the real install, success check and evidence that the corresponding source guidance reaches both installed destinations; do not replace the latter with an exit-status check alone. |
| `contract/test_scientific_check_guidance_ships.py::test_the_check_guidance_reaches_every_copy_and_promise_site` | `dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`, `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, `dimensions/complexity.md`, `dimensions/README.md`, `bootstrap/BOOTSTRAP.md` | RETIRE canonical block, paragraph and phrase pins. KEEP comparisons of corresponding source copies, and slot-placement checks: a filled slot can replace its contents on upgrade. Preserve any other demonstrated installer behavior while splitting this hybrid. |
| `test_session_start_drain_rules.py::test_the_skill_keeps_its_drain_safety_rules` | `templates/skills/session-start/SKILL.md` | KEEP intact: Maintainer expressly retained the drain-mode pin in the accepted source. |

**Coverage and unresolved work**: `scripts/prose_roots.txt` currently contains only its header. The scanner roots do not cover all `templates/`, `dimensions/`, `bootstrap/` or root `README.md` inputs. The report explicitly marks SVG and YAML unsupported and skips short and constructed Python strings; a listed root does not cure those gaps. The stance owner's dynamic walks include `.md`, `.yml` and `.svg`; enumerate the committed members before claiming set coverage. `docs/assets/dual-review-independence.svg` has wording pins, but XML parsing, `aria-labelledby`, description/title relation and embed geometry are behavior to retain. C2 still owes every remaining node and its exact files, any required design for unsupported inputs, each independent-copy mutant and a reviewer's answer. No mutation, coverage or retirement is claimed passed here.

**Elapsed**: unknown. **Tokens**: unknown.


## Implementation clarification -- Codex GPT-6.1 Sol (High) -- 2026-11-08

**Role:** Strategy / in-contract mechanism design, not a review or scope
Decision. Basis: accepted source Outcomes 2–3, this plan's C1/C2, and committed
C1 through `43b29a20`. **Elapsed:** approximately 15 minutes, including corpus
inspection and coordination. **Tokens:** unknown.

**Complete literal evidence can satisfy a text pin's mutant requirement even
when structured sentence extraction is unavailable.** Outcome 3 requires the
specific mutant to appear as changed, removed or added with before/after text,
followed by a reviewer's judgment; it does not require a YAML/XML parser.
Outcome 2 still requires unsupported formats to say **NOT COMPARED**. Keep
that notice, qualified as structured prose extraction, and supply supplemental
raw source evidence without claiming that the format or its behavior was
interpreted. This preserves both promises. C2's unsupported-file stop remains
until that pin's exact mutant has complete evidence by this mechanism; a root
entry or the notice alone cannot clear it. This is a mechanism clarification,
not permission to omit a mutant, waive coverage or remove behavior checks.

For a changed, covered regular UTF-8 blob, trim its equal Unicode-character
prefix, then its equal nonoverlapping suffix. Compare the remaining exact
spans without whitespace normalization. Emit **RAW CHANGED**, **RAW REMOVED**
or **RAW ADDED**, with escaped before and after text (including an empty side)
and original line ranges. This is one conservative differing span, not a
semantic alignment. Charge both inputs to existing byte budgets, scan linearly
with deadline checks at most every 64 KiB of input, and cap each raw differing
span at 64 KiB UTF-8 bytes before escaping. The rendered result also obeys the
existing output cap. An over-limit span, decode failure, deadline or omitted
output says **RAW EVIDENCE INCOMPLETE**; it stops that retirement. Do not
truncate into apparently complete evidence or report reflow-only for these
raw changes. Links, gitlinks and other refused inputs remain unexamined.

Apply the supplement to unsupported formats such as YAML/SVG/shell source
and to changed Python source, including comments and constructed or short
strings. The inventory also reads `bootstrap/reanchor.sh` and
`bootstrap/reanchor-launcher.template.sh`; show their literal comment mutants
without executing a shell. Preserve Python's six-word structured-extraction threshold and skipped-short count;
the supplement does not claim those gaps were parsed. Use the same mechanism
for revision reports and replacer in-memory reports. Keep the 8 MiB file,
128 MiB aggregate, 120-second execution and 8 MiB rendered-output limits;
raw spans are not whole-file units fed into the 2,048-unit aligner. Execute no
format, parser or repository-supplied code.

The authorized Cairn roots must cover the inventory; the adopter seed stays
header-only. Required falsifiers include a YAML added forbidden term, SVG
wording deletion, and Python comment/short-string obligation loss, each shown
with exact complete raw before/after evidence. Oversized spans and malformed
UTF-8 must visibly remain incomplete. Only literal/obligation assertions may
retire after their exact mutants and reviewer reading; SVG geometry, actual
accessibility relations, slots, installer behavior, parity and the drain pin
stay. No implementation verification or additional review is claimed here.

## C2 classification, continued -- GPT-6.1 Terra (Implementation) -- 2026-11-08

The preceding C2 definitions and gates apply. In the table, **A** means `AGENTS.md` and `templates/core/AGENTS.md`; **S** means `dev/modules/security-review.md` and `templates/modules/team-gated/security-review.md`; **L** means `dev/agent_collaboration.md` and `templates/core/dev/agent_collaboration.md`; **P** means both own and `templates/core/` proposal, plan and strategy `_template.md` files. Installed paths are generated by the real scaffold fixture. RETIRE remains conditional; none has passed its C2 gates.

| Node relative to `bootstrap/tests/contract/` | Files read | Disposition and reason |
|---|---|---|
| `test_review_and_verification_rules_ship.py::test_agents_md_carries_the_obligation` | A | RETIRE positive obligation patterns. |
| `test_review_and_verification_rules_ship.py::test_agents_md_omits_the_forbidden_phrasing` | A | RETIRE forbidden-wording patterns; reintroduce each term as applicable. |
| `test_review_and_verification_rules_ship.py::test_forbidden_patterns_recognize_their_examples` | A | RETIRE controls for the foregoing text-pattern instrument. |
| `test_review_and_verification_rules_ship.py::test_the_external_by_default_pin_ignores_case_and_wrapping` | none; example strings | RETIRE case/wrapping control of a retired pattern. |
| `test_review_and_verification_rules_ship.py::test_an_empty_file_carries_no_obligation` | none; empty string | RETIRE control of the wording-pattern instrument. |
| `test_review_and_verification_rules_ship.py::test_the_commit_rule_sits_in_the_working_tree_section` | A | RETIRE rule text and placement pin. |
| `test_review_and_verification_rules_ship.py::test_the_shipped_copy_makes_claiming_conditional` | `templates/core/AGENTS.md` | RETIRE conditional wording pin. |
| `test_review_and_verification_rules_ship.py::test_cairns_own_copy_claims_unconditionally` | `AGENTS.md` | RETIRE positive and negative claiming wording pins. |
| `test_review_and_verification_rules_ship.py::test_coordination_doctrine_guards_same_file_commits` | `docs/methodology/coordination.md` | RETIRE coordination phrase pins. |
| `test_review_and_verification_rules_ship.py::test_light_tier_can_ship_wide_work_without_a_plan` | A; `docs/methodology/lifecycle.md`, `docs/methodology/proposals.md`, `docs/methodology/plans.md`; own and shipped proposal and plan templates | RETIRE positive wording pins and their deletion controls, each carrier separately. |
| `test_review_and_verification_rules_ship.py::test_security_module_movement_alone_does_not_trigger_review` | S | RETIRE positive and negative wording pins on security triggers. |
| `test_review_and_verification_rules_ship.py::test_security_module_states_guarded_reuse_limits` | S | RETIRE positive and negative wording patterns on guarded reuse. |
| `test_review_and_verification_rules_ship.py::test_security_module_defines_wide_as_mapped_change_verification` | S | RETIRE exact sentence pin. |
| `test_review_and_verification_rules_ship.py::test_security_module_trigger_mutations_are_caught` | S | RETIRE wording-instrument controls after independently demonstrating each removed limit and inserted bypass in the report. |
| `test_writing_rules_ship.py::test_standard_with_version_and_groups_reaches_install` | installed `dev/agent_collaboration.md` | RETIRE fixed version, heading and numbering pins. KEEP real install and evidence that the corresponding source standard reaches the installed file. |
| `test_writing_rules_ship.py::test_changed_rules_match_across_local_shipped_and_public_copies` | L; `docs/plain-language.md` | KEEP comparison of corresponding rule text across copies: parity, not canonical wording. |
| `test_writing_rules_ship.py::test_install_writes_the_shipped_standard_unchanged` | `templates/core/dev/agent_collaboration.md`; installed `dev/agent_collaboration.md` | KEEP source-to-install standard comparison and real install. |
| `test_writing_rules_ship.py::test_standard_sits_just_before_surfacing_judgment_calls` | L | RETIRE fixed heading and ordering pin. |
| `test_writing_rules_ship.py::test_installed_standard_sits_just_before_surfacing_judgment_calls` | installed `dev/agent_collaboration.md` | RETIRE fixed heading and ordering pin; KEEP real install and evidence corresponding source content reaches it. |
| `test_writing_rules_ship.py::test_cairns_own_copy_says_what_it_ships` | L | KEEP corresponding-section parity. |
| `test_writing_rules_ship.py::test_pointer_sentence_is_in_the_installed_agents_file` | installed `AGENTS.md` | RETIRE exact pointer pin; KEEP real install and evidence corresponding source content reaches it. |
| `test_writing_rules_ship.py::test_pointer_sentence_is_in_both_source_agents_files` | A | RETIRE exact pointer and surrounding-text placement pins. |
| `test_writing_rules_ship.py::test_no_copy_tells_agents_to_use_a_readability_score` | A and L | RETIRE negative formula and phrasing patterns, with reintroduced-term mutants. |
| `test_writing_rules_ship.py::test_installed_standard_forbids_a_readability_score` | installed `dev/agent_collaboration.md` | RETIRE exact prohibition pin; KEEP real install and evidence corresponding source content reaches it. |
| `test_writing_rules_ship.py::test_source_readable_prompt_and_contrary_mutation` | P | RETIRE source prompt patterns and their contrary-wording controls, each source and label separately. |
| `test_writing_rules_ship.py::test_installed_readable_prompt_and_contrary_mutation` | installed proposal, plan and strategy templates | RETIRE prompt patterns and contrary-wording controls; KEEP real install and evidence each corresponding source template reaches its destination. |
| `test_writing_rules_ship.py::test_cairn_local_retry_markers_do_not_enter_adopter_guidance` | A; installed `AGENTS.md` | RETIRE canonical local/adopter wording and negative-marker pins; KEEP real install and evidence the shipped guidance reaches the installed file. |

**Elapsed**: unknown. **Tokens**: unknown. No behavior, coverage, mutant or retirement is newly claimed passed.

## C2 classification completion -- GPT-6.1 Terra (Implementation) -- 2026-11-08

Together with the prior ten entries, the tables classify all 159 existing definitions; parametrized cases are separate retirements with the same disposition, and every listed carrier needs its own applicable evidence. KEEP assertions survive in their present or behaviorally equivalent form, including successful real installs and corresponding source/output checks; RETIRE applies only to the identified text pins and their own pattern controls. A RETIRE disposition is not a passed mutant. The eligible deletion set is empty until every relevant coverage, independent-copy mutant and reviewer-answer gate in C2 passes. A mixed node is split, not deleted wholesale. These are author dispositions, not review or Decision.

The following file sets enumerate the existing committed tree at `a9f752e6`. For dynamic walks, each member is listed explicitly; a changed tree must re-enumerate before claiming coverage. W and Z include all walked files, not merely files whose old wording matches. X includes the two own authoring templates and every eligible core file. Paths read by install fixtures are temporary outputs; each fixture also invokes `bootstrap/scaffold.py` with its stated profiles and their install inputs. Generated copies in mutation controls are derived from the named source or installed output.

- **A**: `templates/core/AGENTS.md`, `AGENTS.md`.
- **L**: `templates/core/dev/agent_collaboration.md`, `dev/agent_collaboration.md`.
- **M**: `templates/modules/team-gated/dual-review.md`, `dev/modules/dual-review.md`.
- **T**: `templates/core/dev/proposals/_template.md`, `dev/proposals/_template.md`, `templates/core/dev/plans/_template.md`, `dev/plans/_template.md`.
- **P**: `templates/core/dev/proposals/_template.md`, `dev/proposals/_template.md`.
- **N**: `templates/core/dev/plans/_template.md`, `dev/plans/_template.md`.
- **V**: `templates/core/AGENTS.md`, `AGENTS.md`, `templates/core/dev/agent_collaboration.md`, `dev/agent_collaboration.md`, `templates/core/dev/proposals/_template.md`, `dev/proposals/_template.md`, `templates/core/dev/plans/_template.md`, `dev/plans/_template.md`, `docs/methodology/plans.md`, `docs/methodology/dual-review.md`, `dev/strategy/2026-10-27-antigravity-plain-language-and-scientific-writing.md`, `templates/modules/team-gated/dual-review.md`, `dev/modules/dual-review.md`.
- **K**: `AGENTS.md`, `templates/core/AGENTS.md`, `dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`, `dev/modules/security-review.md`, `templates/modules/team-gated/security-review.md`, `docs/methodology/dual-review.md`, `docs/methodology/plans.md`.
- **R**: `templates/modules/team-gated/model-selection.md`, `dev/modules/model-selection.md`, `templates/modules/team-gated/security-review.md`, `dev/modules/security-review.md`, `templates/phase-0/project-profile-legacy.md`, `templates/skills/session-start/SKILL.md`, `.agents/skills/session-start/SKILL.md`, `bootstrap/fidelity-check.md`, `templates/modules/README.md`, `templates/optional/CONTRIBUTING.md`.
- **D**: `dimensions/complexity.md`, `dimensions/README.md`, `dimensions/agent-team.md`, `dimensions/human-team.md`.
- **Q**: `README.md`, `docs/glossary.md`, `docs/vision.md`, `docs/agent-team-onboarding.md`, `dev/modules/onboarding/agent-team-onboarding.md`, `docs/quickstart.md`, `docs/workflow-role.md`, `docs/getting-started.md`, `docs/dev-tour.md`, `dev/modules/onboarding/dev-tour.md`, `docs/tool-usage.md`, `on-ramp/README.md`, `docs/DOCUMENTATION_PLAN.md`, `templates/modules/default-on/documentation_plan_template.md`, `docs/assets/dual-review-independence.svg`.
- **J**: `docs/methodology/dual-review.md`, `docs/methodology/lifecycle.md`, `docs/methodology/roles.md`.
- **H**: `SECURITY.md`, `bootstrap/REANCHOR_RUNBOOK.md`, `bootstrap/SAFETY.md`, `bootstrap/reanchor-launcher.template.sh`, `bootstrap/reanchor.sh`, `bootstrap/tests/_gate_preflight.py`, `docs/methodology/dual-review.md`, `docs/methodology/lifecycle.md`, `docs/methodology/plans.md`, `docs/methodology/roles.md`, `scripts/reanchor_ceremony.py`, `scripts/repin.py`.
- **W**: `AGENTS.md`, `dev/agent_collaboration.md`, `dev/modules/claim-check.md`, `dev/modules/content-security.md`, `dev/modules/coordination-tiers.md`, `dev/modules/doc-drift-prevention.md`, `dev/modules/documentation-plan.md`, `dev/modules/dual-review.md`, `dev/modules/examples-gallery.md`, `dev/modules/incident-trackers.md`, `dev/modules/incident_log_template.md`, `dev/modules/issue-capture.md`, `dev/modules/model-selection.md`, `dev/modules/onboarding/agent-team-onboarding.md`, `dev/modules/onboarding/dev-tour.md`, `dev/modules/portable-security-sweeps.md`, `dev/modules/reflections.md`, `dev/modules/security-review.md`, `dev/modules/security-verification.md`, `dev/modules/testing-discipline.md`, `dimensions/README.md`, `dimensions/age.md`, `dimensions/agent-team.md`, `dimensions/complexity.md`, `dimensions/human-team.md`, `dimensions/language.md`, `dimensions/size.md`, `docs/DOCUMENTATION_PLAN.md`, `docs/README.md`, `docs/agent-team-onboarding.md`, `docs/build-a-board-view.md`, `docs/code-map.md`, `docs/dev-tour.md`, `docs/further-reading.md`, `docs/getting-started.md`, `docs/glossary.md`, `docs/methodology/README.md`, `docs/methodology/collaboration-stance.md`, `docs/methodology/consolidation-review.md`, `docs/methodology/coordination.md`, `docs/methodology/doc-governance.md`, `docs/methodology/dual-review.md`, `docs/methodology/lifecycle-contract.md`, `docs/methodology/lifecycle.md`, `docs/methodology/onboarding.md`, `docs/methodology/plans.md`, `docs/methodology/proposals.md`, `docs/methodology/rationale.md`, `docs/methodology/roles.md`, `docs/methodology/runtime-contract.md`, `docs/methodology/session-routines.md`, `docs/plain-language.md`, `docs/quickstart.md`, `docs/related-practices.md`, `docs/release-process.md`, `docs/skills-compatibility.md`, `docs/solo-legacy-recipe.md`, `docs/tool-usage.md`, `docs/vision.md`, `docs/workflow-role.md`, `templates/README.md`, `templates/codebase-readiness-report.md`, `templates/core/AGENTS.md`, `templates/core/CHANGELOG.md`, `templates/core/NOTICE.md`, `templates/core/VENDOR.md`, `templates/core/dev/PLANNING.md`, `templates/core/dev/README.md`, `templates/core/dev/agent_collaboration.md`, `templates/core/dev/measurement/README.md`, `templates/core/dev/modules/README.md`, `templates/core/dev/plans/_template.md`, `templates/core/dev/proposals/_template.md`, `templates/core/dev/rules/README.md`, `templates/core/dev/strategy/README.md`, `templates/core/dev/strategy/_template.md`, `templates/core/dev/upstream/README.md`, `templates/core/dev/upstream/_template.md`, `templates/modules/README.md`, `templates/modules/default-on/claim-check.md`, `templates/modules/default-on/documentation-plan.md`, `templates/modules/default-on/documentation_plan_template.md`, `templates/modules/default-on/incident-trackers.md`, `templates/modules/default-on/incident_log_template.md`, `templates/modules/default-on/reflections-README.md`, `templates/modules/default-on/reflections.md`, `templates/modules/default-on/security-verification.md`, `templates/modules/team-gated/api-access-security.md`, `templates/modules/team-gated/architecture-review.md`, `templates/modules/team-gated/architecture_review_template.md`, `templates/modules/team-gated/content-security.md`, `templates/modules/team-gated/coordination-tiers.md`, `templates/modules/team-gated/doc-drift-prevention.md`, `templates/modules/team-gated/domain-agents.md`, `templates/modules/team-gated/dual-language-tests.md`, `templates/modules/team-gated/dual-review.md`, `templates/modules/team-gated/examples-gallery.md`, `templates/modules/team-gated/issue-capture.md`, `templates/modules/team-gated/issue-capture/reference/.github/ISSUE_TEMPLATE/bug.md`, `templates/modules/team-gated/issue-capture/reference/.github/ISSUE_TEMPLATE/friction.md`, `templates/modules/team-gated/issue-capture/reference/.github/ISSUE_TEMPLATE/gap.md`, `templates/modules/team-gated/issue-capture/reference/.github/ISSUE_TEMPLATE/wish.md`, `templates/modules/team-gated/issue-capture/reference/.gitlab/issue_templates/Bug.md`, `templates/modules/team-gated/issue-capture/reference/.gitlab/issue_templates/Friction.md`, `templates/modules/team-gated/issue-capture/reference/.gitlab/issue_templates/Gap.md`, `templates/modules/team-gated/issue-capture/reference/.gitlab/issue_templates/Wish.md`, `templates/modules/team-gated/issue-capture/reference/README.md`, `templates/modules/team-gated/legacy-agent.md`, `templates/modules/team-gated/model-selection.md`, `templates/modules/team-gated/portable-security-sweeps.md`, `templates/modules/team-gated/python-security.md`, `templates/modules/team-gated/security-review.md`, `templates/modules/team-gated/testing-discipline.md`, `templates/modules/team-gated/web-hosting-security.md`, `templates/onboarding/collaborative-team.md`, `templates/onboarding/high-rigor-legacy.md`, `templates/onboarding/solo-greenfield.md`, `templates/optional/CONTRIBUTING.md`, `templates/phase-0/README.md`, `templates/phase-0/project-profile-greenfield.md`, `templates/phase-0/project-profile-legacy.md`, `templates/phase-0/team-profile.md`, `templates/skills/session-end/SKILL.md`, `templates/skills/session-start/SKILL.md`.
- **G**: `templates/onboarding/collaborative-team.md`, `templates/onboarding/high-rigor-legacy.md`, `templates/onboarding/solo-greenfield.md`, `dev/modules/onboarding/agent-team-onboarding.md`, `dev/modules/onboarding/dev-tour.md`.
- **X**: `templates/core/AGENTS.md`, `templates/core/CHANGELOG.md`, `templates/core/NOTICE.md`, `templates/core/VENDOR.md`, `templates/core/dev/PLANNING.md`, `templates/core/dev/README.md`, `templates/core/dev/agent_collaboration.md`, `templates/core/dev/measurement/README.md`, `templates/core/dev/modules/README.md`, `templates/core/dev/plans/_template.md`, `templates/core/dev/proposals/_template.md`, `templates/core/dev/rules/README.md`, `templates/core/dev/strategy/README.md`, `templates/core/dev/strategy/_template.md`, `templates/core/dev/upstream/README.md`, `templates/core/dev/upstream/_template.md`, `dev/proposals/_template.md`, `dev/plans/_template.md`.
- **Z**: `AGENTS.md`, `README.md`, `bootstrap/REANCHOR_RUNBOOK.md`, `bootstrap/UPGRADE.md`, `bootstrap/fidelity-check.md`, `dev/agent_collaboration.md`, `dev/modules/claim-check.md`, `dev/modules/content-security.md`, `dev/modules/coordination-tiers.md`, `dev/modules/doc-drift-prevention.md`, `dev/modules/documentation-plan.md`, `dev/modules/dual-review.md`, `dev/modules/examples-gallery.md`, `dev/modules/incident-trackers.md`, `dev/modules/incident_log_template.md`, `dev/modules/issue-capture.md`, `dev/modules/model-selection.md`, `dev/modules/onboarding/agent-team-onboarding.md`, `dev/modules/onboarding/dev-tour.md`, `dev/modules/portable-security-sweeps.md`, `dev/modules/reflections.md`, `dev/modules/security-review.md`, `dev/modules/security-verification.md`, `dev/modules/testing-discipline.md`, `dev/plans/_template.md`, `dev/proposals/_template.md`, `dimensions/README.md`, `dimensions/age.md`, `dimensions/agent-team.md`, `dimensions/complexity.md`, `dimensions/human-team.md`, `dimensions/language.md`, `dimensions/size.md`, `docs/DOCUMENTATION_PLAN.md`, `docs/README.md`, `docs/agent-team-onboarding.md`, `docs/assets/assai-authority-boundaries.svg`, `docs/assets/assai-components.svg`, `docs/assets/assai-investigation-cycle.svg`, `docs/assets/cairn-banner.svg`, `docs/assets/dual-review-independence.svg`, `docs/assets/independent-scientific-check.svg`, `docs/assets/shared-record-across-sessions.svg`, `docs/assets/three-lanes-of-change.svg`, `docs/assets/two-ways-to-adopt.svg`, `docs/build-a-board-view.md`, `docs/code-map.md`, `docs/dev-tour.md`, `docs/further-reading.md`, `docs/getting-started.md`, `docs/glossary.md`, `docs/methodology/README.md`, `docs/methodology/collaboration-stance.md`, `docs/methodology/consolidation-review.md`, `docs/methodology/coordination.md`, `docs/methodology/doc-governance.md`, `docs/methodology/dual-review.md`, `docs/methodology/lifecycle-contract.md`, `docs/methodology/lifecycle.md`, `docs/methodology/onboarding.md`, `docs/methodology/plans.md`, `docs/methodology/proposals.md`, `docs/methodology/rationale.md`, `docs/methodology/roles.md`, `docs/methodology/runtime-contract.md`, `docs/methodology/session-routines.md`, `docs/plain-language.md`, `docs/quickstart.md`, `docs/related-practices.md`, `docs/release-process.md`, `docs/skills-compatibility.md`, `docs/solo-legacy-recipe.md`, `docs/tool-usage.md`, `docs/vision.md`, `docs/workflow-role.md`, `on-ramp/README.md`, `templates/README.md`, `templates/codebase-readiness-report.md`, `templates/core/AGENTS.md`, `templates/core/CHANGELOG.md`, `templates/core/NOTICE.md`, `templates/core/VENDOR.md`, `templates/core/dev/PLANNING.md`, `templates/core/dev/README.md`, `templates/core/dev/agent_collaboration.md`, `templates/core/dev/measurement/README.md`, `templates/core/dev/modules/README.md`, `templates/core/dev/plans/_template.md`, `templates/core/dev/proposals/_template.md`, `templates/core/dev/rules/README.md`, `templates/core/dev/strategy/README.md`, `templates/core/dev/strategy/_template.md`, `templates/core/dev/upstream/README.md`, `templates/core/dev/upstream/_template.md`, `templates/modules/README.md`, `templates/modules/default-on/claim-check.md`, `templates/modules/default-on/documentation-plan.md`, `templates/modules/default-on/documentation_plan_template.md`, `templates/modules/default-on/incident-trackers.md`, `templates/modules/default-on/incident_log_template.md`, `templates/modules/default-on/reflections-README.md`, `templates/modules/default-on/reflections.md`, `templates/modules/default-on/security-verification.md`, `templates/modules/team-gated/api-access-security.md`, `templates/modules/team-gated/architecture-review.md`, `templates/modules/team-gated/architecture_review_template.md`, `templates/modules/team-gated/content-security.md`, `templates/modules/team-gated/coordination-tiers.md`, `templates/modules/team-gated/doc-drift-prevention.md`, `templates/modules/team-gated/domain-agents.md`, `templates/modules/team-gated/dual-language-tests.md`, `templates/modules/team-gated/dual-review.md`, `templates/modules/team-gated/examples-gallery.md`, `templates/modules/team-gated/issue-capture.md`, `templates/modules/team-gated/issue-capture/reference/.github/ISSUE_TEMPLATE/bug.md`, `templates/modules/team-gated/issue-capture/reference/.github/ISSUE_TEMPLATE/friction.md`, `templates/modules/team-gated/issue-capture/reference/.github/ISSUE_TEMPLATE/gap.md`, `templates/modules/team-gated/issue-capture/reference/.github/ISSUE_TEMPLATE/wish.md`, `templates/modules/team-gated/issue-capture/reference/.github/labels.yml`, `templates/modules/team-gated/issue-capture/reference/.gitlab/issue_templates/Bug.md`, `templates/modules/team-gated/issue-capture/reference/.gitlab/issue_templates/Friction.md`, `templates/modules/team-gated/issue-capture/reference/.gitlab/issue_templates/Gap.md`, `templates/modules/team-gated/issue-capture/reference/.gitlab/issue_templates/Wish.md`, `templates/modules/team-gated/issue-capture/reference/.gitlab/labels.yml`, `templates/modules/team-gated/issue-capture/reference/README.md`, `templates/modules/team-gated/legacy-agent.md`, `templates/modules/team-gated/model-selection.md`, `templates/modules/team-gated/model_selection_mapping_stub.yml`, `templates/modules/team-gated/portable-security-sweeps.md`, `templates/modules/team-gated/python-security.md`, `templates/modules/team-gated/security-review.md`, `templates/modules/team-gated/testing-discipline.md`, `templates/modules/team-gated/web-hosting-security.md`, `templates/onboarding/collaborative-team.md`, `templates/onboarding/high-rigor-legacy.md`, `templates/onboarding/solo-greenfield.md`, `templates/optional/CONTRIBUTING.md`, `templates/phase-0/README.md`, `templates/phase-0/project-profile-greenfield.md`, `templates/phase-0/project-profile-legacy.md`, `templates/phase-0/team-profile.md`, `templates/skills/_data/vendor_targets.yml`, `templates/skills/session-end/SKILL.md`, `templates/skills/session-start/SKILL.md`.

For this table, each node is in `bootstrap/tests/test_review_stance_in_shipped_files.py`.

| Node | Files read | Disposition and reason |
|---|---|---|
| `test_review_section_carries_the_obligation` | A | RETIRE review obligation, single-pass and placement wording pins. |
| `test_plan_review_never_has_a_second_round` | A | RETIRE review obligation, single-pass and placement wording pins. |
| `test_the_stance_sits_in_the_review_section_only_once` | A | RETIRE review obligation, single-pass and placement wording pins. |
| `test_loop_document_roster_carries_the_obligation` | L | RETIRE roster obligation and old-ledger wording pins. |
| `test_team_roster_has_its_own_section_without_adding_roles` | L | RETIRE canonical roster wording; KEEP shipped team-roster slot markers and placement because the installer fills that slot. |
| `test_carrier_omits_the_old_vocabulary` | A + L | RETIRE negative vocabulary pins and their reintroduction controls. |
| `test_carrier_forbidden_patterns_recognize_their_examples` | `templates/core/AGENTS.md` + V | RETIRE examples and negative-ledger pattern controls after each applicable reintroduced term is shown. |
| `test_the_by_default_pin_ignores_case_and_wrapping` | `templates/core/AGENTS.md` | RETIRE case, wrapping and false-positive controls for negative wording patterns. |
| `test_a_sentence_saying_no_tool_reads_the_line_is_not_flagged` | `templates/core/AGENTS.md` | RETIRE case, wrapping and false-positive controls for negative wording patterns. |
| `test_module_omits_the_old_vocabulary` | M | RETIRE module positive or negative wording patterns. |
| `test_module_forbidden_patterns_recognize_their_examples` | `templates/modules/team-gated/dual-review.md` | RETIRE negative-pattern examples as part of the removed instrument. |
| `test_module_says_what_it_is_for` | M | RETIRE module positive or negative wording patterns. |
| `test_deleting_the_called_by_authority_sentence_is_reported` | A | RETIRE existing pattern deletion controls after the corresponding independent-copy report mutants and reviewer answer. |
| `test_deleting_the_plan_obligation_sentence_is_reported` | A | RETIRE existing pattern deletion controls after the corresponding independent-copy report mutants and reviewer answer. |
| `test_deleting_the_two_pass_sentence_is_reported` | A | RETIRE existing pattern deletion controls after the corresponding independent-copy report mutants and reviewer answer. |
| `test_security_cap_contract_is_present_and_each_surface_mutation_is_caught` | K | RETIRE cap wording patterns and controls only after each carrier and its mutation are demonstrated. |
| `test_adding_required_external_to_a_carrier_is_reported` | A + L | RETIRE negative vocabulary pins and their reintroduction controls. |
| `test_template_review_section_carries_the_obligation` | T | RETIRE template obligation or negative-vocabulary patterns. |
| `test_template_omits_the_old_vocabulary` | T | RETIRE template obligation or negative-vocabulary patterns. |
| `test_template_forbidden_patterns_recognize_their_examples` | `templates/core/dev/proposals/_template.md` | RETIRE negative-pattern examples. |
| `test_proposal_header_offers_only_usual_values` | P | RETIRE header, skeleton and deletion wording pins. |
| `test_plan_templates_keep_their_ruled_review_tokens` | N | RETIRE header, skeleton and deletion wording pins. |
| `test_plan_review_skeleton_names_its_security_obligation` | N | RETIRE header, skeleton and deletion wording pins. |
| `test_a_template_offers_external_only_beside_called_by` | T | RETIRE header adjacency or negative-stanza wording pins. |
| `test_proposal_pass_skeleton_asks_the_proposal_questions` | P | RETIRE header, skeleton and deletion wording pins. |
| `test_plan_pass_skeletons_ask_the_plan_and_code_questions` | N | RETIRE header, skeleton and deletion wording pins. |
| `test_a_template_has_no_coverage_line_stanza` | T | RETIRE header adjacency or negative-stanza wording pins. |
| `test_deleting_the_two_pass_sentence_from_a_proposal_template_is_reported` | P | RETIRE header, skeleton and deletion wording pins. |
| `test_deleting_the_obligation_sentence_from_a_plan_template_is_reported` | N | RETIRE header, skeleton and deletion wording pins. |
| `test_shipped_text_carries_the_obligation` | R excluding `bootstrap/fidelity-check.md` | RETIRE positive wording patterns for each mapped carrier. |
| `test_shipped_text_omits_the_old_wording` | R | RETIRE forbidden-wording patterns for each carrier. |
| `test_shipped_text_forbidden_patterns_recognize_their_examples` | `templates/modules/team-gated/model-selection.md` | RETIRE negative-pattern examples. |
| `test_the_model_selection_pair_is_byte_identical` | `dev/modules/model-selection.md`, `templates/modules/team-gated/model-selection.md` | KEEP equality of copies; RETIRE the separate canonical-obligation assertion. |
| `test_the_session_start_twins_are_byte_identical` | `.agents/skills/session-start/SKILL.md`, `templates/skills/session-start/SKILL.md` | KEEP equality of copies; RETIRE the separate canonical-obligation assertion. |
| `test_the_cleanup_row_never_says_usual` | `dev/modules/model-selection.md`, `templates/modules/team-gated/model-selection.md` | RETIRE positive or negative row and wording pins. |
| `test_the_cleanup_row_sits_in_the_role_table` | `dev/modules/model-selection.md`, `templates/modules/team-gated/model-selection.md` | RETIRE positive or negative row and wording pins. |
| `test_the_old_role_rows_are_gone` | `dev/modules/model-selection.md`, `templates/modules/team-gated/model-selection.md` | RETIRE positive or negative row and wording pins. |
| `test_the_fidelity_sample_roster_agrees_with_the_loop_document` | L, `bootstrap/fidelity-check.md` | KEEP comparisons between corresponding actual roster values; RETIRE hard-coded canonical roster. |
| `test_a_sample_roster_with_an_old_role_is_reported` | `templates/core/dev/agent_collaboration.md`, `bootstrap/fidelity-check.md` | KEEP comparison and drift control as parity evidence. |
| `test_doctrine_carries_the_statement` | J | RETIRE positive doctrine patterns, including the legacy-ledger prohibition. |
| `test_doctrine_omits_the_retired_privilege` | H | RETIRE negative patterns and their reintroduction controls; unsupported and constructed inputs remain blocked until covered. |
| `test_putting_a_retired_privilege_back_is_reported` | H | RETIRE negative patterns and their reintroduction controls; unsupported and constructed inputs remain blocked until covered. |
| `test_the_anchor_equals_the_approved_wording` | `docs/methodology/rationale.md` | RETIRE canonical anchor wording and its rewording control. |
| `test_a_reworded_anchor_is_reported` | `docs/methodology/rationale.md` | RETIRE canonical anchor wording and its rewording control. |
| `test_the_two_trap_headings_are_adjacent_and_in_order` | `docs/methodology/dual-review.md` | RETIRE fixed heading/ordering pin. |
| `test_no_live_document_cites_a_heading_that_does_not_exist` | W | RETIRE retired-name patterns only after every dynamically walked carrier and a negative mutant is covered; maintain applicable link checks. |
| `test_no_live_document_credits_a_checker_that_does_not_exist` | W | RETIRE retired-name patterns only after every dynamically walked carrier and a negative mutant is covered; maintain applicable link checks. |
| `test_dimensions_omit_the_old_wording` | D | RETIRE positive or negative wording patterns, each carrier separately. |
| `test_dimensions_forbidden_patterns_recognize_their_examples` | `dimensions/complexity.md` | RETIRE negative-pattern examples. |
| `test_dimensions_page_carries_the_obligation` | D | RETIRE positive or negative wording patterns, each carrier separately. |
| `test_the_complexity_cell_still_names_the_scientific_check` | `dimensions/README.md` | RETIRE exact presence pin. |
| `test_the_upgrade_guides_plan_pass_examples_are_not_external` | `bootstrap/UPGRADE.md` | RETIRE positive and negative example patterns and their reintroduction control. |
| `test_putting_an_external_example_back_in_the_upgrade_guide_is_reported` | `bootstrap/UPGRADE.md` | RETIRE positive and negative example patterns and their reintroduction control. |
| `test_readme_explains_the_review_contract` | `README.md` | RETIRE positive patterns and their deletion and alternate-wording controls. |
| `test_removing_a_readme_review_rule_is_detected` | `README.md` | RETIRE positive patterns and their deletion and alternate-wording controls. |
| `test_equivalent_readme_wording_preserves_the_rule` | `README.md` | RETIRE positive patterns and their deletion and alternate-wording controls. |
| `test_the_review_figure_keeps_an_accessible_conclusion` | `docs/assets/dual-review-independence.svg` | RETIRE canonical title wording; KEEP XML parsing, aria-labelledby and description/title relation. |
| `test_the_figure_parses_and_keeps_its_embed_geometry` | `docs/assets/dual-review-independence.svg` | KEEP XML parsing and embed geometry behavior. |
| `test_the_figure_carries_no_old_phrase` | `docs/assets/dual-review-independence.svg` | RETIRE forbidden wording only after unsupported-file evidence and each relevant negative mutant. |
| `test_descriptive_page_omits_the_old_wording` | Q | RETIRE forbidden wording, each carrier separately, including SVG only after its evidence gate. |
| `test_descriptive_forbidden_patterns_recognize_their_examples` | `README.md` | RETIRE negative-pattern examples. |
| `test_descriptive_page_carries_the_obligation` | `docs/glossary.md`, `docs/vision.md`, `docs/tool-usage.md`, `on-ramp/README.md` | RETIRE positive obligation patterns. |
| `test_an_installed_onboarding_copy_equals_its_page` | `docs/agent-team-onboarding.md`, `dev/modules/onboarding/agent-team-onboarding.md`, `docs/dev-tour.md`, `dev/modules/onboarding/dev-tour.md` | KEEP equality of each corresponding copy; RETIRE separate forbidden-wording assertion. |
| `test_an_empty_carrier_satisfies_no_obligation_pattern` | none (pattern constants only) | RETIRE empty-carrier control of retired wording patterns. |
| `test_a_copy_that_drifts_from_its_page_is_reported` | `docs/agent-team-onboarding.md`, `dev/modules/onboarding/agent-team-onboarding.md` | KEEP copy equality and drift control. |
| `test_the_preset_glob_holds_every_shipped_preset` | G (paths only) | RETIRE enumeration control for the retired negative wording scan. |
| `test_a_preset_names_no_review_tier_anyone_fills` | G | RETIRE negative wording scan, each preset separately. |
| `test_each_retired_literal_matches_its_historic_sentence` | `templates/onboarding/solo-greenfield.md` | RETIRE positive/negative controls for retired wording instrument. |
| `test_putting_a_retired_sentence_back_in_a_preset_is_reported` | `templates/onboarding/solo-greenfield.md`, `templates/onboarding/collaborative-team.md`, `templates/onboarding/high-rigor-legacy.md` | RETIRE reintroduction controls after each applicable mutant is shown. |
| `test_a_correctly_worded_sentence_is_not_flagged` | `templates/onboarding/solo-greenfield.md` | RETIRE positive/negative controls for retired wording instrument. |
| `test_a_mergeable_template_has_no_one_word_placeholder_the_engine_cannot_fill` | X; `bootstrap/_scaffold/config.py`, `bootstrap/_scaffold/slotmerge.py` | KEEP engine-token behavior: unknown placeholders prevent upgrades. |
| `test_the_mergeable_template_list_covers_the_authoring_templates` | X (paths only) | KEEP enumeration control for the template-token behavior test. |
| `test_a_one_word_placeholder_in_an_authoring_template_is_reported` | T; `bootstrap/_scaffold/config.py`, `bootstrap/_scaffold/slotmerge.py` | KEEP known/unknown token behavior and mutation control. |
| `test_every_file_with_a_phrasing_hit_is_exempt_for_a_reason` | Z | RETIRE old-wording scan and its exemption/coverage controls only after all read files and each applicable negative mutant are accounted for. |
| `test_no_exemption_is_stale` | Z | RETIRE old-wording scan and its exemption/coverage controls only after all read files and each applicable negative mutant are accounted for. |
| `test_no_file_an_adopter_receives_is_exempt` | none (exemption and path constants only) | RETIRE exemption-list controls coupled to the removed old-wording scan. |
| `test_removing_an_exemption_is_reported` | Z | RETIRE old-wording scan and its exemption/coverage controls only after all read files and each applicable negative mutant are accounted for. |
| `test_a_phrase_inserted_into_a_scanned_copy_is_reported` | Z | RETIRE old-wording scan and its exemption/coverage controls only after all read files and each applicable negative mutant are accounted for. |
| `test_exempting_an_installed_file_is_reported` | none (exemption and path constants only) | RETIRE exemption-list controls coupled to the removed old-wording scan. |
| `test_the_walk_reaches_the_roots_it_claims` | Z | RETIRE old-wording scan and its exemption/coverage controls only after all read files and each applicable negative mutant are accounted for. |

For the next table, each node is in `bootstrap/tests/test_review_sweep_ships.py`. A, L and M have the same meanings above. Profile fixtures run every `bootstrap/profiles/*.yml` profile: `solo-greenfield.yml`, `collaborative-team.yml`, and `high-rigor-legacy.yml`. Installed-set names below are destination paths in each generated tree.

- **SG**: `AGENTS.md`, `dev/proposals/_template.md`, `dev/plans/_template.md`, `docs/methodology/proposals.md`, `docs/methodology/plans.md`, `docs/methodology/lifecycle.md`, `templates/core/AGENTS.md`, `templates/core/dev/proposals/_template.md`, `templates/core/dev/plans/_template.md`.
- **SGI**: `AGENTS.md`, `dev/proposals/_template.md`, `dev/plans/_template.md`.
- **PC**: `AGENTS.md`, `dev/plans/_template.md`, `templates/core/dev/PLANNING.md`, `docs/methodology/lifecycle.md`, `docs/methodology/plans.md`, `templates/core/AGENTS.md`, `templates/core/dev/plans/_template.md`.
- **PCI**: `AGENTS.md`, `dev/plans/_template.md`, `dev/PLANNING.md`.
- **RW**: `AGENTS.md`, `templates/core/AGENTS.md`, `dev/agent_collaboration.md`, `templates/core/dev/agent_collaboration.md`, `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, `docs/methodology/proposals.md`, `docs/methodology/plans.md`, `docs/methodology/session-routines.md`, `templates/skills/session-end/SKILL.md`, `.agents/skills/session-end/SKILL.md`.
- **RWI**: `AGENTS.md`, `dev/agent_collaboration.md`, `.agents/skills/session-end/SKILL.md`.

| Node | Files read | Disposition and reason |
|---|---|---|
| `test_source_smart_goal_guidance` | SG | RETIRE positive wording patterns and their entrypoint deletion/contrary controls, each carrier separately. |
| `test_source_smart_goal_mutations_fail_entrypoint` | SG | RETIRE positive wording patterns and their entrypoint deletion/contrary controls, each carrier separately. |
| `test_installed_smart_goal_guidance` | installed SGI for every profile | RETIRE positive wording patterns and their entrypoint mutation controls; KEEP real installs and source-to-destination correspondence for every profile. |
| `test_installed_smart_goal_mutations_fail_entrypoint` | installed SGI for every profile | RETIRE positive wording patterns and their entrypoint mutation controls; KEEP real installs and source-to-destination correspondence for every profile. |
| `test_source_plan_completion_rule_and_surface_mutation` | PC | RETIRE positive completion patterns and their deletion controls for each carrier. |
| `test_expected_ast_mismatch_disposition_is_cairn_local` | A | RETIRE local positive and shipped negative phrase pins. |
| `test_source_readable_work_obligation_and_mutation` | RW | RETIRE source wording patterns and their separate-copy deletion controls. |
| `test_installed_readable_work_obligation_and_mutation` | installed RWI for every profile | RETIRE installed wording patterns and their separate-copy controls; KEEP real installs and source-to-destination correspondence. |
| `test_source_sweep_carries_the_obligation` | L | RETIRE wording, order and negative-leak pins. |
| `test_the_sweep_precedes_the_scope_reduction_trap` | L | RETIRE wording, order and negative-leak pins. |
| `test_the_lens_roster_is_exactly_nine_in_the_doctrines_order` | L | RETIRE wording, order and negative-leak pins. |
| `test_the_anchors_a_follower_writes_against_are_present` | L | RETIRE wording, order and negative-leak pins. |
| `test_the_ledger_is_defined_once_with_five_items` | L | RETIRE wording, order and negative-leak pins. |
| `test_the_sweep_leaves_the_doctrines_reasoning_out` | L | RETIRE wording, order and negative-leak pins. |
| `test_the_leak_pattern_matches_the_doctrine_it_guards_against` | `docs/methodology/dual-review.md`, `templates/core/dev/agent_collaboration.md` | RETIRE positive and negative controls for the doctrine-leak wording instrument. |
| `test_the_sweep_is_body_text_not_a_slot` | L | KEEP slot-exclusion check: slot content freezes on upgrade, so moving guidance into one changes install behavior. |
| `test_agents_md_pointer_carries_the_obligation` | A | RETIRE pointer and negative-path wording pins. |
| `test_the_pointer_names_no_test_path` | A | RETIRE pointer and negative-path wording pins. |
| `test_installed_loop_document_carries_the_obligation` | installed `dev/agent_collaboration.md` for every profile | RETIRE wording patterns; KEEP real installs and source-to-installed correspondence. |
| `test_installed_agents_md_carries_the_pointer` | installed `AGENTS.md` for every profile | RETIRE pointer wording; KEEP real installs and source-to-installed correspondence. |
| `test_installed_plan_completion_and_surface_mutation` | installed PCI for every profile | RETIRE wording and deletion controls; KEEP real installs and corresponding source-to-destination checks. |
| `test_an_install_without_the_sweep_is_reported` | installed `dev/agent_collaboration.md` for every profile | RETIRE the pattern instrument deletion control; KEEP real-install and source-to-installed correspondence with a meaningful missing-output control. |
| `test_deleting_lens_4_is_reported` | L | RETIRE existing wording-pattern controls after corresponding independent-copy mutants are shown. |
| `test_deleting_the_not_covered_half_is_reported` | L | RETIRE existing wording-pattern controls after corresponding independent-copy mutants are shown. |
| `test_deleting_the_scope_sentence_is_reported` | L | RETIRE existing wording-pattern controls after corresponding independent-copy mutants are shown. |
| `test_adding_a_sixth_ledger_item_is_reported` | L | RETIRE existing wording-pattern controls after corresponding independent-copy mutants are shown. |
| `test_an_install_leaves_no_placeholder_the_engine_cannot_fill` | all installed .md/.yml/.txt for every profile; `bootstrap/_scaffold/config.py`, `bootstrap/_scaffold/slotmerge.py` | KEEP real install and unfilled token behavior; unknown placeholders prevent upgrades. |
| `test_the_module_carries_no_lens_citation_rule_or_ledger` | M | RETIRE duplicate-guidance negative patterns. |
| `test_restoring_the_roster_into_the_module_is_reported` | M, `templates/core/dev/agent_collaboration.md` | RETIRE negative-pattern reintroduction controls after each corresponding mutant. |
| `test_restoring_the_citation_rule_into_the_module_is_reported` | M, `templates/core/dev/agent_collaboration.md` | RETIRE negative-pattern reintroduction controls after each corresponding mutant. |
| `test_restoring_the_ledger_into_the_module_is_reported` | M, `templates/core/dev/agent_collaboration.md` | RETIRE negative-pattern reintroduction controls after each corresponding mutant. |

For the next table, each node is in `bootstrap/tests/contract/test_model_tier_rule_ships.py`; A is the same pair above. The two fixture profiles are `bootstrap/profiles/solo-greenfield.yml` and `bootstrap/profiles/collaborative-team.yml`.

| Node | Files read | Disposition and reason |
|---|---|---|
| `test_both_agents_copies_carry_the_model_tier_rule` | A | RETIRE positive clause patterns, each source separately. |
| `test_task_floors_reject_lane_based_assignment_and_unreviewed_low_authority` | `AGENTS.md` | RETIRE clause patterns and contrary-wording controls after each report mutant. |
| `test_the_rule_reads_the_same_in_both_copies` | A | KEEP model-tier rule equality with its documented Cairn-local difference; RETIRE separate canonical retry-clause and old-wording pins. |
| `test_the_rule_sits_under_roles` | A | RETIRE fixed label and placement wording pins. |
| `test_deleting_the_name_the_model_sentence_is_reported` | `AGENTS.md` | RETIRE deletion control after the corresponding independent-copy mutant. |
| `test_a_profile_with_no_module_still_installs_the_rule` | installed `AGENTS.md`, installed `dev/modules/model-selection.md` existence | RETIRE fixed clause and retry wording pins; KEEP real solo install, module-absence behavior and source-to-installed guidance correspondence. |
| `test_collaborative_profile_installs_rule_and_preserves_module_safeguards` | installed `AGENTS.md`, installed `dev/modules/model-selection.md` | RETIRE fixed clause, retry and module-wording pins; KEEP real collaborative install, module presence and source-to-installed guidance correspondence. |
| `test_each_retry_clause_fails_when_removed_from_a_physical_copy` | `docs/methodology/roles.md`, installed `AGENTS.md` from solo and collaborative profiles | RETIRE wording-clause patterns and controls; KEEP real installs and source-to-installed correspondence. |
| `test_core_source_retry_limit_mutation_reaches_each_real_install` | `templates/core/AGENTS.md`; installed `AGENTS.md` and model-module presence for both profiles; scaffold and profile inputs | RETIRE canonical clause assertion; KEEP real install, source mutation propagation to each installed output, and profile-specific module presence/absence. Replace literal-coupled assertion with a corresponding source/output behavior check. |
| `test_the_different_maker_condition_is_gone_and_same_tier_is_excluded` | `docs/methodology/roles.md`, `dev/modules/model-selection.md`, `templates/modules/team-gated/model-selection.md` | RETIRE positive and negative wording patterns and their controls; preserve corresponding module-copy parity where actually asserted elsewhere. |
| `test_proposal_authoring_and_ordinary_review_are_medium` | A; `docs/methodology/roles.md`, `dev/modules/model-selection.md`, `templates/modules/team-gated/model-selection.md` | RETIRE hard-coded task-floor wording patterns; KEEP actual comparisons between corresponding copies where asserted. |

**Coverage and follow-through**: the High clarification in this plan specifies bounded literal evidence for unsupported and Python gaps, with `NOT COMPARED` preserved. That design and the new Cairn roots are not themselves proof of any individual mutation. Shell comments and SVG wording are among the affected cases. Demonstrate each applicable dropped-obligation, removal or reintroduced-term mutant in a separate copy and obtain the reviewer answer before its pin is removed. Preserve SVG parsing, accessibility relationships and geometry, slot behavior, copy parity, placeholder/upgrade behavior, real installations and the Maintainer-retained drain node. The exact installed files read by a whole-tree placeholder scan must be enumerated from each actual install when verifying that behavior.

**Elapsed**: unknown. **Tokens**: unknown.

## Maintainer Decision amendment notice -- Claude Opus 5.5 (Strategy) -- 2026-11-08

Relayed at the Maintainer's request; they cannot reach this plan's agent
directly. This is a notice, not an edit to operative cells: the Scope delta
and its placement remain the plan author's.

Commit `0d2fc71f` on `0.7-dev` appends a Decision amendment to both archived
source proposals. The Maintainer's authorization, verbatim:

> "Move the testing rule out of AGENTS.md into the templates and testing module; keep the editing rule to one sentence"

For this plan: `a61af064` adds a "Functional prose" section and a
review-question paragraph to `AGENTS.md` and `templates/core/AGENTS.md`.
Under the amendment each file keeps one sentence for the editing rule (edit
by exact replacement or patch, never regenerate; point to the tools). The
review question moves to the review sections of the proposal, plan and
code-review templates. The trivial-lane obligation (the `prose_diff.py`
report in the commit body; a removed or changed rule makes the edit
non-trivial) needs a stated home, inside the sentence or in the
content-security module, so it is not lost. Record the Scope delta here.

**Elapsed**: under 5 minutes. **Tokens**: unknown.

## Scope delta -- Maintainer Decision amendment -- GPT-6 Luna LowImplementation -- 2026-11-08

**Source:** Decision amendment `0d2fc71f` on `0.7-dev` and its relayed
notice `392e2db3`. The Maintainer authorized: “Move the testing rule out of
AGENTS.md into the templates and testing module; keep the editing rule to one
sentence”. **Elapsed:** under 5 minutes. **Tokens:** unknown.

The local and shipped `AGENTS.md` copies now keep one functional-prose rule
sentence; it retains exact replacement/patch, no regeneration or rewrapping,
commit-body rule-change listing, and the trivial-lane report plus
reclassification duty. The review question remains in local and shipped
proposal and plan template review sections, including the plan's code-review
section; it no longer appears as a second paragraph in `AGENTS.md`. Tools,
coverage, install, pin outcomes, the Maintainer-retained drain pin and heavy
tier are unchanged. No prior review record was removed.

## Implementation constraint -- GPT-6.1 Terra (Implementation support) -- 2026-11-08

The Maintainer directed: "Also, with today's testing plan, we absolutely must achieve a reduction in test volume". Measure a net reduction across the companion promise-testing and functional-prose work, including added tooling, loader and mutation-support tests. Report test definitions and collected parameter-expanded cases before and after, with support-code footprint for context. Preserve promised public behavior, refusals and hostile-state coverage; do not hide or rename discovery or merely pack assertions to manufacture a reduction.

Elapsed: under one minute; tokens: unknown.


## C2 first mutant evidence batch -- GPT-6 Luna LowImplementation -- 2026-11-08

This is an evidence checkpoint, not deletion authority. The node below still
contains its pins. Its nine collected cases passed on the unmutated committed
base (`d5436fe5`) with Python 3.13.13: `python -m pytest
bootstrap/tests/contract/test_review_and_verification_rules_ship.py::test_light_tier_can_ship_wide_work_without_a_plan -q` (9 passed, 0.02 s).

Each mutant is a separate committed clone of `d5436fe5`. The existing source
report was run as
`/Users/kendal30/conda_envs/lhm/bin/python3.13 templates/modules/team-gated/prose_diff.py d5436fe5 HEAD`.
Every result was one complete `CHANGED <carrier>: before <text>; after
<text>` line, with no incomplete or not-compared notice. The nine carriers are
covered by the committed content-scan and prose-root union. These edits are
intentional adverse mutants for reviewer judgment; none is an accepted source
change. The report proves the listed text change is visible, not that the
mutant is safe or that the operative promise survives elsewhere.

| Case | Separate mutant commit | Reported complete before -> after |
|---|---|---|
| `AGENTS.md` | `d1a10add` | `light has no plan even for multi-area or wide implementation` -> `light tier may require a plan for wide implementation` |
| `templates/core/AGENTS.md` | `b16fbce7` | `light has no plan even for multi-area or wide implementation` -> `light tier may require a plan for wide implementation` |
| `docs/methodology/lifecycle.md` | `99473406` | `` `light` is one short review and no plan even when execution spans multiple areas or needs wide Boundary B `` -> `light work may require a plan for multiple areas or wide Boundary B` |
| `docs/methodology/proposals.md` | `b97b639c` | `a light-tier proposal has no plan or code review, regardless of implementation size` -> `a light-tier proposal may require a plan and code review, regardless of implementation size` |
| `docs/methodology/plans.md` | `405ccb02` | `Light has one short proposal review and no plan regardless of these conditions` -> `Light may require a plan regardless of these conditions` |
| `dev/proposals/_template.md` | `2f1bf0da` | `for light, use \`not required(no plan: light tier)\` even for multi-area or wide work` -> `for light, use \`required(Internal)\` even for multi-area or wide work` |
| `templates/core/dev/proposals/_template.md` | `f2fce2a0` | Same template phrase -> `for light, use \`required(Internal)\` even for multi-area or wide work` |
| `dev/plans/_template.md` | `bcbb43df` | `Light has no plan, even for multi-area or wide work` -> `Light may require a plan, even for multi-area or wide work` |
| `templates/core/dev/plans/_template.md` | `390455aa` | Same plan-template phrase -> `Light may require a plan, even for multi-area or wide work` |

The mutant trees remain in `/private/tmp/cairn-mutant-own-agents`,
`/private/tmp/cairn-functional-prose-mutants`, and the seven
`/private/tmp/cairn-mutant-*` clones named by the table. A fresh Medium reader
must decide from these reports whether they make the removed obligation
visible and whether the source promise would be weakened before any pin is
removed. No install, parity, slot, placeholder, accessibility, hostile-state,
or drain behavior was changed in this batch.

**Elapsed**: approximately 20 minutes. **Tokens**: unknown.


## C2 review-stance pin mutants -- GPT-6 Luna LowImplementation -- 2026-11-08

This batch is proof only; no carrier or test was changed. The 68 collected
cases of `test_review_section_carries_the_obligation` passed on the current
committed implementation with Python 3.13.13 (0.13 s). Each case has a
separate adversarial branch commit based on `d5436fe5`: one obligation phrase
removed from the `## Review` section of one actual carrier. The existing
`templates/modules/team-gated/prose_diff.py` command was run for each commit
against `d5436fe5`; all 68 reports returned a complete `CHANGED` line, with
no `INCOMPLETE` or `NOT COMPARED` result. The transcript and clone are in
`/private/tmp/cairn-c2-stance-mutants.tsv` and
`/private/tmp/cairn-c2-stance-mutants`; these are temporary proof inputs,
not shipped project artifacts. The changed text can be inspected and the
report repeated on each `c2-01` through `c2-68` branch.

| Obligation label | Shipped `templates/core/AGENTS.md` mutant | Own `AGENTS.md` mutant |
|---|---|---|
| `a-call-names-one-artifact-that-exists-now` | `46ab004c` | `18d4e75e` |
| `a-called-brief-adds-focus-and-removes-no-owed-answer` | `aedf73c2` | `f332de88` |
| `a-called-by-line-never-confers-authority` | `0e7c4951` | `ecc929d1` |
| `a-called-read-adds-and-replaces-nothing` | `df4213cd` | `4c6d4634` |
| `a-called-read-discharges-no-security-review-by-distance-or-brief` | `6449fe56` | `81f689dd` |
| `a-clean-code-review-shows-a-falsification-ledger` | `a85bbd95` | `7297fd53` |
| `a-clean-pass-needs-evidenced-answers-and-named-gaps` | `ebd656a8` | `2c79b713` |
| `a-fresh-reviewer-on-the-works-side` | `a8b7b640` | `c1ce4adf` |
| `a-high-risk-surface-takes-a-security-review` | `a74568af` | `5ee09ec2` |
| `a-narrowing-is-a-scope-change-only-the-maintainer-concedes` | `383c7f1f` | `05c5fd1e` |
| `a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line` | `e8314827` | `2578d419` |
| `a-roster-you-set-is-not-a-call` | `c8c5acc4` | `d4c76613` |
| `a-standing-call-is-a-floor-and-returns-only-by-proposal` | `fd12290b` | `91933fc5` |
| `an-agent-may-name-a-risk-and-coverage-gap` | `8fd8dd88` | `78844e34` |
| `called-by-carries-the-maintainers-words-verbatim` | `b49353ee` | `8f3ecdb9` |
| `called-by-names-where-the-words-live` | `42830414` | `ba3f146c` |
| `called-by-quote-is-repeated-in-the-commit-body` | `08d34dfc` | `e605d91b` |
| `code-review-floor-is-not-the-implementing-agent` | `e0905bd4` | `b12e2343` |
| `code-review-never-reopens-the-decision` | `e90f1c28` | `9e17fc43` |
| `distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so` | `cd2464ee` | `c723c6de` |
| `external-means-the-maintainer-called-it` | `0e94f068` | `69242772` |
| `foundations-block-three-answers-each-with-its-evidence` | `08d4f62b` | `bd059ec5` |
| `improve-means-recommend` | `ab18653d` | `ccf580d7` |
| `no-agent-declares-external-required-or-recommends-distance` | `e5051de4` | `df332f49` |
| `no-agent-picks-a-kind-of-review` | `fe0f728b` | `2eec6c07` |
| `no-quota-of-findings` | `b6ac6dff` | `eb4a4a9b` |
| `no-tool-reads-the-obligation-line-a-reader-does` | `46a09aee` | `bc308f2d` |
| `nothing-checks-the-quote-a-reader-does` | `317b4d59` | `28ee5e98` |
| `one-stance-at-every-stage` | `2f78982d` | `9d307e78` |
| `other-authority-lives-in-a-decision-or-a-plan-fence` | `3a991cd8` | `14b02370` |
| `plan-review-is-fresh-context` | `d90502e2` | `46bad743` |
| `the-stage-sets-three-questions` | `73bc59d7` | `f8cdd3b8` |
| `tier-external-needs-called-by-else-read-as-the-usual-review` | `f47ae2cc` | `6ac040ab` |
| `usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second` | `e3fea9d5` | `994c229e` |


Examples from the captured output: `46ab004c` changed “The Maintainer alone
calls an External read on one named artifact that exists now.” to “The
Maintainer alone calls an External read on .”; `aedf73c2` changed “The call
adds focus, removes no owed answer, replaces no usual review, clears no
Security Review and grants no Decision or plan-fence authority.” to “The ,
replaces no usual review, clears no Security Review and grants no Decision
or plan-fence authority.” These are complete reporter results, not a claim
that either mutant is acceptable. The transcript has all 68 exact
before/after results.

A fresh Medium reader still needs to answer from these results whether this
pin inventory is useful to remove and whether the required obligations remain
visible after the proposed tests retire. Until that answer, retain all pins.
No install, copy-parity, slot, placeholder, accessibility, hostile-state, or
drain behavior was modified. **Elapsed**: approximately 55 minutes. **Tokens**:
unknown.


## C2 additional text-pin mutants -- GPT-6 Luna LowImplementation -- 2026-11-08

This adds ten candidate cases to the two earlier evidence batches, bringing
the proof set to 87 collected cases before any deletion. It does not remove
pins. On `bcb026f7`, the five targeted test nodes collected and passed all ten
cases with Python 3.13.13 (0.05 s). Each case has an independent adverse
commit in `/private/tmp/cairn-c2-stance-mutants`, based on `d5436fe5`; the
report was run on every branch using the existing source module and returned
a complete `CHANGED` or `ADDED` result without an incomplete or not-compared
notice. The transcript is `/private/tmp/cairn-c2-10-mutants.tsv`.

| Test case | Mutant commit | Complete report evidence |
|---|---|---|
| `test_plan_review_never_has_a_second_round` — own AGENTS | `7c042331` | `Plan review is one pass.` -> `Plan review may have a second pass.` |
| `test_plan_review_never_has_a_second_round` — shipped AGENTS | `5a9677c6` | Same rule -> `Plan review may have a second pass.` |
| `test_the_stance_sits_in_the_review_section_only_once` — own AGENTS | `ea81f0b4` | `The stage sets the questions` -> `The stage does not set the questions` |
| `test_the_stance_sits_in_the_review_section_only_once` — shipped AGENTS | `e24b57ab` | Same sentence -> `The stage does not set the questions` |
| `test_the_shipped_copy_makes_claiming_conditional` | `9ec0c0f5` | `claimed first if the project uses file claims` -> `claimed first whether or not the project uses file claims` |
| `test_cairns_own_copy_claims_unconditionally` | `0f9580f1` | `claimed first, and committed by explicit path` -> `claimed first if the project uses file claims, and committed by explicit path` |
| `test_carrier_omits_the_old_vocabulary` — shipped AGENTS | `5b7786ce` | `ADDED ... [sentence]: Code review is External by default.` |
| `test_carrier_omits_the_old_vocabulary` — own AGENTS | `c3091c14` | `ADDED ... [sentence]: Code review is External by default.` |
| `test_carrier_omits_the_old_vocabulary` — shipped review-loop document | `43fb67ac` | `ADDED ... [sentence]: Code review is External by default.` |
| `test_carrier_omits_the_old_vocabulary` — own review-loop document | `90e349f1` | `ADDED ... [sentence]: Code review is External by default.` |

The commits above are separate proof branches `c2-69` through `c2-78`; every
changed carrier is in the committed base-root union. The addition mutants
reintroduce a forbidden claim only in the temporary copies. The two claim
mutants demonstrate a lost distinction only in those copies. The original
AGENTS files and tests are unchanged.

A single fresh Medium reader can now assess these ten cases with the prior
nine-case light-tier batch and 68 review-stance cases. The total 87 is an
evidence candidate, not a realized test reduction; keep all source pins until
the reader answers whether the reporter shows the changed obligation clearly
and whether removal preserves the accepted rule. The temp transcript and
branches are not project artifacts. **Elapsed**: approximately 8 minutes.
**Tokens**: unknown.


## C2 governing AGENTS obligation mutants -- GPT-6 Luna LowImplementation -- 2026-11-08

This batch is proof only; neither AGENTS copy nor its tests were changed. At
`c97c5d66`, the targeted node `test_agents_md_carries_the_obligation` passed
68/68 cases on Python 3.13.13 (0.12 s). Every one of its 34 labels was removed
from each actual carrier in a separate branch commit based on `d5436fe5`. The
committed source report returned one complete `CHANGED` result for each of all
68 mutants, with no `INCOMPLETE` or `NOT COMPARED` result. Both carriers are
covered by the current content-scan/prose-root union. The transcript and
branch clone are `/private/tmp/cairn-c2-agents-obligation-mutants.tsv` and
`/private/tmp/cairn-c2-stance-mutants`; branch names are `c2-79` through
`c2-146`.

| Obligation label | Shipped `templates/core/AGENTS.md` mutant | Own `AGENTS.md` mutant |
|---|---|---|
| `a-plan-appends-its-verification-section` | `44168e75` | `771bd9d1` |
| `a-set-claim-is-the-mutation-trigger` | `fafa17ed` | `d9d3347d` |
| `a-trivial-change-maps-to-the-tests-that-own-its-surface` | `d5d5c5f2` | `d0e78d20` |
| `a-trivial-change-runs-on-exact-candidate-bytes` | `e9d27ae6` | `097245d0` |
| `an-equivalent-mutant-passes-the-behaviour-test` | `03583ce9` | `02ecff2d` |
| `boundary-b-governs-a-trivial-change` | `37df3aaf` | `ec22d23c` |
| `bounded-mode-covers-affected-behavior-and-consumers` | `d34f2671` | `ca607b4d` |
| `bounded-record-names-touched-surfaces-and-tests` | `18632903` | `68fdab6f` |
| `candidate-inspection-includes-staged-and-unstaged-bytes` | `6447affc` | `043838e5` |
| `changed-bytes-are-reinspected` | `a1c4e3b1` | `491007be` |
| `contract-and-trust-surfaces-use-wide-mode` | `b03337ac` | `2e277b5b` |
| `equivalence-is-measured-not-argued` | `1f40e995` | `2dc7da7b` |
| `failed-serialization-uses-separate-worktrees` | `a2d128ad` | `0bc2409b` |
| `figures-are-measured-on-the-commit` | `504c44db` | `870e43d9` |
| `foreign-or-uncertain-content-stops-commit` | `7efcbc36` | `ae7081be` |
| `governing-text-omissions-are-reported` | `5d7e9fdd` | `7290f578` |
| `ledger-never-reports-a-bare-count` | `88419998` | `5cb92e10` |
| `ledger-reports-each-mutant-against-a-control` | `8e0df608` | `119a7c8c` |
| `mutation-is-otherwise-the-reviewers-choice` | `337335fc` | `a7e1c4bf` |
| `no-reverting-commands-in-a-shared-tree` | `af7fb9dc` | `ea0cc78d` |
| `noncooperating-writer-limit-is-explicit` | `60700885` | `4f5705ae` |
| `other-writes-go-to-a-separate-copy` | `12943fb0` | `fed6590d` |
| `passing-known-checks-identifies-the-verified-commit` | `ee50ba8d` | `3de89858` |
| `pinned-prose-is-substantive` | `bdbcb363` | `071d0bec` |
| `review-reads-a-commit` | `36373475` | `a1ded34f` |
| `reviewer-writes-only-its-own-record` | `167ce3d1` | `8c993638` |
| `set-claims-are-listed-from-the-tree-and-mutated` | `04ecdb22` | `6c53e38c` |
| `shared-paths-are-serialized-through-commit` | `d21782a7` | `ba264b8b` |
| `substantive-surface-is-defined` | `32428ff7` | `93a6e8e5` |
| `tests-are-selected-by-file-reference` | `ba3801b5` | `08734080` |
| `trust-ceremony-surface-is-defined` | `910446c9` | `3d99aafd` |
| `unmeasured-equivalence-is-a-survivor` | `32ee0eea` | `8f3985f3` |
| `unpinned-prose-on-a-high-risk-surface-runs-the-prose-gates` | `61ff0ace` | `ef9c293a` |
| `wide-mode-covers-known-families-and-public-paths` | `3e1059a3` | `6deb98a4` |


Examples from the complete reporter output: `44168e75` removed “The author
appends the record under `## Implementation verification -- <agent> --
YYYY-MM-DD`”; `fafa17ed` removed “A claim that a value reaches every member
of a set”. Their after-text respectively begins “-- <agent> -- YYYY-MM-DD` in
the plan” and “requires listing the set from the tree and mutating each member
in a separate copy.” The transcript contains all 68 full before/after lines.

This is the second high-yield text-only node; its 68 cases are candidates for
retirement only after the fresh Medium reader answers the rule-weakening
question from the output. No certification command or trigger was edited, and
no behavior, parity, install, slot, placeholder, hostile-state or drain check
was changed. Do not treat the 68-case evidence as a realized volume reduction.
**Elapsed**: approximately 55 minutes. **Tokens**: unknown.


## C2 authoring-template obligation mutants -- GPT-6 Luna LowImplementation -- 2026-11-08

This batch is proof only; no template or pin test was changed. At `1ebcfcd0`,
the targeted `test_template_review_section_carries_the_obligation` node passed
118/118 cases with Python 3.13.13 (0.20 s). Its 118 cases cover the own and
shipped proposal and plan templates. Each case has its own adverse commit from
`d5436fe5`, removing the tested obligation pattern inside that template's
Review section. The existing source report returned a complete `CHANGED` line
for all 118 mutations with no incomplete or not-compared result. The transcript
and separate branches are `/private/tmp/cairn-c2-template-mutants.tsv` and
`/private/tmp/cairn-c2-stance-mutants`; branches are `c2-147` through
`c2-264`. All four files are covered by the committed root-list union.

| Obligation label | Own proposal | Shipped proposal | Own plan | Shipped plan |
|---|---|---|---|---|
| `a-call-names-one-artifact-that-exists-now` | `be1b2a86` | `fb3eb6ae` | `9bce45a0` | `00d29686` |
| `a-called-brief-adds-focus-and-removes-no-owed-answer` | `89dce6f6` | `88702edb` | `524917a4` | `c7a11fac` |
| `a-called-by-line-never-confers-authority` | `7435c91a` | `66c245d6` | `05575504` | `bb8f4204` |
| `a-called-read-adds-and-replaces-nothing` | `8b735c69` | `c405295c` | `b98caa17` | `8734f4b3` |
| `a-called-read-discharges-no-security-review-by-distance-or-brief` | `c7870589` | `32d2622f` | `94e72332` | `8ace882f` |
| `a-clean-code-review-shows-a-falsification-ledger` | — | — | `1957d990` | `1f9e3ee2` |
| `a-clean-pass-needs-evidenced-answers-and-named-gaps` | `c80cb555` | `f9b06c91` | `147aa7ba` | `ab1b730f` |
| `a-code-review-asks-whether-it-does-what-it-claims` | — | — | `a2cc133b` | `fff8a4c7` |
| `a-fresh-reviewer-on-the-works-side` | `0caac7b5` | `0958fa85` | `c6768f20` | `87588d7a` |
| `a-high-risk-surface-takes-a-security-review` | `b716e5ae` | `9d2453a8` | — | — |
| `a-plan-review-asks-whether-the-plan-delivers-the-decision` | — | — | `b9f2bda8` | `d3ed0843` |
| `a-plan-security-obligation-is-cleared-only-by-a-matching-obligation-line` | — | — | `b3b2745c` | `96ebc538` |
| `a-proposal-review-asks-whether-it-should-exist-as-framed` | `7d4a1112` | `05dddb10` | — | — |
| `a-roster-you-set-is-not-a-call` | `b2e76cd2` | `eafcb66d` | `42b2d3b3` | `2340781e` |
| `a-standing-call-is-a-floor-and-returns-only-by-proposal` | `e458ac35` | `d5798cca` | `e3224dd0` | `0954e2ad` |
| `an-agent-may-name-a-risk-and-coverage-gap` | `47812aed` | `78ef6682` | `3b53af44` | `0f864d2f` |
| `called-by-carries-the-maintainers-words-verbatim` | `6701dcc3` | `69a68c83` | `27904c0e` | `c4e33db1` |
| `called-by-names-where-the-words-live` | `28d626e3` | `8d7971dc` | `bafa86d6` | `bd8e6dcd` |
| `called-by-quote-is-repeated-in-the-commit-body` | `bf91797c` | `4bf82b1a` | `9c0b0446` | `06b5347c` |
| `code-review-floor-is-not-the-implementing-agent` | — | — | `781b4f98` | `c29d9e43` |
| `code-review-never-reopens-the-decision` | — | — | `31b3eea3` | `c6ee8a2d` |
| `distance-is-information-and-the-staffing-reviewer-follows-the-brief-and-says-so` | `e62dd6de` | `44432f0f` | `5ccab214` | `01aefe2c` |
| `external-means-the-maintainer-called-it` | `44e1ddf4` | `9cc1a181` | `8cb51a89` | `db115350` |
| `foundations-block-three-answers-each-with-its-evidence` | `261ed471` | `723cdf47` | `cb9535fd` | `18f8b1f2` |
| `improve-means-recommend` | `4718f273` | `53728c1a` | `d7a997ba` | `469b6882` |
| `no-agent-declares-external-required-or-recommends-distance` | `9042a86d` | `4248896d` | `9f188c9e` | `01664690` |
| `no-agent-picks-a-kind-of-review` | `3c5eb55d` | `0e2b2b3b` | `9e2b70ba` | `e4f2cbec` |
| `no-quota-of-findings` | `d17e78fc` | `7d005360` | `a7f88386` | `3c511e30` |
| `no-tool-reads-the-obligation-line-a-reader-does` | — | — | `879eeaf8` | `30617acb` |
| `nothing-checks-the-quote-a-reader-does` | `7bf41b57` | `8600ac89` | `91699246` | `118b246e` |
| `one-stance-at-every-stage` | `cc2f9e72` | `f908a34d` | `da1d4d1a` | `9c9638fe` |
| `other-authority-lives-in-a-decision-or-a-plan-fence` | `3e7b8030` | `9949d903` | `37205293` | `afee7afc` |
| `plan-review-is-fresh-context` | — | — | `c92bb594` | `26041ddf` |
| `tier-external-needs-called-by-else-read-as-the-usual-review` | `36bccb40` | `9210adba` | `60b13a60` | `18d67cef` |
| `usual-plus-security-review-is-two-passes-and-the-usual-pass-never-clears-the-second` | `3cc59dd1` | `4dfa72f7` | — | — |


Examples from the report: `fb3eb6ae` removed “one named artifact that exists
now” from the proposal template's called-read rule; `88702edb` removed “Its
brief may add focus; it removes no owed answer” while showing the remaining
sentence. The transcript has all complete before/after output lines.

The cumulative evidence candidate is now 273 cases across four pure-text
nodes, all still present in the source. One fresh Medium reader must judge
whether the reports expose every lost or changed obligation and whether the
proposed pin retirement preserves the required text behavior. No source
proposal/plan template, slot, installer or parity behavior was edited. This
273-case count is not a realized reduction. **Elapsed**: approximately 2
minutes. **Tokens**: unknown.


## C2 source review-sweep pin mutants -- GPT-6 Luna LowImplementation -- 2026-11-08

This batch is proof only; no source carrier or test was changed. At `ebddea30`,
the targeted `test_source_sweep_carries_the_obligation` node passed 56/56 cases
with Python 3.13.13 (0.05 s). Each of its 28 labels was removed from the
actual `## The review sweep` section in each source copy, one separate branch
commit per case from `d5436fe5`. The source report returned a complete
`CHANGED` result for all 56, with no incomplete or not-compared notice. Both
review-loop source files are covered by the committed root-list union. The
transcript and branches are `/private/tmp/cairn-c2-source-sweep-mutants.tsv`
and `/private/tmp/cairn-c2-stance-mutants`; branches are `c2-265` through
`c2-320`.

| Obligation label | Shipped review-loop mutant | Own review-loop mutant |
|---|---|---|
| `a-bare-checked-is-an-incomplete-review` | `c2448d5a` | `a0c047b8` |
| `a-clean-code-review-shows-a-falsification-ledger` | `e9e5de54` | `2e446758` |
| `a-clean-pass-is-treated-with-skepticism` | `dbc61165` | `14b62a9c` |
| `a-project-adds-domain-probes` | `5bda7dd6` | `96e839e9` |
| `a-reviewer-who-tried-to-break-it-has-cleared-the-gate` | `742c8f28` | `283f80d4` |
| `cited-claims-name-evidence` | `0c636553` | `18edb3b4` |
| `coverage-line-covered-half` | `a4f51a4a` | `55b2e410` |
| `coverage-line-does-not-end-in-a-recommendation-for-more-review` | `3f697e5f` | `87c10d45` |
| `coverage-line-not-covered-half` | `0513ef6c` | `06b0447e` |
| `ledger-mutation-summary-names-control-counts-and-exceptions` | `f29837a4` | `60b4dc7b` |
| `ledger-mutation-when-a-claim-names-a-set` | `71396c9c` | `23392e4f` |
| `ledger-negative-or-edge-case-attempt` | `b470fafe` | `4c6d29c0` |
| `ledger-residual-risk` | `886696f1` | `1bed036c` |
| `ledger-surfaces-probed` | `fd985c3d` | `ae442965` |
| `ledger-verification-run-or-consciously-not` | `521da756` | `93cedfbc` |
| `lens-1-claims` | `a73f37bf` | `2ea1c173` |
| `lens-2-production-path-exercised-by-tests` | `c76ca826` | `f4a352da` |
| `lens-3-design-completeness` | `ec7ff23a` | `a156bcdc` |
| `lens-4-silent-failure-fail-closed` | `13d82bee` | `95126d57` |
| `lens-5-cross-document-consistency` | `07ed2f6c` | `6eec1edf` |
| `lens-6-drift` | `e98ce422` | `cf0b1321` |
| `lens-7-lifecycle-process-placement` | `01bc6e9b` | `7fcc60a6` |
| `lens-8-domain-scientific-validity-and-scope` | `e180294a` | `86626905` |
| `lens-9-name-the-satisfier` | `276b565c` | `0f202ef5` |
| `the-lenses-can-inform-review-stages` | `9a7abc4e` | `53c55e93` |
| `the-reading-aid-does-not-downgrade-a-declared-tier` | `1d16e986` | `b173e93f` |
| `the-roster-does-not-require-lens-by-lens-reporting` | `48e31f15` | `d94f9ed9` |
| `the-roster-is-a-reading-aid-not-a-required-checklist` | `e9ae0c21` | `5a71bd4f` |


Examples from the report: `c2448d5a` changed `A bare "checked" is an
*incomplete* review, not a pass.` to an empty sentence; `e9e5de54` removed
`Code review tries to falsify the change.` while retaining the next sentence.
The transcript contains all 56 complete before/after lines.

The current evidence candidate count is 329 cases; all source tests and pins
remain. This is a human review aid only. Keep the nine-lens roster in source,
retain real installs and source/output correspondence in their separate hybrid
nodes, and preserve the body-text/slot check. No installer, slot, parity,
accessibility, hostile-state or drain behavior was changed. A fresh Medium
reader still needs to answer the rule-weakening question before any pin is
removed. **Elapsed**: approximately 1 minute. **Tokens**: unknown.


## C2 source readable-work pin mutants -- GPT-6 Luna LowImplementation -- 2026-11-08

This batch is proof only; no source file or test was changed. At `361be807`,
the targeted `test_source_readable_work_obligation_and_mutation` node passed
58/58 cases with Python 3.13.13 (0.19 s). Each case removed its named regex
obligation from the actual source carrier in a separate branch commit based
on `d5436fe5`. The existing source reporter returned a complete `CHANGED` line
for all 58; none was incomplete or not-compared. The four source roots and the
session-end skill are covered by the committed content-scan/prose-root union.
The transcript and branches are `/private/tmp/cairn-c2-source-readable-mutants.tsv`
and `/private/tmp/cairn-c2-stance-mutants`, branches `c2-321` through `c2-378`.

| Obligation label | Separate actual-carrier mutants (`path: commit`) |
|---|---|
| `assigned-tier-chunks-are-specified` | `AGENTS.md: d13439e6`; `templates/core/AGENTS.md: 1fc1cedb`; `dev/agent_collaboration.md: dac7be83`; `templates/core/dev/agent_collaboration.md: 1f486012`; `docs/methodology/plans.md: 2250a40e` |
| `cheap-defect-exception-stays-narrow` | `dev/plans/_template.md: 9cbce7b3`; `templates/core/dev/plans/_template.md: e3903457` |
| `cheap-follow-up-definition` | `AGENTS.md: a0274fff`; `templates/core/AGENTS.md: 7cc20a4a`; `dev/plans/_template.md: 3159b435`; `templates/core/dev/plans/_template.md: 9d577dc3`; `docs/methodology/plans.md: d3afb1d1` |
| `cheap-follow-ups-fixed-or-authorized-deferral` | `AGENTS.md: d8eb2f9c`; `templates/core/AGENTS.md: 1fd8ae2c`; `dev/plans/_template.md: 2db05b41`; `templates/core/dev/plans/_template.md: 733d342e`; `docs/methodology/plans.md: 74df7013` |
| `cheapness-does-not-waive-checks` | `AGENTS.md: 54f84dd6`; `templates/core/AGENTS.md: 75df5599`; `dev/plans/_template.md: bc19b82c`; `templates/core/dev/plans/_template.md: a4430c8e`; `docs/methodology/plans.md: 4e6df572` |
| `failed-required-check-stays-implementation-work` | `AGENTS.md: 03a83beb`; `templates/core/AGENTS.md: 27222464`; `dev/plans/_template.md: a4ef226a`; `templates/core/dev/plans/_template.md: 1b17dd55`; `docs/methodology/plans.md: eca61f87` |
| `finish-records-at-commit` | `AGENTS.md: d2a97deb`; `templates/core/AGENTS.md: 5fd05455`; `docs/methodology/session-routines.md: f55d1036`; `templates/skills/session-end/SKILL.md: d8ad1d7f`; `.agents/skills/session-end/SKILL.md: 05b8ff71` |
| `non-cheap-advice-keeps-disposition` | `AGENTS.md: 500229c0`; `templates/core/AGENTS.md: a5050f73`; `dev/plans/_template.md: 8bdffe7d`; `templates/core/dev/plans/_template.md: 3a189d05`; `docs/methodology/plans.md: b8e25958` |
| `plan-review-returns-missing-design` | `AGENTS.md: ce2ddf2e`; `templates/core/AGENTS.md: bf8bfab7`; `dev/agent_collaboration.md: b30fd893`; `templates/core/dev/agent_collaboration.md: f54640ce`; `docs/methodology/plans.md: a124ad9d` |
| `proposal-author-rereads-top` | `dev/agent_collaboration.md: 1e42a065`; `templates/core/dev/agent_collaboration.md: 29cb486c`; `docs/methodology/proposals.md: 03d160bc` |
| `proposal-cold-read` | `dev/agent_collaboration.md: 64def8d8`; `templates/core/dev/agent_collaboration.md: cd578ae0`; `docs/methodology/proposals.md: c900b881` |
| `proposal-gist-and-finding` | `dev/agent_collaboration.md: fb868820`; `templates/core/dev/agent_collaboration.md: 75582b1e`; `docs/methodology/proposals.md: 13c704b9` |
| `reviewer-disposes-non-cheap-advice` | `dev/agent_collaboration.md: 41b60477`; `templates/core/dev/agent_collaboration.md: 8184f75b` |
| `session-end-checks-omissions` | `AGENTS.md: f430ce52`; `templates/core/AGENTS.md: 9ac6dddc`; `docs/methodology/session-routines.md: 8eb9b6b0`; `templates/skills/session-end/SKILL.md: 0cb7bd71`; `.agents/skills/session-end/SKILL.md: e697cc1d` |


Two exact outputs: `d2a97deb` removed “At the commit or archive that finishes
work, update applicable roadmap and changelog records”, leaving “under their
existing ownership and serialization rules”; `3159b435` removed the full
cheap-follow-up definition, leaving an empty sentence. The transcript has all
58 reporter lines.

This source-only node is separate from the installed-readable-work node. Keep
its real installations and source-to-destination checks intact, together with
copy parity, the post-install placeholder scan and all other required behavior.
The cumulative evidence candidate is 387 cases; no source pins are removed.
A fresh Medium reader must still answer the rule-weakening question from these
outputs. **Elapsed**: approximately 1 minute. **Tokens**: unknown.


## C2 raw-span gap carrier mutants -- GPT-6 Luna LowImplementation -- 2026-11-08

This batch covers six actual carriers which the structured prose extractor
cannot fully compare. At `22fc4fff`, the focused source pin tests passed 6/6
with Python 3.13.13 (0.12 s). Each mutation was a separate committed branch
from `d5436fe5`; the corresponding existing pin test failed on each mutated
copy as expected. The reporter emitted complete raw evidence for every case;
the SVG rows say `NOT COMPARED` for structured extraction but include the full
`RAW ADDED` fragment. The Python row reports its raw removed phrase and the
188 short-constant/runtime construction gap explicitly.

| Actual carrier obligation | Mutant commit |
|---|---|
| YAML mapping comment `A human fills the External tier.` | `templates/modules/team-gated/model_selection_mapping_stub.yml: f9f04256` |
| SVG comment `two tiers` | `docs/assets/dual-review-independence.svg: c4ae50b3` |
| SVG comment `Internal` | `docs/assets/dual-review-independence.svg: 168fd360` |
| SVG comment `External` | `docs/assets/dual-review-independence.svg: 0e3fecf0` |
| SVG comment `different agent type or human` | `docs/assets/dual-review-independence.svg: 87afe089` |
| Python refusal phrase `before a push, when required` shortened | `bootstrap/tests/conftest.py: 7e00b174` |

The transcript is `/private/tmp/cairn-c2-raw-gap-mutants.tsv`; adverse-copy
pin-test results are in `/private/tmp/cairn-c2-raw-mutant-tests.log`. No
source pin or test was changed. Across the committed batches, 393 candidate
cases now have actual-carrier mutation evidence. This is not a test-volume
reduction: source obligations and tests remain pending one fresh Medium
reader's disposition. **Elapsed**: approximately 2 minutes. **Tokens**: unknown.

## C2 fresh reader -- GPT-6.1 Terra Medium (Reviewer) -- 2026-11-08

Reviewed commit: `f6eede2c3c879dbe3be7e36bc850b65f613ec927`.
**Verdict**: PARTIAL; the named groups below meet this reader prerequisite.
**Elapsed**: approximately 10 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes for the evidenced groups: the actual before/after reports expose the removed obligations, while source rules remain. For example, `d2a97deb` shows finish-time records removed, `e8314827` shows the matching Security Review obligation line removed, and `fb3eb6ae` shows a call no longer limited to an existing artifact. These are adverse changes, not acceptable rule changes. A human must still judge the report; the tool does not enforce meaning.
2. **Best alternative.** Retire only the individually covered text pins and preserve behavior, parity and real installs. The broad search and multi-assertion nodes below need more evidence; one visible mutation does not represent every assertion or scanned file.
3. **What would show it wrong?** A listed carrier's adverse change missing or unintelligible in a report, or a retained installer/parity/slot check failing after the split, would defeat the proposed replacement. Run those checks at the required later boundaries.

**Eligible for this reader prerequisite** (376 collected cases; paths below are under `bootstrap/tests/`):

- `test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation` 68; `::test_template_review_section_carries_the_obligation` 118.
- `contract/test_review_and_verification_rules_ship.py::test_agents_md_carries_the_obligation` 68, `::test_the_shipped_copy_makes_claiming_conditional` 1 and `::test_cairns_own_copy_claims_unconditionally` 1.
- `test_review_sweep_ships.py::test_source_sweep_carries_the_obligation` 56 and `::test_source_readable_work_obligation_and_mutation` 58.
- `test_review_stance_in_shipped_files.py::test_plan_review_never_has_a_second_round` 2 and `::test_the_figure_carries_no_old_phrase` 4 wording cases. The latter's raw additions explicitly show the four forbidden strings despite `NOT COMPARED`; retain SVG parsing, accessibility and geometry.

**Holds**: The nine light-tier cases have named mutant commits and a plan summary but no captured actual reporter outputs found for this read; provide those outputs for the reader. The two `test_the_stance_sits_in_the_review_section_only_once` cases demonstrate changed wording, not the duplicate occurrence that their count assertion also rejects. The four `test_carrier_omits_the_old_vocabulary` cases demonstrate one forbidden phrase each, not the other patterns and probe-inventory assertion. The single `test_every_file_with_a_phrasing_hit_is_exempt_for_a_reason` case walks 144 committed members (131 Markdown, 4 YAML, 9 SVG; exact listing `/private/tmp/cairn-c2-search-a-committed-members.txt`); only one YAML carrier was mutated. The `test_the_broad_run_refusal_no_longer_offers_the_override` case has legible raw and structured evidence for conditional push wording but also checks override advice and record wording, which the shown mutant does not cover. Demonstrate the missing assertions/carriers before retiring those full nodes. This is 17 held collected cases, not a scope concession.

**Coverage**: Read the named report transcripts and raw test failures, source tests and the plan's committed evidence; did not replay mutants, run tests, independently audit tool security or establish net test-volume reduction. The first nine outputs were unavailable to this read. Preserve actual installs, copy parity, slots, placeholders, model-mapping semantics, SVG behavior and the Maintainer-retained drain pin. This reader prerequisite does not replace ordinary or Security code review; no source pin was changed here. Above target because the exact eligible and held sets require identification.


## C2 reader-cleared pin retirement -- GPT-6 Luna LowImplementation -- 2026-11-08

Following the exact eligible set in reader commit `93ea049a`, retired nine
test functions comprising 376 collected cases from three inventory-owner test
files. These are the only removed nodes: the review-section obligation,
template-section obligation, AGENTS obligation and two claim-conditionality
checks; source review-sweep and readable-work obligations; the plan single-pass
wording pin; and the four SVG wording cases. No behavior, copy-parity, real
install, placeholder, slot, model-mapping, SVG parse/accessibility/geometry or
drain check was removed. The exact held set remains pinned: nine light-tier
cases, two duplicate-occurrence cases, four old-vocabulary/probe-inventory
cases, one 144-carrier YAML/file-exemption case, and one multi-assertion broad
run-refusal case.

On Python 3.13.13, collection of the three changed test files now reports 563
cases; the reader's exact deletion set is 376 cases (implied pre-retirement
count 939). Three focused retained figure accessibility, SVG geometry and
model-mapping parity tests passed (0.03 s). `test_tiers.py for` maps these
changed files to four test files; the wider selection was not run while the
coordinator's host map is active. The companion feature counts are upgrade
−5, prose +86, coupling +5 and promise-unit-testing +6 collected cases; after
these 376 retirements the combined change reduces collection by 284 cases.
Definition counts: this edit removes 9 functions; the companion changes add a
net 50, so the combined change adds 41 definitions while reducing collected
cases. **Correction**: the C3 six-function total already includes its five
coupling functions, so the `−284` companion arithmetic above double-counted
those cases and is withdrawn. The final integrated before/after case delta is
not measured yet; dynamic parameterization can also change collection in
unchanged files. The 376 reviewer-cleared cases were removed, but only Root's
clean integrated baseline/control collection can state the net test-volume
reduction. This edit removes 9 test definitions. The earlier +41 overall
definition figure is diagnostic only and may also double-count companion
functions; it is not a target. No source rule text changed. **Elapsed**:
approximately 10 minutes. **Tokens**: unknown.


## C2 accepted helper revision sync -- GPT-6 Luna LowImplementation -- 2026-11-08

Copied `tools/git_read.py` and `templates/skills/_lib/git_read.py` byte for
byte from committed primary revision `4f7be4f6a334906a47bca5f16ac530e7b870f723`;
both now hash to `db7e504bdf3e7c20acf2c03d2a3b9059c69f83df04b44f5ebfd9b93f5ecd1212`.
Updated the existing old helper digest in all 23 callers: the 19 primary source
owners plus both report/replacer twins and their shipped twins. The two
`exact_replace.py` twins also refresh their `_REPORT_SHA256` pair pin to the
new `prose_diff.py` bytes, required for the existing refusal/entrypoint
binding to keep working. The 21-member first-loader census, four keys and
remaining B102 rationale rows were left intact; the two meter callers remain
outside that census as before.

Python 3.13.13 focused helper/report/install checks passed 6/6 (1.65 s): the
raw unsupported-target replacement, substituted-helper refusal, installed
lock refusal, source-layout report, 21-member census and self-hosted helper
byte-parity check. The first-loader native-change-time cases are assigned to
Root after the coherent sync. No broad suite was run. **Elapsed**:
approximately 5 minutes. **Tokens**: unknown.


## C1 native Windows failure fixes -- GPT-6 Luna LowImplementation -- 2026-11-08

Fixed the two failures Root reproduced on commit `319c13c5`. In both
`exact_replace.py` copies, removed the ineffective name-suffix binding gate
and explicitly bound the Git reader to the helper buffer and digest already
verified by `_load_module`; report-module loading remains unbound. Added a
focused witness that the returned helper's `_VERIFIED_SOURCE` and digest equal
the verified buffer. The unsupported-target CLI fixture now derives old/new
fragments from the target's original byte line, preserves its exact CRLF/LF/CR
or absent terminator, and checks the final bytes.

On Python 3.13.13, both focused replacer tests pass (0.57 s), and the paired
source/template replacers remain byte-identical. Root's two native Windows
public-CLI reruns are still required before the reported Windows failures can
be closed. I did not change the speculative source-rewrite metadata comparison
or weaken its checks. **Elapsed**: approximately 4 minutes. **Tokens**: unknown.


## C1 fresh-install fixture correction -- GPT-6 Luna LowImplementation -- 2026-11-08

**Correction to the preceding record**: commit `878149d1` applied the byte
fixture change to the unsupported-target unit test, not the native fresh-install
test named in the failure. Root's native rerun showed the public stdin workflow
passing but the fresh-install workflow still failing with `match 0`. I restored
the unsupported-target test's original `forbidden` to `allowed` raw-change
assertions, then moved the byte-preserving fragment setup to
`test_fresh_scaffold_install_runs_both_public_prose_clis_with_real_lock`. It
now inserts the fixture suffix before the original terminator and compares the
resulting file bytes.

The two affected fixture nodes pass 2/2 on Python 3.13.13 (2.24 s). Root's
focused native Windows fresh-install public CLI run passes on commit `731b799b`
(Python 3.13.17, 1 test, 4.44 s; installed archive SHA-256
`c63ded772f1a28b6c0ca5609deb4af1faff9a314617d61e72e2b0cdba59792bf`;
log `/private/tmp/cairn-prose-public-cli-731b799b/remote-native.log`). The
stdin workflow already passed on `878149d1` with the same product bytes; no
repeat was needed. Both previously observed native public-CLI failures are
closed. **Elapsed**: approximately 2 minutes. **Tokens**: unknown.


## C1 rewritten-source native control -- GPT-6 Luna LowImplementation -- 2026-11-08

Added `test_replacer_reads_rewritten_windows_fragment_after_creation` in
`bootstrap/tests/security/test_prose_tools.py`. It creates a named new-fragment
file, rewrites it before invoking the real exact-replacer CLI, asserts that
Windows path ctime remains mapped to birth time while the reopened descriptor
shows the rewrite's distinct ChangeTime, and requires successful replacement.
This isolates final path identity comparison from a mutation during the read.
The first Windows attempt did not advance ChangeTime with back-to-back writes;
after applying the established wait, identical-byte rewrite, flush and fsync
sequence, Root's native run passed all fixture preconditions and the real CLI
then refused with `source changed while reading` before writing (Python
3.13.17, 1 failed, 1.10 s; log
`/private/tmp/cairn-prose-rewritten-19738bd7/remote-native.log`). Both
`exact_replace.py` twins now compare the final path to the original path-row
identity; the descriptor-to-descriptor ChangeTime check remains strict. Fix
commit: `47d2c97e`. Focused local Python 3.13.13 source/refusal checks passed
11/11 with the native-only case skipped (2.56 s). Root's rerun of the native
positive control remains pending. **Elapsed**: approximately 8 minutes.
**Tokens**: unknown.


## C2 additional carrier and held-assertion outputs -- GPT-6 Luna LowImplementation -- 2026-11-08

Additional evidence only; no source pin or test was removed. The nine light-tier
mutant reports were replayed on their separate committed copies; each returned
one complete `CHANGED` line whose before/after text matches the table in the
first batch, with no incomplete or not-compared notice. For the two
duplicate-occurrence cases, separate own and shipped AGENTS copies appended a
second `The stage sets the questions` sentence; the reporter returned a full
`ADDED` line and the existing test returned 1 failed, 1 passed in each copy.

For the four old-vocabulary carrier cases, each of the four carrier copies was
mutated twice: once with all 19 forbidden-pattern examples and once with the
legacy probe-inventory sentence alone. All eight reports showed complete
`ADDED` lines; the existing test returned 1 failed, 3 passed for each copy.
The probe-only mutant reaches the probe-inventory assertion with the forbidden
set unchanged. For the dynamic scan, the 144 tracked members (131 Markdown, 9
SVG, 4 YAML) were individually mutated in separate committed copies. Its
existing node failed on each of the 143 non-exempt members; the explicit
`docs/methodology/lifecycle-contract.md` exemption remained a pass. All reports
were complete; the 13 YAML/SVG results state `NOT COMPARED` for structured
extraction and show the full added phrase in raw evidence. The clean baseline
node passes 1/1 on Python 3.13.13 (0.11 s).

The certification owner baseline passed 14/14 on Python 3.13.13. Twenty
separate carrier mutations across its RETIRE nodes produced complete reporter
output. The two missing broad-run advice/record mutations each returned 1
failed, 13 passed and complete raw/structured evidence. One uppercase advice
attempt survived; the corrected lowercase mutant failed as expected. Complete
outputs remain in `/private/tmp/cairn-c2-certification-mutants.tsv`,
`/private/tmp/cairn-c2-broad-mutants.tsv`,
`/private/tmp/cairn-c2-duplicate-mutants.tsv`,
`/private/tmp/cairn-c2-vocabulary-mutants.tsv`, and
`/private/tmp/cairn-c2-dynamic-mutants.tsv`; source fixtures and canonical
tests were not changed by these scratch mutations. All named pins remain until
one cumulative fresh Medium reader assesses this new material. These are not
test removals or a net-volume claim. **Elapsed**: approximately 4 minutes of
report replay plus 4 minutes of dynamic mutations. **Tokens**: unknown.

## C2 AGENTS pointer mutants and Windows source-time closeout -- GPT-6 Luna LowImplementation -- 2026-11-08

The four AGENTS pointer obligations were each removed from `AGENTS.md` and
`templates/core/AGENTS.md` in eight separate committed copies. The canonical
`prose_diff.py` source entrypoint emitted complete `CHANGED` before/after
output for every case; `test_agents_md_pointer_carries_the_obligation` failed
only for the mutated carrier (1 failed, 7 passed per copy) under Python
3.13.13. The concise output and scratch copy SHAs are at
`/private/tmp/cairn-c2-pointer-mutants.tsv`; no source pin or install/parity
check changed. The inventory’s KEEP slot, real-install, source-output,
placeholder, SVG and drain checks remain intact.

Root’s focused Windows run against the committed exact-replacer fix
`47d2c97e` passed the rewritten-input positive control: 1 passed in 3.19 s
under Python 3.13.17, archive SHA
`0e78c7a3bf361bcf43a80a96a4700f37a5b8c114fe54d4ba38a31fcc2516e648`, log
`/private/tmp/cairn-prose-rewritten-47d2c97e/remote-native.log`. The preceding
`19738bd7` refusal is retained as defect evidence; comparison now uses the
original path-row identity for the final named-path check while descriptor to
descriptor ChangeTime checks remain strict. This closes that measured C1
source-time defect. C2’s remaining accepted pins still require evidence and a
fresh cumulative reader; no net test-volume result is claimed here. **Elapsed**:
about 2 minutes. **Tokens**: unknown.

## C2 source smart-goal and review-sweep mutants -- GPT-6 Luna LowImplementation -- 2026-11-08

Two additional source-only batches provide actual-carrier evidence without
removing pins. Across both review-loop copies, 16 isolated commits weakened or
removed the sweep/trap order, lens numbering, follower anchors, ledger wording,
no-leak rule or legacy-ledger negative. Each complete source report showed the
changed or added fragment, and its existing focused node failed only for the
mutated copy (1 failed, 1 passed). The 47 smart-goal assertions were each
removed from their actual carrier in separate committed copies across all nine
source carriers; the canonical source reporter produced complete `CHANGED`
output and `test_source_smart_goal_guidance` failed only that case (1 failed,
8 passed). Outputs are `/private/tmp/cairn-c2-sweep-structure-mutants.tsv` and
`/private/tmp/cairn-c2-smart-goal-mutants.tsv`. These mutations leave all
source, installed, parity, slot, placeholder, SVG and drain checks unchanged.
This is evidence for the cumulative fresh Medium reader, not a deletion or a
net test-volume result. **Elapsed**: approximately 2 minutes plus 1 minute.
**Tokens**: unknown.

## C2 plan-completion and AST-disposition mutants -- GPT-6 Luna LowImplementation -- 2026-11-08

Each of the 61 plan-completion assertions was removed from its actual carrier
in a separate committed copy across seven source files. The source report gave
complete `CHANGED` evidence for every removal, and the existing focused owner
node failed only for the mutated carrier (1 failed, 6 passed). Two additional
copies changed the Cairn-local AST disposition: deleting its implementation
rule failed the focused test, and adding that rule to the shipped AGENTS
produced complete `ADDED` output and failed the shipped-absence assertion.
The collected outputs are `/private/tmp/cairn-c2-plan-completion-mutants.tsv`.
The first setup attempt used an absent heading as the shipped-file insertion
anchor and stopped before its test; the corrected end-of-file insertion reached
the owning test and failed as expected. No source pins or install/parity,
placeholder, slot, SVG, or drain checks changed. These 63 cases await the
cumulative fresh Medium reader; no net test-volume result is claimed. **Elapsed**:
about 1 minute of focused collection. **Tokens**: unknown.

## C2 duplicate-module wording mutants -- GPT-6 Luna LowImplementation -- 2026-11-08

The 12 negative phrase patterns in the module-owner test were each restored in
each actual module carrier (`dev/modules/dual-review.md` and
`templates/modules/team-gated/dual-review.md`) in 24 separate committed copies.
Every canonical source report returned complete `ADDED` evidence, and
`test_the_module_carries_no_lens_citation_rule_or_ledger` failed only for the
mutated carrier (1 failed, 1 passed). This covers the lens roster, citation
rule, review-evidence guidance and duplicated scope-reduction trap. The module
content and its installation remain unchanged in the working tree; no pin has
been retired. Outputs are `/private/tmp/cairn-c2-module-mutants.tsv`. The
negative-pattern instrument controls remain pending cumulative reader review.
**Elapsed**: approximately 1 minute. **Tokens**: unknown.

## C2 light-tier and leak-instrument mutants -- GPT-6 Luna LowImplementation -- 2026-11-08

The two light-tier rules were each removed from all nine actual carriers in 18
separate committed copies. The canonical source report showed complete
`CHANGED` evidence and `test_light_tier_can_ship_wide_work_without_a_plan`
failed only for each mutant (1 failed, 8 passed); outputs are
`/private/tmp/cairn-c2-light-tier-mutants.tsv`. A separate copy removed all ten
recognized doctrine-leak examples from `docs/methodology/dual-review.md`; its
complete report showed the change and the existing known-positive instrument
test failed (1 failed). The first attempt replaced only lowercase forms and
the control still passed; the corrected case-insensitive removal is the
reported result. Output and retained initial outcome are at
`/private/tmp/cairn-c2-leak-positive-control.tsv` and
`/private/tmp/cairn-c2-leak-positive-control-first-failure.txt`. No source pins
or behavior checks changed. These cases await cumulative reader review; no net
test-volume result is claimed. **Elapsed**: approximately 1 minute. **Tokens**:
unknown.

## C2 additional fresh reader -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-08

Reviewed commit: `4b559c98281b5f84d620fc072fd5a70c55ae4038`.
**Verdict**: PARTIAL. **Elapsed**: unknown. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes for the named assertions: reports expose the actual lost rule or inserted text, for example the removal of the separate human-operation wait, the narrowed guarded-reuse limits, and the duplicate review sentence (`plan-completion`, `rules-owner`, `duplicate` transcripts).
2. **Best alternative.** Split hybrids and preserve real installs and correspondence; preserving a fixed rule phrase would defeat the accepted Decision, while deleting an installer assertion would lose a different promise (C2 inventory and writing/model tests).
3. **What would show it wrong?** A missing carrier or assertion, unreadable report, or retained install/parity check failing after the split would leave C2 open; test those splits at the required boundaries.

**Additional eligible set**: only the following current nodes or specified wording parts, with all parameters, under `bootstrap/tests/`. This is the reader prerequisite, not authority to remove KEEP assertions.

- `test_review_stance_in_shipped_files.py`: `test_the_stance_sits_in_the_review_section_only_once`, `test_carrier_omits_the_old_vocabulary`, and `test_every_file_with_a_phrasing_hit_is_exempt_for_a_reason` (the latter's old-wording scan only). The 144-member listing equals the `dynamic` transcript: 143 failures and the existing lifecycle-contract exemption passes; YAML/SVG show the actual inserted phrase in raw evidence despite `NOT COMPARED`.
- `contract/test_certifying_run_rule.py`: all seven test definitions, wording assertions only. The two command literals are searched in instruction text, not executed by this node; preserve the actual guard and certification behavior elsewhere. `broad` separately shows the omitted override advice and record wording.
- `contract/test_review_and_verification_rules_ship.py`: `test_agents_md_omits_the_forbidden_phrasing` and its `test_forbidden_patterns_recognize_their_examples`, `test_the_external_by_default_pin_ignores_case_and_wrapping`, `test_an_empty_file_carries_no_obligation` controls; `test_the_commit_rule_sits_in_the_working_tree_section`, `test_coordination_doctrine_guards_same_file_commits`, `test_light_tier_can_ship_wide_work_without_a_plan`, and the four `test_security_module_*` nodes. Evidence: `rules-owner` and `light-tier` transcripts.
- `contract/test_model_tier_rule_ships.py`: the RETIRE assertions in every inventory row in the model-tier table. The `model-retry` and `model-other` transcripts show the removed retry clauses and changed tier rules; retain the table's equality, actual installs, profile module presence/absence and source-to-output mutation propagation. Do not remove mapping semantics.
- `contract/test_writing_rules_ship.py`: the RETIRE assertions in `test_source_readable_prompt_and_contrary_mutation` and `test_installed_readable_prompt_and_contrary_mutation` only. Keep the real install and each source/destination correspondence. The `writing` transcript shows each prompt and corresponding source carrier.
- `test_review_sweep_ships.py`: `test_source_smart_goal_guidance`, `test_source_smart_goal_mutations_fail_entrypoint`, wording parts of `test_installed_smart_goal_guidance` and `test_installed_smart_goal_mutations_fail_entrypoint`; `test_source_plan_completion_rule_and_surface_mutation`, `test_expected_ast_mismatch_disposition_is_cairn_local`, `test_agents_md_pointer_carries_the_obligation`, and `test_the_module_carries_no_lens_citation_rule_or_ledger` plus the three `test_restoring_*_into_the_module_is_reported` controls. Keep all profile installs and corresponding source/output checks. `smart-goal`, `smart-contrary-focused`, `plan-completion`, `pointer` and `module` transcripts show the respective changes.

**Holds**: Other inventory RETIRE assertions remain open, including writing-standard version/group/number/order/pointer/score nodes; the evidence shown does not exercise every assertion and actual carrier. For sweep structure, a renamed heading does not demonstrate reordering, nor a changed number prove every count/order assertion; the pointer negative-path node is also not covered by the eight positive-pointer mutants. Show their applicable independent carrier/negative mutants and intelligible reports before retirement. These are evidence gaps, not scope concessions. No claim is made that any unlisted node is eligible.

**Coverage**: Read the committed inventory and source assertions, the named report transcripts and 144-member listing, and the accepted Decision. The adverse samples visibly change rules; no operative rule was edited in this pass. Did not replay tests, measure integrated net volume, assess tool security or conduct the required code reviews. Preserve actual installs, copy parity, slots, placeholders, schema/mapping, SVG accessibility and geometry, refusal/hostile-state behavior and the Maintainer-kept drain node. Over target to identify the exact eligible groups and remaining evidence gaps.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-08

Commits: `c50dbb843c0213d1243434b87f3d19591b02c2a2` retired the newly cleared
pure wording nodes and split the cleared hybrids; `3eb3731813f56d543f83d88304d440c3986e374b`
replaced invalid full-file byte comparisons with source-region correspondence
after the first committed-copy check exposed install token and slot changes.
The 3eb source copy was clean before and after checks. Under Python 3.13.13,
`py_compile` and `git diff --check` passed. `pytest --collect-only -qq` for the
four changed owners reported stance 291, sweep 105, model-tier 6 and writing
19 cases, down from 291, 196, 64 and 52 at d659: 182 fewer collected cases
in this batch. `tools/test_tiers.py for` selected those four owners.

The bounded targeted selection on the clean 3eb copy passed 37 tests in 5.84s:
model-tier copy equality, both profile installs and module states, source
mutation propagation and task-floor mapping; all three installed prompt
template correspondences; and installed smart-goal, review-loop, pointer and
plan source-region correspondence, including a source/output mutation control.
The first c50 check had 16 passes and 21 failures because full-file byte
equality did not account for install-time token substitution and slot fills;
the corrected projections passed. A precommit collect-only check also caught
an accidental omission of the retained readable-work table; it was restored
before the 3eb commit. The deleted certifying-run and review-and-verification
owners were not rerun. No full suite, Boundary B, code review or integrated
net-volume comparison was performed. The previous 376-case retirement and
this 182-case batch are raw collection deltas, not the final integrated net.

Remaining C2 holds include writing-standard version, group, numbering, order,
pointer and score assertions; review-sweep order/count/ledger structure and
the pointer negative-path assertion. Keep the mapping semantics, real profile
installs, copy parity, source/output checks, install placeholders, SVG geometry
and accessibility, and the Maintainer-kept drain behavior in place. These
holds remain implementation work pending carrier-specific evidence and a fresh
reader; no accepted C2 scope is deferred. **Elapsed**: 5.84s targeted checks,
plus collection and compile. **Tokens**: unknown.

## C2 held-carrier mutation evidence -- GPT-6 Luna (Implementation, Low) -- 2026-11-08

Against `37f148f6d465002186c92042c7ed0a789745cc62`, 36 separate scratch
commits exercised the remaining writing-standard and review-sweep carriers.
The source-side entrypoint `templates/modules/team-gated/prose_diff.py`
returned complete raw spans for every mutation, and the matching existing
owner node failed on the mutated copy. Writing mutations covered version,
license, each of the five headings, item 17 numbering, section order in both
loop copies, the pointer in both AGENTS copies, and scoring phrases in all
four instruction files. Sweep mutations covered trap order, lens order and
numbering in both loop copies, both follower anchors in both copies, both
ledger phrases and the legacy-ledger insertion in both copies, the pointer
negative path in both AGENTS copies, and doctrine-leak insertion in both loop
copies. No source file in the implementation tree changed during collection.

The self-hosted `scripts/prose_diff.py` invocation was incomplete because the
current feature lock does not yet contain its `tools/git_read.py` record; the
source-side copy was the plan's established reporter path and produced the
complete reports. The newly measured outputs address d659's open evidence
questions; they do not clear any node until a fresh Medium reader assesses this
batch. Full suite, review and integrated net-volume comparison remain open.
**Elapsed**: approximately 2 minutes of focused checks. **Tokens**: unknown.

## C2 held-carrier fresh reader -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

1. **Should it happen?** Retire the newly evidenced wording assertions identified below: the source-side reporter showed the version, license, five headings, numbering, pointer deletion, scoring insertion and sweep anchor, ledger, negative-pointer and leak changes on their actual carriers. The author reports the corresponding owner failures at `3fa5769c`; this pass independently read the reporter output, not those failures.
2. **Best alternative.** Split mixed nodes and preserve real installs, source/output correspondence, parity, slot and placeholder behavior. Retaining fixed prose would frustrate the accepted outcome; removing those functional checks would lose separate promises (C2 inventory).
3. **What would show it wrong?** A missing assertion or carrier, an unintelligible report, or a failed retained install or parity check after the split keeps that part open. Check the final split at the required boundaries.

**Newly eligible wording parts**, under `bootstrap/tests/`, all applicable parameters: `contract/test_writing_rules_ship.py::test_standard_with_version_and_groups_reaches_install` (version, license, five groups and numbering); `::test_pointer_sentence_is_in_the_installed_agents_file` and the presence assertion in `::test_pointer_sentence_is_in_both_source_agents_files`; the formula-search assertion in `::test_no_copy_tells_agents_to_use_a_readability_score`. Retain the install and corresponding source/output evidence. In `test_review_sweep_ships.py`, the count and roster wording assertions of `::test_the_lens_roster_is_exactly_nine_in_the_doctrines_order` except its order assertion; `::test_the_anchors_a_follower_writes_against_are_present`, `::test_the_ledger_is_defined_once_with_five_items`, `::test_the_sweep_leaves_the_doctrines_reasoning_out`, `::test_the_leak_pattern_matches_the_doctrine_it_guards_against`, and `::test_the_pointer_names_no_test_path` are eligible. Preserve the slot test and real-install source correspondence.

**Holds:** Writing-standard section order in both source copies and installed node; sweep/trap order in both copies; and lens-order assertion in both copies. The reporter shows identical added and removed spans for the moves without their positions, so its output alone does not convey the order change. The installed score-prohibition phrase, the source pointer's separate adjacency assertion and the readability-context assertion remain held: pointer deletion and Flesch insertion respectively exercise different assertions. These are evidence gaps, not scope concessions. No unlisted assertion is newly cleared.

**Coverage:** Read the committed inventory, accepted proposal and current tests. With Python 3.13, ran the established source-side reporter on each of the 36 committed scratch mutations against its parent; its raw output supports the carrier observations above. Did not rerun owner tests, replay earlier matrices, measure net volume, assess security, or conduct code review. Preserve installs, parity, source/output correspondence, slots, schema/mapping, SVG behavior, hostile-state checks and the Maintainer-retained drain pin. This is a C2 reader prerequisite, not code or Security Review. Over target to specify the exact eligible and held parts. **Elapsed:** approximately 5 minutes. **Tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commits `5a280ed3` and `bf080918` retire only the wording assertions cleared by
the fresh reader at `644bbf1d`. Writing removes two full definitions; review
sweep removes five definitions and nine collected cases. Partial wording pins
were removed from the retained writing source-pointer and score-context checks
and the review-sweep lens-order check. Real installs, source/output
correspondence, the sweep slot, and held order and context checks remain. The
lens-order test keeps its label matches as prerequisites for comparing their
positions; its separate numbered-count assertion is removed.

On clean committed copy `bf080918111e7b6d457b1996d45987fc8a2e4b03`, Python
3.13.13 collect-only measured writing 17 (from 19) and sweep 96 (from 105).
Twenty-four tight retained nodes passed in 2.62s: install and copy
correspondence, source and installed section order, source-pointer adjacency,
score context, installed score prohibition, sweep/trap and lens order, slot
behavior, and installed loop/AGENTS correspondence across all three profiles.
The check copy was clean before and after; `git diff --check` passed.

Four committed scratch mutants closed the held-carrier evidence gap without
retiring those checks: `80dcc7d5` and `fcd797f0` inserted a sentence between
the failure instruction and pointer in the own and shipped AGENTS carriers;
the reporter showed the inserted sentence and each corresponding adjacency
case failed. `fe6b690f` and `a4e66457` changed the own and shipped score rule to
affirm score use; complete reporter output showed the contrary context and the
matching context check failed. On the shipped-loop mutant, the real-install
score prohibition also failed. The initial byte-mutation attempt for the own
loop used a newline-mismatched anchor and made no change; the corrected
newline-aware mutation produced the committed result.

The exact remaining held set from this reader is writing: five definitions,
10 collected cases (source and installed section order, pointer adjacency,
readability context, installed score phrase); review sweep: two definitions,
four cases (sweep/trap order and lens order). The source reporter still lacks
positions for moved spans, so order-pin retirement remains open. No full owner
run, integrated net-volume comparison, full suite, Boundary B, code review or
Security Review was performed. **Elapsed**: approximately 12 minutes including
mutant setup and focused checks. **Tokens**: unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commit `bb4e8cdb` adds one-based typed-unit positions to `REMOVED`, `ADDED` and
`CHANGED` output in both byte-identical reporter copies, using existing
`SequenceMatcher` opcodes and the existing Markdown/Python unit sequences.
Both exact-replacer copies pin reporter SHA-256
`9e8a8c988743f7786728915ba0e60a4024681f1b8c9eee9d7916a7fa0e304416`; their
Git-helper pins and lock checks are unchanged. No parser, output bound,
whitespace rule, escaping, refusal or AST-traversal behavior changed.

On clean committed copy `bb4e8cdba8dd3d1e6bfc09eb37e4af9badda7b39`, Python
3.13.13 ran the four new public CLI cases in 2.75s: a revision-report heading
move and an exact-replacer list-item swap, each through both source and
installed layouts. All passed and require matching moved text at distinct
before/after unit positions. The copy was clean afterward; the four cases
collected as expected. `git diff --check` passed.

`tools/test_tiers.py for` maps these changed files to five test files. I did
not run that wider mapped selection here; Root will run it after integration
alongside the overlapping Meter selection. The scoped lock finalizer in a
disposable copy found no lock rows for either prose tool and wrote nothing.
This establishes the output witness but does not yet re-report the held
writing, sweep/trap and lens-order mutants. Their pins remain in place until
the reporter output is reviewed by a fresh Medium reader. **Elapsed**:
approximately 10 minutes including focused checks and serialization. **Tokens**:
unknown.

## C2 held-order position outputs -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Using the canonical primary reporter, I re-reported four already-failed
carrier commits and made six separate order mutations from base `21bea3ec`.
The reporter was at `0a70b690` (SHA-256
`9e8a8c988743f7786728915ba0e60a4024681f1b8c9eee9d7916a7fa0e304416`). Each
report exited 0 without `INCOMPLETE` or `NOT COMPARED`. The four existing
commits are `80dcc7d5`, `fcd797f0`,
`fe6b690f` and `a4e66457` (base `bf080918`); their pointer and score-context
changes now show typed-unit positions. Their corresponding owner failures
remain recorded in the preceding C2 evidence; I did not rerun those nodes.

The six new committed copies are own/shipped writing-order mutations
`18bea88f`/`be2978b4`, sweep/trap mutations `9809aa52`/`be10d2b8`, and lens
order mutations `8ac1f50c`/`a9a5bcca`. Reports show the moved Surfacing section
at old units 186/184 and new units 119/117; the scope trap at old units
111/109 and new units 61/59; and the Drift lens at old units 80/78 and new
units 76/74. The installed-writing order node failed on the shipped mutant.
Full outputs and that failure are in
`/private/tmp/c2-functional-prose-order-outputs-21bea3ec.txt`.

This makes the evidence for the exact 644 reader hold set (seven definitions,
14 cases) available to its next reader; it does not clear those pins or
reconcile the remaining 159-node inventory. No source or test was changed in
primary. **Elapsed**: approximately 30 minutes including isolated mutations,
reports and the installed witness. **Tokens**: unknown.

## C2 held-carrier fresh reader -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

1. **Should it happen?** Yes for the exact seven definitions and 14 cases held at `644bbf1d`: the ten complete reports identify the affected carriers, changed context and moved units; the earlier 36-mutant record reports matching owner failures, and the four adjacency/context failures and installed-order failure are separately recorded.
2. **Best alternative.** Split hybrids, retaining real installs and source/output correspondence; fixed prose and its placement are the accepted retirement scope, while install behavior is not.
3. **What would show it wrong?** A missing carrier, unintelligible report, or failed retained correspondence after the split leaves that part open; check the final split at the required boundaries.

**Eligible wording parts:** in `contract/test_writing_rules_ship.py`, source and installed section order, source pointer adjacency, source readability context, and installed score prohibition; in `test_review_sweep_ships.py`, sweep/trap order and lens order, all parameters. This clears only the seven-definition hold set, not the rest of the inventory. Preserve real installs, parity, slots, placeholders, schema/mapping, SVG behavior and drain.

**Coverage:** Read `e1fe4c23`, the ten complete outputs at `/private/tmp/c2-functional-prose-order-outputs-21bea3ec.txt`, the recorded mutant and owner-failure evidence, and the current inventory. Did not rerun owner tests, replay the full matrix, assess security or conduct code review. This is the C2 reader prerequisite; the remaining inventory is still open. **Elapsed:** approximately 6 minutes. **Tokens:** unknown.

## C2 retired-instrument controls -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

1. **Should it happen?** Yes: the 13 controls below exercise wording instruments whose consumers have already been retired following the recorded carrier evidence and reader decisions. They do not test independent behavior.
2. **Best alternative.** Retain the separately identified install, parity and slot checks; keeping controls for removed wording instruments would preserve their burden without an active consumer.
3. **What would show it wrong?** A remaining live consumer or an assertion of independent behavior would require splitting or retaining that part; inspect references and the final deletion before integration.

**Eligible controls**, relative to `bootstrap/tests/`: in `test_review_stance_in_shipped_files.py`, `test_deleting_the_called_by_authority_sentence_is_reported`, `test_deleting_the_plan_obligation_sentence_is_reported`, `test_deleting_the_two_pass_sentence_is_reported`, `test_no_exemption_is_stale`, `test_no_file_an_adopter_receives_is_exempt`, `test_removing_an_exemption_is_reported`, `test_a_phrase_inserted_into_a_scanned_copy_is_reported`, `test_exempting_an_installed_file_is_reported`, and `test_the_walk_reaches_the_roots_it_claims`; in `test_review_sweep_ships.py`, `test_deleting_lens_4_is_reported`, `test_deleting_the_not_covered_half_is_reported`, `test_deleting_the_scope_sentence_is_reported`, and `test_adding_a_sixth_ledger_item_is_reported`. The 68 AGENTS mutants and their reader decision cover the first three; the 144-member dynamic transcript and `d6595191` cover the scan; the sweep structure evidence and `644bbf1d` cover the latter four. Delete unused instrument helpers only after checking remaining references.

**Coverage:** Compared these current control bodies with the inventory and recorded decisions; did not rerun tests or conduct code review. This is a C2 prerequisite only. Other remaining inventory and its evidence are still being reconciled. **Elapsed:** approximately 3 minutes. **Tokens:** unknown.

## Integrated inventory and self-hosted delivery -- Codex Terra coordinator -- 2026-11-09

Collection only, under Python 3.13.13, compared clean committed copies before
the two testing Decisions (`6f64ddf5`) and after their integration (`6623e1be`):
7,750 to 7,449 cases, a reduction of 301; 4,078 to 4,149 distinct collected
functions, an increase of 71. Functions are identified by source file and line.
The collections took 6.193 and 6.323 seconds and executed no test bodies.
Concurrent Git work is included; this is an interim whole-repository comparison,
not attribution to either plan or final completion evidence.

Python/JSON files beneath `bootstrap/tests` grew from 6,181,228 to 6,386,488
bytes and 121,951 to 126,159 lines, including fixtures and helpers. The two
replay scripts outside that tree add another 40,548 bytes and 856 lines.
Later default-family support and retirements are outside this snapshot.
Results: `/private/tmp/cairn-combined-test-inventory-geotqhat/result.json`.

The full 159-node inventory remains authoritative. The latest seven-definition
hold set and thirteen obsolete controls are subsets, not all remaining work.
The fixed `e1fe4c23` census still finds wording assertions across the stance
table and mixed readable-work, local-retry, stewardship and scientific checks.
The five model-tier nodes retain actual parity, install and mapping behavior.
Remaining RETIRE assertions keep their original evidence gates; no scope is
deferred or silently retained as a wording exception.

At `4fafbda7`, the existing collision-adoption command appended exactly nine
self-hosted file records and three new base caches. All prior rows, profile,
module roster, base fields and nine destination files stayed unchanged.
The ninth entry beyond the earlier eight-file assessment is the identical
delivered coupling tool. A disposable prototype had the same bounded delta.
On a clean committed copy, the installed-layout report and exact replacement
each exited zero; an altered helper record refused with exit two and the copy
was restored clean. The negative-check wrapper first misparsed the lock's
comment-prefixed JSON; using the existing reader corrected that probe without
repeating the two positives. Results:
`/private/tmp/cairn-selfhost-public-evd0gez0/result.json`.

Required reviews and final mapped verification remain open. **Elapsed:**
unknown beyond the figures above. **Tokens:** unknown.

## C2 batch A fresh reader -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

1. **Should it happen?** Yes for the specific parts below: the reports show the changed rule or inserted phrase on each named carrier, and the author reports the matching owner failures. They do not establish the other clauses of a multi-clause check.
2. **Best alternative.** Split the checks and retain slot and machine-token behavior. Fixed prose and instrument controls fall within accepted retirement; removing install behavior would lose a separate promise.
3. **What would show it wrong?** A missing carrier, incomplete report, surviving instrument consumer, or failed retained behavior would keep the affected part open. Inspect the split and run its mapped checks at the required boundaries.

**Eligible**, relative to `bootstrap/tests/test_review_stance_in_shipped_files.py`: the expected-value requirement and its generated expected-value mutation control in `test_security_cap_contract_is_present_and_each_surface_mutation_is_caught`, all eight carriers; `test_a_template_has_no_coverage_line_stanza`, all four templates, including its Foundations instrument control; and the two controls `test_deleting_the_two_pass_sentence_from_a_proposal_template_is_reported` and `test_deleting_the_obligation_sentence_from_a_plan_template_is_reported`, both template copies. In `test_module_says_what_it_is_for`, the four shipped-module cases and the own-module `the-sweep-and-the-trap-are-in-every-install` case are eligible. The roster node's separate probe-inventory assertion is eligible for both loop copies from the earlier vocabulary evidence and `d6595191`.

**Still open:** The security cap's normal limit, exception basis, insufficiency of prior evidence, named artifact and scope, Maintainer authorization, and renewed authorization on each pass need applicable carrier evidence. The other three own-module cases and ten roster labels lack accessible complete reports in this batch; the team node also needs its own assertions evidenced, including the negative collaboration-agreement phrase and shipped bootstrap wording. Template headers, review skeleton wording and module forbidden-pattern consumers are not cleared by these results. Preserve team-roster slot markers and placement and actual machine tokens. No accepted scope is deferred.

**Coverage:** Read committed test bodies at `3396ddfa`, the eight security, five saved obligation and four coverage reports in `/private/tmp/c2-batchA-*-results.tsv`, and the four relevant cases in `/private/tmp/cairn-c2-template-mutants.tsv` and their prior record. The author reports matching failures. Did not rerun owner tests, replay the matrix, assess security, or conduct code review. Over target to identify exact partial cases and remaining evidence. **Elapsed:** approximately 5 minutes. **Tokens:** unknown.

## C2 batch A reconstructed reports -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

1. **Should it happen?** Yes for the remaining roster and module cases and the two own-team positive assertions: separate committed copies based on `3396ddfa` show each exact adverse wording change in a complete report; the author reports the corresponding owner failures.
2. **Best alternative.** Retain the team slot markers and placement and leave the two still-unproven team wording assertions in place until their evidence is available. Fixed wording need not remain after its C2 evidence is complete.
3. **What would show it wrong?** An unreported carrier or assertion, incomplete result, or failed retained slot check would leave that part open; inspect the final split and run mapped checks at the required boundaries.

**Additional eligible parts**, relative to `bootstrap/tests/test_review_stance_in_shipped_files.py`: the five roster patterns for both loop files in `test_loop_document_roster_carries_the_obligation`; the three remaining own-module cases of `test_module_says_what_it_is_for`; and the two own-team positive wording assertions in `test_team_roster_has_its_own_section_without_adding_roles`. Together with the immediately preceding verdict, the roster and module definitions are eligible in full. The team node's own collaboration-agreement absence and shipped bootstrap sentence remain open; retain shipped slot markers and placement.

**Coverage:** Recreated only the 15 missing report mutations from the author's explicit list in separate copies; the canonical reporter's results and scratch commits are listed at `/private/tmp/c2-reader-reports-6d46a003.tsv`. The other five results and earlier probe evidence are covered in the preceding verdict. Did not rerun owner tests, assess security, or conduct code review. This is a C2 reader prerequisite, not full C2 completion. **Elapsed:** approximately 2 minutes. **Tokens:** unknown.

## C2 Batch B source-carrier proof -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On a disposable clone of `6511ac40`, the selected existing owner checks passed
at baseline: 111 passed, 168 deselected, Python 3.13.13. I re-enumerated
124 dynamic W live files and the 12 H carrier files. Separate committed scratch
mutants removed each of 40 R obligations, inserted the 28 forbidden examples
into each of 10 R carriers, removed each of 10 J obligations, and inserted
each of 19 H examples into its mapped carrier. The exact owning node failed
for each mutation. Seventy-eight reports showed a complete changed/raw span;
H shell cases were explicitly `NOT COMPARED` with complete raw output, and
three Python cases also retained complete raw additions. The remaining H case
inserted `security-asks-for-no-external-security-review` into `SECURITY.md`:
the exact pin failed, but `prose_diff.py` said `No functional prose changes
found in the base-root union`. `SECURITY.md` is absent from both
`scripts/content_scan_roots.txt` and `scripts/prose_roots.txt`; this is an
unresolved coverage gap, not clearance.

Eighteen additional scratch mutations exercised retained pair equality and
roster/drift controls, cleanup wording and role rows, anchor wording, trap
ordering, and representative dynamic W dangling-heading/checker checks. Each
showed a complete report and its exact owner assertion failed. The retained
model-selection and session-start pairs were each reworded consistently in
both copies; both equality nodes failed on the expected missing obligation.
W's actual live-file set was re-enumerated, but only `docs/glossary.md` was
mutated for each generic W check; the other 123 files remain unprobed for those
W predicates. H Python and shell unsupported/raw cases are evidence only for
the named carriers, not every possible source form. No canonical tests or
functional sources changed; no pins are cleared by this record.

Reports are retained temporarily at `/private/tmp/cairn-prose-stance-B-reports/`
and `/private/tmp/cairn-prose-stance-B-extra-reports/`; the runner is
`/private/tmp/cairn-prose-batchB-run.py` and the extra runners are
`/private/tmp/cairn-prose-batchB-extra-run.py` and
`/private/tmp/cairn-prose-batchB-pairs.py`. Scratch clone ended reset and clean.
The initial wrapper misclassified complete Python raw reports at probe 75;
that attempt and its logs remain preserved, and the corrected classification
was rerun for 75–79. **Elapsed**: approximately 50 minutes, including setup,
probe execution and audit. **Tokens**: unknown.

**Coverage:** Read the accepted inventory, current owner tests and prior A
reports; ran the bounded existing owner selection and these isolated
mutations only. Did not modify or remove canonical pins, resolve the
`SECURITY.md` root gap, mutate all dynamic W members, run a full suite, or
conduct code review or Security Review. Dynamic W coverage remains incomplete.

## C2 Batch A supplemental proof -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On frozen commit `3396ddfa7a976187dd98c02e9dd1be6d05a99f5e`, I completed
separate committed scratch mutations for the six remaining security-cap
clauses across all eight carriers (48 cases), all 22 old-vocabulary examples
across both dual-review module copies and all four authoring templates (132
cases), 20 proposal/plan skeleton question and wording assertions, and 20
header, Called-by, Obligation-slot and slot-order contract mutations. Six
additional plan-template mutants covered the code-review evidence and reviewer
floor assertions. Four copies inserted the forbidden `Not covered` stanza in
every template. Each mutation produced a complete source-side reporter span
and the matching exact existing owner node failed once. The expected-value
clause's eight carrier proofs are recorded in the preceding Batch A evidence.
Roster and module-purpose reports were reconstructed in the preceding reader
record.

Receipts: `/private/tmp/c2-batchA-cap-six-3396/results.tsv`,
`/private/tmp/c2-batchA-vocabulary-3396/results.tsv`,
`/private/tmp/c2-batchA-template-questions-3396/results.tsv`,
`/private/tmp/c2-batchA-plan-question-skeletons-3396/results.tsv`,
`/private/tmp/c2-batchA-plan-code-clauses-3396/results.tsv` and
`/private/tmp/c2-batchA-plan-code-clauses-3396-retry1/results.tsv`,
`/private/tmp/c2-batchA-template-contracts-3396/results.tsv`, and
`/private/tmp/c2-batchA-coverage-results.tsv`. The old carrier instrument
controls use `/private/tmp/cairn-c2-vocabulary-mutants.tsv`. One initial plan
question mutant changed the descriptive paragraph outside the skeleton; the
exact skeleton node stayed green. That attempt remains in its scratch copy,
and the corrected skeleton-only mutants are in the listed plan-question
report.

A consumer search found `tools/board.py` and its byte-identical installed
reader parse `Review` and `Plan review` header fields and `Tier`/`Obligation`
fields in review records. It found no tool reader for `Called by`; the quoted
call is a human check in the operative instructions. This record reports the
consumer boundary for the fresh reader and makes no disposition of individual
pins. The prior vocabulary transcript supplies the carrier instrument controls;
I did not replay them or the earlier 118 template reports. No canonical source
or test file changed in this batch. No owner matrix, broad mapped run, or full
suite ran.

**Not evidenced in Batch A:** the remaining assertions in the team-roster
owner node still need disposition: absence of collaboration_agreement.md, the
shipped “The bootstrap records the team here” sentence, the team-roster
start/end markers, and exclusion of team-roster from the shipped Team roles
section.

**Documentation checks:** under Python 3.13.13, `claim_check.py` and
`link_check.py` passed. `check_cairn.py` exited 1 with two unresolved paths
in other existing artifacts and four unused scanner allow entries; it named
no issue in this plan. The default-shell Python attempt failed before scanning
because its Git reader call rejected `realpath(strict=...)`; the canonical
Python run supplied the results above.

**Elapsed:** approximately 40 minutes. **Tokens:** unknown.

## C2 batches A and B fresh reader -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

1. **Should it happen?** Yes for the exact wording parts below: the reports identify each changed carrier and the recorded owner failures; the repaired SECURITY root and its replay now show the formerly missing case.
2. **Best alternative.** Split hybrids and preserve comparisons, install behavior and parsed fields. Keeping fixed prose pins would retain the burden the Decision removes.
3. **What would show it wrong?** A missing carrier, incomplete report or failed retained comparison would leave the affected part open; inspect the final split and run its mapped checks.

**Eligible**, all names relative to `bootstrap/tests/test_review_stance_in_shipped_files.py`: retire the remaining six clauses of `test_security_cap_contract_is_present_and_each_surface_mutation_is_caught` (the seventh was cleared earlier); `test_module_omits_the_old_vocabulary`, `test_module_forbidden_patterns_recognize_their_examples`, `test_template_omits_the_old_vocabulary`, and `test_template_forbidden_patterns_recognize_their_examples`; both proposal and plan question-skeleton nodes; and `test_a_template_offers_external_only_beside_called_by`. All parameters apply. In `test_plan_review_skeleton_names_its_security_obligation`, retire the fixed placeholder wording, preserving the slot and its ordering. Preserve actual parsed Review, Plan review, Tier and Obligation fields in the header/token nodes.

Also retire `test_shipped_text_carries_the_obligation`, `test_shipped_text_omits_the_old_wording`, and their forbidden-pattern control; the wording obligations in both byte-identical pair nodes, retaining equality; `test_the_cleanup_row_never_says_usual` and `test_the_cleanup_row_sits_in_the_role_table`; the hard-coded six-role list in `test_the_fidelity_sample_roster_agrees_with_the_loop_document`, retaining both roster comparisons; and `test_the_anchor_equals_the_approved_wording` with its retired-instrument control `test_a_reworded_anchor_is_reported`. In `test_doctrine_carries_the_statement` and `test_doctrine_omits_the_retired_privilege`, retire the evidenced obligation and forbidden-pattern assertions, all parameters, preserving the separate probe-inventory assertions. The retired-privilege instrument control may go when its consumers go. The earlier coverage-stanza clearance still applies.

**Hold:** team-roster assertions named at `189353fe`; unproved Internal row in `test_the_old_role_rows_are_gone`; trap-heading adjacency/order; and both dynamic live-document checks: only one of 124 members was mutated. Preserve slot markers and ordering, actual source/install correspondence, parity, schema and SVG behavior. No unlisted assertion is newly cleared.

**Coverage:** Read `189353fe`, `0705d322`, the A receipt sets including corrected six code clauses, B reports 001–097 and owner assertions. `67381ce` adds `SECURITY.md` to the base roots; `/private/tmp/cairn-c2-security-root-proof/` shows its exact added sentence and matching owner failure. B's shell and Python raw outputs support only their named mutations. Did not rerun owner tests, all dynamic members, code review or Security Review. This prerequisite exceeds the target to identify exact splits and holds. **Elapsed:** approximately 25 minutes. **Tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09 -- SECURITY.md coverage and portable mode fixture

Commit `67381ce47f6ba1d6e81481df8a0015c55ea9b01f` adds only root
`SECURITY.md` to Cairn's extra `scripts/prose_roots.txt`; the generic shipped
list and scanner roots stay unchanged. This makes the previously uncovered
H-carrier read part of the base-root union. In a separate clone of this new
base, the exact Batch B adverse sentence was appended and committed as scratch
`b60a31db6206`. The complete reporter output now reads `ADDED SECURITY.md
[sentence] [after unit 155]: The launcher is read by an External Security
review.` The exact owner node
`test_doctrine_omits_the_retired_privilege[security-asks-for-no-external-security-review]`
failed on that inserted phrase as expected. Full captures are at
`/private/tmp/cairn-c2-security-root-proof/report.txt` and `pytest.txt`.
This proves that one named formerly-uncovered pin is visible and catches its
specified mutation; it does not retire that pin or clear any other C2 hold.

Commit `2b067c347c3bbd2e24d6ab062f7a32eb64e485d1` repairs the mode fixture's
text assumption: it derives expected replacement bytes from the target's
original bytes, preserving host newline translation, and still compares the
captured target mode and POSIX `0640`. Its exact host node passed on a detached
clean clone under Python 3.13.13 (1 passed, 0.60 seconds).

On a clean Windows archive of `eaff9f82`, Python 3.13.17 ran six exact nodes:
`test_replacer_preserves_target_mode`, both source/installed
`test_replacer_report_marks_a_list_item_swap_by_unit_position` cases, both
source/installed `test_report_cli_marks_a_heading_move_by_unit_position`
cases, and `test_reports_parse_decode_and_out_of_root_link_failures_with_escaped_paths`.
Five passed; the mode case failed because Windows text creation produced CRLF
while the test expected LF. After the fixture-only correction, Root reran that
exact node from a clean archive of `2b067c34`: **1 passed in 2.20 seconds**.
Logs, XML and archive manifests are under `/private/tmp/cairn-prose-native-six-eaff9f82/`
and `/private/tmp/cairn-prose-native-mode-2b067c34/`. The `test_tiers.py for
scripts/prose_roots.txt` map selects `bootstrap/tests/security/test_prose_tools.py`
and `bootstrap/tests/test_content_scan.py`; that two-file host selection was
not run and remains for the shared C1 batch.

These focused receipts cover the named mutation and fixture nodes only. No
wording pin has been retired here; the remaining C2 inventory, its other
mutations, reviews and wide verification remain open. **Elapsed:** approximately
15 minutes; **tokens:** unknown.

## C2 dynamic W full-set and held-pin proofs -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

At frozen commit `ef39b2c7715fcfcf7b0c986f7887f09eab636f4e`, the current
`_live_files()` inventory contained 124 paths. The exact sorted set is retained
at `/private/tmp/cairn-prose-W-full-reports/live-files.txt` (SHA-256
`21fea00c48c567bce015486ce54eac12f59e066daa6d0ae46fb7df0a2b475ad3`). The
baseline two W nodes passed. For each of the 123 members other than
`docs/glossary.md`, a separate one-file scratch commit appended one dangling
heading citation and one retired-checker citation. The real reporter emitted
two complete `ADDED` spans naming that file, and both exact W nodes failed
with that file in their hit list. The earlier 094/095 `docs/glossary.md`
mutations are reusable: the owner test and `prose_diff.py` bytes are unchanged
between their base `6511ac40` and this frozen commit. Reports and exact node
outputs are in `/private/tmp/cairn-prose-W-full-reports/`; the scratch clone
ended reset and clean. This covers both W predicates across the enumerated
124 members, with one combined adverse per file.

Five further separate scratch commits cover held assertions: an Internal
Review row in each own/shipped model-selection carrier, removal of each of the
two fixed trap headings independently, and insertion of an intervening heading
while preserving their original order. Each report had the expected complete
`ADDED` or `REMOVED` heading/row span, and its exact existing owner node failed
at the named assertion. Receipts are in `/private/tmp/cairn-prose-B-held-reports/`.
The first wrapper attempt for the shipped Internal row required the literal
word `AssertionError`, which that assertion output does not print; its complete
report and pytest output are preserved, and the corrected wrapper reran and
passed all five classification checks. No canonical tests or functional prose
changed; no pin is retired here. The separate `SECURITY.md` root-union gap from
Batch B remains unresolved.

**Coverage:** Used Python 3.13.13, the exact enumerated current W set, the
existing source reporter and exact owner nodes in separate scratch commits.
Did not run a full suite, alter roots or canonical files, retire pins, or
conduct code review or Security Review. **Elapsed:** approximately 70 minutes,
including serial scratch commits, focused checks and audit. **Tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09 -- current and historical path claims

Commit `4d12b27f0aa2c83e4e205ab56cb79a15ccb9068c` corrects the active
strategy citation to `bootstrap/tests/contract/test_test_tiers.py` and adds one
exact-path exemption for the historical code-map test citation in the immutable
architecture record. That path is present at its cited commit `9547bf74`; the
archive prose remains unchanged. The exception is document-scoped and leaves
all other config entries untouched.

On a detached clean copy under Python 3.13.13, `claim_check.py` passed both the
strategy and architecture files; it reported the single configured historical
path exemption. One run of `scripts/check_cairn.py` exited 0 after scanning 200
Markdown files. It emitted four unused scanner-entry advisories on stderr;
these were non-failing notices and did not justify removing existing entries.
The combined mapped selection for `scripts/prose_roots.txt`, the strategy,
the config and the historical plan is three files:
`bootstrap/tests/integration/test_claim_check_allow_config.py`,
`bootstrap/tests/security/test_prose_tools.py`, and
`bootstrap/tests/test_content_scan.py`. Those tests are pending the shared C1
host batch and were not run here. No full suite or broader test selection ran.
**Elapsed:** approximately 6 minutes; **tokens:** unknown.

## C2 inventory scope interpretation -- GPT-6.1 Sol (Strategy, High) -- 2026-11-09

The accepted outcome includes old wording pins omitted from the nine-owner
inventory. That inventory is incomplete; it is not an exception to retirement.
The accepted source quotes the Maintainer's 2026-11-06 direction, "anytime we
edit something that is doctrinal as opposed to documentary, then we use exact
text replacement period. That way we can discard the pin testing entirely."
Its Decision summary says "Every other pin retires", retaining only the
drain-mode pin, and the 2026-11-08 Decision accepts the heavy proposal. Outcome
3's "files above" describes the measured inventory; reading it as a permanent
exclusion would silently narrow that categorical direction. This is an
interpretation of existing accepted scope, not a new delegated Decision or a
waiver of C2 evidence.

At committed `df99d1bd`, two concrete omissions are
`bootstrap/tests/contract/test_comprehension_floor.py` and
`bootstrap/tests/test_scope_reduction_trap.py`. Both already exist at the
source's measurement base `176d2caf`. The former's `_REQUIRED` regex assertions
and review-section assertion check prose obligations and placement, not copy
equality. The latter has obligation regexes, fixed headings and declaration
wording, plus a real-installer helper. Calling an assertion semantic or placing
it after installation does not turn its fixed wording predicate into executed
agent behavior. Conversely, its real install, delivered-file and genuinely
parsed token/schema contracts must survive any split.

The next step is a Medium assertion-and-carrier inventory of these omissions
and any other existing wording-pin owners found by the bounded repository
search. Append named dispositions and carrier sets before assigning Low
retirement. Apply the existing C2 coverage, separate-copy adverse-mutation and
fresh-reader prerequisites to each wording assertion; unresolved evidence
keeps that assertion open. Retain actual copy parity, real installation,
machine-token/schema consumers and other behavior. This authorizes neither
deleting unenumerated assertions nor treating unrelated behavior as a pin.
The least involved alternative, stopping at nine owners, leaves known accepted
retirement unfinished. Correcting the inventory delivers the same outcome
with additional audit work and no new human operation or recurring mechanism.

**Coverage:** Read the accepted source, its Decision and amendment, current
proposal/plan templates, plan scope/C2 criteria, and the two committed owners;
confirmed their existence at the source base. Did not conduct a full owner
census, inspect every token consumer, run tests or mutants, retire tests, or
perform code review or Security Review. Root owns the next serialized board
update. **Elapsed:** approximately 12 minutes including serialization wait.
**Tokens:** unknown.

## C2 cleared wording-pin retirement -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commit `2e79c27a` retires only the wording assertions newly cleared by the
Batch A and B fresh-reader verdict at `6c6b257a` in
`bootstrap/tests/test_review_stance_in_shipped_files.py`. It removes the
cleared security-cap, module/template vocabulary, question-skeleton, coverage
stanza, shipped-copy wording, doctrine-anchor and doctrine-phrase checks, plus
their now-unused private patterns and mutation helpers. The mixed plan-review
skeleton check still requires the `Obligation` field before the `Tier` field;
the actual header tokens, source/install equality checks, both roster
comparisons, probe-inventory checks and structural trap checks remain.

The team node retains the two reader-held assertions (absence of
`collaboration_agreement.md` in the own copy and the shipped bootstrap sentence)
and the shipped slot markers and placement. The unproved Internal role-row
assertion also remains. The eligible wording parts were removed without adding
new pins or changing functional prose.

Under Python 3.13.13, collect-only on the changed owner file reported 134
collected cases. The focused retained selection passed 13 cases in 0.04
seconds: team holds and slot markers, roster-to-fidelity comparisons, template
field/order checks, source/install byte parity and the held role rows. The
pre-retirement case count from the committed parent was not separately
collected; Root will compare the clean integrated parent and result once the
next bounded retirement batch is committed. No integrated net-volume claim is
made here.

**Coverage:** Applied only the exact cleared set in the reader record, kept
all named holds, collected the changed owner and ran its focused retained
nodes. Did not run the broad owner file, full suite, remaining inventory,
Boundary B, code review or Security Review. Those remain open. **Elapsed:**
approximately 30 minutes including focused edit and verification. **Tokens:**
unknown.

## C2 W and held-pin fresh reader -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

1. **Should it happen?** Yes: every member of the frozen 124-file W set has matching carrier reports and owner failures; the five held mutations and earlier order mutation show the remaining assertions.
2. **Best alternative.** Retire only these wording checks and keep unrelated behavior, parity and slot checks. Their fixed terms need not constrain future prose edits.
3. **What would show it wrong?** A missing member, incomplete report or changed owner/reporter bytes would leave the affected check open; check the final split and mapped tests.

**Eligible**, in `bootstrap/tests/test_review_stance_in_shipped_files.py`: `test_no_live_document_cites_a_heading_that_does_not_exist`, `test_no_live_document_credits_a_checker_that_does_not_exist`, `test_the_old_role_rows_are_gone` (both parameters, including its wording control), and `test_the_two_trap_headings_are_adjacent_and_in_order`. No other assertions are cleared here.

**Coverage:** Read `df99d1bd`, the 124-path list and all 123 paired report/test outputs in `/private/tmp/cairn-prose-W-full-reports/`: each names its one carrier, both added strings and both failing nodes. The prior glossary 094/095 outputs cover the one remaining member; owner and reporter bytes match between bases `6511ac40` and `ef39b2c7`. Read all five held outputs and prior 093. The statement in `df99d1bd` that SECURITY coverage remains unresolved is stale: `67381ce` and the replay recorded at `6c6b257a` closed that exact gap. Did not rerun owner tests or perform code or Security Review. **Elapsed:** approximately 8 minutes. **Tokens:** unknown.

## C2 expanded inventory, first tranche -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

At committed `df99d1bd`, the source tree has 144 `test_*.py` files; this is a file census, not the host's collected-test-file count. The original nine-owner inventory and dispositions above remain in force. The following additional nodes have fixed wording assertions; RETIRE is a disposition, not clearance to delete. Each still needs C2's per-carrier coverage and applicable independent-copy mutations and reader evidence. This tranche is incomplete: the remaining owners and ambiguous cases are still under examination.

| Owner and node, under `bootstrap/tests/` | Actual carriers | Disposition |
|---|---|---|
| `contract/test_comprehension_floor.py::test_comprehension_floor_obligation_present`, `::test_comprehension_floor_sits_in_the_review_section` | `AGENTS.md`, `templates/core/AGENTS.md` | RETIRE fixed obligation alternatives and placement; prove each parameter and move/removal. |
| `test_scope_reduction_trap.py::test_each_remainder_entry_asks_for_its_own_disposition`, `::test_scope_reduction_obligation_present`, `::test_the_canonical_section_exists_and_sits_beside_its_mirror` | Four proposal/plan templates; `_SURFACES` lists 14 own/shipped governing, loop, template, board and doctrine files; `docs/methodology/dual-review.md` | RETIRE obligation patterns and fixed heading/placement. KEEP the real two-profile installs in the hybrid and establish corresponding source-to-installed content evidence. |
| `test_scope_reduction_trap.py::test_every_template_prints_the_same_declaration_grammar` | `docs/methodology/proposals.md` and four proposal/plan templates | RETIRE only any fixed prose outside actual parsed declaration grammar; KEEP the grammar and parser contract. |
| `test_coordination_broad_intent.py::TestBroadIntentBoundary::test_minimal_install_omits_broad_obligation`, `::test_coordination_tiers_install_carries_broad_obligation` | Real minimal and coordination installs; installed Markdown, especially `dev/modules/coordination-tiers.md` | RETIRE fixed positive/negative rule phrases. KEEP both real installs, module selection and file/slot behavior; enumerate the dynamic install set before a set-wide claim. |
| `test_agreement_retired.py::test_shipped_roles_retain_the_two_agreement_sentences_without_local_rule` | `templates/core/dev/agent_collaboration.md`, `dev/agent_collaboration.md` | RETIRE two fixed role sentences and wording presence/absence; KEEP team-roster slot count. |
| `test_skill_contract.py::test_full_handoff_smoke_reporting_contract`, `::test_smoke_reporting_contract_rejects_false_passes` | `templates/skills/session-end/SKILL.md` and the latter's temporary copy | RETIRE eight phrase pins and their mutation instrument after source evidence. KEEP actual skill frontmatter, `$ARGUMENTS`, path and execution contracts elsewhere. |
| `test_security_stack.py::TestSecurityReviewDoctrine::test_injection_review_by_class_procedure_present`, `::test_v1_self_audit_scope_statement_present`, `::test_no_modflow_tools_specific_tool_names_leaked` | `templates/modules/team-gated/security-review.md` | RETIRE named positive and negative prose pins after each corresponding mutation; retain actual security and installation behavior elsewhere. |
| `test_skills_onboarding.py::test_passive_session_start_pointer_seeded_once` | Three real preset installs, installed `dev/PLANNING.md`; onboarding template sources | RETIRE the fixed sentence assertion; KEEP actual installs, command/pointer counts and seed/trigger machinery. |

**Proof boundary:** No deletion follows from this author inventory. Enumerate the exact parameter/carrier set from the committed owner, cover each source with the base-root union, and show the appropriate removal, contrary or negative-term mutation in a separate copy. For installed hybrids retain real installation and correspondence; preserve schema, parsed tokens, slots and public behavior. No tests or full suite ran. **Elapsed:** approximately 18 minutes for this tranche. **Tokens:** unknown.

## C2 expanded inventory, second tranche -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

This continues `3a14f34b`, with the same RETIRE prerequisites and no deletion clearance. Names are relative to `bootstrap/tests/`; class names below qualify each following node. Original nine-owner dispositions remain above. The complete owner census remains open.

| Owner and nodes | Carriers | Disposition |
|---|---|---|
| `test_install_time_onboarding.py::TestAdoptionAndSessionPointersShip::{test_bootstrap_step_ii6_points_at_the_day_one_list,test_session_start_step_three_names_the_first_onboarding_task,test_a_bullet_under_step_four_does_not_count,test_dropping_the_candidate_and_data_clause_is_caught,test_deleting_either_pointer_is_caught}` | `bootstrap/BOOTSTRAP.md`, `templates/skills/session-start/SKILL.md`, `.agents/skills/session-start/SKILL.md` | RETIRE fixed pointer wording, placement and wording-instrument controls. KEEP the separate skill byte-equality node. |
| `test_install_time_onboarding.py::TestDoctrineStatesTheInstallTimeModel::test_the_doctrine_opens_with_the_model_and_names_no_helper`; `::TestUpgradeLeavesAnOldHelperAlone::{test_the_guide_names_the_step_and_the_three_loose_files,test_the_guide_names_no_prompt_that_shows_later}` | `docs/methodology/onboarding.md`, upgrade guide source | RETIRE prose phrase and negative wording assertions; KEEP actual upgrade behavior and parsed commands. |
| `test_install_time_onboarding.py::TestEveryFormerPromptHasAnInstallTimeHome::{test_sentences_a_to_e_are_in_the_installed_slot,test_a_deleted_sentence_is_reported,test_no_former_prompt_sits_inside_a_conditional}` | Three onboarding preset templates and their real installed `dev/PLANNING.md` slots, across `TEAM_SHAPES` | RETIRE fixed sentence/placement and their wording control. KEEP real installs, source/output correspondence and actual conditional/slot machinery; enumerate each profile/team carrier before proof. |
| `test_model_selection_stub.py::TestAcceptanceChecklistNamesTheMappingCheck::test_item_and_fourth_allowed_class`; `::TestShippedWordsArePinnedByExactString::{test_module_twins_name_staleness_and_the_human_trigger,test_waiting_line_in_both_presets}`; `::TestFamilyNotVersionReachesEverySite::{test_all_model_mapping_sites,test_installed_module_explains_extra_family_rows}` | `bootstrap/BOOTSTRAP.md`, own/shipped model-selection modules, collaborative and legacy onboarding templates, mapping stub and `bootstrap/_scaffold/install.py`; real installed module | RETIRE fixed guidance wording only. KEEP module equality, real install and correspondence, actual mapping schema, waiting/seed tokens and engine behavior; Python-string coverage must be demonstrated. |
| `test_practice_modules.py::TestInstallPath::test_modules_install_on_selection` | Real selected installs from `templates/modules/team-gated/`, notably `testing-discipline.md` | RETIRE fixed guidance sentences. KEEP installs, cross-link validity, tool byte equality and its real workflow. |
| `test_documentation_plan_module.py::TestInstallPath::test_scaffolded_duty_guard_rejects_deletion_and_inversion`; `::TestForkableContent::{test_forkable_carries_four_layer_vision,test_forkable_carries_decision_procedure,test_forkable_carries_agents_boundary_doctrine}`; `::TestCairnSelfHosted::test_cairn_dogfoods_the_module` | Real installed `AGENTS.md` and `docs/DOCUMENTATION_PLAN.md`; shipped module/forkable sources; own `docs/DOCUMENTATION_PLAN.md` | RETIRE rule phrase and instrument assertions. KEEP installs, file presence, source/output correspondence, valid links and slot anchors. |
| `test_incident_trackers_module.py::TestSchemaContract::test_template_defines_confirmed_sweep_reporting` | `templates/modules/default-on/incident_log_template.md` | RETIRE six fixed prose assertions; KEEP independent tracker schema and parser behavior. |
| `test_reanchor.py::TestTheRunbookAndTheRegistryAgree::{test_the_runbook_answers_where_the_review_manifest_comes_from,test_the_runbook_answers_how_to_read_the_report,test_the_runbook_lists_the_prerequisites,test_the_runbook_tells_the_operator_the_values_file_goes_stale,test_the_runbook_says_the_agreement_check_is_shape_only}` | `bootstrap/REANCHOR_RUNBOOK.md` | RETIRE fixed explanatory prose and heading assertions after exact mutants. KEEP actual registry-ID correspondence, executable commands and ceremony behavior. |

**Coverage:** Read these committed node bodies and source declarations; this is classification, not a code or Security Review. No tests ran. Further owner families, including verification boundaries and documentation governance, still require node-level disposition. **Elapsed:** approximately 12 minutes. **Tokens:** unknown.


## C2 team wording-hold proofs -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On two separate copies frozen at `734f65778ac119b604618504d48d9ea6962ec79d`,
I tested the two assertions still held in
`test_team_roster_has_its_own_section_without_adding_roles`. Commit
`52503308a8c7ad3e1a966c4795099d54d9889690` adds a reference in own
`dev/agent_collaboration.md` to the real archived removal proposal. The source
reporter shows the complete added sentence after unit 27, and the exact node
fails at the `collaboration_agreement.md` absence assertion. Commit
`5acb244098322f9ee3bf8b0d2f5e81b2fb189c7b` removes the shipped bootstrap
roster sentence while retaining its slot markers and placement. The reporter
shows the complete changed range at before/after units 33–34, and the exact
node fails at the shipped bootstrap-sentence assertion.

Reports and matching owner-node failures are preserved at
`/private/tmp/c2-team-hold-reports-734f/{own-report.txt,own-test.txt,shipped-report.txt,shipped-test.txt}`.
No canonical source or test bytes changed. The two assertions remain held until
the fresh reader records the eligibility supplement. **Coverage:** Ran the
existing source-side reporter and exact owner node once in each separate
frozen mutation copy; no broader matrix or canonical test run. **Elapsed:**
approximately 10 minutes. **Tokens:** unknown.

## C2 team wording fresh reader -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

1. **Should it happen?** Yes: the two reports show the exact adverse change in each carrier and each matching owner assertion fails.
2. **Best alternative.** Split the node and preserve its shipped team-roster slot markers and placement; only the fixed wording needs retirement.
3. **What would show it wrong?** A lost slot or an incorrect source/output correspondence would leave the split open; run the mapped checks on the final change.

**Eligible:** in `bootstrap/tests/test_review_stance_in_shipped_files.py::test_team_roster_has_its_own_section_without_adding_roles`, retire the own `collaboration_agreement.md` absence assertion and shipped `The bootstrap records the team here` sentence assertion. Preserve the team-roster start/end markers and the assertion excluding the slot from the shipped Team roles section. Earlier clearances of the own positive wording remain unchanged.

**Coverage:** Read committed `a2a5e081` and both full reporter and exact failing-node outputs in `/private/tmp/c2-team-hold-reports-734f/`. The shipped mutation retains the markers while deleting the sentence. Did not rerun owner tests or conduct code or Security Review. **Elapsed:** approximately 3 minutes. **Tokens:** unknown.

## C2 expanded inventory, third tranche -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

This continues `3a14f34b` and `5dcc7a51`; RETIRE remains conditional on the same per-carrier C2 evidence. Names are relative to `bootstrap/tests/`. The census is not yet complete.

| Owner and nodes | Carriers | Disposition |
|---|---|---|
| `test_scaffold.py::TestInstallCore::{test_installs_agents_md,test_installs_changelog_and_publishes_its_mapping}`, `::TestNewTeamGatedModules::test_new_module_installs_when_selected`, `::TestVendorWrapper::test_vendor_md_imports_agents_and_stays_thin` | Real core/module installs from `templates/core/AGENTS.md`, `templates/core/CHANGELOG.md`, `templates/core/VENDOR.md`, and `templates/modules/team-gated/security-review.md` | RETIRE fixed cap, changelog instruction and wrapper prose assertions. KEEP real installation, substitutions, manifest, actual import/slot markers and changelog schema/order; prove correspondence. |
| `test_doc_governance.py::TestTierRecognition::{test_descriptive_layer_section_present,test_names_the_four_conventional_tiers,test_uses_commonly_lives_in_framing_not_legislation}`, `::TestCommonHomesForVision::{test_common_homes_section_present,test_names_the_four_typical_homes,test_is_non_prescriptive}`, `::TestFormatNeutrality::{test_format_neutrality_section_present,test_names_multiple_doc_formats,test_disclaims_adopter_tree_assumptions}`, `::TestStyleConventionsLocation::{test_style_conventions_section_present,test_names_descriptive_layer_as_principle,test_names_multiple_style_homes,test_is_non_prescriptive}` | `docs/methodology/doc-governance.md` | RETIRE fixed positive/negative prose and heading pins, each separately evidenced. KEEP actual link and path validation. |
| `test_doc_governance.py::TestDevReadmeTemplate::{test_dev_readme_does_not_mention_vision_md_in_optional_additions,test_dev_readme_points_at_doc_governance_for_vision_home}` | `templates/core/dev/README.md` | RETIRE fixed positive/negative wording after applicable mutations; KEEP actual link validation. |
| `test_incident_trackers_module.py::TestDoctrineCrossReferences::{test_rationale_md_names_trackers_module,test_session_routines_carries_migration_substep}` | `docs/methodology/rationale.md`, `docs/methodology/session-routines.md` | RETIRE fixed reference and rule phrase pins after exact mutations; KEEP actual links and runtime migration behavior. |
| `test_session_routines.py::test_module_docstring_scopes_dry_run_claim_to_session_end` | Python module docstring in `templates/skills/_lib/session.py` | RETIRE fixed positive/negative docstring wording only after reporting its exact Python mutations. KEEP CLI dry-run execution, public help and byte-identical installed reader. |

`test_doc_governance.py::TestModuleDisambiguation` and `::TestInstalledAdopterWording` combine wording with path-origin and install correspondence: hold their exact assertions for consumer mapping. The large `contract/test_verification_boundaries.py` family also requires per-node split of wording from real schema/tokens and quality-gate behavior; it is not cleared by this tranche. No tests ran. **Elapsed:** approximately 10 minutes. **Tokens:** unknown.

## C2 expanded inventory, verification family -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

This continues `600fafe6`; RETIRE is conditional on the same individual carrier, mutation and reader gates. All nodes below belong to `bootstrap/tests/contract/test_verification_boundaries.py`. The full owner census remains open.

| Nodes | Carriers | Disposition |
|---|---|---|
| `test_both_operational_surfaces_separate_change_checks_from_tree_certification`, `test_operational_guard_detects_removed_wide_surface_fence`, `test_installed_operational_rule_is_project_general` | Own and shipped `AGENTS.md` | RETIRE positive/negative rule prose and wording-instrument assertions. KEEP real schema and mode tokens where consumed. |
| `test_scoped_defaults_reach_core_templates_and_optional_module`, `test_scientific_testing_guidance_is_narrow_and_falsifiable`, `test_plan_templates_offer_optional_observable_criteria_prompts` | Both AGENTS, plan and proposal templates, `docs/methodology/{plans,dual-review}.md`, own/shipped `testing-discipline.md`, as each node's surface tuple specifies | RETIRE fixed guidance phrases and their instrument assertions. KEEP actual module equality in its separate node and any parsed schema or slot tokens. |
| `test_plan_doctrine_binds_record_to_tested_range`, `test_actual_certification_has_one_discoverable_shared_record`, `test_shipped_guidance_records_and_finds_actual_runs`, `test_record_schema_guard_detects_removed_reviewed_range` | `docs/methodology/plans.md`, own/shipped AGENTS and plan templates, review doctrine, as each node names | RETIRE explanatory rule and negative wording assertions. KEEP actual record fields, structured tokens, discoverable command and executable behavior; split wording-instrument controls accordingly. |
| `test_review_doctrine_requires_targeted_falsification_and_replacement_triggers`, `test_plan_and_review_doctrine_share_record_replacement_triggers`, `test_review_reuse_guard_detects_unconditional_reuse` | `docs/methodology/dual-review.md`, and `docs/methodology/plans.md` where named | RETIRE fixed prose, numbered prose placement and wording-instrument assertions. KEEP actual review record fields and parsed values. |
| `test_change_verification_contract_reaches_every_surface`, `test_change_verification_guard_detects_removed_wide_fence`, `test_already_open_plans_can_switch_by_one_line`, `test_change_verification_guard_is_not_satisfied_by_an_empty_file`, `test_boundary_c_adjudicates_a_scoped_record`, `test_wider_run_verdict_invalidates_the_scoped_record` | Own/shipped AGENTS and plan templates, `docs/methodology/plans.md` and `docs/methodology/dual-review.md`, as each node's surface set specifies | RETIRE fixed rule phrases and associated instrument checks. KEEP any actual `bounded`, `wide`, Bounding and verdict fields that consumers parse. |
| `test_both_plan_templates_carry_record_and_review_contract`, `test_plan_template_guard_detects_removed_reviewed_range`, `test_both_proposal_templates_reject_speed_as_coverage` | Own/shipped plan and proposal templates | RETIRE prose-only assertions and wording-instrument controls. KEEP verification slot markers and any actual record schema, token and parser contracts. |

The separate equality and quality-gate-dispatch tests exercise behavior and remain KEEP. For each grouped node, enumerate its exact surface tuple and each wording assertion before independent mutation; this inventory grants no deletion. No tests ran. **Elapsed:** approximately 8 minutes. **Tokens:** unknown.

## C2 expanded inventory, security hybrids -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

This continues `ef562bb7` with the same C2 proof gates; the full owner census remains open. Names below are relative to `bootstrap/tests/`.

| Node | Carrier | Disposition |
|---|---|---|
| `test_portable_security_sweeps.py::test_the_trust_roots_are_enumerated_not_generalized` | `templates/modules/team-gated/portable-security-sweeps.md` and real runner | RETIRE fixed host-name and provenance explanation prose after exact mutations; KEEP the real runner trust-root tuple and execution/security behavior. |
| `test_security_stack.py::TestAuditRootsManifest::test_shipped_audited_set_matches_its_documented_roots` | `dev/modules/content-security.md` and shipped `content_scan_roots.txt` | RETIRE fixed documentation phrases; KEEP actual loaded root list and manifest parsing. |
| `test_security_verification.py::TestBindingModeClosure::test_the_module_doctrine_states_not_applicable_is_not_evidence` | `templates/modules/default-on/security-verification.md` | RETIRE fixed explanation and forbidden-phrase-in-paragraph pins after applicable mutations. KEEP the actual `NOT_APPLICABLE` result token and security behavior. |
| `test_repin_ceremony.py::test_runbook_describes_the_generated_packet_and_launcher` | `bootstrap/REANCHOR_RUNBOOK.md` and `bootstrap/reanchor-launcher.template.sh` | RETIRE prose-only explanation after separate source mutations. KEEP actual packet format, launcher tokens and executable ceremony contract. |
| `test_board_json_contract.py::TestIntentJoinRecipe::test_intent_join_matches_by_stem_only_and_canned_shape_matches_real_tool` | Board guide section and real board/intent tools | RETIRE fixed guide sentence only; KEEP actual join, schema, refusal and tool behavior. |

**Clarification to `734f6577`:** the “wording control” is the row-present assertion inside `test_the_old_role_rows_are_gone`. `test_a_sample_roster_with_an_old_role_is_reported` remains KEEP as the separate roster-drift comparison. No tests ran and no new pin is cleared by this inventory. **Elapsed:** approximately 5 minutes. **Tokens:** unknown.

## C2 expanded inventory, runbook and link hybrids -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

This continues `02d58b91`; RETIRE remains conditional on exact C2 coverage, mutations and fresh reader evidence. Names are relative to `bootstrap/tests/`; the full owner census remains open.

| Nodes | Carriers | Disposition |
|---|---|---|
| `test_repin_ceremony.py::{test_the_page_drops_the_hand_steps_and_says_nothing_calls_promote,test_the_runbook_names_no_ref_that_no_live_step_creates_and_says_what_follows_its_page,test_the_table_says_e7_binds_the_digest_and_not_the_hits_listed,test_neither_the_page_nor_the_artifact_tells_anyone_to_load_the_key,test_a_transition_packet_drives_both_stages_against_a_disposable_signed_anchor}` | `bootstrap/REANCHOR_RUNBOOK.md`, launcher/ceremony source and actual disposable ceremony where each node reads them | RETIRE fixed explanatory positive/negative prose and placement assertions; KEEP actual executable commands, code behavior, signature/ref checks, real ceremony and output semantics. |
| `test_gate_preflight.py::TestRunbookPublicationText::{test_no_partial_push_fallback_is_offered,test_publication_is_verified_by_reading_the_remote_back,test_phase_5_is_marked_maintainer_only}` | `bootstrap/REANCHOR_RUNBOOK.md` | RETIRE fixed explanatory phrases and human-facing placement only after exact mutants. KEEP atomic push, explicit refspecs, remote readback and executable command checks. |
| `test_gate_preflight.py::TestTheTwoStagesWantOppositeAgentStates::{test_the_artifact_says_the_asymmetry_is_deliberate,test_the_probe_docstring_does_not_call_itself_non_interactive}` | Ceremony artifact and `bootstrap/tests/_gate_preflight.py` docstring | RETIRE fixed explanation and docstring wording after raw/Python reporter coverage; KEEP actual two-stage behavior and key-handling tests. |
| `test_doc_governance.py::TestModuleDisambiguation::{test_module_uses_cairns_own_prefix,test_module_uses_cairn_prefixed_path}`, `::TestInstalledAdopterWording::{test_installed_module_carries_cairns_own_prefix,test_installed_module_does_not_assume_adopter_markdown}` | Three team-gated module sources (`examples-gallery`, `doc-drift-prevention`, `testing-discipline`) and their real installs | RETIRE fixed link-label wording; KEEP actual valid destinations, real installs and source/output correspondence. Enumerate all three carriers for each applicable assertion. |

These are author dispositions, not deletion authorization. Other tests in these files that parse or execute commands and validate security behavior remain KEEP; do not remove a whole hybrid. No tests ran. **Elapsed:** approximately 5 minutes. **Tokens:** unknown.

## C2 additional wording-pin retirement verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commit `55b5c333` applies the exact clearances from `734f6577` and
`a4a0a285` in `bootstrap/tests/test_review_stance_in_shipped_files.py`. It
removes the two W live-document wording scans and their now-unused private walk
and regex helpers, both parameters of the old-role row wording check, the trap
heading order pin, and the two team wording assertions. It also completes the
prior 6c6b/6d46 clearance of `test_loop_document_roster_carries_the_obligation`
for five patterns across both loop files, including its probe-inventory wording
assertion, and removes its now-unused obligation map.

The mixed team node retains the shipped slot start/end markers and the
exclusion from Team roles. Both roster-to-fidelity comparisons and the separate
roster-drift control remain. Earlier-retained template fields and ordering,
source/install byte equality, schema/token checks and unrelated behavior remain
in place. The two team adverse mutations and expected node failures are recorded
above at `/private/tmp/c2-team-hold-reports-734f/`.

On clean detached commit `55b5c333`, 13 focused retained cases passed under
Python 3.13.13 in 0.16 seconds. They cover team markers and placement, fidelity
and roster-drift comparisons, template field/order checks, source/install byte
parity and surviving pattern controls. I did not run the broad owner file or
another collect-only pass; Root is measuring the committed parent and final
combined tree once for owner definition/case and integrated-volume counts.

**Coverage:** Applied only committed reader clearances; removed private helpers
only when their consumers were removed. Preserved the actual roster drift,
slot, parity and schema behavior. No broad suite, Boundary B, code review or
Security Review ran in this step. **Elapsed:** approximately 25 minutes
including mutations and focused checks. **Tokens:** unknown.

## C2 docstring boundary and further candidates -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

**Hold for consumer mapping:** The docstring dispositions at `600fafe6` and `17040814` are provisional, not permission to remove a disclosure: trace runtime readers and public help first, retain public diagnostic semantics or map them to an existing public behavior witness, and group unresolved boundaries for High. `_gate_preflight.py` passes its module docstring to argparse; the tested `probe_cannot_sign` function docstring is distinct. The named session, checker and board parsers use explicit descriptions in their parser definitions, but that alone does not establish that no other consumer exists.

Additional candidates, names relative to `bootstrap/tests/`, need that mapping and the normal C2 per-carrier proof before any retirement:

| Node | Carrier and boundary |
|---|---|
| `test_model_selection_stub.py::TestBarePathResidualIsPinned::test_docstring_names_bare_path_residual_classes` | `templates/modules/team-gated/check_model_selection.py` docstring; retain checker behavior and the separate byte-equality test. |
| `test_security_stack.py::TestRunnerUrlRoleBoundary::test_bare_url_in_known_prose_is_the_named_residual` | `templates/modules/team-gated/content_scan_runner.py` docstring; retain the real scanner result and URL-role behavior. |
| `test_board_json_contract.py::TestSymlinkedSourcesAreNotRead::test_symlinked_root_or_parent_above_root_is_read_normally` | `tools/board.py` docstring; retain actual symlink and output behavior. |
| `test_reanchor_driver_disclosures.py::TestTheClosureListIsReadFromTheTemplate::test_the_launcher_template_is_a_member_and_the_docstring_agrees` | `scripts/reanchor_ceremony.py` function docstring; retain actual closure membership and refusal behavior. |
| `test_verify_integrity.py::test_the_hint_and_the_guide_no_longer_offer_history_as_enough` | `bootstrap/verify_integrity.py` and `bootstrap/UPGRADE.md`; retain actual public diagnostic and working recovery. |

The source-glob census at `df99d1bd` contains 138 `test_*.py` files beneath `bootstrap/tests`, three test files in examples/measurement, and three executable tools named `test_*.py`; the earlier 144 count was the whole-tree filename count, not 144 collected test owners. The remainder of the owner census is still open. No tests ran. **Elapsed:** approximately 5 minutes. **Tokens:** unknown.

## C2 expanded inventory, next-session rules -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

This continues `d9be7a53`; RETIRE remains conditional on the exact C2 carrier, mutation and reader gates. The full owner census remains open. All nodes below belong to `bootstrap/tests/test_next_session_local_note.py`.

| Nodes | Carriers | Disposition |
|---|---|---|
| `test_every_writer_copy_forbids_copying_outside_text_and_limits_the_ignore_remedy`, `test_every_read_copy_says_the_note_is_data_not_instructions`, `test_every_copy_of_the_note_rules_refuses_a_link_a_linked_parent_a_folder_or_a_tracked_path`, `test_every_copy_of_the_note_rules_pins_the_action_of_each_rule` | `docs/methodology/session-routines.md`, own/shipped `AGENTS.md`, and own/shipped session-start and session-end `SKILL.md`, as each dynamic group specifies | RETIRE fixed per-rule phrases and their synthetic removal controls after each applicable carrier and phrase is independently evidenced. The seven exact carrier paths were enumerated from `df99d1bd`; retain any real behavior, parity and protected drain tests. |
| `test_no_shipped_source_tells_a_reader_to_read_or_write_the_retired_file` | Dynamic tracked shipped-source set from `_shipped_sources()` | RETIRE only fixed prose absence after enumerating and mutating every applicable member. HOLD code-name/behavior portions pending High boundary mapping; do not treat a representative file as proof of the whole set. |
| `test_no_shipped_python_file_names_the_note`, `test_the_session_kernel_copies_are_identical_and_name_no_retired_file` | Dynamic tracked Python set; own/shipped session kernel | HOLD static code-name assertions for High boundary mapping; KEEP actual kernel equality and all real note, symlink, tracked-path, install and prune behavior. |
| `test_the_upgrade_guide_names_the_path_the_plan_line_prints` | `bootstrap/UPGRADE.md` and real upgrade output | RETIRE fixed explanatory/negative prose after evidence; KEEP real upgrade and source/output path correspondence and public diagnostic behavior. |

No tests ran and no assertion is cleared for deletion by this inventory. **Elapsed:** approximately 5 minutes. **Tokens:** unknown.

## Implementation verification -- GPT-6.1 Terra (Coordinator) -- 2026-11-09

One joined mapped run on clean committed `5dcc7a51`, Python 3.13.13, combined the six C1 reader files with the 21 metadata readers without overlap. The command was `python -m pytest -o addopts= -p no:cacheprovider -q --tb=short <27 mapped files> --quality-gate-shuffle-seed=0 --junitxml=<temporary output>`. It finished in 592.874 seconds: 2,781 passed, eight failed and two skipped; tracked pre/post states were clean. This was neither certification nor this plan's final Boundary B.

The metadata selection's wide change verification completed with 1,392 passes and one Windows-only drive-normalization skip. The six C1 files produced 1,389 passes, eight failures and one native-Windows rewrite skip. The two skipped behaviors have native evidence elsewhere; these skips are not fresh Windows passes. All eight failures are the correct-pin and descriptor-mutation controls for four packaged callers: content runner, link checker, snippet checker and portable sweep. Their fixed source-layout helper path disagrees with the accepted contract. High design `68972c2c` specifies the repair; those checks remain unpassed pending the narrow fix and retry. Do not repeat the joined selection to clear them. Exact selection, results and grouped file counts remain in the temporary `cairn-joined-c1-data-9s0abbss` output.

Collection only, on clean `55b5c333` under Python 3.13.13, took 6.840 seconds and ran no test bodies. Against the existing `6f64ddf5` measurement, cases fell from 7,750 to 7,301 (449 fewer), while distinct collected functions rose from 4,078 to 4,109 (31 more). The stance owner fell from 80 functions/490 cases to 37/119. This whole-branch interim comparison includes concurrent work and the new tooling tests; it is not per-plan attribution or completed reduction. Test Python/JSON support grew from 6,181,228 to 6,380,443 bytes and from 121,951 to 126,137 lines. Three additional replay scripts total 48,265 bytes/1,027 lines. The remaining accepted reductions are still due.

**Test-consolidation list from this run**, slowest first: case-time sums, not whole-file wall times. The integration timing target was missed; shared host activity makes these diagnostic timings unsuitable as benchmarks. Carry these measurements into the existing board list at its next serialization point; no new work item is needed.

| Test owner under `bootstrap/tests/` | Case-time sum |
|---|---:|
| `test_upgrade.py` | 103.1 s |
| `test_upgrade_edit_check_runs_no_project_programs.py` | 85.1 s |
| `test_intents_tool.py` | 68.3 s |
| `test_upgrade_module_additions.py` | 63.5 s |
| `test_security_check.py` | 61.8 s |
| `test_security_stack.py` | 49.1 s |
| `security/test_prose_tools.py` | 38.7 s |
| `test_reference_scripts.py` | 27.7 s |
| `test_install_time_onboarding.py` | 22.5 s |
| `test_upgrade_lockfile_path_containment.py` | 13.1 s |

**Coverage:** Mapped implementation and metadata checks only; eight source-layout failures remain, wider C2 retirement and both code reviews remain open, and final Boundary B is not claimed. The new record alone selects zero test files. **Elapsed:** checks as measured above; coordination approximately 15 minutes. **Tokens:** unknown.

## C2 expanded inventory, further mixed candidates -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

This continues `fdf01fab`; the complete census remains open. These are author classifications and holds, not deletion clearance. Names are relative to `bootstrap/tests/`.

| Node | Carriers and disposition |
|---|---|
| `test_agreement_retired.py::test_no_install_source_cites_the_retired_path_or_trigger` | Dynamically walks `AGENTS.md`, `templates`, `dev/modules`, `docs` and `scripts` for its listed suffixes. RETIRE fixed retired-reference prose only after listing and independently mutating every applicable carrier. HOLD code/format token consumers for boundary mapping; KEEP actual install manifest and living-state checks. |
| `test_security_verification.py::TestTheHighRiskDesignationChannels::test_the_high_risk_designation_survives_on_two_tamper_evident_channels` | Own/shipped security-verification doctrine, dispatcher source, and real installed copies. RETIRE fixed designation prose only after exact proof and a defensible split. KEEP byte parity, real install and integrity tamper detection; HOLD the mixed security boundary for High. Neighboring customized-slot residual and public install-output tests exercise actual behavior and remain KEEP. |
| `test_gate_preflight.py::TestAuthorizationPackage::test_the_retired_no_handoff_artifact_claim_cannot_return` | `bootstrap/tests/_gate_preflight.py` and its real `check` and `stage2` help output. HOLD source-wording versus public disclosure split for High; KEEP truthful public diagnostics and actual authorization behavior. |
| `test_documentation_plan_module.py::TestMergedIntoBlocks::{test_module_names_three_blocks_by_target_and_slot,test_each_block_references_documentation_plan}` | `templates/modules/default-on/documentation-plan.md`. RETIRE fixed human-facing block-heading/link-label wording only after proof; KEEP actual slot markers, destinations and valid links. |

The High holds group unresolved code-name, docstring/public-disclosure and security-ceremony boundaries already named at `d9be7a53`, `fdf01fab` and here. They do not defer accepted scope. The three test files outside `bootstrap/tests` exercise example greeting/scientific behavior and measurement AST attestation; KEEP them. The three other `test_*.py` paths are executable tools, not test owners. No tests ran. **Elapsed:** approximately 6 minutes. **Tokens:** unknown.

## C2 expanded inventory, preflight and board-guide hybrids -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

This continues `f707c8c8`; the full census remains open and no assertion is cleared for deletion. Names are relative to `bootstrap/tests/`.

| Nodes | Carriers and disposition |
|---|---|
| `test_scaffold.py::TestInstallCore::test_installed_templates_carry_security_preflight_questions` | Own and shipped proposal/plan templates and real installed templates. RETIRE fixed question, gate-phrase and stale-wording assertions only after each applicable carrier mutation. KEEP the real install, proposal sub-block byte parity, actual plan/source correspondence and any consumed schema/slot markers. |
| `test_board_json_contract.py::TestGuideAndOutputAgree::{test_guide_opening_section_is_plain_prose_and_defines_terms,test_guide_field_tables_and_standing_phrases_match_output_and_baseline}` | `docs/build-a-board-view.md`, baseline JSON and real board output. RETIRE fixed introduction, wording and placement assertions after exact carrier evidence. KEEP the emitted and baseline field/type comparisons, actual JSON schema, and real board behavior. |

This classification adds no waiver of C2 or Security Review. No tests ran. **Elapsed:** approximately 3 minutes. **Tokens:** unknown.

## C2 D/Q source-carrier proof batch -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On frozen commit `d9be7a5308985abd5475e73fe42c2d5fbec895af`, 23 targeted
baseline/control cases passed in Python 3.13.13. Fifty-three separate committed
scratch mutations then exercised the D/Q wording pins: 26 forbidden examples
in each of four dimension files; all 11 dimension-obligation removals and the
scientific-check cell; both internal upgrade examples removed and both
External examples reintroduced; each of four README obligations removed and
rewritten to its accepted equivalent; all 33 forbidden examples in each of 15
Q carriers; all seven descriptive-obligation removals; forbidden wording in
each onboarding source/copy pair while keeping that pair equal; and the SVG
title wording changed in both title and description. Every exact adverse owner
node failed, with the expected complete reporter output. The four README
alternative rewording probes passed the positive owner node.

SVG mutations were valid XML. The fixed-title mutation preserved
`aria-labelledby` and the description/title prefix relation; its exact title
node failed on the accepted fixed phrase while the geometry node passed. The
SVG negative-wording carrier mutation produced `NOT COMPARED` plus complete
raw output; its exact wording node failed while accessibility and geometry
nodes passed. Paired onboarding mutations kept source/copy equality and failed
only at the distinct forbidden-wording assertion. Empty-carrier and existing
pattern/example controls were included in the 23 baseline cases. No canonical
source or test files changed, and no pins are cleared by this evidence.

Receipts, including 53 report and exact-node outputs, are at
`/private/tmp/cairn-prose-DQ-results/`; runner:
`/private/tmp/cairn-prose-DQ-run.py`. Two wrapper-only classification mistakes
are preserved as `.attempt1.*`: one required a quiet-pass node name not printed
by pytest; the other expected an unrelated string in the SVG raw span. Both
probes were rerun with corrected checks. Scratch clone reset clean to the
frozen base.

**Coverage:** Covered the listed D/Q carriers and exact positive, negative,
example, README alternate-wording and paired-copy assertions only. Did not run
G/Z preset or exemption walks, alter canonical tests or sources, retire pins,
run a full suite, or conduct code or Security Review. **Elapsed:**
approximately 25 minutes. **Tokens:** unknown.

## C1 source-layout failure closure -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

The eight loader failures in the joined `5dcc7a51` result are closed by the
fixed source/helper layout repair in `b00cee1b`; the exact host and native
targeted checks are recorded in the Safe-Git plan's `fixed helper layouts`
verification entry. The 27-file selection was not repeated. The previously
missing `SECURITY.md` root is now represented by committed `scripts/prose_roots.txt`;
commit `924a74e3` uses the official one-path finalizer to update only its lock
hash from `sha256:23c73839a0a3f13a5496aadfddce72e07419aadbd0e89044c473b22327257566`
to `sha256:8aec45a64a697c9493ed765e057b1823e0ceed6f14f0c6f3561bcb9050347bc0`.
Its base hash and other fields remain unchanged. A read-only audit found all
35 verbatim destinations match their recorded hashes. The generic shipped root
list and scanner policy were not changed. This closes only the named C1
implementation mismatch; the wider functional-prose work, final Boundary B,
and usual and Security Reviews remain outstanding. **Elapsed:** unknown;
**tokens:** unknown.

## C2 D/Q follow-ups and G carrier proof -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On frozen base `d9be7a5308985abd5475e73fe42c2d5fbec895af`, three narrow
D/Q probes close the remaining assertions identified by the reader: removal
of `required(not External) is a violation` from the upgrade guide failed only
its exact guide node; synchronized rewording of the SVG reviewer clause in
`<title>` and `<desc>` failed the fixed title assertion while preserving valid
XML, `aria-labelledby`, the description/title prefix and geometry; and a
second `**Complexity**` row retaining the scientific-check phrase failed the
exact row-count assertion. All three reports are complete. Receipts are
`/private/tmp/cairn-prose-DQ-results/054.{report,pytest}.txt`, `055...` and
`056...`.

The current G helper enumerates five files; the exact sorted list and its
SHA-256 `816d1522f916f7a6f4d86be67bddaf9cfcb13b1139988924671d1a7ddd7e9855`
are at `/private/tmp/cairn-prose-GZ-results/preset-files.txt`. Fifteen
focused baseline controls passed. Each carrier then received its own scratch
commit containing all 19 forbidden examples and both historic literal
sentences. Every report showed the complete added text, all 21 labels were
present, and that carrier's exact preset node failed. Reports are in
`/private/tmp/cairn-prose-GZ-results/`; runner:
`/private/tmp/cairn-prose-G-run.py`.

Z remains previously cleared: at the historical owner base `d5436fe5`, the
helper's exact 144-file set (131 Markdown, 4 YAML, 9 SVG) matches
`/private/tmp/cairn-c2-search-a-committed-members.txt` (SHA-256
`d6d0c1f45541c2461786e4c3160c84277ba86b0fb65c442eb64e944b310084f4`). Its
existing transcript has 143 owner failures and the one explicit
`docs/methodology/lifecycle-contract.md` exemption pass. Medium cleared that
walk at `d6595191`; the instrument was retired at `c50dbb84`. I did not replay
this cleared scope or reopen its formatter history.

No canonical prose or tests changed, and this record clears no additional
pins. **Coverage:** Read the three follow-up outputs, the five G reports, the
frozen G roster, and the already-cleared Z transcript and reader disposition.
No full suite, code review or Security Review ran. **Elapsed:** approximately
15 minutes. **Tokens:** unknown.

## C2 D/Q and G fresh reader -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

1. **Should it happen?** Yes for the exact wording parts below: all named carriers have readable mutation reports and their matching owner failures, including the three follow-ups.
2. **Best alternative.** Split hybrids and retain real accessibility, equality, schema and install checks. The fixed prose and its instruments are within accepted retirement.
3. **What would show it wrong?** A missing carrier, incomplete report or failed retained behavior would keep that part open; inspect the final split and run mapped checks.

**Eligible**, relative to `bootstrap/tests/test_review_stance_in_shipped_files.py`, all parameters: `test_dimensions_omit_the_old_wording`, `test_dimensions_forbidden_patterns_recognize_their_examples`, `test_dimensions_page_carries_the_obligation`, `test_the_complexity_cell_still_names_the_scientific_check`, `test_the_upgrade_guides_plan_pass_examples_are_not_external`, and `test_putting_an_external_example_back_in_the_upgrade_guide_is_reported`; the three README obligation and instrument nodes (`test_readme_explains_the_review_contract`, `test_removing_a_readme_review_rule_is_detected`, `test_equivalent_readme_wording_preserves_the_rule`); `test_descriptive_page_omits_the_old_wording`, `test_descriptive_forbidden_patterns_recognize_their_examples`, `test_descriptive_page_carries_the_obligation`, and `test_an_empty_carrier_satisfies_no_obligation_pattern` once their retired instrument consumers are removed. In `test_an_installed_onboarding_copy_equals_its_page`, retire only the forbidden-wording assertion; keep both actual equalities and the drift control. In `test_the_review_figure_keeps_an_accessible_conclusion`, retire only the two fixed title phrases; keep XML parsing, `aria-labelledby`, title/description relation and the geometry node.

Also eligible: `test_a_preset_names_no_review_tier_anyone_fills` for all five enumerated files, plus its pure controls `test_the_preset_glob_holds_every_shipped_preset`, `test_each_retired_literal_matches_its_historic_sentence`, `test_putting_a_retired_sentence_back_in_a_preset_is_reported`, and `test_a_correctly_worded_sentence_is_not_flagged`. Preserve real preset/install behavior, machine tokens, placeholders, slot order and other consumers. Remove shared helpers only after checking references.

**Coverage:** Read `f658d801`, `0c81477d`, all 56 D/Q report and node outputs and all five G report/node outputs. Each aggregated D failure lists all 26 labels and each Q failure all 33; the corresponding reports show each insertion, including complete SVG raw output. Each G failure lists all 21 labels and reports their insertions. The row-count mutation shows the selector's failure; no tools, scripts or scaffold consumer was found. Did not rerun owner tests, replay previously cleared Z, or conduct code or Security Review. This exceeds the target to identify exact splits. **Elapsed:** approximately 15 minutes. **Tokens:** unknown.

## C2 expanded inventory, installed plan line and carrier control -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

This continues `27f34128` and `f8f63d9c`; the full owner census remains open. No additional assertion is cleared here.

| Node | Carriers and disposition |
|---|---|
| `bootstrap/tests/test_scaffold.py::TestInstallCore::test_installed_templates_carry_plan_review_line` | Real installed proposal and plan templates from their shipped core sources. RETIRE the fixed security-cap and criteria-prompt phrases only after each applicable source mutation and report. KEEP the real install, source/output correspondence and parsed `Plan review` field. |
| `bootstrap/tests/test_review_stance_in_shipped_files.py::test_carrier_forbidden_patterns_recognize_their_examples` | Its `_PROBE_INVENTORY_CARRIERS` tuple contains 13 explicit sources. RETIRE the forbidden-pattern instrument only after its D/Q/G consumers are removed. HOLD the separate probe-inventory portion: the earlier vocabulary transcript shows the probe-only mutation in the four AGENTS/loop carriers, not all 13. Establish the remaining applicable carriers and reports before deleting it. |
| `bootstrap/tests/test_review_stance_in_shipped_files.py::{test_the_by_default_pin_ignores_case_and_wrapping,test_a_sentence_saying_no_tool_reads_the_line_is_not_flagged,test_adding_required_external_to_a_carrier_is_reported}` | AGENTS/loop carriers as parametrized. These are controls of the forbidden-pattern instrument: RETIRE once its actual D/Q/G consumers have been removed and remaining references checked. |

Preserve real installs, parsed fields, source parity, the protected drain pin and all still-live instrument consumers. No tests ran. **Elapsed:** approximately 4 minutes. **Tokens:** unknown.

## C2 expanded inventory, upgrade headings -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

`bootstrap/tests/test_upgrade.py::TestTemplateGatingSafety::{test_core_template_keeps_operational_sections,test_solo_keeps_all_brightlines_without_contributor_file,test_multi_keeps_brightlines_and_installs_contributor_file}` reads the five fixed `_BRIGHTLINE_HEADINGS` in `templates/core/AGENTS.md` and, for the latter two nodes, real solo and collaborative installs. RETIRE fixed heading-presence wording only after each applicable source/installed carrier mutation and reader evidence. KEEP real installs, contributor selection, integrity verification, conditional/slot behavior and source/output correspondence. HOLD the `Lifecycle and records` heading until its actual consumers are mapped: `tools/session.py` emits a section reference. The separate contributor-selection node tests real selection and remains KEEP.

This is a conditional author disposition, not deletion clearance. The wider owner census remains open. No tests ran. **Elapsed:** approximately 4 minutes. **Tokens:** unknown.

## C2 expanded inventory, skill description boundary -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

`bootstrap/tests/test_skill_contract.py::test_no_dead_alias_prose` reads `_skill_files()`: at `df99d1bd` its exact set is `templates/skills/session-start/SKILL.md` and `templates/skills/session-end/SKILL.md`. RETIRE the fixed `Friendly alias` absence pin only after separate source mutations and reports for both carriers and the C2 reader answer. No deletion is cleared here.

`test_skill_contract.py::test_skill_contract` combines actual frontmatter/name and `disable-model-invocation` contracts, path pointers, a body-size constraint, and description wording intended to prevent harness auto-triggering. KEEP the actual metadata and invocation behavior. HOLD description wording for the grouped runtime-consumer/public-disclosure mapping; do not assume it is inert text. `test_session_end_plumbs_arguments` remains KEEP. The wider census remains open. No tests ran. **Elapsed:** approximately 3 minutes. **Tokens:** unknown.

## C2 expanded inventory, verification-script explanation -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

`bootstrap/tests/test_verify_ref.py::test_the_workspace_sterility_contract_is_stated` asserts two explanatory strings in `bootstrap/container/verify-ref.sh`. HOLD their split for the grouped High code/public-disclosure boundary and demonstrate raw reporter coverage before any prose retirement. The neighboring tests of actual fetch integrity options, executable ordering, signature/refusal behavior and workspace isolation remain KEEP. This is not deletion clearance; the wider owner census remains open. No tests ran. **Elapsed:** approximately 2 minutes. **Tokens:** unknown.

## C2 expanded inventory, matrix description boundary -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

`bootstrap/tests/test_skills_matrix.py::test_anti_semantic_description_backs_non_native_suppression` tests `manual` and `not a conversational helper` in the same two shipped skill descriptions listed at `b25ff4bc`, conditional on actual vendor-target suppression settings. HOLD this hybrid with the same grouped High runtime-consumer mapping; KEEP actual suppression configuration, generated matrix equality, target levels and privacy checks. No deletion is cleared here. The wider census remains open. No tests ran. **Elapsed:** approximately 2 minutes. **Tokens:** unknown.

## C2 expanded inventory, contributing and stub hybrids -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

`bootstrap/tests/test_scaffold.py::TestOptionalContributing::test_small_multi_install_writes_contributing` asserts a literal `AGENTS.md` reference in the real installed `CONTRIBUTING.md` from `templates/optional/CONTRIBUTING.md`. RETIRE only the fixed reference wording after its C2 source mutation and actual reference-consumer mapping; KEEP real selection/install, valid links and source/output correspondence.

`bootstrap/tests/test_model_selection_stub.py::TestStubExampleNamesAFamilyNotAVersion::test_example_and_placeholder_row` reads the shipped mapping stub: RETIRE the fixed “Name the model family, never a version” comment only after source coverage and mutation evidence. KEEP the actual example and placeholder row shape and mapping schema. These are conditional dispositions, not deletion clearance. The wider census remains open. No tests ran. **Elapsed:** approximately 3 minutes. **Tokens:** unknown.

## C2 expanded inventory, installed mapping seed -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

`bootstrap/tests/test_onboarding_seed_roster.py::TestModelMappingWaitingSeed::test_seed_renders_and_board_lists_it` checks two fixed model-guidance sentences in real collaborative and legacy installs, sourced from their onboarding templates. RETIRE only those fixed sentences after independent per-source mutations and reports. KEEP the actual Waiting line, lockfile, live board output, real installs and source/output correspondence; the other seed-gating nodes exercise actual conditional routing and remain KEEP unless separately split. This is not deletion clearance. The wider owner census remains open. No tests ran. **Elapsed:** approximately 3 minutes. **Tokens:** unknown.

## C2 expanded owner static audit -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

On committed `df99d1bd2d2dea2861166a82106bec67fb4e10df`, I statically inspected the 33 original or previously identified owner files in `/private/tmp/cairn-census-identified-df99.txt` (SHA-256 `6b96659b8212a9bc9341e48004b737cbe5c4ea315c757bd48acf29f449ddb23d`) and the separate 55-file set `/private/tmp/cairn-census-extra-terra-B.txt` (SHA-256 `da607c895fbf87dcbb89a2f55c3a0fc75e357aac13ee2598cc726157658df759`). I examined test assertions, source readers and ambiguous wrappers, using the existing node/carrier dispositions above for the 33; their named High holds and all per-carrier mutation obligations remain open.

Four B-set files have mixed candidates: `test_onboarding_seed_roster.py` at `bd46078e`, `test_reanchor_driver_disclosures.py` and `test_verify_integrity.py` at `d9be7a53`, and the routing-table node below. The other 51 B-set files exercise real code and synthetic fixtures, install/upgrade and parity, schema/tokens, public output, privacy or security behavior; those checks remain KEEP, with no negative-file mutation obligation. Examples include actual quickstart counts compared with a live install, parsed status diagrams compared with the live vocabulary, copy-paste profile grammar, live slot routing, and public recovery and security diagnostics. This is a finite source audit, not a guarantee about arbitrary metaprogramming or a code/Security Review.

`bootstrap/tests/test_session_writes_contained.py::test_the_routing_table_notes_state_the_row_rule` reads `_doc` from `templates/skills/_data/vendor_targets.yml` and `.agents/skills/_data/vendor_targets.yml`. RETIRE the two fixed explanatory phrase assertions only after exact raw-format reporter coverage and separate carrier mutation evidence; HOLD any runtime disclosure boundary until mapped. KEEP the real byte equality, routing schema and executable containment tests.

The other assigned 50-file audit is separate and remains open until its own result. No tests ran and no new assertion is cleared for deletion by this record. **Elapsed:** approximately 35 minutes across search and source inspection. **Tokens:** unknown.

## C2 remaining A50 owner inventory -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

Static author inventory at `df99d1bd2d2dea2861166a82106bec67fb4e10df`. The 50 assigned paths are listed below relative to `bootstrap/tests/`; the coordination inventory is `/private/tmp/cairn-census-extra-terra-A.txt` (SHA-256 `212d2fb2f45be808d6b5697c77fccda31806aceb9de7513a024a982923ca23ae`). The temporary per-file dispositions are in `/private/tmp/cairn-census-extra-terra-A-results.txt` (SHA-256 `0c1094105c099b26f076f07feaba8ab18b51d8dd9a55edd0735e6ecd04f3d74e`). They are coordination aids, not retained evidence or a mutation ledger.

- contract: `test_cairn_prefix_links.py`, `test_release_members_contract.py`, `test_test_tiers.py`.
- integration: `test_check_cairn_counts.py`, `test_claim_check_allow_config.py`, `test_deleted_tracked_markdown.py`, `test_evolution_infer.py`, `test_gauge.py`, `test_link_check_exclusions.py`, `test_meter.py`, `test_prune_tools.py`, `test_quality_gate_redundancy.py`, `test_verify_stems.py`.
- security: `test_check_release_publication.py`, `test_code_map.py`, `test_git_interpreter_binding_portable.py`, `test_git_read.py`, `test_prose_tools.py`.
- root: `test_api_access_security.py`, `test_ast_attest.py`, `test_broad_run_guard.py`, `test_ceremony_review_report.py`, `test_check_cairn_content.py`, `test_claim_check_module.py`, `test_config_module.py`, `test_content_scan.py`, `test_core_dev_folders.py`, `test_default_security_stance.py`, `test_doc_drift_tools.py`, `test_drift_surfacing.py`, `test_engine_copy_fallback_contained.py`, `test_facade_loader_cleanup.py`, `test_finalize_retired_living_state.py`, `test_first_session_report.py`, `test_fork_advisory.py`, `test_gate_manifest.py`, `test_gate_reanchor.py`, `test_gate_transition.py`, `test_generated_output_scan.py`, `test_hardening.py`, `test_install_module.py`, `test_install_report_slots.py`, `test_intents_tool.py`, `test_issue_capture_bootstrap.py`, `test_loader_identity.py`, `test_lockfile_module.py`, `test_lockfile_provenance.py`, `test_loop_fidelity_gate.py`, `test_manifest.py`, `test_module_merge.py`.

| Node | Read carriers and disposition |
|---|---|
| `security/test_code_map.py::test_installed_copy_is_identical_and_runs` | Real installed `dev/architecture_review.md`, from `templates/modules/team-gated/architecture_review_template.md`. RETIRE candidate human-guidance checks for five third-level headings and literal `regular-file reading`, `terminal`, and `Adequate practice`, subject to exact C2 carrier coverage, separate mutations and reader evidence. HOLD `Legacy:`, `New:`, `Mixed:`, and `## Release assessment` pending record/schema consumer judgment. KEEP real install, script parity, non-clobber and actual CLI execution. The installer mapping and human module guide reference the rubric; a tracked-source search did not find a parser of these phrases. |
| `test_intents_tool.py::TestIntentParentHelp::test_parent_help_matches_source_and_installed_entrypoint` | Actual source and installed `--help`, from `tools/_intent/cli.py` and `templates/modules/team-gated/_intent/cli.py`. HOLD the three literal phrases for High judgment on public disclosure; KEEP real execution and truthful opt-in, warning and blocking semantics. |

**Grouped KEEP:** Other assertions in this set exercise real links and directives, installed bytes and placeholders, source selection, parser and record schemas, executable ceremonies, public diagnostics, scanner behavior, filesystem/Git security, measurement and actual installer workflows. For example, the release-member test runs the extracted documented shell sequence, the slot-report test compares real supplier structure, and the gate-manifest AGENTS quotation is an unconsumed docstring while the test exercises integrity HOLD. The two named hybrids retain their behavioral checks. This is an engineering static census, not a claim of formal absence under arbitrary dynamic code. No tests, mutations, retirements, code review or Security Review ran; C2 proof and its remaining holds still apply. **Elapsed:** unknown. **Tokens:** unknown.

## C2 census completion and vendor-table correction -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

The finite source census at `df99d1bd2d2dea2861166a82106bec67fb4e10df` is complete: the 33 identified owners and B55 at `ada59ba2`, plus A50 at `27ae0d09`, cover the 138 `bootstrap/tests/test_*.py` paths. The six other whole-tree filename matches were classified at `f707c8c8`. This static audit does not claim absence under arbitrary dynamic code. The per-node RETIRE candidates, retained behavior, and grouped High holds in those records remain operative; the census is not proof, review or deletion clearance.

**Correction to `ada59ba2`:** `test_the_routing_table_notes_state_the_row_rule` reads `_doc` from the shipped `templates/skills/_data/vendor_targets.yml` after byte-comparing it with `.agents/skills/_data/vendor_targets.yml`; the latter is an equality carrier, not a second `_doc` reader. To reach the phrase assertion without masking it at equality, mutate both copies identically and report both; retain a separate equality/drift witness. Runtime disclosure mapping and raw-format C2 evidence remain due. No tests ran. **Elapsed:** approximately 3 minutes. **Tokens:** unknown.

## C2 grouped consumer mapping -- GPT-6.1 Sol (Strategy, High) -- 2026-11-09

The named English assertions are wording pins even when people or models read
the text. Retire those predicates after the existing C2 proof; preserve actual
software contracts and truthful public guidance. This resolves the grouped
holds, not their carrier/mutation evidence, and does not clear a review cap.
Read committed census records through `5932d159`, current source `83403b35`,
and the original census base `df99d1bd2d2dea2861166a82106bec67fb4e10df`.

**Docstrings and public disclosures (`d9be7a53`, `600fafe6`, `17040814`).**
RETIRE the two checker residual phrases, content runner's `bare hostile URL`,
board's symlink sentence, closure function's negative membership phrase,
session module's dry-run explanation, and probe function's three explanatory
strings. The checker, board and session have explicit argparse descriptions;
the closure and probe function docstrings have no executable consumer found.
Their actual checker/scanner, symlink, closure, dry-run and key-handling nodes
remain KEEP. The probe's `/dev/tty` mention is explanation, not an executed
path at that assertion. In `test_the_hint_and_the_guide_no_longer_offer_history_as_enough`,
RETIRE the old-English absence predicate; KEEP actual recovery/integrity and
public diagnostic behavior. Do not remove or rewrite any disclosure here.

For `_gate_preflight`, argparse really uses the module docstring, and intent's
parent help really exposes its subparser summary. Nevertheless the retired
handoff phrases and three intent summary phrases are not parsed formats.
RETIRE those fixed source/help predicates. KEEP successful real `check` and
`stage2` help, actual authorization-package/flag/refusal tests, and source versus
installed intent help correspondence. In existing nodes, compare live help
with its current source/parser description using whitespace normalization,
and compare source/installed results; do not add a frozen replacement sentence
or a semantic grader. Truthfulness remains a review obligation backed by the
actual opt-in/conflict and authorization behavior tests, not an inference
that help parity proves its claims true.

**Designation, rubric, shell explanation and vendor notes.** In the high-risk
designation node at `f707c8c8`, RETIRE source/installed `DESIGNATION_FLAT`
presence. KEEP doctrine equality, real install and integrity failure on each
recorded channel. Make that existing tamper witness alter actual recorded
bytes without depending on `high-risk` remaining in canonical prose. This
does not remove the security designation or its obligations. In the architecture
rubric at `27ae0d09`, `Legacy:`, `New:`, `Mixed:` and `Release assessment` have
no parser found in the installer, code-map tool or module readers: RETIRE
alongside the other inventoried wording/heading pins. KEEP real installed
rubric-to-template correspondence, non-clobber and code-map behavior. RETIRE
`verify-ref.sh`'s `not candidate-controlled`/`multi-valued` explanation pins;
KEEP its executable sterility, fetch, ordering and signature/refusal checks.
`vendor_targets.yml` loaders select `targets`, not `_doc`; RETIRE its two
English predicates, KEEP paired equality, target fields/enums and routing
containment. The paired mutation correction at `5932d159` still applies.

**Skills and heading reference.** RETIRE `manual` and `not a conversational
helper` predicates in the two skill tests at `b25ff4bc`/`966abd9b`; KEEP nonempty
description/name metadata, actual suppression settings, `$ARGUMENTS`, invocation
flags and reflection-only CLI backstop. Official [OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills)
describes model selection by description and a separate implicit-invocation
policy; [Claude's skill documentation](https://code.claude.com/docs/en/skills)
describes a frontmatter invocation control. Neither establishes those English
substrings as parsed suppression tokens. This is no new harness guarantee or
configuration migration; existing claimed/unverified levels stay truthful.
The session status advisory emits `AGENTS.md > Lifecycle and records` but
parses its own status vocabulary, not that heading. RETIRE the fixed heading
pin; KEEP the real advisory and reference-to-existing-section correspondence,
checking its emitted section against the current source/installed AGENTS
headings rather than hard-coding the English title.

**Code-name guards.** `next-session.md`/`NEXT_SESSION` and retired trigger names
inside executable strings, identifiers or configuration are implementation
guards, not prose wording, so KEEP those portions of the next-session and
agreement nodes. Comments/docstrings and human guidance in their broad scans
are C2 wording candidates, not an exception to retirement. Split the syntax or
configuration portion from prose before removal; do not delete a whole mixed
scan. The next-session code guards are imperfect evidence of no auto-execution:
before replacing them, use the real session entry point with an inert hostile
note/retired-file marker and show it is not executed or consumed, with a positive
tripwire proving reachability. That is the owning promise's behavior evidence;
this C2 judgment alone does not justify retiring its internal code guard.
Preserve installer/living-state and kernel-byte parity checks.

**Header/skeleton refinements (`83403b35`).** `tools/board.py`'s
`_HEADER_FIELD_RE`, `_required_reviews`, `_next_review_state` and Decision-tier
reader require field names and recognized values, not exact whole menu lines.
`_required_reviews` accepts flexible whitespace/case; review-record detection
finds Obligation/Tier independently. RETIRE canonical spacing, whole-line
rendering and `Obligation < Tier` ordering predicates in the three named
stance-owner nodes. KEEP field labels, valid alternative values, placeholders
and actual required security-obligation presence. Check extracted offered
alternatives against the existing board consumers, and preserve existing slot
markers/order required by the merge grammar; that slot contract is distinct
from the unconsumed Obligation/Tier display order. No new parser framework is
needed. C2 proof applies to each retired predicate, including both templates.

**Coverage:** Traced the named assertion bodies, local loaders/parsers, public
help producers, status advisory, rubric mapping and the cited official harness
documentation (OpenAI Docs skill used). No exhaustive dynamic-consumer absence,
harness execution, runtime tests, mutants, suite, code review or Security Review
is claimed. This is an in-contract grouped classification; no rule, source
policy, public diagnostic or metadata changed. **Elapsed:** approximately
15 minutes; **tokens:** unknown.

## C2 D/Q/G retirement and probe-carrier verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commit `83403b359baf95cd243616464c67915c9e2c66a2` applies the exact
D/Q/G wording clearances from `f8f63d9c` and `215e2e34` to
`bootstrap/tests/test_review_stance_in_shipped_files.py`. It removes the
cleared dimensions, README/descriptive-page, and preset fixed-wording tests and
their instruments, plus pure forbidden-vocabulary controls whose consumers are
gone. The probe-inventory portion of
`test_carrier_forbidden_patterns_recognize_their_examples` remains live for all
13 enumerated carriers. The two installed onboarding equalities and their drift
control remain; the figure retains XML parsing, accessibility relation and
geometry. Template fields/order/placeholders, model/session parity, roster
slots/fidelity/drift remain.

On a clean archive of `83403b3`, the owner collected 40 cases. The committed
parent `55b5c333` had 119 cases in Root's earlier owner collection; this batch
therefore removes 79 owner cases. AST counts are 37 test function definitions
at `55b5c333` and 16 at `83403b3`. This owner-local delta is not an integrated
net-volume claim; new tests and dynamic parameterization must be counted in
Root's joined comparison.

With canonical Python 3.13.13, 22 focused retained cases passed and 18 were
deselected (0.10 seconds). The selection covers the surviving carrier guard,
team markers, template values and obligation ordering/placeholders, copy
parity, roster fidelity and drift, SVG accessibility/geometry, and onboarding
equality/drift.

On nine separate committed copies frozen at `83403b3`, I appended
`Code review includes a falsification ledger.` to each remaining proposal,
plan, methodology, strategy and dual-review-module carrier. The source-side
`templates/modules/team-gated/prose_diff.py` completed for each and reported
that exact file as added; the live `test_carrier_forbidden_patterns_recognize_their_examples`
then failed on that carrier's unmutated-text assertion. Clone commits are
`f3018772b948` (shipped proposal), `8fb7668e649e` (own proposal),
`bbfbafcdc6d3` (shipped plan), `31e4a2f8da91` (own plan), `d0a9c637d0bf`
(methodology plans), `82956fceec7a` (methodology dual-review),
`f63c227c8d12` (plain-language strategy), `16d60e6576ff` (shipped
module), and `f0fba3d67d86` (own module). Full reporter and exact-node outputs
are at `/private/tmp/c2-probe-inventory-83403b.txt`; the nine committed copies
remain under `/private/tmp/c2-probe-inventory-83403b/01..09`. The earlier four
carrier proofs are recorded at `f658d801` and `0c81477d`. The final probe-guard
retirement awaits the fresh Medium reader verdict on these reports.

**Coverage:** Applied only reader-cleared D/Q/G assertions and removed private
helpers after their consumers disappeared. Did not remove the 13-carrier
probe-inventory guard, run the broad owner suite or full suite, measure the
integrated net, or conduct code or Security Review. Remaining C2 inventory and
grouped High boundaries are still open. **Elapsed:** approximately 35 minutes.
**Tokens:** unknown.

## C2 probe-inventory fresh reader -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

1. **Should it happen?** Yes: the nine complete reports show the exact adverse sentence on each remaining carrier and the live guard fails naming that carrier; the earlier four cover the rest of its 13-file tuple.
2. **Best alternative.** Retire this wording guard and its now-unused instrument helpers, while retaining the separate slots, fields, parity, roster, SVG and placeholder behavior.
3. **What would show it wrong?** A missing carrier, incomplete report or removed live helper consumer would leave the affected part open; inspect the final deletion and run its mapped checks.

**Eligible:** retire `bootstrap/tests/test_review_stance_in_shipped_files.py::test_carrier_forbidden_patterns_recognize_their_examples` and its private probe-inventory tuple, pattern and predicate. Remove `_normalize` only after confirming no remaining references; retain shared readers used by the structural checks. The Maintainer-retained drain pin remains.

**Coverage:** Read `e7729b15`, all nine reporter and exact-node outputs at `/private/tmp/c2-probe-inventory-83403b.txt`, the current 13-member tuple and assertions, and the earlier four probe entries at `/private/tmp/cairn-c2-vocabulary-mutants.tsv`. The prior four are recorded in `795dfc8b` under “C2 additional carrier and held-assertion outputs”; the reference to `f658d801` and `0c81477d` for those four in `e7729b15` is incorrect. The predicate and normalization match the earlier owner. Did not rerun owner tests or conduct code or Security Review. **Elapsed:** approximately 6 minutes. **Tokens:** unknown.

## C2 final probe-guard retirement verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commit `48d787452773f5bc92ee975e15cac4c44f7bb912` applies the exact
13-carrier guard clearance from fresh Medium reader `6baf7217` in
`bootstrap/tests/test_review_stance_in_shipped_files.py`. It removes the guard,
its private carrier tuple, regex, predicate and normalization helper, plus
carrier constants made unused by that removal. The module summary now describes
only retained behavior/schema checks. Template fields and placeholders, roster
slots/fidelity/drift, copy parity, SVG accessibility/geometry, onboarding
copy equality/drift, and real install semantics remain.

On a clean archive of `48d7874`, the owner collected 39 cases, down one from
40 at `83403b3`. Twenty-one focused retained cases passed and 18 were
deselected under Python 3.13.13 (0.08 seconds). This local count does not
measure the integrated net. Prior four-carrier probe evidence is at
`795dfc8b`; the nine remaining-carrier reports and exact guard failures are at
`/private/tmp/c2-probe-inventory-83403b.txt`, read by `6baf7217`.

**Coverage:** Removed only the reader-cleared wording guard and unused private
machinery. No broad owner suite, full suite, integrated volume comparison, code
review or Security Review ran. Remaining C2 inventory and grouped High
boundaries are open. **Elapsed:** approximately 10 minutes. **Tokens:** unknown.

## C2 header menu and review-field probes -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

At High classification `cd5e8a98`, the remaining exact spacing/whole-menu and
`Obligation`/`Tier` order predicates were held for C2 proof; no source assertion
was removed. On separate committed scratch copies frozen at `de360629`, four
proposal-menu mutations in each proposal template and three plan-menu/order
mutations in each plan template changed only delimiter/padding spacing or the
two field-line order. The actual recognized menu values were preserved. Each
of the 13 captured cases produced source-side `prose_diff.py` CHANGED output
and failed its exact existing parameterized owner node. Existing
`tools.board` consumers accepted the extracted values: `_required_reviews`
recognized both Review and Plan review alternatives, `_next_review_state`
recognized the review Tier values, `_next_decision` accepted the Decision tier
values, and the swapped plan review fields still identified the Security
Review. No enum registry, test framework, or canonical assertion was added.

The first shipped-proposal Review-menu attempt is preserved at scratch commit
`40c344e63ac56e9bd088fe651f2c1fa644060e24`. Its reporter output was
regenerated only and is at `/private/tmp/c2-header-proofs-first-report.txt`.
Before a fixture-only `_next_decision` control failed on a malformed synthetic
`**ACCEPTED.**` record, the runner had already asserted the exact owner-node
return was nonzero and its output named the expected node and `AssertionError`;
the raw pytest output was not saved. The corrected Board control passed on that
same mutant. The later complete transcript is
`/private/tmp/c2-header-proofs-de360-corrected.txt`; its first entry repeats
that shipped-proposal mutation and is not counted as a distinct receipt. An
earlier invalid mutant that changed the recognized value `Security Review` to
double internal spacing was excluded because the real parser correctly rejects
that altered value. Only delimiter/padding spacing mutants count here.

**Coverage:** Mapped offered values to the existing `tools/board.py` parser
functions and exercised the exact held assertion nodes on the frozen template
mutations. No header or skeleton assertion was deleted or weakened; no full
suite, integrated volume measurement, code review or Security Review ran. A
fresh reader must assess this evidence before any header retirement. **Elapsed:**
approximately 35 minutes. **Tokens:** unknown.

## C2 comprehension-floor and scope-reduction carrier probes -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On clean committed copies frozen at `48d787452773f5bc92ee975e15cac4c44f7bb912`,
10 comprehension-floor cases were individually falsified: eight required-rule
patterns across both AGENTS carriers and two moves that left the phrase outside
the Review section. For the scope-reduction owner, all 73 pure wording
predicates among the 79 `_SURFACES` cases were individually removed across the
14 listed files; four per-entry disposition template cases and the canonical
heading-adjacency assertion were also falsified. Each case had a separate
committed copy, complete `scripts/prose_diff.py` CHANGED or ADDED output, and an
exact owner-node assertion failure. Receipts are in
`/private/tmp/c2-expand-low-results.jsonl`; the canonical adjacency report and
node output are from scratch commit `78ffb60ce55983c61f9d2671c208acd4d69578c0`.

Two single-alternative removals on `dev/agent_collaboration.md` survived because
the same owner regex had another matching formulation. Those attempts are
retained in the receipts; independent retries removing all alternatives failed
the exact owner nodes. Six scope cases remain held: the four `**Scope delta**`
declaration markers, the three-value enum assertion in the canonical doctrine,
and the declaration marker in `docs/methodology/proposals.md`. They overlap the
accepted public declaration/grammar KEEP boundary and are not cleared by these
prose-only probes. No test or production assertion was removed or changed.

The healthy accepted-floor parameter passed 1/1 under canonical Python 3.13.13
in 0.79 seconds and executed both profile installs. A separate canonical 3.13.13
two-profile run confirmed the installed `## Scope delta` section is byte-identical
to `templates/core/dev/plans/_template.md` for `solo-greenfield` and
`high-rigor-legacy`. A preliminary manual run with shell Python failed
interpreter binding; the same comparison passed with the canonical interpreter.

**Coverage:** Probed only the two named owners and their listed carriers;
preserved declaration values, parser/schema behavior, and install machinery.
Did not mutate the six held public-marker/enum cases, remove assertions, run
broader owner families or the full suite, measure integrated net test volume, or
conduct code review or Security Review. A fresh Medium reader must assess these
receipts before any retirement. **Elapsed:** approximately 45 minutes.
**Tokens:** unknown.

## C2 header and expanded carrier receipt review -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

1. **Should it happen?** Yes, for the exact wording predicates below: the committed owners at `5ed25dbd` and `48d78745`, the reports and exact-node failures support reporter coverage of those changes; `cd5e8a98` separates display formatting from actual board consumers.
2. **Best alternative.** Retire only those predicates, retaining recognized fields, values, placeholders and merge slots, declaration grammar, real links and install correspondence. Human consumption of prose does not itself make its exact wording a machine contract.
3. **What would show it wrong?** A real consumer relying on a retired format, a missing predicate receipt, or a retained behavior lost in the deletion would reopen that part; inspect the actual deletion and run its mapped checks.

**Eligible:** In the three stance-owner nodes, the canonical menu spacing/whole-line and Obligation-before-Tier checks for both proposal and plan templates, subject to the retained boundaries in `cd5e8a98`. The corrected transcript contains 14 complete cases; its first duplicates the original first case and is counted once. The original raw pytest failure was lost: its regenerated report and runner-control-flow statement are not raw output; the corrected transcript independently captures that same mutation's failure and board controls. Exclude the invalid internal-value-spacing mutation.

In `bootstrap/tests/contract/test_comprehension_floor.py`, the eight `_REQUIRED` carrier cases and two Review-section wording-placement cases are eligible; preserve the actual rationale reference and link validity. In `bootstrap/tests/test_scope_reduction_trap.py`, the 73 pure wording `_SURFACES` cases and four per-entry disposition wording cases are eligible. The two surviving single-alternative mutations are not failures; their all-alternative retries supply the relevant failures. Preserve the installed scope section correspondence and actual declaration behavior.

**Hold:** The six `_SURFACES` declaration/enum cases (four template markers, canonical enum, and proposals doctrine marker) and separate declaration grammar tests remain. Hold canonical heading adjacency pending its actual reporter and exact-node output: scratch commit `78ffb60ce55983c61f9d2671c208acd4d69578c0` exists, but those outputs are not in the cited JSONL; the committed account alone does not provide the complete receipt. This is a receipt review, not authority to change rules or a code review.

**Coverage:** Read committed records `5ed25dbd`, `ddb39967`, classification `cd5e8a98`, owner assertions at their cited bases, both header reports, and `/private/tmp/c2-expand-low-results.jsonl` (including duplicate placement runs and two survivor entries); inspected the adjacency scratch commit and runner. The receipt distinctions and exact hold make this pass longer than the 300-word target. Did not rerun implementation checks, recreate missing outputs, examine every dynamic consumer, review a deletion, or conduct Security Review. **Elapsed:** approximately 12 minutes. **Tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09 -- C2 wording retirement

On `26f0933555ecf687e6584d05c495b5a8435f97cf`, canonical Python 3.13.13 in a clean archive collected 50 tests from the two retained owners; the deleted comprehension-floor owner had 10 cases at the committed review base. Together, the three owners collected 138 at `8816052f`, so this commit removes 88 collected cases locally. It deletes four test definitions and adds one independent install/source correspondence definition; no checks were packed. The focused retained selection passed 17/17, covering both real profile installs, recognized proposal/plan values, all six declaration markers, held heading adjacency, and the five grammar cases. `scripts/check_cairn.py AGENTS.md templates/core/AGENTS.md` passed both preserved rationale-reference checks. The archive was clean; the shared worktree was not clean because an unrelated proposal edit was present and left untouched.

The deletion is limited to Medium-cleared wording predicates. Production prose, rationale references, parsed values and fields, placeholders, declaration grammar, marker cases, heading adjacency, onboarding and SVG behavior remain. The new install/source check preserves both-profile correspondence without pinning wording. No full suite, integrated net-volume comparison, code review, or Security Review ran. **Elapsed:** approximately 4 minutes. **Tokens:** unknown. The removal reduces redundant prose-only checks while keeping the retained behavior checks independently readable; the final integrated test-volume result remains for the coordinator to measure.

## Implementation evidence -- GPT-6 Luna (Implementation, Low) -- 2026-11-09 -- retry and small-fix carriers

On clean base ed9c21606e26d0abb0005426496676f417a249f3, I made 11 separate committed carrier mutants and ran the existing scripts/prose_diff.py reporter plus the exact owning test node in each copy. Four retry mutants cover removing each local-only phrase from Cairn's AGENTS.md and inserting each phrase into templates/core/AGENTS.md; the two removals reported REMOVED and the two insertions ADDED. Seven small-fix mutants cover the three lifecycle phrases, two installed AGENTS phrases, the issue-capture pointer and the defer-OK negative assertion; the six removals reported CHANGED and the insertion ADDED. Every owning node failed once on its adverse carrier.

Mutant commits: 3d59cf8a, 61bb8f03, c1beafe2, 6198f833, cad81762, 64a832b2, c2d3bf35, adb9a2b4, 8dd7e366, 87e7ae02, 0ed9e0ac. Full reports and pytest outputs are retained under /private/tmp/c2-mixed-missing-proof-ed9c2160/<case>-output/. The initial generator stopped after the first successful retry case because a wrapped phrase did not match a raw substring; that output is retained, and the corrected whitespace-aware matcher completed the remaining cases. No canonical source pin has yet been removed from these two owners.

**Coverage:** Retained actual install/source behavior for the later split; did not run full owner files, change protected manifests, or conduct code or Security Review. **Elapsed:** approximately 15 minutes. **Tokens:** unknown.

## C2 mixed-owner receipt review -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

**Reviewed commit:** `c608776a`. **Verdict:** PARTIAL.

1. **Should it happen?** The 11 named wording predicates can be separated from
   actual install behavior: each adverse carrier has reporter output and its
   owner-node failure in `/private/tmp/c2-mixed-missing-proof-ed9c2160/`.
2. **Best alternative.** Retire those exact pins, retaining actual installs,
   source/output correspondence, slot placement, and uncovered assertions;
   the existing `f6eede2c` read already clears the 58 readable-work cases.
3. **What would show it wrong?** A missing or unreadable reporter result, lost
   installed correspondence, or a retained behavior failing after the split
   defeats that part; inspect the deletion and run mapped checks later.

**Eligible:** In `contract/test_writing_rules_ship.py`, the two Cairn-local
retry marker presence assertions and their two shipped-marker exclusions, on
exactly the four evidenced carrier mutations. Preserve generic adopter retry
behavior and real installation/source correspondence. In
`contract/test_stewardship_rules_ship.py`, the three lifecycle phrase pins,
two installed AGENTS phrase pins, issue-capture pointer phrase pin, and
`defer-OK` negative pin have individual receipts. Preserve the real install,
source/output and actual applicability checks when splitting the hybrid node.
The first report says CHANGED, not REMOVED; it still shows the marker loss.

**Hold:** The seven scientific carrier wording predicates pending identification
of their matching reporter receipts in this read; retain scientific source-pair
correspondence and slot placement regardless. No blanket retirement of other
assertions, installed-output consumers or grammar is authorized by this read.

**Coverage:** Read `c608776a`, all 11 report and exact-node outputs, the two
original owners at `ed9c2160`, the scientific owner and prior 58-case reader
record. No replay, product diff, test run, code review or Security Review.
**Elapsed:** about six minutes. **Tokens:** unknown.

## C2 scientific receipt disposition -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

The seven rows in `/private/tmp/cairn-c2-scientific-guidance-mutants.tsv` match
`test_the_check_guidance_reaches_every_copy_and_promise_site` at `d6595191`:
both proposal carriers, both plan carriers and all three named promise sites
each have a CHANGED report and a failed owner-node result. The seven source
wording pins are eligible for the C2 split. Preserve corresponding source-copy
comparisons and the slot-placement protection; this receipt does not validate
installer behavior or waive later review. No mutant was replayed. **Elapsed:**
about two minutes. **Tokens:** unknown.

## C2 remaining scope wording disposition -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

<!-- claim-check-allow: bootstrap/tests/contract/test_comprehension_floor.py -->

The exact-path exemption preserves historical references to the wording-only
test file removed at `26f09335`; its original bytes remain available in Git.
It does not restore that file or exempt other paths.

1. **Should these retire?** Yes: High mapping `6d9df5a5` found no live executable
   consumer of these scope markers, vocabulary or heading adjacency. The twelve
   actual reports show the changes that their exact old owner cases reject;
   these are instructional-prose pins, not parser contracts.
2. **Best alternative.** Retain the real two-profile installation/source
   equality check and actual board field/value consumers. Keeping these prose
   patterns would preserve the editing burden the accepted proposal removes
   -- current scope owner and the board's review-field readers.
3. **What would show this wrong?** A live consumer of a removed literal or a
   missing report would reopen that predicate. Changed-input tests through that
   consumer, rather than another source-string assertion, would establish it.

**Disposition:** RETIRE all six remaining `_SURFACES` cases, all five
`_GRAMMAR_TEMPLATES` cases and
`test_the_canonical_section_exists_and_sits_beside_its_mirror` in the scope
owner. This supersedes the earlier declaration/grammar and adjacency holds.
The five marker changes, one vocabulary change, five grammar changes and
adjacency insertion each have complete reporter output and their exact
single-case assertion failure in
`/private/tmp/c2-scope-missing-proof-c608776a/`. The reports identify the actual
changed carrier and text; the adjacency output explicitly shows the intervening
heading. Independent-copy commits are the twelve cited by the producer, based
on `c608776a`. No production text is changed by this disposition.

**Coverage:** Read all twelve report/test outputs, the committed owner and
High's executable census with its positive board-consumer control. No tests or
mutants rerun, installation proof added, code review or Security Review
performed. Real source-copy equality and later required assurance remain.
**Elapsed:** about five minutes. **Tokens:** unknown.

## C2 ordinary carrier proof batch -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On six separate committed copies frozen at `23091ca13f15a3302b570aa68a2d5ca893150309`, the existing `templates/modules/team-gated/prose_diff.py` reported six carrier mutations across four files: the model-stub comment as `RAW CHANGED` (YAML also reports `NOT COMPARED` because its structured extractor does not support YAML), the optional CONTRIBUTING reference as three `CHANGED` spans, and each of the two guidance sentences removed separately from both onboarding templates as `CHANGED`. The exact C2 owner nodes failed for each mutation. The two onboarding cases also failed their existing sibling fixed-sentence node. The model-stub mutation additionally failed `TestFamilyNotVersionReachesEverySite::test_all_model_mapping_sites`, revealing a second consumer of the same fixed phrase; that assertion remains outside this batch's proposed retirement pending reader assessment.

Scratch copies and complete report/pytest outputs are at `/private/tmp/c2-small-proof-23091ca1/`. The first attempt stopped before mutation because the model-stub phrase crosses a YAML comment line; a retry matched the exact wrapped bytes. The initial onboarding attempt likewise stopped before mutation because its phrase crosses a line; each corrected attempt used the exact source bytes. No canonical test or prose file changed. Actual model example and placeholder row, optional-template selection/install, onboarding Waiting line, lockfile, and board output assertions remain.

**Coverage:** Probed only the six named adverse mutations and their exact owner nodes; reported the additional existing phrase consumer. Did not change assertions, run broad owner files, mutate other carriers, or conduct code or Security Review. A grouped independent reader must decide whether the two overlapping assertion nodes are both eligible before either is removed. **Elapsed:** about 12 minutes. **Tokens:** unknown.

## C2 skill-description carrier proof batch -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On six separate committed copies frozen at `63aaf188840aaaf7573d043a7cbb3ada37f29f0a`, the existing source-side `templates/modules/team-gated/prose_diff.py` reported complete `CHANGED` spans for each mutation in the two skill files listed by the C2 inventory. Inserting `Friendly alias` separately into session-start and session-end failed the exact `test_no_dead_alias_prose[skill]` case. Removing `manual` and `not a conversational helper`, one phrase at a time from each description, failed the matching `test_skill_contract[skill]` and `test_anti_semantic_description_backs_non_native_suppression` nodes. Full outputs are at `/private/tmp/c2-skill-proof-63aaf188/`.

The mutations preserved each description's nonempty value, skill name, `disable-model-invocation: true`, body, pointers and arguments. No canonical test or functional-prose file changed; no actual invocation or CLI behavior was tested or altered.

**Coverage:** Probed the two listed carriers and six phrase mutations only. No assertion removal, broad owner run, full suite, code review or Security Review. The grouped reader must assess this wording batch alongside the preceding ordinary-carrier proof before any retirement. **Elapsed:** about 8 minutes. **Tokens:** unknown.

## C2 grouped receipt disposition -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

**Read:** ordinary receipt `63aaf188`, skill receipt `efb471df`, owner
predicates and High mappings `cd5e8a98`/`6d9df5a5`, and the reporter and
exact-node outputs in both named scratch directories. **Disposition:** Clear
only the following wording predicates for the planned C2 retirement, retaining
their other assertions and later required review and verification:

- The optional CONTRIBUTING `AGENTS.md` presence predicate: its three
  references changed together, the reporter showed all three spans, and the
  installed-content owner failed. Keep optional selection and actual install.
- Both guidance-sentence predicates in each of the collaborative-team and
  high-rigor-legacy onboarding carriers, including the overlapping installed
  and source checks. Each separate mutation produced `CHANGED` and failed both
  matching nodes. Keep the Waiting line, lockfile and board behavior.
- The `Friendly alias` absence predicate for each session skill and the two
  description wording predicates (`manual`, `not a conversational helper`)
  in both skill-contract and matrix nodes. Each of six separate mutations
  produced `CHANGED` and failed its matching node or nodes. Preserve actual
  names, frontmatter, nonempty descriptions, suppression flags, pointers,
  invocation flags and real CLI/runtime behavior; no native harness behavior
  is established by these receipts.

**Hold:** The model-stub YAML wording predicate and its all-sites counterpart.
The reporter gives `RAW CHANGED` but explicitly says `NOT COMPARED` for YAML;
both owner nodes fail on the same phrase. This is not a complete structured
report or disposition of the other all-sites carriers. A named disposition and
applicable C2 coverage are needed before retirement; the example and placeholder
row remain. No source or assertion has been removed by this receipt.

**Coverage:** Read the named output files and actual predicates; did not rerun
mutants or tests, inspect other carriers, or conduct code or Security Review.
This grouped reading is not final implementation clearance. **Elapsed:** about
five minutes. **Tokens:** unknown.

## C2 ordinary and skill pin retirement verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commit `0e65e126472db04f41d13f3bd30d0e0a8d90c5b6` applies only reader `ae6d0df0`'s clearances across five test files. It removes the single CONTRIBUTING reference assertion, four source/installed onboarding sentence assertions, two skill-description predicates in two consumers, and the two-case Friendly-alias absence test. The actual install and selection checks, Waiting line, board output and lockfile, skill names and frontmatter, invocation flags, pointer and argument checks, matrix equality, allowed values, non-native-mode presence, and privacy checks remain. The stub YAML comment and its all-sites check remain held.

In clean copies under Python 3.13.13, the five-file collection changed from 186 cases at parent `839aad7a` to 184 at `0e65e126`; AST test-function definitions changed from 161 to 160. No checks were packed. The focused retained selection passed 11/11 in 0.77 seconds, covering CONTRIBUTING installation, both onboarding presets and installed-seed sibling checks, skill contract and argument routing, and compatibility-matrix generation and values. `tools/test_tiers.py for` these paths maps seven test files; only the focused nodes ran here, leaving the full mapped-file run for the required later integration boundary.

**Coverage:** Ran the mapped exact retained nodes and clean collect-only comparison. Did not run all seven mapped files, the full suite, Boundary B, code review or Security Review. No production prose or runtime code changed. **Elapsed:** about 8 minutes. **Tokens:** unknown.

## C2 project-general guidance carrier proof -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On seven separate committed copies frozen at `dac1611c289c28c20c971ef57556d5c9472564d7`, I changed only `templates/core/AGENTS.md` for the existing `test_installed_operational_rule_is_project_general` predicate. The three fixed positive phrases were removed one at a time; each of the four project-specific forbidden terms was inserted separately into visible prose. The existing source-side reporter produced three complete `CHANGED` spans and four `ADDED` spans; the exact owner node failed once for each case. Reports and test output are at `/private/tmp/c2-verification-guidance-proofs-dac1611c/`. Initial forbidden-term attempts placed terms in HTML comments and are retained but excluded; the four retries place each term in visible text.

The tested mutation set follows the per-node inventory: three project-general guidance assertions and four absence predicates. No production or canonical test bytes changed. Actual verification fields, `bounded`/`wide` values, commands, record schema and quality-gate dispatch were not mutated.

**Coverage:** Probed one shipped carrier and this one existing node only. No retirement, broad owner run, full suite, code review or Security Review. This batch requires grouped fresh reader disposition before any predicate removal. **Elapsed:** about 12 minutes. **Tokens:** unknown.

## C2 verification-script explanation carrier proof -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On two separate committed copies frozen at `dac1611c289c28c20c971ef57556d5c9472564d7`, I changed one explanatory phrase at a time in `bootstrap/container/verify-ref.sh`: `not candidate-controlled` and `multi-valued`. The exact existing `test_the_workspace_sterility_contract_is_stated` node failed in each copy. The source-side reporter showed a complete `RAW CHANGED` span at the corresponding line and also stated `NOT COMPARED` because shell structured extraction is unsupported. Captures are at `/private/tmp/c2-verify-ref-proof-dac1611c/`; the script was not executed.

**Coverage:** Probed the two named prose phrases and their exact negative owner. Did not change fetch, executable, signature, refusal or workspace-isolation behavior, edit assertions, run the owner suite, or conduct code or Security Review. These raw spans need grouped fresh-reader assessment before retirement. **Elapsed:** about 4 minutes. **Tokens:** unknown.

## C2 verification-boundary guidance proof batch -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On two separate copies frozen at `858bc6a7c71005b1dd70b7914b414b620278f991`, I changed `Use wide for a contract or trust-ceremony surface` to `bounded` independently in own and shipped `AGENTS.md`. Each existing source reporter showed a complete `CHANGED` unit span, and `test_both_operational_surfaces_separate_change_checks_from_tree_certification` failed at that exact carrier. The own-file mutation also failed the separate `test_change_verification_guard_detects_removed_wide_fence`. On two more copies, changing the optional EARS prompt from `SHALL` to `MAY` in each plan template produced complete `CHANGED` spans and failed the exact `test_plan_templates_offer_optional_observable_criteria_prompts` node.

Five further copies changed `unit checks` to `local checks`, one carrier per copy, across own `AGENTS.md`, adopter `AGENTS.md`, `docs/methodology/plans.md`, and both plan templates. Each report showed the complete changed unit and the existing `test_scoped_defaults_reach_core_templates_and_optional_module` failed at the changed path. Its unmutated frozen copy passed. An initial attempt to match the doctrine phrase without preserving its source newline failed before mutation; the corrected retry changed `Unit\nchecks` and passed the same reporter and owner-node checks. All captures and exact test outputs are under `/private/tmp/c2-operational-guard-proof-858bc6a7/`, `/private/tmp/c2-operational-own-proof-858bc6a7/`, `/private/tmp/c2-criteria-self-proof-858bc6a7/`, `/private/tmp/c2-criteria-adopter-proof-858bc6a7/`, and `/private/tmp/c2-scoped-unit-*-858bc6a7/`.

These receipts cover only the named prose predicates and five carriers in the scoped-category subcheck. No canonical tests or production prose changed. The real module-copy equality, quality-gate dispatch/default selection, verification schema and actual mode values were not mutated; other predicates in the verification-boundary inventory remain unassessed here.

**Coverage:** Ran the exact existing nodes on each frozen adverse copy and the scoped-category node once on its unmutated copy. Did not retire assertions, run the full owner file or suite, test installed behavior, or conduct code or Security Review. The whole batch needs fresh reader disposition before retirement. **Elapsed:** about 12 minutes. **Tokens:** unknown.

## C2 scoped-check categories, remaining carrier predicates -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Completing the scoped-category subcheck recorded above, I changed each remaining literal phrase independently in all five carriers named by the node tuple: own and adopter `AGENTS.md`, `docs/methodology/plans.md`, and both plan templates. `contract checks` became `interface checks`, `integration checks` became `connected checks`, and `small workflow` became `short exercise`, for 15 separate committed mutations frozen at `858bc6a7c71005b1dd70b7914b414b620278f991`. Each existing source report contains the complete `CHANGED` unit and each exact `test_scoped_defaults_reach_core_templates_and_optional_module` run failed at the mutated carrier. Captures are in `/private/tmp/c2-scoped-{self,adopter,doctrine,selfplan,adopterplan}-{contract-checks,integration-checks,small-workflow}-858bc6a7/`.

The first own/adopter integration-phrase match attempts stopped before mutation because the source line break separates `integration` from `checks`; the corrected retries replaced the exact `integration\nchecks` bytes. The plan-doctrine retry and all other mutations preserved source line breaks. No canonical tests or product prose changed. Together with the five `unit checks` mutations above, the 20 category/carrier assertions in this node's second loop now have independent adverse coverage; its broad first-loop word-presence predicates remain unassessed.

**Coverage:** Ran this exact owner node in each adverse copy; the unmutated pass is the single one recorded above. Did not edit assertions, remove any pin, run the whole owner file or suite, test installed behavior, or conduct code or Security Review. Fresh reader disposition remains required. **Elapsed:** about 12 minutes. **Tokens:** unknown.

## C2 receipt correction and disposition -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

The YAML hold in my `ae6d0df0` receipt was mistaken. This plan's existing
literal-evidence clarification permits complete RAW before/after spans for
unsupported structured formats while retaining the `NOT COMPARED` notice.
The stub report at `/private/tmp/c2-small-proof-23091ca1/` shows the complete
changed comment span and both matching owner failures. Clear the stub comment
phrase predicate in `test_example_and_placeholder_row` and the stub tuple in
`test_all_model_mapping_sites` for planned retirement. Keep the actual example,
placeholder and schema checks; this does not clear any other all-sites member.

The two `858bc6a7` shell reports show complete RAW before/after spans for
`not candidate-controlled` and `multi-valued`, each with its matching owner
failure. Clear those two explanation predicates; preserve real workspace
isolation, fetch, ordering, signature and refusal checks. `NOT COMPARED` means
structured shell extraction was unavailable, not that the literal evidence
was incomplete; no shell execution is claimed.

The seven `f1704fd2` supported-format receipts show three distinct removed
phrases and four separate visible-text forbidden-term insertions, each with a
complete structured report and matching owner failure. Clear those seven
wording predicates in `test_installed_operational_rule_is_project_general`;
retain actual verification fields, modes, commands, record schema and quality
checks. The four earlier comment-only attempts are excluded.

**Coverage:** Read the cited receipts, their exact reporter and failure outputs,
and owner predicates against the existing High classifications. No tests or
mutants rerun, other all-sites members assessed, shell executed, or code or
Security Review performed. These are scoped C2 dispositions, not final
implementation clearance. **Elapsed:** about six minutes. **Tokens:** unknown.

## C2 scoped-defaults broad-word carrier proof -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On 70 independent committed copies frozen at `858bc6a7c71005b1dd70b7914b414b620278f991`, I removed one broad word at a time (`callers`, `configuration`, `public`, `local`, `shared`, `uncertain`, or `review`) from each of the ten carriers in `test_scoped_defaults_reach_core_templates_and_optional_module`. Each source report contains the full `CHANGED` context and each observed exact owner-node run failed at the affected carrier. All reports and most output captures are in `/private/tmp/c2-scoped-broad-<carrier>-<word>-858bc6a7/`; source reports for `callers`, `configuration`, and `public` were preserved after the runs in their scratch copies. The own/adopter `callers` and own `configuration`/`local`/`shared`/`review` copies used a sequential `-retry` setup after the first clone batch failed; own `public` used a sequential retry suffix after the base hash. Two initial no-checkout scratch copies are retained but excluded. Each valid receipt was checked to use the frozen parent before testing.

These are generic substring-presence predicates; the replacements remove all occurrences of the tested word in the individual scratch carrier so the exact predicate fails. That produces several spans where a word recurs. In particular, the `local` and `review` scratch replacements also touch names or status text containing those strings; they are not evidence to change any real path, state token, parser contract or runtime behavior. No canonical test, production text or actual interface value changed. The independent module-copy equality and actual quality-gate behavior checks remain outside this adverse set.

**Coverage:** Completed all seven broad-word predicates over the node's exact ten-carrier tuple; did not mutate the separately tested four category phrases again, edit or remove any assertion, run the whole owner file or suite, or conduct code or Security Review. The complete combined receipt packet still needs a fresh reader before retirement. **Elapsed:** about 35 minutes. **Tokens:** unknown.

## C2 operational guidance wording carrier proofs -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On 16 separate copies frozen at `858bc6a7c71005b1dd70b7914b414b620278f991`, I changed eight exact entries used by `_operational_violations` in each own/adopter `AGENTS.md`: Boundary A wording, the Boundary B sentence while preserving the literal `bounded | wide` values, Boundary C wording, wide-family coverage wording, future-certification wording, change/tree-certification wording, the integration-after-review phrase, and release-ceremony wording. Each mutation produced a complete changed-unit report and the exact `test_both_operational_surfaces_separate_change_checks_from_tree_certification` node failed at the mutated carrier. The already-recorded own/adopter wide-for-contract mutations provide the ninth wording predicate and were confirmed against complete saved reports in the same two proof copies. Captures for the 16 new mutations are in `/private/tmp/c2-operational-guidance-{own,adopter}-{boundary-a,boundary-b,boundary-c,wide-families,future-cert,separate-cert,review-trigger,release-separate}-858bc6a7/`.

The additional generic `record heading` predicate in this helper was left intact because it names a live implementation-verification record heading; no adverse heading edit was made. The actual mode values stayed intact in every new mutant. No canonical test or product prose changed. The component quality-gate tests, parsed review/plan tokens, fields and actual command behavior remain outside this wording evidence.

**Coverage:** Ran the exact owner node on each of these 16 adverse copies; the unmutated base passed the same node once. Did not mutate the record heading, alter actual mode values, remove assertions, run the whole file or suite, test installed behavior, or conduct code or Security Review. This proof packet needs grouped reader disposition before retirement. **Elapsed:** about 18 minutes. **Tokens:** unknown.

## C2 project-general adopter guidance pin retirement -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commit `11fff8a17754e2ce51ad30c2b6ffd96983237995` applies Medium clearance `5993ff51` to `test_installed_operational_rule_is_project_general`: it removes the seven assertions checking three fixed positive phrases and four project-specific forbidden examples. This node had no schema parsing or command execution. Actual record fields, bounded/wide values, quality-gate dispatch/default behavior and both own/adopter operational checks remain unchanged.

On a clean copy of parent `faa391fc18014ef767a9327497faecf2ca292185`, the exact owner file collected 50 cases before and 49 after the deletion. The changed owner file passed 49/49 in 0.06 seconds under Python 3.13.13. No checks were packed; no product text or runtime code changed.

**Coverage:** Ran the whole one-file tier selection from `tools/test_tiers.py for bootstrap/tests/contract/test_verification_boundaries.py` on the clean copy. Did not run other mapped files, the full suite, Boundary B, code review or Security Review. Other verification-boundary predicates remain in the accepted C2 inventory. **Elapsed:** about 6 minutes. **Tokens:** unknown.

## C2 scientific fixture correction -- GPT-6.1 Terra (Implementation, Medium) -- 2026-11-09

After two Low fixture failures caused by a double-escaped whitespace pattern,
the one-tier-up correction completed the remaining 35 distinct mutations
sequentially. Neither failed setup wrote a carrier or ran its check. The prior
successful `p01/module` mutation was retained, not repeated. Each of the 18
phrase predicates now has a separate committed mutation in each of the two
testing-module carriers, frozen at `858bc6a7`.

Each report shows the complete changed span and each exact scientific-guidance
owner node fails at its expected missing-phrase assertion under Python
3.13.13. Reports and failures remain in the existing
`/private/tmp/c2-scientific-guidance-pNN-{module,shippedmodule}-858bc6a7/`
copies. The corrected driver is
`/private/tmp/cairn-science-fixture-medium.py`; its receipt manifest identifies
the 35 completed copies. The existing unmutated control was not rerun.

**Coverage:** Corrected the fixture and executed only these remaining
single-node adverse checks. No canonical tests or guidance changed, assertion
retired, suite run or code/Security Review performed. Grouped fresh-reader
disposition remains due before retirement. **Elapsed:** about five minutes
including diagnosis and execution. **Tokens:** unknown.

## C2 grouped verification and scientific receipt disposition -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

Read the owner predicates, High classifications and receipts `604f0547`,
`8f1356f7`, `7e8e4c9d`, `426a4d12`, `b495e2e0` and `488b4f19`. The
20 category/carrier and two optional EARS mutations show complete changed
units; I reproduced missing reports against each committed scratch parent and
head without rerunning tests. The 70 broad-word carrier mutations have changed
source and complete reports, including the corrected retries. Their author
records the expected owner failures; saved failure output is available for
part of that batch. These are evidence of wording sensitivity, not permission
to change names, statuses or machine fields touched incidentally in scratch.

The 18 operational cases cover nine wording predicates in both surfaces; the
16 newer cases each have complete reports and captured matching owner failures,
and the earlier two have complete reports and recorded failures. The 36
scientific phrase/carrier cases each have complete reports and captured owner
failures matching the corresponding phrase. Clear these named wording
predicates for planned C2 retirement, including the scientific helper's
self-mutation tied to the first phrase. Keep the implementation-verification
record heading and actual `bounded`/`wide` values, module-copy parity, CLI and
quality-gate dispatch, actual verification fields and real behavior. The
separate routine-operation and cross-component-workflow subchecks are not
covered by this receipt.

**Coverage:** Read the recorded exact-node results, captured failures and
reports, committed mutations and current owner bodies. Did not rerun tests or
mutants, assess other predicates, run a suite or perform code or Security Review.
These are scoped receipt dispositions, not final implementation clearance.
**Elapsed:** about eight minutes. **Tokens:** unknown.

## C2 cleared wording-pin retirements -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commit `d00c846a` removes only the cleared YAML-stub comment and shell
explanation assertions. The YAML example/schema and shell refusal and
`fsck.skipList` behavior checks remain. Its mapped clean-copy selection
collected 479 cases: 475 passed, with four environment-limited failures in
`test_gate_preflight.py`. Two could not resolve the scratch `refs/cairn/gate-anchor`;
two could not bind the test-owned `ssh-agent` socket (`Operation not permitted`).
Root reran only those four nodes on a clean disposable copy with the trusted
local anchor and permitted disposable sockets; all four passed in 1.51 seconds
(4.736 seconds wall). Evidence: `/private/tmp/cairn-four-environment-dd7g_8xh/`
(`result.json`, `pytest.log`, `results.xml`), Python 3.13.13. The three-file
selection was not replayed.

Commits `3a4f40cc` and `10e2b95b` remove the 20 scoped-category, 70 broad-word,
18 operational-wording, two optional EARS, and 36 scientific prose predicates
cleared by `59a8b826`. They also remove only private helpers used by those
assertions. The second commit restores the two routine-operation and
cross-component-workflow assertions across own AGENTS, shipped AGENTS and plan
doctrine because the reader explicitly held them. Module-copy equality,
record heading and actual fields, `bounded | wide` values, dispatch/default
behavior, falsification triggers and real quality checks remain.

On clean copy `10e2b95b` (Python 3.13.13), `tools/test_tiers.py for
bootstrap/tests/contract/test_verification_boundaries.py` selected that file.
It collected 49 cases before and 45 after; the changed file passed 45/45 in
0.06 seconds. No product prose or runtime code changed and no full suite ran.
The remaining routine-operation and cross-component predicates are not cleared;
they cover two phrases in each of three carriers and need their existing
grouped C2 proof and reader disposition.

**Elapsed:** about 12 minutes across the edits and focused checks. **Tokens:**
unknown. The measured reductions remove recurring text-maintenance checks while
retaining behavior and schema coverage; the four initial failures were resolved
by the narrow environment-specific rerun, without repeating the full selection.

## C2 routine-guidance carrier proofs -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

On six independent committed copies of `10e2b95b`, I removed one phrase at a
time: “Routine project operations use affected checks” and “representative
cross-component workflow” from each of own `AGENTS.md`, shipped
`templates/core/AGENTS.md`, and `docs/methodology/plans.md`. The current
`prose_diff.py` produced a complete `CHANGED` report for every carrier, and
the exact retained node
`test_routine_operations_and_cross_component_guidance_reaches_governing_surfaces`
failed for each mutation. The receipts are in
`/private/tmp/c2-routine-cross-proofs-10e2b95b/`, indexed by
`receipt-manifest.json`.

The initial receipt wrapper incorrectly expected the reporter label `RAW
CHANGED`; this UTF-8 Markdown input correctly reported `CHANGED`. The affected
report and same owner-node check were rerun from the unchanged mutant commit
with the accepted complete-change format; all six receipts above are complete.
No canonical source or test changed. Fresh grouped reader disposition remains
due before removing these two predicates.

**Elapsed:** about 4 minutes including wrapper correction. **Tokens:** unknown.

## C2 routine-guidance wording retirement -- GPT-6 Luna (Implementation, Low) -- 2026-11-09

Commit `89a13436` removes the two wording predicates across own AGENTS, shipped
AGENTS and plan doctrine, following the six-carrier disposition in
`3f0d81f6`. Actual instructions and behavior were not changed. On a clean copy
at Python 3.13.13, the focused owner file collected 44 cases and passed 44/44
in 0.07 seconds. The earlier committed owner file collected 45 cases; the net
reduction is one collected test definition. Wider integration checks and the
remaining functional-prose plan work are still due.

**Elapsed:** about 2 minutes. **Tokens:** unknown.

## C2 routine-guidance grouped disposition -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

Read the six manifest entries and complete changed-unit reports against `10e2b95b`, the exact retained owner node, and the author's recorded failures in `4f643005`. Each carrier independently substitutes equivalent English for one of the two pinned phrases, and the author reports the corresponding node failure. These receipts establish wording sensitivity across both AGENTS files and plan doctrine. Clear these two English phrase predicates for the planned retirement; retain actual machine fields, parity, commands and behavior. This does not authorize changing the underlying guidance.

Coverage: The six named receipts only; no mutant or test replay, other receipts, suite, code review or Security Review. **Elapsed:** about 4 minutes. **Tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09 -- history and scanner wording

Commit `da62fbbf` removes the cleared pure history-phrase absence test and
the `csr.__doc__` wording assertion. The scanner test retains its real
classification and scan assertions. On the clean committed copy at
`da62fbbfc98e108c3404da6ed468c0a1b034c867`, the focused retained node
`TestRunnerUrlRoleBoundary.test_bare_url_in_known_prose_is_the_named_residual`
passed (1 passed, 0.20 seconds, Python 3.13.13). The deletion removes one
collected test definition; the retained scanner case remains. The exact
pre-deletion carrier reports and owner failures were reviewed in `b0c671a5`.

No product prose, scanner behavior, verification fields or recovery path
changed. Integrity behavior nodes and broad owner checks were not rerun here;
Root will join the mapped owner checks. **Elapsed:** about 12 minutes.
**Tokens:** unknown.


## C2 grouped receipt disposition -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-09

Clear the exact history-phrase absence node in the integrity owner. Separate
committed mutations at `864cb051` insert the forbidden phrase in each actual
reader, the verifier module and upgrade guide; both complete reports show the
added text and both owner runs fail at that phrase predicate. These historical
sentences do not alter verification behavior or grant authority.

Clear only the `csr.__doc__` wording assertion in
`TestRunnerUrlRoleBoundary.test_bare_url_in_known_prose_is_the_named_residual`.
The complete RAW before/after span shows the equivalent wording change; the
owner reaches and passes its real scan assertions before failing the docstring
pin. Preserve that scanner behavior test and all other verification, heading,
field and copy checks.

Evidence: `/private/tmp/c2-low-cost-proof-864cb051/`, three named report/owner
pairs and the current committed predicates. **Coverage:** read the reports,
observed-failure captures and owner bodies; no checks repeated, production
text changed or whole code/Security Review conducted. This clears only these
named prose predicates. **Elapsed:** about three minutes. **Tokens:** unknown.

## C2 session-docstring receipt disposition -- GPT-6.1 Terra (Medium) -- 2026-11-09

Read the two committed carrier mutations frozen at `4c8e8b7c` and their
reporter and exact-owner outputs in
`/private/tmp/c2-session-wording-proof-4c8e8b7c/`. Mutation `8878eb14`
substitutes “supports” for “honors”; the complete changed docstring is visible
and the positive fixed-phrase assertion fails. Mutation `6504e420` adds the
old blanket phrase as a historical statement; the report shows the addition
and the negative phrase assertion fails. Both reports completed; neither
mutation changes execution.

**Disposition:** Retire exactly
`test_session_routines.py::test_module_docstring_scopes_dry_run_claim_to_session_end`.
Its sole carrier is `templates/skills/_lib/session.py`; the two predicates
are wording pins already classified by High. Preserve source/copy parity,
public help and actual dry-run behavior, including
`test_handoff_dry_run_does_not_touch_the_intent_surface`.

**Coverage:** Read both receipts and the current owner and retained behavior
witness. Did not rerun tests, change production prose, conduct code or Security
Review, or clear final change verification. **Elapsed:** approximately three
minutes. **Tokens:** unknown.

## C2 closure and board docstring disposition -- GPT-6.1 Terra (Medium) -- 2026-11-09

Read both completed reports and exact-node failures in
`/private/tmp/c2-low-docstring-packet-9ee5dada/`. Reanchor mutant `6d97e628`
adds the forbidden phrase to `scripts/reanchor_ceremony.py`; board mutant
`67dc5f85`, based on coverage-list commit `184913eb`, substitutes equivalent
wording in `tools/board.py`. Both reports show the complete changed units;
the old assertions fail only their fixed docstring predicates. The earlier
board report without root coverage is incomplete and excluded.

**Disposition:** Remove only the negative docstring assertion in
`test_reanchor_driver_disclosures.py::TestTheClosureListIsReadFromTheTemplate::test_the_launcher_template_is_a_member_and_the_docstring_agrees`
and the two docstring assertions in
`test_board_json_contract.py::TestSymlinkedSourcesAreNotRead::test_symlinked_root_or_parent_above_root_is_read_normally`.
Keep actual launcher membership and the complete real symlink-root and
parent workflow. These are the existing High-classified prose predicates;
this clears no other node or security finding.

**Coverage:** Read reports, exact failures and retained owner bodies; no
checks repeated, production prose changed, or whole code/Security Review
performed. **Elapsed:** approximately three minutes. **Tokens:** unknown.


## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09 -- exact board and closure docstring pins

Cairn's extra prose-root list now includes only `tools/board.py` for the
board carrier. Commit `184913eb` leaves the shipped root list empty and uses
the scoped finalizer to advance only the `scripts/prose_roots.txt` lock hash.
A preflight report on a disposable copy showed the list-control notice and a
complete RAW change to that hash; the reporter correctly did not compare YAML
structure. The scoped finalizer ran before I claimed `dev/.cairn/cairn-lock.yml`;
the commit hook reported that missing pre-edit claim. It changed only the one
expected root-list hash. Root inspected the committed diff and directed that it
not be rewritten. Future scoped finalizers require claiming both destination
and lock paths first.

On separate committed copies, reanchor mutant `6d97e628` added the negative
closure phrase and board mutant `67dc5f85` changed the symlink sentence, based
on the newly covered root `184913eb`. The source reporter emitted complete
RAW and typed changed spans for each. Each exact old owner assertion failed
once at its docstring predicate. The earlier board report without root
coverage was incomplete and is excluded. Medium receipt `96114544` cleared
only those three wording assertions.

Commit `14d48450` removed the reanchor negative assertion and the board
docstring-existence and fixed-sentence assertions. It retains the true launcher
membership assertion and the board's complete real symlink-root and parent
workflows. These two hybrid test functions remain, so this change removes no
collected definitions or cases; it removes only the cleared text predicates.
On a clean committed Python 3.13.13 copy, the retained membership and symlink
workflow nodes passed: 2 passed in 0.14 seconds. Results are in
`/private/tmp/c2-docstring-retained-14d48450-results/`.

**Coverage:** No production behavior changed. No full suite, Boundary B, code
review or Security Review ran in this step. Other accepted C2 pins and final
wide verification remain due. **Elapsed:** approximately 20 minutes, including
coverage correction and focused checks. **Tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-09 -- joined check repairs

Commit `d6fc68cd` updates both exact-replacer report pins to the reviewed
`prose_diff.py` digest, finalizes only the `scripts/exact_replace.py` lock row,
mirrors the instrumented Git reader at the installed and template destinations
in the content fixture, and aligns the fixture's POSIX source guard to 646.
On the clean isolated worktree at
`/private/tmp/cairn-joined-check-d6fc68cd` (source SHA
`d6fc68cd08c2bef63992b4f9264357008e8d5aa9`), canonical Python 3.13.13 ran
`python -m pytest -q` over the 19 exact previously failing
`bootstrap/tests/security/test_prose_tools.py` nodes, the 3 failed
`TestContentComposition` nodes, and
`test_committed_fixture_connects_real_record_and_join_entrypoints` in
`bootstrap/tests/test_security_check.py`: 23 passed in 36.00 seconds, with 3
deprecation warnings. The exact selection was the failed-node set from
`/private/tmp/cairn-docs-final-c__6r1bb/batch-1.xml`; the pytest exec session
was 50759. Pre- and post-run worktree status was clean. No separate stdout file
was saved. This targeted retry follows the initial shell glob error, which
started no tests. Full owners, Boundary B, and review were not run here; root
joins the mapped final checks. **Elapsed:** approximately 12 minutes.
**Tokens:** unknown.

## Test-volume checkpoint -- GPT-6.1 Terra (Medium) -- 2026-11-09

Clean committed `99590d7e`, Python 3.13.13: `python -m pytest --collect-only
-q bootstrap/tests` collected 7,161 cases and 4,107 distinct functions. Against
`6f64ddf5`'s recorded 7,750 cases/4,078 functions, that is 589 fewer executable
cases (7.6%) and 29 more functions. This includes new tool-test coverage and
concurrent branch work; it is not per-plan attribution or a runtime result.

Tracked Python/JSON test support grew from 155 files/6,181,228 bytes/121,951
lines to 161 files/6,417,189 bytes/127,410 lines. Fewer cases are measured;
fewer functions, less support code and runtime savings are not demonstrated.
The clean collection and support census took 7.42 seconds, ran no test bodies
and left the copy clean. Reproducible collection output and measurement data:
`/private/tmp/cairn-test-volume-jgqoihxp/{collection.log,result.json}`.
**Elapsed:** 7.42 seconds measured plus approximately two minutes to reconcile
and record. **Tokens:** unknown. Remaining accepted C2 work and final reviews
are unchanged.

## C2 preflight, help and rubric disposition -- GPT-6.1 Terra (Medium) -- 2026-11-10

Read the six complete reports and exact-owner failures supplied by Low:
`5603c08e`, `11685672`, `5989a606`, `f99c5a29`, `067af9d8` and `795fb5dd`.
The three preflight mutations independently reach the source scan, check help
and stage2 help; the last two expose lost parameter guidance. The intent
mutations separately reach source and installed help, retaining the three
pinned policy meanings in different words while dropping another explanatory
clause. The rubric mutation changes regular-file specificity and encoding
scope. These differences are visible to a reader; production text is unchanged.
Reports and failures are in the supplied `c2-rubric-help-docstring` temporary
copies. Exclude the passing parent-docstring attempt, malformed help attempt
and source-intent attempt made before its persistent root coverage existed.

**Disposition:** Retire the complete
`TestAuthorizationPackage::test_the_retired_no_handoff_artifact_claim_cannot_return`
wording node in `test_gate_preflight.py`. Retire only the three English
predicates in `TestIntentParentHelp::test_parent_help_matches_source_and_installed_entrypoint`,
keeping both real source/installed CLI success checks. In
`security/test_code_map.py::test_installed_copy_is_identical_and_runs`, retire
only `regular-file reading` and `terminal` from the phrase tuple. Keep all
mapping, parity, customization and executable behavior; remaining rubric
wording/count predicates still need their applicable proof.

**Coverage:** Read complete changed units, current predicates and exact
failures; no checks repeated, production changed, whole code/Security Review
performed, or final verification cleared. **Elapsed:** approximately five
minutes. **Tokens:** unknown.

## C2 remaining rubric disposition -- GPT-6.1 Terra (Medium) -- 2026-11-10

Read complete report `07fad49a` at
`/private/tmp/c2-rubric-compound-07fad49a/report.txt` and the exact installed
owner failure. It exposes the changed heading level and all changed table and
release-heading units. The test executes installation then fails at four
third-level headings instead of five. Inspection of the committed mutant also
confirms each remaining pinned label is absent; those later predicates did
not execute after the first failure. This is one compound same-carrier proof,
not a claim of separate runtime failures for every word.

**Disposition:** Retire the remaining heading-count and
`Legacy:`/`New:`/`Mixed:`/`Adequate practice`/`## Release assessment` predicates
in `security/test_code_map.py::test_installed_copy_is_identical_and_runs`,
consistent with the existing High classification. Preserve initial installed
rubric correspondence with the actual source template: the current call uses
empty tokens and no axes, so its text should equal that template. Keep script
mapping/verbatim/parity, non-clobber, customization and real CLI assertions.

**Coverage:** Read changed units and predicate inputs; no test rerun, production
change, whole code/Security Review or final verification. **Elapsed:**
approximately three minutes. **Tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-10

Commit `4f5ada5e` removes the Medium-cleared obsolete handoff wording test,
three English parent-help predicates, and the rubric's heading-count and
English-label pins. The help node still requires successful source and
installed `--help` execution. The installed rubric workflow now compares the
initial installed bytes with the actual template bytes, then retains
customization, non-clobber, installation, and real CLI checks. No product text,
parsed fields, installer mappings, or runtime behavior changed.

On clean committed copy `4f5ada5e`, canonical Python 3.13.13 ran the retained
source/installed help node and installed code-map workflow: 2 passed in 0.48
seconds. The root-list change was checked separately on clean commit `ea466be1`:
the prose-tool and content-scan files had 278 passes and one native-Windows
skip (66.753 seconds wall time). The exact results are under
`/private/tmp/c2-retained-4f5ada5e-result/` and
`/private/tmp/c2-intent-root-validation-ea466be1-clean/`.

**Coverage:** The deleted pure wording node was not rerun. No full owner-file
selection, full suite, final Boundary B, integrated test-volume collection,
code review, or Security Review ran here. Remaining accepted C2 work and final
verification remain due; no final-B claim is made. **Elapsed:** approximately eight minutes.
**Tokens:** unknown.

## C2 designation and customization disposition -- GPT-6.1 Terra (Medium) -- 2026-11-10

Read complete reports and exact failures for `ab755475`, `8ccc43cc`,
`09081be5` and `b5082451`. Separate source, twin and dispatcher mutations
preserve the risk meaning with different words; the last report exposes an
accurate additional sentence outside the customized slot, which nevertheless
fails the global phrase-absence predicate. The reused template mutations also
fail the neighbor's installed-channel phrase checks. These are wording pins;
no production designation or risk obligation is changing.

**Disposition:** Retire `DESIGNATION_FLAT` predicates and the dead constant
in the two inventoried `TestTheHighRiskDesignationChannels` nodes. Preserve
source/twin equality, real installation and initial integrity. Replace source
and installed presence checks with actual template/output correspondence.
Make the existing tamper witness test each recorded destination independently
using a nonempty appended test comment, exact restoration and clean control.
In the customized-slot witness, compare the actual slot to the fixture-owned
customized marker/text; preserve status, warning, side-file, standing-command
and fidelity checks. Both other installed artifacts must still equal their
sources and pass integrity. This retains behavior without canonical wording.

**Coverage:** Read reports and old predicate/behavior bodies; no tests
repeated, production changed, whole code/Security Review or final verification
cleared. **Elapsed:** approximately five minutes. **Tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-10

Commits `faef0556` and `bcf69600` remove the fixed designation string from
the two high-risk channel tests while retaining doctrine-twin equality, actual
installation, source/output correspondence, independent nonempty byte tamper
and restore checks, and the verifier's clean result. The customized-slot node
keeps its status, no-warning, no-side-file, command-absence and fidelity checks,
and now checks its exact fixture-owned slot body. After the additional module
is selected, its doctrine and dispatcher outputs remain byte-equal to their
sources. The `DESIGNATION_FLAT` constant is removed.

Three separate carrier mutants on `cb9ce37a` changed the doctrine source,
its self-hosted twin, and the dispatcher comment. Complete report/failure pairs
are in `/private/tmp/c2-risk-designation-proof-cb9ce37a-doctrine-source/`,
`/private/tmp/c2-risk-designation-proof-cb9ce37a-doctrine-twin/`, and
`/private/tmp/c2-risk-designation-proof-cb9ce37a-dispatcher/`. A core-AGENTS
insertion outside the customized slot demonstrates the neighboring global-
absence false positive at
`/private/tmp/c2-risk-designation-proof-cb9ce37a-core-negative/`. Reusing the
source and dispatcher mutants, the neighbor's installed-presence
predicates failed at the matching channel in
`/private/tmp/c2-risk-designation-neighbor-proof-cb9ce37a-doctrine-source/` and
`/private/tmp/c2-risk-designation-neighbor-proof-cb9ce37a-dispatcher/`. Medium
disposition `e0712209` cleared the exact replacements.

On clean `faef0556`, Python 3.13.13 ran both retained nodes: 1 passed and
1 failed in 1.44 seconds. The tamper node passed; the customized-slot node
exposed a misplaced post-customization `verify==0` expectation. The first
corrected copy moved that check before the
slot edit but read module outputs before the test selected the module; failure
`FileNotFoundError` is retained at
`/private/tmp/c2-designation-retained-a3b6139d-result/pytest.log`. Commit
`bcf69600` keeps clean verification on the initial claim-check-only install;
the existing later selection installs the module before dynamic channel
correspondence is asserted. On clean `bcf69600`, the affected neighbor node
passed 1/1 in 0.92 seconds (1.502 seconds wall); the first node was unchanged
and its pass from the clean `faef0556` run is reused. Final result:
`/private/tmp/c2-designation-neighbor-final-bcf69600-result/`.

**Coverage:** No full owner file, suite, final Boundary B, integrated volume
collection, code review or Security Review ran. Remaining C2 inventory and final
verification remain due; no final-B claim is made. **Elapsed:** approximately
15 minutes including two focused fixture corrections. **Tokens:** unknown.

## C2 preflight and heading consumer split -- GPT-6.1 Sol (Strategy, High) -- 2026-11-10

Read committed `299767a2`, the C2 inventories and existing grouped High
consumer mapping. This supplies execution detail, not deletion evidence or
implementation/Security Review clearance.

**Preflight: RETIRE** S1–S5 titles, gate/stale phrases, plan marker/sentence
presence and English extractor delimiters after the required per-carrier C2
proof and fresh disposition. **KEEP** real installation and proposal-region
byte parity. Modify existing `_extract_security_preflight`, adding no helper:
start after the existing `examples-smoke-home` end marker and stop at the
next generic H3 (`### `). Require both boundaries and nonempty content;
compare the entire region, including the prospective paragraph formerly
excluded. No executable consumer of the English delimiters was found in
installer, tools, scripts or shipped session code.

For both proposal and plan, compare real installed output with the complete
current shipped template passed through existing `substitute_tokens(raw,
tokens)`: this node calls `install_core` without axes, so no conditional
stripping applies. `_CORE_MAPPINGS` in `bootstrap/_scaffold/config.py` maps
both source templates to their installed destinations. Preserve supplied-token
checks. Do not compare whole own/shipped plan files: deliberate module slots
and project-specific verification text differ. The original plan predicates
were independent fixed-sentence presence checks, not a general parity contract.

**Upgrade headings: RETIRE** the five fixed `_BRIGHTLINE_HEADINGS` predicates
after their applicable source/solo/multi proofs. **KEEP** the lifecycle
reference relationship: session's `_status_advisory` actually emits an
`AGENTS.md > section` destination; its nearby comment and
`scripts/verify_stems.py` docstring do not parse headings. Extend the existing
public session-start retired/unknown-status witness in
`bootstrap/tests/test_status_vocabulary_advisory.py`: extract the destination
from the emitted advisory and resolve its section against actual own/shipped
AGENTS H2 headings, without a replacement canonical title. A stale public
target is the real uncovered fault. Preserve installs, contributor selection,
profile-neutral review-copy equality, token, conditional and integrity checks.

**Coverage:** Source classification only; no tests or mutations replayed,
production changed, earlier families reopened or review/check waived.
**Elapsed:** approximately 12 minutes. **Tokens:** unknown.
