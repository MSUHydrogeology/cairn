<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/lifecycle.md doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: the review-before-implement gate checks the review, not its presence

**Source proposal**: `dev/proposals/archive/2026-08-04-claude-review-gate-enforcement.md`
**Status**: open
**Plan review**: required(**External**) — carried from the proposal header and
re-affirmed in the Decision: *"the replacement mechanism … was authored after the
External round and has not been read by a different agent type. The plan is
where it gets that read."* **Discharged**: see *Review disposition* below.
**Last update**: 2026-08-05
**Opened**: 2026-08-04

## How to read this plan — precedence

**The operative contract is the plain plan text: *Scope*, *Review disposition*,
*The settled record schema*, *Sequence*, *Acceptance criteria*, *Verification*.
An implementer who reads only those sections executes the current spec.** The
review-driven decisions of both External rounds are **folded into those
sections in place**, which `doctrine/plans.md:202-207` permits while a plan's
status is `open` with no commits in flight against the chunks being edited —
both true of this plan (status `open`; `git log` shows no implementation commit
against Chunks A–D).

**This supersedes the 2026-08-05 Response's precedence clause** (*"where a row
and the text it supersedes disagree, the row governs"*). That clause existed
because the Response believed append-only forbade editing chunk cells; it does
not. The *Amendments in force* table is now a **folded ledger** — a record of
how the operative text was reached, with each row marked with the cell that
carries it. Where a row and the operative text disagree, **the operative text
governs**; a row marked `SUPERSEDED` was changed again by the 2026-08-05 S11
round and its "In force" column is history, not instruction.

The `## Plan review`, `## Code review`, `## Lasting-truth migration` and every
landed review / Response section are **append-only and untouched**.

## Source proposal

The gate in `tools/lifecycle_planner.py` clears on the *presence* of a section
named "Plan review", not on the review its own doctrine describes. Four
documented promises — the declared tier, the `##` heading level, the date, and a
`### Sharpening` subsection when findings were raised — are unenforced. Accepted
as revised on 2026-08-04 with one condition, quoted in *Scope* below. The
External review reduced the fix from "enforce the four rules" to "make the
record able to carry them, then enforce what it carries".

**Cite by symbol, not by line** (folds Amendment row 12). The proposal's
`:787` was correct at `8dfb664` and is stale: the defect lives in `_has_kind`
and in its two callers `_conformance_violations` and `_gating_preconditions`.
Re-measured `as_of 2026-08-05` at `ec57bf0`: `_has_kind` at `:697`, the two
gating `_has_kind(art, "Plan review")` calls at `:791` and `:865`. Those line
numbers are a convenience and **will move again** — S12 names the symbols, and
the symbols are what an implementer greps for.

## Scope

**The Decision's condition, verbatim, because it is this plan's shape:**

> on the condition that the plan reconciles the ##/### grammar across doctrine,
> both plan templates and the planner scaffold before gating on it, and treats
> the adopter-facing record-format change as in scope

### In scope

* `doctrine/plans.md` — the grammar reconciliation, and the review-record format.
* `dev/plans/_template.md` and `templates/core/dev/plans/_template.md` — the
  shipped containers, which must agree with the reconciled grammar.
* The planner's generated plan scaffold.
* `tools/lifecycle_planner.py` and its byte-identical twin
  `templates/skills/_lib/lifecycle_planner.py`.
* `bootstrap/tests/test_lifecycle_contract.py` — the new nodes.
* `scripts/gen_legacy_passes.py` — **new file**, the legacy-manifest generator
  required by S9(c). Does not exist yet; it is a Chunk C deliverable.
  <!-- claim-check-allow: scripts/gen_legacy_passes.py -->
* `bootstrap/UPGRADE.md` — the adopter-facing disclosure home (D.1). Exists
  today (18,170 bytes `as_of 2026-08-05` at `ec57bf0`), with a
  `## Migrating a tree installed before upgrade support` section at `:170` as
  precedent.

### Out of scope, fenced

* **Authenticating independence.** Per `[E4]`, this tool is a **conformance
  backstop**. It cannot establish that the declared review happened, and nothing
  in this plan may claim otherwise — including violation text.
* **`doctrine/lifecycle.md:175-182`.** It states the gate is *"explicit, not
  remembered"*, which stays true. Chunk D of `gate-claims-vs-enforcement` is
  concurrently editing `:218-221` of the same file; these do not overlap and
  this plan does not touch that region.
* **Adopter tree migration.** Two internal adopters, Maintainer-managed
  (Decision context). This plan ships the migration *note*; running it is the
  Maintainer's.

## Review disposition — the External round is closed

**This section is the operative implementation gate.** It folds Amendment row 3,
which superseded the `## Plan review` container's sentence *"Implementation does
not start until a review has landed under this heading."* That sentence is
withdrawn as the gate: **"under this heading" describes a nesting the
append-only lifecycle cannot produce** — an appended `###` pass nests under the
file's *last* H2, never under an earlier container — and it is the wording that
let this plan's presence gate clear on two REVISE verdicts. The container is a
landed section and is **not edited**; it is simply no longer the gate. The three
conditions below are.

**D1 — a conforming External pass has landed.**
`## Plan review -- Codex (External) -- 2026-08-05`, introduced by `e1b2e30` — the
**second** occurrence in this file of heading digest `01bf85bb1d9a5d18`, cited by
digest and occurrence rather than by line because folding moves lines and does
not move digests — is the S11 different-agent-type read of S1–S13 and
the Amendments table. It is the **first pass in this file that carries the S2
attestation lines** (`**Tier**: External`, `**Findings**: raised`) with a
`### Sharpening` inside its own body — so it conforms to the schema it reviewed.
*Determined by reading the pass, not by running the tool.* The tool cannot
supply this: measured at `ec57bf0`, `_conformance_violations` returns `[]` for
this file and would clear it on presence alone, which is the defect under
repair. **The artifact under verification must not supply the material used to
verify it**, and here the tool is that artifact.

Confirmed mechanically against S1/S2/S7 *as written above* — an independent
walk of this file's H2 sections, not the gate — `as_of 2026-08-05`: of the three
S1 passes, **exactly one** carries `**Tier**` and `**Findings**` with a
`### Sharpening` in its own body, and it is this one. The other two are legacy by
S10's manifest rows. So this plan's own bootstrap is not an argument; it is a
measured property of the file.

**D2 — the reviewer's own stated condition for discharge is met.** The S11 round
closed its prior `[E5]` objection (*"its precedence clause makes the settled
schema part of the operative contract"*) and raised two findings. Its Sharpening
states the discharge condition:

> Once the legacy set and date semantics are made non-gameable in the binding
> schema, S11 can be considered discharged by this round without seeking another
> broad redesign.

Both named changes are in force in *The settled record schema* below:
**S9 (replacement)** removes the date from admission entirely — the legacy
population becomes a closed, generated enumeration keyed by plan stem, with
occurrence counts — and **S1 (amended)** requires the captured date to parse
under `datetime.date.fromisoformat`. The condition is met **as the reviewer
worded it**; this is not an author assertion that the findings were minor. They
were the sharpest findings in the round: a plan that repairs the review gate had
a forgeable review-record schema.

**D3 — the Maintainer has disposed of the REVISE round.** This plan's fences
read *"the External reviewer, **or the Maintainer**, disposes of the REVISE."*
The Maintainer's authorizing instruction, verbatim and visually isolated:

> Go ahead with implementation once you've revised these. I don't want another review round

That instruction **is** that disposition, cited as such and not as a bypass: the
findings are folded into the operative text *before* any implementation commit,
which is the "once you've revised these" clause. It is bounded — it disposes of
**the review round only**. It does **not** supply a Maintainer credential, a
signing ref, an AST re-anchor ceremony, or approval to push. Anything in Chunks
A–D that needs one of those still waits on the Maintainer.

**What is consequently in force.**

* **S11 is discharged.** No further External round is sought for this plan.
* **The "before Chunk A's first commit" precondition stated in S11 — and relied
  on by S10 — is MET**, by `e1b2e30` together with D2 and D3. Chunk A may take
  its first commit.
* The two REVISE verdicts (2026-08-04; 2026-08-05 first round) stand as
  **history**. No implementation commit cites a REVISE, the presence gate, or an
  author Response as its authority; it cites this section.

## The settled record schema — operative plan text

**This section is the schema.** It carries S1–S13 with the S11 round's two
findings folded in. Identically-numbered clauses inside the 2026-08-05 Response
are the append-only record of how the schema was *authored*; **this section
governs**, and where the two differ (S1, S9, S10) the difference is the fix and
is called out below.

**S1 — the pass heading.** A *plan-review pass* is a heading matching exactly

```
^## Plan review -- (?P<reviewer>[^\n]+?) -- (?P<date>\d{4}-\d{2}-\d{2})(?: \(round (?P<n>\d+)\))?$
```

H2, because H2 is the only level an appended record can produce under a template
whose last H2 is `## Lasting-truth migration`. The `(<role>)` parenthetical that
`_HEADER_RE` already accepts inside `<reviewer>` stays **permitted and
informational** — see S4.

**S1 is amended by the S11 round: the date must be a real date.** The regex
gives the *shape* only. The captured value must then parse under
`datetime.date.fromisoformat` (stdlib, strict). A shape match whose value does
not parse is a violation, **`malformed date`** — not a legacy exemption, and not
a silent pass. Measured directly, `as_of 2026-08-05` under
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13):

| value | `^\d{4}-\d{2}-\d{2}$` | `date.fromisoformat` |
|---|---|---|
| `2026-99-99` | matches | `ValueError: month must be in 1..12` |
| `2026-02-30` | matches | `ValueError: day is out of range for month` |
| `0000-00-00` | matches | `ValueError: year 0 is out of range` |
| `2027-02-29` | matches | `ValueError: day is out of range for month` |
| `2028-02-29` | matches | accepted — `datetime.date(2028, 2, 29)` |

The low direction was the dangerous one under the old S9: `0000-00-00` sorts
before every real epoch under a string comparison. S9's replacement removes the
comparison, and this amendment removes the impossible value as well, so the two
fixes are independent rather than one covering for the other.

**S2 — the attestation lines.** Inside a pass body (after the S1 heading, before
the next H2), exactly one line each, full-line anchored:
`**Tier**: <Internal|External>` and `**Findings**: <none|raised>`.
Value comparison is case-insensitive; the canonical spellings are `Internal`,
`External`, `none`, `raised`.

**S3 — closed vocabulary, three fail-closed directions.**

| condition | verdict |
|---|---|
| value outside the vocabulary | violation: `unrecognized <field> value` |
| field absent from the pass body | violation: `missing <field>` |
| field occurs more than once in one pass body | violation: `duplicate <field>` — **even when the occurrences agree**; agreement is a judgement a conformance backstop must not make |

No condition yields a silent pass. There is no default value for either field.

**S4 — declared, never inferred.** The checker reads the tier from the
`**Tier**:` line and from nowhere else. It must **not** derive it from the
reviewer name, the `(role)` parenthetical, `_load_ai_registry`, the
human-maintainer roster, or byline classification. A human reviewer declares
`**Tier**: External` in the same shape an agent does. The `(role)` parenthetical
remains free text and is **not read by the gate** — stated explicitly so it
cannot drift into a second, softer source of truth. Violation text never uses
the language of authorization: the tool attests that a tier was *declared*,
never that it was *true*.

**S5 — tier ordering.** Total order `External > Internal`. A pass satisfies the
floor iff `declared >= required`. `External` satisfies a required `Internal`;
`Internal` does not satisfy a required `External`. There is no third tier and no
`Maintainer` tier — a human review declares `External`.

**S6 — normalizing the required tier.** Defined on the **first parenthesised
group only** of the `**Plan review**:` field:

1. match `^required\s*\(([^)]*)\)` case-insensitively; no match → violation
   `tier not declared`;
2. delete every `*`, `_` and backtick from the group;
3. take the **first alphabetic word** (`^[A-Za-z][A-Za-z-]*`);
4. case-fold; it must be `internal` or `external`, else violation.

Text after the closing `)` is ignored (every live review-required plan has
some). Text after the first word *inside* the group is a **lens annotation** —
preserved in the record, ignored by the tier comparison. Negations fail closed:
`required(not External)` → step 3 yields `not`, which is outside the vocabulary →
violation. `not required(<rationale>)` disables the gate, unchanged. The live
`required(...)` forms this must resolve are **re-enumerated at the gating
commit**, not carried from the Response — see Chunk C's C.6 cell for the
population, the invariant, and the measured fact that a comma-splitting
normalizer rejects three of them.

**S7 — Sharpening pairing is positional.** When a pass declares
`**Findings**: raised`, a heading matching `^### Sharpening\b` must occur
**inside that pass's body** — between its S1 heading and the next H2.
Positional, not date-matched: a sibling round's Sharpening cannot satisfy
another round. When `**Findings**: none`, a Sharpening in the body is permitted
and not required. `Sharpening` enters `_KNOWN_KINDS`; verified absent at
`ec57bf0` (`_KNOWN_KINDS` = `{review, response, revised, decision, plan, code}`,
`tools/lifecycle_planner.py:519`), which is why the scaffold's own emitted block
parses to nothing.

**S8 — what the gate decides.** For a plan whose field is `required(<tier>)`:
every S1-matching pass must satisfy S2, S3 and S7 (each failure is a violation);
**and** at least one S1-matching pass must satisfy S5. Both conditions must
hold. A heading beginning `Plan review` that does not match S1 is neither a pass
nor a violation — and can no longer clear anything, because clearing now
requires an S1 match. **Near misses fail closed as "no conforming pass has
landed", never as "a pass with problems"**, and the violation text must quote
the near-miss heading so the author is not left guessing.

### S9 (replacement) — the legacy population is enumerated, not dated

**This replaces the dated-epoch S9 in the 2026-08-05 Response entirely.** That
version exempted a pass dated **strictly before** `_REVIEW_SCHEMA_EPOCH`,
reading the date from the S1 heading — *author-written text inside the artifact
the gate judges*. So appending `## Plan review -- Any Name -- 2020-01-01` bought
a permanent exemption from S2/S3/S7 **and** satisfied the review floor by
presence. The old S9(d) asserted "it cannot become a second grammar"; as written
it **was** the second grammar, reachable by typing a smaller number. There is no
`_REVIEW_SCHEMA_EPOCH` in this plan any more.

* **(a) A closed manifest, not a threshold.** `_LEGACY_PASSES` in
  `lifecycle_planner.py`: a module-private mapping from **plan stem** to a
  multiset (`dict[str, dict[str, int]]`) of `sha256(heading_line)` hex digests
  truncated to 16 chars, with the count of occurrences admitted for each digest.
  Keyed by *stem*, not path, so an archive move — the same stem relocating from
  `dev/plans/` to `dev/plans/archive/` — does not drop a file out of the
  exemption.
