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
| tags proposal | The finding-tag revision pass — **see "What counts as a tag" below**; the plan's earlier "262 sites" was one form of three |
| names proposal | Coordinate-named test containers renamed, bodies untouched — **36 by the matching rule stated in Chunk D** |
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
  generated output, or fixture data. **The count is not pinned here** — the
  plan's earlier "~8" was wrong by roughly 5×, and the review measured 42 by a
  different pattern than mine returns. Two greps disagreeing is the signal that
  this class is *not* mechanically separable from docstrings, so the fence is
  stated as a **property the implementer applies per file**: a string addressed
  to a parser is out; prose addressed to a reader is in. Concentrations to
  expect: `test_transition_lint.py`, `test_byline_identity.py`, and both
  planner twins' emitted template strings.
* **No `doctrine/` change beyond Anchor 16.** The operational rules live in
  `AGENTS.md`; no second doctrine home is created.

### What counts as a tag — the definition the plan owed

The review's first finding is that "tag" was never defined, and that every count
in the opened plan was of **bracketed** forms only. That is right, and it
matters: `FUR5` — the Maintainer's raising quote, and *both* worked examples in
the accepted proposal — is **bare**, and appeared in none of the plan's sites.

Measured `as_of 2026-08-13`, three classes:

| Class | Form | Count | Mechanically findable? |
|---|---|---:|---|
| 1 | bracketed — `[S1]`, `[M2-1]`, `[R2-E1]` | **346** | yes |
| 2 | bare, distinctive prefix — `FUR5`, `CF9` | **145** | yes |
| 3 | bare, single letter + digit — `S1`, `C4` in running prose | **not enumerable** | **no** |

**Class 3 is why this plan cannot carry one number.** A grep for `\b[A-Z][0-9]\b`
returns **5194** matches, overwhelmingly ordinary identifiers and variables. The
class is real — it is the same failure — but it is found only by reading, which
is what the accepted proposal already requires and what the no-sweep fence
already says.

**Implementer's rule**: classes 1 and 2 are enumerable and must all be cleared —
**491 sites**. Class 3 is cleared opportunistically *within each file already
being read*, and is not a completion criterion, because no one can enumerate it.

**No accepted outcome changes.** The proposal's rule was always "comments explain
the code, not the process", and its own examples were class 2. What was wrong was
the plan's size estimate, not its scope.

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
| A3 | `doctrine/rationale.md` | The grounding citation, which the opened plan dropped (F9): Naur, P. (1985). *Programming as theory building.* Microprocessing and Microprogramming, 15(5), 253–261. doi:10.1016/0165-6074(85)90032-8 — verified independently at Round 2 of the source proposal, not taken on a reviewer's confirmation. |

**Acceptance**: Anchor 16 carries both; Anchor 17 is named *in* the extension,
not only cross-referenced; `check_cairn.py` resolves every reference.

### Chunk B -- the two conventions

| # | File | Change |
|---|------|--------|
| B1 | `AGENTS.md` | Beside `**Naming.**`: tests are named for the property they pin; the docstring carries the *reason*, not the finding id. Includes the worked docstring example the names review required — **stating why the obligation exists and naming no coordinate**. |
| B2 | `AGENTS.md` | Beside B1: comments and docstrings explain the code, not the process. State the reason; do not cite the finding. |
| B3 | `templates/core/AGENTS.md` | B1 + B2, adopter-general wording, **immediately above `## Project-specific conventions` and outside every `cairn:slot`** — see the placement note. |
| B4 | `AGENTS.md` ×2 | A one-line pointer from the comprehension-floor paragraph to the conventions, so the derivation stays visible from the other direction. |

**Placement note (plan review F3).** The accepted proposals say "beside
`**Naming.**`". In Cairn's own `AGENTS.md` that paragraph sits **inside** the
`cairn:slot project-conventions` block (`AGENTS.md:414`). The shipped copy has
**no `**Naming.**` paragraph at all** — that same slot ships as an *unfilled
placeholder* telling the adopter to write their own conventions
(`templates/core/AGENTS.md:390-396`).

So the literal placement is impossible in the shipped copy, and taking it would
write Cairn-authored universal rules into **adopter-owned space**, where they
would collide at install and misrepresent whose rules they are.

