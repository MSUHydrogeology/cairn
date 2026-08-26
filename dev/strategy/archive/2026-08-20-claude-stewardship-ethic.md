# Stewardship — the work that never enters a lifecycle

**Author**: Claude (Strategy)
**Model**: Opus 5
**Date**: 2026-08-20
**Status**: revised (External round 1 — Codex and Antigravity, both different
agent types — folded in and removed 2026-08-20; the arc is in `git log`, not
this body)
**Type**: design-exploration
**Surfaces this would feed**: the guide star
(`2026-05-14-claude-human-ai-team-development-framework.md`) as a plank;
`doctrine/proposals.md` > Triage; **`templates/core/AGENTS.md` and Cairn's own
`AGENTS.md`** (the plan-deviation rule — see Finding 1);
`docs/solo-legacy-recipe.md`; the slot set in
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

**One thing this note initially got wrong about its own subject.** An early
draft claimed stewardship asks for no new authority. For standalone work that is
true; for work noticed *during a scoped implementation* it is false, and the
distinction turns out to be the load-bearing one (Finding 1).

## Method

Read: the guide star; `doctrine/proposals.md` > Triage; `AGENTS.md` and
`templates/core/AGENTS.md` on scope deviation and verification boundaries;
`dev/strategy/README.md`; `docs/solo-legacy-recipe.md`; the shipped slot set in
`templates/core/dev/proposals/_template.md` and `bootstrap/UPGRADE.md`'s merge
contract. Measured the composition of `dev/PLANNING.md`. Searched `doctrine/`,
`dev/`, and `templates/` for prior deliberation on incidental fixes.

**Two instrument failures, recorded because the note is partly about
them.** Both were caught in review, not in authoring:

* A search for stewardship vocabulary (`boy.?scout`, `broken window`, `litter`,
  `opportunistic refactor`) returned only false positives — `litter` matching
  inside `splitter` — and the absence read as "greenfield." It is not: the
  concept is already in the guide star under other words (Finding 2). **A
  vocabulary grep tests the vocabulary, not the idea.**
* A count of shipped slot markers returned 26. The true figure for the
  *installed* set is **25 markers over 24 unique names**; the extra came from a
  marker sitting inside a fenced code block in `templates/README.md`, which is
  documentation *about* the slot syntax and is not installed anywhere
  (`scaffold.py --manifest` does not list it). **A marker count that cannot
  distinguish a live marker from an example of one is not a count of
  customization surfaces.**

Both are the same failure at different depths, and both are instances of
`AGENTS.md` > *Confirm the instrument before trusting an absence* — the second
one committed *after* that caution was written into this note's own Method
section. The lesson that survives: run the measurement against a case known to
be present, and against a case known to be excluded.

**What would falsify this note's direction:** a prospective observation window
(Finding 3) showing either that the fix-in-passing class is rare at discovery
time, or that its members stop being small once examined.

## Findings

### 1. Two authority contexts, and only one of them already has permission

`doctrine/proposals.md` > Triage already closes with: "Everything else — a new
helper, a test, a typo fix, a docstring polish, a self-contained refactor — just
commit." The escape hatch widens it further for anything urgent, reversible, or
experimental.

**Outside an active accepted plan, that settles it.** A trivial standalone
change has permission; whatever suppresses the behaviour is attention and cost,
not authority (Findings 3–5). A doctrine that re-grants the permission more
warmly changes nothing.

**Inside a scoped implementation, it is the opposite.** Both Cairn's `AGENTS.md`
and the shipped `templates/core/AGENTS.md` hold that **new scope is a plan
deviation requiring the Maintainer's approval** — and the felt case is precisely
an agent noticing unrelated work while executing an accepted plan. A separate
commit (Finding 6) fixes the tangled-history problem; it grants no authority to
do the work at all. So in this context stewardship *is* an authority question,
and the two rules point opposite ways.

**This note does not pre-decide which way that resolves.** It names it as the
central design decision: is a fenced incidental fix *authorized side work*
during scoped implementation, or does it remain a stop-and-ask deviation? Either
answer is defensible; leaving it implicit is not, because the deviation rule is
always loaded and would win by default. And it must be settled **where that rule
lives** — a proposal-template slot cannot override an always-loaded operational
rule by implication, which is why `templates/core/AGENTS.md` now appears among
the surfaces this could feed.

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

