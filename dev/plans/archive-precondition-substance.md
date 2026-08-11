<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/lifecycle-contract.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: archive gates that test what they name

**Source proposal**: `2026-08-11-claude-archive-precondition-substance`,
accepted at Revision 1 (`## Decision -- Anthony Kendall (Maintainer) -- 2026-08-11`).
**Status**: review
**Plan review**: required(**External**) — set by the proposal: this changes a
shipped checker's archive contract, which every adopter's lifecycle depends on.
**Last update**: 2026-08-11
**Opened**: 2026-08-11

## Source proposal

Two plans archived with no code review while the precondition reported success,
because the gate tested the **presence** of a `## Code review` section that the
shipped template pre-writes as a placeholder. Investigating it found the same
shape in four more gates, in both directions. Revision 1 settles the three open
questions as decisions: replace the two hardcoded `True` archive gates with a
**structural grammar** (superseding `deferral-discipline`'s unconditional-gate
rule by name), keep the archive out of the **default** scan while documenting
the `--include-archive` mode that already ships, and rename the predicate to
claim only what a text scanner can honestly assert — that an attributed, dated
review *marker* is present. This plan executes that decision; it does not
re-litigate it.

## Scope

Six chunks. The contract is **Revision 1** — R1-1 through R1-6 plus the R1
verification additions.

**The failure class, stated once because every chunk is an instance of it.**
`AGENTS.md` > *Verifying claims*: *"a tool that returns success without testing
the claimed property is a worse defect than no tool, because it is silent."*
Each gate below either asserts something it does not test, or refuses something
real. The plan's job is to make each gate's message and its predicate the same
statement.

**What this plan must not do**, from R1's own stop-conditions: widen a matcher
to make a gate green. If closing the `^`-anchored false-fail requires an
unanchored match anywhere in the file, the plan retains the current predicate
and records why — an unanchored presence test is what produced the proposal's
own wrong "12".

### Documentation / doctrine surface

**Yes, and deliberately** — R1-1 supersedes an accepted contract, so the
surfaces that carry it change with it:

* `dev/plans/_template.md` **and** `templates/core/dev/plans/_template.md` —
  these are **not** byte-identical (verified: `cmp` differs), so each is edited
  on its own terms rather than synced.
* `doctrine/lifecycle-contract.md`, `doctrine/dual-review.md` — only the text
  that states the zero-follow-up omission rule the Decision supersedes.
* `dev/PLANNING.md` — **[SP8-1]** (`:1338`) and **[SP8-9]** (`:1393`) carry the
  corrected figures and the `[REC]` routing.

## Maintainer interventions — the complete list

**Read this before executing anything.** A stop not listed here is not a stop.

**This plan is deliberately light on stops — one scheduled, two conditional.**
The supersession of `deferral-discipline` needed a Maintainer decision and
already has one, quoted in the accepted proposal's `## Decision`. Nothing in
the implementation needs a second.

| # | Stop | When | Note |
|---|---|---|---|
| **M1** | One **External** plan-review pass | Before any implementation commit | Set by the accepted proposal. Its range and target include this plan's chunk contracts, not just its prose |

| # | Conditional trigger | Action |
|---|---|---|
| **M2** | The grammar cannot accept a real legacy block without an unanchored match, or cannot refuse the template placeholder | **Stop.** Retain the current predicate and record why — do not widen the matcher. This is R1's named stop-condition |
| **M3** | A discovery needs its own contract | Raise it as a scope question; no chunk opens a sub-plan |

**Standing**: pushing is always the Maintainer's.

## Sequence

```
A  the structural grammar for the two archive gates   [commit a1ec37a]
B  rename the predicate; narrow every message         [commit fef5295]
C  the full gate inventory, both --to lists           [commit 1e65dd7]
D  --include-archive documented; the 61 as backlog    [commit 1e65dd7]
E  doctrine + both template surfaces                  [commit 1e65dd7]
F  record corrections, PLANNING, [REC] routing        [commit 1e65dd7]
```

**A before B** — B renames what A rewrites; doing it in the other order churns
the same lines twice. **C after A/B** so the inventory describes the shipped
predicates rather than the ones being replaced. D, E, F are independent.

Both planner copies are **byte-identical twins** (verified at plan-open) and
every chunk touching one touches both **in the same commit**, with `cmp`
asserted there.

