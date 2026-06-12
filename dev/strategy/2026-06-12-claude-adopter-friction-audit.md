# Cairn adopter-friction audit — current state (post-self-host)

**Author**: Claude (Strategy), with a parallel surface-walk gather pass
**Role**: External Reviewer / prospective adopter
**Date**: 2026-06-12
**Status**: settled
**Type**: comparative-research
**Re-runs**: `dev/strategy/archive/2026-05-27-codex-cairn-adopter-friction-audit.md`
(the original pre-0.3 lens, archived once this re-run superseded it; this
is the v0.3 / self-hosted re-run)

## Lens

Read Cairn as a new potential adopter — a scientist maintaining or
starting a codebase, who knows only that Cairn promises a way to build
better scientific software with AI agents than ad-hoc prompting. The
question is not "is the doctrine internally coherent?" but **"does a
scientist + one AI agent know what to do, trust the apparatus, and get
value before the process feels heavier than the problem?"** A skeptical
first-time adopter.

## Summary

The original (2026-05-27) audit's pre-0.3 **adopter-friction package
shipped**: 8 of its 9 gaps are resolved, and the 9th (a scientific
example) exists as an artifact but is undiscoverable. On paper Cairn now
"feels small at the point of entry."

A fresh walk surfaces one **dominant, ironic** failure: the
**adopter-entry docs have drifted behind the shipped scaffold** — the
exact "docs lag the tool" failure mode Cairn's own lifecycle exists to
prevent. `docs/quickstart.md`'s most *checkable* claims (the module
count, the slot count, the installed-file list, and "leave the slots")
are now factually wrong against the live scaffold. Because the quickstart's
whole job is to let a skeptic confirm "the apparatus does what the page
says," a doc-vs-terminal mismatch at the install step **corrodes the
trust the quickstart exists to build**. The fix is a focused doc-refresh,
not a redesign.

## Original-gap resolution (the 9 from 2026-05-27)

1. **No 15-minute quickstart** — **RESOLVED** (`docs/quickstart.md`, a
   concrete 7-step recipe), with accuracy defects (F1).
2. **Bootstrap intimidating** — **RESOLVED**
   (`bootstrap/prompts/bootstrap-lite.md`; `BOOTSTRAP.md` opens with the
   "smaller first step" pointer).
3. **Manual module merging fragile** — **RESOLVED** (mechanized merge
   pass + `slot-content-stale-or-partial` fidelity check, `BOOTSTRAP.md`
   II-4/II-5).
4. **"Faster" claim not honest** — **RESOLVED** (the "slower for the first
   few changes" line is in `README.md`, `docs/quickstart.md`,
   `on-ramp/README.md`, and `docs/getting-started.md`, consistently).
5. **Single-agent reassurance** — **RESOLVED** (`README.md` "Cairn works
   with one agent"; `on-ramp/README.md` Level 1 as the solo+one-agent
   home).
6. **Legacy readiness artifact** — **RESOLVED**
   (`templates/codebase-readiness-report.md`, an 11-section G/M/P
   assessment with a profile-mapping appendix).
