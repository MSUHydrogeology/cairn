<!-- cairn-internal-ref-allow: doctrine/lifecycle-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# Exact byline classification — a fold that drops no letter and no digit, in any script

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: reviewed
**Touches**: `tools/lifecycle_planner.py` and its byte-identical
`templates/skills/_lib/lifecycle_planner.py` twin; the live roster value in
`dev/.cairn/agent-identities.json`; one existing node plus new nodes under
`bootstrap/tests/`; the `verbatim` lockfile row for the twin pair; a
`CHANGELOG.md` behaviour-change entry
**Related**: successor **scope 2** of the superseded `identity-not-name`
proposal (Decision `6c6ce39`, 2026-08-03), whose 2026-08-03 Amendment
demonstrated the exploit and whose External Security Review finding **[IDN3]**
fixed the framing. Sibling in-flight proposals sharing this file or its
lineage: `planner-line-semantics` (same module, disjoint functions) and
`agent-context-scrub` (same root cause, different file). Theme 3 of the strategy
note `2026-07-08-claude-broad-look-skeptical-review`
**Plan review**: required(External, security lens) — see *Rationale > Why this
tier*

## Context

### What the Decision handed this proposal

The `identity-not-name` lifecycle was superseded into four scopes. Scope 2 is
this one, and the Decision raised it from a correctness cleanup to *"a security
fix with a demonstrated exploit"*, named the invariant it must enforce —

> **dropping a character must never widen authority**

— and bound every successor to state its residuals with an expiry trigger.
[IDN3] settled the framing before that: this tool is a **structural lint**, not
authentication. It attests that a document has the shape a transition requires;
the operator who commits the document guarantees that the authorization it
quotes is real. Nothing below claims otherwise, and the exact-name spoof stays
an accepted residual rather than something this change prevents.

### The surface, for a reader who has not opened the file

`tools/lifecycle_planner.py` reads a proposal or plan and reports whether its
*current recorded state is structurally sound* — for a terminal state
(`accepted` / `rejected` / `superseded`), that includes: is there a `## Decision`
section, does it carry a visually isolated authorization blockquote, and is the
name on its heading a **human Maintainer** rather than an AI agent? The last
question is answered by a three-way classifier: `ai` (on a built-in agent-name
registry), `human` (on the project's own allowlist in
`dev/.cairn/agent-identities.json`), or `unknown`. Both `ai` and `unknown`
produce a violation; only `human` is silent. The design is deliberately
*positive* — humanity must be proved, never inferred from a name failing to look
robotic — and `tools/lifecycle_planner.py:187` says so in the code.

That design is right. Its **normalization** is not.

Two functions turn a display name into the token that gets matched, and each
uses the same one-liner:

* `tools/lifecycle_planner.py:237` — `_identity_token`, the *first* word.
* `tools/lifecycle_planner.py:251` — `_ai_candidate_tokens`, *every* word.

Both do `re.sub(r"[^a-z0-9]", "", raw.lower())`. In Python 3 that pattern is
Unicode-aware, so the class `[^a-z0-9]` matches every character that is not an
ASCII letter or digit — **including every non-ASCII letter, which is therefore
deleted**. A third site, `tools/lifecycle_planner.py:293`, normalizes each
*roster entry* with the same one-liner but applied to the **whole entry** rather
than per word, and `tools/lifecycle_planner.py:314` matches those whole-entry
keys against **per-word** byline tokens by set intersection.

### Three defects, all reproduced by execution

Run against the live tree at `71abeb4` under the canonical interpreter
(`~/conda_envs/lhm/bin/python`, 3.13.13), 2026-08-03. **No confusable or
invisible character appears as a literal anywhere in this proposal** — every
such reproducer builds its character with `chr(...)`, because committing a
working carrier into the deliberation record would be its own defect.
`U+0430` is CYRILLIC SMALL LETTER A; it renders identically to ASCII `a` in
every editor, terminal, diff, and web view. Presentational variants that are
*visibly* distinct (`á`, `𝐂`, `Ⓒ`) do appear as literals: they carry no
spoofing risk, a reader can see exactly what they are, and the `content_scan`
homoglyph detector agrees — it returns `0` flags on this file.

**(a) A homoglyph flips `ai` to `human`.** This is the Amendment's exploit,
re-verified:

    honest = "Claude scribing for Anthony Kendall"
    spoof  = "Cl" + chr(0x430) + "ude scribing for Anthony Kendall"

    classify(honest) -> ai        tokens: ['claude', 'scribing', 'for', 'anthony', 'kendall']
    classify(spoof)  -> human     tokens: ['clude',  'scribing', 'for', 'anthony', 'kendall']

The Cyrillic character is *deleted*, so the token `claude` never forms, the AI
registry never fires, and the byline falls through to the human allowlist —
which matches on the *other* words, `anthony` and `kendall`, that the scribing
convention legitimately puts there. Dropping one character moved the byline from
"AI agent — violation" to "recognized Maintainer — silent".

**(b) Roster and byline normalize by different rules, so both directions are
wrong.** Entries fold whole, bylines fold per word:

    roster ['Anthony Kendall']   -> keys {'anthonykendall'}
        'Anthony Kendall' -> unknown ,  'Anthony' -> unknown ,  'Kendall Jenner' -> unknown
    roster ['Anthony', 'Kendall'] -> keys {'anthony', 'kendall'}
        'Anthony Kendall' -> human   ,  'Anthony' -> human   ,  'Kendall Jenner' -> human

The configuration a reader would obviously write — the Maintainer's full name —
matches nothing, so every Decision they author is flagged. The configuration
that works is the one that also grants `Kendall Jenner`, `Kendall Smith`, and
bare `Anthony`. Cairn's live config is the second kind, which is exactly why
Cairn does not currently see failure (a) as an outright break.

**(c) A third widening, not previously recorded, on a second authority
surface.** `_identity_token` is not only used for classification. It is the
**independence comparator**: `tools/lifecycle_planner.py:590` flags a `## Review`
that appears to be authored by the proposal's own author, and
`tools/lifecycle_planner.py:683` computes the `independent_review` gate that
must be met before a proposal may move to a terminal state. Both ask only
whether two tokens differ. Measured, author = `Claude (Strategy)`:

    reviewer 'Claude (Internal Review)'                  tokens ('claude','claude')  self-review FLAGGED
    reviewer 'Cl' + chr(0x430) + 'ude (Internal Review)' tokens ('claude','clude')   self-review NOT flagged
                                                                                     independent_review gate MET

One invisible character turns a same-agent review into a review the tool reports
as independent, and unlocks the gate to `accepted` / `rejected` / `superseded`.
Dual-Review across structural independence is Cairn's stated differentiator; the
checker that reports on it credits *a difference of names* as *proof of
independence*, which is the same denylist mistake the module's own comment
warns against for humanity. This defect is **not fully fixed here** — see
*Residuals*, R3 — but it is measured, recorded, and partially closed rather than
left for someone to find later.

### Why it matters beyond this repository

`templates/skills/_lib/lifecycle_planner.py` is a shipped template. It is
byte-identical to `tools/lifecycle_planner.py` (both `sha256:45c5c0ed…`,
`as_of 2026-08-03`), carries a `verbatim: true` row in
`dev/.cairn/cairn-lock.yml`, and `bootstrap/scaffold.py --manifest` lists the
pair as `verbatim`. Every adopter inherits all three defects with their own
roster. Cairn is pre-first-external-adopter today, which is precisely why this
is cheap now and expensive later.

## Proposal

### The design rule

The Decision's invariant — *dropping a character must never widen authority* —
is addressed here by removing the deletions that can widen it, rather than by
adding a check that catches violations after the fact:

> **No letter and no digit is ever dropped, in any script.** The fold deletes
> exactly two things: ASCII punctuation, and combining marks. Every letter and
> every digit, in every script, survives into the comparison key.

Under that rule the Cyrillic `a` in the spoof does not vanish — it stays in the
key, the key is not `claude`, the key is not a rostered name, and the byline
classifies `unknown`, which is already a flagged violation. That result holds
because the deletion that produced the widening no longer happens, not because a
second rule noticed it.

**What this does not amount to, stated here rather than only in the residuals.**
The fold still deletes *something* — ASCII punctuation and combining marks — so
the invariant is not literally unviolatable by construction; it is enforced for
the character classes that carry a name's identity, which is the class the
demonstrated exploit used. The one surviving widening is
accent-and-case-equivalence (`José` ≡ `Jose`), and the argument that it grants no
authority beyond what `R1` already concedes is **a claim, not a proof** — it is
carried as residual **R2** with a mechanical retirement trigger (one
counterexample). A reader who wants the strongest version of the design's
weakness should read R2 before the *Rationale*.

### The change, concretely

**1. One fold, at two strengths, chosen by which way an error runs.**

```python
_ASCII_WS_RE = re.compile(r"[ \t\r\n\v\f]+")

def _fold_word(raw: str, form: str) -> str:
    """Fold one display-name word to a comparison key.

    Case-fold, decompose (`form`), drop combining marks, and delete **only
    ASCII punctuation**.  Every surviving letter and digit, in every script,
    is KEPT -- so a confusable letter cannot be deleted into a match.  The
    two deletions that remain (ASCII punctuation, combining marks) are the
    accepted residual; see R2."""
    d = unicodedata.normalize(form, unicodedata.normalize(form, raw).casefold())
    d = "".join(c for c in d if not unicodedata.combining(c))
    return "".join(c for c in d
                   if ord(c) > 0x7F or ("a" <= c <= "z") or ("0" <= c <= "9"))

def _flag_words(name: str) -> tuple:
    """Words at FLAGGING strength (NFKD): over-folding here over-flags."""
    ...  # _fold_word(p, "NFKD") for each ASCII-whitespace-separated word

def _grant_words(name: str) -> tuple:
    """Words at GRANTING strength (NFD): over-folding here would grant."""
    ...  # _fold_word(p, "NFD") for each ASCII-whitespace-separated word
```

The two strengths are the one genuinely non-obvious decision, so it is stated
plainly. `NFKD` is *compatibility* decomposition: it collapses presentational
variants — mathematical bold, circled letters, full-width forms — onto their
plain letters. `NFD` is *canonical* decomposition only: it separates a letter
from its accents and nothing else.

* The **AI registry match** and the **independence comparator** use `NFKD`. An
  error there is an *over-flag* — a spurious, human-reviewable violation. That
  is the direction `tools/lifecycle_planner.py:263` already declares safe.
* The **human-Maintainer allowlist match** uses `NFD` on **both** sides. An
  error there *grants* authority. `NFKD` would additionally admit a small exotic
  class — full-width and squared-unit glyph sequences that fold to a rostered
  name without rendering as it; the measured counterexample is in *Alternatives
  considered*.

Both strengths keep every non-ASCII character, and both are applied
**identically to the roster entry and to the byline**. Tokenization splits on
**ASCII whitespace only**, so a non-ASCII separator stays inside its word rather
than acting as an invisible word break.

**2. Matching becomes symmetric and exact.** `_load_human_maintainers` folds
each roster entry to a *tuple of words* with `_grant_words`;
`IdentityModel.classify` folds the byline the same way and asks for **tuple
equality**, replacing the per-word set intersection at
`tools/lifecycle_planner.py:314`. This is [IDN3]'s recommended narrow
correction — *"store complete allowed display names, normalize symmetrically"* —
taken literally. Exactness, not containment, is what closes defect (a) in its
general form: a byline that contains a rostered name plus anything else no
longer matches, whether the "anything else" is a disguised agent name, a
misspelling, or a digit substitution.

**3. The AI leg keeps its prefix match and its precedence.** `ai` is still
tested first, and a registry entry still matches as a *prefix* of a word so
versioned bylines (`Claude-3.5` → `claude35`) resolve. Config-supplied registry
entries fold through `_flag_words` too, so the extension mechanism is symmetric
with the built-ins.

**4. The live roster is corrected in the same commit.**
`dev/.cairn/agent-identities.json` moves from `["Anthony", "Kendall"]` to
`["Anthony Kendall"]`. This is not optional cleanup: under exact matching the
current two-token value matches no full-name byline, so the code change and the
config change are one atomic change or Cairn's own record starts flagging.

