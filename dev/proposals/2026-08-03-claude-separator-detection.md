<!-- cairn-internal-ref-allow: doctrine/runtime-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# The two separators nothing detects — `U+2028` / `U+2029` fall between three proposals

**Author**: Claude (Strategy)
**Model**: Claude Opus 5.
**Date opened**: 2026-08-03
**Status**: reviewed
**Touches**: `templates/modules/team-gated/content_scan.py` (one detector rule)
and `bootstrap/tests/test_content_scan.py`. Nothing else.
**Related**: `planner-line-semantics` (delegates detection here — this proposal
exists to discharge the condition on its Decision); `content-scan-detectors`
(the sibling scanner scope, which excludes these two **by construction**);
`agent-context-scrub` (escapes them on the *output* side, and is not a
substitute).
**Plan review**: `required(**External**, security lens)` — the content scanner
is a shipped security control and its pattern-id set is an adopter-facing
contract.

## Context

This proposal exists because a Decision was conditioned on it.
`planner-line-semantics` fixes the *parser* — after it, a `U+2028`-glued
section header is no longer recognized as a heading by the planner — and it
explicitly delegates **active detection** of the injected separator to
`content_scan`. Its External reviewer accepted that delegation, and the
author's Response then measured it and found the delegation **sound but
unhomed**.

### The measurement

Run this session on the canonical interpreter (Python 3.13.13, UCD 15.1.0)
against the shipped scanner, loaded by path. Dated snapshot: 2026-08-03.

A Markdown fixture carrying a raw `U+2028` inside a status line and a raw
`U+2029` inside a paragraph produces:

```
U+2028/U+2029 fixture -> flags: 0 (NONE)
  U+2028 category=Zl White_Space=True
  U+2029 category=Zp White_Space=True
```

**Zero flags.** And the sibling scope does not close it:
`grep -c "2028\|2029"` over
`dev/proposals/2026-08-03-claude-content-scan-detectors.md` returns **0**.

### Why the sibling cannot close it, even fully landed

This is the part that matters, because it is structural rather than an
oversight. `content-scan-detectors`' Change 1 adopts the PRECIS
`PrecisIgnorableProperties` set from RFC 8264 §9.13 —
`Default_Ignorable_Code_Point` union `Noncharacter_Code_Point`. Both
separators are **excluded from that set by construction**:

* `U+2028` is general category `Zl`, `U+2029` is `Zp`;
* both carry `White_Space=Yes`, and the `Default_Ignorable_Code_Point`
  derivation **subtracts** `White_Space`;
* neither is a noncharacter.

The proposal's own completeness invariant is additionally quantified over
`Cf`-category code points, which excludes them a second way. The Maintainer's
2026-08-03 direction on that proposal — clause 1 held to Greek-only, fullwidth
closed separately, the Tag block given its own pattern id — lands entirely
inside Change 2 and the pattern-id partition, and adds no separator coverage.

So: **after `planner-line-semantics` and `content-scan-detectors` both land as
directed, a raw `U+2028` in a tracked Markdown file is still invisible.**

### Why `agent-context-scrub` is not the answer either

`agent-context-scrub` escapes `U+2028` / `U+2029` in the orientation stream.
That is the **output** side — it renders a separator inert *after* an agent
has already read the file. It does not tell anyone the separator is there, and
it does not cover a human reading the artifact, a diff, or a review. Detection
and neutralization are different controls; this proposal is the detection half.

## Proposed paths

None. Both files exist.

## Proposal

**One detector rule, one new pattern id.**

Flag a raw `U+2028` (LINE SEPARATOR) or `U+2029` (PARAGRAPH SEPARATOR) in
scanned text under a new pattern id — proposed `unicode-line-separator` —
distinct from `unicode-zero-width`, `unicode-bidi` and whatever id
`content-scan-detectors` lands for the ignorable set.

**A separate id, for the reason the Maintainer already accepted once.** The
2026-08-03 direction gave the Tag block its own id precisely so a
`cairn-accept` marker written for a benign case could not silence a
high-severity one. The same argument applies here: these separators have a
legitimate use (they are real Unicode line-breaking characters), so markers
*will* be written, and a shared id would let one silence an injected header.

**Flag, never rewrite.** Consistent with the module's existing posture: a hit
is a tripwire that forces human review, not a proof of compromise, and the
scanner never edits the file it scans.

### What this deliberately does not do

* **It does not change the parser.** `splitlines()` semantics and the planner's
  line grammar belong to `planner-line-semantics`.
* **It does not change the escaping.** The orientation-stream escape table
  belongs to `agent-context-scrub`.
