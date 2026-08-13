<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/dual-review.md doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: comprehension outlives the artifact

**Source proposals** — three, accepted 2026-08-13, draining into one plan by
Maintainer direction:
* [`comprehension-outlives-the-room`](../proposals/2026-08-13-claude-comprehension-outlives-the-room.md)
  — the doctrine principle
* [`finding-tags-are-not-reasons`](../proposals/2026-08-13-claude-finding-tags-are-not-reasons.md)
  — comments and docstrings
* [`test-names-outlive-their-plans`](../proposals/2026-08-13-claude-test-names-outlive-their-plans.md)
  — test names

**Status**: awaiting-plan-review
**Plan review**: required(Internal) — the highest tier among the constituents.
The two operational proposals declare `not required`; the doctrine one requires
Internal because it edits the invariant kernel, and a plan draining a doctrine
change does not inherit its siblings' weaker declaration. **Fully Internal** by
Maintainer direction; no External round is sought at any stage.
**Last update**: 2026-08-13
**Opened**: 2026-08-13

> **Start precondition, Maintainer direction 2026-08-13**: *"I will finish
> review-efficient-lifecycle before this begins at all."* **No chunk of this
> plan executes until that plan archives.** This is not a per-chunk gate — it is
> a precondition on the whole plan, and it removes every sequencing hazard the
> constituent proposals wrote around.

## Source proposals

One principle and its two operational reaches. **A durable artifact must stand
without the deliberation that produced it** — because the record is a
by-product, and an artifact whose meaning depends on it decays at exactly the
rate the record archives. The two operational rules apply that to the artifact
classes where it has already failed and been measured: test names, and comments
and docstrings.

The plan executes the decisions. It does not re-open them.

## Scope

**In scope**

| From | What |
|---|---|
| doctrine proposal | Extend Anchor 16 in `doctrine/rationale.md` with the temporal half, paired with Anchor 17 so it cannot be read as licence to narrate |
| both operational proposals | Two convention rules in `AGENTS.md` and `templates/core/AGENTS.md`, **beside `**Naming.**`** — code-authoring conventions, not `## Review` |
| tags proposal | The finding-tag revision pass over 262 sites in `.py`, **in one plan rather than three phases** — see the start precondition |
| names proposal | ~36 coordinate-named test containers renamed, bodies untouched |
| tags proposal | Close the `dev/PLANNING.md` item this plan drains. **No revival rows** — nothing is deferred, so none is owed |

**The scope fence — what this plan does *not* do**

* **No new tests.** All three proposals concluded none is possible or warranted:
  no test distinguishes a comment that carries its reason from one that does
  not, and the rename's acceptance is that the suite is *unchanged*. **This is
  the inherited decision, not a judgement made here** — but see the open
  question below, which the plan review should settle rather than leaving to
  the implementer.
* **No lint.** Both operational proposals declined one with recorded revival
  conditions. Reviving either is a new proposal.
* **No sweep without reading.** Deletion has a bar — the sentence must stand
  without the tag — and that bar is a human read, per the board's own warning.
* **Out of scope by fence**: tags inside string literals that are test inputs,
  generated output, or fixture data (~8 sites). The rule governs prose
  addressed to a reader, not strings addressed to a parser.
* **No `doctrine/` change beyond Anchor 16.** The operational rules live in
  `AGENTS.md`; no second doctrine home is created.

### A correction the plan must carry: phase 1's trigger is already dead

The tags proposal routes the `_gate_preflight` sites through *"their security
plan's closure"*. **That plan archived at `f654dc0` without clearing them.**
Re-measured `as_of 2026-08-13`: **97** tags across
`bootstrap/tests/_gate_preflight.py` and `bootstrap/tests/test_gate_preflight.py`.

They are therefore **not** riding anything. This plan adopts them directly in
Chunk C rather than leaving them to a trigger that has passed — which is the
failure the tags proposal itself names, arriving inside the plan that drains it.

### Documentation / doctrine surface

