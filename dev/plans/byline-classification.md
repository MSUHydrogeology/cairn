<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/lifecycle-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- The new test module is a forward reference registered under `Proposed paths`.
     The marker exempts only its own contiguous block, and the chunk tables cite it
     many sections later, so it needs the file-scoped directive too.  Drop this
     directive once the path lands (Chunk A), per the marker discipline. -->
<!-- claim-check-allow: bootstrap/tests/test_byline_identity.py -->

# Plan: exact byline classification — a fold that drops no letter and no digit

**Source proposal**: `byline-classification` (accepted 2026-08-03; the Decision
commit is `76a48af`). It currently sits under `dev/proposals/` and moves to
`dev/proposals/archive/` when it archives.
**Status**: open
**Plan review**: required(**External**, security lens) — carried verbatim from
the proposal header, and **not** discharged by either round the proposal already
had. The proposal's own Internal reviewer wrote that their pass *"does not
discharge the `required(External, security lens)` tier and must not be counted
toward it."* **No implementation commit lands before the `## Plan review`
section carries a real review.**
**Last update**: 2026-08-03
**Opened**: 2026-08-03

## Source proposal

`byline-classification` is scope 2 of the superseded `identity-not-name`
proposal. It fixes a **demonstrated** privilege-widening defect in the tool that
reports whether a proposal's or plan's recorded state is structurally sound.
One invisible character — a Cyrillic letter that renders identically to an ASCII
one — currently moves a byline from *"AI agent, flagged"* to *"recognized human
Maintainer, silent"*. The proposal replaces a character-**deleting**
normalization with a character-**preserving** one, and replaces
per-word-fragment matching with whole-name exact matching.

The Decision raised the scope from a correctness cleanup to *"a security fix
with a demonstrated exploit"* and named the invariant the fix must serve:

> **dropping a character must never widen authority**

The proposal settles the design. This plan executes it and does not re-litigate
it.

### Glossary — every term glossed on first use

The audience is a scientist who codes, and this scope is Unicode-dense.

* **Byline** — the `-- <name> (<role>) -- <date>` tail on a `## Decision` or
  `## Review` heading. It is the only place the record says *who* authored a
  section.
* **Classifier** — the three-way function that answers *is this byline an AI
  agent, a known human Maintainer, or neither?* `ai` and `unknown` both raise a
  structural violation; only `human` is silent. Humanity must be **proved** from
  a project-owned allowlist, never inferred from a name failing to look robotic.
* **Roster** — that allowlist. It lives in `dev/.cairn/agent-identities.json`
  under the key `human_maintainers`.
* **Fold** — the function that reduces a display name to the key actually
  compared. Today it is `re.sub(r"[^a-z0-9]", "", raw.lower())`, which deletes
  every character that is not an ASCII letter or digit — **including every
  non-ASCII letter**. That deletion is the defect.
* **Homoglyph / confusable** — a character that renders like another. `chr(0x430)`
  is CYRILLIC SMALL LETTER A and is visually indistinguishable from ASCII `a` in
  every editor, terminal, diff and web view.
* **Normal form, `NFD` vs `NFKD`** — two ways of decomposing a character.
  **`NFD`** (*canonical*) separates a letter from its accents and does nothing
  else. **`NFKD`** (*compatibility*) additionally collapses presentational
  variants — mathematical-bold letters, circled letters, full-width forms — onto
  plain ones. The proposal uses `NFKD` on the leg where an error **over-flags**
  (safe) and `NFD` on the leg where an error would **grant** authority (unsafe).
* **Combining mark** — a character that attaches to the preceding one (an accent,
  a tone mark, a dakuten). `unicodedata.combining()` reports it.
* **Case folding** — `str.casefold()`. Stronger than `lower()`: it also expands
  ligatures and sharp-s. That extra strength is load-bearing below.
* **Twin** — Cairn ships `tools/lifecycle_planner.py` to adopters as
  `templates/skills/_lib/lifecycle_planner.py`. The two files must stay
  **byte-identical**; a suite node enforces it.

### Character convention, adopted from the proposal and binding on this plan

**No confusable or invisible character appears as a literal anywhere in this
plan.** Every one is written `chr(0x...)`. Visibly-distinct international
characters (`Łukasz`, `José`, `张伟`) *do* appear as literals — a reader can see
exactly what they are, and they carry no spoofing risk. The same rule binds the
test module: confusables constructed with `chr()`, ordinary international names
written plainly.

## The gap this plan must close before it can execute

**Read this before *Scope*.** It is the single most important structural fact
about this lifecycle, and an implementing agent who misses it will silently
under-deliver.

The proposal's section order is: External Security Review (SHIP) → author
Response → **Internal Security Review (verdict: REVISE, seven findings
[I1]–[I7])** → Decision. **There is no Response to that Internal review, and no
revision followed it.** Verified against the file's section list and its commit
history at `05515df`, 2026-08-03: the Internal review landed at `a597b30` and
the Decision at `76a48af`, with nothing between them.

The Decision reads **"Accepted, as revised."** Because no revision exists in the
artifact, that phrase cannot point backwards at one. This plan therefore reads
it as pointing **forward**: the revisions the Internal review named are this
plan's to execute, and the Decision accepted the proposal *on the condition that
they land*. That reading is stated explicitly rather than assumed, because the
alternative reading — that "as revised" ratifies the proposal exactly as
written — would ship two named-near-vacuous tests and ratify a residual whose
own expiry trigger was already satisfied at the moment of ratification.

**Three items reach the Maintainer, not the implementing agent** (below, under
*Maintainer questions*). Everything else in [I1]–[I7] is sequenced into the
chunks.

### What each Internal finding becomes here

Each is reproduced by execution for this plan — commands and outputs are in
*Verification* — rather than carried forward on the review's word.

| Finding | Substance | Where it lands |
|---|---|---|
| **[I1a]** `casefold()` expands ligatures and long-s onto the *granting* leg | `chr(0x17f)` reads as `f` to a modern eye and folds to `s` | R2 restated (Chunk 0); pinned by a residual test (B4) |
| **[I1b]** combining-mark stripping merges *letter-distinguishing* marks | Vietnamese tone, kana dakuten, Devanagari nukta, Cyrillic YE/YO | R2 restated (Chunk 0); pinned by a residual test (B4) |
| **[I2]** the fold deletes **three** classes, not the two the rule names | C0 controls + DEL, and ASCII *symbols*, are undeclared | Deletion set becomes an explicit allow-set (A1); pinned by B2 |
| **[I3]** the roster-symmetry test is near-vacuous — its oracle is the function under test | passes even against a fold that grants authority to a different person | replaced by an **anti-collision** test (B3); symmetry kept, relabelled (B5) |
| **[I4]** the character-preservation invariant cannot be implemented as worded | case folding replaces letters, so a literal reading fails everywhere | restated as the **non-empty-fold** invariant (B1) |
| **[I5]** an empty-folding config entry matches every byline | `"anything".startswith("")` is `True`; `() == ()` is `True` | folded-value guards on **both** loaders (A3, A4); pinned by A7 |
| **[I6]** ASCII-only tokenization breaks a legitimately-rostered non-ASCII name | CJK `chr(0x3000)`, French `chr(0x202f)` | recorded as an honest cost (B6); the fold change itself is a **Maintainer question** |
| **[I7a]** the frozen-file count moved the same day | `162` at the measured commit, `164` now | re-measured for this plan (*Gate accounting*) |
| **[I7b]** a sibling states this proposal's behaviour wrongly | `planner-line-semantics` describes the *replaced* recipe | recorded here; the correction is that proposal's to make |

### Maintainer questions — three, and none is an implementing agent's to answer

1. **Does "as revised" carry the Internal review's revisions?** This plan
   assumes yes. If the Maintainer intended an unconditioned accept of the text
   as written, say so before Chunk A — the chunk contents change.
2. **Ratifying R2 in its corrected form.** The proposal asked the Decision to
   ratify residual R2 as *"accent- and case-variants … every member reads as the
   rostered name to a human."* Three measured classes falsify that wording, and
   they are reproduced in *Verification* below. Chunk 0 lands R2 on
   `dev/PLANNING.md` **restated** — canonical-decomposition equivalence *plus
   full case folding* — with the three classes named. That is a change to text
   the Decision was asked to ratify, so it is the Maintainer's to confirm or
   correct, not the plan author's to make quietly.
3. **[I6] — should Unicode `Zs` (space separators) be word breaks?** The
   Internal reviewer offered this as *"one optional design question for the
   Maintainer, not a finding."* It is **not implemented here**; the accepted
   design's ASCII-only split ships. Measured both ways for this plan, so the
   question is decidable rather than rhetorical:

   * **Which option is the *change* — corrected at plan review, because this
     plan had the direction backwards.** Today's code tokenizes with a bare
     `name.strip().split()`, which splits on **Unicode** whitespace. Measured
     against the live planner: with the current roster, all six `Zs` separators
     below classify `human` **in the tree as it stands**. So the accepted
     design's ASCII-only split is a *behaviour change* on this axis, and a `Zs`
     split *preserves* today's behaviour. This does not decide the question —
     the accepted design is still the accepted design and the exploit is
     unaffected either way — but the Maintainer should have the baseline right,
     and Chunk C now carries the change in the release notes.
   * **Cost of shipping as accepted**: a CJK byline separated by `chr(0x3000)`
     IDEOGRAPHIC SPACE, and a French byline separated by `chr(0x202f)` NARROW
     NO-BREAK SPACE, both classify `unknown` against a roster typed with an
     ASCII space. Both are legitimate, real-world spellings. The direction is
     safe (it over-flags, it does not grant), but it is a real false positive on
     the axis the proposal headlines as costless.
   * **Cost of the `Zs` change**: it widens `human` by six separators measured
     here — `chr(0xa0)`, `chr(0x2000)`, `chr(0x3000)`, `chr(0x202f)`,
     `chr(0x1680)`, `chr(0x205f)`. The argument offered for it is that a `Zs`
     character is *visible* as a space. **That argument has a counterexample
     this plan found and the review did not**: `chr(0x1680)` OGHAM SPACE MARK is
     category `Zs` but is rendered as a visible stem segment in Ogham-aware
     fonts and as blank elsewhere — so its visibility is font-dependent, which
     is precisely the property the "visible space" argument needs to exclude.
   * **Not affected either way**: the exploit. `chr(0x2028)` and `chr(0x2029)`
     are `Zl`/`Zp`, `chr(0x200b)` and `chr(0xad)` are `Cf`; none is `Zs`, and
     the homoglyph bylines classify `unknown` under both splits. Measured.

   If the Maintainer wants `Zs` word breaks — which is also what the tree does
   today, per the first bullet — it is a one-line edit to the tokenizer
   plus one behaviour-table row, and B6's test inverts. **Absent an answer, the
   accepted design ships and B6 records the cost.**

