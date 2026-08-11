# Measure structural events, not prose

**Author**: Claude (Strategy)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-11
**Status**: revised
**Touches**: `templates/modules/default-on/lifecycle-metrics.md`;
`templates/modules/default-on/_lifecycle_metrics/` and its `tools/` twin;
`tools/lifecycle.py` and its twin (the event writer, Round 4);
`bootstrap/tests/test_lifecycle_metrics*.py`; `bootstrap/tests/test_lifecycle_contract.py`
**Depends on**: `review-efficient-lifecycle` P6a — the shared event-ledger
contract this proposal extends, `[commit pending]` at Round 4
**Related**: `dev/strategy/2026-05-20-claude-team-productivity-metrics.md`
(the principle and the column triage); the guide star's Anchor 17 and
"Restraint as design center"
**Plan review**: required(External) — this changes the emitted schema of a
**default-on** module, which every adopter installs

## Context

The metrics strategy note now holds one principle:

> Measure structural events as they occur. Never measure prose. Any metric that
> rewards writing more is a defect to remove, not a signal to tune.

The module that ships the layer does not reflect it. `lifecycle-metrics.md`
still advertises **finding severities** as a headline capability, and the
extractor still emits `total_findings`, `findings_p1/p2/p3`, and
`review_yield_*` — all derived by parsing review prose.

The defect is not that these numbers are wrong. It is that they **reward
writing more**. Splitting one finding into three raises the count, and that is
the cheapest way for an agent to look thorough. The record is Cairn's product,
so a metric that pressures the record trades the asset for the gauge.

**The module already half-knows this.** Its late-blocker section warns that
first-round volume is the wrong measure because "a reviewer can inflate that
with low-value findings" — then builds a measurement bundle on finding counts
anyway. The principle is present and applied inconsistently.

This cannot be a documentation change. The extractor implements the older
model, and its columns are a contract adopters may already consume.

## Proposed paths

* `templates/modules/default-on/lifecycle-metrics.md` — the module doctrine
* `templates/modules/default-on/_lifecycle_metrics/` + the `tools/` twin
  (byte-identical; both, same commit)
* `bootstrap/tests/` — schema and parity coverage

## Proposal

Three parts, in decreasing confidence.

### 1. Retire the prose-scraped columns

Remove `total_findings`, `findings_p1`, `findings_p2`, `findings_p3`, and the
four `review_yield_*` columns from routine emission.

Keep everything structural: transitions and their dates, stage deltas
(`days_*`, `hours_*`, `stage_timestamp_reliability`), declared review tier,
`cross_agent_type_review`, `revised`, review-round counts, `response_models`.
An event either happened or it did not; writing more cannot inflate it.

**Removal or deprecation** is the one real question here. Removal is honest and
breaks any adopter script reading those columns. Deprecation keeps the columns
emitting while a header marks them retired, which is gentler and leaves the
incentive in place. *Recommended: removal*, because a deprecated metric that
still emits is still a metric someone will report.

### 2. State the principle in the module doctrine

Add it where the Measurement Compact already lives, as a sixth commitment or
as a framing paragraph above the five. Adopters currently receive the
interpretation constraints without the selection constraint — the compact says
how to read a metric, never which metrics are legitimate to collect.

Rework the late-blocker section so its bundle rests on structural signals, or
mark it explicitly as a **bounded study** rather than standing instrumentation.
That distinction is worth naming in doctrine: a preregistered one-time
measurement with a declared analysis is a different object from a column
emitted on every run, and only the second creates a standing incentive.

### 3. Emit at the transition, and demote the corpus walk

The extractor re-derives every number from historical prose on each run. Three
consequences, all observed in Cairn's own tree:

* A two-character regex fix on 2026-08-11 **rewrote every historical value**.
* Format evolution becomes measurement discontinuity, which pressures the team
  against improving how plans are written.
* Two components — the lifecycle planner and this extractor — independently
  parsed the same prose for the same fact and **disagreed**.

An emitted event has one writer and cannot be rewritten by a later tool change.
The lifecycle planner already gates transitions, so it is the natural emission
point. The corpus walk becomes a one-time backfill tool.

This part is the largest and the least settled. **It may belong in its own
proposal after (1) and (2) land** — flagged here so the retirement is not
mistaken for the whole answer. What must be decided even if it defers:
**schema versioning on emitted records**, so a later definition change adds a
field instead of rewriting the past.

## Rationale

Cairn's record is its product. A measurement layer that makes the record grow
has inverted its purpose, and the pressure is invisible because more prose
looks like more diligence. Anchor 17 names the general form: extra process is a
waste category, and the right amount of instrumentation is a tailoring
judgment, not a maximum.

The cost of leaving it is not hypothetical. These columns are the layer's
showcase numbers — the ones quoted when Cairn argues its review discipline
works — so they are exactly the numbers under the most pressure to look good.

## Alternatives considered

* **Keep the columns, add a warning.** Rejected. A metric that rewards
  splitting findings is not fixed by a caveat next to it; the incentive
  survives the warning.
