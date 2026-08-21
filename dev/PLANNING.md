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

* **[TOOL, URGENT] `dev/plans/` corpus-wide metrics extraction is currently
  broken -- `lifecycle_metrics.py plans` exits 3 (`INCOMPLETE`) against the
  live tree** *(filed 2026-08-21, from `metrics-events-not-prose`'s code
  review, CR1)* -- `dev/plans/metrics-events-not-prose.md`'s own commit
  `822cf903` flipped its header `**Status**` from `implementing` to
  `awaiting-code-review` after this plan's Chunk 6 established the
  `cairn-event-v1` activation cutoff for `dev/plans/` (`126cda5`), with no
  matching event block -- a direct miss of that same chunk's own acceptance
  criterion ("every act *this plan's own commits* perform, from this chunk
  onward, carries a matching block and reconciles cleanly").

  **This is not recoverable by editing code.** The reconciler's own rule --
  a `transition` block may only be attributed to the commit whose diff also
  changes `**Status**` -- means no later commit can retroactively supply the
  missing block without either rewriting `822cf903` (destructive, and it
  would invalidate the commit hashes this plan's own Implementation section
  already cites) or building a new, explicitly-authorized grandfather /
  exemption mechanism in the reconciler. `plan_rows()` aborts the *entire*
  `dev/plans/` walk on the first unreconciled artifact (checked: confirmed
  via `git merge-base --is-ancestor` that this is currently the *only*
  artifact in the corpus with post-cutoff history, so today's blast radius
  is total but self-contained to this one file), and archiving this plan
  does not remove it from the walk (`iter_plan_files()` includes
  `dev/plans/archive/**/*.md`).

  **Needs a Maintainer decision**, not a routine backlog pick: whether to
  accept a permanently-`INCOMPLETE` `plans` corpus walk as the cost of this
  feature landing the way it did, or to scope a small, explicit exemption
  mechanism (a `(path, commit)` grandfather list, most likely) as new,
  authorized work. Reproduce with `python tools/lifecycle_metrics.py plans
  --root .` on the current tree. Full writeup: the plan's own `## Code
  review -- Claude Sonnet 5 -- 2026-08-21` section, finding CR1, and its
  `## Lasting-truth migration` Dispositions entry.

* **[TOOL] The divergent-activation-marker safety check the accepted
  `metrics-events-not-prose` contract requires ("Both refuse") is
  implemented but never reachable from a real corpus walk** *(filed
  2026-08-21, from the same code review, CR3)* -- `events.activation_commit()`'s
  `companion_relpath` parameter is the mechanism for catching Cairn's own
  installed template (`dev/proposals/_template.md` / `dev/plans/_template.md`)
  diverging from its shipped doctrine twin (`templates/core/dev/proposals/_template.md`
  / `templates/core/dev/plans/_template.md`), and it works correctly when
  called directly. `extract.py`'s `_reconcile_artifact` -- the only call site
  the real `proposal_rows()`/`plan_rows()` walk goes through -- never passes
  `companion_relpath`, confirmed end to end against a real divergent-marker
  scratch repo through `extract_proposal_row`. Currently harmless (all four
  marker paths agree at `HEAD` as of this writing) and already
  transparently disclosed in `126cda5`'s own commit body, not hidden.

  Wiring it needs the four companion paths threaded through
  `extract_proposal_row`/`extract_plan_row` and `_reconcile_artifact`, a
  decision about whether `templates/core/` is always Cairn's own
  self-hosted layout or something a `config.py` override could relocate
  (guessing wrong risks a false refusal on an adopter tree that happens to
  carry an unrelated `templates/core/` directory), and a new
  corpus-walk-level fixture proving the *real* `proposal_rows()`/
  `plan_rows()` path refuses on a synthetic divergence -- none of which
  exists today. Full writeup: the same code review section, finding CR3.

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

* **[TOOL] The lifecycle checker flags every Internal review as
  author-written, because the identity comparator takes the first word**
  *(filed 2026-08-20, from three concurrent Internal proposal reviews)* —
  `lifecycle_planner`'s independence check derives an identity token from the
  byline's first word. Cairn's Internal review floor is **"the same agent in a
  fresh session"** (`AGENTS.md` > Review), so an honest Internal byline is
  `Claude (Internal, fresh-context subagent)` against an author of
  `Claude (Strategy)` — same first word, and the checker reports:

  > `'## Review' at line N appears authored by the proposal author
  > ('Claude (Strategy)'); a review carries reviewer-authorship (independent
  > reviewer).`

  **The checker flags correct reviews by construction.** It fired identically
  on all three of `2026-08-20-claude-portable-sweeps-cannot-run`,
  `2026-08-20-claude-adopt-into-existing-tree` and
  `2026-08-20-claude-scanner-claim-scope` — reviews that met the Internal floor
  exactly. It cannot fire on an External review, because a different agent type
  has a different first word.

  **Two properties make it worse than a cosmetic false positive.** It clears
  once the author's Response lands *until a later review is appended beneath,
  which re-fires it* (observed 2026-08-20 across two External rounds; the
  original filing said only that it clears, which understated the window). So
  it is red exactly during the window a reviewer is waiting on the artifact — the moment someone is most likely to be
  reading the scan. And the cheapest way to silence it is to write a byline that
  is not the reviewer's, which is a **false attribution on a record whose
  integrity is its attribution** (`AGENTS.md` > Review). All three reviewers
  independently declined to do that and documented the flag instead; that was
  right, and a gate that rewards the wrong answer should not stay.

  **What is owed is a distinguishing comparator**, not a naming convention: the
  Internal floor is a statement about *context*, not about identity, so
  first-word identity cannot express it. Options worth weighing — compare the
  full parenthetical role rather than the first token; treat an explicit
  `(Internal, …)` marker as a declared-independence assertion the checker
  accepts; or drop the author-identity heuristic for Internal passes and rely on
  the tier declaration. **Not yet proposed** — it is a checker defect, filed for
  routing, and the fix touches lifecycle enforcement, which is governing
  doctrine and takes its own proposal.

* **[VER] ~~The AST attestation baseline needs re-anchoring after the tag pass~~ — CLOSED 2026-08-20, the work landed**
  *(filed 2026-08-19; Maintainer authorized the re-anchor over a revert; closed 2026-08-20 while preparing the differential-oracle re-anchor)* —
  **This row is answered and is kept only so a reader who arrives via a citation is not misdirected.** The re-anchor landed at `77d2b3b` ("install contract: record the Maintainer's supervised re-anchor of three artifacts"). Verified at HEAD on 2026-08-20 by running the tool rather than reading this row: `_ast_attest.py verify` reports **AST attestation OK — 173 baselined symbol(s) accounted for, unchanged**, and `test_ast_attest.py` passes.

  **Why it stayed open two commits past being true.** The row instructs a reader to *"derive the expected CHANGED set against the committed baseline rather than carrying the figure forward from this row — including from this row."* Following that instruction is what closed it. Nothing in the tree contradicts a stale roadmap entry, so the entry outlives its subject by exactly as long as it takes someone to re-run the measurement instead of reading the number.

  The original diagnosis, retained for the record:
  `bootstrap/tests/test_ast_attest.py` reports **13 CHANGED symbols**: 11 in
  `bootstrap/_scaffold/upgrade.py`, 2 in `bootstrap/_scaffold/config.py`.

  **Cause is prose, not logic.** Docstrings are AST nodes, so revising one
  changes the attested hash even though nothing executable moved. The pass
  edited 18 docstrings in `upgrade.py` and 5 in `config.py`; the ~987 comment
  lines in those two files are invisible to the AST and are not implicated.

  **Not self-serviceable.** `_ast_attest._UPDATE_ALLOWLIST` covers
  `_CORE_MAPPINGS`, `_MODULE_MAPPINGS`, `_SKILLS_MAPPINGS` and
  `install_onboarding` — none of the 13. `AGENTS.md` makes anything outside
  that list a **Maintainer-run, dry-run-verified direct correction that an
  implementing agent does not perform** (precedent `c3d5bd9`), so the
  implementing agent has left it alone rather than repairing it.

  **Procedure**: [`bootstrap/AST_BASELINE_RUNBOOK.md`](../bootstrap/AST_BASELINE_RUNBOOK.md).
  Derive the expected CHANGED set against the committed baseline rather than
  carrying the figure 13 forward from this row — including from this row.

  **Decision recorded**: the Maintainer chose re-anchor over reverting the
  docstrings. Reverting would have left 23 docstrings in the engine package as
  the only place in the tree still carrying dead coordinates, which is the
  never-finishes shape this plan exists to prevent.

* **[REC] Five plan-review sections owe three of the four basis fields**
  *(filed 2026-08-19)* — the Internal plan reviews in
  `comprehension-outlives-the-artifact.md` (lines 573 / 950 / 1319 / 1591 /
  1998) each carry `Reviewed commit` and none of `Target`, `Prior findings`,
  `Assurance path`. The four-field basis became mandatory at `76bc678`
  (2026-08-12), one day before those reviews, so the obligation was in force.
  `test_lifecycle_contract.py::test_the_live_corpus_is_sound_under_the_p1_contract`
  reported 19 violations; 15 remain after the heading fix below,
  and the file is red at HEAD.

  **The implementer cannot fix this, which is the point.** Those three fields
  are declarations by a reviewer about their own read. Filling them in is
  inferring another agent's basis and signing it — the failure the attribution
  rule exists to prevent — and the record is append-only besides. So this is a
  Maintainer call among three dispositions: **amend** the sections, **append**
  a correction naming the omission, or **accept** and let it clear when the
  plan archives (the scan globs `dev/plans/*.md`, live-only, so archiving
  removes it from the corpus without fixing it).

  **It blocks a second party.** The `ceremony-as-code` implementer cannot file
  a Boundary B record while the suite is red for reasons outside its change,
  and its Boundary B refuses bounded mode. Accepting the third disposition
  means that plan waits on this one's archive.

  **Four of the 19 were a second kind, and they were the author's defect, not
  the checker's** — fixed here, taking the count to 15. The disposition
  predicate compares a section's *kind* — the text before the first ` -- ` —
  exactly. Four Response headings read `## Response to plan review (round 2)
  -- Claude -- 2026-08-13`, putting the round marker inside the kind, so they
  parsed as four distinct kinds and none matched. Moving it after the date
  (`... -- 2026-08-13 (round 2)`) restores the canonical kind and disposes all
  four. Headings only; no finding or wording touched.

  Worth recording because **two agents independently concluded the checker was
  broken and it was right both times** — `ceremony-as-code` had drifted to
  informative heading variants (`## Response to the clearing review`), this
  plan had drifted to a round marker in the kind slot. Both drifts read as
  harmless formatting and both silently voided a conformance obligation. A
  format contract is most likely to be broken exactly where following it feels
  like pedantry.

* **[SEC] M2 conflates "review" with "produce", so a second clearing review
  manufactures a competing authority pair** *(filed 2026-08-19, from the
  `ceremony-as-code` M2)* — the plan's M2 row says *"the **reviewer** produces
  and self-records the launcher/packet pair"*, singular. It assumes one
  reviewer. **Two independent External Security reviews cleared round 2**
  (Antigravity and Codex), so two valid authority pairs now exist:

  | reviewer | packet | instantiated launcher |
  |---|---|---|
  | Antigravity | `c18c0a17…` | `391ceb9b…` |
  | Codex | `411bed01…` | `9c8cf374…` |

  **The review redundancy is a gain; the pair redundancy is a liability.** They
  cannot be *mixed* — each launcher carries its own packet's digest, so a
  cross-pair combination fails the binding check — but nothing says which pair
  is canonical, and nothing stops someone later finding the unused one and
  running it in good faith. Codex's was used at M3; Antigravity's was never
  delivered to disk and is void by circumstance rather than by rule.

  **What is owed is one sentence in the contract**, not a mechanism: a second
  clearing review confirms the same bytes and **produces no pair** unless the
  first is withdrawn. Cheap, and it removes the ambiguity entirely.

  **Filed because the archived plan is not a home.** The `ceremony-as-code`
  lasting-truth section named this observation and said *"filed rather than
  fixed here"* while its disposition block read `Dispositions: none` — an
  attestation that was accurate when written and false by the time the section
  around it grew. See the row below on the archive gate, which is the general
  form of that failure.

* **The lasting-truth attestation is written once and the section grows after
  it, and nothing re-checks** *(filed 2026-08-19, the general form of the M2 row
  above)* — a plan can archive attesting `Dispositions: none` while its own
  section names follow-ups in prose. Measured on `ceremony-as-code`: the
  attestation was accurate when written, three durable observations were
  appended below it, and the archive gate passed because it reads the
  attestation and never compares it to the section around it.

  **Two sentences in the instructions do most of the work.**

  1. *"Only `defer` needs a durable home outside the plan; the other
     dispositions **are** the home."* True for `accept` when a change actually
     landed — a commit, a comment, a test a reader will meet. **False for an
     observation**, where `accept` means nothing was written anywhere living
     and the plan is about to stop being read. The sentence invites reading
     `accept` as "no further action", which is right for a fixed bug and wrong
     for a durable truth.
  2. *"Filled in at archive time"* implies one moment, while
     *"append-only once written"* guarantees the section accretes. Nothing says
     **an append re-opens the attestation**.

  **Suggested wording, not applied** — this is `templates/core` doctrine and
  wants a decision rather than an edit in passing:

  * qualify the first: *"`accept` is the home only when the accepting change
    landed somewhere a reader will meet. An observation with no landing place
    is a `defer` and needs a row."*
  * add to the second: *"Appending to this section re-opens the attestation. If
    you add content, restate or amend the disposition line."*

  **Why prose rather than a mechanism.** The predicate already learned this
  lesson once — its own comment reads *"Presence of the label is never enough
  -- that is the defect this predicate exists to close."* The remaining gap is
  one level up and is a **consistency** question between an attestation and
  free prose, which a regex answers badly. The cheap honest fix is to tell the
  author when to look again.

* **[SEC] The lockfile has no regeneration procedure for an existing lockfile**
  *(filed 2026-08-19, found while executing the install-contract batch)* —
  `test_cairns_own_install_records_all_three_files_in_the_lockfile` states the
  rule in its own docstring: *"the lockfile is regenerated, never
  hand-edited."* **There is no command that regenerates an existing one.**
  `scaffold.py upgrade --init-lock` is the only writer, and it refuses when the
  file is already present — measured `as_of 2026-08-19`, run against a
  throwaway worktree copy: `[info] dev/.cairn/cairn-lock.yml already exists;
  nothing to migrate.`, **0 lines changed**.

  So a stale digest leaves an operator with two options the project forbids:
  delete-and-reinit, which discards the 89 records that were correct and
  rewrites `migrated`/`cairn_commit`/`profile` besides; or hand-editing, which
  is what the docstring rules out. **This is the `AGENTS.md` named-trigger rule
  failing on an artifact rather than a document** — *"a named trigger is
  checked by opening it and confirming the procedure is there"* — and it was
  invisible until someone needed the procedure, because the sentence reads like
  it describes one.

  **What was done instead**, so this row is not read as an open failure: a
  purpose-built correction script, dry-run-verified and Maintainer-applied at
  `77d2b3b`. It rewrites only records whose recorded digest disagrees with
  disk, and moves a verbatim record's `hash` *and* `base_hash` only after
  proving the installed file is byte-identical to its template. That script is
  a one-off in a scratchpad, deliberately: shipping it would answer the wrong
  question.

  **What is actually owed is a decision, not a script.** Either the writer
  grows a targeted refresh (a subcommand that re-records named files against
  disk, with the same byte-identical proof), or the test's docstring stops
  naming a procedure that does not exist and names the real one. The first is
  better; the second is the minimum. **Leaving both undone is the state that
  produced this row**: the instruction is followed by nobody and believed by
  everybody, and the next person to hit it will either hand-edit the install
  contract or delete it and start over.

* **[SEC] ~~Two install-contract artifacts are stale after the tag pass~~ —
  RESOLVED 2026-08-19 at `77d2b3b`.** The Maintainer ran all three corrections
  under supervision: the AST baseline (37 symbols, every one verified
  docstring-only against the baseline's own provenance commit before any
  write), the lockfile (37 of 90 records), and the gate manifest (141 digests).
  `_ast_attest verify` reports 173 baselined symbols **unchanged in count** —
  the runbook's check that a correction happened rather than a full re-pin.
  Every figure in the original row below was stale by the time it ran, which is
  why the runbook forbids carrying a delta forward. Kept for the record:
  *(filed 2026-08-19)* — `bootstrap/tests/fixtures/gate_manifest.json` has **35 frozen
  entries** whose bytes no longer match the tree, and
  `dev/.cairn/cairn-lock.yml` records a digest for
  `scripts/run_portable_security_sweeps.py` that disagrees with disk
  (`test_cairns_own_install_records_all_three_files_in_the_lockfile`, the one
  test that catches either).

  **Not a suite failure.** `test_gate_manifest.py` passes 21/0, because those
  tests `produce()` a fresh manifest and verify against that rather than against
  the committed fixture. Green suite, stale fixture — different things, and an
  earlier version of this row conflated them.

  **What needs deciding is narrow**: *who* regenerates the manifest and
  re-records the lockfile, and under what review. Coverage itself is a
  sequencing question — whatever the anchor is at ceremony time covers whatever
  is committed then — so this does not need another plan's scope widened. It is
  the same self-certification question as the interpreter re-pin above, on two
  more artifacts, one of which (`run_portable_security_sweeps.py`) is a named
  high-risk surface and the other of which is the install contract.

* **[SEC] The interpreter-binding re-pin at `c29ead3` — REPRODUCTION
  CONFIRMED 2026-08-19, tier question still open.** A second agent re-derived
  the docstring-stripped digests with its own stripper, on both twins, and got
  the three recorded values exactly; the edit is comment-only and none of the
  five gated properties changed. **What remains is not technical**: the
  re-derivation rode an implementing commit, while the pin's own text says to
  re-derive "in that review's own commit", and a same-agent-type confirmation
  is a second reading rather than an independent tier. Also still open: the
  `_has_symlink_component` coverage gap below — the fence pins the caller and
  not the callee, so a behavioural change to symlink detection would not redden
  it. Original row: *(filed
  2026-08-18 by the `comprehension-outlives-the-artifact` implementer)* — the
  four digests in
  `bootstrap/tests/test_lifecycle_brief.py::_INTERPRETER_SYMBOL_DIGESTS` were
  re-derived by an **implementing agent under explicit Maintainer
  authorization**, not by a Security Review. The pin guards the local
  interpreter binding, which `AGENTS.md` lists as a high-risk surface.

  The change was comment- and docstring-only and that is **shown, not
  asserted**: every pinned function digests identically on both sides of the
  edit once every docstring is stripped before `ast.dump` (`08856288621efb6f`,
  `92fdb64150ee4ef5`, `d5d3de3acd75a08b`) — reproducible against `c29ead3^`,
  method in `dev/measurement/tag-pass-dispositions.md`. None of the five gated
  properties (schema, validation order, fallback disposition, warning
  visibility, subprocess use) changed. **Independently reproduced** by the
  `ceremony-as-code` agent with its own stripper, on both twins, at three
  commits.

  **The edits were in `_has_symlink_component` (1 line, unpinned) and
  `_resolve_interpreter` (4 lines, pinned)** — an earlier version of this row
  named the wrong functions; one pinned pair was re-derived, which is correct
  and complete.

  **A second, sharper item rides here (pre-existing).** `_has_symlink_component`
  is *not* pinned, though its caller `_probe_interpreter` is — and a pinned
  digest covers the call, not the callee. `AGENTS.md` documents this trust
  root's reader as checking *"absoluteness, schema, symlink-freedom and the
  executable bit"*, and `_has_symlink_component` **is** the symlink-freedom
  check. So a behavioural change to symlink detection would not redden the
  fence. Nothing introduced this; a comment edit landing one level outside the
  boundary surfaced it. **This is the half with teeth.**

  **What is owed, and what is now settled.** The *technical* question is
  closed: the `ceremony-as-code` agent reproduced the result independently and
  confirmed no behavioural change. The *procedural* question is open and is the
  Maintainer's, for three reasons that agent named rather than waved past: it is
  **the same agent type**, so its confirmation is a second reading and not an
  independent tier; the pin's own text says to re-derive *"in that review's own
  commit"* and `c29ead3` is an implementing commit; and the authorization
  (*"we'll re-pin with the other agent"*) describes a second party at the
  re-pin, which is not the same thing as a Security Review. Treat that
  reproduction as **evidence for** a review, not as the review.

  **Worth a view while someone is in there**: a byte pin that trips on a
  docstring edit may be mis-scoped for what it protects. Not a proposal, an
  observation — the fence worked, but it cost a Maintainer decision over five
  comments.

* **The controlled re-anchor path cannot run for the ordinary case** *(observed
  2026-08-13 during the second real gate re-anchor; homed at goodnight because
  it belongs to no plan)* — there are two ways to move the gate's trust root, and
  neither fits routine work. The **controlled** path refuses unless the
  differential oracle has *run*, and that oracle only runs when a pre-refactor
  baseline is configured — i.e. **during an engine refactor**. It reports itself
  *"dormant between refactors"* and the promotion then refuses, because the
  refusal cannot distinguish *"the check failed"* from *"the check did not need
  to run."*

  So a re-anchor caused by ordinary churn — test files legitimately changing —
  has only the **establishment** path, which is documented as *"supervised,
  one-time"* and skips the authorization binding and the compare-and-swap that
  make the controlled path controlled. **Both of Cairn's real re-anchors have now
  gone through it.** A one-time procedure used twice is a routine procedure that
  nobody designed.

  **Do not close this by configuring a baseline to satisfy the check** — that
  declares a refactor that did not happen, which is fabricating evidence to stop
  a control objecting, on a trust root. The honest options are to give the
  controlled path a way to record *"no refactor, oracle not applicable"* without
  treating it as a failure, or to accept the establishment path as the routine
  one and give it the missing controls. *Trigger:* the next gate re-anchor, or
  any work on the re-anchor machinery.

* **The review-allocation pilot is built and reviewed, but has never been
  switched on** *(homed 2026-08-13, when the plan that built it archived)* — the
  machinery for measuring whether the lighter review allocation actually works
  is in the tree and under test: a record naming the exact reviewed commit the
  measurement applies to, an append-only ledger with one entry per plan counted
  or pause taken, and counts derived from that ledger rather than stored
  anywhere they could drift. Its mutation tests cover interrupted writes, a
  stale writer overwriting a fresher one, and the off-by-one at the window's
  final day. **None of it is running.** Two acts remain, and both are the
  Maintainer's — recorded here because the plan that owned them is archived, and
  an archive is a historical record rather than a work queue.

  **Switching it on — possible now, nothing blocks it.** One commit adds the
  activation record naming `089a9db` as the reviewed commit whose machinery is
  being enabled, and the 60-day window starts from that commit's author date.
  **That commit must contain data and nothing else**; if it carries code, the
  activation is wrong and should be rejected rather than amended. Until it
  lands the evidence report says *not installed* — deliberately, so an
  un-activated pilot can never be mistaken for a pilot that ran and found
  nothing.

  **Deciding what it showed — about 60 days after switch-on, and only if you
  want it.** The outcome is one of *keep the lighter allocation*, *change it*,
  or *drop it and go back*. It is a judgement about evidence, not a formality,
  and there is deliberately no "it worked" default. If that change touches any
  executable, test, template or fixture byte it takes fresh integration evidence
  and an independent code review of its own — it inherits nothing from the
  archived plan's runs, because those measured a different tree.

  **Why neither blocked the archive.** They are points where the plan was built
  to stop and hand over, not work it left undone: an implementing agent may not
  switch on the measurement of its own review budget, nor decide what the
  measurement meant. *Trigger:* whenever you want the window to start. The
  second follows about two months later, or never.

* **The loop-fidelity gate covers one folder out of several** *(homed 2026-08-13
  from `review-efficient-lifecycle` [CF9], at the Maintainer's instruction; that
  plan measured it and deliberately did not widen it)* — `check_cairn`'s
  `_CAIRN_INTERNAL_PREFIXES` is `('doctrine/',)`. The gate exists to stop a
  **shipped** `templates/**` surface citing a path that exists in Cairn's tree
  but not in an adopter's; with one prefix it catches `doctrine/` and nothing
  else, so a `bootstrap/`, `dev/plans/`, `dev/proposals/`, `dev/measurement/`,
  `case-studies/` or `dimensions/` citation dangles in an adopter tree and
  passes clean.

  **Measured, not inferred** (`review-efficient-lifecycle` [CF9], 2026-08-12):
  with `bootstrap/fidelity-check.md` and a `dev/plans/` path appended to a
  shipped surface, `check_cairn` printed `OK -- 1 Markdown file(s) scanned; no
  issues.` **There is at least one live instance today**: `templates/core/AGENTS.md`
  cites `bootstrap/fidelity-check.md` in its drift-guard paragraph. It predates
  that plan.

  **Why it was not fixed in passing, and what the first task is.** Widening the
  tuple changes a standing gate's verdict across the whole repository, and
  nobody knows yet how many currently-passing surfaces it would flag — one, or
  dozens. That count *is* the first task, and it decides the shape of the rest:
  a handful of real dangling citations is an ordinary fix; a large population
  means the widening needs staging, or a deprecation window like the one D4 gave
  the claim-check globs. Doing it as a side effect of an unrelated plan is how a
  standing gate changes behaviour without anyone reviewing the change.
  *Trigger:* the next change to `check_cairn`'s prefix set or to shipped-template
  citation policy — or sooner, since the live instance is already shipping.

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
  row is another hand-count of one plan. **That ledger shipped 2026-08-21**
  (plan `suite-run-diagnostics`, archived): the collector writes one row per
  top-level session to the gitignored `dev/measurement/suite-runs.jsonl`, and
  `tools/suite_cost.py` renders it without re-running anything. The dependency
  this row names is satisfied; what it still needs is elapsed time and rows.
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

* **Portable-security-sweeps deferred set (LT-1, LT-2, LT-4, LT-6)** *(homed
  2026-08-10 as that plan's archive precondition; LT-3 and LT-5 live in
  `dev/measurement/gitleaks-version-support.md`, and LT-7 was resolved outright
  when `AGENTS.md` began naming `bootstrap/AST_BASELINE_RUNBOOK.md` directly)* —
  four follow-ups the plan fenced out of its own scope. **LT-1 — preset
  selection.** The adoption amendment's five-row table (`collaborative-team` and
  `high-rigor-legacy` baseline; `solo-greenfield` opt-in; a Python team receiving
  *both* modules; `modules_remove` as the visible waiver; literal `modules:` lists
  staying exact) is unimplemented. Its home is a **new proposal** against the
  accepted `default-security-stance` selection contract, not this row alone: it
  edits `_PRESETS`, a symbol `_ast_attest._UPDATE_ALLOWLIST` does not admit, so it
  carries its own re-anchor accounting, and it changes what fresh adopters
  receive — Decision-bearing. *Trigger:* the next change to preset composition.
  **LT-2 — the activation registry row, and a naming-contract mismatch measured
  2026-08-10.** Chunk G took **Branch 2** (not landed), but not for the reason
  Branch 2 states: the dispatcher `run_security_verification.py` **does** exist
  (`6e3a8ed`). The real blocker is that `_selected_capability_ids` admits only
  module IDs ending in **`-security`**, and this module's ID ends in `-sweeps` —
  measured at `9724c0f`, the module *is* installed (16 in the lockfile) yet the
  dispatcher sees only `['content-security']`. A Branch-1 registry row would be
  **inert by construction**, and worse, Chunk G's required deletion mutant
  (`test_the_standing_command_includes_the_portable_leg`) **could not fail** — the
  row's presence changes nothing. **RESOLVED 2026-08-10 — Maintainer accepted the
  third option** (*"Accept on the LT-2"*): portable sweeps runs via its own
  standing command and **not** through the dispatcher, so this is a **permanent
  documented residual, not a deferral**, and it does not gate that plan's
  archive. The two rejected alternatives are recorded because the residual can be
  revisited: widening `_selected_capability_ids` (owned by
  `security-verification-activation`, and a trust-boundary change to what the
  dispatcher admits → Security Review), or renaming the module ID to end in
  `-security` (shipped ID + lockfile + three file paths → Decision-bearing).
  *Revival condition:* the filter widening riding along with that plan's
  registry-admission chunk, which is already unfenced — at which point the
  inert-row and vacuous-mutant analysis above is the evidence to re-read, **not**
  Chunk G's Branch 1 table, which assumes an effective row. **LT-4 — the three
  withdrawn adapters** (OSV-Scanner, zizmor, Trivy), named here as a set so they
  are not silently forgotten. Each arrives as its own proposal per the revision's
  rule: its own executable chain, ambient-config execution evidence, network
  posture, output schema, and offline-CLEAN disposition. This is **distinct from**
  the conda-advisory row elsewhere on this board, which cites Trivy and
  OSV-Scanner as *evidence about conda ecosystem coverage* — a different question.
  **LT-6 — the `.json`-under-`templates/` precedent.** The licence half landed
  (`bootstrap/DEPENDENCY_BUDGET.md`, `portable_security_policy.json` → MIT, no
  header, being a data asset with no comment syntax). The open question is whether
  `_self_hosted_twins()` should stop being `.py`-keyed; generalizing that helper
  changes a gate the plan does not own. *Trigger:* the second non-`.py` verbatim
  asset under `templates/`.
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
* **[TRU-7] the gate anchor is unpublished, and no document says to publish it**
  *(deferred 2026-08-05 from `release-security-orchestration`, which recorded the
  measurement out of its declared scope; mirrored in
  `2026-08-05-codex-security-strategy` > [TRU] as [TRU-7])* — `refs/cairn/gate-anchor`
  exists locally at `e45e1fc`; `git ls-remote origin 'refs/cairn/*'` returns nothing.
  **No ordinary push can publish it**: git's default refspec is `refs/heads/*`, so
  `refs/cairn/*` is skipped by `git push`, `git push origin master`, `--all` and
  `--tags`, and no `remote.origin.push` is configured. It takes an explicit
  `git push origin refs/cairn/gate-anchor:refs/cairn/gate-anchor`, plus a matching
  fetch refspec on the other side. **`bootstrap/REANCHOR_RUNBOOK.md` contains zero
  occurrences of `git push`** — it covers advancing the anchor locally and requires
  local write access to the ref, but never publication.
  `refs/cairn/gate-authorization` has the same gap. Consequence: the
  differential-oracle trust root is single-machine by construction, a fresh clone
  has no anchor, and recovering a lost one is a Maintainer ceremony under a runbook
  silent on how the anchor travels. A runbook gap, not a defect in the gate.

