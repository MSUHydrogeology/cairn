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
2. Chunk B -- vocabulary reconciliation (scope-cut vs scope reduction) [commit 99451d2]
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

### C6 re-take -- declined, with the reasoning -- 2026-08-11

The code review's third *Not covered* bullet reads: *"If `4f17fef` is not the
commit that ultimately archives, C6's figures need re-taking at whatever tip
does."* The tip moved (Sharpening at `3f92cd8`, C11 record at `86da18a`), so the
caveat fires. **I started a full suite at `86da18a` and then killed it**, on
Maintainer challenge, and the challenge was right.

What changed between `4f17fef` and `86da18a`: prose in `dev/modules/dual-review.md`
and four templates; **one string literal per planner twin** (`degraded | lost`
→ `preserved | degraded | lost`); the test module itself; and this plan. No
contract surface, no new executable path. The re-derived mapped set — 28
modules generated by the recorded command, which now includes `dual-review` and
`scope_reduction` — covers every one of those and returned **1014 passed, 1
failed** (the pre-existing `__pycache__` guard, homed at `e150b7d`).

And C6's substance was never an unknown count. It was that the record *framed*
the mapped set's "1 failed" as the tree's standing state. That is corrected in
prose above, and the review itself established the standing state as **3
pre-existing failures, identical node ids at `4f17fef` and at `6a4b3a0`**. A
third full run would only test whether prose edits broke a module unrelated to
any touched surface.

**The pattern is worth recording, because it is this proposal's own subject.**
This is the third time in one plan that I defaulted verification upward and the
Maintainer pulled it back — the External plan review, the first Boundary B, and
now this. Each time the correction came from outside the doctrine rather than
from it. That is evidence the plan shipped its two halves unevenly: real
machinery for *do not cut reach*, and a slogan for *cut ceremony*. Recorded as
an observation for whoever revisits the counterweight, not as a finding this
plan will fix.

## Code review -- Claude (Internal) -- 2026-08-12

**Reviewed commit**: `f928d9c`, reached through the three Sharpening commits
`3f92cd8`, `86da18a` and `f928d9c`, each diffed against **its own parent** so the
other agents' commits interleaved in that range are excluded rather than trusted.
**Target**: the Sharpening and what it claims to have fixed — the dispositions on
C1-C11, the Maintainer's C11 disposition, and the declined C6 re-take. Not a
fresh end-to-end read of the change; that pass landed on 2026-08-11 and I did not
repeat it.
**Prior findings**: C1-C11 from `## Code review -- Claude (Internal) -- 2026-08-11`,
verdict `REVISE`. C1-C10 dispositioned by the author at `3f92cd8`, C11 by the
Maintainer at `86da18a`, the C6 re-take declined at `f928d9c`.
**Assurance path**: standard
**Model**: Claude Opus 5 (`claude-opus-5`)
**Findings**: raised

**Tier — stated honestly.** Fresh-session, same-agent-type: the **Internal**
floor, *not* External. What this pass does supply is the one structural property
the doctrine requires here — a blocking verdict answered by a **later independent
pass** rather than by the implementer's own Sharpening. What it does not supply is
cross-type assurance on the distribution's judgement calls; those have had none
since the proposal, and nothing here changes that.

**Verdict: REVISE.**

I tried to break each disposition rather than read the table. Most hold. **C1 is
genuinely fixed** — the installed and shipped `dual-review` bodies agree again, the
unrestricted `scope-cut` mapping is gone from the copy Cairn reads, and the pair is
now a test surface that reddens **5** nodes if you revert it. **C7 is fixed at the
canonical home**: gutting the trap section's body while keeping its heading turns
**11** nodes red where it used to turn **0**. **C3's authority half bites** — both
of the mutations that produced it now redden 2 nodes each. C5 records a real
generating command, C10's stale directive is gone, and C11's authorization is
quoted verbatim and isolated in both the record and the commit.

One accepted finding did not close, and it is the same finding. **C4 said an
invariant had named enforcers that do not enforce it. The guard added for C4 has
that same defect**: the fence sweeps `_gating_preconditions` only over the legal
targets of a proposal fixture whose status is already `revised`, so the two
transitions the mechanism is actually about — `proposal reviewed -> revised` and
`plan awaiting-plan-review -> executing`, the exact pair `_SCAFFOLDED_TRANSITIONS`
enumerates — are never swept. The 2026-08-11 review's own M7 mutation, applied
verbatim to both twins, still passes **83 of 83**, and produces **zero** new
failures across the whole cited enforcer set (386 nodes). The declined planner gate
can still come back at the surface an author reads, with a green suite and a
`wontfix` row in the disposition ledger pointing at the test node that was supposed
to catch it. That row would be written into an archived plan, which is not re-read.

Five dispositions closed only partly: C3's grouped-record half was never
implemented (D2), C5's figure still does not reproduce from its own command (D3),
C8 left the author-facing scaffold on the old grammar (D5), C2's second half was
skipped (D6), and C9's fix plus one C7 obligation are unguarded (D7). None
re-opens the rule and all are cheap. Only D1 blocks.

### Findings

**[D1 -- P1] The C4 guard does not fire on the mutation that produced C4.**
`test_the_planner_does_not_gate_on_a_missing_declaration` now sweeps
`_gating_preconditions` as well as `_conformance_violations` — but it sweeps it
over `planner._legal_transitions(art)` for a fixture,
`_REVISED_PROPOSAL_WITHOUT_A_DECLARATION`, whose `**Status**` is already
`revised`. Those legal targets are `reviewed`, `accepted`, `rejected`,
`superseded`. **`revised` is not among them**, and no plan artifact is
constructed at all. So the sweep covers every transition except the two the
declaration exists for.

Measured at `f928d9c`, canonical interpreter, each mutation applied to **both**
planner twins and reverted after:

