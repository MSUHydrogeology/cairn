# Make existing code and system shape cheap to inspect

**Author**: Codex (runtime model identifier unavailable; Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy -- repository inspection and selected-module install contract
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Extend architecture guidance with a generated code map, reuse leads and a bounded visual pilot, then retire the source strategies when their work is complete.

## Decision summary

Help scientists understand what agent teams build without reading every patch.
Extend the existing optional architecture module, not the core approval process.
Build one shared, read-only collection layer; make repetition visible before
adding more code. The recurring costs are maintaining that collector and a
short structure assessment at each release for projects selecting the module.

## Context

At `5c9129a5`, `templates/modules/team-gated/architecture-review.md` targets
accreted systems and adds no standing routine. The
[architecture-growth study](../strategy/2026-10-30-claude-architecture-growth.md)
proposes a map, neighbors, critical capability homes and release assessments.
Its historical duplication figures are not re-measured here.

The [engineering-practices note](../strategy/2026-10-27-codex-adopter-engineering-practices.md)
covers legacy, new and mixed systems.
[Visual review](../strategy/2026-10-28-codex-review-at-agent-scale.md)
asks different questions from patch correctness. These directions share data,
not an automatic verdict.

## Proposal

**1. Generate a map.** List components, files, public functions/classes and
docstring summaries, grouped by location. Python uses the standard-library
AST; other languages retain file/component coverage with unsupported
symbol analysis explicit. Include source revision, locations, omissions and
parse errors. Reuse existing collection/classification in `tools/gauge.py`
and `scripts/measurements.py` where suitable; do not create competing
history extractors or force Cairn's categories onto adopters.
Ship `templates/modules/team-gated/code_map.py` with its byte-identical
self-hosted copy at `tools/code_map.py`.

**2. Show neighbors.** Compare added/changed functions with existing functions
by normalized structure and names; provide a whole-tree release mode.
Plans' existing reuse answers and review packets can cite entries.
Similarity is an advisory lead, not semantic equivalence, plagiarism or proof
that deletion is safe. Preserve deliberate standalone shipped copies.

**3. Name critical homes.** In the existing architecture record, name the
owners of safe reading, containment, terminal encoding and Git execution.
Add narrow duplicate-pattern checks where divergence would be dangerous.
Document legitimate wrappers and copies. This is not a general prohibition
on functions, classes or abstraction.

**4. Improve the rubric.** Support legacy, new and mixed systems. Retain its
five lenses; add accretion/reuse, contrasting examples and links to the
testing module rather than duplicate testing instruction. At selected-module
projects' releases, use the same architecture record for map, neighbors,
growth and ranked consolidation candidates with preserving tests.
Adequate existing practice is a valid result. No removal quota or extra
approval meeting; judge useful simplification, not lines deleted alone.

**5. Pilot visual review.** Reuse LHM's scope-map interaction and shared
collection. Compare unchanged practice, an existing visualization product,
and a small offline report. Assess workstreams, system shape, capabilities
and growth; keep all four questions visible. Static symbols cannot prove
capability or unused code: semantic views need cited workflows/declarations,
with missing evidence shown. Record annotation effort, understanding,
false alarms and misses. A finished four-view interface is not promised.

**6. Retire completed strategies.** This implementation plan owns the
one-time v0.7 strategy closeout assignment, recorded as one grouped board
row owned by the release-closeout agent before this plan archives.
Retire the delivery-sequence note at the v0.7 cut, or when superseded or
cancelled, after every item has a delivered outcome or explicit live home.
For other source notes, use
`dev/strategy/2026-11-02-codex-v07-delivery-sequence.md`'s retirement table: archive
only after their whole scope is delivered or explicitly dispositioned,
move lasting guidance to its proper home, and repair live links.
Unfinished scope cannot disappear into an archive. Broad living registers
remain active while they have work. This creates no new archival gate
or recurring inventory.

## Rationale

Reduce discovery cost and connect architectural advice to concrete action.
Share data and records; do not mistake a colorful picture for verification.
The pilot can reject graphics that cost more than they help.

## Alternatives considered

Doing nothing costs least but leaves discovery manual. Mandatory third-party
analyzers add dependencies and maintenance. A full new review platform adds
premature interface and service costs. Recommend the shared static core and
bounded pilot; optional external tools remain separately assessed.

## Documentation / doctrine surface

Update the selected module, rubric, existing reuse prompts and install/script
registry; keep adopter edits and vendor neutrality.

Proposed paths:
- `templates/modules/team-gated/code_map.py`
- `tools/code_map.py`
- `bootstrap/tests/test_code_map.py`
- `dev/strategy/2026-11-02-codex-v07-delivery-sequence.md`

## Evidence / verification plan

### Tests required

Exercise real command and installed copy; check minimal, mixed-language,
malformed-source, link/escape and control-character cases. Never import or run
candidate code. Place focused checks in `bootstrap/tests/test_code_map.py`.
Use existing `test_reference_scripts.py`,
`test_manifest.py`, `test_scaffold.py` and `test_module_merge.py`
under `bootstrap/tests/` for affected contracts.

### Examples / smoke checks

Demonstrate a genuine reuse lead, justified copy, unsupported language and
missing capability evidence. Check offline output, bounded traversal,
path containment and escaped repository-controlled display data.
Run standing prose gates. No implementation experiment has yet run.

#### Security preflight

S1: repository text is untrusted input, not instructions or authority.
S2: implement no-import/no-execution and escaping probes through the real entry.
S3: selected module owns use; wording: "The map is evidence for investigation."
S4: unreadable, incomplete or stale input remains visibly incomplete.
S5: similarity and static relationships can mislead; no network, automatic
refactor, deletion, publication or candidate execution is authorized.

### Independent scientific check

N/A: no scientific equation changes; capability claims still need evidence.

## Signals the change is wrong

Nobody uses the map, false positives dominate, semantic claims lack evidence,
or collection, checklists and strategy notes multiply.

## Scope delta

**Scope delta**: preserved -- shared foundations and exploration, not a finished interface.

## Assurance path

**Assurance path**: high-assurance -- untrusted repository inputs and install contract.

