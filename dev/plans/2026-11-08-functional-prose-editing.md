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