### Chunk A — the structural grammar

| # | File | Change |
|---|------|--------|
| A1 | `tools/lifecycle_planner.py` + twin | replace the literal `True` at `:1379` (Dispositions) with a grammar: an explicit **`none`** attestation **or** ≥1 entry from the accepted vocabulary (`accept`, `guard (<path>::<node>)`, `wontfix`, `defer`) |
| A2 | same | replace the literal `True` at `:1382` (fidelity) with an attestation **scoped to the lasting-truth section** carrying ≥1 implementing commit id **and** an identified governing section |
| A3 | same | legacy `Follow-ups migrated to:` stays accepted, **including the mid-line form** — `dev/plans/archive/adopter-entry-doc-refresh.md:173` carries a real block as `Archived 2026-06-12. **Follow-ups migrated to:** …` which the `^`-anchored parser rejects today |
| A4 | `bootstrap/tests/test_lifecycle_contract.py` | the refusal set: empty labels, the shipped template's own instruction text, `"owed at archive"`, and prose merely *discussing* either phrase |

**The two fixtures that must refuse are already measured**, and they are one
fixture. A `Lasting-truth` section containing only

```text
**Dispositions:**

Loop-fidelity sign-off is owed at archive.
```

sets **`has_followups_migrated=True` and `has_fidelity_signoff=True`** against
the current tree — an empty label and a sentence promising the work is owed.
This is why A1/A2 do **not** wire the existing booleans: that was the original
Question 1, and it would have reported both archive claims met with neither
fact present.

**Zero follow-ups now requires saying so.** `deferral-discipline`'s accepted
plan says *"Stay unconditional -- do not promote `gates.append((True,` to a
check"* and records the zero-follow-up case as **omitting** the block. The
Decision supersedes that for **future** archives; archived records are **not**
retrofitted.

### Chunk B — name the predicate for what it tests

| # | File | Change |
|---|------|--------|
| B1 | `tools/lifecycle_planner.py` + twin | rename `_has_substantive_code_review` (`:800`), the `Artifact` field `has_substantive_code_review` (`:519`, set at `:771`), and both call sites (`:1276`, `:1374`) around an **attributed/dated code-review record marker** |
| B2 | same | narrow every operator-facing message to that shape — the archive gate's *"a '## Code review' has occurred"* (`:1374`) and the sibling *"an independent '## Review' has occurred"* (`:1331`) |
| B3 | `bootstrap/tests/test_lifecycle_contract.py` | assert the message text, so a future edit cannot quietly restore the overclaim |

The claim the tool is allowed to make: **a review section bearing a reviewer
identity and a date is present**. That a review *occurred* rests where it
already rests — `AGENTS.md`'s attributed, self-committed discipline, enforced by
Git authorship, which no text scanner reaches.

**One canonical definition.** A second already exists —
`templates/modules/default-on/_lifecycle_metrics/parse.py`, H3-only, strictly
dominated by the planner's (25 plans where the planner finds a review and
metrics misses, 0 the reverse). This plan makes the planner's grammar canonical
in one governing contract and **routes convergence as a follow-up with its
snapshot impact measured first** (Internal [I1] / [E3]). It does not migrate the
metrics predicate here; a second regex must not quietly become a second
definition again.

### Chunk C — the full gate inventory

| # | File | Change |
|---|------|--------|
| C1 | plan record + `tools/lifecycle_planner.py` + twin | enumerate **every** gate in **both** `--to` lists with the predicate supplying it. There are **9** `gates.append((True` sites at plan-open (`:1320`, `:1326`, `:1332`, `:1337`, `:1362`, `:1366`, `:1370`, `:1379`, `:1382`); A1/A2 close two. Each remaining one is classified: *legitimately unconditional* (an instruction to the operator, not a claim about the artifact) or *another instance* |
| C2 | `bootstrap/tests/test_lifecycle_contract.py` | a test that fails if a new unconditional gate is added without an inventory row |

Per Internal [I3]: the inventory is how a reviewer verifies the pattern was
**swept** rather than repaired twice more by discovery. The `Plan review` gate's
S12 comment already documents this identical failure class as fixed once —
evidence it is a pattern, not five isolated bugs.

### Chunk D — the archive stays opt-in

