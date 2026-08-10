<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/plans.md doctrine/proposals.md doctrine/lifecycle-contract.md doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: bootstrap/tests/test_lifecycle_board.py, bootstrap/tests/test_lifecycle_vocabulary.py, scripts/gen_legacy_code_review_passes.py, dev/measurement/pilot-activation.md, dev/measurement/pilot-events.md, dev/.cairn/pilot-state.json, tools/__init__.py -->
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
raised to the Maintainer as a scope question, not converted into another
planning artifact. Chunk count is not ceremony; review passes are.

## Bootstrap attestation — the two obligations, recorded manually

This plan's header requires two distinct plan-review passes, but the predicate
that enforces multi-obligation discharge is Chunk E's deliverable. Verified
2026-08-10, today's parser normalizes
`required(**External** + **External Security Review**)` to `('external', None)`
— the second obligation is **silently dropped**, so current tooling would
report the floor satisfied by one pass.

Until Chunk E lands, this table is the enforcement, and the plan stays at
`open` until both rows are filled:

| Obligation | **Clearing** review commit | Verdict | Unresolved findings |
|---|---|---|---|
| `External` | *pending* | *pending* | *pending* |
| `External Security Review` | *pending* | *pending* | *pending* |

**A row is filled only by a distinct clearing pass.** An author Response is
evidence of correction, never the clearing review — the opened table recorded
the blocking pass `8f37a9b` as its own clearance, which is exactly the
self-clearance it was introduced to prevent. Blocking passes so far:
`8f37a9b` (External, REVISE), `ef70da8` (External round 2, REVISE),
`fc96373` (External Security Review, REVISE). Each row needs a later pass
reading `SHIP` with zero unresolved findings before Chunk A begins.

This attestation is retired by Chunk E, in the same commit that makes its
multi-obligation predicate active and tested. It adds no review pass; it makes
the two already-declared passes enforceable during their own bootstrap.

### The gate deadlock, and the one-time exception it needs

Filling both rows above is **not sufficient** to reach Chunk A. Executed under
the canonical interpreter at this commit:

```text
review_record_violations(...)            -> 3 violations
_gating_preconditions(..., 'executing')  -> UNMET: "a CONFORMING '## Plan review'
                                            pass has landed"
```

Every violation is the same shape: a pass declares `**Findings**: raised` and
its Response falls *after* the next pass, outside the parser's positional
ceiling. Append-only forbids inserting a Response between two landed reviews,
so once a blocking pass is overtaken by the next pass, its violation is
permanent and no later pass removes it.

**Precisely which rounds cost a violation** — measured against the parser, not
inferred:

| round shape | adds |
|---|---|
| clearing pass, `**Findings**: none`, no disposition | **0** |
| blocking pass, `**Findings**: raised`, dispositioned before the next pass | **0** |
| blocking pass overtaken by the next pass before its Response | **1, permanent** |

So a **closure pass that ships costs nothing**, and the current count is stable
at **2** — the round-2 and round-3 External passes, each overtaken by the
Security pass that followed it. An earlier revision of this section said the
count "grows by one with every additional review round"; that was imprecise and
is corrected here, because the exception below pins the count and the
Maintainer must pin a number that will not move.

**The exception is the Maintainer's to grant, and is deliberately left
unfilled here.** It authorizes nothing until every field below is completed by
the Maintainer:

| Field | Value |
|---|---|
| Plan blob (`git hash-object`) at authorization | *pending* |
| Clearing `External` review commit | *pending* |
| Clearing `External Security Review` commit | *pending* |
| Exact expected violation text | *pending* |
| Exact expected violation **count** | *pending* |
| Authorizing Maintainer, quoted verbatim | *pending* |

Bounded by construction:

* it authorizes **only** the `awaiting-plan-review → executing` transition and
  the Chunk A/B bootstrap window, for **this artifact only**;
* it is valid only while **no other** violation exists — one additional
  violation of any other shape voids it;
* it **expires when Chunk B lands**, and Chunk B must make this artifact
  conform with **no** wildcard, path-prefix, date, reviewer-name, or reusable
  legacy exemption; and
* a test pins it: changing the plan blob, either review commit, the violation
  text, or the violation count **refuses**, and every broadened or replayed
  form of the exemption refuses.

Because it overrides a live governance gate, the authority is the Maintainer's
alone — no agent fills this table, and no Response substitutes for it.


## Proposed paths