## Proposed paths

Proposed paths:
- `bootstrap/tests/test_byline_identity.py` — the new pytest module: behaviour table, deletion-set pin, non-empty-fold invariant, anti-collision corpus, residual pins, loader-guard tests. Lands in Chunk A and grows through Chunk B.

## Scope

Executes the accepted proposal's five numbered changes, plus the Internal
review's recommended dispositions per the table above.

**In scope:**

* `tools/lifecycle_planner.py` and its byte-identical twin
  `templates/skills/_lib/lifecycle_planner.py` — the identity helpers,
  `IdentityModel.classify`, both config loaders, the `unknown` violation
  message, and the identity-model comment block.
* `dev/.cairn/agent-identities.json` — the live roster value.
* `dev/.cairn/cairn-lock.yml` — the `hash` field on the twin pair's `verbatim`
  row, which re-records when either side changes.
* `bootstrap/tests/test_lifecycle_contract.py` — exactly one existing node.
* `bootstrap/tests/test_byline_identity.py` — new.
* `CHANGELOG.md` — the behaviour-change entry R5 requires.
* `dev/PLANNING.md` — the residual expiry rows, at plan-open.

**Out of scope, fenced explicitly:**

* **`bootstrap/_scaffold/` — untouched.** No engine file is edited, therefore
  **no AST attestation re-anchor and no Bandit engine gate attaches to this
  plan**. The `ast-attest-verify` gate scopes to `bootstrap/_scaffold/*.py` and
  nothing in scope matches it. There is **no Maintainer-only Phase 0** in this
  plan for that reason, and an implementing agent must not invent one. This is
  stated affirmatively because omitting it drew a blocking finding on the parent
  lifecycle.
* **The consuming policy.** What `_conformance_violations` and
  `_gating_preconditions` *do* with a classification is a separate contract.
  Changing the independence gate soundly needs a **reviewer**-identity roster,
  and the only human list that exists confers *Decision* authority. Reusing it
  would couple two authorities to buy one fix. That is residual R3.
* **Defect (c) in full — the independence widening.** The `NFKD` comparator
  closes three of four measured variants; the Cyrillic-homoglyph variant stays
  open. Partially closed, measured, pinned (B7), **not fixed**.
* **The four parsing functions `planner-line-semantics` claims** —
  `_parse_status`, `_parse_field`, `_parse_sections`, `_has_isolated_blockquote`.
  Same module, disjoint functions, no shared line, either landing order works.
* **Any config schema change.** No new key. The two existing lists keep their
  meaning; only the *granularity* of a `human_maintainers` entry changes, from
  name-fragment to complete display name.
* **R6's documentation sentence.** `dev/.cairn/agent-identities.json` is read by
  shipped code, written by no installer, and documented only in a code comment.
  Its expiry is *"no later than v0.4.0 release preparation"*, and the proposal's
  documentation surface explicitly excludes it. It goes on `dev/PLANNING.md`
  (Chunk 0) and **is not written here** — this plan changes the *content* of an
  installed file, not the set of installed files or their docs.
* **The pre-existing `Devine` over-flag.** The AI registry matches `devin` as a
  prefix, so the real surname *Devine* classifies `ai` today and after this
  change; because the AI leg has precedence, a Maintainer with that name cannot
  fix it via the roster. Pre-existing, not introduced, and a genuine
  postdoc-first hazard — recorded on `dev/PLANNING.md`, not fixed here.
* **The unswept `re.sub` normalization pattern elsewhere.** `tools/lifecycle.py`
  and `scripts/` were never swept for the same bare-`re.sub` shape. Both reviews
  declared it uncovered. It stays uncovered and is a mandate to the plan
  reviewer, not work in this plan.

**Sequencing invariant — every intermediate commit is fail-closed.** Chunk A is
deliberately large because it cannot be split without producing a fail-**open**
intermediate state, and this is the claim a reviewer should check hardest:

* Splitting the fold from **exact matching** leaves the pre-fix fold matching by
  set intersection — the current defect, unchanged.
* Splitting exact matching from the **roster correction** leaves Cairn's own
  record flagging every Decision (the two-fragment roster matches no full-name
  byline under exact equality).
* Splitting the fold from the **loader guards** creates a *new* fail-open state
  that does not exist today: under tuple equality `() == ()` is `True`, so a
  punctuation-only roster entry would match a punctuation-only byline, and an
  empty-folding AI-registry entry would classify *every* byline `ai` because
  `"anything".startswith("")` is `True`. Both are measured below. Today these
  are inert; after a partial landing they are not.
* Splitting either twin from the other fires the byte-parity node — verified by
  perturbation, not asserted (see *Verification*).

### Documentation / doctrine surface

* **Descriptive layer, in-code** — the `_fold_word` docstring stating the
  two-strength rationale, and a revision of the identity-model comment block at
  `tools/lifecycle_planner.py:180` so it states what a roster entry now *is*.
  That comment is the only place the config's grammar is written down, which is
  residual R6.
* **Release-facing** — `CHANGELOG.md > Unreleased > Fixed`, one behaviour-change
  entry, which is R5's expiry trigger.
* **Deliberation layer** — this plan, its plan review, its code review, and the
  residual rows it lands on `dev/PLANNING.md`.
* **Governing layer — none.** No `AGENTS.md` change and no `doctrine/` change.
  This changes no rule a contributor follows; it is a defect fix in code plus
  its tests plus one config value. The doctrine-change rate-limit gate is
  therefore not engaged.
* **Entry layer — none.** No new document.
* **Install contract — unchanged.** The shipped twin's *content* changes; the
  set of installed files does not. Re-measured for this plan under the canonical
  interpreter: `python bootstrap/scaffold.py --manifest` emits 96 lines, of
  which exactly 1 names `lifecycle_planner`, `as_of 2026-08-03`. This plan adds
  and removes no row, and that is an assertion in *Verification*, not a
  prediction.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

### Gate accounting

Every figure re-measured for this plan under the canonical interpreter
(`~/conda_envs/lhm/bin/python`, 3.13.13) with `PYTHONDONTWRITEBYTECODE=1`, at
`05515df`, 2026-08-03. The proposal called its gate figures *"a live invariant
to re-check at plan time"*, and [I7a] showed one moving within a single day, so
none is carried forward.

* **The gate batch is closed and frozen-file edits are no longer held.** The
  frozen set holds **164** entries, `as_of 2026-08-03` — not the `162` the
  proposal and its Response recorded. `bootstrap/tests/test_lifecycle_contract.py`
  **is** frozen; `tools/lifecycle_planner.py`,
  `templates/skills/_lib/lifecycle_planner.py` and
  `dev/.cairn/agent-identities.json` are **not**. Re-verified individually, not
  inferred from the count.
* **A documented gate that nothing fires — stated rather than glossed.**
  `bootstrap/tests/_gate_manifest.py verify` is **not** invoked by the pytest
  suite and by no CI workflow; it runs only inside the Maintainer's supervised
  re-anchor ceremony (`bootstrap/REANCHOR_RUNBOOK.md`). The evidence is the
  tree's own state: running it today reports **two** pre-existing
  `FROZEN-MODIFIED` holds — `bootstrap/tests/test_quality_gate_redundancy.py`
  and `scripts/quality_gate.py`, both from the r6 fix that landed at `7066489`
  — and that commit landed anyway. So editing a frozen file is genuinely
  unblocked today; what it does is add a **third** stale entry that the next
  ceremony's `produce` step absorbs. An implementing agent should expect a
  `FROZEN-MODIFIED` line for `test_lifecycle_contract.py` and must **not** treat
  it as a stop, nor "fix" it by regenerating the manifest — regenerating it is a
  supervised, Maintainer-only trust-root step.
* **Collection only grows.** The gate holds on a *dropped* node or a *new*
  skip/xfail marker; added nodes are recorded. This plan adds nodes, updates one
  in place, and drops none.
* **Suite baseline: 1601 passed, 0 failed, 0 skipped**, `as_of 2026-08-03`,
  re-measured in the real checkout for this plan (156 s wall).
* **Run the suite in the real checkout, never in a `git archive` sandbox.**
  Measured for this plan: a clean `git archive HEAD` sandbox reports **9 failed,
  1591 passed, 1 skipped** — nine tests need a real git tree the archive does
  not carry. A sandbox run therefore has a nine-failure floor that would mask a
  real regression, and the proposal's own `1545 passed / 10 failures` figure was
  taken that way. Sandbox runs are for *perturbation deltas* only, where the
  clean baseline is subtracted.

## Sequence

```
0. plan-open      -- this plan + dev/PLANNING.md residual rows        [commit pending]
   (plan review)  -- required(External, security lens); NO code before it lands
1. Chunk A -- the fold, exact matching, both guards, the roster        [commit pending]
2. Chunk B -- the invariant, the corpus, and the residual pins         [commit pending]
3. Chunk C -- CHANGELOG behaviour-change entry                        [commit pending]
```

Three chunks, not more. Chunk A is indivisible for the fail-closed reason given
in *Scope*; B is test-only and could not have preceded it; C is release-facing
bookkeeping.

### Chunk 0 — plan-open and the residual homes

Lands with this plan, before the plan review, because the proposal states the
expiry rows land *"at plan-open, not at archive, so they outlive this
proposal's readership."* A trigger recorded only in a proposal is inert:
accepted proposals archive, and archived proposals are not read.

