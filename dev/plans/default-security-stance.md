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
