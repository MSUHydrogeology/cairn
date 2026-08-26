<!-- The plan template. Copy everything below the rule into
     `dev/plans/<slug>.md`. Keep it short: a plan is a working
     document, not a second proposal. -->

# Plan template

A non-trivial accepted proposal opens a plan. The plan says how the work
happens and how you will know it worked; it does not re-argue the decision.

## Lifecycle

```
awaiting-plan-review <-> revising-plan -> ready-to-implement
  -> implementing -> awaiting-code-review <-> revising-code
  -> ready-to-archive -> archived
```

Each status names **who holds it next**. Opening a plan archives its source
proposal in the same commit.

**Reviews, responses and decisions append and are never edited. Operative
cells — Scope, Sequence, Acceptance criteria, Verification — revise in place
until implementation begins.**

**A plan answers plan review in its cells, not in a contract revision.** This
is the one place the plan's rule is the *opposite* of the proposal's, so it is
stated rather than left to be inferred: a proposal Response appends a complete
current contract carrying a withdrawal ledger; a plan does not. Before
implementation, fold plan-review corrections straight into the mutable
operative cells and let the appended `## Response to plan review` be a
disposition table that *points at* them — a second copy of a cell is
immediately a second answer to the same question.
Once execution of a chunk begins, changes append instead.

**A plan review is Internal, fresh-context.** Code review's floor is separate
and independent: not the implementing agent.

**Deviating from an accepted plan takes the Maintainer's word** — new scope, a
contract review never saw, an acceptance criterion you cannot meet, **or
accepted scope removed**. Removal counts in both directions: accepted scope is
a floor, and a reviewer cannot create authority to narrow by calling the
remainder out of scope.

## Forward-reference paths

A path that does not exist yet trips `claim_check`. Declare it instead — the
literal `Proposed paths:` line, no blank line before the first bullet, one
physical line per bullet. Drop a line once its path resolves.

---

# Plan: {{short title}}

**Source proposal**: {{dev/proposals/archive/...}}
**Status**: awaiting-plan-review
**Plan review**: {{required(Internal) | required(Internal + Internal Security Review)}}
**Opened**: {{YYYY-MM-DD}}

## Source proposal

One paragraph: what the proposal decided. The plan executes it.

## Scope

What this plan does and, where it is not obvious, what it deliberately does
not. Name the surfaces it touches.

### Documentation / doctrine surface

<!-- cairn:slot documentation-tier-home -->
(Filled from the `documentation-plan` default-on module when installed
— paste content from `dev/modules/documentation-plan.md` > "Merged
into" > Block 3: dev/plans/_template.md. The merged content names
the per-layer routing rule for doc + doctrine changes, pointing at
`docs/DOCUMENTATION_PLAN.md`. If documentation-plan is not installed,
replace with `N/A: documentation-plan not installed`. An unfilled
slot is a review finding.)
<!-- cairn:end documentation-tier-home -->

## Sequence

One row per chunk: what it does, what gates it, roughly what it ships. Mark a
chunk MAINTAINER-GATED or MAINTAINER-ONLY where approval is actually
load-bearing — that fence, not a blanket per-commit gate, is where approval
binds to something specific.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | | | |

## Acceptance criteria

Per chunk, each falsifiable. A criterion you cannot imagine failing is not one.

  <!-- cairn:slot acceptance-doc-tooling -->
  (Adopter-specific doc-generation tooling — the exact schema source +
  render command, the snippet-sync command, the CLI / notebook smoke
  surfaces the project uses. Fill with the project's commands, or
  replace with `N/A: no generated or snippet-synced docs`.)
  <!-- cairn:end acceptance-doc-tooling -->

## Scope delta

**Accepted scope is a floor.** The baseline is the scope as accepted by the
proposal, and dropping an outcome it committed to is a deviation exactly as
adding one is. Sequencing is free — moving work between chunks owes nothing —
but delivering less does not.

**A reviewer cannot create that authority by calling the remainder "out of
scope."** Narrowing is the path of least resistance in review: it costs the
reviewer nothing, reads as prudence, and can never be shown wrong, because the
wider version is never built. Neither author nor reviewer may concede a
baseline outcome; only the Maintainer can.

If scope is reduced, declare it here — one grouped record, not a set of roadmap
rows, and each entry blocks archive until dispositioned:

