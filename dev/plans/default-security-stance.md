<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/lifecycle.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Two populations of non-resolving path, kept separate on purpose.
     (a) ONE adopter-tree destination -- `scripts/run_security_audit.py`, where
         python-security's orchestrator lands in a Python adopter's tree. Under
         this Decision Cairn does NOT install python-security, so it never
         resolves here: not while the plan is open, not after it archives. It is
         an allow, never a `Proposed paths:` forward reference. Same directive
         and same reasoning as the source proposal.
     (b) SEVEN forward references registered under `Proposed paths:` below --
         six that materialize when Chunk D adopts content-security into Cairn's
         own tree, one when Chunk C writes its test module. The marker exempts
         only its own contiguous block and the chunk tables cite these paths
         many sections later, so they need the file-scoped directive too. Drop
         each from this directive as its path lands, per the marker discipline. -->
<!-- claim-check-allow: scripts/run_security_audit.py, scripts/content_scan.py, scripts/content_scan_runner.py, scripts/content_scan_roots.txt, scripts/content_scan_residuals.txt, scripts/content_scan_allowlist.txt, dev/modules/content-security.md, bootstrap/tests/test_default_security_stance.py -->

# Plan: the default install carries the content scanner, and the Python gate follows its token

**Source proposal**: `default-security-stance` (accepted 2026-08-03 by
Maintainer Decision, *"as amended by the author's Response"*). It currently sits
under `dev/proposals/` and moves to `dev/proposals/archive/` when it archives.
**Status**: open
**Plan review**: required(**External**, security lens) — carried verbatim from
the proposal header, where the tier is a *declared trigger* rather than a
judgement call: this is an install-contract change on a surface `AGENTS.md`
names high-risk, and it changes what every adopter receives. **No implementation
commit lands before the `## Plan review` section is in the tree.** See
*Plan review — the brief*.
**Last update**: 2026-08-04
**Opened**: 2026-08-04

## Source proposal

The proposal asked four things; the Decision granted two, narrowed one, and
withdrew one. What this plan executes is the **Decision**, not the proposal
body, and where the two disagree the Decision wins:

* **Change 1** — `content-security` becomes default-on, landing on the
  **restated** argument: measured-zero cost on fresh scaffolds, a loud one-line
  `modules_remove` opt-out that announces itself, and Cairn's own install
  already assuming the auto-load predicate. **The tautology argument is
  withdrawn** and this plan does not resurrect it (see *The argument this plan
  is allowed to make*).
* **Change 2** — `python-security` is **token-gated**: selected when the adopter
  declares a filled `python_package`, never installed for a non-Python adopter.
* **Change 3 — narrowed and partly reversed.** Per [E2] the **template source
  stays the executed authority**: `scripts/check_cairn.py` keeps its source-path
  composition and **is not edited by this plan**. **Cairn does not install
  `python-security`.** The **`content-security` parity test lands here**,
  binding Cairn's installed `scripts/content_scan.py` to the template source.
* **Change 4 — withdrawn.** `upgrade --plan` already lists new modules under
  `new modules available (opt-in)`; it becomes a property to **preserve and
  pin**, not a mechanism to build.
* **The selection-precedence rule** — an explicit `modules:` list is **exact and
  is never overridden**, not by a default-on module and not by a token trigger.
  All three profile shapes are pinned, including `token + modules: []` and
  `token + preset + modules_remove`.

The plan executes that decision; it does not re-litigate it.

## Proposed paths

Every path below is a **forward reference that materializes inside this plan**
— six of them when Chunk D runs `upgrade --adopt-module content-security` on
Cairn's own tree, one when Chunk C writes its new test file. None resolves
today. Each drops out of this list as it lands.

Proposed paths:
- `scripts/content_scan.py` — Cairn's installed `content-security` twin of the template scanner; lands in Chunk D.
- `scripts/content_scan_runner.py` — the installed advisory runner; lands in Chunk D.
- `scripts/content_scan_roots.txt` — the installed audited-roots manifest; lands in Chunk D.
- `scripts/content_scan_residuals.txt` — the installed reviewed-residual baseline; lands in Chunk D.
- `scripts/content_scan_allowlist.txt` — the installed URL allowlist; lands in Chunk D.
- `dev/modules/content-security.md` — the installed module doctrine (substituted); lands in Chunk D.
- `bootstrap/tests/test_default_security_stance.py` — the selection-contract pins; lands in Chunk C.

## The argument this plan is allowed to make

Placed before *Scope* because a plan that restates a withdrawn argument in a
docstring or a changelog line silently reinstates it, and the Decision is
explicit that it does not survive.

**Withdrawn — do not write, cite, or paraphrase.** *"`content-security`'s
selection condition is a tautology over Cairn's adopter population, so gating it
is incoherent."* [E1] falsified it with a counterexample the proposal had itself
registered as its own falsifier: an adopter whose harness receives only
operator-attached files, with no automatic discovery of `AGENTS.md`, `dev/`
artifacts or incoming diffs, while still using git-committed files as the
durable coordination channel. That is a Cairn adoption for which the auto-load
predicate is false.

**What survives, and is the only case any prose this plan writes may make:**

1. **The measured cost is zero.** The External reviewer scaffolded all three
   presets with `content-security` added, committed the generated files and ran
   the installed runner: **34 / 39 / 42 audited files, `result: clean (no
   flags)`, exit 0** on all three, `as_of 2026-08-03`. Chunk D re-measures on
   Cairn's own tree; that number is this plan's alarm-fatigue budget.
2. **The failure modes are asymmetric.** A tripwire that is not installed fails
   silently and permanently; one that is installed and noisy fails visibly and
   tunably. Untouched by [E1].
3. **The opt-out is one line and it announces itself.** `modules_remove` drops a
   default-on module and the summary carries `removed_default_on` plus an
   explicit `[info]` line. Chunk C pins that; it is the property the restated
   argument rests on, so it gets a test rather than a sentence.
4. **Cairn's own install already assumes the predicate** — `templates/core/VENDOR.md`
   exists precisely because the harness auto-loads.

## Scope

Five chunks. Executes Changes 1, 2 and the narrowed Change 3, pins Change 4 as a
preserved property, and pins the selection-precedence rule across all three
profile shapes.

**Out of scope, fenced explicitly:**

* **Any edit to `scripts/check_cairn.py`.** The proposal's original
  recommendation — repoint the scanner import at the installed copy — is
  **withdrawn as wrong** by the Decision. `check_cairn.py` keeps the deliberate
  `_SRC` + `_load_module` source-path pattern it applies uniformly to
  `claim_check.py` (`scripts/check_cairn.py:84`), `content_scan.py`
  (`scripts/check_cairn.py:91`) and `link_check.py`
  (`scripts/check_cairn.py:100`). Zero bytes change in that file, and it stays
  frozen-clean.
* **Cairn installing `python-security`.** The Decision settles it: Cairn does
  not. Consequently `dev/.cairn/profile.yml` gains **no `python_package` token**,
  and Cairn's `python_package` value is not chosen here.
* **Cairn's `security_check.py` integrity preflight.** The gap is real
  (`run_security_audit.py` refuses to run when the apparatus or its policy inputs
  are not lockfile-clean; `bootstrap/security_check.py` has no equivalent) and
  the Decision records it as a follow-up, explicitly *not* a reason to adopt a
  module sideways. Routed in *Lasting-truth migration*.
* **`templates/onboarding/high-rigor-legacy.md` lines 123 / 164.** Owned by
  `gate-claims-vs-enforcement`. Whichever lands second must not re-assert what
  this one falsifies.
* **Wiring `content_scan_runner.py` into Cairn's own gate sequence.** Chunk D
  installs it and runs it once to take the measurement. Making it a standing
  gate is `security-verification-activation`'s surface, not this plan's.
* **Parity for the three `content_scan_*.txt` policy files.** Deliberately
  **not** pinned to their template sources: a residual baseline and a roots
  manifest are adopter-tunable **by design** — Cairn curating its own residuals
  is the module working, not drift. Only the two `.py` files are byte-pinned.
  Named, with its residual, in *Author-accounting*.
* **Re-deriving the stale rows in `templates/modules/README.md`.** That table
  omits `incident-trackers` and `documentation-plan` from default-on and six
  team-gated modules, independently of this change. This plan adds the two rows
  its own change makes necessary and routes the rest.
* **Any re-anchor ceremony.** Chunk R is a Maintainer fence, not a chunk an
  implementing agent enters.

### Documentation / doctrine surface

