<!-- Forward-reference paths this proposal plans to create (the adoption record) or that materialize in its implementing plan / archive move. -->

# Record corrections: the v0.3.0 attestation erratum, the missing adoption-decision record, and the zero-rejections gating-function caveat

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-07-11
**Status**: accepted
**Touches**: `CHANGELOG.md` (an `## Unreleased` erratum entry); a new deliberation note `dev/strategy/2026-07-11-claude-cairn-adoption-record.md`; a dated addendum to `dev/strategy/2026-05-20-claude-team-productivity-metrics.md`; pointer edits to `dev/.cairn/profile.yml` (comment) and `dev/PLANNING.md`. No `doctrine/`, no code, no install-contract surface.
**Related**: broad-look review `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md` (Theme 1; its A1 recommendation items 2, 3, 5 at `:543-549`). Sibling **accepted** `2026-07-08-claude-review-record-integrity` — carried A1 items 1 + 4, and its Internal review **R12** (`dev/proposals/archive/2026-07-08-claude-review-record-integrity.md:385-391`) explicitly flagged *this* remainder ("the v0.3.0 release-notes correction, the adoption-decision note, and the zero-rejections explanation are absent"). **Superseded** `2026-07-08-claude-automated-review-committer` — the model for a rate-limit-gated deferral (its Decision `:456-463`). The v0.3.0 cut is commit `12ec2ad`.
**Plan review**: required(Internal) — this edits the deliberation record, writes a reconstructed record, and edits two shared communication files; Internal floor now (fresh-context), with an External (cross-type) read **recommended** before the Decision because this proposal is itself *about* the record-integrity differentiator (the same reasoning the sibling proposal used, `:406-416`). Ratified at Decision.

## Context

The broad-look audit's Theme 1 — "Cairn's own deliberation record has verifiable
cracks exactly where a skeptic looks first" — was only partly repaired. The
sibling `review-record-integrity` proposal carried the review/transition slice
(A1 item 1, the showcase-arc provenance; A1 item 4, the review-floor-deviation
ledger). Its own Internal review closed with **R12**
(`dev/proposals/archive/2026-07-08-claude-review-record-integrity.md:385-391`):
the three *record-of-fact* slices were left undone, and "A Maintainer tracking
Phase A would mark A1 done at ~40%." This proposal is those three slices —
verified independently this session:

1. **The v0.3.0 release attestation does not replay.** The cut commit
   `12ec2ad`'s body attests: `"quality_gate exit 0 (neutrality
   all-info/justified; 6 advisory R6 redundancy notes ... accepted for a private
   cut)"`. Replaying the **identical gate code** on the **committed cut tree**
   (`git archive 12ec2ad | tar -x`, then `python scripts/quality_gate.py`)
   yields `--sub neutrality` **exit 1, fail=99** (FAIL-class vendor tokens, not
   "all-info/justified") and `--sub redundancy` **exit 1, fail=6** (FAIL-class,
   not "advisory"). The gate code is byte-identical between the cut and HEAD
   (`git diff 12ec2ad HEAD -- scripts/quality_gate.py` → empty; no commits touch
   it in `12ec2ad..HEAD`), and the sub-gates scan by filesystem walk
   (`scripts/quality_gate.py:455` use `rglob`), so the archived tree
   replays faithfully. The audit reached the same 99/6 counts independently
   (`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md:135-142`). A
   release commit carrying a false gate-green attestation is the exact failure
   class the methodology sells protection against.

