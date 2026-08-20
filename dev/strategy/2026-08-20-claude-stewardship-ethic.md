# Stewardship — the work that never enters a lifecycle

**Author**: Claude (Strategy)
**Model**: Opus 5
**Date**: 2026-08-20
**Status**: draft
**Type**: design-exploration
**Surfaces this would feed**: the guide star
(`2026-05-14-claude-human-ai-team-development-framework.md`) as a plank;
`doctrine/proposals.md` > Triage; `docs/solo-legacy-recipe.md`; the slot set in
`templates/core/dev/proposals/_template.md`

## The question / felt gap

An agent that notices a small, obviously-correct defect while working on
something else should fix it — the way a citizen picks up litter rather than
filing a report about it. The felt pain is two-sided: small decay accumulates
unnoticed, **particularly in docs**, and work that could have been done in
passing instead becomes a roadmap row.

The scope is **not Cairn's own tree.** Cairn's record has been extensively
proposed, debated, planned, and reviewed; its defects are the ones that survived
review, not the ones nobody looked at. The target is the tree Cairn *adopts
into*: a scientific codebase authored over years or decades, where nobody ever
decided the current state — it accreted. And this is not purely a legacy
problem. Drift accumulates in any long-lived tree, which is why the framing here
is an **ethic** rather than a migration step.

The evidence is observational and unrecorded, as the Maintainer states plainly.
This note therefore explores; it does not conclude.

One clarification of what the topic is *not*. This is not a request for agents
to have more authority over what they change. It is about a class of work that
never enters a lifecycle at all — in either direction.

## Method

Read: the guide star; `doctrine/proposals.md` > Triage; `AGENTS.md` on scope
deviation and verification boundaries; `dev/strategy/README.md`;
`docs/solo-legacy-recipe.md`; the shipped slot set in
`templates/core/dev/proposals/_template.md`. Measured the composition of
`dev/PLANNING.md`. Searched `doctrine/`, `dev/`, and `templates/` for prior
deliberation on incidental fixes.

**One methodological caution, recorded because it nearly produced a wrong
finding.** A first search for stewardship vocabulary (`boy.?scout`, `broken
window`, `litter`, `opportunistic refactor`) returned only false positives —
`litter` matching inside `splitter` — and the absence read as "greenfield." It
is not: the concept is already in the guide star under entirely different words
(Finding 2). The pattern could not have matched the concept, so its silence was
never evidence. This is `AGENTS.md` > *Confirm the instrument before trusting an
absence*, and concept search is exactly where it bites: **a vocabulary grep
tests the vocabulary, not the idea.**

**What would falsify this note's direction:** an evidence pass over a real
legacy tree showing either that the fix-in-passing class is rare, or that its
members stop being small once examined. Both are checkable — see *Open
questions* (1).

## Findings

### 1. The permission already exists; the gap is not authority

`doctrine/proposals.md` > Triage already closes with: "Everything else — a new
helper, a test, a typo fix, a docstring polish, a self-contained refactor — just
commit." The escape hatch widens it further for anything urgent, reversible, or
experimental.

So a stewardship doctrine that grants the permission a second time, more warmly,
changes nothing. **Whatever suppresses the behaviour is not a missing rule** —
and a proposal that assumes otherwise ships a paragraph and no behaviour change.
Everything below is an attempt to find the actual cause.

### 2. The guide star already carries half of this, under other vocabulary

"Restraint as design center" > "The default is currently backwards" records the
same pathology from Cairn's own side: triage separates trivial from substantive,
but in practice everything routes to the heavy path unless the maintainer
intervenes — with two dated instances of the Maintainer asking "why not just do
it?" It is grounded on **Anchor 17** (Poppendieck & Poppendieck 2003; Boehm &
Turner 2003; Saltzer & Schroeder 1975) and already registered in *Still open* as
gap **(17)**, "The default routes to ceremony."

