<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/plans.md doctrine/proposals.md doctrine/lifecycle-contract.md doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: dev/.cairn/pilot-state.json, tools/__init__.py -->
<!-- Both paths above are PERMANENT exemptions, not forward references, and
     neither is expressible as a typed declaration -- which is why H2's
     metadata migration kept them while retiring the rest.
     `tools/__init__.py` is cited BECAUSE it must never exist -- A3/A5's
     no-package-shortcut clause -- so there is no path for a declaration to
     register.  `dev/.cairn/pilot-state.json` is cited by the landed,
     append-only Security review, and the revision that review prompted
     replaced that path with the two `dev/measurement/` records; the review
     section is immutable, so the citation is marked rather than edited.
     Chunk H2 retired three now-redundant entries, each measured rather than
     assumed -- removing them produced zero new claim_check flags, and D4
     independently classified all three as `migration item`, not stale debt:
     the `dev/measurement/pilot-activation.md` glob (`resolved-by-registry` --
     the `Proposed paths:` declaration below authorizes every occurrence it
     suppressed), the `dev/plans/corpus-tier-cost.md` glob, and that path's own
     `Proposed paths:` bullet (both `resolved-by-archive` -- D1's exact archive
     rule resolves every occurrence through `dev/plans/archive/`).
     Chunk F's `bootstrap/tests/test_lifecycle_board.py` had already dropped
     both of its declarations when it landed, per the same rule: a materialized
     path leaves a stale declaration that `check_cairn` reports, so the drop
     belongs in the commit that lands the file. -->

# Plan: one lifecycle contract, one evidence boundary

**Source proposal**: [`review-efficient-lifecycle`](../proposals/archive/2026-08-10-codex-review-efficient-lifecycle.md),
executing jointly with its three accepted amendments —
[`claim-check-exemption-hygiene`](../proposals/archive/2026-08-10-codex-claim-check-exemption-hygiene.md),
[`code-review-blindness`](../proposals/archive/2026-08-10-claude-code-review-blindness.md),
and [`lifecycle-status-vocabulary`](../proposals/archive/2026-08-10-codex-lifecycle-status-vocabulary.md).
All four are `accepted`, and three of them state in their own accepted text
that they open no standalone plan. This is that plan.
**Status**: implementing
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
- `dev/measurement/pilot-activation.md` — P6a's immutable activation record; introduced by P6d.

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
A   central vocabulary + contained loaders         [DONE 1c68926 b0e92fd ca22f21 94bda8b]
B   canonical pass boundaries                      [DONE 1329b22 B1/B2; da23dbc B3]
P1  assurance paths + four-field review basis      [DONE 76bc678]
C   Code-review record schema + legacy manifest    [DONE C3 0935a09; C1/C2/C4/C5 36b0c53]
P5  Contract non-expansion attestation             [DONE 772c14d; CF2 840d807]
D   claim-check archive resolution + registry      [DONE 4723107 D1/D2/D5; 6869022 D3/D4]
E   status vocabulary, transitions, conformance    [DONE ec6139e E1/E2/E3]
P2  plan readiness, inheritance, expansion refusal [DONE b00ab89 P2-R + [CF1]]
P3  current-contract revision + withdrawal ledger  [DONE b3d17a5; CF5 filed]
P4  review-brief + closeout --dry-run              [DONE 6bc33d2; CF6 filed]
P6a pilot engine + state schema (in reviewed range)[DONE 8bf1154]
P6b pilot human contract                           [commit pending]
P6c pilot mutation tests                           [commit pending]
F   the derived board                              [commit pending]
G   doctrine, templates, agent teaching            [DONE 5257bde G1 + CF5; 7d9594a G2; 94f13d1 G4; 45ad708 G3; 43df6fd G5]
H   migration + source-proposal archive            [commit pending]
--- stable bytes ---------------------------------------------------
B1  Boundary B on the pre-review commit            [record]
CR  independent Code review over that range        [review]
I   Maintainer re-anchor of the reviewed frozen set[M1]
B2  Boundary B + closeout on post-ceremony commit  [record]
--- pilot ----------------------------------------------------------
P6d pilot ACTIVATION (data-only, Maintainer-gated)  [M2]
P7  post-monitoring retain/revise/retire           [M6-R; own evidence]
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
| P6b | `dev/collaboration_agreement.md` + twin | the pilot's human contract: pause conditions, evidence report shape, and a description of the Maintainer's `retain | revise | retire` Decision at the monitoring boundary (**not** a *promotion* Decision -- that token is retired by `M6-R`; see the 2026-08-11 revision). **Agent-authored**, inside the reviewed range — describing the Decision is not taking it; the Decision itself is M6 |
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

       **Tier**: <Internal|External>   <-- closed vocabulary, exact match
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

## Maintainer-directed contract revision -- 2026-08-11

This section is an append-only sequence revision made after execution began. It
supersedes the affected P2, G, P6, P7, P8 and M6 cells where they conflict. It
does not alter completed Chunk A work or reopen the External and Security SHIP
passes over the unchanged parts of this plan.

The Maintainer's direction, quoted verbatim:

> The problem is that throwing external plan + code review in creates multiple
> hurdles to development, and slows the process down immensely. The proposal is
> where the deliberative weight should reside.

> I am completely fine with the policy change here. We are doing everything
> possible to reduce the burden that Cairn's machinery creates while balancing
> quality. So, go ahead and make this change

And the process disposition, also verbatim:

> I really don't want a proposal. I just want this changed. Please watch for
> when the files are available and make your changes

This is the explicit Maintainer authorization for the deviation from the
accepted pilot-first contract. No separate proposal is opened. The revision
itself receives one fresh-context **Internal** plan review before revised P2
executes; A through E may continue while that review is obtained. This is the
review allocation being adopted, applied to its own implementation rather than
requiring the External plan round it removes as a default.

### The default review allocation

The proposal is the deliberative boundary. When an **External proposal review**
has reviewed a complete current contract and records `Plan readiness: READY`,
the derived plan receives a fresh-context **Internal plan review**, not another
different-agent-type External round.

The plan carries both facts separately:

```text
Plan review: required(Internal)
Inherited proposal basis: review=<full External-review commit>;
                            proposal=<full accepted commit>
```

The Internal reviewer checks faithful translation into files, chunks,
sequencing, tests, omissions, failure dispositions and Maintainer fences. It
does not reopen the accepted design. A new scope item, invariant, public path,
failure disposition, trust boundary, scientific assumption or ceremony
invalidates readiness and stops implementation until the change returns to the
proposal boundary or a distinct review is explicitly required.

`Plan readiness: DISTINCT REVIEW REQUIRED` still requires a separate plan
review at the tier named by the proposal/Decision. The proposal reviewer uses
it when consequential design necessarily remains for planning. It is an
explicit finding about the contract, not a default inferred from the topic.

**Assurance path no longer decides plan-review independence.** Standard and
high-assurance proposals may both receive `READY` when their External review
settled the complete contract. High assurance continues to govern verification,
Security Review, scientific review, protected-surface handling, risk acceptance
and ceremonies. It does not automatically purchase a second External read of a
plan that only translates already-reviewed decisions.

### Code review is unchanged

Current doctrine already sets the ordinary Code-review floor at **not the
implementing agent**, not at different agent type. A same-type agent in an
independent context may perform it. External or Security code review remains an
explicit escalation for implementation risk not resolved at proposal review;
this revision neither removes Code review nor adds a universal External code
review.

### Pilot becomes monitoring, not permission

The machinery and evidence work in P6a--P6d remain in scope. Their purpose
changes from deciding whether the review allocation may become the default to
monitoring a default that is already active:

* G teaches the proposal-centered allocation in Cairn's self-hosted surfaces
  and the shipped templates in the reviewed implementation range. There are no
  existing adopters and therefore no migration or compatibility branch.
* P6d activates the bounded evidence window only. It does not activate the
  review policy.
* The six-plan / 60-day report still measures review input, removed
  transitions, escaped findings, Maintainer prompts and pauses.
* M6 becomes a `retain | revise | retire` Decision at the monitoring boundary,
  not a promotion Decision. `retain` requires no second distribution change;
  `revise` or `retire` executes P7 against the same changed-path,
  Boundary-B/Code-review and ceremony classification already specified.

This keeps the evidence and rollback mechanism the accepted proposal paid for,
without making the efficiency improvement wait for permission from its own
pilot.

### Superseding chunk cells

| Cell | Revised executable contract |
|---|---|
| **P2-R** | Implement the two-field inheritance shape above. `READY` requires an exact External proposal-review commit, the exact accepted proposal commit, and a fresh-context Internal plan review. Remove the automatic high-assurance refusal. `DISTINCT REVIEW REQUIRED`, a mismatched binding, or any declared expansion refuses. |
| **G-R** | Teach the proposal-centered default immediately in canonical, self-hosted and shipped operational surfaces. State plainly that plan review is Internal after an External proposal `READY`, Code review's floor is a non-implementer, and External plan/code review is explicit escalation. |
| **P6-R** | Preserve activation, ledger, report, pause and mutation machinery; relabel it as monitoring evidence. No reader or writer may treat absent monitoring activation as disabling the review policy. |
| **P7-R** | `retain` is a no-op disposition over already-distributed policy. `revise` and `retire` remain conditional implementations with their existing evidence and classification requirements. |
| **P8-R** | Add the matrix below and replace tests whose oracle is “high assurance can never inherit.” Preserve every binding, expansion, uncertainty, malformed-record and downgrade mutation not contradicted here. |
| **M6-R** | At the six-plan / 60-day boundary the Maintainer chooses `retain`, `revise` or `retire`; no promotion gate remains. |

### Required test matrix

The revised P8 acceptance matrix proves at least:

* External proposal `READY` plus exact Decision binding plus Internal plan
  review clears, for both standard and high-assurance fixtures;
* same proposal with no Internal plan review refuses;
* an Internal proposal review cannot supply the inherited External basis;
* changed review or accepted-proposal SHA refuses;
* `DISTINCT REVIEW REQUIRED` cannot be satisfied by the Internal plan pass;
* every declared expansion dimension still invalidates readiness;
* an absent monitoring activation record does **not** restore distinct External
  plan review or disable the policy;
* Code review still requires a non-implementer and is not silently upgraded to
  External by this routing change; and
* `revise` / `retire` after monitoring retain P7's evidence and restart rules.

### Scope and verification effect

This revision changes review allocation and rollout, not the accepted outcome:
bounded contracts, exact review binding, independent implementation review and
measured evidence remain. It removes one routine cross-type reread between an
External proposal review and implementation. All implementation bytes produced
for this revision remain inside this plan's existing B1, Code-review, M1 and B2
boundaries. The final Code review must name this section in its reviewed
contract and falsify at least the wrong-tier, wrong-SHA, high-assurance-READY
and monitoring-absent cases rather than treating the table's presence as proof.

## Plan review -- Claude -- 2026-08-11

**Model**: Claude Sonnet 5 (claude-sonnet-5)
**Tier**: Internal
**Obligation**: the Maintainer-directed contract revision's own fresh-context
Internal plan review
**Reviewed commit**: `da23dbca99b567026296300ad86988b2b1d68566`
**Target**: the 2026-08-11 Maintainer-directed contract revision
**Findings**: raised

**Method.** Fresh context; nothing inherited from the authoring session. Read
`AGENTS.md` in full, this plan's header, `## The review budget`, `##
Maintainer interventions`, `## Sequence`, the P1--P8 chunk table, `##
Acceptance criteria`, `## Verification`, both clearing passes (round 7
External, round 6 Security), and the revision section itself in full. Read
`doctrine/dual-review.md` in full for the structural-independence floors,
Code-review floor, and the standing recommend-and-decide instrument. Read the
parent proposal `dev/proposals/2026-08-10-codex-review-efficient-lifecycle.md`
sections 1--3 (assurance paths, the four-field basis, the original
inheritance/high-assurance-refusal design) to understand exactly what the
revision changes relative to what was accepted. Grepped the whole plan file
for `promotion`, `high.assurance`, `External plan`, `distinct review` and
`cross-type` to hunt for surviving contradictions outside the named
superseded cells. Ran `tools/lifecycle_planner.py scan` (all 8 artifacts
structurally sound) and `scripts/claim_check.py` against this file (clean)
directly against the current tree.

**Verdict: REVISE.** The revision is implementable and internally consistent
in its core mechanism -- the two-field `Inherited proposal basis`, the
`DISTINCT REVIEW REQUIRED` escape valve, and the unchanged Code-review floor
are all precise enough to execute as written, and M1/M2 are verified
untouched (below). But the superseding table does not reach every place the
old contract's assumptions still live, one of the six invalidating triggers
is defined at the wrong grain to catch the exact risk the parent proposal
built the high-assurance path to stop, and the required test matrix has a
shape-shaped hole where the old row-level matrix had an oracle. None of this
reopens the Maintainer's policy choice; each finding is a text-only
tightening inside P2-R/G-R/P8-R's own chunks, addressable without another
round.

