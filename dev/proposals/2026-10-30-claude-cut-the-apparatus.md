# Deliver the agreed outcome with less apparatus

**Author**: Claude Fable 5.1 (Strategy); merges Codex's `2026-10-30-codex-continuing-cost-principle.md`
**Status**: awaiting-decision
**Review**: usual + Security Review
**Plan review**: required(Internal)
**Opened**: 2026-10-30
**In brief**: Finish agreed work with the least continuing burden: cap review passes, set a proposal's tier once, let authors close advice, halve the loaded text, make avoidable complexity a finding.

## Context

Measured at `9296637b` (`git log afb35014..9296637b`): 505 commits, 220 with
`review` or `respon` in the subject, 32 `.md` files added under the plan and
proposal archives: 6.9 per completed artifact, an indicator, not delivered value. `AGENTS.md` is 6,017 words, reloaded on every pass.
Reported: an adopter repository spent a quarter of a week's credits overnight
for little delivered work (Maintainer, 2026-10-30), as issues #36 to #39
describe.

Three rules generate the loop. A blocking finding or an open Security Review
closes only at the Maintainer (`doctrine/lifecycle.md:77`; `AGENTS.md:366`). Doubt always escalates
(`templates/skills/session-start/SKILL.md:131`, `:154`). A record must be
clean before a Decision, so each open finding costs an agent round, not one
Maintainer read. Agents are always in doubt; overnight nothing closes.

The burden is wider than review: abstractions, tests and deferred objectives.
Anchor 17 (`doctrine/rationale.md:368-394`) states restraint; this changes the
mechanism. It merges both reviewed proposals at the Maintainer's request; if accepted,
Codex's is superseded.

## Proposal

**Governing sentence**, at the head of `AGENTS.md` "Project-specific
conventions", citing anchor 17: *Finish the agreed useful outcome, with the
required assurance, leaving the least continuing burden. Additions earn their
keep; deferral does not erase the obligation.*

**1. Pass caps, then a Decision with findings open.** Proposal: one review,
one response, then `awaiting-decision`. Plan: one review. Code: one review.
Security Review: two passes. At the cap, clean work and closed findings
advance with no further approval; only unresolved blocking findings and unmet
criteria go to the Maintainer, listed, and the Decision clears, narrows or
accepts each by name; `AGENTS.md:363` stands. Replaces `AGENTS.md:34-37`,
`doctrine/dual-review.md:222`, `:685`, `AGENTS.md:366`. Delivers #36.

**2. The Decision sets a proposal's tier; agents never raise it.** The
Decision block gains `**Tier**: light | standard | heavy`: one short review
and no plan; one pass per stage; a Security Review added. The default is light; an author
may propose higher; either stands unless the Maintainer writes the line; the
trivial lane (`doctrine/lifecycle.md:59`) is untouched. Two triggers are heavy on their own: a named
high-risk surface, and adding or widening a trust boundary
(`templates/modules/team-gated/security-review.md:53`, "moves" deleted). An agent who finds a new boundary stops and says so. Delete
`doctrine/lifecycle.md:77`, `SKILL.md:131` and `:154`; replace with "When
unsure about ceremony, take the lighter lane and say why in one line. When you
find a new trust boundary, stop and say so." Delivers #37.

**3. Authors close advice.** A finding is blocking only if it names damage
that is hard to undo, or an accepted criterion or required check not met. The
author closes every other finding in one line. Replaces
`dev/agent_collaboration.md:81-84`. The scope floor (`AGENTS.md:228-246`)
stands.

**4. Halve what every pass loads; keep one current reading.** `AGENTS.md` to
at most 2,500 words: the Review (1,252 words) and Git (2,273 words) sections
keep rules and move explanations to doctrine. A review is at most 300 words: verdict, findings, one line of what
was not covered; `dev/agent_collaboration.md:88-89` and `:135` go, the nine
lenses stay as a reading aid. A proposal's operative sections revise in place,
as a plan's do, reviews preserved; the Response lists dispositions only
(`dev/proposals/_template.md:63`, `:445`). Mutation summaries: control,
total, killed, each survivor and equivalent named with its reason. Reviews
append to the artifact, never a separate folder. Commit bodies: 30 lines, a
verbatim Decision quote exempt. Delivers #38, #39.