* **Shipped module doctrine (two files, both doctrine changes in templates)** —
  `templates/modules/team-gated/content-security.md` (the **Selected when:**
  line) and `templates/modules/team-gated/python-security.md` (the "never
  default-on" sentence). The rate-limit gate (`doctrine/rationale.md` > "How the
  doctrine evolves under evidence") is cleared on the **high-risk case** limb,
  not the incident-count limb: the evidence is a standing measured state — zero
  of three presets selected either module across every release to date — on a
  surface whose failure mode is silent, and the two sentences being changed are
  the direct cause of that state.
* **Governing layer — none.** No `AGENTS.md` change. The doc-tier home rule
  routes a module's own selection condition to the module file, which is where
  both edits land.
* **Descriptive / bootstrap prose** — `bootstrap/BOOTSTRAP.md` enumerates the
  default-on roster in **three** places (Act I-5 step 2, the Act I-6 summary
  template, and the hand-derived `modules:` example). **The proposal's
  documentation section did not name this file.** It is a defect fix inside the
  surface the proposal opened — the same "as revised" reading `scan-coverage`
  applied — and is fenced into its own chunk so the Maintainer can strike it in
  one line. `templates/modules/README.md` gains two rows.
* **Generated / derived prose** — the three `bootstrap/profiles/*.yml`
  "Resulting module roster" comment blocks. All three are **already wrong**
  (they omit `incident-trackers` and `documentation-plan`), so they are
  **re-derived from a live expansion**, never hand-patched.
* **No change needed, checked rather than assumed** — `bootstrap/SAFETY.md:155`
  already names the `content-security` / `python-security` apparatus as Layer-4
  code and stays true. `bootstrap/DEPENDENCY_BUDGET.md:30` already records
  `content-security` as carrying no runtime dependency and stays true; making it
  default-on is exactly the claim that file already makes.
* **Release-facing** — one `CHANGELOG.md > Unreleased > Changed` line, routed to
  the serialization point (see *Serialized shared files*).
* **Deliberation layer** — this plan, its plan review, its code review, and the
  `dev/PLANNING.md` row-move that serializes the plan-open.

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

### Serialized shared files — not edited by an implementation chunk

`CHANGELOG.md`, `dev/PLANNING.md`, `AGENTS.md`, `docs/DOCUMENTATION_PLAN.md` and
`bootstrap/REANCHOR_RUNBOOK.md` are edited only at defined serialization points
(`AGENTS.md > Shared communication files`). This plan touches **none of them**
inside a chunk. The `CHANGELOG.md` line and the `dev/PLANNING.md` deferred-row
additions land at the archive / goodnight serialization point; their exact
content is pre-declared in *Lasting-truth migration* so the serializing agent
does not have to reconstruct it.

## The cluster constraint

**Five accepted scopes edit `bootstrap/_scaffold/config.py`** —
`profile-parse-fail-open`, this plan, `api-web-security-modules`,
`portable-security-sweeps`, and `security-verification-activation`. That is not
ordinary file overlap. `bootstrap/_scaffold/` is covered by an AST source-motion
attestation whose re-anchor ceremony pins a **falsifiable union of CHANGED
symbols agreed in advance**; a concurrent engine change from an undeclared scope
does not merely enlarge the union, it **destroys the property the ceremony
exists to provide**, because "any symbol outside the union is a stop-and-explain"
stops discriminating.

**The window is already open, measured rather than predicted.** At working-tree
HEAD `eacb7dd` on 2026-08-04, under the canonical interpreter
(`~/conda_envs/lhm/bin/python3.13`, Python 3.13.13) with
`PYTHONDONTWRITEBYTECODE=1`:

* `python -m pytest bootstrap/tests` → **1744 passed, 2 failed**, 165s. The two
  failures are `test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`
  and `::test_ast_gate_passes_over_the_full_scaffold_module_set`, reporting
  3 CHANGED symbols — `FunctionDef:cmd_upgrade` (`bootstrap/_scaffold/upgrade.py`),
  `FunctionDef:forked_facade_findings` and `FunctionDef:format_forked_facade_warning`
  (`bootstrap/_scaffold/lockfile.py`) — from a sibling's uncommitted work.
* Against the **committed** HEAD engine sources (extracted to a scratch tree,
  no repository file touched) the same verify returns **rc 0: 174 baselined
  symbols accounted for, unchanged**. So the baseline is clean at HEAD and the
  red is entirely the in-flight sibling's.

**The baseline, measured for this plan, not quoted.**
`bootstrap/tests/fixtures/scaffold_ast_baseline.json` holds **174** entries,
**161** of them `FunctionDef:` / `Assign:` / `ClassDef:` (98 / 53 / 10); the
remaining 13 are `Import:` / `Docstring` / `Expr` / `If` / `Try` keys that
`_classify()` exempts as per-module necessities. `as_of 2026-08-04`.

### This plan's declared `bootstrap/_scaffold/` symbol delta

Derived by applying this plan's intended edits to a **scratch copy of the
committed HEAD engine sources** and running the real
`bootstrap/tests/_ast_attest.py verify` against the real committed baseline. No
repository file was modified. `as_of 2026-08-04`.

**4 CHANGED (all baselined), 2 NEW, 0 MISSING, 0 DUPLICATE.**

| Class | Key | Module | Baseline digest |
|---|---|---|---|
| CHANGED | `Assign:_DEFAULT_ON_MODULES` | `bootstrap/_scaffold/config.py` | `2c8ef688f6865487` |
| CHANGED | `FunctionDef:expand_preset` | `bootstrap/_scaffold/config.py` | `6bd2e6caa83f4017` |
| CHANGED | `FunctionDef:format_profile_summary` | `bootstrap/_scaffold/config.py` | `830aac8b7c3d1bde` |
| CHANGED | `FunctionDef:main` | `bootstrap/_scaffold/cli.py` | `ff5a7441cceda605` |
| NEW | `Assign:_TOKEN_GATED_MODULES` | `bootstrap/_scaffold/config.py` | *(n/a — needs a `known_new` pin)* |
| NEW | `FunctionDef:token_gated_modules` | `bootstrap/_scaffold/config.py` | *(n/a — needs a `known_new` pin)* |

Four notes a reviewer should hold:

1. **The two NEW keys need `known_new` pins at ceremony time, and their digests
   cannot be pre-declared** — they depend on the final function body, which does
   not exist until Chunk A lands. What *is* declared in advance is the **key
   set**: exactly these two, and a third NEW non-`Import:` / non-`Docstring:`
   key from this scope is a stop-and-explain.
2. **The `DUPLICATE` hazard was checked, not assumed.** The baseline is keyed by
   bare symbol name with no module field, so a new top-level name colliding with
   a name baselined in a *different* engine module is a hard `DUPLICATE`
   ("single-source broken"), not a note. Both new names were checked against all
   161 baselined `FunctionDef:` / `Assign:` / `ClassDef:` names and are free.
   Re-check before the commit; a `DUPLICATE` on one of *this plan's* two names
   is a rename, and every other `DUPLICATE` is a stop-and-explain.
3. **`_MODULE_MAPPINGS` does **not** change.** Both modules are already
   registered with complete `InstallSpec` lists (six for `content-security`, two
   for `python-security`). This scope adds **zero manifest rows** — see *The
   install contract does not move*.
4. **The self-service repair path is unavailable.** `_ast_attest._UPDATE_ALLOWLIST`
   admits exactly four symbols — `_MODULE_MAPPINGS`, `_SKILLS_MAPPINGS`,
   `_CORE_MAPPINGS`, `install_onboarding` — and **none of this plan's four
   CHANGED symbols is among them**. `update-symbol` also refuses on more than one
   CHANGED symbol by construction. So the surgical path cannot be used here even
   for one of the four.

### One shared ceremony, and this plan does not assume it lands first

* **This plan shares one re-anchor ceremony with the rest of the cluster.** The
  **union is formed by the Maintainer at ceremony time from each scope's
  declared delta** — it is not this plan's to assemble, and this plan does not
  name the other scopes' symbols.
* **What is true regardless of intra-cluster order.** The four CHANGED keys and
  the two NEW keys above are this scope's contribution to the union whether it
  lands first, last, or in the middle: none of them is a symbol another scope
  can move on this scope's behalf, and none of this scope's edits is conditional
  on another scope's code. The engine chunk (A) and the doc chunk (B) are
  **order-independent**.
* **What is order-sensitive, named.** Chunk D — Cairn installing
  `content-security` into its own tree — creates a byte-pinned twin of
  `templates/modules/team-gated/content_scan.py`. `content-scan-detectors` and
  `separator-detection` both edit that exact file.
  * **Preferred order: Chunk D lands *after* both.** Then the twin is installed
    once, from final content, and neither sibling inherits a step it did not
    plan.
  * **If Chunk D lands first**, each of those two scopes acquires an obligation
    this plan created: re-sync the twin in the same commit as the template edit
    (`cp templates/modules/team-gated/content_scan.py scripts/content_scan.py`)
    and re-finalize the one lockfile record
    (`python bootstrap/scaffold.py upgrade --finalize scripts/content_scan.py --target .`).
    **The hazard is loud, not silent**: `test_every_self_hosted_twin_stays_byte_identical_to_its_source`
    in [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
    goes red on the omission. Chunk D's commit body must state the obligation and
    name both scopes.
  * Chunk C's test file is written before Chunk D installs the twin, so **C2's
    two twin pins are the only nodes in this plan that fail between C and D**.
    That is stated in Chunk C's acceptance rather than discovered at review.
* **Three cluster scopes add module files, which this one does not.** A new
  manifest row is an install-contract change with its own acceptance criteria.
  This plan's contribution to that surface is exactly **zero rows**, and it
  asserts that rather than assuming it.

### The install contract does not move

`AGENTS.md` calls the install contract byte-level stable and
adopter-depended-upon. This change moves **which modules a preset resolves to**,
not **what a module installs**. Measured at HEAD `eacb7dd`, `as_of 2026-08-04`:
`python bootstrap/scaffold.py --manifest` emits **96 lines** (header + 95 data
rows). Expected diff after Chunk A: **empty**. A non-empty diff means a mapping
registry was edited rather than merely read — stop and re-review, because that
is a contract change this scope did not declare.

### Gate accounting

Each figure is a dated snapshot measured for this plan, to be re-taken at
implementation rather than quoted from here.

* **Suite baseline: 1744 passed / 2 failed** (both the AST nodes, from the
  in-flight sibling), 165s, `as_of 2026-08-04`. Collection may only grow by this
  plan's new nodes; a dropped node or a new skip/xfail marker is a HOLD class.
* **Frozen files modified: four**, all in `bootstrap/tests/`, all literal keys in
  the 164-entry `frozen_files` map (`as_of 2026-08-04`) —
  `test_notice_install.py` (C2), `test_security_stack.py` (C3),
  `test_presets.py` and `test_profiles_smoke.py` (C4, docstring-only). Plus one
  **`FROZEN-NEW`**: `bootstrap/tests/test_default_security_stance.py` (C1).
  `bootstrap/_scaffold/config.py` and `bootstrap/_scaffold/cli.py` are **not** in
  `frozen_files`; `config.py` appears under `cascade_mutable` with a
  `pre_run_sha256` and the note *"one predeclared mapping-symbol delta only"* —
  a stale artifact of a closed batch window (its sibling `collection.node_count`
  reads **1598** against today's 1746), so the plan records the state and leaves
  the re-pin decision to Chunk R.
* **`scripts/check_cairn.py` is frozen and is not touched** — zero bytes, per the
  Decision. That is checkable with `git diff scripts/check_cairn.py` returning
  empty at every commit.
* **Prose integrity** — `python scripts/check_cairn.py` → `OK -- 180 Markdown
  file(s) scanned; no issues; 68 external link(s) not probed`, `as_of
  2026-08-04`. Chunk D adds `dev/modules/content-security.md`, so the count grows
  by one plus whatever `dev/` artifacts this lifecycle itself contributes.
* **The release Bandit gate** — `scan_targets()` returns **74** targets,
  `as_of 2026-08-04`. After Chunk D it returns **76**: Cairn's own
  `scripts/*.py` glob picks up `scripts/content_scan.py` and
  `scripts/content_scan_runner.py`, whose template twins were already in the
  manifest-derived set. Both new targets are byte-identical to files Bandit
  already reads, so the severity histogram must not gain a MEDIUM+.
* **Cairn's lockfile** — `dev/.cairn/cairn-lock.yml` records **81 files / 14
  modules**, `as_of 2026-08-04`. After Chunk D: **87 files / 15 modules**. Five
  records currently carry legitimate customization drift (`AGENTS.md`,
  `dev/NEXT_SESSION.md`, `dev/PLANNING.md`, `dev/collaboration_agreement.md`,
  `dev/modules/security-review.md`); **all 41 existing `scripts/` + `tools/`
  twins are hash-clean**, which is the invariant Chunk D must not break.

## Sequence

Chunk order is load-bearing. **C lands before D**: the twin pins must exist and
be red-for-the-right-reason before the twin is installed, so that "the test went
green" is evidence the install happened rather than evidence the test never
looked.

```
0. plan-open -- this plan + the dev/PLANNING.md row-move            [commit pending]
   (plan review) -- required(External, security lens); NO code before it lands
1. Chunk A -- engine: default-on + the token gate                   [commit pending]
2. Chunk B -- the doctrine and prose the engine change falsifies    [commit pending]
3. Chunk C -- the selection contract, pinned with literal names     [commit pending]
4. Chunk D -- Cairn adopts content-security on itself               [commit pending]
   Chunk R -- MAINTAINER FENCE: the shared re-anchor ceremony       [Maintainer]
```

---

### Chunk A — engine: `content-security` default-on, `python-security` token-gated

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/_scaffold/config.py` | `_DEFAULT_ON_MODULES` gains `"content-security"` (6 → 7 entries), appended last so `_canonical_order`'s existing ordering for the six is unchanged. The adjacent comment states the restated argument in one clause — measured-zero cost + a loud `modules_remove` opt-out — and **must not** state the withdrawn tautology. |
| A2 | `bootstrap/_scaffold/config.py` | New `_TOKEN_GATED_MODULES: dict[str, tuple[str, ...]] = {"python-security": ("python_package",)}`, placed beside `_MODULE_REQUIRED_TOKENS`. Its comment must say why the two tables are **not** merged despite carrying the same pair today: `_MODULE_REQUIRED_TOKENS` means *"if selected, this token must be filled"* (a fail-closed pre-write gate); `_TOKEN_GATED_MODULES` means *"a filled token selects this"*. Merging them would make every future required-token module auto-install itself. |
| A3 | `bootstrap/_scaffold/config.py` | New `token_gated_modules(cfg) -> list[str]`: for each entry, select the module iff **every** gating token is present, non-blank after `.strip()`, and not still an unfilled `{{placeholder}}` — reusing the existing `_UNFILLED_TOKEN_VALUE` regex rather than a second definition of "filled". Pure: reads no filesystem, mutates nothing. |
| A4 | `bootstrap/_scaffold/config.py` | `expand_preset`: after the team-staffing gate and **before** `modules_add` / `modules_remove`, `baseline |= set(token_gated_modules(cfg))`. Placement is the contract, not a detail — it is what makes `modules_remove: [python-security]` win against a declared token, per the Decision's conservative rule. The summary dict gains `"token_gated"` (the token-selected modules that survived into the final roster). |
| A5 | `bootstrap/_scaffold/config.py` | `format_profile_summary` gains one line, `Token-gated (selected by a declared token): …`, emitted only when non-empty. This is the pre-install acceptance artifact; a security module appearing in the roster with no stated cause is exactly the silent-materialization failure the proposal was opened over. |
| A6 | `bootstrap/_scaffold/cli.py` | `main`'s **no-key** branch (`modules = list(_DEFAULT_ON_MODULES)`) appends `token_gated_modules(cfg)`, and its `[info]` line names the token-gated additions separately from the default-on set so the printed message stays true. **The `modules:`-alone branch is not touched** — that is the exact-list contract, and leaving it alone is the implementation of the Decision's precedence rule. |

**Acceptance criteria — Chunk A.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_presets.py bootstrap/tests/test_profiles_smoke.py bootstrap/tests/test_config_module.py -q` → green.
* **The install contract is unchanged.** Capture `python bootstrap/scaffold.py
  --manifest` to the session scratch directory at the plan-open commit; diff
  after A6. **Expected empty**, 96 lines / 95 data rows.
* **The declared symbol delta is exactly what lands.**
  `python bootstrap/tests/_ast_attest.py verify bootstrap/tests/fixtures/scaffold_ast_baseline.json bootstrap/_scaffold/*.py`
  reports **4 CHANGED** — and exactly the four in the table — **0 MISSING, 0
  DUPLICATE**, and **2 NEW non-`Import:` / non-`Docstring` keys** with the two
  declared names. Any fifth CHANGED or third NEW key attributable to this scope
  is a stop-and-explain before the commit, not a ceremony-time discovery. *(The
  sibling's in-flight symbols will also appear; the assertion is over **this
  scope's** contribution, established by diffing against the same verify run on
  the pre-chunk working tree.)*
* **The suite is red on exactly two nodes and no others** from this commit until
  Chunk R: the two `test_ast_attest.py` nodes. Any third failure is this plan's
  to explain.
* **Channel note.** Nothing in this chunk is self-verifying: A1–A6 change the
  subject only. Every oracle lives in Chunk C, written from literal module names
  typed by hand, never derived from `_DEFAULT_ON_MODULES` or
  `_TOKEN_GATED_MODULES`.

---

### Chunk B — the doctrine and prose the engine change falsifies

Every quoted sentence below is quoted from the tree at plan-authoring time.
**Re-read each file before editing**; siblings may have moved them.

| # | File | Change |
|---|------|--------|
| B1 | `templates/modules/team-gated/content-security.md` | The **Selected when:** line (currently *"the team's agents auto-load text files from the working tree … Team-gated."*) becomes a default-on statement: installed by default, with the one-line `modules_remove: [content-security]` opt-out named explicitly and the adopter shape it is for — an adopter whose agents receive only operator-attached files — named honestly, because that is the [E1] adopter. The body's threat description is unchanged and stays correct. |
| B2 | `templates/modules/team-gated/python-security.md` | The sentence *"Team-gated and **opt-in**: never default-on, and never installed for a non-Python adopter."* becomes the Decision's wording: **token-gated** — selected automatically when the adopter declares a `python_package` token, **and never installed for a non-Python adopter**. That second clause is preserved **verbatim**; it is the half that carries the safety property. |
| B3 | `bootstrap/profiles/solo-greenfield.yml`, `collaborative-team.yml`, `high-rigor-legacy.yml` | The "Resulting module roster" comment block in each is **re-derived from a live `expand_preset` run**, not hand-patched. All three are already wrong today (each omits `incident-trackers` and `documentation-plan`), so hand-patching would propagate an existing error. Record the derivation command in the commit body. |
| B4 | `bootstrap/BOOTSTRAP.md` | Three enumerations of the default-on roster — Act I-5 step 2 (`bootstrap/BOOTSTRAP.md:108`), the Act I-6 summary template (`bootstrap/BOOTSTRAP.md:215`), and the hand-derived `modules:` example (`bootstrap/BOOTSTRAP.md:703`) — gain `content-security`. The Act I-5 entry also gains one sentence on the token-gated tier and one on the exact-list rule: **a `modules:` list is exact and is never widened by a default-on module or a token trigger.** |
| B5 | `templates/modules/README.md` | Two rows in "The modules" table: `default-on \| content-security \| …` and a token-gated row for `python-security`. The table's four pre-existing omissions are **not** fixed here; routed in *Lasting-truth migration*. |

**Acceptance criteria — Chunk B.**

* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → OK; the Markdown
  count may only grow.
* `~/conda_envs/lhm/bin/python3.13 scripts/quality_gate.py --sub neutrality` →
  unchanged. `templates/` and `bootstrap/*.md` are both inside its scan roots,
  so every edit above passes through it; the figure must not move.
* `~/conda_envs/lhm/bin/python3.13 scripts/claim_check.py <file>` over each
  edited Markdown file, **one file per invocation** — the checker takes a single
  path and exits 2 on more.
* **B3's rosters agree with the code, checked by running it**, not by reading
  it: for each preset, `expand_preset({"preset": p})[0]` is compared against the
  comment block by eye at implementation, and the three rosters are pinned by
  test in Chunk C.
* **Channel note.** The claim is "the prose now matches the selector". The
  evidence is a *live expansion run*, not a reading of the prose just written.
  `check_cairn` verifies link and claim-path integrity — it catches drift, never
  absence, and this plan does not lean on it for truth.

---

### Chunk C — the selection contract, pinned with literal names

The heart of the plan, and the chunk a reviewer should read first. **Every
existing guard over the default-on roster derives its oracle from
`_DEFAULT_ON_MODULES` itself** and will therefore go green on Chunk A
automatically, having verified nothing:

* `bootstrap/tests/test_presets.py:91` — `test_default_on_always_present`
  asserts `_DEFAULT_ON <= _roster(...)` where `_DEFAULT_ON` **is** the table
  under test.
* `bootstrap/tests/test_profiles_smoke.py:112` — `for default_on in
  _DEFAULT_ON_MODULES: assert default_on in modules`, the same shape.
* `bootstrap/tests/test_profiles_smoke.py:227` — the same loop against
  `--summary` stdout.

That is the `scan-coverage` Defect-2 shape one abstraction up. **The oracle in
every new test below is a module name typed by a human into the test file.**

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/tests/test_default_security_stance.py` *(new)* | Ten pins, listed with their perturbations below. Preset names are typed as the literal tuple `("solo-greenfield", "collaborative-team", "high-rigor-legacy")` — **not** `_PRESETS.keys()`, which would make the test vacuous the day a preset is removed. |
| C2 | `bootstrap/tests/test_notice_install.py` | The Decision's parity test, as a **named** pair pin: `test_content_scan_twin_is_present_and_byte_identical` asserts `("scripts/content_scan.py", "templates/modules/team-gated/content_scan.py")` is a member of `_self_hosted_twins()` **and** that the two files are byte-equal; likewise for `content_scan_runner.py`. The existing generic `test_every_self_hosted_twin_stays_byte_identical_to_its_source` is **presence-derived** — `_self_hosted_twins()` discovers twins by globbing `scripts/`/`tools/` — so deleting the installed copy silently shrinks the twin set and leaves the generic test green. The named pin is what closes that, and its perturbation is *deletion*, not a byte edit. **Frozen file.** |
| C3 | `bootstrap/tests/test_security_stack.py` | `test_python_security_not_in_any_default_or_preset` keeps both assertions (they stay true: token-gating adds the module at expansion time, not to `_DEFAULT_ON_MODULES` or a preset baseline) but its **name now over-reads as "never selected automatically"**. Renamed to `test_python_security_is_never_default_on_or_in_a_preset_baseline`, with a docstring naming the token gate as the one path that does select it and pointing at C1's pins. A test whose name retires a question it does not answer is worse than a missing test. **Frozen file.** |
| C4 | `bootstrap/tests/test_presets.py`, `bootstrap/tests/test_profiles_smoke.py` | **Docstring-only.** The three tautological guards above are *kept* — they pin "the expansion consumes the table", which is real — and each gains one sentence stating what it cannot do (fail on a change to the table itself) and naming C1a as the guard that can. Both **frozen files**; no assertion changes, so no behaviour rides on a frozen-file edit. |

**The ten C1 pins, each with the perturbation that makes it RED.** Every
perturbation below targets **the hazard**, never the test's own body: perturbing
a test's body validates the test, and only perturbing the hazard validates the
claim. Each is **run**, its failure observed, and the byte-identical restore
verified with `git diff <path>` returning empty; the ledger goes in the commit
body.

| Pin | Asserts | Perturbation (RUN) |
|---|---|---|
| C1a `test_content_security_is_in_every_shipped_preset_roster` | `"content-security" in expand_preset({"preset": p})[0]` for the three literal preset names | Remove `"content-security"` from `_DEFAULT_ON_MODULES` → red, naming all three presets |
| C1b `test_content_security_reaches_the_no_key_default_shape` | A profile with neither `preset:` nor `modules:` installs `scripts/content_scan.py` into `tmp_path` | Same removal → red *(and it is a **different** code path from C1a: `cli.main`'s no-key branch, not `expand_preset`)* |
| C1c `test_an_exact_modules_list_is_never_widened_by_the_default_on_module` | `modules: [claim-check]` → neither `scripts/content_scan.py` nor `dev/modules/content-security.md` exists | Make `cli.main`'s `modules:`-alone branch union `_DEFAULT_ON_MODULES` → red |
| C1d `test_modules_empty_list_opts_out_entirely` | `modules: []` **with** `python_package: mypkg` → no `content_scan.py`, no `run_security_audit.py` | Same as C1c, and independently: make `token_gated_modules` apply to the exact-list branch → red |
| C1e `test_python_security_is_selected_when_the_token_is_declared` | `preset: solo-greenfield` + `python_package: mypkg` → `scripts/run_security_audit.py` exists | Delete the `baseline |= set(token_gated_modules(cfg))` line in `expand_preset` → red |
| C1f `test_python_security_is_absent_without_the_token` | `preset: solo-greenfield`, no token → `run_security_audit.py` absent **and** rc == 0 | Make `_TOKEN_GATED_MODULES`'s gate unconditional → red. Asserting **both** absence and rc catches either direction: an unconditional select makes the install exit 2 (`refusing to install (no files written)`), which the rc assertion catches even though the file is still absent |
| C1g `test_the_token_gate_does_not_override_modules_remove` | `preset: solo-greenfield` + `python_package: mypkg` + `modules_remove: [python-security]` → absent | Move A4's union from before the overrides to after them → red. **This is the pin for the Decision's conservative rule** |
| C1h `test_content_security_opts_out_loudly` | `preset: solo-greenfield` + `modules_remove: [content-security]` → absent from the roster **and** present in `summary["removed_default_on"]` | Remove `"content-security"` from `_DEFAULT_ON_MODULES` → `removed_default_on` comes back empty → red. **This is the pin under the restated argument's "loud opt-out" limb** |
| C1i `test_an_unfilled_python_package_token_does_not_select` | `python_package: "{{python_package}}"` and `python_package: "   "` each → not selected | Drop the `_UNFILLED_TOKEN_VALUE` / `.strip()` check from `token_gated_modules` → red on both cases |
| C1j `test_the_profile_summary_names_the_token_gated_addition` | `scaffold.py --summary` over a preset + filled token names `python-security` under the token-gated line | Delete A5's summary line → red |

**Two further pins in C1, both non-obvious and both required by the Decision:**

* **C1k `test_a_new_default_on_module_stays_opt_in_for_an_existing_adopter`** —
  Change 4 as a *preserved property*. Install into `tmp_path` with an exact
  `modules:` list lacking `content-security`; run `upgrade --plan`; assert
  stdout carries `new modules available (opt-in)` naming `content-security`, and
  that `scripts/content_scan.py` was **not** written. **Perturbation:** delete
  the `new modules available (opt-in)` listing block from `cmd_upgrade` in
  `bootstrap/_scaffold/upgrade.py` → red. **Cite it by its printed string, not by
  line number**: that file is under concurrent edit and the line already moved
  once while this plan was being written. Note the collision — `cmd_upgrade` is a
  symbol a sibling scope is editing right now, so the perturbation must be
  restored byte-identically and verified with `git diff bootstrap/_scaffold/upgrade.py`
  against the **pre-perturbation** state, not against HEAD.
* **C1l `test_a_declared_token_never_conscripts_a_module_into_an_exact_list`** —
  the composite the Decision names: `token + preset + modules_remove` (C1g) and
  `token + modules: []` (C1d) are the two shapes it calls out by name, and this
  pin is the third leg: `modules: [claim-check]` **with** `python_package:
  mypkg` → `run_security_audit.py` absent and rc == 0.

**Acceptance criteria — Chunk C.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_default_security_stance.py bootstrap/tests/test_notice_install.py bootstrap/tests/test_security_stack.py -q` → all pass **except** C2's two twin pins, which **fail until Chunk D installs the twins**. That is stated here rather than discovered: a test written against a file that does not exist yet is red for the right reason, and its going green at Chunk D is the evidence that the install happened.
* **C2's discriminating perturbation, and it is the one that matters.** After
  Chunk D: (i) `git mv scripts/content_scan.py <scratch>/` → **C2's named pin
  fails while `test_every_self_hosted_twin_stays_byte_identical_to_its_source`
  stays green**. That pair is the entire argument for C2 and is what makes it a
  test rather than a restatement. Restore, confirm `git status --short` clean.
  (ii) Append one byte to `scripts/content_scan.py` → **both** fail. Restore,
  confirm clean.
* **Every new node shown non-vacuous by a RUN perturbation**, ledger in the
  commit body — the change made, the failure observed with its message, the
  byte-identical restore verified.
* **Channel note.** Subject: `expand_preset` / `cli.main` / `_self_hosted_twins`.
  Oracles: literal module names and literal preset names typed into the test
  file, and — for C1b through C1l — the **presence or absence of files in a
  scaffolded `tmp_path` tree**, which the selector never reads. The independence
  is demonstrated rather than asserted: under C1a's perturbation the table
  changes and the typed literals do not, and the two come apart.

---

### Chunk D — Cairn adopts `content-security` on its own tree

Order-sensitive; see *The cluster constraint*. This is the half that answers the
Maintainer's direction directly, and under the Decision it is much smaller than
the proposal drafted.

| # | File / action | Change |
|---|------|--------|
| D1 | `python bootstrap/scaffold.py upgrade --adopt-module content-security --target .` | The **adopter-facing** mechanism, deliberately — Cairn dogfoods the same opt-in path an existing adopter uses. It installs each spec's `dst` that is missing on disk and records six lockfile entries: `dev/modules/content-security.md` (substituted → `base_cache` + `base_hash`), `scripts/content_scan.py`, `scripts/content_scan_runner.py`, and the three `content_scan_*.txt` policy files (all verbatim). **Not a hand-edit of `dev/.cairn/cairn-lock.yml`** — that file is tool-owned and regenerate-only, and [E3] is on record that hand-editing it inverts the documented workflow. |
| D2 | `dev/.cairn/profile.yml` | **No edit, and that is a decision rather than an omission.** Cairn's profile is `preset: collaborative-team`, which after Chunk A resolves to include `content-security` mechanically. Adding `modules_add: [content-security]` would be redundant *and* actively harmful: it would mask the default-on path, so a regression that dropped the module from `_DEFAULT_ON_MODULES` would leave Cairn's own tree silently unaffected — the repository would stop being its own first adopter for exactly the property under test. And per the Decision, no `python_package` token is added. |
| D3 | `scripts/content_scan_residuals.txt` | Run `python scripts/content_scan_runner.py` once over Cairn's tree and **record the flag count in the commit body**. The three REQUIRED roots (`AGENTS.md`, `.agents/skills`, `dev`) all exist in Cairn — verified `as_of 2026-08-04` — so the runner will not fail closed on a missing root. If flags appear, each residual added carries its own reviewed rationale; a blanket suppression is the alarm-fatigue failure the proposal names and is not acceptable here. **If the count is non-trivial, that is a *Signals the change is wrong* trigger: stop and put it to the Maintainer rather than curating it away.** |
| D4 | — | Confirm the twin invariant Chunk D must not break: all `scripts/` + `tools/` `.py` lockfile records stay hash-clean (41 today, 43 after). |

**Acceptance criteria — Chunk D.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_notice_install.py -q` → green, **including C2's two named pins**, which were red before this chunk. That transition is the acceptance evidence.
* `~/conda_envs/lhm/bin/python3.13 bootstrap/security_check.py` → `PASS`, target
  count **76** (from 74). Both new targets are byte-identical to template files
  Bandit already reads, so the severity histogram gains **no MEDIUM+**; a
  MEDIUM+ appearing is a stop.
* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → OK, count +1 for
  `dev/modules/content-security.md`.
* **The lockfile moved exactly as predicted**: 81 → **87** files, 14 → **15**
  modules. Re-derive rather than trust: parse the lock and count. The five
  pre-existing customization-drifted records are unchanged in number.
* **The content-scan measurement is recorded, not just passed.** The flag count
  from D3 goes in the commit body as a number, even when it is zero — that
  number is this plan's alarm-fatigue budget and the External reviewer's
  34 / 39 / 42-file clean runs are the comparison.
* **The obligation this chunk creates is stated in its own commit body**: any
  later edit to `templates/modules/team-gated/content_scan.py` must re-sync
  `scripts/content_scan.py` and re-finalize its lockfile record in the same
  commit. Name `content-scan-detectors` and `separator-detection` explicitly.
* **Channel note.** Subject: the scaffold's adopt path. Oracle: the **contents of
  Cairn's own working tree and lockfile after the command ran**, read back
  independently — not the command's own success message.

---

### Chunk R — MAINTAINER FENCE

> **An implementing agent does not enter this chunk.** The AST attestation is
> the gate that would catch an implementer smuggling an undeclared engine
> change; an implementer who re-anchors it is blessing their own gate. The
> implementing agent's work **ends at Chunk D plus a stated readiness
> condition**. The agent may *prepare and dry-run* the correction — that is the
> `lockfile-provenance-fields` precedent — but the Maintainer runs the real one
> and authors the commit.

1. **Readiness condition.** All four implementation chunks are in the tree, the
   suite is green **except** the two `test_ast_attest.py` nodes, and this plan's
   contribution to the union is exactly the declared four CHANGED + two NEW keys.
2. **The AST baseline re-anchor** (`bootstrap/tests/fixtures/scaffold_ast_baseline.json`)
   — **not** `bootstrap/REANCHOR_RUNBOOK.md`, which governs a different gate and
   contains zero mentions of `ast_attest` or `scaffold_ast_baseline` (already
   `dev/PLANNING.md`'s deferred Maintainer question 4). The mechanism is the
   Maintainer-run, dry-run-verified direct-correction script established by
   `lockfile-provenance-fields`. **`update-symbol` is unavailable** for this
   scope on two independent grounds: its allowlist admits four symbols and none
   of this plan's four is among them, and it refuses on more than one CHANGED
   symbol by construction. **The union is the Maintainer's to form** from each
   cluster scope's declared delta; a symbol outside the union is a stop.
3. **The `known_new` manifest.** The two NEW keys —
   `Assign:_TOKEN_GATED_MODULES` and `FunctionDef:token_gated_modules` — need
   digest pins in `bootstrap/tests/fixtures/scaffold_ast_known_new.json`,
   measured at ceremony time against the landed bodies. Their **key set** is
   declared in advance; their digests cannot be.
4. **The frozen-set decision.** Four frozen files are modified and one is
   `FROZEN-NEW`; `bootstrap/tests/fixtures/gate_manifest.json` also carries a
   `cascade_mutable` entry for `bootstrap/_scaffold/config.py` and a
   `collection.node_count` of 1598 against today's 1746, both stale from a
   closed window. Whether to re-pin, and whether the stale entries are cleared
   here or routed onward, is the Maintainer's call. **This plan does not
   re-pin**; it records the delta.
5. **Green.** `python -m pytest bootstrap/tests` returns to 0 failed / 0 skipped.

**Nothing in this plan requires a key, credential, token, or signing material.**
Stated explicitly so its absence is a checked fact rather than an omission.

## Acceptance criteria

Per-chunk criteria are above; these are the plan-level deliverables.

* **Tests that must pass.**
  * `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` — the whole
    suite, **0 failed / 0 skipped / 0 xfailed** after Chunk R, under the
    canonical interpreter (3.13.13) with `PYTHONDONTWRITEBYTECODE=1`. Baseline
    **1744 passed / 2 failed**, `as_of 2026-08-04` (the 2 are the in-flight
    sibling's). Collection grows by exactly this plan's new nodes and drops none.
  * `bootstrap/tests/test_default_security_stance.py` *(new; a `Proposed paths:`
    entry until Chunk C)* — the twelve selection-contract pins.
  * [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
    — the two named twin pins (C2), green only after Chunk D.
  * [`bootstrap/tests/test_security_stack.py`](../../bootstrap/tests/test_security_stack.py)
    — the renamed and re-documented never-default-on test (C3), plus its existing
    module-matrix suite unchanged and green.
  * [`bootstrap/tests/test_presets.py`](../../bootstrap/tests/test_presets.py) and
    [`bootstrap/tests/test_profiles_smoke.py`](../../bootstrap/tests/test_profiles_smoke.py)
    — green, with the three tautological guards documented rather than deleted.
  * [`bootstrap/tests/test_config_module.py`](../../bootstrap/tests/test_config_module.py)
    — unchanged and green; it pins the config module's exported surface, which
    gains two names.
  * **Every new node shown non-vacuous by a RUN perturbation**, with the ledger
    in the commit body. Where a test *cannot* be made to fail, the plan says so
    instead — the three inherited tautological guards in C4 are exactly that case
    and are documented, not claimed.
* **Doc updates that must land.** All hand-authored: the two shipped module docs
  (B1, B2), the three profile roster comments (B3, re-derived from a live run
  rather than edited), `bootstrap/BOOTSTRAP.md` × 3 sites (B4),
  `templates/modules/README.md` × 2 rows (B5). No generated docs, no
  snippet-synced blocks. `CHANGELOG.md > Unreleased > Changed` is **routed to the
  serialization point**, pre-declared in *Lasting-truth migration*.
* **Examples / smoke checks required.** `python bootstrap/scaffold.py --manifest`
  — expected **unchanged**, which is itself the assertion that this plan adds no
  install-contract row. `python bootstrap/scaffold.py --summary --config
  <fixture>` for a preset + filled token — expected to name the token-gated
  addition (pinned by C1j). `python scripts/content_scan_runner.py` on Cairn's
  own tree after Chunk D — the alarm-fatigue measurement. **N/A**: the runnable
  gallery under `examples/` — this change touches nothing it demonstrates.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk and the test that enforces it.**
  * *No non-Python adopter receives `python-security`.* Necessary holds (the
    required-token preflight refuses, `exit 2`, no files written); **sufficient
    does not**, and the proposal's "necessary and sufficient" phrasing is false
    as written and does not survive into this plan. Enforced by C1f and C1l.
  * *An explicit `modules:` list is exact and is never widened.* Enforced by
    C1c, C1d, C1l — three shapes, three tests, because a single test over one
    shape would leave the other two unguarded.
  * *`modules_remove` wins against a token trigger.* Enforced by C1g, whose
    perturbation is precisely the placement error (union after the overrides
    instead of before).
  * *The default-on opt-out stays loud.* Enforced by C1h, which asserts the
    `removed_default_on` disclosure and not merely the absence.
  * *One authoritative scanner; the installed copy never diverges from the
    template source.* Enforced by C2's named pins, whose discriminating
    perturbation is deletion. **The template source remains the executed
    authority** — `check_cairn.py` is not edited.
  * *A new default-on module is not silently materialized on upgrade.* Enforced
    by C1k, pinning behaviour that already ships rather than building it.
  * *The published install manifest does not move.* Enforced by the diff against
    a pre-change capture, in Chunk A's acceptance.
  * *The scan set cannot silently shrink.* Pre-existing and unchanged:
    `content_scan_roots.txt` is fail-closed on a missing REQUIRED root and on an
    audited set that resolves to zero files. Chunk D verifies Cairn satisfies the
    three REQUIRED roots rather than assuming it.
* **Public-path → test mapping.** The public entry points this plan touches are
  `expand_preset`, `format_profile_summary` and `cli.main`. `expand_preset` and
  `format_profile_summary` are exercised directly (C1a, C1e, C1g, C1h, C1j);
  `cli.main` is exercised **through its real CLI path into a scaffolded
  `tmp_path` tree** (C1b, C1c, C1d, C1f, C1l) using the `_install_modules` idiom
  already established in
  [`bootstrap/tests/test_security_stack.py`](../../bootstrap/tests/test_security_stack.py),
  never through a stub of itself. No test stubs the function it is verifying.
* **Failure modes.**
  * A declared-but-wrong `python_package` → **already closed upstream**, verified
    by the External reviewer: installation proceeds, and the installed audit
    exits 20 with `preflight: DEGRADED (fail-closed; no passes ran)`. "Did not
    scan" does not read as "clean". This plan changes nothing there.
  * An unfilled or placeholder `python_package` → **closed** by A3's fill check,
    pinned by C1i. Without it, `python_package: "{{python_package}}"` would
    select the module and then be refused by the required-token preflight — a
    confusing `exit 2` on a profile the adopter never meant to opt in with.
  * An adopter who has already hand-selected `content-security` → **idempotent**:
    a set union, and `--adopt-module` is a documented no-op when the module is
    already locked.
  * An adopter whose `scripts/content_scan.py` already exists with different
    content → the standard install collision path, unchanged by this plan.
  * A template edit to `content_scan.py` without a twin re-sync → **open at the
    engine, closed at the test** (C2 + the generic byte-identity test). Named as
    an obligation on two sibling scopes rather than mitigated.
  * The three policy `.txt` files diverging from their template sources →
    **deliberately unguarded**; that is adopter tuning, not drift. The residual:
    an *accidental* Cairn-side edit to `content_scan_roots.txt` that narrows
    coverage would not be caught by a parity test. It would still be caught by
    the lockfile hash and by the roots file's own fail-closed reading, and it is
    recorded here rather than assumed away.
  * A vendor wrapper that is neither `CLAUDE.md` nor `VENDOR.md` (e.g.
    `GEMINI.md`) → **open**. `content_scan_roots.txt` names two wrapper filenames
    by hand as optional roots, so a third goes unscanned silently. Small, real,
    routed in *Lasting-truth migration* rather than fixed here.
* **Edge cases handled.** `modules: []` with a filled token (C1d). `preset:` +
  `modules:` together — a pre-existing hard error, untouched. A preset whose
  `modules_remove` names a token-gated module (C1g). Cairn itself, simultaneously
  source repo and adopter (Chunk D). A fresh adopter with no `python_package`
  (C1f). Duplicate roster entries — `expand_preset` returns a set-derived ordered
  list, and the existing no-duplicates assertion in
  `bootstrap/tests/test_profiles_smoke.py` still covers it.
* **Known omissions, stated rather than implied.** (a) No human has read
  `templates/modules/team-gated/content_scan.py` line by line for security
  content as part of this plan; that surface belongs to `content-scan-detectors`.
  (b) The alarm-fatigue measurement is taken on **Cairn's own tree** in Chunk D
  and on three synthetic scaffolds by the External reviewer — neither is a real
  third-party adopter tree, and the number could be worse there. (c) No test
  guards the *ordering* of `_DEFAULT_ON_MODULES` itself, only membership.
  (d) The `cascade_mutable` / `collection` staleness in `gate_manifest.json` is
  observed and reported, not repaired. (e) Whether the residual [E1] adopter
  population is large enough to justify a real selection signal (the reviewer's
  alternative to default-on) is settled by the Decision, not measured.

## Verification

Run under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`, Python
3.13.13) with `PYTHONDONTWRITEBYTECODE=1`; a different minor silently changes
both the suite figure and `ast.dump` structure, which the attestation depends on.

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

Plan-specific gates (a security-lint budget, a doc-drift gate, the
model-selection mapping check `python scripts/check_model_selection.py`)
are added per plan when the change touches that surface.
<!-- cairn:end verification-commands -->

**Plan-specific gates, added here because this change touches those surfaces.**

* **The install-contract assertion** — `python bootstrap/scaffold.py --manifest`,
  diffed against a capture taken at the plan-open commit into the session
  scratch directory. **Expected empty.** 96 lines / 95 data rows,
  `as_of 2026-08-04`.
* **The declared-delta assertion** — `python bootstrap/tests/_ast_attest.py
  verify bootstrap/tests/fixtures/scaffold_ast_baseline.json
  bootstrap/_scaffold/*.py`, run **before** Chunk A and again after, with this
  scope's contribution taken as the difference between the two reports. Expected
  contribution: 4 CHANGED (named), 2 NEW (named), 0 MISSING, 0 DUPLICATE.
* **The name-collision pre-check** — before committing Chunk A, both new
  top-level names are checked against the 161 baselined
  `FunctionDef:` / `Assign:` / `ClassDef:` keys. A `DUPLICATE` on one of this
  plan's names is a rename; every other `DUPLICATE` is a stop.
* **The release Bandit gate** — `python bootstrap/security_check.py` → `PASS`,
  74 targets before Chunk D and 76 after, with no MEDIUM+ appearing.
* **The lockfile assertion** — parse `dev/.cairn/cairn-lock.yml` and count:
  81 → 87 files, 14 → 15 modules; all `scripts/` + `tools/` `.py` records
  hash-clean (41 → 43).
* **The content-scan measurement** — `python scripts/content_scan_runner.py` on
  Cairn's tree after Chunk D; the flag count recorded as a number in the commit
  body.
* **The frozen-file note** — after the last implementation chunk, record in the
  commit body that four frozen entries are now stale and one file is
  `FROZEN-NEW`, naming all five. **Do not re-pin**: that is Chunk R.
* **The perturbation ledgers** — per chunk, in the commit body: the change made,
  the failure observed with its message, and the byte-identical restore verified
  with `git diff <path>` (empty).

## Plan review — the brief

**Declared tier: `required(**External**, security lens)`.** Carried verbatim
from the proposal header, where it is a *declared trigger* rather than a
judgement call.

**An Internal round does not discharge it.** The trigger is structural: this is
an install-contract change on a surface `AGENTS.md` names high-risk, and it
changes what every adopter receives by default. Internal review's job is to help
a change land; the question here is whether it *should* land in this shape, and
that needs the different-agent-type read. A fresh-session same-type read may run
first and is useful, but the plan is not review-discharged until an **External**
security-lens section is in the tree.

**No implementation commit lands before the `## Plan review` section is
committed** (`doctrine/plans.md` > plan-review precondition).

**What the reviewer should attack first, in order of how much rides on it:**

1. **C2's discriminating perturbation.** The claim is that deleting
   `scripts/content_scan.py` fails the named pin while leaving the generic
   byte-identity test green. If that is wrong — if the generic test already
   catches deletion — C2 is a restatement and the Decision's parity requirement
   is already satisfied without it. Reproduce this first.
2. **A4's placement.** The union of token-gated modules goes into the *baseline*,
   before `modules_add` / `modules_remove`. Everything the Decision's
   precedence rule promises rests on that one line's position. C1g is the pin;
   check that the pin actually discriminates the two placements.
3. **The exact-list boundary across all three shapes.** C1c / C1d / C1l claim to
   cover `modules: [x]`, `modules: []`, and `modules: [x] + token`. Ask whether a
   fourth shape exists that none of them reaches.
4. **The declared symbol delta.** Re-derive it. The measurement in *The cluster
   constraint* was taken by applying the intended edits to a scratch copy of the
   committed HEAD engine; a reviewer who reproduces it and gets a fifth CHANGED
   symbol has found the thing that would break the ceremony.
5. **Chunk D's ordering claim.** Whether landing D before the two `content_scan.py`
   scopes is merely inconvenient or actually unsafe. The plan argues loud-not-silent;
   test that.

## Code review

*Filled in after implementation commits land.* See `doctrine/plans.md` >
"Code review" for the full doctrine: falsification ledger, coverage line,
reviewer identity (not the implementing agent), and the append-only rule.

Begin with `**Model**: <model or tier when known>` immediately below the section
header (or below a `### Code review -- <reviewer> -- YYYY-MM-DD` sub-heading if
used). Do not copy a model label from a past template or archive; state the
actual running model identity.

## Lasting-truth migration

*Completed at archive time.* Pre-declared here so the archiving agent does not
have to reconstruct each home, and so the archive precondition
([Archive preconditions](../PLANNING.md#archive-preconditions-proposals-and-plans)
— a plan archives only after every deferred follow-up has a durable home outside
the plan) is satisfiable by checking a list rather than by re-reading the plan.

| # | Deferred follow-up | Durable home |
|---|---|---|
| 1 | **Cairn's `bootstrap/security_check.py` has no integrity preflight.** `run_security_audit.py` refuses to run when the apparatus or its policy inputs are not lockfile-clean; Cairn's own gate has no equivalent. Surfaced by the Decision, explicitly *not* a reason to adopt a module sideways. | `dev/PLANNING.md > Deferred follow-ups (durable home)` — one row, added at the archive / goodnight serialization point. |
| 2 | **`templates/modules/README.md`'s four pre-existing stale rows** — `incident-trackers` and `documentation-plan` missing from default-on; `model-selection`, `testing-discipline`, `doc-drift-prevention`, `examples-gallery` missing from team-gated. Independent of this change; three cluster scopes are adding further modules, so a one-off patch would be stale on arrival. | `dev/PLANNING.md > Deferred follow-ups`, phrased as a **re-derivation** task (generate the table from `_MODULE_MAPPINGS` + `_DEFAULT_ON_MODULES`), not a patch. |
| 3 | **The vendor-wrapper root gap.** `content_scan_roots.txt` names `CLAUDE.md` and `VENDOR.md` as optional roots by hand, so a third wrapper filename (`GEMINI.md`, …) goes unscanned silently — a vendor-neutrality defect in a security policy file. | `dev/PLANNING.md > Deferred follow-ups`. Candidate fix (derive the wrapper root from the installed lockfile rather than a hand list) recorded but not decided. |
| 4 | **Policy-file parity is deliberately unguarded**, and the accidental-narrowing residual that leaves open. | Recorded in the archive record of this plan **and** as a one-line note in Chunk D's commit body; no separate `dev/PLANNING.md` row, because the decision is settled rather than open. |
| 5 | **The `gate_manifest.json` staleness** (`cascade_mutable` note for `config.py`, `collection.node_count` 1598 vs 1746). | Chunk R's ceremony record — it is a Maintainer decision, not a deferred task. |
| 6 | **`templates/onboarding/high-rigor-legacy.md` lines 123 / 164.** | Already owned by `gate-claims-vs-enforcement`; **no migration needed**, recorded here so its absence from the list above is deliberate. |
| 7 | **The `CHANGELOG.md > Unreleased > Changed` line.** Pre-declared content: *the default install now carries the `content-security` scanner (opt out with one `modules_remove` line), and `python-security` is selected automatically when a `python_package` token is declared; an explicit `modules:` list stays exact and is never widened by either.* Cross-link the proposal and plan by stem. | The archive / goodnight serialization point, per `AGENTS.md > Shared communication files`. |

See also `doctrine/lifecycle.md` > "Loop-fidelity verification" for the
Decision→implementation fidelity sign-off checkpoint. That sign-off should
check, specifically, that no landed artifact restates the **withdrawn tautology
argument** and that `scripts/check_cairn.py` carries zero bytes of change.

This section is append-only once written.

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`).

**Standing.** I am the **same agent type as the plan's author**, in a fresh
session with no memory of the authoring context. That gives session
independence and nothing more — **no cross-type structural independence**. This
plan declares `required(**External**, security lens)`, and the plan's own *Plan
review — the brief* is right that an Internal round does not discharge it.
**This section does NOT discharge the declared tier.** It is a fresh-session
same-type read that runs first to make the External round cheaper; the plan
remains review-blocked until an **External** security-lens section is in the
tree. Everything below is measured against the working tree and committed HEAD
under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`, Python
3.13.13) with `PYTHONDONTWRITEBYTECODE=1`; every engine measurement was taken on
a **scratch copy** — no repository file was modified, added, moved or committed.

**Steelman.** This is the strongest-measured plan I have reviewed in this
cluster, and the measurement is real rather than decorative. I reproduced the
declared `bootstrap/_scaffold/` symbol delta independently — extracted the
committed HEAD engine to a scratch tree, applied A1–A6, ran the *real*
`_ast_attest.py verify` against the *real* baseline — and got **4 CHANGED, 2
NEW, 0 MISSING, 0 DUPLICATE**, with the four CHANGED keys and all four baseline
digests matching the plan's table character-for-character. The install-contract
assertion is likewise exact: 96 manifest lines, empty diff. The lockfile
accounting is exact down to the *identity* of the five customization-drifted
records. Most importantly, the plan's own #1 reviewer question — C2's
discriminating perturbation — is **correct**, and I confirmed it by running it:
`_self_hosted_twins()` is presence-derived, so deleting `scripts/content_scan.py`
silently shrinks the twin set from 43 to 42 and leaves
`test_every_self_hosted_twin_stays_byte_identical_to_its_source` **green**,
while a one-byte edit turns it red. C2 is a genuine test, not a restatement.
C1f's two-sided assertion is also exactly right for exactly the stated reason.
The plan's structural instincts — Chunk R as a Maintainer fence, oracles typed
by hand rather than derived from the table under test, C lands before D so the
green transition is evidence — are the right ones. My concerns are gaps in
*surface enumeration*, not in reasoning.

### Concerns

**[I1] — the `--summary` no-preset path is a fourth selection path the plan
never touches, and it under-reports a security module.** `cli.main` has **four**
module-selection sites, not three. Beyond the preset branch, the `modules:`-alone
branch and the install-path no-key branch that A6 names, there is a *separate*
no-key fallback inside the `--summary` handler
(`bootstrap/_scaffold/cli.py:236`–`239`: `else list(_DEFAULT_ON_MODULES)`), which
builds its roster inline and never calls `format_profile_summary`. A5 therefore
does not reach it and A6 does not touch it. Reproduced on the scratch engine with
a profile carrying `python_package: "mypkg"` and neither `preset:` nor `modules:`:

* `scaffold.py --summary` prints a **7-module roster** under *"Module roster (to
  install):"* — `python-security` absent — and closes with *"Does this profile
  look right before I install anything?"*.
* The **install of that same profile** writes both of `python-security`'s
  installed files into the target tree — the audit orchestrator under
  `scripts/`, and the module doctrine under the adopter's `dev/modules/`.

A5's own justification is that "a security module appearing in the roster with no
stated cause is exactly the silent-materialization failure the proposal was
opened over". This is the *inverse and worse*: a security module that
materializes on disk while the pre-install acceptance artifact says it will not.
C1j pins only the **preset** summary path (`format_profile_summary`), a different
function, so no pin in the plan reaches this shape. A6 must cover this branch
too, and C1j needs a second shape (no-preset + filled token → the summary names
the token-gated addition). Worth noting this is a **pre-existing latent
inconsistency** that Chunk A converts into a live one: today no module is
token-selected, so the two paths cannot disagree.

**[I2] — Chunk A turns two undeclared nodes RED; the plan asserts zero, and one
fix breaks a frozen-file claim.** Measured as a controlled delta on one scratch
tree (committed HEAD vs HEAD+A1–A6, same interpreter, same environment):

| Tree | Result |
|---|---|
| committed HEAD, unedited | 9 failed, 1700 passed, 1 skipped |
| HEAD + A1–A6 | 13 failed, 1696 passed, 1 skipped |

The 9 common failures are scratch-environment artifacts (`test_oracle.py`,
`test_gate_preflight.py`, `test_upgrade_module_additions.py` — present in both
runs, attributable to the absent `.git`), so the attributable delta is **four**
nodes: the two declared `test_ast_attest.py` nodes **plus**

* In [`bootstrap/tests/test_presets.py`](../../bootstrap/tests/test_presets.py),
  class `TestSoloLegacyRecipe`, test
  `test_literal_recipe_yaml_round_trips_under_the_stdlib_parser` — line 415 is
  `assert len(modules) == 8`; the run reports `AssertionError: assert 9 == 8`.
* In [`bootstrap/tests/test_quickstart_sequence.py`](../../bootstrap/tests/test_quickstart_sequence.py),
  class `TestLayerAStepsOneThroughThree`, test
  `test_step3_install_writes_expected_kernel_and_modules` — line 235 reports
  *"quickstart says '**6**' modules but the live solo-greenfield install
  resolves 7 ... refresh the quickstart prose"*.

This falsifies three stated claims: Chunk A's acceptance that `test_presets.py`
runs **green**; *"The suite is red on exactly two nodes and no others from this
commit until Chunk R ... Any third failure is this plan's to explain"*; and —
most consequentially — **C4's "Docstring-only ... no assertion changes, so no
behaviour rides on a frozen-file edit."** `test_presets.py` is a **frozen file**
(confirmed present in the 164-entry `frozen_files` map), and repairing this node
requires an **assertion** change, not a docstring. C4's frozen-file justification
does not survive, and the *Gate accounting* line "Frozen files modified: four"
now understates what those four edits are.

**[I3] — Chunk B's documentation surface is short by two files, and the one that
matters has no prose guard.** Neither `docs/quickstart.md` nor
`docs/solo-legacy-recipe.md` appears in *Documentation / doctrine surface*, in
*Out of scope*, or in *Serialized shared files* — yet both enumerate the
default-on roster and both are falsified by Chunk A. The asymmetry between them
is the real hazard:

* `docs/quickstart.md:129` carries an inline `<!-- verify:
  solo_greenfield_module_count -->` marker and `test_quickstart_sequence.py`
  **extracts the number and compares it to the live install**. Prose drift is
  caught mechanically. Fix = one prose edit.
* `docs/solo-legacy-recipe.md:58`–`62` says *"an **8-module roster** — the six
  default-on modules (`lifecycle-metrics`, `reflections`, `claim-check`,
  `fold-back-ledger`, `incident-trackers`, `documentation-plan`) plus
  `legacy-agent` and `testing-discipline`"*. **No test extracts that prose** —
  `grep` over `bootstrap/tests/` for the roster wording returns nothing;
  `test_presets.py:415` hardcodes the literal `8`. So the mechanical repair of
  [I2] — bump `8` to `9` — **turns the suite green while leaving the recipe
  permanently wrong** (still claiming an 8-module roster and six default-on
  modules). "The test went green" would be evidence that a literal was edited,
  not evidence that the document was. That is precisely the vacuity shape Chunk
  C's own preamble is built to reject, arriving through a door the plan left
  open. Both prose sites must be named in Chunk B, and the recipe fix must be
  stated as a *doc* obligation that the test bump does not discharge.

**[I4] — B3's stated premise is false for one of three files, and its guard
claim is false for all three.** The plan justifies re-derivation with *"All three
are **already wrong** (they omit `incident-trackers` and `documentation-plan`)"*.
Checked: `bootstrap/profiles/solo-greenfield.yml:17`–`18` **already lists all six
correctly**. Only `bootstrap/profiles/collaborative-team.yml:16`–`17` and
`bootstrap/profiles/high-rigor-legacy.yml:16`–`17` omit them (each lists four).
Separately, Chunk B's acceptance says *"the three rosters are pinned by test in
Chunk C"* — they are **not**. No C1 pin reads a `bootstrap/profiles/*.yml`
comment block, and `grep "Resulting module roster" bootstrap/tests/ scripts/`
returns nothing. C1a pins the *expansion*, which is a different object from the
*comment describing it*. The only stated oracle for B3 is "compared against the
comment block **by eye** at implementation" — which is exactly how two of the
three drifted in the first place. Re-derivation is still the right call; the
premise and the guard claim both need correcting, and the residual (these blocks
stay unguarded and will drift again) should be named rather than implied away.

**[I5] — the NEW-key acceptance criterion is literally false and misattributes
the excess.** Chunk A's acceptance says `verify` *"reports 4 CHANGED ... and **2
NEW non-`Import:` / non-`Docstring` keys** with the two declared names"*, with a
parenthetical that *"the sibling's in-flight symbols will also appear"*. Measured:
on the **committed HEAD** engine — no sibling work, no edits, `verify` returning
**rc 0** — the tool already emits **29** NEW non-`Import:` / non-`Docstring`
keys (`Assign:_MODULE_REQUIRED_TOKENS`, `FunctionDef:missing_required_tokens`,
`ClassDef:EngineFinder`, …). The edited tree emits **31**. So the excess is *not*
the sibling's; it is a standing set of post-baseline engine additions. The
plan's diff-against-pre-chunk method is correct and rescues the operation — the
set-difference is exactly the two declared names, which I confirmed — but an
implementer reading the literal criterion will see 31 where 2 was promised and be
told the wrong cause. State the criterion as a **set difference** and drop the
sibling attribution.

*Nits, non-blocking.* `scripts/check_cairn.py:100` lands on the comment
introducing `_LINK_CHECK_SRC`; the assignment is at `:101` (`:84` and `:91` are
exact). The *Gate accounting* figure *"180 Markdown file(s)"* now reads **181** —
the plan's own file makes it stale on arrival, which the plan half-anticipates
("plus whatever `dev/` artifacts this lifecycle itself contributes"); prefer the
`as_of` + growth-direction form over a bare count.

### Covered

Verified true by measurement, not by reading:

1. **The declared symbol delta — reproduced exactly.** Applying A1–A6 to a
   scratch copy of the committed HEAD engine and running the real
   `bootstrap/tests/_ast_attest.py verify` against the real
   `bootstrap/tests/fixtures/scaffold_ast_baseline.json` yields **4 CHANGED, 2
   NEW, 0 MISSING, 0 DUPLICATE**. The four CHANGED keys are exactly
   `Assign:_DEFAULT_ON_MODULES`, `FunctionDef:expand_preset`,
   `FunctionDef:format_profile_summary` (`config.py`) and `FunctionDef:main`
   (`cli.py`), and all four baseline digests match the plan's table exactly
   (`2c8ef688f6865487`, `6bd2e6caa83f4017`, `830aac8b7c3d1bde`,
   `ff5a7441cceda605`). The set-difference of NEW keys against the pre-edit run
   is exactly `Assign:_TOKEN_GATED_MODULES` and `FunctionDef:token_gated_modules`.
   **No fifth CHANGED symbol exists.** This is the check the brief called
   highest-value, and the plan survives it.
2. **Baseline composition — exact.** 174 entries; 161 of the three kinds
   (98 `FunctionDef:` / 53 `Assign:` / 10 `ClassDef:`); 13 exempt (8 `Import:`,
   1 `Docstring`, 1 `Expr`, 2 `If`, 1 `Try`).
3. **Committed HEAD is clean** — `verify` returns **rc 0**, "174 baselined
   symbol(s) accounted for, unchanged". The working-tree red is entirely the
   in-flight sibling's, as the plan says.
4. **The `DUPLICATE` pre-check** — both new top-level names are free against all
   161 baselined three-kind names.
5. **`_UPDATE_ALLOWLIST`** admits exactly four symbols (`_MODULE_MAPPINGS`,
   `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`, `install_onboarding`); none of the four
   CHANGED is among them. The self-service repair path is genuinely unavailable.
6. **The install contract does not move.** `scaffold.py --manifest` emits **96**
   lines (header + 95 rows), and the diff between committed HEAD and the edited
   engine is **empty**. All six `content-security` specs and both
   `python-security` specs are already registered — **zero manifest rows added**.
7. **C2's discriminating perturbation — the plan's #1 question, confirmed by
   running it.** With both twins installed the set is **43**. Deleting
   `scripts/content_scan.py` drops it to **42** and
   `test_every_self_hosted_twin_stays_byte_identical_to_its_source` **passes**
   (as does `test_every_self_hosted_twin_carries_spdx_header`, whose non-empty
   assertion only catches deleting *all* twins). Appending one byte makes the
   generic test **fail** at `bootstrap/tests/test_notice_install.py:109`. C2 is
   necessary, and deletion is the right perturbation.
8. **A4's placement / C1g — the pin discriminates.** Moving the union from the
   baseline to after the overrides makes `preset: solo-greenfield` +
   `python_package: mypkg` + `modules_remove: [python-security]` install
   `scripts/run_security_audit.py`. C1g goes red on exactly the placement error.
9. **C1f's two-sided assertion — exactly right, for the stated reason.** Making
   the gate unconditional yields **rc 2**, `refusing to install (no files
   written)`, with `run_security_audit.py` still **absent**. An absence-only
   assertion stays green; the `rc == 0` assertion is what catches it.
10. **All selection shapes behave as claimed**, each run through the real CLI
    into a scratch target: exact lists never widened (C1c/C1d/C1l — no
    `content_scan.py`, no `run_security_audit.py`, rc 0, including with a filled
    token); C1e selects on a filled token; C1f absent without one; C1h opts out
    loudly (`[info] default-on opted out via modules_remove: content-security.`);
    C1i correct on **both** unfilled shapes (`{{python_package}}` and `"   "`).
11. **Lockfile figures — exact**, including identities: **81** files, **14**
    modules, **41** `scripts/`+`tools/` `.py` records **all hash-clean**, and
    exactly **five** drifted records — exactly the five named.
12. **`scan_targets()` returns 74.** Exact.
13. **Gate-manifest figures — exact.** `frozen_files` has **164** entries;
    all four named test files are present; `config.py`/`cli.py` are absent from
    it; `cascade_mutable` carries `bootstrap/_scaffold/config.py`; and
    `collection.node_count` is **1598**, stale as the plan reports.
14. **Every other cited line number resolves** to what the plan says it does:
    `bootstrap/BOOTSTRAP.md:108`/`215`/`703`, `bootstrap/tests/test_presets.py:91`,
    `bootstrap/tests/test_profiles_smoke.py:112` and `:227`,
    `bootstrap/SAFETY.md:155`, `bootstrap/DEPENDENCY_BUDGET.md:30`,
    `scripts/check_cairn.py:84` and `:91`.
15. **B1 and B2's quoted sentences are verbatim-correct** in the tree, and C3's
    premise holds: `test_python_security_not_in_any_default_or_preset`
    (`bootstrap/tests/test_security_stack.py:733`) asserts against
    `_DEFAULT_ON_MODULES` and each preset's `modules_add`, both of which stay
    true under token-gating. The rename-plus-docstring reading is correct.
16. **C1k's printed string exists**, and citing it by string rather than line
    number is the right call — that file is under concurrent edit.
17. **The three REQUIRED content-scan roots are exactly `!AGENTS.md`,
    `!.agents/skills`, `!dev`**, all present in Cairn. The vendor-wrapper gap
    (migration row 3) is real: the optional roots name `CLAUDE.md` and
    `VENDOR.md` by hand, with no third-wrapper path.
18. **Checked because the plan did not, and it comes out in the plan's favour:**
    a token-gated module **cannot** silently materialize on an existing adopter's
    upgrade. `structural["new_modules"]` is `sorted(current_modules -
    lock_modules)` with `current_modules = set(_MODULE_MAPPINGS)` — a
    registry-versus-lockfile comparison, independent of both
    `_DEFAULT_ON_MODULES` and the profile expansion. So an adopter carrying a
    `python_package` token gets `python-security` listed under `new modules
    available (opt-in)`, never installed. This closes a hazard the plan does not
    name; C1k's preserved-property framing is correct, though its perturbation
    validates `cmd_upgrade`'s printing rather than anything this change alters.

Both required checkers were run and pass on the pre-review file:
`claim_check.py` → `OK, no claim-check flags` (20 paths exempted by the
`claim-check-allow` directive); `check_cairn.py` → `OK -- 1 Markdown file(s)
scanned; no issues`.

### Not covered / low confidence

* **Chunk D was not executed.** I did not run `upgrade --adopt-module
  content-security --target .` — it writes to the repository. The 81→87 /
  14→15 arithmetic is consistent with six registered specs plus one module, and
  I confirmed 41→43 twins by simulating the two `.py` copies, but the actual
  adopt run, the substitution/`base_cache`/`base_hash` behaviour for
  `dev/modules/content-security.md`, the `security_check.py` 74→76 transition,
  and the post-D Bandit severity histogram are all **unverified**.
* **D3's alarm-fatigue measurement is unmeasured** — the runner is not installed,
  so I could not take it. That number is the one figure the entire restated
  argument rests on, and it is deferred to implementation. An External reviewer
  cannot close it either; only Chunk D can.
* **The `1744 passed / 2 failed` baseline is not reproducible from the record.**
  It was measured on a working tree containing another scope's **uncommitted**
  test files (`bootstrap/tests/test_fork_advisory.py`,
  `bootstrap/tests/test_profile_grammar.py`); committed HEAD collects **1710**
  nodes in my scratch tree. The passed count, not just the 2 failures, is
  contaminated by in-flight sibling work. Relatedly, the plan's post-R target of
  "0 skipped" is unverified — committed HEAD carries one environment-conditional
  skip (`bootstrap/tests/test_foldback_suggest.py:297`, "live ledger not
  available in this checkout") that may or may not fire in the real tree.
* **My A1–A6 reconstruction is mine, not the author's.** The symbol delta is
  robust to body details (all four CHANGED keys change under any faithful
  implementation, and the two NEW names are specified), but a materially
  different implementation — e.g. one that adds a helper, or edits
  `_canonical_order` — would change the delta. The declared-delta assertion must
  still be re-run against the *actual* Chunk A before commit.
* **Not assessed:** whether B1/B2's rewritten wording clears `quality_gate.py
  --sub neutrality`; the security content of
  `templates/modules/team-gated/content_scan.py` itself (correctly fenced to
  `content-scan-detectors`); and whether a *fifth* selection shape exists beyond
  the four I enumerated — I found the fourth by reading `cli.main` end to end,
  but I did not prove the enumeration complete.
* **Same-type blind spot.** [I1]–[I4] are all *surface-enumeration* misses, and
  I found them by running things rather than by reading — which is some evidence
  that a same-type reader shares the author's framing and will miss what the
  author missed by reading alone. The External round should assume there are
  more enumeration gaps and should re-derive rather than re-read.

### Second-round recommendation

**REVISE, then proceed to the required External security-lens round — and the
revision should land before that round, not after.** [I1] is a substantive scope
gap that changes the content of both Chunk A and Chunk C, and [I2]/[I3] change
what Chunk B touches and what C4 may claim about a frozen file; an External
reviewer should be reading the corrected shape rather than re-deriving these.
None of the five is a reason to reject the plan's approach: the engine design,
the precedence rule, C2, C1f and C1g all survive direct falsification attempts,
and the plan's core measured claims — the symbol delta, the install contract,
the lockfile accounting — reproduce exactly.

Specifically, the revision should: extend A6 and C1j to the `--summary`
no-preset branch [I1]; declare the two additional red nodes and correct Chunk A's
green claim, the "exactly two nodes" claim, and C4's docstring-only /
no-assertion-changes claim [I2]; add `docs/quickstart.md` and
`docs/solo-legacy-recipe.md` to Chunk B, with the recipe's prose fix stated as an
obligation the `8`→`9` test bump does **not** discharge [I3]; correct B3's
premise and drop or requalify the "pinned by test in Chunk C" claim [I4]; and
restate the NEW-key criterion as a set difference without the sibling
attribution [I5].

**This Internal round does not discharge the declared
`required(**External**, security lens)` tier.** No implementation commit should
land until an External security-lens section is in the tree.

## Response to plan review -- Claude (author) -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`).

**Standing and scope.** I am the plan's author, responding to the Internal
(same-agent-type, security-lens) plan review committed at `ab66d19`. This
Response **dispositions findings and amends the plan**; it discharges **no**
review tier. The declared tier is `required(**External**, security lens)` and
**no External security-lens section is in the tree**. The plan remains
review-blocked and **no implementation commit may land**. See *Clearance* below.

**Method, and why every figure moved.** The review was written at `ab66d19`.
Working-tree HEAD is now **`6618e54`**, and **two commits landed in between that
invalidate the plan's own measurement frame**:

* **`3852cf7` — "Ceremony 1 -- batched AST baseline re-anchor for Wave 2
  (Maintainer-run)"**, which is **not** an ancestor of `ab66d19`
  (`git merge-base --is-ancestor 3852cf7 ab66d19` → false). It re-anchored
  `bootstrap/tests/fixtures/scaffold_ast_baseline.json` and absorbed the
  in-flight sibling's three CHANGED symbols.
* **`84fbef4` — `gate-claims-vs-enforcement` Chunk E**, which edited
  `bootstrap/SAFETY.md` and moved a line this plan cites.

So I re-derived rather than inherited. Every engine measurement below was taken
on a **`git clone` of the repository into the session scratch directory** — a
clone, not a bare source extract, so `.git` is present and the git-dependent
gates actually run. **No repository file was modified, added, moved, staged or
committed**; the only path this Response writes is
`dev/plans/default-security-stance.md`. Interpreter throughout:
`~/conda_envs/lhm/bin/python3.13` (CPython 3.13.13) with
`PYTHONDONTWRITEBYTECODE=1`. `as_of 2026-08-04`, at `6618e54` unless stated.

### The headline: the plan's measurement frame is stale, and one review finding was itself mis-measured

1. **The suite is green.** `python -m pytest bootstrap/tests` on the live tree
   returns **1790 passed, 0 failed, 0 skipped**, 186.73s. The plan's
   *"1744 passed, 2 failed"* and the whole *"The window is already open, measured
   rather than predicted"* premise describe a state that no longer exists:
   Ceremony 1 re-anchored the baseline and the two `test_ast_attest.py` nodes are
   green. **This is not a cosmetic drift** — Chunk A's central acceptance
   criterion ("red on exactly two nodes") was written against a red baseline and
   is now measuring against a green one.
2. **The AST baseline shrank, and the four declared digests survived.** The
   baseline now holds **173** entries, not 174. The three-kind count is
   **unchanged at 161 (98 `FunctionDef:` / 53 `Assign:` / 10 `ClassDef:`)**; the
   12 remaining are 8 `Import:`, 1 `Docstring`, 1 `Expr`, and 2 `If`-prefixed
   (`If:` and `If#2:`). **There is no `Try:` key** — the review's *"13 exempt (8 `Import:`,
   1 `Docstring`, 1 `Expr`, 2 `If`, 1 `Try`)"* is wrong on both the total and
   the `Try`. Against that new baseline, **all four declared CHANGED digests
   still match character-for-character** (`2c8ef688f6865487`, `6bd2e6caa83f4017`,
   `830aac8b7c3d1bde`, `ff5a7441cceda605`), and `verify` on the unedited tree
   returns **rc 0, "173 baselined symbol(s) accounted for, unchanged"**. The
   plan's symbol table survives the ceremony; only its *sizing* prose does not.
