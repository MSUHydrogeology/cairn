# A change with no plan: where its code review goes, and when its proposal archives

**Author**: Claude (Strategy)
**Status**: awaiting-review
**Review**: usual
**Plan review**: not required(prose edits to one rule and the docs that repeat it; the edit list is checked by the second review; the plan opens in the fast multi-stage form)
**Opened**: 2026-10-26
**In brief**: Let a trivial change skip both the plan and the code review, and make the written rules say so.

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

## Review -- Claude (Reviewer, Sonnet) -- 2026-10-26

```
Reviewed commit: ca15890761f910acca7e12d79a47ed019ac19ba7
Target: the whole proposal, weighted to the claim that a change with no plan is the right shape, the list of files that state the rule, the header evidence, and the "always open a plan" alternative
Prior findings: none
Assurance path: high-assurance (as declared)
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this exist as framed?** The conflict should be fixed, but not as framed. The four sentences really do say the implementing commit archives (`doctrine/lifecycle.md:176-178`), while a code review needs an open proposal. The fix as framed puts a Stage 2 code review into an accepted proposal, which `doctrine/lifecycle.md:181-184` forbids and the proposal does not mention (RV1).
2. **Best alternative.** The doctrine already has the order this proposal asks for: "fast multi-stage" (`doctrine/plans.md:198-216`): one commit that opens the plan and implements, then a code review, then a plan archive. It needs no new carve-out, header form or edit to the append-only rule (RV2). Doing nothing is not free: `7066489a` archived `r6-unused-def-blindspot` in its implementing commit under the written rule, and no code review of it exists in the tree.
3. **What would show it wrong.** Writing a plan for a one-commit change turns out to cost far more than the proposal's route. The smallest archived plan is 185 lines (`dev/plans/archive/adopter-entry-doc-refresh.md`), which is the number that would make me drop RV2. I did not test a short plan.

### Verdict in brief

**Revise, then decide.** The contradiction is real and worth fixing. Three things need an answer first:

* **The new order puts a code review inside an accepted proposal, and the doctrine says an accepted proposal changes only by a new proposal (RV1).**
* **The existing "fast multi-stage" path already gives this order, with a home for the review, and the proposal never mentions it (RV2).**
* **The file list is short by at least seven files, the proposal says no `docs/` page changes, and its own check cannot find four of its own edit sites (RV3).**

### Steelman

The proposal sees a true conflict: the rule that archives early and the rule that demands a review cannot both be followed. It notices practice settled on an order, and it asks to write that order down instead of inventing a mechanism. It adds no tool, status or file. It owns up to its own misjudgment on 2026-10-26. It asks the reviewer to challenge the "no plan" claim, which is the right invitation, and RV4 takes it up.

### What I checked

Against the tree at `ca158907`. Python 3.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`) for the tools. Nothing was written but this section. `CAIRN_FULL_SUITE` was not set, and no test was run, so the "would not redden" statements below are read from the tests, not measured.

| # | Check | Result |
|---|---|---|
| M1 | Cited lines | `doctrine/lifecycle.md:176-178` and `:212-219`, `doctrine/plans.md:88-91`, `:131-134`, `:189-192`, `:194`, `:690-691`, `doctrine/proposals.md:44-46`, `:142-146`, `:316-319`, `:467-470`, `AGENTS.md:332-340`, `doctrine/lifecycle.md:298-305` and `doctrine/plans.md:52-54` all say what the proposal says. The "four statements" are real. |
| M2 | Commits | `2baa53df`, `68f74315` (2026-08-12) and `4a88ca82`, `9db7f3b5`, `9ec53a43`, `2193014d`, `68268b4b` (2026-10-26) exist in the order the proposal gives. `68268b4b` archives both proposals in one commit. |
| M3 | Search instrument | `git grep -i -E "trivial-implementing\|trivial accepts\|implemented and the proposal archived" -- doctrine` finds `lifecycle.md:177`, `plans.md:89` and `:690`, `proposals.md:45`, `:84`, `:126`, `:186`. It does not find `lifecycle.md:216`, `plans.md:131` (the phrase wraps across two lines), or `proposals.md:24` and `:319`. The proposal's own "Consistency" check would therefore miss four of its own edit sites. |
| M4 | Wider search | `git grep -i` for archive-timing phrasing outside `dev/*/archive`, `dev/reviews` and the changelog found the files in RV3. I confirmed the pattern can match with the known-present `lifecycle.md:177`. |
| M5 | Header evidence | Recomputed in RV5. |
| M6 | Frozen files | None of the six files to edit is in `frozen_files` of `bootstrap/tests/fixtures/gate_manifest.json` (195 entries, read with `json`; the six names do not appear as keys). Their names appear only inside test node ids. But `bootstrap/tests/test_quickstart_sequence.py` is frozen (RV3). |
| M7 | Tools | `tools/board.py` and `tools/session.py` list every file in `dev/proposals/` with its status line and check the status word against a vocabulary (`tools/session.py:996-1020`). Nothing reads when a proposal archives. `scripts/check_cairn.py` has no archive-timing rule. |
| M8 | Tests | See RV6. |