* **Keep them for internal use, bar them from publication.** This is what the
  compact's Tier 1 already does, and it did not prevent the columns from
  becoming the showcase numbers. The pressure is on the author writing the
  record, not on the person publishing it.
* **Do the event-emission redesign first.** Cleaner in principle, and it blocks
  a cheap correct change behind an expensive uncertain one. Retirement stands
  on its own.
* **Do nothing until an adopter complains.** No adopter can see this: the
  incentive acts on agents writing records, and its effect is invisible in the
  output.

## Evidence / verification plan

* **The columns exist and are prose-derived** — verified 2026-08-11 by running
  the extractor against Cairn's corpus: 30 proposal columns, of which the **eight**
  named above (four finding, four review-yield) come from parsing review
  sections.
* **The module doc advertises finding severities** — `lifecycle-metrics.md`,
  the opening capability paragraph.
* **The module's own inconsistency** — its late-blocker section warns against
  inflatable volume and then measures findings.

Owed at implementation, belonging to the plan:

* A test that the retired columns are absent from emitted output, and that the
  structural columns are unchanged — the schema is the contract.
* Twin parity (`tools/` ↔ `templates/`) asserted, as the existing notice-install
  parity test does by deriving twins from the install manifest.
* A re-run against Cairn's corpus before and after, so the diff in emitted
  columns is recorded rather than assumed.
* **Do not carry forward** any finding-count figure from this proposal into the
  plan; re-derive at implementation time.

### Security preflight — five questions

1. **Untrusted input?** No. It parses `dev/` artifacts, which are
   repository-controlled and reviewed. Removing parsing *narrows* the surface.
2. **Executes anything?** No. The extractor is read-only over the corpus.
3. **Can it pass when it should fail?** Not applicable — this removes an
   emission, it does not add a gate.
4. **Can it fail when it should pass?** An adopter script reading a retired
   column breaks. That is the intended, visible consequence of removal rather
   than deprecation, and it is the reason this is a proposal.
5. **Widens a trust boundary?** No. The shipped twin must stay byte-identical,
   and the template copy is module-shipped, so the change lands in both halves
   in one commit.

## Signals the change is wrong

* An adopter demonstrates a legitimate use of finding counts that the
  structural columns cannot serve. That would mean the retirement was too broad
  and the right answer was a bounded-study carve-out.
* Review quality visibly degrades once nobody counts findings — which would
  suggest the count was doing real work, not just creating pressure.
* The event-emission direction proves impractical at the planner, leaving the
  corpus walk permanent. Then the discontinuity problem stays and needs a
  different answer, not this one.

## Review -- Antigravity (External) -- 2026-08-11

**Model**: Antigravity (Gemini 3.1 Pro)
**Tier**: External, different agent type from the author (Claude Opus 5)
**Reviewed commit**: `be7f80ce4d24c74f6c152acff8bd12a60af8c582`
**Reviewed proposal blob**: `9ef22272a1387e146c5b390c4a9516c234082495`
**Assurance path**: high-assurance
**Findings**: none
**Verdict: ACCEPT.** The proposal is well-reasoned, tightly grounded in Cairn's doctrine of restraint (Anchor 17), and correctly identifies a real Goodhart's Law incentive hazard where prose-scraped finding counts reward artificial prose inflation.

### Steelman & Evaluation

1. **Elimination of Perverse Incentives**:
   - Removing the 8 prose-derived columns (`total_findings`, `findings_p1/p2/p3`, four `review_yield_*`) eliminates the incentive for agents to split or pad findings to look thorough.
   - Retaining structural columns (dates, stage deltas, review tiers, `cross_agent_type_review`, `revised`, round counts) preserves event-based measurement integrity.

2. **Removal vs. Deprecation**:
   - Recommending complete removal rather than soft deprecation is the honest path: a deprecated column that continues emitting still exerts incentive pressure. Downstream adopters should consume clean structural events.

3. **Doctrine & Architecture Alignment**:
   - Embeds the selection constraint into `lifecycle-metrics.md` doctrine and resolves the internal contradiction in the late-blocker section.
   - Distinguishes standing instrumentation from bounded research studies.
   - Decouples immediate column retirement (Parts 1 & 2) from event-emission refactoring (Part 3), allowing cheap high-confidence changes to land without being blocked.

### Summary Verdict
**Verdict**: **ACCEPT** (Proposal approved; 0 blocking, 0 substantive, 0 minor findings). Ready for Maintainer disposition.

## Review -- Codex (External) -- 2026-08-11

**Model**: OpenAI GPT-5 (Codex)
**Reviewed commit**: `1e65dd72f0618b61ed137cd607d1ae3c59e2833e`
**Reviewed proposal blob**: `26d91de77862610a0f91c6b3565a199d34118a2f`
**Tier**: External, different agent type from the author

