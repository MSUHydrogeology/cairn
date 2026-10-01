# One installer: make the adoption ladder measure obligation, not mechanism

**Author**: Claude (Strategy)
**Model**: Opus 5 (opened); Opus 5.5 (Response, 2026-10-01)
**Opened**: 2026-08-20
**Status**: revising
**Review**: required(External) — the deliberate-lane proposal floor
(`doctrine/dual-review.md:217`). The one round taken (2026-08-31) was Internal;
the Response recommends the Maintainer waive the floor at Decision rather than
run a second round, and says why.
**Assurance path**: high-assurance — the change edits `doctrine/onboarding.md`,
and anything under `doctrine/` is a mandatory trigger.
**Touches** (Revision 1 — the documentation half): `README.md`;
`on-ramp/README.md`; `docs/getting-started.md`; `docs/quickstart.md`;
`docs/solo-legacy-recipe.md`; `bootstrap/profiles/solo-greenfield.yml` (header
comment only); `bootstrap/prompts/bootstrap-lite.md`; `bootstrap/BOOTSTRAP.md`;
`bootstrap/UPGRADE.md` (one line); `templates/README.md`;
`templates/codebase-readiness-report.md`; `templates/onboarding/*.md` (prompt
bodies; row headings unchanged); **`doctrine/onboarding.md`**;
`examples/minimal/README.md`; `examples/scientific-minimal/README.md`. **Not
touched:** `bootstrap/_scaffold/`, `scripts/_onboarding/` and its template
twin, any test, any frozen file — the executable half is split out (Revision 1
> Scope delta).
**Related**: `dev/strategy/archive/2026-06-12-claude-adopter-friction-audit.md` (merged 2026-08-26 into `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md`) — this is
the "adopter-path consolidation proposal" that note named as its first
downstream surface and that was never opened;
`dev/strategy/archive/2026-08-10-claude-documentation-enhancement.md` > F9 (which
deferred the README lines here) and > F8 (the install-output friction, deferred
here and re-deferred below); the same-day sibling
`dev/proposals/archive/2026-08-20-claude-adopt-into-existing-tree.md` (disjoint
surfaces, same triage).
**Plan review**: required(**Internal**) — with item 6 split out, the plan is a
prose rewrite over the surfaces enumerated in Revision 1. Ratified at Decision.

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

## Review -- Claude (Internal, fresh-context subagent) -- 2026-08-31

**Model**: claude-opus-5 (Claude Opus 5)

Reviewed commit: 468c7448c7f696b0b6ca6eb8a75e983cf1b848bf
Target: the proposal as opened -- `## Context` (31) through `## Signals the change is wrong` (304)
Prior findings: none
Assurance path: high-assurance

**Tier**: Internal
**Findings**: raised (9 blocking, 9 non-blocking, 3 nits)

No `Plan readiness` is recorded: only an **External** pass may supply it. Tracked
tree confirmed clean before every read, so line numbers are the committed ones.

### What I checked

Four lenses -- design soundness; the adopter's first two weeks; published contract
and backward compatibility; evidence and falsifiability -- over four ground-truth
passes. Instruments, each with its control:

* `grep -rlE "Level [012]|hand-copy"` over the shipped roots -> **26 files**
  (control: matched `README.md` immediately, so absences below are evidence).
* `evaluate_maturity_triggers` on a fresh `solo-greenfield` install ->
  `['level-1-to-2']` at zero archived proposals; add one archive file ->
  `['level-0-to-1', 'level-1-to-2']`, so the evaluator *can* fire `level-0-to-1`.
* `render_active_surfacing_prompt` with each row name from `_ACTIVE_SURFACING_ROWS`:
  `collab-agreement-signing` 424 chars, `second-agent-type` 459,
  `Level-1-to-2-graduation` **None** -- two rendering siblings are the control.
* Gate-manifest fixture parsed (183 frozen entries), candidates hashed live; the
  probe separates FROZEN-MATCH from NOT-FROZEN and from a nonexistent path.
* `scaffold.py --manifest` -> 98 lines (header + 97 rows); install into a fresh temp
  repo -> exit 0; onto a hand-copied tree -> 16 skips, no lockfile, `--force`
  verified to overwrite authored content.
* `claim_check.py` -> OK (control: a scratch file with one bad path -> 1 hard flag);
  `check_cairn.py` over the seven ladder surfaces -> clean; `quality_gate.py --sub
  neutrality` -> no mentions, which is structural, not a pass
  (`scripts/quality_gate.py:440-472` does not scan `dev/`).
* `test_active_surfacing_render.py`, `test_trigger_evaluation_maturity.py`,
  `test_quickstart_sequence.py` -> 33 passed (Python 3.13.x, canonical interpreter).
  **Every check the proposal registers is green today.**

Not run: the full suite; anything on a real adopter tree (there are none -- [N9]).

### Steelman

**The diagnosis is real and better evidenced than the proposal claims.** Every
load-bearing quote of shipped prose verifies exactly -- `on-ramp/README.md:33` and
`:94-95`, `README.md:266`, `solo-greenfield.yml:22-27`, `doctrine/onboarding.md:69-73`,
the friction-audit line, the "no roadmap row" claim. The sharpest exhibit is unused:
`docs/quickstart.md:350-353`, the page's last substantive instruction, tells an
adopter who just installed that "Most teams start at Level 1" -- the level they did
not do. And the hand-copy instruction really is non-executable: 18 files, 18
`{{token}}` occurrences, 21 `cairn:slot` blocks, ~20 destinations documented nowhere.
The direction is right, the A2 rejection is correct, and the trigger hazard is
disclosed rather than smuggled. Nine blocking findings do not mean "do not do this";
they mean the artifact does not yet describe accurately enough what will be done.
Every satisfier is additive -- none reopens the design, none narrows scope.

### Findings