**Scope delta**: preserved | degraded | lost

One line per removed unit, each carrying its own
`**disposition**: <accept | guard | wontfix | defer>` — a group-level home is a
location, not a decision. Say what was dropped, why specifying was rejected in
favour of cutting, and quote the Maintainer's allowance. Declining a proposed *expansion* is not a
reduction — it was never in the baseline. A chunk's own fence bounds this pass,
not the accepted proposal.

## Verification

**Boundary A (iteration, scoped).** The tests owning each touched surface,
plus its standing gates.

<!-- cairn:slot verification-commands -->
Before implementation, make Boundary A a **reviewed mapping**: for each changed
invariant and public path, name the exact affected test node/file and every
standing non-test gate for the touched surface. Run that scope while iterating.
There is no permanent fast tier; if a substantive code surface has no reviewed
mapping or cannot be bounded confidently, run the configured full suite.

After the final implementation commit, Boundary B runs once against a clean,
unchanged commit under the project's canonical interpreter/runtime. The default
is the **configured full suite** plus standing integration gates; a plan whose
reviewed mapping **bounds the change's effects confidently** may instead run
that mapping plus every standing gate for every touched surface. Bounded mode
**refuses** — run full — when the change touches a **contract surface** (the
project's install contract, manifests, or lockfile schema) or a
**trust-ceremony surface** (any high-risk surface the governing file names, or
release/security ceremony work). **Uncertainty resolves to `full`.** List those
concrete commands here, including test outcomes and every plan-specific
acceptance command.

Only after that stable run, append a dated section named
`Implementation verification -- <agent> -- YYYY-MM-DD` at H2. Do not place an
empty heading in a new plan. The record uses these exact fields:

* **Boundary B mode** — `full` | `bounded`. On `bounded`, also name the touched
  surfaces, the reviewed mapping and standing gates run, why the effects are
  bounded, and the explicit absence of any contract or trust-ceremony surface.
* **Tested commit** — full revision ID.
* **Reviewed range** — base and tested endpoint.
* **Interpreter/runtime** — canonical path and version.
* **Pre-run state** and **Post-run state** — clean tree and identical tested
  revision.
* A command table with **Command**, **Exit**, **Outcomes**, and **Elapsed**
  columns, including pass/fail/skip/xfail/xpass counts where applicable.
* **Non-pass disposition**, **Plan-specific acceptance commands**, and
  **Known omissions**.

Also name the project's documentation, schema, snippet, security, and smoke
gates here. If none applies, record `N/A` with a reason rather than omitting the
surface silently.
<!-- cairn:end verification-commands -->

**Boundary B (integration).** After the final implementation commit, against a
clean unchanged commit under the canonical interpreter. Record
`**Boundary B mode**: full | bounded`. **Uncertainty resolves to `full`**, and
`full` is mandatory for any contract or trust-ceremony surface. On `bounded`,
name the touched surfaces, the mapping run, and why the effects are bounded.

Append the evidence as `## Implementation verification -- <agent> -- YYYY-MM-DD`:
tested SHA, interpreter, clean pre/post state, commands, outcomes, timing,
disposition of every non-pass, known omissions.

**Boundary C (falsification)** is the code reviewer's, and it is not re-running
Boundary B's command. Verify the record against the reviewed range, then attack
the claims that would hurt most if wrong.

## Plan review -- <reviewer> -- <YYYY-MM-DD>

Open every pass with its basis, so a later reader knows what was actually read:

```
Reviewed commit: <full commit id>
Target: <the sections this pass reviewed>
Prior findings: <ids being closed, or none>
Assurance path: <the plan's declared path>
```

**Obligation**: <the one clause this pass clears>
**Tier**: <Internal | Internal Security Review>
**Findings**: <raised | none>

An H3 inside another pass does not count as a pass of its own — a heading at
the left margin is what the checker reads.

## Code review -- <reviewer> -- <YYYY-MM-DD>

Floor: a same-type agent in an independent context, not the implementing agent.
Self-committed by its author; blocking findings move the plan to
`revising-code`. Same basis block, with the range made explicit:

```
Reviewed commit: <full commit id>
Target: <the code range this pass reviewed>
Prior findings: <ids being closed, or none>
```

**Bounding**: ACCEPTED | FULL RUN REQUIRED — recorded only after challenging a
named surface or mapped test, never because the field is present.