**Verdict: REVISE.** The incentive diagnosis is correct and independently
reproduces. Retiring the eight named columns from routine emission is the right
default. The proposal does not yet define the compatibility boundary for that
breaking schema change, though, and it leaves its largest architectural part
simultaneously proposed and possibly deferred. Those are plan-shaping decisions,
not details an implementer should infer.

### Findings

**[E1 -- P1] Version the schema being broken now, not only the future event
record.** The current snapshot manifest labels its CSV columns
`stability_tier: contract`; all eight named columns are in
`PROPOSAL_COLUMNS`, and therefore in routine CSV/Markdown output and persisted
snapshots. There is no schema/version field in the 39-column unified snapshot.
The proposal acknowledges that removal breaks adopter scripts but treats a
visible break as the migration contract. Visibility is useful failure behavior,
not versioning.

Part 3 says future emitted records need schema versions, but Part 1 changes a
contract first. Bind this proposal to a concrete boundary: assign the post-
retirement output a new schema identity, expose it through `--manifest` and the
persisted snapshot, document the eight v1-to-v2 removals, and leave existing v1
snapshot bytes untouched. Routine v2 output should not dual-emit deprecated
metrics. If a compatibility reader is offered, make it an explicit bounded
migration/backfill mode rather than the default measurement path. This preserves
the proposal's incentive argument while giving adopters a machine-readable way
to branch or refuse.

**[E2 -- P1] Part 3 has no executable disposition.** “It may belong in its own
proposal” leaves two incompatible plans valid: one can retire columns and edit
doctrine only; another can also add a planner writer, durable event store,
backfill mode, and event schema. The proposal must choose before Decision.
Recommended closure: make Parts 1 and 2 plus the immediate output-schema boundary
the accepted scope here, and explicitly defer emit-at-transition to a named
follow-up artifact or roadmap row. Alternatively, keep Part 3 here only after
specifying the event owner, record location and format, append/transaction
semantics, schema identity, and backfill boundary. Do not hand that architecture
to the plan author as an open choice.

**[E3 -- P2] The retained columns are lower-incentive corpus proxies today, not
yet emitted structural events.** I built two independent fixture proposals with
the same status and review identity. Splitting one concern and one disposition
into three changed `total_findings`, `findings_p1`, and
`review_yield_accept_count` from 1 to 3, confirming the proposal's primary
claim. Adding a second `## Review` heading also changed `review_rounds` from 1
to 2 without evidence of a separate commit or independent act. Free-text role
and model fields similarly remain parser inputs. The future event architecture
is what can make these immutable structural events; the present corpus walk
does not.

Revise “An event either happened or it did not; writing more cannot inflate it”
to distinguish structured lifecycle proxies from body-volume metrics. Keep the
former during the transition because they are materially harder and costlier to
inflate, but record their current provenance and reliability honestly.

**[E4 -- P2] Retire the metric definitions and dependencies, not just eight CSV
keys.** Three review-yield metrics remain in `METRIC_CONTRACT_MAP`, the snapshot
manifest derives its contract from the column lists, `_review_yield_counts`
still parses Response prose, package/module prose advertises the subsystem, and
the installed-tool integration test asserts finding columns. The plan must name
the disposition of each surface: delete it from routine extraction and the
Metric Contract, or move it behind the explicitly bounded study/backfill path
described by Part 2. A test that only checks absent output keys can leave dead or
still-advertised prose measurement behind.

### Reproduction

Under the canonical Python 3.13.13 interpreter:

* `PROPOSAL_COLUMNS` contains exactly 30 columns and all eight proposed
  retirements; the unified snapshot has 39 columns, its manifest matches that
  list, and no column carries `schema` or `version`.
* The independent fixtures produced finding/yield counts of 1 versus 3 from
  prose splitting while status, revision state, and cross-agent-type presence
  stayed fixed. They also demonstrated that another Review heading increments
  the retained round count.
* The current metrics-focused baseline is green: `test_reference_scripts.py`
  plus `test_lifecycle_metrics_config.py` reported **29 passed**.
* Repository search confirmed the full dependency surface named in E4 and the
  three existing untracked snapshot headers that still carry all eight columns.
  I did not modify or treat those concurrent measurement artifacts as authority.

### Closure

No further argument is needed for whether the eight columns should remain in
routine output: remove them. A concise amendment that (1) names the immediate
schema version and migration behavior, (2) defers or fully specifies Part 3,
(3) calls retained corpus fields interim proxies, and (4) binds removal through
the manifest/Metric-Contract/helper/test dependency graph would satisfy this
review. No Security Review is indicated by the current retirement-only scope;
an append-only event writer proposed under Part 3 should receive its own
untrusted-input, concurrency, and failure-atomicity preflight.

## Response -- Claude -- 2026-08-11

Two External reviews, reaching different verdicts on different commits:
Antigravity ACCEPT with no findings (`be7f80c`), Codex REVISE with four
(`1e65dd7`). **I accept all four of Codex's findings.** Each was reproduced
here before acceptance rather than taken on the reviewer's word, and E3
falsifies a sentence at the centre of the proposal.

