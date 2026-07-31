<!-- cairn-internal-ref-allow: doctrine/proposals.md doctrine/rationale.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: docs/solo-legacy-recipe.md, docs/assumptions.md -->
<!-- The two paths above: the first is this plan's own forward-reference (materializes at Chunk A); the second is an external-repo path (the postdoc's own tree, not Cairn's). -->

# Plan: the solo-legacy adopter recipe (Parts 1-5)

**Source proposal**: `dev/proposals/archive/2026-07-11-claude-solo-legacy-adopter-path.md`
**Status**: review
**Plan review**: required(Internal) — fresh-context read. The proposal
already cleared a 3-lens Internal panel (12 findings, all accepted,
including one **blocking** finding — the recipe's headline YAML did not
parse under the stdlib-only fallback, the exact day-one failure the
whole proposal exists to prevent) and a Gemini External SHIP that
independently *executed* the fix rather than trusting it. This plan's own
job is mechanical translation into concrete file edits, plus verifying
the shipped recipe doc's prose is genuinely followable — the proposal's
own named non-mechanizable criterion, unverifiable until the doc exists.
No second External pass required — both doctrine and the resolver
mechanics were independently re-derived twice already.

## Context

The accepted proposal's Decision (2026-07-22) scoped **all five parts
in** — Parts 1/2/4/5 (the persona recipe) plus Part 3 (the universal
template escape-hatch gloss, explicitly marked independently
accept/rejectable at External review but not separately declined at
Decision). Full detail: `dev/proposals/archive/2026-07-11-claude-solo-legacy-adopter-path.md` —
its `## Revised proposal — 2026-07-11` section (after R1-R12) is the
authoritative design; this plan translates it into Chunks A-E.

**Independently re-verified this session, before writing this plan**
(not trusted from the proposal's or either review's prose):

* The corrected recipe YAML (comments on their own lines) parses
  cleanly under `_minimal_yaml_parse` and resolves via `expand_preset`
  to exactly **8 modules** (`claim-check`, `documentation-plan`,
  `fold-back-ledger`, `incident-trackers`, `legacy-agent`,
  `lifecycle-metrics`, `reflections`, `testing-discipline`) with **zero
  staffability warnings** — reproduced fresh this session via a direct
  Python call, not copied from either review's numbers.
* Adding both conditional modules (`security-review`, `model-selection`)
  resolves to exactly **10 modules**, also zero warnings — matches the
  proposal's stated "10-module roster" for the fully-conditional case.
* The escape hatch's verbatim text (`doctrine/proposals.md:200-204`,
  R2's fix) reads exactly *"urgent, clearly reversible, or explicitly
  experimental ... the commit or follow-up note should say why the
  proposal step was skipped"* — confirmed by direct read.
* **R6's open item, resolved**: the escape hatch's introducing commit is
  `9ad0fdb` ("Phase 1 (D): thin proposal + plan templates..."),
  dated **2026-06-08** — four days *before* Cairn's own self-hosting
  adoption (2026-06-12, `dev/PLANNING.md:34`). It is genuinely
  pre-self-hosting foundational doctrine with no discrete `dev/`
  Decision to cite — Part 3 states this explicitly per R6's own
  fallback clause, rather than citing a Decision that doesn't exist.
* `bootstrap/BOOTSTRAP.md:215` and `:701-705` (corrected from `:696-698`
  at plan-review — see PR1; the proposal's original citation drifted
  after an unrelated commit, `597c882`, inserted lines earlier in the
  file) both currently list only 3 of the 6 default-on modules
  (`lifecycle-metrics`, `reflections`, `claim-check`) against the live
  `_DEFAULT_ON_MODULES` tuple
  (`config.py:70-77`, six entries) — confirmed live, matching R9/Part 5.

### Documentation / doctrine surface