2. **The adoption-decision record does not exist.** `dev/.cairn/profile.yml:7-8`
   states the profile was "Accepted by the Maintainer on 2026-06-12 (Act I-6).
   The deliberation behind it lives in `dev/strategy/` (the adoption record),"
   and `dev/PLANNING.md:34-40` repeats it ("the deliberation is in
   `dev/strategy/`"). No such document exists: `grep -rn "collaborative-team"
   dev/strategy/` returns only unrelated mentions (line-count audits, the
   framework note's generic six-axis discussion) — nothing that records the
   preset choice (`profile.yml:17-18`: `collaborative-team` + `human_team: solo`
   override), the six-axis point, or the three added modules
   (`profile.yml:20-23`). The audit flags exactly this dangling pointer
   (`...broad-look...:149-151`, "A pointer to a decision record leads nowhere").

3. **The zero-rejections fact is unstated where the numbers are presented.** The
   only measured corpus (`dev/strategy/2026-05-20-claude-team-productivity-metrics.md:149-153`)
   is a **modflow_tools** 2026-05-19 baseline: 51 proposals, 49 accepted, **0
   rejected, 0 superseded**, 50/51 revised, mean 7.7 findings/review, 80%
   cross-type, median `days_to_decision` = 0. The *improvement* function is
   well-evidenced (7.7 findings/review); the *gating* function is not — a
   skeptic reads ~96% same-day acceptance as an accept-ceremony
   (`...broad-look...:162-171`). The candidate honest explanation — bad ideas
   die in chat-stage shaping before a proposal is ever written — is
   half-acknowledged at `doctrine/lifecycle.md:285-296` ("Chat preferences are
   not a lifecycle Decision") but stated nowhere near the numbers. A materially
   relevant update now exists: Cairn's own self-hosted tree has produced its
   **first superseded proposal** (`2026-07-08-claude-automated-review-committer`,
   killed by its Internal review, Decision 2026-07-09) — the first recorded
   instance of review performing its *kill* function, not just its improvement
   function.

The fix follows the sibling's shape and its resolved pattern — **correct the
record in a durable, discoverable home; where the original artifact is closed or
immutable, add a discoverable pointer (link-maintenance); where the record is
merely missing, create it; never rewrite a closed artifact** — applied to three
record types with three type-appropriate homes.

## Proposed paths

*(Files this proposal creates or that materialize in its plan / archive.)*

Proposed paths:
- `dev/strategy/2026-07-11-claude-cairn-adoption-record.md` — the reconstructed adoption-decision note (Correction 2); lands with the implementing commit.
- `dev/plans/record-corrections.md` — the implementing plan (opens after acceptance; archives this proposal).
- `dev/proposals/archive/2026-07-11-claude-record-corrections.md` — this proposal's archive path after plan-open.

## Proposal

Three corrections, one argument (Cairn's durable record must honestly represent
its release attestations, its own adoption decision, and its review-gating
evidence), plus one **explicitly split-out** follow-up.

### Correction 1 — the v0.3.0 attestation erratum

The false attestation lives in an **immutable** commit body (`12ec2ad`, tagged
`v0.3.0`) and is echoed by the closed `## 0.3.0 — 2026-06-12` CHANGELOG entry.
History is not rewritten (see Alternative 3). Instead:

* **Record the erratum** as a dated entry under the **open** `## Unreleased`
  CHANGELOG section (a `### Fixed` / correction entry): name commit `12ec2ad`,
  quote its `quality_gate exit 0` claim, state the replay result (`--sub
  neutrality` exit 1 / fail=99; `--sub redundancy` exit 1 / fail=6, as_of
  2026-07-11, reproducible from the immutable cut tree + identical gate code),
  and adopt the audit's honest framing: the likely cause is a hand-written
  attestation from a partial/remembered gate run, not fabrication, but the
  record must say so because a reader cannot otherwise tell the two apart. The
  erratum folds forward into the 0.4 release notes at the next cut.
* **Open question (OQ1)** — whether a single dated **link-maintenance pointer**
  may also be added *into* the closed `## 0.3.0` entry (mirroring the sibling's
  top-of-file pointer on a closed proposal file,
  `doctrine/proposals.md:136-140`), or whether the CHANGELOG's stricter
  "entries are written once at finalization" rule (`doctrine/proposals.md:132`)
  forbids even a pointer there. **Default:** Unreleased-only, which is
  unambiguously within the rules; the pointer is added only if the Maintainer
  extends the link-maintenance reading to CHANGELOG entries.

### Correction 2 — write the missing adoption-decision record

Create `dev/strategy/2026-07-11-claude-cairn-adoption-record.md` — the document
the two live pointers already promise. It records: the six-axis profile point
(`profile.yml:14-16`); the `collaborative-team` preset + `human_team: solo`
override and why (`:17-18`); the three `modules_add` and the trust-boundary
rationale each carries (`:20-23`); and that the profile was accepted 2026-06-12
(Act I-6). Then **repoint the two dangling references** to name it: the
`profile.yml:7-8` comment and the `dev/PLANNING.md:34-40` line.

**Honesty guard (this is a reconstruction, not a contemporaneous record).** The
note is dated **2026-07-11** and states plainly that it is reconstructed after
the fact — it must **not** be backdated to 2026-06-12 or assert a deliberation
transcript that did not exist (that would repeat the very showcase-arc sin the
sibling corrected). It records only what is recoverable (the `profile.yml`
choices and their evident rationale, cross-referenced to the framework note
`dev/strategy/2026-05-14-claude-human-ai-team-development-framework.md` that
defined the six-axis model) and explicitly marks what is **not** recoverable
(any contemporaneous 2026-06-12 deliberation).

Once the two pointers name a concrete file, `scripts/check_cairn.py`'s existing
claim-path/link check catches any future breakage — so the "pointer leads
nowhere" class is closed by an **existing** mechanism, with no new tool.

### Correction 3 — the zero-rejections gating-function caveat

Append a dated **"Gating-function caveat" addendum** to
`dev/strategy/2026-05-20-claude-team-productivity-metrics.md` (append-only-safe;
it does not rewrite the original analysis at `:149-153`). The addendum records,
where the numbers are presented: (i) the corpus is a modflow_tools 2026-05-19
baseline, not Cairn's own tree; (ii) the numbers evidence review's *improvement*
function (mean 7.7 findings/review), **not** its *gating* function — 0 rejected
/ 0 superseded + median 0 days-to-decision is consistent with proposals opening
only after chat-stage shaping has filtered the losers (the mechanism at
`doctrine/lifecycle.md:285-296`); (iii) the material update: Cairn's own tree
has since produced its first **superseded** proposal
(`2026-07-08-claude-automated-review-committer`, 2026-07-09), the first recorded
instance of review killing a change on its own merits.

### Deferred (split-out) follow-up — a gate transcript in the cut commit

The v0.3.0 attestation failed replay because the gate-green claim was
hand-written, not machine-captured. The natural preventive — **require the cut
commit (or a committed release artifact) to carry a machine-generated gate
transcript** — is a change to the *release/cut process*, i.e. a **doctrine
change**. It is **deliberately not in this proposal**: a false-attestation
incident is a **record-integrity** surface, which is neither the **security**
nor the **data-loss** surface that
`doctrine/rationale.md:333-343` makes the *exhaustive* list for the
single-incident high-risk bypass; and there is exactly **one** such incident, so
the counted-recurrence path (`:325-328`, "the same failure shape occurs again")
is not met. Bundling a doctrine change that cannot clear its own gate is the
error the superseded `automated-review-committer` proposal died on
(`dev/proposals/archive/2026-07-08-claude-automated-review-committer.md:224-236`).
This follow-up is therefore **named and deferred**, with an explicit revival
condition: a **second** attestation-replay failure counted in an appropriate
tracker, **or** an explicit Maintainer high-risk classification. Whether such a
tracker is warranted (and its class) is decided *by that follow-up*, not
invented here — the v0.3.0 erratum is the first (n=1) data point.

### Documentation / doctrine surface

* **Correction 1** edits `CHANGELOG.md` — descriptive/record layer, and a
  **shared communication file** edited only at a serialization point
  (`AGENTS.md > Shared communication files`); it lands at the implementing
  commit under explicit instruction.
* **Correction 2** writes into the **deliberation layer** (`dev/strategy/`) and
  edits two pointers (`dev/.cairn/profile.yml` comment — deliberation-adjacent
  machine-state; `dev/PLANNING.md` — a shared comm file, so its pointer edit
  lands at a serialization point, e.g. goodnight or the plan archive).
* **Correction 3** appends to a **deliberation-layer** note (`dev/strategy/`).

Per the doc-tier home rule, **none of the three routes to `AGENTS.md` or
`doctrine/`** — they are records, not rules. The one change that *would* be
doctrine (the cut-process transcript requirement) is split out above precisely
because it cannot clear the rate-limit gate now.

### Doctrine-change rate-limit (if this proposal changes doctrine)

**N/A — this proposal changes no doctrine.** All three corrections are
record-of-fact edits in the deliberation/descriptive layers. The gate governs
*new* doctrine; the only doctrine-shaped idea (the cut transcript requirement)
is explicitly deferred and rate-limited above, not carried here.

## Rationale

* **Which user workflow does it improve?** The first external adopter's *study*
  of Cairn's worked example. The postdoc will read the v0.3.0 release record,
  the adoption profile, and the metrics — the three artifacts a skeptic checks
  first. Each must be honest *before* that read.
* **What contract does it clarify?** The integrity of the durable record itself
  — the property the whole methodology is differentiated on. Correction 1 makes
  a release attestation match its own replay; Correction 2 makes a promised
  record exist; Correction 3 states the gating-function evidence honestly rather
  than letting a favorable-looking number stand unqualified.
* **Transparency / reproducibility improved?** Correction 1 ships the exact
  reproduction command; Corrections 2–3 are dated, honestly-scoped, and
  cross-linked so an auditor can trace them.
* **Why now?** The postdoc install is imminent (Phase A = "before the postdoc
  installs"), and the sibling proposal left A1 at ~40% by its own reviewer's
  count. This closes the remainder.

## Alternatives considered

1. **Do nothing.** Rejected — Theme 1's cracks stand; the false attestation, the
   dangling pointer, and the unqualified number are exactly what a skeptic (and
   the postdoc) hit first.
2. **Bundle the 0.4 cut-process transcript requirement in.** Rejected — it is a
   doctrine change that cannot clear the rate-limit gate on a single
   non-security/non-data-loss incident (`doctrine/rationale.md:319-347`); split
   it out with a revival condition instead. Bundling it is the superseded
   proposal's fatal error.
3. **Rewrite history / re-annotate the `v0.3.0` tag to fix the commit body.**
   Rejected — it mutates the immutable record and violates append-only; the
   entire point of the methodology is that you *correct forward*, not overwrite.
   (git-notes were considered as a commit-annotation mechanism but are not
   fetched by default and an adopter would never see them — not a durable,
   discoverable home.)
4. **Route all three into the existing `dev/measurement/review-floor-deviations.md`
   ledger.** Rejected — that tracker's membership is the `review-floor-deviation`
   class feeding `evolution_infer`'s rate-limit gate
   (`dev/measurement/review-floor-deviations.md` "What counts"), and
   `dev/measurement/README.md`'s two-sided rule excludes non-measurement records.
   Reusing it repeats the sibling's R5 (mixing record types into one ledger).
5. **Edit the closed v0.3.0 CHANGELOG entry / the 2026-05-20 note body in
   place.** Rejected — violates "written once at finalization"
   (`doctrine/proposals.md:132`) and append-only; use an `## Unreleased` erratum
   and a dated addendum instead.
6. **Recommended: three type-appropriate corrections + a split-out,
   rate-limited cut-process follow-up.**

**Open questions for the Maintainer.** OQ1 (Correction 1): may a
link-maintenance pointer go *into* the closed 0.3.0 CHANGELOG entry, or
Unreleased-only? OQ2: does the gating-function framing also warrant a standalone
citable note for the eventual public case study, or is the addendum enough
(default: addendum)? OQ3: confirm no new tracker for the attestation incident
now (default: none; n=1). OQ4: confirm the reconstructed adoption record is
dated 2026-07-11, not backdated.

## Evidence / verification plan

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.** (i) The adoption record is dated at reconstruction time and
  asserts no non-recoverable deliberation — *enforced by* the honesty guard +
  reviewer read of the note against `profile.yml`. (ii) The v0.3.0 erratum's
  replay is reproducible from immutable inputs (fixed commit `12ec2ad` +
  byte-identical gate code) — *enforced by* the pinned command below. (iii) The
  two repointed references resolve to a real file — *enforced by* the existing
  `scripts/check_cairn.py` claim-path/link check.
* **Failure modes.** All corrections are additive/append text; the failure mode
  is *content* (an inaccurate or over-reaching record), caught by review, not a
  runtime break. The one runtime-adjacent check (`check_cairn`) fails **closed**
  (red) on a broken pointer.
* **Edge cases.** The reconstruction must degrade **open** where a rationale is
  not recoverable — marked "not recoverable," never invented. The Unreleased
  erratum must not be written at a non-serialization point (lands only at the
  implementing commit).
* **Public-path → test mapping.** **N/A** — no code or public entry point is
  added; the change is record text. Its "tests" are the prose-integrity gates
  below.
* **Known omissions.** This proposal does **not** carry: the split-out
  cut-process transcript requirement (deferred, rate-limited); a v0.3.0
  pre-release *sweep* reconstruction (broad-look Theme 1 item 3,
  `...broad-look...:143-148` — a separate, unassigned record gap); any new
  incident tracker.

### Tests required

* **N/A for behavioral pytest** — no code surface. `python -m pytest
  bootstrap/tests` stays green (modulo the separately-tracked pre-existing
  failures the sibling plan already documents); this proposal touches no engine
  code.

### Examples / smoke checks

* **Correction 1 replay (the primary evidence):**
  `git archive 12ec2ad | tar -x -C <tmp>` then, in `<tmp>`,
  `python scripts/quality_gate.py --sub neutrality` (exit 1, fail=99) and
  `--sub redundancy` (exit 1, fail=6) — reproduced this session (2026-07-11).
* `python scripts/check_cairn.py` clean over the new adoption note, the edited
  pointers, the CHANGELOG erratum, and the metrics-note addendum.
* `python scripts/claim_check.py` clean over this proposal, its plan, and the
  new note.

## Signals the change is wrong

* The reconstructed adoption record asserts a 2026-06-12 rationale the Maintainer
  did not actually hold → it fabricates deliberation. Recovery: strip to only
  what `profile.yml` + the framework note objectively support; mark the rest
  "not recoverable."
* The v0.3.0 replay numbers do not reproduce for the Maintainer or a third party
  → the replay was environment-dependent. Recovery: the erratum already pins the
  exact `git archive` + command; re-verify and correct the recorded counts.
* The gating caveat reads as "review is theater" (over-correction) → it undercuts
  the real improvement evidence. Recovery: keep the mean-7.7-findings improvement
  framing prominent alongside the caveat, and lead with the first-supersession
  fact as positive gating evidence.
* An Unreleased CHANGELOG erratum lands at a non-serialization point → it trips
  the shared-comm-file discipline. Recovery: land the CHANGELOG and PLANNING
  edits only at the implementing-commit / goodnight serialization points.
* Review judges a pointer into the closed 0.3.0 entry *is* permitted
  link-maintenance after all (OQ1 resolves "yes") → the Unreleased-only default
  was too conservative; add the single dated pointer line.
## Review -- Claude (Internal, fresh-context subagent panel) -- 2026-07-11

**Model**: Claude Opus 4.8 (three fresh-context subagents — doctrine-conformance, evidence-feasibility, scope-adopter — no access to the authoring session; consolidated, none dropped).

**Attribution / committer note.** The panel's findings, transcribed faithfully — none softened, reordered to bury, or dropped. Per the binding practice from the superseded automated-review-committer Decision (2026-07-09), the raw panel source is committed in-tree at `dev/proposals/archive/2026-07-11-record-corrections-internal-panel.json`; this section is committed under the Maintainer's git identity by the author-session as disclosed scribe.

**Steelman.** Doctrinally and evidentially this is a strong, disciplined proposal that should land. It clears the rate-limit gate honestly as N/A (all three corrections are record-of-fact edits — no doctrine/AGENTS.md surface, verified) and correctly splits out and defers the one genuine doctrine change (the cut-commit gate-transcript requirement) with a recurrence-gated revival condition instead of bundling it or bypassing the gate — citing the exact R1 finding (automated-review-committer.md:224-236) that killed the superseded proposal. It has internalized that proposal's lessons: the "security/data-loss-exhaustive, else counted-recurrence" gate, don't-bundle-doctrine, reuse-an-existing-mechanism (check_cairn) rather than inventing a tool, and no new adopter-facing apparatus. The central evidentiary claim reproduces EXACTLY this session: replaying byte-identical gate code on the immutable/archived v0.3.0 (12ec2ad) tree yields neutrality exit 1/fail=99 and redundancy exit 1/fail=6 (plus full-gate exit 1), versus the commit body's "exit 0 / all-info / 6 advisory." Every doctrine, sibling, and audit citation checked resolves to real text; the A1 item-mapping (sibling carried 1+4; this carries 2/3/5) is exact against broad-look:543-549; doc-tier routing is honest; and the honesty guards (dated markers, "not recoverable" notes, no backdating, no over-correction) are well-designed and directly answer the showcase-arc sin. Alternatives 3-5 are doctrine-grounded and correct. All three lenses concur it is a model of the shape this repo rewards.

**Critiques** (descending severity; each grounded in a command/citation the reviewer ran):

* **[R1] (substantive)** The deferred cut-transcript follow-up leans on a recurrence-gated revival ("a second attestation-replay failure counted in an appropriate tracker"), but the proposal records the n=1 v0.3.0 failure ONLY as a CHANGELOG erratum (Correction 1) and OQ3 defaults to opening no tracker. So the recurrence path is un-armed: there is no incrementable counter, reproducing the exact "the tracker that would count it isn't established yet" gap that R1 killed the superseded proposal on. Cairn already ships the fix: the incident-trackers module is installed and is explicitly the rate-limit gate's "parse target," with live trackers homing under dev/measurement/ — so the existing substrate (lesson #4) covers this.
  *Grounding:* dev/modules/incident-trackers.md:1-45 (module IS the rate-limit gate's parse target; live trackers home under dev/measurement/); dev/.cairn/cairn-lock.yml:589 (module installed); dev/proposals/archive/2026-07-08-claude-automated-review-committer.md:233 (R1: "the tracker that would count it isn't established yet"); doctrine/rationale.md:327-329 ("recorded wherever the team tracks the recurrence") — all read this session.
  *Suggested fix:* Resolve OQ3 toward using the existing substrate: log the v0.3.0 attestation-replay failure as the first row of an incident tracker forked from dev/modules/incident_log_template.md into dev/measurement/ (defining an "attestation-replay-failure" event class), so the deferred follow-up's counted-recurrence path is actually armed. If OQ3 stays "no tracker," reword the revival condition so it does not depend on a counter that will not exist (e.g., revive on the second observed incident, or on Maintainer high-risk classification alone).

* **[R2] (substantive)** Citation drift on the load-bearing rate-limit gate — and the entire deferral rests on the gate being exhaustive to security + data-loss, so these citations must be exact (the cite-doctrine-exactly discipline a reviewer here enforces by hand). The proposal cites doctrine/rationale.md:333-343 for the "exhaustive two-surface list," but the two-surface list is at 337-344 (line 333 is the tail of the Synthesis-bullet parenthetical) and the exhaustiveness clincher ("Any other 'this feels urgent' framing falls outside the bypass") is at 346-347 — outside the cited range. Likewise the recurrence-path anchor :325-328 clips the actual bullet, which is at 327-329. The superseded proposal's own R1 cited the accurate :337-347. Substance is correct; the anchors drift.
  *Grounding:* doctrine/rationale.md:337 ("Two surfaces qualify"), :339-344 (security/data-loss bullets), :346-347 ("Any other ... falls outside the bypass"); line 333 = Synthesis bullet; :327-329 (recurrence bullet); dev/proposals/archive/2026-07-08-claude-automated-review-committer.md:225 (sibling R1 cites the accurate :337-347) — verified this session.
  *Suggested fix:* Change the exhaustiveness citation from :333-343 to :337-347 (or :335-347) so it covers the "Two surfaces qualify" list and the "falls outside the bypass" clincher, and change the recurrence-path citation from :325-328 to :327-329. The Alt-2 cite :319-347 is already correct. Argument is unaffected.

* **[R3] (substantive)** The erratum treats the redundancy and neutrality attestations as equally false, but they are not — a precision the proposal's own honesty-selling premise demands. Replay shows redundancy fail=6, and the attestation ("6 advisory R6 redundancy notes ... accepted for a private cut") CORRECTLY counted exactly 6 R6 findings and consciously accepted them as pre-existing debt. What is false is (a) the umbrella "quality_gate exit 0" and (b) the neutrality "all-info/justified" claim, which is materially false (99 fails, not zero). Framing both sub-gates as equally "does not replay / not advisory" overstates the redundancy problem.
  *Grounding:* Replay on 12ec2ad tree this session: redundancy fail=6 (matches attested count) vs neutrality fail=99 (attested "all-info", i.e. zero); commit 12ec2ad body "quality_gate exit 0 (neutrality all-info/justified; 6 advisory R6 redundancy notes)".
  *Suggested fix:* In the erratum, separate the two: the redundancy finding-count was accurate and honestly disclosed as accepted debt; the neutrality "all-info/justified" claim was materially false; and the "exit 0" umbrella is contradicted by the actual exit. This keeps the erratum itself precisely honest.

* **[R4] (substantive)** C3 frames the first supersession as "review performing its kill function ... review killing a change on its own merits." But the record shows automated-review-committer was "Superseded in favor of" alternatives taken from the AUTHOR's own Response (an immediate practice under existing doctrine + a deferred follow-up), triggered by blocking finding R1 — that is gating AND improvement working together, the idea was reshaped, not rejected, and supersession is not rejection (the "0 rejected" number stays 0). The disposition was "superseded" (over-reached / superseded-by-a-plan), not "rejected"; calling it review's "kill function" reads as a hard rejection. In a correction whose whole thesis is honest record-keeping, this over-claim is the exact irony a skeptic (or the postdoc) will catch, undercutting C3's credibility.
  *Grounding:* dev/proposals/archive/2026-07-08-claude-automated-review-committer.md:8 ("Status: superseded"), :428-438 and :448-463 (Decision: "Superseded in favor of ... from the author Response"; "The fresh-context Internal panel gated it on its own text — three blocking findings"); R1 at :224-236; grep confirms it is the only superseded/rejected proposal in dev/proposals/.
  *Suggested fix:* Reword the C3 addendum precisely: review's blocking finding (R1) led the author to supersede the proposal in favor of an existing-doctrine practice plus a recurrence-gated follow-up — the first recorded instance of the adversarial read materially blocking a change as written. Keep "gating CAN bite" as the point; drop "kill"/"killing"; use "superseded" precisely and state that the rejected count is still 0 and supersession is the distinct signal (not a hard rejection).

* **[R5] (substantive)** Correction 2 invariant (iii) overstates enforcement for both C2 pointers, and check_cairn cannot force either to closeout. Facet A (profile.yml out of scope): invariant (iii) claims "The two repointed references resolve to a real file — enforced by the existing scripts/check_cairn.py claim-path/link check," but check_cairn scans only tracked Markdown (git ls-files '*.md'); dev/.cairn/profile.yml is a .yml file and is out of scope, so its repointed pointer is NOT machine-checked — only the PLANNING.md pointer (a .md, and only if backticked as a path token) is covered, so the "pointer leads nowhere class is closed by an existing mechanism, with no new tool" claim holds for one of the two pointers, not both. Facet B (deferred PLANNING repoint / inconsistent window): C1's CHANGELOG erratum + C2's profile.yml comment repoint at the implementing commit, but C2's PLANNING.md repoint "lands at a serialization point, e.g. goodnight or the plan archive," creating a window where profile.yml names the concrete file while PLANNING.md:34-40 still says the generic "dev/strategy/" directory — an inconsistent pointer pair that check_cairn will NOT red-flag (a directory ref resolves), so nothing forces closeout and the PLANNING repoint can silently be dropped.
  *Grounding:* scripts/check_cairn.py:47 ("Scanned set: the whole tracked Markdown tree") and :177-182 (tracked_markdown = git ls-files '*.md'); dev/.cairn/profile.yml is .yml; current PLANNING.md:34-40 uses generic "dev/strategy/" directory pointer; AGENTS.md shared-comm-file rule — verified this session.
  *Suggested fix:* Scope invariant (iii) to the PLANNING.md pointer; state explicitly that the profile.yml comment is machine-state relying on reviewer verification (not check_cairn), or move the durable pointer into a scanned .md and treat the .yml comment as secondary. Additionally, in the implementing plan make the PLANNING.md repoint a required, tracked closeout step tied to the plan-archive serialization (not left to "e.g. goodnight") so both pointers land consistent; and note that the implementing commit bundling CHANGELOG.md is NOT auto-carved (CHANGELOG is carved only in the goodnight-handoff commit), so it is approval-gated — the proposal's "under explicit instruction" should be stated as a hard requirement in the plan.

* **[R6] (substantive)** Of the three corrections, C3 is the weakest fit for the stated Phase-A deadline ("before the postdoc installs") and the most interpretive. C1 (false attestation) and C2 (dangling pointer) are artifacts a skeptic/postdoc hits first when auditing the record (broad-look 135-152); C3 appends an argument to an internal 2026-05-20 metrics strategy note the postdoc is unlikely to audit at install time, and the proposal's own OQ2 asks whether C3 really belongs to the eventual PUBLIC case study. Bundling is defensible — all three are one low-risk record-text class, so this is NOT the forced-tool-split situation — but the Maintainer should have explicit per-correction accept latitude rather than an all-or-nothing unit.
  *Grounding:* broad-look :135-152 (attestation+pointer, adopter-first) vs :162-171 (zero-rejections) vs proposal OQ2; metrics note is dev/strategy/2026-05-20-...:145-160.
  *Suggested fix:* Make the Decision explicitly per-correction: C1+C2 are the Phase-A-critical factual corrections and should land now; let the Maintainer accept C3 now OR route it to public-release prep (resolving OQ2) without holding C1/C2. Say so in the proposal so acceptance-as-a-unit isn't forced.

* **[R7] (minor)** Evidence-to-claim scope mismatch, plus an unmentioned third failure. The attestation's literal claim is "quality_gate exit 0" (the full gate), but the pinned reproduction replays only two --sub invocations. The OR-aggregation (report.failed = any fail) means the two sub-gate fails do entail full-gate exit 1, so the logic holds — but an erratum refuting a false "exit 0" is strongest showing full-gate exit 1 directly. Separately, running the full gate on the cut tree ALSO fails order-independence (fail=1, pytest exit 1), which is pytest/environment-sensitive and is not mentioned; a Maintainer running the literally-attested full command would hit an unexplained third failure.
  *Grounding:* quality_gate.py:114-115 (failed = any fail), :809 (default runs all sub-gates), :819 (return 1 if failed); full-gate replay this session: order-independence fail=1, neutrality fail=99, redundancy fail=6, exit=1.
  *Suggested fix:* Either add a full-gate "exit 1 vs attested exit 0" line to the erratum, or explicitly scope the refutation to the two deterministic filesystem-walk sub-gates and state why order-independence is excluded (pytest-based, environment-sensitive) so the Maintainer isn't surprised.

* **[R8] (minor)** The lifecycle.md citation supports less than the framing implies. Correction 3 says the "bad ideas die in chat-stage shaping" explanation is "half-acknowledged at doctrine/lifecycle.md:285-296." That section establishes that a chat-stage shaping phase exists (preferences are input folded into drafts) but does NOT say losing ideas are filtered/die there. The proposal hedges ("half-acknowledged", "candidate honest explanation") and broad-look:168-171 independently calls it "written down only obliquely", so it is defensible — but the citation does less work than a fast reader infers.
  *Grounding:* doctrine/lifecycle.md:285-296 ("Chat preferences are not a lifecycle Decision" — preferences are "input ... fold them into a proposal draft", no filtering claim); broad-look:168-171 ("written down only obliquely"); verified this session.
  *Suggested fix:* Keep the hedge explicit in the addendum: cite lifecycle.md:285-296 only for "a pre-proposal shaping stage exists", and present the losers-die-in-chat mechanism as an unverified candidate explanation, not a doctrine-backed fact.

* **[R9] (minor)** In "Documentation / doctrine surface", Correction 1 labels CHANGELOG.md as "descriptive/record layer". Per the placement procedure the proposal is bound by, cairn/CHANGELOG.md (the release record) is in the Entry layer, not the Descriptive layer (Descriptive = docs/). The routing conclusion (a record not a rule; edited only at a serialization point) is correct and unaffected — only the layer name is wrong.
  *Grounding:* docs/DOCUMENTATION_PLAN.md:42-43 (read this session): "cairn/CHANGELOG.md (the release record)" listed under "### 1. Entry layer".
  *Suggested fix:* Relabel Correction 1 as "Entry layer (the release record)" rather than "descriptive/record layer".

* **[R10] (minor)** OQ1 frames a possible pointer into the closed 0.3.0 CHANGELOG entry as "mirroring the sibling's top-of-file pointer on a closed proposal file (doctrine/proposals.md:136-140)". But proposals.md:129-133 explicitly puts CHANGELOG outside the outbound-link set and holds its entries "written once at finalization, never updated afterward" — a stricter rule than the archived-proposal link-maintenance exemption at :136-140. The proposal's Unreleased-only DEFAULT is doctrinally correct, so the outcome is unaffected; but the analogy understates the gap: a Maintainer "yes" would extend the exemption to an artifact doctrine currently excludes, not merely mirror an existing one.
  *Grounding:* doctrine/proposals.md:129-133 (CHANGELOG not in outbound-link set; "written once at finalization, never updated afterward") and :136-140 (archived-proposal link-maintenance exemption) — read this session.
  *Suggested fix:* In OQ1, note that CHANGELOG's :129-133 rule is stricter than the archived-proposal :136-140 exemption, so answering "yes" extends the link-maintenance reading to a new artifact class; keep Unreleased-only as the default (already correct).

* **[R11] (minor)** C1's erratum records the symptom (false gate-green attestation) but not its cause. Broad-look Theme 1 item 3 (:142-148) — the pre-release sweep that would have machine-captured the gate result was skipped for v0.3.0 — is causally the reason the attestation was hand-written. The proposal correctly defers reconstructing the missing sweep record (genuinely separate, unassigned), but omitting even a cross-reference means a forward-auditing reader can't connect the false attestation to the skipped practice that was supposed to catch it.
  *Grounding:* broad-look dev/strategy/2026-07-08-...:142-148 (skipped v0.3.0 sweep) vs :135-141 (attestation replay); proposal "Known omissions".
  *Suggested fix:* Have the C1 erratum cross-reference broad-look Theme 1 item 3 (the skipped v0.3.0 pre-release sweep) as the proximate cause, while keeping the sweep-record reconstruction itself deferred. One sentence closes the causal loop without expanding scope.

* **[R12] (minor)** The proposal header's cairn-internal-ref-allow rationale states a doctrine reference is "a citation to Cairn's published methodology, not an installed local file." That is the adopter-tree convention, but this IS the Cairn self-host repo where doctrine/ exists locally (ls doctrine/ returns dual-review.md, lifecycle.md, rationale.md, proposals.md) and check_cairn resolves those paths. So the suppression is a no-op here and its stated reason is contextually wrong; it also slightly reduces the safety net by exempting doctrine paths that would otherwise be checked. Harmless to correctness (all cited doctrine resolves and is accurate, verified this session), but a blemish in a proposal about record accuracy.
  *Grounding:* ls doctrine/ shows dual-review.md, lifecycle.md, rationale.md, proposals.md present locally; all doctrine line-citations verified to resolve this session.
  *Suggested fix:* Either drop the doctrine-path ref-allow (the paths resolve in this repo, so the checker passes without it) or reword its rationale to reflect the self-host context rather than the adopter-tree citation convention.

**Coverage.** All three lenses swept, each reproducing/verifying this session. (1) Attestation replay on the archived 12ec2ad tree — neutrality exit 1/fail=99, redundancy exit 1/fail=6, full gate exit 1; gate code byte-identical (git diff 12ec2ad HEAD empty; git log 12ec2ad..HEAD -- scripts/quality_gate.py empty; no touching commits); tag v0.3.0→12ec2ad; rglob at quality_gate.py:455,536,603; failed/exit logic at :114-115,809,819. (2) Doctrine citations: rationale.md rate-limit gate 319-347 (found the two-surface/exhaustiveness-clincher line-range drift and the recurrence-bullet drift), proposals.md:129-133/:132/:136-140, lifecycle.md:285-296, dual-review.md:442. (3) Sibling review-record-integrity R12:385-391, R5:322, plan-review:406-416. (4) Superseded automated-review-committer Decision:428-438/:448-463, bundling-R1:224-236, deferral-model:456-463; archive enumeration confirms exactly one superseded proposal (first-supersession claim holds; grep confirms 0 rejected). (5) broad-look:135-152,162-171,543-549 and the A1 item 1-5 mapping (sibling did 1+4; this does 2/3/5; skipped-sweep item 3 legitimately outside A1). (6) measurement/README two-sided rule; profile.yml:7-8,14-23 and PLANNING.md:34-40 REAL and dangling; metrics-note corpus:147-153. (7) check_cairn/claim_check scan scope (tracked Markdown only). Cut process homes in doctrine/consolidation-review.md, supporting the deferred item's doctrine-change classification. NEGATIVE SPACE no lens could exercise: the CONTENT of the yet-unwritten adoption record (C2) and metrics addendum — they do not exist yet, so their honesty/completeness/over-reach (does profile.yml's six-axis + three-module rationale fully recover the 2026-05-14 framework note?) is a review-of-artifact catchable only at plan/implementation/note-read time, and it is the exact class the showcase-arc sin embodied; OQ1's resolution (a Maintainer judgment on link-maintenance into the closed CHANGELOG entry); the root cause of the order-independence pytest failure on the cut tree (environment vs. cut-tree defect — full suite not run); whether the sibling actually carries a post-archive top-of-file pointer (OQ1's precedent, not load-bearing since default is no); check_cairn/claim_check over the nonexistent new artifacts; and the Maintainer's actual 2026-06-12 deliberation state (unrecoverable by construction — which is the proposal's own point).

