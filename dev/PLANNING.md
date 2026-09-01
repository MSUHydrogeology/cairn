<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/lifecycle.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Cairn — development roadmap

`PLANNING.md` is the **roadmap board**: a current-state index of
what is queued and in flight. It is **not** a historical log —
completed items are *removed* from the board, not crossed off or
struck through, once their lasting truth has migrated to the
durable record (archived proposals and plans, implementing
commits, the changelog). See `doctrine/lifecycle.md` > "The
roadmap is a current-state index, not a historical log" for the
load-bearing reasoning.

`PLANNING.md` is a **shared communication file**: edited only at
defined serialization points — a lifecycle archive, the goodnight
routine, or explicit maintainer instruction — and referring to
proposals and plans by **filename stem**, not path link, so an
archive-move needs no edit here. The required-signal-read
discipline on shared communication files applies
(`doctrine/coordination.md` > "Required signal+read for
coordination-surface files").

## Where the project stands

<!-- cairn:slot project-status -->
**Released at v0.3.0 (2026-06-12).** Phases 1–4 are complete: doctrine
extraction, the forkable templates, the bootstrap procedure + scaffold +
the engine test suite, and two case studies (modflow_tools — the
reference instance — and LHM). The methodology is in active use in those
two real projects. **Phase 5 — launch and governance — is in progress;**
the R-H third-party correctness probe (plan chunk 5.3) is still
outstanding, awaiting a consenting third-party scientific repository that
did not contribute to the doctrine.

**Cairn now self-hosts (adopted 2026-06-12).** Development was previously
tracked in the modflow_tools repository's `dev/plans/` lifecycle; this
`dev/` tree is Cairn running its own methodology on itself, so future
development — and Issues filed via GitHub — happens here. The accepted
adoption profile is recorded at `dev/.cairn/profile.yml`
(`collaborative-team` preset, human-team overridden to solo; the
deliberation is at `dev/strategy/archive/2026-07-11-claude-cairn-adoption-record.md`,
a 2026-07-11 reconstruction, not contemporaneous).

**Where it is headed.** The broad-look pass is **done** (2026-07-08, note
`2026-07-08-claude-broad-look-skeptical-review`): ~100 verified findings in
eight themes and a three-phase tighten-up. Phase A of that tighten-up has
largely shipped — licensing compliance, first-session survivability, record
corrections, lockfile provenance, the interpreter trust root, and
review-record integrity are all implemented and archived. **Two standing
directions now order the remaining work** (Maintainer, 2026-07-22):
*postdoc-first* — order by whether it affects the first external adopter's
first two weeks; and *fix defects, build nothing new* — any new tool or
mechanism needs an explicit go-ahead, however well it reviews.

**The subtraction sweep is done and archived (2026-08-28).** ~55,000 lines of
Cairn's own process machinery removed, measured per file rather than headlined;
the record is
[`plans/archive/subtraction-sweep.md`](plans/archive/subtraction-sweep.md) and
what it cost against what it was estimated to cost migrated to
[`strategy/2026-08-21-claude-nimbleness-recovery.md`](strategy/2026-08-21-claude-nimbleness-recovery.md).
The gate anchor moved `5f99273 -> bd66a70` after eight days stopped, and both
sister repositories consumed the change — `lhm` merged, `modflow_tools` still on
its migration branch.

**Three defects surfaced during that work that nobody had filed**, each closed
with a control test: the upgrade engine never advanced `base_hash` for verbatim
records, so adopters silently froze on old versions of every shipped script and
were told they had forked files they never touched; the AST attestation's
known-new digest check ran only on its repair path, so an injected statement in
the containment guard passed the gate; and Cairn was still *shipping* prose about
machinery it had removed, which both sisters inherited through the upgrade.

**Next is the `repin` tool** — the successor to the blocked digest corrector,
designed in
[`strategy/2026-08-28-claude-repin-revitalization.md`](strategy/2026-08-28-claude-repin-revitalization.md)
and routed through the deliberate lane, because it is a trust-ceremony surface
and the External floor belongs at the proposal where the design is still
movable. Until it lands, corrections continue by hand.

*(Refreshed at each goodnight scrub.)*
<!-- cairn:end project-status -->

## Onboarding

Progressive onboarding tasks live here. The bootstrap fills this
section from the chosen profile preset (`solo-greenfield`,
`collaborative-team`, or `high-rigor-legacy`) with the preset's
day-one seed tasks plus a preset-metadata comment that the
goodnight activation helper reads to discover the preset's
deferred tasks (held in `dev/modules/onboarding/`'s installed
preset file until their named trigger fires). The progressive-
onboarding doctrine is the source of the mechanism; this section
is its surface in PLANNING.

<!-- cairn:slot onboarding-tasks -->
<!-- preset: collaborative-team -->

* [seed; id: try-session-start-skill]
  Try the `session-start` skill (`/session-start`): run
  `python tools/session.py session-start` to orient at the top of a
  session. The lifecycle routines are now invokable skills installed under
  `.agents/skills/`; the canonical doctrine is `doctrine/session-routines.md`.
* [seed; id: read-lifecycle-doctrine]
  Read `doctrine/lifecycle.md` together as a team -- the
  proposal -> review -> decision -> archive shape is the load-
  bearing convention every later coordination behavior assumes.
* [seed; id: read-coordination-doctrine]
  Read `doctrine/coordination.md`. The work-intent mechanism is
  what prevents collision between concurrent agents in the same
  tree; multi-agent teams need this from day one, not as a
  later upgrade.
* [seed; id: install-work-intent-hooks]
  Install the work-intent git hooks, or record that you are skipping
  them. This preset is concurrent, so the scaffold *recommended* the
  hooks at install time but does **not** install them for you (it
  never mutates `.git/hooks`). Run `python tools/intent.py
  install-hook` + `install-precommit`, then `hooks-status` to confirm.
  Without them, `dev/intents.jsonl` stays empty and the coordination
  signal never fires. To opt out (now or later), re-run either command
  with `--uninstall`; note the choice here so the team's preference is
  on the record.
* [seed; id: read-dual-review-module]
  Read `dev/modules/dual-review.md`. The collaborative-team
  preset installs the dual-review module by default; the
  External-tier review now has structural independence from
  the start.
* [seed; id: walk-dev-tour]
  Walk the `dev/`-tree tour at `dev/modules/onboarding/dev-tour.md`
  together. It carries one paragraph per `dev/` subdirectory plus a
  worked example showing one change through the full lifecycle.
* [seed; id: agent-team-onboarding]
  Walk `dev/modules/onboarding/agent-team-onboarding.md` to align on capability
  tiers + the `Co-Authored-By:` trailer convention for each
  agent in the roster. Multi-agent is this preset's defining
  shape; the agent-team-onboarding doc carries the
  baseline configuration the team uses.
* [seed; id: sign-collab-agreement-day-one]
  Convene the team + agents in your first session and fill the
  `team-roster` slot in `dev/collaboration_agreement.md`. The
  roster is what makes Dual-Review's External tier
  structurally meaningful; teams without an explicit roster
  fall back to fresh-session same-vendor review, which the
  collaborative-team profile is sized past.
<!-- cairn:end onboarding-tasks -->

## Queued

The forward-looking board: substantive work that is accepted or
anticipated but not yet in flight. When a queued item grows into
multi-step work, open a plan under `plans/` and replace the entry
with the plan's filename stem.

* **Re-anchor the gate manifest — 10 frozen files.** Deposited 2026-09-01 at
  the archive of `plans/archive/portable-sweeps-cannot-run.md` and
  `plans/archive/scanner-claim-scope.md`. The frozen files changed by those two
  implementations plus the active-surfacing prompt fix are stale against
  `bootstrap/tests/fixtures/gate_manifest.json`. Maintainer authorization for
  the deferral, quoted verbatim:

  > "If we don't need to re-anchor now, let's not. We've got a couple of big
  > new features coming, one of which will be a better automation."

  **This will not announce itself.** `test_gate_manifest.py` verifies a freshly
  produced manifest and never diffs the committed fixture, so the suite stays
  green while the trust root sits stale — which is why the deferral is on this
  board and not only in the archived plans that declared it. The procedure is
  `bootstrap/REANCHOR_RUNBOOK.md`, and it is Maintainer-only and supervised:
  an implementing agent must not perform it.


**Nineteen rows left this block on 2026-08-27**, at the sweep's C7 bankruptcy
pass, taking it from 852 lines to 260.

* **Twelve were security-cluster rows** and folded into
  [`strategy/2026-08-05-codex-security-strategy.md`](strategy/2026-08-05-codex-security-strategy.md)'s
  Live residual register. Eleven carried content that moved; the twelfth
  (`[TRU-7]`, the unpublished gate anchor) was already there in full and was
  a duplicate. **The board no longer owns security triggers** — a residual's
  revival condition should not sit in a task board that has no task for it.
* **Seven were dead or already closed** — six lost their subject to the sweep
  (the metrics extractor, the divergent-activation-marker check, the identity
  comparator, the five plan-review basis fields, transition-lint, the
  review-allocation pilot) and one had been marked resolved since 2026-08-20.
  Each is on the dead list in
  [`plans/archive/subtraction-sweep.md`](plans/archive/subtraction-sweep.md) with the
  measurement that showed it gone.

**What remains here is the untriaged product, docs and process backlog**, which
the routing map sends to forge issues row by row rather than to a bulk decline.

* **[DOC] Candidate: a withdrawal ledger records the correction, not the
  reasoning — so a later agent can re-derive the original error**
  *(filed 2026-08-20, from the adopter-issue proposal set)* — `scanner-claim-scope`
  declared "no Security Review trigger"; a blocking review refuted it (the
  trigger is **surface-based**, and `dev/proposals/_template.md:76-78` names the
  content scanner); the contract was corrected in Revision 2 and carried through
  Revision 4. A later decision-support pass then independently re-derived the
  **boundary** argument — *"strictly modifies report formatting"* — concluded no
  trigger, and that conclusion propagated into the scribed Decision summary,
  which now contradicts the contract it accepted.

  **What travelled was the corrected value; what did not travel was the
  reasoning that produced it.** The withdrawal ledger records *that* a claim was
  withdrawn and why the author changed it — it does not reach a reader who never
  opens it and re-derives the claim from scratch. The failure is cheap to miss
  precisely because the artifact is *correct*: only the summary is wrong, and
  the summary is what gets skimmed.

  **A second candidate from the same set, filed together because they may be one
  rule:** three invariants this session were **satisfied by their own wording
  rather than by the hazard** — an identity over an empty set, a claim scoped to
  "any path `read_report` refused" on a path that never called it, and an oracle
  that projected away the field it guarded. Each was caught only when someone
  ran the falsifying mutation. The general form — *state an invariant over the
  whole space it claims to cover, and run its falsifying mutation before
  trusting it* — may be the same rule as `AGENTS.md` > "Confirm the instrument
  before trusting an absence", one level up.

  **Neither is proposed as doctrine.** `AGENTS.md` gained a related rule on
  2026-08-19 from the same agent, and a second and third generalised from that
  agent's own recurrence on consecutive days is the churn the rate-limit gate
  exists to prevent. Filed for a goodnight-time synthesis or a Maintainer call,
  with the evidence attached so the gate can be cleared honestly if a third
  party sees the pattern independently.

* **Agent-facing discipline does not survive delegation** *(observed 2026-08-13
  during `review-efficient-lifecycle` Chunk H1; raised by the Maintainer)* — every
  operational rule in `AGENTS.md` is written for *the* agent, in the singular. It
  binds the agent that reads it. It says nothing about the agents that agent
  spawns, and a subagent does not read `AGENTS.md` unless its brief carries the
  rule down. Two independent instances landed the same day, which is what makes
  this a pattern rather than one session's sloppiness:

  **(a) The verification-boundary budget, measured.** *Verification boundaries*
  opens with *"do not pay for the same broad run at every one"*: Boundary A is
  scoped to the plan's reviewed mapping, B is the one stable run, and C states
  outright that *"copying Boundary B's broad command is not a falsification
  ledger."* `review-efficient-lifecycle` budgets **two** full suites (B1, and B2
  after the ceremony). The chunk spent **13** — roughly 2¼ hours of compute.
  **11 of the 13 were delegated agents**, each independently reaching for
  `pytest bootstrap/tests` because that is the obvious way to answer "did this
  break anything," with nothing in their brief saying a budget existed or that a
  six-file scoped mapping (~70s) was available. The implementing agent held the
  mapping and did not pass it down.

  **(b) Work-intent claims are advisory, not locking.** Two artifacts moved under
  a claim this session was holding (`e02f6a8`, `618ec47`), one discarding an
  uncommitted edit. Correct behaviour on every side — a claim is a coordination
  *signal* — but an agent that reads "claim before editing" without also reading
  "and re-check the blob, because the claim guarantees nothing" will lose work.
  The migration refused both rows, which is the designed outcome; the cost was
  the pass, not the data.

  **The shape both share.** A rule is stated once, in a file only the top-level
  agent loads, and the mechanism that would carry it to a subagent is the
  spawning agent's own memory of it. That is the weakest possible transmission
  path, and it degrades exactly when a task is large enough to be worth
  delegating — i.e. when the discipline matters most.

  **Not proposing a doctrine change on this evidence.** `doctrine/rationale.md` >
  *"How the doctrine evolves under evidence"* rate-limits changes on a single
  incident, and while there are two instances here they are one day, one plan,
  one agent. What is wanted first is a **decision about where the rule belongs**:
  a delegation clause in `AGENTS.md`; a required preamble every subagent brief
  carries; a tool-level default; or an explicit acceptance that budgets are the
  spawning agent's job and the failure was ordinary. That routing question is the
  Maintainer's, and it wants its own proposal rather than a row here.

  **Routing decided 2026-08-19 by the Maintainer — and it is none of the four
  above.** A six-agent analysis under three adversarial verification lenses was
  run over this question. It killed the delegation-clause option on three
  independent grounds. First, the rule it would add is **already loaded**:
  `AGENTS.md` auto-loads into a spawned session through the vendor wrapper's
  import, measured directly — a subagent received the entire file with nothing
  about verification in its brief. That falsifies this row's own premise that "a
  subagent does not read `AGENTS.md`"; the load-bearing gap is that the *mapping*
  lives in the spawner's head, not that the rule fails to arrive. Second,
  `doctrine/roles.md` **already** binds orchestrated sub-agents about fan-out
  specifically, and did not prevent this. Third, the clause is counterproductive
  at the leaf: the subagent reads it too, and what it reads is that `full` is the
  correct answer — ratifying every run it was written to prevent.

  **The adopted rule is structural rather than exhortative: verification is not
  delegated — the spawner verifies once, after the join.** It removes the
  multiplier by construction instead of budgeting it, needs no tooling, and binds
  only the spawner, who demonstrably does read the rule. The leaf never needs to
  know it, which is exactly what makes it immune to the transmission failure this
  row records. Applied as working practice from 2026-08-19.

  **The durable doctrine edit is deliberately not proposed here, and the gate is
  why.** `doctrine/rationale.md` > *"How the doctrine evolves under evidence"*
  bypasses the rate limit only for a **security** or a **data-loss** surface.
  This is a cost surface and qualifies for neither, so the honest route is the
  gate's second trigger — **synthesis at a routine boundary**, where this becomes
  one input to a single aggregated doctrine-proposal stub rather than a
  standalone proposal on one incident. Recording it here is that aggregation
  step, not a substitute for it.

  **One further fact, which bears on any future version of this rule.** The
  eleven runs are *not recoverable from the record*: the plan's
  `Implementation verification` shows exactly the two Boundary B runs it budgeted
  (622.22s and 689.49s), and its code reviewer states outright that they ran
  **zero** full suites, citing the verification boundaries. The doctrine worked
  wherever a record was kept and failed only where nothing observes. So measuring
  whether this rule works depends on the run-frequency ledger proposed in
  `2026-08-19-claude-suite-run-diagnostics`; without it, the next reading of this
  row is another hand-count of one plan. That ledger shipped 2026-08-21 and was
  **retired 2026-08-26** by the subtraction sweep, under the accepted-scope
  allowance its Decision grants. So this row's stated dependency no longer
  exists and will not be satisfied: measuring whether the rule works is back to
  reading the plans themselves. Recorded rather than left implying a collector
  that is coming.
  *Trigger:* the next plan that fans work out to subagents, or any change to how
  briefs are composed.

