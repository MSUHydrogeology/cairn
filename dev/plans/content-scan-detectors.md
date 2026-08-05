<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/lifecycle.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: dev/proposals/2026-08-03-claude-content-scan-detectors.md, dev/proposals/2026-08-03-claude-default-security-stance.md, dev/proposals/2026-08-03-codex-api-web-security-modules.md, dev/proposals/2026-08-03-claude-identity-not-name.md -->
<!-- ^ Source/sibling proposals archived 2026-08-04. These citations sit in
     append-only sections, so the path is exempted rather than rewritten. -->


# Plan: the scanner's character model — an invisible channel it cannot see, and a script it cannot tell from a spoof

**Source proposal**: `content-scan-detectors` (accepted 2026-08-03 by Maintainer
Decision, *"as revised"*). It sits at
`dev/proposals/archive/2026-08-03-claude-content-scan-detectors.md` and moves to
`dev/proposals/archive/` when it archives.
**Status**: open
**Plan review**: required(**External**, security lens) — carried from the
proposal header and restated in the Decision (*"The plan carries
`required(External, security lens)` in its own right; this Decision does not
discharge it."*). **No implementation commit lands before a review section is in
the tree.** See *Plan review — the brief* for why the Internal round about to run
is a floor and not the tier.
**Last update**: 2026-08-04
**Opened**: 2026-08-04

## Notation convention — this plan file is letter-ASCII by construction

Every non-ASCII letter and every invisible code point in this plan is written in
`U+XXXX` notation, never as a raw character: `<U+03C1>assword`, not the raw
mixed-script token. Two reasons, both learned inside the source proposal's own
record:

* The proposal's Internal review demonstrated an invisible-character finding by
  writing the character raw, and thereby planted two live instances of the
  hazard in the very section that certified their absence. The Maintainer
  direction repaired them and settled the general form by convention: *a review
  demonstrating an invisible character writes it as `U+00AD`, never as the raw
  byte.* A plan for that same detector is the last file that should break the
  convention.
* It costs this plan **zero** `cairn-accept` markers. A plan carrying
  suppression markers for the detector it is planning is a plan that cannot be
  used as its own regression fixture.

Where a test needs the literal character, the test source uses `\uXXXX` escape
forms — the convention `bootstrap/tests/test_content_scan.py` already follows and
`TestSourceCarriesNoRawInvisibles` already enforces for the scanner.

## Proposed paths

*Forward references — paths that do not resolve yet and materialize as the
lifecycle advances.*

Proposed paths:
- `dev/proposals/archive/2026-08-03-claude-content-scan-detectors.md` — where the source proposal lands at archive time.
- `dev/proposals/archive/2026-08-03-claude-separator-detection.md` — where the sibling proposal lands at archive time.

## Source proposal

`content-scan-detectors` settles the **character model** underneath two shipped
detectors in `templates/modules/team-gated/content_scan.py`, in both directions
at once:

* **Change 1 — an entire invisible channel becomes visible.** A new detector over
  RFC 8264 (PRECIS) § 9.13 `PrecisIgnorableProperties` —
  `Default_Ignorable_Code_Point` union `Noncharacter_Code_Point` — held as
  hard-coded numeric range tables. At HEAD an override-plus-exfiltration payload
  re-encoded one-for-one into the Unicode Tag block produces **zero** flags while
  its ASCII twin produces two.
* **Change 2 — the homoglyph rule becomes confusability-aware.** "Any two script
  ranges in one token" becomes a three-clause rule pivoting on whether a
  character actually has an ASCII-Latin look-alike, so ordinary scientific
  notation stops being reported as a prompt-injection attempt.

The plan executes that decision. It does not re-litigate it.

### Glossary — every term glossed on first use

The audience is a scientist who codes, and this scope is dense in Unicode
vocabulary that is easy to nod at and hard to hold.

* **Code point** — a number Unicode assigns to a character, written `U+00AD`.
  Distinct from how it *renders*: some code points render as nothing at all.
* **Default_Ignorable_Code_Point** — a Unicode property marking code points a
  conforming renderer may draw as nothing. It is a **derived** property, not a
  general category, and its members span several categories.
* **General category** — Unicode's coarse classification (`Lo` letter-other,
  `Mn` mark-nonspacing, `Cf` format, `Cn` unassigned). `unicodedata.category`
  exposes it. It is **not** Default_Ignorable, and confusing the two is finding
  [I4] in the source proposal's record.
* **Noncharacter** — a code point permanently reserved never to be assigned
  (`U+FDD0`–`U+FDEF`, and `U+nFFFE`/`U+nFFFF` on every plane). All are `Cn`.
* **The Tag block** — `U+E0000`–`U+E007F`, a complete shadow ASCII alphabet that
  renders as nothing. Re-encoding a sentence into it produces text a human
  cannot see, `git diff` does not show, and a model reads normally.
* **Homoglyph** — a character that looks like another. The classic spoof
  substitutes one Cyrillic letter into a Latin word.
* **Confusable / twinned** — in this plan, *has an ASCII-Latin look-alike*. A
  Greek letter with no ASCII twin cannot power a visual spoof **by definition of
  the threat**, so clearing it costs no detection.
* **Allowlist vs denylist polarity** — the source proposal's central insight. An
  omission from an *allowlist of confusables* is a **silently missed spoof**; an
  omission from a *denylist of non-confusables* is a **visible false positive** an
  adopter reports. One failure mode is discoverable and one is not.
* **NFD** — canonical decomposition: it folds a precomposed accented vowel into
  its base letter plus a combining mark.
* **Pattern id** — the string a flag carries (`homoglyph`, `unicode-bidi`) and
  the key an adopter writes a `cairn-accept` suppression marker against. It is an
  **adopter-facing contract surface**, not an internal label.
* **Frozen file** — a file whose sha256 is pinned in
  `bootstrap/tests/fixtures/gate_manifest.json`. Editing one makes gate
  verification report `FROZEN-MODIFIED`; re-pinning is a supervised act.
* **Perturbation** — a deliberate change to repository state that a regression
  test is claimed to detect. This repository accepts a regression test only when
  its author can name a future state in which it fails **and has run** the change
  that produces that state. **Perturbing a test's own body validates the test;
  only perturbing the hazard validates the claim.**

## What "ACCEPTED as revised" is read to mean

The Decision is short and the record behind it is not, so the reading has to be
stated before this plan can have a scope. Where the Decision and earlier text
disagree, **the Decision wins**.

**Settled by the Decision itself, no interpretation needed:**

1. **Change 1 stands byte-for-byte as proposed** — the `unicode-ignorable`
   detector over the PRECIS set, held as numeric range tables, skipping
   characters an existing pattern id already owns, **detect and never rewrite**.
2. **Change 2 is accepted as amended in the Revised proposal** — the
   `_CONFUSABLE_GREEK` allowlist is replaced by a `_NO_LATIN_TWIN` denylist, with
   NFD folding before the lookup. Clauses 1, 2 and 3 keep their shape, the
   two-character carve-out stays, the RV5 scientific-unit allowance stays.
3. **Whole-script Cyrillic is out of scope, as a declared residual.** The
   reasoning of record: the severe consequence of a Cyrillic homoglyph in this
   repository is *authority granting* — a byline flipping `ai` to `human` — and
   that path is closed independently by `byline-classification`, accepted,
   planned, externally reviewed and implemented. This clause would add prose
   *detection*, not authority protection, at a real cost to international proper
   nouns.

**Settled by the `## Maintainer direction` section, and binding:**

4. **The Tag block (`U+E0000`–`U+E007F`) gets its own pattern id.** So a
   `cairn-accept` marker written in good faith for an emoji variation selector
   can no longer silence a Tag-block shadow-alphabet payload. Change 1 accepts
   one additional pattern id in the shipped contract, against its own "no new
   configuration surface" fence; **the fence is held everywhere else**.
5. **Clause 1's predicate is Greek-only, and fullwidth is closed separately.**
   Two obligations follow and are not optional: the clause text and the module
   doc must say **"for Greek"** — the sentence "This closes a pre-existing hole"
   is false without that qualifier — and **whole-script fullwidth Latin is closed
   script-generally**, since it carries no legitimate proper-noun cost in an
   English tree.
6. **The two raw ignorable code points in the proposal file were repaired to
   escaped form and the repair recorded.** Re-verified for this plan
   (*Gate accounting*): the exposure is gone and Change 1's corpus cost on
   Cairn's own tree is back to **zero**.

**Read into "as revised" by this plan, because the author's Response classified
each as *within-contract* — a correction to an artifact the proposal already
specifies, adding no surface and changing no accepted behaviour:**

7. **[I4]** — the drift sentinel as specified guards a set disjoint from the rows
   it exists to guard. Corrected in Chunk C.
8. **[I5]** — *Tests required* #7 cannot fail (`str` is immutable). Replaced by
   the assertion with teeth in Chunk C.
9. **[I6]** — the naive implementation dominates the whole scan against a
   fail-closed wall-clock budget. The one-line ASCII short-circuit is carried in
   Chunk B.
10. **[I3] remedy 2** — the flag message names the count and the distinct code
    points, not only the first character. Carried in Chunk B. (`_flag_fingerprint`
    hashes `relpath:pattern_id:sha256(stripped line)` — verified for this plan at
    `templates/modules/team-gated/content_scan_runner.py:291` — so enriching a
    message churns no residual fingerprint.)
11. **[I7] bullet 1** — the published residual list must be **measured at
    execution**, never carried. Chunk E.
12. **The gate-manifest re-pin obligation**, which the proposal's *Evidence /
    verification plan* does not list. It is a real, missing plan obligation; see
    *The Maintainer fence*.

**The one place this plan must interpret rather than transcribe, stated so the
Maintainer can strike it in one line rather than discover it at code review:**

13. **[I1] — how `_NO_LATIN_TWIN` is populated.** The amendment's own two
    passages disagree, and the plan cannot execute both. This is settled in
    *Chunk D* against the artifact's own published figures, with the strike-line
    named there.

**Not read in, and explicitly not executed:** everything the Maintainer direction
lists as *"Still undecided and not folded in"* — the split recommendation, the
derivation-instead-of-curation redesign, and the "as data" fence question. The
Decision accepted the proposal **whole, not split**, so Change 2 lands as the
amended curated denylist, not as an exhaustive UTS #39-derived classification.
The consequence is stated honestly in Chunk D and routed to the plan review.

## Scope

Three files and one release note, across five chunks:
`templates/modules/team-gated/content_scan.py` (the two detector rules and the
module docstring), `templates/modules/team-gated/content-security.md` (the module
doc that describes them), `bootstrap/tests/test_content_scan.py` (new cases), and
one `CHANGELOG.md > Unreleased` line.

**Out of scope, fenced explicitly:**

* **Whole-script Cyrillic.** A declared residual of the Decision, with recorded
  reasoning. This plan does not close it, and Chunk D carries a
  *characterization* test that pins it open so a later change to it is a
  deliberate Decision rather than a side effect.
* **Any change to the suppression grammar, the reviewed-residual baseline, the
  audited-roots manifest, or `content_scan_runner.py`.** The proposal's fence,
  held. The one new pattern id is the single, Maintainer-directed exception.
* **The preset-roster / default-security-stance question.** Verified in the
  record and unchanged: no preset selects `content-security`. That belongs to
  `dev/proposals/2026-08-03-claude-default-security-stance.md`, not here. This
  plan touches neither `bootstrap/_scaffold/config.py` nor `bootstrap/profiles/`.
* **An exhaustive derivation of Greek twinning from UTS #39.** Left undecided by
  the Maintainer direction (question 4, the "as data" fence question), and it has
  an unresolved oracle dependency: `unicodedata` at UCD 15.1.0 exposes no
  confusables, skeleton, script or identifier-status accessor. Chunk D ships the
  amended curated denylist with a reconciliation test in its place, and says so.
* **Changing the per-category-per-line `break` convention.** One flag per line per
  category, unchanged. Altering it would change shipped `unicode-zero-width` and
  `unicode-bidi` output for every adopter and needs its own proposal — the same
  declared limit the sibling `separator-detection` Decision records.
* **`bootstrap/_scaffold/` — no engine change.** No `InstallSpec` added or moved;
  `content_scan.py` is already registered as a verbatim install. Therefore no AST
  re-anchor obligation and no `scaffold_ast_baseline.json` delta. Verified for
  this plan, not assumed: `python bootstrap/scaffold.py --manifest` emits the row
  `scripts/content_scan.py<TAB>modules/team-gated/content_scan.py<TAB>verbatim`,
  and `install_manifest` emits no content digest, so a content-only edit changes
  no row. **Re-verify at execution with a diff against a pre-change capture.**
* **`bootstrap/SAFETY.md` and `SECURITY.md`.** Re-checked for this plan: neither
  enumerates the scanner's pattern ids, so neither moves. No file under
  `doctrine/` is touched, `AGENTS.md` is untouched, and Cairn's own
  `dev/modules/` directory carries **no** `content-security` mirror (verified —
  18 module files, and that is not among them).

### Documentation / doctrine surface

* **Governing layer — none.** No `AGENTS.md` change, no `doctrine/` change. This
  corrects two defects in a shipped tool and syncs the doc that describes it; it
  introduces no rule a contributor must follow. The **doctrine-change
  rate-limit** in `doctrine/rationale.md` is therefore not engaged. (If a reviewer
  instead classifies "what the security scanner flags" as doctrine, the gate
  clears on the high-risk-classification branch, not on recurrence — the
  Maintainer commissioned this as a security surface and Change 1 closes a
  detection hole in the injection-defence layer.)
* **The shipped contract, code-adjacent** — the module docstring's pattern-id list
  in `templates/modules/team-gated/content_scan.py` (lines 29–55 at HEAD;
  `unicode-zero-width` at line 40, `unicode-bidi` at line 43, `homoglyph` at line
  46). This docstring **is** the user-facing contract; it gains two pattern ids
  and its `homoglyph` entry is rewritten. It moves in the same commit as the
  behaviour it describes, never later.
* **Descriptive / adopter-facing** — the *Scientific-unit homoglyph allowance*
  section of `templates/modules/team-gated/content-security.md` (lines 138–144 at
  HEAD), rewritten as a *scientific-notation* allowance. It ships to every adopter
  that installs the module, landing in the adopter's own `dev/modules/`
  directory. (The install destination is an *adopter-tree* path, not a Cairn one
  — the self-host citation gotcha `AGENTS.md` names under *Operational
  pitfalls*, which is why it is described rather than cited here.)
* **Release-facing** — one `CHANGELOG.md > Unreleased` line.
* **Deliberation layer** — this plan, its plan review, its code review, and the
  one-line `dev/PLANNING.md` row-move that serializes the plan-open.

`CHANGELOG.md`, `dev/PLANNING.md`, `AGENTS.md`, `docs/DOCUMENTATION_PLAN.md` and
`bootstrap/REANCHOR_RUNBOOK.md` are **serialized shared files**: they are edited
only at their defined serialization points, never opportunistically mid-chunk.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

## Gate accounting

Every figure below is a **dated snapshot measured for this plan**, `as_of
2026-08-04`, under the canonical interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13, UCD 15.1.0) with `PYTHONDONTWRITEBYTECODE=1`, at HEAD `eacb7dd`.
**No repository file was modified to produce any of them.** They are to be
re-taken at implementation, not quoted from here — the source proposal's record
contains four separate instances of a carried figure going stale within hours,
and the module doc's published residual list is under the same rule (item 11
above).

* **Suite collection: 1746 nodes**, `python -m pytest bootstrap/tests
  --collect-only -q`. Collection may only grow; a dropped node or a new
  skip/xfail marker is a HOLD class. (The proposal's `1556 passed` and the
  sibling `scan-coverage` plan's `1601` are both older snapshots; other work has
  landed since. Re-measure, do not carry.)
* **`python scripts/check_cairn.py` → `OK -- 180 Markdown file(s) scanned; no
  issues; 68 external link(s) not probed.`** The predicted delta from this plan
  is **zero new flags**, and the tripwire below applies to any movement.
* **Change 1's corpus cost on Cairn's own tree is zero, re-measured.** Sweeping
  all 452 tracked `.md` / `.txt` / `.py` files against the 17 ignorable rows and
  18 noncharacter rows: **9 lines** carry a covered code point and **0** of them
  carry a code point not already owned by `unicode-zero-width` or `unicode-bidi`.
  The `+2` delta the proposal's Response established is **gone** — the Maintainer
  direction's escape-form repair holds and no new raw code point has entered.
  This restores the proposal's own tripwire to full strength; see *Verification*.
* **Tracked-file counts**: 234 `.md`, 452 `.md`/`.txt`/`.py`. Decision-irrelevant
  and dated; do not chase.
* **Two frozen files are modified by this plan**, and both are literal keys in
  the 164-entry `frozen_files` map with hashes that **match the live tree today**
  (checked, not assumed):
  * `templates/modules/team-gated/content_scan.py`
  * `bootstrap/tests/test_content_scan.py`

  `templates/modules/team-gated/content-security.md` is **not** frozen (checked).
  No new file is created, so there is no `FROZEN-NEW` row.
* **The collection identity also goes stale.** `gate_manifest.json` pins
  `collection.node_count = 1598` and 1598 `node_ids`. The live tree is already at
  1746 from other work, and this plan adds further nodes. Both the frozen hashes
  and the collection pin are advanced by the same supervised act.
* **Ordinary `python -m pytest bootstrap/tests` does NOT catch any of this.**
  Checked: `bootstrap/tests/test_gate_manifest.py` verifies a manifest **produced
  from the live tree at test time** (its `produced` fixture); the committed
  `bootstrap/tests/fixtures/gate_manifest.json` is read only by the gate-control
  path (`bootstrap/tests/_gate_manifest.py`, `bootstrap/tests/_gate_preflight.py`,
  `bootstrap/tests/_gate_reanchor.py`) when an operator runs it. So the suite stays
  green across these edits and the staleness surfaces **at gate time, not at test
  time**. That asymmetry is the whole reason for the fence below.
* **`bootstrap/tests/test_gate_manifest.py:67` asserts
  `templates/modules/team-gated/content_scan.py` is in the frozen set** (verified
  at that line: *"shipped scanner / security-gate implementations ARE frozen"*).
  That assertion must stay green — this plan does not move the file out of the
  frozen class, it edits a file that is in it.
* **The install contract must not move.** `python bootstrap/scaffold.py
  --manifest` emits 96 lines (1 header + 95 data rows), `as_of 2026-08-04`.
  Expected diff after this plan: **empty**. A non-empty diff means
  `install_manifest()` was edited rather than merely read — stop and re-review.
* **`vermin` is not installed in this environment**, so
  `bootstrap/tests/test_python_floor.py` **skips gracefully** rather than
  verifying the >= 3.11 floor for the new code. This is an unrun plan obligation
  the proposal, the External round and the Internal round all left open; it stays
  open and is fenced below rather than reasoned away.
* **Bandit 1.9.4 is available** at the canonical interpreter, so the
  Bandit-over-the-edited-file obligation is dischargeable in-session.

### The Maintainer fence

Three items in this plan are **not an implementing agent's to perform**. They are
listed here rather than discovered at gate time.