Both rules therefore land **immediately above `## Project-specific conventions`,
outside every slot**, in both copies — so an adopter filling their own slot meets
the universal rule directly above it, and Cairn's project-specific `**Naming.**`
stays where it belongs, inside the slot. **Scope delta: preserved** — the
accepted outcome is that a code-authoring agent finds the rule in the conventions
region rather than under `## Review`, and this delivers it; only the anchor
moves, forced by a fact the proposals did not have.

**Acceptance**: both rules present in both copies, in the conventions region,
**outside every `cairn:slot`**, and **not** under `## Review`; the shipped copy
carries no Cairn-only token (`test_installed_operational_rule_is_project_general`
still bites); the worked example contains no finding tag — the names review
supplied one that did, and it is rejected here on the accepted terms.

### Chunk C -- the finding-tag revision pass

262 sites, less ~8 fenced. Revised **by reading**, one file at a time.

| # | Files | Notes |
|---|------|--------|
| C1 | `bootstrap/tests/_gate_preflight.py`, `bootstrap/tests/test_gate_preflight.py` | **97 sites** — the orphaned set. Largest and first, because they have no other home. |
| C2 | `tools/lifecycle_planner.py` + twin | **25 each** (F6 — the opened plan said ~21). **Twins must stay byte-identical.** |
| C2b | every other byte-identical twin pair | Named rather than assumed (F6): `tools/lifecycle.py` ↔ `templates/skills/_lib/lifecycle.py` (17 sites), plus any remaining `tools/` ↔ `templates/skills/_lib/` pair. Parity is enforced by `bootstrap/tests/test_lifecycle_brief.py`; edit both or neither. |
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

| # | File | Change |
|---|------|--------|
| D1 | `bootstrap/tests/*.py` | The renames. **36** containers by the matching rule below. |
| D2 | `bootstrap/tests/fixtures/gate_manifest.json` | **Regenerate.** It pins **356** node ids naming classes this chunk renames (measured 2026-08-13; regenerated as recently as `cfaace9`). The opened plan named neither the file nor a disposition. |

**Matching rule (F7)**: a container is in scope when its name matches
`^class Test[A-Za-z]*(P|C|M|R|E|CF|D|S)[0-9]` — a plan or finding coordinate
embedded in the class name. **36** as of 2026-08-13. Classes whose names merely
*contain* a digit are out; the rule is the coordinate prefix, not the digit.

**Acceptance (F4, corrected)**: the opened plan said "collected node ids
unchanged", which **cannot pass** — renaming a class changes its node ids by
definition. The criterion is:

* the **pass/fail/skip set is unchanged** in count and in outcome per test;
* every node id in `gate_manifest.json` resolves after regeneration, with no
  orphans;
* no test body is edited.

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

**Boundary B mode**: **full**, and not by preference — **the fence refuses.**

The opened plan argued `bounded` on the grounds that no contract surface is
touched. **That was false and the review falsified it on the plan's own terms.**
Chunk D regenerates `bootstrap/tests/fixtures/gate_manifest.json`, and
`AGENTS.md` names the gate manifest as part of the install contract — a contract
surface, where bounded mode refuses outright.

Worse, the opened plan wrote its falsification as a *discovery* condition
("if Chunk C's reading turns up..."), when the disqualifying fact was knowable
at plan-open by reading the chunk list against the fence. A condition that waits
to be discovered is not a fence.

So: **one full-suite Boundary B run** after the final implementation commit, on
a clean unchanged commit under the canonical interpreter with
`PYTHONDONTWRITEBYTECODE=1`. This is the first time the clause has refused a
bounded claim, which is what it is for.

**Standing gates mapped for Chunks A and B (F8)**, which the opened plan omitted:
`bootstrap/tests/test_comprehension_floor.py` (Chunk A edits the anchor it pins)
and `python scripts/quality_gate.py --sub neutrality --sub redundancy` (Chunk B
edits `templates/core/AGENTS.md`, a neutrality surface).

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

## Response to plan review -- Claude -- 2026-08-13

**All nine accepted. None rejected, none deferred.** The review's own summary is
the fair reading: the plan's *design* is a faithful translation — nothing added,
nothing dropped — and what failed is the layer a plan review exists to check.
That is the tier working, and it is worth saying plainly that a plan I described
as "complete" was wrong on five substantive points.