* **Adversarially pre-reviewing a revision before submitting it** *(observed
  2026-08-19 across two proposals; migrated from a session reflection before it
  pruned)* — before answering an External review, both revisions were put through
  four independent adversarial lenses instructed to find what the *next* round
  would find, each able to run probes. **Yield: nine defects in one draft and six
  in the other, four blocking each time.** Every one was later confirmed to be the
  shape a real reviewer raises: tautological falsifiers, an unsound classifier, a
  sanitizer that raised on ordinary text, a resolver that worked only by luck on
  the fixture it was tested against.

  **Why this is worth a row rather than a habit.** The cost is one workflow; the
  saving is a review round, and a review round on a high-assurance proposal is the
  scarcest resource in this method. It also changes *what* the author submits: a
  contract that has already survived an adversarial read is a different artifact
  from one that has only survived its author.

  **The counter-observation, recorded with it, because it is load-bearing.** A
  pre-review optimises for **the defect it names, not the artifact's purpose**. One
  of its fixes answered a real defect (an undeclared value type) by changing a
  cost field to a node count — destroying what the field was *for*, which the next
  External round caught as an accepted-scope regression. A pasted pre-review fix
  needs the same "does this still do the job" check as any edit the author writes.
  *Trigger:* the next proposal facing a second or later review round; or a
  decision about whether this belongs in `doctrine/dual-review.md` as a named
  practice rather than a roadmap row.

