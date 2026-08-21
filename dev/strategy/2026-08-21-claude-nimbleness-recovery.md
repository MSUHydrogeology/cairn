# Nimbleness recovery — shedding process mass without losing the point

**Author**: Claude (Strategy)
**Model**: Fable 5
**Date**: 2026-08-21
**Status**: revised (Maintainer feedback folded in inline; literature pass
added and every citation verified against its published source, 2026-08-21)
**Type**: product-strategy
**Audience**: the Maintainer first; the agents who work here second
**Surfaces this would feed**: `AGENTS.md`, the proposal/plan templates,
`doctrine/proposals.md` triage, `dev/PLANNING.md`, the shipped
`templates/core/` defaults, and Cairn's own operating profile

---

## The question

Cairn began as *"Yes, we can do that — let's take a moment to make it
good."* It has mutated into *"We can't do that without endless revision
and process adherence."* The Maintainer's word is **process-zombies**,
and the record supports it. The question: **what do we cut, what do we
keep, and how do we stop it growing back?** This note is deliberately
short by current Cairn standards — the first recommendation, demonstrated.

## What the numbers say

All figures as_of 2026-08-21 and deliberately approximate — the shape
matters, not the third digit.

| Measure | Figure |
|---|---|
| Commits in this repo | ~2,000, of which **~65% touch `dev/`** (the deliberation record) and ~40% touch anything shipped |
| Proposals written | 67 — **median ~900 lines, mean ~1,100**, largest 2,800 |
| Plans written | 46 — **median ~1,800 lines** |
| Lifecycle commits per proposal | ~8, before any implementation begins |
| Deliberation prose (proposals + plans) | **~166,000 lines** |
| Everything Cairn actually ships (templates Python + scaffold engine + doctrine) | ~49,000 lines |
| Process tooling (`lifecycle.py` + `lifecycle_planner.py`) | ~10,500 lines — as large as the scaffold engine it administers |
| Test suite | **4,468 tests, ~10 minutes** — for a product that is mostly markdown templates and a stdlib installer |
| Governing prose in front of a new adopter | ~7,800 words before the first real commit (friction audit, 2026-06-12) |
| The proposal *template* alone | 693 lines |
| Occurrences of "refuse/refusal" across governing docs and tools | ~170 |

One lived case, from 2026-08-20: **an adopter filed four bug reports** —
at bottom a regex fix, a timeout flag, a stale comment, and an exit-code
cleanup. Handling them produced **3 proposals totaling 6,475 lines, ~45
findings across four review rounds each, two external security reviews,
and 57 lifecycle commits — and zero lines of shipped fix.** In an
ordinary healthy repo this is three pull requests and a day's work.

The sister repo shows the same signature: in `modflow_tools` a single
plotting feature took **three plan-review rounds and six code-review
rounds**, commit subjects read as process narration, and roughly
three-quarters of recent commits are lifecycle traffic rather than
hydrology.

**The honest other side:** review catches real defects — a regex that
refused dotted branch names, an invariant satisfied only over an empty
set, a dependency-closure inflation of 580 vs 5. But every one of those
catches came from *running something* — a fresh repo, a canary, a
falsifying mutation — and none needed a 900-line proposal to exist. The
rigor lives in the measurements; the mass lives in the prose. Keep the
first, shed the second.

## How we got here — five ratchets

Cutting mass without disabling the mechanisms means it all grows back.

1. **Every incident becomes a rule, and no rule ever leaves.** A
   rate-limit gate slows *adding* rules; nothing removes one. Sediment
   accretes; nothing flushes. (The exception that proves the fix works:
   the 2026-08 rewrite replacing the blanket per-commit approval gate
   with targeted fences.)
2. **Agents are compliance-maximizers with an asymmetric loss
   function.** No agent is criticized for a 2,500-line proposal;
   any omission is blocked. So agents write armor: nothing in the
   doctrine prices time or length, and verbosity is currently
   indistinguishable from rigor — while being cheaper to produce.
