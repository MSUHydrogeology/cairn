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
deliberation is at `dev/strategy/2026-07-11-claude-cairn-adoption-record.md`,
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
  `python tools/lifecycle.py session-start` to orient at the top of a
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

* **`SECURITY.md` disclosure channel** *(split out of `contributor-entry` by
  Maintainer direction, 2026-08-03)* — `SECURITY.md` tells a reporter to report
  "privately to the maintainer" and **names no mechanism**. Verified 2026-08-03:
  no root `CONTRIBUTING.md` exists, and `README.md` carries no *Contributing*
  heading, so a would-be reporter has no route. This is the half of
  `contributor-entry` that the I2 decision keeps: the disclosure gap is real and
  fixing it needs **no** `CONTRIBUTING.md` and no doctrine change, which is
  precisely why it separates cleanly. Diagnosis of record: a stated control with
  no mechanism behind it — the same shape as `PROVENANCE.md`'s unchecked
  signature, catalogued in `gate-claims-vs-enforcement`. Carries one
  non-reviewable precondition from that proposal's finding [I7]: the channel's
  deciding property (whether the forge setting is actually enabled) cannot be
  established by a reviewer and is a **Maintainer live-verification step**.

* **Adopter-entry doc-refresh follow-ups** *(deferred, Jun 2026)* — the
  doc-refresh + prose↔runtime drift-gate shipped (plan
  `adopter-entry-doc-refresh`, archived; from the 2026-06-12
  adopter-friction audit). Two deferred follow-ups: (a) a context-aware
  scaffold **`--quickstart` mode** (richer than the "Next steps for a real
  adoption" reframe — let the scaffold print a trimmed next-step for the
  trivial path); (b) extend the `verify:` count guard to **other
  adopter-facing counts** beyond the quickstart's two. Each → its own
  proposal when revived.
* **Transition-lint** *(queued, accepted 2026-07-22)* — an **advisory**
  check that a commit's message claim is supported by its diff: a subject
  claiming a review / response / decision transition whose diff adds no such
  section, and a proposal-*open* commit whose file already carries reviews.
  Guards the failure that opened the tighten-up (Cairn's own showcase arc
  carried both shapes). Accepted at proposal stem
  `2026-07-22-claude-transition-lint`, which pinned the heuristics this entry's
  earlier deferral was waiting on — an independent reimplementation scored **0
  false positives across 538 commit subjects**, surfacing exactly the 3 real
  incidents. The sibling reader-fix (stem
  `2026-07-22-claude-stage-commit-patterns`) confirmed it is *not* made
  redundant: that reader classifies messages and never opens a diff.
  **Queued, not next** — maintainer-facing apparatus, and the standing priority
  is postdoc-first; it does not displace adopter-path work. Plan conditions
  (rename-awareness, narrowed trigger, carve-in-bounded exceptions, advisory
  exit 0, no silent-clean) are ratified in the Decision. → plan-open when it
  reaches the top.
* **Self-host lockfile reconciliation** *(deferred, Jul 2026)* —
  `python bootstrap/scaffold.py upgrade --target . --cairn-root . --plan`
  currently reports **38** files as "no recoverable base (review-only
  diff)" against the base cache, each needing a by-hand `--stage`/`--apply`
  merge or a reviewed `--finalize` once its actual customization state is
  confirmed. Surfaced (not caused) by the `solo-legacy-adopter-path` plan
  (archived; Part 3 touched one of the 38, `dev/proposals/_template.md`,
  and deliberately left its lockfile hash un-finalized rather than
  hand-patching one file in isolation — see that plan's Lasting-truth
  migration for the full account). No proposal yet; revive by running
  `--plan` fresh, confirming the current file list, and scoping the
  reconciliation pass (likely several small, reviewed `--finalize` batches
  rather than one large `--apply`).
