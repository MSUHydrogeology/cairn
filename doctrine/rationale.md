# Rationale — why this method

Cairn is not invented from first principles. Its practices answer
to a body of research on how software is built with AI agents, how
multi-agent systems are organized, how trust in AI is calibrated,
how scientific software earns rigor, how agents coordinate, and how
scientific peer review works. This document records that grounding
— the **six framework anchors** — and then states, honestly, where
Cairn *follows* the literature and where it deliberately *diverges*
from it.

A reader adopting Cairn does not need to read the sources. But the
methodology should be able to show its work: every practice in
`doctrine/` traces to a reason here.

## The six framework anchors

**1. Interaction taxonomy.** Treude & Gerosa (2025), *How
Developers Interact with AI* (FORGE 2025; arXiv:2501.08774), maps
eleven distinct human-AI interaction types across the software
lifecycle. It anchors the claim that "using AI to build software"
is not one activity — Cairn's role roster (`roles.md`) exists
because different lifecycle stages are different kinds of work.

**2. Multi-agent SDLC role design.** Liu et al. (2025), *LLM-Based
Multi-Agent Systems for Software Engineering* (ACM TOSEM;
doi:10.1145/3712003), systematically reviews how multi-agent
systems assign roles across the lifecycle. Cairn's roster is
positioned against it — including one deliberate divergence
(below).

**3. Trust and governance maturity.** Steinmetz et al. (2025), the
*Trust Calibration Maturity Model* (SAND2025-00999O;
arXiv:2503.15511), gives five dimensions for characterizing AI
trustworthiness — performance characterization, bias & robustness,
transparency, safety & security, usability. It anchors Cairn's
insistence that claims about the team's own discipline be
*measurable*, not merely asserted.

**4. Scientific-software rigor.** Bridgeford et al. (2025), *Ten
Simple Rules for AI-Assisted Coding in Science*
(arXiv:2510.22254), with the risk-side companion in *Nature
Computational Science* (2025), *Threats to scientific software
from over-reliance on AI code assistants*
(doi:10.1038/s43588-025-00845-2). Together they anchor the
discipline that scientific software carries stakes ordinary
software does not — a wrong result that *looks* right is the
failure mode — so testing, validation, and review are not
optional.

**5. Inter-agent communication patterns.** Two literatures.
*Cognitive stigmergy* — Ricci et al. (2007), *Cognitive Stigmergy*
(LNAI 4389); Crowston on stigmergic coordination in software
development — describes agents coordinating through persistent
shared artifacts. *Direct agent protocols* — Ehtesham et al.
(2025), *A Survey of Agent Interoperability Protocols*
(arXiv:2505.02279) — describes the real-time message-passing
protocols (MCP, A2A, ACP) dominant in 2025. And *multi-agent
debate* — Du et al. (2024), *Improving Factuality and Reasoning
through Multiagent Debate* (ICML 2024; arXiv:2305.14325) —
describes agents debating to consensus. Cairn's coordination
(`coordination.md`) sits in the stigmergy lineage and treats the
others as a measured, firewalled escalation.

**6. Scientific peer review as a process model.** Cairn's review
system's closest real-world analog is not multi-agent debate but
**scientific peer review** itself — the author / editor / reviewer
division of labor codified by editorial-standards bodies (ICMJE;
the Council of Science Editors), and the open-peer-review taxonomy
of Ross-Hellauer (2017), *What is open peer review?*
(*F1000Research* 6:588). This is the anchor Cairn instantiates
most directly (`dual-review.md`).

## What Cairn contributes

The anchors are the field; the contribution is where Cairn adds
something the surveyed literature does not describe, or sits in a
named-but-uncommon corner of it.

* **The append-only, git-committed deliberation lifecycle.** The
  multi-agent SDLC literature describes role assignment and
  orchestration; it does not center a *durable, append-only,
  reviewable record of the reasoning*. Cairn does (`lifecycle.md`)
  — and that record is the artifact that makes everything else
  inspectable. Its proposal-first shape is, specifically, a
  **Registered Report**: the design and verification plan are
  locked and reviewed before the code, which defends against
  post-hoc *metric p-hacking* the way pre-registration defends a
  study against it.

