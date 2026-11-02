# Plan: Prepare a forward AST correction

**Source proposal**: dev/proposals/archive/2026-11-02-codex-forward-ast-preparation.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Prepare and review current code fingerprints for a Maintainer-approved forward baseline without reconstructing prior history.

## Source proposal

The Maintainer accepted the heavy proposal and its explicit loss of historical AST certification. It authorizes implementation, not a correction, baseline installation or signing.

## Scope

Extend the explicit forward path in `scripts/repin.py`, its `bootstrap/tests/test_repin.py`, `bootstrap/tests/test_repin_ceremony.py` and `bootstrap/tests/test_ast_attest.py` coverage, and `bootstrap/AST_BASELINE_RUNBOOK.md` and `bootstrap/REANCHOR_RUNBOOK.md`. Clarify `AGENTS.md` only if its correction rule conflicts. Preserve ordinary historical correction, release certification and baseline-install requirements. Add no trust store, ledger or manual JSON workflow.

**Reuse.** Search `scripts/repin.py` for `baseline_reader_inputs`, `build_transaction`, `apply_reviewed_pin` and `commit_reviewed_pin`: the existing classification, transaction, binding and exact-path commands are the starting point. Extend their mechanisms in explicit forward mode; identify only fields needed to bind two independent reviews and exact inputs.

### Documentation / doctrine surface

Runbooks describe the maintained ceremony; any necessary governing permission belongs in `AGENTS.md`. The existing Maintainer authority and fences remain.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Implement forward preparation, review binding and guided apply/commit with focused tests and runbook guidance. | Both required plan reviews and author response | Maintained commands, documentation and disposable workflow evidence. |
| C2 | Independent code and Security Reviews, response and final integration. | C1 committed | Review records and wide Boundary B evidence. |

## Acceptance criteria

**C1.** Explicit preparation reads one committed candidate without loading or comparing a historical anchor, preserves baseline membership, and writes only a new external evidence directory. The packet binds candidate, canonical interpreter, tool and fixture hashes, changed bodies/locations, proposed digest replacements and known-new delta; it states that history is not certified. Missing or duplicate symbols and lockfile correction refuse. Fresh ordinary and Security reviewers examine current behavior, protection machinery and checks; their records and the exact transaction are bound before application. The maintained script presents concrete approval, revalidates inputs, applies only reviewed fixture paths, and separately confirms the exact-path commit. No manual JSON or repository write occurs during preparation; no baseline is installed or signed by preparation. Ordinary paths stay strict.

**C2.** Ordinary and separate Security Reviews assess the committed implementation; all required checks pass, including wide Boundary B. Hashes identify bytes, not reviewer independence or safety.

Actual correction approval, exact-path commit and later baseline approval/signing are Maintainer-only steps outside this implementation; they require their own concrete approvals and existing ceremony controls. This plan authorizes none of them.

## Scope delta

**Scope delta**: preserved.

## Verification

`python tools/test_tiers.py for scripts/repin.py bootstrap/tests/test_repin.py bootstrap/tests/test_repin_ceremony.py bootstrap/tests/test_ast_attest.py bootstrap/AST_BASELINE_RUNBOOK.md bootstrap/REANCHOR_RUNBOOK.md` selects ten files, including the three named command and AST tests, re-anchor, gate and review consumers. Remap all final paths, including any governing change with its reviewed range; inspect readers and byte pins. Run mapped iteration checks and applicable claim, link, snippet, neutrality and `python scripts/check_cairn.py` gates.

C1 exercises real commands in disposable repositories: no prior anchor, unchanged ordinary refusal, missing/duplicate and lockfile-debt refusal, no preparation writes, unreviewed packet refusal, and reviewed-path-only apply/commit. Separately mutate candidate, transaction/packet, review binding and target fixture; each must refuse. `bootstrap/tests/test_ast_attest.py` checks unchanged membership and accounted-for digests. These tests are S2/S3; report outcomes and omissions concisely. No real refs move and no signing occurs in tests.

Boundary C is independent ordinary and Security code review, examining affected engine behavior and protection machinery as well as the packet. After fixes, wide Boundary B on a clean unchanged final commit under canonical Python 3.13 covers mapped iteration and integration/workflow tests, owning families, public command paths, standing gates and the disposable workflow. Record SHA/range, interpreter, pre/post state, commands, counts, timing, tokens, non-pass dispositions and omissions. Combine overlapping checks only on the same reviewed commit without dropping coverage. Full certification and actual baseline ceremony remain separate authorized work; do not run another full suite for this plan.
