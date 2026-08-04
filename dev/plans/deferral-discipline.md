# Plan: deferral discipline — the archive precondition routes, not only preserves

**Source proposal**: [`dev/proposals/archive/2026-08-04-claude-deferral-discipline.md`](../proposals/archive/2026-08-04-claude-deferral-discipline.md)
**Status**: executing
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

### Internal plan review -- Claude (fresh session) -- 2026-08-04

**Model**: claude-opus-5
**Reviewed at**: `2ec7ca4` (the tree moved to `4a7d70a` mid-review — a concurrent
session landed `transition-lint` Chunk D; nothing it touched overlaps this plan's
fifteen surfaces)
**Interpreter for every figure below**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13), the canonical interpreter

Requested by the Maintainer in the Decision (`6e349b3`): *"Please open this plan,
review it internally, then implement + code review and archive independently."*
Tier ratified at Internal there. Implementation has not started, so the bar
applied below is *is it sequenced and protected by acceptance criteria*, not
*does the landed code work*.

**Structural-independence stance.** Same-type, fresh session — the Internal
floor and nothing more. The author is Claude (Strategy); I am Claude with no
inherited context. The design was settled at proposal review and I did not
re-open it; this pass is about the execution spec.

**Verification done before drafting** — every load-bearing figure re-derived by
running something, none accepted on assertion:

* `python -m pytest bootstrap/tests` at `2ec7ca4` → **1950 passed**, 246.98s,
  exit 0. The pre-implementation baseline.
* `python scripts/check_cairn.py` → **OK — 191 Markdown file(s) scanned; no
  issues.** The plan-open body records 11 issues; those were repaired by
  `2ec7ca4` ("repair the citations the five archive moves broke"). I confirmed
  independently that `9052b09` touches only the plan file and the proposal move,
  so none of the 11 originated here. **This plan starts from a clean
  prose-integrity baseline** — the characterization in the plan-open body holds
  and is now historical.
* `python scripts/sync_doc_snippets.py --check` → OK, 252 docs, no drift; and no
  file among the fifteen carries a snippet marker. The *"none generated, none
  snippet-synced"* claim **holds**.
* `python scripts/claim_check.py dev/plans/deferral-discipline.md` → OK, no
  flags; the `Proposed paths:` forward-reference for the D1 successor resolves.
* `python bootstrap/scaffold.py --help` → `--summary` and `--config` both exist,
  and `bootstrap/profiles/` carries three profiles. The Chunk-C smoke check is
  runnable as written.
* **Deletion test on the one named enforcer.** Mutated a single string in
  `tools/lifecycle_planner.py`, leaving `templates/skills/_lib/lifecycle_planner.py`
  untouched → `bootstrap/tests/test_notice_install.py`
  `::test_every_self_hosted_twin_stays_byte_identical_to_its_source`
  **FAILED** (`twin parity broken: tools/lifecycle_planner.py !=
  templates/skills/_lib/lifecycle_planner.py`); restored → passes. `git ls-files -s`
  puts both copies at blob `afa702d`.
* Every line citation in the six chunk tables opened and read.
* An independent sweep for all four carried strings across `doctrine/`,
  `templates/`, `dev/`, `bootstrap/`, `tools/`, `scripts/`, `.agents/`, `docs/`.

### Steelman

**Chunk A-first is correct, and the sequence has no cycle.** The canonical rule
lands before every surface that points at it; Chunks E and F are genuinely
independent of A–D. I looked specifically for a later chunk depending on state an
earlier one does not create, and there is none.

**Chunk E's "moves together" instruction is the right shape and is backed by a
real enforcer**, which I verified by mutation rather than by reading. Naming the
exact node in *Acceptance* instead of gesturing at "the suite" is the discipline
`AGENTS.md` > "Name the trigger, check what it checks" asks for, and on that one
claim the plan passes its own test: the node exists at `:98`, it compares bytes,
and it fails when one copy moves alone.

**The scope fence holds on both halves the Decision fenced.** I read all six
chunk tables looking for a smuggled D2 or a board re-route. Neither is there: no
chunk adds a checker, a test, or a count guard, and D1f says *"prose only — **no**
board rows re-routed"*. The plan does not overstep the Decision. It also carries
the half the Decision *did* authorize, and better than its own text claims — see
[P9].

**The author-accounting refuses the flattering claim in three places** — all three
invariants marked documentary, the routing estimate withdrawn rather than
softened, and the zero-hit grep stated against the plan's own interest. I re-ran
that grep: `durable home`, `Follow-ups migrated`, and `has_followups_migrated`
return **zero hits** across `bootstrap/tests/`. That one is true, and it is the
sentence that should have prompted the author to ask what *else* is unguarded.

My findings are concentrated on one factual mis-scoping rather than a design
error: **the planner is not a pair of message strings.**

---

### Findings

#### [P1] (LOAD-BEARING) — Chunk E is scoped to two message strings; the planner carries a live conditional check on the exact string C1 renames

