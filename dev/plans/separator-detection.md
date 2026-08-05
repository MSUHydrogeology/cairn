<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/lifecycle.md doctrine/coordination.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: ../proposals/2026-08-03-claude-separator-detection.md -->
<!-- ^ Source/sibling proposals archived 2026-08-04. These citations sit in
     append-only sections, so the path is exempted rather than rewritten. -->


# Plan: the two separators nothing detects — `U+2028` / `U+2029`

**Source proposal**: [`dev/proposals/archive/2026-08-03-claude-separator-detection.md`](../proposals/archive/2026-08-03-claude-separator-detection.md)
(accepted 2026-08-03 by Maintainer Decision, *as revised*). It sits under
`dev/proposals/` today and moves to `dev/proposals/archive/` when it archives.
**Status**: review
**Plan review**: required(**External**, security lens) — carried from the
proposal header and re-declared by the Decision's *Next transition* line, which
routes the tier into the plan "in its own right". The content scanner is a
shipped security control and its pattern-id set is an adopter-facing contract.
**No implementation commit lands before an External `## Plan review` section is
in the tree** (`doctrine/plans.md` > plan-review precondition). See
[*Plan review — the brief*](#plan-review--the-brief) for what the Internal round
about to run does and does not discharge.
**Review disposition**: the External round-2 `## Plan review` section (Codex,
2026-08-05, verdict **REVISE**) is in the tree, and the Maintainer has disposed
of that REVISE. The authorizing instruction, quoted verbatim:

> Go ahead with implementation once you've revised these. I don't want another review round

That disposition covers **the review round only**. It is not a bypass of the
plan-review precondition — the required External section exists, and the
Maintainer holds the standing to dispose of its findings, which is the escape the
round-2 verdict itself contemplates. It supplies **no** Maintainer credential, no
signing ref, no AST re-anchor ceremony, and **no approval to push**; the
Maintainer fence below is untouched by it. The revision it conditions on is the
inline fold recorded in *Sharpening — Claude (author) — 2026-08-05 (the inline
fold of A1–A33)* at the end of this file: **A1–A33 are folded into the operative
chunk rows and acceptance criteria, and the amendment tables are marked folded.
The chunk table is now the executable contract — read it, not the amendment
tables.**
**Last update**: 2026-08-05
**Opened**: 2026-08-04

## Source proposal

The proposal settles one contract: **a raw `U+2028` (LINE SEPARATOR) or `U+2029`
(PARAGRAPH SEPARATOR) in scanned text produces at least one flag naming the code
point, under its own pattern id `unicode-line-separator`, suppressible only by a
marker written against that id.** The Decision additionally accepts the
precondition the author's revision established — `_scan_unicode` **yields** its
pattern id instead of the caller re-deriving one by substring-matching the
human-readable message — because without it the detector's flags are labelled
`unicode-zero-width` and the promised marker matches nothing.

The proposal ran an External security review (SHIP), an author Response that
found the dispatch defect and moved the artifact to `revised`, an External
re-review that independently reproduced the defect (SHIP), and a second author
Response fixing the sequencing against `content-scan-detectors`. This plan
executes that decision and does not re-litigate it.

### Glossary — every term glossed on first use

* **Pattern id** — the first field of a `Flag`, e.g. `unicode-zero-width`. It is
  the key an adopter writes in a `cairn-accept` suppression marker, so the id set
  is an **adopter-facing contract**, not an implementation detail.
* **`_scan_unicode`** — the generator at
  `templates/modules/team-gated/content_scan.py:295`. It runs two per-line loops
  (zero-width, then bidi), each breaking after its first hit on that line.
* **The dispatch defect** — the ternary at
  `templates/modules/team-gated/content_scan.py:402`, which reads the message
  text to choose an id. `_scan_unicode` is the **only** generator whose caller
  re-derives its id; every other call site in `scan_text` passes a literal.
* **Frozen file** — a file whose sha256 is pinned in
  `bootstrap/tests/fixtures/gate_manifest.json`. Both files this plan edits are
  frozen; re-pinning is a supervised Maintainer act.
* **Perturbation** — a deliberate change to repository state that a test is
  claimed to detect. This repository accepts a test only when its author can name
  a state in which it fails **and has run** the change producing that state.
  **Perturbing a test's own body validates the test; only perturbing the hazard
  validates the claim** — every perturbation below edits production code, never
  the assertion.

## The measurements — taken for this plan, at HEAD `eacb7dd`

All figures below were measured on 2026-08-04 under the canonical interpreter
`~/conda_envs/lhm/bin/python3.13` (Python 3.13.13, UCD 15.1.0), against the real
scanner loaded by path. **No repository file was modified**: the "after" figures
come from two throwaway copies of `content_scan.py` in the session scratch
directory, never in the tree.

### The gap, re-measured rather than carried forward

```
python 3.13.13 UCD 15.1.0
U+2028 cat=Zl ws=True flags=0
U+2029 cat=Zp ws=True flags=0
fixture flags: []          # "## Status: open<U+2028>## Injected header" + a U+2029 paragraph
```

Zero flags, and both carry `White_Space=Yes` — which is why the RFC 8264
`Default_Ignorable_Code_Point` derivation `content-scan-detectors` adopts
excludes them **by construction**, not by oversight.

One fact worth recording because it bounds the blast radius: `scan_text` splits
on `"\n"` only (`templates/modules/team-gated/content_scan.py:390`), **not**
`splitlines()`. Measured on the fixture above: `splitlines()` → 5 lines,
`split("\n")` → 4. So a `U+2028` does **not** shift the scanner's reported line
numbers, and the flag lands on the physical line a human reading a diff sees.
That is the opposite of the planner's problem, which is why the parser fix and
this detector are genuinely separate controls.

### Alarm fatigue — the measurement the proposal requires before landing

The proposal's first *Signals the change is wrong* entry, and its named failure
mode, is that legitimate tracked files already carry these and the rule ships as
noise. Swept the whole tracked corpus:

```
files with raw U+2028/U+2029: 0
```

**Zero hits, and this plan states no denominator** (amendment A33, folded).
Every tracked file was read, not only Markdown, so `templates/`, `bootstrap/`,
`scripts/`, `docs/` and `dev/` are all inside the sweep. The rule ships silent on
today's corpus and the signal to reconsider did not fire. Re-derived at revision
`ec57bf0`, `as_of 2026-08-05`: **0 hits**, every tracked file decoding as UTF-8.
The load-bearing claim is the **hit count**, which is a stop-signal predicate; the
denominator is a moving count of unrelated commits and three different values
(494, 511, 520) were written into this plan for the same unchanged verdict across
three days — a fourth would be measured today. The implementing agent re-runs the
sweep and records **the hit count and the date**, never a denominator.

An External reviewer should re-run this sweep rather than trust it — it is the
one measurement that decides whether the tripwire trains people to ignore it.

### The dispatch defect and its fix, both reproduced against real objects

Two scratch copies of the scanner: `cs_naive` adds the detector loop and leaves
the call site alone; `cs_fixed` applies the accepted revision (yielded ids, no
ternary). Same input, three scanners:

```
HEAD  plain U+2028 : []
NAIVE plain U+2028 : ['unicode-zero-width']              <- MISLABELLED
NAIVE zw-marker    : []                                  <- silently suppressed
NAIVE sep-marker   : ['unicode-zero-width']              <- marker matches nothing
FIXED plain U+2028 : ['unicode-line-separator']
FIXED plain U+2029 : ['unicode-line-separator']
FIXED zw-marker    : ['unicode-line-separator']          <- NOT suppressed
FIXED sep-marker   : []                                  <- suppressed
```

The two middle NAIVE lines are the Decision's stated defect, executed rather than
argued: a `cairn-accept: unicode-zero-width` marker written in good faith for a
benign emoji joiner **silently clears an injected section header**, and the
marker an adopter is told to write does nothing. This is why the signature change
is a precondition and not a tidy-up.

Two further facts fall out and are used below:

```
FIXED tri-fixture  : ['unicode-bidi', 'unicode-line-separator', 'unicode-zero-width']
HEAD  tri-fixture  : ['unicode-bidi', 'unicode-zero-width']
FIXED two-sep line : [(1, 'unicode-line-separator', 'unicode line/paragraph separator U+2028')]
```

The first pair is the coexistence test the Decision requires both plans to carry,
red at HEAD and green after. The second is the Decision's **declared limit**
executed: two separators on one line flag once, and the flag names the first.

### The refactor is behaviour-preserving, checked rather than asserted

The existing suite was run against `cs_fixed` by pointing a scratch copy of the
test module at it:

```
24 passed, 1 deselected in 0.03s
```

Baseline for that file at HEAD: **25 passed** (`as_of 2026-08-04`). The one
deselection is `test_content_security_module_installs_scanner_verbatim`, which
compares installed bytes against `CONTENT_SCAN_SRC` and is meaningless when that
constant points outside the tree — it is not a result this plan may claim, and
the implementing agent runs it for real. Five direct probes (`U+202E`, `U+200B`,
`U+2060`, leading BOM, non-leading BOM) returned **identical** id sets on HEAD
and on `cs_fixed`.

Bandit over `cs_fixed`: `errors: []`, zero findings at any severity.

## Scope

Executes the accepted contract across two implementation chunks and **two
files** — exactly the proposal's *Touches* line:

* `templates/modules/team-gated/content_scan.py`
* [`bootstrap/tests/test_content_scan.py`](../../bootstrap/tests/test_content_scan.py)

Within `content_scan.py` there are **four** sites, all verified present at
revision `ec57bf0`: the module-docstring pattern-id list (the `unicode-bidi`
bullet ends at `templates/modules/team-gated/content_scan.py:45`), the detector
loops in `_scan_unicode` (`templates/modules/team-gated/content_scan.py:295`),
the call site at `templates/modules/team-gated/content_scan.py:401`, and — added
by finding [E1] — the final suppression filter at
`templates/modules/team-gated/content_scan.py:409` plus the new helper placed
above `scan_text` (`templates/modules/team-gated/content_scan.py:376`). The
fourth site is a **suppression-grammar** change scoped to the new pattern id; it
is inside the plan's two-file *Touches* line but beyond the Decision's literal
text, and it is named here rather than folded in silently.

Verified rather than assumed: `grep -rln "unicode-zero-width"` over the tracked
tree outside `dev/proposals/` and `dev/plans/` returns exactly those two files,
re-derived at revision `ec57bf0` (`as_of 2026-08-05`). In particular
`templates/modules/team-gated/content-security.md` does **not** enumerate pattern
ids, and there is no self-hosted `scripts/` twin of the scanner —
`scripts/check_cairn.py:91`–`94` loads the template file directly by path, so no
twin-parity obligation is engaged.

**And the grep is not what carries the conclusion**, because a literal-id grep
structurally cannot see a coupling that names no id.
`templates/modules/team-gated/content_scan_runner.py` builds its reviewed-residual
key as `f"{rel}:{pattern_id}:{code_hash}"`
(`templates/modules/team-gated/content_scan_runner.py:299`, consumed at
`templates/modules/team-gated/content_scan_runner.py:403`), so it is coupled to
the **id set** while containing no id. That file is untouched here and no residual
baseline churns — because Chunk A is id-preserving for both existing ids (the
pre-change tuple capture in Chunk A's acceptance is what establishes that, taken
before the edit) and the corpus carries **0** separator hits. The conclusion is
reached by that argument about the fingerprint, not by the grep. The same failure
mode applies to `bootstrap/security_check.py`: `grep -n "content_scan"` over it
returns **nothing**, yet executing `scan_targets()`
(`bootstrap/security_check.py:63`, which walks the module specs rather than a
literal list) puts both `content_scan.py` and `content_scan_runner.py` in the scan
set. A name-matching probe cannot see a set built by construction — establish
membership by executing the call path, never by grep.

**Out of scope, fenced explicitly:**

* **The parser.** `splitlines()` semantics and the planner's line grammar belong
  to `planner-line-semantics`, already decided. This plan changes no parser.
* **The orientation-stream escape table.** `agent-context-scrub` owns the output
  side. Detection and neutralization are different controls.
* **The ignorable and homoglyph rules.** `content-scan-detectors` owns
  `unicode-ignorable`, `unicode-tag` and the Greek confusable narrowing. This
  plan adds a rule **beside** them and edits neither. The one place the two
  plans meet is the `_scan_unicode` signature, and the Decision assigns it here.
* **The `Zs` space-separator space.** A different question with a real
  international-name cost, live as a Maintainer question on
  `byline-classification`. Not touched.
* **Changing the per-line `break` convention.** The Decision records one
  separator flag per line as a **declared limit**. Changing it would alter
  shipped `unicode-zero-width` and `unicode-bidi` output for every adopter and
  needs its own proposal. This plan *pins* the limit with a test rather than
  leaving it implicit.
* **Re-pinning `bootstrap/tests/fixtures/gate_manifest.json`.** A supervised
  Maintainer act — see [*Maintainer fence*](#maintainer-fence).
* **Widening `_BANNED_CODEPOINTS` beyond the two separators.** The test-side
  hygiene set grows by exactly two entries; the general question of which
  invisibles the scanner's own source may carry is `content-scan-detectors`'.

### Documentation / doctrine surface

* **Governing layer — none.** No `AGENTS.md` change, no `doctrine/` change. The
  doctrine-change rate-limit is not engaged.
* **Adopter-facing contract — yes, and this is the one that matters.** The
  pattern-id set grows by one. Its single canonical home is the bulleted list in
  the `content_scan.py` module docstring
  (`templates/modules/team-gated/content_scan.py:40`–`45` today), which is
  shipped verbatim into an adopter's own `scripts/` directory. Edited in the same
  commit as the behaviour it describes (Chunk B), never later.
* **Descriptive layer — none.** Checked, not assumed: no file under `docs/` or
  `bootstrap/` enumerates scanner pattern ids
  (`grep -rln "unicode-zero-width"`, above).
* **Release-facing — one line, deferred to a serialization point.**
  `CHANGELOG.md > Unreleased > Added`. `CHANGELOG.md` is a **serialized shared
  file** (`AGENTS.md` > *Shared communication files*) and this plan does not
  edit it in an implementation commit. See Chunk C.
* **Deliberation layer** — this plan, its plan review, its code review, and the
  one-line `dev/PLANNING.md` row-move that serializes the plan-open.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

## Maintainer fence

Two items are **not the implementing agent's to perform**, and one of them is the
reason this plan is batched with its sibling rather than standing alone.

**F1 — the frozen-file re-pin (needs a key and a supervised session).** Both
files this plan edits are literal keys in the 164-entry `frozen_files` map in
`bootstrap/tests/fixtures/gate_manifest.json`, verified at revision `ec57bf0`
(`as_of 2026-08-05`; `templates/modules/**/*.py` and `bootstrap/tests/**/*.py` are
both frozen-set globs — `bootstrap/tests/_gate_manifest.py:165`–`167`). After this
plan lands, `python bootstrap/tests/_gate_manifest.py verify` reports **these two
files among its `FROZEN-MODIFIED` entries**. **Name the two files; state no
total** (amendment A14, folded) — the total is other workflows' to move and is
stale by the time it is read. Re-producing the manifest is a supervised
prerequisite commit under `bootstrap/REANCHOR_RUNBOOK.md`, whose Phase 0 runs
under a clean child shell with recorded values and a signing backend. The
implementing agent's whole obligation is to **say so in the final commit body and
name the two files**.

**F2 — one ceremony for two plans, and only if it can be bounded to them.**
`content-scan-detectors` edits the **same two files** and is being planned in
parallel; its frozen-file delta is the identical pair. Per finding [E2], a shared
ceremony is **not** authorized by that coincidence alone: it is authorized only
over an exact, reviewed set owned by these two plans. The batch rule this plan
adopts:

* Neither plan re-pins.
* Whichever lands second records **the same two files** as the pair *this change*
  makes stale, and states plainly that `_gate_manifest.py verify` will report
  **others belonging to other workflows** — the plan asserts no total.
* **The shared ceremony is conditional, and the condition is checked before it
  runs.** It is authorized **only** over the exact set
  `{templates/modules/team-gated/content_scan.py,
  bootstrap/tests/test_content_scan.py}`. Before the re-produce, the Maintainer
  enumerates the `FROZEN-MODIFIED` / `COLLECTION-DROPPED` / `SKIP-XFAIL-NEW` paths
  from `python bootstrap/tests/_gate_manifest.py verify`; **if any member falls
  outside that set, the shared ceremony is off** and each unrelated surface takes
  its own disposition first. A blanket re-produce would bless concurrently-landed
  frozen-surface changes nobody reviewed.
* **What runs that enumeration is a human, and nothing else.** Checked by opening
  the artifacts rather than by citing them: `bootstrap/tests/_gate_preflight.py`
  derives the blessing scope as bare **counts** —
  `bootstrap/tests/_gate_preflight.py:1164`–`1170` builds
  `{"modified": …, "added": …, "removed": …, "collection_before": …,
  "collection_after": …}` by `sum(1 for …)` and `draft_message` prints those
  counts. It names **no paths** and has **no refusal path** for an unexpected
  member. Only `bootstrap/tests/_gate_manifest.py:364` names paths, and only in
  `verify` output a human reads. So the condition above is discharged by the
  Maintainer reading the enumeration; **this plan does not build a gate and must
  not be read as implying one** (adding the refusal is `_gate_preflight.py`'s
  surface — outside this plan's two files and inside
  `bootstrap/REANCHOR_RUNBOOK.md`'s Maintainer-only territory).
* **The state being blessed moves faster than any figure written here.** The
  enumeration is taken **at ceremony time** and this plan quotes no violation
  count: successive readings of the same command gave 17 (2026-08-04), 60
  (2026-08-05 morning) and a materially larger set at revision `ec57bf0` the same
  afternoon, **none of them this plan's**. The invariant, not the number, is what
  binds: *every member of the enumeration is inside the two-file set, or the
  shared ceremony is off.*
* If only one of the two lands (the other is struck or deferred), the surviving
  plan's commit body is already correct and the ceremony is unchanged — still
  subject to the bounding condition above.

**No AST re-anchor.** Checked: no file under `bootstrap/_scaffold/` is touched,
so `bootstrap/tests/fixtures/scaffold_ast_baseline.json` is unaffected and the
runbook's attestation half is not engaged.

**No active batch window.** The `gate-reanchor-preflight` plan is archived
(`dev/plans/archive/gate-reanchor-preflight.md`), so the batch-window HOLD-by-
default on editing a frozen file is not in force. Re-confirm at implementation
rather than inherit this line.

## Sequence

Chunk order is load-bearing. **Chunk A lands before Chunk B**: if the detector
arrives first, then at that intermediate commit every separator flag is labelled
`unicode-zero-width` and any existing zero-width suppression in an adopter tree
silently hides it. That intermediate state is the exact defect the Decision
exists to close, so it must never be a commit.

```
0. plan-open   -- this plan + the dev/PLANNING.md row-move              [commit pending]
   (plan review) -- required(External, security lens): round 1 landed 0deeac0,
                    round 2 landed e1b2e30 (REVISE), Maintainer-disposed and
                    folded inline -- see the header's Review disposition
1. Chunk A -- _scan_unicode yields its own pattern id; the ternary dies [commit pending]
2. Chunk B -- the detector, the acceptance-association refusal (B10),
              the collection-integrity guard (B11), + the contract entry [commit pending]
3. Chunk C -- the shared release note, at a serialization point         [deferred]
```

**Cross-plan ordering, binding on both plans.** Whichever of
`separator-detection` / `content-scan-detectors` lands second **re-reads
`bootstrap/tests/test_content_scan.py` rather than appending blind**, and uses
test-class names specific to its own plan. This is not a courtesy: a duplicate
top-level class name silently removes the earlier class from collection, with no
error and no warning. The convention is stated in full — and backed by the
mechanical guard **B11** — under Chunk B.

---

### Chunk A — prose stops being a dispatch key

Behaviour-preserving by construction and by measurement: the two existing ids are
produced by the same two loops, in the same order, with the same messages. What
changes is *where the id comes from*.

| # | File | Change |
|---|------|--------|
| A1 | `templates/modules/team-gated/content_scan.py` | `_scan_unicode` (at `templates/modules/team-gated/content_scan.py:295`) yields **3-tuples** `(lineno, pattern_id, msg)`. The zero-width loop yields the literal `"unicode-zero-width"`; the bidi loop yields the literal `"unicode-bidi"`. Messages unchanged, byte for byte — an adopter grepping logs for the old wording is unaffected. |
| A2 | `templates/modules/team-gated/content_scan.py` | The call site at `templates/modules/team-gated/content_scan.py:401`–`403` becomes `for lineno, pid, msg in _scan_unicode(...): raw.append(Flag(pid, lineno, msg))`. **The ternary is deleted, not amended.** A comment states the contract in one line: this generator yields its own id because a message is prose and prose is not a dispatch key. |
| A3 | `bootstrap/tests/test_content_scan.py` | New `TestUnicodeDispatchContract::test_scan_unicode_yields_its_own_pattern_id`: call the module-private `_scan_unicode` directly on a two-line fixture (a zero-width character on line 1, a bidi override on line 2) and assert the yielded items are exactly `[(1, "unicode-zero-width", <msg>), (2, "unicode-bidi", <msg>)]` on the id field, unpacking as 3-tuples. This is the contract `content-scan-detectors` rebases onto, so it is pinned by a test rather than by a sentence in a Decision. |

**Acceptance criteria — Chunk A.**

* **Command**: `~/conda_envs/lhm/bin/python3.13 -m pytest
  bootstrap/tests/test_content_scan.py -q` → all pass, 0 skipped.
  **Invariant, not a count** (amendment A18, folded): capture the collected
  **node-id set** with `--collect-only -q` **before** the edit and again after,
  and require the after-set to be a **strict superset** of the before-set. Assert
  the set, never its size — a count check cannot distinguish "n nodes added" from
  "n+k added, k silently shadowed away", which is the hazard B11 exists for. Store
  the before-capture outside the tree; it cannot be regenerated once the edit
  lands. **What runs this**: a person typing the command. There is no CI in this
  repository, and the two installed git hooks (`tools/intent.py`, pre-commit
  intent-claim check and post-commit auto-release) run no tests — nothing fires
  this gate unless a human or a reviewer types it.
* **Behaviour identity, checked against a pre-change capture.** Before row A1,
  write the full `(line, pattern_id, message)` tuple list for a five-probe fixture
  (`U+202E`, `U+200B`, `U+2060`, leading `U+FEFF`, non-leading `U+FEFF`) to a
  scratch file **outside the tree**; after row A2, assert byte-equal. **The
  material for this check cannot come from the artifact under test**: once rows
  A1–A2 land, the pre-change tuple list is unrecoverable from the working tree, so
  a baseline "reconstructed" afterwards would be the edited scanner describing
  itself. Take it first or the criterion is unsatisfiable — do not substitute a
  post-hoc reconstruction, and do not carry this plan's simulated figures as the
  baseline.
* **Perturbation P-A1 — A3 discriminates the shape (hazard-side, RUN).** In
  `content_scan.py`, restore the 2-tuple yield and the ternary; A3 fails on the
  unpack. Restore; confirm `git diff templates/modules/team-gated/content_scan.py`
  is empty.
* **Perturbation P-A2 — A3 discriminates the *value*, not merely the arity
  (hazard-side, RUN).** Keep the 3-tuple shape but swap the two yielded
  literals (zero-width loop yields `"unicode-bidi"` and vice versa); A3 fails on
  the id field, **and** the pre-existing `test_zero_width_caught` and
  `test_bidi_control_caught` fail with it. P-A1 alone would pass against a test
  that only counted tuple elements; P-A2 is what shows the assertion is about
  identity. Restore; confirm `git diff` empty.
* **The future state in which A3 fails** is concrete and near: any later author —
  including `content-scan-detectors`' implementer — who reintroduces id
  derivation from message text. That is precisely the state the Decision's
  sequencing rule forbids, and A3 is how the second plan inherits a guard rather
  than a promise.
* **Channel note.** Subject: `_scan_unicode` and `scan_text`. Oracle: two id
  literals typed into the test by a human, and a pre-change capture taken
  outside the repository. Neither is derived from the code under verification.

---

### Chunk B — the detector, and the id that makes its marker mean something

**Production rows: B1, B2, B3, B10. Test rows: B4, B5, B6a, B6b, B7, B8, B9a,
B9b, B9c, B11.** Rows are listed in label order, not landing order; the whole
chunk lands as one commit, so no intermediate state ships a detector without its
refusal or its tests.

**Test-class naming, binding on both plans** (folded from amendment A32, which
superseded A17). Every test class this chunk adds carries a name specific to
*this* plan — `TestSeparatorDetection` for the detection, suppression and refusal
nodes, `TestSeparatorDetectionCoexistence` for the shared coexistence node,
`TestSeparatorDetectionCollectionIntegrity` for the guard — and
`content-scan-detectors` uses its own distinct class names. Whichever plan lands
second **re-reads the file rather than appending blind**. This is not style: a
duplicate top-level class name **shadows the entire earlier class**. Measured on
standalone hazard modules — a 5-method class followed by a 1-method class of the
same name collects **1** node; a class with a duplicated method collects **2** of
3 — silently in both cases, no error, no warning. The convention is **backed by
B11**, because a convention cannot protect against a failure that produces no
error; the guard reports the collision, it does not resolve it, so the habit is
retained alongside it.

| # | File | Change |
|---|------|--------|
| B1 | `templates/modules/team-gated/content_scan.py` | New module constant `_LINE_SEPARATORS`, beside `_ZERO_WIDTH` (`templates/modules/team-gated/content_scan.py:137`) and `_BIDI` (`:144`), holding `U+2028` and `U+2029` **as `\uXXXX` escape forms with a naming comment each** — never raw. The existing comment block above `_ZERO_WIDTH` already states this rule (trojansource-safe, Bandit B613) and the new constant is placed under it so the rule covers it by adjacency, not by a second copy. |
| B2 | `templates/modules/team-gated/content_scan.py` | A third per-line loop in `_scan_unicode`, after the bidi loop, yielding `(i, "unicode-line-separator", f"unicode line/paragraph separator U+{ord(ch):04X}")` and breaking after the first hit on that line — **following** the existing per-category-per-line convention, which the Decision fixes as a declared limit. |
| B3 | `templates/modules/team-gated/content_scan.py` | Module-docstring pattern-id list: a `unicode-line-separator` bullet after the `unicode-bidi` bullet (which ends at `templates/modules/team-gated/content_scan.py:45`). It names both code points, says the detector **flags and never rewrites**, and states the declared limit (one separator flag per line; the flag names the first) in one clause. Two further clauses are required, and they are the adopter-visible half of [E1] (folded from amendments A9 → A24): **(i)** an acceptance for this id is honoured **only when the marker renders on the same display line as the separator it accepts** — suppression scope is *file*-line scope, and `U+2028` is the first detected code point for which a file line and a display line differ; **(ii)** the **block form** (`cairn-accept` … `cairn-accept-end` spanning the hit) does **not** suppress this id — measured, not inferred. This bullet *is* the adopter-facing contract entry. |
| B4 | `bootstrap/tests/test_content_scan.py` | Extend `_BANNED_CODEPOINTS` (`bootstrap/tests/test_content_scan.py:48`–`52`) with `0x2028, 0x2029`, **and widen `TestSourceCarriesNoRawInvisibles::test_no_raw_banned_codepoints_in_source` to read both `CONTENT_SCAN_SRC` and the test module's own path** — today it reads `CONTENT_SCAN_SRC` only (`bootstrap/tests/test_content_scan.py:65`). Folded from amendment A16. After B5–B9c the test module is itself a file whose fixtures are separator code points, and "escape forms in the test source" is otherwise a convention with nothing enforcing it. A scanner that smuggles the code point it detects is the exact failure this class of test exists for. Verified the widening is what does the work, not the pre-existing set: with a raw `U+2028` planted in a source comment, `_BANNED_CODEPOINTS` as it stands reports **no hits** and the widened set reports `0x2028`. |
| B5 | `bootstrap/tests/test_content_scan.py` | New `TestSeparatorDetection::test_each_separator_is_caught`, **parametrized** — `@pytest.mark.parametrize("cp", [0x2028, 0x2029])` — so each code point is its **own collected node** asserting exactly one flag with `pattern_id == "unicode-line-separator"` and `f"U+{cp:04X}"` in the message. Folded from amendment A4: a per-member claim requires a per-member node, and the un-parametrized form cannot support the per-member perturbation P-B2 in both directions. Escape forms in the test source, matching B4. |
| B6a | `bootstrap/tests/test_content_scan.py` | New `TestSeparatorDetection::test_own_id_marker_suppresses`: a `cairn-accept` marker naming `unicode-line-separator`, **written before the separator on the same file line** (the associable form B10 honours), clears the flag. Folded from amendment A1, which split the original single-node B6. |
| B6b | `bootstrap/tests/test_content_scan.py` | New `TestSeparatorDetection::test_foreign_id_marker_does_not_suppress`: a marker naming `unicode-zero-width` does **not** clear a separator flag; asserts `[f.pattern_id for f in scan_text(fixture)] == ["unicode-line-separator"]`. This is the regression for the dispatch defect and **the security-critical assertion in the whole plan**, so it is a node of its own: a shared node cannot be independently falsifiable, and under the P-B3 state a single-node B6 aborts at its positive half so the negative half never executes. Its perturbation is P-B7 (two-site — see the acceptance criteria), **not** P-B3. |
| B7 | `bootstrap/tests/test_content_scan.py` | New `TestSeparatorDetectionCoexistence::test_all_three_unicode_ids_trip_independently`: one three-line fixture (zero-width on line 1, bidi on line 2, `U+2028` on line 3); assert the `(line, pattern_id)` set is **exactly** `{(1, "unicode-zero-width"), (2, "unicode-bidi"), (3, "unicode-line-separator")}`. This is the coexistence test the Decision requires **both** plans to carry; whichever lands first turns it green and the second inherits it. The class name is plan-specific by the convention above — `content-scan-detectors` must **not** reuse it. |
| B8 | `bootstrap/tests/test_content_scan.py` | New `TestSeparatorDetection::test_two_separators_on_one_line_flag_once`: a line carrying `U+2028` then `U+2029` yields exactly one flag, naming `U+2028`. Pins the Decision's **declared limit** so a later author who changes the `break` semantics does so deliberately, against a red test and its own proposal, rather than by accident. |
| B9a | `bootstrap/tests/test_content_scan.py` | New `TestSeparatorDetection::test_cross_separator_acceptance_refused_same_file_line`: payload, then a separator, then an own-id `cairn-accept` marker, **all on one file line**; assert `[f.pattern_id for f in scan_text(fixture)] == ["unicode-line-separator"]` — the acceptance is **refused**. Folded from amendments A6 → A20: the previous B9 *pinned* this waiver, and [E1] is right that "pinning that behavior makes the exception durable; it does not make it safe". **Do not build the pinning B9.** Measured against a build carrying B10: green; against a build without B10: fails. |
| B9b | `bootstrap/tests/test_content_scan.py` | New `TestSeparatorDetection::test_cross_separator_acceptance_refused_preceding_line`: an own-id marker on file line 1, the hit on file line 2 spanning four display lines; assert the flag **survives**. This is the `{i, i + 1}` preceding-line scope (`templates/modules/team-gated/content_scan.py:261`) crossed with a separator — a reviewer who writes a marker believing it annotates "the line just below" would otherwise clear an injected header several display lines away. |
| B9c | `bootstrap/tests/test_content_scan.py` | New `TestSeparatorDetection::test_same_display_line_acceptance_is_honoured`: an own-id marker written **before** the separator on the same file line; assert `scan_text(fixture) == []`. This is the "tests for both paths" half [E1] asks for, and it is what stops B10 being a silent conversion of the rule to *unsuppressible*. Measured: green against builds with **and** without B10. |
| B10 | `templates/modules/team-gated/content_scan.py` | **Production.** Folded from amendment A21 — the [E1] refusal, taken in the reviewer's first branch. A module-level helper `_separator_accept_is_associable(line)` placed immediately above `scan_text` (`templates/modules/team-gated/content_scan.py:376`): it locates the first `_LINE_SEPARATORS` member in the file line and returns `True` only if `_ACCEPT_RE` (`templates/modules/team-gated/content_scan.py:193`) finds a marker **before** that index whose `pid` is `unicode-line-separator` and whose `reason` attribute is non-empty — the same validity rule `_parse_suppressions` applies (`templates/modules/team-gated/content_scan.py:240`, reason check at `:259`). The final filter at `templates/modules/team-gated/content_scan.py:409` becomes an explicit loop: a flag suppressed by the existing per-id line scope is **re-emitted** when `f.pattern_id == "unicode-line-separator"` and the helper returns `False`. `_parse_suppressions` is **not** modified and **no other pattern id's path changes** — measured: the real test module repointed at this build is byte-identical in outcome to the build without it, so no marker any adopter has already written changes meaning. Two consequences stated rather than left to discovery: the **block form** spanning the hit is also refused (a block acceptance is even less reliably associable than a preceding-line one), and the accept path survives (B9c), so this is a narrowing inside the Decision's *"suppressible only by a marker written against that id"* bound, not a conversion to unsuppressible. |
| B11 | `bootstrap/tests/test_content_scan.py` | New `TestSeparatorDetectionCollectionIntegrity::test_no_duplicate_test_class_or_method_names`: parse **this module's own source** with the standard-library `ast` (no new dependency — `bootstrap/DEPENDENCY_BUDGET.md` unaffected) and assert that (i) no two top-level `ClassDef` nodes share a name and (ii) within each class, no two `FunctionDef` / `AsyncFunctionDef` nodes share a name. Folded from amendments A30 and A32: this is [E3]'s mechanical guard, because "a naming convention cannot protect against the known silent class shadowing failure". It fires **inside the file** at the moment a second plan appends a colliding class, where a collection-count check fires only after nodes have already vanished. Measured at revision `ec57bf0`: the guard returns clean against `bootstrap/tests/test_content_scan.py` as it stands, and flags `duplicate top-level class: <name>` and `duplicate method <Class>.<name>` on hazard modules. **Named residual — the guard lives in the file it judges**: a duplicate of *its own* class name would shadow the guard itself, silently. Two mitigations, both stated because neither alone closes it: the class name is plan-specific by the convention above (A30 proposed the generic `TestCollectionIntegrity`; the convention that A32 makes binding forbids a generic name here, so the plan-specific name is used and the deviation is recorded in the Sharpening), and the **independent** catcher is Chunk A's node-id-set criterion, whose before-capture is taken outside the tree by a person and therefore is not supplied by the module under test. |

**Acceptance criteria — Chunk B.**

**Every gate below is triggered by a person typing the command.** There is no CI
in this repository. The only installed git hooks are `tools/intent.py`'s
pre-commit intent-claim check and its post-commit auto-release; neither runs
pytest, neither runs a checker, and neither can fail this chunk. Nothing here is
enforced by machinery on a push.

* **Focused module** — `~/conda_envs/lhm/bin/python3.13 -m pytest
  bootstrap/tests/test_content_scan.py -q` → all pass, 0 skipped, including
  `test_content_security_module_installs_scanner_verbatim` run **for real**
  (this plan's own measurement deselected it; the implementation may not).
  **The invariant is the node-id set, not a node count** (amendment A18, folded):
  capture `--collect-only -q` before and after and require the after-set to be a
  **strict superset** of the before-set. No frozen denominator appears in this
  criterion, deliberately — the reviewer's sharpening on the round-2 verdict says
  the chunk must "name the command and invariant rather than freeze an incidental
  denominator", and the counts in this plan's review history are already stale.
* **Whole suite, as a delta** (amendment A10, folded) —
  `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests`: **no failure
  present that is absent from a baseline captured at implementation start, no node
  dropped from collection, no new skip or xfail.** Record both readings in the
  commit body. The predicate is a delta and **not** an absolute because the
  absolute is not a stable function of committed content: the same commit read
  hours apart in this tree has given "3 failed" and "0 failed", and independent
  readers have obtained different absolutes from one commit. Do **not** carry a
  suite total out of this plan; take the baseline yourself, before the edit.
* **The corpus sweep, re-run as the alarm-fatigue gate — and it must not be run
  by the code under test** (amendment A33, folded). Two different claims, so two
  different commands, and only one of them is independent:
  * *Independent measurement of the corpus.* Re-run the raw sweep over
    `git ls-files` with a script that reads the code points **literally** and does
    **not** import `content_scan` — record **the hit count and the date** in the
    commit body. **No denominator**: three have been written into this plan for the
    same unchanged verdict. **A non-zero hit count is a signal to stop and
    reconsider, not to suppress**; the disposition is a Maintainer question, never
    an inline `cairn-accept`.
  * *Not independent, and useful anyway.* `~/conda_envs/lhm/bin/python3.13
    scripts/check_cairn.py` runs the **shipped scanner** — i.e. the artifact this
    chunk edits — over Cairn's own corpus. After B2 lands it is a measurement of
    the new detector's behaviour, not of whether the corpus contains separators.
    Treat it as the doc gate and as a smoke test of the detector, never as the
    alarm-fatigue evidence.
  * *Predicate for `check_cairn`* (amendment A12, folded, with the clause the
    Figure correction withdrew left out): **no issue attributable to this change**,
    as a delta against a baseline captured at implementation start; **and** a run
    scoped to the two touched files must be clean outright. A non-`OK` whole-tree
    run is a signal to look for untracked or concurrent state — it is **not** an
    expected condition, and this plan does not tell you to anticipate one.
* `~/conda_envs/lhm/bin/python3.13 -m bandit -q -f json
  templates/modules/team-gated/content_scan.py` → `errors: []`, zero findings at
  every severity. Measured on the prototype (including the build carrying B10);
  **re-take against the real edit** — the prototype is not the artifact.
  `templates/modules/team-gated/content_scan.py` is inside
  `bootstrap/security_check.py`'s scan set, established by executing
  `scan_targets()` (`bootstrap/security_check.py:63`) and **not** by grep, which
  finds no mention of the file at all. A MEDIUM+ finding here is a release
  blocker, not a lint nit.
* `~/conda_envs/lhm/bin/python3.13 scripts/quality_gate.py --sub neutrality` →
  **invariant: no new `fail` entry attributable to either touched file.**
  `bootstrap/` is a neutrality scan root, so the test file passes through it;
  `templates/` is not. Capture the baseline **before** the edit and compare — the
  reading is tree-sensitive, so a figure quoted from this plan is not a baseline.
  Snapshot for orientation only, re-derived at revision `ec57bf0`
  (`as_of 2026-08-05`): `fail=95 info=21`.
**Perturbation ledgers record which nodes fail, never a pass/fail total.** The
totals in this plan's review history (`1 failed, 4 passed`, `2 failed, 7 passed`,
`9 passed`, …) were measured against scratch reconstructions whose node set
predates this fold — B5 is now two nodes, B6 is two, B9 is three, and B11 is new,
so those totals do not correspond to anything an implementer will see. **Do not
copy them into a ledger**; record the *named nodes* that went red and the *named
nodes* that stayed green, which is the claim that discriminates.

* **Perturbation P-B1 — the detector loop is load-bearing (hazard-side, RUN).**
  Delete the B2 loop; **both** B5 nodes fail, B7 fails on the third pair, B8
  fails, and B9a/B9b fail (no flag survives to be refused). B6a and B9c stay
  green. Restore; confirm `git diff
  templates/modules/team-gated/content_scan.py` empty.
* **Perturbation P-B2 — B5 discriminates *each member*, not just the loop
  (hazard-side, RUN, both directions)** (amendment A5, folded). Remove `U+2029`
  from `_LINE_SEPARATORS`, leaving `U+2028`: the **`0x2029` node** fails and the
  `0x2028` node stays green. Then repeat the other way round: remove `U+2028`,
  leaving `U+2029`, and the **`0x2028` node** fails alone. **The second direction
  only works because B5 is parametrized** — on the un-parametrized single node it
  aborted at the `U+2028` assertion so the `U+2029` assertion never ran, and
  B6/B7/B8 failed with it because their fixtures use `U+2028`. Without a
  per-member node a single-member constant would pass a loop-level perturbation
  and ship half the contract. Restore; confirm `git diff` empty.
* **Perturbation P-B3 — B6a is the dispatch regression (hazard-side, RUN)**
  (amendment A2, folded). Revert Chunk A in place (restore the 2-tuple yield and
  the ternary) while keeping the B2 loop; **B6a** fails — the own-id marker
  matches nothing, because the flag is labelled `unicode-zero-width`. Measured
  under this exact state on a scratch reconstruction: `AssertionError: own-id
  marker must clear` / `assert ['unicode-zero-width'] == []`. **P-B3 says nothing
  about B6b**, which in the single-node form never executed under this state at
  all; **B6b's perturbation is P-B7**. Restore; confirm `git diff` empty.
* **Perturbation P-B4 — B7 discriminates the id, not the count (hazard-side,
  RUN).** Change the B2 loop's yielded literal to `"unicode-zero-width"`; B7
  fails on the set comparison while a hypothetical "three flags appeared" test
  would have passed. This is why B7 asserts the exact `(line, pattern_id)` set.
* **Perturbation P-B5 — B8's limit can fire (hazard-side, RUN).** Remove the
  `break` from the B2 loop; B8 fails with two flags on one line. Restore. This
  perturbation is also the *proposal* a future author would need: it shows the
  limit is enforced, not merely described.
* **Perturbation P-B6 — B4's hygiene guard can fire (hazard-side, RUN,
  transient).** Write a raw `U+2028` into a comment in `content_scan.py` in the
  working tree; `test_no_raw_banned_codepoints_in_source` fails naming
  `0x2028`. Repeat in `bootstrap/tests/test_content_scan.py` itself, which the
  B4 widening brings into the guard's scope — it must fail there too, and on the
  pre-widening guard it would not. Delete both; confirm `git status --short`
  clean. Never committed.
* **Perturbation P-B7 — B6b's negative half is non-vacuous (hazard-side, RUN,
  TWO-SITE)** (amendments A3 → A26, folded). **The single-site form must not be
  carried forward: it stopped working once B10 landed.** Widening the final filter
  (`templates/modules/team-gated/content_scan.py:409`) alone to suppress by line
  while ignoring `pattern_id` leaves **every node green** — B10's own pid check
  independently keeps the foreign marker from clearing the flag, so the
  perturbation never reaches the assertion it exists to falsify. A one-line
  version of this perturbation is therefore a **false ledger entry**. Perturb
  **both** id checks: (1) the final filter suppresses by line ignoring
  `pattern_id`, **and** (2) `_separator_accept_is_associable` accepts any valid
  `cairn-accept` marker regardless of its `pid`. Measured on a scratch
  reconstruction: exactly `test_foreign_id_marker_does_not_suppress` (B6b) goes
  red and nothing else does. **This is the only perturbation that falsifies the
  plan's security-critical assertion; without it that assertion ships
  unfalsified.** Restore both sites; confirm `git diff
  templates/modules/team-gated/content_scan.py` empty.
* **Perturbation P-B8 — the [E1] refusal can fire (hazard-side, RUN)**
  (amendments A7 → A25, folded). Delete the B10 re-emit branch from the final
  filter, restoring the plain per-id line filter, while keeping every test node;
  **B9a and B9b go red and B9c stays green**, and only those three are implicated.
  `_parse_suppressions` is untouched by this perturbation, so it discriminates the
  refusal itself rather than the line scope. (The superseded form of this
  perturbation narrowed `{i, i + 1}` to `{i}` at
  `templates/modules/team-gated/content_scan.py:261`; that no longer targets the
  mechanism, because under B10 the preceding-line case is already refused. **Do
  not run the superseded form.**) Restore; confirm `git diff` empty.
* **Perturbation P-B9 — B11 can fire (hazard-side, RUN, transient)**
  (amendment A31, folded). Append a second `class
  TestSeparatorDetectionCollectionIntegrity` carrying one method to
  `bootstrap/tests/test_content_scan.py`; B11 fails naming `duplicate top-level
  class: TestSeparatorDetectionCollectionIntegrity`. Repeat with a duplicate
  **method** name inside one class; B11 fails naming `duplicate method
  <Class>.<name>`. Delete both; confirm `git status --short` clean. **This is the
  one perturbation whose subject is the test module rather than production code,
  and that is correct, not an exception**: the hazard [E3] names *is* a property of
  the test module's own source, so perturbing that source is perturbing the
  hazard, not softening an assertion. Re-measured at revision `ec57bf0` on
  standalone hazard modules: a 5-method class followed by a 1-method class of the
  same name collects **1** node, and a class with a duplicated method collects
  **2** of 3 — silently in both cases, no error and no warning, which is exactly
  why a collection **count** check cannot see it and why Chunk A's criterion
  asserts the node-id **set**.
* **The future states in which B5–B9c and B11 fail**, named because that is the
  acceptance bar: (i) the detector loop removed or narrowed by a later refactor;
  (ii) the ternary reintroduced by whichever sibling plan lands second — the
  state the Decision's sequencing rule exists to forbid; (iii) the yielded id
  renamed without the docstring contract entry moving with it; (iv) the
  per-line `break` semantics changed as a rider on some other change; (v) the B10
  re-emit branch dropped or its pid check widened, restoring the waiver [E1]
  refuses; (vi) a colliding test-class or method name appended by the sibling plan,
  which B11 catches inside the file and Chunk A's node-id-set capture catches
  across the merge.
* **Channel note.** Subject: `scan_text` through its public path — no stub of
  the function under test anywhere in B5–B9c. Oracles: code-point literals and id
  strings typed into the test by a human, plus `unicodedata`'s categories quoted
  in the docstring. Nothing in the oracle is computed from `_LINE_SEPARATORS`,
  from the detector loop, or from `_separator_accept_is_associable`, so a gap
  cannot move both together. **B11 is the one node whose subject is a repository
  file rather than a function**, and its oracle — "no two names collide" — is a
  property of the AST, not a value the module computes about itself; its named
  residual (the guard sits in the file it judges) is recorded in the B11 row.

---

### Chunk C — the shared release note

**Deferred, and deliberately not an implementation commit.** `CHANGELOG.md` is a
serialized shared file, edited only at a defined serialization point
(`AGENTS.md` > *Shared communication files*).

| # | File | Change |
|---|------|--------|
| C1 | `CHANGELOG.md > Unreleased > Added` | **One** line covering the pattern-id partition, shared with `content-scan-detectors` rather than duplicated: the content scanner's unicode detectors now carry their own pattern ids, and a raw `U+2028` / `U+2029` flags under `unicode-line-separator`. **The same line must state the acceptance-association rule** (amendment A27, folded): a `unicode-line-separator` acceptance is honoured only when it renders on the same display line as the separator it accepts, and the block form does not suppress it. That is the adopter-visible half of [E1], and a release note that omits it ships a surprise. Cross-reference both proposals and both plans **by stem**, per `AGENTS.md`. |

**Acceptance criteria — Chunk C.**

* Written at the next serialization point (a lifecycle archive, the goodnight
  routine, or explicit Maintainer instruction) — **not** in an implementation
  commit, and not by an agent holding this plan open mid-flight.
* **One line for both plans.** If `content-scan-detectors` has already written
  its line, this plan **amends that line** rather than adding a second. Two
  adjacent entries describing one pattern-id partition is drift by construction.
* `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py CHANGELOG.md` → clean.

## Acceptance criteria

Per-chunk criteria are above; these are the plan-level deliverables.

* **Tests that must pass.**
  * `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` — under the
    canonical interpreter (3.13.13), **as the delta defined in Chunk B**: no new
    failure, no dropped node, no new skip or xfail, against a baseline captured at
    implementation start (amendment A11, folded). **No absolute suite figure is
    asserted anywhere in this plan**, and none may be carried out of it.
  * [`bootstrap/tests/test_content_scan.py`](../../bootstrap/tests/test_content_scan.py)
    — the dispatch-contract test (Chunk A row A3), the detection **pair of nodes**
    (B5, parametrized), the two suppression-isolation nodes (B6a, B6b), the
    coexistence set (B7), the declared limit (B8), the three acceptance-association
    nodes (B9a, B9b, B9c), the collection-integrity guard (B11), and the widened
    hygiene set (B4). **Command plus invariant, not a count**: capture the
    `--collect-only -q` node-id set before and after and require a strict superset
    (amendment A18, folded). A collected-node **count** is not the predicate,
    because a count cannot see nodes silently shadowed away.
  * **Every new test shown non-vacuous by a perturbation of the hazard**, with
    the ledger — the change made, the **named nodes** observed red and green, and
    the byte-identical restore confirmed by an empty `git diff <path>` — in the
    commit body. **Eleven** perturbations are specified above: P-A1, P-A2, and
    P-B1 through P-B9. Nine of them edit `templates/modules/team-gated/content_scan.py`;
    **P-B6 and P-B9 edit `bootstrap/tests/test_content_scan.py`**, which is
    correct rather than an exception, because in both cases the hazard *is* a
    property of that file's source (a smuggled raw code point, a colliding name) —
    **none** of the eleven edits an assertion to make it pass. Record named nodes,
    never pass/fail totals: the totals in this plan's review history predate the
    node-set changes this fold makes. Where a claim cannot be perturbed, this plan
    says so rather than implying coverage.
* **Doc updates that must land.** Hand-authored, one surface: the
  `unicode-line-separator` bullet in the `content_scan.py` module docstring
  (B3), landing in the same commit as the behaviour — and it must carry the
  acceptance-association clause and the block-form clause, because after B10 the
  docstring is the only place an adopter learns which markers work. No generated
  docs, no snippet-synced blocks. `CHANGELOG.md` is Chunk C, deferred and shared.
* **Examples / smoke checks required.** `python scripts/check_cairn.py` over the
  whole tree — the doc gate, **and after B2 it is the shipped scanner run against
  Cairn's own corpus, i.e. the artifact under test measuring the corpus.** It is
  therefore a smoke test of the detector and **not** the alarm-fatigue evidence;
  that evidence comes from the independent raw sweep specified in Chunk B, which
  must not import `content_scan`. `python bootstrap/security_check.py` — expected
  `PASS`; both edited-adjacent scanner files are in the release gate's scan set,
  established by executing `scan_targets()` (`bootstrap/security_check.py:63`).
  **N/A**: the runnable example gallery under `examples/` — this change touches
  nothing it demonstrates.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk and node that enforces it.**
  * *A raw `U+2028` or `U+2029` in scanned text produces at least one flag
    naming the code point.* Enforced by B5 in
    [`bootstrap/tests/test_content_scan.py`](../../bootstrap/tests/test_content_scan.py),
    perturbable by P-B1 and — per member — P-B2.
  * *That flag is suppressible only by a marker naming its own id.* The positive
    half is enforced by **B6a**, perturbable by P-B3. The negative half (a
    `unicode-zero-width` marker does not suppress it) is the dispatch regression
    and the security-critical assertion in this plan; it is enforced by **B6b** as
    a node of its own, perturbable **only** by the two-site P-B7 — P-B3 does not
    reach it, and a one-site P-B7 does not either.
  * *A `unicode-line-separator` hit is cleared **only** by an own-id marker that
    renders on the same display line as the separator it accepts; an acceptance
    separated from its payload by a separator — on the preceding file line, later
    on the same file line, or in `cairn-accept` / `cairn-accept-end` block form —
    is **refused**.* Folded from amendments A9 → A24, and the disposition of [E1]
    in the reviewer's first branch. Enforced by B9a / B9b / B9c over B10,
    perturbable by P-B8.
  * *No two test classes, and no two methods within a class, share a name in
    `bootstrap/tests/test_content_scan.py`.* Enforced by B11, perturbable by P-B9.
    The violation removes nodes from collection with no error and no warning, so
    the invariant is what stands between the two sibling plans and a silently
    shrinking suite.
  * *`_scan_unicode` yields its pattern id; no caller derives one from message
    text.* Enforced by Chunk A row A3, perturbable by P-A1 (shape) and P-A2
    (value). This is the invariant `content-scan-detectors` depends on and the
    reason the signature change is owned here.
  * *`unicode-zero-width` and `unicode-bidi` keep their exact current meaning,
    so existing suppressions and residual fingerprints stay valid.* Enforced by
    the pre-existing nodes at
    [`bootstrap/tests/test_content_scan.py`](../../bootstrap/tests/test_content_scan.py)
    staying green, and by the pre-change tuple capture in Chunk A's acceptance.
    P-A2 shows those nodes can fail.
  * *One separator flag per line; the flag names the first.* The Decision's
    declared limit. Enforced by B8, perturbable by P-B5.
  * *The scanner's own source carries no raw copy of a code point it detects.*
    Pre-existing invariant, widened by B4, perturbable by P-B6.
* **Public-path → test mapping.** `scan_text` is the public entry point this
  plan changes, and B5, B6a, B6b, B7, B8 and B9a–B9c exercise it **through its
  public path** with no stub of it anywhere. `scan_file` is unchanged and reaches
  the same code by delegation, covered by the pre-existing red-team fixture node.
  Two nodes deliberately do not go through the public path, and both are named as
  such rather than passed off as contract tests: **Chunk A row A3** touches the
  module-private `_scan_unicode`, because the thing being pinned *is* an internal
  signature a sibling plan must rebase onto; and **B11** has no runtime subject at
  all — its subject is `bootstrap/tests/test_content_scan.py`'s own AST.
  `_separator_accept_is_associable` (B10) is private and is **not** tested
  directly: every assertion about it is made through `scan_text`, so the contract
  under test is the observable suppression behaviour, not the helper's signature.
* **Failure modes.**
  * *Alarm fatigue.* → **Measured: 0 hits across the tracked corpus, re-derived
    at revision `ec57bf0`, `as_of 2026-08-05`. This plan states no denominator**
    (amendment A33, folded) — three were written for the same unchanged verdict and
    each was stale within a day. Re-measured as a Chunk B gate, by the independent
    raw sweep and not by `check_cairn`. If the re-measurement is non-zero, the
    plan's instruction is to stop and route it to the Maintainer.
  * *Marker collision (a benign suppression silences an injected header).* →
    **Closed** by Chunk A + B6b, and reproduced as an executed defect above
    rather than argued.
  * *An adopter with a legitimate word-processor paste finds their marker
    refused.* → **Open by design, and narrower than it looks** (amendment A24,
    folded). The working form is documented in the B3 docstring bullet — the marker
    goes **before** the separator on the same display line — and 0 tracked files
    exercise the rule today. If the refusal proves noisy in an adopter tree, that
    is a Maintainer question, not an inline widening of B10.
  * *Same-line masking (two separators, one flag).* → **Open by decision**, and
    now pinned rather than implicit (B8). `content-scan-detectors` [I3] disposes
    of the same behaviour for its own rules; if its resolution changes the
    convention, that is a shared follow-up, not a rider here.
  * *A legitimate producer emits a separator (a word-processor paste).* →
    **Open by design.** That is the tripwire working. The suppression path is
    per-id and reviewed, which is what the separate pattern id buys.
  * *The docstring contract entry drifts from the yielded id.* → **Open, no
    mechanical guard.** No test compares the docstring's bullet list to the id
    set the code can emit. Named as a known omission rather than implied.
  * *The sibling plan lands second and reintroduces the ternary.* → **Closed**
    by A3, which is exactly why A3 exists.
* **Edge cases handled.** A separator inside a `cairn-accept` marker's scope
  (amendments A8 → A23, folded) — line-scope is **file**-line scope, and `U+2028`
  is the first detected code point for which a file line and a display line differ.
  For every **pre-existing** pattern id that divergence is left exactly as it is
  (out of scope, and 0 tracked files can exercise it). For `unicode-line-separator`
  it is **closed**: B10 refuses an acceptance that does not render on the same
  display line as the separator it accepts. Measured, un-remedied build vs remedied
  build: marker-after-separator `[]` → `['unicode-line-separator']`;
  preceding-file-line marker `[]` → `['unicode-line-separator']`; marker before the
  separator on the same display line `[]` → `[]`. **The previous form of this
  bullet asserted the divergence was benign and the previous B9 pinned it — both
  are superseded; do not build the pin.**
  A separator at file index 0 (no BOM-style exemption applies; it flags, and it
  should — unlike `U+FEFF` there is no benign encoding role). A file with no
  trailing newline (`split("\n")` handles it; unchanged). Line numbering under a
  separator (measured above: `split("\n")` is unaffected, so reported line
  numbers stay physical).
* **Known omissions, stated rather than implied.** (a) No mechanical guard ties
  the docstring pattern-id list to the ids the code emits — the doc entry is
  enforced by review, not by test. An honest guard needs a `_PATTERN_IDS` registry
  constant in the shipped module to compare the docstring against, which is
  adopter-visible surface this Decision did not authorize; **its home is
  `content-scan-detectors`**, which adds two more ids and so doubles the drift
  surface, and it is named there rather than parked here. (b) The plan asserts
  **no** absolute suite figure and no collected-node count anywhere; every such
  predicate is a delta the implementing agent captures. (c) `Zs` space separators
  are untouched and remain a live Maintainer question on `byline-classification`.
  (d) Whether the per-line `break` convention should change at all is deferred
  to its own proposal; this plan only makes the current behaviour falsifiable.
  (e) No human has audited whether any *untracked* or generated artifact in an
  adopter tree carries these code points — the sweep is over Cairn's tracked
  corpus only. (f) **B11 sits in the file it judges**, so a duplicate of its own
  class name would silence it; the independent catcher is Chunk A's node-id-set
  capture, taken outside the tree. A guard covering all of `bootstrap/tests/`
  rather than one module is the better instrument and is **not** built here — it is
  outside this plan's two-file scope. (g) **The folded B9a–B9c / B10 refusal and
  the bounded-ceremony contract have had no post-fold External read.** The round-2
  External review asked for "a focused External confirmation of the folded B9/B10
  refusal and ceremony contract"; the Maintainer disposed of the round instead —
  *"Go ahead with implementation once you've revised these. I don't want another
  review round"* — so that confirmation is **dispositioned, not performed**, and
  this plan does not claim it as coverage.

## Verification

Run under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`,
Python 3.13.13). A different Python minor silently changes both the suite figure
and the UCD version behind any `unicodedata` cross-check.

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

**A correction to the slot above, because the trigger matters more than the
list.** The templated line "the same ones CI enforces" is boilerplate: **Cairn has
no CI.** The only automation installed in this repository is `tools/intent.py`'s
pre-commit intent-claim check and its post-commit auto-release hook, and neither
runs pytest or any checker. Every gate in this plan fires when a **person types
the command** — an implementing agent before committing, or a reviewer. Nothing
listed here is enforced by machinery on a push.

**Plan-specific gates, added here because this change touches those surfaces.**

* **The release security gate** — `python bootstrap/security_check.py`.
  `templates/modules/team-gated/content_scan.py` is a verbatim shipped `.py` and
  is inside the scan set. Expected `PASS`.
* **Bandit, file-scoped, while iterating** — `python -m bandit -q -f json
  templates/modules/team-gated/content_scan.py`. Expected `errors: []` and zero
  findings; measured on the prototype for this plan.
* **The alarm-fatigue re-measurement** — the raw sweep over `git ls-files` for
  `U+2028` / `U+2029`, by a script that reads the code points **literally and does
  not import `content_scan`**, recorded in the commit body as **the hit count and
  the date, with no denominator** (amendment A33, folded). Re-derived at revision
  `ec57bf0` (`as_of 2026-08-05`): **0 hits**. The `check_cairn` run is a different
  claim in the same neighbourhood and is **not** a substitute — after Chunk B it
  runs the edited scanner, so it measures the detector, not the corpus.
* **The behaviour-identity capture** — the pre-change `(line, pattern_id,
  message)` tuple list for the five-probe fixture, written to the session
  scratch directory **before** Chunk A and diffed after. It cannot be reconstructed
  afterwards: the only source of the pre-change tuples is the pre-change scanner.
* **The node-id-set capture** — `--collect-only -q` over
  `bootstrap/tests/test_content_scan.py` before and after, stored outside the tree.
  The predicate is a strict superset of node ids, not a count.
* **The perturbation ledgers** — **eleven** of them (P-A1, P-A2, P-B1…P-B9), per
  chunk, in the commit body: the change made, the **named nodes** observed red and
  the named nodes observed green, and the byte-identical restore verified by an
  empty `git diff <path>` (or `git status --short` clean for the two transient
  ones). **Record named nodes, not pass/fail totals** — the totals in this plan's
  review history were measured against a node set this fold has changed.
* **The gate-integrity note** — after Chunk B, record in the commit body that
  `templates/modules/team-gated/content_scan.py` and
  `bootstrap/tests/test_content_scan.py` now differ from their pinned sha256 in
  `bootstrap/tests/fixtures/gate_manifest.json`, so a later
  `_gate_manifest.py verify` reports **these two files among its**
  `FROZEN-MODIFIED` entries — the **same two** `content-scan-detectors` will
  report. **Name the two files; state no total** (amendment A14, folded): the total
  is other workflows' to move and is stale by the time it is read. Do not re-pin;
  see [*Maintainer fence*](#maintainer-fence), whose F2 bounding condition now
  gates the shared ceremony.

**Note on doc gates**: drift gates catch **drift**, not **absence** of a new doc
update. `check_cairn` will not notice if B3's docstring bullet is never written —
nor its acceptance-association and block-form clauses, which are the adopter-visible
half of the [E1] refusal. Confirm by reading. And do not let the one command stand
for two claims: `check_cairn` is the doc gate, and after Chunk B it is also the
edited scanner running over Cairn's corpus. **The artifact under verification may
not supply the material** — the alarm-fatigue evidence comes from the independent
raw sweep above, never from this command.

## Plan review — the brief

**Declared tier: `required(External, security lens)`**, carried from the proposal
header and re-declared by the Decision's *Next transition* line.

**The Internal round about to run does not discharge it.** Cairn's floor for
Internal is the same agent type in a fresh session; the floor for External is a
**different agent type, or a human**. The declared tier names External with a
security lens, so an Internal round — however sharp — leaves the requirement
open. Stated plainly so it is not discovered at archive time:

* **What the Internal round is for**: sharpening. The chunk boundary, the
  perturbation set, whether P-B2 and P-B4 really discriminate what they claim,
  whether the docstring-drift omission deserves a mechanical guard, and whether
  the batch rule in *Maintainer fence* is the right way to spend one ceremony.
* **What is still owed before any implementation commit**: an **External**
  security-lens review appended to this plan. `doctrine/plans.md`'s plan-review
  precondition binds — a review-required plan does not start implementation
  until its plan-review section has landed.
* **What an External reviewer should attack first**, in order: (1) re-run the
  494-file alarm-fatigue sweep, because it is the one measurement that can
  invalidate the whole rule; (2) reproduce the NAIVE-vs-FIXED marker table,
  because it is the argument for spending a signature change; (3) challenge P-B3
  specifically — it is the only perturbation that requires *reverting a landed
  chunk*, which is the most awkward one to actually run and therefore the most
  likely to be waved through.

## Code review

*Filled in after implementation commits land.* See `doctrine/plans.md` >
"Code review" for the full doctrine: falsification ledger, coverage line,
reviewer identity (not the implementing agent), and the append-only rule.

## Lasting-truth migration

*Pre-declared here at plan-open; completed at archive time.* Per the
[Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
this plan archives only after every deferred follow-up has a durable home
outside it. The homes are named now so none of them ends its life as a sentence
in an archived plan.

| Deferred item | Durable home | Written by |
|---|---|---|
| The adopter-facing pattern-id contract (that `unicode-line-separator` exists, what it covers, that it flags and never rewrites) | The `content_scan.py` module-docstring bullet list — the file shipped verbatim to adopters | Chunk B (B3), at implementation |
| The **declared limit** (one separator flag per line; the flag names the first) | Two homes, deliberately: the same docstring bullet, and the executable pin at B8 | Chunk B (B3 + B8) |
| The `_scan_unicode` yielded-id contract that `content-scan-detectors` must rebase onto | The test A3 — a guard, not a promise, which is the form the Decision asked for | Chunk A (A3) |
| The release note | `CHANGELOG.md > Unreleased > Added`, **one shared line** with `content-scan-detectors` | Chunk C, at a serialization point |
| The frozen-file re-pin obligation (two `FROZEN-MODIFIED` entries, batched with the sibling) | The final commit body, then `bootstrap/tests/fixtures/gate_manifest.json` itself once the Maintainer re-produces it | Implementing agent records; Maintainer discharges |
| Whether the per-line `break` convention should change at all | Its **own proposal**, not this plan and not a rider. B8 is what makes the current behaviour falsifiable so the future proposal has something to argue against | Not this plan |
| `Zs` space separators | The open Maintainer question on `byline-classification` | Not this plan |
| The docstring-vs-emitted-id drift gap (no mechanical guard) | Recorded as a known omission in *Author-accounting* above; if it recurs, the `incident-trackers` module is its home, not a new test bolted on at archive time | This plan, above |
| The evidence ledger (measurements, perturbation results, the corpus sweep) | The commit bodies and the `## Code review` section of this plan | Implementing agent, then the reviewer |
| The display-line association rule for `unicode-line-separator` acceptances — an acceptance is honoured only when it renders on the same display line as the separator it accepts, and the block form does not suppress it | The B9a / B9b / B9c pins plus the B3 docstring clause | Chunk B (B3 + B9a–B9c + B10) |

This section is append-only once written. The final row was **appended** under that
rule as the residue of amendment A24; no prior entry was edited.

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-04

**Model**: claude-opus-5.

**Standing.** I am the **same agent type as the plan's author**, in a fresh
session. That is Cairn's *Internal* floor and nothing more: there is **no
cross-type structural independence** here, so a blind spot the author has I
most likely share -- in particular any assumption about what a generator
signature or a suppression grammar "obviously" means, since that is exactly
the shape of reasoning both of us produce the same way. **This round does not
discharge the declared `required(External, security lens)` tier.** The plan's
own *Plan review -- the brief* says so, and I confirm that self-assessment is
correct rather than merely restating it: an External security-lens section is
still owed before any implementation commit. Everything below was re-measured
against the working tree at HEAD `eacb7dd` under
`~/conda_envs/lhm/bin/python3.13` (3.13.13); where I reconstructed the proposed
change I say so, and **no repository file was modified** -- all variants live
in the session scratch directory.

**Steelman.** This is the strongest plan I have reviewed in this tree on the
axis that matters most for a security control: it *executes* its central
argument instead of asserting it. The NAIVE-vs-FIXED marker table is the whole
case for spending a signature change, and it is a table of real scanner output,
not a narrative. The alarm-fatigue sweep is taken as the dated figure the
proposal demanded, with an explicit instruction to re-take it rather than quote
it. The `split("\n")`-vs-`splitlines()` discovery is a genuinely new fact that
*narrows* the change's claimed blast radius -- an author-adverse finding
volunteered rather than buried. Chunk ordering is justified by naming the exact
intermediate commit that would itself be the defect. The perturbation set edits
production code and never an assertion, which is the discipline most plans get
backwards. And the known-omissions list names the docstring-drift gap the plan
could have quietly implied coverage of. My concerns below are almost entirely
about the *ledger mechanics* of three perturbations and one acceptance
predicate -- not about the design, which I think is right.

### Concerns

**[I1] P-B3 does not exercise the assertion it is named for, and B6's negative
half -- the dispatch regression itself -- has no perturbation.** MEASURED, on
my reconstruction. Under the NAIVE state P-B3 specifies (Chunk A reverted,
the B2 loop kept), a single-node B6 fails at its **first** assertion, the
*positive* half: in NAIVE the separator flag is labelled `unicode-zero-width`,
so a `cairn-accept: unicode-line-separator` marker matches nothing and the
own-id half fails first. Observed:

```
E  AssertionError: own-id marker must clear
E  assert ['unicode-zero-width'] == []
```

The node aborts there; the `unicode-zero-width`-marker half **never executes**.
So the plan's stated observation ("B6's `unicode-zero-width`-marker half
fails") is not what an implementer will record -- and the real cost is that
**no specified perturbation shows B6's negative half is non-vacuous**. That
half is the security-critical assertion in the entire plan: a foreign marker
must not silence a separator flag. Ask: split B6 into two nodes (own-id
suppresses / foreign-id does not), so P-B3 reports both cleanly; and add the
one perturbation that fails the negative half *alone* -- widen the final
filter in `scan_text` to ignore `pattern_id` (i.e. suppress by line only).

**[I2] P-B2's "repeat the other way round" direction does not produce the
claimed observation.** MEASURED, both directions:

| perturbation | result | B5 fails at |
|---|---|---|
| remove U+2029, keep U+2028 | **1 failed, 4 passed** | the U+2029 assertion, after the U+2028 assertion passed |
| remove U+2028, keep U+2029 | **4 failed, 1 passed** | the **U+2028** assertion -- the U+2029 assertion is never reached; B6, B7 and B8 fail too (all use U+2028 fixtures) |

So "B5's assertion fails *alone* while the other stays green" is true in one
direction and false in the other, and the reverse direction produces no
per-member evidence at all. Same structural cause as [I1]: a multi-assertion
node cannot support a per-assertion perturbation claim. Ask: parametrize B5
over the two code points so it is two nodes; then both directions are
symmetric and the per-member claim is actually demonstrated.

**[I3] The new detector is self-suppressible on its own physical line, and the
plan asserts that is benign without measuring it.** MEASURED against my
reconstruction of the fixed scanner:

```
control:  "## Status: open" +U+2028+ "## Injected header"        -> ['unicode-line-separator']
+ marker: ... + ' <!-- cairn-accept: unicode-line-separator
                     reason="pasted from Word" reviewer="x" date=... -->'  -> []
that string: split("\n") -> 1 line ;  splitlines() -> 2 lines
```

`_parse_suppressions` iterates the same `split("\n")` lines
(`templates/modules/team-gated/content_scan.py:255`, line-scope written at
`:261` as `{i, i + 1}`). So a payload and its own suppression marker share one
**suppression** line while occupying two **display** lines in any renderer that
honours U+2028. The plan's edge-case bullet -- "A separator inside a
`cairn-accept` marker's own line (line-scope covers the marker's own line --
pre-existing semantics, unchanged)" -- is true of the *code* and false of the
*security property*: for zero-width and bidi the marker and the payload also
share a display line, whereas U+2028 is the **first detected code point that
makes the display/file line relationship diverge**, which is the entire premise
of the rule. The plan follows its own headline `split("\n")`-vs-`splitlines()`
measurement into line *numbering* and stops before the *suppression grammar*.
The `{i, i + 1}` preceding-line scope compounds it: a marker written to
annotate what a reviewer sees as the next display line can clear a hit that is
several display lines away. Ask: give this the B8 treatment -- pin it with a
node so it is a *declared* limit a future author must argue against, and say so
in the B3 docstring bullet -- or record an explicit disposition. I am not
asking for a behaviour change here; I am asking that the one interaction
between the new code point and the suppression grammar not be the single
unmeasured assertion in an otherwise fully-executed plan.

