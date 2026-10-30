# Keep probe evidence in tests and scripts

**Author**: Codex gpt-6
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — governing doctrine and vendor-neutral authoring templates are named high-risk surfaces.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Remove probe ledgers from plans, reviews and commit messages while keeping evidence reproducible in tests and scripts.

## Context

The Maintainer directed: “Let's address the rest of issue #39 too. We don't need probe ledgers in plans or reviews or commit messages; keep the evidence reproducible in tests and scripts.” `AGENTS.md` requires a code-review falsification ledger; `dev/agent_collaboration.md` specifies its five items. `dev/plans/_template.md`, `dev/proposals/_template.md`, `doctrine/plans.md` and `doctrine/dual-review.md` repeat or direct readers to it. Shipped counterparts exist under `templates/core/`. `bootstrap/tests/test_review_sweep_ships.py` and `bootstrap/tests/test_review_stance_in_shipped_files.py` assert ledger wording.

## Proposal

Remove requirements to maintain probe or falsification ledgers in plans, reviews and commit messages, including per-probe and mutation inventories there. Keep reproducible evidence in tests and scripts, and cite relevant evidence and results concisely in the existing records. Preserve independent review, the three evidenced Foundations answers, findings and coverage gaps, applicable verification and mutation checks, and reporting of outcomes and omissions. Do not retrofit historical records. Align operative self-hosted and shipped text and its actual readers with this change; do not add a replacement reporting process.

## Rationale

A reproducible test or script preserves how to repeat a probe without duplicating its steps in lifecycle records. Concise findings and results still let a reader assess the review and locate the evidence.

## Alternatives considered

Keep the ledger: this preserves the existing record format but retains the duplication the Maintainer wants removed.

## Documentation / doctrine surface

Route cross-cutting prescription through `AGENTS.md` and `templates/core/AGENTS.md`, review guidance through `dev/agent_collaboration.md` and its shipped copy, lifecycle authoring through the proposal and plan templates and their shipped copies, and rationale through `doctrine/plans.md` and `doctrine/dual-review.md`. Search for other operative references and readers during implementation; historical archives and the changelog are history, not instructions to rewrite.

## Evidence / verification plan

A remaining operative requirement for a probe ledger in a plan, review or commit message, or loss of reproducible evidence or an existing review or verification obligation, would falsify the change. Search self-hosted and shipped surfaces, their readers and byte pins; check negative searches with a known positive. Exercise actual affected readers and installed copies, and run the applicable prose claim, link, snippet and neutrality gates. Map exact tests and commands in the reviewed plan; retain existing Boundary B and independent Boundary C requirements. Full-tree certification and re-anchor are not proposed here.

### Tests required

At minimum inspect and map the affected assertions in `bootstrap/tests/test_review_sweep_ships.py` and `bootstrap/tests/test_review_stance_in_shipped_files.py`, including their installed-file paths; identify other readers before implementation.

### Examples / smoke checks

Run `python scripts/claim_check.py` on changed documents and applicable link, snippet and neutrality gates; identify their actual triggers and consumers in the plan.

#### Security preflight — five questions, answered in writing

S1: The changed instructions are maintained repository text, installed from `templates/core/`; their readers include the named tests. No input is supplied by the work being judged as an authority to approve it.

S2: A surviving operative ledger requirement or an assertion expecting one would challenge alignment; the current references and assertions above demonstrate those checks are actionable. Implementation must test changed checks against a known positive.

S3: The named test files are selected by pytest; their exact nodes and installed-file inputs require mapping in the plan. The shipped instruction currently says code review includes a falsification ledger (`templates/core/AGENTS.md`); the named tests check that text.

S4: No parsing, fallback or authority default is proposed to change. Existing review and verification obligations remain.

S5: A reviewer could still overlook a defect, or a test could fail to exercise the claimed behavior. Reproducibility and independent review reduce neither risk to zero.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Reviewers cannot reproduce decisive evidence from the cited tests or scripts, or the change removes a required check or obscures an unresolved finding.

## Scope delta

None.

## Assurance path

**Assurance path**: high-assurance

## Proposal review -- Codex (model identifier unavailable) -- 2026-10-30

**Verdict:** Support, with one non-blocking clarification. Security Review remains separate.

**Foundations**
1. **Should it happen as framed?** Yes. The Maintainer asks to remove ledgers while retaining reproducible evidence; the proposal preserves independent review, checks, findings and omissions. Existing ledger requirements appear in `AGENTS.md` and `dev/agent_collaboration.md`.
2. **Best alternative:** Keep concise results and evidence references, with reproducible probes in tests or scripts, rather than replacing the ledger with another inventory; the proposal's operative section already takes that route.
3. **What would show it wrong?** A surviving operative inventory, a weakened falsification check, or a decisive probe that cannot be reproduced would contradict the proposal. `bootstrap/tests/test_review_stance_in_shipped_files.py` and `test_review_sweep_ships.py` include positive ledger assertions to update and test.

**Advice:** Make clear in the plan how mutation outcomes and omissions remain honest without recreating per-mutant inventories in records. `AGENTS.md` currently requires naming each survivor and equivalent, while the proposal removes mutation inventories and preserves outcome reporting.

**Coverage:** Read the committed proposal, current template and named ledger assertions; searched the named governing and shipped surfaces for ledger and mutation wording. Did not run tests, inspect every consumer or assess security independently. Elapsed: approximately 2 minutes; tokens: unknown.