1. **The gate-manifest re-pin. Supervised, and the batching is the point.**
   After the last chunk lands, `_gate_manifest.py verify` reports
   `FROZEN-MODIFIED` for `templates/modules/team-gated/content_scan.py` and
   `bootstrap/tests/test_content_scan.py`, plus a collection-identity delta.
   Re-pinning is a **two-stage supervised act** under
   `bootstrap/REANCHOR_RUNBOOK.md` and `bootstrap/tests/_gate_reanchor.py` —
   Stage A gathers evidence in an isolated tree, Stage B is data-only, executes
   no candidate code, and advances a single designated trusted ref by
   compare-and-swap, described in that module's own header as the Maintainer's
   supervised act guarded by explicit confirmation.

   **Batch the ceremony with `separator-detection`.** That proposal is accepted
   the same day, over the **same two frozen files**, and is being planned in
   parallel this session (`dev/plans/separator-detection.md`). Both plans
   invalidate the same two pins and the same collection identity. One re-pin
   after **both** land costs one supervised ceremony; one re-pin after each costs
   two, and leaves a window in which the first re-pin is already stale. **The
   implementing agent's obligation is to state, in the final commit body, that
   the two frozen entries and the collection pin are stale and that the re-pin is
   batched with `separator-detection`** — and then to stop.

   Confirmed against the sibling as authored (`dev/plans/separator-detection.md`,
   its own fence section): it adopts the identical rule — **neither plan re-pins**,
   one ceremony covers both, and one shared `CHANGELOG.md` line rather than two.
   It also records that the `gate-reanchor-preflight` batch is archived, so the
   batch-window HOLD-by-default is no longer in force; the re-pin is schedulable
   rather than blocked.

2. **The `vermin` / Python-floor verification.** `vermin` is a dev-only
   dependency and is absent here, so `test_python_floor.py` skips rather than
   verifying. The amendment adds `unicodedata.normalize` and the detector adds
   `unicodedata.name`, neither of which moves the floor **by reasoning** — and
   reasoning is not a `vermin` run. Either the Maintainer installs the dev
   dependency and the run is recorded, or the >= 3.11 floor claim for the new
   code ships **unverified and labelled as such**. Do not let the graceful skip
   read as a pass.

3. **Any decision to close whole-script Cyrillic.** Out of scope by the Decision,
   with recorded reasoning. Chunk D pins it open with a characterization test; if
   that test goes red, the correct response is a Decision, never a test edit.

## Sequencing against `separator-detection`

Both accepted proposals edit `templates/modules/team-gated/content_scan.py` and
`bootstrap/tests/test_content_scan.py`, and their Decisions set the rule between
them explicitly:

* **`separator-detection` owns the pattern-id signature change.** Its own
  correctness depends on it; this proposal merely benefits. At HEAD,
  `templates/modules/team-gated/content_scan.py:401-403` derives the pattern id
  by substring-matching the human-readable message:

  ```python
  for lineno, msg in _scan_unicode(lines, leading_bom):
      pid = "unicode-bidi" if "bidirectional" in msg else "unicode-zero-width"
  ```

  `_scan_unicode` is the **only** generator whose caller re-derives its id; every
  other call site passes a literal. A `unicode-ignorable` or `unicode-tag` message
  contains no `"bidirectional"`, so **without the fix both new ids are labelled
  `unicode-zero-width`** — the promised `cairn-accept: unicode-ignorable` marker
  would match nothing, and any existing `unicode-zero-width` suppression anywhere
  in the tree would silently hide the new detections.
* **Whichever plan implements second rebases onto the yielded-id form** and does
  not reintroduce the ternary.
* **Both plans carry the coexistence test.** It fails against the code as it
  stands, so whichever lands first turns it green and the second inherits a guard
  rather than a promise.

**Chunk A is written to be correct in either order** — it performs the signature
change if `_scan_unicode` still yields two-tuples, and degrades to a verification
step if `separator-detection` has already landed it. The first action of Chunk A
is to read the call site, not to apply this plan's text.

## Sequence

Chunk order is load-bearing. **Chunk A lands before Chunk B** because a new
pattern id introduced over the prose-dispatch call site is a mislabelled flag and
a marker that matches nothing — the fix is a precondition for the id being real,
not a tidy-up. **Chunks A–C are Change 1**, which the proposal names as
independently landable; **Chunk D is Change 2**; **Chunk E** syncs the two
documents that publish the contract.

```
0. plan-open   -- this plan + the dev/PLANNING.md row-move            [commit pending]
   (plan review) -- required(External, security lens); NO code before it lands
1. Chunk A -- the pattern id stops being inferred from prose          [commit pending]
2. Chunk B -- unicode-tag + unicode-ignorable, guarded and legible    [commit pending]
3. Chunk C -- the drift sentinel that can actually fail               [commit pending]
4. Chunk D -- the homoglyph rule becomes confusability-aware          [commit pending]
5. Chunk E -- the two documents that publish the contract, + changelog [commit pending]
```

---

### Chunk A — the pattern id stops being inferred from prose

**Read the call site first.** If `_scan_unicode` already yields
`(lineno, pattern_id, msg)`, `separator-detection` has landed the change; A1/A2
become a verification step and only A3 is authored. If it still yields
`(lineno, msg)`, this plan performs the change and `separator-detection` inherits
it.

| # | File | Change |
|---|------|--------|
| A1 | `templates/modules/team-gated/content_scan.py` | `_scan_unicode` yields `(lineno, pattern_id, msg)`; each of its loops passes its own literal id (`"unicode-zero-width"`, `"unicode-bidi"`). |
| A2 | `templates/modules/team-gated/content_scan.py` | The call site at `content_scan.py:401-403` consumes the yielded id; **the ternary is deleted**. A comment states why: prose is not a dispatch key, and an `else` branch that catches everything silently mislabels every future detector. |
| A3 | `bootstrap/tests/test_content_scan.py` | `TestUnicodePatternIdIsolation` — one fixture carrying a zero-width character, a bidi control, a Tag-block character and a soft hyphen on **separate lines**; assert each line yields its own id and only its own. Plus: a `cairn-accept: unicode-zero-width` marker suppresses **only** `unicode-zero-width` and does **not** suppress the other three. |

**Acceptance criteria — Chunk A.**

* `python -m pytest bootstrap/tests/test_content_scan.py -q` → all pass, 0 skipped.
* `python scripts/check_cairn.py` → unchanged from the *Gate accounting* baseline.
* **Perturbation P-A1, RUN, hazard-side.** Restore the ternary at the call site
  (`pid = "unicode-bidi" if "bidirectional" in msg else "unicode-zero-width"`) and
  confirm A3 goes **RED**, naming the collapsed ids. Restore; confirm `git diff
  templates/modules/team-gated/content_scan.py` is empty. *This perturbs the
  scanner, not the test — a test edited to fail proves only that it was edited.*
* **Perturbation P-A2, RUN.** Delete the marker-isolation half of A3's fixture's
  guard by widening the marker's pattern id to a second id in the **scanner's**
  `_parse_suppressions` (make a marker suppress all ids); confirm A3 goes RED.
  Restore and verify byte-identically.
* **The future state in which A3 fails** is not hypothetical: any commit adding a
  detector to `_scan_unicode` without touching the call site. That is exactly what
  Chunk B does, which is why A precedes B.
* **Channel note.** Subject: `scan_text`'s id assignment. Oracle: pattern-id
  string literals typed into the test by a human. No shared derivation.

---

### Chunk B — `unicode-tag` and `unicode-ignorable`, guarded and legible

Change 1's substance, plus the three within-contract corrections it carries
([I3] remedy 2, [I6], and the Maintainer-directed id split).

**Two ids, and the split is the Maintainer's direction, not an optimization.**
`U+FE00`–`U+FE0F` (variation selectors) is benign-and-common — emoji use it.
`U+E0000`–`U+E007F` (the Tag block) is never-benign in agent-loaded Markdown.
Routing both through one id means a good-faith `cairn-accept` marker for the first
blesses the second inside its block — demonstrated in the record against the
*shipped* scanner's suppression grammar, not a reconstruction.

| # | File | Change |
|---|------|--------|
| B1 | `templates/modules/team-gated/content_scan.py` | Two module-level range tables as tuples of `(lo, hi)` integer pairs, each row commented with what it covers: `_IGNORABLE_RANGES` (17 rows, the PRECIS `Default_Ignorable_Code_Point` set) and `_NONCHARACTER_RANGES` (18 rows: `U+FDD0`-`U+FDEF` plus `U+nFFFE`/`U+nFFFF` for planes 0-16). **Numeric ranges, never raw characters** — this preserves the `TestSourceCarriesNoRawInvisibles` invariant. Verified for this plan: those exact row counts cover the whole set, and the **lowest code point across both tables is `U+00AD`**. |
| B2 | `templates/modules/team-gated/content_scan.py` | `_TAG_RANGE = (0xE0000, 0xE007F)`, carved out of the ignorable set and given the pattern id **`unicode-tag`**. The remainder of the `U+E0000`-`U+E0FFF` row (including the Variation Selectors Supplement, `U+E0100`-`U+E01EF`) stays under `unicode-ignorable`. |
| B3 | `templates/modules/team-gated/content_scan.py` | A `_scan_unicode` loop yielding `unicode-tag` and a loop yielding `unicode-ignorable`, both following the existing **one flag per line per category** convention. **The ASCII short-circuit ([I6]) is the first statement in each character loop**: `if ch < "\u00ad": continue` (an escape form in the source, never the raw character), with a comment naming the invariant that licenses it — every code point in both tables is >= `U+00AD`, so the guard can never skip a detected code point. |
| B4 | `templates/modules/team-gated/content_scan.py` | **The skip rule.** A character in `_ZERO_WIDTH` or `_BIDI` is skipped by both new loops, so `unicode-zero-width` and `unicode-bidi` keep their **exact current meaning** and no existing `cairn-accept` marker or residual fingerprint is invalidated. The leading-BOM exemption (`U+FEFF` at line 1, column 0) is preserved on the new path too. |
| B5 | `templates/modules/team-gated/content_scan.py` | **The message ([I3] remedy 2).** Each flag names the **count and the distinct code points on that line**, not only the first: e.g. `3 default-ignorable code point(s) on this line: U+FE0F (VARIATION SELECTOR-16) x2, U+2061 (FUNCTION APPLICATION)`. `unicodedata.name(ch, "unnamed / reserved")` — the **two-argument form**, so a reserved code point with no name still flags. *A missing name must never suppress a flag.* This is the one new import: `unicodedata`, standard library. |
| B6 | `bootstrap/tests/test_content_scan.py` | `TestUnicodeIgnorable` — `unicode-tag` fires on a Tag-block payload; `unicode-ignorable` fires on SOFT HYPHEN inside a word, on a variation selector, and on noncharacter `U+FDD0`; ordinary clean prose yields neither. All built with `\uXXXX` escapes. |
| B7 | `bootstrap/tests/test_content_scan.py` | `test_tag_id_is_not_suppressed_by_an_ignorable_marker` — a **block-scoped** `cairn-accept: unicode-ignorable` written for a variation-selector line does **not** silence a Tag-block payload planted inside the same block. This is the test that pins the Maintainer's direction. |
| B8 | `bootstrap/tests/test_content_scan.py` | `test_existing_ids_keep_their_meaning` — a ZWSP line yields `unicode-zero-width` and **not** `unicode-ignorable`; a bidi line yields `unicode-bidi` only; a leading BOM stays exempt; a non-leading BOM still flags `unicode-zero-width`. |
| B9 | `bootstrap/tests/test_content_scan.py` | `test_message_names_every_distinct_codepoint_on_the_line` — a line carrying a benign `U+FE0F` **before** a Tag-block payload produces a message naming **both** code points and a count. This is the same-line masking case. |
| B10 | `bootstrap/tests/test_content_scan.py` | `test_ascii_guard_can_never_skip_a_detected_codepoint` — assert `min(lo for lo, _ in _IGNORABLE_RANGES + _NONCHARACTER_RANGES + [_TAG_RANGE]) >= 0x00AD`. Not a timing test; it pins the *precondition* the performance guard rests on. |

**Acceptance criteria — Chunk B.**

* `python -m pytest bootstrap/tests/test_content_scan.py -q` → all pass, 0 skipped.
* `python scripts/check_cairn.py` → **flag count unchanged**. The predicted delta
  is zero and it is re-measured for this plan at zero (*Gate accounting*). **Any
  movement means the corpus sweep was wrong; re-measure, do not suppress the new
  flag** — that is the proposal's own signal-the-change-is-wrong tripwire, and it
  is at full strength again now that the `+2` exposure has been repaired.
* **Perturbation P-B1, RUN, per-row and hazard-side.** Delete the
  `U+E0000`-`U+E007F` row; confirm B6's Tag case goes RED. Delete the
  `U+00AD` row; confirm B6's soft-hyphen case goes RED. Delete the `U+FDD0`-`U+FDEF`
  row; confirm B6's noncharacter case goes RED. Restore after each and confirm
  `git diff` empty.
* **Perturbation P-B2 — the id split is load-bearing, RUN.** Merge the Tag rows
  back into `unicode-ignorable` (delete `_TAG_RANGE` and let the general table
  cover it); confirm **B7 goes RED** — the good-faith marker now silences the
  payload. This is the perturbation that proves the Maintainer's direction is
  carrying weight rather than decorating.
* **Perturbation P-B3 — the skip rule, RUN.** Delete the `_ZERO_WIDTH`/`_BIDI`
  skip; confirm **B8 goes RED** with a ZWSP line double-flagging.
* **Perturbation P-B4 — the message, RUN.** Revert B5's message to naming only the
  first character; confirm **B9 goes RED**.
* **Perturbation P-B5 — the guard's precondition, RUN.** Add a table row below
  `U+00AD` (e.g. `(0x0000, 0x0008)`); confirm **B10 goes RED**. Restore.