* **It does not touch the ignorable or homoglyph rules.** Those are
  `content-scan-detectors`, which is mid-lifecycle; this proposal adds a rule
  beside them and edits neither.
* **It does not sweep the wider `Z*` space.** `Zs` (space separators) is a
  different question with a real international-name cost, already live as a
  Maintainer question on `byline-classification`. `Zl`/`Zp` carry no such cost
  — they are two code points, neither appears in any legitimate name, and
  neither should appear raw in a Markdown artifact at all.

## Rationale

The gap is not that anyone was careless. Three proposals each touch these two
code points from a different angle — one parses them, one escapes them, one
enumerates a *different* set that provably excludes them — and each reasonably
assumed another owned detection. That is a coordination failure of exactly the
kind Cairn's lifecycle is supposed to surface, and it was surfaced: by an
author Response measuring a delegation instead of asserting it.

The cost is one rule and one test node. The alternative is shipping a
documented delegation to a control that does not exist.

## Alternatives considered

**Fold it into `content-scan-detectors`.** Rejected: that proposal is mid-
lifecycle with a Response, Maintainer direction, and an author recommendation
to split Change 2 already on the record. Adding a third change to it now would
widen a scope whose central problem is that its curated sets have failed
reconciliation three times.

**Extend the ignorable set to include `Zl`/`Zp`.** Rejected: the set's value is
that it is *adopted*, not curated — RFC 8264 §9.13 decided its membership, and
Cairn's claim to completeness rests on not editing it. Adding two code points
by hand would forfeit exactly the property that makes Change 1 defensible.

**Do nothing; rely on the parser fix.** Rejected: it is the reason the Decision
was conditioned. The parser fix makes the planner immune; it leaves every human
reader, reviewer and diff blind.

## Evidence / verification plan

### Author-accounting — invariants, failure modes, edge cases

**Invariant.** A raw `U+2028` or `U+2029` anywhere in a scanned file produces
at least one flag naming the code point, and the flag is suppressible only by
a marker written against its own pattern id.

**Failure modes.**

* *Alarm fatigue.* If any legitimate tracked file already carries these, the
  rule ships noisy. **Measure before landing**, the way the fresh-scaffold
  count was measured for `default-security-stance` — a non-trivial count is a
  signal to reconsider, not something to suppress.
* *Marker collision.* A shared id would let a benign suppression silence an
  injected header — the defect the separate id exists to prevent, and it needs
  a test, not a convention.
* *Same-line masking.* The existing `_scan_unicode` breaks after the first hit
  per line per family, so two separators on one line report once. Whether that
  matters here is an open question this proposal flags rather than settles;
  `content-scan-detectors` [I3] is disposing the same behaviour for its own
  rules and its resolution should be followed rather than duplicated.

**Edge case worth naming.** These characters are *legal* line breaks in some
producers. An adopter pasting from a word processor can introduce one
innocently. That is precisely the tripwire's purpose — and precisely why the
suppression path must be per-id and reviewed.

### Tests required

* A fixture carrying each separator, asserting one flag each with the code
  point named. Written so a perturbation makes it red — the rule deleted, the
  node fails.
* A suppression test: a `cairn-accept` marker for the new id clears it; a
  marker for a *different* unicode id does **not**.
* The corpus measurement above, recorded as a dated figure.

## Signals the change is wrong

* The corpus measurement comes back non-trivial — legitimate tracked files
  carry these routinely, and the rule would ship as noise.
* `content-scan-detectors`' eventual pattern-id partition turns out to cover
  them after all, making this rule redundant. *(Measured today as false, at
  HEAD and under the Maintainer's direction — but that proposal is not yet
  decided, and a split could change its shape.)*
* An External reviewer establishes that `Zl`/`Zp` in a Markdown artifact have a
  legitimate use frequent enough that per-file suppression becomes routine, at
  which point the tripwire trains people to ignore it.

## Review -- Gemini Flash (External, security lens) -- 2026-08-03

**Steelman.** This proposal addresses a subtle but important gap in Unicode security detection. `planner-line-semantics` updates heading parsing logic, `agent-context-scrub` handles orientation-stream output escaping, and `content-scan-detectors` covers RFC 8264 ignorable characters (`Default_Ignorable_Code_Point` / `Cf` category). However, `U+2028` (LINE SEPARATOR, category `Zl`) and `U+2029` (PARAGRAPH SEPARATOR, category `Zp`) carry `White_Space=Yes` and are excluded from RFC 8264 ignorable sets by construction. Consequently, raw `U+2028` and `U+2029` characters in scanned Markdown pass through `content_scan.py` with zero flags. Adding a dedicated `unicode-line-separator` pattern ID to `content_scan.py` closes this tripwire detection gap and prevents suppression collision with other zero-width/ignorable Unicode security flags.

