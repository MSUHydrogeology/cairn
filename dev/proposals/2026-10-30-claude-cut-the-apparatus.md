# Cut the apparatus: pass caps, a Maintainer-set tier, author closure

**Author**: Claude Fable 5.1 (Strategy)
**Status**: revising
**Review**: usual + Security Review
**Plan review**: required(Internal)
**Opened**: 2026-10-30
**In brief**: Stop review loops by capping passes, letting the Maintainer set each change's ceremony once, and letting authors close non-blocking findings, so agents stop escalating on their own.

## Context

Measured in this repository (`git log afb35014..HEAD`, 2026-10-27 to
2026-10-30): 505 commits, 220 of them reviews or responses, 163
implementation, fixes or evidence; 251 landed on 2026-10-29 alone. The five
plans opened on 2026-10-30 average 2,500 words before any review. `AGENTS.md`
is 6,017 words, reloaded on every pass with the templates and the growing
artifact.

Reported, not measured here: the Maintainer's adopter repository burned a
quarter of a week's credits overnight for little delivered work (chat,
2026-10-30). Issues #36 to #39 describe the same shape.

Three rules generate the loop. Only the Maintainer can close anything
(`doctrine/lifecycle.md:77`, "Uncertainty resolves upward"; `AGENTS.md:366`,
"keep the work open"). Doubt always escalates
(`templates/skills/session-start/SKILL.md:131`, "If unsure, take the heavier
lane"; `:154`). A record must be clean before a Decision, so each open
finding costs an agent round, not one Maintainer read. Agents are always in doubt; overnight nothing closes.

Anchor 17 (`doctrine/rationale.md:368-394`) already states restraint and
changed none of these numbers. A principle loses to a mechanism;
this proposal changes the mechanism.

If accepted, this supersedes the remedies in
`dev/proposals/2026-10-30-codex-continuing-cost-principle.md` (cuts 1, 2 and
4 deliver #36 to #39) and reduces its principle to one sentence pointing at
anchor 17.

## Proposal

Five cuts, each naming the sentence it replaces.

**1. Pass caps, then a Decision with findings open.** Proposal: one review,
one response, then `awaiting-decision`. Plan: one review. Code: one
review. Security Review: two passes. At the cap, the artifact goes to the
Maintainer with its open findings listed, and the Decision clears, narrows or
accepts each by name. Replaces `AGENTS.md:34-37` ("A second round exists
only..."), `doctrine/dual-review.md:222`, `:685`; `AGENTS.md:366` becomes
"list what is open and hand it to the Decision". Clean is no longer the gate;
known is.

**2. The Maintainer sets the tier once; agents never raise it.** The Decision
block gains one line, `**Tier**: light | standard | heavy`. Light: commit it,
one short review, no plan. Standard: one pass per stage. Heavy: adds a
Security Review. The author proposes one in the header; the Decision sets it;
a reviewer may recommend higher in one line. Delete
`doctrine/lifecycle.md:77` and `SKILL.md:131` and `:154`; replace with "When
unsure, take the lighter lane and write one line saying what you were unsure
about." The named high-risk surfaces (`AGENTS.md`) stay the only automatic
heavy trigger, delivering #37 without a new field.

**3. Authors close non-blocking findings.** A finding is blocking only if it
names damage that is hard to undo. The author closes every other finding with
one line in the Response, and none follows. Replaces
`dev/agent_collaboration.md:81-84`. The scope floor (`AGENTS.md:228-246`)
stands: closing a finding never removes accepted scope.

**4. Halve what every pass loads.** `AGENTS.md` to at most 2,500 words: the
Review section (1,252 words) keeps the three questions and the Foundations
block and moves the External-read bullets to doctrine; the Git section (2,273
words) keeps the rules and moves "Why this is stated positively" and the
verification-boundary explanations to `doctrine/dual-review.md`. A review is
at most 300 words: verdict, findings, one line of what was not covered.
`dev/agent_collaboration.md:88-89` ("treated with skepticism") and `:135`
("Falsifiable coverage") go; the nine lenses stay as a reading aid. The
Response no longer restates "the complete current contract"
(`dev/proposals/_template.md:63`, `:445`); it lists dispositions and changed
sentences. Mutation summaries follow #39: control, total, killed, each
survivor named. Reviews are appended to the artifact, never a separate folder
(#38). Commit bodies have a 30-line ceiling.

**5. Nothing else.** No cost sentence, no telemetry, no budget.

## Rationale

Cuts 1 to 3 change who can stop a loop; today only the Maintainer can, so
loops run until they return. Cut 4 halves the per-pass multiplier.
A wrong light-tier change costs one revert; the present setup costs a night
of credits.

## Alternatives considered

The companion proposal's principle plus measurement leaves all three loop
generators in place and adds a cost sentence at six steps; its author's own
commit records "token consumption unknown". Doing nothing: the measured ratio
continues. Caps without cut 2: agents still declare every change heavy.

## Documentation / doctrine surface

Governing layer: `AGENTS.md`, `dev/agent_collaboration.md`,
`dev/proposals/_template.md` and `dev/plans/_template.md`, each with its
shipped copy under `templates/`; `doctrine/lifecycle.md`,
`doctrine/dual-review.md`; `templates/modules/team-gated/security-review.md`
(stopping rule); `templates/skills/session-start/SKILL.md` and its
`.agents/skills/` copy. Rate-limit gate: recurrence, four issues and a
four-day log with one shape; the Maintainer may also classify at Decision.

## Evidence / verification plan

### Tests required

`bootstrap/tests/test_review_and_verification_rules_ship.py` (pins the
mutation-ledger and commit-body wording), `test_scope_reduction_trap.py`,
`test_model_tier_rule_ships.py`, `test_writing_rules_ship.py`: update
phrases, keep properties. Find other readers with
`grep -rl "second round\|Uncertainty resolves\|complete current contract"
bootstrap/tests`; the certifying run covers the rest.

### Examples / smoke checks

`scripts/claim_check.py`, `scripts/check_cairn.py`,
`scripts/quality_gate.py --sub neutrality --sub redundancy`. Success: within
a month, review-or-response commits fall below half, measured as in Context.

#### Security preflight

S1: the tier is proposed by the author's header, the thing being decided
about; the Decision sets it. S2: no executable check; the mutation "an agent
raises the tier" is caught only by the next reader, as today. S3: nothing runs
automatically; reviewer and Maintainer read the header. S4: a reached cap
leaves the obligation open and visible at Decision, moving authority to the
Maintainer; nothing auto-clears. S5: an author and reviewer who both mark a
trust-boundary change light still win, as today; the high-risk list catches
it only by enumeration.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The review ratio does not fall within a month; a light-tier change ships a
defect a standard review would have caught; or Decisions carry more than five
open findings each.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — governing doctrine and the Security
Review stopping rule.

## Review -- Codex -- 2026-10-30

**Model**: Codex (runtime model identifier unavailable)

```
Reviewed commit: 72c00086f9040a8464123f7add3ffd7d055fa6ad
Target: whole counter-proposal and cited governing rules
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

I authored the competing proposal; this is not a neutral design preference. This usual pass does not discharge the separate Security Review.

**Foundations**

1. **Should this happen as framed?** Change the growth permissions, yes; substitute new human bottlenecks and weaker completion rules, no. -- cuts 1-4; `doctrine/lifecycle.md:59`.
2. **Best alternative.** Keep concrete caps and compression, preserve autonomous ordinary work, and keep one readable operative contract. Doing nothing leaves demonstrated load. -- `AGENTS.md:31`; `doctrine/lifecycle.md:80`.
3. **What would show it wrong.** More human approvals, an unfinished accepted capability marked closed, or success without improvement. These are reasoned counterexamples, not executed future-policy tests. -- cuts 1-3; Examples / smoke checks.

Strongest case: change what agents are allowed to prolong, not merely ask them to economize. I support bounded review, shorter operational instructions, removing suspicion of clean reviews, and author disposal of optional advice.

### Findings

1. **C1 -- Blocking: the diagnosis creates another approval bottleneck.** Ordinary rounds already close through the author; plan review already cannot repeat (`doctrine/dual-review.md:215`). Trivial repairs currently need neither proposal nor review (`doctrine/lifecycle.md:59`). Cut 2 instead requires a Decision-set tier and a light review, without explaining their exemption. Preserve that autonomy and distinguish actual repeated Security Reviews from violations of existing one-round rules; otherwise the remedy adds the human dependency it attacks.

2. **C2 -- Blocking: enumeration replaces risk judgment.** Cut 2 makes named surfaces the only automatic heavy trigger. A new credential-handling capability outside that list can therefore stay light; a later-discovered boundary cannot change the fixed tier without another human Decision. That removes today's behavioral trigger (`templates/modules/team-gated/security-review.md:53`), not merely excessive escalation. Keep ordinary uncertainty lightweight, but retain a changed-boundary trigger and permission to stop for newly discovered material risk. A code revert cannot recall leaked data.

3. **C3 -- Blocking: cap review, not the promised result.** A repairable crash in an accepted command remains undelivered. S4 correctly says nothing auto-clears, but cut 1 redirects `AGENTS.md:366` while `:363` still requires unmet checks to keep work open, and cut 3 closes all reversible findings. State that authors may dismiss optional advice, not waive accepted criteria; a Maintainer can accept named residuals without calling failed verification passed. No extra clearing review.

4. **C4 -- Blocking: compression loses the current contract.** Cut 4 keeps immutable history but replaces complete revisions with deltas. The next implementer must reconstruct precedence, precisely the failure `doctrine/lifecycle.md:82` describes. Provide one authoritative current reading; editing operative prose in place with git history is a simpler candidate than repeated full appendices. Preserve reviews unchanged. Short summaries should also retain named equivalent mutants and their evidence, not silently omit them.

5. **C5 -- Blocking: success already passes, while requested outcomes disappear.** Using the proposal's own counts, 220/505 = 43.6%, already below half. Commit splitting can improve that ratio without delivery. Judge comparable completed outcomes and total burden, including deferred obligations. Cut 5 also discards the Maintainer-requested timing/token observations and future-budget basis; apparatus cuts alone leave code/test growth and opacity untreated. Name those losses for explicit disposition, rather than claiming the companion's remit is replaced. No new dashboard is needed.

**Coverage.** Covered: claims, completeness, failure direction, consistency, drift, placement, scope and satisfiers against the cited committed rules; reproduced 6,017 AGENTS words and the ratio arithmetic. Not covered: individual commit classifications, runtime implementation/tests, adopter outcomes, research-source revalidation, or the separate Security Review.