| | Disposition |
|---|---|
| **F1** | accept — "tag" is now defined in three classes, with the honest consequence. |
| **F2** | accept — the fence is a property, not a number. |
| **F3** | accept — the named placement does not exist; corrected. |
| **F4** | accept — a contract-surface file was missing and the criterion was impossible. |
| **F5** | accept — the bounding is falsified; Boundary B is now **full**. |
| **F6-F9** | accept — counts, twin pairs, matching rule, gate mapping, citation. |

**[F1] is the finding of this round.** Every count I published was of *bracketed*
tags. `FUR5` — the Maintainer's raising quote and **both** worked examples in the
accepted proposal — is bare, and appeared in none of my 97 sites. I measured the
form I had noticed rather than the thing the rule is about.

Re-measuring produced something better than a bigger number: **three classes**,
of which the third is **not mechanically enumerable** — `\b[A-Z][0-9]\b` returns
**5194** matches, almost all ordinary identifiers. So the plan cannot carry one
completion figure, and pretending otherwise would have handed the implementer a
false target. Classes 1 and 2 are enumerable at **491 sites** and must all clear;
class 3 is cleared within files already being read. No accepted outcome changes.

**[F4] and [F5] together are the more serious pair.** `gate_manifest.json` pins
**356** node ids naming classes Chunk D renames, and `AGENTS.md` lists the gate
manifest in the install contract. So the plan (a) omitted a file that must be
regenerated, and (b) claimed a bounded Boundary B on the explicit ground that no
contract surface is touched.

**Boundary B is now `full`, because the fence refuses** — not because I prefer
it. This is the first time the bounding clause has refused a claim, and it
refused mine, three days after I implemented it. The clause's own words are
`uncertainty resolves to full`, and there was not even uncertainty here: the fact
was knowable at plan-open by reading the chunk list against the fence. I had also
written the falsification as a *discovery* condition, which is not a fence at
all.

**[F3] is the one where the accepted text could not be followed literally.** Both
proposals say "beside `**Naming.**`". The shipped `AGENTS.md` has no such
paragraph — that slot ships as an unfilled placeholder for the adopter's own
conventions, and Cairn's `**Naming.**` sits *inside* it. Following the letter
would write Cairn-authored universal rules into adopter-owned space. Both rules
now land immediately above `## Project-specific conventions`, outside every slot,
in both copies. **Scope delta: preserved** — the accepted outcome is that a
code-authoring agent finds the rule in the conventions region instead of under
`## Review`; only the anchor moves.

**What I did not do**: raise the parity guard, reopen any accepted decision, or
treat the review's "no accepted outcome added or dropped" as licence to relax.

**Status returns to `awaiting-plan-review`.** Clearing the floor is the
reviewer's move, not mine.

## Plan review -- Claude Opus 5 (Internal) -- 2026-08-13 (round 2)

**Tier**: Internal
**Findings**: raised
**Model**: Claude Opus 5 (`claude-opus-5`)

**Reviewed commit**: `3a407d4ca541d144e31d92e081d83508e172a056`
**Basis**: the response and revision at `3a407d4`, re-measured from **blobs at
that commit** (`git show 3a407d4:<path>`) rather than the working tree — three
`.py` files are dirty under another agent's claim, including both planner twins.
**Verdict: REVISE** — six findings, two of them load-bearing. Four of the nine
round-1 findings are now **fully satisfied** and are recorded as closed below.
F4 and F5 are answered in substance. **F1 is not**: the definition the plan owed
has arrived, and it is the right shape, but its two enumerable counts do not
reproduce and its non-enumerable class is dismissed on a claim the measurement
contradicts.

I am aware this is a second block on a plan whose start precondition is unmet,
and I have kept the findings to what would change the implementer's behaviour.

### Round-1 findings: closed