The scope fence says:

> **No new mechanical gate of any kind.** The planner strings stay unconditional
> reminders (`templates/skills/_lib/lifecycle_planner.py:878` is literally
> `gates.append((True,`).

`:878` *is* `gates.append((True,` — confirmed. But that is true of one site and
false as a description of the file. Each planner copy carries **six** sites bound
to this string, and two of them are a check:

| site | what it is | in Chunk E? |
|---|---|---|
| `:501` | `self.has_followups_migrated = False` | no |
| `:630-631` | `re.search(r"^\s*Follow-ups migrated to\s*:", text, re.MULTILINE)` — **the recognizer** | **no** |
| `:798-801` | `if not art.has_followups_migrated:` → `"status is 'archived' but no 'Follow-ups migrated to:' block is present (archive precondition)."` — **a conditional violation** | **no** |
| `:879-880` | the unconditional reminder | yes |
| `:1013` | the `-> archived` scaffold **emits** `"Follow-ups migrated to:\n"` | **no** |
| `:1024-1025` | the unconditional manifest line | yes |

Reproducer — one archived artifact, block renamed, nothing else changed:

```
OLD form (Follow-ups migrated to:)  -> has_followups_migrated=True   (no archive violation)
NEW form (Dispositions:)            -> has_followups_migrated=False
    VIOLATION: status is 'archived' but no 'Follow-ups migrated to:' block
               is present (archive precondition).
```

An artifact written to **the doctrine this plan lands** is reported by the shipped
planner as violating the archive precondition. This is not dormant plumbing:
`cmd_scan` (`tools/lifecycle_planner.py:1111`) documents itself as *"the
**adopter-side fidelity scan** (R3) ... Exit code is non-zero when any violation
is found, so an adopter test wrapper can assert a clean corpus"*, and
`python tools/lifecycle_planner.py scan --include-archive` on the live corpus
today reports **35 of 69 artifacts** carrying violations — the signal is live.

Three sentences of the plan's own accounting are falsified:

* *"The only code edit is two message strings per planner copy"* — it is four to
  six sites, one a regex and one a branch.
* *"Every failure in this plan is a **prose defect**, which fails *open*"* — this
  one fails **closed against compliant artifacts**, which is worse than
  fail-open: it trains readers to ignore the scan.
* *"This plan adds **no public code path**"* — it changes the recognized
  vocabulary of an existing adopter-facing check.

There is also a design decision buried here that the plan never surfaces: the
recognizer must accept **both** spellings. Measured — **six** archived artifacts
satisfy the recognizer today (`dev/plans/archive/`: `adopter-licensing-compliance`,
`ast-known-new-repin`, `first-session-survivability`, `record-corrections`,
`review-record-integrity`, `solo-legacy-adopter-path`); a recognizer matching only
`Dispositions:` would newly flag all six.

**Satisfier** — extend Chunk E to `:501`, `:630-631`, `:798-801` and `:1013` in
**both** copies; state in the chunk cell that the recognizer accepts the legacy
`Follow-ups migrated to:` **and** the new `Dispositions:` form; correct the three
author-accounting sentences above; and record explicitly that this is *keeping an
existing check consistent with renamed doctrine*, not promoting `:878` to a
check — so it does **not** fire the proposal's External-escalation rule.

#### [P2] (LOAD-BEARING) — C3 and C5 land in one table cell of a sibling file; the four adopter templates never receive the Maintainer-approval gate

The plan's own routing statement says the disposition grammar *"is cross-cutting
**prescription**, so its canonical home is `doctrine/lifecycle.md` with the
siblings pointing at it, and its adopter-facing surface is the `templates/core/`
mirror."* The chunk tables do not follow it.

Chunk A's four rows carry **C1, C2, C4** — the Sequence line says so. **C3**
(*`defer` at archive time requires a quoted Maintainer authorization*) and **C5**
(*archive-preparation is the single serialization point*) appear in exactly one
place in the whole plan: row **B5**, `doctrine/lifecycle-contract.md:137`. Three
defects follow:

1. **The canonical section never states the rule.** `doctrine/lifecycle.md:403-421`
   is the archive precondition in full; after Chunk A it defines the disposition
   tokens and says nothing about who may authorize `defer`. A reader consulting
   the canonical home learns the vocabulary and not the gate.
2. **Adopters do not get it at all.** Chunk C's rows say *"Mirror A1–A4"* and
   *"Mirror the archive precondition wording"* — and A1–A4 are C1/C2/C4. So
   `templates/core/dev/PLANNING.md` would ship the disposition vocabulary
   **without** the approval gate, which is the change's entire backpressure
   mechanism, is the Maintainer's own contribution to the proposal, and is what C7
   means by *"The fifteen surfaces carry it."* This is the plan **under**-delivering
   what the Decision authorized.
