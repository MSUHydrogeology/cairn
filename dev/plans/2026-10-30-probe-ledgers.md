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

## Implementation verification -- Codex gpt-6-luna -- 2026-10-30

**Boundary B mode**: wide. The governing review instructions, installed copies, authoring templates and review doctrine changed. The mapped suite exercises source, shipped and installed text; its install fixture invokes the scaffold CLI for all shipped profiles.

**Certified by**: pending

**Tested commit**: `2fc884de1b756add61e61816d48aa598590cbe2d`

**Reviewed range**: `d268d574c31434ec9a27329e9a5219cae5b1c4a7..2fc884de1b756add61e61816d48aa598590cbe2d`; includes implementation commit `bf5d566d94fd64a20031ce9325581f132783f23e` and the separate metered-cost Decision commit `2fc884de`.

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13.

**Pre-run state**: clean clone at the tested SHA; `git status --porcelain=v1` empty.

**Post-run state**: clean clone at the same tested SHA; `git status --porcelain=v1` empty.

| Command | Exit | Outcomes | Elapsed | Tokens |
| --- | ---: | --- | ---: | --- |
| `python -m pytest bootstrap/tests/test_review_sweep_ships.py bootstrap/tests/test_review_stance_in_shipped_files.py bootstrap/tests/test_review_and_verification_rules_ship.py` | 0 | 774 passed; 0 failed, skipped, xfailed or xpassed | 2.64 s | unknown |
| `python scripts/claim_check.py` on each of the 11 changed documents | 0 | 11 passed; no claim-check flags | about 0.23 s combined command time | unknown |
| `python scripts/check_cairn.py` | 0 | 189 Markdown files; no issues; 87 external links not probed | 1.25 s | unknown |
| `python scripts/link_check.py` | 0 | 189 Markdown files; no issues; 88 external links not probed | 0.18 s | unknown |
| `python scripts/sync_doc_snippets.py` | 0 | 485 documents; no drift | 0.19 s | unknown |
| `python scripts/quality_gate.py --sub neutrality` | 0 | 0 failures; 43 informational messages | 0.90 s | unknown |

**Non-pass disposition**: none. Neutrality messages were informational; external URLs were not probed by the mapped local checks.

**Plan-specific acceptance commands**: the mapped three-file test run, document claim checks, Cairn content/link checks, snippet synchronization and neutrality gate all passed.

**Known omissions**: no full-suite certification or re-anchor was run; both remain separate authorized ceremonies. External links were not probed. Detailed mutation controls remain in the mapped test families; no additional manual mutation run was performed.

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

## Code review -- Codex gpt-6 -- 2026-10-30

Reviewed commit: 2fc884de1b756add61e61816d48aa598590cbe2d
Target: implementation bf5d566d and Boundary B record at 8d806843
Prior findings: none

**Findings**: raised
**Verdict**: REVISE
**Elapsed**: approximately 3 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** The text removes duplicate inventories while retaining independent falsification, but the tests do not reliably detect their return. -- `dev/agent_collaboration.md` review sweep; C1; finding below.
2. **Best alternative.** Reuse the existing governing-text checks and add a meaningful forbidden-return control, rather than create a reporting procedure. -- `bootstrap/tests/test_review_stance_in_shipped_files.py`.
3. **What would show it wrong?** Reintroducing the old governing requirement without a failing check shows C1's forbidden-return assurance is unmet. -- isolated mutation and mapped governing nodes below.

**P1 — Forbidden return survives the mapped checks.** In an isolated copy of 2fc884de, appending `Code review includes a falsification ledger.` to `AGENTS.md` left both mapped governing nodes in `test_review_stance_in_shipped_files.py` and `test_review_and_verification_rules_ship.py` passing: 136 passed under Python 3.13.13. The existing negative control in `test_review_sweep_ships.py::test_adding_a_sixth_ledger_item_is_reported` checks the injected string directly, not the assertion that guards the governing file. C1 requires updated tests to detect forbidden return. Close by exercising the actual absence check against a known-positive forbidden requirement across the affected operative carriers, and record fresh verification.

**Bounding**: WIDER RUN REQUIRED — the mapped checks do not detect the demonstrated forbidden return in governing instructions. Add the relevant control and verify its affected consumers.

**Coverage:** Examined the committed implementation and Boundary B record, challenged the governing instructions and their mapped checks in an isolated copy. Did not rerun Boundary B, inspect every operative carrier independently, or perform Security Review; no full suite or re-anchor was run.

## Code review -- Codex Sol -- 2026-10-30

Reviewed commit: 2fc884de1b756add61e61816d48aa598590cbe2d
Target: implementation bf5d566d and Boundary B record at 8d806843
Prior findings: ordinary code-review P1 remains open

**Obligation**: Security Review
**Tier**: Security Review
**Findings**: none additional
**Verdict**: REVISE for existing P1; no additional security defect found
**Elapsed**: approximately 4 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** The changed instruction authority preserves separate Security Review, independent reviewers and Maintainer-only scope decisions; forbidden-return assurance remains incomplete. -- governing-file diff; `test_review_stance_in_shipped_files.py` authority assertions; ordinary P1.
2. **Best alternative.** Strengthen the existing absence checks and controls; retain concise records and existing installation tests. -- `test_review_sweep_ships.py`, installed-text assertions and `test_adding_a_sixth_ledger_item_is_reported`.
3. **What would show it wrong?** A control that passes without testing the real detector cannot establish C1. The altered sixth-item control tests its own appended literal, so it does not challenge the source-file assertion. -- `test_review_sweep_ships.py::test_adding_a_sixth_ledger_item_is_reported`.

No parser, executable-selection, credential or network boundary changed. Existing security-obligation assertions remain intact. Boundary B identifies a clean committed tree, Python 3.13.13, mapped outcomes and omissions; its tested commit contains the implementation, with only an unrelated Decision added afterward. Those passing results do not close P1's demonstrated coverage gap.

**Bounding**: WIDER RUN REQUIRED — close P1 through actual forbidden-return checks and fresh affected-consumer verification.

**Coverage:** Independently inspected committed governing/shipped changes, retained authority assertions, negative-control logic and Boundary B provenance. Did not rerun implementation checks or perform additional executable mutation; the ordinary review owns its reported mutation result. No complete consumer enumeration, full suite or re-anchor was performed.
