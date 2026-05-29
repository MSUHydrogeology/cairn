<!-- claim-check-allow: scripts/onboarding_activate.py, dev/.cairn/onboarding-activated.jsonl, dev/modules/onboarding/ -->
<!-- The scripts/ + dev/ paths refer to ADOPTER install destinations.
     From Cairn's own checkout these paths do not resolve (the source
     of truth lives at templates/modules/default-on/onboarding_activate.py
     + templates/onboarding/<preset>.md).  Exempted so the adopter-
     facing cite stays correct -- parallel to the fold-back.md pattern. -->

# Progressive onboarding -- the apparatus growing with the team

Cairn's static entry-surface artifacts (`docs/quickstart.md`,
`templates/codebase-readiness-report.md`, the bootstrap profile
examples) answer "how do I start?" Cairn shipped them with the
adopter-friction package. They stop at the install.

**Progressive onboarding** is the post-install counterpart. It
answers the sequence of "what's next?" questions an adopter faces
once they have Cairn in their tree:

* When should I open my first proposal?  How?
* When does signing the collaboration agreement matter?
* When am I ready to spin up a second agent type?
* When my deployment has a foldback candidate, how do I file it
  upstream?

The mechanism: **`dev/PLANNING.md` carries preset-keyed
onboarding tasks that activate as the adopter's relationship with
Cairn deepens** -- maturity-ladder transitions + concrete action
signals fire tasks into the backlog; important transitions get
terminal-output prompts at the next goodnight.

## The four components

### Component 1 -- Preset-keyed PLANNING.md slot

The PLANNING.md template (`templates/core/dev/PLANNING.md`)
carries a new `<!-- cairn:slot onboarding-tasks -->` block
between `## Where the project stands` and `## Queued`. The
bootstrap fills this slot at install time from a profile preset:

* `solo-greenfield` -- the lightest profile (one human +
  one AI agent on a new codebase).
* `collaborative-team` -- 2-4 humans + 1-2 agent types on a
  greenfield or near-greenfield codebase.
* `high-rigor-legacy` -- 5+ humans + multi-agent + legacy +
  multi-language + security boundaries.

The three preset onboarding files live at
`templates/onboarding/<preset>.md`. Each carries seed tasks +
deferred tasks + active-surfacing prompt content; the scaffold
**inlines only the seed tasks** into the PLANNING slot (plus a
`<!-- preset: <name> -->` metadata comment); the full source file
installs to `<target>/dev/modules/onboarding/<preset>.md` for the
activation helper to read at goodnight.

### Component 2 -- The trigger system

Two trigger kinds drive activation: **maturity-ladder
transitions** + **concrete action signals**.

**Maturity-ladder triggers** observe the existing on-ramp
doctrine (`on-ramp/README.md`):

* `level-0-to-1` -- `dev/proposals/_template.md` is present
  (the canonical Level 1 signal: the adopter graduated from
  "read the doctrine" to "hand-copy the kernel").
* `level-1-to-2` -- `dev/cairn-lock.yml` is present (the
  canonical Level 2 signal: the adopter ran the full bootstrap).
