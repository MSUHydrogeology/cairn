# Make existing code and system shape cheap to inspect

**Author**: Codex (runtime model identifier unavailable; Strategy)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy -- repository inspection and selected-module install contract
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Extend architecture guidance with a generated code map, reuse leads and a bounded visual pilot, then retire the source strategies when their work is complete.

## Decision summary

Help scientists understand agent-built systems without reading every patch.
Extend the optional architecture module, not the core approval process.
Costs: one shared read-only collector, maintained examples and a short release structure
assessment for selected-module projects; no new service or approval meeting.

## Context

At `5c9129a5`, `templates/modules/team-gated/architecture-review.md` targets
accreted systems without a standing routine.
[Architecture growth](../strategy/2026-10-30-claude-architecture-growth.md),
[engineering practices](../strategy/2026-10-27-codex-adopter-engineering-practices.md)
and [visual review](../strategy/2026-10-28-codex-review-at-agent-scale.md)
supply the direction. Historical duplication figures are not re-measured here.

## Proposal

**1. Generate a map.** List components, files, public functions/classes and
docstring summaries by location. Use Python AST; other languages retain
file/component coverage with unsupported analysis explicit. Include revision,
locations, omissions and parse errors; diagnostics name the corrective action.
Ship `templates/modules/team-gated/code_map.py` and byte-identical
`tools/code_map.py`.

Collector/runtime are trusted, outside the inspected inputs. Reuse only
suitable parsing/classification from `scripts/measurements.py` and
`tools/gauge.py`, not target-root imports or their inherited-environment Git
calls. Git-backed inspection requires the shared sterile helper: validated
executable, fixed arguments and sanitized configuration/environment.
Missing that boundary makes the view incomplete; the plan must still deliver
the pilot, not defer it indefinitely. Share history extraction without
imposing Cairn's categories on adopters.

**2. Show neighbors.** Compare added/changed functions with existing functions
by normalized structure/names, plus whole-tree release mode. Existing reuse
answers and review packets can cite entries. Similarity is advisory, not
equivalence, plagiarism or permission to delete. Retain justified standalone
shipped copies.

**3. Name critical homes.** Record safe-reading, containment, terminal-encoding
and Git-execution owners in the existing architecture record. Add narrow
duplicate-pattern checks for dangerous divergence, documenting legitimate
wrappers/copies; no general prohibition on functions, classes or abstraction.

**4. Improve the rubric.** Support legacy, new and mixed systems. Keep five
lenses; add accretion/reuse and contrasting examples, including justified
action and adequate existing practice. This work owns rubric examples that
separate functional test scope from execution cost; fault-centered testing
owns matching testing-module guidance; link it rather than duplicate instruction.
At selected-module releases, record map, neighbors, growth and ranked
consolidation candidates with preserving tests in the same record.
Judge useful simplification, not a deletion quota.

**5. Pilot visual review.** Compare manual practice, an existing product and
a small offline report reusing LHM's scope-map interaction/shared collection.
Cover workstreams, shape, capabilities and growth; semantic views require
cited workflows/declarations. Symbols prove neither capability nor unused code.
Use independently prepared duplication, drift, capability overclaims and
justified growth as known-answer tasks. Measure accuracy/time, annotation
effort, false alarms and misses; reject graphics improving neither
understanding nor decisions or requiring unreliable guesses.
Separate editing activity from endpoint change, count shared-file endpoint
growth once, and display ambiguous/unattributed ownership.
Compare bottom-up folder summaries with map-first discovery.
No finished four-view interface or README-per-folder promise.

**6. Retire completed strategies.** The implementation plan owns one grouped
v0.7 closeout assignment to the release-closeout agent before plan archive.
Retire the sequence note at the release cut, cancellation or supersession,
once every item has an outcome or explicit live home.
Follow `dev/strategy/2026-11-02-codex-v07-delivery-sequence.md`'s table:
resolve whole scope, move lasting guidance, archive notes/owned assets and
repair links. Keep unfinished scope visible and broad living registers active.
No extra archival gate or recurring inventory.

## Rationale

Make discovery cheaper and architectural advice actionable. Shared data is
not a correctness verdict; the pilot may reject unhelpful graphics.

## Alternatives considered

Doing nothing keeps manual discovery. Third-party analyzers add dependencies;
a full review platform adds premature interface/service costs.
Recommend shared static foundations and bounded exploration, with optional
tools separately assessed.

## Documentation / doctrine surface

Update selected module, rubric, reuse prompts and install/script registry;
preserve adopter edits and vendor neutrality.

