# Plan: Keep probe evidence in tests and scripts

**Source proposal**: dev/proposals/archive/2026-10-30-codex-probe-ledgers.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Remove duplicate probe inventories while keeping evidence reproducible and review independent.

## Source proposal

The Maintainer accepted the heavy proposal at cfe260eb: remove probe ledgers and per-mutation inventories from plans, reviews and commit messages, retaining reproducible evidence and existing checks.

## Scope

Align operative `AGENTS.md`, `dev/agent_collaboration.md`, plan and proposal templates, their `templates/core/` counterparts, and `doctrine/plans.md` and `doctrine/dual-review.md`. Search other operative references and readers, including byte pins, and update affected assertions. Preserve independent review, Foundations answers, findings, coverage gaps, verification and mutation checks, and honest concise outcomes and omissions, including surviving or unmeasured mutations. Keep repeatable probes in tests or scripts; add no replacement reporting procedure. Leave historical records unchanged.

**Reuse**: N/A: no code added beyond adapting existing tests where needed.

### Documentation / doctrine surface

Prescription belongs in governing files; review guidance and authoring templates in `dev/` and shipped counterparts; rationale in the named doctrine files, per `docs/DOCUMENTATION_PLAN.md`.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Align operative text and actual readers, including shipped installation | Reviewed plan | Text and test changes |

## Acceptance criteria

C1: No operative requirement remains for a probe ledger or per-probe or per-mutant inventory in plans, reviews or commit messages. Reproducible tests or scripts retain decisive evidence; the retained obligations in Scope remain effective. Self-hosted and installed instructions agree in substance. Updated tests exercise the affected requirements and detect their absence or forbidden return; negative searches are checked against a known positive. No historical retrofit or new reporting process is introduced.

Security preflight S2/S3: C1 exercises changed assertions and their negative controls in the mapped test families below, including installation through the scaffold CLI; the independent reviewer challenges the resulting authority carried by installed instructions.

## Scope delta

Preserved.

## Verification

Boundary A: Search operative text and consumers for ledger, probe and mutation inventory wording and byte pins; inspect each hit and test negative searches against a known positive. Run `python -m pytest bootstrap/tests/test_review_sweep_ships.py bootstrap/tests/test_review_stance_in_shipped_files.py bootstrap/tests/test_review_and_verification_rules_ship.py` for source, installed and governing rule assertions, including their negative controls. Search for additional readers of changed files and run affected owning tests discovered; inspect `bootstrap/tests/fixtures/gate_manifest.json` and any other pins without changing protected controls absent the required authority. Run `python scripts/claim_check.py` on changed documents, `python scripts/check_cairn.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py`, and `python scripts/quality_gate.py --sub neutrality` for claim, link, snippet and neutrality checks. Inspect each command's trigger and actual runner before relying on it.

Boundary B: wide, because governing and shipped review contracts change. After the final implementation commit, run the mapped checks on a clean unchanged commit under canonical Python 3.13.x and append the required verification record, including the tested range, state, outcomes, elapsed time, tokens, non-pass dispositions and omissions; certification remains pending. Include affected owning families, installed paths and standing gates. Full-tree certification and re-anchor are separate ceremonies, not per-plan checks.

Boundary C: a fresh code reviewer independently challenges the changed authority and evidence, verifies the Boundary B record and decides whether its bounds suffice. Ordinary and Security Reviews remain separate.

## Plan review -- Codex gpt-6 -- 2026-10-30

Reviewed commit: 38e3bfaae94f4be913e4cfb79185e9db75c73c36
Target: scope, acceptance criteria and verification mapping against the accepted proposal
Prior findings: none
Assurance path: high-assurance

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: approximately 3 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes, provided the implementation preserves repeatable evidence and the existing independent checks; the plan's C1 and Boundaries B/C aim to do so. -- accepted proposal, Proposal and Signals; plan, C1 and Verification.
2. **Best alternative.** Keep the single implementation chunk and existing test families; map the checks already needed rather than add a reporting ceremony. -- plan, Sequence and Boundary A.
3. **What would show it wrong?** An installed instruction still requiring an inventory, or a changed assertion that no longer detects a missing retained obligation, would defeat C1. -- plan, C1; `bootstrap/tests/test_review_sweep_ships.py` installed and negative-control tests.

**P1 — Required verification mapping is deferred.** The accepted proposal's S3 requires mapping exact nodes and installed-file inputs in the plan, and its verification plan requires identifying the actual gate triggers and consumers. Boundary A names whole files and commands but defers discovering readers and inspecting command triggers until implementation. For example, `test_installed_loop_document_carries_the_obligation` and `test_an_install_without_the_sweep_is_reported` exercise installed text, while `test_plan_pass_skeletons_ask_the_plan_and_code_questions` checks template content; the plan does not map these or their inputs to changed obligations. Close by mapping the affected nodes, installed inputs, and gate triggers/runners before implementation, including any additional readers found. This is blocking because an accepted preflight requirement is unmet.

**Coverage:** Read the committed plan, accepted proposal and plan review template; inspected named test node locations and ledger assertions. Did not run checks, enumerate every reader, or perform Security Review.