* **The performance number, recorded in the commit body, not asserted as a test.**
  Measured for this plan over the tracked `.md` corpus (89 445 lines, 5.59 MB),
  best of three: HEAD `_scan_unicode` 0.218 s; a naive per-character table walk
  **5.757 s (26.4x)**; the same walk with the `U+00AD` guard **0.121 s (0.56x —
  below HEAD's existing pass)**, with an **identical hit set**. The consequence is
  why this is not cosmetic: `content_scan_runner.py:83` sets
  `_MAX_WALL_SECONDS = 120.0` and a breach is a **fail-closed exit 2**, not a slow
  pass. Re-measure at implementation against the real code; the interesting claim
  is the direction and the guard, not the constant.
* **Bandit over the edited file** — `python -m bandit -q
  templates/modules/team-gated/content_scan.py`, expected clean, exit 0.
* **Channel note.** Subject: the two new detector loops. Oracle: `\uXXXX` escape
  literals typed into the test by a human, plus `unicodedata` (a different data
  source than the hand-written range tables). Neither is derived from the tables
  under verification — which is exactly the independence Chunk C then tests
  systematically.

---

### Chunk C — the drift sentinel that can actually fail

Closes **[I4]** and **[I5]**. The sentinel the proposal specifies guards a set
**disjoint** from most of what it exists to guard, and the invariant test it
proposes cannot fail.

**Why the specified sentinel is hollow, re-derived from `unicodedata` for this
plan with no reconstruction in the loop:**

```
python 3.13.13   UCD 15.1.0
sampled Default_Ignorable code point categories : ['Lo', 'Mn']   any Cf: False
noncharacter categories                         : ['Cn']
total Cf code points in UCD 15.1.0              : 170
```

`Default_Ignorable_Code_Point` is **not** general category `Cf`. Ten sampled
members — COMBINING GRAPHEME JOINER `U+034F`, the Hangul fillers `U+115F`,
`U+1160`, `U+3164`, `U+FFA0`, the Khmer inherent vowels `U+17B4`, `U+17B5`, and
the variation selectors `U+FE00`, `U+FE0F`, `U+E0100` — are all `Mn` or `Lo`, and
**every** noncharacter is `Cn`. So a `Cf` sweep guards neither six of the
seventeen ignorable rows **nor any of the eighteen noncharacter rows**. The named
future state in which it passes anyway: *a future UCD adds a default-ignorable
code point of category `Mn` or `Lo` outside the frozen ranges* — precisely where
Unicode has added them before. `U+3164` HANGUL FILLER is `Lo`, so `re`'s `\w`
treats it as a letter: it sits **inside** a word without even splitting the token.

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/tests/test_content_scan.py` | `test_cf_sweep_is_covered` — every `Cf` code point in the running interpreter's UCD, minus the documented exclusions (prepended concatenation marks, interlinear annotation, the Egyptian hieroglyph format controls), falls inside the tables. Retained from the proposal, **relabelled** as one of three sentinels rather than the sentinel. |
| C2 | `bootstrap/tests/test_content_scan.py` | `test_non_cf_default_ignorables_are_covered` — an explicit, commented list of the Default_Ignorable members that are **not** `Cf`, each asserted detected through the public `scan_text` path: `U+034F`, `U+115F`, `U+1160`, `U+17B4`, `U+17B5`, `U+180B`-`U+180D`, `U+3164`, `U+FE00`-`U+FE0F`, `U+FFA0`, `U+E0100`. Stdlib-only, one table, zero dependencies. |
| C3 | `bootstrap/tests/test_content_scan.py` | `test_every_noncharacter_row_is_covered` — `U+FDD0`-`U+FDEF` sampled at both ends and the middle, plus `U+nFFFE`/`U+nFFFF` for **every** plane 0-16, asserted detected. Guards the eighteen rows the `Cf` sweep reaches not at all. |
| C4 | `bootstrap/tests/test_content_scan.py` | Widen `_BANNED_CODEPOINTS` (the `TestSourceCarriesNoRawInvisibles` hygiene set, at `bootstrap/tests/test_content_scan.py:47-52`) to the **union of the new tables**, so the "the scanner carries none of the code points it detects" invariant actually extends to the newly-detected set instead of silently staying at its 2026-era membership. |
| C5 | `bootstrap/tests/test_content_scan.py` | **[I5]** — replace *Tests required* #7 with `test_scan_file_leaves_the_file_bytes_unchanged`: write a fixture into `tmp_path`, hash it, `scan_file` it, re-hash, assert equal. A comment records **why the specified form was dropped**: Python `str` is immutable, so `assert text_unchanged_after_scan_text(...)` passes against a scanner that strips ignorables — the behaviour the proposal forbids most emphatically. Keeping the vacuous form without that comment invites a future author to re-add it. |

**Acceptance criteria — Chunk C.**

* `python -m pytest bootstrap/tests/test_content_scan.py -q` → all pass, 0 skipped.
* **Perturbation P-C1 — the discriminating pair, and it is the whole point of the
  chunk. RUN.** Delete the `U+FE00`-`U+FE0F` row from `_IGNORABLE_RANGES` and
  observe, in the **same run**: **C1 green, C2 RED** naming the variation
  selectors. Repeat for `U+034F` and for `U+3164`. If C1 also goes red, the
  finding was wrong; if C2 stays green, Chunk C is decoration.
* **Perturbation P-C2 — the noncharacter half, RUN.** Delete the plane-1
  noncharacter row (`U+1FFFE`-`U+1FFFF`); confirm **C3 RED, C1 green**.
* **Perturbation P-C3 — the hygiene test still bites, RUN, hazard-side.** Plant a
  **raw** `U+00AD` in `templates/modules/team-gated/content_scan.py` (working tree
  only, never committed); confirm **C4 RED**. Delete it; confirm `git status
  --short` is clean for that path. Note that at HEAD, *before* C4's widening, this
  same perturbation leaves the hygiene test **green** — that is the gap C4 closes,
  and both halves of the pair must be run.
* **Perturbation P-C4 — [I5]'s replacement is not itself vacuous, RUN.** Make
  `scan_file` write a normalized copy back to disk; confirm **C5 RED**. Restore.
  Then confirm the retired assertion's vacuity directly: run the old
  `scan_text`-immutability form against that same rewriting scanner and observe it
  **pass**. Record both results — the second is the evidence that [I5] was a real
  finding and not a style note.
* **Channel note.** Subject: the two range tables in `content_scan.py`. C1/C2/C3's
  oracle is `unicodedata` and a human-typed code-point list — a channel the tables
  do not read. Under P-C1 the table changes and `unicodedata` does not, and the two
  come apart. That independence is **demonstrated**, not asserted.
* **A named limit, stated rather than discovered.** C2's list is hand-maintained
  and pinned to UCD 15.1.0. It does not *derive* Default_Ignorable — `unicodedata`
  exposes no such accessor, probed for this plan and absent. So a future UCD
  addition outside both the ranges and C2's list is still a silent gap. C2 shrinks
  the hole from "six rows plus all eighteen" to "code points nobody has heard of
  yet"; it does not close it. The module doc must not claim otherwise.

---

### Chunk D — the homoglyph rule becomes confusability-aware

Change 2, as amended, under the Maintainer's Greek-only + close-fullwidth
direction and the Decision's Cyrillic residual.

**The three clauses. A token flags when any holds:**

1. **Whole-script confusable — Greek only, plus fullwidth Latin closed
   separately.** *Greek arm*: the token has no Latin characters, all its letters
   are Greek, it has at least three letters, and **every** letter is confusable
   (absent from `_NO_LATIN_TWIN`). *Fullwidth arm*: the token's letters are all
   fullwidth Latin (`U+FF21`-`U+FF5A`) and there are at least three. The fullwidth
   arm needs **no** confusability table at all — `U+FF21`-`U+FF5A` is a bijection
   onto ASCII `A`-`Z`/`a`-`z` by construction, which is exactly why the Maintainer
   direction calls it a pure-loss vector closable at zero natural-language cost.
   **Whole-script Cyrillic is deliberately not an arm here.**
2. **Non-Greek confusable script mixed with Latin always flags.** Cyrillic,
   Armenian, Cherokee, Coptic, fullwidth. Unchanged behaviour from HEAD.
3. **Greek mixed with Latin where a Greek character is confusable.** NFD-fold each
   Greek character, then test membership in `_NO_LATIN_TWIN`. The one exception is
   the two-character variable-plus-subscript shape: exactly one Latin letter,
   exactly one Greek letter, total length two.

`_is_scientific_unit` (RV5) is left in place, unchanged.

#### How `_NO_LATIN_TWIN` is populated — the one interpretive call, and its evidence

**The problem.** [I1] is ACCEPTED in the author's Response, and its substance is
that the amendment's enumerated parenthetical (`Gamma Delta Theta Lambda Xi Pi
Sigma Phi Psi Omega and their lowercase, plus the theta/phi/pi symbol variants`)
**silently clears 14 tokens HEAD flags**, and is simultaneously **short** — it
omits `U+03B2` and `U+03BC`, which the amendment's own *Named residual* section
and its 14/83 figure both require it to contain. A set that contradicts its own
published figures cannot be transcribed; it has to be reconciled.

**The rule this plan executes**, which is [I1]'s own suggested disposition:

* **Seed** `_NO_LATIN_TWIN` from the base proposal's own untwinned classification,
  read **case-exactly** as written: `U+0394`, `U+03BB`, `U+03C3`, `U+03B8`,
  `U+03C6`, `U+03C8`, `U+03B2`, `U+03BC`, `U+03A9`.
* **Admit any further code point only on a per-code-point justification against
  the ASCII alphabet**, recorded in a comment beside the entry. Membership is
  **never inherited from a base letter**. That single rule does two jobs at once:
  it admits the theta/phi/pi symbol variants the amendment names (`U+03D1`,
  `U+03D5`, `U+03D6` — none has an ASCII twin), and it **refuses** the lunate
  sigma `U+03F2`, which is a variant of a seeded letter but reads as Latin `c`.
  Inheritance would have admitted it and reopened the round-one bypass family.
* **Erring toward the smaller denylist is the safe direction**, because a smaller
  denylist means more flagging.

**Why case-exact rather than case-loose, and this is the evidence that decides
it.** Measured for this plan in a scratch reconstruction outside the repository
(nothing was written into the working tree), under the canonical interpreter at
HEAD `eacb7dd`:

| measure | HEAD | case-exact seed |
|---|---|---|
| scientific false positives, the proposal's own 42-token set | 37 / 42 | **7 / 42** |
| ...and the residual tokens | — | `U+03BD`+`max`, `U+03C9`+`opt`, `U+03BA`+`eff`, `U+03B1`+`level`, `U+03B7`+`eff`, `U+03B3`+`ray`, `U+03B1`+`decay` |
| [I1]'s 14 falsifying tokens, flagged | 14 / 14 | **13 / 14** |
| whole-script Greek (`U+03C4 U+03BF U+03BA U+03B5 U+03B7`) | miss | **caught** |
| the variant-letterform bypass (`U+03F0` swapped in) | miss | **caught** |
| the lunate-sigma word (`U+03B5 U+03C7 U+03B5 U+03F2 U+03C5 U+03C4 U+03B5`) | miss | **caught** |
| whole-script fullwidth | miss | **caught** |
| whole-script Cyrillic, and a Cyrillic personal name | miss | miss *(declared residual)* |
| the two-character carve-out, the beta family | clear | clear *(declared limits)* |

Three things fall out, and each is a reconciliation the amendment never
performed:

* **7 / 42 is exactly the figure the amendment publishes**, and the seven tokens
  are exactly the seven the proposal commits the module doc to naming. The literal
  parenthetical yields **5 / 42** instead, which is [I7] bullet 1 — the
  benign-direction shadow of the same defect.
* **13 of [I1]'s 14 tokens close.** The fourteenth is `U+03B4`+`o`, a
  two-character token — the shape the proposal explicitly names and carves out.
  So the proposal's own falsifying criterion (*"a spoof that HEAD catches and the
  patch clears, other than the named two-character shape"*) **no longer fires**.
* Every one of the nine seeded letters appears in the proposal's 42-token set in
  **exactly the case the parenthetical names**, which is strong evidence the
  parenthetical was read off the measured residual case-exactly in the first
  place.

**Maintainer strike-line.** If *"as amended"* is read as the literal parenthetical
(case-loose, `Gamma`/`Theta`/`Lambda`/`Xi`/`Pi`/`Sigma`/`Phi`/`Psi` and all
lowercase forms included), then D1's seed changes, the published residual list
becomes **five** rather than seven, and 14 tokens HEAD flags are cleared. Nothing
else in this plan moves. Strike this sub-section and D1's seed; D2-D10 stand as
written with re-measured figures.

**What this plan does *not* deliver, said plainly.** This is still a **curated
set**, one layer up. The Response's recommendation — replace curation with an
exhaustive classification of all 347 assigned letters in the two Greek
`_SCRIPT_RANGES` rows — was left **undecided** by the Maintainer direction, and it
has an unresolved oracle dependency (no stdlib confusables accessor; UTS #39's
data file is an external dependency against a zero-runtime-dependency budget).
D9 and D10 substitute a *reconciliation* test and a *pinned size* for that
derivation. That converts "someone's judgment was incomplete" into "the table
disagrees with its own published figures", which is a test — but it does not
convert it into "the table covers its domain", which is not.

| # | File | Change |
|---|------|--------|
| D1 | `templates/modules/team-gated/content_scan.py` | `_NO_LATIN_TWIN`, a `frozenset` of Greek code points **written as `\uXXXX` escapes or integer literals**, each with a comment naming why it has no ASCII twin. Seeded and admitted per the rule above. |
| D2 | `templates/modules/team-gated/content_scan.py` | `_is_confusable_greek(ch)` — NFD-fold, then test non-membership in `_NO_LATIN_TWIN`. |
| D3 | `templates/modules/team-gated/content_scan.py` | `_scan_homoglyph` rewritten to the three clauses. Clause 1's comment and the code both say **"for Greek"**; the fullwidth arm is separate and commented as the bijection case. A comment records that **whole-script Cyrillic is a declared residual of the Decision**, with the one-line reason (authority granting is closed by `byline-classification`) so a future reader meets a priced decision rather than an oversight. |
| D4 | `bootstrap/tests/test_content_scan.py` | `test_scientific_notation_does_not_flag` — the cleared shapes, by code point: `U+0394`+`G`, `U+03BB`+`max`, `U+03C3`+`y`, `U+03C1`+`w`, `K`+`U+03B1`, `U+03B5`+`r`, `U+03B2`+`sheet`, `U+03B8`+`r`, `U+03C6`+`p`, `U+03A9`+`n`. |
| D5 | `bootstrap/tests/test_content_scan.py` | `test_spoofs_still_flag` — `p`+`U+0430`+`ssword` (Cyrillic), `U+0391`+`dmin`, `U+03C1`+`assword`, `s`+`U+03BF`+`urce`, `k`+`U+03B5`+`y`, plus **all 14 of [I1]'s tokens except the named two-character shape**. This is the [I1] regression and the reason the falsifying criterion stops firing. |
| D6 | `bootstrap/tests/test_content_scan.py` | `test_whole_script_greek_flags` — `U+03C4 U+03BF U+03BA U+03B5 U+03B7`, the variant-letterform form with `U+03F0` substituted, and the lunate-sigma word with `U+03F2`. |
| D7 | `bootstrap/tests/test_content_scan.py` | `test_whole_script_fullwidth_flags` — a fullwidth-Latin token of at least three letters flags; a two-letter one does not. |
| D8 | `bootstrap/tests/test_content_scan.py` | `test_declared_residuals_stay_open` — the **characterization** test. Whole-script Cyrillic does **not** flag; a Cyrillic personal name does **not** flag; the beta family does **not** flag; the two-character carve-out does **not** flag. Its docstring says what it is for: these are limits the Decision **priced**, and if this test goes red the correct response is a Decision, never a test edit. |
| D9 | `bootstrap/tests/test_content_scan.py` | `test_the_table_reconciles_with_its_published_figures` — over the proposal's own 42-token scientific set, assert the false-positive set is **exactly** the seven named tokens; over the committed spoof set, assert every member flags. This is the substitute for the derivation: it makes "the curated set drifted from what the module doc publishes" a test failure instead of a documentation defect. |
| D10 | `bootstrap/tests/test_content_scan.py` | `test_no_latin_twin_is_bounded_and_in_domain` — every member is inside the two Greek `_SCRIPT_RANGES` rows (`U+0370`-`U+03FF`, `U+1F00`-`U+1FFF`), no member is a dead entry, and the set's size is **pinned** so a silent addition fails loudly. Verified for this plan: those two rows span 400 code points carrying **347** assigned letters, 129 in Greek and Coptic and 218 in Greek Extended. |
| D11 | `bootstrap/tests/test_content_scan.py` | `test_rv5_scientific_units_still_clear` — the micro and ohm unit shapes, unchanged. |
| D12 | `bootstrap/tests/test_content_scan.py` | The existing `TestHomoglyphExpandedScripts::test_expanded_confusable_scripts_flagged` (at `bootstrap/tests/test_content_scan.py:81`) must pass **unmodified**. Clause 2 is unchanged behaviour and an edit to that test would be the tell that it is not. |

**Acceptance criteria — Chunk D.**

* `python -m pytest bootstrap/tests/test_content_scan.py -q` → all pass, 0 skipped,
  and `TestHomoglyphExpandedScripts` **untouched**.
* `python scripts/check_cairn.py` → **flag count unchanged**. Re-measure the
  file-by-file flag-set comparison across all tracked `.md` at implementation;
  the proposal's "0 files change" prediction is stated over the full tracked set,
  not over `check_cairn`'s filtered set, and both must be checked.
* **Perturbation P-D1 — the denylist is load-bearing in both directions, RUN,
  hazard-side.** Remove `U+03BB` from `_NO_LATIN_TWIN`; confirm **D4 RED**
  (`U+03BB`+`max` now flags). Add `U+03B3` to `_NO_LATIN_TWIN`; confirm **D9 RED**
  (the published seven becomes six) and **D5 RED** (`ke`+`U+03B3` clears). Restore
  after each; confirm `git diff` empty.
* **Perturbation P-D2 — clause 1 exists, RUN.** Restore HEAD's
  `len(_token_scripts(token)) > 1` rule in place of the three clauses; confirm
  **D6 and D7 both RED**.
* **Perturbation P-D3 — the fullwidth arm is separate, RUN.** Delete only the
  fullwidth arm; confirm **D7 RED and D6 green**. That pair is what shows the
  Maintainer's "closed separately" direction was implemented separately rather
  than folded into a script-general clause.
* **Perturbation P-D4 — the Cyrillic residual is pinned, RUN.** Make clause 1
  script-general; confirm **D8 RED** on both the whole-script Cyrillic case and the
  personal-name case. Restore. *This is the perturbation that makes D8 a guard
  rather than a comment: it proves the declared residual is a decision the code
  implements, not an accident of the token set.*
* **Perturbation P-D5 — the two-character carve-out is a choice, RUN.** Delete the
  carve-out; confirm **D8 RED** on the two-character case and **D4 RED** on the
  two-character scientific shapes. Restore. Record the scientific false-positive
  count under the carve-out's absence — the proposal names ~19/42 as the recovery
  posture if a reviewer breaks clause 3, and the real number should be in the
  record before anyone needs it.
* **Perturbation P-D6 — RV5 still carries weight, RUN.** Delete the
  `_is_scientific_unit` call from `_scan_homoglyph`; confirm **D11 RED**.
* **The falsifying sweep must be RUN, not reasoned.** Over the union of every
  token set in the proposal's record — 42 + 83 scientific, and the 21 hand-built,
  153 single-substitution, 40 maximal-substitution, 41-token and 51-token spoof
  sets — enumerate **every** token that HEAD flags and the implementation clears.
  The expected answer is the two-character shape and nothing else. Any other member
  is the falsifying test firing for the third time in this lifecycle, and the
  recovery is named in the proposal: drop clause 3's two-character exception and
  accept the higher scientific false-positive rate. **Restate the maximal-sweep
  `missed=` set from the run** — the record establishes it moves under any change
  to the denylist, and `U+03C1 U+03BF U+03C3 U+03B9` is predicted to stay missed
  because `U+03C3` is seeded untwinned.
* **NFD folding — measure it, and report what it does.** Under a denylist,
  NFD folding **widens clearing** rather than closing a bypass; that polarity
  inverted when the set inverted, and the amendment carried the mechanism over
  without restating its effect. Under the case-exact seed, **no** precomposed or
  Greek Extended form appears to fold onto a seeded base, which would make the
  folding inert. Measure it: report how many of the 218 assigned Greek Extended
  letters fold onto a `_NO_LATIN_TWIN` member, and whether any of them is itself
  ASCII-confusable. If the number is zero, say so in the code comment and keep the
  fold as declared defence for a future denylist addition; if it is not zero, the
  cleared set must be listed and put to the plan reviewer. **Do not ship a
  mechanism described as a guard without a number saying what it guards.**
* **Channel note.** Subject: `_scan_homoglyph` and `_NO_LATIN_TWIN`. D4-D8 and D11's
  oracle is code-point literals typed into the test by a human from the proposal's
  published token sets — not derived from the table. D9's oracle is the
  proposal's own **published figures**, an artifact written before the
  implementation existed. D10's oracle is `_SCRIPT_RANGES` plus `unicodedata`
  category data, which the denylist does not read.

---

### Chunk E — the two documents that publish the contract

Both documents describe behaviour this plan changes. Leaving either is how a
claim outruns its implementation, which is the defect class this whole proposal
exists to close.

| # | File | Change |
|---|------|--------|
| E1 | `templates/modules/team-gated/content_scan.py` module docstring | The bulleted pattern-id list (lines 29-55 at HEAD) gains **`unicode-tag`** and **`unicode-ignorable`**, each with a one-line description and the PRECIS / RFC 8264 § 9.13 citation. The `unicode-zero-width` and `unicode-bidi` entries gain a clause stating their meaning is **unchanged** and that a character they own is skipped by the new detectors. |
| E2 | `templates/modules/team-gated/content_scan.py` module docstring | The `homoglyph` entry (line 46 at HEAD) is rewritten to describe the confusability rule: what a flag now means (*a character here imitates a Latin letter*, not *this token contains Greek*), the three clauses with clause 1 stated **"for Greek"** and the fullwidth arm named separately, and the retained RV5 allowance. |
| E3 | `templates/modules/team-gated/content-security.md` | The *Scientific-unit homoglyph allowance* section (lines 138-144 at HEAD) becomes *Scientific-notation homoglyph allowance*: the rule in two sentences; the residual shapes that still flag — **measured at execution, never carried from this plan or from the proposal**; the beta-family limit and the one-line reason it was priced that way; the two-character carve-out; and the declared whole-script-Cyrillic residual with its reason. It must also state the limit C2 names: the ignorable table is a **pinned snapshot** of UCD 15.1.0, not a live derivation. |
| E4 | `templates/modules/team-gated/content-security.md` | The *Template content* blockquote (lines 25-33 at HEAD) lists the flagged families for an adopter's docs guide; add the invisible / default-ignorable family so the adopter-facing sentence matches the shipped detector set. |
| E5 | `CHANGELOG.md > Unreleased` | **`Added`** — the `unicode-ignorable` and `unicode-tag` detectors over the PRECIS set. **`Changed`** — the `homoglyph` detector is confusability-aware; scientific Greek notation no longer flags. **`Fixed`** — the pattern id is no longer inferred from message prose (shared with `separator-detection`; whichever lands second does not duplicate the line). Cross-reference the proposal and plan **by filename stem, not path link**. Written at the serialization point, not mid-chunk. |

**Acceptance criteria — Chunk E.**

* `python scripts/check_cairn.py` → OK, 180 Markdown files `as_of 2026-08-04`; the
  count may only grow and the flag count may not move.
* `python scripts/quality_gate.py --sub neutrality` → unchanged. Re-capture the
  baseline immediately before the edit; the figure is owned by other work and moves.
* `python scripts/claim_check.py <file>` over each edited Markdown file, **one file
  per invocation** — the checker takes a single path and exits 2 on more.
* **Verify every quoted line before editing.** E1-E4 cite line numbers measured
  `as_of 2026-08-04`, and `separator-detection` edits the same docstring. Re-read
  both files at implementation time; **do not apply the edits from this plan's text
  alone.**
* **The published residual list is measured, not transcribed.** Run the 42-token
  set against the **real** implementation and paste the result. The record contains
  a specific instance of this going wrong — the module doc was committed to
  publishing seven shapes by a section whose own amendment made it five — and it is
  the single most likely place for this plan to ship a false sentence.
* **Adopter-upgrade consequence, recorded in the commit body.** Change 2 clears
  flags. An adopter's own `content_scan_residuals.txt` carrying a `homoglyph`
  fingerprint for a now-cleared line goes **STALE** and fails their scan at
  **exit 3** until pruned. Checked for this plan: the **shipped** baseline
  (`templates/modules/team-gated/content_scan_residuals.txt`) is comment-only with
  no fingerprints, so no adopter *inherits* one from Cairn — but an established
  adopter may have written their own. The `Changed` changelog line must say so.
* **Channel note.** The claim is that the two documents now match the scanner. The
  evidence is a **live run of the edited scanner** over the published token sets,
  not a reading of the prose just written. `check_cairn` verifies link and
  claim-path integrity, never whether a sentence is true: it catches drift, never
  absence.

## Acceptance criteria

Per-chunk criteria are above; these are the plan-level deliverables.

* **Tests that must pass.**
  * `python -m pytest bootstrap/tests` — the whole suite, green, **0 failed /
    0 skipped beyond the pre-existing `vermin` skip / 0 xfailed**, under the
    canonical interpreter (3.13.13) with `PYTHONDONTWRITEBYTECODE=1`. Collection
    baseline **1746 nodes `as_of 2026-08-04`**; it grows by exactly the new nodes
    and drops none.
  * [`bootstrap/tests/test_content_scan.py`](../../bootstrap/tests/test_content_scan.py)
    — every new case A3, B6-B10, C1-C5, D4-D12, and the existing 15 assertions
    unmodified.
  * **Every new test shown non-vacuous by a RUN perturbation of the hazard**, with
    the ledger — the change made, the failure observed with its message, the
    byte-identical restore verified against `git diff <path>` — in the commit body.
    Where a test cannot be made to fail, the plan says so instead of implying a
    guard. *Two tests that could not fail have already shipped in this repository
    this session; a perturbation of a test's own body is not evidence.*
* **Doc updates that must land.** All hand-authored: the module docstring in
  `templates/modules/team-gated/content_scan.py` (E1, E2), two sections of
  `templates/modules/team-gated/content-security.md` (E3, E4), and
  `CHANGELOG.md > Unreleased` (E5). No generated docs, no snippet-synced blocks.
* **Examples / smoke checks required.**
  * `python scripts/check_cairn.py` — the composed self-scan, expected at its
    current flag count.
  * `python scripts/content_scan.py <file>` **in a scaffolded tree** — the
    adopter's own path, confirming the shipped verbatim copy behaves identically to
    the composed one. Named in the proposal's *Examples / smoke checks* and unrun
    by every party so far.
  * `python bootstrap/scaffold.py --manifest` — expected **byte-identical** to a
    pre-change capture, which is itself the assertion that this plan installs
    nothing new into an adopter tree.
  * `python -m bandit -q templates/modules/team-gated/content_scan.py` — clean,
    exit 0.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk and the enforcing test.**
  * *Every pattern id is assigned by a literal, never inferred from message
    prose.* Enforced by A3 in
    [`bootstrap/tests/test_content_scan.py`](../../bootstrap/tests/test_content_scan.py),
    perturbed by P-A1.
  * *`unicode-zero-width` and `unicode-bidi` keep their exact current meaning, so
    existing suppressions and residual fingerprints stay valid.* Enforced by B8,
    perturbed by P-B3.
  * *A `cairn-accept` marker for one id never silences another.* Enforced by A3
    and B7, perturbed by P-A2 and P-B2. **This is the invariant the Maintainer's
    id split exists to create.**
  * *The scanner source carries no raw code point it detects.* Enforced by the
    widened `TestSourceCarriesNoRawInvisibles` (C4), perturbed by P-C3, and
    structurally by holding the tables as numeric ranges.
  * *The ASCII short-circuit can never skip a detected code point.* Enforced by
    B10, perturbed by P-B5.
  * *The ignorable and noncharacter tables cover their documented set.* Enforced
    by C1 + C2 + C3 as three sentinels over three disjoint category families,
    perturbed by P-C1 and P-C2. **C1 alone is the hollow form and must not be
    cited as the guard.**
  * *The scanner never modifies the text or the file it scans.* Enforced by C5,
    perturbed by P-C4. The `scan_text` form of this assertion is vacuous and is
    retired with a comment saying why.
  * *`_NO_LATIN_TWIN` agrees with the figures the module doc publishes.* Enforced
    by D9, perturbed by P-D1.
  * *Clause 1 is Greek-only; fullwidth is a separate arm; Cyrillic stays open.*
    Enforced by D6, D7 and D8, perturbed by P-D3 and P-D4.
  * *The install contract does not move.* Enforced by the manifest diff against a
    pre-change capture, **not by any test**.
* **Public-path to test mapping.** The two public entry points are `scan_text` and
  `scan_file`; both are exercised **through their public path** by
  [`bootstrap/tests/test_content_scan.py`](../../bootstrap/tests/test_content_scan.py).
  No new public function is added. `_scan_unicode`, `_scan_homoglyph`,
  `_is_confusable_greek` and the range tables are private and reached through
  `scan_text`; `_NO_LATIN_TWIN`, `_IGNORABLE_RANGES`, `_NONCHARACTER_RANGES` and
  `_TAG_RANGE` are read directly **only** by the structural tests B10 and D10,
  which are about the tables' shape rather than the scanner's behaviour.
* **Failure modes.**
  * *Closed* — a malformed or unreadable file: unchanged, `scan_file` propagates.
  * *Open, and intentional* — `unicodedata.name` has no name for a reserved code
    point; the two-argument form supplies a placeholder so the flag still fires.
    **A missing name must never suppress a flag.** B6's noncharacter case covers it.
  * *Open, and intentional* — the confusable set is curated, so an unlisted
    look-alike is a miss. Unchanged in kind from HEAD; the scanner's declared
    witness-not-proof posture.
  * *Open, and named* — a future UCD adds a default-ignorable code point outside
    both the frozen ranges and C2's hand-maintained list. C2 shrinks this hole
    substantially; it does not close it, and `unicodedata` exposes no accessor that
    would.
  * *Open, and priced by the Decision* — whole-script Cyrillic. D8 pins it.
  * *Open, and priced by the amendment* — the beta family, where the look-alike is
    Latin-1 `U+00DF` rather than ASCII. D8 pins it. A maintainer who wants it
    closed moves two code points and pays roughly six more scientific false
    positives; the module doc says so.
  * *Open, and priced by the proposal* — the two-character carve-out. D8 pins it.
    The one case with teeth is a two-letter domain label, and `suspicious-url`
    covers it independently **for an allowlisted domain** (the proposal's original
    example was corrected in its own revision; use the corrected form).
* **Edge cases handled** — empty file; single-character token; a digits-only token
  (no script, never flags); leading BOM (exemption preserved on the new path,
  B8); non-leading BOM; a line mixing an already-covered zero-width character and a
  newly-covered ignorable one (the existing id wins, B8); a line carrying a benign
  variation selector *and* a Tag payload (both named in one message, B9); an
  ignorable code point of category `Lo` sitting **inside** a word without splitting
  the token (C2's Hangul filler case).
* **Known omissions, stated rather than implied.**
  (a) The exhaustive Greek classification the Response recommended is **not**
  delivered; D9/D10 substitute reconciliation and a size pin, and the oracle gap
  is unresolved.
  (b) The `vermin` >= 3.11 floor check is **unrun** and fenced to the Maintainer.
  (c) Performance is measured for one implementation on one machine; the guard's
  direction reproduces across three independent implementations in the record, the
  constant does not.
  (d) No human has read UTS #39's confusables data against `_NO_LATIN_TWIN`; the
  table's judgments are unattested to any external oracle.
  (e) Whole-script Cyrillic and the international-proper-noun question stay open
  and become materially more consequential if
  `dev/proposals/2026-08-03-claude-default-security-stance.md` makes this module a
  default; that sequencing is a Maintainer question this plan raises and does not
  answer.
  (f) The interaction between the two new pattern ids and an adopter's existing
  residual baseline is reasoned from `_flag_fingerprint`'s shape, not tested
  end-to-end through `content_scan_runner.py`.

## Verification

Run under the canonical interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13, UCD 15.1.0) with `PYTHONDONTWRITEBYTECODE=1`. **A different Python
minor silently changes both the suite figure and the UCD the sentinels sweep**, so
name the interpreter alongside any figure asserted.

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

**Plan-specific gates, added because this change touches those surfaces.**

* **The security lint** — `python -m bandit -q
  templates/modules/team-gated/content_scan.py`, expected clean, exit 0.
* **The Python floor** — `python -m pytest bootstrap/tests/test_python_floor.py -v`.
  **It currently skips**: `vermin` is not installed at the canonical interpreter,
  verified for this plan. A skip is **not** a pass; see *The Maintainer fence*.
* **The install contract** — `python bootstrap/scaffold.py --manifest`, diffed
  against a capture taken at the plan-open commit. **Expected empty.** 96 lines
  (95 data rows) `as_of 2026-08-04`.
* **The adopter path** — scaffold a throwaway tree with the `content-security`
  module and run `python scripts/content_scan.py <file>` inside it. The installed
  copy must be byte-identical to the template and behave identically.
* **The corpus tripwire, at full strength.** `python scripts/check_cairn.py` flag
  count **must not move**. Re-measured for this plan at a predicted delta of
  **zero**, now that the two raw ignorable code points in the proposal file have
  been repaired to escaped form. Any movement means the corpus comparison was
  wrong: **re-measure before proceeding, do not suppress the new flag.**
* **The file-by-file flag-set comparison** — for each tracked `.md`, compare the
  full `(pattern_id, line)` set before and after. Predicted: **0 files change**.
  Do this over the full tracked set, not `check_cairn`'s filtered set: the two
  differ (`filter_sources` in `scripts/link_check.py` drops archived deliberation
  files), and the proposal's prediction is stated over the full set.
* **The falsifying sweep** (Chunk D acceptance) — the single most important run in
  this plan. Its output goes in the commit body verbatim.
* **The perturbation ledgers** — per chunk, in the commit body: the change made,
  the failure observed with its message, and the byte-identical restore verified
  with `git diff <path>` (empty). Hazard-side perturbations only.
* **The gate-integrity note** — after the last chunk, record in the commit body
  that `templates/modules/team-gated/content_scan.py` and
  `bootstrap/tests/test_content_scan.py` now differ from their pinned sha256 in
  `bootstrap/tests/fixtures/gate_manifest.json`, and that the collection identity
  has moved. **Do not re-pin**; the ceremony is supervised and is batched with
  `separator-detection`. See *The Maintainer fence*.

**Note on doc gates.** Drift gates catch **drift**, not **absence** of a new doc
update. Confirm each document named in *Acceptance* was actually updated; the
gates do not enforce that, and the module doc's published residual list is the
specific sentence a gate will never check.

## Plan review — the brief, and why the tier is not discharged

*Required — **External**, security lens. Implementation does not start until a
review has landed under this heading.*

**The declared tier is `required(External, security lens)`, and the Internal round
about to run does not discharge it.** Stated plainly because the record makes the
distinction unusually concrete here:

* An Internal round is, by construction, the **same agent type** as the plan's
  author. The proposal's own Internal reviewer said so first and correctly: *"I am
  Claude reviewing Claude... my spoof set is my own construction."* If the author's
  imagination and the reviewer's overlap, both miss the same vector — and the
  vector this change is about is precisely the one an author does not think of.
* **The External tier has effectively not been exercised on the half that removes
  flags.** The proposal's External round returned SHIP, but all three of its swept
  lenses ran the scanner **at HEAD**; no External reviewer has executed the
  narrowed rule against anything. That is established in the record by the author's
  own Response, not asserted here.
* **The curated set has now failed twice, for the same reason both times** — a set
  asserted by judgment and never swept against its own domain. Round one: a
  32-entry allowlist over a 347-letter domain, 15 bypasses. Round two: a denylist
  that clears 14 tokens HEAD flags and omits two letters its own figures require.
  This plan asserts a **third** reading of that set. It reconciles against the
  artifact's published figures, which is more than either predecessor did, but *an
  author reconciling their own reading* is exactly the shape that failed twice.

So: **an Internal plan-review round is welcome as a floor** — it can execute, it
can measure, it can catch an arithmetic error — **and it leaves the tier owed.**
No implementation commit lands on an Internal round alone.

**The four questions this review should aim at, in descending weight:**

1. **Attack `_NO_LATIN_TWIN` adversarially, and do it with a token set you built.**
   Find a spoof HEAD catches that the case-exact seed clears, other than the named
   two-character shape. That is the falsifying test for this whole lifecycle, and
   it has fired on both previous readings. Reproduce the 7/42 and 13/14 figures in
   *Chunk D* first — if either does not reproduce, the plan's interpretive call is
   built on a bad measurement.
2. **Is the Maintainer's id split actually implemented as a split?** Reproduce
   P-B2: merge the Tag rows back into `unicode-ignorable` and confirm B7 goes red.
   If B7 stays green, the split is decoration and the documented remedy for the
   detector's most common false positive is still a working bypass for its
   highest-severity true positive.
3. **Is the drift sentinel real?** Reproduce P-C1: delete the `U+FE00`-`U+FE0F`
   row and confirm **C1 green, C2 red**. If C1 also goes red, [I4] was wrong; if C2
   stays green, Chunk C is decoration.
4. **Is Greek-only defensible, and is the fullwidth arm genuinely free?** The
   Decision prices whole-script Cyrillic out on the ground that authority granting
   is closed elsewhere. Attack that: name a Cyrillic prose-detection consequence
   that `byline-classification` does not cover, or confirm you cannot. And check
   that closing fullwidth script-generally really carries no natural-language cost
   in an English tree.

**Two things a reviewer is invited to strike rather than accept:** the case-exact
reading of `_NO_LATIN_TWIN` in Chunk D (the strike-line is written there), and
C4's widening of `_BANNED_CODEPOINTS`, which is a hygiene strengthening this plan
adds rather than proposal text.

> **The landed review appends here as a `### Plan review -- <reviewer> --
> YYYY-MM-DD` sub-heading** (plus a `### Sharpening` sub-heading if it raised
> findings). **Do not rename this heading to a bare `## Plan review`.** The
> lifecycle checker matches a section *kind*, not a review: with a bare heading,
> an **empty** section satisfies the gate. This heading is shaped so a placeholder
> cannot satisfy it.