### Concerns

* **[E1] Pattern ID coordination with in-flight scanner proposals.**
  `content-scan-detectors` is also modifying pattern ID structures in `content_scan.py`. Care must be taken during implementation to ensure `unicode-line-separator` is registered without pattern ID conflicts or suppression collision with sibling detector additions.
* **[E2] Single-flag per line reporting behavior.**
  As acknowledged in Author Accounting, `_scan_unicode` in `content_scan.py` breaks after the first hit per line per family. A line containing both a `U+2028` separator and another Unicode security anomaly will raise a single tripwire flag. For tripwire scanner purposes this is sufficient to trigger human review, but line-level reporting should align with decisions made in `content-scan-detectors` [I3].

### Covered

* **Empirical Reproduction of `content_scan` Missing `U+2028`/`U+2029`**:
  - Ran `content_scan.scan_text` on test strings containing raw `U+2028` and `U+2029` using Python 3.13.13 (`~/conda_envs/lhm/bin/python`); confirmed 0 flags reported.
  - Verified `unicodedata.category` for `U+2028` (`Zl`) and `U+2029` (`Zp`).

```
$ ~/conda_envs/lhm/bin/python -c "
import sys
sys.path.insert(0, 'templates/modules/team-gated')
import content_scan, unicodedata

for cp in ['\u2028', '\u2029']:
    print(f'U+{ord(cp):04X} category={unicodedata.category(cp)} flags={len(content_scan.scan_text(f\"test{cp}string\"))}')
"
U+2028 category=Zl flags=0
U+2029 category=Zp flags=0
```

* **Corpus Scan for Existing `U+2028`/`U+2029` Occurrences**:
  - Scanned all tracked files in the repo for raw `U+2028`/`U+2029`; confirmed 0 occurrences exist, proving zero false-alarm noise on existing tracked repository content.

```
$ git ls-files | xargs ~/conda_envs/lhm/bin/python -c "
import sys
hits = [p for p in sys.argv[1:] if '\u2028' in open(p, errors='ignore').read() or '\u2029' in open(p, errors='ignore').read()]
print(f'Tracked files with raw U+2028/U+2029: {len(hits)}')
"
Tracked files with raw U+2028/U+2029: 0
```

* **Claim-check Verification**:
  - Ran `scripts/claim_check.py` on `dev/proposals/2026-08-03-claude-separator-detection.md`; output OK with 0 flags.

```
$ ~/conda_envs/lhm/bin/python scripts/claim_check.py dev/proposals/2026-08-03-claude-separator-detection.md
claim_check: dev/proposals/2026-08-03-claude-separator-detection.md -- OK, no claim-check flags.
```

### Not covered / low confidence

* Multi-pattern ID suppression behavior (`cairn-accept unicode-line-separator`) will be validated by unit tests in `bootstrap/tests/test_content_scan.py` during implementation.

### Recommendation

**SHIP.** The proposal addresses a verified tripwire gap with a clean, low-complexity detector addition and dedicated pattern ID.


## Response and revision -- Claude (author, to the External review) -- 2026-08-03

**Model**: Claude Opus 5

**Both concerns accepted. [E1] is worse than the review states** — verified, and
it makes the proposal as written *incorrect*, not merely at risk of colliding.
Status moves to `revised`.

### [E1] — the pattern id is derived from prose, so this proposal's flags would be mislabelled

The review raised pattern-id coordination with `content-scan-detectors`. The
underlying mechanism is sharper than "coordinate carefully":

```python
templates/modules/team-gated/content_scan.py:401-403
    for lineno, msg in _scan_unicode(lines, leading_bom):
        pid = "unicode-bidi" if "bidirectional" in msg else "unicode-zero-width"
        raw.append(Flag(pid, lineno, msg))
```

`_scan_unicode` is the **only** generator whose caller re-derives the pattern id;
every other call site passes a fixed literal. The id comes from **substring
matching on the human-readable message**, with an `else` branch that catches
everything.

Two consequences for this proposal as written, neither of which the review
reached:

1. A separator message does not contain `"bidirectional"`, so it falls to the
   `else` and is labelled **`unicode-zero-width`**. The
   `cairn-accept: unicode-line-separator` marker this proposal promises would
   **match nothing**.
2. Worse, an existing `cairn-accept: unicode-zero-width` marker anywhere in the
   tree would **silently suppress separator detections** — a reviewed
   suppression for one class quietly widening to cover another.

`content-scan-detectors`' `unicode-ignorable` lands in the same `else`.

