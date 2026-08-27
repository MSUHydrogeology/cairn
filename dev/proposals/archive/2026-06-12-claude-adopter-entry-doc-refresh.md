
# Adopter-entry doc-refresh + a drift-gate so the docs can't silently lag the scaffold

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-06-12
**Status**: accepted
**Touches**: `docs/quickstart.md`, `README.md`, `examples/scientific-minimal/README.md`, `bootstrap/profiles/solo-greenfield.yml` (the doc-refresh); a new drift-gate (a `bootstrap/tests/` test, plus possibly a `check_cairn` hook).
**Related**: the adopter-friction audit `dev/strategy/archive/2026-06-12-claude-adopter-friction-audit.md` (this proposal implements its recommended package); the `doc-drift-prevention` module.
**Plan review**: required(Internal) — multi-file doc change plus a new gate on a self-check surface; ratified at Decision.

## Context

The 2026-06-12 adopter-friction audit re-ran the prospective-scientist lens
on the self-hosted v0.3 tree. The pre-0.3 friction package shipped (8/9
gaps resolved), but the audit surfaced one dominant, *ironic* failure: the
**adopter-entry docs drifted behind the shipped scaffold** — the exact
"docs lag the tool" failure Cairn's lifecycle exists to prevent.

Verified against the live scaffold: `docs/quickstart.md` Step 3 tells a
newcomer they will see **4** modules and **20** slots for `solo-greenfield`;
the live install resolves **6** modules (`incident-trackers` +
`documentation-plan` were added since) and reports **21** slots. The
quickstart's named-file list also omits the onboarding/skills subsystem the
scaffold now installs. Because the quickstart's whole job is to let a
skeptic confirm "the apparatus does what the page says," a doc-vs-terminal
mismatch at the install step corrodes the trust it exists to build.

Audit findings F1–F9 (full detail in the audit note): stale module/slot
counts + file list (F1); an incomplete `git add` line (F2); the scaffold's
"Next steps" output contradicting the quickstart's "leave the slots" (F3);
an unexplained provenance warning on every run (F4); an inconsistent Python
floor — 3.11+ is the security-driven floor, the quickstart's 3.8+ and the
example's 3.10+ are stale and below it (F5); the scientific example
undiscoverable from the front door (F6); `/path/to/cairn` placeholders that
break literal copy-paste (F7); onboarding/skills vocabulary leaking into the
scaffold output with no entry-doc coverage (F8); a stale README repo-layout
table (F9).

**Root cause:** the default-on set grew and an onboarding/skills layer was
added *after* the friction package shipped, and the entry docs were never
regenerated against it. The same failure will recur on the next default-on
change unless prevention is built in.

## Proposal

Two parts: fix the current drift (a refresh), and prevent its recurrence (a
gate). Part B is the durable contribution; Part A is the immediate
remediation.

### Part A — the doc-refresh (immediate)

Regenerate the drifted surfaces from a live `solo-greenfield` install:

* **`docs/quickstart.md` Step 3** — correct the module roster (six), the
  slot count (21), and the installed-file list (add the onboarding/skills
  subsystem: `.agents/skills/`, `tools/lifecycle.py`, `scripts/_onboarding/`,
  `dev/modules/onboarding/`, `docs/DOCUMENTATION_PLAN.md`). Fix the `git add`
  line to include `.agents/` and `docs/` (F2). Reconcile the "leave the
  slots" instruction with the scaffold's "Next steps" output (F3) — see the
  open question below.
* **Copy-paste fixes** — add `export CAIRN=$(pwd)` to Step 1 and replace the
  `/path/to/cairn` placeholders so the recipe is literally pasteable (F7).
* **One-sentence defusers** — explain the provenance warning (F4: expected
  for a tip clone; `--allow-dev` silences it) and name the onboarding/skills
  artifacts the adopter now owns (F8).
* **Python floor → 3.11+** in `docs/quickstart.md` and
  `examples/scientific-minimal/README.md` (F5), matching the security-driven
  floor `bootstrap/prompts/bootstrap-lite.md` already states.
