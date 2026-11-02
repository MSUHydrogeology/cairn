# Plan: Remove the obsolete finding marker

**Source proposal**: dev/proposals/archive/2026-11-02-codex-stray-finding-id.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Remove one closed-review marker while preserving the documented scaffold safeguard.

## Source proposal

The Maintainer accepted the heavy proposal to remove only the obsolete `(R5)` marker from the named inventory entry.

## Scope

Delete the preceding space and `(R5)` from the `new-core-blocked` / `new-core-lockconflict` bullet in `bootstrap/_scaffold/SECURITY_MUTATIONS.md`. Preserve its behavior description, all other identifiers and the rest of the file. No scaffold behavior changes.

**Reuse.** N/A: no code added.

### Documentation / doctrine surface

The existing security inventory is descriptive prose under the high-risk scaffold surface; no governing doctrine changes.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Check consumers and pins, make the exact deletion and exercise its byte control. | Both required plan reviews and author response | Inventory edit and iteration evidence. |
| C2 | Independent code and Security Reviews, response and final integration. | C1 committed | Review records and wide Boundary B evidence. |

## Acceptance criteria

**C1.** The final inventory equals its parent after removing exactly the specified space and marker once. The safeguard description and all other identifiers remain byte-identical. Demonstrate that comparison rejects an additional changed byte. A live consumer or byte pin requiring the marker stops the edit for reassessment.

**C2.** Ordinary and separate Security Reviews assess the committed edit; required checks pass and wide Boundary B covers the final reviewed commit.

## Scope delta

**Scope delta**: preserved.

## Verification

`python tools/test_tiers.py for bootstrap/_scaffold/SECURITY_MUTATIONS.md` selects `bootstrap/tests/test_install_module.py`, `bootstrap/tests/test_security_leaf.py` and `bootstrap/tests/test_upgrade_lockfile_path_containment.py`. The first two cite the Class A inventory; the third reads it in its path-containment assertion. Search direct readers and byte pins with a known-positive control before editing; remap if paths change. Compare parent and edited bytes with only the one deletion permitted, and demonstrate rejection of an extra byte in a separate copy. Run the mapped iteration tests and `python scripts/claim_check.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check` on the inventory, plus `python scripts/quality_gate.py --sub neutrality` and `python scripts/check_cairn.py`. The comparison and negative control are S2/S3; no runtime security proof is claimed.

Boundary C is independent targeted falsification, including separate Security Review. After review and fixes, run wide Boundary B on a clean unchanged final commit under canonical Python 3.13: mapped iteration and integration/workflow tests, owning families, known consumers, standing gates and byte control. Record SHA/range, interpreter, clean pre/post state, commands, counts, timing, tokens, non-pass dispositions and omissions. Combine overlapping final checks with other ready plans only on the same reviewed commit and without dropping coverage. No full certification run is authorized here.

## Plan review -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed commit: 9b3eb574bcb5b3ea38a2ec6b272097c948acf99b  
Target: complete exact-deletion plan against accepted scope  
Prior findings: none  
Assurance path: high-assurance

**Obligation**: Internal Security Review  
**Tier**: Internal Security Review  
**Findings**: none  
**Verdict**: ACCEPT  
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. C1 permits only the space and `(R5)` deletion once and preserves every safeguard byte and other identifier. A consumer requiring that marker stops implementation for reassessment. This retains the occupied-destination hard block and no-silent-overwrite explanation. -- Plan, Scope and C1; committed inventory bullet; accepted Decision.
2. **Best alternative.** Use the planned parent-byte comparison and existing prose/readers rather than add a scanner or test infrastructure. Leaving the marker retains the obsolete reference; broader identifier cleanup is outside the accepted correction. -- Plan, Reuse and Verification; accepted proposal, Alternatives.
3. **What would show it wrong?** Another byte changing or the comparison accepting an altered safeguard. C1 requires the exact comparison and an extra-byte negative control in a separate copy; the known-positive reader search protects against an assumed absence of consumers. -- Plan, C1 and Verification; proposal S2/S3.

No blocking finding. The named path-containment test actually reads the inventory and checks guard names; the install and leaf references document their Class A sets rather than test this marker. The plan correctly avoids claiming runtime security proof and retains mapped checks, independent reviews and clean canonical-Python wide verification. No new machinery is necessary.

Coverage: read committed plan, accepted proposal/Decision, current plan template, inventory entry and three named test references including the live inventory assertion. Did not reproduce mapping, enumerate all pins/readers, run the byte control or execute suites. Those implementation checks remain owed; this pass clears only the Security plan obligation.

## Plan review -- Codex (GPT-6), Reviewer -- 2026-11-02

**Obligation**: Internal  
**Verdict**: proceed as framed; no findings.

**Foundations.** (1) Yes: C1 limits the edit to the space and `(R5)` in the named bullet. The committed inventory's following lines describe the occupied-destination split, which the byte-equality criterion preserves. A live consumer or pin requiring the marker stops the edit. (2) The least involved credible alternative is to leave the marker; that saves the edit and its checks but leaves the obsolete reference. For removal, the existing byte comparison and mapped checks are sufficient without adding a scanner. (3) Another changed byte, a consumer requiring the marker, or a comparison that accepts an extra changed byte would show the plan wrong. C1 and the known-positive reader search explicitly test those cases.