3. **Review has no cost side.** Every finding is free to file, every
   round free to demand — 45 of 45 findings accepted on 2026-08-20,
   rounds ratcheted from one to six with no one deciding that. A
   reviewer who extends process can never be shown wrong, because the
   lighter path is never run.
4. **Self-hosting doubles everything.** Cairn builds Cairn using Cairn,
   so every attempt to lighten the process runs at full process weight.
   The `review-efficient-lifecycle` proposal (2026-08-10) diagnosed
   this exactly — then landed as *more* vocabulary. The immune system
   attacks the cure.
5. **The triage is dead in practice.** `doctrine/proposals.md` already
   says *"Everything else … just commit,"* but surface-based triggers
   and a culture of exhaustive caution capture nearly everything above
   a typo. Bug fixes became security-reviewed proposals.

## The same conclusions, top-down

The sections above argue bottom-up from Cairn's own measurements. These
nine principles derive the same conclusions from established theory —
so the measurements become confirmation, not the whole case. (Citations
verified against their published sources, 2026-08-21.)

**P1 — Process weight is a dial set by consequence, not a virtue.**
Boehm & Turner, *Balancing Agility and Discipline* (Addison-Wesley,
2003): under- and over-process are both risks, tailored per project by
what failure costs, and small teams are damaged more by excess
discipline. The high-reliability literature (Weick & Sutcliffe,
*Managing the Unexpected*, 2001; Perrow, *Normal Accidents*, 1984)
warrants heavy control for tight coupling and irreversible failure —
neither describes a template repository. *Licenses: the three lanes,
C0's hard-to-undo test, the deliberate lane for named surfaces.*

**P2 — Decision rights belong where the specific knowledge is.**
Hayek, "The Use of Knowledge in Society" (*Am. Econ. Rev.* 35(4),
1945); Jensen & Meckling, "Specific and General Knowledge, and
Organizational Structure" (in *Contract Economics*, Blackwell, 1992):
moving a decision away from the knowledge means either moving the
knowledge (expensive) or deciding without it (worse). *Licenses:
expertise routing — science to the Maintainer in domain terms,
implementation detail to the author, structure as
recommendation-with-default.*

**P3 — Small batches converge; large batches diverge.** Reinertsen,
*The Principles of Product Development Flow* (Celeritas, 2009): batch
size drives cycle time, feedback delay, and risk. The review literature
agrees empirically: open source, Google, and Microsoft *converged
independently* on small changes, one-to-two reviewers, fast iteration
(Rigby & Bird, ESEC/FSE 2013; Sadowski et al., ICSE-SEIP 2018 — at
Google most changes are small, single-reviewer, committed within a
day), and defect discovery per line falls off sharply beyond ~200–400
lines under review (Cohen, *Best Kept Secrets of Peer Code Review*,
SmartBear 2006 — the Cisco study). The industry already ran Cairn's
arc once: Fagan's formal inspections (*IBM Systems Journal* 15(3),
1976) gave way to lightweight review after Votta ("Does Every
Inspection Need a Meeting?", FSE 1993) showed the ceremony added little
beyond the reading. *Licenses: size anchors, the change note, the
two-round cap.*

**P4 — Where cases are few and judgment is rich, standards beat rules —
and a rule routinely circumvented is worse than none.** Kaplow, "Rules
versus Standards" (*Duke Law Journal* 42(3), 1992): rules pay off with
frequent homogeneous cases; standards win where cases are heterogeneous
and judgment is present — a two-person research team is the far
standards end. Hollnagel (*Safety-I and Safety-II*, Ashgate, 2014):
procedures that must be bypassed to get work done *train* bypassing —
the Maintainer's "they will ALWAYS be circumvented" restates this. The
automation literature closes the loop: restrictive or false-alarm-prone
automation produces disuse (Parasuraman & Riley, *Human Factors* 39(2),
1997; Lee & See, *Human Factors* 46(1), 2004). Ostrom (*Governing the
Commons*, Cambridge, 1990) adds minimal rules congruent with local
conditions and *graduated* sanctions — a warning before a refusal.
*Licenses: advisory-not-binding, warnings-first tooling, rule removal.*

**P5 — Satisficing terminates; optimizing doesn't.** Simon, "Rational
Choice and the Structure of the Environment" (*Psychological Review*
63, 1956): search has costs the optimum ignores, so a good procedure
stops at good-enough. Merton, "Bureaucratic Structure and Personality"
(*Social Forces* 18(4), 1940) names the alternative: goal displacement
— rules conceived as means become ends in themselves. A process-zombie
is a Mertonian ritualist. *Licenses: termination rules, author-decides
after round two, C0 as a satisficing test, the moratorium.*