* **Complete-contract revisions lose sections silently, and the ledger cannot see
  it** *(two instances, 2026-08-19, same artifact — recorded because two is the
  recurrence trigger, not because one was surprising)* — Cairn requires each
  Response to append **one complete current-contract revision** that supersedes
  its predecessor in full, plus a mandatory `### Withdrawn / superseded
  commitments` ledger. Both instances came from that shape:

  **(a)** `by_file` changed from per-file *cost* to a node *count* between
  revisions, unlisted. **(b)** Two entire sections — the reader contract and the
  security preflight — were present in Revisions 1 and 2, absent from 3 and 4, and
  **neither the author nor the External reviewer noticed for two rounds**.

  **The mechanism is the ledger's own blind spot.** It is populated from the
  author's memory of what they *consciously changed*; an omission is by definition
  not in that set. So the one instrument designed to make a dropped commitment
  visible is the instrument that cannot see the most common way one is dropped.

  **Mitigation already applied in both live proposals**: each revision now carries
  forward the prior revision's `###` section inventory and states that no section
  is absent. That is cheap, mechanical, and would have caught both instances.
  Whether it belongs in `dev/proposals/_template.md` — or is enforceable by the
  lifecycle checker, which already parses these headings to detect the missing
  ledger — is the open question.

  **Route, deliberately.** `doctrine/rationale.md` > *"How the doctrine evolves
  under evidence"* bypasses the rate limit only for a security or data-loss
  surface, and this is neither. Two instances in one artifact on one day is thin
  for the recurrence trigger. So this is an input to a **goodnight-time synthesis
  stub**, not a standalone proposal.
  *Trigger:* a third instance, or the next synthesis at a routine boundary.

