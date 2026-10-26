<!-- Forward-reference + external-repo paths this proposal cites: the recipe doc it creates, and the adopter-repo `docs/assumptions.md` it points the postdoc at (which lives in the postdoc's tree, not Cairn's). -->

# The solo-legacy adopter recipe: a verified adoption path for the solo scientist + one agent + an existing research codebase

**Author**: Claude (Strategy)
**Model**: Claude Opus 4.8
**Date opened**: 2026-07-11
**Status**: accepted
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
## Review -- Claude (Internal, fresh-context subagent panel) -- 2026-07-11

**Model**: Claude Opus 4.8 (three fresh-context subagents — doctrine-conformance, evidence-feasibility, scope-adopter — no access to the authoring session; consolidated, none dropped).

**Attribution / committer note.** The panel's findings, transcribed faithfully — none softened, reordered to bury, or dropped. Per the binding practice from the superseded automated-review-committer Decision (2026-07-09), the raw panel source is committed in-tree at `dev/proposals/archive/2026-07-11-solo-legacy-internal-panel.json`; this section is committed under the Maintainer's git identity by the author-session as disclosed scribe.

**Steelman.** All three lenses converge: this is an unusually well-verified proposal and a model of navigating Cairn's known failure modes. The empirical spine is solid and independently reproduces across lenses — re-running expand_preset confirms exactly: naive {preset: solo-greenfield, age: legacy} -> the 6 default-on modules with no legacy-agent and no warning (config.py:1143-1148 static-baseline mechanism); +complexity:complex/language:multi -> still 6; and the recipe composition -> the documented 10-module roster in the exact printed order with zero staffability warnings. Every doctrine quote is faithful (rationale.md:337-347/346-347/327-329; proposals.md:154-177/200-204; readiness-report:295/299-302/363-367), and Findings 1-6 are real and reproduce. The rate-limit reasoning is honest and correct: it refuses the gate-blocked universal-triage doctrine change, reads doctrine/rationale.md:337-347 as exhaustive to security + data-loss with "differentiator => high-risk" excluded (verified verbatim), notes recurrence is uncounted, and routes the science trigger through the existing per-project triage-extra-triggers slot whose placeholder already names "a domain assumption class the project guards" (template:48-54) — the honest AND correct home, so slot-fill is not a doctrine change; LESSON #4 respected and the automated-review-committer R1 precedent faithfully invoked. Part 3's escape-hatch port is genuinely non-redundant: templates/core/AGENTS.md:76-79 and the installed template :39-40 both dead-end at a doctrine/ pointer the adopter lacks — real gap, right mechanisms. The work is built only from shipped mechanisms with no engine change (AST re-anchor correctly not triggered), and it defers the engine fix, the Appendix-B fix, and the first-class preset to their own proposals — respecting the anti-bundling and rate-limit lessons that killed prior proposals. The docs/assumptions.md week-one arc targets the differentiator well.

**Critiques** (descending severity; each grounded in a command/citation the reviewer ran):

