<!-- cairn-internal-ref-allow: doctrine/proposals.md doctrine/lifecycle.md doctrine/rationale.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: dev/strategy/2026-07-11-claude-cairn-adoption-record.md, dev/measurement/attestation-replay-failures.md -->
<!-- The two paths above are forward-reference files this plan creates; they materialize as Chunks B and D land. -->

# Plan: record corrections (C1, C2, C3, OQ3 tracker)

**Source proposal**: `dev/proposals/archive/2026-07-11-claude-record-corrections.md`
**Status**: review
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
| A1 | `CHANGELOG.md` | Append one entry to the existing `## Unreleased` > `### Fixed` subsection (below the one current entry). **Content simplified from the Revised proposal's design (`:420-427`) at the Maintainer's explicit direction during implementation-time approval, 2026-07-22** — the original design (quoted attestation, per-sub-gate refutation, the OR-aggregation argument, the order-independence caveat, the sweep cross-reference) is exactly the deliberation content `CHANGELOG.md:22-28`'s own entry-shape rule says does **not** belong inline ("the changelog curates and points"; the existing precedent `### Fixed` entry is 3 dense sentences, not a walkthrough). Final, approved one-line entry: **"Corrected the `v0.3.0` release commit's quality-gate attestation** (claimed a clean run; didn't reproduce on replay) **— see `dev/proposals/archive/2026-07-11-claude-record-corrections.md`."** All of the elaborate content this replaces — the exact FAIL counts, the sub-gate precision (R3), the OR-aggregation refutation (R7), the sweep cross-reference (R11), this plan's own finding-1 gate-code-drift correction and finding re: the broad-look citation drift (PR2) — lives in the linked proposal already; nothing is lost, only not duplicated a second time in a file whose own convention argues against it. |

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
| C1 | `dev/strategy/2026-05-20-claude-team-productivity-metrics.md` | Append a dated "**Gating-function caveat (\<the date this commit lands\> addendum)**" — dated at commit-landing time, not backdated to 2026-07-11 (plan-review PR3: unlike C2, no Decision-level OQ pins C3's date, so it follows the general honesty-guard principle of recording at true landing time) — directly below the existing 2026-05-19 baseline bullet list (`:149-153`, ending "Median `days_to_decision` = 0 days") — append-only, the original analysis at `:149-153` is untouched. Content, per the Revised proposal `:433-435`: (i) the corpus is a **modflow_tools** 2026-05-19 baseline, not Cairn's own tree; (ii) the numbers evidence review's **improvement** function (mean 7.7 findings/review) — kept prominent — **not** its **gating** function; 0 rejected / 0 superseded + median 0 days-to-decision is consistent with proposals opening only after chat-stage shaping has already filtered the losers, citing `doctrine/lifecycle.md:285-296` **only** for "a pre-proposal shaping stage exists" (R8 — the citation does not itself claim losers are filtered there; present that mechanism as an unverified candidate explanation, not a doctrine-backed fact); (iii) the material update, precisely framed (R4): Cairn's own tree has since produced its first **superseded** proposal (`2026-07-08-claude-automated-review-committer`, superseded 2026-07-09) — review's blocking finding (Internal R1 in that proposal) led the author to *supersede* the proposal in favor of an existing-doctrine practice plus a recurrence-gated follow-up, **not** a hard rejection; state explicitly that the **rejected count stays 0** and supersession is the distinct, non-rejection gating signal. No "kill"/"killing" language (R4). |

### Chunk D — OQ3 (arm the deferred follow-up's recurrence path)

| # | File | Change |
|---|------|--------|
| D1 | `dev/measurement/attestation-replay-failures.md` (new) | Forked from `dev/modules/incident_log_template.md`, structured identically to the `review-floor-deviations.md` precedent (Purpose / Rate-limit gate connection / Rolling window / What counts / Incidents table / Column contract / Goodnight migration). **Event class:** `attestation-replay-failure` — a release-commit gate attestation that does not reproduce when replayed against the identical gate code on the committed cut tree. **Same-shape criteria:** two entries are the same shape if both are a release-commit gate-attestation claim that fails to replay, regardless of which sub-gate or which release. **What does NOT count:** a gate result that changes between the cut and a later replay *because the gate code itself changed* in the interim (a tooling update, not an attestation failure) — this row is NOT that case (the only intervening diff is a comment-only SPDX header, independently confirmed non-functional, this plan's finding 1). **Rolling window: 90 days** (revised per plan-review PR1 — *not* the 14 days `review-floor-deviations.md` uses; the window is documented as an explicit per-tracker adopter choice, `dev/modules/incident-trackers.md:136-142`, not a fixed default). Stated rationale, recorded in the tracker file itself: `attestation-replay-failure` attaches to **release commits**, a much lower-frequency event than review-floor process deviations (which can recur every proposal); Cairn's own release history (`CHANGELOG.md`'s dated section headers: 0.1.0 2026-05-20 → 0.1.1 2026-05-21 → 0.2.0 2026-05-27 → 0.3.0 2026-06-12) shows gaps of 1, 6, and 16 days — already exceeding a 14-day window during Cairn's fastest development phase, and gaps are expected to widen as the project matures toward 1.0; 90 days gives a row real multi-month liveness against a realistic next-release attestation. |
| D2 | (same file) | Row 1: **Date = 2026-06-12, the true occurrence date** (`12ec2ad`'s actual commit date — revised per plan-review PR1; *not* the commit-landing date this plan originally proposed, which would have broken `dev/modules/incident_log_template.md:40`'s column contract, "ISO date of the incident," for no lasting benefit). Event Class `attestation-replay-failure`. Description: "Release commit `12ec2ad` (v0.3.0, 2026-06-12) attested `quality_gate exit 0`; replay on the immutable cut tree (confirmed 2026-07-11 during `record-corrections` proposal drafting, re-confirmed at this plan's own preparation and again at plan-review) yields neutrality exit 1/fail=99, redundancy exit 1/fail=6." Recurrence-Window Match: none (first entry). **Impact: `occurred`** — the point of OQ3 is arming a *forward* recurrence check; with the corrected 90-day window and the true occurrence date, this row is live (within-window) for roughly two and a half months from today, giving real room for a genuine second incident to combine with it, unlike a `historical`-tagged row (which `evolution_infer.py` documents and this session verifies as never counting) or the originally-proposed commit-landing date (which would only have restarted an equally-short 14-day clock from an arbitrary anchor). Migrated From Reflection: `direct`. Resolved By: **`pending`** — the erratum (Chunk A) documents the incident; the actual recurrence-*prevention* mechanism (the cut-transcript requirement) is the proposal's own explicitly deferred follow-up and has not landed, so nothing has actually "resolved" the underlying gap yet. |

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
    Chunk D lands, confirming the seeded row parses cleanly and — this is
    the actual test of finding 3's resolution, sharpened per plan-review
    PR1 — confirming the row is genuinely **live now**, not just
    trivially live against a same-day synthetic row: compute
    `cutoff = today - 90` and confirm `2026-06-12 >= cutoff` holds at
    verification time, then, in a scratch copy (not the committed file),
    add a second synthetic `occurred` row dated **realistically distant**
    from today (e.g. 60-80 days out, simulating a next release landing on
    a cadence in line with the observed 1/6/16-day gaps but slower, not a
    same-day row) and confirm `evaluate_tracker` fires; discard the
    scratch copy afterward (mirrors this session's established
    mutation-testing discipline, extended per the review's critique that
    a same-window-by-construction test proves nothing about whether the
    window itself is well-chosen).
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

**Attribution / committer note.** Fresh-context subagent plan-review; the
subagent cannot commit, so the author-session commits this section as a
disclosed scribe, the accepted deviation model used throughout this
repo's lifecycle.

## Plan review -- Claude (Internal, fresh-context) -- 2026-07-22

**Model**: Claude Sonnet 5

**Steelman.** This plan does exactly what a plan should: it translates an already-heavily-reviewed design (12 Internal + 4 External findings, all accepted, a Maintainer Decision) into concrete, faithful chunks, and it does not treat "already accepted" as license to stop verifying. All three claims disclosed in its own "Context" section reproduce independently: the gate-code diff is genuinely comment-only (12 lines, one commit, SPDX header, zero AST effect), the v0.3.0 replay numbers are exact (neutrality exit 1/99, redundancy exit 1/6), and the six-axis citation correction is real (the framework note names the axes but not this project's point on them; `BOOTSTRAP.md:178-181` is the actual technical source). The approval-gate flag on Chunk A is correctly reasoned against `AGENTS.md`'s actual carve-in text, not just asserted. `check_cairn` and `claim_check` are genuinely clean at HEAD, and the two citation-break fixes the commit message claims did land. The plan's own "Signals the change is wrong" list already flags residual risk on the tracker-arming fix ("re-derive `evaluate_tracker`'s cutoff arithmetic... and confirm live, not just reason about it here") — an honest hedge rather than false confidence. This is a well-disciplined translation pass.

**Findings** (most significant first):

* **[PR1] Finding 3's diagnosis is correct, but its proposed fix (shift the Date, keep the 14-day window) is not the best available resolution — a deliberately-chosen, longer rolling window is superior and was not seriously considered.**

  The mechanics diagnosis checks out exactly. `tools/evolution_infer.py:187` computes `cutoff = today - datetime.timedelta(days=window)` where `today = datetime.date.today()` (line 284) — evaluation-time, not incident-time — and `evaluate_tracker` (lines 176-196) only counts a row where `inc["impact"] == "occurred" and inc["date"] >= cutoff`. With a 14-day window evaluated today (2026-07-22), `cutoff = 2026-07-08`; the true incident date `2026-06-12` is 40 days prior and already excluded (`2026-06-12 >= 2026-07-08` is `False`, confirmed by direct computation). A truthfully-dated `occurred` row is DOA before Chunk D even lands — the plan is right about this.

  But the plan's fix — date the row at Chunk D's commit-landing date instead, with the true date pushed into Description, plus a tracker-level note explaining the departure — only buys a **new, equally-perishable ~14-day grace window starting from an arbitrary anchor** (whenever the commit happens to land), not a durable fix. It also breaks the column contract: `dev/modules/incident_log_template.md`'s "Column contract" defines `Date` as **"ISO date of the incident"** (line 40) — not date-of-logging — and this is the schema `dev/modules/incident-trackers.md` says "Goal 7's eventual cross-adopter harvest reads against" (line 41-42). Corrupting `Date`'s meaning for one row (even disclosed in prose) is a different and arguably worse kind of departure than the `historical` Impact-value extension it's modeled on, which only added a new enum *value*, not redefined an existing column's semantics.

  Critically, `dev/modules/incident-trackers.md:141` and `doctrine/rationale.md:327-329` both confirm the window is explicitly an **adopter/per-tracker choice** ("the window length is an adopter choice"; "typically 14 days" is a default, not a mandate) — so there is no doctrinal reason the plan had to inherit 14 days from `review-floor-deviations.md`, a tracker built for a much higher-frequency event class (review-floor process deviations, which can recur on nearly every proposal). `attestation-replay-failure` is tied to **release commits**, and Cairn's own release history (`git log --grep`) shows v0.1.0→v0.1.1 (1 day), v0.1.1→v0.2.0 (6 days), v0.2.0→v0.3.0 (**16 days** — already exceeding 14) — a cadence a 14-day window barely fits even now, during the fastest phase of development, and will fit worse as the project matures and releases slow down.

  A cleaner fix exists and preserves everything the plan's own fix sacrifices: **keep the true date (`2026-06-12`), keep `Impact: occurred`, and choose a longer, deliberately-justified window** (e.g., on the order of 60-90+ days, sized to Cairn's actual observed release cadence) instead of reflexively copying the precedent tracker's window. This keeps `Date` meaning what the schema says it means, needs no tracker-level "departure from precedent" note, and — unlike the plan's fix — gives the row genuine multi-week/multi-month "liveness" against the *next* release's attestation, rather than a ~14-day grace period that itself expires before most realistic next-release timelines.

  The plan's own acceptance-criteria mutation test (adding "a hypothetical second same-window occurred row" in a scratch copy) doesn't catch this: it only proves the mechanism fires for a synthetically-nearby row, which is true by construction regardless of whether 14 days is the right window — it never tests against a realistically-spaced future incident.

  *Grounding:* `tools/evolution_infer.py:176-196` and `:284` (read in full); `dev/measurement/review-floor-deviations.md:19` (14-day window) and `:38-48` and `:54-55` (`historical` extension documented and both precedent rows dated `2026-06-12` true-occurrence); `dev/modules/incident_log_template.md:14` (window is a per-tracker `<adopter-chosen value>`) and `:40` (Date column contract = "ISO date of the incident") and `:48-58`; `dev/modules/incident-trackers.md:136-142` ("the window length is an adopter choice... typically 14 days"); `doctrine/rationale.md:327-329`; release-cadence from `CHANGELOG.md`'s dated section headers (0.1.0→0.3.0, gaps of 1/6/16 days); date arithmetic computed directly (`cutoff = 2026-07-08` vs. incident date `2026-06-12`, 40 days elapsed).
  *Suggested fix:* Revise Chunk D1/D2 to keep `Date = 2026-06-12` (true occurrence) and `Impact: occurred`, and choose a rolling window with a stated rationale tied to Cairn's own release cadence (not "no proposal-stated reason to diverge" from an unrelated tracker's window) — long enough that the row stays live across a realistic next-release gap. This drops the need for the Date-vs-`historical` departure note entirely and keeps the column contract intact.

* **[PR2] A second, previously-uncaught citation drift — parallel in kind to the plan's own Finding 1 — is about to land wrong in a permanent CHANGELOG.md record.**

  Chunk A's erratum text cross-references "broad-look Theme 1 item 3 (`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:142-148`, the skipped v0.3.0 pre-release sweep)" — inherited verbatim from the accepted proposal's Revised-proposal section and R11's grounding. This citation **was accurate when the proposal was authored and reviewed** (verified: at commit `5575e48~1`, lines 142-148 do contain item 3, the skipped-sweep discussion). But commit `5575e48` ("dev/strategy: correct the broad-look note's Bandit finding," **same day**, 2026-07-22, 12:02:16 -0400) inserted a 43-line "Corrections since publication" section earlier in the same file, shifting everything after it down. At current HEAD, lines 142-148 land on the "Theme 1" section header and lead-in prose, not item 3; the skipped-sweep discussion is now at **lines 173-179**. This is structurally the same failure class as Finding 1 (a same-day, unrelated commit invalidating a citation the proposal/reviews verified earlier) — but the plan did not catch it, despite explicitly re-verifying the parallel `quality_gate.py` citation issue in the same session. `check_cairn`/`claim_check` cannot catch this: they validate that a path exists and a line number is in-bounds, not that the cited range's *content* matches the prose describing it (exactly the class of gap `AGENTS.md`'s "Verifying claims" section describes as outside the checker's reach).

  *Grounding:* `git log --format="%h %ad %s" -- dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md` (commit `5575e48`, 2026-07-22); `git show 5575e48 --stat` (+43/-6 lines); `git show 5575e48~1:...md | sed -n '135,150p'` (item 3 at old 142-148); current `grep -n "" ...md | sed -n '168,182p'` (item 3 now at 173-179; old 142-148 now covers the Theme 1 header/lead-in).
  *Suggested fix:* Before Chunk A's commit lands, update the cross-reference to `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:173-179`, and re-run `claim_check`/a manual content spot-check on any other line-pinned citation this plan carries into a permanent artifact, since the checker will not catch this class of drift.

* **[PR3] Chunk C's addendum date ("2026-07-11") has no stated rationale and no governing OQ, unlike Chunk B's date (which OQ4 explicitly resolves).**

  Chunk C hardcodes the addendum heading as "**Gating-function caveat (2026-07-11 addendum)**." Neither the accepted proposal nor the Decision pins a date for C3's text the way OQ4 pins C2's adoption-record date ("confirm the reconstructed adoption record is dated 2026-07-11, not backdated"). Given this proposal's own honesty-guard spirit runs throughout (record artifacts at their true authoring/landing time, not an earlier date associated with the underlying idea), it's worth an explicit one-line justification in the plan: either the addendum text is genuinely verbatim from the 2026-07-11 proposal draft (defensible), or it should carry the actual date Chunk C's commit lands (likely later, given the plan and both review rounds post-date 2026-07-11).

  *Grounding:* `dev/plans/record-corrections.md:161` (hardcoded "2026-07-11 addendum"); proposal Correction 3 / Revised-proposal Correction 3 section (no date specified); Decision (`:541-565`, OQ4 dates only C2).
  *Suggested fix:* Add one sentence to Chunk C stating why 2026-07-11 is the right date for this addendum (or switch it to the commit-landing date for consistency with the pattern OQ4 sets for C2).

**Coverage.** Independently reproduced: the `quality_gate.py` diff (12 lines, comment-only, commit `501efe3`) and the full v0.3.0 replay (neutrality exit 1/99 `FAIL`-class lines, redundancy exit 1/6, both exact matches, scratch dir cleaned up afterward). Independently grepped the framework note (zero six-axis point-value hits; `dimensions/` mentioned only as existing) and confirmed `bootstrap/BOOTSTRAP.md:178-181` + `profile.yml:14-16` match exactly once the `human_team: solo` override is applied. Read `evaluate_tracker()` and `main()` in full and worked the cutoff arithmetic by hand against both the plan's fix and an alternative (longer-window) fix; read `review-floor-deviations.md` in full including its `Impact` semantics and both historical rows. Verified every Chunk A-D bullet against the "Revised proposal" section and Decision text line-by-line; found the design faithfully carried except PR1-PR3 above. Verified the `AGENTS.md` shared-communication-file carve-in text directly — the plan's characterization of Chunk A's approval gate (CHANGELOG additions auto-carve *only* in the single goodnight-handoff commit, not a standalone implementation commit) is accurate, neither overstated nor understated. Ran `check_cairn.py` (OK, 162 files) and `claim_check.py` on the plan, the archived proposal, and the sibling `transition-lint.md` proposal — all clean at current HEAD, and independently confirmed the two citation-break fixes the commit message claims (the `dev/proposals/2026-07-22-claude-transition-lint.md` claim-marker-maintenance note and `claim-check-allow`) are real and correctly scoped. Verified the `82d24bc` archive-commit precedent the plan cites for its `PLANNING.md` row-move exists and does what's claimed. **Not independently exercised**: the actual prose content of the not-yet-written `dev/strategy/2026-07-11-claude-cairn-adoption-record.md` and the tracker file itself (both forward-referenced, materializing only when Chunks B/D land) — this is squarely out of reach for a plan-review pass and is correctly flagged by the plan itself as the negative-space item neither proposal-stage review could exercise either.

**Verdict:** Proceed with the fixes above folded in. PR2 must be corrected before Chunk A's commit (it is about to write a now-stale citation into a permanent CHANGELOG.md record). PR1 should be resolved before Chunk D lands — my recommendation is to keep the true incident date and `Impact: occurred`, and choose a rolling window sized to Cairn's actual release cadence rather than reflexively inheriting `review-floor-deviations.md`'s 14 days; if the plan's author disagrees and prefers the date-shift approach, that's a defensible fallback but should be adopted as a *considered* choice against this alternative, not a default. PR3 is a minor confirm-or-fix item. Nothing here reopens the proposal-stage design; all findings are translation/implementation-time corrections within the plan's own remit.

### Sharpening -- Claude (author) -- 2026-07-22

All three findings independently re-verified before disposing (not taken
on the reviewer's word) — PR2's citation drift reproduced exactly
(`5575e48~1` has item 3 at `:142-148`; current HEAD has it at
`:173-179`, confirmed by direct `sed` read of both ranges), and PR1's
release-cadence numbers reproduced from `CHANGELOG.md`'s own dated
section headers (0.1.0 2026-05-20 → 0.1.1 2026-05-21 → 0.2.0 2026-05-27
→ 0.3.0 2026-06-12: gaps of 1, 6, 16 days, matching the review exactly).

* **[PR1] accept.** The reviewer's alternative is genuinely better, not
  just different: it keeps `Date` meaning what
  `dev/modules/incident_log_template.md:40`'s column contract says
  ("ISO date of the incident"), needs no tracker-level departure note,
  and gives real multi-month liveness instead of a ~14-day window that
  restarts from an arbitrary commit-landing anchor. Revised: Chunk D1/D2
  now keep `Date = 2026-06-12` (true occurrence) and `Impact: occurred`,
  with a **90-day** rolling window — chosen over the reviewer's "60-90+"
  range at the long end of that band since the one observed gap that
  matters most (v0.2.0→v0.3.0, 16 days) is from Cairn's *fastest*
  development phase; 90 days gives real margin as release cadence slows
  toward 1.0 without being arbitrarily unbounded. Stated explicitly in
  the tracker file itself (not just this plan), citing the three
  observed gaps as the rationale — an adopter-choice per
  `dev/modules/incident-trackers.md:136-142`, not a doctrine deviation.
* **[PR2] accept — corrected before Chunk A lands.** Re-verified
  directly: `git show 5575e48~1:dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md`
  lines 142-148 hold item 3's text; current HEAD's lines 142-148 are the
  "Theme 1" header and lead-in, and item 3 is now at `:173-179`. Chunk
  A's cross-reference is corrected to the current line range.
* **[PR3] accept.** Chunk C's addendum date is switched from a
  hardcoded "2026-07-11" to the date Chunk C's own commit actually
  lands — consistent with the honesty-guard spirit the whole proposal
  argues for (record artifacts at their true landing time), and honest
  about the fact that the addendum, unlike C2, has no Decision-level
  date pin (OQ4 governs only C2).

**Status: open → executing.** All findings disposed; implementation
begins next (Chunks A-D in sequence, Chunk A's commit gated on separate
explicit approval per its own flag above).

## Code review

**Attribution / committer note.** Fresh-context subagent review of the
four implementation commits; the subagent cannot commit, so the
author-session commits this section as a disclosed scribe, the accepted
deviation model used throughout this repo's lifecycle.

## Code review -- Claude (sub-agent, fresh context, not the implementer) -- 2026-07-22

**Verdict: Request changes**, applying to the four commits `9a95ee0`
(Chunk A), `59885ec` (Chunk B), `84c23a0` (Chunk C), `938aa20` (Chunk D).
Chunks A, C, and D independently verify clean end-to-end. Chunk B
contains two real, independently-reproduced content defects in the new
adoption-record note — neither fabricates deliberation (the
honesty-guard boundary holds), but both are factual misstatements a
skeptical reader who follows the citations would catch, exactly the
failure class this whole proposal exists to correct.

**Model**: Claude Sonnet 5, fresh session, no access to the implementing
session. Read all four diffs in full, the plan (including Plan review +
Sharpening), the accepted proposal's Revised proposal + Decision, and
independently re-ran every gate the commit messages cite.

### Falsification ledger

**Chunk A — clean.** CHANGELOG.md entry matches the plan's
post-simplification A1 spec verbatim. Independently replayed `12ec2ad`
in a scratch dir: `--sub neutrality` exit 1/99 `FAIL`-class,
`--sub redundancy` exit 1/6 `FAIL`-class — exact match. Gate-code diff
confirmed comment-only (12 lines, SPDX header). The stale broad-look
citation PR2 flagged turned out moot in the shipped one-line entry (it
doesn't cite that note at all). Approval-gate framing against `AGENTS.md`
confirmed accurate.

**Chunk B — two real defects, both fixed post-review (see Sharpening).**

* **[CR1, blocking] Three of four `profile.yml` line citations in the
  new adoption record were off by exactly one line**, because the same
  commit's B2 edit expanded `profile.yml:7-8`'s comment from 1 line to 2,
  shifting everything below down by +1 — *within the same commit* the
  note was drafted against the pre-edit numbering. Directly diffed
  `59885ec^` vs `59885ec`: the six-axis comment cited as `:14-16` is
  actually at `:15-17`; the preset/`human_team` cited as `:17-18` is
  actually at `:18-19`; the `modules_add` block cited as `:20-23` is
  actually at `:21-24` (only 2 of 3 entries, missing
  `examples-gallery`). Only `profile.yml:7` (preceding the insertion
  point) survived correctly. `claim_check` passed throughout — it only
  bounds-checks, doesn't read cited-range content — confirming this is
  the same failure class as plan-review's own PR2 finding, this time
  self-inflicted within Chunk B's own commit and uncaught there.
* **[CR2, blocking] The note misstated `dimensions/README.md`'s axis
  grouping** as "three describing the codebase (age, size, complexity),
  three describing the team (language, human-team, agent-team)" — a
  false 3/3 split. `dimensions/README.md:15-37` (read directly) actually
  defines **four** codebase axes (age, size, complexity, **language**)
  and **two** team axes (human-team, agent-team) — a 4/2 split. The axis
  *point values* and their mapping onto `profile.yml`'s six-axis comment
  were unaffected — only the note's descriptive claim about its own
  cited source's structure was wrong.
* Minor: the commit message's `check_cairn OK (163 files)` undercounts
  by one (actual: 164) — a self-verification ordering slip (checked
  before `git add`, not after), not a content defect.

**Chunk C — clean.** Genuinely append-only (29 insertions, 0 deletions
against the original baseline bullets). `doctrine/lifecycle.md:280-296`
cited precisely (shaping-stage-exists only, not losers-die-there).
`automated-review-committer`'s Decision confirmed "Superseded," not
rejected; grepped every `**Status**:` field across `dev/proposals/` +
archive (12 proposals) — exactly one superseded, zero rejected. Dated at
actual commit-landing time (2026-07-22), matching PR3's fix.

**Chunk D — clean, and the fix genuinely works, not just reads well.**
`parse_rolling_window` resolves to 90 against the committed file;
`evaluate_tracker` confirms the seeded row (`2026-06-12`, `occurred`) is
live as of today (cutoff `2026-04-23`). A scratch-copy mutation test
(discarded after) with a synthetic second row dated **70 days** after
the true incident — a realistically-spaced next-release gap, not a
same-day trivial case — confirmed the recurrence trigger genuinely
fires at threshold=2, directly validating plan-review PR1's fix rather
than just trusting its prose. Release-cadence numbers (1/6/16-day gaps)
re-verified directly from `CHANGELOG.md`. Minor: commit message's
`check_cairn OK (164 files)` undercounts by one (actual: 165), same
class of slip as Chunk B's.

### Gate sweep at current HEAD

Full suite: 1432 passed / 3 skipped / 2 failed (both the documented
pre-existing `test_ast_attest.py` sandbox-interpreter artifacts).
Canonical `lhm` interpreter: `test_ast_attest.py` 26/26 green — confirms
zero AST impact, as this plan (touching no code) claims.
`check_cairn.py` OK, 165 files. `claim_check.py` clean on every
touched/new file. `quality_gate.py --sub neutrality` at 99 FAILs,
matching the pre-existing baseline, none from the touched files. Scope
discipline: each chunk touches only its table's files; Chunk A
additionally touches the plan itself (the disclosed Maintainer
simplification), not scope creep.

### Coverage

Independently verified: the v0.3.0 replay, the gate-code diff, every
`profile.yml` citation in the new note against the actual committed
file (both pre- and post-edit numbering), the `dimensions/README.md`
grouping against the note's paraphrase, `bootstrap/BOOTSTRAP.md`'s
preset table, the 2026-05-14 framework note's actual content, the
metrics addendum's append-only property and citation precision, the
supersession-vs-rejection framing against every proposal's `Status`
field, `evolution_infer.py`'s rolling-window/recurrence mechanics (both
as-shipped and via mutation test), the release-cadence dates, and the
full gate sweep. Not independently exercised: whether explicit
Maintainer approval was actually given in conversation before Chunk A's
commit (git authorship is consistent with, not conclusive proof of, the
claimed gate); the redundancy/order-independence sub-gate replay (task
scope specified neutrality only); the plan's own header `Status` field,
which still read `open` despite the body's executing transition and all
four chunks landed (predates Chunks A-D, introduced at the plan-review
commit `b533596`, uncorrected by any of them).

### Required follow-ups

1. **(Blocking, resolved post-review)** The three drifted `profile.yml`
   citations in the adoption record, corrected: `:14-16` → `:15-17`,
   `:17-18` → `:18-19`, `:20-23` → `:21-24`.
2. **(Blocking, resolved post-review)** The axis-grouping misstatement,
   corrected to the accurate 4-codebase/2-team split.
3. **(Non-blocking, noted)** Chunk B/D commit-message file-count slips —
   no action; a habit note for future commits (run `check_cairn` after
   staging, not before).
4. **(Non-blocking, resolved post-review)** The plan's header `Status`
   field, corrected from `open` to `executing`.

### Sharpening -- Claude (author) -- 2026-07-22

Both blocking findings independently re-verified before fixing (not
taken on the reviewer's word): re-read `profile.yml` with line numbers
and confirmed the three citations were exactly as drifted as CR1
describes; re-read `dimensions/README.md:15-37` directly and confirmed
the 4/2 split CR2 describes, not the note's claimed 3/3.

* **[CR1] accept — fixed.** `dev/strategy/2026-07-11-claude-cairn-adoption-record.md`'s
  three citations corrected to `:15-17`, `:18-19`, `:21-24`, verified
  against the actual file content post-fix.
* **[CR2] accept — fixed.** The axis-grouping sentence corrected to
  "four describing the codebase (age, size, complexity, language), two
  describing the team (human-team, agent-team)."
* **[Minor findings] accept, noted, no further action needed** — the
  commit-message undercounts are historical (not rewriting past commit
  messages); the Status field is fixed in this same commit.

**Status: executing → review.** Code review's two blocking findings are
resolved; the plan is otherwise complete and gate-clean. Archive next.

## Lasting-truth migration

*Filled in at archive time. Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home
outside the plan — the cut-transcript requirement stays the proposal's
own explicitly deferred, rate-limit-gated follow-up (armed by Chunk D,
not carried by this plan).*

This section is append-only once written.
