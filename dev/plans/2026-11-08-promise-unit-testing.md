# Plan: Promise-unit testing

**Source proposal**: dev/proposals/archive/2026-11-08-claude-promise-unit-testing.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-08
**In brief**: Test component promises through their public entry points and give adopters the same practical guidance.

## Build summary

Pilot promise-based tests on upgrade, independently check the protection they retain, then apply the method to the eligible families and ship the guidance and advisory report. Security-sensitive removals receive an additional review before they land. The work produces evidence for a separate release re-anchor, not the re-anchor itself.

## Source proposal

The Maintainer accepted the heavy proposal at `0e1f9ae2`, including the widened adopter capabilities. The accepted change gives up tests catching only internal-only mutants; it does not waive protection of caller-visible behavior, including hostile input and timing.

## Scope

Change Cairn's governing `AGENTS.md` Verification rule and the corresponding shipped rule, testing-discipline module, core plan template, install specification and capability row. Add the standard-library advisory tool at its team-gated source and installed `scripts/` path. Convert the protected `bootstrap/tests/test_upgrade.py` pilot and then the eligible families, including `test_gate_preflight.py`, `test_reanchor.py`, `test_repin_ceremony.py`, `test_upgrade_removes_retired_files.py`, and security families. Promise lists live in test-file docstrings. Text-pin retirement belongs to the functional-prose plan; meter and claims-tool families remain on the board pending their respective Decisions. Hostile-state injection tests remain as declared exceptions.

Reuse: `rg` for mutation and upgrade tests found existing fixtures and public upgrade tests in `bootstrap/tests/test_upgrade.py`, and mutation examples in `bootstrap/tests/test_review_sweep_ships.py`; reuse suitable fixtures and entry points rather than build a parallel harness. The existing testing-discipline paragraph and install patterns are the homes for guidance and the tool. The proposal specifies path-only AST resolution and its failure behavior; use those contracts, without importing inspected modules. A new security or trust design beyond them needs high-tier design before execution.

## Sequence

One coherent outcome has three dependent internal chunks. Estimate 3–6 focused workdays, with substantial uncertainty from family inventory, defensive-site probes and review; this is not a deadline. The installed interpreter, existing tests and source are available. The implementation coordinator arranges the available Windows VM window and stages disposable committed source copies; fresh agents provide the independent probes and required reviews.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inventory eligible families and pilot upgrade promises, retained checks and removal candidates; collect baseline counts and runtime. Convert the pilot and independently probe it. | Fresh high-tier Security Review agrees to the protected pilot removal set before removals land; independent old/new behavior-mutant check passes before C2 or C3. | Pilot tests, promise list and recorded evidence. |
| C2 | Apply the same method to each eligible family, ordered by private reach and runtime; independently inspect defensive sites for security families. | Fresh high-tier Security Review agrees to each security/high-risk removal set before it lands, and to every listed native-only node individually. | Reviewed removals and grouped evidence for the release owner. |
| C3 | After C1 passes, replace the rule, extend shipped guidance and plan prompt, and install the advisory tool. | Contract and forward tests pass. | Cairn and adopter capabilities. |

A reviewed expected AST mismatch from planned engine changes remains unpassed until the separate Maintainer-owned release baseline operation; unexpected drift and unexplained integrity failures remain implementation work. Record the human re-anchor and baseline operation as a separate named board wait with evidence, not as a plan completion condition. Archive requires all agent-owned work, reviews and checks; it grants no release authority.

## Acceptance criteria

**C1.** List upgrade's caller-visible promises, including refusals, and cover each through `scaffold.py --upgrade` or its public function. Record before/after collection, every removed node, counts and runtime. A fresh agent, without reading the tests, derives at least one behavior-changing mutant per promise and an accepting mutant per refusal from the list and `bootstrap/_scaffold/`. It runs each once against the old file from the commit before first removal and once against the new file. Any mutant caught by old and missed by new fails the pilot; restore or strengthen coverage and record the result. The retired-files test belongs to C2.