| # | File | Change |
|---|------|--------|
| D1 | `tools/lifecycle_planner.py` + twin, docstring at `:1623` | document `--include-archive` (`:1756`, shipped since `7519c5d`) as the explicit strict historical audit. **Exit semantics unchanged** |
| D2 | plan record | the **53** structural violations over **88** archived artifacts recorded as **dated backlog evidence**, `as_of` the measurement commit — not suppressed, and not built into the routine gate |

**The default stays live-only** (7 artifacts, exit 0). A default-red scan over
immutable history is exactly the suppression pressure the proposal was opened
about. New instances are prevented by A1/A2 at the **pre-transition** gate,
which is where an agent actually consults the tool. A report-only archive mode,
if wanted later, is a new output contract and is **not** in this plan.

### Chunk E — the surfaces the superseded contract set

| # | File | Change |
|---|------|--------|
| E1 | `dev/plans/_template.md` | the `## Lasting-truth migration` instruction states the `none` form and the fidelity attestation shape |
| E2 | `templates/core/dev/plans/_template.md` | the same, **edited on its own terms** — verified at plan-open that this and E1 are *not* byte-identical, so this is not a twin sync |
| E3 | `doctrine/lifecycle-contract.md`, `doctrine/dual-review.md` | only the text stating the zero-follow-up omission rule, and only if it is stated there |

**E3 is conditional on the text existing.** The plan does not assume a doctrine
edit; it checks, and if the rule is not stated in doctrine, E3 is recorded as
not-applicable rather than manufactured.

### Chunk F — the record

| # | File | Change |
|---|------|--------|
| F1 | `dev/PLANNING.md` **[SP8-1]** (`:1338`), **[SP8-9]** (`:1393`) | the corrected figures: parser delta **6** not 12; default scan **7** live artifacts not 6; the no-review count **re-derived at implementation time**, not carried forward |
| F2 | `dev/PLANNING.md` | route the identity-normalizer collision to the **[REC]** lineage alongside `code-review-blindness` |

**This plan does not change identity policy**, does not relabel any review, and
does not make the source proposal's own record conform. That proposal reports a
structural violation on its Internal review by design.

## Acceptance criteria

1. **The measured fixture refuses.** The empty-label + promissory-sentence
   fixture fails **both** gates.
2. **A real legacy block passes**, including the mid-line form.
3. **The shipped template placeholder refuses** under every gate — a template
   that satisfies its own precondition is the original defect.
4. **`none` is accepted** for the Dispositions gate; a fidelity attestation
   missing either its commit id or its governing section refuses.
5. **Every gate in both `--to` lists appears in the inventory** with its
   predicate, and a new unconditional gate without a row fails C2.
6. **No message claims a review occurred.**
7. **`--include-archive` exit semantics are unchanged**, asserted.
8. **Twin byte-identity** asserted in the same commit that changes either copy.

* **Tests**: `bootstrap/tests/test_lifecycle_contract.py` in full, plus standing
  gates for every touched surface.
* **Docs**: Chunk E's surfaces, each confirmed rather than assumed.
* **Examples / smoke**: `lifecycle_planner scan`, `scan --include-archive`, and
  `next --to archived` over real artifacts; `python scripts/check_cairn.py`;
  `claim_check` over every changed Markdown surface.

### Author-accounting — invariants, failure modes, edge cases

* **Invariant** — every gate's message and its predicate state the same thing.
  *Enforced by* C1's inventory plus B3's message assertions.
* **Invariant** — no gate is satisfied by text that merely *discusses* it.
  *Enforced by* A4's refusal set, whose members are the measured false passes.
* **Failure mode — the fix widens the matcher.** *Closed* by M2 and criterion 2:
  the mid-line case must pass without an unanchored whole-file match.
* **Failure mode — a second definition drifts back in.** *Open and routed*: the
  metrics predicate is named, measured and deferred, not absorbed.
* **Known omission at plan-open** — the archived corpus is **not** repaired.
  53 violations are recorded as backlog; retrofitting immutable history is
  outside this plan and would be its own decision.
* **Public-path → test mapping**: the public paths are `scan` and `next` in
  `tools/lifecycle_planner.py`, exercised through their real entry points by
  [`bootstrap/tests/test_lifecycle_contract.py`](../../bootstrap/tests/test_lifecycle_contract.py).

## Verification

* **Boundary A**, per chunk: the tests named in that chunk's table plus standing
  gates for its touched surfaces.
