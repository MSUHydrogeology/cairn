# A change with no plan: where its code review goes, and when its proposal archives

**Author**: Claude (Strategy)
**Status**: awaiting-review
**Review**: usual
**Plan review**: not required(no plan: one commit, three doctrine files and one template pair, no follow-ups; the change is prose in four areas that share one rule, and the reviewer is asked to challenge that claim)
**Opened**: 2026-10-26
**In brief**: Make the written rules match what already works for a change that needs no plan: build it, have it code-reviewed in its proposal, then archive the proposal.

## Context

**The rules for a change with no plan contradict each other.** Four places say
a "trivial implementation" ships and archives its proposal in one commit:
`doctrine/lifecycle.md:176-178`, `doctrine/plans.md:88-91`,
`doctrine/proposals.md:44-46` and `:316-319`. The same rules require a code
review of every implementation, and `AGENTS.md:332-340` assumes one happens for a
change with no plan, since the code reviewer "rules on whether the tests chosen
were enough". An archived proposal is closed to everything but link
maintenance (`doctrine/proposals.md:142-146`), and a code review needs a commit
to read. So the review cannot follow an archive made in the implementing
commit, and no rule says where it goes instead.

**Practice has already chosen an order, and it works.** On 2026-08-12 the
proposal `boundary-b-bounding-clause` went implement, then an Internal code
review appended to the still-open proposal (`2baa53df`), then a sharpening
commit, then a separate archive commit (`68f74315`). On 2026-10-26 two
proposals followed the same order: `writing-for-the-reader` (implemented
`4a88ca82`, reviewed `9db7f3b5`, archived `68268b4b`) and
`check-cairn-deleted-files` (implemented `9ec53a43`, reviewed `2193014d`,
archived `68268b4b`). Following the written rule would have left both reviews
with nowhere to be recorded. I told the Maintainer the opposite for a few hours
on 2026-10-26, and had a memory note saying so; it was the rule that was wrong.

**The header that says "no plan" does not say it.** `Plan review: not
required(...)` is defined as "a plan opens and skips its own review"
(`doctrine/lifecycle.md:298-305`, `doctrine/plans.md:52-54`). Eight archived
proposals carry that value. One has a plan under a matching name, one was
superseded, and six have no plan file under a matching name (a name match, not
proof). Four of those six show no `## Code review` section in the proposal; I
did not look for a review anywhere else. So the value is used to claim "no
plan", and nothing makes the author show the claim. The claim was wrong on
2026-10-26: the `check-cairn-deleted-files` change touched scripts, shipped
copies, a doc and a test, and left a step for the Maintainer to run (a gate
re-anchor). That meets two of the four triggers in `doctrine/plans.md:176-186`
("touches multiple files / areas" and a follow-up needing a home), and
`doctrine/plans.md:194` says "When in doubt, open the plan."

## Proposal

Three changes. All are prose; none adds a tool, a header value or a status.

1. **A change with no plan: build, review, then archive.** For an accepted
   proposal that meets all three skip conditions of the plan triage rule
   (`doctrine/plans.md:189-192`):
   * The implementing commit ships the work and records its Boundary B result
     in its body (`AGENTS.md:332-340`, unchanged). It does not archive the
     proposal.
   * A code reviewer who is not the implementer appends a `## Code review`
     section to the still-open proposal. The author answers it with a
     `## Code review response` section, using the code-review-Response grammar
     that already exists (`doctrine/proposals.md:467-470`). The proposal's
     status stays `accepted` throughout; no new status.
   * The proposal archives in its own commit, after the review has closed, with
     the link maintenance that already applies. This is the plan-archive
     precondition applied to a change with no plan: no archive until a code
     review has occurred, and the archive commit is distinct from the
     implementing commit.
   * If the work or the review shows the change was not trivial after all, a
     plan opens then, and the plan-open commit archives the proposal as it does
     today.
2. **Say "no plan" as a claim a reviewer can test.** A proposal that expects to
   need no plan writes its `Plan review` line as
   `not required(no plan: <how each of the three skip conditions holds>)`, and
   the sentence in `doctrine/proposals.md:191-203` gains a clause: bare
   `not required` describes a plan that skips its review, and a "no plan" claim
   without the three conditions shown is a review finding, like an unfilled
   slot. The Decision already ratifies the line.
3. **Make the other statements agree.** The sentences listed below change so
   that none of them says the implementing commit archives.

Edits, by file:

| File | Where | Change |
| --- | --- | --- |
| `doctrine/lifecycle.md` | 176-178, 212-219 | "Trivial vs. non-trivial": the no-plan path is build, code review in the proposal, then archive |
| `doctrine/proposals.md` | 20-31 (diagram), 42-46, 82-85, 126-130, 183-190, 316-319, 343-346 | the same order; the "no plan" `Plan review` form |
| `doctrine/plans.md` | 88-91, 131-134, 690-691 | "Trivial accepts collapse implementation + proposal-archive" becomes the new order |
| `doctrine/lifecycle-contract.md` | one row after the Decision rows | an accepted proposal with no plan archives only after a code review |
| `dev/proposals/_template.md` and `templates/core/dev/proposals/_template.md` | the `Plan review` header line | the same "no plan" form, in one sentence |