* **Doctrine** — `doctrine/rationale.md`, Anchor 16 only.
* **Governing layer** — `AGENTS.md` and its shipped twin, in the conventions
  region beside `**Naming.**`. Placement is load-bearing: the tags review's E3
  found the rule under `## Review`, where an agent writing code never looks.
* **Deliberation layer** — `dev/PLANNING.md`, one item closed.

No `docs/` page changes.

## Sequence

```
1. Chunk A -- doctrine: Anchor 16 gains the temporal half     [commit pending]
2. Chunk B -- the two conventions, beside Naming, both copies [commit pending]
3. Chunk C -- the finding-tag revision pass                   [commit pending]
4. Chunk D -- the test-container rename                       [commit pending]
5. Chunk E -- close the PLANNING.md item                      [commit pending]
```

A and B land first because the rules should exist before the passes that apply
them — an agent touching a tagged file mid-pass should find the convention
already in `AGENTS.md`. Nothing after that is gated on anything: the start
precondition above retires the sequencing both operational proposals wrote
around.

### Chunk A -- doctrine

| # | File | Change |
|---|------|--------|
| A1 | `doctrine/rationale.md` | Anchor 16 gains the temporal paragraph: the reader who must understand a durable artifact is whoever meets it next, not whoever decided on it; the artifact must stand without the record. |
| A2 | `doctrine/rationale.md` | The Anchor 17 pairing, **in the anchor text** — writing the reason in is not licence to restate what the code already says. |

**Acceptance**: Anchor 16 carries both; Anchor 17 is named *in* the extension,
not only cross-referenced; `check_cairn.py` resolves every reference.

### Chunk B -- the two conventions

| # | File | Change |
|---|------|--------|
| B1 | `AGENTS.md` | Beside `**Naming.**`: tests are named for the property they pin; the docstring carries the *reason*, not the finding id. Includes the worked docstring example the names review required — **stating why the obligation exists and naming no coordinate**. |
| B2 | `AGENTS.md` | Beside B1: comments and docstrings explain the code, not the process. State the reason; do not cite the finding. |
| B3 | `templates/core/AGENTS.md` | B1 + B2, adopter-general wording. |
| B4 | `AGENTS.md` ×2 | A one-line pointer from the comprehension-floor paragraph to the conventions, so the derivation stays visible from the other direction. |

**Acceptance**: both rules present in both copies, in the conventions region and
**not** under `## Review`; the shipped copy carries no Cairn-only token
(`test_installed_operational_rule_is_project_general` still bites); the worked
example contains no finding tag — the names review supplied one that did, and
it is rejected here on the accepted terms.

### Chunk C -- the finding-tag revision pass

262 sites, less ~8 fenced. Revised **by reading**, one file at a time.

| # | Files | Notes |
|---|------|--------|
| C1 | `bootstrap/tests/_gate_preflight.py`, `bootstrap/tests/test_gate_preflight.py` | **97 sites** — the orphaned set. Largest and first, because they have no other home. |
| C2 | `tools/lifecycle_planner.py` + twin | ~21 each; **twins must stay byte-identical**. |
| C3 | the remainder | By file, smallest last. |

**Acceptance per file**: no tag remains except inside fenced string literals;
every sentence that previously leaned on a tag now states its reason; the
suite's pass/fail set is unchanged.

**Coordination**: `_gate_preflight` and the planner twins are high-traffic. Claim
work-intent per file, and check the active claim set immediately before each
commit — this tree has produced two in-file collisions in three days.

### Chunk D -- the test-container rename

~36 classes (re-measured `as_of 2026-08-13`), bodies untouched, coordinate moved
out of the name and the reason stated in the docstring.

The names proposal gated this on `review-efficient-lifecycle` archiving, because
it owns most of the affected classes and renaming another plan's tests mid-flight
is the collision this repository has paid for twice this week. **The start
precondition satisfies that gate for the whole plan**, so no per-chunk deferral
survives — and the `dev/PLANNING.md` revival row the proposal committed to is
no longer owed, because nothing is being deferred.

