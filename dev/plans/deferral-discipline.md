# Plan: deferral discipline — the archive precondition routes, not only preserves

**Source proposal**: [`dev/proposals/archive/2026-08-04-claude-deferral-discipline.md`](../proposals/archive/2026-08-04-claude-deferral-discipline.md)
**Status**: awaiting-plan-review
**Plan review**: required(Internal) — ratified in the Decision (`6e349b3`)
**Last update**: 2026-08-04
**Opened**: 2026-08-04

## Source proposal

The archive precondition (`doctrine/lifecycle.md:403`) requires every
explicitly-deferred follow-up to have "a durable home outside the file", first-
naming `dev/PLANNING.md`. Composed with review-sweep lens #9 (which promotes
observations to findings) and the plan scope fence (which defers what it cannot
fix), that produces a one-way ratchet with no discarding step: `dev/PLANNING.md`
went from 349 to 1002 lines between 2026-07-22 and 2026-08-04, 59 of those items
in a single deferred-follow-ups section.

The Internal review established that Cairn **already has** the missing
disposition — `wontfix`, in the code-review-Response grammar
(`doctrine/proposals.md:458`), already mechanized in
`templates/modules/default-on/_lifecycle_metrics/subsystems.py`. It is simply not
available at archive time. So the accepted change is small: make the existing
grammar the archive precondition's vocabulary, add the one disposition it lacks,
and gate the board-depositing one behind the Maintainer.

Accepted as revised at `6e349b3`, plan review ratified at **Internal**.

## Proposed paths

Proposed paths:
- `dev/proposals/2026-08-04-claude-board-retro-disposition.md` — the D1 successor; opens in Chunk F, this session.

## Scope

**This plan executes C1–C7 of the Revised proposal** across fifteen surfaces:
the canonical doctrine rule, four sibling doctrine files, four adopter templates,
four self-hosted mirrors, and the byte-identical planner twin pair.

**Scope fence — what this plan does NOT do:**

* **The 59-row retrospective pass (D1).** Split out by the Decision. This plan
  *opens* its successor artifact (Chunk F) but performs **no** re-routing of
  existing `dev/PLANNING.md` rows. The board's existing content is untouched
  except for the archive-precondition prose at `dev/PLANNING.md:433-444`.
* **The content-parity gate (D2).** Explicitly **not carried** by the Decision:
  *"No authorizing words were given for it, and under the proposal's own C4 it is
  adopter-reaching and therefore ineligible for author disposition."* Invariant 3
  lands **documented as fail-open**. Building any mechanical content-parity check
  in this plan would contradict the Decision and fire the External-escalation
  rule the Internal tier was ratified against.
* **No new mechanical gate of any kind.** The planner strings stay unconditional
  reminders (`templates/skills/_lib/lifecycle_planner.py:878` is literally
  `gates.append((True,`). Item 7 of the proposal refuses to promote them and this
  plan honours that refusal.
* **`AGENTS.md` is not touched.** The proposal routes this as deliberation-process
  doctrine, not operational safety.

### Documentation / doctrine surface

This plan is **almost entirely** a doctrine and template change; there is no
`docs/` descriptive-layer surface. Routing per `docs/DOCUMENTATION_PLAN.md`: the
disposition grammar is cross-cutting **prescription**, so its canonical home is
`doctrine/lifecycle.md` with the siblings pointing at it, and its adopter-facing
surface is the `templates/core/` mirror. One `CHANGELOG.md > Unreleased >
Changed` line, because the archive precondition is a contributor-visible contract.

## Sequence

```
1. Chunk A -- doctrine/lifecycle.md: the canonical rule (C1, C2, C4)   [pending]
2. Chunk B -- the four sibling doctrine files (C3, C5, C6)             [pending]
3. Chunk C -- the four adopter templates                               [pending]
4. Chunk D -- the four self-hosted mirrors                             [pending]
5. Chunk E -- the planner twin pair (byte-identical, moves together)   [pending]
6. Chunk F -- CHANGELOG + open the D1 successor                        [pending]
```

### Chunk A — the canonical rule

