<!-- cairn-internal-ref-allow: doctrine/proposals.md doctrine/rationale.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Forward-reference + external-repo paths this proposal cites: the recipe doc it creates, and the adopter-repo `docs/assumptions.md` it points the postdoc at (which lives in the postdoc's tree, not Cairn's). -->
<!-- claim-check-allow: docs/solo-legacy-recipe.md, docs/assumptions.md -->

# The solo-legacy adopter recipe: a verified adoption path for the solo scientist + one agent + an existing research codebase

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-07-11
**Status**: proposed
**Touches**: a new adopter-facing recipe doc (`docs/solo-legacy-recipe.md`); the adoption-path routing in `on-ramp/README.md`; a one-paragraph escape-hatch port into the installed proposal template `templates/core/dev/proposals/_template.md`; a regression test in `bootstrap/tests/test_presets.py`. **No engine change; no doctrine change.**
**Related**: broad-look review `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md` Themes 5.1 / 5.3 / 5.4 / 5.5 (Phase A, "before the postdoc installs"); the accepted sibling `2026-07-08-claude-review-record-integrity` (same instance/record shape, and the model of a good proposal here); the superseded `2026-07-08-claude-automated-review-committer` (the rate-limit-gate lesson this proposal is deliberately built to respect).
**Plan review**: required(Internal) — touches shipped adopter templates and the adoption-path docs and adds a regression test; Internal floor (fresh-context), with an External cross-type read *recommended* before the Decision because this is the exact path the first external adopter walks and a different agent type is likelier to catch a routing / usability gap. Ratified at Decision.

## Context

The first external adopter is a hydrogeology postdoc with an **existing, messy research codebase**, working **solo with one agent**. That persona — solo + one-agent + legacy scientific code — is the path the broad-look audit (Theme 5) found Cairn does *not* actually pave. Every landmark on the walk mis-routes, undercounts, or omits the one thing the postdoc most needs. Verified this session:

1. **No preset or level fits them.** `on-ramp/README.md:33` says "Level 1 is the natural home for solo + one-agent adopters," but `on-ramp/README.md:47-48` and the choosing-a-level table at `on-ramp/README.md:63` send "large, legacy, or multi-team" to Level 2. A solo adopter *on a legacy tree* is both at once, and the table has no row for them. `bootstrap/prompts/bootstrap-lite.md:1` targets "one-human + one-agent adopters" yet `bootstrap-lite.md:8` is explicitly for when "you have a real codebase," routing that same persona to the Level 2 scaffold. The three named presets are the only fast paths, and none is solo-legacy: `high-rigor-legacy`'s canonical point is large / complex / multi-language / large-multi / concurrent-multi-type (`bootstrap/profiles/high-rigor-legacy.yml:5-12`) — a five-person multi-agent shop, not a solo postdoc.

2. **The obvious workaround silently under-installs.** A natural instinct is "take `solo-greenfield` and set `age: legacy`." That does **not** work, and fails *silently*. `resolve_axes` (`bootstrap/_scaffold/config.py:973-988`) overrides the axis *value*, but `expand_preset` (`config.py:1115-1200`) builds the roster from the preset's **static authored baseline** (`config.py:1143-1144`) — for `solo-greenfield` that baseline is empty (`config.py:906`) — and re-derives *only* the two team-staffing-gated modules from the resolved axes (`config.py:1145-1148`). Age-gated rows are never re-derived. Verified empirically (as_of 2026-07-11): `{preset: solo-greenfield, age: legacy}` resolves to the identical 6-module default-on roster with **no `legacy-agent`, and no warning** — even `{age: legacy, complexity: complex, language: multi}` yields the same 6. The adopter never learns they missed the legacy-retrofit apparatus `dimensions/age.md:43-56` prescribes (Legacy Agent role, surface-readiness map, characterization testing). `test_presets.py:155-160` guards the *coordination* axis-override; there is no counterpart for age.

3. **The documented fallback is itself buggy.** `bootstrap/BOOTSTRAP.md` Appendix B's hand-derived `modules:` example (`BOOTSTRAP.md:683-711`) lists only three of the six default-on modules (`BOOTSTRAP.md:696-698`; the I-6 summary at `BOOTSTRAP.md:215` repeats the three-of-six drift), and a literal `modules:` list is **exact-list** semantics — the `modules:` branch in `bootstrap/_scaffold/cli.py:348-353` emits **no missing-default-on warning** (only the no-preset/no-modules else-branch at `cli.py:356-364` prints the default-on set). So an adopter who follows Appendix B by hand ships a roster missing `fold-back-ledger`, `incident-trackers`, and `documentation-plan`, silently.

