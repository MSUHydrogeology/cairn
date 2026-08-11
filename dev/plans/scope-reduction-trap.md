<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/plans.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: bootstrap/tests/test_scope_reduction_trap.py -->
<!-- One forward reference, created by Chunk E and also registered under
     `Proposed paths:`. The marker exempts only its own contiguous bullet
     block, so this file-scoped directive covers the chunk table that names the
     same path. The line drops when the file lands. -->

# Plan: the scope-reduction trap

**Source proposal**: [`2026-08-11-claude-scope-reduction-trap`](../proposals/archive/2026-08-11-claude-scope-reduction-trap.md)
**Status**: executing
**Plan review**: none — **waived by the Maintainer at plan-open**, adjusting the
accepted proposal's `required(External)` declaration. See "The waived plan
review" below; the code review before archive is unaffected and remains
mandatory.
**Last update**: 2026-08-11
**Opened**: 2026-08-11

## The waived plan review

The source proposal declared `Plan review: required(External)`. That field sits
on an *accepted* proposal, so relaxing it is an adjustment to accepted terms and
is the Maintainer's alone. It is recorded here rather than silently applied.

**Maintainer authorization (verbatim):**

> "Let's think about this external Plan review. It quite honestly creates a huge
> hurdle to implementation. If we've already done an External proposal review,
> why replicate it here? I mean, many many people won't have another Agent at
> all--the fact that I'm running three is extremely uncommon."

followed by the selection **"Waive it"** from the options put to the Maintainer.

**The reasoning, applying this plan's own rule to itself.** The baseline
commitment behind `required(External)` is *an independent read before this
lands*. Two passes would ask different questions — is this the right rule,
versus is this the right distribution of it — but the **proposal** review
already answered the second: Codex's E5 finding *was* the distribution finding,
and the Decision baked its surface list into the proposal's Part 9. What
remains is executing an enumerated list, and the live risk is executing the
wrong one or quietly reviving the declined planner gate.

The **code review** catches that better, because it reads the landed diff
instead of a promise to produce one. A plan never archives without it, and its
floor — not the implementing agent — is reachable by a single-agent adopter
whose reviewer is the Maintainer.

**Outcome test: preserved.** The independent read still happens; only its
position moves, from before the diff exists to after. No remainder record is
owed.

**Second, and the reason this is worth recording beyond this plan.** The
Maintainer's objection is a finding about Cairn, not about this change:
stacking `External` at every tier is reachable for a three-agent tree and a
real barrier for the one-agent scientist Cairn is built for. The External floor
already reads *"a different agent type, **or a human**"*, so the barrier is
partly a habit of this repository rather than a rule. Whether the tier-stacking
default should change is out of scope here and belongs in its own proposal.

## Source proposal

Review has a systematic bias toward narrowing: a reviewer who recommends a
reduction bears no cost, looks prudent, and can never be shown wrong because
the wider version is never built. The proposal names that bias, and binds it
with the **baseline-bound outcome test** — when a change is narrowed, ask
whether the narrower version still delivers the *concrete outcome commitments
of the baseline artifact*. `preserved` needs nothing. `degraded` and `lost`
both take a declaration, a grouped remainder record, and a Maintainer authority
point. Declining a stronger outcome a reviewer proposed is not a reduction at
all.

The plan distributes that settled rule. It does not re-open the rule.

## Proposed paths

Proposed paths:
- `bootstrap/tests/test_scope_reduction_trap.py` — the obligation-parity test; lands in Chunk E.

## Scope

**In scope** — landing the accepted Round-6 text across the surfaces the
proposal's Part 9 names: Cairn's doctrine, the shipped and self-hosted
templates, the planner scaffolds an author actually reads, the governing
`AGENTS.md` deviation wording, the adopter-facing `agent_collaboration.md`, the
board's inline disposition taxonomy, and one obligation-parity test.

**The scope fence — what this plan does *not* do:**

* **No planner gate.** Round 3 declined it and the Decision accepted that
  disposition. `_conformance_violations` is untouched; no transition refuses on
  a missing or malformed `Scope delta`. The revival condition stands as
  recorded in the proposal — if authors omit the declaration in practice, the
  gate becomes warranted, and that is a new proposal.
* **No mutation tests for a gate that does not exist.** They were bound to the
  declined mechanism.
