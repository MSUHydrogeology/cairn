# Living plans, a shorter verification record, and a benefit-versus-cost line

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-review
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