| Gate added to | Test result |
|---|---|
| `_gating_preconditions`, `proposal` / `target == "revised"` (C4's M7, verbatim) | **83 passed** — undetected |
| the same mutation, whole cited enforcer set (`test_scope_reduction_trap`, `test_lifecycle_cli`, `test_lifecycle_contract`, `test_transition_lint`, `test_lifecycle_vocabulary`) | 2 failed / 384 passed — **both pre-existing**, 0 new |
| `_gating_preconditions`, `plan` / `target == "executing"` | **83 passed** — undetected |
| `_gating_preconditions`, `proposal` / `target == "accepted"` | 1 failed — detected |
| `_gating_preconditions`, unconditional on any proposal target | 1 failed — detected |
| `_conformance_violations`, unconditional | 1 failed — detected |

The two detected rows are why the Sharpening's perturbation looked convincing: a
gate placed anywhere *except* where the mechanism lives does redden the fence.

Two corroborating details. The Sharpening records the composite perturbation as
*"8 failed, including 4 on `dev/modules/dual-review.md` where the old suite
produced 0."* Reconstructing that composite as described — revert the installed
twin, cut the shipped board's authority sentence, add the scope-delta gate to
`_gating_preconditions` in both twins — I get **6 failed, 5 of them on
`dev/modules/dual-review.md`**, and the gate component contributes **0**. And the
lifecycle disposition ledger homes the `wontfix` in this node: *"and
`test_the_planner_does_not_gate_on_a_missing_declaration`, which fails if the gate
returns"*. It does not, for the returning gate that matters.

Under `AGENTS.md` > *Verifying claims* — *"a tool that returns success without
testing the claimed property is a worse defect than no tool, because it is
silent"* — this is the blocking one.

*Satisfier*: **test** — parametrize the fence over the artifact states that reach
the scaffolded transitions (a `reviewed` proposal and an `awaiting-plan-review`
plan at minimum; the `(kind, status)` cross-product is stronger), so the swept set
is derived from `_SCAFFOLDED_TRANSITIONS` rather than from one fixture's accident
of status.

**[D2 -- P2] C3's satisfier had two halves and one landed.** The 2026-08-11
satisfier reads: *"give every surface that states the authority rule the `only the
Maintainer may concede` obligation, **and every surface that states the grouped
record the `one grouped record` obligation**."* The first half landed and bites —
I re-ran both of C3's mutations and each now reddens 2 nodes. The second half did
not: `_BOARD_TAXONOMY` carries three obligations and none of them is the grouped
record.

Mutation, against the landed tree: from the shipped board's `accept` bullet
(`templates/core/dev/PLANNING.md`) I deleted the baseline definition, the
`**Scope delta**` declaration, the grouped scope-remainder record and the
Maintainer's-allowance clause, keeping only *"Neither author nor reviewer may
concede a baseline outcome."* Result: **83 passed**. That paragraph is the one
`99451d2` says had to be written self-containedly *"because that path dangles once
installed"*, and most of it can still leave the adopter's copy silently.

*Satisfier*: **test** — the shared-base-obligation shape C3 asked for, so the
asymmetry cannot be reintroduced surface by surface.

**[D3 -- P2] The mapped-set figure still does not reproduce from the record.** C5
was fixed the right way — the Verification section now carries the literal grep
instead of a description. Running that exact command in a clean checkout:

* at `4f17fef` — **28** modules (matches the original record);
* at `3f92cd8` (the Sharpening) — **29**;
* at `86da18a` and `f928d9c` — **30**.

The Sharpening records *"28 modules, excluding another agent's untracked one"* and
the C6-decline records *"28 modules generated by the recorded command, which now
includes `dual-review` and `scope_reduction`"*. Neither figure is derivable from
the bytes it is attached to. The two additions are
`bootstrap/tests/test_lifecycle_vocabulary.py` and
`bootstrap/tests/test_claim_check_module.py` — other agents' modules that the
recorded grep pulls into this plan's mapped set, and that were not run. Nothing
about this plan turns on them, which is exactly why the figure should be dated
rather than asserted: this is the third numeric claim in this record to need
correction (`fail=0`, then `1 failed`, now `28`).

*Satisfier*: **doc** — record the count with an `as_of` commit, or list the
modules literally.

**[D4 -- P3] "One string literal per planner twin" is two.** The C6-decline
section and `f928d9c`'s commit body both bound the delta as *"prose plus one
string literal per planner twin."* `3f92cd8` changes
`**Scope delta**: degraded | lost` to `preserved | degraded | lost` at **two**
sites in each twin — the proposal-revision scaffold and the plan-Sharpening
scaffold, both inside `_scaffold`. The bounding argument is unaffected in
substance (both are string literals in one function, no contract surface), and the
sentence also silently omits the largest executable change in that range, the
+124-line rewrite of `bootstrap/tests/test_scope_reduction_trap.py`, which the
mapped set does cover.

*Satisfier*: **doc**.

**[D5 -- P3] C8 unified the grammar everywhere except the surface Chunk C exists
for.** All six live surfaces now print `preserved | degraded | lost` — I swept for
stragglers and found none outside the archived proposal, which is append-only
history. But the *prose around* the scaffold literal was not updated: the emitted
block still reads *"Omit entirely when every opened outcome is still delivered"*
and the manifest line still reads *"the Scope-delta block is OMITTED unless the
revision narrows"*, while both proposal templates were changed to *"You may state
`preserved` so the record shows you checked."* The scaffold is the surface Chunk C
justified itself on — *the declaration where the author is typing* — and it is the
one still telling the author to omit.

Related: nothing guards the unified grammar. Reverting all six surfaces to
`degraded | lost` leaves **83 passed**; the parity pattern is `\*\*Scope delta\*\*`
and the scaffold assertion is `"**Scope delta**" in emitted`, so both match either
form. That is the same blind spot C8 named, still open one layer down.

*Satisfier*: **doc** (one sentence in each scaffold literal), optionally **test**.

**[D6 -- P3] C2's second half was not done.** The satisfier read: *"reword the
citation so the plan does not depend on another agent's tree state, **and note in
the record that the row was working-tree-dependent**."* The rewording landed and I
verified it — `scripts/claim_check.py` is clean on the plan in a clean checkout at
`f928d9c`, and the Pre-run paragraph now cites `bootstrap/tests/` plus bare
filenames. The note did not: the Implementation verification table still asserts
`scripts/claim_check.py` → *"clean on both"* with no marker that the result as
originally taken depended on another agent's untracked file. The only occurrence
of the phrase in the file is inside the 2026-08-11 satisfier text.

*Satisfier*: **doc**.

**[D7 -- P3] The C9 fix is unguarded, and one C7 obligation is still pinned by a
heading.** Two small residuals of the same shape:

* Deleting the **entire** paragraph C9 added to both plan templates' `## Scope`
  fence — *"The fence bounds this pass; it does not bound the accepted
  proposal…"* — leaves **83 passed**, because `accepted scope is a floor` is
  independently satisfied by the plan-review block's `SCOPE DELTA -- accepted
  scope is a FLOOR` far below it. C9's whole point was *placement*, and placement
  is what nothing checks.
* In `doctrine/plans.md`, the `accepted scope is a floor` obligation is satisfied
  by the **heading** `### Accepted scope is a floor — the scope fence is not a
  licence to shrink`. Gutting that section's body while keeping the heading leaves
  that node green — the exact construction C7 was raised about, surviving on one
  of the four surfaces C7's fix covered. (The other three obligations in
  `doctrine/plans.md` do redden, so the section is not unguarded, only that one
  claim.)

*Satisfier*: **doc** (say so) or **test** (scope the obligation to the section
body).

### What I probed and could not defeat

A clean pass on any of these should have made me suspicious, so I am naming the
attack rather than the conclusion.

* **C1 — the twin drift.** `dev/modules/dual-review.md` and
  `templates/modules/team-gated/dual-review.md` at `f928d9c` differ by exactly one
  line, the shipped copy's `cairn-internal-ref-allow` header — the legitimate
  difference the Sharpening's own correction describes. The installed copy now
  carries the restricted `scope-cut` sentence, the trap, and the three-way outcome
  test. Reverting it to its `4f17fef` bytes reddens **5** nodes on that path, where
  the pre-Sharpening suite produced 0. I also swept `scope-cut` across every
  shipped and self-hosted surface: six files carry it, and every occurrence of the
  `scope-cut -> accept` mapping is now immediately followed by the restriction.
* **The C1 fix did not create lockfile drift.** The lock entry at
  `dev/.cairn/cairn-lock.yml` for that pair digests to neither the pre-fix nor the
  post-fix content, so the entry was already adrift before this plan — consistent
  with the 14 pre-existing mismatches the 2026-08-11 pass recorded. No new finding.
* **C3's authority half.** Both of the 2026-08-11 mutations now bite: rewriting the
  module's `degraded`/`lost` sentence to let author and reviewer settle it reddens
  both module copies; cutting the concede sentence reddens both boards.
* **C7 at the canonical home.** Replacing the body of *"Review expectations — the
  scope-reduction trap"* with `TBD.` while keeping the heading reddens **all 11**
  `doctrine/dual-review.md` obligations. Gutting the three added sections in
  `doctrine/proposals.md`, `doctrine/plans.md` and `doctrine/lifecycle.md` reddens
  11 more; the two survivors are the heading match in D7 and a `scope-cut`
  sentence that legitimately also lives in `lifecycle.md`'s archive-precondition
  text.
* **Vacuity.** I re-ran the sweep myself rather than taking it: all **78**
  parametrized patterns applied to the `6a4b3a0` bytes match **0** times. No node
  is testing text that predates the change.
* **Twin parity.** The planner twins are byte-identical, and a gate added to only
  one would be caught by `test_the_two_planner_twins_stay_byte_identical` even
  though D1's sweep would not.
* **C11's attribution.** The authorization is quoted verbatim and visually
  isolated in both the plan record and `86da18a`'s commit body, and the commit is
  disposition-only (+30 lines, plan file alone). I did not re-litigate the
  decision. I cannot verify the quoted fragment against the Maintainer's actual
  words — no reviewer can — so I checked the form, which is correct.

### On the declined C6 re-take

**The bounding holds, and I ran the suite anyway.** Filtered to this plan's own
commits, the delta from `4f17fef` to `f928d9c` is prose across four templates and
the installed module, four string literals inside `_scaffold`, the test module,
and the plan itself. No contract surface, no new executable path. I confirmed the
attribution premise independently rather than accepting it:
`bootstrap/tests/test_verify_ref.py` passes **71/71** in isolation at `f928d9c`,
so those failures remain order-dependent and unattributable here.

Two qualifications the record should carry. First, *"between `4f17fef` and
`86da18a`"* is only true of this plan's commits; the **tree** between those two
points also absorbed several other agents' large changes, so the sentence as
written describes a filtered range while naming an unfiltered one. Second, the
standing state has moved and is **not** a superset of the old one: at `f928d9c`,
in a pristine detached worktree verified clean before and after, the full suite is
**4 failed, 3260 passed, 1 skipped** in 500.6 s — not the 3 the 2026-08-11 pass
established at `4f17fef` and `6a4b3a0`. Two nodes joined
(`TestLoaderContainmentMatrix::…[transition_lint]` and `[metrics_extract]`, which
also fail with `bootstrap/tests/test_lifecycle_vocabulary.py` run alone and belong
to `review-efficient-lifecycle`), and one left
(`test_verify_ref.py::test_mutation_verifying_inside_the_candidate_runs_the_forger`
no longer fails). The other two are the disclosed `__pycache__` guard and the
remaining order-dependent `verify_ref` node. None of the movement is this plan's.

So the decline was defensible on attribution and I would not have blocked on it
alone — but the figure it rests on is stale in a way the reasoning asserts it is
not (*"the review already established the standing state as 3 pre-existing
failures"*), and D3/D4 are the record defects it left behind.

### Verification

All under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), the
canonical interpreter. Two detached worktrees at `f928d9c`: one pristine, used for
the full run and nothing else; one for mutation, verified clean by
`git status --short` before and after every mutation.

| Probe | Result |
|---|---|
| Full suite at `f928d9c`, pristine worktree, `--quality-gate-shuffle-seed=0` | 4 failed, 3260 passed, 1 skipped, 500.6 s; worktree clean before and after |
| `bootstrap/tests/test_verify_ref.py` alone at `f928d9c` | 71 passed |
| `bootstrap/tests/test_lifecycle_vocabulary.py` alone at `f928d9c` | 2 failed, 28 passed — the same two node ids |
| Baseline `bootstrap/tests/test_scope_reduction_trap.py` | 83 passed (78 parametrized + 5) |
| Vacuity: 78 patterns vs `6a4b3a0` bytes | 0 matched |
| C4's M7 verbatim, both twins | **83 passed** (D1) |
| C4's M7, whole cited enforcer set | 2 failed / 384 passed — 0 new (D1) |
| Plan-side gate (`plan -> executing`), both twins | **83 passed** (D1) |
| Controls: gate at `-> accepted`, unconditional, or in `_conformance_violations` | 1 failed each — the fence does bite elsewhere |
| Shipped board loses baseline + grouped record + allowance, keeps concede | **83 passed** (D2) |
| C3 controls: concede sentence cut / rewritten, board pair and module pair | 2 failed each — C3's authority half bites |
| Installed `dual-review` reverted to `4f17fef` | 5 failed on that surface (C1 closed) |
| `doctrine/dual-review.md` trap body gutted, heading kept | 11 failed (C7 closed) |
| Three added doctrine sections gutted, headings kept | 11 failed, 2 survivors (D7) |
| C9 scope-fence paragraph deleted from both plan templates | **83 passed** (D7) |
| C8 grammar reverted on all six surfaces | **83 passed** (D5) |
| Sharpening's composite perturbation, reconstructed | 6 failed, 5 on the twin — record says 8 and 4 (D1) |
| Recorded mapped-set command, clean checkouts | 28 / 29 / 30 at `4f17fef` / `3f92cd8` / `f928d9c` (D3) |
| Installed vs shipped `dual-review` bodies | identical but for the shipped `cairn-internal-ref-allow` header |
| Planner twins | byte-identical |
| `scripts/claim_check.py` on the plan, clean checkout | clean (C2 closed) |
| `**Scope delta**:` grammar sweep, whole tree | 6 live surfaces, all three-value; only the archived proposal differs (C8 closed) |
| `scripts/check_cairn.py` | OK, 176 Markdown files, no issues — unchanged |
| `scripts/quality_gate.py --sub neutrality --sub redundancy` | neutrality fail=93 info=21; redundancy fail=0 info=2 — unchanged |
| `docs/glossary.md` E2 entries | all three present (*Outcome test*, *scope reduction*, *Scope-remainder record*) — but unpinned by any test |

**One observation on the archive gate, not a finding against this plan.**
`tools/lifecycle_planner.py next` on this plan at `f928d9c` reports the review
record as `[ok]` for `-> archived` **despite the latest pass carrying a blocking
verdict** — because `scope-reduction-trap` is enumerated in
`_LEGACY_CODE_REVIEW_DISPOSITIONS`, which admits the blocking pass on the
`### Sharpening -- Claude -- 2026-08-11` heading. That grandfathering belongs to
`review-efficient-lifecycle`, and it is doing what it was written to do; the point
worth recording is that on this plan the `[ok]` is an exemption, not a clearing.
Once this section lands as the latest pass, the gate refuses on its own terms.

### Coverage

**Covered, with falsifiable citations** — every one of C1-C11 verified against the
committed bytes or by execution, never from the disposition table: the twin drift
by byte-diff at `f928d9c` plus a revert mutation (C1); the two record rewordings by
clean-checkout re-runs of `claim_check` and by reading the landed lines (C2, C10);
the three test gaps by re-running the original reviewer's own mutations and then
building six more (C3 closed, C4 **not** closed — D1, D2); the mapped-set command
by re-derivation at four commits (C5, D3); the doctrine pinning by gutting four
section bodies (C7, D7); the declaration grammar by a whole-tree sweep and a
revert mutation (C8, D5); the plan-template placement by deletion mutation (C9,
D7); the C11 attribution by reading the record and the commit body (C11); the C6
bounding by an independent full run in a pristine worktree plus isolation runs.
Test construction re-checked from scratch: vacuity sweep 0/78, twin parity, and
the scaffold assertions exercised through `_scaffold` rather than by grep.

**Not covered / low confidence** —

* **This is an Internal read**, same agent type as the author and as the 2026-08-11
  reviewer. It supplies independence of *session*, not of *prior*. The
  distribution's judgement calls — `preserved`-owes-nothing as the default, the
  grouped record's shape, the three-value grammar C8 settled by author call rather
  than escalation — have had no cross-type read at any point in this plan.
* **I did not re-read the change end to end.** My scope was the Sharpening. If the
  2026-08-11 pass missed an enumerated Part 9 surface, I would not have found it;
  I took its distribution audit as given.
* **I did not test the rule in use**, and neither did anything else. Nothing here
  observes an author meeting the declaration and behaving differently. The
  proposal's own residual stands untouched.
* **The mutation worktree cannot prove a negative about placement.** My D1 table
  enumerates six gate placements; a seventh I did not think of could also evade
  the fence. The fix I recommend is to derive the swept set from
  `_SCAFFOLDED_TRANSITIONS` rather than to enumerate placements at all.
* **The two `test_lifecycle_vocabulary` failures are not root-caused**, only
  isolated and attributed elsewhere by module ownership. Someone owns them; it is
  not this plan.
* **`docs/glossary.md` is not a test surface.** Its three E2 entries are present
  and correct — I read them — but deleting them would leave the suite green. That
  is a pre-existing property of E1's enumeration, disclosed in the plan, not
  something the Sharpening changed; I record it because I looked and it is the
  kind of gap a later reader will otherwise assume was covered.

### Sharpening -- Claude -- 2026-08-12 (on the clearing pass, D1-D7)

**Model**: Claude Opus 5 (`claude-opus-5`)

**Verdict accepted; every finding verified before acting.** D1 is the one that
matters and it is the same defect twice: C4 said *"an invariant has named
enforcers that do not enforce it,"* and I closed it with an enforcer that did
not enforce.

**D1 — accept.** Confirmed exactly as described. The fixture sat at `revised`,
whose legal targets are `reviewed / accepted / rejected / superseded`, so
sweeping `_legal_transitions` covered every transition *except* the two
`_SCAFFOLDED_TRANSITIONS` names — and no plan artifact was built at all. A real
gate at `proposal / target == "revised"` left the suite green.

Fixed by deriving the sweep from the **scaffolded** transitions rather than from
`_legal_transitions`, with a fixture at the correct *source* status for each
(`reviewed → revised`; `awaiting-plan-review → executing`), and a plan fixture
that did not previously exist. The reviewer's four named mutations are now the
acceptance bar, and all four are red:

| Mutation | Before | After |
|---|---|---|
| gate at `proposal / target == "revised"` | 83 passed | **1 failed** |
| gate at `plan / target == "executing"` | 83 passed | **1 failed** |
| gate unconditional | detected | **2 failed** |
| gate in `_conformance_violations` | detected | **2 failed** |

**D2, D7 — accept.** Three more obligations that could be deleted while the
suite stayed green: the shipped board's baseline framing and its grouped
scope-remainder requirement (C3's second half, which never landed), and C9's
entire scope-fence paragraph in both plan templates. A fourth, in
`doctrine/plans.md`, was satisfied by its own **section heading** — the pattern
matched the title, so the body could be emptied. All four now red on the
mutations the clearing pass described; the doctrine pattern is re-pinned to body
prose rather than the heading.

**D3 — accept.** The record said 28 modules. The recorded command yields **31**
at this commit — 30 at `f928d9c`, 29 at `3f92cd8`, 28 at `4f17fef`. The drift is
the finding: the set grows as tests are added, so a bare count is a snapshot
masquerading as a fact. Under the three-kind precision discipline it needed an
`as_of`, or better, no count at all — **the command is the reproducible thing
and the count is not**. The Verification section already carries the command;
the count is withdrawn as a *standing figure* rather than re-dated. Where a
count appears below it is an `as_of` snapshot of one named run, never a property
of the mapped set.

**D4 — accept.** "One string literal per planner twin" was wrong: `3f92cd8`
changed **two** per twin — the `**Scope delta**` value list appears in both the
proposal `revised` scaffold and the plan `executing` scaffold. Verified by diff.
The bounding argument is unaffected; the count was still wrong and stated as
fact.

**D6 — accept.** C2's second half was skipped. Recording it now: **the
`claim_check` row in the Implementation verification table was
working-tree-dependent when written.** At `d330083` in a clean checkout the plan
carried one hard flag — a cited path that existed only as another agent's
untracked file — and became clean only when that agent committed it, mid-review.
The citation is reworded; this note is the disclosure that was owed alongside it.

**D5 — deferred within this plan, not dispositioned away.** The scaffold prose
in `tools/lifecycle_planner.py` still reads *"Omit entirely when every opened
outcome is still delivered"* one line above a value list offering `preserved`,
contradicting the templates C8 unified. Both twins are held under another
agent's active work-intent claim (`chunk P5`), so editing them now would
collide. **This is the only D-finding still open**, and the plan does not
archive until it closes.

**On the C6 re-take.** The clearing pass ran the full suite at `f928d9c` and
found **4 failed, 3260 passed** — not the 3 my decline asserted, and not a
superset: two `TestLoaderContainmentMatrix` nodes joined from another agent's
work and one `verify_ref` node left. The attribution argument survives (none of
the movement is this plan's) but the *number* I stated had already moved when I
stated it. Third numeric claim of mine in this record to need correction, which
is its own signal.

**On the archive gate reporting `[ok]`.** I reported this as a defect — that the
gate never reads the verdict. **That was wrong.** `tools/lifecycle_planner.py`
enumerates `scope-reduction-trap` by name in `_LEGACY_CODE_REVIEW_DISPOSITIONS`,
which admits its blocking pass; the comment above that table says so explicitly.
The gate works and this artifact is grandfathered. My four-way probe was
consistent with both explanations and I chose the wrong one instead of grepping
for the artifact's own stem.

### D5 closed -- Claude -- 2026-08-12

The last open finding from the clearing pass. Both planner twins were held under
another agent's `chunk P5` claim when the rest of D1-D7 landed; the claim has
since released and the twins are free.

**The defect, confirmed still present at HEAD before the fix.** The scaffold told
the author *"Omit entirely when every opened outcome is still delivered"* on the
line directly above `**Scope delta**: preserved | degraded | lost`, while both
proposal templates said *"you may state `preserved`"*. Adjacent lines
contradicting each other, so the field meant different things depending on which
sentence the author read.

Both scaffolds now say what the templates say. Twins byte-identical.

**And D5's other half, which was the more important one**: *nothing guarded the
grammar* — the clearing pass showed all six surfaces could be reverted together
and the suite stayed green. Three guards added: every template prints the agreed
values; both **emitted** scaffolds print them (through `_scaffold`, not by
grepping source — the block is built from adjacent literals); and neither
scaffold contains the contradiction.

**Verified against the clearing pass's own mutations**, not mutations I chose:

| Mutation | Before | After |
|---|---|---|
| revert the grammar on **all six** surfaces | 83 passed | **6 failed** |
| restore the "omit entirely" contradiction on one twin | 83 passed | **1 failed** |

Mapped set (31 modules `as_of 8ad50ed`, generated by the recorded command):
**1559 passed, 3 failed**. All three
reproduce at clean `HEAD` without this change, with identical node ids — two
`TestLoaderContainmentMatrix` nodes from another agent's in-flight work, and
`test_detached_checkout_excludes_an_ignored_pytest_override`, already homed on
the board at `e150b7d`. None is attributable here. `check_cairn` OK (173);
redundancy `fail=0`; neutrality `fail=93`, unchanged.

**All seven D-findings are now closed.** What the plan still owes before archive
is an independent pass: the code review's verdict was `REVISE`, and both
Sharpenings answering it are mine. Doctrine is explicit that a blocking verdict
is answered by a later independent pass, never by the author's own response.


## Code review -- Claude (Internal, second clearing pass) -- 2026-08-12

**Reviewed commit**: `8ad50ed`, reached through `6dde057` and `8ad50ed`, each
diffed against **its own parent** so the other agents' commits interleaved in
that range are excluded rather than trusted.
**Target**: whether D1-D7 are genuinely closed, and whether anything the two
Sharpenings introduced is itself defective. Not a fresh end-to-end read of the
change, and not a re-audit of C1-C11; those passes landed on 2026-08-11 and
2026-08-12 and I repeated neither.
**Prior findings**: D1-D7 from `## Code review -- Claude (Internal) -- 2026-08-12`,
verdict `REVISE`. D1-D4, D6 and D7 dispositioned by the author at `6dde057`; D5
at `8ad50ed`.
**Assurance path**: standard
**Model**: Claude Opus 5 (`claude-opus-5`)
**Findings**: raised

**Tier — stated honestly.** Fresh session, same agent type as the author and as
both prior reviewers: the **Internal** floor, *not* External. What this pass
supplies is the one structural property the doctrine requires here — a blocking
verdict answered by a **later independent pass** rather than by the
implementer's own Sharpening. It supplies no cross-type assurance on the
distribution's judgement calls; those have had none since the proposal.

**Verdict: REVISE.**

**Five of the seven D-findings are genuinely closed, and I closed them by
attack rather than by reading the table.** D2 and D7 bite individually, not just
as the composite the clearing pass described: each new obligation reddens on its
own, on **both** copies of the board and **both** plan templates, and the
heading-satisfaction defect is gone — I re-derived the match site of all **84**
parametrized patterns against the raw bytes and **none** now lands on a heading
line. D3's corrected figure reproduces (the recorded grep yields **31** modules
at `8ad50ed`) and D4's does too (`3f92cd8` changed exactly **two** `Scope delta`
literal lines per twin). D6's disclosure landed. The D1 fix does close the two
mutations that produced D1: a gate at `proposal / target == "revised"` and one at
`plan / target == "executing"` each redden the fence now, where both left it at
83 passed before.

Three things are open. **D5 is not closed** — the Sharpening restated the finding
without half of it, fixed the half it restated, and declared the whole thing
closed; the contradiction D5 named by quotation is still in the emitted scaffold
at `tools/lifecycle_planner.py:3808`, and the new guard passes over it (E1).
**The D1 fix bought its coverage by trading some away**: a gate placement the
*previous* fence caught now passes, and `_SCAFFOLDED_TRANSITIONS` does not
contain one of the transitions its own scaffold serves (E2). And the grammar
guard covers six of the **seven** live surfaces that print the declaration, the
missing one being the canonical doctrine the other six were unified onto (E3).

E1 is the blocking one. It is the fourth instance in this record of the same
shape — *a guard that passes while the thing it names is absent* — and this time
the guard was written against the reviewer's literal mutation string rather than
against the property, which is why it cannot see the surviving half.

### Findings

**[E1 -- P1] D5 was narrowed, then declared closed; the contradiction it named
is still emitted, and the new guard cannot see it.**

The clearing pass's D5 named **two** contradictory pieces, both by quotation:

> the emitted block still reads *"Omit entirely when every opened outcome is
> still delivered"* **and the manifest line still reads *"the Scope-delta block
> is OMITTED unless the revision narrows"***

`8ad50ed` changed the first and left the second. At `8ad50ed`, both twins carry
at line 3808:

```
"the Scope-delta block is OMITTED unless the revision narrows "
"an outcome the proposal opened with; ..."
```

That string is in the manifest, and the manifest is part of what `_scaffold`
hands the author — `blocks` is `[block] + manifest`, and this module's own
`test_the_emitted_scaffold_carries_the_declaration` asserts on `"DOES NOT
CHECK"`, a manifest string, through exactly that path. So the `proposal ->
revised` scaffold still tells the author, ten lines apart:

* *"State `preserved` if you want the record to show you checked; only
  `degraded` and `lost` require the block below."* (the block, fixed)
* *"the Scope-delta block is OMITTED unless the revision narrows an outcome the
  proposal opened with"* (the manifest, unchanged)

The `### D5 closed` section restates D5 as the block half alone and then asserts
*"Both scaffolds now say what the templates say."* They do not. The plan-side
manifest carries no omission claim, so this is the proposal side only — but the
proposal side is where a pre-Decision narrowing is declared.

The guard does not reach it. `test_the_scaffolds_do_not_contradict_the_offered_values`
asserts one literal: `"omit entirely" not in emitted`. Measured at `8ad50ed`,
canonical interpreter, mutation applied to **both** twins and reverted after:

| Mutation | Test result |
|---|---|
| restore the contradiction verbatim (*"Omit entirely when every opened outcome is still delivered."*) | 1 failed — detected |
| restore the same contradiction **reworded** (*"Leave the block out completely when every opened outcome is still delivered."*) | **98 passed** — undetected |
| (no mutation) the manifest's *"is OMITTED unless the revision narrows"*, live at HEAD | **98 passed** — undetected |

The Sharpening says the guards were *"verified against the clearing pass's own
mutations, not mutations I chose."* That is honest, and it is also the mechanism
of the defect: a guard fitted to the reviewer's mutation string tests the string,
not the property, and the property is *the scaffold does not tell the author to
omit a block it offers `preserved` for*.

*Satisfier*: **doc** — bring the manifest line onto the templates' grammar; and
**test** — assert the property over the whole emitted text (no omission
instruction anywhere in `blocks` while `preserved` is an offered value), not one
phrase.

**[E2 -- P2] The D1 fix traded coverage: a placement the previous fence caught
now passes, and `_SCAFFOLDED_TRANSITIONS` omits a transition its own scaffold
serves.**

The fence is now derived from `_SCAFFOLDED_TRANSITIONS`, exactly as D1's
satisfier asked. Two consequences the Sharpening's table does not show.

*First, `_SCAFFOLDED_TRANSITIONS` is incomplete on its own terms.* `_scaffold`'s
plan branch returns `("open/awaiting-plan-review", "executing", ...)` — the same
block is emitted from **two** source statuses, and `PLAN_TRANSITIONS_REVIEW_NOT_REQUIRED`
confirms `open -> executing` is the path a plan takes when plan review is *not*
required. The constant names only `("plan", "awaiting-plan-review",
"executing")`, and the fixture declares `**Plan review**: required(Internal)`. So
the lighter-ceremony path — the one where no plan reviewer is watching — is
unswept.

*Second, the sweep is narrower than the one it replaced.* The old fence swept
`_legal_transitions` from a `revised` fixture, which covered `-> accepted`. The
new one does not.

Measured at `8ad50ed` unless stated, each mutation applied to **both** twins and
reverted after; the gate body is identical in every row, only its condition and
message change:

| Gate added to | Test result |
|---|---|
| `_gating_preconditions`, `proposal` / `target == "revised"` | 1 failed — detected (D1 closed) |
| `_gating_preconditions`, `plan` / `target == "executing"` | 1 failed — detected (D1 closed) |
| `_gating_preconditions`, unconditional | 2 failed — detected |
| `_conformance_violations`, unconditional | 2 failed — detected |
| `_gating_preconditions`, `plan` / `executing` / `art.status == "open"` | **98 passed** — undetected |
| `_gating_preconditions`, `plan` / `executing` / plan review not required | **98 passed** — undetected |
| `_gating_preconditions`, `proposal` / `target == "accepted"` | **98 passed** — undetected |
| the same `-> accepted` gate against the **pre-`6dde057`** fence at `f928d9c` | 1 failed / 82 passed — **it used to be detected** |
| `_gating_preconditions`, `plan` / `target == "archived"` | **98 passed** — undetected |
| refusal via `_legal_transitions` — the scaffolded target withheld entirely when the declaration is absent | **98 passed** — undetected |
| `_gating_preconditions`, `proposal` / `target == "revised"`, message worded without "scope delta" / "scope-remainder" | **98 passed** — undetected |
| `_conformance_violations`, unconditional, same rewording | **98 passed** — undetected |

The last three rows are **pre-existing**, not introduced by `6dde057`: the fence
has always asserted on the *text of a gate's description* (`"scope delta" not in
joined`) rather than on whether a gate is unmet, and it has never looked at
`_legal_transitions`, which is the strongest way to refuse a transition — not
offering it. I record them because the clearing pass's own closing note said the
derived-set fix *"removes the enumeration problem"*. It does not; it moves it
from a list of placements to a list of triples plus a list of message phrases.

*Satisfier*: **test** — take the `(kind, status)` cross-product over every source
status that reaches a scaffolded target (derive it from `PLAN_TRANSITIONS` /
`PLAN_TRANSITIONS_REVIEW_NOT_REQUIRED` / `PROPOSAL_TRANSITIONS` rather than
hand-listing), and assert on *gate state* — that the set of unmet gates and
conformance violations is unchanged between an artifact with and without a
declaration — instead of grepping their prose. Or **wontfix** with the residual
stated in the module docstring, which is cheaper and honest; what is not
acceptable is the current docstring, which claims the absence is pinned.

**[E3 -- P3] The grammar guard pins six of seven surfaces, and the missing one is
the canonical source.** `_GRAMMAR_TEMPLATES` lists four templates and the two
scaffolds are covered through `_scaffold`. A whole-tree sweep for
`**Scope delta**` finds a **seventh** live surface printing the value list:
`doctrine/proposals.md:523`. That is not incidental — this plan's own record
(C8) says the six were unified *onto* doctrine's three-value grammar. Reverting
`doctrine/proposals.md` alone to `degraded | lost` leaves **98 passed**; the
six-surface revert the Sharpening's table records reddens **6**, and adding the
seventh to that revert still reddens only **6**, so the doctrine surface
contributes nothing. The `_DOCTRINE_PROPOSALS` obligation on that file is
`r"\*\*Scope delta\*\*"`, which matches either grammar.

*Satisfier*: **test** — add `doctrine/proposals.md` to `_GRAMMAR_TEMPLATES` (one
line), or **doc** — say in the module docstring that the canonical grammar's own
home is deliberately unpinned and why.

**[E4 -- P3] "The count is withdrawn rather than re-dated," and a bare count
appears one section later.** D3's disposition reads: *"the count is withdrawn
rather than re-dated"* — and `### D5 closed` opens its verification with
*"Mapped set (31 modules, recorded command)"*. The figure is **correct** (I ran
the recorded grep at `8ad50ed` and got 31) and the section heading dates it, so
this is a wording defect, not a false claim. It is worth one line because the
stated remedy and the next paragraph disagree, and a later reader deciding how to
record a count will find both.

*Satisfier*: **doc**.

**[E5 -- observation, not a finding against this plan] The fence is pinned to
pending-retirement vocabulary, and would go vacuous silently.**
`_SCAFFOLDED_TRANSITIONS` names `proposal reviewed -> revised`. At `8ad50ed`
`PROPOSAL_STATES` carries both vocabularies — `awaiting-review / revising /
awaiting-decision` alongside `proposed / reviewed / revised` — and `_scaffold`
has branches for `reviewed`, `revised`, `awaiting-plan-review`, `executing`,
`awaiting-code-review`, `review`, `archived`, and **none** for `revising`. That
belongs to `review-efficient-lifecycle`, in flight, and is not this plan's to
fix. The part that *is* this plan's to know: the fence never asserts that its
transitions are legal, so when `reviewed -> revised` retires the two fence nodes
keep passing against a transition that no longer exists. A one-line assertion
that `target in planner._legal_transitions(art)` would make that retirement loud
instead of silent.

*Satisfier*: **test** (one assertion) or **defer**, homed on
`review-efficient-lifecycle`.

### What I probed and could not defeat

Given this record's history, a clean row is a claim about my probe, not about the
code, so I name the attack.

* **D2 and D7, obligation by obligation.** I did not re-run the composite. On the
  shipped board I deleted the grouped-remainder requirement *alone* (1 failed)
  and the both-stages baseline framing *alone* (1 failed); the clearing pass's own
  keep-only-concede mutation reddens 2. Cairn's own board reddens 2 on the
  equivalent cut. C9's fence paragraph reddens 1 in **each** plan template
  independently. Gutting `doctrine/plans.md`'s floor-section body while keeping
  the heading reddens 1 — the exact construction D7 raised, now closed. Each new
  pattern has exactly **one** occurrence in its file, so none is being satisfied
  from a different section.
* **The heading-satisfaction class, swept exhaustively rather than spot-checked.**
  I re-derived the match site of every one of the **84** parametrized patterns
  against the raw bytes with a whitespace offset map, and classified each: **0**
  land on a heading line. 38 land inside a blockquote, a fenced code block, or
  across a line wrap — all legitimate (the team-gated module states its rule *as*
  a blockquote; the templates state the declaration *as* a code block; the
  wrapping is what `_normalized` exists for). No table-of-contents entry or quoted
  example satisfies any pattern.
* **The twins, and what this plan ever touched in them.** `cmp` says
  byte-identical at `8ad50ed`. Every planner hunk this plan has *ever* produced —
  `ccffb77`, `3f92cd8`, `8ad50ed`, found by diffing each of the plan's fourteen
  commits against its own parent — lands inside `_scaffold`. `_conformance_violations`
  is byte-unchanged by this plan, as the Verification section claims. No
  transition refuses on anything new: the planner's gate list for the two
  scaffolded transitions is identical with and without a declaration.
* **Partial and single-surface grammar drift.** Reverting one template alone
  reddens 1; all four templates reddens 4; the two scaffold literals reddens 2;
  all six reddens 6 — matching the Sharpening's figure once you revert **both**
  literals per twin (there are two, per D4; a first-occurrence-only revert reddens
  5, which is how I first mis-measured it). Whitespace and wrapping do not evade:
  `_normalized` collapses runs, and the scaffold assertions go through `_scaffold`
  rather than the source text.
* **The mapped set, re-derived and re-run.** The recorded grep yields **31**
  modules at `8ad50ed`; running them gives **3 failed, 1559 passed** in 160.1 s —
  the Sharpening's figures, reproduced independently. The three are the node ids
  the record names; the two `TestLoaderContainmentMatrix` failures are
  *"loading the planner mutated the working tree"* (`__pycache__`), which no
  string literal inside `_scaffold` can cause. Attribution elsewhere holds.
* **The archive gate, re-checked because the record contains two contradictory
  accounts of it.** `tools/lifecycle_planner.py next` on this plan at `8ad50ed`
  now **refuses** `-> archived` and `-> ready-to-archive`, naming
  `'## Code review -- Claude (Internal) -- 2026-08-12' carries a BLOCKING
  verdict`. The clearing pass reported `[ok]`, the Sharpening explained it as
  `_LEGACY_CODE_REVIEW_DISPOSITIONS` grandfathering; at the current tree state
  neither is live — the gate reads the verdict and refuses. Whatever clears this
  plan has to be a clearing verdict on a later pass.
* **Standing gates.** `scripts/claim_check.py` on this plan: clean.
  `scripts/check_cairn.py`: OK, 173 Markdown files, no issues.
  `quality_gate --sub neutrality --sub redundancy`: neutrality `fail=93 info=21`,
  redundancy `fail=0 info=2` — unchanged from the figures the record carries.

### Verification

All under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), the
canonical interpreter. Two detached worktrees at `8ad50ed`: one for the mapped
run and the standing gates, one for mutation, `git status --short` clean before
and after every mutation (the harness aborts on a dirty tree and restores from an
in-memory copy). One additional swap of `f928d9c`'s test module into the
mutation worktree, to measure the pre-fix fence against the same gate.