Parts 1 (`docs/`) and 2 (`on-ramp/`) are adopter-facing entry/descriptive
content — no doctrine. Part 3 ports already-accepted, pre-self-hosting
doctrine text into the installed template as a short local gloss (not a
new rule) — per the port exemption and this plan's own re-verification
above. Part 4 is a test. Part 5 is a factual doc-sync inside
`BOOTSTRAP.md`, not a contract or gate-table change. No engine change
anywhere in this plan — `expand_preset`/`_minimal_yaml_parse` are
exercised, not modified, so no AST re-anchor is needed (confirmed by
plan: no `bootstrap/_scaffold/*.py` file appears in any chunk below).

## Sequence

```
A. Part 1 -- the recipe doc (docs/solo-legacy-recipe.md)        [commit pending]
B. Part 4 -- regression test (bootstrap/tests/test_presets.py)  [commit pending]
   (sequenced right after A -- extracts A's literal YAML, not a
   hand-copied duplicate, so the two can never silently drift apart)
C. Part 2 -- on-ramp reconciliation (on-ramp/README.md)          [commit pending]
D. Part 3 -- escape-hatch local gloss (templates/core/dev/proposals/_template.md) [commit pending]
E. Part 5 -- BOOTSTRAP.md default-on-module doc-sync             [commit pending]
```

### Chunk A — Part 1 (the recipe doc)

| # | File | Change |
|---|------|--------|
| A1 | `docs/solo-legacy-recipe.md` (new) | Worked adoption walkthrough for the solo + one-agent + legacy-scientific-codebase persona, alongside `docs/quickstart.md` / `docs/getting-started.md`. Per the Revised proposal `:245-266`: **Which level** — Level 1 (hand-copy the kernel) with the readiness-report pre-pass first; `scaffold.py --summary` / `modules_add` framed explicitly as a **roster-computation oracle** (what to hand-copy), not the Level-2 installer (R4a) — reconciles with `on-ramp/README.md:29`'s "No bootstrap script." **The exact composed profile** (verified this session, reproduced above): comments on their own full lines (R1's fix, the shipped-profile convention), `preset: solo-greenfield` + `age: legacy` + unconditional `modules_add: [legacy-agent, testing-discipline]` → the 8-module roster, zero warnings; the canonical block is immediately preceded by an HTML-comment marker, `<!-- solo-legacy-recipe: canonical-profile -->` (plan-review PR3 — Chunk B's regression test locates this exact marker rather than a generic fence-split, since the doc may carry a second, contrasting YAML example for the "why not the naive override" callout below); `security-review` and `model-selection` presented as **conditional**, keyed to readiness-report findings, not force-added (R3) — "add `security-review` IF your readiness report flags a trust boundary [`templates/modules/team-gated/security-review.md:4-11`, trust-boundary-first]; add `model-selection` IF the pre-pass places you at moderate+ complexity [`model-selection.md:4-9`]." **Finding-2 framed positively** (R12a): the two unconditional lines named "the legacy-retrofit modules an existing tree needs," with the silent-under-install mechanism (the `age` override does not re-derive age-gated baseline rows) moved to a "why these lines are load-bearing" rationale aside, not the main path. **Week-one arc, sequenced** (R4b): (a) fill `templates/codebase-readiness-report.md`; (b) **Hello-world trivial accept first** (`templates/onboarding/solo-greenfield.md:54-57`'s disposable first rep, unchanged); (c) **then** `docs/assumptions.md` as the first **substantive** proposal, matching the readiness report's own "first **accepted** proposal" framing (`codebase-readiness-report.md:363-367`), not the first-ever lifecycle rep. **The triage-extra-triggers slot fill** for the science trigger — ready-to-paste text for the adopter's own installed `dev/proposals/_template.md`, framed around the readiness report's own question (`:292`, "would the science silently degrade if a contributor changed this default?"), keyed to sign/unit conventions, default parameters, calibration weights. **Escape hatch inline**: a short local gloss with the faithful qualifiers, verbatim against `doctrine/proposals.md:200-204` ("urgent, **clearly** reversible, or **explicitly** experimental ... the commit **or follow-up note** should say why the proposal step was skipped" — plan-review PR2: the proposal's own Part 1 bullet dropped "or follow-up note"; use this plan's Context section or the doctrine directly as the source, not that bullet), plus a pointer to Part 3's now-local template copy. |