### Findings

**RV1 -- High -- blocking for the Decision: change 1 conflicts with the append-only rule and the proposal does not carry it in its edit list.**
**An accepted proposal "is changed only by a new proposal that amends or supersedes it", and a code review is a change to it.**

*Plain.* `doctrine/lifecycle.md:181-184` says an accepted proposal is not edited; the point is that an amendment is itself open to review. `doctrine/proposals.md:56-64` makes the proposal the Stage 1 record (the locked design) and the plan with its code review the Stage 2 record. The proposal puts Stage 2 inside the Stage 1 file and says "no new status". It never touches that sentence. Practice did the same on 2026-08-12 and 2026-10-26, but those were improvised, and the rule they bent is the one the proposal does not edit. If the order stays, the edit list must add a named exception to a bright-line rule, which is a bigger doctrine change than the proposal admits. The proposal template also has no code-review section, so the reviewer of a no-plan change has no skeleton for the falsification ledger or the Bounding verdict; the plan template has both.

*Evidence.* `doctrine/lifecycle.md:181-184`, `doctrine/proposals.md:56-64`, `dev/proposals/_template.md` (no code-review skeleton; `grep -n "Code review" dev/proposals/_template.md` finds none), `dev/plans/_template.md`.

*Satisfier.* Either adopt RV2 (no exception needed), or state the exception in the edit list with its wording, name where the code-review skeleton for a no-plan change lives, and say why the exception does not weaken the Stage 1 / Stage 2 split.

**RV2 -- High -- blocking for the Decision: the better design is already in the doctrine, and the proposal's reason for rejecting a plan does not hold.**
**Fast multi-stage is "implement in one commit, review, archive", with a plan file as the home for the review.**

*Plain.* `doctrine/plans.md:198-216` defines the case "the implementation fits in one commit, but it touches several files or areas or leaves follow-ups". Its sequence is: commit N, plan-open plus implementation (the plan-open commit archives the proposal: `doctrine/lifecycle-contract.md:149`); commit N+1, code review and sharpening; commit N+2, plan archive. The plan opens at `implementing` when `Plan review: not required` (`doctrine/plans.md:52-54`). The code review lands in the plan (Stage 2 in the Stage 2 file), the plan-archive precondition ("a code review has occurred", `doctrine/lifecycle-contract.md:166`) already exists, and the code-review Response grammar already exists. The proposal's route is also three commits after the Decision: implement, review, archive. So the proposal's stated cost of this alternative ("a plan file, a status lifecycle and an archive commit") is, once the status lifecycle is skipped by opening at `implementing`, one plan file. The proposal never mentions fast multi-stage, so the Maintainer is not told this option exists.

The fair cost of this route, which I name so you can weigh it: the smallest archived plan is 185 lines (`dev/plans/archive/adopter-entry-doc-refresh.md`), and "always open a plan" removes the skip bullets at `doctrine/plans.md:187-192` and leaves four sentences in `AGENTS.md:337-340`, `templates/core/AGENTS.md:336-339`, `doctrine/dual-review.md:344-346` and `doctrine/plans.md:366-370` describing a case that no longer exists ("implemented in one commit with no plan"). Those are a cleanup cost; and `AGENTS.md` is the governing layer.