* **Lockfile schema validate-on-read** *(deferred, Jul 2026)* — the
  `lockfile-provenance-fields` proposal (plan `lockfile-provenance-fields`)
  adds two provenance fields to the install lockfile without bumping
  `_LOCK_SCHEMA` or teaching `read_lockfile` to validate on read — a
  deliberate P4 deferral, not an oversight: `read_lockfile` is the second
  trust anchor (`bootstrap/_scaffold/lockfile.py:3`), and teaching it to
  *reject* a lockfile on a version predicate is a fail-closed behavior
  change on the path `upgrade` and `verify_integrity` both traverse —
  plausibly its own Security-Review trigger, and exactly the "contract
  change married to a smaller change" bundling this proposal itself was
  split out to avoid. Revive as: validate `schema` on read, with a
  migration hint, and decide the fail-open / fail-closed disposition — its
  own proposal, on its own review tier.

* **Scoped test execution for iterative agent work** *(queued 2026-08-03,
  Maintainer-raised)* — the full suite is **1560 tests in 128s** (`as_of
  2026-08-03`, canonical Python 3.13.13). Run once at a commit boundary that is
  fine; run it mid-iteration in a multi-agent loop — where several agents each
  verify, several times — and it dominates wall-clock. **The cost is spread, not
  concentrated:** the slowest 20 tests total ~28s, about 22% of the run, so there
  is no hot spot to mark `slow` and no single test to fix. It is ~1560 tests
  averaging ~82ms, most of them installing scaffold trees into temp dirs and
  shelling out. The problem is also **growing**: 1471 → 1560 tests in one
  session as gate-preflight Chunk A landed.

  Three candidate directions, none chosen — this entry is the problem statement,
  not the design:
  (a) **Parallel execution.** 14 cores available, zero used. `pytest -n auto`
  (xdist) is dev-only, which the dependency budget already permits by the
  `vermin` precedent (`bootstrap/requirements-dev.txt`). Biggest single lever,
  but needs a parallel-safety audit first — tests sharing the AST baseline, the
  gate manifest, or fixed temp paths may not be isolated.
  (b) **A change→surface test map.** `AGENTS.md` already tells an agent to
  "route by file (`test_<surface>.py`) and by node when scoping a change", but
  ships no mapping, so an agent with no way to know which subset covers its edit
  conservatively runs everything. This is the closest thing to the actual ask.
  (c) **A named fast tier** for mid-iteration, with the full suite reserved for
  commit and review boundaries.

  **The build-nothing-new gate is cleared:** the Maintainer raised this directly
  and asked for it, which is the explicit go-ahead that standing direction
  requires. Recorded here so a later reader does not re-litigate it.
  **Open question for whoever picks this up:** any fast tier is a claim about
  what it is safe *not* to run, and a green fast tier that misses a real
  regression is worse than a slow suite — so the design has to say what evidence
  backs the subset, not just how much time it saves.

* **Four deferred Maintainer questions** *(deferred 2026-08-03, Maintainer-instructed
  to record)* — set aside during the 2026-08-03 Decision round with an explicit "don't
  forget them". Recorded here rather than left in a chat log, because a deferred item
  with no durable home is exactly how the `SECURITY_MUTATIONS.md` Class C security
  follow-on was lost for two months.
  1. **The Class C orphan.** Both `release-authenticity` and `fork-advisory-semantics`
     declined the never-opened Class C follow-on, with reasons, and neither claims it.
     Recommendation on the record in both: ratify it as its own proposal and extend the
     `identity-not-name` archive condition to cover it.
  2. **Is the `Touches` header line mutable?** `Status` already is treated as mutable.
     Append-only protects what was believed at open time, but a stale `Touches` line
     breaks the discovery index siblings grep against. Raised by `fork-advisory-semantics`
     finding I5; the author declined to decide it alone.
  3. **An `AGENTS.md` governing-layer edit** proposed inside `gate-claims-vs-enforcement`
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
     **Residual, deliberately not closed:** there is still no runbook for the AST
     re-anchor — verified, zero Markdown files under `bootstrap/`, `docs/` or `doctrine/`
     mention `ast_attest` or `scaffold_ast_baseline`. The procedure lives only as
     precedent and as prose inside two plans. Whether it earns a runbook of its own is a
     live question; the pointer is no longer *wrong*, it is merely inline.