* **[R1] BLOCKING -- the criterion replacing "mechanism" is wrong, in the prose and
  in the trigger.** Design + adopter lenses (a); design + contract lenses (b).
  (a) `:92-95` defines Level 1 as the kernel plus default-on modules, "**no
  team-gated modules**". `docs/solo-legacy-recipe.md:50-52` requires `legacy-agent`
  and `testing-discipline`, both under `templates/modules/team-gated/` -- so the solo
  scientist on a legacy codebase, whom `on-ramp/README.md:67-69` keeps at Level 1 in
  as many words, becomes Level 2; and `on-ramp/README.md:95` defines the
  *deepen-within-Level-1* rung as "test tiers, the doc-drift gate, an examples
  gallery," all three team-gated, so exercising that rung promotes you out of the
  level. `team-gated/` is a directory tier, not a staffing predicate: only
  `dual-review` and `coordination-tiers` key on `agent_team` (`config.py:1325-1330`).
  (b) `:125` states the replacement axis as settled -- "the installed module roster
  does" -- but the roster persists only in `dev/.cairn/cairn-lock.yml` and
  `profile.yml`, both scaffold-written, so it is unevaluable for the hand-copy
  population `:270-272` promises to protect, and it is the shape already removed from
  this file (`triggers.py:81-88`: the `_template.md` check "fired at install time for
  every adopter and carried no signal value"). `level-1-to-2` is also the classifier
  gating `level-1-deepen`/`level-2-deepen` (`triggers.py:108-121`), unmentioned here.
  C0: yes -- this is the definition ~20 shipped surfaces plus `doctrine/onboarding.md`
  get rewritten to, in an append-only accepted record; re-inverting a published level
  name is a second vocabulary break, not a revert. Satisfier: state **one** criterion
  and derive the rest -- staffed structural independence survives the solo-legacy case
  -- say which governs when roster and staffing disagree, add both deepen triggers to
  `Touches`, and either settle the signal here or demote `:125` to open (see [R9]).

* **[R2] BLOCKING -- the "working precedent" is an instance of the alternative the
  proposal rejects.** Claim-verification, contract and adopter lenses. `:213-216` says
  `docs/solo-legacy-recipe.md` "hand-copies nothing ... runs the scaffold." The file
  says the opposite twice: `:17` "**Level 1** -- hand-copy the kernel
  (`templates/core/`), no bootstrap script," and `:33-36` "`scaffold.py --summary` as
  a **roster-computation oracle** -- it tells you which modules to hand-copy, it does
  not install anything for you. **This stays a Level 1 hand-copy path**." That is A2's
  shape. The file is absent from `Touches`, so after the rewrite `on-ramp/README.md`
  says Level 1 means run the scaffold while the recipe it links to at `:73` says it
  means do not. C0: yes -- this is the sole support for "a consolidation rather than
  an invention, and much smaller than it was in June" (`:216-218`), the sentence that
  most shapes how a Decision sizes the change. Satisfier: withdraw "the working
  precedent" and argue on the merits, **or** add the recipe to `Touches` as a surface
  that must also be converted and re-size accordingly. Not both.

* **[R3] BLOCKING -- item 4 blesses `docs/quickstart.md` for real repositories without
  touching its trust ceremony, its `rm -rf`, or the installer string that contradicts
  it.** All four lenses. Item 4 (`:118-120`) is one sentence. Disposability is that
  page's spine: `:47` ("You are *not* installing Cairn into a real project here"),
  `:61-67` (release-tag signature verification explicitly skippable *because*
  throwaway), `:153-157` (the provenance warning "does not appear" in a real adoption;
  Step 1 clones tip), `:287-290` (`## Step 7 -- teardown` / `rm -rf
  /tmp/cairn-quickstart`). `test_quickstart_sequence.py` covers Steps 1-3 and 4-6 by
  its own docstring; grep `step7|teardown|rm -rf` -> nothing (control `step6|step3` ->
  3). And `bootstrap/_scaffold/install.py:1462-1470` prints on every install "(Just
  trying Cairn on a throwaway repo? The docs/quickstart.md shakedown skips 3-5 ...)",
  so `bootstrap/_scaffold/` is *not* untouched. C0: yes, twice -- an adopter follows a
  page now sanctioned for their real project into a bare `rm -rf` of a substituted
  path, or installs unverified tip code; and that string sits on a named
  Security-Review trigger surface, so accepting with the surface list wrong ratifies
  the wrong tier. Satisfier: expand item 4 to name the structural edits (real-repo
  branch, teardown fenced to disposable, release-tag verification required on the real
  branch, which of Act II-3/4/5 a real Level 1 owes); merge items 4 and 7, since
  `bootstrap-lite.md:14-26` states its reason to exist in terms item 4 voids; and
  either add `install.py:1462-1470` to `Touches` and correct `:192-194` or record it
  as a deferred inconsistency with a disposition.

* **[R4] BLOCKING -- "the gate manifest is unchanged" (`:192-194`) is false, and the
  staleness is silent.** Contract + evidence lenses.
  `bootstrap/tests/fixtures/gate_manifest.json` freezes seven files this change
  touches, all FROZEN-MATCH today (hashed): both `_onboarding/triggers.py` and
  `_onboarding/prompts.py` template twins, plus `test_trigger_evaluation_maturity.py`,
  `test_trigger_evaluation_action.py`, `test_onboarding_activation_helper.py`,
  `test_active_surfacing_render.py`, `test_active_surfacing_mechanism.py`.
  `test_gate_manifest.py` verifies a freshly produced manifest against itself and
  never diffs the committed fixture -- the pitfall `AGENTS.md` names; and the named
  byte-twin check (`:291-292`) stays green because both twins change together. C0:
  yes -- the plan is written from this declaration, the files are edited, the suite
  stays green, and the trust root goes stale unreported; once commits land on top,
  drift is indistinguishable from tampering without the Maintainer-only ceremony
  (`bootstrap/REANCHOR_RUNBOOK.md:9-15`), which the proposal fences nowhere.
  Satisfier: strike "gate manifest" from `:193`; add the three missing files to
  `Touches`; add a **MAINTAINER-ONLY** plan chunk naming the runbook and the expected
  FROZEN-MODIFIED set, sequenced after the last implementation commit; and add a
  committed-fixture verify to the smoke checks, which the suite omits.

* **[R5] BLOCKING -- the Level 1->2 graduation prompt renders empty today, and its
  test passes a string production never passes.** Contract + adopter lenses;
  reproduced above. `scripts/_onboarding/prompts.py:22-26` registers row name
  `Level-1-to-2-graduation`; `:58-63` builds `^###\s+Row\s+\d+\s+--\s+.*<escaped
  name>.*$`; every preset heading is `### Row 2 -- Level 1→2 graduation prompt`
  (`solo-greenfield.md:107`, `collaborative-team.md:130`, `high-rigor-legacy.md:141`).
  `1→2` never matches `1-to-2`. `test_active_surfacing_render.py:93-97,157-166`
  substitutes the keyword `"Level 1"` before calling the renderer, so the suite is
  green while the adopter gets a fallback pointing at `doctrine/onboarding.md`, absent
  from an installed tree. (The evidence lens read this as non-blocking because
  preserving the trigger *name* means `prompts.py` needs no edit -- true of the
  trigger map, and it does not reach the render miss.) C0: yes, three ways -- `:187-190`
  rests the high-assurance tier on an adopter-visible nag that cannot currently reach
  the adopter; item 7 rewrites those exact headings, so the plan will fix or entrench
  a coupling it was never told about, green either way; and the row name is the
  idempotency key in `dev/.cairn/onboarding-activated.jsonl`, so renaming it re-fires
  the one-shot for everyone who already dismissed it, in trees Cairn cannot reach.
  Satisfier: record the breakage and say whether it is fixed here or split out; add
  `_onboarding/prompts.py` (both twins) and both `test_active_surfacing_*.py` to
  `Touches`; name the coupling chain (trigger id -> row name -> preset `[trigger:]`
  tag -> `### Row N --` heading -> activation-log key) as an invariant; and add a test
  taking row names **from `_ACTIVE_SURFACING_ROWS` itself**, asserting non-None for
  every (preset, row) pair.

