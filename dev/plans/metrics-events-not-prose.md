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
wiring every retained event-derived field to exactly one event kind. **"Every
retained event-derived field" spans both schemas the extractor emits, not only
`PROPOSAL_COLUMNS`.** `PLAN_COLUMNS`' `plan_review_rounds`/`code_review_rounds`
are retained (Part 1 retires none of the six `PLAN_COLUMNS` names) and are
computed today by the same heading-count regex class Part 3 exists to retire —
Round 6's taxonomy names `## Plan review` and `## Code review` sections
explicitly among the acts a `review-pass` block supplies. Chunk 6 wires them
alongside the proposal-row fields, rather than leaving them prose-derived while
`PROPOSAL_COLUMNS`' `review_rounds` is fixed beside them. Nothing here narrows
any of Round 7's commitments — this is decomposition into commits, not a
second design pass.

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

**The declaration above named one failure-disposition determination and
missed three more this plan also makes, beyond the accepted contract's own
text.** `dev/plans/_template.md`'s review-basis doctrine lists "failure
disposition" as a dimension a plan declares under `Contract expansion`; the
three below were flagged as undeclared in review and are recorded here rather
than left implicit in the paragraphs that reason them out (Chunk 5's
Activation section; Chunk 5's act-list paragraph):

* **A missing activation marker does not refuse.** Round 7 §4's own text reads
  "Missing, divergent, or multiply-introduced markers refuse" — this plan
  departs from the literal "Missing" clause, authorized by the Maintainer's
  "I think (c) is right" (Chunk 5's Activation section names what (a) and (b)
  were).
* **The marker's own introducing commit is pre-cutoff**, not post-cutoff —
  this plan's own inference (Chunk 5's Activation section), not a Round 7
  sentence.