3. **[I2]'s red-node enumeration is short by three, and the review
   mis-attributed them.** Controlled delta, same clone, same interpreter:

   | Tree | Result |
   |---|---|
   | committed `6618e54`, unedited clone | **1 failed, 1788 passed, 1 skipped** |
   | `6618e54` + A1–A6 (uncommitted) | **8 failed, 1781 passed, 1 skipped** |

   The one common failure is a clone artifact
   (`test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports`,
   which runs against the live repo). The attributable delta is **seven** nodes,
   not two and not four: the two `test_ast_attest.py` nodes, the two [I2] nodes,
   **and three `test_oracle.py` nodes** —
   `test_oracle_matrix_behavior_preserved`, `test_oracle_privileged_workflows_preserved`,
   `test_oracle_measures_target_not_verifier`. The review dismissed
   `test_oracle.py` as an *"absent `.git`"* artifact *"present in both runs"*.
   With `.git` present it is **green on the base tree and red on the edited
   one**: the differential oracle materializes the baseline engine at
   `baseline_ref="HEAD"` and diffs its scaffold output against the current
   engine, so an uncommitted A1 makes every scenario report
   `only_in_current: scripts/content_scan_*` diffs. **Committing A1–A6 in the
   scratch clone clears all three** (`test_oracle.py` → 18 passed). They are
   working-tree-only transients and do not violate Chunk A's *"from this
   commit"* scoping — but an implementer who runs the suite before committing
   sees **seven** reds where the plan promises two, and must be told which three
   clear on the commit itself. This is exactly the hazard the review warned about
   in its own *Same-type blind spot* note, landing on the review.

