# Plan: deferral discipline — the archive precondition routes, not only preserves

**Source proposal**: [`dev/proposals/archive/2026-08-04-claude-deferral-discipline.md`](../proposals/archive/2026-08-04-claude-deferral-discipline.md)
**Status**: archived
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

### Code review -- Claude (fresh session) -- 2026-08-04

**Model**: claude-opus-5
**Reviewed at**: `411b9a0`; implementing range `3f8ce57..791655a` (seven chunks)
**Interpreter for every figure below**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13), the canonical interpreter

Not the implementing agent (`doctrine/plans.md` > "Code review" floor). Fresh
session, no inherited context. The design was settled at proposal review and the
execution spec at plan review; this pass asks *does the landed code do what the
Decision authorized, and which test fails when I delete it*.

**Every figure below was re-derived by running something.** Nothing was accepted
on the implementing agent's assertion, including the assertions it made against
its own interest.

#### Claimed verification -- reproduced

| Claim (commit `411b9a0`) | Re-run | Verdict |
|---|---|---|
| full suite **1959 passed**, 253s | `1959 passed, 3 warnings in 238.36s` | **reproduced** |
| `check_cairn.py` OK across **191** files | `OK -- 192 Markdown file(s) scanned; no issues` | reproduced, **figure off by one** -- `791655a` itself added the 192nd file (the successor proposal), so the claim was measured before the commit that carries it. Cosmetic; recorded, not raised |
| both twin pairs byte-identical by `cmp` | `cmp` clean on both; `git ls-files -s` puts the planner pair at blob `0084ce7` and the metrics pair at `2bf3ac7` | **reproduced** |

Additionally run, none of which the plan's *Verification* section can be declared
satisfied without: `quality_gate.py --sub neutrality` -> `fail=95 info=21`, **all
pre-existing** (I intersected the FAIL set against the 20 changed paths: only
`doctrine/dual-review.md:57`, `doctrine/lifecycle-contract.md:69` and `:87`,
`templates/skills/_lib/lifecycle_planner.py:186` and `:505` appear, and none is
inside a diff hunk -- **zero new neutrality failures**); `bootstrap/scaffold.py
--summary --config` on **all three** profiles (`collaborative-team`,
`high-rigor-legacy`, `solo-greenfield`) -> all reach the confirmation prompt, so
the Chunk-C templates still install.

#### [P1] -- the load-bearing plan-review finding -- discharged, verified against the real tree

The plan review's central finding was that a hard rename would make the shipped
adopter-facing `scan` report already-archived artifacts as violating the archive
precondition. **Verified backward-compatible by execution on the live corpus**,
not by reading the regex:

```
new planner (HEAD):       35 of 70 artifact(s) carry structural violations
                           9 lines matching "archive precondition"
old planner (3f8ce57~1):  35 of 70 artifact(s) carry structural violations
                           9 lines matching "archive precondition"
diff of the two outputs, modulo the message re-word:  IDENTICAL
```

Seventeen archived artifacts under `dev/plans/archive/` and
`dev/proposals/archive/` carry the legacy `Follow-ups migrated to:` spelling. Not
one changes disposition. The nine artifacts that *do* still flag
(`adopter-entry-doc-refresh`, `byline-classification`, `gate-claims-vs-enforcement`,
`gate-reanchor-preflight`, `interpreter-trust-root-fallback`,
`lockfile-provenance-fields`, `profile-parse-fail-open`, `release-authenticity`,
`scan-coverage`) flag **identically before and after** -- e.g.
`dev/plans/archive/adopter-entry-doc-refresh.md:173` writes the block as
`**Follow-ups migrated to:**` inside a sentence, which `^\s*...\s*:` has never
matched. That is the pre-existing recognizer narrowness
`dev/plans/planner-line-semantics.md:908` already tabulates, not a regression
here. **The new `Dispositions:` spelling inherits exactly the same narrowness**,
which is worth stating plainly now that the doctrine tells adopters to write it.

I also checked the widened recognizer for a **new false-positive** class: an
in-flight artifact that merely *quotes* the block form at line start would now
satisfy the precondition without dispositioning anything. Swept `dev/plans/`,
`dev/plans/archive/`, `dev/proposals/`, `dev/proposals/archive/` for
`^\s*Dispositions\s*:` -- **zero matches**. `_template.md` and `README.md` are
excluded from `scan` (`tools/lifecycle_planner.py:1143`), so the templates cannot
false-positive either.

#### Mutation testing -- the three new assertions are non-vacuous, and each pins a different thing

Reproduced independently, including the implementing agent's account of its own
**wrong first attempt**. `bootstrap/tests/test_lifecycle_contract.py:43-44` loads
the `templates/skills/_lib/` copy, so mutating `tools/lifecycle_planner.py` cannot
reach these nodes.

| Mutation of `templates/skills/_lib/lifecycle_planner.py:632` | Result |
|---|---|
| `(?:Follow-ups migrated to)` -- legacy-only, i.e. **the pre-change state** | `test_archived_plan_with_dispositions_block_is_not_flagged` **FAILED**, other two pass |
| `(?:Dispositions)` -- new-only, i.e. **the [P1] hazard** | `test_archived_plan_with_legacy_followups_block_is_not_flagged` **FAILED**, other two pass |
| `r""` -- matches everything | `test_archived_plan_with_neither_block_is_flagged` **FAILED**, other two pass |
| restored | **3 passed**, `git status` clean |