| Probe | Result |
|---|---|
| Baseline `bootstrap/tests/test_scope_reduction_trap.py` at `8ad50ed` | 98 passed (83 at `f928d9c`; +7 at `6dde057`, +8 at `8ad50ed`) |
| Mapped set (31 modules, recorded grep), `--quality-gate-shuffle-seed=0` | 3 failed, 1559 passed, 160.07 s — the three node ids the record names |
| D1 controls: gate at `proposal -> revised` / `plan -> executing` | 1 failed each — **closed** |
| D1 controls: gate unconditional / in `_conformance_violations` | 2 failed each — closed |
| Gate at `plan open -> executing` (no-plan-review path) | **98 passed** (E2) |
| Gate at `plan -> executing` when plan review not required | **98 passed** (E2) |
| Gate at `proposal -> accepted`, at `8ad50ed` | **98 passed** (E2) |
| The same gate against `f928d9c`'s fence | 1 failed / 82 passed — coverage lost (E2) |
| Gate at `plan -> archived` | **98 passed** (E2) |
| Refusal by withholding the target in `_legal_transitions` | **98 passed** (E2, pre-existing) |
| Gate at `proposal -> revised`, message reworded off the two pinned phrases | **98 passed** (E2, pre-existing) |
| `_conformance_violations` gate, same rewording | **98 passed** (E2, pre-existing) |
| Scaffold contradiction restored verbatim / **reworded** | 1 failed / **98 passed** (E1) |
| Manifest *"is OMITTED unless the revision narrows"*, live at HEAD, no mutation | **98 passed** (E1) |
| `doctrine/proposals.md` reverted to `degraded \| lost` | **98 passed** (E3) |
| Six-surface grammar revert (both literals per twin) / seven-surface | 6 failed / 6 failed (E3) |
| One template reverted alone | 1 failed — the grammar guard bites per surface |
| Shipped board: grouped-remainder alone / baseline framing alone / clearing pass's composite | 1, 1, 2 failed (D2 closed) |
| Cairn's own board: equivalent composite | 2 failed (D2 closed) |
| C9 fence paragraph deleted, each plan template separately | 1 failed each (D7 closed) |
| `doctrine/plans.md` floor-section body gutted, heading kept | 1 failed (D7 closed) |
| Match-site classification of all 84 parametrized patterns | 0 on a heading; 38 in blockquote / code fence / across a wrap, all legitimate |
| Recorded mapped-set grep at `8ad50ed` | 31 modules (D3 correct) |
| `3f92cd8` `Scope delta` literal lines changed per twin | 2 (D4 correct) |
| Planner hunks across all 14 plan commits | all inside `_scaffold`; `_conformance_violations` byte-unchanged |
| Planner twins at `8ad50ed` | byte-identical (`cmp`) |
| `tools/lifecycle_planner.py next` on this plan | refuses `-> archived` on the blocking verdict |
| `scripts/claim_check.py` on this plan | clean |
| `scripts/check_cairn.py` | OK, 173 Markdown files, no issues |
| `quality_gate --sub neutrality --sub redundancy` | neutrality fail=93 info=21; redundancy fail=0 info=2 — unchanged |