* **[REL-6] `SECURITY.md` disclosure channel** *(split out of `contributor-entry` by
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
  **Also carries the `README.md` pointer** that was part 3 of `contributor-entry`:
  `README.md` is the only entry-layer file a first-time visitor reliably reads,
  and a disclosure channel nobody can find from the front page is not a channel.
  Scoped to `SECURITY.md` only -- the `CONTRIBUTING.md` half of that pointer is
  declined with part 1.

* **Adopter-entry doc-refresh follow-ups** *(deferred, Jun 2026)* — the
  doc-refresh + prose↔runtime drift-gate shipped (plan
  `adopter-entry-doc-refresh`, archived; from the 2026-06-12
  adopter-friction audit). Two deferred follow-ups: (a) a context-aware
  scaffold **`--quickstart` mode** (richer than the "Next steps for a real
  adoption" reframe — let the scaffold print a trimmed next-step for the
  trivial path); (b) extend the `verify:` count guard to **other
  adopter-facing counts** beyond the quickstart's two. Each → its own
  proposal when revived.
* **[REC-3] Transition-lint** *(archived 2026-08-10)* — the **advisory**
  commit-message-vs-diff check shipped: plan `transition-lint`
  (`dev/plans/archive/transition-lint.md`), six implementation commits,
  External Antigravity code review (SHIP, 2026-08-10). Fence 1 (amending the
  Decision's pinned claim vocabulary) ratified the same day to a 10-finding
  posture over `57d1daf..8f47c76` — the corpus drifted from the proposal's
  0-false-positives pin (120 commits, 2026-07-22) to 20 false positives in
  332 commits nine months later, now `docs/tool-usage.md`'s own headline
  caveat. **The plan's still-owed second Internal plan-review round was
  never formally re-run**; the archive record's own disposition reads the
  External code review as substantively covering its brief at a stronger
  tier and flags that reading for the Maintainer's concurrence rather than
  asserting it closed. Deferred, each already homed rather than a new board
  row: adopter shipping (v2, a `lifecycle_metrics` subcommand — needs a
  second real tree's corpus); the 245-of-332 unaudited false-negative gap
  (stated, not measured, in `docs/tool-usage.md`); the dropped class-level
  `info` suppression layer (Fence 2, disclosed in `docs/tool-usage.md`). Each
  → its own proposal if picked up.
* **[TRU-1] Self-host lockfile reconciliation** *(deferred, Jul 2026)* —
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
* **[BND-6] Lockfile schema validate-on-read** *(deferred, Jul 2026)* — the
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

Substantive work currently in flight: open plans, executing
sub-tracks, in-progress proposals between Decision and
plan-open. When an entry completes, it is **removed** from this
section at the next goodnight scrub — the truth migrates to the
archived plan / proposal, the implementing commits, and the
changelog. There is no "completed recently" section on this
board by design.

* **git-native-security-foundations** *(plan opened 2026-08-11)* -- align
  Cairn's security boundary with Git's native object, signature, graph, and ref
  primitives: replace incompatible per-agent signing with Maintainer-signed
  checkpoints bound to a canonical range-review report, delegate blob ids and
  strict object validation to Git, migrate the frozen-file leg to Git object
  identity without dropping SHA-256 or losing collection semantics, add
  diagnostic reflogs, and publish only the durable gate anchor atomically.
  Eight chunks; `required(External + External Security Review)`. Four
  Maintainer stops, enumerated in the plan's own fence table, including a
  Maintainer-only exact-byte trust-root bootstrap that no agent performs.
  **Chunk D is fenced behind `review-efficient-lifecycle`'s Chunk I ceremony
  and B2** -- both plans touch the gate manifest, and this one migrates its
  schema.

* **review-efficient-lifecycle** *(plan opened 2026-08-10; **archived
  2026-08-13**)* -- one plan for the four accepted lifecycle contracts
  (`review-efficient-lifecycle` plus the `claim-check-exemption-hygiene`,
  `code-review-blindness`, and `lifecycle-status-vocabulary` amendments), which
  three of them require by their own accepted text. **Delivered**: sixteen
  implementation rows plus H1's retirement of the six legacy status tokens into
  the historical tuples, one clearing code review (Internal, delegated -- SHIP,
  eight findings, all answered), two Boundary B runs, and the Maintainer's gate
  re-anchor `cfaace9` -> `089a9db`.

  **Two things it did not deliver, both recorded rather than absorbed.** R3's
  legacy multi-obligation mapping over three archived plans was **withdrawn by
  the Maintainer** (quoted verbatim in the plan's `## Dispositions`) on the
  principle that archives are a historical record, not an active area. And the
  loop-fidelity gate's single-prefix gap is deferred to the Queued row above.
  The review budget it planned -- one Boundary B -- became two, because the
  re-anchor rewrote the gate manifest inside the reviewed range and the runbook
  runs no tests.

* **lifecycle-status-vocabulary** *(accepted 2026-08-10; **proposal archived
  2026-08-12**)* --
  make proposal and plan status name the next responsible action: explicit
  review, revision, implementation, Decision, and archive-readiness states;
  orthogonal blocker metadata; evidence-backed transitions; and an
  evidence-derived migration. Accepted and **executing inside** the
  `review-efficient-lifecycle` plan (Chunks A, E, F); the archived proposal
  remains the authoritative contract.

* **claim-check-exemption-hygiene** *(accepted 2026-08-10; **proposal archived
  2026-08-12**)* --
  keep claim-check's useful path discipline while retiring exemption clutter:
  resolve exact lifecycle archive moves, make typed path declarations reusable
  and auditable, fail stale active exemptions, and stop copying inert internal-
  reference headers into Cairn's self-hosted deliberation artifacts.
  Accepted and **delivered** by the `review-efficient-lifecycle` plan's Chunk D
  (`4723107` D1/D2/D5, `6869022` D3/D4); the archived proposal remains the
  authoritative contract.

* **Security program — clustered current view** *(living strategy opened
  2026-08-05)* — the canonical taxonomy, threat posture, sequencing rules and
  cluster exit conditions are in
  [`strategy/2026-08-05-codex-security-strategy.md`](strategy/2026-08-05-codex-security-strategy.md).
  This table is the roadmap view: lifecycle artifacts own design detail, and
  the residual rows farther down retain their original evidence and triggers.

  | Cluster | Current lifecycle owners | Next boundary |
  |---|---|---|
  | **[BND] Input, execution, containment** | `api-web-security-modules` (`fork-advisory-semantics` archived 2026-08-10, SHIP) | profile-authority consolidation; Class C no later than v0.4 preparation |
  | **[VER] Verification and coverage** | `security-verification-activation`; `api-web-security-modules` | `content-scan-detectors` + `separator-detection` archived 2026-08-10 (both SHIP-reviewed), `security-preflight-checklist` archived 2026-08-10 (SHIP; its broad-run evidence is implementer-supplied, see its archive record), `portable-security-sweeps` archived 2026-08-10 (SHIP on the CR1-CR3 correction round; Chunk G took Branch 2 and did NOT land -- see LT-2): reconcile the live frozen-file union and run one supervised re-pin over `content_scan.py` + `test_content_scan.py`, batched per both plans' Maintainer fence; then repair the two portable-sweep code-review findings |
  | **[TRU] Trust roots and provenance** | `fork-advisory-semantics` archived 2026-08-10 (SHIP); the live gate-reanchor posture below | trusted-source boundary after the release bar settles required source/install claims |
  | **[REC] Deliberation authority, identity, context, record integrity** | `code-review-blindness` (proposal, 2026-08-10); byline residuals below — `review-gate-enforcement` **archived 2026-08-10** (SHIP, no findings; its two residuals owned by that proposal) | one identity-authority consolidation when a trigger fires, not one proposal per Unicode row |
  | **[REL] Release evidence and ceremonies** | the landed Maintainer-run release command; the scheduled frozen-file union (`release-security-bar` **archived 2026-08-10** -- audited REVISE, all three pre-archive blockers discharged; residuals in the *Release bar (v0.5)* group) | serialize the SHIP-reviewed release register; derive every ceremony from the live held set, then run one reviewed supervised union |

* **[TRU-5] gate-reanchor-preflight posture** *(plan archived 2026-08-03; this entry
  survives because its commitments are live, not completed)* — the trust root is
  established at `cfaace9` *(re-anchored 2026-08-13; previously `e45e1fc`)* and
  the pre-flight is in the anchor, so every ceremony from here runs the anchored
  loader. What remains open is the **dated
  threat-model posture**: Cairn accepts a *trusted-contributor* model for its own
  trust root, **single-maintainer, as of 2026-08-03** — not a standing
  assumption. Its mechanical expiry is **the Maintainer's signature on a
  checkpoint whose message binds the canonical range-review report digest**,
  verified against the roster read from the anchor.
  *(Corrected 2026-08-13: this entry previously named a per-commit "signing
  epoch" tripwire at `a07fac8`. That mechanism was **retired**, not renamed —
  the epoch constant lived in the tree being blessed, so a candidate could move
  the line deciding which of its own commits were exempt, and refusing unsigned
  agent commits contradicted the normal workflow badly enough that operations
  disabled it. A control routinely disabled is not a control. Authorization now
  happens in exactly one place: the signed checkpoint. The per-commit census
  survives as diagnostics inside the range report and is never a verdict.)* *(Corrected at archive: this entry previously
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

* **[REC-1] byline-classification residuals** *(plan open 2026-08-03; the rows land at
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

The detailed rows below preserve their original migration provenance and
reproducers; this index supplies the operational organization. A new security
finding receives one primary cluster, one owner or revival trigger, and one
decisive evidence path. Sharing a source plan or the word "security" is not a
reason to open another scope.

| Cluster | Detailed homes in this board |
|---|---|
| **[BND] Input, execution, containment** | queued Class C; lockfile schema validate-on-read; interpreter race; scaffold/engine path residuals; `fork-advisory-semantics` identity-warning, `base_hash`, and `_infer_init_lock_axes` rows; profile G1/G2/G3/G5/totality rows |
| **[VER] Verification and coverage** | Security apparatus conda row; Scan coverage SC1-SC3; shipped-executable authority unification; cross-language conformance fixtures; capability plans in the Active table |
| **[TRU] Trust roots and provenance** | self-host lockfile reconciliation; install-integrity anchor; end-gate frozen-set decision; attestation kind-prefix validation; AST re-anchor runbook; Release authenticity RA1/RA3/RA5/RA6; fork advisory FA-R1; gate-reanchor posture |
| **[REC] Deliberation authority, identity, context, record integrity** | lifecycle mutation/commit arm, dogfood study, and later routine skills; transition and planner conformance; byline residuals and four archive follow-ups; gate-claims archive-auditability rows; lifecycle text-boundary follow-ups; `review-gate-enforcement` **archived 2026-08-10**, its code-review-blindness and synthesized-pass-ceiling residuals owned by the `code-review-blindness` proposal |
| **[REL] Release evidence and ceremonies** | SC4 and all stale frozen pins; profile G4 and manifest delta; release-authenticity archive/Zenodo rows; gate-claims trigger/CI rows; disclosure channel |

The strategy is the cluster authority; this board remains the task and trigger
authority. Completed rows leave this file at their lifecycle serialization
point rather than being copied into another backlog.

**Lifecycle apparatus**
* **Security-preflight residuals (R1-R6)** *(deferred, Aug 2026; plan
  `security-preflight-checklist` archived 2026-08-10)* -- the five-question
  preflight block ships declared-unenforced, and these are its named expiry
  triggers. **R1**: plan templates carry a clause, not the block, so a
  security-touching plan whose source proposal predates the change inherits no
  answered block -- trigger is the first such plan. **R2**: the
  security-touching gate is self-judged; nothing checks an "N/A" line --
  trigger is the *second* review that finds a security-touching change which
  wrote one. **R3**: nothing mechanical fires at all; enforcement is a reviewer
  declining to review an unanswered block -- trigger is the `transition-lint`
  proposal landing a lifecycle linter with somewhere cheap to add a presence
  check. **R4**: five shapes, not all shapes -- trigger is the first security
  finding that fits none of the five, at which point the shape has an instance
  and the recurrence limb applies to adding it. **R5**: the parity test pins
  only the added sub-block, while the whole `Author-accounting` block is
  byte-identical across both twins today -- trigger is the first legitimate
  divergence inside that block (a `cairn:slot` added to one side), which is the
  moment to decide whether the wider invariant is worth asserting. **R6** *(added
  by that plan's amendment A-14)*: a plan's bare `## Plan review` container
  satisfies `_has_kind` on presence, so the review-before-implement gate reads
  satisfied with **zero reviews landed**; measured `_has_kind -> True` against
  the plan as opened at `4020b76`. R6's durable owner was
  `review-gate-enforcement`, **which archived 2026-08-10 at `be42ba6`** -- so the
  trigger is named here rather than left to die with it: revival is the next
  change to either plan template's review container. Ritualization recovery (cut
  to S1 and S2) fires on either of two `git grep`-able signals: three
  consecutive proposals whose S1-S5 answers are byte-identical to a prior
  proposal's, or any proposal answering all "N/A" while its own `Touches` line
  names a surface `AGENTS.md` lists under *High-risk surfaces*.
* **[REC-3 / VER-3] Implementation-verification record conformance** *(deferred
  2026-08-05 from `verification-evidence-boundaries` External finding [E1])* —
  the v1 contract instructs authors to append a dated, field-complete record
  only after the stable Boundary B run, but lifecycle parsing does not prove the
  section is nonempty or schema-complete. Trigger: the first malformed record
  that reaches code review, or the next lifecycle-parser conformance expansion.
  A successor must validate the settled record schema without mistaking heading
  presence for evidence or rewriting append-only history.
* **[REC-3] Structural line-reader follow-ups** *(plans
  `planner-line-semantics` and `agent-context-scrub`, archived 2026-08-05)* —
  three measured edges share one home: `_gitignore_status` still uses
  `splitlines()` on `.gitignore` membership before its repair write; 25 class-D
  `splitlines()` sites in onboarding, intent, lifecycle-metrics, and evolution
  were audited as non-authoritative and need no speculative rewrite; and the
  two private CR/LF helpers have behavioral test parity but no textual-parity
  gate. *Triggers:* the next gitignore-repair change; a class-D site becoming an
  authority/structure reader; or a change to either private helper.
* **[BND-4 / REC-2] Relayed sub-tool stream boundary** *(deferred by
  `agent-context-scrub`, 2026-08-05)* — session routines relay structured stdout
  from intent, metrics, and evolution tools. Newline is legitimate data there,
  so field escaping cannot establish the same one-line authority boundary as it
  does for filenames and git metadata. A successor must define framing and
  trust for relayed tool output before changing bytes. *Trigger:* the next
  session-stream format change, or a demonstrated forged `lifecycle:` line from
  one of these relays.
* **[BND-4] CRLF-pairs-only relay contract** *(accepted guard from
  `agent-context-scrub`, 2026-08-05)* — `_git` normalizes CRLF pairs before
  escaping, but a lone CR remains payload and must not become a line ending;
  splitting on `\r\n|\r|\n` reopens the reproduced author-name forgery. The
  regression tests are the guard. *Trigger:* any change to `_git` decoding,
  `_safe_stream`, or Windows line-ending handling.
* **[REC-5] Lifecycle mutation/commit arm** — the typed-mutation ops (decision /
  review / open / archive) + commit the read-only planner deferred; gated on
  the dogfood study *and* its own Security Review (commit is a separate
  privilege; print-the-command in v1).
* **[REC-5] Lifecycle mechanization dogfood study** — the multi-session,
  Maintainer-run measurement that earns (or declines) the mutation arm; rank
  by prevented-failure / preserved-assurance, not frequency.
* **[REC-3] Planner cross-checks** — `next` surfaces "review status undetermined" on
  an absent/malformed plan-review line (E-#1); assert the artifact resolves
  under `dev/` (E-#2).
* **[REC-3] `_agent_of` round-suffix regression test** — pin the `## Review (Round
  N)` header shape in the Cairn tree.
* **[BND-3 / TRU-5] Interpreter trust-root check/use race (S2)** *(deferred, Jul 2026)* —
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

**[BND] Scaffold / engine**
* **[BND-3] Facade-loader symlink hardening (C-#3)** — refuse any engine submodule
  that is a symlink or resolves out-of-tree, across all three facades.
* **[TRU-4] End-gate frozen-set decision (C-#4)** — whether the A/B/C engine
  packages fold into the gate manifest's `frozen_files`.
* **[BND-3] Facade failed-load cleanup (B-#1)** — clean a partial
  `sys.modules` entry on a failed mid-load.
* **[TRU-4] Attestation kind-prefix validation (B-#2)** — reject a mismatched
  `<kind>:` prefix in `_ast_attest`.
* **[BND-3] Side-door non-executable surfaces** — disposition for the onboarding
  activation log, preset sources, and issue-capture forge starters.
* **[BND-3] Module destination renames / binary module files** — relocation
  classification when a module's destination changes; byte-preserving staging
  for non-text module files.

**[TRU / VER] Security apparatus**
* **[VER-3] A security test whose oracle is elapsed time fails open**
  *(found 2026-08-19 by adversarial review; confirmed independently by a second
  session; neither owns the file, so it is filed rather than fixed in passing)* —
  `bootstrap/tests/test_security_stack.py`,
  `test_a_t6_descendants_do_not_outlive_the_timeout`. The test spawns a
  SIGTERM-ignoring grandchild that sleeps 3s then writes a sentinel, forces the
  parent's timeout to 1.5s with a 0.5s kill grace, sleeps 4s, and asserts the
  sentinel does not exist.

  **The oracle is *absence of a sentinel within a window*, and absence has two
  causes it cannot distinguish**: the grandchild died — the property holds — or
  the grandchild is merely slow, in which case the property is violated and
  unobserved. Nominal timing puts the write at T≈3 and the check at T≈6, so the
  verdict rests on about **three seconds of scheduler luck**, and the failure
  direction is the harmful one. A saturated machine does not make this test
  flaky; it makes it **quietly green** — a security test reporting success
  without testing its property, which `AGENTS.md` names as worse than no test
  because it is silent.

  **The design intent was sound and should be preserved.** The comment states
  the oracle is deliberately the grandchild's own observable side effect rather
  than "any status this code returns" — that judgement is right. The defect is
  the *choice* of observable, not the philosophy.

  **Its neighbour is the instructive contrast.**
  `test_a_t2_timeout_is_enforced_and_bounded` asserts `elapsed < 10` against a
  ~2s nominal, so load pushes it toward failure: it fails **closed**. The pair
  reads as uniform and is not, so a reader who checks one and generalises gets
  the wrong answer about the other.

  *Fix direction:* assert on process state rather than elapsed time — a signal-0
  probe or `waitpid` on the process group turns *"I did not see it"* into *"it is
  not there"*. Note this is a real change, not a one-line swap: the fixture does
  not surface the grandchild's pid, since the grandchild is spawned by a
  `subprocess.Popen` inside a generated child program.

  *Generalises:* any other time-window oracle in the suite has the same defect,
  so the fix should be written as a claim about what makes a security test
  trustworthy, not as a local patch.

  *Trigger — and this is the load-bearing one:* **any evaluation of parallel test
  execution must fix this first.** Today the silent pass is rare; under `pytest
  -n auto` it becomes routine, and the evaluation would be reading a green
  security test that is not testing anything. Fixing it edits a gate-frozen file,
  so it **joins the re-anchor ceremony already owed** rather than creating a new
  obligation — alongside the AST attestation baseline (`191fb93`), the
  interpreter-binding re-pin confirmation (`017b2f2`), and the two stale
  install-contract artifacts (`fbd34ed`).
* **[TRU-4] The trust apparatus is protected by a glob, not by being named**
  *(found 2026-08-19 by an adversarial review of a proposed fence narrowing;
  not yet proposed)* — sixteen files that decide whether the gates pass are
  gate-frozen under the blanket `bootstrap/tests/**/*.py` glob:
  `bootstrap/tests/conftest.py`, `_gate_manifest.py`, `_gate_preflight.py`,
  `_gate_reanchor.py`, `_ast_attest.py`, `_oracle.py`, `_oracle_activation.py`,
  `_oracle_trust.py`, `_loader_proto.py` and their `test_*` counterparts. Of
  these, **only `test_ast_attest.py` is named anywhere in `AGENTS.md` >
  "High-risk surfaces"**, and only in the operational-pitfalls sense of
  re-anchoring its baseline. `conftest.py` is the sharpest case: it carries the
  release-mode outcome rule that refuses a skip as release evidence and can set
  `session.exitstatus`, and it is named nowhere.

  **Why this is a gap rather than a redundancy.** The verification fence refuses
  bounded mode on a "contract surface", and the *broad* reading of that phrase —
  frozen glob membership counts — is currently the only thing forcing a full
  suite when someone edits the release-mode rule. That reading is contested:
  two reviewers took opposite positions on it within one week
  (`scope-reduction-trap.md:3005` declared bounded and was accepted;
  `review-efficient-lifecycle.md:3719` states frozen paths are a contract
  surface "on which bounded mode refuses on its own terms"). The narrow reading
  is defensible — 129 of the 203 frozen files are simply every `.py` under
  `bootstrap/tests/`, so the broad reading makes bounded mode dead text for
  nearly any change. But adopting it would remove the *only* protection these
  sixteen files have, because none of them is independently named.

  So the fence is doing security work **by accident**, and the argument for
  narrowing it is sound on its own terms. *Ordering matters and is the whole
  point of this row:* enumerate the trust-apparatus files as named
  trust-ceremony surfaces **first**, land that, and only then reconsider the
  glob reading — never the reverse. A narrowing that lands first opens the fence
  widest at exactly the files it exists to protect.

  *Trigger:* any proposal to narrow or clarify the contract-surface fence, or
  the next Security Review that reaches `bootstrap/tests/`. Related: the
  repo-root `conftest.py` row above — both are cases of the frozen set's
  coverage being assumed rather than stated.
* **[TRU-4] The frozen set does not cover a repository-root `conftest.py`**
  *(found 2026-08-19 while scoping suite-cost instrumentation; not yet
  proposed)* — `_frozen_files` in `bootstrap/tests/_gate_manifest.py` discovers
  the frozen surface from five globs: `bootstrap/*.py`,
  `bootstrap/tests/**/*.py`, `bootstrap/tests/fixtures/**/*`, `scripts/*.py`,
  and `templates/modules/**/*.py`. A `conftest.py` placed at the repository
  root matches none of them, yet pytest loads it on every invocation this
  project actually uses. Verified by probe on 2026-08-19: a root `conftest.py`
  printing from `pytest_configure` fired under both `pytest
  bootstrap/tests/test_python_floor.py` and `pytest bootstrap/tests`, with
  `rootdir` resolving to the repository root; the probe was removed immediately
  and never committed. This matters because `bootstrap/tests/conftest.py` **is**
  frozen, and for precisely the reason that applies here — a conftest defines a
  gate's pass/fail semantics, and that file carries the release-mode outcome
  rule that can set `session.exitstatus`. A root conftest has the same power
  over the same session with none of the coverage, so the frozen set currently
  asserts an authority it does not hold. Adjacent surfaces share the shape and
  each needs its own disposition rather than being assumed in or out: a root
  `pytest.ini` / `pyproject.toml` / `tox.ini` / `setup.cfg` — **none exists
  today**, so the suite runs with no ini file and an inferred `rootdir`, and
  adding one would presently be an unreviewed act — and the `PYTEST_PLUGINS` /
  `PYTEST_ADDOPTS` environment variables, which cannot be frozen but whose
  absence a release run could assert. *Trigger:* the next change to the
  `_frozen_files` globs, or sooner — this is a live gap, not a latent one.
  Closing it edits `_gate_manifest.py`, itself frozen, so the fix costs a gate
  re-anchor; scope it to be worth that. Related: the end-gate frozen-set
  decision under **[BND] Scaffold / engine**, which asks the same authority-set
  question about the engine packages.
* **[TRU-4] `--noconftest` silently disables the release-mode outcome rule**
  *(found 2026-08-20 while planning the broad-run cost guard; Maintainer
  directed it here rather than into that plan, which keeps the accepted
  probe-only treatment)* — `pytest --noconftest` skips loading
  `bootstrap/tests/conftest.py` entirely. That file does not only hold test
  fixtures: it carries the **release-mode outcome rule**, which refuses a
  release when a security gate *skipped* rather than passed. Its own docstring
  states the reason — a suite that exits 0 after a skip is not acceptable
  release evidence. So a single flag turns off a release trust control, and the
  suite still exits 0. Verified 2026-08-20: `noconftest` appears **nowhere** in
  the tree outside the deliberation record — not in `AGENTS.md`, not in
  `bootstrap/SAFETY.md`, not in any docstring — so nothing warns a reader, and
  nothing asserts its absence on a release run.

  **Why this is filed rather than fixed in passing.** The exposure predates the
  cost guard by as long as the outcome rule has existed; the guard only made it
  visible, because a guard creates the first population of people motivated to
  get *past* a refusal. That is also why the fix is not "document the flag": a
  note reading "`--noconftest` bypasses the guard" would advertise the release
  control's off-switch to exactly that audience. If anything is written, it
  belongs with the release trust surface and must lead with what else the flag
  disables — `CAIRN_FULL_SUITE=1` is the supported override and leaves every
  other control intact.

  **The candidate mechanism, not yet weighed.** A release run could assert its
  own conftest was loaded — the same shape as the `PYTEST_PLUGINS` /
  `PYTEST_ADDOPTS` absence assertion the row above already contemplates, and
  probably the same disposition. Whether that is worth the gate re-anchor it
  would cost is the open question. *Trigger:* the next release-gate change, or
  any work on the row above — the two share a mechanism and should be weighed
  together rather than closed separately.
* **[VER-4 / TRU-3] Dependency-advisory evidence tightening** *(deferred
  2026-08-05 from `dependency-advisory-coverage`)* — v1 reports the complete
  validated partition for each run but stores no integrity-covered residual
  baseline for run-over-run diffs. Its OSV source claim also relies on
  pip-audit 2.10.1's default endpoint constant rather than an explicit
  `--osv-url` argv pin; the closed child environment prevents ambient override.
  Trigger: a requirement for historical drift evidence, a pip-audit version
  bump, or any widening of the pinned-source claim. A successor must bind the
  baseline into the install/integrity contract rather than trust an adjacent
  editable file.
* **[BND-3] Security-runner resource containment** *(deferred 2026-08-05 from
  `dependency-advisory-coverage`)* — POSIX timeout cleanup now kills a surviving
  process group, but Windows descendant cleanup remains unverified and child
  disk growth is not bounded. Trigger: Windows support for this runner, adding
  a tool that writes candidate-controlled volumes, or the first cleanup/disk
  incident. Keep these as containment limits, not advisory-parser defects.
* **[VER-4] Cairn security-check integrity preflight** *(deferred Aug 2026 from
  `default-security-stance`)* — `run_security_audit.py` refuses to run when its
  apparatus or policy inputs are not lockfile-clean; Cairn's own
  `bootstrap/security_check.py` has no equivalent preflight. Do not adopt the
  Python module sideways: define the authority for the checker's own bytes and
  policy inputs, then fail closed before any security phase executes when that
  authority disagrees.
* **[VER-3] Generated module-catalog parity** *(deferred Aug 2026 from
  `default-security-stance`)* — derive or executable-check the module catalog in
  `templates/modules/README.md` against `_MODULE_MAPPINGS`,
  `_DEFAULT_ON_MODULES`, and token-gated selection. The current hand table omits
  default-on and team-gated modules. Include the preset roster comments and
  `docs/solo-legacy-recipe.md` in the same catalog-wide design so the next
  selector change cannot make those descriptions stale independently.
* **[VER-3 / BND-3] Vendor-wrapper scan-root discovery** *(deferred Aug 2026 from
  `default-security-stance`)* — `content_scan_roots.txt` names optional wrapper
  filenames by hand, so a new vendor wrapper can go unscanned. Prefer deriving
  the installed wrapper path from trusted lockfile state; retain the current
  fail-closed handling for missing required roots and option-shaped roots.
* **[TRU-1] Install-integrity trust anchor** — `bootstrap/verify_integrity.py` reads
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
* **[TRU-1b] The doctrine overstates what the integrity check can promise**
  *(homed 2026-08-10; the claim-side twin of [TRU-1] above, which owns the
  tool-side gap)* — two adopter-facing files assert a property the tool cannot
  deliver. `doctrine/runtime-contract.md:132` lists the integrity check as
  core/Required and describes it as *"Detects tampered apparatus before it can
  self-audit; fail-closed"*; `SECURITY.md:51` carries a matching overstatement.
  Measured: a **coordinated tamper — rewrite the covered files, then regenerate
  the lockfile over them — returns exit 0, `OK`, with the marker byte still on
  disk**, for both checked record types, while the untampered-lockfile control
  correctly returns exit 1. **Enforcers: none.** This is not really an algorithm
  defect: no unsigned hash check *can* survive an attacker who rewrites both the
  bytes and their recorded digest — which is exactly the strategy's design
  principle 1 (*"A digest next to the bytes it covers is corruption detection,
  not tamper evidence"*). The defect is the **claim**. *Revival condition —
  either half discharges it:* narrow both sentences to what a lockfile-backed
  preflight can actually promise, **or** land [TRU-1]'s verbatim-subset
  anchoring, after which the claim becomes true for that subset and the wording
  should say which subset. **Why it is here and not escalated only:** the
  `release-security-bar` plan routes NOT MET rows to the Maintainer as
  release-blocking and explicitly *not* to this board — but "escalated" names a
  recipient, not a durable home, and the archive precondition requires a home.
  Its own End-of-Line Audit (2026-08-10, Antigravity, External) recorded this
  row as *"unowned by any active plan"*, so without this entry it would archive
  into a closed document. [TRU-1] already homes the tool half; this homes the
  claim half. Maintainer direction: *"move that to NOT MET row to PLANNING.md"*.
* **[VER] The detached-checkout guard counts `__pycache__` as unexpected
  content** *(deferred 2026-08-11 from `scope-reduction-trap`'s Boundary B)* —
  `bootstrap/tests/test_security_check.py::test_detached_checkout_excludes_an_ignored_pytest_override`
  fails with `_RepoStateError: detached checkout does not contain exactly the
  committed paths (missing=[], extra=['bootstrap/tests/__pycache__/…pyc', …])`.
  Compiled bytecode caches are not committed content, so the containment guard
  in `bootstrap/security_check.py` reports them as `extra`. **Reproducer:**
  fails in the main checkout, and in a clean `git worktree` at `6a4b3a0` — the
  commit *before* the source plan opened — so it predates that work; it passes
  only when the tests' generated `__pycache__` directory happens to be empty,
  which means it
  is effectively always red for anyone who has run the suite before.
  **Sharper diagnosis (External review, 2026-08-12):** the failure is
  *environmental, not a byte defect*. All three standing failures — this one and
  the two `TestLoaderContainmentMatrix` nodes — reproduce when Python writes
  bytecode and **clear entirely under `PYTHONDONTWRITEBYTECODE=1`**
  (independently reproduced: 3 failed → 31 passed). So the successor's first
  question is narrower than first recorded: whether the guard should ignore
  bytecode caches, or whether the suite should stop writing them. **Why it
  is not `wontfix`:** it reaches no adopter, but it leaves a permanently red
  node in every future Boundary B record, which degrades release evidence — the
  eligibility rule bars `wontfix` for anything release-blocking. **Why it was
  not fixed in place:** the two candidate fixes sit on different surfaces —
  relaxing the guard touches a named Security-Review surface
  (`AGENTS.md` > "High-risk surfaces"), while making the test arrange a
  pristine checkout does not. Choosing between them is the successor's first
  question, and the guard's strictness is plausibly the point. *Trigger:* the
  next change to the containment guard or its callers, the next release sweep
  (lens D, test & verification health), or any Boundary B run whose record
  would otherwise carry this as a standing non-pass.
  Maintainer authorization: *"And with the detached-checkout guard, go ahead
  and file that as a dev/PLANNING.md item"*.
**Release bar (v0.5)** *(group created 2026-08-10 at `release-security-bar`'s
archive; the plan's Lasting-truth table pre-declared this home, and its
End-of-Line Audit cited it as already existing when it did not — so it is created
here rather than assumed)*

* **[RB5-1] The register's coverage gap — enumerated, and re-derivable.** The bar
  adjudicated ~25 surfaces; its own declared scope contains substantially more,
  and the surplus has **no register row**. The plan measured this as a *count*
  (49 at `6912d52`, or 52 under a wider independent leg) and never enumerated it;
  the External Audit ruled *"counted-not-enumerated is NOT adequate for
  archive."* **The count is a moving target — it read 49 this morning and 69 this
  afternoon** at `32a7b8e`, because the tree grew (`api-web-security-modules`
  alone added 6 `templates/**/*.py`). So this row records the **producing
  command**, not the number, following this board's own precedent for derived
  lists:
  ```python
  # independent leg  =  Set 3 claim-bearing docs  ∪  every templates/**/*.py on disk
  # surface list     =  the committed H2 extraction over the register's Chunk RUN cells
  # gap              =  independent leg − surface list
  PATH_RE = re.compile(r"`([A-Za-z0-9_./-]+\.(?:py|sh|md|json|yml))(?::[0-9]+)?[^`]*`")
  runs    = re.split(r"^#### Chunk [A-H] — RUN", plan_text, flags=re.M)[1:]
  surface = {m.group(1) for c in runs for m in PATH_RE.finditer(c) if (root/m.group(1)).is_file()}
  ```
  **Shape at `32a7b8e`, under a wider-than-faithful independent leg (all
  `templates/**/*.md` + `dev/modules/*.md`, stated so the figure is reproducible
  rather than authoritative): 69 = 59 `templates/modules/**/*.py` + 7
  `dev/modules/*.md` + 3 others** (`templates/core/dev/plans/_template.md`,
  `templates/core/dev/proposals/_template.md`,
  `templates/skills/session-end/SKILL.md`). The seven `dev/modules/*.md` are
  `coordination-tiers`, `dual-review`, `fold-back-active-prompt`,
  `fold-back-ledger`, `foldback_export_scan`, `incident-trackers`,
  `lifecycle-metrics`. *Revival condition:* a v0.5 bar, which starts by re-running
  the command above rather than trusting any figure in this row.
* **[RB5-2] Set 3 quantifies over a static candidate-path list, not a tree walk.**
  Its positive control catches a planted `templates/**/*.py` but **not** a planted
  adopter-installed Markdown security claim, because `A30(ii)` defines Set 3 by a
  fixed list. The Audit ruled this **acceptable for v0.4.0 as a recorded
  residual** — so the residual has to actually be recorded, which is this row.
  *Revival condition:* expanding the independent leg to a dynamic traversal, which
  is what makes the coverage assertion self-maintaining.
* **[RB5-3] The five proposal-level v0.5 deferrals**, carried from the plan's
  Lasting-truth table: token-substituted lockfile anchoring; non-test derived-list
  integrity; extending the bar to Cairn's own dev tooling (including the
  `check_cairn` coverage gap); mutation testing as a standing mechanism; and
  cryptographic attestation. Each returns with a v0.5 bar. The second of these is
  the general form of **[RB5-4]**.
* **[RB5-4] B6's reach table is unpinned** — no test keeps it in step with preset
  composition, so it can go stale silently. *Trigger:* the first time it is found
  stale by the staleness command, **which has its own defect** — see [RB5-5].
* **[RB5-5] The staleness command can report FRESH when it matched nothing.**
  `git log -1 --format=%cI -- <surface list>` with an unquoted list under zsh
  passes one multi-word pathspec, git matches zero paths, and exit 0 with empty
  output is indistinguishable from "no commits since the audit". Audited severity:
  **MEDIUM (operational tooling hazard)** — this is the mechanism that decides
  whether a release tag waits. *Fix:* explicit array expansion
  (`"${surfaces[@]}"`) plus a non-zero-match assertion over the surface set, so an
  empty match is an error rather than a pass.
* **[RB5-6] The staleness surface list contains a path it is structurally blind
  to, and that path is an executable trust root.**
  `dev/.cairn/local-env.json` is in the register's own derived surface list and is
  **untracked and gitignored**, so `git log … -- <that path>` returns empty **for
  all time** — it can never signal staleness, however the pathspec is quoted. This
  is **not** the same defect as [RB5-5] and quoting cannot fix it: [RB5-5] is a
  *malformed-invocation* hazard, this is a *tracking* hazard. On this bar's own
  **B4** standard it is a check that cannot fail, and its output is worse than
  silence — a permanent `FRESH` reads as "this trust root has not moved" when the
  mechanism has never been able to see it. `AGENTS.md` > *High-risk surfaces*
  classifies that file as an *"untracked, gitignored, lockfile-uncovered
  **executable trust root**"*, so the one member the mechanism is blind to is the
  highest-risk member of the list. Found on the mechanism's **first real run**,
  2026-08-10, immediately after `refs/cairn/release-bar-audit` was published — by
  the `git ls-files --error-unmatch` assertion [RB5-5] prescribes, which is the
  only reason it was visible at all. *Fix, either half:* exclude untracked paths
  from the derived surface list **and say so**, so the list stops implying coverage
  it lacks; **or** give that trust root a tracked witness (a committed digest or
  shape record) that `git log` can actually observe. *Homed 2026-08-10 on
  Maintainer challenge* — it had been written only into the archive record of the
  plan that found it, which is the disposal-by-archive failure the archive
  precondition exists to prevent.

* **[VER-1] Content-scanner homoglyph classification residuals** *(deferred
  2026-08-10 from `content-scan-detectors`, archived)* — two follow-ups from
  the confusability-aware `homoglyph` rule, each needing its own proposal
  rather than a plan rider: (a) an exhaustive UTS #39-derived Greek
  classification to replace the 12-member curated `_NO_LATIN_TWIN` denylist —
  unresolved oracle dependency, since `unicodedata` at UCD 15.1.0 exposes no
  confusables / skeleton / script / identifier-status accessor; (b)
  whole-script Cyrillic, left an explicit residual because the
  authority-granting consequence is already closed by `byline-classification`
  and flagging the whole script would cost legitimate international names —
  revival needs its own measured corpus, per the Decision. Trigger: either
  question recurring, or a Maintainer call to invest in one.
* **[VER-1] Content-scanner per-line-per-category flag limit** *(deferred
  2026-08-10 from `content-scan-detectors` + `separator-detection`, both
  archived)* — `_scan_unicode` flags at most one hit per category per line
  (each detector loop `break`s after its first hit on that line); both plans
  pinned the current behaviour with a falsifiable test rather than changing
  it. Widening it would alter shipped `unicode-zero-width` / `unicode-bidi` /
  `unicode-line-separator` / `unicode-ignorable` / `unicode-tag` output for
  every adopter and needs its own proposal. Trigger: a demonstrated
  multi-hit-per-line attack the current limit misses.
* **[VER-4] Conda advisory coverage** — `python-security` audits **Python
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
* **[VER-7] Language-neutral conformance fixtures + golden vectors (Move 5)** — for
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

**[VER / REL] Scan coverage** *(residuals from plan `scan-coverage`, homed 2026-08-04 so the
plan can archive)*

* **[VER-5] SC1 — the registry census was struck, and the census shape is the reason.**
  The proposal's name-keyed census (`*_MAPPINGS`) is blind on the day it is
  written: `_OPTIONAL_TEMPLATES` (`bootstrap/_scaffold/config.py:249`, verified
  at HEAD 2026-08-04) is a live delivery registry that never reaches the
  manifest and whose name does not match the pattern. A census that enumerates
  by name cannot see a registry that declines to be named that way.
  *Trigger:* a **shape-based** key — one that finds delivery registries by what
  they are rather than what they are called — or the first new delivery
  registry added under any name. Until then the gate's coverage claim is
  bounded by `install_manifest()`, which `bootstrap/SAFETY.md` now states in
  terms.

* **[BND-3] SC2 — four `B607` findings, recorded and not fixed.** `git` invoked by name
  rather than absolute path, in `templates/skills/_lib/lifecycle.py` and
  `templates/skills/_lib/lifecycle_planner.py`. Re-measured 2026-08-04: those
  two files carry **16 LOW findings — `B404`×2, `B603`×10, `B607`×4** — and the
  `B607` four run inside *an adopter's own repository*, which is a real
  question rather than a formality. Deliberately deferred: bundling a
  code-hardening contract into a coverage contract is what cost
  `identity-not-name` a REVISE/SPLIT verdict.
  *Trigger:* an adopter reporting a `PATH`-resolution surprise, or any decision
  to lower the blocking threshold to LOW — which would turn the gate red on 113
  findings, only 16 of them newly visible.

* **[VER-5] SC3 — the union-vs-replacement monotonicity claim is unguarded.** Chunk B
  makes `scan_targets()` a *union* with the manifest rather than a replacement,
  and the plan's own author-accounting records that **no test guards that
  directly**. Verified 2026-08-04: zero tests in
  `bootstrap/tests/test_security_lint.py` mention it. The failure state is
  concrete — a later refactor deletes the union and the scan silently narrows.
  The on-disk oracle (`test_every_templates_py_on_disk_is_release_scanned`)
  catches it *if* the narrowing drops a file that exists on disk, which is the
  usual case but not the claim.
  *Trigger:* any edit to `scan_targets()`.
  **Remedy corrected 2026-08-04** *(plan `board-drain-guards`, Internal review)*:
  this row previously read *"the guard is one assertion and should be written
  rather than re-deferred"*, and that assertion is **vacuous**. Measured: the
  registry (42 entries) is a **subset** of the manifest (44), so deleting the
  union is a pure no-op — 76 scan targets either way, 10/10 nodes green. An
  assertion on "is a union" passes whether or not the property holds. The
  **provable** claim is narrower: *`scan_targets()` consumes `install_manifest`*,
  demonstrable by a sentinel monkeypatch that reddens under a hand-rolled-mapping
  refactor. Anyone writing this guard writes that claim, not the one this row
  used to prescribe.

* **[REL-3] SC4 — three frozen pins are stale, and the re-pin timing is a Maintainer
  question.** Verified 2026-08-04, `_gate_manifest.py verify` reports
  `FROZEN-MODIFIED` on `bootstrap/security_check.py`,
  `bootstrap/tests/test_security_check.py` and
  `bootstrap/tests/test_security_lint.py`. The plan raises and explicitly does
  **not** answer whether re-pinning happens now or at the next supervised
  re-anchor.
  *Trigger:* the next supervised re-anchor ceremony, which is where this is
  cheapest to fold in. Not mechanical — a re-pin is a Maintainer act.
  **Maintainer disposition 2026-08-04: fold in** — quoted verbatim, *"SC4 - fold
  in"*. The re-pin happens at the next supervised ceremony rather than as a
  standalone act, so it batches with the engine re-anchor that Wave 2 already
  requires. This is the **last** outstanding precondition on plan
  `scan-coverage`; everything else it owed now has a durable home above.
  **DISPOSITIONED AND SCHEDULED — do not re-adjudicate** *(marked 2026-08-04)*.
  This row is not an open follow-up: it carries a quoted Maintainer disposition
  and a named ceremony. It stays on the board as a *scheduled* item, and its
  removal condition is the ceremony running, not a decision.

* **[REL-3] Dependency-audit frozen pins await the scheduled ceremony**
  *(plan `dependency-advisory-coverage`, archived 2026-08-05)* —
  `templates/modules/team-gated/run_security_audit.py` and
  `bootstrap/tests/test_security_stack.py` are attributable
  `FROZEN-MODIFIED` entries. They join the already-scheduled supervised frozen
  union; no standalone re-pin is authorized. Removal condition: the ceremony
  verifies and records these exact paths.

**[TRU / REL] Release authenticity** *(residuals from plan `release-authenticity`)*
* **[TRU-6] RA1 (a) — Cairn's signing authority widens** *(non-mechanical for the
  adopter, mechanical for Cairn)* — the principal-count warning in
  `bootstrap/container/verify-ref.sh` counts a roster the *adopter* typed and has
  no channel back here, so it is adopter hygiene, not a Cairn-side trigger. The
  mechanical half is a Cairn suite node
  (`bootstrap/tests/test_verify_ref.py`, `test_cairn_roster_names_one_principal`
  — exactly 1 principal in `dev/.cairn/allowed_signers`, `as_of 2026-08-03`).
  Revive when that node fires: the one-signer, two-accounts trust model no
  longer describes Cairn.
* **[TRU-6] RA1 (b) — transparency-log / keyless verification** — revive when such a
  verifier is usable without adding an adopter runtime dependency. The
  zero-dependency budget is the constraint, not the idea.
* **[TRU-6] RA1 (c) — a reported cross-channel fingerprint mismatch** — revive the moment
  any adopter reports one; the two-channel comparison is the whole trust anchor,
  and a mismatch means it failed.
* **[TRU-3] RA3 — verifying the tree you build from** — the bootstrap proves a tag object
  is signed, not that a working tree equals that tag's tree. Revive when the
  scaffold gains a "verify my source" entry point, or when the lockfile's
  `cairn_commit` is cross-checked against a verified tag; either makes this an
  addition rather than a redesign.
* **[TRU-6] RA5 — the candidate-git-config class on OTHER surfaces** — closed for
  `bootstrap/container/verify-ref.sh` by construction (verification runs in a
  workspace the script creates, never in the candidate), but **not swept**: no
  enumeration of every config key that can influence a git verification, and the
  fetch still runs `upload-pack` inside the candidate. Revive at the next Cairn
  surface that shells out to `git` against a tree Cairn does not control.
* **[TRU-3] RA6 — install-side provenance** — source-side signing landed; the lockfile's
  `source_repository` / `source_licenses` stay **declared**, not attested, and
  `python bootstrap/scaffold.py --manifest` stays unsigned. Revive when an
  adopter asks "how do I know my installed tree came from the release I
  verified?", or when the fork-advisory scope reaches the same seam from the
  other side.

**Adoption UX**
* **[VER-3] Constructive readiness** — when a Cairn tool finds a project below an
  expected bar, it should *offer and drive the path to readiness* (scaffold
  the missing pieces, guide the next action), not emit a bare "not ready"
  verdict. Generative about adoption, not only diagnostic.

**Lower-priority**
* **[BND-5] Container P3s** — acceptance credential-residue leg (note/drop); `--user`
  on a future Docker acceptance leg; pin the `git` apt version for image
  byte-reproducibility.
* **[TRU-4] Differential-oracle two-stage `promote`** — future-use mechanism for a
  Cairn-engine refactor needing behavior-preservation promotion (trust root
  established, nothing pending; see `bootstrap/REANCHOR_RUNBOOK.md`).
* **[REC-5] Lifecycle-routine skill payloads (post-v1)** — additional episodic skills
  (proposal-open, review-append, decision-scribe, plan-archive); promote
  harness skill targets to native-tested as fixtures prove them.

**Archive-time follow-ups — the 2026-08-04 six-plan census**

Every deferred follow-up named in the six plans that reached code review
on 2026-08-04, homed here so they survive the archive. Produced by a per-
plan census that verified each claimed home by opening it: 95 candidate
items, 29 already homed, 38 judged fenced residuals rather than follow-
ups, and the 28 below with no durable home at all (**27 as of 2026-08-04** —
one was merged into its duplicate). A plan does not archive
until its items here are landed -- that is this section's whole purpose.

*From `archive-precondition-substance` (2) — [REC], deposited 2026-08-11:*

* **The marker grammar has a second, weaker definition.**
  `templates/modules/default-on/_lifecycle_metrics/parse.py` matches
  `### (?:[a-z]+ )?code review\b` (H3 only) while the planner's grammar is
  strictly stronger — measured, 25 plans where the planner finds a review and
  metrics misses, 0 the reverse. Two components answering "did a review happen"
  differently, with nothing keeping them in sync. **Converge them, measuring the
  snapshot impact first** (R1-3 / [E3] / [I1]). A second regex must not quietly
  become a second definition again.
* **One unchecked claim survives in the transition gates.** *"the plan-open and
  first-implementation commits stay distinct"* asserts a git-history property
  the planner cannot see from artifact text, and reports it met unconditionally.
  Inventoried and count-guarded in `bootstrap/tests/test_lifecycle_contract.py`;
  closing it needs a contract that lets the planner read history.

*From `byline-classification` (4) — [REC]:*
* **[REC-1] byline-classification, uncovered — the NFKD compatibility mappings are
  unpinned.** The `NFD`-granting / `NFKD`-flagging split rests on a
  *representative*, not exhaustive, enumeration of NFKD's compatibility
  mappings; B2 pins only the ASCII deletion set. Plan-review mandate 1,
  returned unanswered. *Trigger:* the first demonstrated compatibility
  mapping that folds a non-rostered name onto a rostered one, or a UCD
  version bump under the canonical interpreter.
* **[REC-1] Author-accounting omission (d): "`casefold()` was sampled, not
  enumerated against the full case-folding table — [I1a] shows the class
  reaches the granting path and there may be worse members than
  `chr(0x17f)`." Plan-review mandate 2 asked for the enumeration and
  returned unanswered.** *(census produced no drafted row; text is the
  plan's own wording)*
* **[REC-1] byline-classification, uncovered — no hostile roster has been
  tested.** `dev/.cairn/agent-identities.json` is lockfile-untracked and
  written by no installer; both proposal reviews and the External plan
  review probed benign typos only, so a deliberately hostile config
  remains an unexplored threat model on the granting leg. Plan-review
  mandate 3, returned unanswered. *Trigger:* any change to how the roster
  file is written, installed or trusted — or the first external adopter.
* **[REC-1] byline-classification, undecided — the B2 adjacency.** B2's expected
  deletion set is the allow-set literal in `_fold_word`'s own docstring,
  so the pin proves self-consistency rather than correctness; the plan
  named the remedy (move the literal into the test module, docstring cites
  it) and asked a reviewer to decide whether the shipped arrangement is
  enough. Neither reviewer decided. *Trigger:* the decision itself, or the
  move.

*From `scan-coverage` (1) — [VER / REL]:*
*From `release-authenticity` (2) — [REL]:*
* **[REL-4] `release-authenticity` — the Decision's flagged condition,
  undispositioned** — the approved ledger entry read *"Accept, conditioned
  on a scoped External round for the tag-substitution fix only"*, but the
  Maintainer's quoted words said only *"as revised"*. Either strike it in
  one line or name what discharges it (the 2026-08-03 Gemini Flash
  External plan review is the candidate, per `dev/NEXT_SESSION.md`).
  Blocks the plan's archive until dispositioned.
* **[REL-4] `release-authenticity` — channel 3 (Zenodo) is a documented channel
  with nothing in it** — `bootstrap/PROVENANCE.md`'s channel table lists
  the per-version deposition as channel 3, but no fingerprint has ever
  been recorded in a deposition and no public-launch step names it. At
  launch step 6, either record the fingerprint beside the deposition or
  correct the table row to say channel 3 is prospective.

*From `fork-advisory-semantics` (5) — [BND / TRU / REL]:*
* **[TRU-2] FA-R1 — the fork advisory's comparison bytes are caller-trusted, not
  anchored** *(residual R1 of plan `fork-advisory-semantics`)* — the
  upstream operand is read from the checkout hosting the verifier, **or
  from any directory an operator names with `--cairn-root`, which may
  point inside the target**; containment is proven, provenance is not.
  Revive when `release-authenticity` lands an out-of-band trust bootstrap,
  or on the first Cairn install verified from a checkout the adopter did
  not obtain themselves.
* **[REL-3] Two frozen pins stale from `7066489`** *(surfaced by plan `fork-
  advisory-semantics`, Correction 2; unclaimed)* — `_gate_manifest.py
  verify --no-collect` HOLDs on
  `bootstrap/tests/test_quality_gate_redundancy.py` and
  `scripts/quality_gate.py`, edited by the `r6-unused-def-blindspot` fix
  with no re-pin. Seam with `gate-claims-vs-enforcement`, which
  inventories them but does not claim them. Trigger: the next supervised
  re-anchor ceremony, where the re-pin is cheapest to fold in.
* **[TRU-2] `identity-not-name` condition 3 is unlanded** *(Maintainer call; plan
  `fork-advisory-semantics` Chunk B is fenced on it)* —
  `format_forked_facade_warning` still advises "remove the dormant engine
  package", which makes `tools/intent.py`'s `_load_engine()` raise
  `RuntimeError` and disables work-intent coordination. Decide shape (1)
  trivial commit now + own ceremony, (2) trivial commit now + re-anchor at
  Chunk R, or (3) amend condition 3 and let Chunk B run inside the
  already-red window.
* **[BND-1] Sweep the other consumers of `base_hash`** *(known omission (c) of
  plan `fork-advisory-semantics`; named in the proposal and never
  measured)* — `base_hash` ratchets forward on every `--finalize`, and the
  fork advisory was one consumer that treated the ratchet as an upstream
  signal. No enumeration exists of the other readers of the field or of
  which inherit the same wrong inference. Trigger: the next change to
  `--finalize`'s backfill, or any new detector keyed on `base_hash`.
* **[BND-1] `_infer_init_lock_axes` guesses `human_team` from a filename**
  *(orphaned residual: routed by `fork-advisory-semantics` to scope 4,
  whose supersession Decision did not carry it; also fenced by `profile-
  parse-fail-open`. **Second provenance, merged in 2026-08-04:** the same
  defect was independently routed here as `contributor-entry` R1, which was
  superseded 2026-08-03 without migrating it — that duplicate row is now a
  pointer to this one.)* — `bootstrap/_scaffold/upgrade.py` infers `small-
  multi` from the mere presence of a root `CONTRIBUTING.md` and `solo`
  otherwise, so the engine's heuristic can read a project's declared axis
  back wrong. Named upgrade path: read the manifest's `optional_templates`
  block instead of file presence. *Trigger (carried in from the merged
  duplicate, 2026-08-04):* the next proposal touching
  `bootstrap/_scaffold/upgrade.py`'s init-lock axis inference. Reachable only
  on a first `upgrade
  --init-lock` in a tree with no committed `dev/.cairn/profile.yml`.

*From `profile-parse-fail-open` (8, was 9 — one row merged 2026-08-04) — [BND / VER / REL]:*
* **[BND-1] Profile key with an unrecognized *value*** *(residual from plan
  `profile-parse-fail-open`, G1)* — a profile listing `- not-a-real-
  module` under `modules:` is accepted at exit 0 and printed in the
  roster; measured 2026-08-03, there is **no** downstream module
  validation to catch it. *Trigger:* the first adopter report of a mis-
  typed module name, or the next proposal touching `expand_preset`.
* **[BND-1] Profile forward-compatibility cost is argued, not measured**
  *(residual from plan `profile-parse-fail-open`, G2)* — unknown profile
  keys now refuse; the reserved `schema` key rescues no already-released
  engine, so the disposition is free only while the adopter set is empty.
  *Trigger:* the first genuine older-engine/newer-profile break. *Remedy:*
  a follow-up proposal reversing the disposition — never a quiet
  loosening.
* **[BND-1] Two `test_presets.py` nodes use `_yaml_load` as its own oracle**
  *(residual from plan `profile-parse-fail-open`, G3)* —
  `bootstrap/tests/test_presets.py:293` and `:423` compare the parser
  against itself whenever PyYAML is absent; left standing because the file
  is frozen. *Trigger:* the next change that edits `test_presets.py` for
  any reason. *Mechanical:* `grep -n "_yaml_load"
  bootstrap/tests/test_presets.py`.
* **[REL-3] `_gate_manifest.py`'s `SKIP-XFAIL-NEW` over-reports** *(residual from
  plan `profile-parse-fail-open`, G4)* — the check reads
  `get_closest_marker("skipif")`, which resolves a module-level
  `pytestmark`, so any node added to such a module registers as newly
  marked; 34 `test_presets.py` nodes are recorded "marked" while the suite
  reports 0 skipped. *Trigger:* the next supervised ceremony, or the next
  plan needing a node in a marked module. *Mechanical:* `python
  bootstrap/tests/_gate_manifest.py verify --anchor-ref <P>`.
* **[BND-1] `_resolve_current_profile`'s lockfile fallback is audible but
  unexamined** *(residual from plan `profile-parse-fail-open`, G5)* —
  Chunk A made the swallowed exception print to stderr; whether
  substituting the lockfile profile is the right disposition at all was
  never examined. *Trigger:* the next upgrade-path proposal.
* **[BND-1] `profile-parse-fail-open` decision point 4 — the totality claim is
  affirmed but unchecked** *(Maintainer question, carried since plan-open
  2026-08-03)* — the recommended focused Internal round on the closed
  grammar's totality claim never ran; the External round affirmed it from
  the plan's own specification prose and the author's Response banks it
  **unverified**. Implementation landed anyway at `e7394cb`. *Decide:*
  strike it as absorbed, or run the round against the landed code.
* **[REL-3] `profile-parse-fail-open`'s gate-manifest delta awaits a supervised
  ceremony** *(residual, 2026-08-04)* — one `FROZEN-MODIFIED` on
  `bootstrap/tests/test_scaffold.py` plus one `COLLECTION-DROPPED` from
  the `test_mixed_indent_list` → `..._is_refused` rename; the plan
  measured them and explicitly neither performs nor schedules the re-pin.
  *Trigger:* the next supervised gate ceremony — batch with SC4, which
  carries the same disposition.
*(The second `_infer_init_lock_axes` row that stood here was **merged
2026-08-04** into the row of the same name under *From
`fork-advisory-semantics`* above — same defect in
`bootstrap/_scaffold/upgrade.py`, recorded twice because two plans each
routed it here. Both provenances are preserved on the surviving row;
nothing was dropped.)*

*From `gate-claims-vs-enforcement` (7) — [REC / REL]:*
* **[REC-4] Gate-claims B2 — the archive-commit-body auditability claim is
  falsified** (`doctrine/proposals.md` > "Archive preconditions" and
  `doctrine/plans.md` > "Lasting-truth migration doctrine":
  *"This makes the migration auditable from `git log` alone"*) — keep the
  "must", name the trigger, correct the consequence claim; its own
  proposal, because the block is restated at `doctrine/lifecycle-
  contract.md:137` and `templates/core/dev/PLANNING.md:105`, which engages
  the loop-fidelity lens.
* **[REC-4] B2's evidentiary figure is re-measured at pickup, never carried** —
  the proposal's *"zero archive commits"* is falsified; measured
  2026-08-04 at HEAD `da2d00e`: plan archives **1 of 10** (`b67fabc`),
  proposal archives **2 of 21** (`bd608c9`, `9c95653`). Re-run the
  enumeration before writing any number.
* **[REL-5] The gate-claims audit's axis 2 (behavioural — run the artifact that
  would check the stated control) and axis 3 (does the named trigger
  contain the procedure) were never swept systematically** — `gate-claims-
  vs-enforcement` sampled both; two ledger rows fell out of a single ad-
  hoc axis-3 pass, which is the argument for finishing the sweep as its
  own proposal.


**Security pair close-out (2026-08-11)** *(group created at the archive of
`api-web-security-modules` and `security-verification-activation`. Both plans'
Lasting-truth tables declared homes for several of these; two of those declared
homes were "the code review", which does not exist -- so they are re-homed here
rather than left pointing at a section that was never written.)*

* **[SP8-1] Neither plan received a code review, and the archive gate cannot
  detect that.** Both `## Code review` sections were untouched placeholders at archive.
  **Discharged 2026-08-11**: External Security Review by Antigravity (Gemini 3.1 Pro)
  appended to both archived plans (`dev/plans/archive/api-web-security-modules.md` and
  `dev/plans/archive/security-verification-activation.md`). Item (b) remains: fix
  `tools/lifecycle_planner.py` archive gate to require a non-placeholder body.
* **[SP8-2] Four Security Reviews are owed, none satisfied.** **Discharged 2026-08-11**:
  All four surfaces (`701be3a` `_LIVING_STATE_DSTS` widening, `04e8609` `argv_mode` schema,
  `04e8609` `_DECLARED_CAPABILITY_MODULES` frozenset, `fd0eb21` child `details` string contract)
  independently falsified and accepted in the External Security Review.
* **[SP8-10] `test_child_env_is_minimal_and_strips_proxies_and_credentials` assertion sensitivity to subprocess CPython PEP 538 locale injection.**
  `bootstrap/tests/test_security_verification.py` line 360 computes `expected` from parent `os.environ` at call time. On platform environments where parent `os.environ` lacks `LC_CTYPE`, CPython subprocess spawn auto-injects `LC_CTYPE="C.UTF-8"`. The dispatcher admits `LC_` via `_CHILD_ENV_ALLOWLIST_PREFIXES`, but the test assertion fails exact set equality due to the post-spawn injection. Test expected set calculation should account for CPython's auto-injected `LC_` keys. Found during External Security Review 2026-08-11.
* **[SP8-3] The dispatcher cannot ever report CLEAN for a credentialed
  capability -- design question, not a bug.** `_read_credentials` runs for
  `local` mode and refuses `E_CREDENTIAL_ABSENT` when a principal's credential is
  absent from the environment; the dispatcher's child env allowlist admits no
  credential name and no `SSL_CERT_FILE`. So both capabilities can report
  *unconfigured*, *refused* or *degraded* through the dispatcher, never *passed*
  -- which sits oddly beside their registry entries declaring `evidence_mode:
  loopback`. Weakening the allowlist would be a real security regression and was
  correctly refused. Needs a proposal on what the dispatcher's role **is** for a
  credentialed capability.
* **[SP8-4] Three defects hid at one interface because each side tested itself.**
  The `-security` name-suffix filter, the single-token `argv_mode`, and the
  `details` dict-vs-string contract were all invisible to both plans' reviews:
  the activation tests drive a **synthetic** runner and the facade tests invoke
  the CLI **directly**. `TestChunkGRealFacadeThroughRealDispatcher` now closes
  this seam. The generalizable question -- whether any reciprocal plan pair
  should be *required* to carry a both-sides-real integration test before either
  half archives -- belongs in the Dual-Review doctrine, not in a plan.
* **[SP8-5] Cairn does not self-host the dispatcher, and that was never
  decided.** Activation's L2 pre-declared the decision to the first capability
  plan; no capability plan made it. Measured 2026-08-11: no copy of
  `run_security_verification.py` exists under `scripts/` (the path is cited
  nowhere here precisely because it does not resolve) and the lockfile carries
  zero references. The de facto
  answer is "no self-hosting"; making it deliberate is a one-line decision
  nobody has taken. Related: **Cairn's own lockfile does not record
  `dev/modules/security-verification.md`** even though the file is in the tree
  and the module is default-on, and **no gate reddened** -- a scoped
  re-finalize.
* **[SP8-6] Activation's L4 and L6, re-homed from a review that does not
  exist.** L4 (the destination-collision path for the two new files) and L6 (the
  install-manifest byte-stability invariant having no standing test) both
  declared "the code review" as their durable home. Carried here verbatim so
  neither is lost; L6 in particular is a *gap claim* that wanted a reviewer's
  agreement it is real.
* **[SP8-8] Every adopter's `AGENTS.md` reads `clean-locally-modified` on
  upgrade with no adopter edit.** The module merge pass rewrites the file after
  `install_core` while the base cache retains the unmerged template, so the
  classifier sees divergence that the adopter did not create. Not a blocked
  upgrade -- the kind stays inside `_ADVANCING_KINDS` -- but an inaccurate label
  on the single most-read file Cairn installs. Found by
  `security-verification-activation`'s Chunk B when it reddened a test whose
  docstring premise that chunk had falsified.
* **[SP8-9] The archive preconditions did not test what they name -- CLOSED
  2026-08-11.** Plan `archive-precondition-substance` archived to `dev/plans/archive/`: SHIP on both
  the External plan review and the External code review, zero regressions
  against baseline (2933 -> 2955 passing, identical 4 pre-existing failures).
  Two follow-ups deposited under [REC] above. Corrected figures, superseding
  the ones this entry carried: the old-vs-new `Dispositions:` parser delta is
  **6**, not 12 (the 12 came from an unanchored presence test used to measure a
  presence-test bug); the default scan covers **7** live artifacts, not 6; and
  the no-review count is **re-derived at implementation time** rather than
  carried forward, having been measured 27 -> 23 -> 3 before it was right.
  Strict archive audit, `as_of` 2026-08-11 under the new predicates:
  **61 of 91** artifacts flagged by `scan --include-archive` (was 53 of 88
  under the old ones) -- a dated **measurement of the predicates**, not a
  drainable backlog: R1-1 forbids retrofitting archived records, so
  nothing clears that count and it is not a debt. Re-derive it whenever a
  predicate changes. Deliberately **not** folded into the default gate,
  which stays live-only, and nothing currently invokes the archive mode. The identity-
  normalizer collision that makes a valid same-agent-type Internal review read
  as author-review is routed to **[REC]** alongside `code-review-blindness`;
  this plan does not change identity policy. Proposal accepted at
  Revision 1 and archived; the plan
  `dev/plans/archive/archive-precondition-substance.md` is the permanent home
  for the remainder. Its Boundary C range must include
  `da3e296`, which shipped both planner twins and eight tests before the
  proposal was reviewed. **Fixed in code:** the `## Code review`
  gate now requires a reviewer marker (a `**Model**:` line or a dated `Code
  review -- <reviewer> -- YYYY-MM-DD` heading) instead of the section's mere
  presence; and the `Dispositions:` pattern now tolerates markdown emphasis,
  which had made it report "no Dispositions block" against archived plans that
  carried one. **That count was first recorded as 12 and is wrong: the real
  old-vs-new parser delta is 6.** The 12 came from an unanchored hand-rolled
  regex -- 5 of its hits were prose *discussing* the phrase, and 1
  (`adopter-entry-doc-refresh.md:173`) is a real **mid-line** block the
  `^`-anchored fix still rejects, i.e. a live false-fail. Measuring a
  presence-test bug with a presence test; see the proposal's Response. **Left to the proposal**, because each is a behaviour
  change adopters would see: the Dispositions and loop-fidelity gates in the
  `--to archived` pre-transition list are literal `True` and always report met;
  the `scan` subcommand does not walk `dev/plans/archive/`, which is why none of
  this surfaced; and whether a text scanner should assert "code review occurred"
  at all rather than the checkable "a section bearing a reviewer identity and
  date exists". Measured, and each figure was wrong on the first attempt:
  **3** archived plans have no real code review anywhere (not 27, not 23 --
  earlier passes examined only the first `## Code review` section, and only its
  first three lines), the third being `gate-reanchor-preflight`, previously
  unknown. Re-derive that count when picking this up; it moves as reviews land.
  Still unfixed and carried by the proposal: the loop-fidelity precondition is
  satisfied by a case-insensitive regex for the phrase *"Fidelity sign-off"* or
  *"loop-fidelity"* anywhere in the artifact — writing the phrase satisfies the
  gate, and no sign-off need have occurred.
* **[SP8-11] `dev/intents.jsonl` grows without bound, and the cost lands on the
  commit path.** **DISCHARGED 2026-08-11** — shipped at `e54f43c`, External code
  review (Codex) BLOCK at `bf38e67`, answered at `80e6ea4` + `409caae`, Response
  and Addendum at `3bf5ccf` and the archive commit; proposal archived at
  `dev/proposals/archive/2026-08-11-claude-intent-ledger-pruning.md`. All five
  findings dispositioned `accept`/`guard` — see the Addendum's superseding
  block. **One correction to the text below, which is preserved as written:**
  "a lost claim is a lost lock" is **false** and was retracted in the
  implementation. `dev/intents.jsonl` is an *advisory* collision hint, not a
  mutual-exclusion lock; a claim past the 4h TTL warns but never blocks. That
  one wrong sentence, written here and in the proposal's [H2], is what escalated
  a file prune into a BLOCKER. The remaining concurrency window is closed by
  disposition, not by code: the full handoff runs after other sessions end, and
  that precondition is now written into `session-end`'s `SKILL.md`. The ledger
  is a
  **coordination surface, not an archive** (Maintainer's framing) -- gitignored,
  local to one checkout -- yet nothing prunes it: claim and release both append,
  and the full handoff's `_surface_intents` is read-only. Measured 2026-08-11:
  650 records / 188 KB since 2026-07-22. `active_intents` replays the whole file
  and runs in the **pre-commit hook**, so every commit pays for project age.
  Two hazards are the design content, both verified: pruning a release without
  its claim **resurrects the claim as active** and blocks its paths forever; and
  any rewrite races the deliberately append-only single-`os.write` shape, where a
  lost claim is a lost lock. Recommendation in the proposal: prune released pairs
  only, and *report* never-released claims rather than deleting them -- a 30-day
  unreleased claim is a bug signal, and this session hit that failure twice.
* **[SP8-12] `test_verify_ref`'s two failures are NOT a missing GPG key.** That
  explanation was propagated all day -- into both archived plans' verification
  sections, the `da3e296` and archive commit bodies, and several sub-agent
  briefs -- and it is **false**. Measured 2026-08-11: `test_verify_ref.py` alone
  is **67/67 green**; both nodes fail only in the full suite, reproducibly across
  two consecutive runs, and not when paired with `test_gate_preflight`,
  `test_security_check`, or `test_lifecycle_cli` individually. So it is cross-file
  state pollution, and the conclusion those records drew ("not this work's") was
  right for the wrong reason. A wrong reason is worse than none here: "needs a
  GPG key" tells the next reader to stop looking. Narrowing the polluter is a
  bisect nobody has run. Adjacent to Antigravity's **[SP8-10]** (same shape: a
  test whose expectation depends on ambient state).
* **[SP8-13] `intent.py claim` cannot record a legitimate wide claim, and its
  error advises the wrong remedy.** Met 2026-08-11 while claiming nine paths for
  the intent-prune close-out: refused at **553** bytes, then at **522** after
  shortening `--action` to two words, against the **512**-byte cap — with **342
  bytes of that being paths alone**. The cap itself is correct and load-bearing:
  it keeps one record inside a single `os.write`, which is the append atomicity
  the whole surface rests on (`record_io.py`'s Atomicity note). The defect is
  that the error names `--stem` and a shorter `--action` as the remedies while
  reporting paths as the dominant contributor — neither remedy touches paths — so
  the operator's only recourse is to split the claim into pieces and hope the
  overlap check still means something. A cross-cutting refactor is exactly when a
  claim matters most and exactly when it cannot be filed. Candidate shapes: fold
  a common prefix (`templates/modules/team-gated/_intent/` appeared twice in that
  set), or emit **multiple lines sharing one `id`** so the record stays inside one
  `os.write` per line while the claim stays whole. Either is a change to the
  record schema that `active_intents`, `conflict`, and now `prune_released_pairs`
  all read, so it takes a proposal. Adjacent: **[SP8-11]** (archived).
* **[SP8-7] `api-web-security-modules` never landed its
  `templates/modules/README.md` catalog row (F-11).** Activation's Chunk D landed
  its own row at `dd15268`; api-web's was left because another session held the
  file. Activation's L5 assigned the pre-existing default-on drift fix to
  "whichever cluster scope lands its README row last" -- with api-web's row
  never landing, that owner never resolved.


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