3. **It is homed in a column headed "Machine-verifiable preconditions"**
   (`doctrine/lifecycle-contract.md:131`). A rule requiring a quoted human
   authorization is the least machine-verifiable thing in the change. That is the
   `gate-claims-vs-enforcement` shape, in a plan whose [I1] lineage exists because
   of it.

Separable and related: **D3 has no chunk row at all.** *Edge cases* asserts
*"Solo profile → `defer` collapses to a written self-justification; stated in the
doctrine text per D3, not left implicit"* — but no row in any table places that
sentence in any file. An implementer following the tables would not write it, and
no acceptance criterion would notice.

**Satisfier** — add an **A5** row placing C3, C5 and the D3 solo-profile sentence
in `doctrine/lifecycle.md` > "Archive precondition", and extend C1f and D1f to
mirror them. B5 then restates by pointer, which is what the plan's own routing
rule says a sibling should do.

#### [P3] (LOAD-BEARING) — three chunk-table citations are wrong or incomplete; "all fifteen surfaces" is not reachable by following the tables

**(a) `dev/plans/_template.md:261-269` (row D2f) is the wrong range.** Those lines
are the `## Plan review` and `## Code review` headers. The Lasting-truth migration
content — the block form at `:285`, the durable-home clause at `:292` — is at
**`:281-293`**. The cause is visible: D2f says *"Mirror C2f"* and reuses C2f's
range verbatim, but the files are not the same length (`dev/plans/_template.md`
is 295 lines; `templates/core/dev/plans/_template.md` is 272). C2f's `:261-269`
is correct **for the template**; copying it into D2f is not. This is the third
citation defect in this artifact's history and the same mechanism each time — a
figure carried rather than re-derived.