**Steelman first.** The core trade is honestly stated, not smuggled: the
revision states plainly that it "removes one routine cross-type reread," it
does not touch Code review's independence floor, it keeps M1's ceremony and
M2's data-only activation exactly where they were, and it converts the old
promote/revise/retire vocabulary to retain/revise/retire without inventing a
new mechanism -- P6a--P6c's engine, ledger, report, pause and mutation
machinery survive by relabeling, not rewrite. The standing `recommend-and-
decide` instrument (`doctrine/dual-review.md`, "Recommend-and-decide -- the
second independent pass") is untouched by this revision and remains a live
escape hatch: any reviewer, including a future Internal one, can still
recommend a cross-type second pass to the Maintainer at any point, so "no
independent read ever" is not literally true even under the new default --
it is "no independent read *by default*." And the revision is honest about
its own residual authority: it does not claim the six-item invalidation list
is exhaustive protection, it describes the pilot/monitoring machinery
accurately as evidence rather than permission, and it correctly keeps this
very self-review as a precondition on P2 rather than skipping review of
itself.

### [R1] The high-assurance READY removal is checked at the wrong grain --
translation fidelity, not sequencing risk

The parent proposal's own words for why high-assurance was excluded from
inheritance: *"High-assurance plans cannot inherit plan readiness. They
retain a distinct plan review because sequencing itself can create risk even
when the proposal is sound"*
(`dev/proposals/2026-08-10-codex-review-efficient-lifecycle.md:171-173`).
That is a claim about a **fully faithful** translation still being
dangerous -- risk introduced by *how* a sound design is sequenced into
chunks, not by any deviation from the design. The revision's own mitigant is
the six-item invalidation list -- *"a new scope item, invariant, public
path, failure disposition, trust boundary, scientific assumption, or
ceremony invalidates readiness"* (line 2464) -- which by construction only
fires on an *addition* relative to the proposal. A plan that sequences a
faithful translation of a high-assurance design into a *dangerous order*
(the exact failure class B4/H/I exist in this very plan to catch) trips none
of the six items and would clear an Internal-only pass, precisely because
the Internal reviewer's charter is *"it does not reopen the accepted
design."* Under the pre-revision contract this was exactly what the
mandatory distinct (External-tier, per this plan's own opening line 24 and
`doctrine/dual-review.md:181-187`) plan review existed to catch, independent
of translation fidelity.

The revision's compensating claim -- *"High assurance continues to govern
verification, Security Review, scientific review, protected-surface
handling, risk acceptance and ceremonies"* (line 2475-2477) -- only actually
backstops one of the parent's five original high-assurance trigger
categories. Checked against `AGENTS.md`'s "High-risk surfaces" list
(`AGENTS.md:372` onward): a *security trust boundary, credential, executable
path, parser, or network boundary* trigger keeps an independent fallback via
the named-protected-surface Security-Review fences (M3-style). The other
three original trigger categories --- *"a scientific assumption ...  that
can change reported results"*, *"a destructive migration, data-loss risk,
public compatibility break"*, and *"a governing doctrine or
lifecycle-enforcement change"*
(`dev/proposals/2026-08-10-codex-review-efficient-lifecycle.md:80-84`) ---
have no AGENTS.md-named fallback at all once plan review is Internal-only;
"scientific review" and "risk acceptance" are named in the mitigant sentence
but neither is a defined mechanism anywhere in this plan or in
`doctrine/dual-review.md` as read. Concretely: a future high-assurance
proposal whose trigger is a doctrine/lifecycle-enforcement change (this
revision's own P2/G work is itself exactly that category) can reach
implementation behind nothing but one same-agent-type Internal pass, with no
structural requirement that anyone independent ever sees the sequencing.

**Required satisfier.** State this trade-off explicitly rather than
implicitly, in the same section that removes the refusal: name which of the
five original high-assurance trigger categories keep an independent-review
backstop elsewhere (security-trust-boundary, via AGENTS.md's named
surfaces) and which now rely solely on the Internal reviewer's judgment plus
the optional `recommend-and-decide` escalation (scientific-assumption,
destructive-migration/data-loss/compatibility-break,
doctrine/lifecycle-enforcement-change). This can land as a one-paragraph
addition to this revision section or as part of P2-R/G-R's `dual-review.md`
text -- it does not require reopening the policy.

### [R2] Silent scope reduction during translation is not one of the six
invalidating triggers

The six items that invalidate `READY` (line 2464) guard against *additions*
a translation makes beyond the proposal. They say nothing about a
translation that **narrows** an accepted proposal's committed scope --
exactly the failure class `AGENTS.md` was sharpened for in this same
session: *"Removal counts as a deviation, in both directions ... A reviewer
cannot create that authority by calling the remainder 'out of scope.'
Narrowing is the path of least resistance in review -- it costs the
reviewer nothing, reads as prudence, and can never be shown wrong, because
the wider version is never built"* (`AGENTS.md:169-176`; see also the
concurrently-landed `scope-reduction-trap` work, commit `3f92cd8`). The
Internal plan reviewer's charter -- *"it does not reopen the accepted
design"* -- is exactly the posture in which narrowing is easiest to wave
through as a faithful-looking translation choice, and under the new default
this reviewer is the *only* read most plans will get before implementation.

**Required satisfier.** Add "a scope reduction or removed accepted outcome
relative to the proposal's committed scope, absent a Maintainer-recorded
`Scope delta` allowance per `AGENTS.md`" to the list of items that
invalidate readiness (alongside the existing six), and add a corresponding
bullet to the required test matrix. This is additive to P2-R/P8-R, not a
redesign.

### [R3] Stale "promotion" language survives in two live locations the
superseding table does not name

The superseding table's cells are the P1--P8 table rows and the M-table row;
two other locations still describe the retired `promote` disposition and are
not literally any of "P2, G, P6, P7, P8 and M6 cells" even though they carry
the same content:

* `## Sequence`'s ASCII diagram, the P7 line: *"P7  post-pilot promotion /
  retirement              [M6; own evidence]"* (line 299). Post-revision,
  `promote` no longer exists as a disposition (`M6-R` / `P7-R` replace it
  with `retain`/`revise`/`retire`), so this line now names a removed token,
  not merely an imprecise one.
* Chunk P6b's own row: *"the pilot's human contract: pause conditions,
  evidence report shape, and a description of the Maintainer promotion
  Decision at the boundary"* (line 482). `P6-R`'s *"relabel it as monitoring
  evidence"* only reaches this by inference through the separate `M6-R`
  bullet; it does not say in so many words that P6b's authored prose must
  now describe a retain/revise/retire Decision rather than "the promotion
  Decision." P6b has not landed yet (`commit pending`), so an implementer
  copying this row's wording into `dev/collaboration_agreement.md` risks
  writing the retired term into the shipped contract.

**Required satisfier.** A one-line correction to each location (or folding
both explicitly into the superseding table as named cells) closes this --
no design question, purely a stale-reference cleanup of exactly the kind
Chunk G's own acceptance criteria already check for elsewhere in this plan
("no second restart rule exists anywhere in this plan", line 598-599).

### [R4] "A through E may continue" does not name two chunks that sit in
that exact span

`## Sequence`'s dependency order is `A, B, P1, C, P5, D, E, P2, ...` (lines
275--300). P1 and P5 are neither superseded by this revision nor excluded
from "may continue" by anything the revision says -- they simply are not
named. A literal reading of *"A through E may continue while that review is
obtained"* (line 2441-2442) leaves an implementing agent to infer, rather
than be told, that P1 (`commit pending`) and P5 (`commit pending`), which sit
between C and D in the load-bearing order, are also authorized to proceed.

**Required satisfier.** Reword to name the actual pre-P2 span explicitly --
e.g. "every chunk preceding P2 in the Sequence order (A, B, P1, C, P5, D,
E)" -- removing the inference step.

### [R5] The required test matrix has no malformed-shape fixture for the new
two-field basis

The old row-level assurance matrix this table replaces explicitly required
*"missing / duplicate / unknown `Assurance path` values (all refuse --
**never default to `standard`**)"* (line 486). The new matrix's closest
analog is *"changed review or accepted-proposal SHA refuses"* (line 2530) --
which covers a *mismatched* SHA but not an absent, half-present (only
`review=` or only `proposal=`), or unparseable `Inherited proposal basis`
field. `P8-R`'s *"preserve every ... malformed-record ... mutation not
contradicted here"* (line 2519) cannot preserve a test for a field shape
that did not exist before this revision.

**Required satisfier.** Add to the required test matrix: "a malformed or
partially-specified `Inherited proposal basis` (only one sub-field present,
unparseable commit id, wrong field name) refuses and never defaults to
`READY`."

**Second-round recommendation.** Recommended, narrowly, and not blocking.
R1 and R2 concern the review-independence axis and the scope-reduction
failure mode this very repository is actively hardening against elsewhere
this session; the Maintainer already explicitly authorized skipping a
distinct plan-review round for *this* revision, so I do not gate P2 on a
cross-type read of my own findings. But once P2/G land, a cross-type or
human second look at R1/R2's disposition (folded into the plan's Code review
or flagged separately) would be consistent with `AGENTS.md`'s own
rate-limit-gate rationale for doctrine changes and with the fact that this
change touches the mechanism that decides when such a second look happens at
all.

**Covered by execution/inspection**: the revision section in full
(2417--2548); the P1--P8 chunk table (327--513) and Maintainer interventions
table (50--133), confirming M1/M2 mechanically untouched and M0 irrelevant
here; `## Sequence` (270--326); `## Acceptance criteria` / `## Verification`
(514--602); both clearing passes (2314--2416) read to confirm nothing here
reopens them; a full-file grep for `promotion`, `high.assurance`, `External
plan`, `distinct review`, `cross-type` to find surviving contradictions;
`dev/proposals/2026-08-10-codex-review-efficient-lifecycle.md` sections 1--3
(lines 60--248) for the original inheritance/high-assurance design this
revision changes; `doctrine/dual-review.md` in full for the independence
floors, Code-review floor, and recommend-and-decide; `AGENTS.md`'s deviation
and High-risk-surfaces sections; direct execution of
`tools/lifecycle_planner.py scan` (8/8 sound on the tree before this pass was
appended) and `scripts/claim_check.py` against this file, clean of anything
this pass's own text introduces. Both are re-run after this pass lands, and
their post-append state is exactly what a `**Findings**: raised` pass with no
disposition yet should show -- see the note after **Not covered**, below.

**Not covered**: `dev/proposals/2026-08-10-codex-lifecycle-status-vocabulary.md`
beyond a grep for `retain`/`revise`/`retire`; `dev/collaboration_agreement.md`,
`doctrine/dual-review.md`'s and `AGENTS.md`'s own future edited text, since
P2/G have not executed and there is nothing yet to falsify there;
implementation of P1--P8, B1, Code review, M1, B2 or pilot evidence, all
explicitly execution-phase; the sibling plans and the two files another
session has modified (`bootstrap/tests/_gate_manifest.py`,
`bootstrap/tests/test_gate_manifest.py`), untouched per instruction; whether
bypassing the proposal boundary for this revision was itself the right call,
out of scope per this review's charge; and a structurally-independent
(cross-type) read of this review's own findings -- see the second-round
recommendation above.

**Note on post-append verification state.** After this pass lands,
`tools/lifecycle_planner.py scan` correctly reports this artifact as carrying
a structural violation -- `**Findings**: raised` with no `### Sharpening` or
`## Response to plan review` yet -- and that is this pass doing its job, not
a defect: it is the mechanical form of "revised P2 does not execute until
this review is obtained and answered." `scripts/claim_check.py` separately
reports pre-existing, unrelated hard flags on this file's `Proposed paths:`
declarations (lines 2, 211, 217) for `bootstrap/tests/test_lifecycle_vocabulary.py`
and `dev/plans/git-native-security-foundations.md`, both of which have
already materialized; those declarations predate this pass, are caused by an
in-flight, uncommitted edit to `scripts/claim_check.py` and its twin by
another concurrent session, and are outside this review's target. This
pass's own added text introduces no claim-check flag.

## Response to plan review -- Claude -- 2026-08-11

**Model**: Claude Opus 5 (`claude-opus-5`)
**Reviewed review commit**: `62e2db2`
**Obligation answered**: the Maintainer-directed contract revision's own
fresh-context Internal plan review
**Disposition**: accept [R1]--[R5]. All five are text-only and additive; none
reopens the Maintainer's policy decision, and none required a redesign. The
amendments below are **binding on P2-R, G-R and P8-R** and are stated here rather
than edited into the Maintainer's own revision section, whose authorizing quotes
must stay verbatim.

### [R3] -- accept, and fixed inline, because it named a *retired token*

Two live locations still spoke of a `promote` disposition that `M6-R` had
removed. Left alone, an implementer copying P6b's row into
`dev/collaboration_agreement.md` would have written a retired token into a
shipped adopter contract. Corrected:

* `## Sequence`, the P7 line -> `P7  post-monitoring retain/revise/retire
  [M6-R; own evidence]`.
* Chunk P6b's row -> now names the `retain | revise | retire` Decision at the
  **monitoring** boundary, and says explicitly that *promotion* is retired.

This is the class of stale-reference cleanup Chunk G's own acceptance already
checks for elsewhere in this plan, and the reviewer was right that the
superseding table did not literally reach either location.

### [R1] -- accept. The trade-off is now stated where the refusal was removed.

**Amendment A (binds G-R's `doctrine/dual-review.md` text and this plan's
record).** Removing the automatic high-assurance refusal removes the *plan's*
only mandated independent read for some triggers but not others, and the
difference is now named rather than left implicit. Of the five original
high-assurance trigger categories:

* **security / trust-boundary** -- keeps an independent backstop **outside**
  this plan: `AGENTS.md`'s named high-risk surfaces each require a Security
  Review, and fence **M3** already stops implementation that touches
  `_resolve_interpreter`. Unchanged by this revision.
* **scientific-assumption**, **destructive migration / data-loss /
  compatibility-break**, and **doctrine or lifecycle-enforcement change** --
  now rely on the fresh-context Internal reviewer's judgement plus the
  *optional* `recommend-and-decide` escalation in `doctrine/dual-review.md`.
  There is no structural requirement that a different agent type ever reads the
  sequencing.

The reviewer's sharpest point is that this revision's **own** P2/G work falls in
the third category, so the policy change is being made under the allocation it
installs. That is exactly what the Maintainer authorized and it is recorded in
their quoted words; naming it here means a later reader sees the reflexivity
rather than discovering it.

### [R2] -- accept, and this is the finding I would have missed.

**Amendment B (binds P2-R and P8-R).** A seventh item joins the six that
invalidate `READY`:

> a **scope reduction or removed accepted outcome** relative to the proposal's
> committed scope, absent a Maintainer-recorded `Scope delta` allowance per
> `AGENTS.md` > *Git and commit workflow*.

