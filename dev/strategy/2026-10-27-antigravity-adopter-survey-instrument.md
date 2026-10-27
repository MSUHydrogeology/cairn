# Outside-adopter feedback survey and interview instrument

**Author**: Antigravity (Strategy)
**Model**: Gemini 3.8 Flash
**Date**: 2026-10-27
**Status**: draft
**Type**: product-strategy
**Surfaces this would feed**: [`dev/PLANNING.md`](../PLANNING.md) v0.6 candidate "Outside-adopter interview & testimonial (Stid)"; [`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md`](2026-07-08-claude-broad-look-skeptical-review.md); GitHub Issue #19; eventual adopter case study.

## The question / felt gap

Every deployment of Cairn to date (`Cairn`, `modflow_tools`, `LHM`, `Assai`) has shared one Maintainer. As established in the adopter audit ([`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md`](2026-07-08-claude-broad-look-skeptical-review.md)), completing `scaffold.py install` proves the Python scripts run; it does not prove an outside scientist understood the obligations they agreed to, or that the deliberation lifecycle repaid its token and cognitive cost on their project.

The Maintainer has identified an active outside adopter (Stid). Rather than conducting an unscripted conversation that risks yielding vague impressions, this note designs a structured **survey instrument and interview protocol**. It is intentionally staged here first—not sent immediately—so the Maintainer can refine the questions, calibrate the burden, and choose the right timing for outreach.

## Method *(grounded, falsifiable — verify-before-asserting)*

* **Prior art surveyed:** Reviewed the skeptical audit findings (`2026-07-08-claude-broad-look-skeptical-review.md`), GitHub Issue #19 (domain correctness vs. structural review), and Issue #31 (agent readability and plan token costs).
* **Falsification criteria:**
  * If the adopter reports that agents repeatedly bypassed proposal/plan gates or that review passes only mirrored linter output, the Dual-Review model does not yet justify its overhead for solo external teams.
  * If the adopter cannot restate their Decision obligations or found `AGENTS.md` impenetrable, the plain-language and comprehension precondition has failed its primary adopter test.

## Findings: The Instrument Design

A two-tiered instrument balances minimal respondent burden (a 5-minute async survey) with the depth of a 15-minute structured interview.

### Tier 1: The Asynchronous Feedback Questionnaire (5–8 minutes)

```markdown
### Cairn Outside-Adopter Feedback Survey

#### 1. Context & Setup
* Repository type: [ ] Simulation model  [ ] Data pipeline  [ ] Numerical library  [ ] Tooling/CLI  [ ] Other: ___
* Host platform: [ ] Windows (native)  [ ] Windows (WSL)  [ ] macOS  [ ] Linux
* Installation experience:
  - Did `scaffold.py install` complete cleanly without manual intervention? [ ] Yes  [ ] No
  - Rate setup friction (1 = completely seamless, 5 = confusing/blocked): [ 1 | 2 | 3 | 4 | 5 ]

#### 2. Agent Deliberation in Practice
* How well did AI coding agents stay within Cairn's lifecycle boundaries?
  [ ] Consistently followed proposal -> plan -> code review
  [ ] Occasionally drifted or attempted bare commits
  [ ] Constantly fought or ignored the rules
* Review effectiveness:
  - Did code review / falsification passes catch real bugs or design flaws before commit? [ ] Frequently  [ ] Occasionally  [ ] Never / False alarms only
* Cost vs. Value:
  - Did the append-only deliberation trail repay its token/time cost? [ ] Easily  [ ] Break-even  [ ] Too heavy for routine changes

#### 3. Scientific Software Rigor
* Did Cairn help with domain validity (units, boundary conditions, physical invariants)?
  [ ] Yes, significantly  [ ] Moderately  [ ] No, reviews remained purely structural/syntactic
* How valuable is the git-committed deliberation trail for scientific reproducibility?
  [ 1 = Essential / High confidence | 2 | 3 | 4 | 5 = Low value / Not worth it ]

#### 4. Open Reflections
* What was the single biggest friction point or source of confusion?
* What was the single most valuable habit or guardrail Cairn introduced?
```

### Tier 2: The Semi-Structured Interview Protocol (15 minutes)

Designed for a synchronous or recorded voice/chat walkthrough to capture nuanced quotes and testimonials:

1. **The Entry Walkthrough:** "When you first opened `AGENTS.md` and ran the installer, what made immediate sense, and what felt like unnecessary jargon or machinery?"
2. **Day-to-Day Agent Pairing:** "Describe a moment where Cairn saved you from a bad agent hallucination or architectural regression. Describe a moment where you felt bogged down by the process."
3. **Scientific Credibility:** "Has having git-committed deliberation files changed how you discuss AI-assisted changes with peers, co-authors, or reviewers?"
4. **Peer Advice & Testimonial:** "If a colleague asked whether they should adopt Cairn for their scientific codebase, what would you tell them? In one or two sentences, what is the core difference Cairn made for your team?"

## Options

1. **Do nothing / ad-hoc chat:** Rely on informal impressions in chat when Stid mentions Cairn. *Risk: yields anecdotes rather than actionable diagnostic evidence on comprehension and friction.*
2. **Deploy async survey only (Tier 1):** Send a lightweight Google Form or Markdown questionnaire. *Advantage: respect adopter time; collects quantitative ratings. Disadvantage: loses spontaneous narrative context.*
3. **Staged deployment: Async survey + optional follow-up interview (Recommended):** Provide the Tier 1 questionnaire first. If the responses show interesting failure modes or strong enthusiasm, invite him to the 15-minute Tier 2 interview to capture a public testimonial.

## Recommendation

* **Adopt Option 3.** Keep the survey instrument staged in this strategy document on `0.5-dev`.
* **Timing:** Do not send immediately. Reach out after `0.5.0` ships, or at a natural pause in Stid's project milestones, so feedback evaluates Cairn's hardened 0.5 onboarding rather than interim development artifacts.
* **Consent & Attribution:** Ensure explicit permission is asked before using any quote as a public testimonial or case study in `README.md` or `docs/`.

## Open questions

* **Form factor:** Should Tier 1 be delivered as an interactive Google Form, an emailed Markdown template, or a private GitHub discussion? (A private GitHub issue/discussion fits developer workflows best).
* **Testimonial placement:** Once gathered, where does an outside testimonial live? Recommended: a dedicated "In the wild" section in [`README.md`](../../README.md) or an adopter documentation page.