* **Stage-reader tier-semantics defects, and the price of the ratified narrowing**
  *(migrated 2026-08-10 from plan `stage-commit-patterns` at archive, per its
  pre-declared Lasting-truth homing)* — three known, pre-existing observations
  about `_lifecycle_metrics/gitmeta.py`, kept together because they are all
  tier-semantics claims about one module. **(1) R12c, both halves.** The
  behaviour: a transient `git log` failure in `_git_log_for_path` returns `[]`
  and silently downgrades a row with no signal. The documentation half: the same
  function's docstring carries a second falsely-exhaustive cause list that omits
  the `returncode != 0` path. Both halves are named because the plan's grep was
  structurally scoped not to see the second, so an archive that recorded only
  the behaviour would orphan it. **(2)** `_stage_reliability` emits an `Exact`
  row with empty `hours_*` when a proposal's dated stage sections are a
  *non-empty proper subset* of the stages its git history resolves (observed:
  `present = {'decision'}`, `resolved = {'open','decision'}`). **(3) A Maintainer
  question, not a defect:** the ratified scope-gate narrowing buys 0
  false-positive stage assignments at a cost of roughly 17 reliability tiers on
  the live corpus — materially more than the figure priced at Decision time —
  and whether that trade warrants revisiting is the Maintainer's call. Opening a
  proposal for (1) or (2) needs the Maintainer's go-ahead under the standing
  build-nothing-new rule; until then these are recorded as known pre-existing
  defects, not scheduled work. **Separately and more urgent than any of the
  three**: the *shipped* stage vocabulary makes one wrong-stage assignment on
  Cairn's own corpus because a subject matches `^Review\b` across a hyphen —
  that one reaches adopters and is described in the archived plan's archive
  record.
* **Adopter-entry doc-refresh follow-ups** *(deferred, Jun 2026)* — the
  doc-refresh + prose↔runtime drift-gate shipped (plan
  `adopter-entry-doc-refresh`, archived; from the 2026-06-12
  adopter-friction audit). Two deferred follow-ups: (a) a context-aware
  scaffold **`--quickstart` mode** (richer than the "Next steps for a real
  adoption" reframe — let the scaffold print a trimmed next-step for the
  trivial path); (b) extend the `verify:` count guard to **other
  adopter-facing counts** beyond the quickstart's two. Each → its own
  proposal when revived.
* **Four deferred Maintainer questions** *(deferred 2026-08-03, Maintainer-instructed
  to record)* — set aside during the 2026-08-03 Decision round with an explicit "don't
  forget them". Recorded here rather than left in a chat log, because a deferred item
  with no durable home is exactly how the `SECURITY_MUTATIONS.md` Class C security
  follow-on was lost for two months.
  1. **[BND-2] The Class C orphan.** Both `release-authenticity` and `fork-advisory-semantics`
     declined the never-opened Class C follow-on, with reasons, and neither claims it.
     Recommendation on the record in both: ratify it as its own proposal and extend the
     `identity-not-name` archive condition to cover it.
  2. **[REC-3] Is the `Touches` header line mutable?** `Status` already is treated as mutable.
     Append-only protects what was believed at open time, but a stale `Touches` line
     breaks the discovery index siblings grep against. Raised by `fork-advisory-semantics`
     finding I5; the author declined to decide it alone.
  3. **[REL-5] An `AGENTS.md` governing-layer edit** proposed inside `gate-claims-vs-enforcement`
     — extending the rule from "name the trigger" to "name the trigger *and check what it
     checks*", on the argument that a purely lexical rule would not have caught the
     `PROVENANCE.md` instance. Outside Theme 3 and outside the brief that produced it.
  4. ~~**`AGENTS.md` line 337 is a broken pointer**~~ — **RESOLVED 2026-08-03**,
     trivial-class as this entry anticipated. The pointer sent agents to
     `bootstrap/REANCHOR_RUNBOOK.md` to re-anchor the AST baseline; that runbook has zero
     mentions of `ast_attest` or `scaffold_ast_baseline` and governs a different gate.
     Demonstrated to propagate: it seeded four freshly-drafted proposals on 2026-08-03
     before reconciliation caught two — the last of them, `yaml-parser-divergence`,
     inherited it and was caught at External review (finding E4b). `AGENTS.md` now names
     the applicable ceremony inline: a Maintainer-run, dry-run-verified direct correction
     an implementing agent does not perform, precedent `c3d5bd9`.
     **[TRU-4] Residual, deliberately not closed:** there is still no runbook for the AST
     re-anchor — verified, zero Markdown files under `bootstrap/`, `docs/` or `doctrine/`
     mention `ast_attest` or `scaffold_ast_baseline`. The procedure lives only as
     precedent and as prose inside two plans. Whether it earns a runbook of its own is a
     live question; the pointer is no longer *wrong*, it is merely inline.

*(Otherwise empty at adoption — native proposals populate this board. The
Cairn roadmap migrated 2026-06-12 from modflow_tools — queued items,
deferred follow-ups, and the release path — lives at the **bottom** of this
file under "Migrated Cairn roadmap (2026-06-12)".)*

## Active

**This section no longer lists work.** `python tools/board.py` derives the
current view from the artifacts' own header blocks, so a hand-maintained table
here could only be a second, staler copy of it.

