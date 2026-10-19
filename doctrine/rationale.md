# Rationale — why this method

Cairn is not invented from first principles. Its practices answer
to a body of research on how software is built with AI agents, how
multi-agent systems are organized, how trust in AI is calibrated,
how scientific software earns rigor, how agents coordinate, and how
scientific peer review works. This document records that grounding
— the **framework anchors** — and then states, honestly, where
Cairn *follows* the literature and where it deliberately *diverges*
from it.

A reader adopting Cairn does not need to read the sources. But the
methodology should be able to show its work: every practice in
`doctrine/` traces to a reason here.

## Organizing structure

The anchors fall into a **Foundation plus four thematic clusters**.
The Foundation — Anchor 13, the narrow-waist coordination layer —
is the open-science substrate the four clusters all rest on. It is
not a peer cluster but the layer beneath them: the same thin-stable-
interface principle whether the interface is a data format, a science
protocol, or Cairn's `dev/` tree. The four clusters organize
the anchors by concern: AI and multi-agent collaboration (I), trust
and governance (II), scientific-software rigor and validation (III),
and community, sustainability, and restraint (IV).

**Numbering is canonical and append-only.** Each anchor keeps its
integer from the guide-star, so the harvested set reads non-sequentially
(11, 12, 13, 16, 17) by design — a *harvested* anchor retains its guide-star
identifier rather than being renumbered into sequence. The existing six
(1–6) are regrouped into clusters — not renumbered or rewritten. A newly
*authored* Cairn anchor (one with no guide-star origin) takes the next
unused integer.

| Cluster | # | Theme |
|---|---|---|
| **0 · Foundation** | 13 | Durable neutral coordination layer (hourglass / narrow-waist) |
| **I · AI & multi-agent** | 1 | Interaction taxonomy |
| | 2 | Multi-agent SDLC role design |
| | 5 | Inter-agent communication patterns |
| | 11 | AI-productivity value curve |
| | 12 | Agentic context efficiency |
| **II · Trust & governance** | 3 | Trust and governance maturity |
| | 16 | Comprehension floor |
| **III · Scientific-software rigor** | 4 | Scientific-software rigor |
| | 6 | Scientific peer review as a process model |
| **IV · Community, sustainability & restraint** | 7–9 | Community-maintained scientific software (horizon) |
| | 10 | Trustworthy operation |
| | 17 | Waste and proportional process |

---

## Foundation (Anchor 13) — the durable neutral coordination layer