* **The Dual-Review model.** Two-tier review — Internal to help a
  change land, External to make it prove it should — executed
  across **structural independence**, asynchronously and
  commit-mediated (`dual-review.md`). It is a specialized variant
  of multi-agent debate (anchor 5) with role-asymmetric stances,
  and a faithful instantiation of scientific peer review
  (anchor 6). Its sharpest point: structural independence — a
  different model architecture — is a *more enforceable*
  conflict-of-interest criterion than the institutional
  independence that journal peer review relies on.

* **Stigmergy as a deliberate choice.** Cairn coordinates through
  persistent `dev/` artifacts (the stigmergy lineage of anchor 5)
  rather than through the dominant 2025 real-time agent protocols.
  The literature treats these as alternatives suiting different
  contexts; Cairn's choice is structural and load-bearing, and the
  Coordination module's hybrid design (`coordination.md`) shows
  how to add real-time coordination *without* surrendering the
  recorded-deliberation discipline.

* **Absorbing tests and docs into every proposal.** Rather than
  standing up dedicated Test and Doc agents — the retrofit pattern
  the multi-agent literature describes — Cairn makes testing,
  documentation, and examples *required prompts in the proposal
  template*, where their omission is itself a review finding. This
  is the AI-team-first stance: a project built with the
  methodology from the start need not retrofit a role for what
  should be part of every change.

For a scientific-computing audience, the two differentiators Cairn
leads with are the **recorded deliberation lifecycle** and the
**Dual-Review model**. The rest of the doctrine supports them.

## How the doctrine evolves under evidence

Cairn is a *self-improving* methodology: observed failure modes
become doctrine changes. That feedback loop has its own failure
mode — a team that rewrites a rule on every incident churns its
doctrine faster than anyone can internalize it, and the churn
itself becomes the instability. A framework that taught adopters
to do this would be exporting the failure, not the fix. So the
loop runs under a **rate-limit gate**, stated as core doctrine:

> **No doctrine change from a single incident** unless the
> Maintainer explicitly classifies the incident as high-risk.
> Otherwise the trigger requires one of:
>
> * **Recurrence** — the same failure shape occurs again (a small
>   count within a rolling window; the window length is an adopter
>   choice, recorded wherever the team tracks the recurrence).
> * **Synthesis at a routine boundary** — the session-close routine
>   owner aggregates the period's signal into a *single*
>   doctrine-proposal stub, rather than one proposal per incident
>   (see `session-routines.md` > "Goodnight-time synthesis").

High-risk classification is the Maintainer's, and is itself a
recorded decision, so the audit trail survives on either side of
the gate. Two surfaces qualify:

* a **security surface** — the change closes a vulnerability,
  hardens an authentication path, or removes a credential-leak
  vector;
* a **data-loss surface** — the change prevents irrecoverable loss
  of work that cannot be reconstructed (stronger than "data
  quality": the bar is that the data *can't* be rebuilt).

Any other "this feels urgent" framing falls outside the bypass and
obeys the recurrence requirement.

The gate composes with the measurement discipline (anchor 3) as a
matched pair: the **metrics layer diagnoses** where the apparatus
drifts; the **gate governs how fast the team may act** on that
diagnosis. Metrics diagnose, doctrine adapts under rate-limit, and
the loop closes at a routine boundary rather than
incident-by-incident — the structural ward against
measurement-driven over-correction.

## Where the rationale is still thin

Honesty is part of the method. Two areas the anchors expose as
under-built — carried as named follow-ups, not hidden:

* **Measurement.** Anchor 3 asks for *measurable* trust. Cairn
  ships the infrastructure for a lifecycle-metrics layer and a
  baseline, but a single baseline is not yet a trend; the
  longitudinal evidence is future work.
* **Scientific-correctness interlock.** Anchor 4's failure mode —
  a wrong result that looks right — is only partly addressed by
  structural review. Catching *scientific*, as opposed to
  *structural*, error without the Maintainer in the loop is an
  open problem Cairn names but does not yet solve.
