# Plan: Living plans and concise records

**Source proposal**: dev/proposals/archive/2026-11-12-claude-plan-records-and-living-plans.md
**Author**: gpt-6.1-terra (Medium), plan author
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: Keep active plans current while preserving reviewed evidence and making costs visible at closeout.

## Build summary

Make the four operative plan cells editable throughout active work, with review bound to substantive changes. Preserve historical authority and every verification duty while shortening repeated instructions. Give final records a countable benefit judgment and add its advisory summary to Cairn's existing release report.

## Source proposal

Decision `5962633b` accepted the revised heavy v0.7 proposal, including its design-origin routing. Its Proposal A–C, security preflight and retained scope govern this plan; its historical measurements are not implementation evidence.

## Scope

Change Cairn's `AGENTS.md`, `dev/agent_collaboration.md`, plan and proposal templates and their `templates/core/` counterparts; reconcile `docs/methodology/plans.md`, `lifecycle.md` and `lifecycle-contract.md` with the installed rules. Change `tools/board.py` and its shipped `templates/skills/_lib/board.py` twin, Cairn-only `tools/audit_report.py`, and `docs/release-process.md`. Inventory other actual consumers of review headings and verification records before editing, including audit pulse; preserve their evidence semantics. Do not ship the audit reporter or change release authority.

Reuse: `tools/board.py`'s `--next` review/response reader and H2 section parser, its shipped twin, and `tools/audit_report.py`'s archive walk, `--root` and pulse paths already serve these jobs. `rg` for their headings and filenames found the board contract and replacement-tool tests; extend their public entry paths, not a new command, checker, collector or sidecar.

## Sequence

Estimate two focused implementation windows plus independent reviews and final verification. The main uncertainty is preserving advisory reader compatibility across legacy and amended records. Both chunks are agent-executable after the required plan reviews; C2 depends on C1's contract. Commit each lifecycle transition separately.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Reconcile active-plan lifecycle, record grammar and receipt guidance. | Plan reviews | Paired governing templates and methodology |
| C2 | Implement and verify existing readers and release invocation. | C1 | Board twins, advisory audit report, public-contract tests and release guidance |

C1: Scope, Sequence, Acceptance criteria and Verification remain mutable only while active. A change-log entry identifies the revision commit, cells, change and reason; it cannot rewrite historical Reviews, responses, records, Decisions, quotations, accepted proposal scope or fences. Substantive changes stop affected and dependent work; return to `revising-plan`, commit the replacement, request a fresh non-author ordinary review and applicable Security Review, record author disposition, then use `ready-to-implement` before resuming. Preserve owed code-review returns, final verification, scope-reduction approval and Security Review caps. Wording/status changes that change no obligation need no amendment review; missing design returns to the existing operative cells.

For machine-readable amendment chains, each change-log entry names the full prior and replacement Git object IDs (40 or 64 hexadecimal characters), affected cells/dependencies, change, reason and exact required obligations. The operative revision commit may use `this commit` for its replacement while status is `revising-plan`; the next plan-only metadata fill commit replaces that marker in the same entry with the just-created revision SHA before review. This fill is not another revision. Affected work remains stopped until the ID is bound and review and disposition are complete. The first prior ID is the original full-review target; each later prior ID is the preceding amendment replacement SHA, not a review or disposition commit.

Each distinct `## Plan amendment review -- <reviewer> -- <date>` records the identical prior/replacement pair, affected cells/dependencies, one `**Obligation**` and `**Verdict**`. Require one unambiguous ACCEPT per required obligation and an author ready disposition. Committed records are authority; the board is advisory and compares full SHA strings and record order without invoking Git or proving SHA ownership. A consistently forged SHA cannot be detected by this text-only comparison. No historical record is overwritten. Keep original full review distinct and existing full-review behavior compatible.