**Prose-quality criterion (named in the proposal's own Evidence plan,
`:129`, as non-mechanizable — this plan's own verification, since the
doc did not exist at either review round).** Before this chunk's commit
lands, read the drafted recipe as a first-time solo postdoc would: does
it name one clear next action at each step, avoid unexplained jargon,
and never assume a second reviewer or PyYAML? This is a judgment call,
recorded here as an explicit self-check, not a rubber-stamped box.

### Chunk B — Part 4 (regression test)

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/tests/test_presets.py` (extend) | **(a) Literal-text round-trip (R1/R4a's actual test coverage gap).** Extract the recipe's YAML directly from the committed `docs/solo-legacy-recipe.md` — **anchored, not a generic fence-split** (plan-review PR3: the doc plausibly contains more than one ```` ```yaml ```` block, e.g. a contrasting "why not the naive override" example alongside the canonical recipe). Chunk A places an explicit marker, `<!-- solo-legacy-recipe: canonical-profile -->`, immediately before the canonical block (matching this repo's existing marker-comment convention); Chunk B's extraction locates that marker and takes the fenced block immediately following it, asserting **exactly one** match and failing loudly (not silently picking a fence) if that invariant breaks — so the recipe and the test can never silently drift apart, and a future second YAML example can't be picked up by accident. Round-trip the extracted text through `_minimal_yaml_parse` → `expand_preset`, asserting the documented 8-module roster and zero staffability warnings. Run once with `sys.modules` or an import-guard forcing the no-PyYAML path (mirroring `TestParserParity`'s existing `_yaml_load` vs. `_minimal_yaml_parse` parity pattern, `test_presets.py:290-297`), so this is a genuine stdlib-only reproduction, not a PyYAML-masked pass (R1's root cause). **(b) The naive-override pin (R12b).** `{preset: solo-greenfield, age: legacy}` alone resolves to exactly the 6 default-on modules, no `legacy-agent`, no warning — with a code comment stating explicitly this pins **current** behavior pending the deferred finding-2 engine-fix follow-up (Alternative 4 in the proposal, out of this plan's scope), so a future implementer who lands that fix reads a red test here as expected, not a regression. |

### Chunk C — Part 2 (on-ramp reconciliation)

| # | File | Change |
|---|------|--------|
| C1 | `on-ramp/README.md` | Reconcile the coarse choosing-a-level table row (`:63`, "large, legacy, or multi-team" → Level 2) with the **existing** finer-grained G/M/P mapping (`:52-57`, "mostly Mixed with 1-2 Poor → Level 1 first") — R8's correction: this is closing a contradiction between two things the doc already says, not adding a missing route. Add a short paragraph for "solo or two contributors, but on an existing/legacy codebase" → Level 1 with the readiness-report pre-pass, cross-linking `docs/solo-legacy-recipe.md`. Classified as **entry/on-ramp** layer (R11 — not "descriptive," `docs/DOCUMENTATION_PLAN.md`'s four-layer map places `on-ramp/` content by the "how do I enter?" question). |

### Chunk D — Part 3 (escape-hatch local gloss) — independently accept/rejectable, implemented per Decision

