# The slot system ratchets: give adopter triage-lightening a durable home

**Author**: Claude (Strategy)
**Model**: Opus 5
**Date opened**: 2026-08-20
**Status**: superseded
**Assurance path**: standard — see "Assurance-path reasoning" below; this is a
template-body change flowing through the designed, tested slot-merge path and
touches none of the four install-contract artifacts and no high-risk surface
**Touches**: `templates/core/dev/proposals/_template.md`,
`dev/proposals/_template.md`, `bootstrap/tests/test_lifecycle_contract.py`,
`docs/solo-legacy-recipe.md`, `CHANGELOG.md`
**Related**: `dev/strategy/2026-08-20-claude-stewardship-ethic.md` (Finding 8,
from which this is severed); the guide star's "Restraint as design center" >
"The default is currently backwards" and its open gap (17)
**Plan review**: not required (trivial implementation — one surface, one
commit, no follow-ups; see "Triage and implementation shape")

## Context

Cairn ships **26 `cairn:slot` markers across its core and optional templates**
(24 unique names), plus 12 phase-0 intake slots (`as_of` 2026-08-20, counted
with `grep -rc 'cairn:slot' templates/`). Most are directionally neutral —
*descriptive* (`project-overview`, `team-roster`, the phase-0 maps) or *routing*
(`documentation-tier-home`, `tests-tier-home`, `examples-smoke-home`,
`verification-commands`), naming where a project's docs, tests, and commands
live without adding or removing an obligation.

**Every slot whose placeholder scripts a direction scripts the same one.** In
their own words:

* `triage-extra-triggers` — "Fill with your project's extra *'open a proposal
  when…'* bullets."
* `assurance-path-triggers` — "high-assurance triggers *beyond the mandatory
  list above*."
* `tests-tier-home` — "*unknown or uncertain scope falls back to the full
  suite*."
* `verification-commands` — bounded mode "*refuses*"; "*Uncertainty resolves to
  `full`*."
* `project-conventions` — "the *high-risk surfaces*, and the operational
  pitfalls."

There is no counterpart: no place an adopter is invited to record which
recurring change classes their project has decided are *not* proposal-worthy.
Four of the directional slots additionally carry "**An unfilled slot is a review
finding**", so considering what to *add* is compulsory while considering what to
resolve downward is prompted nowhere in the shipped tree.

**The defect is in the upgrade contract, not the affordance.**
`bootstrap/UPGRADE.md` > "How the merge protects your customizations":

> **Slots are adopter-owned.** Content between `cairn:slot NAME` and
> `cairn:end NAME` is yours. […] the surrounding doctrine merges, your slot
> body is preserved verbatim.

So an adopter's **tightening**, written into a slot, survives every upgrade
untouched. Their **loosening** has nowhere to live but the shipped prose around
the slots — precisely the text the merge reconciles from upstream. The one
loosening device Cairn ships, the escape hatch in
`templates/core/dev/proposals/_template.md`, sits in unslotted prose carrying a
*"Sync note: this gloss is a duplicate of `doctrine/proposals.md`'s escape-hatch
paragraph; if that doctrine text is ever revised, re-sync this copy"* — it is
upstream-owned by construction, so an adopter cannot safely extend it in place.

**Across successive upgrades an adopter's apparatus can therefore only ratchet
heavier.** That is the guide star's gap (17) with a mechanism behind it rather
than a disposition, and it contradicts the adoption promise the same document
makes — *keep the apparatus only as heavy as your codebase and team earn* —
because "as heavy as you earn" presupposes the ability to reduce, and reduction
is the perishable half.

The felt pain that produced this is the Maintainer's, recorded in the guide star:
twice in one day having to ask "why not just do it?" — once about a two-character
fix. The observation generalizes past Cairn, which is why it is worth fixing in
the shipped templates rather than in Cairn's own tree alone.

## Proposal

Add **one slot**, `triage-just-commit`, to
`templates/core/dev/proposals/_template.md`, immediately after the existing
`triage-extra-triggers` block in the "Triage: trivial vs. non-trivial" section,
so the two sit visibly paired. Its placeholder:

```
<!-- cairn:slot triage-just-commit -->
(Adopter-specific triage resolutions in the just-commit direction — the
recurring change classes this project has already decided are *not*
proposal-worthy, recorded once instead of re-derived (or defaulted heavy)
every time they come up. Typical entries: regenerated API docs, a new test
fixture nothing reads yet, a dev-only version pin, a doc typo or link fix.

**This slot resolves ambiguity; it does not override.** It cannot exempt
anything the general list above names, any high-assurance trigger, or any
surface the project's `AGENTS.md` names high-risk — those are floors. Each
entry names a *class* and why it is not proposal-worthy, never a blanket
path or directory.

Fill with your project's bullets, or replace with `N/A: no recorded
just-commit classes`.)
<!-- cairn:end triage-just-commit -->
```