**C2.** For each eligible family, list promises, retain public-entry coverage, record counts, runtime and every removed node, and pass the same independent old/new mutant comparison. For security families the independent agent additionally derives an accepting mutant for each defensive check found in code, even if absent from the list. Treat every file guarding a security property or named high-risk surface as protected, whether or not the gate holds it. Before removal, obtain the family Security Review; require its node-by-node agreement for `NATIVE_ONLY_NODE_IDS` members and preserve a reason for each affected manifest member. Group protected removed nodes by promise with the retained check and mutant result; a node missing either is `stop` and stays. Ordinary drops are gate notes; protected drops are holds pending re-anchor. Do not remove a family that has not completed its checks.

**C3.** Both rules express the accepted promise, refactor, scaffolding, surviving-mutant, refusal and justified internal-test provisions, including hostile-state exceptions. Extend the existing testing paragraph, map each removed caller-visible fault to a retained check using behavior mutants, and include a pin-style before and the existing scientific-minimal test as after. The plan prompt asks which promise changes and which entry point checks it. A promise list is a module docstring line `Promises:` followed by at least one `- ` line. Resolve project imports by paths inside the project root outside tests, without imports; count `from m import _x` and `alias._x` for bound project modules. The advisory tool installs verbatim with its module and reports private reach and missing `Promises:` lists worst first, states that refusal and hostile-state injection tests stay, names its Python-only gap, and exits zero unless strict mode is requested. Its CLI tests cover project-module aliases and private imports, exclusions for local helpers, fixtures and dunders, missing lists, strict/non-strict exits, parse, recursion and decoding failures, escaped output, no import machinery, and out-of-root links reported without following. The scientific-minimal forward test has no private reach; five sampled upgrade tests agree with a hand count. The install test and `python bootstrap/scaffold.py --dry-run` demonstrate installation.

## Scope delta

**Scope delta**: preserved. The accepted internal-only mutant loss is explicit above; no broader fault criterion is waived. The source assigns text pins to the functional-prose work and fences meter and claims on their own Decisions.

## Verification

Boundary A: before implementation use `python tools/test_tiers.py for <paths>` and run the deduplicated tests naming changed files, with the complete reviewed range for governing text. Map changed behavior, callers and consumers to existing test homes; run standing claim, link, snippet and neutrality gates for prose. The independent mutant agent uses isolated copies of the old and new committed files, one probe per mutant per file; retain repeatable probes in tests or scripts and summarize outcomes and omissions. Do not replay broad tests for each mutation.

For C2 native-only evidence, the implementation coordinator uses the available `cairn-windows` SSH host (Windows 11 ARM64, `C:\ProgramData\miniconda3\python.exe` 3.13.17). Transfer disposable exact committed old and new source copies and verify their commits and source hashes. In the activated Miniconda environment, run `scripts/run_windows_interpreter_binding.py` for its binding family: its DLL path, Git, pytest and symlink privilege prerequisites must hold. Also run the exact applicable Windows `NATIVE_ONLY_NODE_IDS` for eligible code-map and interpreter-binding families, and each independent old/new mutant through its actual public entry point on Windows. Retain commands, node IDs, interpreter, hashes, old/new results and skips in the plan evidence; use existing runners and canonical test homes for reproducible probes. A host skip, missing prerequisite, unmatched native probe or absent evidence is unpassed and stops that family’s removals. An equivalent probe must exercise the actual public behavior. No human trial or broad Windows suite is a prerequisite.

Boundary B: **wide**, on a clean final reviewed commit under `/Users/kendal30/conda_envs/lhm/bin/python3.13`, after code review and fixes. Run the deduplicated iteration list for the whole reviewed range plus tier-map integration/workflow tests naming those files, the acceptance commands above and applicable security and trust-ceremony checks. Record SHA and range, interpreter, pre/post state, commands, counts, elapsed time, omissions and non-passes; record timing misses and the over-10-second files on the consolidation list. Boundary C is independent code-review falsification, including targeted checks and explicit coverage gaps. The Security Review for each removal set is in addition to ordinary review. The release certification and re-anchor are separate; neither substitutes for a failed change check.

## Plan review -- GPT-6.1 Terra (Reviewer) -- 2026-11-08