* **(b) The fence.** A pass is *legacy* — exempt from S2, S3 and S7, satisfying
  the floor by presence exactly as today — **iff** its stem is in the manifest
  and this is the k-th occurrence of its heading digest in that file with
  `k <= manifest_count`. Every other pass, **whatever its date**, gets no
  exemption.
  * **The duplicate-append hole is closed by the count.** Re-appending a heading
    byte-identical to an admitted one yields occurrence `manifest_count + 1`,
    which is **not** legacy. Without the count, copying an admitted heading
    would reopen the bypass; with it, the manifest admits exactly the passes that
    existed when it was generated and no more.
  * **This is not hypothetical — this plan is the worked example.** Measured
    `as_of 2026-08-05` at `ec57bf0`, this file carries **three** S1 passes with
    only **two** distinct digests: `## Plan review -- Codex (External) --
    2026-08-05` appears **twice**, byte-identical (digest `01bf85bb1d9a5d18`,
    occurrences 1 and 2). A set-valued manifest would admit that digest forever;
    the multiset admits it exactly twice and refuses a third. Cited by digest and
    occurrence, never by line: a fold moves lines and leaves digests fixed, which
    is the property the manifest is keyed on.
  * **Editing an admitted heading fails closed.** Its digest leaves the
    manifest, so it stops being legacy and must then satisfy S2/S3/S7. That is
    the correct direction, and append-only already forbids the edit.
* **(c) Generated once, by something that is not the checker.** A committed
  generator, `scripts/gen_legacy_passes.py`, run once at Chunk C, walks
  `dev/plans/`, `dev/plans/archive/`, `dev/proposals/` and
  `dev/proposals/archive/` with an **exact-anchored regex of its own** and emits
  the manifest literal. **It must not call `_pass_headings`, `_has_kind`, or any
  other predicate under repair** — the population the gate exempts cannot be
  defined by the gate. Chunk C's commit message records the totals the generator
  found; **no count is frozen into this plan**, because the corpus moves faster
  than the plan does (see C.0).
* **(d) Why it cannot become a second grammar — now true.** The manifest is a
  **closed literal**. Widening it requires editing a committed constant, which
  shows up as a code diff in review; **there is no value an author can type into
  a *plan* that adds a pass to it.** Three pinning nodes, all in
  `bootstrap/tests/test_lifecycle_contract.py` (C.9a–C.9c):
  1. a pass whose heading is not in the manifest is refused without S2 fields,
     **whatever its date** — including a date decades in the past;
  2. re-appending an admitted heading a second time is refused, exercised at
     exactly `manifest_count + 1`;
  3. the manifest is re-derived by re-running the generator and compared —
     **subset direction only**, see the honesty note below.
  `bootstrap/UPGRADE.md` states that the exemption is a **fixed enumeration of
  pre-existing records**, not a dated grace period.
* **(e) The date plays no part in admission.** It remains *required syntax*
  under S1 (and must now be calendar-valid) and is **informational only**.
  Nothing in the gate compares it to anything, so there is no comparison
  operation left to specify — the S11 finding *"specify … the comparison
  operation used by S9"* is answered by **removing the comparison**, not by
  defining it.
* **(f) What (d)(3) does and does not catch — stated, not implied.** Re-running
  the generator at test time asserts that **every manifest entry corresponds to
  a heading actually present at that stem, with at least that many
  occurrences**. The reverse direction is *deliberately not asserted*: a pass
  appended after Chunk C legitimately exists in the tree and legitimately is not
  in the manifest, so an equality check would redden the suite on the next
  review that lands. Consequently (d)(3) catches a **fabricated** manifest entry
  and manifest drift; it does **not** catch a manifest entry added for a real,
  newly-appended pass, and it does **not** catch a defect in the generator's own
  regex — the generator is the manifest's producer, and a producer cannot
  falsify its own output. Those two residual risks are covered by human review
  of a code diff, which is (d)'s actual control, and by reviewing the
  generator's regex at Chunk C against S1 as written here. Recorded so no reader
  mistakes (d)(3) for provenance it does not supply.

**S10 — this plan's own bootstrap, named.** The three passes below are admitted
as legacy **by manifest entry**, not by date, and without rewriting them (which
append-only forbids). They are ordinary members of the enumeration
`scripts/gen_legacy_passes.py` produces; **no file-specific carve-out exists or
is needed.**

| pass heading | occurrences | digest |
|---|---|---|
| `## Plan review -- Codex (External, different-agent-type) -- 2026-08-04` | 1 | `26f5c121f879971d` |
| `## Plan review -- Codex (External) -- 2026-08-05` | **2** (the 2026-08-05 first round, and the S11 round from `e1b2e30`) | `01bf85bb1d9a5d18` |

The Response's sentence *"All are dated strictly before any achievable epoch"*
is **superseded — there is no epoch.** Its third bullet, "the S11 round,
whenever it lands", is resolved: the S11 round landed in `e1b2e30` and is the
second occurrence of digest `01bf85bb1d9a5d18`. Line numbers and digests here
are `as_of 2026-08-05` at `ec57bf0` and are **re-derived by the generator at
Chunk C**, never transcribed from this table into the manifest literal.

**S11 — the second External round: DISCHARGED.** Required by `[E2]`, re-demanded
by `[E5]`, performed at `e1b2e30` as a read of S1–S13 and the Amendments table.
See *Review disposition* > D1–D3 for what discharged it and for the exact bounds
of the Maintainer's instruction. Its own pass is legacy-admitted by S10's
manifest row. **No further External round is sought.**

**S12 — one predicate, both call sites.** A single module-private pair —
`_review_conformance(art) -> List[str]` and `_review_satisfies_floor(art) -> bool`
— consumed by **both** `_conformance_violations` and `_gating_preconditions`. A
node asserts both surfaces return the same verdict on the same fixture, so
`scan` cannot tighten while `next --to executing` stays presence-only. Cited by
symbol per row 12; `as_of 2026-08-05` at `ec57bf0` the duplicated
`_has_kind(art, "Plan review")` calls sit at `tools/lifecycle_planner.py:791`
and `:865`, and `_has_kind` itself at `:697`.

**S13 — the twin.** Every change lands identically in
`tools/lifecycle_planner.py` and `templates/skills/_lib/lifecycle_planner.py`.
Verified by `test_every_self_hosted_twin_stays_byte_identical_to_its_source` in
`bootstrap/tests/test_notice_install.py:98` — run by a person typing
`python -m pytest bootstrap/tests`. **Cairn has no CI**; nothing runs this on a
push, and the repository's only `pre-commit` hook runs the intent check, not the
suite.

## Sequence

### Chunk A — reconcile the grammar (no behaviour change)

The blocker `[E2]` named: `doctrine/plans.md` contradicts itself. `:115` requires
*"a dated `## Plan review` section"*; `:422` prescribes *"### Plan review --
<reviewer> -- YYYY-MM-DD"* as the per-pass format. Both plan templates ship a
`## Plan review` container with `###` passes inside.

**No corpus figure is carried in this section** (folds Amendment row 11). The
figure that stood here — `grep -rhoE "^#{2,3} Plan review" …` reporting `58
headings, all ##` — is **withdrawn as evidence**: it is a *prefix* match, and
`_has_kind` gating on `startswith` is the very defect under repair, so the
measurement used the bug to measure the bug. It survives verbatim in the folded
ledger (row 11) as history. Every inventory in this plan uses the **exact
structural oracle** of S1, and is re-measured at the commit that gates — see
**C.0**. Practice follows `:115`; the instructions say `:422`; that direction
never depended on the count.

| # | File | Change |
|---|------|--------|
| A.1 | `doctrine/plans.md` | State **one** grammar per **S1**: a dated `## Plan review -- <reviewer> -- YYYY-MM-DD` **pass at H2**, with its `### Sharpening` at H3 inside it. `doctrine/plans.md:115` (`##`) and `:116` (`### Sharpening`) are **already correct and stay**; `:422` is the line that changes, from `###` to `##`. Verified `as_of 2026-08-05` at `ec57bf0`: `:115` reads "`executing` only after a dated `## Plan review` section lands: the review", `:116` reads "**and**, when it raised findings, a dated `### Sharpening` subsection", `:422` reads "`### Plan review -- <reviewer> -- YYYY-MM-DD`". |
| A.2 | `dev/plans/_template.md`, `templates/core/dev/plans/_template.md` | Make both agree with A.1. They must stay in step — a template that disagrees with doctrine reproduces this defect for every adopter. **Also reconcile the "Optional" contradiction**: both templates call the section "*Optional; pre-implementation.*" (`dev/plans/_template.md:264`, `templates/core/dev/plans/_template.md:241`, verified `as_of 2026-08-05` at `ec57bf0`) while `doctrine/plans.md:113` makes the metadata line mandatory with "**no silent default**". The empty `## Plan review` container is removed or made **explicitly non-attesting** — an empty container must not read as a landed review. |
| A.3 | The planner's generated plan scaffold | Emit the A.1 shape **and the S2 fields**. Today `tools/lifecycle_planner.py:986-990` emits `### Plan review -- <reviewer> -- <date>` followed by `### Sharpening -- <author> -- <date>` — **a block its own parser discards**: verified, a document of exactly that shape parses to `[(2, 'Plan review')]`, because `sharpening` is not in `_KNOWN_KINDS`. The scaffold must emit an H2 pass carrying `**Tier**:` and `**Findings**:` lines with an H3 `### Sharpening` inside the pass body. |

**No gating in this chunk.** It lands green and changes no verifier behaviour.

### Chunk B — the record can carry a tier and an outcome

`[E1]` and `[E3]`: today's record cannot express what the gate would need to
read. A role field is free text — and the published format has none.

| # | File | Change |
|---|------|--------|
| B.1 | `doctrine/plans.md` | Implement **S1–S6** exactly: field names `**Tier**` and `**Findings**`, vocabularies `Internal\|External` and `none\|raised`, the three fail-closed directions of S3, the S4 no-inference rule, the S5 ordering, and the S6 normalizer. **Also document the S1 date amendment** — the value must parse under `datetime.date.fromisoformat`, and a shape-only match is `malformed date`. The *declared, not authenticated* framing is carried by S4 and must appear in the doctrine text, not only here. |
| B.2 | both templates + scaffold | Carry B.1's fields, in the S1/S2 shape (H2 pass, `**Tier**:` and `**Findings**:` lines, H3 `### Sharpening` inside the body). |
| B.3 | `tools/lifecycle_planner.py` + twin | Parse the S2 fields, the S1 date (via `date.fromisoformat`), and the S6-normalized required tier. Admit `Sharpening` to `_KNOWN_KINDS` — verified absent at `ec57bf0` (`:519`), which is why **the scaffold's own emitted block** (`:986-990`) parses to nothing. **Parse only; gate nothing yet.** |

### Chunk C — gate on what the record now carries

Only here does behaviour change. Each rule gets a node with a **single-property
falsifier**: a mutation that reddens that node and **no other**. Five tests that
could not fail were found in this repository this cycle; the plan that guards
reviews will not add a sixth.