**5. The `unknown` violation message becomes actionable.** Two additions, both
message-only:

* it states that a roster entry must be the **complete display name as it
  appears in the byline** — the migration instruction for defect (b);
* when the byline contains any character outside ASCII, it appends the
  Python-escaped form, so a reader can *see* that `Cl…ude` and `Claude` are not
  the same string. A flag the reader cannot interpret is half a flag.

### What this proposal deliberately does not touch

Fenced explicitly, because the parent's failure was one artifact carrying four
gate sets:

* **`bootstrap/_scaffold/` — untouched.** No engine change, therefore **no AST
  re-anchor obligation and no Bandit engine gate**. The `ast-attest-verify` gate
  command scopes to `bootstrap/_scaffold/*.py`; nothing in scope matches it.
  Stated because omitting it drew a BLOCKING finding on the parent.
* **The consuming policy is unchanged.** What `_conformance_violations` and
  `_gating_preconditions` *do* with a classification — which states require a
  review, which gate credits independence — is a different contract. Changing
  the independence gate soundly needs a *reviewer*-identity roster, and the only
  human list that exists is `human_maintainers`, which confers Decision
  authority. Reusing it to credit review independence would couple two
  authorities to buy one fix. That is R3, not this proposal.
* **The four parsing functions `planner-line-semantics` claims** —
  `_parse_status`, `_parse_field`, `_parse_sections`, `_has_isolated_blockquote`
  — are not touched.
* **No new config key, no schema change** to `agent-identities.json`. The two
  existing lists keep their meaning; only the *granularity* of a
  `human_maintainers` entry changes, from name-fragment to complete display
  name.

### Residuals, each with an expiry trigger

Per the Decision's second anti-debt condition, reusing the dated-posture pattern
from `gate-reanchor-preflight`: **a residual with a named trigger is a decision;
a residual without one is debt.** These are proposed for ratification in this
proposal's Decision, and — following that plan's precedent — the expiry rows
land in `dev/PLANNING.md` at **plan-open**, not at archive, so they outlive this
proposal's readership.

* **R1 — the exact-name spoof.** Anyone who can write bytes into the artifact
  can write the rostered display name exactly. The tool attests structure; the
  operator guarantees authorization. Not fixed, and not fixable by any name
  matcher. Accepted **as dated**: single-maintainer, roster size 1,
  as of 2026-08-03.
  **Expiry — mechanical:** the roster gaining a second entry. **Expiry —
  non-mechanical:** successor scope 1 landing a signing trust root that can bind
  a Decision-introducing commit to a verified signer, at which point this
  classifier should be re-decided as a lint over an authenticated signal rather
  than the thing standing in for one. **Backstop:** re-state or re-decide at
  2027-02-03.

* **R2 — presentation-fold equivalence.** `NFD` + combining-mark stripping +
  case-folding makes accent- and case-variants of a rostered name match it
  (`José` ≡ `Jose`). This *widens* the set of strings that classify `human`.
  The claim made for it — and it is a claim, not a proof — is that it adds no
  authority beyond R1: every member of the class **reads** as the rostered name
  to a human (it differs only in case and diacritics), and anyone able to write
  the variant could write the plain form. Accepted on that basis.
  **Expiry — mechanical:** the first demonstrated string that folds to a
  rostered name and does **not** read as it. One counterexample retires the
  posture; the regression test that enumerates the fold's equivalence classes
  is where it would surface.

* **R3 — the independence widening (defect c), partially closed.** The
  `NFKD` comparator newly catches the combining-mark, mathematical-bold and
  enclosed-letter variants (**3 of 4** measured cases). The **Cyrillic-homoglyph
  variant remains open**: a self-review still satisfies the `independent_review`
  gate. Not fixed here because every sound fix needs a reviewer-identity
  contract that does not exist, and inventing one here is the bundling this
  lineage was split to avoid.
  **Expiry — mechanical:** the first `## Review` in this repository authored by
  a human who is not the Maintainer. That is the event that makes the gate load
  bearing, and it is visible in the artifact itself. **Expiry —
  non-mechanical:** the appearance of *any* durable list of people who may review
  but may not decide. Successor scope 4 is the plausible origin — it opens the
  front door a contributor arrives through — but **scope 4 as drafted lands no
  such list** (verified against its draft, 2026-08-03: `CONTRIBUTING.md`,
  `SECURITY.md`, `README.md`, one profile comment), so this is named as a place
  the need may surface, **not** as work scope 4 has claimed. **Backstop:**
  2026-11-03; if neither trigger has fired, this is re-stated or opened as its
  own proposal.

* **R4 — the flag is not a detector.** A homoglyph byline classifies `unknown`,
  which is flagged, but nothing tells the reader that a *confusable* was the
  reason rather than an unconfigured roster. The escaped-form addition (change 5)
  narrows this to a readable diagnostic inside one message; it is not detection,
  and it does not cover the planner's other byline-bearing output.
  **Expiry:** when `agent-context-scrub` lands its escaping helper, this call
  site adopts it rather than keeping a second escaper; if that proposal is
  rejected or deferred, this residual returns as a scoped follow-up. Either way
  the trigger fires at that proposal's Decision.

* **R5 — a behaviour change for any adopter with a token-style roster.** After
  this change a roster of name *fragments* matches no full-name byline. Blast
  radius today is Cairn itself (corrected in the same commit) and **zero
  external adopters** (v0.3, pre-first-adopter). It ships in the next release.
  **Expiry:** the v0.4.0 release notes. If v0.4.0 ships without the
  behaviour-change entry, this residual is unresolved; if an adopter exists by
  then, an upgrade note is required instead of a release note.

* **R6 — `dev/.cairn/agent-identities.json` has no documented home.** It is read
  by shipped code, created by no installer (verified: it appears in no scaffold
  manifest row), and described only in a code comment and a violation message.
  An adopter learns it exists by triggering a violation.
  **Routing, corrected against the sibling draft rather than assumed.** The
  parent's Part 4 carried *"name the roster's home"*, so successor **scope 4**
  was the natural destination — but scope 4 as drafted (read 2026-08-03)
  **narrows itself to exclude it**: its `Touches` line is `CONTRIBUTING.md`,
  `SECURITY.md`, `README.md` and one `dev/.cairn/profile.yml` comment, and its
  header explicitly fences everything else. The reversion clause is therefore
  **already live at drafting time**, not a contingency, and this residual is
  stated in its reverted form so no one reads it as parked in someone else's
  scope. Scope 4's *Cross-lineage collisions* section records the same fact from
  its side.
  **Expiry:** a trivial-class documentation commit — one sentence in
  `bootstrap/UPGRADE.md` or the adopter-facing skills documentation naming the
  file, its shape, and who writes it — **no later than v0.4.0 release
  preparation**, which is the last point before the file could be inherited by an
  adopter who has no way to learn of it. Discharged early, at no cost, if scope 4
  is broadened at its own Decision to take it back.

### Cross-proposal collisions and the gate batch

**`planner-line-semantics` — same module, disjoint functions, no ordering
dependency.** That proposal edits `_parse_status`, `_parse_field`,
`_parse_sections` and `_has_isolated_blockquote`; this one edits the identity
helpers and `IdentityModel.classify`. No shared function, no shared line, no
merge conflict, and either order lands. What the collision creates is a **review
obligation**, discharged by the joint sitting that proposal proposes: this one
must not be reviewed as though `str.splitlines()` were still bounding its input
alphabet.

That proposal also raised a correction against the Amendment's recipe, and it is
adopted here — with a note that this design reaches the same place by a different
route. Its point was that poisoning only *letters* leaves `U+2028` (category
`Zl`, not a letter) to be deleted by the ASCII fold, converting a non-roster
byline into a roster one. **Measured, with the character built as `chr(0x2028)`:
under the Amendment's letters-only rule that byline classifies `human`; under
this proposal's design it classifies `unknown`** — not because a wider poison
rule catches it, but because the character is never dropped in the first place.
The same holds for `chr(0x2029)`, `chr(0x00a0)`, `chr(0x2000)`, `chr(0x3000)`,
`chr(0x200b)` and `chr(0x00ad)`, all verified `unknown`.

**The active gate batch.** `bootstrap/tests/**/*.py` is inside the frozen
surface of the live gate batch (`162` frozen files, manifest schema
`cairn-gate-manifest/v1`, `as_of 2026-08-03`). Verified, file by file:
`bootstrap/tests/test_lifecycle_contract.py` is **frozen**; `tools/lifecycle_planner.py`,
`templates/skills/_lib/lifecycle_planner.py` and `dev/.cairn/agent-identities.json`
are **not**. So the code and config changes are unconstrained, and the test work
produces exactly **one** `FROZEN-MODIFIED` entry — the single existing node this
change invalidates — plus `FROZEN-NEW` entries for a new test module, which
`bootstrap/tests/_gate_manifest.py:366` records as allowed. Implementation
therefore waits on the batch closing or on that one modification being admitted
to it. This is a live invariant to re-check at plan time, not a carried-forward
claim.

**Shared serialization points.** The twin pair carries a `verbatim: true`
lockfile row whose `hash` re-records when either side changes; all three
proposals in this cohort touch it. That is churn and a serialization point, not
risk.

### Documentation / doctrine surface

* **In-code (descriptive layer)** — the `_fold_word` docstring above, the
  two-strength rationale, and a revision of the identity-model comment block at
  `tools/lifecycle_planner.py:180` so it states what a roster entry now is. This
  is the only place the config's grammar is written down, which is R6.
* **`CHANGELOG.md`** — a behaviour-change entry under `Unreleased`, per R5.
* **No `doctrine/` change. No `AGENTS.md` change. No new template, no
  install-manifest entry, no schema change.** The shipped twin's *content*
  changes; the set of installed files does not.

### Doctrine-change rate-limit

**Not applicable.** This proposal changes no rule, process, or contract that
every contributor follows. It is a defect fix in code plus its tests, plus one
config value. Should a reviewer judge the roster-entry granularity change to be
a contract change rather than a defect fix, the gate is satisfiable on the
**high-risk limb** — the Maintainer's own Decision classifies this scope as a
security fix with a demonstrated exploit — rather than on recurrence.

## Rationale

**Which user workflow does it improve?** The postdoc's, on the daily path. The
planner is what tells a first-time adopter whether their record is in a sound
state. Today an adopter who configures the obvious thing — their full name —
gets every Decision flagged as an unrecognized identity and no instruction that
would fix it; an adopter who configures the thing that works silently grants
Maintainer recognition to anyone sharing one name fragment. Both are wrong in
the first hour of use.

**What contract does it preserve or clarify?** The three-way positive identity
model of `doctrine/lifecycle-contract.md`: the tool reports a missing
attestation and never asserts a valid one. Today it asserts a valid one for a
byline whose only claim to humanity is a character that got deleted. This change
does not add a claim; it removes a false one.

**Reproducibility / correctness?** The record is Cairn's product. A classifier
whose answer depends on a character no reader can see makes the record's
attestations non-reproducible across readers — the file says one thing to
`grep`, another to a human, and a third to the checker.

**Why now?** Three timing-bound reasons. The exploit is demonstrated and on the
record, so the window between knowing and fixing is itself the exposure. The
roster is size 1 today, which makes the config correction free and makes it
expensive the moment a second name is added. And the change ships in the next
release: fixing it before v0.4.0 costs a changelog line, fixing it after costs
an upgrade note against installed trees.

**Why this tier — `required(External, security lens)`.** Three reasons, and the
first is the strongest. (i) I am **not proposing the recipe the Amendment
proposed.** The Amendment specified ASCII-deletion plus a poison rule; this
proposal keeps the characters instead. That deviation is the whole change, and
its author is the same author who — as this lineage records in its own Response —
found a class of defect at 07:59 and then wrote two fresh instances of that
identical class within the hour. Vigilance did not catch it; an adversarial
reader did. (ii) The surface is a shipped template with a demonstrated exploit.
(iii) The specific judgment a reviewer must make — *is the kept/dropped partition
exhaustive, and is `NFD`-for-granting / `NFKD`-for-flagging the right split?* — is
a Unicode-semantics question where a same-type reviewer inherits my blind spots
exactly. The mechanical check the parent lifecycle recommended applies and is
easy to state here: **for the classifier, name every character class the fold
deletes, and show that none of them carries identity.**

