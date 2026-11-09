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