### Disposition of every finding

| # | Disposition | Reasoning | Mechanical residue |
|---|---|---|---|
| **[I1]** — the `--summary` no-preset path | **ACCEPT** | Reproduced end-to-end on the edited clone, and it is worse than the review states because I ran the install too. `bootstrap/_scaffold/cli.py:236`–`239` (`else list(_DEFAULT_ON_MODULES)`) is verbatim as cited. With `project_name` + `python_package: mypkg` and neither `preset:` nor `modules:`, `scaffold.py --summary` prints a **7-module roster with `python-security` absent** and asks *"Does this profile look right before I install anything?"*; the install of that same profile writes **`scripts/run_security_audit.py`, and the module's doctrine file under the target's `dev/modules/`**. A5's own stated justification is inverted: the pre-install acceptance artifact promises a security module will not be installed, and it is. | New **A7**; **C1j** gains a second shape; new pin **C1m** (summary/install agreement) |
| **[I2]** — two undeclared RED nodes | **ACCEPT WITH MODIFICATION** | The substance reproduces exactly, message text included: `bootstrap/tests/test_presets.py:415` is `assert len(modules) == 8` and reports `AssertionError: assert 9 == 8`; `bootstrap/tests/test_quickstart_sequence.py:235` reports *"docs/quickstart.md says '**6** modules' but the live solo-greenfield install resolves 7 ... refresh the quickstart prose."* `test_presets.py` **is** a frozen file (confirmed in the 164-entry `frozen_files` map at `6618e54`), so C4's *"no assertion changes"* justification does not survive. **Modified because the enumeration is short by three** — see the headline table. | Chunk A acceptance bullets 1 and 4 rewritten; **C4** rewritten; *Gate accounting* frozen-files line rewritten |
| **[I3]** — Chunk B is short by two doc files | **ACCEPT WITH MODIFICATION** | Both sites reproduce: `docs/quickstart.md:129` carries `**6** modules listed <!-- verify: solo_greenfield_module_count -->`, and `docs/solo-legacy-recipe.md:58`–`62` claims an *"**8-module roster** — the six default-on modules"*. No test extracts the recipe prose. **Modified on two points.** (a) The review says the quickstart fix is *"one prose edit"*; it is **two** — `:129`'s guarded number **and** `:130`–`:131`'s **unguarded** six-name enumeration, which no test reads. The quickstart carries the same guarded/unguarded split as the recipe. (b) I measured the enumeration surface for completeness rather than leaving it open: `grep -rl` for `fold-back-ledger` across `docs/`, `bootstrap/`, `templates/` returns **exactly** `docs/solo-legacy-recipe.md`, `docs/quickstart.md`, `bootstrap/BOOTSTRAP.md` (×3 sites), the three `bootstrap/profiles/*.yml`, and `templates/modules/README.md`. With B6/B7 added the prose surface is **complete**, and I assert that as a measurement. | New **B6**, new **B7**; *Documentation / doctrine surface* amended |
| **[I4]** — B3's premise and guard claim | **ACCEPT** | Both halves reproduce. `bootstrap/profiles/solo-greenfield.yml:17`–`18` **already lists all six** default-on modules correctly; only `collaborative-team.yml:16`–`17` and `high-rigor-legacy.yml:16`–`17` omit `incident-trackers` and `documentation-plan` (each lists four). And `grep "Resulting module roster" bootstrap/tests/ scripts/` returns **nothing** at `6618e54` — no C1 pin reads a profile comment block, so *"pinned by test in Chunk C"* is false. Re-derivation remains right; the justification was wrong. | **B3** row rewritten; Chunk B acceptance bullet 4 rewritten with the residual named |
| **[I5]** — the NEW-key criterion | **ACCEPT WITH MODIFICATION** | The finding's substance is right and its **figures do not reproduce**. On the unedited committed engine at `6618e54`, `verify` emits **45** NEW non-`Import:` / non-`Docstring` keys (the review said 29); the edited tree emits **47** (the review said 31). The set difference is **exactly** `Assign:_TOKEN_GATED_MODULES` and `FunctionDef:token_gated_modules`, so the plan's diff-against-pre-chunk method rescues the operation, as the review says. The right correction is therefore **not** to substitute 45 for 29 — that number will drift again on the next engine change. The criterion must be stated as a **set difference with no count at all**, and the sibling attribution dropped: the excess is a standing set of post-baseline engine additions, because the baseline is a partial pin rather than a complete inventory. | Chunk A acceptance bullet 3 rewritten as a set difference |
| *Nit* — `scripts/check_cairn.py:100` vs `:101` | **DECLINE** | Does not reproduce, and did not reproduce when written. At `6618e54`, `scripts/check_cairn.py:100` **is** `_LINK_CHECK_SRC = (`; the comment is `:96`–`:99`. At the review's own commit `ab66d19` the same line was already the assignment (`git show ab66d19:scripts/check_cairn.py`), and the file has not changed since. The plan's `:84` / `:91` / `:100` citations are all exact. | None — the plan is correct as written |
| *Nit* — `180 Markdown file(s)` | **ACCEPT WITH MODIFICATION** | Neither figure holds. `python scripts/check_cairn.py` at `6618e54` → `OK -- 195 Markdown file(s) scanned; no issues; 68 external link(s) not probed`. The review's 181 was already stale when written. The nit's *prescription* — prefer `as_of` + growth-direction over a bare count — is right and is what I adopt; substituting 195 would repeat the error in three weeks. | *Gate accounting* prose-integrity bullet rewritten |