* **[R6] BLOCKING -- the doctrine-surface record is wrong twice, once inside the
  artifact.** Claim-verification + contract lenses. (a) The Evidence row at `:259`
  still reads "`doctrine/` does not name the ladder -- Same grep, scoped to
  `doctrine/` -- no hits," while `:144-150` records that this was an earlier draft's
  error "from a grep that never covered `doctrine/`" and states the correction; the
  row is the uncorrected claim, and `doctrine/onboarding.md:69-96` does carry the
  vocabulary. The failure the proposal warns about is live in the artifact to be
  decided on. (b) Rate-limit ground #2 (`:171-176`) says `level-0-to-1` fires on
  `_template.md` presence; `triggers.py:100-102` fires it on `archived_proposals >= 1`
  and has since `7519c5d` (2026-06-12), reproduced above. Ground #1 (four-artifact
  recurrence) verifies independently and carries the gate alone. C0: yes -- `:145-146`
  commits to re-expressing both signals "against obligation rather than mechanism," so
  an implementer holding this model rewrites the `level-0-to-1` line and leaves it
  still divergent from code that counts archives, inside a commit whose stated purpose
  is correcting that line; a line a reader believes was just checked, and was not, is
  harder to undo than one known to be stale. Satisfier: correct the table row;
  withdraw ground #2 and rest the gate on recurrence; restate the doctrine job as
  **reconciliation with shipped behaviour**; and add an acceptance criterion that each
  maturity-signal sentence names the condition `evaluate_maturity_triggers` evaluates.

* **[R7] BLOCKING -- the evidence lock is vacuous: nothing registered can fail on the
  central outcome, and the one lockable criterion is declared unlockable.** Evidence
  lens. All five registered checks are green today and none is sensitive to whether
  the rewrite is complete, partial or self-contradictory: the scaffold run cannot
  break, because `:192-194` says no code path it uses changes;
  `scripts/check_cairn.py:259-281` re-measures only numbers carrying a
  `<!-- verify: -->` annotation, of which the four ladder surfaces have exactly one;
  `--manifest` emits path rows, so a content change cannot move one. The deliverable
  is a rewrite over a **declared** set of "nineteen shipped surfaces" (`:137`) and no
  check compares delivered against declared. And `:127-128`/`:289-290` defer item 6's
  criterion as undesignable, when a design-independent invariant is writable today and
  catches the failure `:267-268` names: `evaluate_maturity_triggers` on a fresh
  minimal-profile install with zero archived proposals and plans must **not** contain
  `level-1-to-2`. C0: yes -- Accepting ratifies a Stage-1 lock whose green result is
  known in advance, and a half-finished rewrite leaving
  `docs/solo-legacy-recipe.md:35` ("This stays a Level 1 hand-copy path") beside a
  README saying the opposite ships a *worse* version of the contradiction this
  proposal exists to remove, every check green. Satisfier: add that negative trigger
  invariant to `Tests required`, pre-committed and design-independent; and add a
  completeness invariant over the **declared** set to `Examples / smoke checks` --
  enumerate the 19 surfaces by path and register the vocabulary grep as an acceptance
  criterion returning only an explicit allowlist of deliberate retentions, run before
  the rewrite as its own positive control.

* **[R8] BLOCKING -- no item covers the adopters the redefinition reclassifies, and
  the new prose induces an action that destroys their work.** Adopter lens,
  reproduced. `:270-272` ("the rewrite must say that an existing hand-copied tree is
  still a valid Level 1") sits in Author-accounting and appears in none of items 1-7,
  so a plan built from the item list ships the reclassification with no migration
  text. Measured on a hand-copied tree: install -> exit 0, 16 `[skip] ... pass --force
  to overwrite`, `[warn] cairn-lock.yml NOT written: 9 installed file(s) differ`; and
  re-running with `--force`, as the message advises, removed a hand-written line from
  `AGENTS.md`. The real recovery (`upgrade --init-lock` -> fill four placeholders ->
  re-run) appears only at `bootstrap/UPGRADE.md:170-187`, under a heading a hand-copy
  adopter will not read as addressing them, in no adopter-facing page and nowhere in
  the proposal (greps: `migration` 0, `init-lock` 0; control `scaffold` 20). C0: yes
  -- force-overwriting filled `cairn:slot` bodies loses work, `unrecoverable-base` is
  durable per `UPGRADE.md:180-187`, and reassurance-only mitigation induces exactly
  the action that causes the loss. Satisfier: add an item -- a named migration
  paragraph in `on-ramp/README.md` with the literal `upgrade --init-lock` sequence,
  stating that a hand-copied tree gets no upgrades and no maturity prompts until it
  runs, and saying explicitly **not** to pass `--force`. Add `UPGRADE.md` to `Touches`.

* **[R9] BLOCKING -- the header never declares the proposal's own review obligation,
  and the design that earns high-assurance is routed to the weaker floor.** Hygiene
  audit + design lens. `dev/proposals/_template.md:79-83` requires five header fields;
  **`Review`: is absent entirely** (the only `Review` match in the file is
  `**Plan review**` at `:27`, present and well-formed, so the instrument is fine). The
  mandatory `#### Security preflight` block, or its one-line `N/A: no trust boundary
  added, moved, or widened` fallback, is also absent (0 hits), and the template says
  an absent answer is itself a review finding. `### Assurance-path reasoning`
  (`:178-195`) cites two off-template grounds and never names the one enumerated
  trigger that cleanly fires -- "anything under `doctrine/`" -- which `:144` has
  already conceded. Then `:27-29` sets `Plan review: required(Internal)` because "a
  plan is mechanical translation across a known surface list," while `:127-128` calls
  item 6 "the one genuinely open design question here" and `:244-246` defers A4 to the
  plan. C0: yes -- `doctrine/lifecycle.md:71-75` makes a floor declared, not a
  reviewer's lever, and that binds the author too; if the design earning
  high-assurance is decided under Internal plan review the declaration bought nothing,
  unrecoverably, because the record will claim the higher tier. Satisfier: add
  `**Review**:` with an explicit tier; rename `Date opened` to `Opened`; enter the
  Security-preflight line (N/A is the likely answer, but it must be entered); cite the
  `doctrine/` trigger; and either settle item 6 and A4 here or raise the plan tier and
  delete the "mechanical translation" justification.

---

* **[N1] `Touches` is short of the measured set.** Absent, carrying the retiring
  framing: `templates/codebase-readiness-report.md:344-345` -- the shipped instrument
  that *assigns* an adopter their level, and which `README.md:281-286` routes every
  legacy adopter to first; `examples/minimal/README.md:11` and
  `examples/scientific-minimal/README.md:34` (their `dev/` trees hold one archived
  proposal, so a word swap will not make them honest); `docs/agent-team-onboarding.md`
  `:7-9`; plus everything [R2]/[R4]/[R5] add. Unmapped in `Tests required`:
  `test_active_surfacing_render.py` (item 7) and `test_quickstart_sequence.py` (item
  4) -- both redden loudly, so the cost is Boundary B scoping, not a shipped defect.
  Conversely item 5 over-reaches: only `solo-greenfield.yml` carries the hand-copy
  recommendation; the other two profiles already recommend Level 2.

* **[N2] The misfire is present tense, which strengthens the case.** `:187-190` says
  the signal "changes meaning"; it has none to change -- it already means "you ran the
  scaffold," and fires today for every quickstart and bootstrap-lite follower and
  every Level 2 adopter (`bootstrap/_scaffold/cli.py:740` writes the lockfile
  unconditionally). Rewrite `:78-83` in the present tense with the reproduction and
  drop that assurance ground; the `doctrine/` trigger carries the tier alone.
  Corollary: item 6 need not be gated behind the redefinition at all.

* **[N3] Four numbers are stale or measure the wrong set.** `--manifest` is 97 rows,
  not 114 (`:202`); author-accounting prints ~140 lines / 22 slots, not 161 / 24
  (`:276-279`) -- both exact at the authoring commit `160c583` and drifted by the
  subtraction sweep; "the seven default-on modules" (`:74`, `:92-95`) is six
  (`config.py:82-95`). The 114 figure is load-bearing for the A2 rejection while
  measuring the whole manifest -- the hand-copy set is 18 files, and the measured
  obstacle (18 token occurrences, 21 slot bodies, ~20 undocumented destinations) is a
  *stronger* rejection. `solo-greenfield.yml:17-19` and
  `docs/solo-legacy-recipe.md:55-62` also list retired modules, so the recipe's
  "confirm your run matches" check cannot pass.

* **[N4] A commitment the binding strategy note assigned here is dropped without a
  disposition.** `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md`:
  "Quickstart command hygiene (path-scoped commits; a staging list that matches the
  installed state) rides with the consolidation rather than as separate items." Still
  live: `docs/quickstart.md:194` omits `NOTICE.md`, which the scaffold installs
  (`config.py:540`). The deferred-friction section dispositions only F8; give this one
  `accept`, `defer` or `wontfix`, with a reason.