```bash
python tools/board.py
```

**Why it was emptied (2026-08-27, the sweep's C7 bankruptcy pass).** All four
entries named here were **archived plans and delivered proposals** —
`git-native-security-foundations`, `review-efficient-lifecycle`,
`lifecycle-status-vocabulary`, `claim-check-exemption-hygiene` — and the block
carried 204 lines describing them as in flight. The section's own rule said a
completed entry is removed at the next goodnight scrub; the scrub had not caught
up, which is the argument for deriving the view rather than scrubbing it.

**Two entries carried live commitments rather than task state, and moved rather
than died** — both into
[`strategy/2026-08-05-codex-security-strategy.md`](strategy/2026-08-05-codex-security-strategy.md)'s
Live residual register:

* the **[TRU-5] gate-reanchor trusted-contributor posture**, which had outlived
  its plan's archive on exactly the grounds that make it a register row;
* the **[REC-1] byline-classification residuals** — six ratified residuals plus
  the `Devine` over-flag. **These lost their subject to the sweep**: the identity
  classifier, the independence comparator and every reader of the roster file
  were removed with the lifecycle machinery that hosted them. The register
  records that as a finding, because it means reviewer independence is now
  enforced by doctrine and Maintainer reading alone, and no one decided that —
  it fell out of deleting the host module.

## Status taxonomy

A board item carries one status. These are the inline reference
for any agent editing the board (the full *why* is in
`doctrine/lifecycle.md`):

* `queued` — accepted or anticipated, not yet in flight.
* `active` — in flight: an open plan, an executing sub-track.
* `blocked` — in flight but waiting on an external dependency or a
  Decision; name the blocker so it is actionable cold.
* `deferred` — consciously parked, **with revival conditions** (what
  must become true for it to return to `queued`).
* `completed` — **transient**: held only between finishing the work
  and the next goodnight scrub, then *removed*. The board keeps no
  completion history — a finished item's permanent home is the
  archived proposal / plan, the implementing commits, and the
  changelog.

**Date-marker convention.** Each item — or its parent section —
carries a `(Mon YYYY)` marker recording when it was added or last
reaffirmed (e.g. `(May 2026)`). The marker makes the staleness sweep
(below) performable by **reading the file**, not by `git blame` or
memory. Refresh the marker whenever the item is reaffirmed at a
goodnight scrub.

## Archive preconditions (proposals and plans)

Before a proposal or plan moves to `archive/`, every
**explicitly-deferred follow-up** it carries must carry a **recorded
disposition**. A disposition is not the same thing as a durable home:
the precondition exists so nothing is dropped *silently*, not so
everything is kept *forever*. Requiring a home for every deferral
makes this board the only sanctioned outcome, which turns it into a
one-way accumulator.

The vocabulary (full rule, including *why*, in
`doctrine/lifecycle.md` > "Archive precondition"):

* `accept` — fixed in scope. Includes writing the doc, and narrowing
  the artifact's own claim so the finding no longer applies (a
  *scope-cut*). **A scope-cut removes no work** — it corrects a claim
  to match what the artifact always did. Removing previously proposed
  or accepted work is a **scope reduction**, which is not an `accept`:
  it takes the outcome test in `doctrine/dual-review.md` and a grouped
  scope-remainder record, and only the Maintainer may concede it.
* `guard (<path>::<node>)` — homed in something that **executes** —
  a test node, an assertion, a runtime guard — and **names the node**.
  A comment is *not* eligible: comments do not fire, and a comment is
  a board row relocated somewhere fewer people read.
* `wontfix` — explicit non-action, **with a rationale**.
* `defer` — deposited on this board. **Requires the Maintainer's
  authorization, quoted verbatim.** A deposit on a shared board is a
  scope decision.

**No required order** — the record says why the chosen disposition is
right. Two eligibility rules bound it: a follow-up that **reaches an
adopter, blocks a release, or needs a Decision** cannot be `wontfix`;
and one **named by a closed artifact's disposition block** cannot be
`wontfix` without the Maintainer, because an archived record is
append-only and cannot be corrected in place.

Record each disposition in a durable, auditable location the team's
workflow preserves (the archive commit body, the PR description, or
the plan's closing metadata) as a `Dispositions: …` block, so the
outcome is reconstructible from the durable record alone. The older
`Follow-ups migrated to: …` spelling stays valid and is still
recognized. **Archive-preparation is the serialization point**, and
`defer` requests are presented there as **one batch** — that batching
is what keeps the Maintainer gate affordable.

On a **solo profile**, where author and Maintainer are the same
person, the `defer` gate collapses to a written justification to
oneself: weaker, but not vacuous — it is on the record at a
serialization point.

This precondition is **documentary, not mechanical**: a reviewer
opening the artifact at archive-preparation is the enforcer.

## Removal preconditions

A `completed` item is **removed**, not crossed off — but removal has
gates. Before deleting a board entry, confirm all three:

1. the accepted proposal / plan is archived;
2. its lasting truth has migrated to durable homes (doctrine, topic
   docs, the changelog);
3. the cold-start "what was tried, and why?" is answerable from the
   archives + commit log **without** this board entry.

If a gate is unmet, finish that migration first, then delete. See
`doctrine/lifecycle.md` > "Removal preconditions for a roadmap item".

---

## Migrated Cairn roadmap (2026-06-12)

Imported from the modflow_tools-side Cairn roadmap when Cairn self-hosted —
live items only, re-expressed for Cairn's vantage (shipped history stays in
the archives); see [`strategy/MIGRATION.md`](strategy/MIGRATION.md). As
native proposals pick these up, they move into the Queued / Active board
near the top of this file.

### Queued

* **Broad-look + roadmap pass** *(queued, Jun 2026)* — the strategy /
  tighten-up pass: take a wide read of the project now that it self-hosts,
  consolidate what accreted across phases 1–4, and shape the forward
  roadmap. The first `dev/strategy/` notes + proposals of the self-hosted
  era.
* **0.3 external correctness test (R-H third-party probe)** *(blocked,
  Jun 2026)* — the launch gate: a consenting third-party scientific repo
  (one that did not contribute to the doctrine) runs the bootstrap
  end-to-end. **Blocks the 0.4 public release.** Blocked on enrolling a
  third party.
