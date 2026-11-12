# Living plans, a shorter verification record, and a benefit-versus-cost line

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy — it edits the authoring templates, `AGENTS.md` and the lifecycle contract, all named high-risk surfaces.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: A plan would be edited in place for its whole life, its final verification record would be shorter, and it would end with one labeled line saying whether the work was worth its cost.

## Decision summary

Keep an active plan current without rewriting its historical reviews or evidence. The Maintainer accepted living plans on 2026-11-10 and agreed on 2026-11-12 to shorter verification guidance and a countable benefit-versus-cost line. This v0.7 proposal joins those changes. The full receipt, required checks and conditional Tokens retirement stay. Changed requirements receive commit-bound targeted review before affected work resumes; archived plans remain immutable. Costs are paired doctrine/template edits, compatible handling of amendment reviews in existing readers, and one Cairn-only advisory report at release. No new standing review stage or human operation is added; scope reductions and extra Security passes retain their existing approvals.

## Context

The weight-review note reports a 2026-11-11 measurement of 174 plans and 572 verification sections, totaling 194,944 words, with 67 records in eight open plans. Its script was not saved: these are historical author-reported figures, not reproduced measurements or an admission criterion. The ordinary reviewer independently confirmed the template growth from 4,004 words at v0.6.1 to 4,832 at reviewed commit `98baa070`.

Re-counted 2026-11-12 with `awk '/^## Verification/{f=1;next} /^## /{f=0} f' <template> | wc -w`: the `## Verification` section is 903 words in Cairn's template and 1,021 in the shipped one. (The 885 in the weight-review note used a different count.)

The closing benefit sentence (Decision `036a0495`, 2026-11-06) has no structured reader today. A plan's operative cells stop being revisable once implementation begins (plan template, `AGENTS.md`), so later design changes arrive as appended sections.

**Origin and gate applicability.** This is a planned design proposal from the weight review and recorded Maintainer direction, not an incident-triggered doctrine patch. `dev/rules/working-agreements.md` > "Deciding and asking" says design/strategy proposals go forward on their merits and must not claim a rate-limit trigger they do not have. No recurrence count, session-close synthesis or high-risk bypass is asserted. The Decision must assess the merits; measurements alone do not establish an incident trigger.

## Proposal

**A. Living plans** (Maintainer, 2026-11-10: "Accept the living plans. That should really help.").
1. Scope, Sequence, Acceptance criteria and Verification remain revisable while the plan is active, not after archive. Each revision adds one line to a `Change log`: the commit identifying the replacement, what changed, why. Accepted proposal scope, Maintainer quotations, fences and prior reviewed/verified commits remain the baseline; editing cannot reduce their authority.
2. Reviews, responses, records and quoted Maintainer words stay append-only.
3. A substantive change to any of those four cells, including changed verification or prerequisites, stops affected execution and dependent chunks. The author commits the revision and requests a fresh non-author ordinary reviewer plus any applicable Security Review. A targeted record names the prior reviewed commit, replacement commit, affected cells/dependencies, obligation and verdict. Pure wording or status updates that change no obligation need no extra review. Scope reduction still needs the Maintainer; Security caps and authorization for further passes remain unchanged.
4. Design found missing during implementation returns the plan to `revising-plan`; it is not appended as a new section.
5. The author returns changed plans from implementation, code review or pre-archive to `revising-plan`. After targeted review and author disposition, use `ready-to-implement` before affected work resumes; retain owed code-review returns and final verification. Example: dropping a security command from Verification cannot use an old ACCEPT; affected work waits for review and any required Maintainer disposition. Reconcile the lifecycle/template rules with this changed-material exception, not unlimited full plan rounds.
6. Use `## Plan amendment review -- <reviewer> -- <date>` for the targeted record, distinct from the original full review. Update the existing board reader and its shipped twin to recognize the linked amendment chain without calling it duplicate original authority. Require one unambiguous applicable review per obligation/revision; missing, conflicting or rejected links leave the advisory stopped, never silently selecting an earlier ACCEPT. Inventory other record consumers, including the audit reporter, and preserve their evidence semantics. No new command or authority source: committed plan records remain authoritative, the board remains advisory.