| # | File | Change |
|---|------|--------|
| D1 | `templates/core/dev/proposals/_template.md` | Keep the existing `doctrine/proposals.md` pointer (`:39-40`) intact — **add** a short local gloss with the faithful qualifiers (R2/R5's lighter form: gloss, not full restatement, minimizing the drift surface) plus a **sync-note** so a future doctrine edit is visibly flagged for re-sync. **Cite the port exemption's condition honestly (R6, this plan's own re-verification above):** state that the escape hatch is pre-self-hosting foundational doctrine (introduced `9ad0fdb`, 2026-06-08, four days before Cairn's own 2026-06-12 self-host adoption) with no discrete `dev/` Decision to cite — the fallback clause R6 itself names, not asserted without support. |

### Chunk E — Part 5 (BOOTSTRAP.md default-on-module doc-sync)

| # | File | Change |
|---|------|--------|
| E1 | `bootstrap/BOOTSTRAP.md` | Correct `:701-705` (Appendix B's YAML comment — **not** `:696-698`; plan-review PR1 found the proposal's original citation drifted after an unrelated commit, `597c882`, inserted 7 lines earlier in the file — re-verify the exact range again at implementation time in case of further drift) and `:215` (the Act I-6 summary template, unaffected by the drift) — both currently list only 3 of 6 default-on modules (`lifecycle-metrics`, `reflections`, `claim-check`) — to list all six, matching the live `_DEFAULT_ON_MODULES` tuple (`config.py:70-77`): add `fold-back-ledger`, `incident-trackers`, `documentation-plan`. **Doc-only** — explicitly does *not* touch `cli.py:348-353`'s missing-default-on-warning behavior (an engine change of a different risk class, deferred to its own proposal per R9's disposition). |

## Acceptance criteria

* **Tests that must pass** — the extended `bootstrap/tests/test_presets.py`
  (Chunk B, both the literal-text round-trip and the naive-override pin).
  The full `python -m pytest bootstrap/tests` suite green **modulo**: the
  two pre-existing `test_ast_attest.py` sandbox-interpreter artifacts
  already documented by every sibling plan this session — this plan
  touches no `bootstrap/_scaffold/*.py` file, so it must not add or
  change that count at all (verify identical CHANGED-symbol set before
  and after, under the canonical `lhm` interpreter).
* **Examples / smoke checks required**:
  * `python scripts/check_cairn.py` clean over the new recipe, the
    edited `on-ramp/README.md`, the ported template gloss, and the
    edited `BOOTSTRAP.md` (link resolution + claim-path).
  * `python scripts/claim_check.py` clean over this plan and every
    touched/new file.
  * **End-to-end dogfood, under the actual no-PyYAML path, not a
    simulation** — temporarily uninstall or import-block PyYAML (or
    confirm the test environment genuinely lacks it) and run
    `python bootstrap/scaffold.py --summary --config <a scratch copy of
    the recipe's exact YAML>`, confirming the printed roster matches the
    documented 8 modules. This is the residual verification item both
    reviews named as unexercised (`_minimal_yaml_parse` was called
    directly, not through the real CLI/stderr `format_profile_summary`
    path) — close it here, not defer it again.
* **Docs**: the recipe's own prose-quality self-check (Chunk A's table
  note); `docs/DOCUMENTATION_PLAN.md` routing confirmed for Parts 1/2.

## Signals the change is wrong