* **F5 — closed, and correctly reasoned.** I checked the derivation, not the
  conclusion. Chunk D now regenerates `bootstrap/tests/fixtures/gate_manifest.json`
  (D2); `AGENTS.md` names the gate manifest in the install contract; the fence's
  words are *"bounded mode refuses … whenever the change touches a contract
  surface"*. So `full` is compelled, not chosen — and the plan says so in those
  terms. The added observation that a *discovery* condition is not a fence is
  the right generalisation. One residue: the run is described as "one full-suite
  Boundary B run" without naming the commands; `AGENTS.md`'s canonical pair
  (`python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0`, then
  `python scripts/quality_gate.py --sub neutrality --sub redundancy`) should be
  written into the plan so the evidence record has a target.
* **F8 — closed.** `test_comprehension_floor.py` and the neutrality/redundancy
  gates are mapped for Chunks A and B.
* **F9 — closed.** A3 restores the Naur citation with its DOI.
* **F2 — closed as accepted.** A per-file property is the right form; two
  patterns disagreeing (my 42, yours 24) is a fair signal that the class boundary
  is semantic. For the record, a number *is* partially recoverable — by
  `tokenize`, class-1 tags in non-docstring string literals are exactly 42 and
  class-2 are 7 — but tokenizing separates *string literal from docstring*, not
  *parser-addressed from reader-addressed*, which is the distinction the fence
  actually draws. The property stands.
* **F3 — the `Scope delta: preserved` declaration survives my attack**, with one
  correction below (R2-F6). I tried to break it and could not: the accepted
  satisfier is the tags review's E3, whose own words are *"Place the rule under
  code-authoring / development conventions in `AGENTS.md` (e.g. alongside
  `**Naming.**` **or project conventions**)"* — the anchor was offered as an
  example with an alternative, not as the outcome. The outcome is *a
  code-authoring agent finds the rule where they are working, not under
  `## Review`*, and that is delivered. The shipped-copy fact (no `**Naming.**`
  exists; the slot is adopter-owned) genuinely forbids the literal reading, and
  the plan states the fact rather than asserting equivalence. **Preserved is
  earned here.**

### Findings

**[R2-F1 — major] The 491 figure does not reproduce, and class 2 is understated
by roughly half.**

Measured at `3a407d4` over `git ls-files '*.py'` (248 files), classified by
`tokenize` + `ast`:

| Class | Plan | Measured (comments + docstrings) | Measured (all tokens) |
|---|---:|---:|---:|
| 1 — bracketed | **346** | 222 narrow / **260** widest | 265 narrow / **309** widest |
| 2 — bare, ≥2-letter prefix, lint codes excluded | **145** | **322** | **347** |
| 1 + 2 | **491** | **544–582** | 612 |

Class 2 is the serious half: the plan's 145 is less than half the 322 I measure
in the surface the rule governs. The top contributors are not exotic — `CR1`
(39), `CR2` (25), `SR1` (22), `RV5` (22), `CR3` (14), `SR6` (12), `FUR5` (12).
An implementer holding 491 as the completion target will believe they are done
with roughly 150 class-2 sites still standing.

Class 1's 346 is wrong in the other direction, and the likely cause is the one
named in round 1: **346 is unreachable from tracked files under any bracket
pattern I try** (max 311), but scanning the whole tree *including the untracked
`.claude/worktrees/` copies* gives 329 narrow / 368 wide / 375 widest. If that is
what happened, the headline figure of this revision is contaminated by stale
worktree duplicates.

*Required satisfier*: re-measure both classes against tracked files only, state
the pattern and the token-class restriction, and correct 491.

**[R2-F2 — major] "Class 3 is not mechanically enumerable" is not supported by
the measurement, and its disposition re-creates the failure Round 3 of the
accepted proposal corrected.**

The claim rests on `\b[A-Z][0-9]\b` returning 5194 matches *"overwhelmingly
ordinary identifiers and variables"*. Restricted to the surface the rule governs,
that is not what the corpus says:

* **2679** matches in comments and docstrings, across **170** files;
* **136** in string literals;
* **35** in code tokens — total, tree-wide.