**Second-round recommendation.** Yes — all three lenses independently recommend an External (cross-type) read before the Decision, concurring with the proposal's own plan-review request and the sibling review-record-integrity precedent, and this consolidated panel concurs. The doctrine/gate mechanics themselves are sound and do not need a second Internal pass; the Internal floor is met by this pass, and the record-of-fact corrections plus the enforcement-invariant fix are near-mechanical once R1-R5 land. What an External, different-agent-type reviewer is best placed to stress-test: (a) whether the deferred follow-up's recurrence path must be armed now via the existing incident-trackers substrate or the revival condition reworded (R1); (b) the honesty framing of the erratum — \"hand-written, not fabrication,\" the reconstruction/over-reach guard, and the redundancy-vs-neutrality precision (R3, R4); (c) whether Correction 2's reconstructed adoption note over-reaches its \"only what profile.yml + the 2026-05-14 framework note support\" boundary — unverifiable until written; and (d) OQ1 (may a link-maintenance pointer go into the closed 0.3.0 CHANGELOG entry, given proposals.md:132's \"written once\" vs :136-140's link-maintenance exemption). These are judgment calls a same-type reviewer sharing the author's priors is likelier to wave through (citation-precision items like R2 are themselves doctrine-recall slips a cross-type read catches better). External should gate the Decision, not the plan-open.
## Response -- Claude (author) -- 2026-07-11

