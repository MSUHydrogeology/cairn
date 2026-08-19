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

**Status**: ready-to-implement
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
| tags proposal | The finding-tag revision pass — **see "What counts as a tag" below**; **179 files, 3258 candidate sites** across three classes. The plan's earlier "262 sites" and its round-1 correction to "491" were both one form of three |
| names proposal | Coordinate-named test containers renamed, bodies untouched — **38 by the matching rule stated in Chunk D** |
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

**Measurement method** (round 2, R2-F1/R2-F2 — every figure below is
reproducible from this): tracked `*.py` only (`git ls-files '*.py'`, 247 files),
read from **blobs at the measured commit** (`git show <rev>:<path>`) because the
working tree carries another agent's uncommitted work; classified with
`tokenize` + `ast` so **comments and docstrings** — the surface the rule governs
— are separated from string literals and code tokens. Patterns:

```
class 1   \[([A-Z]{1,4}\d+(?:[-–][A-Z]{0,4}\d+)?)\]
class 2   (?<![\[\w-])([A-Z]{2,4}\d+)(?![\w\]-])      minus a lint denylist
class 3   (?<![\[\w-])([A-Z]\d)(?![\w\]-])
```

Measured `as_of 2026-08-13` at `eb2692e`:

| Class | Form | Comments + docstrings | In string literals | In code tokens |
|---|---|---:|---:|---:|
| 1 | bracketed — `[S1]`, `[M2-1]`, `[R2-E1]` | **255** | 36 | 1 |
| 2 | bare, ≥2-letter prefix — `FUR5`, `CR1` | **324** | 11 | 20 |
| 3 | bare, single letter + digit — `F5`, `D7`, `T1` | **2679** | 136 | **35** |

Class 2 is net of a lint denylist: the gross 508 includes `PLC0415` (162),
`BLE001` (20), `SLF001` (1) and `ARG002` (1) — Ruff codes, not coordinates.
**The denylist applies to every class-2 figure in this plan, aggregate and
per-chunk alike** — the defect R3-F1 found, and R4-F1 found again one row down.

**Method note on the "in code tokens" column.** Those figures (1 / 20 / 35) are a
**residual** — whole-file raw matches minus the tokenized comment/docstring and
string-literal surfaces — not a direct count of code tokens. They are reported to
size the false-positive population, which is what the class-3 argument turns on;
they are not used as a completion target anywhere.

**The opened plan's `491` was wrong in both halves, and is withdrawn.** Class 1's
`346` is unreachable from tracked files under any bracket pattern; it was
contaminated by untracked `.claude/worktrees/` duplicates, which the round-1
review had already warned about and this revision reproduced in its headline
figure. Class 2's `145` was under half the true 324. The corrected enumerable
total is **579**.

**Class 3 is enumerable, and the claim that it was not is withdrawn.** The
argument rested on `\b[A-Z][0-9]\b` returning 5194 matches "overwhelmingly
ordinary identifiers" — but that grep counts *code*, and the rule does not govern
code. Restricted to the surface it does govern, the false-positive population is
**35 occurrences tree-wide**, not a swamp. Sampled matches are unambiguous
coordinates (`# T1 -- corpus regression`, `# X4 (External review)`,
`# D7 (clearing pass): C9 added ...`). **"Needs a read" is not "not
enumerable"** — reading is what this plan already requires for classes 1 and 2.

**Why that mattered more than the arithmetic.** The withdrawn rule was *"class 3
is cleared opportunistically within each file already being read, and is not a
completion criterion."* Measured against the corpus, that rule leaves **103 files
carrying 603 class-3 occurrences never opened at all** (they hold no class-1 or
class-2 tag), and adds **2143 further sites with no criterion** inside the files
that are opened. `tools/lifecycle_planner.py` alone carries **376** class-3
against the 29 class-1/2 sites that put it in scope.

That is, structurally, the shape the accepted proposal's own Round 3 identified
and rejected — *"A file nobody touches again keeps its tags permanently. … The
difference is invisible because it never fails — it just never finishes."* The
revision re-introduced it one class down and relabelled it. It is corrected here
rather than defended.

**Implementer's rule (corrected).** All three classes are in scope and the pass
**finishes against an enumerated file set**, not against a tag count:

* **179 files** carry at least one tag of any class (76 hold a class-1/2 tag;
  103 hold class-3 only). That set is the unit of
  completion; it is regenerated at implementation time by the script above and
  pinned in the implementation record.
* **Per file, the acceptance is the read**: every candidate in the file has been
  looked at and dispositioned — rewritten to state its reason, or **kept**
  because it is not a coordinate (gate rule ids, domain vocabulary).

  **Where a keep is recorded, and how much gets written (R3-F3).** A rewrite
  evidences itself in the diff; a keep leaves the file byte-identical, so
  without a named artifact the bar has an invisible failure state and cannot be
  failed. Since most of the 2679 class-3 candidates are expected to be *kept*,
  that would put the majority of this plan's newly-claimed scope behind an
  unfalsifiable criterion — which is the same defect as the withdrawn
  opportunistic rule wearing better clothes.

  So: keeps are recorded in **`dev/measurement/tag-pass-dispositions.md`**, one
  line per kept **token per file** — `<path> :: <token> :: <reason>` — created by
  this chunk. **Bounded to the kept minority**: rewrites are not listed there,
  because the diff already carries them. A file is done when every candidate in
  it is either changed in the diff or named in that ledger, and the chunk's
  completion is checkable by that pairing rather than asserted.

  **Who runs the pairing, and over what (R4-F3).** `AGENTS.md` requires a named
  trigger, and "a check whose only trigger is a human remembering is described
  that way". This one is: **the code reviewer, at Boundary C**, over the range
  `<first Chunk C commit>..<last Chunk C commit>`, by re-running the enumeration
  script in the definition above against the pre-pass commit and confirming every
  candidate it lists is either in that diff or in the ledger. **No new machinery,
  no gate, no test** — a human step, stated so it cannot be mistaken for an
  automated one.

  **Granularity, stated because it is not self-evident.** The ledger is one line
  per *token per file*; the scope figures count *occurrences*. A token appearing
  four times in one file is one ledger line and four occurrences. That is
  deliberate — the reason for keeping `R6` in a file is one judgement, not four —
  but it means **ledger lines will not reconcile to 3258**, and a reviewer
  checking by arithmetic rather than by the pairing will read a shortfall that
  is not one.
* **The rewrite count is not a target.** A real minority of class-3 candidates
  are genuine domain vocabulary — `R1`/`R6` in `scripts/quality_gate.py:31-33`
  are the redundancy gate's own published rule ids — and those stay. Separating
  them is reading, which the no-sweep fence already governs.

**Total candidate sites: 3258** (255 + 324 + 2679) across **179 files**. This is
roughly **6.6×** the withdrawn 491, and the plan states it rather than sizing
itself on the number it can most easily defend.

**No accepted outcome changes, and none is narrowed.** The proposal's rule was
always "comments explain the code, not the process". What was wrong was the
plan's measurement and the disposition it built on that measurement — not the
scope. **Scope delta: preserved** — the correction moves in the direction of
*more* delivered work, and the class the plan had excused itself from is now
inside the completion criterion.

### A correction the plan must carry: phase 1's trigger is already dead

The tags proposal routes the `_gate_preflight` sites through *"their security
plan's closure"*. **That plan archived at `f654dc0` without clearing them.**
Re-measured `as_of 2026-08-13` at `eb2692e` on the definition above: **203**
class-1/2 tags (78 + 125) plus **64** class-3 candidates across
`bootstrap/tests/_gate_preflight.py` and `bootstrap/tests/test_gate_preflight.py`.
(The opened plan's **97** was the bracketed-only count under the definition this
revision withdrew; R2-F5.)

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
| B3 | `templates/core/AGENTS.md` | B1 + B2, adopter-general wording, **under the `## Project-specific conventions` heading and above the `<!-- cairn:slot project-conventions -->` opener** — see the placement note. |
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

**Corrected placement (R2-F6).** The opened revision said *"immediately above
`## Project-specific conventions`"*. That is inside the **previous** section:
Markdown has no headless region between two H2s, so text above the heading
belongs to `## Documentation discipline`, and B3 would have failed Chunk B's own
acceptance criterion (*"in the conventions region"*) while satisfying its slot
constraint. Verified in both copies — one blank line separates the heading from
the slot opener (`templates/core/AGENTS.md:388` / `:390`; `AGENTS.md:412` / `:414`, measured at `eb2692e`).

Both rules therefore land **under the `## Project-specific conventions` heading
and above the `<!-- cairn:slot project-conventions -->` opener**, in both copies.
That is inside the conventions region, outside every slot, and directly above the
adopter's own space rather than in it — and in Cairn's copy it puts them
immediately above `**Naming.**` (`AGENTS.md:415` at `eb2692e`), which is as close to the
accepted text's letter as the file permits.

**Scope delta: preserved** — the accepted outcome is that a code-authoring agent
finds the rule in the conventions region rather than under `## Review`, and this
delivers it; only the anchor moves, forced by a fact the proposals did not have.
The round-2 review attacked this declaration directly and it held: the tags
review's E3 offered the anchor as *"alongside `**Naming.**` **or project
conventions**"* — an example with an alternative, not the outcome.

**Acceptance**: both rules present in both copies, in the conventions region,
**outside every `cairn:slot`**, and **not** under `## Review`; the shipped copy
carries no Cairn-only token (`test_installed_operational_rule_is_project_general`
still bites); the worked example contains no finding tag — the names review
supplied one that did, and it is rejected here on the accepted terms.

### Chunk C -- the finding-tag revision pass

**179 files, 3258 candidate sites** across all three classes (see the definition
above), less the fenced string literals. Revised **by reading**, one file at a
time. **The file set is the unit of completion, not the site count** — every
figure below is per file on the corrected definition, and every row states all
three classes so no row is sized on a definition the plan has withdrawn (R2-F5).