* **Remove the collaboration agreement** *(queued, gate: before 0.4)* —
  Maintainer decision (2026-06-12): Cairn no longer needs a collaboration
  agreement. Retire `templates/core/dev/collaboration_agreement.md` and
  re-home/drop every surface that references it (the `AGENTS.md`
  required-reading link, the `agent_collaboration.md` / `dev/README.md`
  pointers, the onboarding tour step, the `doctrine/plans.md` External
  Review Norms cite — re-home those norms, the scaffold's expected-folder
  wiring, the bootstrap tests). Cross-cutting doctrine + template +
  scaffold + test change → its own proposal (the guide star treats the
  agreement as load-bearing, so the proposal carries the deliberation).
* **0.4 launch-surface polish** *(queued for 0.4, not launch-blocking)* —
  graphics/figures in the adopter-facing docs + quickstart (lower the
  "doctrine-heavy at first contact" friction); a comment-cleanup pass
  (strip blow-by-blow comments; keep the *why*) before public adopters
  fork the code.
* **[VER-5] Shipped-executable authority unification** *(queued for 0.4,
  not launch-blocking)* — one `shipped_executables()` traversal for install,
  manifest, security scan, and upgrade, so delivery and scan coverage cannot
  drift through parallel registries.

### Deferred follow-ups (durable home)

* **A stable section identity for an append-only artifact, and a complete-set
  rule over it** *(registered 2026-08-21, from
  `2026-08-20-claude-review-loop-termination` > "Deferred work")* — an
  append-only proposal or plan has no durable handle on its own sections, so a
  rule that wants to say *"every finding of the preceding review is disposed"*
  cannot name the set it must be complete over. This is the gap that made that
  proposal's Change 1 unbuildable and forced its withdrawal. The two halves are
  one problem and are filed together: identity without a complete-set rule
  names sections nothing has to cover, and a complete-set rule without identity
  cannot say what it ranges over. **Revival condition:** a second rule needing
  set-completeness over an append-only artifact — the closure-binding predicate
  in that proposal's C7 is a candidate, and if it lands needing this, that is
  the second instance.

* **A feature list is a claim surface** *(deferred 2026-08-20, from the
  archived `2026-08-10-claude-documentation-enhancement` note's fold-up
  candidates)* — enumerating capabilities on an entry page creates exactly the
  hand-maintained-description-of-a-moving-thing class that drift gates exist
  for, and the observation generalizes past Cairn's own README to any adopter's.
  Candidate line for the `doc-drift-prevention` module's doctrine. **Revival
  condition:** a second instance of an entry-page feature claim going stale, or
  an adopter hitting it — one incident does not clear the doctrine-evolution
  rate-limit gate, and this is currently one. Filed here rather than left in the
  archived note, whose other fold-up candidate shipped and whose remaining
  stages are covered by the *0.4 launch-surface polish* row above.

The permanent, tracked home for Cairn work parked with revival conditions
— each becomes its own proposal when picked up (re-expressed generalizably,
no adopter specifics). Imported from the modflow_tools-side batch ledgers;
none blocking.

**This section cannot be drained from this file — and half of it is unassessed**
*(established 2026-08-04, proposal `2026-08-04-claude-board-retro-disposition`)*.
A pass to mass-adjudicate these rows under the new archive-precondition
vocabulary was proposed and **withdrawn at Internal review**. That withdrawal is
a finding about *method and evidence*, **not** a ruling that the section should
stay this long. Two findings are worth carrying, because they will otherwise be
rediscovered:

  1. **A hand-read sample found reproducers, measured figures and named revival
     conditions.** Bounded, and the bound matters: the sample (~12 rows) came
     **entirely from the census half**, which is the best-documented part of the
     section. Measured across all 58, **29 carry no revival condition**, and the
     shortfall concentrates in the ~31 rows imported from another repository,
     several of which are short stubs with no reproducer. So the defensible claim
     is *"the census rows are genuine obligations"*, **not** *"nothing here is
     clearable"* — the imported half has not been assessed and may well contain
     rows that should be closed.
  2. **Editing only this file cannot dispose of these rows.** The vocabulary's
     two useful tokens — `accept` (fix it) and `guard` (home it in something
     that executes) — both require touching the thing the row is *about*. A
     board-only pass can reach just `wontfix` and `defer`, and the eligibility
     rule bars `wontfix` for anything adopter-reaching, so such a pass would
     **lengthen** this section, not drain it.

**Inbound references — what could be falsified by re-routing a row** *(re-derived
2026-08-04; the proposal's original "six artifacts, two of them archived" was
wrong in both directions and is retracted)*. Two different questions, kept apart
because conflating them is how the first enumeration went wrong:

  * **Artifacts naming *this section*, `as_of 2026-08-04`:** **1** archived plan
  (`interpreter-trust-root-fallback`) and **3** archived proposals.
  `lockfile-provenance-fields` is *not* one — its row is under `## Queued`
  (`dev/PLANNING.md` > "Queued"), which is what the accepted Response promised to
  drop and this line now does.
  * **Commit bodies carrying a migration/disposition block anywhere:** **37** by
  `git log --all --grep='Follow-ups migrated to:\|Dispositions:'`; **30** if the
  marker must start at column 0. Of these, **7** name this section and 13 name
  `dev/PLANNING.md` at all. The method matters more than the number, so the
  command is recorded rather than the figure alone.

Commit bodies are the **most immutable** record of all and no artifact-level
enumeration reaches them — which is the real reason a row a closed artifact names
is ineligible for `wontfix` without the Maintainer.

#### From the first re-anchor ceremony (2026-08-13) — deferred as one batch

The ceremony ran for the first time on 2026-08-13 (`e45e1fc` → `cfaace9`,
published atomically). Both source plans archived the same day. These are the
findings the run itself produced, deferred here on the Maintainer's
authorization at the archive serialization point:

> "Yes, go ahead and close everything else from these two plans out, including
> finding a permanent home for any remaining items"

**Four of the five below change the authority closure, so each one costs a
reviewed-authority transition ceremony.** That is the single most useful thing
to know about this batch: **do not spend a ceremony on any one of them alone.**
Batch them with the implementation of
`2026-08-13-claude-ceremony-as-code`, which already requires a transition
because it changes closure membership. Revival condition for all four is
therefore *"when that proposal reaches implementation"*, not a date.

