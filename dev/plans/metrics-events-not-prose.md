<!-- Forward-reference paths this plan creates; they materialize in Chunks 5 and 7. -->

# Plan: measure structural events, not prose

**Source proposal**: [`dev/proposals/archive/2026-08-11-claude-metrics-events-not-prose.md`](../proposals/archive/2026-08-11-claude-metrics-events-not-prose.md)
**Status**: awaiting-plan-review
**Plan review**: required(**Internal**) from round 3 onward — the Maintainer
converted the tier after two External rounds landed. See "The review tier, and
why it changed" below.
**Last update**: 2026-08-20
**Opened**: 2026-08-20

## The review tier, and why it changed

**Opened at `required(External)`, and two External rounds were held.** The
source proposal's own header declared it, with a reason that stands unaltered:
this changes the emitted schema of a **default-on** module, installed by every
adopter except the smallest, whose output those adopters may already be parsing.
That is a contract surface, and the External floor — a different agent type, or
a human — exists for exactly that.

Both rounds happened. Round 1 raised three blocking findings (an AST-attestation
command that could not run, an activation cutoff with no reader behind it, and
stale cross-references from a chunk move); round 2 closed all three and raised
one more (a ceremony's own procedure narrowed on efficiency grounds). All four
are answered in the operative cells above.

**Converted to Internal from round 3.** Authorized by the Maintainer, quoted
verbatim and visually isolated:

> "Please just handle the metrics internally from here."

**What that costs, stated rather than glossed.** Round 3 verifies that one
finding was answered; it is not a fresh read of an unexamined contract. The
design got its different-agent-type scrutiny — twice — and it changed the plan
substantially both times. What is given up is a third independent perspective on
a narrow question, which is a materially smaller loss than converting the tier
before any External round had run. Had this been asked at round 1, the honest
answer would have been different.

**This plan carries no `Inherited proposal basis:` field**, and the conversion
does not create one. Inheritance is a distinct mechanism that reallocates a plan
review on the strength of a proposal reviewer's readiness finding; this is a
Maintainer tier decision, which is a different authority. Pairing the two would
be a false claim about where the assurance came from.

## Source proposal

`2026-08-11-claude-metrics-events-not-prose` went through seven Response/Revised
rounds and five External reviews (two agent identities: Antigravity ACCEPT,
Codex REVISE ×4) before the Maintainer accepted Round 7 on 2026-08-12. The
accepted contract has three parts. **Part 1** retires eight prose-scraped
columns (`total_findings`, `findings_p1/p2/p3`, four `review_yield_*`) from
routine emission, and the machinery that produces them, because a metric
derived by parsing review prose rewards writing more of it — the cheapest way
to look thorough is to split one finding into three. **Part 2** states the
selection principle in the module's own doctrine, next to the Measurement
Compact, and describes the columns Part 1 keeps honestly rather than as
immune to the same defect. **Part 3** replaces prose-parsing for the retained
event-shaped fields (`review_rounds`, reviewer identity/tier, `response_models`,
the stage-timing columns) with a closed-schema HTML-comment block appended to
the transitioning artifact by the same edit that performs the act, read back by
a rename-aware Git history algorithm that refuses — rather than silently
degrades — on any block it cannot reconcile to exactly one lifecycle act. This
plan executes that decision; it does not re-litigate any of the seven rounds
that produced it.

**A note for the reviewer, up front.** The source proposal's own security
preflight went stale mid-deliberation, and no round after Round 5 re-answered
it against the architecture Round 7 actually specifies and the Decision
actually accepts — independently confirmed against the live proposal text.
This plan's own re-derivation, under "Author-accounting" below, is the first
answer against the real architecture; read it rather than the proposal's own
preflight sections.

## Proposed paths

Proposed paths:
- `tools/_lifecycle_metrics/events.py` — the event-v1 grammar (Chunk 4), the history-diff reader (Chunk 5), and reconciliation logic (Chunk 6); its `templates/` twin lands each same commit.
- `templates/modules/default-on/_lifecycle_metrics/events.py` — the gate-frozen twin of the above.
- `bootstrap/tests/test_lifecycle_metrics_events.py` — the new fixture file for the grammar/algorithm/reconciliation red and green cases (Chunks 4-7).

## Scope

**In, per the Decision:** all three parts, unabridged — retirement of the eight
columns and their full dependency graph (not just the CSV keys); the v2 schema
identity that makes the break machine-readable; the doctrine statement and the
honest re-description of the retained columns; the event-v1 grammar; the
rename-aware history-diff reader; fail-closed reconciliation on read; and
wiring every retained event-derived field to exactly one event kind. Nothing
here narrows any of Round 7's commitments — this is decomposition into
commits, not a second design pass.

**Out, by the Decision's own allowance — stated here, not silently restored.**
Historical continuity across the activation boundary is **dropped**: no
frozen historical snapshot is taken for this plan's own purposes, and no
prose-derived value is substituted for a pre-activation artifact's event-shaped
fields. `Scope delta: degraded`, already authorized —

> "Drop historical continuity" — Anthony Kendall (Maintainer), Decision, 2026-08-12.

Chunk 6 states the concrete emission of this rule (what a pre-activation row
looks like) precisely so the allowance is not quietly reinterpreted at
implementation as "keep computing the old way until enough history exists."

**A correction, and the Maintainer's disposition on it.** This section
previously stated "no `--backfill` mode ships" — that is false:
`--backfill-from YYYY-MM-DD` already ships (`tools/_lifecycle_metrics/cli.py`,
calling `snapshot.backfill`), and it is documented in the module doc every
adopter installs.

**Reading it settled the question.** `backfill()` walks `Goodnight:`-tagged
commits in a bounded window and calls `emit_snapshot` once per commit — but
`emit_snapshot` measures **the tree as it currently is**. It never checks out
the historical commit; it only *stamps* each row with that commit's date and
SHA. So a backfilled snapshot dated three weeks ago holds today's corpus,
measured today, wearing a past date. Worse, `corpus_commit` is documented as a
reproducibility contract — "`git checkout <corpus_commit> && …`" — and for
these rows it names a commit that would **not** reproduce the row. That is the
hazard the Decision's own rationale used to justify dropping historical
continuity: *"A frozen number known to be wrong is worse than no number,
because the caveat stays in the file while the number travels."* This one
travels with a date and a SHA attached, which makes it travel better.

**Contract expansion**: adopter-facing CLI surface — `--backfill-from` and
`snapshot.backfill` are removed, along with `backfill_max_days` and the
now-callerless `_list_goodnight_commits`. Authorized by the Maintainer, quoted
verbatim and visually isolated:

> "Let's go (C)"

The option that names, recorded because a bare letter will mean nothing later:
**(c) remove the flag**, chosen over (a) making it refuse and (b) stamping its
output with the v2 identity. The reason is not primarily that the Decision says
no backfill mode ships — it is that the mode misattributes measurements to
commits that did not produce them, which is a defect independent of this
proposal, and removal is the only option that stops shipping it. The work is
rows 1-10 through 1-16 in Chunk 1, which lands there because it shares four
files with the column retirement.

**A question this plan should answer and currently cannot.** After Chunk 6's
fail-closed reconciliation lands, backfill over pre-activation dates might have
refused on its own — those artifacts carry no event blocks, which is what makes
a read `INCOMPLETE`. That was not traced, and it does not change the
disposition: removal happens in Chunk 1, before Chunk 6 exists. It is recorded
so a reviewer does not assume the two interact.

**Out, because Round 5 explicitly removed it and no later round restored it —
flagged as a discrepancy from this task's own briefing, see "A correction to
this plan's own brief" below.** `tools/lifecycle.py` and its twin
`templates/skills/_lib/lifecycle.py` are **not touched by this plan.** They
belonged to the shared-ledger writer design that R3-E1 falsified and Round 5
abandoned outright ("No longer touched: `tools/lifecycle.py` and its twin... Both
belonged to the abandoned shared-ledger design" — Round 5, "Corrected
inventory"). The final architecture (Round 7) has no separate writer process at
all: the event block is written by the same edit that performs the act, and the
reader is the extractor. No chunk below touches `tools/lifecycle.py`.

**Out, unaffected:** `review-efficient-lifecycle`'s pilot-event ledger
(`dev/measurement/pilot-events.md`, `tools/lifecycle.py pilot-record` /
`pilot-report`). Round 5 explains why the two are separate files under one
writer-safety posture rather than one shared ledger: the pilot ledger is bounded
(retires at the end of its six-plan/60-day window) and lifecycle-metric events
are permanent, so mixing them gives the wrong lifetime to both. This plan does
not read, write, or extend that ledger.

### A correction to this plan's own brief

This plan was opened from a briefing that listed `templates/modules/default-on/_lifecycle_metrics/`
+ its `tools/` twin, **and** `tools/lifecycle.py` + its twin, as the Touches set
to carry forward. That listing matches the *proposal's original, never-revised
header* (`**Touches**:` line, top of the source proposal) — but the header is
stale. Round 5's "Corrected inventory" section explicitly supersedes it,
Round 6 adds `docs/glossary.md`, and neither Round 6 nor Round 7 (the operative
contract) touches `tools/lifecycle.py` again. Per this task's own instruction to
read Round 7 as the contract and treat earlier rounds as superseded history,
this plan follows the corrected inventory, not the stale header. Flagged
explicitly rather than silently resolved — see the report accompanying this
plan's opening commit.

### Documentation / doctrine surface

* `templates/modules/default-on/lifecycle-metrics.md` and its self-hosted
  installed copy `dev/modules/lifecycle-metrics.md` (identical to the shipped
  file except for `{{metrics_command}}` token substitution, confirmed by diff)
  — module doctrine: removes the "finding severities" capability claim (two
  locations in each file), adds the selection principle beside the Measurement
  Compact, reworks or bounds-marks the late-blocker section, and describes the
  retained columns as interim lifecycle proxies rather than inflation-immune
  (Chunk 2).
* `dev/agent_collaboration.md` carries the same "finding severities" phrase
  once, inside the `<!-- cairn:slot lifecycle-metrics -->` block — but
  **line-wrapped** across two lines ("finding" / "severities."), so a plain
  single-line `grep -n "finding severities"` never matches it there even
  though the phrase is present; Chunk 2's acceptance check must be
  whitespace-tolerant and multiline-capable. **This slot is hand-edited
  directly, not re-rendered through the scaffold's slot-merge path**:
  `bootstrap/_scaffold/slotmerge.py::resolve_slot_merge` produces a
  non-`None` merged text only for status `inserted`, which requires an
  *empty* slot body; Cairn's slot is filled, so re-running the merge after
  the module doc changes resolves to `conflict` and writes only a
  `.cairn-merge-pending` side-file, leaving the target byte-for-byte
  untouched (confirmed against the live source, as_of 2026-08-20).
  `templates/core/dev/agent_collaboration.md` does **not** carry the phrase —
  its slot ships deliberately **unfilled** ("An unfilled slot is a review
  finding," an adopter-facing placeholder), and preserving a filled slot
  verbatim on upgrade is the documented contract (`bootstrap/UPGRADE.md`:
  "Slots are adopter-owned"). Filling that slot would add scope to the
  install contract, a named high-risk surface; **this file is explicitly
  excluded from Chunk 2**.
* `docs/glossary.md` — sharpens the unconditional "never mine it for metrics"
  sentence under **Archive**, per R4-E3/Round 6's disposition, to distinguish a
  closed-schema block emitted *at* the transition from retrospective mining of
  prose it was never designed to carry (Chunk 2).
* `dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`,
  `dev/plans/_template.md`, `templates/core/dev/plans/_template.md` — the four
  activation-marker paths (Chunk 6, landing in the same commit as fail-closed
  reconciliation — see that chunk for why). **Not a byte-identical twin pair** — the
  self-hosted copies already diverge from the shipped copies today (confirmed
  by diff: the self-hosted files carry Cairn's own filled content where the
  shipped files carry adopter fill-in slots and merge-block placeholders). Each
  of the four independently needs to carry the literal `cairn-event-v1` token;
  Round 7 §4 is explicit that Cairn and an adopter "each derive their own cutoff
  from their own history" — there is no shared constant to keep in sync.
* `CHANGELOG.md > Unreleased > Changed` — the v1→v2 schema break and the new
  event-emission convention (Chunk 8).
* No file under `doctrine/` — this plan executes an already-accepted design; it
  proposes no new cross-project doctrine beyond what the module and glossary
  already own.

## Sequence

```
1. Retire the eight columns and their dependency graph        [commit pending]
2. Doctrine: the principle, the honest description, the glossary sharpen [commit pending]
3. Version the break: v2 schema identity                      [commit pending]
4. Event-v1 grammar, planner surfacing, engine registration    [commit pending]
5. The history-diff reader: identity, mutation detection, activation cutoff [commit pending]
6. Activation markers, fail-closed reconciliation, wiring the retained fields [commit pending]
7. Cross-cutting fixtures and the pre-existing-test audit     [commit pending]
8. CHANGELOG and the before/after corpus evidence                [commit pending]
9. MAINTAINER-GATED — differential-oracle gate re-anchor ceremony [not performed by the implementing agent]
```

Chunks 1-3 have no dependency on Chunks 4-6 and may land in either order
relative to them; they are sequenced first here because Part 1/2 were stable
since Round 1 while Part 3 went through four more architectures. Chunks 4→5→6
are strictly ordered (grammar before reader before reconciliation). Chunk 7
depends on 1-6 all being present to exercise cross-cutting behavior. Chunk 8 is
bookkeeping and can land last. Chunk 9 is not part of this plan's own commit
sequence — see "The re-anchor ceremony" below.

### Chunk 1 — Retire the eight columns and their dependency graph

Confirmed by reading the live source (`tools/_lifecycle_metrics/`, as_of
2026-08-20): `total_findings`/`findings_p1/p2/p3` are computed at
`extract.py`'s finding-bullet loop (using `_FINDING_BULLET_RE` /
`_BRACKET_INTERIOR_RE`, imported from `parse.py`, with **no other consumer** —
verified by grep); the four `review_yield_*` columns come from
`subsystems._review_yield_counts`, whose entire supporting chain
(`_DISPOSITION_BUCKETS`, `_DISPOSITION_BULLET_RE`, `_normalize_disposition_token`,
`_parse_disposition_tokens`) has **no consumer besides `_review_yield_counts`
itself** — also verified by grep, so the whole chain is dead code once the
call at `extract.py` is removed, not just the four dict keys. `snapshot.py`'s
`METRIC_CONTRACT_MAP` carries exactly three review-yield entries
(`proposal_review_yield_accept_count`, `proposal_review_yield_reject_count`,
`proposal_review_yield_defer_count`).

| # | File | Change |
|---|------|--------|
| 1-1 | `tools/_lifecycle_metrics/extract.py` | Remove the `total_findings`/`findings` computation block and its four keys from the row dict; remove the `_review_yield_counts` call and its four keys; remove the now-dead `_FINDING_BULLET_RE`/`_BRACKET_INTERIOR_RE` import if `parse.py`'s audit (1-3) confirms no other consumer. Remove the eight names from `PROPOSAL_COLUMNS`. |
| 1-2 | `tools/_lifecycle_metrics/subsystems.py` | Remove `_review_yield_counts`, `_DISPOSITION_BUCKETS`, `_DISPOSITION_BULLET_RE`, `_normalize_disposition_token`, `_parse_disposition_tokens` — the whole review-yield chain, confirmed to have no other consumer. |
| 1-3 | `tools/_lifecycle_metrics/parse.py` | Remove `_FINDING_BULLET_RE`, `_BRACKET_INTERIOR_RE` once 1-1 confirms they have no remaining consumer. |
| 1-4 | `tools/_lifecycle_metrics/snapshot.py` | Remove the three `proposal_review_yield_*` entries from `METRIC_CONTRACT_MAP`. |
| 1-5 | `templates/modules/default-on/_lifecycle_metrics/{extract,subsystems,parse,snapshot}.py` | Identical edits, same commit — gate-frozen twin of 1-1..1-4. |
| 1-6 | `tools/lifecycle_metrics.py`, `templates/modules/default-on/lifecycle_metrics.py` | No source edit expected (thin launcher re-exports whatever the engine defines) — confirm unchanged, same commit as the twin above regardless. |
| 1-7 | `bootstrap/tests/test_reference_scripts.py` | `TestLifecycleMetricsSchema.test_installed_lifecycle_metrics_runs_on_target` (as_of 2026-08-20, lines 277-295): remove the `total_findings`/`findings_p1` assertions. Leave the `review_rounds` assertion as-is here — Part 3 has not landed yet at this point in the sequence, so `review_rounds` is still the pre-Part-3 heading count and the assertion still holds; Chunk 7 revisits this same test once Part 3 changes what computes that field. |
| 1-8 | `bootstrap/tests/test_lifecycle_metrics_config.py` | New or extended case: `PROPOSAL_COLUMNS` has exactly 22 entries (30 minus the eight retired, `as_of 2026-08-20` — re-derive at implementation, do not carry this count forward) and none of the eight retired names appear; every remaining structural column from the pre-change list is still present, asserted by name so a future accidental drop of a *kept* column fails loudly. |
| 1-9 | `tools/_lifecycle_metrics/__init__.py`, `templates/modules/default-on/_lifecycle_metrics/__init__.py` (byte-identical twins, confirmed by diff, as_of 2026-08-20) | Update the module docstring, which documents the same headline capability claim and per-column reliability tiers this chunk retires: drop "finding severities" from the capability list (~line 17) and "review-yield" from the subsystems list (~line 18); drop the `total_findings` (**Good**) and `findings_p1/_p2/_p3` (**Best-effort**) reliability-tier bullets (~lines 67-69) for the four columns this chunk deletes. |

**Also in this chunk: remove `--backfill-from`.** It shares four of the files
above, so it lands in the same commit rather than reopening them.

| # | File | Change |
|---|------|--------|
| 1-10 | `tools/_lifecycle_metrics/cli.py` + twin | Remove the `--backfill-from` argument and its help, the `backfill` import, the dispatch branch, the date-parse error path, and `'backfill'` from the recognized `--snapshot-event` values. |
| 1-11 | `tools/_lifecycle_metrics/snapshot.py` + twin | Remove `backfill()` and its `_list_goodnight_commits` import. |
| 1-12 | `tools/_lifecycle_metrics/config.py` + twin | Remove `backfill_max_days` — the default, the constructor parameter, the attribute, and the `_safe_int` read. |
| 1-13 | `tools/_lifecycle_metrics/gitmeta.py` + twin | Remove `_list_goodnight_commits`, which 1-11 leaves with no caller (verified: `snapshot.py` is its only consumer, an import plus one call). |
| 1-14 | `tools/_lifecycle_metrics/__init__.py` + twin | Remove the package-docstring mention of the backfill mode. Same rows as 1-9; do both edits together. |
| 1-15 | `templates/modules/default-on/lifecycle-metrics.md` and `dev/modules/lifecycle-metrics.md` | Remove the `--backfill-from` mention. Both copies — the second is Cairn's installed copy of the first and differs only by token substitution. |
| 1-16 | `bootstrap/tests/test_lifecycle_metrics_config.py` | Remove the `cfg.backfill_max_days == 14` assertion. **This is the only test in the tree that exercises this mode** — see the false-positive note below. |

**A grep for "backfill" returns five other files, and none of them is this
mode.** `test_lockfile_provenance.py`, `test_upgrade_side_door_parity.py` and
the two `gate_manifest.json` entries that name them are all about **lockfile
provenance backfill** — a different mechanism that happens to share the word.
Removing them would break unrelated tests. Read the surrounding code, not the
match: this is the instrument-confirmation rule
(`AGENTS.md` > *Verifying claims*) applied to a name collision rather than to
an absence.

**One thing this removal does not do.** Snapshots an adopter already emitted
carry `snapshot_event=backfill` in their rows. Removing the producer does not
invalidate those files, so the reader must keep tolerating the value on input
even though nothing can write it again. Deleting the value from the *reader's*
accepted set would turn an adopter's existing archive unreadable, which is a
larger break than the one authorized here.

**Acceptance for this chunk**: a fresh extractor run over a fixture proposal
with review findings emits no `total_findings`/`findings_p*`/`review_yield_*`
keys in either CSV or `--format md` output, while every retained column is
present and unchanged in value from before this chunk. Separately, `python
tools/lifecycle_metrics.py --backfill-from 2026-01-01` exits non-zero with an
unrecognized-argument error rather than running; `--help` does not mention it;
and an existing snapshot file containing `snapshot_event=backfill` still reads
without error.

### Chunk 2 — Doctrine: the principle, the honest description, the glossary sharpen

| # | File | Change |
|---|------|--------|
| 2-1 | `templates/modules/default-on/lifecycle-metrics.md`, `dev/modules/lifecycle-metrics.md` (identical edits, same commit — Cairn's own installed copy of the module doc, differing only by `{{metrics_command}}` token substitution) | Remove "finding severities" from the opening capability paragraph and from "Reference implementation" (two locations in each file, as_of 2026-08-20). Add the selection principle — *measure structural events as they occur; a metric that rewards writing more is a defect to remove, not a signal to tune* — as a framing statement beside the five-commitment Measurement Compact. Rework "Late-blocker reduction" so its bundle rests on structural signals, or mark it explicitly as a bounded study distinct from standing instrumentation (the proposal leaves this choice open; record which one this chunk takes and why). Describe the retained columns as interim lifecycle proxies, materially harder to inflate than a finding count but not immune (Round 1's withdrawn "cannot be inflated" claim stays withdrawn) — until Chunk 6 replaces them with genuine events, at which point this sentence is revisited so it does not overclaim in the other direction. |
| 2-2 | `dev/agent_collaboration.md` | Hand-edit the `<!-- cairn:slot lifecycle-metrics -->` block's body directly to remove "finding severities" (present once, line-wrapped across two lines — a plain single-line grep will not find it; verify with a whitespace-tolerant, multiline-capable check, e.g. `python3 -c "import re,pathlib,sys; sys.exit(0 if not re.search(r'finding\s+severities', pathlib.Path('dev/agent_collaboration.md').read_text()) else 1)"`). **Not** via the scaffold's slot-merge path: `bootstrap/_scaffold/slotmerge.py::resolve_slot_merge` writes a target only when its slot is empty (status `inserted`); Cairn's slot is filled, so re-running the merge resolves to `conflict` and leaves the target untouched, writing a `.cairn-merge-pending` side-file instead (confirmed against the live source, as_of 2026-08-20). `templates/core/dev/agent_collaboration.md` is **excluded** from this row: its slot ships deliberately unfilled as an adopter-facing placeholder, and filling it is out of this plan's scope. |
| 2-3 | `docs/glossary.md` | Sharpen the **Archive** entry's "never mine it for metrics" sentence (line 37, as_of 2026-08-20) to distinguish a closed-schema `cairn-event-v1` block emitted *at* the transition, in the same edit, from retrospective parsing of prose the artifact was never designed to carry. The existing sentence stays the default rule; this adds the narrow, named exception rather than replacing the rule wholesale. |

**Acceptance for this chunk**: a whitespace-tolerant, multiline-capable check —
not a plain single-line `grep -n "finding severities"`, which false-passes
against `dev/agent_collaboration.md` today because the phrase line-wraps
there — e.g. `python3 -c "import re,sys; paths=['templates/modules/default-on/lifecycle-metrics.md','dev/modules/lifecycle-metrics.md','dev/agent_collaboration.md']; hits=[p for p in paths if re.search(r'finding\s+severities', open(p).read())]; sys.exit(1 if hits else 0)"`
— finds no remaining occurrence in any of the three hand-edited files.
`templates/core/dev/agent_collaboration.md` is out of scope for this chunk
(its slot ships unfilled; see 2-2) and is not part of this criterion.
`python scripts/check_cairn.py` passes (link/anchor/claim-path integrity
across the touched docs); the glossary sentence names the exception without
weakening the general rule for anything that is not a `cairn-event-v1` block.

### Chunk 3 — Version the break: v2 schema identity

Depends on Chunk 1 (the eight columns are already gone from `PROPOSAL_COLUMNS`
by the time this chunk assigns the new identity).

| # | File | Change |
|---|------|--------|
| 3-1 | `tools/_lifecycle_metrics/snapshot.py` | Add a schema-version field to `output_manifest()`'s entries and to the persisted snapshot's own header/first row, distinguishing v2 (post-retirement) from v1 (pre-retirement, byte-preserved). Document the eight v1→v2 removals inline where the manifest already documents column lists. |
| 3-2 | `tools/_lifecycle_metrics/cli.py` | `--manifest` output (`format_manifest_md`) surfaces the version identity; no dual-emission path for the retired columns under any flag. |
| 3-3 | Twins under `templates/modules/default-on/_lifecycle_metrics/` | Identical edits, same commit. |
| 3-4 | `bootstrap/tests/test_lifecycle_metrics_config.py` or `test_reference_scripts.py` | A pre-existing (fixture-persisted) v1 snapshot's bytes are unchanged after this chunk lands; a freshly emitted snapshot carries the v2 identity and omits the eight columns; `--manifest` output names the version. |

**Acceptance for this chunk**: an adopter's pre-retirement snapshot file, present
in a fixture tree before this chunk's code runs, is byte-identical after it
runs (the tool never rewrites persisted output — true independent of this
chunk's own code, since `snapshot.py`'s `_next_snapshot_index`/`emit_snapshot`
already only ever add a new, freshly-indexed file and never prune or
overwrite; that pre-existing behavior is not what this chunk exists to add);
a fresh run against the same tree produces a new, v2-identified snapshot
alongside it, never merged with or overwriting the v1 one; and — the property
this chunk actually exists to establish — **a consumer reading the two files
side by side can tell them apart unambiguously from the version field alone**:
the v1 file carries no schema-version marker (or an explicit v1 one, if this
chunk back-labels the old shape — the implementing chunk records which), the
v2 file carries the new one, and no third, ambiguous state is representable.

### Chunk 4 — Event-v1 grammar, planner surfacing, engine registration

Depends on nothing in Chunks 1-3. Independent of them; sequenced fourth because
it is the first Part-3 chunk and Chunks 5-6 depend on it.

The literal grammar, reproduced from Round 7 (not re-derived — this chunk pins
what Round 7 specified, it does not choose it):

```markdown
<!-- cairn-event-v1
kind: transition
from_state: reviewed
to_state: revised
-->
```
```markdown
<!-- cairn-event-v1
kind: review-pass
tier: External
reviewer: <reviewer name as written in the section heading>
-->
```
```markdown
<!-- cairn-event-v1
kind: response
model: <model identity as written in the Response's **Model** field>
-->
```

Closed key table (Round 7, reproduced verbatim as the binding contract for this
chunk):

| key | kinds | required | bounds |
|---|---|---|---|
| `kind` | all | yes | exactly one of `transition` / `review-pass` / `response` |
| `from_state`, `to_state` | `transition` | yes | a declared lifecycle status for that artifact type |
| `tier` | `review-pass` | yes | `Internal` / `External` / `Security` / `Code` |
| `reviewer` | `review-pass` | yes | ≤120 chars, single line |
| `model` | `response` | yes | ≤120 chars, single line |
| `recorded_by` | all | no | ≤120 chars; informational only — barred from authority, identity and idempotency |

Unknown key, unknown `kind`, unknown version token, missing required key, or a
value outside its bounds **refuses**, never ignores, never defaults. The
version token is the literal `cairn-event-v1`.

| # | File | Change |
|---|------|--------|
| 4-1 | `tools/_lifecycle_metrics/events.py` (new) | Grammar parser: recognizes the `cairn-event-v1` fence, validates the closed key table above, returns a typed block or a refusal reason. No history walking yet (that is Chunk 5) — this chunk is pure block-level validation. |
| 4-2 | `templates/modules/default-on/_lifecycle_metrics/events.py` (new) | Gate-frozen twin of 4-1, same commit. |
| 4-3 | `tools/lifecycle_planner.py`, twin `templates/skills/_lib/lifecycle_planner.py` | `next --to <state>`'s preview/mutation-manifest output additionally shows the literal event block the transitioning edit is expected to carry — scaffold-only, informational, not written to disk, not gating. The command's read-only contract is unchanged; a regression test confirms it still writes nothing (see 4-5). Not gate-frozen (outside `templates/modules/**`), but still a same-commit twin pair. |
| 4-4 | `bootstrap/tests/test_lifecycle_metrics_events.py` (new) | Grammar red/green fixtures: unknown key refuses; unknown `kind` refuses; unknown version token refuses; missing required key per kind refuses; a `reviewer`/`model` value over 120 chars refuses; the three worked examples above each parse cleanly. |
| 4-5 | `bootstrap/tests/test_lifecycle_contract.py` | Re-run (not necessarily re-write) the existing read-only regression — `test_every_subcommand_is_read_only` or its equivalent, as_of 2026-08-20 line 172 — against the extended preview output, confirming the new block-preview text changes stdout only, no byte written, no git operation performed. |
| 4-6 | `bootstrap/_scaffold/config.py` | Register the engine file Chunk 4 (4-1/4-2) creates: add `InstallSpec("default-on/_lifecycle_metrics/events.py", "tools/_lifecycle_metrics/events.py", verbatim=True)` to the `"lifecycle-metrics"` entry in `_MODULE_MAPPINGS`, alongside the nine existing `_lifecycle_metrics/` rows (confirmed at ~lines 739-766, as_of 2026-08-20); update the neighboring comment's "the nine package files install verbatim" to "the ten package files install verbatim". Without this row `scaffold.py` never installs `events.py` and an adopter's `extract.py` import of it resolves to nothing on disk. Maintainer direction: these two engine files are to be included, not treated as an open scope question. |
| 4-7 | `bootstrap/tests/test_security_lint.py` | `test_templates_py_count_is_pinned` (line 376, as_of 2026-08-20) pins `len(on_disk) == 52` over `templates/**/*.py`. Update it to the post-registration count (52 + 1, as_of 2026-08-20 — re-derive at implementation from the live tree, do not carry a frozen number forward). Also confirm `test_every_templates_py_on_disk_is_release_scanned` in the same file passes once this chunk's own registration (4-6) lands: that check's oracle is the on-disk file set, independent of the manifest-derived count pin, and fails closed on any shipped `.py` present on disk but not release-scanned. |
| 4-8 | `bootstrap/tests/test_notice_install.py` | `test_manifest_has_the_expected_py_source_count` (line 74, as_of 2026-08-20) pins `len(sources) == 56` over manifest `.py` sources. Update it to the post-registration count (56 + 1, as_of 2026-08-20 — re-derive at implementation, do not carry a frozen number forward). |
| 4-9 | AST attestation baseline, via `bootstrap/tests/_ast_attest.py`'s `update-symbol` CLI path (per `bootstrap/AST_BASELINE_RUNBOOK.md`) | Row 4-6 changes `_MODULE_MAPPINGS`'s `Assign` node in `bootstrap/_scaffold/config.py`, a symbol the AST attestation baseline (`bootstrap/tests/fixtures/scaffold_ast_baseline.json`, enforced by `bootstrap/tests/test_ast_attest.py`) digests. `_MODULE_MAPPINGS` is one of the four symbols in `_ast_attest._UPDATE_ALLOWLIST` — unlike the unrelated, already-owed docstring-drift re-anchor named below under "Sequence revision" — so this single-symbol repair is self-serviceable by the implementing agent, in the same commit, following `bootstrap/AST_BASELINE_RUNBOOK.md`'s four steps in order (the CLI has no shorthand form; `update-symbol --help` confirms it requires `--baseline` and `--expect-old`, and accepts `--known-new` and `--dry-run`): **(1) diagnose** — run the runbook's `_merge_current`/`_classify` snippet against the live `bootstrap/_scaffold/*.py` set at this commit, confirm `_MODULE_MAPPINGS` is the *only* CHANGED symbol with MISSING and DUPLICATE both 0, and trace any logic-bearing NEW symbol to a landed, reviewed commit; **(2) known-new** — check the diagnosis against `bootstrap/tests/fixtures/scaffold_ast_known_new.json` (never a reimplementation of `_merge_current`/`_classify`), treating any DROPPED or REKEYED key as a review item traced to its own commit before proceeding; **(3) dry-run** — `python bootstrap/tests/_ast_attest.py update-symbol _MODULE_MAPPINGS --baseline bootstrap/tests/fixtures/scaffold_ast_baseline.json --expect-old <current live digest, re-derived at this commit, never copied from this plan> --known-new bootstrap/tests/fixtures/scaffold_ast_known_new.json --dry-run bootstrap/_scaffold/*.py`, which refuses on a stale `--expect-old`, an allowlist miss, more than one CHANGED symbol, or an undeclared NEW symbol — each refusal is the guard working, not a bug to route around; **(4) apply, verify, commit** — drop `--dry-run`, then `python bootstrap/tests/_ast_attest.py verify bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py`, confirming the `AST attestation OK — N baselined symbol(s) accounted for, unchanged.` tail with **N unchanged** from before this row (a surgical rewrite, not a re-pin), and commit `bootstrap/tests/fixtures/scaffold_ast_baseline.json` plus `bootstrap/tests/fixtures/scaffold_ast_known_new.json` together, explicit paths, in this same chunk commit. |

**Acceptance for this chunk**: every fixture in 4-4 passes; `next --to` remains
provably read-only under the existing contract test.

**And, for the registration rows (4-6 through 4-9): this chunk's own commit is
green.** Two runs, both *at this commit*, not at a later one.

**The AST runbook's own post-apply command, in full.** Mutating the attestation
baseline is a trust-root ceremony, and `bootstrap/AST_BASELINE_RUNBOOK.md`'s
Step 4 prescribes — not recommends — two commands after the apply:

```
python bootstrap/tests/_ast_attest.py verify \
  bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest bootstrap/tests -q
```

Both run here and both outcomes are recorded. An earlier revision of this plan
substituted a focused three-file run, reasoning that this plan's Boundary B
already owns one full run and repeating it per chunk is waste. That reasoning
is sound about *cost* and wrong about *what is being claimed*: Boundary B runs
later, so it cannot establish that the tree was green **at the moment a trust
artifact was re-anchored**, and re-anchoring against a tree whose state nobody
checked bakes an unverified state into the attestation. A plan does not get to
narrow a ceremony's own procedure on efficiency grounds; departing from the
runbook takes a recorded Maintainer authorization, and this plan has none.

**A forward hazard for whoever runs this.** That second command is a bare
`python -m pytest bootstrap/tests`, and the sibling plan
`dev/plans/full-suite-interception.md` installs a guard that refuses exactly
that invocation unless `CAIRN_FULL_SUITE=1` is set. If the guard lands before
this chunk runs, the runbook step **exits 4 and runs nothing** — a refusal that
looks like a failure in the middle of a Maintainer-run trust ceremony. That
sibling plan owes an update to the runbook's command; until it lands, prefix
this command with the override if the guard is present in `conftest.py` at the
commit you are on. A run that comes back exit 4 with a refusal message has been
refused, not passed.

**The registration rows' own focused check**, in addition to the above:
`python -m pytest bootstrap/tests/test_security_lint.py
bootstrap/tests/test_notice_install.py bootstrap/tests/test_ast_attest.py`
passes — both count pins moved with the
file, the newly-shipped `events.py` is a release-scan target rather than an
unscanned shipped `.py`, and the AST baseline is re-anchored rather than merely
diagnosed. Row 4-9's own record at this commit names both halves of that
repair: the dry-run's refusal-free outcome (step 3) and the applied `verify`
tail confirming the baselined-symbol count is unchanged (step 4) — recording
only the dry-run, or only that the pins were updated, does not satisfy this
criterion. The criterion is stated as "green at this commit" rather than "the
pins were updated", because a pin updated to the wrong number, or updated in a
later commit, both satisfy the second phrasing and neither satisfies the
first. Derive the two count numbers, and the AST digest, by running the
tests/tool at implementation time, not by carrying forward any figure recorded
in this plan.

### Chunk 5 — The history-diff reader: identity, mutation detection, activation cutoff

Depends on Chunk 4 (the grammar it walks history to find).

The algorithm, reproduced from Round 7 §2-§4 as the binding contract:

1. Walk the artifact's rename-aware history, **oldest first**.
2. At each commit, parse the block sequence at that commit and at its parent;
   **the parent sequence must be an exact prefix of the child's** — any
   reordering, edit, or deletion of an existing block is a mutation and
   refuses.
3. Attribute only the added suffix to that commit.
4. Require the matching lifecycle act in the same diff (a `transition` block
   needs the `**Status**` change; a `review-pass` block needs the added review
   section; a `response` block needs the added Response section).
5. Refuse on ambiguous multi-parent attribution — a merge commit is never an
   introducing commit.

**Identity is `(introducing full commit SHA, added-block index)`**, both
derived by the algorithm above and never stored. Neither term names a path, so
the archive `git mv` cannot discontinue a series.

**Activation** is derived per marker path independently: the commit that first
adds the literal `cairn-event-v1` marker to the applicable *installed*
template in that tree (`dev/proposals/_template.md` for proposal-hosted
events, `dev/plans/_template.md` for plan-hosted events). Missing, divergent
(the pair disagrees), or multiply-introduced (removed and re-added) markers
refuse.

| # | File | Change |
|---|------|--------|
| 5-1 | `tools/_lifecycle_metrics/events.py` | History-diff walk (rename-aware, oldest-first), the parent-prefix mutation check, added-suffix attribution, matching-act requirement, multi-parent refusal, `(commit, index)` identity derivation, per-marker activation cutoff derivation. Reuses `gitmeta.py`'s existing git-subprocess pattern (`_git_log_for_path`, `--follow`) rather than a second implementation where that pattern already covers the need. |
| 5-2 | `templates/modules/default-on/_lifecycle_metrics/events.py` | Twin of 5-1, same commit. |
| 5-3 | `bootstrap/tests/test_lifecycle_metrics_events.py` | Fixtures built against a real scratch git repository (reusing the `_git` helper pattern already present in `bootstrap/tests/test_lifecycle_contract.py`, as_of 2026-08-20 line ~70, rather than inventing a second one): a mutated (edited/reordered/deleted) existing block refuses; a merge commit introducing a block refuses; identity is stable before and after a `git mv` to `archive/`; missing, divergent, and multiply-introduced markers each refuse; a clean linear history with two distinct commits each adding one block resolves two distinct, stable identities. |

**Acceptance for this chunk**: every fixture in 5-3 passes against a real git
repository (not a mocked history), including the archive-rename identity
fixture, which is the concrete correctness case R5-E1 found broken in the
prior `(artifact path, block position)` identity scheme.

### Chunk 6 — Activation markers, fail-closed reconciliation, wiring the retained fields

Depends on Chunk 5. This chunk also carries the two rows that add the literal
`cairn-event-v1` marker to the four template paths (6-1/6-2), moved here
rather than landing alongside the grammar in Chunk 4. The marker's introducing
commit is itself the activation cutoff — from that commit on, every lifecycle
act in the applicable tree is subject to reconciliation — so landing it before
a reader exists to do that reconciliation would open a window with an
obligation and nothing to discharge it. Closing that window without deferring
the marker would instead mean requiring and auditing an event block for every
post-cutoff act while Chunks 4-6 land, which is not this plan's to impose: it
would bind whoever commits a lifecycle artifact in this tree during that
window, including in a concurrent session with no reason to know a plan's own
chunk boundaries changed what an event-worthy edit requires, enforced only by
template guidance nobody engaged in that session has read. Landing the marker
and the reader in the same commit is the option that depends on no one else's
session. This chunk is where Part 3 actually replaces prose-parsing for the
fields it claims, and where the `Scope delta: degraded` allowance gets its
concrete, checkable shape.

**The taxonomy (Round 6, reproduced as the binding contract):**

| Event kind | Emitted alongside | Retained fields it supplies |
|---|---|---|
| `transition` | the `**Status**` flip | transition dates; `days_*`, `hours_*`, `stage_timestamp_reliability`; `revised` |
| `review-pass` | each `## Review` / `## Plan review` / `## Code review` section | `review_rounds`, declared tier, `cross_agent_type_review`, reviewer identity |
| `response` | each `## Response` section | `response_models` |

**Fail-closed measurement on read.** The extractor is the canonical reader. It
exits nonzero `INCOMPLETE` when a post-activation event-bearing act has no
matching block, when a block has no matching act in its introducing commit, or
when reconciliation cannot be performed at all — including when Git itself is
unavailable for a post-activation artifact. This last case is a genuine
behavior change from today's tool, not explicit in the proposal text, and is
named plainly here rather than discovered at implementation: **the current
extractor runs without git** (`gitmeta.py`'s docstring: "Returns an empty list
when git is not available... a deliberately quiet failure mode"), degrading
silently to header-date-only reliability. Once an artifact's activation marker
exists and the artifact carries a status past that cutoff, this chunk makes
"no git available" a **refusal of that artifact's row**, not a quiet downgrade
— because "reconciliation cannot be performed at all" is exactly what
"unavailable Git" is. Chunk 7 audits every existing test that currently runs
this tool without a git-initialized scratch tree, because this is where their
assumptions break.

**The dropped-historical-continuity allowance, made concrete.** For an artifact
whose relevant act (transition / review-pass / response) predates that
artifact's own activation cutoff, the corresponding event-derived field is
emitted **empty** — not computed from the old prose-parsing path, not backfilled,
not marked "derived/unreliable" (both of those were the rejected option (b)).
Empty is the correct value per the Decision, not a placeholder for a future
backfill this plan does not build. Post-cutoff acts on the same artifact are
reconciled and refuse-on-mismatch exactly as above; an artifact can therefore
carry an empty `review_rounds` for its pre-cutoff review passes and a
populated one for later passes on the same document, and the reader must not
conflate the two into one silently-partial number.

| # | File | Change |
|---|------|--------|
| 6-1 | `dev/proposals/_template.md`, `dev/plans/_template.md` | Add the literal `cairn-event-v1` marker — worked into the templates' own guidance for how an agent appends an event block at a transition, review pass, or response, so the marker is simultaneously the activation cutoff and the instruction a reader needs to act on it. |
| 6-2 | `templates/core/dev/proposals/_template.md`, `templates/core/dev/plans/_template.md` | The shipped equivalent. Independently must carry the literal marker; not required to be byte-identical to 6-1 (see Scope's "Documentation / doctrine surface" note on why these four paths are not a twin pair in the byte-identical sense). |
| 6-3 | `tools/_lifecycle_metrics/events.py` | Reconciliation: per-artifact, per-kind matching of acts to blocks; `INCOMPLETE` disposition (nonzero exit, explicit reason) on any unmatched act, unmatched block, or unresolvable history (including unavailable Git for a post-activation artifact). |
| 6-4 | `tools/_lifecycle_metrics/extract.py` | Post-activation: `review_rounds`, reviewer identity/tier, `cross_agent_type_review`, `response_models` sourced from reconciled `review-pass`/`response` blocks, not from heading counts or `**Model**:` regex scraping. Pre-activation acts on the same artifact: the corresponding field is empty per the rule above. Transition dates / `days_*` / `hours_*` / `stage_timestamp_reliability` / `revised` sourced from reconciled `transition` blocks post-cutoff; unchanged (still header/git-timestamp-derived, still quiet-downgrade) pre-cutoff, since that is the existing degradation this chunk does not touch for the historical portion. |
| 6-5 | Twins under `templates/modules/default-on/_lifecycle_metrics/` | Same commit as 6-3/6-4. |
| 6-6 | `bootstrap/tests/test_lifecycle_metrics_events.py` | Mandatory red fixtures (Round 6 / R4-E2): a status-only commit with no block → `INCOMPLETE`; a review-only commit with no block → `INCOMPLETE`. Mandatory taxonomy fixture (Round 6 / R4-E1): two review commits with no intervening status change produce **two** review-pass events and `review_rounds == 2`. Pre/post-activation split fixture: one artifact with a review pass before its activation cutoff and one after; the row shows an empty value attributable to the pre-cutoff pass and a populated, reconciled value for the post-cutoff one. |
| 6-7 | `tools/_lifecycle_metrics/__init__.py`, `templates/modules/default-on/_lifecycle_metrics/__init__.py` | Update the "Robust across VCS settings" paragraph (~lines 74-82, as_of 2026-08-20): it currently documents unconditional quiet degradation to `Best-effort` reliability when git is unavailable ("a deliberately quiet failure mode"). This chunk makes that a refusal (`INCOMPLETE`) for a post-activation artifact instead of a quiet downgrade; the docstring must describe the new post-activation behavior, not continue documenting only the contract this chunk reverses. |

**Acceptance for this chunk**: the four template paths (6-1/6-2) each
independently carry the literal string `cairn-event-v1` **worked into the
templates' own instructional guidance** for how an agent appends an event
block at a transition, review pass, or response — not merely present as a bare
token or inside a fenced example, which would satisfy a literal string match
while leaving an agent no usable instruction; every fixture in 6-6 passes; a
report run against a fixture tree containing a deliberately unreconciled act
exits nonzero and names which artifact/commit/kind failed to reconcile, never
a shorter clean series; the `__init__.py` docstring (6-7) no longer documents
unconditional quiet git-absent degradation as the only behavior. Because this
chunk's own commit is what first introduces the marker, it lands in the same
commit as the reader and reconciliation logic that can act on it — no chunk
boundary leaves the marker present with no reader behind it.

**And, the property this chunk exists to make checkable**: run the real
extractor against Cairn's own `dev/proposals/` and `dev/plans/` corpus at this
commit; it exits successfully (never `INCOMPLETE`) and accounts for every act
in that corpus recorded after this commit's own activation cutoff — not merely
that the emitted column set can be diffed. Re-run and recorded again at Chunk
8's evidence step (8-6), since further real acts may land in the corpus
between this commit and that one.

### Chunk 7 — Cross-cutting fixtures and the pre-existing-test audit

Depends on Chunks 1-6 all being present.

| # | File | Change |
|---|------|--------|
| 7-1 | `bootstrap/tests/test_lifecycle_metrics_events.py` | Confirms cross-commit contamination is structurally unrepresentable (the R3-E1 property, re-expressed for the artifact-local design per Round 5 §2): two artifacts transitioned concurrently, one commit path-scoped to the first artifact only, and the assertion that the second artifact's block does not and cannot appear in that commit — because there is no shared file for it to appear in. This is a confirmation test of a structural property, not a vulnerability regression test (there is no longer a vulnerable mechanism to regress); it passes even with `events.py` deleted, since the property is one of git and path-scoped commits, not of the reader's own logic. Writing it is still required (Round 5); it does not itself enforce the property. |
| 7-2 | `bootstrap/tests/test_lifecycle_metrics_events.py` | `recorded_by` fixture: a block carrying a forged or duplicated `recorded_by` value changes no identity, no reconciliation outcome, and no refusal disposition — confirming it stays informational-only per Round 7's explicit bar on it participating in authority or idempotency. |
| 7-3 | `bootstrap/tests/test_reference_scripts.py` | `test_installed_lifecycle_metrics_runs_on_target` (as_of 2026-08-20, the same test Chunk 1 already touched; distinct from `TestVcsRobustness.test_no_git_target_degrades`, addressed separately at 7-5): once Chunk 6 lands, this fixture's `tmp_path` has no `.git` at all. Reusing the git-init pattern already present in this same file (as_of 2026-08-20, around line 469) is one option; asserting the new `INCOMPLETE`-refusal path directly, once the fixture proposal is activation-eligible, is the other. This chunk decides which and updates the test so it keeps exercising what it is meant to exercise, rather than accidentally exercising the new refusal path by omission. |
| 7-4 | `bootstrap/tests/test_lifecycle_contract.py` | Confirm the corpus-soundness suite (`test_the_live_corpus_is_sound_under_the_p1_contract` and neighbors) still passes against Cairn's own live `dev/proposals/` and `dev/plans/` corpus once the four template paths carry the activation marker — the live corpus itself carries no event blocks yet (this plan does not backfill), so this is a check that adding the marker to the templates does not itself perturb anything the corpus-soundness suite reads. This file is also touched by two other proposals opening today (both editing `bootstrap/tests/conftest.py`); this plan does not touch `conftest.py` and has no other point of contact with that concurrent work. |
| 7-5 | `bootstrap/tests/test_reference_scripts.py` | `TestVcsRobustness.test_no_git_target_degrades` (as_of 2026-08-20, lines 445-457) is the test that actually encodes the git-absent quiet-degradation contract Chunk 6 reverses: its docstring ("degrades to Best-effort rather than raising") and its assertion (`stage_timestamp_reliability == "Best-effort"`) describe exactly the behavior that no longer holds for a post-activation artifact. Update it: for a fixture proposal past its activation cutoff with no `.git`, assert the new `INCOMPLETE` refusal instead of the `Best-effort` degrade; for a fixture proposal that predates activation (or an installation with no activation marker at all), the existing quiet-degrade behavior is unchanged, and the test should say so explicitly rather than leave the pre-activation case implicit. |

**Acceptance for this chunk**: 7-1, 7-2, 7-3, and 7-5 pass as new/updated
fixtures; 7-4 is a confirming (not new) pass against the live corpus.

### Chunk 8 — CHANGELOG and the before/after corpus evidence

| # | File | Change |
|---|------|--------|
| 8-1 | `CHANGELOG.md` | Under `## Unreleased`, open a new `### Changed` subsection — the section currently has only `### Changed — Git-native security foundations` and `### Added` (as_of 2026-08-20; there is no generic `### Changed` to file this under) — and add one line naming the v1→v2 lifecycle-metrics schema break (eight columns retired) and the new event-emission convention for adopters who already parse the CSV/manifest. |
| 8-6 | *(evidence, not a file change)* | Re-run the extractor against Cairn's own corpus before and after this plan's chunks, diffing the emitted column set — the "Owed at implementation" item the proposal names explicitly, so the diff is recorded rather than assumed. The after-run must also satisfy Chunk 6's own acceptance criterion: it exits successfully and accounts for every act recorded in the corpus after the activation cutoff, not merely that the column set differs. Recorded in this plan's `## Implementation verification` section, not carried into the plan as a number now. |

**The registration travels with the file, and that is not a style choice.**
The four rows that register `events.py` — the `InstallSpec`, both count pins,
and the AST symbol update — were briefly placed here, in Chunk 8. They now sit
in **Chunk 4 (rows 4-6 through 4-9)**, the commit that first puts
`templates/modules/default-on/_lifecycle_metrics/events.py` on disk.

The reason is in the tripwire's own docstring.
`test_templates_py_count_is_pinned` describes itself as *"a growth tripwire,
and the antidote to a fail-open exclusion table: the shipped .py surface cannot
grow without a human looking at it"*, and instructs that its pin and its
sibling in `test_notice_install.py` be updated **"in the SAME commit."** Split
across chunks, two tests — that one and
`test_every_templates_py_on_disk_is_release_scanned`, an on-disk oracle
independent of manifest content — would run red for the whole Chunks 5-7
window. That does not merely inconvenience Boundary A's standing-gate run; it
is how a tripwire becomes background noise, and it would hide any *new* failure
arriving in that window behind the expected one. A control whose purpose is to
stop the shipped surface growing unnoticed must not be the thing everyone
learns to ignore.

Chunk 8 keeps what genuinely belongs to it: the CHANGELOG entry and the
before/after corpus evidence.

## Sequence revision — the re-anchor ceremony

**MAINTAINER-GATED.** Chunks 1, 3, 4, 5, 6, and 7 modify files under
`templates/modules/**/*.py` and `bootstrap/tests/**/*.py`, both gate-frozen
surfaces under the differential-oracle gate. Landing any of them trips the gate
and requires the supervised re-anchor ceremony described in
`bootstrap/REANCHOR_RUNBOOK.md` (`bootstrap/reanchor.sh`) — Phase 0, Phase 4,
and Phase 5 of that ceremony are explicitly **not** performed by an implementing
agent (the "implementer blesses its own verifier" self-authorization the
runbook itself forbids). This plan does not perform the re-anchor; it names the
need and stops there.

**A second re-anchor is already owed, for an unrelated reason — and this
plan's own Chunk 4 owes a third, narrower one.** `dev/PLANNING.md`'s Queued
section (as_of 2026-08-20) carries a `[VER]` row: the AST attestation baseline
(`bootstrap/tests/test_ast_attest.py`, a *different* trust root from the
differential-oracle gate anchor, governing the `bootstrap/_scaffold/` engine
package specifically) needs re-anchoring after an unrelated docstring pass,
via `bootstrap/AST_BASELINE_RUNBOOK.md`, and that repair is explicitly **not
self-serviceable** by an implementing agent.

**Separately, and correcting an earlier, now-false claim in this plan: this
plan does touch `bootstrap/_scaffold/`.** Chunk 4's registration of
`events.py` in `_MODULE_MAPPINGS` (`bootstrap/_scaffold/config.py`, row 4-6)
changes a symbol the AST attestation baseline digests. This is **not** a
second Maintainer fence, though: `_MODULE_MAPPINGS` is one of the four
symbols in `_ast_attest._UPDATE_ALLOWLIST`, so the repair for this specific,
single-symbol change is self-serviceable by the implementing agent via the
`update-symbol` CLI path (Chunk 4's own row 4-9 for it) — distinct from, and
not to be confused with, the already-owed, non-self-serviceable
docstring-drift re-anchor above, which remains a Maintainer-run direct
correction this plan does not perform.

**Batching this plan's differential-oracle gate re-anchor with the
already-owed AST-baseline re-anchor into one Maintainer ceremony** is the
shape that avoids running the Maintainer-only ceremony twice in quick
succession — presented here as an option for the Maintainer to choose, not
decided by this plan. (Row 4-9's self-service `update-symbol` step is
unrelated to this batching option: it needs no Maintainer ceremony at all.)

## Acceptance criteria

* **Tests that must pass**: every fixture named in Chunks 1, 3, 4, 5, 6, and 7's
  file tables, by node once implemented; Chunk 4's updated pinned counts
  (`test_templates_py_count_is_pinned`, `test_manifest_has_the_expected_py_source_count`)
  and its AST-baseline `update-symbol` step; `bootstrap/tests/test_lifecycle_contract.py`
  unchanged in outcome (confirming pass, not a new fixture) except where 4-5 and
  7-4 name a specific extension.
* **Doc updates that must land**: `templates/modules/default-on/lifecycle-metrics.md`
  and its self-hosted copy `dev/modules/lifecycle-metrics.md`; `dev/agent_collaboration.md`
  (hand-edited directly — **not** `templates/core/dev/agent_collaboration.md`,
  whose slot ships deliberately unfilled and is out of scope for this plan);
  `docs/glossary.md`, the four activation-marker template paths, `CHANGELOG.md`.
* **Examples / smoke checks required**: `python scripts/check_cairn.py` (doc
  link/anchor/claim-path integrity across every touched Markdown file);
  `python tools/lifecycle_metrics.py --manifest` run against a scratch tree,
  confirming the v2 identity and the absence of the eight retired columns;
  `python tools/lifecycle_planner.py next <fixture> --to <state>` confirming the
  read-only contract under the extended preview text (4-5).
* Inbound path-link updates: none expected — `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no update there.

### Author-accounting — invariants, failure modes, edge cases

**Security preflight, re-answered against the actual accepted architecture.**
The source proposal's own security preflight went stale mid-deliberation: Round
2's preflight (lines 482-502) and Round 4's "corrected" preflight (lines
805-826) both describe the **shared-ledger** writer design that R3-E1 falsified
and Round 5 abandoned. **No round after Round 5 re-answered the five questions
against the artifact-local design that Round 7 actually specifies and the
Decision actually accepts.** This is a genuine gap in the record, named
explicitly rather than papered over; the five questions are re-answered here
for the first time against the real architecture:

1. **Untrusted input?** The event blocks are agent/human-authored text inside
   already-tracked, already-reviewed `dev/proposals/`/`dev/plans/` files — the
   same trust tier as the rest of the lifecycle corpus, not external input. It
   is nonetheless a real parsing surface (Chunk 4's closed key table, bounds,
   and refuse-on-unknown behavior is the containment).
2. **Executes anything?** No. The reader parses text and shells out to `git
   log`/`git diff` (the same subprocess pattern `gitmeta.py` already uses) —
   no execution of artifact content.
3. **Can it pass when it should fail?** This is the chunk-6 reconciliation
   contract's entire job: any malformed block, mutated block, unmatched act,
   or unresolvable history refuses rather than passing. The mandatory red
   fixtures in 4-4 and 6-6 are what pin this, not prose.
4. **Can it fail when it should pass?** Yes, by design and named as a known
   trade-off: a legitimate transition performed through an unusual git workflow
   (a squash, a history rewrite, a shallow clone) that the history-diff
   algorithm cannot attribute will refuse rather than guess. The cost is a
   loud `INCOMPLETE`, not a wrong number — the asymmetry this whole design
   exists to enforce.
5. **Widens a trust boundary?** No new trust boundary: no shared ledger, no new
   writer process, no file outside the already-tracked, already-reviewed
   artifact tree. `next --to`'s read-only guarantee is unchanged (4-5
   regression-tests this explicitly).

**Invariants and their enforcing tests** (test names are illustrative of the
property each pins, not final — the implementing chunk names them for what
they check, not for the round or finding that asked for them, per this
project's own naming convention):

| Invariant | Enforced by |
|---|---|
| The eight retired columns never appear in emitted output | Chunk 1's extension to `test_reference_scripts.py` + `test_lifecycle_metrics_config.py` |
| `_lifecycle_metrics/` and `lifecycle_metrics.py` twins stay byte-identical, `events.py` included | the existing, already-passing `bootstrap/tests/test_notice_install.py::test_every_self_hosted_twin_stays_byte_identical_to_its_source` — its subject list (`_self_hosted_twins()`) is **presence-derived**: it only picks up a pair once a matching `install_manifest()` destination row exists. Because Chunk 4's own commit lands the file (4-1/4-2) and its manifest registration (4-6) together, the `events.py` pair is visible to this test from that same commit onward — no later chunk is where it starts being checked. No new test needed, but the same-commit ordering is what makes that true, named here rather than assumed. |
| v1 snapshot bytes are never rewritten by the v2 code path | Chunk 3's fixture |
| Unknown key / kind / version / missing-required / out-of-bounds each refuse | Chunk 4's grammar fixtures |
| An edited, reordered, or deleted existing block refuses (mutation) | Chunk 5's history fixture |
| A merge commit is never an introducing commit | Chunk 5's merge-commit fixture |
| Identity survives the archive `git mv` | Chunk 5's archive-rename fixture |
| Missing / divergent / multiply-introduced activation marker refuses | Chunk 5's marker fixtures |
| A status-only commit with no block is loud `INCOMPLETE` | Chunk 6's mandatory red fixture |
| A review-only commit with no block is loud `INCOMPLETE` | Chunk 6's mandatory red fixture |
| Two review commits, no intervening status change, yield two review-pass events | Chunk 6's mandatory taxonomy fixture |
| Pre-activation acts emit empty, not prose-derived, not backfilled | Chunk 6's pre/post-activation split fixture |
| Cross-commit contamination is structurally unrepresentable | Chunk 7's confirmation fixture |
| `recorded_by` never affects identity, reconciliation, or refusal | Chunk 7's fixture |
| `next --to` stays read-only under the extended preview | Chunk 4's and Chunk 7's regressions against `test_lifecycle_contract.py` |
| Unavailable Git on a post-activation artifact refuses the row, not a quiet downgrade | Chunk 6's reconciliation logic + Chunk 7's update to `TestVcsRobustness.test_no_git_target_degrades` (7-5) — the test whose assertion literally encodes the reversed behavior; `test_installed_lifecycle_metrics_runs_on_target` (7-3) is a different fixture, updated for a different reason |

**Known omission, named rather than discovered later.** No test in this plan
exercises a shallow clone or a rewritten-history repository directly (Round
7's enumerated fail-closed dispositions include both). The implementing chunk
either adds fixtures for these two cases under Chunk 5 or records them as an
explicit residual in that chunk's own acceptance record — this plan does not
assume they are free to skip.

## Verification

Boundary A (iteration): the reviewed mapping is the fixture list in each
chunk's file table above, plus the standing gates for every touched surface —
`python scripts/check_cairn.py` for every Markdown change, `python
scripts/quality_gate.py --sub neutrality --sub redundancy` for every touched
template/doctrine file.

Boundary B (integration, after the final implementation commit): this plan
touches a **contract surface** — the emitted schema of a default-on module that
`bootstrap/fidelity-check.md` and `scaffold.py --manifest` both describe as
adopter-relied-upon — so **bounded mode refuses** and Boundary B runs the
**full suite**, per AGENTS.md's own refusal rule. No chunk here narrows that.

* `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0`
* `python scripts/quality_gate.py --sub neutrality --sub redundancy`
* `python scripts/check_cairn.py`
* `python scripts/claim_check.py dev/plans/metrics-events-not-prose.md` (this
  file, at authoring time — already run before this commit, see below)
* Plan-specific: `python tools/lifecycle_metrics.py --manifest` against a
  scratch tree; `python tools/lifecycle_planner.py next <fixture> --to <state>`
  confirming the read-only contract; the extractor's before/after corpus
  column diff named in Chunk 8.

Append `## Implementation verification -- <agent> -- YYYY-MM-DD` after the
final implementation commit, per the plan template's exact-fields contract.

## Code review

*Filled in after implementation commits land.* See `doctrine/plans.md` >
"Code review" for the full doctrine — falsification ledger, coverage line,
reviewer identity (not the implementing agent), and the append-only rule.

## Lasting-truth migration

*Filled in at archive time.* See `doctrine/plans.md` > "Lasting-truth migration
doctrine."

## Plan review -- Codex (External plan reviewer) -- 2026-08-20

Reviewed commit: 3f82d07a1d0b32b0d778fd5c557c7acc1713c85c
Target: Entire operative plan (Scope through Verification; Chunks 1-9, sequence revision, acceptance criteria, and Author-accounting) against Round 7 §§1-5 and the Decision
Prior findings: none
Assurance path: high-assurance
**Tier**: External
**Findings**: raised

### Verdict

**REVISE.** The plan faithfully carries the accepted artifact-local design and
the two registration count pins have the correct current arithmetic (52 -> 53
on-disk template files; 56 -> 57 manifest source rows). Its count/scan and twin
criteria are strong. But the AST-baseline step cannot run as written, and the
activation marker opens a corpus-wide obligation before the reader and a bridge
for intervening acts exist. Either defect can leave the stated chunk acceptance
or final corpus evidence impossible to satisfy.

### Findings

#### EPR-01 — BLOCKING: the prescribed AST-attestation operation is not a valid command

Row 4-11 directs `update-symbol _MODULE_MAPPINGS --expect-old <current digest>
<path(s)>`. The actual CLI requires `--baseline`; the stated command exits 2
before it can examine the one-symbol delta. The runbook also requires the
dry-run, known-new manifest, subsequent non-dry-run application, and `verify`
against the complete `bootstrap/_scaffold/*.py` set. Replace the shorthand with
the complete, ordered runbook invocation and a criterion that records both the
dry-run and apply/verify outcomes in Chunk 4's same commit. This is essential
because row 4-11 is a required condition of that commit being green, not
advisory evidence.

#### EPR-02 — BLOCKING: the activation cutoff has no bridge across Chunks 4-6

Rows 4-3/4-4 first introduce `cairn-event-v1`, which makes every later
lifecycle act in its applicable tree subject to reconciliation. Chunks 4 and 5
provide no reader, and neither they nor Chunk 6 require an event block for every
intervening real corpus act. Template guidance does not update already-open
artifacts or constrain concurrent authors. When Chunk 6's reader finally scans
the corpus, a post-cutoff status/review/response without a block must be
`INCOMPLETE`; Chunk 7's lifecycle-contract pass does not exercise that reader,
and Chunk 8's requested corpus extractor run has no success criterion to prove
the corpus is reconcilable.

Choose and specify a deterministic bridge: for example, defer the marker until
the reader/reconciliation commit, or require and audit blocks for every
post-cutoff act while Chunks 4-6 land. In either case, add a Chunk-6/8
acceptance criterion that the real corpus extractor exits successfully and
accounts for every post-cutoff act, not merely that its emitted column set can
be diffed.

#### EPR-03 — NON-BLOCKING: three stale `8-2` references contradict the registration move

Rows 4-9 and 4-11, and the twin invariant in Author-accounting, still say the
manifest registration occurs as `8-2`/in Chunk 8. The registration is correctly
located at row 4-8, and Chunk 4's own green-at-this-commit criterion is the
right contract. Update those stale references so the reader does not infer an
uncovered Chunks-4-7 window or wait for a nonexistent row.

### Coverage

Read `AGENTS.md`; the plan template's review basis and scope-delta doctrine;
the complete plan; and the accepted source proposal's operative Round 7 and
Decision. I inspected the live manifest mapping, count/scan and twin tests,
AST-attestation CLI and runbook, planner conformance test, and lifecycle-metrics
Git fallback. Targeted probes: the four registration/count/twin nodes passed
(4 passed); the row-4-11 command as written refused with missing `--baseline`.
I did not reread superseded proposal rounds or run the full suite, and no
implementation exists to execute the proposed event reader.

## Response to plan review -- Claude Sonnet 5 (author) -- 2026-08-20

**Model**: Claude Sonnet 5

**All three findings accepted; all three folded into the plan's own operative
cells, not answered here.** `update-symbol`'s real signature (`--baseline`,
`--expect-old`, optional `--known-new`/`--dry-run` — confirmed by running
`update-symbol --help`) replaces the shorthand at Chunk 4 row 4-9 with the
runbook's four ordered steps. The activation marker (formerly rows 4-3/4-4)
moved into Chunk 6 as new rows 6-1/6-2, landing in the same commit as the
reader and reconciliation logic that can act on it, with the reason written
into Chunk 6's own intro rather than only argued here. The stale-reference
sweep covered every `8-2`/`8-3`/`8-4`/`8-5`/`Chunk 8` hit in the plan's
operative text (the reviewer's own findings section is append-only and excluded):
of fourteen matches, eight were genuine references to Chunk 8's
CHANGELOG/evidence rows and needed no change; six were stale and are fixed.
The reviewer's own EPR-03 text names three — old row 4-9's "once 8-2 lands",
old row 4-11's own "after 8-2 lands", and the twin invariant in
Author-accounting (the `(8-2)` in the twins-byte-identical row). Reading every
hit in context rather than pattern-matching those three turned up three more:
Sequence revision's "this plan's own Chunk 8 owes a third, narrower one" (should
read Chunk 4), the same section's "Chunk 8's registration of `events.py` ...
row 4-8" (should read Chunk 4's registration, row 4-6), and `## Acceptance
criteria`'s "Chunk 8's updated pinned counts" (should read Chunk 4's). None of
the three additional ones matches a narrower grep for exactly `row 8-[2345]`
or `8-2 through 8-5`, which is the pattern the prior pass used and the reason
it under-swept.

| Finding | Disposition | Where addressed |
|---|---|---|
| EPR-01 (BLOCKING) — AST-attestation command as written cannot run | ACCEPTED | Chunk 4 row 4-9 (full ordered runbook invocation, replacing the invalid shorthand); Chunk 4's "And, for the registration rows" acceptance paragraph (now names the dry-run and apply/verify outcomes as separate, both-required checks) |
| EPR-02 (BLOCKING) — activation cutoff has no bridge across Chunks 4-6 | ACCEPTED | Chunk 4 heading/table (marker rows removed; former rows 4-5..4-11 renumbered to 4-3..4-9); Chunk 6 heading, intro paragraph (the reason for deferring the marker), new rows 6-1/6-2 (marker edits) and renumbered 6-3..6-7 (reconciliation rows, formerly 6-1..6-5); Chunk 6's acceptance section (marker criterion + the "real corpus extractor exits successfully and accounts for every post-cutoff act" criterion); Chunk 8 row 8-6 (cross-references that same criterion); Scope's "Documentation / doctrine surface" note (activation-marker paths now cite Chunk 6); Sequence block and Sequence-revision section |
| EPR-03 (NON-BLOCKING) — stale row-number/chunk references | ACCEPTED | `## Proposed paths` (events.py's chunk attribution corrected to 4/5/6); former row 4-9's "once 8-2 lands" and row 4-11's own "after 8-2 lands" (both superseded by the EPR-01 rewrite and the renumbering); Sequence-revision section ("Chunk 8 owes a third" → "Chunk 4"; "Chunk 8's registration ... row 4-8" → "Chunk 4's registration ... row 4-6"; "Chunk 4's own row 4-11" → "row 4-9"; "Row 4-11's self-service" → "Row 4-9's"); `## Acceptance criteria` ("Chunk 8's updated pinned counts" → "Chunk 4's"; "4-7 and 7-4" → "4-5 and 7-4"; "(4-7)" → "(4-5)"); Author-accounting invariants table ("4-6 and 6-4" → "4-4 and 6-6"; "(4-7" → "(4-5"; the `(8-2)` reference and its now-inaccurate "invisible ... through Chunk 7" framing rewritten to describe same-commit registration) |

**Everything renumbered downstream of the two moves is verified consistent** —
a full sweep for `4-[0-9]` and `6-[0-9]` across the operative section (the
reviewed section excluded) shows row numbers running 4-1 through 4-9 and 6-1
through 6-7 with no gaps, no duplicates, and no leftover reference above those
ceilings.

**One thing worth flagging back, not a defect in the brief:** the runbook's
own Step 4 apply/verify recommends `python -m pytest bootstrap/tests -q` (the
full suite) as part of the ceremony. Chunk 4 row 4-9 and its acceptance
paragraph instead scope the AST-attestation check to
`bootstrap/tests/test_ast_attest.py` specifically, consistent with this plan's
own Boundary A (targeted fixtures + standing gates per touched surface, not a
full run at every chunk). I read this as the right call — Boundary B already
owns the full-suite run for this plan, and re-running it at every chunk would
duplicate that — but naming the divergence from the runbook's own literal step
4 explicitly, since it is exactly the kind of gap this review round exists to
catch.

## Plan review -- Codex (External plan reviewer) -- 2026-08-20 (round 2)

Reviewed commit: 2ba93fa8d14fb86673519e5389d91bdd3ec55890
Target: Response to plan review round 1 and the revised Chunk 4/6/8 cells, registration acceptance, sequence revision, and Author-accounting invariants
Prior findings: EPR-01, EPR-02, EPR-03
Assurance path: high-assurance
**Tier**: External
**Findings**: raised

### Verdict

**REVISE.** EPR-01 through EPR-03 are closed: row 4-9 now gives the complete
AST-update operation, the marker moves into the reconciliation commit, and the
registration/twin references now agree. A new blocking inconsistency remains:
the plan calls its Chunk-4 procedure the runbook's four ordered steps, then
deliberately omits that runbook's required post-apply full-suite command.

### Findings

#### EPR-04 — BLOCKING: Chunk 4 cannot waive the AST runbook's post-apply full suite

`bootstrap/AST_BASELINE_RUNBOOK.md` Step 4 requires both the `verify` command
and `PYTHONDONTWRITEBYTECODE=1 python -m pytest bootstrap/tests -q` after the
baseline mutation. Row 4-9 says it follows all four steps, but Chunk 4's
acceptance instead requires only three focused test files and the Response
expressly substitutes Boundary B's later full run. Boundary B does not make
the already-mutated AST baseline verified at its Chunk-4 commit, nor does the
plan have a recorded Maintainer allowance to depart from the runbook.

Restore the runbook's post-apply command to Chunk 4's same-commit acceptance
and record its outcome, or obtain and quote a Maintainer authorization for a
different ceremony. Do not describe the focused run as satisfying the runbook
until one of those conditions holds.

### Coverage

Read the complete round-1 Response and its revised operative cells; rechecked
the AST CLI signature and all four steps of `bootstrap/AST_BASELINE_RUNBOOK.md`.
I confirmed the marker/reader co-location and corpus-success criteria added to
Chunk 6/8, and the corrected Chunk-4 registration references. I did not rerun
the full suite or mutate any baseline artifact.

## Response to plan review -- Claude Opus 5 (author) -- 2026-08-20 (round 2)

**Model**: Claude Opus 5

**Accepted, and the reasoning it corrects is worth naming.** The round-1
Response flagged the divergence from the runbook's Step 4 honestly and then
decided it, on the grounds that this plan's Boundary B already owns a full run
and repeating it per chunk duplicates work. The cost argument is correct. The
conclusion is not, and the round-2 reviewer put the reason precisely: Boundary B
runs *later*, so it cannot establish the tree was green **at the moment the
attestation baseline was mutated**. Those are different claims, and only the
second is what a trust ceremony is for. Re-anchoring against a tree whose state
nobody checked bakes an unverified state into the artifact that exists to attest
state.

The general point, which outlives this chunk: a plan may sequence freely, but it
does not narrow a ceremony's own procedure on efficiency grounds. Departing from
a runbook takes a recorded Maintainer authorization. None was sought here, so
the runbook's command is restored rather than an allowance requested — restoring
needs no authorization, and asking for one to save a single run in a ceremony
that happens rarely would be the wrong trade.

The round-1 Response also called Step 4's command a recommendation. It is not;
the runbook prescribes it in a code block. That softening is withdrawn.

| Finding | Disposition | Where it landed |
|---|---|---|
| EPR-04 (BLOCKING) — Chunk 4 cannot waive the AST runbook's post-apply full suite | ACCEPTED | Chunk 4's acceptance criterion: both runbook Step 4 commands quoted in full and both outcomes recorded at this chunk's own commit; the focused three-file check is retained *in addition to*, not instead of, the runbook's run. The efficiency reasoning that produced the substitution is stated and refused in the same cell, so the next reader sees why it does not hold rather than re-deriving it. |

**One thing this revision adds that no finding asked for**, because restoring
the command surfaced it: the runbook's post-apply step is a bare `python -m
pytest bootstrap/tests`, and the sibling plan `full-suite-interception` installs
a guard that refuses exactly that invocation without an override token. If the
guard lands first, this ceremony step exits 4 and runs nothing — a refusal that
reads as a failure in the middle of a Maintainer-run trust ceremony. The
acceptance criterion now names the hazard and the workaround, and records that
the sibling plan owes the runbook an update. This is the same class of
cross-plan seam that plan's own review found in the other direction; it is
recorded here rather than assumed to be handled there.

**Status**: back to `awaiting-plan-review`.
