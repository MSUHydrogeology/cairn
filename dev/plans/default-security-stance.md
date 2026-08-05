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
commit lands before all three of the following hold.** (i) A dated `## Plan
review` section is in the tree — **satisfied**, `2077a25`. (ii) The findings it
raised are dispositioned in a dated section — `doctrine/plans.md:114`-`:117` makes
the disposition the *second limb* of the plan-review precondition, and the
mechanical helper (`_has_kind` in `templates/skills/_lib/lifecycle_planner.py`)
checks only the first, so this limb is carried by a human reader. (iii) **Gate
D-ON** is satisfied for any chunk it fences. The 2026-08-05 External verdict was
REVISE and the **Maintainer has disposed of the round** — see *Maintainer
disposition of the 2026-08-05 External review round*. See also *Plan review — the
brief*.
**Last update**: 2026-08-05
**Opened**: 2026-08-04

## Folded, not amended — how to read this plan

**An implementing agent who reads only the chunk tables and their acceptance
criteria executes the current spec.** Amendments 1-44, which the two author
Responses bound *by reference*, are folded into the operative rows.
`doctrine/plans.md:202-207` makes chunk-table cell text mutable in place while a
plan's status is `open` with no commits in flight against the chunks being edited
— this plan's exact state: status `open`, zero implementation commits.

The `## Plan review`, `## Response to plan review`, `## Lasting-truth migration`
and `Sharpening` sections are **untouched and stay append-only**. The fold ledger
in `### Sharpening — the 2026-08-05 fold pass` at the end of this file names every
amendment row now carried by a cell **and every row that is not folded**.

**Where a folded cell and an amendment row disagree, the cell governs.** In
particular the shared *Gate D-ON* block supersedes **amendment 32**'s `G1`/`G2` in
their entirety.

**Notation — `[E#]` is overloaded in this file, and the two populations must not be
confused.** Bare `[E1]` / `[E2]` / `[E3]` in the plan body always mean the *source
proposal's* External reviewer. The 2026-08-05 plan review's findings are cited as
`[PR-E1]` / `[PR-E2]` / `[PR-E3]`. The Internal round's findings keep `[I1]`-`[I5]`;
the 2026-08-04 Response's own additions keep `[R1]`-`[R5]`; the 2026-08-05
Response's are `[S1]`-`[S7]`.

## Maintainer disposition of the 2026-08-05 External review round

The 2026-08-05 External round (`## Plan review -- Codex (External) -- 2026-08-05`,
introduced by `e1b2e30`) returned **REVISE**. The Maintainer has disposed of it.
The authorizing instruction, quoted verbatim and visually isolated:

> Go ahead with implementation once you've revised these. I don't want another review round

**What it disposes of.** The **review round**: the REVISE no longer fences
implementation, and no round-2 External section is owed. This is a disposition,
**not a bypass** — the round's finding is *closed in the operative text* (the shared
*Gate D-ON* block, which replaces `G1`/`G2` and is byte-identical to the copy in
`dev/plans/content-scan-detectors.md`), not waived.

**What it does not supply, enumerated so nothing further is read into it.**

* **No Maintainer credential, key, token or signing ref.** Nothing in this plan
  needs one — already stated as a checked fact in *Chunk R*.
* **No AST re-anchor ceremony and no gate-manifest re-pin.** *Chunk R* is
  untouched: an implementing agent still does not enter it.
* **No approval to push.** Pushing takes its own approval (`AGENTS.md` > *Git and
  commit workflow*); the deliberation-layer carve-in covers `git commit` only.
* **No disposition of the default-on consequence.** That is the separate question
  Gate D-ON condition **D-ON-2** names — the whole-script-Cyrillic and
  international-proper-noun cost *under default adoption* — and it is **NOT MET**.
  **So Gate D-ON is still closed, and it fences Chunk A, Chunk B, Chunk C and
  Chunk D. In practice that is this whole plan.** The Maintainer's instruction
  unblocks *revision-then-implementation* in general; it does not open this gate.
* **No ratification of D3's 52-flag HOLD.** That trigger is firing on its own
  terms; see Chunk D row D3.

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

* **The suite criterion is an invariant; the number is provenance only.**
  Invariant: **0 failed / 0 skipped / 0 xfailed**, and **collection grows by
  exactly this plan's new nodes and drops none**, established by a **same-session
  before/after pair** — never against a figure quoted from this file. A dropped node
  or a new skip/xfail marker is a HOLD class. Provenance: **1987 nodes collected**,
  `as_of 2026-08-05` at `66ce8c0`. The frame has now moved four times in three days
  (**1744 → 1790 → 1959 → 1987**), which is exactly why the criterion is the delta
  and not the count.
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
* **Prose integrity** — `python scripts/check_cairn.py` → **`OK`, and
  `dev/modules/content-security.md` is in the scanned set after Chunk D. The
  "non-decreasing count" criterion is withdrawn as unsound**, and the "+1" with it.
  `check_cairn.main` filters `git ls-files '*.md'` through `link_check.filter_sources`
  (`scripts/link_check.py:503`), which drops `dev/**/archive/`, `dev/modules/`,
  `dev/.cairn/` and `dev/reflections/` **as sources** — so archiving a plan or
  proposal *decreases* the count, and a non-decreasing gate would fire on a correct
  archive. Note the interaction: because `dev/modules/` is excluded, Chunk D's
  installed module doc is scanned by `content_scan_runner.py` (whose `!dev` root has
  no such exclusion) but **not** by `check_cairn`, so it never raises that count at
  all. Re-measured `as_of 2026-08-05` at `66ce8c0`: **178 file(s) scanned; 48
  external link(s) not probed; 2 issue(s)** — both `[path]` flags in
  `dev/plans/review-gate-enforcement.md` from a concurrent scope's **uncommitted**
  work, neither this plan's. **Assert `OK` and assert membership where membership is
  what matters — never a count, never a direction.**
* **The release Bandit gate — assert the delta, never the absolute.**
  `scan_targets()` returns **76** targets, re-measured `as_of 2026-08-05` at
  `64e8b7c`, **not the 74 this plan and both review rounds recorded**:
  `scripts/transition_lint.py` and `scripts/transition_lint_whitelist.py` were added
  by an unrelated scope at `4a7d70a`, which means the old "74 → 76" criterion is
  *already satisfied by someone else's work and gates nothing*. **Re-measure
  immediately before Chunk D and assert exactly +2 targets, naming the two new paths
  as `scripts/content_scan.py` and `scripts/content_scan_runner.py`** (expected 78
  if the base is still 76). Both new targets are byte-identical to template files
  Bandit already reads — confirmed at `64e8b7c`, where the manifest-derived set
  already contains `templates/modules/team-gated/content_scan.py` and
  `templates/modules/team-gated/content_scan_runner.py` — so the severity histogram
  must not gain a MEDIUM+.
* **Cairn's lockfile** — `dev/.cairn/cairn-lock.yml` records **81 files / 14
  modules** with **41** `scripts/` + `tools/` `.py` twin records, all re-measured
  `as_of 2026-08-05` at `64e8b7c` by parsing the lock (the plan's 2026-08-04 figures
  reproduce). After Chunk D: **87 files / 15 modules / 43 twins**. Five records
  currently carry legitimate customization drift (`AGENTS.md`,
  `dev/NEXT_SESSION.md`, `dev/PLANNING.md`, `dev/collaboration_agreement.md`,
  `dev/modules/security-review.md`); **every one of the 41 twins is hash-clean**,
  which is the invariant Chunk D must not break. **Re-derive by parsing the lock at
  implementation, not by trusting these numbers.**

### Gate D-ON — the default-on admission gate

**This block is shared, verbatim, with the reciprocal plan
(`content-scan-detectors` <-> `default-security-stance`). A change to it lands
in both files in the same commit, or it has not landed.** Identical copies are
what stop either plan from reporting ready while its reciprocal is blocked.

No chunk that flips a default selection from false to true lands until all
three conditions hold. Each names *how it is determined*, and none is
determined by a date or a position written inside the plan.

* **D-ON-1 — the governing External round carries no outstanding REVISE.**
  Determined by: enumerate every `## Plan review` section in this file whose
  body carries `**Tier**: External`; for each, take the commit that introduced
  it (`git log --format='%h %ad' --date=short -S '<its exact heading line>' --
  <this file>`); the **governing** round is the one with the latest introducing
  commit. Its verdict must not be REVISE. *The existence of a review section is
  not discharge of a finding* — a SHIP, or a Maintainer disposition recorded
  under D-ON-2, is.
  **Why not file order, and why not the heading date.** Neither is provenance.
  File position is editable and is already non-monotonic in this tree:
  `dev/plans/portable-security-sweeps.md` carries its newest External section
  (introduced by `e1b2e30`) at a *lower* line than the Response it answers, and
  above an older External section introduced by `976b402`. The heading date is
  author-written text inside the artifact under gate, so reading it lets the
  gated party choose its own gate.
* **D-ON-2 — the Maintainer's disposition of the default-on consequence is
  recorded.** Determined by: a section in this plan that quotes the authorizing
  instruction **verbatim and visually isolated** and names the consequence being
  disposed of. Absent that quoted authorization the gate is NOT MET, whatever an
  author Response asserts.
* **D-ON-3 — the named default-adoption corpus is in the binding test
  contract.** Determined by: each named corpus row exists as a parametrized case
  in the named test file, and the suite passes with those cases present. Prose
  that *cites* an example does not satisfy this; a row that is not in the test
  file does not count, including a row named in an amendments table.

D-ON is outcome-based, not round-counting: a single focused closure round may
satisfy D-ON-1. It does not weaken the requirement that the findings themselves
be settled.

**Plan-local notes on applying D-ON.** Not part of the shared block. The
reciprocal plan (`dev/plans/content-scan-detectors.md`) carries the same four
notes.

* **What D-ON fences in this plan, and it is more than amendment 32 said.**
  **Chunk A** — row A1 *is* the flip from false to true. **Chunk B** — its prose
  asserts A1's behaviour, so it cannot truthfully land first. **Chunk C** — pins
  C1a, C1b and C1h assert A1's behaviour and are red without it. **Chunk D** — the
  self-adoption. **In practice Gate D-ON fences this entire plan**, which is the
  reviewer's finding taken at face value rather than softened. Amendment 32
  considered splitting the token-gate half (A2-A6, which flips no *default*
  selection) out and landing it early and **declined**: a half-landed engine change
  parked in a five-scope `config.py` window is a new hazard, and narrowing a gate an
  External reviewer set is the author's least defensible move. **The Maintainer may
  narrow it; the author does not.**