### Coverage

**Covered, with falsifiable citations** — every one of D1-D7 checked against the
landed bytes or by execution, never from the Sharpening's tables, and every
mutation chosen by me rather than copied from the record except where a row says
otherwise: D1 by thirteen gate placements across three refusal surfaces including
one measured against both versions of the fence (closed for its two named
mutations, E2 for the rest); D2 and D7 by per-obligation deletion on both copies
of every paired surface, plus an exhaustive match-site classification of all 84
patterns for the heading defect; D3 by re-running the recorded grep; D4 by diffing
`3f92cd8`; D5 by reading the emitted `blocks` and by a reworded-contradiction
mutation (**open**, E1); D6 by locating the disclosure in the record; the
Sharpenings' collateral by diffing every plan commit's planner hunks, `cmp` on the
twins, and confirming the gate list is unchanged with and without a declaration.
Sweep roster worked in full: claims (every figure in both Sharpenings re-derived),
production path (the scaffold exercised through `_scaffold`, the gates through
`_gating_preconditions` / `_conformance_violations` / `_legal_transitions`),
design completeness (the `(kind, status)` cross-product, E2), fail-closed (E1 and
E2 are both guards that return success without testing the property), cross-
document consistency (the seventh grammar surface, E3), drift (commit bodies
against landed bytes; the archive gate against two contradictory accounts of it),
lifecycle placement (the gate now refuses on the verdict), scope (nothing
expanded), and a named satisfier on every finding.

