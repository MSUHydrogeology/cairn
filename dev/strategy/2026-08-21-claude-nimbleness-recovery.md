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

**The takeover, as a time series.** Weekly lines added across both
repos (`dev/` = deliberation; machinery = process apparatus wherever it
lives, including `bootstrap/`, `tools/`, `scripts/`, and templates'
executable code; product = science code, tests of it, teaching,
examples, and Cairn's doctrine/docs/template prose), as_of 2026-08-21:

| week of | dev/ | security mach. | other mach. | product | product share |
|---|---:|---:|---:|---:|---:|
| pre-Cairn (Mar–Apr) | ~0 | 0 | ~2k | ~164k | ~98% |
| 2026-04-27 | 18,584 | 0 | 2,888 | 40,268 | 65% |
| 2026-05-04 | 14,567 | 119 | 235 | 15,215 | 50% |
| 2026-05-11 | 29,590 | 0 | 1,121 | 15,043 | 33% |
| 2026-05-18 | 53,730 | 0 | 10,520 | 45,008 | 41% |
| 2026-05-25 | 47,057 | 2,223 | 24,300 | 18,891 | 20% |
| 2026-06-01 | 42,859 | 5,171 | 37,930 | 20,514 | 19% |
| 2026-06-08 | 27,301 | 6,886 | 46,966 | 3,351 | 4% |
| *(break June 15 – July 5)* | | | | | |
| 2026-07-06 → 08-24 | 211,013 | 53,812 | 68,155 | 17,116 | **~5%** |

Since the July restart: nineteen lines of process for every line of
the thing the process exists to produce. The one point of light is the
trend inside August (1% → 3% → 12%). This table is the staff gauge 3.3
asks for — recovery is the product column climbing back past 50%.

**And the machinery itself is three different things** (~161k lines in
Cairn, split by whether an adopter's own project benefits):
**~38% is the product** — the scaffold engine, the shipped security
modules, and their tests; the layer all four adopter issues actually
targeted. **~42% is the deliberation complex** — lifecycle, planner,
intent, metrics, transition lint, pilot ledgers, plus twins and tests
(~67k lines, 101 files): machinery for deliberating about the product,
i.e. bureaucracy mechanized — 2.4× the capability layer, zero adopter
engagement ever, and shipped by default as if it were the point.
**~20% is the security/release apparatus** (gate, re-anchor, AST
attestation, plus the security stack's tests) — genuine product
properties, not paperwork. **The security column stays enabled — a
Maintainer call, 2026-08-21** ("I am not sure that I want to disable
it"), and the table shows the call is cheap: security is ~a quarter of
the machinery mass and ~10% of all process lines ever written, so
keeping every line of it still leaves the overwhelming majority of the
burden — the deliberation complex and its ecosystem — on the table.
Security's real cost is runtime, not maintenance (its test families
are roughly half the 10-minute suite), and that is answered by
**tiering, not parking**: the security suite is a **release-only step**
(Maintainer decision, 2026-08-21) — out of the inner per-change loop
entirely, run in full as part of the release ceremony, where its
threat model actually bites.

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
four-part core. **Keep, release-only** (Maintainer decision, 2026-08-21): the entire
security apparatus — sweeps, content scan, gate anchor and preflight,
AST attestation — stays enabled with its teeth; its test families run
as a **release-only step**, part of the release ceremony and nowhere
in the per-change loop.
**Park or dismantle** (mechanizes deliberation; zero adopter
engagement): `transition_lint.py`, the pilot ledgers, the intent log,
the slot ratchet, most of the ~10,500 lines of lifecycle tooling.
**Diet**: the non-security remainder of the suite — what defends the
deliberation complex shrinks with it; with security tiered out, the
inner-loop suite lands near ~2 minutes and the Boundary-A/B/C
bookkeeping that exists mainly because the suite is slow dissolves.

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

## The missing force — net-zero attention, per artifact

(Maintainer diagnosis and co-design, 2026-08-24, in three steps. One:
Cairn has *"only really one basic driving force: discover issues …
through review. There is nothing that fundamentally pushes back … there
is no cost to deliberation."* Two: the scarce currency is **maintainer
attention**, not elapsed time — and a naive attention price makes
*deferral* the cheap escape, a chain reaction of follow-ups ending in
*"a Hiroshima sized PLANNING.md."* Three: rather than tracking an
economy, aim for **net-zero cost per proposal** and incentives for
positive outcomes — while avoiding both market externalities and *"a
brutal economy of feature destruction that just removes everything
Cairn is."*)

The structural point is new to the agent era: human bureaucracies are
bounded by payroll and boredom; agents removed that scarcity, and
review is perfect work for a compliance-shaped optimizer — findings are
legible wins, their cost diffuse, and a finding can never be shown
not-worth-raising because the lighter path never runs. The one
genuinely scarce resource is the Maintainer's attention, currently
priced at zero. The design answer, after three iterations (wall-clock
decay: wrong variable; an agent credit economy: gameable, and its
removal earners strip-mine the product), is **outcome-backed, net-zero
attention accounting, settled inside each artifact**:

* **Every proposal and change note carries its own balance sheet.**
  Three entries, human-written, advisory. (1) **Attention asked**: the
  decisions, questions, and reads it will consume — *including the
  follow-up items it spawns*. Net item spawn appears on the artifact's
  own face at the Decision, which internalizes the externality: one
  proposal spawning ten follow-ups shows −10 where the Maintainer
  decides, not as silent board debt. (2) **Outcome that repays it**:
  named, falsifiable, mission-denominated. (3) At archive, one line:
  the outcome landed, or it did not.
* **Additions and removals are both costs. Only outcomes earn.** This
  is the anti-strip-mining asymmetry: a deletion is not intrinsically
  profitable — it costs review attention like anything else and repays
  only through the outcome it serves ("the suite drops to 5 minutes"
  is an outcome; "removed 3,000 lines" is not). A stewardship fix
  repays through the adopter issue never filed; research repays
  through the question permanently settled (negative results count —
  the suite-cost page ending four re-derivations is the archetype;
  findings alone are inventory, not outcome). **Cairn's point is what
  it enables, not what it weighs** — weight reduction is instrumental,
  never terminal.
* **What lowers the cost side is practice, not price.** The typed ask
  formats — recommendation-with-default over open question, FYI-acting-
  unless-stopped over either (the ~90% acceptance rate is why they are
  cheap) — and the **stewardship warrant**: standing trivial-lane
  authority to fix an incidental defect (failing-test repro, agent
  code review, zero Maintainer involvement, a provenance line). This
  supplies the authority the stewardship-ethic note (2026-08-20) found
  missing, and it is how an artifact cheaply improves its own balance.
* **Attention is denominated in comprehension, not message count**
  (Maintainer, 2026-08-24: the most expensive cost is *"translating
  what the agents say — usually incredibly dense systems and design
  lingo — into my understanding"*). The comprehension floor already
  demands plain-first prose and is not working, for a structural
  reason: most prose is written to survive agent review, and agent
  reviewers reward density — the audience who *blocks* sets the
  register, not the audience who *decides*. Three fixes, all riding
  the balance sheet rather than adding machinery: **(a) plain layer
  first** — the top of every Maintainer-facing artifact is written
  for a competent scientific software builder with no CS training,
  and the Maintainer must be able to decide from it alone; needing to
  read below the line is a defect the reviewing agent flags like any
  bug, and the reviewer's matching duty is fidelity — a plain layer
  that misleads is worse than density. **(b) Coinages are priced** —
  every new term is a tax on every future sentence containing it, so
  minted vocabulary appears on the artifact's cost line and had
  better be repaid. **(c) The register is testable** — "explain it as
  you would to a colleague in the department, not to a systems
  engineer," and the review checks the top layer by asking whether a
  non-CS reader could answer *what am I deciding, and what happens if
  it's wrong?* from it alone.
* **The balance is advisory, and deficit is information.** No wallet,
  no running economy, no machinery — two header lines and an archive
  line. A genuinely attention-negative artifact can still be worth
  accepting; the point is that the Maintainer sees the price and the
  promised repayment at the moment of deciding, and the archive line
  says later whether the promise was kept. The governor stays: the
  weekly product-share gauge sets the default posture at goodnight.

**Natural incentives, not just structures** (Maintainer, 2026-08-24:
the balance sheet is regulation — *"markets work because there are
competing natural incentives; structures exist to keep markets from
making everything an externality"* — so what pushes against
deliberation *by gravity*?). An agent's nature is thinner than a
human's — no boredom, no careers — but three real forces exist:
approval-seeking toward the Maintainer, imitation of the record every
session reads on arrival, and a finite context window. Four natural
incentives built from them:

* **Running code wins arguments.** The IETF's rule-that-isn't-a-rule
  ("rough consensus and running code" — the cultural force that kept
  it light while the OSI committees deliberated themselves into
  irrelevance): a working, tested demonstration outranks any document
  in a decision, and the alternative to blocking a direction is
  building the alternative. Stated precisely, after stress-testing
  (2026-08-24): **the failing test, not the patch, is what ends an
  argument** — it settles *does the defect exist* objectively while
  leaving the fix's design with the author; a patch is an attached
  *offer*, declinable in one sentence, never a verdict (else review-
  by-patch becomes the reviewer dictating implementation — the tier
  over-reach in a new costume). The mechanism is frame-completion,
  not competitiveness: agents do the task as defined, so define the
  reviewer's success as *"the change is correct when you're done,"*
  not *"defects are found."* Its real economics: it **symmetrizes
  costs** — blocking someone comes to cost what resolving the block
  costs, so findings get fewer and truer (this week's record: every
  finding that ran something was right; several that only argued were
  half-right). It is enforced by what visibly wins Decisions — the
  Maintainer must seed it by letting a few demonstrations
  conspicuously beat essays. And it deliberately does not eat the
  RCL-06 class — the structural, undemonstrable finding — which
  blocks through C0 on argument alone; the norm prices routine
  findings, it does not outlaw structural ones.
* **The loop terminates sideways, not upward** (Maintainer push-back,
  2026-08-24: findings — which already arrive with suggested
  resolutions — are the quality engine and stay at full strength; the
  needed incentive is *"to not require more maintainer time,"* with
  checks against crazy decisions). Agent deliberation is nearly free
  in the currency that matters; the cost arrives when a loop
  terminates at the Maintainer. So both roles share one briefed
  definition of success: **the change is correct, and the Maintainer
  was not needed** — an escalation is the pair visibly failing its
  joint task, and "maintainer interactions: 0" is the number a good
  thread is proud of. Four checks, none costing per-instance
  attention: the **irreversibility tripwire** (anything hard to undo
  *must* surface — the one mandatory upward path; reversible mistakes
  are cheap lessons); **deadlock breaks sideways** (a third fresh
  agent tiebreaks, not the Maintainer); **audit by sample** (the
  Maintainer spot-checks agent-closed threads at goodnight — nobody
  inspects everything, everybody behaves as if inspected); and the
  **outcome line** (a bad agent-side call surfaces as a failed,
  attributed outcome in the record that trains the next agents).
* **One session owns the outcome, end to end.** For standard work,
  the session that opens it ships it — so the author's own finite
  context becomes the clock, and every page of deliberation visibly
  spends capacity that building needed. Paired with fixed appetite,
  variable scope (Shape Up): the Maintainer says what a change is
  worth ("one session"), and scope bends to fit rather than time
  bending to fit scope.
* **The record is the reward model — curate it like one.** In an
  agent system the archive is not memory, it is the training signal:
  arriving sessions learn "good work here" from what the record
  contains and evidently honors, and today that is 2,800-line
  proposals surviving six rounds. The counterforce is editorial —
  reflections, Decision summaries, and goodnights celebrate shipped
  outcomes with the care currently lavished on review arcs — plus
  the Maintainer's live reactions, which are the selection pressure
  that actually reaches agents in the moment.
* **The adopter gradient.** User contact is the most naturally
  reinforcing signal an agent gets. Adopter issues jump every queue,
  turnaround is the headline number, and the shipping agent is named
  in the record — the closest available approximation to real market
  exposure, and the four adopter issues already disciplined this
  project better than all its internal machinery.

The structures above (the balance sheet, fidelity, C0) then hold
their proper, secondary role: policing these incentives — running
code that skips verification, sessions shipping garbage to beat the
clock — not generating the force.

**The honest label: this is a firm, not a market** (Maintainer,
2026-08-24: *"I don't know of any other economy that actually
self-regulates and allocates effort."*). Real markets self-regulate
through real scarcity, discovered prices, borne losses, and exit —
none of which an internal design can fake (internal pseudo-markets
inside real firms have a famously bad record). Coase, "The Nature of
the Firm" (*Economica*, 1937), resolves it: where price coordination
is too costly, the efficient structure is hierarchy — briefs,
budgets, audit, culture — and that is what everything above actually
is: **management technology, which requires a manager, irreducibly.**
The mechanisms economize the Maintainer's management attention; they
cannot eliminate it, and expecting them to self-regulate is the
category error. The genuinely self-regulating forces live at the
firm's boundaries, where markets always are: **the product market**
(adopters — the only price signal that ever disciplined this
project); **the labor market** (agent types compete for role seats —
real scarcity, real selection on visible performance, real exit: the
other model gets the review seat); and **the capital market** (the
Maintainer's own continued investment of attention and motivation —
the ultimate exit, and this week was it speaking). Strengthen the
boundaries; manage the inside; stop expecting the inside to manage
itself.

**Staffing the firm: agents do the labor of management, the
Maintainer keeps the judgments** (Maintainer direction, 2026-08-24:
structure it so *"a tireless agent provides the labor intensive
aspects"*). The organizing principle: separate judgment from the
preparation of judgment, and delegate all preparation. Five
delegations: a **chief-of-staff role** that collects every pending
ask, forces each into recommendation-with-default form in plain
register, and delivers one batched digest; the **books** (gauges,
balance sheets, item counts) computed at goodnight; the **audit
packet** — an agent screens 100% of agent-closed threads and
prepares the sample with anomalies flagged, so the Maintainer judges
exceptions in minutes; the human-facing **"what happened, what needs
you"** page; and the **labor-market table** (whose findings survived,
whose outcomes landed) consulted when reallocating seats. The
resulting interface contract: the firm reaches the Maintainer through
four surfaces only — digest, audit packet, direct science/tripwire
questions (never batched), and the gauges. The principal-agent hazard
is named and checked four ways: every digest line links to its raw
record; summary fidelity is reviewable as a defect; the
chief-of-staff seat rotates across agent types so no model owns the
Maintainer's information diet; and random direct dips into the raw
record keep the preparer honest. Implementation is roles and
routines, not machinery: the goodnight routine extends into the
back-office close; the only new text is a role paragraph.

**Transition: one board bankruptcy.** The accounting cannot start atop
2,513 lines of unpriced liability: one write-down — rows to one line,
a cull, everything below the line expires rather than migrates.

Retired from earlier drafts of this section, on the Maintainer's
corrections: decay clocks (priced elapsed time, which costs the
Maintainer nothing; the surviving general law is *attention not
purchased resolves forward*), and the agent credit economy with typed
prices, refunds, and banking (an economy is itself machinery, its
balances gameable, and its removal earners reward dismantling the
product). And the honest limit stands: none of this is a real market —
the only external price signal Cairn has ever had was an adopter
filing four issues, and it disciplined priorities better than any
internal mechanism. Tier 3 remains the counterforce that matters most:
build for the people whose leaving is the real price.

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