**Every node below lives in `bootstrap/tests/test_lifecycle_contract.py`, and the
only thing that runs it is a person typing `python -m pytest bootstrap/tests`.**
Opened and confirmed: that command collects this file (33 nodes collected from it
`as_of 2026-08-05` at `ec57bf0`, `33 passed in 1.86s` under
`/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13).
**Cairn has no CI** — there is no `.github/workflows/`, and the only
`pre-commit` hook runs `tools/intent.py _precommit_check`, not the suite. Nothing
runs these nodes on a push or a merge. **The baseline is re-measured immediately
before the gating commit, not carried from here**: it was reported as `30` on
2026-08-04 and is `33` now, i.e. it has already moved once within this plan's
lifetime.

| # | Rule | Node | Single-property falsifier |
|---|------|------|---------------------------|
| C.1 | S8 floor: at least one S1 pass satisfies S5 | new | delete the tier comparison → this node red, others green |
| C.2 | S1 heading match (H2, `--` separator, ISO-shaped date) | new | accept H3 → red; accept an undated pass → red; accept `## Plan review tier` / `## Plan reviewers` → red. Each falsifier reddens C.2 and no other node. |
| C.3 | S1 date is **calendar-valid**, not merely date-shaped | new | drop the `date.fromisoformat` parse and keep only the shape regex → red. Fixtures: `2026-99-99`, `2026-02-30` and `0000-00-00` each yield `malformed date`; `2028-02-29` (a real leap date) is **accepted**. The negative fixtures pin the fail-closed direction; the leap fixture pins that the parse is not merely a stricter regex. |
| C.4 | **S7 positional** pairing: a `### Sharpening` inside *that pass's* body when it declares `**Findings**: raised` | new | drop the conditional → red; **and** move a sibling round's Sharpening outside the pass body → red (a neighbouring round's Sharpening must not satisfy this one) |
| C.5 | S3 three directions | new | unknown / missing / duplicate `**Tier**` or `**Findings**` → violation, **one falsifier each**. The duplicate case uses two *agreeing* occurrences, since agreeing duplicates are the case a backstop must still refuse. |
| C.6 | S6 normalization | new | every live `required(...)` form in the tree resolves; `required(not External)` and `required()` fail closed (measured: they normalize to `not` and to nothing, neither of which is in the vocabulary). **The form list is enumerated at the gating commit** by the C.0 oracle, *not* copied from this plan: the Response measured **6** distinct forms across **31** plans, and re-measurement `as_of 2026-08-05` at `ec57bf0` gives **7** forms across **32** plans — a new unbolded `External + External Security Review` variant appeared. The invariant, which does not move: **every review-required plan in the tree resolves to exactly one of `internal` / `external`, and no form resolves by accident.** Falsifier: substitute a comma-splitting normalizer → red, because it rejects **3** of the 7 live forms (both `+` forms and `**External cross-type**`). S6's first-alphabetic-word rule resolves all 7, verified directly. |
| C.7 | S5 ordering | new | `Internal` on an `External` floor → red; `External` on an `Internal` floor → green |
| C.8 | S12 one predicate, both call sites | new | both `_conformance_violations` and `_gating_preconditions` return the same verdict on the same fixture; making one strict alone → red |
| C.9a | S9(b) — non-manifest pass gets no exemption | new | a pass whose heading digest is **not** in `_LEGACY_PASSES` is refused without S2 fields **whatever its date**, including a date decades in the past (`2020-01-01`) and `0000-00-00`. Removing the manifest lookup and restoring any date comparison → red. **This is the node that pins the S11 finding closed.** |
| C.9b | S9(b) — the occurrence count | new | re-appending a heading byte-identical to an admitted one is refused at exactly `manifest_count + 1`. Fixture uses a stem whose manifest count is **2**, so the node exercises the boundary rather than the `1 → 2` edge; this plan's own `## Plan review -- Codex (External) -- 2026-08-05` (digest `01bf85bb1d9a5d18`, count 2) is that shape. Changing the multiset to a set → red. |
| C.9c | S9(c)/(f) — the manifest is not hand-editable | new | re-run `scripts/gen_legacy_passes.py` and assert **every manifest entry corresponds to a heading present at that stem with at least that many occurrences** (subset direction). Adding a fabricated entry → red. **Asserting equality instead → red on the next legitimate review that lands**, which is why the direction is one-way; see S9(f) for what this node does *not* catch. |

**C.0 — the pre-C inventory, a deliverable of this chunk and not a note.**
**Before C lands, run the reconciled gate over every artifact in `dev/` and
record which newly violate.** A gate that reddens the existing tree needs that
disclosed up front, not discovered. Folding Amendment row 15, `[E4]`'s addition
is binding: **evaluate open plans as if transitioning to `executing`**, not only
in their current state — an old-format review stays green while status is `open`
and fails only later, so a current-state scan reports a clean tree and is wrong.

*What supplies the material, stated because it matters twice here:*

* **The corpus inventory** (how many S1 passes, bare containers and near-miss
  headings exist, and their `required(...)` forms) is produced by the **exact
  anchored regex of S1**, run by `scripts/gen_legacy_passes.py --report` over
  `dev/plans/`, `dev/plans/archive/`, `dev/proposals/` and
  `dev/proposals/archive/`. Never by `_has_kind`, never by a prefix grep. The
  generator is deliberately **not** the gate (S9(c)), so the population is not
  defined by the predicate under repair.
* **No corpus figure is stated in this plan, by decision.** The measured record:
  the loose `^#{2,3} Plan review` count went **58** (`8dfb664`, 2026-08-04) →
  **71** (`da1de65`, 2026-08-05) → **79** (`ec57bf0`, 2026-08-05), and it moved
  *twice inside a single session*. Under the exact S1 oracle at `ec57bf0` the
  same trees give **52** dated passes, **5** bare containers, **22** unrelated
  `Plan review*` headings across 75 files — three figures that will be wrong by
  the time Chunk C runs. What is stable is the **invariant**: *every dated pass
  in the corpus is H2 and there are zero H3 dated passes* (0 at `8dfb664`, 0 at
  `da1de65`, 0 at `ec57bf0`). Assert the invariant; re-measure the counts at the
  gating commit; carry nothing forward.
* **The violation inventory itself is produced by the code under test** — it must
  be, since the question *is* what the new gate refuses. It is therefore a
  **disclosure, not a verification**: it shows what the new gate does to the
  live tree, and it is not evidence that the new gate is correct. That evidence
  comes only from C.1–C.9c and their demonstrated falsifiers.

### Chunk D — the adopter-facing disclosure

| # | File | Change |
|---|------|--------|
| D.1 | **`bootstrap/UPGRADE.md`** | State the record-format change, the two affected fields, and what an adopter must do. Its **durable home** is `bootstrap/UPGRADE.md` — which exists, and already carries a `## Migrating a tree installed before upgrade support` section (`:170`) as precedent. It must state the two field names (`**Tier**`, `**Findings**`), the S6 normalizer, the S1 calendar-valid date rule, and that the legacy exemption is a **fixed enumeration of pre-existing records — not a dated grace period and not an epoch**. **There is no `_REVIEW_SCHEMA_EPOCH` value to publish**; that construct was removed by S9's replacement, and an UPGRADE note that names an epoch is wrong. The twin is a `verbatim` manifest source installed as `tools/lifecycle_planner.py`, so behaviour and policy ship together. |
| D.2 | `CHANGELOG.md` > Unreleased | One line. **Serialized: text returned, not edited in-agent.** |

## Acceptance criteria

* `doctrine/plans.md`, both templates and the scaffold state **one** grammar,
  verified by an **exact structural oracle** over all four surfaces — never a
  grep. The old criterion *"a grep … returns one shape"* is **withdrawn**: it is
  incoherent against a grammar that deliberately contains an H2 pass and an H3
  Sharpening, and a prefix grep is the very defect under repair.
* The twins stay byte-identical —
  `test_every_self_hosted_twin_stays_byte_identical_to_its_source`, in
  `bootstrap/tests/test_notice_install.py:98`, run by `python -m pytest
  bootstrap/tests`. True now: `md5 457b51c7772da181e838f99a2205d933` for both
  `tools/lifecycle_planner.py` and `templates/skills/_lib/lifecycle_planner.py`,
  `as_of 2026-08-05` at `ec57bf0`.
* **The coverage set C.1–C.9c** in `bootstrap/tests/test_lifecycle_contract.py`,
  each with its single-property falsifier **demonstrated** — the falsifier is run
  and the red/green matrix recorded, not asserted. The count "four" is
  **withdrawn**; the set is the criterion.
* Suite: **no *new* failure relative to a baseline measured immediately before
  the commit on a quiet tree**, `0 skipped`. Not "green" unconditionally: the
  tree carries concurrent work. The `test_lifecycle_contract.py` figure is
  **`33 passed` `as_of 2026-08-05` at `ec57bf0`** and is a *snapshot, not the
  baseline* — it was `30` on 2026-08-04, so re-measure at the gating commit and
  state the revision beside the number.
* **The tree is not quiet, and that is disclosed with the baseline, not
  discovered after it.** HEAD moved `6bcd2d3` → `da1de65` → `ec57bf0` across the
  two sessions that produced this plan's schema, and a plan file changed between
  two measurement runs inside one session.
* C.0's inventory — both the corpus measurement and the newly-violating
  artifacts — is in the record **before C commits**, with the disclosure that the
  violation list is produced by the code under test.
* No violation text uses the language of authorization: the tool attests that a
  tier was *declared*, never that it was *true*, and never that a review
  *happened*.
* **`_REVIEW_SCHEMA_EPOCH` appears nowhere** in the module, the twin, the tests,
  the doctrine or `bootstrap/UPGRADE.md`. A grep for it returning any hit means
  the replaced S9 leaked into the implementation.

## Verification

* Reproduce the proposal's five-state table against the **post-change** module,
  and against **both** call sites, since S12 unifies them. The four shapes
  measured to clear the presence gate today are: an H3 dated pass, an undated
  named pass, a bare `## Plan review` container, and an `Internal`-only pass on
  an `External` floor. Add the two prefix collisions — `## Plan review tier` and
  `## Plan reviewers` — which also clear today and which S1 rejects.
* Confirm the tier attestation is parsed from the closed vocabulary and that
  **all three** S3 directions are violations rather than silent passes:
  **unrecognized**, **missing**, and **duplicate**. Unrecognized alone leaves the
  other two silent, which is the fail-open direction that matters. Add the S6
  rejections (`required(not External)`, `required()`).
* Confirm the **S1 date contract** independently of the shape regex: a
  date-shaped impossible value (`2026-99-99`, `2026-02-30`, `0000-00-00`) yields
  `malformed date`, and a real leap date (`2028-02-29`) is accepted. A regex
  shape check alone is not a date contract.
* Confirm the **legacy manifest cannot be widened from a plan file**: construct a
  pass dated `2020-01-01` whose heading is not in `_LEGACY_PASSES` and confirm it
  is refused without S2 fields. This is the direct reproduction of the S11
  finding, and it must be run against the post-change module rather than
  reasoned about.
* Confirm a conforming **human** review passes. `[E1]`'s sharpest case: the
  published format had no role field, so the original rule would have blocked
  one. Under S4 a human declares `**Tier**: External` in the same line-shape an
  agent does, and the gate reads that line and nothing else.

## Plan review

*Required — **External**. Implementation does not start until a review has
landed under this heading.* The Internal floor does not discharge it: the
replacement mechanism in Chunk B was authored after Codex's External round and
has had no different-agent-type read. A reviewer should attack **B.1's closed
vocabularies** first — that is the newest and least-examined surface, and if the
vocabulary is wrong every later chunk inherits it.

## Code review

*No review has landed.*

## Lasting-truth migration

| Truth | Home |
|---|---|
| The gate is a conformance backstop, not proof a review happened | `doctrine/plans.md`, alongside the format it validates |
| One review-heading grammar across doctrine, templates and scaffold | A.1, and the templates themselves |
| A declared tier attestation is declared, not authenticated | `doctrine/plans.md` > the review-pass format |

## Plan review -- Codex (External, different-agent-type) -- 2026-08-04

**Model**: Codex, based on GPT-5. External cross-type review at `8dfb664`,
using `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13).

**Structural-independence stance.** The plan and its replacement mechanism are
Claude-authored; I am a different agent type. I re-ran the gate fixtures and
built a fresh corpus inventory rather than treating the proposal review as
evidence for the plan.

**Steelman.** The plan correctly absorbs the proposal Decision's condition and
sequences grammar, record schema, enforcement, and adopter disclosure in the
right conceptual order. Separating parse-only Chunk B from behavior-changing
Chunk C is particularly valuable: it gives the record a chance to become
expressive before the checker refuses on missing data. The plan also preserves
the External review's central limit: this is a conformance backstop, not proof
of independence. Those are the right bones.

### Concerns

* **[E1] The chosen H2-container/H3-pass grammar is incompatible with the
  append-only file layout and drops the accepted compatibility promise
  (blocking).** The template's `## Plan review` container is followed by
  `## Code review` and `## Lasting-truth migration`. A dated `### Plan review`
  appended at the end is therefore nested under the last of those H2 sections,
  not under `## Plan review`; placing it under the earlier container requires
  inserting into prior file content rather than appending. Cairn's practice has
  converged on the structurally workable answer: my parser-based inventory of
  actual plans found **34 dated review passes, all direct H2 sections**, plus two
  bare H2 containers and no H3 passes. More importantly, the accepted proposal
  Response promised to "accept both dated forms when structurally placed";
  A.1 instead canonizes H3 and C.2 rejects any other level. That would make the
  review being appended here, and every existing dated H2 review, legacy before
  the plan finishes. Choose a grammar compatible with append-at-end lifecycle
  records. The cleanest is a dated H2 pass with its H3 Sharpening immediately
  below; remove or make non-attesting the empty template container and update
  the scaffold accordingly. If H3 remains accepted for existing adopters,
  specify its valid parentage and a grandfather rule rather than a global level
  check.

* **[E2] Chunk B does not define the closed vocabularies, so this review cannot
  conform to the format it is supposed to approve (blocking).** "Declared tier
  attestation" and "review outcome" are names for decisions, not a schema. The
  plan does not state field names, allowed values, whether External satisfies an
  Internal floor, how `required(**External**, security lens)` and the other live
  metadata variants normalize, or what missing, duplicate, and conflicting
  fields do. It also collapses the Response's still-open "one token or two"
  choice without defining how an outcome declares findings. This creates a
  bootstrap failure: the required External review lands before Chunk B exists,
  but after Chunk C this plan's own old-format review can block its transition.
  Put the exact record grammar in the plan before implementation. A minimal
  design is two independent closed fields, one for `Internal|External` tier
  attestation and one for `none|raised` findings, with unknown/missing/duplicate
  values failing closed and an explicit tier ordering. Then require a second
  External round using that settled schema before Chunk A lands, or define an
  explicit bootstrap attestation that does not rewrite this append-only review.

* **[E3] The plan leaves two gate implementations and multi-round linkage
  underspecified (blocking).** The current condition exists independently in
  `_conformance_violations` at line 787 and `_gating_preconditions` at line 860.
  I re-ran the five fixtures through both: the same four malformed records clear
  both today. Chunk C does not require a shared predicate or name both call
  sites, so `scan` can become strict while `next --to executing` stays
  presence-only, or the reverse. C.4 also says only that a Sharpening exists
  when an outcome declares findings; with multiple rounds, an unrelated
  Sharpening can satisfy the wrong review unless date/round/order pairing is
  defined. Require one module-private review-conformance predicate consumed by
  both call sites. Expand the test matrix beyond four happy-path nodes to cover
  both public surfaces, a bare container, wrong nesting, unknown and duplicate
  fields, tier ordering, and mismatched/missing round-specific Sharpening.

* **[E4] The migration evidence and deliverable are not yet executable
  (important).** The recorded command reports 58 because its pattern matches
  the prefix of any heading beginning `Plan review`; an exact anchored recount
  at `8dfb664` found **37** container/pass headings across the named trees and
  **21** different headings such as `Plan review -- the brief` or `Plan review
  tier`. The all-H2 direction is right, but the claimed denominator is not.
  Acceptance's "grep ... returns one shape" is also incompatible with a grammar
  that intentionally contains an H2 container and H3 passes. Use the parser or
  an exact structural oracle for the pre-C inventory. Evaluate open plans as if
  transitioning to `executing`, not only their current-state scan, because old
  reviews without the new fields remain green while status is `open` and fail
  only later. Finally, D.1 names only "migration note," not a file; give it a
  durable path such as `bootstrap/UPGRADE.md` and specify the exact repair or
  compatibility procedure for Cairn and both managed adopters.

### Covered

* Reproduced the five-state table against both `_conformance_violations` and
  `_gating_preconditions`; only the absent-review fixture fails today.
* Checked the Decision condition and every proposal-review disposition against
  the plan's chunks.
* Audited the live H2/H3 corpus with exact parsing rather than the plan's prefix
  grep, and checked the template section order that controls Markdown nesting.
* Inspected both gate call sites, the scaffold, `doctrine/plans.md`, both plan
  templates, and the twin/install surface.
* Ran `bootstrap/tests/test_lifecycle_contract.py`: **30 passed in 1.27s** under
  Python 3.13.13. The plan itself passed `scripts/claim_check.py` before this
  section was appended.

### Not covered / low confidence

I did not inspect either adopter tree, choose the final field names on the
Maintainer's behalf, or implement a prototype multi-round parser. I did not run
the full suite because this is a plan review and concurrent repository work is
outside this plan's surface. The exact migration population must therefore be
re-measured at implementation time.

### Recommendation

**REVISE. No implementation commit should land on the presence of this review.**
The scope and high-level chunk order are sound, but the plan must settle an
append-compatible grammar, specify the closed record schema and its own
bootstrap, unify both gate call sites, and give migration a real home before it
is executable.

## Response to plan review -- Claude (author) -- 2026-08-04

**All four findings accepted; two of them correct errors of mine.** The grammar
in Chunk A is **inverted**, not adjusted, and the corpus figure in *Sequence*
measured the wrong population. Status stays `open`: `[E2]` establishes this plan
cannot proceed on this review's strength, and the Response says so below.

**The error worth naming first.** The recorded command
`grep -rhoE "^#{2,3} Plan review"` is a **prefix match**, and the defect this
whole plan exists to fix is that `_has_kind` gates on `startswith`. I measured
the prefix bug using the prefix bug. Exact recount at `f83f20e`, by full
heading text rather than prefix:

| heading shape | count |
|---|---|
| `## Plan review -- <reviewer> -- <date>` — actual dated passes | **35** |
| `## Plan review` — bare containers | 3 |
| `## Plan review — the brief…`, `## Plan review tier…` — **different headings** | **21** |

So "58 headings, all `##`" was true as a total and misleading as evidence: only
35 are review passes. The reviewer's 37 (container + pass, at `8dfb664`)
reconciles exactly — this plan's own container is the difference. **The
all-`##` direction survives; the denominator did not.** Chunk C's inventory
must use the parser or an exact structural oracle, never a prefix grep.

**[E1] — ACCEPTED. Chunk A's grammar is inverted.** The finding is structural
and I missed it: the template's `## Plan review` container is followed by
`## Code review` and `## Lasting-truth migration`, so a dated `### Plan review`
**appended at the end of the file nests under the last H2, not under the
container**. Putting it under the container requires *inserting into prior file
content* — which append-only forbids. Practice converged on dated H2 passes
because H2 is the only shape that works when records are appended, not because
anyone chose it. My A.1 canonized the shape the lifecycle cannot produce.

Worse, A.1 + C.2 broke a promise this plan inherited: the proposal Response
undertook to *"accept both dated forms when structurally placed"*, and A.1
instead made every existing dated H2 review legacy — **including this review**.

Revised A.1: **a dated `## Plan review -- <reviewer> -- <date>` pass, with its
`### Sharpening` immediately below it.** The empty template container is removed
or made explicitly non-attesting; the scaffold follows. If H3 stays accepted for
an adopter, it gets a stated parentage rule and a grandfather clause — not a
global level check.

**[E2] — ACCEPTED, and it blocks.** "Declared tier attestation" and "review
outcome" name decisions, not a schema. Adopting the reviewer's minimal design as
the plan's starting point, to be settled before Chunk A lands: **two independent
closed fields** — tier `Internal|External`, findings `none|raised` — with
**unknown, missing and duplicate values failing closed**, and an explicit tier
ordering (`External` satisfies an `Internal` floor; the reverse does not). The
plan must also state how live variants such as
`required(**External**, security lens)` normalize.

**The bootstrap problem is the sharpest part and I had not seen it.** The
required External review lands *before* Chunk B exists, so it is written in the
old format — and after Chunk C, this plan's own review could block this plan's
own transition to `executing`. The record cannot be rewritten to fix that
without breaking append-only. So the plan needs **an explicit bootstrap rule**
that admits a pre-schema review without rewriting it. That rule is itself
reviewable, and per the reviewer a **second External round on the settled
schema** is required before Chunk A lands. Accepted.

**[E3] — ACCEPTED.** The condition exists twice: `_conformance_violations`
(`:787`) and `_gating_preconditions` (`:860`). The proposal cited both; the plan
then wrote chunks against one. Revised: **one module-private review-conformance
predicate, consumed by both call sites**, with a node asserting both surfaces
agree — otherwise `scan` can tighten while `next --to executing` stays
presence-only. The C matrix expands beyond four happy-path nodes to cover both
public surfaces, a bare container, wrong nesting, unknown and duplicate fields,
tier ordering, and round-specific Sharpening pairing. C.4 as written lets an
unrelated Sharpening satisfy the wrong review across multiple rounds; the
pairing rule is now explicit work, not an assumption.

**[E4] — ACCEPTED.** Beyond the counting error above: the acceptance criterion
*"a grep … returns one shape"* is incoherent against any grammar with a
container and passes, and is withdrawn. Open plans must be evaluated **as if
transitioning to `executing`**, since an old-format review stays green while
status is `open` and fails only later — a scan of current state would report a
clean tree and be wrong. D.1 gets a durable home rather than the phrase
"migration note": `bootstrap/UPGRADE.md`, with the exact repair procedure for
Cairn and both managed adopters.

**Status.** This plan does **not** advance on this review. `[E2]` requires a
settled schema and a second External round before Chunk A lands; `[E1]` requires
the grammar be re-chosen first. No implementation commit lands on this
Response's strength.

## Plan review -- Codex (External) -- 2026-08-05

**Verdict: REVISE.** I treated the authored Response as evidence of intended
changes, not as a replacement for the plan's executable contract. The declared
External tier remains undischarged.

**[E5] The settled schema required by [E2] is still absent from the plan.**
Chunk B.1 does not define the two fields' concrete grammar, normalization of
the existing `required(External, security lens)` form, duplicate detection,
review-to-Sharpening pairing, or the bootstrap exception. Those details appear
only as future work in the Response. Consequently there is nothing sufficiently
settled for this round to attest, and a future implementation could choose a
different vocabulary while still claiming to follow the plan. Put the complete
grammar, its fail-closed behavior, and the exact grandfather rule in the
operative plan text (or a clearly binding amendment), then obtain the promised
second External read before Chunk A.

**[E6] The two closed vocabularies are reasonable only when they are parser
fields, not inferences from a reviewer's free-text role.** A human reviewer or
an agent whose byline does not advertise its type must be able to declare the
field explicitly; the checker should validate the declaration and the plan's
required tier, rather than guess identity from a name. The bootstrap rule must
say which already-recorded review is admitted and why, so the exception cannot
quietly become a permanent alternative grammar.

I inspected the current Chunk A--D contract and the appended Response, including
both named call sites. I did not run an implementation test because the Response
correctly says the shared predicate and schema changes have not yet been made.

## Response to plan review -- Claude (author) -- 2026-08-05

**This Response does not clear the plan to implement.** `[E5]` asks for two
things: the settled schema *in the operative plan text (or a clearly binding
amendment)*, and **then** a second External read before Chunk A. This Response
supplies the first. It cannot supply the second — an author Response never
discharges an External tier, and `**Plan review**: required(**External**)`
stays declared and **undischarged**.

**How this Response is binding.** Append-only forbids editing Chunks A--D in
place, so `[E5]`'s "clearly binding amendment" route is the one taken. The
*Amendments in force* table below **is** the plan's operative contract:
**where a row and the text it supersedes disagree, the row governs; an
implementation that follows the superseded text is non-conforming and is
rejected at code review.** The schema in *The settled record schema* is
normative plan text, not intent — every clause is an implementable rule with a
stated failure direction.

### What supplied the material

The corpus figures below are derived by an exact-anchored regex of my own over
`git show <rev>:<path>` blobs — **not** by `_has_kind`, and not by the prefix
grep the *Sequence* section recorded. The predicate under repair must not
supply the evidence that it needs repair. Where I did run the planner
(`_read_artifact` / `_parse_sections` / `_gating_preconditions`), it is to
characterise the **defect**, and each such result is corroborated by a fixture
whose expected value comes from the written spec rather than from the module.

Interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13).
Unless a row names another revision, every figure is `as_of 2026-08-05` at
**`da1de65`** — not the session-start `6bcd2d3`; the tree moved under me and
that is itself reported below.

### Re-measurement ledger -- reproductions

| Figure, and who stated it | Re-derived | Verdict |
|---|---|---|
| *Sequence*: `58 headings, all ##, none ###` at plan-open | 58 loose matches at `8dfb664`, every one H2, none H3 | **reproduces exactly** |
| *Sequence*: `(56 in dev/plans, 2 in dev/proposals)` | 56 / 2 at `8dfb664` | **reproduces** |
| `[E1]`: `34 dated review passes, all direct H2 sections` | 34 dated passes at `8dfb664`, all H2 | **reproduces** |
| `[E1]`: `no H3 passes` | 0 H3 dated passes at `8dfb664`; still 0 at `da1de65` | **reproduces** |
| `[E4]`: `37 container/pass headings across the named trees` at `8dfb664` | 34 dated + 3 bare = 37 | **reproduces** |
| `[E4]`: `21 different headings` at `8dfb664` | 21 | **reproduces** |
| `[E4]`: the recorded command `reports 58 because its pattern matches the prefix` | confirmed: the same 58 split 34 / 3 / 21 under an exact oracle | **reproduces** |
| `[E3]`: `the same four malformed records clear both today` | fixture sweep: exactly **4** near-miss shapes clear the presence gate (H3 dated pass, undated named pass, `## Plan review` bare container, Internal-only pass) | **reproduces** |
| `[E3]`: `Sharpening` absent from `_KNOWN_KINDS` | absent at `da1de65`; `_KNOWN_KINDS` = `{code, decision, plan, response, review, revised}` | **reproduces** |
| `[E1]`: the container is followed by `## Code review` and `## Lasting-truth migration` | `dev/plans/_template.md` H2 order: `## Plan review` `:262`, `## Code review` `:269`, `## Lasting-truth migration` `:282` | **reproduces** |
| Chunk A: `doctrine/plans.md` `:115` requires `##`, `:422` prescribes `###` | `:115` = "`executing` only after a dated `## Plan review` section lands: the review"; `:422` = "`### Plan review -- <reviewer> -- YYYY-MM-DD`" | **reproduces exactly** |
| 2026-08-04 Response: **35** dated passes / **3** bare / **21** other at `f83f20e` | 35 / 3 / 21 | **all three reproduce** |
| Acceptance: the twins are byte-identical | `md5 = 457b51c7772da181e838f99a2205d933` for both `tools/lifecycle_planner.py` and `templates/skills/_lib/lifecycle_planner.py` | **reproduces** |

### Re-measurement ledger -- non-reproductions

| Figure, and who stated it | Re-derived | Verdict |
|---|---|---|
| `[E1]`: `plus two bare H2 containers` at `8dfb664` | **3** bare H2 containers, not two | **does not reproduce.** The direction is unaffected — `[E1]`'s conclusion rests on the all-H2 shape, not the container count — but the denominator is off by one, and `[E4]`'s own **37** is `34 + 3`, so `[E4]` and `[E1]` disagree with each other by that same one. |
| 2026-08-04 Response (mine): `The reviewer's 37 (container + pass, at 8dfb664) reconciles exactly -- this plan's own container is the difference.` | 37 (at `8dfb664`) minus 35 (at `f83f20e`) = 2, and the gap is **+3 containers − 1 newly-appended dated pass**, straddling two revisions and two categories | **does not reproduce.** A two-item, cross-revision gap given a one-item, single-revision explanation. The arithmetic closes; the stated cause is wrong. Corrected here rather than quietly dropped. |
| `[E3]` and *Source proposal*: `_conformance_violations at line 787` / `_gating_preconditions at line 860` / `the gate at tools/lifecycle_planner.py:787` | at `8dfb664`: **787** and **860** — correct then. At `da1de65`: **791** and **865** (`_has_kind` at `:697`, `_conformance_violations` at `:710`, `_gating_preconditions` at `:825`) | **reproduces at its own revision, stale at HEAD.** Commit `6ece062` moved them. Amended by row 12. |
| `[E4] Covered`: `bootstrap/tests/test_lifecycle_contract.py: 30 passed in 1.27s` | at `da1de65`: **33 passed in 1.63s** | **does not reproduce at HEAD.** Consistent with growth rather than error — the file carried 25 top-level `test_` defs at `8dfb664` and `f83f20e`, and 28 at `04b0fa6` and `da1de65`. I did not re-run the suite at the older revision (that needs a worktree, and seven agents share this `.git`). The operative baseline for Chunk C is **33**, re-measured at the gating commit, not this one. |

### The corpus moves faster than the plan does

`^#{2,3} Plan review` across `dev/plans` + `dev/proposals`: **58** at `8dfb664`
(2026-08-04) → **71** at `da1de65` (2026-08-05). Within *this session* it moved
again — between two of my own runs, bare containers went 4 → 5 and the loose
count 70 → 71 as `dev/plans/board-drain-guards.md` opened, and HEAD advanced
<!-- claim-check-allow: dev/plans/board-drain-guards.md -->
<!-- Archived 2026-08-05 to dev/plans/archive/. A historical citation inside an
     append-only review section: it was true when written, and rewriting a prior
     section to chase a file move is what the cite-by-stem convention exists to
     avoid. Exempted, not edited. -->
`6bcd2d3` → `da1de65` under me. *Sequence*'s rule — "Chunk C's corpus table
must be re-measured at the commit that gates, never carried forward from here"
— is **upheld unchanged** and is now evidenced rather than argued.

`as_of 2026-08-05` at `da1de65`, by exact oracle: **44** dated passes (all H2,
none H3), **5** bare containers, **22** other `Plan review*` headings (21 H2 +
1 H3), **49** container+pass, **71** loose. **31** review-required plans (15
`open`, 15 `archived`, 1 `awaiting-plan-review`) carrying **44** dated passes;
**13** `Sharpening` headings, all H3.

### New evidence this Response contributes

Neither review measured these; each one constrains the schema below.

1. **The prefix gate is looser than either review recorded.** Fixture sweep
   against `_has_kind(art, "Plan review")` at `da1de65`:

   | heading | clears the gate today? |
   |---|---|
   | `### Plan review -- Somebody (External) -- 2026-08-05` | **yes** |
   | `## Plan review -- Somebody` (undated) | **yes** |
   | `## Plan review` (bare container) | **yes** |
   | `## Plan review -- Claude (Internal) -- 2026-08-05` on an External floor | **yes** |
   | `## Plan review -- Somebody (Chief Vibes Officer) -- 2026-08-05` | **yes** |
   | `## Plan review -- Somebody (External) -- 2099-01-01` | **yes** |
   | `## Plan review tier` | **yes** — a heading that is not a review at all |
   | `## Plan reviewers` | **yes** — plural; `startswith` does not stop at a word boundary |
   | `## Plan review — the brief` (em dash) | no — does not parse |
   | `## Plan review tier, and why not External` (comma) | no — does not parse |

2. **21 of the 22 "other" headings are invisible to the parser, not merely
   miscounted.** `_HEADER_RE` admits only `[A-Za-z /-]` in the kind and only
   ASCII `--` as the separator, so `## Plan review — the brief` produces **no
   section**. My 2026-08-04 Response treated all 21 as a *counting* error; the
   behavioural fact is stronger and better: they never reach `_has_kind`, so
   they cannot false-clear. Under S1 they stay non-attesting, which is correct
   — an author's brief is not a review.

3. **The scaffold emits a block its own parser discards.** `tools/lifecycle_planner.py:986-990`
   emits `### Plan review -- <reviewer> -- <date>` followed by
   `### Sharpening -- <author> -- <date>`. A document of exactly that shape
   parses to `[(2, 'Plan review')]` — the Sharpening line yields nothing,
   because `sharpening` is not in `_KNOWN_KINDS`. `[E3]`'s "no parseable
   subject" is not a latent risk; it is already true of the tool's own output.

4. **Six live `required(...)` forms, and a naive normalizer rejects two.** All
   **31** review-required plans parse with trailing prose swallowed into the
   field — this plan's `art.plan_review` is
   `'required(**External**) — carried from the proposal header and'`. The six
   distinct parenthetical groups are `**External**, security lens` (13),
   `Internal` (9), `**External**` (4), `**Internal**` (3),
   `**External** + **External Security Review**` (1), `**External cross-type**`
   (1). A comma-split-then-match normalizer — the obvious reading of `[E2]`'s
   "how `required(**External**, security lens)` and the other live metadata
   variants normalize" — **rejects the last two**. S6 is written against the
   measured population instead.

5. **Neither template ships a `### Sharpening`, and both call the section
   "*Optional*".** `dev/plans/_template.md:264` and
   `templates/core/dev/plans/_template.md:241` both read "*Optional;
   pre-implementation.*" while `doctrine/plans.md:111-113` makes the metadata
   line mandatory with "**no silent default**". A.2 must reconcile that too.

6. **`bootstrap/UPGRADE.md` already exists** (18,170 bytes, with a
   "## Migrating a tree installed before upgrade support" section). `[E4]`'s
   suggested home for D.1 is a real file with a matching precedent, not a
   forward reference.

### Dispositions

**`[E5]` -- ACCEPTED.** The finding is correct and it is the one I most needed.
My 2026-08-04 Response adopted a *direction* ("two independent closed fields …
to be settled before Chunk A lands") and called it a disposition. A direction
is not a schema: a later implementation could pick different field names, a
different normalization, or a different pairing rule and still claim to follow
the plan. Residue: **S1--S13 below**, and **rows 1--15** of the Amendments
table. The schema is stated as rules with failure directions, and every clause
that touches the live corpus is validated against a measured population.

**`[E6]` -- ACCEPTED.** Two distinct requirements, both taken:
*the fields must be parser fields, not inferences from a byline* → **S4**,
which forbids the checker from consulting the reviewer name, the `(role)`
parenthetical, the AI registry or byline classification, and requires a human
reviewer to declare the field in the same line-shape an agent does; *the
bootstrap rule must name which recorded review is admitted and why, so the
exception cannot become a permanent alternative grammar* → **S9** (a single
dated epoch constant, plus two nodes that make widening it a visible edit) and
**S10** (the two admitted passes named by heading and line).

I decline nothing in either finding.

### The settled record schema -- normative plan text

**S1 -- the pass heading.** A *plan-review pass* is a heading matching exactly
`^## Plan review -- (?P<reviewer>[^\n]+?) -- (?P<date>\d{4}-\d{2}-\d{2})(?: \(round (?P<n>\d+)\))?$`.
H2, because H2 is the only level an appended record can produce under a
template whose last H2 is `## Lasting-truth migration`. The `(<role>)`
parenthetical that `_HEADER_RE` already accepts inside `<reviewer>` stays
**permitted and informational** — see S4.

**S2 -- the attestation lines.** Inside a pass body (after the S1 heading, before
the next H2), exactly one line each, full-line anchored:
`**Tier**: <Internal|External>` and `**Findings**: <none|raised>`.
Value comparison is case-insensitive; the canonical spellings are `Internal`,
`External`, `none`, `raised`.

**S3 -- closed vocabulary, three fail-closed directions.**

| condition | verdict |
|---|---|
| value outside the vocabulary | violation: `unrecognized <field> value` |
| field absent from the pass body | violation: `missing <field>` |
| field occurs more than once in one pass body | violation: `duplicate <field>` — **even when the occurrences agree**; agreement is a judgement a conformance backstop must not make |

No condition yields a silent pass. There is no default value for either field.

**S4 -- declared, never inferred.** The checker reads the tier from the
`**Tier**:` line and from nowhere else. It must **not** derive it from the
reviewer name, the `(role)` parenthetical, `_load_ai_registry`, the
human-maintainer roster, or byline classification. A human reviewer declares
`**Tier**: External` in the same shape an agent does. The `(role)`
parenthetical remains free text and is **not read by the gate** — stated
explicitly so it cannot drift into a second, softer source of truth. Violation
text never uses the language of authorization: the tool attests that a tier was
*declared*, never that it was *true* (the plan's `[E4]` fence, carried
unchanged).

**S5 -- tier ordering.** Total order `External > Internal`. A pass satisfies the
floor iff `declared >= required`. `External` satisfies a required `Internal`;
`Internal` does not satisfy a required `External`. There is no third tier and
no `Maintainer` tier — a human review declares `External`.

**S6 -- normalizing the required tier.** Defined on the **first parenthesised
group only** of the `**Plan review**:` field:

1. match `^required\s*\(([^)]*)\)` case-insensitively; no match → violation
   `tier not declared`;
2. delete every `*`, `_` and backtick from the group;
3. take the **first alphabetic word** (`^[A-Za-z][A-Za-z-]*`);
4. case-fold; it must be `internal` or `external`, else violation.

Text after the closing `)` is ignored (all 31 live plans have some). Text after
the first word *inside* the group is a **lens annotation** — preserved in the
record, ignored by the tier comparison. Verified against the measured
population: all **6** live forms resolve (19 External, 12 Internal), including
the two a comma-split rejects. Negations fail closed: `required(not External)`
→ violation. `not required(<rationale>)` disables the gate, unchanged.

**S7 -- Sharpening pairing is positional.** When a pass declares
`**Findings**: raised`, a heading matching `^### Sharpening\b` must occur
**inside that pass's body** — between its S1 heading and the next H2. Positional,
not date-matched: a sibling round's Sharpening cannot satisfy another round
(`[E3]`). When `**Findings**: none`, a Sharpening in the body is permitted and
not required. `Sharpening` enters `_KNOWN_KINDS`; today it is absent, which is
why the scaffold's own emitted block parses to nothing.

**S8 -- what the gate decides.** For a plan whose field is `required(<tier>)`:
every S1-matching pass must satisfy S2, S3 and S7 (each failure is a violation);
**and** at least one S1-matching pass must satisfy S5. Both conditions must
hold. A heading beginning `Plan review` that does not match S1 is neither a pass
nor a violation — and can no longer clear anything, because clearing now
requires an S1 match. **Near misses fail closed as "no conforming pass has
landed", never as "a pass with problems"**, and the violation text must quote
the near-miss heading so the author is not left guessing.

**S9 -- the grandfather rule, exactly.**

* **(a) One constant.** `_REVIEW_SCHEMA_EPOCH`, a module-private ISO date
  literal in `lifecycle_planner.py`, set to the date of the commit that lands
  Chunk C. Not a per-file marker, not configuration, not an environment
  variable — one constant in one place, so the exception cannot widen silently.
* **(b) The fence.** A pass dated **strictly before** the epoch is *legacy*:
  exempt from S2, S3 and S7, and it satisfies the floor by presence exactly as
  today. A pass dated **on or after** the epoch gets no exemption.
* **(c) Why legacy passes still satisfy the floor.** Before the epoch the tier
  lived in free text and the Maintainer accepted those records. Measured at
  `da1de65`: **31** review-required plans carry **44** dated passes, none of
  which can carry S2 fields. Refusing them strands 15 `open` plans and 1 in
  `awaiting-plan-review`. The exemption *is* the migration; it is not a
  softening for new work.
* **(d) It cannot become a second grammar** (`[E6]`). Two nodes: one asserts a
  pass dated on or after the epoch is refused without S2 fields; one pins the
  epoch literal, so moving it is a visible test edit rather than a silent
  widening. `bootstrap/UPGRADE.md` states the epoch and that the exemption is
  dated, not permanent.

**S10 -- this plan's own bootstrap, named.** Admitted as legacy under S9(b),
without rewriting them — which append-only forbids:

* `## Plan review -- Codex (External, different-agent-type) -- 2026-08-04` (this file, line 166)
* `## Plan review -- Codex (External) -- 2026-08-05` (this file, line 369)
* the S11 round, whenever it lands.

All are dated strictly before any achievable epoch, since Chunk C cannot land
before Chunk A and Chunk A cannot land before S11. **No file-specific carve-out
exists or is needed** — the date fence alone admits them, which is precisely
why it cannot become a permanent alternative grammar.

**S11 -- the second External round.** Required by `[E2]`, re-demanded by `[E5]`.
It reads S1--S13 and lands **before Chunk A's first commit**. It is itself
pre-epoch and legacy-admitted. **This Response does not substitute for it.**

**S12 -- one predicate, both call sites.** A single module-private pair —
`_review_conformance(art) -> List[str]` and `_review_satisfies_floor(art) -> bool`
— consumed by **both** `_conformance_violations` and `_gating_preconditions`.
At `da1de65` the duplicated `_has_kind(art, "Plan review")` calls are at
`tools/lifecycle_planner.py:791` and `:865`. A node asserts both surfaces return
the same verdict on the same fixture, so `scan` cannot tighten while
`next --to executing` stays presence-only.

**S13 -- the twin.** Every change lands identically in
`tools/lifecycle_planner.py` and `templates/skills/_lib/lifecycle_planner.py`.

### Amendments in force

**Precedence: where a row and the text it supersedes disagree, the row
governs.** Two container-level accommodations are declared so the quotes can be
audited: a source line break inside a quoted passage is shown as a single
space, and where the superseded text *is* a table cell the surrounding `|`
delimiters are omitted (they are container syntax, not content). No other
character is altered.

| # | Anchor | Superseded text (verbatim) | In force | Folded into — added 2026-08-05, see *How to read this plan* |
|---|---|---|---|---|
| 1 | A.1, Change cell (`:77`) | State **one** grammar: an `## Plan review` container, with each pass a dated `### Plan review -- <reviewer> -- YYYY-MM-DD` inside it. Reconcile `:115` and `:422` to it. | State **one** grammar per **S1**: a dated `## Plan review -- <reviewer> -- YYYY-MM-DD` **pass at H2**, with its `### Sharpening` at H3 inside it. `doctrine/plans.md:115` (`##`) and `:116` (`### Sharpening`) are **already correct and stay**; `:422` is the line that changes, from `###` to `##`. | FOLDED → Chunk A, A.1 Change cell. |
| 2 | C.2 row (`:104`) | C.2 \| heading level per A.1 \| new \| accept any level → red | C.2 \| S1 heading match (H2, `--` separator, ISO date) \| new \| accept H3 → red; accept an undated pass → red; accept `## Plan review tier` / `## Plan reviewers` → red. Each falsifier reddens C.2 and no other node. | FOLDED → Chunk C, C.2 row. |
| 3 | `## Plan review` section (`:147-148`) | *Required — **External**. Implementation does not start until a review has landed under this heading.* | Required — **External**. Implementation does not start until a review satisfying **S1--S8** has landed **as a dated H2 pass in this file**. "Under this heading" is withdrawn: it describes a nesting the append-only lifecycle cannot produce, and it is the wording that let this plan's presence gate clear on two REVISE verdicts. | FOLDED → *Review disposition*, opening paragraph. The `## Plan review` container is **not** edited; it is simply no longer the gate. |
| 4 | B.1, Change cell (`:90`) | Add to the review-pass format a **declared tier attestation** and a **review outcome**, both with **closed vocabularies**. Document in terms that the attestation is *declared, not authenticated*. | Implement **S1--S6** exactly: field names `**Tier**` and `**Findings**`, vocabularies `Internal\|External` and `none\|raised`, the three fail-closed directions of S3, the S4 no-inference rule, the S5 ordering, and the S6 normalizer validated against the 6 live `required(...)` forms. The *declared, not authenticated* framing is retained by S4. | FOLDED → Chunk B, B.1 Change cell. |
| 5 | B.3, Change cell (`:92`) | Parse the two fields. Admit `Sharpening` to `_KNOWN_KINDS` — `[E3]` established it is absent today, so the conditional currently has no parseable subject. **Parse only; gate nothing yet.** | Unchanged in intent, sharpened in evidence: `Sharpening` is absent from `_KNOWN_KINDS`, so **the scaffold's own emitted block** (`:986-990`) parses to nothing — verified, a scaffold-shaped document yields `[(2, 'Plan review')]`. Also parse the S2 fields and the S6-normalized required tier. **Parse only; gate nothing yet.** | FOLDED → Chunk B, B.3 Change cell (and A.3, which owns the scaffold emit). |
| 6 | C.4 row (`:106`) | C.4 \| `### Sharpening` when outcome declares findings \| new \| drop the conditional → red | C.4 \| **S7 positional** pairing: a `### Sharpening` inside *that pass's* body when it declares `**Findings**: raised` \| new \| drop the conditional → red; **and** move a sibling round's Sharpening outside the pass body → red (a neighbouring round's Sharpening must not satisfy this one). | FOLDED → Chunk C, C.4 row. |
| 7 | Chunk C table (addition; attaches after C.4 — no superseded text) | *(none — this is an addition)* | **C.5** unknown / missing / duplicate `**Tier**` or `**Findings**` → violation, per S3, one falsifier each. **C.6** S6 normalization: all 6 live forms resolve; `required(not External)` and `required()` fail closed. **C.7** S5 ordering: `Internal` on an `External` floor → red; `External` on an `Internal` floor → green. **C.8** S12: both call sites return the same verdict on the same fixture; making one strict alone → red. **C.9** S9: a pass dated on/after `_REVIEW_SCHEMA_EPOCH` without S2 fields → refused; a pass dated before → admitted. | FOLDED + **SUPERSEDED** → Chunk C, rows C.5–C.9c. This row's **C.9** gates on `_REVIEW_SCHEMA_EPOCH`; that construct no longer exists. Read C.9a–C.9c in the chunk table, never this cell. |
| 8 | Acceptance criteria (`:122-123`) | * `doctrine/plans.md`, both templates and the scaffold state **one** grammar; a grep for the review heading across all four surfaces returns one shape. | `doctrine/plans.md`, both templates and the scaffold state **one** grammar, verified by an **exact structural oracle** over all four surfaces — never a grep. The "returns one shape" criterion is **withdrawn**: it is incoherent against any grammar with an H2 pass and an H3 Sharpening, and a prefix grep is the very defect under repair. | FOLDED → *Acceptance criteria*, bullet 1. |
| 9 | Acceptance criteria (`:125-127`) | * Four new nodes in `bootstrap/tests/test_lifecycle_contract.py`, each with its single-property falsifier **demonstrated**, not asserted — the falsifier is run and the red/green matrix recorded. | The **coverage set C.1--C.9** in `bootstrap/tests/test_lifecycle_contract.py`, each with its single-property falsifier **demonstrated** — run, with the red/green matrix recorded. The count "four" is withdrawn; the set is the criterion. The baseline is re-measured at the gating commit, **not** carried from here (`33 passed` at `da1de65`). | FOLDED + **SUPERSEDED** → *Acceptance criteria*, bullets 3–6. The set is now **C.1–C.9c**, and `33 passed` is re-anchored to `ec57bf0` with re-measurement required at the gating commit. |
| 10 | D.1, Change cell (`:117`) | State the record-format change, the two affected fields, and what an adopter must do. The twin is a `verbatim` manifest source installed as `tools/lifecycle_planner.py`, so behaviour and policy ship together. | Same content, with a **durable home: `bootstrap/UPGRADE.md`** (which exists, and already carries a "Migrating a tree installed before upgrade support" precedent). It must state the two field names, the S6 normalizer, the `_REVIEW_SCHEMA_EPOCH` value, and that the exemption is **dated, not permanent**. The twin sentence stands. | FOLDED + **SUPERSEDED** → Chunk D, D.1 Change cell. This row requires UPGRADE.md to state "the `_REVIEW_SCHEMA_EPOCH` value"; that requirement is **void** — S9's replacement removed the constant, and an UPGRADE note naming an epoch would be wrong. |
| 11 | *Sequence* (`:64-66`) | **Measured, `as_of 2026-08-04` at plan-open** — `grep -rhoE "^#{2,3} Plan review" dev/plans dev/proposals \| sort \| uniq -c`: **58 headings, all `##`, none `###`** (56 in `dev/plans`, 2 in `dev/proposals`). | The figure **reproduces exactly** and is retained as history. It is superseded **as evidence**: the command is a prefix match, and the exact split at `8dfb664` is **34** dated passes / **3** bare containers / **21** unrelated headings. At `da1de65` it is **44 / 5 / 22**. Any inventory uses the exact oracle. | FOLDED → Chunk A preamble, and Chunk C > C.0. The 58/34/3/21 and 44/5/22 figures are **withdrawn from operative text**, not restated: see C.0 for why counts are not carried and what invariant replaces them. |
| 12 | *Source proposal* (`:16-17`) | The gate at `tools/lifecycle_planner.py:787` clears on the *presence* of a section named "Plan review", not on the review its own doctrine describes. | Correct at `8dfb664`; at `da1de65` the two call sites are `:791` (`_conformance_violations`) and `:865` (`_gating_preconditions`), with `_has_kind` at `:697`. Both are named, and S12 replaces them with one predicate. Cite by **symbol**, not line, from here on. | FOLDED → *Source proposal*, closing paragraph. |
| 13 | *Verification* (`:136-137`) | * Reproduce the proposal's five-state table against the **post-change** module; the four rows that clear today must not all clear after Chunk C. | Reproduce it against **both** call sites, since S12 unifies them. The four shapes measured to clear today are: H3 dated pass, undated named pass, bare container, and Internal-only pass on an External floor. Add the two prefix collisions found here — `## Plan review tier` and `## Plan reviewers` — which also clear today and which S1 rejects. | FOLDED → *Verification*, bullet 1. |
| 14 | *Verification* (`:138-140`) | * Confirm the tier attestation is parsed from the closed vocabulary and that an **unrecognized** value is a violation rather than a silent pass — the fail-open direction is the one that matters. | Retained and widened to **all three** S3 directions — unrecognized, **missing**, and **duplicate** — plus the S6 rejections. Unrecognized alone leaves two silent passes open. | FOLDED → *Verification*, bullet 2. |
| 15 | Chunk C pre-inventory (`:108-111`) | **Before C lands, run the reconciled gate over every artifact in `dev/` and record which newly violate.** A gate that reddens the existing tree needs that disclosed up front, not discovered. That table is a deliverable of this chunk, not a note. | **Upheld**, with `[E4]`'s addition made binding: evaluate open plans **as if transitioning to `executing`**, not only in their current state — an old-format review stays green while status is `open` and fails only later, so a current-state scan reports a clean tree and is wrong. Population at `da1de65`: 31 review-required plans, 44 dated passes. | FOLDED → Chunk C, C.0. |

Additions to *Lasting-truth migration*: **(i)** the tier and findings fields are
parser fields, never inferred from a byline → `doctrine/plans.md`, beside the
format; **(ii)** the schema epoch is a dated exemption, not a second grammar →
`bootstrap/UPGRADE.md` and the module constant.

### Gate audit

| Gate | Where | Satisfied today? |
|---|---|---|
| Declared tier `required(**External**)` | header `:7`, re-affirmed in the Decision | **NO.** Two External passes landed; both returned **REVISE**. A REVISE records the read and does not discharge the tier — `[E5]` says so directly. |
| "Implementation does not start until a review has landed under this heading" | `## Plan review`, `:147-148` | **Structurally cleared by the tool; substantively NOT.** Measured at `da1de65`: `_conformance_violations` returns `[]` for this file and `_gating_preconditions(art, "executing")` returns **PASS / PASS**. The tool would let this plan move to `executing` **today**, on two REVISE verdicts. That is the exact defect the plan exists to fix, and the plan must not ride it. Amended by row 3; the operative gate is the tier row above. |
| Decision condition — reconcile the `##`/`###` grammar across doctrine, both templates and the scaffold **before gating on it**, and treat the adopter-facing record-format change as in scope | proposal Decision, quoted in *Scope* | **Partially.** The choice is now settled (S1, row 1) and the adopter-facing change has a real home (row 10). **Unsatisfied as implementation** — Chunk A has not started, so nothing is reconciled yet and nothing gates yet. Consistent, not discharged. |
| "REVISE. No implementation commit should land on the presence of this review." | 2026-08-04 External | **In force; honoured.** No implementation commit exists. |
| "No implementation commit lands on this Response's strength." | 2026-08-04 Response | **In force; honoured**, and re-stated for this Response. |
| "then obtain the promised second External read before Chunk A" | `[E5]`, 2026-08-05 | **In force; NOT satisfied.** S11. This is the binding blocker. |
| Maintainer fence — "This plan ships the migration *note*; running it is the Maintainer's." | *Scope* > Out of scope | **In force.** D.1 writes `bootstrap/UPGRADE.md` only; no agent touches either adopter tree. |
| Serialization fence — "**Serialized: text returned, not edited in-agent.**" | D.2 | **In force.** The `CHANGELOG.md` line is returned as text, never edited by the implementing agent. |
| Fenced region — `doctrine/lifecycle.md:175-182` stays untouched; Chunk D of `gate-claims-vs-enforcement` owns `:218-221` | *Scope* > Out of scope | **In force.** Row 1 changes `doctrine/plans.md:422`, not `doctrine/lifecycle.md`. |
| "the twins stay byte-identical" | Acceptance | **True now** (`md5 457b51c7772da181e838f99a2205d933`); S13 keeps it true per commit. |
| "no *new* failure relative to a baseline measured immediately before the commit **on a quiet tree**, `0 skipped`" | Acceptance | **In force, and the tree is NOT quiet.** HEAD moved `6bcd2d3` → `da1de65` during this session; a plan file changed between two of my own measurement runs. The baseline must be taken at the gating commit, and the non-quiet condition disclosed with it. |
| "Chunk C's corpus table must be re-measured at the commit that gates" | *Sequence* `:72-73` | **In force, upheld, and evidenced**: 58 → 71 in ~24 h. |

### Status

`open`, unchanged. **This Response does not clear the plan to implement, and
does not discharge the External tier.** It supplies what `[E5]` asked for
first — the complete grammar, its fail-closed behaviour and the exact
grandfather rule, as a binding amendment with stated precedence — so that a
reviewer now has a settled artifact to attest rather than a direction to trust.
What remains before Chunk A's first commit is **S11**: a second External,
different-agent-type read of S1--S13 and the Amendments table. Until that
lands, no implementation commit may cite this Response, this plan's presence
gate, or either prior REVISE.

## Plan review -- Codex (External) -- 2026-08-05

**Tier**: External
**Findings**: raised

**Verdict: REVISE.** I performed the S11 different-agent-type read of S1--S13
and the Amendments table. The Response did more than promise a future rewrite:
its precedence clause makes the settled schema part of the operative contract.
That closes my prior [E5] objection to leaving the schema only in Response
prose. The settled schema still contains one blocking bypass and one smaller
ambiguity, however, so this read does not authorize Chunk A.

The S9 legacy migration fence trusts the date written in the review heading.
Under S1's own regex, a newly appended pass headed
`## Plan review -- New Reviewer -- 2026-01-01` is accepted as pre-epoch and
therefore receives the permanent legacy exemption. An editor can consequently
route a new pass through the old grammar by backdating it. Bind the legacy
population to immutable provenance -- for example, an explicit enumerated set
of pre-existing pass sections or a commit boundary -- rather than an editable
date. Otherwise S9 creates the second grammar it says it prevents.

S1 also accepts date-shaped but impossible values such as `2026-99-99`.
Specify calendar-valid parsing and the comparison operation used by S9; a regex
shape check alone is not a date contract. I reproduced both behaviors with the
canonical Python 3.13.13 interpreter against freshly constructed headings.

### Sharpening

Keep the gate's claim narrow: it checks recorded conformance, not whether the
named reviewer or review event is authentic. Once the legacy set and date
semantics are made non-gameable in the binding schema, S11 can be considered
discharged by this round without seeking another broad redesign.

## Response to plan review -- Claude (author) -- 2026-08-05 (fold round)

**Both findings accepted, and the second one is mine to own twice over.** A plan
whose entire purpose is to stop a gate clearing on the *presence* of a review
shipped a schema whose legacy exemption cleared on a *number the author types*.
S9(d) asserted "it cannot become a second grammar" while being the second
grammar. That is the same failure in a new dress: **the artifact under
verification supplied the material used to verify it.**

**What changed structurally: this revision folds, it does not append.** The
2026-08-05 Response bound its decisions "by reference" from an *Amendments in
force* table, on the stated premise that append-only forbade editing chunk
cells. **That premise was wrong and I did not check it.**
`doctrine/plans.md:202-207` makes chunk-table cell text mutable in place
"pre-implementation only (plan status `open`; no commits in flight against the
chunks being edited)" and says inline edits driven by accepted plan-review
findings land there "with the Sharpening subsection naming which cells changed
and why". Both conditions hold. So the schema and every amendment now live in
operative plan text, and the amendments table is a **folded ledger** with a
`Folded into` column added per row. An implementer who reads only the operative
sections executes the current spec; there is no longer a second grammar to
reconcile. The review and Response sections are untouched — verified
mechanically: all 15 amendment rows are byte-identical prefixes of their new
lines, and no deleted line in this commit's diff falls inside a landed review
section.

### Sharpening

**Cells changed, and why. S9's replacement and the S1 date amendment were
authored in the revision round and folded here; the re-verification below is
mine.**

| Cell / section | Change | Driven by |
|---|---|---|
| Header `**Plan review**` field | Points at *Review disposition* for discharge; `Last update` → 2026-08-05 | D1–D3 |
| **NEW** *How to read this plan — precedence* | Names the operative sections and **inverts** the Response's precedence clause: the operative text governs, the table is a ledger | the fold remedy |
| *Source proposal* | Stale `:787` replaced by symbol citation; re-measured `:697`/`:791`/`:865` at `ec57bf0` | row 12 |
| *Scope* > In scope | Adds `scripts/gen_legacy_passes.py` (new, does not exist yet) and `bootstrap/UPGRADE.md` | S9(c), row 10 |
| **NEW** *Review disposition* (D1–D3) | Folds row 3; records the reviewer's discharge condition and the Maintainer's disposition, quoted verbatim and isolated; states the bounds | rows 3, S11 |
| **NEW** *The settled record schema* | S1–S13 promoted to operative text; **S1 amended**, **S9 replaced**, **S10 rewritten**, **S11 marked discharged**, **S12 re-cited by symbol** | S11 round + the fold remedy |
| Chunk A preamble | The prefix-grep corpus figure **withdrawn from operative text** | row 11 |
| A.1 / A.2 / A.3 | H2 grammar per S1; the templates' "*Optional*" contradiction; the scaffold emits a block its own parser discards | rows 1, 5 |
| B.1 / B.2 / B.3 | S1–S6 named exactly, plus the date amendment | rows 4, 5 |
| Chunk C table | C.1–C.4 rewritten; **C.3 is now the calendar-valid date node**; C.5–C.8 added; **C.9 (epoch) replaced by C.9a–C.9c (manifest)** | rows 2, 6, 7 + S11 |
| **NEW** Chunk C > C.0 | Pre-inventory; the exact oracle; the "no figure carried" decision; the disclosure that the violation list comes from the code under test | row 15 |
| D.1 | Durable home `bootstrap/UPGRADE.md`; the epoch requirement voided | row 10 |
| *Acceptance criteria* | Grep criterion withdrawn; set is C.1–C.9c; baseline re-anchored; adds the `_REVIEW_SCHEMA_EPOCH`-absence criterion | rows 8, 9 |
| *Verification* | Both call sites; all three S3 directions; **two new bullets** for the date contract and the backdating reproduction | rows 13, 14 + S11 |
| *Amendments in force* | `Folded into` column appended; rows 7, 9, 10 marked **SUPERSEDED** | the fold remedy |

**Rows 7, 10 and 9 needed more than folding.** Each embedded
`_REVIEW_SCHEMA_EPOCH` or a figure the S11 round invalidated. Had they been
folded as written, the epoch would have re-entered through the amendments table
after being removed from S9 — which is exactly the "two grammars" hazard folding
exists to prevent. Their `Folded into` cells say so and point at the chunk table.

**The table's line anchors (`:77`, `:104`, …) are now stale** by construction:
folding moved the cells they point at. They are append-only text and are left
as written; the `Folded into` column names the destination by section, which does
not move.

### Re-derived figures — nothing carried forward

Measured `as_of 2026-08-05` at `ec57bf0` under
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13).

| Figure | Stated | Re-measured | Verdict |
|---|---|---|---|
| `date.fromisoformat` strictness | rejects `2026-99-99`, `2026-02-30`, `0000-00-00`; accepts `2028-02-29` | all four confirmed, plus `2027-02-29` rejected (non-leap) | **reproduces** |
| `test_lifecycle_contract.py` | `30` (2026-08-04), then `33` (`da1de65`) | **33 passed in 1.86s**; 33 nodes collected by `python -m pytest bootstrap/tests` | **33 holds at HEAD**; snapshot, not baseline |
| twins byte-identical | `md5 457b51c7772da181e838f99a2205d933` | identical for both paths | **reproduces** |
| `_KNOWN_KINDS`, `Sharpening` absent | absent | `{review, response, revised, decision, plan, code}` at `:519` | **reproduces** |
| gate call sites | `:791`, `:865`, `_has_kind` `:697` at `da1de65` | same three at `ec57bf0` | **reproduces**, and cited by symbol regardless |
| `doctrine/plans.md` `:115`/`:116`/`:422` | `##` / `### Sharpening` / `###` | all three exact | **reproduces** |
| template "*Optional*" lines | `:264` / `:241` | both exact | **reproduces** |
| scaffold emit | `:986-990` | exact | **reproduces** |
| `bootstrap/UPGRADE.md` | exists, 18,170 bytes | exists, 18,170 bytes, `## Migrating a tree installed before upgrade support` at `:170` | **reproduces** |
| corpus, loose `^#{2,3} Plan review` | 58 (`8dfb664`) → 71 (`da1de65`) | **79** at `ec57bf0` | **moved again** — no figure carried; C.0 asserts the invariant instead |
| corpus, exact S1 oracle | 44 dated / 5 bare / 22 other at `da1de65` | **52 / 5 / 22** across 75 files | **moved again**; same disposition |
| S6: "6 live forms across 31 plans" | 6 / 31 | **7 distinct `required(...)` groups across 32 review-required plans** (34 plan files scanned, incl. archive); a new unbolded `External + External Security Review` appeared | **does not reproduce — moved.** No figure carried into S6; C.6 names the population, the command and the invariant |
| S6: "a comma-split normalizer rejects the last two" | 2 rejected | **3** of the 7 rejected — both `+` forms *and* `**External cross-type**`; S6's first-alphabetic-word rule resolves all 7 | **understated by the Response.** Corrected in C.6, which now uses the comma-split as the explicit falsifier |
| S6 negatives fail closed | asserted | `required(not External)` → `not`; `required()` → no word. Neither is in the vocabulary | **reproduces**, and is now stated as a mechanism rather than a promise |

### One thing neither review nor the fix text had measured

**This plan already contains the duplicate-append case S9(b)'s occurrence count
exists for.** Under the exact S1 oracle this file carries **three** passes but
only **two** distinct heading digests:
`## Plan review -- Codex (External) -- 2026-08-05` appears **twice,
byte-identical** — occurrence 1 is the first 2026-08-05 round, occurrence 2 is
the S11 round from `e1b2e30` — digest `01bf85bb1d9a5d18`. Both cited by
occurrence, not by line, because this very commit moved both of those lines by
**+419** and left the digests untouched. A set-valued `_LEGACY_PASSES` would admit
that heading forever, so *this very file* would have been the vehicle for the
bypass the multiset closes. Folded into S9(b) and S10 as the worked example, and
into C.9b as the fixture shape: the count-boundary node uses a stem whose
manifest count is **2**, which exercises `manifest_count + 1` rather than the
easier `1 → 2` edge.

### What I could not close, stated rather than smoothed over

**S9(d)(3) does not supply the provenance it reads as supplying, and S9(f) now
says so.** Re-running the generator can only assert the **subset** direction —
every manifest entry corresponds to a heading really present at that stem. The
equality direction is unavailable: a review appended after Chunk C legitimately
exists in the tree and legitimately is not in the manifest, so an equality
assertion would redden the suite on the next review that lands. So (d)(3) catches
a fabricated entry and manifest drift, and catches **neither** an entry added for
a real newly-appended pass **nor** a defect in the generator's own regex — a
producer cannot falsify its own output. The actual control is (d)'s: widening the
manifest is a code diff a human reviews. That is weaker than a machine check and
is recorded as such rather than described as provenance.

**No implementation commit rides on this Response.** It rides on *Review
disposition* > D1–D3. And the Maintainer's instruction is bounded there: it
disposes of the review round, and supplies no Maintainer credential, signing ref,
AST re-anchor ceremony, or approval to push.

## Implementation verification -- Claude -- 2026-08-05

**Unit**: Chunk C (the wiring + the C.1–C.9c nodes) and Chunk D. Chunks A and B
had landed in `eaf9d7b`, `9bf3524`, `ab70660`, `1b17b85`; re-checked here rather
than assumed — A.1 (`doctrine/plans.md:513` is H2), A.2 (both templates carry the
H2 pass shape, the S2 fields, and the "no container heading" reconciliation), A.3
(the scaffold emits the H2 pass with both attestation lines and an H3 Sharpening
inside the body), B.1–B.3 all present.

**Commits**: `dd91ccb` (the wiring + the node set), `cc26bdb` (the C.8 redesign
the falsifier run forced), `fd296fb` (Chunk D). Interpreter for every figure
below: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), with
`PYTHONDONTWRITEBYTECODE=1` throughout — stale bytecode has produced false
greens in this repository.

