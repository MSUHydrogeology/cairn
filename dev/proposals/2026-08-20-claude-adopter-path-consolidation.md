# One installer: make the adoption ladder measure obligation, not mechanism

**Author**: Claude (Strategy)
**Model**: Opus 5
**Date opened**: 2026-08-20
**Status**: awaiting-review
**Assurance path**: high-assurance — see "Assurance-path reasoning". This
redefines a published adoption model existing adopters have been classified
under, and changes the behaviour of shipped executable code that keys off the
old distinction.
**Touches**: `README.md`; `on-ramp/README.md` (the ladder, the choosing-a-level
table, and the maturity ladder); `docs/getting-started.md`;
`docs/quickstart.md`; the three `bootstrap/profiles/*.yml` comment blocks;
`bootstrap/prompts/bootstrap-lite.md`; `bootstrap/BOOTSTRAP.md`;
`templates/README.md`; `templates/onboarding/*.md`;
**`doctrine/onboarding.md`** (the maturity-ladder trigger definitions);
`scripts/_onboarding/triggers.py` and its byte-twin
`templates/modules/default-on/_onboarding/triggers.py`; the onboarding trigger
tests under `bootstrap/tests/`.
**Related**: `dev/strategy/2026-06-12-claude-adopter-friction-audit.md` — this is
the "adopter-path consolidation proposal" that note named as its first
downstream surface and that was never opened;
`dev/strategy/archive/2026-08-10-claude-documentation-enhancement.md` > F9 (which
deferred the README lines here) and > F8 (the install-output friction, deferred
here and re-deferred below); `docs/solo-legacy-recipe.md` (the working
precedent).
**Plan review**: required(**Internal**) — the deliberative weight sits in this
proposal; a plan is mechanical translation across a known surface list. Ratified
at Decision.

## Context

Cairn publishes a three-level adoption ladder. **Level 1 — hand-copy the
kernel** is the level it recommends to its primary audience:
`on-ramp/README.md` says *"Level 1 is the natural home for solo + one-agent
adopters."*

The adopter-friction audit found in June that this level has no executable
greenfield path, and summarized the whole problem in one line: **"The product
has one functioning installer and two names for the experience around it."** Its
recommendation was not another installer, but to make the scaffold the single
installation mechanism for Levels 1 and 2, with the levels distinguished by
assessment and operating burden rather than by whether files were copied by
hand.

The Maintainer's framing when this resurfaced, quoted because it is what settles
the alternative below:

> Yeah no one will ever actually hand-copy Cairn, that's against the whole
> philosophy.

**Two months on, nothing carries the finding.** The `adopter-entry-doc-refresh`
proposal did the doc-polish half and archived; `solo-legacy-adopter-path`
mechanized the *legacy* branch and archived; the consolidation proposal was never
opened; `dev/PLANNING.md` has no row. The documentation-enhancement note's F9
then deferred the README lines to "the adopter-path proposal" — an artifact that
did not exist. Four artifacts each did an adjacent piece and each correctly
deferred the core to something nobody created. **No one decided to drop this.**

### What re-measurement adds to the June finding

Three things checked today, none of which were in the audit:

* **The contradiction is inside a single file.** `bootstrap/profiles/solo-greenfield.yml`
  says, in its own header comment, *"On-ramp recommendation: Level 1 (hand-copy
  the kernel + default-on modules...)"* — and six lines later, *"Quickstart
  adopters: copy this file as `profile.yml` in your target repo; see
  cairn/docs/quickstart.md for the literal command sequence."* The quickstart's
  command sequence runs `scaffold.py`. The same artifact recommends hand-copying
  and hands you the mechanized route.
* **The mechanized Level 1 already exists; it is just framed as a toy.** The
  audit concluded no runnable greenfield Level 1 route was found. Strictly, one
  is: `docs/quickstart.md` installs the `solo-greenfield` profile — invariant
  kernel plus the seven default-on modules, no team-gated modules — with the
  scaffold. Verified today: it completes, exit 0, on a fresh repo. What is
  missing is not a mechanism but **permission to use it on a real repository**,
  because the page presents it as a disposable-repo demonstration.