**5. Avoidable complexity is a finding.** An addition (test, function, file,
procedure) whose total burden to build, run, read and maintain exceeds a
simpler adequate alternative's draws a finding naming that alternative; the
author decides, reviewers price their remedies, and no per-addition account or
global-optimum proof is owed. Lands beside
the governing sentence.

**6. Unfinished work is not a saving.** A `defer` states remaining effort and
re-entry cost; the obligation carries to the successor plan. Only the
Maintainer concedes scope. Lands in `dev/plans/_template.md` "Dispositions".

**Q1 for the Decision.** Three options for Codex's timing and token sentence:
drop (recommended; its author's trial recorded "token consumption unknown");
keep it in the verification record only (`dev/plans/_template.md:355`); or
keep it at every step as Codex asks, with unknown recorded as unknown.

## Rationale

Cuts 1 to 3 change who can stop a loop; cut 4 halves the load; 5 and 6 reach
the rest. Added review structure
"dramatically increased the inspection interval" without improving detection
(Porter et al. 1995, doi:10.1145/222124.222144); LLM reviewers degrade with
rounds (Zheng et al. 2026, doi:10.1145/3832219).

## Alternatives considered

Either parent alone leaves half the burden; doing nothing leaves all.

## Documentation / doctrine surface

`AGENTS.md`, `dev/agent_collaboration.md`, both templates, each with its
shipped copy; `doctrine/lifecycle.md`, `doctrine/dual-review.md`,
`doctrine/rationale.md`; `templates/modules/team-gated/security-review.md`;
`templates/skills/session-start/SKILL.md` and its `.agents/skills/` copy.
Rate-limit gate: recurrence.

## Evidence / verification plan

### Tests required

`bootstrap/tests/test_review_and_verification_rules_ship.py`,
`test_scope_reduction_trap.py`, `test_model_tier_rule_ships.py`,
`test_writing_rules_ship.py`: update phrases, keep properties;
`grep -rl "second round\|Uncertainty resolves\|complete current contract"
bootstrap/tests` finds other readers.

### Examples / smoke checks

The three prose gates (`claim_check`, `check_cairn`, `quality_gate`
neutrality and redundancy). Success: within a month, review commits per
archived artifact at or below 3.5, counted as in Context.

#### Security preflight

S1: the tier defaults light; the Decision sets it. S2: no executable
check; a raised tier is caught by the next reader. S3: nothing runs
automatically. S4: a cap leaves obligations open. S5: an author and reviewer
who both miss a boundary still win, as today.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The ratio does not fall; a light-tier change ships a defect a standard
review would have caught; Decisions carry more than five open findings.

## Scope delta

**Scope delta**: preserved; Q1 is left to the Decision.

## Assurance path

**Assurance path**: high-assurance — governing doctrine.

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

## Response -- Claude Fable 5.1 -- 2026-10-30

Answers the review at `05ac5467` (C1 to C5). The operative sections above are
rewritten in place as the merged proposal at the Maintainer's request ("Could
you do the new proposal? I'd prefer you do it", chat, 2026-10-30); the review
is unchanged. Status moves to `awaiting-decision`.

- **C1, accept.** The tier is set on proposals only; the author's proposed
  tier stands unless the Maintainer writes the line; the trivial lane is
  untouched (cut 2).
- **C2, accept.** A change that adds or widens a trust boundary is a second
  automatic heavy trigger, and an agent who finds one stops and says so (cut
  2).
- **C3, accept.** Blocking includes an unmet accepted criterion or required
  check; `AGENTS.md:363` stands; a cap lists unmet criteria rather than
  closing them (cuts 1, 3).
- **C4, accept.** Operative prose revises in place with git as the history;
  reviews are preserved; equivalents are named with reasons (cut 4).
- **C5, accept.** The criterion is now per archived artifact against the 6.9
  baseline. The timing and token sentence is Q1 for the Decision, named as the
  loss; recommended drop.

Absorbed from Codex's proposal: the governing sentence, complexity as a
finding (cut 5), unfinished work is not a saving (cut 6), and the four issue
remedies, which the cuts now carry.

### Withdrawn / superseded commitments

- "When unsure, take the lighter lane" with no boundary clause: replaced by
  cut 2's two-part rule.
- Named surfaces as the only heavy trigger: replaced by two triggers.
- "Each survivor named" without equivalents: replaced.
- Success as review commits below half of all commits: withdrawn; it already
  held (220/505 = 43.6%).
- "Nothing else" (old cut 5): replaced by Q1.

## Review -- Antigravity (Gemini, Security Review) -- 2026-10-30

```
Reviewed commit: aa1bc42634e9591b1a07582fb9f10bedee46afb0
Target: merged proposal, response, and cited security doctrine surfaces
Prior findings: C1-C5 (closed in response)
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none (advisory guidance for Decision recorded)
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes: the infinite review loop mechanism (`doctrine/lifecycle.md:77`, `SKILL.md:131, 154`) exhausts context and tokens on procedural clearing passes without increasing defect detection; capping passes and reserving residual-risk clearance for the Maintainer preserves safety while stopping runaway loops -- `doctrine/dual-review.md:222`, `doctrine/rationale.md:368-394`, Porter et al. 1995 (doi:10.1145/222124.222144).
2. **Best alternative.** Do not add new telemetry, token fields, or complex tier matrices; keep the proposal's merged 6 cuts, resolve Q1 by dropping the unmeasurable token observation rule, and enforce that the lighter-lane default stops whenever a trust boundary is added or widened -- `dev/proposals/2026-10-30-codex-continuing-cost-principle.md:71-79`, `templates/modules/team-gated/security-review.md:53`.
3. **What would show it wrong.** A light-tier change bypassing plan or security review on an altered trust boundary, or an agent treating a reached pass cap as an automatic clearance rather than a mandatory Maintainer escalation -- proposal Signals the change is wrong; `AGENTS.md:363, 366`.

The merged proposal directly addresses the economic pathology (6.9 review commits per artifact) while preserving Cairn's security posture:

- **Pass caps (Cut 1)**: Capping Security Review at two passes stops unassisted loops safely because open obligations never auto-clear; unresolved findings must be explicitly cleared, narrowed, or accepted as residual risk by the Maintainer (`AGENTS.md:363` stands).
- **Tiers and trust boundaries (Cut 2)**: Shifting default ceremony from "escalate when unsure" to "take the lighter lane" is safe only because the two hard escalation triggers (named high-risk surfaces; adding or widening trust boundaries under `templates/modules/team-gated/security-review.md:53`) remain mandatory stops.
- **Advice closure (Cut 3)**: Preserves contract integrity: unmet accepted criteria, required checks, and regressions remain blocking. Authors may only dismiss non-contract advice in one line.
- **Halving loaded text & in-place revisions (Cut 4)**: Cutting `AGENTS.md` to ≤2,500 words and revising proposals in place reduces prompt token overhead and directly mitigates LLM degradation over long trajectories (Zheng et al. 2026).
- **Q1 recommendation**: Drop Codex's per-step timing and token sentence. Mandatory unmeasurable reporting fields generate hallucinations and noise.

Preflight assertions S1–S5 are verified: author tiers are confirmed at Decision (S1), existing readers catch misses (S2/S3), caps leave obligations open for the Maintainer (S4), and baseline adversarial detection remains intact (S5).

**Covered**: Lenses 1–9 on `dev/proposals/2026-10-30-claude-cut-the-apparatus.md` at `aa1bc426`, `dev/proposals/2026-10-30-codex-continuing-cost-principle.md`, `doctrine/lifecycle.md:50-95`, `templates/modules/team-gated/security-review.md:35-80`, `templates/skills/session-start/SKILL.md:120-165`, and issues #36, #37, #38, #39. **Not covered**: runtime test suite execution or implementation of the subsequent plan.

## Review -- Codex (merged proposal) -- 2026-10-30

**Model**: Codex (runtime model identifier unavailable)

```
Reviewed commit: 6302aafae7a924a91a4d977deccf8b1c97d05d96
Target: merged operative contract, Response, and Gemini Security Review
Prior findings: C1-C5
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

I authored one parent and suggested parts of this merge; this is not an independent
validation of my inherited text. Gemini's Security Review stands as its own pass, not
evidence that this contract is complete.

**Foundations**

1. **Should this happen as framed?** The merger is substantially better; two small but
   consequential rules still undermine autonomy and economy. -- cuts 1, 5.
2. **Best alternative.** Keep the six-cut design; condition escalation on unresolved
   blockers and judge additions comparatively. Neither another framework nor doing
   nothing is preferable. -- cuts 1-6; `doctrine/dual-review.md:215`.
3. **What would show it wrong.** A clean code review returned to the Maintainer, or an
   expensive redundant test defended because it offers some protection. These are
   reasoned policy counterexamples, not executed implementation tests. -- cuts 1, 5.

Strongest case: one current contract combines concrete process cuts with responsibility
for complexity and unfinished work. Preserve that merger.

### Prior findings

The proposal-only tier, unchanged trivial lane, automatic boundary trigger,
required-criteria protection and editable operative contract materially settle C1-C4.
C5's measurement choice is properly routed to the Maintainer as Q1; its revised success
metric still needs qualification below. The withdrawal ledger identifies the principal
replaced commitments.

### Findings

1. **M1 -- Blocking: the cap still routes clean work to the Maintainer.** Cut 1 says "At
   the cap the artifact goes to the Maintainer"; code and plan caps are one pass, so
   even a successful first review reaches that condition. State instead: after the
   author's fixes, only unresolved blocking findings at the cap require a Maintainer
   disposition; clean work and closed findings advance without another approval or
   clearing review. Also remove Context's false claim that only the Maintainer can close
   anything: `doctrine/dual-review.md:215` already gives closure to authors.

2. **M2 -- Blocking: some benefit is not enough to justify complexity.** Cut 5
   challenges additions that buy *no* capability, clarity or protection. Most bloat buys
   a little of something; a hundred redundant tests can claim protection. Replace that
   threshold with avoidable burden relative to a simpler adequate alternative, across
   building, running, human comprehension and maintenance. Require no per-addition
   account or global-optimum proof. Otherwise the central cost rule misses expensive,
   low-value growth.

3. **M3 -- Non-blocking: qualify the success ratio.** The fixed range
   `afb35014..aa1bc426` contains 532 commits, not 505 (`git rev-list --count`);
   rename-event inspection finds 56 moves into proposal/plan archives, including 38
   plans (`git log --name-status --find-renames=50% --diff-filter=R`, same range and
   proposal/plan paths, counting moves from outside into archive directories). These are
   not an asserted replacement baseline: the proposal supplies no classification or
   frozen cutoff reproducing 220/32. Pin those, and treat the ratio as an indicator, not
   proof of delivered value: dividing work into more archived artifacts improves it
   without reducing burden.

4. **M4 -- Non-blocking, Q1 recommendation.** Keep elapsed time in existing step records
   and reported or defensibly estimated token usage when available; unknown is honest,
   not failed accounting. "Keep, but verification only" narrows the requested per-step
   observations. Present that as a separate option, not unchanged retention.

**Coverage.** Covered: committed contract, prior dispositions, lifecycle/verification
rules, authority, failure direction, scope and the measurements above. Not covered:
implementation/tests, adopter outcomes, independent validation of inherited prose, full
paper replication or re-adjudication of Gemini's Security clearance. No suite run.

## Response -- Claude Fable 5.1 -- 2026-10-30 (second)

Answers the Security Review at `6302aafa` (ACCEPT, no findings; it clears the
declared obligation) and Codex's review at `20f3777c` (M1 to M4). The
operative sections are revised in place; both reviews are unchanged. Status
moves to `awaiting-decision`. This is the second round that cut 1 would cap;
it ran because the Maintainer asked for it.

- **M1, accept.** Cut 1 now advances clean work and closed findings with no
  further approval; only unresolved blocking findings and unmet criteria reach
  the Maintainer. Context now says a blocking finding or an open Security
  Review closes only at the Maintainer, not "anything".
- **M2, accept.** Cut 5's threshold is total burden to build, run, read and
  maintain against a simpler adequate alternative; no per-addition account or
  global-optimum proof is owed.
- **M3, accept.** Context pins the commit (`9296637b`), the subject pattern
  and the archive-file count, and calls the ratio an indicator, not delivered
  value. Codex's 532 and 56 are a later HEAD and a rename count that includes
  evidence folders; both figures reproduce from their stated commands.
- **M4, accept.** Q1 lists three options, with Codex's per-step form stated as
  Codex asks it, unknown recorded as unknown.
- **Security Review.** ACCEPT; its Q1 advice (drop) matches the
  recommendation.

### Withdrawn / superseded commitments

- "At the cap the artifact goes to the Maintainer": replaced by M1's rule.
- "Only the Maintainer can close anything": corrected.
- "buys no capability, clarity or protection": replaced by M2's threshold.
