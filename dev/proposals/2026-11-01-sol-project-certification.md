# Let projects choose what certification covers

**Author**: Codex Sol (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — changes protected methodology and shipped verification guidance.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Let each project certify the affected software without making a whole-project test run a universal requirement.

## Decision summary

Let a project's Maintainer choose what certification covers and when broader
checks run. A small change can then earn certification from its affected
checks, without rerunning unrelated components. Preserve every applicable
accepted, safety, security and release requirement. This adds a short project
policy in existing guidance, not a new tool or review stage.

## Context

[Issue #33](https://github.com/MSUHydrogeology/cairn/issues/33) reports roughly
an hour each for unit and runtime-engine suites, plus longer model-evidence
runs. These are reported, not measured here. Its local remedy
makes certification scoped and whole-suite checking a separate obligation.
The accepted scoped-change proposal separates change verification from full
tree certification; the accepted model-evidence proposal clarifies evidence
ownership but explicitly preserves the configured full-suite contract.
Neither delivers the broader adopter choice now requested.

`templates/core/AGENTS.md`, Verification, still defines certification as the
configured full suite and static gates, including before release cuts.
`docs/methodology/plans.md`, Tree certification, says a green commit certifies
every preceding change. That inference is too broad for scoped evidence.
Cairn's own release and re-anchor requirements need not prescribe adopters' releases.

## Proposal

Make certification a recorded claim about specified software at a tested
commit. Require each project's Maintainer to choose its meaning, scope and
triggers in the existing Verification section before using that claim. Offer
a short adaptable example: affected checks certify a change; separately,
project-chosen integration or release checks assess the combined software.
A project can instead retain whole-project certification. Do not require a whole suite or policy menu.

A scoped claim names affected components, consumers and integration paths,
checks, results and omissions using existing evidence records. It cannot
certify unrelated software or automatically certify every ancestor. Missing
known required coverage keeps that claim open; uncertainty widens coverage to
the relevant owning families and integration paths. Existing independent
review challenges coverage where the lifecycle requires it. A trivial change
keeps its existing author-owned evidence path. No new review is added.

The project policy states when broader checks run and what a failure blocks.
It may choose component releases, scheduled integration, pre-push checks,
whole-suite release checks or other justified boundaries. Dependencies and risks determine coverage; duration cannot exempt a check. A failure contradicting an earlier scoped claim
reopens that claim; an unrelated failure does not invalidate passing evidence
for unaffected software. Applicable requirements still block their named
operation until satisfied.

A policy change does not silently remove an existing required test, accepted
criterion, scientific control, safety/security obligation or release check.
Identify affected existing obligations and obtain the Maintainer's explicit
change through the applicable lifecycle before replacing or rescheduling
them. Until then they remain owed. Required checks cannot disappear because
a suite was renamed or divided. Retain work-specific scientific evidence and
its controls. Preserve historical records and existing plan contracts unless
explicitly revised; no archive backfill.

Cairn itself retains its configured whole-tree certification pair, triggers,
release and re-anchor ceremonies, guard and security checks. Change only its
wording that presents those local choices as requirements for all adopters.
Do not change executable selection, installer behavior or trust machinery.

## Rationale

A hydrology component fix may require its tests, downstream consumers and a
shared-data integration check while leaving an independent engine untouched.
No time saving is measured here.
Use existing records.

## Alternatives considered

Keep current rules: no work, but adopters inherit full-suite certification.

Rename scoped verification to certification universally: modest prose work,
but removes the choice for projects that value whole-project certification;
still needs clear broader-check obligations.

Project-chosen certification: align guidance and maintain a short local policy. It avoids mandatory
whole-suite costs while retaining explicit coverage and requirement ownership.

Recommendation: project-chosen certification; adopter scale and risk vary. No new machinery or recurring review.

## Documentation / doctrine surface

Prescription: `templates/core/AGENTS.md` and aligned self-hosted `AGENTS.md`.
Align both plan and proposal templates, `docs/methodology/plans.md`,
`docs/methodology/dual-review.md`, and lifecycle guidance where it assumes
universal full-tree certification. Search other readers, shipped modules and
examples before editing. Deliberation stays here. Keep Cairn's release and
re-anchor runbooks' concrete commands unchanged.

## Evidence / verification plan

### Tests required

Map final changed paths using `tools/test_tiers.py` and search direct readers
and byte pins, including `bootstrap/tests/test_certifying_run_rule.py`,
`bootstrap/tests/test_verification_boundaries.py` and
`bootstrap/tests/test_review_and_verification_rules_ship.py`. Adjust tests of
universal wording while preserving tests of Cairn's local requirements.

### Examples / smoke checks

Run applicable claim, link, snippet and neutrality gates. Exercise three
illustrative policies through installed guidance: a component change with an
unaffected slow engine; a shared contract requiring wider consumer checks;
and a release with an existing whole-suite obligation. Record reviewer
judgments: no unrelated run forced in the first, no missing consumer accepted
in the second, no existing obligation waived in the third. Include the
whole-project policy alternative. These are procedural examples, not machine
proof of coverage. Final implementation records wide Boundary B; no suite is
requested for this proposal.

#### Security preflight — five questions, answered in writing

S1: Maintainers choose policy; authors supply coverage evidence. S2: Omission
examples challenge waiver and scope; not yet exercised. S3: Existing authors
and reviewers apply requirements at their existing stages. S4: Known missing
required evidence keeps the affected claim or operation open. S5: A plausible
incomplete mapping can miss a dependency; no automatic coverage guarantee is
claimed.

### Independent scientific check

N/A: changes evidence governance, not a scientific result.

## Signals the change is wrong

An adopter still must run unrelated suites solely to certify a small change;
a scoped run claims the whole tree; or an existing required check disappears
without explicit authorized replacement.

## Scope delta

Opening scope. This would replace the universal full-suite definition retained
by the two accepted proposals; it does not revise their historical records.

## Assurance path

**Assurance path**: high-assurance

Authoring: approximately 10 minutes; tokens unknown. Issue #33 read directly.
No suite or adopter software run.