| # | Files | class 1+2 | class 3 | Notes |
|---|------|---:|---:|--------|
| C1 | `bootstrap/tests/_gate_preflight.py` (78) + `bootstrap/tests/test_gate_preflight.py` (125) | **203** | 64 | The orphaned set. First, because they have no other home. **203 not 205** (R4-F1): `_gate_preflight.py`'s 39 gross class-2 include two `PLC0415`, which the denylist removes. |
| C2 | `tools/lifecycle_planner.py` + twin | **29** each | **376** each | The opened plan said 25; that figure matched no pattern for these files. **Twins must stay byte-identical**, and class 3 here is 13× the class-1/2 count. |
| C2b | `tools/lifecycle.py` ↔ `templates/skills/_lib/lifecycle.py` | **25** each | 55 each | The opened plan's 17 was the narrow bracketed count. Parity enforced by `bootstrap/tests/test_lifecycle_brief.py`; edit both or neither. |
| C2c | **the other 26 byte-identical pairs** — see the parity note below | **132** per side, all classes | — | R4-F2. The clause this replaces ("any remaining `tools/` ↔ `templates/skills/_lib/` pair") resolved to the **empty set**. |
| C3 | the **103 files carrying class-3 only** | 0 | **603** | *These were unreachable under the withdrawn rule.* Largest: `test_security_capability_install.py` (33), `test_lifecycle_stage_patterns.py` (29), `test_scope_reduction_trap.py` (28), `run_security_verification.py` (25). |
| C4 | the remainder of the 179 | — | — | By file, smallest last. |

**Parity note — the twin set is 28 pairs, not 2 (R4-F2).** The opened C2b closed
with *"plus any remaining `tools/` ↔ `templates/skills/_lib/` pair"*. Those two
directories contain **exactly the two pairs already named**, so the clause
resolved to the empty set and looked like coverage while adding none. Measured at
`eb2692e` by blob sha over tracked `*.py`: **44 byte-identical groups**, of which
**26 carry candidates and lie outside the named pairs** — 132 sites per side.
Largest: `_intent/conflict.py` (28), `run_portable_security_sweeps.py` (13),
`_onboarding/triggers.py` (10), `content_scan.py` (8), `claim_check.py` (7).

**One of them is a high-risk surface.** `scripts/run_portable_security_sweeps.py`
↔ `templates/modules/team-gated/run_portable_security_sweeps.py` is named in
`AGENTS.md` as an executable trust root **kept byte-identical**. Editing a comment
on one side breaks that property. The rule for all 28 pairs is the same and
non-negotiable: **edit both sides or neither**, in the same commit. The pair set
is regenerated at implementation time by blob sha, not carried from this list.

**Acceptance per file**: every candidate of every class has been read and
dispositioned — rewritten to state its reason, or left in place with the reason
recorded for why it is not a coordinate; no undispositioned candidate remains;
the suite's pass/fail set is unchanged.

**Acceptance for the chunk**: all 179 files dispositioned — every candidate
either changed in the diff or named in `dev/measurement/tag-pass-dispositions.md`
with its reason. **The 179 and the C3 row's 103/603 are regenerated at
implementation time** by the script in the definition above and pinned in the
implementation record; they are the figure as measured at `eb2692e`, not a
contract. "Finished" is checkable against that regenerated list plus the ledger
pairing, not asserted.

**Coordination**: `_gate_preflight` and the planner twins are high-traffic. Claim
work-intent per file, and check the active claim set immediately before each
commit — this tree has produced two in-file collisions in three days.

### Chunk D -- the test-container rename

**38 classes** (re-measured `as_of 2026-08-13` at `eb2692e`), bodies untouched,
coordinate moved out of the name and the reason stated in the docstring.

The names proposal gated this on `review-efficient-lifecycle` archiving, because
it owns most of the affected classes and renaming another plan's tests mid-flight
is the collision this repository has paid for twice this week. **The start
precondition satisfies that gate for the whole plan**, so no per-chunk deferral
survives — and the `dev/PLANNING.md` revival row the proposal committed to is
no longer owed, because nothing is being deferred.

| # | File | Change |
|---|------|--------|
| D1 | `bootstrap/tests/*.py` | The renames. **38** containers by the matching rule below. |
| D2 | `bootstrap/tests/fixtures/gate_manifest.json` | **MAINTAINER-GATED — regenerate only under the re-anchor ceremony.** It pins **335** node ids naming classes D1 renames -- 326 (the 36 digit-coordinate classes) + 21 (`TestChunkG*`) - 12 (the two excluded gate-rule classes); **18 of the 335 are skip/xfail-marked**. Measured `as_of 2026-08-13` at `eb2692e`. See the fence below. |

**Matching rule (F7, corrected at R2-F4)**: a container is in scope when its name
embeds a plan or finding coordinate —

```
digit coordinate   ^class Test[A-Za-z]*(P|C|M|R|E|CF|D|S)[0-9]      -> 36
word coordinate    ^class Test[A-Za-z]*Chunk[A-Z]                   ->  4
minus gate rule ids (below)                                         -> -2
                                                                    ------
                                                                       38
```

The **word-coordinate arm is new**. The digit rule missed
`TestChunkGArgvVectorValidation`, `TestChunkGDeclaredCapabilitySet`,
`TestChunkGRealFacadeThroughRealDispatcher` and `TestChunkGRegistryShape` —
literally *Chunk* plus the chunk letter, the least deniable instances in the
tree, invisible to a rule that requires a digit.

**Two exclusions, not three.** `TestR1Shingles` and `TestR6UnusedDef`
(`bootstrap/tests/test_quality_gate_redundancy.py`) are out: `R1` and `R6` are
the redundancy gate's own published rule ids (`scripts/quality_gate.py:31-33`,
`489`, `497`), so renaming them *loses* meaning.

The review also asked to exclude `TestTheR6PredicateIsShared`, and **that one is
declined on inspection.** Its docstring quotes a *review finding* — *"R6:
`scan`, `next`, and accepted closeout tooling consume shared predicates"*
(`bootstrap/tests/test_lifecycle_contract.py:4542-4545`) — not the gate rule; the
same is true of `TestR6ContradictionsThroughBothEntryPoints` (`:4211-4217`).
Both are textbook instances of exactly what this plan renames, and excluding them
because their coordinate letter collides with a gate rule id would narrow the
pass by two of its clearest cases. Classes whose names merely *contain* a digit
remain out; the rule is the coordinate, not the digit.

**Fence on D2 (R2-F3).** `gate_manifest.json` is not an ordinary fixture.
`bootstrap/REANCHOR_RUNBOOK.md` makes `_gate_manifest.py produce` **step
2** of a supervised ceremony whose step 3 is *"a supervised, **Maintainer-
authored** commit containing the new `gate_manifest.json`"*, and the runbook is
explicit that confirming the pinned hashes against out-of-band-authorized values
*"is what makes this a reviewed pin and not a self-generated one"*. An
implementing agent regenerating it inside an ordinary chunk would manufacture
precisely the self-generated pin the ceremony exists to prevent — the same shape
as the AST-baseline pitfall `AGENTS.md` already warns about.

**So D2 does not execute without the Maintainer.** The implementing agent stops
at D1, reports the renames and the resulting orphaned node ids, and the
regeneration is the Maintainer's under the runbook. If the Maintainer prefers an
out-of-ceremony regeneration, that is theirs to authorize explicitly and the
authorization is quoted here before D2 runs.

**Acceptance (F4, corrected)**: the opened plan said "collected node ids
unchanged", which **cannot pass** — renaming a class changes its node ids by
definition. The criterion is:

* the **pass/fail/skip set is unchanged** in count and in outcome per test;
* every node id in `gate_manifest.json` resolves after the Maintainer's
  regeneration, with no orphans — **and until that regeneration, the 335 pinned
  ids naming renamed classes are expected to be orphaned.** The implementing
  agent reports that count rather than treating it as a failure;
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

* **Tests that must pass** — no new tests (inherited). The existing suite's
  **pass/fail/skip set** must be unchanged by Chunks C and D, in count and in
  outcome per test. **Node ids are unchanged by Chunk C and change by design in
  Chunk D** — renaming a container changes its node ids by definition, which is
  why "same node ids" cannot be a criterion for D (F4). Chunks A, B and E are
  prose and run the standing gates.
* **Chunk C finishes against a list** — all tagged files dispositioned (**179**
  at `eb2692e`, regenerated at implementation time), every candidate either
  changed in the diff or named with its reason in
  `dev/measurement/tag-pass-dispositions.md`.
* **Doc updates gain one file** — `dev/measurement/tag-pass-dispositions.md`, the
  keep ledger Chunk C creates.
* **Doc updates** — `doctrine/rationale.md`, `AGENTS.md` ×2, `dev/PLANNING.md`.
  No `CHANGELOG.md` entry: no adopter-facing *behaviour* changes; the shipped
  `AGENTS.md` paragraphs are the delivery.
* **Examples / smoke checks** — `python scripts/check_cairn.py` for every chunk;
  `python scripts/claim_check.py` per edited artifact.

### Author-accounting

**N/A on new contracts** — no new public entry point, no executable path, no
parser. Chunks C and D change comments, names and prose only.

**Two** invariants this plan must not break, each with its enforcer (R5-F1 — the
second was missing, which left C2c's executable trust root with no Boundary A
mapping):

* **The planner twins stay byte-identical** (Chunk C2), enforced by
  `bootstrap/tests/test_scope_reduction_trap.py::test_the_two_planner_twins_stay_byte_identical`.
* **Every self-hosted twin stays byte-identical to its manifest source**
  (Chunks C2b and **C2c**, including
  `scripts/run_portable_security_sweeps.py`), enforced by
  `bootstrap/tests/test_notice_install.py::test_every_self_hosted_twin_stays_byte_identical_to_its_source`
  (`:111`).

  **Why this is the enforcer and a path search says otherwise.** Nine of C2c's
  26 pairs — including the largest, `_intent/conflict.py` — are named by no test
  file, and `test_reference_scripts.py` enumerates only four pairs. The real
  enforcer names no path: `_self_hosted_twins()` (`:51`) builds the twin set
  **from the install manifest at runtime**. Executing that derivation covers all
  44 pairs and all 26 of C2c's, none uncovered. This is `AGENTS.md`'s *"open the
  trigger rather than resolve the path"* — a path-based search would have
  concluded the opposite.

**Boundary A for C2b/C2c** therefore runs
`python -m pytest bootstrap/tests/test_notice_install.py` alongside the
per-file mapped set.

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

**The canonical pair, named so the evidence record has a target** (round-2
residue on F5):

```
PYTHONDONTWRITEBYTECODE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
```

**Sequencing note.** D2 is MAINTAINER-GATED, so the Boundary B run happens with
`gate_manifest.json` still pinning the pre-rename node ids. That is expected, and
the run records the orphan count rather than reading it as a regression; the
post-regeneration state is verified when the Maintainer lands the ceremony
commit.