**B. Records** (Maintainer, 2026-11-12: "Yes to all of it.").
7. Keep every receipt field: Boundary B mode/rationale, tested commit, reviewed range, interpreter, clean pre/post state, command table (Tokens included), plan-specific acceptance commands, non-pass disposition and known omissions. Preserve the underlying check, review, timing and final-commit duties, not only their field names.
8. Target about 700 words in each template's Verification section by removing repetition, not obligations. The plan maps exact replacements to retained duties. This is a clarity target, not a forced cut or a new cap on evidence needed to demonstrate delivery.
9. Replace the closing benefit sentence once in the final record with `**Benefit versus cost**: <verdict> -- <benefit>; cost <measured>; remaining burden <measured>`. Verdicts: `worth it`, `partly`, `not worth it`, `unknown` (with a revisit condition). Use the declared implementation-to-tested range for Git counts and net burden; distinguish aggregate agent elapsed from wall time and report missing values as `unknown`, never zero. Include available decision counts, shipped/always-loaded word changes, test count/runtime and installed-file deltas using existing records, not new collectors. The code reviewer may comment; it adds no pass or Maintainer reply. Apply equivalent wording to light-proposal final records, both proposal templates and lifecycle guidance.
10. `tools/audit_report.py` remains Cairn-only, read-only and advisory. The release-closeout owner runs its existing public command in `docs/release-process.md`. For each archived plan select only the last H2 implementation-verification record and its single unfenced, unquoted labeled line. Never count an earlier line or an example. Missing lines report `no line` without warnings, including historical plans; malformed, duplicate or conflicting current lines report `unknown` with an advisory diagnostic, not a valid verdict or historical absence. List each plan before totals. No archive backfill or release gate.
11. Not adopted: replacing older records with one current record. Evidence accumulates across commits; archiving never rewrites it.

**C. `AGENTS.md`** (and its shipped copy). Replace the freeze-after-implementation rule with the active-plan mutability and change-log rule above, routing detailed obligations to installed collaboration guidance. Preserve archive immutability and append-only historical records. Remeasure both Cairn's and the shipped always-loaded files during implementation: Cairn's current combined cap is 2,000 words; the shipped cap remains 1,500. No claim of a six-word delta is retained.

## Rationale

The records are the largest single repeating cost in plans, and a judgment nobody can count cannot guide anything. Living plans keep the plan true to what is built. A verdict word loosens the "not a score" wording of Decision `036a0495`: it is a label, not a number.

## Alternatives considered