* **The key-channel probe cannot see an agent-held key** *(closure change;
  `bootstrap/tests/_gate_preflight.py`)*. `probe_cannot_sign` drops
  `SSH_AUTH_SOCK` from its own environment, while the recorded loader
  deliberately passes `SSH_AUTH_SOCK` **through** to Stage 1. So the probe
  measures the on-disk key while an agent-held copy of the same key is
  invisible to the check and available to everything else in that stage.
  `ssh-keygen -Y sign -f <public key>` signs via the agent when the agent holds
  the private half — which is how the 2026-08-13 Stage 2 signed with no
  passphrase prompt. **Observed, not theorised.** Whether the key was in the
  agent during that run's Stage 1 could not be determined afterwards: the agent
  keeps no log, and `AddKeysToAgent yes` was set. Fix direction: the probe must
  test the same channel candidate code has, or the loader must stop forwarding
  the socket — and the runbook's claim must match whichever is chosen.
* **The probe's "non-interactive" claim is false** *(closure change; same
  file)*. The docstring says `< /dev/null` plus a timeout makes the probe a
  definite negative. `ssh-keygen` reads passphrases from `/dev/tty`, so on a
  controlling terminal it **prompts the operator** — observed on 2026-08-13,
  where supplying the passphrase produced a signature and the correct refusal.
  It fails closed, and the claim still does not describe the behaviour.
* **Cairn's roster pins a general-purpose auth key** *(closure change;
  `dev/.cairn/allowed_signers`)*. The anchored roster pins
  `~/.ssh/id_ed25519` — the Maintainer's **GitHub authentication key**. So N4's
  "loaded into no agent" requires removing the key that authenticates day-to-day
  git work, and `AddKeysToAgent yes` silently restores it. A dedicated ceremony
  key makes N4 cheap; a shared auth key makes it disruptive and therefore
  fragile. The repository's `user.signingkey` already names a separate
  `cairn_signing` key that is **not** on the roster — a pre-existing
  inconsistency that only surfaced when the two were first exercised together.
  This is also **adopter-facing doctrine**: what Cairn tells adopters about
  ceremony key hygiene, not just this laptop's setup.
* **Opaque finding-IDs in code comments and docstrings** — **DONE** *(closed
  2026-08-19 by the plan `comprehension-outlives-the-artifact`)*. Raised by the
  Maintainer 2026-08-13: *"They don't inform anyone anything. I don't know what
  FUR5 is."*

  **3,258 occurrences to 260** (`as_of 2026-08-19`, at `f129178`), **and the
  actionable set is empty.** Every remaining
  occurrence is an adjudicated keep, each with its reason in the dispositions
  ledger (folded into the archived plan as *Appendix: the dispositions ledger*): Markdown heading levels
  (`H2`/`H3`), Unicode control classes (`C0`/`C1`), the redundancy gate's
  published detectors (`R1`/`R6`/`R7`), two self-defined in-file schemes
  (`test_transition_lint.py`'s `A1`–`E9`, `test_lifecycle_stage_patterns.py`'s
  `T1`–`T12`), two live Maintainer fences (`N4`, `M3`), one live principal
  ordinal (`P1` in `CAIRN_API_P1_CREDENTIAL`), the `SR6` mutation inventory's
  own title, and the bracketed specimens in two finding-id regex specs.

  **The earlier scope delta is withdrawn and delivered.** An interim state of
  this row deferred 142 occurrences (the frozen `bootstrap/_scaffold/` package
  and the re-anchor ceremony surface) and filed a 246-occurrence blind spot in
  the plan's own three-class matching rule. The Maintainer ruled *"Let's just
  get all of them done before reanchor"*, the rule was widened to five classes
  on that allowance, and both sets are complete. One re-anchor now covers
  everything instead of two.

  **The re-anchor batch has landed** (`77d2b3b`, the Maintainer's supervised
  ceremony). All three artifacts below were regenerated and the suite is green
  on them, re-measured 2026-08-19: `test_ast_attest.py`, `test_gate_manifest.py`
  and `test_portable_security_sweeps.py` pass. Recorded for the audit trail —
  **what the batch carried**, all of it caused by this work and
  none of it self-serviceable: the AST attestation baseline (**37 CHANGED
  symbols** across **74 node lines**, up from 13, `as_of 2026-08-19` at `f129178`
  — `upgrade.py` 26 nodes, `install.py` 18, `slotmerge.py` 10, `merge.py` 8,
  `config.py` 6, `lockfile.py` 4, `security.py` 2; **derive the set against the
  committed baseline at ceremony time rather than carrying this figure forward**,
  per `bootstrap/AST_BASELINE_RUNBOOK.md`); the gate
  manifest, whose frozen-file set and 335 pinned node ids both moved (Chunk D
  renamed 38 containers); and the install lockfile's digest for
  `run_portable_security_sweeps.py`.

