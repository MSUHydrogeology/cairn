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

* **[TOOL, URGENT] ~~`dev/plans/` corpus-wide metrics extraction is currently
  broken -- `lifecycle_metrics.py plans` exits 3 (`INCOMPLETE`) against the
  live tree~~ -- CLOSED 2026-08-25.** The 2026-08-25 goodnight run walked the
  whole corpus clean: `dev/measurement/snapshots/2026-08-25-1.csv`, **120 rows,
  71 proposals + 49 plans**, exit 0 -- every plan file in the tree, none
  refused. The `cairn-event-v1` cutoff that caused the `INCOMPLETE` no longer
  applies: `retire-event-blocks` removed the event machinery this row depended
  on, so the unreconcilable transition it describes cannot arise. **No
  Maintainer decision is needed** -- neither of the two options below (accept a
  permanently-`INCOMPLETE` walk, or build a grandfather list) has anything left
  to decide. **Note the reproduction command below is wrong and always was:**
  running the *template* copy refuses by design ("no planner installed
  alongside"), and `--root` defaults to the script's own directory. Use the
  self-hosted tool from the repo root. The original text is kept below for the
  record.

  ~~Original finding:~~ *(filed 2026-08-21, from `metrics-events-not-prose`'s code
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
| What the sweep deleted, and the measurement that justified it | [`dev/plans/subtraction-sweep.md`](plans/subtraction-sweep.md), C7 bankruptcy record |

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