And the required test matrix gains: *a plan whose chunk table drops an outcome
the accepted proposal committed to refuses, and a recorded `Scope delta`
allowance is the only thing that admits it.*

The six existing triggers all guard against a translation **adding** something.
Narrowing was unguarded — and the Internal reviewer's charter ("it does not
reopen the accepted design") is precisely the posture in which a quiet narrowing
reads as a faithful translation choice. `AGENTS.md:169-176` was sharpened against
this exact failure in this same session, and the concurrently-landing
`scope-reduction-trap` work exists for it. Under the new default this reviewer is
the only read most plans get before implementation, so the asymmetry mattered
more here than it would have under the old allocation.

### [R4] -- accept. The inference step is removed.

**Amendment C.** "A through E may continue" is read as **every chunk preceding
P2 in the `## Sequence` order — A, B, P1, C, P5, D, E**. P1 and P5 sit inside
that span, are neither superseded nor excluded, and were previously left to
inference. This matters operationally right now: P1 is the next chunk in
dependency order.

### [R5] -- accept. The new field gets the shape tests the old one had.

**Amendment D (binds P8-R).** The required test matrix gains: *a malformed or
partially-specified `Inherited proposal basis` — only one sub-field present, an
unparseable commit id, or a wrong field name — refuses, and never defaults to
`READY`.* The reviewer is right that `P8-R`'s "preserve every malformed-record
mutation" cannot preserve a test for a field shape that did not exist before the
revision, and that "changed SHA refuses" covers mismatch but not absence.

### Second-round recommendation -- noted, not gated

The reviewer recommended, narrowly and non-blockingly, a cross-type or human
second look at [R1]/[R2]'s disposition once P2/G land. Recorded rather than
actioned: the Maintainer authorized internal delegated review for this work, and
the plan's single Code review already must name the revision section and falsify
its wrong-tier, wrong-SHA, high-assurance-`READY` and monitoring-absent cases.
Amendments A and B are the surfaces that read should attack first.

### Verification of this Response

`lifecycle_planner scan` returns to **all artifacts sound** with this Response
landed — the 7/8 the reviewer honestly reported was their own raised finding
awaiting disposition, which is the mechanism working, not a defect.

## Carried-forward obligations -- Claude (Implementation) -- 2026-08-12

Two things surfaced during execution that belong to a **later** chunk and would
otherwise be lost between agents. Recorded here so the eventual Code review can
check them off rather than rediscover them.

### [CF1] P2 owes the report's eligible/ineligible split (a dependency, not a cut)

Chunk **P6a** (`8bf1154`) implements the five measures `P6-R` names — review
input, removed transitions, escaped findings, Maintainer prompts, pauses. The
accepted parent's fuller list also has the report record *"eligible and
ineligible plans"*, and P6a's implementer flagged, correctly, that its derived
report **cannot** split them: no `plan-counted` event records the plan's
assurance path.