The stated heavy review and wide final verification follow the accepted Decision and existing obligations; they do not change the one-line implementation scope or claim a new runtime security proof.

**Coverage:** Read the committed plan, accepted proposal and Decision, and the named inventory entry at `e8ce3e37`. Did not run checks, enumerate consumers or independently prove runtime safeguard behavior; implementation and separate Security Review cover their respective obligations. Elapsed: approximately 2 minutes. Tokens: unknown.

## Response to plan reviews -- Codex GPT-6.1 Sol -- 2026-11-02

Both reviews accepted the plan without findings. The exact-byte control, mapped checks, separate Security code review and wide final verification remain required. Elapsed: under one minute; tokens: unknown.

## Implementation verification -- Codex GPT-6 (Implementation) -- 2026-11-02

**C1 changed surface:** `bootstrap/_scaffold/SECURITY_MUTATIONS.md`; removed only the space and `(R5)` before the colon. The two guarded-write test files cite the inventory as the Class A set. `test_upgrade_lockfile_path_containment.py` dynamically reads it at `test_the_inventory_of_guards_names_each_one` and checks three guard names, not this marker. A known-positive path search found those three test references; an exact-marker search found one occurrence, in the target bullet. No consumer or byte pin requires `(R5)`.

The parent-derived byte comparison confirmed the file equals its parent after exactly that deletion. A separate copy with one appended byte failed the equality control. The mapped selector returned `bootstrap/tests/test_install_module.py`, `test_security_leaf.py` and `test_upgrade_lockfile_path_containment.py`; all 118 tests passed in 9.25 seconds on Python 3.12.9 in a separate candidate copy.

The inventory claim, link and snippet checks passed. Neutrality reported zero failures and 43 informational results. `check_cairn.py` reported three existing broken proposal links in `dev/PLANNING.md` and `dev/strategy/2026-10-28-codex-v06-decision-master.md`; this inventory edit introduces none. An initial selector command used the wrong `scripts/` path and ran no tests; the corrected `tools/test_tiers.py` command selected the three files above.

**Not yet covered:** independent ordinary and Security code reviews, final wide Boundary B, canonical Python 3.13, and clean committed-tree evidence remain due after review. No full certification run was made. **Elapsed:** approximately 5 minutes; **tokens:** unknown.

## Code review -- Codex (GPT-6), Reviewer -- 2026-11-02

**Reviewed:** `34fdba18`. **Verdict:** no findings; proceed to separate Security Review and final verification. **Bounding:** no wider run required beyond the already planned wide Boundary B.

**Foundations.** (1) Yes: a direct comparison of committed parent and candidate bytes confirms that the only inventory change is removal of the one space and `(R5)` from the named bullet; the safeguard description remains intact. (2) Leaving it would avoid the edit but retain the obsolete reference identified in the accepted proposal; the single deletion meets the agreed scope without new machinery. (3) Another changed byte or a consumer needing the marker would disprove the change. The byte comparison passed; the implementation record reports a known-positive consumer search and a negative comparison control. It also records 118 mapped tests passing on Python 3.12.9 and the outstanding canonical-Python final run.

The implementation snapshot's three broken proposal links were reported, not passed; `1f51b479` subsequently updates the relevant planning and strategy links. Their final gate result remains owed at Boundary B.

**Coverage:** Inspected the committed diff, plan and implementation evidence, independently compared inventory bytes, and inspected the subsequent link correction. Did not rerun implementation tests, enumerate all consumers or assess runtime security behavior; separate Security Review and wide Boundary B remain due. Elapsed: approximately 2 minutes; tokens: unknown.

## Security code review -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed commit: 34fdba186a1b8e972e617d554625fab075de457d  
Target: inventory deletion and C1 evidence; ordinary review `d1660b3b`  
Prior findings: none  
**Tier**: Security Review  
**Verdict**: ACCEPT; no findings.  
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. Direct comparison of committed parent and candidate proves the inventory changes only by removing the specified space and `(R5)` once. All safeguard descriptions, guard names and other identifiers remain byte-identical. -- Targeted byte comparison; implementation diff; C1.
2. **Best alternative.** Leave the marker, avoiding an edit but retaining the obsolete reference. The exact deletion meets the accepted correction without a scanner, new test infrastructure or changed security behavior. -- Accepted proposal, Alternatives; inventory diff.
3. **What would show it wrong?** Another changed byte or a consumer requiring the marker. My parent-derived comparison passed, and an extra-byte candidate failed its equality control. Author evidence reports a known-positive reader search and no marker consumer; the live reader checks guard names. -- Targeted assertions; iteration record and named path-containment reader.

**Bounding**: ACCEPTED — challenged the exact-byte boundary directly; no security information was lost. Author evidence records 118 mapped passes under Python 3.12.9, inventory prose checks and neutrality. Its three unrelated broken links were explicitly reported; ordinary review identifies subsequent correction `1f51b479`, whose final gate result remains required rather than assumed passed.

Coverage: read accepted scope, committed inventory and plan evidence, ordinary review and reader contract; independently executed the exact-deletion/extra-byte controls on committed bytes. Did not rerun implementation tests, enumerate every consumer or audit runtime guards. No suite run. No reached approval fence or scope deviation in the edit. Clean canonical-Python wide Boundary B, including final standing-gate results, remains owed before closure.