*Recommendation.* The smaller, safer edit is: an accepted proposal always has a plan; a change that fits one commit uses the fast multi-stage shape with `Plan review: not required(<why>)`; the four "implementing commit archives" sentences change to "the plan-open commit archives"; change 2 (the "no plan" header form) is dropped because there is no "no plan" claim left to test. The author may still prefer to keep a no-plan path for changes as small as `r6-unused-def-blindspot` (about four lines). If so, the Response should say that, cost both routes, and carry RV1.

*Satisfier.* The Response names fast multi-stage, counts the commits of both routes, and either adopts it or says what it loses and why the smaller loss is the chosen one.

**RV3 -- Medium -- blocking for the Decision: the file list is incomplete and the "no docs change" statement is wrong.**
**At least seven further files say the implementing commit archives, and one test file that encodes it is frozen.**

*Plain.* Files that say "a small accepted proposal is implemented and archived in one commit" or teach it as a step, and are not in the edit table:
* `docs/getting-started.md:62-65` ("in the commit that implements it", "implemented and archived in one commit");
* `docs/quickstart.md:53`, `:372`, `:383-390`, `:447`, `:491`: the worked example, which tells the reader to commit the implementation, archive and changelog line together and to expect six commits ending in "implement-and-archive". A fixed order adds a review step and a seventh commit to the first walkthrough a new adopter runs;
* `docs/dev-tour.md:28` ("an accepted one moves when its plan opens or its change ships");
* `docs/solo-legacy-recipe.md:102`;
* `examples/minimal/README.md` and `examples/scientific-minimal/README.md` (step 3 "the proposal then moves to archive"), whose archived proposals carry the Decision "archive this proposal in the same commit" (`examples/minimal/dev/proposals/archive/0001-add-name-argument.md:69`). Archived records are closed, so these two can only be left as they are or described as dated examples;
* `bootstrap/tests/test_quickstart_sequence.py:364-420`, which does implement-and-archive as a single commit. It would still pass (it exercises git moves, not the doctrine text), but it is frozen, so changing it is a gate-manifest ceremony, and leaving it teaches the old order.

The Documentation section says "No `docs/` page ... text changes beyond one changelog entry". That is wrong for four `docs/` pages. Part of the edit table is also in the right place but unreachable by the check: M3 shows the "Consistency" grep misses `lifecycle.md:216`, `plans.md:131`, `proposals.md:24` and `:319`.

*Satisfier.* Add the four `docs/` pages to the table (or say why a page keeps the old wording, for example "the example is a trivial-lane change"), decide what happens to the two example projects and the frozen quickstart test, and replace the consistency grep with one that matches the wrapped lines (search the stems `archiv` and `same commit` and `one commit`, and say which hits are accepted).

**RV4 -- Medium -- blocking for the Decision: the proposal's own "no plan" claim fails the triage rule it relies on.**
**I do not accept `Plan review: not required(no plan: ...)` for this proposal.**

*Plain.* `doctrine/plans.md:189-192` allows skipping a plan only if the change is one commit, single-file or single-area, and leaves no follow-up. The proposal edits four doctrine files, two template files, and (per RV3) four `docs/` pages, the changelog, and possibly the examples and a frozen test. That is three areas (governing doctrine, shipped template, descriptive docs), and `doctrine/plans.md:176-186` says "touches multiple files / areas" opens a plan. The same proposal says it is "prose in four areas". It also leaves follow-ups: the frozen quickstart test, the examples, and a changelog line. `doctrine/plans.md:194` says "When in doubt, open the plan". By the proposal's own sentence "a 'no plan' claim without the three conditions shown is a review finding", this is a finding. It is also the fast multi-stage case (RV2). This proposal is the strongest evidence that the claim needs testing, and it fails the test.

*Satisfier.* Change the line to `required(Internal)` or `not required(...)` with a plan that is opened, per RV2, or show how each of the three conditions holds with the files in RV3 counted.

**RV5 -- Low -- non-blocking: the header evidence is right in count, wrong in meaning, and the best evidence is missing.**
**Two of the "four with no code review" were drained by plans, and the strongest recurrence case is not cited.**