### Findings I am adding on my own re-measurement

* **[R1] The three `test_oracle.py` transients.** Above. Amends Chunk A's
  acceptance and adds a workflow note, because an implementer confronted with
  seven reds and a plan promising two will reasonably stop.
* **[R2] `bootstrap/SAFETY.md:155` no longer resolves.** The plan cites it for
  *"already names the `content-security` / `python-security` apparatus as Layer-4
  code"*, and the review's *Covered #14* endorsed the citation. At `6618e54`
  that text is at **`:173`**; `:155` is now `` `upgrade`, `cli` — plus the
  verifying loader `_guard.py`; *every module ``. `gate-claims-vs-enforcement`
  Chunk E (`84fbef4`) moved it **after** the review was written. The underlying
  claim — that the file already covers this apparatus and stays true — still
  holds; only the line number is wrong.
* **[R3] B5's "four pre-existing omissions" is arithmetically wrong.** Derived
  from `_MODULE_MAPPINGS` + `_DEFAULT_ON_MODULES` against the table's 12 rows:
  `templates/modules/README.md` omits **two** default-on (`incident-trackers`,
  `documentation-plan`) and **six** team-gated (`content-security`,
  `doc-drift-prevention`, `examples-gallery`, `model-selection`,
  `python-security`, `testing-discipline`). B5 adds two of the six, leaving
  **six** residual rows (2 + 4) — which is what *Lasting-truth migration* row 2
  actually lists. *Scope*'s "six team-gated modules" is right; B5's "four" is
  not.