So the false-positive population the argument rests on is **35 occurrences**, not
a swamp. The matches are also not ambiguous on inspection — sampled from files
the plan would never open: `"""Tests for api-web-security-modules Chunk F, row
**F5**"""`, `# T1 -- corpus regression`,
`# X4 (External review): Codex deleted the reviewer-duty …`,
`# D7 (clearing pass): C9 added the floor rule …`,
`# R2-E1 again. The code review (C3) rewrote this module …`
(`bootstrap/tests/test_scope_reduction_trap.py:106` and `:143`). A real minority is
genuine domain vocabulary — `R1`/`R6` in `scripts/quality_gate.py:31-33` are the
redundancy gate's own rule ids — but separating those is *reading*, which the
plan already requires for classes 1 and 2 and which the no-sweep fence already
governs. **"Needs a read" is not "not enumerable".** The honest statement is
*2679 candidate sites, decided by reading* — which is a number, and a large one.

The consequence is what makes this major rather than pedantic. The plan's rule is
*"class 3 is cleared opportunistically within each file already being read"*.
Measured against that rule:

* **105 files carrying 657 class-3 occurrences contain no class-1 or class-2
  tag at all**, so they are never opened and never cleared — among them
  `test_security_capability_install.py` (33), `test_lifecycle_stage_patterns.py`
  (29), `_intent/conflict.py` ×2 (27 each), `bootstrap/_scaffold/cli.py` (19).
* In the files that *are* opened, class 3 adds **2022** further sites with no
  criterion, no estimate and no budget. `tools/lifecycle_planner.py` alone
  carries **376** class-3 occurrences against its 29 class-1/2 sites — the
  chunk sized at "25 each" contains thirteen times that in the class the plan
  declines to count.

That first bullet is, structurally, the thing the accepted proposal's Round 3
already caught and fixed in itself:

> *"A file nobody touches again keeps its tags permanently. … The difference is
> invisible because it never fails — it just never finishes."*

Round 3 rejected exactly this shape as a `dev/PLANNING.md` revival condition. The
revision re-introduces it inside the plan, one class down, and calls it "not a
completion criterion".

*Required satisfier*: either (a) publish the class-3 candidate count and a
disposition that finishes — the files needing a read, enumerated, with the
reading itself as the acceptance bar; or (b) declare it a **scope boundary**,
with the count stated, and take it to the Maintainer for an explicit allowance.
The plan may not settle this by declaring the remainder unmeasurable: it is
measured above, and `AGENTS.md` is explicit that narrowing which the wider
version never gets built cannot be shown wrong.

**[R2-F3 — moderate] D2 regenerates a Maintainer-authored ceremony artifact, with
no fence.**

Accepting the file was right. But `bootstrap/tests/fixtures/gate_manifest.json`
is not an ordinary fixture: `bootstrap/REANCHOR_RUNBOOK.md:734-749` makes
`_gate_manifest.py produce` **step 2** of a supervised ceremony whose step 3 is
*"a supervised, **Maintainer-authored** commit containing the new
`gate_manifest.json`"*, and the value of the pin is that it is *"a reviewed pin
and not a self-generated one"*. D2 says "Regenerate" inside an ordinary
implementation chunk with no `MAINTAINER-GATED` marking and no reference to the
runbook. This is the same shape as the AST-baseline pitfall `AGENTS.md` already
warns about, where self-service repair reaches only a named allowlist and
anything else is Maintainer-run.

*Required satisfier*: mark D2 MAINTAINER-GATED and cite the runbook, or record
the Maintainer's explicit position that an out-of-ceremony regeneration is
acceptable here and how it gets re-anchored.

**[R2-F4 — moderate] The container matching rule misses the most literal
coordinates and sweeps in domain vocabulary; 356 does not reproduce.**

The rule `^class Test[A-Za-z]*(P|C|M|R|E|CF|D|S)[0-9]` yields exactly **36** —
reproducible, and stating it was the right response to F7. But:

* It **excludes the four `TestChunkG*` classes** —
  `TestChunkGArgvVectorValidation`, `TestChunkGDeclaredCapabilitySet`,
  `TestChunkGRealFacadeThroughRealDispatcher`, `TestChunkGRegistryShape` — whose
  names contain the word *Chunk* followed by the chunk letter. The accepted
  proposal's subject is names carrying *"the plan chunk or review finding that
  produced them"*; these are the least deniable instances in the tree, and the
  rule as written is blind to them because the coordinate has no digit.
* It **includes** `TestR1Shingles`, `TestR6UnusedDef` and
  `TestTheR6PredicateIsShared`, where `R1` and `R6` are the redundancy gate's own
  published rule ids (`scripts/quality_gate.py:31-33`, *"redundancy (G R1 + R6)"*).
  Round 1 flagged these by name; the response did not dispose of them, and the
  rule now sweeps them in silently. Renaming them *loses* meaning.