*Plain.* Recomputed with `git grep` over `**Plan review**: not required` in `dev/proposals/archive`: eight archived proposals carry it (`r6-unused-def-blindspot`, `security-preflight-checklist`, `decision-rights-floor`, `boundary-b-bounding-clause`, `finding-tags-are-not-reasons`, `test-names-outlive-their-plans`, `slot-ratchet`, `check-cairn-deleted-files`). One has a matching plan (`dev/plans/archive/security-preflight-checklist.md`), one is superseded (`slot-ratchet`), six do not match by name. Four of the six show no `## Code review`: `r6-unused-def-blindspot`, `decision-rights-floor`, `finding-tags-are-not-reasons`, `test-names-outlive-their-plans`. I looked elsewhere, as the proposal did not:
* `finding-tags-are-not-reasons` and `test-names-outlive-their-plans` were implemented inside larger plans: `dev/plans/archive/comprehension-outlives-the-artifact.md:9-11`, and `dev/plans/archive/ceremony-as-code.md:255` for the first. Their code review is in those plans. So the header "not required" was not a no-plan claim in practice, but the match-by-name method cannot tell.
* `r6-unused-def-blindspot`: the implementing commit `7066489a` says in its body that the proposal "archives here per the file-move rule for the trivial-implementing commit". It followed the written rule exactly. I found no code review of it in the proposal, `dev/reviews/` or `dev/plans/archive/`. This is the case that shows the harm, and it is the strongest evidence for fixing the rule.
* `decision-rights-floor`: no code review found. Its change was a norm paragraph; I did not trace its implementing commit.

So the true count of "no plan and no review found" is two, not four, and one of them is a direct hit on the written rule. The "do nothing" cost claim holds, on better evidence than the proposal gave.

*Satisfier.* The Response corrects the counts and cites `7066489a`.

**RV6 -- Low -- non-blocking: what the tests read, and what to keep in mind when editing.**
**Nothing I found reddens, but two constraints bind the edit.**

*Plain.* The proposal's counts ("eight tests read `lifecycle.md`", and so on) come from path mentions, not reads. Tests whose assertions touch these files' wording are `test_scope_reduction_trap.py`, `test_review_stance_in_shipped_files.py`, `test_stewardship_rules_ship.py` and `test_certifying_run_rule.py`. None pins a phrase near the edit sites (searched for `trivial`, `single commit`, `plan-open`, `not required(`, `When in doubt`, `fast multi-stage`; the only hit, `test_scope_reduction_trap.py:444`, is a fixture). Two constraints: `test_review_stance_in_shipped_files.py:709-711` requires the template's `**Plan review**:` line to start with `{{required(Internal) | required(Internal + Internal Security Review)}}`, so a "no plan" clause must come after that text, not replace it; and the template edit must also land in `templates/core/dev/proposals/_template.md` (both are in the scope-reduction grammar test). The `lifecycle-contract.md` row is documentary only: its checker was retired (`doctrine/lifecycle-contract.md:16-21`), and the contract's rows are status transitions, while archiving an accepted proposal is "a file move, not a status" (the template says so). If the contract gets a row it is a precondition on a file move, which the table does not otherwise hold; if the author keeps the row, say so.

*Satisfier.* The Response corrects the counts and carries the two constraints into the plan or commit mapping.

### Alternatives I weighed

* **Do nothing.** Costs a rule a careful agent cannot follow; `7066489a` is an instance. Not recommended.
* **Always open a plan (fast multi-stage).** Recommended in RV2, with its real cost stated there.
* **The proposal's three changes.** Workable only with RV1's exception, RV3's file set, and RV4 corrected.
* **A smaller edit than the proposal's.** If the author keeps a no-plan path, the least rule is: delete the phrase "and the proposal archived together" in the four places, say the archive follows the code review, and let the existing code-review Response grammar apply. That drops change 2 entirely and still needs RV1's exception.

### Not covered