* **Doctrine candidate: a figure is true at a commit, not in general** *(filed
  2026-08-19 at the goodnight serialization point, migrated out of a reflection
  before pruning)* — `AGENTS.md`'s numeric-precision rule dates a **published
  snapshot**. It says nothing about a **disposition**, which is also a claim
  about state and carries no date at all. Three instances in one plan: an AST
  count written 35 and true at 37 by the time it was read (**caught by the code
  reviewer, not the author**); corpus totals undated until challenged; and a
  `Dispositions:` block naming three artifacts `defer` after the re-anchor had
  already landed them, corrected only because the block was re-measured
  immediately before commit.

  **Not proposed as doctrine**, deliberately. `AGENTS.md` gained a related rule
  the same day (`ab3d987`, *"confirm the instrument before trusting an
  absence"*), and a second doctrine change generalised from the same agent's
  same session is the churn the rate-limit gate exists to prevent
  (`doctrine/rationale.md` > "How the doctrine evolves under evidence").
  Recorded here so a **recurrence by someone else** clears the gate honestly
  rather than being rediscovered. If it recurs, the cheap form is probably a
  convention that a disposition carries the commit it was measured at, the way
  a snapshot carries `as_of`.

* **The shared *working tree* is an uncovered coordination hazard** *(no closure
  change)*. On 2026-08-12 a concurrent session's path-scoped commit swept
  another agent's **uncommitted** review section into it; the author noticed and
  corrected it. `AGENTS.md`'s commit discipline addresses the shared **index**,
  and path-scoped commits make that hazard structurally impossible — they do
  nothing about two sessions appending to one file. Recorded once, so a second
  occurrence clears the doctrine rate-limit gate rather than being rediscovered.

Also from this cluster and already homed, listed so the batch reads complete:
the runbook-usability defect became proposal
`2026-08-13-claude-ceremony-as-code`; the missing gate-anchor fetch instruction
was fixed in `AGENTS.md` (`088539f`); and the `.pyc`-as-working-tree-mutation
test defect is queued as its own task.

### Security-cluster routing

**The detailed security-debt index moved out of this file on 2026-08-27**, at
the subtraction sweep's C7 bankruptcy pass. It lived here as 93 rows over 1,010
lines; it now lives in
[`dev/strategy/2026-08-05-codex-security-strategy.md`](strategy/2026-08-05-codex-security-strategy.md)
under **Live residual register**, one entry per surviving row, each reduced to
its lasting boundary, residual, or revival trigger.

**Why it moved.** The strategy was already the cluster authority and this board
the task authority, but the *triggers* had accumulated here — so a security
residual's revival condition sat in a task board that no longer had a task for
it. The board now owns task state and which artifact is active; the strategy
owns the residual and what revives it.

**Where to look.**

| If you want | Read |
|---|---|
| A live residual and what revives it | the strategy's **Live residual register** |
| The cluster a finding belongs to, and whether two findings are one scope | the strategy's **Cluster map** and **Decision test for new findings** |
| Reproductions, per-row evidence, review findings | the archived plan named on the register entry |
| What the sweep deleted, and the measurement that justified it | [`dev/plans/archive/subtraction-sweep.md`](plans/archive/subtraction-sweep.md), C7 bankruptcy record |

**Filing a new security finding.** It receives one primary cluster, one owner or
revival trigger, and one decisive evidence path — in the strategy, not here.
Sharing a source plan or the word "security" is not a reason to open another
scope. Completed rows leave at their lifecycle serialization point rather than
being copied into another backlog.

### Release path

The version ladder is staged so the methodology stabilizes before going
public:

* **0.3.0** — current; private internal milestone (2026-06-12). Phases 1–4
  complete; Phase 5 (launch + governance) in progress.
* **0.3 external test** — the R-H third-party correctness probe (queued
  above); must clear before going public.
* **0.4 — earliest public release.** No earlier than 0.4, and only after the
  0.3 external test clears. The 0.4 candidates above are launch-surface
  polish, not blockers.
* **0.5+** — per-project efficacy-data infrastructure and beyond.

**Public-launch sequence** (deferred to 0.4+; Maintainer-gated, in order).
**Revised 2026-08-04** to carry plan `release-authenticity`'s Chunk M, which is
Maintainer-only and was not performed by the implementing agent. The previous
ordering is preserved below under *What changed and why*, because following it
would have failed this scope's own acceptance check.

1. Eyeball-check the private mirror renders cleanly.
2. **Publish the signing key's fingerprint on the named channels.** This
   creates the trust root and **must precede the tag**, so the tag is
   verifiable the moment it exists. Includes confirming the forge actually
   serves SSH **signing** keys (not authentication keys) at a stable public
   endpoint for this account — `bootstrap/PROVENANCE.md` records this as **"not
   established, as_of 2026-08-03"** and names it the fact the scope most
   expects to be corrected. If it is false, ORCID is promoted to primary and a
   third channel is added; the procedure is unchanged, only the table.
3. Flip the repo to public + set the template-repo flag (the actual "ship it"
   moment; explicit go-ahead required).
4. **Tag `v0.4.0` with `git tag -s`** — signed, **not** `-a`.
5. **Run the bootstrap block cold against the pushed tag**, from a machine and
   a roster that did not come from the repository. **This is the acceptance
   check for the whole `release-authenticity` scope**: if it does not pass
   here, nothing in that plan's Chunks A–G established the control.
6. **Only then** enable Zenodo integration and let deposition proceed → DOI.
7. Commit the issued DOI into `CITATION.cff`.
8. Archive the `cairn_methodology_repo` construction plan via lasting-truth
   migration.

**What changed and why.** The prior sequence read *"enable Zenodo integration →
tag `v0.4.0` and push (triggers Zenodo deposition → DOI)"*. Because deposition
fires automatically on the tag push, enabling Zenodo before the tag leaves **no
window** for step 5's cold run — the acceptance check would land after an
immutable version record already existed. Steps 5 and 6 are therefore swapped
relative to the old ordering, and steps 2 and 4 are new. The old sequence also
did not specify `-s`, so it would have produced an **unsigned** tag that the
whole scope exists to make verifiable.

**If the launch reaches step 4 before step 2 is done, HOLD the tag** rather
than shipping an unsigned one and fixing it later. A Zenodo version record is
immutable once published and a methods-section citation is not recallable.

**Archive note.** Plan `release-authenticity` **cannot archive until step 5
passes.** Its control is *documented and tested but not established* — no
fingerprint is published, no signed tag exists, and no network-side fact has
been checked. Homing Chunk M here gives it a durable home; it does not make the
plan complete.

**Revised 2026-08-04 — steps 4-7 released from the plan, and the archive no
longer gates on step 5.** By Maintainer ruling (recorded in the plan), Chunk M's
tag, cold run and Zenodo deposition are **released to this sequence** and no
longer block `release-authenticity`'s archive; only a code review does. They are
released, **not dropped** — the obligation lives here now. Two facts changed
under the earlier note above and it is superseded to that extent: the signing
key's fingerprint **is** published (channels 1 and 2, 2026-08-04) and the forge's
signing-key endpoint **is** established, serving signing keys distinctly from
authentication keys. Zenodo stays unchecked, so channel 3 does not exist and the
two-channel rule runs on channels 1 and 2 — sufficient under
`bootstrap/PROVENANCE.md`, which requires at least two. **The control itself
remains documented and tested but not established:** no signed tag has ever been
verified by it, and step 5 is still what would establish it.