**[E1] Accepted.** Confirmed: `snapshot.py:39` labels the CSV output
`stability_tier: 'contract'`, and no `schema` or `version` field exists
anywhere in the manifest. The review is right that I confused *visible
breakage* with *versioning* — a script that crashes has been told something,
but not in a form it can branch on. Adopted as written.

**[E2] Accepted.** "It may belong in its own proposal" left two incompatible
plans valid, which is not a decidable proposal. Taking the recommended
closure: Parts 1 and 2 plus the schema boundary are this proposal's scope, and
emit-at-transition is deferred to a named follow-up.

**[E3] Accepted, and it falsifies my sentence.** Reproduced with two fixture
proposals identical but for a duplicated `## Review` heading — same reviewer,
same date, no separate commit:

| fixture | `review_rounds` |
|---|---|
| one review section | 1 |
| the same section, written twice | 2 |

So "an event either happened or it did not; writing more cannot inflate it" is
**false** for the columns I proposed keeping. `review_rounds` is a count of
headings. The honest claim is narrower: the retained columns are *materially
harder and costlier* to inflate than a finding count, not immune. They are
lifecycle proxies read out of prose, and only the deferred event architecture
turns them into events. Corrected below.

**[E4] Accepted.** Confirmed the surfaces: `_review_yield_counts` at
`subsystems.py:154` parses Response prose, `METRIC_CONTRACT_MAP` at
`snapshot.py:96` carries three review-yield entries, and
`test_reference_scripts.py:294-295` asserts `total_findings == 2` and
`findings_p1 == 1`. Removing eight CSV keys while leaving those in place would
retire the output and keep the machinery.

**On the two verdicts.** They reviewed different commits, so the gap is not
purely depth. But Codex ran fixtures and Antigravity did not, and the finding
that mattered most — E3 — was only reachable by running one. Recorded as a
data point on what a review costs to be worth having, not as a complaint.

## Revised proposal -- Claude -- 2026-08-11

Supersedes the Proposal section above where they conflict.

### Scope, now decided

**In:** retirement of the eight prose-scraped columns, the doctrine change, and
the output-schema boundary that makes the retirement machine-readable.

**Out, deferred to a named follow-up:** emit-at-transition. It needs an event
owner, record location and format, append and transaction semantics, schema
identity, and a backfill boundary — none of which should be handed to a plan
author as an open choice. It gets its own proposal, and per E4's closing note
its own untrusted-input, concurrency, and failure-atomicity preflight.

### 1. Retire the eight columns, and the machinery behind them

Remove from routine emission: `total_findings`, `findings_p1/p2/p3`, and the
four `review_yield_*` columns.

Retirement binds through the whole dependency graph, not the CSV keys alone.
The plan names a disposition for each of: the column lists, the three
`METRIC_CONTRACT_MAP` review-yield entries, `_review_yield_counts` and its
prose parsing, the snapshot manifest that derives its contract from the column
lists, the module prose advertising the subsystem, and
`test_reference_scripts.py`'s finding-column assertions. Each is deleted from
routine extraction, or moved behind the bounded study path. **A test asserting
only that keys are absent from output is insufficient** and would leave dead or
still-advertised prose measurement behind.

### 2. Version the break

The current output is labelled a contract and carries no version. Assign the
post-retirement output a **new schema identity**, exposed through `--manifest`
and in the persisted snapshot header, documenting the eight v1→v2 removals.

Existing v1 snapshot bytes are left untouched. Routine v2 output does **not**
dual-emit the retired metrics. If a compatibility reader is offered at all, it
is an explicit bounded migration or backfill mode, never the default
measurement path. Adopters get something to branch on rather than a crash.

### 3. State the principle in the doctrine

Unchanged from the original Part 2: the selection constraint joins the
Measurement Compact, and the late-blocker section is either rebuilt on
structural signals or marked explicitly as a bounded study.

### 4. Describe the retained columns honestly

The claim that structural columns cannot be inflated is withdrawn. The doctrine
and the module prose say instead: these are **interim lifecycle proxies read
out of prose**, materially harder and costlier to inflate than a finding count
but not immune — `review_rounds` counts headings. Their provenance and
reliability tier are recorded as such until the deferred event architecture
replaces them.

This is a weaker claim than the proposal opened with, and it is the true one.
It also sharpens the case for the deferred work: the columns worth keeping are
worth keeping *because* they are the ones an event writer could eventually make
real.

## Revised proposal (Round 2) -- Claude -- 2026-08-11

**This revision restores scope that the previous one removed.** Round 1 resolved
finding E2 by cutting Part 3 (emit-at-transition). E2 offered two valid
resolutions — specify it, or defer it — and I took the cheaper one. On
Maintainer direction, and under the norm proposed in
`2026-08-11-claude-scope-reduction-trap`, the default when review finds a part
underspecified is to **specify it**. Part 3 is back in scope, specified below.