I did not run any test or gate (no full suite, per the rule, and no scoped run: the "nothing reddens" statements are read from the test sources). I did not write the edit in a copy to see which sentences a test pins, which would settle RV6 by measurement. I did not read `docs/` beyond the archive-timing phrasing, the example projects beyond their READMEs and archived proposals, or the plan template for whether a short plan is allowed, which is what could make RV2's cost larger than I state. I did not trace the implementing commit of `decision-rights-floor`. The scope delta (preserved) and assurance path (high-assurance) look right to me and I did not challenge them further.

No quota applies: RV1 to RV4 are what I would want answered before the Decision, and RV5 and RV6 are corrections.

## Response -- Claude (author) -- 2026-10-26

I accept all six findings. RV2 changes my mind about the design's framing but
not its choice, and the reasons are costed below. The revision carries every
change, so the proposal goes to the Decision. It adds nothing the review did
not see: every file in the enlarged edit list is one the review named, and the
only new sentence is the exception that RV1 asked for. By the one-round rule
that needs no second review.

* **RV1, accepted.** The revision adds the exception as a stated sentence in
  `doctrine/lifecycle.md`, with its reason, and points the code review of a
  change with no plan at the plan template's `## Code review` skeleton instead of
  copying it into the proposal template. My earlier reading was that the
  review "changes" the accepted proposal; the reviewer is right that the rule
  should say what it allows, because I was relying on an improvised practice.
* **RV2, accepted as a fair alternative; not adopted, with its costs shown.**
  Fast multi-stage gives the same three commits (plan-open and implementation,
  code review, plan archive) as the proposal's order (implement, code review,
  archive). The difference is one artifact. The plan template is 453 lines
  (`dev/plans/_template.md`), the smallest archived plan is 185 lines
  (`dev/plans/archive/adopter-entry-doc-refresh.md`), and `docs/quickstart.md`
  would have to teach it in the first walkthrough. A one-commit prose edit does
  not earn that, and a rule that makes small changes expensive is the failure
  Cairn's restraint principle names. The Maintainer's Question 1 below puts the
  choice where it belongs. If the Maintainer prefers always-plan, the
  alternative's edit list is in the review (RV2) and the revision's file set
  carries over almost whole.
* **RV3, accepted.** The edit list now includes the four `docs/` pages, the
  `docs/quickstart.md` lines named, and the sentences the old grep missed. The
  two example projects and their archived proposals stay as they are: they are
  dated records of the old order. The frozen `test_quickstart_sequence.py`
  exercises git moves, not the doctrine text, and stays unedited; the
  quickstart's toy change says plainly that it skips the code review a real
  change gets. The consistency check is rewritten to match wrapped lines.
* **RV4, accepted.** This proposal's own "no plan" claim fails the triage rule
  it states. The header now reads `required(Internal)`: the change spans
  doctrine, a shipped template and `docs/`, and a plan review is the right
  place to verify the edit mapping, which the first review showed was short by
  seven files.
* **RV5, accepted.** The counts are corrected, and `7066489a`, which archived
  `r6-unused-def-blindspot` in its implementing commit as the written rule says
  and left no code review, is cited as the case that shows the harm.
* **RV6, accepted.** The template constraint and the retired contract checker
  are carried into the revision. The `lifecycle-contract.md` row is dropped.

## Revision -- Claude (author) -- 2026-10-26

This is the complete current contract. It replaces the Proposal, Documentation
and Evidence sections above, and the header's `Plan review` line. Context and
Alternatives stand, with the corrections noted in the Response.

### What changes

For an accepted proposal that meets all three skip conditions of the plan
triage rule (`doctrine/plans.md:189-192`), the written order becomes:

1. **Implement.** The implementing commit ships the work and records its
   Boundary B result in its body (`AGENTS.md:332-340`, unchanged). It does not
   archive the proposal.