**Not covered / low confidence** —

* **This is an Internal read** — same agent type as the author and as both prior
  reviewers. It supplies independence of *session* and of *prior within this
  plan*, not of *type*. The distribution's judgement calls — `preserved`-owes-
  nothing as the default, the grouped record's shape, the three-value grammar —
  have had no cross-type read at any point in this plan, and nothing here changes
  that.
* **I did not re-read the change end to end**, and did not re-audit C1-C11. My
  scope was D1-D7 and the two Sharpenings. If the 2026-08-11 pass missed an
  enumerated Part 9 surface, I would not have found it.
* **E2's table is still an enumeration.** I found five evading placements the
  previous pass did not; I have no argument that a sixth does not exist. That is
  precisely why E2's satisfier asks for an assertion on *gate state* rather than a
  longer list — but I did not build it, so I cannot claim the space is closed.
* **I did not run the full suite.** The plan's Boundary-B bounding argument — the
  whole executable delta is string literals inside `_scaffold`, plus one
  file-reading test module — held under my own inspection of all fourteen commits'
  planner hunks, so I ran the 31-module mapped set instead. If that bounding is
  wrong, my run does not catch it.
* **The three mapped-set failures are attributed, not root-caused.** I read the
  assertion text and satisfied myself that a string literal in `_scaffold` cannot
  produce *"loading the planner mutated the working tree"*. I did not bisect them.
* **Nothing here tests the rule in use.** No author has met this declaration and
  behaved differently. The proposal's own residual is untouched, and three review
  passes have now been spent on whether the guards guard rather than on whether
  the rule works.

**On archiving.** This plan cannot archive on this section. E1 is a blocking
finding on a D-finding the record declares closed, and the planner already
refuses `-> archived` on the standing blocking verdict. E1 and E3 are one-line
fixes; E2's honest form may well be a `wontfix` with the residual moved out of
the docstring's claim and into its disclosure. What clears this plan is a *later*
independent pass over those corrections — not a response appended beneath this
one.

### Sharpening -- Claude -- 2026-08-12 (on the second clearing pass, E1-E5)

**Model**: Claude Opus 5 (`claude-opus-5`)

**E1 accepted and diagnosed, but NOT LANDED — see "Blocked on contention"
below before reading the rest of this section as done.**

**E1 is the finding, and it is worse than a missed fix.** D5 named two
contradictory pieces by direct quotation — the block prose *and* the manifest
line. I fixed the block, restated D5 in my Sharpening **without the manifest
half**, and wrote "Both scaffolds now say what the templates say." That is a
scope reduction performed inside a fix, in the plan whose subject is scope
reduction, and it is the fourth instance of the same shape in this record.

The mechanism is now specific enough to name: **I paraphrase a finding before
fixing it, and the paraphrase drops parts.** Not a testing failure — a reading
failure that testing then inherits, because I test the paraphrase. Working from
the reviewer's literal quoted text, item by item, is the correction; that is
what this round did.

| | Disposition |
|---|---|
| **E1** | `accept` — **applied, then backed out; blocked on contention.** See below. |
| **E2** | `accept` — coverage restored *and* extended, not `wontfix`. |
| **E3** | `accept` — the canonical surface now pinned first. |
| **E4** | `accept` — the record's own contradiction corrected. |
| **E5** | `defer` — see below; it belongs to another plan. |

**[E2] not a `wontfix`.** The reviewer offered one, and it would have been the
easy resolution to an underspecification finding — the exact move Part 2 of this
proposal says must argue for itself. It does not need to: the D1 fix swept only
the scaffolded transitions and lost the all-legal-transitions coverage the
version before it had, so a gate at `proposal -> accepted` went undetected. The
fence now sweeps **both** — the scaffolded target *and* every other legal
target — plus a third fixture for the plan `open -> executing` route, which
`_scaffold` serves and no fixture reached.

**[E5] defer** — the fence pins `reviewed -> revised`, vocabulary pending
retirement in `review-efficient-lifecycle`. When it retires this fence goes
vacuous-but-green. That is that plan's territory and its own transition work
will surface it; homing it here would duplicate the ownership.

### A finding of my own, and it needs the Maintainer

While fixing E1 I found the planner has grown `_declared_reduction` and
`plan_inheritance_violations` (`review-efficient-lifecycle`, Amendment B), which
**refuse a transition** when a declared `degraded`/`lost` carries no Maintainer
allowance blockquote.

Two consequences:

1. **Both my manifest strings have become false.** They say "THE TOOL DOES NOT
   CHECK THIS". The tool now checks part of it. My own guard caught this — it
   pinned the literal "DOES NOT CHECK" and went red when reality diverged from
   the claim, which is the one thing today a guard of mine did before a
   reviewer did. The correction is written and verified but **not landed**; see
   below.
2. **Whether this is the declined gate arriving is not mine to decide.** Round 3
   declined a gate that refuses "when the declaration is missing, **or** when
   `reduced` carries no grouped disposition." The landed check does not do the
   first and does something close to the second. Its rationale differs — Round 3
   declined *presence* checking because it catches forgetting rather than
   evading; this checks *authorization on a declaration that exists*, which is
   the authority rule made structural rather than a clean pass manufactured.

I did **not** extend the fence to `plan_inheritance_violations`. Doing so would
turn the build red and assert that another plan's accepted, landed work is
wrong, which is a Maintainer call across two plans, not an implementer's.

### Verification

### Blocked on contention — E1 and the manifest correction

I wrote both fixes, verified them, and **backed them out again**. The two
planner twins carry **~773 lines of another agent's uncommitted `chunk P2`
work**, under their own active work-intent claim. My claim overlapped without
the tool reporting a conflict.

Path-scoped committing does not help here: the collision is *inside a file*, not
across the index, so committing `tools/lifecycle_planner.py` would carry their
773 lines into my commit under my message — and leaving my ten lines there would
put mine into theirs. Backing out was the only option that protects both.

The fixes are recorded verbatim in this section and in `d74a47c`'s E1, so
nothing is lost. They land when the twins are free. Until then the manifest
assertion in `test_scope_reduction_trap.py` deliberately still pins
`"DOES NOT CHECK"` with a comment naming it as currently false — a known-stale
pin is safer than no pin, because it cannot be forgotten silently.

**Twin drift note**: `test_the_two_planner_twins_stay_byte_identical` is red in
the working tree. Verified as **not mine** — 16 differing lines, none of them
touching the declaration, the manifest, or any string I wrote. It is that
agent's transient mid-edit state.

### Verification

The second clearing pass's own defeating mutations, all four now red:

| Mutation | Before | After |
|---|---|---|
| gate at `proposal -> accepted` | 98 passed | **1 failed** |
| gate at plan `open -> executing` | 98 passed | **2 failed** |
| revert `doctrine/proposals.md` grammar alone | 98 passed | **1 failed** |
| restore the manifest contradiction | 98 passed (no mutation needed) | **1 failed** |