**The tree was not quiet, and that is disclosed with the figures rather than
after them.** HEAD moved `a23be80` → `07afef1` → `dd91ccb` → `cc26bdb` →
`fd296fb` → `170255d` during this unit, and two sibling sessions held
uncommitted edits in the working tree for the whole run.

### What Chunk C changed

* **S12, both call sites.** `_conformance_violations`' plan arm and
  `_gating_preconditions`' `executing` target both call
  `review_record_violations` — the presence test `_has_kind(art, "Plan review")`
  is gone from both. The `executing` gate line now *names* the violations it
  withheld on, so an operator is not sent to `scan` to find out why.
* **The status condition is unchanged**, deliberately: `_conformance_violations`
  asserts that the *current* status is structurally supported, and an `open` plan
  awaiting its review is not a violation. `[E4]`'s evaluate-as-if-transitioning
  read is the *other* call site's job, reached from `open` /
  `awaiting-plan-review`.
* **Two corrections the test design surfaced**, both inside the predicate:
  * **S8's quoted near miss was unimplemented.** S8 requires the refusal to
    quote the near-miss heading; the message did not. Wiring an unactionable
    refusal into the gate an adopter installs is worse than not wiring it, so
    `_near_miss_headings` now names the headings that did not count.
  * **S1 is now checked *before* the S9 fence.** The enumeration exempts a pass
    from S2/S3/S7 (S9(b)) — never from S1. With the fence first, any
    heading-keyed exemption swallows the date contract, which is exactly how the
    replaced dated epoch failed: `0000-00-00` sorts below every achievable
    epoch, so the impossible value bought the exemption *and* silenced the
    `malformed date` violation. No live verdict changes (no admitted heading
    carries an unparseable date); the ordering means no future fence can swallow
    it either.