**(b) `doctrine/plans.md:605` is cited by no row.** B3 names `:492`, `:543`,
`:586`. The literal block form lives in the fenced example at
`doctrine/plans.md:602-611`. There are only **four** canonical statements of the
block form in `doctrine/` — `lifecycle.md:417` (A1 ✓), `proposals.md:364` (inside
B2's range ✓), `lifecycle-contract.md:137` (B5 ✓), and **this one, uncited**. A1
renames the block; `doctrine/plans.md` would be left asserting the old form, in
the very section (`## Lasting-truth migration doctrine`) both plan templates point
at.

**(c) `templates/core/dev/proposals/_template.md:89` (row C3f)** points one line
above the string, which is at `:90`. Cosmetic, but a reader checking the cell does
not find what the cell describes.

**Satisfier** — correct D2f to `:281-293`; add `:602-611` to B3; nudge C3f to
`:88-91`. Then re-derive every remaining cell against the tree rather than against
its sibling row.

#### [P4] (important) — the one new token, `guard`, is silently discarded by the only mechanized consumer of the grammar the plan extends

[I2]'s satisfier was adopted precisely to avoid a parallel vocabulary, and the
Response claims the result *"removes the parallel-vocabulary hazard, including the
silent-drop behaviour of `_normalize_disposition_token`."* True for four tokens,
false for the fifth.

`templates/modules/default-on/_lifecycle_metrics/subsystems.py:88-94` defines
`_DISPOSITION_BUCKETS = ('accept', 'accept_with_modification', 'reject', 'defer',
'wontfix')`; `_normalize_disposition_token` (`:105-127`) returns `''` for anything
else, and `_parse_disposition_tokens` (`:130-145`) drops falsy buckets. Measured:

```
'accept' -> 'accept'    'reject'  -> 'reject'    'defer' -> 'defer'
'wontfix'-> 'wontfix'   'guard'   -> ''          'guard (pinned at tests/test_x.py::test_y)' -> ''

_review_yield_counts over a '## Response' body containing one `guard` bullet:
  {'accept': 1, 'accept_with_modification': 0, 'reject': 0, 'defer': 0, 'wontfix': 1}
```

The `guard` bullet vanishes with no error and no residual bucket. It is
**reachable**, not theoretical: row **B1** extends `doctrine/proposals.md:450-458`
— the *code-review-Response* grammar — with `guard`, and `_review_yield_counts`
parses exactly `## Response` sections (`subsystems.py:158`). After Chunk B the
doctrine instructs authors to write a token in the one place the tool reads, and
the tool discards it. Neither
`templates/modules/default-on/_lifecycle_metrics/subsystems.py` nor its
byte-identical twin `tools/_lifecycle_metrics/subsystems.py` (both blob
`f0ff9a4`) is among the fifteen.

**Satisfier** — either closes it: (i) add `guard` to `_DISPOSITION_BUCKETS` and a
`startswith('guard')` branch in **both** twins — a sixteenth and seventeenth
surface, and note this pair *is* covered by the twin-parity node, so it is cheap
and self-protecting; or (ii) state on the record that `guard` is an
**archive-time-only** token, forbid it in `## Response` bullets, and amend B1
accordingly — B1 as written does the opposite.

#### [P5] (important) — the chunk boundaries apply "moves together" to the pair that has a gate and split the three pairs that do not

Chunk E bundles the planner twins because they must move together — and that is
the pair with a **real** enforcer, which I mutation-tested. Meanwhile the plan
splits across Chunks C and D:

* `dev/modules/dual-review.md` ↔ `templates/modules/team-gated/dual-review.md` —
  **byte-identical**, blob `1812542` (`cmp` clean). Split across D4f and C4f.
* `dev/PLANNING.md:433-444` ↔ `templates/core/dev/PLANNING.md:97-108` —
  **prose-identical** (`diff` of the two ranges is empty). Split across D1f and C1f.
* the two `_template.md` pairs — near-identical prose. Split across C2f/C3f and
  D2f/D3f.

None of the three is covered by anything.
`bootstrap/tests/test_notice_install.py:51-64` (`_self_hosted_twins`) globs
`scripts/` and `tools/` and filters `src.endswith(".py")`, so a `.md` file under
`dev/modules/` is structurally outside its population. Confirmed by mutation —
inverting lens #9 in `dev/modules/dual-review.md` so it contradicts its
`templates/` source leaves `check_cairn` at **OK / no issues**,
`sync_doc_snippets --check` at **OK / no drift**, `quality_gate --sub neutrality`
with no new failure, and `pytest bootstrap/tests` at **1956 passed, zero
failures** (run at `4a7d70a`, where the concurrent session's Chunk D had added
six nodes to my 1950 baseline). Nothing anywhere notices.

So the plan concentrates its commit-boundary discipline on the pair that would be
caught anyway, and splits the three pairs where *a reviewer opening both files* is
the only enforcement invariant 3 has — into two different commits, which is where
that comparison is hardest to run.

**Satisfier** — merge Chunks C and D into one chunk (or at minimum one commit).
Each mirror pair then appears side-by-side in a single `git show`, and the
reviewer's diff *is* the enforcement. Costs nothing, adds no gate, and is the same
reasoning Chunk E already applies correctly.

#### [P6] (important) — the acceptance criteria cannot fail on a missed surface

The plan concedes the hole twice — *"The drift gates catch broken references,
**not** absence, so each of the fifteen is confirmed by opening it at code
review"* and *"the gates will not tell you a mirror was missed."* As written,
"done" is a reviewer's assertion with no falsifiable form, which is exactly the
condition under which the plan could be declared complete with a surface
unedited. Given [P2] (a rule with no row), [P3b] (a site with no citation) and
[P5] (three unguarded pairs), that is not theoretical.

**Satisfier** — make the changed-file set the criterion; it needs no code and no
new gate. `git diff --name-only <plan-open sha>..<final implementing sha>` must
equal the enumerated surface list plus `CHANGELOG.md` plus the successor
proposal's path. A reviewer compares two lists; a missed mirror shows as a missing
path. Falsifiable, mechanical, free.

#### [P7] (important) — a position on the no-new-test decision: sound for the prose, unsound for Chunk E

I agree with three quarters of the argument. For the fourteen prose surfaces the
reasoning is correct and I would resist a test: a node asserting a doctrine
sentence exists would pass while the rule it describes went unfollowed — the
degenerate-green case `AGENTS.md` > "Name the trigger, check what it checks"
warns about — and the content-parity guard that *would* matter is D2, which the
Decision declined. That is principle, not scope relief.

But the conclusion is reached through [P1]'s mis-scoping. *"A doctrine sentence
has no behavioral surface"* is true of A1–D4f and false of Chunk E once Chunk E is
correctly scoped, because it then edits a regex and a conditional branch in a
shipped module.

**The assertions I think are warranted**, in `bootstrap/tests/`, over
`lifecycle_planner._read_artifact` / `_conformance_violations`:

1. an archived artifact whose block is `Dispositions:` produces **no**
   archive-precondition violation;
2. an archived artifact whose block is the legacy `Follow-ups migrated to:` still
   produces none (the grandfathering [P1] requires);
3. an archived artifact carrying **neither** still produces one.

**What that catches which a reviewer would not.** The recognizer is
`^\s*Follow-ups migrated to\s*:` under `re.MULTILINE`, and this repo has an *open*
plan about precisely this line: `dev/plans/planner-line-semantics.md:908`
tabulates the contradiction inside `_read_artifact` where `splitlines()` sees the
block line and `re.MULTILINE '^'` does not. Hand-editing that pattern into an
alternation is exactly where an anchoring bug lands, and it fails silently in the
direction of (3) — a genuinely un-homed follow-up quietly stops being flagged.
Reading a regex does not catch an anchoring bug; running it does. Three
assertions, no new gate, no new surface: it pins behavior the plan is already
changing.

#### [P8] (important) — the in-flight cohort is an unlisted edge case

Seven live artifacts pre-declare that *their own* future archive will carry a
`Follow-ups migrated to:` block: `dev/plans/agent-context-scrub.md`,
`dev/plans/fork-advisory-semantics.md`, `dev/plans/planner-line-semantics.md`,
`dev/plans/release-security-bar.md`, and the proposals
`dev/proposals/2026-08-03-claude-dependency-advisory-coverage.md`,
`dev/proposals/2026-08-03-claude-gate-claims-vs-enforcement.md`,
`dev/proposals/2026-08-03-claude-release-security-bar.md`. None has archived.
After C1 each either archives against a form the doctrine no longer names, or
carries a stale self-declaration.

*Edge cases* covers zero-follow-ups, the proposal-archives-at-plan-open case, and
the solo profile — not this cohort, which is the largest and the only one that
exists today.

**Satisfier** — one sentence in A1 grandfathering the legacy spelling (the same
answer [P1] needs for the recognizer, so the two close together), plus one line in
*Edge cases* naming the cohort and stating that no in-flight artifact is edited by
this plan.

#### [P9] (nit) — F2's stated visibility mechanism is circular, and the Decision's binding is already discharged

The Decision binds: *"its stem is named in a commit body so its absence is visible
in `git log`."* Row F2 restates that as *"Its stem is named in the Chunk F commit
body"* — but if the successor is created in Chunk F, naming it in Chunk F's own
commit body carries no forward information. The real protection already exists:
`9052b09`'s body reads *"this plan OPENS its successor (stem
2026-08-04-claude-board-retro-disposition)"*, so the obligation is visible in
`git log` **today**, before Chunk F. The plan is safer than its own text claims.