Proposed paths:
- `templates/modules/team-gated/code_map.py`
- `tools/code_map.py`
- `bootstrap/tests/test_code_map.py`

## Evidence / verification plan

### Tests required

In `bootstrap/tests/test_code_map.py`, exercise real CLI/installed copy,
minimal trees, mixed/unsupported languages, malformed source, links, control characters,
hostile HTML, target imports and Git configuration attempting execution.
Require finite file-count, byte, parser/elapsed-work and comparison budgets;
choose measured limits in the plan. Oversized/deep/pathological inputs
must stop affected processing and visibly report incomplete evidence.
Use existing `test_scaffold.py`, `test_manifest.py`,
`test_reference_scripts.py` and `test_module_merge.py` under
`bootstrap/tests/` for affected contracts.
Exercise legacy/new/mixed rubric examples, not only tooling.

### Examples / smoke checks

Show genuine reuse, justified copies and missing capability evidence.
Verify offline output, contained regular-file traversal, escaped display
and known-answer pilot tasks. Run prose gates.
These implementation demonstrations have not run.

#### Security preflight

S1: inspected text is untrusted data; trusted collector/runtime decide parsing.
S2: planted imports, executable Git settings, active HTML and budget overflow
must trip real-entry-point probes; future controls, not executed safeguards.
S3: selected-module CLI/report covers the requested root/range; omissions stay
visible. Wording: "The map is evidence for investigation."
S4: unreadable, truncated or stale inputs are incomplete, never clean.
S5: hostile descriptions can still mislead; no network, refactor, deletion,
publication or target execution is authorized. A compromised host remains
outside this static-inspection guarantee.

### Independent scientific check

N/A: no equations change; capability claims still require evidence.

## Signals the change is wrong

Unused maps, mostly justified neighbors, unsupported semantic claims or
multiplying collectors, checklists and strategy notes.

## Scope delta

**Scope delta**: preserved -- all shared foundations, pilot and retirement outcomes remain.

## Assurance path

**Assurance path**: high-assurance -- untrusted inputs and install contract.

## Review -- Codex (fresh-context usual reviewer) -- 2026-11-02

**Model**: inherited Codex runtime; exact identifier unavailable; no downshift.
**Reviewed commit**: `9d5a69e524a2ab3a749b386dd67efe2861f2ecf0`
**Tier**: usual
**Target**: opening proposal. **Prior findings**: none.
**Assurance path**: high-assurance.

**Foundations**

1. **Should this happen as framed?** Yes: make investigation cheaper without
   automated refactoring. Architecture support ships questions; the gauge
   collects editing history, not endpoint growth --
   `templates/modules/team-gated/architecture-review.md`; `tools/gauge.py`, `_numstat`.
2. **Best alternative.** An existing visualization plus a thin map/neighbor
   command could reduce interface upkeep; setup/privacy costs remain
   unmeasured --
   `dev/strategy/2026-10-28-codex-review-at-agent-scale.md`, Options.
3. **What would show it wrong?** Mostly justified neighbors, unsupported
   capability claims, or no understanding gain against manual practice --
   Proposal 2/5; source visual strategy, Open questions and falsification.

**Verdict**: REVISE. **Findings**: two non-blocking improvements; no blockers.

1. **AR-1 -- Give the pilot known answers.** Proposal 5 records understanding,
   false alarms and misses, but names no independent cases. The visual
   strategy specifies prepared duplication, drift and capability overclaims.
   Close by carrying those cases, comparator tasks, attribution/endpoint
   counting rules and a rejection criterion into the planned pilot evidence.
   Repeated edits must not masquerade as net growth.
2. **AR-2 -- Evaluate the rubric, not only the collector.** Tests required
   exercises tooling; `dev/strategy/2026-10-27-codex-adopter-engineering-practices.md` calls for
   contrasting adopter assessments and separates functional scope from
   execution cost. Close with small legacy/new/mixed examples yielding a
   justified action or adequate-practice result, and explicit ownership of
   that testing distinction between this work and fault-centered testing.

The grouped release-closeout row survives child-plan archive and retains
source retirement ownership. No board outcome is proposed for removal.

**Elapsed**: approximately 8 minutes, including shared source inspection.
**Tokens**: unknown.

**Covered**: source strategies, board outcomes, module/rubric, collector
boundaries and retirement ownership. **Not covered / low confidence**: no
implementation experiments, tool trials, duplication remeasurement or Security
Review; benefit/annotation cost remains unmeasured.

## Review -- Codex (independent Security Reviewer) -- 2026-11-02