* **[N5] Three of the four "Signals the change is wrong" are not falsifiers.** Signal
  1 names no observation or threshold; signal 3's recovery ("must not weaken its
  pre-pass language") is satisfied by doing nothing, since that file is not in
  `Touches`; signal 4 waits on a support question from an empty adopter population.
  Signal 2 is a real falsifier, misfiled -- it belongs in `Tests required` ([R7]).

* **[N6] A3 is rejected on a consequence no code path produces.** `:238-242` claims
  losing the ladder "would push every adopter toward the widest roster," but the roster
  derives from preset plus six axes (`config.py:1353-1392`) and no engine code reads a
  level (control: `grep "preset" config.py` -> hits; the level grep over
  `bootstrap/_scaffold/` and `bootstrap/profiles/` -> three YAML comments only). The
  argument that survives is one sentence earlier -- the ladder is a self-locate aid for
  review staffing. Add A3's genuine cost: the four maturity triggers lose their
  addressing scheme.

* **[N7] The byte-twin edge case is stated backwards, and a lockfile re-finalize is
  owed.** `bootstrap/verify_integrity.py:106-111` compares on-disk bytes to the
  *lockfile-recorded* hash, never to the template, so a template-only edit passes (the
  dangerous direction) and a correct coordinated edit **fails** until the tracked
  `dev/.cairn/cairn-lock.yml` is re-finalized -- the opposite of `:273-274`, and
  nothing in the suite runs it against Cairn's own tree. Correct the sentence, add the
  re-finalize as a named plan step, and add `verify_integrity.py` to `Tests required`.

* **[N8] The "one genuinely open design question" is already half-answered by a
  shipped trigger.** `scripts/_onboarding/triggers.py:386` defines `second-agent-type`
  -- "team-roster slot lists 2+ distinct agent identifiers," an explicit-state signal,
  not a file the scaffold writes -- and `docs/agent-team-onboarding.md:7-9` already
  calls it "the trigger that graduates the deployment past Level 1's review baseline,"
  the boundary `:94-95` uses. Naming it in item 6 shrinks the question to "should
  `level-1-to-2` alias the existing condition?" and removes the *build nothing new*
  exposure.

* **[N9] The premise is argued, not measured, and the proposal does not say so.**
  `dev/measurement/` holds zero ladder evidence (control, same flags and scope:
  `adopter|lockfile` -> 65 hits), and Cairn has zero external adopters
  (`dev/proposals/archive/2026-08-03-claude-byline-classification.md:342`). The defect
  being fixed is internal self-contradiction, which needs no adopters -- so label it
  that way, as `dev/plans/archive/profile-parse-fail-open.md:521` does, and disposition
  the friction audit's eight success criteria rather than leaving them unmentioned.

---

* **[T1] nit** -- the `--manifest` invariant is sharp against row movement and
  insensitive to file content, so it is not evidence the rewrite is correct. Add
  "provided no file is added, removed, or renamed," so a revived A4 rename is visibly
  able to move rows.
* **[T2] nit** -- `Documentation / doctrine surface` and `Assurance-path reasoning`
  are H3s nested under other sections rather than the standalone `##` sections the
  template names; `Related` omits the same-day sibling
  `2026-08-20-claude-adopt-into-existing-tree.md` (disjoint surfaces, same triage).
* **[T3] nit** -- "six lines later" (`:68`) is two to four; `docs/quickstart.md:296`
  prints "Time: ~30 seconds" on a page whose opening note declines to state one.

### Not covered / low confidence

* **Same-type reviewer**, and no `Plan readiness` from an Internal read.
* **No full suite run** -- three test files only, so nothing here is evidence about
  the rest of the suite.
* **The Maintainer quote is unverifiable** -- "Yeah no one will ever actually
  hand-copy Cairn" (`:49-50`) appears nowhere in `dev/` outside this proposal; it
  settles an alternative and is not a standing authorization for the redesign.
* **The *build nothing new* question** -- I read item 6 as inside *fix defects*, but
  it is genuine new decision logic; [N8] would dissolve it. Not adjudicated.
* **[R8]'s severity** -- mechanism and `--force` loss verified; whether a supported
  reconciliation makes `unrecoverable-base` routinely recoverable, I did not determine.
* **The 19-surface figure** -- I measured 26 files (25 excluding `CHANGELOG.md`); I
  did not reconstruct which 19 the author counted.

### Second-round recommendation