C1 also replaces the repeated Verification instructions in both plan templates toward 700 words each, mapping each removed passage to its retained duty: Boundary A selection and prose gates; Boundary B timing, clean unchanged final commit, mode/rationale and consumers, range, interpreter, command outcomes/counts/elapsed/Tokens, acceptance commands, non-pass disposition and omissions; Boundary C, timing diagnostics, conditional Tokens retirement, review fixes and final commit duties. Keep checks, not merely field names. Replace the old closing sentence in both plan and light-proposal templates and lifecycle guidance with `**Benefit versus cost**: <verdict> -- <benefit>; cost <measured>; remaining burden <measured>`. Verdict is `worth it`, `partly`, `not worth it`, or `unknown` with revisit condition. Use the declared implementation-to-tested range for Git counts and net burden; distinguish aggregate agent elapsed from wall time, report missing as `unknown`, and include available decision counts, shipped/always-loaded word changes, test count/runtime and installed-file deltas from existing records. No new collector or review stage.

C2: board `--next` recognizes the chain without counting amendment records as duplicate original reviews. A missing, conflicting, rejected, extra or skipped link/obligation, duplicate or mismatched record, or unresolved marker stops selection; Git and non-Git roots behave identically for identical records, and unavailable Git never approves an unknown marker; a changed Verification or dependency cannot inherit an earlier ACCEPT. The audit command selects each archive's last H2 implementation-verification section only, ignores fenced and quoted examples, lists each plan then verdict totals, reports absent lines `no line` without a new warning, and malformed/duplicate/conflicting current lines `unknown` with advisory diagnostic. Keep historical archives unchanged; preserve existing audit and pulse evidence semantics. Document `python tools/audit_report.py` for the existing release-closeout owner; it is read-only, advisory and not a release gate.

## Acceptance criteria

### C1

The paired rules and published explanations agree on the revision, stop, review and resume conditions and retain accepted baseline, immutable history and all prior assurance duties. Compare each original Verification duty and receipt field to its new home; measure both sections and both always-loaded caps (Cairn 2,000; shipped 1,500). The 700-word target is not a cap or permission to omit evidence. Light and planned final records use the same countable line, including unknowns and range.

### C2

Extend `bootstrap/tests/test_board_json_contract.py` through `board.py --next --json` for both board copies using temporary artifacts: a complete chain with distinct ordinary and Security obligation records and a subsequent revision continues; unresolved markers and absent, inconsistent, skipped, extra, duplicate, mismatched, conflicting and rejected links or obligations stop in Git and non-Git fixtures; Verification-only weakening and changed dependency cannot reuse old approval. Extend `bootstrap/tests/test_replacement_tools.py` through `python tools/audit_report.py --root <temporary-root>`: last versus earlier record, historical absence, duplicate/malformed current line, fenced/quoted example, and valid totals. Preserve existing public pulse and review-evidence behavior. Tests assert structured fields, verdicts and stop behavior, not prose wording; temporary developmental probes are removed. Security preflight S2/S3 uses these real entry points; no identity authentication or tamper-proof Git is claimed.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation run `python tools/test_tiers.py for <changed paths>`; pass the reviewed range for governing text. Run mapped tests and applicable claim, link/content, snippet and neutrality prose gates; count negative searches against a known-positive case. Compare paired copies and receipt-duty mapping, measure word counts and exercise the named public commands. Boundary C is independent ordinary and Security code review with targeted falsification. After reviews, Boundary B is wide for governing and trust surfaces, on a clean unchanged final commit: mapped iteration and integration tests, owning/public paths, standing gates and plan-specific commands. Record mode and rationale, full tested SHA and reviewed range, interpreter, pre/post state, command table including outcomes, elapsed and Tokens, non-passes and omissions. Certification remains separate.

## Plan review -- GPT-6 Sol (Security Review, High) -- 2026-11-12

Reviewed commit: `857ff426`

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: approximately 5 minutes
**Tokens**: unknown