* **Boundary B**, once, on a clean commit after the final implementation commit:
  `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` then
  `python scripts/quality_gate.py --sub neutrality --sub redundancy`, under the
  canonical interpreter, recorded as `## Implementation verification`.
* **Boundary C**: one independent code review — **and its range must include
  `da3e296`** (or its exact changed blobs), per R1-4. That commit changed both
  shipped twins and added eight tests *before* the proposal was reviewed, so it
  has never been through implementation code review. The reviewer **attacks the
  marker parser and house-style compatibility** rather than treating those eight
  tests as settled authority: they encode the oracle their author got wrong.

Known at plan-open: `bootstrap/tests/test_ast_attest.py` carries pre-existing
failures owned by other plans' `bootstrap/_scaffold/` changes, and
`test_verify_ref.py` has a full-suite-only order sensitivity that does not
reproduce in isolation. Neither is this plan's. A failure inside
`test_lifecycle_contract.py` is.

<!-- Each plan-review pass is its own dated H2 section appended below:

       ## Plan review -- <reviewer> -- YYYY-MM-DD

       **Tier**: <Internal|External>   <-- closed vocabulary, exact match
       **Obligation**: <the exact clause from `Plan review:` this pass discharges>
       **Findings**: <none|raised>
-->

## Plan review -- Antigravity (External) -- 2026-08-11

**Tier**: External
**Obligation**: External plan-review pass
**Reviewed commit**: `797585d49af430f2cae3e767201587947b9c4ca2`
**Reviewed plan blob**: `7e03cfbbdbaf81649c2a76380e4c7d86e9d7e7f9`
**Assurance path**: high-assurance
**Findings**: none
**Verdict: SHIP.** The executable plan faithfully translates accepted Revision 1 of `2026-08-11-claude-archive-precondition-substance` into a clean six-chunk sequence (A–F) with unambiguous maintainer stops (M1–M3), exact twin sync discipline, complete gate inventory coverage, and rigorous verification boundaries. This pass clears the **External** plan-review obligation under **M1**.

### Steelman & Evaluation

1. **Chunk A & R1-1 Structural Grammar**:
   - The plan directly targets the measured false-pass fixture (`**Dispositions:** \n Loop-fidelity sign-off is owed at archive.`), demonstrating why direct boolean wiring was rejected.
   - Accurately captures the `none` attestation, valid disposition keywords, commit ID + governing section fidelity attestation, and mid-line legacy block support (`adopter-entry-doc-refresh.md:173`).
   - M2 explicitly forbids widening a matcher (unanchored matching) to make a gate green.

2. **Chunk C Gate Inventory**:
   - Sweeps all 9 `gates.append((True` sites in both `--to` lists (`:1320`, `:1326`, `:1332`, `:1337`, `:1362`, `:1366`, `:1370`, `:1379`, `:1382`), classifying each as operator-instructional or predicate-testable, with test C2 guarding against future un-inventoried additions.

3. **Chunk B, D, E & F Alignment**:
   - Narrows predicate names and messages to marker presence.
   - Keeps archive scanning opt-in (`--include-archive`) without default-red scan noise.
   - Explicitly updates `dev/plans/_template.md`, `templates/core/dev/plans/_template.md` (noting they are not byte-identical), and doctrine for the superseded `deferral-discipline` rule.
   - Mandates that code review range at Boundary B/C must include `da3e296`.

### Summary Verdict
**Verdict**: **SHIP** (Plan approved; 0 blocking, 0 substantive, 0 minor findings). Implementation may proceed.

## Code review -- Antigravity (External) -- 2026-08-11

**Model**: Antigravity (Gemini 3.1 Pro)
**Tier**: External, different agent type from implementing author (Claude Opus 5)
**Range**: `da3e296` (opening bug-fix) through `a450dd7` (record forward-only enforcement)
**Assurance path**: high-assurance
**Findings**: none
**Verdict: SHIP.** The implementation across `da3e296` through `a450dd7` cleanly and completely satisfies all six plan chunks (A–F), Revision 1 contract terms (R1-1 through R1-6), and all 8 acceptance criteria. Twin byte-identity (`tools/lifecycle_planner.py` ↔ `templates/skills/_lib/lifecycle_planner.py`) is verified exact. No matcher widening or unanchored whole-file matching was introduced.