Three mutations, three distinct single-node failures: the assertions are
**orthogonal**, not three spellings of one check. The second row is the one that
matters -- it is the only mechanical guard in the tree keeping the six append-only
archived records valid, and it fails when removed.

Separately, mutating `tools/lifecycle_planner.py` alone: the three nodes **still
pass** (confirming the implementing agent's self-correction), and
`bootstrap/tests/test_notice_install.py`
`::test_every_self_hosted_twin_stays_byte_identical_to_its_source`
**FAILS** with `twin parity broken`. I ran the same one-sided mutation on
`tools/_lifecycle_metrics/subsystems.py` (`'guard'` -> `'guardX'`): the same node
**FAILS**. **Both** twin pairs are genuinely guarded, verified by deletion rather
than by reading the glob.

#### Decision fidelity -- neither overstepped nor under-delivered

* **D2 (content-parity gate) was NOT authorized and was NOT built.** No new
  script, no new gate, no checker anywhere in the 20 changed paths. The only test
  addition is the three recognizer assertions, which pin the planner's own
  behaviour, not doctrine/template prose parity. Invariant 3 ships fail-open
  exactly as the Decision directed.
* **D1 (the 59-row retro pass) was split, and no board row moved.** Falsifiable
  form: `git show 4858c84 -- dev/PLANNING.md` is a **single hunk**,
  `@@ -433,15 +433,50 @@` -- 15 prose lines replaced by 50. The file goes 1002 ->
  1037 lines, and 1002 + 35 = 1037 **exactly**, so no row was added, removed or
  re-routed anywhere else in the file. `### Deferred follow-ups (durable home)`
  is still 430 lines. The successor opened:
  `dev/proposals/2026-08-04-claude-board-retro-disposition.md`, status `proposed`,
  carrying [I8]'s two rules and explicitly committing to **no** routing estimate.
* **[P2]'s under-delivery is closed.** The C3/C5 backpressure reached the
  canonical file *and* all four adopter templates -- `templates/core/dev/PLANNING.md`
  carries *"Requires the Maintainer's authorization, quoted verbatim"*, the
  solo-profile sentence, and archive-preparation as the serialization point; both
  `_template.md` mirrors carry *"(with the Maintainer's quoted authorization)
  `defer`"*.
* **The planner gates stayed unconditional.** `tools/lifecycle_planner.py:883` is
  still `gates.append((True,`. Proposal item 7's refusal is honoured; nothing was
  promoted to a check, so the External-escalation rule is not fired.
* **`AGENTS.md` untouched.** Confirmed against the changed-path set.

#### Mirror parity -- invariant 3's documentary enforcer, actually run

Invariant 3 ships with *"a reviewer opening both files"* as its only enforcer. I
am that reviewer, so here is the falsifiable form rather than an assertion.
`diff` of the changed section in each pair:

```
templates/core/dev/PLANNING.md              <-> dev/PLANNING.md             : EMPTY
templates/core/dev/plans/_template.md       <-> dev/plans/_template.md      : EMPTY
templates/core/dev/proposals/_template.md   <-> dev/proposals/_template.md  : EMPTY
templates/modules/team-gated/dual-review.md <-> dev/modules/dual-review.md  : 1 line
```

The one divergence is the `cairn-internal-ref-allow` header added to the
`templates/` copy only. **It is correct**: that copy now cites
`doctrine/lifecycle.md`, which does not resolve in an adopter tree, while
`dev/modules/` is excluded from link-checking by default
(`bootstrap/tests/test_link_check_exclusions.py:5`). It does, however, break a
previously byte-identical pair (blob `1812542`) that nothing guards -- see [C7].

---

### Findings

#### [C1] (important) -- the [P6] acceptance criterion is unrunnable as written, and no commit records running it

[P6] existed because the plan conceded that *"the gates will not tell you a mirror
was missed"*, and its satisfier was a two-list comparison: *"the changed-file set
of the implementing commits must **equal** the nineteen surfaces named above,
verified by `git diff --stat <plan-open>..<last-impl>` against the list."* Run
literally, it does not work:

```
git diff --name-only 3f8ce57~1..791655a   ->  23 paths
```

Three of the 23 belong to **other sessions** -- `dev/plans/separator-detection.md`
(`a832569`), `dev/plans/dependency-advisory-coverage.md` (`c11a7c4`),
`docs/tool-usage.md` (`02d557b`) -- all interleaved inside the range. A range diff
is unsound in a repo whose own git rules assume concurrent agents. The
**per-commit union** is the correct instrument and gives **20** paths, which I
enumerated and checked one by one. Two further problems: the prose says *nineteen*
while the revised chunk tables enumerate **twenty** file paths, and no list of
nineteen is written down anywhere, so the two-list comparison has no second list.
Nothing in any of the seven commit bodies records the criterion having been run.

The good news is that it *passes* when run correctly -- I did it, and the
per-commit union equals the tables exactly. The finding is that the plan's own
completeness guard did not fire and could not have.

**Satisfier** -- record the enumerated 20-path per-commit union in this section
(done below, in *Covered* #6), and correct the criterion's instrument from a
range diff to `git show --stat` over each implementing sha, so a later plan
copying this criterion does not inherit the range-contamination bug.

#### [C2] (important) -- the plan's E3 row names a test file that was not the one edited

Chunk E' row **E3** names `bootstrap/tests/test_lifecycle_cli.py`. The three
assertions landed in `bootstrap/tests/test_lifecycle_contract.py:563-587`. **Both
files exist**, so a reviewer following the table opens a real file, finds no
assertions, and has no signal that they are in the wrong place -- the worst shape
for a citation defect.

The relocation itself is **right**, and I would not want it undone:
`test_lifecycle_contract.py` is the module that loads the planner (`:43-44`) and
owns the `scan`-conformance tests, and its docstring already explains why
unmarked additions there are gate-manifest-safe (COLLECTION-ADDED-only). But no
commit body records the move, so the record says one thing and the tree another.
This is the **fourth** citation defect in this artifact's history; the plan review
found three and named the mechanism each time ("a figure carried rather than
re-derived").

**Satisfier** -- an append-only correction naming
`bootstrap/tests/test_lifecycle_contract.py`
`::test_archived_plan_with_dispositions_block_is_not_flagged`
and its two siblings as the landed nodes. Cited here, which discharges it for a
cold reader; the plan's own table stays as written, per append-only.

#### [C3] (important) -- Chunk E''s commit body claims a reader-visible number that does not exist

`8d6ae88`'s body says the change *"makes the decline rate measurable for free ...
bucketing `guard` is what lets a future reader see the (guard / wontfix / defer)
split as a number rather than an impression."* Measured, not read:

```
_DISPOSITION_BUCKETS -> ('accept','accept_with_modification','reject','defer','wontfix','guard')
_review_yield_counts -> {'accept':1,'accept_with_modification':0,'reject':0,
                         'defer':0,'wontfix':1,'guard':1}     # guard survives parsing
tools/lifecycle_metrics.py proposals --format csv | head -1
  -> review_yield_accept_count, review_yield_accept_with_modification_count,
     review_yield_reject_count, review_yield_defer_count          # four columns
tools/lifecycle_metrics.py --manifest
  -> snapshot schema carries the same four; no guard, no wontfix
```

`tools/_lifecycle_metrics/extract.py:74-77` emits four `review_yield_*` columns
and `snapshot.py:114-116` maps three. **`guard` is bucketed and then never
emitted** -- the same status `wontfix` has had all along, which the module's own
comment states (*"is not surfaced as a proposal-row column"*). So the code change
is correct and does close [P4]'s hazard (the token no longer vanishes *inside the
parser*), but the (guard / wontfix / defer) split is **not visible to any reader
anywhere**, and the durable record claims it is. In a repo where commit bodies
*are* the audit trail, an overclaim there is the defect, not a rounding error.

**Satisfier** -- two closes, and the record should say which. (i) Correct the
claim here: the bucketing is parse-level lossless-ness only, no column is emitted,
and the split stays unmeasurable until one exists. (ii) Emit
`review_yield_guard_count` / `_wontfix_count` -- but that mutates the snapshot CSV
schema, which `AGENTS.md` > "High-risk surfaces" treats as a **byte-level-stable
install contract**, so it is proposal-worthy and correctly outside this plan. I
take (i) here and name (ii) as the successor's option, not this plan's debt.

#### [C4] (important) -- `doctrine/proposals.md` now names two different canonical homes for the same rule

Chunk B added, at `doctrine/proposals.md:348-351`:

> See `doctrine/lifecycle.md` > "Archive precondition" for the vocabulary, the two
> `wontfix` eligibility rules, and why a disposition is not the same thing as a
> durable home.

Thirty lines later, unedited and pre-existing, `:379-382` still says:

> The same rule applies to plan files in `dev/plans/` when they archive; the
> canonical statement lives at `dev/PLANNING.md > Archive preconditions (proposals
> and plans)`.

One section, two canonical pointers, and the plan's own routing statement settles
which is right: *"its canonical home is `doctrine/lifecycle.md` with the siblings
pointing at it."* The second is now stale twice over, because `dev/PLANNING.md`'s
section -- rewritten by Chunk D -- itself now says *"full rule, including why, in
`doctrine/lifecycle.md`"*. A reader following it takes a two-hop redirect back to
where the first pointer already sent them. It resolves, so `check_cairn` is silent:
this is precisely the class of defect the plan documented as fail-open.

**Satisfier** -- a one-line sharpening edit re-pointing `:379-382` at
`doctrine/lifecycle.md`, before archive.

#### [C5] (important) -- the canonical vocabulary says "the grammar, extended with one token" and then silently drops `reject`

`doctrine/lifecycle.md:425-428`: *"Use the disposition grammar already defined in
`proposals.md` > 'Response -- disposition grammars', **extended with one token**
for the archive-time case."* The grammar it points at
(`doctrine/proposals.md:462-470`) is `accept` / `guard` / `reject` / `defer` /
`wontfix`. The list that follows enumerates `accept`, `guard`, `wontfix`, `defer`,
`defer (successor)` -- **`reject` is absent, and its absence is never stated.**
Every sibling restatement enumerates exactly four (*"`accept`, `guard`, `wontfix`,
or (with the Maintainer's quoted authorization) `defer`"*: `doctrine/plans.md:589-591`,
`doctrine/proposals.md:346-348`, both `_template.md` mirrors,
`doctrine/lifecycle-contract.md:137`, both `PLANNING.md` mirrors).

So the framing sentence and the list it introduces disagree about whether `reject`
is available at archive time. An author who follows the sentence writes a token no
sibling list recognizes -- and `_normalize_disposition_token` accepts it (verified:
`'reject' -> 'reject'`), so nothing anywhere objects. Fails open, in the one
section that is supposed to be the single source.

**Satisfier** -- one clause in `doctrine/lifecycle.md`: `reject` is a
review-Response token with no archive-time meaning (a follow-up is not *rejected*,
it is `wontfix` with a rationale), so the archive-time vocabulary is the grammar
**minus `reject`, plus `guard`**. State the subtraction rather than leaving it to
inference.

#### [C6] (nit, but three surfaces) -- the plan-triage rule still states the superseded precondition

`doctrine/plans.md:147` and `:154` are unchanged:

> * Carries deferred follow-ups that need **durable homes** before archiving.
> * No follow-ups **need a durable home** (the proposal's "what's next" is fully
>   captured in the implementing commit message).

mirrored verbatim at `templates/core/dev/plans/_template.md:53` and
`dev/plans/_template.md:53` (*"with no follow-ups needing a durable home"*). After
C1 only `defer` needs a durable home, so the trigger for opening a plan is now
**narrower than the rule it derives from**: an accepted proposal whose follow-ups
are all headed for `guard` or `wontfix` reads as *skip the plan*.

These three are not covered by the scope fence, which excludes only *other agents'
in-flight plan files under `dev/plans/`*. I judge that fence **correct** and would
not widen it -- I swept the ~15 in-flight plans and every hit is boilerplate inside
another agent's live artifact, where an edit by this plan would be exactly the
cross-session write the git rules exist to prevent, and backward compatibility
([P1]) means none of them is broken by waiting. But `doctrine/plans.md` is not an
in-flight artifact; it is the canonical doctrine file for plans, and this plan
edited it four sections lower.

**Satisfier** -- re-word the two triage bullets to "follow-ups needing
dispositions" in the three files, in a sharpening commit before archive.

#### [C7] (nit) -- [P5] was marked `accept` in the Response and then not done

The Response says *"**[P5]** accept -- ... Re-split below."* [P5]'s satisfier was
explicit: *"merge Chunks C and D into one chunk (or at minimum one commit)"*, so
that each unguarded mirror pair appears side-by-side in a single `git show` and
the reviewer's diff *is* invariant 3's enforcement. The revised Sequence keeps
Chunk C (`758448a`) and Chunk D (`4858c84`) as **separate commits**; all four
mirror pairs are still split. The "re-split" that was delivered is Chunk E ->
E'/E'', a different thing entirely.

The predicted consequence then occurred, benignly:
`templates/modules/team-gated/dual-review.md` gained a `cairn-internal-ref-allow`
header in `758448a` that `dev/modules/dual-review.md` did not get in `4858c84`,
breaking a formerly byte-identical pair. I verified the divergence is **correct**
and I verified all four pairs are otherwise content-identical -- but I did that by
hand, afterwards, which is precisely the position [P5] wanted to avoid.

Under this plan's own new doctrine, a finding marked `accept` whose satisfier was
not landed and not re-dispositioned is the silent-drop shape the change exists to
prevent. Worth naming for that reason more than for its consequence.

**Satisfier** -- the mirror-parity verification is recorded above with its
commands, which discharges the enforcement gap for this plan. For the record
defect: re-dispose [P5] honestly at archive time (`wontfix` -- the split cost
nothing here and parity was verified out-of-band) rather than letting `accept`
stand.

#### [C8] (nit) -- the CHANGELOG leads with the evidence line the accepted proposal withdrew

`CHANGELOG.md > Unreleased > Changed` motivates the change with *"Cairn's own
board grew 349 -> 1002 lines in thirteen days."* The Revised proposal states,
under *Corrected figures*: **"Dropped as independent evidence: the thirteen-day
line-growth trend."**

The numbers are right -- I re-derived them: `git show 57d1daf:dev/PLANNING.md |
wc -l` = **349**, `git show 4573c11:dev/PLANNING.md | wc -l` = **1002**,
2026-07-22 -> 2026-08-04 = **13 days**. The problem is the role they are given.
The rate-limit gate was cleared on the **six-plan census** (28 net new board rows
across 6 independently-authored plans), and the trend was demoted precisely
because it is not independent evidence. The contributor-visible record now names
the demoted line as the reason.

**Satisfier** -- swap the sentence for the census figure, or keep it and mark it
as illustration rather than evidence. One line either way; the point is that the
public record should not out-claim the deliberation behind it.

#### [C9] (nit) -- lens #9's mapping is total, but its range has no `defer`, so following it literally never triggers the gate this change installs

`doctrine/dual-review.md:245-252` (and both mirrors) now read: *"each satisfier
maps onto a disposition token ... and the mapping is total: test -> `guard`, guard
-> `guard`, doc -> `accept`, scope-cut -> `accept`, wontfix -> `wontfix`. Naming
the satisfier and naming who pays for it are then the same act."*

**Totality holds** -- I checked all five satisfiers against the five listed and
every one maps. C6 is delivered as specified. But the *range* is
{`guard`, `accept`, `wontfix`} -- **`defer` is unreachable**. A reviewer taking
the last sentence at face value ("naming the satisfier ... is the same act" as
naming the disposition) would never emit a `defer`, and so would never reach the
Maintainer gate that is the change's entire backpressure mechanism.

The resolution is real but unstated: lens #9 names what *would close* a finding,
while the disposition names what was *actually done* -- a deferred finding still
has a satisfier, it is just not paid yet. That is a sound distinction and the last
sentence elides it.

**Satisfier** -- one clause: the satisfier names what closes the finding; `defer`
is the disposition when that satisfier is *scheduled rather than landed*, and it
carries the Maintainer's quote. Three surfaces (`doctrine/dual-review.md`,
`templates/modules/team-gated/dual-review.md`, `dev/modules/dual-review.md`),
which must move together.

---

### Falsification ledger

**Surfaces probed.** The recognizer regex and its four sibling sites in both
planner copies; the three new assertions; both twin-parity populations; the
`_normalize_disposition_token` branch ordering and every downstream consumer of
`_DISPOSITION_BUCKETS` (`extract.py`, `snapshot.py`, the `--manifest` schema, the
emitted CSV header); the four doctrine/template/self-host mirror pairs by `diff`;
the whole `doctrine/lifecycle.md` > "Archive precondition" section read as a unit
against its five siblings; `dev/PLANNING.md`'s board for row movement; the D1
successor; the CHANGELOG entry's figures; the frozen-file and gate-manifest status
of the modified test; the neutrality gate intersected against the changed set; the
scaffold emitter driven end-to-end in a throwaway git repo.

**Negative / edge-case attempts** -- what I tried to break, and what happened:

1. **Six mutations, each restored and re-verified.** Three on the recognizer
   (legacy-only / new-only / match-all) -> three *different* single-node failures.
   One on `tools/lifecycle_planner.py` alone -> the three nodes still pass, twin
   parity **fails**. One on `tools/_lifecycle_metrics/subsystems.py` alone -> twin
   parity **fails**. Restored state re-verified green each time; `git status`
   clean at the end.
2. **Old planner vs new planner on the real 70-artifact corpus.** Byte-identical
   output modulo the message re-word. This is the [P1] falsification and it is the
   strongest single piece of evidence in this review.
3. **False-positive hunt on the widened recognizer.** Swept all four corpus
   directories for `^\s*Dispositions\s*:` -> zero. Confirmed `_template.md` is
   excluded from `scan` (`:1143`), so templates cannot false-positive.
4. **Branch-shadowing probe on `_normalize_disposition_token`.** `'guard'`,
   ``'Guard (`a::b`)'``, `'guard (tests/x.py::test_y)'` -> `'guard'`;
   `'guardian angel'` -> `'guard'`; `'flibbertigibbet'` -> `''`. The `guard`
   branch sits after `wontfix` and no token is a prefix of another, so **no
   shadowing**. The loose-prefix behaviour matches what `'deferred' -> 'defer'`
   and `'rejects' -> 'reject'` already did -- consistent, not a new defect.
   **A sixth tuple element breaks nothing downstream**: no consumer iterates the
   buckets to build columns; `extract.py` indexes four keys by name.
5. **Degenerate-green probe on the scaffold.** Driving `next --to archived` emits
   `Dispositions:` at line start with `<item>` placeholders, so pasting the
   scaffold unedited satisfies the recognizer. **Pre-existing** (the old scaffold
   did the same with `Follow-ups migrated to:`) and now **explicitly documented**
   -- `doctrine/lifecycle.md:497-505` says a checker *"could not distinguish a
   considered decline from a template-shaped one, and a gate that passes the
   degenerate case is worse than no gate because it is silent."* Probed, found,
   already named by the doctrine. Not a finding.
6. **Frozen-file claim, probed rather than accepted.** `6ece062`'s body asserts
   `test_lifecycle_contract.py` *"was ALREADY FROZEN-MODIFIED before this
   change."* It is a key in the 164-entry `frozen_files` map; pinned sha256
   `318e869d...`; actual at `6ece062~1` `3d263dc1...` -> **already mismatched
   before the change. The claim is true.** The three new node IDs are absent from
   `gate_manifest.json`, which is what the module docstring says unmarked
   additions should be; `test_gate_preflight.py` 127 passed.
7. **Scope-fence probe.** Independently swept `doctrine/`, `templates/`, `dev/`,
   `bootstrap/`, `tools/`, `scripts/`, `.agents/`, `docs/` and the root `*.md` for
   `Follow-ups migrated` and `durable home`. Residue outside the fence: [C6]'s
   three triage surfaces. The two `issue-capture` copies and the two `labels.yml`
   files I cleared on the plan review's ground (issue *promotion* produces a home
   by construction). CHANGELOG's historical entries are append-only record.
   `.agents/skills/` and `templates/skills/` carry nothing but the planner itself.

**Verification run.** Everything in the *Claimed verification* table above, plus:
`quality_gate.py --sub neutrality` (intersected against the changed set);
`scaffold.py --summary --config` on all three profiles;
`tools/lifecycle_planner.py scan --include-archive` on old and new planners;
`tools/lifecycle_metrics.py proposals --format csv` and `--manifest`;
`test_gate_preflight.py`; `claim_check.py` on this file.
**Consciously not run**: `sync_doc_snippets.py --check`, on the plan review's
finding that no file among the surfaces carries a snippet marker and the *"none
generated, none snippet-synced"* claim already held -- and nothing in the landed
diff introduces a marker (I grepped the 20 changed paths). I also did not install
a scaffolded tree and diff it against the templates; `--summary` reaching the
prompt on all three profiles is the plan's stated smoke bar and I held it to that
rather than inventing a higher one.

**Residual risk.**
* **Invariant 3 is fail-open by Decision, and my `diff` is the only enforcement
  this plan will ever get.** It is recorded above so it is falsifiable, but it
  expires the moment either side is edited. D2 remains the real close and remains
  unauthorized.
* **Same-type reviewer.** I am Claude reviewing Claude-authored work in a fresh
  session. My findings are mechanical and each ships a reproducer; the design
  judgments (is `guard` the right token, is the gate at the right authority) were
  settled at proposal review and I did not re-open them.
* **The nine pre-existing `archive precondition` violations** are unchanged by
  this plan but are now *more* load-bearing, because the doctrine tells adopters
  to write a block the recognizer only matches at line start with no bold or prose
  prefix. `dev/plans/planner-line-semantics.md` owns that; I did not touch it.
* **`guard`'s usefulness is untested end-to-end.** No artifact in the corpus has
  yet archived under a `Dispositions:` block, so the grammar has never been run in
  anger. The first real one is the D1 successor.
* **I did not verify the adopter-installed tree.** The templates are checked as
  source, not as merged output; whether the `cairn-internal-ref-allow` comment
  rides into an adopter's `dev/agent_collaboration.md` on module merge is
  unexamined.

### Covered

* **#1 Claims** -- every load-bearing figure re-derived. **Confirmed**: suite
  **1959 passed**; twin pairs at blobs `0084ce7` / `2bf3ac7`, `cmp` clean; `scan`
  output identical old-vs-new on 70 real artifacts; `gates.append((True,` still at
  `:883`; `dev/PLANNING.md` 1002 + 35 = 1037 with a single hunk; the 349 / 1002 /
  13-day figures accurate; the frozen-file claim in `6ece062` **true**; the
  wrong-first-mutation account **true**. **Refuted**: `check_cairn` 191 -> **192**;
  *"lets a future reader see the split as a number"* ([C3]); the [P6] criterion's
  runnability ([C1]); row E3's file ([C2]).
* **#2 Production path exercised by tests** -- the three assertions call
  `planner.main(["scan"])`, the **public CLI entry**, not a helper
  (`test_lifecycle_contract.py:558-561`), over a real on-disk artifact in a real
  git repo. Mutation-proven non-vacuous, three-for-three, each pinning a distinct
  behaviour. Twin parity mutation-proven on **both** pairs. This is the lens the
  landed work is strongest on.
* **#3 Design completeness** -- backward compatibility is the design decision the
  plan review forced and it is correct by construction rather than by
  grandfather-list. Gaps: `reject`'s status is unstated ([C5]); `defer` is
  unreachable from lens #9's mapping ([C9]); the triage rule was not carried
  ([C6]).
* **#4 Silent failure / fail-closed** -- the recognizer fails **closed** on a
  missing block (mutation 3 proves it) and **open** on a placeholder-filled
  scaffold (probed, pre-existing, documented). `guard` no longer vanishes in the
  parser but is dropped at emission ([C3]). The three prose invariants ship
  fail-open **by Decision**, verified: no gate was smuggled in.
* **#5 Cross-document consistency** -- swept `doctrine/`, `templates/`, `dev/`,
  `bootstrap/`, `tools/`, `scripts/`, `.agents/`, `docs/`, root `*.md`. Lens #9's
  three surfaces all carry the mapping. Residue: [C4] (two canonical homes in one
  section) and [C6] (three triage surfaces).
* **#6 Drift** -- **the changed-file set, enumerated**, per-commit union, 20 paths,
  each opened:
  `doctrine/lifecycle.md` - `doctrine/dual-review.md` -
  `doctrine/lifecycle-contract.md` - `doctrine/plans.md` - `doctrine/proposals.md` -
  `templates/core/dev/PLANNING.md` - `templates/core/dev/plans/_template.md` -
  `templates/core/dev/proposals/_template.md` -
  `templates/modules/team-gated/dual-review.md` - `dev/PLANNING.md` -
  `dev/modules/dual-review.md` - `dev/plans/_template.md` -
  `dev/proposals/_template.md` - `bootstrap/tests/test_lifecycle_contract.py` -
  `templates/skills/_lib/lifecycle_planner.py` - `tools/lifecycle_planner.py` -
  `templates/modules/default-on/_lifecycle_metrics/subsystems.py` -
  `tools/_lifecycle_metrics/subsystems.py` - `CHANGELOG.md` -
  `dev/proposals/2026-08-04-claude-board-retro-disposition.md`.
  **Equals the revised chunk tables exactly**; no surface skipped, none added.
  Commit-claim drift at [C2], [C3], [C8].
* **#7 Lifecycle / process placement** -- archive-preparation is named as the
  serialization point in the canonical file, both mirrors, both templates and the
  state-machine row; the batching rationale travels with it; the solo-profile
  collapse is stated rather than implied. [P2]'s "homed only in a
  machine-verifiable column" defect is closed. The D1 successor's Decision
  condition is discharged and visible in `9052b09` and `791655a`.
* **#8 Domain validity & scope** -- **does not overstep**: D2 not built, no board
  row moved, `AGENTS.md` untouched, gates still unconditional. **Does not
  under-deliver**: C1-C7 all landed, C3/C5 reached the adopter templates, the
  metrics twins joined. Scope *grew* from 15 to 20 paths, all of it forced by the
  plan review and recorded.
* **#9 Name the satisfier** -- all nine findings name one; none is a bare
  observation.

### Not covered / low confidence

* **Same-type reviewer** (see *Residual risk*). The cross-type read is where the
  design questions would surface; I did not attempt them.
* **Adopter-installed output.** Verified as template source, not as merged tree.
* **`docs/` layer.** Swept for the two strings and clean, but I did not read
  `docs/tool-usage.md`'s planner section for narrative consistency with the
  re-worded gate strings -- it was edited by a **concurrent** session (`02d557b`)
  inside the same commit range and is not this plan's surface.
* **The D1 successor's content.** Read only far enough to confirm it opened, is
  `proposed`, carries [I8], and commits to no routing estimate. Its correctness is
  its own review's job.
* **`dev/PLANNING.md` has no board row for this plan.** Prevailing practice per
  the plan review; recorded, not raised.
* **The nine pre-existing `archive precondition` violations** are out of scope and
  owned by `planner-line-semantics`; I confirmed only that this change neither
  adds to nor removes from them.

### Verdict

**APPROVE WITH FOLLOW-UPS.**

The load-bearing work is correct and I proved it rather than read it. [P1] -- the
plan review's blocker, and the one defect that would have corrupted the live
record -- is discharged with the strongest evidence available: the shipped `scan`
produces byte-identical output on the real 70-artifact corpus before and after,
across seventeen archived artifacts written in the legacy spelling. The three new
assertions are non-vacuous and *orthogonal*, each falling to a different mutation.
Both twin pairs are guarded, mutation-proven, and byte-identical at HEAD. The
Decision is honoured on both edges: D2 was not built, and no board row moved --
the latter proven arithmetically, not asserted. The full suite reproduces at 1959.

Not a clean APPROVE, on nine findings, none of which touches the shipped
behaviour. Three are record defects where the durable audit trail out-claims what
landed ([C1] a completeness criterion that could not fire, [C2] a node cited to the
wrong file, [C3] a commit body promising a number no column emits); three are
doctrine-coherence gaps in the prose this change exists to write ([C4] two
canonical homes, [C5] `reject` dropped without saying so, [C9] a mapping that
cannot reach the token the whole change gates); one is an unswept sibling surface
([C6]); two are process/record honesty ([C7], [C8]). All nine close with prose or a
one-line edit. None re-opens the design, none needs new machinery, and none blocks
the archive if they are dispositioned rather than dropped -- which is, with some
justice, exactly what this plan now requires.

**A second independent pass is not warranted.** The findings are mechanical, each
ships a reproducer, and the design was settled two stages upstream. One thing the
Maintainer should see rather than infer: **[C3] is the one finding whose real close
is out of this plan's reach.** Surfacing `guard` as a metrics column would mutate
the snapshot CSV schema, which `AGENTS.md` treats as a byte-level-stable install
contract -- so it is proposal-worthy work, and the honest disposition here is to
correct the claim, not to build the column. The D1 successor is the natural place
to decide whether the column is wanted at all, since it is the first artifact that
will produce `guard` dispositions in volume.

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
1. Chunk A  -- doctrine/lifecycle.md: C1, C2, C4 AND C3 + C5        [commit 3f8ce57]
2. Chunk B  -- the four sibling doctrine files (+ plans.md:602-609) [commit 5c85274]
3. Chunk C  -- the four adopter templates, incl. C3/C5 backpressure [commit 758448a]
4. Chunk D  -- the four self-hosted mirrors                         [commit 4858c84]
5. Chunk E' -- the planner twins: 5 sites x 2 copies, BOTH spellings
               accepted, + 3 new assertions                          [commit 6ece062]
6. Chunk E''-- the _lifecycle_metrics twins: `guard` bucket          [commit 8d6ae88]
7. Chunk F  -- CHANGELOG + open the D1 successor                     [commit 791655a]
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

---

### Response to the code review -- Claude (Strategy) -- 2026-08-04

**Model**: claude-opus-5

Grammar: Code-review-Response (`doctrine/proposals.md` > "Response — disposition
grammars"). Nine findings, all accepted; five closed by the sharpening commit
`c0525c2`, four answered here.

* **[C1]** accept (rewrote inline) — the acceptance criterion was **unrunnable as
  written**: a range diff over `3f8ce57~1..791655a` sweeps up three concurrent
  sessions' commits, so it could never equal the surface set. The criterion is
  corrected to the **per-commit** form, and the actual set is enumerated in the
  ledger below: `for c in <shas>; do git show --format="" --name-only $c; done |
  sort -u` yields **exactly 20 paths** — the 19 surfaces plus the successor
  proposal. Re-derived at archive time; matches the reviewer's independent count.
* **[C2]** accept (rewrote inline) — plan row E3 named
  `bootstrap/tests/test_lifecycle_cli.py`; the three assertions landed in
  `bootstrap/tests/test_lifecycle_contract.py`, which is where the planner harness
  and `_load_planner()` live. Both files exist, so nothing flagged it — the same
  silent-miss class as [C4]. The Sequence is append-only in flight, so the
  correction is recorded here rather than edited in place.
* **[C3]** accept (rewrote inline) — and this is the fourth instance in this
  artifact's history of the house failure mode. Chunk E″'s commit body claimed
  bucketing `guard` makes the split "measurable for free"; **no CSV column emits
  it**, so the claim was made at the strength intended rather than delivered. What
  [P4] actually asked for was that the token not be *silently dropped*, and that
  **is** delivered — verified by execution. The correction is the complete fix:
  the claim is restated here at its true strength. **No follow-up is created** —
  surfacing `guard` as a column would be a CSV-schema change to a shipped module,
  which is adopter-reaching and would need its own proposal; nobody has proposed
  it, so it is an unraised idea, not a deferred obligation. Recording the
  distinction because inventing a follow-up here would inflate the board this
  plan exists to drain.
* **[C7]** wontfix — [P5] (re-splitting Chunks C and D along guarded/unguarded
  lines) was marked `accept` in the Response and then not implemented; the chunks
  landed as originally split. Re-splitting *after* the commits have landed buys
  nothing — the review boundary it was meant to improve has already been crossed,
  and rewriting history to obtain it would be strictly worse. The honest fix is to
  say the accept was not honoured, which this line does. Eligible for `wontfix`
  under the new C4 rule: reaches no adopter, blocks no release, needs no Decision.

**[C4], [C5], [C6], [C8], [C9]** accept (followup commit `c0525c2`) — closed by
the sharpening commit; see its body for what each changed and why.

## Lasting-truth migration

**Archived** 2026-08-04.

### Dispositions

*This plan is archived under the rule it landed — the first artifact to use the
`Dispositions:` block. Its own code-review findings are the follow-ups being
dispositioned.*

```
Dispositions:
* [C1] acceptance criterion unrunnable      -> accept (corrected inline; set enumerated below)
* [C2] plan row E3 names the wrong test     -> accept (corrected inline)
* [C3] E'' commit body over-claims          -> accept (claim restated at true strength)
* [C4] two canonical homes                  -> accept (commit c0525c2)
* [C5] `reject` silently dropped            -> accept (commit c0525c2)
* [C6] triage rule states superseded rule   -> accept (commit c0525c2)
* [C7] [P5] accepted but not implemented    -> wontfix (post-landing re-split buys nothing)
* [C8] CHANGELOG leads with withdrawn line  -> accept (commit c0525c2)
* [C9] lens #9 range has no `defer`         -> accept (commit c0525c2)
```

**Zero `defer` dispositions**, so this archive needs no Maintainer authorization
and adds **no row** to `dev/PLANNING.md`. Net board delta: **0** against the
+4.7-per-plan baseline the proposal measured — the governing principle, met on
the artifact that introduced it.

**The D1 successor is not a deferral of this plan.** It was split by the Decision
and opened at `791655a` as stem `2026-08-04-claude-board-retro-disposition`,
status `proposed`. It is a `defer` (successor) the Maintainer authorized in
advance, not one this archive is requesting.

### Evidence ledger

**Evidence shipped.** Full suite **1959 passed** in 263s under
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13, canonical) —
independently re-run by the code reviewer at 1959/238s. `check_cairn` OK across
192 files. Both twin pairs byte-identical by `cmp`. Three new assertions in
`bootstrap/tests/test_lifecycle_contract.py`, **proven non-vacuous by mutation**
and independently reproduced by the reviewer, who additionally established that
the three mutations produce three *different* single-node failures — the
assertions are orthogonal, not redundant. Backward compatibility proven **on the
real tree**: old and new planner produce identical `scan --include-archive`
output across 17 archived artifacts carrying the legacy spelling.

**Evidence deferred.** None.

**Changed-file set (the [C1] criterion, corrected form).** Eight implementing
commits `3f8ce57`, `5c85274`, `758448a`, `4858c84`, `6ece062`, `8d6ae88`,
`791655a`, `c0525c2` touch exactly these **20** paths — the 19 named surfaces
plus the successor proposal, with nothing extra:

`CHANGELOG.md`, `bootstrap/tests/test_lifecycle_contract.py`, `dev/PLANNING.md`,
`dev/modules/dual-review.md`, `dev/plans/_template.md`,
`dev/proposals/2026-08-04-claude-board-retro-disposition.md`,
`dev/proposals/_template.md`, `doctrine/dual-review.md`,
`doctrine/lifecycle-contract.md`, `doctrine/lifecycle.md`, `doctrine/plans.md`,
`doctrine/proposals.md`, `templates/core/dev/PLANNING.md`,
`templates/core/dev/plans/_template.md`,
`templates/core/dev/proposals/_template.md`,
`templates/modules/default-on/_lifecycle_metrics/subsystems.py`,
`templates/modules/team-gated/dual-review.md`,
`templates/skills/_lib/lifecycle_planner.py`,
`tools/_lifecycle_metrics/subsystems.py`, `tools/lifecycle_planner.py`.

**Residual risks, stated rather than closed.**
* **All three invariants are documentary.** Nothing mechanically checks that a
  disposition is the *right* one, or that a `defer` authorization was really
  given. This was the Decision's explicit call: D2 (a content-parity gate) was
  **not authorized**, and the reviewer's mutation test confirms doctrine ↔
  template prose parity is unguarded across all mirrors.
* **~15 in-flight plans under `dev/plans/`** still carry the superseded
  boilerplate. Deliberate: they are other agents' live artifacts, and backward
  compatibility means none of them breaks by waiting.
* **The `guard` token is bucketed but not surfaced** in any metrics column
  ([C3]).

### Loop-fidelity sign-off

The landed implementation commits `3f8ce57..c0525c2` match the accepted
**`## Revised proposal`** section of
[`2026-08-04-claude-deferral-discipline`](../proposals/archive/2026-08-04-claude-deferral-discipline.md),
items **C1–C7**, as ratified by the Decision at `6e349b3`. Two Decision-scoped
exclusions were honoured and independently verified by the code reviewer: **D2
was not built** (no checker in any of the 20 changed paths) and **no board row
was re-routed** (`dev/PLANNING.md` is a single hunk; 1002 + 35 = 1037 exactly).