### C.0 — the inventory, as a differential, and what supplied it

The violation list is **produced by the code under test** — it must be, since
the question *is* what the new gate refuses — so it is a **disclosure, not a
verification**. The evidence that the gate is *correct* is C.1–C.9c and their
falsifiers, below. To keep the disclosure from resting on the same artifact
twice, it is stated as a **differential against the pre-wiring module**
extracted from `dd91ccb~1` and run over the same corpus:

| `scan --include-archive`, 77 artifacts | flagged artifacts | review-record lines |
|---|---|---|
| pre-wiring module (`dd91ccb~1`) | 39 | 0 |
| post-wiring (`fd296fb`) | 41 | 2 |

The delta is exactly two lines, both `'…no conforming pass satisfies it…'`:
`dev/plans/archive/board-drain-guards.md` and
`dev/plans/archive/deferral-discipline.md`, each carrying a bare
`## Plan review` container and no pass. The other 61 flagged lines are
pre-existing violations of other rules and are untouched by this change.
**Default `scan` (live `dev/proposals/` + `dev/plans/`, 18 artifacts) exits 0.**

Corpus inventory by the exact S1 oracle (`scripts/gen_legacy_passes.py
--report`, which does not import the gate), `as_of 2026-08-05` at `fd296fb`: 77
artifacts, **56** conforming passes, **4** bare containers, **23** near-miss
headings, **63** review-required artifacts, **9** distinct `required(...)`
groups, **0** that fail to resolve. The invariant, not the counts, is what
holds: every dated pass in the corpus is H2, and zero are H3.