* **D-ON-1's enumeration, run here.** Sections in this file matching `^## Plan
  review` whose body carries `**Tier**: External`: **exactly one** — the section
  headed `## Plan review -- Codex (External) -- 2026-08-05`, introduced by
  **`e1b2e30`** (2026-08-05). Measured `as_of 2026-08-05` at `66ce8c0` with `git
  log --format='%h %ad' --date=short -S '## Plan review -- Codex (External) --
  2026-08-05' -- dev/plans/default-security-stance.md`. The governing round is
  therefore that section and its verdict is **REVISE**. **Cited by heading text
  rather than by line number, deliberately:** a line citation into the same file
  that carries it shifts on every edit, including the edit that writes it. **A
  standing obligation follows:** every future External section in either plan
  **must** carry a `**Tier**: External` line — the two earlier External sections,
  each headed `## Plan review -- Codex (External, security lens) -- 2026-08-05`,
  one in each plan, do **not**, so a round that omits the marker is invisible to
  the enumeration and an older *marked* section would be read as governing. That is
  a gate an author could walk through by forgetting a line.
* **D-ON status today.** **D-ON-1 — NOT MET.** The governing verdict is REVISE, and
  D-ON-1 admits only two discharges: a SHIP, or *"a Maintainer disposition recorded
  under D-ON-2"*. The Maintainer's 2026-08-05 instruction disposes of the **review
  round** and is recorded above; it is **not** a D-ON-2 disposition, because it does
  not name the default-on consequence. With a further round declined, the only
  remaining route to D-ON-1 is a D-ON-2 disposition, which discharges both at once.
  **D-ON-2 — NOT MET**, and it is the load-bearing one: the question is the
  whole-script-Cyrillic and international-proper-noun cost *under default adoption*,
  which `dev/plans/content-scan-detectors.md`'s own *Known omissions* (e) raises and
  does not answer. **D-ON-3 — NOT MET today, satisfied by that plan's Chunk D**: the
  named corpus is its *The default-adoption corpus* subsection (Appendix F's 71
  fixture ids plus three External-reviewer-supplied rows `RX-1`-`RX-3`), and the
  named test file is `bootstrap/tests/test_content_scan.py`
  (`test_appendix_f_fixture_contract`, its row D14). Checked `as_of 2026-08-05` at
  `64e8b7c`: no such parametrized cases exist in that file yet.
* **A measured correction to the shared block's rationale, reported rather than
  silently fixed.** The block's *"Why not file order"* paragraph says
  `dev/plans/portable-security-sweeps.md` carries its newest External section
  *"above an older External section introduced by `976b402`"*. **That clause does
  not reproduce.** Measured `as_of 2026-08-05` at `64e8b7c`: the `976b402` section
  is at `dev/plans/portable-security-sweeps.md:1153` and the `e1b2e30` section is at
  `:2253` — the newest is **below** the older. The load-bearing half *does*
  reproduce: the `e1b2e30` section at `:2253` sits at a **lower** line than the
  Response at `:2275` that it re-reviews, and that Response was introduced by
  `38858f1`, an **earlier** commit than `e1b2e30` (`976b402` 08:02 → `38858f1` 09:00
  → `e1b2e30` 10:02, same day). File position is therefore non-monotonic in
  introducing-commit order in that tree, exactly as the block claims, and the
  determination rule is unaffected. The block is left **byte-identical in both
  plans** rather than reworded, because byte-identity is the property that stops the
  two sides drifting; the correction lives here and in *Sharpening*.

**The reciprocal obligation is discharged by this commit.** Amendment 32 recorded
the sibling half as *"an obligation on that plan's author"* and routed it to
migration row 10; the reciprocal plan's own AM-25 recorded the gate as
*"half-stated"*. Both plans now carry the identical block, landed in one commit, so
migration row 10 is **moot** and no new row is owed. The append-only migration table
is untouched.

## Sequence

Chunk order is load-bearing. **C lands before D**: the twin pins must exist and
be red-for-the-right-reason before the twin is installed, so that "the test went
green" is evidence the install happened rather than evidence the test never
looked.

```
0. plan-open -- this plan + the dev/PLANNING.md row-move            [commit pending]
   (plan review) -- required(External, security lens). Internal landed 2026-08-04;
                    External landed 2026-08-05, verdict REVISE, disposed of by the
                    Maintainer (see the disposition section). No round 2 owed.
   (gate D-ON)   -- Gate D-ON, in "The cluster constraint". NO Chunk A, NO Chunk B,
                    NO Chunk C, NO Chunk D before D-ON-1..3 all hold.
   Both gate lines have exactly one trigger: a person reading them. No test, no
   hook, no CI enforces either -- Cairn has no CI.
1. Chunk A -- engine: default-on + the token gate                   [commit pending]
2. Chunk B -- the doctrine and prose the engine change falsifies    [commit pending]
3. Chunk C -- the selection contract, pinned with literal names     [commit pending]
4. Chunk D -- Cairn adopts content-security on itself               [commit pending]
   Chunk R -- MAINTAINER FENCE: the shared re-anchor ceremony       [Maintainer]
```

---

### Chunk A — engine: `content-security` default-on, `python-security` token-gated

> **FENCED BY GATE D-ON.** Row **A1 is the default-on flip itself**, so no part of
> this chunk lands until D-ON-1, D-ON-2 and D-ON-3 all hold (*The cluster
> constraint* > *Gate D-ON*). All three are **NOT MET** today. The token-gate half
> (A2-A6) flips no *default* selection and could in principle be split out; the
> author **declined** to narrow the gate that way, and only the Maintainer may.

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

> **FENCED BY GATE D-ON.** Every sentence this chunk writes *asserts A1's
> behaviour*, so it cannot truthfully land before A1. The fence is therefore the
> same one, not a weaker one.

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

* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → **`OK` and no new
  flag. The "count may only grow" criterion is withdrawn as unsound** —
  `link_check.filter_sources` drops archived, `dev/modules/`, `dev/.cairn/` and
  `dev/reflections/` sources, so a correct archive *lowers* the count. Assert `OK`
  and compare the flag set, never the count.
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

> **FENCED BY GATE D-ON.** Pins **C1a**, **C1b** and **C1h** assert A1's behaviour
> and are red without it, so this chunk does not land ahead of A either.

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

> **FENCED BY GATE D-ON**, and additionally **HELD by D3's own stop trigger**
> (below), which is already firing on a pre-implementation measurement.

Order-sensitive; see *The cluster constraint*. This is the half that answers the
Maintainer's direction directly, and under the Decision it is much smaller than
the proposal drafted.

| # | File / action | Change |
|---|------|--------|
| D1 | `python bootstrap/scaffold.py upgrade --adopt-module content-security --target .` | The **adopter-facing** mechanism, deliberately — Cairn dogfoods the same opt-in path an existing adopter uses. It installs each spec's `dst` that is missing on disk and records six lockfile entries: `dev/modules/content-security.md` (substituted → `base_cache` + `base_hash`), `scripts/content_scan.py`, `scripts/content_scan_runner.py`, and the three `content_scan_*.txt` policy files (all verbatim). **Not a hand-edit of `dev/.cairn/cairn-lock.yml`** — that file is tool-owned and regenerate-only, and [E3] is on record that hand-editing it inverts the documented workflow. |
| D2 | `dev/.cairn/profile.yml` | **No edit, and that is a decision rather than an omission.** Cairn's profile is `preset: collaborative-team`, which after Chunk A resolves to include `content-security` mechanically. Adding `modules_add: [content-security]` would be redundant *and* actively harmful: it would mask the default-on path, so a regression that dropped the module from `_DEFAULT_ON_MODULES` would leave Cairn's own tree silently unaffected — the repository would stop being its own first adopter for exactly the property under test. And per the Decision, no `python_package` token is added. |
| D3 | `scripts/content_scan_residuals.txt` | **The measurement, and a threshold with no judgment in it.** Run `python scripts/content_scan_runner.py` once over Cairn's tree and **record the exit code and the flag count in the commit body**. The three REQUIRED roots (`AGENTS.md`, `.agents/skills`, `dev`) all exist in Cairn — re-verified `as_of 2026-08-05` at `64e8b7c` by running the scanner, which scanned the audited set and exited **1** rather than failing closed at 2. **The decision rule, and the implementer applies no other: exit 0 → proceed; any non-zero exit → HOLD and put it to the Maintainer.** No count appears in the rule, because the shipped `content_scan_residuals.txt` is a sentinel-only empty baseline, so every flag is NEW and *"any unsuppressed finding"* and *"exit non-zero"* are the same condition. **The pre-measured baseline this compares against, re-measured for the fold pass** in a scratch `git clone` at `64e8b7c` with the five shipped `content_scan*` files copied verbatim into `scripts/`: **80 audited files, 52 flags, 52 NEW, exit 1**, all 52 `[suspicious-url]`, concentrated in `dev/strategy/` and `docs/further-reading.md`. (The 2026-08-05 Response recorded 78 files / 52 flags at `b8ab678`; the flag count reproduces, the file count has grown.) **So the HOLD is already triggered before implementation** — Chunk D will not exit 0 on a clean adoption, and the implementer is not the one who decides what to do about it. **The implementer adds no residual and no allowlist entry.** Whether these editorial-citation hits are cleared by trusted-publication entries in `content_scan_allowlist.txt`, by reviewed `[editorial-url]` residual entries, or by neither, is a **policy decision under D3's own escalation trigger and it is the Maintainer's**. A blanket suppression remains the alarm-fatigue failure the proposal names and is not acceptable at any volume. **Expect ≥ 52, not = 52**: `--adopt-module` writes `dev/modules/content-security.md` inside the audited `!dev` root, and this lifecycle's own `dev/` artifacts are audited too. |
| D4 | — | Confirm the twin invariant Chunk D must not break: all `scripts/` + `tools/` `.py` lockfile records stay hash-clean (41 today, 43 after). |