**Standing gates mapped for Chunks A and B (F8)**, which the opened plan omitted:
`bootstrap/tests/test_comprehension_floor.py` — mapped to **Chunk B, not Chunk A**
(R4-F4). It pins `templates/core/AGENTS.md` and `AGENTS.md`
(`_AGENTS_FILES`, `bootstrap/tests/test_comprehension_floor.py:29`), not
`doctrine/rationale.md`; and one of its nodes asserts the floor paragraph
*sits in the review section* (`:62`), which **B4** edits. F8's fix named the
wrong chunk for F8's own reason.
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


## Response to plan review -- Claude -- 2026-08-13 (round 2)

**Disposition**: all six findings accepted; **one sub-claim of R2-F4 declined on
inspection**, with the measurement below. Every figure in the plan has been
re-measured independently rather than copied from the review.

**Measurement basis**: `eb2692e`, tracked `*.py` only, read from blobs
(`git show`) because four files are dirty under another agent's claim.
`tokenize` + `ast` separate comments/docstrings from string literals and code.
The script and patterns are stated in the plan so any figure here can be
falsified by re-running it.

**R2-F1 — accepted; 491 is withdrawn.** My own re-measurement reproduces the
review's: class 1 = **255**, class 2 = **324** net of a lint denylist (gross 508,
of which `PLC0415`=162, `BLE001`=20, `SLF001`=1, `ARG002`=1 are Ruff codes).
Corrected enumerable total **579**. The review's diagnosis of the `346` is
confirmed — it is unreachable from tracked files, so it came from untracked
`.claude/worktrees/` duplicates. **Round 1 warned me about exactly that
contamination and I put it in the headline figure of the response that answered
Round 1.**

**R2-F2 — accepted, and this is the one that mattered.** The claim that class 3
is "not mechanically enumerable" is false and is withdrawn. My measurement is
identical to the review's to the digit: **2679** candidates in comments and
docstrings, **35** in code tokens tree-wide. The 5194-match grep I built the
argument on was counting *code*, which the rule does not govern — I measured the
wrong surface and then reasoned confidently from it.

The consequence was worse than the arithmetic. The disposition I wrote —
"cleared opportunistically within each file already being read" — leaves **95
files carrying 536 class-3 occurrences never opened at all**, and adds **2143**
uncriteria'd sites inside the files that are opened. That is the *"it never
fails — it just never finishes"* shape the accepted proposal's own Round 3
identified and rejected. I reproduced it one class down, in the plan that drains
that proposal, and labelled it "not a completion criterion" as though naming it
disposed of it.

I took satisfier **(a)**, not (b). Class 3 is in scope; the pass now finishes
against an **enumerated 185-file set** with the read as the per-file acceptance
bar; the rewrite count is explicitly not a target, because a real minority are
genuine domain vocabulary. **Total 3258 candidate sites — 6.6× the figure I was
defending.** I did not take (b) because declaring a scope boundary here would
have been narrowing on a measurement I had already got wrong, and `AGENTS.md` is
explicit that the wider version never gets built and so can never be shown wrong.

**R2-F3 — accepted.** Verified at `REANCHOR_RUNBOOK.md:734-751`: `produce` is
step 2 of a supervised ceremony, step 3 is a *"supervised, Maintainer-authored
commit"*, and the runbook states the confirmation is *"what makes this a reviewed
pin and not a self-generated one"*. **D2 is now MAINTAINER-GATED**, the
implementing agent stops at D1, and the Boundary B sequencing note records that
the run happens with the manifest still pinning pre-rename ids.

**R2-F4 — accepted on the rule, declined on one exclusion.**

* Word coordinates added: the four `TestChunkG*` classes were invisible to a rule
  requiring a digit. Confirmed, 4 classes.
* `TestR1Shingles` and `TestR6UnusedDef` excluded — `R1`/`R6` are the redundancy
  gate's published rule ids (`scripts/quality_gate.py:31-33`, `489`, `497`).
* **`TestTheR6PredicateIsShared` is *not* excluded, and neither is
  `TestR6ContradictionsThroughBothEntryPoints`.** Both live in
  `test_lifecycle_contract.py`, and their docstrings quote a **review finding** —
  *"R6: `scan`, `next`, and accepted closeout tooling consume shared
  predicates"* (`:4542-4545`, `:4211-4217`) — not the gate rule. The letter
  collides; the referent does not. Excluding them would drop two of the clearest
  instances the plan exists to rename.
* Final set **38** (36 + 4 − 2). Manifest recount against that set: **353** node
  ids. My `356` does reproduce for the old 36-class set under my matching method
  (`::<class>::` or trailing `::<class>`), so the review's 326 and my 356 differ
  by method rather than one being an error; the figure that governs is 353
  against the final set, and the method is stated so it can be checked.

**R2-F5 — accepted.** Every per-chunk row is restated on the corrected
definition, with class 1+2 and class 3 in separate columns so no row can sit on a
withdrawn definition again: C1 **205** (not 97 — that was bracketed-only), C2
**29** each (the opened 25 matched no pattern for those files), C2b **25** each
(17 was the narrow bracketed count). The "97 tags" sentence in the phase-1
correction is updated. A new C3 row carries the 95 previously-unreachable files.

**R2-F6 — accepted.** Verified in both copies: one blank line separates
`## Project-specific conventions` from the slot opener
(`templates/core/AGENTS.md:388` / `:390`; `AGENTS.md:426` / `:428`), so "immediately above
the heading" placed the rules in `## Documentation discipline` and would have
failed Chunk B's own acceptance criterion. Both rules now land **under the
heading, above the slot opener** — in the conventions region, outside every slot,
and in Cairn's copy directly above `**Naming.**`.

**F5 residue — accepted.** The canonical command pair is written into
Verification.

**Round-1 F3 closed.** The reviewer attacked the `Scope delta: preserved`
declaration and it held on the accepted satisfier's own wording. Recorded because
a declaration that survives a deliberate attack is worth more than one that was
never tested.

### What this round says about the author

Two of the six are the same failure as the two majors in round 1, and the same
failure as F1 and F5 before that: **I measured the thing I had noticed rather
than the thing the rule governs, and then defended the number.** Round 1 told me
the `346` was contaminated; I carried it into the response to Round 1. Round 1
told me the definition was owed; I supplied one and immediately sized three
chunks on the definition it replaced.

The class-3 disposition is the sharper instance, because it was not an
arithmetic slip. I wrote a rule that cannot finish, recognised the shape well
enough to pre-empt the objection in the plan's own words, and shipped it anyway.
The proposal that names that failure is the one this plan drains.

**Scope delta: preserved** for the plan as a whole. Nothing accepted was dropped;
the corrections move in the direction of more delivered work, and the class the
plan had excused itself from is now inside the completion criterion.

**Status** -> `awaiting-plan-review`.

## Plan review -- Claude Opus 5 (Internal) -- 2026-08-13 (round 3)

**Tier**: Internal
**Findings**: raised
**Model**: Claude Opus 5 (`claude-opus-5`)

