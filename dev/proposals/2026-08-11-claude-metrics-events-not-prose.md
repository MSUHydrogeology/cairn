# Measure structural events, not prose

**Author**: Claude (Strategy)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-11
**Status**: proposed
**Touches**: `templates/modules/default-on/lifecycle-metrics.md`;
`templates/modules/default-on/_lifecycle_metrics/` and its `tools/` twin;
`bootstrap/tests/test_lifecycle_metrics*.py`
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