Then, following the established shipped-vs-self-hosted pattern (the two
`_template.md` copies are deliberately not byte-identical twins — the shipped
copy carries placeholders, Cairn's copy carries the filled instance):

1. **Fill it in `dev/proposals/_template.md`** with Cairn's own classes. A
   starting set, offered for the Maintainer to set rather than settled here,
   since its content *is* a triage decision and therefore theirs:
   * A typo, wording, or broken-link fix in `docs/` or `dev/` prose that changes
     no claim, no path, and no procedure.
   * A test that pins already-shipped behaviour without changing it.
   * A fixture added under `bootstrap/tests/fixtures/` that no test reads yet.
   * Roadmap-board, changelog, and handoff edits made at their defined
     serialization points.
2. **A contract test** in `bootstrap/tests/test_lifecycle_contract.py`, beside
   the existing `test_the_shipped_proposal_template_carries_an_unfilled_trigger_slot`,
   asserting both slots are present and paired in both copies and that Cairn's
   own body is filled rather than placeholder.
3. **A symmetric paragraph in `docs/solo-legacy-recipe.md`**, next to its
   existing "Add the science trigger to your own triage rules" section, teaching
   the downward fill the way that section teaches the upward one.
4. **A `CHANGELOG.md` entry.**

**One deliberate asymmetry.** The new slot does *not* carry "An unfilled slot is
a review finding." Its siblings `triage-extra-triggers` and
`assurance-path-triggers` do, because failing to consider a project's protected
surfaces is a real omission. Failing to record a lightening class is not — a
project with none is in a fine state. The `N/A:` form is offered instead, which
is exactly the precedent `examples-smoke-home` already sets. A reviewer will
notice the asymmetry; it is intended, and this is the argument for it.

### Documentation / doctrine surface

* `docs/solo-legacy-recipe.md` — descriptive layer; gains the symmetric
  teaching paragraph.
* `CHANGELOG.md` — one entry.
* **`doctrine/proposals.md` — no change, and this is load-bearing.** Doctrine
  documents none of the existing 26 slots; each carries its own semantics in its
  placeholder text (verified: `grep -n -i 'slot' doctrine/proposals.md` returns
  one unrelated hit, about the `Plan review` metadata line). Adding a slot
  therefore extends an existing, doctrine-silent mechanism rather than changing
  a rule anyone follows.

### Doctrine-change rate-limit (if this proposal changes doctrine)

**Not applicable — this proposal changes no doctrine.** Per the surface analysis
above, it adds a placeholder to a template whose slot mechanism doctrine does not
describe. It therefore does not enter the doctrine-evolution gate
(`doctrine/rationale.md` > "How the doctrine evolves under evidence"), and no
single-incident justification is owed.

If a reviewer concludes otherwise — that a shipped placeholder telling adopters
they *may* record just-commit classes is itself doctrine — then the gate applies
and this proposal is under-argued on evidence, since its grounding is one
maintainer's repeated observation plus a structural reading of the upgrade
contract. That is a fair finding and the right place to raise it.

### Triage and implementation shape

**Proposal-worthy**: yes — it changes a shipped adopter-facing template, which
is a contract-adjacent surface, and the triage list's "implementation tradeoffs
you want a second opinion on" applies squarely.

**Implementation: trivial** — one surface (the proposal-template pair and its
two satellites), one commit, no deferred follow-ups. Under
`doctrine/proposals.md` that means implement and archive together, with no plan.

Stating this plainly because the alternative is the pathology this proposal is
about: a one-slot change routed through a full plan cycle would be gap (17)
demonstrating itself. If a reviewer thinks the blast radius earns a plan, that
is a legitimate call — but it should rest on the blast radius, which the
**assurance path** field exists to carry, not on the change's contract-adjacency
alone.

### Assurance-path reasoning

`standard`. The field admits no default and uncertainty resolves to
high-assurance, so the reasoning is recorded rather than assumed:

* **Not the install contract.** `AGENTS.md` names four artifacts — the fidelity
  manifest, the gate manifest, the lockfile schema, and the published
  `scaffold.py --manifest`. A template *body* is none of them. Verified: the
  published manifest is a `destination<TAB>source<TAB>mode` table and does not
  enumerate slot names, so adding a slot changes neither its rows nor its schema.
* **Not a high-risk surface.** It touches no engine code, no neutrality surface,
  no license boundary, no interpreter binding, no sweep trust root.
* **The upgrade path is designed and tested for exactly this.**
  `bootstrap/UPGRADE.md`: "A slot **added** upstream arrives with its placeholder
  for you to fill." `bootstrap/tests/test_upgrade.py` covers the slot parser and
  the added/removed-slot cases.

## Rationale

**Why a slot rather than better prose.** The gap is not that Cairn says too
little about lightening; it is that whatever an adopter concludes about *their*
project has no upgrade-durable home. Only a slot is preserved verbatim through
the merge. Any amount of improved shipped prose remains upstream-owned and
merges over.

**Why it is safe to let adopters write here.** The slot resolves ambiguity
inside Cairn's floor; it does not lower the floor. The universal triage list, the
high-assurance triggers, and the project's own high-risk surfaces all still bind,
and the placeholder says so. The realistic entries are answers to genuinely
open questions — *is a new fixture a new abstraction? is a dev-only pin a config
contract change?* — which today have no recorded answer, so each agent re-derives
one, and under uncertainty re-derives it heavy.

**Why the ratchet matters more than any single over-charged change.** A default
that routes heavy costs one decision at a time and can be corrected by the
maintainer in the moment — which is what has been happening. A ratchet
accumulates: every correction the maintainer makes is written somewhere
perishable, so the same correction is owed again after the next upgrade. That is
the difference between a disposition and a mechanism, and it is why this is
worth a change rather than a habit.

## Alternatives considered

**A1 — Do nothing.** Defensible: the escape hatch exists, and a maintainer can
always say "just do it." Rejected because that is precisely the state the guide
star already records as a gap, and because the correction is perishable.

**A2 — Widen the shipped escape-hatch prose instead.** The escape hatch answers
*"is this one change urgent, reversible, or experimental?"* The defect concerns
*recurring classes in a specific project* — an answer upstream cannot write,
because it depends on what the project guards. Widening the shipped hatch would
also lower Cairn's floor for every adopter at once, which *would* be a doctrine
change subject to the rate-limit gate, and it still leaves the adopter without a
durable home. Rejected for this proposal; it remains a separate question worth
asking on its own evidence.

**A3 — A slot in `AGENTS.md` instead of the proposal template.** Triage lives in
the proposal template; putting its counterpart elsewhere splits one decision
across two files. Rejected.

**A4 — Both a slot and a doctrine paragraph.** Rejected on restraint: the slot
alone fixes the named defect, and a doctrine paragraph would pull a template
change into the doctrine-evolution gate for no additional effect.

## Evidence / verification plan

Every claim in this proposal is checkable against files in the tree today; none
depends on external literature or on the stewardship note's contested half.

| Claim | How it was established |
|---|---|
| 26 slot markers, 24 unique names, +12 phase-0 | `grep -rc 'cairn:slot' templates/` and `grep -rho 'cairn:slot [a-z-]*' \| sort -u` |
| Every directional slot points one way | Read all five placeholders in context; quoted verbatim above |
| Slot bodies are upgrade-durable, surrounding prose is not | `bootstrap/UPGRADE.md` > "How the merge protects your customizations" |
| The escape hatch is upstream-owned | Its own `Sync note` in `templates/core/dev/proposals/_template.md` |
| Doctrine documents no slot | `grep -n -i 'slot' doctrine/proposals.md` — one unrelated hit |
| The published manifest does not name slots | `python bootstrap/scaffold.py --manifest` |
| Shipped and self-hosted templates are deliberate non-twins | `bootstrap/tests/test_lifecycle_contract.py::test_the_shipped_proposal_template_carries_an_unfilled_trigger_slot` |

### Author-accounting — invariants, failure modes, edge cases

* **Invariant: slot-name uniqueness.** `bootstrap/_scaffold/install.py` warns on
  unpaired markers and `BOOTSTRAP.md` records the uniqueness invariant.
  `triage-just-commit` is a new name repo-wide (`grep -r 'triage-just-commit'`
  returns nothing before this change).
* **Failure mode: an adopter writes a blanket exemption** — "anything under
  `src/`" — and hollows out their own apparatus. Bounded, not eliminated: the
  universal list and high-assurance triggers still bind, so the blast radius is
  the ambiguous middle, not the floor. The placeholder names the failure
  explicitly ("a *class* … never a blanket path or directory"). Residual risk
  accepted; the alternative is that the ambiguous middle keeps defaulting heavy
  forever.
* **Failure mode: the slot is universally `N/A`.** Then the ambiguity it targets
  is not real and the change is dead weight — a shipped placeholder nobody
  fills. This is the honest downside case and is listed under *Signals* below.
* **Edge case: existing adopters mid-upgrade.** They receive the new slot with
  its placeholder; their existing slot bodies are untouched. Designed and tested.
* **Edge case: an adopter who forked their `_template.md`.** The verbatim-script
  hash rule does not apply to templates (they are 3-way-merged
  customization-expected files), so a forked template merges normally and may
  conflict in the ordinary way.

### Tests required

`bootstrap/tests/test_lifecycle_contract.py` — one test beside the existing
trigger-slot test, named for the property rather than this proposal (per
`AGENTS.md` > durable artifacts): the triage section admits both directions.
It asserts:

* Both `triage-extra-triggers` and `triage-just-commit` appear exactly once,
  paired, in `templates/core/dev/proposals/_template.md`.
* Both appear exactly once, paired, in `dev/proposals/_template.md`.
* Cairn's own `triage-just-commit` body is filled, not the shipped placeholder.

Boundary A scope: that file plus `bootstrap/tests/test_upgrade.py` (the slot
parser and added-slot cases) and the standing prose gates for the touched doc
surfaces — `claim_check`, `link_check`, and `check_cairn`. No engine code
changes, so no Bandit or AST-attestation involvement.

### Examples / smoke checks

`bootstrap/scaffold.py --manifest` before and after, to confirm the published
manifest is byte-identical (it lists files, not slots). A scratch install into a
temporary target, confirming the new slot arrives with its placeholder and that
`grep -rn 'cairn:slot' <target>/dev/` lists it for the BOOTSTRAP fill checklist.

## Signals the change is wrong

* **Adopters fill it with blanket path exemptions rather than classes.** The
  fence is placeholder prose, and prose is a weak fence. Recovery: tighten the
  placeholder, or add a lint that rejects bare paths in that slot body.
* **The slot is `N/A` everywhere, including in Cairn.** Then the ambiguous
  middle was imagined and the honest move is to remove the slot — upstream slot
  removal is a flagged, non-silent path, so this is recoverable.
* **The recorded classes drift out of date and license changes nobody would
  approve today.** Recovery: the slot body is ordinary reviewable content; a
  stale entry is a review finding like any other.
* **A reviewer shows the loosening belongs in doctrine, uniform across
  adopters.** Then A2 is right and this is the wrong shape. Recovery: supersede
  in favour of a doctrine proposal, which carries the rate-limit gate this one
  deliberately avoids.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-20

**Superseded.**

**Maintainer authorization, quoted verbatim:**

> Okay, supersede then archive, please.

**Scribe**: Claude (Strategy). Commit permission was **explicitly given** in
that same instruction, which directs both the disposition and the archive move
— neither of which exists except as a commit. No separate confirmation was
sought or needed. Per the scribing guard-rail this is a Decision-only commit;
the archive move lands separately.

**Scribing context** — the scribe's framing, not the Maintainer's words. This
answers an offer made in the preceding exchange: supersede and re-open the
surviving question once the operating rule is settled, or append an author
revision re-scoping the proposal in place. The Maintainer chose the former.

**Basis in the record.** Two External strategy reviews (Codex; Antigravity),
folded into `dev/strategy/2026-08-20-claude-stewardship-ethic.md` at `be7d24e`,
invalidated three load-bearing claims of this proposal:

* **The count in *Context* is wrong.** The installed set carries **25 markers
  over 24 unique names**, not 26. The extra came from a marker sitting inside a
  fenced code block in `templates/README.md`, which documents the slot syntax
  and is installed nowhere.
* **"An adopter's apparatus can only ratchet heavier" is retracted** as
  overstated. `coordination-additions` records a *reduction* in its own slot
  body ("a sequential team runs only the baseline above"), so slot persistence
  favours whichever direction the adopter writes. What survives is narrower:
  the **prompting** and the **supported override authority** are asymmetric.
* **The `standard` / trivial / no-doctrine declarations rest on a false
  premise** — "adding one costs no doctrine at all." A marker is cheap;
  granting it bounded authority, defining what it may never exempt, and stating
  **precedence** against the mandatory triage list and the plan-scope rule is
  the design work, and it is not trivial.

**The severability claim failed.** This proposal was severed from the strategy
note on the premise that it stood alone. It does not: its placeholder fences
against the general triage list and the high-risk surfaces but is silent on the
**plan-deviation rule**, which the revised note's Finding 1 identifies as the
central undecided question. A widening slot cannot state precedence against a
rule nobody has decided yet.

**Where the surviving content lives.** The revised strategy note carries it as
**O5** (the slot work of its Finding 9, explicitly dependent on O4) and **Open
question 4** (the precedence contract). Re-opening is expected once the
operating rule is settled — deferred, not abandoned.

**Deferred-follow-up dispositions.** This proposal declared "no deferred
follow-ups" under *Triage and implementation shape*. Its single forward-looking
remark — A2, that widening the shipped escape-hatch prose "remains a separate
question worth asking on its own evidence" — takes disposition `accept`: it is
now homed in the revised strategy note as its own A2 and Open question 4.
