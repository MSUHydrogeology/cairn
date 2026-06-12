<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/lifecycle.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: adopter-entry doc-refresh + verify-count drift-gate

**Source proposal**: `dev/proposals/archive/2026-06-12-claude-adopter-entry-doc-refresh.md`
**Status**: open
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
* **Docs** — `python scripts/check_cairn.py` green over the refreshed docs
  (incl. the new `verify:` annotations resolving against the live
  measurements).

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

## Code review

*Filled in after implementation commits land.* Floor: not the implementing
agent.

## Lasting-truth migration

*Filled in at archive time.* Deferred follow-ups (the `--quickstart` mode;
extending the `verify:` guard to other adopter counts) migrate to
`dev/PLANNING.md` before archive.