* **356 node ids does not reproduce.** Against the plan's own 36-class set the
  manifest yields **326**; against my round-1 40-class set, 349; against the
  union, 353. No reading gives 356.

*Required satisfier*: extend the rule to word-coordinates (`Chunk<X>`), exclude
the redundancy-gate trio explicitly with the reason, and re-derive the manifest
figure from the final class list.

**[R2-F5 — moderate] The chunk sizing was not carried onto the new definition —
three rows, three different definitions.**

The plan now defines a tag in three classes, then sizes its chunks on the old
one:

| Row | Plan says | Measured at `3a407d4` (comments + docstrings) |
|---|---|---|
| C1, the two `_gate_preflight` files | **97 sites** | class 1 = 102, class 2 = 101, **class 1+2 = 203**; 97 was the *bracketed-only* count |
| C2, planner twins | **25 each** | class 1 = 24, **class 1+2 = 29**, narrow-bracketed = 14 |
| C2b, `lifecycle.py` twins | **17 sites** | narrow-bracketed = 17, **class 1+2 = 25** |

C1 is still on the round-1 definition the response repudiated; C2b is on the
narrow bracketed pattern; C2's 25 matches no pattern I can construct for the
planner twins, though it is exactly the class-1+2 figure for the *`lifecycle.py`*
twins one row below — which suggests the two rows' figures were transposed. The
"A correction the plan must carry" section likewise still reads *"**97** tags
across …"*.

*Required satisfier*: restate every per-chunk figure in the definition's own
terms, or drop the per-chunk numbers and keep only the definition plus the
per-file acceptance property.

**[R2-F6 — minor] "Immediately above `## Project-specific conventions`" is inside
the previous section.**

Markdown has no headless region between two H2s: text placed immediately above
`## Project-specific conventions` belongs to `## Documentation discipline` — in
the shipped copy that is right after `<!-- cairn:end documentation-discipline -->`
(`templates/core/AGENTS.md:374-388`), and in Cairn's copy after the same marker
(`AGENTS.md:410-412`). So B3's placement satisfies "outside every slot" and
fails Chunk B's own acceptance criterion, *"in the conventions region"*. An
agent scanning headings for conventions finds the section and not the rules.

The fix is one line and keeps everything the response wanted: place both rules
**under the `## Project-specific conventions` heading and above the
`<!-- cairn:slot project-conventions -->` opener**. That is inside the conventions
region, outside every slot, above the adopter's own space rather than in it, and
in Cairn's copy it puts them directly above `**Naming.**` — as close to the
accepted text's letter as the file allows.

### Coverage

**Covered, with falsifiable citations**: all three tag classes re-measured from
blobs at `3a407d4` by `tokenize` + `ast`, reported per token class so the figures
are separable; the class-3 enumerability claim tested directly, including the
false-positive population and a sample from the never-opened files; the reachable
/ unreachable file split under the plan's own opportunistic rule; the container
matching rule executed as written, with its inclusions and exclusions listed and
the manifest recount done against the plan's own class set; the per-chunk figures
recomputed per file; the F5 bounding derivation checked against the fence's text
rather than its conclusion; the F3 `Scope delta` declaration tested against the
accepted satisfier's own wording; B3's placement checked against both files'
actual section and slot boundaries; D2's authority checked against
`REANCHOR_RUNBOOK.md`.

**Not covered / low confidence**: (1) I still have not run the suite or
`--collect-only` — node-id figures come from the committed manifest and `ast`.
(2) The class-2 lint denylist is hand-built; a few of its 347 may be tool codes I
did not recognise, which would move the figure by single digits, not by the ~180
that separates it from 145. (3) Whether each of the 2679 class-3 candidates is a
coordinate or domain vocabulary is a semantic judgement I sampled rather than
enumerated — my claim is that the *candidate set* is enumerable and the sample is
dominated by coordinates, not that all 2679 need rewriting. (4) I have not
verified that `_gate_manifest.py produce` is refused outside a ceremony, only
that the runbook assigns the commit to the Maintainer.

