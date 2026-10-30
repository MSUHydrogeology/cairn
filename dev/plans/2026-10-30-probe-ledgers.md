# Plan: Keep probe evidence in tests and scripts

**Source proposal**: dev/proposals/archive/2026-10-30-codex-probe-ledgers.md
**Status**: ready-to-implement
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

Reader mapping: `test_review_sweep_ships.py::test_source_sweep_carries_the_obligation` and `::test_the_ledger_is_defined_once_with_five_items` read both loop copies; `::test_agents_md_pointer_carries_the_obligation` reads both governing copies. Its `installs` fixture runs `bootstrap/scaffold.py --config <profile> --target <temporary tree>` for every `bootstrap/profiles/*.yml`; `::test_installed_loop_document_carries_the_obligation`, `::test_installed_agents_md_carries_the_pointer`, and `::test_an_install_without_the_sweep_is_reported` read installed `dev/agent_collaboration.md` and `AGENTS.md`. Adapt the ledger shape and mutation controls (`::test_adding_a_sixth_ledger_item_is_reported`) to the retained outcomes.

`test_review_stance_in_shipped_files.py::test_review_section_carries_the_obligation` and `::test_loop_document_roster_carries_the_obligation` read both governing and loop copies; `::test_template_review_section_carries_the_obligation` and `::test_plan_pass_skeletons_ask_the_plan_and_code_questions` read both plan and proposal templates as applicable; `::test_doctrine_carries_the_statement` reads doctrine. `test_review_and_verification_rules_ship.py::test_agents_md_carries_the_obligation` reads both governing copies and pins set mutation and summaries. Run the complete three files above to include their negative controls and other retained authority assertions. A text search found these three direct ledger readers; the open upgrade plan contains historical work records, not an operative ledger rule. The manifest lists test files, so inspect its pin implications before altering tests.

Gate triggers and runners: `claim_check.py` takes one named document and calls `check_file`; `check_cairn.py` walks filtered tracked Markdown and delegates claims and links to shipped `templates/modules/default-on/claim_check.py` and `templates/modules/team-gated/link_check.py`. `link_check.py` walks filtered tracked Markdown; `sync_doc_snippets.py` checks tracked Markdown by default; `quality_gate.py --sub neutrality` walks its configured roots and scans their files. These commands themselves run the checks, rather than recording claims for a later runner.

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

## Plan review -- Codex Sol -- 2026-10-30

Reviewed commit: 38e3bfaae94f4be913e4cfb79185e9db75c73c36
Target: security preflight, instruction authority and verification boundaries
Prior findings: none
Assurance path: high-assurance

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none additional
**Verdict**: Support security scope; ordinary finding P1 remains open
**Elapsed**: approximately 4 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. The plan retains independent review, mutation checks and unresolved outcomes while removing duplicate inventories; these are the accepted security safeguards. -- accepted proposal, Proposal; plan, Scope and C1.
2. **Best alternative.** Use existing test families and their installation path, with concise evidence references; no replacement ceremony is needed. -- `bootstrap/tests/test_review_sweep_ships.py`, `installs` fixture invokes the scaffold CLI for shipped profiles.
3. **What would show it wrong?** Installed instructions permitting self-approval, dropping an owed check, or leaving decisive evidence unreproducible would contradict C1. -- plan, C1 and Boundaries B/C; `bootstrap/tests/test_review_stance_in_shipped_files.py`, security-obligation and independence assertions.

The changed authority is the instruction text delivered to adopters. The plan explicitly challenges that installed authority and retains separate ordinary and Security Reviews. It proposes no new parser, execution, credential or network boundary. Wide Boundary B is appropriate for this contract surface. P1's missing mapping must be resolved before implementation; naming a test family alone does not establish that its controls cover the retained safeguards.

**Coverage:** Read the committed plan and accepted proposal, plan-review template and named test consumers, including scaffold installation and independent security-obligation assertions. Did not run implementation checks, enumerate all consumers or assess implementation bytes; full-suite certification and re-anchor were not run.

## Response to plan review -- Codex gpt-6.1-terra -- 2026-10-30

P1: accepted; Verification now maps affected nodes, installed inputs and gate runners. Security Review raised no additional finding. Elapsed: approximately 3 minutes; tokens: unknown.