7. **Security earlier** — **RESOLVED** (`README.md` Trust-and-safety box;
   `SECURITY.md`; the readiness report's check-in posture).
8. **Minimal example too toy-like** — **PARTIAL**:
   `examples/scientific-minimal/` exists and is excellent, but it is **not
   linked from the README or the quickstart** (F6). The fix shipped; the
   wayfinding did not.
9. **Release hygiene / pristine tree** — **RESOLVED** (clean tree; no
   stray cache under the examples).

## Current friction (highest-friction first)

**F1 — the quickstart's load-bearing numbers and file list are stale
against the live scaffold (the headline).** `docs/quickstart.md` Step 3
tells the reader they "should see four modules" for `solo-greenfield`
(`lifecycle-metrics`, `reflections`, `claim-check`, `fold-back-ledger`) and
that the scaffold reports "20 unfilled block slots." **Verified against the
live scaffold:** `solo-greenfield` resolves **six** default-on modules —
those four *plus* `incident-trackers` and `documentation-plan` — and the
install reports **21** slots. The named-file list also omits an entire
subsystem the scaffold now installs: `.agents/skills/` (session-start /
session-end), `tools/lifecycle.py`, `scripts/_onboarding/`,
`dev/modules/onboarding/`, and `docs/DOCUMENTATION_PLAN.md`. The
`bootstrap/profiles/solo-greenfield.yml` header comment carries the same
stale four-module claim. *Lens:* a skeptic who reads "four," runs the
command, and sees "six" immediately distrusts the apparatus — exactly the
trust the page exists to build.

**F2 — the quickstart's `git add` line drops files the scaffold wrote.**
Step 3's `git add AGENTS.md VENDOR.md dev/ tools/ scripts/` omits
`.agents/` and `docs/`, so the documented commit is *incomplete*; the
"one commit per lifecycle step, visibly clean" promise breaks on the very
first commit, and Step 6's `git log` shows an untracked `.agents/` the
adopter was never told about.

**F3 — the scaffold's own "Next steps" output contradicts the quickstart.**
The post-scaffold report prints "Next steps (BOOTSTRAP.md Act II): … Fill
all block slots (II-4). Run the R-F acceptance gate (II-5). Dogfood…" The
quickstart says the opposite for this path: "we leave them; the trivial
dogfood does not need them filled." A newcomer reading doc and terminal
side by side cannot tell which authority to trust — and the tool's
instruction (fill 21 slots, run a gate) makes the "15–25 minute" promise
feel false.

**F4 — an unexplained provenance warning fires on every quickstart run.**
Step 1 clones the tip (not a tagged release), so the scaffold prints a
provenance warning suggesting `--allow-dev`. A security-conscious
scientist — the exact persona the Trust-and-safety box courts — hits this
on their first command with no preparation. One sentence ("you'll see a
provenance warning because you cloned the tip; expected for a shakedown")
defuses it.

**F5 — the Python-version floor is stated inconsistently across three
surfaces.** The intended floor is **3.11+** (a deliberate, security-driven
choice — a dependency deprecation / security floor), and
`bootstrap/prompts/bootstrap-lite.md` states it correctly. But
`docs/quickstart.md` says 3.8+ and `examples/scientific-minimal/README.md`
says 3.10+ — both stale and **below** the security floor. The apparatus
looks under-tested on its own prerequisites — corrosive for a scientist
evaluating reproducibility discipline, and the quickstart/example numbers
actively undersell the security posture. Fix: raise both to 3.11+.

**F6 — the scientific example is undiscoverable from the front door.** The
`README.md` repo-layout table and examples row cite only
`examples/minimal/` (the `greet` toy the README itself calls a toy);
neither the README nor `docs/quickstart.md` links
`examples/scientific-minimal/`. The artifact built to answer gap #8 is
hidden from the scientist it was built for.

**F7 — `/path/to/cairn` placeholders break literal copy-paste on the most
important command.** Step 1 clones into `cairn/`, but Steps 2–3 use
`/path/to/cairn/bootstrap/scaffold.py`. A true copy-paste fails on the
scaffold command. A single `export CAIRN=$(pwd)` in Step 1 makes the rest
literally pasteable.

**F8 — onboarding/skills vocabulary leaks into the scaffold output with no
entry-doc coverage.** The scaffold references "progressive onboarding,"
"lifecycle skills," `session-start`/`session-end`, and `/good-morning` —
none of which appear in the README, quickstart, getting-started, or
on-ramp. The adopter ends Step 3 holding a `.agents/skills/` tree and a
`tools/lifecycle.py` CLI the docs never mention.

**F9 — the README repo-layout table is out of step with what installs.**
It describes `templates/` as `core/` + `modules/default-on/` +
`modules/team-gated/` + `phase-0/`, but the scaffold now also installs an
onboarding module layer and the documentation-plan module. Lowest-stakes,
same root cause.

**Root cause (F1–F4, F8, F9):** the scaffold gained an onboarding/skills
layer and the `incident-trackers` + `documentation-plan` default-on
modules *after* the pre-0.3 friction package shipped; the entry docs were
not regenerated against it. The doctrine/docs layer drifted behind the
tool — precisely the failure Cairn's lifecycle exists to prevent. The fix
is a focused refresh, not a redesign.

## Where Cairn now overachieves

* **The honest-speed framing is everywhere and consistent** — four
  surfaces carry compatible "slower first, pays back later" wording; a
  skeptic is never sold a false speed promise.
* **The single-agent reassurance is explicit and repeated** — README,
  on-ramp Level 1, and bootstrap-lite all tell a one-human+one-agent
  scientist this works for them and how the Dual-Review tier degrades
  gracefully.
* **The Codebase Readiness Report is excellent and genuinely
  pre-doctrine** — scientifically literate (sign conventions, hidden
  state, reproducibility, data provenance), with a real scoring→level
  mapping and a standout privacy-aware "what to check in" posture.
* **The scientific-minimal example is the right artifact** — a
  mass-balance invariant, explicit tolerance rationale, sign/unit
  conventions made load-bearing, a non-vacuous test, exit codes, zero
  third-party deps. A hydrologist recognizes it instantly. Its only
  problem is discoverability (F6).
* **The trust contract is mature** — the README box's "Cairn's own tools
  never phone home, but the *agents* you run send everything they read to
  their provider" is exactly the nuance a scientist needs; `SECURITY.md`'s
  supply-chain threat model is unusually serious for a methodology repo.
* **`docs/workflow-role.md` nails the most common misread** — the "what
  Cairn does NOT do" framing (not CI, not a test runner, not a prompt
  library) is what a tool-fatigued scientist needs to decide whether to
  invest.

## Quickstart cold-walk verdict

The path **mechanically works end-to-end** (install succeeds, the lifecycle
is real, teardown is clean) — but a first-time adopter loses trust around
**Step 3**, because the doc's described output no longer matches the tool's
actual output (F1), the documented commit is incomplete (F2), the tool's
"Next steps" contradict the doc (F3), and two copy-paste breaks (F4
warning, F7 placeholder) hit the most important command. The 15–25-minute
*clock* is plausible for the trivial path; the 15–25-minute *confidence* is
not, because the page's most checkable claims are exactly the ones now
wrong.

## Recommended package — a doc-refresh, not doctrine

1. **Regenerate `docs/quickstart.md` Step 3 from a live `solo-greenfield`
   run** — the module roster (six), the slot count (21), and the
   installed-file list (include the onboarding/skills/docs subsystem);
   fix the `solo-greenfield.yml` header comment too.
2. **Reconcile "leave the slots" with the scaffold's "Next steps"** (F3) —
   either soften the scaffold's next-steps wording for the trivial path,
   or have the quickstart explain the divergence explicitly.
3. **Add one sentence each** for the provenance warning (F4) and the
   onboarding/skills artifacts (F8).
4. **Align the Python floor** (F5) — raise `docs/quickstart.md` (3.8+) and
   `examples/scientific-minimal/README.md` (3.10+) to **3.11+**, the
   security-driven floor that `bootstrap/prompts/bootstrap-lite.md` already
   states.
5. **Link `examples/scientific-minimal/` from the README and the
   quickstart's "what next"** (F6) — close gap #8's discoverability.
6. **Refresh the README repo-layout table** for the current module
   taxonomy (F9); fix the `git add` line (F2) and the `/path/to/cairn`
   placeholders (F7).
7. **Durable fix (a candidate proposal, not a one-time refresh):** make
   the quickstart's load-bearing numbers **generated or drift-gated**
   against a live scaffold run, rather than hand-maintained. This failure
   recurs every time the default-on set changes — which is exactly the
   class the `doc-drift-prevention` module exists to guard. A small drift
   gate ("the quickstart's claimed module/slot counts match a live
   `solo-greenfield` install") would have caught F1 at the moment the
   default-on set grew.

## Product framing (unchanged, still right)

> Start small. Use Cairn to make one AI-assisted change with a recorded
> decision and test. Keep the apparatus only as heavy as your codebase and
> team earn.

The promise is sound; the entry surface just needs to *match the tool* so
a skeptic's first command confirms the promise instead of undercutting it.