**Satisfier** — cite `9052b09` in F2 rather than restating a self-satisfying
version.

#### [P10] (nit) — intra-file edit order will invalidate the plan's own citations

B1 (`doctrine/proposals.md:450-458`) and B2 (`:342-373`) are the same file, and B3
names three sites in `doctrine/plans.md` (four, after [P3b]). Editing low-to-high
shifts every later citation in that file.

**Satisfier** — one line in Chunk B: edit bottom-up within a file, or verify by
section heading rather than by line number.

---

### Suggested sharpening before implementation

1. **[P1]** Rewrite Chunk E's rows to name `:501`, `:630-631`, `:798-801`,
   `:1013`, `:1024-1025`, with the both-spellings rule stated; correct the three
   falsified author-accounting sentences; record why this does not escalate the
   tier.
2. **[P2]** Add row A5 (C3 + C5 + the D3 solo sentence in `doctrine/lifecycle.md`)
   and extend C1f/D1f to mirror it.
3. **[P3]** Fix D2f to `:281-293`, add `:602-611` to B3, nudge C3f.
4. **[P4]** Decide `guard`'s status in the metrics grammar and record it.
5. **[P5]** Merge Chunks C and D.
6. **[P6]** Add the changed-file-set acceptance criterion.
7. **[P7]** Add the three-assertion planner test to Chunk E, or record a reasoned
   refusal against those specific assertions.
8. **[P8]–[P10]** Prose.

### Covered

* **#1 Claims** — re-derived every load-bearing figure. **Confirmed**: `:878` is
  `gates.append((True,`; `test_notice_install.py:98` exists and compares bytes;
  both planner copies at blob `afa702d`; `grep` over `bootstrap/tests/` for
  `durable home` / `Follow-ups migrated` / `has_followups_migrated` returns
  **zero**; `scaffold.py --summary --config` exists with three profiles present;
  the successor stem is named in `9052b09`; suite **1950 passed** at `2ec7ca4`;
  lens #9 has exactly the three surfaces the plan names. **Refuted**: *"the only
  code edit is two message strings per planner copy"*, *"every failure in this
  plan is a prose defect, which fails open"*, and *"this plan adds no public code
  path"* ([P1]); `dev/plans/_template.md:261-269` ([P3a]); the completeness of
  `doctrine/plans.md`'s citation set ([P3b]).
* **#2 Production path exercised by tests** — mutation-tested the one named node:
  editing `tools/lifecycle_planner.py` alone **fails**
  `test_every_self_hosted_twin_stays_byte_identical_to_its_source`; restored, it
  passes. The node is real. But it pins *byte parity*, not *behavior* — it would
  pass on two identically-broken copies, which is what [P7] is about.
* **#3 Design completeness** — the token vocabulary is not total over its own
  mechanization ([P4]); the transition cohort is unenumerated ([P8]); C3, C5 and
  D3 have no home in the canonical file or the adopter templates ([P2]).
* **#4 Silent failure / fail-closed** — the plan claims uniform fail-open.
  Refuted twice: the rename makes `_conformance_violations` fail **closed against
  compliant artifacts** ([P1], reproduced), and `_normalize_disposition_token`
  fail **silently open** on `guard` ([P4], reproduced). The `.md` mirrors are
  genuinely unguarded ([P5], mutation-tested), which confirms invariant 3 ships
  fail-open exactly as the Decision intended.