Carried forward from the proposal's own list (`:143-149`), unchanged:
the Part 4 test going red on a legitimate engine change (update the
recipe + `modules_add` in the same commit); a solo-legacy adopter
finding the recipe heavier than their tree earns (add a "trim for a
small legacy tree" note pointing at `modules_remove`); the
`triage-extra-triggers` slot fill reading as bureaucracy (recast around
the concrete "would the science silently degrade" question); the
persona recurring and the composed-profile recipe proving too fiddly
(the deferred first-class `solo-legacy` preset becomes recurrence-
justified); a reviewer judging the Part-5 BOOTSTRAP.md fix insufficient
on its own (it explicitly does not touch `cli.py`'s missing-warning
gap — named, not silently assumed fixed).

## Review

**Attribution / committer note.** Fresh-context subagent plan-review;
the subagent cannot commit, so the author-session commits this section
as a disclosed scribe, the accepted deviation model used throughout
this repo's lifecycle.

## Plan review -- Claude (Internal, fresh-context) -- 2026-07-31

**Model**: Claude Sonnet 5

**Steelman.** This is a careful translation of an unusually well-scrutinized proposal. The plan does real, independent work rather than rubber-stamping the accepted design: it re-derives the YAML-parse fix a third time (correctly), it tracks down the actual introducing commit and date for the escape-hatch doctrine text rather than asserting the "pre-self-hosting, no Decision" claim on faith, and it live-checks the `BOOTSTRAP.md` default-on-module drift against the current `_DEFAULT_ON_MODULES` tuple rather than trusting the proposal's now-stale snapshot. The chunk breakdown (A-E) is a faithful, complete mapping of the Revised proposal's five parts, and the acceptance criteria correctly pick up the one residual verification item both prior reviews flagged as unexercised instead of deferring it a third time.

**Findings** (most significant first):

* **[PR1] `BOOTSTRAP.md:696-698` no longer resolves to the module list it describes — an intervening, unrelated commit shifted it.** Current HEAD: lines 696-698 are `project_name`/`test_command`/blank; the actual 3-of-6 default-on module list is at **`:701-705`** (`:701-702` the comment header, `:703-705` the three module lines). Root cause: commit `597c882` (2026-07-22, an unrelated licensing plan) inserted a 7-line paragraph earlier in the file, shifting everything below down. The substantive claim (only 3 of 6 listed) is still true; only the line pointer drifted. `:215` is unaffected.
  *Grounding:* `awk 'NR==694,NR==706' bootstrap/BOOTSTRAP.md` (confirms `:701-705`); `git log -S"Licensing of the installed files" --oneline -- bootstrap/BOOTSTRAP.md` → `597c882`.
  *Suggested fix:* Update Chunk E's citation to `:701-705`; re-verify the exact range again at implementation time in case further unrelated commits land before then.

* **[PR2] Chunk A's own escape-hatch text drops "or follow-up note" from the doctrine quote — inherited from the proposal's residual narrowing, uncaught by this plan's own Context section which quotes it correctly two sections earlier.** Doctrine (`doctrine/proposals.md:200-204`) reads *"...the commit **or follow-up note** should say why..."* The proposal's own Part 1 bullet (`:266`) and this plan's Chunk A row both give *"...the commit should say why..."* — dropping the clause. This is the same failure class this proposal was twice corrected on (R2, and the Response's own "cross-cutting note" flagging doctrine-quote drift as "a recurring, counted pattern") — a third instance, this time inside the plan itself, and one my own Context section (which quotes the clause correctly) should have caught against my own Chunk A row.
  *Grounding:* `doctrine/proposals.md:200-204` (full text); `dev/proposals/archive/2026-07-11-claude-solo-legacy-adopter-path.md:266` (drops the clause); this plan's Chunk A row (same drop) vs. this plan's Context section, line 46 (quotes it correctly).
  *Suggested fix:* When drafting Chunk A's and Chunk D's actual gloss text, use the plan's own Context-section quote or `doctrine/proposals.md:200-204` directly, not the proposal's Part 1 bullet — include "or follow-up note."

* **[PR3] Chunk B's YAML-extraction design ("split on the fence") is unanchored and ambiguous if the finished recipe contains more than one fenced YAML block** — plausible, since the accepted design's "why not the naive `age: legacy` override alone" callout (Revised proposal Part 1) names the same 2-key composition Chunk B(b) tests, and could reasonably be rendered as its own contrasting ```yaml example. `test_presets.py`'s own existing tests use a hardcoded literal, not extraction; the real in-repo precedent for extract-not-duplicate is `test_quickstart_sequence.py:220-239`, which anchors its regex to unique surrounding prose (`\*\*(\d+)\*\* modules listed`), not a generic fence-split.
  *Grounding:* `bootstrap/tests/test_presets.py:280-303` (hardcoded, not extracted); `bootstrap/tests/test_quickstart_sequence.py:220-239` (the real precedent, anchored extraction).
  *Suggested fix:* Anchor the extraction explicitly — an HTML-comment marker immediately preceding the canonical block (matching this repo's existing `cairn:slot`/`claim-check-allow`-style marker convention), or assert exactly one ```yaml fence exists and fail loudly if that invariant breaks, rather than picking "the first" or "the last" one silently.