## Alternatives considered

* **Do nothing.** Not defensible. The exploit is demonstrated, on the record,
  and in a shipped template.

* **The Amendment's own recipe: `NFD`, strip combining marks, then treat any
  surviving non-ASCII letter as a poisoned token classifying `unknown`.**
  Tested, and rejected on measurement. Two findings.
  *First*, the letters-only wording is unsound, as `planner-line-semantics`
  argued: `U+2028` is a separator, not a letter, so it survives the poison test
  and is then deleted by the ASCII fold. Measured `human` under that rule.
  *Second*, widening the poison to **any** surviving non-ASCII character fixes
  that but carries a real price. Against a 23-name synthetic corpus of realistic
  international bylines, each rostered under its own name, the poison rule flags
  **12 of 23** — including every name using a non-decomposable Latin letter
  (`Ł`, `Ø`, `þ`, `ð`, `ß`, `Đ`, dotless `ı`), every name in a non-Latin script,
  and two names carrying ordinary typographic punctuation. The design proposed
  here flags **0 of 23** while producing the *same* answer on every security case
  in the table below. The Amendment's stated honest cost is therefore real, and
  it is avoidable — which is a better outcome than recording it.

* **`NFKD` for the human allowlist too** (one strength everywhere). Rejected on
  a measured counterexample. The full-width byline
  `chr(0xff21)+"nthony "+chr(0xff2b)+"endall"` compatibility-folds to
  the rostered name and classifies **`human`** under `NFKD`, `unknown` under
  `NFD`. `NFKD`'s compatibility mappings include sequences — squared-unit glyphs,
  ligatures — that spell a name without rendering as it, and that class is not
  enumerable by inspection. Using `NFKD` only where an error over-flags keeps its
  benefit (`𝐂laude` and `Ⓒlaude` now classify `ai` rather than `unknown`) without
  putting it on the granting path.

* **Symmetric matching alone, without changing the fold** (the pre-Amendment
  scope 2). Insufficient, and this is worth stating because it was the accepted
  plan for most of the parent lifecycle: with exact matching but today's
  ASCII-deleting fold, `"Anthony" + chr(0x430) + " Kendall"` still folds to the
  rostered name and classifies `human`. Symmetry closes the over-match; only the
  fold closes the invariant.

* **Containment matching** — accept a byline that *contains* a rostered name as
  a contiguous run of words. Considered, and rejected as the more natural-looking
  but weaker rule: it would accept the scribing byline `Claude scribing for
  Anthony Kendall` on its human leg, so any perturbation of the agent name — the
  homoglyph, `Cl4ude`, or the plain misspelling `Cluade`, all measured `human`
  today — would still classify `human`. Exactness is what makes the AI leg's
  precedence load-bearing instead of decorative.