Same design center, different failure surface.

### 3. Neither the board nor any commit history can observe this

The Queued section of `dev/PLANNING.md` runs 693 lines over 22 items — **~31.5
lines per item**; the migrated deferred register, 173 lines over six (~28.8).
These are tagged, dated, multi-part entries. Nearly none is something an agent
could have fixed in passing. So on Cairn a stewardship norm would remove a
handful of rows from a 2,375-line board: **Cairn cannot be its own evidence
base.**

**But the same selection problem defeats the obvious substitute.** A commit
history contains only work that *happened*. It carries no denominator of nearby
defects an agent noticed and declined, and it cannot separate "never noticed"
from "noticed and correctly left alone." Reconstructing candidates from a diff
after the fact measures the reconstructor's taste, not the agent's behaviour.
The board characterizes *filed* work; this note's subject is work that never
reached the board — and a commit log is the same instrument with the same blind
spot.

**The measurement therefore has to be prospective and taken at discovery time**,
not retrospective. Design in the Recommendation.

### 4. Filing dominates fixing — but the dichotomy is false

Filing a roadmap row costs one line, is always defensible, and can never be
shown wrong. Fixing costs a commit, Boundary A verification, the standing gates
for every touched surface, and sometimes a re-anchor. Under any uncertainty,
filing strictly dominates. **Exhortation cannot move a gradient** — a doctrine
has to change a cost, not a sentiment. And **"minor" is a property of the
surface, not of the change**: a one-line docstring fix inside
`bootstrap/_scaffold/` summons the Bandit gate and the AST attestation baseline.

**There is a third option the framing above hides.** Between heavy roadmap
filing and immediate fixing sits a one-line note in an ephemeral session
surface — a scratchpad or handoff note — batched for the Maintainer's rapid
triage. That costs neither board weight nor the context switch of fixing, and it
is probably the correct disposition for most candidates. One caution: the
routine surface may be ephemeral, but the **observation ledger of Finding 3 must
be durable**, or the evidence pass measures nothing. `dev/reflections/` is
gitignored and pruned, so it can host the former and not the latter.

### 5. Agents over-supply two things, not one

Every source in *Literature* assumes tidying is **under-supplied**, because for
humans it is: it costs attention, earns no credit, and someone else might do it.
That is the bystander-and-commons structure, and the Boy Scout Rule is a remedy
for it.

**Agents have none of those brakes**, and the over-supply shows up in two
places:

* **In the diff.** Near-zero marginal cost to touch a file, no felt cost for the
  reviewer's time, no embarrassment at a forty-file cleanup.
* **In attention.** An agent that stops mid-task to fix an incidental flaw burns
  tool turns and working context that the primary objective needed. This is the
  more insidious half, because it damages the assigned work rather than the
  commit log, and nothing in the repository records that it happened.

**The human problem is under-supply; the agent problem is over-supply of both
kinds.** A doctrine written from the human literature aims at the wrong one.
What agents need is a **licence with a fence** — a ceiling, a stop rule, a
refusal list, and a rule about *when* in a task a fix may happen — not
encouragement. The exhortation half is nearly free to write; the fence is the
entire design.

### 6. The record-legibility constraint

The tangled-change literature finds that bundling unrelated changes into one
commit degrades both review quality and any later reconstruction of what the
commit did. **Cairn's product is the legibility of its record.** So: **a
stewardship fix never shares a commit with anything else** — already compatible
with one-commit-per-transition and path-scoped commits, so it costs no new
mechanism.

This is necessary and not sufficient. It answers *how the fix is recorded*, not
*whether it was permitted* (Finding 1) or *whether it was correct* (Finding 7).

### 7. "Obviously harmless" is domain-opaque in scientific code

This is the finding that most changes the shape of an adopter-facing rule, and
it comes from the target population rather than from the general literature.

In a decades-old scientific codebase, what reads to a model as sub-optimal
style, a dead parameter, a redundant cast, or a pointless intermediate is
frequently **load-bearing**: a numerical-stability workaround, a memory-layout
choice, an operation-order constraint that preserves conditioning, a
unit-handling convention. The code carries no comment saying so, because the
person who wrote it knew. That is exactly the tree this note targets.