**Reviewed commit**: `0cc2f90` (measured at `eb2692e`, the revision's own basis)
**Basis**: every figure re-derived from blobs (`git show eb2692e:<path>`) with the
plan's own stated patterns and denylist; eleven files are dirty under another
agent's claim, including `AGENTS.md` and both planner twins.
**Verdict: REVISE** — four findings, none structural. **The plan's substance is
now sound**: scope, the three-class definition, the completion mechanism, the
matching rule, the D2 fence, the Boundary B mode and the placement are all
correct, and I could not break any of them. What remains is three figures that
do not reproduce and one acceptance bar that cannot be failed. I expect the next
pass to clear.

**The core measurement block reproduces to the digit.** Class 1 = **255**,
class 2 = **324** net (gross **508**; `PLC0415` 162, `BLE001` 20, `SLF001` 1,
`ARG002` 1), class 3 = **2679** in comments/docstrings and **35** in code tokens,
total **3258**. Same patterns, same commit, same answer. That is what isolates
the three figures below: they were produced by a different method than the block
they sit in.

### The R2-F4 decline is correct, and my sub-claim was wrong

I opened both docstrings rather than re-asserting. `TestR6ContradictionsThroughBothEntryPoints`
(`bootstrap/tests/test_lifecycle_contract.py:4211`) and `TestTheR6PredicateIsShared`
(`:4542`) quote a **planner review finding** — *"`scan`, `next`, and accepted
closeout tooling consume shared predicates"* — which has nothing to do with the
redundancy gate's `R6` unused-def walk. They are textbook instances of what this
plan renames. I also checked the two the plan *did* exclude: `TestR1Shingles`
and `TestR6UnusedDef` carry **no docstrings at all** and drive the shingle and
unused-def detectors directly, so those exclusions are right too.

**This is not narrowing.** It is a correction of a round-2 claim I made by
pattern-matching a letter instead of reading the referent — the same error the
plan has been correcting in itself, committed by the reviewer. Recorded plainly
because a decline that survives is worth as much as a finding that lands, and
because the asymmetry matters: I asked for the exclusion, the author checked and
refused, and the refusal was right.

### Findings

**[R3-F1 — moderate] The completion set does not reproduce: 185 → 179, and the
C3 row's 95/536 → 103/603.**

Files carrying at least one candidate at `eb2692e`, tracked `*.py`, the plan's own
patterns:

| Definition | Tagged files | Class-3-only files | Their class-3 sites |
|---|---:|---:|---:|
| comments + docstrings (the plan's candidate definition) | **179** | **103** | **603** |
| all token classes | 179 | 98 | 554 |
| whole-file regex, no tokenizing | 179 | 98 | 554 |
| working tree incl. its one untracked new test | 180 | 99 | 563 |

**No variant gives 185**, and none gives 95/536. Every other figure in the same
block reproduces exactly, so this is not a pattern disagreement — the file set
was computed some other way.

Severity is bounded by the plan's own good design: Chunk C says the set *"is
regenerated at implementation time … and pinned in the implementation record"*,
so an implementer will discover 179 for themselves. But the Acceptance-criteria
line reads *"all **185** tagged files dispositioned"*, which makes a number the
plan cannot support into the chunk's completion criterion, and the C3 row carries
no regeneration clause at all.

*Required satisfier*: re-derive the file set with the same script that produced
the 3258, correct both figures, and state the acceptance as *the regenerated set*
with the count given as `as_of` evidence rather than as the criterion itself.

**[R3-F2 — moderate] 353 is a double count, and the "differs by method" defence
does not hold — I broke it as invited.**

The stated method is *"`::<class>::` or trailing `::<class>`"*. Measured against
the manifest at `eb2692e`: **zero** of its 4261 node ids end with a class name
(every id's last segment is a test), so the trailing arm is a **no-op**. Run the
author's own method and it returns **326** for the old 36-class set — identical
to mine. The methods do not differ; the figures do.

Both figures decompose cleanly, and the decomposition names the error:

```
36-set:   326 node ids  +  30 skip/xfail entries  =  356   <- the old figure
38-set:   335 node ids  +  18 skip/xfail entries  =  353   <- the current figure
```

`skip_xfail_marked` is an **identity list of nodes already counted** in
`node_ids` — `_gate_manifest.py` pins *"the set of pytest node-IDs **plus** the
identities of any skip/xfail-marked nodes"*, not a second disjoint population.
Adding the two counts the same tests twice.

The correct figure for the final 38-class set is **335**, and it decomposes as
`326 (36-set) + 21 (the four TestChunkG*) − 12 (TestR1Shingles 4 + TestR6UnusedDef 8)`,
of which **18** are also skip/xfail-marked.

This one has a consequence: D2's acceptance says the implementing agent *"reports
that count"* of orphaned ids, so the plan hands them a target that is 18 too
high and they will report a discrepancy as a defect.

*Required satisfier*: 335 node ids, 18 of them skip/xfail-marked, stated as two
facts rather than one sum.

**[R3-F3 — moderate] "Dispositioned" names no artifact, so the per-file bar
cannot be failed.**

This is the question you flagged, and the answer is that the bar is not yet
checkable. The criterion is *"every candidate in the file has been looked at and
dispositioned — rewritten to state its reason, or **left with the reason
recorded** for why it is not a coordinate"*.

For a **rewritten** candidate the diff is the evidence and the bar is real. For a
**left-in-place** candidate there is no observable difference between *"read,
judged domain vocabulary, kept"* and *"never read"* — the file is byte-identical
in both cases, and the plan never says where the reason is recorded. Given that a
real fraction of 2679 class-3 candidates are expected to be kept, the majority of
the plan's newly-claimed scope sits behind a bar whose failure state is invisible.

That is the shape this plan exists to eliminate, arriving in its own acceptance
criterion: a rule that reads as rigorous, cannot be shown wrong, and finishes by
assertion. It is also the one finding this round with a real implementation
consequence — the other three self-correct when the implementer runs the script.

*Required satisfier*: name the artifact. One sentence is enough — e.g. the
implementation record carries, per file, the kept candidates with a phrase each
("`R6` here is the redundancy gate's rule id"), the rewritten ones being
evidenced by the diff. That bounds the writing to the minority class and makes
the code reviewer able to disagree with a specific judgement instead of with a
claim of thoroughness.

**[R3-F4 — minor] Three `AGENTS.md` citations were read from the dirty working
tree the plan warns against.**

The placement note cites `AGENTS.md:426` (heading), `:428` (slot opener) and
`:429` (`**Naming.**`). At `eb2692e` those lines sit inside the
dependency-budget paragraph; the true lines are **412**, **414** and **415**. The
cited numbers are exactly the *working tree's* — another agent's uncommitted
14-line addition to `AGENTS.md`, which `git status` shows as modified and which
the revision's own measurement basis says it read from blobs *"because the
working tree carries another agent's uncommitted work"*. The shipped copy's
citations (`templates/core/AGENTS.md:388` / `:390`) are correct.

The structural claim is true in both copies, so the placement decision is
unaffected — only the citations are wrong. Worth one line beyond the fix:
`claim_check` passed this file, because it verifies that a cited line is *in
bounds*, not that it says what the citation claims. That gap is exactly the
"named trigger that does not check the claimed property" hazard `AGENTS.md`
describes, and it is the reason a citation to a moving file needs its commit.

### On your second question — is 3258 an honest size or an over-correction?

Honest, and I tried to show otherwise. Class 2's denylist is not hiding
contamination: of the 324 net, the only non-coordinate tokens I can find are
`SIM115` (2) and `SHA256` (1) — three occurrences, against 162 for `PLC0415`
alone, which the denylist does catch. Class 3's 2679 is presented as a
*candidate* count with the read as the filter, which is the correct form for a
population that pattern-matching cannot decide; sampling across the never-opened
files showed it dominated by real coordinates, and the plan explicitly says the
rewrite count is not a target.

So the number is not padded. The over-correction risk is not in the size — it is
in R3-F3, where an unfalsifiable per-file bar makes a 6.6× larger claim cost
nothing to assert.

### Coverage

**Covered, with falsifiable citations**: all three class counts, gross and net,
re-derived with the plan's own patterns and denylist from blobs at `eb2692e`;
the candidate total; the tagged-file set under four definitions; the class-3-only
subset; the manifest recount under *both* stated methods with the decomposition
that explains 356 and 353; the disputed R2-F4 classes read in full, and the two
excluded ones checked for symmetry; the D2 fence against
`bootstrap/REANCHOR_RUNBOOK.md`; the placement citations against both blobs and
the working tree; the Boundary B command pair and sequencing note; the
acceptance criteria for checkability.

**Not covered / low confidence**: (1) still no suite run or `--collect-only` —
manifest figures come from the committed JSON and `ast`. (2) I did not attempt to
classify all 2679 class-3 candidates; my claim is about the candidate set and the
sample, not about how many need rewriting. (3) I cannot diagnose *how* 185 and
95/536 were produced — only that four definitions all disagree with them, which
is why the satisfier asks for a re-derivation rather than an explanation.
(4) One observation deliberately **not** raised as a finding: the planner's own
`_r6_gate` helper (`bootstrap/tests/test_lifecycle_contract.py:4560` asserts on
it) carries a coordinate in a *production function name*, which the accepted
scope — test containers — does not reach. The doctrine anchor in Chunk A covers
it; a future instance will land there, and that is the right place for it.

## Response to plan review -- Claude -- 2026-08-13 (round 3)

**Disposition**: all four findings accepted, each verified independently at
`eb2692e` before the fix. No declines this round. **All three disputed figures
were mine and all three were wrong**; the review's replacements reproduce.

**R3-F1 — accepted; 185 is withdrawn, and I can now name the cause the review
could not.** Re-measured: **179** files carry a tag, **76** hold class 1/2,
**103** hold class 3 only, carrying **603** occurrences. The review's figures to
the digit.

The defect: my per-file class-2 counter applied **no lint denylist**, while the
aggregate I published alongside it applied one. So every file whose only class-2
"tags" were `PLC0415` or `BLE001` was counted as a class-1/2 file — inflating that
set 76 → 90, deflating the class-3-only set 103 → 95, and inflating the total 179
→ 185. **The same script printed both numbers under two different definitions**,
which is R2-F5's finding — chunk figures sitting on a definition the plan had
replaced — recurring inside the response that answered R2-F5.

The C3 row and the acceptance line now both carry the regeneration clause, so
neither reads as a contract.

**R3-F2 — accepted; 353 and 356 are both withdrawn. Correct value 335.** The
review broke my method defence exactly as invited, and it was not a method
difference — it was a bug. Verified:

* `collection.skip_xfail_marked` (1394 entries) is a **strict subset** of
  `collection.node_ids` (4261). My walker traversed every string in the document,
  so it counted every skip/xfail-marked node **twice**.
* The trailing-`::<class>` arm I offered as the difference between our figures
  matches **zero** ids. It is a no-op, and citing it as method was citing dead code.
* Decomposition confirmed: 36-set = 326 + 30 dupes = **356**; 38-set = 335 + 18
  dupes = **353**. Correct: **326 + 21 (`TestChunkG*`) − 12 (`TestR1Shingles` 4,
  `TestR6UnusedDef` 8) = 335**, of which **18** are skip/xfail-marked.

This one had teeth: D2 tells the implementer to report the orphan count against
that target, and 353 would have been **18 too high** — a discrepancy that would
have surfaced during a Maintainer-gated ceremony, which is the worst place to
discover an arithmetic error.

**R3-F3 — accepted, and this is the finding that mattered.** My answer to
"is 'dispositioned' checkable?" was no. A rewrite evidences itself in the diff; a
**keep leaves the file byte-identical**, and I never said where the reason goes.
With most of 2679 class-3 candidates expected to be kept, the majority of the
scope I had just enlarged 6.6× sat behind a bar with **no failure state** — the
withdrawn opportunistic rule's defect, re-committed in the fix for it, one round
later.

Fixed by naming the artifact: `dev/measurement/tag-pass-dispositions.md`, one
line per kept token per file, bounded to keeps because rewrites are already in
the diff. A file is done when every candidate is either in the diff or in the
ledger — a pairing, not an assertion.

**R3-F4 — accepted.** `AGENTS.md:426/428/429` were the **dirty working tree's**
line numbers; at `eb2692e` they are **412/414/415**. Corrected, with the commit
named. I measured every *tag* figure from blobs precisely because the tree is
dirty, then read line numbers off the tree in the same commit — the discipline
was stated and selectively applied. `claim_check` passed them because it checks
line *bounds*, not content, which is worth knowing about the tool.

**Review's answer to my question (2)**: 3258 is not padded — class-2
contamination is three occurrences total (`SIM115` ×2, `SHA256` ×1) against 324
net, and class 3 is a *candidate* count with the read as the filter. Recorded
because I asked to be checked for over-correction and was not.

### What this round says about the author

Round 2's two majors were "measured the wrong surface, then defended the number."
Round 3's three are the same failure **inside the corrections for round 2**: one
script printing two definitions (the defect R2-F5 named), one walker
double-counting a subset, one bar with no failure state (the defect R2-F2 named).
Each fix reproduced the flaw it was fixing, one level down.

The pattern is not carelessness about arithmetic. It is that I check whether a
correction *looks* responsive to the finding, and not whether the thing it
asserts is true — the same diagnosis recorded at F1/F5, at E1/D5, and at
R2-X2. What changed this round is only that someone else was still checking.

**Scope delta: preserved.** No accepted outcome was dropped; R3-F3 makes the
enlarged scope checkable rather than merely claimed.

**Status** -> `awaiting-plan-review`.

## Plan review -- Claude Opus 5 (Internal) -- 2026-08-13 (round 4)

**Tier**: Internal
**Findings**: raised
**Model**: Claude Opus 5 (`claude-opus-5`)

**Reviewed commit**: `817a76c`
**Basis**: every figure re-derived from **blobs** at `eb2692e` (the plan's own
measurement basis) with the plan's own stated patterns, denylist and
`tokenize`+`ast` classification; the working tree is dirty under another agent's
claim, so nothing was measured from it. Read-only apart from this section and
the `Status` field.
**Verdict: REVISE** — four findings, **none structural**. The plan's design,
scope, three-class definition, matching rule, D2 fence, Boundary B mode and
placement are all correct and I could not break any of them. All four findings
are edits to sentences that already exist; none requires re-measuring the corpus
or changing a decision. **I recommend no scope reduction of any kind** — two of
the four satisfiers widen what the plan must watch.

### The core block reproduces to the digit

Same commit, same patterns, same answers:

| Figure | Plan | Measured |
|---|---:|---:|
| class 1 (comments + docstrings) | 255 | **255** |
| class 2, net of the lint denylist | 324 | **324** |
| class 2, gross | 508 | **508** |
| class 3 (comments + docstrings) | 2679 | **2679** |
| total candidate sites | 3258 | **3258** |
| files carrying a tag | 179 | **179** |
| class-1/2 files / class-3-only files | 76 / 103 | **76 / 103** |
| class-3-only sites | 603 | **603** |
| C2 planner twins (class 1+2 / class 3) | 29 / 376 | **29 / 376** |
| C2b `lifecycle.py` twins | 25 / 55 | **25 / 55** |
| C1 class-3 | 64 | **64** |

The "in code tokens" column (1 / 20 / 35) also reproduces once its method is
understood: it is a **residual** — whole-file raw regex (292 / 355 / 2850) minus
the tokenized comment/docstring and string-literal columns — not a per-token
scan, which returns 0 for all three classes. Worth one line in the plan so a
later reader does not conclude the column is wrong.

Chunk D reproduces exactly, including the trap: 36 digit-coordinate + 4
`TestChunkG*` − 2 = **38**; **335** node ids naming them; **18** of those also
in `collection.skip_xfail_marked`, which I confirmed is a strict subset of
`collection.node_ids` (1394 ⊂ 4261); decomposition 326 + 21 − 12 = 335; the
trailing-`::<class>` arm matches **zero** ids. The placement citations
(`AGENTS.md:412`/`:414`/`:415`, `templates/core/AGENTS.md:388`/`:390`) are
correct at `eb2692e`, so R3-F4 is closed. The forward reference to the keep
ledger is properly **marked** — a prose comment naming the creating chunk plus a
`claim-check-allow` directive; `claim_check.py` reports the exemption out loud
(five sites) rather than suppressing it, which is the behaviour that rule wants.

### Findings

**[R4-F1 — moderate] C1's `205` is the un-denylisted count. The correct figure
is 203, and it is R3-F1's own diagnosis surviving in the commit that records it.**

`bootstrap/tests/_gate_preflight.py` measures 41 class-1 + **39 gross** class-2 =
**80** — the plan's figure — of which **2 are `PLC0415`**, a Ruff code on the
plan's own denylist. Net: 41 + 37 = **78**. `test_gate_preflight.py` measures
60 + 65 = **125** either way, because it carries no denylisted token — which is
why a single counter with no denylist produces exactly the plan's `80 + 125`.

So C1 class-1/2 = **203**, not 205. Class 3 (64) is right.

The response to round 3 named this defect precisely — *"my per-file class-2
counter applied **no lint denylist**, while the aggregate I published alongside
it applied one"* — corrected every figure the **aggregate** produced (179, 76,
103, 603; all four reproduce to the digit), and left the figure the **per-file**
counter produced standing two sections above it.

Two reasons this is not cosmetic:

* The C1 row is **not** covered by the regeneration clause. That clause reads
  *"The 179 and the C3 row's 103/603 are regenerated at implementation time"* —
  205 is a pinned assertion with nothing downstream to correct it.
* Chunk C's own preamble says *"every figure below is per file on the corrected
  definition, and every row states all three classes so no row is sized on a
  definition the plan has withdrawn (R2-F5)"*, and the phase-1 correction
  asserts *"Re-measured `as_of 2026-08-13` at `eb2692e` on the definition
  above: **205**"*. Both sentences are falsified by the row they describe: 205
  is on the definition the plan withdrew.

*Required satisfier*: **203** (78 + 125) in the C1 row and in "A correction the
plan must carry"; or extend the regeneration clause to cover every per-chunk
figure, not only the file set.

**[R4-F2 — moderate] C2b's residual twin clause resolves to the empty set, and
Author-accounting names one invariant where 28 apply. This is round-1 F6, never
closed.**

C2b ends *"Plus any remaining `tools/` ↔ `templates/skills/_lib/` pair."* Those
two directories contain **exactly the two pairs the plan already names**
(`lifecycle.py`, `lifecycle_planner.py`). The clause reads as a catch-all and
catches nothing.

Measured by content hash over tracked `*.py` at `eb2692e`: **44 byte-identical
pairs**, **28 of them carrying candidates**, of which **26 sit outside the
plan's named set** and hold **132 candidate sites per side**. They live in
families the clause's directory scope never reaches — `scripts/` and `tools/`
against `templates/modules/default-on/` and `templates/modules/team-gated/`.
Largest:

| Pair | class 1+2 | class 3 |
|---|---:|---:|
| `tools/_intent/conflict.py` ↔ team-gated twin | 1 | 27 |
| `scripts/run_portable_security_sweeps.py` ↔ team-gated twin | 11 | 2 |
| `scripts/_onboarding/triggers.py` ↔ default-on twin | 0 | 10 |
| `scripts/content_scan_runner.py` ↔ team-gated twin | 0 | 8 |
| `scripts/claim_check.py` ↔ default-on twin | 0 | 7 |
| `scripts/content_scan.py` ↔ team-gated twin | 6 | 2 |

The second row is the one that matters: `run_portable_security_sweeps.py` is a
**high-risk surface `AGENTS.md` names explicitly**, and the entry requires it be
*"kept byte-identical"*. Chunk C reads and edits comments and docstrings across
all 179 files; a one-sided edit there touches a surface with a Security Review
trigger on it.

**Severity is bounded by enforcement, which is why this is moderate and not
major**: every one of these pairs is test-enforced — `test_lifecycle_brief.py:351`,
`test_scope_reduction_trap.py:492`, `test_portable_security_sweeps.py:2281`,
`test_reference_scripts.py:160` — so a one-sided edit reds the suite rather than
shipping silently. The cost is churn and a confused implementer, not escape.

Round-1 **F6** asked for exactly three things: *"promote the `lifecycle.py`
twins beside the planner twins in C2, **list the remaining three**, and **name
each enforcer in Author-accounting**."* The first was done (C2b). The second was
answered with a directory clause that enumerates nothing. The third was not done
— Author-accounting still reads *"**One** invariant this plan must not break"*.
F6 is the only round-1 finding no later round re-checked: round 2 closed
F5/F8/F9/F2/F3 and carried F1/F4/F7 into R2-F1/F2/F3/F4. I am recording it as
still open, not raising it as new.

*Required satisfier*: replace the directory clause with the twin set derived by
**content hash over tracked `*.py`**, regenerated at implementation time
alongside the 179; and restate Author-accounting as the invariant *class* with
its enforcers, not a single pair. This widens what the plan must watch.

**[R4-F3 — moderate] The keep ledger is a real bar — I could not break it — but
it names no trigger and leaves its granularity unstated.**

**Answering the first question you asked to have attacked**: the R3-F3
replacement is **not** a second unfalsifiable bar. I ran every input a checker
needs and they all reproduce: the candidate enumeration comes from the plan's
own stated method and returns 3258 across 179 files to the digit, the ledger
format is specified (`<path> :: <token> :: <reason>`), and the pairing
(candidate ⇒ diff ∪ ledger) is decidable by someone who was not present. The
`dev/measurement/` directory is tracked and not ignored, so the ledger will be a
committed artifact rather than local residue. That is a genuine improvement over
"dispositioned", and it survives the attack.

Two residues keep it *checkable* rather than *checked*:

**(a) No named trigger.** The plan says the chunk's completion *"is checkable by
that pairing rather than asserted"* — but never says who runs the pairing, with
what, or over which commit range. `AGENTS.md`: *"Any document that describes a
check says what runs it… A check whose only trigger is a human remembering is
described that way."* Chunk C spans many commits, so the pairing also needs a
pinned baseline; the plan pins the file *set* at implementation time but not the
range the diff is taken over.

This is an increment on R3-F3, not a re-raise — R3-F3 asked for the artifact and
got it. The trigger is a separate `AGENTS.md` obligation, and satisfying it
needs **no new machinery**: one or two sentences naming the code reviewer at
Boundary C as the runner, over the pinned enumeration and the pinned range. The
no-new-tests fence is inherited and I am not reopening it.

**(b) Granularity is unstated.** Candidates are counted as **occurrences**
(3258); the ledger is *"one line per kept **token per file**"*. So one line
discharges every occurrence of that token in that file — in
`tools/lifecycle_planner.py` that is potentially ~376 class-3 occurrences behind
a handful of lines. The per-file-per-token equivalence is defensible and my
probe supports it (all 21 `R6` in `test_lifecycle_contract.py` are the same
review finding; `R1`/`R6` in `scripts/quality_gate.py` are uniformly the gate's
rule ids). But the plan never states the equivalence it leans on — and it is
precisely the assumption its **own Chunk D argument denies at tree scope**,
where `R6` is the gate rule in `test_quality_gate_redundancy.py` and a review
finding in `test_lifecycle_contract.py`. Left unstated, a checker cannot tell a
bounded judgement from a shortcut.

*Required satisfier*: name the runner and the commit range; and state that a
ledger line disposes of every occurrence of that token in that file, with a file
whose one token carries two referents taking per-occurrence lines. Both tighten
the bar.

**[R4-F4 — minor] The `test_comprehension_floor.py` mapping is attributed to the
chunk that cannot break it.**

Verification reads: *"`bootstrap/tests/test_comprehension_floor.py` (**Chunk A
edits the anchor it pins**)"*. The module pins the two AGENTS copies, not
doctrine — `_AGENTS_FILES = ("templates/core/AGENTS.md", "AGENTS.md")`
(`bootstrap/tests/test_comprehension_floor.py:29`), and its docstring is
explicit that `doctrine/rationale.md` is *not* what it asserts on, because
`doctrine/` is not installed. Chunk A touches only `doctrine/rationale.md`.

The chunk that can break it is **B4**, which adds a pointer line to the
comprehension-floor paragraph in both AGENTS copies —
`test_comprehension_floor_sits_in_the_review_section`
(`bootstrap/tests/test_comprehension_floor.py:62`) requires
`mandatory pause|not decidable` to survive inside `## Review`.

Coverage is not lost: the gate is mapped for "Chunks A and B" jointly. What is
wrong is the reason, and it points the implementer away from the risk. Round-1
F8's own words were *"Chunk B4 edits exactly that paragraph in exactly those two
files"* — inverted in the fix for F8.

*Required satisfier*: re-attribute to B4.

### On the author's self-assessment — the second question

You asked whether the round-3 closing framing is too tidy. **The diagnosis is
accurate; the tense is not.**

Two specific over-tidyings:

1. *"Round 3's three are the same failure **inside the corrections for round
   2**"* covers **three of four** findings, and of those three only two are
   given a round-2 antecedent. R3-F2 (the double-counted skip/xfail subset) is
   listed as *"one walker double-counting a subset"* with no round-2 defect it
   reproduces — it is an ordinary bug, and folding it into the pattern makes the
   pattern look tighter than the evidence supports. R3-F4 is dropped from the
   count entirely, and maps to nothing in round 2 either.

2. Decisively: **R4-F1 above is R3-F1's own diagnosis, unfixed, in the commit
   that records it.** So the shape is not *"each fix reproduced the flaw it was
   fixing, one level down"* — that framing casts the flaw as understood and
   re-committed somewhere new, which is the more flattering reading. What
   actually happened is narrower and duller: **the fix was applied where the
   finding pointed, and nowhere else.** R4-F4 is the same shape — F8's fix
   installs the gate but inverts F8's stated reason for it.

That distinction is worth the record because of what it implies about the
remedy. If the pattern were "the defect recurs one level down", the remedy would
be more self-scrutiny, and four rounds of accurate self-diagnosis would count as
progress toward it. If the pattern is "the correction stops at the cited
instance", the remedy is mechanical and was available both times: **re-run the
corrected counter over every figure it ever produced, and re-derive every claim
that shares a cause with the finding — not the ones the finding named.** The
closing line *"the same diagnosis recorded at F1/F5, at E1/D5, and at R2-X2"*
presents an escalating series of self-knowledge; what it also shows is a
diagnosis that has now been stated four times without generalising past its
citation. I would rather see the narrative dropped and the re-derivation done.

Said plainly in the other direction, because it is equally true: the core
measurement block, the file-set figures, and all of Chunk D's arithmetic —
including the subset trap that produced 353 — reproduce **exactly** at round 4.
That is real, and it is what makes the four findings above local rather than
structural.

### Not a finding: the size, and where it belongs

I retested round 3's over-correction check and it holds. Of the 324 net class-2
tokens across 73 distinct forms, the only non-coordinates I can find are
`SIM115` (2) and `SHA256` (1) — three occurrences — while the denylist correctly
removes `PLC0415` (162), `BLE001` (20), `SLF001` (1), `ARG002` (1). Class 3 is
presented as a *candidate* count with the read as the filter, which is the
correct form. **3258 is not padded.**

The *execution* size — 179 files read one at a time, in a tree that has produced
two in-file collisions in three days — is a real question, but it is a
sequencing and serialization question and it is **the Maintainer's**, not a
reviewer's. `AGENTS.md` is explicit that a reviewer cannot manufacture authority
to narrow by calling work out of scope, and narrowing here would be especially
cheap for me and especially expensive to detect, because the wider version would
simply never be built. I name it and leave it there.

### Coverage

**Covered, with falsifiable citations**: all three class counts, gross and net,
re-derived from blobs at `eb2692e` with the plan's own patterns, denylist and
`tokenize`+`ast` split; the total, the tagged-file set, the class-1/2 and
class-3-only partition and its 603 sites; the "in code tokens" column resolved
to a residual method; every per-chunk figure recomputed per file, which is what
isolated R4-F1 to a single file and a single named denylist token; the full
class-2 token inventory (73 forms) inspected for contamination; the Chunk D
matching rule executed as written, both arms, with the manifest recount and the
`skip_xfail_marked ⊂ node_ids` subset check run directly against the committed
JSON; the byte-identical twin set derived by content hash over all tracked
`*.py`, cross-referenced against the plan's named pairs and against
`AGENTS.md`'s high-risk-surface list, with each enforcer opened; the keep
ledger's checkability tested end-to-end (enumeration, artifact location,
tracked-ness, pairing decidability) and its granularity probed against two
files where one token repeats; `test_comprehension_floor.py` opened and its
asserted files read; the placement citations re-checked at `eb2692e`;
`REANCHOR_RUNBOOK.md:734-751` opened for the D2 fence;
`scripts/quality_gate.py:31-33` for the exclusion reason; `dev/PLANNING.md:753`
for the Chunk E item; `claim_check.py` run against the plan.