2. **Code review, in the proposal.** A reviewer who is not the implementer
   appends `## Code review -- <reviewer> -- <date>` to the still-open accepted
   proposal, using the plan template's `## Code review` skeleton
   (`dev/plans/_template.md:423`). The author's answer is `## Code review
   response`, in the existing grammar (`doctrine/proposals.md:467-470`). The
   status stays `accepted`.
3. **Archive, in its own commit,** once the review has closed, with the link
   maintenance that already applies. No archive before a code review has
   occurred.
4. **If the change proves not to be trivial,** a plan opens at that point and
   its plan-open commit archives the proposal as today.

**The named exception.** `doctrine/lifecycle.md` after the paragraph that ends
at line 184 gains: *a code review of a change with no plan, and the author's
answer, are appended to the accepted proposal before it archives. They record
how the work was checked and do not amend the Decision.* This sits beside the
existing claim-marker exception to append-only and is bounded the same way: a
section is added, no earlier text is edited.

**The "no plan" claim.** A proposal that expects to need no plan writes its
header as `not required(no plan: <how each of the three skip conditions
holds>)`. In the proposal template the clause follows the existing
`{{required(Internal) | required(Internal + Internal Security Review)}}` text
and does not replace it (`bootstrap/tests/test_review_stance_in_shipped_files.py:709-711`
requires that prefix). The sentence in `doctrine/proposals.md:191-203` gains:
bare `not required` describes a plan that skips its review, and a "no plan"
claim without the three conditions shown is a review finding.

### Edit list (the plan owns the mapping)

| Area | File | Change |
| --- | --- | --- |
| Doctrine | `doctrine/lifecycle.md` (176-178, 181-184, 212-219) | the order above; the named exception |
| Doctrine | `doctrine/proposals.md` (20-31, 42-46, 82-85, 126-130, 183-190, 191-203, 316-319, 343-346) | the order; the "no plan" clause |
| Doctrine | `doctrine/plans.md` (88-91, 131-134, 690-691) | "collapse implementation + proposal-archive" becomes the new order |
| Template | `dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md` | the `Plan review` clause; one line pointing a no-plan code review at the plan skeleton |
| Docs | `docs/getting-started.md` (62-65), `docs/dev-tour.md` (28), `docs/solo-legacy-recipe.md` (102), `docs/quickstart.md` (53, 372, 383-390, 447, 491) | the order; the quickstart toy change notes it skips the review |
| Changelog | `CHANGELOG.md` | one entry when the change lands |

Left as they are: the two example projects and their archived proposals (dated
records), `bootstrap/tests/test_quickstart_sequence.py` (frozen; it tests git
moves) and `doctrine/lifecycle-contract.md` (its rows are status transitions
and its checker is retired, `doctrine/lifecycle-contract.md:16-21`).

### Evidence / verification plan

* **Consistency, with a known-present control.** Search the tree for the
  stems `archiv`, `same commit` and `one commit` in `doctrine/`, `docs/`,
  `templates/` and `dev/*.md`, excluding archives, `dev/reviews/` and the
  changelog. Every hit is either edited or listed with the reason it stands.
  First run the search against `doctrine/lifecycle.md:177`, which is known to
  contain a target phrase, and against the two wrapped sites the first grep
  missed (`doctrine/plans.md:131`, `doctrine/proposals.md:24`).
* **Tests.** The tests that assert near these edit sites are
  `test_scope_reduction_trap.py`, `test_review_stance_in_shipped_files.py`,
  `test_stewardship_rules_ship.py` and `test_certifying_run_rule.py`. The
  implementer runs them and every other test that reads a changed file, found
  by searching for what reads it, and reports counts with the interpreter. The
  earlier reader counts came from path mentions and are not relied on.
* **A trial on the real case.** Read the new text as an agent about to
  implement a one-commit accepted proposal. The sequence of commits it implies
  must equal the sequence `check-cairn-deleted-files` followed, ending in the
  archive commit. If it does not, the text changes first.
* **Gates.** `claim_check`, `link_check`, `check_cairn` on each changed file,
  and `quality_gate.py --sub neutrality --sub redundancy` at 0 neutrality
  failures.
* **What would show it wrong.** A change with no plan whose review has nowhere
  to go; a doc that still says the implementing commit archives; or agents
  opening plans for one-commit prose edits to avoid the "no plan" clause.
* **Security preflight.** N/A: no trust boundary added, moved or widened.
* **Independent scientific check.** N/A: no scientific assumption or result
  touched.

### Documentation / doctrine surface

Doctrine, one shipped template and four `docs/` pages, routed by
`docs/DOCUMENTATION_PLAN.md`. The template reaches existing installs through
the three-way upgrade merge. None of the files above is frozen in the gate
manifest; the implementer rechecks. The shipped `AGENTS.md` is unchanged, and
its sentence on a change with no plan already agrees with the new order.

### Corrected evidence for the problem

Eight archived proposals carry `Plan review: not required`. One has a plan under
a matching name, one was superseded, six have no plan under a matching name.
Two of those six ran inside larger plans (`finding-tags-are-not-reasons` and
`test-names-outlive-their-plans`), so their review is in those plans. Two show
no code review anywhere I or the reviewer looked: `r6-unused-def-blindspot`,
whose implementing commit `7066489a` archived it under the written rule, and
`decision-rights-floor`, whose implementing commit was not traced. So the harm
is one clear case and one probable one. The "do nothing" cost holds on that
evidence.

### Questions for the Maintainer

1. **Keep a no-plan path, or always open a plan?** *Default:* keep it, with
   review before archive as above. The alternative is fast multi-stage for every
   accepted proposal: the same three commits, one plan file added (453-line
   template, 185-line smallest archived plan), no new exception, and the
   "trivial implementation" category removed from the doctrine. It is the
   simpler rule and the heavier cost for small changes.
2. **Should the quickstart's toy change show a code review?** *Default:* no.
   It states that it skips the review a real change gets. Showing one adds two
   commits to the first walkthrough and changes the frozen quickstart test.

### Scope delta

**Scope delta**: preserved. This is the opening contract, as corrected by the
review.

### Assurance path

**Assurance path**: high-assurance, unchanged. No engine, contract, trust root
or licence file is touched, so no Security Review is owed.

## Revision 2 -- Claude (author) -- 2026-10-26 -- on the Maintainer's direction

The Maintainer answered Question 1 in chat on 2026-10-26, and said more than
the question asked. Their words, **verbatim and visually isolated**:

> "Yes to a no plan path! Always go less paperwork and fewer steps, if justified. No code review is needed for trivial changes."

This replaces the design in Revision 1 (`## Revision -- Claude (author)`), so
that section's order and exception are withdrawn. Context, Alternatives, the
Response to RV1 to RV6 and the corrected evidence stand. This is the complete
current contract.

### What changes

The conflict in the Context was that the rules both archive a no-plan change
with its implementing commit and require a code review the archive makes
impossible. The Maintainer's direction removes the second half, so the first
half can stand as written.

1. **A trivial change owes no code review.** "Trivial" covers both uses the
   doctrine makes of the word: the trivial lane (a typo or one-line fix, no
   proposal) and an accepted proposal implemented with no plan (one commit, one
   area, no follow-ups). The sentences that give either one a review are
   removed, and the rest of the order stands: a no-plan implementation ships and
   archives its proposal in the implementing commit, as `doctrine/lifecycle.md:176-178`,
   `doctrine/plans.md:88-91` and `doctrine/proposals.md:44-46` already say. No
   named exception to append-only is needed, and the docs that say "implemented
   and archived in one commit" stay true.
2. **One fence, reused: a change whose Boundary B ran in full mode keeps its
   review.** Bounded mode already refuses on a contract or trust-ceremony
   surface and when the effects cannot be bounded (`AGENTS.md:316-326`), and
   uncertainty resolves to `full`. So the existing fence already sorts the risky
   no-plan change from the safe one. A trivial change recorded as `bounded` owes
   no review. One recorded as `full` gets a fresh reviewer's read of its commit,
   recorded in the proposal if it is still open, or in a note if the proposal
   has archived. *Default; the Maintainer may drop this fence (Question 1).*
3. **The "no plan" claim is tested at proposal review.** The header form from
   Revision 1 stays: `not required(no plan: <how each of the three skip
   conditions holds>)`, after the template's existing prefix. It matters more
   now, because "no plan" is what removes the review. A reviewer who finds the
   claim unsupported records a finding, as RV4 did. If the work proves not to be
   trivial, a plan opens then.

### What this costs

A defect the owning tests do not see ships without a second reader until the
certifying run, which tests regressions, not new defects. The two reviews that
found real problems on 2026-10-26 were of changes that were not trivial under
the triage rule: the `check_cairn` fix found a bug that silently skipped files
with non-English names (a defect no test covered), and the Cairn Plain Language
review found two test gaps and a dropped half-finding. Applying the triage rule
honestly would have given both a plan and its review. So the cost falls on the
claim, which item 3 tests, and the fence in item 2.

### Edit list (the plan owns the mapping)

| Area | File | Change |
| --- | --- | --- |
| Governing | `AGENTS.md`, `templates/core/AGENTS.md` (Boundary B, the paragraph that begins "Boundary B governs every implementation") | drop "Boundary C's Bounding verdict reviews it afterwards" for a trivial change and the closing sentence on the code reviewer's Bounding verdict for a change with no plan; add the item 2 fence |
| Doctrine | `doctrine/lifecycle.md` (61) | the trivial lane is "code + test", no review |
| Doctrine | `doctrine/proposals.md` (191-203) | the "no plan" clause |
| Template | `dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md` | the `Plan review` clause, after the existing prefix (`bootstrap/tests/test_review_stance_in_shipped_files.py:709-711`) |
| Docs | `docs/dev-tour.md` (81-84 and the worked example from line 95), `docs/glossary.md` (18), `docs/quickstart.md` (15-16, 501) | the trivial lane has no code review |
| Figure and lane summaries | `docs/assets/three-lanes-of-change.svg` (header comment, `desc`, trivial-lane text), `README.md` (44), `docs/getting-started.md` (28), `docs/index.html` (168) | the trivial lane is "the change with its test"; the figure keeps its house rules (alt text, a recorded legibility pass) |
| Changelog | `CHANGELOG.md` | one entry |

Not edited: `doctrine/lifecycle.md` 176-184 and 212-219, `doctrine/plans.md`
88-91, and the `docs/` sentences "implemented and archived in one commit" (they
are now true as written); the two example projects; the frozen
`bootstrap/tests/test_quickstart_sequence.py`; `doctrine/lifecycle-contract.md`.
`dev/agent_collaboration.md:133` and its template already say "a trivial change
with no review owes none".

### Verification

* **Consistency, with controls.** Search `README.md`, `docs/`, `doctrine/`,
  `templates/` and `AGENTS.md` for "code review" within a few lines of
  "trivial", "typo" or "one-line", and for "Bounding verdict". Every hit is
  edited or listed with its reason. First run the search against
  `doctrine/lifecycle.md:61` and `docs/glossary.md:18`, which are known to
  contain the target.
* **Tests.** The tests near the edit sites are
  `test_review_stance_in_shipped_files.py`, `test_verification_boundaries.py`,
  `test_certifying_run_rule.py`, `test_scope_reduction_trap.py` and
  `test_stewardship_rules_ship.py`; the implementer also runs every test that
  reads a changed file, found by search. `AGENTS.md` and its template change,
  so the lockfile step (`scaffold.py upgrade --finalize`) applies.
* **The figure.** A re-render check at 375 and 1200 px with the legibility pass
  recorded, as the house rules require.
* **Gates.** `claim_check`, `link_check`, `check_cairn`, and the neutrality and
  redundancy gates.
* **What would show it wrong.** A change that shipped a defect a review would
  have caught and that the triage rule called trivial.

### Questions for the Maintainer

1. **Keep the fence in item 2** (a change with a `full` Boundary B keeps its
   review)? *Default:* yes. It reuses a line the doctrine already draws and
   costs nothing for a safe change. The alternative is no review for any trivial
   change, whatever its surface.
2. **Does "trivial" include the trivial lane?** *Default:* yes, so a typo fix
   no longer needs a fresh reviewer. If you meant only the no-plan
   implementation of an accepted proposal, drop the figure, README, glossary and
   dev-tour rows from the table.

### Header and scope

**Plan review**: `not required(prose edits to one rule and the docs that repeat
it; the edit list was checked against the tree by the first review and is
checked again by the second; the plan opens in the fast multi-stage form)`. A
reviewer is asked to challenge it.

**Scope delta**: narrowed by the Maintainer's direction. Revision 1's
reordering and its named exception are withdrawn; no accepted scope is removed,
because nothing was accepted. **Assurance path**: high-assurance, unchanged.