* **Git entirely absent is treated as pre-cutoff, field-kind-dependent**,
  rather than as "reconciliation cannot be performed" — also this plan's own
  inference (Chunk 5's Activation section), reasoned from the refusal
  trigger's own precondition rather than stated in Round 7's text.

None of the three narrows accepted scope — each is a reading of an
underspecified edge the accepted text leaves open, not a retreat from it — but
the declaration exists so a future reader sees what this plan settled beyond
the literal accepted contract without re-deriving it from the reasoning
paragraphs.

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

**A correction to this section's own earlier reasoning, caught in review.**
This paragraph previously worried that removing `'backfill'` from `--event`'s
recognized values would make an adopter's already-written
`snapshot_event=backfill` rows "unreadable," and built an acceptance clause
on that worry. Checked directly: no tool in this tree parses a persisted
snapshot CSV back in at all — `grep -rn 'csv.DictReader|csv.reader'` over
`tools/` and `scripts/` returns nothing, and `snapshot.py`'s only read of the
snapshot directory is `_next_snapshot_index`, which reads filenames, not
rows (the same grep form finds `csv.writer` at
`tools/_lifecycle_metrics/report.py:35`, confirming the instrument could
have matched before trusting its absence). There is no reader to render
anything unreadable, so removing `'backfill'` from `--event`'s choices — part
of this row's own edit — carries no read-side hazard; a pre-existing file
with `snapshot_event=backfill` in it is inert data, exactly as any other
persisted CSV is once written. The conservative instinct was right for the
wrong reason: nothing in 1-10 deletes or rewrites a persisted file either
way, so no adopter archive is at risk — but not because a reader "tolerates"
the value, since none reads it.

**Acceptance for this chunk**: a fresh extractor run over a fixture proposal
with review findings emits no `total_findings`/`findings_p*`/`review_yield_*`
keys in either CSV or `--format md` output, while every retained column is
present and unchanged in value from before this chunk. Separately, `python
tools/lifecycle_metrics.py --backfill-from 2026-01-01` exits non-zero with an
unrecognized-argument error rather than running, and `--help` does not
mention it.

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
| 4-1 | `tools/_lifecycle_metrics/events.py` (new) | Grammar parser: recognizes the `cairn-event-v1` fence, validates the closed key table above, returns a typed block or a refusal reason. No history walking yet (that is Chunk 5) — this chunk is pure block-level validation. The `from_state`/`to_state` check takes the valid-state collection as an explicit parameter (`valid_states: Sequence[str]`) rather than loading it itself: `events.py` carries **no import of `extract.py`**, because Chunk 6 wires `extract.py` to import `events.py` for reconciliation (row 6-3/6-4), and a loader call the other direction would be circular. The caller supplies the vocabulary — row 4-10 names where `extract.py` gets it from for the real corpus walk; this chunk's own fixtures (4-4) pass a small literal test vocabulary directly, which is ordinary unit-test practice and not the local-status-tuple fork row 4-12 exists to catch (no production code here declares a status literal). Carries the `SPDX-License-Identifier: MIT` header within its first four lines, matching every other file in this package. |
| 4-2 | `templates/modules/default-on/_lifecycle_metrics/events.py` (new) | Gate-frozen twin of 4-1, same commit — SPDX header included. `bootstrap/tests/test_notice_install.py::test_every_template_py_source_carries_spdx_header` and `::test_every_self_hosted_twin_carries_spdx_header` require it of both new files; the focused check at row 4-9 already runs this test file, so a missing header fails loudly there. |
| 4-3 | `tools/lifecycle_planner.py`, twin `templates/skills/_lib/lifecycle_planner.py` | `next --to <state>`'s preview/mutation-manifest output additionally shows the literal event block the transitioning edit is expected to carry — scaffold-only, informational, not written to disk, not gating. The command's read-only contract is unchanged; a regression test confirms it still writes nothing (see 4-5). Not gate-frozen (outside `templates/modules/**`), but still a same-commit twin pair. |
| 4-4 | `bootstrap/tests/test_lifecycle_metrics_events.py` (new) | Grammar red/green fixtures: unknown key refuses; unknown `kind` refuses; unknown version token refuses; missing required key per kind refuses; a `reviewer`/`model` value over 120 chars refuses; the three worked examples above each parse cleanly. |
| 4-5 | `bootstrap/tests/test_lifecycle_contract.py` | Re-run (not necessarily re-write) the existing read-only regression — `test_every_subcommand_is_read_only` or its equivalent, as_of 2026-08-20 line 172 — against the extended preview output, confirming the new block-preview text changes stdout only, no byte written, no git operation performed. |
| 4-6 | `bootstrap/_scaffold/config.py` | Register the engine file Chunk 4 (4-1/4-2) creates: add `InstallSpec("default-on/_lifecycle_metrics/events.py", "tools/_lifecycle_metrics/events.py", verbatim=True)` to the `"lifecycle-metrics"` entry in `_MODULE_MAPPINGS`, alongside the nine existing `_lifecycle_metrics/` rows (confirmed at ~lines 739-766, as_of 2026-08-20); update the neighboring comment's "the nine package files install verbatim" to "the ten package files install verbatim". Without this row `scaffold.py` never installs `events.py` and an adopter's `extract.py` import of it resolves to nothing on disk. Maintainer direction: these two engine files are to be included, not treated as an open scope question. |
| 4-7 | `bootstrap/tests/test_security_lint.py` | `test_templates_py_count_is_pinned` (line 376, as_of 2026-08-20) pins `len(on_disk) == 52` over `templates/**/*.py`. Update it to the post-registration count (52 + 1, as_of 2026-08-20 — re-derive at implementation from the live tree, do not carry a frozen number forward). Also confirm `test_every_templates_py_on_disk_is_release_scanned` in the same file passes once this chunk's own registration (4-6) lands: that check's oracle is the on-disk file set, independent of the manifest-derived count pin, and fails closed on any shipped `.py` present on disk but not release-scanned. |
| 4-8 | `bootstrap/tests/test_notice_install.py` | `test_manifest_has_the_expected_py_source_count` (line 74, as_of 2026-08-20) pins `len(sources) == 56` over manifest `.py` sources. Update it to the post-registration count (56 + 1, as_of 2026-08-20 — re-derive at implementation, do not carry a frozen number forward). |
| 4-9 | AST attestation baseline, via `bootstrap/tests/_ast_attest.py`'s `update-symbol` CLI path (per `bootstrap/AST_BASELINE_RUNBOOK.md`) | Row 4-6 changes `_MODULE_MAPPINGS`'s `Assign` node in `bootstrap/_scaffold/config.py`, a symbol the AST attestation baseline (`bootstrap/tests/fixtures/scaffold_ast_baseline.json`, enforced by `bootstrap/tests/test_ast_attest.py`) digests. `_MODULE_MAPPINGS` is one of the four symbols in `_ast_attest._UPDATE_ALLOWLIST` — unlike the unrelated, already-owed docstring-drift re-anchor named below under "Sequence revision" — so this single-symbol repair is self-serviceable by the implementing agent, in the same commit, following `bootstrap/AST_BASELINE_RUNBOOK.md`'s four steps in order (the CLI has no shorthand form; `update-symbol --help` confirms it requires `--baseline` and `--expect-old`, and accepts `--known-new` and `--dry-run`): **(1) diagnose** — run the runbook's `_merge_current`/`_classify` snippet against the live `bootstrap/_scaffold/*.py` set at this commit, confirm `_MODULE_MAPPINGS` is the *only* CHANGED symbol with MISSING and DUPLICATE both 0, and trace any logic-bearing NEW symbol to a landed, reviewed commit; **(2) known-new** — check the diagnosis against `bootstrap/tests/fixtures/scaffold_ast_known_new.json` (never a reimplementation of `_merge_current`/`_classify`), treating any DROPPED or REKEYED key as a review item traced to its own commit before proceeding; **(3) dry-run** — `python bootstrap/tests/_ast_attest.py update-symbol _MODULE_MAPPINGS --baseline bootstrap/tests/fixtures/scaffold_ast_baseline.json --expect-old <current live digest, re-derived at this commit, never copied from this plan> --known-new bootstrap/tests/fixtures/scaffold_ast_known_new.json --dry-run bootstrap/_scaffold/*.py`, which refuses on a stale `--expect-old`, an allowlist miss, more than one CHANGED symbol, or an undeclared NEW symbol — each refusal is the guard working, not a bug to route around; **(4) apply, verify, commit** — drop `--dry-run`, then `python bootstrap/tests/_ast_attest.py verify bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py`, confirming the `AST attestation OK — N baselined symbol(s) accounted for, unchanged.` tail with **N unchanged** from before this row (a surgical rewrite, not a re-pin), and commit `bootstrap/tests/fixtures/scaffold_ast_baseline.json` plus `bootstrap/tests/fixtures/scaffold_ast_known_new.json` together, explicit paths, in this same chunk commit. |

**The grammar's `from_state`/`to_state` bound needs a named vocabulary
source, and the anti-fork audit needs to know this file exists.** Round 7's
closed key table bounds those two keys to "a declared lifecycle status for
that artifact type" — `events.py` is therefore a new consumer of Cairn's one
runtime status vocabulary, and three more rows exist because of it, rather
than leaving an implementer to invent a fourth copy of the loader pattern or a
locally-declared status tuple (`AGENTS.md` > *Verifying claims* names a silent
gap in a guard as worse than no guard).

| # | File | Change |
|---|------|--------|
| 4-10 | `tools/_lifecycle_metrics/extract.py` + twin | Extend `_REQUIRED_EXPORTS` from `('PLAN_STATES', 'HISTORICAL_PLAN_STATES')` to also require `'PROPOSAL_STATES'` (the planner's **current** proposal-status enum, `tools/lifecycle_planner.py:1113`) — the historical variant is not added, because a freshly-authored event block only ever names a currently-declared status, never a retired token. `extract.py`'s existing `_vocabulary()`/`_validated_planner_path()` mechanism is otherwise unchanged: this row widens what it requires, not how it loads. This is the vocabulary `events.py`'s grammar checks against (row 4-1); `extract.py` calls `_vocabulary()` once per corpus walk and passes the relevant enum — `PROPOSAL_STATES` for a proposal-hosted `transition` block, `PLAN_STATES` for a plan-hosted one — into `events.py`'s parser as the `valid_states` argument. |
| 4-11 | `bootstrap/tests/test_lifecycle_vocabulary.py` | This file's `METRICS_SPEC` (a `ConsumerSpec` instance, ~line 580) drives `extract.py`'s half of `TestLoaderContainmentMatrix` and names one export it requires (`"PLAN_STATES"`, used to build a decoy planner satisfying every consumer under test, ~line 593's `_DECOY_PLANNER_SRC`). Add `PROPOSAL_STATES = ('DECOY',)` to `_DECOY_PLANNER_SRC` so the decoy still structurally satisfies both consumers once `extract.py` requires a second export; add a fixture mirroring the existing "missing a required export is purged, not cached" case (~line 794) for the newly-required export specifically, so both halves of `_REQUIRED_EXPORTS` are independently exercised, not only the one the existing matrix already covers. This is the file EPR-14 asked for, corrected from the round-4 review's own citation: `bootstrap/tests/test_pilot_evidence.py::TestVocabularyLoader` tests `templates/skills/_lib/lifecycle.py`'s own independent copy of the loader pattern (`MODULE_PATH` there, line 51) — a different consumer this plan does not touch, confirmed by reading that file's import target directly rather than trusting the citation. |
| 4-12 | `bootstrap/tests/test_lifecycle_vocabulary.py` | `_AUDITED_CONSUMER_SOURCES` (~line 327, currently a 5-tuple: `transition_lint.py`, both `extract.py` copies, both `lifecycle.py` copies) grows to a 7-tuple with both `events.py` copies added. Update the count/uniqueness assertions that currently pin `5` (`len(_AUDITED_CONSUMER_SOURCES) == 5`, `len(set(...)) == 5`) to `7`, and add the same pairwise-distinctness assertions the existing pairs already carry (mirroring `_AUDITED_CONSUMER_SOURCES[3] != _AUDITED_CONSUMER_SOURCES[4]`) for the two new entries. `events.py` declares no local status literal under this chunk's design (row 4-1), so this addition is presently vacuous against `test_no_consumer_local_status_literal_survives` — it is still required, because the audit's whole purpose is to catch a *future* local literal in a file it already scans, not only a present one, and a consumer left out of the tuple is invisible to it regardless of whether today's version of that file happens to be clean. |
| 4-13 | `bootstrap/tests/test_lifecycle_metrics_events.py` | Extend 4-4's fixture list: a `from_state`/`to_state` value outside the supplied `valid_states` refuses, using a small literal test vocabulary (not the real loader) — this chunk's own fixtures stay pure-function and need no planner on disk. Chunk 6 (row 6-3/6-4) adds the integration-level fixture that exercises the real vocabulary end to end. |

**Acceptance for this chunk**: every fixture in 4-4 and 4-13 passes;
`bootstrap/tests/test_lifecycle_vocabulary.py` passes in full, including the
extended `_AUDITED_CONSUMER_SOURCES` tuple (4-12) and the second-export
fixture (4-11); `next --to` remains provably read-only under the existing
contract test.

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

**A hazard for whoever runs this — already live, not merely forward.** That
second command is a bare `python -m pytest bootstrap/tests`, and
`bootstrap/tests/conftest.py`'s `pytest_collection_finish` (landed 2026-08-20
per the sibling plan `full-suite-interception`'s Chunk A) refuses exactly
that invocation — `pytest.UsageError`, exit 4 — unless `CAIRN_FULL_SUITE=1`
is set. Prefix this command with the override:
`CAIRN_FULL_SUITE=1 PYTHONDONTWRITEBYTECODE=1 python -m pytest bootstrap/tests -q`.
This is the standing answer, not a stopgap pending someone else's fix: reading
that sibling plan directly, `bootstrap/AST_BASELINE_RUNBOOK.md:126` appears
under a section headed "Live commands the guard breaks beyond AGENTS.md's own
sentence — **flagged, not authorized**," and no chunk in that plan edits the
runbook. The fix is recommended to the Maintainer there, not owed by that
plan's own agent. A run that comes back exit 4 with a refusal message has been
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
events, `dev/plans/_template.md` for plan-hosted events).

**A marker path can be wrong, or it can simply not exist yet — those are
different dispositions.** A **divergent** marker (the pair — Cairn's own
installed copy and the shipped template — disagrees) or a **multiply-
introduced** one (removed and re-added) is a tree where something is
genuinely wrong: you cannot compute a defensible series when you do not know
what period it covers, and producing one anyway is worse than producing
none. **Both refuse.** A tree with **no marker at all** is different in
kind, not degree — nothing is wrong with it, recording simply has not
started there yet.

**The option that names, recorded because a bare letter will mean nothing
later** — the same discipline the `--backfill-from` removal above already
applies to its own lettered choice: **(a) refuse**, matching Round 7 §4's
literal "Missing ... markers refuse" text without exception; **(b) quiet-
degrade to the old prose-parsed value** for an unmarked tree, the same
backfill/derived-unreliable shape the Decision's `Scope delta: degraded`
allowance already rejects for the historical-continuity question (the
"rejected option (b)" the Chunk 6 empty-value paragraph below refers back
to); **(c) treat an unmarked tree as not yet activated** and return an empty
series. Maintainer decision, quoted verbatim: "I think (c) is right" — the
chosen disposition is (c): an unmarked tree returns an empty series, the same
emission this chunk already gives every pre-cutoff act on an activated tree
(see "The dropped-historical-continuity allowance, made concrete" below),
generalized to the case where no cutoff has been established at all.
**Missing does not refuse.**

This is a **departure from Round 7 §4's own literal text**, not a reading
compatible with it — the accepted contract says "Missing ... markers refuse"
in as many words, and (c) is the opposite for the specific case of a marker
that never existed. The departure is authorized (the Maintainer's quote
above), and it is declared as a departure — not silently folded in as if the
accepted text already said this — in Scope's `Contract expansion`
declaration.

**What (c) concedes, named rather than glossed.** A marker deleted by
accident now reads exactly like a tree that never took the template
update — "not started," not "something is wrong." Refusal is kept for the
divergent and multiply-introduced cases precisely so a corrupted marker is
not the *only* undetectable failure mode; a clean deletion is genuinely
indistinguishable from never-installed, and this plan builds no mechanism to
tell the two apart.

**The marker's own introducing commit is pre-cutoff, not post-cutoff.**
"From that commit on" (Chunk 6's framing) names the window reconciliation
applies to; it does not mean the introducing commit's own diff is itself
inside that window. The introducing commit is the *first* commit at which
"the tree now has a marker" becomes true — an act co-committed in that same
diff (a status flip, a review pass, a response) was authored before any
reader existed to tell its author a block was expected, since the marker and
the reader land together (Chunk 6). Treating that commit as pre-cutoff is
not a special case bolted on; it is (c)'s own "recording has not started
yet" logic applied at commit granularity instead of tree granularity. The
concrete case this resolves:
`bootstrap/tests/test_reference_scripts.py::TestVcsRobustness::test_main_branch_target_runs`
scaffolds a tree — which, once Chunk 6 lands, installs a marker-carrying
`dev/proposals/_template.md` — writes a sample proposal that already
carries a `## Review` section, and commits everything (the marker's own
introduction and the proposal's review-pass act) in **one** `git commit`.
Under the exclusive reading taken here, that act is pre-cutoff and the
test's `# must not raise` comment holds with no code or test change; under
an inclusive reading it would refuse. 5-3's fixtures pin the exclusive
reading directly, and Chunk 7 confirms this specific pre-existing test
against it.

**What the exclusive reading concedes, for the case this section had not yet
named.** The deletion paragraph above names what (c) concedes for a marker
that is later removed; the exclusive cutoff has its own concession, distinct
from that one. A lifecycle act co-committed with the marker's own
introduction is **permanently unmeasured and undetectable** — there is no
later signal that distinguishes "this commit performed a lifecycle act
before any reader existed" from "this commit performed a lifecycle act and
the block was simply never written." In Cairn's own tree that window is
**empty**: the marker's introducing commit is Chunk 6's own implementation
commit, which lands the reader and the reconciliation logic, not a status
flip, review pass, or Response of its own — confirmed by inspecting what
Chunk 6's commit actually contains. **It is not empty for an adopter tree**:
an adopter who takes the template update in the same commit as a status flip,
a review pass, or a Response silently drops that one act from the series,
with no error and no residual marker distinguishing it from ordinary
pre-cutoff history. Named here because the plan is elsewhere careful to state
what an authorized departure costs, and this is the one place that habit had
been applied to the deletion case but not to this one.

**A root commit's parent sequence is empty, not ambiguous.** Step 2 requires
"the parent sequence" and step 5 refuses on ambiguous multi-parent
attribution; neither sentence says what a commit with **zero** parents (a
repository's first commit) resolves to. It is not the step-5 refusal case —
that refusal is about *multiple* parents making attribution ambiguous, and a
root commit has no ambiguity to resolve. A root commit's parent sequence is
the empty sequence, which is trivially a prefix of its own block sequence, so
step 2's prefix check holds and every block introduced by a root commit is
attributed to it exactly as an ordinary linear commit would be. This matters
concretely: a fresh adopter tree's first commit, and 5-3's own "clean linear
history" fixture, both begin at a root commit, and an implementer reading
"refuse on ambiguous parent attribution" in isolation could reasonably (and
wrongly) extend the refusal to zero parents too.

**The act list the reconciler checks is read from the same committed history
it reads blocks from, not from the live working-copy file — named explicitly
because the two disagree in the ordinary case of an uncommitted edit.**
Today's extractor parses the file on disk directly for every field
(`text = path.read_text(...)`, `extract_proposal_row`); Chunk 5's algorithm
walks committed history for blocks. Left unresolved, those are two different
sources of truth: a review section written into the file but not yet
committed exists on the working-copy side and cannot exist on the
history-walk side, which under a naive reading of Chunk 6's refusal rule
would make every such edit a post-cutoff act with no matching block —
`INCOMPLETE` on every dirty working tree carrying an uncommitted lifecycle
act, including this plan's own evidence runs (row 6-8 appends a block "in
the same commit that performs the act", which means a window where the act
is written and uncommitted exists on every such turn). **Resolved:** for
**every** post-cutoff reconciliation — `transition` acts exactly as
`review-pass`/`response` ones, since row 6-4 sources post-cutoff `transition`
fields from reconciled blocks too, not only the review-pass/response
half — the act list is derived from HEAD, the same commit the block-history
walk reads from, not from the working-copy text. An uncommitted lifecycle
act is invisible to *both* sides symmetrically until it is committed, exactly
as an uncommitted block would be. Running the tool against a dirty working
tree neither refuses nor counts the uncommitted act; it reports the corpus as
it stood at the last commit, and a subsequent run after committing the act
(with its matching block) reconciles and counts it normally. This is a
genuine behavior change from today's tool for the **post-cutoff** portion
only — pre-cutoff fields already read the working copy directly and are
unaffected, per row 6-4's unconditional quiet-degrade rule for
transition-kind fields and the empty-emission rule for review-pass/
response-kind fields. 5-3 adds the fixture: a post-cutoff artifact with an
uncommitted review-pass edit in the working tree neither refuses nor
reflects that edit; committing it (with its block) in a following commit
does.

**Git entirely absent is a different question from "unavailable Git for a
post-activation artifact," and the fallback it produces is not one thing —
it is field-kind-dependent, exactly as Chunk 6 (row 6-4) already splits
pre-cutoff behavior for an activated tree.** Chunk 6's refusal for
unavailable Git presupposes the tool already knows the artifact is past its
cutoff — a fact only a history walk can establish. With no `.git` in the
target at all, there is no history to walk, so that fact cannot be
established either way; the refusal trigger's own precondition is unmet, and
the act is treated as **pre-cutoff** — the same disposition a missing marker
already gets under (c), for the same reason (nothing proves otherwise). This
is not a weakening of Chunk 6's rule; it is the rule's own precondition
failing to hold. What "pre-cutoff" *means* is not uniform across field
kinds, and this row does not introduce a new rule here — it inherits the one
row 6-4 already states: **transition**-kind fields (dates, `days_*`,
`hours_*`, `stage_timestamp_reliability`, `revised`) keep their existing,
unconditional quiet-degrade computation — Part 3 does not touch that
historical portion regardless of *why* the act is pre-cutoff. **Review-pass
and response**-kind fields (`review_rounds`, reviewer identity,
`cross_agent_type_review`, `response_models`) emit **empty**, never the old
heading-count/regex-scraped value — the Decision is explicit that the old
prose-parsing path is retired, not merely superseded once a cutoff exists
("not computed from the old prose-parsing path... both of those were the
rejected option (b)"), so falling back to it for an unprovable-cutoff act
would reintroduce exactly the inflatable metric Part 3 exists to remove.

Three existing tests turn on this and are confirmed, not merely assumed, in
Chunk 7 — and one of them genuinely changes:

* This file's own `test_no_git_target_degrades` and
  `bootstrap/tests/test_lifecycle_stage_patterns.py::test_t12_a_target_with_no_git_still_degrades_to_best_effort`
  assert only **transition**-kind fields (`stage_timestamp_reliability`),
  so both keep passing unmodified under the "unconditional quiet degrade"
  half of the rule above.
* `test_installed_lifecycle_metrics_runs_on_target` (this file) scaffolds a
  marker-carrying template, never runs `git init`, and asserts
  `row["review_rounds"] == 1` — a **review-pass**-kind field. Under the
  "empty, never old-computed" half of the rule above, that assertion no
  longer holds once Chunk 6 lands: `review_rounds` becomes empty for this
  row, and the test's assertion is updated accordingly (7-3), not left as a
  false confirmation.

| # | File | Change |
|---|------|--------|
| 5-1 | `tools/_lifecycle_metrics/events.py` | History-diff walk (rename-aware, oldest-first), the parent-prefix mutation check, added-suffix attribution, matching-act requirement, multi-parent refusal, `(commit, index)` identity derivation, per-marker activation cutoff derivation. The walker's own public entry point takes and threads through the same `valid_states` parameter row 4-1's block parser accepts (it calls that parser once per commit's block sequence) — the parameter is not reintroduced at this layer, only forwarded. Reuses `gitmeta.py`'s existing git-subprocess pattern (`_git_log_for_path`, `--follow`) rather than a second implementation where that pattern already covers the need. |
| 5-2 | `templates/modules/default-on/_lifecycle_metrics/events.py` | Twin of 5-1, same commit. |
| 5-3 | `bootstrap/tests/test_lifecycle_metrics_events.py` | Fixtures built against a real scratch git repository (reusing the `_git` helper pattern already present in `bootstrap/tests/test_lifecycle_contract.py`, as_of 2026-08-20 line ~70, rather than inventing a second one): a mutated (edited/reordered/deleted) existing block refuses; a merge commit introducing a block refuses; identity is stable before and after a `git mv` to `archive/`; divergent and multiply-introduced markers each refuse, a **missing** marker does not (it resolves to no activation cutoff, and the reader treats every act as pre-cutoff — empty for review-pass/response fields, unchanged quiet-degrade for transition fields, per Chunk 6's row 6-4 — rather than raising); an act committed in the **same diff as the marker's own introduction** is pre-cutoff by the same rule (the boundary case `test_main_branch_target_runs` already exercises informally, reproduced here as a named fixture rather than left to that one test); a clean linear history with two distinct commits each adding one block resolves two distinct, stable identities; **a root (zero-parent) commit** introducing a block is attributed normally, not refused as ambiguous; **an uncommitted working-copy edit** on a post-cutoff artifact (a review-pass act written to disk but not yet committed) is invisible to reconciliation — neither refused nor counted — until a following commit lands it alongside its block. |

**Acceptance for this chunk**: every fixture in 5-3 passes against a real git
repository (not a mocked history), including the archive-rename identity
fixture, which is the concrete correctness case R5-E1 found broken in the
prior `(artifact path, block position)` identity scheme.

### Chunk 6 — Activation markers, fail-closed reconciliation, wiring the retained fields

Depends on Chunk 5. This chunk also carries the two rows that add the literal
`cairn-event-v1` marker to the four template paths (6-1/6-2), moved here
rather than landing alongside the grammar in Chunk 4. The marker's introducing
commit establishes the activation cutoff; every lifecycle act committed
**strictly after** it — not the introducing commit's own diff, which is
pre-cutoff (Chunk 5's Activation section states why) — is subject to
reconciliation. So landing the marker before a reader exists to do that
reconciliation would open a window with an obligation and nothing to
discharge it. Closing that window without deferring the marker would instead
mean requiring and auditing an event block for every post-cutoff act while
Chunks 4-6 land, which is not this plan's to impose: it
would bind whoever commits a lifecycle artifact in this tree during that
window, including in a concurrent session with no reason to know a plan's own
chunk boundaries changed what an event-worthy edit requires, enforced only by
template guidance nobody engaged in that session has read. Landing the marker
and the reader in the same commit is the option that depends on no one else's
session. This chunk is where Part 3 actually replaces prose-parsing for the
fields it claims, and where the `Scope delta: degraded` allowance gets its
concrete, checkable shape.

**That "depends on no one else's session" claim holds only for the Chunks
4-6 window; it does not extend past this chunk's own commit, and this plan
names what changes there rather than leaving it implicit.** From this
chunk's commit onward, every `**Status**` flip, review section, and Response
section committed anywhere in `dev/proposals/` or `dev/plans/` — by any
session, not only this plan's — is a post-cutoff act the extractor now
expects a block for. This plan controls its own commits and nothing else's,
so the disposition is two-part:

* **This plan's own acts.** From this chunk's own commit onward, the
  implementing agent appends a `cairn-event-v1` block to every lifecycle act
  it performs on this plan's own file — a further status flip, this file's
  own eventual code review, and so on — in the same commit that performs the
  act (row 6-8).
* **Everyone else's acts.** Two sibling plans are active on the board as of
  this writing (`full-suite-interception`, `suite-run-diagnostics`), each
  expected to take further review passes and status flips of its own before
  this plan's implementation finishes. This plan has no authority over those
  sessions and invents none. Row 8-6's corpus-wide extractor run is recorded
  as **evidence** of the corpus's real state — including naming any
  unreconciled act by artifact/commit/kind — not as a pass/fail gate this
  plan's own completion can be held to independent of its own conduct. What
  gates this plan's own acceptance is narrower: every act *this plan's own
  commits* perform, from this chunk onward, carries a matching block and
  reconciles cleanly (see this chunk's own acceptance section and 8-6).

**The taxonomy (Round 6, reproduced as the binding contract):**

| Event kind | Emitted alongside | Retained fields it supplies |
|---|---|---|
| `transition` | the `**Status**` flip | transition dates; `days_*`, `hours_*`, `stage_timestamp_reliability`; `revised` |
| `review-pass` | each `## Review` / `## Plan review` / `## Code review` section | `review_rounds`, declared tier, `cross_agent_type_review`, reviewer identity |
| `response` | each `## Response` section | `response_models` |

**The taxonomy's middle row names two plan-specific heading types by
name, and this chunk wires the plan-row fields they feed, not only the
proposal-row ones.** `## Plan review` and `## Code review` sections exist on
plan artifacts, never proposal artifacts, so their presence in the taxonomy
above is Round 6's own signal that the retained-field wiring spans both
schemas `extract.py` emits. `PLAN_COLUMNS`' `plan_review_rounds` and
`code_review_rounds` (`extract.py:92-93`) are retained fields — Part 1 does
not retire them — computed today by `extract_plan_row`'s own heading-count
loop (`_CODE_REVIEW_HEADING_RE`/`_PLAN_REVIEW_HEADING_RE` against every line
carrying a date), the same prose-scraping class `review_rounds` was in before
this chunk. Left unwired, the two halves of this chunk's own acceptance would
contradict each other on a plan artifact: reconciliation (row 6-3) already
covers `dev/plans/` and refuses a post-cutoff `## Plan review`/`## Code
review` section with no matching block, while `extract_plan_row` would keep
reporting a heading count for that same artifact — refusing and still
quietly keeping the prose scraper at once. Rows 6-9 through 6-12 below close
this.

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
"unavailable Git" is. Establishing "carries a status past that cutoff" is
itself only possible through a successful history read, so a target with
**no git at all** cannot satisfy this refusal's own precondition and falls
back to the pre-activation behavior instead (Chunk 5's Activation section
states this in full). The correct audit predicate for Chunk 7 is therefore
broader than "no git": **every existing test that runs this tool's
extractor over any tree** is in scope, because a git-present tree whose
lifecycle acts carry no blocks refuses under this chunk's rule once that
tree is activated — a materially larger set than the git-absent tests alone.
Chunk 7 audits against that predicate.

**The dropped-historical-continuity allowance, made concrete — and a
field-kind split named here rather than left to conflict with row 6-4.**
For an artifact whose relevant **review-pass or response** act predates that
artifact's own activation cutoff, the corresponding event-derived field
(`review_rounds`, reviewer identity/tier, `cross_agent_type_review`,
`response_models`, and — per the taxonomy note above — `plan_review_rounds`/
`code_review_rounds`) is emitted **empty** — not computed from the old
prose-parsing path, not backfilled, not marked "derived/unreliable" (both of
those were the rejected option (b)). Empty is the correct value per the
Decision, not a placeholder for a future backfill this plan does not build.

**"Empty" is the literal string `''`, not `0` or any other falsy stand-in —
named explicitly because a numeric column has two plausible empty
representations and only one is correct.** `review_rounds`,
`plan_review_rounds`, and `code_review_rounds` are `int` today; if this
allowance emitted `0` for an unprovable-cutoff act, that `0` would be
indistinguishable from a genuinely-zero review count, which is exactly the
shape of defect the Decision's own rationale names — "`code_review_rounds`
read 0 on 28 of 38 artifacts from a regex/template mismatch... a frozen
number known to be wrong is worse than no number, because the caveat stays
in the file while the number travels." Emitting `0` here would reproduce
that same travelling-wrong-number shape under a new mechanism. `''` already
has precedent in this exact package for "the field could not be reliably
computed" on a normally-numeric column — `_hour_delta` (`gitmeta.py:127`)
returns `''`, not `0`, when either endpoint is unavailable, and the CSV/`md`
emission paths already carry a mixed-type column through unchanged. `cross_agent_type_review`
(a `bool` today) and `reviewer_agents`/`response_models` (already
`str`, pipe-joined) follow the same rule: `''` for `reviewer_agents`/
`response_models`, and `''` (not `False`) for `cross_agent_type_review`, for
the same reason — `False` reads as "checked and no cross-type review
occurred," which this state does not know.

**Transition-kind fields are the one exception, and it is not new here**:
row 6-4 already states that `days_*`/`hours_*`/`stage_timestamp_reliability`/
`revised` keep their existing header/git-timestamp-derived, quiet-downgrade
computation pre-cutoff, unconditionally — Part 3 does not touch that
historical portion at all, so a pre-cutoff transition never goes empty by
this allowance; it simply keeps computing the way it always has. An earlier
draft of this paragraph listed "transition" alongside review-pass and
response as all going empty, which would have broken the transition-only
fixtures Chunk 7 confirms unaffected (7-5, 7-6) — corrected here so this
paragraph and row 6-4 say the same thing. Post-cutoff acts on the same
artifact are reconciled and refuse-on-mismatch exactly as above; an artifact
can therefore carry an empty `review_rounds` for its pre-cutoff review
passes and a populated one for later passes on the same document, and the
reader must not conflate the two into one silently-partial number.

| # | File | Change |
|---|------|--------|
| 6-1 | `dev/proposals/_template.md`, `dev/plans/_template.md` | Add the literal `cairn-event-v1` marker — worked into the templates' own guidance for how an agent appends an event block at a transition, review pass, or response, so the marker is simultaneously the activation cutoff and the instruction a reader needs to act on it. |
| 6-2 | `templates/core/dev/proposals/_template.md`, `templates/core/dev/plans/_template.md` | The shipped equivalent. Independently must carry the literal marker; not required to be byte-identical to 6-1 (see Scope's "Documentation / doctrine surface" note on why these four paths are not a twin pair in the byte-identical sense). |
| 6-3 | `tools/_lifecycle_metrics/events.py` | Reconciliation: per-artifact, per-kind matching of acts to blocks; `INCOMPLETE` disposition (nonzero exit, explicit reason) on any unmatched act, unmatched block, or unresolvable history (including unavailable Git for a post-activation artifact). |
| 6-4 | `tools/_lifecycle_metrics/extract.py` | Post-activation: `review_rounds`, reviewer identity/tier, `cross_agent_type_review`, `response_models` sourced from reconciled `review-pass`/`response` blocks, not from heading counts or `**Model**:` regex scraping. **Reviewer-identity normalization, pinned**: the grammar's `reviewer` key stores the name as written in the section heading (Chunk 4's literal text), but `reviewer_agents`/`cross_agent_type_review` are existing v1 columns whose semantics depend on a normalized agent token, not a raw heading fragment — `extract.py` already owns that normalization (`_agent_of(h)`, applied today to the heading itself). This chunk applies the same normalization to the block's `reviewer` value before it lands in `reviewer_agents`, so the `a != author` comparison in `cross_agent_type_review` keeps comparing like values and the emitted column shape is unchanged for post-cutoff rows: the block becomes the source, the value shape does not. Pre-activation acts on the same artifact: the corresponding field is empty per the rule above. Transition dates / `days_*` / `hours_*` / `stage_timestamp_reliability` / `revised` sourced from reconciled `transition` blocks post-cutoff; unchanged (still header/git-timestamp-derived, still quiet-downgrade) pre-cutoff, since that is the existing degradation this chunk does not touch for the historical portion. |
| 6-5 | Twins under `templates/modules/default-on/_lifecycle_metrics/` | Same commit as 6-3/6-4. |
| 6-6 | `bootstrap/tests/test_lifecycle_metrics_events.py` | Mandatory red fixtures (Round 6 / R4-E2): a status-only commit with no block → `INCOMPLETE`; a review-only commit with no block → `INCOMPLETE`. Mandatory taxonomy fixture (Round 6 / R4-E1): two review commits with no intervening status change produce **two** review-pass events and `review_rounds == 2`. Pre/post-activation split fixture: one artifact with a review pass before its activation cutoff and one after; the row shows an empty value attributable to the pre-cutoff pass and a populated, reconciled value for the post-cutoff one. |
| 6-7 | `tools/_lifecycle_metrics/__init__.py`, `templates/modules/default-on/_lifecycle_metrics/__init__.py` | Update the "Robust across VCS settings" paragraph (~lines 74-82, as_of 2026-08-20): it currently documents unconditional quiet degradation to `Best-effort` reliability when git is unavailable ("a deliberately quiet failure mode"). This chunk makes that a refusal (`INCOMPLETE`) for a post-activation artifact instead of a quiet downgrade; the docstring must describe the new post-activation behavior, not continue documenting only the contract this chunk reverses. |
| 6-8 | *(process instruction, not a file change)* | From this chunk's own commit onward, whoever performs a lifecycle act on `dev/plans/metrics-events-not-prose.md` appends the matching `cairn-event-v1` block in the same commit that performs the act — discharging, for the one artifact this plan controls, the residual named in this chunk's intro. **Not uniformly "the implementing agent"**: a further status flip on this plan is the implementing agent's own act, but this file's own eventual code review is performed and self-committed by its named reviewer (`AGENTS.md` > Review: "No agent writes or commits a review attributed to another agent" — code review's floor is explicitly not the implementing agent), so the block for that act is that reviewer's to append, not the implementing agent's. This row instructs the act's performer, whoever that is, rather than naming one agent for an act it cannot perform. |
| 6-9 | `tools/_lifecycle_metrics/extract.py` | `extract_plan_row` gains `repo_root: Optional[Path] = None` and `include_git_timestamps: bool = True` parameters, mirroring `extract_proposal_row`'s shape (today it is a pure text function with neither). Post-cutoff: `plan_review_rounds`/`code_review_rounds` are sourced from reconciled `review-pass` blocks on the plan file, not from `_CODE_REVIEW_HEADING_RE`/`_PLAN_REVIEW_HEADING_RE` line-counting. **Classification, not the block's own `tier` field**: a plan's `review-pass` acts come from two distinct heading types sharing one event kind, and the reconciler already inspects the matched section's heading line to confirm the act exists (Round 7 §2 step 4, "requires the matching lifecycle act in the same diff... a `review-pass` block needs the added review section") — this chunk has that reconciled record retain the matched heading line (or an equivalent section-kind tag) so `extract_plan_row` can classify it with the same `_CODE_REVIEW_HEADING_RE`/`_PLAN_REVIEW_HEADING_RE` patterns it already imports, incrementing `code_review_rounds` or `plan_review_rounds` accordingly. This repurposes those two regexes from direct heading-counters into section-kind classifiers of an already-reconciled act; Chunk 1 does not remove them and this row is why. The block's own `tier` key (Internal/External/Security/Code) is left for a future consumer that wants the review's declared independence tier — not used here, because the heading type, not the self-reported tier, is the classifier the reconciler already computed to find the act at all. Pre-cutoff acts on the same plan artifact: `plan_review_rounds`/`code_review_rounds` are `''` (empty), per the pinned representation above — not the old heading-count value. |
| 6-10 | `templates/modules/default-on/_lifecycle_metrics/extract.py` | Twin of 6-9, same commit. |
| 6-11 | `tools/_lifecycle_metrics/extract.py` | `plan_rows()` passes `repo_root=root` through to `extract_plan_row` (mirroring `proposal_rows()`'s existing `repo_root=root` pass-through to `extract_proposal_row`), so the real corpus walk reconciles plan-row acts rather than only unit tests that pass `repo_root` explicitly. Twin: same commit. |
| 6-12 | `bootstrap/tests/test_lifecycle_metrics_events.py` or `bootstrap/tests/test_lifecycle_metrics_config.py` | New fixtures, mirroring 6-6's proposal-row shape for the plan schema: a plan artifact with one `## Plan review` post-cutoff section and no block → `INCOMPLETE`; one `## Code review` post-cutoff section and no block → `INCOMPLETE`; two `## Plan review` sections and one `## Code review` section, no intervening status change, reconciled → `plan_review_rounds == 2`, `code_review_rounds == 1`; a plan artifact with a `## Plan review` pass before its activation cutoff and one after → the pre-cutoff contribution reads `''`, the post-cutoff value is populated and reconciled, matching 6-6's pre/post-activation split fixture for the proposal schema. |

**Acceptance for this chunk**: the four template paths (6-1/6-2) each
independently carry the literal string `cairn-event-v1` **worked into the
templates' own instructional guidance** for how an agent appends an event
block at a transition, review pass, or response — not merely present as a bare
token or inside a fenced example, which would satisfy a literal string match
while leaving an agent no usable instruction; every fixture in 6-6 and 6-12
passes; a report run against a fixture tree containing a deliberately
unreconciled act exits nonzero and names which artifact/commit/kind failed to
reconcile, never a shorter clean series — including a deliberately
unreconciled `## Plan review`/`## Code review` act on a plan artifact, not
only a proposal's `## Review` act; `extract_plan_row`'s `plan_review_rounds`/
`code_review_rounds` are reconciled-block-derived post-cutoff and `''`
pre-cutoff, never the `_CODE_REVIEW_HEADING_RE`/`_PLAN_REVIEW_HEADING_RE`
line count, for every plan row `plan_rows()` emits; the `__init__.py`
docstring (6-7) no longer documents unconditional quiet git-absent
degradation as the only behavior. Because this
chunk's own commit is what first introduces the marker, it lands in the same
commit as the reader and reconciliation logic that can act on it — no chunk
boundary leaves the marker present with no reader behind it.

**And, the property this chunk exists to make checkable — recorded as
evidence of the corpus's real state, not as a gate on other sessions'
conduct (see the disposition above)**: run the real extractor against
Cairn's own `dev/proposals/` and `dev/plans/` corpus at this commit; record
whether it exits successfully and, if not, which artifact/commit/kind fails
to reconcile — not merely that the emitted column set can be diffed. The
gating half of this chunk's own acceptance is narrower: every act *this
plan's own commits* perform, from this commit onward, carries a matching
block and reconciles cleanly (row 6-8). Re-run and recorded again at Chunk
8's evidence step (8-6), since further real acts may land in the corpus
between this commit and that one.

### Chunk 7 — Cross-cutting fixtures and the pre-existing-test audit

Depends on Chunks 1-6 all being present.

| # | File | Change |
|---|------|--------|
| 7-1 | `bootstrap/tests/test_lifecycle_metrics_events.py` | Confirms cross-commit contamination is structurally unrepresentable (the R3-E1 property, re-expressed for the artifact-local design per Round 5 §2): two artifacts transitioned concurrently, one commit path-scoped to the first artifact only, and the assertion that the second artifact's block does not and cannot appear in that commit — because there is no shared file for it to appear in. This is a confirmation test of a structural property, not a vulnerability regression test (there is no longer a vulnerable mechanism to regress); it passes even with `events.py` deleted, since the property is one of git and path-scoped commits, not of the reader's own logic. Writing it is still required (Round 5); it does not itself enforce the property. |
| 7-2 | `bootstrap/tests/test_lifecycle_metrics_events.py` | `recorded_by` fixture: a block carrying a forged or duplicated `recorded_by` value changes no identity, no reconciliation outcome, and no refusal disposition — confirming it stays informational-only per Round 7's explicit bar on it participating in authority or idempotency. |
| 7-3 | `bootstrap/tests/test_reference_scripts.py` | `test_installed_lifecycle_metrics_runs_on_target` (as_of 2026-08-20, the same test Chunk 1 already touched; distinct from `TestVcsRobustness.test_no_git_target_degrades`, addressed separately at 7-5): its `tmp_path` scaffolds `lifecycle-metrics` (so once Chunk 6 lands its installed `dev/proposals/_template.md` carries the marker) but **never runs `git init`** — no `.git` at all, so the extractor cannot prove this artifact is past any cutoff and the act is pre-cutoff by the rule in Chunk 5's Activation section. **This is the one pre-existing test in this audit that genuinely changes**: `review_rounds` is a review-pass-kind field, and pre-cutoff review-pass fields emit empty (never the retired heading-count value) — so `assert row["review_rounds"] == 1` no longer holds and is updated to assert the empty value once Chunk 6 lands. Not a refusal, not a silent hold-over: an explicit, confirmed value change, distinct from 7-5's and 7-6/7-7's true no-op confirmations below, because this is the only audited test asserting a review-pass-kind field's value on a tree whose post-cutoff status cannot be proven. |
| 7-4 | `bootstrap/tests/test_lifecycle_contract.py` | Confirm the corpus-soundness suite (`test_the_live_corpus_is_sound_under_the_p1_contract` and neighbors) still passes against Cairn's own live `dev/proposals/` and `dev/plans/` corpus once the four template paths carry the activation marker — the live corpus itself carries no event blocks yet **except this plan's own `dev/plans/metrics-events-not-prose.md`, which by this point may carry blocks per row 6-8** — so this is a check that adding the marker, plus this plan's own compliant acts, does not perturb anything the corpus-soundness suite reads. This file is also touched by two other proposals opening today (both editing `bootstrap/tests/conftest.py`); this plan does not touch `conftest.py` and has no other point of contact with that concurrent work. |
| 7-5 | `bootstrap/tests/test_reference_scripts.py` | `TestVcsRobustness.test_no_git_target_degrades` (as_of 2026-08-20, lines 445-457) scaffolds a marker-carrying template but never runs `git init` — the same git-absence shape as 7-3, and the same resolution: the refusal Chunk 6 adds presupposes proof of post-activation status that only a history read can supply, and no `.git` forecloses that proof. **Confirmed, not updated to assert `INCOMPLETE`**: `stage_timestamp_reliability == "Best-effort"` keeps holding, and the docstring is updated to state the more precise reason (git-absence forecloses the cutoff proof the new refusal needs) rather than the older, now-imprecise "degrades to Best-effort rather than raising." **A uniqueness claim this row must not repeat**: this is not the only test encoding the git-absent contract — `bootstrap/tests/test_lifecycle_stage_patterns.py::test_t12_a_target_with_no_git_still_degrades_to_best_effort` (7-6) duplicates it deliberately, by that test's own docstring. |
| 7-6 | `bootstrap/tests/test_lifecycle_stage_patterns.py` | `test_t10_public_path_reports_exact_with_populated_hour_deltas` and `test_t12_a_target_with_no_git_still_degrades_to_best_effort` both hand-build their `tmp_path` (`_write_proposal` + `_init_repo`/no repo) with **no `dev/proposals/_template.md` at all** — no marker file exists on disk in either fixture, the plainest case of "missing marker." Per (c), both trees are simply not yet activated: `stage_timestamp_reliability` keeps its existing timestamp-derived computation in both (`Exact` for T10's real four-commit history, `Best-effort` for T12's no-git case). **Confirmed unaffected**; no code or test change. |
| 7-7 | `bootstrap/tests/test_lifecycle_cli.py` | `test_emit_snapshot_creates_indexed_csv`, `test_emit_snapshot_same_day_coalesces_by_index`, `test_snapshot_flag_via_main` all drive the extractor through the `lm_repo` fixture, which creates only a bare `dev/proposals/` directory with one hand-written proposal — no installed template, no `.git`. No marker anywhere in the tree, so (c) applies; none of the three asserts a review-pass-kind field's specific value (they check row count, CSV header shape, and file paths), so the empty-vs-unchanged split above has no observable effect here either way. **Confirmed unaffected**; no code or test change. |
| 7-8 | `bootstrap/tests/test_reference_scripts.py` | `TestVcsRobustness::test_main_branch_target_runs` (~line 458) is the concrete case the Activation section's exclusive-cutoff resolution exists to keep passing: `_scaffold` installs the marker-carrying template, a sample proposal carrying a `## Review` section is written, and `git init` + `add -A` + **one** commit lands both the marker's own introduction and the proposal's review-pass act together. Under the exclusive reading (5-3), that commit is pre-cutoff, so `rows = lm.proposal_rows(tmp_path)  # must not raise` continues to hold with no change. **Confirmed, and named as the regression this plan would otherwise silently depend on** — an inclusive reading would red this test, and nothing before this audit pinned that as a fixture against the real test rather than 5-3's synthetic one alone. |
| 7-9 | `bootstrap/tests/test_lifecycle_metrics_config.py` | `test_emit_snapshot_stays_contained_under_hostile_config` (line 112, as_of 2026-08-20) builds a tree with a real proposal under `dev/proposals/` and calls `emit_snapshot` on it (line 123) — a call path the enumeration below reaches and Chunk 7's own table had not previously named. Disposition confirmed by reading the fixture directly: no installed template (so no marker, so (c) applies), the proposal carries no `## Review` section, and the test asserts only the snapshot path and containment, never a review-pass-kind field's value. **Confirmed unaffected**, same shape as 7-7; no code or test change. |

**The enumeration this row's own audit runs on, recorded so a later pass
re-runs it rather than re-deriving it**:
`grep -rn 'extract_proposal_row\|extract_plan_row\|proposal_rows\|plan_rows\|emit_snapshot' bootstrap/tests/*.py`.
Confirmed against a known-present case before trusting a clean run against
it: this form returns the eight tests this chunk's table names (7-3, 7-5,
7-6 ×2, 7-7 ×3, 7-8, 7-9), so an enumeration that returned fewer would be a
real signal, not a null result to wave past.

**Acceptance for this chunk**: 7-1 and 7-2 pass as new fixtures. 7-4, 7-5,
7-6, 7-7, 7-8, and 7-9 are confirming (not new) passes against the live or
existing-fixture code paths — each one audited under the corrected
predicate ("every existing test that runs the extractor over any tree", not
only the git-absent ones) and found unaffected by Chunks 4-6, for the
reason its own row states, with a docstring/comment update where the row
says so. 7-3 is the one exception in this audit: its `review_rounds`
assertion is updated to expect `''`, and passes against that updated
assertion, not against the pre-Chunk-6 one.

### Chunk 8 — CHANGELOG and the before/after corpus evidence

| # | File | Change |
|---|------|--------|
| 8-1 | `CHANGELOG.md` | Under `## Unreleased`, add a line to the section's **existing, generic `### Changed` heading (`CHANGELOG.md:222`, as_of 2026-08-20)** — not a new subsection. `## Unreleased` (line 41) already carries four subsections before the next `## ` release heading (line 497): `### Changed — Git-native security foundations` (42), `### Added` (60), a bare **`### Changed`** (222), and `### Fixed` (317); the bare one at 222 is the right home. Add one line naming the v1→v2 lifecycle-metrics schema break (eight columns retired) and the new event-emission convention for adopters who already parse the CSV/manifest. |
| 8-6 | *(evidence, not a file change)* | Re-run the extractor against Cairn's own corpus before and after this plan's chunks, diffing the emitted column set — the "Owed at implementation" item the proposal names explicitly, so the diff is recorded rather than assumed. The after-run also records Chunk 6's corpus-wide property — whether the run exits successfully and, if not, which artifact/commit/kind fails to reconcile — as **evidence of the corpus's real state, not a gate on this plan's own completion**: reconciling acts this plan does not control is outside its authority (Chunk 6's disposition, above). What *is* gating: every act this plan's own commits performed on its own artifacts from Chunk 6 onward reconciles cleanly. Recorded in this plan's `## Implementation verification` section, not carried into the plan as a number now. |

**The registration travels with the file, and that is not a style choice.**
The four rows that register `events.py` — the `InstallSpec`, both count pins,
and the AST symbol update — were briefly placed here, in Chunk 8. They now sit
in **Chunk 4 (rows 4-6 through 4-9)**, the commit that first puts
`templates/modules/default-on/_lifecycle_metrics/events.py` on disk. **Rows
8-2 through 8-5 are deliberately absent from this chunk's own numbering as a
result** — not a gap a future sweep should try to close — which is why this
chunk's table runs 8-1 straight to 8-6.

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
  and its AST-baseline `update-symbol` step; Chunk 4's extended vocabulary
  matrix (`bootstrap/tests/test_lifecycle_vocabulary.py`, rows 4-10 through
  4-13); Chunk 6's plan-row wiring fixtures (rows 6-9 through 6-12);
  `bootstrap/tests/test_lifecycle_contract.py`
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
  read-only contract under the extended preview text (4-5); a plan-row smoke
  check confirming `plan_review_rounds`/`code_review_rounds` are
  reconciled-block-derived post-cutoff and `''` pre-cutoff, not the retired
  heading-count regex (rows 6-9 through 6-12).
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
| Divergent / multiply-introduced activation marker refuses | Chunk 5's marker fixtures |
| A **missing** activation marker does not refuse — it resolves to no cutoff, treating every act as pre-cutoff (field-kind-dependent, next two rows) | Chunk 5's marker fixtures; confirmed against real pre-existing fixtures with no template file at all in Chunk 7 (7-6, 7-7) |
| Pre-cutoff (including "cannot prove post-cutoff") **transition**-kind fields keep their existing quiet-degrade computation, unconditionally | Row 6-4 (unchanged, pre-existing behavior); confirmed against `test_no_git_target_degrades`, `test_t10_public_path_reports_exact_with_populated_hour_deltas`, `test_t12_a_target_with_no_git_still_degrades_to_best_effort` (7-5, 7-6) |
| Pre-cutoff (including "cannot prove post-cutoff") **review-pass/response**-kind fields emit empty, never the retired heading-count/regex value | Row 6-4; the one place this is a real, observable change against a pre-existing test: `test_installed_lifecycle_metrics_runs_on_target`'s `review_rounds` assertion (7-3) |
| An act committed in the same diff as the marker's own introduction is pre-cutoff, by the same rule as a missing marker | Chunk 5's boundary fixture; confirmed against the real `test_main_branch_target_runs` in Chunk 7 (7-8) — that test asserts no review-pass-kind value, so it holds with no change even though the act's `review_rounds` is itself empty |
| A status-only commit with no block is loud `INCOMPLETE` | Chunk 6's mandatory red fixture |
| A review-only commit with no block is loud `INCOMPLETE` | Chunk 6's mandatory red fixture |
| Two review commits, no intervening status change, yield two review-pass events | Chunk 6's mandatory taxonomy fixture |
| Pre-activation acts emit empty, not prose-derived, not backfilled | Chunk 6's pre/post-activation split fixture |
| Cross-commit contamination is structurally unrepresentable | Chunk 7's confirmation fixture |
| `recorded_by` never affects identity, reconciliation, or refusal | Chunk 7's fixture |
| `next --to` stays read-only under the extended preview | Chunk 4's and Chunk 7's regressions against `test_lifecycle_contract.py` |
| Unavailable Git on a **provably** post-activation artifact refuses the row, not a quiet downgrade | Chunk 6's reconciliation logic; no pre-existing test currently reaches this state (every git-absent fixture Chunk 7 audited also lacks a way to prove post-activation status, so each falls back to the pre-cutoff, field-kind-dependent disposition instead — see the two rows above) |
| Git entirely absent forecloses proving post-activation status, so the tree is treated as pre-cutoff rather than refused | Chunk 5's Activation section; confirmed against `test_no_git_target_degrades` (7-5, unaffected — transition field), `test_installed_lifecycle_metrics_runs_on_target` (7-3, the one real change — review-pass field), and `test_t12_a_target_with_no_git_still_degrades_to_best_effort` (7-6, unaffected — transition field), all `test_reference_scripts.py` except the last |
| `plan_review_rounds`/`code_review_rounds` (`PLAN_COLUMNS`) are wired to reconciled `review-pass` blocks, classified by matched heading (`## Plan review` vs. `## Code review`), not left computing the retired heading-count regex | Rows 6-9 through 6-12; the taxonomy note in Chunk 6's intro naming both `PLAN_COLUMNS` fields as in scope |
| `events.py`'s `from_state`/`to_state` bound is checked against the real runtime vocabulary (`PROPOSAL_STATES`/`PLAN_STATES`), sourced through `extract.py`'s existing contained loader and passed in as a parameter — never a second, locally-declared copy | Rows 4-10 through 4-13; `bootstrap/tests/test_lifecycle_vocabulary.py`'s extended `_AUDITED_CONSUMER_SOURCES` and `METRICS_SPEC` matrix |
| The reconciler's act list and its block list are read from the same committed history (HEAD), so an uncommitted lifecycle act is invisible to both sides and is neither refused nor counted until committed | Chunk 5's act-list paragraph and its new 5-3 fixture |
| A root (zero-parent) commit is attributed normally — its empty parent sequence trivially satisfies the prefix check, and step 5's multi-parent refusal does not extend to it | Chunk 5's root-commit paragraph and its new 5-3 fixture |
| A pre-cutoff or unprovable-cutoff review-pass/response field emits the literal `''`, never `0`/`False`/any other falsy stand-in that could be mistaken for a computed value | Chunk 6's "Empty is the literal string" paragraph; rows 6-9/6-12, 7-3 |

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

* `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0`
  — the override is required as of 2026-08-20: `bootstrap/tests/conftest.py`'s
  broad-run guard refuses an unscoped full-suite invocation (`pytest.UsageError`,
  exit 4) without it, and `AGENTS.md`'s own Boundary B text now carries the same
  requirement.
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

## Plan review -- Claude Opus 5 (Internal plan reviewer) -- 2026-08-20 (round 3)

Reviewed commit: b9a032428515b4d11a9093b867e476bd9780b1dc
Target: the whole operative plan (Scope through Verification; Chunks 1-9, the sequence revision, Acceptance criteria, Author-accounting), plus the round-1/round-2 findings and Responses, against the source proposal's Round 7 and Decision
Prior findings: EPR-01, EPR-02, EPR-03, EPR-04
Assurance path: high-assurance
**Tier**: Internal
**Findings**: raised

### Verdict

**REVISE.** All four prior findings are genuinely closed — I re-ran the
instruments rather than taking the Responses' word for it (see Coverage). The
plan's factual claims about the live tree are in unusually good shape: I checked
sixteen of them and every one held. Three blocking defects remain, all in the
same region — the activation boundary and what it does to code and tests this
plan does not name. Each one, left as written, leaves a chunk's acceptance
either unsatisfiable or self-contradictory.

### Prior findings — closure, verified

* **EPR-01 (AST command cannot run) — CLOSED.** `update-symbol --help` confirms
  the real signature: `--baseline` and `--expect-old` required, `--known-new`
  and `--dry-run` optional, `symbol` then `modules...` positional. Row 4-9's
  invocation matches, and its four ordered steps match
  `bootstrap/AST_BASELINE_RUNBOOK.md`'s steps 1-4. `_UPDATE_ALLOWLIST` does
  contain `_MODULE_MAPPINGS: "Assign"`, so the self-service claim holds.
* **EPR-02 (no bridge across Chunks 4-6) — CLOSED as scoped.** Chunk 4's table
  carries no marker rows; 6-1/6-2 land the marker in the same commit as 6-3/6-4.
  The window the finding named is gone. The window on the *far* side of the
  cutoff is not — that is EPR-07 below, a new finding rather than a reopening.
* **EPR-03 (stale `8-2` references) — CLOSED.** A sweep of the operative text
  (everything above the first appended review section) for `8-[2-5]`,
  `4-1[0-9]`, `6-[89]` and `Chunk 8` returns no stale row reference; the row-id
  set runs 1-1..1-16, 2-1..2-3, 3-1..3-4, 4-1..4-9, 5-1..5-3, 6-1..6-7,
  7-1..7-5 with no gaps or duplicates. Worth recording for the next sweeper:
  every `8-[2-5]` hit in this file is the substring of `as_of 2026-08-20`, so
  that pattern is nearly all false positive and a future pass should anchor on
  `\|\s*8-\d` or `row 8-\d` instead.
* **EPR-04 (runbook's post-apply full suite) — CLOSED.** Both Step 4 commands
  are quoted in Chunk 4's acceptance and both outcomes are required at that
  commit. I diffed the quoted block against the runbook's own: identical,
  including `PYTHONDONTWRITEBYTECODE=1`. The round-1 softening ("recommends") is
  withdrawn in the round-2 Response.

### Findings

#### EPR-05 — BLOCKING: the activation rule has two unresolved edges, and each decides what a required fixture asserts

**(a) A tree with no marker at all: the plan says both things.** Chunk 5
reproduces Round 7 §4 — "Missing, divergent (the pair disagrees), or
multiply-introduced (removed and re-added) markers refuse" — and row 5-3 makes
"missing ... markers each refuse" a **mandatory fixture**. Row 7-5 then says the
opposite for the same state: "for a fixture proposal that predates activation
(**or an installation with no activation marker at all**), the existing
quiet-degrade behavior is unchanged, and the test should say so explicitly."
A fixture asserting refusal and a test asserting quiet degradation cannot both
describe an unmarked tree.

This is not a wording tidy-up, because the reading decides an adopter-facing
outcome the plan never declares. `lifecycle-metrics` is **default-on**. Every
adopter tree that installed it before this change has a
`dev/proposals/_template.md` with no `cairn-event-v1` token. Under Chunk 5's
reading, `python tools/lifecycle_metrics.py` refuses in every one of those trees
from the moment they take the engine update, until they separately take the
template update — a break materially larger than the eight retired columns, and
one the `**Contract expansion**` declaration (currently "adopter-facing CLI
surface", scoped to `--backfill-from`) does not cover. Under 7-5's reading, an
unmarked tree is simply pre-activation everywhere and behaves as today, which is
the benign outcome and is what "before its cutoff, an empty series is
**correct**" reads like in Round 7 §4. I lean to the second, but the plan must
state which, because Chunk 5 currently commits to the first.

**(b) Is an act in the marker's own commit pre- or post-cutoff?** Chunk 6 says
"from that commit on" (inclusive); nothing else in the plan resolves it, and
neither Chunk 5's fixture list nor Chunk 6's pre/post split fixture ("one
artifact with a review pass before its activation cutoff and one after")
contains the at-the-cutoff case. This is reachable today, not hypothetical:
`bootstrap/tests/test_reference_scripts.py::TestVcsRobustness::test_main_branch_target_runs`
(~line 460) scaffolds `lifecycle-metrics`, writes a proposal, then `git init` +
`git add -A` + **one** commit — so the marker-bearing installed template and the
proposal's opening act arrive in the same commit. Inclusive means that act is
post-cutoff with no block, so `proposal_rows` refuses where the test says "must
not raise"; exclusive means it is pre-cutoff and empty. Decide it, name it in
Chunk 5's algorithm block, and add the boundary case to 5-3's fixtures.

#### EPR-06 — BLOCKING: Chunk 7's audit uses the wrong predicate, and misses at least five tests

Chunk 6 states the audit's scope as "Chunk 7 audits every existing test that
currently runs this tool **without a git-initialized scratch tree**, because
this is where their assumptions break." That predicate is too narrow by the
plan's own contract. A *git-present* tree whose lifecycle acts carry no event
blocks also refuses under 6-3 — that is the whole point of fail-closed
reconciliation. The correct predicate is "every existing test that runs the
extractor over any tree."

Under the correct predicate, Chunk 7's table (7-3, 7-5, both in
`test_reference_scripts.py`) is incomplete. Enumerated by grepping
`proposal_rows|plan_rows|emit_snapshot` across `bootstrap/tests/`:

* `bootstrap/tests/test_lifecycle_stage_patterns.py::test_t10_public_path_reports_exact_with_populated_hour_deltas`
  (line 647) — builds a synthetic **four-commit** history whose subjects drive
  open → reviewed → revised → decision, then asserts
  `stage_timestamp_reliability == "Exact"` and populated `hours_*`. Four real
  transitions, zero event blocks.
* `bootstrap/tests/test_lifecycle_stage_patterns.py::test_t12_a_target_with_no_git_still_degrades_to_best_effort`
  (line 730) — asserts `stage_timestamp_reliability == "Best-effort"` and three
  empty `hours_*` columns with no `.git`. **This falsifies a uniqueness claim
  the plan makes in row 7-5**: `TestVcsRobustness.test_no_git_target_degrades`
  is *not* "the test that actually encodes the git-absent quiet-degradation
  contract Chunk 6 reverses" — T12 encodes it too, by name and by assertion, in
  a file this plan never touches. T12's own docstring says it "deliberately
  duplicates the guarantee `bootstrap/tests/test_reference_scripts.py` already
  holds", so the duplication is documented in the tree and was findable.
* `bootstrap/tests/test_reference_scripts.py::TestVcsRobustness::test_main_branch_target_runs`
  (~line 460) — the single-commit scaffolded tree from EPR-05(b);
  `rows = lm.proposal_rows(tmp_path)  # must not raise`.
* `bootstrap/tests/test_lifecycle_cli.py` — `test_emit_snapshot_creates_indexed_csv`,
  `test_emit_snapshot_same_day_coalesces_by_index`, `test_snapshot_flag_via_main`
  (lines 471-522) all drive the extractor through the `lm_repo` fixture (a
  tmp root, no `.git`, no installed template).

Boundary B's full suite would eventually catch these, but Chunk 7 is *named* as
the audit and its acceptance criterion is "7-1, 7-2, 7-3, and 7-5 pass" — a
criterion that cannot see a test the enumeration omitted. Fix the predicate and
extend the table; the disposition of each test then follows from EPR-05.

#### EPR-07 — BLOCKING: from Chunk 6 onward the obligation binds sessions this plan does not control, and row 8-6's criterion depends on their compliance

Chunk 6's intro rejects the alternative bridge because it "would bind whoever
commits a lifecycle artifact in this tree during that window, including in a
concurrent session with no reason to know a plan's own chunk boundaries changed
what an event-worthy edit requires", and concludes: "Landing the marker and the
reader in the same commit is the option that **depends on no one else's
session**." That conclusion is true for the Chunks 4-6 window and false
afterwards. From Chunk 6's commit on, every `**Status**` flip, review section
and Response section committed anywhere in `dev/proposals/` or `dev/plans/` —
by any session — is a post-cutoff act that must carry a block or the extractor
refuses globally (Chunk 6's own acceptance: the report "exits nonzero and names
which artifact/commit/kind failed to reconcile").

Row 8-6 then makes that an acceptance criterion for *this* plan: the after-run
"must also satisfy Chunk 6's own acceptance criterion: it exits successfully and
accounts for every act recorded in the corpus after the activation cutoff." The
board at this commit shows two sibling plans active — `full-suite-interception`
(`awaiting-plan-review`) and `suite-run-diagnostics` (`revising-plan`) — each of
which will take further review passes and status flips during an eight-chunk
implementation. One block-less act in either, and row 8-6 cannot be satisfied by
this plan's agent through no act of theirs.

The plan is also silent on the artifacts it *does* control. Between Chunk 6 and
archive, this plan's own file takes a code-review pass and several status flips,
all post-cutoff. Nothing instructs the implementing agent to append blocks to
them.

Name the disposition. Any of these discharges it; the choice is the author's,
and none of them narrows accepted scope: (i) instruct the implementing agent to
append the literal blocks to every lifecycle act it performs on its own
artifacts from Chunk 6 onward, and state a residual for concurrent sessions;
(ii) scope row 8-6's criterion to acts this plan's own commits produced, with
the corpus-wide run recorded as evidence rather than as a gate; (iii) obtain a
Maintainer announcement of the obligation at the Chunk 6 commit. What is not
available is leaving the criterion as a gate on other people's sessions while
the plan's own reasoning says binding them is not this plan's to do.

#### EPR-08 — NON-BLOCKING: row 8-1's premise about `## Unreleased` is false, and its instruction would create a duplicate heading

Row 8-1 says to "open a new `### Changed` subsection — the section currently has
only `### Changed — Git-native security foundations` and `### Added` (as_of
2026-08-20; **there is no generic `### Changed` to file this under**)". At the
reviewed commit, `## Unreleased` (CHANGELOG.md:41) carries four subsections:
`### Changed — Git-native security foundations` (42), `### Added` (60),
**`### Changed` (222)**, and `### Fixed` (317); the next `## ` is at line 497.
I checked this against `git show b9a0324:CHANGELOG.md`, so it was already false
when written, not overtaken by a concurrent commit. Following the row as written
adds a third `### Changed` inside one release section, exactly duplicating the
existing one. File the line under CHANGELOG.md:222 instead.

#### EPR-09 — NON-BLOCKING: the sibling-guard seam is flagged for Chunk 4 but not for this plan's own Boundary B, and the sibling does not in fact owe the runbook fix

Two halves.

**The Verification section still names the bare command.** `## Verification`
lists `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` as
Boundary B's first command with no override and no note — the same invocation
`full-suite-interception`'s Chunk A1 refuses (`pytest.UsageError`, exit 4, on a
cleanly-collected session spanning more than 40 distinct test files unless
`CAIRN_FULL_SUITE=1`). The plan flags this seam carefully for Chunk 4's runbook
step and then leaves its own integration evidence exposed to it. Mitigating:
that sibling's Chunk B1 appends a corrective sentence to `AGENTS.md`'s
Verification-boundaries text, so an implementer re-reading `AGENTS.md` at
Boundary B time is told; and exit 4 is loud. Hence non-blocking. Still worth the
one sentence, since the plan's own text warns that "a run that comes back exit 4
with a refusal message has been refused, not passed."

**The attribution is wrong.** The round-2 Response says the sibling "owes the
runbook an update". Reading that plan: `bootstrap/AST_BASELINE_RUNBOOK.md:126`
appears under a section headed "Live commands the guard breaks beyond AGENTS.md's
own sentence — **flagged, not authorized**", and no chunk row in that plan edits
the runbook. So the fix is recommended to the Maintainer, not owed by that plan.
Write the workaround as the standing answer rather than as a stopgap until
someone else lands something.

#### EPR-10 — NON-BLOCKING: Chunk 1's `snapshot_event=backfill` acceptance clause cannot fail

Chunk 1's acceptance ends "and an existing snapshot file containing
`snapshot_event=backfill` still reads without error", and the paragraph above it
reasons that "the reader must keep tolerating the value on input". There is no
such reader. Persisted snapshots are write-only: `grep -rn 'csv.DictReader|csv.reader'`
over `tools/` and `scripts/` returns nothing, and `snapshot.py`'s only read of
the snapshot directory is `_next_snapshot_index`, which reads filenames, not
rows. I confirmed the instrument could match before trusting the absence — the
same grep form finds `csv.writer` at `tools/_lifecycle_metrics/report.py:35`.
The `<release>-rollup.csv` entry in `output_manifest()` is documentation of an
out-of-core artifact; nothing produces or consumes it.

Keep the conservative instinct — do not delete `backfill` from any accepted-value
set — but either drop the clause or replace it with something that can fail (for
instance: the string `backfill` still appears in whatever accepted-value
constant survives 1-10, asserted by name).

#### EPR-11 — NON-BLOCKING: row 6-4 wires `reviewer_agents` / `cross_agent_type_review` to a block value of a different shape

The grammar defines `reviewer` as "reviewer name **as written in the section
heading**". Today `extract.py` does not use the heading as written: it derives
`reviewer_agents` via `_agent_of(h)` and computes
`cross_agent_type_review = any(a and author and a != author for a in reviewer_agents)`
(lines 169-178) — an identity comparison against the header `author` token. Row
6-4 moves both to the block without saying which value lands in the column. If
the raw heading fragment is stored, `reviewer_agents`' emitted values change
shape for every post-cutoff pass, and the `!= author` comparison silently stops
being able to return `False`. Pin it in 6-4: either `reviewer` carries the
normalized agent token, or the reader applies `_agent_of`-equivalent
normalization on read. Note this is a v2-schema value change beyond the eight
retired columns if left as the raw fragment.

#### EPR-12 — NON-BLOCKING: two small ones

* **New shipped `.py` files need the SPDX header.**
  `test_notice_install.py::test_every_template_py_source_carries_spdx_header`
  and `::test_every_self_hosted_twin_carries_spdx_header` require
  `SPDX-License-Identifier: MIT` within the first four lines of every
  manifest-sourced `templates/**/*.py` and its self-hosted twin. Rows 4-1/4-2
  create two such files and never say so. Chunk 4's focused check runs
  `test_notice_install.py`, so the failure is loud rather than silent — but it
  belongs in the row, next to the other registration obligations.
* **Chunk 8's row ids jump 8-1 → 8-6.** A leftover from the registration move.
  Harmless, but the round-1 Response claimed a full continuity sweep of `4-[0-9]`
  and `6-[0-9]`; the sweep never covered `8-[0-9]`.

### What I tested that held

Reported because a defect-only review tells the author nothing about which
claims were exercised. Every one of these I ran against the live tree:

* `PROPOSAL_COLUMNS` has exactly **30** entries and all eight retirement targets
  are present, so 1-8's "22 after" arithmetic is right (and it correctly says to
  re-derive).
* `test_templates_py_count_is_pinned` pins **52** (line ~376);
  `test_manifest_has_the_expected_py_source_count` pins **56** (line 74). One
  source installed to one destination moves them to 53 and 57 — and the first
  pin's own message confirms the two "must not be made to agree", which 4-7/4-8
  respects.
* `scan_targets()` derives from `_MODULE_MAPPINGS`, so 4-6's registration alone
  makes `events.py` a release-scan target — 4-7's claim that
  `test_every_templates_py_on_disk_is_release_scanned` passes "once this chunk's
  own registration lands" is correct, and the two tests really do have
  independent oracles (one manifest-derived, one on-disk).
* `_gate_manifest._frozen_files()` discovers by glob over
  `templates/modules/**/*.py`, so `events.py` becomes gate-frozen automatically
  — no manifest row is missing, and the Chunk 9 fence is the right and only
  handling. `templates/skills/**` is genuinely outside that glob, as 4-3 says.
* `_MODULE_MAPPINGS` carries exactly **nine** `_lifecycle_metrics/` rows (lines
  749-766) and the neighbouring comment does say "the nine package files install
  verbatim" (line 746). 4-6's citation and its comment edit are both accurate.
* `_self_hosted_twins()` is presence-derived from `install_manifest()`, so the
  Author-accounting invariant is right that the `events.py` pair becomes visible
  to the byte-identity test from Chunk 4's own commit.
* `resolve_slot_merge` returns a non-`None` merged text only for `inserted`,
  which requires `_slot_is_empty(body)`. Cairn's filled slot resolves
  `customized`/`conflict`, both writing nothing. 2-2's hand-edit justification
  holds exactly as stated.
* **The wrapped-phrase hazard, tested with the plan's own instrument.**
  `re.search(r'finding\s+severities', ...)` finds the occurrence in
  `dev/agent_collaboration.md` that a single-line grep misses — the text really
  is `finding\nseverities.` inside the slot block. It also finds **2** in each
  of the two module docs (matching "two locations in each file") and **0** in
  `templates/core/dev/agent_collaboration.md` (matching the exclusion). The
  acceptance criterion at Chunk 2 is a real instrument, and I confirmed it
  against a known-present case before trusting it.
* The two `_lifecycle_metrics/__init__.py` copies are byte-identical (1-9's
  claim), and every docstring line citation lands: "finding severities" at 17,
  "review-yield" at 18, the `total_findings`/`findings_p*` reliability bullets
  at 67-69, "Robust across VCS settings" with "a deliberately quiet failure
  mode" at 74-82.
* `dev/modules/lifecycle-metrics.md` vs the shipped copy differs **only** by
  `{{metrics_command}}` substitution (4 hunks, all token) — the "differ only by
  token substitution" claim is exact.
* `test_every_subcommand_is_read_only` is at line 172; the `_git` helper is at
  ~line 68; `test_installed_lifecycle_metrics_runs_on_target` at 277-295 with
  the `total_findings == 2` / `findings_p1 == 1` assertions;
  `TestVcsRobustness.test_no_git_target_degrades` at 445-457 with the
  `Best-effort` assertion; the git-init pattern at ~469. All five citations hold.
* The backfill inventory is right: `cfg.backfill_max_days == 14` at
  `test_lifecycle_metrics_config.py:61` is the only test exercising the mode,
  and every other `backfill` hit in `bootstrap/tests/` is lockfile-provenance —
  the name-collision warning is accurate.
* **The template-parsing hazard I went looking for is already closed.**
  `_iter_corpus_files` excludes `_template.md` by name
  (`extract.py:114`), so the marker and the worked example blocks 6-1 adds to
  `dev/proposals/_template.md` are never parsed as real events by the extractor.
  Nothing in the plan claims this, and it is the kind of thing that would have
  bitten at Chunk 6.
* `python scripts/claim_check.py dev/plans/metrics-events-not-prose.md` — OK, no
  flags; the three forward-referenced paths resolve through the `Proposed paths:`
  declaration.
* `python tools/lifecycle_planner.py board --compact` shows the row `valid`,
  `awaiting-plan-review`, owner `plan-reviewer`.
* Chunk 3's acceptance already avoids the cannot-fail trap on its own: it says
  outright that byte-preservation is pre-existing behavior and names the
  distinguishability property as the thing the chunk exists to establish. That
  is the right shape and I have no finding on it.

### Sharpening

None. Nothing in this pass narrows what the plan will deliver.
**Scope delta**: preserved.

### Coverage

Read: `AGENTS.md` in full; `dev/plans/_template.md`'s review-basis and
scope-delta doctrine (~lines 400-470); the complete plan including both prior
External reviews and both Responses; the source proposal's Round 7 (§§1-5) and
`## Decision`; `bootstrap/AST_BASELINE_RUNBOOK.md` in full; the operative
sections of both sibling plans (`full-suite-interception`'s Chunk A/B tables and
its "Live commands the guard breaks" section; `suite-run-diagnostics`'s scope
and conftest rows).

Inspected in the live tree: `tools/_lifecycle_metrics/{extract,snapshot,cli,config,gitmeta}.py`;
`bootstrap/_scaffold/config.py`'s `_MODULE_MAPPINGS` and `slotmerge.py`;
`bootstrap/security_check.py`'s `scan_targets`/`ALLOWLIST`;
`bootstrap/tests/{_ast_attest,_gate_manifest}.py`;
`bootstrap/tests/test_{security_lint,notice_install,reference_scripts,lifecycle_contract,lifecycle_stage_patterns,lifecycle_cli}.py`;
`CHANGELOG.md`; `docs/glossary.md`; `dev/agent_collaboration.md`; both
`lifecycle-metrics.md` copies.

Ran: `_ast_attest.py update-symbol --help`; `scripts/claim_check.py` on this
plan; `tools/lifecycle_planner.py board --compact`; targeted `python3 -c`
regex/AST-free probes for the wrapped-phrase case, the column count, the twin
diffs, and the plan's own row-id continuity; `git show b9a0324:CHANGELOG.md`.

Did **not** run: the full suite (no implementation exists, and the brief reserves
verification for the spawner), `scripts/quality_gate.py`, `scripts/check_cairn.py`,
any pytest node, or any baseline mutation. Did not re-read the source proposal's
superseded Rounds 1-6 except where a Round 7 or plan claim cited them (Round 5's
corrected inventory, Round 6's taxonomy). Did not review `tools/lifecycle.py` or
the pilot-event ledger, both of which the plan places out of scope and which I
confirmed no chunk touches.

**Status**: `awaiting-plan-review` -> `revising-plan`.

## Response to plan review -- Claude Sonnet 5 (author) -- 2026-08-20 (round 3)

**Model**: Claude Sonnet 5

**All three blocking findings and all five non-blocking findings accepted;
all folded into the plan's own operative cells, not answered here.** The
Maintainer decided the first blocking finding's core question directly
(quoted below); the remaining sub-question inside it, and both other
blocking findings, required an author disposition, made and reasoned in the
cells themselves rather than only in this table.

| Finding | Disposition | Where addressed |
|---|---|---|
| EPR-05(a) (BLOCKING) — the plan states two contradictory dispositions for a tree with no activation marker | ACCEPTED — decided by the Maintainer, quoted verbatim: **"I think (c) is right."** | Chunk 5's Activation section, new "A marker path can be wrong, or it can simply not exist yet" and "What (c) concedes" paragraphs (divergent/multiply-introduced still refuse; missing does not, and treats every act as pre-cutoff); row 5-3's fixture list; row 7-6/7-7 (confirmed against the real fixtures that carry no marker at all); Author-accounting invariants table (two new rows replacing the single wrong one) |
| EPR-05(b) (BLOCKING) — is an act in the marker's own introducing commit pre- or post-cutoff? | ACCEPTED, resolved **exclusive** (the introducing commit itself is pre-cutoff) — this plan's own disposition, reasoned in the cell rather than asserted | Chunk 5's Activation section, "The marker's own introducing commit is pre-cutoff, not post-cutoff" paragraph; Chunk 6's intro (the "strictly after" correction); row 5-3 (new boundary fixture); row 7-8 (confirmed against the real `test_main_branch_target_runs`, the concrete case this resolution exists to keep passing) |
| EPR-06 (BLOCKING) — Chunk 7's audit uses the wrong predicate and misses at least five tests | ACCEPTED | Chunk 6's fail-closed-measurement paragraph (predicate corrected to "every existing test that runs the extractor over any tree"); Chunk 7's table extended with rows 7-6 (T10/T12), 7-7 (the three `lm_repo` tests), 7-8 (`test_main_branch_target_runs`), and 7-3/7-5 rewritten from "decide which" to confirmed dispositions; Chunk 7's acceptance line. **One of the five turned out to be a real change, not a confirmation** — see the note below. |
| EPR-07 (BLOCKING) — the obligation binds sessions this plan does not control, and row 8-6 depends on their compliance | ACCEPTED, disposition (i)+(ii) combined: this plan's own future acts carry blocks; the corpus-wide run is evidence, not a gate on other sessions | Chunk 6's intro, new "That 'depends on no one else's session' claim holds only for the Chunks 4-6 window" paragraph; new row 6-8 (process instruction: append blocks to this plan's own future acts); Chunk 6's acceptance corpus-check paragraph (evidence, not gate); row 8-6 (same scoping); row 7-4 (notes this plan's own file may itself carry blocks by that point) |
| EPR-08 (NON-BLOCKING) — row 8-1's premise about `## Unreleased` is false | ACCEPTED — confirmed directly: `## Unreleased` at line 41, the bare `### Changed` at line 222, next `## ` at line 497 | Row 8-1, rewritten to file under the existing heading at `CHANGELOG.md:222` instead of opening a duplicate |
| EPR-09 (NON-BLOCKING) — the sibling-guard seam is unflagged for this plan's own Boundary B, and the attribution to the sibling plan is wrong | ACCEPTED, both halves | `## Verification`'s Boundary B command list (now `CAIRN_FULL_SUITE=1`-prefixed, with the reason stated); Chunk 4's "A hazard for whoever runs this" paragraph (rewritten: the guard has already landed as of 2026-08-20, confirmed against `bootstrap/tests/conftest.py`; the runbook fix is "flagged, not authorized" for the sibling plan, confirmed by reading that plan directly, not owed by its agent) |
| EPR-10 (NON-BLOCKING) — Chunk 1's `snapshot_event=backfill` acceptance clause cannot fail | ACCEPTED, clause dropped and the paragraph's reasoning corrected | Chunk 1, "A correction to this section's own earlier reasoning" paragraph (no reader parses persisted snapshot CSVs at all, confirmed by the same grep the reviewer ran); Chunk 1's acceptance line (clause removed) |
| EPR-11 (NON-BLOCKING) — row 6-4 wires `reviewer_agents`/`cross_agent_type_review` to a block value of a different shape | ACCEPTED | Row 6-4, new "Reviewer-identity normalization, pinned" sentence: the block's `reviewer` value is normalized via the same `_agent_of`-equivalent logic `extract.py` already applies to the heading, before it lands in `reviewer_agents` |
| EPR-12 (NON-BLOCKING) — two small ones (SPDX headers; Chunk 8's row-id jump) | ACCEPTED, both | Rows 4-1/4-2 (SPDX-header requirement named); Chunk 8's "registration travels with the file" paragraph (explicit note that rows 8-2 through 8-5 are deliberately absent) |

**One correction this round's own analysis produced, beyond what any finding
asked for — reported per this task's brief rather than left for a future
round to rediscover.** Resolving EPR-06 required working out, field by
field, what "pre-cutoff" actually emits, and that turned up two things:

1. **`test_installed_lifecycle_metrics_runs_on_target` genuinely changes.**
   Of the five tests EPR-06 named, four are confirmed unaffected (they touch
   only transition-kind fields, which keep their existing quiet-degrade
   computation unconditionally pre-cutoff, or touch no review-pass-kind
   field's value at all). The fifth asserts `review_rounds == 1` on a tree
   whose post-cutoff status cannot be proven (marker present via scaffold,
   no `.git`). Review-pass-kind fields emit **empty**, not the retired
   heading-count value, for any act that cannot be proven post-cutoff — the
   Decision is explicit that the old prose-parsing path is retired outright,
   not merely superseded once a cutoff exists. That assertion is updated
   (row 7-3), not left as a false confirmation.
2. **A pre-existing internal contradiction, not raised by any finding**:
   the "dropped-historical-continuity allowance, made concrete" paragraph
   (Chunk 6) said pre-cutoff `transition` acts also emit empty, while row
   6-4 — two paragraphs later in the same chunk — said transition fields
   keep their existing quiet-degrade computation, unconditionally, pre-cutoff.
   Those cannot both be true; row 6-4's reading is the one four of the five
   audited tests already depend on (`stage_timestamp_reliability` staying
   `Exact`/`Best-effort`, never empty), so the allowance paragraph is
   corrected to match row 6-4 rather than the reverse.

**What I believe may still be wrong, flagged rather than deferred, per this
task's own brief.** The exclusive reading of EPR-05(b) (the marker's own
introducing commit is pre-cutoff) and the "git-absent forecloses proof, so
treat as pre-cutoff" resolution for git-absence are both **this plan's own
inferences**, not something the Maintainer's quoted decision or the source
proposal's Round 7 text states directly. I am confident in the reasoning —
both are the only readings that keep the concrete pre-existing tests this
plan does not otherwise touch (`test_main_branch_target_runs`,
`test_no_git_target_degrades`, T10, T12) passing without an unrelated scope
expansion — but they are new design decisions this round makes, not findings
this round merely closes, and a future round should treat them as such
rather than as already-settled Round 7 contract.

**Searches confirmed against a known-present case, per this task's
instrument-confirmation rule.** (1) `_scaffold(tmp_path, ["lifecycle-metrics"])`
installs `dev/proposals/_template.md` unconditionally — confirmed by reading
`bootstrap/_scaffold/config.py`'s `_CORE_MAPPINGS` (line 555), which installs
"like `AGENTS.md`" regardless of the module list, not by trusting the
absence of a per-module gate. (2) The `lm_repo` fixture in
`test_lifecycle_cli.py` installs no template — confirmed by reading the
fixture body (lines 459-468) directly, not inferred from the reviewer's own
claim. (3) `grep -rn 'csv.DictReader|csv.reader' tools/ scripts/` returns
nothing (EPR-10) — confirmed the pattern could match by finding
`csv.writer` at `tools/_lifecycle_metrics/report.py:35` with the same
grep form before trusting the absence. (4) The CHANGELOG line citations
(41, 60, 222, 317, 497) — read directly via `sed -n`, not carried forward
from the review's own citation.

**Status**: `revising-plan` -> `awaiting-plan-review`.

## Plan review -- Claude Opus 5 (Internal plan reviewer) -- 2026-08-20 (round 4)

Reviewed commit: 6c517db66e7276fb54694afac6a4b4b52386532a
Target: the whole operative plan (Scope through Verification; Chunks 1-9, the sequence revision, Acceptance criteria, Author-accounting), the three prior review sections and their Responses, and the two dispositions the round-3 Response flagged as its own inferences -- read against the source proposal's Round 6 taxonomy, Round 7 §§1-5, and the Decision
Prior findings: EPR-01, EPR-02, EPR-03, EPR-04, EPR-05, EPR-06, EPR-07, EPR-08, EPR-09, EPR-10, EPR-11, EPR-12
Assurance path: high-assurance
**Tier**: Internal
**Findings**: raised

### Verdict

**REVISE.** All twelve prior findings are genuinely closed, and I re-ran the
instruments rather than reading the Responses (see "Prior findings" and
"What I tested that held"). **Both dispositions the round-3 Response flagged as
its own inference are correct**, and I say so with the checks that establish it
below, so round 5 need not re-derive them.

Three blocking defects remain. None is a reopening of a prior finding; all three
are in the region the prior rounds did not reach, because every round so far has
read Part 3 through the **proposal**-row schema. The plan's own Scope says it
wires "every retained event-derived field to exactly one event kind", and Chunk 6
reproduces a taxonomy that names `## Plan review` and `## Code review` sections
as review-pass acts -- but no chunk touches the plan-row schema, no chunk names
where the grammar's mandatory status bound reads its vocabulary, and no chunk
says which side of the tree (working copy or history) supplies the act list the
reconciler matches against. Each one, left as written, has an implementer
choosing a contract in the editor.

### Prior findings -- closure, verified

* **EPR-01 (AST command cannot run) / EPR-04 (runbook's post-apply suite) --
  CLOSED, re-checked.** `_UPDATE_ALLOWLIST` really does carry
  `"_MODULE_MAPPINGS": "Assign"` (`bootstrap/tests/_ast_attest.py:142-147`), so
  the self-service claim holds; both Step 4 commands are quoted in Chunk 4's
  acceptance and both outcomes are required at that commit.
* **EPR-02 (no bridge across Chunks 4-6) -- CLOSED.** Chunk 4's table carries no
  marker rows; 6-1/6-2 land the marker in 6-3/6-4's commit.
* **EPR-03 (stale `8-2` references) -- CLOSED.**
* **EPR-05(a) (missing marker: the plan said both things) -- CLOSED.** A
  multiline search of the operative text finds **zero** occurrences of the
  refusing formulation for a missing marker; Chunk 5's two new paragraphs, row
  5-3's fixture list, rows 7-6/7-7 and the two replacement invariant rows all
  say the same thing. See EPR-17 for what the closure did *not* do.
* **EPR-05(b) (act in the marker's own commit) -- CLOSED, and independently
  re-derived.** See "The two flagged inferences" below.
* **EPR-06 (Chunk 7's audit predicate) -- CLOSED as to the predicate.** Chunk 6
  now says "every existing test that runs this tool's extractor over any tree",
  and 7-6/7-7/7-8 were added. The *enumeration* under that predicate is still
  one test short -- EPR-16, a new finding rather than a reopening.
* **EPR-07 (the obligation binds sessions this plan does not control) --
  CLOSED.** Chunk 6's disposition paragraph, row 6-8, and 8-6's evidence-not-gate
  scoping are all present and consistent with each other. One seam inside row
  6-8 remains, noted in EPR-18.
* **EPR-08 (row 8-1's CHANGELOG premise) -- CLOSED, re-measured at this commit,
  not carried forward.** `## Unreleased` is at 41; its subsections are
  `### Changed — Git-native security foundations` (42), `### Added` (60), a bare
  `### Changed` (**222**), `### Fixed` (317); the next `## ` is at 497. Row 8-1's
  target is exact and survived today's concurrent commits.
* **EPR-09 (sibling-guard seam and its attribution) -- CLOSED, both halves.**
  `## Verification`'s Boundary B command now carries `CAIRN_FULL_SUITE=1`;
  `bootstrap/tests/conftest.py` really does define `FULL_SUITE_ENV`,
  `BROAD_RUN_FILE_THRESHOLD = 40` and a `pytest_collection_finish` raising
  `pytest.UsageError`. The sibling plan's section heading at
  `dev/plans/full-suite-interception.md:450` reads exactly "Live commands the
  guard breaks beyond AGENTS.md's own sentence — flagged, not authorized", so
  the corrected attribution is accurate.
* **EPR-10 (the clause that could not fail) -- CLOSED, instrument confirmed.**
  `grep -rnE 'csv\.DictReader|csv\.reader' tools/ scripts/` returns 0; the same
  form finds `csv.writer` at `tools/_lifecycle_metrics/report.py:35`, so the
  instrument could have matched. The clause is gone and Chunk 1's acceptance now
  asserts something falsifiable (`--backfill-from` exits non-zero; `--help` does
  not name it).
* **EPR-11 (reviewer-identity shape) -- CLOSED.** Row 6-4 pins normalization
  through `extract.py`'s existing `_agent_of` path before the value reaches
  `reviewer_agents`, which is what keeps `cross_agent_type_review`'s
  `a != author` comparison comparing like values.
* **EPR-12 (SPDX; Chunk 8's row-id gap) -- CLOSED, both.**

### The two flagged inferences -- checked, not inherited

The round-3 Response asked that these be treated as new design decisions rather
than settled contract. I treated them that way. **Both are right**, and neither
is merely defensible -- each is the only reading that survives the tests it
touches.

**(1) The marker's own introducing commit is pre-cutoff (exclusive) -- CORRECT.**
Round 7 §4 says the cutoff *is* the commit that first adds the marker and says
nothing about that commit's own diff, so the text does not decide it. The tree
does. I read the whole of
`bootstrap/tests/test_reference_scripts.py::TestVcsRobustness::test_main_branch_target_runs`
(lines 458-486) and the fixture it uses: `_scaffold` installs
`dev/proposals/_template.md` unconditionally -- confirmed at
`bootstrap/_scaffold/config.py:555`, in `_CORE_MAPPINGS`, not behind a module
gate -- `_SAMPLE_PROPOSAL` (lines 122-132) carries a real
`## Review -- Bob (External Reviewer) -- 2026-05-02` section, and `git init` /
`add -A` / **one** `commit` lands the marker's introduction and that review-pass
act in the same diff. Under the inclusive reading that act is post-cutoff with
no block, so `proposal_rows` refuses where the test's own comment says
`# must not raise`. Under the exclusive reading it is pre-cutoff and the test
holds untouched. Nothing else in the accepted contract pulls the other way, and
the exclusive reading is (c)'s own "recording has not started yet" logic applied
at commit granularity, which is the reasoning the plan gives. I also checked the
tree-level cost: the marker's introducing commit in Cairn is Chunk 6's own
implementation commit, which performs no lifecycle act, so the blind spot the
exclusive reading opens is **empty here**. It is not empty for an adopter -- see
EPR-18's first bullet.

**(2) Git entirely absent is field-kind-dependent -- CORRECT, and the split is
the right one.** The refusal Chunk 6 adds is conditioned on the artifact being
*provably* past its cutoff, and that proof is only available from a history
walk; with no `.git` the trigger's own precondition is unmet. I checked all
three tests this turns on, by reading them rather than the plan's description:
`TestVcsRobustness::test_no_git_target_degrades` (445-457) asserts only
`stage_timestamp_reliability == "Best-effort"`, and
`test_lifecycle_stage_patterns.py::test_t12_...` (730) asserts `Best-effort` plus
empty `hours_*` -- both transition-kind, both unaffected under the
"unconditional quiet degrade" half. `test_installed_lifecycle_metrics_runs_on_target`
(277-295) really does assert `row["review_rounds"] == 1` on a scaffolded,
never-`git init`-ed tree, so it really does change, and 7-3 is right to call it
the one genuine change in the audit rather than a confirmation. The alternative
reading -- "no git means reconciliation cannot be performed at all, so refuse" --
would red all three and would also reverse `gitmeta.py`'s documented quiet-degrade
contract (`_git_log_for_path`, lines 67-84, "a deliberately quiet failure mode")
for the transition half that Part 3 explicitly does not touch. And refusing to
fall back to the heading count for the review-pass half is required, not
optional: the Decision retires the prose path outright.

What the resolution does *not* cover is the case one step in from "no `.git` at
all" -- a git repository whose working copy carries an act that is not committed
yet. That is EPR-15, and it is a different question, not a hole in this one.

### Findings

#### EPR-13 -- BLOCKING: `plan_review_rounds` and `code_review_rounds` are retained event-derived fields that no chunk wires and no section declares a residual

`extract.py` emits two schemas. Every chunk in this plan operates on the first.

`PLAN_COLUMNS` (`tools/_lifecycle_metrics/extract.py:89-96`, six entries)
carries `plan_review_rounds` and `code_review_rounds`, and
`extract_plan_row` computes both by **counting headings**
(lines 517-525): a line matching `_CODE_REVIEW_HEADING_RE` or
`_PLAN_REVIEW_HEADING_RE` (`parse.py:30-31`) that also contains a date. That is
the same prose-scraping class as `review_rounds`, in the same package, on the
artifacts this plan is about.

Three things make this a defect rather than an omission a reader can absorb:

1. **The accepted contract names these acts and pre-commits the disposition.**
   Round 6's taxonomy -- which this plan reproduces in Chunk 6 as "the binding
   contract" -- maps `review-pass` to "each `## Review` / `## Plan review` /
   `## Code review` section", and the paragraph immediately under it says: "Every
   retained event-derived field maps to exactly one kind and one same-artifact
   section. **No retained field is left prose-derived** ... and if the plan finds
   one that will not map, it declares that field a **residual** rather than
   quietly keeping the prose scraper." The plan does neither.
2. **The plan claims the work.** `## Scope` lists "wiring every retained
   event-derived field to exactly one event kind" as in, per the Decision. Row
   6-4 then enumerates `review_rounds`, reviewer identity/tier,
   `cross_agent_type_review`, `response_models` -- all proposal-row -- and
   `tools/_lifecycle_metrics/extract.py` is the only file it touches for the
   wiring.
3. **The two halves will actively disagree after Chunk 6.** Reconciliation
   covers `dev/plans/` (Chunk 5 derives a cutoff from `dev/plans/_template.md`;
   Chunk 6's acceptance runs the extractor over "`dev/proposals/` and
   `dev/plans/`"). So a plan artifact whose post-cutoff `## Plan review` section
   carries no block makes the run `INCOMPLETE` -- while the value the tool
   computes for that same artifact is still a heading count. That is precisely
   "quietly keeping the prose scraper", with a refusal bolted on top of it.

It is also the field with the worst known record: the Decision's own rationale
for the `degraded` allowance is that "`code_review_rounds` read 0 on 28 of 38
artifacts from a regex/template mismatch". This plan is the one that was supposed
to stop that, and as written it leaves that exact regex in place.

Cost, so the disposition is chosen with it in view: `extract_plan_row(path,
proposal_stems=())` takes **no** `repo_root` and **no** `include_git_timestamps`
-- it is a pure text function today, with no git plumbing at all, unlike
`extract_proposal_row`. Wiring it is real work that Chunk 6's table does not
budget.

Either disposition is available and neither narrows accepted scope, because
Round 6 authorizes both: wire the two fields (extending row 6-4 and Chunk 6's
fixtures to the plan row), **or** declare them a residual in the plan's own
words, with the reason and a revival condition -- but say which, and say what
the tool emits for them in the meantime. What is not available is leaving the
plan silent while its Scope claims the field set is complete.

#### EPR-14 -- BLOCKING: the grammar's `from_state`/`to_state` bound has no named vocabulary source, and the audit that exists to stop a vocabulary fork does not scan the file this plan creates

Chunk 4's closed key table -- reproduced verbatim from Round 7 as this chunk's
binding contract -- bounds `from_state` and `to_state` to "a declared lifecycle
status for that artifact type", and a value outside its bounds **refuses**. So
`events.py` is, by construction, a new consumer of Cairn's one runtime status
vocabulary. The plan never says where it reads it. A multiline search of the
operative text finds zero occurrences of `PLAN_STATES`, `PROPOSAL_STATES`, or
`vocabulary`.

This is not a detail an implementer can settle locally, for three reasons I
checked in the tree:

* **There is an established mechanism, and it is deliberate.** `extract.py`
  carries a contained loader -- `_validated_planner_path()`, `_vocabulary()`,
  `VocabularyUnavailable`, module-purge on failure (lines ~340-430) -- with a
  comment at lines 100-102 recording that a local tuple *was* declared here
  once, omitted `awaiting-plan-review`, and was removed for that reason.
* **The loader does not currently expose the half this grammar needs.**
  `_REQUIRED_EXPORTS = ('PLAN_STATES', 'HISTORICAL_PLAN_STATES')`
  (`extract.py:340`). There is no `PROPOSAL_STATES`, and a `transition` block on
  a proposal needs exactly that. Extending `_REQUIRED_EXPORTS` changes the
  contained loader's own contract, which is pinned in
  `bootstrap/tests/test_pilot_evidence.py::TestVocabularyLoader` -- so this
  reaches a test file the plan does not name.
* **The existing anti-fork audit fails open for a new file, by construction.**
  `bootstrap/tests/test_lifecycle_vocabulary.py`'s `_AUDITED_CONSUMER_SOURCES`
  (lines ~328-334) is a hard-coded five-tuple -- `scripts/transition_lint.py`,
  both `extract.py` copies, both `lifecycle.py` copies -- **not a glob**. A local
  status tuple written into `events.py` would be invisible to
  `test_no_consumer_local_status_literal_survives`. That file's own comment says
  why `lifecycle.py` was added to the tuple: "A status literal written locally
  there would be a vocabulary fork in a file this audit did not scan -- the
  precise failure Chunk A exists to prevent, in the one consumer whose absence
  from this tuple would have made the guarantee quietly incomplete." This plan
  creates that consumer and leaves the tuple alone.

Chunk 4 needs to say (a) that `events.py` reads the vocabulary through
`extract.py`'s existing contained loader rather than declaring its own, (b) what
happens when the planner is absent -- adopters can install `lifecycle-metrics`
without it, which is why `test_lifecycle_vocabulary.py`'s `_make_metrics_root`
has a `with_planner=False` mode -- and (c) that both `events.py` copies join
`_AUDITED_CONSUMER_SOURCES`. Without (c) the guard is silently incomplete from
the commit that creates the file, which is the failure mode `AGENTS.md` >
*Verifying claims* calls worse than no tool.

#### EPR-15 -- BLOCKING: the reconciler's act list has no named source, and working copy and history disagree in the ordinary case

Chunk 6's refusal fires when "a post-activation event-bearing act has no
matching block". Nothing in Chunks 5 or 6 says where the *act list* comes from,
and the two candidate sources are already split inside the existing extractor:

* **Acts are read from the working copy today.** `extract_proposal_row` opens the
  file directly (`text = path.read_text(encoding='utf-8')`, line ~149) and
  derives `review_sections`, `revised`, status and Response sections from that
  text. Nothing consults git for them.
* **Blocks are read from history.** Chunk 5's algorithm is a rename-aware
  oldest-first walk over `git log`/`git diff`; identity is `(introducing commit
  SHA, added-block index)`; a block is attributed only where it appears in a
  commit's added suffix.

So an act written into the file but not yet committed exists on the first side
and cannot exist on the second. Under the rule as written that is an unmatched
post-activation act, and the run is `INCOMPLETE`.

This is not an exotic state. It is the state Cairn is in every time an agent runs
the metrics command before committing -- including this plan's own evidence runs:
Chunk 6's acceptance says to "run the real extractor against Cairn's own
`dev/proposals/` and `dev/plans/` corpus at this commit", and row 6-8 has the
implementing agent append a block "in the same commit that performs the act",
which means there is a window in every such turn where the act is written and
uncommitted. The tooling already distinguishes these states elsewhere --
`lifecycle_planner board` reports `lifecycle files differ from HEAD: no` -- so
the concept exists in the tree and is simply unclaimed here.

Name it in Chunk 5's algorithm block: either the reconciler enumerates acts from
the same history it enumerates blocks from (uncommitted edits are invisible to
both sides, which is self-consistent and is what makes `(commit, index)` identity
meaningful), or it reads acts from the working copy and must then say what an
uncommitted act resolves to. Add the fixture to 5-3 either way. The same sentence
disposes of the neighbouring case where an artifact is tracked but its acts
predate nothing -- an artifact with no commits at all in a repo whose marker is
committed.

#### EPR-16 -- NON-BLOCKING: Chunk 7's audit is still one test short under its own corrected predicate

The predicate is now right ("every existing test that runs the extractor over any
tree"). The enumeration under it is not.
`bootstrap/tests/test_lifecycle_metrics_config.py::test_emit_snapshot_stays_contained_under_hostile_config`
(line 112) builds a tree with a real proposal under `dev/proposals/` and calls
`_lm.emit_snapshot` on it (line 123). It is not in Chunk 7's table.

Its disposition is benign -- no template, so no marker, so (c); the proposal
carries no `## Review` section; and the test asserts only the snapshot path and
containment -- so it lands with 7-7's group as a true no-op. The finding is not
the outcome, it is that Chunk 7's acceptance criterion is "7-1 ... 7-8", a
criterion that cannot see a test the enumeration omitted. That is the same shape
EPR-06 raised, one round later, and this one was inside the reach of the round-3
enumeration's own instrument: `emit_snapshot` matches it at line 123.

Add the row, and record the enumeration command in the chunk so a later pass
re-runs it rather than re-deriving it. The form I used, which finds all of
7-3/7-5/7-6/7-7/7-8 plus this one:
`grep -rn 'extract_proposal_row\|extract_plan_row\|proposal_rows\|plan_rows\|emit_snapshot' bootstrap/tests/*.py`.
I confirmed it could match before trusting it -- it returns the five tests the
plan already names, so a null result would have been meaningful.

#### EPR-17 -- NON-BLOCKING: the missing-marker resolution departs from the accepted Decision's stated term, and neither the departure nor its contract dimension is declared

The substance is authorized -- the Maintainer's "I think (c) is right" is quoted
verbatim and visually isolated, and I am not reopening it. Two record defects
travel with it.

**The departure is not named as one.** Round 7 §4 and the Decision's summary of
accepted terms both read "Missing, divergent, or multiply-introduced markers
refuse." Chunk 5 reproduces §4's activation rule as the binding contract and
silently drops `Missing` from the refusing set. A reader coming to this plan from
the archived proposal hits a flat contradiction with no bridge; a reader coming
to it cold never learns the accepted contract said otherwise. The plan is
scrupulous about exactly this elsewhere -- the `--backfill-from` removal states
the false claim it corrects, quotes the authorization, *and* records which
lettered option was chosen and what the other two were, "recorded because a bare
letter will mean nothing later". The marker resolution quotes a bare letter and
does not say what (a) and (b) were. Apply the plan's own standard to it.

**The `Contract expansion` declaration is stale.** `dev/plans/_template.md`'s
review-basis doctrine lists "failure disposition" among the dimensions a plan
declares, and the plan's only declaration reads "adopter-facing CLI surface",
scoped to `--backfill-from`. This plan now makes three failure-disposition
determinations beyond the accepted contract: missing marker does not refuse;
the marker's own commit is pre-cutoff; git-absent falls back rather than
refusing. EPR-05(a) said in as many words that the declaration "does not cover"
the marker outcome, and the resolution did not extend it. The gate this feeds is
already satisfied -- the plan is at `required(Internal)` and is getting a
distinct review -- so this is record fidelity, not a bypass. Fix it in the
declaration, not in a paragraph.

#### EPR-18 -- NON-BLOCKING: four small ones

* **The exclusive reading's concession is named for the wrong case.** Chunk 5
  names what (c) concedes for a *deleted* marker but not what the exclusive
  cutoff concedes: a lifecycle act co-committed with the marker's introduction is
  permanently unmeasured and undetectable. In Cairn that window is empty (the
  marker lands in Chunk 6's implementation commit, which performs no lifecycle
  act -- I checked). In an adopter tree it is not: taking the template update in
  the same commit as a status flip silently drops one act. One sentence, in the
  paragraph that already does this work for the deletion case.
* **"Empty" has no pinned representation.** `review_rounds` is an `int` today;
  the plan says pre-cutoff review-pass fields "emit empty" and row 7-3 says the
  assertion is "updated to assert the empty value" without saying what that
  value is. `''` and `0` are both writable and only one of them is correct --
  the Decision's own rationale for dropping historical continuity is a
  `code_review_rounds` that "read 0" and travelled. There is precedent in the
  tree (`hours_*` emit `''` on the degraded path, per T12); name it rather than
  leave a numeric column's empty state to the editor.
* **The history algorithm never names the zero-parent commit.** Step 2 requires
  "the parent sequence" and step 5 refuses on multi-parent attribution; a root
  commit has neither one parent nor several. An implementer reading "refuse on
  ambiguous parent attribution" could reasonably refuse on zero parents too,
  which would refuse any artifact whose history begins at a repository's first
  commit -- reachable in a fresh adopter tree and in 5-3's own "clean linear
  history" fixture. State that a root commit's parent sequence is empty.
* **Row 6-8 assigns an act to an agent who may not perform it.** It instructs
  "the implementing agent" to append a block to every lifecycle act on this
  plan's own file, and names "this file's own eventual code review" among them.
  Code review's floor is *not* the implementing agent, and reviews are
  self-committed by their named author (`AGENTS.md` > Review). The instruction
  as written cannot be followed for the one act it names explicitly. Route it to
  the reviewer-facing text, or record it as part of the concurrent-session
  residual the same chunk already names.
* (Housekeeping, no disposition needed: row 1-14 says "the package-docstring
  mention of the backfill mode" -- there are three, at
  `tools/_lifecycle_metrics/__init__.py` lines 28, 47 and 60, plus the worked
  example command. Row 1-9's "two locations in each file" style is the right
  precision here.)

### What I tested that held

Reported because a defect-only review tells the author nothing about which
claims were exercised. Everything below I ran or read against the live tree at
this commit, not carried forward from a prior round's record.

* **`PROPOSAL_COLUMNS` has exactly 30 entries**, all eight retirement targets
  present, so 1-8's "22 after" is right; and **`PLAN_COLUMNS` carries none of the
  eight**, so Chunk 1's "remove the eight names from `PROPOSAL_COLUMNS`" is
  complete rather than half a sweep. (This is also how I found EPR-13: the same
  probe that confirms the retirement is complete shows the second schema exists.)
* **`METRIC_CONTRACT_MAP` carries exactly three `proposal_review_yield_*`
  entries** and no `total_findings`/`findings_p*` entry at all -- 1-4 is exact.
* **The retirement inventory is complete outside the engine.** A tree-wide search
  for the eight names across `*.py`/`*.md`/`*.json`/`*.yml` finds them only in
  the six files Chunk 1 names, plus two archived deliberation artifacts. No
  module doc, gate manifest, or fidelity file names a retired column, so no
  seventh file is owed.
* **The launcher facade needs no edit** (row 1-6): it re-exports the engine
  namespace wholesale and carries no submodule list, so `events.py` needs no
  registration there.
* **No count pin beyond the two the plan names moves when `events.py` lands.**
  `scripts/measurements.py`'s `REGISTRY` has two keys
  (`claim_check_watch_file_lines`, `solo_greenfield_module_count`), neither a
  shipped-`.py` count, so `verify_counts` does not drift.
  `test_security_lint.py:376` pins 52 and `test_notice_install.py:74` pins 56 --
  both still current at this commit, both correctly told to re-derive.
* **The gate-frozen change does not red the suite mid-implementation.** I ran
  `python -m pytest bootstrap/tests/test_gate_manifest.py` -- 21 passed -- on a
  tree that has already taken gate-frozen edits today (`bootstrap/tests/conftest.py`
  at `a316d75`). The gate's trust root is the `refs/cairn/gate-anchor` ceremony,
  not a pytest tripwire, so Chunk 4's "this chunk's own commit is green" criterion
  is satisfiable even though Chunk 1 has already touched frozen files. I went
  looking for this expecting a defect and did not find one.
* **The wrapped-phrase instrument works, confirmed against a known-present
  case.** `re.search(r'finding\s+severities', ...)` finds 2 in each module doc,
  **1** in `dev/agent_collaboration.md` (at lines 385-386, wrapping as
  `finding` / `severities.`) and **0** in
  `templates/core/dev/agent_collaboration.md`; a single-line `grep` finds 2, 2,
  **0**, 0. So the acceptance criterion at Chunk 2 discriminates exactly where
  the plan says it does, and the exclusion of the shipped core file is real.
* **`_iter_corpus_files` excludes `_template.md` by name** (`extract.py:114`), so
  the marker and worked examples Chunk 6 adds to the templates are never parsed
  as real events. The plan does not claim this; it holds, and Chunk 6 depends on
  it.
* **`_scaffold` installs both marker paths unconditionally** --
  `bootstrap/_scaffold/config.py:555-556`, in `_CORE_MAPPINGS` -- which is what
  makes the git-absent and single-commit cases reachable at all.
* **Every line citation in the operative text that I checked lands**:
  `test_every_subcommand_is_read_only` at `test_lifecycle_contract.py:172` and
  its `_git` helper at 69; T10 at `test_lifecycle_stage_patterns.py:647`, T12 at
  730; `lm_repo` at `test_lifecycle_cli.py:460` with its three consumers at 472,
  499, 520; `test_installed_lifecycle_metrics_runs_on_target` at 277-295;
  `test_no_git_target_degrades` at 445-457; `docs/glossary.md`'s "never mine it
  for metrics" at 37; `_MODULE_MAPPINGS`'s nine `_lifecycle_metrics/` rows with
  the "nine package files install verbatim" comment at
  `bootstrap/_scaffold/config.py:746`; `cfg.backfill_max_days == 14` at
  `test_lifecycle_metrics_config.py:61` as the only test exercising that mode.
* **Row 5-1's reuse claim is real**: `gitmeta.py:67-84` defines
  `_git_log_for_path` and already passes `--follow`, so "rename-aware" is an
  existing capability rather than something Chunk 5 invents.
* `python scripts/claim_check.py dev/plans/metrics-events-not-prose.md` -- OK, no
  flags; the three forward-referenced paths clear through the `Proposed paths:`
  declaration.
* `python tools/lifecycle_planner.py board --compact` -- the row reads
  `plan|metrics-events-not-prose|awaiting-plan-review|plan-reviewer|...|valid`.
* **Chunk 3's acceptance still avoids the cannot-fail trap**, and Chunk 1's
  acceptance now does too after EPR-10 -- both name a property that can be
  observed false.

### Sharpening

None. Nothing in this pass narrows what the plan will deliver; EPR-13 and EPR-14
each ask for work the plan's own Scope already claims, and EPR-13's residual
option is the accepted contract's own named alternative (Round 6), not a fence
this review is drawing.

**Scope delta**: preserved.

### Coverage

Read: `AGENTS.md` in full; `dev/plans/_template.md`'s review-basis, inheritance
and scope-delta doctrine (~lines 395-490); the complete plan including all three
prior review sections and all three Responses; the source proposal's Round 6
taxonomy section (§1, lines 1200-1250), Round 7 §§1-5, and `## Decision`;
`dev/plans/full-suite-interception.md`'s "Live commands the guard breaks"
section.

Inspected in the live tree: `tools/_lifecycle_metrics/{extract,parse,snapshot,
cli,config,gitmeta,subsystems}.py` and the launcher facade;
`bootstrap/_scaffold/config.py` (`_CORE_MAPPINGS`, `_MODULE_MAPPINGS`);
`bootstrap/tests/{_ast_attest,_gate_manifest,conftest}.py`;
`bootstrap/tests/test_{reference_scripts,lifecycle_stage_patterns,lifecycle_cli,
lifecycle_contract,lifecycle_vocabulary,lifecycle_metrics_config,
metrics_status_normalization,pilot_evidence,security_lint,notice_install,
quickstart_sequence,verify_counts,manifest}.py`; `scripts/measurements.py`;
`CHANGELOG.md`; `docs/glossary.md`; both `agent_collaboration.md` copies; both
`lifecycle-metrics.md` copies.

Ran: `python -m pytest bootstrap/tests/test_gate_manifest.py` (21 passed);
`python scripts/claim_check.py` on this plan; `python
tools/lifecycle_planner.py board --compact`; `python scripts/quality_gate.py
--sub neutrality` (to establish scope, not as a gate on this plan); targeted
`python3 -c` probes for the column counts, the wrapped-phrase instrument, the
plan's own operative-text term census, and the CHANGELOG heading positions;
`git show`/`git log` for the reviewed-commit and sibling-plan citations.

Did **not** run: the full suite (verification is not delegated to this pass, and
a bare `python -m pytest bootstrap/tests` now exits 4 by the broad-run guard);
`scripts/check_cairn.py`; `scripts/quality_gate.py --sub redundancy`; any
baseline mutation or `update-symbol` invocation, dry-run or otherwise. Did not
re-read the source proposal's superseded Rounds 1-5 except where a Round 6/7 or
plan claim cited them. Did not review `tools/lifecycle.py` or the pilot-event
ledger; I confirmed by search that no chunk touches either.

**Status**: `awaiting-plan-review` -> `revising-plan`.

## Response to plan review -- Claude Sonnet 5 (author) -- 2026-08-20 (round 4)

**Model**: Claude Sonnet 5

**All six findings accepted; all folded into the plan's own operative cells,
not answered here.** The three blocking findings share one root cause named
in the review's own verdict: every prior round read Part 3 through the
**proposal**-row schema and never opened the **plan**-row schema, the
vocabulary-loader source, or the reconciler's own act-list source. Re-deriving
the field inventory from `tools/_lifecycle_metrics/extract.py` directly
(`PLAN_COLUMNS`, `_REQUIRED_EXPORTS`, `extract_plan_row`'s current signature)
rather than from what the plan previously claimed is what each disposition
below is built on.

| Finding | Disposition | Where addressed |
|---|---|---|
| EPR-13 (BLOCKING) — `plan_review_rounds`/`code_review_rounds` are retained event-derived fields no chunk wires | ACCEPTED, disposition: **wire**, not residual | Scope's "In, per the Decision" paragraph (both schemas named); Chunk 6's intro, new taxonomy-extension paragraph; Chunk 6's "dropped-historical-continuity allowance" paragraph (both fields added to the empty-emission list); new rows 6-9 through 6-12 (`extract_plan_row` gains `repo_root`/`include_git_timestamps`, sources both fields from reconciled `review-pass` blocks classified by matched heading via the existing `_CODE_REVIEW_HEADING_RE`/`_PLAN_REVIEW_HEADING_RE`, `plan_rows()` passes `repo_root` through, new fixtures); Chunk 6's acceptance paragraph; Author-accounting invariants table (new row) |
| EPR-14 (BLOCKING) — the grammar's `from_state`/`to_state` bound has no named vocabulary source, and the anti-fork audit does not scan `events.py` | ACCEPTED | Row 4-1 (the check takes `valid_states` as an explicit parameter — no import of `extract.py`, avoiding the circular dependency Chunk 6 would otherwise create); new rows 4-10 through 4-13 (`_REQUIRED_EXPORTS` extended to require `PROPOSAL_STATES` alongside `PLAN_STATES`; `test_lifecycle_vocabulary.py`'s `METRICS_SPEC`/`_DECOY_PLANNER_SRC` and `_AUDITED_CONSUMER_SOURCES` both extended); row 5-1 (the history walker threads the same parameter through, not a second declaration of it); Author-accounting invariants table (new row) |
| EPR-15 (BLOCKING) — the reconciler's act list has no named source, and working copy and history disagree in the ordinary case | ACCEPTED, resolved: the act list is read from the same committed history (HEAD) the block list is read from, not the live working-copy text | Chunk 5, new "The act list the reconciler checks" paragraph (the resolution, its reasoning, and the named behavior change from today's working-copy-reading tool); row 5-3 (new fixture); Author-accounting invariants table (new row) |
| EPR-16 (NON-BLOCKING) — Chunk 7's audit is one test short under its own corrected predicate | ACCEPTED | New row 7-9 (`test_emit_snapshot_stays_contained_under_hostile_config`, confirmed unaffected); the enumeration command recorded in Chunk 7's own text so a later pass re-runs rather than re-derives it; Chunk 7's acceptance line |
| EPR-17 (NON-BLOCKING) — the missing-marker resolution departs from the Decision's stated term undeclared, and `Contract expansion` is stale | ACCEPTED, both halves | Chunk 5's Activation section, new "The option that names" paragraph (states what (a) and (b) were, alongside the chosen (c), mirroring the `--backfill-from` section's own standard) and the "departure from Round 7 §4's own literal text" paragraph immediately after it; Scope's `Contract expansion` section, new paragraph naming all three failure-disposition determinations this plan makes beyond the accepted text |
| EPR-18 (NON-BLOCKING) — four small ones | ACCEPTED, all four addressed; the fifth item was housekeeping only, per the finding's own text, and needed no disposition | (1) Chunk 5, new "What the exclusive reading concedes" paragraph (the adopter-tree cost, distinct from the deletion-case concession already stated); (2) Chunk 6, new "'Empty' is the literal string `''`" paragraph, plus the reasoning tying it to the Decision's own `code_review_rounds`-read-0 rationale; (3) Chunk 5, new "A root commit's parent sequence is empty" paragraph; (4) row 6-8, rewritten to instruct the act's performer rather than naming "the implementing agent" for an act (code review) it cannot perform under `AGENTS.md` > Review |

**One correction this round's own drafting produced, beyond what any finding
asked for.** EPR-14's own finding text cites `bootstrap/tests/test_pilot_evidence.py::TestVocabularyLoader`
as where extending `extract.py`'s `_REQUIRED_EXPORTS` reaches a pinned test
file. Checked directly rather than carried forward: that file's `MODULE_PATH`
(line 51) is `templates/skills/_lib/lifecycle.py` — `tools/lifecycle.py`'s own
independent copy of the loader pattern, a consumer this plan does not touch
and explicitly places out of scope elsewhere ("Out, because Round 5
explicitly removed it"). The test surface the extension actually reaches is
`bootstrap/tests/test_lifecycle_vocabulary.py`'s `METRICS_SPEC`/
`TestLoaderContainmentMatrix`, confirmed by reading that file's `ConsumerSpec`
structure directly (row 4-11 names the concrete edits it needs). Row 4-11
carries the correction rather than silently repeating the review's own
citation.

**What I believe may still be under-specified, flagged rather than deferred,
per this task's own brief.** The classification of a plan artifact's
`review-pass` events into `plan_review_rounds` vs. `code_review_rounds` (row
6-9) reuses the matched section heading (`_CODE_REVIEW_HEADING_RE`/
`_PLAN_REVIEW_HEADING_RE`) rather than the event block's own `tier` key
(bounded to `Internal`/`External`/`Security`/`Code` by Round 7's grammar,
reproduced in Chunk 4). I read the heading as the more robust classifier — it
is what the reconciler already inspects to confirm the act exists at all, so
it does not depend on the block-writer correctly setting `tier: Code` — but
Round 7's text does not say which of the two the taxonomy intends, and the
`tier` bound's own fourth value (`Code`) is otherwise unused by any field this
plan wires. This is a design choice this round makes, not a specification
Round 7 states directly, and a future round should treat it as such.

**Searches confirmed against a known-present case, per this task's
instrument-confirmation rule.** (1) `grep -n "^PLAN_STATES\|^PROPOSAL_STATES\|^HISTORICAL_PLAN_STATES\|^HISTORICAL_PROPOSAL_STATES" tools/lifecycle_planner.py`
— confirmed `PROPOSAL_STATES` exists in the planner (line 1113) but is absent
from `extract.py`'s `_REQUIRED_EXPORTS` (line 340), which is EPR-14's own
claim and the reason row 4-10 is needed rather than assumed unnecessary. (2)
`grep -rn "plan_review_rounds\|code_review_rounds" bootstrap/tests/*.py`
returns nothing — no pre-existing test asserts either field's value, so
EPR-13's wiring (unlike `review_rounds`'s row 7-3) needs no pre-existing-test
audit row of its own; confirmed by the same search finding `_hour_delta`'s
`''`-on-missing precedent at `gitmeta.py:127` when checking for one, which
the search could have failed to find had the file not been read directly. (3)
`grep -n "_review_tier" tools/_lifecycle_metrics/parse.py` and reading the
function — confirmed it is heading-generic (works on any `## `-prefixed
header, not proposal-specific) but is not the mechanism row 6-9's
classification uses, ruling out a plausible-looking shortcut before writing
the row. (4) `grep -rn "_REQUIRED_EXPORTS\|LoaderSpec(" bootstrap/tests/*.py tools/_lifecycle_metrics/*.py`
— located `test_lifecycle_vocabulary.py`'s `ConsumerSpec`/`METRICS_SPEC`
structure directly, which is what produced the EPR-14 citation correction
above.

**Status**: `revising-plan` -> `awaiting-plan-review`.