## Code review

*Filled in after implementation commits land.* The reviewer is not the
implementing agent. Begin with `**Model**: <model or tier when known; "unknown" if
not. Do not copy-paste an old model label; query and state your actual running
model identity.>` immediately below the section header, or below a
`### Code review -- <reviewer> -- YYYY-MM-DD` sub-heading.

The falsification ledger this review owes, at minimum:

* **Independently re-run the falsifying sweep** over the union of the record's
  token sets, rather than re-trusting the implementing session's transcript. State
  the `missed=` set you got.
* **Independently reproduce P-B2 and P-C1**, the two discriminating pairs.
* **Confirm every perturbation's byte-identical restore** with `git hash-object`
  against `git rev-parse HEAD:<path>` — not by reading the transcript.
* **Confirm the module doc's published residual list was measured against the
  landed implementation**, not carried from this plan. Run the 42-token set
  yourself.
* **Confirm no `cairn-accept` marker was added to any file to make a gate pass.**
  A suppression written to quiet this change is the alarm-fatigue failure the
  proposal exists to prevent, committed by the proposal's own implementation.

## Lasting-truth migration

*Filled in at archive time.* Per the
[Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home outside the
plan. **Pre-declared here so no follow-up is homeless at archive time:**

| Deferred follow-up | Durable home |
|---|---|
| The exhaustive UTS #39-derived Greek classification, and the "as data" fence question (in-module table vs shipped data file) | A new proposal. It changes the shape of a shipped security control and has an unresolved external-oracle dependency; it is not a plan follow-up. |
| Whole-script Cyrillic, and the international-proper-noun cost | A new proposal, to be decided **against a measured corpus of its own** — the Decision says so in terms. Sequenced against `default-security-stance`, not against this plan. |
| The beta-family residual (`U+00DF` is Latin-1, not ASCII) | `templates/modules/team-gated/content-security.md`, as a documented limit with the two-code-point recipe for closing it and its measured cost. Lands in Chunk E, so it is homed on landing rather than at archive. |
| The pinned-snapshot limit of the ignorable table, and C2's hand-maintained non-`Cf` list | `templates/modules/team-gated/content-security.md` (Chunk E) plus the code comment beside the tables. If it recurs across UCD versions, the `incident-trackers` module is the escalation path. |
| The unrun `vermin` >= 3.11 floor verification | *The Maintainer fence* above, and the final commit body. It does **not** archive as discharged unless it was run. |
| The stale gate-manifest pins and collection identity | The supervised re-anchor under `bootstrap/REANCHOR_RUNBOOK.md`, batched with `separator-detection`. Named in the final commit body. |
| The adopter-side stale-residual consequence of Change 2 (`exit 3`) | `CHANGELOG.md > Unreleased > Changed` (Chunk E5). |
| The unbenchmarked interaction of the new detector with `content_scan_runner.py`'s `_MAX_WALL_SECONDS` budget on a large adopter tree | This plan's evidence ledger plus the commit body number; escalates to a proposal only if an adopter reports a breach. |

This section is append-only once written.

## Plan review -- Codex (External, security lens) -- 2026-08-05

**Verdict: REVISE.** The response made a welcome correction: I independently
agree that the `check_cairn` and tracked-Markdown corpus checks cannot evidence
either proposed detector. A zero result over a corpus with no relevant,
unsuppressed material is a test of the corpus, not the detector.

**[E1] The replacement evidence source is still not an acceptance contract.**
AM-14 says to build a purpose-built corpus "at implementation" and AM-5 adds
six more tokens at that time, but it does not bind their identities, expected
outcomes, construction rule, or independence from the classifier being tested.
That leaves the implementer able to select only examples the new rule already
passes. Put a named, review-supplied fixture set in the plan now, with escaped
code points, provenance, and a positive/negative expected result for each
detector clause. The existing six reviewer-built no-Latin tokens are a start;
they need to become a committed test oracle, not a narrative prompt to invent
more evidence later.

**[E2] The curated Greek denylist must be described as a policy judgment, not
as validation by its own figures.** AM-12 correctly reduces D9 to a drift guard,
and the plan admits there is no UTS #39 oracle. I accept that an exhaustive
derivation is out of scope for this optional module, but not a claim that the
seed is independently established. Require the shipped documentation and
commit record to say that the listed ASCII-twin families are reviewed curation,
with the exact known false-negative boundary. Do not use the residual-count
reconciliation or a self-selected corpus as evidence that the judgments are
correct.

**[E3] The default-on consequence needs an explicit sequencing guard.** The
plan says whole-script Cyrillic and international-name cost become materially
more consequential if `content-security` becomes a default, yet leaves that to
an unanswered Maintainer question. Detection work can remain optional, but a
default-security implementation must be prohibited from selecting this module
until that decision has a recorded disposition and a corpus appropriate to
default adoption. State that cross-plan gate in both plans, rather than relying
on a reader to infer it from a known omission.

I inspected the effective amendments AM-1--AM-18 and the figure correction. I
also executed the current direct scanner suite under the canonical interpreter:
`bootstrap/tests/test_content_scan.py` has `25 passed`. I did not treat current
repository Markdown or the proposal's suppressed examples as security evidence,
and I did not run hypothetical production-code perturbations.

---

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`), queried at review time, not copied
from a prior label.

*Placement note.* The plan's *Plan review -- the brief* section asks a landed
review to append there as a `### Plan review -- <reviewer> -- <date>`
sub-heading. This round was commissioned with an explicit end-of-file `##`
heading, so it lands here; retitling or relocating it is a one-line edit for
whoever files the External round, and nothing in the lifecycle gate depends on
which of the two the Maintainer prefers.

**Standing, stated before anything else.** I am Claude reviewing a plan written
by Claude. There is **no cross-type independence** in this read: a blind spot the
author has, I probably share, and the plan says so itself in terms I cannot
improve on. **This round does NOT discharge the plan's declared tier.** The tier
is `required(External, security lens)`, carried from the proposal header and
restated in the Decision; it stays owed after this section lands. What an
Internal round can do is execute, measure, and arithmetic-check, and that is what
this one did: every figure below is a run, not a reading. Where I built code to
test a claim, it is **my reconstruction of the plan's prose, not the author's
code**, and it is labelled as such at every use. No repository file was modified;
no source file was touched; nothing was committed, added, or moved.

Both mandated checkers were run at `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13, UCD 15.1.0):

```
claim_check: dev/plans/content-scan-detectors.md -- OK, no claim-check flags.        (exit 0)
check_cairn: OK -- 1 Markdown file(s) scanned; no issues.                            (exit 0)
```

### Steelman

This is the strongest plan I have read in this tree, and most of what it claims
is true. Its central moves are right and they are *demonstrated* rather than
asserted:

* **The `_scan_unicode` prose-dispatch finding is exactly correct and correctly
  sequenced.** `templates/modules/team-gated/content_scan.py:402` reads
  `pid = "unicode-bidi" if "bidirectional" in msg else "unicode-zero-width"` --
  verbatim, at that line. A new id introduced over that call site is silently
  relabelled `unicode-zero-width`, its promised `cairn-accept` marker matches
  nothing, and any existing `unicode-zero-width` suppression anywhere in the tree
  hides it. Making Chunk A a **precondition** rather than a tidy-up is the right
  call, and writing it to be correct in either landing order with the sibling is
  the right engineering.
* **[I4] is real and I re-derived it independently.** Sampled
  Default_Ignorable members are `Lo`/`Mn` with **no** `Cf`; **every**
  noncharacter is `Cn`; 170 `Cf` code points exist in UCD 15.1.0. A `Cf` sweep
  guards neither the non-`Cf` ignorable rows nor **any** of the 18 noncharacter
  rows. The C1/C2/C3 three-sentinel replacement, and the P-C1 discriminating pair
  (*C1 green, C2 red* in the same run), are the correct shape: the pair is what
  converts a finding into a guard.
* **[I5] is a real finding, not a style note**, and the replacement is right:
  `str` immutability makes the specified assertion pass against a scanner that
  strips ignorables, and P-C4's second half -- running the retired form against a
  deliberately-rewriting scanner and observing it **pass** -- is the evidence,
  not the argument.
* **The [I6] guard reproduces, closely.** My own independent walk over the
  tracked `.md` corpus (235 files, 91 182 lines, 5.81 MB, best of three):
  HEAD `_scan_unicode` **0.220 s**, naive table walk **5.953 s (27.1x)**, the
  same walk with the `U+00AD` short-circuit **0.118 s (0.54x)**. The plan's
  0.218 / 5.757 / 0.121 are within noise of that. Against
  `content_scan_runner.py:83`'s `_MAX_WALL_SECONDS = 120.0` fail-closed ceiling
  (verified at that line), the direction is the load-bearing claim and it holds.
* **The Maintainer's id split is correctly identified as load-bearing**, and
  P-B2 (merge the Tag rows back, watch B7 go red) is the perturbation that proves
  it rather than decorating it.
* **The gate accounting is honest and, where checkable, exact.** 164 frozen
  entries; both edited files present with hashes matching the live tree;
  `content-security.md` genuinely not frozen; collection pinned at 1598/1598;
  `scaffold.py --manifest` at 96 lines with the expected verbatim row. The
  Maintainer fence -- do not re-pin, batch with `separator-detection`, a skip is
  not a pass -- is the right disposition and the sibling plan does adopt the
  identical rule (checked in its own fence section).
* **Every line citation in the plan is exact.** Ten spot-checks, ten hits.
* **The `_flag_fingerprint` reasoning is correct.**
  `content_scan_runner.py:291-299` hashes `rel:pattern_id:sha256(line.strip())`
  -- the *message* is not an input, so [I3] remedy 2's enrichment churns no
  residual fingerprint. Verified, not reasoned.
* And the plan's self-assessment of its weakest joint is accurate: it *says*
  the curated set has failed twice for the same reason, it *says* an author
  reconciling their own reading is that same shape a third time, and it hands
  the reviewer a strike-line. Findings [I1] and [I5] below are the plan's own
  warning coming true, which is a point in the plan's favour, not against it.

### Concerns

#### [I1] The falsifying test fires a third time. The three-clause rule releases every token that mixes two non-Latin confusable scripts with no Latin character -- a class HEAD flags, no clause covers, and no Decision priced.

Clauses 2 and 3 both predicate on **Latin being present** ("mixed with Latin").
Clause 1 covers only all-Greek and all-fullwidth. So a token whose scripts are,
say, Cyrillic + Armenian, or Cyrillic + Coptic, or Greek + Cyrillic, with **zero**
Latin characters, falls through all three clauses. HEAD flags it, because HEAD's
rule is `len(_token_scripts(token)) > 1`
(`templates/modules/team-gated/content_scan.py:357`) and does not care which
scripts.

Measured. HEAD column is the **shipped scanner**; the `rule` column is **my
reconstruction of the plan's clause prose**, not the author's code. Tokens are
mine, built for this review, none drawn from the record:

```
token (reviewer-built, no Latin character)                     HEAD    rule
Cyrillic s,e,c,c,i,o + Armenian n   -- renders "session"       flag    CLEAR
Armenian r + Cyrillic o,n,i,o       -- renders "ronin"         flag    CLEAR
Cyrillic o + Coptic + Armenian r                               flag    CLEAR
Greek U+03C1 + Cyrillic a,s,s       -- renders "pass"          flag    CLEAR
Cyrillic a,d + Armenian m,i,n       -- renders "admin"         flag    CLEAR
Cyrillic o + Greek U+03C1 + Cyrillic e,n                       flag    CLEAR
```

Six for six. **None of them is the named two-character shape**, so the proposal's
falsifying criterion -- *"a spoof that HEAD catches and the patch clears, other
than the named two-character shape"* -- is met, on a class the record never
imagined.

Three consequences, each independently worth fixing:

1. **The plan's clause-2 sentence is false.** It says "Non-Greek confusable
   script mixed with Latin always flags. Cyrillic, Armenian, Cherokee, Coptic,
   fullwidth. **Unchanged behaviour from HEAD.**" It is not unchanged from HEAD
   for any token without a Latin character. The Maintainer direction narrowed
   clause 1 from the proposal's script-general form
   (`dev/proposals/2026-08-03-claude-content-scan-detectors.md:163`: *"the token
   has no Latin characters, has at least three letters, and every letter has an
   ASCII-Latin look-alike"*) to Greek-only, and nothing was added to catch what
   the old clause-1-plus-HEAD-rule pair used to catch between them.
2. **D12 cannot detect it.** The retained
   `TestHomoglyphExpandedScripts::test_expanded_confusable_scripts_flagged`
   (verified at `bootstrap/tests/test_content_scan.py:81-87`) tests
   `A<U+0561>bc`, `A<U+13A0>bc`, `A<U+2C80>bc`, `A<U+0430>bc` -- **all four carry
   Latin**. It passes unmodified while the hole is wide open, which is precisely
   the "an edit to that test would be the tell" argument failing in the
   direction the plan did not consider.
3. **The specified falsifying sweep cannot find it, by construction.** The Chunk
   D acceptance criterion says to sweep "the union of every token set in the
   proposal's record". Those sets are 42 + 83 scientific, 21 hand-built, 153
   single-substitution, 40 maximal-substitution, 41 and 51 spoof -- and the
   maximal-substitution family is documented single-script Greek
   (`...:187-193`, `missed=['<U+03B5><U+03C7>...', ...]`). **No set in the record
   contains a no-Latin multi-script token.** So the sweep is guaranteed to return
   "the two-character shape and nothing else" whether or not the rule is sound.
   This is the recurring failure the brief names: *the artifact under
   verification supplying the material used to verify it.* The sweep is a
   regression check against the record's imagination, and the plan cites it as
   "the single most important run in this plan".

**Remedy, cheap and script-general.** Add a clause 0 before the others: *two or
more distinct confusable scripts in one token always flags* -- which is exactly
HEAD's rule restricted to the no-Latin case, so it removes zero flags relative
to HEAD and costs no scientific notation (a token with no Latin character is not
`<U+0394>G`). Then clauses 1-3 do what the Decision asked without opening a new
hole. If instead this class is to stay open, it is a **new** declared residual,
not the priced Cyrillic one -- the Cyrillic residual is *whole-script*, and
`<U+03C1>` + Cyrillic `a,s,s` is neither whole-script nor Cyrillic. A new
residual needs the Maintainer, not a plan sentence.

#### [I2] The NFD fold is not inert. Twenty Greek code points join `_NO_LATIN_TWIN` through it, and the plan predicts zero -- then pre-commits to a branch that measurement does not take.

The Chunk D acceptance criterion says: *"Under the case-exact seed, **no**
precomposed or Greek Extended form appears to fold onto a seeded base, which
would make the folding inert. Measure it: report how many of the 218 assigned
Greek Extended letters fold onto a `_NO_LATIN_TWIN` member... If the number is
zero, say so in the code comment and keep the fold... if it is not zero, the
cleared set must be listed and put to the plan reviewer."*

Measured (`unicodedata`, UCD 15.1.0), seed plus the three admitted symbol
variants:

```
non-seed Greek letters whose NFD base is a _NO_LATIN_TWIN member : 20
  U+038F  GREEK CAPITAL LETTER OMEGA WITH TONOS            (Greek and Coptic block)
  U+1F68 .. U+1F6F   OMEGA WITH PSILI / DASIA / VARIA / OXIA / PERISPOMENI  (8)
  U+1FA8 .. U+1FAF   the same, WITH PROSGEGRAMMENI                          (8)
  U+1FFA, U+1FFB, U+1FFC   OMEGA WITH VARIA / OXIA / PROSGEGRAMMENI         (3)
```

Nineteen are in Greek Extended; the twentieth, `U+038F`, is in **Greek and
Coptic** -- a block the plan's measurement question does not even scope, so the
under-scoped question would have under-counted even if it had been asked
honestly. Concrete effect, HEAD = shipped scanner, `rule` = my reconstruction:
`U+038F`+`mega`, `U+1F68`+`mega`, `U+1FFB`+`mega` are **flag -> CLEAR** in all
three cases.

The severity is *modest* -- these are all capital-omega variants and omega is a
weak ASCII twin at best -- but the finding is not about severity. It is that the
plan states a measurement result it did not take, in a section whose own last
sentence is **"Do not ship a mechanism described as a guard without a number
saying what it guards."** The number is 20, the cleared set is listed above, and
the plan's stated branch ("say so in the code comment and keep the fold as
declared defence") is the wrong branch. Under a **denylist**, folding widens
clearing -- the plan correctly identifies that the polarity inverted when the
set inverted, and then reports the pre-inversion answer.

#### [I3] D2's fold arity is unspecified, and the most natural reading crashes the scanner on ordinary polytonic Greek.

D1 holds `_NO_LATIN_TWIN` as "a `frozenset` of Greek code points **written as
`\uXXXX` escapes or integer literals**" -- chars or ints, unresolved. D2 says
`_is_confusable_greek(ch)` is "NFD-fold, then test non-membership in
`_NO_LATIN_TWIN`". `unicodedata.normalize("NFD", ch)` returns a **string**, and
**217 of the 218** assigned Greek Extended letters decompose to more than one
character. Measured:

```
>>> ord(unicodedata.normalize("NFD", "ἀ"))
TypeError: ord() expected a character, but string of length 2 found
```

Failure scenario: the implementer writes the int-set form
(`ord(unicodedata.normalize("NFD", ch)) not in _NO_LATIN_TWIN`), which D1's
"integer literals" clause invites; an adopter scans a file containing any
polytonic Greek word -- a classics repository, a quoted epigraph, a Unicode test
fixture; `_scan_homoglyph` raises `TypeError`; the plan's own failure-mode table
says *"a malformed or unreadable file: unchanged, `scan_file` propagates"*, so
the exception leaves the scanner and aborts the audited run. In a fail-closed
security runner that is a **denial-of-scan triggered by legitimate content**, and
nothing in the plan's test list touches Greek Extended at all: D4-D11 are drawn
from `U+0370`-`U+03FF` exclusively.

The fix is two words in D2 (`normalize(..., ch)[0]`) plus one decision in D1
(chars, not ints), and one new test: assert `scan_text` **does not raise** across
all 347 assigned letters in the two Greek `_SCRIPT_RANGES` rows. That test also
gives D10 a companion with teeth -- D10 checks the table's *members* are in
domain, and nothing checks the *function* survives its domain.

#### [I4] The nine seeded members -- the only load-bearing part of `_NO_LATIN_TWIN` -- are exempted from the plan's own admission rule, and one of them is invisible to both figures the plan uses to justify the seed.

The rule reads: *"Admit any further code point only on a per-code-point
justification against the ASCII alphabet, recorded in a comment beside the entry.
Membership is **never** inherited from a base letter."* That rule governs only
what is admitted **beyond** the seed. It therefore applies to `U+03D1`, `U+03D5`,
`U+03D6` -- which clear nothing in any published figure -- and it refuses
`U+03F2` -- correctly. Meanwhile the nine seeded letters, which do **all** of the
clearing, are admitted by inheritance from the artifact the plan itself says
failed twice, with no per-code-point justification required.

That would be defensible if the seed were pinned by measurement. It is only
partly. Measured, dropping `U+03BC` from the seed:

```
seed as the plan lists it       sci FP = 7/42    [I1]-token kept = 13/14
seed WITHOUT U+03BC             sci FP = 7/42    [I1]-token kept = 13/14
```

**Identical.** Neither of the plan's two decisive measurements touches `U+03BC`
at all -- the micro tokens in the 42-token set are `U+00B5` MICRO SIGN, not
`U+03BC`. Its membership rests entirely on the assertion that the amendment's
*Named residual* and its 14/83 figure "require it to contain" it, and the plan
does not reproduce the 83-token set. So the one seeded letter with the most
arguable ASCII twin (`u`) is the one seeded letter no measurement in this plan
constrains.

(Adjacent, and worth a sentence in the module doc rather than a finding: RV5
already clears short micro-prefixed tokens at HEAD -- `U+03BC`+`ser` and
`U+03BC`+`rl` are **HEAD-clean** today, verified with the shipped scanner. So
`U+03BC`'s real new exposure is longer tokens such as `U+03BC`+`pload`, which
HEAD flags and the rule clears.)

Minimum ask: write the per-code-point justification for all nine seeded letters,
under the same rule the plan applies to the three additions, and mark which of
the nine are pinned by a published figure (`U+0394`, `U+03BB`, `U+03C3`,
`U+03B8`, `U+03C6`, `U+03C8`, `U+03B2`, `U+03A9` move 7/42) and which are not
(`U+03BC`).

#### [I5] "The proposal's own falsifying criterion no longer fires" is retired by definition, not by measurement.

Measured, HEAD = shipped scanner, `rule` = my reconstruction of the plan's
clauses:

```
reviewer-built token          HEAD    rule
U+0394 + "elete"              flag    CLEAR
U+03BB + "ogin"               flag    CLEAR
U+03C6 + "ile"                flag    CLEAR
U+03A9 + "mega"               flag    CLEAR
U+03B2 + "ank"                flag    CLEAR   (priced: the beta family)
U+03B2 + "ase64"              flag    CLEAR   (priced: the beta family)
U+03BC + "pload"              flag    CLEAR
```

Seven token families, none of them the two-character shape, every one a spoof
HEAD catches and the rule clears. The plan's answer is that these letters "cannot
power a visual spoof **by definition of the threat**". That may well be right --
but it is a **judgment**, and the plan's own *Known omissions* (d) concedes it is
"unattested to any external oracle". So the criterion is satisfied only by
accepting the exact judgment that failed in round one (a 32-entry allowlist over
a 347-letter domain, 15 bypasses) and round two (a denylist clearing 14 tokens
HEAD flags). Round three retires the criterion by redefining its subject.

I am not asserting `U+0394`/`U+03BB`/`U+03C6`/`U+03A9` **are** convincing
spoofs -- I think most are not. I am asserting that the plan's claim "the
falsifying criterion no longer fires" is stronger than its evidence supports, and
that a claim of that weight in a security control should be restated as what it
is: *"no spoof HEAD catches is cleared **except** the two-character shape and the
seven seeded-letter families, whose ASCII-twin status is asserted by judgment and
unattested."* That sentence is checkable; the current one is not.

#### [I6] D9's channel note claims an independence the selection step destroys.

The Chunk D channel note says *"D9's oracle is the proposal's own **published
figures**, an artifact written before the implementation existed."* True of the
artifact; false of the coupling. The plan **chose** the case-exact seed *because*
it reproduces the published 7/42 -- that is the argument of the whole
sub-section, and its first bullet is "7 / 42 is exactly the figure the amendment
publishes". D9 then asserts that the implementation reproduces 7/42. The oracle
supplied the subject; D9 cannot fail for the seed as selected.

D9 is still worth having -- as a **drift** guard it has real teeth, and P-D1's
"add `U+03B3`, watch the seven become six" is a correct hazard-side perturbation.
But the channel note should say drift, not independence, and the *Author-
accounting* invariant "`_NO_LATIN_TWIN` agrees with the figures the module doc
publishes" should be read for what it is: a consistency check between two
descriptions of the same judgment, not a check that the judgment is right. The
plan gets three-quarters of the way to saying this ("it does not convert it into
'the table covers its domain'") and then the channel note takes it back.

#### [I7] The `check_cairn` corpus tripwire cannot move for Change 1, so it is not the guard the plan says it is.

The plan calls the zero-delta `check_cairn` flag count "the proposal's own
signal-the-change-is-wrong tripwire, and it is at full strength again now that
the `+2` exposure has been repaired". Measured, it has no strength on Change 1 at
all:

* `scripts/check_cairn.py` scans **tracked Markdown only** -- its own header says
  *"the whole tracked Markdown tree (`git ls-files '*.md'`)"*, and it composes
  `content_scan.scan_file` over those files (`scripts/check_cairn.py:393`).
* **Zero** tracked `.md` lines carry any code point in the ignorable-union-
  noncharacter set. All nine lines the plan counts are in `.py` files:

```
bootstrap/tests/test_content_scan.py         L138 L142 L148 L149 L150 L205 L208
scripts/link_check.py                        L87
templates/modules/team-gated/link_check.py   L87
```

So Change 1 adds exactly zero `check_cairn` flags **whether the detector is
correct or broken**. The tripwire is a guard against someone planting a raw code
point in Markdown, not a verification of this change. The plan's own
file-by-file `(pattern_id, line)` comparison "over the full tracked set" is the
run with power -- and it should be stated that its `.md` half is 0-vs-0 by
construction, so the informative half is the `.py`/`.txt` half plus a corpus that
actually contains the newly-covered code points. Presenting a structurally-null
check as a restored tripwire is the kind of sentence this plan exists to
prevent.

#### [I8] Cairn's corpus is a biased oracle for exactly the cost Change 1 imposes on adopters, and the plan prices only the other direction.

Measured over the 453 tracked `.md`/`.txt`/`.py` files: **zero** lines carry
`U+FE0F` VARIATION SELECTOR-16. That is not evidence that variation selectors are
rare; it is the house emoji rule showing up in the data. `unicode-ignorable`
fires on `U+FE0F`, and `U+FE0F` is how ordinary Markdown writes `warning`,
`check`, and most other emoji. An adopter with an emoji-bearing README gains one
`unicode-ignorable` flag **per emoji line** on upgrade, each requiring a
`cairn-accept` marker with reason/reviewer/date or a baseline fingerprint.

That is Defect (b) -- "the homoglyph rule cries wolf at ordinary scientific
notation", the cry-wolf defect this proposal exists to fix -- reintroduced
through Change 1 on a different axis, and the plan's zero-cost evidence comes
from the one corpus structurally guaranteed not to show it. The plan *notices*
the fact (`U+FE00`-`U+FE0F` is "benign-and-common -- emoji use it") and uses it
to justify the id split, then never carries it into a cost estimate.

The adopter-facing accounting is one-sided to match: the Chunk E acceptance
bullet and E5's changelog line cover only Change 2's **clearing** direction (a
stale `homoglyph` fingerprint going `STALE` at exit 3). The Change 1 **adding**
direction -- a previously-clean adopter tree that now fails -- is not in the
changelog, not in `content-security.md`, and not in the commit-body obligation.
Minimum ask: measure `U+FE0F` density on one emoji-bearing corpus outside this
repository, state the number, and give the `Added` changelog line the same
upgrade-consequence sentence the `Changed` line gets.

#### [I9] B10 as literally specified raises rather than asserts, and it pins the table without pinning the guard. (Minor.)

`min(lo for lo, _ in _IGNORABLE_RANGES + _NONCHARACTER_RANGES + [_TAG_RANGE])` --
B1 declares both tables as **tuples** of pairs, and `tuple + list` raises
`TypeError`. A typo, and it would surface on the first run; noted so it does not
consume a debugging cycle.

The substantive half: B10 compares the table minimum against a hard-coded
`0x00AD` rather than against the guard constant the module actually uses, so it
enforces "the table never drops below `U+00AD`" and **not** the invariant the
plan claims for it -- *"the ASCII short-circuit can never skip a detected code
point."* A future author who raises the guard leaves B10 green. B6 does catch
that today (its lowest case is `U+00AD` itself), so this is hardening rather than
a hole; but the invariant table in *Author-accounting* names B10 as the enforcer,
and B10 is not it. Assert against the module's own constant and the coupling
becomes real.

#### Carried figures that have already drifted (not a numbered finding, but the plan's own indictment applies)

Re-measured just now, same interpreter, same machine:

| plan says | measured 2026-08-04 |
|---|---|
| suite collection **1746** nodes | **1749** |
| **234** tracked `.md` | **235** |
| **452** tracked `.md`/`.txt`/`.py` | **453** |
| `check_cairn` 180 Markdown / 68 external | **180 / 68** -- exact |
| `scaffold.py --manifest` 96 lines | **96** -- exact |

The tree is being edited by concurrent sessions **while this review runs**:
`bootstrap/tests/test_scaffold.py` became modified and one plan file left the
untracked set between my first and second `git status`. The plan says "Re-measure,
do not carry" -- and then states **1746** as an acceptance-criteria baseline
("Collection baseline 1746 nodes `as_of 2026-08-04`; it grows by exactly the new
nodes and drops none"). An implementing agent that computes its delta against
1746 will report a wrong number. Make the baseline a *procedure* ("capture
immediately before the first chunk"), not a constant.

### Covered

Every line below is a run at `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13, UCD 15.1.0), `PYTHONDONTWRITEBYTECODE=1`, working tree at
HEAD `eacb7dd` plus concurrent uncommitted work by other sessions.

