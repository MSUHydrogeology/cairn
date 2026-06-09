<!-- cairn-internal-ref-allow: doctrine/lifecycle.md doctrine/proposals.md doctrine/plans.md doctrine/dual-review.md doctrine/session-routines.md doctrine/roles.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# The lifecycle contract

This document is the **executable formalization** of the lifecycle —
the legal states, the legal transitions between them, the **authority**
each transition requires, and the **per-type precondition** each
transition must satisfy. It does not restate *why* the lifecycle is
shaped as it is; that reasoning lives in
[`lifecycle.md`](lifecycle.md), and the per-artifact prose contracts
live in [`proposals.md`](proposals.md) and [`plans.md`](plans.md). This
contract **references** those homes and renders their rules in a single
machine-checkable form, so a tool can report an artifact's state and the
preconditions a transition has not yet met — **without** re-litigating
or fragmenting the doctrine.

It is the foundation two things read against: the **read-only
checker/planner** (`templates/skills/_lib/lifecycle_planner.py`), which
reports state + legal transitions + unmet preconditions and emits a
*proposed* scaffold for a chosen transition; and the **conformance
test** (`bootstrap/tests/test_lifecycle_contract.py`), which guards this
contract's executable form Cairn-side.

## The authority contract — the safety boundary

A tool may **mechanize the assembly, the gates, and the formatting**; it
must **never mechanize the judgment**. This boundary is what lets
mechanization *serve* the deliberation instead of eroding it, and it is
stated here as a contract, not an aspiration:

1. **Structural attestation, not authenticity.** A tool **attests the
   structure and presence** of an authority-bearing artifact — a
   blockquote is present, visually isolated, and matches the commit
   message — and reports a *missing or malformed* one. It **never
   certifies authenticity**: a local tool has no access to the harness's
   chat or system logs, so it cannot know whether a quoted authorization
   was truly given. The **committing harness/operator remains the sole
   guarantor** that the quote is real. The tool reports a missing
   attestation; it never asserts a valid one.
2. **Infer, validate, quote — never invent.** A tool may **infer**
   structural state from committed artifacts, **validate** attestations
   those artifacts carry, and **quote** authority-bearing inputs. It may
   **not invent** them: it never authors a disposition, a finding, or an
   authorization.
3. **A status flips only on a machine-verifiable precondition.** When the
   documentary precondition for a transition is absent, the tool reports
   the **missing attestation** rather than guessing the transition is
   legal.
4. **The visible pause is preserved.** Mechanization prepares and quotes;
   an agent or the Maintainer owns the transition. The tool's output is a
   *proposal* — a scaffold and a manifest of what would change — not a
   mutation and not a commit.

The read-only checker/planner honors this contract by construction: it
**reports and proposes; it does not write the corpus and does not
commit.** Any future mutating arm is a separate, separately-reviewed
privilege (see [`lifecycle.md`](lifecycle.md) and the proposal that
defers it); this contract governs what such an arm would have to honor,
but the read-only program neither needs nor claims that privilege.

## Identity: AI reviewer vs. human authority

Several preconditions turn on *who* authored a section — a review is
authored by a reviewer (an AI agent or a human), but a **Decision** is a
**Human Maintainer** authority. The contract distinguishes them by an
**extensible, vendor-neutral identity model**, never a closed enum:

* The author token is parsed generically from the section header
  (`## Review -- <name> (<role>) -- <date>`), preserving the real
  identity (`Codex`, `Claude`, `Antigravity`, `Gemini`, a future agent).