**Steelman.** Active plans can stay accurate while commit-linked review records preserve earlier authority and the existing advisory board shows the next move.

**Foundations**
1. **Should this happen as framed?** Yes, once amendment identity is specified so changed Verification cannot inherit old approval -- source proposal, Proposal A and S1-S5.
2. **Best alternative.** Keep the board and distinct records, defining unresolvable-history behavior -- `tools/board.py`, `_next_review_state`.
3. **What would show it wrong?** A Verification-only revision labeled `this commit` remains actionable through an old ACCEPT; test both boards with Git and non-Git fixtures -- C2 acceptance criterion.

**Blocking finding -- amendment binding is underspecified.** C1 permits `this commit` as a replacement identifier, but later reviews use a full commit ID. The board reads plan text without Git history (`tools/board.py`, `_next_sections`/`_next_review_state`); its `--root` fixtures need not be Git repositories (`bootstrap/tests/test_board_json_contract.py`). Specify how to resolve that marker, check original-to-amendment and subsequent links across separate review commits, and stop when a link cannot be established, including without Git. Test complete and forged, skipped or unresolvable chains through `--next --json`. This trust-boundary choice cannot be left to a Low implementer.

**Does any rule weaken or disappear?** Freeze and one-round rules change intentionally; C1 retains fences, history, Security caps and Boundary A/B/C duties, subject to the gap above.

**Covered:** source A-C/S1-S5, plan C1/C2, board reader and tests, receipt fields. **Not covered / low confidence:** implementation, parser probe or test run.

## Plan review -- GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-12

Reviewed commit: 857ff426

**Obligation**: Internal
**Tier**: Internal
**Findings**: blocking
**Verdict**: REVISE
**Elapsed**: approximately four minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes in purpose: current operative cells and retained evidence can coexist, but the reader needs a specified commit-binding mechanism before Low execution -- accepted proposal A; Sequence C1–C2.
2. **Best alternative.** Reuse the existing advisory board and committed records with a small, explicit resolution rule; do not add another authority source -- `tools/board.py` `--next`; proposal A6.
3. **What would show it wrong?** A changed Verification or dependency accepted under an earlier review, or an unresolved replacement treated as approved, would falsify it. Exercise both board copies through `--next --json` with linked Git revisions and unavailable history -- C2.

**Blocking:** C1 permits `this commit`, but neither its grammar nor C2 says how the reader identifies the revision containing that line, matches it to the review's full replacement SHA and prior chain, or behaves when Git history is unavailable or ambiguous. Current public `--root` fixtures use plain temporary directories; they cannot establish that binding. Specify the smallest workable resolution and conservative advisory stop, including how changed Verification and dependencies are associated with the reviewed replacement; add public Git and non-Git falsifiers. This closes the execution design without making the advisory board an authority.

**Rules and audience:** The freeze after implementation intentionally changes; immutable history, accepted scope, review and verification duties remain specified in C1. Installed guidance must carry those duties for agents without a person-level decision.

**Coverage:** Read the committed plan, accepted proposal, plan template, board reader and representative public fixtures. Did not implement, run tests or independently review every consumer; Security Review is separate.


## Response -- GPT-6.1 Terra (plan author, Medium) -- 2026-11-12

- **Security blocking finding / ordinary blocking finding:** C1 now requires explicit full object IDs in settled entries, a plan-only metadata fill before review, the original review target as the first prior and the preceding replacement as each later prior. It binds affected cells, dependencies and separate required obligation records to the same pair and requires author disposition. The board compares record strings and order, stops on unresolved or broken chains and does not use Git; its inability to detect a consistently forged SHA is explicit. C2 adds the requested public Git and non-Git falsifiers and next-revision coverage. These additions are necessary to close the two findings and account for the opening plan exceeding its 1,000-word target.

No implementation, new review pass or scope waiver is claimed. **Elapsed**: unknown. **Tokens**: unknown.
