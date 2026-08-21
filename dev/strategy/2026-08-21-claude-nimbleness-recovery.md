# Nimbleness recovery — shedding process mass without losing the point

**Author**: Claude (Strategy)
**Model**: Fable 5
**Date**: 2026-08-21
**Status**: draft
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
keep, and how do we stop it growing back?**

This note is deliberately short by current Cairn standards. That is not
laziness; it is the first recommendation, demonstrated.

## What the numbers say

All figures as_of 2026-08-21, and all deliberately approximate — the
shape matters, not the third digit.

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

And one lived case, from yesterday (2026-08-20): **an adopter filed four
bug reports** — at bottom a regex fix, a timeout flag, a stale comment,
and an exit-code cleanup. Handling them produced **3 proposals totaling
6,475 lines, ~45 review findings across four rounds each, two external
security reviews, and 57 lifecycle commits in one day — and zero lines
of shipped fix.** The fixes still await plans (median plan: 1,800
lines) before any code may be written. In an ordinary healthy repo this
is three pull requests and a day's work.

The sister repo shows the same signature. In `modflow_tools`, a single
plotting feature (`review_bc_properties_and_stress_periods` — a
boundary-condition review panel) took **three plan-review rounds and six
code-review rounds**; commit subjects there now read as process
narration ("Response to code review round 5 + Boundary B…"). Science
throughput is the casualty: July 2026 saw 10 commits in that repo, and
roughly three-quarters of recent commits are lifecycle traffic rather
than hydrology.

**The honest other side:** the review discipline catches real defects.
Yesterday alone, independent review caught a regex that refused dotted
branch names, a timeout flag Gitleaks rejects, an invariant satisfied
only over an empty set, and a dependency-closure inflation of 580 vs 5.
Those catches are worth keeping. But notice *what caught them*: *someone
ran something* — a fresh repo, a real invocation, a canary, a falsifying
mutation. **Not one of those catches needed a 900-line proposal to
exist.** The rigor lives in the measurements; the mass lives in the
prose. We can keep the first and shed the second.

## How we got here — five ratchets

Naming the mechanisms matters, because cutting mass without disabling
the ratchets means it all grows back.

1. **Every incident becomes a rule, and no rule ever leaves.** The
   doctrine has a rate-limit gate on *adding* rules but no pathway for
   *removing* one. Sediment accretes; nothing flushes. (The one
   counter-example — the 2026-08 rewrite that replaced the blanket
   per-commit approval gate with targeted fences — is the model this
   note generalizes.)

2. **Agents are compliance-maximizers with an asymmetric loss
   function.** An agent is never criticized for a 2,500-line proposal
   but is blocked for any omission. So agents write armor. Rules
   written as "bright line", "refuses", "never" get followed at maximal
   literalism, because nothing in the doctrine prices *time* or
   *length*. Verbosity is currently indistinguishable from rigor — and
   is cheaper for the agent to produce.

3. **Review has no cost side.** Reviewers face no budget: every finding
   is free to file, every round free to demand, and yesterday 45 of 45
   findings were accepted. A reviewer who narrows or extends a process
   can never be shown wrong, because the lighter path is never run.
   Rounds ratcheted from one to four-to-six with no one deciding that.

4. **Self-hosting doubles everything.** Cairn builds Cairn using Cairn,
   so most work *is* process work, and every attempt to lighten the
   process is itself executed at full process weight. The
   `review-efficient-lifecycle` proposal (2026-08-10) diagnosed this
   exactly — *"a process that is robust only when a scientist can
   repeatedly fund very large contexts will be abandoned or performed
   ceremonially"* — and then landed as **more** vocabulary: assurance
   paths, inheritance rules, an activation ledger with its own
   immutability invariants. The immune system attacks the cure.

5. **The triage exists on paper and is dead in practice.**
   `doctrine/proposals.md` already says *"Everything else — a new
   helper, a test, a typo fix — just commit."* But the surface-based
   security triggers, the touched-a-contract clauses, and the culture
   of exhaustive caution capture nearly everything above a typo.
   Yesterday's *bug fixes* became security-reviewed proposals. The
   trivial path atrophied from disuse.

