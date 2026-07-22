<!-- cairn-internal-ref-allow: doctrine/proposals.md doctrine/lifecycle.md doctrine/rationale.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: dev/strategy/2026-07-11-claude-cairn-adoption-record.md, dev/measurement/attestation-replay-failures.md -->
<!-- The two paths above are forward-reference files this plan creates; they materialize as Chunks B and D land. -->

# Plan: record corrections (C1, C2, C3, OQ3 tracker)

**Source proposal**: `dev/proposals/archive/2026-07-11-claude-record-corrections.md`
**Status**: open
**Plan review**: required(Internal) — fresh-context read. The proposal
already cleared a 3-lens Internal panel *and* a Gemini External SHIP at
the proposal stage; this plan's own job is mechanical translation of an
already-accepted, already-revised design into concrete file edits, plus
verifying the record-authoring content (C2/C3 prose) doesn't over-reach —
exactly the negative-space gap both the Internal panel and Gemini flagged
("the CONTENT of the yet-unwritten adoption record... is a review-of-
artifact catchable only at plan/implementation/note-read time"). No
second External pass required — the doctrine/gate mechanics were already
independently stress-tested twice; Internal floor is the right tier here.

## Context

The accepted proposal's Decision (2026-07-22) scoped C1 + C2 + C3 all in,
plus one departure from the proposal's own default: OQ3 seeds an
`attestation-replay-failure` tracker in `dev/measurement/` (arming the
deferred cut-transcript follow-up's recurrence path) rather than leaving
it un-armed at n=1. OQ1 (Unreleased-only, no pointer into the closed 0.3.0
entry), OQ2 (no standalone note — addendum is enough), and OQ4 (dated
2026-07-11, not backdated) are also resolved at Decision. Full detail:
`dev/proposals/archive/2026-07-11-claude-record-corrections.md` — its
Revised proposal section (`:414-443`) is the authoritative design; this
plan translates it into Chunks A-D.

**Three findings from this plan's own preparation, not caught by either
proposal-stage review round** (disclosed up front, not folded in
silently):

1. **The "byte-identical gate code" claim needs a small correction.**
   Re-replayed this session: `git diff 12ec2ad HEAD -- scripts/quality_gate.py`
   is **no longer empty** (12 lines) — this same implementing session's
   `adopter-licensing-compliance` plan (commit `501efe3`) added a 3-line
   SPDX/copyright header to the top of the file after the proposal and
   both reviews verified byte-identity. The diff is comment-only (already
   independently confirmed AST-invisible this session, via the sibling
   plan's own AST-attestation work) — it changes nothing about
   `quality_gate.py`'s behavior. Re-ran the replay anyway rather than
   trusting the stale claim: `git archive 12ec2ad | tar -x`, then
   `python3 scripts/quality_gate.py --sub neutrality` → **exit 1, 99
   `FAIL`-class lines** (grep-counted, not estimated); `--sub redundancy`
   → **exit 1, 6 `FAIL`-class lines** — both numbers reproduce exactly.
   Chunk A's erratum states "gate code differs from the cut only by a
   later, comment-only SPDX-header addition (non-functional, independently
   confirmed AST-invisible)" rather than "byte-identical."
2. **C2's six-axis citation is imprecise.** The proposal says the
   adoption record should be "cross-referenced to the framework note
   `dev/strategy/2026-05-14-claude-human-ai-team-development-framework.md`
   that defined the six-axis model." Grepped that note for the actual
   six-axis terminology (`greenfield`/`medium`/`moderate`/etc.) — zero
   hits; it discusses the `dimensions/` system's *existence* in one
   sentence (`:443`, "`dimensions/` -- six adaptive axes...") as part of a
   broader structural survey, but does not define it. The canonical
   technical definition — the exact six-axis point `profile.yml:14-16`'s
   comment states (`greenfield / medium / moderate / single / solo /
   concurrent-multi-type`) — is `bootstrap/BOOTSTRAP.md:178-181`'s preset
   table (`collaborative-team` = `greenfield / medium / moderate / single
   / small-multi / concurrent-multi-type`, matching profile.yml exactly
   once the documented `human_team: solo` override is applied) plus the
   individual axis docs under `dimensions/*.md`. Chunk B cites
   `bootstrap/BOOTSTRAP.md:178-181` + `dimensions/` as the primary
   technical source and the 2026-05-14 framework note as a secondary,
   contextual cross-reference (it discusses the system's existence, not
   its definition) — more precise than the proposal's phrasing, same
   underlying fact.
3. **A real rolling-window mechanics gap in OQ3's tracker seeding —
   flagged for plan-review, not silently resolved.** `tools/evolution_infer.py:186-190`'s
   `evaluate_tracker()` computes `cutoff = today - window_days` **at
   evaluation time** and only counts an `Impact: occurred` row if
   `inc["date"] >= cutoff`. The `review-floor-deviations.md` precedent
   backdates its two seeded rows to their *true* historical occurrence
   date under `Impact: historical` — but `historical` rows are
   documented (and verified, same file) to **never** count toward the
   recurrence trigger, by design. `12ec2ad`'s true incident date is
   **2026-06-12** (`git show -s --format=%ci 12ec2ad`). If this plan
   follows the same backdating convention with `Impact: occurred`
   instead, the row would already sit outside any realistic rolling
   window by the time it is logged (5+ weeks later) and would **never**
   be able to combine with a future second incident — functionally inert
   against the exact arming purpose the Decision cites for OQ3 ("an n=1
   recorded only in prose can never become an n=2"). **Proposed
   resolution (Chunk D row):** date the row at the date this plan's
   Chunk D commit lands (when active tracking of this event class
   begins), not the true 2026-06-12 occurrence; state the true
   occurrence date in the row's own Description text so the historical
   fact isn't lost, and add a tracker-level note (mirroring
   `review-floor-deviations.md`'s own documented `Impact` local-extension
   pattern) explaining the departure from that precedent's backdating
   convention and why. This is a genuine judgment call neither proposal-
   stage review round exercised (both discussed *whether* to seed a
   tracker, not the seeded row's date semantics against
   `evaluate_tracker`'s actual cutoff arithmetic) — flagged explicitly
   for the plan-review pass below rather than resolved unilaterally.

### Documentation / doctrine surface

Record-of-fact edits across the deliberation layer (`dev/strategy/`,
`dev/measurement/`) and one Entry-layer shared-communication-file edit
(`CHANGELOG.md`, per R9's correction — Entry layer, not descriptive).
Two machine-state pointer repoints (`dev/.cairn/profile.yml` comment;
`dev/PLANNING.md`, a shared comm file). No `doctrine/` or `AGENTS.md`
change — matches the accepted proposal's own routing exactly; nothing in
plan-authoring changes that conclusion.

## Sequence

```
A. C1 -- v0.3.0 attestation erratum (CHANGELOG.md, Unreleased)  [approval-gated; commit pending]
B. C2 -- write the adoption record + repoint profile.yml         [commit pending]
C. C3 -- gating-function caveat addendum                         [commit pending]
D. OQ3 -- seed the attestation-replay-failure tracker            [commit pending]
   (PLANNING.md's C2 repoint lands at this plan's archive commit, per R5 --
   not bundled into Chunk B; see "Archive closeout" below)
```

### Chunk A — C1 (the v0.3.0 attestation erratum) — approval-gated

| # | File | Change |
|---|------|--------|
| A1 | `CHANGELOG.md` | Append one entry to the existing `## Unreleased` > `### Fixed` subsection (below the one current entry, same style — bold lead phrase then prose). Content, per the Revised proposal `:420-427` + this plan's finding 1 correction: names `12ec2ad`, quotes its attestation verbatim (`"quality_gate exit 0 (neutrality all-info/justified; 6 advisory R6 redundancy notes ... accepted for a private cut)"`); refutes **per sub-gate** (neutrality attested zero, replays exit 1/99 `FAIL`-class — materially false; redundancy's count of 6 was accurate and its acceptance honestly disclosed, only the "advisory" class-label + umbrella "exit 0" are wrong); refutes the "exit 0" umbrella via the OR-aggregation logic at `quality_gate.py:114-115` (either FAIL-class sub-gate alone entails full-gate exit 1); notes order-independence *also* fails on the cut tree but is pytest-based/environment-sensitive and is disclosed **without** a pinned count (R7); pins the exact reproduction (`git archive 12ec2ad \| tar -x`, then the two `--sub` invocations); states gate code is comment-only-different from the cut, not byte-identical (this plan's finding 1); adopts "hand-written from a partial/remembered run, not fabrication" framing; cross-references broad-look Theme 1 item 3 (`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:142-148`, the skipped v0.3.0 pre-release sweep) as the proximate cause, without attempting that sweep's own reconstruction (R11, genuinely separate, unassigned). |

**Approval gate (hard requirement, per plan-review R5).** `CHANGELOG.md`
is a shared communication file; per `AGENTS.md`'s carve-in, its additions
are auto-carved only in the goodnight-handoff commit — **not** the
deliberation/plan-open carve-out this plan otherwise relies on for
`dev/proposals/`/`dev/plans/` commits. This chunk's commit requires
**explicit, separate go-ahead** before it lands, distinct from the
general plan-execution authorization. Ask at the point of implementation;
do not bundle this commit's approval into a broader "proceed with the
plan" instruction.

### Chunk B — C2 (write the missing adoption-decision record)

| # | File | Change |
|---|------|--------|
| B1 | `dev/strategy/2026-07-11-claude-cairn-adoption-record.md` (new) | Reconstructed adoption-decision note. Dated **2026-07-11** (OQ4 — the true authoring date, not backdated to 2026-06-12), states plainly it is a reconstruction. Records: the six-axis point `greenfield / medium / moderate / single / solo / concurrent-multi-type` (`profile.yml:14-16`), citing `bootstrap/BOOTSTRAP.md:178-181` (the `collaborative-team` canonical point + `dimensions/*.md`) as the primary technical source and the 2026-05-14 framework note (`:443`, discusses `dimensions/`'s existence) as a secondary contextual cross-reference — this plan's finding 2 correction, more precise than the proposal's original phrasing; the `collaborative-team` preset + `human_team: solo` override and why (a 1-human-maintainer project overriding the preset's default `small-multi` human-team point); the three `modules_add` entries and the trust-boundary rationale each already carries inline in `profile.yml:20-23` (`issue-capture` — GitHub Issues for gap/friction capture; `security-review` — real trust boundary: file I/O, path handling, YAML/module parsing; `examples-gallery` — `examples/` ships runnable code, others adopt Cairn); that the profile was accepted 2026-06-12 (Act I-6). **Honesty guard:** explicitly marks the one thing **not recoverable** — any contemporaneous 2026-06-12 deliberation transcript or chat record; the note draws only on what `profile.yml`'s own committed content and the framework/BOOTSTRAP citations objectively support. |
| B2 | `dev/.cairn/profile.yml` | Repoint the `:7-8` comment ("The deliberation behind it lives in `dev/strategy/` (the adoption record).") to name the concrete file: `dev/strategy/2026-07-11-claude-cairn-adoption-record.md`. **Not machine-checked** (`.yml`, out of `check_cairn`'s tracked-Markdown scope, R5) — correctness rests on this chunk's own review, not a gate. |

**B3 — PLANNING.md's repoint is deferred to this plan's archive commit,
not bundled here** (R5's fix: a required, *tracked* closeout step, not
"e.g. goodnight"). See "Archive closeout" below. Landing it here would
create the exact inconsistent-pointer window R5 flagged (`profile.yml`
naming the concrete file while `PLANNING.md:34-40` still says the
generic `dev/strategy/` directory) for the span between this chunk's
commit and the plan's eventual archive — the archive-commit binding
closes that window by construction, matching the licensing plan's own
`dev/PLANNING.md` row-move precedent (bundled directly into that plan's
archive commit, not a separate step).

### Chunk C — C3 (the zero-rejections gating-function caveat)

| # | File | Change |
|---|------|--------|
| C1 | `dev/strategy/2026-05-20-claude-team-productivity-metrics.md` | Append a dated "**Gating-function caveat (2026-07-11 addendum)**" directly below the existing 2026-05-19 baseline bullet list (`:149-153`, ending "Median `days_to_decision` = 0 days") — append-only, the original analysis at `:149-153` is untouched. Content, per the Revised proposal `:433-435`: (i) the corpus is a **modflow_tools** 2026-05-19 baseline, not Cairn's own tree; (ii) the numbers evidence review's **improvement** function (mean 7.7 findings/review) — kept prominent — **not** its **gating** function; 0 rejected / 0 superseded + median 0 days-to-decision is consistent with proposals opening only after chat-stage shaping has already filtered the losers, citing `doctrine/lifecycle.md:285-296` **only** for "a pre-proposal shaping stage exists" (R8 — the citation does not itself claim losers are filtered there; present that mechanism as an unverified candidate explanation, not a doctrine-backed fact); (iii) the material update, precisely framed (R4): Cairn's own tree has since produced its first **superseded** proposal (`2026-07-08-claude-automated-review-committer`, superseded 2026-07-09) — review's blocking finding (Internal R1 in that proposal) led the author to *supersede* the proposal in favor of an existing-doctrine practice plus a recurrence-gated follow-up, **not** a hard rejection; state explicitly that the **rejected count stays 0** and supersession is the distinct, non-rejection gating signal. No "kill"/"killing" language (R4). |

### Chunk D — OQ3 (arm the deferred follow-up's recurrence path)

| # | File | Change |
|---|------|--------|
| D1 | `dev/measurement/attestation-replay-failures.md` (new) | Forked from `dev/modules/incident_log_template.md`, structured identically to the `review-floor-deviations.md` precedent (Purpose / Rate-limit gate connection / Rolling window / What counts / Incidents table / Column contract / Goodnight migration). **Event class:** `attestation-replay-failure` — a release-commit gate attestation that does not reproduce when replayed against the identical gate code on the committed cut tree. **Same-shape criteria:** two entries are the same shape if both are a release-commit gate-attestation claim that fails to replay, regardless of which sub-gate or which release. **What does NOT count:** a gate result that changes between the cut and a later replay *because the gate code itself changed* in the interim (a tooling update, not an attestation failure) — this row is NOT that case (the only intervening diff is a comment-only SPDX header, independently confirmed non-functional, this plan's finding 1). **Rolling window:** 14 days, matching the `review-floor-deviations.md` precedent (no proposal-stated reason to diverge). |
| D2 | (same file) | Row 1: **Date = the date this Chunk D commit lands** (not the true 2026-06-12 occurrence — this plan's finding 3; the true date is stated in the row's own Description instead). Event Class `attestation-replay-failure`. Description states both dates plainly: "Release commit `12ec2ad` (v0.3.0, 2026-06-12) attested `quality_gate exit 0`; replay on the immutable cut tree (confirmed 2026-07-11 during `record-corrections` proposal drafting, re-confirmed at this plan's own preparation) yields neutrality exit 1/fail=99, redundancy exit 1/fail=6." Recurrence-Window Match: none (first entry). **Impact: `occurred`** (not `historical` — this plan's finding 3: the point of OQ3 is arming a *forward* recurrence check, which a `historical`-tagged row structurally cannot do, per `evolution_infer.py`'s documented and verified never-counts behavior). Migrated From Reflection: `direct`. Resolved By: **`pending`** — the erratum (Chunk A) documents the incident; the actual recurrence-*prevention* mechanism (the cut-transcript requirement) is the proposal's own explicitly deferred follow-up and has not landed, so nothing has actually "resolved" the underlying gap yet. A tracker-level note (mirroring `review-floor-deviations.md`'s own documented `Impact` local-extension precedent) explains the date-vs-`historical` departure from that precedent's convention and why (this plan's finding 3, reproduced in the file itself so a future reader doesn't have to reconstruct the reasoning from this plan). |

## Archive closeout (required, per R5 — not a separate goodnight step)

The plan's archive commit bundles, alongside the usual Lasting-truth
migration + `dev/plans/` → `dev/plans/archive/` move:

* **`dev/PLANNING.md:34-40`** repointed from the generic "the deliberation
  is in `dev/strategy/`" to name `dev/strategy/2026-07-11-claude-cairn-adoption-record.md`
  concretely — closing the inconsistent-pointer window Chunk B's
  `profile.yml`-only repoint would otherwise leave open (R5).

This mirrors the `adopter-licensing-compliance` plan's own precedent
(its `dev/PLANNING.md` Active-row removal bundled directly into its
archive commit, `82d24bc`) — a lifecycle-transition row-move is within
the no-per-commit-approval carve-in `AGENTS.md` already grants archive
commits.

## Acceptance criteria

* **Tests that must pass** — **N/A for behavioral pytest**, per the
  proposal's own accounting: no code surface is touched by C1/C2/C3/OQ3.
  `python -m pytest bootstrap/tests` stays green (modulo the pre-existing,
  separately-tracked failures already documented by the sibling plans
  this session — the two AST-digest interpreter artifacts under the
  sandbox's non-canonical Python, not this plan's concern).
* **Examples / smoke checks required**:
  * The v0.3.0 replay (Chunk A's primary evidence), reproduced fresh at
    implementation time, not copied from this plan's own preparation
    numbers without re-running: `git archive 12ec2ad | tar -x -C <tmp>`,
    then `python3 scripts/quality_gate.py --sub neutrality` (expect exit
    1, 99 `FAIL`-class lines) and `--sub redundancy` (expect exit 1, 6
    `FAIL`-class lines) in `<tmp>`.
  * `python3 tools/evolution_infer.py` (or its tracker-evaluation entry
    point) run against the new `attestation-replay-failures.md` after
    Chunk D lands, confirming the seeded row parses cleanly and — this
    is the actual test of finding 3's resolution — confirming the row's
    `occurred` Impact with the logging-date choice means a *hypothetical*
    second same-window `occurred` row would trigger the gate (verify by
    temporarily adding a synthetic second row in a scratch copy, not the
    committed file, and confirming `evaluate_tracker` fires — then
    discarding the scratch copy; mirrors this session's established
    mutation-testing discipline).
* **Docs**: `python scripts/check_cairn.py` and `python scripts/claim_check.py`
  clean over every touched/new file (the erratum, the new adoption note,
  the new tracker, the metrics addendum, both repointed pointers).

## Signals the change is wrong

Carried forward from the proposal's own list (`:302-320`), unchanged —
still the right failure signals for this plan's implementation:
the reconstructed adoption record asserting unrecoverable rationale; the
v0.3.0 replay numbers failing to reproduce for a third party; the gating
caveat reading as "review is theater" (over-correction); a shared-comm-
file edit landing at a non-serialization point; OQ1 needing to be
revisited. Add one from this plan's own preparation: **the seeded
tracker row still cannot arm a future recurrence trigger** even after
finding 3's fix — recovery: re-derive `evaluate_tracker`'s cutoff
arithmetic against the row's actual committed date once Chunk D lands
and confirm live, not just reason about it here.

## Review

*Filled in after the fresh-context Internal plan-review subagent pass.*

## Code review

*Filled in after implementation commits land (Chunks A-D).*

## Lasting-truth migration

*Filled in at archive time. Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home
outside the plan — the cut-transcript requirement stays the proposal's
own explicitly deferred, rate-limit-gated follow-up (armed by Chunk D,
not carried by this plan).*

This section is append-only once written.