**Reproduced with the shipped scanner (no reconstruction in the loop):**

```
len(SCI42) = 42
HEAD scientific FPs: 37/42     <- token-for-token identical to the proposal's list
HEAD flags I1 tokens: 14/14
```

**Reproduced with my reconstruction of the plan's clause prose (NOT the author's code):**

```
recon scientific FPs: 7/42
  U+03BD+max, U+03C9+opt, U+03BA+eff, U+03B1+level, U+03B7+eff, U+03B3+ray, U+03B1+decay
I1: HEAD flags & recon KEEPS  : 13/14
I1: HEAD flags & recon CLEARS :  1/14  -- the two-character U+03B4+o shape, as named
```

The seven residual tokens are **exactly** the seven the proposal commits the
module doc to naming (`...:435-437`). The plan's interpretive call reproduces on
both figures.

**Unicode / UCD claims, all exact:**

```
unicodedata.unidata_version = 15.1.0
Greek _SCRIPT_RANGES span : 400 code points   assigned letters: 347  [129 + 218]
sampled default-ignorable categories : ['Lo', 'Mn']      any Cf: False
noncharacter categories              : {'Cn'}
total Cf code points in UCD 15.1.0   : 170
fullwidth U+FF21-U+FF5A rows whose NFKC is not a single ASCII char : 0
```