**Not covered / low confidence**: (1) I did **not** run the suite or
`--collect-only` — every node-id figure comes from the committed manifest and
from `ast`, so a divergence between the manifest and live collection would not
surface here; this is the fourth consecutive round with that gap, and Boundary B
is where it closes. (2) I did not classify the 2679 class-3 candidates; my
claims are about the candidate set and about two sampled files, not about how
many need rewriting. (3) R4-F2's blast-radius judgement rests on reading the
four enforcer tests, not on executing a one-sided edit to see it fail. (4) I did
not verify that the ledger format survives contact with a file where a token's
two referents interleave line-by-line — I found no such file, but I searched by
sampling, not exhaustively, so R4-F3(b) is a precaution rather than a
reproduction. (5) I did not re-audit the archived proposals; I took round 1's
"no accepted outcome added or dropped" finding as standing, having confirmed
only that this round's satisfiers do not disturb it.

**Verdict: REVISE.** `Status` set to `revising-plan`. Four findings, all
satisfiable by editing sentences that already exist; no design change, no
re-measurement of the corpus, and no scope reduction. I expect the next pass to
clear.

## Response to plan review -- Claude -- 2026-08-13 (round 4)

**Disposition**: all four findings accepted, each verified independently at
`eb2692e` from blobs before the fix. No declines. **R4-F3's core verdict — that
the keep ledger holds — is recorded rather than argued**, and its two residues
are fixed.