| # | File | Change |
|---|------|--------|
| A1 | `doctrine/lifecycle.md` > "Archive precondition" | **C1** — precondition satisfied by a recorded disposition token, not only a durable home; `Follow-ups migrated to:` → `Dispositions:` |
| A2 | `doctrine/lifecycle.md` (same section) | **C2** — define `guard`: the follow-up is homed in an artifact that *executes*, and the entry names the node (`path::node`). Comments are explicitly ineligible |
| A3 | `doctrine/lifecycle.md` (same section) | **C4** — the two eligibility rules; explicit statement that there is **no** required ordering |
| A4 | `doctrine/lifecycle.md` (same section) | State that all three invariants are documentary — enforcer is *a reviewer opening both files at archive-preparation* |

### Chunk B — the sibling doctrine files

| # | File | Change |
|---|------|--------|
| B1 | `doctrine/proposals.md:450-458` | Extend the disposition grammar with `guard`; note the grammar now also governs archive-time dispositions |
| B2 | `doctrine/proposals.md:342-373` | Archive preconditions restate C1 by pointer; `Follow-ups migrated to:` → `Dispositions:` |
| B3 | `doctrine/plans.md:492`, `:543`, `:586` | Same token addition in the Sharpening template + archive precondition pointer |
| B4 | `doctrine/dual-review.md:245-247` | **C6** — lens #9 keeps its five satisfiers, gains the total mapping (test→`guard`, guard→`guard`, doc→`accept`, scope-cut→`accept`, wontfix→`wontfix`) |
| B5 | `doctrine/lifecycle-contract.md:137` | **C3 + C5** — the `review → archived` row: `Dispositions:` block, archive-preparation as the serialization point, `defer` needs a quoted Maintainer authorization |

### Chunk C — the adopter templates

