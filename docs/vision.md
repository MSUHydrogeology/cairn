# Cairn — vision and charter

> Cairn's **purpose, design centers, and anti-scope** — the project's
> foundational identity. The `README.md` is the front door;
> `doctrine/rationale.md` is the research grounding; this is the charter
> that states *what Cairn is for, and what it refuses to become*. It is
> distilled from the fuller guide-star deliberation record under
> `dev/strategy/`.

## Purpose

Cairn is an **Open Science methodology repository** — explanatory doctrine
plus reusable, forkable templates — for **scientists building their own
scientific-computing software** who want a disciplined human + AI
development methodology.

Its structure was **not designed top-down.** It was extracted and
generalized from a working team — one human Maintainer and AI
collaborators of more than one type — where each piece was added in answer
to a concrete failure mode: silent agent drift, deliberation arcs lost when
a chat closed, cross-agent review masking a shared blind spot. Every
mechanism is tied to the failure it answers; the grounding is in
`doctrine/rationale.md`.

Cairn is **repo-first.** A forkable, DOI-bearing repository gets *adopted*
where a paper gets *cited*; a preprint is optional later amplification, not
the primary artifact.

## What makes it Cairn

Two differentiators, both genuinely uncommon, define the method:

* **An append-only, git-committed deliberation lifecycle** — every
  substantive change moves through a recorded proposal (and, for
  non-trivial work, a plan); the full arc of a decision is reconstructible
  from `git log`, not lost when a session ends (`doctrine/lifecycle.md`).
* **The Dual-Review model** — one review at every stage: a fresh reviewer
  who did not write the work questions its foundations and answers in
  writing, and a different model or a person adds more distance whenever
  the Maintainer asks. Asynchronous, commit-mediated, attributed — a faithful
  instantiation of scientific peer review (`doctrine/dual-review.md`).

Around these, Cairn ships the apparatus a forkable, *living* standard needs
and a static prose framework does not: a layered security model; an upgrade
capability (a deployment folds in new Cairn doctrine while keeping its local
customizations); the fold-back channel (deployments improve Cairn
upstream); and an executable coordination primitive.

**The honest value curve.** Cairn *adds friction before code* and pays it
back later — in less rework, fewer forgotten decisions, fewer agent
collisions, fewer unreviewed scientific changes. This is an evidence-based
bet, not an aspiration: raw AI speed is partly illusory (experienced
developers on mature repositories have *measured* slower with AI tooling
while believing they were faster), and the expensive errors are the late
ones (catch it in review, not in production). The promise that follows:
**keep the apparatus only as heavy as your codebase and team earn** — which
is what lets a lone scientist with one agent start at the kernel and deepen
only as the project earns it.

## Trust is the design center

Adopting Cairn is an unusual ask: not just "use this tool" but **commit
this load-bearing apparatus to your git history, give AI agents read/write
authority on the repository that holds your science, and let the apparatus
shape how your team deliberates.** The adoption decision is therefore a
**trust decision** — larger than adopting a library, smaller than joining a
movement. Cairn earns or loses that trust by structural choices, not by
marketing. Five dimensions, each mapped to a concrete commitment:

* **Transparency** — every decision lives in a public, append-only
  deliberation record; every load-bearing claim cites its source (the
  verify-before-asserting discipline); the anti-scope is explicit.
* **Responsibility** — Cairn does not ship doctrine it has not exercised:
  two dogfooded case studies carry the apparatus through real work, a
  pre-release sweep gates every cut, and fail-closed integrity checks catch
  the failure modes the doctrine warns about.
* **User focus** — the two-ways-in on-ramp, the adopter-friction work, and
  progressive onboarding let the adopter choose their depth; multi-user is
  the design center, with the Maintainer one user among many.
* **Sustainability** — dual CC BY 4.0 + MIT licensing, no vendor lock-in,
  no telemetry by default. Adoption is reversible; nothing about adopting
  Cairn commits a team to anything it cannot exit.
* **Technology** — no network by default, an export-safety scrub, content
  scanning, and an explicit trust-boundary doctrine (a project's own runs
  are trusted; colleague-supplied artifacts are user-controlled). The
  infrastructure does not silently exfiltrate.

The fuller treatment — and where Cairn deliberately *diverges* from the
literature it draws on — is `doctrine/rationale.md`; the contract for what
the agent reads and the scanners check is `SECURITY.md`.

## Restraint is the other design center

Cairn fails if its trust machinery becomes expensive enough that people work
around it. Process must therefore track the consequence and reach of the
change, not how interesting the question is. Low-risk, local work should take
the light path; critical, cross-cutting, uncertain, or trust-boundary work
earns deeper ceremony.

This is not a license to skip a declared review, a Maintainer fence, or a
security control. A one-person scientific project can still carry a
high-criticality surface, and controls such as fail-closed defaults and measured
trust roots are often cheapest to establish before assumptions spread. The
discipline is to keep those protections small and legible, and to prevent the
deliberation around them from growing without regard to blast radius.

The practical test is whether the apparatus continues to help the Maintainer
understand and judge the work. When ceremony repeatedly outweighs the change,
obscures it, or makes bypass attractive, the mechanism needs simplification or
the work needs the lighter route. The research grounding is Anchor 17 in
`doctrine/rationale.md`.

## Anti-scope — what Cairn refuses to become

A charter is as much about boundaries as aspirations. Cairn is **not** a
project-management framework, a CI/CD tool, or a prompt library — it is
*upstream* of those: the doctrine that decides what gets prompted,
reviewed, and shipped. It does not claim to be peer-reviewed science; it
claims to be *grounded in* peer-reviewed work on human-AI software
development and *explicit about where it diverges*.

And this charter is **the agenda, not the authorization.** Stating a
direction here does not by itself authorize it. In particular, nothing here
authorizes — absent its own proposal, review, and Maintainer Decision:

* adding a new `dimensions/` axis, or changing the role roster, the
  lifecycle, or the review stance;
* building a self-instrumenting maturity layer;
* any public-surface action (flipping the repository public, tagging a
  public release) — those are Maintainer-performed.

Cairn's current structure is organically derived and load-bearing; horizons
*extend* it, they do not replace it. Concrete moves go through the normal
proposal cycle.

## Where the rest lives

This charter is deliberately compact. The fuller record:

* **Rationale + research grounding** (the framework anchors,
  follows-and-diverges) — `doctrine/rationale.md`, `docs/further-reading.md`.
* **Front door** (what it is, how to adopt) — the repository `README.md`.
* **Direction** (the live roadmap + release path) — `dev/PLANNING.md`.
* **The guide-star deliberation record** this was distilled from — under
  `dev/strategy/`.