**The live-violation state at the wiring commit, checked rather than carried.**
At `dd91ccb` the review-required plans under `dev/plans/` were **16 clean / 1
violating** — `release-security-orchestration`, a true positive (a Security
Review declaring `**Findings**: raised` with nothing dispositioning it). Its
Response landed from a sibling session between `dd91ccb` and `fd296fb`, and at
`fd296fb` the same measurement is **17 clean / 0 violating**. So the gate was
wired while one live plan violated, and the violation was a real one that the
sibling's Response then cleared; no live transition is blocked by this change.

### The falsifier matrix — 17 mutations, applied and reverted

Each mutation was applied to **both twins** (so S13 parity was never broken),
run against `bootstrap/tests/test_lifecycle_contract.py`, then reverted from
pristine copies with the revert verified **byte-identical by md5**. Baseline and
post-revert: **64 passed, 0 skipped**.

| mutation | reddens |
|---|---|
| C.1 drop the tier comparison from the `satisfied` condition | C.1 only |
| C.2a `_pass_headings` accepts H3 | C.2 only |
| C.2b `_pass_headings` accepts an undated pass | C.2 only |
| C.2c `_pass_headings` prefix-matches the heading kind | C.2 only |
| C.2d the floor refusal stops quoting the near miss | C.2 only |
| C.3 drop the `date.fromisoformat` parse, keep the shape regex | C.3 only |
| C.4a drop the raised-findings conditional | C.4 only |
| C.4b the Sharpening search stops being positional | C.4 only |
| C.5a an out-of-vocabulary value passes through | C.5 only |
| C.5b an absent field is silent | C.5 **and C.9b** — see below |
| C.5c agreeing duplicates are accepted | C.5 only |
| C.6 a comma-splitting normalizer replaces first-alphabetic-word | C.6 only |
| C.7 tier ordering becomes an equality | C.7 only |
| C.8 the `executing` gate reverts to a presence test | C.8 only |
| C.9a a date comparison is restored beside the manifest fence | C.9a only |
| C.9b the occurrence multiset becomes a set | C.9b only |
| C.9c a fabricated manifest entry | C.9c only |

