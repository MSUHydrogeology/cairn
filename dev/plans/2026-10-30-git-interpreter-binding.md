# Plan: Bind the interpreter in per-worktree Git administration

**Source proposal**: dev/proposals/archive/2026-10-29-codex-git-interpreter-binding.md
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance
**Opened**: 2026-10-30
**In brief**: Store each worktree's interpreter choice in its Git administration instead of project content.

## Source proposal

The accepted contract relocates the executable selection from checkout content
into trusted per-worktree Git administration, without migrating the old file.
It preserves explicit rebinding, records copied administration as a residual
trust assumption, and requires native Windows evidence.

## Scope

Change the installer, session resolver and shipped copies, their consumers and
owning tests; retain the legacy ignore rule. Inventory references before
implementation. Update `AGENTS.md`, its shipped equivalent,
`bootstrap/UPGRADE.md` and `bootstrap/SAFETY.md`, including rebinding and the
copied-administration and delivered-pointer residual. Same-user races and
executable provenance remain outside the boundary. No scientific check applies.

**Reuse.** Searching `tools/session.py` and `bootstrap/_scaffold/install.py`
for `local-env`, `local_env` and `interpreter` found `_resolve_interpreter`,
`write_local_env`, existing path and tracked-executable checks; reuse or adapt
them and the existing scrubbed Git invocation where applicable. Search
`rg -n 'local-env|local_env|_resolve_interpreter|write_local_env' tools bootstrap templates AGENTS.md`
for consumers and documentation before implementation; account for each hit.

### Documentation / doctrine surface

`AGENTS.md` and its shipped equivalent carry governing instructions; safety and
upgrade guides describe operation. Route changes under
`docs/DOCUMENTATION_PLAN.md`. Do not change other doctrine without establishing
its evolution trigger and recording the evidence.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Relocate discovery, reading and writing; update guidance and tests | Both plan reviews | Installer and session paths, shipped copies, docs and portable tests |
| C2 | Verify final implementation and hand to code review | C1 complete; native Windows evidence | Wide change-specific record and review handoff |

## Acceptance criteria

### C1

Discovery uses a scrubbed Git environment and requires the supplied root to be
the exact worktree root. Normal, linked, separate-directory and submodule
repositories work independently. Non-repository and nested targets install
without a binding, report this and give Git initialization and rerun guidance;
session falls back with guidance. Discovery errors and unsafe state refuse.
Never read or migrate the legacy file. Only true absence falls back; dangling
links, reparse points, wrong types and unreadable state refuse before launch.
Preserve schema, executable-shape, tracked in-project executable and warned
stale-executable behavior. Writes stay inside verified per-worktree
administration through a dedicated guard; unsafe destinations cannot be
clobbered even with force. Existing safe bindings survive unless forced. Do
not relax the target-tree guard. Guidance explains that copied administration
or a delivered pointer can supply a binding and must be trusted or rebound.

S2: a marker test through the real entry point detects deliberate redirection
to the legacy file; record control and mutant outcomes. S3: mapped tests and
gates below exercise the revised guidance and implementation.

### C2

Record clean tested commit, range, canonical interpreter, pre/post state,
commands, counts, timing, non-pass dispositions and omissions. Native Windows
must demonstrate discovery and junction/reparse handling before acceptance;
name any unsupported link case and leave a required unchecked case open. Hand
implementation and evidence to independent usual and Security code reviews.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A runs the mapping while iterating; Boundary B repeats it on the final
clean committed tree under canonical Python 3.13 in **wide** mode for the
trust boundary, with `Certified by: pending`. Split selections within the
pytest guard's file limit and reconcile their union. No full certification run
is authorized by this plan.

* Exercise actual scaffold and session entry points for normal, linked,
  separate-directory and submodule repositories; no-repository and nested
  targets; hostile Git environment; legacy malicious binding; safe existing
  destinations and unsafe destinations with and without force; valid,
  malformed, stale and tracked executables. Assert ancestor isolation,
  containment, no launch on refusal, and worktree independence. Add portable
  tests that run on Windows; record native Windows discovery and
  junction/reparse results separately.
* Run owning families `bootstrap/tests/test_session_binding_untracked.py`,
  `bootstrap/tests/test_session_binding_gate_and_printing_hold.py`,
  `bootstrap/tests/test_session_kernel.py`, `bootstrap/tests/test_session_failsafe.py`,
  `bootstrap/tests/test_session_writes_contained.py`,
  `bootstrap/tests/test_install_module.py`, `bootstrap/tests/test_skills_install.py`,
  `bootstrap/tests/test_skills_security.py`, `bootstrap/tests/test_security_leaf.py`
  and `bootstrap/tests/test_security_stack.py`, plus readers found by inventory.
* Run `python scripts/claim_check.py` on changed documents,
  `python scripts/check_cairn.py`, `python scripts/link_check.py`,
  `python scripts/quality_gate.py --sub neutrality --sub redundancy`, and
  `python -m pytest bootstrap/tests/test_security_lint.py` for the engine
  security lint; a skip does not satisfy it. Run snippet sync if a synced source
  changes. Preserve applicable frozen-file and AST re-anchor ceremonies; do not
  compare against a historical anchor as change verification.

Boundary C independently falsifies the reviewed change and verification record;
its reviewer records bounding and a targeted ledger, without running the full
suite.


## Plan review -- Codex gpt-6.1-sol -- 2026-10-30

```
Reviewed commit: 49e6a59123b88bf954d1b5ee4e7a6a6ba2b0fc05
Target: opening plan and accepted proposal contract
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The outcomes follow the Decision, but the test and consumer mapping must be finished before implementation so this review can assess its coverage -- plan Scope and Verification; `dev/plans/_template.md` > Verification.
2. **Best alternative.** Keep the two chunks, but complete the reference inventory and map affected consumers to checks now; this preserves all accepted outcomes without another implementation chunk -- plan Sequence and Verification.
3. **What would show it wrong.** A no-repository install changes an ancestor binding, an unsafe path launches or escapes containment, or a required native Windows case cannot be demonstrated -- plan Acceptance criteria C1–C2.

**P1 -- blocking: finish the reviewed verification mapping.** Scope defers the reference inventory until implementation, and Verification adds unspecified “readers found by inventory.” The template requires the mapping before implementation, and the accepted proposal requires readers, writers and consumers mapped in the plan. The named families and behavioral list do not establish which existing consumers or shipped copies are covered, nor the commands that exercise the new entry-point and mutation checks. **Satisfier:** run the stated inventory against the committed tree, account for affected readers and shipped copies, and name their test files or nodes and executable commands (including the control and mutant check); identify any uncovered surface and its required check. This retains the accepted scope and lets the author respond without another plan review.

**Coverage:** accepted contract and Decision, repository-less and nested targets, supported Git layouts, refusal and native Windows acceptance: plan C1–C2 and proposal Current contract; verification and lifecycle: plan Verification and `dev/plans/_template.md`. **Not covered:** no implementation or native Windows evidence exists; no tests were run. The separate Internal Security Review remains open.