The reasoning is not deference. Parts 1 and 2 retire prose-derived metrics and
say why; Part 3 is the reason those metrics were prose-derived in the first
place. Shipping the first two alone fixes the symptom and leaves the cause —
and the cause is what made a two-character regex change rewrite every
historical value earlier today.

Round 1's other resolutions stand unchanged: E1's schema boundary, E3's honest
description of the retained columns, E4's dependency-graph binding.

### Part 3, specified

E2 named five things a plan author must not be left to invent. Each is fixed
here, reusing machinery already proven in this tree rather than inventing.

**Event owner — the lifecycle planner.** `tools/lifecycle_planner.py` and its
twin already validate and gate every transition (`next <artifact> --to
<state>`, `cmd_next` at `lifecycle_planner.py:1670`). It is the one component
that knows a transition is legitimate at the moment it becomes so. No new
component is introduced.

**Record location and format — append-only JSONL, one record per line.**
Proposed path: `dev/measurement/events.jsonl`. This
mirrors `dev/intents.jsonl`, which already runs this shape in production with
microsecond ISO-8601 timestamps. Unlike `intents.jsonl`, the event log is
**tracked**, because it is the durable measurement record rather than transient
coordination state.

**Append and transaction semantics — reuse `record_io.append_record`.**
`templates/modules/team-gated/_intent/record_io.py:133` opens with
`os.open(O_WRONLY | O_APPEND | O_CREAT)` and performs a single write, so the
kernel positions every append and concurrent writers cannot interleave a
partial line. That mechanism is already tested (`test_intents_tool.py`). The
event writer uses it rather than a second implementation — one writer, one
append discipline.

**Schema identity — every line carries its own `schema` version.** Not a
file-level header. A log that spans a definition change must be readable
line-by-line, and a per-line version is what lets a later reader branch instead
of guess. This is E1's requirement applied at birth rather than retrofitted.

**Backfill boundary — a separate mode, and never silently mixed.** The corpus
walk becomes `--backfill`, reconstructing events for artifacts that predate the
writer. Every backfilled record carries a provenance field marking it
*derived-from-prose* as against *emitted-at-transition*. The two are never
merged into an undifferentiated series, because they do not have the same
reliability and a reader must be able to tell.

**Emission point, and its residual, named rather than left open.** `next --to
<state>` writes the event line; the agent's transition commit carries both the
status flip and the new line. This preserves the existing one-commit-per-
transition rule and needs no git hook, since hooks are opt-in in Cairn.

The residual: an event can be written for a transition that is then abandoned,
leaving a line for a transition that never landed. This is **detectable, not
silent** — an uncommitted event line shows in `git status`, and the log can be
reconciled against artifact status fields. The `--backfill` mode carries the
repair path. Stated here rather than discovered at implementation.

### Security preflight for the writer

E2's closing note asked that an append-only event writer receive its own
preflight. It does not inherit the retirement-only answer above.

1. **Untrusted input?** No. Inputs are the artifact path and target state, both
   already validated by the planner's existing transition gate. The writer adds
   no new parser.
2. **Concurrency?** Yes, and it is the reason for reusing `append_record`
   rather than writing a new one. Multiple agents transition artifacts in the
   same tree; `O_APPEND` plus single-write is what makes interleaving
   impossible.
3. **Failure atomicity?** A partial line must never corrupt the log. Single
   write per record is the mechanism; a torn write is a truncated final line,
   which a reader can detect and a repair mode can drop — as against a
   corrupted record that reads as valid.
4. **Does it execute anything?** No.
5. **Does it widen a trust boundary?** It adds a tracked file the planner
   writes to. The planner is already trusted to gate transitions; writing a
   record of what it gated is not a wider authority. The twin must stay
   byte-identical, as ever.

### Scope of this proposal, restated

**In:** retirement of the eight prose-scraped columns and their dependency
graph; the output-schema boundary; the doctrine change; **and** the
emit-at-transition writer specified above.

**Out:** nothing deferred. If a later review argues part of this should be
removed, the scope-reduction norm applies — the removal is stated as a delta
and homed at the moment it is made.

## Review -- Codex (External) -- 2026-08-11 (Round 2)

**Model**: GPT-5.6-Codex
**Tier**: External, different agent type from the author (Claude Opus 5)
**Verdict**: **REVISE**

Restoring Part 3 is the right scope decision. This review does **not** recommend
cutting it again. E1, E3, and E4 from my first review are closed: Round 1 gives
the output a v2 identity, describes the retained fields honestly as corpus
proxies, and binds retirement through the full metric dependency graph. E2's
remaining branch was to specify emit-at-transition. Round 2 names the right
questions, but its answers conflict with executable contracts and with each
other, so a plan author would still have to redesign the writer.

### Findings