| # | File | Change |
|---|------|--------|
| C1f | `templates/core/dev/PLANNING.md:97-108` | Mirror A1–A4 |
| C2f | `templates/core/dev/plans/_template.md:261-269` | Mirror the archive precondition wording |
| C3f | `templates/core/dev/proposals/_template.md:89` | Mirror the archive precondition wording |
| C4f | `templates/modules/team-gated/dual-review.md:69` | Mirror B4 (lens #9 verbatim quote) |

### Chunk D — the self-hosted mirrors

| # | File | Change |
|---|------|--------|
| D1f | `dev/PLANNING.md:433-444` | Mirror A1–A4 (prose only — **no** board rows re-routed) |
| D2f | `dev/plans/_template.md:261-269` | Mirror C2f |
| D3f | `dev/proposals/_template.md:103-108` | Mirror C3f |
| D4f | `dev/modules/dual-review.md:69` | Mirror C4f |

### Chunk E — the planner twins

| # | File | Change |
|---|------|--------|
| E1 | `templates/skills/_lib/lifecycle_planner.py:879`, `:1024` | Re-word the durable-home reminder strings to the `Dispositions:` form. Stay unconditional — do **not** promote `gates.append((True,` to a check |
| E2 | `tools/lifecycle_planner.py:879`, `:1024` | The byte-identical twin (blob `afa702d`) — same edit, same commit |

### Chunk F — changelog and the D1 successor

| # | File | Change |
|---|------|--------|
| F1 | `CHANGELOG.md > Unreleased > Changed` | One line: the archive precondition accepts a recorded disposition |
| F2 | stem `2026-08-04-claude-board-retro-disposition` (under `dev/proposals/`) | **Open the D1 successor** — the 59-row retro pass, carrying [I8]'s forwarding rule and the closed-artifact ineligibility. Its stem is named in the Chunk F commit body so its absence is visible in `git log` |

## Acceptance criteria

* **Tests that must pass** — `python -m pytest bootstrap/tests`, the full suite,
  under the canonical interpreter (Python 3.13.x). One node is load-bearing for
  Chunk E: [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
  `::test_every_self_hosted_twin_stays_byte_identical_to_its_source` (`:98`) fails
  if the two planner copies diverge, so it is what proves E1 and E2 moved
  together. **No new test is added** — see *Known omissions*.
* **Doc updates that must land** — all fifteen surfaces above (hand-authored;
  none generated, none snippet-synced), plus `CHANGELOG.md > Unreleased >
  Changed` (F1). The drift gates catch broken references, **not** absence, so
  each of the fifteen is confirmed by opening it at code review.
* **Examples / smoke checks** — `python bootstrap/scaffold.py --summary --config
  <profile>` proves the four adopter templates (Chunk C) still install. The
  Internal proposal review flagged this as unexercised evidence; it is exercised
  here.
* **Inbound path-link updates** — the source proposal moves to
  `dev/proposals/archive/` in the plan-open commit. `PLANNING.md` and
  `NEXT_SESSION.md` refer to plans by stem, so neither needs an edit.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants and their enforcers — all three are documentary, by Decision.**
  1. *No follow-up is silently dropped.* Enforcer: the `Dispositions:` block,
     checked by a reviewer at archive-preparation. **No test.**
  2. *`defer` is never taken without a quoted Maintainer authorization.*
     Enforcer: the same reviewer. **No test.**
  3. *Doctrine and its `templates/core/` mirror agree.* Enforcer: a reviewer
     opening both files. **No test** — the Internal review's mutation test
     (inverting `templates/core/dev/PLANNING.md` to contradict
     `doctrine/lifecycle.md` → `check_cairn` rc=0, 1916 pytest passed) proved the
     loop-fidelity lens and `bootstrap/fidelity-check.md` do not cover prose
     parity. D2 would have closed this and was **not authorized**.

  The one invariant with a real enforcer is *the planner twins stay
  byte-identical*, pinned by the `test_notice_install.py` node above. That is the
  only row in this table a deletion test would fail on, and it is sequenced into
  Chunk E.
* **Failure modes.** Every failure in this plan is a **prose defect**, which
  fails *open* — a mis-worded rule misroutes a future follow-up and nothing
  raises. The single exception is Chunk E: editing one planner copy and not the
  other fails **closed** at the twin-parity node.
* **Edge cases.** *Zero follow-ups* → the `Dispositions:` block is omitted
  (unchanged from today). *A proposal archiving inside its plan-open commit*
  (`doctrine/lifecycle-contract.md:133`) → its block is presented at that commit's
  preparation (C5). *Solo profile* → `defer` collapses to a written
  self-justification; stated in the doctrine text per D3, not left implicit.
* **Public-path → test mapping.** This plan adds **no public code path**. The
  only code edit is two message strings per planner copy, covered through the
  twin-parity node cited in *Acceptance*. Verified 2026-08-04: `grep` over
  `bootstrap/tests/` for the durable-home strings returns **zero** hits, so no
  test asserts their content and none needs updating for a re-word.
* **Known omissions.**
  * **No new test is written by this plan.** A doctrine sentence has no
    behavioral surface, and the one mechanical guard that would matter (content
    parity) is D2, which the Decision declined to authorize. Stating this plainly
    rather than adding a test that asserts a string exists — which would pass
    while the rule it describes went unfollowed.
  * **Invariant 3 ships fail-open**, knowingly, per the Decision.
  * **The (guard/wontfix/defer) routing estimate for the existing 59 rows is not
    reproduced here.** It was withdrawn in the Response as unreproducible; the D1
    successor produces the real figure per-item.

## Verification

Run before the cut. Cairn has **no CI** — every command below is run by a person
or an agent at the commit boundary, and nothing enforces them automatically:

* **Engine suite** — `python -m pytest bootstrap/tests` under the canonical
  interpreter (Python 3.13.x); a different minor silently changes the result.
* **Prose integrity** — `python scripts/check_cairn.py` (internal link / anchor
  resolution + claim-path check). The primary gate for this plan.
* **Quality gate** — `python scripts/quality_gate.py --sub neutrality`; this is a
  doctrine / template wording change, which is the neutrality surface.
* **Write-time claim check** — `python scripts/claim_check.py <file>` over this
  plan and the D1 successor. **One file per invocation.**
* **Scaffold smoke** — `python bootstrap/scaffold.py --summary --config <profile>`
  after Chunk C.

**Note on doc gates**: these catch drift, not absence. Confirm each of the fifteen
surfaces was actually edited by opening it — the gates will not tell you a mirror
was missed.

## Plan review

*Awaiting Internal plan review — implementation does not begin until this section
lands (`doctrine/plans.md:108`).*

## Code review

*Filled in after implementation commits land. Reviewer is not the implementing
agent.*

## Lasting-truth migration

*Filled in at archive time.*