* **[R4] Chunk R item 3's `known_new` requirement may target the wrong
  mechanism.** `known_new` is read **only** by `update_symbol`
  (`bootstrap/tests/_ast_attest.py:230`, its keyword parameter; `verify` never
  reads it — `A.verify(baseline, modules)` takes two arguments). This plan
  establishes on two independent grounds that `update-symbol` is unavailable to
  this scope. So either the ceremony does not need `known_new` pins for these two
  keys, or the ceremony mechanism is not the one Chunk R names. **Routed to the
  Maintainer, not decided here** — Chunk R is a Maintainer fence and this is a
  ceremony-design question.
* **[R5] "0 skipped" is now measured-reachable.** The review flagged the plan's
  post-R *"0 failed / 0 skipped"* target as unverified, citing an
  environment-conditional skip. On the **live tree** the suite reports **0
  skipped** at `6618e54`. (One skip fires in the scratch clone; that is a clone
  artifact, like the `test_gate_preflight` failure.) This closes a review
  *Not covered* item in the plan's favour.

### Review claims I re-ran and confirmed exactly

Reported as plainly as the non-reproductions. Each was **run**, not read:

1. **The declared symbol delta, against the *new* baseline.** Applying A1–A6 to
   the clone and running the real `bootstrap/tests/_ast_attest.py verify` against
   the real re-anchored baseline: **4 CHANGED — exactly the four in the plan's
   table, with the four declared digests — 0 MISSING, 0 DUPLICATE**, and a NEW
   set difference of exactly the two declared names. **No fifth CHANGED symbol.**