* **No lockfile schema change and no fidelity-manifest change.** The install
  set is unchanged: every file this plan touches is already in it.
* **No retro-fitting of in-flight artifacts.** The rule is prospective. No
  existing proposal or plan gains a `Scope delta` line.
* **No corpus measurement of historical reductions.** The proposal explicitly
  declined to manufacture a number for the recurrence claim; the plan inherits
  that refusal.

**Twin and slot parity.** Three pairs move together and must not drift:

| Pair | Relationship |
|---|---|
| `tools/lifecycle_planner.py` ↔ `templates/skills/_lib/lifecycle_planner.py` | **Byte-identical twins.** Verified identical at plan-open. |
| `dev/proposals/_template.md` ↔ `templates/core/dev/proposals/_template.md` | **Slot-differentiated.** Self-hosted carries filled slots; shipped carries placeholders. New text lands in *both*, outside the slots. |
| `dev/plans/_template.md` ↔ `templates/core/dev/plans/_template.md` | Same slot relationship. |

Likewise `AGENTS.md` ↔ `templates/core/AGENTS.md`,
`dev/agent_collaboration.md` ↔ `templates/core/dev/agent_collaboration.md`, and
`dev/PLANNING.md` ↔ `templates/core/dev/PLANNING.md`.

### Documentation / doctrine surface

**This plan is almost entirely doctrine surface**, which is why it exists.

