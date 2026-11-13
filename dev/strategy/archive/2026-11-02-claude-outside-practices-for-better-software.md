# Outside practices for better software — what Cairn can borrow

**Author**: Claude Opus 5.5 (Strategy)
**Model**: Claude Opus 5.5 (`claude-opus-5-5`); sources read by one Claude Sonnet 5.5 agent, the OpenAI post by Claude Opus 5.5
**Date**: 2026-11-02
**Status**: archived
**Type**: comparative-research
**Surfaces this would feed**: [`dev/PLANNING.md`](../../PLANNING.md) v0.7 rows; [`templates/modules/team-gated/testing-discipline.md`](../../../templates/modules/team-gated/testing-discipline.md); [`dev/plans/_template.md`](../../plans/_template.md) acceptance criteria; [architecture growth](2026-10-30-claude-architecture-growth.md); [judicious testing](2026-10-27-antigravity-judicious-testing-and-simulation-verification.md)

## Conclusion first

The outside work that would most improve the software Cairn adopters build is
about **tests that catch real faults**, not about more planning or review.
Three practices are worth a proposal for the shipped testing module:
characterization tests for functions that carry a scientific claim, property
tests for invariants, and mutation checks on the lines a change touched. A
second, smaller idea is **acceptance criteria written so they can be tested**.
The OpenAI harness report independently supports the v0.7 architecture-growth
direction. It also shows two choices Cairn should keep making differently:
optional human review and automatic merging.

Cairn already covers most of "Ten Simple Rules for AI-Assisted Coding in
Science". The clearest gap is its warning that agents weaken or fake tests to
make them pass.

## The question

The Maintainer asked (chat, 2026-11-02) which outside projects hold ideas that
help build better software, a focus for Cairn going forward. The trigger was
Google's Elephant–Goldfish Model, already cited on the v0.7 "reading old code"
row.

## Method

- **Search:** a web search on 2026-11-02 for spec-driven development,
  agent skill frameworks, harness engineering, agent testing and
  AI-assisted scientific coding.
- **Primary reading:** one Sonnet agent fetched eight primary pages. One
  fetch failed, and I read that page (the OpenAI post) in the browser.
  Fetched pages were summarized by a model, so their details are second-hand.
- **Not read:** the skill files and prompts of any project, the spec-kit
  walkthrough, Kiro pages beyond specs, and Trail of Bits' earlier posts.
  Seen in search results only: BMAD Method and Agent OS.
- **What would show this wrong:** the testing practices fail to find faults in
  a real adopter's scientific code, or cost more review than they save.

## Tests that catch real faults

- **Characterization tests** (Barba, arXiv 2609.11728, section 2.1). These pin
  the trusted behavior of each function that supports a scientific claim. The
  paper argues about 30 such tests are worth more than 300 tests of trivial
  accessors. It is an opinion essay with no measured outcome.
- **Property tests found by an agent** (Anthropic, 14 January 2026). An agent
  states rules the code should always obey, writes Hypothesis tests, runs them
  and reflects before reporting. It tested more than 100 Python packages,
  including NumPy, SciPy and Pandas, and filed 5 bugs with patches, several
  merged. The `numpy.random.wald` fix cut relative error by nearly ten orders
  of magnitude. Precision before filtering was low: of a manually reviewed
  sample, 56% were valid and 32% worth reporting. Each bug took a human expert
  about an hour, and one first patch was wrong.
- **Mutation checks for agents** (Trail of Bits, 1 April 2026). Mutation
  testing plants deliberate bugs and checks that the tests catch them. Its
  limit is runtime: a 5-minute suite against 1,000 mutants takes about 83
  hours. Running only the changed lines, and parking results so they can
  resume, keeps it affordable. The post warns that tests generated from
  surviving mutants can lock in a bug unless the expected behavior is checked
  first. Its core tool, mewt, is AGPL-3.0, so Cairn could recommend it but
  not ship it.
- **Red before green** (Superpowers; Ten Simple Rules, rule 6). Write a
  failing test, watch it fail, then write the code. Rule 6 also warns that
  agents edit tests or leave placeholder logic to fake a pass.

**Fit.** These belong in the shipped `testing-discipline` module as adopter
guidance. They complement, rather than repeat, the judicious-testing note's
work on Cairn's own suite. Hypothesis and mutation tools stay optional
recommendations, since what Cairn ships uses the standard library only.
Cairn's reviewers already mutate by hand when a claim names a set; a
changed-lines tool would make that cheaper.

## Testable acceptance criteria

- **EARS sentences** (Kiro). Each requirement takes the form "WHEN
  *condition* THE SYSTEM SHALL *behavior*", which makes it clear and testable.
  Only this one form was confirmed on the pages read.
