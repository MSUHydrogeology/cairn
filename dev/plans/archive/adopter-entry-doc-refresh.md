<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/lifecycle.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: adopter-entry doc-refresh + verify-count drift-gate

**Source proposal**: `dev/proposals/archive/2026-06-12-claude-adopter-entry-doc-refresh.md`
**Status**: archived
**Plan review**: not required — the revised approach was reviewed at
proposal stage by a 3-reviewer Internal panel and accepted with revisions
folded in; this plan only sequences accepted work.
**Last update**: 2026-06-12
**Opened**: 2026-06-12

## Source proposal

The 2026-06-12 adopter-friction audit found the adopter-entry docs drifted
behind the scaffold (`quickstart` names 4 modules / 20 slots; the live
`solo-greenfield` install is 6 / 21). The accepted, revised proposal: refresh
the drifted surfaces, and re-ground a drift-gate on Cairn's existing
`verify_counts`/`measurements` mechanism so the quickstart's load-bearing
numbers can't silently lag the scaffold; resolve the F3 doc-vs-terminal
contradiction source-side.

## Scope

Implement the Revised proposal. **Scope fence (what this does NOT do):** no
`--quickstart` scaffold mode (deferred follow-up); no extension of the
`verify:` guard beyond the quickstart's two `solo-greenfield` numbers
(deferred); the quickstart *points at* the scaffold's authoritative
file-tally rather than enumerating files (so file-list drift is dodged, not
gated).

### Documentation / doctrine surface

Descriptive/entry docs + scaffold output; no doctrine change. Implements the
existing `doc-drift-prevention` principle (`doctrine/doc-governance.md`), not
a new rule.

## Sequence

```
A. verify-count gate          -- scripts/measurements.py: preset_module_count + preset_slot_count   [commit pending]
B. quickstart refresh         -- docs/quickstart.md: counts+annotations, point-at-tally, git add, $CAIRN, floor   [commit pending]
C. other adopter surfaces     -- README, solo-greenfield.yml, BOOTSTRAP.md, scientific-minimal, getting-started   [commit pending]
D. install.py Next-steps (F3) -- bootstrap/_scaffold/install.py: reframe "Next steps for a real adoption"   [commit pending]
```

### Chunk A — the verify-count gate (mechanism first; the quickstart's annotations depend on it)

| # | File | Change |
|---|------|--------|
| A1 | `scripts/measurements.py` | Add `preset_module_count` (live: `len(expand_preset(solo-greenfield))`) + `preset_slot_count` (live: the install-accounting slot count) as `Invariant`s under the closed `MEASURE_FNS` allowlist + `REGISTRY`; confirm the resolver import respects the module's security posture. |
| A2 | `bootstrap/tests/test_check_cairn_counts.py` (or sibling) | Cover the two new measurements; assert drift is flagged. |
| A3 | `bootstrap/tests/test_quickstart_sequence.py` | Reconcile: it gates scaffold *output* (hardcoded 21); note the prose↔runtime gate now lives in the `verify:` annotations — extend, don't duplicate; remove any hardcoded literal that the annotation now owns. |

### Chunk B — quickstart refresh

| # | File | Change |
|---|------|--------|
| B1 | `docs/quickstart.md` | Module count → **6** (digit) + `verify: preset_module_count` annotation; slot count → **21** (digit) + `verify: preset_slot_count`; replace the file *enumeration* with a point-at-the-scaffold-tally + one orientation line naming the onboarding subsystem; `git add` → include `.gitignore .agents/ docs/`; add `export CAIRN=$(pwd)` to Step 1 + replace `/path/to/cairn`; one sentence each for the provenance warning + the onboarding/skills artifacts; Python floor → **3.11+**. |

### Chunk C — other adopter surfaces

| # | File | Change |
|---|------|--------|
| C1 | `README.md` | `templates/` row += `onboarding/`; link `examples/scientific-minimal/` from the examples row. |
| C2 | `bootstrap/profiles/solo-greenfield.yml` | Header comment: four → six default-on modules. |
| C3 | `bootstrap/BOOTSTRAP.md` | I-5 default-on list: five → six (add `documentation-plan`). |
| C4 | `examples/scientific-minimal/README.md` | Python floor → 3.11+. |
| C5 | `docs/getting-started.md` | Add a `examples/scientific-minimal/` pointer alongside the `examples/minimal/` one. |

### Chunk D — install.py Next-steps reframe (F3)

| # | File | Change |
|---|------|--------|
| D1 | `bootstrap/_scaffold/install.py` | Reframe the unconditional post-install "Next steps (BOOTSTRAP.md Act II)" block as "Next steps **for a real adoption**" so it stops contradicting the quickstart's trivial path. |
| D2 | `bootstrap/tests/` | Adjust any test asserting the old "Next steps" wording. |

## Acceptance criteria

* **Tests** — `python -m pytest bootstrap/tests` green (the two new
  measurements + any adjusted output assertions); the verify-count gate
  fails on the pre-refresh numbers (4≠6 / 20≠21) and passes on the refreshed
  ones.
* **Examples / smoke** — a cold-walk of `docs/quickstart.md` end-to-end on a
  disposable repo: every stated number + the `git add` line match the live
  install; `git status` clean after the documented commit; the scaffold's
  "Next steps" no longer contradicts the page.