Reviewed commit: 864b5a783c7efd7d6116d3cac0f6c61f7206fe83

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: APPROVE
**Elapsed**: approximately 3 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: C1 tests upgrade promises and refusals against the old file, C2 carries the comparison and independent defensive-site probes into later families, and C3 ships the accepted adopter capabilities after the pilot; protected removals receive the separate reviews and evidence the Decision requires. -- Plan Scope, Sequence and C1–C3; accepted proposal Outcomes 2–4 and Decision.
2. **Best alternative.** Keep inventory as C1's internal step and reuse the existing tests and guidance: a pilot-only delivery would lose the accepted later-family work and adopter tool, while a separate inventory plan would add a dependency without delivering the outcome. -- Plan Sequence and Reuse; `test_upgrade.py` and `testing-discipline.md` at the reviewed commit.
3. **What would show it wrong?** A pilot mutant caught by the old file but missed by the new one, or a tool false positive on the scientific example or sampled upgrade tests, would fail its stated gate and require repair. -- Plan C1 and C3.

The plan explicitly preserves hostile-state and caller-visible fault coverage while recording the Maintainer's narrower acceptance of internal-only mutant loss. It assigns text pins to functional prose, leaves meter and claims behind their Decisions, and keeps the human release baseline operation outside archive while retaining failed checks as implementation work. -- Plan Scope, Scope delta and Verification; accepted proposal Outcome 3.

**Coverage:** Compared the committed plan with the accepted proposal, its widening and Decision, and inspected the named reuse homes and plan template. Did not execute implementation checks, enumerate future removal families, or perform the separately required Security Review; no suite was run.

## Plan review -- GPT-6.1 Sol (Security Review) -- 2026-11-08

Reviewed commit: 864b5a783c7efd7d6116d3cac0f6c61f7206fe83

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: approximately 8 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes, with the native execution prerequisite repaired: C1/C2 preserve caller-visible refusals through independent old/new probes, defensive-site enumeration and removal-set Security Review; the accepted loss concerns internal-only mutants. -- Plan C1/C2; source Outcomes 2/3 and Decision.
2. **Best alternative.** Reuse the existing native probe route within C2 rather than add another approval or defer an eligible family; keep node-level reviewer agreement and the existing human release ceremony. -- Plan Sequence/C2; source Outcome 3; finding 1.
3. **What would show it wrong?** An accepting mutant for a Windows reparse refusal caught by the old file but missed by the replacement would falsify retained protection; a skipped native probe establishes neither result. -- Plan C2; `bootstrap/tests/security/test_git_interpreter_binding_portable.py:397`.

**Finding 1 -- Blocking: specify the native evidence route.** C2 promises completed independent old/new probes for every eligible family, but Verification names only the local canonical interpreter. The committed code-map tests at lines 492, 516, 527 and 584 require native Windows; the interpreter-binding reparse test at line 397 does too. These non-meter security families are eligible, and local skips cannot prove their refusal coverage. Close by naming the available native execution route, its prerequisite/owner and how committed old/new probe evidence is retained; an equivalent probe must exercise the actual public behavior. Keep unmatched checks unpassed and their removals stopped. This requests execution detail for accepted checks, not a new human gate.

C3's path-only resolution, no imports, escaped output and reported parse/link failures bound the advisory tool without executing inspected projects. Source/shipped rules, module, template and install coverage are named. Expected reviewed AST mismatch remains separate from actual failed checks; release authority is preserved.

**Coverage:** Read the committed plan, accepted source and reviews/Decision, plan template, security manifest and native test guards, safety/runbook provisions. Did not enumerate every defensive site, validate future removals or run tests; those remain implementation and removal-review evidence. No suite run. Over target to explain the native dependency and its closure without adding a gate.

## Plan review response -- GPT-6.1 Terra (Implementation) -- 2026-11-08

**Elapsed**: approximately 5 minutes. **Tokens**: unknown.

- Ordinary review: no findings.
- Security finding 1, accepted: Sequence assigns the VM window and committed source staging; Verification names the Windows interpreter, existing binding runner and prerequisites, applicable native nodes, public-entry mutant probes, evidence and stop conditions. Skips do not establish coverage.