* **#5 Cross-document consistency** — independent sweep across `doctrine/`,
  `templates/`, `dev/`, `bootstrap/`, `tools/`, `scripts/`, `.agents/`, `docs/`
  for `Follow-ups migrated`, `durable home`, `Name the satisfier`, `scope-cut`.
  **Fifteen is right on the lens-#9 axis** (`doctrine/dual-review.md:245`,
  `templates/modules/team-gated/dual-review.md:69`, `dev/modules/dual-review.md:69`
  — exactly the three named). It is **wrong on three others**: the planner is
  under-counted as a surface ([P1]), `doctrine/plans.md:605` is uncited ([P3b]),
  and the `_lifecycle_metrics` twins are absent ([P4]).
* **#6 Drift** — `sync_doc_snippets --check` clean and no snippet markers among
  the fifteen, so *"none generated, none snippet-synced"* holds. `check_cairn`
  clean at `2ec7ca4`; the 11 issues named in the plan-open body were repaired by
  that commit and are confirmed **not** this plan's.
* **#7 Lifecycle / process placement** — C5 names archive-preparation as the
  serialization point but homes it in a state-machine table cell ([P2]); the
  Decision's D1 binding is discharged ([P9]).
* **#8 Domain validity & scope** — the plan does **not** overstep: no chunk builds
  D2, none re-routes a board row, `AGENTS.md` is untouched. It **under**-delivers
  C3/C5 to the adopter surface ([P2]).
* **#9 Name the satisfier** — every finding above names one; none is a bare
  observation.

### Not covered / low confidence

* **Same-type reviewer.** I am Claude reviewing a Claude-authored plan in a fresh
  session — the Internal floor and nothing more. My findings are mechanical and
  reproducible, which is the class where same-type independence costs least; the
  design judgments (is `guard` the right token, is the approval gate at the right
  authority) were settled at proposal review and I did not re-open them.
* **I did not run the suite under the [P1] rename**, because the rename does not
  exist yet. I demonstrated the violation by driving `_read_artifact` /
  `_conformance_violations` directly on a synthetic archived artifact. Whether any
  *pytest node* would catch the doctrine/tool contradiction is settled by the
  zero-hit grep, not by a run.
* **The tree moved under me.** A concurrent session landed `4a7d70a` mid-review.
  My suite baseline and `check_cairn` figure are at `2ec7ca4`; nothing `4a7d70a`
  touched overlaps the fifteen, but the figures should be re-taken at
  implementation time rather than carried from here.
* **I took no position on whether `guard` should join `_DISPOSITION_BUCKETS` or be
  fenced to archive-time.** [P4] names both closes; the choice is the author's,
  and adding a bucket touches a `default-on` module twin, which may deserve its
  own sentence in the fence.
* **The D1 successor's content** is out of this plan's scope by the Decision and I
  reviewed it no further than confirming Chunk F opens the artifact and re-routes
  nothing.
* **`dev/PLANNING.md` has no board row for this plan.** Ten of the sixteen
  in-flight plans also have none, so this is prevailing board practice rather than
  a defect of this plan; recorded, not raised.
