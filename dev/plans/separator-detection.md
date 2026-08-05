<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/lifecycle.md doctrine/coordination.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: ../proposals/2026-08-03-claude-separator-detection.md -->
<!-- ^ Source/sibling proposals archived 2026-08-04. These citations sit in
     append-only sections, so the path is exempted rather than rewritten. -->


# Plan: the two separators nothing detects — `U+2028` / `U+2029`

**Source proposal**: [`dev/proposals/archive/2026-08-03-claude-separator-detection.md`](../proposals/archive/2026-08-03-claude-separator-detection.md)
(accepted 2026-08-03 by Maintainer Decision, *as revised*). It sits under
`dev/proposals/` today and moves to `dev/proposals/archive/` when it archives.
**Status**: open
**Plan review**: required(**External**, security lens) — carried from the
proposal header and re-declared by the Decision's *Next transition* line, which
routes the tier into the plan "in its own right". The content scanner is a
shipped security control and its pattern-id set is an adopter-facing contract.
**No implementation commit lands before an External `## Plan review` section is
in the tree** (`doctrine/plans.md` > plan-review precondition). See
[*Plan review — the brief*](#plan-review--the-brief) for what the Internal round
about to run does and does not discharge.
**Last update**: 2026-08-04
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
tracked files read: 494 of 494
files with raw U+2028/U+2029: 0
```

**Zero, over 494 tracked files, `as_of 2026-08-04`** — every tracked file, not
only Markdown, so `templates/`, `bootstrap/`, `scripts/`, `docs/` and `dev/` are
all inside it. The rule ships silent on today's corpus. The signal to reconsider
did not fire; recorded here as the dated figure the proposal asks for, and
re-taken at implementation rather than quoted from here.

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

Within `content_scan.py` the Response named three sites, and all three are
verified present at HEAD: the module-docstring pattern-id list (the
`unicode-bidi` bullet ends at
`templates/modules/team-gated/content_scan.py:45`), the detector loops in
`_scan_unicode`, and the call site at
`templates/modules/team-gated/content_scan.py:401`.

Verified rather than assumed: `grep -rln "unicode-zero-width"` over the tracked
tree outside `dev/proposals/` and `dev/plans/` returns exactly those two files,
`as_of 2026-08-04`. In particular `templates/modules/team-gated/content-security.md`
does **not** enumerate pattern ids, and there is no self-hosted `scripts/`
twin of the scanner — `scripts/check_cairn.py:91`–`94` loads the template file
directly by path, so no twin-parity obligation is engaged.

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
`bootstrap/tests/fixtures/gate_manifest.json`, verified `as_of 2026-08-04`
(`templates/modules/**/*.py` and `bootstrap/tests/**/*.py` are both frozen-set
globs — `bootstrap/tests/_gate_manifest.py:165`–`167`). After this plan lands,
`python bootstrap/tests/_gate_manifest.py verify` reports **two
`FROZEN-MODIFIED` entries**. Re-producing the manifest is a supervised
prerequisite commit under `bootstrap/REANCHOR_RUNBOOK.md`, whose Phase 0 runs
under a clean child shell with recorded values and a signing backend. The
implementing agent's whole obligation is to **say so in the final commit body and
name the two files**.

**F2 — one ceremony for two plans, not two.** `content-scan-detectors` edits the
**same two files** and is being planned in parallel. Its frozen-file delta is the
identical pair. The batch rule this plan adopts:

* Neither plan re-pins.
* Whichever lands second records that **the same two entries** are stale — not a
  second, different pair.
* The Maintainer performs **one** supervised re-produce after both have landed.
* If only one of the two lands (the other is struck or deferred), the surviving
  plan's commit body is already correct and the ceremony is unchanged.

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
   (plan review) -- required(External, security lens); NO code before it lands
1. Chunk A -- _scan_unicode yields its own pattern id; the ternary dies [commit pending]
2. Chunk B -- the unicode-line-separator detector + its contract entry  [commit pending]
3. Chunk C -- the shared release note, at a serialization point         [deferred]
```

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

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_content_scan.py -q`
  → all pass, 0 skipped. Baseline **25 nodes** `as_of 2026-08-04`; collection
  grows by exactly the new node and drops none.
* **Behaviour identity, checked against a pre-change capture.** Before A1, write
  the full `(line, pattern_id, message)` tuple list for a five-probe fixture
  (`U+202E`, `U+200B`, `U+2060`, leading `U+FEFF`, non-leading `U+FEFF`) to a
  scratch file **outside the tree**; after A2, assert byte-equal. Simulated for
  this plan with the predicted result; the baseline must arrive from a
  pre-change execution, because the artifact under verification cannot supply
  it.
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

| # | File | Change |
|---|------|--------|
| B1 | `templates/modules/team-gated/content_scan.py` | New module constant `_LINE_SEPARATORS`, beside `_ZERO_WIDTH` (`templates/modules/team-gated/content_scan.py:137`) and `_BIDI` (`:144`), holding `U+2028` and `U+2029` **as `\uXXXX` escape forms with a naming comment each** — never raw. The existing comment block above `_ZERO_WIDTH` already states this rule (trojansource-safe, Bandit B613) and the new constant is placed under it so the rule covers it by adjacency, not by a second copy. |
| B2 | `templates/modules/team-gated/content_scan.py` | A third per-line loop in `_scan_unicode`, after the bidi loop, yielding `(i, "unicode-line-separator", f"unicode line/paragraph separator U+{ord(ch):04X}")` and breaking after the first hit on that line — **following** the existing per-category-per-line convention, which the Decision fixes as a declared limit. |
| B3 | `templates/modules/team-gated/content_scan.py` | Module-docstring pattern-id list: a `unicode-line-separator` bullet after the `unicode-bidi` bullet (which ends at `templates/modules/team-gated/content_scan.py:45`). It names both code points, says the detector **flags and never rewrites**, and states the declared limit in one clause. This bullet *is* the adopter-facing contract entry; a hit is only suppressible by a marker naming this id. |
| B4 | `bootstrap/tests/test_content_scan.py` | Extend `_BANNED_CODEPOINTS` (`bootstrap/tests/test_content_scan.py:48`–`52`) with `0x2028, 0x2029`, so `test_no_raw_banned_codepoints_in_source` now also refuses a raw separator in the scanner's own source. A scanner that smuggles the code point it detects is the exact failure this class of test exists for. |
| B5 | `bootstrap/tests/test_content_scan.py` | New `TestLineSeparator::test_each_separator_is_caught`: `scan_text` over a fixture carrying a raw `U+2028` and, separately, one carrying a raw `U+2029`; assert each yields exactly one flag with `pattern_id == "unicode-line-separator"` and a message containing `U+2028` / `U+2029` respectively. Escape forms in the test source, matching B4. |
| B6 | `bootstrap/tests/test_content_scan.py` | New `TestLineSeparator::test_marker_suppresses_only_its_own_id`: a `cairn-accept` marker naming `unicode-line-separator` clears the flag; a marker naming `unicode-zero-width` does **not**. The second half is the regression for the dispatch defect — it is red against the code at HEAD and red against any future reintroduction of the ternary. |
| B7 | `bootstrap/tests/test_content_scan.py` | New `TestLineSeparator::test_all_three_unicode_ids_trip_independently`: one three-line fixture (zero-width on line 1, bidi on line 2, `U+2028` on line 3); assert the `(line, pattern_id)` set is **exactly** `{(1, "unicode-zero-width"), (2, "unicode-bidi"), (3, "unicode-line-separator")}`. This is the coexistence test the Decision requires **both** plans to carry; whichever lands first turns it green and the second inherits it. |
| B8 | `bootstrap/tests/test_content_scan.py` | New `TestLineSeparator::test_two_separators_on_one_line_flag_once`: a line carrying `U+2028` then `U+2029` yields exactly one flag, naming `U+2028`. Pins the Decision's **declared limit** so a later author who changes the `break` semantics does so deliberately, against a red test and its own proposal, rather than by accident. |

**Acceptance criteria — Chunk B.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_content_scan.py -q`
  → all pass, 0 skipped, including
  `test_content_security_module_installs_scanner_verbatim` run **for real**
  (this plan's own measurement deselected it; the implementation may not).
* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` → the whole suite
  green, 0 failed / 0 skipped / 0 xfailed. **Take the baseline at implementation
  start, not from this plan**: the working tree carried other workflows'
  in-flight edits under `bootstrap/_scaffold/` `as_of 2026-08-04`, so any suite
  figure measured here would be measuring someone else's change.
* **The corpus sweep, re-run as the alarm-fatigue gate.**
  `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → OK. Baseline
  **180 Markdown files, no issues**, `as_of 2026-08-04`; the count may only grow
  and the verdict may not change. Independently, re-run the raw sweep over
  `git ls-files` and record the count in the commit body as a dated figure — 0
  of 494 today. **A non-trivial count is a signal to stop and reconsider, not to
  suppress**; if it fires, the disposition is a Maintainer question, not an
  inline `cairn-accept`.
* `~/conda_envs/lhm/bin/python3.13 -m bandit -q -f json
  templates/modules/team-gated/content_scan.py` → `errors: []`, zero findings.
  Measured on the prototype for this plan; re-take against the real edit. The
  file is in the release gate's scan set, so a MEDIUM+ finding here is a release
  blocker, not a lint nit.
* `~/conda_envs/lhm/bin/python3.13 scripts/quality_gate.py --sub neutrality` →
  `fail=95`, `as_of 2026-08-04`. `bootstrap/` is a neutrality scan root, so the
  test file passes through it; `templates/` is not. The figure must not move —
  and it is a dated snapshot taken over a dirty tree, so re-take the baseline
  before the edit rather than diffing against this line.
* **Perturbation P-B1 — B5 discriminates the detector (hazard-side, RUN).**
  Delete the B2 loop; B5 fails on both separators, B7 fails on the third pair,
  B8 fails. Restore; confirm `git diff` empty.
* **Perturbation P-B2 — B5 discriminates *each member*, not just the loop
  (hazard-side, RUN).** Remove `U+2029` from `_LINE_SEPARATORS`, leaving
  `U+2028`; B5's `U+2029` assertion fails **alone** while its `U+2028` assertion
  stays green. Repeat the other way round. Without this, a single-member
  constant would pass a loop-level perturbation and ship half the contract.
* **Perturbation P-B3 — B6 is the dispatch regression (hazard-side, RUN).**
  Revert Chunk A in place (restore the 2-tuple yield and the ternary) while
  keeping the B2 loop; B6's `unicode-zero-width`-marker half fails, because the
  separator flag is labelled `unicode-zero-width` and the foreign marker
  suppresses it. Reproduced for this plan against a scratch copy: NAIVE
  zero-width-marker → `[]`, FIXED → `['unicode-line-separator']`. Restore;
  confirm `git diff` empty.
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
  `0x2028`. Delete it; confirm `git status --short` clean. Never committed.
* **The future states in which B5–B8 fail**, named because that is the
  acceptance bar: (i) the detector loop removed or narrowed by a later refactor;
  (ii) the ternary reintroduced by whichever sibling plan lands second — the
  state the Decision's sequencing rule exists to forbid; (iii) the yielded id
  renamed without the docstring contract entry moving with it; (iv) the
  per-line `break` semantics changed as a rider on some other change.
* **Channel note.** Subject: `scan_text` through its public path — no stub of
  the function under test anywhere in B5–B8. Oracles: code-point literals and id
  strings typed into the test by a human, plus `unicodedata`'s categories quoted
  in the docstring. Nothing in the oracle is computed from `_LINE_SEPARATORS` or
  from the detector loop, so a gap cannot move both together.

---

### Chunk C — the shared release note

**Deferred, and deliberately not an implementation commit.** `CHANGELOG.md` is a
serialized shared file, edited only at a defined serialization point
(`AGENTS.md` > *Shared communication files*).

| # | File | Change |
|---|------|--------|
| C1 | `CHANGELOG.md > Unreleased > Added` | **One** line covering the pattern-id partition, shared with `content-scan-detectors` rather than duplicated: the content scanner's unicode detectors now carry their own pattern ids, and a raw `U+2028` / `U+2029` flags under `unicode-line-separator`. Cross-reference both proposals and both plans **by stem**, per `AGENTS.md`. |

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
  * `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` — the whole
    suite, green, **0 failed / 0 skipped / 0 xfailed**, under the canonical
    interpreter (3.13.13). Baseline taken at implementation start, for the
    reason given in Chunk B.
  * [`bootstrap/tests/test_content_scan.py`](../../bootstrap/tests/test_content_scan.py)
    — the dispatch-contract test (A3), the detection pair (B5), the
    suppression-isolation pair (B6), the coexistence set (B7), the declared
    limit (B8), and the widened hygiene set (B4). Baseline **25 nodes**
    `as_of 2026-08-04`; collection grows by exactly the new nodes.
  * **Every new test shown non-vacuous by a perturbation of the hazard**, with
    the ledger — the production-code change made, the failure observed with its
    message, the byte-identical restore confirmed by an empty `git diff <path>`
    — in the commit body. Six perturbations are specified above and every one of
    them edits `content_scan.py`; **none** edits an assertion. Where a claim
    cannot be perturbed, this plan says so rather than implying coverage.
* **Doc updates that must land.** Hand-authored, one surface: the
  `unicode-line-separator` bullet in the `content_scan.py` module docstring
  (B3), landing in the same commit as the behaviour. No generated docs, no
  snippet-synced blocks. `CHANGELOG.md` is Chunk C, deferred and shared.
* **Examples / smoke checks required.** `python scripts/check_cairn.py` over the
  whole tree — the shipped scanner run against Cairn's own corpus, which is
  simultaneously the doc gate and the live alarm-fatigue re-measurement.
  `python bootstrap/security_check.py` — expected `PASS`; the edited file is in
  the release gate's scan set. **N/A**: the runnable example gallery under
  `examples/` — this change touches nothing it demonstrates.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk and node that enforces it.**
  * *A raw `U+2028` or `U+2029` in scanned text produces at least one flag
    naming the code point.* Enforced by B5 in
    [`bootstrap/tests/test_content_scan.py`](../../bootstrap/tests/test_content_scan.py),
    perturbable by P-B1 and — per member — P-B2.
  * *That flag is suppressible only by a marker naming its own id.* Enforced by
    B6; the negative half (a `unicode-zero-width` marker does not suppress it)
    is the dispatch regression, perturbable by P-B3.
  * *`_scan_unicode` yields its pattern id; no caller derives one from message
    text.* Enforced by A3, perturbable by P-A1 (shape) and P-A2 (value). This is
    the invariant `content-scan-detectors` depends on and the reason the
    signature change is owned here.
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
  plan changes, and B5–B8 exercise it **through its public path** with no stub
  of it anywhere. `scan_file` is unchanged and reaches the same code by
  delegation, covered by the pre-existing red-team fixture node. A3 is the one
  node touching a module-private (`_scan_unicode`) — deliberately, because the
  thing being pinned *is* an internal signature that a sibling plan must rebase
  onto; it is named as a private-surface test rather than passed off as a
  contract test.
* **Failure modes.**
  * *Alarm fatigue.* → **Measured, 0 of 494 tracked files, `as_of 2026-08-04`.**
    Re-measured as a Chunk B gate. If the re-measurement is non-zero, the plan's
    instruction is to stop and route it to the Maintainer.
  * *Marker collision (a benign suppression silences an injected header).* →
    **Closed** by Chunk A + B6, and reproduced as an executed defect above
    rather than argued.
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
* **Edge cases handled.** A separator inside a `cairn-accept` marker's own line
  (line-scope covers the marker's own line — pre-existing semantics, unchanged).
  A separator at file index 0 (no BOM-style exemption applies; it flags, and it
  should — unlike `U+FEFF` there is no benign encoding role). A file with no
  trailing newline (`split("\n")` handles it; unchanged). Line numbering under a
  separator (measured above: `split("\n")` is unaffected, so reported line
  numbers stay physical).
* **Known omissions, stated rather than implied.** (a) No mechanical guard ties
  the docstring pattern-id list to the ids the code emits — the doc entry is
  enforced by review, not by test. (b) The plan asserts no full-suite baseline
  figure, because the working tree was dirty with other workflows' edits when it
  was written; the implementing agent takes it. (c) `Zs` space separators are
  untouched and remain a live Maintainer question on `byline-classification`.
  (d) Whether the per-line `break` convention should change at all is deferred
  to its own proposal; this plan only makes the current behaviour falsifiable.
  (e) No human has audited whether any *untracked* or generated artifact in an
  adopter tree carries these code points — the sweep is over Cairn's tracked
  corpus only.

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

**Plan-specific gates, added here because this change touches those surfaces.**

* **The release security gate** — `python bootstrap/security_check.py`.
  `templates/modules/team-gated/content_scan.py` is a verbatim shipped `.py` and
  is inside the scan set. Expected `PASS`.
* **Bandit, file-scoped, while iterating** — `python -m bandit -q -f json
  templates/modules/team-gated/content_scan.py`. Expected `errors: []` and zero
  findings; measured on the prototype for this plan.
* **The alarm-fatigue re-measurement** — the raw sweep over `git ls-files` for
  `U+2028` / `U+2029`, recorded in the commit body as a dated figure. 0 of 494,
  `as_of 2026-08-04`.
* **The behaviour-identity capture** — the pre-change `(line, pattern_id,
  message)` tuple list for the five-probe fixture, written to the session
  scratch directory before Chunk A and diffed after.
* **The perturbation ledgers** — six of them, per chunk, in the commit body: the
  production-code change made, the failure observed with its message, and the
  byte-identical restore verified by an empty `git diff <path>`.
* **The gate-integrity note** — after Chunk B, record in the commit body that
  `templates/modules/team-gated/content_scan.py` and
  `bootstrap/tests/test_content_scan.py` now differ from their pinned sha256 in
  `bootstrap/tests/fixtures/gate_manifest.json`, so a later
  `_gate_manifest.py verify` reports two `FROZEN-MODIFIED` entries — the **same
  two** `content-scan-detectors` will report. Do not re-pin; see
  [*Maintainer fence*](#maintainer-fence).

**Note on doc gates**: drift gates catch **drift**, not **absence** of a new doc
update. `check_cairn` will not notice if B3's docstring bullet is never written.
Confirm it by reading, and note that here it doubles as the alarm-fatigue
measurement, which is a different claim in the same command.

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

This section is append-only once written.

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

| # | Superseded text (verbatim) | Replaced by |
|---|---|---|
| A1 | Chunk B row **B6**, verbatim: `New TestLineSeparator::test_marker_suppresses_only_its_own_id: a cairn-accept marker naming unicode-line-separator clears the flag; a marker naming unicode-zero-width does **not**. The second half is the regression for the dispatch defect — it is red against the code at HEAD and red against any future reintroduction of the ternary.` | **Two nodes, not one.** `B6a` -- `TestLineSeparator::test_own_id_marker_suppresses`: a `cairn-accept` marker naming `unicode-line-separator` clears the flag. `B6b` -- `TestLineSeparator::test_foreign_id_marker_does_not_suppress`: a marker naming `unicode-zero-width` does **not** clear it; asserts `[f.pattern_id for f in scan_text(fixture)] == ["unicode-line-separator"]`. B6b is the dispatch regression and **must be independently falsifiable**, which a shared node cannot be. |
| A2 | `* **Perturbation P-B3 — B6 is the dispatch regression (hazard-side, RUN).** Revert Chunk A in place (restore the 2-tuple yield and the ternary) while keeping the B2 loop; B6's `unicode-zero-width`-marker half fails, because the separator flag is labelled `unicode-zero-width` and the foreign marker suppresses it.` | `* **Perturbation P-B3 — B6a is the dispatch regression (hazard-side, RUN).** Revert Chunk A in place (restore the 2-tuple yield and the ternary) while keeping the B2 loop; **B6a** fails -- the own-id marker matches nothing because the flag is labelled `unicode-zero-width`. Measured under this exact state: `AssertionError: own-id marker must clear / assert ['unicode-zero-width'] == []`. **P-B3 says nothing about B6b**, which does not execute in a single-node form and is not exercised by this perturbation; P-B7 is B6b's perturbation.` |
| A3 | *(added)* | `* **Perturbation P-B7 — B6b's negative half is non-vacuous (hazard-side, RUN).** In `scan_text`, widen the final filter (`templates/modules/team-gated/content_scan.py:409`) to suppress by line while ignoring `pattern_id`; **B6b fails alone** -- measured 1 failed, 4 passed, failing at the foreign-marker assertion. This is the only perturbation that falsifies the plan's security-critical assertion, and without it that assertion ships unfalsified. Restore; confirm `git diff templates/modules/team-gated/content_scan.py` empty.` |
| A4 | Chunk B row **B5**, verbatim: `New TestLineSeparator::test_each_separator_is_caught: scan_text over a fixture carrying a raw U+2028 and, separately, one carrying a raw U+2029; assert each yields exactly one flag with pattern_id == "unicode-line-separator" and a message containing U+2028 / U+2029 respectively. Escape forms in the test source, matching B4.` | **Parametrized into two nodes.** `TestLineSeparator::test_each_separator_is_caught` gains `@pytest.mark.parametrize("cp", [0x2028, 0x2029])`, so each code point is its own collected node asserting exactly one flag with `pattern_id == "unicode-line-separator"` and `f"U+{cp:04X}"` in the message. Escape forms in the test source, matching B4. A per-member claim requires a per-member node. |
| A5 | `Remove `U+2029` from `_LINE_SEPARATORS`, leaving `U+2028`; B5's `U+2029` assertion fails **alone** while its `U+2028` assertion stays green. Repeat the other way round.` | `Remove `U+2029` from `_LINE_SEPARATORS`, leaving `U+2028`; the `0x2029` **node** fails and the `0x2028` node stays green (measured on a single-node B5: 1 failed, 4 passed). Repeat the other way round: with B5 parametrized, the `0x2028` node fails alone. **On the un-parametrized node this direction does not work** -- measured 4 failed, 1 passed, with B5 aborting at its `U+2028` assertion so the `U+2029` assertion never runs, and B6/B7/B8 failing too because their fixtures use `U+2028`. A4 is what makes both directions symmetric.` |
| A6 | *(added)* | New Chunk B row **B9**, in `bootstrap/tests/test_content_scan.py`: `TestLineSeparator::test_separator_and_its_marker_share_one_scanned_line` — pin the measured interaction between the new code point and the line-scoped suppression grammar. (i) A payload and a `cairn-accept: unicode-line-separator` marker on **one** `split("\n")` line: the flag is cleared, though the two occupy two *display* lines. (ii) A marker on file line 1 clearing a hit on file line 2 that occupies four display lines. Both assert the **current** behaviour, so the node is a declared-limit pin in B8's sense, not a behaviour change. |
| A7 | *(added)* | `* **Perturbation P-B8 — B9's limit can fire (hazard-side, RUN).** Narrow the line-scope at `templates/modules/team-gated/content_scan.py:261` from `{i, i + 1}` to `{i}`; B9's second half fails because the preceding-line marker no longer clears the hit. Restore; confirm `git diff` empty. This perturbation is also the *proposal* a future author would need to change the grammar.` |
| A8 | `A separator inside a `cairn-accept` marker's own line (line-scope covers the marker's own line — pre-existing semantics, unchanged).` | `A separator inside a `cairn-accept` marker's own line — line-scope is **file**-line scope, and `U+2028` is the first detected code point for which a file line and a display line differ, so a marker and the payload it clears can be several display lines apart. Measured: a marker on file line 1 clears a `unicode-line-separator` hit on file line 2 spanning four display lines. Pre-existing semantics, **unchanged by this plan and now pinned by B9** rather than asserted benign.` |
| A9 | *(added)* | Two entries. **Invariant**: *A `unicode-line-separator` hit is cleared by an own-id marker on its own **file** line or the file line above, even when those are several display lines apart.* Enforced by B9, perturbable by P-B8. **Lasting-truth row**, deferred item *"The file-line-vs-display-line divergence in the suppression grammar"*, durable home *"The B9 pin plus the B3 docstring clause"*, written by *"Chunk B (B3 + B9)"*. Also: B3's docstring bullet gains one clause stating that suppression is scoped to **file** lines, which a separator can make differ from what a renderer shows. |
| A10 | `* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` → the whole suite green, 0 failed / 0 skipped / 0 xfailed. **Take the baseline at implementation start, not from this plan**: the working tree carried other workflows' in-flight edits under `bootstrap/_scaffold/` `as_of 2026-08-04`, so any suite figure measured here would be measuring someone else's change.` | `* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` → **as a delta against a baseline captured at implementation start**: no failure present that is absent from the baseline, no node dropped from collection, no new skip or xfail. Record both figures in the commit body. `as_of 2026-08-04` the tree is **1790 passed, 0 failed, 0 skipped, 0 xfailed** (178s) -- clean, but it was 3-failing days earlier, which is exactly why the predicate is a delta and not an absolute.` |
| A11 | `  * `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` — the whole suite, green, **0 failed / 0 skipped / 0 xfailed**, under the canonical interpreter (3.13.13). Baseline taken at implementation start, for the reason given in Chunk B.` | `  * `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` — under the canonical interpreter (3.13.13), **as the delta defined in Chunk B**: no new failure, no dropped node, no new skip/xfail against a baseline captured at implementation start.` |
| A12 | `` `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → OK. Baseline **180 Markdown files, no issues**, `as_of 2026-08-04`; the count may only grow and the verdict may not change.`` | `` `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → **no issue attributable to this change**, as a delta against an implementation-start baseline. `as_of 2026-08-04` the whole-tree run is **2 issues across 195 files** — both at `dev/PLANNING.md:886`-`887`, from commit `4573c11`, unreachable from this plan's two files. An absolute "→ OK" here is **not achievable** by an implementing agent who touches only `content_scan.py` and `test_content_scan.py`. Additionally run `scripts/check_cairn.py` scoped to the files this change touches, which must be clean outright.`` |
| A13 | `* Whichever lands second records that **the same two entries** are stale — not a second, different pair.` `* The Maintainer performs **one** supervised re-produce after both have landed.` | `* Whichever lands second records **the same two files** as the pair *this change* makes stale, and states plainly that `_gate_manifest.py verify` will report **others belonging to other workflows** — the plan asserts no total. Measured `as_of 2026-08-04`, before either plan lands: **HOLD, 17 violations — 10 `FROZEN-MODIFIED`, 3 `COLLECTION-DROPPED`, 4 `SKIP-XFAIL-NEW`**, none of them this plan's.` `* The Maintainer performs **one** supervised re-produce after both have landed, **scoped to whatever is stale at ceremony time** — which is a Maintainer review item, not a two-entry formality, and is a wider authority act than a two-file re-pin. `bootstrap/tests/_gate_preflight.py` refuses a dirty tree, but does not refuse other workflows' *committed* frozen-file edits.` |
| A14 | `so a later `_gate_manifest.py verify` reports two `FROZEN-MODIFIED` entries — the **same two** `content-scan-detectors` will report.` | `so a later `_gate_manifest.py verify` reports these two files among its `FROZEN-MODIFIED` entries — the **same two** `content-scan-detectors` will report. **Name the two files; do not state a total**, which is other workflows' to move and is stale by the time it is read.` |
| A15 | `Verified rather than assumed: `grep -rln "unicode-zero-width"` over the tracked tree outside `dev/proposals/` and `dev/plans/` returns exactly those two files, `as_of 2026-08-04`.` | Unchanged as a figure (it reproduces), **plus** this qualification: a literal-id grep cannot see a coupling that names no id. `templates/modules/team-gated/content_scan_runner.py` builds its reviewed-residual key as `f"{rel}:{pattern_id}:{code_hash}"` (`:299`, consumed at `:403`), so it is coupled to the **id set** without containing any id. That file is untouched here and no residual baseline churns, because Chunk A is id-preserving for both existing ids (measured: HEAD, A-only and FIXED produce byte-identical `(line, pattern_id, message)` tuples across the five probes) and the corpus carries **0** separator flags. The conclusion is reached by that argument, not by the grep. |
| A16 | `Extend `_BANNED_CODEPOINTS` (`bootstrap/tests/test_content_scan.py:48`–`52`) with `0x2028, 0x2029`, so `test_no_raw_banned_codepoints_in_source` now also refuses a raw separator in the scanner's own source.` | `Extend `_BANNED_CODEPOINTS` (`bootstrap/tests/test_content_scan.py:48`–`52`) with `0x2028, 0x2029`, **and widen the guard to read both `CONTENT_SCAN_SRC` and the test module's own path** (today it reads `CONTENT_SCAN_SRC` only, `bootstrap/tests/test_content_scan.py:65`). After B5–B9 the test module is itself a file whose fixtures are separator code points, and "escape forms in the test source" is otherwise a convention with nothing enforcing it. Verified the widening does the work: with a raw `U+2028` planted in a source comment, the pre-existing set reports no hits and the widened set reports `0x2028`.` |
| A17 | *(added, Sequence + Chunk B)* | **Shared-node naming convention, binding on both plans.** The coexistence node lives in a class named for its owning plan — `TestSeparatorDetectionCoexistence` here, and `content-scan-detectors` uses its own distinct class name. Measured hazard: a duplicate `class TestLineSeparator` in one module **shadows the entire earlier class** — a 5-method class followed by a 1-method class of the same name collects **1 test**, silently, no error, no warning. Whichever plan lands second must re-read the file rather than append blind. |
| A18 | `Baseline **25 nodes** `as_of 2026-08-04`; collection grows by exactly the new nodes.` | `Baseline **25 nodes** `as_of 2026-08-04` (re-measured; all 25 pass at HEAD). **Assert the collected node-id set, not its size**: capture `--collect-only -q` before and after and require the new set to be a strict superset of the old. A count check cannot distinguish "n nodes added" from "n+k added, k shadowed away" — see A17.` |
| A19 | `**Zero, over 494 tracked files, `as_of 2026-08-04`**` (and the two further occurrences of the 494 denominator, at the Chunk B sweep gate and the *Failure modes* alarm-fatigue bullet) | `**Zero, over 511 tracked files, `as_of 2026-08-04`** — re-measured at HEAD `6618e54`: 511 listed, 511 decode as UTF-8, **0** carry a raw `U+2028` or `U+2029`. The verdict is unchanged; only the denominator grew, as the review predicted. Re-take at implementation rather than quoting either figure. |

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
