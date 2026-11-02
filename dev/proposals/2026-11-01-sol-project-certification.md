# Supply testing architecture that makes scoped certification dependable

**Author**: Codex Sol (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — protected methodology and shipped verification guidance.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Give agents practical testing defaults so small changes earn scoped certification without making scientists design the testing process.

## Decision summary

Cairn supplies testing architecture; agents apply coverage defaults. Scientists
need not design certification or approve coverage per proposal.
Default to certifying affected behavior, with broader checks for shared
boundaries and project operations. Improve guidance; add no infrastructure. Required checks remain owed.

## Context

[Issue #33](https://github.com/MSUHydrogeology/cairn/issues/33) reports roughly
an hour each for unit and engine suites, plus long model runs. These are
reported timings, not measured here. Accepted scoped-verification and
model-evidence proposals retain universal full-suite tree certification.
The Maintainer rejected delegated design in chat, 2026-11-01:

> "Instead, shouldn't this be dictated by good testing architecture provided by Cairn?"

Testing-discipline supplies tiers, contracts, budgets and simulation timescales. Architecture-review examines accumulated structure. Neither supplies a
complete scoped-certification default.
Cairn's own `tools/test_tiers.py` is repository-specific; it is not an adopter
coverage oracle.

## Proposal

Supply the following practical default in core verification guidance, with
examples expanding existing testing-discipline guidance. Use existing runners, directories and dependency information. Reuse existing guides; do not require a new manifest, selector,
service, ledger or architecture-review program.

**Organize around promises and boundaries.** Explain component ownership;
unit checks for local behavior; contract checks for public interfaces and data
formats; integration checks for connected components; and small workflow
checks through real entry points. For simulations, retain real equations on small domains, analytical or
convergence benchmarks when relevant, and work-specific long-run evidence.
Runtime cannot prove coverage.

**Select by effects.** The implementing agent searches changed behavior,
callers, imports, configuration/data readers and public entry points, then
maps existing checks to affected components and consumers in the current
implementation record. Run applicable standing gates too. Add or extend a
test only for a plausible uncovered fault. A local change defaults to these
checks, not the entire codebase. Independent review challenges the selection
within the existing lifecycle; trivial work retains author-owned evidence.
No extra approval.

**Widen for shared effects.** A changed contract, common infrastructure,
cross-language seam, solver/physics behavior or uncertain dependency requires
owning test families and relevant consumer/integration paths. State uncertainty. Missing known required evidence keeps the work open. If tangled
architecture prevents defensible selection, agents explain the missing seam
and propose the smallest useful remedy; the existing optional architecture
review is available, not imposed for each change or adoption. Do not hide gaps or automatically demand all tests.

**Certify a stated scope.** Existing records name tested commit, components,
checks, results and omissions. Scoped certification covers those behaviors;
unrelated components and untested combined behavior remain unclaimed. It does
not certify every preceding change. A later discovered failure that
contradicts the claim reopens it.

**Separate project operations.** Cairn's starting guidance recommends affected
checks for routine changes and a representative cross-component workflow at
integration/release boundaries. Agents adapt this once to existing project
commands and dependencies, identifying required security, safety, scientific
and release checks. The Maintainer sets high-level operational needs and
material exceptions, using an agent's concrete recommendation and costs.
Whole-suite runs are optional unless an applicable project requirement makes
them mandatory. No universal full-suite trigger. Failures block applicable claims or operations.

Existing accepted criteria, required suite checks, scientific controls and
release/security ceremonies remain owed until explicitly changed through the
applicable lifecycle. Splitting or renaming a suite does not waive them.
Preserve historical records and unrevised plans. Cairn itself retains its
full-tree certification pair, triggers, release/re-anchor and security checks.

## Rationale

For LHM-like software, a local input-reader fix can check malformed inputs,
the data contract and a small consuming workflow without an unrelated engine
suite. A shared solver change needs relevant numerical benchmarks and
connected workflows. Illustrative; LHM dependencies uninspected.
Cairn supplies the reasoning pattern; agents establish the actual mapping.

## Alternatives considered

Keep current rules: free, but universally full-suite. Let each Maintainer design policy: less Cairn
guidance, but transfers testing expertise and maintenance to scientists.
Automated impact analysis: potentially useful where already available, but
building it here adds infrastructure and cannot establish all dynamic effects.

Recommendation: practical defaults applied by agents using existing tools.
Cost is aligning guidance and examples, plus ordinary coverage reasoning;
Maintainers handle meaningful project choices, not routine test selection.

## Documentation / doctrine surface

Align core and self-hosted `AGENTS.md`, plan/proposal templates and
`docs/methodology/plans.md`, `docs/methodology/dual-review.md` and lifecycle
wording. Align testing-discipline and its self-hosted copy; reference
architecture-review without changing its optional selection. Search consumers
and examples. Core must remain usable without optional modules. Leave engine,
installer and ceremony commands unchanged. Prescription ships; deliberation
stays here.

## Evidence / verification plan

### Tests required

Map changed files with `tools/test_tiers.py`; search direct readers/pins,
including certifying-rule, verification-boundary and shipped-rule tests in
`bootstrap/tests/`. Preserve Cairn-specific ceremony assertions. No automatic coverage guarantee.

### Examples / smoke checks

Exercise installed guidance for local reader, shared solver, uncertain
cross-component dependency, and existing mandatory release-check cases.
A reviewer must find sufficient coverage without scientist-designed policy,
no unrelated suite forced, no missing known consumer accepted and no existing
requirement waived. Also exercise core without optional modules. Run applicable
claim, link, snippet and neutrality gates; final implementation gets wide
Boundary B. No proposal suite.

#### Security preflight — five questions, answered in writing

S1: Agents supply mappings; Maintainers own direction. S2: Omission examples
challenge gaps; not run yet. S3: Existing authors/reviewers apply coverage at
existing stages. S4: Missing required evidence keeps work open. S5: Plausible
incomplete mappings can miss dependencies; no automatic guarantee.

### Independent scientific check

N/A: no scientific result changes.

## Signals the change is wrong

Scientists must design routine coverage; tiny changes force unrelated suites;
a scoped claim implies whole-tree assurance; or required checks disappear.

## Scope delta

Widened: replace self-designed policy with supplied architecture and defaults.
Fresh usual and Security reviews required. Earlier reviews remain historical.

## Assurance path

**Assurance path**: high-assurance

Revision: approximately 8 minutes; tokens unknown. No suites run.

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


## Revision -- Codex Sol (Strategy) -- 2026-11-01

**Elapsed**: approximately 8 minutes. **Tokens**: unknown.

Accepted the Maintainer direction: Cairn supplies architecture and defaults;
agents map effects and recommend checks. Maintainers handle high-level project
needs and meaningful exceptions, not coverage design per proposal. Added
module integration and core-only examples; no new infrastructure or Decision.
Scope widened, so fresh usual and Security reviews read this revision.

## Review -- Codex Sol (Reviewer) -- 2026-11-01

Reviewed commit: 55637307b6284f6bef3eff6c0958139f7bd2299f
Target: widened architecture and scoped-certification default
Prior findings: none
Assurance path: high-assurance

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. Agents map effects and apply a concrete local/widened default; scientists decide high-level needs and material exceptions, not routine selections. Existing requirements remain owed. -- Proposal, Select by effects and Separate project operations.
2. **Best alternative.** Keep the current full-suite rule: simpler to explain, but it forces unrelated suites at named operations. Automated impact analysis adds machinery without resolving all dynamic dependencies. -- `templates/core/AGENTS.md`, Verification; proposal Alternatives.
3. **What would show it wrong?** Core-only installed guidance requiring scientists to design routine coverage, missing a known consumer, or forcing an unrelated suite would defeat the default. The proposed installed examples challenge those outcomes. -- Proposal, Examples / smoke checks and Signals.

Existing testing-discipline guidance supplies tiers, contracts, budgets and simulation timescales; the architecture-review module exists. The proposal reuses these and avoids a new selector or review program. -- `templates/modules/team-gated/testing-discipline.md`; `templates/modules/team-gated/architecture-review.md`; Proposal.

Coverage: read the committed revision, shipped core verification and named module guidance. Did not exercise installed examples, inspect LHM dependencies, measure timings or perform Security Review.

## Security Review -- Codex gpt-6.1-sol -- 2026-11-01 (widened scope)

Reviewed commit: d3398d2262d3b6aaf724b98df4fb60e195eb9731  
Target: supplied testing architecture, agent defaults and core-only use  
Prior findings: earlier S1 assurance disclosure retained; fresh pass for widened scope  
Assurance path: high-assurance

**Tier**: Security Review  
**Findings**: none  
**Verdict**: ACCEPT as framed; recommendation, not a Maintainer Decision.  
**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. Cairn supplies the local/widened defaults; agents search actual effects, consumers and entry points and record selection with implementation. Scientists set high-level needs and material exceptions, not routine coverage. Known required checks remain owed; named trust-boundary/heavy rules are not replaced. -- Proposal, Select by effects, Widen for shared effects and Separate project operations; governing Review rule.
2. **Best alternative.** Keep universal whole-suite certification: easier selection but unnecessary work for independent components. Automated impact machinery cannot prove dynamic dependencies and would add infrastructure. Existing test organization and optional architecture guidance support the supplied default without making modules or a review program prerequisites. -- Proposal, Alternatives and core-only requirement; testing-discipline and architecture-review module selection/composition text.
3. **What would show it wrong?** Core-only guidance asking scientists to invent coverage, a familiar local interface hiding changed trust or a shared consumer, or duration excusing a required security check. Effect mapping, widening under uncertainty, unchanged obligations and installed local/shared/uncertain/mandatory examples challenge those outcomes; no automatic coverage guarantee is claimed. -- Proposal, Examples, S4/S5 and requirement-preservation paragraph.

No new finding. The revision preserves S1's scoped assurance limit, keeps concrete Cairn release/re-anchor requirements, and distinguishes architecture guidance from building infrastructure. Widening covers owning families and connected paths.

Coverage: examined committed widened proposal, ordinary review, current proposal template, governing heavy triggers and named module content. Did not validate LHM architecture, exercise installed examples, measure savings or run suites. Final dependency mapping remains unverified.