* **The two `issue-capture.md` copies** (`:97`, *"its closing comment names the
  durable home"*) I swept and cleared — on a different ground than the Response
  gave: that rule governs issue **promotion**, which by construction produces a
  durable home, so the new dispositions do not reach it. No edit needed.
* **`templates/modules/team-gated/issue-capture/reference/`'s two `labels.yml`
  files** carry *"Reviewed; durable home assigned."* Low consequence, arguably
  stale under the new rule; an observation, not a finding.

### Verdict

**REVISE.**

Not HOLD: the sequence has no cycle, the scope fence holds on both halves the
Decision fenced, and every finding closes with prose, a citation fix, a chunk
merge, or three assertions — none requires new machinery or re-opening the
design. Chunk A-first is right and Chunk E's instinct is right.

Not PROCEED, on **[P1]**, **[P2]** and **[P3]**, which are blockers in the
`(LOAD-BEARING)` sense — *plan-as-written will not achieve its acceptance
criteria*. [P1] means implementing the plan literally ships a doctrine that the
repo's own shipped tool reports as a violation. [P2] means the adopter templates
would not carry the Maintainer-approval gate at all — the change's central
mechanism, and part of what the Decision authorized. [P3] sends the implementer to
the wrong lines in one file and omits a canonical site in another, so *"all fifteen
surfaces"* is not reachable by following the tables.

[P4]–[P8] are important but a Sharpening can carry them without re-opening the
design; [P9]–[P10] are polish.

**Second round: not recommended as a separate pass.** The findings are mechanical
and each ships a reproducer the author can re-run; a Sharpening plus a re-read is
proportionate, and the Decision ratified Internal. One caveat the Maintainer
should see rather than infer: the Internal tier was ratified against a
characterization of Chunk E as *"two message strings"*, and [P1] falsifies it. I
do **not** think correcting an existing check's recognized vocabulary is *"adding
a mechanical gate"* under the proposal's escalation rule, so I do not think the
tier moves — but the Sharpening should state that reasoning explicitly rather than
let a tier ratified on a false premise stand silently.

## Code review

*Filled in after implementation commits land. Reviewer is not the implementing
agent.*

## Lasting-truth migration

*Filled in at archive time.*

---

## Response to the Internal plan review -- Claude (Strategy) -- 2026-08-04

**Model**: claude-opus-5

Ten findings, accepted in full. Two ([P1], [P2]) are load-bearing enough that the
Sequence is revised below rather than patched in place.

**[P1]** accept -- and it falsifies three sentences of this plan's own
author-accounting. Reproduced independently: `tools/lifecycle_planner.py:631` is
a **live conditional** --
`re.search(r"^\s*Follow-ups migrated to\s*:", text, re.MULTILINE)` -- feeding a
violation branch at `:798-801` that emits *"status is 'archived' but no
'Follow-ups migrated to:' block is present (archive precondition)"*. So the
string C1 renames is **load-bearing in shipped code**, not documentation. The
plan's claims that Chunk E touches "only two message strings", that "every
failure in this plan is a prose defect, which fails *open*", and that there is
"no public code path" are **all three false and are retracted**. There are
**five** bound sites per copy (`:631`, `:800`, `:880`, `:1013`, `:1025`), across
two copies.

The design decision this forces, which the plan never surfaced: **the recognizer
must accept both spellings.** Six archived artifacts satisfy the old form today
and are append-only; a rename that invalidates them would make the shipped
adopter-facing scan report historically-correct records as violations. Chunk E
becomes backward-compatible by construction -- `Follow-ups migrated to:` **or**
`Dispositions:` -- which is the only option that does not corrupt the existing
record.

**[P2]** accept -- the plan **under-delivers the Decision**, and it under-delivers
precisely the Maintainer's own contribution. C3 (`defer` needs a quoted
authorization) and C5 (archive-preparation as the serialization point) were
sequenced only into `doctrine/lifecycle-contract.md:137`, so the canonical
`doctrine/lifecycle.md` section and all four adopter templates would have shipped
the disposition **vocabulary without the backpressure** -- a strictly worse
artifact than today, because it makes declining easy and never introduces the
gate that was the point. C3 and C5 move into Chunk A (canonical) and Chunk C
(templates). D3 (the solo-profile statement) gains an explicit row rather than
living only in *Edge cases*.

**[P3]** accept -- all three verified and corrected. `dev/plans/_template.md`'s
archive-precondition prose is at **`:284-292`**, not `:261-269`; the wrong range
was copied from C2f without re-checking, and the two files differ in length (295
vs 272 lines). `doctrine/plans.md:602-609` carries one of the four canonical
statements of the block form and was cited by **no** row. The
`templates/core/dev/proposals/_template.md` citation is off by one. This is the
third citation defect in this artifact's history and the second caused by
carrying a range across files.

**[P4]** accept -- verified: `_DISPOSITION_BUCKETS` at
`templates/modules/default-on/_lifecycle_metrics/subsystems.py:88-94` is a
five-token tuple with no `guard`, and `_normalize_disposition_token` returns `''`
for an unrecognized token, which the caller drops. So the new token would be
**silently invisible** to the metrics report -- the exact silent-drop hazard the
proposal's Response cited [I2] to avoid, reappearing because the token is new.
`guard` is added to the bucket tuple, and the `_lifecycle_metrics` twin pair
joins the surface set.

**[P5]** accept -- Chunk E bundled the one *guarded* twin pair while Chunks C and
D split the three *unguarded* mirror pairs, which is backwards: the pairs a test
protects can safely ride together, the ones nothing protects are where a split
review earns its keep. Re-split below.

**[P6]** accept -- acceptance criteria were not falsifiable. Added: the changed-
file set of the implementing commits must equal the surface set named in the
Sequence, verified by `git diff --stat` against the list, so "done while a
surface went unedited" is detectable rather than assertable.

**[P7]** accept, and the reviewer is right that the no-new-test justification was
sound for the prose and **unsound for Chunk E**. It is not scope relief in the
prose chunks -- a doctrine sentence genuinely has no behavioral surface -- but
[P1] establishes that Chunk E has one. Three assertions are added, named in the
revised Chunk E.

**[P8]** accept -- seven in-flight artifacts pre-declare the old block form.
Backward compatibility ([P1]) covers them with no edit, which is why it is the
right design rather than merely the compatible one.

**[P9], [P10]** accept -- folded into the revision.

**Second round** not run, per the reviewer's own recommendation that a separate
pass is not warranted. Every finding's satisfier is a scope correction or a named
assertion; none re-opens the design.

## Sequence revision 2026-08-04

Supersedes the original Sequence. Surface count corrected from **fifteen to
nineteen**: the planner pair carries five bound sites each (not two), and the
`_lifecycle_metrics` twin pair joins.

