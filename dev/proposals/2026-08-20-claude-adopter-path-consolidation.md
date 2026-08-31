# One installer: make the adoption ladder measure obligation, not mechanism

**Author**: Claude (Strategy)
**Model**: Opus 5
**Date opened**: 2026-08-20
**Status**: revising
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
**Related**: `dev/strategy/archive/2026-06-12-claude-adopter-friction-audit.md` (merged 2026-08-26 into `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md`) — this is
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