| # | File | Change |
|---|------|--------|
| 0a | `dev/PLANNING.md` | **R1** (the exact-name spoof) — dated posture: single maintainer, roster size 1, `as_of 2026-08-03`. Mechanical expiry: the roster gaining a second entry. Non-mechanical: successor scope 1 landing a signing trust root. Backstop 2027-02-03. |
| 0b | `dev/PLANNING.md` | **R2 restated** — *canonical-decomposition equivalence plus full case folding*, naming the three [I1] classes: ligature/long-s expansion, letter-distinguishing combining marks, and case. Its old mechanical expiry was satisfied before ratification, so the row records the counterexamples as **accepted with the class on the record**, and re-marks the trigger as: a member of the class that is *not* in the three named groups. |
| 0c | `dev/PLANNING.md` | **R3** (independence widening, partially closed) — mechanical expiry: the first `## Review` in this repository authored by a human who is not the Maintainer. Non-mechanical: any durable list of people who may review but may not decide. Backstop 2026-11-03. |
| 0d | `dev/PLANNING.md` | **R4 corrected** (the flag is not a detector) — with the measured correction below, which changes its disposition. |
| 0e | `dev/PLANNING.md` | **R5** (behaviour change for a token-style roster) — expiry: the v0.4.0 release notes. |
| 0f | `dev/PLANNING.md` | **R6** (the roster file has no documented home) — expiry: one sentence in `bootstrap/UPGRADE.md` or the adopter-facing skills documentation, no later than v0.4.0 release preparation. Fenced out of this plan. |
| 0g | `dev/PLANNING.md` | The pre-existing `Devine` over-flag, recorded so it is not mistaken for a regression and so someone eventually owns it. |

**R4's correction, measured for this plan.** R4's stated expiry is *"when
`agent-context-scrub` lands its escaping helper, this call site adopts it rather
than keeping a second escaper."* That sibling was accepted the same day
(`c7266d4`). Reading its design: its `_FIELD_ESCAPES` table covers C0 and C1
controls, DEL, `chr(0x2028)`, `chr(0x2029)` and backslash, and it states in
terms that *"ordinary international text — accented author names, CJK commit
subjects, Greek letters — passes through untouched."* A Cyrillic `chr(0x430)` is
ordinary international text. **Adopting that helper for this call site would
produce no diagnostic at all** — it would render the confusable byline
unchanged, which is the exact failure change 5 exists to fix. The two escapers
serve opposite purposes: one renders a payload inert while preserving
international text, the other reveals that international text is present. R4's
row therefore records that the merge is **measured as wrong**, and the trigger
becomes: a shared helper that takes the *reveal* mode as a parameter, or
nothing. This is a correction to a residual's routing, not a design change, and
it is flagged for the Maintainer alongside question 2.

**Acceptance criteria — Chunk 0**

* Every residual R1–R6 has a row on `dev/PLANNING.md` whose trigger names an
  observable event, not a feeling. A reviewer's check: for each row, name the
  thing you would look at to see whether it fired.
* R2's row does **not** carry the proposal's original wording. If it does, a
  residual whose expiry was already satisfied has been ratified, which is debt
  wearing a decision's clothes.
* `python scripts/claim_check.py dev/PLANNING.md` clean.
* This is a `dev/`-only commit and lands under the deliberation carve-in; it
  bundles no code.

### Chunk A — the fold, exact matching, the guards, and the roster

The security core, and the smallest self-contained unit that is fail-closed at
every point. One commit.

| # | File | Change |
|---|------|--------|
| A1 | `tools/lifecycle_planner.py` | `_fold_word(raw, form)` — case-fold, normalize twice at `form`, drop combining marks, then keep a character if it is non-ASCII **or** in `a-z0-9`. Per [I2] the surviving deletion is expressed as an **explicit allow-set**, so the rule and the code are the same statement, and the docstring names all three deleted classes (ASCII punctuation **and symbols**; C0 controls and DEL; combining marks) rather than the two the proposal named. |
| A2 | `tools/lifecycle_planner.py` | `_flag_words(name)` at `NFKD` (over-folding here over-flags) and `_grant_words(name)` at `NFD` (over-folding here would grant). Tokenization splits on **ASCII whitespace only**, so a non-ASCII separator stays inside its word rather than acting as an invisible word break. The two-strength asymmetry is stated in the docstrings, not left to be inferred. **"ASCII-only" is a mechanism requirement, not a description** — the split is an explicit ASCII class (`[ \t\n\r\f\v]+`, or an `re.ASCII` pattern), because both obvious implementations are Unicode-aware and would silently decide Maintainer question 3: today's bare `name.strip().split()` splits on every `Zs` separator measured below, and so does a `\s` class in a `str` pattern (both measured at plan review). B6 catches either, but it lands a chunk later, so the mechanism is pinned here. |
| A3 | `tools/lifecycle_planner.py` | `_load_human_maintainers` returns a frozenset of **word tuples** produced by `_grant_words`, and — per [I5] — filters on the **folded** value, not the raw entry. The existing guard tests whether the *entry* is blank; the correct predicate is whether the *key* is empty. Under tuple equality `() == ()` is `True`, so the old predicate would let one punctuation-only typo match a punctuation-only byline. |
| A4 | `tools/lifecycle_planner.py` | `_load_ai_registry` applies the same folded-value filter, per [I5]. An entry folding to the empty string would otherwise classify **every** byline `ai`, because `"anything".startswith("")` is `True`. Config-supplied entries fold through `_flag_words`, so the extension mechanism is symmetric with the built-ins. |
| A5 | `tools/lifecycle_planner.py` | `IdentityModel.classify` — AI leg first (prefix match on `_flag_words`, precedence preserved), then **tuple equality** of `_grant_words(byline)` against the roster's key set, replacing the per-word set intersection at `tools/lifecycle_planner.py:314`. Exactness, not containment, is what closes the defect in its general form. |
| A6 | `tools/lifecycle_planner.py` | `_identity_token` becomes the first element of `_flag_words` — the independence comparator at `tools/lifecycle_planner.py:590` and the `independent_review` gate at `tools/lifecycle_planner.py:683` inherit `NFKD` and stop deleting characters. Partial close of defect (c); see B7. |
| A7 | `tools/lifecycle_planner.py` | The `unknown` violation message gains two additions, both message-only: that a roster entry must be the **complete display name as it appears in the byline**; and, when the byline holds any character outside ASCII, the `ascii()`-escaped form appended. Measured: `repr()` renders the Cyrillic byline indistinguishably from the honest one, because `repr()` of a `str` leaves non-ASCII characters as-is; `ascii()` renders the same byline with the confusable spelled out as the six ASCII characters `\u0430`, so `Cl` + that escape + `ude` is visibly not `Claude`. A flag the reader cannot interpret is half a flag. |
| A8 | `tools/lifecycle_planner.py` | The identity-model comment block at `tools/lifecycle_planner.py:180` revised to state what a roster entry now is. This is the only place the config's grammar is written down (R6). |
| A9 | `templates/skills/_lib/lifecycle_planner.py` | The identical edit. Byte parity re-measured before and after; the edit lands in **both** files or in neither. |
| A10 | `dev/.cairn/agent-identities.json` | `human_maintainers` moves from `["Anthony", "Kendall"]` to `["Anthony Kendall"]`. **Not optional cleanup**: under exact matching the current two-fragment value matches no full-name byline, so the code change and the config change are one atomic change or Cairn's own record starts flagging. |
| A11 | `dev/.cairn/cairn-lock.yml` | Re-record the `hash` on the twin pair's `verbatim: true` row. `base_hash` is unchanged — it pins the install-time base, not the current content. |
| A12 | `bootstrap/tests/test_lifecycle_contract.py` | Update `test_identity_model_is_three_way_positive_human`. Of its six assertions exactly one breaks: `classify("Anthony (Maintainer)") == "human"` against a roster of `["Anthony"]`. **That assertion is the over-match defect written down as an expectation** — a name fragment plus a parenthetical role matching the allowlist. It is corrected to the full-name roster, not worked around. |
| A13 | `bootstrap/tests/test_byline_identity.py` *(new)* | The parametrized behaviour table, transcribed from the accepted proposal's Evidence table (see *channel discipline* below). |
| A14 | `bootstrap/tests/test_byline_identity.py` | The two [I5] loader-guard tests: a punctuation-only roster entry alongside a real one must not make a punctuation-only byline `human`; an empty-folding AI-registry entry must not make every byline `ai`. |

**Acceptance criteria — Chunk A**

* **The behaviour table passes**, every row, driven through `classify` with the
  roster `["Anthony Kendall"]`. Rows and expected values are transcribed from
  the proposal's committed Evidence table — an artifact written before the code
  exists — never generated by running the new code.
* **Perturbation, run and recorded — the table.** Replace `_fold_word` with the
  pre-fix `re.sub(r"[^a-z0-9]", "", raw.lower())` and restore set-intersection
  matching: the table **fails on 4 rows**, including `Anthony Kendall` itself
  (which becomes `unknown`) and the two presentational-variant rows. Restore
  byte-identical → green. Run for this plan against a transcription of the
  design; the implementing agent re-runs it against the landed code.
* **Perturbation — the NFD/NFKD split.** Switch the *granting* leg alone from
  `NFD` to `NFKD`, changing nothing else: **exactly one row flips** — the
  full-width byline `chr(0xff21)+"nthony "+chr(0xff2b)+"endall"` goes `unknown`
  → `human`. That single row is the entire mechanical justification for the
  two-strength design, so it must be present and it must be the *only* row that
  moves. Measured for this plan; if a second row moves at implementation, the
  perturbation was not isolated and the result is void.
* **Perturbation — the [I5] guards.** Delete the folded-value filter from
  `_load_human_maintainers`: with a roster of `["Anthony Kendall", "-"]` the
  byline `"."` classifies `human`. Delete it from `_load_ai_registry`: with an
  entry of `"-"`, the bylines `Anthony Kendall`, `Jane Doe` and an all-Cyrillic
  name **all** classify `ai`. Both measured for this plan.
* **Perturbation — the twins.** Apply the change to one twin only:
  `test_every_self_hosted_twin_stays_byte_identical_to_its_source` fails.
  **Run, not asserted**: measured for this plan in a `git archive HEAD` sandbox
  with one byte appended to `tools/lifecycle_planner.py`, against a clean
  sandbox baseline of 9 failures — the perturbed run reports 10, and the single
  delta is that node.