* An **allowlist/registry of AI agent identities** classifies a token as
  an AI agent; the **human Maintainer is the residual** (a token not on
  the AI registry, matching the project's Maintainer identity). New
  vendors join the registry by configuration, never a code edit — the
  same open posture as the model-tier list in `lifecycle_metrics`.

This forecloses the failure mode where a non-Codex/non-Claude agent
(e.g. Antigravity) is misread as the human Maintainer, which would
corrupt both authorship checks and the human/AI split the Decision
authority depends on.

## The proposal state machine

```
proposed --> reviewed --> revised --> accepted
                                  --> rejected
                                  --> superseded
```

| Transition | Authority | Machine-verifiable preconditions |
|---|---|---|
| → **proposed** | author | the file exists under `dev/proposals/`; carries the house front-matter (`Author`, `Date opened`, `Status: proposed`) and the opening sections (context, the change, alternatives, evidence/verification plan, signals-it-is-wrong); a mandatory `Plan review:` line is present. |
| proposed → **reviewed** | a reviewer (AI or human), **not the author** | a `## Review -- <reviewer> ... ` section is appended; its author token is **not** the proposal's author (reviewer-authorship); prior sections are unmodified (append-only). |
| reviewed → **revised** | author | a `## Response` (and, where needed, a revised section) is appended; prior sections unmodified. Review and revision may repeat (`revised → reviewed → revised`). |
| → **accepted** | **Human Maintainer** | a `## Decision -- <Maintainer> ... ` section is appended that (a) is authored by the human Maintainer identity, (b) **quotes an authorization verbatim** in an isolated blockquote, (c) is **Decision-only** — the commit touches nothing but this section, and (d) does **not** archive the file (an accepted proposal stays in `dev/proposals/`). |
| → **rejected** / **superseded** | **Human Maintainer** | as **accepted**, except the Decision commit **also** archives the file (moves it to `archive/`). |

**Per-type rules made explicit** (the checker validates structure +
presence; the operator guarantees authenticity):

* **Decision is Decision-only and quotes verbatim.** The tool attests
  that a Decision section carries an isolated authorization blockquote
  and that the staged change is the Decision section alone. It never
  authors the disposition or the quote.
* **A review carries reviewer-authorship.** A generated review scaffold
  carries **no reviewer attribution** — the reviewer fills their own
  identity; the tool never attributes a review to an agent that did not
  write it.
* **Append-only.** Every transition after `proposed` is an *appended*
  section; modifying a prior section is a violation (the one bounded
  exception — mechanical claim-marker maintenance — is defined in
  [`lifecycle.md`](lifecycle.md) and is not a lifecycle transition).

## The plan state machine

```
open --> [awaiting-plan-review] --> executing --> review --> archived
```

| Transition | Authority | Machine-verifiable preconditions |
|---|---|---|
| → **open** | author | the plan-open commit creates the plan **and** archives the source proposal (the source proposal moves to `archive/` in this commit); the plan carries the mandatory `Plan review:` line. |
| open → **awaiting-plan-review** | (state) | only when `Plan review: required(<tier>)`; the plan waits for its plan-review section. A `not required(<rationale>)` plan **skips** this state. |
| → **executing** | author | for a review-required plan, a plan-review section has landed and the plan-open and first-implementation commits are **distinct**; for a `not required` plan, execution may combine with plan-open (fast multi-stage). |
| executing → **review** | a reviewer | a code-review pass section is appended (append-only). |
| review → **archived** | author | **the plan-archive precondition holds: a code review has occurred** (the archive commit is distinct from the implementing commits); **and** every explicitly-deferred follow-up has a durable home recorded in an auditable `Follow-ups migrated to: …` block; the loop-fidelity sign-off names the implementing commit and the governing Revised section. |

A plan is an execution artifact: `Status:`, progress markers, and commit
hashes update **in place**. But review-finding and archive sections are
**append-only**, mirroring the proposal contract.

## What is machine-verifiable vs. human-owned

The boundary the checker must respect, restated operationally:

* **Machine-verifiable (the tool reports / scaffolds):** the current
  `Status:`, the set of legal next transitions from it, the *structural*
  presence/absence of each transition's documentary precondition (a
  Review section exists; a Decision carries an isolated blockquote; the
  plan-archive review section is present; an accepted proposal has not
  been edited in place), and a *proposed* house-format scaffold for a
  chosen transition.
* **Human-owned (the tool never produces):** the disposition itself, the
  content of any review finding, and — above all — the **verbatim
  authorization** a Decision quotes. The tool reports that an attestation
  is *missing or malformed*; it never asserts one is *valid*, and it
  never authors one.

When a precondition is structurally absent the tool reports the **missing
attestation** and declines to present the transition as ready — it never
guesses a transition legal to be helpful.

## Adaptation

This contract is the executable face of the lifecycle, which is part of
Cairn's **invariant kernel** ([`lifecycle.md`](lifecycle.md) >
"Adaptation"). What scales with the team is the *review tier* applied
within it (see [`dual-review.md`](dual-review.md)), not the state machine.
The read-only checker that reads against this contract is an **optional
aid, outside the minimum mechanized kernel**: a team without a Python
runtime runs the lifecycle **manually** against this document, with no
loss of the contract itself — only of the mechanized convenience.