**Acceptance criteria — Chunk D.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_notice_install.py -q` → green, **including C2's two named pins**, which were red before this chunk. That transition is the acceptance evidence.
* `~/conda_envs/lhm/bin/python3.13 bootstrap/security_check.py` → `PASS`, with
  **the target count exactly +2 against a pre-chunk measurement taken in the same
  session**, and the two added paths identified as `scripts/content_scan.py` and
  `scripts/content_scan_runner.py`. **The literal "76 (from 74)" is struck**: the
  base is already **76** at `64e8b7c`, so the old criterion is satisfied by an
  unrelated scope's work and gates nothing. Both new targets are byte-identical to
  template files Bandit already reads, so the severity histogram gains **no
  MEDIUM+**; a MEDIUM+ appearing is a stop.
* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → **OK**. **The "+1" is
  struck**: `dev/modules/` is excluded from `check_cairn`'s scan set by
  `link_check.filter_sources`, so the installed module doc does **not** raise that
  count at all, and a concurrent archive can lower it. The assertion is `OK` and no
  new flags.
* **The lockfile moved exactly as predicted**: 81 → **87** files, 14 → **15**
  modules. Re-derive rather than trust: parse the lock and count. The five
  pre-existing customization-drifted records are unchanged in number.
* **The content-scan measurement is recorded, and the exit code is the gate.** The
  exit code **and** the flag count from D3 go in the commit body, even when the
  count is zero. **The comparison is the pre-measured Cairn baseline in D3 — 80
  audited files / 52 flags / exit 1 at `64e8b7c` — not the proposal reviewer's
  34 / 39 / 42-file clean runs**, which were taken on fresh scaffolds with no
  bibliography and do not predict a tree that cites literature. **Acceptance is
  `exit 0`; any non-zero exit is a HOLD to the Maintainer**, not a number for the
  implementer to weigh.
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
3. **The `known_new` manifest — decided now, and the decision is: do not touch
   it.** **This scope does not edit, re-pin, or add entries to
   `bootstrap/tests/fixtures/scaffold_ast_known_new.json`.** Settled ahead of the
   ceremony rather than during it, on measured grounds: `verify` is
   `verify(baseline_path, module_paths)` in `bootstrap/tests/_ast_attest.py` and
   never reads the manifest; `known_new` is `update_symbol`'s keyword parameter, and
   `update-symbol` is unavailable to this scope on two independent grounds already
   established above; and — decisively — `verify` at `b8ab678` emitted **78 `note:
   NEW` keys, 45 of them non-`Import:` / non-`Docstring`, and still returned rc
   0**, so an unpinned NEW symbol is a note and not a failure. Those 45 survived
   Ceremony 1 unpinned; this scope's two join them on identical terms.
   **Re-derive the NEW-key report at ceremony time rather than carrying those
   counts forward.** <br> **What the implementing agent does instead:** declare the
   **exact NEW-key set — `Assign:_TOKEN_GATED_MODULES` and
   `FunctionDef:token_gated_modules`, and nothing else** — and stop. **Any third
   NEW non-`Import:` / non-`Docstring` key attributable to this scope, established
   as the set difference of the before/after `verify` pair, STOPS THE CEREMONY.** No
   digest is pre-declared, because none is needed.
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
    suite, **0 failed / 0 skipped / 0 xfailed** after Chunk R, under the canonical
    interpreter (3.13.13) with `PYTHONDONTWRITEBYTECODE=1`. **The criterion is the
    delta, established by a same-session before/after pair; the number is
    provenance only** (**1987 collected**, `as_of 2026-08-05` at `66ce8c0`; the
    plan's 1744 does not reproduce and neither do the two AST failures, which were
    a sibling's uncommitted work). Collection grows by exactly this plan's new
    nodes and drops none. **Do not compute a delta against any number written in
    this file.**
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
  **target count +2 across Chunk D against a same-session pre-chunk measurement**
  (base **76** at `64e8b7c`; the absolute is not pinned, and the plan's original
  "74 before" is stale), the two added paths named, and no MEDIUM+ appearing.
* **The lockfile assertion** — parse `dev/.cairn/cairn-lock.yml` and count:
  81 → 87 files, 14 → 15 modules; all `scripts/` + `tools/` `.py` records
  hash-clean (41 → 43). The pre-chunk side (81 / 14 / 41) re-measured `as_of
  2026-08-05` at `64e8b7c`; **re-derive it again immediately before Chunk D rather
  than trusting the figure.**
* **The content-scan measurement** — `python scripts/content_scan_runner.py` on
  Cairn's tree after Chunk D. **Exit 0 → pass; any non-zero exit → HOLD to the
  Maintainer.** The exit code and the flag count are both recorded in the commit
  body, against the pre-measured baseline in D3 (80 audited files / 52 flags /
  exit 1 at `64e8b7c`).
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

## Plan review -- Codex (External, security lens) -- 2026-08-05

**Verdict: REVISE.** The exact-list boundary, `modules_remove` precedence, and
the previously missed no-preset summary shape are now specified with useful
public-path tests. I also agree with the later correction that selection has
five construction sites, not four. Defaulting a scanner is nevertheless a
behavioral commitment to every new adopter, so its dependencies and ceremony
choices need to be settled before the engine changes land.

**[E1] Default adoption is not gated on the scanner's unresolved security
posture.** This plan makes `content-security` unavoidable for presets and the
no-key path while the sibling content-scan plan still records an unpriced
whole-script/Cyrillic boundary and lacks an External security disposition on
its test material. An explicit modules list remains an opt-out, but most new
adopters will never exercise it. Add a hard sequencing condition: no default-on
selection or Cairn self-adoption until `content-scan-detectors` has its required
External security review and the default-on consequence has a recorded
disposition. This is not a request to solve that detector scope here; it keeps a
high-blast default from overtaking its security evidence.

**[E2] The `known_new` choice must be decided before, not during, the ceremony.**
The response correctly establishes that `verify` does not consume
`scaffold_ast_known_new.json` and the direct-correction path is unavailable.
That is sufficient to make the plan's original pin requirement inapplicable:
do not edit or re-pin `known_new` for this scope. Leave a named, exact NEW-key
set in the declaration and require any unexpected NEW key to stop the ceremony.
Asking the Maintainer to decide the mechanism while performing a trust-root
ceremony turns a technical ambiguity into pressured operator judgment.

**[E3] The alarm-fatigue stop needs a measurable escalation threshold.** D3 says
to stop on a "non-trivial" flag count but supplies neither a baseline fixture
nor a decision rule. A default-on scanner cannot safely rely on an implementer
to intuit when an unfamiliar warning volume is material. Define the comparison
(including the roots and committed tree it is measured from) and a small,
actionable hold condition such as any unsuppressed finding or any count above
the independently recorded baseline; route exceptional expected findings to
review rather than a commit-body judgment.

I inspected the operative chunks, the Internal review/Response/amendments, and
the two later figure corrections. I did not execute a proposed engine delta or
an adoption command, because no implementation is present and the review is of
the plan rather than a candidate tree.

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

### Figure correction -- Claude -- 2026-08-04

An audit of the Response committed at `bd661fa` reported one figure in it that
does not reproduce. I re-measured that figure from scratch, adopting neither
the Response's number nor the audit's, and I re-derived the conclusion the
figure was offered in support of rather than inheriting it from either. A
second number the audit raised as a note rather than a defect is measured here
as well, because it too is stated as a figure inside an in-force amendment.

**Nothing here changes a disposition.** Every finding stays accepted,
accepted-with-modification, or declined exactly as the Response left it. This
section corrects evidence and states, for each corrected figure, whether the
amendment carrying it survives.

Measurement provenance: the Response's own commit is `bd661fa`; repository HEAD
when I ran was `4a7d70a`. The working tree carried other agents' uncommitted
edits throughout, so the two decisive runs below read **tree objects**, not the
working tree.

#### 1. The `fold-back-ledger` enumeration grep -- amendment **10**, and its twin in the `[I3]` disposition row

**What was claimed.** Amendment 10 declares the prose enumeration surface
"complete, measured", on this evidence:

> `grep -rl "fold-back-ledger"` across `docs/`, `bootstrap/` and `templates/`
> returns exactly these three files, the three `bootstrap/profiles/*.yml` (B3)
> and `templates/modules/README.md` (B5).

That is seven files. The `[I3]` disposition row states the same seven and adds
*"and I assert that as a measurement."*

**What I measured: seventeen.** Three runs, two of them index- and
worktree-independent:

| # | Command | Read from | Result |
|---|---|---|---|
| 1 | `grep -rl "fold-back-ledger" docs/ bootstrap/ templates/`, run inside a clean `git archive bd661fa \| tar -x` export in scratch | the Response's own commit | **17** |
| 2 | `git grep -l "fold-back-ledger" bd661fa -- docs bootstrap templates` | the same commit's tree object | **17** |
| 3 | `git grep -l "fold-back-ledger" HEAD -- docs bootstrap templates` | `4a7d70a` | **17** |

Identical at the Response's commit and at HEAD, so **drift is not the
explanation** -- the figure was wrong when written, not overtaken.

The ten files beyond the seven the amendment names are
`bootstrap/_scaffold/config.py`,
`bootstrap/tests/fixtures/gate_manifest.json`,
`bootstrap/tests/test_fold_back_ledger_module.py`,
`bootstrap/tests/test_foldback_ledger_module.py`,
`bootstrap/tests/test_quickstart_sequence.py`,
`bootstrap/tests/test_reference_scripts.py`,
`templates/skills/_lib/lifecycle.py`,
`templates/core/dev/upstream/README.md`,
`templates/modules/default-on/fold-back-ledger.md`, and
`templates/modules/default-on/foldback_export_scan.md`.

**Where seven probably came from, and why it does not rescue the sentence.**
`grep -rl --include='*.md' "fold-back-ledger" docs/ bootstrap/ templates/` at
`bd661fa` does return exactly **7** -- but a *different* seven: it picks up the
three template documents above and drops the three `bootstrap/profiles/*.yml`
files, which the amendment names explicitly. So no variant of the command as
written yields the listed set. An implementer or the External reviewer who runs
the command in the amendment gets 17 and is right to stop there.

**Verdict on this figure: the audit is correct and the Response is wrong.** My
number is the audit's, arrived at independently and by two methods it did not
use.

**Does amendment 10 still hold? Yes -- it stays in force, with the figure
corrected.** Its conclusion is that the *prose enumeration surface* is complete
once B6 and B7 land; that conclusion does not rest on the grep being exclusive,
it rests on none of the unlisted hits being a default-on roster enumeration. I
checked that myself rather than taking it on report. Seven of the ten are code,
tests, or a fixture. The three that are prose are not roster enumerations:
`templates/core/dev/upstream/README.md:37` names the module as the installer of
the fold-back ledger; `templates/modules/default-on/fold-back-ledger.md` hits
its own title and its own goodnight-step quote; and
`templates/modules/default-on/foldback_export_scan.md` names the ledger module
once as the sibling it ships beside (`:12`) and once in a solo-adopter caveat
(`:164`). None of the three lists the default-on set, so none goes stale when
`content-security` joins it.

Read amendment 10's last sentence as: the command returns **17** files, of
which **7** carry default-on roster enumerations -- `docs/quickstart.md`,
`docs/solo-legacy-recipe.md`, `bootstrap/BOOTSTRAP.md`, the three
`bootstrap/profiles/*.yml`, and `templates/modules/README.md` -- and those 7
are the complete enumeration surface after B6/B7. Do **not** read it as an
exclusivity claim about the grep; the exclusivity claim, and the `[I3]` row's
*"I assert that as a measurement"*, are withdrawn as stated.

#### 2. Amendment **11**'s "four module-selection sites" -- measured, and it is five

The audit raised this as a note, not a defect. It is a number inside an in-force
amendment, so I measured it rather than leaving it.

**What was claimed.** Amendment 11: *"`cli.main` has four module-selection
sites, not three."*

**What I measured: five construction sites**, by reading the two branch
structures in `bootstrap/_scaffold/cli.py` (byte-identical at `bd661fa` and at
`4a7d70a` -- `git diff bd661fa HEAD -- bootstrap/_scaffold/cli.py` is empty).
The `--summary` handler carries two: `:232` (`preset:` present ->
`format_profile_summary`) and the inline fallback at `:236`-`:239`, whose
ternary is itself two cases (`modules:` present, else `_DEFAULT_ON_MODULES`).
The install path carries three: `:330` (`expand_preset`), `:350` (`modules:`
alone), `:356` (neither key -> `_DEFAULT_ON_MODULES`). Counting construction
sites gives **5**; counting branch limbs gives **6**.

**Verdict: the audit's count is right and mine agrees with it.** The Response's
"four" is one low however you slice it.

**Does amendment 11 still hold? Yes -- in force, figure corrected.** Nothing the
amendment instructs depends on the total: it directs that A6 covers the
install-path no-key branch, that the `modules:`-alone branch stays untouched,
and that the `--summary` no-preset fallback gets its own row A7. All three of
those are site-specific and unaffected. Read the sentence as: `cli.main` builds
a module roster at **five** sites, of which this plan touches two (`:239` via
A7, `:356` via A6). The Response's own External brief already flagged that the
`cli.main` enumeration was unproven; this is that proof, and it moves the
number.

#### 3. What this correction does not do

* It does not re-open any disposition. `[I1]`--`[I5]`, the accepted nits and the
  declined `check_cairn.py:100` nit stand as the Response left them.
* It does not change code, tests, fixtures, templates or docs. One file is
  written: this plan.
* It does not touch the amendments the audit reported as reproducing. I did not
  re-run the twenty-plus figures it verified; I re-ran the one it disputed and
  the one it flagged, which is the scope of this section.
* It does not discharge any review tier. The plan still declares
  `required(**External**, security lens)`, and this section -- like the Response
  it corrects -- is the author's own hand and clears nothing.

This section is append-only once written.

## Response to plan review -- Claude (author) -- 2026-08-05

**Model**: Claude Opus 5 (`claude-opus-5`).

**Standing and scope.** I am the plan's author, responding to the **External
(cross-agent-type, security-lens) plan review by Codex dated 2026-08-05**,
committed at `2077a25`. This Response **dispositions findings and amends the
plan**; it discharges **no** review tier. An author's Response is not a review
of any tier, and the External tier is not something its subject can sign off.
See *Gate audit* and *Clearance* — the answer is **NO**.

**Read this before anything else — the `[E#]` labels are overloaded in this
file.** The plan body already cites `[E1]`, `[E2]` and `[E3]` **six times**
(measured, not estimated: lines 46, 85, 101, 430, 552, 744), and every one of
those refers to the **source proposal's** External review, not to the plan
review being answered here — *Source proposal* Change 3 (*"Per [E2] the
**template source stays the executed authority**"*), *The argument this plan is
allowed to make* twice (*"[E1] falsified it with a counterexample"*,
*"Untouched by [E1]"*), Chunk B's B1 cell (*"that is the [E1] adopter"*),
Chunk D's D1 cell (*"[E3] is on record that hand-editing it inverts the
documented workflow"*), and *Author-accounting*'s known omissions (*"the
residual [E1] adopter population"*). The 2026-08-05 plan review reuses the same
three labels for three unrelated findings. **In this Response the plan-review findings are
`[PR-E1]`, `[PR-E2]`, `[PR-E3]`; a bare `[E1]`/`[E2]`/`[E3]` anywhere in this
file continues to mean the proposal's reviewer.** Amendment 43 puts that
convention in the plan so an implementer does not resolve a label to the wrong
finding.

**Where the plan review sits in the file — it is not the last section.** The
External section was **inserted before** the existing Internal review and the
2026-08-04 Response rather than appended at the end. Reading order by date is
therefore: Internal (2026-08-04) → Response + Figure correction (2026-08-04) →
**External (2026-08-05)** → this Response. Anyone re-deriving from "the last
section" reads the wrong round.

**Method.** Every figure below was re-derived at repository HEAD **`b8ab678`**
under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`, CPython
3.13.13) with `PYTHONDONTWRITEBYTECODE=1`. Engine, `scripts/` and `templates/`
are byte-identical between `6bcd2d3` and `b8ab678` (`git diff --stat 6bcd2d3
b8ab678 -- bootstrap/ scripts/ templates/` is empty), so measurements taken
across that window are comparable. The content-scan measurement was taken in a
**`git clone` of this repository into the session scratch directory**, with the
five shipped policy/apparatus files copied verbatim into the clone's `scripts/`
— never in the repository. **No repository file was modified, added, moved,
staged or committed; the only path this Response writes is
`dev/plans/default-security-stance.md`.** `as_of 2026-08-05` at `b8ab678`
throughout unless stated.

**Working-tree provenance for the suite figure**, because the Internal round was
right that a passed-count taken over sibling work is contaminated. The suite run
started and finished with **no tracked file modified** in the working tree
(checked at the start, and confirmed afterwards by mtime: the two sibling edits
present by the end of this session — `bootstrap/tests/test_security_stack.py`
and `templates/modules/team-gated/run_security_audit.py` — were both written
*after* the run completed). The figure is therefore a committed-tree figure, not
a contaminated one.

### The headline: the alarm-fatigue number exists, it can be taken before Chunk D, and it is 52

The Internal round recorded that D3's measurement *"is unmeasured … only Chunk D
can [take it]"*, and my own 2026-08-04 Response repeated that it *"cannot be
taken by any reviewer"*. **Both are false, and I falsified them by taking it.**

Copying the five shipped files (`content_scan.py`, `content_scan_runner.py`, and
the three `content_scan_*.txt` policy files — exactly the set
`--adopt-module content-security` installs under `scripts/`) into a scratch
clone at `b8ab678` and running the runner from the clone root:

```
content_scan runner: scanned 78 audited text file(s) from content_scan_roots.txt
result: 52 flag(s), 52 NEW -- ADVISORY (human-review tripwire, not a gate).
exit 1
```

Run twice, identical both times. Composition, measured rather than characterized:

* **All 52 are `[suspicious-url]`.** Zero homoglyph flags, zero invisible-character
  flags, zero of any other pattern id.
* **They live in five files**: 27 in one `dev/strategy/` document, 17 in another,
  3 in `docs/further-reading.md`, 3 in `dev/plans/api-web-security-modules.md`,
  2 in `dev/plans/dependency-advisory-coverage.md`. The `dev/strategy/` and
  `docs/` hits are academic-publisher, standards-body and research-infrastructure
  citation hosts in bibliographies; the two `dev/plans/` sets are loopback
  addresses and single-letter placeholder hosts inside worked security examples.
* **Nothing failed closed.** Exit 1, not 2 — so D3's claim that *"the three
  REQUIRED roots … all exist in Cairn … so the runner will not fail closed on a
  missing root"* **reproduces**.

Four consequences, each of which lands as an amendment rather than as prose here:

1. **D3's stop trigger fires today, before any implementation.** D3 says *"If the
   count is non-trivial, that is a *Signals the change is wrong* trigger: stop and
   put it to the Maintainer rather than curating it away."* 52 is non-trivial by
   any reading. This is now a Maintainer question, not an implementer judgment,
   and it is a second independent reason this Response does not clear the plan.
2. **Chunk D's stated comparison is inapt and is struck.** *"the External
   reviewer's 34 / 39 / 42-file clean runs are the comparison"* — those were
   **fresh scaffolds**: template prose with no bibliography. Cairn's tree is 78
   audited files including a deliberation record and two strategy documents with
   reference lists. A fresh-scaffold zero does not predict an adopter's number,
   and Cairn — the first adopter — is the counterexample.
3. **The plan's surviving-argument limb 1 needs its scope stated.** *"**The
   measured cost is zero.**"* is true **of a fresh scaffold** and does not
   generalize. I am not withdrawing the limb: the flags are a single tunable
   class with a documented tuning path (the module's own allowlist policy
   distinguishes trusted-publication hosts from multi-tenant hosts, and the
   residual baseline ships an `[editorial-url]` tag for exactly this). But the
   honest statement is "zero on a fresh scaffold; tunable and non-zero on a tree
   that cites literature", and Chunk D must carry that.
4. **D3's residual-only remedy is incomplete.** D3 contemplates only
   `content_scan_residuals.txt`. 52 editorial-citation flags are the case the
   shipped allowlist policy is written for, and the plan's *Out of scope* fence
   already treats the three `.txt` policy files as adopter-tunable by design. The
   allowlist-versus-residual split for these 52 is a **policy decision**, and
   under D3's own rule it is the Maintainer's.

**The post-Chunk-D number will be ≥ 52, not = 52.** `--adopt-module` also writes
`dev/modules/content-security.md` (substituted) **inside the audited `!dev`
root**, and this lifecycle's own `dev/` artifacts are audited too. The number is
a floor measured on a tree that does not yet contain the installed doc.

### Three in-force figures moved again, and one in-force *criterion* is unsound

Reported as plainly as the reproductions.

1. **Suite: 1959, not 1790.** `python -m pytest bootstrap/tests` at `b8ab678` →
   **1959 passed, 0 failed, 0 skipped**, 296.63s. Amendment 5 pinned **1790** at
   `6618e54` one day ago and instructed a re-take; the collection grew by **169
   nodes in a day**. This is the *third* suite frame in three days (1744 → 1790 →
   1959). Amendment 40 restates the criterion as an invariant with a re-measure
   instruction, and keeps a dated number only as provenance.
2. **`scan_targets()` returns 76 *today*, before Chunk D.** The plan says 74
   before and 76 after; the Internal round confirmed 74; my own 2026-08-04
   Response confirmed 74 at `6618e54`. At `b8ab678` it is **76**, and the two
   additions are attributable: `scripts/transition_lint.py` and
   `scripts/transition_lint_whitelist.py`, added by the `transition-lint` scope
   (`4a7d70a`, 2026-08-04). **Chunk D's acceptance criterion `PASS, target count
   76 (from 74)` is therefore satisfiable by doing nothing** — the gate has
   already been walked past its own expected value. Expected after Chunk D:
   **78**, re-measured immediately before the chunk. Amendments 37–39.
3. **`check_cairn.py`'s scanned count went *down*, and the criterion that says it
   cannot is unsound by construction.** At `b8ab678`: `OK -- 176 Markdown file(s)
   scanned; no issues; 48 external link(s) not probed`. Amendment 8 pinned **195**
   and 68, and asserts *"the assertion is `OK` and a **non-decreasing count**"*.
   **176 < 195.** The mechanism is not drift, it is design:
   `check_cairn.main` collects `git ls-files '*.md'` and passes it through
   `link_check.filter_sources` (`scripts/link_check.py:503`), which drops
   `dev/**/archive/`, `dev/modules/`, `dev/.cairn/` and `dev/reflections/`.
   Measured: **255** tracked Markdown files, **176** after the filter. **Archiving
   a plan or proposal removes it from the scanned set**, so the count falls every
   time this repository does the thing its lifecycle exists to do. A
   non-decreasing-count gate would fire on a correct archive. Amendment 41
   replaces it with a membership assertion, which is what Chunk D actually needs.

None of the three changes a disposition. All three are the same failure the
2026-08-04 Response's *Clearance* item 4 raised and the External round did not
address: **a count asserted without a mechanism is stale on arrival in a
nine-scope repository.** Three more instances in one day is enough evidence to
stop asserting counts where an invariant will do, and amendments 40–42 do that
rather than substituting today's numbers.

### Disposition of every finding

`[PR-E1]`–`[PR-E3]` are the 2026-08-05 External review's findings (see the
notation warning above).

| # | Disposition | Reasoning | Mechanical residue |
|---|---|---|---|
| **[PR-E1]** — default adoption is not gated on the scanner's unresolved security posture | **ACCEPT WITH MODIFICATION** — the *instruction* is accepted unmodified; the modification is to the finding's premise and to how each limb is made checkable | **The instruction is right and I am adopting it whole**: a default-on flip that reaches every new adopter must not overtake the security evidence for the thing being defaulted. It is also **independently demanded from the other side**: the sibling plan's own External review (`b80bcd0`, 2026-08-05 07:58 — **two minutes before this one**) says in its [E3] *"a default-security implementation must be prohibited from selecting this module until that decision has a recorded disposition and a corpus appropriate to default adoption. State that cross-plan gate in both plans."* And `dev/plans/content-scan-detectors.md:1128` already routes the whole-script-Cyrillic cost as *"Sequenced against `default-security-stance`, not against this plan"* — so the sibling has been pointing at this plan for the gate, and this plan has been silent. **Premise correction, measured**: the finding says the sibling *"lacks an External security disposition on its test material"*. `dev/plans/content-scan-detectors.md:1138` **does** carry `## Plan review -- Codex (External, security lens) -- 2026-08-05`, landed before this review was written. What is missing is the **disposition**: that plan's newest section is dated 2026-08-04, so its External [E1] on the test-material fixture set is undispositioned. Under the "disposition" reading the finding is exactly right; under a "no External review exists" reading it is not. The gate below is written against the reading that measures true. **Also measured, and it cuts in the plan's favour**: none of Cairn's own 52 flags is a homoglyph or invisible-character flag, so the detectors under dispute contribute **zero** of Cairn's current noise — the gate is about the adopter population, not about Cairn's own measurement. | Amendments **30**, **31**, **32**; migration row **10** (amendment 44) |
| **[PR-E2]** — the `known_new` choice must be decided before, not during, the ceremony | **ACCEPT** | The finding closes [R4], which my 2026-08-04 Response left routed to the Maintainer, and it closes it in the direction the code supports. Re-derived at `b8ab678`, three ways: (i) `verify` is `def verify(baseline_path, module_paths)` (`bootstrap/tests/_ast_attest.py:204`) — two parameters, no `known_new`; (ii) `known_new` is a keyword parameter of `update_symbol` (`bootstrap/tests/_ast_attest.py:230`) and is supplied only by the `--known-new` flag on the update-symbol subparser; (iii) **the decisive one, which neither round had run**: `verify` at HEAD emits **78** `note: NEW …` lines — **45** of them non-`Import:` / non-`Docstring` — and **still returns rc 0** (`AST attestation OK — 173 baselined symbol(s) accounted for, unchanged`). An unpinned NEW key is a *note*, not a failure. So the 45 standing unpinned NEW symbols survived the Maintainer-run **Ceremony 1** re-anchor untouched, and this scope's two would join them on identical terms. **Asking the Maintainer to decide a pin that no consumer reads, while performing a trust-root ceremony, is exactly the pressured-operator-judgment failure the finding names.** The archived `ast-known-new-repin` plan reached the same conclusion independently by reading the signature (`dev/plans/archive/ast-known-new-repin.md:248`). | Amendment **36** (supersedes amendment 26, which superseded Chunk R item 3) |
| **[PR-E3]** — the alarm-fatigue stop needs a measurable escalation threshold | **ACCEPT WITH MODIFICATION** | The finding is correct that *"non-trivial"* is not a decision rule and that a default-on scanner cannot rely on an implementer to intuit when warning volume is material. **Modified on two points, both because I took the measurement the finding asks for instead of instructing the implementer to take it.** (a) The finding offers *"any count above the independently recorded baseline"* as one option — there was no independently recorded baseline for Cairn's tree, so I recorded one: **52 flags / 52 NEW / exit 1 over 78 audited files at `b8ab678`**, taken in a scratch clone, which satisfies the "measured from a committed tree, not from the artifact under verification" discipline by construction. (b) That measurement makes the *simpler* of the finding's two suggested rules the correct one and the baseline-comparison rule the wrong one: the shipped residual baseline is empty by design (sentinel line only), so **every** flag is NEW and the rule collapses to **exit code 0 or HOLD**. The threshold is therefore mechanical with no count in it at all: `content_scan_runner.py` exit 0 → proceed; any non-zero → HOLD. Curation of the 52 — allowlist entries versus reviewed residuals — is routed to the Maintainer, per D3's own trigger, and is explicitly **not** an implementer decision. | Amendments **33**, **34**, **35**; migration row **11** (amendment 44) |
| *Framing* — *"I also agree with the later correction that selection has five construction sites, not four"* | **CONFIRMED, no residue needed** | Re-derived rather than inherited, by reading both branch structures in `bootstrap/_scaffold/cli.py` at `b8ab678`: `--summary` carries `:232` (preset → `format_profile_summary`) and the inline fallback at `:236`–`:239` (a ternary, two limbs); the install path carries `:330` (`expand_preset`), `:350` (`modules:` alone) and `:356` (neither key → `_DEFAULT_ON_MODULES`). **Five construction sites, six branch limbs.** The figure correction of 2026-08-04 stands. | None |