**Model**: inherited Codex runtime; exact identifier unavailable; no downshift.
**Reviewed commit**: `9d5a69e524a2ab3a749b386dd67efe2861f2ecf0`
**Target**: opening proposal. **Prior findings**: none.
**Assurance path**: high-assurance. **Tier**: Security Review.

**Foundations**

1. **Should this happen as framed?** Yes: an advisory static map and bounded
   pilot can improve discovery without authorizing deletion -- Proposal 1-5.
2. **Best alternative.** Retain rubric/manual search as the pilot comparator;
   share only suitable collection logic --
   `templates/modules/team-gated/architecture-review.md`; Proposal 1/5.
3. **What would show it wrong?** Inspection executes target code, escapes its
   root, renders active content or silently truncates evidence -- Tests
   required; Security preflight.

**Verdict**: ACCEPT. **Findings**: two non-blocking improvements; no blockers.

1. **AR-S1 -- Specify executable trust.** Reuse candidates cross executable
   boundaries: `scripts/measurements.py:160-179` imports `_scaffold` from its
   supplied root; `tools/gauge.py:102-108` invokes PATH-resolved Git with
   inherited environment. Neither guarantees safe untrusted-repository reading.
   Close by distinguishing trusted collector/runtime from inspected inputs,
   identifying suitable static reuse, and assigning target-import and
   Git-environment probes in the plan. This is not a demonstrated defect in
   the unbuilt collector.
2. **AR-S2 -- Bound processing too.** "Bounded traversal" leaves file bytes,
   parser work and whole-tree comparison work unspecified;
   `scripts/measurements.py:127-139` reads the entire file before parsing.
   Close with finite processing budgets and visibly incomplete results when
   limits are reached. Exact limits and measurements belong in the plan.

The parent retirement table requires whole-scope outcomes and reserves scope
changes to the Maintainer --
`dev/strategy/2026-11-02-codex-v07-delivery-sequence.md`, Retirement ownership.
Archiving cannot erase unfinished work. S2's future demonstrations are honestly
unmeasured, not missing current collector experiments.

**Elapsed**: shared approximately six-minute review window; per-file split
unmeasured; recording approximately two minutes. **Tokens**: unknown.

**Covered**: S1-S5, helper trust assumptions and retirement ownership.
**Not covered / low confidence**: future filesystem-race, terminal/HTML,
no-execution, resource-limit, installed-copy or pilot demonstrations.

## Response -- Codex (author) -- 2026-11-02

**Model**: Codex (runtime model identifier unavailable).

- **AR-1 accepted:** The pilot now has independently prepared duplication,
  drift, capability-overclaim and justified-growth tasks; comparator
  accuracy/time, annotation effort and rejection criteria. Editing activity
  is separate from endpoint growth; shared files count once and uncertain
  attribution remains visible.
- **AR-2 accepted:** Verification covers legacy/new/mixed rubric examples
  yielding an action or adequate-practice conclusion. The rubric owns these
  examples; fault-centered testing owns corresponding scope-versus-cost
  guidance in its module. Both proposals state that division.
- **AR-S1 accepted:** Trusted collector/runtime are distinct from inspected
  data. Reuse excludes target imports and inherited-environment Git calls.
  Git-backed inspection requires the shared sterile boundary, with planted
  import/config execution probes; missing it cannot yield complete evidence.
- **AR-S2 accepted:** The plan must choose finite measured file-count, byte,
  parser/elapsed-work and comparison limits. Pathological inputs must stop
  affected processing and visibly report incomplete evidence.

All findings were non-blocking and are addressed in the operative contract.
The map, neighbors, critical homes, rubric, four-view pilot and retirement
assignment remain. No implementation controls or benefits are claimed tested.
The proposal is ready for the Maintainer's Decision, not implementation.

**Elapsed**: approximately 7 minutes shared revision design; per-file split
unmeasured. **Tokens**: unknown.

### Withdrawn / superseded commitments

None. Restricting reuse to suitable safe helpers specifies the original
qualification; it does not drop collection, pilot or retirement outcomes.

## Decision -- Maintainer -- 2026-11-02

**Elapsed**: unknown; **Tokens**: unknown.

**Tier**: heavy

**ACCEPTED.** Asked "Architecture and reuse: accept as heavy?", the Maintainer's authorization, quoted verbatim:

> "Accept as heavy. This should also be not just for Cairn, but architecture for adopter projects to use, right?"

Scribe's note (not part of the quote): the question in the last sentence is answered by the proposal itself. The code map, neighbors and rubric ship to adopter projects through the optional architecture-review module (Proposals 1 and 4; Documentation / doctrine surface), and the rubric covers legacy, new and mixed systems. The module is selected, not installed by default.