## What must be kept

The irreducible core — the part that actually answers the founding
problem (sloppy vibe-coded output) — is small:

1. **Write intent before code.** A paragraph saying what and why,
   committed, before a substantive change. This is the cairn on the
   trail.
2. **Independent review before it lands.** One structurally-independent
   read, with at least one *falsification attempt* — run the thing, try
   to break it — not a prose audit.
3. **Record the decision.** One line, committed, saying who decided and
   what.
4. **Empirical verification.** Tests for code; a real invocation for
   tools; the claim checker for prose. Measurements, not assertions.

Everything else in the current apparatus is elaboration on those four,
and each elaboration should have to pay rent.

## Recommendations

Three tiers: **Tier 1** is decree — the Maintainer says so, effective
immediately, no proposals required (running these changes through the
full lifecycle would be the disease treating itself). **Tier 2** is
structural — a small number of focused, *lightweight* changes over the
next month. **Tier 3** is strategic — what Cairn is actually for.

### Tier 1 — stop the bleeding (this week, by decree)

**1.1 Impose size budgets, framed as comprehension, not thrift.**
A proposal fits in ~150 lines; a plan in ~300; a review round in ~50; a
commit body in ~10. The justification is already doctrine: the
comprehension floor says an artifact the Maintainer cannot penetrate is
not decidable — **and length is the dominant form of opacity in this
repo**. A 900-line proposal is not rigorous; it is unreviewable. If it
doesn't fit, the thinking isn't done. (Exceeding the budget is a smell
to name in review, not a hard refusal — we are not building another
gate.)

**1.2 Cap review at two rounds — and then the author makes the call.**
After round two, the author decides each open finding — accept,
decline, or defer — records a one- or two-sentence defense, and
proceeds. The reviewer's disagreement is recorded as dissent, not
relitigated. Six-round chains end.

**What does not happen is escalation-by-question.** (Maintainer
direction, 2026-08-21.) The failure mode to guard against is agents
handing the Maintainer arcane disputes they have no ability to settle
— that converts "decide" into "approve", exactly as the comprehension
floor warns. An item reaches the Maintainer only when it is genuinely
theirs — scope, priorities, risk appetite, user-facing behavior — and
it arrives in plain language **with a recommendation and a stated
default** ("we'll do X unless you object"), never as an open question.
If it cannot be posed that way, it is not ready for the Maintainer; it
is the author's to decide and defend. The record protects everyone:
the call and the dissent both live in the artifact, so a wrong call is
visible and cheap to reverse — which is exactly why making it is safe.

There is direct evidence for this design: the Maintainer estimates they
have accepted agent recommendations **~90% of the time or more**. A
gate that approves nine times in ten is not where the judgment lives —
it is latency. The Maintainer's value is concentrated in the tenth
case, and the way to surface that case is a two-sentence
recommendation with a default they can veto on sight, not a bullet
list of open disputes. Design the flow to make the 90% frictionless
and the 10% conspicuous.

**1.3 Give findings a cost vocabulary: `blocking` / `note` / `nit`.**
Only `blocking` requires a written response. A `note` may be taken
silently; a `nit` may be ignored without ceremony. A round that
produces no `blocking` findings *clears* — it does not recycle.

**1.4 Re-arm the just-commit path, explicitly.** A bug fix that comes
with a failing-test reproduction is **code + test + one code review**,
full stop — no proposal, no plan, even when the buggy line lives on a
"security surface." The security-review triggers exist for *new
machinery and changed contracts*, not for fixing a regex inside
existing, already-reviewed machinery. Adopter-filed bugs get a service
target: **fixed and shipped within two sessions.** (The three accepted
proposals from yesterday should be implemented directly from their
Decision summaries — short plans of a page each, not 1,800 lines.)