**[I4] "The whole suite green, 0 failed / 0 skipped / 0 xfailed" is not
achievable in the tree this plan was written against.** MEASURED --
`~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` at HEAD `eacb7dd`
with the current working tree: **3 failed, 1746 passed, 0 skipped, 0 xfailed,
162s**. The three are, in `bootstrap/tests/test_ast_attest.py`, the nodes
`test_committed_baseline_accounted_for_across_the_engine_package` and
`test_ast_gate_passes_over_the_full_scaffold_module_set`; and in
`bootstrap/tests/test_scaffold.py`, the node
`TestMinimalYamlParse::test_mixed_indent_list`
-- all from other workflows' in-flight `bootstrap/_scaffold/` edits, none
reachable from this plan's two files. The plan anticipated the dirty tree for
the *figure* ("take the baseline at implementation start") but states the
*predicate* absolutely. As written the gate is either unachievable or waived by
judgement -- which is precisely the failure mode the rest of the plan works
hard to design out. Ask: restate it as a delta -- no failure absent from the
implementation-start baseline, and no node dropped from collection.

**[I5] F2's "the same two entries" is already false, and the ceremony's blast
radius is wider than the batch rule describes.** MEASURED --
`~/conda_envs/lhm/bin/python3.13 bootstrap/tests/_gate_manifest.py verify` on
the current tree already reports **six** `FROZEN-MODIFIED` entries
(`bootstrap/tests/test_quality_gate_redundancy.py`,
`bootstrap/tests/test_security_check.py`,
`bootstrap/tests/test_security_lint.py`,
`bootstrap/tests/test_verify_integrity.py`, `bootstrap/verify_integrity.py`,
`scripts/quality_gate.py`), plus 2 `COLLECTION-DROPPED` and 4
`SKIP-XFAIL-NEW` -- none of them this plan's. So the commit-body sentence the
plan mandates ("a later `_gate_manifest.py verify` reports two
`FROZEN-MODIFIED` entries") will be **false when written**, and "one supervised
re-produce after both have landed" re-anchors *everything* stale at that
moment, not the pair. Partial mitigation exists and is worth recording:
`bootstrap/tests/_gate_preflight.py:784`-`790` HOLDs on uncommitted tracked
changes, so the ceremony refuses a dirty tree -- but it does not refuse other
workflows' *committed* frozen-file edits, and
`bootstrap/REANCHOR_RUNBOOK.md:10`-`11` forbids the implementer performing
Phase 0 precisely because a re-anchor is an authority act. Ask: have the commit
body name the two files **this change** makes stale and state plainly that the
verify output will contain others; and make F2 say the ceremony is scoped to
whatever is stale at ceremony time -- a Maintainer review item -- rather than
to this pair.

**[I6] (low) The "exactly two files" scope check used a method that could not
have found the third coupling.** The plan establishes its two-file scope with
`grep -rln "unicode-zero-width"`; I re-ran it and it returns exactly
`templates/modules/team-gated/content_scan.py` and
`bootstrap/tests/test_content_scan.py`, `as_of 2026-08-04` -- the plan's figure
is right. But `templates/modules/team-gated/content_scan_runner.py` is coupled
to the id set **without naming any id**: it builds the reviewed-residual key as
`f"{rel}:{pattern_id}:{code_hash}"` (`:299`, used at `:403`). A literal-id grep
structurally cannot see that. The conclusion still holds -- 0 separator flags
in today's corpus and Chunk A is id-preserving, so no residual baseline churns
-- but it should be reached by an argument about the fingerprint, not by a grep
that cannot cover it. This is the plan's own "verified rather than assumed"
standard turned on the plan.

**[I7] (low) B4 widens the hygiene set but the guard reads only one of the two
files it now matters for.** `test_no_raw_banned_codepoints_in_source` reads
`CONTENT_SCAN_SRC` only (`bootstrap/tests/test_content_scan.py:65`); it does
not scan the test module. After B5-B8 land, `test_content_scan.py` is itself a
file whose fixtures are separator code points, and B5's "escape forms in the
test source, matching B4" is a convention with nothing enforcing it. One extra
line in that node (scan both paths) closes it.

### Covered

Re-measured, not accepted:

* **Every cited line number is exact.** `content_scan.py`: `:295`
  (`def _scan_unicode`), `:390` (`lines = text.split("\n")`), `:401`-`403`
  (call site), `:402` (the ternary, character-for-character as the plan and the
  Decision quote it), `:40`/`:43`-`45` (the `unicode-zero-width` and
  `unicode-bidi` docstring bullets, the latter ending at 45), `:137`
  (`_ZERO_WIDTH = {`), `:144` (`_BIDI = (`). `test_content_scan.py:48`-`52` is
  exactly the `_BANNED_CODEPOINTS` block, and 0x2028/0x2029 are confirmed
  **absent** from it today ({0x200B-0x200F, 0x2060, 0xFEFF} | 0x202A-0x202E |
  0x2066-0x2069) -- so P-B6 is sound: the widening, not the pre-existing set,
  is what would catch an injected raw separator.
  `bootstrap/tests/_gate_manifest.py:165`-`167` is the frozen-glob tuple with
  `templates/modules/**/*.py` on 167. `scripts/check_cairn.py:91`-`94` is
  `_CONTENT_SCAN_SRC`, loaded by path -- the no-twin claim holds.
* **Every figure.** 494 tracked files (independent sweep: all 494 decode as
  UTF-8, **0** carry a raw U+2028 or U+2029, `as_of 2026-08-04` -- the
  stop-signal did not fire, confirmed independently). 25 collected nodes in
  `test_content_scan.py`. 164 `frozen_files` entries, both target files
  present. Whole-tree `check_cairn` -> **180 Markdown files, no issues**, 68
  external links not probed. `quality_gate.py --sub neutrality` -> **fail=95**,
  info=21.
* **The NAIVE/FIXED marker table reproduces, all eight rows**, against my own
  reconstruction of the two variants (not the author's code): HEAD flags
  nothing; NAIVE mislabels both separators `unicode-zero-width`, is silently
  cleared by a zero-width marker, and ignores the promised separator marker;
  FIXED labels both `unicode-line-separator`, is *not* cleared by the
  zero-width marker, and *is* cleared by its own. The Decision's defect is real
  and the signature change is the right precondition.
* **The refactor is behaviour-preserving.** I repointed the *real* 25-node
  `bootstrap/tests/test_content_scan.py` at my reconstructed FIXED build and at
  an A-only build: **24 passed, 1 deselected** in both cases, matching the
  author's figure and each other. The deselected node is the verbatim-install
  comparison, correctly excluded and correctly flagged as owed for real at
  implementation.
* **P-A1** -- confirmed: NAIVE raises `ValueError` on the 3-tuple unpack.
* **P-A2** -- confirmed, and **under-reported in the safe direction**: swapping
  the two literals fails not two but **six** pre-existing nodes
  (`test_scanner_still_detects_after_escaping`,
  `test_malicious_fixture_is_caught`, `test_zero_width_caught`,
  `test_bidi_control_caught`, `test_expanded_unicode_controls_caught`,
  `test_non_leading_bom_flagged`).
* **P-B1** -- confirmed; also under-reported in the safe direction (B6 fails
  too, which the plan does not claim).
* **P-B4** -- confirmed **exactly as argued**, which is the sharpest
  perturbation in the set. The wrong-id variant yields three flags,
  `{(1,'unicode-zero-width'), (2,'unicode-bidi'), (3,'unicode-zero-width')}`:
  a hypothetical "three flags appeared" test passes, and B7's exact-set
  assertion fails. That is precisely the discrimination the plan claims.
* **P-B5** -- confirmed exactly: removing the `break` gives
  `assert 2 == 1` with both separator flags on line 1; **1 failed, 4 passed**.
  The cleanest perturbation in the plan.
* **Scope holds against the Decision.** I read the Decision. The signature
  change is assigned here; the coexistence test is required of both plans; the
  per-line limit is declared there. Nothing in the plan absorbs
  `content-scan-detectors`' surface, the parser's, or `agent-context-scrub`'s.
  B4 and B8 are additions beyond the Decision's literal text, but both are
  pinning/hygiene rather than behaviour, and B4 is explicitly fenced to exactly
  two entries.
* **Self-verification hunt.** The plan already closes the one that would have
  mattered most -- Chunk A's behaviour-identity baseline must come from a
  pre-change execution, stated in those words -- and already notes that
  `check_cairn` doubles as doc gate and alarm-fatigue measurement, "a different
  claim in the same command". I found no case of the artifact supplying its own
  oracle. B5's message oracle (`"U+2028"` typed by a human) is independent of
  `_LINE_SEPARATORS`, since the message is computed via `ord(ch)`; a wrong
  constant member produces a wrong message and B5 fails.
* **Required checkers, both clean.**
  `claim_check.py dev/plans/separator-detection.md` -> "OK, no claim-check
  flags"; `check_cairn.py dev/plans/separator-detection.md` -> "OK -- 1
  Markdown file(s) scanned; no issues".

**Direct answers to the three questions the brief poses to this round.**
(1) *Chunk boundary* -- correct and necessary; the A-only build is
behaviour-identical (24/24) so A-before-B costs nothing and B-before-A is the
defect. (2) *Do P-B2 and P-B4 discriminate what they claim* -- P-B4 yes,
exactly; P-B2 in one direction only, see [I2]. (3) *Does the docstring-drift
omission deserve a mechanical guard* -- **not in this plan.** An honest guard
needs a `_PATTERN_IDS` registry constant in the shipped module to compare the
docstring against, which adds adopter-visible surface this Decision did not
authorize. But do not leave it as a bare "known omission": its right home is
`content-scan-detectors`, which adds two more ids and so doubles the drift
surface, and the plan should say that rather than parking it. (4) *Is the batch
rule the right way to spend one ceremony* -- the idea is right, the accounting
is not; see [I5].

### Not covered / low confidence

* **The External tier is not discharged.** Same agent type; no cross-type
  independence. Anything the author and I both find natural about generator
  signatures, suppression grammars, or what "line" means is unexamined by this
  round *by construction*.
* **My variants are a reconstruction, not the author's code.** Every "MEASURED"
  claim above about post-change behaviour was taken against scratch builds I
  wrote from the plan's prose, and against my own reconstruction of nodes
  A3/B5-B8. Where the implementer writes those nodes differently -- especially
  if they split them per [I1]/[I2] -- my failure-site observations change. The
  pre-change measurements (line numbers, figures, HEAD behaviour, the 3-failure
  suite baseline, the six `FROZEN-MODIFIED` entries) are against the real tree
  and do not carry that caveat.
* **I did not run `bootstrap/security_check.py` or Bandit** over a real edit;
  the plan's own figures there are prototype figures and it says so.
* **Node-name collision between the two plans, unresolved and untested.** Both
  plans must carry the coexistence test. If both write
  `TestLineSeparator::test_all_three_unicode_ids_trip_independently` into the
  same file, Python silently keeps the last definition -- no error, no warning,
  one collected node. I did not construct this case, so I am not raising it as
  a finding, but the plan names no convention for the shared node's identity
  and "collection grows by exactly the new nodes" would not detect it.
* **The 494 figure moves before implementation.** This plan and its siblings
  are untracked today; committing them raises the denominator. Immaterial to
  the verdict, and the plan already instructs a re-take.
* **Adopter-tree impact is unmeasured by anyone**, as the plan's omission (e)
  says. The sweep is Cairn's tracked corpus only.

### Recommendation

**Revise, then send to External -- do not send as-is.** The design is sound and
I found nothing wrong with it; [I1], [I2] and [I4] are cheap edits to *this
document* (split two test nodes into four, restate one acceptance predicate as
a delta) and fixing them first means the External security reviewer spends
their independent read on the two questions that actually need cross-type
independence -- **[I3]**, whether the separator's interaction with the
line-scoped suppression grammar needs a pin or a disposition, and **[I5]**,
whether one supervised re-pin ceremony can honestly be described as covering
"the same two entries". I would also ask the External reviewer to keep the
plan's own attack order, with one substitution: item (3) of its brief,
"challenge P-B3", is now *known* to be mis-specified -- the useful version is
to check that the revised B6 split makes the negative half independently
falsifiable, which is the assertion the whole Decision exists to protect.

**No implementation commit before the External section lands** -- unchanged,
and this round does not move that line.

## Response to plan review -- Claude (author) -- 2026-08-04

**Model**: claude-opus-5. **Standing**: plan author, dispositioning the Internal
plan review appended above.

**Method, and the one rule that governed it.** The review was written against
HEAD `eacb7dd`; this Response is written against HEAD `6618e54`. I re-derived
**every** figure the review and the plan state against the live tree under
`~/conda_envs/lhm/bin/python3.13` (3.13.13, UCD 15.1.0) rather than inheriting
any of them, and I reconstructed the NAIVE / FIXED / A-only / per-member /
wrong-id / no-break / line-only-suppression variants from the real
`templates/modules/team-gated/content_scan.py` in the session scratch
directory. **No repository file outside this plan was modified.** Where a
figure moved, it is reported below as plainly as where it held -- four of them
moved, and two of those are load-bearing.

One method note that changed an answer. The plan asserts
`templates/modules/team-gated/content_scan.py` is "inside the scan set" of
`bootstrap/security_check.py`. `grep -n "content_scan" bootstrap/security_check.py`
returns **nothing** -- the file is never named. Executing the call path instead
(`scan_targets()`, defined at `bootstrap/security_check.py:63`, which walks the
module specs rather than a literal list) returns **74 targets** and both
`templates/modules/team-gated/content_scan.py` and
`templates/modules/team-gated/content_scan_runner.py` are in it. **The plan's
claim is correct and the grep would have falsified it wrongly.** I record this
because it is the same failure mode as [I6], committed by me while checking
that very finding -- a name-matching probe cannot see a set built by
construction.

### Re-measurement ledger

**Reproduced exactly** (plan figures unless marked):

| Figure | Source | Live result |
|---|---|---|
| `U+2028` cat=Zl / `U+2029` cat=Zp, `White_Space=Yes`, **0 flags** at HEAD | plan | reproduces; UCD 15.1.0 |
| `splitlines()` 5 / `split("\n")` 4 on the header fixture | plan | reproduces **only with a trailing newline**; without one it is 5 / 3. The claim it supports -- `splitlines()` sees more lines, so a separator does not shift reported line numbers -- holds either way |
| NAIVE-vs-FIXED marker table, **all eight rows** | plan | reproduces, row for row, against my own reconstruction |
| `FIXED tri-fixture` / `HEAD tri-fixture` | plan | reproduces |
| `FIXED two-sep line` -> one flag naming `U+2028` | plan | reproduces |
| `24 passed, 1 deselected` repointing the real test module at FIXED | plan | reproduces; **and at the A-only build**, also 24/1 |
| Five-probe behaviour identity (`U+202E`, `U+200B`, `U+2060`, leading/non-leading BOM) | plan | reproduces on the full `(line, pattern_id, message)` tuple, not just id sets: HEAD == A-only == FIXED |
| Bandit over the FIXED prototype: `errors: []`, zero findings | plan | reproduces; 0 at every severity, 354 loc |
| **25** collected nodes in `bootstrap/tests/test_content_scan.py` | plan | reproduces, and all 25 pass at HEAD |
| **164** `frozen_files` entries; both target files present | plan | reproduces |
| `grep -rln "unicode-zero-width"` -> exactly the two files | plan / [I6] | reproduces |
| `quality_gate.py --sub neutrality` -> `fail=95` | plan / review | reproduces (`info=21`) |
| Every cited line number in `content_scan.py`, `test_content_scan.py:48`-`52` and `:65`, `_gate_manifest.py:165`-`167`, `check_cairn.py:91`-`94` | review "Covered" | **all reproduce**, character-for-character where quoted |
| `content_scan_runner.py:299` fingerprint, used at `:403` | [I6] | reproduces |
| `_gate_preflight.py` refuses on uncommitted tracked changes; `REANCHOR_RUNBOOK.md:10`-`11` forbids the implementer running Phase 0 | [I5] | reproduce (the report level is literally `"refuse"`, which is blocking) |
| P-A1 -> `ValueError: not enough values to unpack (expected 3, got 2)` | review | reproduces, given A3 written as an unpack (as the plan specifies) |
| P-B1 -> B5, B6, B7, B8 fail; A3 passes | review | reproduces, including the B6 failure the **plan** does not claim |
| P-B5 -> B8 alone; **1 failed, 4 passed** | review | reproduces exactly |
| P-B4 wrong-id flag set `{(1,'unicode-zero-width'), (2,'unicode-bidi'), (3,'unicode-zero-width')}`, 3 flags | review | reproduces exactly; the discrimination claim holds |
| [I1] failure text, verbatim | review | reproduces **character-for-character**: `AssertionError: own-id marker must clear` / `assert ['unicode-zero-width'] == []` |
| [I2] both directions: 1 failed/4 passed and 4 failed/1 passed | review | reproduces exactly, including that the reverse direction fails B5 at its *`U+2028`* assertion so the `U+2029` assertion is never reached |
| [I3] control -> `['unicode-line-separator']`, +marker -> `[]`, `split("\n")` 1 / `splitlines()` 2 | review | reproduces exactly |

**Did not reproduce** -- reported as findings, not inconveniences:

1. **The corpus sweep denominator moved: 494 -> 511.** Live:
   511 tracked files listed, 511 decode as UTF-8, **0 carry a raw `U+2028` or
   `U+2029`**, `as_of 2026-08-04`. The verdict is unchanged and the rule still
   ships silent; only the denominator grew, exactly as the review predicted
   under *Not covered*. The plan's three copies of "494" are stale.

2. **[I4] does not reproduce, and its remedy is still right.** The review
   measured "3 failed, 1746 passed". Live:
   `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` -> **1790
   passed, 0 failed, 0 skipped, 0 xfailed, 178s**. The three named failures are
   gone -- the other workflows' `bootstrap/_scaffold/` edits have landed. So
   the plan's absolute suite predicate **is** achievable at this instant, and
   the review's stated reason for restating it has evaporated. The *structural*
   objection survives intact, because a **different** absolute predicate in the
   same plan is unachievable right now (below).

3. **A gate the review passed as clean is now red, and the plan makes it an
   acceptance criterion.** The review recorded "Whole-tree `check_cairn` ->
   **180 Markdown files, no issues**". Live: `scripts/check_cairn.py` reports
   **2 issue(s) across 195 file(s)** -- both in `dev/PLANNING.md:886`-`887`,
   introduced by commit `4573c11` (the six-plan follow-up census), neither
   reachable from this plan's two files. The plan's Chunk B criterion
   "`scripts/check_cairn.py` -> OK" is therefore **not achievable today** by an
   implementing agent who touches only `content_scan.py` and
   `test_content_scan.py`. This is [I4]'s hazard, relocated: the review found
   the right disease on the wrong organ.

4. **[I5]'s figures understate the drift by 4.** The review reported "six
   `FROZEN-MODIFIED` ... plus 2 `COLLECTION-DROPPED` and 4 `SKIP-XFAIL-NEW`".
   Live `bootstrap/tests/_gate_manifest.py verify` -> **HOLD, 17 gate-integrity
   violations**: **10** `FROZEN-MODIFIED` (the review's six, plus
   `bootstrap/security_check.py`, `bootstrap/tests/test_lifecycle_contract.py`,
   `bootstrap/tests/test_lockfile_module.py`,
   `bootstrap/tests/test_scaffold.py`), **3** `COLLECTION-DROPPED`, **4**
   `SKIP-XFAIL-NEW`. The finding is **strengthened**, not weakened: the
   mandated commit-body sentence would be even more false than the review said,
   and the "one supervised re-produce" is a larger authority act than F2
   describes. The right fix is to stop quoting a count at all.

5. **P-A2's blast radius is 5 pre-existing nodes, not 6.** The review lists
   `test_malicious_fixture_is_caught` among the six. Live, on both the A-only
   and the FIXED build, the swap fails **5**:
   `test_scanner_still_detects_after_escaping`, `test_zero_width_caught`,
   `test_bidi_control_caught`, `test_expanded_unicode_controls_caught`,
   `test_non_leading_bom_flagged`. `test_malicious_fixture_is_caught`
   **cannot** fail under that perturbation -- it asserts only
   `imperative-override`, `egress`, `suspicious-url` and
   `instruction-html-comment` (`bootstrap/tests/test_content_scan.py:115`-`121`),
   naming no unicode id. The three files involved are byte-identical to
   `eacb7dd`, so this is a mis-attribution in the review, not tree drift. The
   plan's own claim (2 nodes) remains true-but-under-reported; nothing in the
   plan needs to change, and no perturbation ledger should carry "6".

6. **P-B4's blast radius is 3 nodes, not 1.** The review calls P-B4 "confirmed
   **exactly as argued**". Live, the wrong-id variant fails B5 and B6 as well
   as B7. The *discrimination* claim -- B7's exact-set assertion fails where a
   count-only test would pass -- is confirmed exactly (3 flags, the set above).
   The plan's P-B4 text under-reports in the safe direction; recorded, no
   amendment needed.

### Dispositions

**[I1] -- ACCEPTED.** Reproduced verbatim, including the quoted failure text.
Under the P-B3 state a single-node B6 aborts at its *positive* assertion, so
the plan's stated observation is wrong and -- the part that actually matters --
**no perturbation in the plan shows B6's negative half is non-vacuous**, and
that half is the security-critical assertion in the whole plan. I went further
than confirming the finding: I **ran the remedy the review only proposed**.
Widening the final filter at
`templates/modules/team-gated/content_scan.py:409` to suppress by line while
ignoring `pattern_id` fails the negative half **alone** -- 1 failed, 4 passed,
failing at the `foreign marker must NOT clear` assertion and nowhere else. It
is a real, runnable, isolating perturbation. Residue: **A1-A3** below (B6
split; new P-B7; invariant row rewritten).

**[I2] -- ACCEPTED.** Reproduced in both directions, exactly. Residue: **A4-A5**
(B5 parametrized into two nodes; P-B2 restated).

**[I3] -- ACCEPTED WITH MODIFICATION.** Reproduced exactly, and I extended it
one step, which changed my disposition from "record it" to "pin it". The review
measured the same-line case (marker and payload sharing one file line, two
display lines). I also measured the `{i, i + 1}` preceding-line scope
(`templates/modules/team-gated/content_scan.py:261`) across a
separator-inflated line: a marker on **file line 1** clears a
`unicode-line-separator` hit on **file line 2** that occupies **4 display
lines** -- measured 2 file lines, 5 display lines, flags `[]` with the marker
and `['unicode-line-separator']` without it. So a reviewer who writes a marker
believing it annotates "the line just below" can clear an injected header
several display lines away. The review offered "pin it **or** record a
disposition"; I take the pin, because an unpinned disposition in a security
control is the thing this plan exists to stop doing. Residue: **A6-A9** (new
node B9, new perturbation P-B8, B3 docstring clause, edge-case bullet
superseded, new invariant, new lasting-truth row).

**[I4] -- ACCEPTED WITH MODIFICATION.** The remedy is right; the evidence is
stale and I am replacing it rather than repeating it. The suite predicate is
achievable today (1790/0/0/0), so I do **not** restate the finding's premise as
the review wrote it. But the identical defect is live on the `check_cairn`
predicate, which fails today for reasons no implementer of this plan can fix.
Both predicates become deltas against an implementation-start baseline.
Residue: **A10-A12**.

**[I5] -- ACCEPTED**, with the figure corrected and, more importantly, deleted
rather than updated. Any count I write here is stale by the time it is read --
that is the finding. Residue: **A13-A14** (F2 bullets and the gate-integrity
note both stop asserting "two" as the total).

**[I6] -- ACCEPTED.** The fingerprint coupling is real and confirmed at
`templates/modules/team-gated/content_scan_runner.py:299`, consumed at `:403`;
the runner is additionally in `security_check.py`'s scan set and in
`frozen_files`, so it is a live surface, merely one this plan does not edit.
The conclusion holds and now rests on an argument about the fingerprint rather
than on a grep. Residue: **A15**.

**[I7] -- ACCEPTED.** Confirmed: the guard reads `CONTENT_SCAN_SRC` only
(`bootstrap/tests/test_content_scan.py:65`), so B5's "escape forms in the test
source" is a convention with nothing enforcing it. Verified the widening is
what does the work: with a raw `U+2028` planted in a source comment, the
**pre-existing** `_BANNED_CODEPOINTS` reports no hits and the **widened** set
reports `0x2028`. Residue: **A16**.

**[R1] -- NEW, raised by this Response, promoted from the review's "Not
covered".** The review flagged the node-name collision between the two plans
but explicitly declined to raise it as a finding ("I did not construct this
case"). I constructed it, and it is worse than the review guessed. A second
`class TestLineSeparator` in the same module does not merely collapse the one
shared node -- **it shadows the entire first class**. Measured: a module with a
5-method `TestLineSeparator` followed by a 1-method `TestLineSeparator`
collects **1 test**, silently, with no error and no warning. If
`content-scan-detectors` lands second and writes its own `class
TestLineSeparator` holding only the coexistence node, **B5, B6, B7 and B8
vanish from collection** and the suite stays green. The plan's guard against
this -- "collection grows by exactly the new nodes" -- is a count check on a
tree that has just lost nodes, and the plan names no convention for the shared
node's identity. Residue: **A17-A18**.

### Amendments in force

Every row below is a mechanical change to this plan. Rows marked *(added)*
introduce text where none stood; all others quote the superseded text verbatim.

| # | Superseded text (verbatim) | Replaced by | Folded into (2026-08-05) |
|---|---|---|---|
| A1 | Chunk B row **B6**, verbatim: `New TestLineSeparator::test_marker_suppresses_only_its_own_id: a cairn-accept marker naming unicode-line-separator clears the flag; a marker naming unicode-zero-width does **not**. The second half is the regression for the dispatch defect — it is red against the code at HEAD and red against any future reintroduction of the ternary.` | **Two nodes, not one.** `B6a` -- `TestLineSeparator::test_own_id_marker_suppresses`: a `cairn-accept` marker naming `unicode-line-separator` clears the flag. `B6b` -- `TestLineSeparator::test_foreign_id_marker_does_not_suppress`: a marker naming `unicode-zero-width` does **not** clear it; asserts `[f.pattern_id for f in scan_text(fixture)] == ["unicode-line-separator"]`. B6b is the dispatch regression and **must be independently falsifiable**, which a shared node cannot be. | **FOLDED** -> Chunk B rows **B6a** and **B6b** |
| A2 | `* **Perturbation P-B3 — B6 is the dispatch regression (hazard-side, RUN).** Revert Chunk A in place (restore the 2-tuple yield and the ternary) while keeping the B2 loop; B6's `unicode-zero-width`-marker half fails, because the separator flag is labelled `unicode-zero-width` and the foreign marker suppresses it.` | `* **Perturbation P-B3 — B6a is the dispatch regression (hazard-side, RUN).** Revert Chunk A in place (restore the 2-tuple yield and the ternary) while keeping the B2 loop; **B6a** fails -- the own-id marker matches nothing because the flag is labelled `unicode-zero-width`. Measured under this exact state: `AssertionError: own-id marker must clear / assert ['unicode-zero-width'] == []`. **P-B3 says nothing about B6b**, which does not execute in a single-node form and is not exercised by this perturbation; P-B7 is B6b's perturbation.` | **FOLDED** -> Chunk B acceptance, perturbation **P-B3** |
| A3 | *(added)* | `* **Perturbation P-B7 — B6b's negative half is non-vacuous (hazard-side, RUN).** In `scan_text`, widen the final filter (`templates/modules/team-gated/content_scan.py:409`) to suppress by line while ignoring `pattern_id`; **B6b fails alone** -- measured 1 failed, 4 passed, failing at the foreign-marker assertion. This is the only perturbation that falsifies the plan's security-critical assertion, and without it that assertion ships unfalsified. Restore; confirm `git diff templates/modules/team-gated/content_scan.py` empty.` | **SUPERSEDED by A26**, folded -> Chunk B acceptance, perturbation **P-B7** (two-site) |
| A4 | Chunk B row **B5**, verbatim: `New TestLineSeparator::test_each_separator_is_caught: scan_text over a fixture carrying a raw U+2028 and, separately, one carrying a raw U+2029; assert each yields exactly one flag with pattern_id == "unicode-line-separator" and a message containing U+2028 / U+2029 respectively. Escape forms in the test source, matching B4.` | **Parametrized into two nodes.** `TestLineSeparator::test_each_separator_is_caught` gains `@pytest.mark.parametrize("cp", [0x2028, 0x2029])`, so each code point is its own collected node asserting exactly one flag with `pattern_id == "unicode-line-separator"` and `f"U+{cp:04X}"` in the message. Escape forms in the test source, matching B4. A per-member claim requires a per-member node. | **FOLDED** -> Chunk B row **B5** (parametrized) |
| A5 | `Remove `U+2029` from `_LINE_SEPARATORS`, leaving `U+2028`; B5's `U+2029` assertion fails **alone** while its `U+2028` assertion stays green. Repeat the other way round.` | `Remove `U+2029` from `_LINE_SEPARATORS`, leaving `U+2028`; the `0x2029` **node** fails and the `0x2028` node stays green (measured on a single-node B5: 1 failed, 4 passed). Repeat the other way round: with B5 parametrized, the `0x2028` node fails alone. **On the un-parametrized node this direction does not work** -- measured 4 failed, 1 passed, with B5 aborting at its `U+2028` assertion so the `U+2029` assertion never runs, and B6/B7/B8 failing too because their fixtures use `U+2028`. A4 is what makes both directions symmetric.` | **FOLDED** -> Chunk B acceptance, perturbation **P-B2** |
| A6 | *(added)* | New Chunk B row **B9**, in `bootstrap/tests/test_content_scan.py`: `TestLineSeparator::test_separator_and_its_marker_share_one_scanned_line` — pin the measured interaction between the new code point and the line-scoped suppression grammar. (i) A payload and a `cairn-accept: unicode-line-separator` marker on **one** `split("\n")` line: the flag is cleared, though the two occupy two *display* lines. (ii) A marker on file line 1 clearing a hit on file line 2 that occupies four display lines. Both assert the **current** behaviour, so the node is a declared-limit pin in B8's sense, not a behaviour change. | **SUPERSEDED by A20**, folded -> Chunk B rows **B9a / B9b / B9c** |
| A7 | *(added)* | `* **Perturbation P-B8 — B9's limit can fire (hazard-side, RUN).** Narrow the line-scope at `templates/modules/team-gated/content_scan.py:261` from `{i, i + 1}` to `{i}`; B9's second half fails because the preceding-line marker no longer clears the hit. Restore; confirm `git diff` empty. This perturbation is also the *proposal* a future author would need to change the grammar.` | **SUPERSEDED by A25**, folded -> Chunk B acceptance, perturbation **P-B8** |
| A8 | `A separator inside a `cairn-accept` marker's own line (line-scope covers the marker's own line — pre-existing semantics, unchanged).` | `A separator inside a `cairn-accept` marker's own line — line-scope is **file**-line scope, and `U+2028` is the first detected code point for which a file line and a display line differ, so a marker and the payload it clears can be several display lines apart. Measured: a marker on file line 1 clears a `unicode-line-separator` hit on file line 2 spanning four display lines. Pre-existing semantics, **unchanged by this plan and now pinned by B9** rather than asserted benign.` | **SUPERSEDED by A23**, folded -> *Author-accounting* > **Edge cases handled** |
| A9 | *(added)* | Two entries. **Invariant**: *A `unicode-line-separator` hit is cleared by an own-id marker on its own **file** line or the file line above, even when those are several display lines apart.* Enforced by B9, perturbable by P-B8. **Lasting-truth row**, deferred item *"The file-line-vs-display-line divergence in the suppression grammar"*, durable home *"The B9 pin plus the B3 docstring clause"*, written by *"Chunk B (B3 + B9)"*. Also: B3's docstring bullet gains one clause stating that suppression is scoped to **file** lines, which a separator can make differ from what a renderer shows. | **SUPERSEDED by A24**, folded -> *Author-accounting* invariant + failure-mode bullet, Chunk B row **B3**, and the appended *Lasting-truth migration* row |
| A10 | `* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` → the whole suite green, 0 failed / 0 skipped / 0 xfailed. **Take the baseline at implementation start, not from this plan**: the working tree carried other workflows' in-flight edits under `bootstrap/_scaffold/` `as_of 2026-08-04`, so any suite figure measured here would be measuring someone else's change.` | `* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` → **as a delta against a baseline captured at implementation start**: no failure present that is absent from the baseline, no node dropped from collection, no new skip or xfail. Record both figures in the commit body. `as_of 2026-08-04` the tree is **1790 passed, 0 failed, 0 skipped, 0 xfailed** (178s) -- clean, but it was 3-failing days earlier, which is exactly why the predicate is a delta and not an absolute.` | **FOLDED** -> Chunk B acceptance, **Whole suite, as a delta** (figure not carried; predicate only) |
| A11 | `  * `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` — the whole suite, green, **0 failed / 0 skipped / 0 xfailed**, under the canonical interpreter (3.13.13). Baseline taken at implementation start, for the reason given in Chunk B.` | `  * `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` — under the canonical interpreter (3.13.13), **as the delta defined in Chunk B**: no new failure, no dropped node, no new skip/xfail against a baseline captured at implementation start.` | **FOLDED** -> plan-level *Acceptance criteria* > **Tests that must pass**, first sub-bullet |
| A12 | `` `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → OK. Baseline **180 Markdown files, no issues**, `as_of 2026-08-04`; the count may only grow and the verdict may not change.`` | `` `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → **no issue attributable to this change**, as a delta against an implementation-start baseline. `as_of 2026-08-04` the whole-tree run is **2 issues across 195 files** — both at `dev/PLANNING.md:886`-`887`, from commit `4573c11`, unreachable from this plan's two files. An absolute "→ OK" here is **not achievable** by an implementing agent who touches only `content_scan.py` and `test_content_scan.py`. Additionally run `scripts/check_cairn.py` scoped to the files this change touches, which must be clean outright.`` | **FOLDED** -> Chunk B acceptance, **Predicate for `check_cairn`** sub-bullet; the clause the *Figure correction* withdrew is **not** carried |
| A13 | `* Whichever lands second records that **the same two entries** are stale — not a second, different pair.` `* The Maintainer performs **one** supervised re-produce after both have landed.` | `* Whichever lands second records **the same two files** as the pair *this change* makes stale, and states plainly that `_gate_manifest.py verify` will report **others belonging to other workflows** — the plan asserts no total. Measured `as_of 2026-08-04`, before either plan lands: **HOLD, 17 violations — 10 `FROZEN-MODIFIED`, 3 `COLLECTION-DROPPED`, 4 `SKIP-XFAIL-NEW`**, none of them this plan's.` `* The Maintainer performs **one** supervised re-produce after both have landed, **scoped to whatever is stale at ceremony time** — which is a Maintainer review item, not a two-entry formality, and is a wider authority act than a two-file re-pin. `bootstrap/tests/_gate_preflight.py` refuses a dirty tree, but does not refuse other workflows' *committed* frozen-file edits.` | **SUPERSEDED by A29**, folded -> *Maintainer fence* > **F2** bullets |
| A14 | `so a later `_gate_manifest.py verify` reports two `FROZEN-MODIFIED` entries — the **same two** `content-scan-detectors` will report.` | `so a later `_gate_manifest.py verify` reports these two files among its `FROZEN-MODIFIED` entries — the **same two** `content-scan-detectors` will report. **Name the two files; do not state a total**, which is other workflows' to move and is stale by the time it is read.` | **FOLDED** -> *Maintainer fence* > **F1** and *Verification* > **the gate-integrity note** |
| A15 | `Verified rather than assumed: `grep -rln "unicode-zero-width"` over the tracked tree outside `dev/proposals/` and `dev/plans/` returns exactly those two files, `as_of 2026-08-04`.` | Unchanged as a figure (it reproduces), **plus** this qualification: a literal-id grep cannot see a coupling that names no id. `templates/modules/team-gated/content_scan_runner.py` builds its reviewed-residual key as `f"{rel}:{pattern_id}:{code_hash}"` (`:299`, consumed at `:403`), so it is coupled to the **id set** without containing any id. That file is untouched here and no residual baseline churns, because Chunk A is id-preserving for both existing ids (measured: HEAD, A-only and FIXED produce byte-identical `(line, pattern_id, message)` tuples across the five probes) and the corpus carries **0** separator flags. The conclusion is reached by that argument, not by the grep. | **FOLDED** -> *Scope*, the fingerprint paragraph (*"And the grep is not what carries the conclusion"*) |
| A16 | `Extend `_BANNED_CODEPOINTS` (`bootstrap/tests/test_content_scan.py:48`–`52`) with `0x2028, 0x2029`, so `test_no_raw_banned_codepoints_in_source` now also refuses a raw separator in the scanner's own source.` | `Extend `_BANNED_CODEPOINTS` (`bootstrap/tests/test_content_scan.py:48`–`52`) with `0x2028, 0x2029`, **and widen the guard to read both `CONTENT_SCAN_SRC` and the test module's own path** (today it reads `CONTENT_SCAN_SRC` only, `bootstrap/tests/test_content_scan.py:65`). After B5–B9 the test module is itself a file whose fixtures are separator code points, and "escape forms in the test source" is otherwise a convention with nothing enforcing it. Verified the widening does the work: with a raw `U+2028` planted in a source comment, the pre-existing set reports no hits and the widened set reports `0x2028`.` | **FOLDED** -> Chunk B row **B4** |
| A17 | *(added, Sequence + Chunk B)* | **Shared-node naming convention, binding on both plans.** The coexistence node lives in a class named for its owning plan — `TestSeparatorDetectionCoexistence` here, and `content-scan-detectors` uses its own distinct class name. Measured hazard: a duplicate `class TestLineSeparator` in one module **shadows the entire earlier class** — a 5-method class followed by a 1-method class of the same name collects **1 test**, silently, no error, no warning. Whichever plan lands second must re-read the file rather than append blind. | **SUPERSEDED by A32**, folded -> Chunk B **Test-class naming** note + *Sequence* **Cross-plan ordering** note |
| A18 | `Baseline **25 nodes** `as_of 2026-08-04`; collection grows by exactly the new nodes.` | `Baseline **25 nodes** `as_of 2026-08-04` (re-measured; all 25 pass at HEAD). **Assert the collected node-id set, not its size**: capture `--collect-only -q` before and after and require the new set to be a strict superset of the old. A count check cannot distinguish "n nodes added" from "n+k added, k shadowed away" — see A17.` | **FOLDED** -> Chunk A acceptance (node-id set), Chunk B acceptance **Focused module**, and plan-level *Acceptance criteria* |
| A19 | `**Zero, over 494 tracked files, `as_of 2026-08-04`**` (and the two further occurrences of the 494 denominator, at the Chunk B sweep gate and the *Failure modes* alarm-fatigue bullet) | `**Zero, over 511 tracked files, `as_of 2026-08-04`** — re-measured at HEAD `6618e54`: 511 listed, 511 decode as UTF-8, **0** carry a raw `U+2028` or `U+2029`. The verdict is unchanged; only the denominator grew, as the review predicted. Re-take at implementation rather than quoting either figure. | **SUPERSEDED by A33**, folded -> *The measurements* > alarm fatigue, Chunk B sweep criterion, and *Failure modes* |

### Does this Response clear the plan to implement?

**No.** Stated plainly so it is not discovered at archive time:

* The declared tier is **`required(External, security lens)`**. The only review
  in this tree is **Internal** (same agent type, fresh session), and this
  Response is by the **author**. An author Response cannot discharge a review
  tier -- if it could, the tier would mean nothing.
* **The External security-lens `## Plan review` section is still owed, and no
  implementation commit may land before it is in the tree**
  (`doctrine/plans.md` > plan-review precondition). Nothing in this Response
  moves that line, and the review's closing sentence saying so remains correct.
* What this Response does discharge is the review's own recommendation --
  *"Revise, then send to External -- do not send as-is."* [I1], [I2] and [I4]
  are now mechanically amended (A1-A5, A10-A12), so the External reviewer
  spends their independent read on the questions that need cross-type
  independence rather than on ledger mechanics.

**Revised attack order for the External reviewer**, superseding the three-item
list in *Plan review -- the brief*:

1. **[I3] / B9 / P-B8 -- the suppression grammar.** Whether pinning the
   file-line-vs-display-line divergence is the right disposition, or whether a
   security control should refuse a marker that spans a separator at all. This
   is a design question an author and a same-type reviewer are structurally
   poor at, and it is the one place this plan's new code point touches an
   existing security-relevant grammar.
2. **[I5] / A13 -- the re-pin ceremony.** Whether "one supervised re-produce"
   over a set that is 17 violations wide and growing is an authority act the
   Maintainer should be asked to perform as a rider on two content plans.
3. **A17 / [R1] -- the silent-shadowing hazard.** Whether a naming convention
   in prose is sufficient protection against a failure mode that removes tests
   with no error, or whether it needs a mechanical guard.
4. Re-run the corpus sweep (**511 files, 0 hits** today) and the NAIVE-vs-FIXED
   marker table. Both reproduced for me; both are cheap and both are
   load-bearing.
5. **Do not spend the read on P-B3** -- item (3) of the original brief. It is
   now known mis-specified and is fixed by A2/A3; the useful successor is
   confirming that P-B7 falsifies B6b alone, which I measured at 1 failed,
   4 passed.

This section is append-only.

## Plan review -- Codex (External, security lens) -- 2026-08-05

**Verdict: REVISE.** The detector and its direct-test baseline reproduce
(`25 passed` under the canonical interpreter), and splitting the marker tests
into independently falsifiable nodes is a meaningful improvement. The plan is
not yet ready to make the security-relevant policy choices it identifies.

**[E1] B9 preserves a waiver path whose visible meaning diverges from the
scanned meaning.** The new detector treats `U+2028`/`U+2029` as dangerous
because they make what a person sees diverge from the file's newline grammar.
Yet B9 expressly accepts an own-id `cairn-accept` marker on the preceding file
line even when the separator makes it appear several display lines away. That
lets an explicit acceptance suppress a finding a reviewer cannot reliably
associate with it. Pinning that behavior makes the exception durable; it does
not make it safe. Change the plan to refuse cross-separator acceptance (or
obtain a Maintainer decision explicitly accepting this waiver semantics and its
user-facing warning), with tests for both paths.

**[E2] The combined re-pin is not bounded enough to be a one-time ceremony.**
A13 acknowledges a gate state wider than these two files and says the
Maintainer should re-produce "whatever is stale at ceremony time." That turns
the proposed batch into authorization to bless unrelated, concurrently landed
frozen-surface changes. The batch can share one ceremony only if preflight
identifies an exact, reviewed set owned by these two plans and refuses any extra
violation; otherwise each unrelated surface needs its own disposition before
the re-pin.

**[E3] A naming convention cannot protect against the known silent class
shadowing failure.** A17 correctly demonstrates that pytest can collect fewer
nodes without an error. Add a mechanical duplicate-test-class-name guard (or an
equivalent AST collection assertion) over `test_content_scan.py`; re-reading a
file before appending is a useful habit but is not an enforceable acceptance
criterion.

I inspected the effective amendment table and the plan's sequencing and
ceremony language, and executed
`/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_content_scan.py -q`
(`25 passed`). I did not execute a frozen-file re-pin or perturb production code.

### Figure correction -- Claude -- 2026-08-04

An audit of the Response committed at `8a14a8d` reported two `as_of 2026-08-04`
figures -- in amendments **A10** and **A12** -- that it could not reproduce. I
re-measured both from scratch, adopting neither the Response's numbers nor the
audit's, and I re-derived the conclusion each figure was offered in support of
rather than inheriting it from either party.

**The two figures do not fare alike.** A12's is false and the audit is right
about it. A10's is correct as written and the audit's challenge to it does not
survive. One of these corrections is therefore a correction of the *Response*
and the other is a correction of the *audit*.

**Nothing here changes a disposition.** Every finding stays accepted,
accepted-with-modification, or declined exactly as the Response left it. This
section corrects evidence and states, for each figure, whether the amendment
carrying it still holds.

#### Method, and the trap in the obvious method

Both disputed figures are **working-tree-sensitive**, and this tree has been
mutated by concurrent agents all session. So I measured on an isolated
`git clone --local --no-hardlinks` of this repository, `git checkout --detach
8a14a8d`, `git status --short` empty -- not on the shared live tree that both
the Response and the audit read.

That is the obvious method and **on its own it is wrong**, which is worth
recording because it produces confident third numbers that are pure artifact. A
fresh clone silently omits every piece of state that is not committed content
reachable from `refs/heads`, and *both* checks at issue read exactly such state.
I found three such artifacts and eliminated each before trusting any number:

| # | Omitted by a bare clone | What it fabricated |
|---|---|---|
| 1 | `dev/.cairn/local-env.json` -- untracked and gitignored (`.gitignore:7`) | `check_cairn.py` reported **9** issues, all of them `cited path does not resolve: dev/.cairn/local-env.json`, none in `dev/PLANNING.md` |
| 2 | `refs/cairn/gate-anchor` -- `git clone` copies `refs/heads` and `refs/tags`, not custom ref namespaces | 1 failure in `bootstrap/tests/test_gate_preflight.py:595`, the anchored-roster read fail-closing |
| 3 | a **sibling repository** beside the checkout -- `test_foldback_suggest.py:295` probes `CAIRN_ROOT.parent / "modflow_tools" / …` | 1 skip, `live ledger not available in this checkout` |

Restoring all three -- copying the one untracked file, `git update-ref
refs/cairn/gate-anchor e45e1fc`, and replacing the sibling ledger -- reconstructs
the tree an agent standing at `8a14a8d` would actually have had. Every number
below is from that reconstruction, with `git status --short` still empty.

Provenance: the Response's own commit is `8a14a8d`; repository HEAD during my
runs moved `ad401b2` -> `c11a7c4` under other agents; interpreter
Python 3.13.13 (the canonical interpreter), `PYTHONDONTWRITEBYTECODE=1`.

#### 1. A12's `check_cairn.py` figure -- **false; the audit is right**

**What was claimed.** A12 replaces a Chunk C acceptance criterion and asserts:

> `as_of 2026-08-04` the whole-tree run is **2 issues across 195 files** -- both
> at `dev/PLANNING.md:886`-`887`, from commit `4573c11`, unreachable from this
> plan's two files. An absolute "-> OK" here is **not achievable** by an
> implementing agent who touches only `content_scan.py` and
> `test_content_scan.py`.

| source | figure |
|---|---|
| A12, as written | **2 issues across 195 files**, both at `dev/PLANNING.md:886`-`887` |
| the audit | **OK -- 0 issues**, 195 files |
| **mine** | **OK -- 0 issues across 195 file(s)**, `rc 0` |

Command, run in the reconstructed checkout of `8a14a8d`:

```
~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py
  -> check_cairn: OK -- 195 Markdown file(s) scanned; no issues;
     68 external link(s) not probed.        rc=0
```

The **file count of 195 is exactly right**; the **2 issues do not exist**. Three
independent confirmations that this is not drift:

1. Scoped directly at the accused file, in the same checkout:
   `scripts/check_cairn.py dev/PLANNING.md` -> `OK -- 1 Markdown file(s)
   scanned; no issues`, `rc 0`.
2. `git diff 8a14a8d HEAD -- dev/PLANNING.md` is **empty** -- the file is
   byte-identical to the commit's own tree, so no later edit can have removed a
   flag that was there.
3. The cited lines are not a form the checker parses. `dev/PLANNING.md:886`-`887`
   read `(bootstrap/tests/test_security_lint.py` **lines 12 and 89**`;
   bootstrap/tests/fixtures/skills/README.md` **lines 16 and 41**`)` -- prose
   line references, not `path:line` citations, and both paths resolve.

So the figure was wrong when written, not overtaken. The likeliest mechanism is
the one the audit proposes and my artifact table independently corroborates:
`check_cairn.py` reads the **working tree, not HEAD**, and a concurrently-
mutating shared tree supplied the reading, which was then recorded as a durable
`as_of`-dated claim and attributed to a named commit (`4573c11`) that
demonstrably does not produce it.

**Does A12 still hold?** **Partly -- it stays in force, with one clause
withdrawn.** A12 is compound:

* **Retained.** The delta predicate (*"no issue attributable to this change,
  as a delta against an implementation-start baseline"*) and the requirement
  that a **scoped** run over the touched files be *clean outright*. These do not
  rest on the false figure, and my own method section is fresh independent
  evidence for them: the same command at the same commit returns `OK` or 9
  issues depending on untracked, gitignored state. A whole-tree verdict is
  genuinely not a stable function of committed content, so instructing an
  implementing agent to measure a delta is right.
* **Withdrawn.** The sentence *"An absolute `-> OK` here is **not achievable**
  by an implementing agent"* is **refuted, not merely unsupported** -- I
  achieved exactly that at this plan's own commit, in one run, above. An
  implementing agent who sees a non-`OK` whole-tree run should read it as a
  signal to look for untracked or concurrent state, **not** as the expected
  condition A12 told them to anticipate. Also withdrawn with it: the
  `dev/PLANNING.md:886`-`887` figure and the attribution to commit `4573c11`.

A13/A14's own rule -- *name the delta, assert no total* -- applies to A12
verbatim, and the Response did not apply it there. It is applied here.

#### 2. A10's suite figure -- **correct as written; the audit is wrong**

**What was claimed.** A10 records:

> `as_of 2026-08-04` the tree is **1790 passed, 0 failed, 0 skipped, 0 xfailed**
> (178s) -- clean, but it was 3-failing days earlier, which is exactly why the
> predicate is a delta and not an absolute.

| source | figure |
|---|---|
| A10, as written | **1790 passed, 0 failed, 0 skipped, 0 xfailed** (178s) |
| the audit | 2 failed, 1788 passed (175.46s) |
| **mine** | **1790 passed, 0 failed, 0 skipped, 0 xfailed** (160.45s) |

Command, run in the reconstructed checkout of `8a14a8d`:

```
~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests -q -rs
  -> 1790 passed, 3 warnings in 160.45s (0:02:40)
```

**The audit's challenge does not survive, and I am correcting nothing here.**
All three parties agree the collected total is **1790**; the dispute is only
whether two nodes were red. The audit named them --
`test_gate_manifest.py::test_verify_allows_added_test` and
`test_gate_manifest.py::test_trusted_verifier_detects_tamper_in_separate_target_tree`
-- and itself attributed them to *"the churning tree (siblings hold frozen gate
files dirty)"*. That attribution is correct, and it disqualifies the reading as
a measurement of this commit. Two confirmations:

1. Both nodes **pass in the reconstructed checkout of `8a14a8d`** (`2 passed`).
2. Both nodes **pass on the live tree now**, at HEAD `c11a7c4` (`2 passed in
   1.14s`) -- the sibling edits that reddened them have since been committed or
   reverted, and nothing in this plan touched them.

The audit performed a real reading of a dirty shared tree and then compared it
against a figure describing committed content. That is the same category error
the audit correctly diagnoses in A12 -- here committed by the auditor rather
than by the Response.

**Does A10 still hold?** **Yes, in force and unamended.** Its figure reproduces
exactly. Its conclusion is in fact *strengthened* by this episode: A10's whole
point is that the suite predicate must be a **delta against a baseline captured
at implementation start**, precisely because an absolute figure is hostage to
whatever else the tree is carrying. Two independent readers just obtained two
different absolutes from the same commit within hours. A10 anticipated that and
is the reason the predicate is already a delta.

#### 3. The audit's third figure, and what I did not re-open

The audit's `[I5]` gate-manifest comparison (Response **17** violations --
10 `FROZEN-MODIFIED`, 3 `COLLECTION-DROPPED`, 4 `SKIP-XFAIL-NEW`; audit **18**)
is **not a dispute**: the audit reproduces the Response's 10/3/4 exactly once
the single sibling-dirty file the Response explicitly excluded is subtracted,
and confirms the Response's correction of the review. I did not re-measure it,
and it needs no correction. That the count moved between two readings hours
apart is further evidence for A13/A14, as the audit says.

I likewise did not re-open the figures the audit re-measured and found to
reproduce (the 511-file corpus sweep in A19, the 25-node collection baseline in
A18, `frozen_files` at 164, the `[I6]`/A15 grep scope, the neutrality gate's
`fail=95` / `info=21`, the `[R1]` silent class-shadowing measurement behind A17,
and every cited line number). No disposition is re-litigated anywhere above.

#### 4. Net effect on the amendment table

| amendment | figure | status |
|---|---|---|
| **A10** | `1790 passed, 0 failed, 0 skipped, 0 xfailed` | **Reproduces. Unamended, in force.** The audit's contrary reading is an artifact of a dirty shared tree. |
| **A12** | `2 issues across 195 files` at `dev/PLANNING.md:886`-`887`, from `4573c11` | **False.** Figure withdrawn, and with it the derived clause that an absolute `-> OK` is *not achievable*. The delta predicate and the scoped-clean requirement **stay in force** on independent evidence. |

The implementing agent's instructions change in exactly one way: A12 no longer
tells you to expect a non-`OK` whole-tree run. Measure the delta because the
verdict is not a stable function of committed content -- not because the tree is
known dirty.

This section is append-only.

## Response to plan review -- Claude (author) -- 2026-08-05

**Model**: claude-opus-5. **Standing**: plan author, dispositioning the
**External** security-lens plan review (Codex, 2026-08-05, verdict **REVISE**)
appended above.

**Where that review sits, because the file is not chronological.** The External
section was inserted at what is now line 1235, **before** the
`### Figure correction -- Claude -- 2026-08-04` subsection that closes the
previous Response. The last section in this file is therefore *not* the newest
one, and a reader who assumes append-at-end will disposition the wrong text. I
record it here so the next reader does not have to rediscover it.

**Method, and the rule that governed it.** Every figure the External review
states, and every figure the previous Response and its Figure correction
assert, was re-derived against the live tree at HEAD `6bcd2d3` under
`~/conda_envs/lhm/bin/python3.13` (3.13.13, UCD 15.1.0), `PYTHONDONTWRITEBYTECODE=1`.
Nothing was inherited. Where a remedy was proposed, I **built and ran it**
rather than describing it: all variants live in the session scratch directory
and **no repository file outside this plan was modified**. Four figures moved
and one previously-accepted perturbation stopped working; all five are reported
below as plainly as the reproductions.

The rule that decided the shape of this Response: *the artifact under
verification must not supply the material used to verify it.* Applied twice
here — the refusal rule E1 asks for was checked by running the plan's **own
node set against a build that lacks it**, and the shadowing guard E3 asks for
was checked against a module that actually shadows, not against its own claim.

### Re-measurement ledger

**Reproduced exactly:**

| Figure | Source | Live result |
|---|---|---|
| `pytest bootstrap/tests/test_content_scan.py -q` -> **25 passed** | External review | reproduces (0.07s); `--collect-only -q` -> **25 tests collected** |
| Corpus sweep verdict: **0** tracked files carry a raw `U+2028`/`U+2029` | plan / A19 | reproduces; **0** hits, every file decodes as UTF-8 (denominator moved -- below) |
| `frozen_files` = **164** entries; both target files present | plan / prior Response | reproduces; `content_scan_runner.py` is present too |
| `quality_gate.py --sub neutrality` -> `fail=95 info=21` | plan / prior Response | reproduces exactly |
| Every cited line number: `content_scan.py:137` `_ZERO_WIDTH`, `:144` `_BIDI`, `:261` `suppressed[pid].update({i, i + 1})`, `:295` `def _scan_unicode`, `:390` `lines = text.split("\n")`, `:402` the ternary, `:409` the final filter; docstring bullets at `:40` and `:43`-`45`; `test_content_scan.py:48`-`52` `_BANNED_CODEPOINTS` and `:65` the `CONTENT_SCAN_SRC` read | plan / Internal review / prior Response | **all reproduce**, character-for-character where quoted |
| `check_cairn.py:91`-`94` loads the template scanner by path (no twin); `content_scan_runner.py:299` fingerprint consumed at `:403` | plan / [I6] / A15 | reproduce |
| [I3]/A6 hazard, case A: payload + own-id marker on **one** file line -> flag cleared | prior Response | reproduces: 1 file line, 2 display lines, `[]` with marker, `['unicode-line-separator']` without |
| [I3]/A6 hazard, case B: marker on file line 1 clears a hit on file line 2 spanning **four** display lines | prior Response | reproduces exactly: 2 file lines, 5 display lines total, `[]` with marker |
| Foreign-id (`unicode-zero-width`) marker does **not** clear a separator flag | plan B6b | reproduces: `['unicode-line-separator']` |
| Tri-fixture `{(1,'unicode-zero-width'), (2,'unicode-bidi'), (3,'unicode-line-separator')}`; two separators on one line -> **one** flag naming `U+2028` | plan | reproduce exactly |
| Real 25-node module repointed at the fixed build -> **24 passed, 1 deselected** | plan / Internal review | reproduces |
| Bandit over the fixed build -> `errors: []`, zero findings | plan | reproduces (0 results at every severity, 373 loc, on the build that also carries E1's remedy) |
| [R1]/A17 silent class shadowing: a 5-method class followed by a 1-method class of the same name collects **1 test**, no error, no warning | prior Response | reproduces exactly |

**Did not reproduce, or moved** -- reported as findings:

1. **The corpus denominator moved again: 511 -> 520.** Live: `git ls-files` lists
   **520** entries, **520** regular files read, **0** non-UTF-8, **0** carrying a
   raw `U+2028` or `U+2029`. This is the **third** distinct denominator this plan
   has carried (494 -> 511 -> 520) across three days. The verdict is unchanged and
   the rule still ships silent; the figure is the problem, not the sweep.
   Amendment **A33** stops the plan quoting a denominator at all, applying
   A13/A14's own rule (*name the delta, assert no total*) to the one figure that
   kept escaping it.

2. **The whole-tree `check_cairn` counts do not reproduce; its verdict does.**
   The Figure correction records `OK -- 0 issues across 195 file(s)`, 68 external
   links not probed. Live: `check_cairn: OK -- **176** Markdown file(s) scanned;
   no issues; **48** external link(s) not probed`, rc 0. The **verdict**
   reproduces and the Figure correction's central claim -- that an absolute `OK`
   *is* achievable, contra the withdrawn A12 clause -- is confirmed a second time
   by an independent run. Only the counts moved, by 19 files and 20 links.

3. **[E2]'s underlying gate state is far wider than A13 recorded: 17 -> 60
   violations.** A13 states, `as_of 2026-08-04`, `HOLD, 17 violations -- 10
   FROZEN-MODIFIED, 3 COLLECTION-DROPPED, 4 SKIP-XFAIL-NEW`. Live
   `bootstrap/tests/_gate_manifest.py verify` -> **13 `FROZEN-MODIFIED`, 3
   `COLLECTION-DROPPED`, 44 `SKIP-XFAIL-NEW` = 60 violations**, plus `ANCHOR:
   skipped` and three `FROZEN-NEW` notes. The External finding is **strengthened
   by a factor of three and a half in one day**, which is itself the argument
   A13 was reaching for.

4. **A3's perturbation P-B7 stops falsifying B6b once E1's remedy lands.**
   This is the load-bearing non-reproduction and I found it only because I built
   the remedy before writing about it. P-B7 as A3 specifies it -- widen the final
   filter at `templates/modules/team-gated/content_scan.py:409` to suppress by
   line while ignoring `pattern_id` -- was measured at *1 failed, 4 passed*
   against the fixed build. Against the build that carries E1's refusal, the
   same single-site perturbation yields **9 passed**: the refusal's own
   pid check independently keeps the foreign marker from clearing the flag, so
   the perturbation no longer reaches the assertion it exists to falsify. A
   two-site perturbation is required and was measured -- see **A26**. Accepting
   E1 without this amendment would have shipped the plan's security-critical
   assertion **unfalsified while a ledger entry claimed otherwise**.

5. **The old P-B8 no longer targets its mechanism.** A7 specifies narrowing
   `{i, i + 1}` to `{i}` at `content_scan.py:261`. Under E1's refusal, case B is
   already refused, so that narrowing is not what B9 discriminates. Restated
   and re-measured at **A25**.

**New measurements taken for this Response** (all against builds reconstructed
from the plan's prose, in scratch, never in the tree):

| What | Result |
|---|---|
| E1 remedy, case A (marker after the separator, same file line) | **refused** -- `['unicode-line-separator']` survives, where the un-remedied build returns `[]` |
| E1 remedy, case B (marker on the preceding file line, hit 4 display lines away) | **refused** -- `['unicode-line-separator']` survives |
| E1 remedy, case C (marker *before* the separator, same display line) | **honoured** -- `[]`. The accept path survives, so the rule is not a disguised "unsuppressible" |
| E1 remedy, foreign-id marker | never honoured, in either build |
| E1 remedy, **block form** (`cairn-accept` ... `cairn-accept-end` spanning the hit) | **refused** -- `['unicode-line-separator']` survives where the un-remedied build returns `[]`. A real contract consequence, named in **A24** rather than discovered later |
| E1 remedy vs. existing behaviour | real 25-node module repointed at it -> **24 passed, 1 deselected** -- byte-identical outcome to the build without it. No existing id's suppression changes |
| New P-B8 (delete the association guard) | **2 failed, 7 passed** -- exactly the two refusal nodes, and only those |
| New P-B7 (two-site: line-blind filter **and** pid-blind association) | **1 failed, 8 passed** -- exactly `test_foreign_id_marker_does_not_suppress` |
| Single-site pid-blind association alone | **9 passed** -- does *not* falsify B6b; recorded so no one re-specifies P-B7 as a one-line edit |
| Duplicate **method** shadowing (not just class) | `test_one` defined twice in one class collects **2** of 3 nodes, silently. A17's class-naming convention does not address this variant at all |
| AST duplicate-name guard prototype | `clean` on the real `bootstrap/tests/test_content_scan.py` today; flags `duplicate top-level class: TestLineSeparator` and `duplicate method TestX.test_one` on the two hazard modules |
| Does any existing mechanism bound the re-pin set? | **No.** `bootstrap/tests/_gate_preflight.py:1163`-`1170` builds the blessing scope as **counts only** -- `modified` / `added` / `removed` and collection before/after -- and `draft_message` prints those counts. It names **no paths** and **refuses nothing**. Only `bootstrap/tests/_gate_manifest.py:364` names paths, and only in `verify` output a human reads |

### Dispositions

**[E1] -- ACCEPTED, in the reviewer's first branch (refuse cross-separator
acceptance), and executed rather than promised.**

The finding is correct and reproduces exactly. B9 as the previous Response wrote
it pins the waiver: it asserts the *current* behaviour, in which an own-id
marker on the preceding file line clears a hit four display lines away. The
reviewer's sentence is the right one -- *"Pinning that behavior makes the
exception durable; it does not make it safe."* A declared-limit pin is the right
instrument for the per-line `break` convention, where the limit is visible in
the flag itself; it is the wrong instrument for a waiver whose whole defect is
that a reviewer cannot see what it waives.

I took **branch (a)** rather than routing to the Maintainer, for three reasons I
can defend by measurement, not preference:

* **It is inside the Decision's contract, not beyond it.** The Decision settles
  that a separator hit is *"suppressible only by a marker written against that
  id"* -- an upper bound on what may suppress. A refusal narrows within that
  bound; it cannot conflict with it. The Decision also requires that *"each
  marker suppresses only its own id"*, which the refusal strengthens.
* **Its blast radius on existing behaviour is measured at zero.** The real
  25-node module against the remedied build: **24 passed, 1 deselected** --
  identical to the build without it. The refusal is scoped to a pattern id that
  does not exist yet, so no marker any adopter has already written changes
  meaning. There is no shipped semantics to break.
* **The accept path survives**, so this is a narrowing and not a silent
  conversion of the rule to "unsuppressible": a marker written **before** the
  separator on the same file line -- i.e. rendering on the same display line as
  the payload it accepts -- is honoured (`[]`, measured). That is precisely the
  reviewer's association property, made mechanical.

Two consequences I am naming rather than letting an implementer discover:
(i) the **block form** (`cairn-accept` / `cairn-accept-end` spanning the hit) is
also refused -- measured -- because a block acceptance is even less reliably
associable than a preceding-line one; (ii) this is **new production behaviour
the External reviewer has not seen**, which is the largest single reason this
Response does not clear the plan (below).

Residue: **A20-A24, A26, A27** -- B9 replaced by three nodes pinning the refusal
*and* the honoured path ("tests for both paths", as the finding asks); a new
production chunk row B10; the Scope's site list, the edge-case bullet, the
invariant, the lasting-truth row, the docstring clause and the release note all
moved from *blessed waiver* to *refused waiver*; and P-B7 re-specified because
the remedy neutered it.

**[E2] -- ACCEPTED.** Reproduced and strengthened. A13's *"scoped to whatever is
stale at ceremony time"* is exactly the sentence the reviewer names, and my
re-measurement shows why it cannot stand: the gate state it would bless went
from **17 violations to 60 in a single day**, none of them this plan's. The
reviewer's condition -- *"preflight identifies an exact, reviewed set owned by
these two plans and refuses any extra violation"* -- is **not met by anything
that exists today**, and I checked rather than assumed: `_gate_preflight.py`
computes the blessing scope as bare **counts** (`bootstrap/tests/_gate_preflight.py:1163`-`1170`),
names no paths, and has no refusal path for an unexpected member. Building that
refusal is `bootstrap/tests/_gate_preflight.py`'s surface, outside this plan's
two-file scope and squarely inside `bootstrap/REANCHOR_RUNBOOK.md`'s
Maintainer-only territory. So the disposition is the reviewer's *"otherwise"*
branch, made binding on the plan: the batch loses its shared-ceremony
authorization unless it can be bounded, and each unrelated surface takes its own
disposition first. Residue: **A28, A29**.

**[E3] -- ACCEPTED.** The reviewer is right that A17 is prose where a mechanism
is required, and my own measurement makes the case worse than A17 stated: the
same silent-collection-loss failure occurs at **method** level too -- a
duplicate `test_one` in one class collects 2 of 3 nodes with no error and no
warning -- which a class-naming convention does not touch at all. The guard is
cheap, stdlib-only (`ast`, inside the dependency budget), and its subject is the
test module's own AST rather than pytest's collection, so it does not ask the
artifact under verification to supply its own oracle. Prototype measured: clean
on the real file today, and it flags both hazard shapes. Residue: **A30, A31,
A32**. **A18 stays in force unamended** -- the collected-node-id-set assertion
and the duplicate-name guard are complementary, not alternatives: the guard
catches the cause inside one file, A18 catches the effect across a merge.

**Nothing is declined.** All three External findings are accepted, two of them
in the reviewer's own preferred branch.

### Amendments in force

Every row below is a mechanical change to this plan, continuing the A-series.
Rows marked *(added)* introduce text where none stood; all others quote the
superseded text **verbatim** -- where a row supersedes an earlier amendment, the
quoted text is that amendment's in-force replacement cell.

| # | Superseded text (verbatim) | Replaced by | Folded into (2026-08-05) |
|---|---|---|---|
| A20 | **A6**, verbatim: New Chunk B row **B9**, in `bootstrap/tests/test_content_scan.py`: `TestLineSeparator::test_separator_and_its_marker_share_one_scanned_line` — pin the measured interaction between the new code point and the line-scoped suppression grammar. (i) A payload and a `cairn-accept: unicode-line-separator` marker on **one** `split("\n")` line: the flag is cleared, though the two occupy two *display* lines. (ii) A marker on file line 1 clearing a hit on file line 2 that occupies four display lines. Both assert the **current** behaviour, so the node is a declared-limit pin in B8's sense, not a behaviour change. | **Three nodes in `bootstrap/tests/test_content_scan.py`, pinning the refusal and the accept path — "tests for both paths" per [E1].** `B9a` — `TestSeparatorDetection::test_cross_separator_acceptance_refused_same_file_line`: payload, then a separator, then an own-id `cairn-accept` marker, all on one file line; assert `[f.pattern_id for f in scan_text(fixture)] == ["unicode-line-separator"]` (the acceptance is **refused**). `B9b` — `TestSeparatorDetection::test_cross_separator_acceptance_refused_preceding_line`: an own-id marker on file line 1, the hit on file line 2 spanning four display lines; assert the flag **survives**. `B9c` — `TestSeparatorDetection::test_same_display_line_acceptance_is_honoured`: an own-id marker written **before** the separator on the same file line; assert `scan_text(fixture) == []`. Measured against the remedied build: all three green; against a build without the refusal, B9a and B9b fail and B9c stays green. | **FOLDED** -> Chunk B rows **B9a / B9b / B9c** (the pinning B9 is deleted, not amended) |
| A21 | *(added — new Chunk B production row)* | New Chunk B row **B10**, in `templates/modules/team-gated/content_scan.py`: a module-level helper `_separator_accept_is_associable(line)` placed immediately above `scan_text`, which locates the first `_LINE_SEPARATORS` member in the file line and returns `True` only if `_ACCEPT_RE` finds a marker **before** that index whose `pid` is `unicode-line-separator` and whose `reason` attribute is non-empty (the same validity rule `_parse_suppressions` applies). The final filter at `templates/modules/team-gated/content_scan.py:409` becomes an explicit loop: a flag suppressed by the existing per-id line scope is **re-emitted** when `f.pattern_id == "unicode-line-separator"` and the helper returns `False`. `_parse_suppressions` is **not** modified, and no other pattern id's path changes — measured: the real 25-node module against this build is **24 passed, 1 deselected**, byte-identical to the build without it. | **FOLDED** -> Chunk B row **B10** (production) |
| A22 | `Within `content_scan.py` the Response named three sites, and all three are verified present at HEAD: the module-docstring pattern-id list (the `unicode-bidi` bullet ends at `templates/modules/team-gated/content_scan.py:45`), the detector loops in `_scan_unicode`, and the call site at `templates/modules/team-gated/content_scan.py:401`.` | `Within `content_scan.py` there are now **four** sites, all verified present at HEAD: the module-docstring pattern-id list (the `unicode-bidi` bullet ends at `templates/modules/team-gated/content_scan.py:45`), the detector loops in `_scan_unicode` (`:295`), the call site at `:401`, and — added by [E1] — the final suppression filter at `:409` plus the new helper above `scan_text`. The fourth site is a **suppression-grammar** change scoped to the new pattern id; it is inside the plan's two-file *Touches* line but beyond the Decision's literal text, and it is named here rather than folded in silently.` | **FOLDED** -> *Scope*, the **four sites** paragraph |
| A23 | **A8**, verbatim: A separator inside a `cairn-accept` marker's own line — line-scope is **file**-line scope, and `U+2028` is the first detected code point for which a file line and a display line differ, so a marker and the payload it clears can be several display lines apart. Measured: a marker on file line 1 clears a `unicode-line-separator` hit on file line 2 spanning four display lines. Pre-existing semantics, **unchanged by this plan and now pinned by B9** rather than asserted benign. | A separator inside a `cairn-accept` marker's scope — line-scope is **file**-line scope, and `U+2028` is the first detected code point for which a file line and a display line differ. For every **pre-existing** pattern id that divergence is left exactly as it is (out of scope, and 0 tracked files can exercise it). For `unicode-line-separator` it is **closed**: B10 refuses an acceptance that does not render on the same display line as the separator it accepts. Measured, un-remedied build vs remedied build: marker-after-separator `[]` -> `['unicode-line-separator']`; preceding-file-line marker `[]` -> `['unicode-line-separator']`; marker before the separator on the same display line `[]` -> `[]`. | **FOLDED** -> *Author-accounting* > **Edge cases handled** |
| A24 | **A9**, verbatim: Two entries. **Invariant**: *A `unicode-line-separator` hit is cleared by an own-id marker on its own **file** line or the file line above, even when those are several display lines apart.* Enforced by B9, perturbable by P-B8. **Lasting-truth row**, deferred item *"The file-line-vs-display-line divergence in the suppression grammar"*, durable home *"The B9 pin plus the B3 docstring clause"*, written by *"Chunk B (B3 + B9)"*. Also: B3's docstring bullet gains one clause stating that suppression is scoped to **file** lines, which a separator can make differ from what a renderer shows. | Three entries. **Invariant**: *A `unicode-line-separator` hit is cleared **only** by an own-id marker that renders on the same display line as the separator it accepts; an acceptance separated from its payload by a separator — on the preceding file line, later on the same file line, or in `cairn-accept` / `cairn-accept-end` block form — is refused.* Enforced by B9a/B9b/B9c, perturbable by the new P-B8. **Failure mode** (new bullet in *Author-accounting*): *An adopter with a legitimate word-processor paste finds the marker refused.* -> **Open by design, and narrower than it looks**: the working form is documented (marker before the separator on the same display line) and 0 tracked files exercise the rule today; if the refusal proves noisy in an adopter tree that is a Maintainer question, not an inline widening. **Lasting-truth row**, deferred item *"The display-line association rule for `unicode-line-separator` acceptances"*, durable home *"The B9a/B9b/B9c pins plus the B3 docstring clause"*, written by *"Chunk B (B3 + B9a-c + B10)"*. Also: B3's docstring bullet gains one clause stating that an acceptance for this id must render on the same display line as the separator, **and that the block form does not suppress it** — measured, not inferred. | **FOLDED** -> *Author-accounting* invariant + failure-mode bullet, Chunk B row **B3**, and the appended *Lasting-truth migration* row |
| A25 | **A7**, verbatim: `* **Perturbation P-B8 — B9's limit can fire (hazard-side, RUN).** Narrow the line-scope at `templates/modules/team-gated/content_scan.py:261` from `{i, i + 1}` to `{i}`; B9's second half fails because the preceding-line marker no longer clears the hit. Restore; confirm `git diff` empty. This perturbation is also the *proposal* a future author would need to change the grammar.` | `* **Perturbation P-B8 — the refusal can fire (hazard-side, RUN).** Delete the B10 re-emit branch from the final filter (restoring the plain per-id line filter) while keeping every test node; **B9a and B9b fail and B9c stays green** — measured **2 failed, 7 passed**, and only those two. `_parse_suppressions` is untouched by this perturbation, so it discriminates the refusal itself rather than the line scope. Restore; confirm `git diff templates/modules/team-gated/content_scan.py` empty.` | **FOLDED** -> Chunk B acceptance, perturbation **P-B8** |
| A26 | **A3**, verbatim: `* **Perturbation P-B7 — B6b's negative half is non-vacuous (hazard-side, RUN).** In `scan_text`, widen the final filter (`templates/modules/team-gated/content_scan.py:409`) to suppress by line while ignoring `pattern_id`; **B6b fails alone** -- measured 1 failed, 4 passed, failing at the foreign-marker assertion. This is the only perturbation that falsifies the plan's security-critical assertion, and without it that assertion ships unfalsified. Restore; confirm `git diff templates/modules/team-gated/content_scan.py` empty.` | `* **Perturbation P-B7 — B6b's negative half is non-vacuous (hazard-side, RUN, TWO-SITE).** The single-site form specified before **no longer works once B10 lands** and must not be carried forward: widening the final filter alone to suppress by line while ignoring `pattern_id` yields **9 passed** — B10's own pid check independently keeps the foreign marker from clearing the flag, so the perturbation never reaches the assertion. Perturb **both** id checks: (1) the final filter suppresses by line ignoring `pattern_id`, **and** (2) `_separator_accept_is_associable` accepts any valid `cairn-accept` marker regardless of its `pid`. Measured: **1 failed, 8 passed**, failing exactly `test_foreign_id_marker_does_not_suppress`. Recorded as a caution: the pid-blind association edit **alone** yields 9 passed, so a one-line version of this perturbation is a false ledger entry. Restore both; confirm `git diff templates/modules/team-gated/content_scan.py` empty.` | **FOLDED** -> Chunk B acceptance, perturbation **P-B7** |
| A27 | `**One** line covering the pattern-id partition, shared with `content-scan-detectors` rather than duplicated: the content scanner's unicode detectors now carry their own pattern ids, and a raw `U+2028` / `U+2029` flags under `unicode-line-separator`. Cross-reference both proposals and both plans **by stem**, per `AGENTS.md`.` | `**One** line covering the pattern-id partition, shared with `content-scan-detectors` rather than duplicated: the content scanner's unicode detectors now carry their own pattern ids, and a raw `U+2028` / `U+2029` flags under `unicode-line-separator`. **The same line must state the acceptance-association rule** — a `unicode-line-separator` acceptance is honoured only when it renders on the same display line as the separator, and the block form does not suppress it — because that is the adopter-visible half of [E1] and a release note that omits it ships a surprise. Cross-reference both proposals and both plans **by stem**, per `AGENTS.md`.` | **FOLDED** -> Chunk C row **C1** |
| A28 | `**F2 — one ceremony for two plans, not two.** `content-scan-detectors` edits the **same two files** and is being planned in parallel. Its frozen-file delta is the identical pair. The batch rule this plan adopts:` | `**F2 — one ceremony for two plans, and only if it can be bounded to them.** `content-scan-detectors` edits the **same two files** and is being planned in parallel; its frozen-file delta is the identical pair. Per [E2], a shared ceremony is **not** authorized by that coincidence alone: it is authorized only over an exact, reviewed set owned by these two plans. The batch rule this plan adopts:` | **FOLDED** -> *Maintainer fence* > **F2** heading and preamble |
| A29 | **A13**, verbatim: `* Whichever lands second records **the same two files** as the pair *this change* makes stale, and states plainly that `_gate_manifest.py verify` will report **others belonging to other workflows** — the plan asserts no total. Measured `as_of 2026-08-04`, before either plan lands: **HOLD, 17 violations — 10 `FROZEN-MODIFIED`, 3 `COLLECTION-DROPPED`, 4 `SKIP-XFAIL-NEW`**, none of them this plan's.` `* The Maintainer performs **one** supervised re-produce after both have landed, **scoped to whatever is stale at ceremony time** — which is a Maintainer review item, not a two-entry formality, and is a wider authority act than a two-file re-pin. `bootstrap/tests/_gate_preflight.py` refuses a dirty tree, but does not refuse other workflows' *committed* frozen-file edits.` | `* Whichever lands second records **the same two files** as the pair *this change* makes stale, and states plainly that `_gate_manifest.py verify` will report **others belonging to other workflows** — the plan asserts no total.` `* **The shared ceremony is conditional, and the condition is checked before it runs.** It is authorized **only** over the exact set `{templates/modules/team-gated/content_scan.py, bootstrap/tests/test_content_scan.py}`. Before the re-produce, the Maintainer enumerates the `FROZEN-MODIFIED` / `COLLECTION-DROPPED` / `SKIP-XFAIL-NEW` paths from `bootstrap/tests/_gate_manifest.py verify`; **if any member falls outside that set, the shared ceremony is off** and each unrelated surface takes its own disposition first. A blanket re-produce would bless concurrently-landed frozen-surface changes nobody reviewed.` `* **No mechanism enforces that condition today, and this plan does not build one.** Measured: `bootstrap/tests/_gate_preflight.py:1163`-`1170` derives the blessing scope as bare **counts** (`modified` / `added` / `removed`, plus collection before/after) and `draft_message` prints those counts; it names **no paths** and refuses nothing. Only `bootstrap/tests/_gate_manifest.py:364` names paths, in `verify` output a human reads. Adding a refusal is `_gate_preflight.py`'s surface — outside this plan's two files and inside `bootstrap/REANCHOR_RUNBOOK.md`'s Maintainer-only territory — so the condition is discharged by the Maintainer reading the enumeration, and the plan says so instead of implying a gate.` `* **The state being blessed is moving fast.** Measured `as_of 2026-08-04`: 17 violations. Re-measured `as_of 2026-08-05`, before either plan lands: **13 `FROZEN-MODIFIED`, 3 `COLLECTION-DROPPED`, 44 `SKIP-XFAIL-NEW` = 60**, none of them this plan's. Any count written here is stale when read; the enumeration is taken **at ceremony time**, not quoted from this plan.` | **FOLDED** -> *Maintainer fence* > **F2** bullets (violation counts dropped per A29's own rule) |
| A30 | *(added — new Chunk B test row)* | New Chunk B row **B11**, in `bootstrap/tests/test_content_scan.py`: `TestCollectionIntegrity::test_no_duplicate_test_class_or_method_names` — parse **this module's own source** with the standard-library `ast` (no new dependency; `bootstrap/DEPENDENCY_BUDGET.md` unaffected) and assert that (i) no two top-level `ClassDef` nodes share a name and (ii) within each class, no two `FunctionDef`/`AsyncFunctionDef` nodes share a name. This is [E3]'s mechanical guard: it fires **inside the file** at the moment a second plan appends a colliding class, where a collection-count check fires only after nodes have already vanished. Measured: the prototype returns `clean` against `bootstrap/tests/test_content_scan.py` at HEAD today. | **FOLDED** -> Chunk B row **B11** |
| A31 | *(added — new perturbation)* | `* **Perturbation P-B9 — B11 can fire (hazard-side, RUN, transient).** Append a second `class TestSeparatorDetection` carrying one method to `bootstrap/tests/test_content_scan.py`; B11 fails naming `duplicate top-level class: TestSeparatorDetection`. Repeat with a duplicate **method** name inside one class; B11 fails naming `duplicate method <Class>.<name>`. Delete both; confirm `git status --short` clean. **This is the one perturbation in the plan whose subject is the test module rather than production code, and that is correct, not an exception**: the hazard [E3] names *is* a property of the test module's own source, so perturbing that source is perturbing the hazard, not softening an assertion. Measured on standalone hazard modules: a 5-method class followed by a 1-method class of the same name collects **1** node, and a class with a duplicated method collects **2** of 3 — in both cases silently, with no error and no warning, which is exactly why a count check cannot see it.` | **FOLDED** -> Chunk B acceptance, perturbation **P-B9** |
| A32 | **A17**, verbatim: **Shared-node naming convention, binding on both plans.** The coexistence node lives in a class named for its owning plan — `TestSeparatorDetectionCoexistence` here, and `content-scan-detectors` uses its own distinct class name. Measured hazard: a duplicate `class TestLineSeparator` in one module **shadows the entire earlier class** — a 5-method class followed by a 1-method class of the same name collects **1 test**, silently, no error, no warning. Whichever plan lands second must re-read the file rather than append blind. | **Shared-node naming convention, binding on both plans — and now enforced, not merely agreed.** The coexistence node lives in a class named for its owning plan — `TestSeparatorDetectionCoexistence` here, and `content-scan-detectors` uses its own distinct class name; whichever plan lands second re-reads the file rather than appending blind. Per [E3] the convention is **backed by B11**, which fails on a duplicate class name *or* a duplicate method name within a class, because a convention cannot protect against a failure that produces no error. Measured hazard, both shapes: a 5-method class followed by a 1-method class of the same name collects **1 test**; a class with a duplicated method collects **2** of 3 — silently in both cases. The habit is retained because the guard reports the collision, it does not resolve it. | **FOLDED** -> Chunk B **Test-class naming** note + *Sequence* **Cross-plan ordering** note |
| A33 | **A19**, verbatim: **Zero, over 511 tracked files, `as_of 2026-08-04`** — re-measured at HEAD `6618e54`: 511 listed, 511 decode as UTF-8, **0** carry a raw `U+2028` or `U+2029`. The verdict is unchanged; only the denominator grew, as the review predicted. Re-take at implementation rather than quoting either figure. | **Zero tracked files carry a raw `U+2028` or `U+2029` — and the plan states no denominator, anywhere.** Three denominators have now been written into this plan for the same unchanged verdict: **494** (`as_of 2026-08-04`), **511** (`as_of 2026-08-04`, later that day), **520** (`as_of 2026-08-05`, this Response: 520 listed, 520 read, 0 non-UTF-8, **0** hits). A13/A14's own rule — *name the delta, assert no total* — applies here and was not applied: the load-bearing claim is **"0 hits"**, which is a stop-signal predicate, and the denominator is a moving count of unrelated commits. The implementing agent re-runs the sweep and records **the hit count and the date** in the commit body; a non-zero hit count is a Maintainer question, not an inline `cairn-accept`. | **FOLDED** -> *The measurements* > alarm fatigue, Chunk B sweep criterion, *Failure modes*, and *Verification* |

### Gate audit -- what is satisfied today, and what is not

Read before implementing. Two gates were breached elsewhere in this repository
yesterday because nobody opened them.

| Gate | Where declared | Satisfied today? |
|---|---|---|
| Declared review tier `required(External, security lens)` | plan header; Decision *Next transition*: `plan-open, carrying required(External, security lens) in its own right` (`dev/proposals/archive/2026-08-03-claude-separator-detection.md:466`-`467`) | **Routing satisfied.** The tier is correctly carried and an External security-lens section is in the tree (commit `0deeac0`). |
| *"No implementation commit lands before an External `## Plan review` section is in the tree"* | plan header | **Literally satisfied** — the section exists. **But not sufficient**: see the next two rows. |
| `doctrine/plans.md:114`-`117` — a review-required plan reaches `executing` only after the review **and**, when it raised findings, a dated dispositioning subsection | `doctrine/plans.md` | **Not satisfied.** The External review raised E1-E3; this Response is the disposition, but doctrine names the artifact a `### Sharpening` subsection under the review heading, and this is an H2 `## Response` following the plan's own established form. Flagged, not silently reconciled. |
| `doctrine/plans.md:503` — *"Chunk-table cells are edited inline when sharpening accepts a finding; the Sharpening subsection NAMES which cells changed and why"* | `doctrine/plans.md` | **Not satisfied, and this is the important one.** This Response was authored under an append-only constraint, so the chunk tables at Chunk A/B/C still read as they did before A1-A33. The amendments are binding by reference, **but the plan's executable contract has not been folded in place**, and doctrine's stated reason is exactly the risk here: *"the implementer reads the corrected chunk, not the obsolete one"*. An agent authorized to edit in place (the Maintainer, or the implementer at implementation start) must fold A1-A33 into the chunk cells **before** any code lands. An implementer who reads only Chunk B will build the waiver-pinning B9 that [E1] rejects. |
| Plan status token | plan header: `**Status**: open` | **Not satisfied.** `doctrine/plans.md:114` says a review-required plan opens in `awaiting-plan-review`. The header carries `open`. A lifecycle flip is not this Response's to make. |
| Sequence step 0 — *"plan-open -- this plan + the dev/PLANNING.md row-move [commit pending]"* | *Sequence* | **Not satisfied.** `dev/PLANNING.md` carries **no row for `separator-detection`** — verified by grep over the whole board today; the three `separator` hits are unrelated `byline-classification` text at `dev/PLANNING.md:368` and `:380`-`381`. The plan-open serialization is incomplete. `dev/PLANNING.md` is a serialized shared file and this Response does not edit it. |
| Maintainer fence **F1** — the frozen-file re-pin | *Maintainer fence* | **Not due yet, correctly not discharged.** Both target files are in the 164-entry `frozen_files` map (verified today); the re-pin is post-landing and Maintainer-only. |
| Maintainer fence **F2** — one ceremony for two plans | *Maintainer fence*, as amended by A13 and now **A28/A29** | **Not satisfied, and now conditional.** Its precondition (an exact, reviewed, bounded set) has no mechanical enforcement — measured above — and the ambient gate state is 60 violations wide. |
| *"No active batch window"* — the batch-window HOLD-by-default | *Maintainer fence* | **Satisfied.** `dev/plans/archive/gate-reanchor-preflight.md` exists, so the plan is archived and the HOLD is not in force. Re-confirm at implementation, per the plan's own instruction. |
| Decision conditions — signature change owned here; both plans carry the coexistence test; whichever lands second rebases onto the yielded-id form | Decision, `dev/proposals/archive/2026-08-03-claude-separator-detection.md:441`-`452` | **Satisfied as planned**, and unchanged by this Response. B7 carries the coexistence test; A32 keeps its class name distinct; A21's refusal narrows *within* *"each marker suppresses only its own id"* rather than against it. |

### Does this Response clear the plan to implement?

**No.** Four reasons, in descending order of how badly each would bite an
implementer who started today.

1. **The plan's executable contract has not been amended in place.** A1-A33 are
   binding by reference, but Chunk A/B/C still read as written. Doctrine
   requires the inline fold precisely so *"the implementer reads the corrected
   chunk, not the obsolete one"* (`doctrine/plans.md:503`). An author Response
   is **evidence of intended changes, not a replacement for the plan's
   executable contract** — and here the gap is not cosmetic: an implementer
   reading only Chunk B builds the B9 that pins the waiver [E1] rejects, and
   runs a P-B7 that I have measured **no longer falsifies anything**.
2. **[E1]'s remedy is new production behaviour the External reviewer has not
   seen.** The reviewer asked for a refusal and I built one; but a suppression-
   grammar change to a shipped security control, added *after* the security-lens
   read, is exactly the material that read exists to examine.
   `doctrine/plans.md:391`-`393` treats a revision that materially expands scope
   as warranting a review pass before chunks land. A **round-2 External
   confirmation** is owed, scoped to A20-A24 and A26 — and specifically to
   whether *"renders on the same display line"* is the right association
   predicate, and whether refusing the block form is acceptable.
3. **[E2] is dispositioned but not dischargeable by any agent.** The bounded
   ceremony A29 mandates has no mechanical enforcement, and the enumeration it
   turns on is a Maintainer act. The plan may not land its second chunk on the
   assumption that the ceremony will be available.
4. **Two lifecycle gates are open**: the plan's status token is `open` where
   doctrine requires `awaiting-plan-review`, and `dev/PLANNING.md` has no row
   for this plan at all. Both are serialization-point acts, not this Response's.

**An author Response never discharges a review tier.** The External tier's
round-1 findings are dispositioned here; the tier is *not* thereby closed, and
nothing in this section moves the *"no implementation commit lands before"* line
in the plan header.

**What the round-2 External reviewer should attack first**, superseding the
five-item list in the previous Response:

1. **A20/A21/A24 — the association predicate.** Is *"the marker renders on the
   same display line as the separator"* the right rule, or should the id be
   unsuppressible outright? Check the block-form refusal, which I measured but
   did not ask anyone about.
2. **A26 — the two-site perturbation.** Verify that the single-site P-B7 really
   yields 9 passed against the remedied build. If it does not, my whole account
   of why the remedy neuters the old perturbation is wrong, and that is the
   cheapest thing in this Response to falsify.
3. **A29 — whether a conditional ceremony is a gate or a wish**, given that
   nothing refuses an out-of-set member and the set moved 17 -> 60 in a day.
4. **A30/A31 — whether an in-file AST guard is the right instrument**, or
   whether the guard belongs across `bootstrap/tests/` rather than in the one
   file two plans happen to collide in.
5. **Re-run the corpus sweep** (0 hits today) and confirm A33's rule that the
   plan should state no denominator.

This section is append-only.

## Plan review -- Codex (External) -- 2026-08-05

**Tier**: External
**Findings**: raised

**Verdict: REVISE.** A20--A32 substantively answer my prior findings: the
unsafe waiver is refused, the ceremony requires bounded human enumeration, and
the AST guard covers duplicate classes and methods. But these decisions remain
binding only by reference from an amendments table. The original Chunk B still
instructs an implementer to build the waiver that A20 rejects.

That is not an executable contract for an implementer who follows the chunk
table, and the plan's cited doctrine requires amendments to be folded into the
affected chunk cells before implementation. Fold A1--A33 into the operative
chunk rows and acceptance criteria, removing or replacing superseded
instructions rather than asking execution to reconcile two grammars. Then seek
a focused External confirmation of the folded B9/B10 refusal and ceremony
contract.

### Sharpening

Re-measure counts during that fold rather than preserving historical figures.
The current canonical-interpreter focused baseline is 104 passing tests across
`test_content_scan.py` and `test_security_stack.py`; the older security-stack
count cited in review history is already stale because of unrelated landed
work. That does not change this verdict, but it illustrates why the chunk should
name the command and invariant rather than freeze an incidental denominator.

### Sharpening -- Claude (author) -- 2026-08-05 (the inline fold of A1--A33)

**Model**: claude-opus-5. **Standing**: plan author, performing the inline fold
the round-2 External verdict requires. Written at revision `ec57bf0` under
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13),
`PYTHONDONTWRITEBYTECODE=1`.

**Maintainer disposition of the REVISE round.** The authorizing instruction,
quoted verbatim and visually isolated:

> Go ahead with implementation once you've revised these. I don't want another review round

That instruction disposes of **the review round**, which is exactly the escape
this plan's own fence contemplates ("the External reviewer, *or the Maintainer*,
disposes of the REVISE"). It is **not** a bypass of the plan-review precondition:
the required External section is in the tree, and the Maintainer holds the
standing to dispose of its findings. Read narrowly, as it must be: it supplies
**no** Maintainer credential, **no** signing ref, **no** AST re-anchor ceremony,
and **no** approval to push. The re-pin fence (F1) and the bounded-ceremony
condition (F2) are untouched by it and remain Maintainer-only. The one thing it
closes beyond the round itself is the "focused External confirmation of the folded
B9/B10 refusal and ceremony contract" the verdict asked for — that is
**dispositioned, not performed**, and it is recorded as known omission (g) rather
than claimed as coverage.

**Doctrine basis for editing chunk cells in place.** `doctrine/plans.md:202`--`207`
makes chunk-table cell text mutable in place **pre-implementation only** (plan
status `open`; no commits in flight against the chunks being edited), and says
inline edits driven by accepted plan-review findings land there with a Sharpening
subsection naming which cells changed and why. This plan's status is `open` and it
has no implementation commit, so the premise the previous Response worked
under — that append-only forbade the fold — was false. **All 33 amendment rows are
now folded**; each row in both amendment tables carries a `Folded into (2026-08-05)`
column naming the cell that carries it. That column was **appended**, so every
existing amendment cell is byte-identical to what was committed (verified by
diffing the row prefixes). No `## Plan review`, `## Response to plan review`,
`## Code review`, `### Sharpening` or `### Figure correction` text was rewritten.

**Cells changed, and why.**

* **Header** — added a `**Review disposition**` field carrying the quoted
  authorization and the narrow reading, plus the instruction to read the chunk
  table rather than the amendment tables. `Last update` -> 2026-08-05.
* **Sequence** — the plan-review line now records both External rounds by commit
  and the Maintainer disposition; the Chunk B line names B10 and B11; a
  **Cross-plan ordering** note carries A17 -> A32's binding re-read rule.
* **The measurements > alarm fatigue** — A19 -> A33: the denominator is gone from
  the figure, the code block, and the prose. Only the hit count and its date
  remain.
* **Scope** — A22: three sites -> **four**, naming the final filter at
  `content_scan.py:409` and the new helper. A15: the grep figure is re-derived and
  explicitly demoted — the conclusion now rests on the `content_scan_runner.py`
  fingerprint argument, with `bootstrap/security_check.py`'s `scan_targets()`
  added as a second case where grep would have falsified a true claim.
* **Maintainer fence** — A14 applied to **F1** (name the two files, state no
  total). A28 rewrote **F2**'s heading and preamble; A29 replaced its bullets with
  the bounded-ceremony condition, the *checked-by-opening-it* finding that
  `_gate_preflight.py:1164`--`1170` computes counts and refuses nothing, and the
  explicit statement that **this plan builds no gate**.
* **Chunk A acceptance** — A18: the `25 nodes` count is replaced by a node-id-set
  superset invariant with a named command. The behaviour-identity bullet now states
  why the material cannot come from the artifact under test.
* **Chunk B** — the chunk that carried the reviewer's named contradiction.
  * Row **B3** gained A9 -> A24's two docstring clauses (display-line association;
    the block form does not suppress).
  * Row **B4** gained A16 (both code points **and** the widened guard reading the
    test module's own path).
  * Row **B5** gained A4 (parametrized into two nodes).
  * Row **B6** is **replaced** by **B6a** and **B6b** (A1); B6b is marked as the
    security-critical assertion whose only perturbation is the two-site P-B7.
  * Rows **B9a / B9b / B9c** replace the pinning **B9** (A6 -> A20). **This is the
    contradiction the reviewer named, and it is gone**: the cells now *refuse* the
    cross-separator acceptance and pin the honoured path, and each says in so many
    words *do not build the pin*.
  * Row **B10** is new (A21) — the production refusal.
  * Row **B11** is new (A30) — the AST duplicate-name guard, covering duplicate
    **classes and methods**.
  * A **Test-class naming** note carries A32 and names which rows are production.
* **Chunk B acceptance** — A10 (suite delta, no absolute), A18 (node-id set), A12
  (`check_cairn` delta plus scoped-clean, **without** the clause the Figure
  correction withdrew), A33 (independent sweep, no denominator), A5 (P-B2 both
  directions), A2 (P-B3 -> B6a only), A26 (P-B7 two-site, with the explicit warning
  that the one-site form is a false ledger entry), A25 (P-B8 -> the refusal, with
  the superseded `{i, i+1}` form marked *do not run*), A31 (P-B9). The
  future-states and channel-note bullets now cover B9a--B9c, B10 and B11.
* **Chunk C** — row **C1** gained A27 (the release note must state the
  acceptance-association rule and the block-form refusal).
* **Plan-level acceptance** — A11 (delta), A18, the new node list, and the
  perturbation count corrected from **six to eleven** with the two test-source
  perturbations named and justified rather than glossed.
* **Author-accounting** — A23 (edge case: divergence closed for this id, and the
  superseded pin called out), A24 (the association invariant, the refused-marker
  failure mode), A1 (B6a/B6b invariant split), A30/A31 (collection-integrity
  invariant), A33 (alarm-fatigue bullet), plus known omissions (a) rehomed to
  `content-scan-detectors`, (f) B11's residual, (g) the dispositioned confirmation.
* **Verification** — A33 (sweep with no denominator, and *not* via `check_cairn`),
  A14 (gate-integrity note), the node-id-set capture added, "six perturbations"
  -> eleven with the record-named-nodes rule, and a correction of the templated
  slot's "the same ones CI enforces" wording.
* **Lasting-truth migration** — one row **appended** (A24's residue). No existing
  entry edited; the section's own rule is append-only and that is what was done.

**Figures re-derived at revision `ec57bf0`, `as_of 2026-08-05`** (nothing carried
forward):

| Figure | Previously stated | Measured now | Disposition |
|---|---|---|---|
| Corpus sweep hits / denominator | 0 of 494; 0 of 511; 0 of 520 | **0 hits**, all tracked files decoding as UTF-8 | verdict holds; **denominator deleted** everywhere (A33) |
| `test_content_scan.py` collection | 25 nodes | 25 collected, 25 passed | **count removed from every criterion**; replaced by a node-id-set superset invariant |
| Focused pair `test_content_scan.py` + `test_security_stack.py` | 104 (reviewer's sharpening) | **104 passed** | reproduces; **not** written into any cell — it is not this plan's surface and would be another frozen denominator |
| `quality_gate.py --sub neutrality` | `fail=95` `as_of 2026-08-04` | `fail=95 info=21` | reproduces; predicate restated as a delta, figure kept only as a labelled orientation snapshot |
| `frozen_files` entries | 164, both target files present | **164**, both present | reproduces |
| Whole-tree `check_cairn` | 180 files / 195 files / 176 files | `OK -- 177 Markdown file(s); no issues; 48 external link(s) not probed` | **fourth distinct count in four readings**; no count written into any cell, verdict-only predicate retained |
| `_gate_manifest.py verify` violations | 17 (08-04) -> 60 (08-05 am) | materially larger again the same afternoon | **count deleted from F2** per A29's own rule; the enumeration is taken at ceremony time |
| Cited line numbers: `content_scan.py` `:45` `:137` `:144` `:193` `:240` `:259` `:261` `:295` `:376` `:390` `:401`--`403` `:409`; `test_content_scan.py` `:48`--`52` `:65`; `_gate_manifest.py` `:165`--`167` `:364`; `check_cairn.py` `:91`--`94`; `content_scan_runner.py` `:299` `:403`; `security_check.py` `:63` | various | **all resolve**, character-for-character where quoted; the ternary is still at `content_scan.py:402` | reproduce |
| `_gate_preflight.py` blessing scope is counts-only | `:1163`--`1170` | **`:1164`--`1170`** is the `scope = {...}` dict of `sum(1 for ...)` counts; names no paths, refuses nothing | citation corrected by one line; the finding is unchanged |
| AST duplicate-name guard prototype | clean on the real module; flags both hazard shapes | **clean** on `test_content_scan.py`; on a 4-line hazard module (one class defining `test_one` twice plus `test_two`) the prototype flags `duplicate method <Class>.test_one` and pytest collects **2 of 3** nodes silently | reproduces. The hazard module was a scratch file, not a tree artifact; construct it to re-check |

**Three figures I deliberately did not restate rather than carry.** (1) Every
perturbation pass/fail total in the review history — they were measured against a
node set this fold changes (B5 -> 2 nodes, B6 -> 2, B9 -> 3, B11 new), so the cells
now specify **which named nodes** go red and green. (2) Any absolute whole-suite
figure — the predicate is a delta and running the 1700-node suite here would only
mint a fourth stale number. (3) The security-stack count the reviewer flagged as
stale; the reviewer's own point is that a chunk should not freeze it.

**One deviation from an amendment's literal text, recorded rather than slipped
in.** A30 names the guard's class `TestCollectionIntegrity`. A32 makes
plan-specific test-class names **binding on both plans**, and B11's own residual is
that a duplicate of its class name silently shadows the guard itself — a generic
name is the most likely collision in the tree. The two amendments conflict, so the
fold applies the later binding one: the class is
`TestSeparatorDetectionCollectionIntegrity`. Named in the B11 cell and here.

**Verification post-sharpening.**

* `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py
  dev/plans/separator-detection.md` -> clean, no hard flags.
* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py
  dev/plans/separator-detection.md` -> OK, no issues.
* The plan re-reads coherently end-to-end, and the chunk table now stands alone:
  an implementer who reads only Chunks A--C executes the post-[E1] contract, builds
  the refusal instead of the waiver, and runs no perturbation this fold has
  invalidated.

This subsection is append-only.

## Implementation note -- Claude -- 2026-08-05

**Scope, stated first so this is not mistaken for the plan's implementation
record.** Chunks A and B were implemented and verified by a **sibling session**
(`8a7fb86`, `a23be80`, `83d5b9b`). This section records **one** follow-on commit
of mine plus **one** finding, and nothing else. It is **not** the plan's
`## Implementation verification` record and does not discharge the code-review
tier.

### The commit -- B11's guard covered two of three silent-shadowing forms

`d5909b4`. B11's cell enumerates *(i)* duplicate top-level `ClassDef` and
*(ii)* duplicate method within a class. A **duplicate top-level function**
shadows exactly as silently, and this file is exposed to it: it carries a
top-level `def test_content_security_module_installs_scanner_verbatim`, and
`content-scan-detectors` appends here. The guard now checks top-level
`FunctionDef` / `AsyncFunctionDef` names too, reporting `duplicate top-level
function: <name>` -- **all** top-level functions, not only `test_*`, because a
shadowed `_ids` helper breaks the file the same way.

**This is beyond the letter of the B11 cell and is recorded here so the plan
text is not narrower than the code.** It adds no node, no class, and no shipped
byte: the existing node got stronger. Test-only, and trivially revertible if the
Maintainer would rather the cell bound the code.

Perturbation ledger -- hazard-side, all RUN under
`~/conda_envs/lhm/bin/python3.13` (3.13.13), `PYTHONDONTWRITEBYTECODE=1`,
`as_of 2026-08-05`; restore verified byte-identical by `git hash-object`
against a copy held outside the tree, not by `git diff`, because the change was
uncommitted at perturbation time:

| # | Mutation | Red | Green |
|---|---|---|---|
| P1 | duplicate top-level function appended | B11 **alone**, naming it | 35 |
| P2 | the same hazard against the **pre-extension** guard | none -- 36 passed | — |
| P3 | duplicate top-level class (`TestSeparatorDetection`) | B11 alone | 28 |
| P4 | duplicate method in that class | B11 alone | 35 |

P2 is the half that shows the extension does the work rather than the
pre-existing checks. P3/P4 confirm the two original forms still fire after the
loop refactor.

**One measurement worth keeping.** Under P1 collection stays at **36** either
way -- the shadowed node is lost and the shadowing one gained, so the totals
match. The plan asserts this as its reason for making the criterion the node-id
**set**; it is now demonstrated *in this file* rather than on a standalone
hazard module.

### Finding -- B3 clause (ii) is true, and has no independent falsifier

The shipped docstring tells adopters the **block form** (`cairn-accept` …
`cairn-accept-end` spanning the hit) does not suppress `unicode-line-separator`.
**Measured true** against the shipped `scan_text` (`as_of 2026-08-05`): a block
opened on file line 1, hit on line 3, closed on line 5 still yields
`[(3, "unicode-line-separator")]`; the associable case (marker before the
separator on the hit's own line) still returns `[]`.

**But no node pins it, and none usefully can.** Clause (ii) and the
preceding-line half of clause (i) are **one mechanism**, not two: the re-emit
branch asks only whether the *hit's own file line* carries an associable
marker, and in both cases it does not. Every mutation that reddens a
block-form node also reddens **B9b** -- deleting the B10 branch (P-B8) reddens
B9a and B9b; making re-emission conditional on the hit line carrying any marker
reddens B9b as well. So a block-form node would add a green light without
adding discrimination, which is the "test that could not fail alone" shape this
plan is otherwise careful about. **No node was added.**

The plan's own rule applies -- *"Where a claim cannot be perturbed, this plan
says so rather than implying coverage"* -- and B3's *"measured, not inferred"*
currently reads as independent coverage. Recorded here rather than fixed in the
cell, because the cell is post-review text and the correction is a wording call
for the Maintainer or the code reviewer.

### Not done

**Chunk C is untouched and remains deferred**, on its own terms: `CHANGELOG.md`
is a serialized shared file, the cell says the line is *"deliberately not an
implementation commit"*, and a standalone `CHANGELOG.md` edit is outside the
no-approval carve-in in `AGENTS.md` > *Git and commit workflow*. Its
one-line-for-both-plans rule also wants `content-scan-detectors`' state, which
had not landed.

This section is append-only.

## Implementation record -- Codex -- 2026-08-05

Chunks A and B were already implemented in `8a7fb86` and `a23be80`, with the
comment-only repair `83d5b9b` and the test-only collection-integrity extension
`d5909b4`. The implementation follows the folded contract: `_scan_unicode`
supplies literal pattern ids; U+2028/U+2029 emit
`unicode-line-separator`; own-id suppression is accepted only before the
separator on the same display line; later, preceding-line, and block-form
acceptances are refused; and duplicate top-level functions, classes, or methods
are detected in the shared test module.

Chunk C is now complete at the shared changelog serialization point. The single
Added entry covers both scanner plans, names the raw separators and their own
pattern id, states the same-display-line acceptance rule and block-form refusal,
and preserves the variation-selector upgrade consequence.

The implementation commits carry the complete P-A1/P-A2 and P-B1--P-B9
perturbation ledgers, including the two-site P-B7 result: changing only either
suppression site remains green, while changing both makes the foreign-id marker
test red. The B11 extension separately proves that duplicate top-level function
names evade its predecessor while the extended guard catches them. Restores
were verified byte-identical in those commits.

**Stable evidence.** The canonical real-environment boundary at
`75da38349e0f804209234ef668aedbbd909caef1` includes all four implementation
commits and passed **2513 tests**, with zero failures, skips, xfails, or xpasses
under CPython 3.13.13. Rechecked after the three independent reviews and archive
serialization: `test_content_scan.py` reports **198 passed**;
`test_security_stack.py` reports **98 passed**; `scripts/check_cairn.py` is clean
over 173 Markdown files; and this plan's claim check is clean.

The plan enters `review`. The independent security code reviewer should cover
`8a7fb86`, `a23be80`, `83d5b9b`, `d5909b4`, the later
`content-scan-detectors` coexistence changes, the implementation note's
block-form coverage finding, and this changelog serialization. The two frozen
files remain deliberately unpinned. Only after this review ships may the
Maintainer evaluate the exact-path bounded shared ceremony with the
already-SHIP-reviewed `content-scan-detectors` plan.

## Code review -- Codex -- 2026-08-05

**Role:** External security code reviewer; different agent type from the Claude
implementation sessions. **Verdict: REVISE.** The detector, literal pattern-id
dispatch, cross-separator refusal, coexistence behavior, and collection-shadow
guard otherwise match the folded contract. One suppression interaction remains
blocking.

### [CR1] HIGH -- an accepted first separator hides an unaccepted second separator

The detector deliberately emits one `unicode-line-separator` flag per file line
and names the first separator. `_separator_accept_is_associable` accepts a valid
marker before that first separator, but it does not check whether the same file
line carries another separator. The accepted first hit therefore suppresses the
line's only flag, and a second separator plus injected display-line content is
never represented.

Reproduced through the production `scan_text` at `36d8122` under canonical
Python 3.13.13. This input returned `[]`:

```text
<valid unicode-line-separator marker> U+2028 benign U+2028 ## Injected header
```

That weakens the same-display-line association rule: the marker is visually
associated with the first separator, not the second injected display line. It
also gives a contributor a clean-result transformation using an existing valid
acceptance marker.

**Required correction.** Preserve the Decision's one-flag-per-file-line limit,
but honor an acceptance only when the hit line contains exactly one member of
`_LINE_SEPARATORS`. With two or more, refuse the suppression and retain the one
flag naming the first. Add a regression combining a valid marker, an accepted
first separator, and a second separator with injected header text. The existing
single-separator acceptance test must remain green. I executed this rule by
temporarily wrapping the production helper: the legitimate one-separator case
remained `[]`, while the two-separator attack returned
`[(1, "unicode-line-separator")]`.

### Verification and bounds

Before the attack, canonical focused execution reported **198 passed** in
`test_content_scan.py` and **98 passed** in `test_security_stack.py`;
`check_cairn` and this plan's claim check were clean. I also executed the
documented block-form refusal through production and observed the separator
flag survive, and verified marker-after-separator and foreign-id markers remain
refused. I did not run the frozen re-pin, alter Maintainer refs, test a GUI
renderer's Unicode line-breaking, or independently replay every historical
P-A/P-B mutation. The broad 2513-test record predates the correction now
required and will be invalidated when executable/test bytes change.

## Corrective implementation -- Codex -- 2026-08-05

CR1 is corrected in `0d02d5d`, with the self-hosted twin synchronized in
`e131b33`. `_separator_accept_is_associable` now requires exactly one member of
`_LINE_SEPARATORS` on the file line before it considers a marker. The existing
single-separator acceptance remains valid; a line with two or more separators
retains the one declared flag naming the first, so accepting that first boundary
cannot hide a later display line.

`TestSeparatorDetection::test_second_separator_cannot_piggyback_on_accepted_first`
is the direct regression: valid own-id marker, accepted U+2028, benign text,
second U+2028, injected header. It failed against the reviewed production
behavior (`scan_text` returned `[]`) and passes against the correction with
`[(1, "unicode-line-separator")]`. The shipped module docstring and shared
changelog entry state that multi-separator file lines are unsuppressible.

**Focused verification.** Canonical Python 3.13.13 with
`PYTHONDONTWRITEBYTECODE=1`: `test_content_scan.py` **199 passed**;
`test_security_stack.py` **98 passed**; `test_notice_install.py` **12 passed**;
Bandit reported zero findings in the template scanner; and `check_cairn` was
clean. `scripts/content_scan.py` and
`templates/modules/team-gated/content_scan.py` are byte-identical at SHA-256
`677d07fdb93a3978339b90f4415803069169028f7165f4c2d45641b0d2dd8ae7`.

**Broad-boundary ledger.** The first shuffled full run after `0d02d5d` reported
**2512 passed, 2 failed** in 341.36 seconds. Both failures were twin-parity
guards identifying the omitted `scripts/content_scan.py` synchronization; no
behavioral node failed. After `e131b33`, the same canonical command completed
with **2514 passed, 0 failed, 0 skipped, 0 xfailed, 0 xpassed**, plus three
third-party deprecation warnings, in 339.59 seconds. HEAD and tracked files were
unchanged during the final run.

This implementation does not self-clear the Codex review. A different-agent-
type or human correction review must reproduce the two-separator attack against
`e131b33`, confirm the one-separator acceptance remains green, and verify the
source/self-hosted twin identity. The bounded frozen re-pin remains unperformed
until that review returns SHIP.