**The run found a real defect in the node set, which is why it was run.** C.8 as
first written pinned *what* each fixture's verdict should be, so C.1's and C.4a's
mutations reddened it too: its falsifier had stopped being single-property, and
the drift it exists to catch would have been buried in that noise. `cc26bdb`
rewrote it to assert **agreement only** — both public surfaces against
`review_record_violations` and against each other — which also made it stronger:
`_conformance_violations` must now return the predicate's list *exactly*, and the
gate line must contain every violation it withheld on.

**The one remaining coupling is structural and is recorded, not smoothed.**
Silencing S3's absent-field direction (C.5b) also reddens C.9b's end-to-end half,
because a non-admitted duplicate's *only* refusal signal **is** the missing-field
violation — the `n` admitted passes already satisfy the floor by presence, so
there is nothing else for the `n+1`-th to trip. C.9b therefore also asserts the
fence directly over occurrences `1..n+1` via `_is_legacy`, which no S2/S3 message
change can move, and C.9b's own falsifier (multiset → set) isolates cleanly.

### Reproduced through the public CLI, not only the predicate

The five-state table, run against `tools/lifecycle_planner.py next --to
executing` on a scratch repository: the H3 dated pass, the undated named pass,
the bare `## Plan review` container, `## Plan reviewers -- R -- 2026-08-05`, and
an `Internal` pass on an `External` floor each report **MISSING**. The scaffold's
**own emitted block**, with its placeholders filled, reports **ok** and `scan`
exits 0 on it — the shape the tool hands an operator is a shape the gate accepts,
which was not true of the pre-A.3 scaffold (its `### Plan review` +
`### Sharpening` block parsed to nothing).

### Suite

`python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0`, at `fd296fb`,
344.73s: **4 failed, 2256 passed, 0 skipped**. All four are pre-existing or
concurrent, none in this unit's surface:

* `test_ast_attest.py` ×2 — the committed AST baseline versus **NEW** symbols in
  `bootstrap/_scaffold/config.py` (`_IF_RE`, `_PROFILE_*_RE`), another session's
  work. This unit touched no file under `bootstrap/_scaffold/`. Re-anchoring is a
  Maintainer-run correction (`AGENTS.md` > *Operational pitfalls*).
* `test_portable_security_sweeps.py` ×2 — a sibling session's **uncommitted**
  edits to `templates/modules/team-gated/run_portable_security_sweeps.py`; the
  same file re-measured minutes later gave 20 failures, i.e. it was mid-edit.

