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

### 8. The slot system ratchets — tightening is upgrade-durable, loosening is not

Cairn ships **26 slot markers across its core and optional templates** (24
unique names) plus 12 phase-0 intake slots, `as_of` 2026-08-20. Most are
directionally neutral: they are either *descriptive* (`project-overview`,
`team-roster`, `next-start`, the phase-0 maps) or *routing* —
`documentation-tier-home`, `tests-tier-home`, `examples-smoke-home`,
`verification-commands` name where a project's docs, tests, and commands live
without adding or removing an obligation.

**But every slot whose prompt text scripts a direction points the same way:**

* `triage-extra-triggers` — "Fill with your project's extra *'open a proposal
  when…'* bullets."
* `assurance-path-triggers` — "Adopter-specific high-assurance triggers *beyond
  the mandatory list above*."
* `tests-tier-home` — "*unknown or uncertain scope falls back to the full
  suite*."
* `verification-commands` — bounded mode "*refuses*"; "*Uncertainty resolves to
  `full`*."
* `project-conventions` — "the *high-risk surfaces*, and the operational
  pitfalls."

There is no `triage-exemptions`, no just-commit-widening seam, nowhere an
adopter is invited to record *where their project's ceremony is
disproportionate*. Four of these also carry "**An unfilled slot is a review
finding**", so considering what to *add* is compulsory while considering what to
drop is prompted nowhere.

**The teeth are in the upgrade contract, and they are what make this structural
rather than rhetorical.** `bootstrap/UPGRADE.md`: "**Slots are adopter-owned.**
Content between `cairn:slot NAME` and `cairn:end NAME` is yours… the surrounding
doctrine merges, your slot body is preserved verbatim."

So an adopter's *tightening*, written into a slot, survives every upgrade
untouched. Their *loosening* has nowhere to live but the shipped prose around
the slots — precisely the text the merge reconciles from upstream. The one
loosening device Cairn does ship, the escape hatch, sits in unslotted prose
carrying a "*Sync note:* this gloss is a duplicate of `doctrine/proposals.md`'s
escape-hatch paragraph": upstream-owned by construction, so an adopter cannot
safely extend it in place.

**Across successive upgrades, an adopter's apparatus can therefore only ratchet
heavier.** That is gap (17) with a mechanism behind it rather than a
disposition, and it quietly contradicts the adoption promise the guide star
makes — *keep the apparatus only as heavy as your codebase and team earn* —
because "as heavy as you earn" presupposes the ability to reduce, and reduction
is the perishable half.

This is the note's most checkable claim and its cheapest fix: a slot is a
comment marker, and adding one costs no doctrine at all.

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
`docs/solo-legacy-recipe.md`, and/or a **widening slot** letting an adopter
record where ceremony is disproportionate, the way `triage-extra-triggers` lets
them record where it is insufficient (Finding 8). This is the only option that reaches the messy trees the felt gap
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
5. **Is a widening slot the right mechanism for Finding 8**, or does the ratchet
   want fixing in the shipped escape-hatch prose instead — which would make the
   loosening upstream-owned, and therefore uniform across adopters rather than
   per-project?

## Fold-up note

Findings 1, 4, 5, 6, and 8 are **methodology-general** rather than
Cairn-specific: they describe how any lifecycle-based method interacts with
unbidden work. Finding 3 is Cairn-specific measurement. If this note promotes,
1/4/5/6/8 are the fold-back candidates for `dev/.cairn/cairn_foldback.md`.

---

## Review -- Codex (External) -- 2026-08-20

<!-- TEMPORARY REVIEW: the author folds accepted findings inline and deletes
     this section. Strategy notes are inline-revised, not append-only. -->

**Structural independence.** Cross-type read: Claude authored the note; Codex
reviewed it. Reviewed strategy bytes: `9c0a435059aa4e7afe5d4b4878bb2bd8012627b6`.

**Recommendation: REVISE before promotion.** The direction is worth preserving:
stewardship is a second face of Restraint, docs are the right first surface, and
the agent failure mode needs a ceiling rather than encouragement. The draft is
not yet ready to feed doctrine or a proposal because its motivating case crosses
an authority boundary it says is absent, and its proposed evidence source cannot
observe the phenomenon it is meant to count.

### Steelman