The last line confirms the plan's "bijection by construction" claim for the
fullwidth arm -- **and** shows a stdlib oracle exists for it:
`unicodedata.normalize("NFKC", ch)` is `A`-`Z`/`a`-`z` for every one of those 58
code points. The fullwidth arm could be *derived* rather than range-asserted, at
zero dependency cost. Offered as a strengthening, not a finding.

**Corpus sweep, reproduced:**

```
tracked files (.md/.txt/.py) : 453
lines carrying a covered code point            : 9
lines carrying an UNOWNED covered code point   : 0
lines carrying U+FE0F                          : 0
```

**Performance, independently re-run (235 files / 91 182 lines / 5.81 MB, best of three):**

```
HEAD _scan_unicode   0.220 s
naive walk           5.953 s   (27.1x)
guarded walk         0.118 s   (0.54x)
```

**Line citations -- ten checked, ten exact:** `content_scan.py:29` (the
`What it flags` list opener), `:40` `unicode-zero-width`, `:43` `unicode-bidi`,
`:46` `homoglyph`, `:401-403` with the ternary verbatim at `:402`;
`content-security.md:138-144` (*Scientific-unit homoglyph allowance*) and
`:25-33` (the *Template content* blockquote); `test_content_scan.py:47-52`
(`_BANNED_CODEPOINTS`, and `0x00AD` is indeed **absent**, so P-C3's "green at
HEAD, red after C4" pair is real) and `:81`; `test_gate_manifest.py:67`
(*"shipped scanner / security-gate implementations ARE frozen"*);
`content_scan_runner.py:83` (`_MAX_WALL_SECONDS = 120.0`) and `:291-299`.

**Gate accounting:** 164 `frozen_files` entries; both
`templates/modules/team-gated/content_scan.py` and
`bootstrap/tests/test_content_scan.py` present with sha256 **matching the live
tree**; `templates/modules/team-gated/content-security.md` **not** frozen;
`collection.node_count = 1598` with 1598 `node_ids`.
`python bootstrap/scaffold.py --manifest` emits **96** lines and carries
`scripts/content_scan.py<TAB>modules/team-gated/content_scan.py<TAB>verbatim`.

**Scope fences, each checked:** three presets (`solo-greenfield`,
`collaborative-team`, `high-rigor-legacy`) and **none** selects
`content-security`; `dev/modules/` holds **18** files with **no**
`content-security` mirror;
`templates/modules/team-gated/content_scan_residuals.txt` has **0**
non-comment lines, so no adopter inherits a fingerprint from Cairn; `vermin`
is **absent** (`No module named vermin`) so `test_python_floor.py` skips;
`bandit 1.9.4` is present.

**Sibling coordination:** `dev/plans/separator-detection.md` does adopt the
identical rule -- neither plan re-pins, one ceremony, one shared `CHANGELOG.md`
line -- and does record that the `gate-reanchor-preflight` batch is archived.
The plan's cross-reference is accurate.

**Perturbations, named against the hazard.** Every perturbation the plan
specifies is hazard-side (it changes the scanner or a table, never a test body),
which is the right discipline and rarer than it should be. Reading each one
against the state it would have to detect, the two the plan calls discriminating
(P-B2, P-C1) are correctly constructed, and P-D3's *"D7 red and D6 green"* pair is
the right shape for proving the fullwidth arm is separate rather than folded in.
**The perturbations this plan omits** are the ones for the hazards above: nothing
perturbs the no-Latin multi-script case ([I1] -- add a Cyrillic+Armenian token to
D5 and it becomes a real guard), nothing perturbs the NFD fold ([I2] -- swap
`normalize("NFD", ch)` for `ch` and no listed test moves, because no listed test
uses a decomposable letter), and nothing exercises Greek Extended at all ([I3]).

### Not covered / low confidence

* **The 17-row ignorable table's completeness against RFC 8264 s 9.13 is
  unverified.** `unicodedata` exposes no Default_Ignorable accessor -- I probed
  and confirm the plan's statement -- and I did not fetch DerivedCoreProperties
  from outside the tree. I checked what is checkable: the **minimum** across both
  tables is `U+00AD` (which licenses the [I6] guard), and the 18 noncharacter
  rows are arithmetically right (1 + 17 planes). The 17 ignorable rows are taken
  on the author's word.
* **My homoglyph rule is a reconstruction from the plan's prose, not the
  author's code.** [I1], [I2] and [I5] are claims about *the rule as the plan
  states it*. An implementer who writes clause 2 as "two or more confusable
  scripts" rather than the plan's "mixed with Latin" would not have [I1] -- which
  is itself the argument for fixing the plan's sentence rather than trusting the
  implementation to be luckier than its specification.
* **I did not reproduce the 83-token, 21-token, 153-token, 40-token, 41-token or
  51-token sets** -- they are not enumerated in the record in a form I could
  extract without transcription risk. [I4]'s `U+03BC` finding is therefore
  bounded: it says the *plan's own two figures* do not constrain `U+03BC`, not
  that the 83-token figure is wrong.
* **No perturbation was executed against real code**, because no implementation
  exists. Every P-* verdict above is a reading of the specified perturbation
  against the specified test, not a run.
* **Brief question 4 (Cyrillic), partially answered.** I did not find a Cyrillic
  prose-detection consequence outside `byline-classification`'s reach, and I did
  not attack it hard -- one Internal round is the wrong instrument for that
  question. But note the framing correction [I1] forces: the class I *did* find
  is **not** the declared Cyrillic residual. Greek `U+03C1` + Cyrillic `a,s,s` is
  neither whole-script nor Cyrillic-only, and no Decision priced it.
* **The adopter path was not exercised end-to-end.** I did not scaffold a tree,
  did not run `content_scan_runner.py`, and did not test the residual-baseline
  interaction. The plan's own omission (f) already says the fingerprint reasoning
  is untested end-to-end; [I8] adds that the *volume* of new adopter-side flags
  is unmeasured on any corpus that could show it.
* **Vendor-neutrality and quality gates** were not run over the plan (it is a
  `dev/` deliberation artifact; the plan schedules them for the Chunk E edits).

### Recommendation

**A second round is required, and it is the External round -- this one does not
substitute for it.**

Three findings are **pre-implementation blockers**, in the sense that landing
Chunk D as written would ship a security control weaker than HEAD on a class the
record never priced:

* **[I1]** -- the rule releases every no-Latin multi-script token; the fix is a
  clause 0, or a Maintainer-priced residual. The specified falsifying sweep
  cannot find this, so the sweep must be widened with reviewer-built tokens
  before it is treated as evidence.
* **[I2]** -- the NFD-fold measurement the plan pre-commits to reports 20, not
  zero, and the cleared set is listed above; the plan's own conditional branch
  says that goes to the plan reviewer, so it is now discharged and the code
  comment must carry 20.
* **[I3]** -- pin the fold's arity and the set's element type, and add a
  does-not-raise sweep over all 347 Greek letters, before any Greek-facing code
  is written.

Three more should be **fixed in the plan text** rather than deferred to code
review: **[I4]** (justify the nine seeded letters under the plan's own admission
rule; mark `U+03BC` as figure-unconstrained), **[I5]** (restate the
falsifying-criterion claim to what the evidence supports), and **[I8]** (measure
`U+FE0F` density on a corpus that has some, and give the `Added` changelog line
an upgrade-consequence sentence). **[I6]**, **[I7]** and **[I9]** are wording and
one typo -- they cost the plan credibility on claims it did not need to make, and
each is a one-paragraph repair.

On the two things the plan invites a reviewer to strike: I would **not** strike
C4's `_BANNED_CODEPOINTS` widening -- P-C3's green-then-red pair shows it closes
a real gap at no cost. On the case-exact reading of `_NO_LATIN_TWIN`, I confirm
the arithmetic that motivates it (7/42 and 13/14 both reproduce exactly), so the
*reading* is well-evidenced; what is not evidenced is the **seed's** ASCII-twin
judgment, which [I4] and [I5] leave standing as the plan's largest unattested
surface and which no same-type reviewer -- including this one -- is the right
instrument to settle.

---

## Response to plan review -- Claude (author) -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`), queried at response time, not copied
from a prior label.

**Standing, and what this Response is not.** I am the plan's author responding to
an Internal round written by the same agent type. **This Response does not
discharge the plan's declared tier**, and neither did the round it answers. The
tier is `required(External, security lens)`; it stays owed after this section
lands, and no implementation commit may proceed on the strength of an author's
Response to a same-type review. What a Response can do is disposition, amend, and
**re-measure** — and the re-measurement is the part with teeth here, because the
review was written against HEAD `eacb7dd` and the tree has moved to `e20b18e`
since.

Every figure below is a run at `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13, UCD 15.1.0), `PYTHONDONTWRITEBYTECODE=1`, working tree at HEAD
`e20b18e`. **No repository file was modified to produce any of them**; the
homoglyph reconstruction lives in a scratch directory outside the repository and
is *my reconstruction of the plan's clause prose*, labelled as such at every use.
The shipped scanner supplied every `HEAD` column. Both mandated checkers were run
over this file:

```
claim_check: dev/plans/content-scan-detectors.md -- OK, no claim-check flags.   (exit 0)
check_cairn: OK -- 195 Markdown file(s) scanned; no issues; 68 external link(s)
             not probed.                                                        (exit 0)
```

**Headline.** Nine findings: **eight accepted** (two with modification), **one
accepted with its remedy corrected**, **zero declined**. Every acceptance carries
mechanical residue in the *Amendments in force* table below — a superseded row, a
new row, a new perturbation, or a retired obligation. And the re-measurement
produced **two things neither the plan nor the review has**: the plan's `vermin`
fence rests on a **false premise** that the review confirmed with the wrong
oracle, and the review's own [I7] understates itself — the `check_cairn` tripwire
is structurally null for **Change 2 as well**, for a reason that is this cycle's
recurring failure in its purest form.

### 1. Re-measurement: the plan's own figures against the live tree

| the plan states (`as_of 2026-08-04`, HEAD `eacb7dd`) | live tree, HEAD `e20b18e` | verdict |
|---|---|---|
| Suite collection **1746 nodes** | **1790** | drifted (+44) |
| `check_cairn` **180** Markdown / **68** external | **195 / 68** | Markdown drifted; external exact |
| **234** tracked `.md` | **249** | drifted |
| **452** tracked `.md`/`.txt`/`.py` | **469** | drifted |
| **9 lines** carry a covered code point, **0** unowned | **9 / 0**, identical file:line list | **exact** |
| 17 ignorable rows, 18 noncharacter rows, lowest `U+00AD` | **17 / 18 / U+00AD** | **exact** |
| **164**-entry `frozen_files`; both edited files present, hashes match the live tree | 164; both present; **both match** | **exact** |
| `content-security.md` **not** frozen | not frozen | **exact** |
| `collection.node_count = 1598`, 1598 `node_ids` | **1598 / 1598** | **exact** |
| `scaffold.py --manifest` **96** lines (1 header + 95 data) | **96**, header at line 1 | **exact** |
| `test_gate_manifest.py:67` asserts the scanner frozen | verbatim at that line | **exact** |
| sampled Default_Ignorable categories `['Lo','Mn']`, any `Cf` **False**; noncharacters `Cn`; **170** `Cf` in UCD 15.1.0 | `['Lo','Mn']` / False / `['Cn']` / **170** | **exact** |
| Greek `_SCRIPT_RANGES` span **400** code points, **347** assigned letters (129 + 218) | 400 / **347** / 129 + 218 | **exact** |
| HEAD flags **37/42** scientific tokens | **37 of the 37 published** false positives flag | **exact** |
| case-exact seed leaves **7** residuals, exactly the seven the module doc is committed to naming | **7**, token-for-token the named seven | **exact** |
| **13 of [I1]'s 14** tokens stay flagged; the cleared one is the two-character shape | **13/14**; cleared = `U+03B4`+`o` | **exact** |
| `U+03C1 U+03BF U+03C3 U+03B9` predicted to stay missed because `U+03C3` is seeded | still missed; the other six HEAD-missed maximal tokens are caught | **exact** |
| Perf: HEAD 0.218 s / naive **5.757 s (26.4x)** / guarded 0.121 s (0.56x) | HEAD **0.209 s** / naive **7.774 s (37.2x)** / guarded **0.150 s (0.72x)** over 249 files, 114 493 lines, 7.44 MB | direction **exact**, constants moved (see below) |
| `bandit 1.9.4` present; scanner clean, exit 0 | 1.9.4; **exit 0** | **exact** |
| three presets, **none** selects `content-security` | three; none | **exact** |
| `dev/modules/` holds 18 files, no `content-security` mirror | 18; none | **exact** |
| shipped residual baseline comment-only, 0 fingerprints | 0 non-comment lines | **exact** |
| `_flag_fingerprint` at runner `:291` hashes `relpath:pattern_id:sha256(stripped line)` | verbatim at `:291-299`; the **message is not an input** | **exact** |
| `content_scan.py:401-403`, ternary verbatim at `:402`; HEAD homoglyph rule at `:357`; runner `:83` `_MAX_WALL_SECONDS = 120.0`; docstring `29-55` / `:40` / `:43` / `:46`; `content-security.md:138-144` and `:25-33`; `test_content_scan.py:47-52` (`0x00AD` **absent**) and `:81` | all verbatim at the cited lines | **exact** |
| `vermin` is not installed, so `test_python_floor.py` **skips gracefully** | **`vermin 1.8.0` is on PATH; the test runs and both cases PASS** | **DOES NOT REPRODUCE** |

**On the performance constants.** The naive-walk multiplier moved from **26.4x**
to **37.2x** — outside noise, and in the direction that *strengthens* [I6] rather
than weakening it. The corpus grew from 89 445 to 114 493 lines while the guard's
cost stayed flat, which is what a per-character table walk does and a
short-circuit does not. The plan already says "the interesting claim is the
direction and the guard, not the constant"; that instruction is correct and is
now evidenced twice over.

### 2. Re-measurement: the review's own figures

| the review states | live tree | verdict |
|---|---|---|
| collection **1749**; **235** `.md`; **453** `.md`/`.txt`/`.py` | **1790 / 249 / 469** | drifted further — the review's own point, proven again |
| `check_cairn` **180 / 68** exact; manifest **96** exact | **195 / 68**; **96** | manifest exact; Markdown count drifted |
| [I1]: six reviewer-built no-Latin multi-script tokens, HEAD **flag** -> rule **CLEAR**, 6 for 6 | **6 for 6**, every row identical | **exact** |
| [I2]: **20** non-seed Greek letters whose NFD base is a `_NO_LATIN_TWIN` member — `U+038F` plus 19 in Greek Extended (`U+1F68`-`U+1F6F`, `U+1FA8`-`U+1FAF`, `U+1FFA`-`U+1FFC`) | **20**; `U+038F` + **19** spanning `U+1F68`..`U+1FFC` | **exact** |
| [I2]: `U+038F`+`mega`, `U+1F68`+`mega`, `U+1FFB`+`mega` are flag -> CLEAR | all three | **exact** |
| [I3]: **217 of 218** Greek Extended letters decompose to >1 char; `ord(normalize("NFD", ...))` raises `TypeError` | **217/218**; `TypeError: ord() expected a character, but string of length 2 found` | **exact** |
| [I4]: dropping `U+03BC` leaves both decisive figures **identical** | 7 and 13/14 both unchanged | **exact** |
| [I4]: `U+03BC`+`ser` and `U+03BC`+`rl` are HEAD-clean; `U+03BC`+`pload` HEAD-flags | clean / clean / flags | **exact** |
| [I5]: seven seeded-letter families, HEAD **flag** -> rule **CLEAR** | 7 for 7 | **exact** |
| [I7]: the 9 covered-code-point lines are **all** in `.py`; **zero** tracked `.md` lines carry one | identical file:line list; **0** `.md` lines | **exact** |
| [I8]: **zero** lines carry `U+FE0F` | **0** | **exact** |
| [I9]: `tuple + list` raises | `TypeError: can only concatenate tuple (not "list") to tuple` | **exact** |
| fullwidth `U+FF21`-`U+FF5A`: **0** rows whose NFKC is not a single ASCII char | **0** of 58 | **exact** |
| `test_content_scan.py:81-87` tests four tokens, **all** carrying Latin | all four are `A`+X+`bc` | **exact** |
| `vermin` is **absent** (`No module named vermin`) so `test_python_floor.py` skips | the **import** fails; the **test passes** | premise reproduces, **consequence does not** |

**The review's measurements are, with one exception, exact.** Eighteen
independent re-runs, eighteen hits. That is unusually good and it is worth saying
before the dispositions, because every finding below inherits its credibility
from it.

### 3. Disposition

#### [I1] — **ACCEPTED, with the remedy corrected.** The finding is right; its remedy as worded reverts Change 2 entirely.

The hole is real and I reproduce it 6 for 6 with the shipped scanner. Clauses 2
and 3 both predicate on Latin being present; clause 1 covers all-Greek and
all-fullwidth. A token whose scripts are Cyrillic + Armenian, or Greek +
Cyrillic, with **zero** Latin characters, falls through all four gaps. HEAD flags
it (`content_scan.py:357`, `len(_token_scripts(token)) > 1`, script-blind); the
rule as the plan words it clears it. The Maintainer direction narrowed clause 1
to Greek-only and nothing was added to catch what the old script-general clause 1
and HEAD's rule used to catch between them. The review's three consequences all
hold: the plan's "Unchanged behaviour from HEAD" sentence is false, D12 cannot
detect it (all four of its tokens carry Latin, verified at `:81-87`), and the
specified falsifying sweep cannot find it because no token set in the record
contains a no-Latin multi-script token.

**But the remedy as the review words it does not work, and I measured it rather
than reasoning about it.** The review proposes *"two or more distinct confusable
scripts in one token always flags"* and asserts it "removes zero flags relative
to HEAD and costs no scientific notation":

```
                                        sciFP    [I1] kept   no-Latin caught
plan as written                          7/37      13/14           0/6
clause 0, non-Latin scripts only         7/37      13/14           6/6
clause 0, literal ("any two scripts")   37/37      14/14           6/6
```

The literal reading restores **all thirty-seven** scientific false positives —
it is HEAD's rule, and it deletes Change 2. The review's claimed properties hold
**only** under the non-Latin restriction, which the sentence does not say. This
is the same defect class as the review's own [I3]: a remedy whose most natural
reading breaks the thing it is repairing.

**Why the non-Latin form is genuinely free, measured rather than asserted:**
every one of the 37 published false-positive tokens carries **exactly one**
non-Latin script (`Counter({1: 37})`). A clause keyed on *two or more non-Latin
confusable scripts* therefore cannot touch any of them, by measurement of the
token set and not by intuition about scientific notation.

Residue: **AM-1** through **AM-5**.

**Maintainer strike-line.** Clause 0 adds a clause the Decision did not
enumerate, even though it restores only behaviour HEAD already has and removes
none. I classify it *within-contract* — a correction preserving accepted
behaviour, adding no surface. If the Maintainer instead reads it as scope, strike
AM-1 through AM-4 and the class becomes a **new** declared residual needing a
Decision; it is emphatically **not** the priced whole-script Cyrillic residual,
since `U+03C1` + Cyrillic `a,s,s` is neither whole-script nor Cyrillic.

#### [I2] — **ACCEPTED in full.** The number is 20, the branch is the other one, and the plan wrote down an answer it had not taken.

Reproduced exactly: 20 non-seed Greek letters fold onto a `_NO_LATIN_TWIN`
member — `U+038F`, `U+1F68`-`U+1F6F`, `U+1FA8`-`U+1FAF`, `U+1FFA`-`U+1FFC`. The
review is also right that the plan's measurement *question* is under-scoped: it
asks about "the 218 assigned Greek Extended letters" and `U+038F` is in Greek and
Coptic, so an honest answer to the question as asked would still have
under-counted by one.

I accept the sharper half without argument. The plan's own sentence is **"Do not
ship a mechanism described as a guard without a number saying what it guards"**
and the plan then supplied a predicted number in place of a measured one, in that
same paragraph. Under a denylist the fold **widens clearing**; the plan
identified that polarity inversion correctly and then reported the pre-inversion
answer. The conditional branch the plan pre-committed to ("if it is not zero, the
cleared set must be listed and put to the plan reviewer") is hereby **taken**:
the set is listed above and is now in the record.

Residue: **AM-6**.

#### [I3] — **ACCEPTED in full.** This is the finding with the worst failure mode and the cheapest fix.

Reproduced: 217 of 218 Greek Extended letters decompose to more than one
character, and `ord(unicodedata.normalize("NFD", ch))` raises `TypeError`. D1
offers "escapes **or** integer literals" and D2 says "NFD-fold, then test
non-membership" — between them they invite the int-set form, which raises on any
polytonic Greek. The failure scenario is exactly as stated: an adopter with a
classics repository, a quoted epigraph, or a Unicode fixture gets a **denial of
scan** in a fail-closed runner, triggered by legitimate content. And the review
is right that nothing in D4-D11 touches Greek Extended at all — every token in
those rows draws from `U+0370`-`U+03FF`.

Residue: **AM-7**, **AM-8**, **AM-9** (the new does-not-raise sweep over all 347
assigned letters — which also gives D10 the companion the review names: D10 pins
the table's *members*, nothing pinned the *function* against its domain).

#### [I4] — **ACCEPTED.** The seed is exempted from the plan's own admission rule, and `U+03BC` is unconstrained by every figure the plan uses.

Reproduced: dropping `U+03BC` from the seed leaves **both** decisive figures
bit-identical (7 residuals, 13/14 kept). The plan's two measurements do not
touch it — the micro tokens in the 42-set are `U+00B5` MICRO SIGN, not `U+03BC` —
so the one seeded letter with the most arguable ASCII twin (`u`) is the one no
measurement in this plan constrains. The structural point is the stronger one:
the admission rule governs only what is admitted *beyond* the seed, so it binds
`U+03D1`/`U+03D5`/`U+03D6` (which clear nothing in any published figure) and
correctly refuses `U+03F2`, while the nine letters that do **all** the clearing
are admitted by inheritance from the artifact the plan itself says failed twice.

The reviewer's adjacent note also reproduces: `U+03BC`+`ser` and `U+03BC`+`rl`
are HEAD-clean (RV5 already clears them), so `U+03BC`'s real new exposure is
longer tokens such as `U+03BC`+`pload`, which HEAD flags and the rule clears.
That belongs in the module doc, and AM-10 puts it there.

Residue: **AM-10**.

#### [I5] — **ACCEPTED.** The claim is stronger than the evidence, and the fix is to write the checkable sentence.

Reproduced 7 for 7. I want to be precise about what I am conceding, because the
plan's underlying judgment is not what is wrong. I still think most of
`U+0394`/`U+03BB`/`U+03C6`/`U+03A9` are weak spoofs and the review says it agrees.
What is wrong is the **form** of the claim: "the falsifying criterion no longer
fires" is a statement about the world, and it is true only if you first accept
the ASCII-twin judgment as settled — which *Known omissions* (d) already concedes
is "unattested to any external oracle". A security control should not carry a
claim whose truth depends on the reader granting the very judgment under review.
The review's replacement sentence is checkable and mine is not, so I take it.

Residue: **AM-11**.

#### [I6] — **ACCEPTED.** The channel note claims independence the selection step destroyed.

This one I should have caught myself, because the plan half-says it: "it does not
convert it into 'the table covers its domain', which is not [a test]" — and then
the channel note takes it back by calling the published figures an independent
oracle. They are not independent of the seed: the seed was **chosen because** it
reproduces 7/42. D9 is a genuine **drift** guard (P-D1's "add `U+03B3`, watch the
seven become six" is a correct hazard-side perturbation and I keep it), but it
cannot fail for the seed as selected. Both the channel note and the
*Author-accounting* invariant get restated as drift.

Residue: **AM-12**.

#### [I7] — **ACCEPTED, and it understates itself. The tripwire is null for Change 2 too.**

The review's Change 1 half reproduces exactly: `check_cairn` scans tracked
Markdown only (`scripts/check_cairn.py:50` says so, `:182` runs the `git ls-files
'*.md'`, `:393` composes `content_scan.scan_file`), and **zero** tracked `.md`
lines carry any code point in the ignorable-union-noncharacter set — all nine
live in `.py` files. Change 1 therefore adds zero `check_cairn` flags whether the
detector is correct or broken.

**What the review did not check, and I did.** I ran the file-by-file
`(pattern_id, line)` comparison the plan specifies, over all 249 tracked `.md`,
through `scan_file` (so suppressions apply), with `_scan_homoglyph` swapped for
my reconstruction of the plan's rule:

```
post-suppression flags over tracked .md   BEFORE: 77   AFTER: 77
flags REMOVED: 0    flags ADDED: 0    files whose flag set changes: 0
post-suppression `homoglyph` flags across all 249 tracked .md : 0
```

The "0 files change" prediction reproduces — but for a reason that voids it as
evidence. There are **zero** unsuppressed `homoglyph` flags in the entire tracked
Markdown tree. The one file that carries any is the source proposal itself: 73
raw homoglyph lines, **all** silenced by its 23 block-scoped `cairn-accept:
homoglyph` markers. Pre-suppression, my reconstruction moves 26 lines cleared and
16 added in that file — and every one of them is inside a suppression block the
proposal wrote about itself.

**This is the recurring failure of this cycle in its purest form: the artifact
under verification is the only file supplying the material the check runs on, and
it has suppressed itself.** The plan cites the flag-count tripwire twice as a
signal-the-change-is-wrong guard. It is structurally incapable of moving for
either change. Calling that "at full strength again" is precisely the kind of
sentence this plan exists to prevent, and the review was right to name it — it
was simply right about half of it.

Residue: **AM-13**, **AM-14**.

#### [I8] — **ACCEPTED with modification.** The bias is real; the "one emoji-bearing corpus outside this repository" is not a measurement I can bound.

Reproduced: **zero** lines carry `U+FE0F` across 469 tracked files. The review is
right that this is the house emoji rule showing up in the data rather than
evidence about the world, that `unicode-ignorable` fires on `U+FE0F`, and that
the adopter-facing accounting is one-sided — E5's `Changed` line covers Change 2's
clearing direction (`STALE` at exit 3) while Change 1's **adding** direction
appears nowhere.

I accept the asymmetry and the changelog fix without reservation. I **modify**
the measurement ask. "Measure `U+FE0F` density on one emoji-bearing corpus
outside this repository" has no defensible sampling frame — one arbitrary
repository's emoji rate is not a number an adopter can use, and quoting it in a
changelog would be a figure with a false precision, which is the failure mode
this whole lifecycle is about. What is both measurable and *decision-relevant* is
the **shape**: `unicode-ignorable` fires once per line per category, so the
upgrade cost is bounded by *emoji-bearing lines*, not emoji. AM-15 requires the
per-line bound to be stated as a rule with a worked example, and the `Added`
changelog line to carry the same upgrade-consequence sentence the `Changed` line
gets. If the Maintainer wants a density figure with a named corpus and a stated
frame, that is a one-line instruction and I will take it.

Residue: **AM-15**.

#### [I9] — **ACCEPTED in full.** Both halves.

`tuple + list` raises, confirmed. And the substantive half is the one that
matters: B10 as specified compares the table minimum against a hard-coded
`0x00AD`, so it pins "the table never drops below `U+00AD`" and **not** the
invariant *Author-accounting* names it as enforcing. A future author who raises
the guard constant leaves B10 green. Asserting against the module's own constant
makes the coupling real.

Residue: **AM-16**.

#### Carried figures — **ACCEPTED.** And the drift is now larger than the review found.

The review measured 1749 against the plan's 1746; the live tree is at **1790**.
Tracked `.md` has gone 234 -> 235 -> **249**. The plan says "Re-measure, do not
carry" and then hands an implementing agent a constant to compute a delta
against. AM-17 makes the baseline a **procedure**.

#### On the two things the plan invited a reviewer to strike

* **C4's `_BANNED_CODEPOINTS` widening** — the review declines to strike it and I
  agree. `0x00AD` is verifiably **absent** from the set at
  `test_content_scan.py:47-52`, so P-C3's green-at-HEAD / red-after-C4 pair is
  real and the widening closes a live gap at no cost. **Kept, unchanged.**
* **The case-exact reading of `_NO_LATIN_TWIN`** — the review confirms the
  arithmetic (7 residuals and 13/14 both reproduce exactly here too) and declines
  to strike the *reading*. **Kept.** The strike-line in *Chunk D* stays live for
  the Maintainer; what [I4] and [I5] establish is that the reading is
  well-evidenced while the **seed's** ASCII-twin judgment is not, and AM-10 and
  AM-11 make the plan say so in both places.

### 4. Two things the re-measurement forced, that the review did not raise

#### [A1] The `vermin` fence rests on a false premise. The plan asserted it, the review confirmed it with the wrong oracle, and the test has been passing the whole time.

The plan says `vermin` "is not installed in this environment" and that
`test_python_floor.py` "**skips gracefully**". The review confirms it: "`vermin`
is **absent** (`No module named vermin`) so `test_python_floor.py` skips."

Both premises come from an **import probe**. That is not what the test checks:

```
bootstrap/tests/test_python_floor.py  _vermin_cmd()
    subprocess.run(["vermin", "--version"], ...)          # the binary on PATH
    shutil.which("vermin", path=<interpreter dir>)        # then interpreter-adjacent
```

`import vermin` fails because `vermin` installs as a **standalone executable, not
an importable module** — the test's own docstring says so in terms. Followed to
the call path rather than to the first check that supports the claim:

```
$ which vermin      -> /Users/kendal30/conda_envs/miniforge3/bin/vermin
$ vermin --version  -> 1.8.0
$ python -m pytest bootstrap/tests/test_python_floor.py -v
  TestPythonFloor::test_engine_floor_does_not_exceed_declared_minimum PASSED
  TestPythonFloor::test_engine_floor_is_at_least_3_7                  PASSED
  2 passed
```

**It does not skip. It passes.** This is the round's stated failure mode with the
roles reversed: *follow the call path, not the first function that supports the
claim.* I asserted the skip; the reviewer probed the artifact I named rather than
the trigger that governs, and confirmed it.

**And the conclusion survives anyway, for a better reason.**
`test_python_floor.py` scopes to `ENGINE_DIR = bootstrap/_scaffold` — the scaffold
engine, **not** `templates/modules/team-gated/content_scan.py`. So even with
`vermin` present and both cases green, that test verifies nothing about the file
this plan edits. Installing the dev dependency, which is the remedy the plan's
fence names, would have discharged **nothing**.

The correct check is a **scoped `vermin` run over the edited file**, which is
dischargeable in-session and which I have taken a pre-change baseline for:

```
$ vermin --backport dataclasses --backport typing \
      templates/modules/team-gated/content_scan.py
  Minimum required versions: 3.7
  Incompatible versions:     2.x
```

`3.7`, well under the declared `>= 3.11` floor. So *The Maintainer fence* item 2
is **retired** — the obligation moves back to the implementing agent as a scoped
run against a stated baseline, not up to the Maintainer as an uninstallable
dependency. Residue: **AM-18**.

#### [A2] The `check_cairn` tripwire is null for Change 2 as well

Stated under [I7] above; it is listed separately here because it is an author
finding against the author's own plan, not a disposition of a reviewer's, and
because it is the one place where the plan's central self-verification story is
load-free in both halves rather than one. Residue: **AM-14**.

### 5. Amendments in force

Append-only: the rows below **supersede** the quoted text without editing it. An
implementing agent reads the plan **through** this table.

| # | Superseded text (verbatim) | Replaced by |
|---|---|---|
| **AM-1** | Chunk D: `**The three clauses. A token flags when any holds:**` | `**The four clauses. A token flags when any holds:**`, with a new **clause 0** inserted first: *"**Two or more distinct non-Latin confusable scripts in one token always flags.** Latin is excluded from the count; the clause is HEAD's script-blind rule restricted to the no-Latin case, so it removes no flag HEAD has and adds none. Measured free: all 37 published scientific false positives carry exactly one non-Latin script."* Clauses 1-3 keep their numbering and text, evaluated after clause 0. |
| **AM-2** | Chunk D, clause 2: `2. **Non-Greek confusable script mixed with Latin always flags.** Cyrillic,` / `   Armenian, Cherokee, Coptic, fullwidth. Unchanged behaviour from HEAD.` | Same first sentence; the second becomes: *"Cyrillic, Armenian, Cherokee, Coptic, fullwidth. **Unchanged behaviour from HEAD for any token containing a Latin character**; the no-Latin case is clause 0's, and without clause 0 this sentence is false."* |
| **AM-3** | Chunk D row **D3** (`_scan_homoglyph` rewritten to the three clauses) | `_scan_homoglyph` rewritten to the **four** clauses. Clause 0 is evaluated first and its comment states the measured zero-cost basis (37/37 tokens carry one non-Latin script). Clause 1's comment and code still say **"for Greek"**; the fullwidth arm stays separate; the Cyrillic-residual comment is unchanged. |
| **AM-4** | Chunk D row **D5** (`test_spoofs_still_flag`) | Gains a `test_no_latin_multi_script_flags` case carrying the six reviewer-built tokens (Cyrillic+Armenian "session", Armenian+Cyrillic "ronin", Cyrillic+Coptic+Armenian, `U+03C1`+Cyrillic "pass", Cyrillic+Armenian "admin", Cyrillic+Greek "open"), all written as `\uXXXX` escapes, each asserted **flagged**. Their provenance — *built by the plan reviewer, present in no set in the record* — is recorded in the docstring. |
| **AM-5** | Chunk D acceptance, `**The falsifying sweep must be RUN, not reasoned.**` bullet | Unchanged in its demand, prefaced by: *"**The record's token sets cannot find the no-Latin multi-script class — no set in the record contains such a token, so the sweep's answer is fixed by construction.** Widen the sweep with the six reviewer-built tokens above plus at least six more built at implementation time, before treating any sweep result as evidence."* New perturbation **P-D7, RUN**: delete clause 0; confirm the new D5 case goes RED and D4's scientific set stays green. |
| **AM-6** | Chunk D acceptance: `Under the case-exact seed, **no** precomposed or` / `Greek Extended form appears to fold onto a seeded base, which would make the` / `folding inert.` | **Measured, not predicted: the number is 20.** `U+038F` (Greek and Coptic — a block the original question did not even scope), `U+1F68`-`U+1F6F` (8), `U+1FA8`-`U+1FAF` (8), `U+1FFA`-`U+1FFC` (3). All are capital-omega variants; `U+038F`+`mega`, `U+1F68`+`mega` and `U+1FFB`+`mega` are flag-at-HEAD -> cleared-by-the-rule. The plan's own conditional ("if it is not zero, the cleared set must be listed and put to the plan reviewer") is **discharged** by this Response. The code comment beside the fold must carry **20** and the listed set, and the module doc must state that the fold widens clearing under a denylist. |
| **AM-7** | Chunk D row **D1**: `` `_NO_LATIN_TWIN`, a `frozenset` of Greek code points **written as `\uXXXX` escapes or integer literals** `` | `` `_NO_LATIN_TWIN`, a `frozenset` of **single-character `str` members written as `\uXXXX` escapes. Integer literals are forbidden** — the int form invites `ord(normalize("NFD", ch))`, which raises on 217 of the 218 Greek Extended letters. `` |
| **AM-8** | Chunk D row **D2**: `` `_is_confusable_greek(ch)` — NFD-fold, then test non-membership in `_NO_LATIN_TWIN`. `` | `` `_is_confusable_greek(ch)` — take `unicodedata.normalize("NFD", ch)[0]` (**the arity is pinned: NFD of a Greek Extended letter is a multi-character string**), then test non-membership in `_NO_LATIN_TWIN`. `` |
| **AM-9** | *(new row)* | **D13** — `test_scan_text_survives_every_greek_letter`: `scan_text` **does not raise** across all **347** assigned letters in the two Greek `_SCRIPT_RANGES` rows (`U+0370`-`U+03FF`, `U+1F00`-`U+1FFF`), each in a token with a Latin neighbour and alone. New perturbation **P-D8, RUN**: replace the pinned `[0]` with the bare `normalize(...)` inside `ord(...)`; confirm D13 goes RED with `TypeError`. D10 pins the table's members; D13 pins the function against its domain. |
| **AM-10** | Chunk D row **D1** (the seed's admission) | Additionally: the **nine seeded letters each carry their own per-code-point justification comment**, under the same rule the plan applies to the three admitted variants — inheritance from the base proposal is no longer sufficient. Each comment states whether the letter is **pinned by a published figure** (`U+0394`, `U+03BB`, `U+03C3`, `U+03B8`, `U+03C6`, `U+03C8`, `U+03B2`, `U+03A9` — these move the residual count) or **figure-unconstrained** (`U+03BC` — dropping it leaves both decisive figures bit-identical; the 42-set's micro tokens are `U+00B5` MICRO SIGN, not `U+03BC`). The module doc records that RV5 already clears short micro-prefixed tokens at HEAD, so `U+03BC`'s new exposure is longer tokens such as `U+03BC`+`pload`. |
| **AM-11** | Chunk D: `So the proposal's own falsifying criterion (*"a spoof that HEAD catches and the` / `patch clears, other than the named two-character shape"*) **no longer fires**.` | *"So the proposal's own falsifying criterion fires only on a class the plan can name: **no spoof HEAD catches is cleared except the two-character shape and the seven seeded-letter families (`U+0394`, `U+03BB`, `U+03C6`, `U+03A9`, `U+03B2` x2, `U+03BC`), whose ASCII-twin status is asserted by judgment and unattested to any external oracle.** That sentence is checkable; 'no longer fires' was not."* |
| **AM-12** | Chunk D channel note: `` D9's oracle is the `` / `` proposal's own **published figures**, an artifact written before the `` / `` implementation existed. `` | *"D9 is a **drift** guard, not an independence check. The case-exact seed was selected **because** it reproduces the published residual count, so D9 cannot fail for the seed as selected; it fails when the table drifts from what the module doc publishes, which is what P-D1 perturbs and what it is worth having."* The *Author-accounting* invariant `` *`_NO_LATIN_TWIN` agrees with the figures the module doc publishes.* `` is read as a consistency check between two descriptions of one judgment, never as a check that the judgment is right. |
| **AM-13** | Chunk B acceptance: `* `python scripts/check_cairn.py` → **flag count unchanged**. The predicted delta` ... `is at full strength again now that the `+2` exposure has been repaired.` | *"`python scripts/check_cairn.py` -> flag count unchanged. **This check is structurally incapable of moving for Change 1**: `check_cairn` scans tracked Markdown only (`scripts/check_cairn.py:50`, `:182`, `:393`) and **zero** tracked `.md` lines carry any covered code point — all nine live in `.py` files. It is a guard against someone planting a raw code point in Markdown, **not** a verification of this change. Run it, expect no movement, and do **not** cite it as evidence the detector is correct."* |
| **AM-14** | *Verification*: `* **The corpus tripwire, at full strength.**` bullet, and the `* **The file-by-file flag-set comparison**` bullet's `Predicted: **0 files change**.` | *"**The corpus tripwire is null for both changes, and this is the plan's own recurring-failure class.** Change 1: zero tracked `.md` lines carry a covered code point. Change 2: there are **zero unsuppressed `homoglyph` flags in the entire tracked Markdown tree** — the only file carrying any is the source proposal (73 raw lines, all silenced by its own 23 block-scoped `cairn-accept: homoglyph` markers), so a measured 0-removed / 0-added over 249 files is an artifact of the proposal having suppressed itself. **The artifact under verification is supplying the material the check runs on.** The informative run is the `.py`/`.txt` half plus a purpose-built corpus that actually contains the newly-covered code points and no-Latin multi-script tokens; build it at implementation and state its provenance."* |
| **AM-15** | Chunk E row **E5**, and the Chunk E `**Adopter-upgrade consequence**` bullet | The `Added` changelog line gains its own upgrade-consequence sentence, symmetric with `Changed`: *"`unicode-ignorable` fires on variation selectors, so a previously-clean adopter tree containing emoji gains flags on upgrade."* The bound is stated as a **rule, not a density figure**: one flag **per line per category**, so the cost is bounded by emoji-bearing *lines*, with a worked example in `content-security.md`. Cairn's own corpus is named as **unusable evidence** here — zero `U+FE0F` across 469 tracked files is the house emoji rule, not a fact about adopters. *(A density figure against a named external corpus with a stated sampling frame is a Maintainer call, not this plan's to invent.)* |
| **AM-16** | Chunk B row **B10**: `` assert `min(lo for lo, _ in _IGNORABLE_RANGES + _NONCHARACTER_RANGES + [_TAG_RANGE]) >= 0x00AD` `` | `` assert `min(lo for lo, _ in (*_IGNORABLE_RANGES, *_NONCHARACTER_RANGES, _TAG_RANGE)) >= ord(_ASCII_GUARD)` `` — the tuple/list concatenation raises `TypeError` as written, and the bound must be **the module's own guard constant**, not a hard-coded `0x00AD`, or a future author who raises the guard leaves B10 green. **P-B5** additionally raises the guard constant (leaving the tables alone) and confirms B10 goes RED. |
| **AM-17** | *Acceptance criteria*: `canonical interpreter (3.13.13) with `PYTHONDONTWRITEBYTECODE=1`. Collection` / `baseline **1746 nodes `as_of 2026-08-04`**; it grows by exactly the new nodes` / `and drops none.` | *"Collection baseline is a **procedure, not a constant**: capture `python -m pytest bootstrap/tests --collect-only -q` immediately before the first chunk and record it in the first commit body; the final count must exceed it by exactly the new nodes and drop none. The plan's 1746 was 1749 within hours and is **1790** as of this Response — do not compute a delta against any number written in this file."* |
| **AM-18** | *Gate accounting*: `* **`vermin` is not installed in this environment**, so` ... `open and is fenced below rather than reasoned away.` — together with *The Maintainer fence* item **2**, the *Verification* bullet `* **The Python floor** — ... **It currently skips**: `vermin` is not installed at the canonical interpreter,` , *Known omissions* **(b)**, and the *Lasting-truth migration* row `The unrun `vermin` >= 3.11 floor verification` | **All five superseded; the fence item is retired.** `vermin 1.8.0` **is** on PATH (`/Users/kendal30/conda_envs/miniforge3/bin/vermin`); `test_python_floor.py` **passes**, it does not skip — the `import vermin` probe both the plan and the review used is not the trigger the test consults (`_vermin_cmd()` shells the binary). Separately, that test scopes to `bootstrap/_scaffold/` and so verifies **nothing** about the edited file either way. The obligation returns to the **implementing agent** as a scoped run — `vermin --backport dataclasses --backport typing templates/modules/team-gated/content_scan.py`, pre-change baseline **`Minimum required versions: 3.7`** measured for this Response — recorded in the Chunk B commit body. The *Lasting-truth* row is replaced by: *"Discharged in-session by the scoped run; no Maintainer action."* |

