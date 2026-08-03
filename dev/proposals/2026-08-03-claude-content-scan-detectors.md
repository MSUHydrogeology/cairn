<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/proposals.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# The content scanner misses the invisible channel and cries wolf at Greek variables

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: proposed
**Touches**: `templates/modules/team-gated/content_scan.py` (the two detector
rules only), `templates/modules/team-gated/content-security.md` (the module
doc that describes them), `bootstrap/tests/test_content_scan.py` (new cases)
**Related**: Theme 3 of the `2026-07-08-claude-broad-look-skeptical-review`
strategy note, item 2 of the Maintainer's Theme-3 work order; the
`content-security` module; the reviewed-residual baseline mechanism in
`templates/modules/team-gated/content_scan_runner.py`
**Plan review**: required(External, security lens) — the change alters what a
shipped **security detector** does and does not flag, which is the
"Bootstrap safety / security stack" trigger in the proposal template's
`triage-extra-triggers` block ("`bootstrap/SAFETY.md` (R-I),
`bootstrap/security_check.py`, or the content scanner; a change here is also a
Security Review trigger"). Half of this change *removes* flags, so a
same-type reviewer who shares my threat-model blind spots is not enough: the
detection-loss claim needs an adversarial read by a different agent type or a
human. A same-session Internal pass would be a floor, not the tier.

## Context

**What the thing is.** `content_scan.py` is Cairn's content-integrity
tripwire — a small standard-library scanner that reads the Markdown an AI agent
will later load as governing instructions (`AGENTS.md`, the `dev/` tree, the
skills) and flags patterns that look like a **prompt-injection** attempt: text
planted in a document that an agent obeys as though the maintainer had written
it. It is deliberately a *witness*, not a proof: it forces a human to look, it
never certifies a file safe. The same file ships verbatim into every adopter
that installs the `content-security` module, and Cairn runs it on its own tree
through `scripts/check_cairn.py`. It is not dormant: `check_cairn.py` loads it
by `importlib` and scans every tracked `.md`.

Among its seven detectors, two matter here:

* **`unicode-zero-width` / `unicode-bidi`** — the "invisible character"
  detectors. They exist because a code point that renders as nothing can carry
  text a human reviewer physically cannot see while an AI model reads it
  normally.
<!-- cairn-accept: homoglyph reason="This section's mixed-script tokens ARE the evidence: the scientific notation is the false-positive case being measured and the spoofs are the true-positive case. Rewriting them to ASCII would delete the finding this proposal exists to record. Block-scoped, not document-scoped, so a homoglyph planted elsewhere in this file still flags." reviewer="Claude (Strategy)" date=2026-08-03 -->
* **`homoglyph`** — flags a single word that mixes writing systems, e.g. a
  Latin word with one Cyrillic letter substituted (`pаssword`), the classic
  look-alike spoof.
<!-- cairn-accept-end: homoglyph -->

Both are defective at HEAD (`3292f21`), and the two defects are the two halves
of the same mistake: **the character model underneath them is wrong in both
directions** — too narrow about which invisible code points exist, and too
coarse about which visible ones are confusable.

### Defect (a) — an entire invisible channel passes with zero flags

The invisible-character detectors enumerate nine specific code points
(`_ZERO_WIDTH` plus `_BIDI`). Unicode's *Default_Ignorable_Code_Point*
property covers far more, including the whole **Tag block** (U+E0000–U+E007F),
which encodes a complete shadow ASCII alphabet in characters of Unicode
category `Cf` that render as nothing at all. Verified at HEAD under the
canonical interpreter (Python 3.13.13):

```
plain ASCII payload  -> 2 flag(s): ['imperative-override', 'egress']
tag-block payload    -> 0 flag(s): []
```

The payload in both runs is the same sentence — an override instruction plus an
exfiltration instruction. Written in ASCII the scanner catches it twice.
Re-encoded one-for-one into the Tag block it is invisible on screen, invisible
to `git diff`, and produces **no flags at all**. Eight other invisible or
default-ignorable code points tested the same way also produce zero flags,
including SOFT HYPHEN (U+00AD) — which can be dropped *inside* a word — and
the variation selectors.

This is the highest-severity finding in this proposal: the detector class whose
entire purpose is "a human cannot see this" has a hole shaped exactly like its
purpose.

### Defect (b) — the homoglyph rule cries wolf at ordinary scientific notation

<!-- cairn-accept: homoglyph reason="This section's mixed-script tokens ARE the evidence: the scientific notation is the false-positive case being measured and the spoofs are the true-positive case. Rewriting them to ASCII would delete the finding this proposal exists to record. Block-scoped, not document-scoped, so a homoglyph planted elsewhere in this file still flags." reviewer="Claude (Strategy)" date=2026-08-03 -->
The homoglyph rule flags any token that mixes two script ranges, and its
`_SCRIPT_RANGES` table treats the **whole Greek block** as conflicting with
Latin. A `Δ` in `ΔG` is, to this rule, the same event as a Cyrillic `а` in
`pаssword`. The one carve-out (`_is_scientific_unit`, "RV5") covers only the
micro and ohm *unit* shapes (`µs`, `kΩ`) — not Greek letters used as
*variables*, which is how scientists actually write.

Measured at HEAD over 42 ordinary scientific tokens — Gibbs free energy,
peak wavelength, yield stress, bulk density, dispersivity, and so on, each
written with the real Greek letter a scientist would type:

```
=== current ===
  scientific FALSE POSITIVES : 37/42  ['ΔG', 'ΔH', 'ΔS', 'ΔCp', 'ΔGrxn', 'Kα',
  'Kβ', 'λmax', 'νmax', 'εr', 'λex', 'λem', 'σy', 'σmax', 'τc', 'εp', 'γd',
  'νp', 'ρw', 'ρb', 'ρs', 'αL', 'αT', 'νt', 'θr', 'θs', 'ψm', 'ωopt', 'κeff',
  'αlevel', 'βpower', 'ηeff', 'φp', 'Ωn', 'βsheet', 'γray', 'αdecay']
```

**Why this is a security defect and not a papercut.** The scanner's contract is
that a flag means *stop and look*. Clearing a flag is not free in Cairn: an
adopter must either write an inline `cairn-accept` marker with a reason,
reviewer, and date, or add a per-occurrence fingerprint to the reviewed-residual
baseline — which is multiset-compared, so a *stale* entry fails the scan and
must be pruned when the line is edited. A hydrologist writing a design note
about `ρw`, `αL`, and `νt` therefore pays a per-line review tax for writing
their own discipline's notation correctly. The predictable adaptation is to
stop reading `homoglyph` output, which is exactly how the real Cyrillic
substitution gets through. This project already has one live instance of the
genuine article: the `2026-08-03-claude-identity-not-name` proposal carries two
`cairn-accept: homoglyph` markers for a demonstrated Cyrillic byline spoof. A
detector that fires 37 times on thermodynamics for every once on that is not a
tripwire; it is background noise.

**Postdoc-first.** The first external adopter is a scientist. Week one, they
write a proposal containing `ΔG` and `λmax`, run the gate Cairn told them to
run, and get flagged for prompt injection in their own prose. Meanwhile the
channel that would actually be used against them is wide open.
<!-- cairn-accept-end: homoglyph -->

## Proposal

Two rule corrections inside `templates/modules/team-gated/content_scan.py`.
No new file, no new tool, no new configuration surface, no change to the
suppression grammar, the allowlist, the roots manifest, or the residual
baseline.

### Change 1 — a `unicode-ignorable` detector, adopted not invented

Add one detector and one pattern id, `unicode-ignorable`, over the set RFC 8264
(the PRECIS framework) § 9.13 `PrecisIgnorableProperties` defines for free-form
text: `Default_Ignorable_Code_Point(cp) = True OR
Noncharacter_Code_Point(cp) = True`. Citing PRECIS matters — this is the set an
existing standard already decided must not pass silently through free-form
text, so the rule reads as adopted rather than hand-rolled.

The set is held as two hard-coded numeric range tables — 17 ignorable rows and
18 noncharacter rows — **not** raw characters, preserving the existing
invariant (enforced by `TestSourceCarriesNoRawInvisibles`) that the scanner
carries none of the code points it detects. There is no data file and no new
dependency; the one new import is `unicodedata`, standard library, used only to
put a human-readable character name in the message.

* A character already reported by `unicode-zero-width` or `unicode-bidi` is
  **skipped**, so no line double-flags and no existing `cairn-accept` marker or
  residual fingerprint is invalidated. The two existing pattern ids keep their
  exact current meaning.
* **Detect and fail. Never rewrite.** The scanner does not strip, normalize, or
  "clean" anything. The deliberation record is append-only; a tool that
  silently edited committed prose would be a worse defect than the one it
  fixed. The flag says *a human must look at this line*, and that is all.

### Change 2 — the homoglyph rule becomes confusability-aware

Replace "any two script ranges in one token" with a three-clause rule. A token
flags when **any** clause holds:

1. **Whole-script confusable** — the token has no Latin characters, has at
   least three letters, and *every* letter has an ASCII-Latin look-alike. This
   closes a pre-existing hole (below).
2. **Non-Greek script mixed with Latin** — Cyrillic, Armenian, Cherokee,
   Coptic, or fullwidth Latin inside a Latin token always flags. Unchanged
   behaviour.
<!-- cairn-accept: homoglyph reason="This section's mixed-script tokens ARE the evidence: the scientific notation is the false-positive case being measured and the spoofs are the true-positive case. Rewriting them to ASCII would delete the finding this proposal exists to record. Block-scoped, not document-scoped, so a homoglyph planted elsewhere in this file still flags." reviewer="Claude (Strategy)" date=2026-08-03 -->
3. **Greek mixed with Latin, where a Greek character has a Latin look-alike** —
   e.g. `ρassword` (rho reads as `p`), `Αdmin` (capital Alpha reads as `A`).
   The one exception is the two-character variable-plus-subscript shape:
   exactly one Latin letter and exactly one Greek letter, total length two
   (`ρw`, `Kα`, `εr`, `αL`, `τc`).

The pivot is a new frozen set, `_CONFUSABLE_GREEK` — 32 Greek/Coptic code
points that have an ASCII-Latin twin, each commented with the Latin letter it
imitates, curated from the shape correspondences in UTS #39's confusables data.
Erring toward *inclusion* is the safe direction, because inclusion means
flagging. A Greek letter with no Latin twin (`Δ`, `λ`, `σ`, `θ`, `φ`, `ψ`, `β`,
`μ`, `Ω`) cannot power a visual spoof **by definition of the threat**, so
clearing it costs no detection.

The existing `_is_scientific_unit` (RV5) allowance is left in place unchanged.

### What Change 2 also fixes, unasked

The current rule misses a *fully* substituted word, because an all-Greek token
is single-script and single-script tokens are never flagged. Measured over 40
security-relevant words with every substitutable letter replaced:

```
=== current ===
  maximal-sub sweep caught   : 34/40  missed=['εχεϲυτε', 'τοκεη', 'κεγ', 'αρι', 'εην', 'ηοτ']
=== FINAL ===
  maximal-sub sweep caught   : 39/40  missed=['dο']
```
<!-- cairn-accept-end: homoglyph -->

An attacker one keystroke past the current rule's reach — substitute *every*
letter instead of one — walks straight through today. Clause 1 closes five of
those six. This is why the relaxation in clause 3 is not a net weakening: the
proposal ends with **strictly better** detection than HEAD on every adversarial
sweep run except one two-letter token, and that one is named below.

### Why this is one proposal and not two

Both changes are the same contract — the character model of one shipped
scanner — in one file, and they carry one review tier, one gate set, and one
verification command. Splitting them would put the same `test_content_scan.py`
and the same External security review through two lifecycles for one file.
That said, the split line is clean if a reviewer wants it: **Change 1 is
independently landable** (it only adds flags and touches no existing rule).
Change 2 is not independently landable in the other direction — dropped alone
it would leave the invisible channel open, which is the worse of the two
defects.

### Documentation / doctrine surface

* `templates/modules/team-gated/content_scan.py` — the module docstring's
  bulleted pattern-id list gains `unicode-ignorable` and the `homoglyph` entry
  is rewritten to describe the confusability rule. This docstring is the
  scanner's user-facing contract.
* `templates/modules/team-gated/content-security.md` — the
  "Scientific-unit homoglyph allowance" section (currently describing RV5 only)
  is rewritten as a *scientific-notation* allowance, stating the rule, the seven
  residual shapes that still flag, and what to do about them.
* **No other surface.** `bootstrap/SAFETY.md` and `SECURITY.md` name the
  scanner but do not enumerate its pattern ids — checked, no edit needed.
  `AGENTS.md` is untouched. No file under `doctrine/` is touched. No
  `dev/modules/` mirror of `content-security.md` exists.
* **Not touched, stated explicitly**: `bootstrap/_scaffold/` — no engine
  change, no `InstallSpec` added or moved (`content_scan.py` is already
  registered as a verbatim install), therefore **no AST re-anchor obligation**
  and no `scaffold_ast_baseline.json` delta. If review shows I am wrong about
  that, the plan must gain the full high-risk engine obligations from
  `AGENTS.md` before executing.

### Doctrine-change rate-limit (if this proposal changes doctrine)

**Not a doctrine change.** This corrects two defects in a shipped tool and
syncs the module doc that describes that tool; it introduces no rule, process,
or contract that a contributor must follow. The rate-limit gate does not apply.

If a reviewer instead classifies "what the security scanner flags" as doctrine,
the gate is cleared on the **high-risk classification** branch rather than
recurrence: the Maintainer commissioned Theme-3 work explicitly as a security
surface, and defect (a) is a detection hole in the injection-defence layer.

## Rationale

* **Which user workflow does it improve?** Writing scientific prose in a
  Cairn-governed repository. Today that workflow collides with the security
  gate 37 times in 42 tokens; after this change, 7.
* **What contract does it clarify?** That a `homoglyph` flag means "a character
  here imitates a Latin letter", not "this token contains Greek". The current
  rule's name and its behaviour disagree, and the behaviour is the one adopters
  experience.
* **What correctness does it improve?** Detection, on both axes: an entire
  invisible encoding channel becomes visible to the gate, and five of six
  fully-substituted spoofs that pass today are caught.
* **Why now?** Pre-first-external-adopter. Both defects are cheap to fix now
  and expensive later: once a scientist's repository carries dozens of
  `cairn-accept: homoglyph` markers and residual fingerprints written to silence
  false alarms, tightening the rule means auditing every one of them to tell a
  reasoned suppression from a reflexive one.

## Alternatives considered

* **Do nothing.** Rejected on defect (a) alone — the invisible channel is a
  live detection hole in the layer Cairn advertises as its injection defence.
  On defect (b), do-nothing has a hidden cost that compounds: every month of
  delay is more suppression markers written to quiet a rule that was wrong.
* **Fix (a) only; leave the homoglyph rule alone.** The honest fallback, and
  the named split line if review wants it. Rejected as the primary plan because
  the alarm-fatigue defect is what makes an adopter *stop reading* the very
  output that (a) newly produces. Fixing detection while leaving the channel
  noisy delivers the flag to someone who has learned to ignore flags.
* **Ship the full UTS #39 confusables data and do real restriction-level
  detection.** The rigorous answer, and rejected: `confusables.txt` is a
  large external data file requiring a version pin and an update path, against
  a hard zero-runtime-dependency budget (`bootstrap/DEPENDENCY_BUDGET.md`), for
  a tool whose own docstring says it is a witness and not a proof. A 32-entry
  curated set, each entry commented with the Latin letter it imitates, is
  auditable by a reviewer in one screen — which a several-thousand-line data
  file is not.
* **Widen the RV5 unit allowance to a longer list of scientific tokens.**
  Rejected: an enumerated token list is a treadmill that is always behind the
  next discipline, and it answers "is this token on my list?" rather than the
  actual question, "can this character imitate a Latin letter?".
* **Let adopters absorb the false positives through the residual baseline.**
  That is the status quo, and it is what makes the defect expensive rather than
  merely annoying — each occurrence is a fingerprint that must be pruned when
  its line changes. Making the tool correct is cheaper than making every
  adopter maintain a list of the tool's mistakes.
* **Normalize or strip the ignorable characters instead of flagging them.**
  Rejected outright and on principle. The record is append-only; a scanner that
  edited committed prose would be a larger defect than the one it repaired.
  Detect and fail.
<!-- cairn-accept: homoglyph reason="This section's mixed-script tokens ARE the evidence: the scientific notation is the false-positive case being measured and the spoofs are the true-positive case. Rewriting them to ASCII would delete the finding this proposal exists to record. Block-scoped, not document-scoped, so a homoglyph planted elsewhere in this file still flags." reviewer="Claude (Strategy)" date=2026-08-03 -->
* **Position-only relaxation** (allow any Greek run at a token boundary).
  Tested and rejected during drafting: it clears `Αdmin` and `ρassword`, both
  boundary-leading spoofs. Confusability, not position, is the load-bearing
  axis.
* **Relax on "at most one Latin letter"** (a first draft of clause 3). Tested
  and rejected: an adversarial sweep showed it lets nine fully-substituted
  spoofs through (`ροsτ`, `lεακ`, `rυη`, `rοοτ`, `ενιl`, `ρωd`, `τhε`, …) by
  driving the Latin count to one. Tightening it to "exactly two characters, one
  Latin and one Greek" removed all nine at no cost to the scientific-token
  numbers. This is the substantive design iteration in the proposal and the
  place a reviewer should push hardest.
<!-- cairn-accept-end: homoglyph -->

## Evidence / verification plan

All figures below are dated snapshots measured at `3292f21` on 2026-08-03
under the canonical interpreter (Python 3.13.13, UCD 15.1.0), by loading the
scanner with `importlib` and, for the "after" figures, by patching a **scratch
copy** outside the repository. Nothing in the working tree was modified to
produce them. HEAD advanced to `8d17d9a` during drafting; that commit touches
no file in scope (verified with `git diff --stat` over the scanner, its tests,
and `scripts/check_cairn.py` — empty), so the figures stand.

**Baseline suite at HEAD**: `python -m pytest bootstrap/tests` →
`1556 passed` in 143s.

**Defect (a), before and after** — same payload, three encodings:

| case | at HEAD | with the patch |
|---|---|---|
| ASCII payload | 2 flags | 2 flags |
| Tag-block payload (U+E0000–) | **0 flags** | 1 `unicode-ignorable` |
| SOFT HYPHEN inside a word | **0 flags** | 1 `unicode-ignorable` |
| noncharacter U+FDD0 | **0 flags** | 1 `unicode-ignorable` |
| ordinary clean prose | 0 flags | 0 flags |

**The ignorable constant is complete against the shipped interpreter's
Unicode**: every `Cf`-category code point in UCD 15.1.0, excluding the two
families PRECIS itself excludes (prepended concatenation marks, interlinear
annotation) plus the Egyptian hieroglyph format controls, falls inside the
17 hard-coded ranges. Measured result: the uncovered set is empty (`[]`).

**Defect (a) costs Cairn nothing today**: the detector run across all 423
tracked `.md` / `.txt` / `.py` files raises **0** new flags — no emoji
variation selector, no stray soft hyphen.

**Defect (b), the full rule comparison** (42 scientific tokens; 21 hand-built
spoofs; 153 single-substitution spoofs generated from 40 security-relevant
words; 40 maximal-substitution spoofs):

| measure | at HEAD | with the patch |
|---|---|---|
| scientific-token false positives | 37 / 42 | **7 / 42** |
| Cyrillic spoofs caught | 7 / 7 | 7 / 7 |
| Greek spoofs caught | 14 / 14 | 14 / 14 |
| single-substitution sweep caught | 153 / 153 | 152 / 153 |
| maximal-substitution sweep caught | 34 / 40 | **39 / 40** |

<!-- cairn-accept: homoglyph reason="This section's mixed-script tokens ARE the evidence: the scientific notation is the false-positive case being measured and the spoofs are the true-positive case. Rewriting them to ASCII would delete the finding this proposal exists to record. Block-scoped, not document-scoped, so a homoglyph planted elsewhere in this file still flags." reviewer="Claude (Strategy)" date=2026-08-03 -->
Net across both sweeps: **one** false negative introduced (`dο`, the two-letter
word "do"), **five** pre-existing false negatives closed, **30** false positives
removed.
<!-- cairn-accept-end: homoglyph -->

**No regression on Cairn's own corpus**: comparing the full flag set —
pattern id and line number — file by file across all 207 tracked `.md` files,
the number of files whose flag set changes is **0**. Both existing
`cairn-accept: homoglyph` markers stay live and necessary (their tokens are
Cyrillic). Over ~508k tokens in the tracked `.md` / `.txt` tree, **0** tokens
change verdict.

**Every existing assertion in `test_content_scan.py` was replayed against the
patched scanner**: 15 of 15 pass, including the source-carries-no-raw-invisibles
hygiene test, all four expanded-script homoglyph cases, the BOM cases, the URL
allowlist, and the red-team fixture on every vector. **Bandit** over the patched
file: clean, exit 0.

**Left to the plan, not claimed here**: the real `pytest` run of the whole
suite against the real file; `scripts/check_cairn.py` end to end;
`bootstrap/tests/test_python_floor.py` (`vermin` is not installed in this
session, so the ≥3.11 floor claim for the new code is *unverified* — the plan
must run it); and confirming the RFC 8264 section number against the published
RFC, which I cited from knowledge and could not fetch offline.

### Author-accounting — invariants, failure modes, edge cases

**Invariants**

| invariant | enforcer |
|---|---|
| The scanner source carries no raw invisible code point it detects | existing `TestSourceCarriesNoRawInvisibles::test_no_raw_banned_codepoints_in_source`; the new tables are numeric ranges |
| `unicode-zero-width` and `unicode-bidi` keep their exact current meaning, so existing suppressions and residual fingerprints stay valid | the skip in the new detector; a new test asserting a ZWSP line yields `unicode-zero-width` and *not* `unicode-ignorable` |
| A non-Greek confusable script mixed with Latin always flags | existing `TestHomoglyphExpandedScripts::test_expanded_confusable_scripts_flagged`, unmodified |
| The scanner never modifies the text it scans | `scan_text` returns flags and has no write path; new test asserting the input string is unchanged after a scan |
| The ignorable constant covers every `Cf` code point in the running interpreter's UCD, minus the documented exclusions | new test computing the set from `unicodedata` and asserting the uncovered set is empty — this is the invariant that catches a future UCD drift |

**Failure modes**

* *Closed* — a malformed or unreadable file: unchanged, `scan_file` propagates.
* *Open, and intentional* — `unicodedata.name()` has no name for a reserved
  code point; the two-argument form supplies `"unnamed / reserved"` so the flag
  still fires. A missing name must never suppress a flag.
* *Open, and intentional* — the confusable set is curated, so an unlisted
  look-alike is a miss. This is the scanner's declared witness-not-proof
  posture, unchanged in kind from HEAD.
* *Open, and the one to watch* — a future Unicode version could add a
  default-ignorable code point outside the frozen ranges. The derivation's
  exclusion list has moved between UCD versions before, so the constant is a
  pinned snapshot, not a live derivation. The UCD cross-check test above is
  what surfaces the drift.

**Edge cases** — handled: empty file; single-character token; a token of digits
only (no script, never flags); leading BOM (existing exemption preserved); a
line mixing an already-covered zero-width character and a newly-covered
ignorable one (reported once, under the existing id). Out of scope: text in a
non-Latin *natural language* — a Greek- or Russian-language repository would
see clause 1 misfire, and Cairn's doctrine and templates are English.

**Public-path → test mapping** — the two public entry points are `scan_text`
and `scan_file`; both are exercised through their public path in
[`bootstrap/tests/test_content_scan.py`](../../bootstrap/tests/test_content_scan.py),
where the new cases go alongside the existing ones. No new public function is
added; `_is_homoglyph`, `_is_ignorable`, and the two range tables are private
and are reached through `scan_text`.

**Known omissions / intentionally untested edges**

<!-- cairn-accept: homoglyph reason="This section's mixed-script tokens ARE the evidence: the scientific notation is the false-positive case being measured and the spoofs are the true-positive case. Rewriting them to ASCII would delete the finding this proposal exists to record. Block-scoped, not document-scoped, so a homoglyph planted elsewhere in this file still flags." reviewer="Claude (Strategy)" date=2026-08-03 -->
* **The named false negative**: a two-character token of one Latin letter plus
  one confusable Greek letter is cleared, so `dο` ("do"), `ιd` ("id"),
  `gο` ("go") pass. Two characters cannot carry an instruction. The one case
  with teeth is a two-letter *domain label* (`gο.dev`), and the `suspicious-url`
  detector covers it independently — verified: a Greek-omicron domain does not
  match an ASCII allowlist entry and flags as a non-allowlisted URL, where the
  ASCII original is clean.
* **The seven residual scientific false positives** — `νmax`, `ωopt`, `κeff`,
  `αlevel`, `ηeff`, `γray`, `αdecay`: a confusable Greek letter leading a Latin
  run of three or more. These are structurally indistinguishable from `ρassword`
  and `Αdmin`; separating them needs a lexicon, which is out of budget and out
  of scope. They stay flagged, and the module doc will say so plainly so an
  adopter meets a documented limit rather than a surprise.
<!-- cairn-accept-end: homoglyph -->
* **Not measured**: performance. The scanner gains two range-table lookups per
  character; the corpus runs above completed in seconds over ~508k tokens, but
  I did not benchmark it and do not claim a number.
* **Not attempted**: any change to the suppression grammar, the residual
  baseline, the roots manifest, or the runner.

### Tests required

All in `bootstrap/tests/test_content_scan.py`, built with `\uXXXX` escape
forms — never raw invisible characters — matching the file's existing
convention:

1. `unicode-ignorable` fires on a Tag-block payload, on SOFT HYPHEN inside a
   word, on a variation selector, and on a noncharacter.
2. `unicode-ignorable` does **not** fire on a character already covered by
   `unicode-zero-width` or `unicode-bidi`, and those two ids still fire there.
3. The ignorable range table covers every `Cf` code point in the running
   interpreter's UCD minus the documented exclusions (the drift sentinel).
<!-- cairn-accept: homoglyph reason="This section's mixed-script tokens ARE the evidence: the scientific notation is the false-positive case being measured and the spoofs are the true-positive case. Rewriting them to ASCII would delete the finding this proposal exists to record. Block-scoped, not document-scoped, so a homoglyph planted elsewhere in this file still flags." reviewer="Claude (Strategy)" date=2026-08-03 -->
4. Ordinary scientific tokens do not flag: `ΔG`, `λmax`, `σy`, `ρw`, `Kα`,
   `εr`, `βsheet`.
5. Spoofs still flag: `pаssword` (Cyrillic), `Αdmin` and `ρassword` (leading
   confusable Greek), `sοurce` (interior), `kεy` (the tightest three-letter
   case), `τοκεη` (whole-script confusable).
<!-- cairn-accept-end: homoglyph -->
6. The named two-character carve-out is asserted **as a known limit**, so a
   future reader sees it was chosen rather than overlooked.
7. `scan_text` leaves its input unmodified.

New nodes must be added to `bootstrap/tests/fixtures/gate_manifest.json` if a
gate-manifest batch is running; note also that editing `test_content_scan.py`
is a modification to a *frozen* file under that tool's rules and HOLDs by
default in an unattended batch. This change is supervised, so that is a
sequencing note for the plan, not a blocker.

### Examples / smoke checks

* `python -m pytest bootstrap/tests` — the full suite; baseline `1556 passed`
  must not regress.
* `python scripts/check_cairn.py` — the composed self-scan over the tracked
  `.md` tree; must stay at its current flag count, which the corpus comparison
  above predicts (0 files change).
* `python scripts/content_scan.py <file>` in a scaffolded tree — the adopter's
  own path, to confirm the shipped verbatim copy behaves identically.
* `python bootstrap/scaffold.py --manifest` — unchanged output expected; the
  install contract is not touched.
* **Docs**: delivered, named above under *Documentation / doctrine surface*.

## Signals the change is wrong

* **`scripts/check_cairn.py` flag count moves at all.** Predicted delta is
  zero. Any movement means the corpus comparison was wrong; re-measure before
  proceeding, do not suppress the new flag.
<!-- cairn-accept: homoglyph reason="This section's mixed-script tokens ARE the evidence: the scientific notation is the false-positive case being measured and the spoofs are the true-positive case. Rewriting them to ASCII would delete the finding this proposal exists to record. Block-scoped, not document-scoped, so a homoglyph planted elsewhere in this file still flags." reviewer="Claude (Strategy)" date=2026-08-03 -->
* **A reviewer produces a spoof that HEAD catches and the patch clears, other
  than the named `dο` shape.** That is the falsifying test for this whole
  proposal. Recovery: drop clause 3's two-character exception, accept ~19 of
  42 scientific false positives instead of 7, and keep the rest.
<!-- cairn-accept-end: homoglyph -->
* **The UCD cross-check test fails on a future interpreter.** The pinned
  ranges have drifted; update the constant, do not relax the test.
* **An adopter reports a legitimate document that now flags `unicode-ignorable`
  and cannot reasonably be rewritten** — most plausibly an emoji sequence using
  a variation selector or a regional-tag flag. Recovery: an inline
  `cairn-accept` marker is the designed answer; if it recurs across adopters,
  carve out U+FE00–FE0F specifically and document why, rather than weakening
  the PRECIS set wholesale.
* **The seven residual scientific false positives generate suppression markers
  in an adopter's tree within the first month.** The precision fix did not go
  far enough for real scientific prose, and the lexicon alternative this
  proposal rejected deserves reopening on evidence.
* **Anyone proposes to make the scanner rewrite rather than flag.** That is the
  signal the "detect and fail" boundary was not stated loudly enough here.