The distinction between *work overcharged after entering a lifecycle* and *work
never put on a path* is real and useful. Findings 4-7 are the strongest part of
the note: cost gradients explain behaviour better than exhortation; risk belongs
to the surface rather than the line count; agents invert the human literature's
under-supply problem; and a separate commit protects Cairn's durable record.
The docs-first direction follows cleanly from those premises.

The repository facts mostly reproduce. `dev/PLANNING.md`'s live Queued section
is exactly 693 lines over 22 top-level items (31.5 lines/item), and the migrated
deferred register is 173 lines over six (28.8/item). Anchor 17 and gap (17) say
what the note attributes to them. The triage quote, five named directional slot
prompts, and `bootstrap/UPGRADE.md`'s preserve-the-slot-body contract are real.
The claim checker reports no flags.

### Findings

**[S1] BLOCKING -- the motivating case partly is an authority gap, and a
separate commit does not resolve it.** `doctrine/proposals.md` grants the
just-commit path when deciding whether a standalone change needs a proposal.
The felt case is narrower and different: an agent notices unrelated work while
executing an accepted plan. Both Cairn's and the shipped
`templates/core/AGENTS.md` say that **new scope is a plan deviation and requires
Maintainer approval**. Splitting the incidental fix into its own commit closes
the tangled-history problem; it does not grant authority to perform that work
during the scoped execution.

The draft sees the conflict in Open question 4, but Finding 1 has already ruled
it out (*"the gap is not authority"*), the opening says this is not a request
for more authority, and the header omits the shipped `AGENTS.md` from the
surfaces this could feed. Those cannot all stand. Revise by separating two
contexts:

* outside an active accepted plan, trivial standalone work already has
  permission and the question is attention/cost; and
* during scoped implementation, stewardship needs an explicit rule saying
  whether a fenced incidental fix is authorized side work or remains a stop-
  and-ask deviation.