**Split, then take the second pass External.** The documentation consolidation is
genuinely low-risk once [R1a], [R2], [R3], [R6] and [R7] land, and it delivers most of
the adopter value. The executable half -- the replacement axis ([R1b]), the live
render defect ([R5]), the frozen-fixture re-anchor ([R4]) and the row-name idempotency
migration -- is less understood than the document represents, and each is a design
still movable, which is exactly the case `doctrine/dual-review.md` reserves the
External proposal floor for.

Split or not: **this Internal pass does not discharge the External floor on
deliberate-lane proposal review** (`doctrine/lifecycle.md:71-75` -- floors "stay as
declared ... a floor is not a reviewer's lever"). Clearing the findings above returns
the artifact to `awaiting-review`, not `awaiting-decision`; the External round is
still owed, and it is the pass that may record `Plan readiness`.

**Disposition: blocking.** Nine blocking findings ([R1]-[R9]); status moved to
`revising`.

## Response -- Claude (author) -- 2026-10-01

**Model**: claude-opus-5-5 (Claude Opus 5.5)
Responding to: the Internal review of 2026-08-31, findings [R1]-[R9], [N1]-[N9], [T1]-[T3].

Two things changed after the review, and both shape this Response.

* **[R5] is already fixed.** `a1a58f93` (2026-09-01) repaired the graduation-prompt
  matcher without renaming the row, and the test now takes row names from the registry
  for all nine preset x row pairs -- the review's own satisfier.
* **Review is one round** (`898398f6`; `doctrine/dual-review.md:143`). The author's
  revision carries the status forward, and a second round exists only for material the
  review never saw. So this Response answers each finding with the satisfier the review
  named, and moves the proposal to `awaiting-decision`. The one place it departs from a
  suggested satisfier is marked ([R1]).

### The split

**I am taking the review's recommendation and splitting the proposal.** This artifact
keeps the documentation half: the ladder's redefinition across the adopter-facing pages,
`doctrine/onboarding.md`, and a migration note. The executable half -- item 6, the
replacement for the `level-1-to-2` signal and the deepen classifier it gates, with its
gate-manifest re-anchor and lockfile re-finalize -- leaves for its own proposal.

Why split rather than settle item 6 here:

* **The halves cost different things.** Checked today, no file in the documentation half
  is frozen in the gate manifest or recorded in Cairn's own lockfile, so its plan is
  prose verified by prose gates: no suite run, no Maintainer ceremony. The executable
  half touches seven frozen files and needs the Maintainer-only re-anchor.
* **Neither depends on the other.** The misfire is present tense ([N2]): `level-1-to-2`
  fires on the lockfile, which every scaffold install writes, so it fires today for every
  quickstart follower. The documentation half neither causes it nor needs it fixed first.

**The cost.** Until the split-out proposal lands, a scaffolded Level 1 install sees the
Level 1->2 prompt once, at its first goodnight. Item 7 rewrites that prompt's body to
state its own condition, so an early showing reads as "this applies when...", not as an
instruction. Cairn has no external adopters today ([N9]).

Dropping item 6 is a scope reduction, which only the Maintainer can allow. It is
recorded in Revision 1 > Scope delta, with both deferred items as one batch for the
board.

### The External floor -- the one question for the Maintainer

`doctrine/dual-review.md:217` keeps "the External floor on deliberate-lane proposal
review". The one round here was Internal. **I recommend the Maintainer waive the floor
at Decision rather than run a second round:**

1. **The review did the External work in substance.** It gave a verdict on whether the
   change should happen ("The direction is right"), weighed the strongest alternative
   (confirmed the A2 rejection, corrected the A3 one in [N6]), and named what would
   falsify it ([N5], [R7]).
2. **Its reason for wanting External was the executable half** -- "a design still
   movable". The split sends that half to its own proposal, which takes its own review.
3. **The Maintainer's direction of 2026-10-01**: a single round on the proposal, then
   the decision.

If the Maintainer prefers the round, it needs a fresh session, not a second agent type,
and it reads this Response rather than the whole artifact.

### Dispositions

**[R1] Accepted, with one departure.** (a) **One criterion: staffing -- whether more
than one agent works in the tree at once.** Level 1 is one Maintainer working with one
agent at a time (`agent_team: single`). Level 2 begins when the work is concurrent
(`concurrent-single-type` or `concurrent-multi-type`), the axis on which the scaffold
already adds `coordination-tiers` and `dual-review`
(`bootstrap/_scaffold/config.py:1312-1331`). The roster follows the profile; where roster
and staffing disagree, **staffing governs** -- so a solo legacy adopter running
`legacy-agent` and `testing-discipline` is Level 1, and deepening within Level 1 promotes
no one. The text says plainly that `team-gated` is a directory, not a level.
*The departure:* the review suggested "staffed structural independence". Since
2026-09-01 no review tier requires a different agent type, so independence is no longer
something a team must staff. Concurrency is what changes a team's needs, and it is the
axis the engine already reads. If the Maintainer reads this as material the review never
saw, it is the one place a round on this Response would have something to read.
(b) Item 6 and both deepen triggers move to the split-out proposal; `:125` no longer
stands as settled.

**[R2] Accepted.** "The working precedent" is withdrawn, and with it "much smaller than
it was in June", which rested on it. `docs/solo-legacy-recipe.md` joins `Touches` as a
page to convert: "run the scaffold with this profile", not "hand-copy what `--summary`
lists". Measured today: the recipe's profile, scaffolded into a scratch repository that
already had its own `README.md` and `CHANGELOG.md`, exits 0, writes the lockfile, and
leaves both files untouched.

**[R3] Accepted -- by keeping the quickstart disposable, not by removing that.** Its
teardown, its waiver of the signature check for a throwaway clone, and its framing stay.
Item 4 becomes: the page says plainly that the commands just run *are* a Level 1
install, and "What to do next" gives the real route -- Steps 2-3 in your own repository,
from a release tag verified per `bootstrap/PROVENANCE.md` (not skippable there), then the
four steps the installer prints for a real adoption (Act II-3 to II-6). Two consequences:
the installer's throwaway line (`bootstrap/_scaffold/install.py:1462-1469`) stays true,
so the engine is untouched; and bootstrap-lite's reason to exist
(`bootstrap/prompts/bootstrap-lite.md:14-26`) is not voided, so items 4 and 7 need no
merge. bootstrap-lite is re-described as the assessment-assisted route to either level.

**[R4] Resolved by the split.** Checked today against `frozen_files` in the committed
fixture (183 entries; control: the `_onboarding/triggers.py` template twin reads
frozen): no file in the revised `Touches` is frozen. The seven the review found all
belong to the executable half and leave with it. One frozen neighbour constrains the
rewrite: `bootstrap/tests/test_quickstart_sequence.py` reads two phrases from
`docs/quickstart.md` (`**N** modules listed`, `**N unfilled block slots**`). The rewrite
keeps both, so the test is not edited. A committed-fixture check joins the acceptance
criteria.

**[R5] Closed independently** by `a1a58f93`. This revision adds one invariant: the
`### Row N --` headings in `templates/onboarding/*.md` are not renamed.

**[R6] Accepted.** The Evidence row is corrected. Rate-limit ground #2 is withdrawn, and
the gate rests on recurrence alone. The doctrine job is restated as reconciliation with
shipped behaviour, with an acceptance criterion: each maturity-signal sentence in
`doctrine/onboarding.md` names the condition `evaluate_maturity_triggers` evaluates
(`scripts/_onboarding/triggers.py:101-104`).

**[R7] Split.** The negative trigger invariant tests item 6 and leaves with it; it fails
today, which is the defect. The completeness invariant stays here: the declared set is
enumerated by path in Revision 1, with a grep whose before-and-after results are fixed in
advance.

**[R8] Accepted** as new item 8, a migration note in `on-ramp/README.md`. The literal
sequence was run today on a scratch hand-copied tree: `python bootstrap/scaffold.py
upgrade --target <repo> --init-lock` writes `dev/.cairn/profile.yml` with four
placeholders and stops (exit 2); fill them; re-run -- exit 0, lockfile written,
token-substituted files upgrade as review-only diffs. The note says a hand-copied tree is
still Level 1, that without a lockfile it gets no upgrades and no maturity prompts, and
**not to re-run the install with `--force`**. `bootstrap/UPGRADE.md` joins `Touches`
for one pointer line, so a hand-copy adopter recognises its migration section as theirs.

**[R9] Accepted.** The header gains `Review` and `Opened`; the Security-preflight line is
entered; the Assurance path cites the `doctrine/` trigger. A4 is settled: the names
stay. With item 6 split out the plan is a prose rewrite over an enumerated list, and
`Plan review: required(Internal)` stands -- it is also the only plan tier doctrine now
has.

**[N1] Accepted.** `templates/codebase-readiness-report.md`, both example READMEs and
`bootstrap/BOOTSTRAP.md` join `Touches`. The examples will describe how they were
actually built -- a hand-copied kernel, no lockfile -- rather than claim a route they did
not take. `docs/agent-team-onboarding.md:7-9` already matches the staffing criterion and
needs no edit. Item 5 narrows to `solo-greenfield.yml`: the other two profiles are
`concurrent-multi-type` and already recommend Level 2.

**[N2] Accepted.** Context is in the present tense; the executable-behaviour assurance
ground is dropped.

**[N3] Accepted**, re-measured today: 97 manifest rows; a `solo-greenfield` install
prints 140 lines and 22 slots; six default-on modules; 18 kernel files.
`solo-greenfield.yml:17-19` and the recipe's ten-module roster
(`docs/solo-legacy-recipe.md:50-62`) still list `lifecycle-metrics` and
`fold-back-ledger`, retired in August; the legacy roster installs eight. Both are
corrected in the rewrite.

**[N4] Accepted, fixed here.** The staging list at `docs/quickstart.md:194` gains
`NOTICE.md`, which the scaffold installs.

**[N5] Accepted.** The signals are rewritten as observations.

**[N6] Accepted.** A3 is re-argued on the ladder's self-locate purpose, with its real
cost.

**[N7] Leaves with the split.** The twin edit and the lockfile re-finalize are item 6's.
The documentation half edits nothing recorded in Cairn's own lockfile (73 entries; the
`_onboarding` scripts are there, no onboarding page is).