2. **C2's discriminating perturbation — the brief's #1 question.** Twins: **41**
   before, **43** after copying both `.py` files into `scripts/`. Deleting
   `scripts/content_scan.py` → **42** twins and `test_notice_install.py` stays
   **fully green (10 passed)**. Appending one byte → **`FAILED ... ::test_every_self_hosted_twin_stays_byte_identical_to_its_source`**
   at `bootstrap/tests/test_notice_install.py:109`. C2 is necessary; deletion is
   the right perturbation. Restore verified byte-identical.
3. **The install contract does not move.** `scaffold.py --manifest` → **96**
   lines. `content-security` carries **6** `InstallSpec`s and `python-security`
   **2**, both already registered — **zero manifest rows added**.
4. **A4's placement / C1g.** `preset: solo-greenfield` + `python_package: mypkg`
   + `modules_remove: [python-security]` → `python-security` **absent** and
   `summary["token_gated"]` **empty**, with the union in the baseline.
5. **The `DUPLICATE` pre-check.** Neither `_TOKEN_GATED_MODULES` nor
   `token_gated_modules` collides with any of the 161 baselined three-kind names.
6. **`_UPDATE_ALLOWLIST`** admits exactly `_CORE_MAPPINGS`, `_MODULE_MAPPINGS`,
   `_SKILLS_MAPPINGS`, `install_onboarding`; none of the four CHANGED is among
   them.
7. **Lockfile accounting — exact, including identities.** **81** files, **14**
   modules, **41** `scripts/`+`tools/` `.py` records **all hash-clean**, and
   exactly **five** drifted records: `AGENTS.md`, `dev/NEXT_SESSION.md`,
   `dev/PLANNING.md`, `dev/collaboration_agreement.md`,
   `dev/modules/security-review.md`.
8. **`scan_targets()` returns 74.** Exact.
9. **Gate-manifest figures.** `frozen_files` **164** entries; all four named test
   files present; `config.py` / `cli.py` absent; `cascade_mutable` carries
   `bootstrap/_scaffold/config.py`; `collection.node_count` **1598**.
10. **`_self_hosted_twins()` is presence-derived** — it `rglob`s `scripts/` and
    `tools/` and intersects with the manifest, so a deleted twin silently leaves
    the set.
11. **`structural["new_modules"]` is registry-versus-lockfile** —
    `sorted(set(_MODULE_MAPPINGS) - lock_modules)` at
    `bootstrap/_scaffold/upgrade.py:628`, independent of `_DEFAULT_ON_MODULES`
    and of the expansion. The printed string `new modules available (opt-in)` is
    at `:679`–`:680`. Review *Covered #18* holds.
12. **The three REQUIRED content-scan roots** are exactly `!AGENTS.md`,
    `!.agents/skills`, `!dev`; all present in Cairn.
13. **B1 / B2's quoted sentences are verbatim-correct** in the tree
    (`templates/modules/team-gated/content-security.md:3`,
    `templates/modules/team-gated/python-security.md:6`–`7`), and C3's premise
    holds at `bootstrap/tests/test_security_stack.py:733`.
14. **Remaining line citations resolve**: `bootstrap/BOOTSTRAP.md:108` / `:215` /
    `:703` (and these are the **only** three roster enumerations in that file),
    `bootstrap/tests/test_presets.py:91`,
    `bootstrap/tests/test_profiles_smoke.py:112` and `:227`,
    `bootstrap/DEPENDENCY_BUDGET.md:30`, `scripts/check_cairn.py:84` and `:91`.

### Amendments in force

Every row supersedes the quoted text **verbatim**. Where an amendment adds a
chunk row or a pin, the added text is given in full so no reconstruction is
needed at implementation. **One rendering caveat, stated so the quotes stay
checkable:** when a superseded span is itself a chunk-table row, its cell
separators appear here as `\|` so this table renders; the *words* are verbatim
and every quote below was verified by substring match against the plan file
before commit.

