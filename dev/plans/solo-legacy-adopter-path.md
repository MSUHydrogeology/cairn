<!-- cairn-internal-ref-allow: doctrine/proposals.md doctrine/rationale.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: docs/solo-legacy-recipe.md, docs/assumptions.md -->
<!-- The two paths above: the first is this plan's own forward-reference (materializes at Chunk A); the second is an external-repo path (the postdoc's own tree, not Cairn's). -->

# Plan: the solo-legacy adopter recipe (Parts 1-5)

**Source proposal**: `dev/proposals/archive/2026-07-11-claude-solo-legacy-adopter-path.md`
**Status**: open
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
* `bootstrap/BOOTSTRAP.md:215` and `:696-698` both currently list only
  3 of the 6 default-on modules (`lifecycle-metrics`, `reflections`,
  `claim-check`) against the live `_DEFAULT_ON_MODULES` tuple
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
| A1 | `docs/solo-legacy-recipe.md` (new) | Worked adoption walkthrough for the solo + one-agent + legacy-scientific-codebase persona, alongside `docs/quickstart.md` / `docs/getting-started.md`. Per the Revised proposal `:245-266`: **Which level** — Level 1 (hand-copy the kernel) with the readiness-report pre-pass first; `scaffold.py --summary` / `modules_add` framed explicitly as a **roster-computation oracle** (what to hand-copy), not the Level-2 installer (R4a) — reconciles with `on-ramp/README.md:29`'s "No bootstrap script." **The exact composed profile** (verified this session, reproduced above): comments on their own full lines (R1's fix, the shipped-profile convention), `preset: solo-greenfield` + `age: legacy` + unconditional `modules_add: [legacy-agent, testing-discipline]` → the 8-module roster, zero warnings; `security-review` and `model-selection` presented as **conditional**, keyed to readiness-report findings, not force-added (R3) — "add `security-review` IF your readiness report flags a trust boundary [`templates/modules/team-gated/security-review.md:4-11`, trust-boundary-first]; add `model-selection` IF the pre-pass places you at moderate+ complexity [`model-selection.md:4-9`]." **Finding-2 framed positively** (R12a): the two unconditional lines named "the legacy-retrofit modules an existing tree needs," with the silent-under-install mechanism (the `age` override does not re-derive age-gated baseline rows) moved to a "why these lines are load-bearing" rationale aside, not the main path. **Week-one arc, sequenced** (R4b): (a) fill `templates/codebase-readiness-report.md`; (b) **Hello-world trivial accept first** (`templates/onboarding/solo-greenfield.md:54-57`'s disposable first rep, unchanged); (c) **then** `docs/assumptions.md` as the first **substantive** proposal, matching the readiness report's own "first **accepted** proposal" framing (`codebase-readiness-report.md:363-367`), not the first-ever lifecycle rep. **The triage-extra-triggers slot fill** for the science trigger — ready-to-paste text for the adopter's own installed `dev/proposals/_template.md`, framed around the readiness report's own question (`:292`, "would the science silently degrade if a contributor changed this default?"), keyed to sign/unit conventions, default parameters, calibration weights. **Escape hatch inline**: a short local gloss with the faithful qualifiers ("urgent, **clearly** reversible, or **explicitly** experimental ... the commit should **say why the proposal step was skipped**," R2), plus a pointer to Part 3's now-local template copy. |

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
| B1 | `bootstrap/tests/test_presets.py` (extend) | **(a) Literal-text round-trip (R1/R4a's actual test coverage gap).** Extract the recipe's YAML fenced code block directly from the committed `docs/solo-legacy-recipe.md` (regex/split on the ```` ```yaml ```` fence, not a hand-copied duplicate string — so the recipe and the test can never silently drift apart, matching this session's own established discipline of extracting real values over duplicating them) and round-trip it through `_minimal_yaml_parse` → `expand_preset`, asserting the documented 8-module roster and zero staffability warnings. Run once with `sys.modules` or an import-guard forcing the no-PyYAML path (mirroring `TestParserParity`'s existing `_yaml_load` vs. `_minimal_yaml_parse` parity pattern, `test_presets.py:290-297`), so this is a genuine stdlib-only reproduction, not a PyYAML-masked pass (R1's root cause). **(b) The naive-override pin (R12b).** `{preset: solo-greenfield, age: legacy}` alone resolves to exactly the 6 default-on modules, no `legacy-agent`, no warning — with a code comment stating explicitly this pins **current** behavior pending the deferred finding-2 engine-fix follow-up (Alternative 4 in the proposal, out of this plan's scope), so a future implementer who lands that fix reads a red test here as expected, not a regression. |

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
| E1 | `bootstrap/BOOTSTRAP.md` | Correct `:696-698` (Appendix B's YAML comment) and `:215` (the Act I-6 summary template) — both currently list only 3 of 6 default-on modules (`lifecycle-metrics`, `reflections`, `claim-check`) — to list all six, matching the live `_DEFAULT_ON_MODULES` tuple (`config.py:70-77`): add `fold-back-ledger`, `incident-trackers`, `documentation-plan`. **Doc-only** — explicitly does *not* touch `cli.py:348-353`'s missing-default-on-warning behavior (an engine change of a different risk class, deferred to its own proposal per R9's disposition). |

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

*Filled in after the fresh-context Internal plan-review subagent pass.*

## Code review

*Filled in after implementation commits land (Chunks A-E).*

## Lasting-truth migration

*Filled in at archive time. Per the [Archive preconditions rule](../PLANNING.md#archive-preconditions-proposals-and-plans),
plans archive only after every deferred follow-up has a durable home
outside the plan — the finding-2 engine-fix (Alternative 4), the
`cli.py` missing-warning gap, and a first-class `solo-legacy` preset
(Alternative 3, recurrence-gated) all stay the proposal's own explicitly
deferred follow-ups, not carried by this plan.*

This section is append-only once written.