**[N8] Recorded** as the split-out proposal's starting point.

**[N9] Accepted.** The defect is internal self-contradiction, which needs no adopters to
be real. Revision 1 says so, and dispositions the friction audit's eight success
criteria.

**[T1]-[T3] Accepted.** The manifest smoke check carries the "no file added, removed or
renamed" condition; this revision uses standalone sections and names the sibling
proposal; "six lines later" is gone with the paragraph it was in, and the quickstart's
unsupported "Time: ~30 seconds" is removed.

## Revision 1 -- Claude -- 2026-10-01 -- the complete current contract

### Context

Cairn publishes a three-level adoption ladder. The level it recommends to its primary
audience -- Level 1, "the natural home for solo + one-agent adopters"
(`on-ramp/README.md:33`) -- is defined as **hand-copy the kernel** (`:24`). Nobody does
that, and nothing says how: 18 kernel files, with tokens to substitute, slot bodies to
fill and destinations documented nowhere. The Maintainer: "no one will ever actually
hand-copy Cairn, that's against the whole philosophy."

The scaffold already performs a Level 1 install. `docs/quickstart.md` runs it with the
`solo-greenfield` profile -- the kernel plus six default-on modules, exit 0 -- but
presents it only as a throwaway demonstration, then tells the reader that most teams
start at Level 1 (`:350-353`), the level they did not just do.

**This is an internal self-contradiction, and it needs no adopters to be real.**
`bootstrap/profiles/solo-greenfield.yml` recommends hand-copying in its header (`:22-24`)
and then hands you the scaffold command. The legacy recipe calls itself "a Level 1
hand-copy path" (`docs/solo-legacy-recipe.md:35`), while `on-ramp/README.md` sends solo
legacy adopters to it. Ten shipped files carry the hand-copy instruction. Cairn has no
external adopters, so this is not measured friction; it is a published model that
contradicts the tool beside it.

The model has also reached code. `level-1-to-2` fires on `dev/.cairn/cairn-lock.yml`
(`scripts/_onboarding/triggers.py:104`), which every scaffold install writes, so today
it fires for every quickstart follower. That defect is real and separate; this revision
splits it out (Scope delta).

The finding has been deferred four times: the friction audit named a consolidation
proposal nobody opened; `adopter-entry-doc-refresh` and `solo-legacy-adopter-path` each
did an adjacent piece and archived; the documentation note's F9 deferred to this
artifact before it existed.

### Proposal

**One installer. Keep three levels, and define the upper two by staffing.**

* **Level 0 -- read the doctrine.** Unchanged: nothing installed, no `dev/` tree.
* **Level 1 -- one Maintainer, one agent at a time.** Install with the scaffold, using
  the profile your project's axes give: `solo-greenfield` for a new project, the composed
  profile in `docs/solo-legacy-recipe.md` for an existing one. Reviews are fresh
  sessions of the one agent, or the Maintainer's own.
* **Level 2 -- concurrent work.** More than one agent working in the tree at once. The
  same scaffold; the profile's `agent_team` axis leaves `single`, and the scaffold adds
  the coordination and dual-review modules it already gates on that axis.

**Staffing is the one criterion.** The module roster follows the profile and is not a
level marker; where roster and staffing disagree, staffing governs. `team-gated` names a
directory of modules, not a level, so a solo legacy adopter running `legacy-agent` and
`testing-discipline` is Level 1. A second agent type is never required at either level;
it strengthens review where a team has one.

**The route is the same at both levels:** choose a profile (a preset, bootstrap-lite's
assessment, or `bootstrap/BOOTSTRAP.md` Act I), run the scaffold, then do the four steps
the installer prints for a real adoption (Act II-3 to II-6).