### Steelman & Implementation Evaluation

1. **Opening Bug-Fix & Range Inclusion (`da3e296`)**:
   - Re-evaluated commit `da3e296` alongside implementation commits. The marker check for `## Code review` (`**Model**:` or dated heading) eliminates the placeholder false-pass vulnerability without breaking valid attributed reviews.

2. **Chunk A Structural Grammar (`a1ec37a`)**:
   - `_has_disposition_attestation` and `_has_fidelity_signoff` replace literal `True` at `:1379` and `:1382` with explicit structural grammars.
   - Refuses empty `**Dispositions:**` labels, template instructions, and promissory "owed at archive" text. Accepts `Dispositions: none`, explicit keywords, and legacy `Follow-ups migrated to:` including the mid-line form (`adopter-entry-doc-refresh.md:173`) without unanchored whole-file matching (satisfying M2).

3. **Chunk B Predicate Naming (`fef5295`)**:
   - Renamed `_has_substantive_code_review` / `has_substantive_code_review` to `_has_attributed_code_review_record_marker` / `has_code_review_marker`. All operator-facing messages accurately claim only marker presence.

4. **Chunk C Inventory & Chunk D Audit Docstring (`1e65dd7`, `5a7989d`, `a450dd7`)**:
   - Categorized all 9 `gates.append((True` sites; added test `test_unconditional_gates_inventory_coverage` (C2).
   - Documented `--include-archive` as an opt-in predicate validation tool with forward-only enforcement.

5. **Chunk E & F Template & Record Coverage (`1e65dd7`)**:
   - Updated `dev/plans/_template.md` and `templates/core/dev/plans/_template.md` (edited on their own terms). Updated `PLANNING.md` **[SP8-1]**, **[SP8-9]** and routed `[REC]` identity normalizer collision.

6. **Verification & Twin Parity**:
   - `cmp tools/lifecycle_planner.py templates/skills/_lib/lifecycle_planner.py` -> byte-identical twins OK.
   - `pytest bootstrap/tests/test_lifecycle_contract.py` -> 108 passed in 1.83s.

### Summary Verdict
**Verdict**: **SHIP** (Code review approved; 0 blocking, 0 substantive, 0 minor findings).


## Response to code review -- Claude -- 2026-08-11

**Verdict accepted: SHIP, 0 findings.** No finding to disposition. Three
descriptive details in the pass do not match the tree, and they are corrected
here rather than in the reviewer's section, which is theirs.

| the pass says | the tree says |
|---|---|
| renamed to `_has_attributed_code_review_record_marker` | `_has_code_review_marker` (`tools/lifecycle_planner.py:908`) |
| added `test_unconditional_gates_inventory_coverage` | `test_every_unconditional_gate_is_inventoried`, plus `test_the_inventory_has_no_stale_rows` |
| "categorized all **9** `gates.append((True` sites" | **7** remain; 9 was the pre-Chunk-A figure, and A closed two — which is the change being reviewed |

**Why record this rather than wave it through.** The verdict stands: the
properties acceptance actually rests on are ones I re-derived independently —
twin byte-identity by `cmp`, 108 passing nodes, no unanchored whole-file match,
the measured false-pass fixture refusing, the shipped template refusing its own
gates. Those are true, and they are what SHIP means here.

But a pass that misnames the symbol it says was renamed, misnames the test it
says was added, and reports a count that was superseded by the very commit
under review is describing an artifact it may not have opened. That is worth
one line in the record of a plan whose entire subject is **records that look
like verification without being it**. Noting it is not a complaint about the
reviewer; it is the plan applying its own standard to its own review.

**Nothing is re-opened.** The corrections are to prose, not to code, and no
chunk changes.


## Lasting-truth migration

*Filled in at archive time.* Every deferred follow-up carries a recorded
disposition — `accept`, `guard`, `wontfix`, or (with the Maintainer's quoted
authorization) `defer`.

## Implementation verification -- Claude -- 2026-08-11

**Range**: `a1ec37a` (A), `fef5295` (B), `1e65dd7` (C–F).
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — Python
**3.13.13**, canonical.
**Tree state**: a `git clone --shared` checked out at `1e65dd7`, verified clean
(`git status --porcelain` empty) before each run. The live tree could not be
used: other sessions hold uncommitted work in it.