* `level-1-deepen` / `level-2-deepen` -- in-level action-count
  thresholds (e.g., five archived proposals + three archived
  plans for `level-1-deepen`; the thresholds are concrete +
  named in the activation helper's evaluator).

**Action triggers** observe the adopter's actual work:

* `first-proposal-opened` -- a non-template file in
  `dev/proposals/` exists.
* `first-proposal-archived` -- a file in
  `dev/proposals/archive/` exists.
* `first-plan-opened` / `first-plan-archived` -- parallel for
  plans.
* `first-changelog-entry` -- `CHANGELOG.md > Unreleased` is
  non-empty (any text between the heading and the next
  release header).
* `second-agent-type` -- the team-roster slot in
  `dev/collaboration_agreement.md` lists at least two distinct
  agent identifiers. **Explicit-state observation** (the
  Maintainer's roster fill is the signal), NOT git-trailer
  archaeology -- per the round-1 External-Review disposition.
* `first-cross-type-review` -- a proposal or plan's `## Review`
  section is attributed to an agent type different from the
  file's author. Determined by **file-content scan** of
  `dev/proposals/**/*.md` + `dev/plans/**/*.md` -- a flavor of
  explicit-state observation (the file content IS the explicit
  state; not git archaeology of trailers).
* `first-foldback-candidate` -- the fold-back ledger
  (`dev/.cairn/cairn_foldback.md`) has at least one open
  `candidate`-status row.
* `collab-agreement-signing` -- the team-roster slot in
  `dev/collaboration_agreement.md` is unfilled (template default
  text OR empty between the slot tags) AND
  `first-proposal-archived` has previously fired. Once the
  roster is filled, the trigger's activation is recorded in
  `activated.jsonl`, so subsequent partial edits to the roster
  do not re-fire the prompt.

### Component 3 -- Hybrid surfacing (passive + active)

**Passive surfacing** (the default): when a trigger fires, the
deferred onboarding task's body is **inlined into PLANNING's
`onboarding-tasks` slot**. The adopter discovers it at the next
session-start read. Low friction; matches how PLANNING already
works for ordinary roadmap items.

**Active surfacing** (for important transitions): a small named
set of transitions also gets **terminal-output prompts** at the
goodnight activation run. The four named rows:

1. **Collab-agreement signing** -- fires on the
   `collab-agreement-signing` trigger above.
2. **Level 1 → 2 graduation** -- fires on `level-1-to-2`.
3. **Second-agent-type spin-up** -- fires on `second-agent-type`.
4. **Upstream PR/issue walkthrough** -- fires on
   `first-foldback-candidate`.

Each row carries **per-preset prompt content** authored in the
preset file's active-surfacing-prompt-content blocks. The
solo-greenfield variant talks to one human + one agent; the
collaborative-team variant invokes multi-party negotiation; the
high-rigor-legacy variant assumes pre-existing maintainer
authority + security-review module gates.

### Component 4 -- Tour content

Two tour docs ship as part of progressive onboarding:

* `docs/dev-tour.md` -- the `dev/` subdirectory taxonomy + a
  worked example. **Accessible from day one** via every preset's
  seed task list (no trigger gating: tour docs are consumed
  BEFORE commitment, not after, per the post-revision Internal
  Review disposition).
* `docs/agent-team-onboarding.md` -- the second-agent-type
  spin-up checklist. Activated by the `second-agent-type`
  trigger (solo-greenfield) OR referenced from the
  collaborative-team + high-rigor-legacy preset's seed task
  lists (those presets expect multi-agent from day one).

The remaining tour surfaces -- the collaboration-agreement
signing dialogue (Component 3, Row 1) + the upstream PR/issue
walkthrough (Row 4) -- reuse existing mechanisms (the
collab-agreement slot fill is just the slot-fill protocol; the
foldback walkthrough invokes the existing
`doctrine/fold-back.md > Active surfacing` 6-step protocol).

## State-file schema + edit cadence

The activation helper records each activation as one line in
`dev/.cairn/onboarding-activated.jsonl`. The file is **tracked**
(parallel to `dev/intents.jsonl`'s atomic-append precedent):
shared across team members through git; edited at the goodnight
serialization point only. The scaffold seeds it as empty at
install time (header comment only) so no lazy-mkdir is required
at first helper run.

**Schema** (one JSON object per line; sorted keys):

```jsonl
{"activated-at":"2026-05-29T11:00:00Z","by-agent":"claude-abc123","source-preset":"solo-greenfield","task-id":"dev-tour-walkthrough","trigger":"first-proposal-archived"}
```

* `task-id` -- the stable id from the source file's
  `[trigger: X; id: Y]` header. Primary key for idempotency.
* `activated-at` -- ISO-8601 UTC timestamp with second
  precision.
* `by-agent` -- the identifier of the agent (or runner)
  performing the activation. Reads `CAIRN_AGENT_ID` env var
  when set; otherwise `unknown-agent`.
* `source-preset` -- which preset the task originated from.
* `trigger` -- which trigger fired the activation.

**Idempotency** (eventual no-op contract; calibrated by the
dogfood pilots): a task-id already in the log does not re-fire,
and an active-surfacing row already emitted (`active-surface:<row>`
in the log) does not re-emit. The log is the authoritative dedup
key. **The cap is per-invocation**: each helper run drains at
most one active-surfacing prompt from the priority queue, so
consecutive runs against the same deployment state can each
emit one prompt (next-priority) until the queue is drained,
after which subsequent runs are strict no-ops. The dogfood
pilots all confirmed this "eventual no-op" semantics: 3 runs
drained the queue for solo-greenfield / collaborative-team /
high-rigor-legacy fixtures; the 4th run was a strict no-op.
For a goodnight owner who fires the helper once per goodnight
(the recommended pattern), each goodnight emits one prompt at
most. The helper's `dry-run` mode shows what would be appended
without writing.

**Held + completed are derived** (not persisted):

* **Held tasks** = source-file deferred task ids - log
  activations. Re-computed each goodnight from the source file +
  the log.
* **Completed tasks** = log activations whose body no longer
  appears in PLANNING's slot. Inferred from the standard
  `doctrine/lifecycle.md` "remove when complete" pattern; an
  adopter who deletes an activated task's body from PLANNING
  signals completion implicitly.

## UX caps + priority order

The activation helper enforces caps so a goodnight returning the
next morning doesn't surface a wall of text:

* **≤1 active-surfacing prompt per goodnight.** Multiple fires
  in one cycle defer to the next goodnight, in priority order.
* **≤3 newly-inserted onboarding tasks per goodnight.** Overflow
  defers identically.
* **Priority order** (highest first):
  1. `collab-agreement-signing`
  2. Level 1 → 2 graduation
  3. `second-agent-type` spin-up
  4. Upstream PR/issue walkthrough

The priority order is **v1-fixed**; adopter-tunable priority
becomes a v1.x candidate (see "Capability-pull follow-ups" below).

## Goodnight invocation

The standing pattern (per `doctrine/session-routines.md`):

```bash
python scripts/onboarding_activate.py            # default: scan + activate
python scripts/onboarding_activate.py --dry-run  # show plan, no writes
```

The full-handoff owner runs the helper as part of the
**foldback-capture step** at goodnight. The two steps are paired
deliberately -- both are "scan the day's state for things that
need recording / surfacing"; both close out cleanly with an
"empty scan is success" posture.

Future `cairn-update` mini-command may fold this into a single
goodnight wrapper (capability-pull follow-up).

## Existing-adopter manual opt-in path

An adopter whose tree was scaffolded BEFORE this update can opt
in to progressive onboarding through a **documented manual
recipe**:

1. **Paste the slot block** into the adopter's existing
   `dev/PLANNING.md`. The block:

       ## Onboarding

       <!-- cairn:slot onboarding-tasks -->
       <!-- cairn:end onboarding-tasks -->

   Place it between `## Where the project stands` and
   `## Queued` (the canonical position) -- or wherever the
   adopter's tree shape supports it.

2. **Run the activation helper's `--seed` mode** (lands in
   plan Chunk P1.11):

       python scripts/onboarding_activate.py --seed --preset <name>

   The helper writes the `<!-- preset: <name> -->` metadata
   comment + inlines the preset's seed tasks into the slot;
   it also installs the full source file at
   `<target>/dev/modules/onboarding/<name>.md` (the
   authoritative reference the helper reads at goodnight).

3. **Verify the seed tasks appear** in PLANNING.md and that
   `dev/.cairn/onboarding-activated.jsonl` exists (the
   scaffold seeds it empty; `--seed` mode does the same if
   the file is absent).

4. **From the next goodnight onward**, run
   `python scripts/onboarding_activate.py` as part of the
   standing routine; activation proceeds normally.

A `cairn-update --add-onboarding` automation of this recipe
becomes a v1.x candidate when an adopter asks for it (see
below).

## Capability-pull follow-ups (v1.x)

V1 ships at full L3 scope -- three presets, full trigger
matrix, all four active-surfacing rows, both tour docs. **V1.x
opens only when a real adopter hits a v1 gap**, not on a
schedule. The named candidate gaps:

* **Adopter-extensible custom task lists** -- v1.x if an
  adopter wants lab-specific onboarding content. (Trust-
  boundary design required: downstream user-supplied task
  content has no upstream review.)
* **Tunable priority order** -- v1.x if an adopter's scenario
  inverts the v1 default (e.g., a research consortium whose
  primary need is upstream-PR-walkthrough first).
* **Additional preset profiles** -- v1.x if an adopter's
  shape doesn't fit one of the three named presets.
* **`cairn-update --add-onboarding` mini-command** -- v1.x
  when an existing-adopter opts in via the manual path enough
  that the manual friction is worth automating.

V1 stays at L3 indefinitely until a v1.x candidate's gap
becomes load-bearing. Evidence-gated, not schedule-gated.

## Dispatching an agent session

The apparatus assumes you can hand a *fresh* agent session the context it
needs to act in the right frame. That hand-off is vendor-neutral doctrine:

* **Name the role first.** Open the session by stating its role (Strategy, a
  Domain, Legacy, a Reviewer tier -- see `doctrine/roles.md` > "When to
  dispatch which role"). The role determines the artifact; an unframed
  session defaults to whatever the prompt's verb implies, which is often the
  wrong frame.
* **Hand it the orientation, not the whole history.** Point the session at
  the `dev/` tree (the deliberation surfaces it will read and write) and at
  the one artifact this task turns on -- the proposal it implements, the plan
  it reviews, the issue it diagnoses -- rather than replaying the prior
  session. The durable record *is* the context; that is what it is for.
* **State the task and its boundary.** What this session should produce, and
  explicitly what it should *not* touch (the scope fence). A session given a
  clear "not this pass" stays bounded.

**Vendor boundary (load-bearing).** *How* you literally start a session -- the
command, the IDE action, the API call for a given agent harness -- is **not**
Cairn doctrine and is deliberately absent here: it is per-vendor and changes
faster than the methodology. Those mechanics live in your **vendor wrapper**
(the agent-specific file that imports the kernel `AGENTS.md` -- a
`CLAUDE.md`-style doc), which is where a harness-specific habit belongs. Cairn
stays vendor-neutral; the wrapper carries the spawn recipe.

## Cross-references

* `doctrine/lifecycle.md` -- the proposal-lifecycle the seed
  tasks introduce.
* `doctrine/roles.md` -- the role roster + the "When to dispatch which role"
  heuristics a fresh session is framed by.
* `doctrine/coordination.md` -- the work-intent mechanism the
  multi-agent presets exercise from day one.
* `doctrine/fold-back.md` -- the active-surfacing 6-step
  protocol Component 3 Row 4 invokes.
* `doctrine/session-routines.md` -- the goodnight step the
  activation helper runs at.
* `docs/tool-usage.md` -- worked invocations of the shipped tools
  (`claim_check`, `intent.py`, `lifecycle_metrics`, `link_check`).
* `on-ramp/README.md` -- the maturity ladder the
  maturity-ladder triggers observe.