* **The live record does not regress.** `python tools/lifecycle_planner.py scan`
  from inside the checkout, captured **before** the edit to a scratch file, and
  diffed after. The four real identities in the tree must classify exactly as
  they do today. A non-empty diff is a stop.
* **Twin byte parity** holds after the edit: `shasum -a 256` equal on both
  files, and `cmp` silent.
* **`python bootstrap/scaffold.py --manifest` diff is empty** against a
  pre-change capture. 96 lines, `as_of 2026-08-03`.
* Full suite green **in the real checkout**, 0 skipped / 0 xfailed, collection
  grown by exactly the new nodes and dropped by none.
* **Mutation ledger in the commit body**: each perturbation above, the observed
  failure, and the byte-identical restore.

### Chunk B — the invariant, the corpus, and the residual pins

Test-only. This is where [I3] and [I4] are actually discharged, and it is the
chunk most worth a reviewer's attention, because the proposal's two named guards
could not do the job claimed for them.

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/tests/test_byline_identity.py` | **The non-empty-fold invariant** — [I4] restated so it can be true *and* can fail: for every input character whose Unicode general category begins `L` or `N`, `_fold_word(c, form)` is **non-empty**, at both strengths. No letter and no digit is ever deleted *to nothing*. The literal "preserves every input character" wording is unimplementable — case folding and combining-mark stripping both *replace* letters — and a test weakened at implementation to something that passes would not be the Decision's invariant while the record claimed it was. |
| B2 | `bootstrap/tests/test_byline_identity.py` | **The deletion-set pin** — [I2]. Enumerate every ASCII codepoint the fold deletes and assert the set equals the explicit allow-set complement stated in A1's docstring. This is the mechanical check the proposal's own *Why this tier* section asked a reviewer to run: *name every character class the fold deletes, and show that none of them carries identity.* Run literally against the proposal's wording it fails; against A1's corrected wording it passes. |
| B3 | `bootstrap/tests/test_byline_identity.py` | **The anti-collision test** — [I3]'s replacement. Over a corpus **committed in this module**, assert that no corpus name classifies `human` against a roster holding a *different* corpus name, except for the pairs the design deliberately merges (B4). |
| B4 | `bootstrap/tests/test_byline_identity.py` | **The R2 residual pin.** The [I1a] and [I1b] classes are asserted to **still collide** — a ligature/long-s variant and a decomposing-accent variant each classify `human` against the plain rostered name. Pinned, not fixed: R2 accepts this widening, and pinning it means a later narrowing of the granting fold is a deliberate, visible test change rather than a silent behaviour drift. |
| B5 | `bootstrap/tests/test_byline_identity.py` | **The roster-symmetry test, kept and relabelled.** `classify(x)` with roster `[x]` over the corpus. Its docstring says what it actually is — a smoke check on the AI leg and the empty-fold guard — **not** the international-cost measurement. Per [I3] it holds for every total function and cannot detect over-folding. |
| B6 | `bootstrap/tests/test_byline_identity.py` | **The [I6] separator cost, recorded as a test.** A CJK name rostered with an ASCII space and written with `chr(0x3000)`, and a French name rostered with an ASCII space and written with `chr(0x202f)`, both classify `unknown`. This is a **cost-recording** test: it asserts the false positive exists. It also asserts the **remedy**, so the cost is recorded with its exit: the same two bylines classify `human` when the roster carries the *exact* separator (measured at plan review — the `NFD` granting leg preserves a `Zs` character inside its word, so roster and byline fold to the same key). A recorded cost with no recorded way out reads as a dead end to the next reader. If the Maintainer answers question 3 by adopting `Zs` word breaks, the false-positive half of this test inverts — which is exactly the signal that the optional change landed. |
| B7 | `bootstrap/tests/test_byline_identity.py` | **The R3 residual pin.** Against author `Claude (Strategy)`, the `NFKD` comparator flags the precomposed-accent, mathematical-bold and circled-letter reviewer variants (3 of 4) and does **not** flag the Cyrillic one. Asserted as a *known* residual so it cannot regress silently and so closing it is a deliberate test change. |

**The corpus is a deliverable, and it must be adversarial.** Carry (i) from the
proposal's Response is explicit: *"the international corpus must be committed in
the test module, not described"*, because a figure resting on an unenumerated
synthetic corpus is not reproducible from the artifact. This plan adds a second,
sharper requirement, from measurement rather than from doctrine:

> **A corpus of dissimilar names gives the anti-collision test no power.**
> Measured for this plan: a twelve-name corpus of realistic international names
> passes the anti-collision test *even against a deliberately destructive fold
> that reduces each word to its first letter* — because no two of those names
> share initials. The corpus must contain, for each wrong fold worth defending
> against, at least one pair that fold would merge.

Verified for this plan, a corpus built to that rule discriminates:

| corpus property | catches |
|---|---|
| a shared-initials pair and a prefix pair (`Amos Kim` / `Anthony Kendall`; `Jan Doe` / `Jane Doe`) | any truncating or destructive fold |
| non-decomposing letter pairs (`Łukasz`/`Lukasz`, `Søren`/`Soren`) | a fold that deletes or transliterates non-ASCII |
| decomposing-accent pairs (`Ana Ngô`/`Ana Ngo`, `Ibrahim Şahin`/`Ibrahim Sahin`) | held as **pinned merges** (B4) — a fold that stops merging them has narrowed R2 |
| single-character-apart non-Latin pairs (Cyrillic, Han) | a fold that empties or collapses a whole script |

Measured outcome, four folds, `as_of 2026-08-03`: the accepted design **passes**;
a first-letter-truncating fold **fails** (two unexpected collisions); today's
ASCII-deleting fold **fails** (the two pinned merges do not occur, so the pin is
violated in the other direction). One honest limit, stated rather than hidden:
an `NFKD`-on-the-granting-leg variant **passes** this corpus — the corpus does
not discriminate the two-strength choice. That is what Chunk A's full-width
behaviour row is for, and it is the reason both tests are required rather than
either alone.

**Acceptance criteria — Chunk B**

* **B1 perturbation, run**: restore the pre-fix ASCII deletion and the invariant
  fails on a large, non-trivial count. Measured for this plan over samples
  spanning Latin-1, Latin Extended-A/B, Greek, Cyrillic, Arabic, Thai, Han,
  Devanagari, kana and the mathematical alphanumerics: the accepted fold gives
  **0** letters/digits folding to empty; today's fold gives **965**. That is a
  1-vs-0 outcome, not a margin.
* **B1's oracle is not the code under test.** The character sample and the
  `L*`/`N*` classification come from `unicodedata`, a Python standard-library
  table shipped with the interpreter. `lifecycle_planner.py` supplies the
  function under test and nothing else. This is the channel separation the
  repository has failed four times in one week; it is stated per-test in
  *Verification*.
* **B3 perturbation, run**: the anti-collision test **fails** against a
  first-letter fold, with `Amos Kim` / `Anthony Kendall` among the reported
  collisions. Run against the committed corpus, not a hypothetical one.
* **B4 perturbation, run**: remove combining-mark stripping from the granting
  fold; the pinned merges stop occurring and B4 **fails**. This is the future
  state the pin exists to make visible — narrowing the granting fold is R2's own
  named recovery path.
* **B6 perturbation, run**: switch the tokenizer to treat Unicode `Zs` as a word
  break; B6 **fails** (both bylines become `human`). Measured for this plan.
* **B7 perturbation, run**: give the comparator a confusables mapping that folds
  `chr(0x430)` to `a`; the fourth variant becomes flagged and B7 **fails**,
  which is what closing R3 should look like.
* **B5 carries no perturbation, and its docstring says so.** Per [I3] it cannot
  fail except through the AI leg or an empty fold. Claiming a perturbation for
  it would be the vacuity this chunk exists to remove. It ships as a labelled
  smoke check or not at all.
* Full suite green in the real checkout, 0 skipped / 0 xfailed.
* **Recorded as not established**: the corpus is synthetic and chosen to span
  failure classes, not sampled from a real multilingual name distribution. It
  discriminates against the four folds named above and no claim is made beyond
  those four.

### Chunk C — the release-facing entry

| # | File | Change |
|---|------|--------|
| C1 | `CHANGELOG.md > Unreleased > Fixed` | One behaviour-change entry: the homoglyph widening, the roster-granularity change, and the migration instruction (a roster entry is now a complete display name). **Plus the separator change** ([E1]): a byline whose words are separated by a non-ASCII `Zs` character is recognized *today* and classifies `unknown` after this change, so the entry states that a roster entry is compared **separator-for-separator** — such a name is rostered exactly as it appears in the byline, or typed with ASCII spaces. Two behaviour changes in the entry, not one with a footnote. This is R5's expiry trigger — if v0.4.0 ships without it, R5 is unresolved. |

**Acceptance criteria — Chunk C**

* The entry states the **behaviour change**, not only the fix: an adopter with a
  fragment-style roster must be able to read what to do. Blast radius today is
  Cairn itself (corrected in Chunk A) and **zero external adopters** (v0.3,
  pre-first-adopter), which is why this is a release note and not an upgrade
  note. If an adopter exists by v0.4.0, R5's row says an upgrade note is
  required instead.
* **Both behaviour changes are findable in the entry**, not only the headline
  one. A person with `chr(0xa0)` or `chr(0x3000)` inside their display name is
  recognized today and is not after this change; if the entry does not let them
  discover that and act on it, the entry is incomplete. This is where [E1] is
  discharged.
* `python scripts/check_cairn.py` green.
* `python scripts/claim_check.py CHANGELOG.md` clean.

## Acceptance criteria

Per-chunk criteria are above. These are the plan-level deliverables.

* **Tests that must pass.**
  * `python -m pytest bootstrap/tests` — the whole suite, green, **0 skipped /
    0 xfailed**, under the canonical interpreter (3.13.13), **in the real
    checkout**. Baseline 1601 passed, `as_of 2026-08-03`; collection grows by
    exactly the new nodes and drops none.
  * `bootstrap/tests/test_byline_identity.py` — the new module, exercising the
    classifier through `IdentityModel.classify` and through
    `_load_identity_model` over a temporary config, with the committed corpus.
  * `bootstrap/tests/test_lifecycle_contract.py` — the updated node, plus the
    existing terminal-Decision tests unchanged, so the classifier is exercised
    through its **public path** (the conformance report for a terminal proposal
    state) and not only at helper level.
  * `bootstrap/tests/test_notice_install.py` — the twin byte-parity node,
    unchanged and passing.
  * **Every new test shown non-vacuous by a run perturbation**, except B5, which
    is labelled a smoke check precisely because it cannot be. The ledger goes in
    each commit body.
* **Doc updates that must land.** All hand-authored, and there are only three:
  the in-code docstrings and comment block (A1, A2, A8), `CHANGELOG.md` (C1),
  and the `dev/PLANNING.md` residual rows (Chunk 0). **No generated docs, no
  snippet-synced blocks, no `docs/` change, no `doctrine/` change, no
  `AGENTS.md` change.** Stated explicitly because silent omission is a
  code-review finding.
* **Examples / smoke checks required.** `python tools/lifecycle_planner.py scan`
  from inside the checkout, before and after, diffed; `cmp` of the twin pair;
  `python bootstrap/scaffold.py --manifest`, expected **unchanged**, which is
  itself the assertion that this plan installs nothing new into an adopter tree.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk and the test that enforces it.**
  * *No letter and no digit is deleted to nothing, in any script* — the
    Decision's named invariant, in the only form that can both hold and fail.
    Enforced by B1, oracle from `unicodedata`.
  * *The fold's deletion set is exactly what its docstring says* — enforced by
    B2, which is the mechanical check the proposal asked a reviewer for, moved
    into the suite so it runs every time instead of once.
  * *Distinct names produce distinct keys, except for the ratified R2 classes* —
    enforced by B3 against an adversarial corpus, with B4 pinning the
    exceptions. This pair is what [I3] and [I4] were reaching for; neither
    proposed test could reach it.
  * *Roster and byline fold through the same function at the same strength* —
    structural in A3/A5 (one call each side), smoke-checked by B5.
  * *The AI leg keeps precedence over the human leg* — enforced by the
    behaviour table's scribing rows (A13), where `Claude scribing for Anthony
    Kendall` must stay `ai`.
  * *The twins stay byte-identical* — enforced by the existing node
    `test_every_self_hosted_twin_stays_byte_identical_to_its_source`,
    perturbation-verified for this plan.
* **Public-path → test mapping.** The public entry point this change affects is
  the planner's conformance report for a terminal proposal state, reached
  through `IdentityModel.classify` and consumed at exactly one call site —
  `tools/lifecycle_planner.py:613` — where both `ai` and `unknown` raise a
  violation. It is exercised through that public path by the existing
  terminal-Decision tests in
  [`test_lifecycle_contract.py`](../../bootstrap/tests/test_lifecycle_contract.py),
  which this plan extends rather than replaces. The second affected public path
  is the `independent_review` gate at `tools/lifecycle_planner.py:683`, reached
  through `python tools/lifecycle_planner.py next`; B7 pins its residual
  behaviour. The new test module is cited as a code span rather than a relative
  markdown link because it does not exist yet; it is registered under *Proposed
  paths*, and the link form is adopted at code review once the file resolves.
* **Failure modes.** An unrecognized byline → `unknown` → violation. An absent,
  unreadable or wrong-shape config → empty allowlist → no byline can be
  confirmed human (the existing fail-closed posture, unchanged and re-verified:
  with no config file at all, `Anthony Kendall` classifies `unknown` and
  `Claude` classifies `ai`). A config entry folding to nothing → skipped, per
  A3/A4. A byline whose non-ASCII form differs from the rostered form
  (`O’Brien` rostered as `O'Brien`) → flagged; a false positive in the safe
  direction, resolved by rostering the exact form. **Two costs are recorded, not
  claimed absent**: that apostrophe case, and [I6]'s non-ASCII separator case
  (B6). The proposal's *"international cost: zero"* headline is not repeated
  here — [I3] showed the measurement producing it was near-guaranteed by
  construction.