### 6. Does this Response clear the plan to implement?

**No. The plan is not cleared, and this Response does not clear it.**

* **The declared tier is `required(External, security lens)` and it is
  undischarged.** The Internal round said so; this Response says so; nothing has
  changed that. An author's Response to a same-type review is the weakest
  possible instrument for a tier that exists precisely because author and
  same-type reviewer share blind spots — and this round is the demonstration: I
  wrote the plan, an Internal round found nine things, and re-measuring for this
  Response found a tenth ([A1]) that **both of us had asserted incorrectly, from
  the same wrong probe**. That is what structural non-independence looks like
  from the inside.
* **The three named pre-implementation blockers are addressed in the plan text,
  not resolved in code.** [I1], [I2] and [I3] now have amendments; an amendment
  is a specification, and a specification is what the External round exists to
  attack. [I1] in particular is the falsifying criterion firing for the **third**
  time in this lifecycle, and its remedy needed correcting on first contact with
  measurement — which is not a reason to trust the corrected remedy more.
* **What the External round should now aim at**, revised from the brief in light
  of this round:
  1. **Clause 0 is a new sentence in a security control and has never been
     reviewed by anyone but its author.** Attack it. Build no-Latin
     multi-script tokens I have not seen; check the non-Latin restriction is
     correct rather than merely convenient; check it does not resurrect the
     scientific false positives under some token shape the 37-token set lacks.
  2. **The seed's ASCII-twin judgment remains the plan's largest unattested
     surface** ([I4], [I5]) and no same-type reviewer — author or Internal — is
     the right instrument. This is question 1 of the original brief, unchanged
     and un-discharged.
  3. **Every corpus-based self-check in this plan is now known to be
     structurally null** ([I7], [A2]). Any evidence the External round accepts
     must come from a corpus built for the purpose, with stated provenance —
     not from Cairn's tree, and not from the proposal's token sets.
  4. Questions 2, 3 and 4 of the original brief stand as written.
