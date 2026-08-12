<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/plans.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: the scope-reduction trap

**Source proposal**: [`2026-08-11-claude-scope-reduction-trap`](../proposals/archive/2026-08-11-claude-scope-reduction-trap.md)
**Status**: review
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
default should change is out of scope here. **It is already owned** — see the
Sharpening's disposition ledger; do not open a proposal for it.

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
3. Chunk C -- templates + planner scaffolds (the author-facing surface)[commit ccffb77]
4. Chunk D -- governing + deliberation surfaces (AGENTS, collaboration)[commit 64b4ee2]
5. Chunk E -- obligation-parity test, glossary, changelog              [commit 4f17fef]
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

* the **mapped** pytest set, generated by this exact command rather than
  described (code-review C5 — the earlier wording named neither the grep nor
  the module list, and a reviewer's own grep returned a different count):

  ```bash
  grep -rlE 'lifecycle_planner|dev/(plans|proposals)/_template|core/AGENTS|agent_collaboration|PLANNING\.md|dual-review|scope_reduction' bootstrap/tests/*.py | sort
  ```
* `python scripts/quality_gate.py --sub neutrality --sub redundancy`
* `python scripts/check_cairn.py`
* `python scripts/claim_check.py` on this plan and the archived proposal

### Sequence revision 2026-08-11 — the full suite, replaced by a mapped run

This section originally specified `pytest bootstrap/tests` in full. **Maintainer
challenge at Boundary B**: *"Why are you doing a full suite test run? Haven't
you basically just edited doctrine files? You haven't touched a contract
surface."*

The challenge is correct, and the original line was reflex rather than
judgement — copied from the template without testing it against what this plan
actually changed. AGENTS.md reserves the full suite for a substantive code
surface that has **no reviewed mapping** or whose effects **cannot be bounded
confidently**. Both are bounded here:

* The entire executable diff is **four hunks inside `_scaffold`**, all string
  literals, reachable only through `next --to`. Both paths were exercised
  directly against fixtures.
* `_conformance_violations` is byte-unchanged, and a test now pins that.
* No contract surface is touched — not the install set, the lockfile schema,
  the fidelity manifest, the gate manifest, nor `bootstrap/_scaffold/` (so no
  AST-attestation re-anchor is owed either).
* Everything else is Markdown plus one new test module that only reads files.

**Outcome test on this plan's own verification: preserved.** The baseline
commitment is that the landed change is verified against the surfaces it
touches. A mapped run over all 25 modules that reference those surfaces, plus
every standing gate, still delivers it. This is ceremony cut, not reach cut —
no declaration or Maintainer allowance is owed, and this note exists because
the reasoning should be visible, not because the rule requires it.

**Neutrality matters more than usual here.** Chunk C edits shipped templates
and Chunk D edits `templates/core/AGENTS.md`; both are on the vendor-neutrality
surface. The neutrality leg is not a formality on this plan.

**Correction, recorded rather than quietly fixed.** The Chunk B commit body
(`99451d2`) claims `quality_gate neutrality fail=0`. That is **false**. The
neutrality leg stands at **fail=93 as_of 2026-08-11**, and stood there before
this plan opened — I read only the tail of the gate output, saw the redundancy
summary and the neutrality *info* lines, and inferred a summary line I never
saw. The claim is wrong; the underlying state is unchanged by this work.
Verified at Chunk D: every one of the 93 sits in fixtures, adopter-example
docs, and the lifecycle-metrics vendor registries. Exactly one falls in a file
this plan touches — `doctrine/dual-review.md:57` — and it was last written by
`160cbb2`, not by any commit here. A reader of `99451d2` should take the
verification line as covering `check_cairn` and redundancy only.

Then append `## Implementation verification -- <agent> -- YYYY-MM-DD` with the
fields the template names.

**Note on doc gates**: `check_cairn.py` catches drift, not *absence*. It will
not tell anyone that Chunk D2 was skipped. E1 is what covers absence, and it
covers only the surfaces it enumerates — so the reviewer checks the enumeration
against Part 9 of the proposal, not just that the test passes.

## Implementation verification -- Claude -- 2026-08-11

**Tested commit**: `4f17fefd84ff2059be15d90e0f0a69fcb4db392d`
**Reviewed range**: `6a4b3a0..4f17fef` (five implementing commits plus
plan-open).
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13), the canonical interpreter.
**Pre-run state**: the working tree carried **another agent's** uncommitted
work (in `bootstrap/tests/`: `_gate_preflight.py` modified,
`test_lifecycle_vocabulary.py` untracked), so the run was
performed in a **detached git worktree at `4f17fef`**, verified clean by
`git status --short` before the run. Nothing of this plan's was uncommitted.
**Post-run state**: worktree unchanged at `4f17fef`; removed after the run.