The general literature already says some refactoring categories measurably
induce bugs, and that low-ownership contributors correlate with more defects —
which is close to the definition of an agent passing through. Scientific code
sharpens both: the defect is silent, it corrupts results rather than crashing,
and no test necessarily fails.

**So any stewardship rule for adopter code must enforce semantic humility**, and
must place numerical and kernel logic on the refusal list outright. "Obviously
harmless" cannot be an agent's judgment call in a domain it does not model.

### 8. Docs are the right first surface — bounded to mechanically provable defects

The Maintainer named docs specifically, and the case is strongest there:

* **Decay is silent.** No test fails when a doc goes stale, so the normal
  detector is simply absent.
* **The verification cost is lowest.** Prose work runs its claim, link, snippet
  and neutrality gates rather than the suite, so the Finding 4 gradient is at
  its shallowest.
* **The tangling risk is smallest.** A doc fix rarely needs to ride inside a
  code commit, so Finding 6 costs almost nothing to honour.

**But docs carry their own version of Finding 7, and it is worse than it
looks.** Agents consume documentation as ground truth for architectural
reasoning. A plausible-but-subtly-wrong doc rewrite does not merely sit there
being wrong — it actively misleads every subsequent agent session, and it is far
harder to detect than a broken link because it reads well.

So doc stewardship is safe only where the defect is **mechanically provable**:
broken links, literal typos, statically verified identifier renames, paths that
no longer resolve. **Speculative semantic re-phrasing is out of scope**, however
much better the rewrite reads. `docs/DOCUMENTATION_PLAN.md` already answers
*where a doc belongs*; what no document answers is **who fixes one when it
rots** — and now, *which rot is safe to touch.*

### 9. The slot asymmetry — prompts and override authority, not a universal ratchet

Cairn ships **25 slot markers over 24 unique names** across its installed core
and optional templates, plus 12 phase-0 intake slots (`as_of` 2026-08-20; see
*Method* for the correction). Most are directionally neutral: *descriptive*
(`project-overview`, `team-roster`, the phase-0 maps) or *routing*
(`documentation-tier-home`, `tests-tier-home`, `examples-smoke-home`,
`verification-commands`).