**P6 — The record serves the reader's comprehension, not completeness.**
Parnas & Clements, "A Rational Design Process: How and Why to Fake It"
(*IEEE TSE* SE-12(2), 1986): produce the document the next reader
needs, not the transcript of the search. Bacchelli & Bird (ICSE 2013):
review's dominant product *and* obstacle is understanding — so size,
which impedes understanding, degrades the very thing review makes.
This is Cairn's own comprehension floor, independently supported.
*Licenses: write-once-restate-never, the ≤150-line change note.*

**P7 — For scientists, good-enough is the adoption frontier.** The
research-software community ran this correction on itself: "Best
Practices for Scientific Computing" (Wilson et al., *PLoS Biology*
12(1), 2014) asked more than working scientists would adopt, and its
own authors republished the realistic subset as "Good Enough Practices
in Scientific Computing" (Wilson et al., *PLoS Computational Biology*
13(6), 2017). Segal (*Empirical Software Engineering* 10(4), 2005)
documents document-led SE process imposed on scientists being rejected:
scientists expect emergent requirements. Cairn is recapitulating the
2014→2017 arc and should complete it deliberately. *Licenses: the
light default profile, dogfooding the median, handbook-as-product.*

**P8 — A measure that becomes a target stops measuring.** Goodhart's
law; Campbell, "Assessing the Impact of Planned Social Change"
(*Evaluation and Program Planning* 2, 1979). *Licenses: caps as review
vocabulary never tool-enforced, staff gauges, the sunset clause.*

**P9 — One falsifying test outranks accumulated argument.** Platt,
"Strong Inference" (*Science* 146, 1964) — the paper most working
scientists already know: fields advance fastest when each step could
refute. Every high-value review catch in Cairn's record was a Platt
move; none was a prose volume. *Licenses: measurement-rigor as the
review centerpiece.*

The mapping: Tier 1 rests on P3/P5 (caps, termination), P2
(author-decides), P1 (just-commit), P4 (advisory); Tier 2 on P1
(keep/park/kill), P3/P6 (change note, templates), P4/P5 (rule removal);
Tier 3 on P7, P9, P8. Checked both directions: no recommendation stands
on local numbers alone, and no principle demands a recommendation the
note omits — except P4's graduated sanctions (warnings that escalate on
repetition), deliberately left out as machinery this scale doesn't earn.

**Convergent work, same day:** `2026-08-20-claude-review-loop-termination`
(accepted at Revision 7, superseded the same day on the Maintainer's
direction) attacked the same disease from inside the lifecycle; its C0
risk posture and C1 editor authority are this note's 3.5 and 1.2,
independently derived. Its successor,
`2026-08-21-claude-convergent-lifecycle`, carries C0, C1, and C7 forward
and replaces the container — this note's Tier 1 and much of Tier 2, cast
as one 131-line proposal.

## What must be kept

The irreducible core — what actually answers the founding problem
(sloppy vibe-coded output) — is four things:

1. **Write intent before code.** A committed paragraph: what and why.
2. **Independent review before it lands**, with at least one
   *falsification attempt* — run the thing, try to break it.
3. **Record the decision.** One committed line: who decided, what.
4. **Empirical verification.** Tests for code; a real invocation for
   tools; the claim checker for prose.

Everything else is elaboration, and each elaboration should pay rent.