4. **The triage list omits science.** The canonical triggers (`doctrine/proposals.md:154-177`) and the installed adopter copy (`templates/core/dev/proposals/_template.md:42-46`) name public-API/config contracts, new abstractions, and file moves — never a scientific assumption, sign/unit convention, default parameter, or calibration constant. Yet the readiness report calls exactly that class "the question Cairn is most differentiated on" (`templates/codebase-readiness-report.md:295`) and asks the maintainer to "list the assumptions that *should not* be changed without a proposal" (`codebase-readiness-report.md:299-302`). Result: the postdoc's first real change — tweaking a recharge default — hits none of the triggers and triages to "just commit" (`doctrine/proposals.md:175-177`). The differentiator misses the differentiating change.

5. **The escape hatch is off-tree.** `doctrine/proposals.md:200-204` carries the "urgent, reversible, or experimental may proceed without a proposal, but say why" rule; the installed template (`templates/core/dev/proposals/_template.md:39-40`) carries only a *pointer* to `doctrine/`, which the adopter does not have locally. The adopter's own tree never states the escape hatch.

6. **No named week-one payoff for a scientist.** The one early science-shaped artifact — "the first proposal should be a `docs/assumptions.md`" — exists only as a *Section-11-is-Poor conditional* in the readiness report (`codebase-readiness-report.md:363-367`), while the shipped solo onboarding prescribes a "Hello world"-style trivial accept instead (`templates/onboarding/solo-greenfield.md:54-57`) and states it assumes "no legacy-tree pre-pass" (`solo-greenfield.md:25-28`). The onboarding task list is keyed 1:1 to the three preset names (`bootstrap/_scaffold/install.py:736-738`), so there is no solo-legacy task list to inherit, and the `high-rigor-legacy` one assumes concurrency and multi-agent staffing throughout (`templates/onboarding/high-rigor-legacy.md:79-94`) — wrong for a solo postdoc.

The through-line: the postdoc's path exists in pieces, but no artifact assembles it, and the pieces that touch them either mis-route or under-deliver. This proposal assembles the path from **mechanisms Cairn already ships**, and is deliberately built to serve the postdoc *without* the one move that would kill it in review — a doctrine change to the universal triage list (see *Doctrine-change rate-limit*).

## Proposed paths

Proposed paths:
- `docs/solo-legacy-recipe.md` — the new adopter-facing recipe; lands in this proposal's implementation.

## Proposal

Four parts, one spine: **give the solo + one-agent + legacy scientific adopter a single, verified, copy-pasteable path built entirely from shipped mechanisms.**

### Part 1 — the recipe doc (`docs/solo-legacy-recipe.md`)

A worked adoption walkthrough for the persona, in the descriptive layer alongside `docs/quickstart.md` and `docs/getting-started.md`. It carries, concretely:

* **Which level.** Level 1 (hand-copy the kernel) with a **readiness-report pre-pass first** — resolving finding 1: solo staffing keeps them at Level 1, but the legacy tree earns the pre-pass that greenfield skips.
* **The exact composed profile**, using the "compose, don't bypass" path `BOOTSTRAP.md:188` already blesses — *not* a new preset, and *not* a hand-derived `modules:` list (which finding 3 shows under-installs silently):

  ```yaml
  project_name: "<your-repo>"
  test_command: "<your test command, or 'no tests today'>"

  preset: solo-greenfield     # solo staffing: one human + one agent
  age: legacy                 # existing codebase — drives conditional
                              #   stripping + the readiness pre-pass framing
  modules_add:                # the age/complexity-gated rows the override
    - legacy-agent            #   does NOT auto-derive (finding 2)
    - testing-discipline
    - model-selection
    - security-review
  ```

  Verified this session (as_of 2026-07-11): this resolves to the 10-module roster
  `lifecycle-metrics, reflections, claim-check, fold-back-ledger, incident-trackers, documentation-plan, legacy-agent, security-review, model-selection, testing-discipline` — all six default-on modules **plus** the legacy-retrofit set — with **no staffability warnings** (the added modules are not team-staffing-gated, so `single` agent-team does not veto them). The recipe states this roster explicitly so the adopter can confirm the `--summary` output matches.