* **Edge cases handled.** Empty byline; whitespace-only byline; punctuation-only
  byline; punctuation-only roster entry; empty-folding registry entry;
  single-word names; multi-word names; word-count mismatch; case variation;
  accent variation; non-Latin scripts; the ten separators measured in
  *Verification*; zero-width and soft-hyphen characters; full-width,
  circled and mathematical-alphanumeric forms; versioned agent bylines;
  roster entries with leading or trailing whitespace.
* **Known omissions, stated rather than implied.** (a) The bare-`re.sub`
  normalization pattern is **not swept** elsewhere — `tools/lifecycle.py` and
  `scripts/` are uncovered by both proposal reviews and by this plan; it is a
  mandate to the plan reviewer. (b) The corpus is synthetic. (c) The `NFD`
  granting choice rests on an enumeration of `NFKD`'s compatibility mappings
  that is *representative*, not exhaustive; B2 pins the ASCII deletion set but
  no test enumerates the compatibility mappings, and no one has. (d) `casefold()`
  was sampled, not enumerated against the full case-folding table — [I1a] shows
  the class reaches the granting path and there may be worse members than
  `chr(0x17f)`. (e) **No hostile roster has been tested.** Both reviews probed
  benign typos only. `dev/.cairn/agent-identities.json` is untracked by the
  lockfile and written by no installer, so a deliberately hostile config is a
  live and unexplored threat model. (f) R1, R3's Cyrillic case and R4 are
  untouched by any measurement in this lineage.

## Verification

The concrete commands the implementation must pass.

<!-- cairn:slot verification-commands -->
The standing gates Cairn runs before a change lands (the same ones CI
enforces):

* **Engine suite** — `python -m pytest bootstrap/tests` (the whole
  suite; scope to `bootstrap/tests/test_<surface>.py` while iterating,
  but the full suite gates the cut).
* **Prose integrity** — `python scripts/check_cairn.py` (internal link
  / anchor resolution + claim-path check over the Markdown tree).
* **Quality gate** — `python scripts/quality_gate.py` (order-
  independence + vendor-neutrality + redundancy; `--sub neutrality`
  alone for a doctrine / template wording change).
* **Write-time claim check** — `python scripts/claim_check.py <file>` over
  each proposal / plan / doc the change authored. **One file per
  invocation** — the checker takes a single path and exits 2 (usage) on
  more, so loop rather than passing a list.

Plan-specific gates (a security-lint budget, a doc-drift gate, the
model-selection mapping check `python scripts/check_model_selection.py`)
are added per plan when the change touches that surface.
<!-- cairn:end verification-commands -->

Run everything under the canonical interpreter (`~/conda_envs/lhm/bin/python`,
3.13.13) with `PYTHONDONTWRITEBYTECODE=1`. A different Python minor silently
changes the result, and `unicodedata` in particular tracks the interpreter's
Unicode version — so the interpreter must be named alongside any figure.

**Plan-specific gates, added here because this change touches those surfaces.**

* **Twin byte parity** — `cmp tools/lifecycle_planner.py templates/skills/_lib/lifecycle_planner.py`,
  silent, plus `shasum -a 256` on both, equal. Before and after.
* **The install-contract assertion** — `python bootstrap/scaffold.py --manifest`,
  diffed against a capture taken **before** the edit. Expected empty.
* **The live-record assertion** — `python tools/lifecycle_planner.py scan`,
  diffed against a capture taken **before** the edit. Expected empty.
* **The lockfile row** — the twin pair's `hash` re-recorded, `base_hash`
  untouched.
* **The gate manifest** — expect exactly one *new* `FROZEN-MODIFIED` line, for
  `bootstrap/tests/test_lifecycle_contract.py`, alongside the two that already
  exist at `05515df`. Do not regenerate the manifest; that is a supervised
  Maintainer step.
* **The mutation ledgers** — per chunk, in the commit body: the deletion, the
  observed failure, and the byte-identical restore.

### Channel discipline — for every verification step, what supplies the input

The repository has recorded four instances in one week of an artifact supplying
the material used to verify it. This table is how this plan answers that, and a
reviewer should treat a missing or hand-waved row as a finding.

| Verification step | Input | Channel it arrives by | Is it the thing being verified? |
|---|---|---|---|
| Behaviour table (A13) | the row set and the expected column | transcribed from the accepted proposal's Evidence table, committed at `dcd64fa` before any code existed | **No** — it predates the implementation |
| Behaviour table | the roster | a literal in the test's temporary config | No |
| Non-empty-fold invariant (B1) | the character sample, and `L*`/`N*` classification | `unicodedata`, a standard-library table shipped with the interpreter | **No** — the planner supplies only the function under test |
| Deletion-set pin (B2) | the expected deletion set | the explicit allow-set literal in A1's docstring, written by hand | No, but **it is adjacent** — see the caveat below |
| Anti-collision corpus (B3) | the name list | hand-written into the module; never harvested by running the fold | No |
| R2 residual pin (B4) | the expected collisions | transcribed from the Internal review's measured output block, committed at `a597b30` | **No** — it predates the implementation |
| R3 residual pin (B7) | the 3-of-4 expectation | transcribed from the Internal review's measured block; independently re-derived for this plan | No |
| Twin parity | the comparison | byte equality of two files; the oracle is supplied by neither | No |
| Suite baseline | 1601 passed | pytest in the real checkout, before the change | No |
| `--manifest` diff | the pre-image | captured to a scratch file **before** editing | No — provided the capture is not regenerated afterwards |
| `scan` diff | the pre-image | captured to a scratch file **before** editing | No — same proviso |
| Sandbox perturbation deltas | the 9-failure floor | a **clean** `git archive HEAD` sandbox, run separately | No — the baseline comes from the unpatched tree |

**The one adjacency, named rather than buried.** B2's expected deletion set is
written in the same file it verifies — the docstring and the code are both in
`lifecycle_planner.py`. That is by design: [I2]'s recommended disposition was
*"restrict the deletion to an explicit codepoint set and delete nothing else, so
that the rule and the code are the same statement."* The test then proves the
statement is *self-consistent*, not that it is *right*. What makes it non-vacuous
is that the allow-set is a literal a human wrote and a reviewer can read, while
the deletion is computed by executing the fold over `range(0x80)` — so a change
to the fold's logic that widens the deletion fails the test even though both
live in one file. A reviewer should decide whether that is enough; if not, the
allow-set literal moves into the test module and the docstring cites it.