**13. The hourglass / narrow-waist model.** Beck, M. (2019), *On
the Hourglass Model*, Communications of the ACM 62(7):48–57
([doi:10.1145/3274770](https://dl.acm.org/doi/10.1145/3274770));
Akhshabi, S., & Dovrolis, C. (2011), *The Evolution of Layered
Protocol Stacks Leads to an Hourglass-Shaped Architecture*, ACM
SIGCOMM 2011, 206–217
([doi:10.1145/2018436.2018460](https://dl.acm.org/doi/10.1145/2018436.2018460)).

Cairn's "no vendor lock-in" and "vendor-neutrality" are usually
stated as *features*. They are better understood as one
**architectural principle**: a deliberately minimal, stable
interface layer — a "waist" — between two layers that change at
very different rates. Below the waist: the adopter's project stack
(Fortran, R, Rust, JavaScript, Python). Above it: the AI tooling
acting on the deliberation record (Claude, Codex, Cursor). The <!-- vendor-ok: example AI tools named in the layered description -->
waist itself — plain markdown in a git history — is the durable
asset, kept deliberately minimal so neither the tool layer above
nor the language layer below can capture it. Beck's contribution
is the design rule: a waist works *because* it is kept **minimal
and weak** — only what is strictly necessary — which is exactly
what lets it be implemented on almost any substrate. Akhshabi and
Dovrolis supply the empirical half: a successful waist **ossifies
and survives** for decades precisely because so much comes to
depend on it.

*That minimalism is the single source of both neutralities* —
vendor-neutrality and stack-neutrality are not two features but one
principle seen from two sides. This also explains why the Python
tooling sits *above* the waist (and is therefore independently
replaceable) while the methodology substrate is the waist itself.

---

## Cluster I — AI and multi-agent collaboration

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

**11. AI-productivity value curve.** Two sources ground Cairn's
"slower first, faster later" claim.

*Raw AI speed is partly illusory.* METR (2025), *Measuring the
Impact of Early-2025 AI on Experienced Open-Source Developer
Productivity* (arXiv:2507.09089), found experienced developers
working on their own mature repositories were **19% slower** with
early-2025 AI tools, while believing they were ~20% *faster*.
Closing that perception-vs-reality gap with a recorded, reviewed
process is exactly the friction Cairn front-loads.

*The expensive errors are the late ones.* The cost-of-change
literature — Boehm, B. (1981), *Software Engineering Economics*,
Prentice Hall; Boehm, B. & Basili, V. (2001), *Software Defect
Reduction Top 10 List*, IEEE Computer — holds that defects cost
more the later they are caught. The magnitude is contested (the
classic 100:1 multiplier is weakly evidenced and nearer 5:1 for
small, noncritical systems), so Cairn leans on the *direction*:
catch it in review, not in production.

Together, Anchor 11 is the evidence-based grounding under the
adoption promise — *keep the apparatus only as heavy as your
codebase and team earn* — and under the proposition that Cairn's
front-loaded friction pays back in less rework and fewer
unreviewed scientific changes.

**12. Agentic context efficiency.** Cairn's own `AGENTS.md` and
`RULES.md` are read into every agent session. That always-loaded
surface has a correctness cost, not only a token cost:
*Context Length Alone Hurts LLM Performance Despite Perfect
Retrieval* (EMNLP 2025; arXiv:2510.05381) found accuracy degrades
as input length grows **even at 100% exact-match retrieval**. The
corroborating pattern — position-dependent degradation — is
documented in Liu et al. (2024), *Lost in the Middle: How Language
Models Use Long Contexts*, Transactions of the ACL 12
(arXiv:2307.03172).

This anchor grounds three repository-structure choices:

* **Archive inactive proposals and plans.** Keeping
  `dev/proposals/` and `dev/plans/` lean — moving inactive
  artifacts to `archive/` subdirectories — reduces the
  always-loaded index surface and keeps the checkout's working
  context to live work.
* **Keep `AGENTS.md` compact.** The doctrine's insistence that
  `AGENTS.md` stay thin (pointers, not prose) is a correctness
  property, not only a style preference: a bloated always-loaded
  prefix degrades the agent's accuracy.
* **`RULES.md` as a lookup cache.** The bright-line rules file is
  a compact router — load it always, load the full doctrine
  on-demand. This is progressive disclosure, sized so the
  always-loaded signal is sufficient to route reliably.

The scope of this anchor in Cairn is **repository-structure
grounding only**. Cairn does not ship a context-compiler,
progressive-disclosure automation, or token-budget enforcement
tool; those remain future work.

---

## Cluster II — Trust and governance

**3. Trust and governance maturity.** Steinmetz et al. (2025), the
*Trust Calibration Maturity Model* (SAND2025-00999O;
arXiv:2503.15511), gives five dimensions for characterizing AI
trustworthiness — performance characterization, bias & robustness,
transparency, safety & security, usability. It anchors Cairn's
insistence that claims about the team's own discipline be
*measurable*, not merely asserted.

**16. The comprehension floor.** Review is Cairn's whole engine.
Opaque language quietly switches it off: you cannot review what
you cannot penetrate, so "review and decide" collapses into
"approve." Comprehension is therefore not a courtesy the agent
extends to the human — it is a **precondition of the human's
authority**. A Maintainer who does not understand a change cannot
legitimately decide on it; they can only rubber-stamp it.

Four converging literatures ground the principle:

* **Recipient-designed explanation** — Miller (2019), *Explanation
  in artificial intelligence: insights from the social sciences*
  (Artificial Intelligence 267:1–38;
  doi:10.1016/j.artint.2018.07.007): human explanation is
  selective and tailored to the listener, not exhaustive. An agent
  that dumps everything it knows is transcribing, not explaining.
* **The right level depends on expertise** — Kalyuga (2007),
  *Expertise Reversal Effect and Its Implications for
  Learner-Tailored Instruction* (Educational Psychology Review
  19:509–539): instructional support that helps a novice actively
  *harms* an expert (redundant detail becomes cognitive-load
  cost). There is no one-size explanation.
* **Comprehension is built and verified, not assumed** — Clark &
  Brennan (1991), *Grounding in communication* (in *Perspectives
  on Socially Shared Cognition*, 127–149): mutual understanding is
  grounded turn by turn; the agent owns the grounding — it checks
  the human is still with it, rather than reading silence after a
  wall of jargon as assent.
* **When this fails, the human over-relies** — the
  appropriate-reliance literature (e.g. arXiv:2301.11333;
  arXiv:2305.07722): fluent explanations can *increase*
  over-reliance and manufacture an *illusion of understanding*;
  genuine complementary performance needs **verifiability**, not a
  plausible-sounding story.
* **The understanding is the artifact, and it does not persist by
  itself** — Naur (1985), *Programming as Theory Building*
  (Microprocessing and Microprogramming 15(5):253–261;
  doi:10.1016/0165-6074(85)90032-8): a program's essential content
  is a *theory* held by the people who built it, and that theory
  is not contained in the program text or its documentation. When
  the holders disperse, the theory is lost and the artifact
  becomes unmodifiable in any principled way. Naur's conclusion is
  bleak by design; Cairn's answer is not to pretend the theory can
  be written down whole, but to require that the artifact carry
  **the reasons a reader needs to rebuild it** — which is the
  temporal half below.

Cairn's contribution is to make the comprehension floor a
**reviewable property of the lifecycle** — the same move that
turned review into a recorded, checkable step.
"Did the human actually understand what they decided?" is a
first-class question, not an afterthought.

The operative norm: lead plain, keep precision beneath, and treat
*"I don't understand this yet"* as a **mandatory pause** — a
decision surface the Maintainer cannot follow is not decidable.

**The floor has a temporal half.** Everything above is about the
reader in the room — the Maintainer deciding now, with the
proposal open and the reviewer reachable. But a durable artifact
outlives that room. **The reader who must understand it is
whoever meets it next**, and that reader has no deliberation to
consult: the proposal is archived, the review is a section in a
file nobody opens, and the agent that wrote the code is a session
that ended. The record is a *by-product* of deciding, not a
channel to the future — so **an artifact whose meaning depends on
the record decays at exactly the rate the record archives.**

The obligation this creates is narrow and concrete: **a durable
artifact must stand without the deliberation that produced it.**
A test name says what property it pins, not which plan chunk
produced it. A comment says why the code is the way it is, not
which review finding asked for it. A coordinate — `F5`,
`CR1`, `TestP2AmendmentBScopeReduction` — is a pointer into a
conversation that has ended; to the next reader it is a token
that *looks* like information and carries none. It is worse than
silence, because silence prompts a question and a dead coordinate
answers it wrongly.

**This is not licence to narrate, and Anchor 17 is the fence.**
Writing the reason in means writing the reason the code does not
already state — not restating the code in prose, not transcribing
the deliberation into the artifact, not a comment on every line.
Naur's point cuts both ways: the theory cannot be written down
whole, so an attempt to write it all down produces volume without
transmission, and volume is waste in Anchor 17's exact sense.
The test is not *"is the reasoning recorded somewhere"* but
**"can the next reader act on this without the record?"** — which
usually takes one sentence, and sometimes takes none.

This anchor is scoped to that **universal norm**. The further
dimension — calibrating communication by the recipient's domain
and software proximity — is observed in the guide-star but is not
yet harvested here; it remains in the reference instance.

---

## Cluster III — Scientific-software rigor and validation

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

**6. Scientific peer review as a process model.** Cairn's review
system's closest real-world analog is not multi-agent debate but
**scientific peer review** itself — the author / editor / reviewer
division of labor codified by editorial-standards bodies (ICMJE;
the Council of Science Editors), and the open-peer-review taxonomy
of Ross-Hellauer (2017), *What is open peer review?*
(*F1000Research* 6:588). This is the anchor Cairn instantiates
most directly (`dual-review.md`).

---

## Cluster IV — Community, sustainability, and restraint

Anchors 7–10 remain Cairn's community-maintained-software and
trustworthy-operation horizon. Anchor 17 supplies the present-tense design
discipline that keeps the methodology sustainable enough to use.

**17. Waste and proportional process.** Poppendieck & Poppendieck
(2003), *Lean Software Development: An Agile Toolkit*, Addison-Wesley,
names extra processes and extra features as waste when they do not produce
value for the user. Boehm & Turner (2003), *Balancing Agility and
Discipline: A Guide for the Perplexed*, Addison-Wesley, makes the amount of
process a judgment across personnel, criticality, size, culture, and
dynamism: too much ceremony and too little are both failure modes. Saltzer
& Schroeder (1975), *The Protection of Information in Computer Systems*,
*Proceedings of the IEEE* 63(9):1278–1308, supplies the security-side
companion through **economy of mechanism**: protection mechanisms should
remain as simple and small as possible so unwanted access paths stay
visible.

Cairn therefore treats **restraint as a design center beside trust**. The
method's default path should be proportionate to demonstrated blast
radius, while deeper ceremony is earned by criticality, uncertainty,
cross-cutting reach, or a real trust boundary. This is not permission to
skip a declared review tier, a Maintainer fence, or a security control.
Criticality measures the consequence of being wrong, not the number of
users: fail-closed defaults and measured trust roots can remain necessary
even in a one-person project. The restraint test applies to the
*deliberation around* those controls as much as to any other work.

The operational warning is simple: if the apparatus repeatedly costs more
than the change it governs, obscures the work the Maintainer must judge, or
makes bypass attractive, it is no longer buying rigor. Simplify the
mechanism or route low-risk work through the lighter path while preserving
the load-bearing property.

---

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

* **The Dual-Review model.** One review stance at every stage: a fresh
  reviewer, who did not write the work, on the work's side, who makes
  it better by questioning its foundations and answers in writing —
  should it exist as framed, what is the best alternative, what would
  show it wrong — executed asynchronously and commit-mediated
  (`dual-review.md`). It is a specialized variant of multi-agent debate
  (anchor 5) and a faithful instantiation of scientific peer review
  (anchor 6). Its sharpest point: independence is *recorded, not
  claimed* — every review names its reviewer, so how far that reviewer
  stood from the author is visible, and a different model architecture
  or a person is available whenever the Maintainer asks for more
  distance.

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

The substrate is shipped by the default-on
[`incident-trackers`](../templates/modules/default-on/incident-trackers.md)
module, which installs a forkable tracker template + the goodnight
migration sub-step. Adopters fork the template to taste — one
tracker, two trackers, or several class-specific trackers — and
the rate-limit gate evaluates against whichever instance(s) the
deployment maintains. The gate counts `Impact = occurred` rows
within the rolling-window boundary the adopter pinned in the
tracker's "What counts" sub-section.

### The reference-instance doctrine harvest

The rate-limit gate governs the loop *within* an adopter: incident →
recorded signal → doctrine change. A second loop runs the other
direction, at framework scale. Cairn is "the generalized doctrine
extracted from" a reference instance — but an extraction is a
*snapshot*: the reference instance keeps accreting operating doctrine
incident-by-incident, and core silently falls behind. The R-F fidelity
gate cannot see this — it audits faithfulness to the manifest, so it
certifies a faithful install of a *thin* core and is structurally
blind to core *incompleteness*. The **doctrine harvest** is the
standing process that closes that gap.

* **A harvest run.** A periodic sweep that diffs a mature reference
  instance's operating-doctrine prose — its `AGENTS.md` and
  `agent_collaboration.md`, where incident-driven rules accrete —
  against Cairn core, recording each *generalizable* gap as a
  fold-back. The generalizable-vs-local test: a gap qualifies if a
  differently-shaped team would hit the same failure; adopter-local
  quirks (a project's own tools, naming, science) do not. The
  first-adopter comparison that produced this very batch of fold-backs
  was the harvest's first run, by hand.
* **Which instance.** Target whichever adopter has **out-accreted**
  core since the last harvest — the one carrying mature doctrine core
  lacks. Name it in the run's record.
* **Convergence — an empty sweep is success.** A harvest pays only
  when an instance is ahead of core. Right after one lands, core ≈ that
  instance's current doctrine, so the next sweep may legitimately find
  **nothing** — the loop *converging*, not failing. Never manufacture
  marginal gaps to justify the run. This is the ward against the
  harvest becoming ceremony.
* **Where the run is recorded.** Each harvest — findings *and* empty
  sweeps — is logged where the harvesting party already tracks fold-backs:
  the adopter's `dev/.cairn/<framework>_foldback.md` ledger today (a one-line
  "harvest <date> vs `<instance>`: N items / core current" entry), or a
  Cairn-side log once Cairn runs its own `dev/`. An empty sweep recorded
  as "core current as of `<date>` against `<instance>`" is the visible
  proof the cadence ran and converged — not a missing run.
* **Cadence.** Run a harvest (a) before each Cairn minor release (the
  floor), and (b) on an adopter signal. The signal is a **counted**
  trigger, not a vibe: a harvest fires when the reference instance has
  landed *k* operating-doctrine additions to its `AGENTS.md` /
  `agent_collaboration.md` since the last harvest (commits touching
  those files are a cheap proxy). Like the rate-limit gate's
  recurrence window above, *k* is the harvesting party's choice,
  **recorded with the cadence** — the doctrine fixes that a count
  governs, not the specific number.
* **Where findings go.** Until Cairn runs its own `dev/`, a finding
  is filed as an upstream fold-back issue on Cairn's own tracker
  (`.github/ISSUE_TEMPLATE/foldback.md`) → proposal → lands in cairn
  (the adopter-lifecycle these very items rode); once Cairn adopts its
  own `dev/`, findings become Cairn's own proposals. Either way the
  finding is *deliberated*, not applied raw — the harvest feeds the
  lifecycle, it does not bypass it. The local ledger this once routed
  through — the deployment-side artifact, its lifecycle and status
  vocabulary, the nightly capture, and the scrub-before-export rule —
  is retired; filing now goes straight upstream. The harvest remains
  the framework-side *pull*, filing the deployment-side *push*, and
  both record here.

A companion **core-completeness probe** — the adopter-side check that an
install merged all its module content and captured its tacit rules in
`AGENTS.md` — lives in `../bootstrap/fidelity-check.md`. The harvest
keeps *core* from lagging its best adopter; the probe keeps an
*install* from silently shipping incomplete. Both are distinct from the
R-F fidelity gate, which proves only *faithful install*.

## Where the rationale is still thin

Honesty is part of the method. Two areas the anchors expose as
under-built — carried as named open problems, not hidden:

* **Measurement.** Anchor 3 asks for *measurable* trust. Cairn does
  not currently ship any metrics tooling for proposal/plan cycle time
  or throughput — the layer that once did was removed, with no
  replacement built — so measurable trust for this anchor is not yet
  mechanized. The longitudinal evidence remains future work.
* **Scientific-correctness interlock.** Anchor 4's failure mode —
  a wrong result that looks right — is only partly addressed by
  structural review. The V&V canon (Oberkampf & Roy 2010,
  *Verification and Validation in Scientific Computing*; Sandve
  et al. 2013, *Ten Simple Rules for Reproducible Computational
  Research*) provides the citation frame for what a deeper interlock
  would look like, but catching *scientific*, as opposed to
  *structural*, error without the Maintainer in the loop is an
  open problem Cairn names but does not yet solve.