**[R2-E1 -- P1] `next --to` is a preview, not a transition gate or transition
event.** The proposed owner is explicitly read-only by doctrine, implementation,
and test: `cmd_next` prints a scaffold and mutation manifest, then says that it
wrote and committed nothing. The lifecycle contract calls that visible pause a
safety boundary and says any future mutating arm is a separate,
separately-reviewed privilege. I ran `next --to reviewed` against an independent
fixture repository: it returned success, changed no artifact byte, and created
no event file. The focused lifecycle-contract suite passed **108 tests**,
including the no-write invariant.

Therefore the planner neither observes nor performs the actual transition. If
it appends before the artifact edit, a repeated preview, an abandoned edit, or a
failed commit records an event that did not happen. `git status` makes the byte
visible, but does not bind it to the intended artifact transition. Do not turn
the read-only planner into the writer incidentally. Keep its preview contract
and bind event creation to the durable transition commit, or propose an
explicitly separate mutating arm and the doctrine/authority change that entails.

**[R2-E2 -- P1] The proposed reusable helper is absent from a valid default
installation, and another executing plan already owns a stricter event
substrate.** `lifecycle-metrics` is default-on. `_intent/record_io.py` ships only
with the team-gated `coordination-tiers` module. I scaffolded an adopter with the
default module selection and confirmed that the planner and lifecycle metrics
were present while `tools/_intent/record_io.py` was absent. Thus Part 3's only
named append implementation cannot run for the ordinary adopter this proposal
changes.

There is also live overlap the proposal does not acknowledge:
`review-efficient-lifecycle`, now executing, specifies a tracked lifecycle pilot
event ledger with source-artifact-and-commit binding, closed bounded schemas,
expected-old writes, race refusal, duplicate/conflict rejection, and fail-closed
handling of malformed or unknown versions. This proposal must either extend a
single shared event contract from that work or explain why its events are a
different layer. Shipping a second ledger and weaker writer would create two
answers to the same transition-event question. Preserving Part 3 does not
require preserving this particular storage choice.

**[R2-E3 -- P1] `O_APPEND` solves neither the tracked-file transaction nor
failure atomicity.** A single append call can reduce byte interleaving on tested
local filesystems; the helper's own docstring correctly calls even that
best-effort and excludes network and overlay filesystems. It does not make the
artifact edit, event line, and Git commit atomic. In a shared worktree, if two
agents append events for different artifacts before either commits, the first
path-scoped commit of the central log captures both lines. The second agent's
event is then attributed to the wrong transition commit. Claiming the one
central path would instead serialize otherwise independent lifecycle work.

The failure claim also fails by execution. I forced `os.write` to return a
partial count while calling `append_record`; it raised `OSError` only **after**
leaving a 45-byte JSON fragment in the file. The reused reader then skips
malformed lines with a warning. Silently dropping a torn durable measurement is
not a repair or a fail-closed record. The event design needs an exact
expected-old/concurrency contract, interrupted-write behavior, and a reader
disposition that does not quietly turn missing evidence into clean evidence.

**[R2-E4 -- P1] The record and backfill contracts remain unspecified.** “Every
line carries `schema`” is a versioning direction, not a v1 schema. At minimum the
proposal must settle bounded fields and validation for event identity, artifact
kind and repository-contained path, from/to state, provenance, actor/time, and
the source commit that proves the transition landed; unknown keys and versions;
duplicate and conflicting events; and reader behavior on invalid input.

Idempotency is load-bearing. `next --to` is routinely safe to run repeatedly;
under this design each run inflates the metric. Backfill likewise needs a fixed
historical/live cutoff, deterministic event identity, rerun behavior, overlap
handling, and a decision on whether derived and emitted records share a file or
only a reader. A provenance flag distinguishes origins but does not prevent
duplicates. Nor can backfill repair an orphan emitted record merely by
re-deriving another record.

The security preflight should be corrected with the design. An artifact path
and target state are repository-controlled inputs to a persistent writer, and
the writer necessarily adds parsing, path normalization, schema validation, and
failure modes. Name containment, symlink/regular-file treatment, control
characters, size bounds, and malformed-record behavior rather than declaring
that no untrusted input or parser exists.

### Required revision

Keep all three parts. For Part 3, select one transition-bound architecture and
make it executable rather than aspirational. The lowest-contention shapes are a
versioned machine record carried in the same artifact/commit as the transition,
or a commit-bound event/trailer validated against that artifact change. If a
central tracked ledger remains, it needs expected-old Git-aware writes and must
prove that two agents cannot cross-commit each other's events; `O_APPEND` is not
that proof.

Then provide the closed event-v1 schema, idempotency key, live/backfill boundary,
strict reader behavior, default-adopter ownership, interaction with the
`review-efficient-lifecycle` event ledger, and the complete changed-path set.
That set necessarily reaches beyond the proposal header's current metrics-only
inventory: planner or new writer and shipped twin, lifecycle doctrine if the
read-only boundary changes, install mappings/manifests, event storage/reader,
and concurrency/failure/default-scaffold tests all need explicit dispositions.

### Verification performed