* **The level model has reached executable code, and it keys off exactly the
  distinction this proposal removes.** `_onboarding/triggers.py` fires
  `level-1-to-2` on *"`dev/.cairn/cairn-lock.yml` present (canonical Level 2
  signal)"*. The lockfile is written by the scaffold. So the moment Level 1 is
  mechanized, every Level 1 adopter is flagged as ready to promote to Level 2 on
  their first install, and the trigger stops meaning anything.

## Proposal

**Retire mechanism as the thing the ladder measures. Keep three levels; define
them by what the adopter is obliged to run.**

* **Level 0 — read the doctrine.** Unchanged, and genuinely different in kind:
  nothing is installed, there is no `dev/` tree.
* **Level 1 — the kernel, installed.** The scaffold, run against a minimal
  profile: the invariant kernel plus the default-on modules, no team-gated
  modules. The lifecycle runs with the Maintainer's own review (or a
  fresh-session read from the same agent type) covering the Dual-Review tier.
  This is what `docs/quickstart.md` already does.
* **Level 2 — the full apparatus.** The same scaffold, a wider profile: the
  team-gated modules the dimensional profile warrants, structural-independence
  floors actually staffed, and the assessment pre-pass and dogfood pass that
  `bootstrap/BOOTSTRAP.md` walks.

**One installer throughout.** The ladder becomes *read it → run it small → run
it wide*, and each rung names an obligation the adopter takes on rather than a
file-copying technique nobody uses.

Concretely:

1. **`on-ramp/README.md`** — rewrite the Level 1 section, the choosing-a-level
   table, and the maturity ladder's Level 0→1 and Level 1→2 rows, which
   currently read "hand-copy the kernel and run one real change" and "move to
   Level 2 when the customization is large enough that automating it pays."
   Under one installer, the second promotion is about *obligation*, not
   automation.
2. **`README.md`** — the three-level block, and the "Level 1 — hand-copy the
   kernel" bullet.
3. **`docs/getting-started.md`** — the ladder gloss and the "Ready to adopt?"
   pointer.
4. **`docs/quickstart.md`** — say plainly that its mechanism *is* Level 1 and
   may be run against a real repository, not only a disposable one. This is the
   smallest change with the largest effect, because the route already works.
5. **The three `bootstrap/profiles/*.yml` header comments** — remove the
   hand-copy recommendation that contradicts the file it sits in.
6. **`_onboarding/triggers.py` (both twins) and its tests** — `level-1-to-2`
   needs a signal that survives a mechanized Level 1. The lockfile no longer
   distinguishes the levels; **the installed module roster does.** The
   replacement signal, and whether the trigger should fire on roster width or on
   a staffed-review condition, is the one genuinely open design question here and
   is called out below rather than settled.
7. **`bootstrap/BOOTSTRAP.md`, `bootstrap/prompts/bootstrap-lite.md`,
   `templates/README.md`, `templates/onboarding/*.md`** — level references
   brought into line. `bootstrap-lite` describes itself as a step short of the
   full Level 2 procedure while ending by running the same scaffold; under the
   new model it is a Level 1 route and should say so.

### Documentation / doctrine surface

