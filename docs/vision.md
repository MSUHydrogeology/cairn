# Cairn — vision and charter

> Cairn's **purpose, design centers, and anti-scope** — what the project is
> for and what it refuses to become. The `README.md` is the front door;
> `doctrine/rationale.md` is the research grounding. This page is distilled
> from longer strategy notes under `dev/strategy/`.

## Purpose

Cairn is an **Open Science methodology repository** — explanatory doctrine
plus reusable, forkable templates — for **scientists building their own
scientific-computing software** who want a disciplined human + AI
development methodology.

Its structure was **not designed top-down.** It grew out of one working
team: a human Maintainer and AI collaborators of more than one type. Each
piece was added in answer to a concrete failure: agents drifting silently,
reasoning lost when a chat closed, and reviews that shared the author's blind
spot. Every mechanism is tied to the failure it answers; the grounding is in
`doctrine/rationale.md`. That history is where the method came from. Today it
needs only a human and one AI tool.

Cairn is **repo-first.** A forkable, DOI-bearing repository gets *adopted*
where a paper gets *cited*; a preprint is optional later amplification, not
the primary artifact.

## What makes it Cairn

Two differentiators, both genuinely uncommon, define the method:

* **An append-only, git-committed deliberation lifecycle.** Changes are
  sorted into three lanes before anything is written. A typo or one-line fix
  gets a test and a code review. A change with a settled shape gets a short
  change note and a review. A new feature, a contract change or a high-risk
  surface gets a recorded proposal, the Maintainer's decision and a plan. The
  arc of a decision can be rebuilt from `git log`, not lost when a session
  ends (`doctrine/lifecycle.md`).
* **The Dual-Review model** — one review at every stage: a fresh reviewer
  who did not write the work questions its foundations and answers in
  writing, and a different model or a person adds more distance whenever
  the Maintainer asks. Asynchronous, commit-mediated, attributed — a faithful
  instantiation of scientific peer review (`doctrine/dual-review.md`).

Around these, Cairn ships what a living standard needs and a static document
does not: security checks; an updater that brings in new Cairn guidance while
keeping your local edits; a way to suggest improvements back to Cairn through
its issue tracker; and a tool that stops two agents editing the same files at
once.

**The honest value curve.** Cairn *adds friction before code* and hopes to
pay it back later, in less rework, fewer forgotten decisions, fewer agent
collisions and fewer unreviewed scientific changes. It is a bet backed by
research, not a proven result. The speed-up from AI is easy to overestimate:
in a 2025 trial, experienced developers believed AI tools made them faster
while being measured slower, and later studies find the real gain depends on
the task. Either way, the cost moves to checking the work, and the expensive
errors are the late ones, so catch them in review, not in production. The promise that follows: **keep
the method only as heavy as your codebase and team need.** A lone scientist
with one agent can start with the smallest set of rules and add more only as
the project earns it.

## Trust is the design center

Adopting Cairn asks more than "use this tool." You commit its files to your
git history, give AI agents read and write access to the repository that holds
your science, and let the method shape how your team makes decisions. That is
a **trust decision**, larger than adopting a library. Cairn tries to earn that
trust through how it is built. Five areas, each with a concrete commitment:

* **Transparency** — every decision lives in a public, append-only
  deliberation record; every load-bearing claim cites its source (the
  verify-before-asserting discipline); the anti-scope is explicit.
* **Responsibility** — Cairn does not ship guidance it has not used. Two case
  studies carry the method through real work, though both are by the same
  maintainer and are not independent adoptions. A pre-release sweep gates every
  release, and integrity checks refuse to pass when something is wrong.
* **User focus** — two ways in (read the guidance, or install it) and
  progressive onboarding let you choose how deep to go.
* **Sustainability** — code under the MIT license; prose, templates and
  diagrams under CC BY 4.0; the brand mark alone under CC BY-ND 4.0. No vendor
  lock-in: the record is plain files in git.
* **Technology** — the installer makes no network requests
  (`bootstrap/SAFETY.md`), and Cairn ships an export-safety scrub, content
  scanning, and an explicit trust boundary: a project's own runs are trusted;
  artifacts supplied by colleagues are not. Some installed modules do use the
  network when you run them; `bootstrap/SAFETY.md` says which.

The fuller treatment — and where Cairn deliberately *diverges* from the
literature it draws on — is `doctrine/rationale.md`; the contract for what
the agent reads and the scanners check is `SECURITY.md`.

## Restraint is the other design center

Cairn fails if its checks become so costly that people work around them. The
amount of process should follow the consequence and reach of the change, not
how interesting the question is. Low-risk, local work takes the light lane.
Critical, cross-cutting, uncertain or trust-boundary work earns more.

This is not permission to skip a declared review, a step reserved for the
Maintainer, or a security control. A one-person scientific project can still
carry a high-risk surface, and safeguards that refuse to pass when something
is wrong are cheapest to set up early. Keep those safeguards small and
readable, and stop the discussion around them from growing out of proportion
to the risk.

The practical test is whether the method still helps the Maintainer
understand and judge the work. When the ceremony repeatedly outweighs the
change, hides it, or makes bypass attractive, simplify the mechanism or move
the work to a lighter lane. The research grounding is Anchor 17 in
`doctrine/rationale.md`.

## Anti-scope — what Cairn refuses to become

A charter is as much about boundaries as aspirations. Cairn is **not** a
project-management framework, a CI/CD tool, or a prompt library — it is
*upstream* of those: the guidance for how changes are argued, reviewed,
and recorded before they ship. It does not claim to be peer-reviewed science; it
claims to be *grounded in* peer-reviewed work on human-AI software
development and *explicit about where it diverges*.

And this charter is **the agenda, not the authorization.** Stating a
direction here does not by itself authorize it. In particular, nothing here
authorizes — absent its own proposal, review, and Maintainer Decision:

* adding a new `dimensions/` axis, or changing the role roster, the
  lifecycle, or the review stance;
* any public-surface action (pushing, tagging a release, changing the
  repository's settings) — those are Maintainer-performed.

Cairn's current structure is organically derived and load-bearing; horizons
*extend* it, they do not replace it. Concrete moves go through the normal
proposal cycle.

## Where the rest lives

This charter is deliberately compact. The fuller record:

* **Rationale + research grounding** (the framework anchors,
  follows-and-diverges) — `doctrine/rationale.md`, `docs/further-reading.md`.
* **Front door** (what it is, how to adopt) — the repository `README.md`.
* **Direction** (the live roadmap + release path) — `dev/PLANNING.md`.
* **The strategy notes** this page was distilled from — under
  `dev/strategy/`.
