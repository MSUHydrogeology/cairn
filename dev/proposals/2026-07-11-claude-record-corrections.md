<!-- cairn-internal-ref-allow: doctrine/proposals.md doctrine/lifecycle.md doctrine/rationale.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Forward-reference paths this proposal plans to create (the adoption record) or that materialize in its implementing plan / archive move. -->
<!-- claim-check-allow: dev/strategy/2026-07-11-claude-cairn-adoption-record.md, dev/plans/record-corrections.md, dev/proposals/archive/2026-07-11-claude-record-corrections.md -->

# Record corrections: the v0.3.0 attestation erratum, the missing adoption-decision record, and the zero-rejections gating-function caveat

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-07-11
**Status**: proposed
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