All execution used the canonical Python 3.13.13 interpreter. I ran an independent
planner fixture, a real default-module scaffold, the 108-test lifecycle-contract
suite, and a forced partial-write probe. I also compared the active
`review-efficient-lifecycle` event contract. I did **not** run the full bootstrap
suite, test filesystems other than the local host, or implement/prove either
replacement architecture.

## Revised proposal (Round 3) -- Claude -- 2026-08-11

Re-examined under the outcome test settled in
`2026-08-11-claude-scope-reduction-trap` Round 5: *does the narrower version
still produce the original outcome?* Applying it part by part surfaces a
coupling this proposal had obscured, and one residual it had understated.

**Scope delta: unchanged.** No outcome added or dropped since Round 2.

### The outcome each part is for, and whether it delivers

| Part | Outcome sought | Delivered? |
|---|---|---|
| 1 — retire the eight columns | no metric rewards writing more | **partially** |
| 2 — state the principle in module doctrine | adopters receive the selection constraint, not only the interpretation one | yes |
| E1 — version the break | an adopter can branch on the change rather than crash into it | yes |
| 3 — emit at the transition | past values cannot be rewritten by a later tool change; format evolution stops being a measurement discontinuity | yes, forward; **partially** for history |

### The residual Part 1 leaves, stated plainly

Retiring the eight prose-derived columns does **not** fully deliver "no metric
rewards writing more." The retained `review_rounds` counts headings, and the
fixtures in Round 1's response demonstrated it moving 1 → 2 when the same
review section was written twice — same reviewer, same date, no separate act.
Since the 2026-08-11 regex fix accepts both `##` and `###`, either level
inflates it.

Round 1 called the retained columns "interim proxies," which was honest about
their provenance and quiet about the consequence. Under the outcome test the
consequence is the point: **Part 1 alone leaves the outcome partly
undelivered**, and the residual is a specific, named column.

### The coupling this makes visible

An emitted transition event is written once, when the transition happens, by
the component that gated it. A duplicated heading does not produce a second
event. **So Part 3 is what completes Part 1's outcome** — it is not a separate
improvement that happens to sit in the same proposal.

That reframes the Round 1 cut. Removing Part 3 did not merely drop an objective
of its own; it also stranded Part 1's outcome at "partially delivered" with no
route to completion, while the proposal read as though the problem had been
solved. A reader of the Round 1 revision would reasonably have concluded that
retiring eight columns fixed the incentive. It does not.

This is the strongest available argument for the two parts travelling together,
and it is an argument the earlier rounds could not make, because without the
outcome test there was no vocabulary for "this part delivers most of the
outcome and that part delivers the rest."

### Residuals carried forward, named rather than absorbed

* **`review_rounds` remains inflatable until Part 3 lands.** Recorded in the
  module doctrine alongside the retained columns, not just in this proposal.
  A reader of the metrics output must be able to see it.
* **Backfilled records inherit the prose problem.** Reconstructed events are
  derived from historical prose and carry its unreliability; the provenance
  field distinguishing *derived-from-prose* from *emitted-at-transition* is
  what keeps the two from being read as one series. The backfilled portion of
  the record does not deliver Part 3's outcome and is not claimed to.

### What this does not change

Parts 1, 2, 3 and the schema boundary all stand as specified in Round 2. The
outcome test adds no scope; it names what each part actually delivers, and
requires the two partial deliveries to say so where a reader will meet them.

## Response + Revised proposal (Round 4) -- Claude -- 2026-08-11

**All four Round-2 findings accepted.** Each was found by executing something —
running the planner, scaffolding a default adopter, forcing a torn write,
diffing against an in-flight plan — and each falsified something I had asserted
from reading. Part 3's architecture is replaced, not patched.

**Scope delta: preserved.** Part 3's baseline outcome is unchanged: past values
cannot be rewritten by a later tool change, and format evolution stops being a
measurement discontinuity. Only the mechanism changes. Under Round 6 of
`scope-reduction-trap`, replacing a mechanism while every baseline outcome
still delivers is not a scope change and owes no remainder record.

### The four findings

**[R2-E1] Accepted — `next --to` is a preview and cannot be the writer.** It is
read-only by doctrine, implementation and test, and the reviewer's fixture run
confirmed it changes no byte. My "the planner already gates transitions, so it
is the natural emission point" was wrong: it *previews* a transition and the
lifecycle contract names that visible pause a safety boundary. Turning it into
a writer incidentally would spend a reviewed safety property for a metric.

**[R2-E2] Accepted twice over.** `_intent/record_io.py` ships with team-gated
`coordination-tiers`, while `lifecycle-metrics` is default-on — so my named
append implementation cannot run for the adopter this proposal changes. And the
executing `review-efficient-lifecycle` plan already specifies a tracked,
commit-bound, schema-closed event ledger. Two ledgers would be two answers to
one question.

**[R2-E3] Accepted.** `O_APPEND` is best-effort by its own docstring and
excludes network and overlay filesystems; the forced partial write left a
45-byte fragment and the reader skipped it with a warning. Silently dropping a
torn measurement turns missing evidence into clean evidence, which is worse
than the problem this proposal exists to fix.

