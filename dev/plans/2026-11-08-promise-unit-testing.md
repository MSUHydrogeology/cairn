# Plan: Promise-unit testing

**Source proposal**: dev/proposals/archive/2026-11-08-claude-promise-unit-testing.md
**Status**: awaiting-plan-review
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

One coherent outcome has three dependent internal chunks. Estimate 3–6 focused workdays, with substantial uncertainty from family inventory, defensive-site probes and review; this is not a deadline. The installed interpreter, existing tests and source are available. Fresh agents provide the independent probes and required reviews.

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

Boundary B: **wide**, on a clean final reviewed commit under `/Users/kendal30/conda_envs/lhm/bin/python3.13`, after code review and fixes. Run the deduplicated iteration list for the whole reviewed range plus tier-map integration/workflow tests naming those files, the acceptance commands above and applicable security and trust-ceremony checks. Record SHA and range, interpreter, pre/post state, commands, counts, elapsed time, omissions and non-passes; record timing misses and the over-10-second files on the consolidation list. Boundary C is independent code-review falsification, including targeted checks and explicit coverage gaps. The Security Review for each removal set is in addition to ordinary review. The release certification and re-anchor are separate; neither substitutes for a failed change check.