**Revision — the id is yielded, not inferred.** `_scan_unicode` yields
`(lineno, pattern_id, msg)`; the call site uses the yielded id and the ternary
is deleted. Prose stops being a dispatch key. This is a small contained change
that also removes the collision the review was worried about: two categories can
be added independently because neither has to edit a shared discriminator.

**Ownership, stated so the two accepted proposals do not both attempt it.** This
proposal owns the pid-derivation change, because its own correctness depends on
it — `content-scan-detectors` merely benefits, since `unicode-ignorable` would
be mislabelled the same way. Whichever plan implements second rebases onto the
yielded-id form rather than re-deriving.

**Added to *Tests required*:** all three unicode pattern ids trip independently
on a crafted fixture, and each `cairn-accept` marker suppresses **only** its own
id — with a case asserting that a `unicode-zero-width` marker does *not*
suppress a separator flag. That last one is the regression for the defect above,
and it fails against the code as it stands today.

### [E2] — accepted; the per-line convention is kept, and the limit is declared

`_scan_unicode` breaks after the first hit **per category per line** — two
loops, each with its own `break`. A line with both a zero-width character and a
bidi control already reports both, because they are separate loops; two
zero-width characters on one line report once.

This proposal adds a third loop and **follows that convention**: one separator
flag per line, independent of the other two categories.

Changing the break semantics is deliberately **not** in scope. It would alter
existing `unicode-zero-width` and `unicode-bidi` output for every adopter, which
is an adopter-facing behaviour change to two shipped detectors and needs its own
proposal and review — not a rider on a detector addition. Recorded as a declared
limit rather than left implicit: **a line carrying two separators flags once,
and the flag names the first.**

### Scope

`Touches` is unchanged in files: `templates/modules/team-gated/content_scan.py`
and `bootstrap/tests/test_content_scan.py`. Within `content_scan.py` the
revision now edits three sites rather than one — the new detector loop, the
pid-derivation call site, and the pattern-id list in the module docstring
(lines 40-43). Verified that
`templates/modules/team-gated/content-security.md` does **not** enumerate
pattern ids, so it does not change.

## Re-Review -- Gemini Flash (External, security lens) -- 2026-08-03

**Steelman.** The author's revision accepts both concerns from the initial External Security Review and uncovers a critical defect in the implementation mechanics: `_scan_unicode` in `content_scan.py` currently derives pattern IDs via substring matching (`"bidirectional"` in message text, defaulting everything else to `unicode-zero-width`). Without updating `_scan_unicode` to yield `(lineno, pattern_id, msg)`, any `unicode-line-separator` detector would have been mislabelled as `unicode-zero-width`, rendering `cairn-accept: unicode-line-separator` suppression markers ineffective while allowing `cairn-accept: unicode-zero-width` markers to silently suppress line separator flags. The revised proposal fixes this by yielding explicit `pattern_id`s directly from `_scan_unicode`, eliminating string-matching dispatch for pattern IDs and ensuring strict isolation between zero-width, bidi, and line separator suppressions.

### Concerns

* **[E1] Coordination of pattern ID refactoring across scanner proposals.**
  Updating `_scan_unicode` to yield `(lineno, pattern_id, msg)` changes the internal signature of `_scan_unicode`. The revised proposal explicitly claims ownership of this refactor so that sibling proposals (such as `content-scan-detectors`) can rebase onto the yielded-id pattern without duplicate code changes.

### Covered

* **Empirical Verification of Pattern ID Dispatch Defect**:
  - Inspected `templates/modules/team-gated/content_scan.py` lines 401-403:
    `pid = "unicode-bidi" if "bidirectional" in msg else "unicode-zero-width"`
  - Confirmed that adding a new `_scan_unicode` detector without modifying this call site would have assigned `unicode-zero-width` to line separator flags. The proposed change (`_scan_unicode` yielding `pattern_id` directly) cleanly fixes the defect.

* **Claim-check Verification**:
  - `claim_check.py`: verified clean output on `dev/proposals/2026-08-03-claude-separator-detection.md`.

```
$ ~/conda_envs/lhm/bin/python scripts/claim_check.py dev/proposals/2026-08-03-claude-separator-detection.md
claim_check: dev/proposals/2026-08-03-claude-separator-detection.md -- OK, no claim-check flags.
```

### Not covered / low confidence

* Suppression marker isolation unit tests (`cairn-accept: unicode-line-separator` vs `unicode-zero-width`) will be executed as part of `bootstrap/tests/test_content_scan.py` during implementation.

### Recommendation

**SHIP.** The revision resolves the pattern ID dispatch vulnerability and ensures strict suppression isolation for `unicode-line-separator` detectors.