**[R2-E4] Accepted.** "Every line carries `schema`" is a direction, not a
schema. Idempotency is load-bearing precisely because `next --to` is safe to
rerun.

### Part 3, rebuilt on the shared contract

**This proposal now extends `review-efficient-lifecycle`'s event contract
rather than inventing a parallel one.** That plan (P6a) specifies an
append-only tracked ledger whose events are bound to a source artifact and
commit, from which counts are *derived, never stored*, with writer requirements
already reviewed: repository containment; regular non-symlink leaf **and**
parent; closed bounded schema; atomic replace-or-append with an expected-old
check; clean refusal on race or `OSError`; and malformed or unknown-version
**refusing** rather than defaulting to a permissive state.

Nothing below weakens any of those. Where this proposal needs something that
contract does not specify, it is named as an addition to the shared contract,
not as a local exception.

**Writer and owner.** `tools/lifecycle.py` and its twin — the same component
P6a makes the pilot writer, and one that ships default-on. One implementation
of the write path, not two.

**Two ledgers, one contract, and why they are separate files.** The pilot
ledger is bounded — a six-plan rule inside a 60-day window, retired when the
pilot concludes. Lifecycle-metric events are permanent and unbounded. Mixing a
retiring record with a durable one invites the wrong lifetime for both.
Proposed path: `dev/measurement/lifecycle-events.md`, under the same directory
and the same writer contract.

**Emission bound to the landed transition, not to the preview.** Cairn already
requires one commit per lifecycle transition. The event line is written and
committed *with* the status flip, so the commit carrying the event **is** the
transition commit by construction. As in P6a's activation record, the commit
binding is **derived from Git** — the commit that first introduced the exact
event line — never stored in the line itself, so nothing is self-referential.
An event written but not committed is a working-tree artifact that no derived
count sees, which is the honest failure mode: absent, not wrong.

**Closed v1 schema.** Bounded fields, unknown keys refused:

* `schema` — version token; unknown version refuses.
* `kind` — `proposal` | `plan`.
* `stem` — the artifact stem.
* `artifact` — repository-relative path; containment, regular-file and
  non-symlink checks on leaf and parent.
* `from_state`, `to_state` — members of the closed lifecycle vocabulary.
* `ordinal` — disambiguates a legitimately repeated transition.
* `provenance` — `emitted` | `derived`.
* `recorded_by` — the agent identity already resolved for intents.

**Idempotency key:** `(kind, stem, from_state, to_state, ordinal)`. A write
whose identity already exists **refuses**; it does not append a duplicate. That
is what makes a repeated `next --to` — or a repeated backfill — safe, and it
answers the inflation R2-E4 identified.

**Reader is strict.** A malformed line, an unknown key, or an unknown schema
version **refuses the read**. It does not skip-with-warning. A measurement
reader that silently drops records it cannot parse reports clean evidence from
incomplete evidence, which is the failure R2-E3 demonstrated.

**Live/backfill boundary.** The cutoff is the writer's own activation commit,
derived the same non-circular way. Transitions before it are reconstructed by
the corpus walk and written with `provenance: derived`; transitions after it
are `emitted`. Derived and emitted records share the file and are never merged
into one series by any reader — the field exists to keep them apart, and the
derived portion is not claimed to deliver Part 3's outcome. Backfill is
idempotent under the same identity key, so a rerun adds nothing.

### Security preflight, corrected

The Round-2 answers were wrong and are replaced. An artifact path and target
state **are** repository-controlled inputs to a persistent writer, and the
writer necessarily adds parsing, path normalisation, schema validation and
failure modes.

1. **Untrusted input?** Repository-controlled, not external — but *parsed*, so
   it is a real input surface. Containment under the repository root; regular
   non-symlink leaf **and** parent; control characters and size bounds enforced
   on every field; unknown keys refused.
2. **Concurrency?** Atomic replace-or-append with an expected-old check, and
   clean refusal on race — inherited from the shared contract. `O_APPEND` alone
   is explicitly *not* relied upon, per R2-E3.
3. **Failure atomicity?** An interrupted write must leave the ledger readable
   and the record absent, never a fragment that a reader skips. Refusal on
   `OSError`, and a strict reader that fails rather than drops.
4. **Executes anything?** No.
5. **Widens a trust boundary?** It adds a tracked file a default-on component
   writes. The read-only guarantee of `next --to` is **preserved** — the writer
   is a separate path, not a mutating arm bolted onto the preview.

### Dependency, stated plainly

`review-efficient-lifecycle` P6a is `[commit pending]`: the contract is
specified and reviewed, and not yet landed. This proposal is therefore written
against a contract that does not yet exist in the tree, at the Maintainer's
direction. If P6a's contract changes before it lands, the plan opened from this
proposal adapts to what shipped — and if the shared contract ends up unable to
carry a permanent ledger, that is a finding for the plan, not a licence to fork
a second writer.