**1.5 Every tool becomes advisory: warn, never bind.** (Maintainer
direction, 2026-08-21.) A check that fires is information; a check that
*blocks* is a decision delegated to a script. The tools should keep
firing — the intent-tracker note, the lifecycle checks, the claim
flags are all useful signal — but demoted from refusal to loud
warning. The ~170 "refuse/refusal" occurrences in the table above are
the work list: the broad-run guard's `CAIRN_FULL_SUITE=1` gate,
transition-lint hard stops, lifecycle-planner and ledger refusals all
become warnings a human can read and overrule in the moment. Binding
survives only where the property is genuine safety rather than process
conformance: the scaffold engine's symlink/containment check (it
writes into someone's tree), and trust-root verification during an
actual release ceremony. Everything else advises.

**1.6 Declare a construction moratorium.** No new doctrine files, no
new gates, no new lifecycle vocabulary, no new ledgers or trackers,
until the Tier-2 removal pass is complete. The rate-limit gate slows
additions; this halts them while we flush.

**1.7 Commit subjects go back to normal.** "Fix dotted-branch refusal
in inert-key fence" — not a narrated arc. The record's story lives in
the artifacts, once, not in every subject line.

### Tier 2 — remove mass (this month)

**2.1 A keep/park/kill pass over the apparatus.** One session, one
table, Maintainer decides each row. Suggested starting dispositions:

* **Keep** (cheap, catches real defects, serves adopters): the scaffold
  engine and its tests; `claim_check.py`; `link_check.py`; the
  quality-gate neutrality check; the four-part core above.
* **Park** (defends hazards no current adopter has; archive the code,
  keep the lesson): the differential-oracle gate anchor and its
  preflight, AST attestation, `transition_lint.py`, the pilot
  activation/event ledgers, the intent log and its pruning machinery,
  the slot ratchet, most of the ~10,500 lines of lifecycle tooling.
  A project with one adopter does not need airport security.
* **Diet**: the test suite. 4,468 tests at ~10 minutes mostly defend
  the parked machinery; pruning to what defends shipped adopter value
  should land near **~2 minutes** — which also dissolves the
  Boundary-A/B/C bookkeeping that exists mainly because the suite is
  slow.

**2.2 Merge proposal + plan into a single "change note" for standard
work.** One artifact, ≤2 pages: *what / why / approach / how verified /
who reviews*. The proposal→plan two-stage survives only for
architecture-class changes (new abstractions, contract breaks, the
scaffold engine). This alone removes roughly half the lifecycle commits
and most of the duplicated prose — the plan corpus is *larger* than the
proposal corpus and restates much of it.

**2.3 Cut the templates to the size we want the artifacts to be.** The
proposal template is 693 lines; agents mirror the template. A template
of ~80 lines teaches ~150-line proposals. Same for plans, reviews, and
the PLANNING.md board: **one line per row** — kind, stem, status,
owner. The current Queued board carries 40-line essays per entry;
essays go in the artifact or nowhere.

**2.4 Build the flush: a rule-removal pathway.** Every rule in
`AGENTS.md` and `doctrine/` must name the incident it answers. Twice a
year (or at any release), a scrub asks of each rule: *is this hazard
now handled structurally — by a fence, a test, a tool?* If yes, the
rule is removed, citing the replacement. The per-commit-approval
rewrite is the worked precedent. Incidents accumulate in a lightweight
log and are promoted to doctrine only after **three independent
recurrences** — one bad day is a reflection, not a rule.

**2.5 Ship the light profile as the default.** `templates/core/` should
install the four-part core plus the change-note lifecycle. The full
stack — security ceremonies, gate anchors, measurement ledgers —
becomes an explicitly opt-in "high-assurance" module set for teams that
need it (regulated environments, released libraries with users). The
on-ramp's Level 1 finally means something an adopter can hold.

### Tier 3 — re-aim the product (strategic)

