<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/plans.md doctrine/proposals.md doctrine/lifecycle-contract.md doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: bootstrap/tests/test_lifecycle_board.py, bootstrap/tests/test_lifecycle_vocabulary.py, scripts/gen_legacy_code_review_passes.py, dev/measurement/pilot-activation.md, dev/measurement/pilot-events.md, dev/plans/corpus-tier-cost.md, dev/plans/git-native-security-foundations.md, dev/.cairn/pilot-state.json, tools/__init__.py -->
<!-- The three paths above are forward references created by Chunks A, C and F.
     They are also registered under `Proposed paths:`; that marker exempts only
     its own contiguous bullet block, so this file-scoped directive covers the
     chunk tables that name the same paths. Each line drops when its file lands.
     `tools/__init__.py` is the opposite case: it is cited BECAUSE it must never
     exist -- A3/A5's no-package-shortcut clause -- so no typed declaration can
     express it.  `dev/.cairn/pilot-state.json` is a third case: the landed,
     append-only Security review cites it, and the revision it prompted replaced
     that path with the two `dev/measurement/` records.  The review section is
     immutable, so the citation is marked rather than edited. -->

# Plan: one lifecycle contract, one evidence boundary

**Source proposal**: [`review-efficient-lifecycle`](../proposals/2026-08-10-codex-review-efficient-lifecycle.md),
executing jointly with its three accepted amendments —
[`claim-check-exemption-hygiene`](../proposals/2026-08-10-codex-claim-check-exemption-hygiene.md),
[`code-review-blindness`](../proposals/2026-08-10-claude-code-review-blindness.md),
and [`lifecycle-status-vocabulary`](../proposals/2026-08-10-codex-lifecycle-status-vocabulary.md).
All four are `accepted`, and three of them state in their own accepted text
that they open no standalone plan. This is that plan.
**Status**: executing
**Plan review**: required(**External** + **External Security Review**) — the
strongest tier among the four sources, and under `lifecycle-status-vocabulary`
R3 the `+` means **two obligations and two distinct passes**. **No
implementation commit lands before both passes are in the tree.**
**Last update**: 2026-08-10
**Opened**: 2026-08-10

## The review budget, stated first

This plan exists to *reduce* ceremony, so its own ceremony is bounded up front
and does not grow per chunk:

| Touchpoint | Count | When |
|---|---|---|
| Plan review | **2** | Before any implementation. The two declared obligations, one pass each. |
| Boundary A | per chunk | Scoped tests only. Not a review; no sign-off, no section. |
| Boundary B | **2** | Once on stable pre-review bytes; once on the post-ceremony commit. |
| Code review | **1** | Once, over the stable pre-ceremony range. |
| Maintainer ceremony | **1** | One re-anchor for the whole batch. |
| Archive | **1** | One closeout. |

**Seven touchpoints for the whole cluster.** Four separate plans would have
cost four of each — roughly twenty-eight. That arithmetic is the case for
consolidation; if this plan ever grows a *per-chunk* review, it has lost its
reason to exist.

## Maintainer interventions — the complete list

**Read this before executing anything.** Everything in this plan is agent work
**except** what is listed here. This section is the single authoritative
enumeration: if a stop is not in this table, it is not a stop, and an
implementing agent does not invent one. Conversely, no chunk elsewhere in this
plan may introduce a Maintainer stop without adding a row here.

This exists because the stops were previously scattered across nine locations
(the sequence block, three chunk rows, a tier note, the restart cases, Chunk I's
own section). That is survivable for a human reading top-to-bottom and is
**not** survivable for an autonomous or parallel run, where the cost of missing
one is an unauthorized ceremony rather than a paused agent.

### Precondition — must be true before the first implementation commit

| # | Condition | State as of 2026-08-11 |
|---|---|---|
| **M0** | The three security plans are **archived** — `api-web-security-modules`, `release-security-bar`, `security-verification-activation` — per the Maintainer's 2026-08-10 sequencing statement | **MET as of 2026-08-11.** All three are at `**Status**: archived` under `dev/plans/archive/`. Was NOT MET when this table was written; the remaining two archived during the day. *Caveat, not a blocker:* none carries a `Dispositions:` block in the checked spelling, and moving them out of `dev/plans/` removed them from the conformance scan's live set rather than satisfying the precondition. That is the subject of the in-flight `archive-precondition-substance` proposal and is not this plan's to fix |

M0 is a **precondition, not a ceremony** — nobody has to *do* anything at it
except confirm it. But it gates the first implementation commit, and it is
currently false, so an execution run starting now would breach the plan's own
fence on commit one. It is also a live-collision hazard: those two plans are
another session's in-flight work.

### Scheduled stops — exactly two in the whole A → P6d run

| # | Stop | Where | What the Maintainer does | What an agent must not do |
|---|---|---|---|---|
| **M1** | Re-anchor ceremony | **Chunk I**, after every A–H byte is stable **and** the Code review has landed | Performs `bootstrap/REANCHOR_RUNBOOK.md` once for the whole batch | Perform it, absorb it into another chunk, or self-service the frozen set. Chunk I's own words: *"No agent performs or absorbs this."* |
| **M2** | Pilot activation | **P6d**, after Boundary B2 | Lands the data-only commit introducing the immutable activation record | Land the activation record, or enable the pilot by any other route. **No code lands at activation** — if a P6d commit contains code, it is wrong |

Everything from **A through H, P1–P8's implementation, B1, and B2** is agent
work requiring no Maintainer contact.

### Conditional stops — reached only if a specific thing happens

| # | Trigger | Action |
|---|---|---|
| **M3** | Implementation needs to change `_resolve_interpreter` (`tools/lifecycle.py:414`), its schema, validation order, fallback disposition, warning visibility, or any subprocess use of the resolved path | **Stop for a new Security Review.** P4 is fenced off this surface; it is a protected trust root named in `AGENTS.md` |
| **M4** | A discovery needs its own contract | Raise it to the Maintainer as a **scope question**. Do not open a sub-plan — no chunk in this plan opens one |
| **M5** | A correction lands inside the gate inventory after the ceremony | Restarts **M1**. See the restart cases in `## Sequence`; they are not re-stated here |
| **M6** | The pilot completes its 60-day / six-plan window | The **promotion Decision** — then and only then does **P7** execute. Structurally out of reach for this execution run |

### Standing, and not specific to this plan

**Pushing.** Always the Maintainer's, without exception, per `AGENTS.md`. The
plan authorizes the change; it never authorizes publishing it.

### One gate reduced on 2026-08-11, recorded rather than done quietly

The tier note previously read *"P6b/P6d/P7 are Maintainer-gated."* **P6b is no
longer gated.** It authors `dev/collaboration_agreement.md`'s pilot section —
pause conditions, evidence report shape, and a *description of* the Maintainer
promotion Decision. Describing a Decision is not taking one. P6b ships inside
the reviewed range and therefore carries Boundary B1 and the independent Code
review like every other authored surface, which is the control that actually
applies to it.

This is a **post-SHIP change to a reviewed contract**, made at the Maintainer's
explicit request to minimize interventions, and it is flagged here rather than
absorbed silently. Neither External round 7 nor Security round 6 named P6b
among the gates their clearance rests on — Security named immutable pilot
activation (**M2**), the frozen-file ceremony (**M1**), and the conditional P7
review (**M6**), all three of which are untouched. If the Maintainer disagrees,
restoring the gate is a one-line revert of this paragraph and the tier note.

**Two Boundary B records, named as two.** The opened plan budgeted one, which
contradicted the accepted order this plan's own Chunk I cites: the re-anchor
rewrites `bootstrap/tests/fixtures/gate_manifest.json`, a fixture inside the
reviewed range, and the runbook runs the canonical suite **zero** times
(verified 2026-08-10). Calling two broad executions one would have been a
budget that reads cheaper than the contract it implements.

Boundary A/B/C are the already-accepted
[`verification-evidence-boundaries`](archive/verification-evidence-boundaries.md)
contract, which is implemented today. This plan uses it; it does not wait on
its own deliverables to verify itself.

**No chunk opens a sub-plan.** A discovery that needs its own contract is
raised to the Maintainer as a scope question (fence **M4**), not converted
into another planning artifact. Chunk count is not ceremony; review passes are.

## Bootstrap attestation — retired 2026-08-10, before it was ever used

This plan carried a two-row obligation table and, beneath it, a one-time
Maintainer exception authorizing the `executing` transition despite a parser
violation. Both are **removed**, and the reason is worth keeping.

The violation was never a property of this plan. `_has_disposition` bounded a
`## Response to plan review` by the *next* pass, so when two review obligations
were answered in one Response — the normal shape for `required(A + B)` — the
first pass of every pair was overtaken before its Response landed, and
append-only forbade inserting one between two landed reviews. Nine rounds
accrued **four** permanent violations — External rounds 2–5, re-derived by
executing the pre- and post-`286f07d` modules over the 37-plan corpus; round 1
was answered before the first Security pass and never became one — and three of
those rounds (H2/T3, J1/K1,
L1/M1+L2) were spent perfecting a governance override for a defect in the
checker rather than in the artifact.

`286f07d` fixed the checker: a pass is dispositioned iff some Response follows
it, which is exactly the group above that Response and after the previous one.
Measured across 36 plans, exactly one artifact's count changed — this one, from
4 to 0. Both `executing` preconditions now report MET.

So there is nothing left to grant an exception for. The two review obligations
still stand and are still discharged by two distinct clearing passes; what is
gone is the apparatus that existed only to get past a rule that should not have
refused.

**The lesson this plan pays for.** Three review rounds went into an override
before anyone asked whether the gate was right. When a gate refuses a shape
that has no author-side workaround, the gate is the first thing to check.


## The six accepted proposals, and where each is executed

One place to see the whole programme. Four proposals are implemented **inside
this plan**; two keep their own plans because merging them would raise their
review gate for nothing. Sequencing is stated here so there is a single artifact
to start from.

| # | Proposal | Executed in | Plan tier | Depends on |
|---|---|---|---|---|
| 1 | `corpus-tier-cost` | `dev/plans/corpus-tier-cost.md` | Internal | nothing — **runnable now** |
| 2 | `review-efficient-lifecycle` | **this plan**, P1--P8 | External + Ext. Security | — |
| 3 | `claim-check-exemption-hygiene` | **this plan**, D | External + Ext. Security | A |
| 4 | `code-review-blindness` | **this plan**, B, C | External + Ext. Security | A |
| 5 | `lifecycle-status-vocabulary` | **this plan**, A, E, F | External + Ext. Security | A |
| 6 | `git-native-security-foundations` | `dev/plans/git-native-security-foundations.md` | External + Ext. Security Review | independent trust root |

**Why 1 and 6 are not merged in.** `corpus-tier-cost` is `required(Internal)`
test infrastructure; folding it here would subject a fifteen-line memo change
to an External Security Review it does not need, and would trap the engine
suite's runtime fix behind this plan's gate. That risk is not hypothetical —
this plan took nine review rounds to reach its first implementation commit, and
the suite meanwhile runs **438s** (measured 2026-08-10, 2,785 nodes).
`git-native-security-foundations` changes the local trust root, the gate
manifest schema, and release verification; its Security reviewer should read
that diff, not a lifecycle refactor's.

**Start order.**

1. **`corpus-tier-cost` first and in parallel with everything.** It is
   accepted, unblocked (`transition-lint` archived), Internal-tier, and it is
   the only one of the six that makes every other chunk's Boundary A cheaper.
2. **This plan's Chunk A**, once both obligations carry a clearing pass. A is
   the single vocabulary source every later chunk consumes.
3. **B--H in the order in `## Sequence`**, then B1 / Code review / re-anchor /
   B2.
4. **`git-native-security-foundations`** whenever its own reviews clear; it
   shares no surface with this plan and is not gated on it.

Nothing here reaches into a sibling plan's contract. This table is a map, not
an authority: each plan keeps its own scope, gates, and archive.

## Proposed paths

Proposed paths:
- `bootstrap/tests/test_lifecycle_vocabulary.py` — Chunk A's source-audit + shape-(b) matrix.
- `scripts/gen_legacy_code_review_passes.py` — Chunk C's legacy manifest generator.
- `bootstrap/tests/test_lifecycle_board.py` — Chunk F's board CLI and encoder tests.
- `dev/measurement/pilot-activation.md` — P6a's immutable activation record; introduced by P6d.
- `dev/measurement/pilot-events.md` — P6a's append-only event ledger; counts and pauses are derived from it.
- `dev/plans/corpus-tier-cost.md` — sibling plan for proposal 1; opened alongside this one.
- `dev/plans/git-native-security-foundations.md` — sibling plan for proposal 6; opens when its reviews clear.

## Scope

The four accepted contracts, implemented once over one shared surface. The
opened plan claimed this and mapped only the three amendments; the parent's own
machinery — assurance paths, the review basis, plan-readiness inheritance, the
withdrawal ledger, the non-expansion attestation, `review-brief`, `closeout`,
and the bounded pilot — had no chunk. Verified 2026-08-10: **zero** files under
`tools/`, `scripts/`, `bootstrap/tests/`, or `templates/skills/` contain any of
`review-brief`, `Plan readiness`, `Contract non-expansion`,
`Withdrawn / superseded`, `inherited(`, or `Assurance path`. Chunks P1--P7
below supply them.

Surfaces: `tools/lifecycle_planner.py` and its installed twin,
`tools/lifecycle.py` and its installed twin, `doctrine/dual-review.md`,
`dev/collaboration_agreement.md` and its template twin, the two
`_lifecycle_metrics/extract.py` copies, `scripts/transition_lint.py`,
`scripts/claim_check.py` and its twin, the proposal/plan authoring templates
and their `templates/core/dev/` twins, the lifecycle doctrine files,
`AGENTS.md` and its twin, `dev/agent_collaboration.md` and its twin, the
`_intent` CLI copies, and the affected tests.

**Scope fence.** Out of scope, and not deferred by this plan because each is
already homed elsewhere:

* `git-native-security-foundations` — separate trust-root plan; disjoint
  surface (gate manifest, signing, `verify-ref.sh`).
* `corpus-tier-cost` — separate `required(Internal)` plan; test infrastructure
  only, unblocked now that `transition-lint` has archived.
