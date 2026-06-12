<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Adopter-entry doc-refresh + a drift-gate so the docs can't silently lag the scaffold

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-06-12
**Status**: proposed
**Touches**: `docs/quickstart.md`, `README.md`, `examples/scientific-minimal/README.md`, `bootstrap/profiles/solo-greenfield.yml` (the doc-refresh); a new drift-gate (a `bootstrap/tests/` test, plus possibly a `check_cairn` hook).
**Related**: the adopter-friction audit `dev/strategy/2026-06-12-claude-adopter-friction-audit.md` (this proposal implements its recommended package); the `doc-drift-prevention` module.
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

## Review -- {{reviewer}} -- {{YYYY-MM-DD}}

(awaiting Internal review — sub-agent panel)

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

(awaiting Maintainer Decision)