## Recommendations

**Tier 1** is decree — effective immediately, no proposals (running
these through the full lifecycle would be the disease treating itself).
**Tier 2** is structural, this month. **Tier 3** is strategic.

### Tier 1 — stop the bleeding (this week, by decree)

**1.1 Impose size budgets, framed as comprehension, not thrift.**
Proposal ~150 lines; plan ~300; review round ~50; commit body ~10. The
comprehension floor already says an artifact the Maintainer cannot
penetrate is not decidable — and length is the dominant opacity here. A
900-line proposal is not rigorous; it is unreviewable. (Exceeding a
budget is a smell named in review, not a refusal — no new gate.)

**1.2 Cap review at two rounds — then the author makes the call.**
After round two the author decides each open finding — accept, decline,
or defer, with a one- or two-sentence defense — dissent is recorded,
work proceeds. **No escalation-by-question** (Maintainer direction,
2026-08-21): handing the Maintainer arcane disputes converts "decide"
into "approve". Route by expertise instead — the science goes to them
in domain terms, every time, no default needed; **structure and
direction** arrive in plain language with a recommendation and a stated
default ("we'll do X unless you object"); **implementation detail is
the author's** — escalating it is misrouting, not deference. Every
Cairn adopter is a scientist in this seat, so expertise routing belongs
in the shipped doctrine. The evidence: the Maintainer accepts agent
recommendations **~90% of the time**. A gate that approves nine in ten
is latency, not judgment — make the 90% frictionless and the 10%
conspicuous, which two-sentence recommendations do and bullet lists of
open disputes do not. The recorded, reversible call is what makes
deciding safe.

**1.3 Give findings a cost vocabulary: `blocking` / `note` / `nit`.**
Only `blocking` requires a written response; a round with no blocking
findings *clears* — it does not recycle.

**1.4 Re-arm the just-commit path.** A bug fix with a failing-test
reproduction is **code + test + one code review** — no proposal, no
plan, even on a "security surface": those triggers exist for new
machinery and changed contracts, not for fixing a regex inside
already-reviewed machinery. Adopter bugs get a service target: **fixed
within two sessions.** (The three accepted adopter proposals should be
implemented from page-length plans, not 1,800-line ones.)

**1.5 Every tool becomes advisory: warn, never bind.** (Maintainer
direction, 2026-08-21.) A check that fires is information; a check that
blocks is a decision delegated to a script. Tools keep firing — demoted
from refusal to loud warning a human can overrule in the moment. The
~170 "refuse/refusal" occurrences are the work list. Binding survives
only for genuine safety: the scaffold's symlink/containment check, and
trust-root verification during an actual release ceremony.

**1.6 Declare a construction moratorium.** No new doctrine, gates,
lifecycle vocabulary, ledgers, or trackers until the Tier-2 removal
pass is complete.

**1.7 Commit subjects go back to normal.** "Fix dotted-branch refusal
in inert-key fence" — not a narrated arc.

### Tier 2 — remove mass (this month)

**2.1 A keep/park/kill pass over the apparatus.** One session, one
table, Maintainer decides each row. Suggested dispositions — **keep**
(cheap, real defects, serves adopters): the scaffold engine and its
tests, `claim_check.py`, `link_check.py`, the neutrality gate, the
four-part core. **Park** (defends hazards no current adopter has): the
differential-oracle gate anchor and preflight, AST attestation,
`transition_lint.py`, the pilot ledgers, the intent log, the slot
ratchet, most of the ~10,500 lines of lifecycle tooling — a project
with one adopter does not need airport security. **Diet**: the test
suite — 4,468 tests at ~10 minutes mostly defend parked machinery;
pruning toward ~2 minutes also dissolves the Boundary-A/B/C bookkeeping
that exists mainly because the suite is slow.

**2.2 Merge proposal + plan into a single "change note" for standard
work.** One artifact, ≤2 pages: what / why / approach / verification /
who reviews. The two-stage survives only for architecture-class
changes. This removes roughly half the lifecycle commits and most of
the duplicated prose — the plan corpus is *larger* than the proposal
corpus it restates. (Now concrete as `convergent-lifecycle`.)