* **[R1] (blocking)** The recipe's headline deliverable — a 'verified, copy-pasteable' YAML — does NOT parse for the zero-dependency adopter Cairn explicitly targets. The block puts inline comments on scalar lines (`preset: solo-greenfield   # ...`, `age: legacy   # ...`); config.py:34-43 uses PyYAML if present else `_minimal_yaml_parse`, and the minimal parser strips comments on list items but NOT on scalar `key: value` lines, so it hard-stops the first external adopter on day one with a confusing PresetError — the exact failure the proposal exists to prevent. Same defect, its root cause: the verification that produced the 'verified' claim never exercised the adopter path — 'Already exercised manually this session via expand_preset' bypasses YAML parsing entirely (expand_preset takes a pre-parsed dict), and this environment has PyYAML 6.0.3, so the plan's end-to-end dogfood passes silently and masks the failure; Part 4 tests roster math via expand_preset(dict), giving no coverage of the copy-pasteability claim that is the recipe's core value.
  *Grounding:* Reproduced: python3 _minimal_yaml_parse(recipe.yml) -> age='legacy                 # ...'; expand_preset -> PresetError unknown preset 'solo-greenfield     # solo staffing: ...'; config.py:34-43 (parser selection); grep -nE '^[a-z_]+:[^#]*#' bootstrap/profiles/*.yml -> NONE (no shipped profile inline-comments a scalar). Plus: proposal text 'Already exercised manually this session via expand_preset'; `import yaml` succeeds here (PyYAML 6.0.3); config.py:34-43 shows the PyYAML branch masks the minimal-parser behavior.
  *Suggested fix:* Move all comments to their own full lines (the shipped-profile convention), and re-verify the recipe YAML through `load_config`/`scaffold.py --config` under the stdlib-only path (not `expand_preset` on a hand-built dict). Run the dogfood explicitly under the no-PyYAML path (or force `_minimal_yaml_parse`), and have Part 4 add a case that round-trips the recipe's literal YAML text through `load_config`, asserting the 10-module roster — pinning copy-pasteability, not just the resolver.

* **[R2] (substantive)** Finding 5 presents a LOOSENED PARAPHRASE as a verbatim doctrine quote — the exact LESSON #1 failure mode. The proposal quotes the escape hatch as 'urgent, reversible, or experimental may proceed without a proposal, but say why'. Actual doctrine (verified) reads 'urgent, clearly reversible, or explicitly experimental ... the commit or follow-up note should say why the proposal step was skipped.' The paraphrase drops the tightening qualifiers 'clearly'/'explicitly' and compresses the say-why clause — it BROADENS the escape hatch. Since Part 3 ports this exact text and invariant (iii) demands 'no more and no less than' the doctrine, the implementer risks shipping the loosened version to every adopter.
  *Grounding:* doctrine/proposals.md:200-204 vs proposal Context finding 5
  *Suggested fix:* Quote doctrine/proposals.md:200-204 verbatim in finding 5, and state that Part 3's port must carry 'clearly reversible', 'explicitly experimental', and the full 'say why the proposal step was skipped' clause — not the broadened paraphrase.

* **[R3] (substantive)** The recipe force-adds security-review and model-selection into the canonical 10-module roster, but both FAIL their own selection gates for this persona, and doing so pre-empts the readiness-report pre-pass the same recipe prescribes. security-review is trust-boundary-first ('a place where untrusted input meets the system: deserialization, subprocess, file/network I/O, path handling, credential/env use') — a solo hydrogeology recharge model reading its own input data typically has no non-trivial trust boundary. model-selection is 'Selected when the project sits at moderate or complex on the Complexity axis... A greenfield experimental project at low complexity does not install this module' — yet the recipe keeps complexity:simple (solo-greenfield canonical, never overridden by the recipe YAML) and force-adds it anyway. The recipe's whole framing is 'readiness-report pre-pass first' to discover complexity/trust-boundaries/hidden-state, then hands the adopter a FIXED modules_add that decides those very questions before the pre-pass runs — precisely the over-provisioning Cairn's own cited doctrine warns against.
  *Grounding:* templates/modules/team-gated/security-review.md:3-11 (trust-boundary-first gate); templates/modules/team-gated/model-selection.md:3-9 ('greenfield experimental project at low complexity does not install this module'); verified via expand_preset that the recipe YAML sets only preset/age/modules_add so complexity stays 'simple'; doctrine/dual-review.md:442 ('never installs more apparatus than the team can staff'); on-ramp/README.md:40 ('sized to the work'); templates/modules/team-gated/testing-discipline.md:5-7 ('not every adoption paying for it by default')
  *Suggested fix:* Split modules_add into (a) the two the persona unconditionally needs — legacy-agent (the actual finding-2 gap) + testing-discipline (pairs with the characterization-testing age.md:52-54 prescribes for legacy) — and (b) security-review / model-selection presented as CONDITIONAL, keyed to pre-pass findings ('add security-review IF your readiness report flags a trust boundary; add model-selection IF complexity is moderate+'). This makes the recipe teach the sizing discipline instead of contradicting it; both subsets still resolve without staffability warnings.

* **[R4] (substantive)** The recipe is internally inconsistent about adoption level, and its first-proposal / week-one arc contradicts the onboarding tasks solo-greenfield actually renders. (a) Part 1 says 'Level 1 (hand-copy the kernel)', but on-ramp/README.md:29 defines Level 1 as 'No bootstrap script', while the recipe delivers a scaffold profile + `modules_add` + `scaffold.py --summary` (Level-2 machinery); and if the adopter scaffolds with `preset: solo-greenfield` (the quickstart pattern), install.py:736-738 renders solo-greenfield's onboarding tasks into PLANNING.md — 'Hello world trivial accept' (solo-greenfield.md:54-57) and 'no legacy-tree pre-pass' (solo-greenfield.md:28) — which directly contradict the recipe's week-one arc (assumptions.md-first + do the pre-pass), and the recipe delivers its arc as external prose only and never reconciles the rendered tasks. (b) Relatedly, promoting docs/assumptions.md to the 'default first real proposal' in place of the greenfield Hello-world removes the low-stakes first rep that teaches the lifecycle mechanics safely — solo-greenfield's first proposal is deliberately a 'Hello world'-style TRIVIAL accept ('the single best way to learn the apparatus by doing'); docs/assumptions.md is a real, non-trivial, science-laden artifact, so making it the postdoc's very first lifecycle experience runs their first-ever review/Decision loop on content that matters, and the readiness report's own conditional says assumptions.md should be the first ACCEPTED proposal, not the first-ever learning rep.
  *Grounding:* on-ramp/README.md:29 (Level 1 = no script); templates/onboarding/solo-greenfield.md:54-57 and :28; bootstrap/_scaffold/install.py:736-738; templates/core/dev/PLANNING.md:33,43 (slot filled by bootstrap, empty at hand-copy); templates/codebase-readiness-report.md:363-367 (Section-11-Poor conditional: assumptions.md as first artifact)
  *Suggested fix:* State the flow explicitly. If scaffold-install: instruct the adopter to override the rendered 'Hello world'/'no pre-pass' onboarding task and acknowledge the conflict. If pure hand-copy: label `--summary`/`modules_add` as a roster-computation oracle (what to copy), not the installer, and reconcile with on-ramp:29. And sequence the first proposals rather than replace: Hello-world trivial accept FIRST to learn the mechanics on something disposable, THEN docs/assumptions.md as the first SUBSTANTIVE proposal — reframe from 'in place of the Hello world' to 'after the Hello world.'

* **[R5] (substantive)** Invariant (iii) claims the faithful-port property ('the escape-hatch paragraph says no more and no less than doctrine/proposals.md:200-204') is 'enforced by review reading, plus check_cairn staying clean' — but check_cairn does link + claim-path checking only (per AGENTS.md it 'imports the same claim-path checker and adds link-checking') and structurally cannot detect semantic drift between the ported template paragraph and doctrine; the claimed automated guard does not exist, and the port creates exactly the duplication-drift failure doc-governance warns about ('copied into both files, later edited in one, and now silently contradictory'). Part 3 also breaks the template's deliberate pointer-only convention (template:39-40, :58-60, :68-69 all say 'See doctrine/... for the full rule'), creating a duplicate-text drift surface — the very thing pointer-only avoids.
  *Grounding:* doctrine/doc-governance.md:74-81 (drift failure mode); AGENTS.md check_cairn description; templates/core/dev/proposals/_template.md:39-40 (existing escape-hatch pointer), :58-60, :68-69 (pointer convention); doctrine/proposals.md:200-204
  *Suggested fix:* Drop the check_cairn clause from invariant (iii); correct the verification plan to state the port is enforced by review reading, not check_cairn, and acknowledge there is no automated drift guard for template<->doctrine fidelity — the port creates a small standing drift surface, mitigated only by keeping the ported text minimal and by review. Prefer keeping the pointer plus a short local gloss (finding-5's real need: adopters lack doctrine/ locally) over a full restatement; or add an explicit sync-note so a future doctrine edit re-syncs the template copy.

* **[R6] (substantive)** Part 3 invokes the template's port exemption but does not satisfy the exemption's own stated condition. The exemption text requires that a porting proposal 'cites the original accepting Decision and the gate does not re-apply.' The proposal cites only the doctrine location (doctrine/proposals.md:200-204), not the Decision that originally accepted the escape hatch into doctrine. Without that citation the exemption is asserted, not established.
  *Grounding:* templates/core/dev/proposals/_template.md:164-166
  *Suggested fix:* Cite the accepting Decision for the escape-hatch rule; or, if it is foundational/pre-self-hosting doctrine with no discrete dev/ Decision, state that explicitly under the port-exemption invocation so a reviewer can see the exemption's condition is met (or waived for cause).

* **[R7] (substantive)** Part 3 (porting the escape-hatch paragraph into templates/core/dev/proposals/_template.md) has a broader beneficiary scope than Parts 1/2/4 and is separable: Parts 1, 2, 4 all serve the solo-legacy persona, but Part 3 edits the UNIVERSAL installed proposal template every adopter gets and the escape hatch benefits all adopters equally — so the 'one spine' claim is overstated. Further, finding-5's own logic (the adopter lacks doctrine/ locally) applies to EVERY 'See doctrine/...' pointer in that template — including the triage-rule pointer at :39-40, arguably more important than the escape hatch — so singling out the escape hatch is a partial fix to a systematic dangling-pointer problem. This is not the fatal new-tool-vs-fixes bundling (all four parts are low-risk prose/test), so it need not force a split, but the Maintainer should be able to accept/reject Part 3 independently.
  *Grounding:* templates/core/dev/proposals/_template.md:39-40 (an existing 'See doctrine/...' pointer that also dangles for adopters lacking doctrine/) and :48-54 (the slot); the escape-hatch text lives canonically at doctrine/proposals.md:200-204
  *Suggested fix:* Either carve Part 3 out as its own trivial follow-up commit (it is a pure doctrine-text port, cleanly separable), or broaden it to address the systematic dangling-doctrine-pointer issue in the template — and in either case state explicitly that Part 3 is independently acceptable, so the Maintainer isn't forced to take the general template change to get the persona recipe.

* **[R8] (minor)** Part 2 overstates the on-ramp routing gap by omitting an existing mechanism that already partly solves it. The choosing-a-level section already maps a legacy solo project via the readiness report's G/M/P scores — 'mostly Mixed with 1-2 Poor -> Level 1 first' — i.e. the legacy->Level 1 route Part 2 proposes already exists in finer-grained form; only the coarse table row (:63) contradicts 'solo -> Level 1'. Presenting the routing as wholly broken misstates the negative space.
  *Grounding:* on-ramp/README.md:52-57 vs on-ramp/README.md:63
  *Suggested fix:* Cite on-ramp/README.md:52-57 and scope Part 2 as reconciling the coarse table row with the existing G/M/P mapping (and cross-linking the recipe), not as adding a missing route.

* **[R9] (minor)** Finding 3 (the Appendix B / I-6 summary three-of-six default-on drift) is deferred as a separate risk class, but it is a pure factual doc error in the SAME document the recipe leans on for its 'compose, don't bypass' authority (BOOTSTRAP.md:188). Verified live: BOOTSTRAP.md:696-698 lists only 3 of the 6 default-on modules, :215 repeats it, and cli.py:348-353 (the 'modules:' branch) emits no missing-default-on warning — so any adopter who wanders off the recipe to Appendix B silently under-installs. This is the same risk class as an adopter-facing doc recipe (not an engine change), and the fix is ~3 lines in 2 places; the anti-bundling lesson does not clearly bar folding it in, and the recipe should not send the postdoc to a doc containing a known-wrong hand-derivation example.
  *Grounding:* bootstrap/BOOTSTRAP.md:696-698 and :215 (both list only 3 of the 6 default-on modules; the full set is lifecycle-metrics, reflections, claim-check, fold-back-ledger, incident-trackers, documentation-plan per _DEFAULT_ON_MODULES); bootstrap/_scaffold/cli.py:348-353 (the 'modules:' branch prints no missing-default-on warning) vs :356-364 (else-branch prints the default-on set)
  *Suggested fix:* Consider folding the finding-3 doc-sync into scope as a bounded same-class factual correction (the proposal's own 'signals' section already anticipates this), or land it as a separate trivial commit BEFORE the install so the recipe's host document is not self-contradicting.

* **[R10] (minor)** Finding 1 overstates one sub-claim: it says bootstrap-lite.md:8 routes the solo persona 'to the Level 2 scaffold'. But bootstrap-lite.md:5-6 is explicitly for adopting Cairn 'without running the full Level 2 procedure in ../BOOTSTRAP.md yet' — it is a heavier middle on-ramp, not the Level 2 scaffold. The core finding (bootstrap-lite targets one-human+one-agent yet is gated on 'you have a real codebase', so the persona is mis-served) is verified and stands; only the 'Level 2 scaffold' characterization is inaccurate.
  *Grounding:* bootstrap/prompts/bootstrap-lite.md:1 (one-human+one-agent), :5-6 ('without running the full Level 2 procedure'), :8 ('you have a real codebase')
  *Suggested fix:* Reword finding 1 to say bootstrap-lite is a heavier middle path gated on 'you have a real codebase', not that it routes to the Level 2 scaffold.

* **[R11] (minor)** Doc-tier label imprecision: the routing note calls Part 2 'descriptive layer (on-ramp/).' DOCUMENTATION_PLAN.md's four-layer map locates the descriptive layer at docs/ (layer 4) and defines the entry layer by the 'how do I enter?' question, which is what on-ramp self-locate content answers. No gate consequence (on-ramp/ is not doctrine either way), but the classification is inaccurate.
  *Grounding:* docs/DOCUMENTATION_PLAN.md:39 and :115
  *Suggested fix:* Reclassify Part 2's surface as entry/on-ramp, or note that on-ramp/ is not formally placed in the four-layer map; either way confirm no doctrine gate applies.

* **[R12] (minor)** Two concerns about how the proposal handles the deferred silent engine bug (finding 2). (a) The recipe exposes that acknowledged silent engine bug to the adopter as first-contact content: Part 1's 'Why not the naive age: legacy override alone' callout explains, to a postdoc on day one, that the tool has a silent under-install path they must hand-work-around — maintainer-facing concern, not adoption-path content — which adds cognitive load and undermines confidence at the exact moment the adopter is deciding whether to trust the tool; the paired 'confirm the --summary roster matches the documented 10' step is a verification chore whose failure mode (mismatch) a moderate-git postdoc cannot diagnose. (b) Part 4's regression test pins finding-2's behavior (age override does NOT re-derive age-gated rows) as a baseline, but finding 2 is simultaneously flagged as a bug deferred to its own engine-fix proposal (Alternative 4); if that fix later lands (making the override re-derive), invariant (ii) goes red — which the proposal calls 'intended,' but a future implementer could mistake it for a regression.
  *Grounding:* The recipe's own Part 1 text ('a short, honest callout of finding 2, so the adopter understands why the modules_add lines are load-bearing'); finding 2's mechanism verified at bootstrap/_scaffold/config.py:1143-1148 (baseline is static + default-on + team-staffing re-derive only); the proposal's Part 4 / Evidence invariant (ii) ('the naive {solo-greenfield, age:legacy} resolves to the 6 default-on modules... pinned so any future change to it is a deliberate diff'); the deferred fix is Alternative 4 ('Fix the engine so an age override re-derives age-gated baseline rows')
  *Suggested fix:* Keep the modules_add workaround but frame those lines positively as 'the legacy-retrofit modules for an existing codebase' rather than 'the ones the override silently fails to add'; move the finding-2 mechanism explanation to a footnote/rationale aside for the curious, not the main path. And make the Part 4 test comment state explicitly that it pins CURRENT behavior pending the deferred finding-2 engine fix (Alt 4), not a desired invariant — so a future implementer who lands that fix knows the red is expected and updates the test as part of that change.

**Coverage.** Swept and reproduced across the panel this session. Doctrine/rate-limit substrate (all lenses, verified verbatim): the rate-limit gate doctrine/rationale.md:323-347 (two-surface security+data-loss bypass exhaustive, "differentiator => high-risk" excluded), :327-329 (recurrence uncounted), the "any other 'this feels urgent'" clause :346-347; the triage list doctrine/proposals.md:154-177 (genuinely omits science) and :175-177 ("just commit"); the escape hatch :200-204 (found finding-5's quote is a loosened paraphrase); the port exemption in both templates (core :164-166, self-hosted :179-183 — requires citing the accepting Decision); the triage-extra-triggers slot templates/core/dev/proposals/_template.md:39-54 (placeholder does name "a domain assumption class the project guards", so slot-fill is not a doctrine change); doc-governance.md:74-81 one-canonical-home/drift rule; DOCUMENTATION_PLAN.md four-layer model; dimensions/age.md:43-56; on-ramp/README.md:33/47-48/52-57/63; templates/core/AGENTS.md:76-79 (confirms Part 3 is NOT redundant); the archived automated-review-committer R1 precedent (faithfully cited). Empirical resolver core (evidence-feasibility and scope-adopter both re-ran expand_preset directly): naive {solo-greenfield, age:legacy} -> 6 default-on / no legacy-agent / no warning (config.py:906,973-988,1115-1192,1143-1148); +complexity:complex/language:multi -> still 6; recipe composition -> exact 10-module roster in documented printed order, zero staffability warnings. Test baseline: `python -m pytest bootstrap/tests` -> 3 failed (test_ast_attest x2, test_evolution_infer x1), 1408 passed — matches the as_of claim. The blocking YAML-parse defect reproduced via `_minimal_yaml_parse` + config.py:34-43. All six findings' file:line citations checked (on-ramp, bootstrap-lite:1/5/8, high-rigor-legacy.yml/.md, config.py, cli.py:348-364, BOOTSTRAP.md:188/215/696-711, template:39-54, install.py:736-738, solo-greenfield.md:25-28/54-57, readiness-report:288-305/362-367); every doctrine quote faithful; test_presets.py:148-162 (coordination guard, confirms the missing age counterpart). NOTE: the doctrine-conformance lens flagged the resolver-internals roster claims (config.py:906/973-988/1115-1200/1145-1148; cli.py:348-364) and BOOTSTRAP.md:188/215/683-711 as its own negative space (did not run expand_preset/scaffold --summary) — that negative space was exercised and confirmed by the evidence-feasibility and scope-adopter lenses. Negative space still unexercised by the whole panel: a full `scaffold.py` install into a target tree end-to-end (only expand_preset + minimal parser run — a faithful no-PyYAML simulation); the recipe under a genuinely PyYAML-absent interpreter (this env has 6.0.3); `scaffold.py --summary` through the real CLI/stderr path (format_profile_summary end-to-end); and — since the recipe doc does not yet exist — its prose readability/followability by a real postdoc, the proposal's own named non-mechanizable criterion, explicitly deferred to External.

**Second-round recommendation.** Yes — all three lenses recommend an External cross-type read before the Decision, matching the proposal's own request; scope-adopter would elevate it from "recommended" to effectively expected for this one. Reasons converge: (1) the blocking YAML-parse defect (R1) must be fixed and re-verified through the stdlib-only path before landing, and an independent read should confirm the fix rather than trust a re-run in this PyYAML-present environment; (2) the Level-1-vs-scaffold flow, the onboarding-task conflict (R4), and the routing/usability gaps sit on the exact path the first external adopter walks — routing/usability judgments a different agent type catches best; (3) recipe prose readability/followability is a named plan-review criterion no scanner reaches, unverifiable until the doc exists, best sampled by the cross-type reviewer. Per the maintainer's cross-type workflow, the standing External is the Antigravity/Gemini reviewer. Two sequencing notes: the proportionality finding (R3) and the Part-3-scope finding (R7) should be addressed — or consciously rejected — in a Response BEFORE the External read, so it evaluates the sharpened recipe rather than re-deriving the same gaps; and the one residual engine-verification item is the full `scaffold.py --summary` end-to-end path (the roster itself is already confirmed via expand_preset across two lenses). The doctrine findings are all tightening, not blocking, and none requires a doctrine-gate re-litigation.
## Response — Claude (author) — 2026-07-11

The panel's read is fair and, on the load-bearing points, correct. I reproduced the blocking and the doctrine-quote findings this session and they hold; several tightening findings caught real errors in my own draft, including a LESSON #1 misquote I should have caught before opening. The **design is sound** — compose on a real preset with `modules_add` rather than inventing a fourth preset or a hand-derived `modules:` list, and route the science trigger through the existing per-project slot rather than the gate-blocked universal-triage doctrine change. None of the findings is design-fatal. This proposal should **revise, not supersede**: R1 is a fixable verification/formatting defect in the headline artifact, and R2–R12 are tightening or scope-sharpening that the recipe is stronger for. Per-finding dispositions below; the corrected design is in *Revised proposal*.

**R1 — accept (blocking).** Reproduced this session: the recipe YAML puts comments on scalar lines (`preset: solo-greenfield   # …`), and `_minimal_yaml_parse` strips `#` only from list items, not scalar `key: value` lines (`config.py:122-134`), so under the stdlib-only path the parser yields `preset = 'solo-greenfield     # solo staffing…'` → `PresetError` — the exact day-one failure the recipe exists to prevent, masked because my "verified" run fed `expand_preset` a pre-parsed dict and this env has PyYAML 6.0.3; fix in *Revised proposal* (comments on their own lines + round-trip the literal YAML through the parser under a forced no-PyYAML path).

**R2 — accept.** Finding 5's "urgent, reversible, or experimental … but say why" is a loosened paraphrase of `doctrine/proposals.md:200-204` ("urgent, **clearly** reversible, or **explicitly** experimental … say why **the proposal step was skipped**") — a LESSON #1 violation in my own draft; I correct the quote to verbatim and require any local escape-hatch text to carry the tightening qualifiers.

**R3 — accept.** Verified against the gates: `security-review` is trust-boundary-first (`security-review.md:4-11`) and a solo hydrogeology model reading its own data typically has none, and `model-selection` explicitly "does not install" at low complexity (`model-selection.md:4-9`) while the recipe keeps `complexity: simple` — so force-adding both pre-decides the very questions the readiness pre-pass is meant to surface; I split `modules_add` into unconditional (`legacy-agent` + `testing-discipline`) and pre-pass-conditional (`security-review` IF a trust boundary, `model-selection` IF complexity is moderate+).

**R4 — accept.** Both sub-points are real: "Level 1 (hand-copy the kernel)" collides with `on-ramp/README.md:29` ("No bootstrap script") while the recipe uses `scaffold.py --summary`/`modules_add`, and promoting `docs/assumptions.md` to the *first-ever* lifecycle rep contradicts `solo-greenfield.md:54-57` and the readiness report's own "first **accepted** proposal" framing; I reframe the resolver as a roster-computation oracle (what to copy, not the installer), reconcile the rendered onboarding task, and **sequence** Hello-world-trivial-accept *first*, then `docs/assumptions.md` as the first *substantive* proposal.

**R5 — accept.** Invariant (iii) is wrong: `check_cairn` is link + claim-path only (per `AGENTS.md`) and structurally cannot detect template↔doctrine semantic drift, so I drop that clause, state the port's fidelity is enforced by review reading, keep the local text minimal, and add an explicit sync-note.

**R6 — accept.** The port exemption (`_template.md:163-166`) requires citing "the original accepting Decision"; I cite only the doctrine location — I will either cite the accepting Decision or, if the escape hatch is pre-self-hosting foundational doctrine with no discrete `dev/` Decision, state that explicitly at the invocation so the exemption's condition is visibly met (verifiable at implementation, not asserted here).

**R7 — accept.** The "one spine" claim over-reached: Part 3 edits the universal installed template and benefits all adopters, so I mark it **independently accept/rejectable** and reduce it to pointer-plus-short-local-gloss (R5's lighter form) so the Maintainer is not forced to take a universal template change to get the persona recipe.

**R8 — accept.** `on-ramp/README.md:52-57` already maps "mostly Mixed with 1-2 Poor → Level 1 first," so Part 2 is a *reconciliation of the coarse table row (:63) with the existing G/M/P mapping* plus a cross-link, not a wholly-missing route; I rescope the finding and Part 2 accordingly.

**R9 — accept with modification.** I fold in *only* the BOOTSTRAP.md factual correction (`:696-698` and the `:215` I-6 summary list 3 of 6 default-on modules) as a bounded, same-risk-class doc-only fix (new Part 5) so the recipe's cited authority document is not self-contradicting before the postdoc reads it — but I do **not** fold in `cli.py:348-353`'s missing-default-on-warning gap, which is an engine change of a different risk class and stays deferred to its own proposal (respecting LESSON #3).

**R10 — accept.** I reword finding 1: `bootstrap-lite` is a heavier *middle* on-ramp gated on "you have a real codebase" (`bootstrap-lite.md:5-6,8`), not "the Level 2 scaffold" — the mis-served-persona core stands, the characterization was loose.

**R11 — accept.** I reclassify Part 2's surface as **entry/on-ramp** rather than "descriptive layer," per `DOCUMENTATION_PLAN.md`'s four-layer map; no doctrine gate applies either way.

**R12 — accept.** (a) I reframe the `modules_add` lines positively as "the legacy-retrofit modules an existing codebase needs" and move the finding-2 silent-under-install mechanism to a rationale aside for the curious, off the postdoc's main path; (b) the Part 4 age-override pin gets a comment stating it pins **current** behavior pending the deferred finding-2 engine fix (Alt 4), so a future implementer who lands that fix reads the red as expected and updates the test in the same change.

**On sequencing.** Per the panel's note, R3 and R7 are resolved *in this Response* (not left for the External read to re-derive), so the standing External cross-type reviewer evaluates the sharpened recipe. The one residual engine-verification item — the full `scaffold.py --summary` end-to-end/stderr path — is named in the revised verification plan; the roster math itself is already confirmed via `expand_preset` across the panel and reconfirmed by me this session.

## Revised proposal — 2026-07-11

Design unchanged; five corrections and one bounded scope addition. Five parts, still one spine for Parts 1/2/4/5 (the solo-legacy persona), with **Part 3 explicitly separable and independently accept/rejectable**.

**Part 1 — recipe doc (`docs/solo-legacy-recipe.md`).**
- **Corrected YAML (R1)** — all comments on their own full lines (the shipped-profile convention; no shipped profile inline-comments a scalar). Verified this session under the stdlib-only `_minimal_yaml_parse`: it parses and `expand_preset` resolves to the documented roster.

  ```yaml
  project_name: "<your-repo>"
  test_command: "<your test command, or 'no tests today'>"

  # solo staffing: one human + one agent
  preset: solo-greenfield
  # existing codebase -- earns the readiness pre-pass greenfield skips
  age: legacy
  # legacy-retrofit modules an existing tree needs (the age-gated rows
  # the axis override does not auto-derive -- see rationale aside)
  modules_add:
    - legacy-agent
    - testing-discipline
  ```
- **Split `modules_add` (R3).** Unconditional: `legacy-agent` (the finding-2 gap) + `testing-discipline` (pairs with the characterization testing `age.md:52-54` prescribes). **Conditional, keyed to pre-pass findings:** "add `security-review` IF your readiness report flags a trust boundary; add `model-selection` IF the pre-pass places you at moderate+ complexity." This teaches the sizing discipline instead of pre-deciding it. Documented rosters (verified this session, as_of 2026-07-11): the 2-module baseline resolves to the 6 default-on + `legacy-agent` + `testing-discipline` = **8 modules, no staffability warnings**; adding both conditionals = the **10-module** roster, no warnings.
- **Level framing (R4a).** Label `scaffold.py --summary`/`modules_add` as a **roster-computation oracle** — the tool tells the adopter *which modules to hand-copy* — not the Level-2 installer; this keeps the recipe a Level-1 hand-copy path and reconciles with `on-ramp/README.md:29`.
- **Week-one arc, sequenced (R4b).** (a) fill the readiness report; (b) **Hello-world trivial accept first** — the disposable first lifecycle rep `solo-greenfield.md:54-57` is built for; (c) **then `docs/assumptions.md` as the first *substantive* proposal** — matching the readiness report's "first **accepted** proposal" framing, not the first-ever rep.
- **Finding-2 (R12a).** `modules_add` framed positively as legacy-retrofit modules; the silent-under-install mechanism moved to a "why these lines are load-bearing" rationale aside.
- **Escape hatch inline (R2).** Short local gloss using the faithful qualifiers ("urgent, **clearly** reversible, or **explicitly** experimental … the commit should **say why the proposal step was skipped**") plus a pointer.

**Part 2 — on-ramp reconciliation (`on-ramp/README.md`) (R8, R11).** Reconcile the coarse table row (`:63`) with the *existing* G/M/P mapping (`:52-57`) and cross-link the recipe; scoped as a reconciliation, not a missing route. Classified as **entry/on-ramp** layer.

**Part 3 — escape hatch in the installed template (`templates/core/dev/proposals/_template.md`) — independently accept/rejectable (R5/R6/R7).** Keep the existing `doctrine/` pointer and add a **short local gloss** (faithful qualifiers, R2) rather than a full verbatim restatement, minimizing the drift surface; add a **sync-note** so a future doctrine edit re-syncs the copy. Cite the escape hatch's accepting Decision, or state it is pre-self-hosting foundational doctrine with no discrete `dev/` Decision (R6). Verification plan no longer claims `check_cairn` guards fidelity (R5). Flagged so the Maintainer can take Parts 1/2/4/5 without Part 3.

**Part 4 — regression test (`bootstrap/tests/test_presets.py`) (R1/R12b).** (a) Round-trip the recipe's **literal YAML text** through the stdlib-only parser (`_minimal_yaml_parse` → `expand_preset`), asserting the documented roster and zero staffability warnings — pinning copy-pasteability, not just resolver math; run once forcing the no-PyYAML path. (b) Pin the naive `{solo-greenfield, age: legacy}` → 6 default-on / no `legacy-agent` behavior, with a comment stating it pins **current** behavior pending the deferred finding-2 engine fix (Alt 4).

**Part 5 (new, bounded, R9) — BOOTSTRAP.md doc-sync.** Correct `BOOTSTRAP.md:696-698` and the `:215` I-6 summary to list all six default-on modules. **Doc-only**; explicitly does not touch `cli.py:348-353`'s missing-warning behavior (engine, different risk class, deferred).

**Verification plan corrections.** Invariant (iii) drops the `check_cairn` clause (enforced by review reading + minimal ported text + sync-note). The end-to-end dogfood runs under a forced no-PyYAML path (this env has PyYAML 6.0.3, which masked R1), and adds the literal-YAML round-trip. Findings 1 and 5 quotes corrected in Context. Deferred to their own proposals, unchanged: the finding-2 engine re-derivation fix (Alt 4), `cli.py`'s missing-warning gap, and a first-class `solo-legacy` preset (Alt 3) — recurrence-gated.

**Open for the External read.** Recipe prose readability/followability by a real postdoc (named non-mechanizable criterion), the Level-1-oracle framing, and the reshaped conditional-modules guidance — the routing/usability judgments a different agent type catches best, on the exact path the first external adopter walks.

## Review -- Gemini (External, different-agent-type) -- 2026-07-22

**Model**: Gemini 3.6 Flash / Antigravity
**Verdict**: SHIP (conditional on Maintainer decision on Part 3 separability)

### Steelman
This proposal constructs a verified, zero-engine-risk adoption path (`docs/solo-legacy-recipe.md`) for the solo scientist working with one agent on an existing, legacy codebase. By composing `preset: solo-greenfield` with `age: legacy` and explicit `modules_add: [legacy-agent, testing-discipline]`, the recipe avoids the silent under-installation of the naive axis override while preserving standard-library-only execution. Splitting `security-review` and `model-selection` into conditional pre-pass recommendations respects Cairn's sizing discipline. Testing literal YAML round-tripping against `_minimal_yaml_parse` (Part 4) ensures PyYAML-independent copy-pasteability.

### Critiques

* **[E1] (Blocking Finding Verification — Stdlib Minimal Parser Execution)**
  Independent empirical verification of the revised YAML under `_minimal_yaml_parse` (`bootstrap/_scaffold/config.py:84-140`) confirms the fix:
  1. Placing comments on dedicated full lines avoids scalar-line comment mangling (where `# comment` was previously included as part of the string value).
  2. Executing `_minimal_yaml_parse` on the revised YAML string yields `{'preset': 'solo-greenfield', 'age': 'legacy', 'modules_add': ['legacy-agent', 'testing-discipline']}` without error.
  3. Passing the parsed dictionary to `expand_preset` resolves cleanly to the expected 8-module roster (`lifecycle-metrics, reflections, claim-check, fold-back-ledger, incident-trackers, documentation-plan, legacy-agent, testing-discipline`) with zero staffability warnings.

* **[E2] (Verbatim Doctrine Citation Check)**
  Verified that `doctrine/proposals.md:200-204` is quoted accurately in the Revised section and Part 3 port:
  > *"urgent, clearly reversible, or explicitly experimental ... the commit or follow-up note should say why the proposal step was skipped."*
  The previous broadened paraphrase ("urgent, reversible, or experimental ... say why") has been corrected to include the exact qualifying adverbs ("clearly", "explicitly").

* **[E3] (Sizing Discipline — Conditional Module Split)**
  The revised `modules_add` design successfully addresses the Internal panel's objection (R3). Unconditionally adding only `legacy-agent` (the finding-2 gap) and `testing-discipline` (for characterization testing) keeps the baseline lightweight (8 modules), while making `security-review` (trust boundary dependent) and `model-selection` (complexity dependent) conditional on readiness report findings.

* **[E4] (Separability of Part 3 Template Port)**
  Part 3 (adding a local escape-hatch gloss to `templates/core/dev/proposals/_template.md`) edits a universal template affecting all adopters. Marking Part 3 as independently accept/rejectable allows the Maintainer to adopt the persona recipe (Parts 1, 2, 4, 5) without altering universal template pointer conventions if strict pointer-only discipline is preferred.

### Coverage

* **Covered**:
  * Executed `_minimal_yaml_parse` and `expand_preset` via Python subshell under standard-library-only execution simulation.
  * Verified verbatim quotes against `doctrine/proposals.md:200-204` and `templates/core/dev/proposals/_template.md:39-40`.
  * Checked module staffing gates in `bootstrap/_scaffold/config.py:870-937` and `templates/modules/team-gated/`.
  * Verified `BOOTSTRAP.md:696-698` and `:215` default-on module list discrepancies.
* **Not covered**:
  * Content of `docs/solo-legacy-recipe.md` (to be created during plan execution).

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

*(Awaiting the Maintainer. The revised proposal package has cleared both Internal and External reads. Maintainer options: (1) Accept Parts 1, 2, 4, 5 and Part 3 as a complete package; or (2) Accept Parts 1, 2, 4, 5 (the solo-legacy recipe) while declining Part 3 (universal template edit) to preserve pointer-only template discipline.)*
## Response -- Claude (author, to External review) -- 2026-07-22

**Model**: Claude Opus 4.8. Proposal-Response grammar. The External read returned
**SHIP** and, critically, did not take the blocking fix on faith — it *executed*
the revised YAML through the stdlib-only path. That is exactly the verification
the Internal panel could not supply about its own finding. All four accepted.

* **[E1] accept — the blocking finding is verified closed.** The reviewer ran
  `_minimal_yaml_parse` on the revised profile and got
  `{'preset': 'solo-greenfield', 'age': 'legacy', 'modules_add': ['legacy-agent',
  'testing-discipline']}`, then resolved it through `expand_preset` to the
  intended 8-module roster with zero staffability warnings. Moving comments to
  dedicated full lines (rather than trailing scalar values) is what makes the
  recipe genuinely copy-pasteable for a zero-dependency adopter — the persona the
  whole proposal exists for. No further change.
* **[E2] accept — confirmatory, and the lesson lands.** The escape-hatch quote is
  now verbatim, including the qualifying adverbs my original paraphrase dropped
  ("*clearly* reversible", "*explicitly* experimental"). Those adverbs are
  load-bearing — a looser hatch is a wider hatch — so the correction is
  substantive, not cosmetic. This is the second time a review has caught a
  doctrine-quote drift in this series; see the cross-cutting note below.
* **[E3] accept — confirmatory.** Adding only `legacy-agent` and
  `testing-discipline` unconditionally, with `security-review` and
  `model-selection` made conditional on readiness-report findings, keeps the
  baseline at 8 modules and respects the sizing discipline
  (`doctrine/dual-review.md`: never install more apparatus than the team can
  staff). The earlier force-add would have pre-empted the readiness report's own
  job.
* **[E4] accept.** Part 3 (the local escape-hatch gloss in
  `templates/core/dev/proposals/_template.md`) is hereby marked
  **independently accept/rejectable**: it edits a *universal* template affecting
  every adopter, whereas Parts 1/2/4/5 are a persona-scoped recipe. The
  Maintainer can take the recipe without altering the pointer-only convention if
  strict pointer discipline is preferred.

**Cross-cutting note for the Decision.** Two proposals in this batch had a
doctrine-quote drift caught in review despite the authors being explicitly warned
about that exact failure mode. That is now a recurring, counted pattern rather
than an anecdote — and unlike the earlier one-off it may eventually meet the
recurrence bar the rate-limit gate requires. I am not proposing a doctrine change
here; I am flagging that the evidence is accumulating in the record.

Net: External SHIP, conditional only on the Maintainer's Part-3 separability
call. Decision-ready.

## Decision -- Anthony Kendall (Maintainer) -- 2026-07-22

**Accepted.** Scribed by Claude (Strategy) at the Maintainer's explicit,
unambiguous instruction; commit permission given in the same instruction.

Maintainer's authorization (verbatim):

> Okay, I accept your recommendations on each of these. Please scribe my
> acceptance, and mark them as accepted. When you're done with that we can go
> ahead with the follow-on proposals.

**Accepted scope: Parts 1, 2, 4, and 5** — the solo-legacy adopter recipe — **and
Part 3** (the local escape-hatch gloss in
`templates/core/dev/proposals/_template.md`).

*Recorded explicitly, because Part 3 was carved as separable:* Part 3 was marked
**independently accept/rejectable** at External review (E4) because it edits a
*universal* template affecting every adopter, whereas Parts 1/2/4/5 are a
persona-scoped recipe. The Maintainer's acceptance was given to the
recommendations as a whole and did not separately decline Part 3, so Part 3 is
accepted with the package. If the Maintainer intended to retain
pointer-only discipline in the universal template, that is a one-line
correction appended to this record — the separability is preserved, not spent.

**Why it lands.** The Internal panel's **blocking** finding was real and is now
verified closed: the headline deliverable — a "copy-pasteable" profile — did not
parse for a zero-dependency adopter, because inline comments on scalar lines are
mangled by `_minimal_yaml_parse`, the stdlib fallback used whenever PyYAML is
absent. The External reviewer did not take the fix on faith: it **executed**
`_minimal_yaml_parse` on the revised YAML and then `expand_preset`, confirming a
clean parse and the intended 8-module roster with zero staffability warnings.
That is the persona this proposal exists for.

The panel also caught a **loosened paraphrase presented as a verbatim doctrine
quote**; the escape-hatch rule now quotes `doctrine/proposals.md:200-204`
exactly, including the qualifying adverbs the paraphrase had dropped
("*clearly* reversible", "*explicitly* experimental"). Those adverbs are
load-bearing — a looser hatch is a wider hatch.

**Sizing discipline upheld:** only `legacy-agent` and `testing-discipline` are
added unconditionally (8 modules total); `security-review` and `model-selection`
are conditional on readiness-report findings rather than force-added, so the
readiness report keeps its own job.

**Next (separate commits):** open the plan (which archives this proposal),
execute, non-implementing code review, archive.