*(Otherwise empty at adoption — native proposals populate this board. The
Cairn roadmap migrated 2026-06-12 from modflow_tools — queued items,
deferred follow-ups, and the release path — lives at the **bottom** of this
file under "Migrated Cairn roadmap (2026-06-12)".)*

## Active

Substantive work currently in flight: open plans, executing
sub-tracks, in-progress proposals between Decision and
plan-open. When an entry completes, it is **removed** from this
section at the next goodnight scrub — the truth migrates to the
archived plan / proposal, the implementing commits, and the
changelog. There is no "completed recently" section on this
board by design.

* **gate-reanchor-preflight posture** *(plan archived 2026-08-03; this entry
  survives because its commitments are live, not completed)* — the trust root is
  established at `e45e1fc` and the pre-flight is in the anchor, so every ceremony
  from here runs the anchored loader. What remains open is the **dated
  threat-model posture**: Cairn accepts a *trusted-contributor* model for its own
  trust root, **single-maintainer, as of 2026-08-03** — not a standing
  assumption. Its mechanical expiry is **signature verification against a pinned
  roster from the recorded signing epoch** (`a07fac8`); `apply` refuses any
  commit at or after it that is unsigned or signed by a key outside
  `dev/.cairn/allowed_signers`. *(Corrected at archive: this entry previously
  named a committer-identity tripwire. That mechanism was superseded during
  implementation — Git's committer name and email are unauthenticated and a
  spoofing probe defeated it, GPR2.)* **Two triggers cannot be mechanical and
  live here on purpose:** (a) the ceremony run on a checkout the Maintainer does
  not solely control; (b) any adopter taking the mechanism. On either, revisit
  the posture — the named upgrade paths are OS containment for the evidence stage
  (SR7), external anchoring via `_gate_manifest.py verify --trusted-repo` (SR9,
  supported all along and **newly usable now that a `P` exists to anchor**), and
  a single-use nonce / consumption ledger (SR10). Archived plan
  `gate-reanchor-preflight`; eleven findings closed across seven reviews (CR1,
  FUR1-FUR10).

* **stage-commit-patterns** *(accepted 2026-07-22, awaiting plan-open)* — the
  reader fix: `_STAGE_COMMIT_PATTERNS` matched **zero of 76** real commit
  subjects, leaving every stage-timing metric empty at `Best-effort` while the
  tool exited 0. Accepted with the design narrowed (no bare-subject fallback)
  so no commit is ever mislabelled at `Exact`. Part 1 is **transcription, not
  audit** — the 28-symbol table is verified in the Revised proposal. Plan
  carries a scoped `upgrade --finalize` for `gitmeta.py` and its `__init__.py`
  twin, now mandatory since the lockfile is clean.