| Command | Exit | Outcomes | Elapsed |
|---|---|---|---|
| mapped pytest set (25 modules, see Verification) | 1 | **916 passed, 1 failed** | 83.5 s |
| `scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | neutrality fail=93 info=21; redundancy fail=0 info=2 | — |
| `scripts/check_cairn.py` | 0 | 176 Markdown files, no issues | — |
| `scripts/claim_check.py` (plan, archived proposal) | 0 | clean on both | — |
| `tools/lifecycle_planner.py next --to revised` / `--to executing` | 0 | both scaffolds emit the block; gating preconditions unchanged | — |

**Non-pass disposition.**

* `test_security_check.py::test_detached_checkout_excludes_an_ignored_pytest_override`
  — **pre-existing, not in this range.** Reproduced at `6a4b3a0`, the commit
  before this plan opened, in its own clean worktree. It fails on stray
  `__pycache__/*.pyc` files inside `bootstrap/tests/`, which the detached-
  checkout guard reports as `extra=[...]`. That is environment pollution, not
  a defect in the reviewed bytes. Surfaced to the Maintainer rather than
  fixed here — it is outside this plan's scope and belongs to whoever owns
  that guard.
* **Correction (added at Sharpening, from code-review C6).** The row above
  reports the *mapped* set's one failure. The **full** suite at `4f17fef` is
  **3 failed / 3063 passed / 1 skipped**, and at `6a4b3a0` — before this plan
  opened — **3 failed / 2962 passed / 1 skipped**, with the **same three node
  ids**. So all three are pre-existing and the attribution argument holds, but
  "1 failed" describes the mapped set and must not be read as the tree's
  standing state. The mapped set was too small to see the other two.
* **Neutrality `fail=93`** — pre-existing and unchanged; reproduced at clean
  `HEAD` before any of this work. All 93 sit in test fixtures, adopter-example
  docs, and the lifecycle-metrics vendor registries. Exactly one falls in a
  file this plan touches, `doctrine/dual-review.md:57`, last written by
  `160cbb2`. See the correction note above for the false `fail=0` claim in
  `99451d2`'s commit body.

**Plan-specific acceptance commands.** Twin parity
(`diff tools/lifecycle_planner.py templates/skills/_lib/lifecycle_planner.py`,
empty, and pinned by a test node); both planner scaffold paths exercised;
perturbation of the new test in both directions — deleting the AGENTS clause,
the template declaration and the scaffold literal turns 5 nodes red, and adding
a scope-delta refusal to `_conformance_violations` turns the fence node red.

**Known omissions.**

* The **full** suite was not run; a mapped 25-module set was, for the reason
  recorded in the Sequence revision above. A code reviewer who disagrees with
  that bounding should run the full suite — that judgement is theirs.
* No test asserts that a `Scope delta` declaration is **truthful**. It cannot;
  the property is semantic, which is why the gate was declined. Review is the
  enforcement, and saying so is the honest form of the residual.
* The recurrence claim behind the proposal remains the Maintainer's standing
  observation. Nothing here measures it, and the proposal explicitly declined
  to manufacture a number.

## Code review

*Filled in after implementation commits land.*

## Code review -- Claude (Internal) -- 2026-08-11

**Model**: Claude Opus 5 (`claude-opus-5`)

**Tier — stated honestly.** This is a **fresh-session, same-agent-type** read: the
**Internal floor**, *not* a cross-type External one. It matters here more than
usual. The source proposal got two External (Codex) rounds, but this plan's own
plan review was **waived**, so before this section nothing structurally
independent had read the *landed diff* — and the waiver's own argument was that
"the code review catches that better, because it reads the landed diff." That
argument is sound; it just does not make a same-type read into an independent
one. If the Maintainer wants External assurance on the distribution, this
section does not supply it.

**Reviewed range**: `3bcc0b7..d330083`, filtered per-commit to the seven
`scope-reduction-trap` commits (`3bcc0b7`, `be40b41`, `99451d2`, `ccffb77`,
`64b4ee2`, `4f17fef`, `d330083`). Other agents' commits interleave that range;
they were excluded by diffing each commit against its own parent, not by
trusting the range.
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python
3.13.13), the canonical interpreter.
**Method**: two detached worktrees (`4f17fef`, `6a4b3a0`), seven mutations of
the landed tree, one independent **full**-suite run, and a vacuity sweep of
every pattern in the new test against the pre-change bytes.

**Verdict: REVISE.** The distribution is faithful — I could not find an
enumerated Part 9 surface that was missed, and the declined planner gate really
was left out; I checked that at every home it could have been revived in. Three
things need fixing first. The change **created a twin drift** that leaves the
exact unsound `scope-cut` mapping E4 exists to close still live in Cairn's own
tree (C1, the only P1). The obligation-parity test — the artifact whose whole
job is to make omission visible — leaves the R2-E1 authority rule **unpinned on
two adopter-facing surfaces**, and I re-introduced that contradiction by
mutation with the suite green (C3). And the invariant "no transition refuses on
anything new" has named enforcers that do not enforce it at one of the two
planner surfaces (C4). None of this re-opens the rule. All of it is cheap.

### Findings

**[C1 -- P1] Chunk B created a twin drift, and the surviving copy is the
unsound mapping the proposal exists to close.** `dev/modules/dual-review.md` is
Cairn's *installed* copy of `templates/modules/team-gated/dual-review.md` — the
lockfile records the pair (`src: modules/team-gated/dual-review.md` →
`dst: dev/modules/dual-review.md`). Chunk B edited only the shipped source. The
installed copy still carries the **unrestricted** satisfier mapping
(`dev/modules/dual-review.md:74`: *scope-cut* → `accept`) with no restriction,
no trap, and no outcome test.

This is not pre-existing drift. I extracted the blockquoted `## Template
content` body from both files at two commits:

* at `6a4b3a0` (before the plan opened) — 103 lines each, **byte-identical**;
* at `d330083` — 131 vs 103, **divergent**.

So Chunk B introduced it. Cairn is its own first adopter, and this is the E5
failure mode reproduced in Cairn's own tree: a reader who consults the installed
module gets the mapping that lets lost work take an `accept`.

Two contributing causes worth naming, because they are why nobody saw it:

* **Chunk B's acceptance criterion cannot see the file.** It reads
  `grep -rn "scope-cut" doctrine/ templates/ dev/PLANNING.md` — three roots, none
  of which contains `dev/modules/`. The criterion was written narrow enough to
  pass over the miss.
* **The plan's twin-parity table omits the pair.** It lists three pairs plus
  `AGENTS.md`, `agent_collaboration.md` and `PLANNING.md`, then Chunk B edited a
  seventh pair that the table never named.

*Satisfier*: **doc** — bring `dev/modules/dual-review.md` into line with the
shipped module; **test** — add the pair to `_SURFACES` in
`bootstrap/tests/test_scope_reduction_trap.py` so it is checked as a pair, as
every other surface in that dict already is.

**[C2 -- P2] The record's "claim_check clean" was not reproducible from the
committed tree, and only became true by an unrelated commit.** The record's
table asserts `scripts/claim_check.py` (plan, archived proposal) → exit `0`,
*"clean on both"*. The **Pre-run state** paragraph cites, by full slashed path,
another agent's then-**untracked** test module. `claim_check` treats a
backticked token whose first segment is a real top-level directory as a repo-path
claim and resolves it against the **working tree**, so it passed only because
that agent's file happened to be sitting on disk.

I record the timeline precisely, because it moved under me mid-review:

* At `d330083` in a clean detached worktree — and in the main working tree when
  I first probed it — the plan carried **1 hard flag**: `line 359: cited path
  does not resolve: bootstrap/tests/test_lifecycle_vocabulary.py`.
* While I was reviewing, `ca22f21` (`review-efficient-lifecycle A6/A7`, another
  agent) committed that file. The main tree is now **clean**; a clean checkout
  of `d330083` is **still red**.

So the gate result asserted in the record was not derivable from the bytes the
record covers, and its becoming true is an accident of someone else's commit.
Under `AGENTS.md` > *Verifying claims*, "a hard flag is resolved before commit."
`doctrine/plans.md` > "Forward-reference paths" already names the remedy for
this exact shape: cite the existing parent directory plus the **bare filename**,
since a token with no `/` is not a repo-path claim.

*Satisfier*: **doc** — reword the citation so the plan does not depend on
another agent's tree state, and note in the record that the row was
working-tree-dependent. (No re-run is needed; the current result is clean.)

**[C3 -- P2] The obligation-parity test does not pin the authority rule on two
of the surfaces that carry it, and I re-introduced R2-E1 with a green suite.**
The per-surface obligation sets are ad-hoc rather than derived from the rule, so
what is pinned varies by surface. `_REVIEW_LOOP` pins *"only the Maintainer may
concede"*; `_BOARD_TAXONOMY` and `_TEAM_GATED_MODULE` do not. Two mutations,
each run against the landed tree:

* **M2** — I cut `templates/core/dev/PLANNING.md`'s `accept` bullet back to the
  two sentences the patterns match, deleting the baseline, the grouped
  scope-remainder record and the Maintainer allowance. That paragraph is
  *precisely* the self-contained text `99451d2` says had to be written
  self-containedly "because that path dangles once installed." Result:
  **51 passed**.
* **M3** — I rewrote the team-gated module's `degraded`/`lost` sentence to read
  "**degraded** or **lost** are for the author and reviewer to settle between
  them." That is the authority contradiction R2-E1 spent a whole External round
  eliminating, landing on the adopter's installed body. Result: **51 passed**.

The test does bite where it is aimed — deleting the shipped `AGENTS.md` floor
paragraph (M4) turns 2 nodes red — and it is not vacuous: I applied all 46
parametrized patterns to the `6a4b3a0` bytes and **0 of 46** matched, so every
node is testing text this change added. The defect is coverage shape, not
construction.

*Satisfier*: **test** — give every surface that states the authority rule the
`only the Maintainer may concede` obligation, and every surface that states the
grouped record the `one grouped record` obligation. A shared base obligation set
with per-surface additions would make the asymmetry impossible to reintroduce.

**[C4 -- P2] The invariant "no transition refuses on anything new" has named
enforcers that do not enforce it.** The plan's author-accounting table lists the
invariant with the enforcers *"`bootstrap/tests/test_lifecycle_cli.py` unchanged
and green; `_conformance_violations` byte-unchanged"*, and
`test_the_planner_does_not_gate_on_a_missing_declaration` pins the absence by
inspecting `_conformance_violations` alone.

But `_conformance_violations` is not the only place the planner can refuse a
transition. `_gating_preconditions` (`tools/lifecycle_planner.py:1558`) is the
function that decides whether `next --to` reports a transition as structurally
`MISSING` and prints *"the tool does NOT present it as ready"* — the
author-visible form of the declined mechanism. **M7**: I added

```python
if art.kind == "proposal" and target == "revised":
    gates.append(("**Scope delta**" in art.text,
                  "declare the Scope delta before revising"))
```

to `_gating_preconditions` in both twins. `test_scope_reduction_trap.py`,
`test_lifecycle_cli.py` and `test_lifecycle_contract.py` together: **188
passed.** The declined gate can come back at the surface an author actually
reads, and the whole cited enforcer set stays green.

I checked the other two candidate homes before rating this. `scripts/
transition_lint.py` is not one — it declares itself *"advisory forever … nothing
here may be wired to a gate"* and never returns `1`. And I confirmed
`_conformance_violations` is byte-identical to `6a4b3a0` by AST function-hash,
so the fence is correct about the surface it does cover; it is the coverage that
is one surface short.

*Satisfier*: **test** — extend the fence node to `_gating_preconditions`
(assert no emitted gate description mentions the declaration), or **explicit
wontfix** recording that only the exit-code-bearing surface is pinned.

**[C5 -- P2] Boundary B is not reproducible.** The record's command column reads
*"mapped pytest set (25 modules, see Verification)"*, and the Verification
section says only *"every module in `bootstrap/tests` that references a surface
this plan touches (derived by grep, 25 modules)"*. Neither the grep nor the
module list is recorded. My own grep over the touched surfaces returns **48**
modules, so I cannot reconstruct the set that produced "916 passed, 1 failed" —
and `AGENTS.md` > Boundary B requires the *commands* in the record.

I want to be clear that I judge the **bounding decision itself sound**, and I
verified its premise rather than taking it: by AST function-hash against
`6a4b3a0`, the only function Chunk C changed in either twin is `_scaffold`, all
four hunks are string literals, and `_legal_transitions` — which *did* change in
the range — changed at `1c68926`, another agent's commit. The defect is the
record, not the judgement.

*Satisfier*: **doc** — record the exact command (a literal module list, or the
grep that generates it).

**[C6 -- P3] The full suite at the reviewed tip is 3 failed, not 1 — all three
pre-existing.** I ran the full suite twice, both in clean detached worktrees
under the canonical interpreter:

* at `4f17fef` — **3 failed, 3063 passed, 1 skipped**, 416 s;
* at `6a4b3a0` (the commit before the plan opened) — **3 failed, 2962 passed,
  1 skipped**, 402 s.

**The same three node ids at both.** Beyond the disclosed
`test_security_check.py::test_detached_checkout_excludes_an_ignored_pytest_override`:

* `test_verify_ref.py::test_mutation_verifying_inside_the_candidate_runs_the_forger`
* `test_verify_ref.py::test_candidate_gpg_ssh_program_never_executes`

So the *attribution* half of the bounding argument is vindicated, and I checked
it two ways rather than one: the paired full runs above, plus isolation —
`test_verify_ref.py` passes **67/67 alone** at `4f17fef`, `ab51587`, `be40b41`
and `6a4b3a0`, so these are suite-order/interaction failures, not new breakage.

I also confirmed the disclosed failure's characterisation is exact: it fails on
regenerated `bootstrap/tests/__pycache__/*.pyc` reported as `extra=[...]`, which
reproduced after I deleted the caches and let pytest recreate them. Environment
pollution, as recorded.

What is left is a record defect, not a verification defect: "916 passed, 1
failed" reads as a characterisation of the tree, and a mapped run cannot support
one. Two other failures were sitting outside the map the whole time.

*Satisfier*: **doc** — note the other two as pre-existing (they now have paired
full-run evidence), or cite this section.

**[C7 -- P3] Nothing pins any doctrine body — including the canonical home every
other surface points at.** `test_the_canonical_section_exists_and_sits_beside_its_mirror`
checks only that two `##` headings exist and are adjacent. **M1**: I replaced the
entire body of "Review expectations — the scope-reduction trap" with `TBD.` and
deleted the new sections in `doctrine/proposals.md`, `doctrine/plans.md` and
`doctrine/lifecycle.md`, keeping the headings. Result: **51 passed**.

The plan discloses the shape of this ("E1 covers absence, and it covers only the
surfaces it enumerates"), so it is not concealed. But the test module's own
comment above `_SURFACES` says *"Every path here is one an adopter receives,
except `doctrine/dual-review.md`, which is the canonical home the others point
at"* — and `doctrine/dual-review.md` is **not a key in `_SURFACES` at all**. A
reader of the test is told the canonical home is covered when it is not.

*Satisfier*: **doc** (correct the comment) or **test** (add the canonical
section's obligations, scoped to the section rather than the file).

**[C8 -- P3] The declaration ships with two different value sets.**
`doctrine/proposals.md` prints `**Scope delta**: preserved | degraded | lost`.
All four templates and both planner scaffolds print `**Scope delta**: degraded |
lost` and instruct the author to omit the block when preserved. Meanwhile the
accepted proposal's Round 6 closes with "**Scope delta: preserved.**", and this
plan's own Sequence revision writes "**Outcome test on this plan's own
verification: preserved.**" — so the three-value form is what the corpus
actually uses while the two-value form is what the tool hands the author.

The parity test cannot see this: its pattern is `\*\*Scope delta\*\*`, which
matches either.

*Satisfier*: **doc** — pick one grammar. (I have no view on which; both are
defensible and the choice is the Maintainer's.)

**[C9 -- P3] The plan template puts the floor rule everywhere except where E1's
failure happens.** `doctrine/plans.md` deliberately placed the new section
*"under the planning-handshake scope fence where the confusion lives"* — the
right call. The templates did not mirror it: the new text sits inside the
**plan-review comment block**, conditioned on *"when a Sharpening disposition
narrows"*. E1's canonical scenario — a plan carrying only A from an accepted
A+B+C — happens at **plan-open**, in the `## Scope` section where "what this
plan does *not* do" is authored, and that section gained no prompt.

An adopter is not left unbound: I verified the `open -> executing` scaffold path
emits the block too (not only `awaiting-plan-review -> executing`), and shipped
`AGENTS.md` carries the floor rule. So this is placement, not absence.

*Satisfier*: **doc** — one sentence in the plan template's scope-fence text, or
**explicit wontfix**.

**[C10 -- P3] The plan did not do its own declared housekeeping.** Line 2 still
carries `<!-- claim-check-allow: bootstrap/tests/test_scope_reduction_trap.py -->`
with the comment *"The line drops when the file lands."* The file landed at
`4f17fef`; the directive and its `Proposed paths:` block are still there at
`d330083`. I confirmed the directive is now genuinely stale — removing it
produces no flag for that path (it produces C2's flag, which is a different
problem).

*Satisfier*: **doc**.

**[C11 -- P3] `templates/modules/team-gated/dual-review.md` is scope the
Decision did not enumerate.** Part 9 lists `doctrine/plans.md`, both template
pairs, the planner scaffolds, the planner/transition-lint tests, Cairn's own
`agent_collaboration.md`, and both `AGENTS.md` copies. The team-gated module is
not on it. I judge the addition **correct on the merits** — `doctrine/` is not
installed, so without it the reconciled vocabulary would not reach an adopter at
all, which is E5's whole objective — and the plan declared it at open, in Chunk
B2, where the Maintainer could see it. Raising it only so the Maintainer
disposes of it deliberately rather than by silence; note also that it is the
edit that produced C1.

*Satisfier*: **explicit wontfix** (Maintainer confirms the addition), or
scope-cut.

### Two claims I checked and can confirm

* **The lockfile claim holds.** Part 9 said "the applicable lockfile
  finalization is part of the plan"; the plan declared none owed. Correct: the
  install *set* is unchanged, and Cairn's self-hosted `cairn-lock.yml` already
  carried **14** content-hash mismatches at `6a4b3a0` — including `AGENTS.md`,
  `dev/PLANNING.md`, `dev/modules/dual-review.md` and both `_template.md` files
  — because those entries are `verbatim: false` living files. Nothing gates
  them. One entry (`dev/agent_collaboration.md`) went from in-sync to out-of-sync
  here; with no enforcing check and 14 already adrift, that is an observation,
  not a finding.
* **The neutrality accounting is exact.** I reproduce `fail=93 info=21`, and the
  only failing token in any file this plan touched is `doctrine/dual-review.md:57`
  (`Claude`), which `git log -L` blames to `160cbb2`. The correction recorded
  against `99451d2`'s false `fail=0` is honest and complete, and self-reported —
  which is worth saying out loud.

### Verification

All under `/Users/kendal30/conda_envs/lhm/bin/python3.13`.

| Probe | Result |
|---|---|
| Full suite at `4f17fef`, clean detached worktree, `--quality-gate-shuffle-seed=0` | 3 failed, 3063 passed, 1 skipped, 416 s (C6) |
| Same full suite at `6a4b3a0`, second clean worktree | 3 failed, 2962 passed, 1 skipped, 402 s — **identical node ids** (C6) |
| `test_verify_ref.py` in isolation at `4f17fef`, `ab51587`, `be40b41`, `6a4b3a0` | 67 passed at each |
| Vacuity sweep: all 46 parametrized patterns vs `6a4b3a0` bytes | 0 of 46 matched — no vacuous node |
| M1 doctrine bodies gutted, headings kept | 51 passed (C7) |
| M2 shipped board loses baseline + grouped record + allowance | 51 passed (C3) |
| M3 team-gated module: author + reviewer may concede | 51 passed (C3) |
| M4 shipped `AGENTS.md` floor paragraph deleted | 2 failed, 49 passed — the test bites |
| M7 scope-delta gate added to `_gating_preconditions`, both twins | 188 passed across the plan's whole cited enforcer set (C4) |
| `_conformance_violations` AST function-hash, `6a4b3a0` vs `4f17fef` | identical; only `_scaffold` changed by `ccffb77` |
| Planner twins | byte-identical (`cmp`) |
| Scaffold coverage across 7 transitions | `**Scope delta**` + `DOES NOT CHECK` on exactly `proposal reviewed→revised`, `plan open→executing`, `plan awaiting-plan-review→executing`; absent elsewhere |
| `cairn:slot` placement | all five shipped files' markers are single-line insertion points; nearest precedes the new text by 100+ lines — no new text inside a slot |
| `scripts/check_cairn.py` | OK, 176 files, no issues |
| `scripts/quality_gate.py --sub neutrality --sub redundancy` | neutrality fail=93 info=21; redundancy fail=0 info=2 |
| `scripts/claim_check.py` on plan / archived proposal | 1 hard flag at `d330083` in a clean checkout / clean; main tree now clean after `ca22f21` (C2) |
| Shipped-surface `doctrine/` citations | covered by pre-existing file-scoped `cairn-internal-ref-allow` markers; no dangling-citation regression |

### Coverage

**Covered** — Part 9 enumeration against the landed diff, surface by surface
(all eleven present; C11 is the only addition); the declined planner gate as an
absence, at all three candidate homes (`_conformance_violations` byte-identical;
`_gating_preconditions` unpinned, C4; `transition_lint` structurally ineligible);
twin and slot parity (planner twins `cmp`-identical, slots verified as
single-line markers, and the one drifted pair found — C1); the new test's
construction (vacuity sweep, seven mutations); adopter reachability (shipped
surfaces carry the rule standalone; `check_cairn` clean; citation markers
pre-existing); internal consistency across the landed statements (C8, C9, and
the lens-9 mapping, which stays total — a scope reduction routes to `defer`,
"the Maintainer's call", consistent with "only the Maintainer may concede");
the verification record's every numeric claim (C2, C5, C6, plus the neutrality
and pre-existing-failure claims, both confirmed).

**Not covered / low confidence** —

* **This is an Internal read.** Same agent type as the author. The
  distribution's *judgement* calls — is `preserved`-owes-nothing the right
  default, is the grouped record the right shape — got two External rounds at
  the proposal and none here. I did not re-litigate them and could not have read
  them independently if I had.
* **I did not test the rule in use.** No probe here shows an author meeting the
  declaration and behaving differently. The proposal's own signals ("authors
  write the sentence as boilerplate") are only observable over a corpus, and
  nothing in this change measures them.
* **I did not audit the other agents' interleaved commits**, only excluded them.
  If `4f17fef` is not the commit that ultimately archives, C6's figures need
  re-taking at whatever tip does.
* **The two `test_verify_ref` failures are order-dependent and I did not find
  the polluting module.** I established non-attribution by isolation and by the
  shape of this plan's diff, not by root-causing the interaction. Someone owns
  that; it is not this plan.

## Lasting-truth migration

*Filled in at archive time.*

### Sharpening -- Claude -- 2026-08-11

**Model**: Claude Opus 5 (`claude-opus-5`)

**Verdict accepted. Every finding is real; none is rejected.** I verified C1
independently before acting on it rather than taking the report — the lockfile
pairing is at `dev/.cairn/cairn-lock.yml:133`, and the installed copy did still
carry the unrestricted mapping.

One correction to the review's own wording, which does not change the finding:
the two files were never *byte*-identical at `6a4b3a0` — the shipped copy
carries a `cairn-internal-ref-allow` header the installed one does not. The
**bodies** were identical, which is what the review actually measured and what
its line counts (103 each) describe. The drift is mine either way.

| # | Disposition |
|---|---|
| **C1** | **accept** — the block Chunk B added to the shipped module is now in `dev/modules/dual-review.md`; bodies identical again. |
| **C2** | **accept** — the Pre-run citation now uses parent-directory + bare filename, so the plan no longer depends on another agent's tree state. |
| **C3** | **accept (guard)** — `test_scope_reduction_trap.py`, authority-rule patterns on the board pair and the module pair. |
| **C4** | **accept (guard)** — the fence test now sweeps `_gating_preconditions` across every legal target as well as `_conformance_violations`. |
| **C5** | **accept** — the Verification section now carries the literal generating command instead of a description. |
| **C6** | **accept** — correction appended to the verification record. |
| **C7** | **accept (guard)** — four doctrine surfaces pinned by body, not by heading. |
| **C8** | **accept with modification** — see below. |
| **C9** | **accept** — the floor rule now also sits in both plan templates' `## Scope` fence text, where plan-open happens. |
| **C10** | **accept** — stale directive and `Proposed paths` block removed. |
| **C11** | **MAINTAINER** — see below. |

**C1 is the finding that matters, and it is the proposal's own thesis landing
on its author.** This change exists because an External review found the
teaching surfaces incomplete. I then shipped it with an incomplete teaching
surface, in Cairn's own tree, leaving the unsound `scope-cut -> accept` mapping
live in the copy Cairn itself reads. Two causes, both now closed: Chunk B's
acceptance grep was scoped to `doctrine/ templates/ dev/PLANNING.md`, which
structurally could not see `dev/modules/`; and the plan's twin-parity table
never listed the pair it went on to edit. `dev/modules/dual-review.md` is now a
test surface, so the drift is a red test rather than a lucky catch.

**C8 — accept with modification.** The review left the grammar choice to the
Maintainer. I made an author call instead of escalating, because both forms
were already *mine* and the inconsistency was an implementation slip rather
than a design question: doctrine printed three values, the templates printed
two. All six surfaces now print `preserved | degraded | lost`, with `preserved`
statable but not required. That matches Round 6 (preserved owes nothing) *and*
the corpus habit of writing it affirmatively. If the Maintainer prefers the
two-value form, it is a one-line change on six surfaces.

**C11 is the one thing I cannot dispose of.** `templates/modules/team-gated/dual-review.md`
— and now its installed twin — is scope the Decision did not enumerate. The
review judges the addition correct on the merits and I agree: `doctrine/` is not
installed, so without it the reconciled vocabulary reaches no adopter, which is
E5's whole objective. But agreeing is not authority. Under this plan's own rule
it is **added scope post-Decision**, which is a deviation needing the
Maintainer's explicit disposition — the same gate as removal, and the rule
would be worthless if its author could self-approve an expansion under it.

**Verification of this Sharpening.**

* Mapped set re-derived by the recorded command (28 modules, excluding another
  agent's untracked one) — **1014 passed, 1 failed**, 74.7 s. The one failure
  is `test_security_check.py::test_detached_checkout_excludes_an_ignored_pytest_override`,
  already homed on the board at `e150b7d`.
* **Perturbation, three mutations at once**: reverting the installed twin,
  cutting the shipped board's authority sentence, and adding a scope-delta gate
  to `_gating_preconditions` — **8 failed**, including 4 on
  `dev/modules/dual-review.md` where the old suite produced 0.
* **Vacuity sweep**: all **78** parity patterns run against `6a4b3a0` bytes —
  **0 matched**. No pattern passes on text that predates the change.
* Twins byte-identical; `check_cairn` OK (176 files); `claim_check` clean;
  neutrality `fail=93` / redundancy `fail=0`, both unchanged.

**Status stays `review`.** C11 is undisposed and the plan cannot archive with an
open Maintainer item.

## Lifecycle disposition ledger -- Claude -- 2026-08-11

Prepared at Sharpening; the archive block will carry it. Recorded here because
an archived plan is not re-read — each item's *home* is a live surface, and
this table records which one.

| Item | Disposition | Home |
|---|---|---|
| The detached-checkout guard counts `__pycache__` as unexpected content | `defer` (Maintainer-authorized, quoted verbatim in the row) | `dev/PLANNING.md` > Deferred follow-ups > Lifecycle apparatus, at `e150b7d` |
| Cairn stacks review tiers upward by default | `superseded` | `dev/plans/review-efficient-lifecycle.md` — the Maintainer-directed contract revision at `4db16d4`, binding via cell **G-R** (teach the default in canonical, self-hosted and shipped surfaces) and cell **P8-R** (test matrix) |
| The planner gate on the `Scope delta` declaration | `wontfix`, revival condition recorded | The accepted proposal's Round 3, and `test_the_planner_does_not_gate_on_a_missing_declaration`, which fails if the gate returns |

**A note on `superseded`.** It is not one of the archive-time tokens
(`accept` / `guard` / `wontfix` / `defer`), and none of the four fits an item
already owned by another *live* artifact: it is not non-action, not fixed in
this artifact's scope, and a roadmap row would be actively wrong. Doctrine
requires the record to justify the disposition rather than to pick from a
closed list, so the token is used with its home cited. Flagged rather than
forced into a token that would misdescribe it.

The `superseded` home is load-bearing only while that plan carries G-R. If it
narrows and drops it, that is a `lost` outcome against its accepted baseline —
owing a declaration and the Maintainer's allowance under the rule this plan
just landed. The protection is structural, not hopeful.

### Sharpening addendum -- C11 disposed -- 2026-08-11

**C11: accept (Maintainer-confirmed).** The team-gated `dual-review` module and
its installed twin stay.

Maintainer authorization, quoted verbatim:

> "We definitely don't want to ship any self-contradicting"

**What the disposition rests on**, since the framing changed between the review
and the decision. The module is **not** an independent doctrinal authority: its
header reads *"Adds to: the review section of `dev/agent_collaboration.md`"* and
its body opens *"Merged into `dev/agent_collaboration.md`"*. It is a transplant
whose canonical source is `doctrine/dual-review.md`, which Chunk A already
changed, and whose destination file Part 9 **does** name.

So the omission would not have produced a thinner distribution. It would have
produced an **incoherent** one: an adopter with `dual-review` installed would
receive a single `agent_collaboration.md` carrying the trap and the outcome test
from Chunk D4, while the lens roster merged into that same file still mapped
`scope-cut` → `accept` with no restriction. One file contradicting itself, which
is the specific defect Part 8 exists to remove.

**The reach does still extend beyond the enumeration**, and that is why it was
put to the Maintainer rather than self-approved. Part 8 named three homes for
the vocabulary reconciliation — `doctrine/dual-review.md`, the lifecycle
disposition text, and the board's inline taxonomy — and the module is a fourth.
An author who may widen scope under a rule about not narrowing it has defeated
the rule's own symmetry; the deviation gate governs both directions or neither.