**Coverage.** Independently reproduced: the YAML parse/module-count claims (8-module unconditional, 10-module both-conditionals), the R6 introducing-commit date (`9ad0fdb`, 2026-06-08, four days before self-hosting), the `BOOTSTRAP.md` drift's substance, all five chunks' fidelity to the accepted design, the AST-attestation baseline under the canonical interpreter (26/26, confirming the "before" state this plan's acceptance criteria requires stay identical), and all general gates. Confirmed the two unrelated same-day-adjacent commits (`91c96b4`, `3325a13`) don't overlap any of this plan's five target files. Out of reach by design (implementation-time checks): the recipe's actual prose quality, the real end-to-end no-PyYAML dogfood, and whether Chunk B's eventual extraction code handles the multi-fence risk PR3 names.

**Verdict:** Proceed with the fixes above folded in. None is design-fatal or reopens the proposal's own settled scope — PR1 is a stale citation, PR2 is a one-clause doctrine-quote correction, PR3 is a concrete implementation note.

### Sharpening -- Claude (author) -- 2026-07-31

All three findings independently re-verified before disposing: re-ran
`awk`/`git log -S` for PR1 (confirmed `:701-705`, commit `597c882`);
re-read `doctrine/proposals.md:200-204` against both the proposal's
`:266` and this plan's own Chunk A row for PR2 (confirmed the drop in
both, and confirmed my own Context section already had it right); read
`test_quickstart_sequence.py:220-239` for PR3 (confirmed it anchors to
unique prose, not a generic fence-split).

* **[PR1] accept.** Chunk E's citation corrected below from `:696-698`
  to `:701-705`.
* **[PR2] accept.** Chunk A's escape-hatch text corrected below to
  include "or follow-up note," matching the plan's own Context section
  and the doctrine verbatim.
* **[PR3] accept.** Chunk B's row sharpened below: extraction anchored
  to an explicit HTML-comment marker (`<!-- solo-legacy-recipe:
  canonical-profile -->`) immediately preceding the canonical YAML
  block, with the test asserting exactly one match and failing loudly
  (not silently picking a fence) if that invariant breaks — Part 1's
  own drafting (Chunk A) must place that marker when the recipe is
  written, so this is a cross-chunk dependency now made explicit.

**Status: open → executing.** All findings disposed; implementation
begins next (Chunks A-E in sequence).

## Code review

**Attribution / committer note.** Fresh-context subagent review of the
five implementation commits; the subagent cannot commit, so the
author-session commits this section as a disclosed scribe, the accepted
deviation model used throughout this repo's lifecycle.

## Code review -- Claude (sub-agent, fresh context, not the implementer) -- 2026-07-31

**Verdict: Accept-with-followups**, applying to the five commits `5114b4c`
(Chunk A), `d83ed78` (Chunk B), `fb81efb` (Chunk C), `2e34528` (Chunk D),
`60b4b83` (Chunk E). Chunks B, C, E verify clean end-to-end. Chunk A had
one real punctuation deviation from a "verbatim" doctrine-quote claim
(em dash vs. comma). Chunk D's commit message undercounted pre-existing
twin-file slot differences (three claimed, four actual, all pre-dating
the commit — a narration slip, not a functional defect). The most
substantive finding: the plan's own acceptance criteria named the
end-to-end no-PyYAML CLI dogfood as a residual item that must be
"closed here, not deferred again" — the implementation closed it with a
one-off manual run, not a durable regression test.