**But it is genuinely only half.** The existing plank is about the *cost of the
path* travelled by work that **entered** a lifecycle: someone decided this
needed doing, and the ceremony over-charged them. Stewardship is about work that
**never enters a lifecycle at all** — nobody proposed it, nobody filed it,
nobody noticed. Restraint asks *how heavy should this path be?*; stewardship
asks *what happens to what is never put on a path?* The first is a question
about ceremony, the second about attention.

Same design center, different failure surface. That distinction is this note's
central claim, and the first thing to attack.

### 3. Cairn's own board is the wrong population — with a number

The Queued section of `dev/PLANNING.md` runs 693 lines over 22 items — **~31.5
lines per item**; the deferred-follow-up register runs ~29. These are tagged,
dated, multi-part entries with sub-breakdowns. Nearly none of them is something
an agent could have fixed in passing.

So on Cairn, a stewardship norm would remove a handful of rows from a 2,375-line
board. That confirms the Maintainer's reframe with a measurement rather than an
intuition, and it carries a constraint: **Cairn cannot serve as its own evidence
base here.** Any evidence pass has to run on an adopter-shaped tree.

### 4. Filing dominates fixing, and it is a gradient, not a values failure

Filing costs one line, is always defensible, and can never be shown wrong.
Fixing costs a commit, Boundary A verification, the standing gates for every
touched surface, and sometimes a re-anchor. Under any uncertainty, filing
strictly dominates.

Two consequences. **Exhortation cannot move a gradient** — the doctrine has to
change a cost, not a sentiment. And **"minor" is a property of the surface, not
of the change**: a one-line docstring fix inside `bootstrap/_scaffold/` summons
the Bandit gate and the AST attestation baseline. Any stewardship licence must
therefore be surface-indexed, which is fortunate, because `AGENTS.md` already
names the surfaces where nothing is ever minor.

### 5. The literature is about the opposite failure — and this should shape the mechanism

Every source below assumes tidying is **under-supplied**, because for humans it
is: it costs attention, earns no credit, and someone else might do it. That is
the bystander-and-commons structure, and the Boy Scout Rule is a remedy for it.

**Agents have none of those brakes.** Near-zero marginal cost to touch a file,
no felt cost for the reviewer's time, no embarrassment at a forty-file diff, and
a strong pull toward visible thoroughness. Point an agent at a decade-old tree
with "leave it better than you found it" and the failure mode is not that
nothing gets tidied — it is a nine-hundred-line cleanup tangled into an
unrelated change.

**The human problem is under-supply; the agent problem is over-supply.** A
doctrine written from the human literature will aim at the wrong one. What
agents need is a **licence with a fence** — a ceiling, a stop rule, and a
refusal list — not encouragement. The exhortation half is nearly free to write;
the fence half is the entire design.

### 6. The strongest counter-consideration threatens Cairn's own product

The tangled-change literature finds that bundling unrelated changes into one
commit degrades both review quality and any later reconstruction of what the
commit did. **Cairn's product is the legibility of its record.** A stewardship
norm that lets cleanups ride inside lifecycle-transition commits attacks the
differentiator directly.

That is not a reason to reject the idea; it is the binding design constraint.
**A stewardship fix never shares a commit with anything else** — already
compatible with one-commit-per-transition and with path-scoped commits, so it
costs no new mechanism.

Two further cautions from the same literature: some refactoring categories
measurably induce bugs, so "obviously harmless" is an empirical claim rather
than a definition; and low-ownership contributors correlate with more defects,
which is close to the definition of an agent passing through unfamiliar code.

### 7. Docs are the high-yield, low-risk surface — and Cairn already knows why

The Maintainer named docs specifically, and docs are where the case is strongest
on both sides of the ledger:

* **Decay is silent.** No test fails when a doc goes stale, so the normal
  detector is simply absent — the unnoticed accumulation described in the felt
  gap is what theory predicts.