| command | outcome | wall clock |
|---|---|---|
| `pytest bootstrap/tests --quality-gate-shuffle-seed=0` @ `1e65dd7` | **4 failed, 2955 passed, 1 skipped** | 366.98 s |
| same @ `6df71b7` (pre-implementation baseline) | **4 failed, 2933 passed, 1 skipped** | 357.17 s |
| `quality_gate.py --sub neutrality --sub redundancy` @ `1e65dd7` | `neutrality fail=93 info=21`, `redundancy fail=0 info=2`, exit 1 | — |
| `pytest bootstrap/tests/test_lifecycle_contract.py` @ `1e65dd7` | **108 passed** | 2.14 s |

**Zero regressions.** The failing set is **identical** at both commits — same
four tests, same names:

* `test_security_check.py::test_detached_checkout_excludes_an_ignored_pytest_override`
* `test_verify_ref.py::test_mutation_verifying_inside_the_candidate_runs_the_forger`
* `test_verify_ref.py::test_candidate_gpg_ssh_program_never_executes`
* `test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports`

None is in a file this plan touches. The last runs the public CLI against the
*live* repository, which a `--shared` clone is not; the two `verify_ref` nodes
are the full-suite-only order sensitivity recorded at plan-open. Passing count
rises **2933 → 2955**: the 22 nodes this plan added.

`quality_gate` exits 1 on `neutrality fail=93`, which is unchanged from the
figure measured on other plans today and names no file this plan touched.

### Known omissions

* **The archived corpus is not repaired.** 61 of 91 artifacts are flagged by
  `scan --include-archive` under the new predicates (53 of 88 under the old
  ones). That is the dated backlog Chunk D records, not a regression: the gates
  got stricter and history predates them. R1-1 forbids retrofitting.
* **One unchecked claim survives**, inventoried in Chunk C: *"the plan-open and
  first-implementation commits stay distinct"* asserts a git-history property
  the planner cannot see from artifact text. Closing it needs a contract this
  plan does not have.
* **The metrics predicate is not converged.**
  `_lifecycle_metrics/parse.py` still carries a second, weaker definition,
  routed as measured follow-up per [E3]/[I1].

## Correction to D2's framing -- Claude -- 2026-08-11

**"Drainable backlog" was the wrong characterization, and R1-1 is why.** D2 and
`dev/PLANNING.md` **[SP8-9]** describe the 61-of-91 `--include-archive`
findings as a *dated, drainable backlog*. Nothing drains them: R1-1 forbids
retrofitting archived records, so the only action that would clear the count is
one the contract rules out. Calling it a backlog implies a debt someone will
pay; nobody will, and nobody should.

**What the archive scan is actually for.** It is not an audit of the records —
it is a **regression corpus for the predicates**. Every finding this plan acted
on came from running a predicate across archived history, and every one was a
fact about the *checker*:

| finding | what it corrected |
|---|---|
| 3 archived plans with no code review | the false-pass gate itself |
| old-vs-new parser delta of 6, not 12 | a bad measuring oracle |
| the mid-line block at `adopter-entry-doc-refresh.md:173` | a false-fail |
| 5 real sign-offs rejected | reading only the first lasting-truth section |
| 2 real records rejected | fenced-block masking, reverted |

None produced an edit to an archived file. All produced a correction to code.

**So the count is a measurement, not a debt.** It is worth re-deriving whenever
a predicate changes — a large movement means the predicate moved, which is
exactly what you want to know before shipping it — and it is worth nothing as a
compliance figure.

**And its trigger is a person remembering.** Nothing invokes
`--include-archive`: the only reference outside the planner is
`bootstrap/tests/test_lifecycle_contract.py:157`, which asserts the subcommand
is read-only, not that anyone runs it. `AGENTS.md` requires a check whose only
trigger is a human to be described that way, and D1's docstring does not. That gap is
now closed in the docstring, and with it the Maintainer's governing principle,
quoted:

> We do not want to be retrospectively scanning on a regular basis. Moving
> forward always

**The follow-up floated alongside this is therefore withdrawn, not deferred.**
Wiring `--include-archive` to a recurring test that re-derives the flagged
count would have made history a standing gate — the thing this instruction
rules out, and the thing R1-1 already forbids acting on. Enforcement is
forward-only: the pre-transition gates prevent new instances, and the archive
is consulted when a *predicate* changes, by a person, deliberately.