**This is a sequencing dependency on P2, not a scope reduction, and the
distinction is checkable.** Splitting eligible from ineligible requires a
*plan's* assurance path, and a plan **has** none to read: Chunk P1 pinned that
absence deliberately —
`test_lifecycle_contract.py::test_a_plan_carries_no_artifact_level_declaration`,
whose docstring states *"the plan carries the inheritance metadata instead (P2's
cell)"*. A plan's assurance path is resolvable only through P2's inheritance
chain (plan → `Inherited proposal basis` → the accepted proposal's declaration).
So the input does not exist yet. Nothing accepted is dropped and **no
`Scope delta` allowance is required**; the measure is owed by the chunk that
supplies its input.

The same shape has now occurred three times in this plan — P1's blocking half
behind C's enumeration, P5's trigger behind P2's inheritance metadata, and this.
The `## Sequence` order is dependency-ordered for the *chunks* but not for the
*fields those chunks require*, which is worth one line in the Code review.

**P2 obligation.** Record the counted plan's assurance path on the event, via the
`cairn-pilot-event/2` bump P6a already provisioned (its unknown-version refusal
path is tested), and make the report split eligible from ineligible. P6a
deliberately did **not** fork the assurance vocabulary or reach for the private
`_ASSURANCE_PATHS` to close this early; either would have created a second
vocabulary, which is the defect Chunk A exists to prevent.

**Discharged at `b00ab89` (P2).** The vocabulary is now public
(`ASSURANCE_PATHS`, plus `ASSURANCE_NOT_INHERITED` for a plan that declares no
chain) and read through the same contained loader as `PLAN_STATES`; the schema is
`cairn-pilot-event/2` with a mandatory `assurance_path` on every `plan-counted`
event, **derived** by the CLI from the plan through P2-R's chain rather than
typed -- and a plan that declares a chain the planner cannot resolve refuses the
write. `pilot-report` prints the split. **One thing was deliberately not
decided**: the counted-stem quota still counts distinct stems, because the
accepted parent ("high-assurance work ... does not fill the sample") and the
2026-08-11 revision ("standard and high-assurance proposals may both receive
`READY`") pull opposite ways on *whose* plans fill the six. Re-deciding the
denominator is a Maintainer's call, so the report prints the tension whenever the
sample holds an ineligible stem, and `dev/measurement/pilot-events.md` records it.

### [CF4] Two P1 legacy-manifest entries went stale mid-chunk -- Claude (Implementation) -- 2026-08-12

Not P2's, not caused by P2, and left rather than absorbed. Another session's
Decision commit `d1b61b2` flipped
`dev/proposals/2026-08-11-claude-metrics-events-not-prose.md` to `accepted`,
which makes it **terminal and therefore immutable** -- so `_is_immutable` now
covers it and P1's two scoped grandfather entries for that stem are dead weight.
P1's own guard-on-the-guard says exactly what to do (*"if this reddens, delete the
entry"*), and it reddens now:
`test_lifecycle_contract.py::TestBasisLegacyEnumerations::test_every_basis_manifest_entry_is_still_needed`
and `::test_the_declaration_exemption_names_only_live_undeclared_proposals`.

Both nodes fail identically against **HEAD's** planner over the same tree, so
this is a stale-data finding, not a P2 regression. The repair is deleting the
stem's entry from `_LEGACY_UNDECLARED_BASIS` and from
`_LEGACY_UNDECLARED_ASSURANCE_PATH` -- which *tightens* the gate and changes no
behavior, since immutability already covers the artifact. It is left to the
chunk that owns those enumerations (or the Code review) because deleting another
chunk's committed grandfather data as a side effect of P2 is the deviation-shaped
choice, and the triggering event was a concurrent session's Decision rather than
anything in this cell.

### [CF2] A stale comment in the planner, owed to whoever next edits it

`tools/lifecycle_planner.py` (and its twin) still says *"Two consumers live
OUTSIDE this file's package"* and lists two. There are now **three**: Chunk P6a
added `tools/lifecycle.py` as a third contained-loader consumer, and extended
`_AUDITED_CONSUMER_SOURCES` from three sources to five accordingly. P6a could not
fix the comment because P1/P5 held that file. A comment that miscounts the
consumers of a single-source vocabulary is exactly the drift Chunk A's audit
exists to catch, so it should not survive to the Code review.

### [CF3] Chunk E's two residuals, both owed to H1 -- Claude (Implementation) -- 2026-08-12

Chunk E landed the accepted vocabulary **additively** (`ec6139e`): the new tokens
became legal, `open` / `executing` / `review` stayed legal, and
`HISTORICAL_PLAN_STATES` stayed empty. That is **sequencing, not scope
reduction** -- the accepted R2 text says *"Replace"*, and the replacement is
Chunk H1's named job, *"rewrites the `Status:` of every active artifact"*, behind
a dry-run inventory, blob-checked, admitted by a reviewer independent of the
generator. Measured at E's parent: `git-native-security-foundations` and
`review-efficient-lifecycle` declare `executing` and `scope-reduction-trap`
declares `review`, two of the three another session's in-flight work, and *"all
live artifacts sound"* is this plan's own acceptance criterion. A hard
replacement at E would have reddened all three.

Two specific obligations fall out of that, and neither is a cut:

**(a) H1 retires the three tokens by MOVING them, not deleting them.** Every
legacy arm in the planner's vocabulary block and both transition tables is marked
`PENDING-RETIREMENT (H1)` as a grep target. The edit is: drop the three from
`PLAN_STATES` / `PROPOSAL_STATES`, add them to `HISTORICAL_PLAN_STATES` /
`HISTORICAL_PROPOSAL_STATES` (metrics must keep parsing pre-migration commits, per
R7), and drop the legacy transition arms -- in the same commit that rewrites the
artifacts, so the planner never contradicts the tree it scans.
`TestTheLegacyTokensAreStillLegalUntilH1` in
`bootstrap/tests/test_lifecycle_contract.py` is what reddens if the tuples move
without the artifacts, and
`test_the_counting_rule_still_fails_closed_if_the_token_ever_goes_away` in
`bootstrap/tests/test_pilot_evidence.py` is the guard on the other direction.

**(b) H1 owes R3's multi-obligation legacy mapping.** R3: *"Existing
multi-obligation passes are append-only. Migration enumerates them by artifact,
raw-heading digest, and occurrence count, then records which exact obligation
each admitted pass satisfied ... The mapping is reviewed independently of the
inventory generator."* E did **not** build that enumeration, because it belongs to
migration by the clause's own words. The population is measured and small:
**three archived plans** declare `required(External + External Security Review)`
with no `**Obligation**:` line anywhere -- `api-web-security-modules`,
`release-security-orchestration`, `verification-evidence-boundaries` -- and every
one of their passes is already admitted by `_LEGACY_PASSES`, which E therefore
treats as grandfathering the floor as a whole (its pre-E behaviour, preserved
exactly). Both live `+` plans, by contrast, carry real per-pass `**Obligation**:`
lines and resolve both clauses under the new rule, so nothing live depends on the
grandfather.

**A third item, declined rather than deferred, and recorded because declining is
the deviation-shaped choice.** P6a's red-by-construction node
(`8bf1154`) carried a two-part remedy in its docstring: *"replace this node with
the positive one and delete the UNAVAILABLE branch's reason from the report"*. E
did the first. It did **not** do the second: `templates/skills/_lib/lifecycle.py`
and its twin are outside E's cell, and the `UNAVAILABLE` branch is a live
fail-closed guard, not scaffolding -- item (a) above edits the very tuples it
protects, so *"the vocabulary lost a token the engine needs"* stays reachable.
Deleting it would leave three code paths with no test, which is the silent-tool
defect `AGENTS.md` > *Verifying claims* forbids. The branch is instead kept under
test through the inverted `lifecycle_without_counted_state` fixture. If a later
reviewer disagrees, the removal is a small edit to two byte-identical files plus
the four nodes that exercise it.

### [CF5] `doctrine/proposals.md` still calls the revision optional -- owed to G -- Claude (Implementation) -- 2026-08-12

P3 (`b3d17a5`) landed the accepted parent's "Bounded current contracts" clause in
the **tool** and in **both authoring templates plus their twins**, which is
exactly the surface list P3's cell names. It did **not** touch `doctrine/`,
because P3's cell does not name it and Chunk **G** does (`G-R`: *"Teach the
proposal-centered default immediately in canonical, self-hosted and shipped
operational surfaces"*), backed by the accepted three-layer distribution matrix,
whose *Published canonical method* row names `doctrine/proposals.md` by name.

**This is a sequencing dependency on G, not a scope reduction, and no `Scope
delta` allowance is required** -- every outcome P3's cell committed to shipped.
But it leaves a live contradiction that the Code review should check off rather
than rediscover. Three exact locations in `doctrine/proposals.md` still carry the
pre-contract, *conditional* wording:

* line 36 -- *"the author appends a `## Response` and, **where needed**, a `##
  Revised proposal`"*. The contract has no "where needed": one complete current
  contract follows every Response.
* line 71 -- *"Commit on **appending a Response and any "Revised proposal"
  section**"*. "any" reads as optional for the same reason.
* line 504 -- *"If accepted critiques substantially change the proposal, write a
  short "## Revised proposal" section"*. This is the sentence P3 **replaced** in
  all four template copies; the doctrine copy of it survives.

**Why leaving it is safe, stated rather than assumed.** The contradiction runs in
the loud direction: doctrine is *permissive* and the tool *refuses*, so an author
who follows the stale doctrine is stopped by a refusal that names the exact
heading to add and quotes what a complete contract contains. The failure mode is
a puzzled author, not a silent gap -- the inverse (doctrine strict, tool
permissive) is the one that would have to be fixed immediately.

**Also corrected inside P3, and named because it edits another chunk's text.**
Two live locations in `tools/lifecycle_planner.py` told the author the revision
was optional, and a scaffold that emits text its own gate refuses is worse than
no scaffold: the `revised` transition's pasteable block (*"If accepted critiques
substantially change the proposal, add a '## Revised proposal' section"*) and
Chunk E's `revising -> awaiting-review` gate description (*"append a '##
Response' (+ optional '## Revised proposal')"*). Both now emit the mandatory
form, the scaffold emits the ledger with it, and
`test_the_emitted_revised_scaffold_clears_its_own_gate` pins the property that
the tool never hands an operator a violation. E's neighbouring
`_STATUS_MOVES_WITH` entry already said *"'## Response' + complete
current-contract revision commit"*, so E had the rule right in one of its two
locations -- the same one-fixed-one-missed shape [H1]/[T4] named.

**One thing P3 decided rather than left ambiguous, for the Code review to
attack.** The contract says *"After a proposal review Response, the author
appends one complete current contract"* and fixes neither an **order** nor a
**ratio**. P3 therefore checks position-agnostic *presence* -- a Response
requires at least one revision somewhere in the artifact -- and does **not** pair
revisions to Responses one-for-one. That restraint is measured, not lazy: of the
39 proposals in this tree that carry a revision, 6 place it **above** its
Response (which is what the proposal template's own long-standing instruction
told authors to do), and `resp=2 rev=1` is the single most common shape. A
pairing rule would have refused correct records for a rule no accepted text
states. The residual is that a proposal with five Responses and one round-1
revision clears; closing it needs a contract sentence, not a tighter regex.

### [CF6] P4 published one planner name outside its own cell -- Claude (Implementation) -- 2026-08-12

**Declared rather than absorbed, because it edits a file the P4 cell's Surface
column does not name.** That column reads `tools/lifecycle.py` + installed twin.
P4 also added **one line** to `tools/lifecycle_planner.py` and its twin:

```
read_artifact = _read_artifact
```

**Why it was unavoidable.** R6 requires that *"`scan`, `next`, and accepted
closeout tooling consume shared predicates rather than implement three
interpretations of readiness"*, and Chunk E wrote P4's half of that into the
planner by name -- `status_evidence_violations`'s own docstring says *"Public
because three surfaces consume it ... and, when P4 lands it, `closeout
--dry-run`"*, and the E2 section comment says *"P4's `closeout --dry-run` will
pass `ready-to-archive`; three call sites, one interpretation."* That predicate
and the three beside it (`review_record_violations`, `blocked_by_violations`,
`plan_inheritance_violations`) are already public and all four take an
`Artifact` -- and **nothing public built one**. The only two remaining routes
were to reach a private name across the module boundary, or to grow a second
artifact parser in the CLI. Chunk P6a refused exactly that pair for the
assurance vocabulary and deferred to P2, which **published** `ASSURANCE_PATHS`
and recorded why; there is no later chunk to defer to here, so this is the same
move for the parser.

**Why it is a declaration and not a `Scope delta`.** The planner and its twin
are named in this plan's own `## Scope` surface list, no accepted outcome is
dropped, and the change adds no behavior: it is an alias, not a wrapper, so
there is no second body to drift from the one every in-file call site uses. It
is recorded here so the Code review checks it off rather than discovering it in
a diff.

**What P4 did NOT do, and the reader should confirm.** It did not make the
planner's heading, field or clause grammars public. The CLI restates three of
them locally to *locate* records, and
`bootstrap/tests/test_lifecycle_brief.py::TestNoGrammarDrift` compares each
against the planner's own helper over the whole live corpus. That guard earned
itself during implementation: a hand-rolled verdict-clause split classified
`REVISE / NOT CLEARED.` as *unreadable* where the planner reads `REVISE` -- a
blocking code review silently losing its class. The rule is now the planner's
expression, pinned by that node.

**One measurement worth carrying to the Code review.** The mutation run found
that P4's two ASCII-safety nodes were injecting non-ASCII into an H1 title and a
verdict's trailing clause -- neither of which any reported field carries -- so
both passed with `ensure_ascii=False` and proved nothing. Same shape as P2's
[M16] and P3's [M10]. Fixed by injecting into two fields the payload demonstrably
carries, with an assertion that it carries them.

### [CF7] A correction owed to `a404a92`'s commit body

P6c's commit body states *"17 falsifiers were applied"*. **That figure is wrong.**
The accurate ones, from its own record: **22** falsifiers run to *verify the
delegation* to `test_pilot_evidence.py` (of which **3 survived**, which is the
finding), and **12** more run to redden the 13 nodes it added. The table in the
committed test file's section banner is correct; only the commit message is not.

Recorded here rather than amended: Chunk G had already committed on top
(`5257bde`) by the time P6c went to fix it, and rewriting another session's
commit to correct a message is the worse trade. The Code review should read the
banner table, not the count in the body.

**Why the 3 survivors matter more than the count.** P6c was asked to verify
P6a's claim that all ten of its cells already had behavioural equivalents, rather
than accept it. It held for 7 cells and for the first clause of cell 10, and
**broke for two**:

* **cell 6, interrupted write** — a mutation making a failed write return success
  and record nothing left **97/97 sibling tests green**;
* **cell 8, boundary-day arithmetic** — two mutations of the deadline comparison
  each left **97/97 green**. The sibling's only deadline node stands a day *past*
  the boundary and its only OPEN node fifty days *inside* it, so the compared
  edge had no witness at all — while `_window_bounds`' own docstring says the
  off-by-one *"silently moves a Maintainer Decision by a day"*.

Both gaps are closed in `test_lifecycle_contract.py`. The third finding is
structural: P6c added `_P6C_COVERAGE`, a map from each cell to the sibling node
carrying it **and the falsifier that reddened that node**, which itself reddens
when a covering node is renamed or deleted. Without it, "cell N is covered
elsewhere" is a claim in a commit message that goes false silently — and the
sibling file is named by neither the P6a nor the P6c row.

### [CF5] CLOSED by Chunk G -- Claude (Implementation) -- 2026-08-12

Closed at `5257bde` (G1). All three cited `doctrine/proposals.md` locations
carried the pre-contract conditional wording; a fourth, unfiled instance was in
`doctrine/lifecycle-contract.md`'s own transition table, which is the
*executable formalization* and therefore the worse of the four to leave stale.

| filed location | before | after |
|---|---|---|
| `proposals.md` :36 | *"the author appends a `## Response` and, **where needed**, a `## Revised proposal`"* | *"appends a `## Response` **and one complete current-contract revision** ... The revision is mandatory with every Response, not conditional on how much changed."* |
| `proposals.md` :71 | *"Commit on **appending a Response and any "Revised proposal" section**"* | *"Commit on **appending a Response and its complete current-contract revision** ... the two land together, because a Response without a revision is not a legal `revised` state."* |
| `proposals.md` :504 | *"If accepted critiques substantially change the proposal, write a short "## Revised proposal" section"* | replaced by `### Append one complete current contract with the Response, every time`, carrying the mandatory ledger, the `* None` rule, and an explicit note that the older conditional form made record completeness depend on the author's own estimate of significance |
| **not filed** -- `lifecycle-contract.md`, the `reviewed -> revised` row | *"a `## Response` (and, where needed, a revised section) is appended"* | *"a `## Response` **and one complete current-contract revision** ... are appended ... The revision is **not optional** -- a Response with none refuses."* |

`doctrine/proposals.md` also gained a `## Plan readiness` section, since the
accepted three-layer distribution matrix names that file as the *Published
canonical method* row for this contract and G-R distributes it there.

### [CF8] Two red gates at HEAD that Chunk G did not create and did not touch -- Claude (Implementation) -- 2026-08-12

Both were measured against a clean detached worktree at `5257bde` (G1), i.e.
**before** any G2--G5 byte, so neither is attributable to this chunk. Both are
owed to Boundary B, and neither file is in a G cell.

1. **`test_quickstart_sequence.py::test_step3_install_writes_expected_kernel_and_modules`
   is RED.** *"docs/quickstart.md says '23 unfilled block slots' but the live
   install reports 24."* The 24th slot is
   `<!-- cairn:slot assurance-path-triggers -->`, which **P1** (`76bc678`, this
   plan) added to `templates/core/dev/proposals/_template.md`; `docs/quickstart.md`
   was not refreshed with it. The fix is a one-number edit to a file no G cell
   names, so G leaves it: it belongs to P1's own surface, and sweeping it in
   would be scope this chunk's cell never carried.

2. **`scripts/verify_stems.py` reports 2 issues**, both in `dev/PLANNING.md`:
   stems `2026-07-08-claude-broad-look-skeptical-review` and
   `2026-08-05-codex-security-strategy` resolve to no file. `dev/PLANNING.md` is
   a shared board this chunk does not touch; likely an H4 row-move concern.

### [CF9] The #58 loop-fidelity gate has one prefix, and G is the chunk that most needed more -- Claude (Implementation) -- 2026-08-12

`scripts/check_cairn.py`'s `_CAIRN_INTERNAL_PREFIXES` is `('doctrine/',)`. The
gate therefore catches a shipped `templates/**` surface citing any path under
`doctrine/` and **nothing else** -- a `bootstrap/`, `dev/plans/`, `dev/proposals/`,
`dev/measurement/`, `case-studies/` or `dimensions/` path in the same position
dangles in an adopter tree and passes clean.

**Measured, not inferred.** With
`` `bootstrap/fidelity-check.md` `` and
`` `dev/plans/review-efficient-lifecycle.md` `` appended to a shipped surface
(`templates/skills/session-start/SKILL.md`), `check_cairn` on that file printed
`OK -- 1 Markdown file(s) scanned; no issues.` The synthetic lines were removed
and the file restored byte-exactly (`cmp` clean) before any commit.

There is already at least one live instance: `templates/core/AGENTS.md` cites
`bootstrap/fidelity-check.md` in its drift-guard paragraph. It predates this
plan and G did not touch it.

**G self-policed instead of widening the set**, because widening a standing gate
as a side effect of a prose chunk is exactly the deviation the plan forbids.
The check run over every added line in every `templates/**` file across the
whole Chunk G range (`b7f93dc..43df6fd`): resolve each path-shaped backtick and
link token against the real install set from `scaffold.py --manifest`, skipping
`doctrine/` (the #58 gate's own territory) and 4-space-indented illustrative
blocks (the house convention `claim_check.scannable_lines` already honors).
Result **5 shipped files with additions, 5 path-shaped tokens, 0 leaks**; the
check was falsified twice against synthetic leaks, each removed byte-exactly.
It caught one real defect pre-commit: an example path under `bootstrap/tests/`
in G3's registry block -- a Cairn-only path in a surface that ships -- now
`tests/test_widget_contract.py`.

**Recommendation, as a finding and not an action.** Extend
`_CAIRN_INTERNAL_PREFIXES` to the verified-not-installed set, with the live
`templates/core/AGENTS.md` instance dispositioned first (an inline
`cairn-internal-ref:` marker, or transplanting the reference). It is a
contract-surface change to a standing gate and wants its own cell.

## Cross-cutting findings for the Code review -- Claude (Implementation) -- 2026-08-13

Per-chunk evidence is in each chunk's commit body and its tests. **These five are
patterns across chunks**, visible only from the coordinating seat, and they are
recorded here because that seat's context does not survive a compaction. Each is
a claim the Code review can check, not a summary to take on trust.

### 1. `## Sequence` is dependency-ordered for CHUNKS but not for the FIELDS they need

**Five instances**, each found by measurement before implementation, each resolved
as sequencing (no accepted outcome dropped) rather than as scope reduction:

| Chunk | Needed a field supplied by | Resolution |
|---|---|---|
| P1 | C's legacy enumeration | grandfather via `_is_immutable`, 72 -> 8 entries |
| P5 | P2's `Inherited proposal basis` | trigger keyed, empty set proved by synthetic fixtures |
| P6a | P2's assurance chain | report split deferred, filed **[CF1]**, discharged by P2 |
| E | H1's status migration | vocabulary landed **additively**; retirement stays H1's |
| P4 | F2's encoder | F resequenced before P4 |

The plan orders chunks by dependency and its two load-bearing orderings hold. But
a chunk can need a *field* a later chunk creates, and nothing in the artifact
surfaces that. Worth one sentence in the doctrine the next plan inherits.

### 2. A fixture that cannot reach the property it tests -- four occurrences

P2's M16, P3's M10, P4's ASCII-safety nodes, and (in a different shape) the two
gaps P6c found in P6a's suite. Every one **passed under the mutation it was
written to catch**, and every one was found by mutation rather than by review:

* M16 put the field mid-sentence where a full-line-anchored matcher never looks;
* M10 wrote a heading at H2, which both missed the level *and terminated the
  record it was meant to sit inside*;
* P4 injected non-ASCII into fields no reported output carries;
* P6c's cell 8: the sibling's only deadline node stood a day *past* the boundary
  and its only OPEN node fifty days *inside* it, so the compared edge had **no
  witness** -- two mutations of it left 97/97 green.

The mutation discipline caught all four. **A green suite plus a written-down
mutation is not evidence; the observed red is.** This is the strongest argument
in the range for the per-node RED requirement.

### 3. Three cross-session hazards, none of them defects in any one plan

* **An uncommitted change to a shipped checker silently changes every other
  session's gate output.** D3/D4's in-flight `claim_check.py` made this plan's
  artifact read as red under one checker and clean under the committed one. I
  only avoided a wrong conclusion by running both.
* **A Decision landing elsewhere kills grandfather entries here.** Twice
  (`8308fdc`, `6f2b01c`): another session flipped a proposal terminal,
  `_is_immutable` began covering it, and P1's entries became dead weight --
  reddening tests for whoever committed next. That is P1's design working (the
  enumeration liquidates itself), but the toil lands on a stranger.
* **Committed changes landing unfinalized.** Three `scope-reduction-trap` commits
  changed the planner without a scoped finalize, so `verify_integrity` was red on
  that path until Chunk F swept it current -- and F's finalize then recorded
  their bytes under F's commit.

### 4. A standing gate covers less than its name suggests

`scripts/check_cairn.py`'s #58 loop-fidelity gate has
`_CAIRN_INTERNAL_PREFIXES = ('doctrine/',)` -- **one prefix**. A `dev/**`,
`bootstrap/**` or `dev/measurement/**` path leaking into a shipped
`templates/core/**` surface is not caught. I asserted the opposite to two agents
before measuring it. G confirmed it empirically, self-policed its own range with a
throwaway checker (5 shipped files, 5 tokens, 0 leaks; one real defect caught
pre-commit), and filed the widening as **[CF9]** rather than changing a standing
gate as a side effect.

### 5. A mutation harness must never restore with `git checkout`

P4's driver did, against **uncommitted** work, and destroyed ~1000 lines on its
first mutation. Restore from an in-memory or out-of-tree byte snapshot, with a
pre-flight assertion that the snapshot still contains the chunk under test. P6c
adopted that and verified 34 restores by digest.

### Ceremony scope, re-measured as the plan requires

Chunk I's cell states two manifest-pinned and two `FROZEN-NEW` paths and says to
**re-measure at the implementation parent**. Measured 2026-08-12 over this plan's
own commits only (the range also holds 54 commits from three other sessions):
**5 frozen paths changed and 5 discovered `FROZEN-NEW`** -- ten, not four -- and it
grew again with F, P4 and G. `bootstrap/_scaffold/` is untouched, so the **AST
attestation baseline needs no re-anchor**; only the gate manifest does.

## Chunk I is subsumed, and the ceremony has run -- Claude (Implementation) -- 2026-08-13

**Chunk I no longer executes.** The Maintainer decided on 2026-08-11 that the
re-anchor would be a single ceremony, performed by
`git-native-security-foundations`'s Chunk H rather than twice. Authorization,
quoted verbatim from that plan's record
([`dev/plans/archive/git-native-security-foundations.md:1012`](archive/git-native-security-foundations.md)):

> Let's go a single ceremony. The other plan doesn't care about what's in the
> runbook

That plan states the consequence and assigns this record explicitly — *"The
other plan's owner should know its Chunk I no longer executes ... a subsumed
chunk is that plan's own record to make"* (line 1028). This section is that
record. The reasoning was that its Chunk H already re-derives the evidence and
advances branch and anchor, so it re-pins the frozen set Chunk I would have
re-pinned; running both would re-anchor twice, the second time over a set the
first had just fixed.

**The ceremony ran on 2026-08-13**, anchor `e45e1fc` -> `cfaace9`, over the
reviewed tree at `b8c1fac`: 164 frozen files modified, 37 added, 0 removed;
pytest collection 1598 -> 4261. Verified here rather than taken on trust —
`test_gate_manifest.py` is **21 passed** at that anchor, and collection measures
**4261**, so this plan's ten frozen paths (re-measured in the section above) are
absorbed and the `FROZEN-MODIFIED` dirtiness signals this plan carried through
G are cleared.

**One ordering divergence, recorded because it is load-bearing and because
nothing should infer it later.** Chunk I's condition was *"after every
executable, test, template and frozen byte across A–H is stable **and** the
single code review has landed"*. The ceremony instead ran with **H still
outstanding and before the code review**, because it was scheduled by the other
plan's needs, not this one's. The subsumption record asserts the single
ceremony's delta *"covers both plans, including
`bootstrap/tests/test_lifecycle_contract.py`"* (line 1025) — true as of
`b8c1fac`, but that file is **frozen** (confirmed present in
`frozen_files`, 201 entries) and **H1 must edit it**, since retiring the legacy
tokens is exactly what `TestTheLegacyTokensAreStillLegalUntilH1` pins. So H1's
frozen-byte change post-dates the anchor that was supposed to cover it.

Whether that leaves the gate red is **measured when H1 lands, not asserted
here** — and the disposition is the Maintainer's, not an implementing agent's,
because a re-anchor is fenced work. What is already certain is bounded and
small: the remaining delta is H's paths alone, not the ten this plan
accumulated, so any follow-on ceremony has a far smaller and more reviewable
scope than the one just performed.

**B2 still stands and its position moves.** It was defined as the Boundary B on
*"the post-ceremony commit after Chunk I"*. Chunk I is gone, so B2 attaches to
the post-ceremony commit after whichever re-anchor finally covers H's frozen
delta. B1, the single code review, and the union range are untouched.

**The plan's sequencing assumption became true, late.** Chunk H's cell says the
security plans *"are already archived when this plan implements, so the quiet
tree is a precondition to check at H, not a wait to schedule"*. They were not
archived when H began; both were archived at `f654dc0` on 2026-08-13, mid-H. The
precondition therefore had to be checked as the cell requires, and it did not
hold on first check — two other sessions held live intent claims on two of the
four active artifacts, one of them writing an archive record. Those rows waited
rather than being applied against moving blobs.

## H1 is applied but not complete: the retirement waits on quiescence -- Claude (Implementation) -- 2026-08-13

**What landed.** H2's metadata migration (`17cceb2`), the artifact rewrites for
every row that could be applied (`42322f3`, `c4b9b04`), and the templates fix
that H1 could not converge without (`ac8a9a8`).

**What has not, and why it is the cell's own precondition rather than a cut.**
The vocabulary retirement -- moving `open` / `executing` / `review` and
`proposed` / `reviewed` / `revised` out of `PLAN_STATES` / `PROPOSAL_STATES` and
into the historical tuples, with the legacy transition arms dropped -- is **not
applied**. Chunk H's cell requires a quiet tree and says the precondition is
*"a precondition to check at H, not a wait to schedule"*. It was checked, and it
does not hold.

**The evidence, measured rather than characterized.** Between 07:52 and 08:26 on
2026-08-13, three other sessions landed twelve commits touching active lifecycle
artifacts. Two artifacts moved *under an intent claim this session held*:

* `2026-08-13-claude-test-names-outlive-their-plans` -- `proposed` -> `reviewed`
  at `e02f6a8`, while claimed.
* `2026-08-13-claude-finding-tags-are-not-reasons` -- rewritten to `reviewed` at
  `618ec47`, discarding an uncommitted `awaiting-review` edit, while claimed.

Both rows were therefore **refused**, which is exactly what H1's *"apply only
admitted rows whose blobs still match"* requires. Intent claims are advisory
coordination signals, not locks, and this is the first recorded case in this
repository of that distinction costing a migration pass. It is a coordination
fact, not a defect in either session.

**Why the retirement must not be forced through anyway.** Both moves went *into*
the legacy vocabulary via the legal legacy arm `proposed -> reviewed`. A session
is actively driving artifacts through the tokens H1 retires. Retiring them mid-
flight would strand that session with no legal forward move -- precisely the
hazard Chunk E's sequencing decision was taken to avoid, and the reason
`test_each_legacy_state_keeps_a_forward_path` exists.

**What the retirement will cost when it runs, so the next implementer does not
re-derive it.**

* Both planner twins: the two state tuples, the three legacy `PROPOSAL_TRANSITIONS`
  arms, the three legacy `PLAN_TRANSITIONS` arms plus `executing` as a target of
  `awaiting-plan-review`, the `open` entry in
  `PLAN_TRANSITIONS_REVIEW_NOT_REQUIRED`, `PLAN_REVIEW_CLEARED_STATES` and
  `_PROPOSAL_POST_REVIEW_STATES`, and both historical tuples.
* **The legacy `PROPOSAL_NEXT_OWNERS` / `PLAN_NEXT_OWNERS` entries stay.**
  `test_the_legacy_multi_successor_tokens_report_unresolved` pins them, and
  historical tokens still occur on archived artifacts and in metrics. Retiring a
  token removes it from the *current* vocabulary; it does not make the board
  unable to render it.
* `bootstrap/tests/test_lifecycle_contract.py` -- `TestTheLegacyTokensAreStillLegalUntilH1`
  inverts, and `test_the_historical_tuples_are_still_empty_and_that_is_the_seam`
  is the node that must flip rather than be deleted.
* **A corpus measurement is mandatory, not optional.** `SHAPE_B_STATUSES` goes
  **16 -> 12**: the current non-terminal sets lose `reviewed`, `revised`,
  `executing` and `review`, while `proposed` and `open` re-enter through the
  `OPENING_STATES`-in-historical filter. The comment above that tuple states
  that a change reaching historical NON-opening tokens is **corpus-CHANGING and
  re-runs that measurement**. So `test_transition_lint.py`'s pinned corpus
  expectations must be re-measured, not assumed to hold -- four tokens leaving
  the shape-(b) candidate set can only remove findings, and any that disappear
  are pinned expectations that move.
* This edit touches the **frozen** `bootstrap/tests/test_lifecycle_contract.py`,
  and the single ceremony has already run (`cfaace9`), so it lands after the
  anchor meant to cover it. See the Chunk I section above; the disposition is the
  Maintainer's.

## H1 retirement: measured blast radius before implementing -- Claude (Implementation) -- 2026-08-13

Five independent read-only sweeps plus one scratch-clone apply. **Measured, not
predicted**: baseline `4257 passed, 1 skipped`; with the retirement applied to
both planner twins and nothing else, **29 failed, 4228 passed**. The findings
below are recorded before implementation because three of them are not
discoverable from the `PENDING-RETIREMENT (H1)` markers, and two are scope
questions rather than edits.

### Two findings that are the Maintainer's call, not an implementer's

**[H1-S1] The retirement deletes the `Scope delta` scaffold from every user
path.** Enumerated across every legal transition's `_scaffold` output: today
exactly two arms emit `**Scope delta**` -- proposal `reviewed -> revised` and
plan `awaiting-plan-review -> executing`. **Both are legacy-only.** After a
literal retirement, **zero** legal transitions emit it, so the surface where an
author meets the scope-reduction rule *while typing* disappears. That is
`scope-reduction-trap`'s central mechanism, and removing it is removing another
plan's accepted scope -- the deviation `AGENTS.md` names, and precisely the
narrowing its "a reviewer cannot create that authority" clause warns about.
`test_scope_reduction_trap.py:572` planted an explicit tripwire for this and it
fired exactly as designed; its message says *"Re-point it at the transitions that
scaffold the declaration today; do not delete it."*
**Disposition taken: PRESERVE, not delete.** The scaffold text moves to the
live-vocabulary arms that carry the same authorial moment. Preserving is the
non-narrowing default and is cheaply reversible; deleting is neither.

**[H1-S2] After retirement no legal proposal transition emits a review
scaffold at all.** `test_review_scaffold_carries_no_reviewer_attribution`
(`test_lifecycle_contract.py:249`) pins that the tool never fills in a reviewer
identity. Measured: today only `proposed -> reviewed` and `revised -> reviewed`
emit the `<reviewer>` placeholder; post-retirement every proposal target is a
status-move manifest or a Decision block.

**A first reading of this said the property "survives on the plan side"; an
independent reachability probe falsified that and it is corrected here rather
than left standing.** `## Code review` is emitted **only** from
`executing -> review`, which the retirement also retires, so the property would
have **no surviving witness on either side**. The full post-retirement scaffold
inventory is three sections -- `## Decision`, `## Implementation verification`,
`## Lasting-truth migration` -- and no reviewer placeholder anywhere. Same
disposition as [H1-S1]: re-point rather than delete.

### Three sites the `PENDING-RETIREMENT (H1)` markers do not cover

**[H1-D1] The metrics normalizer silently breaks R7's own guarantee.**
`tools/_lifecycle_metrics/extract.py:340` declares
`_REQUIRED_EXPORTS = ('PLAN_STATES',)` and `_plan_status_enum()` (:432) returns
`PLAN_STATES` alone -- no historical tuple. `_normalize_plan_status` resolves by
*prefix* over that enum, so measured:

```
'reviewed; awaiting code review'  ->  BASE 'review'   AFTER 'reviewed'   CHANGED
'open' / 'executing' / 'review'   ->  unchanged (exact lead falls through)
```

Only the prefix case moves, which is why it is invisible: **no test anywhere
references `_normalize_plan_status`, `_plan_status_enum`, or that input**, so the
suite stays green while a longitudinal bucket splits in two. R7 requires metrics
keep parsing pre-migration commits; this is the one clause the retirement would
break. Fix is the enum plus the historical tuple (order-safe: no current token
prefix-collides), in **both** twins -- and the template copy is **frozen**. A
regression test lands with it; shipping the fix without one leaves the same
silent hole.

**[H1-D2] `_conformance_violations` calls archived artifacts malformed.**
`tools/lifecycle_planner.py:4513` tests `s not in _PROPOSAL_STATES`, so after
retirement an archived proposal at `revised` reports `unknown proposal status`.
It must consult the historical tuples (or `RECOGNIZED_STATES`, whose docstring is
*"every status any consumer may recognize"*).

**[H1-D3] `test_pilot_evidence.py:502`** asserts
`{"review","archived"} <= set(planner.PLAN_STATES)` -- unmarked, and red.

### Coverage that goes silently absent (a green suite would hide all of it)

* **Three fixture helpers default to a retired token** -- `_plan_art`
  (`status="executing"`, 17 of 30 callers), `_prop_art` (`"reviewed"`, 10 of 11),
  `_p3_prop` (`"revised"`, 6 of 6). Three one-line edits re-validate ~33 nodes
  against the live vocabulary; leaving them exercises the P1/P3/C suites against
  statuses no artifact may declare.
* **Three owner-table entries end up covered by no test at all** --
  `PROPOSAL_NEXT_OWNERS["proposed"]`, `PLAN_NEXT_OWNERS["open"]` and
  `["executing"]`. `test_the_legacy_multi_successor_tokens_report_unresolved`
  pins only 3 of the 6 legacy entries; the other coverage iterates
  `PROPOSAL_STATES`/`PLAN_STATES` and stops visiting them. Deleting those three
  would pass the suite -- so the retained entries need their own assertions.
* **`test_every_shape_b_status_detects_a_baked_in_review`** resolves fixture kind
  as `"proposal" if status in PROPOSAL_STATES else "plan"`, so post-retirement
  `proposed` writes into `dev/plans/`. Still green (shape (b) is kind-blind), so
  the drift is invisible.
* **`_scaffold`'s four legacy branches** become unreachable via
  `_legal_transitions` while three `test_scope_reduction_trap.py` nodes keep
  calling them directly -- passing **vacuously**. That is the file's own
  *"named enforcer that does not enforce"* shape.

### Do not touch

`bootstrap/tests/test_lifecycle_stage_patterns.py` (49 hits) uses `open`,
`reviewed` and `revised` as **commit-subject stage names** -- a second vocabulary
sharing four spellings with the status one, and 41 of the 66 gate-manifest node
ids carrying a legacy token belong to it. Retirement must not touch it.

### Corpus: neutral, by measurement

`SHAPE_B_STATUSES` 16 -> 12 (`reviewed`, `revised`, `executing`, `review` leave;
`proposed`, `open` re-enter through the historical-opening filter, which is the
accepted R5 text *"plus the historical opening statuses"* -- a widening to all
historical tokens would contradict it). `RECOGNIZED_STATES` membership is
**unchanged at 20**; the tokens only move between its inputs. Every added
lifecycle file across both pinned windows declares `proposed`, `open` or
`awaiting-plan-review`, all of which survive, so **no pinned corpus expectation
moves** -- checked against the rule that corpus counts *"are a finding to report
if they move, never a number to update"*. The three
`TestShapeBWideningAndAdvisory` nodes that do move are **fixture** assertions,
not corpus ones, and invert.

### [H1-D4] The plan's own cost list is wrong on one tuple, and following it would disable a real check

The cost list above says to drop the legacy members of
`_PROPOSAL_POST_REVIEW_STATES`. **That instruction is incorrect and is not
followed.** The tuple's comment is a standing argument, not a retirement note:
*"Both vocabularies, because the check is about the record and not about the
token."*

Measured on a self-reviewed proposal declaring `reviewed`:

```
BEFORE  - '## Review' at line 12 appears authored by the proposal author
          ('Claude'); a review carries reviewer-authorship
AFTER   - unknown proposal status 'reviewed'
          (the reviewer-authorship finding is GONE)
```

So narrowing that tuple does not add a vocabulary message -- it **silently
disables the reviewer-authorship independence check** for those artifacts. The
failure mode actively invites the wrong repair: `scan` still exits 1, on the
*unknown status* message, so an implementer who "fixes"
`test_scan_flags_review_authored_by_proposal_author` by moving its fixture to
`awaiting-decision` restores green while leaving the independence check
unexercised. This is the highest-risk repair in H1 and the reason the retirement
is not a mechanical find-and-replace.

`_PROPOSAL_POST_REVIEW_STATES` therefore **keeps** its legacy members, and this
paragraph is the deviation record for departing from the cost list written
above. Same reasoning, same disposition as the owner tables: retiring a token
from the *current* vocabulary must not stop a consumer recognising it on an
archived artifact.

## Implementation verification -- Claude (Implementation) -- 2026-08-13

**Boundary B mode**: full.

Bounded mode was not available and would have refused twice over: this plan was
opened before bounded mode existed, so under `AGENTS.md` it *"keeps the
verification contract written in it"* and that contract names the full command
pair; and the change dirties gate-manifest-frozen files, which is a contract
surface where bounded mode refuses on its own terms. Uncertainty resolves to
`full`.

**Tested commit**: `3defdb78ef5f994fbe0fdb6062be562781af55c6` -- this plan's
final implementation commit. Clean before and after (`git status --porcelain`
empty but for the pre-existing untracked `.claude/`, `dev/measurement/
collision_log.md`, `dev/measurement/snapshots/`).

**Interpreter**: CPython 3.13.13, the canonical interpreter,
`/Users/kendal30/conda_envs/lhm/bin/python3.13`, `PYTHONDONTWRITEBYTECODE=1`.

| command | outcome | timing |
|---|---|---|
| `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` | **4275 passed**, 0 failed, 3 warnings | 622.22s |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | neutrality `fail=93 info=21`; redundancy `fail=0 info=2`; exit 0 | <1s |

**The collection delta is accounted for exactly, not approximately.** The
pre-change baseline on this tree was **4258 passed**; B1 is **4275**, +17 =
`test_metrics_status_normalization.py`'s 16 nodes plus the one positive
shape-(b) node added to `test_transition_lint.py`. No test was deleted or
skipped to reach green. Neutrality's 93/21 and redundancy's 0/2 are the
unchanged pre-existing baseline, not a new floor.

**One honest discrepancy, recorded rather than smoothed.** The suite ran
against `3defdb7`; another session committed `36808ea` and `11a8dde` during the
622s run, so the **gate half executed with the working tree at `11a8dde`**. The
two halves therefore did not observe byte-identical trees, and the gate figure
is not asserted to have been produced at `3defdb7`.

It is nonetheless sound for this plan, by measurement rather than by argument:
`git diff --stat 3defdb7..11a8dde` is exactly one file,
`dev/plans/ceremony-as-code.md` (+67/-2), another plan's deliberation record.
**No gate scan root contains `dev/`** -- neutrality scans `doctrine`,
`dimensions`, `bootstrap`, `scripts`, `on-ramp`, `docs`, `examples`; R1 scans
`doctrine`, `dimensions`, `on-ramp`, `docs`; R6 scans `scripts`, `bootstrap`,
`templates/modules` less `bootstrap/tests`. The one differing file is outside
every root, so the gate could not have observed it and its result at `11a8dde`
is identical to its result at `3defdb7`. Confirmed empirically: that path
appears 0 times in the gate's output.

The suite half is unaffected regardless -- it ran on `3defdb7`, which is the
commit this plan's reviewed range ends at. The intervening commits belong to
`ceremony-as-code` and are outside that range. As a cheap independent check that
their content did not invalidate the corpus-reading node, `scan` reports all 4
active artifacts sound and
`test_the_live_corpus_is_sound_under_the_p1_contract` passes at `11a8dde`.

**Known omissions.** No release ceremony was run (out of scope). The AST
attestation baseline needs no re-anchor: `bootstrap/_scaffold/` is untouched.
The **gate manifest does**, and that is fenced work for the Maintainer -- H1
changed two frozen paths *after* the 2026-08-13 ceremony:
`bootstrap/tests/test_lifecycle_contract.py` and
`templates/modules/default-on/_lifecycle_metrics/extract.py`, plus the
`FROZEN-NEW` `bootstrap/tests/test_metrics_status_normalization.py`. See the
Chunk I section above; that re-anchor is the one archive precondition an
implementing agent cannot discharge.

## Code review -- Claude (Internal, delegated) -- 2026-08-13

**Reviewed commit**: `3defdb7`
**Target**: this plan's implementation range — the pre-landed gate repair `286f07d^..286f07d`, and the `review-efficient-lifecycle` commits within `1c68926^..3defdb7` (filtered from the 213 commits in that window; the rest belong to concurrent sessions and were not reviewed). Substantively: **H1's retirement of the six legacy lifecycle status tokens** across `tools/lifecycle_planner.py` + its `templates/skills/_lib/` twin, `tools/_lifecycle_metrics/extract.py` + its `templates/modules/default-on/` twin, and the five test files H1 touched — plus the plan's own self-reported records (`## H1 retirement: measured blast radius`, `## Cross-cutting findings`, `## Implementation verification`, `[H1-D1]`–`[H1-D4]`, `[H1-S1]`–`[H1-S2]`, `[CF1]`–`[CF9]`), which were treated as claims to be checked rather than as evidence.
**Prior findings**: none — this is the first code-review pass on this range. The author's `[CF1]`–`[CF9]` hand-off list was checked but is not a prior review's findings.
**Assurance path**: standard
**Tier**: Internal
**Model**: Claude Opus 5 — five independent lenses, one adversarial verifier per finding, and the synthesis, all at the session model; none authored by the implementing agent.
**Verdict**: SHIP
**Findings**: raised — six MEDIUM, one LOW, one observation. No HIGH survived verification.
**Bounding**: **not applicable.** The Boundary B record declares `**Boundary B mode**: full`, so there is no bounded record to accept or reject and no `ACCEPTED / FULL RUN REQUIRED` verdict is owed. I verified the declaration is *correct* rather than merely present: the change dirties gate-manifest-frozen paths (a contract surface, on which bounded mode refuses on its own terms — measured below at five paths, not the two the record names), and the plan was opened before bounded mode existed, so under `AGENTS.md` it keeps the verification contract written in it. Both of the record's stated reasons hold.

**What this change is, in plain language.** Six status tokens (`proposed`, `reviewed`, `revised` for proposals; `open`, `executing`, `review` for plans) were removed from the *current* lifecycle vocabulary and moved into two `HISTORICAL_*_STATES` tuples. The design commitment is that **retired is not the same as unrecognized**: an *active* artifact that still declares a retired token is refused by name and handed a migration target, while an *archived* artifact declaring one is left entirely alone, because reading history is never a violation. A genuinely unknown token stays loud in both places. Around that sit four deliberate retention decisions ([H1-D1]–[H1-D4]) and two scope-preservation decisions ([H1-S1]–[H1-S2]).

**How I reviewed it.** Five lenses were run over the range and every finding was put to an adversarial verifier instructed to refute by default; I then re-derived the load-bearing measurements myself before writing this record. I ran **zero** full suites — Boundary B already spent the broad run (4275 passed / 0 failed / 622s on clean `3defdb7`), and `AGENTS.md` > *Verification boundaries* is explicit that copying it here would not be a falsification ledger. All work below is the plan's scoped mapping, single-node runs, static enumeration over the real corpus, and in-memory mutation.

**Method note the Maintainer should know.** Two lenses reported `tools/lifecycle_planner.py` and its twin being edited *under them* by a concurrent session mid-review (digest moving `3af73b06 → a2b8fdbc → 2ce1dccf`, and at one point all six historical owner rows deleted in the working tree). At the time I took the measurements below the tree was clean for `tools/`, `bootstrap/`, `templates/`, `scripts/` and both planner twins digested `3af73b06e10ba17c95cb5e34c669b4a89d073e65c10f929ad2d9d23b7bac1c74`, identical to `git show 3defdb7:tools/lifecycle_planner.py`. I wrote no file in the repository; every mutation below is in-memory (module attribute patched after `exec_module`) or in an out-of-tree scratch tree. **Any Boundary C evidence produced in this working tree during that window is unreliable unless the file digest was pinned before and after each run.**

---

### Falsification performed

**1. The scoped mapping, at review time.**

```
$ python3.13 -m pytest bootstrap/tests/{test_lifecycle_contract,test_lifecycle_board,\
  test_lifecycle_vocabulary,test_transition_lint,test_pilot_evidence,\
  test_scope_reduction_trap,test_metrics_status_normalization,test_notice_install}.py -q -p no:randomly
1 failed, 1124 passed in 74.75s
```

The single failure is **not attributable to this change**, and I established that rather than assuming it:

```
$ python3.13 tools/lifecycle_planner.py scan
dev/plans/comprehension-outlives-the-artifact.md: 'Plan review -- ... -- 2026-08-13': missing 'Target:' ...
```

Every violation belongs to another session's in-flight plan artifact landed after `3defdb7`, on the review-basis axis, not the status axis. Code and test bytes are unchanged from `3defdb7`. (It is mild positive evidence that the P1 contract bites on a live artifact it was never fixtured against.)

**2. Shipped behaviour of the headline design — probed directly, both directions.** Synthetic proposals declaring `revised`, one active and one under `dev/proposals/archive/`:

```
dev/proposals/2026-01-01-x-live.md        | immutable=False
    "retired proposal status 'revised' -- the accepted vocabulary replaced it (proposed -> awaiting-review; ...)"
dev/proposals/archive/2026-01-01-x-old.md | immutable=True
    (no status-axis violation)
```

**The behaviour is correct.** Every surviving finding below is about *coverage* or *the record*, not about a wrong answer the shipped code produces today. That is why none of them is HIGH.

**3. The standing `_PROPOSAL_POST_REVIEW_STATES` note, reproduced against its own stated case.** In-memory narrowing of the tuple, on a clean self-reviewed **archived** proposal declaring `reviewed` — the exact artifact the comment at `tools/lifecycle_planner.py:4176-4181` names:

```
--- BASELINE (as shipped)
    * '## Review' at line 11 appears authored by the proposal author ('Ada Lovelace (Strategy)') ...
--- MUT-A: narrow _PROPOSAL_POST_REVIEW_STATES
    * (NO VIOLATIONS -- scan would exit 0)
```

The comment promises `unknown proposal status` survives and *"`scan` still exits 1 either way"*. It does not. See [C4].

**4. Gate-manifest frozen-path drift, computed per-path against `bootstrap/tests/fixtures/gate_manifest.json` (201 entries) at three revisions.**

```
=== 3defdb7^: 2 frozen paths differ
    test_lifecycle_contract.py, test_scope_reduction_trap.py
=== 3defdb7 : 5 frozen paths differ
    test_lifecycle_contract.py, test_pilot_evidence.py, test_scope_reduction_trap.py,
    test_transition_lint.py, templates/modules/default-on/_lifecycle_metrics/extract.py
$ python3.13 -m pytest bootstrap/tests/test_gate_manifest.py -q -p no:randomly
21 passed in 14.43s
```

Five, not two — and nothing reports it. See [C5].

**5. The standing gate's exit code.**

```
$ python3.13 scripts/quality_gate.py --sub neutrality --sub redundancy ; echo "EXIT=$?"
[neutrality]  fail=93  info=21
[redundancy]  fail=0  info=2
EXIT=1
```

See [C6]. The two *figures* are correct and were independently reproduced at `3defdb7^` and at HEAD — they are the unchanged pre-existing baseline, exactly as the record claims.

**6. Test-witness enumeration for the retirement message and the owner tables** (exhaustive, repo-wide, not sampled):

```
$ grep -rn "retired proposal status\|retired plan status" bootstrap/tests/ scripts/ templates/ tools/ | grep -v lifecycle_planner.py:
bootstrap/tests/test_lifecycle_contract.py:3953:  f"retired plan status {state!r}" in v for v in violations
bootstrap/tests/test_lifecycle_contract.py:3962:  assert not any("retired plan status" in v for v in violations)
```

Plan side only. Nothing anywhere asserts the proposal-side message. See [C1].

```
$ python3.13 -c '... next_owner probes ...'
owner(proposal,proposed) proposal-reviewer   owner(plan,open) plan-reviewer   owner(plan,executing) implementation
```

…and `TestOwnerVocabulary` (`test_lifecycle_board.py:263-302`) iterates only the **current** tuples plus the three `unresolved` legacy tokens. See [C2].

**7. `[CF8]`'s two red gates, re-measured at the tested commit.** Item 1 is now **green** — `test_quickstart_sequence.py` → `8 passed` (fixed in-range by `27fde51`), so it does not contradict the 0-failed figure. Item 2 still reproduces — `scripts/verify_stems.py` reports 2 dangling stems in `dev/PLANNING.md`, both introduced by commits that are **ancestors of the range start**, i.e. not this plan's debt at all. The record's hedge is wrong in the plan's own favour.

---

### Findings

* **[C1] MEDIUM — the proposal half of H1's headline behaviour has no test witness, in either direction.** `tools/lifecycle_planner.py:4518-4531` (byte-identical twin at `templates/skills/_lib/lifecycle_planner.py`). The only node that exercises retirement is `bootstrap/tests/test_lifecycle_contract.py:3939` `test_each_legacy_state_now_has_no_forward_path`, whose own docstring calls itself *"the only node that proves retirement actually bites"* — and it parametrizes `("open", "executing", "review")`, the plan side, only. **Failure scenario:** a later edit changes `if not _is_immutable(art):` at :4524. Drop or falsify it and an active proposal declaring `revised` reports `unknown proposal status` — losing the migration target retirement exists to hand the author — or reports nothing at all. Invert it and every archived proposal that ever declared a retired token is called malformed by `scan --include-archive`, which is the exact R7 false positive `HISTORICAL_PROPOSAL_STATES` was added to prevent. Both directions were mutated by two independent lenses and left the mapping fully green (`1125 passed`; and `1 failed, 945 passed` / `1 failed, 834 passed` on wider sets, the one failure being the unrelated live-corpus artifact). Aggravating: the plan's own `[H1-D1]` rule is *"A regression test lands with it; shipping the fix without one leaves the same silent hole."* D1 got `test_metrics_status_normalization.py`; D2's fix got nothing.

* **[C2] MEDIUM — three retained `*_NEXT_OWNERS` rows are guarded by no test, and the source comment states the opposite.** `tools/lifecycle_planner.py:1290-1298` and `:1312-1319`. The comment at :1295-1297 reads *"Deleting these three rows passes the suite — `TestOwnerVocabulary`'s coverage iterates the CURRENT tuples and no longer visits them — which is why they carry their own node."* That node does not exist. `test_the_legacy_multi_successor_tokens_report_unresolved` (`test_lifecycle_board.py:293-302`) pins only `reviewed`/`revised`/`review`; `PROPOSAL_NEXT_OWNERS["proposed"]`, `PLAN_NEXT_OWNERS["open"]` and `["executing"]` are visited by nothing. **Failure scenario:** a cleanup deletes the three rows as dead weight; the mapping stays green (verified twice: `805 passed`, and `1125 passed` on the full mapping, deltas zero against baseline); `next_owner("plan","executing")` then answers `unknown` and the board's `owner` column — B1's entire point — degrades for any active artifact mid-migration. The comment is what a maintainer would rely on to believe the deletion is guarded. **The plan predicted this exactly** (`dev/plans/review-efficient-lifecycle.md:3576-3581`: *"Three owner-table entries end up covered by no test at all … so the retained entries need their own assertions"*) and prescribed the fix; the assertions were never written, and the inaccurate earlier reading was written into the shipped source instead. Cheapest close: three asserts in `TestOwnerVocabulary`, after which the comment becomes true as written.

* **[C3] MEDIUM — the retention justification for those rows is false by measurement.** `tools/lifecycle_planner.py:1290-1291` (*"An archived proposal still declares these"*) and `:1312-1313` (*"40 archived plans still declare these"*), repeated in `3defdb7`'s commit body as one of three decisions offered as *"measured rather than assumed"*. Measured over the live corpus with the planner's own reader: `dev/plans/archive` → 40 × `archived`; `dev/proposals/archive` → 54 × `accepted`, 4 × `superseded`; **historical-token artifacts: 0**. Raw-byte cross-check is stronger still — `grep "^\*\*Status\*\*: *\(open\|executing\|review\)" dev/plans/archive/*.md` returns nothing at all, and every archived plan carries exactly one Status line. (The 7–10 raw `**Status**: revised` hits under `dev/proposals/archive/` are appended-section restatements below the first H2, which `_parse_status` correctly ignores.) The stated *mechanism* is also unreachable: `next_owner` has exactly one call site, `:6183` in the board row builder, and `_board_artifact_paths` (`:5907-5926`) reads direct children only, no archive tree — so no archived artifact can reach `next_owner` at all. **Failure scenario:** the justification cannot survive being checked, which is precisely what invites the deletion [C2] shows is unguarded. The *real* reason to keep the rows is reachable and I demonstrated it — an **active** plan wrongly declaring `executing` renders `owner=implementation` today and `unknown` without them — and it appears nowhere in the comment.

* **[C4] MEDIUM — the standing in-code record of a departure from the plan's own cost list describes a measurement that does not reproduce, and understates the regression.** `tools/lifecycle_planner.py:4174-4185`. The note says that narrowing `_PROPOSAL_POST_REVIEW_STATES` leaves *"only `unknown proposal status`"* and that *"`scan` still exits 1 either way"*. Measured on the exact case it names (§3 above): the narrowing yields **zero violations and exit 0**. Only a *second*, different mutation — also emptying `HISTORICAL_PROPOSAL_STATES`, i.e. the pre-[H1-D2] world — reproduces the stated "after"; the plan's `[H1-D4]` block (`:3620-3636`) carries the same measurement, evidently taken against a partially-applied retirement, and the shipped comment restates it as finished-state fact while additionally re-scoping the case from active to archived. **Failure scenario:** a maintainer does what the comment invites, fails to reproduce it, concludes the note is stale, and proceeds with the narrowing — silently disabling the reviewer-independence check for archived self-reviewed proposals, with no non-zero exit to notice. The *disposition* (keep the tuple wide) is correct and I confirmed it is guarded for the **active** case: narrowing reddens `test_scan_flags_review_authored_by_proposal_author` (`reviewer-authorship` present `True → False`). This finding is about the record, not the behaviour.

* **[C5] MEDIUM — the Known-omissions frozen-path list undercounts by three, and the drift is silent.** `dev/plans/review-efficient-lifecycle.md:3699-3707`. The record names two changed frozen paths plus one `FROZEN-NEW`; measurement (§4 above) shows **five** frozen paths differ from the manifest at `3defdb7`. `test_lifecycle_contract.py` and `test_scope_reduction_trap.py` were already stale at `3defdb7^`; H1 added `test_pilot_evidence.py`, `test_transition_lint.py` and `templates/modules/default-on/_lifecycle_metrics/extract.py`. **Failure scenario:** this section exists to tell the Maintainer what remains before the fenced gate re-anchor. Acting on it re-pins two paths and admits the new file; three stay stale, `test_gate_manifest.py` says `21 passed`, and the omission surfaces at the *next* ceremony attributed to whoever runs it. Note the plan's own cross-cutting section (`:3364`) says *"5 frozen paths changed and 5 discovered FROZEN-NEW — ten, not four"*, so the wider number was known on 2026-08-12; the verification record written a day later narrows it to two without saying why.

* **[C6] MEDIUM — the Boundary B command table records `exit 0` for a command that exits 1.** `dev/plans/review-efficient-lifecycle.md:3666`. Measured deterministically (§5): `EXIT=1`, decomposing to redundancy-only `EXIT=0`, neutrality-only `EXIT=1` — the record's own adjacent `fail=93` is the reason. **Failure scenario:** a reader auditing the ledger, or a future agent scripting that command pair as a pass/fail precondition on the strength of this record, treats the non-zero exit as a regression their own change introduced. The internally contradictory `fail=93` + `exit 0` pairing also costs the ledger credibility on the figures that are right — and most of them are: I reproduced 93/21 and 0/2 at both `3defdb7^` and HEAD, and the `dev/`-scan-root argument for the split-tree discrepancy holds under independent reading of `_NEUTRALITY_SCAN_ROOTS` (`scripts/quality_gate.py:208`), `_R1_SCAN_ROOTS` (`:489`) and `_R6_SCAN_ROOTS` (`:497`) — none contains `dev/` — with `grep -c "dev/"` over the gate output returning **0**.

* **[C7] LOW — a quotation presented verbatim drops a word.** `dev/plans/review-efficient-lifecycle.md:3516-3517` quotes the tripwire as *"Re-point it at the transitions that scaffold the declaration today; do not delete it."* The source (`bootstrap/tests/test_scope_reduction_trap.py:655-658`) reads *"…that scaffold the **Scope-delta** declaration today…"*. **Failure scenario:** a reader greps for the quoted string to find the tripwire and gets only the plan back. Minor mechanically; it earns a line because this plan's own doctrine work is about verbatim quotation of load-bearing text.

* **[C8] OBSERVATION (no reachable failure in the shipped artifact) — a load-bearing fixture sits at a status the tool refuses, undocumented.** `bootstrap/tests/test_lifecycle_contract.py:409-418`. `test_scan_flags_review_authored_by_proposal_author` is the sole behavioural guard on [C4]'s disposition, and it depends on its fixture keeping `status="reviewed"` — now a refused token — yet carries no docstring or comment, in a file where the neighbouring guard nodes all do. The two-step trap: (1) a hygiene pass moves the fixture to `awaiting-decision` (still green, still in the tuple); (2) a later maintainer narrows the tuple (now also green) and the independence check is silently disabled. Both steps were measured green. Step (1) is *more* attractive after H1 than before it. The warning against this lives only in [C4]'s comment — the one that does not reproduce. One-line remedy: a docstring saying the `reviewed` fixture is deliberate and pointing at the tuple. Related and cosmetic: `test_illegal_transition_is_refused` (`:272-279`) still uses `status="proposed"` and now passes degenerately (`legal targets: (none)`), though `TestEveryLegalTransition` covers the real table exhaustively.

#### Refuted during verification

* **Lost `## Code review` scaffold** (claimed [H1-S2] applied asymmetrically). Refuted: `-> awaiting-code-review` is the *implementer's* arm and correctly emits `## Implementation verification`; the reviewer's arms (`-> ready-to-archive`, `-> revising-code`) do print the full code-review grammar, including the four-field basis and the clearing/blocking verdict vocabulary. The dead template is stale and re-pointing it would emit a skeleton that **fails** `review_record_violations` on six predicates — the proposed fix was worse than the state. Downgraded to an observation about unreachable dead code.
* **`tools/lifecycle.py` stale `ready-to-archive` measurement.** Refuted on attribution and reachability: `3defdb7` does not touch that file (the assertion went stale at `ec6139e`, Chunk E), and the `MonitoringIncomplete` branch is reachable only in a tree that has broken the `verbatim=True` fidelity pairing of the two `skills/_lib` files. The retention is deliberated at `[CF3]` and the phrase is pinned by `test_pilot_evidence.py:487`.
* **Board `validity` reason-code collapse** (retired vs unknown both reporting `status-vocabulary`). Refuted: no second command is needed — the `owner` column is a *total, exact* discriminator (proved biconditionally over the whole vocabulary, not sampled), it is pinned by `test_lifecycle_board.py:544-558`, and the closed reason-code set is contract behaviour B1/B2 specify deliberately.

---

### Covered — what was checked and found SOUND

**Contract and vocabulary.** Every derived tuple matches its claimed value *by construction*, not by assertion: `SHAPE_B_STATUSES` 16→12 with `proposed`/`open` re-entering only through the OPENING-states-in-historical filter (the accepted R5 reading, not the trivially-neutral widening), `RECOGNIZED_STATES` unchanged at 20, `PROPOSAL_NON_TERMINAL` 3 / `PLAN_NON_TERMINAL` 7, `NEXT_OWNERS` 10 closed values. Both state machines survive the arm drops: every state reachable from `""`, every state keyed, no transition target outside the current vocabulary, dead ends exactly the declared terminals, `terminal_by_owner == terminal_by_table` for both kinds. All six retired tokens are structurally inert — not keys, not targets, `_legal_transitions` returns `[]`, and `cmd_next` refuses `--to <retired>` before any scaffold runs. Retired-vs-unrecognized was checked on a 13-case matrix and is never inverted, including the fail-closed edges (a non-strict header line yields `_strict_header_status() is None` so the artifact is *not* treated as immutable and the refusal still fires; a cross-kind token is reported unknown, not retired). `scan --include-archive` over the real 102-artifact corpus produces **zero** status-vocabulary findings — the retirement added no archive noise. Board CLI fail-closed behaviour confirmed against a synthetic repo (`--status frobnicated` and `--owner nobody` exit 2; `--status review`, retired-but-recognized, exits 0).

**The four retention decisions.** `[H1-D1]` reproduced through the production path (`_plan_status_enum()` = current + historical, historical last; `'reviewed; awaiting code review'` → `'review'`, regressing to `'reviewed'` if the historical half is dropped; no member is a prefix of another, so order is safe), and its new guard file is real: three separate mutations redden it, including order inversion and single-side twin drift. `[H1-D3]`/`[H1-D4]` dispositions correct, D4's guarded for the active case. `[H1-S1]`/`[H1-S2]` verified by **exhaustive scaffold inventory over all 28–29 reachable transitions**, not by reading: `**Scope delta**` is emitted by exactly two symmetric arms (proposal `revising → awaiting-review`, plan `revising-plan → awaiting-plan-review`), both mutation-caught; `<reviewer>` survives on four to five reachable arms, so the no-attribution property retains live, non-vacuous witnesses (`test_review_scaffold_carries_no_reviewer_attribution` + `test_scope_reduction_trap.py` → `112 passed`).

**Verification-integrity.** The collection delta is exact and fully attributed: 4258 at `3defdb7^` → 4275 at `3defdb7`, per-file `test_metrics_status_normalization` 0→16 and `test_transition_lint` 53→54, with `test_lifecycle_contract` 640→640 (9 defs removed, 9 added — an inversion, not a deletion). **No test was deleted or skipped to reach green.** The corpus rebuttal in the record is true (`test_the_live_corpus_is_sound_under_the_p1_contract` passes at both `3defdb7` and `11a8dde`). SHAPE_B corpus neutrality was re-measured independently of the pinned expectations across all three pinned windows (8/2/1, 5/2/0, 27/2/11 added lifecycle files) — none of the four dropped tokens appears as the status of an added file, so the narrowing can remove no shape-(b) finding, and `test_transition_lint.py` holds 54/54 with its pinned corpus counts unmoved. Twin byte-identity holds for all three pairs at HEAD and is mutation-guarded on both sides. The three fixture-helper defaults the plan flagged as silently drifting were migrated. Every file:line citation in the blast-radius record resolves against the pre-change tree, and `scripts/claim_check.py` on the plan is clean.

**Consumer audit.** No further "reads only the current tuples where it should read history too" defect beyond the one the author fixed: `scripts/transition_lint.py` correctly reads `RECOGNIZED_STATES` + `SHAPE_B_STATUSES`; `_board_validity` correctly reads current-only (the board is active-only); `PLAN_REVIEW_CLEARED_STATES` and `CODE_REVIEW_EFFECTIVE_STATES` correctly current-only.

### Not covered / low confidence

* **Two lenses' reports reached this record in full; the harness delivered adversarial verdicts for one of them.** [C1]–[C4] and [C8] carry an explicit refute-by-default verdict; [C5]–[C7] arrived without one and I re-derived each myself before listing it (the commands are in §4, §5 and the [C7] entry). Findings from the remaining lenses, if any, are not represented here. **Coverage of areas outside contract/vocabulary and verification-integrity should be treated as unestablished, not as clean.**
* **No full suite was run at any point in this review, by design.** The +17 collection delta and the 0-failed figure rest on Boundary B plus the independent per-file collection audit, not on a re-run. If the Maintainer wants the 4275 figure re-observed rather than re-derived, that is a separate spend.
* **The `dev/`-scan-root argument was verified structurally, not by running the gate at `3defdb7` itself** — I ran it at a clean HEAD with a strictly *larger* `dev/` delta than `11a8dde` and got identical figures with zero `dev/` occurrences in the output, which bounds the risk but does not eliminate the split-tree fact the record honestly discloses.
* **Adopter-side behaviour is inferred from twin byte-identity, not exercised.** I did not scaffold a fresh adopter tree and drive the retired vocabulary through it.
* **The concurrent-mutation window.** Two lenses measured against a tree another session was editing. Their *conclusions* were reproduced by me on a pinned-digest clean tree, but any raw figure in their reports taken during that window should be read with that caveat.
* **Security surfaces** (`bootstrap/_scaffold/`, the interpreter binding, the portable sweep) are untouched by this range and were not reviewed; the AST attestation baseline correctly needs no re-anchor.

**Verdict**: **SHIP**

No HIGH survived verification, and the shipped behaviour of H1's central design is correct in both directions on direct probe. The six MEDIUMs are two kinds of debt, both cheap and both worth closing before archive rather than after: **three untested retentions** ([C1], [C2] — the second of which the plan itself predicted and prescribed a fix for, so closing it is arguably owed rather than optional) and **four inaccurate records** ([C3], [C4], [C5], [C6]) that would each mislead the next person to check them — one of which, [C5], mis-states a fenced Maintainer hand-off list by three paths.
## Response to code review -- Claude (Implementation) -- 2026-08-13

Answers: Claude (Internal, delegated) -- 2026-08-13

Eight findings, all against this agent's own work, all accepted. Six are closed in
code at `fc67c29`; three are corrections to landed records and are made **here,
by appending**, rather than by editing the sections they correct -- the record
has to show what was believed when, and a silently-fixed ledger is a worse
artifact than a visibly-corrected one.

The review's framing is the right one and worth restating: none of these breaks
shipped behaviour, which is why no HIGH survived. **Four of them are inaccurate
records.** In a repository whose product *is* the record, that is not a lesser
class of defect than a code bug -- it is the more characteristic one.

| id | disposition |
|---|---|
| C1 | **accept** -- fixed, mutation-verified both directions (`fc67c29`) |
| C2 | **accept** -- fixed, mutation-verified by performing the predicted deletion |
| C3 | **accept** -- justification replaced with the reachable one |
| C4 | **accept** -- note corrected; the truth is worse than the original claim |
| C5 | **accept** -- corrected below; this one mis-states a Maintainer hand-off |
| C6 | **accept** -- corrected below |
| C7 | **accept** -- corrected below |
| C8 | **accept** -- fixture documented |

### [C5] The frozen-path hand-off list was wrong, and it is the fenced one

**Correction, superseding the `Known omissions` paragraph of
`## Implementation verification`.** That paragraph names **two** changed frozen
paths plus one `FROZEN-NEW`. Measured against
`bootstrap/tests/fixtures/gate_manifest.json` (201 entries) at `3defdb7`, **five**
frozen paths differ:

```
bootstrap/tests/test_lifecycle_contract.py
bootstrap/tests/test_pilot_evidence.py
bootstrap/tests/test_scope_reduction_trap.py
bootstrap/tests/test_transition_lint.py
templates/modules/default-on/_lifecycle_metrics/extract.py
```

plus `FROZEN-NEW` `bootstrap/tests/test_metrics_status_normalization.py`, and
`fc67c29` has since also touched `bootstrap/tests/test_lifecycle_board.py`. **The
Maintainer must re-measure at the ceremony parent rather than trust any figure
here** -- which is what Chunk I's cell said in the first place, and what this
error demonstrates the value of.

**How it happened, because the mechanism generalises.** The three paths I missed
are exactly the test files the *delegated repair agents* edited. I wrote the
omissions paragraph from my own memory of what I had touched, and my memory did
not include work I had farmed out. That is the same failure recorded at
`ef5c079` in `dev/PLANNING.md` -- discipline not surviving delegation -- in a
third form: not a budget this time, but an *inventory*. The plan's own
cross-cutting section already said *"5 frozen paths changed and 5 discovered
FROZEN-NEW -- ten, not four"* on 2026-08-12; the record written a day later
narrowed it without saying why. **Nothing is silent about this drift**:
`test_gate_manifest.py` reports `21 passed` with all five stale.

### [C6] The Boundary B table records exit 0 for a command that exits 1

**Correction, superseding that row.** `python scripts/quality_gate.py --sub
neutrality --sub redundancy` exits **1**, not 0. Re-measured deterministically:

```
$ python scripts/quality_gate.py --sub neutrality --sub redundancy >/dev/null 2>&1 ; echo $?
1
```

The cause is a measurement error, not a regression: the original was taken as
`quality_gate ... | grep -E "^\[" ; echo "exit=$?"`, which reports **grep's**
status. `fail=93` and `exit 0` on the same line are mutually contradictory and
should have been caught by reading them together.

**What is unchanged:** the two figures (`neutrality fail=93 info=21`,
`redundancy fail=0 info=2`) are correct, independently reproduced at `3defdb7^`
and at HEAD, and are the pre-existing baseline -- `fail=93` is why the exit is 1,
and it was 1 before this plan began. No gate result moved.

### [C7] A quotation presented as verbatim drops a word

**Correction.** The `[H1-S1]` section quotes the tripwire as *"Re-point it at the
transitions that scaffold the declaration today; do not delete it."* The source
(`bootstrap/tests/test_scope_reduction_trap.py`) reads *"...that scaffold the
**Scope-delta** declaration today..."*. Mechanically minor -- a reader grepping
the quoted string finds only the plan -- but this plan's own doctrine work is
about verbatim quotation of load-bearing text, and the Decision-scribing
guard-rail turns on exactly that discipline. Recorded rather than quietly fixed
for the same reason.

### On the review's own limits

The record is explicit that adversarial verdicts arrived for one lens' findings
and that coverage outside contract/vocabulary and verification-integrity *"should
be treated as unestablished, not as clean"*, and that no adopter tree was
scaffolded. Those are the reviewer's words and this response does not soften
them. It also notes another session edited both planner twins mid-review; the
tree was re-verified afterwards at `3af73b06`, identical to `3defdb7`.

**Re-verification after these fixes** (scoped mapping, canonical interpreter):
`1126 passed, 1 failed` -- the single failure is
`test_the_live_corpus_is_sound_under_the_p1_contract`, reddened solely by another
session's in-flight `dev/plans/comprehension-outlives-the-artifact.md`. Measured:
`scan` names that artifact and zero others, and no violation names this plan.

## Dispositions -- Claude (Implementation) -- 2026-08-13

Every carried-forward obligation, with where it now lives. Two required the
Maintainer; the rest were verified closed rather than asserted closed.

**Dispositions:**

Dispositions use the closed token set (`accept` / `guard` / `wontfix` / `defer`)
that `claim_check` and the archive preflight actually read, rather than prose
labels: *"closed"* and *"homed"* are not dispositions, and a block that reads
well but parses as nothing is the defect this predicate exists to catch. It
caught this one.

| id | disposition | home / evidence |
|---|---|---|
| [CF1] | -> accept | discharged by P2 at `b00ab89` -- `cairn-pilot-event/2` carries a derived `assurance_path` and the report splits eligible from ineligible |
| [CF2] | -> accept | the miscount is gone; the planner comment now reads *"THREE consumers live OUTSIDE this file's package"* (verified 2026-08-13) |
| [CF3] (a) | -> accept | H1's retirement, `3defdb7` -- the six tokens moved to the historical tuples in the same change that migrated the last active artifact off them |
| [CF3] (b) | -> wontfix | withdrawn by the Maintainer, 2026-08-13; authorization quoted verbatim below |
| [CF3] third item | -> wontfix | declined at Chunk E and unchanged; the `UNAVAILABLE` branch stays a live fail-closed guard, kept under test via the inverted fixture |
| [CF4] | -> accept | `TestBasisLegacyEnumerations` is 6 passed -- the two stale grandfather entries are gone (verified 2026-08-13) |
| [CF5] | -> accept | closed by Chunk G, recorded at `12a0ddf` |
| [CF6] | -> wontfix | not deferred work: a declaration that P4 published one line outside its own cell. It was inside the code review's range and drew no finding |
| [CF7] | -> accept | corrected at `1a3ee85` |
| [CF8] (1) | -> accept | quickstart slot tally refreshed at `27fde51` |
| [CF8] (2) | -> wontfix | `verify_stems`' 2 issues are `dev/strategy/` stems, which the checker resolves only under `dev/proposals/` or `dev/plans/`. Measured before and after this plan's edits: identical count, so neither is this plan's to fix |
| [CF9] | -> defer | homed to `dev/PLANNING.md` > Queued at `6c927ff`, at the Maintainer's instruction. Revival condition: the next change to `check_cairn`'s prefix set or to shipped-template citation policy |

### [CF3](b) withdrawn -- Maintainer decision, 2026-08-13

R3 required migration to enumerate the legacy multi-obligation passes in three
**archived** plans and record which obligation each satisfied. The Maintainer
withdrew that obligation. Authorization, quoted verbatim:

> We never need to scan the archives. Those are a historical record, not an
> active area. We can change our handling of future plans and proposals, and
> don't have to go back and adjust the past.

**This is a reduction of accepted scope, and it is labelled as one rather than
absorbed** -- R3's clause is in the accepted contract, and an implementing agent
may not drop it. It is dropped here only because the Maintainer, who holds that
authority, spent it explicitly. The same principle was applied earlier in this
plan when archived artifacts were exempted from retrofitting.

**What is given up, stated plainly so the trade is visible.** The grandfather
list (`_LEGACY_PASSES`) continues to admit those passes wholesale, without
recording *why* any individual pass is acceptable. A later reader asking *"did
that plan actually receive both reviews it declared, or was one pass counted for
both?"* will not find the answer in the record. That question is now permanently
unanswerable for `api-web-security-modules`,
`release-security-orchestration` and `verification-evidence-boundaries`.

**What is not given up.** Nothing live depends on it: both active `+` plans carry
real per-pass `**Obligation**:` lines and resolve their clauses under the current
rule, so the forward contract is intact and unweakened. The three affected plans
are archived and immutable. The decision changes the handling of future
artifacts, not the enforcement applied to them.

### On the loop-fidelity sign-off

Recorded separately below; the archive precondition asks for it by name.

## Lasting-truth migration -- Claude (Implementation) -- 2026-08-13

**Loop-fidelity sign-off, Decision to implementation.** The governing record is the
**accepted** Revision 1 of `2026-08-10-codex-review-efficient-lifecycle` and the
three contracts folded in with it, ratified at the Maintainer's Decision
(`e42f01c`). Implementation ran `1c68926` (Chunk A1/A2) through **`3defdb7`**
(H1's retirement), with the code review's corrections at `fc67c29`. Every chunk
this plan accepted -- A through H, P1 through P6c -- shipped; nothing accepted
was silently dropped, and the two places scope came under pressure were declared
rather than absorbed.

**Corrections forced by independent review, not found by the author.** This is
the part worth recording, because it is the argument for the review tier
existing at all:

* The **plan review** rounds reshaped the chunk table before implementation
  began (Amendments A--D, `## Response to plan review`).
* The **code review** raised eight findings, all against the implementing
  agent's own work, six of which it demonstrated rather than asserted. Four were
  **inaccurate records** -- including a fenced Maintainer hand-off understated by
  three paths, and a Boundary B row recording `exit 0` for a command that exits
  `1`. None was found by the author.
* Two of the three delegated **repair agents** returned defects instead of green
  suites: one refused to loosen an assertion and reported a doctrine sentence
  this agent had deleted while re-homing a template; the other flagged a test
  passing on a substring of an error message this agent had introduced.

**What this plan does not claim.** It does not claim the vocabulary is *right*,
only that it is single-sourced, that retirement is enforced on active artifacts
and silent on archived ones, and that both properties are mutation-verified. It
does not claim the pilot machinery has been exercised by a real monitoring
window -- P6d activation is Maintainer-gated and has not run. It does not claim
adopter-side behaviour was exercised: no fresh adopter tree was scaffolded and
driven through the retired vocabulary, and the code review recorded that gap in
its own words. It does not claim coverage outside contract/vocabulary and
verification-integrity is clean -- the reviewer said *"unestablished, not
clean"*, and this sign-off does not upgrade that.

**One accepted obligation was withdrawn, not delivered**: R3's legacy
multi-obligation mapping over three archived plans, by the Maintainer's explicit
2026-08-13 decision quoted verbatim in `## Dispositions`. It is named here so the
sign-off does not read as "everything accepted shipped" when one thing did not.
