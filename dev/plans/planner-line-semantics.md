<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/lifecycle-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# Plan: the lifecycle tools read a line the way markdown does

**Source proposal**: `planner-line-semantics` (accepted 2026-08-03, conditioned
on the detection follow-up being opened, condition discharged; the Decision
commit is `f32d5e8`, with a status repair and a commit-hygiene record note at
`70d804c`). It currently sits at
[`dev/proposals/2026-08-03-claude-planner-line-semantics.md`](../proposals/2026-08-03-claude-planner-line-semantics.md)
and moves to `dev/proposals/archive/` when it archives.
**Status**: open
**Plan review**: required(**External**) — carried from the proposal header,
which argues the tier on the merits rather than by an `AGENTS.md` enumerated
trigger, and is **not** discharged by the External round the proposal already
had, nor by the Internal review being run on this plan. See *Plan review — the
brief, and why the tier is not discharged*. **No implementation commit lands
before a real `### Plan review -- <reviewer> -- YYYY-MM-DD` sub-heading is in
the tree.**
**Last update**: 2026-08-03
**Opened**: 2026-08-03

## Source proposal

`planner-line-semantics` settles one contract: **the tools that make structural
and authority claims about a human-authored markdown artifact must agree with
that artifact's other readers about what a line is.**

Python's `str.splitlines()` splits on ten characters. Markdown (CommonMark),
git, `grep`, `sed`, `wc` and Python's own `re.MULTILINE` split on two — CR and
LF, plus the CRLF pair. Five places in Cairn's two shipped lifecycle tools read
an artifact through `str.splitlines()` and turn the result into a claim: the
artifact's lifecycle state, its `Author` / `Plan review` fields, which `##
Review` / `## Decision` sections exist, whether a Decision's verbatim
authorization is present and visually isolated, and the status shown in the
session-start orientation survey. The consequence the proposal reproduced is
not a missed catch but a **manufactured one**: the planner printed
`structurally sound` for a terminal `accepted` state that exists in no other
reader's frame.

The accepted design is deliberately small: one nine-line module-private helper
per tool, five call sites rerouted, no new abstraction, no shared import, no
doctrine change, no new detector.

This plan executes that decision. It does not re-open it, and — per the
Decision's closing section — it does not carry forward the one claim the record
retracted.

### Glossary — every term glossed on first use

The audience is a scientist who codes, not a Unicode specialist.

* **Line separator, in the plural senses that matter here.** `str.splitlines()`
  treats ten characters as ending a line. CommonMark's *line ending* is a
  newline, a carriage return, or a carriage return + newline, and nothing else.
  The eight extras are `U+000B` VERTICAL TAB, `U+000C` FORM FEED,
  `U+001C`–`U+001E` (file / group / record separators), `U+0085` NEXT LINE,
  `U+2028` LINE SEPARATOR and `U+2029` PARAGRAPH SEPARATOR.
* **Carrier** — a file containing at least one of those eight extras. The
  tracked tree has none (measured below).
* **Frame-of-reference defect** — not a wrong computation, but a right
  computation in a frame no other reader shares. The bytes really are in the
  file; the tool's line grammar is what invents the heading.
* **Attestor vs. detector** — an attestor says *this structure is present*; a
  detector says *something suspicious is here*. This plan repairs the attestor
  and adds no detector. That split is load-bearing and is defended below.
* **Twin / twin parity** — Cairn self-hosts the apparatus it ships, so
  `tools/lifecycle_planner.py` and `templates/skills/_lib/lifecycle_planner.py`
  are byte-identical, as are `tools/lifecycle.py` and
  `templates/skills/_lib/lifecycle.py`. A suite node enforces both pairs.
* **Lockfile** — `dev/.cairn/cairn-lock.yml`, the machine record of every
  installed file and its hash. Cairn's own tree is recorded there, so an
  un-re-recorded edit makes Cairn report itself as diverged from its own
  install.
* **Orientation stream** — the output of `tools/lifecycle.py session-start`,
  printed into an agent's context window before any human instruction lands.

### Character convention, binding on this plan and on its tests

**No invisible character appears as a literal anywhere in this plan or in the
tests it specifies.** Every one is written `U+2028` in prose, `chr(0x2028)` in
code, and `\u2028` when it appears inside a measured result. This is the
proposal's own rule — *"Committing a carrier into the deliberation record would
be its own defect"* — and the notation convention the sibling records adopted
on 2026-08-03. A test fixture is **built at run time** from `chr()`; no fixture
file carrying a raw separator is committed.

## What the Decision retracted, and what this plan may not carry

**Read this before *Scope*.** The proposal's *Cross-lineage file collisions*,
Collision 2, predicted that under the byline classifier a `U+2028`-glued byline
would classify **`human`** while the plain first name classified `unknown`,
concluded that the classifier's own invariant (*dropping a character must never
widen authority*) was violated, and prescribed a correction *"one word wide"*.

The Decision records that prediction as **measured false** and retracts both
the invariant-violation claim and the prescription. This plan carries neither,
and **no chunk, test, or commit body opened from this plan may reintroduce
them.**