Nineteen shipped surfaces name the levels, and **one doctrine file does too**:
`doctrine/onboarding.md` defines the maturity-ladder triggers in the ladder's
own vocabulary, including *"`level-0-to-1` — `dev/proposals/_template.md` is
present (the canonical Level 1 signal: the adopter graduated from 'read the
doctrine' to **hand-copy the kernel**)"* and *"`level-1-to-2` — ... the adopter
ran the full bootstrap."*

**So this proposal does change doctrine**, and the rate-limit gate below applies.
It is a narrow change: the two canonical signals are re-expressed against
obligation rather than mechanism, and the surrounding trigger doctrine is
untouched. An earlier draft of this section asserted the opposite from a grep
that never covered `doctrine/`; the correction is recorded rather than quietly
made, because the same class of unchecked-absence claim is what let the original
finding sit for two months.

The dimension matrix and module gate-table **are** untouched: which modules a
profile selects is exactly as it was — only the name attached to a roster width
changes.

### Doctrine-change rate-limit (if this proposal changes doctrine)

**Applies.** `doctrine/onboarding.md`'s two canonical maturity signals are
defined in terms of the mechanism this proposal retires, so they cannot stay as
written.

The gate asks whether a single incident justifies a doctrine change. Two grounds
are offered, and a reviewer should test both:

* **Recurrence, not a single incident.** The same finding has been deferred four
  times across four artifacts — the friction audit named a consolidation proposal
  nobody opened; `adopter-entry-doc-refresh` did the doc half and archived;
  `solo-legacy-adopter-path` mechanized one branch and archived; the
  documentation note's F9 deferred to an artifact that does not exist. Nobody
  decided to drop it four times; the structure dropped it four times.
* **The doctrine is already describing something untrue.** `level-0-to-1` fires
  on `dev/proposals/_template.md` being present and calls that "hand-copy the
  kernel" — but the scaffold installs that template too, so the signal already
  fires for adopters who copied nothing. The doctrine text has been describing a
  mechanism its own trigger does not detect. This is a correction as much as a
  change.

### Assurance-path reasoning

`high-assurance`, and the field admits no default. Two of the mandatory triggers
are arguably met and the rule resolves uncertainty upward:

* **A public compatibility break.** Existing adopters were classified under a
  model where "Level 1" means hand-copied. After this they are reclassified by a
  definition they did not adopt under. That is a published-contract change even
  though no bytes of their tree move.
* **Shipped executable behaviour changes.** `_onboarding/triggers.py` runs in
  adopter repositories and its `level-1-to-2` promotion signal changes meaning.
  A trigger that fires on every fresh install is worse than one that never
  fires, because it trains the adopter to ignore it.

It is **not** a scaffold/merge-engine change: `bootstrap/_scaffold/` is
untouched, and the install set, fidelity manifest, gate manifest, lockfile
schema and published `--manifest` are all unchanged.

## Rationale

**Why not simply make hand-copying executable.** It is the cheap fix and it is
available: the two halves of the missing map both exist and are published — the
gate table (`bootstrap/BOOTSTRAP.md` > I-5, now with a diagram in
`dimensions/README.md`) says which modules a profile selects, and
`scaffold.py --manifest` gives 114 source→destination rows. Pointing Level 1 at
both would make it runnable this week.

It is still the wrong fix. **114 rows of manual file placement is not a thing a
scientist will do**, and a route nobody walks is not an adoption path — it is a
paragraph that makes the ladder look complete. It also commits Cairn to
maintaining a second installation mechanism, by hand, in perpetuity, against a
scaffold that already does the job correctly. The Maintainer's framing is the
sharper version: hand-copying is against the philosophy of a project whose whole
claim is a reproducible, verifiable install.

**Why the shape is already proven.** `docs/solo-legacy-recipe.md` hand-copies
nothing. It gives an exact composed profile, runs the scaffold, and expresses
the level as which modules the profile turns on. That is this proposal's model,
shipped and working, for the legacy branch. **Greenfield is simply the branch
that never got it** — which makes this a consolidation rather than an invention,
and much smaller than it was in June.

**Why the ladder is worth keeping at all.** The levels do real work: they let a
solo scientist adopt without pretending to staff a two-agent-type review, and
they give the maturity ladder somewhere to point. What they should not do is
encode a technique. Obligation is the honest axis, and it is the one the
dimensional profile already computes.

## Alternatives considered

**A1 — Do nothing.** The finding stays where it has been for two months: real,
diagnosed, uncarried. Rejected — F9 is now blocked on it, and a deferral that
outlives its owner is an accident rather than a decision.

**A2 — Make hand-copy executable** (point Level 1 at the gate table and
`--manifest`). Rejected on the rationale above. Kept on the record because it is
genuinely cheaper and a reviewer may weigh the trade differently.

**A3 — Collapse to two levels** (read the doctrine / run the scaffold),
dropping the Level 1 / Level 2 distinction entirely. Tempting, and it would
simplify the maturity ladder. Rejected: the distinction between "the kernel,
solo review" and "the full apparatus, staffed independence" is the one an
adopter most needs to make, and it is exactly the distinction the dimensional
profile exists to compute. Losing it would push every adopter toward the widest
roster, which is the failure the restraint doctrine warns about.

**A4 — Rename the levels** (e.g. "kernel" / "full") rather than redefining
them. Deferred, not rejected: worth considering during the plan, but it widens a
published-vocabulary change and the substance should settle first.

## Evidence / verification plan

| Claim | How it was established |
|---|---|
| Level 1 is recommended to the primary audience | `on-ramp/README.md`, the Level 1 section |
| Its instruction is not executable | The module step supplies no source→destination mapping; there are 114 in `scaffold.py --manifest` |
| The consolidation proposal was never opened | `ls dev/proposals/ dev/proposals/archive/`; no roadmap row in `dev/PLANNING.md` |
| A single profile file contradicts itself | `bootstrap/profiles/solo-greenfield.yml` header comment |
| The mechanized route already works | Ran `scaffold.py --config bootstrap/profiles/solo-greenfield.yml` into a fresh repo: exit 0 |
| The level model reached code | `_onboarding/triggers.py`, the `level-1-to-2` signal |
| 19 shipped surfaces name the levels | `grep -rln 'Level [012]\|hand-copy'` over the shipped tree |
| `doctrine/` does not name the ladder | Same grep, scoped to `doctrine/` — no hits |

### Author-accounting — invariants, failure modes, edge cases

* **Invariant: the module gate table is untouched.** Which modules a profile
  selects does not change; only the label attached to a roster width does. If a
  revision finds itself editing the gate table, the scope has slipped.
* **Failure mode: the promotion trigger silently inverts.** Handled as item 6,
  and named as the open design question rather than assumed away. A plan that
  lands the prose without the trigger change ships a signal that fires for
  everyone.
* **Failure mode: existing adopters read the new ladder and think their install
  is wrong.** The rewrite must say that an existing hand-copied tree is still a
  valid Level 1 — the definition changes, not their repository.
* **Edge case: the two `triggers.py` twins are byte-identical by contract.** Both
  change together or the fidelity check fails.
* **Known remaining friction, deliberately deferred with a disposition.** A
  `solo-greenfield` install prints 161 lines and reports **24 slot obligations**,
  several belonging to tiers the profile did not select (`coordination-additions`
  is the clearest). Measured today. This is F8's install-output finding and it
  makes "Level 1 is the small one" feel untrue on first contact. **Disposition:
  `accept` — carried as a named follow-up of this proposal, not fixed here.**
  Fixing it means classifying slot obligations by what the accepted profile makes
  live, which is a change to the install reporting path and would pull the
  scaffold engine into scope. Kept separate deliberately.

### Tests required

* The onboarding trigger tests under `bootstrap/tests/` —
  `test_trigger_evaluation_maturity.py` and `test_trigger_evaluation_action.py`
  own the `level-1-to-2` behaviour and must be rewritten alongside item 6, not
  merely re-baselined.
* `test_onboarding_activation_helper.py` and the byte-twin fidelity check, for
  the two `triggers.py` copies.
* The standing prose gates for every touched doc surface — `claim_check`,
  `link_check`, `check_cairn`, and the neutrality gate (the profiles and
  onboarding templates are adopter-facing).
* A fresh scaffold run against `solo-greenfield` into a temporary target,
  confirming the route the rewritten Level 1 points at still completes.

### Examples / smoke checks

`scaffold.py --manifest` before and after, confirming the published manifest is
byte-identical — this proposal must not move a single row of it.

## Signals the change is wrong

* **The rewritten Level 1 and Level 2 stop being distinguishable in practice** —
  if every adopter's profile lands in the same place, the ladder was carrying the
  mechanism distinction and nothing else, and A3 was right.
* **The replacement promotion signal fires as indiscriminately as the lockfile
  one did.** Recovery: make the trigger a staffed-review condition rather than a
  roster-width one, which is a judgment the adopter answers rather than a file
  the scaffold writes.
* **Adopters read "Level 1 = run the scaffold" and skip the readiness pre-pass**
  that a legacy tree needs. Recovery: the legacy recipe already gates this; the
  rewrite must not weaken its pre-pass language.
* **An existing hand-copied adopter cannot locate themselves in the new ladder.**
  That is a comprehension failure and would show up as the first support
  question; the fix is an explicit sentence, not a new level.
