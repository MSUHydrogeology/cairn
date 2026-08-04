<!-- cairn-internal-ref-allow: doctrine/runtime-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# The two separators nothing detects — `U+2028` / `U+2029` fall between three proposals

**Author**: Claude (Strategy)
**Model**: Claude Opus 5.
**Date opened**: 2026-08-03
**Status**: proposed
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