* **Docs** — `python scripts/check_cairn.py` green over the refreshed docs.
  (Implementation note: the drift-gate landed as a `bootstrap/tests/`
  extension, **not** a `verify:`/measurements annotation — so it runs under
  pytest, not the `check_cairn` count lens. See the Code review's deviation
  note for the rationale; this criterion is corrected from its original
  "incl. the new `verify:` annotations" wording, which no longer applies.)

### Author-accounting

* **Invariant** — the quickstart's stated `solo-greenfield` module + slot
  counts equal a live resolution, enforced by the A1 measurements via
  `check_cairn`. *Enforcer:* A1 + A2.
* **Failure mode** — closed (a hard `check_cairn`/test failure naming the
  divergence). Risk: a resolver import widening `measurements.py`'s trust
  surface — A1 confirms the closed-allowlist posture survives.
* **Edge cases** — spelled-out numbers converted to digits (B1); slot count
  from the install path, not `--summary`; a future default-on change fires
  the gate (correct).
* **Known omission** — file-list drift is dodged (point-at), not gated; other
  profiles + a `--quickstart` mode are deferred follow-ups.

## Verification

```
python -m pytest bootstrap/tests
python scripts/check_cairn.py
# cold-walk: scaffold solo-greenfield into a tmp repo; diff documented numbers/files vs actual
```

## Code review -- Claude (sub-agent, fresh context, not the implementer) -- 2026-06-12

**Verdict: Accept-with-followups** of commit `63db56f`.

**Falsification ledger (highlights).** The gate was proven *non-vacuous* by
mutation: editing the quickstart's `**6** modules` → `**5**` and `**21
…slots**` → `**20…**` each made the test FAIL with a clear message
(reverted). The `-> modules:` info line is on **stderr** and the slot tally
on **stdout** — the test's `result.stdout + result.stderr` combine handles
it; `--summary` emits no roster line, so the gate correctly runs on the
install path. The F2 `git add` was cold-walked exhaustively: every
scaffold-written path (`.agents/ .gitignore AGENTS.md VENDOR.md dev/ docs/
scripts/ tools/`) is captured; only the adopter-authored `profile.yml`
stays untracked (correct). The 2 `test_ast_attest` failures were confirmed
**pre-existing** at the parent commit `0d24fec`; this commit's `install.py`
edit only moves `print_report`'s hash (no new drifting function, no new
failure). Verification re-run: `pytest test_quickstart_sequence.py` 8
passed; `pytest bootstrap/tests` 1404 passed / 2 pre-existing ast_attest;
`check_cairn` OK; cold-walk doc==terminal (6/21/git-add/Next-steps).

**The deviation (recorded here per the review's required follow-up #1).**
The accepted proposal's Part B contracted the `verify_counts`/`measurements`
mechanism (plan A1/A2 + B1's `<!-- verify: -->` annotations). The
implementation instead **extended `bootstrap/tests/test_quickstart_sequence.py`**
to read the quickstart's two prose numbers and assert them against a live
`solo-greenfield` install. This is *faithful to the proposal's intent* (the
B-R2 non-negotiable — read-from-doc, compare-to-live, no third hardcoded
literal — is fully honored, and the prose↔runtime loop the old green-but-blind
test left open is closed) but is a *genuine departure from the contract's
chosen means*. Engineering rationale: `MEASURE_FNS` is a closed allowlist of
`(root, target)` file-path functions; the slot count is only produced by a
full install (not a bounded file scan), so a `measurements.py` fn for it
would have to *run an install* and would widen that module's trust surface —
which the proposal's own author-accounting and the Internal panel's
low-confidence note both flagged. The pytest extension avoids that
surface-widening. **Cost:** the counts are now guarded in the bootstrap
pytest run, not under `check_cairn`'s docs-layer lens.

**Required follow-ups (review):** (1) record this deviation in the plan +
correct the now-false acceptance criterion — *done above + here*; (2) a
Maintainer judgment call on the guard scope — **resolved: Maintainer
decision (2026-06-12) to also wire the module count under `check_cairn`.**
Done: `scripts/measurements.py` gains a resolve-only `count_preset_modules`
fn (imports `_scaffold.expand_preset` in-process; no install/write; preset
name code-fixed) + a `solo_greenfield_module_count` Invariant, and
`docs/quickstart.md` carries the `verify:` annotation. So the **module
count is now guarded by both** the `check_cairn` docs lens (re-measures +
flags `doc says N, measured M -- DRIFT`) **and** the install-path pytest
gate; the **slot count** (which only a full install produces) stays guarded
by the pytest gate. Verified: drift flagged on a mutated number under
`check_cairn`; 102 measurements/verify/preset tests pass.

No correctness defect; no new bug. The shipped gate works.

## Lasting-truth migration

Archived 2026-06-12. **Follow-ups migrated to:** `dev/PLANNING.md` > Queued
("Adopter-entry doc-refresh follow-ups") — the context-aware scaffold
`--quickstart` mode, and extending the `verify:` count guard to other
adopter-facing counts. Both are deferred, each its own future proposal.

**Loop-fidelity sign-off.** The Decision→implementation chain holds: the
accepted proposal's intent (refresh the drifted entry docs + a drift-gate
that closes the prose↔runtime loop) shipped in `63db56f` + `6d61926`; the
one mechanism deviation (test-extension over the `verify:` annotation for
the slot count) is recorded in the Code review with rationale, and the
module count was additionally wired under `check_cairn` per the Maintainer's
follow-up decision. Code review: accept-with-followups, both resolved.
Verification green (drift-gate proven non-vacuous; 1404 + 102 tests;
`check_cairn` OK; F2 cold-walk clean).
