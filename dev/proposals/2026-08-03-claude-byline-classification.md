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