### Reproductions run for this plan

Every figure this plan asserts was produced by execution at `05515df`,
2026-08-03, under the canonical interpreter, against a scratch transcription of
the accepted design in the session scratchpad. **No repository file was
edited.** That is the same limitation both proposal reviews declared, and it
applies here: nothing below is evidence about the code that will ship, only
about the design it will implement.

1. **The [I1a] and [I1b] collisions** — six roster/byline pairs (long-s,
   st-ligature, Vietnamese tone, kana KA/GA, Devanagari nukta, Cyrillic YE/YO)
   through the transcribed `classify`. All six return `human`. R2's stated
   expiry condition is met before ratification, which is Maintainer question 2.
2. **The [I5] guards** — `-`, `--`, `  .  ` and `!!!` all fold to the empty
   tuple at both strengths; with the human-side guard removed a `.` byline
   classifies `human`; the AI-side registry entry `-` folds to `""` and
   `"anything".startswith("")` is `True`.
3. **The behaviour table under three folds** — run over a **15-row subset** of
   the proposal's 20-row Evidence table, chosen to cover every security case
   plus the empty, whitespace-only and punctuation-only bylines the proposal's
   table does not carry. Accepted design passes all 15; today's fold fails 4;
   `NFKD`-on-the-granting-leg fails exactly 1 (the full-width row), with the
   tokenizer held constant so the perturbation is isolated. **The implementing
   agent transcribes all 20 proposal rows plus the three boundary rows** — the
   subset is this plan's evidence, not the shipped table.
4. **The anti-collision corpus under four folds** — accepted design passes;
   first-letter fold fails; today's ASCII fold fails; `NFKD`-on-granting passes
   (the corpus does not discriminate that choice, which is why row 3 exists).
5. **The non-empty-fold invariant** — 0 empties under the accepted fold, 965
   under today's, over nine sampled blocks.
6. **The ten separators** — `chr(0x2028)`, `chr(0x2029)`, `chr(0xa0)`,
   `chr(0x2000)`, `chr(0x3000)`, `chr(0x200b)`, `chr(0xad)`, `chr(0x202f)`,
   `chr(0x1680)`, `chr(0x205f)`, each in `"Anthony<sep>Kendall"`, under both
   tokenizers. All `unknown` under the accepted ASCII-only split; six become
   `human` under a `Zs` split. Categories read from `unicodedata`.
7. **The [I6] legitimate names** — CJK with `chr(0x3000)` and French with
   `chr(0x202f)`, rostered with ASCII spaces: `unknown` as accepted, `human`
   under a `Zs` split.
8. **The R3 comparator** — four reviewer variants against author
   `Claude (Strategy)`: precomposed accent, mathematical-bold `C` and circled
   `C` all newly flag; Cyrillic does not. 3 of 4, confirmed.
9. **The twin-parity perturbation** — clean `git archive HEAD` sandbox: 9
   failed, 1591 passed, 1 skipped. One byte appended to one twin: 10 failed,
   1590 passed, 1 skipped. Single delta is the parity node.
10. **The gate state** — `_gate_manifest.py verify --no-collect` reports two
    pre-existing `FROZEN-MODIFIED` holds; the frozen set holds 164 entries;
    membership of all four touched paths checked individually.
11. **The suite and prose baselines** — 1601 passed / 0 failed / 0 skipped;
    `check_cairn` OK over 174 Markdown files.
12. **The `repr()` vs `ascii()` diagnostic** — `repr()` of the Cyrillic byline
    is visually identical to the honest one; `ascii()` renders the escape `\u0430`.
13. **The R4 escaper seam** — read `agent-context-scrub`'s proposed
    `_FIELD_ESCAPES` table; it covers controls and the two line separators only,
    and states that international text passes untouched.

**Note on doc gates**: drift gates (broken references, stale renders,
snippets that diverged from their source) catch **drift**, not
**absence** of new doc updates. Confirm each doc named in Acceptance
was actually updated; the gates don't enforce that.

### B1 as landed — the per-leg narrowing, recorded

*Appended at implementation, 2026-08-03 — after the plan review and Response
below, which did not see it. Nothing above or below is edited; this subsection
only adds.*

**The B1 row above says the invariant holds "at both strengths". What shipped
does not, and until this subsection the narrowing was nowhere in the record** —
an independent audit of the landed work surfaced the gap. The relaxation is
factually forced and safe-direction, so the tests stay exactly as shipped; the
defect was the record, which is precisely the failure the B1 row itself names:
*"a test weakened at implementation to something that passes would not be the
Decision's invariant while the record claimed it was."*

**Re-measured against the landed `_fold_word`** (not against a scratch
transcription), over the whole codespace `range(0x110000)`, with the `L*`/`N*`
classification read from `unicodedata` — UCD **15.1.0**, canonical interpreter
3.13.13:

| leg | fold | letters/digits folding to empty |
|---|---|---|
| granting (`_grant_words`) | `NFD` | **0** |
| flagging (`_flag_words`) | `NFKD` | **16** |

So B1 ships as two nodes with **different strengths of claim**, and the
difference is the thing to record:

* `test_no_letter_or_digit_folds_to_nothing_on_the_granting_leg` —
  **unconditional**, `empties == []` over the whole codespace at `NFD`. This is
  the leg where a deletion would *grant*, and it is the leg the Decision's
  invariant is about.
* `test_flagging_leg_empties_are_only_compatibility_marks` — a
  **characterization**, not an unconditional invariant. It asserts that every
  `NFKD` empty decomposes entirely into combining marks and ASCII characters
  outside the allow-set; it therefore permits the 16 below and fails on a
  seventeenth member outside the characterization.

**The 16, enumerated** (`as_of 2026-08-03`, UCD 15.1.0 — the set is
UCD-version-dependent, which is why the interpreter is named alongside it):

| codepoints | count | category | `NFKD` decomposition |
|---|---|---|---|
| `U+FC5E`–`U+FC63` — ARABIC LIGATURE SHADDA WITH DAMMATAN / KASRATAN / FATHA / DAMMA / KASRA / SUPERSCRIPT ALEF, ISOLATED FORM | 6 | `Lo` | ASCII SPACE + two `Mn` marks |
| `U+FE70`, `U+FE72`, `U+FE74`, `U+FE76`, `U+FE78`, `U+FE7A`, `U+FE7C`, `U+FE7E` — ARABIC FATHATAN / DAMMATAN / KASRATAN / FATHA / DAMMA / KASRA / SHADDA / SUKUN, ISOLATED FORM | 8 | `Lo` | ASCII SPACE + one `Mn` mark |
| `U+FF9E`, `U+FF9F` — HALFWIDTH KATAKANA VOICED / SEMI-VOICED SOUND MARK | 2 | `Lm` | one `Mn` mark (`U+3099` / `U+309A`) |

Only the **even** codepoints of `U+FE70`–`U+FE7E` are in the class — measured,
not inferred from the range. The odd ones (`U+FE71`, `U+FE77`, `U+FE79`,
`U+FE7B`, `U+FE7D`) decompose to ARABIC TATWEEL `U+0640` plus a mark, and the
tatweel is non-ASCII, so the allow-set keeps it and they fold non-empty.

**Why the relaxation is forced rather than chosen.** The shipped fold is three
steps: case-fold and normalize at `form`; drop every combining mark; keep a
character only if it is non-ASCII or in the allow-set. Each of the 16
decomposes at `NFKD` *entirely* into combining marks, plus — for 14 of them —
one ASCII SPACE. Step 2 removes the marks, and it is load-bearing: it is what
merges the [I1b] classes R2 ratifies and what B4 pins. Step 3 removes the
space, and it is load-bearing: A1's explicit allow-set is the disposition [I2]
asked for and B2 pins it. Nothing survives either step. There is therefore **no
version of the accepted design** in which the flagging leg carries the
invariant unconditionally: the only escapes would be to stop stripping
combining marks at `NFKD` — which breaks the presentational-disguise close the
flagging leg exists for — or to special-case sixteen codepoints, which neither
the proposal nor the Decision asked for. The set is a property of `NFKD` plus
the allow-set, not of this implementation.

**Why it is safe-direction.** Each half measured against the landed code:

* **It cannot grant.** `_grant_words` is `NFD`-only, and the human allowlist is
  compared *exclusively* through it — `classify` reaches the roster by
  `_grant_words(name) in self.human` and by no other path. All 16 fold
  **non-empty** at `NFD`, so a word made of them has a real granting key, never
  the empty tuple that `()` -equality would admit. The flagging leg never
  reaches the human allowlist at all.
* **On the AI leg it can only under-flag, and only in a case that could not
  match anyway.** `_fold_words` drops a word that folds to nothing, so the whole
  effect is that a word made **entirely** of these characters contributes no
  prefix candidate. A *mixed* word is untouched — measured, `"Cl" +
  chr(0xff9e) + "aude"` and `"Cl" + chr(0xfe7c) + "aude"` both still classify
  `ai`, because stripping the mark is exactly what the flagging leg is for. And
  an all-mark word has nothing to match: a config `ai_agents` entry built from
  the same characters folds through `_flag_words` too, so it is dropped rather
  than admitted (measured: it contributes no token, and `""` stays out of the
  registry).
* **The third consumer is fail-closed too.** `_identity_token` shares
  `_flag_words`, so an all-mark author name yields `""`. Both call sites treat
  *equal* tokens as non-independent — the conformance check raises a violation,
  the `independent_review` gate withholds — so an empty flagging key collapses
  toward flagging, never toward clearance.

**What this does not establish, stated rather than implied.** The
characterization is asserted over the codespace, but the safety argument above
is an argument about *call sites*, not a test: no node asserts that the granting
leg never receives an `NFKD` key. That property is structural — one call each
side, per the *Author-accounting* invariant list — and it is something the code
reviewer should re-check directly rather than take from this subsection.

## Plan review — the brief, and why the tier is not discharged

*Required — External, security lens. Implementation does not start until a
review has landed under this heading.* The tier is the proposal's, carried
forward; and the proposal's Internal reviewer disclaimed their own pass toward
it in terms.

