<!-- The plan template. Copy everything below the rule into
     `dev/plans/<slug>.md`. Keep it short: a plan is a working
     document, not a second proposal. -->

# Plan template

A non-trivial accepted proposal opens a plan. The plan says how the work
happens and how you will know it worked; it does not re-argue the decision.

## Lifecycle

```
awaiting-plan-review -> revising-plan -> ready-to-implement
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

**A plan review is Internal, fresh-context, and one round.** The fold carries
the plan to `ready-to-implement`; there is no second plan-review pass. Code
review's floor is separate and independent: not the implementing agent.

**Deviating from an accepted plan takes the Maintainer's word** — new scope, a
contract review never saw, an acceptance criterion you cannot meet, **or
accepted scope removed**. Removal counts in both directions: accepted scope is
a floor, and a reviewer cannot create authority to narrow by calling the
remainder out of scope.

**The Waiting line.** When a plan's next move becomes the Maintainer's, write
one header line, `**Waiting on Maintainer**: <what>`, in the header block,
beside Status, and delete it when they answer. Write it at three moments: work
reaches a fenced chunk (one marked MAINTAINER-GATED or MAINTAINER-ONLY), you
put a `defer` batch to the Maintainer, or you make a deviation request. Keep
`<what>` under 48 characters, the board's cell width; the detail stays in the
plan. A change note (`dev/plans/<slug>.md`) carries the line the same way. The
colon sits outside the bold, exactly as shown: with the colon inside the bold
the board does not read the line. `python tools/board.py --maintainer` lists
every artifact that carries it. This paragraph sits above the rule, so the line
is described here and not printed in the header below: a header line the board
reads would list every new plan as waiting.

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
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

## Sequence

One row per chunk: what it does, what gates it, roughly what it ships. Mark a
chunk MAINTAINER-GATED or MAINTAINER-ONLY where approval is actually
load-bearing — that fence, not a blanket per-commit gate, is where approval
binds to something specific. When work reaches a fenced chunk, write the
Waiting line (`**Waiting on Maintainer**: <what>`) in the header block, beside
Status, and delete it when the Maintainer answers.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | | | |

## Acceptance criteria

Per chunk, each falsifiable. A criterion you cannot imagine failing is not one.

A security-touching plan re-answers the five security-preflight
questions only where its chunking changes an answer — most often S2
(which chunk runs the mutation) and S3 (which gate command fires the
check).


  <!-- cairn:slot acceptance-doc-tooling -->
  Cairn's doc surface is mostly hand-authored Markdown read on GitHub;
  the doc tooling is drift-prevention, not generation:
  - **Snippet-sync** — `python scripts/sync_doc_snippets.py` pulls
    fenced blocks from runnable example sources into docs; update the
    source, then run the sync (never hand-edit a synced block).
  - **Prose-integrity gate** — `python scripts/check_cairn.py` resolves
    every internal Markdown link / anchor and every claim-path; it is
    the doc smoke for any Markdown change.
  - **Link check** — `python scripts/link_check.py` for the broader
    cross-reference sweep.
  There is no schema-render generator; a plan that introduces one names
  its source + render command here.
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
standing non-pytest gate for the touched surface. Run that scope while
iterating. There is no permanent fast tier; if a substantive surface has
no reviewed mapping or cannot be bounded confidently, run the full suite.

After the final implementation commit, Boundary B runs once against a clean,
unchanged commit under the canonical interpreter. The default is the **full
suite**; a plan whose reviewed mapping **bounds the change's effects
confidently** may instead run that mapping plus every standing gate for every
touched surface. Bounded mode **refuses** — run full — when the change touches a
**contract surface** (install contract, fidelity or gate manifest, lockfile
schema, published `scaffold.py --manifest`) or a **trust-ceremony surface**
(any high-risk surface `AGENTS.md` names, or release/security ceremony work).
**Uncertainty resolves to `full`.** The commands:

* **Engine + seed-0 order coverage** — `python -m pytest bootstrap/tests
  --quality-gate-shuffle-seed=0`.
* **Static quality legs** — `python scripts/quality_gate.py --sub neutrality
  --sub redundancy` (does not dispatch pytest again).
* **Prose integrity** — `python scripts/check_cairn.py`.
* **Write-time claim check** — `python scripts/claim_check.py <file>` once for
  each authored proposal, plan, or doc.
* **Plan-specific acceptance commands** — the mapped tests, security budgets,
  doc-drift gates, public-path smokes, and other commands named above.

Only after that stable run, append a dated section named
`Implementation verification -- <agent> -- YYYY-MM-DD` at H2. Do not place an
empty heading in a new plan. The record uses these exact fields:

* **Boundary B mode** — `full` | `bounded`. On `bounded`, also name the touched
  surfaces, the reviewed mapping and standing gates run, why the effects are
  bounded, and the explicit absence of any contract or trust-ceremony surface.
* **Tested commit** — full SHA.
* **Reviewed range** — base and tested endpoint.
* **Interpreter/runtime** — canonical path and version.
* **Pre-run state** and **Post-run state** — clean tree and identical tested
  `HEAD`.
* A command table with **Command**, **Exit**, **Outcomes**, and **Elapsed**
  columns, including pass/fail/skip/xfail/xpass counts where applicable.
* **Non-pass disposition**, **Plan-specific acceptance commands**, and
  **Known omissions**.
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
Boundary B's command. Verify the record against the reviewed range, then run
independent **targeted falsification** — attack the claims that would hurt most
if wrong.

A **fresh full run** is required, and the record does not carry, when any of
these holds: **no valid Boundary B record exists**; an **unrecorded
cross-surface dependency** appears; the run reports a **skip, xfail, or xpass**
the record does not dispose of; **review sharpening changes implementation,
tests, executable templates, or** fixtures; a **trust ceremony that explicitly
requires** one applies; or there is a **concrete reason to distrust or falsify**
the evidence.

## Dispositions

*Filled at archive-preparation, and this section is why the plan cannot archive
without it.* Every **explicitly-deferred follow-up** this plan carries takes one
recorded disposition: `accept` (fixed in scope), `guard (<path>::<node>)` (homed
in something that **executes** and names the node -- a comment is not eligible,
because comments do not fire), `wontfix` (explicit non-action, with a
rationale), or `defer`.

**Every deferred item is recorded in `dev/PLANNING.md`, and requires the
Maintainer's authorization quoted verbatim.** Writing the disposition is not
performing the deposit. An item left only in a plan that then archives is
invisible to anyone looking for outstanding work, and archived artifacts are
not scanned by default -- so it is not deferred, it is lost. Present `defer`
requests as **one batch**; that batching keeps the Maintainer gate affordable.
When you put the batch to the Maintainer, write the Waiting line
(`**Waiting on Maintainer**: <what>`) in the header block, beside Status, and
delete it when they answer.

Record the outcome as a `Dispositions: ...` line so it reconstructs from the
durable record alone. **An append re-opens the attestation**: this section is
append-only, so if you add content after writing the line, restate or amend it.

Two eligibility rules bound the choice: a follow-up that **reaches an adopter,
blocks a release, or needs a Decision** cannot be `wontfix`; and one **named by
a closed artifact's disposition block** cannot be `wontfix` without the
Maintainer.

**Nothing mechanical checks any of this.** The lifecycle planner that once
parsed for a `Dispositions:` block was retired in August 2026; the enforcer is a
reviewer opening the artifact at archive-preparation. The full rule, including
why, is `doctrine/lifecycle.md` > "Archive precondition" and
`doctrine/plans.md` > "Lasting-truth migration doctrine".

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
`revising-code`, and the implementer's answer carries it to `ready-to-archive`.
A second code-review pass runs only when the revision introduced new defects,
never to re-confirm that the first round's findings were addressed. Same basis
block, with the range made explicit:

```
Reviewed commit: <full commit id>
Target: <the code range this pass reviewed>
Prior findings: <ids being closed, or none>
```

**Bounding**: ACCEPTED | FULL RUN REQUIRED — recorded only after challenging a
named surface or mapped test, never because the field is present.

**Waiting-line check.** `git log -p` on the plan must show a Waiting line for
each fenced chunk whose fence became the next move inside the reviewed range,
and for each deviation request made in it. A fence the range did not reach is
not checked, and one whose wait is declared on a marked board row is checked
there. A missing line is a finding, recorded in
`dev/measurement/maintainer-view-misses.md`.
