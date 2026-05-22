# Changelog

Notable changes to Cairn.

Entry-shape: each entry is one line (sometimes 1-3 short
sentences for substantive doctrine landings), grouped by
category, with at least one cross-link to the durable substance
(an archived adopter proposal / plan / commit, or the Cairn-side
doctrine file). The methodology's bias is for the substance to
live in doctrine and case studies; the changelog curates and
points.

The `Unreleased` section accumulates pending entries; when a
release is cut, that section is renamed to the version + date
and a new empty `Unreleased` is started above.

## Unreleased

### Added

- **Per-session coordination identity (ported from the
  `modflow_tools` adopter, 2026-05-21).**  New cross-tier section
  [`doctrine/coordination.md`](doctrine/coordination.md) >
  "Coordination identity — per-session, not per-agent": a
  coordination mechanism that records who holds a path must derive
  identity **per-session** (from the harness session id), not
  per-tool, or concurrent same-tool sessions collapse to one
  identity and one session's auto-release closes another's claims.
  Portable rules: derive from the harness session id; hash the
  *whole* id (time-ordered UUIDv7 ids share leading bytes); treat
  a global identity override as an escape hatch, not a setting;
  auto-release closes only the committing session's own claims
  (fail-soft on resolution failure).  Companion "Substrate
  convergence" note: Tier 2 and Tier 3 can share one append-only
  claim/release log.  Module extension in
  [`templates/modules/team-gated/coordination-tiers.md`](templates/modules/team-gated/coordination-tiers.md)
  > "Extension — Per-session identity for the claim/release log";
  adopter grounding (the JSONL substrate + the three harness
  session-id env vars `CLAUDE_CODE_SESSION_ID` / `CODEX_THREAD_ID`
  / `ANTIGRAVITY_TRAJECTORY_ID`, each supplied by that harness's
  own reviewer) in
  [`case-studies/modflow_tools.md`](case-studies/modflow_tools.md).
  Source: the adopter's accepted + reviewed
  `2026-05-21-claude-per-session-intent-identity` proposal (Codex
  + Antigravity reviewed), itself a follow-on to the JSONL
  work-intent substrate refresh.

## 0.1.1 — 2026-05-21

### Added

- **Doctrine sync 2026-05-19 → 2026-05-21 (cairn-doctrine-sync-may-19-21).**
  Nine doctrine landings ported from the `modflow_tools` adopter
  through a single multi-chunk plan; each Cairn-doctrine surface
  is grounded by the F9 evidence ledger in
  [`case-studies/modflow_tools.md`](case-studies/modflow_tools.md)
  > "Doctrine-sync 2026-05-19 → 2026-05-21 (F9 evidence ledger)".

  * [`doctrine/coordination.md`](doctrine/coordination.md) >
    Tier 2 — extended with a required-signal-read mode for the
    adopter-identified subset of coordination-surface files
    (handoff notes, planning indices, collaboration norms,
    change logs). The baseline courtesy framing is preserved for
    incidental shared files; the required mode applies to the
    adopter-named subset only.
  * [`templates/modules/team-gated/coordination-tiers.md`](templates/modules/team-gated/coordination-tiers.md)
    — two extensions added inside the existing module:
    a tracked **collision log** with a narrow event definition
    (three event kinds; only `true-staged-index` counts against
    the rolling-window trigger) and a **goodnight intent-hygiene**
    step (prune-intents + migrate-collisions, run once per
    session-day by the full-handoff owner).
  * [`doctrine/session-routines.md`](doctrine/session-routines.md)
    > Goodnight — new sub-section on the next-session starting
    plan: **rewrite-from-scratch each goodnight**, with
    durable-claim migration upstream of the rewrite.
  * [`doctrine/dual-review.md`](doctrine/dual-review.md) — new
    section naming the **Decision-support Round-2 review**
    pattern (three structural properties + bounding rules).
  * [`doctrine/lifecycle.md`](doctrine/lifecycle.md) — three
    new sections: **procedural-gap inline Decisions** (three-
    criterion gate); **deferred-follow-up revival** (deferred
    items re-enter the proposal lifecycle when revived);
    **the roadmap is a current-state index, not a historical
    log** (completed work migrates out of the roadmap into the
    durable record).
  * [`doctrine/roles.md`](doctrine/roles.md) — new section on
    the **capability-floor invariant** (each role has a minimum
    capability floor jointly determined by role and risk;
    adopter-local tier labels; default high/medium/low mapping).
  * NEW [`templates/modules/team-gated/model-selection.md`](templates/modules/team-gated/model-selection.md)
    module — conditionally installed at the moderate-or-complex
    end of the Complexity axis. Includes tier-by-role default
    mapping table + override discipline; adopter-local tier-to-
    model mappings live in case studies (the doctrine names the
    invariant; the case study identifies the models).
  * [`templates/core/dev/PLANNING.md`](templates/core/dev/PLANNING.md),
    [`templates/core/dev/NEXT_SESSION.md`](templates/core/dev/NEXT_SESSION.md),
    [`templates/core/dev/agent_collaboration.md`](templates/core/dev/agent_collaboration.md)
    updated to cross-reference the new doctrine and to align
    with the roadmap-no-history posture (PLANNING.md drops the
    "Completed recently" section) and the rewrite-from-scratch
    rule (NEXT_SESSION.md gains explicit rewrite language).
  * [`case-studies/modflow_tools.md`](case-studies/modflow_tools.md)
    — extended with the F9 evidence ledger linking each
    Cairn-doctrine surface to the adopter incident, file, and
    commit that grounded it, plus the modflow_tools tier-to-
    model mapping for the model-selection module.

  External Review (Antigravity / Gemini 2.5 Pro) of the
  abstraction drafts (Chunks 1 + 2) was absorbed via a single
  Sharpening commit. Three findings: vendor-neutrality
  violation in a draft (P1, fixed); module-directory taxonomy
  alignment — the new module goes under `team-gated/` per
  Cairn's catch-all convention, not a new `dimension-gated/`
  subdirectory (P2, fixed); typo/hedge cleanup (P3, fixed).
  The corrections preserved all structural-property abstractions
  intact.

  The full plan, including the External Review record and the
  per-chunk source-commit provenance, lives in the
  modflow_tools-side accepted proposal
  `2026-05-21-claude-cairn-doctrine-sync-may-19-21` and its
  executing plan `cairn-doctrine-sync-may-19-21` (under
  `modflow_tools/dev/plans/`, archiving after Chunk 11
  lasting-truth migration).

## 0.1.0 — 2026-05-20

Initial public release. See the launch commit (`4afcba8`),
which finalized README, CITATION, and licenses for v0.1.0.