I re-verified every load-bearing claim in the panel's findings against the tree this session (replay on the archived `12ec2ad` tree; the rate-limit-gate, `check_cairn`, `proposals.md`, `lifecycle.md`, `DOCUMENTATION_PLAN.md`, and superseded-Decision citations). **All twelve findings hold, and none is dispositive.** They are precision fixes (R2, R3, R4, R8, R9, R10, R11, R12), two enforcement/arming corrections (R1, R5), one evidence-scoping fix (R7), and one Decision-shaping fix (R6). No blocking finding argues "don't ship this"; the corrective is to sharpen the proposal, not withdraw it. I dispose of each below and fold the accepted deltas into the Revised proposal section. No R-number is silently dropped.

**R1 — accept with modification.** Correct and load-bearing: the deferred follow-up's revival phrase ("a second attestation-replay failure counted in an appropriate tracker") presupposes a counter my own OQ3 declines to create, which reproduces the exact un-armed-recurrence gap that killed `automated-review-committer` (its R1). I will (a) reword the revival condition so it does not depend on a pre-existing counter, and (b) make the *recommended* OQ3 resolution to seed a minimal `attestation-replay-failure` tracker forked from the already-installed `incident_log_template.md` (cairn-lock.yml:589) into `dev/measurement/`, with the v0.3.0 erratum as row 1 — arming the recurrence path via **existing substrate** (lesson #4), not new apparatus, and mirroring how that same superseded Decision's own accepted follow-up (`automated-review-committer.md:456-463`) named an *existing* tracker as its counter. Seeding a tracker is a measurement-layer record-of-fact, not a doctrine change, so it clears no gate; the doctrine change (the transcript requirement) stays deferred. *(Modification, not plain accept: whether to seed now is genuinely the Maintainer's measurement-layer call at OQ3, so the reworded revival must stay coherent even if the Maintainer declines to seed — revive on a second observed incident recorded wherever the team then tracks it, or on Maintainer high-risk classification.)*

**R2 — accept.** Verified: the exhaustive two-surface list is `doctrine/rationale.md:337-347` ("Two surfaces qualify" at 337 through "Any other 'this feels urgent' framing falls outside the bypass" at 346-347), and the recurrence bullet is `:327-329`; my `:333-343` and `:325-328` both drift. I will change the exhaustiveness cite to `:337-347` and the recurrence cite to `:327-329`; the Alt-2 cite `:319-347` is already correct and the argument is unaffected.

**R3 — accept.** The erratum must not flatten the two sub-gates into equal falsehood. Replay confirms: redundancy is 6 FAIL-class, and the attestation ("6 advisory R6 redundancy notes ... the documented pre-existing debt ... accepted for a private cut") counted exactly 6 and honestly disclosed the acceptance — so only its *class label* ("advisory" vs FAIL) and the umbrella "exit 0" are wrong there; whereas neutrality's "all-info/justified" asserted zero problems against 99 FAIL-class tokens, which is *materially* false. The erratum will state these separately.

**R4 — accept.** `automated-review-committer.md:448-463` reads "**Superseded in favor of**" alternatives drawn from the author's own Response — the idea was blocked-as-written and *reshaped*, not hard-rejected, and the `0 rejected` count stays 0. Framing it as review's "kill function / killing a change" over-claims in a correction whose whole thesis is honest record-keeping. I will reword C3 to use "superseded" precisely (the adversarial read materially blocked the change as written and the author reshaped it), drop "kill"/"killing," and note that supersession is the distinct gating signal (rejected still 0). This is more honest and actually *stronger* gating evidence — it shows the full loop (block → reshape), not just a rejection.

**R5 — accept.** Two real defects. (i) Invariant (iii) over-claims: `check_cairn` scans only `git ls-files '*.md'` (:47, :177-182), so the `.yml` `profile.yml` pointer is **not** machine-checked — only the `PLANNING.md` pointer is (and only as a backticked path token). I will scope invariant (iii) to the `PLANNING.md` pointer and state that the `profile.yml` comment rests on reviewer verification. (ii) The deferred `PLANNING.md` repoint creates an inconsistent-pointer window `check_cairn` will not red-flag (a directory ref resolves); I will make the `PLANNING.md` repoint a required, tracked closeout step tied to the plan-archive serialization so both pointers land consistent, and state as a hard plan requirement that a CHANGELOG erratum in an implementing commit is **approval-gated** (CHANGELOG additions are auto-carved only in the goodnight-handoff commit, not the deliberation/plan carve-out).

**R6 — accept.** C3 is the weakest Phase-A fit (an internal metrics note the postdoc is unlikely to audit at install) and my own OQ2 already questions whether it belongs to the public case study. I will make the Decision explicitly **per-correction**: C1+C2 are the Phase-A-critical factual corrections and should land now; the Maintainer may accept C3 now *or* route it to public-release prep (resolving OQ2) without holding C1/C2. This is not a forced tool-split (all three are one low-risk record-text class), just Maintainer latitude.

**R7 — accept with modification.** The literal attestation is "quality_gate **exit 0**" (full gate), but my pinned repro runs two sub-gates. I will (a) keep the two deterministic filesystem-walk sub-gates as the pinned, reproducible evidence (neutrality exit 1/fail=99; redundancy exit 1/fail=6, as_of 2026-07-11), (b) add that these two FAIL-class results *entail* full-gate exit 1 by the OR-aggregation at `quality_gate.py:114-115`, directly refuting the attested "exit 0," and (c) note that order-independence *additionally* fails on the cut tree but is pytest-based and environment-sensitive (it is why the full gate ran ~2 min and timed out for me this session), so it is disclosed but **not pinned as a fixed count**. *(Modification: I decline to pin the order-independence number as erratum evidence precisely because it is environment-dependent — pinning it would violate the erratum's own reproducibility standard.)*

**R8 — accept.** `lifecycle.md:285-296` establishes that a pre-proposal shaping stage exists (preferences are input folded into a draft) but does **not** say losing ideas are filtered/die there. I will cite it only for "a shaping stage exists" and present the losers-die-in-chat mechanism as an explicitly *unverified candidate* explanation, keeping the existing hedge.

**R9 — accept.** `docs/DOCUMENTATION_PLAN.md:202` lists `CHANGELOG.md` under the **Entry** layer; my "descriptive/record layer" label is wrong (the routing conclusion — a record, edited only at a serialization point — is unaffected). I will relabel Correction 1 as "Entry layer (the release record)."

**R10 — accept.** `proposals.md:129-133` ("`CHANGELOG.md` entries are written once at finalization, never updated afterward"; CHANGELOG not in the outbound-link set) is *stricter* than the archived-proposal link-maintenance exemption at `:136-140`, so an OQ1 "yes" would **extend** the exemption to a new artifact class, not merely mirror the sibling's precedent. I will say so in OQ1; the Unreleased-only default is already correct and unchanged.

**R11 — accept.** The erratum records the symptom (false gate-green attestation) but not its proximate cause — broad-look Theme 1 item 3 (`:142-148`), the skipped v0.3.0 pre-release sweep that would have machine-captured the gate result. I will add a one-sentence cross-reference to close the causal loop, keeping the sweep-record reconstruction itself deferred (genuinely separate, unassigned).

**R12 — accept.** In this self-host repo `doctrine/` exists locally (`ls doctrine/` resolves) and the internal-ref checker resolves those paths, so the header's doctrine-path `cairn-internal-ref-allow` is a no-op whose stated rationale (adopter-tree citation convention) is contextually wrong and which slightly reduces the safety net. With R2's line-fixes applied, the doctrine citations resolve, so I will **drop the doctrine-path suppression** (restoring the checker's coverage — on-thesis for a record-accuracy proposal) and keep only the forward-reference `claim-check-allow` for the genuinely-not-yet-existent paths; the plan verifies `check_cairn` clean.

**Disposition summary.** 12/12 accepted (R1, R5, R7 with modification; the rest plain accept). Zero rejects, zero deferrals-to-Maintainer among the R-numbers: verification confirmed every finding, and each is a text/arming fix I can make within the proposal's existing frame. The Maintainer judgment calls (OQ1 link-maintenance-into-CHANGELOG, OQ2 C3-routing, OQ3 tracker-seeding, OQ4 dating) remain the open questions they already were, now sharpened by R6/R10/R1.

**Second-round read.** I concur with the panel's recommendation, which also matches my plan-review line and the sibling precedent: the Internal floor is met by this pass; no second Internal pass is needed for the doctrine/gate mechanics (they verified sound). An **External (cross-type) read should gate the Decision** — best placed to stress-test the erratum's honesty framing (R3/R4), whether the reconstructed adoption note (C2) over-reaches its "only what `profile.yml` + the framework note support" boundary (unverifiable until written — the negative-space item the panel flagged and the exact class the showcase-arc sin embodied), and OQ1.

## Revised proposal -- 2026-07-11

Design unchanged in shape (three type-appropriate record-of-fact corrections + one split-out, rate-limited doctrine follow-up); the deltas below fold in R1–R12. No new correction is added; C3's evidence is sharpened, not expanded.

**Header.** Drop the doctrine-path `cairn-internal-ref-allow` (paths resolve in this self-host repo; R12); keep the forward-reference `claim-check-allow`.

**Correction 1 (erratum), revised design.** The Unreleased `### Fixed` erratum will:
- Name commit `12ec2ad` and quote its attestation verbatim.
- **Refute per sub-gate, not as one flat falsehood (R3):** neutrality attested "all-info/justified" but replays **exit 1 / 99 FAIL-class** vendor tokens (materially false — claimed zero, found 99); redundancy attested "6 advisory R6 notes ... accepted" and replays **exit 1 / 6 FAIL-class** — the *count of 6 was accurate and the acceptance honestly disclosed*, so only the "advisory" class-label and the umbrella verdict are wrong there.
- **Refute the "exit 0" umbrella directly (R7):** the two FAIL-class sub-gate results entail full-gate exit 1 by OR-aggregation (`quality_gate.py:114-115`); order-independence *also* fails on the cut tree but is pytest-based/environment-sensitive and is disclosed **without a pinned count**.
- Pin the reproduction: `git archive 12ec2ad | tar -x`, then `python scripts/quality_gate.py --sub neutrality` / `--sub redundancy` (as_of 2026-07-11; gate code byte-identical `12ec2ad..HEAD`).
- Adopt the "hand-written from a partial/remembered run, not fabrication" framing, and **cross-reference broad-look Theme 1 item 3** (`:142-148`, the skipped v0.3.0 pre-release sweep) as the proximate cause, keeping the sweep-record reconstruction deferred (R11).
- Relabel this correction's doc-surface as **Entry layer (the release record)** (R9); the erratum in an implementing commit is **approval-gated** and lands only under explicit instruction (CHANGELOG additions are auto-carved only in the goodnight-handoff commit) — stated as a hard plan requirement (R5).
- **OQ1 (revised):** note that `proposals.md:129-133`'s "written once at finalization, never updated" is *stricter* than the `:136-140` archived-proposal link-maintenance exemption, so a "yes" extends the exemption to a new artifact class; **Unreleased-only remains the default** (R10).

**Correction 2 (adoption record), revised design.** Unchanged in substance (reconstructed, dated 2026-07-11, honesty-guarded, "not recoverable" markers). Fixes:
- **Invariant (iii) scoped (R5):** only the `PLANNING.md` pointer is machine-checked by `check_cairn` (tracked `*.md`); the `profile.yml` comment is `.yml`, out of scope, and rests on reviewer verification.
- **The `PLANNING.md` repoint is a required, tracked plan-archive closeout step** (not "e.g. goodnight"), so it lands consistent with the `profile.yml` repoint and no dangling-generic-vs-concrete window persists.

**Correction 3 (gating-function caveat), revised design.** Fixes:
- **Precise supersession framing (R4):** review's blocking finding (R1) led the author to *supersede* `automated-review-committer` in favor of an existing-doctrine practice plus a recurrence-gated follow-up — the first recorded instance of the adversarial read materially blocking a change *as written*; drop "kill"/"killing," state that the **rejected count is still 0** and supersession is the distinct (non-rejection) gating signal.
- **Honest citation weight (R8):** cite `lifecycle.md:285-296` only for "a pre-proposal shaping stage exists"; present losers-die-in-chat as an unverified candidate explanation, alongside the still-prominent mean-7.7-findings improvement framing.

**Deferred follow-up (cut-transcript requirement), revised design (R1).** Still split out and rate-limited (it is a record-integrity surface, neither the security nor the data-loss surface that `doctrine/rationale.md:337-347` makes the *exhaustive* high-risk list; n=1, so `:327-329` recurrence is unmet). Change: the revival condition no longer presupposes a pre-existing counter. **Recommended OQ3 resolution:** seed a minimal `attestation-replay-failure` tracker forked from the installed `incident_log_template.md` (cairn-lock.yml:589) into `dev/measurement/`, with the v0.3.0 erratum as row 1 — arming the recurrence path with existing substrate. If the Maintainer declines to seed (OQ3 stays "none"), the revival reads: **on a second observed attestation-replay failure (recorded wherever the team then tracks it), or a Maintainer high-risk classification** — coherent either way.

**Rate-limit citations (R2), applied throughout:** exhaustiveness `:337-347`, recurrence `:327-329`; Alt-2 `:319-347` unchanged.

**Decision shape (R6):** the Decision is **per-correction** — C1+C2 are Phase-A-critical and should land now; C3 may land now or route to public-release prep (OQ2) without holding C1/C2. **External (cross-type) read gates the Decision.**

**Verification note.** All deltas above are additive record/text edits (no code, no doctrine, no install-contract surface); the plan verifies `python scripts/check_cairn.py` and `python scripts/claim_check.py` clean over the erratum, the new adoption note, the addendum, the repointed pointers, and — if OQ3 seeds it — the tracker row, with `python -m pytest bootstrap/tests` untouched by this change.

## Review -- Gemini (External, different-agent-type) -- 2026-07-22

**Model**: Gemini 3.6 Flash / Antigravity
**Verdict**: SHIP (conditional on Maintainer resolution of open questions OQ1–OQ4)

### Steelman
This proposal repairs three verified record-of-fact defects in Cairn's historical logs. C1 documents the v0.3.0 release gate attestation discrepancy as an `## Unreleased` erratum in `CHANGELOG.md` with explicit, reproducible replay commands. C2 reconstructs the missing adoption-decision record as `dev/strategy/2026-07-11-claude-cairn-adoption-record.md`, clearly dated and guarded against false historical backdating. C3 adds an accurate gating-function caveat to `dev/strategy/2026-05-20-claude-team-productivity-metrics.md`, citing Cairn's first superseded proposal (`automated-review-committer`) without mislabeling supersessions as hard rejections. Deferring the cut-transcript requirement to a recurrence-gated follow-up respects the adaptive-doctrine rate-limit gate.

### Critiques

* **[E1] (Rate-Limit Gate Citation Verification)**
  Verified that the rate-limit gate citations in `doctrine/rationale.md` are exact:
  1. `doctrine/rationale.md:337-347` explicitly lists security surfaces (:339-341) and data-loss surfaces (:342-345) as the **exhaustive** list of high-risk bypasses ("Any other 'this feels urgent' framing falls outside the bypass and obeys the recurrence requirement").
  2. `doctrine/rationale.md:327-329` codifies the **recurrence** requirement for non-high-risk doctrine changes.
  Because transcript retention is a record-integrity surface rather than security or data-loss, deferring the requirement respects the doctrine gate.

* **[E2] (Arming Recurrence via Tracker Seeding — OQ3)**
  Seeding the `attestation-replay-failure` tracker in `dev/measurement/` via `incident_log_template.md` with the v0.3.0 erratum as row 1 (count=1) successfully arms the recurrence path. `tools/evolution_infer.py` can parse this log in rolling windows, guaranteeing that a second attestation failure automatically triggers doctrine adaptation.

* **[E3] (Consistency with Accepted Review-Record-Integrity Pattern)**
  This proposal reuses the correction pattern established by `2026-07-08-claude-review-record-integrity.md`: placing an `## Unreleased` erratum in `CHANGELOG.md` accompanied by permitted link-maintenance pointers. This maintains single-pattern discipline across historical corrections rather than inventing competing mechanisms.

* **[E4] (First Superseded Proposal & Metrics Precision)**
  Framing `dev/proposals/archive/2026-07-08-claude-automated-review-committer.md` as Cairn's first **superseded** proposal accurately reflects gating-function behavior. Adversarial review blocked the change as written, leading the author to solve the need via existing practice without incrementing the hard rejection count (which remains 0).

### Coverage

* **Covered**:
  * Verified `12ec2ad` attestation replay output for `--sub neutrality` and `--sub redundancy`.
  * Inspected rate-limit gate rules in `doctrine/rationale.md:323-347`.
  * Checked `profile.yml:7-8` and `PLANNING.md:34-40` dangling pointer targets.
  * Verified `dev/proposals/archive/2026-07-08-claude-automated-review-committer.md` supersession record.
* **Not covered**:
  * Content of `dev/strategy/2026-07-11-claude-cairn-adoption-record.md` (to be written during plan execution).

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

*(Awaiting the Maintainer. The revised three-part correction package has cleared Internal and External reviews. Open questions for Maintainer decision: (1) OQ1: keep CHANGELOG erratum under Unreleased-only vs adding a link-maintenance pointer in the closed 0.3.0 section; (2) OQ2: approve C3 metrics caveat now or defer to public-release prep; (3) OQ3: seed the `attestation-replay-failure` tracker in `dev/measurement/` with v0.3.0 as row 1; (4) OQ4: confirm adoption record date of 2026-07-11.)*

## Response -- Claude (author, to External review) -- 2026-07-22

**Model**: Claude Opus 4.8. Proposal-Response grammar. The External read returned
**SHIP** and re-verified the citations the whole deferral rests on. All four
accepted; the open questions remain the Maintainer's.

* **[E1] accept — confirmatory, and load-bearing.** The reviewer independently
  confirmed `doctrine/rationale.md:337-347` lists security (`:339-341`) and
  data-loss (`:342-345`) as the **exhaustive** high-risk bypass, with any other
  urgency framing falling back to the recurrence requirement (`:327-329`). That
  matters because the entire cut-transcript deferral depends on it: transcript
  retention is a record-integrity surface, not a security or data-loss one, so
  deferring rather than forcing a doctrine change now is the honest reading. Had
  this citation been drifted, the deferral's justification would have collapsed.
* **[E2] accept.** Seeding the `attestation-replay-failure` tracker in
  `dev/measurement/` with the v0.3.0 erratum as row 1 does arm the recurrence
  path — `tools/evolution_infer.py` parses it in rolling windows, so a *second*
  attestation-replay failure triggers doctrine adaptation automatically instead
  of depending on someone remembering. This is the fix for the Internal panel's
  R1: an n=1 recorded only in prose can never become an n=2.
* **[E3] accept — confirmatory.** The corrections reuse the pattern the accepted
  `2026-07-08-claude-review-record-integrity` established — a `CHANGELOG.md`
  `## Unreleased` erratum plus permitted link-maintenance pointers — rather than
  inventing a competing mechanism. Single-pattern discipline across historical
  corrections is worth more than any local optimization.
* **[E4] accept — and the precision matters.** Framing
  `2026-07-08-claude-automated-review-committer` as Cairn's first **superseded**
  proposal is accurate and is deliberately *not* inflated into a "rejection":
  adversarial review blocked the change as written, and the author then met the
  underlying need through existing practice. The hard-rejection count remains
  **0**, and C3 says so. Overstating it would be the same candor failure C3
  exists to correct.

**On the open questions.** OQ1–OQ4 are unresolved by design and are the
Maintainer's at Decision — including the per-correction latitude on C3's
placement. Nothing in the External read changes their framing.

Net: External SHIP, conditional on OQ1–OQ4. Decision-ready.

## Decision -- Anthony Kendall (Maintainer) -- 2026-07-22

**Accepted.** Scribed by Claude (Strategy) at the Maintainer's explicit,
unambiguous instruction; commit permission given in the same instruction.

Maintainer's authorization (verbatim):

> Okay, I accept your recommendations on each of these. Please scribe my
> acceptance, and mark them as accepted. When you're done with that we can go
> ahead with the follow-on proposals.

**Accepted scope: C1, C2, and C3.** C1 (the v0.3.0 gate-attestation erratum) and
C2 (the missing self-host adoption-decision record) are the Phase-A-critical
factual corrections — the two a skeptic or the incoming postdoc hits first when
auditing the record. C3 (the gating-function caveat on the metrics note) is
accepted with the per-correction latitude the Internal panel asked for: it may be
re-routed to public-release prep at plan time without holding C1/C2.

**Open questions, resolved at this Decision** (the proposal's stated defaults,
except OQ3):

* **OQ1 — Unreleased-only.** The erratum lives in `CHANGELOG.md >
  ## Unreleased`; **no** pointer is written into the closed `## 0.3.0` entry.
  This is the doctrinally correct default: `doctrine/proposals.md:129-133` puts
  CHANGELOG entries outside the outbound-link set and holds them written once at
  finalization, a *stricter* rule than the archived-proposal link-maintenance
  exemption — so a "yes" would have *extended* an exemption doctrine currently
  withholds, not mirrored one.
* **OQ2 — the addendum is enough.** No standalone citable note is minted now;
  the gating-function framing rides the metrics addendum. Revisit at public-case-
  study prep.
* **OQ3 — seed the tracker** *(the one departure from the proposal's default)*.
  The v0.3.0 attestation-replay failure is logged as row 1 of an
  `attestation-replay-failure` tracker forked from the installed
  `incident_log_template.md` into `dev/measurement/`. Rationale: leaving it at
  "no tracker (n=1)" would leave the deferred cut-transcript follow-up's
  recurrence path **un-armed** — an n=1 recorded only in prose can never become
  an n=2 — reproducing the exact gap that killed the superseded
  `automated-review-committer` proposal. `tools/evolution_infer.py` parses the
  tracker in rolling windows, so a second failure now triggers doctrine
  adaptation automatically instead of depending on memory.
* **OQ4 — dated 2026-07-11, not backdated.** The reconstructed adoption record
  carries its true authoring date and is explicitly marked a reconstruction.

**Why it lands.** The External read verified the citations the entire deferral
rests on: `doctrine/rationale.md:337-347` does make the high-risk bypass
**exhaustive** to security and data-loss surfaces, with any other urgency framing
falling back to the recurrence requirement (`:327-329`). Transcript retention is
a record-integrity surface, so deferring the cut-transcript requirement rather
than forcing a doctrine change now is the honest reading of our own gate.

**Precision preserved.** C3 frames `2026-07-08-claude-automated-review-committer`
as Cairn's first **superseded** proposal — not a rejection. Adversarial review
blocked the change as written and the author then met the underlying need through
existing practice. The hard-rejection count remains **0**, and C3 says so;
inflating it would be the same candor failure C3 exists to correct.

**Next (separate commits):** open the plan (which archives this proposal),
execute C1/C2/C3, non-implementing code review, archive.
