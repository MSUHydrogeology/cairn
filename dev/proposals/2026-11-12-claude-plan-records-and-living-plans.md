# Living plans, a shorter verification record, and a benefit-versus-cost line

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy — it edits the authoring templates, `AGENTS.md` and the lifecycle contract, all named high-risk surfaces.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-12
**In brief**: A plan would be edited in place for its whole life, its final verification record would be shorter, and it would end with one labeled line saying whether the work was worth its cost.

## Decision summary

Plans grow by appending, and their verification records are long. The v0.7 weight review measured this and the Maintainer chose two changes: let a plan's working text be revised in place for its whole life (accepted 2026-11-10), and shorten the verification record while making its benefit-versus-cost judgment countable (direction agreed 2026-11-12). This proposal writes both as one doctrine edit. The receipt stays; the Tokens column stays until the meter's conditions are met. The cost is edits to two plan templates, two proposal templates, `AGENTS.md` (six more words), the collaboration guide, three methodology documents, and one Cairn-only report change. This draft has not been sent for review.

## Context

Measured 2026-11-11 (the script was not saved; the plan recounts): 174 plans hold 572 verification sections, 194,944 words, about 10.5% of plan text, median 250 words, longest 3,240. The 8 open v0.7 plans hold 67 appended records, 15,682 words. The plan template grew from 4,004 words (v0.6.1) to 4,832.

Re-counted 2026-11-12 with `awk '/^## Verification/{f=1;next} /^## /{f=0} f' <template> | wc -w`: the `## Verification` section is 903 words in Cairn's template and 1,021 in the shipped one. (The 885 in the weight-review note used a different count.)

The closing benefit sentence (Decision `036a0495`, 2026-11-06) is untested, and no tool reads it: of ten plans archived since, eight closed that same day. Today a plan's operative cells stop being revisable once a chunk begins (plan template, `AGENTS.md`), so later design changes arrive as appended sections.

## Proposal

**A. Living plans** (Maintainer, 2026-11-10: "Accept the living plans. That should really help.").
1. Operative cells (Scope, Sequence, Acceptance criteria, Verification) are revised in place for the plan's whole life. Each revision adds one line to a `Change log`: commit, what changed, why.
2. Reviews, responses, records and quoted Maintainer words stay append-only.
3. A change to scope or acceptance criteria after plan review gets a targeted look at the changed cells, appended as a short plan-review pass. Removing accepted scope still needs the Maintainer.
4. Design found missing during implementation returns the plan to `revising-plan`; it is not appended as a new section.
5. Reconcile three sentences that say "Plan review has one round, never a second" (`docs/methodology/plans.md`, `lifecycle.md`): the targeted look reviews changed cells only and does not reopen the round. Add an `implementing` to `revising-plan` row to `docs/methodology/lifecycle-contract.md`. `tools/board.py` already treats `revising-plan` as author-held; the plan confirms no tool refuses it.

**B. Records** (Maintainer, 2026-11-12: "Yes to all of it.").
6. Keep the receipt: tested commit, reviewed range, interpreter, clean pre/post state, command table (Tokens included), non-pass disposition, known omissions.
7. Cut the template's `## Verification` section to about 700 words by removing repeatable detail, not fields. The plan lists each cut as an exact replacement.
8. Replace the closing benefit sentence, once per plan, in the final record, with one labeled line: `**Benefit versus cost**: <verdict> — <benefit>; cost <measured>; remaining burden <measured>`. Verdicts: `worth it`, `partly`, `not worth it`, `unknown` (with a revisit condition). Cost comes from Git commits, elapsed time, Maintainer decisions asked, and burden in the weight review's units (words added to shipped or always-loaded text, tests added and seconds, files installed in adopter projects). The code reviewer may add a few words agreeing or disagreeing. The same replacement goes into both proposal templates and `docs/methodology/lifecycle.md`.
9. `tools/audit_report.py` (Cairn-only; it ships to no adopter) lists each archived plan's line and counts verdicts in one table at release verification (roadmap item 12). A plan archived before this change counts as "no line", with no warning.
10. Not adopted: "one current record replaces older ones". Evidence builds across commits.

**C. `AGENTS.md`** (and its shipped copy). Replace "Revise a plan's operative cells in place until implementation begins, then append." with "Revise a plan's operative cells in place, with a one-line change log; append only reviews, responses and records." That is six more words: Cairn's three files go from 1,474 to 1,480 against the 1,500 cap.

## Rationale

The records are the largest single repeating cost in plans, and a judgment nobody can count cannot guide anything. Living plans keep the plan true to what is built. A verdict word loosens the "not a score" wording of Decision `036a0495`: it is a label, not a number.

## Alternatives considered

- **Do nothing.** Records stay about a tenth of plan text, plans drift from what is built, and whether ceremony pays stays unknowable.
- **Drop the benefit sentence** (the weight review's first suggestion). The Maintainer chose to strengthen it; dropping loses the only cost evidence.
- **A tool-enforced word cap.** A tool and its tests would weigh more than the words saved. The target lives in the template.
- **Two proposals.** Both halves edit the same templates; the fold-up note called for one.

## Documentation / doctrine surface

Governing layer: `AGENTS.md` and `templates/core/AGENTS.md`. Deliberation layer: `dev/plans/_template.md`, `dev/proposals/_template.md`, `dev/agent_collaboration.md` > "Plans and records". Shipped copies under `templates/core/`. Descriptive layer: `docs/methodology/lifecycle.md`, `plans.md`, `lifecycle-contract.md`.

Rate-limit gate: this is not one incident. It follows a measurement of 174 plans and every template revision since v0.5.0, reviewed by the Maintainer on 2026-11-10 and 2026-11-12.

## Evidence / verification plan

Falsifiers: the shipped `## Verification` section is not near 700 words by the command above; the next three archived plans lack the line; `audit_report.py` does not list them.

### Tests required

One promise changes with a public entry: `python tools/audit_report.py` lists each archived plan's benefit line, counts verdicts, and counts an older plan as "no line" without a warning. One test, run against a temporary archive. The existing copy-parity checks between Cairn's and the shipped templates stay. No wording-pin test is added; the reviewer answers "does any rule weaken or disappear?" against a list of the rules the plan removes or changes.

Security preflight: N/A: no trust boundary added or widened. The templates are on the high-risk list because agents follow them, so the review is usual + Security Review.

Independent scientific check: N/A: no scientific assumption or result touched.

## Signals the change is wrong

- After ten plans the verdicts are all `worth it` or `unknown`: the line has become ritual.
- Median final-record length stays near 250 words after three months.
- An in-place revision hides a scope removal that the change log does not show.
- Plans average more than one return to `revising-plan`: the rule is churn.

## Scope delta

**Scope delta**: preserved. This is the opening text; nothing has been dropped.

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