> **The landed review appends here as a `### Plan review -- <reviewer> --
> YYYY-MM-DD` sub-heading** (plus a `### Sharpening` sub-heading if it raised
> findings). **Do not rename this heading to a bare `## Plan review`.** The
> checker matches a section *kind*, not a review, so a bare heading would report
> the gate satisfied by a placeholder. This heading is shaped so it cannot be.

**Why the tier is right independent of the mandate.** The proposal states the
reason better than this plan can: its author *"found a class of defect at 07:59
and then wrote two fresh instances of that identical class within the hour.
Vigilance did not catch it; an adversarial reader did."* The same-type Internal
round that followed then found seven further findings, two of which were that
the proposal's own regression guards could not work. Same-agent vigilance has a
measured failure rate on this exact surface.

**Mandates for the reviewer** — offered so the pass has a target rather than a
lens.

1. **Is the kept/dropped partition exhaustive, and is `NFD`-for-granting /
   `NFKD`-for-flagging the right split?** This is the judgment the proposal
   named as the reason for the tier, and it is a Unicode-semantics question
   where a same-type reviewer inherits the author's blind spots exactly. B2 pins
   the ASCII deletion set; **nothing pins the compatibility mappings**, and the
   author's enumeration of them is declared representative, not exhaustive.
2. **Break the `casefold()` claim further.** [I1a] sampled the full-case-folding
   expansions that reach the granting path (`chr(0x17f)`, the `fi`/`ffi`/`st`
   ligatures, sharp-s, micro sign, dotted capital I). Nobody has enumerated
   `CaseFolding.txt`. Is there a member that folds to a rostered name and reads
   as something else more damagingly than a long-s?
3. **The hostile roster.** `dev/.cairn/agent-identities.json` is untracked by
   the lockfile, written by no installer, and both proposal reviews tested only
   benign typos. A deliberately hostile config is unexplored. Can one widen
   authority beyond what R1 already concedes?
4. **Sweep the bare-`re.sub` pattern.** `tools/lifecycle.py` and `scripts/`
   are unswept by both reviews and by this plan. Is the same
   delete-the-non-ASCII shape present on another authority surface? A clean
   enumeration closes a known omission at plan time.
5. **Channel discipline over every step.** Take the table above and challenge a
   row — particularly the B2 adjacency, which this plan names as its weakest.
6. **Answer, or tell the Maintainer they must**: the three Maintainer questions,
   especially question 3 (`Zs` word breaks). This plan measured both sides and
   deliberately did not decide.

**What the reviewer should not spend attention on.** The design itself —
character-preserving fold, exact tuple matching, the two-strength split — has
survived an External round and an Internal round, and both concluded it should
land. Re-opening it is out of bounds; breaking it is the assignment.

## Code review

*Filled in after implementation commits land.* Per `doctrine/plans.md`, the
reviewer is **not** the implementing agent, the section is append-only, and a
clean final review carries a falsification ledger and a coverage line. The
landed review appends here as a `### Code review -- <reviewer> -- YYYY-MM-DD`
sub-heading; the heading above is shaped like the plan-review one and for the
same reason.

Begin with `**Model**: <model or tier when known; "unknown" if not. Do not
copy-paste old model labels from past templates or archives; query and state
your actual running model identity.>` immediately below the section header.

Three checks this plan asks its code reviewer to run rather than read:

* **Re-run the original exploit against the landed code.** Build the byline
  `"Cl" + chr(0x430) + "ude scribing for Anthony Kendall"`, run it through
  `_load_identity_model` over the live tree, and confirm it classifies
  `unknown`. A code review that asserts the fix without re-running the exploit
  does not close it.
* **Re-run one perturbation from each chunk's ledger**, chosen by the reviewer,
  not by the implementer. B5 is exempt and its docstring must say why.
* **Read the new test module and, for each test, name the future state in which
  it fails.** A test whose answer is "none" is a finding, not a passing test.
  This lineage shipped one such test that stayed green for 63 days while the
  drift it was named for occurred.

## Lasting-truth migration

*Filled in at archive time.* Per `doctrine/plans.md`, the archive commit body
carries the literal `Follow-ups migrated to:` block naming where each deferred
item went, so the migration is auditable from the commit log alone — and the
plan does not archive until every deferred follow-up has a durable home outside
it.

The homes are pre-declared here so archive time is bookkeeping rather than
recall: R1, R2 (restated), R3, R4 (corrected), R5 and R6 → `dev/PLANNING.md`
rows landed at plan-open (Chunk 0); R2's classes additionally pinned in code by
B4; R3's measured state pinned by B7; R5 discharged by the `CHANGELOG.md` entry
(C1); [I6]'s cost pinned by B6; the pre-existing `Devine` over-flag →
`dev/PLANNING.md` (0g).

**Three items that are not residuals and must not be archived away as if they
were:**

* **The three Maintainer questions.** They are the Maintainer's to answer or
  strike; an implementing agent cannot discharge them and an archive cannot
  absorb them.
* **[I7b] — the sibling's stale characterization.** `planner-line-semantics`
  states, in its *Cross-lineage file collisions* section, that under scope 2 a
  byline built with `chr(0x2028)` classifies `human`, and prescribes widening a
  poison rule. Both statements describe the **Amendment's** recipe, which this
  proposal replaced; under the accepted design that byline classifies `unknown`,
  and there is no poison rule to widen. The correction is **that proposal's to
  make at its own Response**, not an edit made from this plan. Recorded here so
  the obligation exists on both sides rather than neither.
* **The unswept `re.sub` pattern.** If the plan reviewer returns a clean
  enumeration it closes at plan time; if not, it needs a durable home before
  this plan archives.

Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside the
plan.

This section is append-only once written.

<!-- cairn-accept: homoglyph reason="The External reviewer's exploit reproduction below embeds the live Cyrillic U+0430 spoof token this plan exists to close; the token IS the finding, and rewriting it to ASCII would delete the evidence. Block-scoped over the reviewer's section only. The scanner flagging it is the detector working, not a defect." reviewer="Claude (author, marker only)" date=2026-08-03 -->

## Plan review -- Gemini Flash (External, security lens) -- 2026-08-03

**Steelman.** This plan presents a complete, mathematically sound redesign of identity byline classification. It addresses the character-deleting normalization flaw (`re.sub(r"[^a-z0-9]", "", raw.lower())`) which previously allowed homoglyph spoofing (`chr(0x430)` Cyrillic 'а' replacing ASCII 'a' to grant Maintainer authority). The proposed two-strength normalization (`NFD` for authority-granting, `NFKD` for AI-flagging) and exact tuple matching close the privilege-widening defect completely.

### Concerns

* **[E1] Unicode `Zs` (space separator) word breaking behavior.**
  The plan explicitly retains ASCII-only whitespace splitting (`re.split(r"[\s\t\n\r]+", raw)`). As demonstrated in the plan's Maintainer questions, legitimate non-ASCII spaces like `chr(0x3000)` (Ideographic Space) or `chr(0x202f)` (Narrow No-Break Space) will fail to tokenize into separate words and classify as `unknown`. While fail-closed (safe), Maintainers should note that international human names containing non-ASCII space separators must either be rostered with those exact separators or typed with ASCII spaces.

### Covered

* **Exploit reproduction and fix verification**:
  Executed test python script reproducing the homoglyph spoofing attack:
  - Constructed spoofed byline: `"Cl" + chr(0x430) + "ude scribing for Anthony Kendall"`.
  - **Pre-fix classifier**: returned `True` for Maintainer authorization (GRANTING HUMAN) via set-intersection word matching against `["anthony", "kendall"]`.
  - **Post-fix classifier (Plan A1–A5 exact tuple matching)**: returned `False` (`matches_new == False`), classifying correctly as `unknown`.
* **NFD non-decomposing character behavior**:
  Verified `chr(0x0141)` (`Ł`) under `NFD`: `fold_word_new('Łukasz', 'NFD')` returns `'łukasz'`, which does NOT collapse to `'lukasz'`, preserving character identity without dropping non-ASCII letters.

```
=== EXPLOIT REPRODUCTION ON BYLINE CLASSIFICATION ===
Raw spoof string repr: 'Clаude scribing for Anthony Kendall'
Raw spoof string ascii(): 'Cl\u0430ude scribing for Anthony Kendall'
OLD CLASSIFIER MATCHES ROSTER (GRANTING HUMAN)? True
NEW CLASSIFIER MATCHES ROSTER (GRANTING HUMAN)? False

=== NFD NON-DECOMPOSING TEST ('Łukasz') ===
NFD fold: 'łukasz'
NFKD fold: 'łukasz'
Does Łukasz fold to 'lukasz' under NFD? False
```

### Not covered / low confidence

* Parsing functions in `planner-line-semantics` (`_parse_status`, `_parse_field`, `_parse_sections`) remain in a separate proposal and were not audited in this pass.

### Recommendation

**READY FOR IMPLEMENTATION.** The plan's character-preserving fold, two-strength normalization split, exact tuple matching, and adversarial corpus requirements are verified and sound.

<!-- cairn-accept-end: homoglyph -->

## Response to plan review -- Claude (author) -- 2026-08-03

**Model**: Claude Opus 5

**One finding, accepted — and verifying it surfaced a hazard the finding did
not name.** [E1]'s behaviour claim reproduces exactly, and the remedy it
asserts works. But the review describes ASCII-only splitting as something this
plan *retains*, and that is backwards: today's code tokenizes with a bare
`name.strip().split()`, which splits on **Unicode** whitespace, so every `Zs`
separator in question classifies `human` in the tree as it stands. [E1] is a
behaviour **change** this plan introduces, not an inherited limitation — which
moves it out of "Maintainers should note" and into `CHANGELOG.md`. Separately,
the regex the review quotes as the plan's implementation,
`re.split(r"[\s\t\n\r]+", raw)`, appears nowhere in the plan and does **not**
implement it: `\s` in a `str` pattern is Unicode-aware, so an agent who took
that snippet as the recipe would silently answer Maintainer question 3 in the
affirmative. Four small chunk amendments; no scope added.

### [E1] Unicode `Zs` space separators -- **ACCEPTED**