**Acceptance**: `pytest --collect-only` node count and pass/fail set **identical**
across the rename commit — that is the whole acceptance criterion, and it is
mechanically checkable by diffing collected node ids.

### Chunk E -- the tracked items

| # | File | Change |
|---|------|--------|
| E1 | `dev/PLANNING.md` | Close the "Opaque finding-IDs in code comments and docstrings" item this plan drains. |

**No revival row is created.** Both operational proposals committed to tracked
`dev/PLANNING.md` items as homes for *deferred* work; the start precondition
means nothing is deferred, so a row would manufacture a backlog entry for work
this plan completes. **Scope delta: preserved** — the outcome those rows existed
to protect (the work does not silently evaporate) is delivered by doing it.

## Acceptance criteria

* **Tests that must pass** — no new tests (inherited). The existing suite must
  be **unchanged** by Chunks C and D: same node ids, same pass/fail set. Chunks
  A, B and E are prose and run the standing gates.
* **Doc updates** — `doctrine/rationale.md`, `AGENTS.md` ×2, `dev/PLANNING.md`.
  No `CHANGELOG.md` entry: no adopter-facing *behaviour* changes; the shipped
  `AGENTS.md` paragraphs are the delivery.
* **Examples / smoke checks** — `python scripts/check_cairn.py` for every chunk;
  `python scripts/claim_check.py` per edited artifact.

### Author-accounting

**N/A on new contracts** — no new public entry point, no executable path, no
parser. Chunks C and D change comments, names and prose only.

One invariant this plan must not break, with its enforcer: the planner twins
stay byte-identical (Chunk C2), enforced by
`bootstrap/tests/test_scope_reduction_trap.py::test_the_two_planner_twins_stay_byte_identical`.

**Security preflight**: no answer changes. No trust boundary is added, moved or
widened; no input channel, parser, subprocess or executable path appears.

**Known omissions**: nothing here verifies that a revised comment *actually*
carries its reason. That is semantic, all three proposals said so, and review is
the enforcement.

## Verification

Boundary A per chunk: `check_cairn.py` for every chunk; for C and D, the mapped
test set for the touched files plus a collected-node-id diff.

Boundary B once, on a clean unchanged commit under the canonical interpreter
(`PYTHONDONTWRITEBYTECODE=1` — three suite nodes are bytecode-sensitive and this
is a measured environmental artifact, not a defect).

**Boundary B mode**: expected **bounded**, and the argument is owed *in the
record*, not here — no contract surface (the touched files are not the fidelity
or gate manifest, the lockfile schema, or the published `scaffold.py --manifest`)
and no trust-ceremony surface. **If Chunk C's reading turns up a tag inside a
security-gate file whose comment is load-bearing for the gate's behaviour, the
bounding fails and Boundary B runs full.** Uncertainty resolves to `full`.

## Open question for the plan review

**Should the two `AGENTS.md` conventions carry a parity guard?**

All three proposals declined new tests, and this plan inherits that. But the
scope-reduction-trap plan that closed today landed exactly this shape — rules in
`AGENTS.md` ×2 — and an obligation-parity test caught **four** cases where a
rule could be deleted from a shipped copy while the suite stayed green.

The counter-argument is the proposals' own: no test can tell whether a comment
carries its reason. **But that is not what a parity guard would test.** It would
test that the *rule text* survives in both copies, which is formal and fully
decidable — the same property `test_comprehension_floor.py` already pins for the
comprehension floor.

I have **not** added one, because adding scope the accepted proposals declined
is a deviation and not the implementer's call. **The plan review should settle
it.** If the answer is yes, it is one parametrised test in the shape of
`test_comprehension_floor.py` and belongs in Chunk B.

## Plan review

*Awaiting a fresh-context Internal pass.*

## Code review

*Filled in after implementation commits land.*

## Lasting-truth migration

*Filled in at archive time.*