- **Bug records with three parts** (Kiro). A bug spec states current,
  expected and unchanged behavior. "Unchanged" matches Cairn's defect-fix
  rule: restore a promise without changing others.
- **A verdict on each bug test** (Spec Kit). The test of a fix is marked
  verified, partial or failed.

**Fit.** These could be optional prompts in the plan template's acceptance
criteria. Each criterion then names its own test, which also helps the
Boundary B record. Spec Kit's clarify, analyze and checklist steps were not
on the README page read, so they are not claimed here.

## Mechanical enforcement and cleanup

OpenAI's harness-engineering post (Ryan Lopopolo, 11 February 2026)
describes a product built over five months with no hand-written code: about a
million lines and roughly 1,500 merged pull requests. Its practices:

- `AGENTS.md` is a map of about 100 lines, with depth in an indexed `docs/`
  folder. Plans, completed plans and a technical-debt tracker are committed.
- Rules are enforced by custom linters and structural tests. Lint messages
  tell the agent how to fix the violation. When documentation is not enough,
  the rule becomes code.
- Recurring background agents scan for drift, update a quality grade for each
  domain, and open small refactoring changes. This replaced a Friday cleanup
  that took 20% of the team's week.

**Fit.** This supports architecture-growth recommendations 3 (one home per
critical capability, enforced by a test) and 4 (a routine structure pass).
It adds one cheap idea: write each Cairn check's message as the fix to make.

**Where Cairn differs on purpose.** In that project humans may review but
are not required to, agents merge their own changes, and flaky tests are
often re-run rather than fixed. The post itself calls that irresponsible at
low throughput. Cairn's adopters are scientists who own their results; Ten
Simple Rules says accountability lies with the scientist. Cairn keeps the
Maintainer's Decision and a fresh human-side review.

## Cairn against Ten Simple Rules

My reading against Cairn's current rules (an assessment, not a measurement):

| Rule | Cairn today |
|---|---|
| 1. Learn the domain first | Partly: the independent scientific check, not a general step |
| 2. Frame the problem before coding | Covered: proposal before plan |
| 3. Choose the interaction mode | Partly: model tier, not mode |
| 4. Think through a solution first | Covered: proposal and plan |
| 5. Manage context with files | Covered: committed records, session start |
| 6. Test first; watch for faked passes | Gap for adopters: Cairn freezes its own tests only |
| 7. Use AI for test planning | Partly: testing-discipline module |
| 8. Know when to restart | Partly: context-loss rule, one-tier-up retry |
| 9. Review generated code critically | Covered: fresh review, checks not run stated |
| 10. Refine incrementally | Covered: lanes, one commit per step |

Barba's paper argues that reproducibility practices double as agent context,
and that provenance lives in maintained artifacts rather than conversations.
That is Cairn's own premise, argued by an outside author.

## Seen and set aside

- **Persona swarms** (BMAD Method; search results only). Many specialized
  agents per change; Cairn cut to one review pass per stage.
- **Mandatory installed skills** (Superpowers). Cairn's files work with any
  tool and enforce nothing beyond its safety rules.
- **Loops that run until the agent says "Converged"** (Spec Kit). That is
  self-certification; Cairn requires a reviewer who did not write the work.
- **Discovering a codebase's unwritten standards** (Agent OS; search results
  only). Possibly useful for legacy adopters; it needs a primary read first.

## Recommendation

Add two v0.7 rows and widen one:

1. **Tests that catch real faults.** A proposal for the testing-discipline
   module: characterization tests for claim-bearing functions, optional
   property tests, changed-lines mutation checks, red-before-green, and a
   warning about weakened tests. It changes a shipped template, so it needs a
   proposal.
2. **Testable acceptance criteria.** A proposal for optional EARS-style
   criteria and three-part bug records in the plan template.
3. **Reading old code** row: cite the harness post as corroboration, and add
   fix-instructing check messages to that proposal.

Residual risk: property and mutation tools add triage work, and the Anthropic
figures show most raw findings are not bugs. The proposal should keep a human
judging every reported fault.

## Sources

- [Anthropic: property-based testing](https://www.anthropic.com/research/property-based-testing)
- [Trail of Bits: mutation testing for the agentic era](https://blog.trailofbits.com/2026/04/01/mutation-testing-for-the-agentic-era/)
- [Ten Simple Rules for AI-Assisted Coding in Science](https://arxiv.org/abs/2510.22254) (CC BY 4.0)
- [Barba: Reproducibility in the Age of Agentic AI](https://arxiv.org/abs/2609.11728)
- [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/)
- [Kiro specs](https://kiro.dev/docs/specs/)
- [GitHub Spec Kit](https://github.com/github/spec-kit) (MIT)
- [Superpowers](https://github.com/obra/superpowers) (MIT)
- [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD), [Agent OS](https://github.com/buildermethods/agent-os): search results only