- **Do nothing.** Records stay about a tenth of plan text, plans drift from what is built, and whether ceremony pays stays unknowable.
- **Drop the benefit sentence** (the weight review's first suggestion). The Maintainer chose to strengthen it; dropping loses the only cost evidence.
- **A tool-enforced word cap.** A tool and its tests would weigh more than the words saved. The target lives in the template.
- **Two proposals.** Both halves edit the same templates; the fold-up note called for one.

## Documentation / doctrine surface

Governing layer: paired `AGENTS.md`, plan/proposal templates and collaboration guidance. Keep operative duties in their installed authoritative homes; published lifecycle/plans/contract pages explain them. Software: existing board/twin and Cairn-only audit reporter. Release procedure: the advisory report invocation, not a new release gate.

The design-origin rule and its distinction from incident-triggered evolution are stated in Context. No high-risk classification or gate waiver is manufactured.

## Evidence / verification plan

Falsifiers: the shipped `## Verification` section is not near 700 words by the command above; the next three archived plans lack the line; `audit_report.py` does not list them.

### Tests required

Extend existing public-entry contract tests with small temporary artifacts: the audit command distinguishes last versus earlier records, missing historical lines, duplicate/malformed lines and fenced examples; the board command accepts a complete reviewed amendment chain but stops on missing, conflicting or rejected obligations. A Verification-only weakening and a dependency change must not reuse old approval. Keep existing copy-parity checks and inventory actual readers before editing; no new wording-pin tests or suite trigger. Proposal evidence is not implementation proof.

### Security preflight

- **S1. Inputs and authority:** Authors supply plan text through committed files. Reviewers supply attributed review records; only the Maintainer supplies scope/fence dispensations. Archive text is untrusted input to advisory reporting, not fresh authority.
- **S2. Falsifiers:** Change only Verification to omit a required command; create a broken amendment link or conflicting verdict; put a favorable label in an earlier record or code fence. Each must fail to establish current approval or a valid final verdict through the real consumer.
- **S3. Coverage:** The implementation maps every changed authoritative rule and actual consumer to its existing public-path tests and independent reviews; the release owner runs the advisory aggregate. No claim of exhaustive proof from a happy-path sample.
- **S4. Failure behavior:** Missing or ambiguous approvals stop affected work/advisory selection; invalid report lines remain unknown. Unknown measurements never become zero. Shortening preserves all required checks and omitted coverage disclosures.
- **S5. Residual:** This does not authenticate authors or make local Git history tamper-proof. A cooperating team must honor commit-bound records and scope fences; self-reported costs are evidence with limits, not billing truth. Archived evidence remains immutable by rule, not a new cryptographic mechanism.

Independent scientific check: N/A: no scientific assumption or result touched.

## Signals the change is wrong

- After ten plans the verdicts are all `worth it` or `unknown`: the line has become ritual.
- Median final-record length stays near 250 words after three months.
- An in-place revision hides a scope removal that the change log does not show.
- Plans average more than one return to `revising-plan`: the rule is churn.

## Scope delta

**Scope delta**: preserved. Living active plans, retained evidence, shorter guidance and benefit reporting remain. Review-driven additions specify amendment consumers and failure behavior needed to deliver those outcomes; no new lifecycle stage or cost collector is added.

## Assurance path

**Assurance path**: high-assurance

## Review -- Terra (ordinary, Medium) -- 2026-11-12

Reviewed commit: `98baa07016a4c9a92df70e042252533eee2cbab2`

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**
1. **Should this happen as framed?** The goal is worthwhile, but the doctrine gate and delivery details need repair before decision; see findings 1-3 -- `docs/methodology/rationale.md` > "How the doctrine evolves under evidence".
2. **Best alternative.** Keep append-only evidence and shorten repeated instructions first; living cells and a report add value only if their review and measurement costs remain justified -- `dev/plans/_template.md` > "Verification".
3. **What would show it wrong?** Withdraw or reconsider if a trial of three completed plans cannot reconstruct the reviewed scope and final receipt, or produces verdicts without usable cost evidence -- `dev/strategy/2026-11-06-claude-v07-weight-review.md` > "Agreed direction".

**Steelman.** A current plan can guide implementation while its history preserves accountability; compact receipts and comparable judgments could make the cost of the process visible.

1. **Blocking: doctrine gate not established.** A count of plans and template revisions does not identify recurrence of the same failure shape, its rolling window, or a session-close synthesis. The gate requires one of those or a Maintainer high-risk classification. Close with evidence meeting the actual gate, or the applicable recorded classification -- `docs/methodology/rationale.md` lines 466-487.
2. **Non-blocking: report contract and trigger.** The source specifies the *last* verification record, but item 9 says each archived plan's line; it also does not place the report command in the release procedure. A stale earlier line could be counted and the report never run. Specify last-record selection, missing/malformed handling, a public-entry test with older and multiple-record plans, and the responsible release step -- weight review, "Agreed direction"; `tools/audit_report.py`.
3. **Non-blocking: evidence and current cap.** The source says the 174-plan figures need a rerun; the proposal defers it to the plan, yet uses them to justify a doctrine change. Reproduce against identified committed bytes with the section-selection method, or qualify the claims. The cap is 2,000, not 1,500: correct item C and the summary. At the reviewed commit I measured 903/1,021 verification-section words, 4,004/4,832 template words, and 1,474 words across Cairn's three rules files -- `RULES.md`; `git show` and the proposal's `awk` command.
4. **Non-blocking: transition and review ownership.** Item 3 does not say who requests and performs the targeted look or how a plan resumes when changed after implementation or during code review. Specify the handoff, return state, and preservation of independent and Security Review obligations; include a worked changed-scope example -- `docs/methodology/lifecycle-contract.md` plan transitions.

**Functional prose and audience.** The proposed replacement makes the append-after-implementation rule disappear intentionally; the changed-cell review is its partial safeguard. The installed plan guidance must carry that duty without relying on a Maintainer being present.

**Coverage.** I read the named source note, lifecycle contract, templates, report entry and review rules; I did not reconstruct the unsaved historical measurement, audit every affected document, run a suite, or perform Security Review. The session-start helper could not identify the checkout. This pass exceeds the target to preserve the distinct gate, execution and evidence findings.

## Review -- Sol (Security Reviewer, High) -- 2026-11-12

Reviewed commit: `98baa07016a4c9a92df70e042252533eee2cbab2`

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Steelman.** Keep one usable current specification, accumulated evidence and inspectable ceremony costs without another ceremony. My findings precede the ordinary review; its commit establishes serialization and the current `revising` status only.

**Foundations**
1. **Should this happen as framed?** Yes in purpose, not yet in safeguards; the Maintainer direction supports living plans and retained evidence -- `dev/strategy/2026-11-06-claude-v07-weight-review.md`, "Agreed direction".
2. **Best alternative.** Keep the compact living document, with commit-bound targeted review and immutable history -- `docs/methodology/plans.md`, "Mutability rule".
3. **What would show it wrong?** Earlier approval authorizes weaker verification, or appended review blocks execution; I reproduced the latter -- `tools/board.py:153-181`.

1. **SR1 blocking: revised authority needs binding.** A3 omits Verification/Sequence changes; "whole life" omits archived immutability (`docs/methodology/plans.md:692`). Close by preserving archived text, accepted baselines and Maintainer fences, binding review to old/new commits and affected dependencies, and stopping affected execution until applicable ordinary/security obligations are met. Falsifier: deleting a security command solely from Verification proceeds under old approval.
2. **SR2 blocking: board rejects appended review.** One synthetic plan-review ACCEPT returns `(1, 0)`; appending another raises `duplicate review authority` (`tools/board.py:153-181`, unchanged from reviewed commit). Close with specified record semantics, consumer updates and a public-path check; preserve Security Review caps and authorization beyond them.
3. **SR3 blocking: required preflight missing.** Line 66's N/A contradicts the high-risk trigger in `dev/proposals/_template.md`, "Security preflight". Close with S1-S5 answers covering mutable authority, historical evidence and archive parsing.
4. **SR4 non-blocking: specify retained assurance and measurements.** B6 omits Boundary B mode and acceptance commands (`dev/plans/_template.md:435-453`). Preserve duties, not just fields. Specify cost ranges, unknown versus zero, and duplicate/fenced/malformed verdict handling; malformed current records must not become historical "no line".

**Does any rule weaken or disappear?** A removes freeze/one-round rules intentionally; B has not demonstrated assurance-duty retention.

**Covered:** committed proposal, governing rules, source tracing and positive/adversarial board probes. **Not covered / low confidence:** implementation, future replacement diff, parser execution or suites. Over target to retain distinct closures and evidence. Canonical session-start succeeded after default Python failed repository detection.

## Response -- Codex Sol (High), revising author -- 2026-11-12

- **Terra 1:** Disagree with incident-gate applicability here. Context now cites the explicit design-origin rule in `dev/rules/working-agreements.md`; this is the Maintainer's planned design discussion, not a claimed incident trigger. No recurrence or high-risk bypass is asserted. This interpretation and the reviewer's dissent are visible for the Decision.
- **Terra 2 / SR4:** Specify last-record-only advisory reporting, malformed/duplicate handling, the release owner and command home. Preserve every receipt field and assurance duty. Define ranges and unknown values without adding collectors.
- **Terra 3:** Qualify the unsaved historical measurement, retain the reviewer's identified-commit template measurements, correct Cairn's cap to 2,000 and keep the shipped 1,500 cap. Withdraw the unverified six-word forecast.
- **Terra 4 / SR1:** Limit mutability to active operative cells. Preserve archive/history, accepted scope and fences. Any substantive change in all four cells stops affected work for commit-bound applicable review; name requestor, return states and dependencies. Include the Verification-only counterexample.
- **SR2:** Specify distinct amendment records and compatible existing board/twin consumers, with broken/conflicting chains remaining stopped. Preserve ordinary-review independence and Security caps. This is necessary compatibility work, not a new authority source.
- **SR3:** Replace N/A with S1-S5 and real-entry falsifiers.

The opening summary was reread and revised to match the contract. No implementation, Decision, scope waiver or clearing review is claimed; tests of the future behavior remain implementation work.

### Withdrawn / superseded commitments

Unrestricted "whole life" mutability, Scope/Acceptance-only review triggers, the claim that the board needs no change, the N/A security preflight, the 1,500 Cairn cap and six-word forecast, and current-proof treatment of unsaved measurements are superseded as described above. No accepted objective or assurance duty is withdrawn.

**Elapsed**: approximately 15 minutes for author revision. **Tokens**: unknown.

## Decision -- Maintainer (scribed by Antigravity Gemini 4 Hydrogen) -- 2026-11-12

**Tier**: heavy

**ACCEPTED.**

> "Accept as revised"

This accepts the v0.7 proposal as revised in `08a54320` (living active plans with commit-bound amendment reviews, shorter `## Verification` guidance preserving every receipt field and duty, countable `**Benefit versus cost**` line, and Cairn-only `tools/audit_report.py` summary at release closeout) and affirms the design-origin routing under `dev/rules/working-agreements.md` > "Deciding and asking". New recurring human operations: zero (uses the existing release-closeout invocation of `tools/audit_report.py`).

**Elapsed:** under 1 minute. **Tokens:** unknown.