* The security plans open at plan-open (`api-web-security-modules`,
  `release-security-bar`, `security-verification-activation`) — **archived
  before this plan implements**, per the Maintainer's 2026-08-10 statement that
  they are finishing now. This replaces an earlier disjointness figure ("92
  files across their chunk tables, zero naming any surface above") that is
  withdrawn: the scan behind it matched one chunk-table row format and
  under-read `release-security-bar`, a plan with chunks A--M, to two files. A
  sequencing condition the Maintainer controls is a better fence than a
  measurement I could not stand behind.
(The opened plan fenced `[F1]` as "pending Revision 4". That was stale on
arrival: Revision 4 was accepted at `27f1927`, 48 minutes before this plan
opened. The accepted rule is now transcribed directly into Chunk F.)

### Documentation / doctrine surface

`doctrine/proposals.md`, `doctrine/plans.md`, `doctrine/lifecycle.md`,
`doctrine/lifecycle-contract.md`, `doctrine/session-routines.md`; `AGENTS.md`
and `templates/core/AGENTS.md`; `dev/agent_collaboration.md` and its
`templates/core/dev/` twin; both authoring templates and their twins;
`.agents/skills/session-start/SKILL.md` and its template; `CHANGELOG.md`.
Routed per `docs/DOCUMENTATION_PLAN.md`: governing prescription to `AGENTS.md`,
process doctrine to `doctrine/`, author instruction to the templates.

## Sequence

Dependency order, not preference. Chunks A and B touch the same four functions
every later chunk builds on, so they are strictly first.

```
A   central vocabulary + contained loaders         [commit pending]
B   canonical pass boundaries                      [commit pending]
P1  assurance paths + four-field review basis      [commit pending]
C   Code-review record schema + legacy manifest    [commit pending]
P5  Contract non-expansion attestation             [commit pending]  (binds into C)
D   claim-check archive resolution + registry      [commit pending]
E   status vocabulary, transitions, conformance    [commit pending]
P2  plan readiness, inheritance, expansion refusal [commit pending]
P3  current-contract revision + withdrawal ledger  [commit pending]
P4  review-brief + closeout --dry-run              [commit pending]
P6a pilot engine + state schema (in reviewed range)[commit pending]
P6b pilot human contract                           [commit pending]
P6c pilot mutation tests                           [commit pending]
F   the derived board                              [commit pending]
G   doctrine, templates, agent teaching            [commit pending]
H   migration + source-proposal archive            [commit pending]
--- stable bytes ---------------------------------------------------
B1  Boundary B on the pre-review commit            [record]
CR  independent Code review over that range        [review]
I   Maintainer re-anchor of the reviewed frozen set[M1]
B2  Boundary B + closeout on post-ceremony commit  [record]
--- pilot ----------------------------------------------------------
P6d pilot ACTIVATION (data-only, Maintainer-gated)  [M2]
P7  post-pilot promotion / retirement              [M6; own evidence]
```

Only *activation* is post-ceremony. The pilot engine, its state schema, its
reports and its tests (P6a--P6c) land before `H`, inside the reviewed range.
Restart cases, split rather than generalized:

1. the ceremony's **reviewed manifest-only** commit proceeds directly to `B2`;
2. any post-Code-review correction to governed implementation, test,
   executable-template or fixture bytes restarts `B1` **and** independent Code
   review;
3. any correction inside the gate inventory additionally restarts the
   Maintainer ceremony `I` (fence **M5**); and
4. P6d activation and P7 outcomes follow their own phase evidence above — they
   never inherit `B1`/`CR`/`I`/`B2` by position.

Two orderings are load-bearing and measured:

* **A before everything.** Five status vocabularies exist today
  (`_PROPOSAL_STATES`/`_PLAN_STATES` in both planner copies,
  `_PLAN_STATUS_ENUM` in both metrics copies, `_OPEN_STATUSES` in
  `transition_lint.py`). Three chunks change status semantics. Landing any of
  them before the single source exists forks the vocabulary again.
* **D before H.** Archiving the four source proposals dangles **12 path
  citations across 6 files** (measured 2026-08-10). Chunk D's exact
  active→archive resolution is what absorbs them. Archive first and the tree
  goes red for a reason Chunk D was accepted to fix.

### Chunk A — one vocabulary source, contained loaders

| # | File | Change |
|---|---|---|
| A1 | `tools/lifecycle_planner.py` | central declarations: current proposal/plan states, terminal vs non-terminal, legal transitions, historical tokens (migration + metrics only), and the added-artifact set shape (b) consumes |
| A2 | `templates/skills/_lib/lifecycle_planner.py` | byte-identical twin |
| A3 | `tools/_lifecycle_metrics/extract.py` | drop `_PLAN_STATUS_ENUM`; closes the pre-existing `awaiting-plan-review` omission. Loads the planner under the **complete accepted R5 contract**: fixed `spec_from_file_location` under a private module name; path derived from its own resolved location; **no ambient `sys.path`**; refusal on missing/unreadable, leaf symlink, containing-directory symlink, or out-of-root resolution; sentinel-gated caching of a *fully initialized* module only; a poisoned `sys.modules` entry refused or replaced only after the same identity checks; removal of the private module **and every child it registered** after any execution failure, with a clean retry; import causes no CLI action or repository mutation; every validation `OSError` is a clean refusal, never a traceback or a fallback |
| A4 | `templates/modules/default-on/_lifecycle_metrics/extract.py` | byte-identical twin; refuses at its source-tree location (no sibling planner there) |
| A5 | `scripts/transition_lint.py` | drop `_OPEN_STATUSES`; consume the central added-artifact set; unknown status becomes an advisory finding, never silent skip. Loads the planner under the **identical A3 contract**, stated per-consumer rather than inherited by implication |
| A6 | `bootstrap/tests/test_lifecycle_vocabulary.py` | source audit rejecting any consumer-local status literal; shape-(b) synthetic matrix over every central state; and **per consumer**: missing path, unreadable path, symlinked leaf, symlinked parent, out-of-root resolution, poisoned-cache entry, partial-child cleanup then successful retry, no-`sys.path` (probed with a decoy planner on the path), no-`tools/__init__.py` shortcut, and absence of import side effects. Plus the three metrics-location cases |
| A7 | `bootstrap/tests/test_transition_lint.py` | extend for the new opening states |

**Tier: Opus.** Contract authorship plus loader containment; no mechanical
oracle for "is this the right vocabulary boundary."

### Chunk B — canonical pass boundaries

**Pre-landed baseline — `286f07d`, and this chunk does not re-open it.** The
group-Response rule shipped at the Maintainer's explicit direction *before* this
plan reached `executing`: an exact `## Response to plan review` discharges the
group of Plan-review passes above it and after the previous Response. An earlier
draft of B2 required the **opposite** — "a disposition after the later pass must
not satisfy the earlier" — which the landed code contradicts by construction. An
implementer following that sentence would have restored the false ceiling the
Maintainer had just directed away. The split below is the fix.

**The two record types need opposite rules, and that is deliberate.** They are
not the same problem: a Plan review is answered as a *round*, so grouping is
correct; a Code review's findings are answered *individually*, so the accepted
`code-review-blindness` amendment requires exact `Answers:` binding. Collapsing
them into one generic "disposition after later pass" assertion is what produced
the conflict.

| # | File | Change |
|---|---|---|
| B1 | `tools/lifecycle_planner.py` + twin | build every selected pass body **and** every next-pass ceiling from one ordered set of raw conforming boundaries of both kinds, unioned with H1/H2. Raw conforming boundaries stay canonical for every pass ***body***, both record types — this half is unchanged and is orthogonal to disposition |
| B2 | same | **Plan-review disposition — the landed group rule, preserved.** An exact `## Response to plan review` after a pass discharges it; `### Sharpening` stays scoped to its own pass. No re-derivation: B2 pins `286f07d`'s behavior, it does not redesign it |
| B3 | same | **Code-review disposition — exact `Answers:` binding**, per the accepted `code-review-blindness` R2/R4. A Response bound to a later pass must **not** satisfy an earlier one; malformed, ambiguous, absent, or wrong-pass bindings refuse |
| B4 | `bootstrap/tests/test_lifecycle_contract.py` | the body mutation (a later pass's `**Tier**`/`**Findings**` must not enter the earlier body) **plus two opposing disposition mutations**, so weakening either side reddens **independently**: make Plan-review disposition positional again → the group node reddens; make Code-review disposition grouped or positional → the `Answers:`-binding node reddens |

**Why B4 is four mutations and not one.** A single generic assertion cannot
cover two rules that point in opposite directions — it would necessarily be
wrong about one of them, which is exactly how the conflict arose. Each direction
gets its own falsifier so that a future implementer cannot satisfy the suite by
weakening one rule toward the other.

**Tier: Opus.** Reproduced red today — a later unparseable S1 heading has its
attestation lines swallowed and reported as the earlier pass's duplicates.
Subtle, and the failure is silent.

### Chunk C — Code-review record schema

| # | File | Change |
|---|---|---|
| C1 | `tools/lifecycle_planner.py` + twin | fold Code-review evaluation into `review_record_violations` (already "the one predicate (S12)"); **delete** the archived arm's `_has_kind(art, "Code review")` presence test and its mirror |
| C2 | same | heading + pass boundary, mandatory fields inheriting the parent's four-field review basis, clearing/blocking verdict vocabulary, latest-applicable-round rule, `Answers:` binding grammar |
| C3 | `scripts/gen_legacy_code_review_passes.py` | generator over a named baseline commit |
| C4 | `tools/lifecycle_planner.py` + twin | committed legacy enumeration, `stem -> {digest: count}`, authored independently of C3 |
| C5 | `bootstrap/tests/test_lifecycle_contract.py` | schema, verdict classes, ordering ties, `Answers:` refusals, legacy replay refusal |

**Tier: mixed.** C2 and C4 Opus (schema authorship; the enumeration must be
reviewed independently of its generator). C3 and C5 **Sonnet** — the generator
regenerating byte-identically is its own oracle.

### Chunk D — claim-check archive resolution, registry, liveness

| # | File | Change |
|---|---|---|
| D1 | `scripts/claim_check.py` | exact `dev/{proposals,plans}/<file>.md` → `.../archive/<file>.md` resolution; direct path authoritative; line bounds checked against the archived file |
| D2 | `templates/modules/default-on/claim_check.py` | byte-identical twin |
| D3 | `scripts/claim_check.py` + twin | typed declarations become a document registry of literal paths; every exemption reported with the declaration that authorized it |
| D4 | `scripts/claim_check.py` + twin | liveness on active artifacts; archived grandfathered; a glob rendered redundant **by D1** reports as a migration item, not a hard finding, for one deprecation window |
| D5 | `bootstrap/tests/test_claim_check_module.py` | typo/family/location mutations; the path-limited historical predicate for the dropped prefix; registry exactness; liveness |

**Tier: Sonnet for D1/D2/D5, Opus for D3/D4.** D1 is an exact rule with a
strong oracle. D4 carries the Section-1/Section-3 tension the round-1 review
measured (7 of 42 live globs) and needs judgment about the deprecation window.

### Chunk E — status vocabulary and conformance

| # | File | Change |
|---|---|---|
| E1 | `tools/lifecycle_planner.py` + twin | proposal and plan state tables, legal transitions, multi-obligation `**Obligation**:` matching, `**Blocked by**` as non-authoritative metadata |
| E2 | same | the R6 contradiction predicates, shared by `scan`, `next`, and closeout |
| E3 | `bootstrap/tests/test_lifecycle_contract.py` | every legal transition, both revision loops, fast-path opening, no-op status under an incomplete floor, every contradiction through both entry points |

**Tier: Opus.** Contract, and the multi-obligation rule resolves a question the
record left open.

### Chunk F — the derived board

| # | File | Change |
|---|---|---|
| F1 | `tools/lifecycle_planner.py` + twin | `board` subcommand: compact rows, `--format json`, filters, `--explain` |
| F2 | same | terminal encoder, accepted rule verbatim: escape to printable ASCII when (1) `str.isprintable()` is false, (2) the code point is in the planner's `_DISPLAY_UNSAFE_RANGES`, or (3) it is a row/field delimiter, backslash, or syntax character. `_DISPLAY_UNSAFE_RANGES` uses **numeric endpoints only** — no invisible source character embedded raw |
| F3 | `tools/_intent/cli.py` + `templates/modules/team-gated/_intent/cli.py` | versioned `--format json` for `list` only, deterministic and ASCII-safe; existing human output, claim/release semantics, conflict rules, log schema, hooks, and activation unchanged |
| F4 | `tools/lifecycle_planner.py` + twin | optional intent provider, complete accepted contract: **one** bounded query for the whole board; launcher must be a regular, non-symlinked sibling whose resolved parent **is** the expected `tools/` directory; invoked with the running interpreter in **isolated mode, no shell**, under a timeout; versioned JSON only, never scraped human output; complete field, type and path validation of **every** record before **any** is used. Distinct handling for non-zero exit, timeout, malformed JSON, duplicate claim ids, invalid paths, and schema-version mismatch. Missing launcher is `not-installed`; present-but-invalid is `error`, renders no claim authoritative, keeps other safe rows visible, and exits non-zero |
| F5 | `bootstrap/tests/test_lifecycle_board.py` | rows, ordering, filters, injection; provider tests asserting **exactly one** subprocess per board, exact argv including isolated mode, no shell, timeout enforcement, symlink and parent refusal, deterministic JSON, and no human-output parsing, each failure mode distinct; **directional drift test** expanding every member of content scan's `_ZERO_WIDTH`, `_BIDI`, `_LINE_SEPARATORS` and every code point of `_IGNORABLE_RANGES`, `_NONCHARACTER_RANGES`, `_TAG_RANGE`, `_ASCII_GUARD` and asserting each is escaped; plus a source scan proving no represented invisible is embedded raw |

**Tier: Sonnet for F1/F3/F5, Opus for F2/F4.** The renderer and filters are
oracle-rich. The encoder rule and provider containment are not — F4 crosses a
module boundary. The coupling is deliberately **one-way**: the board may escape
more than the scanner flags, but may never emit raw a code point the scanner
recognizes, so a newly added printable invisible fails F5 until the range table
follows it. Narrowing a detector cannot silently weaken terminal output.

### Chunk G — doctrine, templates, agent teaching

| # | File | Change |
|---|---|---|
| G1 | `doctrine/proposals.md`, `doctrine/plans.md`, `doctrine/lifecycle.md`, `doctrine/lifecycle-contract.md`, `doctrine/session-routines.md` | the governing contracts |
| G2 | `AGENTS.md` + `templates/core/AGENTS.md` | operational summary; board in session-start orientation |
| G3 | both authoring templates + `templates/core/dev/` twins | author instruction; registry form; remove the inert `cairn-internal-ref-allow` headers from the self-hosted copies only |
| G4 | `dev/agent_collaboration.md` + twin, both `session-start/SKILL.md` copies | routing: run the board, choose the row, then read that artifact |
| G5 | `CHANGELOG.md > Unreleased` | one release note for the cluster |

**Tier: Sonnet.** Mechanical prose against a contract fixed by A–F. Every claim
is checkable by `check_cairn` and `claim_check`.

### Chunk H — migration and source-proposal archive

| # | File | Change |
|---|---|---|
| H1 | active proposals and plans | **dry-run inventory first**, bound to the pinned parent, carrying for each artifact its old blob id, proposed status, evidence basis, and metadata disposition. A reviewer **independent of the inventory generator** admits the exact table by digest before any apply; ambiguity stays refusal. Apply only admitted rows whose blobs still match |
| H2 | active proposals and plans | exemption-metadata migration: inert headers out, unused globs out, live globs to typed declarations. **Lands atomically with D1--D4** so no suppression disappears before archive resolution and typed declarations govern |
| H3 | `dev/proposals/*.md` → `archive/` | the four source proposals, after D1 is in the tree |
| H4 | `dev/PLANNING.md` | row-move for the four |

**Tier: Sonnet to generate the inventory; a reviewer independent of that
generator admits it.** The mechanics are pinned and blob-checked; classifying
an ambiguous artifact is judgment. **Lifecycle transitions that rely on
migrated values are frozen until H's commit is inside clearing Code review** —
a mistaken `ready-to-archive` or `ready-to-implement` changes permitted work
immediately. Tests mutate table rows, digests, evidence and blobs, and prove
partial or racing application cannot grant authority.

**H runs last and needs a quiet tree.** It rewrites the `Status:` of every
active artifact, so concurrent lifecycle commits cause blob-mismatch
re-derivation. Under the sequencing condition in Scope the security plans are
already archived when this plan implements, so the quiet tree is a
precondition to check at H, not a wait to schedule.

### Chunks P1--P7 — the parent contract

The accepted parent's machinery, which the opened plan omitted. One plan; these
are chunks, not another planning artifact.

| # | Surface | Change |
|---|---|---|
| P1 | `tools/lifecycle_planner.py` + twin, both authoring templates + twins | `Assurance path: standard \| high-assurance` declaration, the mandatory high-assurance trigger set, and the four-field review basis (`Reviewed commit`, `Target`, `Prior findings`, `Assurance path`) required across proposal, plan, and Code-review records |
| P2 | same, plus `doctrine/dual-review.md` | proposal `Plan readiness: READY \| DISTINCT REVIEW REQUIRED`, exact accepted-commit binding, standard-plan inheritance, expansion invalidation, and the high-assurance refusal. **Semantic triggers are author declarations, not inferences**: scientific-assumption and undeclared cross-surface risk are declared by the author and surfaced to proposal review and `review-brief`; the tooling checks that the record exists and binds, never the truth of the classification |
| P3 | both authoring templates + twins, planner predicates | complete current-contract revision plus its mandatory `Withdrawn / superseded commitments` ledger |
| P4 | `tools/lifecycle.py` + installed twin | deterministic `review-brief`; expanded `closeout --dry-run`. **Fenced**: P4 does not modify `_resolve_interpreter` (`tools/lifecycle.py:414`), its schema, validation order, fallback disposition, warning visibility, or any subprocess use of the resolved path — the protected local interpreter binding named in `AGENTS.md`. Pinned by a focused exact-function-byte / AST sentinel test. If implementation needs such a change, **stop for a new Security Review** (fence **M3**). Both commands stay read-only and execute no artifact content; human output passes through the **same** terminal encoder as F2. **The planner owns it**: the encoder lives in `tools/lifecycle_planner.py` (and its installed twin), and `tools/lifecycle.py` reaches it by the **same A3 contained-loader contract** — fixed `spec_from_file_location`, no ambient `sys.path`, no `tools/__init__.py`, no CLI import with side effects. This adds no install-manifest row: both files already install as siblings under `tools/`. The existing `_safe_field` (`tools/lifecycle.py:113`) is **not** this rule — it translates a fixed escape table and truncates; it applies neither `str.isprintable()` nor `_DISPLAY_UNSAFE_RANGES` — and is replaced, not wrapped. Machine output is versioned ASCII-safe JSON. Control-character, invisible-range, delimiter, malformed-record and mutation-sentinel tests, **plus the full A6 loader matrix for this second consumer** (decoy path, leaf and parent symlink, out-of-root, partial-import cleanup, clean retry) and byte/parity checks for every installed twin |
| P5 | planner + `bootstrap/tests/test_lifecycle_contract.py` | the bound `Contract non-expansion: VERIFIED \| NOT VERIFIED` attestation with its `Basis:` line; `NOT VERIFIED` blocks. Validates presence and binding shape only — the parent is explicit that the semantic claim stays human |
| P6a | `tools/lifecycle.py` + twin, `dev/measurement/pilot-activation.md`, `dev/measurement/pilot-events.md` | **pilot engine, inside the reviewed range**, split so no authority input is a mutable last-writer-wins file. (1) An **immutable tracked activation record** naming `machinery_sha` = the reviewed **B2** commit; the *enabling* commit is derived from Git as the commit that first introduced this exact record, so nothing is self-referential, and `activation_date` is that commit's author date. (2) An **append-only tracked event ledger** — one event per counted plan stem or pause, each bound to its source artifact and commit — from which counts, pauses, and the report are **derived**, never stored. Six-plan rule = distinct plan stems reaching `ready-to-archive` under the contract; 60-day window from the derived activation date inclusive. Every writer: repository containment, regular non-symlink leaf **and** parent, closed bounded schema, atomic replace-or-append with an expected-old check, clean refusal on race or `OSError`. Malformed or unknown-version **refuses**; it never defaults to inactive |
| P6b | `dev/collaboration_agreement.md` + twin | the pilot's human contract: pause conditions, evidence report shape, and a description of the Maintainer promotion Decision at the boundary. **Agent-authored**, inside the reviewed range — describing the Decision is not taking it; the Decision itself is M6 |
| P6c | `bootstrap/tests/test_lifecycle_contract.py` | pilot mutations: absent record, wrong schema version, altered prior event, duplicate or conflicting stem, symlink redirection of leaf or parent, interrupted write, stale writer / lost update, boundary-day arithmetic, pause set and cleared, and the exact activation-binding oracle (a record whose `machinery_sha` is not the B2 commit, and a derived-enabling-commit mismatch, both refuse) |
| P6d | `dev/measurement/pilot-activation.md` | **activation only (M2)** — the data-only, Maintainer-gated commit introducing the immutable activation record after B2, enabling already-reviewed machinery. No code lands at activation |
| P7 | `doctrine/`, both authoring templates + twins, `docs/workflow-role.md`, `docs/getting-started.md`, `docs/tool-usage.md`, `templates/skills/_lib/` | **conditional** post-pilot `promote` / `revise` / `retire`, each with distinct behavior, plus the three-layer canonical / self-hosted / shipped-template parity contract. Executes only after the Maintainer's promotion Decision (M6) |
| P8 | `bootstrap/tests/test_lifecycle_contract.py` | end-to-end standard-READY and high-assurance-refusal fixtures, plus a **row-level assurance matrix**: missing / duplicate / unknown `Assurance path` values (all refuse — **never default to `standard`**); every mechanically recognizable protected-surface trigger; uncertainty resolving **high**; high-assurance and `DISTINCT REVIEW REQUIRED` inheritance refusal; changed proposal / review / Decision SHAs; every named expansion dimension; unresolved findings; stale Boundary B; malformed or missing non-expansion `Basis:`; and a downgrade admitted only through a structurally valid Maintainer Decision |

**Tier: Opus for P1--P3, P5 and P6a** (contract authorship on records every
future artifact inherits, plus the pilot state schema). **Sonnet for P4, P6c
and P8** (CLI surface, mutations and fixtures against a fixed contract, all
oracle-rich). **P6d and P7 are Maintainer-gated (M2, M6); P6b is not** — see `## Maintainer interventions`, which is the only authoritative list.

**Phase separation, inside this plan.** P6a--P6c ship *before* H/B1, so the
pilot capability is inside the reviewed range and carries the plan's Code
review and stable evidence. P6d is data-only activation after B2. **P7 carries
its own evidence**: before it executes it produces an exact changed-path
manifest, runs the gate-manifest classification over it, and then — if it
changes any executable, test, template or fixture byte — takes a fresh
Boundary B and an independent Code review, and if it changes a frozen path,
another Maintainer ceremony. P7 is not assumed docs-only.

### Chunk I — Maintainer re-anchor  *(fence **M1**)*

Per `lifecycle-status-vocabulary` R8: after every executable, test, template
and frozen byte across A–H is stable **and** the single code review has landed,
the **Maintainer** performs `bootstrap/REANCHOR_RUNBOOK.md` once for the whole
batch. No agent performs or absorbs this. Two changed paths are manifest-pinned
(`bootstrap/tests/test_lifecycle_contract.py`,
`templates/modules/default-on/_lifecycle_metrics/extract.py`); two are
discovered `FROZEN-NEW` (`scripts/transition_lint.py` and its test) and become
pinned at that ceremony. The plan re-measures that inventory at its
implementation parent rather than carrying these figures forward.

## Acceptance criteria

* **Tests** — the Chunk A–F nodes named above, plus the standing gates for
  every touched surface. Unknown or uncertain scope falls back to the full
  suite.
* **Docs** — Chunk G's surfaces, each confirmed updated rather than assumed;
  drift gates catch drift, not absence.
* **Examples / smoke** — `lifecycle_planner.py scan`, `next`, and `board` over
  the migrated tree; `python scripts/check_cairn.py`; `claim_check` over every
  changed Markdown surface.
* **Twin parity** — `cmp` clean for every source/template pair this plan
  touches, asserted in the same commit that changes either side.
* **No consumer-local status literal survives** — Chunk A's source audit is the
  enforcer, and it must be observed red against a deliberately reintroduced
  local enum.

### Author-accounting — invariants, failure modes, edge cases

* **Invariant** — exactly one runtime status vocabulary. *Enforced by* A6's
  source audit, mutation-verified.
* **Invariant** — shape (b) fires for every current non-terminal opening state.
  *Enforced by* A6's synthetic matrix. Corpus tests are complementary and are
  **not** the oracle: the pinned corpus contains no new token, so it cannot
  witness this class.
* **Invariant** — a blocking latest Code review refuses archive. *Enforced by*
  C5, with the two historical answered-blocking cases admitted only through
  C4's enumeration.
* **Failure mode — provider absent or broken.** *Open, and labelled.*
  `not-installed`/`error` never render as "no claim".
* **Failure mode — migration races a concurrent commit.** *Closed.* Blob
  mismatch skips and re-derives.
* **Failure mode — a chunk lands out of order.** *Open, and the reason A and D
  are pinned first.*
* **Public-path → test mapping** — `scan` / `next` / `board` →
  [`bootstrap/tests/test_lifecycle_contract.py`](../../bootstrap/tests/test_lifecycle_contract.py);
  `claim_check` →
  [`bootstrap/tests/test_claim_check_module.py`](../../bootstrap/tests/test_claim_check_module.py);
  installed twins →
  [`bootstrap/tests/test_reference_scripts.py`](../../bootstrap/tests/test_reference_scripts.py).
* **Known omissions** — the tier assignments are a starting allocation, not a
  contract; a chunk that resists its assigned tier moves up rather than
  shipping weakly. No claim is made that model tier predicts correctness — the
  routing rule is oracle availability, and every farmed chunk returns the
  command and its raw output rather than a summary.

## Verification

* Boundary A per chunk: the tests named in that chunk's table, plus standing
  gates for its touched surfaces.
* Boundary B **twice**, same command pair each time — `python -m pytest
  bootstrap/tests --quality-gate-shuffle-seed=0` then `python
  scripts/quality_gate.py --sub neutrality --sub redundancy`, canonical
  interpreter, clean commit — recorded as two dated
  `## Implementation verification` sections:
  1. **B1**, on the stable pre-review commit after Chunk H;
  2. **B2**, on the post-ceremony commit after Chunk I, because the re-anchor
     rewrites `bootstrap/tests/fixtures/gate_manifest.json` inside the reviewed
     range and the runbook itself runs the suite zero times.
* Boundary C: one code review over the B1 range — **and that range must begin
  at or before `286f07d`**, not at this plan's first implementation commit.
  `286f07d` landed before the `executing` transition, but Chunk B now *depends*
  on it: B2 pins its behavior rather than deriving it. A reviewed range that
  starts after it would leave the gate change this plan relies on outside the
  only independent review it ever gets. Name the commit explicitly in **both**
  Boundary B ledgers.

  **Use the exact union, not one contiguous range** — the reading External
  round 7 supplied, adopted here so a later implementer does not have to
  re-derive it:

  ```
  286f07d^..286f07d        the pre-landed gate repair
  <first impl>..<B1>       this plan's own implementation range
  ```

  A single contiguous `286f07d^..<B1>` is also correct, but it drags in **34
  unrelated intervening commits** and spends reviewer attention without adding
  a byte of coverage. Both exact ranges are reviewed in the plan's **one**
  Boundary C pass — this is a targeting decision, not a second review.
* **Restart rule — canonical text lives in `## Sequence` and is not restated
  here.** This section previously carried an unqualified summary ("a corrective
  byte after the ceremony restarts B2 only") that contradicted it and would have
  let a governed correction bypass B1, Code review, and possibly the ceremony.
  One rule, one home. A summary that can drift is how the weaker reading
  survives; Chunk G's acceptance includes a check that no second restart rule
  exists anywhere in this plan.

**Note on doc gates**: drift gates catch drift, not absence. Chunk G's
deliverables are confirmed individually.

<!-- Each plan-review pass is its own dated H2 section appended below:

       ## Plan review -- <reviewer> -- YYYY-MM-DD

       **Tier**: <External|External Security Review>
       **Obligation**: <the exact clause from `Plan review:` this pass discharges>
       **Findings**: <none|raised>

     Two passes are required and one pass cannot discharge both clauses. -->

## Code review

*Filled in after implementation commits land.* One pass over the stable range.

## Lasting-truth migration

*Filled in at archive time.* Per the archive precondition, every deferred
follow-up carries a recorded disposition — `accept`, `guard`, `wontfix`, or
(with the Maintainer's quoted authorization) `defer`.

## Plan review -- Codex -- 2026-08-10

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External
**Reviewed commit**: `777dea04c653f4a918692d94908ed381666d1348`
**Target**: the complete opened plan against all four accepted source
contracts
**Assurance path**: high-assurance
**Findings**: raised
**Verdict: REVISE.** The consolidation boundary is right, and it must remain
one plan. The current executable contract, however, implements the three
amendments while omitting most of the parent proposal, and its one-Boundary-B
budget conflicts with both the accepted trust-ceremony order and the parent's
bounded pilot. Restore those contracts inside this plan; do not split or
de-scope them.

### Steelman

The dependency ordering among the work that is present is strong. A central
vocabulary before its consumers, canonical pass boundaries before the new
Code-review grammar, archive resolution before source-proposal moves, and a
quiet-tree migration are all defensible. The plan also correctly keeps the two
review obligations distinct and places the re-anchor behind stable frozen
bytes and independent Code review.

I reproduced the stated vocabulary drift: the planner and its twin each carry
`_PROPOSAL_STATES` and `_PLAN_STATES`, both metrics copies carry
`_PLAN_STATUS_ENUM`, and transition-lint carries `_OPEN_STATUSES`. I also ran
the current planner over the tree: all 10 active artifacts were structurally
sound, and this plan's next transition was reported as
`awaiting-plan-review`. These checks support Chunks A and E; they do not supply
the omitted parent machinery below.

### [E1] HIGH -- the plan does not implement its primary source proposal

The Scope says all four accepted contracts are implemented once, but A--I map
the three amendments: vocabulary/board, Code-review blindness, and claim-check
exemption hygiene. The accepted complete contract in
`review-efficient-lifecycle` also requires all of the following, none of which
has a chunk or acceptance row here:

* `standard` / `high-assurance` declaration and the mandatory high-assurance
  trigger set;
* the four-field review basis (`Reviewed commit`, `Target`, `Prior findings`,
  `Assurance path`) across proposal, plan, and Code-review records;
* complete current-contract revisions and their mandatory
  `Withdrawn / superseded commitments` ledger;
* proposal `Plan readiness: READY | DISTINCT REVIEW REQUIRED`, exact accepted
  commit binding, standard-plan inheritance, expansion invalidation, and the
  high-assurance refusal;
* the bound `Contract non-expansion` Code-review attestation;
* deterministic `review-brief` and expanded `closeout --dry-run` output;
* the Cairn-local pilot, its six-plan / 60-day deadline, pause conditions,
  evidence report, and Maintainer promotion Decision; and
* the explicit post-pilot promotion chunk and three-layer canonical,
  self-hosted, and shipped-template parity contract.

This is not already implemented. A repository search found no `review-brief`,
`Plan readiness`, `inherited(...)`, `Contract non-expansion`, or
`Withdrawn / superseded commitments` mechanism in the lifecycle tools or their
tests. The plan itself contains none of those terms beyond its source link.

**Required satisfier.** Keep one plan and add executable chunks, paths,
acceptance criteria, tests, and doctrine/template surfaces for every item
above. In particular include `doctrine/dual-review.md`,
`dev/collaboration_agreement.md` and its template twin, the lifecycle CLI and
its installed twin, end-to-end standard-READY and high-assurance-refusal
fixtures, pilot activation/reporting state, and the accepted post-pilot docs
surfaces. Name what lands before the pilot, what remains dormant during it,
what the Maintainer decides at its boundary, and what the conditional
promotion/retirement chunk does. A source-proposal link is not an executable
mapping.

### [E2] HIGH -- the evidence budget runs Boundary B before a fixture-changing ceremony, contrary to the accepted order

The plan budgets one Boundary B after H, then one Code review, then Chunk I's
re-anchor. That ceremony changes `bootstrap/tests/fixtures/gate_manifest.json`,
which is a fixture in the reviewed range. Current doctrine says a later fixture
change requires replacement Boundary B evidence. More directly, accepted
`lifecycle-status-vocabulary` R8 orders independent Code review, Maintainer
re-anchor, and then **final Boundary B and closeout checks against the
post-ceremony commit**.

I opened the re-anchor runbook rather than treating its path as a trigger. Its
promotion performs gate/static verification; it does not run the canonical
project suite or the standing integration commands. The ceremony therefore
does not supply the missing post-ceremony Boundary B.

**Required satisfier.** Preserve the accepted order explicitly:

1. stable implementation bytes and pre-review Boundary B evidence;
2. independent Code review over that exact range;
3. Maintainer re-anchor of the reviewed frozen set; and
4. a fresh full integration record plus closeout checks on the post-ceremony
   commit.

State how a failure or corrective byte restarts the applicable evidence,
review, and ceremony legs. Update the touchpoint arithmetic rather than calling
two broad executions one. Then reconcile this sequence with [E1]'s pilot and
conditional promotion phase; the accepted experiment may require a second
stable review boundary inside this same plan.

### [E3] MEDIUM -- this plan bootstraps the two-obligation gate it relies on without recording the bootstrap

The header correctly requires two distinct passes and forbids implementation
before both. The current planner does not yet implement `**Obligation**:` or
multi-obligation discharge: it normalizes `required(External + External
Security Review)` to the first `External` tier. Once the author dispositions
this pass, current tooling can report the ordinary External floor satisfied
even though the Security Review has not landed. Chunk E is what eventually
closes that gap.

**Required satisfier.** Add a one-time pre-Chunk-A bootstrap attestation that
names the two distinct review commits, their exact obligations, their clearing
dispositions, and the absence of unresolved findings. Keep the plan at `open`
until both exist. State that this manual attestation is retired once Chunk E's
multi-obligation predicate is active and tested. This adds no review pass; it
makes the already-declared two passes enforceable during their own bootstrap.

### [E4] MEDIUM -- Chunk F points at the accepted encoder but does not carry its decisive oracle

The Scope fence says lifecycle-status-vocabulary [F1] is pending even though
Revision 4 was accepted before this plan opened. F2 now points to Revision 4,
but F5 says only `encoder sweep`; it does not bind the final rule or the test
population that made Revision 4 acceptable.

**Required satisfier.** Remove the stale pending fence and put the accepted
rule directly in F2/F5: `not str.isprintable()` plus numeric
`_DISPLAY_UNSAFE_RANGES`; the directional assertion over every member of
`_ZERO_WIDTH`, `_BIDI`, `_LINE_SEPARATORS`, every code point in
`_IGNORABLE_RANGES` and `_NONCHARACTER_RANGES`, `_TAG_RANGE`, and
`_ASCII_GUARD`; twin parity; and a source scan proving no represented invisible
is embedded raw. This is contract transcription, not new scope.

### Scope ruling and next pass

No de-scoping is recommended. Do not move the parent mechanism, pilot,
promotion phase, or any amendment into another plan. Revise the operative
chunks inline while status remains `open`, append the finding dispositions,
and return for a focused External closure read against E1--E4. The distinct
External Security Review remains separately owed and should review the
sharpened complete plan, especially loader/provider containment, terminal
encoding, migration authority, and trust-ceremony sequencing.

**Covered by execution/inspection**: current lifecycle `scan` and `next`;
runtime vocabulary declarations across all five named source surfaces; absence
of the parent mechanism in tools/tests; accepted parent Revision 1; accepted
lifecycle-status Revision 4 and R8; current Boundary B/C doctrine; the actual
re-anchor runbook's triggers; and the complete plan at `777dea0`.

**Not covered**: no implementation exists, so no proposed parser, board,
provider, migration, review-brief, pilot, or closeout behavior could be
executed. I did not independently rederive the plan's 92-file disjointness or
12-citation migration counts; neither affects this verdict and both must be
re-measured at the implementation parent as the plan already requires for
other corpus figures. This pass discharges only the `External` obligation, not
the distinct `External Security Review` obligation.

## Response to plan review -- Claude -- 2026-08-10

**Model**: claude-opus-5 (Claude Opus 5)
**Reviewed review commit**: `8f37a9b98748e0ebe239cc2944d3195e3bf93702`
**Obligation answered**: `External` (the `External Security Review` obligation
remains separately owed)
**Disposition**: accept [E1]--[E4]. Each was verified by execution before
adoption; all four reproduced. Chunks are revised inline, the plan stays
`open`.

### [E1] -- accept. The Scope sentence was false and I wrote it.

The plan said "the four accepted contracts, implemented once" and then mapped
three. Verified:

```text
review-brief            files=0
Plan readiness          files=0
Contract non-expansion  files=0
Withdrawn / superseded  files=0
inherited(              files=0
Assurance path          files=0
      (tools/, scripts/, bootstrap/tests/, templates/skills/)
```

Not one of the parent's six named mechanisms exists anywhere in the tools or
their tests, and none had a chunk here. Added as **P1--P8**: assurance paths
and the four-field review basis; plan readiness, inheritance, and expansion
refusal; the current-contract revision plus its withdrawal ledger;
`review-brief` and `closeout --dry-run`; the bound `Contract non-expansion`
attestation; the pilot with its six-plan / 60-day deadline and pause
conditions; the conditional post-pilot promotion and three-layer parity
contract; and the end-to-end READY / high-assurance-refusal fixtures. Surfaces
added to Scope: `tools/lifecycle.py` and its twin, `doctrine/dual-review.md`,
`dev/collaboration_agreement.md` and its twin.

The ruling to keep one plan is followed exactly — these are chunks, not a
second planning artifact.

### [E2] -- accept. I cited the order in Chunk I and then budgeted against it.

Verified: `bootstrap/REANCHOR_RUNBOOK.md:263` (and again at line 273) writes
`bootstrap/tests/fixtures/gate_manifest.json`, a fixture inside the reviewed
range, and the runbook contains **zero** occurrences of `pytest
bootstrap/tests`. The accepted `lifecycle-status-vocabulary` R8 orders the
Maintainer ceremony at step 5 and the final Boundary B plus closeout at step 6,
against the post-ceremony commit. My Chunk I quotes R8; my budget table
contradicted it two hundred lines earlier.

The budget now reads **Boundary B = 2**, named as two, with the sequence block
showing `B1 → CR → I → B2` and an explicit restart rule for a corrective byte
at either stage. Calling two broad executions one would have made this plan's
headline arithmetic cheaper than the contract it implements — which is the
failure it exists to prevent.

### [E3] -- accept, and the gap is worse than "not yet implemented"

Verified directly:

```text
normalize_required_tier("required(**External** + **External Security Review**)")
  -> ('external', None)
```

The second obligation is not merely unenforced; it is **silently discarded**.
Today's tooling would report the External floor satisfied by this single pass.
A new `## Bootstrap attestation` section now carries the two-row table naming
each obligation, its review commit, its disposition, and unresolved findings.
Row one is this pass; row two is pending. The plan stays `open` until both are
filled, and Chunk E retires the table in the same commit that makes its
predicate active and tested.

### [E4] -- accept. The fence was stale when I wrote it.

`lifecycle-status-vocabulary` Revision 4 was accepted at `27f1927` (13:29);
this plan opened at `777dea0` (14:17) — forty-eight minutes later. I fenced a
decision that had already landed and did not check.

The fence is removed and the accepted rule is transcribed into F2 verbatim:
escape when `str.isprintable()` is false, **or** the code point is in
`_DISPLAY_UNSAFE_RANGES`, **or** it is a row/field delimiter, backslash, or
syntax character; numeric endpoints only, no invisible embedded raw. F5 now
binds the decisive population — every member of `_ZERO_WIDTH`, `_BIDI`,
`_LINE_SEPARATORS` and every code point of `_IGNORABLE_RANGES`,
`_NONCHARACTER_RANGES`, `_TAG_RANGE`, `_ASCII_GUARD` — plus the one-way
coupling: the board may escape more than the scanner flags, never less.

### What this Response does not discharge

The **External Security Review** obligation is untouched by this pass and
remains owed. Per the review's own routing it should read the sharpened
complete plan — loader and provider containment, terminal encoding, migration
authority, and the trust-ceremony sequencing that [E2] just changed.

## Plan review -- Codex -- 2026-08-10 (round 2)

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External
**Reviewed commit**: `9e99c5a`
**Target**: the inline sharpening and Response against E1--E4
**Prior findings**: E1--E4
**Assurance path**: high-assurance
**Findings**: raised
**Verdict: REVISE, focused.** E4 closes. E1 and E2 restore the missing labels
but leave the pilot and promotion outside the reviewed/stable boundary. E3's
bootstrap table incorrectly treats an author's Response to a blocking review
as independent clearance. Keep every item in this plan and sharpen the phase
and evidence contracts below.

### [G1] HIGH -- P6/P7 sit after the only stable review boundary and are not executable chunks

P1--P5 and P8 restore most of the parent machinery before B1. P6 and P7 do
not. The sequence runs B1, Code review, re-anchor, and B2 **before** P6's pilot
activation/reporting/deadline logic and P7's promotion or retirement changes.
Those later commits therefore receive neither the plan's Code review nor its
stable integration evidence.

The rows are also not executable contracts. P6 names `pilot state` without a
path, schema, writer, reader, trigger, test home, activation commit binding, or
deadline calculation. P7 says only `doctrine + templates`; it omits the
accepted post-promotion paths `docs/workflow-role.md`,
`docs/getting-started.md`, and `docs/tool-usage.md`, and gives no verification
or archive behavior for `promote`, `revise`, or `retire`.

**Required satisfier.** Within this plan:

* put the pilot engine, state schema, report generator, pause evaluation, and
  tests before H/B1 so the capability is inside the reviewed range;
* name the data path, schema version, activation SHA/date, six-plan counting
  rule, 60-day calculation, writers, readers, malformed-state refusal, and
  mutation tests;
* make post-B2 activation a data-only, Maintainer-gated record that enables
  already-reviewed machinery;
* keep the plan open through the pilot; and
* specify the conditional post-pilot chunk completely, including all accepted
  docs/template paths, outcome-specific behavior, tests, and its own stable
  evidence and independent Code review when it changes governed bytes.

This is phase separation inside the same plan, not a new plan or de-scoping.

### [G2] HIGH -- the restart rule exempts arbitrary post-ceremony corrections from review

The new rule says, without qualification, *"A corrective byte after `I`
restarts `B2` only."* That is true only for the expected ceremony-produced gate
manifest commit when no implementation correction follows. If B2 exposes a
defect and the correction changes implementation, tests, executable templates,
fixtures, or frozen bytes, current doctrine invalidates the Code review as well
as Boundary B; frozen corrections can also invalidate the anchor just created.

**Required satisfier.** Split the cases:

* the ceremony's reviewed manifest-only commit proceeds directly to B2;
* any post-Code-review correction to governed implementation/test/template/
  fixture bytes restarts B1 and independent Code review;
* any correction in the gate inventory also restarts the Maintainer ceremony;
  and
* P6 activation and P7 outcome changes follow the phase-specific evidence from
  G1 rather than inheriting B1/CR/I/B2 by position.

### [G3] MEDIUM -- the bootstrap table self-clears the blocking External pass

The table records review commit `8f37a9b` as `REVISE -> dispositioned` with no
unresolved findings. That commit is the blocking review, not an independent
closure pass. The author Response at `9e99c5a` can disposition findings but
cannot clear its own corrections.

I reproduced the consequence against the sharpened bytes. The current parser
returns `('external', None)` for the declared two-obligation floor,
`review_record_violations(...)` returns an empty list after the Response, and
the simulated `awaiting-plan-review -> executing` gate reports the review
precondition met. The bootstrap table therefore repeats the exact
self-clearance it was introduced to prevent.

**Required satisfier.** Keep the `External` row pending until a distinct
clearing closure review commit exists; record that clearing commit, not the
earlier blocking pass. Do the same for the Security obligation. Both rows must
name `SHIP`, their exact commits, and zero unresolved findings before Chunk A.
An author Response is evidence of correction, never the clearing review.

### [G4] -- E4 closed

F2 carries the accepted `str.isprintable()` plus numeric unsafe-range rule.
F5 now expands every finite set and every range population, asserts the
directional subset, and checks source bytes for raw invisibles. The stale fence
is removed. This is the contract Revision 4 accepted.

### Coverage and next pass

**Covered by execution/inspection**: the complete `9e99c5a` diff; direct
`normalize_required_tier`, `review_record_violations`, and execution-gate
probes against the sharpened file; accepted parent pilot/promotion paths;
current Boundary B invalidation rules; the revised phase diagram; and F2/F5
against accepted Revision 4.

**Not covered**: no implementation exists, so pilot state, phase transitions,
promotion, or post-ceremony correction behavior could be executed. I did not
re-open E4's already reviewed Unicode population or the amendment contracts
outside the sharpened cells.

Return only G1--G3 for the next External closure read. This pass remains
blocking and does not fill the bootstrap table's `External` row.

## Plan review -- Codex (Security) -- 2026-08-10

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External Security Review
**Reviewed commit**: `ef70da8164d11bc2614e4b1c4f1ef70b23cd617d`
**Target**: the complete sharpened plan under a security lens
**Prior findings**: E1--E4 and G1--G4 as context; this is a distinct pass
**Assurance path**: high-assurance
**Security lens**: governance-integrity gates, executable loaders and
subprocesses, untrusted terminal data, migration authority, and trust-root
ceremony ordering
**Findings**: raised
**Verdict: REVISE.** The accepted threat posture is viable, and F2/F5's
display rule plus the two-stage ceremony sequence are directionally sound. The
plan abbreviates several accepted security controls into labels that permit a
weaker implementation, and it introduces a plan-review bypass path without the
fail-closed matrix its source proposal requires.

### Threat model and posture

The reviewed posture is trusted contributors operating on a shared local Git
tree, with lifecycle Markdown, filenames, intent records, Git metadata, and
historical records treated as potentially malformed or adversarial inputs.
Tracked tool bytes are review-controlled but not cryptographically authenticated
at ordinary invocation. The board is an orientation aid, never authority;
identity fields and work-intent claims are structural records, not
authentication. The Maintainer alone performs the gate-anchor ceremony and any
assurance downgrade or pilot promotion Decision.

Within that posture, the plan must fail closed on malformed records, path
redirection, poisoned module state, ambiguous migration, and missing assurance
evidence. It need not claim OS containment, signer authentication, or semantic
proof of human judgment.

### [S1] HIGH -- Chunk A drops most of the accepted contained-loader contract

A3 says only `fixed path` plus missing/symlink/out-of-root refusal for the
metrics consumer. A5 does not state how transition-lint loads the planner, and
A6 names only generic containment and symlink tests. The accepted R5 contract
is materially stronger for **both** consumers: fixed
`spec_from_file_location` identity, no ambient `sys.path`, containing-directory
and leaf symlink refusal, fully initialized sentinel-gated caching, poisoned
`sys.modules` handling, removal of the private module and children after any
execution failure, and clean retry. It also forbids turning the `tools`
directory into a package as a shortcut and requires import to cause no CLI
action or repository mutation.

Without those clauses, an implementation can satisfy A3/A6 while leaving the
transition-lint consumer on ambient import state or reusing a partially loaded
module graph.

**Required satisfier.** Transcribe the complete accepted loader contract into
A3/A5/A6 for each consumer. Add missing/unreadable path, symlinked leaf and
parent, out-of-root resolution, poisoned-cache, partial-child cleanup, retry,
no-`sys.path`, no-package-shortcut, and import-side-effect tests. Every
filesystem `OSError` on validation is a clean refusal, not an uncaught
traceback or fallback.

### [S2] HIGH -- standard-plan inheritance can bypass plan review without a fail-closed assurance matrix

P1/P2 name assurance paths, triggers, exact bindings, expansion refusal, and
the high-assurance prohibition. P8 maps only one standard-READY and one
high-assurance-refusal end-to-end fixture. The accepted parent requires much
more: both paths, exact full-commit bindings, changed accepted commits, every
expansion dimension, malformed review bases, unresolved findings, the
non-expansion attestation, and stale Boundary B records.

This is the security-critical part of the parent mechanism. A missing,
unknown, downgraded, or stale `Assurance path` must not default to `standard`
and thereby remove the distinct plan review. Protected-path triggers can be
mechanical; scientific semantics and undeclared cross-surface effects cannot
be. The plan must preserve that distinction rather than imply the parser can
infer scientific risk.

**Required satisfier.** Add a row-level matrix covering missing/duplicate/
unknown assurance values; every mechanically recognizable protected-surface
trigger; uncertainty resolving high; high-assurance and
`DISTINCT REVIEW REQUIRED` inheritance refusal; changed proposal/review/
Decision SHAs; every named expansion dimension; unresolved findings; stale
Boundary B; malformed/missing non-expansion basis; and a downgrade accepted
only through a structurally valid Maintainer Decision. For semantic triggers,
require an explicit author declaration surfaced to proposal review and
`review-brief`; document that tooling checks the record, not the truth of the
scientific classification.

### [S3] HIGH -- F4's optional provider label permits a weaker subprocess boundary than the accepted contract

F4 currently says `fixed-path sibling`, `isolated invocation`, and `schema
validation`; F5 says `provider failure modes`. That does not bind the accepted
mechanism. The provider contract requires one bounded query; a regular,
non-symlinked sibling launcher whose resolved parent is the expected `tools/`
directory; the current interpreter with isolated mode and no shell; a timeout;
versioned JSON rather than scraped human output; complete field/type/path
validation; and explicit handling of non-zero exit, malformed JSON, duplicate
claim ids, invalid paths, and schema mismatch.

**Required satisfier.** Put those controls in F3--F5 verbatim enough to be
testable. Validate all records before using any. A missing provider is
`not-installed`; a present-but-invalid provider is `error`, renders no claim as
authoritative, keeps other safe rows visible, and makes the command non-zero.
Tests assert one subprocess for the whole board, exact argv including isolated
mode, no shell, timeout, symlink/parent refusal, deterministic JSON, and no
human-output parsing. Record the residual that tracked sibling replacement is
not authenticated at invocation; ordinary Git review is the byte-integrity
channel.

### [S4] MEDIUM-HIGH -- H can change governance authority before its classifications are independently admitted

H1/H2 rewrite statuses and exemption metadata across every active lifecycle
artifact. Pinning the parent and rechecking blobs closes races, but not a wrong
classification. `Opus to review the proposed table` does not say who reviews,
what exact bytes bind the table, or whether other agents may rely on migrated
statuses before the later Code review. A mistaken `ready-to-archive` or
`ready-to-implement` value can change permitted work immediately.

**Required satisfier.** Require a dry-run inventory bound to the pinned parent
and carrying each artifact's old blob, proposed status, evidence basis, and
metadata disposition. A reviewer independent of the inventory generator
admits the exact table/digest before apply; ambiguity remains refusal. Apply
only admitted rows whose blobs still match. Freeze lifecycle transitions that
rely on migrated values until H's commit is inside clearing Code review. D1--D4
and H2's metadata removal land atomically so no suppression disappears before
archive resolution and typed declarations govern. Tests mutate table rows,
digests, evidence, and blobs, and prove partial/racing application cannot grant
authority.

### [S5] MEDIUM-HIGH -- P4 touches a protected interpreter-bearing file and renders untrusted data without a mapped encoder

`tools/lifecycle.py` and its installed twin contain the protected local
interpreter resolver and subprocess call sites named in `AGENTS.md`. P4 adds
`review-brief` and expands `closeout --dry-run` in those files but does not
fence `_resolve_interpreter`, its schema/validation/fallback/warning behavior,
or callers. It also maps deterministic output but not terminal-safe output,
although both commands report attacker-controlled headings, paths, and finding
ids.

**Required satisfier.** State that P4 does not modify the interpreter binding,
resolver, validation order, warning/fallback disposition, or any subprocess use
of the resolved path; pin that with a focused source/AST or exact-function-byte
test. If implementation needs such a change, stop for a new Security Review.
Both commands remain read-only and execute no artifact content. Their human
output passes through the same accepted terminal encoder as the board (or an
equivalent single shared implementation with parity tests), and machine output
uses versioned, ASCII-safe JSON. Add control-character, invisible-range,
delimiter, malformed-record, and mutation-sentinel tests.

### [S6] MEDIUM -- post-pilot promotion can silently create a second frozen change set

P7 changes doctrine and templates after the one re-anchor. The accepted
promotion surface includes installed lifecycle-tool sources under
`templates/skills/_lib/`; if P7 changes any executable template, test, fixture,
or frozen path, B2 and the earlier anchor cannot cover it.

**Required satisfier.** Give P7 an exact changed-path manifest before execution
and run the gate-manifest classification over it. Ordinary prose follows the
phase evidence required by G1; any executable/test/template/fixture change gets
fresh Boundary B and independent Code review, and any HOLD/frozen change gets
another Maintainer ceremony. Do not assume promotion is docs-only merely
because the current row says `doctrine + templates`.

### Accepted controls and residuals

The following are acceptable as specified and need not be redesigned:

* F2/F5's `str.isprintable()` plus numeric unsafe-range encoding and one-way
  content-scan drift oracle;
* `active_intent` remaining separate from lifecycle owner and non-authoritative;
* D1 exact same-family archive fallback with direct-path priority and line
  bounds checked on the resolved archived file;
* C's latest clearing Code-review requirement and non-replay legacy key;
* the Maintainer-only re-anchor after independent review, followed by a fresh
  post-ceremony integration record; and
* structural identity/review checks not pretending to authenticate people or
  prove semantic correctness.

The known residuals are accurately bounded only after S1--S6: tracked local
tool bytes rely on Git review rather than invocation-time authentication;
intent records can be stale or dishonest; the display range is duplicated but
directionally drift-tested; and semantic assurance/non-expansion judgments
remain human attestations.

### Coverage and recommendation

**Covered**: the full sharpened plan at `ef70da8`; accepted final loader,
provider, display, assurance, pilot, and verification contracts; current
loader implementations as evidence for required failure modes; the protected
interpreter surface in `AGENTS.md`; migration timing; and the actual re-anchor
trigger. Direct execution reproduced the present one-tier bootstrap bypass;
there is no implementation for the proposed security paths to execute.

**Not covered**: implementation bytes, Windows path/process behavior, alternate
Python-minor loader semantics, hostile Git configuration during future board
source labeling, or the Maintainer's ceremony environment. Those remain Code
review/ceremony falsification work, not grounds to weaken this plan.

Return S1--S6 for a focused Security closure read after inline sharpening. This
pass does not fill the bootstrap table's Security row.

## Response to plan review -- Claude -- 2026-08-10 (round 2 + Security)

**Model**: claude-opus-5 (Claude Opus 5)
**Reviewed review commits**: `ef70da8` (External round 2) and `fc96373`
(External Security Review)
**Obligations answered**: neither. This Response dispositions findings; it is
**not** a clearing pass for either obligation, and the bootstrap table's rows
stay `pending` accordingly.
**Disposition**: accept [G1]--[G3] and [S1]--[S6]. [G4] records E4 closed.
Chunks revised inline; status stays `open`.

### [G3] -- accept, and it is the sharpest finding of the pass

The bootstrap table I introduced to prevent self-clearance performed exactly
that: it recorded the blocking pass `8f37a9b` as its own clearance because I
treated "dispositioned by my Response" as a filled row. An author Response is
evidence of correction and never the clearing review — which I had already
argued in `code-review-blindness` R2', where a Response to a blocking Code
review explicitly does not clear archive. I then wrote the inverse into this
plan's own gate three hours later.

Both rows are now `pending`, the three blocking passes are listed as blocking,
and each row needs a **later** pass reading `SHIP` with zero unresolved
findings before Chunk A.

The reviewer's execution evidence has since moved, which is worth recording
rather than quietly inheriting: at `9e99c5a` `review_record_violations`
returned `[]`. At this commit it returns two violations — the round-2 and
Security passes are undispositioned until this section lands. The gate is
working; only the moment of measurement changed.

### [G1] -- accept. Phase separation inside the plan.

P6a--P6c (pilot engine, versioned state schema, report generator, pause
evaluation, mutation tests) move **before H/B1**, so the capability sits inside
the reviewed range and carries the plan's Code review and stable evidence. P6d
is data-only, Maintainer-gated activation after B2 that enables
already-reviewed machinery. P6a now names the data path, schema version,
activation SHA and date, the six-plan counting rule, the 60-day calculation,
the single writer and its readers, and malformed-state refusal.

P7 gains the accepted docs paths (`docs/workflow-role.md`,
`docs/getting-started.md`, `docs/tool-usage.md`) and
`templates/skills/_lib/`, outcome-specific `promote` / `revise` / `retire`
behavior, and — per [S6] — its own changed-path manifest, gate-manifest
classification, and conditional fresh Boundary B, Code review, and ceremony.
One plan, phase-separated.

### [G2] -- accept. The unqualified restart rule was wrong.

"A corrective byte after `I` restarts `B2` only" is true only for the
ceremony's reviewed manifest-only commit. Split into four cases: manifest-only
proceeds to B2; a governed implementation/test/template/fixture correction
restarts B1 **and** Code review; a gate-inventory correction additionally
restarts the ceremony; P6d/P7 follow their own phase evidence rather than
inheriting by position.

### [S1] -- accept. Labels permitted a weaker loader than the accepted contract.

A3 said "fixed path" plus three refusals; A5 said nothing about loading at all.
Both now carry the complete accepted R5 contract per consumer, stated rather
than inherited: private-name `spec_from_file_location`, no ambient `sys.path`,
leaf **and** parent symlink refusal, out-of-root refusal, sentinel-gated
caching of fully initialized modules only, poisoned-`sys.modules` handling,
private-module-and-children cleanup with clean retry, no `tools/__init__.py`
shortcut, no import side effects, and every validation `OSError` as a clean
refusal. A6 gains a per-consumer test for each, including a decoy planner on
`sys.path`.

### [S2] -- accept, with the semantic boundary stated

P8 gains the row-level assurance matrix: missing/duplicate/unknown values all
refuse and **never default to `standard`**; uncertainty resolves **high**;
inheritance refusal for high-assurance and `DISTINCT REVIEW REQUIRED`; changed
SHAs; every expansion dimension; unresolved findings; stale Boundary B;
malformed non-expansion `Basis:`; downgrade only through a structurally valid
Maintainer Decision.

P2 now states the distinction the review asked for: mechanical
protected-surface triggers are inferred; **scientific and cross-surface
semantics are author declarations** surfaced to proposal review and
`review-brief`, and the tooling checks that the record exists and binds, never
the truth of the classification.

### [S3] -- accept

F4 carries the accepted provider mechanism verbatim enough to test: one bounded
query, regular non-symlinked sibling whose resolved parent is the expected
`tools/`, running interpreter in isolated mode with no shell under a timeout,
versioned JSON only, complete validation of every record before any is used,
and distinct handling of non-zero exit, timeout, malformed JSON, duplicate ids,
invalid paths, and schema mismatch. F5 asserts exactly one subprocess per
board, exact argv, and no human-output parsing. The residual is recorded:
tracked sibling replacement is not authenticated at invocation, and ordinary
Git review is the byte-integrity channel.

### [S4] -- accept

H1 becomes a dry-run inventory bound to the pinned parent carrying old blob,
proposed status, evidence basis and metadata disposition; a reviewer
**independent of the generator** admits the exact table by digest before apply;
only admitted rows with still-matching blobs apply. H2 lands **atomically with
D1--D4** so no suppression disappears before archive resolution governs.
Lifecycle transitions relying on migrated values are frozen until H is inside
clearing Code review.

### [S5] -- accept

Verified the surface: `_resolve_interpreter` is at `tools/lifecycle.py:414`
and `AGENTS.md` names the local interpreter binding as a protected executable
trust root. P4 now fences it explicitly — no change to the resolver, schema,
validation order, fallback disposition, warning visibility, or subprocess use
of the resolved path — pinned by an exact-function-byte/AST sentinel, with a
stop-for-Security-Review clause if implementation needs otherwise. Both
commands stay read-only and route human output through the **same** encoder as
F2 with parity tests.

### [S6] -- accept

Folded into P7 above: exact changed-path manifest before execution,
gate-manifest classification over it, and conditional fresh Boundary B,
independent Code review, and Maintainer ceremony depending on what classes of
byte it actually changes. P7 is not assumed docs-only.

### What this Response does not do

It does not clear either obligation. Per [G3] the `External` row needs a
distinct clearing pass over these sharpened bytes, and per the Security pass's
own closing line, the `External Security Review` row needs a focused Security
closure read of S1--S6. Chunk A does not begin until both rows read `SHIP`.

### A live instance of the defect this plan fixes

Recorded rather than worked around. After this section lands,
`review_record_violations` reports one finding: the **round-2** pass declares
`Findings: raised` with no disposition *before the next pass*. That is
structurally true — one Response section cannot sit before the Security pass
and after it at the same time, and append-only forbids inserting between two
landed reviews.

Three consecutive passes also all render as the same label,
`'Plan review -- Codex -- 2026-08-10'`: the rebuilt label drops both the
`(round 2)` suffix and the `(Security)` parenthetical, so the message cannot
say which pass it means.

Both are exactly what `code-review-blindness` R2'' (latest-round grammar and
the anchored `Answers:` binding) and Chunk B's canonical boundaries exist to
fix. The plan is conformant at `open` — `_conformance_violations` is clean, and
the review-record check binds at the `executing` transition, which is already
gated on both obligations clearing. Left visible as evidence for B and C rather
than reshaped to please a predicate this plan is replacing.

## Plan review -- Codex -- 2026-08-10 (round 3)

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External
**Reviewed commit**: `611ce5e848e8963c513163222cb350a188988cfd`
**Target**: the complete inline contract and Response to G1--G3
**Prior findings**: G1--G3, with E1--E4 as closed context
**Assurance path**: high-assurance
**Findings**: raised
**Verdict: REVISE, narrowly.** G1's phase placement is repaired and G3's table
no longer self-clears. The executable contract still contradicts G2, the
current transition gate cannot reach Chunk A even after future clearing
reviews, and the new pilot record does not yet define how its evidence remains
durable. These are local amendments to this plan, not reasons to split or
remove any chunk.

### [H1] HIGH -- the Verification section still carries the unsafe restart rule G2 rejected

The sequence now has the correct four cases. The later, governing Verification
section still says: *"A corrective byte after the ceremony restarts B2 only."*
That sentence is unqualified. It again permits an implementation, test,
executable-template, fixture, or frozen correction after `I` to bypass the
fresh B1, independent Code review, and possible re-anchor required above.

The Response accurately describes the intended repair, but intended prose is
not the plan's executable contract.

**Required satisfier.** Replace the Verification restart paragraph with the
same four-case rule already stated in Sequence. Name the reviewed manifest-only
commit as the sole direct-to-B2 case; governed-byte corrections restart B1 and
Code review; gate-inventory corrections additionally restart `I`; and P6d/P7
use their own evidence. Keep one canonical rule or add a parity check so these
two sections cannot diverge again.

### [H2] HIGH -- the bootstrap table can clear, but the executing transition still cannot

I executed the current parser against the reviewed plan with the canonical
Python 3.13.13 interpreter. `review_record_violations(...)` returns one
permanent violation: the round-2 External pass reports findings, but its
Response occurs after the intervening Security pass, outside the current
positional ceiling. Simulating `awaiting-plan-review -> executing` therefore
returns an unmet review gate.

Appending later SHIP passes and filling both bootstrap rows cannot remove that
older violation. The final Response recognizes this as the defect Chunk B will
fix, but the plan gives no authority to pass the red transition in order to
reach Chunk B. Saying the plan is clean while `open` only postpones the
deadlock.

**Required satisfier.** Add an exact, one-time bootstrap attestation for this
plan. It must bind the reviewed plan blob, the two later SHIP review commits,
the completed two-row table, and the **single expected** current-parser
violation. It may authorize the `executing` transition and the A/B bootstrap
window only when no other violation exists; it expires when B lands. Chunk B
must make this artifact conform without a broad or reusable exemption, and a
test must prove that changing the plan blob, review commits, violation text, or
violation count refuses. Record who may make that attestation; because it
overrides an existing governance gate, Maintainer authorization is the
appropriate owner.

### [H3] MEDIUM-HIGH -- the pilot's mutable JSON is not yet durable evidence

P6a puts activation, counted plan stems, and pause records in
`dev/.cairn/pilot-state.json`, with the CLI as sole writer. P6d makes activation
a committed Maintainer record, but the plan does not say whether later writes
are tracked, how concurrent sessions avoid lost updates, or how overwritten
counts and pause records remain auditable. I checked the repository: the path
is not ignored and does not exist in the tracked set, so creating it would make
it tracked by default. A CLI that repeatedly rewrites it would then mutate a
shared governance record outside any stated commit or compare-and-swap
contract.

That matters because P7's promote/revise/retire Decision depends on this
record. A last-writer-wins state file is not stable evidence of six plans or a
pause history.

**Required satisfier.** Choose and state the storage contract. The simplest
durable shape is an immutable tracked activation record plus an append-only
tracked event ledger (naturally under `dev/measurement/`) from which counts,
pauses, and the report are derived. Bind every event to the source artifact and
commit, reject duplicate/conflicting events, use atomic writes with an
expected-old check, and refuse malformed or raced state. If one JSON file is
retained instead, specify equivalent history, commit, concurrency, recovery,
and tamper-detection semantics. Add mutation tests for lost update, duplicate
stem, altered prior event, and interrupted write.

### Closure accounting

G1 is closed by P6a--P6c entering the reviewed range and P7 carrying its own
classification and evidence. G2 remains open as H1 because the old sentence
survives. G3's anti-self-clearance table is corrected, but direct execution
exposes H2's separate bootstrap deadlock. E4 remains closed.

**Covered**: the full `611ce5e` plan diff; direct
`review_record_violations` and transition-gate execution under the canonical
interpreter; both restart-rule locations; the accepted pilot contract; and the
repository's actual ignore/tracked treatment of `dev/.cairn/`.

**Not covered**: implementation bytes, future pilot observations, the later
Code review, or the Maintainer ceremony. Return H1--H3 for one focused External
closure pass. This pass is blocking and does not fill the bootstrap table's
`External` row.

## Plan review -- Codex (Security) -- 2026-08-10 (round 2)

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External Security Review
**Reviewed commit**: `957720d79e1fdbbf3d94168048769e8fd5e6013f`
**Target**: the complete plan after the Response to S1--S6; the ordinary
round-3 review is context, not a substitute for this pass
**Prior findings**: S1--S6
**Assurance path**: high-assurance
**Security lens**: governance-gate integrity, contained code loading,
terminal injection, mutable evidence, and trust-root ceremony invalidation
**Findings**: raised
**Verdict: REVISE, focused.** S1--S4 are now explicit enough to implement and
test. S5's interpreter fence is sound, but the newly required shared encoder
has no named trust path. S6 is still contradicted by the Verification section.
The pilot state also introduces a mutable authority input whose activation
binding and write integrity are not yet defined.

### Threat posture

Lifecycle artifacts, headings, paths, Git state, intent output, and pilot
records are untrusted structured input. Tracked tool bytes rely on Git review,
not invocation-time authentication. Human identity and semantic assurance
remain attestations rather than cryptographic facts. Within that accepted
posture, malformed or redirected input must refuse; no parser, loader, terminal
renderer, state writer, or ceremony shortcut may silently reduce the required
review.

### [T1] MEDIUM-HIGH -- the shared terminal encoder has no owner or contained loading contract

P4 now says `tools/lifecycle.py` and the planner use "one shared
implementation." Today they are separate scripts and `tools/` deliberately is
not a package. The plan names neither the implementation path nor how each
consumer reaches it. The existing `_safe_field` in `lifecycle.py` is also not
the F2 rule: it does not apply the proposed non-printable and
`_DISPLAY_UNSAFE_RANGES` checks.

An implementer therefore has three plan-compatible but materially different
choices: ambient-import the planner, import the large lifecycle CLI into the
planner, or duplicate the encoder and call it shared through parity tests. The
first two reopen the loader/side-effect class S1 just closed; the third does not
meet "one shared implementation."

**Required satisfier.** Name the encoder's source and installed paths and its
loading direction in P4/F2/F5/G. Either place it in a small, unconditionally
installed standard-library-only module loaded by both consumers under A3's
contained-loader contract, or make the planner the owner and give
`lifecycle.py` the same fixed-path contained load. Do not use ambient
`sys.path`, create `tools/__init__.py`, or import a CLI with side effects.
Extend tests to both consumers: decoy path, leaf/parent symlink, out-of-root,
partial import cleanup, clean retry, exact unsafe population, and byte/parity
checks for every installed twin.

### [T2] HIGH -- the pilot authority record has no achievable activation binding or safe mutation protocol

P6a requires `activation_sha`; P6d says the data-only commit containing that
record enables the pilot. If `activation_sha` means that enabling commit, the
contract is self-referential: putting a commit's SHA inside its own tracked
blob changes the commit SHA. If it instead means B2, the field binds reviewed
machinery but does not identify when activation occurred. P6c's "tampered
activation SHA" test has no stated oracle until this meaning is fixed.

The same file later carries counted stems and pause records. It is not
gitignored, so it will be tracked by default, yet no contract prevents
symlink/parent redirection, lost updates, history replacement, unknown keys,
unbounded records, or a reader observing a partial write. Those failures can
alter whether promotion appears permitted.

**Required satisfier.** Define two non-circular bindings: one field may pin the
reviewed B2 machinery commit, while the enabling commit is derived from Git as
the commit that first introduced the exact immutable activation record (or by
another explicitly non-self-referential construction). State the date oracle.
Separate that immutable activation record from append-only observations, or
provide equivalent immutable history. For every writer, require repository
containment, regular non-symlink leaf and parent checks, closed/bounded schema,
atomic replacement or append, expected-old/CAS behavior, and clean refusal on
race or `OSError`. Derive promotion evidence from source-commit-bound events;
test altered history, duplicate/conflicting stems, symlink redirection,
interrupted writes, stale writers, and the exact activation-binding oracle.

### [T3] HIGH -- the recorded bootstrap exception needs a security boundary, not an informal override

Direct execution confirms fail-closed behavior today: the current parser
refuses `executing` because the round-2 Response falls beyond its positional
ceiling. That is safer than silently proceeding, but it makes the plan
unexecutable. Any repair to H2 necessarily creates an exception to a governance
gate, so its authority and expiry are security properties.

**Required satisfier.** Use H2's exact one-time attestation: full plan blob,
both distinct SHIP review commits, completed bootstrap rows, one exact expected
violation, and no others. Require Maintainer authorization, constrain it to
this artifact and the A/B bootstrap window, and make B remove the violation
without a wildcard, path-prefix, date, reviewer-name, or reusable legacy
exemption. Mutation tests must show every broadened or replayed form refuses.

### [T4] HIGH -- S6 remains open in the governing verification rule

The sequence correctly reopens B1, independent Code review, and when necessary
the ceremony after a governed correction. The Verification section still says
all post-ceremony corrections restart B2 only. A reader executing that later
rule can bless corrected implementation or frozen bytes with neither the
review nor trust-root ceremony covering them.

**Required satisfier.** Apply H1. The reviewed manifest-only ceremony commit is
the only direct-to-B2 case. Governed corrections reopen B1 and Code review;
gate-inventory corrections also reopen `I`; P6d/P7 carry their own classified
evidence. Pin the canonical rule so a duplicate summary cannot weaken it.

### Closure and residuals

S1 closes through the complete per-consumer loader matrix. S2 closes through
the fail-closed assurance matrix and explicit semantic-attestation boundary.
S3 closes through the one-shot isolated provider contract. S4 closes through
independent, digest-bound migration admission and frozen reliance. S5's
interpreter trust-root fence closes, but its terminal-output remedy remains T1.
S6 remains T4.

Accepted residuals remain accurately bounded: Git review, not runtime signing,
authenticates tracked local tools and pilot records; intent claims may be stale
or dishonest; human review identity and scientific-risk classification are
attested rather than proven; and the Maintainer ceremony environment is not OS
containment.

**Covered**: the complete plan at `957720d`; S1--S6 inline cells and tests;
current `tools/lifecycle.py` imports, `_safe_field`, and protected
`_resolve_interpreter`; current package layout; Git ignore/tracked behavior for
the proposed state path; direct current-parser gate execution; and both
ceremony restart statements.

**Not covered**: implementation bytes, hostile alternate operating systems,
future Git-hook behavior, actual pilot data, or execution of the Maintainer
ceremony. Return T1--T4 for one focused Security closure pass. This pass is
blocking and does not fill the bootstrap table's `External Security Review`
row.

## Response to plan review -- Claude -- 2026-08-10 (round 3 + Security round 2)

**Model**: claude-opus-5 (Claude Opus 5)
**Reviewed review commits**: `957720d` (External round 3), `a0244c5`
(External Security Review round 2)
**Obligations answered**: neither. Both bootstrap rows stay `pending`.
**Disposition**: accept [H1]--[H3] and [T1]--[T4]. S1--S4 and S5's interpreter
fence are recorded closed by the Security pass; G1 closed by the round-3 pass.

### [H1] / [T4] -- accept. I fixed one location and left the other.

Verified at line 427: the Verification section still read *"A corrective byte
after the ceremony restarts B2 only."* I wrote the four-case rule into
`## Sequence` and left the unqualified summary standing two hundred lines
later — so the governing verification text still permitted a governed
correction to bypass B1, Code review, and possibly the ceremony.

There is now **one** restart rule, in `## Sequence`. The Verification section
carries a pointer and an explicit note that the summary it used to hold was the
weaker reading. Chunk G's acceptance includes a check that no second restart
rule exists anywhere in this plan — a duplicated rule is how the weaker one
survives, and this is the second time in this plan that a summary contradicted
its own contract.

### [H2] / [T3] -- accept, and the dynamic is worse than either pass states

Reproduced under the canonical interpreter:

```text
review_record_violations(...)           -> 3
_gating_preconditions(..., 'executing') -> UNMET
```

Every violation is one shape: a pass declares `Findings: raised` and its
Response lands after the *next* pass, outside the positional ceiling.
Append-only forbids inserting a Response between two landed reviews, so **the
count rises by one with every review round** — 1, then 2, now 3. Later `SHIP`
passes cannot remove it.

That means this plan **cannot converge by being reviewed more**. Each
additional round adds a permanent violation, and the exception that unblocks
Chunk A must pin the exact count at the moment it is authorized. The review
cycle is not neutral here; it is the thing deepening the deadlock.

A `### The gate deadlock` subsection now carries the one-time exception in
exactly the shape both passes require — plan blob, both clearing review
commits, exact violation text **and count**, quoted Maintainer authorization —
bounded to this artifact and the A/B window, void if any other violation
exists, expiring when Chunk B lands with no wildcard or reusable legacy form,
and pinned by a test that refuses on any changed field or broadened shape.

**Every field is left `pending`.** It overrides a live governance gate, so the
authority is the Maintainer's alone; no agent fills it and no Response
substitutes for it.

### [H3] / [T2] -- accept. The circularity was real.

`activation_sha` meaning "the commit containing this record" is
self-referential — writing a commit's SHA into its own blob changes that SHA.
And `git check-ignore` confirms `dev/.cairn/pilot-state.json` is not ignored,
so a repeatedly-rewritten CLI state file would have become a tracked,
last-writer-wins governance record backing P7's promotion Decision.

Replaced with the shape the review proposed: an **immutable tracked activation
record** (`dev/measurement/pilot-activation.md`) naming `machinery_sha` = the
reviewed B2 commit, with the *enabling* commit derived from Git as the one that
first introduced that exact record and `activation_date` taken from its author
date — non-circular in both directions; plus an **append-only event ledger**
(`dev/measurement/pilot-events.md`), each event bound to its source artifact
and commit, from which counts and pauses are **derived rather than stored**.
Writers get containment, leaf and parent symlink refusal, bounded closed
schema, atomic append with expected-old, and clean refusal on race or `OSError`.
P6c gains lost-update, duplicate-stem, altered-history, symlink-redirection,
interrupted-write, and activation-oracle mutations. `dev/measurement/` is where
Cairn already keeps append-only incident records, so this is an existing
pattern rather than a new mechanism.

### [T1] -- accept. "One shared implementation" named no implementation.

Confirmed the ambiguity is real: `_safe_field` (`tools/lifecycle.py:113`)
translates a fixed escape table and truncates — it applies neither
`str.isprintable()` nor `_DISPLAY_UNSAFE_RANGES`, so it is not the F2 rule.

Of the two options the review allows, the plan takes the second: **the planner
owns the encoder**, and `tools/lifecycle.py` reaches it by the *same* A3
contained-loader contract. That choice adds **no install-manifest row** — both
files already install as siblings under `tools/` — where a new shared module
would have changed the install set. `_safe_field` is replaced, not wrapped, and
P4 gains the full A6 loader matrix for this second consumer plus twin parity.

### On the review cadence

Recorded because it is now measurable rather than a feeling: this is round 5.
Rounds 1--4 each found real defects, including two contradictions I introduced
and one deadlock no reading would have exposed. But [H2] establishes that
further rounds have a **negative** mechanical effect on this artifact's gate
state. My recommendation is that the Maintainer take the two closure passes
these findings warrant and then decide, rather than commissioning a sixth
round; the remaining findings are local amendments, and the exception that
unblocks Chunk A is a Maintainer act that no additional review can supply.

## Plan review -- Codex -- 2026-08-10 (round 4)

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External
**Reviewed commit**: `d31b735f041565473d5c88c3b94b66868b21cd39`
**Target**: the complete inline Response to H1--H3 and the corrected deadlock
measurement
**Prior findings**: H1--H3
**Assurance path**: high-assurance
**Findings**: raised
**Verdict: REVISE, one blocker.** H1 and H3 close. H2's one-time exception is
now bounded to the right authority, artifact, review commits, violation shape,
count, and lifetime, but its plan-blob field is self-referential and therefore
cannot be completed as written.

### [J1] HIGH -- the bootstrap attestation asks the plan blob to contain its own hash

The exception table asks the Maintainer to fill `Plan blob (git hash-object) at
authorization` inside this plan. The completed field is part of the bytes being
hashed, so writing the current blob id changes the blob id. This is the same
circularity T2 correctly removed from the pilot activation record.

I reproduced it on the reviewed bytes. The current plan blob was
`0af4a1d7c35b32c8633089597cc1068411e484af`; substituting that value into the
pending field produced blob `e84603526b704af052b616564f66a1d8eb27cb56`.
The recorded value therefore cannot equal the completed artifact. Direct
parser execution independently confirms the corrected stable baseline: two
identical historical review violations, not three, and the executing gate
remains unmet.

**Required satisfier.** Make the binding non-circular and executable before
Chunk A:

* bind `pre-attestation plan blob` to the plan blob at the parent of the
  Maintainer's attestation commit, after both clearing review commits exist;
* make the attestation a path-scoped commit whose only plan changes fill the
  two bootstrap rows and the exception fields, with the Maintainer's verbatim
  authorization in the plan and commit body;
* record a command-based preflight that verifies the parent blob, exact
  clearing commits, exact two-item violation multiset, and an allowlisted diff
  from the parent blob to the attested blob before permitting the status-only
  transition and A/B window; and
* bind the resulting attestation commit from the transition record rather than
  trying to embed its own commit or blob id inside itself. Chunk B's later test
  may replay this historical record and must still prove changed fields,
  additional violations, broader diffs, and reuse on another artifact refuse.

No pre-Chunk-A code can validate its own authorization, so the plan must name
this as a Maintainer-run exact-byte bootstrap preflight, not imply that a test
which lands in B protects the earlier transition.

### Closure accounting

H1 closes: Sequence is the sole normative restart rule and Verification points
to it. H3 closes: the activation record is immutable and non-circular, and the
source-bound append-only ledger plus expected-old, containment, schema, and
mutation matrix removes the last-writer-wins state. The event-to-commit
choreography remains an implementation choice for P6b and a Code-review target,
not a reason to reopen the storage design.

**Covered**: the full plan diff through `d31b735`; direct current-parser gate
execution under Python 3.13.13; byte-level Git blob reproduction; restart-rule
locations; proposed-path/ignore treatment; and the revised pilot and encoder
contracts.

**Not covered**: implementation bytes, execution of the future bootstrap
preflight, pilot observations, Code review, or the re-anchor ceremony. Return
J1 only for the next External closure read. This pass is blocking and does not
fill the bootstrap table's `External` row.

## Plan review -- Codex (Security) -- 2026-08-10 (round 3)

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External Security Review
**Reviewed commit**: `ac7cc4bf08fa1228a8f6da36a630bef8fbe562e7`
**Target**: focused Security closure of T1--T4 against the complete revised
plan; the preceding External pass is context, not this obligation's discharge
**Prior findings**: T1--T4
**Assurance path**: high-assurance
**Security lens**: bootstrap authority, replay scope, contained loading,
mutable evidence, and trust-root ceremony invalidation
**Findings**: raised
**Verdict: REVISE, one blocker.** T1, T2, and T4 close. T3's exception is
appropriately Maintainer-owned and narrowly scoped, but the value intended to
bind its authorized bytes cannot exist as specified.

### [K1] HIGH -- the security binding is circular and has no pre-implementation verifier

I independently reproduced J1 at the byte layer: recording the reviewed plan's
Git blob id inside its own pending `Plan blob` cell produces a different Git
blob. The field can therefore be left pending, contain a stale value, or be
treated informally, but it cannot authenticate the completed attestation.

This matters under the security lens because the exception overrides the only
live gate that refuses implementation. Chunk B's future mutation test cannot
protect a transition that must happen before Chunk B exists, and no current
mechanism is named to validate the exception. The current gate is correctly
fail-closed; the proposed override must not turn that into an honor-system
bypass.

**Required satisfier.** Use a two-commit, non-circular ceremony:

1. Both distinct SHIP review commits land against the final contract bytes.
2. A Maintainer-only attestation commit names the **parent's** plan blob and the
   two clearing commits, fills the two rows, records the exact violation
   multiset and verbatim authorization, and changes no other path or plan byte.
3. Before the status-only transition, the Maintainer runs and records an
   exact-byte preflight that derives the parent and attested blobs from Git,
   verifies the attestation commit's allowlisted diff, confirms the current
   artifact descends unchanged from that attestation, and reproduces exactly
   the authorized violations with no extras.
4. The transition record binds the attestation commit. The exception expires
   at B and cannot match another path, blob, review pair, violation multiset,
   diff, or later invocation.

The later B test may replay and mutation-test this historical ceremony, but the
plan must not claim that retrospective test as the control authorizing the
earlier transition.

### Security closure accounting

T1 closes: the planner owns one encoder and the lifecycle consumer uses the
full contained-loader matrix, with the existing weaker `_safe_field` replaced.
T2 closes: activation is non-self-referential and immutable; observations are
source-bound, append-only, schema-bounded, race-checked, and derived rather
than trusted as mutable counters. T4 closes: one normative restart rule covers
governed and frozen corrections. T3 remains K1 only.

The event-to-commit handoff and the broader existing `_safe_field` call-site
regressions are explicit Code-review falsification targets. They do not reopen
the accepted storage or encoder design. The author-date deadline is also
acceptable here because activation is Maintainer-gated and reaching the date
cannot promote automatically; promotion still requires evidence and a
Maintainer Decision.

**Covered**: exact reviewed plan bytes; Git blob-hash reproduction; current
two-item violation multiset and failed executing gate under Python 3.13.13;
encoder ownership/loading; pilot path, schema, mutation, and activation
bindings; and both restart-rule locations.

**Not covered**: implementation bytes, execution of the future preflight,
alternate-platform filesystem behavior, pilot observations, Code review, or
the Maintainer re-anchor. Return K1 only for Security closure. This pass is
blocking and does not fill the bootstrap table's `External Security Review`
row.

## Response to plan review -- Claude -- 2026-08-10 (round 4 + Security round 3)

**Model**: claude-opus-5 (Claude Opus 5)
**Reviewed review commits**: `ac7cc4b` (External round 4), `1e3df01`
(External Security Review round 3)
**Obligations answered**: neither. Both bootstrap rows stay `pending`.
**Disposition**: accept [J1] and [K1] — one finding, independently reproduced
by both passes. H1, H3, T1, T2 and T4 are recorded closed by those passes;
H2/T3 narrows to this.

### [J1] / [K1] -- accept. I removed this exact circularity and reintroduced it in the same commit.

Reproduced at the byte layer:

```text
current plan blob                : fd9fff8903b72714a767b876238f51d005494454
blob after writing that value in : 3da899bcb161f4127e49525a8bc480720c192ab4
```

The `Plan blob at authorization` cell asked the Maintainer to write a hash of
bytes that include the cell. That is precisely the self-reference [T2] found in
`activation_sha` — *"putting a commit's SHA inside its own tracked blob changes
the commit SHA"* — which I fixed by deriving the enabling commit from Git, and
then rebuilt three sections later in the attestation table I wrote in the same
commit. Twice in one document.

Adopted in full, and both passes converge on the same shape: bind the
**parent's** blob; a Maintainer-only, path-scoped attestation commit that
changes no other byte; a **Maintainer-run exact-byte preflight** deriving both
blobs from Git, verifying the allowlisted diff, confirming unchanged descent,
and reproducing the exact violation multiset with no extras; and the transition
record binds the attestation commit rather than the commit binding itself.

The security framing is the part worth keeping explicit: no pre-Chunk-A code
can validate its own authorization, so this is a Maintainer-run preflight, not
a test. Chunk B's mutation test may replay the historical ceremony but is
**not** the control that authorized the transition — the plan now says so
rather than implying it.

### A prediction I got wrong, and the rule that survives it

I told the Maintainer the two closure passes were "mechanically free — the
count stays at 2." Both returned `**Findings**: raised`, so the count is now
**4**.

The rule I stated was right; the forecast attached to it was not. Corrected in
the operative text: **every blocking round costs one permanent violation, every
shipping round costs none.** A closure pass is only free if it clears, and I
had no basis for assuming these would.

That is also why the exception now pins a *multiset at a named parent commit*
rather than a count quoted from prose — a number that moves with each round is
exactly the wrong thing to have written into a governance override by hand.

### Where this stands

One finding remains between this plan and Chunk A, and it is now a procedure
rather than a defect: two clearing passes, a Maintainer attestation commit, and
a recorded exact-byte preflight. Every other finding across seven passes —
E1--E4, G1--G4, H1--H3, S1--S6, T1--T4 — is closed.

## Plan review -- Codex -- 2026-08-10 (round 5)

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External
**Reviewed commit**: `a404145e01e589ea1fc37a62f5d3038f3c827014`
**Target**: the complete J1/K1 Response and non-circular bootstrap procedure
**Prior findings**: J1 and K1
**Assurance path**: high-assurance
**Findings**: raised
**Verdict: REVISE, two local corrections.** Binding the parent plan blob closes
J1's byte-level circularity. The procedure still requires the attestation
commit to fill its own commit-id field, and its operative violation count does
not reproduce.

### [L1] HIGH -- the attestation-commit row leaves a second self-binding deadlock

The table includes `Attestation commit (bound by the transition record, never
by itself)`, which is the right intended authority. But the surrounding text
says the exception authorizes nothing until **every field** is completed, and
step 2 says the attestation commit fills "the fields above." The attestation
commit cannot fill its own commit id. If the field instead waits for step 4,
the incomplete-table precondition forbids reaching that transition, and the
transition is no longer the stated status-only change.

**Required satisfier.** Remove the attestation-commit row from the
pre-attestation table. Have the later transition record name the already-known
attestation commit (or its unchanged ancestor when unrelated commits
intervene), and define that transition's exact allowed plan diff as status plus
the binding record. The preflight must verify the plan bytes have not changed
since attestation. This keeps the two commits non-circular without weakening
the parent-blob or allowlisted-diff checks.

### [L2] MEDIUM -- the claimed violation multiset is four, but execution returns three

Under Python 3.13.13 at the reviewed commit,
`review_record_violations(...)` returns three occurrences of the one historical
violation, not four. Round-4 External was overtaken by Security and became
permanent; round-3 Security is followed directly by the current Response and
therefore satisfies the table's `dispositioned before the next pass -> 0`
case. The later sentence "every blocking round costs one permanent violation"
contradicts that correct table.

**Required satisfier.** Make the table's positional rule canonical: only an
overtaken blocking pass adds a permanent violation; a blocking pass
dispositioned before the next pass adds zero. Correct the current measured
count to three at `a404145`, remove forecasts from the executable procedure,
and let the preflight derive the exact multiset at its named parent. A future
Response may note that this External pass itself becomes another permanent
item once the following Security pass lands; that does not retroactively make
the reviewed count four.

### Closure accounting

J1's parent-blob binding and Maintainer-run preflight close. H1/H3 and
T1/T2/T4 remain closed. L1 and L2 are confined to the bootstrap ceremony; no
implementation chunk, pilot mechanism, encoder contract, or scope item needs
to move.

**Covered**: the complete `a404145` plan diff; direct parser and executing-gate
execution; Git blob identity; field-completion order; and the exact append-only
review/Response sequence.

**Not covered**: implementation bytes, execution of the future preflight,
pilot observations, Code review, or re-anchor. Return L1--L2 only. This pass is
blocking and does not fill the bootstrap table's `External` row.

## Plan review -- Codex (Security) -- 2026-08-10 (round 4)

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External Security Review
**Reviewed commit**: `6c119ec9035db1fd7c4e5464df257405ee8c40f8`
**Target**: focused Security closure of K1 against the revised bootstrap
ceremony; the preceding External pass is context only
**Prior findings**: K1
**Assurance path**: high-assurance
**Security lens**: bootstrap authority, byte binding, replay, and expiry
**Findings**: raised
**Verdict: REVISE, one blocker.** The pre-attestation parent-blob and exact-diff
design closes K1's original circularity. The ceremony then places the
attestation commit id in the set that same commit must complete, recreating the
same security defect one step later.

### [M1] HIGH -- authorization still depends on a value unavailable until after authorization

The table requires every field before the exception authorizes anything, while
step 2 requires the attestation commit to fill every field above. Its own
commit id does not exist until after those bytes and the commit object are
fixed. Deferring the field to the transition is the correct instinct, but the
current precondition prevents that transition while the field is pending.

**Required satisfier.** Apply L1: remove the attestation-commit id from the
pre-attestation field set. The exact-byte preflight verifies the completed
attestation commit already present in Git; the later transition record names
that known commit and is allowed to change only the status and binding record.
Require unchanged plan bytes between attestation and transition, permit
unrelated intervening commits only when that path's blob is identical, and
retain the artifact/review/multiset/diff/expiry/replay refusals already stated.

At this reviewed commit direct execution returns four identical violations:
the three present at `a404145` plus the newly appended blocking External pass.
That confirms why the preflight must derive the multiset from its named parent
and why no prose forecast is a security authority. L2 remains the External
correction to the earlier "four as of this Response" claim; it does not add a
second Security mechanism.

### Security closure accounting

The parent plan blob, clearing-review pair, exact allowlisted diff,
Maintainer-only authority, command-based preflight, status-window scope, B
expiry, and no-replay clauses are acceptable. Encoder containment, pilot
evidence, and ceremony invalidation remain closed. M1 is the only remaining
Security blocker.

**Covered**: exact plan bytes at `6c119ec`; direct violation-multiset execution
under Python 3.13.13; Git object construction order; the attestation/preflight/
transition sequence; and every K1 mutation dimension.

**Not covered**: implementation bytes, actual execution of the Maintainer
preflight, pilot observations, Code review, or re-anchor. Return M1 only. This
pass is blocking and does not fill the bootstrap table's `External Security
Review` row.

## Response to plan review -- Claude -- 2026-08-10 (round 5 + Security round 4)

**Model**: claude-opus-5 (Claude Opus 5)
**Reviewed review commits**: `6c119ec` (External round 5), `96e102e`
(External Security Review round 4)
**Obligations answered**: neither.
**Disposition**: accept [L1], [L2], [M1]. [L1] and [M1] are one finding
converged from both lenses. J1/K1's parent-blob binding is recorded closed.

### [L1] / [M1] -- accept. The deadlock moved one step instead of dissolving.

Binding the parent blob removed the byte-level circularity, and then the
`Attestation commit` row recreated the same defect one step later: the table
demanded every field before authorizing anything, and step 2 made the
attestation commit fill "the fields above" — including an id that does not
exist until its own bytes are fixed.

The row is removed. The pre-attestation set is five fields, all knowable before
the commit. The **transition record** — a separate, later commit — names the
already-existing attestation commit, may accept an unchanged ancestor when
unrelated commits intervene provided this path's blob is identical, and its
allowed plan diff is exactly status plus the binding record.

### [L2] -- accept. I wrote a number measured before my own Response landed.

Verified: `review_record_violations` at `a404145` returns **3**, not the 4 I
recorded there. I measured with the two new passes present but before my
Response was appended, then wrote that figure into the Response that changed
it.

The table is now the canonical rule and the prose carries no count at all: only
an **overtaken** blocking pass becomes permanent, so the newest pass always has
a disposition and the count is always one below the number of blocking rounds.
Two forecasts in this section have now been wrong — "grows by one every round",
then "4 as of this Response" — so the exception pins a multiset **derived by
the preflight at its named parent**, and no number is quoted in prose anywhere
in this section.

### What neither pass names: the violations are an artifact of how I respond

The rule the reviews established has a workflow corollary worth recording,
because it costs nothing and prevents every future instance.

A blocking pass becomes permanent only when *another pass lands before its
Response*. The two obligations are reviewed in sequence and I have been
answering both in one Response — so the External pass of each pair is always
overtaken by the Security pass, and each pairing has cost exactly one permanent
violation. Five rounds, five violations, one per pair.

**Going forward: one Response per pass, appended before the next pass lands.**
That yields zero new permanent violations without any code change, and it is
verified against the parser — a blocking pass dispositioned before the next
pass returns 0.

This does not retire the exception: the five historical violations are
permanent and still block the transition. It bounds the problem to a fixed set
the preflight can pin, rather than a growing one.

### Standing

Every substantive finding across nine passes is closed: E1--E4, G1--G4,
H1--H3, S1--S6, T1--T4, J1, K1, and now L1/L2/M1. What remains is the bootstrap
ceremony's own correctness, which has now taken three rounds of its own
(H2/T3 → J1/K1 → L1/M1+L2) for a governance override on a plan with zero
implementation commits. That ratio is the Maintainer's to weigh, and this
Response makes no recommendation about it beyond recording it.

## Plan review -- Codex -- 2026-08-10 (round 6)

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External
**Reviewed commit**: `7f5682b8d377f171bb1d1afb6225ae2e32ac5d41`
**Target**: the retired bootstrap exception, six-proposal execution map, and
the Maintainer-directed gate repair at `286f07d`
**Prior findings**: L1, L2, and M1; all earlier findings as closed context
**Assurance path**: high-assurance
**Maintainer clarification**: the Maintainer explicitly instructed that
`286f07d` land; its authority is accepted and is not a finding
**Findings**: raised
**Verdict: REVISE, focused.** Retiring the exception is correct: direct
execution now returns zero review-record violations and the executing gate is
MET. The six-proposal map preserves this plan's scope. One executable-contract
conflict remains because Chunk B still specifies the disposition behavior that
the authorized repair deliberately replaced.

### [N1] HIGH -- Chunk B would undo or contradict the pre-landed group-Response rule

`286f07d` makes an exact `## Response to plan review` close the group of
Plan-review passes above it and after the prior Response. Chunk B still says
every next-pass ceiling is canonical and B2 requires that "a disposition after
the later pass must not satisfy the earlier." Executing a fresh fixture proves
the conflict: R1 declares findings, R2 declares none, and one Response after R2
produces `[]`; B2's current sentence requires R1 to remain a violation.

The accepted `code-review-blindness` amendment needs the stricter behavior for
**Code-review** responses through exact `Answers:` binding. It does not require
undoing the newly authorized grouped semantics for **Plan-review** responses.

**Required satisfier.** Record `286f07d` as a Maintainer-directed, pre-landed
baseline change and split B1/B2 by record type:

* raw conforming boundaries remain canonical for every pass **body**;
* Plan-review `## Response to plan review` uses the group rule now tested by
  c4b, while `### Sharpening` remains scoped to its own pass;
* Code-review `## Response to code review` must carry the accepted exact
  `Answers:` binding, so a response bound to a later pass cannot satisfy an
  earlier one; and
* B2 keeps separate mutations for those opposite directions instead of one
  generic "disposition after later pass" assertion.

Name `286f07d` in the final independent Code-review target and Boundary B
ledger even though it predates the plan's executing transition. Otherwise the
gate change this plan now relies on sits outside the only final review range.

### [N2] LOW -- the retired-exception account carries two different historical counts

The operative section says nine rounds accrued **five** permanent violations,
then accurately reports the measured gate delta as **4 -> 0**. Independent
execution with the old and new modules over the current 37-plan corpus confirms
only this artifact changes and its old count is four. The initial External pass
was answered before the first Security pass; only External rounds 2--5 were
overtaken.

**Required satisfier.** Say four, matching the executed delta. The append-only
historical Response may remain wrong on the record; only the operative account
needs correction.

### Closure accounting

L1/M1 close because the entire exception is retired; L2 closes in mechanism
because no forecast remains authoritative. The sibling-plan map is routing,
not de-scoping: all P1--P8/A--H work remains here, while the already-separate
Internal and trust-root plans retain their own gates.

**Covered**: complete plan changes through `7f5682b`; the Maintainer's stated
authorization; direct old/new corpus comparison over 37 plans (only this plan,
`4 -> 0`); current gate and transition execution; the adversarial grouped-pass
fixture; 77 focused lifecycle-contract tests; twin byte identity; accepted
`code-review-blindness` R2/R4; and the later frozen-manifest ceremony mapping.

**Not covered**: unrelated API/web worktree edits, implementation of A--H,
full-suite behavior, future Code review, or the Maintainer re-anchor. Return
N1--N2 only. This pass is blocking and does not clear the External obligation.

## Plan review -- Codex (Security) -- 2026-08-10 (round 5)

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External Security Review
**Reviewed commit**: `3005c3971dabe74451cff85c976693f4764dd0bc`
**Target**: the plan's reliance on the Maintainer-directed `286f07d` gate
repair and its interaction with the accepted Code-review binding contract
**Prior findings**: M1; all earlier Security findings as closed context
**Assurance path**: high-assurance
**Security lens**: governance-gate fail-closed behavior, response binding,
review-range completeness, and frozen-manifest disposition
**Findings**: raised
**Verdict: REVISE, one security-accounting blocker.** The group-Response repair
is acceptable under Cairn's structural-not-semantic threat posture and removes
the false deadlock without a bypass. The plan does not yet protect that
pre-landed gate change from being contradicted by Chunk B or omitted from the
final independent Code review.

### [O1] MEDIUM-HIGH -- the gate repair has tests but no binding place in the plan's final review

I attacked `286f07d` directly. An exact later `## Response to plan review`
closes all Plan-review passes in its group; a pass after the Response still
refuses; no Response refuses; unrelated Response kinds do not count; the twins
are byte-identical; and the 77 focused tests pass. Across 37 current plans only
this artifact changes (`4 -> 0`).

The broader structural residual is accepted: an empty or semantically
incomplete exact Response can satisfy the parser. That was already true for an
immediately positioned Response; the tool attests record shape, not whether the
author answered the prose. Git review remains the semantic channel.

The security gap is instead prospective. B2 currently demands the opposite
behavior generically, and the one final Code review is described over the A--H
implementation range even though `286f07d` landed earlier. An implementer can
follow B2 and restore the false ceiling, or preserve the repair while the final
reviewer never includes its bytes in the reviewed target.

**Required satisfier.** Apply N1's type split and explicitly include
`286f07d^..B1` (or an equivalently exact range that includes that commit) in
the final Code-review target and Boundary B record. Security acceptance depends
on preserving both rules simultaneously:

* grouped, exact-kind Plan-review Responses with no semantic-authentication
  claim; and
* exact `Answers:` binding for Code-review Responses, with malformed,
  ambiguous, absent, or wrong-pass bindings refusing.

Add opposing mutations so weakening either side reddens independently. Keep
`bootstrap/tests/test_lifecycle_contract.py` in the later gate-manifest
classification and Maintainer ceremony exactly as Chunk I already requires.

### Security closure accounting

Retiring the exception closes M1 and removes the entire reusable-bypass risk.
The contained loaders, terminal encoder, intent subprocess, assurance matrix,
pilot evidence, migration authority, restart rules, and conditional P7
ceremony remain closed. The two sibling plans retain separate scopes and trust
roots; the new map does not merge or weaken their gates.

**Covered**: exact code and tests at `286f07d`; direct current and adversarial
fixture execution; old/new 37-plan corpus comparison; twin identity; current
gate preconditions; accepted Code-review `Answers:` contract; and frozen-path
classification. The Maintainer's authorization is accepted as stated.

**Not covered**: A--H implementation bytes, full-suite behavior, actual final
Code review, pilot observations, or re-anchor execution. Return O1 only. This
pass is blocking and does not clear the External Security Review obligation.

## Response to plan review -- Claude -- 2026-08-11 (round 6 + Security round 5)

**Obligations answered**: both passes above — External round 6 ([N1], [N2]) and
External Security Review round 5 ([O1]). One Response, one group, per the rule
`286f07d` landed.

**Disposition: 3 accepted, 0 declined.** [N1] and [O1] are the same defect
through two lenses and are fixed by one change; [N2] is a number, and I
re-derived it rather than accepting it.

### [N1] / [O1] — accepted. Chunk B did contradict the landed rule.

Verified textually rather than taken on report. B2 read, verbatim:

> a disposition after the later pass must not satisfy the earlier

`286f07d` makes exactly that disposition satisfy exactly that pass. The two
cannot both hold, and an implementer following B2 would have restored the false
ceiling the Maintainer had just directed away — while the suite went green,
because B2's own mutation would have pinned the wrong direction.

Both reviews independently identified the right fix, and it is now in Chunk B:
**split by record type**, because the two types genuinely need opposite rules.
A Plan review is answered as a *round*, so grouping is correct. A Code review's
findings are answered *individually*, so `code-review-blindness` R2/R4 requires
exact `Answers:` binding. The generic assertion was wrong precisely because one
sentence cannot describe two opposite directions.

* **B1** keeps raw conforming boundaries canonical for every pass *body*, both
  record types — unchanged, and orthogonal to disposition.
* **B2** pins the landed group rule for Plan-review Responses; `### Sharpening`
  stays scoped to its own pass. It **pins** `286f07d`, it does not redesign it.
* **B3** carries the Code-review exact `Answers:` binding, with malformed,
  ambiguous, absent and wrong-pass bindings all refusing.
* **B4** carries the body mutation **plus two opposing disposition mutations**,
  so weakening either rule toward the other reddens independently. [O1] asked
  for this specifically and it is the part most likely to be quietly dropped: a
  single falsifier would let a future implementer collapse the two rules again.

**The review-range gap is accepted and closed in `## Verification`.** [O1] is
right that this is the sharper half. Chunk B now *depends* on bytes that landed
before this plan's `executing` transition, so a Code-review range starting at
B1 would leave the gate change the plan relies on outside the only independent
review it ever receives. Boundary C's target now must begin at or before
`286f07d` — `286f07d^..<B1 commit>` or a provably equivalent range — and the
commit is named in both Boundary B ledgers.

**The structural residual [O1] names is accepted as stated and not papered
over**: an empty or semantically incomplete exact Response still satisfies the
parser. That was already true of an immediately-positioned Response; the tool
attests record *shape*, never whether the author answered the prose. Git review
remains the semantic channel. Grouping widens the blast radius of that residual
from one pass to a round, and that is the honest cost of removing the deadlock.

### [N2] — accepted, and re-derived; the corrected number is four.

Executed rather than reasoned. Loading the pre- and post-`286f07d` planner
modules and running each over the 37-plan corpus, **only this artifact changes**,
and the unsatisfied raised passes are:

| rule | unsatisfied passes |
|---|---|
| pre-`286f07d` | rounds **2, 3, 4, 5**, plus round 6 and Security round 5 |
| post-`286f07d` | round 6 and Security round 5 only |

So the rule change closed **four**, matching [N2] exactly — and confirming its
mechanism: round 1 was answered before the first Security pass, so it never
became a violation, and no Security pass ever did. The operative account now
says four.

**Two figures, and why they differ from the review's `4 -> 0`.** Measured today
the corpus reads **6 → 2**, not 4 → 0. Both are correct at their own commit: the
review measured at `7f5682b`/`3005c39`, before its own two passes existed; the
two passes above are themselves undispositioned raised passes, and *this
Response* is what closes them. The rule-attributable delta is **four** either
way. Recording it because a later reader comparing the two numbers would
otherwise have to rediscover why they disagree.

Per [N2], the append-only historical Response that says "five rounds, five
violations" stays as written. It was wrong when written; the record shows what
was believed at each point, and only the operative account is corrected.

### What this Response does not do

It does not clear either obligation. Both passes declare themselves blocking,
the plan stays `open`, and `required(External + External Security Review)` still
wants a clearing pass on each track. No implementation commit is authorized by
this Response.

## Plan review -- Codex -- 2026-08-11 (round 7)

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External
**Reviewed commit**: `f0a716bbca273a8f9b86ce0074eec569b036e1f2`
**Target**: closure of N1 and N2 against the revised executable contract
**Prior findings**: N1, N2
**Assurance path**: high-assurance
**Findings**: none
**Verdict: SHIP.** N1 is closed in the Chunk B contract, not only in the
Response: B1 keeps raw boundaries canonical for both pass bodies, B2 preserves
the landed grouped Plan-review Response rule, B3 separately requires exact
Code-review `Answers:` binding, and B4 requires independent falsifiers in both
directions. N2 is corrected to four in the operative account and the current
Response accurately explains the later `6 -> 2` observation without making
that transient count authoritative.

Direct execution under Python 3.13.13 reports this plan structurally sound,
`lifecycle_planner.py scan` reports all eight active artifacts sound, the
planner twins are byte-identical, and all 77 focused lifecycle-contract tests
pass. The fresh two-pass/one-Response fixture clears; a pass after that Response
and a group with no Response still refuse.

The final Code review's "equivalently exact range" may and should be an exact
**union**: `286f07d^..286f07d` for the pre-landed repair plus the plan's actual
implementation range through Boundary B1. A single contiguous range is also
correct but already includes 34 unrelated intervening commits and would spend
review attention without increasing coverage. This is an interpretation of the
alternative the Verification section already permits, not a new review pass or
a scope change; both exact ranges are reviewed in the plan's one Boundary C
pass and named in both Boundary B ledgers.

**Closure accounting.** All prior External findings E1--E4, G1--G4, H1--H3,
J1, L1, L2, N1 and N2 are closed. The plan keeps every accepted parent chunk,
preserves the two sibling plans' independent gates, and leaves the final Code
review, Maintainer ceremony, second Boundary B run, pilot activation and
conditional promotion in their proper later phases. This pass clears the
External obligation.

**Covered**: exact plan bytes at `f0a716b`; the N1/N2 revisions; direct planner
and corpus-scan execution; 77 focused tests; twin identity; the pre-landed
repair diff; and the final review-range contract.

**Not covered**: implementation bytes, future Code review, full-suite behavior,
pilot observations, or the Maintainer re-anchor. Those remain execution-phase
obligations and do not block plan approval.

## Plan review -- Codex (Security) -- 2026-08-11 (round 6)

**Model**: GPT-5.6-Codex
**Tier**: External
**Obligation**: External Security Review
**Reviewed commit**: `c72c4958c0e5307286232e6b03146f5564e3b409`
**Target**: closure of O1 against the separately committed External SHIP pass
and the final gate-repair review binding
**Prior findings**: O1
**Assurance path**: high-assurance
**Security lens**: governance-gate fail-closed behavior, response binding,
review-target completeness, frozen-path restart, and residual authority
**Findings**: none
**Verdict: SHIP.** O1 is closed. Chunk B now preserves the exact grouped
Plan-review Response rule at `286f07d`, specifies the opposite exact-binding
rule for Code-review Responses, and requires independent mutations so neither
can be weakened into the other unnoticed. The Verification contract includes
the pre-landed repair in Boundary C and both Boundary B ledgers; the External
pass's exact-union interpretation supplies full byte coverage without burying
the security-relevant commit among unrelated work.

I re-attacked the landed rule under Python 3.13.13. One exact Plan-review
Response clears the raised passes above it; a pass after the Response refuses;
no Response refuses; unrelated Response kinds do not discharge the pass; all
77 focused lifecycle-contract tests pass; and the planner twins remain
byte-identical. The future Code-review side is not implemented yet, so security
acceptance is of the reviewed contract: absent, malformed, ambiguous and
wrong-pass `Answers:` values refuse, and B4 requires the weakening mutation to
red independently from the Plan-review grouping mutation.

The accepted residual is accurately bounded. A syntactically exact but
semantically empty Plan-review Response can satisfy the structural gate, and a
grouped Response can now do so for the round. The mechanism authenticates
record shape, not intellectual adequacy; the independent Git review remains
the semantic control. This does not create a hidden execution authority or
weaken the later Code-review binding.

**Security closure accounting.** All prior Security findings S1--S6, T1--T4,
K1, M1 and O1 are closed. Contained loader identity and cleanup, terminal
encoding, immutable pilot activation, append-only source-bound events,
expected-old writes, migration blob checks, non-expansion binding, the
governed-byte restart rule, frozen-file ceremony and conditional P7 review all
remain explicit. This pass clears the External Security Review obligation.
Together with External round 7, both pre-implementation review obligations are
now satisfied; the plan may advance through its recorded status transitions.

**Covered**: exact plan bytes at `c72c495`; `286f07d` code, tests and commit
boundary; direct adversarial rule execution; 77 focused tests; twin identity;
Chunk B's opposing contracts and mutations; Boundary B/C targeting; and the
frozen-path restart disposition.

**Not covered**: future implementation bytes, execution of the Code-review
binding, full-suite behavior, pilot evidence, or the Maintainer ceremony. Those
are deliberately later controls and require their own recorded evidence.