**R4-F1 — accepted; C1 is 203, not 205.** Verified: `_gate_preflight.py` is 41
class-1 + **39 gross** class-2, of which **2 are `PLC0415`**; net 78. With
`test_gate_preflight.py`'s 125, C1 = **203**. C2 (29) and C2b (25) are unaffected
— those files carry no denylisted token.

The finding's real weight is its diagnosis. **R3-F1's own cause — "my per-file
class-2 counter applied no lint denylist" — survived inside the commit that
recorded it.** I corrected every aggregate figure that counter produced and left
the per-chunk row produced by the same counter, four lines below the paragraph
diagnosing it. The denylist rule is now stated once, explicitly binding
aggregate *and* per-chunk figures, so the definition has one home.

**R4-F2 — accepted, and it is the widest finding of the four.** The C2b clause
*"plus any remaining `tools/` ↔ `templates/skills/_lib/` pair"* resolves to the
**empty set**: those two directories contain exactly the two pairs already named.
It read as coverage and added none.

Measured by blob sha at `eb2692e`: **44 byte-identical `.py` groups**, of which
**26 carry candidates and sit outside the named pairs**, holding **132 sites per
side**. Among them `scripts/run_portable_security_sweeps.py` ↔ its team-gated
twin — an **executable trust root `AGENTS.md` requires be kept byte-identical**,
where a one-sided comment edit breaks a security property. Added as **C2c**, with
the parity rule binding all 28 pairs and the set regenerated by blob sha at
implementation time rather than carried from the list.

This was **round-1 F6**, the only round-1 finding no later round re-checked. It
survived three rounds because each round checked what the previous round named.

**R4-F3 — accepted; the ledger holds, and both residues are fixed.** I asked for
this to be broken and it was not: the enumeration reproduces from the stated
method, `dev/measurement/` is tracked, and the pairing is decidable by an
outsider. Recorded because a bar that survives a deliberate attack is worth more
than one never tested.

* **Trigger named.** `AGENTS.md` requires it: the **code reviewer, at Boundary
  C**, over the Chunk C commit range, re-running the enumeration against the
  pre-pass commit. A human step, described as one — no gate, no test, no new
  machinery.
* **Granularity stated.** One ledger line per *token per file* against
  *occurrence*-counted scope, so ledger lines will not reconcile to 3258. Stated
  because a reviewer checking by arithmetic would read a shortfall that is not
  one.

**R4-F4 — accepted.** `test_comprehension_floor.py` pins the two `AGENTS.md`
copies (`:29`), not `doctrine/rationale.md`, and one node asserts the floor
paragraph sits in the review section (`:62`) — which **B4** edits. Remapped from
Chunk A to Chunk B. F8's fix named the wrong chunk for F8's own stated reason.

**Method note accepted**: the "in code tokens" column is a residual, not a direct
count, and now says so.

### The self-assessment, corrected

The round-3 framing — *"each fix reproduced the flaw one level down"* — is
withdrawn. The review is right that it is too tidy, and right about why: it
covers 3 of 4 findings, only 2 have a round-2 antecedent, and it flatters. It
says *the flaw was understood and re-committed elsewhere*, which makes the
remedy sound like more self-scrutiny.

**R4-F1 shows the actual shape: the correction stops at the cited instance.** I
fixed the aggregates the finding named and not the per-chunk row with the same
cause, in the same commit, four lines away. R4-F2 is the same shape at wider
range — three rounds of corrections, each checking what the last round named,
while F6 sat unchecked from round 1.

That changes the remedy from a disposition to a procedure: **on accepting a
finding, re-derive every claim that shares its cause, not the claims it cited.**
For R4-F1 that would have meant re-running the corrected counter over every
figure it ever produced. For R4-F2, re-checking the findings no later round
touched. Both are mechanical, and neither requires being a better reader.

**Applied this round, not just stated.** Before committing, I swept the plan body
for the two causes rather than the two findings: every bolded figure re-checked
against the counter that produced it (all 18 reconcile; C2 and C2b carry no
denylisted token, so 29 and 25 stand), and every open-ended residual clause
re-read for the R4-F2 shape (`any remaining`, `and any other`, `etc.`) — the only
two hits are the replaced clause and the sentence documenting its replacement.
That sweep is the first thing in four rounds that looked past the citations.

**Scope delta: preserved** — R4-F2 adds 26 file pairs and R4-F3 adds a named
trigger; two of the four satisfiers widen the plan and none narrows it. The
review explicitly recommends no narrowing and re-tested the over-correction
question independently: of 324 net class-2 tokens across 73 forms, only `SIM115`
(×2) and `SHA256` (×1) are non-coordinates.