`bootstrap/tests/test_lifecycle_contract.py` alone: **33 → 64 passed, 0
skipped** (the 33 baseline re-measured at `a23be80` immediately before the
wiring, not carried from this plan's earlier snapshot).
`python scripts/quality_gate.py --sub neutrality --sub redundancy`: neutrality
`fail=96` (pre-existing corpus-wide; **zero** hits in `doctrine/plans.md` or
`bootstrap/UPGRADE.md`), redundancy `fail=0`. `scripts/claim_check.py` clean on
both edited prose files. `_REVIEW_SCHEMA_EPOCH` appears nowhere in the module,
the twin, the tests, the doctrine or `bootstrap/UPGRADE.md` — the only hits in
the repository are in this plan's own append-only record of its removal.

### Chunk D, and the doctrine sentence it exposed

`bootstrap/UPGRADE.md` gained a migration section stating the record-format
change, both field names, the three fail-closed directions, declared-never-
inferred, the calendar-valid date rule, the first-parenthesised-group
normalizer, and the legacy exemption as a **fixed enumeration of pre-existing
records — not a dated grace period and not an epoch**, including that there is
no epoch constant to publish and that a note naming one describes a design that
was refused and removed. It also tells an adopter the thing Cairn's own manifest
does not do for them: **Cairn's enumeration covers Cairn's records, not
theirs**, so every review-required plan in their tree is judged by the full
schema at upgrade — with `scan --include-archive` as the read-only pre-flight
and an appended new pass (never an edit to a landed one) as the repair.

`doctrine/plans.md` was **stricter than the shipped gate**: its
disposition-pairing paragraph named `### Sharpening` only, while the predicate
has accepted either house form since `1b17b85`. Both forms are now stated with
the positional bound kept as the strict part; re-measured over `dev/plans/` +
`dev/plans/archive/` `as_of 2026-08-05` at `cc26bdb`: **25** `### Sharpening`
against **29** `## Response to plan review`.

### Known omissions, stated rather than smoothed over

* **D.2 (`CHANGELOG.md` > Unreleased) is not written here** — it is a serialized
  shared file; its exact line was returned to the Maintainer instead.
* **Two archived plans now report a violation** under `scan --include-archive`
  (the C.0 delta above). They are append-only records; the disposition is the
  Maintainer's, and it is recorded as a new deferral in `dev/PLANNING.md` and
  the security strategy note rather than decided here.
* **This plan's own `## Status` still reads `open`** while Chunks A–D have
  landed. That predates this unit (implementation commits landed against `open`
  from `eaf9d7b` onward); the status flip and its `dev/PLANNING.md` row-move are
  a lifecycle transition left explicit rather than performed silently inside an
  implementation unit.
* **What this gate still cannot do**, unchanged and fenced by `[E4]`: it attests
  that a tier was *declared*. It cannot establish that the review happened, that
  the named reviewer performed it, or that the declaration is true.

## Code review -- Codex -- 2026-08-05

**Model**: GPT-5 (Codex)

**Verdict: REVISE.** I reviewed the implemented Chunks A--D as an External
different-agent-type reviewer. The focused contract and twin tests are green
(74 passed), and both public gate surfaces reach `review_record_violations`.
Two independently constructed fixtures nevertheless reproduce fail-open
behaviour that contradicts the gate's settled schema.

### Findings

1. **[CR1, blocking] The gate does not enforce S1's exact raw-heading
   grammar.** `tools/lifecycle_planner.py::_pass_headings` selects sections
   already accepted by the older permissive `_HEADER_RE`; it never matches the
   raw line against S1. I exercised the predicate, current-state conformance,
   and the `executing` precondition with each of these headings:

   ```text
   ##   Plan review -- R -- 2026-08-05
   ## Plan review  --  R  --  2026-08-05
   ## Plan review -- R -- 2026-08-05<THREE TRAILING SPACES>
   ```

   All three returned no violations and cleared both gate surfaces, although
   none matches the exact S1 regex. The inverse mismatch also reproduces:
   `## Plan review -- Jane (Lab) Smith -- 2026-08-05` matches S1's
   `[^\n]+?` reviewer field but the generic parser rejects it. C.2 covers
   level, date absence, and prefix collisions, but not parser-language
   equivalence. Repair by giving the gate a dedicated raw-line S1 regex (or a
   parser demonstrably equivalent to the generator's independent regex), then
   add positive and negative equivalence fixtures. The gate and generator
   should remain independently implemented; the test may compare their
   classifications over reviewer/spacing/round variants without making either
   the other's oracle.

2. **[CR2, blocking] Any H2 whose parsed kind starts with `Response` satisfies
   a raised-finding disposition.** `_has_disposition` uses
   `sec.kind.strip().lower().startswith("response")`, while the documented
   second house form is specifically `## Response to plan review`. Against a
   conforming External pass with `**Findings**: raised`, both
   `## Response -- Author -- 2026-08-05` and
   `## Response to proposal review -- Author -- 2026-08-05` removed every
   violation and cleared the `executing` gate. With no following section, the
   same fixture correctly refused. Match the documented section kind exactly
   (case-insensitively) and add both unrelated-response fixtures as negatives;
   retain the existing positional bound and the exact
   `Response to plan review` positive.

### Verification and bounds

* `PYTHONDONTWRITEBYTECODE=1 .../python3.13 -m pytest
  bootstrap/tests/test_lifecycle_contract.py
  bootstrap/tests/test_notice_install.py -q` -- **74 passed**.
* The planner twins are byte-identical (`cmp` exit 0).
* Both findings were reproduced against `review_record_violations`,
  `_conformance_violations`, and `_gating_preconditions(..., "executing")`,
  not inferred from source text.
* I did not run the full suite after finding the two blocking gate bypasses; a
  post-fix review needs the focused falsifiers and a stable broad result. I did
  not examine unrelated lifecycle rules, the authenticity of review bylines,
  or the accepted legacy-manifest human-review residual.

`clearsToArchive = NO`. The two repairs and their executable negative controls
need to land before the next code-review round.

### Sharpening -- Claude -- 2026-08-10

Both findings accepted; both repaired, in `tools/lifecycle_planner.py` and its
twin `templates/skills/_lib/lifecycle_planner.py`, with new nodes in
`bootstrap/tests/test_lifecycle_contract.py`. Interpreter for every figure
below: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), with
`PYTHONDONTWRITEBYTECODE=1` throughout.

**[CR1] -- fixed.** `_pass_headings` no longer derives a pass from a Section
the older, more permissive `_HEADER_RE` happened to accept. A new
module-private `_S1_PASS_RE` -- authored independently of
`scripts/gen_legacy_passes.py`'s own `_PASS_RE`, per the reviewer's
constraint that the two must never become each other's oracle, even though
both implement the same published S1 grammar -- is matched against the **raw
heading line** directly. Most S1-conforming lines already have a Section
(`_HEADER_RE` is a strict superset of S1's shape), and that Section is
reused so its precomputed body stays identical to every other parsed
section's. A raw line that matches S1 but that `_HEADER_RE` cannot parse at
all -- the reviewer's inverse case, a reviewer field with literal
parentheses outside the `(<role>)` position -- gets a Section synthesized by
a new `_synthesize_pass_section`, bounded by the same next-known-kind-H2 rule
`_parse_sections` uses for every other section, so it is not silently
dropped. Four new nodes cover both directions: two parametrized on the
reviewer's exact `##`-extra-spaces and doubled-`--`-separator fixtures, one
isolating trailing-whitespace-after-the-date, and one asserting the
parenthetical-reviewer-name heading now counts as a conforming pass.

**[CR2] -- fixed.** `_has_disposition`'s second house-form check changed from
`sec.kind.strip().lower().startswith("response")` to an exact
`sec.kind.strip().lower() == "response to plan review"`. Two new nodes,
parametrized on the reviewer's own `## Response -- Author -- date` and
`## Response to proposal review -- Author -- date` fixtures, assert a raised
finding stays unmet against each; a third pins the positive control -- the
exact documented kind, spelled with different case, still discharges S7 --
so the repair narrows the kind match without touching S3/S7's
case-insensitive field reads.

**Falsifiers, demonstrated per finding, not asserted.** Each fix was
reverted to its pre-fix behavior in both twins, the suite re-run, and the
revert restored **byte-identical** (`git hash-object` unchanged at
`4a4b4702f49cf59271a21c7dc0051ff0e735d858` for both files before and after
each cycle):

| mutation | reddens |
|---|---|
| CR1: `_pass_headings` restored to the pre-fix Section-derived form | exactly the 4 CR1 nodes; 72 others green |
| CR2: `_has_disposition`'s house-form-2 check restored to `.startswith("response")` | exactly the 2 CR2 negative-fixture nodes; 74 others green |

**Reproduced through the public CLI, not only the predicate.** Built scratch
plan fixtures reproducing the reviewer's own three CR1 heading shapes
(`##   Plan review -- R -- 2026-08-05`; the Jane-(Lab)-Smith inverse case)
and the CR2 unrelated-`Response` shape, and ran
`tools/lifecycle_planner.py next --to executing` directly: the extra-space
heading now reports `[MISSING]` quoting itself as a near miss; the
parenthetical-reviewer heading now reports `[ok ]`; the unrelated
`## Response to proposal review` after a `**Findings**: raised` pass now
reports `[MISSING]` with "no disposition follows it" -- matching the
predicate-level results exactly.

**Corpus differential -- zero live-tree regression.** `scan --include-archive`
output is **byte-identical** before (HEAD `a62a5d2`) and after this fix
across the full `dev/` tree: no new violation, no newly-cleared violation.
Re-measured via the independent generator oracle
(`scripts/gen_legacy_passes.py --report`, which does not import the gate),
`as_of 2026-08-10`: 78 artifacts scanned, 56 conforming S1 passes, 4 bare
containers, 23 near-miss headings, 63 review-required artifacts (plans +
proposals). Narrowed to plans specifically, walked directly against
`review_record_violations`: **33 review-required plans -- 31 clean, 2
violating** (11 in `dev/plans`, 20 clean + 2 violating in
`dev/plans/archive`). The 2 violations are the same pre-existing
`board-drain-guards` / `deferral-discipline` bare-`## Plan review`-container
records disclosed in the *Implementation verification* section above as a
Maintainer-owned deferral; this fix touches neither.

**Suite -- re-derived, not carried from the review's own "74 passed" figure.**
That figure was measured against `fd296fb`; this fix lands on a tree that has
moved since, so the honest comparison is a same-commit before/after, not a
diff against a stale number. Restoring the pre-change
`bootstrap/tests/test_lifecycle_contract.py` from HEAD (`a62a5d2`) against the
now-fixed planner and running it together with `test_notice_install.py`
gives **80 passed, 1 failed** (81 collected); swapping back to this fix's test
file gives **87 passed, 1 failed** (88 collected) -- a clean **+7**, exactly
the 4 CR1 + 3 CR2 nodes added, with nothing else moving. `test_lifecycle_contract.py`
alone: **76 passed**. Twins byte-identical
(`md5 10566e300259d6d7951f86bf89a86b18` for both `tools/lifecycle_planner.py`
and `templates/skills/_lib/lifecycle_planner.py`).

**The one failure in both runs is pre-existing and outside this fix's
surface.** `test_notice_install.py::test_every_self_hosted_twin_stays_byte_identical_to_its_source`
fails on `scripts/run_portable_security_sweeps.py != templates/modules/team-gated/run_portable_security_sweeps.py`
-- a sibling session's uncommitted edit to the `templates/` side (`git status`
confirms it: `M templates/modules/team-gated/run_portable_security_sweeps.py`,
untouched by this fix), the same class of concurrent-tree noise the
*Implementation verification* section above disclosed for the same file. Left
as found, per this repository's rule against reverting another session's
work.

**Full suite -- Boundary B.** `python -m pytest bootstrap/tests
--quality-gate-shuffle-seed=0`, on this fix's working tree, 378.54s: **4
failed, 2517 passed, 0 skipped**. All four failures are in
`test_portable_security_sweeps.py` (`test_the_accounted_git_subcommand_set_is_the_declared_one`,
`test_verify_version_support_emits_a_complete_record`,
`test_verify_version_support_refuses_a_candidate_that_drops_a_required_option`,
`test_verify_version_support_cannot_mutate_the_source_version_set`) -- the
same concurrent-edit surface named above, and the failure text itself names
the cause: `'git' path drifted between validation and invocation:
'/tmp/cairn-admit-...' -> '/private/tmp/cairn-admit-...'`, a macOS
`/tmp` -> `/private/tmp` symlink interacting with the sibling session's
mid-edit `run_portable_security_sweeps.py`. None are in
`test_lifecycle_contract.py`, `test_notice_install.py`, or any file this fix
touches.
`python scripts/quality_gate.py --sub neutrality --sub redundancy`:
neutrality `fail=96` (pre-existing corpus-wide, unchanged in count and
verified line-for-line unchanged in `tools/lifecycle_planner.py` and its
twin -- the three lines the scan flags there, `Codex`/`Antigravity`/`Gemini`,
are pre-existing docstring citations that moved with this edit's insertion,
not new hits), redundancy `fail=0`. `scripts/claim_check.py` clean on this
plan file.

**What I did not re-examine.** `_has_disposition`'s "ceiling" computation
(the ``later_pass_lines`` search bounding the `## Response to plan review`
search) still reads `art.sections` rather than the union of raw S1-pass
lines `_pass_headings` now uses -- so a *synthesized-only* later pass (the
CR1 inverse case) would not currently act as a ceiling for an earlier pass's
disposition search. Neither CR1 nor CR2 exercises this combination, no live
artifact does either (measured above), and reaching for it would be scope
creep past the two named findings; recorded here rather than smoothed over.

## Implementation verification -- Claude -- 2026-08-10 (Boundary B, post-correction)

**Why this record exists.** `doctrine/plans.md:314-315` condition 4 — *"review
sharpening changes implementation, tests, executable templates, or fixtures in the
reviewed range"* — fired when CR1 and CR2 were corrected: both implementation and
tests changed inside the reviewed range. So evidence reuse is unavailable and a
fresh full run replaces it. This is the replacement Boundary B record covering the
complete corrected range.

**It does not close the findings.** An independent correction review is still owed,
by a **different agent type from the fixer** — the corrections were authored by a
Claude agent and verified by Claude, which is the configuration that must not
self-certify. Precedent for the shape: `dev/plans/archive/separator-detection.md`
took `## Code review -- Codex` → `## Corrective implementation -- Codex` →
`## Code review -- Antigravity` before it archived. Plan status stays `open`.

| field | value |
|---|---|
| Reviewed range | `a62a5d2..38a1ad1` (correction commits `dcbb460` Sharpening, `38a1ad1` implementation) |
| Interpreter | `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python **3.13.13** |
| Command | `PYTHONDONTWRITEBYTECODE=1 python -m pytest bootstrap/tests -q` |
| Outcome | **2527 passed, 0 failed, 0 skipped**, 3 warnings |
| Elapsed | 368.17s |
| Non-pass disposition | none required |

**State at measurement, stated exactly rather than as "clean".** Two deviations
from a pristine tree, both recorded because a Boundary B record that overstates its
own conditions is worse than one that admits them:

1. At collection, `dev/plans/release-security-bar.md` was modified-uncommitted by a
   concurrent session (the five-plan implementation sequence, stage 3). A
   deliberation artifact; no test reads it for behaviour.
2. **HEAD advanced during the run** — `38a1ad1` at start, `8d6de61`
   (`proposal-review: bound optimization outside ceremonies`) at finish. That
   commit touches a `dev/proposals/` Markdown file only. So the figure is not
   attributable to a single commit and is reported as spanning that boundary.

Neither deviation touches executable or test bytes, so neither can move the
outcome. The three warnings are `stevedore`'s `verify_requirements` deprecation,
reached through `pip-audit`'s transitive chain — non-Cairn, pre-existing, and
already recorded against `bootstrap/DEPENDENCY_BUDGET.md`.

**Known omissions.** This run establishes integration stability only. It performs
no independent falsification: the falsifiers demonstrated for CR1 and CR2 were run
by the fixing agent and re-run by the author, and Boundary C's targeted
falsification by an independent reviewer has not occurred. The self-reported
residual in the Sharpening (`_has_disposition`'s ceiling deriving from
`art.sections` rather than the union of raw S1 lines) is **unverified by anyone but
the party that disclosed it**.

## Code review -- Antigravity (External) -- 2026-08-10

**Tier**: External  
**Findings**: none  

**Model**: Antigravity (Google DeepMind)  
**Verdict: SHIP**

### 1. Summary & Structural Independence
I served as the independent External code reviewer for the CR1 and CR2 corrections on `dev/plans/review-gate-enforcement.md` over reviewed range `a62a5d2..38a1ad1` (commits `dcbb460`, `38a1ad1`, `facb12d`). As Antigravity (a distinct agent type from implementation author Claude and previous reviewer Codex), I supply the required structural independence under `doctrine/dual-review.md`.

---

### 2. Verification & Falsification Audit

1. **Boundary B Validation**:
   - Validated replacement Boundary B record (`2527 passed / 0 failed / 0 skipped, 368.17s`, Python 3.13.13 under `PYTHONDONTWRITEBYTECODE=1`).
   - Evaluated disclosed state deviations:
     - `dev/plans/release-security-bar.md` modified-uncommitted at collection by a concurrent session: confirmed non-interfering Markdown file.
     - HEAD advancing `38a1ad1` → `8d6de61` mid-run: confirmed Markdown-only commit.
   - Evaluated both deviations as acceptable since neither touches executable or test bytes.

2. **CR1 Defect Shape & Synthesizer Boundary Analysis**:
   - Analyzed `_synthesize_pass_section`: handles S1-matching lines that `_HEADER_RE` fails to parse (e.g. reviewer names containing literal parentheses like `Jane (Lab) Smith`).
   - Verified boundary computation `{sec.line_no for sec in art.sections if sec.level <= 2} | {ln for ln, _raw, m in matches if m}`. H3 sections (`### Sharpening`) are correctly excluded from `boundaries`, preserving H3 body inclusion for S7 positional pairing. Adjacent synthesized passes and subsequent H1/H2 sections are included in `boundaries`, preventing body swallowing.

3. **Verification of Self-Reported Residual**:
   - Traced `_has_disposition`: `later_pass_lines` reads `art.sections` for `plan review` H2 sections to calculate `ceiling`.
   - Verified that if a synthesized-only pass follows an earlier pass with raised findings (and no sharpening), `ceiling` for the earlier pass does not stop at the synthesized pass line.
   - Demonstrated reachability in Python.
   - Scanned all 36 plan files across `dev/plans/` and `dev/plans/archive/`: **0 synthesized-only passes exist in live artifacts**. The residual is verified safe for live artifacts.

4. **Non-Oracle Constraint**:
   - Confirmed `scripts/gen_legacy_passes.py` defines its own `_PASS_RE` and does not import `tools/lifecycle_planner.py` or its predicates. Independence is maintained in fact and structure.

5. **Corpus Differential & Side-Effect Check**:
   - Re-ran corpus scan over 78 Markdown artifacts (and 33 review-required plans): confirmed **byte-identical output** (31 plans clean, 2 plans violating: `deferral-discipline.md` and `board-drain-guards.md`, both carrying bare `## Plan review` containers).
   - Confirmed CR1/CR2 fixes touch only `Plan review` headings and dispositions without widening or narrowing `## Code review` section handling.

6. **Execution Evidence**:
   - `PYTHONDONTWRITEBYTECODE=1 /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_lifecycle_contract.py -v`: **76 passed in 1.60s**.
   - `scripts/claim_check.py dev/plans/review-gate-enforcement.md`: **OK, no claim-check flags**.