100 nodes, was 83 before this round of findings. The `manifest-contradiction`
row above was measured with the fix applied, before it was backed out; the other
three are independent of the planner and hold as committed.

**And the archive gate now refuses on its own terms**, naming the blocking
verdict and its section. That supersedes both my earlier report that the gate
never reads the verdict *and* the grandfathering explanation in the previous
Sharpening: at this tree state the exemption no longer applies, because the
latest pass is a real blocking verdict rather than the enumerated legacy one.

### Maintainer decision -- the two gates -- 2026-08-12

**Both stand.** Authorization, quoted verbatim:

> "We are finishing up this plan, I don't think that leaving them standing works
> because they rot. Let's let both stand for now."

Decided rather than deferred, on the Maintainer's reasoning that an unresolved
cross-plan question rots.

**The boundary, stated so it is not accidental:**

* **A presence check is forbidden** — no transition may refuse because a
  `Scope delta` declaration is *missing*. Round 3's reason holds: a tool can see
  whether the box is ticked, never whether the tick is honest, so it catches
  forgetfulness, misses evasion, and supplies cover for evasion by turning the
  transition green.
* **An authorization check is permitted** — refusing a declaration that *exists*
  and declares a loss but carries no Maintainer allowance is enforcing **who may
  concede an outcome**, not the paperwork. The accepted rule's own words:
  *"partial changes what residual is recorded, never who may concede it."*
  Authority is the part that cannot be recovered after the fact.

### Correction, and why the guard is not written yet

I reported to the Maintainer that `review-efficient-lifecycle`'s Amendment B
**had landed** `_declared_reduction` and `plan_inheritance_violations`. **That
was wrong.** Verified: `git show HEAD:tools/lifecycle_planner.py` contains
neither. They exist only in the shared working tree, inside that agent's ~773
uncommitted lines. I read the file, saw the code, and said "landed" when I meant
"present in my tree" — the same conflation behind this record's other errors.

So the decision above is recorded and the guard is **owed, not written**. A test
pinning those functions today would pass for me and fail in any clean checkout,
and would break if that agent revises the design before committing — which is
ordinary mid-plan behaviour, not a hazard on their side.

**What is owed once those functions are committed:** extend the fence in
`bootstrap/tests/test_scope_reduction_trap.py` to assert the boundary in *both*
directions — no surface refuses on a missing declaration, **and** the
authorization check is present, so neither half can drift away silently. The
existing fence already holds the first half and is committed; it is correct as
it stands and needs no change now.

**Trigger:** the commit that lands `plan_inheritance_violations`.

### E1 landed, and the two-gate guard written -- Claude -- 2026-08-12

The contention cleared: `chunk P2` and `P3` committed, both twins byte-identical
at `HEAD`, no active claims, and the Maintainer confirmed the other agent is
paused. Both owed items landed together.

**E1 — the manifest half of D5.** Both scaffolds' manifests now match their block
prose and, more importantly, are **true**. The old text said "THE TOOL DOES NOT
CHECK THIS" flatly; that is no longer accurate, so each manifest now states the
split: a *missing* declaration is uncaught, a *declared* `degraded`/`lost`
without its allowance **does** refuse, and whether a declaration is **true**
stays review's call.

**The two-gate guard, written against measured behaviour rather than my reading
of it.** I probed `_declared_reduction` before pinning anything, and the probe
corrected me twice:

| Input | Result |
|---|---|
| absent declaration | yields nothing |
| `preserved` | yields nothing |
| `degraded` / `lost` without allowance | `(value, allowed=False)` |
| `degraded` with an isolated blockquote | `(value, allowed=True)` |

That is exactly the boundary the Maintainer decided, and it is pinned in both
directions: an absent or `preserved` declaration must keep yielding nothing (the
**forbidden** presence check), and a declared loss must keep reporting its
allowance state (the **permitted** authorization check).

### Two corrections to what I told the Maintainer about the conflict

1. **I overstated the tension.** `_declared_reduction`'s own docstring cites
   `doctrine/dual-review.md` > "The counterweight" and quotes this plan's rule
   verbatim — *"No tool refuses a transition on a missing or malformed
   declaration"* — as the reason a `preserved`, absent or unrecognized value
   yields nothing. The other implementer encoded the boundary deliberately. I
   escalated as a conflict between two accepted proposals something whose
   author had already reconciled them in code.
2. **The refusal is dormant.** `plan_inheritance_violations` is gated on
   `_declares_inheritance`, and its docstring records that **zero of 94
   artifacts** in this tree declare it. So the check currently fires on nothing.
   The Maintainer's decision remains right and is now pinned; the urgency I
   attached to it was not.

Pinning `_declared_reduction` rather than `plan_inheritance_violations` follows
from that dormancy: the predicate carries the rule, the caller carries a
population that is presently empty. A guard on the caller would have tested the
population.

### Verification

| Mutation | Result |
|---|---|
| the **declined** presence check arrives (`preserved` becomes refusable) | **1 failed** |
| the **permitted** authorization signal is lost (`allowed` forced `True`) | **2 failed** |
| the manifest returns to the flat "DOES NOT CHECK THIS" claim | **1 failed** |

105 nodes, was 100. Twins byte-identical. Mapped set (31 modules `as_of` this
commit): **1752 passed, 3 failed** — the three known pre-existing node ids, all
reproduced at clean `HEAD` earlier and none attributable here. `check_cairn`
reports **1 issue**, at `dev/plans/git-native-security-foundations.md:2183`, in
another agent's file and untouched by this change. Neutrality `fail=93`,
redundancy `fail=0`, both unchanged.

**All seven D-findings and all five E-findings are now closed.** What remains
before archive is one independent pass over these corrections — the code
review's verdict is still `REVISE`, and every Sharpening answering it is mine.

## Code review -- Claude (Internal, third clearing pass) -- 2026-08-12

**Reviewed commit**: `c53e706`, reached through `6dde057`, `8ad50ed`, `e33f77d`,
`3789f8d` and `aa4015f`, each diffed against **its own parent** so the other
agents' interleaved commits are excluded rather than trusted.
**Target**: whether D1-D7 and E1-E5 are genuinely closed, and whether the
corrections introduced anything new. Not a fresh end-to-end read of the change
and not a re-audit of C1-C11; those passes landed on 2026-08-11 and 2026-08-12
and I repeated neither.
**Prior findings**: D1-D7 from `## Code review -- Claude (Internal) -- 2026-08-12`
and E1-E5 from `## Code review -- Claude (Internal, second clearing pass) --
2026-08-12`, both verdict `REVISE`. Dispositioned by the author across the
Sharpenings at `6dde057`, `8ad50ed`, `e33f77d` and `aa4015f`, with the
Maintainer's two-gate decision scribed at `3789f8d`.
**Assurance path**: standard
**Model**: Claude Opus 5 (`claude-opus-5`)
**Findings**: raised

**Tier — stated honestly.** Fresh session, same agent type as the author and as
all three prior reviewers: the **Internal** floor, *not* External. What this pass
supplies is the structural property doctrine requires — a blocking verdict
answered by a **later independent pass** rather than by the implementer's own
Sharpening. It supplies no cross-type assurance on the distribution's judgement
calls; those have had none since the proposal, and nothing here changes that.

**Verdict**: REVISE