Concretely:

1. **`on-ramp/README.md`** -- the Level 1 and Level 2 sections, the choosing-a-level
   table and its solo-legacy paragraph, and the maturity ladder's rows, restated by
   staffing.
2. **`README.md`** -- the three-level block and the Level 1 bullet (`:266`).
3. **`docs/getting-started.md`** -- the ladder gloss (`:4`) and the level pointer
   (`:84-86`).
4. **`docs/quickstart.md`** -- stays a disposable shakedown: its teardown, its
   signature-check waiver for the throwaway clone, and its framing are unchanged. It
   gains a plain statement that the commands just run are a Level 1 install, and "What
   to do next" gives the real route: Steps 2-3 in your own repository from a release tag
   verified per `bootstrap/PROVENANCE.md`, then Act II-3 to II-6. Also: `NOTICE.md`
   joins the Step 3 staging list (`:194`); the level summary at `:350-353` is restated;
   the unsupported "Time: ~30 seconds" (`:296`) is removed. The phrases `**N** modules
   listed` and `**N unfilled block slots**` stay -- a frozen test reads them.
5. **`bootstrap/profiles/solo-greenfield.yml`** -- the header comment only: the
   hand-copy recommendation (`:22-24`) and the retired modules in the roster comment
   (`:17-19`).
6. **`docs/solo-legacy-recipe.md`** -- converted from "hand-copy what `--summary` lists"
   to "run the scaffold with this profile", with the roster corrected to the eight
   modules it installs today.
7. **Level references brought into line:** `bootstrap/BOOTSTRAP.md` (`:7`, `:231` -- the
   full walk serves either level); `bootstrap/prompts/bootstrap-lite.md` (the
   assessment-assisted route to either level); `templates/README.md` (`:82-86`);
   `templates/codebase-readiness-report.md` (`:345`); both example READMEs, which
   describe how each was actually built; and the three `templates/onboarding/*.md`
   presets, whose Level 1->2 prompt bodies are rewritten to state the staffing condition.
   **Their `### Row N --` headings are not renamed** -- the prompt renderer matches on
   them.
8. **A migration note in `on-ramp/README.md`.** A hand-copied tree is still Level 1.
   Without a lockfile it receives no upgrades and no maturity prompts. To bring it under
   the installer: run `python bootstrap/scaffold.py upgrade --target <repo>
   --init-lock`; fill the four placeholders it writes into `dev/.cairn/profile.yml`;
   re-run. Files whose tokens were filled by hand upgrade as review-only diffs. **Do not
   re-run the install with `--force`** -- it overwrites what you wrote.
   `bootstrap/UPGRADE.md` gains one line naming hand-copied trees in its migration
   section.

And `doctrine/onboarding.md`, below.

### Rationale

**Why not make hand-copying executable (A2).** It is available: the gate table says which
modules a profile selects, and `scaffold.py --manifest` lists 97 source-to-destination
rows. But the kernel alone is 18 files to place, with tokens to substitute and slots to
fill. A route nobody walks is not an adoption path, and it would commit Cairn to a second
installer maintained by hand beside one that already works.

**Why staffing.** It is the question an adopter most needs answered -- can I run this
alone, or do I need coordination? -- and the engine already answers it: `agent_team` is
the axis on which the scaffold adds the coordination and dual-review modules
(`bootstrap/_scaffold/config.py:1312-1331`). Defining the level by the same axis means
the ladder and the installer cannot disagree.

**Why keep the quickstart disposable.** Disposability is the page's structure, not an
accident: its teardown is an `rm -rf`, and it waives the release-signature check
*because* the target is thrown away (`docs/quickstart.md:61-67`). Sanctioning the page
itself for real repositories would carry both into one. Pointing from it to the real
route keeps the trust step mandatory where it matters, and leaves the installer's own
"throwaway repo" line true.

### Alternatives considered

**A1 -- Do nothing.** The contradiction stays across ten shipped files, and F9 stays
blocked on it. Rejected: a deferral that outlives its owner is an accident, not a
decision.

**A2 -- Make hand-copy executable.** Rejected above.