* **The verification cost is lowest.** Prose work runs its claim, link, snippet
  and neutrality gates rather than the suite, so the Finding 4 gradient is at
  its shallowest here.
* **The tangling risk is smallest.** A doc fix rarely needs to ride inside a
  code commit, so the Finding 6 constraint costs almost nothing to honour.

`docs/DOCUMENTATION_PLAN.md` already answers *where a doc belongs*. What no
document answers is **who fixes one when it rots.** A docs-first stewardship
licence is the narrowest defensible version of this idea, and probably where a
pilot belongs.

### 8. Cairn ships five extensibility slots, and every one adds obligation

`templates/core/dev/proposals/_template.md` carries `triage-extra-triggers`,
`assurance-path-triggers`, `documentation-tier-home`, `tests-tier-home`, and
`examples-smoke-home`. `docs/solo-legacy-recipe.md` teaches an adopter to fill
the first — with an *additional* proposal trigger.

**There is no slot for routing work out of the heavy path.** An adopter can
tighten their triage through a supported, documented seam, and can loosen it
only by editing prose Cairn shipped them. That asymmetry is a small, concrete,
checkable instance of gap (17) — and unlike the rest of this note, it could be
fixed cheaply without any new doctrine at all.

## Literature — a candidate Anchor 18

**Status: unverified.** Recalled, not checked. The guide star's anchors carry
full citations with resolvable identifiers; **verification is a precondition of
promotion**, per `AGENTS.md` > Verifying claims. This block exists so the
*shape* of the anchor is visible, not so it can be cited.

* **The norm.** Martin, *Clean Code* (2008), and his essay in *97 Things Every
  Programmer Should Know* (2010) — the Boy Scout Rule. Hunt & Thomas, *The
  Pragmatic Programmer* (1999) — "don't live with broken windows." Fowler,
  "Opportunistic Refactoring" (bliki, c. 2011), which is the most operationally
  useful of the three because it is a *scoping rule* rather than an exhortation:
  tidying rides along with work already being done.
* **Decay as an empirical claim.** Lehman's laws of software evolution; Eick et
  al., "Does Code Decay?" (IEEE TSE, 2001); Cunningham's technical-debt metaphor
  (OOPSLA 1992).
* **Norm salience — the better half of the litter analogy.** Cialdini, Reno &
  Kallgren (1990) ran the actual littering field experiments and found that a
  *single* piece of litter in an otherwise clean environment suppressed
  littering more than a pristine environment did, because the lone piece made
  the norm salient. The mechanism is **visibility of the norm, not absence of
  disorder** — which, if it transfers, says a doctrine that makes stewardship
  *countable* will beat one that makes the tree tidy.
* **The counter-evidence (Finding 6).** Herzig & Zeller, "The Impact of Tangled
  Code Changes" (MSR 2013); Kirinuki et al., on committing tangled changes
  (ICPC 2014); Bavota et al., "When Does a Refactoring Induce Bugs?" (SCAM
  2012); Bird et al., "Don't Touch My Code!" (FSE 2011).
* **The contested one.** Wilson & Kelling (1982) is the origin of the
  broken-windows metaphor, and the criminological theory is seriously disputed
  — Harcourt & Ludwig (2006) is the standard rebuttal. **Cite it as the
  metaphor's lineage, never as evidence.** A methodology whose differentiator is
  rigor cannot lean on a contested result for a decorative point.

## Options

**O1 — Do nothing.** Gap (17) stays open and the existing triage permission
stands. Cheapest, and defensible while the evidence is observational. Cost: the
thing the Maintainer keeps noticing keeps happening, unmeasured.

**O2 — Fold into the existing Restraint plank**, as a subsection under "The
default is currently backwards", reusing Anchor 17. The cheapest real move; no
new anchor. Risk: Restraint argues for doing *less* and stewardship for doing
*more, unbidden*, so filed there it reads as a corollary when it is partly a
tension — and the guide star's own discipline is that the mismatches are the
interesting part.