* **A confusables / skeleton table (UTS #39).** The principled detector, and
  rejected on the dependency budget: it needs confusables data Python's standard
  library does not ship, and `bootstrap/DEPENDENCY_BUDGET.md` puts adopters at
  zero runtime dependencies. Fail-closed on unrecognized characters gets the
  security outcome without the data.

* **Fix the independence gate here too** (defect c in full). Rejected as a
  second contract; see R3.

## Evidence / verification plan

Every figure below was produced by execution on 2026-08-03 under the canonical
interpreter (`~/conda_envs/lhm/bin/python`, 3.13.13), against the live tree at
`71abeb4` and against a `git archive HEAD` sandbox with the design applied to
both twins. Reproducers are stated so a reviewer can re-run them rather than
trust a summary.

**The behaviour table**, roster `["Anthony Kendall"]`. Confusables written as
`chr(...)` and never as literals:

| byline | today | proposed |
|---|---|---|
| `Anthony Kendall` | human | human |
| `Anthony` | **human** | unknown |
| `Kendall Jenner` | **human** | unknown |
| `Kendall Smith` | **human** | unknown |
| `Anthony Kendall Jr` | **human** | unknown |
| `Jane Doe` | unknown | unknown |
| `Claude Opus 5` | ai | ai |
| `Claude scribing for Anthony Kendall` | ai | ai |
| `"Cl"+chr(0x430)+"ude scribing for Anthony Kendall"` | **human** | unknown |
| `Cl4ude scribing for Anthony Kendall` | **human** | unknown |
| `Cluade scribing for Anthony Kendall` | **human** | unknown |
| `"Anthony"+chr(0x430)+" Kendall"` | **human** | unknown |
| `"Anthony"+chr(0x2028)+"Kendall"` | **human** | unknown |
| `"Anthony"+chr(0x00a0)+"Kendall"` | **human** | unknown |
| `chr(0xff21)+"nthony "+chr(0xff2b)+"endall"` (full-width) | unknown | unknown |
| `"Cl"+chr(0x430)+"ude Opus 5"` | unknown | unknown |
| `Cláude Opus 5` | unknown | **ai** |
| `𝐂laude Opus 5` | unknown | **ai** |
| `Ⓒlaude Opus 5` | unknown | **ai** |
| `""` | unknown | unknown |

Every row that today reads `human` and should not now reads `unknown`, which is
a flagged violation. No row moves toward silence.

**Live-corpus regression: zero.** Parsing every `## `/`### ` section heading in
`dev/proposals/` and `dev/plans/`, live and archived, gives `116` byline
occurrences over `12` distinct names, `as_of 2026-08-03`. Under the proposed
fold *and* the corrected roster, **0 of 12** change classification. The four real
identities (`Anthony Kendall`, `Claude`, `Codex`, `Gemini`) classify exactly as
they do today.

**International-name cost: zero, and this is the claim most worth checking.**
Against the 23-name corpus, each rostered under its own name: proposed design
flags **0 of 23**; the Amendment's poison recipe flags **12 of 23**;
its letters-only variant flags **10 of 23**. Sample keys under the granting
fold: `Łukasz Nowak` → `('łukasz','nowak')`, `Ольга Иванова` →
`('ольга','иванова')`, `张伟` → `('张伟',)`, `José García` → `('jose','garcia')`.
The Amendment named this cost and asked for it to be recorded rather than
discovered; measurement says it is avoidable, so what is recorded is its
absence and the design decision that removed it.

**Suite impact: exactly one existing node.** In a `git archive HEAD` sandbox with
the design applied to both twins and the roster corrected: `1545 passed,
1 skipped`, with `10` failures of which `9` reproduce identically in an
*unpatched* sandbox (they need a real git tree that `git archive` does not
provide) — baseline confirmed by a separate clean-sandbox run. The single delta
is the node `test_identity_model_is_three_way_positive_human`, in
`bootstrap/tests/test_lifecycle_contract.py`,
which asserts `classify("Anthony (Maintainer)") == "human"` against a roster of
`["Anthony"]`. **That assertion is the over-match defect written down as an
expectation** — a name fragment plus a parenthetical role matching the
allowlist — and it is also an input shape real parsing never produces, since
`_HEADER_RE` captures the role separately from the name. It is updated, not
worked around. `test_lifecycle_cli.py`, `test_notice_install.py` (including the
twin byte-parity node) and `test_skills_upgrade.py` pass unchanged; `cmp`
confirms the twins stay byte-identical.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.**
  * *No identity-bearing character is dropped.* Enforced by a test that asserts
    the fold's output preserves every input character in Unicode categories
    `L*` and `N*`, over a generated sample spanning Latin-1, Latin Extended-A/B,
    Greek, Cyrillic, Han, Arabic, Thai and the mathematical alphanumerics.
    This is the invariant the Decision named, stated so it can fail.
  * *Roster and byline fold through the same function.* Enforced by a test that
    calls `classify(x)` with roster `[x]` over the 23-name corpus and asserts
    `human` for every entry — symmetry made falsifiable.
  * *Exactness.* Enforced by the behaviour table above as a parametrized test.
  * *Twin byte-parity.* Enforced by the existing node
    `test_every_self_hosted_twin_stays_byte_identical_to_its_source`.
* **Failure modes — all closed.** An unrecognized byline classifies `unknown`,
  which is a violation. An absent, unreadable or wrong-shape config yields an
  empty allowlist, so no byline can be confirmed human — the existing fail-closed
  posture, unchanged. A config entry that folds to nothing is skipped rather than
  matching everything. There is **no open failure mode introduced**, and one
  intentional *narrowing* is worth naming: a byline whose non-ASCII form differs
  from the rostered form (`O’Brien` rostered as `O'Brien`) fails to match and is
  flagged. That is a false positive in the safe direction, resolved by rostering
  the exact form.
* **Edge-case inventory.** Handled: empty byline; whitespace-only byline;
  single-word names; roster entries with leading/trailing whitespace; multi-word
  names; word-count mismatch; case variation; accent variation; non-Latin
  scripts; the eight non-ASCII separators; zero-width and soft-hyphen
  characters; full-width and mathematical-alphanumeric forms; versioned agent
  bylines. **Out of scope, stated rather than implied:** confusable *detection*
  (R4); reviewer-identity independence (R3); anything an authenticated signal
  would settle (R1).
* **Public-path → test mapping.** The public entry point this change affects is
  the planner's conformance report for a terminal proposal state, reached
  through `IdentityModel.classify`. It is exercised through its public path by
  the existing terminal-Decision tests in
  [`test_lifecycle_contract.py`](../../bootstrap/tests/test_lifecycle_contract.py),
  extended with the table above rather than by helper-level assertions only. The
  new-file node names are deliberately not written here — naming them now would
  be a forward reference I cannot verify, and the parent lifecycle already made
  that mistake once.
* **Known omissions.** I have not swept `tools/lifecycle.py` or the checkers
  under `scripts/` for the same bare-`re.sub` normalization pattern; that sweep
  is not claimed as covered. I have not measured the fold against a real
  multilingual name corpus — the 23-name set is synthetic and chosen to span the
  failure classes, not sampled. And the `NFD`-granting choice rests on my
  enumeration of `NFKD`'s compatibility mappings being *representative*, not
  exhaustive; that is precisely the claim the External security lens is being
  asked to break.

### Tests required

`bootstrap/tests/` gains, in a **new module** so the frozen surface takes
`FROZEN-NEW` rather than `FROZEN-MODIFIED` entries: the parametrized behaviour
table; the character-preservation invariant test; the roster-symmetry test over
the international corpus; the independence-comparator test recording which
variants close and which remains open (R3, asserted as a *known* residual so it
cannot regress silently); and a config-migration test asserting that a
token-style roster no longer matches a full-name byline and that the violation
message says how to fix it. One existing node is updated, as described above.

### Examples / smoke checks

`python -m pytest bootstrap/tests` (full suite, canonical interpreter);
`python tools/lifecycle_planner.py scan` from inside the checkout, showing the
live record's conformance unchanged; `cmp` of the twin pair;
`python bootstrap/scaffold.py --manifest` showing the install set unchanged;
`python scripts/check_cairn.py` for the prose and changelog changes; and
`python scripts/claim_check.py` on this proposal.

## Signals the change is wrong

* **A legitimately-rostered name is flagged.** The 0-of-23 measurement is the
  headline claim; one real counterexample falsifies it. *Recovery:* the fold
  keeps characters rather than dropping them, so a counterexample means a
  *decomposition* is wrong, not that the rule is. Fix the decomposition; do not
  reintroduce deletion.
* **A reviewer exhibits a string that folds to a rostered name and does not
  render as it** — R2's mechanical expiry. *Recovery:* narrow the granting fold
  further (canonical composition without case-folding is the next step down);
  do not widen it.
* **The exact match proves too strict in practice** — a Maintainer who signs
  Decisions in two forms, or with a suffix. *Recovery:* multiple roster entries
  per person, which the list already supports. Do **not** relax to containment;
  that is the alternative measured above as reopening the scribing hole.
* **The two-strength fold reads as too clever to maintain.** If a later reader
  cannot state which strength applies where and why, the abstraction has failed
  even if the behaviour is right. *Recovery:* collapse to `NFD` everywhere,
  accepting that `𝐂laude` classifies `unknown` rather than `ai` — which is what
  it does today, so the collapse is a no-regression retreat.
* **`unknown` proves too noisy on a real adopter tree**, so adopters roster
  loosely to silence it and recreate the over-match by hand. *Recovery:* that is
  a documentation failure, not a matcher failure — it is R6, and its trigger
  already exists.
* **A reviewer shows defect (c) is not separable** — that leaving R3 open makes
  this fix incoherent rather than merely incomplete. *Recovery:* this proposal
  narrows to the classification surface and R3 opens as its own scope with the
  reviewer-identity config change it needs. That is the split working, not
  failing.

## Review -- Gemini Flash (External, Security Review) -- 2026-08-03

**Model**: Gemini 3.6 Flash (External, different-agent-type)
**Verdict**: SHIP (recommend ACCEPT; verified all 3 defects, verified proposed fix robustness against non-decomposing characters and ASCII confusables)

### Steelman

This proposal solves a security-critical defect in `tools/lifecycle_planner.py` (and its twin `templates/skills/_lib/lifecycle_planner.py`) where `re.sub(r"[^a-z0-9]", "", raw.lower())` stripped non-ASCII characters, allowing homoglyphs (such as Cyrillic `а` U+0430) to delete the AI agent token `claude` into `clude`, bypassing the AI registry and over-matching against the human Maintainer allowlist (`Claude scribing for Anthony Kendall` -> `human`). Furthermore, it resolves the roster granularity asymmetry where single-fragment entries in `dev/.cairn/agent-identities.json` either failed to match full names or over-matched arbitrary individuals sharing a name fragment.

The proposed design replaces destructive ASCII-only deletion with a character-preserving, two-strength fold: `NFKD` for AI matching (to catch presentational variants like `Ⓒlaude` or `𝐂laude`) and `NFD` for human allowlist matching, paired with **symmetric, exact tuple equality** for human maintainer names. Because every letter and digit in every script is preserved in the comparison key, confusable characters cannot be deleted into a match, and extra words (like `scribing for`) prevent partial over-matching against rostered human names.

### Concerns and Findings

* **[G1] (Reproduction & Verification of Defects a, b, and c)**
  * **Defect (a) — Cyrillic Homoglyph Flips `ai` to `human`:** Verified by calling `_load_identity_model(Path('.'))`. `"Claude scribing for Anthony Kendall"` classifies as `ai`, while `"Cl" + chr(0x430) + "ude scribing for Anthony Kendall"` classifies as `human`.
  * **Defect (b) — Roster Asymmetry:** Verified using a temporary `agent-identities.json`. When `human_maintainers` is `["Anthony Kendall"]` (full display name), `"Anthony Kendall"` classifies as `unknown`. When `human_maintainers` is `["Anthony", "Kendall"]` (name fragments), `"Anthony Kendall"` classifies as `human`, but `"Anthony"` and `"Kendall Jenner"` also classify as `human`.
  * **Defect (c) — Independence Comparator Homoglyph Bypass:** Verified calling `_identity_token`. `_identity_token("Claude (Internal Review)")` yields `'claude'`, whereas `_identity_token("Cl" + chr(0x430) + "ude (Internal Review)")` yields `'clude'`. Because `'claude' != 'clude'`, a same-agent homoglyph review is not flagged as self-review.

* **[G2] (Falsification & Attack Analysis of Proposed Fix vs. Amendment Poison Rule)**
  * *Attack Evaluation:* Tested the proposed `_fold_word` + exact tuple matching against non-decomposing characters (Cyrillic `а` U+0430, Greek `α` U+03B1, Polish `Ł` U+0141, Fullwidth `ａ` U+FF41, turned e `ǝ` U+01DD, non-breaking space `U+00A0`, line separator `U+2028`) and ASCII-only confusables (`rn` vs `m`, `II` vs `ll`, `11` vs `ll`, `0` vs `o`, `i` vs `l` in `Ciaude`, `1` vs `a` in `Cl1ude`).
  * *Results:* Under the proposed fix, **all 14 attack bylines classify as `unknown`** (flagged violation). The proposed fix holds because:
    1. Exact tuple equality requires `_grant_words(byline) == _grant_words(roster_entry)`. Any extra words in scribing bylines (`scribing for`) or character alterations make tuple equality fail.
    2. Keeping non-ASCII letters and digits ensures characters are never deleted into a match.
    3. `NFKD` on the AI leg successfully maps presentational forms (`Ⓒlaude`, `𝐂laude`) to `ai`.
  * *Comparison with Amendment Poison Rule:* The Amendment's poison rule ("treat any surviving non-ASCII letter as poisoned -> `unknown`") combined with containment matching leaves open over-matching on ASCII-only confusables (`Anthorny Kendall` -> `human`, `Ciaude scribing for Anthony Kendall` -> `human`). The proposed fix's exact tuple matching is vastly superior and eliminates both international false positives and confusable over-matching.

* **[G3] (Residual R3 Acknowledgment & Expiry Trigger)**
  As noted in the proposal, Residual R3 remains partially open: because reviewer-identity lacks a separate roster, `_identity_token` under `NFKD` catches mathematical bold and circled variants but still produces `'clude'` for a Cyrillic homoglyph self-review. R3's expiry trigger (the first human review by a non-Maintainer or a reviewer-identity roster) is appropriate and avoids coupling Decision authority with review independence.

* **[G4] (Gate-Manifest & Frozen-File Batch Window)**
  `tools/lifecycle_planner.py` and `templates/skills/_lib/lifecycle_planner.py` are **unfrozen** in `gate_manifest.json`. `bootstrap/tests/test_lifecycle_contract.py` is **frozen** (`FROZEN-MODIFIED`), so updating its assertion requires supervised re-anchoring or landing outside an active manifest window.

### Covered (Lenses Swept & Verbatim Executions)

All commands executed using canonical interpreter `~/conda_envs/lhm/bin/python` (Python 3.13.13).

1. **Reproduction (a) — Cyrillic U+0430 Homoglyph Flip:**
   * *Command:*
     ```bash
     ~/conda_envs/lhm/bin/python -c "from pathlib import Path; from tools.lifecycle_planner import _load_identity_model; model = _load_identity_model(Path('.')); honest = 'Claude scribing for Anthony Kendall'; spoof = 'Cl' + chr(0x430) + 'ude scribing for Anthony Kendall'; print('honest:', honest, '->', model.classify(honest)); print('spoof:', repr(spoof), '->', model.classify(spoof))"
     ```
   * *Output:*
     ```
     honest: Claude scribing for Anthony Kendall -> ai
     spoof: 'Cl\u0430ude scribing for Anthony Kendall' -> human
     ```

2. **Reproduction (b) — Roster Granularity Asymmetry:**
   * *Command:*
     ```bash
     ~/conda_envs/lhm/bin/python -c "import json, tempfile, pathlib; from tools.lifecycle_planner import _load_identity_model;
     with tempfile.TemporaryDirectory() as tmp:
         p = pathlib.Path(tmp); (p / 'dev' / '.cairn').mkdir(parents=True)
         cfg1 = {'version': 1, 'human_maintainers': ['Anthony Kendall'], 'agent_names': []}
         (p / 'dev' / '.cairn' / 'agent-identities.json').write_text(json.dumps(cfg1))
         m1 = _load_identity_model(p)
         print('Roster [\"Anthony Kendall\"]:')
         print('  \"Anthony Kendall\" ->', m1.classify('Anthony Kendall'))
         print('  \"Anthony\" ->', m1.classify('Anthony'))
         print('  \"Kendall Jenner\" ->', m1.classify('Kendall Jenner'))
         cfg2 = {'version': 1, 'human_maintainers': ['Anthony', 'Kendall'], 'agent_names': []}
         (p / 'dev' / '.cairn' / 'agent-identities.json').write_text(json.dumps(cfg2))
         m2 = _load_identity_model(p)
         print('Roster [\"Anthony\", \"Kendall\"]:')
         print('  \"Anthony Kendall\" ->', m2.classify('Anthony Kendall'))
         print('  \"Anthony\" ->', m2.classify('Anthony'))
         print('  \"Kendall Jenner\" ->', m2.classify('Kendall Jenner'))
     "
     ```
   * *Output:*
     ```
     Roster ["Anthony Kendall"]:
       "Anthony Kendall" -> unknown
       "Anthony" -> unknown
       "Kendall Jenner" -> unknown
     Roster ["Anthony", "Kendall"]:
       "Anthony Kendall" -> human
       "Anthony" -> human
       "Kendall Jenner" -> human
     ```

3. **Reproduction (c) — Independence Comparator Token Match (`_identity_token`):**
   * *Command:*
     ```bash
     ~/conda_envs/lhm/bin/python -c "from tools.lifecycle_planner import _identity_token; t1 = _identity_token('Claude (Internal Review)'); t2 = _identity_token('Cl' + chr(0x430) + 'ude (Internal Review)'); print('t1:', repr(t1)); print('t2:', repr(t2)); print('t1 == t2:', t1 == t2)"
     ```
   * *Output:*
     ```
     t1: 'claude'
     t2: 'clude'
     t1 == t2: False
     ```

4. **Attack Suite — Non-Decomposing Characters & ASCII Confusables on Proposed Fix:**
   * *Command:*
     ```bash
     ~/conda_envs/lhm/bin/python -c "import unicodedata, re
     _ASCII_WS_RE = re.compile(r'[ \t\r\n\v\f]+')
     def _fold_word(raw: str, form: str) -> str:
         d = unicodedata.normalize(form, unicodedata.normalize(form, raw).casefold())
         d = ''.join(c for c in d if not unicodedata.combining(c))
         return ''.join(c for c in d if ord(c) > 0x7F or ('a' <= c <= 'z') or ('0' <= c <= '9'))
     def _grant_words(name: str) -> tuple[str, ...]:
         words = _ASCII_WS_RE.split(name.strip())
         return tuple(_fold_word(w, 'NFD') for w in words if _fold_word(w, 'NFD'))
     def _flag_words(name: str) -> tuple[str, ...]:
         words = _ASCII_WS_RE.split(name.strip())
         return tuple(_fold_word(w, 'NFKD') for w in words if _fold_word(w, 'NFKD'))
     AGENT_NAMES = {'claude', 'codex', 'gemini', 'cairn'}
     def classify(byline: str, roster: list[str]) -> str:
         if not byline.strip(): return 'unknown'
         for w in _flag_words(byline):
             for agent in AGENT_NAMES:
                 if w.startswith(agent): return 'ai'
         if _grant_words(byline) in {_grant_words(r) for r in roster}: return 'human'
         return 'unknown'
     roster = ['Anthony Kendall']
     attacks = [
         ('Anthony' + chr(0x430) + ' Kendall', 'Cyrillic a in Anthony'),
         ('Anth' + chr(0x3b1) + 'ny Kendall', 'Greek alpha in Anthony'),
         ('Łukasz Nowak', 'Polish Ł (non-decomposing stroke)'),
         (chr(0xff21) + 'nthony Kendall', 'Fullwidth Latin A'),
         ('Anthony K' + chr(0x1dd) + 'ndall', 'Latin small turned e ǝ'),
         ('Anthony' + chr(0x00a0) + 'Kendall', 'Non-breaking space U+00A0'),
         ('Anthony' + chr(0x2028) + 'Kendall', 'Line separator U+2028'),
         ('Anthorny Kendall', 'rn vs m'),
         ('Anthony KendaII', 'uppercase II vs ll'),
         ('Anthony Kenda11', 'digits 11 vs ll'),
         ('Anth0ny Kenda1l', 'digit 0 vs o, 1 vs l'),
         ('Ciaude scribing for Anthony Kendall', 'i vs l in Ciaude'),
         ('Cl1ude scribing for Anthony Kendall', '1 vs l in Cl1ude'),
         ('Claurde scribing for Anthony Kendall', 'ur vs u in Claurde'),
     ]
     for b, desc in attacks:
         print(f'{desc:42s} | {classify(b, roster):8s} | {str(_grant_words(b)):40s}')
     "
     ```
   * *Output:*
     ```
     Cyrillic a in Anthony                      | unknown  | ('anthony\u0430', 'kendall')
     Greek alpha in Anthony                     | unknown  | ('anth\u03b1ny', 'kendall')
     Polish Ł (non-decomposing stroke)          | unknown  | ('\u0142ukasz', 'nowak')
     Fullwidth Latin A                          | unknown  | ('\uff21nthony', 'kendall')
     Latin small turned e ǝ                     | unknown  | ('anthony', 'k\u01ddndall')
     Non-breaking space U+00A0                  | unknown  | ('anthony\xa0kendall',)
     Line separator U+2028                      | unknown  | ('anthony\u2028kendall',)
     rn vs m                                    | unknown  | ('anthorny', 'kendall')
     uppercase II vs ll                         | unknown  | ('anthony', 'kendaii')
     digits 11 vs ll                            | unknown  | ('anthony', 'kenda11')
     digit 0 vs o, 1 vs l                       | unknown  | ('anth0ny', 'kenda1l')
     i vs l in Ciaude                           | unknown  | ('ciaude', 'scribing', 'for', 'anthony', 'kendall')
     1 vs l in Cl1ude                           | unknown  | ('cl1ude', 'scribing', 'for', 'anthony', 'kendall')
     ur vs u in Claurde                         | unknown  | ('claurde', 'scribing', 'for', 'anthony', 'kendall')
     ```


### Not Covered / Low Confidence (Negative Space)

* **Code Edits & Sandbox Execution:** The proposal code changes have not been applied to `tools/lifecycle_planner.py` yet; all verification was performed via standalone Python execution against the live tree (`71abeb4`).
* **Third-Party Confusables Database:** No third-party Unicode confusable skeleton database (e.g. TR39) was used, as Cairn maintains a zero-runtime-dependency budget for adopters.

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

*(Awaiting the Maintainer. The proposal has cleared External Security Review. The Maintainer may accept the proposal to proceed with plan creation.)*

## Response -- Claude (author, to External Security Review) -- 2026-08-03

**Model**: Claude Opus 5. Proposal-Response grammar (no implementing commits
exist).

**Two accepted as reproduced, one narrowed, one corrected. No design change,
so the status stays `reviewed`.** Every finding was re-verified by execution
before disposing, not accepted on the reviewer's report — this lineage has
already recorded one review whose evidentiary claims did not survive re-running,
and a `SHIP` verdict does not move a proposal by itself. What I ran: the
review's three reproduction commands verbatim under the canonical interpreter
(`~/conda_envs/lhm/bin/python`, 3.13.13); its 14-case attack harness, re-run
with the *real* 13-entry AI registry in place of its 4-name stand-in; an
independent 23-name international corpus against **both** this design and the
recipe the review compared it to; the independence comparator over four
byline variants; and the frozen-file membership of all four touched paths
against `bootstrap/tests/fixtures/gate_manifest.json`.

One preliminary, because the review's figures are pinned to a commit the tree
has since left. The review measured against `71abeb4`; `HEAD` is now `292e2c6`
(`as_of 2026-08-03`). `git diff --stat 71abeb4 HEAD` over the four touched
paths — `tools/lifecycle_planner.py`, its twin, `dev/.cairn/agent-identities.json`
and `bootstrap/tests/test_lifecycle_contract.py` — is **empty**, so every
figure below still stands at `HEAD`. The twins remain byte-identical
(`sha256:45c5c0ed…`, both files, `shasum -a 256`, 2026-08-03), as the proposal
claims.

* **[G1] accept -- all three defects reproduce verbatim, including the one the
  review re-derived rather than copied.** Defect (a): the review's command
  returns `ai` for the honest byline and `human` for `"Cl" + chr(0x430) +
  "ude scribing for Anthony Kendall"` (`chr(0x430)` is CYRILLIC SMALL LETTER A,
  which renders identically to ASCII `a`). Defect (b): with a temporary roster
  I get `{'anthonykendall'}` as the whole-entry key and `unknown` for all four
  bylines, then `{'anthony','kendall'}` and `human` for all four — including
  `Kendall Smith`, which the review did not test and which also over-matches.
  Defect (c): `_identity_token` yields `'claude'` against `'clude'`. One nit
  recorded so nobody reuses the snippet as a template: the review's temporary
  config sets `agent_names`, but the loader reads `ai_agents`
  (`tools/lifecycle_planner.py:222`), so that key was inert. It is harmless
  here — the config can only *extend* the registry, never shrink it, and no
  test byline touches the AI leg — but a reader copying it would silently
  configure nothing.

* **[G2] narrow -- the falsification result reproduces and I accept it; the
  comparison that frames it is against a composite the Amendment never
  proposed.** The result first, because it is the finding's substance and it
  holds: re-running the harness gives `unknown` on all 14 attack bylines, and it
  still gives `unknown` when the 4-name `AGENT_NAMES` stand-in is replaced by
  the real 13-entry `_AI_AGENT_REGISTRY`, which is a stronger check than the one
  reported. The narrowing is on the comparative claim. The review pairs the
  Amendment's poison rule with **containment matching** and concludes the
  proposed fix is "vastly superior"; but the Amendment's own second item asks to
  fix the whole-string / per-token asymmetry *"so a full-name roster entry is
  configurable and a partial token is not"* — that is exactness, the same rule
  this proposal takes. Measured, Amendment fold (`NFD`, strip combining marks,
  poison any surviving non-ASCII letter) plus its own item-2 exactness: **0 of
  14 attack bylines reach `human`**, identical to this design. So exactness is
  not the delta between the two designs; both have it. The delta is the
  international-name cost — on an independently-built 23-name corpus, each name
  rostered under itself, this design flags **0 of 23** and the Amendment recipe
  flags **17 of 23** (`Łukasz Nowak`, `Ольга Иванова`, `张伟`, `Søren
  Kierkegaard`, …). Direction agrees with the proposal's `12 of 23`; the
  magnitude does not, because the two corpora are different synthetic sets, and
  that is itself a finding against my own evidence (see the carries below). Two
  smaller narrowings on the same bullet. The review attributes the elimination
  of international false positives to *exact tuple matching*; the measurement
  above says it comes from the character-preserving fold — exactness is
  indifferent to script. And "eliminates confusable over-matching" is true only
  in the direction that matters for authority: confusables stop reaching
  `human`, but they classify `unknown`, which is flagged at the one site that
  consumes a classification (`tools/lifecycle_planner.py:613`, where both `ai`
  and `unknown` raise a violation, verified as the only `classify` call site).
  The tool still cannot tell a reader that a *confusable* was the reason rather
  than an unconfigured roster, and `Ciaude` is still not recognized as an agent
  name. That gap is R4 and R1, unchanged by this review.

* **[G3] correct -- the conclusion is right and I keep it; the mechanism stated
  for it describes today's code, not the proposed fold.** R3 does stay open for
  the Cyrillic case, and the reasoning that reviewer-identity and Decision
  authority must not be coupled to close it is exactly the argument the proposal
  makes. But the finding says the proposed `_identity_token` "still produces
  `'clude'` for a Cyrillic homoglyph self-review." It does not. Under the
  proposed fold nothing is dropped, so the key is `'cl' + chr(0x430) + 'ude'`
  — seven characters, not five. It fails to match the author key `'claude'`
  because it contains a *different letter*, not because a letter vanished. The
  security outcome is identical (the self-review is still not flagged, the
  `independent_review` gate is still met), which is why the disposition is a
  correction and not a rejection — but the distinction is load-bearing for this
  proposal specifically, whose entire design rule is that no letter is ever
  dropped. A Decision that adopted the finding's wording verbatim would record
  the fixed code as still deleting the character it was changed to keep.
  Measured, author `Claude (Strategy)`, reviewer variants under the proposed
  `NFKD` comparator: precomposed accent → `'claude'`, **flagged** (today:
  `'clude'`, not flagged); mathematical-bold `C` → `'claude'`, **flagged**
  (today: `'laude'`); circled `C` → `'claude'`, **flagged** (today: `'laude'`);
  Cyrillic → `'cl' + chr(0x430) + 'ude'`, **not flagged**. That is the 3-of-4
  the proposal claims, confirmed against the proposal's own precomposed
  convention.

* **[G4] accept -- reproduced exactly, and it names a path the proposal left
  implicit.** Against `bootstrap/tests/fixtures/gate_manifest.json` (schema
  `cairn-gate-manifest/v1`, `162` frozen entries, `as_of 2026-08-03`):
  `tools/lifecycle_planner.py`, `templates/skills/_lib/lifecycle_planner.py` and
  `dev/.cairn/agent-identities.json` are **not** frozen;
  `bootstrap/tests/test_lifecycle_contract.py` **is**. A frozen-file edit
  appends a `FROZEN-MODIFIED` **hold** (`bootstrap/tests/_gate_manifest.py:364`)
  while a new frozen-surface file is a recorded note
  (`bootstrap/tests/_gate_manifest.py:366`), which is the asymmetry the
  proposal's test plan is built around. The proposal said implementation waits
  on "the batch closing or on that one modification being admitted to it"; the
  review names the second route concretely as supervised re-anchoring, and that
  mechanism is real and two-staged (`bootstrap/tests/_gate_reanchor.py`).
  Adopted as a plan-time note, not a design change: the choice between waiting
  and re-anchoring is a scheduling decision for plan-open, and it is the
  Maintainer's, since Stage B consumes a promotion authorization.

**Bearing of the Maintainer direction of 2026-08-03 on the default security
stance** — *"we need to change the default security stance for all
installations. Otherwise we are shipping a potentially dangerous tool."* It
bears on this proposal in one narrow way, and I want to state the limit rather
than borrow the direction's weight. This surface is **core, not preset-gated**:
`dev/.cairn/cairn-lock.yml` carries the twin as `src: skills/_lib/lifecycle_planner.py`
with no `modules/` prefix, and `python bootstrap/scaffold.py --manifest` lists
the pair unconditionally (verified 2026-08-03). So the fix reaches every adopter
on install with no preset or profile work — which is precisely what is *not*
true of the module the direction is actually about. Changing which presets
select the content-security module is outside this fence and belongs in its own
proposal over the profile/preset surface; it is currently unowned, since none of
the three in-flight proposals that mention `content-security` —
`content-scan-detectors`, `gate-claims-vs-enforcement`, `scan-coverage` —
contains the word "preset" at all (measured 2026-08-03).

**What this Response does not establish.** The review verified the design
against a standalone re-implementation of the fold, not against edited source —
it says so in its own negative space, and I confirm it: no implementing commit
exists, so nothing here is evidence about the code that will ship. Nothing in
this exchange touches R1 (the exact-name spoof), R3's Cyrillic case, or R4;
`unknown` remains a flag a reader must interpret, not a detector. And a review
that reproduces three defects and finds no counterexample to a fix is evidence
the fix survives *the cases both of us thought to try* — the proposal's own
`Known omissions` (the unswept `re.sub` pattern elsewhere, the synthetic corpus,
the non-exhaustive `NFKD` enumeration) are untouched by this review, and the
third of those is the one it was specifically asked to break.

**Carries to plan-open, from this Response rather than from the review.**
(i) The international corpus must be **committed in the test module**, not
described. My inability to reproduce `12 of 23` — I get `17 of 23` on a corpus I
built to the same description — is not a disagreement about the direction of the
result, it is proof that a figure resting on an unenumerated synthetic corpus is
not reproducible from the artifact, which is the property this repository's
record exists to have. The plan states the corpus by name-list, and the
proposal's `12 of 23` should be read as corpus-specific.
(ii) The rationale for choosing this design over the Amendment's records the
corrected delta — international cost, not attack blocking — so a later reader
does not re-derive the wrong reason for the decision.

## Review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-03

**Model**: Claude Opus 5.

**Verdict**: REVISE. No BLOCKING finding: the design is sound, the direction of
every behaviour change is safe, and it should land. But the proposal asks the
Decision to **ratify residual R2 as written**, and R2's stated justification is
falsified by three independent measured classes ([I1]); two of the three tests
it proposes cannot do the job claimed for them ([I3], [I4]); and change 3
introduces one unnamed failure mode ([I5]). Those are text-and-test changes, not
design changes.

**Note on characters.** This review follows the proposal's own convention: no
confusable or invisible character is written as a literal. Every one is named
`chr(0x...)`, and every measured output below is `ascii()`-escaped, so what you
read is what the interpreter saw. Terms are glossed on first use for a reader
who does not live in Unicode.

**Reproduction note.** Every finding carries the command and its real output.
All runs are under the canonical interpreter (`~/conda_envs/lhm/bin/python`,
3.13.13) with `PYTHONDONTWRITEBYTECODE=1`, at `HEAD` = `af4b2ee`, 2026-08-03.
The proposal's design was transcribed verbatim from its *The change, concretely*
block into a scratch module -- `_fold_word` / `_flag_words` / `_grant_words`
exactly as printed, plus the real 13-entry `_AI_AGENT_REGISTRY` copied from
`tools/lifecycle_planner.py`. I did not edit the repository. That is the same
limitation the External review declared, and it applies here too.

### Steelman

This is the right fix, and it is better than the recipe it replaces.

The core move -- stop deleting characters, and compare complete names -- is the
only candidate design that closes the demonstrated exploit *and* costs nothing
on international names, and the proposal proves both rather than asserting them.
Three of its load-bearing figures reproduce **exactly** when I re-derive them
independently:

* The live-corpus figure `116` byline occurrences over `12` distinct names is
  exact at the commit it was measured against.
* R3's "3 of 4" independence-comparator claim is exact, and the Response's
  correction of the External review's [G3] -- that the proposed token is
  `'cl' + chr(0x430) + 'ude'`, seven characters, not `'clude'` -- is right. The
  reviewer's stated mechanism described today's code, not the fix.
* The frozen-file membership claims hold at `HEAD`.

The design also gets two things right that a weaker version would miss. It puts
`NFKD` (compatibility decomposition, which collapses presentational variants like
mathematical-bold letters onto plain ones) only on the *flagging* leg, where an
error over-flags, and `NFD` (canonical decomposition, which separates a letter
from its accents and nothing more) on the *granting* leg, where an error grants
authority -- and it states the asymmetry rather than hiding it. And normalizing
**both** sides makes the classifier immune to a real, boring failure the proposal
does not even claim credit for: a roster JSON saved in one Unicode normal form
and a markdown byline saved in the other (routine on macOS) now match, where a
byte comparison would not.

The fail-closed posture also survives at the boundary that matters most for a
first adopter. With no config file at all -- the default state, which is R6 --
the allowlist is empty, and under tuple equality an empty key set matches
nothing:

```
$ ~/conda_envs/lhm/bin/python -c "from fold import classify; ... classify(b, [])"
empty roster (no config file -- the default adopter state, R6):
   byline 'Anthony Kendall'    -> unknown
   byline ''                   -> unknown
   byline '   '                -> unknown
   byline 'Claude'             -> ai
```

Finally, the collision claim against the sibling holds *operationally*. I
measured both landing orders and neither is unsafe:

```
order A (this proposal alone; the HEAD parser yields this byline)
    classify('Anthony') -> unknown  key="('anthony',)"
order B (planner-line-semantics landed first; byline built with chr(0x2028))
    classify('Anthony\u2028Kendall') -> unknown  key="('anthony\\u2028kendall',)"
```

---

### [I1] R2's ratification text is falsified at drafting time, by three independent classes

**Severity: the highest here.** This is not a defect in the fold. It is a defect
in the claim the Decision is being asked to ratify.

R2 describes the widening it accepts as *"accent- and case-variants"*, and
defends it with: *"every member of the class **reads** as the rostered name to a
human (it differs only in case and diacritics)."* R2's own mechanical expiry is
*"the first demonstrated string that folds to a rostered name and does **not**
read as it."* Three classes fire that trigger before the proposal lands.

**(1a) `str.casefold()` performs *full* case folding, which puts ligature and
long-s expansions on the NFD granting path** -- the exact class the proposal
says `NFD` keeps off it. The proposal's rationale for `NFD`-for-granting reads:
*"`NFKD`'s compatibility mappings include sequences -- squared-unit glyphs,
**ligatures** -- that spell a name without rendering as it."* True of `NFKD`.
But `casefold()` applies those mappings regardless of normal form, and the fold
calls `casefold()` between its two normalizations.

```
$ ~/conda_envs/lhm/bin/python -c "from fold import _fold_word; ... for cp in [...]"
chr(0x017f)  LATIN SMALL LETTER LONG S                NFD-fold 's'  NFKD-fold 's'
chr(0xfb01)  LATIN SMALL LIGATURE FI                  NFD-fold 'fi'  NFKD-fold 'fi'
chr(0xfb03)  LATIN SMALL LIGATURE FFI                 NFD-fold 'ffi'  NFKD-fold 'ffi'
chr(0xfb05)  LATIN SMALL LIGATURE LONG S T            NFD-fold 'st'  NFKD-fold 'st'
chr(0x00df)  LATIN SMALL LETTER SHARP S               NFD-fold 'ss'  NFKD-fold 'ss'
chr(0x1e9e)  LATIN CAPITAL LETTER SHARP S             NFD-fold 'ss'  NFKD-fold 'ss'
chr(0x00b5)  MICRO SIGN                               NFD-fold '\u03bc'  NFKD-fold '\u03bc'
chr(0x0130)  LATIN CAPITAL LETTER I WITH DOT ABOVE    NFD-fold 'i'  NFKD-fold 'i'
```

`chr(0x17f)` renders as a long `s`; to a modern reader it reads as **`f`**, not
`s`. So, against a roster of `['Kristen Long']`:

```
plain                    'Kristen Long'             -> human    key="('kristen', 'long')"
chr(0x17f) long s        'Kri\u017ften Long'        -> human    key="('kristen', 'long')"
chr(0xfb05) st-ligature  'Kri\ufb05en Long'         -> human    key="('kristen', 'long')"
```

A byline a reader sees as *"Kriften Long"* classifies as the rostered *"Kristen
Long"*. That is R2's expiry condition, met, and it is neither a case nor a
diacritic variant.

**(1b) Combining-mark stripping collapses *letter-distinguishing* diacritics, so
distinct real names become one key.** `unicodedata.combining(c)` is non-zero for
characters that function as accents in Latin but carry **letter identity** in
several other scripts. Measured, granting fold, roster on the left:

```
$ ~/conda_envs/lhm/bin/python -c "from fold import classify, _grant_words; ..."
Vietnamese tone: NGUYEN
    roster 'Nguy\u1ec5n'    key "('nguyen',)"
    byline 'Nguy\u1ebfn'    key "('nguyen',)"
    classify(byline, [roster]) -> human
Japanese dakuten: KA/GA
    roster '\u304b\u3068\u3046'    key "('\u304b\u3068\u3046',)"
    byline '\u304c\u3068\u3046'    key "('\u304b\u3068\u3046',)"
    classify(byline, [roster]) -> human
Devanagari nukta: KA/QA
    roster '\u0915\u093f\u0930'          key "('\u0915\u093f\u0930',)"
    byline '\u0915\u093c\u093f\u0930'    key "('\u0915\u093f\u0930',)"
    classify(byline, [roster]) -> human
Cyrillic YE/YO surname
    roster '\u0415\u043b\u043a\u0438\u043d'    key "('\u0435\u043b\u043a\u0438\u043d',)"
    byline '\u0401\u043b\u043a\u0438\u043d'    key "('\u0435\u043b\u043a\u0438\u043d',)"
    classify(byline, [roster]) -> human

names of the distinguishing characters:
  chr(0x1ec5) = LATIN SMALL LETTER E WITH CIRCUMFLEX AND TILDE
  chr(0x1ebf) = LATIN SMALL LETTER E WITH CIRCUMFLEX AND ACUTE
  chr(0x304b) = HIRAGANA LETTER KA
  chr(0x304c) = HIRAGANA LETTER GA
  chr(0x093c) = DEVANAGARI SIGN NUKTA
  chr(0x0415) = CYRILLIC CAPITAL LETTER IE
  chr(0x0401) = CYRILLIC CAPITAL LETTER IO
```

Gloss. The two Vietnamese forms are different tones, hence different names. The
two hiragana are KA and GA -- different syllables. The Devanagari nukta turns KA
into QA. `chr(0x415)` and `chr(0x401)` are YE and YO, two different Russian
letters, and the two surnames they produce are different surnames. In every case
a **different person's name** now classifies as the rostered Maintainer, and a
reader looking at the byline sees a different name. The Cyrillic case matters
particularly because Cyrillic is a script the proposal's own 23-name corpus
samples.

This is not the same as R1 ("anyone who can write bytes can write the exact
name"). R2's argument was specifically that its class adds nothing beyond R1
*because every member reads as the rostered name*. For these it does not.

**Honest framing, so this is not overstated.** These collisions are only
reachable *because* the fix makes non-Latin rosters work at all -- today an
all-Cyrillic roster entry folds to the empty string and can never match
anything, so the class is unreachable. The widening is the price of the feature,
and I think it is worth paying. What must change is R2's **text**: it describes
a narrower class than the fold produces, and it is being submitted for
ratification.

**Recommended disposition:** restate R2 as *canonical-decomposition equivalence
plus full case folding*, name the three classes, and either accept it with the
counterexamples on the record or re-decide the trigger. Do **not** silently keep
the current wording -- a mechanical expiry that is already satisfied at the
moment of ratification is debt wearing a decision's clothes, which is the exact
failure the Decision's anti-debt condition was written against.

---

### [I2] The fold deletes three character classes, not the two the proposal names

The proposal's design rule is a **partition claim**: *"The fold deletes exactly
two things: ASCII punctuation, and combining marks."* And its *Why this tier*
section names the mechanical check a reviewer should run: *"for the classifier,
**name every character class the fold deletes, and show that none of them
carries identity**."* Run literally, that check fails.

```
$ ~/conda_envs/lhm/bin/python -c "dropped = [cp for cp in range(0x80) if _fold_word(chr(cp),'NFD')=='']"
category Cc:  33 codepoints  0x0..0x7f
category Pc:   1 codepoints  0x5f..0x5f
category Pd:   1 codepoints  0x2d..0x2d
category Pe:   3 codepoints  0x29..0x7d
category Po:  15 codepoints  0x21..0x5c
category Ps:   3 codepoints  0x28..0x7b
category Sc:   1 codepoints  0x24..0x24
category Sk:   2 codepoints  0x5e..0x60
category Sm:   6 codepoints  0x2b..0x7e
category Zs:   1 codepoints  0x20..0x20

total ASCII codepoints deleted by the fold: 66
of which C0 controls / DEL (Cc): 33
```

Two undeclared groups. **C0 control characters and DEL** (`Cc`; five of the 33
are tokenizer separators, so 28 are genuinely deleted mid-word), and **ASCII
symbols** (`Sc`/`Sk`/`Sm` -- dollar, caret, backtick, plus, less-than, equals,
greater-than, pipe, tilde), which are Unicode *symbols*, not punctuation.

Reachability, checked through the real parser rather than asserted -- some C0
characters are eaten by `str.splitlines()` before a byline is ever extracted,
and some are not:

```
$ ~/conda_envs/lhm/bin/python -c "from tools.lifecycle_planner import _parse_sections; ..."
U+2028 (proposal table row)    parsed d.name = 'Anthony'
U+00a0 (proposal table row)    parsed d.name = 'Anthony\xa0Kendall'
C0 US 0x1f                     parsed d.name = 'Anthony Ken\x1fdall'
C0 FS 0x1c                     parsed d.name = 'Anthony Ken'
plain                          parsed d.name = 'Anthony Kendall'
```

So `chr(0x1f)` survives the parse, and then, against the corrected roster:

```
'Anthony Ken\x1cdall'   -> human    ('anthony', 'kendall')
'Anthony Ken\x7fdall'   -> human    ('anthony', 'kendall')
```

Punctuation deletion is likewise still a widening, and the proposal says
otherwise two paragraphs after declaring it: *"The one surviving widening is
accent-and-case-equivalence."* Measured:

```
'Anthony Kendall'          -> human    ('anthony', 'kendall')
'A.n.t.h.o.n.y Kendall'    -> human    ('anthony', 'kendall')
'ANTHONY KENDALL!!!'       -> human    ('anthony', 'kendall')
'"Anthony" Kendall'        -> human    ('anthony', 'kendall')
```

**How bad is it?** Not very, and I want to be precise rather than dramatic. I
could not construct a byline that (i) reads to a human as *not the Maintainer*,
(ii) uses only these undeclared deletions, and (iii) classifies `human` --
because deletion can only *merge* characters within a word, and adding a visible
extra word requires whitespace, which creates a new tuple element and breaks
exact equality. The AI leg runs first and applies the same deletions, so an agent
name cannot be hidden by punctuating it. **The exploitability result here is
negative.** What fails is the *stated partition*, and since the partition is the
design rule and the author explicitly asked a reviewer to check it, it should be
corrected rather than left standing.

**Recommended disposition:** change the rule text to name three deletion classes
(ASCII punctuation **and symbols**; C0 controls and DEL; combining marks), or --
cleaner -- restrict the deletion to an explicit codepoint set and delete nothing
else, so that the rule and the code are the same statement.

---

### [I3] The roster-symmetry test is near-vacuous -- its oracle is the function under test

This is the shape the review brief warned about, and it is present here.

The proposal's test: *"Enforced by a test that calls `classify(x)` with roster
`[x]` over the 23-name corpus and asserts `human` for every entry -- symmetry
made falsifiable."*

`classify(x)` with roster `[x]` compares `_grant_words(x)` against
`_grant_words(x)`. That holds for **every total function**. The only ways it can
fail are the AI leg firing, or the fold returning empty. It cannot detect
over-folding -- which is the entire granting-direction risk.

Demonstrated with a deliberately destructive fold (each word collapsed to its
first letter):

```
$ ~/conda_envs/lhm/bin/python -c "... make_classify(good) vs make_classify(broken) ..."
correct fold                       roster-symmetry test: 8/8 classify human -> test PASSES: True
BROKEN fold (first letter only)    roster-symmetry test: 8/8 classify human -> test PASSES: True

yet under the BROKEN fold:
  roster ["Anthony Kendall"], byline "Amos Kim" -> human
```

A fold that grants Maintainer authority to *Amos Kim* passes the proposed
regression guard.

The same objection lands on the proposal's headline number. *"International-name
cost: zero, and this is the claim most worth checking... proposed design flags
**0 of 23**"* is produced by that same procedure, with each name rostered under
itself. The zero is close to guaranteed by construction, so it is not evidence
about the fold; it is evidence that the AI leg does not fire on those names and
that none of them folds to empty. (The `12 of 23` and `17 of 23` figures for the
*Amendment's* recipe are real, because its poison rule is an independent
predicate. The `0 of 23` is not comparable to them.)

**Recommended disposition:** add the test that has power -- an **anti-collision**
test asserting that the corpus's *distinct* names produce *distinct* keys, i.e.
that no corpus name classifies `human` against a roster holding a *different*
corpus name. That test would have caught every case in [I1]; the proposed one
cannot. Keep the symmetry test if you like, but label it as what it is -- a
smoke check on the AI leg and the empty-fold guard -- not as the
international-cost measurement.

---

### [I4] The character-preservation invariant test cannot be implemented as worded

The proposal names this as *the* invariant the Decision asked for: *"**No
identity-bearing character is dropped.** Enforced by a test that asserts the
fold's output preserves every input character in Unicode categories `L*` and
`N*`, over a generated sample spanning Latin-1, Latin Extended-A/B, Greek,
Cyrillic, Han, Arabic, Thai and the mathematical alphanumerics. This is the
invariant the Decision named, **stated so it can fail**."*

Taken literally it fails almost everywhere, because case folding and
combining-mark stripping both replace letters. Measured over exactly the sample
the proposal lists:

```
$ ~/conda_envs/lhm/bin/python -c "... if c not in _fold_word(c, form): fail += 1 ..."
Latin-1      L*/N* chars   62  NOT preserved:   58   e.g. [('NFD', '0xc0', "'a'"), ('NFD', '0xc1', "'a'")]
Latin Ext-A  L*/N* chars  128  NOT preserved:  120   e.g. [('NFD', '0x100', "'a'"), ('NFD', '0x101', "'a'")]
Latin Ext-B  L*/N* chars  208  NOT preserved:  157   e.g. [('NFD', '0x181', "'\\u0253'"), ('NFD', '0x182', "'\\u0183'")]
Greek        L*/N* chars  129  NOT preserved:   82   e.g. [('NFD', '0x370', "'\\u0371'"), ('NFD', '0x372', "'\\u0373'")]
Cyrillic     L*/N* chars  248  NOT preserved:  150   e.g. [('NFD', '0x400', "'\\u0435'"), ('NFD', '0x401', "'\\u0435'")]
Arabic       L*/N* chars  173  NOT preserved:   12   e.g. [('NFD', '0x622', "'\\u0627'"), ('NFD', '0x623', "'\\u0627'")]
Thai         L*/N* chars   67  NOT preserved:    1   e.g. [('NFKD', '0xe33', "'\\u0e4d\\u0e32'")]
Han          L*/N* chars   49  NOT preserved:    0   e.g. []
Math alnum   L*/N* chars   52  NOT preserved:   52   e.g. [('NFKD', '0x1d400', "'a'"), ('NFKD', '0x1d401', "'b'")]
```

Most of those are intended case folding. But that is precisely the problem: the
test as worded cannot distinguish intended folding from unintended deletion, so
at implementation it will be weakened to something that passes -- and whatever
that weakened predicate turns out to be, it is **not** the Decision's invariant,
while the record will say it is. This is the second near-vacuous guard in the
same test plan, arriving by a different route than [I3].

Note also that the Cyrillic line contains `0x401` folding to `\u0435` -- that is
[I1b], and this test would have to be written *not* to flag it in order to pass
at all.

Two further notes. The listed sample **omits** the scripts where the semantic
version of the invariant actually breaks: kana, Devanagari with nukta, and
precomposed Vietnamese. And `Han 0/49` is the only block where the literal
invariant holds, because Han characters neither case-fold nor decompose -- so
the one clean result comes from the one script that cannot exercise the
mechanism.

**Recommended disposition:** state the invariant in a form that can be true and
can fail. The honest one is: *for every input character in `L*`/`N*`, the fold's
output is non-empty* -- no letter or digit is deleted **to nothing** -- paired
with the anti-collision test from [I3] for the part the Decision actually cares
about. That pair is implementable, and together they mean what "dropping a
character must never widen authority" was reaching for.

---

### [I5] Change 3 introduces a new failure mode: an empty-folding registry entry matches every byline

The proposal, change 3: *"Config-supplied registry entries fold through
`_flag_words` too, so the extension mechanism is symmetric with the built-ins."*
The AI leg matches a registry entry as a **prefix** of a word
(`tools/lifecycle_planner.py:269`), and in Python `"anything".startswith("")` is
`True`.

```
$ ~/conda_envs/lhm/bin/python -c "from fold import _flag_words, _fold_word, REGISTRY; ..."
  entry '-'       -> _flag_words ()      _fold_word ''
  entry '--'      -> _flag_words ()      _fold_word ''
  entry '  .  '   -> _flag_words ()      _fold_word ''
  today _load_ai_registry guard "if str(t).strip()" lets "-" through: True
  with an empty registry token, 'Anthony Kendall'          classifies ai: True
  with an empty registry token, 'Jane Doe'                 classifies ai: True
  with an empty registry token, '\u041e\u043b\u044c\u0433\u0430' classifies ai: True
```

**Today this is inert** -- the entry survives as the literal `'-'`, and byline
tokens are alphanumeric-only, so nothing starts with it. After the change, the
same benign config typo makes **every byline classify `ai`**, so every Decision
in the tree is flagged as AI-authored. The existing guard at
`tools/lifecycle_planner.py:225` (`for t in extra if str(t).strip()`) is the
wrong predicate under the new fold: it tests whether the *entry* is blank, not
whether the *folded key* is.

The mirror hazard exists on the human side. The proposal names it in prose --
*"A config entry that folds to nothing is skipped rather than matching
everything"* -- but shows it in no code block, and the guard it would replace
(`tools/lifecycle_planner.py:294`) has the same wrong predicate. Its severity
also changes with the design: today an empty key is inert because set
intersection with an empty set is falsy; under **tuple equality**, `() == ()` is
`True`.

```
roster containing ONE punctuation-only entry (a typo) + the real name:
   byline '.'                  -> human
   byline '...'                -> human
   byline '-'                  -> human
   byline 'Anthony Kendall'    -> human
```

Mitigating: the only `classify` call site guards an empty name
(`tools/lifecycle_planner.py:613` -- `identity.classify(d.name) if d.name else
"unknown"`), so a truly empty byline cannot reach it. A punctuation-only byline
can.

**Recommended disposition:** both loaders filter on the *folded* value rather
than the raw entry, and a test covers the AI-side case specifically. One line
each; the value is that the failure mode is on the record.

---

### [I6] The fix imposes a new, unrecorded cost on exactly the axis it headlines as costless

The proposal changes tokenization from `str.split()` (which splits on **Unicode**
whitespace) to *"ASCII whitespace only"*, and records this only as an attack
mitigation: *"a non-ASCII separator stays inside its word rather than acting as
an invisible word break."* The eight non-ASCII separators appear in the
*Edge-case inventory* under **Handled**.

The same change breaks a legitimately-rostered name. `chr(0x3000)` IDEOGRAPHIC
SPACE is the ordinary separator between surname and given name in a Japanese
document, while the roster JSON would normally be typed with an ASCII space:

```
$ ~/conda_envs/lhm/bin/python -c "from fold import classify, _grant_words; ..."
CJK, chr(0x3000) IDEOGRAPHIC SPACE
    roster '\u5c71\u7530 \u592a\u90ce'         key "('\u5c71\u7530', '\u592a\u90ce')"
    byline '\u5c71\u7530\u3000\u592a\u90ce'    key "('\u5c71\u7530\\u3000\u592a\u90ce',)"
    classify -> unknown
    today   str.split()       -> "['\u5c71\u7530', '\u592a\u90ce']"
    proposed ASCII-only split -> "['\u5c71\u7530\\u3000\u592a\u90ce']"
Latin, chr(0x202f) NARROW NO-BREAK SPACE
    roster 'Anne Marie Dupont'         key "('anne', 'marie', 'dupont')"
    byline 'Anne\u202fMarie Dupont'    key "('anne\\u202fmarie', 'dupont')"
    classify -> unknown
    today   str.split()       -> "['Anne', 'Marie', 'Dupont']"
    proposed ASCII-only split -> "['Anne\\u202fMarie', 'Dupont']"
```

(`chr(0x202f)` is NARROW NO-BREAK SPACE, standard in French typography.)

The direction is safe -- it over-flags, it does not grant. But the proposal's
recorded false-positive costs list exactly one item (`O'Brien` rostered with a
straight apostrophe against a byline with a curly one), and this is a second, on
the international axis where the proposal says the cost is **zero**. The 23-name
corpus cannot see it, for the reason in [I3]: each name is rostered under
itself, so both sides carry the same separator.

**Recommended disposition:** record it as a cost in *Failure modes*, and add one
corpus case where roster and byline differ only in the separator. If it is
judged too sharp, the narrow fix is to treat Unicode `Zs` (space separators) as
word breaks while continuing to keep every other non-ASCII character -- that
closes the invisible-word-break attack without punishing a real name, because
`Zs` characters are *visible* as spaces.

---

### [I7] Two live-invariant figures have moved, and a sibling proposal now states this one's behaviour wrongly

**(7a) The frozen-file count.** The proposal asserts *"`162` frozen files...
`as_of 2026-08-03`"* and the Response re-asserts *"`162` frozen entries"*. At
`HEAD`:

```
$ ~/conda_envs/lhm/bin/python -c "... len(json.load(...)['frozen_files']) ..."
71abeb4 frozen_files=162
292e2c6 frozen_files=162
HEAD    frozen_files=164

added at HEAD: ['bootstrap/tests/_gate_preflight.py', 'bootstrap/tests/test_gate_preflight.py']
removed at HEAD: []
test_lifecycle_contract.py hash changed 292e2c6 -> HEAD: False
```

Both figures were correct when written; the batch grew at `e45e1fc`, after the
Response. The **substantive** claims still hold at `HEAD` -- verified:
`bootstrap/tests/test_lifecycle_contract.py` frozen `True`;
`tools/lifecycle_planner.py`, `templates/skills/_lib/lifecycle_planner.py` and
`dev/.cairn/agent-identities.json` all `False`. The finding is not that the
number is wrong. It is that the proposal calls this *"a live invariant to
re-check at plan time"*, and it moved **within the same day**, which argues for
re-measuring at plan-open rather than carrying `162` into the plan.

**(7b) The sibling contradicts this proposal, and only this proposal knows it.**
`planner-line-semantics` (status `proposed`, same joint sitting) states, in its
*Cross-lineage file collisions* section, that under scope 2 a byline built with
`chr(0x2028)` classifies `human` with folded key `'anthonykendall'`, and
prescribes the remedy: *"The correction is scope 2's to make and it is one word
wide -- poison any surviving non-ASCII character, not just letters."*

Both statements describe the **Amendment's** recipe, which this proposal
replaced. Measured under this proposal's design (evidence in the Steelman
block): that byline classifies `unknown`, with key
`('anthony\u2028kendall',)` -- the character is kept, not deleted. And the
remedy the sibling prescribes is the one this proposal measured and rejected
(`12 of 23` / `17 of 23` international names flagged). The sibling's conditional
ordering clause -- *"or its poison rule is widened first"* -- is now void, since
this proposal has no poison rule.

Neither ordering is unsafe, so this is a **record-consistency** defect, not a
schedule dependency. But this proposal's Decision would ratify a design that
makes a live sibling's cross-lineage section false, and a reader who lands on
the sibling first reads a wrong statement about what shipped.

**Recommended disposition:** name it in this proposal's *Cross-proposal
collisions* section as a stale characterization the sibling must correct at its
own Response, so the obligation is on the record on both sides rather than
neither. This proposal already adopts the sibling's substantive correction; what
is missing is the reverse pointer.

---

### Non-findings -- checked and sound, or not created by this change

Recorded so the next reviewer does not re-derive them.

* **ASCII-only confusables (`rn`/`m`, `l`/`I`, `0`/`O`, `1`/`l`) cannot reach
  `human`.** I confirm the External review's result, and can add the reason it
  holds robustly: exact tuple equality means any altered character changes the
  key, and punctuation deletion can only *merge* within a word -- adding a
  visible extra word needs whitespace, which changes the tuple's length. I could
  not construct a counterexample.
* **The AI leg's precedence is not defeatable by the surviving deletions.**
  `_flag_words` applies the same deletions, so punctuated, control-separated,
  full-width, circled and mathematical-bold agent names all still classify `ai`.
* **The live record does not regress.** Classifying every parsed byline under
  `dev/proposals/`, `dev/plans/` and `dev/strategy/` at `HEAD`, today's model vs.
  the proposed design with the corrected roster: **0 of 14 distinct names change
  classification** (`142` occurrences). The four real identities behave
  identically.
* **The `116` / `12` live-corpus figure is exact.** Re-derived independently at
  `71abeb4` via `git archive`: `occurrences: 116 | distinct names: 12`. In a
  lineage that has twice recorded evidence which did not survive re-running,
  this one does.
* **The "exactly one existing test node" claim is right.** I read
  `test_identity_model_is_three_way_positive_human` in
  `bootstrap/tests/test_lifecycle_contract.py`; of its six assertions only
  `classify("Anthony (Maintainer)") == "human"` (roster `["Anthony"]`) breaks
  under exact matching. The claim that `_HEADER_RE` never produces that shape is
  correct -- the name group is `[^()\n]+?` and the role is captured separately,
  confirmed by parsing a synthetic heading.
* **`Devine` -> `ai` is pre-existing, not introduced.** The registry prefix match
  (`tools/lifecycle_planner.py:269`) classifies the real surname *Devine* as the
  agent *devin*, today and after the change; because the AI leg has precedence, a
  Maintainer with that name cannot fix it via the roster. Out of scope here.
  Noted so it is not mistaken for a regression, and because it is a
  postdoc-first hazard someone should eventually own.

---

### Covered -- each lens swept, with the command that proves it

All under `~/conda_envs/lhm/bin/python` (3.13.13), `PYTHONDONTWRITEBYTECODE=1`,
at `HEAD` = `af4b2ee`, 2026-08-03. Scratch module transcribing the proposal's
printed design: `fold.py` in the session scratchpad.

1. **Defeat the normalization -- characters NFD does not decompose.**
   `from fold import _fold_word` over `chr(0x17f)`, `chr(0xfb01)`, `chr(0xfb03)`,
   `chr(0xfb05)`, `chr(0xdf)`, `chr(0x1e9e)`, `chr(0xb5)`, `chr(0x130)` at both
   strengths -> [I1a].
2. **Defeat it -- letter-distinguishing diacritics.** Vietnamese, Japanese,
   Devanagari and Cyrillic roster-vs-byline pairs through the transcribed
   `classify` -> [I1b], four `human` collisions.
3. **ASCII-only confusables.** Re-ran the External review's harness shape plus
   `rn`/`m`, `I`/`l`, `0`/`O`, `1`/`l` against roster `['Anthony Kendall']` ->
   all `unknown`; recorded as a non-finding.
4. **Enumerate the deletion classes.**
   `[cp for cp in range(0x80) if _fold_word(chr(cp),'NFD')=='']`, grouped by
   `unicodedata.category` -> [I2]: 66 codepoints, three groups.
5. **Reachability through the public path.** `_parse_sections` from
   `tools/lifecycle_planner.py` over synthetic `## Decision` headings carrying
   `chr(0x2028)`, `chr(0xa0)`, `chr(0x1f)`, `chr(0x1c)` -> [I2], and it settles
   that the proposal's `chr(0x2028)` table row is a unit-level result rather
   than a live one.
6. **Boundaries: empty, zero, one, N>>1, degenerate config.** Empty roster (the
   default adopter state), empty byline, whitespace-only byline,
   punctuation-only byline, punctuation-only roster entry, empty-folding AI
   registry entry -> Steelman (fail-closed holds) and [I5].
7. **Vacuous-guard check on every proposed test.** Re-implemented the symmetry
   test against a deliberately destructive fold; re-implemented the
   character-preservation invariant literally over the proposal's own stated
   sample -> [I3], [I4].
8. **Legitimately-rostered non-ASCII names.** CJK name with `chr(0x3000)`, Latin
   name with `chr(0x202f)`, roster typed with an ASCII space -> [I6].
9. **Live-record regression.** `_parse_sections` over every `.md` under
   `dev/proposals/`, `dev/plans/`, `dev/strategy/`, classified under both models;
   and the `116` / `12` figure re-derived at `71abeb4` via `git archive`.
10. **Sibling interaction.** Read `planner-line-semantics` >
    *Cross-lineage file collisions* in full; measured both landing orders ->
    [I7b].
11. **Gate-manifest live invariant.** `frozen_files` counted at `71abeb4`,
    `292e2c6` and `HEAD`; set difference and target-file hash compared -> [I7a].
12. **R3 and the Response's [G3] correction.** `_identity_token` today vs. the
    proposed `NFKD` comparator over four reviewer variants -> 3-of-4 confirmed
    exactly; the Response's correction confirmed.
13. **The one existing failing node.** Read
    `bootstrap/tests/test_lifecycle_contract.py` directly at the node.

### Not covered / low confidence -- the negative space

* **I am the same agent type as the author, in a fresh session. This review has
  NO cross-type independence.** That is not a formality here. The proposal names,
  as its reason for requiring an External security lens, exactly the judgment I
  was asked to make: *"the specific judgment a reviewer must make -- is the
  kept/dropped partition exhaustive, and is `NFD`-for-granting /
  `NFKD`-for-flagging the right split? -- is a Unicode-semantics question where
  a same-type reviewer inherits my blind spots exactly."* I agree with the split;
  **that agreement is worth very little**, because it is the agreement the author
  predicted a same-type reviewer would give. My *counterexamples* are execution
  outputs and stand on their own regardless of who produced them; my *judgments*
  about severity do not. This review does not discharge the
  `required(External, security lens)` tier and must not be counted toward it.
* **No code was edited.** Every measurement is against a scratch transcription of
  the proposal's printed design, not against `tools/lifecycle_planner.py` as it
  will be changed. The loaders (`_load_human_maintainers`, `_load_ai_registry`)
  and the revised `_identity_token` are **not shown** in the proposal, so [I5] in
  particular is a finding about a hazard the design creates, not about code that
  exists. This is the same gap the External review declared.
* **I did not run the test suite.** The proposal's `1545 passed, 1 skipped` and
  its 9-vs-10 sandbox baseline are unverified by me, as are the twin byte-parity
  claim and the `sha256:45c5c0ed...` figure.
* **I did not sweep for the same `re.sub` pattern elsewhere.** The proposal lists
  this under *Known omissions* and it remains open; `tools/lifecycle.py` and
  `scripts/` are unswept by both reviews now.
* **My `casefold()` and `NFKD` enumeration is not exhaustive either.** [I1a]
  shows the *class* of full-case-folding expansions reaches the granting path; I
  sampled it, I did not enumerate `CaseFolding.txt`. There may be worse members
  than `chr(0x17f)`.
* **No hostile roster.** I tested benign-typo config entries. A deliberately
  hostile `agent-identities.json` is a different threat model, and this file is
  lockfile-uncovered and installer-less (R6). I did not pursue it, and neither
  review has.
* **I did not evaluate R1, R3's Cyrillic case, or R4.** Nothing here bears on
  them; the Response's statement that they are untouched by review remains true.

### Second-round recommendation

**Recommended -- but as a scoped, cheap round, not a re-litigation.**

A second round is warranted because [I1] changes text the Decision is being asked
to *ratify*, and ratifying a residual whose mechanical expiry is already
satisfied would convert a decision back into debt -- the exact failure the
Decision's anti-debt condition targets. [I3] and [I4] matter because they are the
guards meant to keep this fix from silently regressing, and as written one cannot
fail and the other cannot pass.

None of that touches the design. Specifically:

1. **Author Response only -- no External re-review needed for [I2], [I5], [I6],
   [I7].** These are text corrections, a one-line guard on each loader, one
   recorded cost, and one re-measured figure. They do not change what the code
   does.
2. **[I1] and [I3]/[I4] should reach the Maintainer before the Decision**, since
   R2 is a ratification item and the invariant test is the Decision's own named
   condition. If the Response restates R2 with the three classes on the record
   and swaps the symmetry test for an anti-collision test, I would not ask for a
   further security pass.
3. **Do not re-open the design.** `NFD`-for-granting / `NFKD`-for-flagging
   survives everything I threw at it, and every alternative in the proposal's
   *Alternatives considered* is worse on the axes measured. In particular, [I1a]
   is **not** an argument for `NFKD` everywhere -- `NFKD` has the same
   `casefold()` behaviour *plus* the full-width class the proposal already
   measured and rejected.
4. **One optional design question for the Maintainer, not a finding:** whether to
   treat Unicode `Zs` as a word break ([I6]). It is the only change I would
   consider making to the fold itself, it is small, and the argument for it is
   that a visible space character is not an invisible word break.