**A3 -- Collapse to two levels** (read the doctrine / run the scaffold). No engine code
reads a level -- the roster comes from the preset and six axes -- so the cost is not a
wider roster. The cost is that the ladder is a self-locate aid ("can I run this
alone?"), and the maturity triggers lose the addressing scheme their prompts are written
in. Rejected for those reasons.

**A4 -- Rename the levels.** Rejected. The substance is the definition; a rename adds a
second vocabulary break across the same files for no gain in meaning.

**A5 -- Settle item 6 here.** Rejected in favour of the split: it costs a Maintainer-only
re-anchor and an open design question that nothing in this change depends on.

### Documentation / doctrine surface

Every change lands in the entry and descriptive layers listed above, plus one doctrine
file. **`doctrine/onboarding.md`**: its two maturity-signal definitions (`:69-73`)
describe a mechanism the code does not check. They are reconciled with shipped
behaviour -- `level-0-to-1` fires on one archived proposal; `level-1-to-2` fires on the
lockfile, which every scaffold install writes, so it does not yet distinguish the levels.
No other trigger doctrine changes.

**Doctrine-change rate-limit: applies, and rests on recurrence.** The finding was
deferred four times across four artifacts (Context). That is a pattern, not a single
incident.

### Evidence / verification plan

| Claim | How it was established (2026-10-01 unless stated) |
|---|---|
| Level 1 is recommended to the primary audience, defined as hand-copy | `on-ramp/README.md:24`, `:33` |
| Hand-copy is not executable as written | 18 kernel files under `templates/core/`; the review counted the tokens, slots and undocumented destinations (2026-08-31) |
| The scaffold already performs a Level 1 install | `solo-greenfield` into a fresh repo: exit 0, six modules, 140 lines of output, 22 slots |
| The legacy route works through the scaffold | the recipe's profile into a scratch repo with its own `README.md` and `CHANGELOG.md`: exit 0, lockfile written, both files unchanged, eight modules |
| The hand-copy migration works | `upgrade --init-lock` on a scratch hand-copied tree: exit 2 with four placeholders; filled and re-run: exit 0, lockfile written |
| `doctrine/` names the ladder | `doctrine/onboarding.md:69-73` |
| `level-1-to-2` fires for every scaffold install | `scripts/_onboarding/triggers.py:104`; every install writes the lockfile |
| No touched file is frozen or lockfile-recorded | `frozen_files` (183 entries) and `dev/.cairn/cairn-lock.yml` (73 entries), each checked with a control that matched |

#### Acceptance criteria

* **Completeness.** `grep -rlE "hand-copy([^i]|$)" --exclude-dir=dev --exclude-dir=.git
  --exclude-dir=.claude --exclude=CHANGELOG.md .` returns these ten files before the
  rewrite -- its positive control -- and **nothing** after: `README.md`,
  `on-ramp/README.md`, `docs/getting-started.md`, `docs/quickstart.md`,
  `docs/solo-legacy-recipe.md`, `doctrine/onboarding.md`,
  `bootstrap/profiles/solo-greenfield.yml`, `templates/README.md`,
  `templates/codebase-readiness-report.md`, `templates/onboarding/high-rigor-legacy.md`.
  "Hand-copied" remains only where it describes an existing tree -- the migration note
  and the two example READMEs -- and in three tests that use it in an unrelated sense.
* **Doctrine reconciliation.** Each maturity-signal sentence in `doctrine/onboarding.md`
  names the condition `evaluate_maturity_triggers` evaluates.
* **No frozen or lockfile-recorded file changes.** Before commit, no path in the change
  set is a key of `frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json`, or a
  `dst` in `dev/.cairn/cairn-lock.yml`.
* **The published manifest does not move.** `scaffold.py --manifest` is byte-identical
  before and after, provided no file is added, removed or renamed.

#### Tests and gates

The change is prose-only, so the suite does not run (`AGENTS.md` > Verification
boundaries). What does run:

* the tests that read touched files -- `bootstrap/tests/test_quickstart_sequence.py`
  (reads `docs/quickstart.md`; frozen, not edited) and
  `bootstrap/tests/test_active_surfacing_render.py` (reads the onboarding presets) --
  plus any other the plan's search for readers of the touched files finds;
* `scripts/claim_check.py`, `scripts/link_check.py`, `scripts/check_cairn.py` and the
  neutrality gate over every touched file;
* a scaffold run of `solo-greenfield` and of the legacy recipe's profile into temporary
  targets, confirming both routes the rewrite points at still complete.

#### Security preflight

N/A: no trust boundary added, moved, or widened. The one trust step on these pages --
release-tag verification -- becomes mandatory on the real-adoption route and is left as
it is on the disposable one.

### Signals the change is wrong

* **A Level 1 adopter cannot tell which profile to use.** The first question after the
  rewrite is "`solo-greenfield` or the recipe?". The fix is a row in the choosing-a-level
  table, not a new level.
* **The staffing criterion misclassifies a real team** -- a project with concurrent
  agents reads itself as Level 1, or a solo project reads itself into Level 2 from its
  module list. Then the criterion is not stated where adopters look.
* **The completeness grep needs an exception this revision did not foresee.** That is a
  retained definition the rewrite missed, not a deliberate one.
* **The early Level 1->2 prompt confuses a Level 1 adopter** before the split-out
  proposal lands. Then the rewritten body is not conditional enough: fix the body, not
  the trigger.

### Scope delta

**Scope delta**: degraded -- one outcome moves to its own proposal; nothing is lost.

* **Item 6 -- a promotion signal that survives a scaffolded Level 1**, with the
  `level-1-deepen` / `level-2-deepen` classifier it gates, the negative trigger invariant
  ([R7]), the seven-file gate-manifest re-anchor ([R4]), the lockfile re-finalize and the
  twin edge case ([N7]). **disposition**: defer -- to a new proposal, starting from
  the observation in [N8] that `second-agent-type` already detects the staffing
  criterion. Specifying it here
  was rejected because it brings a Maintainer-only ceremony this change otherwise
  avoids, and nothing here depends on it.

Carried from the opened version, now with a destination:

* **F8 -- the post-install report lists slots for modules the profile did not select**
  (22 slots on a six-module install). **disposition**: defer -- fixing it changes the
  install reporting path in `bootstrap/_scaffold/`.

**Both defers need a row on `dev/PLANNING.md` and the Maintainer's authorization quoted
verbatim** (`dev/plans/_template.md`). They are presented as one batch for the Decision;
the deposit is its own commit after it.

The friction audit's eight success criteria
(`dev/strategy/archive/2026-06-12-claude-adopter-friction-audit.md:426-440`):

* **Met here:** one obvious trial and one obvious real next step; no undefined hand-copy
  operation on the solo route; one installer for every non-zero level.
* **Met for the quickstart:** the unsupported timing claim is removed.
* **Deferred:** a post-install report that asks only for live work (F8, above).
* **Not addressed, and never in this proposal's scope:** every published command under a
  governing test; a release gate on stale first-contact docs; a canary adopter (none
  exist).

### Assurance path

**Assurance path**: high-assurance -- the change edits `doctrine/onboarding.md`, and
anything under `doctrine/` is a mandatory trigger.

### Withdrawn / superseded commitments

* Level 1 as "no team-gated modules" -- superseded by the staffing criterion ([R1]).
* "the installed module roster does" distinguish the levels (`:125`), and item 6 -- moved
  to the split-out proposal ([R1], Scope delta).
* `docs/solo-legacy-recipe.md` as "the working precedent", and "much smaller than it was
  in June" -- withdrawn; the recipe was a hand-copy path ([R2]).
* Item 4's "may be run against a real repository" -- superseded: the quickstart stays
  disposable and points to the real route ([R3]).
* "the gate manifest ... unchanged" as a claim about the whole change -- withdrawn; it
  holds for the documentation half and is now an acceptance criterion ([R4]).
* The Evidence row "`doctrine/` does not name the ladder" -- withdrawn ([R6]).
* Rate-limit ground #2 -- withdrawn ([R6]).
* The "shipped executable behaviour changes" assurance ground -- withdrawn ([N2]).
* Item 5 across all three profiles -- narrowed to `solo-greenfield.yml` ([N1]).
* The figures 114 manifest rows, 161 lines, 24 slots, and seven default-on modules --
  superseded by today's measurements ([N3]).
* "Nineteen shipped surfaces" -- superseded by the ten enumerated files and the
  surfaces in items 1-8.
* A4 "deferred, not rejected" -- now rejected ([R9]).
* All four original Signals -- replaced ([N5]).
* F8 "accept -- carried as a named follow-up" -- now `defer`, with a board row.
* The plan-review justification "a plan is mechanical translation across a known
  surface list" -- the tier stands; the justification now rests on the split ([R9]).
* Header: `Date opened` renamed `Opened`; `Review` added; `Touches`, `Assurance path`,
  `Related` and `Plan review` restated for this revision.

## Maintainer direction -- Anthony Kendall (Maintainer) -- 2026-10-01

The Maintainer's words, quoted **verbatim and visually isolated**:

> "I'm honestly wondering whether we should make such a distinction. It's so
> trivially easy to add a second agent instance--and this happens through
> delegation, that we should eliminate Level 1. What do you think?"

> "Yes, go ahead and revise the proposal as you've described. Thanks!"

*Scribe's note, separate from the quoted words:* "as you've described" refers to
the author's reply between the two messages: adopt alternative A3 (retire the
Level 1 / Level 2 distinction), return the proposal to `revising`, and write
Revision 2. Status moves `awaiting-decision` -> `revising`. Scribed by Claude
(claude-opus-5-5) on the Maintainer's instruction.