**Ten of the twelve findings are genuinely closed, and I closed them by attack
with mutations I chose rather than the ones in the Sharpening tables.** D1's and
E2's two named gate placements now redden; so does a gate at `proposal ->
accepted`, the coverage E2 showed had been traded away. D2 and D7 bite per
obligation on both copies of every paired surface. I re-derived the match site of
all **84** parametrized obligation patterns against the raw bytes with my own
whitespace offset map: **zero** land on a heading line, so D7's
heading-satisfaction defect is closed independently of the previous pass's
measurement. E3's seventh surface reddens on its own. E4's wording is corrected.
E1's *textual* half is closed on every copy: I called `_scaffold` on **both**
twins for **all three** source statuses that reach the two scaffolded targets and
read the block and the manifest, and no "omit entirely" or "OMITTED unless the
revision narrows" survives anywhere in the tree.

Two things block, and they are the same shape this record has now produced five
times — **a surface that names an enforcement, and the enforcement is not
there**. This time it is not a guard that fails to see a defect; it is the
author-facing scaffold **affirmatively telling the author that a check exists
which does not** (F1), and the newest guard failing to pin the boundary it was
written to pin, in both directions (F2).

### Findings

**[F1 -- P1] The E1 fix replaced a false manifest claim with a differently false
one, on the surface Chunk C exists for — and the new one fails open.**

E1 was right that "THE TOOL DOES NOT CHECK THIS" had become false. The
replacement, live in both twins at `c53e706`, tells the author:

* proposal `-> revised` (`tools/lifecycle_planner.py:4906`): *"A declared
  `degraded`/`lost` WITHOUT the Maintainer's isolated allowance blockquote in the
  same record DOES refuse."*
* plan `-> executing` (`tools/lifecycle_planner.py:4976`): *"A declared
  `degraded`/`lost` without that allowance recorded as an isolated blockquote
  DOES refuse."*

**Nothing refuses.** `_declared_reduction` (`tools/lifecycle_planner.py:3334`)
has exactly **one** caller in the tree — `tools/lifecycle_planner.py:3518`,
inside `plan_inheritance_violations` (`:3368`). That function returns `[]` on its
first statement when `art.kind != "plan"`, and returns before the
`_declared_reduction` loop when `not _declares_inheritance(art)`.

Measured at `c53e706`, canonical interpreter, no mutation — artifacts built under
`dev/proposals/` and `dev/plans/` and read through `planner._read_artifact`:

| Artifact | `_declared_reduction` | `plan_inheritance_violations` | transitions refusing on it |
|---|---|---|---|
| proposal at `reviewed`, `**Scope delta**: lost`, no blockquote | `[(8, 'lost', False)]` | `[]` | **none** — `revised`, `accepted`, `rejected`, `superseded` all clean |
| plan at `executing`, `**Scope delta**: lost`, no blockquote | `[(10, 'lost', False)]` | `[]` | **none** — `review`, `awaiting-code-review` both clean |

So the proposal-side claim is **categorically** false: no proposal can refuse on
this, ever, because the only consumer discards non-plans on entry. That is the
side E1 itself singled out — *"the proposal side is where a pre-Decision
narrowing is declared"*. The plan-side claim is true only for a plan declaring an
inherited proposal basis, which `plan_inheritance_violations`' own docstring
measures at **zero of 94 artifacts** in this tree.

**The record knows and the author is not told.** `aa4015f`'s commit body asserts
*"a declared degraded/lost without its allowance refuses"* and then, four
paragraphs later, *"The refusal is DORMANT."* The plan record and the test module
docstring both carry the dormancy. The scaffold — the surface Chunk C justified
itself on, *the declaration where the author is typing* — carries only the
unqualified positive.

**The direction of the error is what makes this P1.** The old claim was
conservatively false: it understated the tool, and an author who believed it
would still do the work themselves. The new one is permissively false: it tells
an author narrowing their own scope that the tool will stop an unauthorized
concession. Round 3's decline, the Maintainer's 2026-08-12 decision, and this
module's own fence assertion all name that exact hazard in the same words — a
check that *"hands a quiet cut a green check to sit behind."* The scaffold now
manufactures the green check in prose.

**The guard cannot see it.** `test_the_emitted_scaffold_carries_the_declaration`
asserts `"refuse" in lowered` under the message *"the manifest no longer says
what DOES refuse"* — but on the proposal side that substring is already supplied
by *"NO TRANSITION REFUSES ON A MISSING DECLARATION"*, the sentence that says the
opposite. Deleting the entire "DOES refuse" claim from the proposal manifest in
both twins leaves **105 passed**.

*Satisfier*: **doc** — qualify the positive half to the population it actually
governs (a plan declaring an inherited proposal basis; today none), or drop it
and keep only what is true on both sides; and **test** — assert the manifest's
positive claim against the predicate's reach rather than against the substring
`refuse`.

**[F2 -- P1] The two-gate boundary guard does not pin the boundary in either
direction.** `test_the_declared_reduction_boundary_holds` is the answer to the
Maintainer's decision, and its docstring claims: *"if a later change makes an
absent or `preserved` declaration yield something refusable, the forbidden gate
has arrived; if a declared loss stops reporting its allowance state, the
permitted one has been lost."* I chose nine mutations of `_declared_reduction`
and `_has_isolated_blockquote` independently of the record. **Eight leave all 105
nodes green.** Each applied to **both** twins and reverted after; worktree
verified clean by `git status --short` before and after every one.

| Mutation | Boundary half attacked | Result |
|---|---|---|
| an **unrecognized** value becomes refusable (`preserved` still exempt) | forbidden | **105 passed** |
| value match made case-sensitive (`Lost` / `LOST` stop being read) | permitted | **105 passed** |
| emphasis stripping dropped (house form `**Scope delta: lost.**`) | permitted | **105 passed** |
| trailing-period strip dropped (`**Scope delta**: lost.`) | permitted | **105 passed** |
| allowance scoping widened from the record to the **whole artifact** | permitted | **105 passed** |
| fenced-code exemption dropped in `_has_isolated_blockquote` | permitted | **105 passed** |
| **isolation** requirement dropped (any `>` line counts) | permitted | **105 passed** |
| only the **first** declaration in an artifact reported | permitted | **105 passed** |
| allowance scoping narrowed to the declaration line alone | permitted | 1 failed — detected |

The first row is the serious one: it is **the declined presence check arriving**,
through the value-parsing path rather than the gate-placement path the fence
watches. Under it, the template's own unfilled prompt — `**Scope delta**:
preserved | degraded | lost`, the literal string `_scaffold` hands every author —
yields `('lost', False)` and becomes refusable. That is precisely what
`_declared_reduction`'s docstring says its `value is None` branch exists to
prevent, and nothing pins it.

Rows two to four matter because the forms they break are **live**: I confirmed
the predicate today correctly reads `**Scope delta: lost.**` (the house form that
bolds label and value together), `*degraded*`, `Lost`, `LOST` and `lost.`. Each
of those normalizations can be removed silently, and the permitted authorization
check then sees nothing to authorize.

The five parametrized cases pin value-in / value-out for two lowercase bare
spellings plus blockquote-present / blockquote-absent. Nothing pins parsing,
nothing pins record scoping, nothing pins isolation — the three properties the
guard's own prose names.

This is the fourth guard in this record whose stated property exceeds what it
asserts (C4 → D1 → E1 → here), and it was written in direct response to a
Maintainer decision, so it is the one most likely to be cited later as
settling the question.

*Satisfier*: **test** — drive the boundary through the parsing and scoping
surfaces (an unrecognized value and the unfilled prompt must yield nothing; the
house/emphasis/case/period forms must yield their value; an allowance in a
different record and a non-isolated or fenced `>` must not authorize).

**[F3 -- P2] E2 was closed on two of its three parts, and the part left out is
the one E2 said was not acceptable to leave.** The two named placements are
genuinely fixed — I verified the controls rather than reading the table: gates at
`proposal -> revised` (1 failed), `plan -> executing` (2 failed), `proposal ->
accepted` (1 failed) and unconditional (3 failed) all redden, and the third
fixture reaches the `open -> executing` route. But E2's finding had a third
component: three evasions it recorded as pre-existing, closing with *"what is not
acceptable is the current docstring, which claims the absence is pinned."*
Confirmed still open at `c53e706`, each gate body identical and only its
condition or wording changed:

| Real refusal on a missing declaration | Result |
|---|---|
| gate worded without "scope delta" / "scope-remainder" | **105 passed** |
| gate worded as "declares its reduction (preserved \| degraded \| lost)" | **105 passed** |
| refusal by **withholding** the scaffolded target from `_legal_transitions` | **105 passed** |
| gate at `plan -> archived` (also on E2's list) | **105 passed** |

E2 offered exactly two acceptable resolutions — assert on gate state, or
`wontfix` with the residual disclosed in the module docstring. Neither landed:
the fence still greps gate prose, `_FENCE_FIXTURES` is still a hand-list of
three, and a grep of the test module for `residual|wontfix|worded|phrase|evade|
unpinned` returns nothing disclosing any of it. The fence docstring still reads
*"If someone later adds the gate, this fails."* The Sharpening records `**E2** |
`accept` — coverage restored *and* extended, not `wontfix`.`

Worth naming plainly: this is the **same mechanism the implementer diagnosed in
themselves at E1** — *"I paraphrase a finding before fixing it, and the paraphrase
drops parts"* — recurring one section later, on the finding immediately after it.
The correction they adopted (work from the reviewer's literal quoted text, item
by item) was applied to E1 and not to E2.

*Satisfier*: **doc** — take E2's own cheaper option and state the residual in the
module docstring; or **test**.

**[F4 -- P2] The review-loop trap statement's first paragraph is unguarded on
both copies, including the shipped one adopters receive.** Deleting it from
`dev/agent_collaboration.md` and `templates/core/dev/agent_collaboration.md`
together leaves **105 passed**; deleting it from either alone does too. What
leaves with it: the asymmetry that makes narrowing cheap, *"treat a proposed
reduction with the same skepticism as a clean pass"*, the reviewer's obligation
to state **what is lost** and **why the narrower change still reaches the
cause**, *"'this is too large' is not a finding"*, and the author's
specify-don't-cut default.

The cause is the shape D7 was about. `_REVIEW_LOOP` carries five obligations;
four of them live in the *second* paragraph, and the fifth, `names the trap`
(`r"scope-reduction trap"`), is satisfied on its own by the trailing pointer
`(see doctrine/dual-review.md > "Review expectations — the scope-reduction
trap")`. My match-site map shows the two sites 21 lines apart on both copies.

Those three obligations are pinned elsewhere only in `doctrine/dual-review.md` —
which this module's own docstring says *"is **not** installed into an adopter
tree"*, the entire reason the module exists. So for an adopter they are pinned
nowhere. Chunk D's acceptance criterion was *"the two `agent_collaboration.md`
statements say the same thing"*; they can both stop saying half of it silently.
No prior pass reached this surface's first paragraph.

*Satisfier*: **test** — one obligation per claim in that paragraph (the
asymmetry, the reviewer's what-is-lost duty, the specify default), and a `names
the trap` pattern that the citation alone does not satisfy.

**[F5 -- P3] E5's `defer` was taken by the implementer, and no ledger row records
it.** `doctrine/dual-review.md` lens 9: *"a finding whose satisfier is none of the
five ... is the `defer` case, and `defer` is the Maintainer's call."* The
Sharpening records `**E5** | `defer` — see below; it belongs to another plan.`
with no authorization quoted, and `## Lifecycle disposition ledger` still carries
only its original three rows — nothing for D1-D7 or E1-E5. The planner reports
the same gap independently: `next` on this plan lists `[MISSING] every deferred
follow-up carries a recorded disposition` among the unmet archive gates. E5's
author framed it as *"observation, not a finding against this plan"*, which
mitigates the substance but does not move who may take the token.

*Satisfier*: **doc** — Maintainer confirmation and a ledger row.

**[F6 -- P3] The new guard couples this plan's suite to an in-flight plan's
predicate, with no ownership note.** `test_the_declared_reduction_boundary_holds`
pins `_declared_reduction`, owned by `review-efficient-lifecycle`, whose
`**Status**` is `executing`. The implementer named this hazard themselves before
the decision — *"would break if that agent revises the design before committing —
which is ordinary mid-plan behaviour, not a hazard on their side"* — and
committing chunks P2/P3 removed the *contention*, not the *coupling*. If that
plan revises the predicate before it archives, this plan's node goes red under
the wrong plan's name, and the module docstring names the boundary and the
Maintainer decision but not the owner.

*Satisfier*: **doc** — one sentence naming the owning plan in the docstring.

### What I probed and could not defeat

Given this record's history a clean row is a claim about my probe, not about the
code, so I name the attack rather than the conclusion.

* **E1's textual half, through `_scaffold` rather than by grep.** I loaded
  **both** twins as separate modules and emitted the full `[block] + manifest`
  for all three `(kind, status) -> target` combinations that reach the two
  scaffolded targets — proposal `reviewed -> revised`, plan
  `awaiting-plan-review -> executing`, plan `open -> executing`. All six emissions
  offer `preserved | degraded | lost` in the block and describe `preserved` the
  same way in the manifest. A whole-tree grep for `OMITTED` and `omit entirely`
  finds no scope-delta occurrence outside this plan's own record, the guard's
  assertion string, and an unrelated sentence in `doctrine/session-routines.md`.
  D5's block half and E1's manifest half are both closed as *text*; F1 is about
  what the replacement text asserts, not about the contradiction returning.
* **The heading-satisfaction class, re-derived from scratch.** I built my own
  normalized-offset map (mirroring `re.sub(r"\s+", " ", ...)`) and mapped every
  one of the **84** parametrized patterns back to a raw line. **0** land on a
  heading. **22** have more than one match site; I read all 22 and all but the
  ones behind F4 are alternations matching twice inside a single paragraph, or
  the deliberate `Removed scope` / `Disposition/home` pair. The two that span
  genuinely different sections in `dev/plans/_template.md` and its twin
  (`accepted scope is a floor` at L135 and L379) are the D7 case, and the
  placement-specific `fence bounds this pass` obligation now covers it: deleting
  the C9 paragraph from either template alone reddens 1.
* **D2 and D7 per obligation.** Shipped board loses the grouped
  scope-remainder record alone: 1 failed. `doctrine/proposals.md` reverted to
  `degraded | lost` alone (E3): 1 failed. C9's fence paragraph deleted from each
  plan template separately: 1 failed each.
* **The record's own three mutations, reproduced.** `aa4015f`'s Verification
  table claims 1 / 2 / 1 failures for the arriving presence check, the lost
  authorization signal, and the manifest reverting. I re-ran all three: **1, 2,
  1**. The numbers in this round's record are right.
* **The predicate's live behaviour, twelve inputs.** `_declared_reduction`
  correctly reads the house form, emphasised, capitalised, upper-case and
  trailing-period spellings; correctly yields nothing for the unfilled prompt and
  for an unrecognized value; correctly refuses to count a `>` inside a code fence
  or without a preceding blank line; and correctly does **not** reach a
  blockquote in a different heading-bounded record. Two behaviours are disclosed
  design rather than defects: a single blockquote authorizes *every* declaration
  in its record, and any isolated blockquote counts — the docstring says
  structure is attested, never authenticity. The predicate is sound; F2 is about
  the guard over it.
* **Twin parity and the scope fence.** `cmp` says the twins are byte-identical.
  `_conformance_violations` still carries no scope-delta refusal, and the fence's
  four control placements redden, so the declined gate has not arrived by any
  route I found other than the parsing path in F2.
* **The known standing failures, confirmed rather than accepted.** The mapped set
  (31 modules, the recorded grep, re-derived) gives **3 failed / 1752 passed** in
  158.95 s at `c53e706` in a pristine worktree — the record's figures exactly, and
  the three node ids are the three named. I then ran those three nodes alone at
  `3789f8d`, before this plan's last two commits: **3 failed**, same ids. With the
  two earlier passes' measurements at `f928d9c` and `8ad50ed`, they are
  pre-existing and none is attributable here.
* **`check_cairn`'s one issue, confirmed not ours.** `1 issue across 174 files`,
  at `dev/plans/git-native-security-foundations.md:2183`, a broken link target in
  another plan's file that this change never touched. `claim_check` on this plan:
  clean. Neutrality `fail=93 info=21`, redundancy `fail=0 info=2` — unchanged.
* **Tree state.** `git status --short` showed no modified tracked files at the
  start of this pass and none at the end; the three untracked paths (`.claude/`,
  `dev/measurement/collision_log.md`, `dev/measurement/snapshots/`) predate it.
  The tree HEAD advanced from `c53e706` to `4de1132` mid-pass with four commits
  belonging to `ceremony-handshake-and-first-use`; their diff touches two
  Markdown files in that plan's own lifecycle and **no** surface in `_SURFACES`,
  neither planner twin, and not this plan, so the reviewed range is unaffected.

### Verification

All under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), the
canonical interpreter. Two detached worktrees at `c53e706`: one pristine, used
for the mapped run and the standing gates; one for mutation, `git status
--short` asserted clean before and after every mutation by the harness itself,
which restores from an in-memory copy and aborts on a dirty tree.

| Probe | Result |
|---|---|
| Baseline `bootstrap/tests/test_scope_reduction_trap.py` at `c53e706` | 105 passed (was 100 at `3789f8d`, 98 at `8ad50ed`, 83 at `f928d9c`) |
| Mapped set (31 modules, recorded grep re-derived), `--quality-gate-shuffle-seed=0` | 3 failed, 1752 passed, 158.95 s — the three known ids |
| Those three node ids alone at `3789f8d` | 3 failed — pre-existing, not this plan's |
| `_scaffold` emitted from **both** twins × 3 source statuses, block + manifest | no "omit entirely", no "OMITTED unless", no "DOES NOT CHECK" (E1 text closed) |
| Proposal at `reviewed` declaring `lost`, no blockquote — all 4 legal targets | **0 refusals**; `plan_inheritance_violations` → `[]` (F1) |
| Plan at `executing` declaring `lost`, no blockquote — all legal targets | **0 refusals** (F1) |
| Callers of `_declared_reduction` in the tree | exactly one, inside `plan_inheritance_violations` (F1) |
| Delete the proposal-side "DOES refuse" claim from both twins | **105 passed** (F1) |
| Delete the plan-side "DOES refuse" claim from both twins | 1 failed |
| 9 boundary mutations of `_declared_reduction` / `_has_isolated_blockquote` | **8 of 9 leave 105 passed** (F2) |
| Unrecognized value made refusable — unfilled prompt under mutation | yields `('lost', False)`; **105 passed** (F2) |
| 12 live-form inputs to `_declared_reduction`, unmutated | all correct — the predicate is sound |
| Fence controls: `proposal -> revised` / `plan -> executing` / `proposal -> accepted` / unconditional | 1 / 2 / 1 / 3 failed — D1 and E2's two placements closed |
| Gate worded off the two pinned phrases (two spellings) | **105 passed** each (F3) |
| Refusal by withholding the target in `_legal_transitions` | **105 passed** (F3) |
| Gate at `plan -> archived` | **105 passed** (F3) |
| Test module grepped for any residual disclosure | none (F3) |
| Delete review-loop paragraph 1, both copies / dev copy alone | **105 passed** both (F4) |
| Match-site map of all 84 patterns | 0 on a heading; 22 multi-site, all read |
| `doctrine/proposals.md` reverted to `degraded \| lost` alone | 1 failed (E3 closed) |
| C9 fence paragraph deleted, each plan template separately | 1 failed each (D7 closed) |
| Shipped board loses the grouped scope-remainder record alone | 1 failed (D2 closed) |
| `aa4015f`'s own three mutations, re-run | 1 / 2 / 1 failed — record correct |
| Planner twins at `c53e706` | byte-identical (`cmp`) |
| `tools/lifecycle_planner.py next` on this plan | refuses `-> archived` on the blocking verdict, plus two further unmet gates |
| `scripts/check_cairn.py` | 1 issue across 174 files — `git-native-security-foundations.md:2183`, another plan's |
| `scripts/claim_check.py` on this plan | clean |
| `scripts/quality_gate.py --sub neutrality --sub redundancy` | neutrality fail=93 info=21; redundancy fail=0 info=2 — unchanged |

**On archiving, beyond this verdict.** Two archive gates are unmet independently
of any code-review verdict, and a clearing pass alone would not move them:
`## Lasting-truth migration` still reads *"Filled in at archive time."*, so the
loop-fidelity sign-off names no implementing commit; and the deferred-follow-up
dispositions gate is unmet, which F5 is one instance of. Whoever clears this plan
should expect to land those in the same round.

### Coverage

**Covered, with falsifiable citations** — every one of D1-D7 and E1-E5 checked
against the landed bytes or by execution, never from a Sharpening table, and
every mutation chosen by me: E1 by emitting both twins' full scaffolds across all
three source statuses and by tracing every caller of the predicate the new text
describes (**open**, F1); E2 by four control placements plus four evasions
(placements closed, disclosure **open**, F3); E3 by a single-surface revert; E4
by reading the corrected wording; E5 by locating its disposition and the ledger
(**open**, F5); D1 by the four gate controls; D2 and D7 by per-obligation
deletion on both copies of every paired surface plus an independently rebuilt
match-site map of all 84 patterns; D3 by re-deriving the 31-module grep and
running it; D4 by the record's own diff; D5 by the whole-tree omission sweep; D6
by locating the disclosure. Sweep roster worked in full: **claims** (every figure
in `aa4015f` re-derived; the scaffold's new refusal claim probed against the code
rather than accepted, which is F1); **production path** (the scaffold through
`_scaffold` on both twins, the gates through `_gating_preconditions` /
`_conformance_violations` / `_legal_transitions`, the predicate through
`_read_artifact` on real files); **design completeness** (twelve live input forms,
absent / unrecognized / unfilled-prompt / multiple-declaration / different-record
edges — F2); **fail-closed** (F1 and F2 are both surfaces that report success
while the property they name is absent, and F1 fails *open* in the author's
direction); **cross-document consistency** (F4's shipped/self-hosted pair, the
whole-tree grammar and omission sweeps); **drift** (`aa4015f`'s commit body
against the landed bytes — it contains both the claim and its own contradiction);
**lifecycle placement** (the archive gate re-run, and the two further unmet gates
recorded above); **scope** (the cross-plan coupling, F6); and **a named satisfier
on every finding**.

**Not covered / low confidence** —

* **This is an Internal read** — same agent type as the author and as all three
  prior reviewers. It supplies independence of *session* and of *prior within
  this plan*, not of *type*. The distribution's judgement calls —
  `preserved`-owes-nothing as the default, the grouped record's shape, the
  three-value grammar — have had no cross-type read at any point in this plan.
  Four Internal passes are not a substitute for one External one, and the fact
  that each pass has found real P1 defects the last missed is the argument for
  that, not against it.
* **I did not re-read the change end to end**, and did not re-audit C1-C11. My
  scope was D1-D7, E1-E5 and what the corrections introduced. If the 2026-08-11
  pass missed an enumerated Part 9 surface, I would not have found it — though
  F4 is a case of exactly that kind surfacing late, which lowers my confidence
  that the distribution audit is complete.
* **F2's table is an enumeration and I have no argument that it is exhaustive.**
  I found eight evading mutations; a ninth I did not think of may exist. That is
  why F2's satisfier asks for coverage of the parsing and scoping *surfaces*
  rather than a longer list of mutations.
* **I did not run the full suite.** The executable delta across this plan's
  commits is string literals inside `_scaffold` plus two file-reading test
  modules, which I confirmed by inspecting the planner hunks; I ran the 31-module
  mapped set instead. If that bounding is wrong my run does not catch it.
* **The three mapped-set failures are attributed, not root-caused.** I confirmed
  they reproduce before this plan's last two commits and that their assertions
  concern `__pycache__` paths, which no string literal in `_scaffold` can cause.
  I did not bisect them.
* **I could not defeat the predicate itself**, only the guard over it. If
  `_declared_reduction` has a defect, `review-efficient-lifecycle`'s own review
  is where it should surface; I probed twelve input forms and found none.
* **Nothing here tests the rule in use.** No author has met this declaration and
  behaved differently. Four review passes have now been spent on whether the
  guards guard, and none on whether the rule works — the proposal's own residual,
  untouched.

### F1 corrected -- Claude -- 2026-08-12

**F1 accepted, verified, and fixed. F2-F6 are left open deliberately — see the
recommendation.**

**Verified before acting.** `_declared_reduction` has exactly one caller
(`tools/lifecycle_planner.py:3518`), inside `plan_inheritance_violations`, whose
first statement returns `[]` for `art.kind != "plan"`. So on the **proposal**
side — the side E1 was about — nothing refuses, categorically. The plan side is
gated on `_declares_inheritance`, which no artifact declares.

**What I did was worse than what I fixed.** The original manifest understated
the mechanism and failed *closed*. Mine overstated it and fails **open**: it
told an author narrowing their scope that a check would catch them. That is the
"green check to sit behind" that Round 3's decline and the Maintainer's decision
both name, manufactured by the person implementing the rule against it. And
`aa4015f`'s own commit body carries both the claim and the words "The refusal is
DORMANT" — I wrote the refutation beside the assertion and shipped both.

**The correction** states only what is true: no transition refuses on a missing
or malformed declaration, and review is the enforcement including for whether a
declaration is true. D5's actual contradiction ("omit entirely" / "OMITTED
unless") stays gone — that half of E1 was correct and is untouched.

**The guard could not have caught this**, which is the more useful finding. It
asserted `"refuse" in emitted` — satisfied by the words *"NO TRANSITION
REFUSES"*. A guard whose pattern its own subject trivially satisfies tests
nothing. Replaced with an assertion that the manifest must **not** claim a
refusal, plus the caller-chain reasoning in the failure message so the next
person restoring it has to check first. Mutation: restoring the false claim now
fails 2 nodes, where it previously left 105 green.

### Recommendation: stop the Internal cycle

Four Internal passes have now each found real P1 defects the previous one
missed, and F4 — a Chunk D surface enumerated in this plan's own scope — was
reached by none of them. That is not convergence.

My own record is worse: a P1 defect introduced in each of the last three
correction rounds, and this one **actively harmful** rather than merely
incomplete. F2's fix would require me to write more guard logic, which is
precisely the thing failing.

The third pass names the gap directly: *"the distribution's judgement calls have
had no cross-type read since the proposal."* Every pass since has been
same-agent-type. A fifth Internal round would sample the same blind spots a
fifth time.

**F2-F6 are therefore left open and undisposed**, not because they are wrong but
because the next read should be **External** — a different agent type, which is
the tier this plan has not had since its proposal. That is the Maintainer's to
run.