**Every slot whose placeholder scripts a direction scripts the same one:**
`triage-extra-triggers` ("your project's extra *'open a proposal when…'*
bullets"), `assurance-path-triggers` ("*beyond the mandatory list above*"),
`tests-tier-home` ("*unknown or uncertain scope falls back to the full suite*"),
`verification-commands` ("*Uncertainty resolves to `full`*"),
`project-conventions` ("the *high-risk surfaces*"). Four also carry "**An
unfilled slot is a review finding**", so considering what to add is compulsory
while a safe loosening is prompted nowhere.

**The narrower claim is the true one.** `bootstrap/UPGRADE.md` makes slot bodies
adopter-owned and preserved verbatim while the surrounding doctrine merges from
upstream — so persistence favours whatever an adopter writes in a slot, in
*either* direction. `coordination-additions` is a live counter-example: its
placeholder says "a sequential team runs only the baseline above," which is a
reduction. **"The apparatus can only ratchet heavier" overstates the
mechanism.** What is genuinely asymmetric is the **prompting** and the
**supported override authority**: tightening is invited and has somewhere to go;
a loosening has neither an invitation nor any statement of what it may outrank.

**And the fix is not free.** A marker is cheap. Granting it *bounded authority*,
defining what can never be exempted, and stating **precedence** against the
mandatory triage list and the plan-scope rule of Finding 1 is the actual design
work — and without a precedence contract a widening slot merely creates two
disagreeing instructions, which review should reject.

## Literature — a candidate Anchor 18

**Status: unverified.** Recalled, not checked. The guide star's anchors carry
full citations with resolvable identifiers; **verification is a precondition of
promotion**, per `AGENTS.md` > Verifying claims. This block exists so the
*shape* of the anchor is visible, not so it can be cited. Nothing in the
Recommendation depends on it.

* **The norm.** Martin, *Clean Code* (2008), and his essay in *97 Things Every
  Programmer Should Know* (2010) — the Boy Scout Rule. Hunt & Thomas, *The
  Pragmatic Programmer* (1999) — "don't live with broken windows." Fowler,
  "Opportunistic Refactoring" (bliki, c. 2011), the most operationally useful of
  the three because it is a *scoping rule* rather than an exhortation.
* **Decay as an empirical claim.** Lehman's laws of software evolution; Eick et
  al., "Does Code Decay?" (IEEE TSE, 2001); Cunningham's technical-debt metaphor
  (OOPSLA 1992).
* **Norm salience — the better half of the litter analogy.** Cialdini, Reno &
  Kallgren (1990) ran the actual littering field experiments and found a
  *single* piece of litter in an otherwise clean environment suppressed
  littering more than a pristine one, because it made the norm salient. The
  mechanism is **visibility of the norm, not absence of disorder.**
* **The counter-evidence (Findings 6–7).** Herzig & Zeller, "The Impact of
  Tangled Code Changes" (MSR 2013); Kirinuki et al., on committing tangled
  changes (ICPC 2014); Bavota et al., "When Does a Refactoring Induce Bugs?"
  (SCAM 2012); Bird et al., "Don't Touch My Code!" (FSE 2011).
* **The contested one.** Wilson & Kelling (1982) is the origin of the
  broken-windows metaphor, and the criminological theory is seriously disputed
  — Harcourt & Ludwig (2006) is the standard rebuttal. **Cite it as the
  metaphor's lineage, never as evidence.**

## Options

**O1 — Do nothing.** Gap (17) stays open and the standalone just-commit
permission stands. Defensible while the evidence is observational. Cost: the
thing the Maintainer keeps noticing keeps happening, unmeasured — and the
in-plan authority question (Finding 1) stays unresolved, which means the
deviation rule silently decides it.

**O2 — Fold into the existing Restraint plank**, as a subsection under "The
default is currently backwards", reusing Anchor 17. The cheapest guide-star
move; no new anchor. Risk: Restraint argues for doing *less* and stewardship for
doing *more, unbidden*, so filed there it reads as a corollary when it is partly
a tension — and the guide star's own discipline is that mismatches are the
interesting part.

**O3 — A new plank plus Anchor 18**, within Restraint or as a third design
center. Honest about the tension; the anchor index is append-only to allow it.
Cost: a design center is a large claim resting on unrecorded observation.

**O4 — Settle the operating rule where it binds.** The Finding 1 decision in
`AGENTS.md` / `templates/core/AGENTS.md`; the fence (ceiling, refusal list,
timing, proximity) alongside it; docs-first scope per Finding 8. This is the
only option that changes behaviour — O2 and O3 only set direction, and per
Finding 4 direction does not move a gradient.

**O5 — The slot work of Finding 9**, which now requires a precedence contract
rather than a marker. Depends on O4: a slot cannot state precedence against a
rule that has not been decided.

## Recommendation

**Evidence, then the operating rule, then a bounded pilot, then the plank.** The
earlier ordering put the guide-star plank before the pilot, which contradicted
Findings 4 and 5 — the plank is the exhortation half, and it should not precede
the fence that gives it content.

1. **A prospective, discovery-time observation window** over a bounded set of
   ordinary LHM task sessions — the legacy-rooted retrofit already named as a
   case study, not Cairn (Finding 3). Record each candidate **when noticed,
   before its disposition**: where it was encountered, whether the assigned task
   already touched that surface, the estimated size and surface class, and
   `fix separately | defer | leave` with the reason. For those fixed, compare
   estimated against actual scope. **Confirm the instrument against at least one
   known-present candidate**, so a blank ledger cannot masquerade as absence.
   This stays a temporary measurement artifact — it needs no commit trailer and
   no doctrine, and its ledger must be durable even where the routine scratchpad
   of Finding 4 is not.
2. **Settle the operating rule**: the Finding 1 authority question first, then
   the fence — ceiling, refusal surfaces (contract, high-risk, trust-ceremony,
   and per Finding 7 numerical/kernel logic), proximity to the task's existing
   working set, and timing within a task. This is the decision the rest depends
   on, and it belongs in `AGENTS.md`, not a template slot.
3. **A bounded docs-first pilot** (Finding 8), restricted to mechanically
   provable defects — the narrowest surface, the shallowest cost gradient, and
   the one where a wrong "fix" is detectable.
4. **Then O2**, with the tension stated rather than smoothed. On current
   evidence stewardship is a **second face of gap (17)**, not a third design
   center; it earns its own anchor when there is a measurement behind it.
   Writing it up as a design center now would be the recursive-bloat failure the
   guide star names in the very section the plank would sit next to.
5. **O5 last**, once precedence has something to point at.

**Residual risk, stated plainly.** This may be over-thinking a norm that could
be one sentence. That is live, and it is why the first move is a measurement
rather than a rule. The counter-argument is Findings 5 and 7: the one-sentence
version is the version that produces forty-file cleanups and silently breaks a
numerical workaround, because the half that gets remembered is the exhortation
and not the fence.

## Open questions

1. **How is the in-plan authority question resolved?** (Finding 1.) Authorized
   fenced side work, or stop-and-ask? This gates everything downstream and
   cannot be settled by implication.
2. **What is the fence made of?** Candidate rules, offered as a starting point
   and not settled: *proximity* — only files already in the primary task's
   working set; *refusal list* — contracts, schemas, security and ceremony
   paths, public APIs, numerical kernels; *size ceiling* — a small fixed number
   of lines per file; *timing* — a bookend rule, fixes strictly before starting
   or after completing the primary task, never mid-flight, which is the direct
   answer to Finding 5's attentional half. Each needs to be objective enough
   that a model cannot rationalize past it, which rules out "obviously minor."
3. **Does the licence eventually need a marker?** A commit trailer would make
   the class countable — the Cialdini reading of norm salience. Deferred: new
   mechanism for an unmeasured problem is what Restraint warns about, and step 1
   does not need it.
4. **What is the precedence contract for a widening slot?** (Finding 9.) What it
   may outrank, what it may never exempt, and how it composes with the
   mandatory triage list and the plan-scope rule.
5. **Does the scratchpad disposition of Finding 4 need any structure at all**,
   or is a free-form handoff line enough for the Maintainer to triage?

## Fold-up note

Findings 1, 4, 5, 6, and 9 are **methodology-general**: they describe how any
lifecycle-based method interacts with unbidden work. Finding 7 is general to
*scientific* adopters specifically, which is Cairn's stated audience. Finding 3
is Cairn-specific measurement plus a general measurement caution. If this note
promotes, 1/4/5/6/7/9 are the fold-back candidates for
`dev/.cairn/cairn_foldback.md`.

## Closure — integrated into the refocus — 2026-08-26

This note's questions were settled by the 2026-08 refocus
(`2026-08-21-claude-nimbleness-recovery`, accepted through the
subtraction-sweep Decision), five days after it was written. The map:

* **Finding 1 (the authority question) — answered.** The accepted
  counterforce carries the **stewardship warrant**: standing trivial-lane
  authority to fix an incidental defect, fenced objectively — a failing-test
  reproduction, agent code review, zero Maintainer involvement, a provenance
  line. The refocus note says so in terms: it *"supplies the authority the
  stewardship-ethic note (2026-08-20) found missing."* The residual-rights
  rule supplies the consequence test this note asked for: the author decides
  only when every plausible consequence of shipping is readily reversible;
  any hard-to-undo answer latches upward; **science always routes to the
  Maintainer** — which is Finding 7's protection for numerical and kernel
  logic, stated as a routing rule rather than a refusal list.
* **Finding 4 (filing dominates fixing) — answered by the attention books.**
  A stewardship fix *repays* attention ("the adopter issue never filed"),
  and the filing channel became a lightweight Cairn issue rather than a
  board row, so the gradient this finding measured has been re-priced on
  both sides.
* **Findings 5 and 6 (the fence and the record)** — carried by the warrant's
  objective conditions and the standing path-scoped, separate-commit
  discipline.
* **Finding 3 (the observation window) — superseded, deliberately.** The
  refocus settled the design by bounding the warrant objectively instead of
  measuring the candidate class first. The measurement-first ordering this
  note recommended was overtaken, not refuted; if the warrant misbehaves in
  practice, the discovery-time ledger design above is the instrument to
  revive.
* **Findings 8–9 (docs-first pilot; slot precedence) — overtaken.** The
  subtraction sweep rewrites the templates and constitution wholesale; slot
  precedence against a retired rule set is moot. An explicit
  numerical-kernel refusal list in the installed contract remains available
  if adopter experience asks for more than the science-routing rule.

What this note contributed that survives: the two-context authority
distinction, the fence-not-exhortation principle, semantic humility about
scientific code, and two instrument-failure lessons already folded into
`AGENTS.md`'s confirm-the-instrument discipline. Archived as integrated.