Proposed paths:
- `bootstrap/tests/test_lifecycle_vocabulary.py` — Chunk A's source-audit + shape-(b) matrix.
- `scripts/gen_legacy_code_review_passes.py` — Chunk C's legacy manifest generator.
- `bootstrap/tests/test_lifecycle_board.py` — Chunk F's board CLI and encoder tests.
- `dev/measurement/pilot-activation.md` — P6a's immutable activation record; introduced by P6d.
- `dev/measurement/pilot-events.md` — P6a's append-only event ledger; counts and pauses are derived from it.

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
* The three open security plans (`api-web-security-modules`,
  `release-security-bar`, `security-verification-activation`) — measured
  disjoint: 92 files across their chunk tables, **zero** naming any surface
  above.
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
I   Maintainer re-anchor of the reviewed frozen set[Maintainer]
B2  Boundary B + closeout on post-ceremony commit  [record]
--- pilot ----------------------------------------------------------
P6d pilot ACTIVATION (data-only, Maintainer-gated)  [record]
P7  post-pilot promotion / retirement              [conditional; own evidence]
```

Only *activation* is post-ceremony. The pilot engine, its state schema, its
reports and its tests (P6a--P6c) land before `H`, inside the reviewed range.
Restart cases, split rather than generalized:

1. the ceremony's **reviewed manifest-only** commit proceeds directly to `B2`;
2. any post-Code-review correction to governed implementation, test,
   executable-template or fixture bytes restarts `B1` **and** independent Code
   review;
3. any correction inside the gate inventory additionally restarts the
   Maintainer ceremony `I`; and
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
re-derivation. Run it when the three open security plans have archived or are
quiescent.

### Chunks P1--P7 — the parent contract

The accepted parent's machinery, which the opened plan omitted. One plan; these
are chunks, not another planning artifact.

| # | Surface | Change |
|---|---|---|
| P1 | `tools/lifecycle_planner.py` + twin, both authoring templates + twins | `Assurance path: standard \| high-assurance` declaration, the mandatory high-assurance trigger set, and the four-field review basis (`Reviewed commit`, `Target`, `Prior findings`, `Assurance path`) required across proposal, plan, and Code-review records |
| P2 | same, plus `doctrine/dual-review.md` | proposal `Plan readiness: READY \| DISTINCT REVIEW REQUIRED`, exact accepted-commit binding, standard-plan inheritance, expansion invalidation, and the high-assurance refusal. **Semantic triggers are author declarations, not inferences**: scientific-assumption and undeclared cross-surface risk are declared by the author and surfaced to proposal review and `review-brief`; the tooling checks that the record exists and binds, never the truth of the classification |
| P3 | both authoring templates + twins, planner predicates | complete current-contract revision plus its mandatory `Withdrawn / superseded commitments` ledger |
| P4 | `tools/lifecycle.py` + installed twin | deterministic `review-brief`; expanded `closeout --dry-run`. **Fenced**: P4 does not modify `_resolve_interpreter` (`tools/lifecycle.py:414`), its schema, validation order, fallback disposition, warning visibility, or any subprocess use of the resolved path — the protected local interpreter binding named in `AGENTS.md`. Pinned by a focused exact-function-byte / AST sentinel test. If implementation needs such a change, **stop for a new Security Review**. Both commands stay read-only and execute no artifact content; human output passes through the **same** terminal encoder as F2. **The planner owns it**: the encoder lives in `tools/lifecycle_planner.py` (and its installed twin), and `tools/lifecycle.py` reaches it by the **same A3 contained-loader contract** — fixed `spec_from_file_location`, no ambient `sys.path`, no `tools/__init__.py`, no CLI import with side effects. This adds no install-manifest row: both files already install as siblings under `tools/`. The existing `_safe_field` (`tools/lifecycle.py:113`) is **not** this rule — it translates a fixed escape table and truncates; it applies neither `str.isprintable()` nor `_DISPLAY_UNSAFE_RANGES` — and is replaced, not wrapped. Machine output is versioned ASCII-safe JSON. Control-character, invisible-range, delimiter, malformed-record and mutation-sentinel tests, **plus the full A6 loader matrix for this second consumer** (decoy path, leaf and parent symlink, out-of-root, partial-import cleanup, clean retry) and byte/parity checks for every installed twin |
| P5 | planner + `bootstrap/tests/test_lifecycle_contract.py` | the bound `Contract non-expansion: VERIFIED \| NOT VERIFIED` attestation with its `Basis:` line; `NOT VERIFIED` blocks. Validates presence and binding shape only — the parent is explicit that the semantic claim stays human |
| P6a | `tools/lifecycle.py` + twin, `dev/measurement/pilot-activation.md`, `dev/measurement/pilot-events.md` | **pilot engine, inside the reviewed range**, split so no authority input is a mutable last-writer-wins file. (1) An **immutable tracked activation record** naming `machinery_sha` = the reviewed **B2** commit; the *enabling* commit is derived from Git as the commit that first introduced this exact record, so nothing is self-referential, and `activation_date` is that commit's author date. (2) An **append-only tracked event ledger** — one event per counted plan stem or pause, each bound to its source artifact and commit — from which counts, pauses, and the report are **derived**, never stored. Six-plan rule = distinct plan stems reaching `ready-to-archive` under the contract; 60-day window from the derived activation date inclusive. Every writer: repository containment, regular non-symlink leaf **and** parent, closed bounded schema, atomic replace-or-append with an expected-old check, clean refusal on race or `OSError`. Malformed or unknown-version **refuses**; it never defaults to inactive |
| P6b | `dev/collaboration_agreement.md` + twin | the pilot's human contract: pause conditions, evidence report shape, and the Maintainer promotion Decision at the boundary |
| P6c | `bootstrap/tests/test_lifecycle_contract.py` | pilot mutations: absent record, wrong schema version, altered prior event, duplicate or conflicting stem, symlink redirection of leaf or parent, interrupted write, stale writer / lost update, boundary-day arithmetic, pause set and cleared, and the exact activation-binding oracle (a record whose `machinery_sha` is not the B2 commit, and a derived-enabling-commit mismatch, both refuse) |
| P6d | `dev/measurement/pilot-activation.md` | **activation only** — the data-only, Maintainer-gated commit introducing the immutable activation record after B2, enabling already-reviewed machinery. No code lands at activation |
| P7 | `doctrine/`, both authoring templates + twins, `docs/workflow-role.md`, `docs/getting-started.md`, `docs/tool-usage.md`, `templates/skills/_lib/` | **conditional** post-pilot `promote` / `revise` / `retire`, each with distinct behavior, plus the three-layer canonical / self-hosted / shipped-template parity contract. Executes only after the Maintainer's promotion Decision |
| P8 | `bootstrap/tests/test_lifecycle_contract.py` | end-to-end standard-READY and high-assurance-refusal fixtures, plus a **row-level assurance matrix**: missing / duplicate / unknown `Assurance path` values (all refuse — **never default to `standard`**); every mechanically recognizable protected-surface trigger; uncertainty resolving **high**; high-assurance and `DISTINCT REVIEW REQUIRED` inheritance refusal; changed proposal / review / Decision SHAs; every named expansion dimension; unresolved findings; stale Boundary B; malformed or missing non-expansion `Basis:`; and a downgrade admitted only through a structurally valid Maintainer Decision |

**Tier: Opus for P1--P3, P5 and P6a** (contract authorship on records every
future artifact inherits, plus the pilot state schema). **Sonnet for P4, P6c
and P8** (CLI surface, mutations and fixtures against a fixed contract, all
oracle-rich). **P6b/P6d/P7 are Maintainer-gated.**

**Phase separation, inside this plan.** P6a--P6c ship *before* H/B1, so the
pilot capability is inside the reviewed range and carries the plan's Code
review and stable evidence. P6d is data-only activation after B2. **P7 carries
its own evidence**: before it executes it produces an exact changed-path
manifest, runs the gate-manifest classification over it, and then — if it
changes any executable, test, template or fixture byte — takes a fresh
Boundary B and an independent Code review, and if it changes a frozen path,
another Maintainer ceremony. P7 is not assumed docs-only.

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
* Boundary B **twice**, same command pair each time — `python -m pytest
  bootstrap/tests --quality-gate-shuffle-seed=0` then `python
  scripts/quality_gate.py --sub neutrality --sub redundancy`, canonical
  interpreter, clean commit — recorded as two dated
  `## Implementation verification` sections:
  1. **B1**, on the stable pre-review commit after Chunk H;
  2. **B2**, on the post-ceremony commit after Chunk I, because the re-anchor
     rewrites `bootstrap/tests/fixtures/gate_manifest.json` inside the reviewed
     range and the runbook itself runs the suite zero times.
* Boundary C: one code review over the B1 range.
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