* **Discoverability** — link `examples/scientific-minimal/` from `README.md`
  (the repo-layout/examples row) and from the quickstart's "what next" (F6);
  refresh the `README.md` repo-layout table for the current module taxonomy
  (F9). Fix the stale four-module comment in
  `bootstrap/profiles/solo-greenfield.yml` (F1).

### Part B — the drift-gate (durable)

Add a self-check that **fails when the quickstart's load-bearing numbers
diverge from a live `solo-greenfield` install**, so this class of drift is
caught the moment the default-on set changes — not by an adopter at Step 3.

Proposed mechanism (exact form is plan-level): a stdlib-only test under
`bootstrap/tests/` that (1) runs the scaffold's resolver for the
`solo-greenfield` profile to get the canonical module count and slot count,
(2) extracts the counts the quickstart states, and (3) asserts they match.
This re-uses the existing `--summary` / dry-run surfaces the scaffold
already exposes; the quickstart's stated numbers carry a small machine-
readable marker (e.g. an HTML comment) the test reads, so the assertion is
on a declared value, not brittle prose-scraping. An alternative considered
is snippet-sync (the `doc-drift-prevention` module's mechanism) regenerating
the numbers from a generated source; the test form is preferred for v1
because the numbers are few and the failure mode (a hard test failure naming
the divergence) is the clearest signal to a maintainer.

### Documentation / doctrine surface

Descriptive/entry layer only (`docs/`, `README.md`, the example README, the
profile comment). No doctrine change; the drift-gate is tooling. The
`doc-drift-prevention` principle in `doctrine/doc-governance.md`
("generate it outward from the source and guard it with a drift gate") is
the existing doctrine this implements, not a new rule.

### Doctrine-change rate-limit

N/A — this proposal changes no doctrine rule, process, or contract; it
fixes drifted descriptive docs and adds a gate. The rate-limit gate does
not apply.

## Rationale

* **It fixes the highest-friction adopter finding.** The audit's headline
  was that a skeptic's first command undercuts the quickstart's promise.
  Restoring doc==terminal is the single most trust-restoring change available.
* **It prevents recurrence, not just this instance.** Without the gate, the
  next default-on change re-introduces the drift silently. The gate makes the
  failure visible to a maintainer at change time — Lin Transparency +
  Sustainability of the launch surface.
* **It uses Cairn's own doctrine on itself.** `doc-drift-prevention` exists
  precisely for "a descriptive doc that mirrors a source must be guarded by a
  drift gate." The quickstart's numbers mirror the scaffold; guarding them is
  Cairn dogfooding its own anti-drift principle.
* **Now is the right time.** The drift is live in the tree, and the 0.4
  candidates already include adopter-doc graphics/polish; folding the refresh
  + gate in before public adopters fork the scaffold (at 0.4) is on the
  launch-surface path the roadmap names.

## Alternatives considered

1. **Do nothing.** Rejected — the audit's #1 finding stands; a skeptic
   bounces at Step 3.
2. **Doc-refresh only (no gate).** Partial — fixes this instance, but the
   drift recurs on the next default-on change; the audit explicitly flags
   recurrence as the deeper problem.
3. **Fully generate the quickstart from the scaffold.** Rejected — the
   quickstart's prose (the *why* at each step) is its value; only the
   load-bearing *numbers* and *file list* need to be source-true.
4. **Snippet-sync the numbers (vs a test).** Viable; deferred to a plan-level
   choice. A hard test failure naming the divergence is the clearer
   maintainer signal for v1; snippet-sync is the right escalation if the
   guarded surface grows.
5. **Recommended: refresh (Part A) + a targeted drift-gate (Part B).**

## Evidence / verification plan

The three things this change accounts for — tests, examples/smoke, docs:

### Tests required

* **The drift-gate test itself** (Part B) — asserts the quickstart's stated
  `solo-greenfield` module count and slot count match a live scaffold
  resolution. This both *is* the deliverable and *is* its own regression
  test: run it against the refreshed quickstart (passes) and against the
  pre-refresh numbers (fails, naming 4≠6 / 20≠21).
* The existing `bootstrap/tests` suite stays green; the new test is
  stdlib-only and offline (it drives the scaffold resolver, not a network).

### Examples / smoke checks

* **A cold-run of `docs/quickstart.md` end-to-end** (the audit's method) on
  a disposable repo: every stated number, the file list, and the `git add`
  line match the actual install; `git status` is clean after the documented
  commit. This is the acceptance smoke for Part A.
* `python scripts/check_cairn.py` stays green over the refreshed docs.

### Author-accounting — invariants, failure modes, edge cases

* **Invariant** — the quickstart's stated `solo-greenfield` module/slot
  counts equal a live install's, enforced by the Part B gate.
* **Failure mode** — the gate is *closed* (a hard test failure) on
  divergence; the risk is brittleness (failing on a benign formatting
  change). Bounded by reading a declared machine-readable marker, not
  scraping prose.
* **Edge cases** — a future default-on module change (the gate fires,
  correctly); a profile other than `solo-greenfield` (out of scope for v1 —
  the quickstart only uses `solo-greenfield`); the slot count depending on
  which modules declare slots (the gate derives it live, so it tracks).
* **Known omission** — v1 guards only the quickstart's `solo-greenfield`
  numbers, not every adopter-facing count everywhere; the gate is the
  pattern, scoped to the highest-traffic surface first.

## Signals the change is wrong

* The drift-gate fails on a benign edit (too brittle) → it nags rather than
  guards; loosen to the declared-marker read or escalate to snippet-sync.
* The refreshed quickstart introduces a *new* inaccuracy a cold-run catches
  → the refresh wasn't regenerated from a live install; regenerate.
* Adopters still report Step-3 confusion after the refresh → the F3
  "Next steps vs leave-the-slots" reconciliation (the open question) was
  resolved the wrong way.

## Open question for review/Decision

**F3 reconciliation.** The scaffold's post-install report prints
"Next steps (BOOTSTRAP.md Act II): … fill all block slots, run the R-F
gate, dogfood," which contradicts the quickstart's "for this quickstart we
leave them." Two ways to resolve, and the reviewers/Maintainer should weigh
in: (a) soften the scaffold's "Next steps" wording for the trivial path (a
scaffold output change — wider blast radius, but fixes it at the source);
or (b) have the quickstart explicitly explain the divergence (a docs-only
change — narrower, but leaves the contradiction visible). Default
recommendation: (b) for this proposal (docs-scoped), with (a) flagged as a
follow-up if adopters keep tripping.

## Review -- Claude (Internal, sub-agent A: Part A correctness) -- 2026-06-12

**Model**: Claude Opus 4.8 (fresh-context sub-agent). *Independence by time;
same agent type — a cross-type External pass is still recommended.*

**Steelman.** Central factual claims hold under verification: `--summary`
for `solo-greenfield` resolves exactly six modules; a real install reports
"Block slots requiring agent attention (21)"; all five named
onboarding/skills artifacts install; the Python-floor, F6, and F1
profile-comment claims are all confirmed. F1–F9 each get a faithful
remediation; F3 is correctly surfaced for Decision.

* **[A-R1] (required) The F2 `git add` fix is still incomplete — it misses
  `.gitignore`.** Running the exact quickstart `git add AGENTS.md VENDOR.md
  dev/ tools/ scripts/` leaves untracked `.agents/`, `docs/`, **and
  `.gitignore`** (the scaffold seeds it). Adding only `.agents/ docs/`
  still leaves the tree dirty at Step 6 — the very failure F2 is about. Add
  `.gitignore`.
* **[A-R2] The acceptance criterion "file list matches the install" is
  ambiguous** — many more files install than the onboarding five the
  refresh names (`scripts/foldback_export_scan.py`, `tools/prune_reflections.py`,
  …). State explicitly that the refresh is scoped to the onboarding
  subsystem and relies on the quickstart's existing "scaffold output is the
  authoritative tally" hedge.
* **[A-R3] Residual F9 drift unnamed:** the README `templates/` row omits
  `templates/onboarding/`. The F9 fix should verify the row against
  `ls templates/`.
* **[A-R4] Secondary surfaces verified clean** (getting-started, on-ramp,
  workflow-role carry no count/floor/file-list drift) — but all three share
  the F6 link gap; the refresh only fixes README + quickstart. Extend the
  scientific-minimal link to getting-started.
* **[A-R5] "Touches" under-declares** (`.gitignore`).

**Coverage.** *Covered:* 6 modules / 21 slots (verified live), the
onboarding file subsystem, the stale quickstart claims, the incomplete
`git add` (incl. `.gitignore`), the floor inconsistency, F6, secondary
surfaces clean. *Not covered:* Part B mechanism (other lens); the F3
decision; the doctrine/rate-limit classification.

**Second-round recommendation: recommended**, with [A-R1] required and
[A-R2]/[A-R3] should-fix before Decision. None are redesigns.

## Review -- Claude (Internal, sub-agent B: Part B drift-gate) -- 2026-06-12

**Model**: Claude Opus 4.8 (fresh-context sub-agent).

**Steelman.** Part B is the doctrine-faithful instinct (guard a
doc-mirrors-a-source number with a drift gate). The two design choices
(declared marker, live derivation) are defensible, and both source surfaces
exist (`--summary` roster; install slot count).

* **[B-R1] The gate already exists, half-built, and is GREEN while the docs
  are wrong.** `bootstrap/tests/test_quickstart_sequence.py:222` asserts the
  scaffold prints "(21)"; the suite passes while `quickstart.md:171` says
  "20." Part B is a *repair + extension* of an existing test, not greenfield
  — the proposal must cite it and explain why it failed to catch F1.
* **[B-R2] That test passes because it asserts against scaffold OUTPUT,
  never the quickstart PROSE,** with a hardcoded `21`. The non-negotiable
  invariant Part B must state: the asserted value is read *from the
  quickstart file* and compared to the *live resolution*, with **no third
  hardcoded literal**.
* **[B-R4] (most consequential) Cairn already ships the exact mechanism the
  proposal proposes to invent:** `scripts/verify_counts.py` +
  `scripts/measurements.py` (a `verify:`-keyed count annotation, re-measured by
  `check_cairn`). The real choice is **test vs. `verify_counts`**, not test
  vs. snippet-sync (the proposal compared the wrong incumbent). Reuse it:
  add resolver-backed measurement fns (`preset_module_count`,
  `preset_slot_count`) + registry keys + annotate the two numbers. Less
  net-new surface, inherits the security contract, fires under `check_cairn`,
  and `verify_counts` already prints a crisp "doc says 20, measured 21 --
  DRIFT" signal.
* **[B-R3] Pin the derivations:** module count from `expand_preset(cfg)`;
  slot count from the install-accounting path (not `--summary`, which exits
  first).
* **[B-R5/R7] Brittleness:** "four" is spelled out (digit markers won't
  bind); slot count is install-path-only; stdout-scraping couples to a print
  string — derive in-process. Convert spelled numbers to digits; pin the
  profile.
* **[B-R8] The file-list half of F1 is structurally outside any number-gate**
  — name that follow-up, and consider having the quickstart *point at* the
  authoritative tally rather than restate the file list (dodging the drift
  entirely).

**Coverage.** *Covered:* mechanism soundness, brittleness, the
existing-mechanism comparison (`verify_counts`/`test_quickstart_sequence`),
the scaffold surfaces, where it should live. *Low-confidence:* whether a
resolver-driven `MEASURE_FNS` entry fits `measurements.py`'s security
posture / soft cap (plan should check).

**Second-round recommendation: recommended for a second round — not ready
to ratify as written.** Re-ground Part B on `verify_counts`/`measurements`
+ reconcile with `test_quickstart_sequence.py`.

## Review -- Claude (Internal, sub-agent C: adopter-trust + scope + F3) -- 2026-06-12

**Model**: Claude Opus 4.8 (fresh-context sub-agent).

**Steelman.** Correctly aimed and motivated; the cold-walk confirms the
headline (four-vs-six, 20-vs-21). The secondary-finding instincts are right;
Part B's *diagnosis* (recurrence) is the right deeper read; keeping A+B
together is correct.

* **[C-R1/R2] Part B reinvents `verify_counts`/`measurements` and re-treads
  `test_quickstart_sequence.py`** (independent confirmation of B-R4/B-R1):
  re-target onto the existing `verify:` mechanism; cite the existing test.
* **[C-R3] A sixth drifted surface, missed by both audit and proposal:**
  `bootstrap/BOOTSTRAP.md:109-110` lists only five default-on modules
  (omits `documentation-plan`) — the canonical source the profile comment +
  quickstart mirror. Add it to Part A or scope it out explicitly.
* **[C-R5] "Uses Cairn's own doctrine on itself" is undercut** by proposing
  bespoke tooling instead of the existing drift-gate apparatus.
* **[C-R6] State the surface-audit boundary** (which surfaces were checked
  clean vs. deliberately left).
* **[C-R4 — decisive F3 call] Do (a) source-side, not the default (b)
  docs-only.** Under (b) the terminal still tells the adopter to fill 21
  slots + run a gate while the doc says "leave them" — for the skeptical
  persona, the tool contradicting the page is *more* corrosive than the
  count mismatch. **Third option (recommended):** make the scaffold's "Next
  steps" output context-aware — either a trivial/quickstart-path detection
  that prints a trimmed next-step, or reframe the block as "Next steps **for
  a real adoption** (BOOTSTRAP.md Act II)" so it no longer reads as an
  instruction for *this* run. (b) is acceptable only as a stopgap paired
  with a committed (a) — shipping (b) alone is knowingly shipping the
  predicted failure (the proposal's own "Signals wrong" predicts it).

**Coverage.** *Covered:* the adopter outcome (verified targets), F1–F9
weighting, scope (too-little: BOOTSTRAP.md; too-much: parallel tooling), the
F3 call. *Low-confidence:* honest about other profiles, but silent on the
BOOTSTRAP surface audit and the existing drift machinery.

**Second-round recommendation: recommended — with required revisions.**
Re-ground Part B; add BOOTSTRAP.md; resolve F3 source-side.

## Response -- Claude (author) -- 2026-06-12

**Model**: Claude Opus 4.8

The panel converged, with independent confirmation, on two things the
proposal got wrong, and caught a missed surface and an incomplete fix. I
accept the large majority; the dispositions:

* **[B-R4 / C-R1 — re-ground Part B on the existing `verify_counts` /
  `measurements` mechanism] — accept.** This is the headline revision. Part
  B was reinventing the exact in-tree apparatus that embodies the
  doc-drift-prevention doctrine it claimed to dogfood. Revised Part B
  annotates the two quickstart numbers with `verify:`-count markers and adds
  resolver-backed measurement fns + registry keys, so the existing
  `check_cairn` count lens fires — no bespoke test.
* **[B-R1 / B-R2 / C-R2 — the gate exists, green-but-blind] — accept.** The
  revision cites `test_quickstart_sequence.py:160,222`, states the gap
  (scaffold-output gated, prose ungated, hardcoded literal), and forbids any
  new hardcoded count.
* **[B-R3 / B-R5 / B-R7 — pin derivations, no spelled numbers, in-process] —
  accept**, folded into the revised Part B (module count from
  `expand_preset`; slot count from the install-accounting path; convert
  "four"→digit; the measurement fn checks `measurements.py`'s security
  posture per B's low-confidence note).
* **[A-R1 — `.gitignore` in the `git add` fix] — accept** (and **[A-R5]**
  add it to Touches).
* **[C-R3 — BOOTSTRAP.md:109-110 (5 modules)] — accept**; added to Part A's
  refresh + Touches.
* **[B-R8 — file-list outside a number-gate; point-at not restate] — accept
  with modification.** Revised Part A has the quickstart *point at* the
  scaffold's authoritative tally rather than re-enumerate the file list,
  which dodges file-list drift entirely (and resolves A-R2's ambiguity); a
  named follow-up covers any residual.
* **[C-R4 / F3 — source-side fix] — accept with modification.** Resolve F3
  at the terminal: reframe the scaffold's unconditional "Next steps" as
  "Next steps **for a real adoption** (BOOTSTRAP.md Act II)" (the low-blast
  reframe of option (iii)), so it stops contradicting the quickstart for the
  trivial path. This adds `bootstrap/_scaffold/install.py` to Touches. A
  context-aware `--quickstart` flag is noted as a richer follow-up.
* **[A-R3 — README `templates/onboarding/` row] — accept** (verify against
  `ls templates/`).
* **[A-R4 — extend the scientific-minimal link to getting-started] —
  accept.**
* **[C-R6 / A-R2 — state the surface-audit boundary] — accept**: the
  revision records which adopter surfaces were checked-and-clean
  (getting-started, on-ramp, workflow-role) vs. fixed (quickstart, README,
  example, profile, BOOTSTRAP).
* **A/B split — keep together** (both panel members agreed); no change.

## Revised proposal -- 2026-06-12

The aim and Part A's targets stand; the revisions tighten Part A and
re-ground Part B.

1. **Part B re-grounds on Cairn's existing drift apparatus, not new
   tooling.** Annotate the quickstart's `solo-greenfield` module count and
   slot count with `verify:`-count markers (keys `preset_module_count` /
   `preset_slot_count`); add two resolver-backed entries to
   `scripts/measurements.py` (module count from `expand_preset(cfg)`; slot
   count from the install-accounting path) under the existing closed
   `MEASURE_FNS` allowlist + REGISTRY, so `check_cairn`'s `verify_counts`
   lens re-measures and flags drift. Reconcile with
   `test_quickstart_sequence.py` (it gates scaffold output; this gates the
   prose↔runtime loop) — extend, don't duplicate. No hardcoded count
   literal survives. The plan confirms the resolver-driven measurement fn
   respects `measurements.py`'s security posture.
2. **The quickstart points at the authoritative tally instead of
   re-enumerating files** — dodging file-list drift entirely. The
   `verify:`-keyed numbers (module/slot counts) are the guarded facts;
   the file list becomes "the scaffold's install report is the authoritative
   list" with the onboarding subsystem named once as orientation, not a
   maintained enumeration.
3. **Part A also refreshes `bootstrap/BOOTSTRAP.md:109-110`** (the
   five-module default-on list → six) and fixes the `git add` line to
   include `.gitignore`, `.agents/`, and `docs/`.
4. **F3 is resolved source-side:** reframe `bootstrap/_scaffold/install.py`'s
   post-install "Next steps" block as "Next steps **for a real adoption**"
   so the terminal no longer contradicts the quickstart's trivial path.
5. **README:** fix the `templates/` row (add `templates/onboarding/`), link
   `examples/scientific-minimal/` (also from `docs/getting-started.md`).
6. **Surface-audit boundary recorded:** fixed — `docs/quickstart.md`,
   `README.md`, `examples/scientific-minimal/README.md`,
   `bootstrap/profiles/solo-greenfield.yml`, `bootstrap/BOOTSTRAP.md`,
   `bootstrap/_scaffold/install.py`; checked-and-clean —
   `docs/getting-started.md`, `on-ramp/README.md`, `docs/workflow-role.md`
   (no count/floor drift; the scientific-minimal link is the only addition).
7. **Updated Touches:** the four original surfaces + `bootstrap/BOOTSTRAP.md`,
   `bootstrap/_scaffold/install.py`, `scripts/measurements.py`,
   `docs/getting-started.md`, and the seeded `.gitignore` interaction.

**Named follow-up:** a richer context-aware scaffold next-steps (a
`--quickstart` mode), and extending the `verify:` count guard to other
adopter-facing counts beyond the quickstart, are deferred follow-ups.

## Decision -- Anthony Kendall (Maintainer) -- 2026-06-12

**Accepted — open a plan and implement.**

Maintainer authorization (verbatim, via the kickoff Decision prompt):

> "Accept — open a plan + implement"

Scribed by Claude at the Maintainer's explicit instruction. The Revised
proposal is the implementation contract: Part B re-grounded on the existing
`verify_counts`/`measurements` mechanism; the quickstart points at the
authoritative tally rather than re-listing files; `BOOTSTRAP.md` +
`.gitignore` added; F3 resolved source-side via the `install.py` "Next
steps" reframe. Non-trivial + multi-file → a plan sequences the work; this
proposal archives at plan-open.