* **Why not the naive `age: legacy` override alone** — a short, honest callout of finding 2, so the adopter understands *why* the `modules_add` lines are load-bearing rather than cargo-culting them.
* **The week-one arc** (resolving finding 6): (a) fill `templates/codebase-readiness-report.md`; (b) make the **first real proposal** a `docs/assumptions.md` for their own repo — the load-bearing scientific choices written down before any agent edits them — promoting the readiness report's Section-11-Poor conditional (`codebase-readiness-report.md:363-367`) to the *default* first artifact for a legacy scientific adopter, in place of the greenfield "Hello world" trivial accept.
* **The exact `triage-extra-triggers` slot fill** for the science trigger (resolving finding 4 without touching doctrine — see below), given as ready-to-paste text the adopter drops into their installed `dev/proposals/_template.md`.
* **The escape hatch, inline** (a short restatement, plus a pointer to Part 3's now-local copy), resolving finding 5 at the point of use.

### Part 2 — fix the on-ramp routing contradiction (`on-ramp/README.md`)

Add a row / short paragraph to the choosing-a-level guidance for "**solo or two contributors, but on an existing / legacy codebase**" → Level 1 *with the readiness-report pre-pass*, cross-linking the Part 1 recipe. Reconcile the prose at `on-ramp/README.md:33` and `:47-48` so "solo → Level 1" and "legacy → Level 2" no longer read as a contradiction for the adopter who is both (the axis that pushes toward Level 2 is *team/size/complexity*, not age alone; a solo legacy adopter stays at Level 1 and adds the retrofit modules by hand). Descriptive-layer change only.

### Part 3 — port the escape hatch into the installed template (`templates/core/dev/proposals/_template.md`)

Add a one-paragraph escape-hatch statement after the triage summary (`templates/core/dev/proposals/_template.md:44-46`), restating `doctrine/proposals.md:200-204` so every adopter's *own* tree carries it, not just a pointer to a `doctrine/` file they lack. This is a **port of already-accepted doctrine into the installed template**, not a new rule (see *Doctrine-change rate-limit*).

### Part 4 — regression test (`bootstrap/tests/test_presets.py`)

Add a test that pins the recipe's central claim and documents the finding-2 behavior it routes around: (a) `{preset: solo-greenfield, age: legacy}` resolves to exactly the 6 default-on modules (no `legacy-agent`) — the age-override-does-not-re-derive behavior, asserted so any future engine change to it is a *deliberate* diff; and (b) the recipe's `preset + age + modules_add` composition resolves to the documented 10-module roster with no staffability warnings. This keeps the recipe honest against engine drift.

### Documentation / doctrine surface

* **Part 1** is **descriptive layer** (`docs/`) — a worked adoption recipe describing how the shipped mechanisms compose. No doctrine.
* **Part 2** is **descriptive layer** (`on-ramp/`) — the level-selection self-locate aid. No doctrine.
* **Part 3** ports established doctrine text (`doctrine/proposals.md:200-204`) into the installed adopter template. Per the doc-tier home rule and the rate-limit prompt's port exemption, this is a **sync, not a new rule** — the canonical home stays `doctrine/proposals.md`; the template gains a local copy.
* **Part 4** is a test. No doctrine.
* **The science trigger (finding 4)** is delivered through the **existing per-adopter `triage-extra-triggers` slot** (`templates/core/dev/proposals/_template.md:48-54`), whose placeholder text already names "a domain assumption class the project guards" as its intended fill. Filling a per-project slot is *not* a doctrine change; adding the trigger to the universal list in `doctrine/proposals.md:154-177` **would** be — and this proposal deliberately does **not** do that.

### Doctrine-change rate-limit (if this proposal changes doctrine)

**N/A — no new doctrine change**, and this is the load-bearing scoping decision.

The tempting move is to add a "scientific assumption / sign / unit / default-parameter / calibration-constant" trigger to the universal triage list (`doctrine/proposals.md:154-177`). That is a doctrine change and must clear the gate (`doctrine/rationale.md:323-347`). It **cannot** clear it honestly here, for two independent reasons, and I will not fake it:

1. **The high-risk bypass does not apply.** `doctrine/rationale.md:337-347` makes the single-incident bypass **exhaustive to two surfaces — a security surface and a data-loss surface** — and states plainly that "any other 'this feels urgent' framing falls outside the bypass and obeys the recurrence requirement." "Scientific rigor is Cairn's differentiator" is precisely that excluded framing. A prior proposal (`2026-07-08-claude-automated-review-committer`, R1) died on exactly this substitution; I am not repeating it.
2. **Recurrence is uncounted.** This is one design finding from one audit, not the ≥2 counted occurrences in a rolling window the gate requires (`doctrine/rationale.md:327-329`); no tracker has accrued them.

So the honest path is not (a) clearing a gate I don't pass, but (c) using an **existing non-doctrine surface that already permits it**: the `triage-extra-triggers` slot. And this is not merely a workaround — it is the *correct* home. A universal science trigger would be **wrong for non-science adopters** (not every Cairn adopter guards calibration constants); a project-specific triage trigger is inherently per-adopter, which is exactly what the slot is for. The universal list stays general; the postdoc's tree gains the trigger it needs. **No doctrine surface is touched.**

If solo-legacy scientific adopters recur — several installs filling the same science slot — that *counted* recurrence could later justify shipping the trigger as a default (e.g. baked into the scientific example or a small module), reviewed on its own and cleared honestly as recurrence-driven. That is a deferred, recurrence-gated follow-up, named here, not smuggled in now.

## Rationale

* **Which user workflow does it improve?** The first external adopter's entire adoption walk. Today a solo postdoc on a legacy tree either lands on a mis-fitting preset, silently under-installs via the naive override, or under-installs via the buggy hand-derived fallback — and then triages their first real scientific change to "just commit." The recipe gives them one verified path with the right modules, the right first artifact, and the right triage trigger.
* **What contract does it preserve / clarify?** It preserves the "compose, don't bypass" contract (`BOOTSTRAP.md:188`) — the recipe composes on top of a real preset rather than inventing a fourth one, so nothing in the engine or the install contract changes. It clarifies the level-selection routing for the solo-legacy corner the table currently drops.
* **Domain transparency / reproducibility improved?** Directly: it makes the postdoc's load-bearing scientific assumptions a written, reviewed `docs/assumptions.md` artifact in week one, and makes a later change to a default parameter *trip a proposal* via the slot-filled trigger — the exact "the science won't silently degrade" property the readiness report advertises (`codebase-readiness-report.md:292`) but the shipped triage never delivered.
* **Why now?** The postdoc install is imminent and this is the path they walk on day one. The fix must land *before* that install, and it must land *without* a doctrine change that couldn't clear review in time (or at all).

## Alternatives considered

1. **Do nothing.** Rejected — the postdoc walks a broken path on day one; the audit's Theme 5 findings stand and the differentiator misses the differentiating change.
2. **Add the science trigger to universal doctrine (`doctrine/proposals.md`).** Rejected — this is the gate-blocked move (see *Doctrine-change rate-limit*): the high-risk bypass is exhaustive to security + data-loss, recurrence is uncounted, and it over-generalizes onto non-science adopters. The slot is both the honest *and* the correct home.
3. **Ship a fourth `solo-legacy` preset** (a new `_PRESETS` entry + `_ONBOARDING_PRESETS` entry + profile YAML + onboarding task file + `BOOTSTRAP.md` gate-table row). Rejected for now — it is an engine change to `bootstrap/_scaffold/config.py` and the install-contract surface, plausibly a new abstraction under the triage triggers, and heavier review than the imminent deadline allows. The composed-profile recipe delivers the same roster today with zero engine risk. A first-class preset is a reasonable *later* follow-up if the persona recurs (see Part 4 / rate-limit note).
4. **Fix the engine so an `age` override re-derives age-gated baseline rows** (finding 2). Deferred to its own proposal — it touches `expand_preset` and therefore the install contract (a high-risk surface), it has real design questions (does *every* axis override re-derive? what about `modules_remove` interactions? does it change existing adopters' resolved rosters?), and it is a different risk class from an adopter-facing recipe. Bundling a new-behavior engine change with a doc recipe is exactly the anti-bundling error a prior review forced apart. The recipe *routes around* the gap honestly (with the `modules_add` lines and the finding-2 callout) rather than hiding it.
5. **Fix the Appendix B / `BOOTSTRAP.md:215` three-of-six default-on drift** (finding 3). Deferred to a small follow-up doc-sync — it is a factual correction to a gate-table-adjacent surface, cleanly separable, and the recipe already steers adopters *away* from the buggy hand-derived fallback toward the safe `preset + modules_add` composition, so it is not blocking for the postdoc. (Named so it is not lost.)
6. **Recommended: Parts 1–4** — the recipe + the routing fix + the escape-hatch port + the regression test, all non-doctrine, all shippable before the install, with findings 2, 3, and the first-class preset explicitly deferred.

No Maintainer chat-preference input shaped this draft; if the Maintainer has a view on the recipe's home (`docs/` vs `on-ramp/`) or on pulling finding-3's doc-sync into scope, that is an open question for review.

## Evidence / verification plan

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.** (i) The recipe's documented composition (`preset: solo-greenfield` + `age: legacy` + the four `modules_add`) resolves to exactly the 10-module roster the recipe prints, with no staffability warnings — *enforced by* the Part 4 test. (ii) The naive `{preset: solo-greenfield, age: legacy}` resolves to the 6 default-on modules with no `legacy-agent` — the finding-2 behavior, pinned so any future change to it is a deliberate diff — *enforced by* the same test. (iii) Part 3 is a faithful port: the escape-hatch paragraph in the template says no more and no less than `doctrine/proposals.md:200-204` — *enforced by* review reading, plus `check_cairn` staying clean.
* **Failure modes.** All four parts fail *closed* and *loud*: a wrong roster or a spurious warning turns the Part 4 test red; a broken cross-link or path turns `check_cairn` / `claim_check` red; there is no silent-degrade path (the recipe adds documentation and a test, and removes no guard).
* **Edge-case inventory.** The adopter who *removes* a `modules_add` line (gets a smaller roster — their choice, logged); the adopter who is solo-legacy but has *no* tests (`test_command: "no tests today"` — the recipe handles this); the greenfield-solo adopter (unaffected — they keep `solo-greenfield` plain); a future engine change to axis re-derivation (caught by invariant ii turning red — the intended trip-wire). Out of scope: the finding-2 engine fix itself, the finding-3 doc-sync, and a first-class preset.
* **Public-path → test mapping.** The one behavioral surface this proposal adds is the recipe's composition claim, mapped to the new case in [`bootstrap/tests/test_presets.py`](../../bootstrap/tests/test_presets.py) exercising `expand_preset` through its public entry (not a helper). The recipe doc, the on-ramp edit, and the template port are prose surfaces exercised by `check_cairn` (link + claim-path integrity), not pytest.
* **Known omissions / intentionally untested edges.** The prose *quality* of the recipe (is it actually readable and followable by a postdoc?) is not mechanizable — it is named as an explicit **plan-review criterion**, ideally sampled by the cross-type External read. The finding-2 engine fix and finding-3 doc-sync are deferred, not tested here.

### Tests required

* `bootstrap/tests/test_presets.py` (Part 4) — the recipe-composition invariant + the age-override-does-not-re-derive pin. Run: `python -m pytest bootstrap/tests/test_presets.py`.
* The full suite stays green: `python -m pytest bootstrap/tests`. Baseline as_of 2026-07-11 is **3 pre-existing failures** (`test_ast_attest.py` ×2, `test_evolution_infer.py` ×1) tracked separately (AST attestation re-anchor + the clock/gate findings in the maintainer's live-status memory); this proposal touches none of that surface and must not add a fourth.

### Examples / smoke checks

* `python scripts/check_cairn.py` clean over the new recipe, the edited `on-ramp/README.md`, and the ported template paragraph (link resolution + claim-path).
* `python scripts/claim_check.py` clean over this proposal and the plan.
* **End-to-end resolver dogfood** — `python bootstrap/scaffold.py --summary --config <recipe-profile>` over the recipe's exact YAML, confirming the printed roster matches the 10 modules the recipe documents (the same check the adopter is told to run). Already exercised manually this session via `expand_preset`; the plan re-runs it through the CLI summary path.
* **N/A**: no example-gallery change (`examples/`), no neutrality-surface change (`quality_gate.py --sub neutrality`) — the recipe names no vendor.

## Signals the change is wrong

* **The recipe's roster drifts from the engine** (the Part 4 test goes red on a legitimate engine change) → the composition is no longer valid; update the recipe's documented roster and the `modules_add` list in the same commit as the engine change, and re-run the `--summary` dogfood.
* **A solo-legacy adopter finds the recipe heavier than their tree earns** (they install `legacy-agent` + `security-review` but have a 500-line single-file model) → the recipe over-prescribed; add a "trim for a small legacy tree" note pointing at `modules_remove`, keeping the readiness-report pre-pass as the calibration step.
* **The `triage-extra-triggers` slot fill reads as bureaucracy** and the postdoc ignores it → the framing failed; recast it around the concrete "would the science silently degrade if a contributor changed this default?" question from `codebase-readiness-report.md:292` rather than an abstract trigger list.
* **The persona recurs and the composed-profile recipe proves too fiddly** to copy correctly across installs → the deferred first-class `solo-legacy` preset (Alt 3) is now recurrence-justified; open it as its own engine proposal.
* **Reviewers judge finding 3 (Appendix B under-count) can't be left unfixed** while the recipe ships → pull the small doc-sync into scope as a bounded addition, or land it as a separate trivial follow-up commit before the install.