* **Still open and unowned:** `dev/PLANNING.md` carries **no row** for this plan
  (checked), so *Sequence* step 0's row-move has not landed. That file is a
  serialized shared file and is not this Response's to edit; it is raised in the
  handoff.

**Tier status, stated plainly so no one can read discharge into this section:**
Internal plan review — **landed** (floor, not the tier). Author Response —
**this section**. External plan review, security lens — **OWED**. Code review —
not yet due. **No implementation commit lands until the External section is in
the tree.**

### Figure correction -- Claude -- 2026-08-04

**What this is.** An audit of the Response above reported that two figures it
states as measurements do not reproduce, one of them written into a binding
amendment. This section is a **third, independent measurement**: I took no
number from the Response and no number from the audit, and recomputed both from
the shipped scanner over a corpus read out of a named git tree object. **No
disposition moves.** Nothing here accepts, declines, re-opens or withdraws a
finding. Both figures are corrected; both amendments that carry one keep their
conclusions, for reasons re-derived below rather than inherited.

**Provenance.** Canonical interpreter `~/conda_envs/lhm/bin/python3.13`
(CPython 3.13.13), `PYTHONDONTWRITEBYTECODE=1`, `as_of 2026-08-04`. Run at HEAD
`d01ed4f`. The corpus is read with `git show <commit>:<path>`, which reads the
committed tree and never the working copy, so concurrent sibling activity in the
tree cannot reach these numbers. **Scanner drift cannot explain any difference
here**: `git diff --stat e20b18e HEAD -- templates/modules/team-gated/content_scan.py
templates/modules/team-gated/content_scan_allowlist.txt` is empty, and
`git status --short templates/modules/team-gated/` is clean.

#### 1. `BEFORE: 77   AFTER: 77` — the [I7] tripwire baseline (line 1980)

| | figure |
|---|---|
| Response | **77 / 77** |
| Audit | 89 |
| **This measurement** | **89 / 89** |

Measured by importing `scan_text` from the shipped
`templates/modules/team-gated/content_scan.py` and running it with its
documented defaults (`scan_urls=True`) over every tracked `.md` blob at
`e20b18e` — the Response's own stated measurement commit:

* tracked `.md` at `e20b18e`: **249** — the Response's 249 is correct
* post-suppression flags: **89**, of which `suspicious-url` **89**
* the same measurement at HEAD `d01ed4f` (252 tracked `.md`): **89**

**Where the 77 came from.** The shortfall is not noise. Exactly one file,
`dev/proposals/2026-08-03-codex-api-web-security-modules.md`, contributes
**12** flags, and 89 − 12 = **77** exactly. The Response's corpus was its own
corpus minus that single file — consistent with a harness that dropped a file,
and the stated figure is reproducible the moment that file is excluded.

**AM-14 stays IN FORCE. Its conclusion did not depend on this figure.** What the
baseline supports is a *delta* (`0 removed / 0 added / 0 files change`), and a
delta is invariant to the baseline it is measured against. Two independent
measurements confirm the delta holds:

* post-suppression `homoglyph` flags across tracked `.md` = **0**, at both
  `e20b18e` and HEAD. This is the load-bearing claim of `[A2]`, and it
  reproduces exactly.
* with `scan_urls=False` the same corpus yields **0** flags in total — so all 89
  are `suspicious-url`, a detector neither change touches. The tripwire is
  therefore *structurally* unable to move, which states the finding's own point
  more strongly than the figure did.

The baseline is corrected to 89; the finding it was offered in support of is
unchanged.

#### 2. "the only file carrying any is the source proposal (73 raw lines)" — AM-14 (line 2141)

| | figure |
|---|---|
| Response | **one** file, 73 raw lines |
| Audit | 3 files, 76 lines |
| **This measurement** | **3 files, 76 raw lines** |

Raw (pre-suppression) homoglyph lines, from `_scan_homoglyph` called directly on
each tracked `.md` blob at `e20b18e`. That generator breaks after the first
mixed-script token on a line, so one raw flag *is* one raw line:

| file | raw homoglyph lines |
|---|---|
| `dev/proposals/2026-08-03-claude-content-scan-detectors.md` | **73** |
| `dev/proposals/2026-08-03-claude-identity-not-name.md` | **2** |
| `dev/plans/archive/byline-classification.md` | **1** |

The **73** is exact; the count of *files* is not. The source proposal's **23**
block-scoped `cairn-accept: homoglyph` markers also reproduce exactly. Identical
at HEAD, so this is not drift.

**AM-14 stays IN FORCE with the figure corrected — its conclusion is
strengthened, not weakened.** The amendment's claim is that the corpus tripwire
is null because the artifact under verification is itself supplying the material
the check runs on, and has suppressed itself. All 76 raw lines, across all three
files, are suppressed — post-suppression `homoglyph` is 0 tree-wide. Self-
suppression is thus **broader** than the amendment states and the inference from
it is untouched. The single word that must change is "only": three files carry
raw homoglyph lines, not one.

**Neither amendment is withdrawn.** Of the two categories — a conclusion that
survives a wrong figure, versus a conclusion that depended on it — **both of
these are the first kind**. Neither `[A2]`'s delta claim nor AM-14's
self-suppression argument rests on the corrected numbers, and I re-derived each
rather than taking the audit's word that the conclusions survive.

#### One correction to the audit

The audit lists the third homoglyph-bearing file under its **pre-archive**
location — the `byline-classification` plan directly under `dev/plans/`. That
location no longer resolves: the plan was archived mid-session, and the file is
now `dev/plans/archive/byline-classification.md`. Same file, same single raw
line — only the audit's path is stale. (Stated this way deliberately: writing
the dead path as a citation would itself be a broken-path claim, which is what
`scripts/claim_check.py` exists to catch.)

#### The command

Both figures come from one run, at repository root:

```
python - <<'PY'
import importlib.util, subprocess, sys, collections
spec = importlib.util.spec_from_file_location(
    "content_scan", "templates/modules/team-gated/content_scan.py")
cs = importlib.util.module_from_spec(spec)
sys.modules["content_scan"] = cs
spec.loader.exec_module(cs)
REV = "e20b18e"
files = [p for p in subprocess.run(
    ["git", "ls-tree", "-r", "--name-only", REV],
    capture_output=True, text=True, check=True).stdout.splitlines()
    if p.endswith(".md")]
flags = collections.Counter(); raw = {}
for rel in files:
    t = subprocess.run(["git", "show", f"{REV}:{rel}"],
                       capture_output=True, check=True
                       ).stdout.decode("utf-8", "replace")
    for f in cs.scan_text(t):          # defaults: scan_urls=True
        flags[f.pattern_id] += 1
    n = sum(1 for _ in cs._scan_homoglyph(t.split("\n")))
    if n:
        raw[rel] = n
print(len(files), sum(flags.values()), dict(flags))
print(len(raw), sum(raw.values()), raw)
PY
```

**Tier status is unchanged by this section.** External plan review, security
lens, remains **OWED**. A figure correction to an author Response discharges
nothing.

This section is append-only once written.
