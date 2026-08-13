<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/dual-review.md doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: comprehension outlives the artifact

**Source proposals** — three, accepted 2026-08-13, draining into one plan by
Maintainer direction:
* [`comprehension-outlives-the-room`](../proposals/archive/2026-08-13-claude-comprehension-outlives-the-room.md)
  — the doctrine principle
* [`finding-tags-are-not-reasons`](../proposals/archive/2026-08-13-claude-finding-tags-are-not-reasons.md)
  — comments and docstrings
* [`test-names-outlive-their-plans`](../proposals/archive/2026-08-13-claude-test-names-outlive-their-plans.md)
  — test names

**Status**: revising-plan
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

## Settled: no parity guard

Put to the plan review; answered by the Maintainer before it ran.

> *"Let's not make machinery for this one. Just doctrine"*

**No parity guard, and no new test of any kind.** The scope fence above stands
as written, and the plan review need not revisit it.

The argument I had assembled *for* a guard was sound on its own terms — rule-text
survival is formal and decidable, and a parity test caught four deletable
obligations in the plan that closed this morning. It is set aside anyway, on the
Maintainer's standing reasoning: a mechanism has a permanent cost paid by every
contributor thereafter, and too many mechanisms increase the deliberative weight
they were meant to reduce. A rule that a person must read and apply is not a
weaker rule; it is a cheaper one, and this repository has been paying for the
expensive kind all week.

**Consequence for the record**: if these conventions later erode from one copy
while the suite stays green, that is the *accepted* cost of this decision and
not a defect discovered later. The revival conditions in both operational
proposals already name what would change the answer — coordinate names
reappearing after the rename, tags reappearing after the pass.

## Plan review -- Claude Opus 5 (Internal) -- 2026-08-13

**Tier**: Internal
**Findings**: raised
**Model**: Claude Opus 5 (`claude-opus-5`)

**Reviewed commit**: `ef00dfa625dbe1588feffeab5c666036d33c3633`
**Reviewed plan blob**: `73797f16fab1cff6bc7cec158ad3762a571dc3cb`
**Basis**: the three archived source proposals read in full including their
Round 2 / Round 3 revisions and Decisions; the corpus re-measured under the
canonical interpreter (`PYTHONDONTWRITEBYTECODE=1`), read-only.
**Verdict: REVISE** — nine findings, five of them load-bearing. The plan's
*design* is faithful: it executes three accepted decisions, adds no new outcome,
and drops none. What fails is the layer a plan review exists to check —
**the numbers, one named placement, and two acceptance criteria that cannot be
judged as written**. Four of the five major findings are the same defect in
different clothes: a count or a location asserted without being opened.

### What I re-measured, and what I got

All figures `as_of 2026-08-13` at `ef00dfa`, over `git ls-files '*.py'` (248
tracked files; the untracked `.claude/worktrees/` copies are excluded and would
otherwise inflate every count). "Bracketed tag" means
`\[[A-Z]{1,4}[0-9]+(-[0-9]+)?[a-z]?\]`; classification into
comment / docstring / other-string-literal is by `tokenize` + `ast`, not by
quote style.

| Plan says | I measured | Verdict |
|---|---|---|
| 262 tag sites | **265 bracketed occurrences on 238 lines across 37 files** | close enough; but "sites" ≠ "occurrences" and the plan uses them interchangeably |
| ~8 fenced | **42 in non-docstring string literals**, ~38 of them plainly fixture / test-input / generated-output | **wrong by ~5×** (F2) |
| 97 in the two `_gate_preflight` files | **98** in comments + docstrings; 105 including string literals | reproducible, immaterial delta |
| ~21 in each planner twin | **14** each (12 in comments/docstrings), identical at `f654dc0`, `2fd7f4f` and HEAD | **stale inherited figure** (F6) |
| ~36 coordinate-named containers | **40** leading-coordinate classes + **5** embedded-coordinate | under-measured and undefined (F7) |

Two figures the plan does not state, which change decisions:

* **349** of the **4261** pytest node ids pinned in
  `bootstrap/tests/fixtures/gate_manifest.json` carry one of those 40 class
  names, plus **30** skip/xfail entries (F4, F5).
* **Bare** finding tags — `FUR5`, `CR1`, `R2`, `P1` and kin, unbracketed — are
  excluded from every count above and are the larger population by an order of
  magnitude: **168** in the two C1 files alone, **391** in
  `tools/lifecycle_planner.py` (F1).

### Findings

**[F1 — major] The plan never says what a "tag" is, and under the accepted
proposals' own examples the corpus is several times 262.**

Every count in this plan is of *bracketed* tags. The tags proposal's rule is not
so limited — it reads *"`[S1]`, `[M2-1]`, `FUR5` and their kin"*, and its two
worked examples for this very file are **bare**:

* `bootstrap/tests/test_gate_preflight.py:1621` —
  `# FUR5 -- the recorded anchored invocation, actually executed` (the
  proposal's "cheap, immediately glossed" case)
* `bootstrap/tests/test_gate_preflight.py:1703` —
  `recorded one stayed broken, which is FUR5 exactly` (its "expensive, the tag
  is the grammatical subject" case)

`FUR5` never appears bracketed anywhere in the tree. So the Maintainer's raising
quote — *"I don't know what FUR5 is"* — names a form that **none of this plan's
97 sites includes**. An implementer clearing only bracketed forms finishes C1
with the exemplar untouched; one clearing the rule as written meets 168 further
occurrences in those two files and 391 in one C2 file, against a plan that
budgeted 97 and ~21.

*Required satisfier*: state the operative definition of "tag" in the scope
fence — either fence bare tags out **with their measured count**, so the fence
is checkable the way Round 3's `~8` was meant to be, or admit them and re-size
Chunks C1–C3. Silence here is what makes F1 a plan defect rather than a
judgement call: the plan says it will not leave the implementer a judgement the
plan should have made, and then leaves this one.

**[F2 — major] "~8 fenced" is wrong by ~5×, in the direction that breaks tests.**

42 bracketed occurrences sit in non-docstring string literals. Nearly all are
exactly what the fence describes — synthetic review fixtures
(`test_transition_lint.py` ×12, `test_lifecycle_contract.py`,
`test_lifecycle_vocabulary.py`, `test_reference_scripts.py`), homoglyph fixture
labels (`test_byline_identity.py` ×6), and **generated output**: the planner
twins each emit `* **[R1] -- <title>.**` as template text. The ~8 came from
Round 3's *"single-line quoted values"* row, which is a narrower class than the
fence the plan actually adopted.

This matters twice over. Chunk C's per-file acceptance is *"no tag remains
except inside fenced string literals"*; an implementer holding "~8" will read
the 12 `[R1] a finding` strings in `test_transition_lint.py` as in-scope prose
and edit test inputs. And the fence's size is precisely the thing Round 3
insisted on stating, after its own first attempt returned 98 by sweeping
docstrings into the wrong column — the same error, mirrored.

Related, and worth reconciling in the same edit: the accepted class table
(77 comments + 51 docstrings + ~8 quoted = 136) does not sum to 262. My
tokenized re-measure is **103 / 119 / 42 = 264**. All three cells are wrong;
the plan inherits one of them as an arithmetic operand.

*Required satisfier*: re-measure the fence and state it, with the method.

**[F3 — major] Chunk B3 names a placement that does not exist in the file it
names.**

`templates/core/AGENTS.md` has **no `**Naming.**` paragraph**. Its
`## Project-specific conventions` (`templates/core/AGENTS.md:388-396`) is an
*unfilled* `<!-- cairn:slot project-conventions -->` carrying only the prompt
*"Naming conventions, the development environment, the high-risk surfaces …
This is judgment work: a reasoning agent and the maintainer write the project's
**real** conventions here."*

And in Cairn's own copy, `**Naming.**` is **inside that same slot** —
`AGENTS.md:414` opens `cairn:slot project-conventions`, `AGENTS.md:514` closes
it, with the whole conventions body between. `bootstrap/fidelity-check.md:178`
records the slot as `filled`; `bootstrap/BOOTSTRAP.md:688` describes it as
adopter-authored.

So B1/B2 land in Cairn's filled slot (fine), and **B3 has nowhere to go**:
writing two Cairn-authored general rules into the shipped slot converts
adopter-owned space into governing text, which is not what a slot is. The E3
finding that produced this placement was about Cairn's copy, where
`**Naming.**` exists; nobody checked the twin. Chunk B's acceptance — *"both
rules present in both copies, in the conventions region"* — cannot be satisfied
in the shipped copy without deciding this.

*Required satisfier*: decide the shipped copy's home explicitly. Either a
non-slot region of `templates/core/AGENTS.md` (these are general conventions,
not project-specific ones), or an addition to the slot's *prompt* text — and say
which, because the two have different meanings for an adopter.

**[F4 — major] Chunk D's acceptance criterion is self-contradictory, and the
rename touches a file the plan does not list.**

Renaming a class changes every node id beneath it. So *"pass/fail set unchanged"*
is satisfiable, *"node count identical"* is satisfiable, and **"same node ids"**
(Acceptance criteria, line 182) is not — nor is *"mechanically checkable by
diffing collected node ids"* (Chunk D), which will report ~349 differences on a
correct execution. The names proposal wrote the criterion correctly as node
**count**; the plan hardened it to ids in one place and to an id-diff in the
other.

Worse, the same fact reaches a file the plan never names.
`bootstrap/tests/fixtures/gate_manifest.json` pins **4261 node ids**, of which
**349 carry one of the 40 classes**, plus **30** skip/xfail identities. Per
`bootstrap/tests/_gate_manifest.py:33-36` the manifest pins *"the set of pytest
node-IDs plus the identities of any skip/xfail-marked nodes (not merely
counts)"*, and *"a dropped node HOLDs"*. It was regenerated **today** at
`cfaace9` in a supervised re-anchor. Whatever the right disposition is — most
likely "re-produced at the next ceremony's Phase 0, nothing owed here" — the
plan has to state it, because the next ceremony operator inherits the drift.

*Required satisfier*: restate Chunk D's criterion as *node count + leaf ids +
pass/fail set unchanged; container segment changes by construction*, and record
a disposition for `gate_manifest.json` (including whether a Maintainer fence
applies, given the anchor is a supervised artifact).

**[F5 — major] The `Boundary B mode` bounding argument is falsified on its own
stated terms.**

It reads: *"no contract surface (the touched files are not the fidelity or gate
manifest …)"*. By F4, Chunk D invalidates 349 pinned entries in the gate
manifest — which `AGENTS.md` names as part of the install contract, the surface
on which *"bounded mode refuses, and the full suite runs"*. The plan's stated
falsification condition — a load-bearing comment inside a security-gate file
turning up during Chunk C's reading — is a real hazard, but it is not the one
that fires, and it is stated as a *discovery* condition when the disqualifying
fact is knowable now.

Note this is not automatically "run full": if the correct disposition in F4 is
that the manifest is regenerated by ceremony and this plan touches neither its
bytes nor its authority, the bounding may survive. The finding is that the plan
asserts the negative without having checked it, and `AGENTS.md` resolves
uncertainty to `full`.

*Required satisfier*: redo the bounding argument against the measured
interaction, and name the commands bounded mode will actually run.

**[F6 — moderate] C2's "~21 each" is stale, and four of five twin pairs are
unnamed.**

The planner twins carry **14** bracketed occurrences each (12 in
comments/docstrings) — identical at `f654dc0`, at plan-open `2fd7f4f`, and at
HEAD, so this is not drift since the proposal; the figure was never
re-measured. The plan re-measured 97 and ~36 and left this one inherited.

More consequential: five byte-identical `.py` twin pairs carry tags, and C2
names one. `templates/skills/_lib/lifecycle.py` ↔ `tools/lifecycle.py` carry
**17 each** — the third and fourth largest files in the corpus — and their
identity is enforced by
`bootstrap/tests/test_lifecycle_brief.py:351`
(`test_the_two_copies_are_byte_identical`). Also
`_lifecycle_metrics/__init__.py` (3), `_lifecycle_metrics/subsystems.py` (2),
`_intent/record_io.py` (1). All four fall into C3 *"the remainder"*, which
carries no twin warning and names no enforcer — and a one-sided comment edit in
any of them reds the suite.

*Required satisfier*: promote the `lifecycle.py` twins beside the planner twins
in C2, list the remaining three, and name each enforcer in Author-accounting.

**[F7 — moderate] "~36 containers" is under-measured and its rule is unstated.**

40 classes in `bootstrap/tests/` begin with a coordinate token
(`TestP2AmendmentBScopeReduction`, `TestChunkG*`, `TestCF1*`, `TestP6c*`,
`TestR6*`, `TestV1V2Differential`, …), and 5 more carry one embedded:
`TestHomoglyphAllowanceRV5`, `TestLivingStateF1`,
`TestTheLegacyTokensAreStillLegalUntilH1`, `TestEnforceModeAndN1`,
`TestTheR6PredicateIsShared`. In the other direction, a few of the 40 are
arguably domain vocabulary rather than plan coordinates — `V1`/`V2` are gate
manifest schema versions; `R1`/`R6` in `test_quality_gate_redundancy.py` are the
redundancy gate's own rule ids, and renaming those would *lose* meaning.

So "~36" is neither the count of any stated rule nor a bound on the work. One
loose end that falls out of the same read:
`bootstrap/tests/test_security_verification.py:1576` names
`TestChunkGArgvVectorValidation` in a comment, so the rename has at least one
in-tree textual reference to carry.

*Required satisfier*: state the matching rule, publish the resulting list (or
its count under that rule), and say which of the domain-vocabulary cases are
deliberately excluded.

**[F8 — minor] The mapped test/gate set for Chunks A and B is short by at least
one live guard and the standing prose gates.**

`bootstrap/tests/test_comprehension_floor.py` asserts, over **both** AGENTS
copies, that the floor's four obligations are present *and* that it *"sits in
the review section"* (`bootstrap/tests/test_comprehension_floor.py:61-74`).
Chunk B4 edits exactly that paragraph in exactly those two files; the plan names
only `test_installed_operational_rule_is_project_general`. Separately,
Verification names only `check_cairn.py` per chunk, but Chunk A touches
`doctrine/` and B3 touches `templates/` — both neutrality-gate surfaces, and
`AGENTS.md` requires the standing gates for every touched surface.
`python scripts/quality_gate.py --sub neutrality --sub redundancy` appears
nowhere in the plan.

*Required satisfier*: add both to the Chunk A/B mapping.

**[F9 — minor] Chunk A appears to drop the Naur citation.**

The doctrine proposal's grounding is Naur (1985), and its E1 response verified
the pagination independently and recorded it *"with a DOI, which is this file's
convention"* — `doctrine/rationale.md`'s convention being exactly the cited
grounding bullets Anchor 16 already carries (Miller, Kalyuga, Clark & Brennan,
the appropriate-reliance literature). Chunk A's two rows and its acceptance
criterion mention only the temporal paragraph and the Anchor 17 pairing. If the
citation is meant to land, say so in A1/A2; if it is deliberately out, say that
— removal of an accepted outcome is a deviation in the same way an addition is,
and the Decision's own "superseded commitments" list says the *check* is
discharged, not the citation.

### Verified clean — probed and passed

Stated so a later reader can tell what was examined from what was assumed.

* **The dead-trigger correction holds.** `git-native-security-foundations`
  archived at `f654dc0` (2026-08-13, "archive both security plans") and the two
  `_gate_preflight` files carry the same 105 bracketed occurrences at `f654dc0`,
  at `2fd7f4f` and at HEAD — the closure cleared none of them. Adopting them
  into C1 delivers Round 3's phase-3 completion guarantee earlier rather than
  changing scope; **no scope-delta declaration is owed** for it.
* **No accepted outcome is dropped, and none is added.** Each chunk maps to an
  accepted decision; the three "no test / no lint / no second doctrine home"
  fences are the proposals' own conclusions, not narrowing invented here. The
  settled no-parity-guard question is not reopened.
* **Chunk E is right to create no revival row.** Neither tracked
  `dev/PLANNING.md` item the operational proposals promised on acceptance was
  ever written — there is no "Rename coordinate-named test containers" row, and
  the "Opaque finding-IDs" row predates them and carries no three-phase text.
  Executing the work supersedes both; closing the one existing row is correct.
* **Tier and precondition are correct.** `required(Internal)` is the highest
  constituent declaration, recorded in the doctrine proposal's E2; the
  whole-plan start precondition genuinely retires both proposals' per-chunk
  sequencing, including the names proposal's `review-efficient-lifecycle` gate.
* **A→E sequencing is justified** — rules before the passes that apply them, and
  C/D are mutually independent (C touches comment/docstring bytes, D touches
  class names; their only shared file is `test_lifecycle_contract.py`, where the
  two edits do not overlap). I found nothing wrongly gated; the only fence
  question is F4's.
* **No `bootstrap/_scaffold/` file carries a bracketed tag**, so the AST
  attestation baseline is untouched by Chunk C — the plan's silence on it is
  correct rather than an omission.
* **The twin invariant C2 does name is real** and its enforcer resolves
  (`test_scope_reduction_trap.py::test_the_two_planner_twins_stay_byte_identical`).

### Coverage

**Covered, with falsifiable citations**: the three sources' accepted text
including all revision rounds and Decisions; every numeric claim in the plan,
re-measured from tracked files under the canonical interpreter with the method
stated above; the phase-1 dead-trigger claim, checked against `f654dc0` and
against the corpus at three commits; Chunk B's placement, checked by opening
both AGENTS copies and the slot boundaries; Chunk C and D acceptance criteria,
checked for judgeability against the artifacts they would be judged on
(`gate_manifest.json`, the twin tests, `test_comprehension_floor.py`);
sequencing and fences; the Boundary B bounding argument against `AGENTS.md`'s
refusal rule; `dev/PLANNING.md` for the promised tracked items.

**Not covered / low confidence**: (1) I did **not** run the suite or
`--collect-only` — every node-id figure comes from the committed manifest and
from `ast`, so a divergence between manifest and live collection would not have
surfaced here. (2) I did not read all 265 tag sites; the cost split
(cheap/expensive) remains unmeasured, as the proposal itself warned, and F1/F2
are about the *bounds*, not about which sites need rewriting. (3) Whether the
gate manifest's pinned node ids are load-bearing outside a ceremony window is
inferred from `_gate_manifest.py`'s docstring and the re-anchor runbook, not
from executing the verifier — F4/F5 ask the author to settle it, and I may be
overstating the consequence. (4) The bare-tag population (F1) is measured by
pattern with lint codes excluded by denylist; individual members may be domain
vocabulary rather than finding tags, which is part of why the definition is
owed.

## Code review

*Filled in after implementation commits land.*

## Lasting-truth migration

*Filled in at archive time.*