### Findings I am adding on my own re-measurement

* **[S1] The D3 measurement was reachable all along.** Recorded above as the
  headline. Two rounds asserted it could only be taken by Chunk D; a clone plus
  five `cp`s takes it. The general lesson is the one this repository keeps
  paying for: *"structurally deferred to implementation"* deserves one attempt
  at falsification before it is written down.
* **[S2] `scan_targets()` is 76 before Chunk D**, so Chunk D's Bandit criterion
  is already satisfied by an unrelated scope's work. A gate that passes without
  the change it gates is worse than no gate. Amendments 37–39.
* **[S3] `check_cairn.py`'s count is non-monotone by construction.** Amendment
  8's non-decreasing criterion cannot hold in a repository that archives.
  Amendments 41–42.
* **[S4] The suite figure moved 169 nodes in a day.** Third frame in three days.
  Amendment 40.
* **[S5] The `[E#]` label collision.** **Six** live citations in the plan body
  (lines 46, 85, 101, 430, 552, 744) use `[E1]`/`[E2]`/`[E3]` for the
  *proposal's* reviewer; the plan review reuses all three. Amendment 43.
* **[S6] The plan's own gate sentence understates the doctrine gate, and the
  mechanical check is weaker than both.** `doctrine/plans.md:114`–`:117` states
  the plan-review precondition as: a review-required plan reaches `executing`
  *"only after a dated `## Plan review` section lands: the review **and**, when
  it raised findings, a dated `### Sharpening` subsection dispositioning them"*.
  The plan header says only *"No implementation commit lands before the `##
  Plan review` section is in the tree"* — one limb of two. And the mechanical
  helper is weaker still: `templates/skills/_lib/lifecycle_planner.py:865` gates
  the `open → executing` transition on `_has_kind(art, "Plan review")`, which is
  a **section-name prefix test** (`:697`–`:698`) — it checks that a section
  whose kind starts with "Plan review" exists, and checks **nothing** about a
  Sharpening subsection or about whether findings were dispositioned. Following
  the AGENTS.md rule to open a named trigger rather than trust it: the trigger
  exists, and it verifies presence, not disposition. Two further observations,
  reported rather than repaired because repairing either would require editing a
  prior section: **(a)** the plan's `**Status**` field reads `open` and never
  moved to `awaiting-plan-review`, which is the status doctrine assigns a
  review-required plan between opening and review; **(b)** doctrine's named
  disposition vehicle is a `### Sharpening` subsection **with the chunk-table
  cells edited inline** (*"Chunk-table cells are edited inline when sharpening
  accepts a finding"*), whereas this plan and its cluster siblings use an
  append-only `## Response` section with an amendments table. The amendments
  table is this plan's only mutation channel and every row supersedes a verbatim
  span, but an implementer must be told to read the chunk tables *through* the
  amendments — see *Reading order* below. Both belong to the Maintainer, not to
  an author's Response.
* **[S7] The cross-plan gate has no mechanical enforcement, and I am saying so
  rather than implying one.** Nothing in `bootstrap/tests`, no git hook, and no
  CI (Cairn has none) can check that `content-scan-detectors` has a recorded
  disposition before this plan's Chunk A lands. Its trigger is **a human reading
  the plan header and the Sequence block** — that is what amendments 30 and 31
  put those lines there for, and the honest description of the check is "a
  person reads it", not "a gate enforces it".

### Review claims I re-ran and confirmed exactly

Each was **run** at `b8ab678`, not read:

1. **`verify` never consumes `known_new`, and an unpinned NEW key is not a
   failure.** Signature `verify(baseline_path, module_paths)` at
   `bootstrap/tests/_ast_attest.py:204`; `known_new` is `update_symbol`'s keyword
   parameter at `:230`. Live run: rc **0**, `173 baselined symbol(s) accounted
   for, unchanged`, with **78** NEW notes of which **45** are
   non-`Import:` / non-`Docstring`.
2. **The AST baseline composition — amendment 3 reproduces exactly.** 173
   entries; **161** of the three kinds (**98** `FunctionDef:` / **53** `Assign:` /
   **10** `ClassDef:`); **12** exempt (8 `Import:`, 1 `Docstring`, 1 `Expr`, 2
   `If`-prefixed). No `Try:` key.
3. **The `DUPLICATE` pre-check.** Neither `_TOKEN_GATED_MODULES` nor
   `token_gated_modules` collides with any of the 161 baselined three-kind names.
4. **The install contract does not move.** `scaffold.py --manifest` → **96**
   lines.
5. **Lockfile accounting — exact.** **81** files, **14** modules, **41**
   `scripts/` + `tools/` `.py` records.
6. **`scaffold_ast_known_new.json` holds 28 keys**, all named-symbol type.
7. **Every load-bearing line citation resolves.** `bootstrap/_scaffold/cli.py:236`–`:239`
   is the `mods = … else list(_DEFAULT_ON_MODULES)` ternary and `:356` is the
   install-path no-key branch; `bootstrap/tests/test_presets.py:415` is
   `assert len(modules) == 8`; `scripts/check_cairn.py:84` / `:91` / `:100` are
   the three `_SRC` assignments, so the declined nit stays declined.
8. **D3's REQUIRED-roots claim.** The runner scanned 78 files and exited 1, not
   2 — the three REQUIRED roots resolve and contribute.
9. **The sibling plan's External round exists and asks for the same gate.**
   `dev/plans/content-scan-detectors.md:1138`, committed `b80bcd0` at
   2026-08-05 07:58; this plan's External review is `2077a25` at 08:00.

### Amendments in force

Continuing the numbering of the 2026-08-04 Response (rows 1–29). Every row
supersedes the quoted text **verbatim**, with the plan's line wrapping
normalized to single spaces; each quote was verified by whitespace-normalized
substring match against the plan file before commit. Where a superseded span is
a chunk-table row, its cell separators appear as `\|` so this table renders; the
*words* are verbatim.

**Reading order for the implementer.** The chunk tables and acceptance criteria
are **superseded by** amendments 1–44; read the chunk through its amendments,
never alone. Three rows are amended twice — where that happens the **later row
wins**: Chunk R item 3 (row 26 → **row 36**), the suite baseline (row 5 →
**row 40**), and the prose-integrity criterion (row 8 → **row 41**).

| # | Superseded text (verbatim) | Replaced by |
|---|---|---|
| **30** | *"**No implementation commit lands before the `## Plan review` section is in the tree.**"* | **No implementation commit lands before all three of the following hold.** (i) A dated `## Plan review` section is in the tree — **satisfied**, `2077a25`. (ii) The findings it raised are dispositioned in a dated section — `doctrine/plans.md:114`–`:117` makes the disposition the *second limb* of the plan-review precondition, and the mechanical helper (`templates/skills/_lib/lifecycle_planner.py:865`) checks only the first, so this limb is carried by a human reader. (iii) **The cross-plan gate below is satisfied.** The verdict on the External round is **REVISE**; whether the amended shape needs a round-2 External section before implementation is the **Maintainer's** call, and an author's Response never makes it. |
| **31** | *"(plan review) -- required(External, security lens); NO code before it lands"* *(the Sequence block's second line, quoted without its leading indentation)* | `(plan review) -- required(External, security lens); NO code before it lands` <br> `(cross-plan gate) -- G1 + G2 below; NO Chunk A, NO Chunk D before both hold` <br> The two gate lines are the implementer's stop sign, and the *only* trigger either has is a person reading them (**[S7]**) — no test, hook or CI enforces them, and Cairn has no CI. |
| **32** | *(insertion, no superseded text — a new subsection at the end of* The cluster constraint*)* | **### The cross-plan gate ([PR-E1])** — **Neither Chunk A nor Chunk D may land until G1 and G2 both hold.** Chunk A is fenced as well as Chunk D because A1 is the default-on flip itself; the token-gate half (A2–A7) could in principle be split out and landed early, and I considered that and **declined it** — a half-landed engine change parked in a five-scope `config.py` window is a new hazard, and narrowing a gate an External reviewer set is the author's least defensible move. The Maintainer may narrow it; the author does not. <br> **G1 — the sibling scope has its required External security review.** Checked by: `dev/plans/content-scan-detectors.md` carries a dated `## Plan review -- … (External, security lens)` section. **SATISFIED**, measured `as_of 2026-08-05` at `b8ab678`: the section is at `:1138`, committed `b80bcd0`. <br> **G2 — the default-on consequence has a recorded disposition.** Checked by **both**: (i) `dev/plans/content-scan-detectors.md` carries an author disposition of its own 2026-08-05 External findings — a section dated **after** 2026-08-05 that dispositions them; **and** (ii) the Maintainer has recorded a Decision or an explicit direction on the whole-script-Cyrillic and international-proper-noun cost **under default adoption** — the question that plan's own *Known omissions* (e) raises and does not answer, and that its migration table routes to *"a new proposal … Sequenced against `default-security-stance`"*. **NOT SATISFIED**, measured `as_of 2026-08-05` at `b8ab678`: the sibling plan's newest section is dated 2026-08-04. <br> **The sibling side of the gate is not this plan's to write.** That plan's own External [E3] asks for the gate to be *"state[d] … in both plans"*; this amendment is this plan's half. The other half is an obligation on that plan's author, recorded as migration row 10 so it is not lost. |
| **33** | *"\| D3 \| `scripts/content_scan_residuals.txt` \| Run `python scripts/content_scan_runner.py` once over Cairn's tree and **record the flag count in the commit body**. The three REQUIRED roots (`AGENTS.md`, `.agents/skills`, `dev`) all exist in Cairn — verified `as_of 2026-08-04` — so the runner will not fail closed on a missing root. If flags appear, each residual added carries its own reviewed rationale; a blanket suppression is the alarm-fatigue failure the proposal names and is not acceptable here. **If the count is non-trivial, that is a *Signals the change is wrong* trigger: stop and put it to the Maintainer rather than curating it away.** \|"* | **D3 — the measurement, and a threshold with no judgment in it.** Run `python scripts/content_scan_runner.py` once over Cairn's tree and **record the exit code and the flag count in the commit body**. The three REQUIRED roots (`AGENTS.md`, `.agents/skills`, `dev`) all exist in Cairn — **re-verified `as_of 2026-08-05` at `b8ab678` by running the scanner, which scanned 78 files and exited 1 rather than failing closed at 2**. <br> **The decision rule, and the implementer applies no other:** **exit 0 → proceed. Any non-zero exit → HOLD and put it to the Maintainer.** No count appears in the rule, because the shipped `content_scan_residuals.txt` is a sentinel-only empty baseline, so every flag is NEW and "any unsuppressed finding" and "exit non-zero" are the same condition. <br> **The pre-measured baseline this compares against.** In a scratch `git clone` at `b8ab678`, with the five shipped files copied verbatim into `scripts/`: **78 audited files, 52 flags, 52 NEW, exit 1**, all 52 `[suspicious-url]`, in five files. **So the HOLD is already triggered as of this Response** — Chunk D will not exit 0 on a clean adoption, and the implementer is not the one who decides what to do about it. <br> **The implementer adds no residual and no allowlist entry.** Whether these 52 editorial-citation hits are cleared by trusted-publication entries in `content_scan_allowlist.txt`, by reviewed `[editorial-url]` residual entries, or by neither, is a **policy decision under D3's own escalation trigger and it is the Maintainer's**. A blanket suppression remains the alarm-fatigue failure the proposal names and is not acceptable at any volume. <br> **Expect ≥ 52, not = 52**: `--adopt-module` writes `dev/modules/content-security.md` inside the audited `!dev` root, and this lifecycle's own `dev/` artifacts are audited too. |
| **34** | *"* **The content-scan measurement is recorded, not just passed.** The flag count from D3 goes in the commit body as a number, even when it is zero — that number is this plan's alarm-fatigue budget and the External reviewer's 34 / 39 / 42-file clean runs are the comparison."* | **The content-scan measurement is recorded, and the exit code is the gate.** The exit code **and** the flag count from D3 go in the commit body, even when the count is zero. **The comparison is the pre-measured Cairn baseline in D3 — 78 audited files / 52 flags / exit 1 at `b8ab678` — not the proposal reviewer's 34 / 39 / 42-file clean runs**, which were taken on fresh scaffolds with no bibliography and do not predict a tree that cites literature. **Acceptance is `exit 0`; any non-zero exit is a HOLD to the Maintainer**, not a number for the implementer to weigh. |
| **35** | *"* **The content-scan measurement** — `python scripts/content_scan_runner.py` on Cairn's tree after Chunk D; the flag count recorded as a number in the commit body."* | **The content-scan measurement** — `python scripts/content_scan_runner.py` on Cairn's tree after Chunk D. **Exit 0 → pass; any non-zero exit → HOLD to the Maintainer.** The exit code and the flag count are both recorded in the commit body, against the pre-measured baseline in D3 (78 files / 52 flags / exit 1 at `b8ab678`). |
| **36** | *"**3. The `known_new` manifest — declared, but its necessity is an open Maintainer question.** The two NEW keys are `Assign:_TOKEN_GATED_MODULES` and `FunctionDef:token_gated_modules`; their **key set** is declared in advance and their digests cannot be. **Whether they need pins in `bootstrap/tests/fixtures/scaffold_ast_known_new.json` is unresolved**: `known_new` is read **only** by `update_symbol` (`bootstrap/tests/_ast_attest.py:230`) and never by `verify`, and this plan establishes on two independent grounds that `update-symbol` is unavailable to this scope. Either the pins are unnecessary here, or the ceremony mechanism is not the direct-correction script this plan names. **The Maintainer decides at ceremony time**; the implementing agent declares the key set and stops."* *(amendment 26's replacement text, itself superseding Chunk R item 3)* | **3. The `known_new` manifest — decided now, and the decision is: do not touch it.** **This scope does not edit, re-pin, or add entries to `bootstrap/tests/fixtures/scaffold_ast_known_new.json`.** Settled ahead of the ceremony rather than during it, per [PR-E2], on measured grounds: `verify` is `verify(baseline_path, module_paths)` (`bootstrap/tests/_ast_attest.py:204`) and never reads the manifest; `known_new` is `update_symbol`'s keyword parameter (`:230`), and `update-symbol` is unavailable to this scope on two independent grounds already established; and — decisively — `verify` at `b8ab678` emits **78 `note: NEW` keys, 45 of them non-`Import:` / non-`Docstring`, and still returns rc 0**, so an unpinned NEW symbol is a note and not a failure. Those 45 survived Ceremony 1 unpinned; this scope's two join them on identical terms. <br> **What the implementing agent does instead:** declare the **exact NEW-key set — `Assign:_TOKEN_GATED_MODULES` and `FunctionDef:token_gated_modules`, and nothing else** — and stop. **Any third NEW non-`Import:` / non-`Docstring` key attributable to this scope, established as the set difference of amendment 14, STOPS THE CEREMONY.** No digest is pre-declared, because none is needed. |
| **37** | *"* **The release Bandit gate** — `scan_targets()` returns **74** targets, `as_of 2026-08-04`. After Chunk D it returns **76**: Cairn's own `scripts/*.py` glob picks up `scripts/content_scan.py` and `scripts/content_scan_runner.py`, whose template twins were already in the manifest-derived set. Both new targets are byte-identical to files Bandit already reads, so the severity histogram must not gain a MEDIUM+."* | **The release Bandit gate** — `scan_targets()` returns **76** targets `as_of 2026-08-05` at `b8ab678`, **not the 74 this plan and both prior rounds recorded**: `scripts/transition_lint.py` and `scripts/transition_lint_whitelist.py` were added by the `transition-lint` scope at `4a7d70a`. **Re-measure immediately before Chunk D and assert the delta, never the absolute**: Cairn's `scripts/*.py` glob picks up `scripts/content_scan.py` and `scripts/content_scan_runner.py`, so the assertion is **exactly +2 targets, and the two new paths are those two**. Expected **78** if the base is still 76. Both new targets are byte-identical to files Bandit already reads, so the severity histogram must not gain a MEDIUM+. |
| **38** | *"* `~/conda_envs/lhm/bin/python3.13 bootstrap/security_check.py` → `PASS`, target count **76** (from 74). Both new targets are byte-identical to template files Bandit already reads, so the severity histogram gains **no MEDIUM+**; a MEDIUM+ appearing is a stop."* | `~/conda_envs/lhm/bin/python3.13 bootstrap/security_check.py` → `PASS`, with **the target count exactly +2 against a pre-chunk measurement taken in the same session**, and the two added paths identified as `scripts/content_scan.py` and `scripts/content_scan_runner.py`. **The literal "76 (from 74)" is struck**: the base is already **76** at `b8ab678`, so the old criterion is satisfied by an unrelated scope's work and gates nothing (**[S2]**). Both new targets are byte-identical to template files Bandit already reads, so the severity histogram gains **no MEDIUM+**; a MEDIUM+ appearing is a stop. |
| **39** | *"* **The release Bandit gate** — `python bootstrap/security_check.py` → `PASS`, 74 targets before Chunk D and 76 after, with no MEDIUM+ appearing."* | **The release Bandit gate** — `python bootstrap/security_check.py` → `PASS`, **target count +2 across Chunk D against a same-session pre-chunk measurement** (base **76** at `b8ab678`; the absolute is not pinned), the two added paths named, and no MEDIUM+ appearing. |
| **40** | *"**Suite baseline: 1790 passed / 0 failed / 0 skipped**, 186.73s, `as_of 2026-08-04` at `6618e54`. Collection may only grow by this plan's new nodes; a dropped node or a new skip/xfail marker is a HOLD class. **Re-take this figure at implementation** — it moved by 46 nodes in the day between plan-open and this Response."* *(amendment 5's replacement text)* | **The suite criterion is an invariant; the number is provenance only.** Invariant: **0 failed / 0 skipped / 0 xfailed**, and **collection grows by exactly this plan's new nodes and drops none**, established by a same-session before/after pair — never against a figure quoted from this file. Provenance: **1959 passed / 0 failed / 0 skipped**, 296.63s, `as_of 2026-08-05` at `b8ab678`. The frame has now moved three times in three days (**1744 → 1790 → 1959**, the last a 169-node jump), which is why the criterion is the delta and not the count. |
| **41** | *"**Prose integrity** — `python scripts/check_cairn.py` → `OK`, `as_of 2026-08-04` at `6618e54` the count read **195** Markdown files and 68 unprobed external links. **The assertion is `OK` and a non-decreasing count, not a literal figure**: this repository adds Markdown daily (180 → 195 in one day), so a pinned count is stale on arrival. Chunk D must grow it by at least one (`dev/modules/content-security.md`)."* *(amendment 8's replacement text)* | **Prose integrity** — `python scripts/check_cairn.py` → **`OK`, and `dev/modules/content-security.md` is in the scanned set after Chunk D**. **The "non-decreasing count" criterion is withdrawn as unsound.** `check_cairn.main` filters `git ls-files '*.md'` through `link_check.filter_sources` (`scripts/link_check.py:503`), which drops `dev/**/archive/`, `dev/modules/`, `dev/.cairn/` and `dev/reflections/` — **so archiving a plan or proposal *decreases* the count, and a non-decreasing gate would fire on a correct archive**. Measured at `b8ab678`: **255** tracked Markdown files, **176** after the filter, and `OK -- 176 Markdown file(s) scanned; no issues; 48 external link(s) not probed` — **down from the 195 / 68 this amendment previously asserted**. Note the interaction: `dev/modules/` is *excluded* from `check_cairn`'s scan set, so Chunk D's installed module doc is scanned by `content_scan_runner.py` (whose `!dev` root has no such exclusion) but **not** by `check_cairn`. Assert `OK`, and assert membership where membership is what matters — never a count, never a direction. |
| **42** | *"* `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → OK, count +1 for `dev/modules/content-security.md`."* | `~/conda_envs/lhm/bin/python3.13 scripts/check_cairn.py` → **OK**. **The "+1" is struck**: `dev/modules/` is excluded from `check_cairn`'s scan set by `link_check.filter_sources`, so the installed module doc does **not** raise that count at all, and concurrent archiving can lower it (amendment 41). The assertion is `OK` and no new flags. |
| **43** | *(insertion, no superseded text — a notation note, to be read wherever a bracketed `[E#]` label appears)* | **Notation — `[E#]` is overloaded in this file, and the two populations must not be confused.** **Bare `[E1]` / `[E2]` / `[E3]` in the plan body always mean the *source proposal's* External reviewer** — **six** live citations, at lines 46 (*Source proposal*, Change 3), 85 and 101 (*The argument this plan is allowed to make*), 430 (Chunk B, B1), 552 (Chunk D, D1) and 744 (*Author-accounting*, known omissions). **The 2026-08-05 plan review's findings are cited as `[PR-E1]` / `[PR-E2]` / `[PR-E3]`** throughout the 2026-08-05 Response and this amendments table. The Internal round's findings keep `[I1]`–`[I5]`, and that Response's own additions keep `[R1]`–`[R5]`; this Response's additions are `[S1]`–`[S7]`. |
| **44** | *(insertion, no superseded text — two rows appended to* Lasting-truth migration*)* | **Row 10 — the sibling half of the cross-plan gate.** `content-scan-detectors`'s own External [E3] requires the gate to be stated *"in both plans"*; amendment 32 is this plan's half, and the other half is an obligation on that plan's author, which this plan cannot discharge and must not silently assume. Durable home: `dev/PLANNING.md > Deferred follow-ups`, added at the archive / goodnight serialization point, naming both stems. **Row 11 — Cairn's 52 editorial-citation flags.** The allowlist-versus-reviewed-residual policy for the `[suspicious-url]` hits in `dev/strategy/`, `docs/further-reading.md` and two `dev/plans/` files is a Maintainer decision under D3's escalation trigger, and it outlives this plan whether or not Chunk D lands. Durable home: `dev/PLANNING.md > Deferred follow-ups` if the Maintainer defers it; the Chunk D commit body and this plan's archive record if it is settled inside this lifecycle. |

### Gate audit — every gate this plan declares, and whether it holds today

Measured `as_of 2026-08-05` at `b8ab678`. This repository breached two declared
gates yesterday because nobody enumerated them, so they are enumerated.

| Gate | Declared where | What it requires | Holds today? |
|---|---|---|---|
| **Review tier** | Plan header; *Plan review — the brief* | `required(**External**, security lens)`; *"An Internal round does not discharge it"* | **Section present, tier NOT discharged.** The External section is in the tree (`2077a25`) and its verdict is **REVISE**. This Response is the author's disposition; an author's Response discharges nothing. Whether the amended shape needs a round-2 External section is the Maintainer's call. |
| **Implementation fence (plan's wording)** | Plan header; *Plan review — the brief* | *"No implementation commit lands before the `## Plan review` section is in the tree"* | **Satisfied literally** — and it understates the doctrine gate; superseded by amendment 30. |
| **Implementation fence (doctrine)** | `doctrine/plans.md:114`–`:117` | `## Plan review` **plus** a dated disposition of its findings; status `awaiting-plan-review` → `executing`; plan-open and first-implementation commits distinct | **Partly.** Limb 1 satisfied; limb 2 is this Response (form differs from doctrine's inline `### Sharpening` — **[S6]**). The plan's `**Status**` still reads `open` and never moved to `awaiting-plan-review`. The mechanical helper checks limb 1 only. |
| **Cross-plan gate G1** | Amendment 32 (new) | sibling scope carries its External security review | **SATISFIED** — `dev/plans/content-scan-detectors.md:1138`, `b80bcd0`. |
| **Cross-plan gate G2** | Amendment 32 (new) | recorded disposition of the default-on consequence | **NOT SATISFIED** — the sibling plan's newest section is dated 2026-08-04; no Maintainer disposition of the default-adoption cost exists. **This alone blocks Chunk A and Chunk D.** |
| **D3 alarm-fatigue stop** | Chunk D, D3 | non-trivial flag count → stop, put it to the Maintainer | **FIRING NOW.** 52 flags / exit 1 measured before implementation. Under amendment 33 the rule is exit-code-based and the HOLD is already triggered. |
| **Chunk R Maintainer fence** | *Sequence*; Chunk R | *"An implementing agent does not enter this chunk"*; work ends at Chunk D plus a stated readiness condition | **Not yet reached**, and unbreached. Amendment 36 removes the one open ceremony-design question ([R4]) that would otherwise have landed on the operator mid-ceremony. |
| **Decision condition** | Plan header; *Source proposal* | executes the **Decision**, not the proposal body; the withdrawn tautology argument must not be restated; `scripts/check_cairn.py` carries zero bytes of change | **In force, untested** — no implementation exists. Nothing in this Response restates the tautology, and no source file was touched. |
| **Serialized shared files** | *Scope > Serialized shared files* | no chunk edits `CHANGELOG.md`, `dev/PLANNING.md`, `AGENTS.md`, `docs/DOCUMENTATION_PLAN.md`, `bootstrap/REANCHOR_RUNBOOK.md` | **Satisfied.** This Response writes one path: this plan. |
| **Archive precondition** | *Lasting-truth migration* | every deferred follow-up has a durable home before archive | **Pre-declared and current** — rows 1–9 plus rows 10 and 11 (amendment 44). |

### Clearance

**This Response does NOT clear the plan to implement.** Three independent
blockers, none of which an author can clear:

1. **The External round returned REVISE, and no author Response discharges an
   External tier.** The tier is `required(**External**, security lens)`; the
   tree holds one External section, dated 2026-08-05, whose verdict is REVISE.
   This Response is the disposition doctrine's plan-review precondition asks
   for, authored by the plan's author. Whether the amended shape requires a
   round-2 External section before Chunk A is the **Maintainer's** decision, and
   I am not treating silence as a yes.
2. **Cross-plan gate G2 is unmet, by this Response's own new amendment.**
   Accepting [PR-E1] means Chunk A and Chunk D are fenced until the default-on
   consequence has a recorded disposition. It does not today. Two External
   reviewers, on two plans, two minutes apart, asked for the same gate from
   opposite sides; it would be a poor answer to write the gate and then step
   over it.
3. **D3's own stop trigger is already firing.** Cairn's tree produces **52
   flags, exit 1** under the module this plan would make default-on. Under D3 —
   unamended and amended alike — that is a Maintainer question, not an
   implementer's. It is also the first hard evidence that the "measured cost is
   zero" limb does not survive contact with a tree that cites literature, and
   the Maintainer should see that before the flip, not after.

**What is *not* blocking, stated so the Maintainer sees a real cost of delay.**
The engine design survived direct falsification three times now — the symbol
delta, A4's placement / C1g, and C2's discriminating perturbation all reproduced
exactly across two rounds and two independent re-derivations, and this round
adds nothing against them. [PR-E2] is closed rather than deferred. The plan's
executable contract is in better shape than it has been. What blocks it is
evidence and authority, not design.

**Nothing in this Response changes code.** No source file, test, fixture,
template or doc was modified; the amendments are instructions to Chunks A–D and
to Chunk R, not their execution. The one measurement that touched a working tree
touched a scratch clone.

This section is append-only once written.

## Plan review -- Codex (External) -- 2026-08-05

**Tier**: External
**Findings**: raised

**Verdict: REVISE.** Amendment 36 closes the `known_new` policy decision, and
the exit-zero/proceed versus nonzero/hold contract closes the alarm-threshold
finding without turning the old snapshot count into a threshold. The current
tree has no proposed content-scan runner to remeasure, so the Response is right
to treat its historical figure as provenance rather than present evidence.

Amendment 32 does not match the gate in content-scan-detectors AM25. G1 treats
the presence of an External review section as sufficient even when that review
says REVISE. G2 requires a later author disposition and Maintainer direction,
but omits the paired plan's default-adoption corpus condition. It also orders
sections only by written date, which cannot distinguish multiple sections on
the same day and is editable metadata rather than provenance.

Replace both sides with the same gate: no default-on change until the External
round has no outstanding REVISE, the Maintainer's consequence disposition is
recorded, and the named default-adoption corpus is part of the binding test
contract. Identify the satisfying review/response by section identity or commit
order, not date alone. Until both plans carry that condition, each can appear
ready while its reciprocal remains blocked.

### Sharpening

Keep the gate outcome-based rather than requiring a particular number of
rounds. That lets a focused closure round finish the work without weakening the
requirement that the findings themselves be settled.

### Sharpening — the 2026-08-05 fold pass

**What this is.** The inline, in-place fold that `doctrine/plans.md:202-207`
authorises for a plan at status `open` with no commits in flight, driven by the
2026-08-05 External round's finding and by amendments 1-44, which the two author
Responses bound *by reference* rather than folding. Doctrine requires this
subsection to name which cells changed and why; it does that, and it also names
every amendment row that is **not** folded.

**Authority for the pass, and its limit.** The Maintainer's 2026-08-05 instruction
(quoted verbatim in *Maintainer disposition of the 2026-08-05 External review
round*) disposes of the REVISE **round** and authorises revision-then-
implementation. It supplies no credential, no ceremony, no push approval, and **no
disposition of the default-on consequence** — so Gate D-ON stays closed. No
`## Plan review`, `## Response to plan review`, `## Lasting-truth migration` or
`Sharpening` section was edited.

**Reciprocity.** This file and `dev/plans/content-scan-detectors.md` land in **one
commit**, because the shared *Gate D-ON* block requires it in terms: *"A change to
it lands in both files in the same commit, or it has not landed."* The block is
byte-identical in the two files, spliced from a single source rather than retyped.

#### Cells changed, and why

| cell / region | change | why |
|---|---|---|
| header, *Plan review* line | one-limb fence → the three-limb fence, naming Gate D-ON and the disposition | amendment 30; the old wording is satisfied by a section's mere presence |
| *(new)* `## Folded, not amended` | reading rule + the `[E#]` notation note | the External round's diagnosis (two grammars); amendment 43 |
| *(new)* `## Maintainer disposition of the 2026-08-05 External review round` | records the disposition verbatim and visually isolated; enumerates what it does **not** supply, including that Gate D-ON stays closed | the plan's fence names the Maintainer as a disposing party; the scribing guard-rail requires the verbatim quote |
| *The cluster constraint*, new `### Gate D-ON` | the shared block, **verbatim**, plus four plan-local application notes and the discharge of the reciprocal obligation | the External finding — the gate was one-sided. **Supersedes amendment 32's `G1`/`G2` entirely** |
| *Gate accounting*, suite bullet | `1744 passed / 2 failed` → invariant-plus-provenance, re-measured to **1987** | amendment 40; the frame moved four times in three days |
| *Gate accounting*, prose-integrity bullet | 180 / 68 → **178 / 48 / 2 issues**; "non-decreasing count" withdrawn as unsound | amendment 41, re-measured |
| *Gate accounting*, Bandit bullet | "74 → 76" → **assert +2 against a same-session base** (base 76 today) | amendment 37, re-measured |
| *Gate accounting*, lockfile bullet | figures re-measured and marked re-derive-at-implementation | discipline: measure or delete |
| *Sequence* block | adds the D-ON gate line, fences A/B/C/D, and names the only trigger (a person reading it) | amendment 31; Cairn has no CI |
| Chunk **A**, **B**, **C**, **D** headings | each gains an explicit `FENCED BY GATE D-ON` block quote | amendment 32 fenced A and D by reference; B and C are fenced *in fact* because their content asserts A1's behaviour, and that was unstated |
| Chunk D row **D3** | prose "non-trivial" threshold → **exit-code rule**, with the baseline re-measured at **80 files / 52 flags / exit 1** and the HOLD declared already-firing | amendment 33, re-measured |
| Chunk D acceptance, Bandit + `check_cairn` + content-scan bullets | absolutes struck; delta and exit-code criteria substituted | amendments 34, 38, 42 |
| Chunk R item **3** | `known_new` pins required → **do not touch `known_new`**, with the NEW-key set declared and any third key a ceremony stop | amendment 36 (which itself superseded amendment 26) |
| *Acceptance criteria*, suite bullet | baseline number → same-session delta, provenance re-measured | amendment 40 |
| Chunk B acceptance, `check_cairn` bullet | "count may only grow" withdrawn | amendment 41 |
| *Verification*, Bandit + lockfile + content-scan bullets | delta assertions and the exit-code gate | amendments 35, 39 |

#### Amendment rows NOT folded, and why

| row | status |
|---|---|
| **32** | **Superseded**, not folded. `G1`/`G2` are replaced by the shared *Gate D-ON* block: `G1` treated a review section's presence as sufficient even at REVISE, `G2` omitted the corpus condition, and both ordered sections by written date. Its "the sibling side is not this plan's to write" clause is **discharged** — both plans now carry the block in one commit |
| **26** | Already superseded by **36** before this pass; folded via 36 |
| **5**, **8** | Already superseded by **40** and **41**; folded via those |
| **44** | **Moot for row 10** (the reciprocal gate half is discharged by this commit, so no `dev/PLANNING.md` deferred row is owed for it). **Row 11 stands**: the allowlist-versus-reviewed-residual policy for Cairn's 52 editorial-citation `[suspicious-url]` hits is a Maintainer decision under D3's escalation trigger and outlives this plan. It is **not** folded into a chunk because no chunk may decide it |
| **43** | Folded into `## Folded, not amended` as a notation note |
| all others (1-31, 33-42) | Folded; each named in the table above |

#### Figures re-derived in this pass

Measured under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13)
with `PYTHONDONTWRITEBYTECODE=1`. HEAD moved twice during the pass; each figure
names the revision it was taken at.

| figure | stated | measured | verdict |
|---|---|---|---|
| suite | 1744 passed / 2 failed `as_of 2026-08-04` | **1987 collected** at `66ce8c0`; the two AST failures were a sibling's uncommitted work and are gone | **does not reproduce** — criterion is now the delta |
| `check_cairn` | `OK -- 180 file(s); no issues; 68 links` | **178 file(s); 48 links; 2 issue(s)** at `66ce8c0`, both a concurrent scope's uncommitted work | **does not reproduce**; the count criterion is withdrawn as unsound |
| Bandit `scan_targets()` | 74 (plan) / 76 (amendment 37) | **76** at `64e8b7c` | amendment 37 reproduces; the plan's 74 is stale |
| lockfile | 81 files / 14 modules / 41 twins | **81 / 14 / 41** at `64e8b7c` | reproduces |
| `content_scan_runner.py` on Cairn's tree | 78 audited / 52 flags / exit 1 at `b8ab678` | **80 audited / 52 flags / 52 NEW / exit 1** at `64e8b7c` (scratch clone, five shipped files copied verbatim) | flag count reproduces; **file count grew 78 → 80**. The HOLD is still firing |
| `content-security` default selections | false across all presets | **false** in all three presets; absent from the **6**-entry `_DEFAULT_ON_MODULES`; no `_TOKEN_GATED_MODULES` — at `66ce8c0` | reproduces — Gate D-ON is prospective, not a release regression |
| `portable-security-sweeps` non-monotonicity | shared block: newest External *"above an older External section introduced by `976b402`"* | `976b402`'s section at `:1153`, `e1b2e30`'s at `:2253` — the newest is **below** the older | **one clause does not reproduce**; the load-bearing half (position vs commit order) does. Reported, not silently reworded — see *Gate D-ON* > plan-local notes |

#### What this pass did not close

* **Gate D-ON is not satisfied, and it fences this entire plan.** D-ON-1 and
  D-ON-2 are **NOT MET** and only the Maintainer can move them; D-ON-3 waits on the
  reciprocal plan's Chunk D. The fold makes the gate determinable, reciprocal and
  honest about its blast radius; it does not open it.
* **D3's HOLD is firing on a pre-implementation measurement** — 52 flags, exit 1.
  Under D3 that is a Maintainer question, and no fold pass answers it.
* **Amendment 44 row 11** (the editorial-citation policy) has no chunk home by
  construction and still needs its `dev/PLANNING.md` deferred row at the
  serialization point. That file is serialized and out of this pass's scope.
* **`## Verification`'s slot text still says the standing gates are "the same ones
  CI enforces".** Cairn has **no CI**. The text sits inside a
  `<!-- cairn:slot verification-commands -->` block that is template-owned rather
  than plan-owned, so this pass did not edit it; it is raised here because a plan
  that names a trigger must be able to open it, and this one cannot.

## Maintainer disposition -- default-on consequence -- 2026-08-05

The Maintainer's authorizing instruction, quoted verbatim and visually isolated:

> I accept content-security as default-on despite the documented whole-script Cyrillic residual and international-proper-noun tradeoff. I authorize Codex to scribe and commit this disposition in both content-scan-detectors and default-security-stance.

This disposition names and accepts the consequence Gate D-ON required the
Maintainer to own. It therefore satisfies **D-ON-2** and, by the governing
gate's explicit Maintainer-disposition route, **D-ON-1**. **D-ON-3** is already
met by the 74 named parametrized corpus rows landed in `8fea3f6` and verified
under the canonical suite in `7dd73a0`.

**Gate D-ON is MET.** This authorizes the default-on implementation described by
the reciprocal plans. It does not authorize a frozen-manifest re-pin, AST
re-anchor, credential use, signing, pushing, or any other Maintainer ceremony.