Do not pre-decide the second answer, but name it as a real design decision and
add `templates/core/AGENTS.md` (plus Cairn's self-hosted copy) to the possible
promotion surface. A proposal-template slot cannot override an always-loaded
operational rule by implication.

**[S2] BLOCKING -- retrospective commits cannot measure work that was noticed
but never recorded.** Recommendation step 1 proposes sampling LHM commits and
counting both *"what should have been fixed and was not"* and over-supplied
tidying. A commit contains only work that happened. It carries no denominator of
nearby defects the agent noticed and declined, and it cannot distinguish
"unnoticed" from "noticed and correctly left alone." The same selection problem
weakens Finding 3: the board can characterize filed work, but the note's subject
is work that never reached the board.

I tested the suggested population rather than reasoning only from the prose.
LHM's six latest non-lifecycle commits show changed files and shipped outcomes;
none records incidental candidates considered and rejected. A reviewer can
invent such candidates after the fact, but that measures the reviewer's taste,
not the agent's stewardship behaviour.

Make the first evidence pass **prospective and discovery-time**, over a bounded
set of ordinary LHM task sessions. Record a candidate when it is noticed, before
its disposition: where it was encountered, whether the assigned task already
touched that surface, the proposed size/surface class, and `fix separately |
defer | leave` with the reason. Then compare estimated and actual scope for the
ones fixed. Confirm the instrument against at least one known-present candidate
so a blank ledger cannot masquerade as absence. This can remain a temporary
measurement artifact; it does not yet require a permanent trailer or doctrine.

**[S3] MEDIUM -- slot preservation supplies persistence, not exemption
authority, so Finding 8 overstates both the ratchet and the cheapness of its
fix.** The dated count is off by one: exact standalone marker lines under
`templates/core/` plus `templates/optional/` produce **25 occurrences and 24
unique names**, not 26 and 24. The 12 phase-0 markers reproduce. The extra
apparent occurrence comes from counting a marker example outside that installed
set, not another customization surface.

More importantly, a new widening slot would survive upgrades, but it would not
say whether its exemptions outrank the mandatory triage list or the plan-scope
rule. Without a precedence contract it creates two disagreeing instructions,
and review should reject the contradiction. Existing slots also permit an
adopter to reduce obligations *within the policy body that slot owns*, so
"across successive upgrades ... only ratchet heavier" is stronger than the
mechanism establishes.

Keep the useful narrower finding: **the prompts and supported override
authority are asymmetric**. Tightening is explicitly invited; a safe loosening
is not. But remove *"adding one costs no doctrine at all."* A marker is cheap;
granting it bounded authority, defining what can never be exempted, and stating
precedence is the design work.

**[S4] MEDIUM -- the recommendation says "write the plank last" and then writes
it before the operational pilot.** Its sequence is evidence pass -> O2 guide-
star plank -> O4 docs-first behaviour. That ordering also conflicts with
Finding 4's conclusion that exhortation cannot move the gradient and Finding
5's conclusion that the fence is the entire design. Prefer: prospective
evidence -> settle authority, ceiling, stop rule and refusal surfaces -> bounded
docs-first pilot -> only then fold the demonstrated lesson into the guide star.
The plank can still reuse Anchor 17; it simply comes after the thing that gives
it content.

### Disposition and limits

Preserve Findings 2, 4-7 and the O2-not-O3 judgment. Revise Finding 1 and the
opening around the two authority contexts; replace the retrospective commit
sample with a prospective observation window; narrow Finding 8 to prompt and
override asymmetry; and make the recommendation's order literal.

I did not verify the candidate Anchor 18 literature. The draft marks it
unverified and does not rely on it for the current recommendation, so that is a
promotion precondition rather than a finding in this round. I did not audit
LHM for latent defects or judge which of its changes should have been omitted;
doing either retrospectively would reproduce S2's measurement error.

---

## Review -- Antigravity (External Strategy) -- 2026-08-20

<!-- TEMPORARY REVIEW: the author folds accepted findings inline and deletes
     this section. Strategy notes are inline-revised, not append-only. -->

**Structural independence.** Cross-type read: Claude authored; Codex and Antigravity (Gemini 3.7 Flash) reviewed.

**Recommendation: REVISE before promotion.** Concur with Codex's S1–S4 findings. In addition, the draft should incorporate three constraints derived from agent execution behavior and scientific codebases:

### Core Perspectives & Additional Findings

**[S5] Agent-attentional drift vs. pure diff over-supply.** Finding 5 correctly identifies agent over-supply as the inverse of human under-supply, but frames it only as a git/diff problem (large diffs, zero compute cost). In practice, an unconstrained stewardship license causes **cognitive context disruption**: an agent encountering an incidental flaw mid-task gets derailed into fixing it, burning tool turns and working-memory context needed for its primary objective. Stewardship must protect the **agent's focus during complex tasks**, not only the commit log.

**[S6] The domain-opacity trap in scientific legacy trees.** The draft targets adopter trees (decades-old scientific codebases). In scientific code, what appears to an LLM as "sub-optimal style", "dead parameters", or "redundant casting" is frequently a load-bearing numerical stability workaround, memory layout optimization, or unit-handling convention. "Obviously harmless" is domain-opaque; stewardship rules in adopter code must enforce **semantic humility** and forbid speculative refactoring of numerical/kernel logic.

**[S7] Doc stewardship must be mechanically verifiable.** Finding 7 identifies documentation as the ideal first surface. While broken links and literal typos are safe, **speculative semantic re-phrasing of docs is hazardous**: agents consume documentation as ground truth for architectural reasoning. A plausible but subtly incorrect doc rewrite actively misleads subsequent agent sessions. Doc stewardship must be strictly bounded to provable mechanical defects (broken links, literal typos, statically verified identifier renames).

**[S8] Mechanizable fences and the "Third Way" (Session Scratchpad).** 
* **The Fence**: To prevent models rationalizing past subjective guidelines ("obviously minor"), the fence requires objective rules:
  1. *Proximity constraint*: Only files already in the primary task's working set.
  2. *Refusal list*: No contracts, schemas, security/ceremony paths, public APIs, or numerical kernels.
  3. *Size ceiling*: $\le 3$ lines per file.
  4. *Timing (Bookend rule)*: Fixes occur strictly before starting or after completing the primary task, never mid-flight.
* **The Ephemeral Scratchpad**: Finding 4 presents a false dichotomy between heavy roadmap filing and immediate fixing. An agent noticing an incidental defect can log a 1-line note in an ephemeral session scratchpad or handoff note (`dev/reflections/`) for rapid batch triage by the Maintainer, avoiding both roadmap overhead and context derailment.