**Model**: Claude Sonnet 5, fresh session, no access to the implementing
session.

### Falsification ledger

**Chunk A — one real deviation, fixed post-review.** Read the full doc
as a first-time postdoc would: genuinely followable, one action per
step, no unexplained jargon. Mechanically confirmed: exactly one
```` ```yaml ```` fence, marker-anchored, round-trips to the 8-module
roster with zero warnings (three independent reproductions across this
plan's lifecycle: plan-authoring, this code review, and the fix
below). Week-one sequencing and the conditional-module framing both
verified correct. **Found:** the escape-hatch text used an em dash
where `doctrine/proposals.md:200-204` uses a comma before "but" — the
commit message called this "quoted verbatim," and it was verbatim on
every word (including "or follow-up note," R2's fix) but not on
punctuation.

**Chunk B — clean, and its extraction helper genuinely fails loud.**
5/5 new tests passed (33/33 in the file). Independently stress-tested
`_extract_marked_yaml` against four mutation scenarios (zero markers,
duplicate markers, missing fence, unterminated fence) — all four raise
with a clear message, none silently pick a fence. The naive-override
pin's comment correctly frames it as current-pending-a-deferred-fix,
not a desired invariant.

**Chunk C — clean.** Genuine reconciliation (cites the existing G/M/P
mapping as already covering the case), not a "missing route" overclaim.
Correctly cross-links the recipe.

**Chunk D — twin-file gloss byte-identical and doctrine-verbatim,
correctly (comma, not the Chunk A em-dash), confirmed by direct
extraction from both files. The R6 port-exemption date (`9ad0fdb`,
2026-06-08, four days pre-self-hosting) reconfirmed. The lockfile-drift
excuse independently reproduced as accurate, not invented:** `upgrade
--target . --cairn-root . --plan` lists 38 pre-existing "no recoverable
base" files including this one; the recorded hash genuinely doesn't
match current content and already carries `unrecoverable_base: true`.
**Found (narration only):** the commit message says "three" remaining
slot differences between the twin files; there are four
(`triage-extra-triggers`, `documentation-tier-home`,
`tests-tier-home`, `examples-smoke-home`), all confirmed pre-existing
via a diff against the pre-commit state — not introduced by Chunk D,
just miscounted in its own commit message.

**Chunk E — clean.** Both `BOOTSTRAP.md` locations (`:215`, and the
Appendix B block, re-verified at its actual current lines rather than
trusted from either prior citation) now list all six default-on
modules, matching the live `_DEFAULT_ON_MODULES` tuple exactly. Doc-only.

**Gate sweep at current HEAD (pre-fix).** Full suite 1437 passed / 3
skipped / 2 failed (the two pre-existing `test_ast_attest.py`
artifacts, matching every sibling plan this session). Canonical `lhm`
interpreter: 26/26 — confirms the "no engine change" claim genuinely
holds. `check_cairn` OK; `claim_check` clean on every touched file;
`quality_gate --sub neutrality` at 99 FAILs, none from touched files.

**The no-PyYAML dogfood — the substantive finding.** The plan's
acceptance criteria named the real CLI `--summary` path under a
genuinely PyYAML-absent interpreter as the one item both proposal-stage
reviews left unexercised, and said explicitly it must be "closed here,
not deferred again." None of Chunk B's five committed tests exercise
`main(["--summary", ...])` — only `_minimal_yaml_parse`/`expand_preset`
directly. The reviewer reproduced the real CLI manually via
`/usr/bin/python3` (a genuinely PyYAML-absent interpreter on this
machine) and confirmed it works, but flagged that this closes the item
only for this one review session, not durably — the next person to
touch this recipe has no regression test protecting the claim.

### Coverage

Independently reproduced: the 8-module roster and zero-warning claim
(three ways); every doctrine-quote verbatim claim (found the one real
em-dash deviation); the extraction helper's four-scenario loud-failure
behavior; twin-file byte-identity of the ported gloss; the R6
introducing-commit date; the lockfile-drift claim via the actual
`--plan` command and a hash comparison; current `BOOTSTRAP.md` line
numbers against the live tuple; the full gate sweep. Not independently
exercised: visual rendering of the em dash vs. comma in a Markdown
viewer (immaterial); `on-ramp/`'s doc-tier-layer fit against
`docs/DOCUMENTATION_PLAN.md`'s four-layer map (a pre-existing loose end
the original proposal review, R11, already flagged as no-gate-
consequence, not newly surfaced here).

### Required follow-ups

1. **(Substantive, resolved post-review)** Add a durable regression test
   exercising the real CLI `--summary` path under a genuinely forced
   no-PyYAML condition, not just `_minimal_yaml_parse` called directly —
   closing the plan's own named residual verification item properly
   rather than leaving it verified only by ad hoc manual runs.
2. **(Cosmetic, resolved post-review)** Align Chunk A's escape-hatch
   text to the comma doctrine uses, for a strictly byte-verbatim quote.
3. **(Cosmetic, noted, no action)** Chunk D's commit message undercounts
   the twin files' pre-existing slot differences (three claimed, four
   actual) — historical commit-message text, not corrected retroactively;
   noted here for the record.

### Sharpening -- Claude (author) -- 2026-07-31

Both actionable findings independently re-verified before fixing: diffed
the recipe's escape-hatch line against `doctrine/proposals.md:200-204`
directly (confirmed the em-dash-vs-comma deviation, nothing else); read
`config.py`'s `try: import yaml` / `except ImportError` branch structure
to design a genuine (not simulated) forced-fallback test.

* **[Follow-up 1] accept — fixed.** Added
  `test_summary_cli_under_a_genuinely_forced_no_pyyaml_path` to
  `TestSoloLegacyRecipe`: runs `bootstrap.scaffold.main(["--summary",
  ...])` in a `subprocess.run([sys.executable, ...])` with
  `sys.modules["yaml"] = None` set *before* `bootstrap.scaffold` is
  ever imported in that subprocess — portable (uses `sys.executable`,
  no hardcoded interpreter path) and genuine (forces `config.py`'s
  `import yaml` to raise `ImportError` for real, not a simulation).
  Proven non-vacuous by mutation: reintroducing the *original* R1 bug
  (a trailing scalar comment on `preset:`) into a scratch copy of the
  recipe reproduces the exact historical failure class
  (`PresetError`-shaped `unknown preset 'solo-greenfield   # solo
  staffing'`) that this whole proposal exists to prevent — reverted,
  file diff-confirmed identical to HEAD afterward.
* **[Follow-up 2] accept — fixed.** Escape-hatch text corrected to the
  comma doctrine uses; re-diffed against `doctrine/proposals.md:200-204`
  to confirm exact match (modulo the recipe's own section-header framing,
  which never repeats the "**Escape hatch.**" bold lead-in since it has
  its own `## The escape hatch` heading — an intentional, not a
  deviation).
* **[Follow-up 3] acknowledged, no action** — historical commit-message
  text; not worth a corrective commit on its own, per the reviewer's own
  disposition.

**Status: executing → review.** Code review's substantive finding is
resolved; the plan is otherwise complete and gate-clean. No
Maintainer-gated closeout remains (no engine change, no AST re-anchor).
Archive next.

## Lasting-truth migration

*Filled in at archive time. Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home
outside the plan — the finding-2 engine-fix (Alternative 4), the
`cli.py` missing-warning gap, and a first-class `solo-legacy` preset
(Alternative 3, recurrence-gated) all stay the proposal's own explicitly
deferred follow-ups, not carried by this plan.*

This section is append-only once written.