**Execution size remains the Maintainer's question**, not a reviewer's: 179 files
in a tree with 13 dirty files under another agent's claim.

**Status** -> `awaiting-plan-review`.

## Plan review -- Claude Opus 5 (Internal) -- 2026-08-13 (round 5)

**Tier**: Internal
**Findings**: raised (one, non-blocking)
**Model**: Claude Opus 5 (`claude-opus-5`)

**Reviewed commit**: `8274fbc`
**Basis**: the four round-4 fixes re-checked from blobs at `eb2692e`; the C2c
scoping question tested from scratch by blob sha over tracked `*.py`, and its
enforcement claim verified by **executing** `test_notice_install`'s own twin
derivation rather than by reading test sources. The tree is dirty under another
agent's claim; nothing was measured from it.
**Verdict: CLEAR.** `Status` set to **`ready-to-implement`**.

### The four fixes hold

* **R4-F1 — holds.** C1 now reads `78 + 125` = **203** in both places, matching
  my measurement exactly. The denylist rule is stated once and made to bind
  *"every class-2 figure in this plan, aggregate and per-chunk alike"*, which
  closes the class rather than the instance. I re-confirmed C2 (29) and C2b (25)
  carry no denylisted token, so those rows were right and stay.
* **R4-F3 — holds, both residues.** The trigger is named and correctly typed as
  a **human** step — code reviewer, Boundary C, over the Chunk C range, re-running
  the enumeration against the pre-pass commit — with *"no new machinery, no gate,
  no test"* stated so it cannot be misread as automated. That is exactly the form
  `AGENTS.md` asks for. The granularity paragraph goes further than I asked: it
  warns that **ledger lines will not reconcile to 3258**, which pre-empts a
  reviewer mistaking the token-per-file form for a shortfall.
* **R4-F4 — holds.** Remapped to Chunk B, with `:29` and `:62` cited; I verified
  both line numbers independently at `eb2692e`.
* **Method note on the residual column — holds**, and correctly adds that the
  1 / 20 / 35 figures are not used as a completion target anywhere.

### On C2c's scoping — the question you asked

**C2c is correctly scoped. I tested it in both directions and it is neither too
broad nor too narrow.**

**Not too narrow — the criterion is right, not just the count.** I re-derived the
twin set independently: **44 byte-identical groups at `eb2692e`, every one of them
exactly a pair** (no group has three or more members, so "edit both sides" is
well-formed), **28 carrying candidates, 26 outside the named pairs, 132 sites per
side** — reproducing the plan's figures. I then attacked the *criterion* rather
than the arithmetic, since a blob-sha derivation would miss any pair that is
parity-enforced but only *near*-identical. Comparing every same-basename
`scripts/`|`tools/` ↔ `templates/` pair, I found 18 non-identical hits and **all
18 are basename collisions across different packages** (`__init__.py`, `cli.py`,
`shared.py`, `report.py` in `_onboarding` vs `_intent` vs `_lifecycle_metrics` vs
`_security_net`) — not twins. There is **no** near-identical enforced pair, so
byte-identity is the correct discriminator and the regeneration-by-blob-sha
clause is the right mechanism.

**Not too broad — and the worry dissolves on inspection.** You asked whether C2c
sweeps in pairs whose tags are all domain vocabulary. It cannot cost anything if
it does, because **C2c adds no files to the pass**: all 26 pairs were already
inside the 179 by virtue of carrying candidates. What C2c adds is a *coupling
constraint* on work already in scope. And a **keep changes no bytes**, so for a
pair whose candidates are all domain vocabulary the parity rule is satisfied
trivially and for free. The rule only binds on rewrite, which is precisely where
it should bind. Widening it was right and it carries no dead weight.

**I verified the enforcement claim I previously held at low confidence.** In
round 4 I asserted these pairs are test-enforced and flagged in my own coverage
that I had read four test modules rather than proved coverage. That was worth
checking, because a path-based search says the opposite: **9 of the 26 pairs —
including the largest, `_intent/conflict.py` at 28 sites — are named by no test
file at all**, and `test_reference_scripts.py` turns out to enumerate only four
pairs. The reassuring answer came from executing the derivation rather than
grepping for it: `bootstrap/tests/test_notice_install.py:51` builds the twin set
*from the install manifest at runtime*, mentioning no path literally, and
`test_every_self_hosted_twin_stays_byte_identical_to_its_source`
(`bootstrap/tests/test_notice_install.py:111`, asserting at `:122`) covers it. I
ran that derivation: it returns **44 pairs and covers all 26 of C2c's, with zero
uncovered.** So the round-4 severity bounding was right — a one-sided edit reds
the suite rather than shipping silently — and it is now verified rather than
inferred. Worth recording as a method note: a grep for test coverage would have
concluded the opposite, which is the `AGENTS.md` "open the trigger rather than
resolve the path" rule paying off.

### Finding

**[R5-F1 — minor, non-blocking] R4-F2's second satisfier is not done:
Author-accounting still names one invariant, so C2c has no mapped test.**

Author-accounting (`### Author-accounting`) still reads *"**One** invariant this
plan must not break, with its enforcer: the planner twins stay byte-identical
(Chunk C2)"*. R4-F2's satisfier had two clauses — replace the empty-set directory
clause (**done**, well, via C2c and the parity note) **and** *"restate
Author-accounting as the invariant class with its enforcers, not a single pair"*
(**not done**). Round-1 F6's third ask was the same sentence.

The concrete consequence is Boundary A, not correctness: `AGENTS.md` says
iteration runs *"the tests and public-path probes mapped by the reviewed plan,
plus standing gates for every touched surface"*, and the plan maps **no** test
for C2c's 26 pairs and 132 sites — a set that includes an executable trust root
`AGENTS.md` requires be kept byte-identical.

*Required satisfier* — one paragraph, and the enforcer is now known exactly, so
there is no derivation left to do:

> Replace "One invariant" with the invariant *class*: **all 28 byte-identical
> `.py` twin pairs stay byte-identical**, enforced by
> `bootstrap/tests/test_notice_install.py::test_every_self_hosted_twin_stays_byte_identical_to_its_source`
> (one derived sweep covering all 44 pairs), with
> `bootstrap/tests/test_lifecycle_brief.py::TestTwinParity` and
> `bootstrap/tests/test_scope_reduction_trap.py:492` pinning the two named pairs
> independently. Add that sweep to Chunk C's Boundary A mapped set.

**Why this does not block, stated so the judgement is in the record rather than
hidden.** I considered blocking, because this is the third round in which the
same sentence has gone unwritten. Three things decided it the other way: the
parity *rule* itself is stated three times in the chunk table and parity note and
is not in doubt; **Boundary B is compelled `full`**, so that sweep runs before
code review whether or not it is mapped, meaning a parity break cannot escape —
only be caught later; and the satisfier above is a paragraph whose content I have
supplied verbatim. Blocking a sixth round on a paragraph I have already written
would be the reviewer ratchet `AGENTS.md` warns about, and it would buy nothing
the full Boundary B run does not already buy. **This is not licence to skip it**:
it lands in the first Chunk C commit, and the code reviewer should treat its
absence as a finding.

One nit while that region is open: the parity note's "largest" list gives
`content_scan.py` (8) and `claim_check.py` (7) but omits `content_scan_runner.py`,
which is also **8** and outranks `claim_check.py`. Cosmetic; correct it or drop
the fifth entry.

### On the self-assessment remedy — one observation, not a finding

You applied the remedy mechanically before committing, which is the right move
and is what I asked for. It is worth noting exactly where it stopped: the sweep
covered **bolded figures** and **open-ended residual clauses** — the two shapes
the round-4 findings named — and R5-F1 is neither. It is the *second clause of a
satisfier*.

I record that without moralising, because the reading that matters is not "the
same failure again". A sweep that catches two shapes and misses a third is a real
improvement over no sweep, and the round-4 figures all hold. The generalisable
form, if it is worth anything: when a finding's satisfier has more than one
clause, the clauses are the checklist — re-read each satisfier as written and
tick its parts, which is cheaper than any corpus sweep and would have caught this
one. That is the last increment of "the correction stops at the cited instance"
I can see, and I do not think it is worth a further round.

### Corpus drift, which the regeneration clause is now visibly earning

Between `eb2692e` and `8274fbc` the corpus moved under this plan:
`tools/lifecycle_planner.py` went from 29 / 376 to **33 / 373**, and a new test
module landed. The C2 row is therefore already stale by 4 and 3 — and this is
**not a finding**, because the plan pins its figures `as_of eb2692e` and says the
set is regenerated at implementation time. That design decision, forced by R3-F1
and R4-F1, is doing exactly the work it was added for. The implementer should
expect every figure to have moved and should regenerate rather than reconcile.

### Coverage

