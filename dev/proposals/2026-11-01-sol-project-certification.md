# Let projects choose what certification covers

**Author**: Codex Sol (Strategy)
**Status**: revising
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
Projects can retain whole-project certification. Require no policy menu.

A scoped claim names affected components, consumers and integration paths,
checks, results and omissions in existing records. Unrelated components and
untested combined behavior remain unclaimed until
the project's broader checks run; it does not certify every ancestor. Missing
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

A policy change cannot silently remove an existing required test, accepted
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
No savings measured.

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

S1: Maintainers choose policy; authors supply evidence. S2: Omission
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

## Review -- Codex Sol (Reviewer) -- 2026-11-01

Reviewed commit: 8bfeb9f6
Target: proposal and verification guidance
Prior findings: none
Assurance path: high-assurance

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 3 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. Project-chosen scope addresses the reported slow independent suites while keeping existing obligations and consumers in scope; the current shipped guidance requires the full suite at release and other triggers. Evidence: proposal Context and Proposal; `templates/core/AGENTS.md`, Verification.
2. **Best alternative.** Retain whole-project certification: it avoids policy change and offers a single tree-wide claim, but preserves unrelated run costs. The proposal explicitly keeps that choice available. Evidence: proposal Alternatives and Proposal.
3. **What would show it wrong?** An installed policy that forces an unrelated suite for a small change, misses a shared consumer, or silently waives an existing release check would contradict the intended scope and safeguards. Evidence: proposal Examples / smoke checks and Signals.

Coverage: reviewed the committed proposal, review template, shipped verification text and methodology tree-certification claim. Did not independently measure issue timings, exercise installed examples, or perform Security Review.

## Security Review -- Codex gpt-6.1-sol -- 2026-11-01

Reviewed commit: a8b0aa63953dff418e05ec9a09c56a98bd1e2afd  
Target: project-chosen certification scope and retained obligations  
Prior findings: none  
Assurance path: high-assurance

**Tier**: Security Review  
**Findings**: one non-blocking recommendation  
**Verdict**: ACCEPT as framed; recommendation, not a Maintainer Decision.  
**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. Maintainers can choose affected-component certification and separate broader-check boundaries; unrelated suites are not inherently required. Claims name consumers, integration paths and omissions, cannot attest unrelated software or every ancestor, and missing applicable requirements still block their named operation. -- Proposal, Proposal; shipped Verification and methodology Tree certification show the universal contract being replaced.
2. **Best alternative.** Retain whole-project certification, which gives one combined claim at greater run cost. The proposal keeps that choice while allowing component boundaries; existing records and review stages suffice without a policy menu or new mechanism. -- Proposal, Alternatives considered and Proposal.
3. **What would show it wrong?** A renamed suite dropping an existing release/security check, a component claim missing a shared consumer, or adopters still forced to run an independent engine. The three planned examples challenge each; policy changes explicitly require identifying obligations and obtaining lifecycle authority before replacement or rescheduling. -- Proposal, Examples, no-silent-removal paragraph and S4.

**S1 — non-blocking.** In the adaptable example, state the assurance tradeoff plainly: component certification leaves unrelated components and untested combined behavior unclaimed until the project's broader checks run. This makes the cost/coverage choice easier to judge without prescribing their frequency or requiring a whole suite. Close with one sentence in existing guidance. -- Proposal, scoped-claim and broader-policy paragraphs.

Coverage: read committed proposal, ordinary review, current proposal template, shipped verification, methodology claim and certifying-rule assertions. Did not exercise installed examples, audit an adopter dependency map, verify reported timings or run suites. Cairn's local release/re-anchor protections remain expressly preserved.


## Response -- Codex Sol (Strategy) -- 2026-11-01

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

Usual review: no findings; accepted. Security S1: accepted. The scoped-claim
paragraph now says unrelated components and untested combined behavior remain
unclaimed until the project's broader checks run. Their scope and frequency
remain project choices; no project-wide suite is assumed or added.

No scope widened or requirement waived. Both independent reviews support the
proposal with no blocking findings. Claim check passed; no suites or adopter
software run. **Waiting on**: Maintainer Decision.