* **byline-classification residuals** *(plan open 2026-08-03; the rows land at
  plan-open, not at archive, so they outlive the proposal's readership)* — the
  character-preserving identity fold and the whole-name exact match closed a
  demonstrated privilege-widening defect in `IdentityModel.classify`. Six
  residuals were ratified alongside it, each with a named trigger, plus one
  pre-existing over-flag recorded so it is not mistaken for a regression. A
  residual with a named trigger is a decision; one without is debt.
  * **R1 — the exact-name spoof.** Anyone who can write bytes into the artifact
    can write the rostered display name exactly; no name matcher fixes this,
    and the tool attests structure while the operator guarantees authorization.
    Accepted **as dated**: single maintainer, roster size **1**, `as_of
    2026-08-03`. *Mechanical expiry:* `human_maintainers` in
    `dev/.cairn/agent-identities.json` gaining a second entry. *Non-mechanical:*
    a signing trust root that binds a Decision-introducing commit to a verified
    signer, at which point this classifier is re-decided as a lint over an
    authenticated signal rather than the thing standing in for one.
    *Backstop:* re-state or re-decide 2027-02-03.
  * **R2 — presentation-fold equivalence, RESTATED.** The granting fold makes
    two names one key when they differ by **canonical decomposition or full
    case folding**. The proposal asked the Decision to ratify this as "accent-
    and case-variants … every member reads as the rostered name to a human";
    three measured classes falsify that wording, so what is ratified here is
    the restated form with the classes named: (a) **full case folding**
    expands ligatures and long-s, so a byline a reader sees as *Kriften Long*
    keys as the rostered *Kristen Long*; (b) **combining-mark stripping**
    collapses marks that carry letter identity outside Latin — Vietnamese
    tone, hiragana KA vs GA, the Devanagari nukta, Cyrillic YE vs YO — so a
    *different person's* name keys as the rostered one; (c) case. All three are
    **accepted with the class on the record** and pinned in
    `bootstrap/tests/test_byline_identity.py`, so a later narrowing is a
    visible test change, not a silent drift. The original mechanical expiry
    ("the first demonstrated string that folds to a rostered name and does not
    read as it") was satisfied *before* ratification and is therefore spent.
    *Mechanical expiry, re-marked:* a demonstrated member of the class that is
    **not** in the three named groups. *Non-mechanical:* a granting fold that
    narrows (drops case folding or mark stripping) — which the pinned test is
    designed to surface.
  * **R3 — the independence widening, partially closed.** The independence
    comparator now folds at `NFKD` and catches the precomposed-accent,
    mathematical-bold and circled-letter disguises of an author byline — **3 of
    4** measured variants. The **Cyrillic-homoglyph variant stays open**: a
    same-agent review spelled with a confusable still satisfies the
    `independent_review` gate. Not fixed here because every sound fix needs a
    *reviewer*-identity contract that does not exist, and the only human list
    that does exist confers Decision authority; reusing it would couple two
    authorities to buy one fix. The 3-of-4 state is pinned in
    `bootstrap/tests/test_byline_identity.py`. *Mechanical expiry:* the first
    `## Review` in this repository authored by a human who is not the
    Maintainer — the event that makes the gate load-bearing. *Non-mechanical:*
    any durable list of people who may review but may not decide.
    *Backstop:* 2026-11-03.
  * **R4 — the flag is not a detector, CORRECTED.** The `unknown` violation
    message appends the `ascii()`-escaped byline so a confusable is visible at
    the moment of failure; it reveals, it does not detect. R4's stated expiry
    was "when `agent-context-scrub` lands its escaping helper, this call site
    adopts it rather than keeping a second escaper." Measured against that
    sibling's accepted design (`c7266d4`): its `_FIELD_ESCAPES` table covers C0
    and C1 controls, DEL, the two line separators and backslash, and states in
    terms that ordinary international text passes through untouched. A Cyrillic
    confusable **is** ordinary international text, so adopting that helper here
    would produce **no diagnostic at all** — the exact failure this escaper
    exists to fix. The two escapers serve opposite purposes: one renders a
    payload inert while preserving international text, the other reveals that
    international text is present. **The merge is measured as wrong**, and the
    trigger is re-marked: *a shared helper that takes the reveal mode as a
    parameter, or nothing.* (This is a correction to a residual's routing, not
    a design change; flagged for the Maintainer alongside R2's restatement.)
  * **R5 — the behaviour change for a token-style roster.** A `human_maintainers`
    entry is now the complete display name, and names are compared
    separator-for-separator; a fragment-style roster recognizes nobody after
    this change, and a display name written with a non-ASCII `Zs` separator is
    recognized *before* it and not after. *Mechanical expiry:* the entry under
    `CHANGELOG.md` > Unreleased > Fixed reaching the **v0.4.0 release notes**.
    If v0.4.0 ships without it, R5 is unresolved. Blast radius at ratification
    is Cairn itself (corrected in the implementing commit) and **zero external
    adopters**, which is why this is a release note rather than an upgrade
    note; if an adopter exists by v0.4.0, an upgrade note is required instead.
  * **R6 — the roster file has no documented home.**
    `dev/.cairn/agent-identities.json` is read by shipped code, written by no
    installer, and documented only in a code comment (revised by this change to
    state the config's grammar). *Mechanical expiry:* one sentence in
    `bootstrap/UPGRADE.md` or the adopter-facing skills documentation, **no
    later than v0.4.0 release preparation**. Explicitly fenced out of the
    implementing plan, which changes the *content* of an installed file, not
    the set of installed files or their docs.
  * **Pre-existing: the `Devine` over-flag.** The AI registry matches `devin`
    as a *prefix*, so the real surname **Devine** classifies `ai` today and
    after this change — and because the AI leg has precedence, a Maintainer
    with that name cannot fix it from the roster. Not introduced here, not
    fixed here, and a genuine postdoc-first hazard; recorded so it is owned
    rather than rediscovered. *Trigger:* anyone whose display name
    prefix-matches a registry entry needing to be recognized as human — at
    which point the AI leg needs a roster-beats-registry escape, which is its
    own proposal.

---

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
**explicitly-deferred follow-up** it carries must have a durable home
*outside* the file — a board item here, a topic doc's "Future work"
section, or its own queued follow-up proposal. Record where each went
in a durable, auditable location the team's workflow preserves (the
archive commit body, the PR description, or the plan's closing
metadata) as a `Follow-ups migrated to: …` block, so the migration is
reconstructible from the durable record alone. See
`doctrine/lifecycle.md` > "Archive precondition — every deferred
follow-up has a durable home".

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
  fork the code; and the shipped-executable-authority unification (one
  `shipped_executables()` traversal for install / manifest / security
  scan / upgrade).

### Deferred follow-ups (durable home)

The permanent, tracked home for Cairn work parked with revival conditions
— each becomes its own proposal when picked up (re-expressed generalizably,
no adopter specifics). Imported from the modflow_tools-side batch ledgers;
none blocking.

**Lifecycle apparatus**
* **Lifecycle mutation/commit arm** — the typed-mutation ops (decision /
  review / open / archive) + commit the read-only planner deferred; gated on
  the dogfood study *and* its own Security Review (commit is a separate
  privilege; print-the-command in v1).
* **Lifecycle mechanization dogfood study** — the multi-session,
  Maintainer-run measurement that earns (or declines) the mutation arm; rank
  by prevented-failure / preserved-assurance, not frequency.
* **Planner cross-checks** — `next` surfaces "review status undetermined" on
  an absent/malformed plan-review line (E-#1); assert the artifact resolves
  under `dev/` (E-#2).
* **`_agent_of` round-suffix regression test** — pin the `## Review (Round
  N)` header shape in the Cairn tree.
* **Interpreter trust-root check/use race (S2)** *(deferred, Jul 2026)* —
  the `interpreter-trust-root-fallback` proposal's dedicated Security Review
  (plan `interpreter-trust-root-fallback`) red-teamed
  `_has_symlink_component`'s symlink walk in `templates/skills/_lib/
  lifecycle.py` and demonstrated a check/use race: replacing a checked real
  parent with a symlink between the walk and execution selects the
  retargeted binary. Pre-existing (not introduced by that proposal's
  absent-path degrade), and the attacker prerequisites generally permit
  replacing the interpreter directly, so it does not block that proposal's
  bounded downgrade — but the Decision explicitly did not accept it as
  closed. Revive as: a design that closes the race (e.g. re-verify
  post-walk, or resolve and open atomically) — its own proposal, on its own
  review tier given the security surface.

**Scaffold / engine**
* **Facade-loader symlink hardening (C-#3)** — refuse any engine submodule
  that is a symlink or resolves out-of-tree, across all three facades.
* **End-gate frozen-set decision (C-#4)** — whether the A/B/C engine
  packages fold into the gate manifest's `frozen_files`.
* **Facade residuals (B-#1/2)** — clean a partial `sys.modules` entry on a
  failed mid-load; reject a mismatched `<kind>:` prefix in `_ast_attest`.
* **Side-door non-executable surfaces** — disposition for the onboarding
  activation log, preset sources, and issue-capture forge starters.
* **Module destination renames / binary module files** — relocation
  classification when a module's destination changes; byte-preserving staging
  for non-text module files.

**Security apparatus**
* **Install-integrity trust anchor** — `bootstrap/verify_integrity.py` reads
  expected hashes from **the candidate target's own** `dev/.cairn/cairn-lock.yml`
  (`verify_integrity.py:47`, `read_lockfile(target)`), so a coordinated tamper —
  modify target files, then regenerate the lockfile over them — verifies as `OK`.
  `CAIRN_ROOT` exists in that module (`:34`) but only puts the engine on
  `sys.path`; it is not the hash source. Reproduced 2026-08-03 against the
  shipped module; the docstring is accurate that this is "a lockfile-backed
  preflight, not an in-file self-verifier" — the gap is that the lockfile lives
  inside the thing being checked. Revival condition: anchor the **verbatim
  subset** against the caller's trusted `CAIRN_ROOT` checkout. A successor must
  define which files are genuinely verbatim, what happens when the caller's
  checkout *is* the candidate, and how a legitimately-diverged fork is
  distinguished from a tamper — which is why it is a proposal, not a patch.
  Raised by the `release-security-bar` External review, finding E1, and homed
  here rather than widening that proposal's fences.

* **Conda advisory coverage** — `python-security` audits **Python
  distributions**; conda-managed native packages are outside its declared scope
  (narrowed by Maintainer direction 2026-08-03 in `dependency-advisory-coverage`,
  finding DAC3). The gap is measured, not estimated: on the canonical
  environment **147 conda-only packages, 82 of them native** — `krb5`, `openssl`,
  `freetype`, `icu`, `hdf5`, the `aws-c-*` stack — `as_of 2026-08-03`. Revival
  condition: **a maintained advisory authority for conda-forge packages that
  execution demonstrates**, not documentation. Evidence already established, so a
  successor does not re-derive it: **Trivy**'s conda coverage is SBOM/license
  only with vulnerability scanning *unsupported*; **OSV-Scanner** does not list
  Conda among supported ecosystems; **Grype/Syft** match by CPE rather than
  ecosystem and are **unevaluated by anyone** — the first candidate to actually
  run. A hand-built conda-name→CPE map is *not* another adapter: it makes Cairn
  the security authority for product identity, and needs its own Decision.
  Watch-outs a successor inherits: conda-forge can patch a CVE without bumping
  the upstream version (build strings carry no patch manifest), so naive version
  matching produces false positives in one direction and false negatives in the
  other; and vendored/statically-linked code has no record in any inventory.

**Stack-neutrality**
* **Language-neutral conformance fixtures + golden vectors (Move 5)** — for
  the extrication seam (exit semantics, path containment, lockfile schema,
  slot parsing, 3-way merge, security refusals), generated from the Python
  reference. The seam architecture shipped; the executable fixtures are
  deferred.

**Coordination**
* **Refine the intent tool's necessity test** — gate on *shared-worktree*
  multi-agent, not just team size (worktree-per-agent doesn't need it).
* **Move `dev/intent-config.json` → `dev/.cairn/`** — machine-edited settings
  belong in the machine-state dir; transition reads both paths.

**Doctrine**
* **Count-claims doctrine dedup** — fold the three-kind concept into
  `doctrine/lifecycle.md` with a one-line pointer from `doctrine/proposals.md`
  + `doctrine/plans.md`.
* **Model-tier vocab single-source** *(low residual)* — the tier→model
  binding is canonical in `dev/.cairn/model-selection-mapping.yml`; revisit
  only if a project later adds its own metrics-config tier vocab.

**Release authenticity** *(residuals from plan `release-authenticity`)*
* **RA1 (a) — Cairn's signing authority widens** *(non-mechanical for the
  adopter, mechanical for Cairn)* — the principal-count warning in
  `bootstrap/container/verify-ref.sh` counts a roster the *adopter* typed and has
  no channel back here, so it is adopter hygiene, not a Cairn-side trigger. The
  mechanical half is a Cairn suite node
  (`bootstrap/tests/test_verify_ref.py`, `test_cairn_roster_names_one_principal`
  — exactly 1 principal in `dev/.cairn/allowed_signers`, `as_of 2026-08-03`).
  Revive when that node fires: the one-signer, two-accounts trust model no
  longer describes Cairn.
* **RA1 (b) — transparency-log / keyless verification** — revive when such a
  verifier is usable without adding an adopter runtime dependency. The
  zero-dependency budget is the constraint, not the idea.
* **RA1 (c) — a reported cross-channel fingerprint mismatch** — revive the moment
  any adopter reports one; the two-channel comparison is the whole trust anchor,
  and a mismatch means it failed.
* **RA3 — verifying the tree you build from** — the bootstrap proves a tag object
  is signed, not that a working tree equals that tag's tree. Revive when the
  scaffold gains a "verify my source" entry point, or when the lockfile's
  `cairn_commit` is cross-checked against a verified tag; either makes this an
  addition rather than a redesign.
* **RA5 — the candidate-git-config class on OTHER surfaces** — closed for
  `bootstrap/container/verify-ref.sh` by construction (verification runs in a
  workspace the script creates, never in the candidate), but **not swept**: no
  enumeration of every config key that can influence a git verification, and the
  fetch still runs `upload-pack` inside the candidate. Revive at the next Cairn
  surface that shells out to `git` against a tree Cairn does not control.
* **RA6 — install-side provenance** — source-side signing landed; the lockfile's
  `source_repository` / `source_licenses` stay **declared**, not attested, and
  `python bootstrap/scaffold.py --manifest` stays unsigned. Revive when an
  adopter asks "how do I know my installed tree came from the release I
  verified?", or when the fork-advisory scope reaches the same seam from the
  other side.

**Adoption UX**
* **Constructive readiness** — when a Cairn tool finds a project below an
  expected bar, it should *offer and drive the path to readiness* (scaffold
  the missing pieces, guide the next action), not emit a bare "not ready"
  verdict. Generative about adoption, not only diagnostic.

**Lower-priority**
* **Container P3s** — acceptance credential-residue leg (note/drop); `--user`
  on a future Docker acceptance leg; pin the `git` apt version for image
  byte-reproducibility.
* **Differential-oracle two-stage `promote`** — future-use mechanism for a
  Cairn-engine refactor needing behavior-preservation promotion (trust root
  established, nothing pending; see `bootstrap/REANCHOR_RUNBOOK.md`).
* **Lifecycle-routine skill payloads (post-v1)** — additional episodic skills
  (proposal-open, review-append, decision-scribe, plan-archive); promote
  harness skill targets to native-tested as fixtures prove them.

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

**Public-launch sequence** (deferred to 0.4+; Maintainer-gated, in order):
eyeball-check the private mirror renders cleanly → flip the repo to public +
set the template-repo flag (the actual "ship it" moment; explicit go-ahead
required) → enable Zenodo integration → tag `v0.4.0` and push (triggers
Zenodo deposition → DOI) → commit the issued DOI into `CITATION.cff` →
archive the `cairn_methodology_repo` construction plan via lasting-truth
migration.