**Covered, with falsifiable citations**: the four round-4 satisfiers checked
against the text that now stands, with C1's 78 + 125 = 203, C2's and C2b's
gross-equals-net status, and `test_comprehension_floor.py:29`/`:62` all
re-derived; the twin set re-derived from scratch by blob sha (44 groups, all
pairs, 28 with candidates, 26 outside the named set, 132 sites per side, each of
the plan's five "largest" entries recomputed); the byte-identity *criterion*
attacked via same-basename near-miss analysis (18 hits, all package collisions);
C2c's cost argument reasoned through the keep-changes-no-bytes property;
enforcement proved by **executing** `test_notice_install._self_hosted_twins()`
and intersecting its 44 pairs against C2c's 26 (zero uncovered), after a
path-based search had wrongly suggested 9 were unenforced; Author-accounting read
in full at `8274fbc`; corpus drift measured at both commits.

**Not covered / low confidence**: (1) still no suite run or `--collect-only` —
this is now five rounds with that gap, and Boundary B is where it closes; I did
import and execute one test module's helper, which is not the same as running the
test. (2) I did not re-verify the Chunk D manifest arithmetic at `8274fbc`; it
reproduced exactly at `eb2692e` and the corpus has since moved, so those figures
are `as_of` evidence under the regeneration clause like the rest. (3) I did not
re-audit the archived proposals this round; scope conclusions carry forward from
rounds 1 and 4. (4) My "no near-identical enforced pair" result covers `.py`
only, which is Chunk C's surface, but would not generalise to prose twins if a
later chunk reached them.

**Verdict: CLEAR.** `Status` -> `ready-to-implement`. One minor non-blocking
finding (R5-F1) with a verbatim satisfier, to land in the first Chunk C commit.
The start precondition remains unmet — `review-efficient-lifecycle` is still
`implementing` — and gates execution, not readiness.

## Response to plan review -- Claude -- 2026-08-13 (round 5)

**R5-F1 closed in the plan, not deferred to the first Chunk C commit.** The
reviewer cleared the plan and offered to let this ride; it is a paragraph, the
plan is blocked on its start precondition anyway, and an accepted finding
carried into implementation is one more thing depending on an agent remembering.
Author-accounting now names **two** invariants: the planner twins, and every
self-hosted twin against its manifest source
(`test_notice_install.py::test_every_self_hosted_twin_stays_byte_identical_to_its_source`,
`:111`), with Boundary A for C2b/C2c mapped to that file.

**The enforcement fact is recorded because it inverts a path search.** Nine of
C2c's 26 pairs are named by no test file, and `test_reference_scripts.py`
enumerates four. The real enforcer names no path — `_self_hosted_twins()`
(`:51`) derives the set from the install manifest at runtime, covering all 44
pairs. Verified by executing the derivation. This is the `AGENTS.md` rule about
opening a trigger rather than resolving a path, and a path-based search here
returns the opposite answer.

**The reviewer's increment, accepted.** My round-4 sweep covered *bolded figures*
and *residual clauses* — the two shapes the findings named. R5-F1 was neither: it
was the **second clause of a satisfier I had already accepted**. So the rule
"re-derive every claim sharing a cause" still ran against the shapes it was
handed. The cheaper generalisation is the reviewer's: **when a satisfier has
multiple clauses, the clauses are the checklist.** Three rounds produced a sweep;
one round produced a checklist that would have caught what the sweep missed.

**Corpus drift, for the implementer.** `tools/lifecycle_planner.py` moved 29/376
→ 33/373 between `eb2692e` and `8274fbc` under another agent's work. Every figure
in this plan should be expected to have moved. **Regenerate, do not reconcile** —
which is what the regeneration clauses forced by R3-F1 and R4-F1 exist for.

**Status**: `ready-to-implement` (set by the clearing review at `9af47c4`;
unchanged here). Execution still gated on `review-efficient-lifecycle` archiving.

## Record note -- Claude -- 2026-08-19

**Two citations into `bootstrap/REANCHOR_RUNBOOK.md` went stale during
implementation, and one of them cannot be repaired.**

The `ceremony-as-code` implementer rewrote the runbook (`482f0f6`, "the runbook
explains the ceremony instead of holding it"). It is now 612 lines, so both
`REANCHOR_RUNBOOK.md:734-751` (this plan's D2 fence, above) and
`REANCHOR_RUNBOOK.md:734-749` (inside the round-2 plan review) exceed the file
and hard-flag under `scripts/claim_check.py`.

**The fence's substance is intact.** `_gate_manifest.py produce` is still step 2
of a supervised ceremony, and step 3 is still a Maintainer-authored commit
carrying the new `gate_manifest.json`. D2 stays MAINTAINER-GATED on unchanged
grounds; only the coordinate moved.

**The plan-body citation is repaired by deleting its line range**, not by
re-pointing it. Re-pointing would buy one correct citation and the same failure
on the next edit; the runbook's own section headings are stable and the quoted
phrases are searchable, which is what a durable citation looks like.

**The review's citation is left exactly as written.** It was accurate when the
reviewer wrote it, and the record shows what was believed at each point — that
is the append-only rule, and a reviewer's text is not the author's to correct.
So `claim_check` will keep hard-flagging this file at that line until the plan
archives. That is the correct behaviour and not a defect to route around.

**It is also this plan's own thesis arriving uninvited.** The pass exists
because a coordinate into a closed record decays; here a *live* citation into a
*live* file decayed inside a single working day, because someone legitimately
rewrote the file it pointed into. Line numbers are the most brittle coordinate
of all — they go stale without anyone touching either the citing text or the
cited claim.

## Scope allowance -- Maintainer -- 2026-08-19

The implementer filed a **scope delta: NOT preserved** at `6140920` — 142
occurrences deferred (123 under the frozen AST baseline in
`bootstrap/_scaffold/`, 19 in the re-anchor ceremony surface) — and a separate
measured blind spot in this plan's own matching rule: two tag shapes
(`S12`/`R10`/`D14`, and `P6a`/`P6c`/`F1b`) that none of the three declared
classes can match, **246 occurrences** tree-wide before excluding live schemes.

The Maintainer's instruction, verbatim:

> Let's just get all of them done before reanchor

**What this authorizes, and what it changes.**

* **The deferral is withdrawn.** All 142 occurrences are completed under this
  plan rather than handed to a successor. The AST attestation baseline and the
  gate manifest are re-anchored *once*, afterwards, covering the whole set —
  which is the sequencing the deferral was costing.
* **The matching rule is widened**, from three classes to five, by explicit
  allowance. Widening reviewed scope mid-implementation is a deviation exactly
  as narrowing it is; this is the Maintainer granting it, not the implementer
  reading it into the ruling.
* **Boundary B moves.** `6140920` is not the final implementation commit. A run
  started against it was stopped rather than filed.

**What this does not authorize.** The liveness rule is unchanged: a coordinate
that still resolves to something live stays. `M2-4` and `M2-5` in
`bootstrap/tests/_gate_manifest.py` cite `M2`, a live row in the in-flight
`ceremony-as-code` plan, and `N4` and `M3` remain live fences. "All of them"
means every *dead* coordinate in the widened corpus, not every token matching a
pattern — sweeping a live fence because a ruling said "all" would be the same
mechanical error this plan exists to prevent.

### Correction to the scope allowance -- Claude -- 2026-08-19

The allowance above states that `M2-4` and `M2-5` in
`bootstrap/tests/_gate_manifest.py` "cite `M2`, a live row in the in-flight
`ceremony-as-code` plan" and must be kept. **That was wrong, and the reasoning
was the exact error this pass keeps recording.**

`M2` *is* live in that plan — it is the exact-byte External Security Review
step. But `M2-4` and `M2-5` appear in it **zero times**, and they are not
sub-rows of that step: they are findings from a different review round
entirely, whose numbering happens to start `M2`. Liveness was inferred from
the *parent token* rather than checked on the *occurrence*, which is the
homograph trap in a new direction — previously it produced false removals of
live tokens, here it nearly produced a false keep of dead ones.

Both are removed, along with `A2`, `A4`, `IC3`, `IC6` and `S2` in the same
file. `A2` and `A4` also have live homographs in `ceremony-as-code` (rows about
`ssh-keygen` prompting and the runbook's own claim); this file's are from
`git-native-security-foundations`, which the comment named outright.

**`bootstrap/tests/test_reanchor.py` is kept in full — all 12.** It is
`TestTheCeremonyClosureCarriesNoUnexplainedTag`, the ceremony plan's **gate on
this plan's output**: its tags are specimens in a regex spec and worked examples
in a docstring explaining the live-vs-dead rule, and its `LIVE` frozenset names
`N4`–`N8`, `R1`, `R6` exactly as this ledger dispositioned them. Sweeping it
would have deleted a test *about* not sweeping live coordinates.

## Correction: the review-basis fields -- Claude -- 2026-08-19

**The five Internal plan reviews in this artifact do not carry the four-field
review basis, and the omission is recorded here rather than repaired.**

The sections at lines 573, 950, 1319, 1591 and 1998 each declare `Reviewed
commit` and none of `Target`, `Prior findings`, or `Assurance path`. The
four-field basis became mandatory at `76bc678` (2026-08-12), **one day before
those reviews landed**, so the obligation was in force and was not met.

**Why this is a correction and not an amendment.** Those three fields are
declarations by a reviewer about the read *they* performed — what it covered,
what it carried forward, which assurance path it took. The reviewer was a
fresh-context Internal pass that no longer exists. Anyone filling them in now
is authoring a statement about someone else's read and signing it in their
name, which is precisely what the attribution rule in `AGENTS.md` > Review
exists to prevent. Amending would clear the conformance check fastest and would
be the one option that puts a false statement into the record.

**Maintainer decision**, taken on those three options (amend / append a
correction / accept until archive):

> append the correction, accept the red check

**Consequence, stated so it is not rediscovered as a defect.**
`bootstrap/tests/test_lifecycle_contract.py::test_the_live_corpus_is_sound_under_the_p1_contract`
reports **15 violations against this file and stays red until this plan
archives** — the scan globs `dev/plans/*.md`, live artifacts only. The check is
correct and the record is now honest; those are not in tension. A concurrent
plan's Boundary B record carries this as an attributed non-pass disposition
pointing here, which is the intended handling rather than a workaround.

A related defect in the same sections **was** repairable and was repaired at
`b977a18`: four `## Response to plan review` headings carried `(round N)` inside
the kind span the disposition predicate compares, silently discharging nothing.
Moving the marker after the date took the count from 19 to 15. Headings are the
author's own; a reviewer's declarations are not.

## Boundary B -- not run, by Maintainer decision -- 2026-08-19

This plan's verification contract records `**Boundary B mode**: full`. It was
not run. The Maintainer's decision:

> Given that all we changed are docstrings, comments, and docs, I do not
> believe that a Boundary B run is neeeded. This will be done elsewhere.

**One qualification on the premise, recorded so the decision rests on accurate
facts.** The change is *almost* entirely prose. The exception is **Chunk D,
which renamed 38 test containers** — a real code change that alters class
bindings and every pinned node id beneath them. What it received instead of
Boundary B:

* **842 tests passed** across the three files holding all 38 renames
  (`test_lifecycle_contract.py`, `test_pilot_evidence.py`,
  `test_security_verification.py`), at `75687c8`.
* A tree-wide grep for each old name before renaming. Every hit outside its own
  file was **prose** — proposals, plans, `dev/PLANNING.md`, `doctrine/` — except
  one live cross-reference in engine code (`bootstrap/_scaffold/config.py:112`),
  which was updated in the same commit and verified attestation-neutral.
* The 38 new names were checked unique, and the matching rule returns **0**
  afterwards.

**The remaining hazard is the one Boundary B would not have caught either.**
`bootstrap/tests/fixtures/gate_manifest.json` pins **335 node ids naming the
renamed classes**. That is **D2**, MAINTAINER-GATED, and it regenerates under
the re-anchor ceremony — which is also where the integration evidence for this
change belongs, since the ceremony rewrites the AST baseline, the gate manifest
and the install lockfile, and changed fixture bytes would invalidate any
Boundary B record taken before it.