Routing under [`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):

* **Governing layer** — `AGENTS.md` and its shipped twin gain one clause on the
  deviation gate. Cross-cutting prescription an agent must obey, so it belongs
  here and nowhere else.
* **Doctrine (published methodology)** — `doctrine/dual-review.md` holds the
  **canonical** statement of the trap and the outcome test, because it is a
  property of review and it sits as the mirror of the clean-pass trap.
  `doctrine/proposals.md`, `doctrine/plans.md`, and `doctrine/lifecycle.md`
  carry only their **stage-specific obligation** and point at that canonical
  home. One canonical home; the others point.
* **Deliberation layer** — `dev/agent_collaboration.md` and its shipped twin get
  the short operational statement in "The review loop", matching how the
  clean-pass trap is already carried there.
* **Descriptive layer** — [`docs/glossary.md`](../../docs/glossary.md) gains the
  three terms a reader now meets (`outcome test`, `scope reduction`,
  `scope-remainder record`). The glossary states it defines every term that
  carries weight, so omitting these would falsify its own claim.

No `docs/` page other than the glossary changes.

## Sequence

```
1. Chunk A -- doctrine: the trap, the outcome test, the stage floor   [commit be40b41]
2. Chunk B -- vocabulary reconciliation (scope-cut vs scope reduction) [commit pending]
3. Chunk C -- templates + planner scaffolds (the author-facing surface)[commit pending]
4. Chunk D -- governing + deliberation surfaces (AGENTS, collaboration)[commit pending]
5. Chunk E -- obligation-parity test, glossary, changelog              [commit pending]
```

Chunks A and B both edit `doctrine/dual-review.md` and are sequenced apart on
purpose: A *adds* a section, B *edits* an existing sentence inside lens 9. Two
distinct claims, two reviewable diffs.

### Chunk A -- doctrine: the trap, the outcome test, the stage floor

| # | File | Change |
|---|------|--------|
| A1 | `doctrine/dual-review.md` | New `## Review expectations — the scope-reduction trap` section, sibling to and immediately after the clean-pass trap. Carries the **canonical** text: the asymmetry; the reviewer's obligation to state what is lost and why the narrower change still reaches the cause; the baseline-bound `preserved / degraded / lost` test; the declined-expansion clause. |
| A2 | `doctrine/proposals.md` | Pre-Decision obligation: a revision that degrades or loses a baseline outcome states the `Scope delta` and carries the grouped remainder record; the Maintainer decides the resulting scope with the reduction visible. Baseline = scope **as opened**. Points at A1 for the test itself. |
| A3 | `doctrine/plans.md` | Post-Decision obligation: accepted scope is a **floor**. Sequencing may move work between chunks; removing it is a deviation under the `AGENTS.md` gate. Explicit: *a plan reviewer cannot create that authority by calling the remainder "out of scope."* Baseline = scope **as accepted**. |
| A4 | `doctrine/lifecycle.md` | The grouped scope-remainder record **blocks archive** until every entry carries an explicit disposition, stated inside the existing Archive-precondition section so the gate has one home. |

**Acceptance for A**: the canonical text appears exactly once; A2–A4 point at it
rather than restating the test; `python scripts/check_cairn.py` resolves every
new cross-reference.

### Chunk B -- vocabulary reconciliation

The unsound path the proposal's E4 found: today an author can remove real work,
label it a *scope-cut*, take the `accept` disposition, and be conformant.

| # | File | Change |
|---|------|--------|
| B1 | `doctrine/dual-review.md` | Lens 9's satisfier mapping: `scope-cut` → `accept` reserved for **claim correction with no removed work**; removal of previously stated work is a **scope reduction** taking the A1 path. |
| B2 | `templates/modules/team-gated/dual-review.md` | The same reconciliation in the transplanted lens roster (the installed body adopters read). |
| B3 | `doctrine/lifecycle.md` | The `accept` bullet in the archive-time disposition vocabulary carries the same restriction. |
| B4 | `dev/PLANNING.md` | The board's inline taxonomy `accept` bullet, same restriction. |
| B5 | `templates/core/dev/PLANNING.md` | Shipped twin of B4. |

**Acceptance for B**: no surface still maps unrestricted `scope-cut` → `accept`;
`grep -rn "scope-cut" doctrine/ templates/ dev/PLANNING.md` returns only
restricted forms.

**Serialization note for B4.** `dev/PLANNING.md` is a shared communication file
edited only at defined serialization points. The edit is authorized by the
accepted proposal, which names the board's inline taxonomy explicitly. It is a
**taxonomy correction, not a row** — no backlog item is added, which is the
outcome E2 was protecting. Commit it path-scoped and check the active intent
set immediately before.

### Chunk C -- templates and planner scaffolds

This is the surface E5 was about: the author meets the rule while typing, not
in a doctrine essay recalled later.

| # | File | Change |
|---|------|--------|
| C1 | `dev/proposals/_template.md` | `## Response` shape gains the `**Scope delta**: preserved \| degraded \| lost` prompt, with the "required when the revision narrows what the artifact will deliver; omit when nothing was narrowed" condition and the grouped-remainder requirement for `degraded`/`lost`. |
| C2 | `templates/core/dev/proposals/_template.md` | Same text, shipped twin. Lands outside every `cairn:slot` block. |
| C3 | `dev/plans/_template.md` | The plan-review pass shape (the `### Sharpening` comment block) gains the same prompt, since Sharpening is where a plan reviewer's narrowing is dispositioned. |
| C4 | `templates/core/dev/plans/_template.md` | Same text, shipped twin. |
| C5 | `tools/lifecycle_planner.py` | `_scaffold`: the proposal `revised` block and the plan `executing` block each gain the `**Scope delta**` placeholder line. **String literals only** — no change to `_conformance_violations`, no new refusal, no parse. |
| C6 | `templates/skills/_lib/lifecycle_planner.py` | Byte-identical twin of C5. |

**Acceptance for C**: `diff tools/lifecycle_planner.py
templates/skills/_lib/lifecycle_planner.py` is empty; `python
tools/lifecycle_planner.py next <artifact> --to revised` emits the new line;
the planner still refuses nothing it did not refuse before.

**Why C5 cannot drift into a gate.** The scaffold is a printed string the
operator copies. Adding a placeholder to it changes what an author *sees*; it
changes no transition legality. If a reviewer of this plan reads C5 as a gate,
that reading is the thing the fence forbids.

### Chunk D -- governing and deliberation surfaces

| # | File | Change |
|---|------|--------|
| D1 | `AGENTS.md` | The deviation bullet — "new scope, a struck chunk revived, a contract the review never saw, an acceptance criterion you cannot meet" — gains **accepted scope removed**, naming it a scope reduction and pointing at the outcome test. |
| D2 | `templates/core/AGENTS.md` | Same clause, shipped twin. This is the load-bearing copy: adopters receive it. |
| D3 | `dev/agent_collaboration.md` | "The review loop" gains the short operational statement of the trap, beside the clean-pass-trap sentence already there. |
| D4 | `templates/core/dev/agent_collaboration.md` | Same, shipped twin. |

**Acceptance for D**: the deviation gate now enumerates reduction alongside
expansion in both copies; the two `agent_collaboration.md` statements say the
same thing.

### Chunk E -- test, glossary, changelog

| # | File | Change |
|---|------|--------|
| E1 | `bootstrap/tests/test_scope_reduction_trap.py` | Obligation-parity test in the shape of `bootstrap/tests/test_comprehension_floor.py`: alternation patterns for each load-bearing obligation across each surface that must carry it, so a **rewording passes and a deletion fails**. |
| E2 | `docs/glossary.md` | Three entries under "Review": *outcome test*, *scope reduction* (distinguished from *scope-cut*), *scope-remainder record*. |
| E3 | `CHANGELOG.md > Unreleased > Added` | One release-note line. |

## Acceptance criteria

* **Tests that must pass** — `bootstrap/tests/test_scope_reduction_trap.py`
  (new, E1); `bootstrap/tests/test_lifecycle_contract.py` and
  `bootstrap/tests/test_lifecycle_cli.py` (the planner surface C5/C6 touches);
  `bootstrap/tests/test_core_dev_folders.py` and
  `bootstrap/tests/test_doc_governance.py` (the template surface); then the
  full suite at Boundary B.
* **Doc updates that must land** — hand-authored throughout. `docs/glossary.md`
  (E2) and `CHANGELOG.md > Unreleased > Added` (E3). No generated or
  snippet-synced doc is touched.
* **Examples / smoke checks required** — `python scripts/check_cairn.py` (every
  chunk touches Markdown); `python scripts/claim_check.py dev/plans/scope-reduction-trap.md`
  at plan-open; `python tools/lifecycle_planner.py next` against a live
  artifact, to confirm C5 prints and refuses nothing new.
* **Inbound path-link updates** — the source proposal moves to
  `dev/proposals/archive/` in the plan-open commit; this plan's Source-proposal
  link already points there. `PLANNING.md` and `NEXT_SESSION.md` refer to plans
  by stem, so they need no update.

### Author-accounting — invariants, failure modes, edge cases

**N/A on new contracts** — this plan adds no public entry point, no new
contract, and no executable path. C5/C6 change string literals inside an
existing function.

Three invariants it must *not* break, each with its enforcing check:

| Invariant | Enforced by |
|---|---|
| The planner twins stay byte-identical | `diff` in C's acceptance, plus the standing twin-parity coverage in [`bootstrap/tests/test_lifecycle_contract.py`](../../bootstrap/tests/test_lifecycle_contract.py) |
| No transition refuses on anything new | `bootstrap/tests/test_lifecycle_cli.py` unchanged and green; `_conformance_violations` byte-unchanged |
| The shipped templates' slot structure is intact | `bootstrap/tests/test_core_dev_folders.py`; new text lands outside every `cairn:slot` block |

**Security preflight** — no answer changes. This plan mutates Markdown and two
string literals; it parses no untrusted input, resolves no executable, and
touches no named high-risk surface.

**Known omissions**: the plan does not test that a `Scope delta` declaration is
*truthful*. That is semantic and was left to human review by the accepted
Round-3 disposition; E1 tests that the obligation is stated, not that it is
obeyed. Stating this plainly is the point — the residual is the reason the gate
was declined, not an oversight.

## Verification

Boundary A, per chunk: the mapped tests named in Acceptance for the chunks that
touch code (C, E), plus `python scripts/check_cairn.py` for every chunk, since
every chunk touches Markdown.

Boundary B, once, after the final implementation commit, on a clean unchanged
commit under the canonical interpreter:

* `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0`
* `python scripts/quality_gate.py --sub neutrality --sub redundancy`
* `python scripts/check_cairn.py`
* `python scripts/claim_check.py` on this plan and the archived proposal

**Neutrality matters more than usual here.** Chunk C edits shipped templates
and Chunk D edits `templates/core/AGENTS.md`; both are on the vendor-neutrality
surface. The neutrality leg is not a formality on this plan.

Then append `## Implementation verification -- <agent> -- YYYY-MM-DD` with the
fields the template names.

**Note on doc gates**: `check_cairn.py` catches drift, not *absence*. It will
not tell anyone that Chunk D2 was skipped. E1 is what covers absence, and it
covers only the surfaces it enumerates — so the reviewer checks the enumeration
against Part 9 of the proposal, not just that the test passes.

## Code review

*Filled in after implementation commits land.*

## Lasting-truth migration

*Filled in at archive time.*