**2.3 Cut the templates to the size we want the artifacts to be.**
Agents mirror the template; a 693-line proposal template teaches
900-line proposals, an ~80-line one teaches ~150. Same for plans,
reviews, and the boards: **one line per row** — the current Queued
board carries 40-line essays per entry.

**2.4 Build the flush: a rule-removal pathway.** Every rule names the
incident it answers; a semiannual (or per-release) scrub asks whether
that hazard is now handled structurally, and removes the rule citing
the replacement — the per-commit-approval rewrite is the precedent.
Incidents promote to doctrine only after **three independent
recurrences**; one bad day is a reflection, not a rule.

**2.5 Ship the light profile as the default.** `templates/core/`
installs the four-part core plus the change-note lifecycle; the full
stack becomes an opt-in "high-assurance" module set. The on-ramp's
Level 1 finally means something an adopter can hold.

### Tier 3 — re-aim the product (strategic)

**3.1 Dogfood the median, not the maximum.** Cairn's own repo runs the
default profile it recommends, escalating per-surface for the genuinely
dangerous parts. Today Cairn is its own most paranoid adopter, so every
shipped default is calibrated against an experience no real adopter
has. **The methodology repo must live like its median adopter, or its
defaults are fiction.**

**3.2 Replace prose-rigor with measurement-rigor, in doctrine.** The
review's centerpiece becomes **one falsification attempt with its
output pasted in** — the thing that caught every real defect —
not thousands of words of reading.

**3.3 Adopt success metrics a hydrologist would respect** — casual,
monthly-ish, no ledger: adopter issue → shipped fix **≤ 2 sessions**;
new adopter → first reviewed commit **≤ 1 hour**; median
proposal/change-note **≤ 150 lines** (today ~900); science-commit share
in `modflow_tools` **> 50%** (today ~25%). When a metric and the
process conflict, the metric shows where the process stopped serving
the mission.

**3.4 Consider that the handbook is the product.** Level 0 — read the
doctrine and let it change how you work — may be Cairn's real unit of
adoption, the way The Turing Way is read rather than installed: a
~50-page handbook plus a one-file starter template, with the machinery
as the worked maximal case study rather than the price of entry.

**3.5 Write the anti-maximalism into the doctrine itself.** Agents do
what the written rules reward, so the rules must say it: *brevity is
praised in review; verbosity is a defect named in review; a reviewer
may block for excessive process exactly as for missing rigor; time is
a budget the artifact spends.* Until cost enters the loss function,
agents re-armor and this note gets written again in six months.

## How to hold the numbers

The caps and targets are **anchors, not scores** (P8). They exist to
break an equilibrium — with no cost function for length, "be concise"
gets interpreted maximally, while a number makes brevity defensible in
review. Mechanized, they become the next zombie. Three handling rules:
caps live in review vocabulary, never in tools (per 1.5); the judgment
items are the mechanism and the numbers only trigger them (two rounds
isn't the point of 1.2 — the author deciding is); and the numbers
**sunset** under 2.4 once the median artifact settles — scaffolding for
a culture reset, not architecture.

## What would falsify this note

* Shortened artifacts measurably letting through defects the long form
  used to catch — audit each shipped defect: would a longer proposal
  (not a better measurement) have caught it? The prediction: almost
  none trace to brevity.
* The parked machinery turning out to be what adopters ask for. (The
  current adopter's four issues were all "your tool doesn't run.")
* The two-round cap producing Maintainer decision fatigue instead of
  speed — then the cap is wrong, not the direction.

## Anti-scope

This note does **not** propose abandoning independent review, the
recorded decision trail, append-only on the artifacts that keep it,
verification for shipped code, or editing history. The four-part core
is the point of Cairn and stays. What goes is the mass around it — the
armor agents grew because nothing in the rules ever told them to stop.