```
1. Chunk A  -- doctrine/lifecycle.md: C1, C2, C4 AND C3 + C5        [pending]
2. Chunk B  -- the four sibling doctrine files (+ plans.md:602-609) [pending]
3. Chunk C  -- the four adopter templates, incl. C3/C5 backpressure [pending]
4. Chunk D  -- the four self-hosted mirrors                         [pending]
5. Chunk E' -- the planner twins: 5 sites x 2 copies, BOTH spellings
               accepted, + 3 new assertions                          [pending]
6. Chunk E''-- the _lifecycle_metrics twins: `guard` bucket          [pending]
7. Chunk F  -- CHANGELOG + open the D1 successor                     [pending]
```

### Chunk A (revised) — the canonical rule, with the gate

| # | File | Change |
|---|------|--------|
| A1 | `doctrine/lifecycle.md` > "Archive precondition" | **C1** — satisfied by a recorded disposition token; `Follow-ups migrated to:` **or** `Dispositions:` accepted |
| A2 | same | **C2** — define `guard`; the entry names the node (`path::node`); comments explicitly ineligible |
| A3 | same | **C4** — the two eligibility rules; no required ordering |
| A4 | same | **C3 + C5** *(moved here per [P2])* — `defer` requires a quoted Maintainer authorization; archive-preparation is the serialization point |
| A5 | same | **D3** *(new row per [P2])* — on a solo profile the gate is a written self-justification: weaker, not vacuous |
| A6 | same | All three invariants are documentary; enforcer is a reviewer opening both files |

### Chunk B (revised)

| # | File | Change |
|---|------|--------|
| B1 | `doctrine/proposals.md:450-458` | Add `guard` to the grammar; note it governs archive-time dispositions |
| B2 | `doctrine/proposals.md:342-373` | C1 by pointer; both block spellings |
| B3 | `doctrine/plans.md:492`, `:543`, `:586` | Token addition + archive precondition pointer |
| B4 | `doctrine/plans.md:602-609` *(new row per [P3])* | The canonical block-form example gains the `Dispositions:` spelling |
| B5 | `doctrine/dual-review.md:245-247` | **C6** — lens #9's total mapping |
| B6 | `doctrine/lifecycle-contract.md:137` | C3 + C5 in the `review → archived` row (now a restatement, not the sole home) |

### Chunk C (revised) — adopter templates

| # | File | Change |
|---|------|--------|
| C1f | `templates/core/dev/PLANNING.md:97-108` | Mirror A1–A6 **including the C3/C5 gate** |
| C2f | `templates/core/dev/plans/_template.md:261-269` | Archive precondition wording |
| C3f | `templates/core/dev/proposals/_template.md:88-90` *(corrected)* | Archive precondition wording |
| C4f | `templates/modules/team-gated/dual-review.md:69` | Mirror B5 |

### Chunk D (revised) — self-hosted mirrors

| # | File | Change |
|---|------|--------|
| D1f | `dev/PLANNING.md:433-444` | Mirror A1–A6 (prose only) |
| D2f | `dev/plans/_template.md:284-292` *(corrected per [P3])* | Mirror C2f |
| D3f | `dev/proposals/_template.md:103-108` | Mirror C3f |
| D4f | `dev/modules/dual-review.md:69` | Mirror C4f |

### Chunk E′ (revised) — the planner twins, backward-compatible

| # | File | Change |
|---|------|--------|
| E1 | `templates/skills/_lib/lifecycle_planner.py` `:631`, `:800`, `:880`, `:1013`, `:1025` | Recognizer accepts **both** spellings; violation text and scaffold strings name both. Gates stay unconditional |
| E2 | `tools/lifecycle_planner.py` (same five sites) | Byte-identical twin — same edit, same commit |
| E3 | `bootstrap/tests/test_lifecycle_cli.py` | **Three assertions** *(per [P7])*: (1) an archived artifact with only `Dispositions:` is **not** flagged; (2) one with only `Follow-ups migrated to:` is still **not** flagged (the six archived records); (3) one with **neither** **is** flagged |

### Chunk E″ — the metrics twins

| # | File | Change |
|---|------|--------|
| E4 | `templates/modules/default-on/_lifecycle_metrics/subsystems.py:88-94` | Add `guard` to `_DISPOSITION_BUCKETS` |
| E5 | `tools/_lifecycle_metrics/subsystems.py` | Twin — same edit, same commit |

### Acceptance criteria — addition per [P6]

The changed-file set of the implementing commits must **equal** the nineteen
surfaces named above, verified by `git diff --stat <plan-open>..<last-impl>`
against the list. A surface silently skipped is then detectable rather than
assertable.

### Author-accounting — corrections

* **Retracted:** "only two message strings", "every failure fails open", "no
  public code path". Chunk E′ has a behavioral surface, is guarded by three new
  assertions, and fails **closed** on a one-sided twin edit.
* **Retained:** the prose chunks (A–D) genuinely have no behavioral surface and
  add no test. That was sound and is unchanged.