**3.1 Dogfood the median, not the maximum.** Cairn's own repo should
run the *default* profile it recommends — light, with per-surface
escalation for the genuinely dangerous parts (the scaffold engine, the
security tooling). Right now Cairn is its own most paranoid adopter,
which means every shipped default is calibrated against an experience
no real adopter has. **The methodology repo must live like its median
adopter, or its defaults are fiction.**

**3.2 Replace prose-rigor with measurement-rigor, in doctrine.** The
whole recorded history says the valuable findings came from running
things: fresh-repo canaries, real invocations, falsifying mutations,
the 580-vs-5 closure walk. Rewrite the review ask accordingly: a
review's centerpiece is **one falsification attempt with its output
pasted in**, not thousands of words of reading. One measurement
outranks a page of argument. This keeps everything that made yesterday
valuable and drops everything that made it slow.

**3.3 Adopt success metrics a hydrologist would respect.** Casual,
monthly-ish, no ledger machinery:

* Adopter issue → shipped fix: **≤ 2 sessions** (yesterday: ∞ so far).
* New adopter → first reviewed commit in their own repo: **≤ 1 hour**.
* Median proposal/change-note length: **≤ 150 lines** (today: ~900).
* Science-commit share in `modflow_tools`: **> 50%** (today: ~25%).

When a metric and the process conflict, the metric is telling you where
the process stopped serving the mission.

**3.4 Consider that the handbook is the product.** Level 0 — *read the
doctrine and let it change how you work* — may be Cairn's real unit of
adoption, the way The Turing Way is read rather than installed. A
~50-page readable handbook distilled from the 6,300 lines of doctrine,
plus a one-file starter template, might serve more scientists than the
entire bootstrap apparatus. The machinery then becomes the case study
("here is what a maximal instance looks like"), not the price of entry.

**3.5 Write the anti-maximalism into the doctrine itself.** Agents will
keep doing exactly what the written rules reward. So the rules must
say, in words: *brevity is a virtue to be praised in review; verbosity
is a defect to be named in review; a reviewer may block for excessive
process exactly as for missing rigor; time is a budget the artifact
spends.* Until cost appears in the loss function, compliance-maximizing
agents will re-armor, and in six months this note gets written again.

## How to hold the numbers

The caps and targets above are **anchors, not scores**. They exist to
break an equilibrium — agents currently have no cost function for
length or time, so "be concise" gets interpreted maximally, while a
number makes brevity concrete and defensible in review. But a cap that
gets mechanized becomes the next zombie: a linter refusing line 151, a
dashboard scoring sessions, agents gaming "≤2 sessions" by skipping
verification. Three handling rules:

* **Caps live in review vocabulary, never in tools** (per 1.5 — a
  reviewer *names* an oversized artifact; nothing refuses it).
* **The judgment items are the mechanism; the numbers only trigger
  them.** Two rounds isn't the point of 1.2 — the point is that
  disagreement then goes to a human. Metrics in 3.3 are staff gauges
  you glance at, not control structures.
* **The numbers sunset.** Once the median artifact settles near sane
  size and 3.5's cost-awareness is in the doctrine, the caps come out
  under the same rule-removal pathway as everything else (2.4). They
  are scaffolding for a culture reset, not permanent architecture.

## What would falsify this note

* If shortened artifacts measurably let defects through that the long
  form used to catch — track it: when a shipped defect surfaces, ask
  whether a longer proposal (not a better measurement) would have
  caught it. The prediction here is that almost none trace to brevity.
* If the parked machinery turns out to be what an adopter actually
  asks for. (The current adopter's four issues were all "your tool
  doesn't run" — evidence pointing the other way.)
* If the two-round review cap produces Maintainer decision fatigue
  instead of speed — then the cap is wrong, not the direction.

## Anti-scope

This note does **not** propose: abandoning independent review,
abandoning the recorded decision trail, weakening the append-only rule
on the artifacts that remain, dropping verification for shipped code,
or editing history. The four-part core is the point of Cairn and stays.
What goes is the mass around it — the armor that agents grew because
nothing in the rules ever told them to stop.