**The finding, reproduced before disposing.** The plan retains ASCII-only
whitespace splitting, so `chr(0x3000)` IDEOGRAPHIC SPACE or `chr(0x202f)`
NARROW NO-BREAK SPACE inside a legitimate human name fails to tokenize into
separate words and classifies `unknown`. Fail-closed and therefore safe, but
Maintainers must be told that such a name has to be rostered with those exact
separators, or typed with ASCII spaces.

**Verified independently**, against a scratch transcription of A1–A5 in the
session scratchpad (no repository file edited), canonical interpreter 3.13.13,
`unicodedata` 15.1.0:

```
CJK byline U+3000 vs ASCII-space roster:  'unknown'   grant_key=('王\u3000伟',)
CJK byline U+3000 vs U+3000 roster    :    'human'
FR  byline U+202F vs ASCII-space roster:  'unknown'   grant_key=('jean\u202fdupont',)
FR  byline U+202F vs U+202F roster    :    'human'
FR  byline ASCII  vs U+202F roster    :  'unknown'
```

Both halves hold: the false positive is real, and rostering the exact separator
is a working exit — the `NFD` granting leg preserves a `Zs` character inside its
word, so roster and byline fold to the same key. The flagging leg behaves as the
two-strength design intends and was checked too: `NFKD` maps all three of
`chr(0x3000)`, `chr(0x202f)`, `chr(0xa0)` to an ASCII space, which the allow-set
then drops, so `"Cl" + chr(0x202f) + "aude"` still classifies `ai`. The
separator issue is confined to the granting leg, in the safe direction, exactly
as the reviewer says.

**Three things the finding did not name, and they are why this is accepted
rather than cited as covered.**

1. **The direction is reversed.** Measured against the *live* planner with the
   current roster, `chr(0x3000)`, `chr(0x202f)`, `chr(0xa0)`, `chr(0x1680)`,
   `chr(0x205f)` and `chr(0x2000)` between "Anthony" and "Kendall" **all
   classify `human` today** — because `_ai_candidate_tokens` and
   `_identity_token` both use a bare `.split()`. So this plan *removes* a
   recognition that exists, and the plan's own question-3 text — "if the
   Maintainer wants the change, it is a one-line edit" — had the change pointing
   the wrong way. A behaviour a user has today and loses tomorrow belongs in the
   release notes, which is where the plan did not have it.
2. **The review's quoted mechanism would implement the opposite of the plan.**
   `re.split(r"[\s\t\n\r]+", "Anthony" + chr(0x3000) + "Kendall")` returns
   `['Anthony', 'Kendall']` — two tokens, because `\s` is Unicode-aware; only
   `re.ASCII` (or an explicit class) gives one. That snippet is not in the plan,
   but it is now in the plan's file, above a `READY FOR IMPLEMENTATION`, and
   B6 — the test that would catch it — lands a chunk after the tokenizer does.
3. **What *was* already covered, stated so the amendment stays minimal.** A7's
   `unknown` message already tells a Maintainer that a roster entry must be "the
   complete display name as it appears in the byline" and appends the `ascii()`
   escape for any non-ASCII byline; measured, that renders the French case as
   `'Jean\u202fDupont'`, so the separator is visible at the moment of failure.
   The in-tool diagnostic path was there. The release-facing surface and the
   tokenizer's mechanism were not.

**Plan changes — four amendments, all inside existing rows.**

* **Chunk A, row A2.** Added that "ASCII whitespace only" is a *mechanism*
  requirement, not a description: the split is an explicit ASCII class
  (`[ \t\n\r\f\v]+`, or an `re.ASCII` pattern), naming both Unicode-aware traps
  — today's bare `.split()` and a `\s` class — and noting B6 catches either but
  lands a chunk later.
* **Chunk C, row C1.** The `CHANGELOG.md` entry now carries **two** behaviour
  changes, not one: the roster-granularity change, and the separator change —
  a roster entry is compared separator-for-separator, so a name written with a
  non-ASCII `Zs` is rostered exactly as it appears in the byline or typed with
  ASCII spaces.
* **Chunk C acceptance criteria.** New criterion: both behaviour changes must be
  findable in the entry by someone with `chr(0xa0)` or `chr(0x3000)` in their
  display name. This is where [E1] is discharged.
* **Chunk B, row B6.** The cost-recording test now also asserts the **remedy**
  — the same two bylines classify `human` when the roster carries the exact
  separator. A recorded cost with no recorded way out reads as a dead end.

**Also amended, and flagged rather than decided:** Maintainer question 3 gains a
first bullet recording the measured baseline — that a `Zs` split *preserves*
today's behaviour and the accepted ASCII-only split is the change — and its
closing sentence is corrected to match. The question itself is untouched and
stays the Maintainer's; this plan still ships the accepted design absent an
answer. The exploit is unaffected either way, as already measured.

### The reviewer's "Not covered / low confidence" note

Genuinely out of scope, no follow-up row needed. `planner-line-semantics`'s four
parsing functions are fenced out of this plan by name in *Scope* — "Same module,
disjoint functions, no shared line, either landing order works" — and the one
obligation that crosses the two lineages, [I7b]'s stale characterization, is
already recorded in *Lasting-truth migration* as that proposal's to correct at
its own Response.

Two items from the reviewer's mandates did **not** come back, and I record it
rather than treat silence as clearance. Mandate 4 asked for a sweep of the
bare-`re.sub` pattern in `tools/lifecycle.py` and `scripts/`; the plan had
pre-declared that "if the plan reviewer returns a clean enumeration it closes at
plan time; if not, it needs a durable home before this plan archives." No
enumeration came back, so the fallback applies unchanged and that known omission
stands open. Mandates 1–3 and 5 (the compatibility-mapping enumeration, the
`CaseFolding.txt` question, the hostile roster, the B2 adjacency) are likewise
unanswered; they remain listed as omissions in *Author-accounting* and are not
converted into claims by a clean verdict. Nothing here blocks Chunk A — the
tier is discharged and the review's verdict stands — but the plan's own
uncovered list is not shorter than it was before the pass.

## Maintainer ruling 2026-08-04 -- the three questions, answered

**Authorization, quoted verbatim:**

> Q1 - Yes
>
> Q2 - Restatement is confirmed
>
> Q3 - Ship as accepted

Scribed by Claude on the Maintainer's instruction. This is a **ruling on an
already-accepted plan**, not a Decision; the source proposal's Decision stands
unchanged.

### Q1 — "as revised" carries the Internal review's revisions

Answered **yes**. Chunk A's contents stand as planned. The Internal review
preceded the Decision and its revisions were on the record when the accept was
given, so the narrow reading would have ratified a version that no longer
existed. This also closes, for this plan, the thread that produced the
2026-08-03 repair — three Decisions found resting on undispositioned reviews.

### Q2 — R2 lands in its restated form

Confirmed. R2 is ratified as **canonical-decomposition equivalence plus full
case folding**, with the three falsifying classes named on the record:

* **full case folding** expands ligatures and long-s, so a byline a reader sees
  as *Kriften Long* keys as the rostered *Kristen Long*;
* **combining-mark stripping** collapses marks that carry letter identity in
  Vietnamese, Japanese, Devanagari and Cyrillic — so **a different person's**
  name can key as the rostered one;
* case.

The wording originally submitted for ratification — *"every member reads as the
rostered name to a human"* — is **not** what is ratified. Its mechanical expiry
was already satisfied at the moment it was put forward, which is debt wearing a
decision's clothes. The restated form is pinned in
`bootstrap/tests/test_byline_identity.py`, so a later narrowing is a visible
test change rather than silent drift.

### Q3 — ship the accepted ASCII-only split; `Zs` is not adopted

Confirmed. The accepted design ships and the international cost is recorded as
a known residual rather than paid for by widening the `human` leg.

The deciding evidence is the counterexample this plan found and the review did
not: **`U+1680` OGHAM SPACE MARK** is category `Zs` but renders as a visible
stem segment in Ogham-aware fonts and as blank elsewhere. Its visibility is
**font-dependent** — precisely the property the "a `Zs` character is visible as
a space" argument needs to exclude.

Recorded honestly, because the plan corrected its own direction here: today's
code uses a bare `.split()`, which already splits on Unicode whitespace, so the
accepted ASCII-only design is the **behaviour change** on this axis and a `Zs`
split would have *preserved* today's behaviour. Chunk C carries that change in
the release notes. The known cost stands: a CJK byline separated by `U+3000`,
or a French one by `U+202F`, classifies `unknown` against an ASCII-space
roster. Both are legitimate spellings; the direction is safe (it over-flags, it
never grants).

### The fourth archive blocker, closed by measurement

The plan's *Lasting-truth migration* lists a third non-residual: **the unswept
`re.sub` normalization pattern** in `tools/lifecycle.py` and `scripts/`, which
"closes at plan time" if the plan reviewer returns a clean enumeration and
otherwise needs a durable home. Neither review returned one, so it was swept
here. Measured 2026-08-04:

| Site | Shape | Deletes? | Authority path? |
|---|---|---|---|
| `tools/lifecycle.py:270`, `:303` | `re.sub(r"[^A-Za-z0-9._-]", "-", raw)` | no — **replaces** with `-` | no (slug builder) |
| `scripts/link_check.py:175` | strips markdown link syntax | no | no |
| `scripts/link_check.py:176` | `re.sub(r'[^\w\s-]', '', s)` | **yes** | no (anchor slug) |
| `tools/_lifecycle_metrics/extract.py:340` | `re.sub(r'_', '-', ...)` | no | no |
| `tools/_lifecycle_metrics/parse.py:54` | drops a leading `(Round N)` | yes, deliberate | no |

**No bare-`re.sub` deleting shape sits on an identity or authority path outside
the one this plan fixes.** The single deleting instance that could have carried
the defect — `link_check.py:176` — uses `\w`, which is **Unicode-aware**:
measured, `Ünïcödé Ndër-Score` survives it unchanged, where the byline defect's
`[^a-z0-9]` reduced the same string to `ncdndrscore`. That is the whole
difference between the two shapes, and it is why this one is not the same bug.

**The enumeration is clean, so the item closes at plan time as specified** — no
`dev/PLANNING.md` row is owed.

### Archive status

With these three answered and the `re.sub` sweep closed, and `[I7b]` discharged
by `planner-line-semantics`'s Response retracting the claim it was owed, **this
plan's archive preconditions are met.**