**Re-measured for this plan** — not carried forward from the Response —
against the landed `byline-classification` (`1dabe4d`) and the live roster
`dev/.cairn/agent-identities.json`, under the canonical interpreter
(`/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13), 2026-08-03:

```
roster (live)                        [('anthony', 'kendall')]

classify('Anthony')                  -> unknown
classify('Anthony\u2028Kendall')     -> unknown
classify('Anthony Kendall')          -> human
```

**The mechanism, so the result is understood rather than trusted.** The landed
`_fold_word` keeps a character when `ord(c) > 0x7F`, so `U+2028` *survives into
the comparison key* instead of being deleted out of it; and `_ASCII_WS_RE` is
`[ \t\n\r\f\v]+`, so `U+2028` is not a word separator either. The glued byline
therefore folds to a **single** word, `('anthony\u2028kendall',)`, which cannot
equal the two-word roster key `('anthony', 'kendall')`. There is no poison rule
to widen; the invariant is served by *keeping* the character, not by poisoning
it.

**The parse claim still holds exactly**, and is what this plan actually
changes. Measured against the tree as it stands and against a patched copy in a
scratch directory, on an artifact whose `## Decision` heading sits on a real
line with `chr(0x2028)` inside the byline:

```
HEAD  _parse_sections -> [('Review', 'Someone'), ('Decision', 'Anthony')]
PATCH _parse_sections -> [('Review', 'Someone'), ('Decision', 'Anthony\u2028Kendall')]
```

**What survives, stated positively.** This plan is **byline-neutral**: the two
sides classify identically before and after the patch, and they are now neutral
at `unknown` rather than at `human` — the safe direction. Nothing about the
byline surface has to land first, in either order, and **the plan owes the
byline classifier no correction.**

## The landing order binds, and this plan lands first

The Maintainer ruled on the landing order on 2026-08-03. The ruling is recorded
under *Maintainer ruling 2026-08-03* in
[`dev/plans/agent-context-scrub.md`](agent-context-scrub.md) and committed at
`1435f54`; its authorization is quoted verbatim there. Reproducing that record
rather than restating it, the ruling's own operative sentence reads:

> The recorded landing order stands: planner-line-semantics first, agent-context-scrub second.

That ruling binds this plan from the other side: `agent-context-scrub` is
released for execution planning but **its Chunk A must not land into a tree
where this plan has not landed in both twins.** This plan is the first of the
pair.

**Why the two are order-sensitive rather than merely adjacent.** They meet at
exactly one expression. Today, at `tools/lifecycle.py:519`, `_in_flight` builds
each survey line as

```python
f"{kind}/{path.name} -- {_status_of(path)}"
```

and `agent-context-scrub` A2 wraps both halves in its escaper, giving

```python
f"{kind}/{_safe_field(path.name)} -- {_safe_field(_status_of(path))}"
```

`_status_of` **selects** a value; `_safe_field` **renders it inert**. This plan
decides *which* string is selected; that plan decides how the selected string is
*rendered*. The two do not commute: escaping the file text upstream of the
split returns a right-looking survey while `tools/lifecycle_planner.py` — which
carries no escaper at all — goes on attesting a separator-forged `## Decision`
as structurally sound. Split first, then render inert, is the order the code
runs in.

**The coupling is symmetric and already written down on the other side.**
`agent-context-scrub`'s Chunk A acceptance criteria include a positive check
that `_status_of` uses this plan's CR/LF-only splitter and not
`str.splitlines()`, and its Chunk A does **not** add or modify `_status_of`.
Chunk B of this plan is therefore literally the precondition that plan's Chunk
A tests for. If an implementing agent finds the check failing, the order was
violated and that plan does not start — it is not that agent's call to
re-order.

## This change opens a window, and Chunk B is the chunk that opens it

**Landing this plan alone newly admits a raw `U+2028` into the orientation
stream.** The proposal did not say so; the Response measured it and listed it
undecided; the Decision recorded it explicitly as *not covered* by the accept,
and the Maintainer ruling cites it as the reason the ratified order is the safe
one. It is disclosed here, on this side, with its own chunk and its own
acceptance criterion, so that it is neither implicit nor inherited.

**Re-measured for this plan**, on a fixture whose status line is
`**Status**: prop<chr(0x2028)>osed -- the rest of the glued line`:

```
HEAD  _status_of  ->  'prop'
PATCH _status_of  ->  'prop\u2028osed -- the rest of the glued line'
```

and end-to-end through the producer the survey is built from, on a scratch tree
holding one benign and one carrier artifact:

```
HEAD  _in_flight ->
    'proposals/benign.md -- proposed'
    'proposals/carrier.md -- prop'
    raw U+2028 in the relayed stream: False

PATCH _in_flight ->
    'proposals/benign.md -- proposed'
    'proposals/carrier.md -- prop\u2028osed -- the rest of the glued line'
    raw U+2028 in the relayed stream: True
    2 survey lines, 1 real LF -- a splitlines()-based consumer counts 3
```

**What the window is, precisely.** `str.splitlines()` is, accidentally, a
sanitizer: today the separator is where the split *happens*, so the value
`_status_of` returns can never contain one. Narrowing the split removes that
accident on the status surface as well as on the byline surface. Between Chunk
B of this plan and Chunk A of `agent-context-scrub`, a carrier artifact's status
value is relayed into the orientation stream unescaped, where a consumer that
splits on the Unicode set — or a renderer that honours `U+2028` as a forced
break, which CSS Text does — sees more lines than the tool emitted.

**What bounds it.** It is reachable only through a carrier artifact, and the
tracked tree has **zero** carriers (493 tracked files that decode as UTF-8,
493/493 line-split-identical, 0 carriers, `as_of 2026-08-03`). "No real artifact
today" is nevertheless the argument this proposal declines to accept elsewhere,
so the window is given a chunk and a criterion rather than a footnote.

**What closes it.** `agent-context-scrub` Chunk A, whose escape table covers
`0x2028` and `0x2029`. Nothing in this plan can shorten the window; what this
plan can do is refuse to leave it undisclosed, and require the implementing
commit to say it is open. See Chunk B's acceptance criteria.

## The detection half is not this plan's, and no chunk may take it

The proposal's fourth *Signals the change is wrong* entry makes "someone reads
this fix as *the injection is handled*" a named failure mode with a named
recovery. It is not handled. After this plan lands, the forged artifact still
scans clean; what changes is that the planner stops attesting it.

**Detection is owned by `separator-detection`**
([`dev/proposals/2026-08-03-claude-separator-detection.md`](../proposals/2026-08-03-claude-separator-detection.md),
opened at `c40c959`), which the Decision names as the discharge of its
condition. That proposal claims one detector rule under a new pattern id and
nothing else.

**Two facts re-measured for this plan, so the delegation is not taken on
faith.**

1. **`content_scan` at HEAD clears the payload.** A fixture carrying a
   `chr(0x2028)`-glued `## Decision` heading, a `chr(0x2028)`-glued
   authorization blockquote and a `chr(0x2029)`-glued `**Status**: accepted`:

   ```
   $ python templates/modules/team-gated/content_scan.py <fixture>
   content_scan: OK -- 1 file(s) scanned; no flags.        (exit 0)
   ```

2. **`content-scan-detectors` cannot reach them, by construction rather than
   by oversight.** Its Change 1 adopts the RFC 8264 §9.13 set,
   `Default_Ignorable_Code_Point` union `Noncharacter_Code_Point`. Measured:

   ```
   U+2028  category=Zl  isspace=True  LINE SEPARATOR
   U+2029  category=Zp  isspace=True  PARAGRAPH SEPARATOR
   ```

   Both are `White_Space=Yes`, and the `Default_Ignorable_Code_Point`
   derivation **subtracts** `White_Space`; neither is a noncharacter. That
   proposal's own completeness invariant is additionally quantified over
   `Cf`-category code points, which excludes `Zl`/`Zp` a second way.

**Consequence for this plan:** no chunk adds a detector, no acceptance
criterion asks for one, and no commit body may describe this change as closing
the injection. The tripwire is satisfied by `separator-detection` existing and
in flight — not by anything in this plan.

## A premise of the proposal that has since been closed, recorded rather than glossed

The proposal argued, under *Context > Why this file, in particular*, that these
files are *"exactly the set `bootstrap/security_check.py` never scans"* and
that *"a defect here has no downstream catcher."*

**That is no longer true.** `scan-coverage` landed at `5c91c23` and binds the
release scan's target set to the published install manifest. Re-measured for
this plan:

```
$ python bootstrap/security_check.py
security_check: Bandit clean over 74 shipped file(s).
security_check: PASS -- release security gate clean.        (exit 0)

scan_targets() includes:
    templates/skills/_lib/lifecycle.py
    templates/skills/_lib/lifecycle_planner.py
```

Both twins are now inside the release Bandit gate. Recorded here because the
proposal's argument is load-bearing on the tier and a reviewer should not be
handed a stale premise. **It does not change the tier**: the proposal argues
`required(External)` on the *scope call* — fix the frame rather than add a
detector — and the scan-coverage gap was a supporting reason, not the stated
one. The tier is the proposal's declared trigger and stands as declared.

## Scope

Executes the accepted proposal's single change: one module-private helper per
tool, five call sites rerouted, in two twin pairs, plus four test nodes and two
lockfile hash re-records. Two implementation commits.

**In scope:**

* `tools/lifecycle_planner.py` and its byte-identical twin
  `templates/skills/_lib/lifecycle_planner.py` — the helper plus four call
  sites: `_parse_status`, `_parse_field`, `_parse_sections`,
  `_has_isolated_blockquote`.
* `tools/lifecycle.py` and its byte-identical twin
  `templates/skills/_lib/lifecycle.py` — the helper plus one call site,
  `_status_of`.
* `dev/.cairn/cairn-lock.yml` — the recorded hash on each of the two
  `verbatim: true` rows.
* `bootstrap/tests/test_lifecycle_contract.py` — three new nodes.
* `bootstrap/tests/test_lifecycle_cli.py` — one new node.
* `dev/PLANNING.md` — the plan-open row-move, and the deferred-follow-up rows
  named under *Lasting-truth migration*.

**Out of scope, fenced explicitly:**

* **Detection of the separators.** `separator-detection` owns it, in full, for
  the measured reasons above. This plan adds no rule, no warning, no flag.
* **`templates/modules/team-gated/content_scan.py` and its runner, and
  `scripts/check_cairn.py`'s two splits.** These are *detectors*, not
  attestors: narrowing their split changes reported line numbers and the
  line-scope of `cairn-accept` suppression markers, which is a security-gate
  contract on a Security-Review-triggering surface. The proposal fences them
  out by name; so does this plan.
* **`tools/lifecycle_planner.py:1176` and `tools/lifecycle_planner.py:1202`.**
  These split git and subprocess stdout, which is LF-emitted by construction.
  `splitlines()` is correct there and narrowing it buys nothing.
* **`tools/lifecycle.py:615`** — a `.gitignore` membership test feeding a
  **write** path (the gitignore repair). Not a lifecycle artifact, not an
  authority claim; pulling a write path in would widen the gate set. The
  proposal's named follow-up; it stays one.
* **The escaping of the relayed value.** `agent-context-scrub` owns
  `_safe_field` / `_safe_stream` and the `_in_flight` producer. This plan does
  not touch `_in_flight`, does not add an escaper, and does not pre-empt that
  plan's Chunk A.
* **The byline classifier.** `_identity_token`, `_fold_word`, `_flag_words`,
  `_grant_words`, `IdentityModel.classify`, both config loaders and the roster
  are `byline-classification`'s, landed at `1dabe4d`. Same module, disjoint
  functions, no shared line. This plan owes it no correction (see *What the
  Decision retracted*).
* **A shared line-splitting module imported by both tools.** Rejected in the
  proposal as a new abstraction across a boundary the planner's own module
  docstring deliberately keeps separate. The helper is duplicated on purpose.
* **`doctrine/lifecycle-contract.md`.** Unchanged, deliberately. The contract
  already places the current `Status:` and structural precondition presence on
  the machine-verifiable side; a new clause would restate what the code now
  enforces and would have to clear the doctrine-change rate-limit gate to do it.
* **Any `bootstrap/_scaffold/` change.** None. No AST attestation re-anchor and
  no engine Bandit obligation attaches to this plan — stated affirmatively
  because omitting it has drawn a blocking finding on a sibling lifecycle.
* **Any install-contract movement.** No manifest row added or removed, no
  lockfile *schema* field, no fidelity-manifest entry, no gate-manifest command.
  Exactly two recorded hash values change.
* **`CHANGELOG.md`.** One line is owed, and per the proposal it lands at the
  plan-archive or goodnight serialization point, **not** in an implementing
  commit (`AGENTS.md` > *Shared communication files*). It is therefore not a
  chunk.

**Sequencing invariant — and the one place it deliberately does not hold.**
Chunk A closes the false-attestation route and opens nothing: the planner's
output surfaces are `scan` and `next`, not the orientation stream, and its
output over the real corpus is byte-identical before and after (measured
below). **Chunk B is different, and this is the honest statement of it:** Chunk
B is strictly better than HEAD for the *checker* and, until
`agent-context-scrub` Chunk A follows, strictly worse than HEAD for the
*orientation stream* on the carrier path. That is the ratified order's known
cost, it is a Maintainer call already made, and a reviewer should check that it
is disclosed here rather than argued away.

### Documentation / doctrine surface

* **Descriptive layer, in-code** — the helper's comment block and docstring, in
  both tools. This is where the line grammar becomes *stated* rather than
  assumed, and it is the whole of the doc surface the proposal specifies.
* **Deliberation layer** — this plan, its plan review, its code review, the
  `dev/PLANNING.md` row-move that serializes plan-open, and the follow-up rows
  named under *Lasting-truth migration*.
* **Release-facing** — `CHANGELOG.md`, one line, at the serialization point,
  not in an implementing commit.
* **Governing layer — none.** No `AGENTS.md` change.
* **Doctrine layer — none.** `doctrine/lifecycle-contract.md` is deliberately
  unchanged; the doctrine-change rate-limit gate is therefore not engaged, and
  the proposal's *Doctrine-change rate-limit* block records the declined edit
  so the omission is deliberate rather than silent.
* **Entry layer — none.** No `SECURITY.md` bullet: this plan closes a false
  *presence* and discloses a transient window whose residual-risk home, if one
  is owed at all, is `agent-context-scrub` Chunk C, which claims that file.
  Two other in-flight records claim `SECURITY.md`; this plan claims none of it.
* **`docs/` — N/A.** There is no descriptive page for either tool
  (`grep -rln lifecycle_planner docs/` is empty, `as_of 2026-08-03`).
* **Install contract — unchanged.** The shipped twins' *content* changes; the
  set of installed files does not.

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
(`/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13) with
`PYTHONDONTWRITEBYTECODE=1`, at `79df5e5`, 2026-08-03. None is carried forward
from the proposal — three of its figures had already drifted by the time the
Decision landed.

* **Suite baseline: 1710 passed, 0 failed, 3 warnings, 147.7 s**, measured at
  `79df5e5` with a **clean tracked working tree**. The proposal's `1556` and
  its `1557 or more` floor are both stale; the floor survives as a floor but is
  152 nodes below the real baseline and must not be used as the acceptance
  number.
* **Re-measure the baseline at the tip you branch from — this one is known to
  be moving.** A concurrent lifecycle (`fork-advisory-semantics`) is editing
  `bootstrap/_scaffold/` in the working tree as this plan is written. With those
  edits present, `bootstrap/tests/test_ast_attest.py` reports **2 failed**
  (`CHANGED FunctionDef:format_forked_facade_warning ... NOT pure motion`) and
  an untracked `bootstrap/tests/test_fork_advisory.py` appears. Neither failure
  is this plan's, and neither is fixed by it; an implementing agent who takes
  `1710` on faith will mis-attribute them.
* **Collection only grows.** This plan adds four nodes, drops none, and adds no
  skip or xfail marker.
* **Frozen set: 166 entries**, `as_of 2026-08-03`. Verified individually rather
  than inferred from the count: `bootstrap/tests/test_lifecycle_contract.py`
  and `bootstrap/tests/test_lifecycle_cli.py` are **both frozen**; none of the
  four production files is.
* **A documented gate nothing fires.** `bootstrap/tests/_gate_manifest.py
  verify` is invoked by neither the pytest suite nor CI; it runs only inside the
  Maintainer's supervised re-anchor ceremony (`bootstrap/REANCHOR_RUNBOOK.md`).
  Run today it reports **six** pre-existing `FROZEN-MODIFIED` holds, two
  `COLLECTION-DROPPED` entries and four `SKIP-XFAIL-NEW` entries — none of them
  this plan's. Expect this plan's two test-module edits to add two more
  `FROZEN-MODIFIED` lines. **Do not treat that as a stop, and do not "fix" it by
  regenerating the manifest** — regeneration is a supervised, Maintainer-only
  trust-root step.
* **The release Bandit gate now covers both twins.**
  `python bootstrap/security_check.py` → `Bandit clean over 74 shipped file(s)`,
  `PASS`, exit 0, and `scan_targets()` contains both
  `templates/skills/_lib/lifecycle.py` and
  `templates/skills/_lib/lifecycle_planner.py`. This is a *live* channel for
  this plan, not a vacuous pass — unlike the situation the proposal described.
* **`python bootstrap/scaffold.py --manifest` emits 96 lines**, `as_of
  2026-08-03`. This plan adds and removes no row; the diff against the
  pre-change output is asserted **empty**.
* **`python bootstrap/verify_integrity.py --target .` is RED at HEAD**, and the
  assertion is therefore differential rather than absolute. It reports exactly
  two violations — `modified (hash mismatch): AGENTS.md` and
  `modified (hash mismatch): dev/modules/security-review.md` — plus one advisory
  `NOTE` about the forked `tools/lifecycle_metrics.py` facade. **None is this
  plan's**, and a sibling plan's claim that this check is green today has since
  drifted. Each chunk must leave the output with **no new line**; the recorded
  hash on the row it touched must move, and nothing else may.
* **The fork advisory cannot fire on either row.**
  `forked_facade_findings` requires a `verbatim` record with `hash != base_hash`
  **and** an installed `_<name>/` engine package under the target. No
  `_lifecycle` or `_lifecycle_planner` engine package exists under `tools/` —
  the only two that do are `tools/_intent/` and `tools/_lifecycle_metrics/` — so
  re-recording `hash` alone introduces no advisory. Checked by reading the
  committed predicate, not
  assumed — and re-check it, because `fork-advisory-semantics` is concurrently
  editing exactly that function.
* **`python scripts/check_cairn.py` is green**: `OK -- 181 Markdown file(s)
  scanned; no issues; 68 external link(s) not probed`.
* **`python scripts/quality_gate.py` is RED at HEAD for pre-existing reasons**,
  so this assertion is differential too: order-independence `fail=1`
  (`seed=0: pytest exit 1` — the same `test_ast_attest` drift above),
  neutrality `fail=95`, redundancy `fail=0 info=2`. **No flag names any of the
  four files this plan edits**, verified by inspection of the full output. The
  criterion is *no new flag naming a file in scope*, never "the gate is green".
* **`quality_gate`'s R6 unused-definition scan cannot see this helper.** Its
  roots are `scripts`, `bootstrap`, `templates/modules`; neither `tools/` nor
  `templates/skills/` is among them. Not load-bearing here — each chunk defines
  and uses the helper in the same commit — but stated so it is not discovered
  as a surprise.
* **The twin-parity gate exists and fires.** In
  `bootstrap/tests/test_notice_install.py`, the node
  `test_every_self_hosted_twin_stays_byte_identical_to_its_source` compares
  bytes on a pair list derived from the install manifest, so both pairs are in
  it. The three modules this plan touches or relies on
  (`test_lifecycle_contract.py`, `test_lifecycle_cli.py`,
  `test_notice_install.py`) run together as **63 passed in 3.68 s**.
* **The plan-review gate cannot be satisfied by a placeholder.** Measured
  directly against the shipped header regex in `tools/lifecycle_planner.py`:

  ```
  '## Plan review'                                              -> [('Plan review', 2)]
  '## Plan review — the brief, and why the tier is not discharged' -> []
  '## Code review'                                              -> [('Code review', 2)]
  '### Plan review -- Gemini Flash (External, security lens) -- 2026-08-03'
                                                                -> [('Plan review', 3)]
  ```

  A bare `## Plan review` heading registers as a landed review section, so an
  *empty* section would open the gate. The heading as written below is not
  parsed as a section at all — the em dash and comma break the kind group — so
  only a real `###` sub-heading registers. **Do not rename the heading to a
  bare `## Plan review`.** The same shaping, for the same measured reason, is
  applied to `## Code review`.

## Sequence

```
0. plan-open      -- this plan + the dev/PLANNING.md row-move          [commit pending]
   (plan review)  -- required(External); NO implementation commit before it lands
1. Chunk A -- the planner pair: four call sites, the false attestation [commit pending]
2. Chunk B -- the lifecycle.py pair: _status_of, and the window        [commit pending]
   (serialization) -- one CHANGELOG.md line at archive or goodnight    [not a chunk]
```

Two implementation chunks, split on the axis that actually matters: **Chunk A
opens no window and Chunk B does.** Bundling them would hide the one
intermediate state a reviewer needs to see named, and would make the commit
that closes the headline defect indistinguishable from the commit that incurs
the ratified cost.

### Chunk A — the planner pair, and the false attestation

The proposal's headline defect: `structurally sound` printed for a terminal
state that exists in no other reader's frame. One commit.

| # | File | Change |
|---|------|--------|
| A1 | `tools/lifecycle_planner.py` | Add `_LINE_ENDING_RE` and `_split_lines` immediately below the `# --- artifact parsing ---` banner (line 466), **above** `class Section`. Carry the proposal's comment block verbatim in substance: markdown / git / grep / `re.MULTILINE` agree on CR, LF and CRLF; `splitlines()` adds eight separators none of those readers treats as a break; a structural read built on it can attest a heading no human, no `grep -n '^## '` and no renderer sees. |
| A2 | `tools/lifecycle_planner.py` | Route four call sites through the helper: `_parse_status` (line 539), `_parse_field` (line 554), `_parse_sections` (line 563), `_has_isolated_blockquote` (line 606). Leave lines 1176 and 1202 alone — git / subprocess stdout. |
| A3 | `templates/skills/_lib/lifecycle_planner.py` | The identical A1 + A2 edit, **same commit**, or the twin-parity node fires. |
| A4 | `dev/.cairn/cairn-lock.yml` | Re-record the `hash` field on the `tools/lifecycle_planner.py` record to the new sha256. Hand-edit the one line, not `scaffold.py upgrade --target .`. Leave `base_hash` untouched — it already diverges (it records the upstream base) and `byline-classification` set exactly this precedent at `1dabe4d`. |
| A5 | [`bootstrap/tests/test_lifecycle_contract.py`](../../bootstrap/tests/test_lifecycle_contract.py) | **The forged-heading regression.** A `chr(0x2028)`-built fixture with a `## Decision` heading and an isolated `>` authorization glued onto an ordinary prose line, plus an earlier glued `**Status**: accepted`. Assert the planner reports the status a `^`-anchored reader finds, parses **no** Decision section, and emits no positive structural attestation for the fabricated terminal state. |
| A6 | [`bootstrap/tests/test_lifecycle_contract.py`](../../bootstrap/tests/test_lifecycle_contract.py) | **The equivalence property, synthetic.** `_split_lines(t) == t.splitlines()` over the twelve edge cases the proposal enumerates — `""`, `"a"`, `"a\n"`, `"a\n\n"`, `"\n"`, `"\r\n"`, `"a\r\nb"`, `"a\rb\r"`, `"a\r\n\r\nb\r\n"`, trailing-blank runs — **plus a positive control** that is a carrier and must be observed to *differ*. |
| A7 | [`bootstrap/tests/test_lifecycle_contract.py`](../../bootstrap/tests/test_lifecycle_contract.py) | **The equivalence property, over the real corpus.** The same assertion over every `.md` under `dev/`, so a future artifact that introduces a carrier fails loudly rather than silently. Walk the filesystem (`rglob`), **not** `git ls-files` — a git-dependent node adds to the nine-failure floor a `git archive` sandbox already carries. |

**Acceptance criteria — Chunk A**

* **Red-then-green, in that order.** Run A5–A7 against a byte-identical copy of
  the *pre-fix* files in a scratch directory outside the Cairn tree and capture
  the failures **before** A1–A3 are applied. The captured failure output goes in
  the commit body. A test written after the fix, never observed failing against
  the real historical defect, is a test whose discrimination is unmeasured.
* **A5's oracle is independent of the function under test.** The expected
  status and the expected section set are computed by a `^`-anchored read
  (`re.MULTILINE`, or `text.split("\n")`), **not** by calling `_split_lines`
  and **not** by calling the parser a second time. An oracle derived from the
  code under test cannot discriminate. Name the oracle in the test docstring.
* **A6's positive control is mandatory and is asserted to differ.** Measured
  for this plan: for `"a\nb" + chr(0x2028) + "c\n"`, `splitlines()` yields **3**
  and `_split_lines` yields **2**. A property test that only ever sees
  separator-free input cannot distinguish a correct helper from
  `return text.splitlines()`.
* **Byte-identical tool output over the real corpus** — the proposal's central
  zero-regression claim, re-measured for this plan against a patched scratch
  copy under the canonical interpreter, 2026-08-03:
  * `lifecycle_planner.py scan` — HEAD and patched both exit 1, stdout+stderr
    sha256 `991fd1a7…`, ending `6 of 21 artifact(s) carry structural
    violations`.
  * `lifecycle_planner.py next <each of the 21 tracked artifacts>` (15
    proposals + 6 plans, `_template.md` excluded) — sha256 `985e4f72…`, 254
    lines, identical.
  * **Re-measure both; do not compare against the proposal's hashes.** Its
    `f8cc147e…` / `1a1ee8d1…` / 283 lines / 27 artifacts were taken against a
    smaller corpus and no longer reproduce. The claim is *identity between HEAD
    and patched at the same commit*, never identity with a historical digest.
* **Placement is checked, not assumed — and the failure mode is measured.**
  Appending the helper at the **end** of the module leaves it unbound when the
  CLI runs: `if __name__ == "__main__": raise SystemExit(main())` executes while
  the module body is still running, so `main()` is called before any name below
  it is defined. Observed for this plan as a `NameError` traceback from
  `_read_artifact`. The helper goes above its first use.
* **Twin parity demonstrated, not assumed.** Edit `tools/lifecycle_planner.py`
  first, run `python -m pytest bootstrap/tests/test_notice_install.py -q`,
  observe the parity node **fail**, then apply A3 and observe it pass. The
  failure observation goes in the commit body.
* **`shasum -a 256 tools/lifecycle_planner.py
  templates/skills/_lib/lifecycle_planner.py`** — equal to each other and to
  the value re-recorded in A4.
* **`python bootstrap/verify_integrity.py --target .`** — output diffed against
  the pre-chunk run: observed to gain a `tools/lifecycle_planner.py` line
  between A2 and A4, and to return to the two pre-existing violations after A4.
  Both observations in the commit body; the mid-chunk change is the evidence
  that the check is live rather than decorative.
* **Perturbation ledger, in the commit body.** Each perturbation applied to a
  scratch copy, the named test observed to fail, the source restored
  byte-identical (confirmed with `git hash-object` against
  `git rev-parse HEAD:<path>`):
  * revert `_parse_sections` to `splitlines()` → **A5 fails**;
  * revert `_parse_status` to `splitlines()` → **A5 fails** on its status
    assertion;
  * replace the helper body with `return text.splitlines()` → **A6 fails on its
    positive control only**, which is precisely why the control is a
    requirement and not a suggestion;
  * drop the trailing-empty-element `pop()` → **A6 fails** on `"a\n"`.
* Full suite green under the canonical interpreter, **0 skipped / 0 xfailed**,
  collection grown by exactly the three new nodes from the baseline re-measured
  at the branch tip.

### Chunk B — `tools/lifecycle.py`, and the window it opens

The identical defect in the identical shape on the surface an adopter sees most
often — and the chunk that incurs the ratified order's known cost. One commit.

| # | File | Change |
|---|------|--------|
| B1 | `tools/lifecycle.py` | Add `_LINE_ENDING_RE` and `_split_lines` immediately below the `# --- in-flight thread survey ---` banner (line 488), **above** `_status_of`. **Deliberately not** in the `_PREFIX` / `_emit` block at lines 94–112: that is where `agent-context-scrub` A1 inserts `_safe_field` / `_safe_stream`, and keeping the two insertions in different regions of the file removes a textual merge collision that buys nothing. |
| B2 | `tools/lifecycle.py` | Route `_status_of` (line 494) through the helper. Leave line 615 alone — the `.gitignore` membership read, which feeds a write path and is a named follow-up. **No change to `_in_flight`** (line 505) and no escaper: that is `agent-context-scrub` A2's, and pre-empting it would reverse the ratified order inside one commit. |
| B3 | `templates/skills/_lib/lifecycle.py` | The identical B1 + B2 edit, **same commit**. |
| B4 | `dev/.cairn/cairn-lock.yml` | Re-record the `hash` field on the `tools/lifecycle.py` record. **Coordination note, not a free choice:** `agent-context-scrub` A4 specifies re-recording **both** `hash` and `base_hash` on this same row. Whichever plan lands second must not silently pick a different convention on one row. Settle it by measurement — take the `verify_integrity --target .` output before and after and choose the option that adds no line — and record which was chosen and why in the commit body. |
| B5 | [`bootstrap/tests/test_lifecycle_cli.py`](../../bootstrap/tests/test_lifecycle_cli.py) | **`_status_of` agrees with a `^`-anchored grep.** A `chr(0x2028)`-built fixture whose status line is glued mid-token; assert `_status_of` returns the value an independent `^`-anchored read finds, and assert the same through `_in_flight` on a two-artifact fixture so the survey's one-line-per-artifact shape is exercised, not just the helper. |

**Acceptance criteria — Chunk B**

* **The window is stated in the commit body, in the commit that opens it.** The
  body must record, in terms: this commit newly admits a raw `U+2028` into the
  orientation stream on the carrier path; it is closed by `agent-context-scrub`
  Chunk A; the tracked tree carries zero carriers today. Measured evidence to
  paste, re-taken at implementation rather than copied from here:

  ```
  HEAD  _status_of  ->  'prop'
  PATCH _status_of  ->  'prop\u2028osed -- the rest of the glued line'
  ```

* **The two changes should land in the same working session.** The Maintainer
  ruling ties them; if that is not possible, the commit body says so explicitly
  so the Maintainer knows they are holding an open window rather than
  discovering it.
* **Confirm the sibling can actually follow before landing this chunk.**
  `agent-context-scrub` does not start until its own `required(External,
  security lens)` plan review has landed. Check that it has. Landing Chunk B
  into a tree where the sibling is still review-blocked converts "a window
  measured in minutes" into "a window measured in days", and that is a
  materially different disclosure.
* **B5's oracle is independent**, on the same rule as A5: the expected value is
  computed by a `^`-anchored read, never by the function under test.
* **Red-then-green** against a pre-fix copy, captured before B1–B3, in the
  commit body.
* **Perturbation ledger, in the commit body:** revert `_status_of` to
  `splitlines()` → **B5 fails**; delete the helper's trailing-empty `pop()` →
  **A6 fails** (the shared property is pinned once, in Chunk A, and Chunk B's
  copy is the *same* nine lines — say so, and note that the planner-side node is
  what catches a divergent second copy).
* **The two helpers are byte-identical to each other**, and that is asserted by
  hand rather than by a test: the proposal duplicates them on purpose, and a
  drifting duplicate is the cost that decision accepts. Record the comparison in
  the commit body.
* **Twin parity demonstrated by perturbation**, `shasum` equality, and the
  `verify_integrity` before/after diff — all exactly as in Chunk A.
* Full suite green, **0 skipped / 0 xfailed**, collection grown by exactly one
  more node.

## Acceptance criteria

Per-chunk criteria are above. These are the plan-level deliverables.

* **Tests that must pass.**
  * `python -m pytest bootstrap/tests` — the whole suite, green, **0 skipped /
    0 xfailed**, under the canonical interpreter (3.13.13). Baseline **1710
    passed, 0 failed, `as_of 2026-08-03` at `79df5e5` on a clean tracked
    tree** — and **re-measured at the branch tip**, because a concurrent
    `bootstrap/_scaffold/` lifecycle is moving it. Collection grows by exactly
    four nodes and drops none. The proposal's "1557 or more" floor is
    superseded.
  * The three new nodes in
    [`bootstrap/tests/test_lifecycle_contract.py`](../../bootstrap/tests/test_lifecycle_contract.py)
    and the one in
    [`bootstrap/tests/test_lifecycle_cli.py`](../../bootstrap/tests/test_lifecycle_cli.py).
    Both modules importlib-load the **template** copy, so the shipped artifact
    is what gets tested.
  * The existing twin-parity node in
    [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py),
    demonstrated failing once per chunk before the twin is synced. **N/A** as a
    code change: no new node is added there; the existing gate already covers
    both pairs, which is the point of citing it.
  * **Every new test shown non-vacuous by perturbation**, plus the
    red-then-green run against a pre-fix copy. The ledgers go in the commit
    bodies.
* **Doc updates that must land.** Hand-authored only: the in-code comment block
  and docstring in both tools (Chunks A and B), and one
  `CHANGELOG.md > Unreleased > Fixed` line at the serialization point. **N/A**:
  no generated docs, no snippet-synced blocks, no `docs/` topic page, no
  `SECURITY.md` bullet, no doctrine edit.
* **Examples / smoke checks required.**
  * `python tools/lifecycle_planner.py scan` and
    `python tools/lifecycle_planner.py next <artifact>` over every tracked
    proposal and plan — output byte-identical to the pre-change run, compared by
    sha256 at the same commit.
  * `python bootstrap/verify_integrity.py --target .` — output diffed
    before/after each chunk; gains a line mid-chunk, returns to the two
    pre-existing violations after the lockfile re-record.
  * `python bootstrap/scaffold.py --manifest` — diffed against the pre-change
    output, **expected empty** (96 lines, `as_of 2026-08-03`).
  * `shasum -a 256` over both twin pairs — equal within each pair and equal to
    the re-recorded lockfile values.
  * `python bootstrap/security_check.py` — **run it, and expect it to mean
    something**: both twins are now in its 74-file target set.
  * A manual `python tools/lifecycle.py session-start` in a scratch repo
    carrying one benign and one carrier artifact, output pasted into the code
    review — the end-to-end proof that the survey stays one line per artifact
    and the disclosed evidence that the relayed value now carries the separator.
  * **Explicitly not required:** the AST attestation re-anchor. No
    `bootstrap/_scaffold/` file is touched.
  * **Example gallery — N/A**: `examples/` exercises neither lifecycle tool.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans and proposals by filename stem, not path
  link, so the archive-move needs no edit there. Confirm at archive time rather
  than assume.

### Author-accounting — invariants, failure modes, edge cases

**Invariants, each with the chunk that enforces it and the test that pins it.**

* *`_split_lines(t) == t.splitlines()` for every `t` free of the eight extra
  separators.* Chunks A1 and B1, pinned by A6 (synthetic edge cases plus a
  carrier positive control) and A7 (the real `dev/` corpus). Swept for this plan
  over the whole tracked tree: **493 files that decode as UTF-8, 493/493
  identical, 0 carriers**; `dev/` alone **113/113, 0 carriers**;
  `dev/proposals` + `dev/plans` including archives **53/53, 0 carriers**
  (`as_of 2026-08-03`). The sweep was run with a positive control that the same
  machinery correctly reports as differing, so a silently-broken sweep cannot
  produce this result.
* *The planner's structural state for an artifact matches what a `^`-anchored
  grep would find.* Chunk A2, pinned by A5. Reproduced for this plan on a
  forged fixture: the patched planner reports `proposed` and parses no Decision
  where HEAD parses `[('Decision', 'Anthony Kendall', isolated-blockquote=True)]`,
  while `grep -c '^## '` finds 1 and `grep -n '^## Decision'` exits 1 with no
  output.
* *`_status_of` reports the status a `^`-anchored reader finds.* Chunk B2,
  pinned by B5.
* *No real artifact's tool output changes.* Chunks A and B, pinned by the
  byte-identity smoke checks rather than by a test node — a corpus-wide digest
  comparison is not something a unit test can hold, and saying so is better
  than inventing a node that would pass on any output.
* *The twins stay byte-identical and the lockfile records what is on disk.*
  A3/A4 and B3/B4, pinned by the existing twin-parity node and by
  `verify_integrity --target .` read differentially.
* *The planner stays read-only.* Unchanged, already enforced by the existing
  no-write node in `bootstrap/tests/test_lifecycle_contract.py`. This plan adds
  no write path.
* *This plan is byline-neutral.* Structural: it changes which string reaches
  `IdentityModel.classify`, and both strings classify `unknown` against the
  landed classifier and the live roster. Measured above; **not** re-asserted as
  an invariant test, because the classifier is `byline-classification`'s
  contract and pinning it from here would duplicate its ownership.

**Public-path → test mapping.** The public entry points this plan touches are
`lifecycle_planner.py next <artifact>`, `lifecycle_planner.py scan`, and
`lifecycle.py session-start` (which reaches `_status_of` through `_in_flight`).
The first two are exercised through the module's public `_read_artifact` / CLI
path by A5, as the existing nodes in that module already do; the third by B5.
No public entry point is added; no signature changes; no CLI flag is added or
removed.

**Channel discipline — for each verification step, the channel each input
arrives by.** Enumerated rather than asserted, because an oracle the artifact
under test supplies is the failure this repository has repeated.

| Step | Input | Channel | Supplied by the artifact under verification? |
|------|-------|---------|-----|
| A5 expected status / section set | a `^`-anchored read of the fixture | the test's own `re.MULTILINE` computation | No |
| A5/B5 fixture | the forged artifact | built at run time from `chr(0x2028)` by the test | No — and it is never committed as a file |
| A6 oracle | `str.splitlines()` | Python standard library | No — the helper is compared against the stdlib it narrows, not against itself |
| A6 positive control | a carrier string | the test's own construction | No — this is what forbids `return text.splitlines()` passing |
| A7 corpus | every `.md` under `dev/` | the filesystem, walked with `rglob` | No — and deliberately not `git ls-files`, which fails in a `git archive` sandbox |
| Byte-identity smoke | two stdout+stderr digests | two subprocess runs at the same commit | No — the comparison is HEAD-vs-patched, never against a historical digest |
| Twin parity | both files' bytes | the filesystem, compared by a pre-existing node the manifest drives | No |
| Lockfile check | the recorded hash | `dev/.cairn/cairn-lock.yml`, a separate tracked artifact | No — which is why it changes when only one side is updated |

**Failure modes.**

* *A file whose only line endings are among the eight extras parses as one
  line.* **Open** (degrades), and **intentional**: that is what `grep`, git and
  markdown do with such a file, and agreeing with them is the whole change. No
  such file exists in the tracked tree.
* *A lone CR line ending.* **Closed** — the regex alternation puts `\r\n` first
  so CRLF never splits twice, and a bare CR splits, matching both CommonMark
  and `str.splitlines()`. Pinned by A6's `"a\rb\r"` and `"a\r\n\r\nb\r\n"`
  cases.
* *A raw `U+2028` in the orientation stream between Chunk B and
  `agent-context-scrub` Chunk A.* **Open, transient, and the ratified order's
  known cost.** Measured above; disclosed in Chunk B's commit body; closed by
  the sibling. This is the single most important row in this table.
* *A malformed or unreadable artifact.* Unchanged: `PlannerError` and the
  existing `except OSError` in `_status_of`. **Closed** and **open**
  respectively, exactly as today. Note that `_status_of` catches `OSError` only,
  so a non-UTF-8 artifact still aborts `session-start` — a pre-existing defect
  this plan neither introduces nor fixes, disclosed by `agent-context-scrub`
  Chunk C.
* *The two duplicated helpers drift apart.* **Open, by design.** The proposal
  declines a shared import; nothing mechanical compares the two copies. Chunk
  B's acceptance criteria require a by-hand comparison recorded in the commit
  body, which is a habit, not a gate.
* *Someone reads this fix as "the injection is handled".* **Open, and
  permanent until `separator-detection` lands.** The proposal's own tripwire;
  restated here so no chunk quietly re-solves it.

**Edge-case inventory.** Empty string → `[]` (matches `splitlines()`); single
line without trailing newline → one element; trailing newline → no phantom
empty element; multiple trailing newlines → the same count `splitlines()`
gives; CRLF-only file → handled; mixed CRLF/LF → handled; N≫1 (the 1276-line
planner, the 1370-line lifecycle tool, the 493-file tracked tree) → verified
identical. **Out of scope:** non-UTF-8 artifacts — both tools already read with
`encoding="utf-8"` and fail or replace exactly as they do today.

**Known omissions, stated rather than implied.**

1. **No test asserts what a *browser* does with `U+2028`.** CSS Text treats it
   as a forced line break, so a browser reader may see breaks a terminal does
   not. Every claim here is made about CommonMark structure and about
   line-oriented tools, both of which were measured. The External proposal
   reviewer flagged this as their one uncovered item and it stays uncovered.
2. **No end-to-end CLI fixture for the other six separators.** They are covered
   by the equivalence property, not by a fixture each.
3. **Nothing here tests detection**, deliberately. See *The detection half is
   not this plan's*.
4. **The byte-identity smoke checks are not tests.** They are commands a human
   runs and records; nothing in CI holds them. Two same-type executions of the
   same comparison are weak evidence, and the plan reviewer is the first party
   who can make the scope call independent.
5. **No node pins the two helpers as identical to each other.** Named in
   *Failure modes* as an accepted cost of the proposal's no-shared-import
   decision.

## Verification

The concrete commands the implementation must pass. Run every one under the
canonical interpreter (`/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python
3.13.13) with `PYTHONDONTWRITEBYTECODE=1`; a different Python minor silently
changes suite and AST results, and stray `__pycache__` in the tree is its own
small mess.

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
<!-- cairn:end verification-commands -->

**Plan-specific gates, added here because this change touches those surfaces.**

* **Self-host integrity** — `python bootstrap/verify_integrity.py --target .`,
  read **differentially** against the pre-chunk output, because it is red at
  HEAD for two pre-existing reasons that are not this plan's.
* **Twin parity** — `python -m pytest bootstrap/tests/test_notice_install.py -q`,
  observed **failing** with one twin edited and passing after the sync, once per
  chunk.
* **Byte parity by hand** — `shasum -a 256` over each pair, equal to each other
  and to the re-recorded lockfile value.
* **The install-contract assertion** — `python bootstrap/scaffold.py
  --manifest`, diffed against the pre-change output. **Expected empty.**
* **The release security gate** — `python bootstrap/security_check.py`. Unlike
  the situation the proposal described, this is now a live channel for these
  files, so a green here means something.
* **Tool-output identity** — `lifecycle_planner.py scan` and
  `lifecycle_planner.py next` over every tracked artifact, sha256-compared
  HEAD-vs-patched **at the same commit**.
* **The perturbation ledgers and the red-then-green capture** — per chunk, in
  the commit body: the perturbation, the observed test failure, and the
  byte-identical restore confirmed with `git hash-object`.

**Note on doc gates**: drift gates (broken references, stale renders,
snippets that diverged from their source) catch **drift**, not
**absence** of new doc updates. Confirm each doc named in Acceptance
was actually updated; the gates don't enforce that.

### Reproductions run for this plan

Every figure above was taken this session, at `79df5e5`, 2026-08-03, under the
canonical interpreter, against the Cairn tree read-only — the patched copies of
both tools live in a throwaway scratch directory and no source file was
modified to produce any of it. The load-bearing ones, collected:

| # | What | Result |
|---|------|--------|
| 1 | The separator set, swept over the full code-point range | 10 separators; the 8 extras are `0xb 0xc 0x1c 0x1d 0x1e 0x85 0x2028 0x2029` |
| 2 | `U+2028` / `U+2029` properties | `Zl` / `Zp`, `isspace()` True for both — which is why the ignorable-set proposal cannot reach them |
| 3 | The retraction (item 1 of the Decision's closing section) | `classify('Anthony')` → `unknown`; `classify('Anthony\u2028Kendall')` → `unknown`; `classify('Anthony Kendall')` → `human` |
| 4 | The parse claim that still holds | HEAD `[('Decision','Anthony')]` → PATCH `[('Decision','Anthony\u2028Kendall')]` |
| 5 | The false attestation, on a fully forged heading | HEAD parses a `## Decision` with an isolated blockquote; PATCH parses none; `grep -n '^## Decision'` exits 1 |
| 6 | The forged status | HEAD `_parse_status` → `accepted`; PATCH → `proposed` |
| 7 | The window (item 3) | HEAD `_status_of` → `'prop'`; PATCH → `'prop\u2028osed…'`; raw separator in the relayed survey: False → True |
| 8 | The internal contradiction inside `_read_artifact` | `splitlines()` sees the `Follow-ups migrated to:` line: **True**; `re.MULTILINE '^'` sees it: **False** |
| 9 | Corpus equivalence | 493/493 tracked files identical, 0 carriers; positive control differs 3-vs-2 |
| 10 | Tool-output identity | `scan` sha256 `991fd1a7…` both, exit 1 both; `next` over 21 artifacts sha256 `985e4f72…` both, 254 lines |
| 11 | `content_scan` over the forged fixture | `OK -- 1 file(s) scanned; no flags`, exit 0 |
| 12 | Suite baseline | 1710 passed, 0 failed, 147.7 s, clean tracked tree |
| 13 | Release scan coverage | `PASS`, Bandit clean over 74 files, both twins in `scan_targets()` |
| 14 | Heading-shaping of this plan's own review headings | bare `## Plan review` registers a section; the heading as written does not |

## Plan review — the brief, and why the tier is not discharged

*Required — External. Implementation does not start until a review has landed
under this heading.*

**The tier is the proposal's declared trigger, ratified at Decision, not a
judgement call made here.** The proposal argues it on the merits and names
exactly what it is buying: the mechanical half of this change — *is the
replacement equivalent* and *did you find every call site* — is machine-checkable
and this plan ships the checks. The load-bearing judgement is the **scope
call**: fix the frame (agree with markdown) rather than add a detector (flag the
separators). A fresh-session same-type reviewer shares the author's priors on
exactly that question, so an Internal read would very likely reach the same
answer for the same reasons — which is an echo, not independence.

**An Internal review is being run on this plan immediately. It does not
discharge this tier and must not be counted toward it.** Its value is
constructive: it can catch a wrong line number, a vacuous oracle, a missing
perturbation, a chunk boundary in the wrong place. It cannot supply independence
on the one judgement the proposal identified as needing it.

**Nor is the tier discharged by the External round the proposal already had.**
That round returned SHIP with one concern ([E1], lack of active detection),
which the author's Response dispositioned — and in dispositioning it found the
delegation *sound but unhomed*, which is what conditioned the Decision. The
proposal-stage reviewer read a design; this plan is where the design becomes
two commits, four test nodes with named oracles, a disclosed window, and a
landing-order coupling. None of that was in front of them.

**One supporting argument the proposal made has since been closed, and a
reviewer should be told rather than left to discover it.** The proposal's third
argument for the tier — that these files sit outside the release security
scan — no longer holds: `scan-coverage` landed at `5c91c23` and both twins are
now in `security_check.py`'s 74-file target set. The tier does not rest on that
argument, but a reviewer weighing how hard to press should know one leg of the
stool was removed.

**The three questions this review should aim at**, in descending weight:

1. **Is the scope call right — attestor, not detector?** This is the question
   the tier exists to buy. The plan repairs the frame and adds no detection, on
   the argument that a detector cannot repair an attestor and that the CR/LF
   split is not a security filter but the tool agreeing with markdown's own
   definition of a line. The counter-position is real and is stated in the
   proposal's own *Signals the change is wrong*: after this lands, the forged
   artifact still passes both checkers, so the record is **quieter** without
   being **safer** until `separator-detection` lands. Is landing a quieter
   record first the right sequencing, or does the attestor fix need its detector
   in the same window?
2. **Is the disclosed window acceptable, and is the chunk split the right way
   to hold it?** Chunk B knowingly opens a hole this plan cannot close. The plan
   argues the split is what makes the cost visible; a reviewer might argue the
   opposite — that a single commit which is never separately shipped is a
   smaller window than two. Attack the reasoning, and say whether the acceptance
   criterion (a disclosure in the commit body plus a check that the sibling's
   plan review has landed) is a control or a comment.
3. **Can the specified oracles fail?** For each of the four new nodes, name the
   future state in which it fails. The plan claims A6's positive control is what
   forbids `return text.splitlines()` passing, and that A5's `^`-anchored oracle
   is independent of the parser under test. Is there a degenerate implementation
   that satisfies all four nodes and is still wrong — for instance one that
   narrows the split but changes reported line numbers?

**A fourth, if the reviewer has appetite.** The proposal's *Evidence* item 11
audits 41 `splitlines()` call sites and triages 25 as out of scope with no
action proposed. That triage has never been checked by anyone but its author.

**The stopping rule.** A finding on this scope is one of two things. Either it
names a reader in the adopter's toolchain that treats one of the eight
separators as a line ending — in which case the tool is right, the *reader* has
the unusual frame, and the proposal's argument inverts — or it names a property
this plan never stated, in which case the specification was incomplete, the
property is added, and every step is re-swept against it.

> **The landed review appends here as a `### Plan review -- <reviewer> --
> YYYY-MM-DD` sub-heading** (plus a `### Sharpening` sub-heading if it raised
> findings). **Do not rename this heading to a bare `## Plan review`.** Measured
> for this plan against the shipped header regex: the bare form registers as a
> landed review section, so an empty placeholder would open the gate; the
> heading as written is not parsed as a section at all.

## Code review — the brief (no review has landed)

*Filled in after implementation commits land.* Per `doctrine/plans.md`, the
reviewer is **not** the implementing agent, the section is append-only, and a
clean final review carries a falsification ledger and a coverage line. The
landed review appends here as a `### Code review -- <reviewer> -- YYYY-MM-DD`
sub-heading, beginning with a `**Model**:` line stating the reviewer's actual
running model identity rather than one copied from a past template. The heading
above is shaped like the plan-review one and for the same measured reason.

Four checks this plan asks its code reviewer to **run** rather than read:

* **Re-take the byte-identity comparison independently.** Run `scan` and `next`
  over the whole tracked corpus against the landed code and against the parent
  commit, and compare digests yourself. This is the plan's central
  zero-regression claim and it is not held by any test.
* **Re-run one perturbation from each chunk's ledger**, chosen by the reviewer
  and not by the implementer, and confirm the byte-identical restore with
  `git hash-object` against `git rev-parse HEAD:<path>`.
* **Confirm the window disclosure is in Chunk B's commit body**, in terms, and
  confirm whether `agent-context-scrub` Chunk A followed in the same session. If
  it did not, that is a finding about the record, not about the code.
* **Confirm no detector was added anywhere** — no new warning, no new flag, no
  new pattern id. The scope fence on detection is the one this plan is most
  likely to be quietly widened at.

## Lasting-truth migration

*Filled in at archive time.* Per `doctrine/plans.md`, the archive commit body
carries the literal `Follow-ups migrated to:` block naming where each deferred
item went, so the migration is auditable from the commit log alone — and the
plan does not archive until every deferred follow-up has a durable home outside
it.

The homes are pre-declared here so archive time is bookkeeping rather than
recall:

* **Detection of `U+2028` / `U+2029`** → `separator-detection`, already open at
  `c40c959`. This is the discharge of the Decision's condition; if that proposal
  is rejected or superseded without a successor, this plan's fourth *Signals the
  change is wrong* tripwire is unsatisfied and that fact needs a
  `dev/PLANNING.md` row rather than silence.
* **`tools/lifecycle.py:615`, the `.gitignore` membership read** → a
  `dev/PLANNING.md` row, to be bundled with any future change to the
  gitignore-repair path. Not claimed by any in-flight proposal today.
* **The 25 class-D `splitlines()` call sites** in `scripts/_onboarding/`,
  `tools/_intent/`, `tools/_lifecycle_metrics/` and `tools/evolution_infer.py`
  — audited and triaged in the proposal's evidence item 11, no action proposed
  → a `dev/PLANNING.md` row recording that the triage exists, so a future reader
  does not re-derive it. The archived proposal is not a durable home for it.
* **The two duplicated helpers, and the absence of anything comparing them** →
  a `dev/PLANNING.md` row. The proposal's no-shared-import decision is
  deliberate; the drift risk it accepts is not currently written anywhere
  outside this plan.
* **The proposal's superseded premise about the release security scan** → no
  row needed: it is recorded here and the closing change (`scan-coverage`,
  `5c91c23`) is itself in the record. Named so the omission is deliberate.

Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside the
plan.

This section is append-only once written.

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-03

**Model**: Claude Opus 5 (`claude-opus-5`), fresh session, canonical interpreter
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), working tree at
`eacb7dd` (the plan's own figures were taken at `79df5e5`, four commits back).

**Standing, stated honestly.** I am the **same agent type as this plan's author**
and I carry **no cross-type independence**. The threat model I bring is the
author's threat model; a blind spot the author has, I very probably share --
including on the one question the plan itself says the tier exists to buy
(*attestor, not detector*). The declared tier is `required(**External**)` and
**this review does not discharge it, must not be counted toward it, and does not
license an implementation commit.** Read what follows as a second pass that can
*execute and measure*, not as the adversarial read the tier asks for. Everything
below was re-run against the working tree; nothing is carried forward from the
plan, the proposal, or the author's cover note. All patched copies live in a
throwaway scratch directory; **no source file in this tree was modified.**

### Steelman

This is the strongest plan I have read in this repository, and its strength is
not rhetorical -- it is that almost every load-bearing number in it *reproduces*.
I independently rebuilt the patch from the proposal's helper, and:

* The **retraction is honest and correct.** The `U+2028`-glued byline classifies
  `unknown`, not `human`, and the mechanism the plan gives (`_fold_word` keeps
  `ord(c) > 0x7F`; `_ASCII_WS_RE` is `[ \t\n\r\f\v]+`; the glued name folds to a
  one-word key that cannot equal a two-word roster key) is exactly what the code
  does. A plan that carried a retracted claim forward would have been the easiest
  failure available here, and this one instead states the retraction *before*
  Scope and forbids any chunk from reintroducing it.
* The **window is real, measured, and disclosed rather than argued away.** I
  reproduced it end-to-end: raw separator in the relayed survey goes **False ->
  True**, and a `splitlines()`-based consumer counts **3** lines where the tool
  emitted **2**. Giving that its own chunk, its own acceptance criterion and its
  own *Failure modes* row -- rather than a footnote -- is the right call, and the
  plan is correct that bundling A and B would hide the one intermediate state a
  reviewer needs named.
* The **call-site enumeration is exhaustive.** `git grep -n "splitlines()"` over
  both files returns exactly eight occurrences: the four routed in A2 (539, 554,
  563, 606), the two fenced out in the planner (1176, 1202 -- git/subprocess
  stdout), the one routed in B2 (494), and the one fenced out in `lifecycle.py`
  (615, the gitignore membership read feeding a write path). Nothing is missed
  and nothing is over-claimed.
* The **central zero-regression claim holds** when re-measured independently.
* Every cited **commit hash resolves** (`f32d5e8`, `70d804c`, `1dabe4d`,
  `1435f54`, `c40c959`, `5c91c23`, `79df5e5`), every cited **line number is
  right** at the working tree, and the +142 drift the proposal's own citations
  carried has been corrected rather than inherited.
* The **scope fences hold.** I read the sibling records: the plan does not
  re-solve `separator-detection`'s scope and does not absorb
  `agent-context-scrub`'s. Its characterisation of that plan's A2, A4 and its
  Chunk-A precondition is accurate to the word (including that the precondition
  is "a positive check, not a comment").

The findings below are about *specified controls that do not control what they
are claimed to control*. They do not touch the design.

### Concerns

**[I1] The review-before-implement gate is presence-only and tier-blind -- and
*this* Internal review trips it. Gate-accounting #14 draws the wrong conclusion
from a correct measurement.** *(highest weight; security-relevant, and it is a
finding about a control this plan leans on rather than about the code)*

The plan's headline procedural safeguard is stated in its own header: *"**No
implementation commit lands before a real `### Plan review -- <reviewer> --
YYYY-MM-DD` sub-heading is in the tree.**"* Gate accounting #14 measures the
header regex, observes that a bare `## Plan review` registers as a section, and
concludes that shaping the brief heading with an em dash is what stops "an
*empty* section" opening the gate.

Measured against the shipped planner (`tools/lifecycle_planner.py:860`, the
`executing` gate is `_has_kind(art, "Plan review")`):

```
as written (no review section)                   plan_review='required(**External**) —'  _has_kind('Plan review')=False
+ '## Plan review -- Claude (Internal, ...)'     plan_review='required(**External**) —'  _has_kind('Plan review')=True
+ '### Plan review -- Claude (Internal, ...)'    plan_review='required(**External**) —'  _has_kind('Plan review')=True
+ an EMPTY '## Plan review' heading              plan_review='required(**External**) —'  _has_kind('Plan review')=True
```

Three consequences, none of which the plan states:

1. **Heading level is immaterial.** `###` and `##` register identically. The
   `###` prescription buys nothing mechanically.
2. **The `###` shaping does not stop a placeholder.** An *empty* `### Plan review
   -- X -- 2026-08-03` opens the gate exactly as an empty `## Plan review` does.
   What the em-dash shaping actually buys is narrower and worth stating
   correctly: it stops the plan's **own brief heading** from self-satisfying the
   gate. That is a real property; it is not the property #14 claims.
3. **The tier is invisible to the tool.** Nothing in the planner reads the word
   inside `required(External)`, the reviewer identity, or the `(Internal…)`
   label -- `requires_review` is just `plan_review.lower().startswith("required")`.
   So **the moment this section lands, the only mechanical review-before-implement
   check in the repository reports satisfied** -- satisfied by the review the plan
   itself says must not be counted toward the tier.

The plan's `required(External)` discipline is therefore held entirely by prose
and by the Maintainer's attention, with a machine check that will actively say
*"[ok]"* in the wrong direction. **Fix (plan-side, cheap):** state in the header
that the gate is presence-only and tier-blind, that this Internal section
satisfies it, and that the External round is the *only* thing that discharges the
tier -- so an implementing agent who runs `lifecycle_planner.py next` and sees the
gate green does not read that as authorization. Whether the *tool* should read
the tier is a separate finding against `lifecycle_planner.py` and is **out of
this plan's scope** -- it belongs in a `dev/PLANNING.md` row, not in a chunk here.

**[I2] "No flag names any of the four files this plan edits" is false as
measured -- and the helper insertion shifts five of the seven pre-existing flags,
which makes the differential criterion unevaluable as written.**

*Gate accounting* asserts, of `scripts/quality_gate.py`: *"**No flag names any of
the four files this plan edits**, verified by inspection of the full output."*
The `fail=95` figure reproduces exactly. The claim does not:

```
$ python scripts/quality_gate.py --sub neutrality   # fail=95  info=21
  FAIL  templates/skills/_lib/lifecycle.py:76:   unsanctioned vendor/project token `Claude`
  FAIL  templates/skills/_lib/lifecycle.py:526:  unsanctioned vendor/project token `Claude`
  FAIL  templates/skills/_lib/lifecycle.py:729:  unsanctioned vendor/project token `Claude`
  FAIL  templates/skills/_lib/lifecycle.py:745:  unsanctioned vendor/project token `Codex`
  FAIL  templates/skills/_lib/lifecycle.py:1193: unsanctioned vendor/project token `Claude`
  FAIL  templates/skills/_lib/lifecycle_planner.py:186: unsanctioned vendor/project token `Codex`
  FAIL  templates/skills/_lib/lifecycle_planner.py:505: unsanctioned vendor/project token `Antigravity`
```

Seven pre-existing FAIL lines naming **two of the four files in scope**. Both
`tools/` twins are outside the neutrality corpus (`cairn/templates/` only), which
is presumably how the inspection missed them.

The second half is worse than the first. The plan's derived criterion is *"no new
flag naming a file in scope"*. The helper insertion adds **19 lines** at planner
line 466 and at `lifecycle.py` line 488, so:

```
lifecycle_planner.py:  186 -> 186 (above the insert),  505 -> 522
lifecycle.py:           76 ->  76 (above the insert),  526 -> 543,
                                    729 -> 746, 745 -> 762, 1193 -> 1210
```

A naive before/after diff of the gate output then shows **5 removed + 5 added
FAIL lines, every one of them naming a file in scope** -- indistinguishable from
five new flags. **Fix:** record the seven-line pre-existing set in the plan, and
specify the comparison as a multiset over `(file, token)` pairs with line numbers
stripped, not a textual diff.

**[I3] The window opens on two surfaces, not one. `session-end` relays the same
value, and Chunk B's mandated disclosure names only the orientation stream.**

The glossary defines the orientation stream as *"the output of `tools/lifecycle.py
session-start`"*, the *Failure modes* row is scoped to it, and Chunk B's
acceptance criterion requires the commit body to record *"this commit newly
admits a raw `U+2028` into the orientation stream"*. But `_in_flight` has **two**
consumers:

```
tools/lifecycle.py:783   cmd_session_start      -> "in-flight threads (open proposals / plans)"
tools/lifecycle.py:1180  _do_thread_survey      -> "open threads to note in your reflection"
```

and `_do_thread_survey` is called at `cmd_session_end:1206`, **before** the
`--handoff` branch -- i.e. it runs in *both* goodnight modes, including the
reflection-only default that the docstring calls "the portable Layer-2
guarantee". The carrier's status value is relayed verbatim into the goodnight
survey too.

This does not change closure -- `agent-context-scrub` A2 escapes inside the
*producer*, so both consumers are covered -- and it does not change the risk much.
It changes the **disclosure**, which is the thing Chunk B's acceptance criterion
makes mandatory *"in terms"*. A disclosure that names one of two reachable
surfaces is an incomplete disclosure, and this plan's whole posture is that the
window gets named rather than inherited. **Fix:** name both consumers in the
*Failure modes* row and in the B-commit-body requirement.

**[I4] B4's tie-break specifies a measurement with no discriminating power. The
surface that actually discriminates is `upgrade`, not `verify`.**

B4 says the `hash`-only vs `hash`+`base_hash` conflict with `agent-context-scrub`
A4 should be *"settle[d] by measurement -- take the `verify_integrity --target .`
output before and after and choose the option that adds no line"*. Measured, with
the `tools/lifecycle.py` row mutated three ways:

```
baseline (hash == base_hash)         fork-advisory findings -> ['tools/intent.py', 'tools/lifecycle_metrics.py']
B4 Option 1: hash only               fork-advisory findings -> ['tools/intent.py', 'tools/lifecycle_metrics.py']
B4 Option 2: hash AND base_hash      fork-advisory findings -> ['tools/intent.py', 'tools/lifecycle_metrics.py']
```

`tools/lifecycle.py` never appears under any option -- which **confirms** the
plan's "the fork advisory cannot fire on either row" claim (no `_lifecycle`
engine package exists under `tools/` -- the only two that do are
`tools/_intent/` and `tools/_lifecycle_metrics/`), and I re-confirmed the
`hash != base_hash` +
engine-dir gating survives intact in the in-flight `fork-advisory-semantics`
rewrite of `forked_facade_findings`. And `grep base_hash bootstrap/verify_integrity.py`
is **empty** -- the verifier compares on-disk bytes against `hash` alone.

So **both options add no line, and the prescribed arbiter cannot tell them
apart.** The criterion will be recorded as "settled by measurement" when it was
settled by coin-flip.

The surface that *does* discriminate is `bootstrap/_scaffold/upgrade.py:325`,
`classify_verbatim(ours_bytes, rec["base_hash"] or rec["hash"], theirs)`:

```
classify_verbatim(ours=new, base=OLD  (Option 1), theirs=upstream+1) -> locally-modified
classify_verbatim(ours=new, base=NEW  (Option 2), theirs=upstream+1) -> update
```

That is a materially different upgrade classification for Cairn's own self-hosted
tree, and it is invisible to `verify_integrity`. **Fix:** re-point the criterion
at `classify_verbatim` / an `upgrade --dry-run`, or -- better, since the two plans
must agree anyway -- decide it here on the merits and say which, rather than
delegating to a measurement that cannot answer. (For the record, the A4 precedent
claim *is* accurate: `1dabe4d`'s only lockfile hunk is a one-line `hash` change on
the planner row, `base_hash` untouched.)

**[I5] A7 has no perturbation that reddens it, and the perturbation ledger has no
entry for it. It is a corpus canary, not a helper test -- and the plan bills it as
pinning an invariant it cannot pin.**

*Author-accounting* lists A7 as pinning `_split_lines(t) == t.splitlines()` for
separator-free `t`. Measured over the corpus A7 walks:

```
dev/**/*.md (rglob):  108/108 identical, 0 carriers
degenerate helper (`return text.splitlines()`) over the same 108 files:
   files where it disagrees with splitlines(): 0   -> A7 stays GREEN
```

A7 cannot distinguish the correct helper from `return text.splitlines()`; A6's
positive control is the *only* node that can, and the plan says so itself in A6's
criterion. Consistently, the Chunk-A ledger lists four perturbations and **none
of them names A7** -- so by the plan's own standard (*"Every new test shown
non-vacuous by perturbation"*), A7 is the one new node that has no falsifier.

I am **not** saying drop it: as a *canary* it is valuable, because its only red
trigger is a carrier landing in `dev/` -- which is precisely the payload this
change defends against, and turning that into a red suite is a good trade. But
two things should be said out loud, in A7's docstring and in *Known omissions*:
(a) A7 asserts a property of the **corpus**, not of the helper, and no source
perturbation reddens it; (b) A7 converts the plan's prose *Character convention*
("no invisible character appears as a literal") into a **hard suite gate over an
agent-written directory** -- a future proposal that legitimately commits a raw
`U+2028` as a demonstration payload turns the whole suite red, and that
consequence should be a chosen policy rather than a side effect.

**[I6] A5's discriminating power depends on a fixture-ordering detail the plan
does not state; built the other way, half of A5 is vacuous.**

A5 specifies *"an earlier glued `**Status**: accepted`"*. `_parse_status` returns
the **first** match in its scan window, so the placement relative to the *real*
status line is what decides whether the assertion can fail. Measured, same
payload, two placements:

```
glued 'accepted' placed AFTER the real '**Status**: proposed' line:
    HEAD  _parse_status -> 'proposed'      PATCH -> 'proposed'     (A5's status half CANNOT fail)
glued 'accepted' placed BEFORE the real line:
    HEAD  _parse_status -> 'accepted'      PATCH -> 'proposed'     (A5's status half discriminates)
```

The ledger entry *"revert `_parse_status` to `splitlines()` -> A5 fails on its
status assertion"* is the control that would catch a mis-built fixture -- so this
is a spec-precision finding, not a hole. **Fix:** say "earlier **than the real
`**Status**` line**". The section half is robust either way; with the glued
heading in place I reproduced HEAD attesting a full Decision and PATCH agreeing
with grep:

```
HEAD  _parse_status  -> 'accepted'
HEAD  _parse_sections -> [('Decision', 'Anthony', line_no=11, isolated_bq=True)]
PATCH _parse_status  -> 'proposed'
PATCH _parse_sections -> []
oracle re.MULTILINE '^## '  -> ['## Context']
grep -n '^## Decision' exit: 1      grep -c '^## ': 1
grep -n '^\*\*Status\*\*:' : 4:**Status**: proposed
```

**[I7] The `[:60]` / `[:40]` prefix windows reach a different amount of text after
the change -- a second behaviour delta on carriers that the edge-case inventory
omits.**

`_parse_status` / `_parse_field` scan `[:60]` and `_status_of` scans `[:40]` of
the split result. Narrowing the split does not only change *which* lines are
lines; on a carrier it changes *how far into the file the prefix scan reaches*.
Measured on a fixture with 30 `U+2028`-glued prose lines ahead of the real status
line (markdown line 31, `splitlines()` line 61):

```
HEAD  _parse_status -> ''          (the [:60] window truncated the real status line away)
PATCH _parse_status -> 'accepted'
```

Direction is safe (the patched read agrees with markdown, and HEAD's silent
"no status" is the worse answer), and it is unreachable on the real corpus at 0
carriers. But *Edge-case inventory* enumerates nine cases and none of them is
this one, and "the prefix window now covers more of the file" is a distinct claim
from "the split is narrower". **Fix:** one row in the inventory.

**[I8] Three gate-accounting figures have drifted, one of them into a wrong
expectation an implementer would act on.**

* **`_gate_manifest.py verify`** -- the plan says *"six pre-existing
  `FROZEN-MODIFIED` holds, two `COLLECTION-DROPPED` and four `SKIP-XFAIL-NEW`"*.
  Measured now: **HOLD -- 15 violations: 9 FROZEN-MODIFIED / 2 / 4** (the three
  extra are `bootstrap/verify_integrity.py`, `bootstrap/tests/test_lockfile_module.py`,
  `bootstrap/tests/test_verify_integrity.py` -- the in-flight `fork-advisory-semantics`
  working-tree edits, correctly *not* this plan's).
  **The actionable part:** `bootstrap/tests/test_lifecycle_contract.py` is
  **already** on the FROZEN-MODIFIED list, from committed drift, not from the
  working tree. So this plan's two test-module edits add **one** new line
  (`test_lifecycle_cli.py`), not the *"two more"* the plan tells the implementer
  to expect. An implementer who sees one will either doubt their edit or go
  looking for the missing one.
* **`verify_integrity --target .`** -- the plan says two violations *"plus one
  advisory `NOTE` about the forked `tools/lifecycle_metrics.py` facade"*. Run
  against the **HEAD** engine it emits **two** NOTEs (`tools/intent.py` **and**
  `tools/lifecycle_metrics.py`); run against the **current working tree** engine
  it emits **zero** (the fork-advisory rewrite now requires a caller-supplied
  trusted upstream, and the CLI passes none). Since the plan makes this check
  *differential*, an implementer needs to know the baseline moves with which
  engine is on disk -- which is a sharper statement than "re-measure at the branch
  tip".
* **Corpus / tool-output figures** -- all moved, all inside the plan's own `as_of`
  and its explicit "re-measure, do not compare against historical digests"
  instruction, so this is bookkeeping rather than error: tracked files **493 ->
  494**; `dev/**` **113 -> 114**; `dev/proposals`+`dev/plans` **53 -> 53**
  (unchanged); live artifacts **21 -> 25**; `scan` digest `991fd1a7… ->
  88dda344…`; `next` `985e4f72…/254 lines -> c0a8ae35…/220 lines`. The
  *load-bearing* claim -- HEAD output == patched output -- reproduces exactly (below).
  Worth noting how fast this moved: the plan is under a day old.

**[I9] The author's cover note misstates the working tree.** The plan's *body*
gets this right (*"A concurrent lifecycle (`fork-advisory-semantics`) is editing
`bootstrap/_scaffold/` in the working tree as this plan is written"*), but the
accompanying report that *"`git status` shows only the new plan added under
`dev/`"* is not what the tree shows. Snapshot at the start of this review
(`as_of 2026-08-03`; it grew further during it, to ten modified tracked files
and a dozen untracked `dev/plans/` drafts): **eight tracked files were modified**
(`bootstrap/UPGRADE.md`, `bootstrap/_scaffold/{SECURITY_MUTATIONS.md,install.py,lockfile.py,upgrade.py}`,
`bootstrap/{verify_integrity.py}`, `bootstrap/tests/{test_lockfile_module.py,test_verify_integrity.py}`),
plus untracked `bootstrap/tests/test_fork_advisory.py`. None is this plan's, and
the plan does not touch them -- but "no source file touched" and "the tree is
clean" are different statements, and the second one is what an implementer would
branch from. I confirmed the plan itself modified nothing: both twin pairs are
byte-identical and unmodified, and no file in scope appears in `git status`.

### Covered

Everything here was run this session at `eacb7dd` under Python 3.13.13 with
`PYTHONDONTWRITEBYTECODE=1`, against scratch copies of the two tools that I
rebuilt from the proposal's helper. Output is as emitted.

**1. The retraction -- re-measured, and it holds.** The plan does **not** claim a
`U+2028`-glued byline classifies `human`, and the correct claim reproduces:

```
roster (live)                        [('anthony', 'kendall')]
classify('Anthony')                  -> unknown
classify('Anthony\u2028Kendall')     -> unknown
classify('Anthony Kendall')          -> human

_grant_words('Anthony'+SEP+'Kendall') = ('anthony\u2028kendall',)     <- one word, not two
_ASCII_WS_RE.pattern                  = '[ \t\n\r\f\v]+'
NFKD(U+2028) == U+2028 : True    NFD : True    casefold : True
_fold_word(U+2028)                    = '\u2028'                      <- kept, ord > 0x7F
```

Mechanism confirmed independently of the plan's telling: the separator survives
normalization, case-folding and the fold filter, and is not a word separator, so
the glued byline folds to a **single** word that cannot equal the two-word roster
key. There is no poison rule to widen. The plan's framing -- the invariant is
served by *keeping* the character -- is right.

**2. The parse claim still holds exactly** (glued byline, real `## Decision` line):

```
HEAD  _parse_sections -> [('Review', 'Someone'), ('Decision', 'Anthony')]
PATCH _parse_sections -> [('Review', 'Someone'), ('Decision', 'Anthony\u2028Kendall')]
```

Both sides classify `unknown`, so the plan's **byline-neutral** claim is
confirmed, and it is neutral at the safe end.

**3. The orientation-stream window -- established, not refuted.** Fixture
`**Status**: prop<chr(0x2028)>osed -- the rest of the glued line`:

```
HEAD  _status_of  ->  'prop'
PATCH _status_of  ->  'prop\u2028osed -- the rest of the glued line'

HEAD  _in_flight ->
    'proposals/benign.md -- proposed'
    'proposals/carrier.md -- prop'
    raw U+2028 in the relayed stream: False
    2 survey lines, 1 real LF -- a splitlines() consumer counts 2

PATCH _in_flight ->
    'proposals/benign.md -- proposed'
    'proposals/carrier.md -- prop\u2028osed -- the rest of the glued line'
    raw U+2028 in the relayed stream: True
    2 survey lines, 1 real LF -- a splitlines() consumer counts 3
```

Reproduces the plan digit for digit. See **[I3]** for the surface count.

**4. Every cited line number and quoted fragment, checked against the working
tree.** All correct; the proposal's +142 drift is corrected, not inherited.

```
tools/lifecycle_planner.py   466 '# --- artifact parsing ---'   469 class Section
                             539 _parse_status   554 _parse_field
                             563 _parse_sections 606 _has_isolated_blockquote
                             1176 / 1202  git & subprocess stdout  (fenced out -- correct)
tools/lifecycle.py           488 '# --- in-flight thread survey ---'   491 def _status_of
                             494 _status_of split   505 _in_flight   615 gitignore (fenced out)
                             519 f"{kind}/{path.name} -- {_status_of(path)}"   <- quoted verbatim, exact
file lengths                 planner 1276, lifecycle.py 1370            <- as the plan states
```

`git grep -n "splitlines()"` over both files returns exactly those eight sites --
**the enumeration is complete**, which is the "did you find every call site" half
the plan promised to make machine-checkable.

**5. For each specified node, the perturbation that reddens it.**

| node | perturbation that makes it red | measured |
|---|---|---|
| A5 | revert `_parse_sections` to `splitlines()` | yes -- HEAD parses `[('Decision','Anthony',line 11,isolated_bq=True)]`, PATCH parses `[]` |
| A5 (status half) | revert `_parse_status` to `splitlines()` | yes, **but only if the glued status precedes the real one** -- see **[I6]** |
| A6 | `return text.splitlines()` | yes -- **positive control only**: all 12 enumerated cases still agree; the control `'a\nb\u2028c\n'` goes 3-vs-2 -> 3-vs-3 and the differ-assertion fails |
| A6 | drop the trailing-empty `pop()` | yes -- `'a\n'` -> `['a','']` vs `['a']`; also `'a\r\n'`, `'a\n\n'` |
| A7 | **none found** | no source perturbation reddens it -- see **[I5]** |
| B5 | revert `_status_of` to `splitlines()` | yes -- `'prop\u2028osed…'` -> `'prop'` |

The plan's claim that A6's positive control is *"precisely why the control is a
requirement and not a suggestion"* is confirmed: without it, A6 is satisfied by
the identity implementation.

**Degenerate-implementation probe** (the plan's own question 3): I could not find
an implementation that satisfies A5+A6+B5 and is still wrong. On the specific
sub-question the brief raises -- *"one that narrows the split but changes reported
line numbers"* -- narrowing **necessarily** changes `Section.line_no` on a carrier
(11 vs. what a `^`-anchored reader sees), and that change is *toward* `grep -n`;
`line_no` surfaces only in violation messages (planner lines 735/751/758/764) and
no node pins it. On the real corpus it cannot move (0 carriers). I judge this
closed, with the caveat that I share the author's priors on what "toward grep" is
worth.

**6. Twin-parity obligation -- covers both pairs and both lockfile rows.**

```
cmp tools/lifecycle_planner.py templates/skills/_lib/lifecycle_planner.py -> identical
cmp tools/lifecycle.py         templates/skills/_lib/lifecycle.py         -> identical

test_notice_install.py::test_every_self_hosted_twin_stays_byte_identical_to_its_source
  pairs derived from install_manifest() -- both dst rows present, both templates sources exist

dev/.cairn/cairn-lock.yml -- exactly two rows, both "verbatim": true
  tools/lifecycle.py           base_hash == hash  (c77b24c1…)   <- B4 NEWLY diverges this row
  tools/lifecycle_planner.py   base_hash != hash  (2b30639e… / f1552fc7…)  <- A4 keeps the precedent

pytest test_lifecycle_contract.py test_lifecycle_cli.py test_notice_install.py -q
  -> 63 passed in 3.41s        (plan: 63 passed in 3.68s)
```

Both test modules `importlib`-load the **template** copy under
`templates/skills/_lib/`, as the plan claims -- so A5-A7/B5 exercise the
shipped artifact and the `tools/` side is carried solely by the parity node. One
sequencing consequence the plan does not mention: because the tests load
`templates/`, A5-A7 stay **red** after the A1+A2 `tools/`-side edit and only go
green at A3 -- which interacts with the prescribed "edit `tools/` first, observe
parity fail, then apply A3" ordering. Harmless, worth a sentence.

**7. The zero-regression claim -- independently re-taken, and it holds.**

```
tracked live artifacts: 25   (15 proposals + 10 plans; the plan's figure was 21)
HEAD  scan  exit=1  sha256=88dda344…  last='6 of 25 artifact(s) carry structural violations.'
PATCH scan  exit=1  sha256=88dda344…  last='6 of 25 artifact(s) carry structural violations.'
HEAD  next  over 25 artifact(s): sha256=c0a8ae35…  lines=220
PATCH next  over 25 artifact(s): sha256=c0a8ae35…  lines=220
```

Byte-identical, at the same commit, both surfaces. The digests differ from the
plan's because the corpus grew -- which is exactly why the plan tells the
implementer to re-measure rather than compare against a recorded digest. That
instruction is correct and should be kept.

**8. Corpus sweep, with the positive control the plan requires.**

```
tracked tree (git ls-files):            494/494 identical, 0 carriers, 0 non-UTF-8
tracked dev/** (all file types):        114/114 identical, 0 carriers
tracked dev/proposals + dev/plans:       53/53  identical, 0 carriers
dev/**/*.md (rglob, as A7 specifies):   108/108 identical, 0 carriers
positive control 'a\nb\u2028c\n':       splitlines()=3  _split_lines=2  -> differ
12 enumerated edge cases:               no disagreements
```

The sweep machinery is demonstrably able to report a difference, so the
zero-carrier result is not a silently-broken sweep.

**9. Gates re-run.**

```
python bootstrap/security_check.py     -> Bandit clean over 74 shipped file(s); PASS (exit 0)
scan_targets()                         -> 74 targets, including BOTH
                                          templates/skills/_lib/lifecycle.py
                                          templates/skills/_lib/lifecycle_planner.py
python bootstrap/scaffold.py --manifest -> 96 lines
python scripts/check_cairn.py          -> OK -- 180 Markdown file(s) scanned; no issues;
                                          68 external link(s) not probed   (plan said 181)
python scripts/quality_gate.py --sub redundancy -> fail=0 info=2 (both in
                                          _lifecycle_metrics/subsystems.py; neither in scope)
python scripts/quality_gate.py --sub neutrality -> fail=95 info=21   <- but see [I2]
python bootstrap/verify_integrity.py --target .  -> 2 violations (AGENTS.md,
                                          dev/modules/security-review.md); NOTE count see [I8]
```

The scan-coverage premise-closure the plan records is confirmed: both twins are
genuinely inside the release Bandit gate, so a green there means something.

**10. Scope fences -- checked against the sibling records, not taken on faith.**

* **Does not re-solve `separator-detection`.** No chunk adds a detector rule,
  warning, flag or pattern id; `content_scan.py`, its runner and
  `check_cairn.py`'s splits are fenced out by name. `U+2028`/`U+2029` are `Zl`/`Zp`
  with `isspace()` True, so the `Default_Ignorable ∪ Noncharacter` set that
  proposal's Change 1 adopts genuinely cannot reach them -- the delegation is
  sound and the plan's reasoning for it is right.
* **Does not absorb `agent-context-scrub`.** Verified line by line in
  `dev/plans/agent-context-scrub.md`: A2 wraps both halves and makes **no change
  to `_status_of`** (line 345); A4 re-records **both** `hash` and `base_hash`
  (line 346); the Chunk-A precondition is *"A positive check, not a comment"*
  (line 418) -- all three exactly as this plan characterises them. This plan
  touches neither `_in_flight` nor any escaper.
* **The sibling's plan review has landed** -- `## Plan review -- Gemini Flash
  (External, security lens) -- 2026-08-03` at line 830 -- so Chunk B's "confirm
  the sibling can actually follow" criterion is satisfiable today. Note it landed
  as `##`, not `###`; per **[I1]** that makes no mechanical difference.

### Not covered / low confidence

* **The scope call itself -- attestor vs. detector.** This is question 1, the one
  the tier exists to buy, and it is precisely where I have **no independence**. I
  read the argument and agree with it; that agreement is worth close to nothing
  as evidence. **The External round must answer this.**
* **I did not run the full suite.** The `1710` baseline is unverified here; I ran
  63 nodes across the three cited modules. I also did not run
  `quality_gate --sub order-independence` (the plan attributes its `fail=1` to
  the concurrent `test_ast_attest` drift; unverified by me).
* **Browser / renderer behaviour** with `U+2028` -- untested, as the plan's *Known
  omissions* #1 already concedes.
* **The proposal's *Evidence* item 11 triage of 41 `splitlines()` call sites.**
  Not audited. For scale: `git grep -c "splitlines()" -- '*.py'` returns **133**
  occurrences tree-wide (both twin sides, tests included), so the "41" is a
  scoped subset whose scoping I did not reconstruct. This remains checked by
  nobody but its author, and it is a legitimate target for the External round's
  optional fourth question.
* **Whether two commits is safer than one** (question 2). I think the plan's
  argument is right, but a same-type reviewer agreeing that a split makes a cost
  *visible* is the echo the tier warns about. My one measurable contribution is
  **[I3]**: whatever the split, the disclosure currently undercounts the surfaces.
* **The window's duration.** Chunk B's "same working session" criterion is a
  commitment, not a control -- nothing enforces it, and per **[I1]** the tool will
  not stop the sibling's Chunk A either. The plan is honest that this is "a habit,
  not a gate"; I could not find a way to make it one within this plan's scope.

### Second-round recommendation

**A second round is warranted before the External review reads this, and the
External round is still required and still undischarged.**

None of my findings touches the design, the chunk boundary, the retraction, or
the measured window -- those hold, and I could not break them. All nine are
findings about **specified controls that do not control what the plan says they
control**, which is exactly the class an executing same-type reviewer can find
and an independent reader should not have to spend its budget on.

Blocking before implementation, in order:

1. **[I1]** -- the review-before-implement gate is presence-only and tier-blind,
   and this section trips it. Add the disclosure to the header; open a
   `dev/PLANNING.md` row for the tool-side question. *(Do not fix the tool here.)*
2. **[I2]** -- correct the false "no flag names any of the four files" claim,
   record the seven-line pre-existing set, and re-specify the comparison as a
   line-number-stripped `(file, token)` multiset.
3. **[I3]** -- name `session-end`/`_do_thread_survey` alongside `session-start` in
   the *Failure modes* row and in Chunk B's mandated commit-body disclosure.
4. **[I4]** -- re-point B4's tie-break at `classify_verbatim`/`upgrade`, or settle
   it on the merits with `agent-context-scrub` and say which.

Non-blocking but cheap, and all four are one or two sentences:
**[I5]** A7's docstring says it is a corpus canary with no source falsifier, and
*Known omissions* records the suite-gate coupling; **[I6]** "earlier **than the
real `**Status**` line**"; **[I7]** one row in the edge-case inventory;
**[I8]** refresh the three gate figures and correct "two more FROZEN-MODIFIED"
to one.

I have **not** appended a `### Sharpening` sub-heading: per **[I1]** this section
already registers as a landed `Plan review` section, and I am not going to add
structure that makes an Internal read look more like a discharged tier than it
already does.