## Rationale

The order is the one practice settled on, and it needs no new status, header
value, file or tool. The stated rule and the required review cannot both be
followed; this removes the conflict at the smallest cost, by fixing the rule
that is wrong. The "no plan" form puts the claim where the reviewer and the
Maintainer already look, so a wrong claim like 2026-10-26's is a visible finding
instead of something nobody tests.

## Alternatives considered

* **Do nothing.** Each no-plan change improvises the order, as three have. The
  cost is a rule a careful agent cannot follow, and the Maintainer or an agent
  spends attention each time reconciling it. Four of six no-plan proposals show
  no code review in their file, which may be a cost or may be reviews recorded
  elsewhere; the reviewer is asked to check.
* **Always open a plan; drop the no-plan path.** The simplest rule, with one
  home for execution and review. It loses on cost: a plan file, a status
  lifecycle and an archive commit for a one-commit prose edit. Restraint is a
  design centre (`dev/strategy/2026-05-14-claude-human-ai-team-development-framework.md`,
  "Restraint as design center"). It is a fair choice if the Maintainer judges
  that agents will keep misjudging "trivial"; the proposal's second change is the
  cheaper answer to that.
* **Keep archiving in the implementing commit and record the review in a new
  place** (the commit body or a file under `dev/reviews/`). It adds a second home
  for reviews, outside the artifact the board reads and the append-only record
  protects.
* **A checker that tests the "no plan" claim** (count files and areas touched).
  Cairn's tools warn and do not block, a count cannot judge "one area", and the
  Maintainer's attention is the scarce part. A reviewer reading the header already
  catches it.

## Documentation / doctrine surface

Doctrine and the shipped proposal template; routed by
`docs/DOCUMENTATION_PLAN.md`. The doctrine files are Cairn's published
methodology and are not installed into adopters' trees. The proposal template is
shipped, in `templates/core/dev/proposals/_template.md`, and reaches existing
installs through the ordinary three-way upgrade merge. No `docs/` page, `AGENTS.md`
or `CHANGELOG.md` text changes beyond one changelog entry when the change lands.

## Evidence / verification plan

* **Tests that read the files.** Eight tests read `doctrine/lifecycle.md`, two
  read `doctrine/proposals.md`, four read `doctrine/plans.md` and one reads
  `doctrine/lifecycle-contract.md` (counted by `git grep -l` on 2026-10-26; the
  implementer recounts by content). All stay green and unedited. The change
  rewrites sentences, so the implementer runs each reader and reports counts
  with the interpreter.
* **Consistency.** After the edit, `git grep` for "trivial-implementing",
  "trivial accepts" and "implemented and the proposal archived" over the
  doctrine finds only sentences that agree with the new order. The grep is run
  against a sentence known to be present first.
* **A trial on the real case.** Read the new text as an agent about to
  implement a one-commit accepted proposal with no plan, and write the sequence
  of commits it implies. It must equal the sequence `check-cairn-deleted-files`
  followed. If it does not, the text changes first.
* **Gates.** `python scripts/claim_check.py` and `python scripts/link_check.py`
  on each changed file, `python scripts/check_cairn.py`, and
  `python scripts/quality_gate.py --sub neutrality --sub redundancy` with 0
  neutrality failures.
* **What would show it wrong.** A no-plan change whose review has nowhere to go
  under the new text; or two files that still disagree on when the archive
  happens.
* **Security preflight.** N/A: no trust boundary added, moved or widened.
* **Independent scientific check.** N/A: no scientific assumption or result
  touched.

## The rate-limit gate

The gate (`doctrine/rationale.md` > "How the doctrine evolves under evidence")
asks for recurrence, not a single incident. The same order was improvised on
2026-08-12 and twice on 2026-10-26. The header misuse is visible in six
archived proposals. Both are in the record cited above.

## Signals the change is wrong

* **Agents open plans for one-commit prose edits to avoid the "no plan"
  sentence.** The claim form is too heavy; drop it to the old header.
* **Reviews of no-plan changes still appear outside the proposal.** The home is
  not being found; point the implementing commit's body at it.
* **A proposal archives before its review in a later change.** The new order is
  being ignored; look at who briefed the implementer.

## Scope delta

**Scope delta**: preserved. This is the opening contract.

## Assurance path

**Assurance path**: high-assurance. The change edits `doctrine/` and a shipped
template, which the project names as mandatory high-assurance surfaces. It touches
no engine, contract, trust root or licence file, so no Security Review is owed.
The doctrine files are not frozen in the gate manifest and the template is not
either (checked in `bootstrap/tests/fixtures/gate_manifest.json`; the
implementer rechecks), so no re-anchor is owed.