**O3 — A new plank plus Anchor 18**, either within Restraint or as a third
design center beside Trust and Restraint. Honest about the tension, and the
anchor index is explicitly append-only to allow exactly this. Cost: a design
center is a large claim, and this one currently rests on unrecorded observation.

**O4 — Ship it adopter-facing.** A stewardship section in
`docs/solo-legacy-recipe.md`, and/or a sixth template slot letting an adopter
*widen* the just-commit path the way `triage-extra-triggers` lets them narrow it
(Finding 8). This is the only option that reaches the messy trees the felt gap
is actually about; O2 and O3 only set direction.

**Sequencing.** O2/O3 and O4 are complements, not rivals — the guide star sets
direction, doctrine and templates ship it. The real choice is **whether the
guide-star plank is written before or after the evidence pass.**

## Recommendation

**Write the plank last. Start with the narrowest thing that produces evidence.**

1. **Evidence pass first, on an adopter-shaped tree** — LHM, the legacy-rooted
   retrofit already named as a case study, not Cairn (Finding 3). It will not be
   conclusive; it does not need to be. It needs to answer one question: *is the
   fix-in-passing class real and small, or does it dissolve into ordinary work
   once examined?* Because Finding 5 says the risk is over-supply, the pass must
   count **both** directions — what should have been fixed and was not, and what
   was tidied that should have been left alone.
2. **Then O2, with the tension stated rather than smoothed.** On current
   evidence stewardship is a **second face of gap (17)**, not a third design
   center. It earns its own anchor when there is a measurement behind it; today
   there is an observation. Writing it up as a design center now would be the
   recursive-bloat failure the guide star names — in the very section the plank
   would sit next to.
3. **Then O4, docs-first** (Finding 7): the narrowest surface, the shallowest
   cost gradient, the smallest blast radius, and the one where the Maintainer's
   observation is sharpest.

**Residual risk, stated plainly.** This note may be over-thinking a norm that
could be one sentence in `AGENTS.md`. That is live, and it is why the note is
short and the first move small. The counter-argument is Finding 5: the
one-sentence version is precisely the version that produces nine-hundred-line
cleanups, because the half people remember is the exhortation and not the fence.

## Open questions

1. **What does the evidence pass measure?** Sketch: sample N commits from a
   legacy tree; classify each observed-but-unfixed item as
   could-have-been-fixed-in-passing vs. needed-deliberation; separately count
   tidying that happened and should not have. Needs a sampling frame and an
   operational definition of "in passing" before it is worth running.
2. **What is the fence made of?** A per-session ceiling, a surface refusal list
   (contract, high-risk, trust-ceremony — all already named in `AGENTS.md`), a
   "stop at the first one that needs a decision" rule, or some combination.
   Finding 5 says this is the whole design.
3. **Does the licence need a marker?** A commit trailer would make the class
   countable and let the doctrine evolve under evidence per the rate-limit rule
   — the Cialdini reading of norm salience. Against: new mechanism for an
   unmeasured problem is exactly what Restraint warns about.
4. **How does this resolve against the scope-deviation rule?** `AGENTS.md` holds
   that accepted scope is a floor and deviating needs asking; stewardship points
   the other way. If the deviation rule stays silent, it wins by default and any
   new doctrine is inert. **This must be settled explicitly, in both files, or
   O2 and O4 will not change behaviour** (Finding 1).
5. **Is a sixth template slot the right mechanism for Finding 8**, or does the
   asymmetry want fixing in the shipped triage prose instead?

## Fold-up note

Findings 1, 4, 5, 6, and 8 are **methodology-general** rather than
Cairn-specific: they describe how any lifecycle-based method interacts with
unbidden work. Finding 3 is Cairn-specific measurement. If this note promotes,
1/4/5/6/8 are the fold-back candidates for `dev/.cairn/cairn_foldback.md`.