| # | Superseded text (verbatim) | Replaced by |
|---|---|---|
| **1** | *"`python -m pytest bootstrap/tests` → **1744 passed, 2 failed**, 165s. The two failures are `test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package` and `::test_ast_gate_passes_over_the_full_scaffold_module_set`, reporting 3 CHANGED symbols — `FunctionDef:cmd_upgrade` (`bootstrap/_scaffold/upgrade.py`), `FunctionDef:forked_facade_findings` and `FunctionDef:format_forked_facade_warning` (`bootstrap/_scaffold/lockfile.py`) — from a sibling's uncommitted work."* | **The window has closed.** At `6618e54`, `python -m pytest bootstrap/tests` → **1790 passed, 0 failed, 0 skipped**, 186.73s, `as_of 2026-08-04`. The sibling's three CHANGED symbols were absorbed by the Maintainer-run **Ceremony 1** re-anchor (`3852cf7`), which landed **after** the plan review. The whole *"The window is already open, measured rather than predicted"* framing is retired: the cluster hazard it describes is real and unchanged, but the specific red state it cites no longer exists. |
| **2** | *"Against the **committed** HEAD engine sources (extracted to a scratch tree, no repository file touched) the same verify returns **rc 0: 174 baselined symbols accounted for, unchanged**. So the baseline is clean at HEAD and the red is entirely the in-flight sibling's."* | At `6618e54` the **live working tree** returns **rc 0: 173 baselined symbol(s) accounted for, unchanged** — no scratch extraction needed, because there is no in-flight engine red to subtract. |
| **3** | *"`bootstrap/tests/fixtures/scaffold_ast_baseline.json` holds **174** entries, **161** of them `FunctionDef:` / `Assign:` / `ClassDef:` (98 / 53 / 10); the remaining 13 are `Import:` / `Docstring` / `Expr` / `If` / `Try` keys that `_classify()` exempts as per-module necessities. `as_of 2026-08-04`."* | Post-Ceremony-1 (`3852cf7`) the baseline holds **173** entries, **161** of them `FunctionDef:` / `Assign:` / `ClassDef:` (**98 / 53 / 10 — unchanged**); the remaining **12** are 8 `Import:`, 1 `Docstring`, 1 `Expr` and 2 `If`-prefixed (`If:`, `If#2:`) keys that `_classify()` exempts. **There is no `Try:` key.** `as_of 2026-08-04` at `6618e54`. The 161 figure is the one the plan's name-collision pre-check depends on, and it did **not** move. |
| **4** | *"Derived by applying this plan's intended edits to a **scratch copy of the committed HEAD engine sources** and running the real `bootstrap/tests/_ast_attest.py verify` against the real committed baseline. No repository file was modified. `as_of 2026-08-04`."* | Re-derived at `6618e54` against the **re-anchored** baseline, on a `git clone` in the session scratch directory; no repository file modified. **The table below stands unchanged: all four CHANGED keys and all four baseline digests still match exactly.** `as_of 2026-08-04`. |
| **5** | *"* **Suite baseline: 1744 passed / 2 failed** (both the AST nodes, from the in-flight sibling), 165s, `as_of 2026-08-04`. Collection may only grow by this plan's new nodes; a dropped node or a new skip/xfail marker is a HOLD class."* | **Suite baseline: 1790 passed / 0 failed / 0 skipped**, 186.73s, `as_of 2026-08-04` at `6618e54`. Collection may only grow by this plan's new nodes; a dropped node or a new skip/xfail marker is a HOLD class. **Re-take this figure at implementation** — it moved by 46 nodes in the day between plan-open and this Response. |
| **6** | *"* **Frozen files modified: four**, all in `bootstrap/tests/`, all literal keys in the 164-entry `frozen_files` map (`as_of 2026-08-04`) — `test_notice_install.py` (C2), `test_security_stack.py` (C3), `test_presets.py` and `test_profiles_smoke.py` (C4, docstring-only)."* | **Frozen files modified: four**, all in `bootstrap/tests/`, all literal keys in the 164-entry `frozen_files` map (`as_of 2026-08-04`) — `test_notice_install.py` (C2), `test_security_stack.py` (C3), `test_profiles_smoke.py` (C4, **docstring-only**), and `test_presets.py` (C4, **docstring plus one assertion**: `:415`'s `assert len(modules) == 8` → `== 9`). **One of the four now carries a behaviour-bearing edit to a frozen file**, and the Chunk R frozen-set note must say so rather than describing all four as documentation. |
| **7** | *"a stale artifact of a closed batch window (its sibling `collection.node_count` reads **1598** against today's 1746), so the plan records the state and leaves the re-pin decision to Chunk R."* | a stale artifact of a closed batch window (its sibling `collection.node_count` reads **1598** against the **1790** collected at `6618e54`), so the plan records the state and leaves the re-pin decision to Chunk R. |
| **8** | *"* **Prose integrity** — `python scripts/check_cairn.py` → `OK -- 180 Markdown file(s) scanned; no issues; 68 external link(s) not probed`, `as_of 2026-08-04`. Chunk D adds `dev/modules/content-security.md`, so the count grows by one plus whatever `dev/` artifacts this lifecycle itself contributes."* | **Prose integrity** — `python scripts/check_cairn.py` → `OK`, `as_of 2026-08-04` at `6618e54` the count read **195** Markdown files and 68 unprobed external links. **The assertion is `OK` and a non-decreasing count, not a literal figure**: this repository adds Markdown daily (180 → 195 in one day), so a pinned count is stale on arrival. Chunk D must grow it by at least one (`dev/modules/content-security.md`). |
| **9** | *"* **No change needed, checked rather than assumed** — `bootstrap/SAFETY.md:155` already names the `content-security` / `python-security` apparatus as Layer-4 code and stays true."* | **No change needed, checked rather than assumed** — `bootstrap/SAFETY.md:173` (`as_of 2026-08-04`; it was `:155` until `gate-claims-vs-enforcement` Chunk E, `84fbef4`, landed after the plan review) already names the `content-security` / `python-security` apparatus as Layer-4 code and stays true. **Re-locate by string, not by line** — that file is under a sibling scope's edit. |
| **10** | *"* **Descriptive / bootstrap prose** — `bootstrap/BOOTSTRAP.md` enumerates the default-on roster in **three** places (Act I-5 step 2, the Act I-6 summary template, and the hand-derived `modules:` example). **The proposal's documentation section did not name this file.**"* | **Descriptive / bootstrap prose** — `bootstrap/BOOTSTRAP.md` enumerates the default-on roster in **three** places (`:108`, `:215`, `:703`; measured — those are the only three), **and `docs/quickstart.md` and `docs/solo-legacy-recipe.md` each enumerate it once more** (B6, B7 — [I3]). **The proposal's documentation section named none of these three files.** The prose enumeration surface is now **complete, measured**: `grep -rl "fold-back-ledger"` across `docs/`, `bootstrap/` and `templates/` returns exactly these three files, the three `bootstrap/profiles/*.yml` (B3) and `templates/modules/README.md` (B5). |
| **11** | *"| A6 \| `bootstrap/_scaffold/cli.py` \| `main`'s **no-key** branch (`modules = list(_DEFAULT_ON_MODULES)`) appends `token_gated_modules(cfg)`, and its `[info]` line names the token-gated additions separately from the default-on set so the printed message stays true. **The `modules:`-alone branch is not touched** — that is the exact-list contract, and leaving it alone is the implementation of the Decision's precedence rule. |"* | Unchanged in substance, with one correction to its premise: **`cli.main` has four module-selection sites, not three.** A6 covers the **install-path** no-key branch (`bootstrap/_scaffold/cli.py:356`). The `modules:`-alone branch is still not touched. The fourth site gets its own row, **A7**. |
| **12** | *(insertion, no superseded text — new row appended to the Chunk A table)* | **A7 — `bootstrap/_scaffold/cli.py`, the `--summary` no-preset fallback.** The `--summary` handler has its **own** roster construction at `bootstrap/_scaffold/cli.py:236`–`239` (`mods = _as_str_list(...) if "modules" in summary_cfg else list(_DEFAULT_ON_MODULES)`); it builds the roster inline and **never calls `format_profile_summary`**, so A5 does not reach it. Extend the `else` limb with `token_gated_modules(summary_cfg)` and label the additions, exactly as A6 does on the install side. **Measured on the edited clone before A7:** a profile with `python_package: mypkg` and neither `preset:` nor `modules:` prints a **7-module roster with `python-security` absent**, then asks *"Does this profile look right before I install anything?"* — while the install of that same profile writes `scripts/run_security_audit.py` **and** the module's doctrine file under the target's `dev/modules/`. That is A5's stated failure mode inverted and made worse: the acceptance artifact promises absence and the module lands. |
| **13** | *"* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_presets.py bootstrap/tests/test_profiles_smoke.py bootstrap/tests/test_config_module.py -q` → green."* | → green **except** `test_presets.py::TestSoloLegacyRecipe::test_literal_recipe_yaml_round_trips_under_the_stdlib_parser`, which reports `AssertionError: assert 9 == 8` at `bootstrap/tests/test_presets.py:415`. That node is repaired in **Chunk B**, alongside the `docs/solo-legacy-recipe.md` prose it mirrors — **not** in Chunk A, because bumping the literal without the prose is the vacuity [I3] identifies. |
| **14** | *"reports **4 CHANGED** — and exactly the four in the table — **0 MISSING, 0 DUPLICATE**, and **2 NEW non-`Import:` / non-`Docstring` keys** with the two declared names. Any fifth CHANGED or third NEW key attributable to this scope is a stop-and-explain before the commit, not a ceremony-time discovery. *(The sibling's in-flight symbols will also appear; the assertion is over **this scope's** contribution, established by diffing against the same verify run on the pre-chunk working tree.)*"* | reports **4 CHANGED** — and exactly the four in the table — and **0 MISSING, 0 DUPLICATE**. **The NEW criterion is a set difference and carries no count.** `verify` emits a large standing set of NEW non-`Import:` / non-`Docstring` keys on the **unedited** engine (45 at `6618e54`), because the baseline is a **partial pin, not a complete inventory**; that set is **not** sibling work and must not be attributed to it. The assertion is: run `verify` before the chunk and after, and the **set difference of NEW non-`Import:` / non-`Docstring` keys is exactly `{Assign:_TOKEN_GATED_MODULES, FunctionDef:token_gated_modules}`**. Any fifth CHANGED, or any third key in that difference, is a stop-and-explain before the commit. **Do not carry a NEW-key count forward from this plan** — it drifts on every engine change. |
| **15** | *"* **The suite is red on exactly two nodes and no others** from this commit until Chunk R: the two `test_ast_attest.py` nodes. Any third failure is this plan's to explain."* | **From the Chunk A commit, the suite is red on exactly four nodes**: the two `test_ast_attest.py` nodes (red until Chunk R), plus `test_presets.py::TestSoloLegacyRecipe::test_literal_recipe_yaml_round_trips_under_the_stdlib_parser` and `test_quickstart_sequence.py::TestLayerAStepsOneThroughThree::test_step3_install_writes_expected_kernel_and_modules`, **both of which clear inside Chunk B**. Any fifth is this plan's to explain. **Working-tree note, before the commit:** three further nodes go red and **clear on the Chunk A commit itself** — `test_oracle.py::test_oracle_matrix_behavior_preserved`, `::test_oracle_privileged_workflows_preserved`, `::test_oracle_measures_target_not_verifier`. The differential oracle materializes its baseline at `baseline_ref="HEAD"`, so an *uncommitted* A1 makes every scenario report `only_in_current: scripts/content_scan_*`. Measured: 8 failed uncommitted → `test_oracle.py` 18 passed after committing A1–A6 on a scratch clone. **Do not re-anchor the oracle for this** — it is a working-tree artifact, not a gate anchor obligation. |
| **16** | *"| B3 \| `bootstrap/profiles/solo-greenfield.yml`, `collaborative-team.yml`, `high-rigor-legacy.yml` \| The "Resulting module roster" comment block in each is **re-derived from a live `expand_preset` run**, not hand-patched. All three are already wrong today (each omits `incident-trackers` and `documentation-plan`), so hand-patching would propagate an existing error. Record the derivation command in the commit body. |"* | Same action, corrected premise. **`bootstrap/profiles/solo-greenfield.yml:17`–`18` already lists all six default-on modules correctly**; only `collaborative-team.yml:16`–`17` and `high-rigor-legacy.yml:16`–`17` omit `incident-trackers` and `documentation-plan` (each lists four). Re-derive all three from a live `expand_preset` run anyway — the correct one must be **confirmed** by derivation, not assumed — and record the command in the commit body. |
| **17** | *"* **B3's rosters agree with the code, checked by running it**, not by reading it: for each preset, `expand_preset({"preset": p})[0]` is compared against the comment block by eye at implementation, and the three rosters are pinned by test in Chunk C."* | **B3's rosters agree with the code, checked by running it**, not by reading it: for each preset, `expand_preset({"preset": p})[0]` is compared against the comment block at implementation. **The clause "the three rosters are pinned by test in Chunk C" is struck as false** — no C1 pin reads a `bootstrap/profiles/*.yml` comment block, and `grep "Resulting module roster" bootstrap/tests/ scripts/` returns nothing at `6618e54`. **Stated residual:** the three comment blocks remain **unguarded** after this plan and can drift again; two of the three drifted this way already. Routed as *Lasting-truth migration* row 8. |
| **18** | Chunk B, row **B5** — *"The table's four pre-existing omissions are **not** fixed here; routed in *Lasting-truth migration*."* | Same two rows. **Six**, not four, pre-existing omissions remain after B5 — measured by deriving the table from `_MODULE_MAPPINGS` + `_DEFAULT_ON_MODULES` at `6618e54`: two default-on (`incident-trackers`, `documentation-plan`) and four team-gated (`doc-drift-prevention`, `examples-gallery`, `model-selection`, `testing-discipline`). They are **not** fixed here; routed in *Lasting-truth migration* row 2, whose list is the correct one. |
| **19** | *(insertion, no superseded text — new rows appended to the Chunk B table)* | **B6 — `docs/quickstart.md`.** Two edits at one site, and only one of them is guarded. `:129` carries `**6** modules listed <!-- verify: solo_greenfield_module_count -->`; `test_quickstart_sequence.py:235` extracts that integer and compares it to the live install, so the `6` → `7` bump is **mechanically enforced**. `:130`–`:131` then enumerates the six modules **by name** and **no test reads it** — the same unguarded shape as the recipe. Both must change; the green test proves only the first. <br> **B7 — `docs/solo-legacy-recipe.md`.** `:58`–`:62` claims *"an **8-module roster** — the six default-on modules (…) plus `legacy-agent` and `testing-discipline`"*. **No test extracts this prose.** It becomes a 9-module roster over seven default-on modules. **This obligation is not discharged by C4's `8` → `9` bump in `test_presets.py:415`** — that bump turns the suite green while leaving the recipe permanently wrong, which is exactly the vacuity Chunk C's own preamble rejects, arriving through a door the plan left open. Chunk B's commit body states both edits explicitly. |
| **20** | *"| C4 \| `bootstrap/tests/test_presets.py`, `bootstrap/tests/test_profiles_smoke.py` \| **Docstring-only.** The three tautological guards above are *kept* — they pin "the expansion consumes the table", which is real — and each gains one sentence stating what it cannot do (fail on a change to the table itself) and naming C1a as the guard that can. Both **frozen files**; no assertion changes, so no behaviour rides on a frozen-file edit. |"* | **C4 is docstring-only for `bootstrap/tests/test_profiles_smoke.py`, and docstring-plus-one-assertion for `bootstrap/tests/test_presets.py`.** The three tautological guards are kept and each gains its one sentence, as before. **Additionally**, `bootstrap/tests/test_presets.py:415`'s `assert len(modules) == 8` becomes `== 9`. `test_presets.py` **is** a frozen file, so **a behaviour-bearing change does ride on a frozen-file edit**, and the *"no assertion changes"* justification is withdrawn. The bump is committed **together with B7's prose fix in Chunk B**, never alone, and Chunk B's perturbation ledger records that the prose is the claim and the literal is only its mirror. |
| **21** | *"| C1j `test_the_profile_summary_names_the_token_gated_addition` \| `scaffold.py --summary` over a preset + filled token names `python-security` under the token-gated line \| Delete A5's summary line → red |"* | **C1j `test_the_profile_summary_names_the_token_gated_addition` — two shapes, two code paths.** (i) **preset + filled token** → `scaffold.py --summary` names `python-security` under the token-gated line; **perturbation:** delete A5's summary line → red. (ii) **no `preset:`, no `modules:`, filled token** → `scaffold.py --summary` names `python-security` in the roster it prints; **perturbation:** revert A7's `else` limb to bare `list(_DEFAULT_ON_MODULES)` → red. Shape (ii) exercises the inline `--summary` fallback, **a different function from `format_profile_summary`**, which is why one pin over one shape does not reach it. |
| **22** | *"**Two further pins in C1, both non-obvious and both required by the Decision:**"* | **Three further pins in C1, all non-obvious:** C1k and C1l as written, plus **C1m** below. |
| **23** | *(insertion, no superseded text — new pin appended after C1l)* | **C1m `test_the_summary_and_the_install_agree_on_the_roster_for_a_no_preset_profile`** — the pin that closes [I1] **structurally** rather than branch-by-branch. For a profile with `project_name` + `python_package: mypkg` and neither `preset:` nor `modules:`: capture `scaffold.py --summary` stdout, then run the real install into `tmp_path`, and assert **the module set the summary names equals the module set whose files actually landed**. **Perturbation:** revert A7 → the summary omits `python-security` while `scripts/run_security_audit.py` and the module's doctrine file under the target's `dev/modules/` are written → red. **Oracle independence:** the two sides are a parsed stdout roster and a filesystem listing, neither derived from `_DEFAULT_ON_MODULES` or `_TOKEN_GATED_MODULES`. This pin is what makes a *fifth* selection site a test failure rather than another enumeration miss — the failure class the review names as this plan's characteristic weakness. |
| **24** | *"* `bootstrap/tests/test_default_security_stance.py` *(new; a `Proposed paths:` entry until Chunk C)* — the twelve selection-contract pins."* | — the **thirteen** selection-contract pins (C1a–C1j, C1k, C1l, C1m). |
| **25** | *"1. **Readiness condition.** All four implementation chunks are in the tree, the suite is green **except** the two `test_ast_attest.py` nodes, and this plan's contribution to the union is exactly the declared four CHANGED + two NEW keys."* | **1. Readiness condition.** All four implementation chunks are in the tree; the suite is green **except** the two `test_ast_attest.py` nodes — the two [I2] nodes are repaired inside Chunk B and **must not** be carried to R; the three `test_oracle.py` transients cleared at the Chunk A commit and **must not** appear; and this plan's contribution to the union is exactly the declared four CHANGED + two NEW keys, established as a **set difference** per amendment 14. |
| **26** | *"3. **The `known_new` manifest.** The two NEW keys — `Assign:_TOKEN_GATED_MODULES` and `FunctionDef:token_gated_modules` — need digest pins in `bootstrap/tests/fixtures/scaffold_ast_known_new.json`, measured at ceremony time against the landed bodies. Their **key set** is declared in advance; their digests cannot be."* | **3. The `known_new` manifest — declared, but its necessity is an open Maintainer question.** The two NEW keys are `Assign:_TOKEN_GATED_MODULES` and `FunctionDef:token_gated_modules`; their **key set** is declared in advance and their digests cannot be. **Whether they need pins in `bootstrap/tests/fixtures/scaffold_ast_known_new.json` is unresolved**: `known_new` is read **only** by `update_symbol` (`bootstrap/tests/_ast_attest.py:230`) and never by `verify`, and this plan establishes on two independent grounds that `update-symbol` is unavailable to this scope. Either the pins are unnecessary here, or the ceremony mechanism is not the direct-correction script this plan names. **The Maintainer decides at ceremony time**; the implementing agent declares the key set and stops. |
| **27** | *"4. **The frozen-set decision.** Four frozen files are modified and one is `FROZEN-NEW`; `bootstrap/tests/fixtures/gate_manifest.json` also carries a `cascade_mutable` entry for `bootstrap/_scaffold/config.py` and a `collection.node_count` of 1598 against today's 1746, both stale from a closed window."* | **4. The frozen-set decision.** Four frozen files are modified — **one of them (`bootstrap/tests/test_presets.py`) with a behaviour-bearing assertion change, not documentation** — and one is `FROZEN-NEW`; `bootstrap/tests/fixtures/gate_manifest.json` also carries a `cascade_mutable` entry for `bootstrap/_scaffold/config.py` and a `collection.node_count` of **1598** against the **1790** collected at `6618e54`, both stale from a closed window. |
| **28** | *"| 3 \| **The vendor-wrapper root gap.**"* *(migration table, row 3's leading cell)* | Unchanged; **two rows are appended** — **row 8: the three `bootstrap/profiles/*.yml` "Resulting module roster" comment blocks stay unguarded** by any test after B3 (`dev/PLANNING.md > Deferred follow-ups`; candidate fix: generate the blocks, or extract-and-compare them the way `test_quickstart_sequence.py` does for `docs/quickstart.md`). **Row 9: `docs/solo-legacy-recipe.md`'s roster prose stays unguarded** after B7 — `test_presets.py:415` pins the resolver arithmetic, not the sentence (`dev/PLANNING.md > Deferred follow-ups`). |
| **29** | *"* **Every new node shown non-vacuous by a RUN perturbation**, ledger in the commit body — the change made, the failure observed with its message, the byte-identical restore verified."* | Unchanged, with one addition: **the ledger records the interpreter and the commit sha the perturbation ran at.** Two of this plan's own figures and three of its review's went stale inside 24 hours because they were quoted without a sha; a perturbation ledger without one is not reproducible either. |

### Clearance

**This Response does NOT clear the plan to implement.** What remains, stated
without softening:

1. **The declared tier is undischarged.** `required(**External**, security lens)`
   and the tree holds only an Internal, same-agent-type section. **I am the
   plan's author** — this Response is neither Internal nor External review and
   cannot discharge either. Per the plan's own header and
   `doctrine/plans.md`'s plan-review precondition, **no implementation commit
   lands** until an External security-lens section is committed.
2. **The External reviewer reads the amended shape.** The Internal round's
   second-round recommendation was *"REVISE, then proceed to the required
   External security-lens round — and the revision should land before that
   round, not after."* That is what this Response is; the External round starts here.
3. **Four things the External reviewer should attack first**, replacing the
   original brief's list, which the Internal round has already discharged (C2,
   A4/C1g and the symbol delta all survived direct falsification, twice):
   * **The fifth selection site.** Neither the Internal round nor I proved the
     `cli.main` enumeration complete — we each found sites by reading and then
     confirmed by running. C1m is designed to convert a missed site into a red
     test rather than a silent gap; **check that it actually would**, and look
     for a shape it does not reach (`upgrade --adopt-module` with a token
     declared is the one I would try first).
   * **[R4], the `known_new` question.** If the ceremony genuinely needs pins
     that only an unavailable tool consumes, Chunk R has a hole.
   * **Chunk D, still entirely unexecuted.** The 81→87 / 14→15 / 74→76 / 41→43
     arithmetic is consistent but **unverified**, and D3's alarm-fatigue
     measurement — the one number the whole restated argument rests on — cannot
     be taken by any reviewer. It is the plan's largest open risk and it is
     structurally deferred to implementation.
   * **Whether the stale-figure pattern is a plan defect or an environment
     defect.** Three separate measurement frames (the plan's, the review's, and
     the pre-Ceremony-1 baseline) went stale inside 24 hours in a repository with
     nine concurrent scopes. Amendment 29 is a partial mitigation. A reviewer may
     reasonably conclude the plan should assert **invariants and directions**
     rather than counts nearly everywhere it currently asserts a number.
4. **Nothing in this Response changes code.** No source file, test, fixture,
   template or doc was modified; the amendments are instructions to Chunk A–D,
   not their execution.

This section is append-only once written.
