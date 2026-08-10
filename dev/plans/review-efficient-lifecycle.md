<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/plans.md doctrine/proposals.md doctrine/lifecycle-contract.md doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: bootstrap/tests/test_lifecycle_board.py, bootstrap/tests/test_lifecycle_vocabulary.py, scripts/gen_legacy_code_review_passes.py -->
<!-- The three paths above are forward references created by Chunks A, C and F.
     They are also registered under `Proposed paths:`; that marker exempts only
     its own contiguous bullet block, so this file-scoped directive covers the
     chunk tables that name the same paths. Each line drops when its file lands. -->

# Plan: one lifecycle contract, one evidence boundary

**Source proposal**: [`review-efficient-lifecycle`](../proposals/2026-08-10-codex-review-efficient-lifecycle.md),
executing jointly with its three accepted amendments —
[`claim-check-exemption-hygiene`](../proposals/2026-08-10-codex-claim-check-exemption-hygiene.md),
[`code-review-blindness`](../proposals/2026-08-10-claude-code-review-blindness.md),
and [`lifecycle-status-vocabulary`](../proposals/2026-08-10-codex-lifecycle-status-vocabulary.md).
All four are `accepted`, and three of them state in their own accepted text
that they open no standalone plan. This is that plan.
**Status**: open
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
| Plan review | **2** | Now, before any implementation. The two declared obligations, one pass each. |
| Boundary A | per chunk | Scoped tests only. Not a review; no sign-off, no section. |
| Boundary B | **1** | Once, after the final implementation commit, on a clean commit. |
| Code review | **1** | Once, over the stable range. |
| Maintainer ceremony | **1** | One re-anchor for the whole batch. |
| Archive | **1** | One closeout. |

**Six touchpoints for the whole cluster.** Four separate plans would have cost
four of each — roughly twenty. That arithmetic is the case for consolidation;
if this plan ever grows a per-chunk review, it has lost its reason to exist.

Boundary A/B/C are the already-accepted
[`verification-evidence-boundaries`](archive/verification-evidence-boundaries.md)
contract, which is implemented today. This plan uses it; it does not wait on
its own deliverables to verify itself.

**No chunk opens a sub-plan.** A discovery that needs its own contract is
raised to the Maintainer as a scope question, not converted into another
planning artifact.

## Proposed paths

Proposed paths:
- `bootstrap/tests/test_lifecycle_vocabulary.py` — Chunk A's source-audit + shape-(b) matrix.
- `scripts/gen_legacy_code_review_passes.py` — Chunk C's legacy manifest generator.
- `bootstrap/tests/test_lifecycle_board.py` — Chunk F's board CLI and encoder tests.

## Scope

The four accepted contracts, implemented once over one shared surface:
`tools/lifecycle_planner.py` and its installed twin, the two
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
* The three open security plans (`api-web-security-modules`,
  `release-security-bar`, `security-verification-activation`) — measured
  disjoint: 92 files across their chunk tables, **zero** naming any surface
  above.
* `[F1]` from the round-4 review of `lifecycle-status-vocabulary` — pending
  that proposal's Revision 4. Chunk F implements whichever escaping rule that
  revision lands; this plan does not pre-empt the choice.

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
A  central vocabulary + contained loaders          [commit pending]
B  canonical pass boundaries                       [commit pending]
C  Code-review record schema + legacy manifest     [commit pending]
D  claim-check archive resolution + registry       [commit pending]
E  status vocabulary, transitions, conformance     [commit pending]
F  the derived board                               [commit pending]
G  doctrine, templates, agent teaching             [commit pending]
H  migration + source-proposal archive             [commit pending]
I  Maintainer re-anchor ceremony                   [Maintainer]
```

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
| A3 | `tools/_lifecycle_metrics/extract.py` | drop `_PLAN_STATUS_ENUM`; load the planner by fixed path from its own resolved location, refusing missing/symlinked/out-of-root; closes the pre-existing `awaiting-plan-review` omission |
| A4 | `templates/modules/default-on/_lifecycle_metrics/extract.py` | byte-identical twin; refuses at its source-tree location (no sibling planner there) |
| A5 | `scripts/transition_lint.py` | drop `_OPEN_STATUSES`; consume the central added-artifact set; unknown status becomes an advisory finding, never silent skip |
| A6 | `bootstrap/tests/test_lifecycle_vocabulary.py` | source audit rejecting any consumer-local status literal; shape-(b) synthetic matrix over every central state; loader containment, symlink refusal, and the three metrics-location cases |
| A7 | `bootstrap/tests/test_transition_lint.py` | extend for the new opening states |

**Tier: Opus.** Contract authorship plus loader containment; no mechanical
oracle for "is this the right vocabulary boundary."

### Chunk B — canonical pass boundaries

| # | File | Change |
|---|---|---|
| B1 | `tools/lifecycle_planner.py` + twin | build every selected pass body **and** every next-pass ceiling from one ordered set of raw conforming boundaries of both kinds, unioned with H1/H2 |
| B2 | `bootstrap/tests/test_lifecycle_contract.py` | pin both mutations: a later pass's `**Tier**`/`**Findings**` must not enter the earlier body; a disposition after the later pass must not satisfy the earlier |

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
| F2 | same | terminal-safe encoder per `lifecycle-status-vocabulary` Revision 4 |
| F3 | `tools/_intent/cli.py` + `templates/modules/team-gated/_intent/cli.py` | versioned `--format json` for `list` only; existing semantics unchanged |
| F4 | `tools/lifecycle_planner.py` + twin | optional intent provider: fixed-path sibling `tools/intent.py`, isolated invocation, schema validation, `not-installed`/`error` distinct from "no claim" |
| F5 | `bootstrap/tests/test_lifecycle_board.py` | rows, ordering, filters, injection, provider failure modes, encoder sweep |

**Tier: Sonnet for F1/F3/F5, Opus for F2/F4.** The renderer and filters are
oracle-rich. The encoder rule and provider containment are not — F2 is where
the round-4 finding lives, and F4 crosses a module boundary.

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
| H1 | active proposals and plans | evidence-derived status migration over a pinned parent commit; blob-identity re-check before each edit; ambiguous artifacts refuse |
| H2 | active proposals and plans | exemption-metadata migration: inert headers out, unused globs out, live globs to typed declarations |
| H3 | `dev/proposals/*.md` → `archive/` | the four source proposals, after D1 is in the tree |
| H4 | `dev/PLANNING.md` | row-move for the four |

**Tier: Sonnet to execute, Opus to review the proposed table before it is
applied.** The mechanics are pinned and blob-checked; the classification of an
ambiguous artifact is judgment.

**H runs last and needs a quiet tree.** It rewrites the `Status:` of every
active artifact, so concurrent lifecycle commits cause blob-mismatch
re-derivation. Run it when the three open security plans have archived or are
quiescent.

### Chunk I — Maintainer re-anchor

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
* Boundary B once: `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0`
  then `python scripts/quality_gate.py --sub neutrality --sub redundancy`,
  under the canonical interpreter on a clean commit, recorded as
  `## Implementation verification`.
* Boundary C: one code review over that range.

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
