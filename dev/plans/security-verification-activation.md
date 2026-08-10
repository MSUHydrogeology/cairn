<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/lifecycle.md doctrine/rationale.md doctrine/coordination.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->
<!-- cairn-accept: instruction-html-comment reason="The comment below is an explanatory note to human readers and to the claim checker about forward-reference and adopter-tree destination paths; it carries no directive to an agent and names no action to take." reviewer="Claude (author)" date=2026-08-04 -->
<!-- Five paths are exempted below, in two classes, and the `Proposed paths:` ledger further down
     records which materializes when. FORWARD REFERENCES (they resolve once this plan executes):
     templates/modules/default-on/security-verification.md, .../run_security_verification.py,
     bootstrap/tests/test_security_verification.py, dev/modules/security-verification.md.
     ADOPTER-TREE DESTINATION (it never resolves in Cairn): scripts/run_security_verification.py
     is where the dispatcher lands in an ADOPTER's repository; this plan deliberately does NOT
     self-host it in Cairn -- see Scope > "Cairn does not self-host the dispatcher".
     The file-scoped directive is used rather than the `Proposed paths:` marker alone because
     these tokens are cited throughout the chunk tables and acceptance criteria, not only in one
     contiguous block. -->
<!-- claim-check-allow: scripts/run_security_verification.py, templates/modules/default-on/security-verification.md, templates/modules/default-on/run_security_verification.py, bootstrap/tests/test_security_verification.py, dev/modules/security-verification.md -->

# Plan: local security-verification activation — a default-on dispatcher that can only narrow

**Source proposal**: `security-verification-activation` (accepted 2026-08-03 by
Maintainer Decision, *"I accept this proposal as revised"*). It currently sits at
`dev/proposals/archive/2026-08-03-codex-security-verification-activation.md` and moves to
`dev/proposals/archive/` when it archives.
**Status**: open
**Plan review**: required(**External**, security lens) — carried from the
proposal, whose Decision says so in terms: *"The plan carries
`required(External, security lens)` in its own right; this Decision does not
discharge it."* **No implementation commit lands before the `## Plan review`
section is in the tree.** See [Plan review — the brief](#plan-review--the-brief)
for why an Internal round does not discharge it.
**Last update**: 2026-08-04
**Opened**: 2026-08-04

## Source proposal

`security-verification-activation` settles one contract: **selecting a security
capability makes its local or offline evidence runner part of the expected
trusted-checkout workflow, through one default-on dispatcher whose authority is
strictly narrowing.** The plan executes that decision and does not re-litigate
it.

The artifact took a Gemini Flash External round (SHIP, concerns E1/E2), an
author Response accepting both, a revision — *"admitted and bound child
evidence"* — that added the registry-admission rule, parent-computed digest
binding, and exact `NOT_APPLICABLE` semantics, and a Claude External Security
Review returning **NO BLOCKING FINDINGS**. The Decision accepted it *as revised*
and recorded three properties the acceptance rests on. Those three are the plan's
spine and each gets an enforcing test:

1. **A closed registry of evidence modes** — a credentialed, deployed, active,
   arbitrary or unknown result is **not representable**, not merely rejected.
2. **Parent aggregation cannot strengthen a child** — the property that stops the
   dispatcher laundering INCOMPLETE legs into a CLEAN summary.
3. **CLEAN requires an admitted contract**, not a zero exit.

**Where the Decision overrides earlier text.** The Decision establishes the
**ordering** — this artifact is the dependency root for `api-web-security-modules`
and `portable-security-sweeps`, and precedes both their Decisions. Combined with
the revision's admission rule (*"The registry entry cannot precede capability
acceptance. A dormant source entry for an unaccepted or uninstalled capability is
not permitted."*), that settles a question the *original* Proposal left ambiguous
when it wrote that the initial registry *"may name reviewed local legs"* from the
three capability modules. **It may not.** At activation-v1 the shipped registry is
**empty**, and every adopter's first run prints `NOT APPLICABLE`. This is not a
reading of intent: it is the Decision's ordering plus the revision's admission
rule, and the Decision itself says the no-capability runtime effect is nil.

### Glossary — every term glossed on first use

The audience is a scientist who codes. This scope is a *supply-chain* change with
an executable at the end of it, and several of its terms name things that look
similar and are not.

* **The dispatcher** — the new `run_security_verification.py`. It runs no check
  itself. It reads which security capabilities are installed, looks each up in a
  **source-owned registry**, runs that capability's own local runner as a child
  process, validates what comes back, and prints one aggregate verdict.
* **Source-owned registry** — a Python data structure *inside the dispatcher
  file*. "Source-owned" is the whole security claim: no adopter file — not the
  profile, not the lockfile, not a policy file — can add an entry, a path, an
  argument, or an environment variable to it. Adopter data can only *select from*
  it.
* **Evidence mode** — `offline` or `loopback`, and nothing else. The mode is a
  property of the *registry entry*, not of anything the child says. A child
  registered `offline` that returns `loopback` evidence is DEGRADED.
* **Admitted** — a registry entry that cleared the **six**-part admission rule:
  the five parts in the proposal's revision (accepted capability proposal;
  reviewed plan with execution evidence for that exact mode; complete lockfile
  mapping group; schema and precedence tests; a Security Review of the registry
  change) **plus a sixth — the binding mode is part of what is admitted.** An
  entry is admitted *for a named `policy_binding_mode`*; changing an admitted
  entry's mode is a registry change and takes its own Security Review, not a
  follow-up commit. A `"living_state"` entry additionally requires the
  capability's own plan to carry **execution evidence for the compensating
  controls that replace the digest** — for `api-web-security-modules` those are
  the strict schema, the loopback-only local leg and `--authorize-base-url`, and
  *evidence* means an executed run, not a design argument. At v1 nothing is
  admitted, so the registry is empty and no mode is exercised.
* **Aggregate exit ladder** — `0` CLEAN / `5` INCOMPLETE / `10` FINDINGS / `20`
  DEGRADED-or-TAMPER, precedence `20 > 10 > 5 > 0`. **Not new to Cairn**: the
  shipped `templates/modules/team-gated/run_security_audit.py` already defines
  exactly these four constants. The dispatcher reuses the ladder; it does not
  invent one, and it does not touch that runner's finding semantics.
* **`NOT_APPLICABLE`** — a *fifth* state, distinct from CLEAN. It means "no
  installed capability has an admitted local entry". It exits 0 and is
  contractually forbidden from using the word CLEAN, or `secure`, or
  `passed security`.
* **Default-on module** — one installed unless an adopter removes it. Membership
  is the tuple `_DEFAULT_ON_MODULES` in `bootstrap/_scaffold/config.py`. Adding
  one changes what **every** future adopter receives.
* **Install contract** — the published `scaffold.py --manifest` enumeration plus
  the lockfile records derived from it. `AGENTS.md` calls it byte-level stable and
  adopter-depended-upon. A new manifest row is a **contract change**, treated here
  with its own acceptance criteria, never as a side effect of adding a file.
* **Merge directive** — `<!-- cairn:merge-target: <file> > <slot> -->` plus a
  paired `cairn:merge-content-start` / `-end` block inside a module's `.md`. At
  install time the scaffold copies that block into the named slot of the adopter's
  `AGENTS.md`. **No module in `templates/modules/` ships one today** (measured
  below) — this plan is the mechanism's first live use.
* **AST attestation** — a committed digest of every top-level symbol in
  `bootstrap/_scaffold/`. Changing a baselined symbol turns the gate red until a
  **supervised re-anchor** re-pins it. See *The cluster* below; this is the single
  largest coordination hazard in this plan.
* **Perturbation** — a deliberate change to repository state that a test is
  claimed to detect. This repository accepts a test only when its author can name
  a future state in which it fails **and has run** the change producing it.
  Perturbing a test's own body validates the test; only perturbing the **hazard**
  validates the claim. Every test below names the hazard perturbation.

## Proposed paths

Proposed paths:
- `templates/modules/default-on/security-verification.md` — the module doctrine + the `cairn:merge-target` directive; lands Chunk A.
- `templates/modules/default-on/run_security_verification.py` — the standard-library fixed-registry local dispatcher; lands Chunk A.
- `bootstrap/tests/test_security_verification.py` — the dispatcher's behavioral suite; lands Chunk A.
- `dev/modules/security-verification.md` — Cairn's own self-hosted rendering of the module doctrine, matching all six existing default-on modules; lands Chunk B.

## The measurement that shapes this plan

Every figure below was measured **for this plan**, at HEAD `eacb7dd`, under the
canonical interpreter `~/conda_envs/lhm/bin/python3.13` (Python 3.13.x), with
`PYTHONDONTWRITEBYTECODE=1`. **No repository file was modified.** Re-take each at
implementation rather than quoting from here.

### The AST baseline, and the fact that the working tree is not HEAD

```
$ ~/conda_envs/lhm/bin/python3.13 -c "import json,collections; \
    d=json.load(open('bootstrap/tests/fixtures/scaffold_ast_baseline.json')); \
    print(len(d), collections.Counter(k.split(':',1)[0] for k in d))"
174 Counter({'FunctionDef': 98, 'Assign': 53, 'ClassDef': 10, 'Import': 8,
             'Docstring': 1, 'Expr': 1, 'If': 1, 'If#2': 1, 'Try': 1})
```

**174 baseline entries; 161 of the three kinds** (`FunctionDef` 98 + `Assign` 53
+ `ClassDef` 10). Measured, not carried forward.

Verified against **clean HEAD** — the engine files extracted from `HEAD:` into a
scratch directory, so the concurrent working tree cannot contaminate the reading:

```
AST attestation OK — 174 baselined symbol(s) accounted for, unchanged.
```

Verified against the **live working tree at the same moment**:

```
AST attestation FAILED — 3 non-pure-motion symbol(s):
  CHANGED   FunctionDef:cmd_upgrade                in bootstrap/_scaffold/upgrade.py
  CHANGED   FunctionDef:forked_facade_findings     in bootstrap/_scaffold/lockfile.py
  CHANGED   FunctionDef:format_forked_facade_warning in bootstrap/_scaffold/lockfile.py
```

Those three are **uncommitted edits from a concurrent scope** (`git status
--short` showed `bootstrap/_scaffold/install.py`, `lockfile.py` and `upgrade.py`
modified, plus an untracked `bootstrap/tests/test_fork_advisory.py`).

**Re-measured about an hour later, while this plan was still being written, the
same command over the same working tree read:**

```
AST attestation FAILED — 6 non-pure-motion symbol(s):
  CHANGED   FunctionDef:_minimal_yaml_parse           in bootstrap/_scaffold/config.py
  CHANGED   FunctionDef:cmd_upgrade                   in bootstrap/_scaffold/upgrade.py
  CHANGED   FunctionDef:forked_facade_findings        in bootstrap/_scaffold/lockfile.py
  CHANGED   FunctionDef:format_forked_facade_warning  in bootstrap/_scaffold/lockfile.py
  CHANGED   FunctionDef:load_config                   in bootstrap/_scaffold/config.py
  MISSING   Try   (baselined, absent from the current module set)
```

Three became six, and a baselined symbol went **MISSING** — a stronger signal
than CHANGED, since it means a symbol the baseline pinned is no longer anywhere
in the module set. `bootstrap/_scaffold/config.py` had by then accumulated **372
insertions / 69 deletions** of another scope's uncommitted work.

This is the cluster hazard reproduced live, twice, on the day the plan was
written, and it is why the ceremony section below is written the way it is: **the
union must be formed from the tree that is actually being re-anchored, not from
any one plan's declaration read in isolation.** Note also what the two readings
share — **none** of the drift touches this plan's three declared symbols
(`Assign:_MODULE_MAPPINGS`, `Assign:_DEFAULT_ON_MODULES`, `FunctionDef:main` were
unchanged in both). This scope's delta is *currently* disjoint from what is in
flight; that is a snapshot, not a guarantee, and the fence is what makes it safe
either way.

### The symbol this plan changes has no surgical path

```
$ grep -n "_UPDATE_ALLOWLIST" -A 6 bootstrap/tests/_ast_attest.py
_UPDATE_ALLOWLIST: dict[str, str] = {
    "_MODULE_MAPPINGS": "Assign",
    "_SKILLS_MAPPINGS": "Assign",
    "_CORE_MAPPINGS":   "Assign",
    "install_onboarding": "FunctionDef",
}
```

`bootstrap/tests/_ast_attest.py` offers a hardened one-symbol rewrite
(`update-symbol`, `--expect-old` guarded, refusing on any unrelated drift) for
**four** symbols. `_DEFAULT_ON_MODULES` is **not** one of them — and it is not in
`gate_manifest.json`'s `mapping_symbols` either, which names only
`_CORE_MAPPINGS`, `_MODULE_MAPPINGS`, `_SKILLS_MAPPINGS`. It **is** in the AST
baseline (digest `2c8ef688f6865487`).

**Consequence, and it is load-bearing for the whole cluster:** the moment this
plan (or `default-security-stance`) appends one module name to
`_DEFAULT_ON_MODULES`, the surgical single-key path is unavailable and only the
**full supervised re-anchor** can clear the gate. That is a Maintainer act, and
two cluster scopes need it for the *same* symbol.

### New symbols are not gated; changed ones are

Read from `verify()` in `bootstrap/tests/_ast_attest.py` and confirmed by the
clean-HEAD run above, which printed 21 `note: NEW …` lines and still exited 0:
`verify` **reports** new top-level symbols and **fails** only on
CHANGED / MISSING / DUPLICATE. The stricter `known_new` complete-set match applies
to `update-symbol`, not to plain verify. **This plan adds no new
`bootstrap/_scaffold/` symbol**, so `scaffold_ast_known_new.json` is untouched.

### The dispatcher source cannot land unregistered

`scan-coverage` has fully landed. `bootstrap/tests/test_security_lint.py` now
carries an on-disk oracle and a growth tripwire, and there is a sibling pin:

| Pin | File | Value today |
|---|---|---|
| `test_templates_py_count_is_pinned` | `bootstrap/tests/test_security_lint.py` | `44` `.py` on disk under `templates/` |
| `test_manifest_has_the_expected_py_source_count` | `bootstrap/tests/test_notice_install.py` | `44` manifest `.py` sources |
| `test_every_templates_py_on_disk_is_release_scanned` | `bootstrap/tests/test_security_lint.py` | red for any `templates/**/*.py` no registry delivers |

Three channels agree at 44 (`git ls-files templates \| grep '\.py$' \| wc -l` →
44; the working-tree glob → 44; `install_manifest(modules=None)` verbatim `.py` →
44).

**So the dispatcher source and its `_MODULE_MAPPINGS` registration must land in
the SAME commit.** An intermediate commit holding an unregistered
`templates/modules/default-on/run_security_verification.py` fails two tests
immediately. The two `44` pins move to `45` in that same commit, and their own
message already says they must move together.

### Everything else, dated

* **Suite**: `1744 passed, 2 failed` in 159.51s — the two failures are exactly the
  AST-attest pair above, caused by the concurrent uncommitted engine edits, **not**
  by anything at HEAD. Re-baseline against a clean tree at implementation.
* **Install manifest**: `python bootstrap/scaffold.py --manifest` → **95 data
  rows** (96 lines incl. the header comment).
* **Release gate**: `python bootstrap/security_check.py` → `Bandit clean over 74
  shipped file(s).` → `PASS`.
* **Prose integrity**: `python scripts/check_cairn.py` → OK, **180** Markdown
  files, 68 external links not probed.
* **Neutrality**: `python scripts/quality_gate.py --sub neutrality` →
  `fail=95 info=21`, rc 1.
* **Registries**: `_DEFAULT_ON_MODULES` = 6 modules; `_MODULE_MAPPINGS` = 20
  modules; `_PRESETS` = 3 (`solo-greenfield`, `collaborative-team`,
  `high-rigor-legacy`).
* **`gate_manifest.json`**: 164 `frozen_files`. **None** of
  `templates/core/AGENTS.md`, `bootstrap/SAFETY.md`,
  `bootstrap/_scaffold/config.py`, `bootstrap/_scaffold/cli.py`,
  `templates/modules/README.md`, `docs/quickstart.md` is frozen.
  `bootstrap/tests/test_quickstart_sequence.py` **is** frozen — and needs no edit,
  because it derives the expected count live.
* **The merge mechanism has never run from a real module.** `grep -rn
  "cairn:merge" templates/modules/` returns exactly one hit, a *prose* mention in
  `templates/modules/default-on/documentation-plan.md`. Leaf-level coverage exists
  (`bootstrap/tests/test_module_merge.py`); end-to-end from a shipped module does
  not. This plan is the first live use, and Chunk B treats it as such.
* **The proposed slot text passes the content scanner.** Probed, not assumed —
  the exact standing-command block written to a scratch file and scanned with
  `templates/modules/team-gated/content_scan.py` → `OK -- 1 file(s) scanned; no
  flags.` This matters because `templates/core/AGENTS.md` is the strictest class
  under `bootstrap/SAFETY.md` Rule 7 and the block is an imperative aimed at an
  agent.

## The cluster — one ceremony, five scopes, formed by the Maintainer

**Five accepted scopes edit `bootstrap/_scaffold/config.py`**:
`profile-parse-fail-open` (in implementation now), `default-security-stance`,
`api-web-security-modules`, `portable-security-sweeps`, and this one. Four are
being planned in parallel.

This is **not** ordinary file overlap. `bootstrap/_scaffold/` is covered by the
AST attestation, whose re-anchor ceremony pins a **falsifiable union of CHANGED
symbols agreed in advance**. A concurrent engine change from an *undeclared*
scope does not merely enlarge that union — it **destroys the property the
ceremony exists to provide**, because "any symbol outside the union is a
stop-and-explain" stops discriminating the moment the union is not exhaustive.
The live measurement above is that failure mode already in progress.

### This plan's declared symbol delta

Measured against `bootstrap/tests/fixtures/scaffold_ast_baseline.json` at HEAD
`eacb7dd`. **3 CHANGED, 0 NEW, 0 MISSING, 0 DUPLICATE.**

| Symbol | Module | Baseline digest | Chunk | Why it changes | Surgical path? |
|---|---|---|---|---|---|
| `Assign:_MODULE_MAPPINGS` | `config.py` | `26957a8924042a0a` | A | one new key, `security-verification`, holding two `InstallSpec`s | **yes** — in `_UPDATE_ALLOWLIST` *and* `gate_manifest.mapping_symbols` |
| `Assign:_DEFAULT_ON_MODULES` | `config.py` | `2c8ef688f6865487` | B | one appended name, `"security-verification"` | **no** — in neither; full re-anchor only |
| `FunctionDef:main` | `cli.py` | `ff5a7441cceda605` | C | one `if "security-verification" in modules:` post-install note, on the `model-selection` precedent already in that function | **no** |

**Declared NOT changed, so its appearance is a stop-and-explain:**
`FunctionDef:format_profile_summary` (`config.py`, digest `830aac8b7c3d1bde`).
The proposal's revision asks the scaffold summary to name *"each selected
security capability, its local command, prerequisites"*. At v1 **the registry is
empty**, so that rendering has nothing to render and would ship as untestable
dead code. The module name itself already appears in the summary's *"Module
roster (to install)"* for free once `_DEFAULT_ON_MODULES` carries it. The
per-capability rendering is therefore **deferred to the first capability's plan**,
where it can be exercised — recorded in *Lasting-truth migration*. **A Maintainer
who reads the revision as requiring it at v1 can strike this deferral in one
line; it enlarges the union by exactly one symbol and changes no other chunk.**

Also declared **not** changed: `FunctionDef:install_manifest`,
`FunctionDef:install_modules`, `FunctionDef:write_install_lockfile`,
`Assign:KNOWN_TOKENS`, `Assign:_MODULE_REQUIRED_TOKENS`,
`Assign:_REFERENCE_SCRIPT_TOKEN`, `Assign:_GITIGNORE_SEEDS`,
`Assign:_MODULE_SUPERSEDES`, `Assign:_PRESETS`. The module needs no token, seeds
no `.gitignore`, supersedes no local surface, and is added to no preset (it is
default-on, which is a different mechanism). The standing command is a **literal
path** in the merge block, not a `{{token}}`, precisely so `KNOWN_TOKENS` and
`_REFERENCE_SCRIPT_TOKEN` stay out of the union.

### What this plan asserts about the ceremony

* **One ceremony, shared.** This plan does **not** run a re-anchor and does not
  own one. The union is formed **by the Maintainer at ceremony time** from each
  cluster scope's declared delta plus whatever else the tree actually shows.
* **The union is not the sum of the plans.** The live measurement proves a scope
  can be mid-flight and uncommitted. The ceremony's input is `verify` against the
  **tree being re-anchored**; the declarations are the *oracle it is checked
  against*, and a symbol in the tree but in no declaration is the stop-and-explain
  the ceremony exists to produce.
* **A declared symbol that turns out unchanged is reported, not ignored.** A
  shrink is safe but is still a discrepancy between plan and tree, and the
  implementing agent says so in the commit body rather than letting the union
  quietly over-cover.
* **`Assign:_DEFAULT_ON_MODULES` is contended.** `default-security-stance`
  Change 1 appends `content-security` to the *same* tuple. Whichever lands
  second re-measures the digest; **neither may use `update-symbol`** on it,
  because it is not allowlisted. If both land before one ceremony, the ceremony
  covers one symbol carrying two scopes' edits, and the Maintainer should be told
  which two.

### Order-independence, and the two places it fails

**True regardless of intra-cluster order:**

* The dispatcher's own behavior. It reads the lockfile and its own source
  registry. No other cluster scope changes either.
* The empty-registry / `NOT_APPLICABLE` contract. It is empty because no
  capability is accepted, and neither `default-security-stance` nor
  `profile-parse-fail-open` accepts one.
* The `+2` manifest rows and the `44 → 45` `.py` pins. `default-security-stance`
  adds **no** file (it flips an existing module default-on);
  `profile-parse-fail-open` adds none. `portable-security-sweeps` and
  `api-web-security-modules` each add their own, but the Decision orders both
  **after** this artifact.
* `Assign:_MODULE_MAPPINGS` conflict-freedom. Distinct dict keys; a textual
  conflict is possible, a semantic one is not.

**Order-sensitive, named so it is handled rather than discovered:**

1. **The `solo-greenfield` module count.** `docs/quickstart.md` states **6**,
   carrying an inline `verify:` marker naming the `solo_greenfield_module_count`
   invariant (the literal marker is not reproduced here — it would be parsed as a
   live directive in this file), checked by `scripts/measurements.py` and by
   [`bootstrap/tests/test_quickstart_sequence.py`](../../bootstrap/tests/test_quickstart_sequence.py),
   which asserts *prose == live*. Both this plan and `default-security-stance`
   add one default-on module. **Landing first the count is 7; landing second it is
   8.** The implementing agent **re-measures and does not apply the number written
   here.** The test is the guard: it fails RED automatically, in the same commit,
   whichever order obtains.
2. **`docs/solo-legacy-recipe.md`** says *"an **8-module roster** — the six
   default-on modules"*. Same two-scope contention, same rule: re-read and
   re-count, do not apply.
3. **`templates/modules/README.md`'s default-on table.** Both scopes add a row.
   Note in passing: the table already lists only **four** default-on modules
   against six in code — pre-existing drift this plan does not adopt as scope, and
   fixing it is not free of the other scope's row.
4. **The re-anchor itself**, per the previous section.

## Scope

Executes the accepted activation contract across four chunks. **The registry
ships empty.** This plan installs the *route*, not any evidence.

### What lands

* A standard-library, fixed-registry, local-only dispatcher shipped as a
  default-on module, plus its module doctrine.
* One `security-verification` slot in **`templates/core/AGENTS.md`** — the
  **shipped adopter template**, from which every adopter's own `AGENTS.md` is
  installed. **This is not Cairn's own `AGENTS.md`**, which is a serialized shared
  file this plan does not touch at all.
* Registration in `_MODULE_MAPPINGS` and `_DEFAULT_ON_MODULES`; two new install
  manifest rows and their lockfile records.
* A non-silent install: one post-install line naming the first-run command and
  disclaiming that installation gathered evidence.
* `bootstrap/SAFETY.md` recording child-process execution, lockfile integrity,
  ambient-environment reduction, and that command separation is **not** actor
  authentication.

### Out of scope, fenced explicitly

Taken from the proposal's own *Deliberately not touched* line and its Decision:

* **Deployed or credentialed checks.** No `deployed` subcommand, no mutation
  flag, no credential lookup, no socket. Not "guarded" — **not representable**.
* **Capability policy schemas.** Owned by each capability.
* **Third-party scanner installation.** The scaffold installs no scanner and runs
  none.
* **Arbitrary adopter CI.** Rejected in the proposal's *Alternatives*: CI
  providers, credentials, untrusted-change behavior and secret exposure need
  platform-specific review this plan does not do.
* **The existing finding semantics of any security runner.**
  `templates/modules/team-gated/run_security_audit.py` and
  `templates/modules/team-gated/content_scan.py` are read for precedent and
  **not edited**.
* **Any registry entry.** Per the Decision's ordering plus the revision's
  admission rule, no entry can be admitted before its capability's Decision. The
  shipped registry is `{}` and a test pins that.
* **The per-capability scaffold-summary rendering** — deferred, with the
  reasoning and the strike-in-one-line note in *The cluster* above.
* **Cairn does not self-host the dispatcher.** `bootstrap/tests/test_notice_install.py`'s
  twin check is *discovery-based* — it enforces byte-parity only for twins that
  already exist under `scripts/`/`tools/`, so declining to self-host is a
  supported choice, not a gap. Rationale: at v1 Cairn's own run would print
  `NOT APPLICABLE` and gather nothing, in exchange for a twin to keep in sync and
  a second Bandit surface. Cairn **does** self-host the module *doctrine* at
  `dev/modules/security-verification.md`, matching all six existing default-on
  modules. Revisit when the first capability lands — recorded in *Lasting-truth
  migration*.
* **The pre-existing `templates/modules/README.md` default-on drift** (four rows,
  six modules). Named above; not adopted.

### Documentation / doctrine surface

* **Governing layer, adopter-facing — yes.** `templates/core/AGENTS.md` gains one
  slot and, in its *high-risk surfaces* guidance, the dispatcher. This is the
  template an adopter's governing document is built from, so it is the highest-
  consequence prose in the plan and the strictest class under
  `bootstrap/SAFETY.md` Rule 7.
* **Governing layer, Cairn's own — none.** Cairn's `AGENTS.md` is untouched.
* **Deliberation layer** — `templates/modules/default-on/security-verification.md`
  (source) and `dev/modules/security-verification.md` (Cairn's rendering) own the
  registry rules, the aggregate ladder, trusted-checkout scope, local/deployed
  separation, and recovery from incomplete or degraded evidence.
* **Descriptive layer** — `bootstrap/SAFETY.md` (the four recordings the proposal
  names), `templates/modules/README.md` (one catalog row), `docs/quickstart.md`
  and `docs/solo-legacy-recipe.md` (the two counts).
* **Release-facing** — `CHANGELOG.md > Unreleased > Added`, one line, written at
  its serialization point.
* **Serialized shared files this plan does NOT edit**: `CHANGELOG.md` (except at
  its serialization point in Chunk D), `dev/PLANNING.md` (the one-line row-move
  that serializes plan-open), Cairn's own `AGENTS.md`, `docs/DOCUMENTATION_PLAN.md`,
  and `bootstrap/REANCHOR_RUNBOOK.md` (Maintainer-owned; see the fence).

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

## Maintainer fence

**Four things in this plan are not an implementing agent's to do.** They are
listed together, before the chunks, so no chunk can quietly absorb one.

1. **The AST re-anchor ceremony.** After Chunk A and again after Chunks B/C, the
   AST attestation is RED. The implementing agent's obligation is to **stop, name
   the changed symbols with their before/after digests, and report the delta
   against this plan's declaration** — then wait. Re-anchoring is a supervised act
   under `bootstrap/REANCHOR_RUNBOOK.md`, run by the Maintainer, over a union the
   Maintainer forms. **No agent runs `_ast_attest.py update-symbol`, edits
   `bootstrap/tests/fixtures/scaffold_ast_baseline.json`, or edits the runbook.**
   Note specifically: `_DEFAULT_ON_MODULES` is not allowlisted for
   `update-symbol`, so there is no "small" version of this step to be tempted by.
2. **Anything needing a key or credential.** Nothing in this plan does — no
   signing, no publish, no token. It is stated because the ceremony in
   `bootstrap/REANCHOR_RUNBOOK.md` has a signing phase, and an agent following
   the runbook to "finish the job" would walk into it. Do not.
3. **The gate-manifest re-pin. Two `FROZEN-MODIFIED` rows are GUARANTEED, not
   contingent.** Measured at `d73d436`: `gate_manifest.json` holds **164**
   `frozen_files` entries and **both** files this plan edits for the `44 → 45`
   pins — `bootstrap/tests/test_security_lint.py` and
   `bootstrap/tests/test_notice_install.py` — **are in that map.** So the earlier
   reading in *The measurement that shapes this plan* ("no file this plan edits is
   frozen") does not hold, and the conditional phrasing it produced ("if either
   turns out frozen") is replaced by this statement of fact. The implementing agent
   **records both stale entries in the commit body and does not re-pin.**
   `bootstrap/_scaffold/config.py` remains `cascade_mutable` under *"AST
   source-motion attest — one predeclared mapping-symbol delta only"*. Re-check the
   map at implementation anyway — it moves — but expect two rows, not zero.
4. **Ratifying the living-state narrowing — the B3 admission fence.** `policy_binding_mode:
   living_state` narrows a property the accepted proposal established: the
   revision established parent-computed digest binding over *"the runner and
   policy"*, and this mode drops the policy half for a declared class of records.
   **The schema and its tests land** — A1, A2, T5, T17, T36–T40, T44 — **and that
   is safe precisely because the v1 registry is empty and no mode is exercised.**
   What waits is the **living-state entry and every producer of it**: no entry
   using `policy_binding_mode: living_state`, and no chunk that writes the
   living-state record, lands until the Maintainer ratifies the narrowing. **This
   is one condition, stated identically in the reciprocal plan** — see *The binding
   contract, and the admission fence it shares* (B3) below; it is not a registry
   fence here and a chunk fence there. An implementing agent who finds a
   capability plan asking for such an entry **stops and reports**, exactly as at
   the AST fence. The Maintainer's disposition of the 2026-08-05 review round is
   **not** this ratification.

An additional standing rule for this plan: the Maintainer's serialization points
(`dev/PLANNING.md`, `CHANGELOG.md`) are edited at the defined moments only.

### Folded, not amended — how to read this plan

**An implementing agent who reads only the chunk tables and their acceptance
criteria executes the current spec.** The review-driven decisions are folded
into the operative rows below rather than bound by reference from an amendment
table. `doctrine/plans.md:202-207` makes chunk-table cell text mutable in place
while a plan's status is `open` with no commits in flight against the chunks
being edited — this plan's exact state: status `open`, zero implementation
commits. The `## Plan review`, `## Response to plan review` and `Sharpening`
sections are **untouched and stay append-only**; the fold ledger in
`### Sharpening — the 2026-08-05 fold pass` at the end of this file names every
amendment row now carried by a cell.

**Where the shared block below and an earlier amendment row disagree, the block
governs.** It supersedes **M29**'s registry-entry-only fence, and it is
the condition M29's Maintainer-fence item 4 now points at.

**The 2026-08-05 External REVISE round is disposed of by the Maintainer.** The
authorizing instruction, verbatim:

> Go ahead with implementation once you've revised these. I don't want another review round

Recorded in full at `## Maintainer disposition of the 2026-08-05 External review
round` below. **It disposes of the review round and nothing else** — it is not a
bypass of the round, and it supplies no Maintainer credential, no signing ref, no
AST re-anchor ceremony, no ratification of the B3 narrowing below, and no
approval to push.

### The binding contract, and the admission fence it shares

**This block is shared, verbatim, with the reciprocal plan
(`api-web-security-modules` <-> `security-verification-activation`). A change to
it lands in both files in the same commit, or it has not landed.**

**B1 — v1's four named bindings resolve to two apparatus bindings.** The v1
question named four: runner, policy, principal, scope. Exactly two are
apparatus-level: `runner_binding_mode` and `policy_binding_mode`, both in the
registry's closed vocabulary. **Principal and scope are child-policy semantics
and have no apparatus field, by decision and not by oversight.** Verified
against the tree rather than asserted: the installer record binds `src`, `dst`,
`verbatim` and `hash` plus optional living-state / base-cache fields, and
`bootstrap/_scaffold/install.py` contains no `principal` field and no `scope`
binding field — its only occurrences of "scope" are a destination-set comment
and the base-template-cache docstring. Inventing either field is out of scope
for this pair and takes its own design.

**B2 — extra-field disposition.** An unrecognized key in a registry entry or an
installer record is **refused**, not ignored: the reader is a closed-vocabulary
validator and an unknown key is a violation naming the key. Two tests, not one:
the existing missing-field refusal, plus an extra-field refusal. If a
source-owned exact constructor makes an extra field structurally unreachable,
*that* is the contract to state and to test — a structural impossibility is
asserted by a test that tries it, never inferred.

**B3 — the admission fence, one condition on both sides.** The dispatcher and
the registry schema may land with an **empty registry**. What waits is the
*living-state entry and every producer of it*: no entry using
`policy_binding_mode: living_state`, and no chunk that writes the living-state
record, lands until the Maintainer ratifies the narrowing and this shared block
is in force in both files. This is one fence stated identically on both sides,
not a registry fence on one side and a chunk fence on the other.

**B4 — the Chunk F split is replaced, because the old one contradicted its own
criteria.** Fencing F2 while letting F1 and F3--F6 land left Chunk F's
acceptance criteria requiring filled-policy and living-state behavior that F2
was fenced from producing. Chunk F's criteria are rewritten to the B3 line: the
landing part asserts dispatcher-plus-empty-registry behavior only, and every
criterion that needs a filled policy or a living-state record moves to the
fenced part with F2 and Chunk G.


## Sequence

Chunk order is load-bearing. **A before B**: the dispatcher must be registered
and provably narrowing before it becomes universal, so that no intermediate
commit ships a default-on executable whose behavior is unpinned. **C after B**:
the install message names a command that must already install.

```
0. plan-open  -- this plan + the dev/PLANNING.md row-move            [commit pending]
   (plan review) -- required(External, security lens); NO code before it lands
1. Chunk A -- the dispatcher + its module, registered, not universal
   [LANDED: 6e3a8ed, follow-up 6b488a2, 2026-08-10]
   >>> MAINTAINER FENCE: AST re-anchor #1 (Assign:_MODULE_MAPPINGS) -- RED,
       reported not re-anchored, per this plan's own Maintainer fence #1
2. Chunk B -- universality: default-on, the slot fires, the counts   [commit pending]
3. Chunk C -- the non-silent install                                 [commit pending]
   >>> MAINTAINER FENCE: AST re-anchor #2 (_DEFAULT_ON_MODULES, main)
4. Chunk D -- SAFETY.md, the catalog row, the changelog              [commit pending]
```

A single ceremony after Chunk C covering all three symbols is equally acceptable
and is the Maintainer's call; the fence markers show where the gate is red, not
how many times it must be cleared.

---

### Chunk A — the dispatcher and its module, registered but not yet universal

The whole security surface lands here, under an opt-in-only selection path, so
that every property is pinned before universality is switched on. **Atomic by
measurement, not by preference** — see *The dispatcher source cannot land
unregistered*.

| # | File | Change |
|---|---|---|
| A1 | `templates/modules/default-on/run_security_verification.py` *(new)* | The dispatcher. Standard library only. Module-level `_REGISTRY: dict[str, RegistryEntry] = {}` — **empty**, with **eleven** admission fields as a frozen dataclass/`NamedTuple`: `module_id`, `runner_repository_path`, `argv_mode`, `policy_repository_path \| None`, `child_schema_version`, `capability_contract_version`, `evidence_mode`, `accepted_process_exits`, `result_to_aggregate_mapping`, **`runner_binding_mode`**, **`policy_binding_mode`**. **Every field is required, has no default, and is not inferable from any other field.** **No twelfth field, and in particular no `principal` and no `scope`** — per **B1** those are child-policy semantics with no apparatus field, and adding one is a registry-schema change with its own design and its own Security Review. **Three closed sets, all `frozenset` literals in this source, all constrained at construction:** `evidence_mode` ∈ `{"offline", "loopback"}`; `runner_binding_mode` ∈ `{"immutable_digest"}` — a deliberately **one-member** set, so a future "living runner" cannot appear by omission but only by a source edit widening the frozenset, which is a registry-schema change and therefore a Security Review; `policy_binding_mode` ∈ `{"none", "immutable_digest", "living_state"}`. **Agreement rules, each refused at construction with a message naming both fields:** `policy_binding_mode == "none"` **iff** `policy_repository_path is None` (either without the other refuses — this closes the undeclared third mode); `"immutable_digest"` and `"living_state"` each require a non-`None` path. **B2's extra-field disposition, in the constructor and in the lockfile-record reader:** an unrecognized key is **refused, not ignored** — construction with a twelfth field raises (a source-owned exact constructor, so this is structural, and **T44 asserts it by trying it** rather than inferring it from frozenness), and the parent's **lockfile-record reader is a closed-vocabulary validator** over `{src, dst, verbatim, hash}` plus the optional `living_state` / `base_cache` / `base_hash`, refusing an unrecognized key with **DEGRADED (`20`)** and a message naming the key. *Recorded, because it is why this reader exists here:* measured at `d73d436`, `bootstrap/verify_integrity.py:63-111` reads records with `rec.get(...)` and **ignores** an unrecognized key, so this dispatcher is where B2's refusal is actually implemented; the `verify_integrity` half is a lasting truth neither plan in this pair closes. **Runtime binding by mode, all failures DEGRADED (`20`) with no child launched, never INCOMPLETE and never CLEAN:** under `"none"` the parent binds the runner only; under `"immutable_digest"` the parent binds the runner **and** compares the policy's SHA-256 with its lockfile record, **and refuses (`20`) if that record carries `living_state: true`** — an immutable declaration over a living record is a misdeclaration, not a pass; under `"living_state"` the parent binds the runner digest unchanged, binds the policy's **existence, regular-file and non-symlink status**, binds the **presence** of a lockfile record, **refuses (`20`) if that record lacks `living_state: true` or if the policy path is outside the engine's `_LIVING_STATE_DSTS` authoritative set** — the fail-closed mirror of `bootstrap/verify_integrity.py:96-105` — and **does not compare the policy's content digest**, recording the policy in the machine report as `binding: living_state, digest_not_compared` so the dropped property is visible in the output rather than invisible. The dropped property is named in A2's doctrine as a residual, not skipped silently. **The high-risk Security-Review designation is carried in this file too** — a module docstring block at the `_REGISTRY` definition site, verbatim and hash-pinned, so a registry change and its review trigger are one artifact (see A4 and T42). Aggregate constants reuse the ladder already in `templates/modules/team-gated/run_security_audit.py` (`0/5/10/20`) plus `NOT_APPLICABLE`. Child invocation: `[sys.executable, "-I", <registry runner path>, <registry argv_mode>]`, `shell=False`, explicit minimal `env`, `timeout`, byte cap, strict UTF-8, strict JSON. SPDX header, matching every other shipped twin. |
| A2 | `templates/modules/default-on/security-verification.md` *(new)* | Module doctrine: the registry rules, the five-part admission rule quoted from the proposal's revision, the aggregate ladder and its precedence, trusted-checkout scope, the local/deployed separation **and its explicit non-claim** (not actor authentication), and recovery from INCOMPLETE / DEGRADED. **The admission rule is the SIX-part rule** — the five quoted from the revision plus *the binding mode is part of what is admitted* (see the glossary's `Admitted` entry). **Three further contents, because an adopter receives this file and never receives this plan:** (a) **`NOT_APPLICABLE` is not evidence** — it is the *absence* of security evidence, must not be reported, aggregated, or badged as a passing check, and its exit `0` means "nothing was asked of me", not "nothing is wrong"; (b) **the binding-mode schema of A1**, including the residual that a `"living_state"` policy's bytes are **not** lockfile-attested and its review channel is git; (c) **the high-risk Security-Review designation** of the dispatcher, its registry, its child result schema, its binding-mode schema and every registry entry. Carries the `<!-- cairn:merge-target: AGENTS.md > security-verification -->` directive and the paired content block holding the exact standing command. Substituted (`verbatim=False`), so the merge pass reads it. **Residual, stated not hidden:** an adopter who marks the installed slot `<!-- cairn:customized -->` drops the designation from their `AGENTS.md` with **no side file and no warning from any Cairn tool** — pinned by T43 as a characterization, not closed. |
| A3 | `bootstrap/_scaffold/config.py` | One new key in `_MODULE_MAPPINGS`: `"security-verification": [InstallSpec("default-on/security-verification.md", "dev/modules/security-verification.md"), InstallSpec("default-on/run_security_verification.py", "scripts/run_security_verification.py", verbatim=True)]`. **The only engine edit in this chunk.** Symbol delta: `Assign:_MODULE_MAPPINGS`. |
| A4 | `templates/core/AGENTS.md` | A new `## Security verification` heading with the `<!-- cairn:slot security-verification -->` / `<!-- cairn:end security-verification -->` pair, placeholder text on the `claim-check` slot's exact model (*"If security-verification is not installed, replace with `N/A: security-verification not installed`. An unfilled slot is a review finding."*). Plus one line in the *Project-specific conventions* guidance naming the dispatcher, its registry, its child result schema, **its binding-mode schema**, and every registry entry as **high-risk Security Review surfaces**. **This is channel 1 of three, and it is the one that is NOT a guard.** The designation lands on three channels: (1) **this slot** — customizable, and an adopter who marks it `<!-- cairn:customized -->` gets status `customized`, the designation **absent**, **no side file and no fidelity warning at all**; (2) **`dev/modules/security-verification.md`** (B2) — lockfile-recorded and **not** living-state, so an adopter edit is `modified (hash mismatch)`, exit 1; (3) **the dispatcher source** `templates/modules/default-on/run_security_verification.py` (A1) — a module docstring block at the `_REGISTRY` definition site, verbatim and hash-pinned, additionally flagged `locally-modified` by `classify_verbatim` and never clobbered. **Channels 2 and 3 are the tamper-evident ones**; channel 3 exists so that a registry change and its review trigger are one artifact. T42 asserts 2 and 3; T43 pins channel 1's silent-drop residual as a characterization. |
| A5 | `bootstrap/tests/test_security_verification.py` *(new)* | The dispatcher suite: **T1–T24, T36–T41 and T44** below. |
| A6 | `bootstrap/tests/test_security_lint.py` | `test_templates_py_count_is_pinned`: `44` → `45`. Its own message already instructs moving the sibling in the same commit. |
| A7 | `bootstrap/tests/test_notice_install.py` | `test_manifest_has_the_expected_py_source_count`: `44` → `45`. |

#### The tests, each with the perturbation that makes it RED

**The rule applied throughout: the perturbation targets the hazard in the
dispatcher, never the test's own body.** Where a test's only available
perturbation *is* a body edit, that is stated as a weakness rather than dressed
up.

Tests T6–T24 need a child to dispatch, and the shipped registry is empty. They
inject a synthetic entry by monkeypatching the module-level `_REGISTRY` and point
it at a fixture child under `tmp_path`. That injection is legitimate precisely
because `_REGISTRY` is the source-owned surface: patching it is a *source* edit
in test form, which is the only way an entry may ever appear. **No test writes an
entry through adopter data — that is what T2 forbids.**

*Registry integrity — the "closed registry" property.*

| T | Test | Hazard perturbation → RED |
|---|---|---|
| T1 | `test_shipped_registry_is_empty_at_activation_v1` — `_REGISTRY == {}`, asserted against the **shipped module source**, read from `templates/`, not the imported object a fixture may have patched. | Add any entry to `_REGISTRY` in A1's source. Fails. This is the admission rule made mechanical: an entry cannot appear before its capability's Decision. |
| T2 | `test_no_lockfile_or_policy_field_can_enter_the_registry` — table-driven over `runner`, `argv`, `env`, `executable`, `mode`, `python`, `shell`, `cwd`, `timeout`: for each, a crafted lockfile / policy carrying that key, asserting the dispatched call is unaffected and the key is never read. | In A1, make the entry resolver fall back to `lock_entry.get("runner")` when the registry lacks a path. Fails on the `runner` row. |
| T3 | `test_unknown_selected_capability_is_unsupported_not_executed` — a lockfile roster naming `made-up-security`; expect INCOMPLETE (`5`), `subprocess.run` never called. | Replace the registry lookup with a permissive `templates/modules/**/run_{module}.py` derivation. Fails — a child launches. |
| T4 | `test_no_deployed_or_credentialed_mode_is_representable` — parametrized over `deployed`, `credentialed`, `active`, `remote`, `""`, `None`, `"offline,loopback"`: constructing an entry with any of them raises at construction. | Widen the `evidence_mode` frozenset to include `"deployed"`. The `deployed` row fails. **This is the Decision's first named property**, so its perturbation is the one a reviewer should reproduce first. |
| T5 | `test_every_admission_field_is_required` — a deletion mutant per field: **eleven** synthetic entries, each missing one of A1's eleven fields, each refused at construction with a message naming the field. **The two new rows are the load-bearing ones:** an entry that omits `policy_binding_mode` or `runner_binding_mode` must **refuse**, not default — a defaulted binding mode is the *silently change modes* failure, reached by omission. | Give any field a default. That field's row fails. *Weakness stated, unchanged:* this pins the **validator**; that the shipped registry is empty is T1's job, not this one's. |

*Dispatch and subprocess behavior.*

| T | Test | Hazard perturbation → RED |
|---|---|---|
| T6 | `test_child_argv_is_exactly_the_registry_vector` — captured argv equals `[sys.executable, "-I", <runner>, <mode>]`, length 4, no PATH-resolved `python`. | Append a policy-derived argument in A1. Fails. |
| T7 | `test_child_env_is_minimal_and_strips_proxies_and_credentials` — parent env seeded with `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, `NO_PROXY`, `AWS_SECRET_ACCESS_KEY`, `GITHUB_TOKEN`, `PYTHONPATH`, `PYTHONSTARTUP`; the fixture child dumps its own `os.environ` keys into `details`; assert the received set is exactly the declared allowlist. | Pass `env=os.environ.copy()`. Fails, naming every leaked variable. |
| T8 | `test_oversized_child_output_is_degraded_and_not_relayed` — child writes cap+1 bytes; expect `20`, and the child's bytes absent from stdout **and** stderr. | Remove the byte cap. Fails. |
| T9 | `test_child_timeout_is_degraded` — child sleeps past the timeout; expect `20`. | **Raise the timeout constant above the child's sleep** (do *not* delete `timeout=`, which would hang the suite). The child completes, the aggregate becomes CLEAN, the test fails. |
| T10 | `test_invalid_utf8_and_invalid_json_are_degraded` — two children, one emitting a lone `0x80`, one emitting `{`; both `20`. | Decode with `errors="replace"`. The invalid-UTF-8 row now parses and reaches CLEAN. Fails. |
| T11 | `test_forged_terminal_controls_never_reach_the_terminal` — a child whose `details` carries `\x1b[2J`, an OSC-8 hyperlink, `\r`, and a fake `PASS` banner; assert rendered stdout contains no `\x1b`, no `\r`, and none of the child's literal bytes. | Render `details` with a bare f-string instead of the safe renderer. Fails. |
| T12 | `test_raw_child_stdout_and_stderr_are_never_relayed` — child writes distinctive markers to both streams; assert neither appears in the parent's output at any aggregate level, including `20`. | Add `print(proc.stdout)` on the DEGRADED path. Fails. |
| T13 | `test_id_mismatch_is_degraded_never_clean` — parametrized over wrong `capability`, wrong `contract`, wrong `evidence_mode`, wrong `schema`, an unknown extra key, and a wrong-typed `result`; every row `20`, none `0`. | Drop each equality check in turn; the matching row fails. The `evidence_mode` row is the *"a child registered offline cannot return loopback"* property. |
| T14 | `test_process_exit_and_result_must_agree` — two children: exit 0 with `"result": "FINDINGS"`, and exit 1 with `"result": "CLEAN"`; both `20`. | Remove the agreement check. Both rows fail. **This is the Decision's third named property** — CLEAN requires an admitted contract, not a zero exit. |
| T15 | `test_aggregate_precedence_over_every_ordered_pair` — all 16 ordered pairs from `{CLEAN, INCOMPLETE, FINDINGS, DEGRADED}` plus three-leg and four-leg combinations; result is always the max under `20 > 10 > 5 > 0`. | Change the fold from max-by-rank to first-wins. The `(CLEAN, DEGRADED)` row fails. **This is the Decision's second named property** — aggregation cannot strengthen a child. |

*Parent-computed binding.*

| T | Test | Hazard perturbation → RED |
|---|---|---|
| T16 | `test_parent_computes_digests_and_ignores_child_supplied_ones` — child emits `details.runner_sha256 = "deadbeef…"`; assert the report carries the parent's own SHA-256 of the runner bytes and the forged string appears nowhere in the output. | Read the digest from `details`. Fails. |
| T17 | `test_runner_or_policy_digest_mismatch_is_degraded` — **parametrized by `policy_binding_mode`**, because the assertion is no longer unconditional. Rows: (a) runner byte flipped — `20`, no child launched, **under all three modes**; (b) policy byte flipped under `"immutable_digest"` — `20`, no child launched; (c) policy byte flipped under `"living_state"` — the leg **proceeds** (that is the mode's whole point) and the report records the policy as `binding: living_state, digest_not_compared`, so the dropped property is **visible in the machine output** rather than invisible; (d) policy byte flipped under `"none"` — unreachable, since the path is `None`; asserted as a construction refusal, not a runtime row. | Skip the runner comparison: (a) fails under all three modes. Skip the policy comparison: (b) fails. Drop the `digest_not_compared` annotation: (c) fails on a missing key rather than passing silently. |
| T18 | `test_symlinked_runner_or_policy_is_refused` — three rows: symlinked leaf, symlinked parent directory, and a runner replaced by a symlink between the digest read and the launch (the latter asserted as a **named residual**, not as closed). | Open with plain `open()` and no `is_symlink()` / regular-file check. The first two rows fail; the third is documented as the accepted trusted-checkout race the proposal states rather than claims closed. |
| T19 | `test_missing_lockfile_record_for_a_registered_runner_is_degraded` — registry entry present, lockfile record absent; `20`. | Treat a missing record as "unlocked, proceed". Fails. |

*The universal no-capability contract — the E2 surface.*

| T | Test | Hazard perturbation → RED |
|---|---|---|
| T20 | `test_no_capability_prints_the_exact_not_applicable_line_and_exits_0` — stdout contains exactly `NOT APPLICABLE: no selected local security capability`, exit `0`, and **one JSON object** on stdout carrying seven asserted members: `schema` (a versioned literal, on the `bootstrap/tests/_oracle.py:81` model `"cairn.scaffold_split.oracle/v1"`), `status: "not_applicable"` **as an explicit string state**, `ok: true`, `aggregate: "NOT_APPLICABLE"`, `evidence_count: 0` **as an explicit integer**, `legs: []`, and a non-empty `reason`. *Why the explicit state and count, since they look redundant:* `legs: []` makes automation infer a count from a container length and `aggregate` makes it string-match a label; automation needs a state and a count it can key on directly. | Make the no-capability path return `CLEAN`. Fails on the literal, on `status`, and on `aggregate`. **Second perturbation:** drop `evidence_count` from the report; the test fails on a missing key rather than silently passing on a container check. *The hazard is the false-security claim, not the string* — a string-only perturbation would be a body edit and is not the one recorded. |
| T21 | `test_no_capability_output_uses_no_security_coverage_wording` — human **and** machine output scanned for `CLEAN`, `secure`, `passed security`, `no vulnerabilities`, `verified`; none present. | Same hazard as T20. Also fails if a later author adds a friendly *"all clear"* line. |
| T22 | `test_no_capability_opens_no_socket_and_does_no_dns` — `subprocess.run`, `socket.socket`, `socket.create_connection`, `socket.getaddrinfo`, `urllib.request.urlopen` all monkeypatched to raise; run; exit `0`. | Add a socket open on the no-capability path. Fails. |
| T23 | `test_dispatcher_source_reads_no_deployed_credential_variable` — an **AST scan of the dispatcher source file**, asserting every `os.environ` / `os.getenv` read resolves to the declared allowlist and no deployed-credential variable name appears as a literal. | Add `os.getenv("AWS_SECRET_ACCESS_KEY")` to A1. Fails. **Channel note**: the oracle is the source text; the subject is the runtime behavior. Independent — the dispatcher never reads its own source. |
| T24 | `test_a_socket_opening_child_is_excluded_by_admission_not_blocked_at_runtime` — the proposal's specific ask, in two halves. (a) A fixture child that calls `socket.socket()` and binds `("127.0.0.1", 0)` — no outbound traffic — cannot be admitted, because admission requires an accepted capability contract and the shipped registry is empty. (b) Force-injected into `_REGISTRY`, the parent **does** run it and **does not** prevent the bind; the test asserts that, documenting the residual honestly. | For (a): remove the admission check so an arbitrary path becomes reachable; (a) fails. For (b) there is deliberately **no** perturbation that makes the parent block the socket — that is the finding, and the test's docstring says so where a reader will find it. |

*Binding-mode closure — the reciprocal-contract surface. Every row here exists
because a mode that can be omitted, widened, mutated, or misdeclared is the
failure the closed vocabulary was written to prevent.*

| T | Test | Hazard perturbation → RED |
|---|---|---|
| T36 | `test_policy_binding_mode_is_a_closed_set` — parametrized over `deployed`, `unbound`, `skip`, `living`, `immutable`, `""`, `None`, `"none,living_state"`: construction raises for every row. The exact mirror of T4 for the second closed set. | Widen the frozenset to include `"unbound"`; that row fails. |
| T37 | `test_binding_mode_and_policy_path_must_agree` — four rows: (`"none"`, a path) refuses; (`"immutable_digest"`, `None`) refuses; (`"living_state"`, `None`) refuses; (`"none"`, `None`) constructs. | Drop the agreement check; the first three rows fail. |
| T38 | `test_living_state_mode_requires_the_lockfile_flag_and_the_authoritative_set` — three rows: lockfile record present but **without** `living_state: true` → `20`; record flagged but the path is **outside** `_LIVING_STATE_DSTS` → `20`; both satisfied → the leg proceeds and the policy digest is not compared. | Make the living branch skip the flag check; row one reaches CLEAN. |
| T39 | `test_immutable_mode_refuses_a_living_state_record` — an entry declared `"immutable_digest"` whose policy record carries `living_state: true` → `20`, no child launched. **T38 and T39 together are "cannot treat a living policy as an immutable one", in both directions.** | Treat `living_state` as "skip the comparison"; the row reaches CLEAN. |
| T40 | `test_a_registry_entry_cannot_change_mode_after_construction` — assigning `policy_binding_mode` on a constructed entry raises. Mode-immutability at the object level, where T36/T37 cover it at the declaration level. | Make the dataclass non-frozen (or use a plain class); the assignment succeeds and the test fails. |
| T41 | `test_the_module_doctrine_states_not_applicable_is_not_evidence` — read the **shipped** `templates/modules/default-on/security-verification.md` from `templates/`, not an installed copy; assert it contains the non-evidence statement, that `NOT_APPLICABLE` appears in it at all, and that no green-security phrase (`CLEAN`, `secure`, `passed security`, `no vulnerabilities`, `verified`) occurs in the same paragraph. Precedent for asserting shipped doctrine text: `bootstrap/tests/test_practice_modules.py`. *Channel note:* the oracle is the shipped source read independently; the subject is what an adopter receives. Same class as T1 and T23. | Delete the non-evidence sentence from A2's source; the test fails. |
| T44 | `test_an_unrecognized_key_is_refused_and_named` — **B2, in two halves, and the impossibility is asserted by trying it.** (a) *Entry side:* constructing `RegistryEntry` with a twelfth keyword — parametrized over `principal`, `scope`, `runner`, `env`, and one arbitrary name — raises at construction, and the test asserts the **key it tried** appears in the message. This is a source-owned exact constructor, so the refusal is structural; **the test attempts it rather than inferring it from the dataclass being frozen.** (b) *Lockfile-record side:* a record carrying an unrecognized key → **`20`, no child launched**, message naming the key. *Channel note:* (b)'s material is a record the **test** writes, never one the dispatcher wrote, so the check is not verified by the artifact it judges. *Recorded gap, not covered by this test:* `bootstrap/verify_integrity.py:63-111` ignores the same key; that is the paired plan's F5(b) characterization and a lasting truth for neither plan to close silently. | (a) Give the constructor `**kwargs`; every row fails. (b) Make the reader `rec.get(...)`-based like `verify_integrity`; the row reaches CLEAN. |

**Acceptance criteria — Chunk A.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_security_verification.py bootstrap/tests/test_security_lint.py bootstrap/tests/test_notice_install.py -q` → all pass, 0 skipped.
* **Install-contract movement, as a contract change with its own criteria** — not
  a side effect:
  * `python bootstrap/scaffold.py --manifest` → **`N + 2` data rows, where `N` is
    re-taken at the plan-open commit.** `N = 95` measured at `d73d436` under
    `/Users/kendal30/conda_envs/lhm/bin/python3.13` — a starting point, **not a
    constant**: every sibling scope that adds module files moves it, so the
    assertion is on the diff. Diffed against a capture taken at the plan-open
    commit; the diff must be **exactly two added lines** and **zero modified or
    removed** lines. A modified row means an existing destination moved — stop and
    re-review.
  * The two rows are `dev/modules/security-verification.md` (substituted) and
    `scripts/run_security_verification.py` (verbatim), in that tab-separated
    format.
  * `duplicate_destinations` over the full manifest → empty. No existing adopter
    path is shadowed.
  * A fresh scaffold's lockfile records **both** files with hashes — the complete
    mapping group — verified by reading `dev/.cairn/cairn-lock.yml` in a
    `tmp_path` install, not by asserting the writer was called.
* `python bootstrap/security_check.py` → `PASS`, Bandit line reporting **`N + 1`
  shipped files, where `N` is re-taken immediately before this chunk.** Measured
  at `d73d436`: `security_check: Bandit clean over 76 shipped file(s)` → `PASS`.
  **Do not apply 77 from here** — the shipped-file count moves with every cluster
  scope that adds a shipped file; the arithmetic (`+1`, because `scan_targets()`
  derives `templates/` targets from manifest data and the dispatcher adds exactly
  one scanned file) is what is asserted. **The dispatcher is newly scanned Layer-4
  code**; if it produces a MEDIUM+ finding the gate goes red and the fix is the
  code, **never** an allowlist entry. Expect LOW `B404`/`B603` from the
  `subprocess` family, matching `run_security_audit.py`'s existing profile.
* The two `44 → 45` pins move **together**, in this commit —
  `bootstrap/tests/test_notice_install.py:75` (manifest `.py` sources) and
  `bootstrap/tests/test_security_lint.py:291` (distinct `.py` on disk under
  `templates/`). Both values verified `44` at `d73d436`. **Cross-scope hazard,
  named:** `api-web-security-modules` moves the same two pins *and* a third
  (`bootstrap/tests/test_notice_install.py:145`, the `95` manifest-row pin);
  whoever lands second **re-measures and applies no number from either plan.**
* **AST**: `_ast_attest.py verify` reports exactly **one** CHANGED symbol,
  `Assign:_MODULE_MAPPINGS`, baseline `26957a8924042a0a` → measured value. Any
  second symbol is a stop-and-explain. **Then stop** — the fence.
* **Perturbation ledger in the commit body**: for each of **T1–T24, T36–T41 and
  T44**, the change made, the failure observed with its message, and
  `git diff <path>` empty after restore. T24(b)'s deliberate non-perturbation is
  recorded as such. Where a test is a **characterization** rather than a guard,
  the ledger says so **in those words**.
* **Channel note.** The dispatcher's subject is its own runtime behavior; the
  oracles are fixture children written by the test (T6–T22, T24), the shipped
  source text read independently (T1, T23), and the lockfile plus on-disk bytes
  (T16–T19). None is derived from the object under verification.

---

### Chunk B — universality

One tuple entry, and everything that follows from it. This is where **every
adopter** starts receiving the module, and where the merge mechanism runs live
from a real module for the first time.

| # | File | Change |
|---|---|---|
| B1 | `bootstrap/_scaffold/config.py` | Append `"security-verification"` to `_DEFAULT_ON_MODULES`. Symbol delta: `Assign:_DEFAULT_ON_MODULES`. **No surgical path** — see the fence. |
| B2 | `dev/modules/security-verification.md` *(new)* | Cairn's own rendering of A2, matching all six existing default-on modules under `dev/modules/`. Carries the `Cairn's own` prefix on any further-reading link, per the rule in `bootstrap/tests/test_doc_governance.py`. |
| B3 | `docs/quickstart.md` | The `solo-greenfield` count and its enumeration. **Re-measure; do not apply a number from this plan** — see *Order-independence*. |
| B4 | `docs/solo-legacy-recipe.md` | The roster sentence. Same rule. |
| B5 | `bootstrap/tests/test_security_verification.py` | **T25–T33, T31b, T42 and T43** below. |

| T | Test | Hazard perturbation → RED |
|---|---|---|
| T25 | `test_every_preset_installs_the_module` — parametrized over all three presets; `expand_preset` includes `security-verification`; a real `tmp_path` install writes both destinations. | Remove B1. All three rows fail. |
| T26 | `test_modules_empty_list_opts_out_entirely` — `modules: []` installs nothing, per the Decision's settled rule that *an explicit `modules:` list is exact and is never overridden*. | Make the default-on set merge into an explicit list. Fails. |
| T27 | `test_literal_modules_list_without_it_does_not_install_it` — `modules: [claim-check]` yields no dispatcher, no `dev/modules/security-verification.md`. | Same hazard as T26. |
| T28 | `test_modules_remove_opts_out_and_the_summary_announces_it` — `modules_remove: [security-verification]`; not installed, and `format_profile_summary` lists it under *Default-on opted out*. **Note**: this passes on the existing generic mechanism, i.e. it is a *characterization* test, and its docstring says so rather than implying B1 made it true. | Remove B1: the module is no longer default-on, so *"opted out"* has nothing to report and the summary assertion fails. |
| T29 | `test_upgrade_plan_lists_it_and_adopt_module_installs_it` — a lockfile written before the module existed; `upgrade --plan` names it under *new modules available (opt-in)*; `--adopt-module security-verification` writes both files and records both in the lockfile. | Remove the `_MODULE_MAPPINGS` entry (A3): `set(_MODULE_MAPPINGS) - lock_modules` no longer contains it. Fails. |
| T30 | `test_installed_AGENTS_md_carries_the_exact_standing_command` — a real scaffold; the installed `AGENTS.md` contains the exact two-sentence rule between the slot markers. | **The deletion mutant the proposal names**: delete the `cairn:merge-content` block from A2's source. The slot installs with its placeholder, the assertion fails. Run it — this is the mechanism's first live use and the assertion most likely to be silently vacuous. |
| T31 | `test_the_merge_pass_reports_the_fill_and_the_fidelity_check_is_clean` — the install's *Module-merge pass* output names `AGENTS.md > security-verification`, and `check_slot_fidelity` returns no warning. | Change one word inside the merge-content block after install (simulating adopter edit without the customized marker); the fidelity check warns. Confirms the check is live rather than always-silent. |
| T32 | `test_composition_no_capability_one_capability_many` — three synthetic rosters over injected registry entries: none, one, two. Assert no duplicate leg, no leg silently delegated to another, and each leg's `evidence_mode` label survives aggregation unchanged. | Make aggregation collapse legs sharing a runner path. The two-capability row fails. |
| T33 | `test_the_dispatcher_runs_green_from_a_real_fresh_scaffold` — end-to-end: scaffold into `tmp_path`, run `python scripts/run_security_verification.py local` **as a subprocess** from that tree, assert exit `0` and the exact `NOT APPLICABLE` line — **plus every machine assertion of T20 through the same subprocess**: parse the emitted JSON and assert `schema`, `status == "not_applicable"`, `ok is True`, `aggregate == "NOT_APPLICABLE"`, `evidence_count == 0`, `legs == []`. The public path, not an import. **T20 drives `main()` in-process; T33 is the only test that sees what an adopter's automation sees.** | Break the lockfile read path (point `_LOCKFILE` at a non-existent relative location). Fails with DEGRADED rather than 0 — proving the test exercises the real file layout, not a stub of it. **Second perturbation:** make the no-capability path emit exit 0 with **no machine object at all** — the human line still matches, the exit code is still 0, and only the machine assertions go red. That is the generic-exit-0-mistaken-for-a-passing-security-check hazard, made mechanical. |
| T31b | `test_a_prefilled_slot_defers_to_a_side_file_and_warns` — install into a target whose `security-verification` slot body already carries adopter prose; assert outcome `conflict-deferred`, the `.cairn-merge-pending` side file present and named for the slot, a `slot-content-stale-or-partial` fidelity warning, exit 0, and the standing command **absent** from `AGENTS.md`. | Make `_slot_is_empty` treat any body as empty; the side-file and warning assertions go red. |
| T42 | `test_the_high_risk_designation_survives_on_two_tamper_evident_channels` — read the shipped A2, B2 and **dispatcher** sources for the designation; scaffold into `tmp_path`; `verify_integrity` → OK; delete the designation from the installed `dev/modules/security-verification.md` **and** from `scripts/run_security_verification.py`; `verify_integrity` reports `modified (hash mismatch)` for **both** and exits **1**. | Drop the designation from the dispatcher source; the source-read row fails. |
| T43 | `test_a_customized_slot_silently_drops_the_designation` — a **characterization** test that pins the residual rather than closing it: mark the slot `<!-- cairn:customized -->`, run the merge; assert status `customized`, designation absent from `AGENTS.md`, **`check_slot_fidelity` returns an empty list**, no side file, and the two tamper-evident channels still carry it. Its docstring says, where a reader will find it, that **a green T43 is a recorded open residual, not a closed one.** | Make `_slot_is_customized` return `False`; the status and no-warning assertions go red. |

**Acceptance criteria — Chunk B.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests -q` → green apart from
  the AST-attest pair, which is red **by design** until the fence clears. Record
  the exact node ids so a reviewer can see nothing else moved.
* [`bootstrap/tests/test_quickstart_sequence.py`](../../bootstrap/tests/test_quickstart_sequence.py)
  green — it asserts *prose == live*, so B3 is correct only if this passes.
  `python scripts/measurements.py` likewise, for the
  `solo_greenfield_module_count` invariant.
* `python scripts/check_cairn.py` → **OK, and no reported issue attributed to a
  file this plan edits.** That is the whole criterion. **The Markdown file count
  is deliberately not a criterion in any form**: it read **177** at `d73d436` and
  **178** at `d2f82e0` a few commits later, and across four days it has read
  180 → 195 → 176 → 177 → 178 — the checker did not change, the *population* did
  (archived sources are skipped), so the count moves in **both** directions with
  work this plan does not own.
* `python scripts/quality_gate.py --sub neutrality` → `fail` unchanged at **95**
  (verified `fail=95 info=21` at `d73d436`). `templates/modules/*.md` and
  `docs/*.md` are inside its scan roots, so B2/B3/B4 pass through it and the
  figure moving is a finding. **Re-take the number immediately before this chunk**
  rather than trusting this line: it is a same-run comparison, not a constant.
* The new module doctrine passes the content scanner:
  `python templates/modules/team-gated/content_scan.py
  templates/modules/default-on/security-verification.md` → no flags. Already
  probed for the slot text; re-run over the full file.
* **AST**: exactly **one** new CHANGED symbol, `Assign:_DEFAULT_ON_MODULES`,
  baseline `2c8ef688f6865487`. Report; do not re-anchor.
* **Perturbation ledger** for **T25–T33, T31b, T42 and T43** in the commit body,
  T30's deletion mutant called out by name. **T28 and T43 are characterization
  tests, and the ledger says so in those words** — a green characterization test
  is a recorded residual, not a closed one.

---

### Chunk C — the non-silent install

The proposal's *"Adoption must be non-silent"* requirement, reduced to the part
that is true and testable at v1.

| # | File | Change |
|---|---|---|
| C1 | `bootstrap/_scaffold/cli.py` | Inside `main`, one `if "security-verification" in modules:` block on the `model-selection` precedent already in that function: print the first-run command and one sentence stating the module installs a verification route and **gathered no evidence during scaffold**. No host tool runs. Symbol delta: `FunctionDef:main`. |
| C2 | `bootstrap/tests/test_security_verification.py` | T34–T35 below. |

| T | Test | Hazard perturbation → RED |
|---|---|---|
| T34 | `test_install_output_names_the_first_run_command_and_claims_no_evidence` — capture a real scaffold's stdout; assert the literal `python scripts/run_security_verification.py local` appears **and** that the output contains none of `CLEAN`, `secure`, `scanned`, `verified`, `no vulnerabilities`, `security check passed`. | Reword C1 to *"security verified"*. Fails on the forbidden-wording half. |
| T35 | `test_installation_executes_no_selected_scanner` — `subprocess.run` monkeypatched to raise for the whole install; the scaffold completes. | Make C1 invoke the dispatcher to "show the adopter it works". Fails. This is the proposal's *"never claims that installation itself produced security evidence"* turned into a mechanical guard. |

**Acceptance criteria — Chunk C.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_security_verification.py bootstrap/tests/test_scaffold.py bootstrap/tests/test_cli_module.py -q` → green.
* **AST**: exactly one further CHANGED symbol, `FunctionDef:main`, baseline
  `ff5a7441cceda605`. **`FunctionDef:format_profile_summary` must NOT appear** —
  its appearance is the stop-and-explain this plan pre-declared.
* **Then the fence.** Report the full three-symbol delta against this plan's
  declaration, with before/after digests, and wait.

---

### Chunk D — the descriptive surface and the changelog

| # | File | Change |
|---|---|---|
| D1 | `bootstrap/SAFETY.md` | The four recordings the proposal names, sited in Rule 7's Layer-4 discussion and the self-check: (a) the scaffold now ships a file that **executes a child process** in an adopter tree; (b) that dispatch is gated on lockfile integrity and parent-computed digests; (c) the child's environment is reduced from ambient, with proxies and credential-bearing variables stripped; (d) **command separation is not actor authentication** — a person or agent with shell access can invoke another script directly, and Cairn does not claim to distinguish a human process from an agent process. (d) is the sentence that must not be softened. **Plus a fifth recording (e):** the dispatcher, its source-owned registry, its child result schema, **its binding-mode schema**, and every registry entry are **high-risk Security-Review surfaces**; that designation is carried on three channels of which **two are tamper-evident** (the lockfile-recorded `dev/modules/security-verification.md` and the hash-pinned dispatcher source) and **one is not** (the adopter's `AGENTS.md` slot, which `<!-- cairn:customized -->` silently exempts from both the merge and the fidelity check); and an adopter who customizes that slot **removes the designation from their governing document with no warning from any Cairn tool.** (e) is a recorded residual, **not** a claim of coverage. |
| D2 | `templates/modules/README.md` | One `default-on` row. Re-read first — `default-security-stance` adds one too. |
| D3 | `CHANGELOG.md > Unreleased > Added` | One line: a default-on local security-verification dispatcher and its `AGENTS.md` standing rule; registry ships empty, so a no-capability install reports `NOT APPLICABLE` and gathers nothing. Cross-reference proposal and plan **by stem**. Written at its serialization point. |

**Acceptance criteria — Chunk D.**

* `python scripts/check_cairn.py` → OK, with **no issue attributed to a file this
  chunk edits**. No file-count criterion — see Chunk B.
* `python scripts/quality_gate.py --sub neutrality` → **unchanged against a
  capture taken immediately before D1**. Verified `fail=95 info=21` at `d73d436`;
  the comparison is same-run, and the number is re-taken rather than trusted from
  this line.
* `python scripts/claim_check.py <file>` over each edited Markdown file, **one
  file per invocation** — the checker takes a single path and exits 2 on more.
* **Verify the quoted sentences before editing.** D1 and D2 quote surfaces
  sibling scopes may have moved. Re-read at implementation; do not apply this
  plan's text blind.
* **Channel note.** The claim is that the prose matches the code. The evidence is
  a reading of the landed dispatcher **plus a live run of it from a fresh
  scaffold** (T33), never a reading of the prose just written. `check_cairn`
  checks link and claim-path integrity, not whether a sentence is true.

---

## Acceptance criteria

Per-chunk criteria are above; these are the plan-level deliverables.

* **Tests that must pass.**
  * `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests` — the whole suite,
    green, **0 failed / 0 skipped / 0 xfailed**, under the canonical interpreter,
    with `PYTHONDONTWRITEBYTECODE=1`, **measured on a clean tree after the
    Maintainer's re-anchor**. **No baseline total is stated here, deliberately.**
    The figure is **retired as an oracle**: it has read 1744 → 1779 → 1790 → 1959
    across three days, and this fold pass did **not** re-measure it rather than
    add a fifth reading that dates as fast. The binding criterion is
    **"collection grows by exactly the new nodes and drops none"**, against a
    count **re-taken on a clean tree at the implementing commit**.
  * `bootstrap/tests/test_security_verification.py` — **T1–T44 including T31b**,
    the plan's own surface. **Chunk A** holds T1–T24, T36–T41 and T44; **Chunk B**
    holds T25–T33, T31b, T42 and T43; **Chunk C** holds T34–T35. The
    perturbation-ledger obligation extends to every one of them, and where a test
    is a **characterization** rather than a guard — T28, T43 — the ledger says so
    in those words. *(Forward reference: the file lands at Chunk A; registered
    under `Proposed paths:` above.)*
  * [`bootstrap/tests/test_security_lint.py`](../../bootstrap/tests/test_security_lint.py)
    — the `45` pin and the on-disk oracle, which now covers the dispatcher.
  * [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
    — the sibling `45` pin; its twin check stays green because Cairn declines to
    self-host the dispatcher.
  * [`bootstrap/tests/test_quickstart_sequence.py`](../../bootstrap/tests/test_quickstart_sequence.py)
    — unchanged and green; it is the automatic guard on B3's count.
  * [`bootstrap/tests/test_config_module.py`](../../bootstrap/tests/test_config_module.py),
    [`bootstrap/tests/test_profiles_smoke.py`](../../bootstrap/tests/test_profiles_smoke.py),
    [`bootstrap/tests/test_practice_modules.py`](../../bootstrap/tests/test_practice_modules.py)
    — unchanged and green; all three loop `_DEFAULT_ON_MODULES` and pick the new
    member up derivedly.
  * [`bootstrap/tests/test_module_merge.py`](../../bootstrap/tests/test_module_merge.py)
    — unchanged and green; its leaf coverage is what T30/T31 promote to
    end-to-end.
  * **Every new test shown non-vacuous by a run perturbation**, ledger in the
    commit body. Where a test cannot be made to fail, the plan says so instead
    (T24(b), and T28's characterization framing).
* **Doc updates that must land.** All hand-authored: `templates/core/AGENTS.md`
  (slot + high-risk line), `templates/modules/default-on/security-verification.md`,
  `dev/modules/security-verification.md`, `bootstrap/SAFETY.md`,
  `templates/modules/README.md`, `docs/quickstart.md`,
  `docs/solo-legacy-recipe.md`, `CHANGELOG.md > Unreleased > Added`. **No
  generated docs, no snippet-synced blocks.**
* **Examples / smoke checks required.** `python bootstrap/scaffold.py --manifest`
  → `N + 2` rows, diffed to exactly two additions (`N = 95` at `d73d436`, re-taken
  at the plan-open commit). `python bootstrap/security_check.py`
  → `PASS` over `N + 1` shipped files (`N = 76` at `d73d436`, re-taken before
  Chunk A). A fresh `tmp_path` scaffold followed by `python
  scripts/run_security_verification.py local` → exit 0 and the exact
  `NOT APPLICABLE` line (T33). **N/A**: the `examples/` gallery — this change
  touches nothing the runnable examples demonstrate.
* **Inbound path-link updates.** None expected. `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no edit there. Confirm at archive time rather than assume.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants, each with the chunk and test that enforces it.**
  * *No credentialed / deployed / active / unknown evidence mode is representable.*
    T4 (Chunk A). The Decision's first named property.
  * *Parent aggregation never strengthens a child.* T15 (precedence over every
    ordered pair) and T32 (labels survive composition). The Decision's second.
  * *CLEAN requires an admitted contract, not a zero exit.* T13 + T14 + T19
    (Chunk A). The Decision's third.
  * *No adopter file can add or steer a child.* T2 + T3 (Chunk A). This is the
    proposal's own wrongness test — *"the implementation is wrong if a project
    file can add or steer a child"*.
  * *Raw child output never reaches the terminal.* T11 + T12.
  * *The shipped registry is empty at v1.* T1, read from the shipped source.
  * *A no-capability install claims nothing.* T20 + T21 + T34.
  * *Installation gathers no evidence.* T35.
  * *The install contract moves by exactly two additive rows.* Enforced by the
    manifest diff in Chunk A's acceptance, plus the lockfile mapping-group read.
    **Not guarded by a standing test, and that is the claim an External reviewer
    should attack** — nothing goes red if a later author edits an existing row.
    The indirect mitigation is `duplicate_destinations` plus the fidelity check.
  * *The engine symbol delta is exactly three.* Enforced by `_ast_attest.py
    verify` at each fence, checked against the declaration table.
* **Public-path → test mapping.** The dispatcher's public entry point is `python
  scripts/run_security_verification.py local`. It is exercised **through that
  public path as a real subprocess from a real scaffold** by T33, not only by
  importing its functions. T20–T22 drive `main()` in-process, which is the
  argument-handling layer, and say so. `install_modules` and the merge pass are
  exercised through a real `tmp_path` scaffold by T25 and T30–T31, never through
  a stub of themselves. Fixture children in T6–T24 are the **input** to the
  subject, never its oracle.
* **Failure modes.**
  * Lockfile missing / unparseable → **DEGRADED (20)**, on the precedent already
    in `templates/modules/team-gated/run_security_audit.py`. T19.
  * Runner or policy digest mismatch → **DEGRADED**. T17.
  * Symlinked runner or policy, leaf or parent → **DEGRADED**. T18.
  * Child times out, over-writes, or emits invalid UTF-8/JSON → **DEGRADED**.
    T8, T9, T10.
  * Child returns a well-formed result with a wrong ID → **DEGRADED**. T13.
  * Selected capability with no registry entry → **INCOMPLETE (5)**, never
    silently 0. T3.
  * Selected capability whose generated policy is `configured: false` →
    **INCOMPLETE**. Contract stated in A2's doctrine; **untestable at v1** with an
    empty registry, so it lands as a *synthetic-entry* test in T5's table and
    becomes execution-backed in the first capability's plan. Named rather than
    implied.
  * No capability at all → **`NOT_APPLICABLE`, exit 0**, and no word implying
    coverage. T20–T22.
  * A flawed child that opens a socket or reads a credential → **open at the
    dispatcher, closed at admission**. T24. The parent provides **no** network
    containment and this plan does not claim it does; that property is
    capability-owned, per the author Response to [E1].
  * A same-user race between digest verification and child execution →
    **open, accepted residual**, stated in T18's third row and in A2's doctrine.
  * An adopter invoking a capability's deployed procedure directly →
    **out of scope by construction**; command separation is not actor
    authentication, recorded in `bootstrap/SAFETY.md` (D1d).
* **Edge cases handled.** `modules: []` (T26). An explicit list omitting the
  module (T27). `modules_remove` (T28). Upgrade from a pre-module lockfile and
  `--adopt-module` (T29). A destination collision with an adopter's existing
  `scripts/run_security_verification.py` — handled by the scaffold's existing
  `skipped-exists` path; **not newly tested**, and named here as a gap.
  Zero, one and many capabilities (T32). An adopter who customizes the merged
  slot — the existing `cairn-customized` marker path, T31.
* **Known omissions, stated rather than implied.** (a) No capability's local
  contract is exercised, because none is accepted; every child in this plan is a
  fixture, and no fixture discharges a capability's no-network or loopback proof.
  (b) The per-capability scaffold-summary rendering is deferred (see *The
  cluster*). (c) `bootstrap/scaffold.py --manifest` byte-stability is asserted by
  a one-off diff, not by a standing test. (d) The destination-collision path for
  the two new files is untested. (e) The dispatcher's Bandit profile is
  *predicted* from `run_security_audit.py`'s shape and measured only at
  implementation; a MEDIUM+ finding would be a code fix inside Chunk A, not an
  allowlist entry. (f) Whether Cairn should self-host the dispatcher is deferred
  to the first capability's plan. (g) The interaction of this plan's re-anchor
  with the other four cluster scopes' is a Maintainer sequencing question this
  plan surfaces and does not answer.

## Verification

Run under the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`, Python
3.13.x) with `PYTHONDONTWRITEBYTECODE=1`. A different minor silently changes both
the suite figure and `ast.dump` structure, which the attestation depends on.

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

**Plan-specific gates, added because this change touches those surfaces.**

* **The release gate** — `python bootstrap/security_check.py`. Expected `PASS`,
  Bandit line reporting **`N + 1`** shipped files, where `N` is **re-taken
  immediately before Chunk A**. Measured at `d73d436`: `N = 76`, `PASS`. Do not
  apply a number from this plan; the arithmetic is what is asserted.
* **The install-contract diff** — `python bootstrap/scaffold.py --manifest`
  captured at the plan-open commit into the session scratch directory, diffed
  after Chunk A. **Expected: exactly two added lines, zero modified, zero
  removed.** `N` → `N + 2` data rows, `N` re-taken at the plan-open commit
  (`N = 95` measured at `d73d436`).
* **The three-channel agreement on the `.py` count** — `git ls-files templates |
  grep '\.py$' | wc -l`, the working-tree glob, and
  `install_manifest(modules=None)` verbatim `.py`. All **44** before Chunk A, all
  **45** after. A disagreement is a finding wherever it appears.
* **The content scanner over agent-loaded prose** — `python
  templates/modules/team-gated/content_scan.py <file>` over
  `templates/core/AGENTS.md` and
  `templates/modules/default-on/security-verification.md`. Both are Rule-7
  classes and the merge block is an imperative aimed at an agent.
* **The doc-invariant check** — `python scripts/measurements.py` for
  `solo_greenfield_module_count`, alongside `test_quickstart_sequence.py`.
* **The AST delta report, at each fence** — `python bootstrap/tests/_ast_attest.py
  verify bootstrap/tests/fixtures/scaffold_ast_baseline.json
  bootstrap/_scaffold/*.py`, with the CHANGED list compared line by line against
  the declaration table in *The cluster*. **Run on a tree containing only this
  scope's edits**; if another scope's work is uncommitted in the tree, extract
  `HEAD` plus this scope's files to a scratch directory and verify there — the
  technique this plan used, and the reason its own figures are trustworthy.
* **The perturbation ledgers** — per chunk, in the commit body: the change made,
  the failure observed with its message, and the byte-identical restore verified
  with `git diff <path>` (empty).

## Plan review — the brief

**Declared tier: `required(External, security lens)`.** Carried from the
proposal, whose Decision states it explicitly and says the Decision does not
discharge it.

**Does an Internal round discharge it? No.** Internal's floor is the same agent
type in a fresh session; External's floor is a **different agent type, or a
human**. A fresh-session read by this plan's author's own type cannot satisfy a
tier defined by structural independence, and this artifact is the one whose
output every adopter's `AGENTS.md` will carry. An Internal round is welcome as a
*sharpening* pass and does not substitute for the required round. **No
implementation commit lands before the External section is in the tree.**

**What the reviewer should attack first**, in descending order of what would hurt
most if wrong:

1. **T4 and T24 together.** T4 claims deployed evidence is *not representable*;
   T24 claims the boundary is admission rather than runtime. If those two are
   both true the architecture holds; if either is a validation rule wearing a
   structural exclusion's clothes, the Decision's first named property is
   overstated.
2. **The empty-registry reading.** This plan asserts the v1 registry ships empty,
   overriding the original Proposal's *"may name reviewed local legs"*. The
   argument is the Decision's ordering plus the revision's admission rule. If a
   reviewer reads it otherwise, most of Chunk A's shape changes.
3. **The declared symbol delta.** Three CHANGED, zero NEW. A reviewer with a
   checkout can falsify it in one command.
4. **The `format_profile_summary` deferral.** Named as strikeable in one line.
5. **The install-contract invariant with no standing test** — flagged in
   *Author-accounting* as the weakest guard in the plan.

## Code review

*Filled in after implementation commits land.*

## Lasting-truth migration

*Filled in at archive time. Each deferred item's durable home is pre-declared
here so the archive is a check rather than a search — per the archive
precondition, this plan does not archive until every one has landed somewhere
outside it.*

| # | Deferred item | Pre-declared durable home |
|---|---|---|
| L1 | The per-capability scaffold-summary rendering (capability name, local command, prerequisites, meaning of a missing tool or policy) | The **first capability plan to be accepted** — `portable-security-sweeps` or `api-web-security-modules` — as an explicit chunk, since only there can it be exercised. Carries `FunctionDef:format_profile_summary` into *that* plan's declared symbol delta. |
| L2 | Whether Cairn self-hosts `scripts/run_security_verification.py` | Same first capability plan. Once a registry entry exists, Cairn's own run produces evidence and the twin is worth its parity cost. |
| L3 | The `configured: false` → INCOMPLETE contract, execution-backed | Same first capability plan; it needs a real generated policy file, which v1 has none of. |
| L4 | The destination-collision path for the two new files | `dev/modules/incident-trackers.md` if it ever fires in practice; otherwise a one-line note in the code review's coverage line. Not worth a proposal. |
| L5 | `templates/modules/README.md`'s pre-existing default-on drift (four rows, six modules — seven or eight after the cluster) | A **trivial-triage fix** by whichever cluster scope lands its README row last, recorded in that commit body. It needs no proposal; it needs an owner, and the last row-adder is the natural one. |
| L6 | The install-manifest byte-stability invariant having no standing test | `dev/proposals/` — a new proposal if the code review agrees it is a real gap. Explicitly **not** smuggled into this plan. |
| L7 | The cluster's shared re-anchor sequencing across five scopes | Maintainer-owned; the durable record is the ceremony entry in `bootstrap/REANCHOR_RUNBOOK.md`, which this plan does not write. |

This section is append-only once written.

---

## Plan review -- Claude (Internal, same-agent-type; security lens) -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`), fresh session, security lens.

**Standing — this review does NOT discharge the declared tier.** The plan
declares `required(**External**, security lens)`, carried from the proposal's
Decision. I am the **same agent type as this plan's author**, so this read has
**no cross-type structural independence**. Under the Dual-Review model an
External round's floor is a different agent type or a human; a fresh-session
same-type read cannot meet it. The plan's own *Plan review — the brief* says so,
and it is right. **This is a sharpening pass only. The External security-lens
round remains outstanding, and no implementation commit may land on the strength
of this section.** Everything below was measured against the working tree at
HEAD `eacb7dd`; engine measurements were taken against a clean `git archive HEAD`
extraction in a scratch directory so the ten concurrently-modified files could
not contaminate the reading. **No repository file was modified**; the two
end-to-end merge probes ran against throw-away copies of the tree in the session
scratch directory.

### Steelman

This is the strongest plan in the current cluster, and its central load-bearing
finding is **correct on measurement**. `Assign:_DEFAULT_ON_MODULES` really is in
the AST baseline (digest `2c8ef688f6865487`, confirmed byte-exact) and really is
in **neither** `_UPDATE_ALLOWLIST` (`bootstrap/tests/_ast_attest.py`, lines
141–146: exactly `_MODULE_MAPPINGS`, `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`,
`install_onboarding`) **nor** `gate_manifest.json`'s `mapping_symbols` (exactly
the three registry mappings). There is no surgical path, two cluster scopes
contend for that one symbol, and the plan surfaces this to the Maintainer instead
of routing around it. All four declared digests reproduce exactly. The
declared-NOT-changed list, the `44 → 45` atomicity argument, the discovery-based
twin check that makes declining to self-host legitimate, the empty-registry
reading derived from Decision ordering plus the admission rule, and the
`+2`-manifest-row accounting are all verified correct. The perturbation
discipline is real: 33 of 35 tests name a perturbation that targets the *hazard*
rather than the test body, T9 correctly avoids the timeout deletion that would
hang the suite, and T24(b) and T28 declare their non-perturbability honestly
rather than dressing it up. The Maintainer fence is drawn in the right places and
the plan genuinely declines to run the ceremony.

The concerns below are all **execution-blocking-as-written but cheap to fix in
the plan**. None of them touches the architecture the Decision accepted.

### Concerns

**[I1] The slot placeholder in A4 makes the merge defer — the standing rule
never reaches the adopter's `AGENTS.md`. Measured end-to-end, twice.**
This is the plan's headline deliverable and it does not land as specified.
`merge_module_into_slot` (`bootstrap/_scaffold/slotmerge.py`) inserts the
module's contributed content **only** when the slot body is empty, and
`_slot_is_empty` (line 199) is literally `body.strip() == ""`. A4 specifies
placeholder text *"on the `claim-check` slot's exact model"* — and that model
(`templates/core/AGENTS.md`, lines 228–234) is non-blank prose. A non-blank body
that differs from the module content falls through to the **conflict path**.

Reproduced against a scratch copy of HEAD with A4's slot (placeholder prose) plus
A2's merge directive on an installed substituted default-on module, running the
real scaffold into a fresh target:

```
Module-merge pass:
  [conflict-deferred] AGENTS.md > security-verification -> ...cairn-merge-pending
  [slot-content-stale-or-partial] AGENTS.md > security-verification (fidelity check)
```

The installed `AGENTS.md` contained **zero** occurrences of the standing command;
the contributed prose went to a per-slot side file beside `AGENTS.md`; and the
scaffold still **exited 0**. So:

* **T30 fails as specified** — *"the installed `AGENTS.md` contains the exact
  two-sentence rule between the slot markers"* is false on a fresh install.
* **T31 fails as specified** — *"`check_slot_fidelity` returns no warning"* is
  false; it warns `slot-content-stale-or-partial` on **every** fresh install.
* The plan's *What lands* promise — the slot *"from which every adopter's own
  `AGENTS.md` is installed"* — silently does not happen, behind a printed line
  and a zero exit.
* An unadvertised adopter-visible artifact (the `.cairn-merge-pending` side file)
  appears in every adopter root. It is not a manifest row, so the `+2`
  install-contract accounting does not see it.

Counterfactual, same probe, slot body **empty** (marker pair only):

```
Module-merge pass:
  [inserted] AGENTS.md > security-verification
```

rule present in `AGENTS.md`, no side file, no fidelity warning. **The fix is one
line of A4: ship the slot empty.** That costs the placeholder guidance, which is
a real (small) loss worth stating rather than trading silently.

**Root cause, and it is the recurring failure this review was asked to hunt.**
`_slot_is_empty`'s docstring says *"placeholder prose for adopter agents to fill
is fine (it gets overwritten on merge)"* — which **contradicts its own
implementation**. The plan measured everything else in this scope and took this
one from the mechanism's self-description. That is the artifact under
verification supplying the material used to verify it. The plan even flagged T30
as *"the assertion most likely to be silently vacuous"* and then resolved it the
wrong way. The docstring/code divergence is itself worth a separate trivial-triage
fix, and should not be smuggled into this plan.

**[I2] `docs/quickstart.md` carries a *second* pinned number the plan never
names, and A4 turns `test_quickstart_sequence.py` RED from Chunk A.**
`bootstrap/tests/test_quickstart_sequence.py` (lines 240–251) asserts *prose ==
live* for **two** figures, not one: the module count **and** `'**(\d+)
unfilled block slots**'`. `docs/quickstart.md` line 182 states *"**21 unfilled
block slots**"*. Measured: a real `solo-greenfield` scaffold at clean HEAD
reports exactly `Block slots requiring agent attention (21)`, of which
`AGENTS.md` contributes 4. With A4's fifth slot added, the same scaffold reports
**22**, with `AGENTS.md [cairn:slot security-verification]` in the list.

The tally does **not** come back down when Chunk B fills the slot:
`find_block_slots` counts *open markers* in the written text
(`bootstrap/_scaffold/install.py` line 256), and `print_report` (called at
`bootstrap/_scaffold/cli.py` line 581) runs **before** `run_module_merge_pass`
(line 597). I confirmed 22 in the merged-successfully case too.

Consequences the plan does not carry:
* **Chunk A commits a red suite.** Chunk A's acceptance criteria name only three
  test files, so this would not be noticed until Chunk B — and the plan's
  Sequence section asserts each chunk is a landable commit.
* **Chunk B's acceptance is unachievable as written** (*"`test_quickstart_sequence.py`
  green"*) without also editing `docs/quickstart.md`'s slot count. B3 names only
  *"The `solo-greenfield` count and its enumeration"*.
* Unlike the module count, this figure is **not** order-contended with
  `default-security-stance` (that scope adds no slot), so it is `21 → 22` flatly
  — but it must still be re-measured, not applied from here.

**[I3] The Maintainer fence's frozen-files claim is false: two files this plan
edits ARE frozen.** Fence item 3 states *"No file this plan edits is in the
164-entry `frozen_files` map (measured above), so no `FROZEN-MODIFIED` row is
expected"*. `_frozen_files()` in `bootstrap/tests/_gate_manifest.py` (line 151)
globs `bootstrap/tests/**/*.py`, so **every** test file under `bootstrap/tests/`
is frozen unless cascade/phase-excluded. Direct lookup in the committed
`gate_manifest.json` confirms both of A6/A7 are present:

* `bootstrap/tests/test_security_lint.py` — **FROZEN** (A6 edits it, `44 → 45`)
* `bootstrap/tests/test_notice_install.py` — **FROZEN** (A7 edits it, `44 → 45`)

Two `FROZEN-MODIFIED` HOLDs are **guaranteed**, not contingent. The "measured
above" the fence cites measured six *other* files and never covered these two.
The fence's hedge (*"should be re-checked ... because the map moves"*) frames a
present, measurable fact as a future risk, which is precisely backwards for the
one section whose job is to tell the Maintainer what to expect at the gate.

Mitigating (and worth stating so the severity is not overread): no in-suite test
verifies the committed manifest against the tree — `_gate_manifest.py verify` is
a ceremony/preflight tool, so this surfaces at the Maintainer's gate rather than
as a red suite. That is still exactly where the fence promised nothing would
appear.

Two adjacent facts the Maintainer should have alongside it, neither a HOLD:
* `bootstrap/_scaffold/config.py` is **`cascade_mutable`**, governed by
  *"AST source-motion attest — one predeclared mapping-symbol delta only"*. This
  plan makes **two** symbol changes in that file, only one of which is a mapping
  symbol. `CASCADE-CHANGED` is a note, never a HOLD — but the governance string
  and this plan's delta disagree, and the ceremony is the place to reconcile it.
* The new `templates/modules/default-on/run_security_verification.py` will land
  as `FROZEN-NEW` (a note, allowed) and becomes frozen gate surface thereafter.

**[I4] A4's high-risk-surfaces line lands inside a slot the adopter is told to
replace, so the Security-Review designation does not durably reach adopters.**
A4 promises *"one line in the *Project-specific conventions* guidance naming the
dispatcher, its registry, its child result schema, and every registry entry as
**high-risk Security Review surfaces**"*, and the *Documentation / doctrine
surface* section says the template gains *"in its *high-risk surfaces* guidance,
the dispatcher"*. In `templates/core/AGENTS.md`, `## Project-specific
conventions` (line 250) contains **nothing but** `<!-- cairn:slot
project-conventions -->` (line 252) and a placeholder (lines 253–257) that reads
*"This is judgment work: a reasoning agent and the maintainer write the project's
*real* conventions here"*. There is no non-slot high-risk guidance in that
template to add a line to. A line placed in that placeholder is transient prose
the adopter is instructed to overwrite. Under a security lens this is the
substantive half of [I1]: the module doctrine can be installed correctly and the
adopter's governing document still carries no durable statement that the
dispatcher, its registry and every future registry entry are Security-Review
surfaces. The plan needs to say **where** that designation lives such that it
survives an adopter filling their own conventions — the module's own merge block
and `dev/modules/security-verification.md` are the candidates.

**[I5] Two figures in *The measurement that shapes this plan* do not reproduce.**
The section's authority rests on it being measured rather than carried forward,
so both matter more than their size.
* *"printed 21 `note: NEW …` lines"* — re-run on the same clean-HEAD extraction,
  `verify` prints **61** NEW lines (32 `Import`, 20 `FunctionDef`, 7 `Assign`,
  2 `ClassDef`); non-`Import` is 29. Neither figure is 21. The **conclusion**
  survives intact (NEW is reported, exit 0, `known_new` applies only to
  `update-symbol`, this plan adds no engine symbol). What the corrected figure
  adds is context the plan would want: the baseline pins 174 of ~235 live
  top-level symbols, so the attestation is a **partial** pin, which strengthens
  rather than weakens the plan's argument for the stop-and-explain discipline.
* *"Suite: `1744 passed, 2 failed` in 159.51s"* — re-measured at the same HEAD
  under the canonical interpreter: **`2 failed, 1779 passed` in 160.98s**, same
  two `bootstrap/tests/test_ast_attest.py` node ids. The plan already says to
  re-baseline; the point is that the figure is cited in plan-level acceptance as
  the oracle for *"collection grows by exactly the new nodes and drops none"* and
  is already 35 nodes stale within the same day. Either drop it as an oracle or
  bind it to a commit rather than a date.

Minor, same section: the `_UPDATE_ALLOWLIST` block is presented as `$ grep -n
… -A 6` output but carries no line numbers and re-aligns
`"_CORE_MAPPINGS":   "Assign",` — the source (line 144) has a single space. In a
plan whose evidentiary standard is *quote what you ran*, a hand-tidied block
shown as command output is worth correcting.

**[I6] T10's invalid-JSON row has no perturbation.** T10 specifies two children
(a lone `0x80`, and a bare `{`) and names one perturbation, `errors="replace"`,
which makes only the **invalid-UTF-8** row red. Nothing is named that makes the
**invalid-JSON** row red — the JSON leg of that test is unvalidated by the plan's
own rule. A candidate that targets the hazard: replace the strict `json.loads`
result-handling with a `try/except` that falls through to CLEAN on a parse error.

Related coverage gap, flowing from [I1]: **no test covers the `conflict-deferred`
or `customized` merge outcomes for the new slot**, which — as measured — is the
outcome an adopter actually gets today.

### Covered

Everything in this list was re-measured, not read.

* **AST baseline** — 174 entries; `FunctionDef` 98 / `Assign` 53 / `ClassDef` 10
  = **161** of the three kinds. Exact.
* **Clean-HEAD verify** — `AST attestation OK — 174 baselined symbol(s)
  accounted for, unchanged.`, exit 0. Exact.
* **All four declared digests reproduce byte-exact** —
  `Assign:_MODULE_MAPPINGS` `26957a8924042a0a`;
  `Assign:_DEFAULT_ON_MODULES` `2c8ef688f6865487`;
  `FunctionDef:main` `ff5a7441cceda605`;
  `FunctionDef:format_profile_summary` `830aac8b7c3d1bde`.
* **The load-bearing "no surgical path" finding is CORRECT.**
  `_UPDATE_ALLOWLIST` (lines 141–146) holds exactly the four named symbols;
  `_DEFAULT_ON_MODULES` is absent. `gate_manifest.json`'s `mapping_symbols` holds
  exactly `_CORE_MAPPINGS` / `_MODULE_MAPPINGS` / `_SKILLS_MAPPINGS`.
  `_DEFAULT_ON_MODULES` is in the baseline and in neither. Full supervised
  re-anchor is the only path, and `default-security-stance` does contend for the
  same tuple.
* **Symbol-delta declaration** — 3 CHANGED / 0 NEW / 0 MISSING / 0 DUPLICATE is
  consistent with what the three chunks actually edit. The declared-NOT-changed
  list is sound: no token, no `.gitignore` seed, no supersession, no preset entry,
  and the literal-path-not-`{{token}}` choice does keep `KNOWN_TOKENS` and
  `_REFERENCE_SCRIPT_TOKEN` out of the union.
* **`verify` semantics** — fails on CHANGED / MISSING / DUPLICATE only; NEW is a
  note; `known_new` complete-set matching applies to `update-symbol`, not verify.
* **Install contract** — `scaffold.py --manifest` → **95** data rows (96 lines
  incl. header). `+2 → 97` arithmetic correct; the two destinations
  (the module doctrine substituted, the dispatcher verbatim) match the
  `dev/modules/<name>.md` + `scripts/<script>.py` destination pattern every
  existing default-on module uses; the tab-separated format claim
  matches the emitted header; `duplicate_destinations` exists
  (`bootstrap/_scaffold/config.py` line 615) and is the right check.
* **`InstallSpec`** — `NamedTuple(src, dst, verbatim=False)` at
  `bootstrap/_scaffold/config.py` line 555. A3's proposed spec is well-formed.
  A2 being substituted is **required**, not stylistic: `run_module_merge_pass`
  skips `verbatim` specs outright.
* **The `44` pins and their atomicity argument** — three channels agree at 44
  (`git ls-files`, working-tree glob, manifest `.py` sources).
  `test_templates_py_count_is_pinned` (line 291) pins 44 and its message names
  the sibling *"line 75 as of 2026-08-03"*;
  `test_manifest_has_the_expected_py_source_count` asserts at line 75. The
  "must land in the SAME commit" claim is in the source, not inferred.
* **Release gate** — `PASS`, `Bandit clean over 74 shipped file(s).` Exact. The
  74 → 75 prediction is structurally right: `scan_targets()` derives `templates/`
  targets from registry data, so A3's registration is what makes the dispatcher
  scanned — which independently corroborates the atomicity argument.
* **Prose integrity** — `check_cairn.py` → OK, **180** Markdown files, 68
  external links not probed. Exact.
* **Neutrality** — `fail=95 info=21`. Exact.
* **Registries** — `_DEFAULT_ON_MODULES` 6, `_MODULE_MAPPINGS` 20, `_PRESETS` 3
  (`solo-greenfield`, `collaborative-team`, `high-rigor-legacy`). Exact.
* **`gate_manifest.json`** — 164 `frozen_files`. The six files the plan names as
  not-frozen are all genuinely not frozen. `test_quickstart_sequence.py` is
  frozen **and** derives its expectations live (lines 213–251), so it needs no
  edit — correct, though see [I2] for the doc it reads.
* **First live use of the merge mechanism** — `grep -rn "cairn:merge"
  templates/modules/` returns exactly one hit, a prose mention in
  `templates/modules/default-on/documentation-plan.md` line 92. Correct.
* **The exit ladder is reused, not invented** — `_AGG_CLEAN` 0 / `_AGG_INCOMPLETE`
  5 / `_AGG_FINDINGS` 10 / `_AGG_DEGRADED` 20 at
  `templates/modules/team-gated/run_security_audit.py` lines 75–78.
* **The twin check is discovery-based** — `_self_hosted_twins()`
  (`bootstrap/tests/test_notice_install.py` line 51) enumerates manifest
  destinations and keeps only those that already exist under `scripts/`/`tools/`.
  Declining to self-host is genuinely supported, not a gap.
* **Order-sensitive surfaces all real** — `docs/quickstart.md` line 129 states
  **6** with the `verify:` marker; `docs/solo-legacy-recipe.md` line 58 says *"an
  **8-module roster** — the six default-on modules"*; `templates/modules/README.md`
  lists **4** default-on rows (lines 34–37) against 6 in code. The pre-existing
  drift is correctly named and correctly **not** adopted as scope.
* **B2's doc-governance obligation is real** — `bootstrap/tests/test_doc_governance.py`
  line 285 requires the *"Cairn's own"* link-text prefix on `dev/modules/<name>.md`.
* **C1's precedent exists** — `bootstrap/_scaffold/cli.py` `main` already carries
  `if "issue-capture" in modules:` (564), `if "model-selection" in modules:`
  (624), `if "coordination-tiers" in modules:` (660). C1 is a genuine
  in-pattern addition, not a new mechanism.
* **`bootstrap/SAFETY.md` Rule 7 / Layer-4** exists (line 108 ff.) with a
  documented-residual-risks subsection, so D1 has a real home.
* **Perturbation discipline** — 33 of 35 name a hazard perturbation rather than a
  body edit. T9's refusal to delete `timeout=` (which would hang the suite) and
  T20's explicit *"the hazard is the false-security claim, not the string"* are
  both the right call. T24(b) and T28 declare non-perturbability honestly.
  T15/T13/T14 correctly map to the Decision's three named properties.
* **Scope boundaries** — no sibling scope's surface is absorbed and nothing
  widens past the Decision. Every contended surface (`config.py`,
  `_DEFAULT_ON_MODULES`, the README row, the two doc counts) is named as
  contended. The empty-registry reading is a **narrowing** of the original
  Proposal, argued from Decision ordering plus the admission rule, and flagged
  to the External reviewer as attackable — the right handling.
* **Required checkers, run as instructed, both clean** —
  `claim_check.py` → OK, no flags (19 paths exempted via `claim-check-allow`);
  `check_cairn.py` → OK, 1 Markdown file scanned, no issues.

One soft scope edge, not a numbered concern: **L5** assigns the
`templates/modules/README.md` drift fix to *"whichever cluster scope lands its
README row last"*. A plan cannot bind a sibling scope's commit; that is a
Maintainer routing item. Recording it as a Maintainer-owned handoff rather than
an assignment would keep the fence clean.

### Not covered / low confidence

* **The dispatcher's runtime behavior is unverifiable — no code exists.** T1–T24
  are specifications. I checked their *shape*, their perturbations, and their
  channel independence; I could not check that any of them will hold.
* **The Bandit prediction** (75 files, LOW `B404`/`B603`) cannot be measured
  before Chunk A. The plan already books it as known omission (e).
* **The content-scan probe of the proposed slot text** — I could not reproduce
  it; the exact text is not in the tree. Taken on the plan's word.
* **T29's upgrade paths** — I confirmed `upgrade --plan`'s *"new modules
  available (opt-in)"* emission and the `--adopt-module` wiring exist in
  `bootstrap/_scaffold/upgrade.py`; I did not execute either.
* **Whether the Decision requires `format_profile_summary` at v1** is a
  Decision-reading question, not a measurable one. The plan escalates it as
  strikeable-in-one-line, which is the right disposition; I take no position.
* **Cross-cluster re-anchor sequencing (L7)** — Maintainer-owned. The plan is
  right not to answer it, and I add only the `cascade_mutable` note in [I3].
* **The `_slot_is_empty` docstring/implementation divergence** — I did not check
  whether other slots or modules depend on the docstring's reading. That belongs
  in whatever scope picks it up, not here.

### Recommendation

**Second round required — revise, then take the External security-lens round.**

[I1] and [I2] are measured, reproducible, and block execution as written; [I3]
and [I4] mis-set what the Maintainer and the adopter respectively will get. All
four are plan-text fixes that touch no architecture:

1. **[I1]** — A4 ships the `security-verification` slot **empty** (marker pair
   only); T30/T31 re-specified against the `inserted` outcome; the
   `.cairn-merge-pending` side-file possibility named as a failure mode; the
   `_slot_is_empty` docstring divergence routed out of this scope.
2. **[I2]** — B3 gains `docs/quickstart.md`'s block-slot count as a second
   re-measured figure, and Chunk A's acceptance either runs
   `test_quickstart_sequence.py` or the chunk boundary moves so no commit lands
   red.
3. **[I3]** — fence item 3 rewritten to state the two guaranteed
   `FROZEN-MODIFIED` rows as fact, plus the `cascade_mutable` governance note.
4. **[I4]** — the plan names a durable home for the high-risk-surface
   designation outside the adopter-replaced `project-conventions` slot.
5. **[I5]/[I6]** — correct the two figures and the quoted block; add the
   invalid-JSON perturbation to T10.

After the revision, the **External security-lens round still has to happen** —
by a different agent type or the Maintainer. [I1] in particular is exactly the
class of defect a same-type reviewer nearly missed and only caught by running the
mechanism instead of reading it, which is the argument for the declared tier, not
against it.

---

## Response to plan review -- Claude (author) -- 2026-08-04

**Model**: Claude Opus 5 (`claude-opus-5`), author role, fresh session.

**Standing — this Response discharges nothing.** The plan declares
`required(**External**, security lens)`. The landed review is **Internal**, same
agent type, and says so itself. I am the plan author's own type, so this section
is a *disposition of an Internal round* — not a review, not a second opinion
across structural independence, and not a substitute for the declared tier. The
External security-lens round remains outstanding. See *Does this clear the plan
to implement?* below, which answers **no**.

**What supplies the material for this Response.** Both the plan and its review
were written at HEAD `eacb7dd`. This Response was written 61 commits later; HEAD
moved from `6618e54` through `6b6034e` while it was being written, and
`bootstrap/_scaffold/config.py` has gained 511 lines since `eacb7dd`. **Every
figure below was re-derived against the live tree**, not carried forward from
either artifact. Where a check needed a tree, I named which tree and why:

* **Engine, gate and registry readings** — the live working tree. It carries no
  engine or template modification (only sibling scopes' `dev/plans/*.md` edits),
  so no extraction was needed and none was used.
* **Merge and scaffold behaviour** — four throw-away copies of a `git archive
  HEAD` extraction in the session scratch directory, each carrying one synthetic
  variant of A2/A3/A4/B1. **No repository file was modified.**
* **The historical adjudication of [I5]** — a separate `git archive eacb7dd`
  extraction, so the plan's and the review's competing figures could be settled
  at the commit *they* were measured at rather than argued about.
* **The full suite** — the git repository itself, *not* an extraction. That
  choice is a finding in its own right; see [R3].

### Disposition summary

| # | Finding | Disposition | Mechanical residue |
|---|---|---|---|
| I1 | Slot placeholder makes the merge defer | **Accept with modification** — diagnosis confirmed verbatim; remedy improved and measured | M1, M2, M3, M4, M5, M6 |
| I2 | A second pinned number in `docs/quickstart.md`; Chunk A commits red | **Accept** — confirmed by an executed RED test | M7, M8, M9 |
| I3 | The fence's frozen-files claim is false | **Accept** | M10 |
| I4 | The high-risk designation lands in an adopter-replaced slot | **Accept** | M11, M12 |
| I5 | Two figures do not reproduce; the quoted block is hand-tidied | **Accept**, with both replacement figures re-derived (the review's own are now stale too) | M13, M14, M15, M16, M17 |
| I6 | T10's invalid-JSON row has no perturbation | **Accept** | M18 |
| I6b | No test covers the `conflict-deferred` / `customized` merge outcomes | **Accept with modification** — a test of its own, not a widened T31 | M4 |
| — | Soft edge: L5 assigns a sibling scope's commit | **Accept** | M19 |
| R1 | The AST baseline is 173, not 174 | Author-found | M20 |
| R2 | `Assign:_MODULE_REQUIRED_TOKENS` is not baselined | Author-found | M21 |
| R3 | The full suite must not be measured from an extraction | Author-found | M22 |
| R4 | `check_cairn`'s count is a whole-tree reading, so its criterion is fragile | Author-found | M23 |

No finding is declined.

### The findings, one at a time

**[I1] — ACCEPT WITH MODIFICATION. The diagnosis reproduces verbatim; the
remedy the review proposes is not the cheapest one, and I measured a better.**

The mechanism reading is exactly right. `_slot_is_empty`
(`bootstrap/_scaffold/slotmerge.py`, line 199) is literally `return body.strip()
== ""`, its docstring does say placeholder prose *"is fine (it gets overwritten
on merge)"*, and the two readings contradict each other. `merge_module_into_slot`
inserts only on the empty branch (line 314); a non-empty, non-matching,
non-customized body falls to the conflict branch and the side file.
`run_module_merge_pass` (`bootstrap/_scaffold/install.py`) skips `verbatim`
specs, so A2 being substituted is load-bearing, as the review says.

I reproduced the end-to-end probe with A4's slot, A2's merge directive, A3's
registration and B1's default-on append, installing a real `solo-greenfield`
scaffold into a fresh target. **Placeholder body:**

```
Module-merge pass:
  [conflict-deferred] AGENTS.md > security-verification -> .../AGENTS.md.security-verification.cairn-merge-pending
  [slot-content-stale-or-partial] AGENTS.md > security-verification (fidelity check)
```

Zero occurrences of the standing command in the installed `AGENTS.md`; the side
file present in the adopter root; **exit 0**. Every clause of [I1] reproduces,
including the side file's exact name, which the review did not state.

**Where I diverge.** The review's fix — ship the slot empty — is correct but it
books a cost it does not have to pay: *"That costs the placeholder guidance,
which is a real (small) loss worth stating rather than trading silently."* The
slot **body** is what must be empty; the merge reads only between the marker
pair. Guidance placed **between the `## Security verification` heading and the
`cairn:slot` open marker** is outside the body and survives untouched. Measured,
same probe harness, guidance moved outside the pair:

```
Module-merge pass:
  [inserted] AGENTS.md > security-verification
```

standing command present (1 occurrence), **placeholder guidance retained** (1
occurrence), no side file, no fidelity warning, and the installed file reads:

```
## Security verification

(Filled from the `security-verification` default-on module when installed. …)

<!-- cairn:slot security-verification -->
**Security verification.** … `python scripts/run_security_verification.py local` …
<!-- cairn:end security-verification -->
```

So the amendment is *body empty, guidance above the marker*, and the loss the
review stated is not incurred. I also confirmed the opt-out case: with the module
**not** installed (the exact Chunk-A state), `check_slot_fidelity` emits nothing,
because it only walks merges declared by *installed* modules. Shipping the body
empty therefore costs nothing on the opt-out path either — a fact the fix depends
on and neither artifact had established.

The review's root-cause framing is also correct and is the sharpest thing in it:
the plan took the slot's behaviour from the mechanism's own docstring instead of
running it, which is the artifact under verification supplying the material used
to verify it. That is the failure this round exists to catch, and it was caught.

**[I2] — ACCEPT. Confirmed, and confirmed harder than the review confirmed it.**

Every component reproduces. `bootstrap/tests/test_quickstart_sequence.py` asserts
*prose == live* for two figures — the module count and the block-slot count (the
slot half at lines 242–250, marginally off the review's 240–251).
`docs/quickstart.md` line 182 states `**21 unfilled block slots**`; a clean
`solo-greenfield` scaffold reports exactly 21, of which `templates/core/AGENTS.md`
contributes 4 marker pairs. `find_block_slots` counts open markers in the written
text and `print_report` (`bootstrap/_scaffold/cli.py` line 581) runs **before**
`run_module_merge_pass` (line 597).

The review reasoned that the count does not come back down and that Chunk A would
commit red. I executed both. With the fifth slot present the scaffold reports
**22** in all three states I built: module not installed (Chunk-A state), module
installed and merged (`inserted`), and module installed and deferred
(`conflict-deferred`). Running the real test against a tree in the exact Chunk-A
state — A2/A3/A4 landed, B1 not:

```
FAILED bootstrap/tests/test_quickstart_sequence.py::TestLayerAStepsOneThroughThree::test_step3_install_writes_expected_kernel_and_modules
AssertionError: docs/quickstart.md says '21 unfilled block slots' but the live install reports 22
```

The module-count half stays green at Chunk A (roster still 6), which is why the
two figures need **different chunks**: the slot count moves in Chunk A because A4
moves it, and the module count moves in Chunk B because B1 moves it. The review
proposed folding the slot count into B3; that would leave Chunk A red. The
amendment splits them instead.

**[I3] — ACCEPT. The fence's claim is false and the correction is not
contingent.**

`_frozen_files()` (`bootstrap/tests/_gate_manifest.py`, line 151) globs
`bootstrap/tests/**/*.py` at line 165. Direct lookup in the committed
`bootstrap/tests/fixtures/gate_manifest.json` (164 `frozen_files`, reproducing
exactly) confirms both:

* `bootstrap/tests/test_security_lint.py` — **present in the map** (A6 edits it)
* `bootstrap/tests/test_notice_install.py` — **present in the map** (A7 edits it)

Two `FROZEN-MODIFIED` rows are guaranteed. I also confirmed the review's
mitigation rather than taking it: `bootstrap/tests/test_gate_manifest.py` runs
every one of its verify assertions against a `produced` fixture — a manifest
regenerated in the test — never the committed fixture against the live tree. So
this surfaces at the Maintainer's ceremony gate, not as a red suite. The
`cascade_mutable` note reproduces verbatim: `bootstrap/_scaffold/config.py` is
governed by *"AST source-motion attest — one predeclared mapping-symbol delta
only (A/B/C/E)"*, and this plan declares two symbol changes in that file of which
one is a mapping symbol.

**[I4] — ACCEPT. Measured, and stronger than stated.**

In `templates/core/AGENTS.md` the string "high-risk" occurs **exactly once**, at
line 253 — *inside* the `project-conventions` slot placeholder, in the sentence
that tells the adopter this is judgment work they write themselves. There is no
non-slot high-risk guidance in that template for A4's line to join. A
Security-Review designation placed there is prose the adopter is instructed to
overwrite. The durable homes are the module's own merge block (which, after M1,
lands durably in the adopter's `security-verification` slot and is guarded by
`check_slot_fidelity` against later drift) and `dev/modules/security-verification.md`.
Named residual, since the fix should not be oversold: an adopter who marks the
slot `cairn:customized` opts out of the substring check, and the designation is
then theirs to keep or drop.

**[I5] — ACCEPT, and both of the review's replacement figures are themselves now
stale. Adjudicated at `eacb7dd` so the record is settled rather than argued.**

*NEW-line count.* At `eacb7dd`, from a clean extraction, `verify` prints **61**
`note: NEW` lines — 32 `Import`, 20 `FunctionDef`, 7 `Assign`, 2 `ClassDef`.
**The review's figure is exactly right and the plan's 21 was wrong.** At the live
tree the same command prints **78** (32 `Import`, 24 `FunctionDef`, 18 `Assign`,
4 `ClassDef`). The review's derived observation also checks out and gets stronger:
the baseline pinned 174 of 235 live top-level symbols at `eacb7dd` and pins 173 of
251 now, so the attestation is a partial pin and the stop-and-explain discipline
is doing more work, not less. The conclusion the plan drew from the figure —
`verify` reports NEW, exits 0, `known_new` binds `update-symbol` only, this plan
adds no engine symbol — is unaffected and re-confirmed: live `verify` exits **0**.

*Suite figure.* The plan's `1744 passed, 2 failed` does not reproduce. The
review's `2 failed, 1779 passed` is **unreproducible by construction** — its two
failures were caused by another scope's *uncommitted* edits, which no longer
exist and cannot be reconstructed — so I neither confirm nor dispute it and say
so rather than pretending to have checked. The live figure, run in the repository
under the canonical interpreter: **`1790 passed` in 171.22s, 0 failed, 0 skipped,
0 xfailed.** The plan's plan-level target of 0/0/0 is currently *achievable*,
which is worth recording; its numeric baseline is not, having moved 1746 → 1781 →
1790 collected inside two days. The review's disposition is right: bind it to a
commit or drop it as an oracle.

*The hand-tidied block.* Confirmed. Real `grep -n … -A 6` output carries `141:`
through `146-` prefixes, and line 144 reads `"_CORE_MAPPINGS": "Assign",` with a
single space. The plan's rendering has neither. In a plan whose standard is
*quote what you ran*, that is worth fixing.

**[I6] — ACCEPT on T10. The related coverage gap: ACCEPT WITH MODIFICATION.**

T10's reading is correct: two children, one perturbation, and `errors="replace"`
reds only the UTF-8 row. The invalid-JSON row is unvalidated under the plan's own
rule, and the review's candidate perturbation targets the hazard properly.

On the coverage gap, I accept the substance and change the shape. The review
frames it as widening T31. After M1 the `conflict-deferred` path is no longer the
outcome an adopter gets — but it stays reachable (an adopter who edited the slot
before re-scaffolding, or `.cairn-merge-pending` residue from a prior install),
and it is the path on which the plan's headline deliverable silently does not
land. Folding it into T31 would make one test assert two different outcomes.
It gets its own test, T31b, and the outcome becomes a named failure mode.

**[Soft edge on L5] — ACCEPT.** A plan cannot bind a sibling scope's commit. L5
becomes a Maintainer-owned routing item.

### Author-found, not in the review

**[R1] The AST baseline is 173, not 174.** `bootstrap/tests/fixtures/scaffold_ast_baseline.json`
holds **173** entries at the live tree (`FunctionDef` 98, `Assign` 53, `ClassDef`
10, `Import` 8, plus `Docstring`/`Expr`/`If`/`If#2`). The `Try` entry the plan's
Counter shows is **gone** — a re-anchor landed between `eacb7dd` and now, and it
removed exactly the symbol the plan's second live reading had caught going
MISSING. The plan's derived figure **161 of the three kinds** is unchanged and
reproduces. So does every digit that matters: **all four declared digests
reproduce byte-exact** at the live tree — `Assign:_MODULE_MAPPINGS`
`26957a8924042a0a`, `Assign:_DEFAULT_ON_MODULES` `2c8ef688f6865487`,
`FunctionDef:main` `ff5a7441cceda605`, `FunctionDef:format_profile_summary`
`830aac8b7c3d1bde` — and `_DEFAULT_ON_MODULES` is still in neither
`_UPDATE_ALLOWLIST` (lines 141–146, exactly four symbols) nor `mapping_symbols`
(exactly the three registry mappings). **The plan's load-bearing finding survives
61 commits and a re-anchor intact.** Live `verify` is `AST attestation OK — 173
baselined symbol(s) accounted for, unchanged.`, exit 0, on a tree with no engine
modification — so the plan's two transient CHANGED readings were transient
exactly as it said.

**[R2] `Assign:_MODULE_REQUIRED_TOKENS` is not in the AST baseline** — at
`eacb7dd` or now. It appears as a NEW note. `verify` cannot report a non-baselined
symbol CHANGED, so declaring it "not changed" carries no ceremony meaning and
dilutes a declaration whose whole value is falsifiability. The other eight names
in that sentence are all baselined and the declaration stands for them.

**[R3] The full suite must not be measured from a `git archive` extraction.** I
made this mistake deliberately, following the plan's own scratch-extraction
technique, and it produced **9 false failures and 1 false skip** (`1780 passed, 9
failed, 1 skipped`) against **`1790 passed, 0 failed, 0 skipped`** in the
repository at the same commit. Cause, traced rather than guessed: the extraction
has no `.git`, and `resolve_full_sha("HEAD", repo)` in
`bootstrap/tests/_oracle_trust.py` raises `TrustError` when `git rev-parse`
cannot resolve HEAD. The casualties are `bootstrap/tests/test_oracle.py` (7
nodes), plus one node each in `bootstrap/tests/test_gate_preflight.py`
(`TestPublicCli` > `test_check_runs_against_the_live_repo_and_reports`) and
`bootstrap/tests/test_upgrade_module_additions.py`
(`test_module_additions_under_explicit_to_are_hard_blocked`).
The plan's extraction technique is right for the narrow AST reading it prescribes
it for and **wrong for the suite** — the measurement environment itself became
the contaminant. Plan-level acceptance says the suite is measured *"on a clean
tree"*, which reads either way; it needs disambiguating before an implementing
agent books nine phantom regressions.

**[R4] `check_cairn`'s figure is a whole-tree reading, so Chunk B's criterion is
fragile.** Live: **195** Markdown files, 68 external links not probed — against
the plan's 180 and a Chunk B criterion of `≥ 181`. Worse than staleness: at the
moment of writing, `check_cairn` reports **1 issue**, at
`dev/plans/archive/security-preflight-checklist.md:1747`, in a **sibling scope's
uncommitted edit**. A criterion phrased as *"`check_cairn.py` → OK"* is therefore
falsifiable by work this plan does not own. It needs to be phrased against this
plan's own files.

### Re-measurement ledger

Every figure either artifact states, re-derived. Live values are at HEAD
`6b6034e` unless noted.

| Figure | Plan | Review | Live | Verdict |
|---|---|---|---|---|
| AST baseline entries | 174 | 174 | **173** | Non-reproduction ([R1]) |
| Baseline, three kinds | 161 | 161 | 161 | Reproduces |
| `verify` on a clean tree | OK, 174, exit 0 | same | OK, **173**, exit 0 | Reproduces but for the count |
| `Assign:_MODULE_MAPPINGS` digest | `26957a8924042a0a` | confirmed | `26957a8924042a0a` | Reproduces |
| `Assign:_DEFAULT_ON_MODULES` digest | `2c8ef688f6865487` | confirmed | `2c8ef688f6865487` | Reproduces |
| `FunctionDef:main` digest | `ff5a7441cceda605` | confirmed | `ff5a7441cceda605` | Reproduces |
| `FunctionDef:format_profile_summary` digest | `830aac8b7c3d1bde` | confirmed | `830aac8b7c3d1bde` | Reproduces |
| `_UPDATE_ALLOWLIST` contents / lines | four symbols | lines 141–146 | four symbols, lines 141–146 | Reproduces |
| `mapping_symbols` | three registry mappings | same | same three | Reproduces |
| `note: NEW` lines | 21 | 61 | **61** at `eacb7dd`; **78** live | Review right, plan wrong ([I5]) |
| Baseline coverage of live symbols | — | 174 of ~235 | 235 at `eacb7dd`; 251 live | Reproduces |
| Suite | `1744 passed, 2 failed` | `2 failed, 1779 passed` | **1790 passed, 0 failed, 0 skipped** | Plan non-reproduction; review unreproducible by construction |
| Install manifest data rows | 95 | 95 | 95 | Reproduces |
| `templates/**/*.py`, three channels | 44 / 44 / 44 | confirmed | 44 / 44 / 44 | Reproduces |
| `test_security_lint.py` pin | 44 | line 291 | 44 at line 291 | Reproduces |
| `test_notice_install.py` pin | 44 | line 75 | 44 at line 75 | Reproduces |
| Release gate | `Bandit clean over 74 shipped file(s).` | confirmed | identical, `PASS` | Reproduces |
| `check_cairn` | OK, 180 files, 68 links | 180 | **195** files, 68 links, **1 issue in a sibling's edit** | Non-reproduction ([R4]) |
| Neutrality | `fail=95 info=21`, rc 1 | `fail=95 info=21` | `fail=95 info=21`, rc 1 | Reproduces |
| Registries | 6 / 20 / 3 | confirmed | 6 / 20 / 3, same preset names | Reproduces |
| `gate_manifest.json` `frozen_files` | 164 | 164 | 164 | Reproduces |
| The six files named not-frozen | not frozen | confirmed | none in the map | Reproduces |
| `test_security_lint.py` frozen? | implied no | **yes** | **yes** | Review right, plan wrong ([I3]) |
| `test_notice_install.py` frozen? | implied no | **yes** | **yes** | Review right, plan wrong ([I3]) |
| `config.py` `cascade_mutable` string | — | quoted | verbatim match | Reproduces |
| Committed manifest vs tree, in-suite | — | not verified in-suite | confirmed: `produced` fixture only | Reproduces |
| `_slot_is_empty` | assumed permissive | line 199, `body.strip() == ""` | line 199, `body.strip() == ""` | Review right, plan wrong ([I1]) |
| Placeholder-slot merge outcome | `inserted` implied | `conflict-deferred` + `stale-or-partial`, exit 0 | identical, plus side file `AGENTS.md.security-verification.cairn-merge-pending` | Reproduces |
| Empty-slot merge outcome | — | `inserted`, no warning | `inserted`, no side file, no warning | Reproduces |
| Guidance outside the marker pair | — | not tested | `inserted` **and** guidance retained | New measurement ([I1]) |
| `docs/quickstart.md` module count | 6 | line 129, 6 | line 129, 6 | Reproduces |
| `docs/quickstart.md` slot count | not named | line 182, 21 | line 182, 21 | Reproduces |
| Live slot count, clean tree | not named | 21 (4 from `AGENTS.md`) | 21, 4 marker pairs in the template | Reproduces |
| Live slot count with the new slot | not named | 22, also when merged | **22** in all three states, test RED with the exact message | Reproduces, executed |
| `print_report` before merge pass | not named | 581 before 597 | 581 before 597 | Reproduces |
| High-risk prose in the core template | assumed present | only in the slot placeholder | **one** occurrence, line 253, inside the placeholder | Review right, plan wrong ([I4]) |
| `templates/core/AGENTS.md` claim-check slot | model for A4 | lines 228–234, non-blank | lines 228–234, non-blank | Reproduces |
| `run_module_merge_pass` skips `verbatim` | A2 substituted | required, not stylistic | confirmed in `install.py` | Reproduces |
| Exit ladder constants | reused 0/5/10/20 | lines 75–78 | lines 75–78 | Reproduces |
| `_self_hosted_twins()` discovery-based | yes | line 51 | line 51, discovery-based | Reproduces |
| `cairn:merge` hits under `templates/modules/` | exactly one, prose | line 92 | exactly one, line 92 | Reproduces |
| `docs/solo-legacy-recipe.md` roster line | 8-module / six default-on | line 58 | line 58, verbatim | Reproduces |
| `templates/modules/README.md` default-on rows | four vs six | lines 34–37 | four rows, lines 34–37 | Reproduces |
| `cli.py` in-`main` module blocks | `model-selection` precedent | 564 / 624 / 660 | 564 / 624 / 660 | Reproduces |
| `bootstrap/SAFETY.md` Rule 7 | has a home | line 108 | line 108 | Reproduces |
| `test_doc_governance.py` "Cairn's own" | obligation real | line 285 | test at 282–292; source-side assertion at 226 | Reproduces substantively |
| `InstallSpec` NamedTuple | well-formed | `config.py` line 555 | `config.py` line **627** | Line drift only |
| `duplicate_destinations` | the right check | `config.py` line 615 | `config.py` line **687** | Line drift only |
| `claim_check.py` on this plan | OK | OK, 19 exemptions | OK, **22** exemptions | Verdict reproduces; count does not |
| Content scan of a slot-text candidate | OK, no flags | could not reproduce | `OK -- 1 file(s) scanned; no flags` on a candidate rendering | Mechanism confirmed; the plan's exact text still unverifiable |

### Amendments in force

Superseded text is quoted **verbatim**; the plan's hard line-wrapping inside a
quoted passage is collapsed to single spaces so the passage fits a table cell —
no word is altered. This plan is append-only, so these rows *are* the change:
where a row conflicts with text above, **this table governs**.

| # | Locus | Superseded text (verbatim) | Replaced by |
|---|---|---|---|
| M1 | Chunk A, row A4 | "A new `## Security verification` heading with the `<!-- cairn:slot security-verification -->` / `<!-- cairn:end security-verification -->` pair, placeholder text on the `claim-check` slot's exact model" | A new `## Security verification` heading whose **slot body is empty** — the marker pair with nothing between it. The placeholder guidance is **retained but moved above the open marker**, between the heading and `cairn:slot`, where the merge does not read it. Measured: body-empty + guidance-outside yields `[inserted]`, the standing command in the installed `AGENTS.md`, the guidance retained, no side file, no fidelity warning. A non-empty body yields `conflict-deferred` and the rule never reaches the adopter. |
| M2 | Chunk B, T30 | "`test_installed_AGENTS_md_carries_the_exact_standing_command` — a real scaffold; the installed `AGENTS.md` contains the exact two-sentence rule between the slot markers." | Same assertion, plus: the merge pass reports the outcome token **`inserted`** for `AGENTS.md > security-verification`, and **no** `AGENTS.md.security-verification.cairn-merge-pending` file exists anywhere in the target root. Second perturbation added alongside the deletion mutant: **restore non-empty prose to the slot body** — outcome flips to `conflict-deferred`, the rule is absent, the side file appears, and the scaffold still exits 0. That second perturbation is the one that would have caught [I1]. |
| M3 | Chunk B, T31 | "`test_the_merge_pass_reports_the_fill_and_the_fidelity_check_is_clean` — the install's *Module-merge pass* output names `AGENTS.md > security-verification`, and `check_slot_fidelity` returns no warning." | Assert the **outcome token**, not the slot name: `conflict-deferred` also names the slot, so naming alone is a vacuous assertion. Require `[inserted]`, and `check_slot_fidelity` returning no warning **for this slot specifically**. |
| M4 | Chunk B, new test T31b | *(addition)* | `test_a_prefilled_slot_defers_to_a_side_file_and_warns` — install into a target whose `security-verification` slot body already carries adopter prose; assert outcome `conflict-deferred`, the `.cairn-merge-pending` side file present and named for the slot, a `slot-content-stale-or-partial` fidelity warning, exit 0, and the standing command **absent** from `AGENTS.md`. Perturbation: make `_slot_is_empty` treat any body as empty; the side-file and warning assertions go red. Discharges the review's [I6] coverage gap without overloading T31. |
| M5 | *Author-accounting* > *Failure modes* | *(addition)* | A non-empty `security-verification` slot body at install time → the module's contributed rule is **not** merged; it is written to `AGENTS.md.security-verification.cairn-merge-pending` in the adopter root, `check_slot_fidelity` warns `slot-content-stale-or-partial`, and the scaffold **exits 0**. The side file is not a manifest row, so the `+2` install-contract accounting does not see it. T30, T31b. |
| M6 | *Lasting-truth migration*, new row L8 | *(addition)* | `_slot_is_empty`'s docstring in `bootstrap/_scaffold/slotmerge.py` asserts placeholder prose "gets overwritten on merge"; the implementation refuses it. **Routed out of this scope** as a trivial-triage fix in its own commit. Not smuggled in here, and not this plan's to make. |
| M7 | Chunk A, new row A8 | *(addition)* | `docs/quickstart.md` — the **block-slot count** (`**21 unfilled block slots**`). It moves in **Chunk A**, because A4 is what moves it: measured 21 → 22 with the fifth slot, in the module-not-installed, merged, and deferred states alike. Unlike the module count this figure is not order-contended with `default-security-stance` (that scope adds no slot) — but **re-measure and do not apply the number written here**. |
| M8 | Chunk A, acceptance criteria, first bullet | "`~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_security_verification.py bootstrap/tests/test_security_lint.py bootstrap/tests/test_notice_install.py -q` → all pass, 0 skipped." | The same command with **`bootstrap/tests/test_quickstart_sequence.py` added**. Without it Chunk A lands a red commit: executed at the exact Chunk-A state, `test_step3_install_writes_expected_kernel_and_modules` fails with *"docs/quickstart.md says '21 unfilled block slots' but the live install reports 22"*. |
| M9 | Chunk B, row B3 | "`docs/quickstart.md` \| The `solo-greenfield` count and its enumeration. **Re-measure; do not apply a number from this plan** — see *Order-independence*." | Scoped to the **module** count and its enumeration only; the block-slot count is A8's, in Chunk A. Re-measure rule unchanged and it now applies to both figures in their own chunks. |
| M10 | *Maintainer fence*, item 3 | "**The gate-manifest re-pin.** No file this plan edits is in the 164-entry `frozen_files` map (measured above), so no `FROZEN-MODIFIED` row is expected — but `bootstrap/tests/test_security_lint.py` and `bootstrap/tests/test_notice_install.py` carry the two `44` pins and **should be re-checked against the map at implementation**, because the map moves." | **Two `FROZEN-MODIFIED` rows are guaranteed, not contingent**: `bootstrap/tests/test_security_lint.py` (A6) and `bootstrap/tests/test_notice_install.py` (A7) are both in the 164-entry map, because `_frozen_files()` globs `bootstrap/tests/**/*.py`. The "measured above" reading covered six *other* files and never these two. Both are expected HOLDs at the ceremony; the implementing agent **records** them and does not re-pin. Adjacent, neither a HOLD: `bootstrap/_scaffold/config.py` is `cascade_mutable`, governed by *"AST source-motion attest — one predeclared mapping-symbol delta only (A/B/C/E)"*, and this plan changes two symbols there of which one is a mapping symbol — reconcile at the ceremony. The new `templates/modules/default-on/run_security_verification.py` lands `FROZEN-NEW` (a note). Mitigation, stated so severity is not overread: no in-suite test compares the committed manifest against the tree, so this surfaces at the Maintainer's gate rather than as a red suite. |
| M11 | Chunk A, row A4 | "Plus one line in the *Project-specific conventions* guidance naming the dispatcher, its registry, its child result schema, and every registry entry as **high-risk Security Review surfaces**." | **Struck.** `templates/core/AGENTS.md` has no non-slot high-risk guidance to join — the only occurrence of "high-risk" is inside the `project-conventions` slot placeholder the adopter is told to overwrite. The designation moves to **A2's merge-content block** (so it lands durably in the adopter's `security-verification` slot and is guarded by `check_slot_fidelity`) **and to `dev/modules/security-verification.md`** (B2). Named residual: an adopter who marks the slot `cairn:customized` opts out of the substring check. |
| M12 | *Documentation / doctrine surface*, first bullet | "**Governing layer, adopter-facing — yes.** `templates/core/AGENTS.md` gains one slot and, in its *high-risk surfaces* guidance, the dispatcher." | `templates/core/AGENTS.md` gains **one slot and its above-marker guidance, and nothing else**. It carries no high-risk-surfaces guidance for the dispatcher to join; that designation is A2's and B2's, per M11. |
| M13 | *The measurement that shapes this plan* | "**174 baseline entries; 161 of the three kinds** (`FunctionDef` 98 + `Assign` 53 + `ClassDef` 10). Measured, not carried forward." | 174 at `eacb7dd`; **173** at `6b6034e` — a re-anchor landed between and removed the `Try` entry, the same symbol this plan's second live reading caught going MISSING. **161 of the three kinds is unchanged**, and all four declared digests still reproduce byte-exact. Re-measure at implementation; the count moves with the cluster. |
| M14 | *New symbols are not gated; changed ones are* | "confirmed by the clean-HEAD run above, which printed 21 `note: NEW …` lines and still exited 0" | **61** NEW lines at `eacb7dd` (32 `Import`, 20 `FunctionDef`, 7 `Assign`, 2 `ClassDef`); **78** at `6b6034e`. The plan's 21 was wrong; the review's 61 was right for its commit and is now stale. The conclusion is unaffected and re-confirmed at exit 0. Context the corrected figure adds: the baseline pins 173 of 251 live top-level symbols, so the attestation is a **partial** pin. |
| M15 | *Everything else, dated* | "* **Suite**: `1744 passed, 2 failed` in 159.51s — the two failures are exactly the AST-attest pair above, caused by the concurrent uncommitted engine edits, **not** by anything at HEAD. Re-baseline against a clean tree at implementation." | Live: **`1790 passed` in 171.22s, 0 failed, 0 skipped**, in the repository at `6b6034e` with no engine modification in the tree. Collected node count has moved 1746 → 1781 → 1790 in two days, so **this figure is retired as an oracle**: the plan-level criterion *"collection grows by exactly the new nodes and drops none"* binds to a count re-taken at the implementing commit, not to any number written here. |
| M16 | *Everything else, dated* | "* **Prose integrity**: `python scripts/check_cairn.py` → OK, **180** Markdown files, 68 external links not probed." | Live: **195** Markdown files, 68 external links not probed. The count grows with every plan committed and is not this plan's to predict. |
| M17 | *The symbol this plan changes has no surgical path* | the `$ grep -n "_UPDATE_ALLOWLIST" -A 6 bootstrap/tests/_ast_attest.py` block, including the line `    "_CORE_MAPPINGS":   "Assign",` | The block is presented as command output but carries no line-number prefixes and re-aligns one line. Real output prefixes `141:` through `146-`, and line 144 reads `"_CORE_MAPPINGS": "Assign",` with a single space. Re-paste verbatim or drop the `$ grep -n` framing. The four-symbol content and the absence of `_DEFAULT_ON_MODULES` reproduce exactly and are unaffected. |
| M18 | Chunk A, T10 | "Decode with `errors=\"replace\"`. The invalid-UTF-8 row now parses and reaches CLEAN. Fails." | **One perturbation per row.** (a) invalid-UTF-8 row: decode with `errors="replace"` — the row parses and reaches CLEAN. (b) invalid-JSON row: replace the strict `json.loads` result handling with a `try` / `except` that falls through to CLEAN on a parse error. Without (b) the JSON leg is unvalidated under this plan's own rule. |
| M19 | *Lasting-truth migration*, row L5 | "A **trivial-triage fix** by whichever cluster scope lands its README row last, recorded in that commit body. It needs no proposal; it needs an owner, and the last row-adder is the natural one." | **Maintainer-owned routing item.** A plan cannot bind a sibling scope's commit. This plan surfaces the drift and proposes the last row-adder as the natural owner; assigning it is the Maintainer's. |
| M20 | *This plan's declared symbol delta* | "Measured against `bootstrap/tests/fixtures/scaffold_ast_baseline.json` at HEAD `eacb7dd`. **3 CHANGED, 0 NEW, 0 MISSING, 0 DUPLICATE.**" | The delta and all four digests re-verify at `6b6034e` against a **173**-entry baseline. The declaration stands unchanged; only the baseline size moved. Re-measure at implementation and report the baseline size alongside the delta, since the cluster re-anchors it. |
| M21 | *This plan's declared symbol delta* | "Also declared **not** changed: `FunctionDef:install_manifest`, `FunctionDef:install_modules`, `FunctionDef:write_install_lockfile`, `Assign:KNOWN_TOKENS`, `Assign:_MODULE_REQUIRED_TOKENS`, `Assign:_REFERENCE_SCRIPT_TOKEN`, `Assign:_GITIGNORE_SEEDS`, `Assign:_MODULE_SUPERSEDES`, `Assign:_PRESETS`." | **Strike `Assign:_MODULE_REQUIRED_TOKENS`** — it is not in the AST baseline at `eacb7dd` or now, so `verify` reports it as NEW and can never report it CHANGED. Declaring a non-baselined symbol "not changed" carries no ceremony meaning and weakens a declaration whose value is falsifiability. The other eight are baselined and the declaration stands for them. |
| M22 | Plan-level acceptance, first bullet | "**measured on a clean tree after the Maintainer's re-anchor**" | **A clean *working tree in the git repository*** — never a `git archive` extraction. Measured: an extraction yields 9 false failures and 1 false skip, because it has no `.git` and `resolve_full_sha("HEAD", …)` in `bootstrap/tests/_oracle_trust.py` raises `TrustError`; the casualties are `bootstrap/tests/test_oracle.py` (7 nodes), plus one node each in `bootstrap/tests/test_gate_preflight.py` (`TestPublicCli` > `test_check_runs_against_the_live_repo_and_reports`) and `bootstrap/tests/test_upgrade_module_additions.py` (`test_module_additions_under_explicit_to_are_hard_blocked`). The extraction technique in *Verification* stays correct **for the AST reading it is prescribed for** and is wrong for the suite. |
| M23 | Chunk B, acceptance criteria | "* `python scripts/check_cairn.py` → OK; **≥ 181** Markdown files (180 + B2), and the count may only grow." | `check_cairn` is a whole-tree reading, so a bare "→ OK" is falsifiable by a sibling scope's uncommitted edit — it reports 1 issue today, in `dev/plans/archive/security-preflight-checklist.md`, which this plan does not own. Criterion becomes: **no `check_cairn` issue is attributed to a file this plan edits**, and the Markdown-file count is re-measured at the implementing commit rather than predicted (195 at `6b6034e`, +1 for B2). |

Nothing in this table changes the architecture the Decision accepted, adds a
registry entry, widens the empty-registry contract, moves a Maintainer fence, or
takes on a sibling scope's surface.

### What this Response does not settle

* **The dispatcher's runtime behavior.** No code exists. T1–T35 remain
  specifications; the review checked their shape and could not check that any of
  them will hold, and neither could I.
* **The Bandit prediction** (75 files, LOW `B404`/`B603`). Unmeasurable before
  Chunk A. Booked as known omission (e) and it stays booked.
* **The proposed slot text's content-scan result.** The plan's exact text is not
  in the tree. I scanned a plausible rendering of the merge block — `OK -- 1
  file(s) scanned; no flags` — which establishes the mechanism accepts text of
  this shape, not that the plan's text passes. Re-run over the real file at A2.
* **Whether the Decision requires `format_profile_summary` at v1.** A
  Decision-reading question. The plan escalates it as strikeable in one line;
  I take no position, and neither did the review.
* **Cross-cluster re-anchor sequencing (L7).** Maintainer-owned. Unchanged by
  this Response except that M10 gives the ceremony two more facts to work from.
* **Whether the review's `1779 passed` was right at `eacb7dd`.** Unreproducible
  by construction; I decline to assert either way.

### Does this Response clear the plan to implement?

**No.**

The declared tier is `required(**External**, security lens)`. What is in the tree
is an **Internal** round and this **author's Response** to it. Both are the same
agent type as the plan's author, and neither has the structural independence the
tier is defined by. **The External security-lens round is undischarged**, and
under the plan's own standing rule — *"No implementation commit lands before the
`## Plan review` section is in the tree"*, read with its brief, which says an
Internal round does not discharge the tier — **no implementation commit may
land.**

What remains, in order:

1. **The External security-lens round**, by a different agent type or the
   Maintainer. This is the gate. [I1] is the argument for it: a defect in the
   headline deliverable that a same-type reviewer caught only by *running* the
   mechanism rather than reading it, on a plan that had measured everything else.
2. **Two Maintainer calls surfaced and not decided here** — listed in the
   handoff, not silently resolved: whether M1's above-marker guidance is
   acceptable in `templates/core/AGENTS.md`, and whether the two guaranteed
   `FROZEN-MODIFIED` rows change the ceremony's shape.
3. **The AST re-anchor ceremony**, unchanged and still the Maintainer's, over a
   union the Maintainer forms — now against a **173**-entry baseline.

The amendments above make the plan *executable-as-written* once the tier is
discharged. They do not discharge it, and this Response claims no tier
satisfied.

## Plan review -- Codex (External, security lens) -- 2026-08-05

**Verdict: REVISE.** I support the narrow activation-v1 posture: an empty,
source-owned registry that reports `NOT APPLICABLE` is materially safer than a
dispatcher that derives runnable paths from profiles or policy. The current
parent-computed binding needs one explicit extension before capabilities using
adopter-owned policy can be admitted.

**[E1] The binding contract has no defined living-policy mode.** T17 correctly
requires a runner/policy digest mismatch to degrade, yet the API/web capability
plan identifies a legitimate policy record whose content is expected to change
locally. A generic "skip the policy digest" would turn a mandatory binding into
an unreviewed exception. Amend the registry schema with a closed binding mode
(for example, immutable policy hash versus explicitly living policy), define the
fields and failure behavior for each, and test that an entry cannot silently
change modes, omit the required binding fields, or treat a living policy as an
immutable one. This amendment must land here before a capability registry entry
can land there.

**[E2] The initial `NOT APPLICABLE` result must remain non-evidence in every
surface.** T33/T34 cover the installed command and forbid green-security words,
which is good. Add the same assertion to the module documentation and
machine-readable output: an empty registry must expose an explicit
`not_applicable` state and zero evidence count, not a generic exit-0 success
that downstream automation can mistake for a passing security check.

**[E3] High-risk registration must survive the normal customized-slot path.**
M11 moves the designation into merge content and module doctrine, while an
adopter-customized slot deliberately bypasses the slot substring check. The
module doctrine is a useful record but does not necessarily trigger the
project's review routing. State an installer-visible, non-customizable registry
or lockfile marker for this dispatcher/registry schema, or explicitly make
customization refuse an activation upgrade until the Maintainer re-acknowledges
the high-risk surface. A user-authored slot must not silently erase the review
trigger for future registry changes.

I inspected the dispatcher/registry contract, the parent-binding tests T17--T19,
the empty-registry end-to-end path, and amendments M10--M12. I did not run a
candidate dispatcher because it does not exist yet.

## Response to plan review -- Claude (author) -- 2026-08-05

**Model**: Claude Opus 5 (`claude-opus-5`), author role, fresh session.

**Standing — this Response discharges nothing, and a REVISE is not an
approval.** The plan declares `required(**External**, security lens)`. That
round has now been **held**: a `## Plan review -- Codex (External, security
lens) -- 2026-08-05` section is in the tree at `d66be06`. Its verdict is
**REVISE**, and an author's Response does not convert a REVISE into a SHIP. The
sibling artifact `review-gate-enforcement` exists precisely because this tree's
review-before-implement gate is satisfied by section *kind* and never reads a
verdict; its own External reviewer wrote the sentence that governs here — *"I
treated the authored Response as evidence of intended changes, not a
replacement for the plan's executable contract."* This section therefore
records dispositions and lands mechanical amendments; it does not clear the
plan. See *Does this Response clear the plan to implement?* below, which
answers **no**, and *Gate audit* below it, which says exactly which gates are
open.

**Where the review sits in the file.** It was **appended at the end**
(`d66be06`, one file changed, `40 insertions(+)`, no deletions; the hunk
header is `@@ -1773,3 +1773,43 @@`, i.e. entirely after the file's last
line), not inserted before the Internal sections. I checked rather than assumed; the file
order is now plan body → Internal review (2026-08-04) → author Response
(2026-08-04) → External review (2026-08-05) → this section.

**What supplies the material for this Response.** The plan was written at HEAD
`eacb7dd`; the Internal round and the first Response at `eacb7dd` / `6b6034e`.
This Response is written at HEAD **`6bcd2d3`**, **97 commits** after `6b6034e`.
**Every figure below was re-derived at `6bcd2d3`**, none carried forward from
the plan, the Internal review, the first Response, or the External review:

* **Engine, gate, registry and document readings** — the live working tree,
  which carries **no** tracked modification (`git status --short` shows only
  untracked sibling-agent artifacts), so no extraction was needed and none was
  used for these.
* **Merge, fidelity, scaffold and integrity behaviour** — five throw-away
  targets and one `git archive HEAD` extraction in the session scratch
  directory. **No repository file was modified**, before or during; verified
  with `git status --short` after the last probe.
* **The full suite** — the git repository itself, never an extraction, per M22.

**One process note, recorded because it nearly cost measurements.** The session
scratch directory was **deleted underneath this session mid-run** by concurrent
work; the first suite run and the first integrity probe were lost with it. Both
were re-run in a uniquely-named directory. Nothing in this Response rests on a
reading taken before that event.

### Disposition summary

| # | Finding | Disposition | Mechanical residue |
|---|---|---|---|
| E1 | The binding contract has no defined living-policy mode | **Accept** — the premise reproduces from two independent directions and the schema lands here | M24, M25, M26, M27, M28, M29 |
| E2 | The initial `NOT APPLICABLE` result must remain non-evidence in every surface | **Accept with modification** — the machine half is partly already carried by T20/T21, which the review did not cite; the documentation half and the end-to-end half are real gaps | M30, M31, M32, M33 |
| E3 | High-risk registration must survive the normal customized-slot path | **Accept** on the first branch of the reviewer's disjunction; **decline** the second branch, with reasons | M34, M35, M40 |
| R5 | The schema already carries an **undeclared** third policy mode, reachable by `policy_repository_path = None` | Author-found, exposed by E1 | M24, M26 |
| R6 | The release gate's Bandit baseline is **76**, not 74; the plan's `75` and the first Response's "identical" both fail | Author-found | M36 |
| R7 | `check_cairn`'s file count is **176**, not the 180 the plan states or the 195 M23 states | Author-found | M37 |
| R8 | The suite is **1959 passed**, not 1790 | Author-found | M38 |
| R9 | The plan's test-inventory line still says `T1–T35` after two rounds of additions | Author-found | M39 |

No finding is declined in whole. One branch of E3's stated disjunction is
declined and the reason is given.

### The findings, one at a time

**[E1] — ACCEPT. The premise reproduces from two independent directions, and
the schema lands in this plan, not as prose about a schema.**

The reviewer's premise is that a legitimate capability policy record is
expected to change locally, which a mandatory digest binding cannot survive.
I did not take that on the review's word, and I did not take it from the
sibling plan's summary of itself either. Re-derived at `6bcd2d3`:

* `bootstrap/_scaffold/lockfile.py` line 84 defines
  `_LIVING_STATE_DSTS` as a five-entry `frozenset`
  (`dev/PLANNING.md`, `dev/NEXT_SESSION.md`, `dev/.cairn/cairn_foldback.md`,
  `dev/collaboration_agreement.md`, `dev/.cairn/model-selection-mapping.yml`).
* `bootstrap/_scaffold/install.py` line 1634 sets `rec["living_state"] = True`
  **after** line 1629 has already written `"hash": "sha256:" + …`. So a
  living-state record **still carries a hash**. A dispatcher comparing that
  hash against a correctly-filled policy does not get a no-op; it gets a
  **guaranteed mismatch on every correct install**. That is the mechanical
  fact the whole finding turns on, and it is in the engine, not in either plan.
* `bootstrap/verify_integrity.py` lines 96–105 honour the flag **only** for the
  authoritative set and treat it as tamper anywhere else — *"a record outside
  it that carries ``living_state: true`` is a tamper attempt … and fails
  closed"*. Executed on a real install: clean tree → `verify_integrity: OK --
  55 recorded file(s) match … (4 adopter-authored living-state file(s) …)`,
  exit 0.
* The sibling artifact reaches the same place from the other side.
  `dev/plans/api-web-security-modules.md` carries **AM13** (*"The accepted
  activation contract does move, and this plan cannot move it alone … The
  dispatcher must explicitly skip living-state records. That is the activation
  scope's logic"*), **AM15** (Chunk G gated on *"the AM13 cross-scope amendment
  … has landed"*, blocking regardless), and its own External **[E1]** demanding
  the amendment *"be specified and reviewed in `security-verification-
  activation`, not implemented as a local exception in Chunk G"*.

So two External security-lens reads, on two plans, name **this artifact** as
the owner. The finding is accepted without qualification, and the schema is
written into the amendments table rather than described here.

**What accepting it costs, stated rather than absorbed.** A `living_state`
binding mode **narrows** the parent-computed apparatus binding that the
proposal's revision established and the Decision accepted. That is not an
author's to change on a reviewer's say-so. The amendment therefore lands
**with a gate**: the schema and its tests land here (the registry is empty at
v1, so no mode is exercised), and **no entry may be admitted under
`policy_binding_mode: living_state` until the Maintainer ratifies the
narrowing** (M29). This is the difference between specifying a contract and
changing one.

**[R5], which E1 exposed and neither artifact names.** The current schema
already contains an **undeclared third mode**. `policy_repository_path` is
typed `| None`; T5 requires the *field* to be present but nothing constrains
its value, and no test covers the `None` case. So an entry that simply omits a
policy path skips policy binding entirely, with no declaration, no test, and
nothing distinguishing *"this capability has no policy"* from *"this
capability's policy is unbound"*. E1's closed mode set fixes this as a side
effect only if the mode is made **mandatory and total**, which is why M24
requires `policy_binding_mode: "none"` and `policy_repository_path is None` to
imply each other, refusing at construction otherwise.

**[E2] — ACCEPT WITH MODIFICATION. Two of the three surfaces the review names
are real gaps; the third is already carried by tests the review did not cite,
and I say so rather than claiming credit for closing something already closed.**

The review writes: *"T33/T34 cover the installed command and forbid
green-security words, which is good."* That is accurate for what T33 and T34
do. But the dispatcher-output half of the ask is carried by **T20 and T21**,
which the review does not mention:

* T20 already requires *"machine result `aggregate: NOT_APPLICABLE`, `legs:
  []`, a non-empty `reason`"*.
* T21 already scans *"human **and** machine output"* for `CLEAN`, `secure`,
  `passed security`, `no vulnerabilities`, `verified`.

Reported plainly: the review's characterisation of the coverage understates the
plan by two tests. That does not save the finding — three things it asks for
are genuinely absent:

1. **An explicit state field, not an inferred one.** `aggregate:
   NOT_APPLICABLE` makes downstream automation string-match an aggregate label;
   `legs: []` makes it infer a count from a container length. The review asks
   for *"an explicit `not_applicable` state and zero evidence count"*, and this
   tree already has the shape: `bootstrap/tests/_oracle.py` line 473 returns
   `{"schema": REPORT_SCHEMA, "status": "not_applicable", "ok": True, "reason":
   …}` and `bootstrap/tests/test_oracle.py` line 148 asserts `report["status"]
   == "not_applicable" and report["ok"] is True`. The dispatcher should reuse
   that shape, not invent one (M30).
2. **The end-to-end path asserts none of it.** T33 is the only test that runs
   the dispatcher **through its public subprocess path from a real scaffold**,
   and it asserts exactly *"exit `0` and the exact `NOT APPLICABLE` line"*. The
   machine fields are asserted only in-process by T20. The review's instinct to
   cite T33 was right: that is the surface where a generic exit-0 would in fact
   be all an adopter's automation sees (M31).
3. **The module documentation says none of it, and no test reads it.** A2's
   content list names the registry rules, the admission rule, the ladder,
   trusted-checkout scope, the local/deployed non-claim and INCOMPLETE /
   DEGRADED recovery. It does **not** name `NOT_APPLICABLE` at all. The plan's
   *glossary* carries the non-evidence property — that is deliberation-layer
   text an adopter never receives (M32, M33).

**[E3] — ACCEPT, taking the first branch of the reviewer's disjunction.
Measured; the silent-erasure path is worse than the review states, and the
second branch is declined with reasons.**

The review's mechanism reading is correct and I executed it rather than reading
it. Driving `merge_module_into_slot` and `check_slot_fidelity` directly against
three slot bodies, with the designation sentence as merge content:

```
empty          status=inserted             cmd=True  highrisk=True  side=[]
customized     status=customized           cmd=False highrisk=False side=[]
adopter-prose  status=conflict-deferred    cmd=False highrisk=False side=['AGENTS-adopter-prose.md.security-verification.cairn-merge-pending']
```

```
empty          fidelity warnings=[]
customized     fidelity warnings=[]
adopter-prose  fidelity warnings=[('AGENTS-adopter-prose.md', 'security-verification', 'stale-or-partial')]
```

**The `customized` row is the finding, and it is worse than `conflict-deferred`.**
A deferred slot at least leaves a `.cairn-merge-pending` side file and a
`stale-or-partial` fidelity warning. A customized slot leaves **nothing**: the
designation is absent, no side file exists, and `check_slot_fidelity` returns
an **empty list**. `_slot_is_customized` (`bootstrap/_scaffold/slotmerge.py`
line 206) drives both — `merge_module_into_slot` returns `customized` and
preserves the adopter's content (line 312), and the fidelity walk `continue`s
past it (line 379). So M11's *"guarded by `check_slot_fidelity`"* is true for
one of the three reachable body states and false for the one an adopter
deliberately opts into. The residual M11 named was real; its severity was
understated.

**The first branch — an installer-visible, non-customizable marker — already
exists and this plan already installs two of them.** Measured on a real
`solo-greenfield` install from the repository:

* Clean install → `verify_integrity: OK -- 55 recorded file(s) match
  dev/.cairn/cairn-lock.yml (4 adopter-authored living-state file(s) tracked
  for upgrade but excluded from the tamper check).`, **exit 0**.
* Append one line to `dev/modules/claim-check.md` (the exact structural
  stand-in for B2's `dev/modules/security-verification.md`) →
  `modified (hash mismatch): dev/modules/claim-check.md`, **exit 1**.
* Append one line to `scripts/claim_check.py` (the structural stand-in for the
  verbatim dispatcher) → **both** rows reported, **exit 1**.
* Confirmed by reading the lockfile of that install: the four `living_state:
  true` records are the four authoritative adopter-authored files; **no
  `dev/modules/*.md` record and no `scripts/*.py` record carries the flag**, so
  both are inside the tamper check by construction, not by choice.

So the durable home for the designation is **three channels, two of them
tamper-evident**: A2's merge block (customizable — the residual), B2's
`dev/modules/security-verification.md` (lockfile-recorded, non-living-state),
and the **dispatcher source itself** (verbatim, hash-pinned, and additionally
flagged `locally-modified` by `classify_verbatim`
(`bootstrap/_scaffold/lockfile.py` line 287), which never clobbers a fork).
The third is the strongest
because it puts the designation in **the same file as the registry it
designates**: a registry change and the designation are then one reviewed
artifact, which is precisely the review trigger E3 says must not be erasable
(M34).

**The second branch is declined, and here is why.** The review offers *"or
explicitly make customization refuse an activation upgrade until the Maintainer
re-acknowledges the high-risk surface."* That is new engine mechanism in
`bootstrap/_scaffold/slotmerge.py` and/or `bootstrap/_scaffold/upgrade.py`.
Three reasons, none of them "it is inconvenient":

1. It changes the behaviour of `<!-- cairn:customized -->` for **every** slot
   and **every** module, not just this one. That marker is an accepted
   disposition in its own right (the module docstring at
   `bootstrap/_scaffold/slotmerge.py` lines 62–63 records it as "Antigravity
   P2"), and re-opening it from inside a capability-activation
   plan is exactly the cross-scope contract narrowing E1 is being accepted to
   *stop* happening.
2. It enlarges this plan's declared symbol delta beyond the three symbols the
   Maintainer's re-anchor union is formed against, into a second engine file no
   cluster scope has declared. The whole cluster section exists to prevent that.
3. Neither `slotmerge.py` nor `upgrade.py` is in `gate_manifest.json`'s
   `frozen_files` map today (re-checked: 164 entries), so the change would land
   with no gate noticing — the opposite of what the finding wants.

It is a legitimate improvement and it needs its own proposal. Routed to
*Lasting-truth migration* as L9 (M40), and the residual is **pinned by a
characterization test** (T43 in M34) rather than left as prose, so a future
author who closes it has a red test to turn green.

### Author-found, not in the review

**[R6] The release gate's Bandit baseline is 76, not 74.** Live at `6bcd2d3`:
`security_check: Bandit clean over 76 shipped file(s).` → `security_check: PASS
-- release security gate clean.` The plan states 74 and predicts **75** after
Chunk A, in two places; the first Response's re-measurement ledger recorded the
74 reading as *"identical"* and it no longer is. The prediction's *arithmetic*
is unaffected — the dispatcher adds exactly one scanned file — so the criterion
becomes **76 → 77**, and it must be re-taken at the implementing commit rather
than fixed at 77 (M36).

**[R7] `check_cairn` reports 176 Markdown files, not 180 and not 195.** Live:
`check_cairn: OK -- 176 Markdown file(s) scanned; no issues; 48 external
link(s) not probed.` Both figures have moved: files 180 → 195 → **176**,
external links 68 → **48**. The cause is traceable and it is **not** a change
to the checker — `f897cda`, which makes `check_cairn` skip `dev/**/archive/`
by default, is an ancestor of `6b6034e` as well as of `6bcd2d3`, so the same
rule was in force for both readings. What moved is the *population*: 14
proposals were archived between the two commits, and archived sources are
skipped. So the count moves **in both directions** with work this plan does
not own. This *strengthens* M23
rather than replacing it: the criterion stays "no issue attributed to a file
this plan edits", and the figure is now recorded as unpredictable rather than
merely stale (M37). Worth recording alongside: the one `check_cairn` issue M23
cited in a sibling's uncommitted edit is **gone** — the tree is clean today.

**[R8] The suite is 1959 passed, 0 failed, 0 skipped** in 307.28s at `6bcd2d3`,
under the canonical interpreter with `PYTHONDONTWRITEBYTECODE=1`, run in the
repository. Collected node count has now moved 1744 → 1779 → 1790 → **1959**
across four readings in two days. M15 already retired this figure as an oracle;
this reading confirms the retirement was right rather than cautious (M38).

**[R9] The plan's own test inventory is two rounds stale.** Plan-level
acceptance says *"`bootstrap/tests/test_security_verification.py` — T1–T35"*.
The first Response added T31b (M4); this one adds T36–T43. A test-file
inventory that under-states its own contents is the cheapest possible way for a
new test to be quietly dropped at implementation (M39).

### Re-measurement ledger

Every figure the External review states, every figure this Response asserts,
and every figure the plan and the first Response state that this Response
relies on. Live values are at HEAD **`6bcd2d3`**, canonical interpreter,
`PYTHONDONTWRITEBYTECODE=1`.

| Figure | Plan | First Response | Live at `6bcd2d3` | Verdict |
|---|---|---|---|---|
| External review location in file | — | — | appended at end, `d66be06`, `40 insertions(+) 0 deletions` | Checked, not assumed |
| AST baseline entries | 174 | 173 | **173** | Reproduces (first Response right) |
| Baseline, three kinds | 161 | 161 | **161** | Reproduces |
| `Assign:_MODULE_MAPPINGS` digest | `26957a8924042a0a` | same | `26957a8924042a0a` | Reproduces |
| `Assign:_DEFAULT_ON_MODULES` digest | `2c8ef688f6865487` | same | `2c8ef688f6865487` | Reproduces |
| `FunctionDef:main` digest | `ff5a7441cceda605` | same | `ff5a7441cceda605` | Reproduces |
| `FunctionDef:format_profile_summary` digest | `830aac8b7c3d1bde` | same | `830aac8b7c3d1bde` | Reproduces |
| `Assign:_MODULE_REQUIRED_TOKENS` baselined? | declared not-changed | not baselined | **absent from baseline** | Reproduces (M21 stands) |
| Suite | `1744 passed, 2 failed` | `1790 passed, 0 failed` | **1959 passed, 0 failed, 0 skipped**, 307.28s | Non-reproduction ([R8]) |
| Release gate | `Bandit clean over 74 shipped file(s).` | "identical" | **`Bandit clean over 76 shipped file(s).`**, `PASS` | Non-reproduction ([R6]) |
| `check_cairn` | OK, 180 files, 68 links | 195 files, 68 links, 1 issue | **OK, 176 files, 48 links, 0 issues** | Non-reproduction ([R7]) |
| Neutrality | `fail=95 info=21`, rc 1 | same | **`fail=95`, `info=21`**, rc 1 | Reproduces |
| Install manifest data rows | 95 | 95 | **95** | Reproduces |
| `templates/**/*.py`, three channels | 44 / 44 / 44 | 44 / 44 / 44 | **44 / 44 / 44** (`git ls-files`, `find`, `--manifest` rows) | Reproduces |
| Registries | 6 / 20 / 3 | 6 / 20 / 3 | **6 / 20 / 3**, same preset names | Reproduces |
| `gate_manifest.json` `frozen_files` | 164 | 164 | **164** | Reproduces |
| `test_security_lint.py` frozen? | implied no | yes | **yes** | Reproduces (M10 stands) |
| `test_notice_install.py` frozen? | implied no | yes | **yes** | Reproduces (M10 stands) |
| `config.py` `cascade_mutable` string | — | quoted | verbatim: *"AST source-motion attest — one predeclared mapping-symbol delta only (A/B/C/E)"* | Reproduces |
| Six files named not-frozen | not frozen | confirmed | none in the map | Reproduces |
| `docs/quickstart.md` module count | 6 | line 129, 6 | **line 129, 6**, with the `verify:` marker | Reproduces |
| `docs/quickstart.md` slot count | not named | line 182, 21 | **line 182, 21** | Reproduces |
| Live slot count, clean install | not named | 21 | **21**, 4 from `AGENTS.md` | Reproduces, executed |
| Live slot count with the new slot | not named | 22 in all three states | **22**, `AGENTS.md [cairn:slot security-verification]` listed, in the `inserted` state | Reproduces, executed |
| `docs/solo-legacy-recipe.md` roster line | 8-module / six default-on | line 58 | **line 58**, verbatim | Reproduces |
| `templates/modules/README.md` default-on rows | four vs six | lines 34–37 | **four rows, lines 34–37** | Reproduces |
| Empty-slot merge outcome | — | `inserted`, no warning | **`inserted`**, designation present, no side file, no warning | Reproduces, executed |
| Prefilled-slot merge outcome | — | `conflict-deferred` + side file | **`conflict-deferred`**, side file, `stale-or-partial` warning | Reproduces, executed |
| **Customized-slot merge outcome** | not named | named as a residual | **`customized`**, designation **absent**, **no side file**, **no fidelity warning** | New measurement ([E3]) |
| `_slot_is_customized` / fidelity skip | — | — | `slotmerge.py` lines 206, 312, 379 | Reproduces |
| `_LIVING_STATE_DSTS` | not named | not named | **5 entries**, `lockfile.py` line 84 | New measurement ([E1]) |
| Living-state record still carries `hash` | not named | not named | **yes** — `install.py` writes `hash` at 1630, flag at 1634 | New measurement ([E1]) |
| `verify_integrity` honours flag only for the set | not named | not named | `verify_integrity.py` lines 92–105, fails closed otherwise | New measurement ([E1]) |
| Clean install integrity | not named | not named | **OK, 55 recorded files, 4 living-state**, exit 0 | New measurement ([E3]) |
| `dev/modules/*.md` edit detected? | not named | not named | **yes** — `modified (hash mismatch)`, exit 1 | New measurement ([E3]) |
| `scripts/*.py` verbatim edit detected? | not named | not named | **yes** — reported alongside, exit 1 | New measurement ([E3]) |
| In-tree `not_applicable` report shape | not named | not named | `_oracle.py` line 473, `test_oracle.py` line 148 | New measurement ([E2]) |
| `claim_check.py` on this plan | OK | OK, 22 exemptions | **OK, no flags** | Reproduces |

### Amendments in force

Superseded text is quoted **verbatim**; the plan's hard line-wrapping inside a
quoted passage is collapsed to single spaces so the passage fits a table cell —
no word is altered. This plan is append-only, so these rows *are* the change:
where a row conflicts with text above — including with a row in the
2026-08-04 amendments table — **this table governs**, and the 2026-08-04 table
governs everything above it.

| # | Locus | Superseded text (verbatim) | Replaced by |
|---|---|---|---|
| M24 | Chunk A, row A1, the registry-schema fragment | "Module-level `_REGISTRY: dict[str, RegistryEntry] = {}` — **empty**, with the nine admission fields as a frozen dataclass/`NamedTuple` (`module_id`, `runner_repository_path`, `argv_mode`, `policy_repository_path \| None`, `child_schema_version`, `capability_contract_version`, `evidence_mode`, `accepted_process_exits`, `result_to_aggregate_mapping`). `evidence_mode` constrained to `frozenset({"offline", "loopback"})` at construction." | Module-level `_REGISTRY: dict[str, RegistryEntry] = {}` — **empty**, with **eleven** admission fields as a frozen dataclass/`NamedTuple`: the nine above **plus `runner_binding_mode` and `policy_binding_mode`**. Every field is **required, has no default, and is not inferable from any other field.** Two closed sets, both constrained at construction, both `frozenset` literals in the dispatcher source: `evidence_mode` ∈ `{"offline", "loopback"}` (unchanged); `runner_binding_mode` ∈ `{"immutable_digest"}` — a deliberately **one-member** set, so a future "living runner" cannot appear by omission but only by a source edit that widens the frozenset, which is a registry-schema change and therefore a Security Review; `policy_binding_mode` ∈ `{"none", "immutable_digest", "living_state"}`. **Agreement rules, each refused at construction with a message naming both fields:** `policy_binding_mode == "none"` **iff** `policy_repository_path is None` (either without the other refuses — this closes the undeclared third mode [R5] names); `"immutable_digest"` and `"living_state"` each require a non-`None` path. **Runtime binding by mode, all failures DEGRADED (`20`) with no child launched, never INCOMPLETE and never CLEAN:** under `"none"` the parent binds the runner only; under `"immutable_digest"` the parent binds the runner **and** compares the policy's SHA-256 with its lockfile record, **and refuses (`20`) if that record carries `living_state: true`** — an immutable declaration over a living record is a misdeclaration, not a pass; under `"living_state"` the parent binds the runner digest unchanged, binds the policy's **existence, regular-file and non-symlink status**, binds the **presence of a lockfile record**, and **refuses (`20`) if that record lacks `living_state: true` or if the policy path is outside the engine's `_LIVING_STATE_DSTS` authoritative set** — the fail-closed mirror of `bootstrap/verify_integrity.py` lines 96–105 — and **does not compare the policy's content digest**. The dropped property is named in A2's doctrine as a residual, not skipped silently. |
| M25 | Chunk A, T5 | "`test_every_admission_field_is_required` — a deletion mutant per field: nine synthetic entries, each missing one of the nine, each refused at construction with a message naming the field." | Same test, **eleven** deletion mutants over the eleven fields of M24, each refused at construction with a message naming the field. The two new rows are the load-bearing ones: an entry that omits `policy_binding_mode` or `runner_binding_mode` must **refuse**, not default — a defaulted binding mode is the "silently change modes" failure E1 names, reached by omission. *Weakness stated, unchanged:* this pins the **validator**; that the shipped registry is empty is T1's job. |
| M26 | Chunk A, T17 | "`test_runner_or_policy_digest_mismatch_is_degraded` — write the lockfile, then flip one byte of the runner (and, separately, of the policy); both `20`, no child launched." | Same test, **parametrized by `policy_binding_mode`**, because the assertion is no longer unconditional. Rows: (a) runner byte flipped — `20`, no child launched, **under all three modes**; (b) policy byte flipped under `"immutable_digest"` — `20`, no child launched; (c) policy byte flipped under `"living_state"` — the leg **proceeds** (this is the whole point of the mode) and the report records the policy as `binding: living_state, digest_not_compared`, so the dropped property is **visible in the machine output** rather than invisible; (d) policy byte flipped under `"none"` — unreachable, since the path is `None`; asserted as a construction refusal, not a runtime row. |
| M27 | Chunk A, new tests T36–T40 | *(addition)* | **T36** `test_policy_binding_mode_is_a_closed_set` — parametrized over `deployed`, `unbound`, `skip`, `living`, `immutable`, `""`, `None`, `"none,living_state"`: construction raises for every row. *Perturbation:* widen the frozenset to include `"unbound"`; that row fails. The exact mirror of T4 for the second closed set. **T37** `test_binding_mode_and_policy_path_must_agree` — four rows: (`"none"`, a path) refuses; (`"immutable_digest"`, `None`) refuses; (`"living_state"`, `None`) refuses; (`"none"`, `None`) constructs. *Perturbation:* drop the agreement check; the first three rows fail. **T38** `test_living_state_mode_requires_the_lockfile_flag_and_the_authoritative_set` — three rows: lockfile record present but **without** `living_state: true` → `20`; record flagged but the path is **outside** `_LIVING_STATE_DSTS` → `20`; both satisfied → the leg proceeds and the policy digest is not compared. *Perturbation:* make the living branch skip the flag check; row one reaches CLEAN. **T39** `test_immutable_mode_refuses_a_living_state_record` — an entry declared `"immutable_digest"` whose policy record carries `living_state: true` → `20`, no child launched. *Perturbation:* treat `living_state` as "skip the comparison"; the row reaches CLEAN. **T38 and T39 together are E1's "cannot treat a living policy as an immutable one", in both directions.** **T40** `test_a_registry_entry_cannot_change_mode_after_construction` — assigning `policy_binding_mode` on a constructed entry raises. *Perturbation:* make the dataclass non-frozen (or use a plain class); the assignment succeeds and the test fails. This is E1's "cannot silently change modes" at the object level, where T36/T37 cover it at the declaration level. |
| M28 | *Glossary*, the `Admitted` entry | "**Admitted** — a registry entry that cleared the five-part admission rule in the proposal's revision (accepted capability proposal; reviewed plan with execution evidence for that exact mode; complete lockfile mapping group; schema and precedence tests; a Security Review of the registry change). At v1 nothing is admitted, so the registry is empty." | The same five parts, **plus a sixth: the binding mode is part of what is admitted.** An entry is admitted *for a named `policy_binding_mode`*; changing an admitted entry's mode is a registry change and takes its own Security Review, not a follow-up commit. A `"living_state"` entry additionally requires the capability's own plan to carry **execution evidence for the compensating controls that replace the digest** — for `api-web-security-modules` these are the strict schema, the loopback-only local leg and `--authorize-base-url`, and evidence means an executed run, not a design argument. At v1 nothing is admitted, so the registry is empty and no mode is exercised. |
| M29 | *Maintainer fence*, new item 4 | *(addition)* | **The `living_state` binding mode narrows an accepted contract, and admitting an entry under it is not an implementing agent's to do.** The proposal's revision established parent-computed digest binding over *"the runner and policy"*; `policy_binding_mode: living_state` drops the policy half for a declared class of records. M24–M28 land the **schema and its tests** — which is what the External reviewer required to land here, and which is safe because the v1 registry is empty and no mode is exercised — but **no registry entry may be admitted under `"living_state"` until the Maintainer ratifies the narrowing.** An implementing agent who finds a capability plan asking for such an entry **stops and reports**, exactly as at the AST fence. Recorded for the ceremony: `dev/plans/api-web-security-modules.md` AM13/AM15 already gate its Chunk G on this ruling, so the two artifacts agree on the gate and only the Maintainer can open it. |
| M30 | Chunk A, T20 | "`test_no_capability_prints_the_exact_not_applicable_line_and_exits_0` — stdout contains exactly `NOT APPLICABLE: no selected local security capability`, exit `0`, machine result `aggregate: NOT_APPLICABLE`, `legs: []`, a non-empty `reason`." | Same test, with the machine result **named and shaped on the in-tree precedent** rather than left informal. The dispatcher emits **one JSON object** on stdout carrying: `schema` (a versioned literal, on the `bootstrap/tests/_oracle.py` line 81 model `"cairn.scaffold_split.oracle/v1"`), `status: "not_applicable"` **as an explicit string state**, `ok: true`, `aggregate: "NOT_APPLICABLE"`, `evidence_count: 0` **as an explicit integer**, `legs: []`, and a non-empty `reason`. Assert all seven. *Rationale, since the addition is redundant on its face:* `legs: []` makes automation infer a count from a container length and `aggregate` makes it string-match a label; E2 asks for a state and a count it can key on directly. *Perturbation unchanged:* make the no-capability path return `CLEAN` — now fails on the literal, on `status`, and on `aggregate`. **Additional perturbation:** drop `evidence_count` from the report; the test fails on a missing key rather than silently passing on a container check. |
| M31 | Chunk B, T33 | "`test_the_dispatcher_runs_green_from_a_real_fresh_scaffold` — end-to-end: scaffold into `tmp_path`, run `python scripts/run_security_verification.py local` **as a subprocess** from that tree, assert exit `0` and the exact `NOT APPLICABLE` line. The public path, not an import." | Same test, **plus the machine assertions of M30 through the same subprocess**: parse the emitted JSON and assert `schema`, `status == "not_applicable"`, `ok is True`, `aggregate == "NOT_APPLICABLE"`, `evidence_count == 0`, `legs == []`. This is E2's actual surface: T20 drives `main()` in-process, and **T33 is the only test that sees what an adopter's automation sees.** Existing perturbation retained; **second perturbation added:** make the no-capability path emit exit 0 with no machine object at all — the human line still matches, the exit code is still 0, and only the machine assertions go red. That is the *"generic exit-0 success that downstream automation can mistake for a passing security check"* the review names, made mechanical. |
| M32 | Chunk A, row A2, the doctrine content list | "Module doctrine: the registry rules, the five-part admission rule quoted from the proposal's revision, the aggregate ladder and its precedence, trusted-checkout scope, the local/deployed separation **and its explicit non-claim** (not actor authentication), and recovery from INCOMPLETE / DEGRADED." | The same list, **plus three additions**, because an adopter receives A2 and never receives this plan's glossary: (a) **`NOT_APPLICABLE` is not evidence.** The doctrine states in terms that `NOT_APPLICABLE` is the *absence* of security evidence, not a passing check, that it must not be reported, aggregated, or badged as one, and that its exit `0` means "nothing was asked of me", not "nothing is wrong". (b) The **binding-mode schema of M24**, including the residual that a `"living_state"` policy's bytes are not lockfile-attested and its review channel is git. (c) The **high-risk Security-Review designation of M34**. The five-part admission rule quoted from the revision becomes the **six-part** rule of M28. |
| M33 | Chunk A, new test T41 | *(addition)* | `test_the_module_doctrine_states_not_applicable_is_not_evidence` — read the **shipped** `templates/modules/default-on/security-verification.md` from `templates/`, not an installed copy; assert it contains the non-evidence statement, that `NOT_APPLICABLE` appears in it at all, and that no green-security phrase (`CLEAN`, `secure`, `passed security`, `no vulnerabilities`, `verified`) occurs in the same paragraph. *Perturbation:* delete the non-evidence sentence from A2's source; the test fails. Precedent for asserting shipped doctrine text: `bootstrap/tests/test_practice_modules.py`. *Channel note:* the oracle is the shipped source read independently; the subject is what an adopter receives. Same class as T1 and T23. |
| M34 | 2026-08-04 amendments table, row M11, its *Replaced by* cell | "The designation moves to **A2's merge-content block** (so it lands durably in the adopter's `security-verification` slot and is guarded by `check_slot_fidelity`) **and to `dev/modules/security-verification.md`** (B2). Named residual: an adopter who marks the slot `cairn:customized` opts out of the substring check." | The strike of A4's line stands. The designation lands on **three channels, and the guard claim is corrected**: `check_slot_fidelity` guards **one** of the three reachable slot-body states. Measured: `empty` → `inserted`, guarded; `adopter-prose` → `conflict-deferred`, side file **and** a `stale-or-partial` warning; `customized` → status `customized`, designation **absent**, **no side file and no warning at all**. The three channels: (1) **A2's merge block** → the adopter's slot — customizable, and that is the residual, not a guard; (2) **B2 `dev/modules/security-verification.md`** — lockfile-recorded and **not** living-state, so an adopter edit is `modified (hash mismatch)`, exit 1; (3) **the dispatcher source `scripts/run_security_verification.py`** — a module docstring block at the `_REGISTRY` definition site, verbatim and hash-pinned, additionally flagged `locally-modified` by `classify_verbatim` and never clobbered. Channel 3 is the answer to E3: it puts the designation in **the same file as the registry**, so a registry change and its review trigger are one artifact. **Two tests.** **T42** (Chunk B) `test_the_high_risk_designation_survives_on_two_tamper_evident_channels` — read the shipped A2, B2 and dispatcher sources for the designation; scaffold into `tmp_path`; `verify_integrity` → OK; delete the designation from the installed `dev/modules/security-verification.md` and from `scripts/run_security_verification.py`; `verify_integrity` reports `modified (hash mismatch)` for **both** and exits **1**. *Perturbation:* drop the designation from the dispatcher source; the source-read row fails. **T43** (Chunk B) `test_a_customized_slot_silently_drops_the_designation` — a **characterization** test that pins the residual rather than closing it: mark the slot `<!-- cairn:customized -->`, run the merge; assert status `customized`, designation absent from `AGENTS.md`, **`check_slot_fidelity` returns an empty list**, no side file, and the two tamper-evident channels still carry it. *Perturbation:* make `_slot_is_customized` return `False`; the status and no-warning assertions go red. Its docstring says, where a reader will find it, that a green T43 is a **recorded open residual**, not a closed one. |
| M35 | Chunk D, row D1 | "(d) **command separation is not actor authentication** — a person or agent with shell access can invoke another script directly, and Cairn does not claim to distinguish a human process from an agent process. (d) is the sentence that must not be softened." | (d) unchanged and still the sentence that must not be softened, **plus a fifth recording (e)**: the dispatcher, its source-owned registry, its child result schema, its **binding-mode schema**, and every registry entry are **high-risk Security-Review surfaces**; that designation is carried on three channels of which **two are tamper-evident** (the lockfile-recorded `dev/modules/security-verification.md` and the hash-pinned dispatcher source) and one is not (the adopter's `AGENTS.md` slot, which `<!-- cairn:customized -->` silently exempts from both the merge and the fidelity check); and an adopter who customizes that slot **removes the designation from their governing document with no warning from any Cairn tool**. (e) is a recorded residual, not a claim of coverage. |
| M36 | Chunk A acceptance criteria, and *Verification* > plan-specific gates | "* `python bootstrap/security_check.py` → `PASS`, Bandit line reporting **75** files (74 + the dispatcher)." **and** "* **The release gate** — `python bootstrap/security_check.py`. Expected `PASS`, Bandit line reporting **75** files. Baseline before Chunk A: 74." | Live baseline at `6bcd2d3` is **76**, not 74: `security_check: Bandit clean over 76 shipped file(s).` → `PASS`. The arithmetic is unaffected — the dispatcher adds exactly one scanned file, because `scan_targets()` derives `templates/` targets from registry data — so the criterion is **`N` → `N+1`, where `N` is re-taken immediately before Chunk A**, currently 76 → 77. **Do not apply 77 from here**; the shipped-file count moves with every cluster scope that adds a shipped file. The MEDIUM+ rule is unchanged: a finding is a code fix inside Chunk A, never an allowlist entry. |
| M37 | 2026-08-04 amendments table, row M23, its *Replaced by* cell, the parenthetical | "(195 at `6b6034e`, +1 for B2)" | **176** at `6bcd2d3` — `check_cairn: OK -- 176 Markdown file(s) scanned; no issues; 48 external link(s) not probed.` The figure has now moved 180 → 195 → 176 and the external-link count 68 → 48. The cause is **not** a change to the checker: `f897cda`, which makes `check_cairn` skip `dev/**/archive/` by default, is an ancestor of `6b6034e` as well as of `6bcd2d3`, so the same rule governed both readings. What moved is the population — 14 proposals archived between the two commits, and archived sources are skipped. **The count moves in both directions with work this plan does not own, so it is not a criterion in any form.** M23's substantive replacement stands unchanged and is strengthened: the criterion is **"no `check_cairn` issue is attributed to a file this plan edits"**, full stop. Also recorded: the one sibling-scope issue M23 cited is gone; the tree reports **0 issues** today. |
| M38 | 2026-08-04 amendments table, row M15, its *Replaced by* cell, the live figure | "Live: **`1790 passed` in 171.22s, 0 failed, 0 skipped**, in the repository at `6b6034e` with no engine modification in the tree." | **`1959 passed, 0 failed, 0 skipped` in 307.28s** at `6bcd2d3`, in the repository, under the canonical interpreter with `PYTHONDONTWRITEBYTECODE=1`. Four readings in two days: 1744 → 1779 → 1790 → **1959**. M15's disposition — the figure is **retired as an oracle**, and the plan-level criterion *"collection grows by exactly the new nodes and drops none"* binds to a count re-taken at the implementing commit — stands, and this reading is why. |
| M39 | Plan-level acceptance criteria, *Tests that must pass*, second bullet | "* `bootstrap/tests/test_security_verification.py` — T1–T35, the plan's own surface. *(Forward reference: the file lands at Chunk A; registered under `Proposed paths:` above.)*" | `bootstrap/tests/test_security_verification.py` — **T1–T43 plus T31b**, the plan's own surface. Chunk A holds T1–T24 and T36–T41; Chunk B holds T25–T33, T31b, T42 and T43; Chunk C holds T34–T35. *(Forward reference unchanged.)* The perturbation-ledger obligation extends to every added test; where a test is a **characterization** rather than a guard — T28, T43 — the ledger says so in those words. |
| M40 | *Lasting-truth migration*, new rows L9 and L10 | *(addition)* | **L9** — *"`<!-- cairn:customized -->` silently exempts a slot from **both** the module merge and the fidelity check, so an adopter can remove a module's contributed Security-Review designation from their governing document with no warning."* Durable home: **`dev/proposals/` — its own proposal.** Declined for this plan because it changes the marker's behaviour for every slot and every module, re-opens an accepted disposition from inside a capability-activation plan, enlarges this plan's declared symbol delta into a second engine file no cluster scope has declared, and would land in a file (`bootstrap/_scaffold/slotmerge.py`) that is not in the 164-entry `frozen_files` map, so no gate would see it. Pinned meanwhile by T43. **L10** — *"The dispatcher's machine-report schema (M30) is the contract every future capability's automation reads; at v1 no capability exercises it."* Durable home: the **first capability plan to be accepted**, which is the first artifact able to assert the non-`not_applicable` shape end-to-end. |

Nothing in this table adds a registry entry, widens the empty-registry
contract, changes the aggregate ladder or its precedence, weakens any of the
Decision's three named properties, moves a Maintainer fence, or takes on a
sibling scope's surface. One row (M29) **adds** a fence.

### What this Response does not settle

* **The dispatcher's runtime behavior.** No code exists. T1–T43 remain
  specifications. Both prior rounds said so and it is still true; nothing in
  this Response could check that any of them will hold.
* **Whether the Maintainer ratifies the `living_state` narrowing.** M29 is a
  gate, not a decision. This Response specifies the mode and declines to admit
  anything under it.
* **The Bandit profile of the dispatcher.** Unmeasurable before Chunk A; the
  *baseline* is corrected to 76 (M36), the *prediction* is not.
* **The proposed slot text's content-scan result.** The plan's exact text is
  still not in the tree. Unchanged from the first Response.
* **Whether the Decision requires `format_profile_summary` at v1.** A
  Decision-reading question. Three rounds have now declined to answer it; it is
  still strikeable in one line and still the Maintainer's.
* **Cross-cluster re-anchor sequencing (L7).** Maintainer-owned.
* **Whether the External reviewer considers E1–E3 discharged.** That is theirs
  to say, not mine. This Response is the author's disposition of a REVISE.

### Gate audit

Every gate this plan declares, and whether it is satisfied **today**, at
`6bcd2d3`. Two gates were breached elsewhere in this repository yesterday
because nobody read them, so this table is written to be read rather than
skimmed.

| Gate | Where it is declared | Satisfied today? |
|---|---|---|
| **Declared review tier** — `required(External, security lens)` | Header, and *Plan review — the brief* | **NO.** The round was **held** — Codex, External, security lens, 2026-08-05 — and returned **REVISE**. A held round with a REVISE verdict is not a discharged tier. |
| **"No implementation commit lands before the `## Plan review` section is in the tree."** | Header | **Literally yes**, since `d66be06`. **And it is not a licence.** This is the section-*kind* gate that the accepted `review-gate-enforcement` proposal exists to fix: it reads a heading, never a verdict. Treating it as satisfied here would be using a known-defective gate to authorise work its own repair proposal says it cannot authorise. |
| **Sequence step 0** — "(plan review) -- required(External, security lens); NO code before it lands" | *Sequence* | Same reading as above. The section has landed; the verdict has not cleared. |
| **Maintainer fence 1** — the AST re-anchor ceremony, after Chunk A and after Chunks B/C | *Maintainer fence* | **Not reached.** No implementation has occurred. The three declared symbols and all four digests re-verify at `6bcd2d3` against a **173**-entry baseline; `_DEFAULT_ON_MODULES` is still in neither `_UPDATE_ALLOWLIST` nor `mapping_symbols`, so there is still no surgical path. |
| **Maintainer fence 2** — anything needing a key or credential | *Maintainer fence* | **Standing, not reached.** Nothing in this plan needs one; the item exists because the runbook has a signing phase. |
| **Maintainer fence 3** — the gate-manifest re-pin, as corrected by **M10** | *Maintainer fence* + M10 | **Not reached, and re-verified today.** `gate_manifest.json` still holds **164** `frozen_files`; `bootstrap/tests/test_security_lint.py` and `bootstrap/tests/test_notice_install.py` are **both still in it**, so the two `FROZEN-MODIFIED` rows remain **guaranteed, not contingent**. `bootstrap/_scaffold/config.py` is still `cascade_mutable` under *"AST source-motion attest — one predeclared mapping-symbol delta only (A/B/C/E)"*, verbatim. |
| **Maintainer fence 4 (new)** — no entry admitted under `policy_binding_mode: living_state` until the Maintainer ratifies the narrowing | M29, this Response | **Open by construction.** It is created here and nothing satisfies it. `api-web-security-modules` AM15 already gates its Chunk G on the same ruling. |
| **Decision condition** — *"The plan carries `required(External, security lens)` in its own right; this Decision does not discharge it."* | Source proposal, `## Decision -- Anthony Kendall (Maintainer) -- 2026-08-03` | **Holds, verbatim.** Re-read at `dev/proposals/archive/2026-08-03-codex-security-verification-activation.md`. The Decision's ordering clause also still holds: this artifact precedes any Decision on the two capability proposals. |
| **Plan status** | Header, `**Status**: open` | **Unchanged — `open`.** Recorded rather than edited: the header is a prior section and this plan is append-only, so its `**Last update**: 2026-08-04` field is stale by design and only a serialization-point edit may move it. |

### Does this Response clear the plan to implement?

**No.**

Three independent reasons, any one of which is sufficient:

1. **The External round returned REVISE, and an author Response does not
   answer a REVISE.** The reviewer required an amendment to *land here* before
   a sibling's registry entry can land there, and required tests for properties
   that did not exist. M24–M35 and M40 land them. Whether they land them *correctly* is
   a question for a reviewer, not for their author. The precedent is in this
   tree and it is one day old: an External reviewer on a sibling plan wrote
   that they *"treated the authored Response as evidence of intended changes,
   not a replacement for the plan's executable contract"*, and returned REVISE
   a second time.
2. **M29 opens a Maintainer gate that only the Maintainer can close.** The
   `living_state` binding mode narrows a property the accepted proposal
   established and the Decision rests on. The schema lands; the narrowing does
   not take effect for any entry until it is ratified.
3. **The plan's own literal gate is the one `review-gate-enforcement` exists to
   repair.** It is satisfied by a heading. Reading it as authorisation, on the
   very artifact whose reviewer said REVISE, would be the precise defect that
   proposal was accepted to stop.

What remains, in order:

1. **A second External security-lens round** — by a different agent type or the
   Maintainer — reading the plan *with* M24–M40 in force, with E1's schema as
   the first thing to attack. The reviewer's own framing is the right test:
   does the schema make it impossible for an entry to silently change mode,
   omit a binding field, or treat a living policy as immutable? T36–T40 are the
   claim; only a reviewer with a checkout can falsify them once code exists.
2. **Three Maintainer calls, surfaced and not resolved here** — carried forward
   from the first Response and extended by one: whether M1's above-marker
   guidance is acceptable in `templates/core/AGENTS.md`; whether the two
   guaranteed `FROZEN-MODIFIED` rows change the ceremony's shape; and **the
   M29 ratification of the `living_state` narrowing**, which two plans now
   block on.
3. **The AST re-anchor ceremony**, unchanged and still the Maintainer's, over a
   union the Maintainer forms, against a **173**-entry baseline.

The amendments above make the plan executable-as-written on the surfaces the
External round attacked. **They do not discharge the tier, and this Response
claims no tier satisfied.**

## Plan review -- Codex (External) -- 2026-08-05

**Tier**: External
**Findings**: raised

**Verdict: REVISE.** M24 now contains a real closed vocabulary for
`runner_binding_mode` and `policy_binding_mode`, including the narrowed
`living_state` mode, and M25--M29 attach refusal tests and a Maintainer fence.
M30--M35 also settle my prior machine-readable `not_applicable` and high-risk
visibility findings in the executable contract rather than promising them.

The reciprocal API/web plan nevertheless asks this plan to resolve four named
bindings while M24 resolves only runner and policy. State explicitly that the
v1 list resolves to those two apparatus bindings and that principal and scope
remain child-policy semantics with no registry fields. Also specify the
extra-field behavior: M25 tests missing fields, but neither plan says whether an
extra binding field is rejected, ignored, or structurally impossible.

The pair's admission fence is also asymmetric. The API/web plan now blocks F2
and G; M29 blocks only a registry entry using `living_state` and still points to
older amendment labels rather than the widened F2/G condition. Mirror one
condition on both sides, including whatever executable Chunk F split the paired
plan chooses. The narrowing to `policy_binding_mode: living_state` is a sound
Maintainer decision; it does not by itself define when both producers of that
state may land.

### Sharpening

Keep schema implementation separate from entry admission: the dispatcher can
land with an empty registry, while no living-state entry or producer lands
until the paired contract and review are ratified. That preserves progress
without making the cross-plan gate one-sided.

## Maintainer disposition of the 2026-08-05 External review round

The 2026-08-05 `## Plan review -- Codex (External)` section above returned
**REVISE**. This plan fences implementation behind the External reviewer, **or
the Maintainer**, disposing of that REVISE. The Maintainer disposed of it. The
authorizing instruction, **verbatim**:

> Go ahead with implementation once you've revised these. I don't want another review round

**What that authorization does.** It disposes of the review round: the REVISE
verdict on the 2026-08-05 External section is closed by the Maintainer, and no
further review round is required to open implementation on the *unfenced* work —
which for this plan is the schema and its tests, with the registry empty. It is a
disposition, **not a bypass**: the round happened, its findings are closed by the
fold recorded below, and the Maintainer exercised the authority this plan's own
fence names.

**What it does not do**, stated so no later reader can stretch it:

* It is **not** the ratification of the `living_state` narrowing. Maintainer-fence
  item 4 and **B3** stand: no living-state entry, and no producer of the
  living-state record, lands on this instruction. An agent that cites it as
  ratification has breached the fence.
* It supplies **no** Maintainer credential and **no** signing ref.
* It authorizes **no** AST re-anchor ceremony. Fence items 1–3 are untouched, and
  the two guaranteed `FROZEN-MODIFIED` rows are still the Maintainer's to re-pin.
* It is **not** approval to push. Pushing needs its own approval, every time.

### Sharpening — the 2026-08-05 fold pass

Inline chunk-cell edits driven by the accepted plan-review findings, under
`doctrine/plans.md:202-207` (status `open`, no implementation commit, nothing in
flight against the edited chunks). **The reciprocal plan
`api-web-security-modules` carries the identical shared block and lands in the
same commit** — B3's own requirement, not a convenience.

**Cells changed, and why.**

| Cell | Change | Why |
|---|---|---|
| *Glossary*, `Admitted` | Five-part rule → **six**-part: the binding mode is part of what is admitted | A2's doctrine list now cites the six-part rule; the definition had to exist operatively |
| *Maintainer fence*, opening + item 3 + new item 4 | Three things → four; item 3's "no file this plan edits is frozen" conditional replaced by the measured fact that **both** pin files are in the 164-entry map; item 4 is B3 | Item 3 contradicted this plan's own later measurement, and B3 needed an operative home in the fence an implementer reads |
| Chunk A row **A1** | Nine fields → **eleven**; three closed vocabularies; the agreement rules; the per-mode runtime binding with `digest_not_compared` in the report; **B2's closed-vocabulary lockfile-record reader**; no `principal`, no `scope`; the hash-pinned designation docstring | Finding 1 (B1), finding 2 (B2), and the schema that finding 3's fence is drawn around |
| Chunk A row **A2** | Six-part admission rule; `NOT_APPLICABLE`-is-not-evidence; the binding-mode schema and its residual; the high-risk designation; the customized-slot residual | An adopter receives A2 and never receives this plan |
| Chunk A row **A4** | Names the **three** designation channels, which two are tamper-evident, and that this slot is the one that is **not** a guard | The earlier cell implied the fidelity check guarded it |
| Chunk A row **A5** | Suite is T1–T24, **T36–T41, T44** | The rows existed only in an amendment table |
| Chunk A test **T5** | Nine deletion mutants → **eleven** | A defaulted binding mode is the omission failure |
| Chunk A test **T17** | Parametrized by `policy_binding_mode`, four rows, three perturbations | The unconditional assertion is false under `living_state` |
| Chunk A test **T20** | Seven asserted machine members incl. explicit `status` and `evidence_count`; second perturbation | Automation must key on a state and a count, not a container length |
| Chunk A tests **T36–T41**, new **T44** | Added as operative rows | T36–T41 existed only in the amendment table; **T44 is new in this pass** and is finding 2's test — the extra-field impossibility asserted **by trying it** |
| Chunk A criteria | Manifest `N + 2` with `N` re-taken; Bandit `N + 1` with `N = 76` measured; the two `44` pins cited by line with the cross-scope hazard named; ledger extended to T36–T41 and T44 | Every figure re-derived at `d73d436`, and the `75`/`74` pair no longer reproduces |
| Chunk B row **B5** | T25–T33, **T31b, T42, T43** | T31b and T42/T43 existed only in amendment tables |
| Chunk B test **T33** | Adds T20's machine assertions through the same subprocess; second perturbation | T33 is the only test that sees what an adopter's automation sees |
| Chunk B tests **T31b, T42, T43** | Added as operative rows; T43's characterization status stated in the cell | A characterization test read as a guard is worse than no test |
| Chunk B criteria | Markdown file count **deleted as a criterion**; neutrality re-verified at 95 with a re-take instruction; ledger extended | The count has read 180 → 195 → 176 → 177 and moves with work this plan does not own |
| Chunk D row **D1** | Adds the fifth recording (e): the designation's three channels and the silent-drop residual | It was a recorded residual with no operative home |
| Chunk D criteria | `check_cairn` criterion is "no issue attributed to a file this chunk edits"; neutrality same-run comparison | Same reason as Chunk B |
| Plan-level criteria | Suite baseline figure **deleted, not updated**; test surface is T1–T44 incl. T31b, distributed by chunk | Four readings in three days; a fifth would date as fast |
| *Verification* > plan-specific gates + examples | `75`/`74`/`97` replaced by `N + 1` / `N + 2` with `N` measured at `d73d436` | The stated figures no longer reproduce |

**Amendment rows now folded.** Superseded as **operative instructions** — the cell
named carries them. Their text is untouched and stays part of the record; nothing
in this pass rewrites an amendment, a review, a Response, or a Lasting-truth
entry.

| Row | Folded into | Note |
|---|---|---|
| M4 | Chunk B test T31b | |
| M10 | Maintainer fence item 3 | the two `FROZEN-MODIFIED` rows are now stated as guaranteed, re-measured at `d73d436` |
| M24 | Chunk A row A1 | |
| M25 | Chunk A test T5 | |
| M26 | Chunk A test T17 | |
| M27 | Chunk A tests T36–T40 | |
| M28 | *Glossary*, `Admitted` | |
| M29 | Maintainer fence item 4 | **superseded by B3**: one condition on both sides, not a registry-entry-only fence; the older amendment labels it cited are replaced by B3 |
| M30 | Chunk A test T20 | |
| M31 | Chunk B test T33 | |
| M32 | Chunk A row A2 | |
| M33 | Chunk A test T41 | |
| M34 | Chunk A rows A1/A4 + Chunk B tests T42/T43 | |
| M35 | Chunk D row D1 | |
| M36 | Chunk A criteria + *Verification* | figure re-derived, not carried: `N = 76` at `d73d436` |
| M37 | Chunk B criteria | the file count is **deleted** as a criterion rather than re-stated |
| M38 | Plan-level criteria | the suite figure is **deleted**, not updated |
| M39 | Plan-level criteria | extended to T44 |

**Figures re-derived at `d73d436` under
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13).** Nothing below
is carried forward from an earlier revision of this plan. **Measurement
conditions, stated because they matter:** HEAD was `d73d436` and no tracked file
in any measured surface was modified in the working tree at read time, but
untracked files were present and **concurrent sessions moved HEAD to `d2f82e0`
before this commit landed.** Every row below is a **dated snapshot, not a
constant**.

| Figure | Stated before | Measured now | Disposition |
|---|---|---|---|
| Manifest data rows | 95 (→ 97) | **95** | folded as `N` → `N + 2`, `N` re-taken |
| Bandit shipped files | 74 (→ 75); 76 in an amendment row | **76**, `PASS` | folded as `N` → `N + 1`, `N` re-taken |
| `check_cairn` Markdown files | 180 → 195 → 176 | **177** at `d73d436`, 0 issues, 48 links unprobed — and **178** at `d2f82e0` within the same session, with only concurrent scopes' work in between | **deleted as a criterion.** Five readings in four days, moving in both directions, is the argument |
| neutrality | `fail=95` | **`fail=95 info=21`** | reproduces; kept as a same-run comparison |
| AST baseline entries | 173 | **173** | reproduces |
| `Assign:_MODULE_MAPPINGS` digest | `26957a8924042a0a` | **`26957a8924042a0a`** | reproduces |
| `Assign:_DEFAULT_ON_MODULES` digest | `2c8ef688f6865487` | **`2c8ef688f6865487`** | reproduces |
| `FunctionDef:main` digest | `ff5a7441cceda605` | **`ff5a7441cceda605`** | reproduces |
| `frozen_files` entries | 164 | **164**, and **both** pin files are members | folded into fence item 3 as a guaranteed pair |
| `44` pins | 44 / 44 | **44** at `test_notice_install.py:75` and `test_security_lint.py:291` | folded with citations |
| `_oracle.py` schema-literal citation | line 81 | **line 81** (`REPORT_SCHEMA`) | reproduces; kept in T20 |
| Suite total | 1744 → 1779 → 1790 → 1959 | **not re-measured** | **deleted**, not updated. The criterion is the growth-by-exactly-the-new-nodes rule against a count re-taken at the implementing commit |

**What this pass did not fold, and why.**

* **The plan header's review-gate sentence** (*"No implementation commit lands
  before the `## Plan review` section is in the tree"*). It reads a heading, never
  a verdict — the defect `review-gate-enforcement` exists to repair. It is not
  chunk-table cell text, so this pass left it. The Maintainer's disposition above
  is what closes the landed REVISE; **the header sentence is not, and never was,
  the thing that closed it.**
* **`## The measurement that shapes this plan`, the cluster section, `## Scope`,
  *Author-accounting*, and the Lasting-truth table.** Prose or append-only
  surfaces, not chunk cells. Their amendment rows remain operative for them — with
  one exception recorded explicitly: item 3 of the Maintainer fence now
  **contradicts** the older frozen-file reading in *The measurement that shapes
  this plan*, and the fence is the operative statement of the two.
* **`bootstrap/verify_integrity.py`'s extra-key tolerance.** Measured, and B2's
  refusal is implemented in the **dispatcher's** reader instead (A1, T44). Changing
  `verify_integrity` is outside this plan's declared symbol delta; it is a lasting
  truth for the archive, not a silent widening.

## Maintainer ratification -- living-state policy binding -- 2026-08-05

The Maintainer's authorizing instruction, quoted verbatim and visually isolated:

> I ratify policy_binding_mode: living_state for adopter-owned API and web policy files. I accept that the dispatcher binds the runner digest and the policy path, type, and lockfile classification, but does not compare the policy content digest; git review is the policy-byte review channel. I authorize Codex to scribe and commit this ratification in both api-web-security-modules and security-verification-activation.

This ratifies the exact narrowing described by the shared B3 admission fence.
**B3 is MET:** a registry entry may now declare `policy_binding_mode:
living_state`, and the reciprocal capability plan may produce the corresponding
living-state lockfile record, subject to every other chunk criterion and review.

The ratification does not add principal or scope fields, weaken runner-digest
binding, authorize credentials or a non-loopback target, produce the first-use
trust hash set, run an AST or gate-manifest ceremony, authorize signing or
pushing, or waive independent code review.

## Implementation verification -- Claude -- 2026-08-10

**Scope of this pass: Chunk A only.** Chunks B, C, D are untouched. Run under
the canonical interpreter (`~/conda_envs/lhm/bin/python3.13`, Python 3.13.13),
`PYTHONDONTWRITEBYTECODE=1`.

**Commits.** `6e3a8ed` (A1, A2, A3, A5, A6, A7 -- the dispatcher, its doctrine,
the `_MODULE_MAPPINGS` registration, the T1-T24/T36-T41/T44 test suite, both
`.py`-count pins) and `6b488a2` (a same-session follow-up: `docs/quickstart.md`'s
unfilled-block-slot count, 21 -> 22, driven by A4's new slot; two
`claim-check-allow` directives for adopter-tree-only forward references). **A4**
(the `templates/core/AGENTS.md` slot) landed in `6e3a8ed` with placeholder prose
matching the claim-check slot's model; it is **not exercised** by Chunk A's own
tests (T30/T31/T42/T43, which check the live merge, are Chunk B's).

**Targeted tests.**
`pytest bootstrap/tests/test_security_verification.py
bootstrap/tests/test_security_lint.py bootstrap/tests/test_notice_install.py
bootstrap/tests/test_quickstart_sequence.py` -> **96 passed, 0 failed** (measured
after both commits, at HEAD `6b488a2`).

**Full suite, once, between the two commits.**
`pytest bootstrap/tests` at HEAD `6e3a8ed` -> **2587 passed, 5 failed** (379.98s).
Of the five: **2 are the expected, fenced AST-attest RED**
(`test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`,
`::test_ast_gate_passes_over_the_full_scaffold_module_set`) -- this chunk's own
declared delta, not re-anchored per the Maintainer fence. **1**
(`test_quickstart_sequence.py::...test_step3_install_writes_expected_kernel_and_modules`)
was this chunk's own quickstart-slot-count miss, fixed in `6b488a2` (confirmed
green above). **2**
(`test_verification_boundaries.py::test_both_operational_surfaces_fail_to_full`,
`::test_review_doctrine_requires_targeted_falsification_and_six_triggers`) are
**pre-existing and unrelated**: `git diff` shows this session made zero changes to
`AGENTS.md` (Cairn's own root) or `doctrine/dual-review.md`, the two files these
tests read, and both tests were still red at the same failing assertions after
this pass's commits, against files this plan never touches. Not fixed here;
reported to the Maintainer as a pre-existing gap outside this plan's scope.

**AST delta**, measured against `bootstrap/tests/fixtures/scaffold_ast_baseline.json`
via `_ast_attest._classify` over the live `bootstrap/_scaffold/*.py` tree at HEAD
`6b488a2`: **CHANGED 1, MISSING 0, DUPLICATE 0, NEW 80.** The one CHANGED symbol
is `Assign:_MODULE_MAPPINGS` (`config.py`), matching this plan's own declared A3
delta exactly. The 80 NEW symbols are **not this plan's** -- `git diff --stat
bootstrap/_scaffold/` against the pre-session baseline shows exactly one 15-line
insertion inside the existing `_MODULE_MAPPINGS` dict literal, no new top-level
symbol; the 80 NEW entries come from other in-flight cluster scopes' already-
landed or concurrent work in the same shared tree. Per the Maintainer fence: not
re-anchored, `update_symbol` not run, no ceremony requested.

**Install-contract movement.** `install_manifest(modules=None)`: **98 -> 100**
data rows (two additive: `dev/modules/security-verification.md` substituted,
`scripts/run_security_verification.py` verbatim), **45 -> 46** verbatim `.py`
rows, `duplicate_destinations` -> `{}`. The `44/45 -> 46` `.py`-count pins in
`test_security_lint.py` and `test_notice_install.py`, and the `98 -> 100`
manifest-row pin in `test_notice_install.py`, all moved in `6e3a8ed`/`6b488a2` --
three pins, not two, matching this plan's own warning that
`api-web-security-modules` shares two of the same three pins and whoever lands
second re-measures.

**Release gate.** `bootstrap/security_check.py` itself refuses on a dirty
worktree (by design; a release-only gate), so it was not run end-to-end. Bandit
run directly over the new file:
`python -m bandit -q templates/modules/default-on/run_security_verification.py`
-> **2 LOW** (`B404` subprocess import, `B603` subprocess-without-shell=True),
**0 MEDIUM+**, matching `run_security_audit.py`'s established profile per this
plan's own prediction.

**Doc gates.** `scripts/claim_check.py` over each edited/new Markdown file
(`templates/modules/default-on/security-verification.md`,
`templates/core/AGENTS.md`, `docs/quickstart.md`) -- OK, 0 hard flags after two
`claim-check-allow` directives for the two adopter-tree-only forward references
named above. `scripts/check_cairn.py` -> 4 issues, all attributed to a single
`dev/plans/` archive-move a concurrent session made in the same shared tree
while this pass ran, none to a file this plan touches. `scripts/quality_gate.py --sub
neutrality` -> `fail=96 info=21` (re-taken at `6b488a2`; the plan's own quoted
`fail=95` baseline is stale, per its own warning) -- zero fail lines attributable
to a file this plan touches, confirmed by grep.

**Perturbation ledger -- demonstrated, not just described.** Six hazard
mutations applied to the committed dispatcher source, run, confirmed RED at
exactly the predicted row(s) and no other, reverted, and confirmed byte-identical
via `git hash-object` before/after (`9f3a2e2b...`):

| Test | Mutation | Result |
|---|---|---|
| T1 | Added a dormant entry to the shipped `_REGISTRY` | RED: `assert fresh._REGISTRY == {}` fails, showing the injected entry |
| T4 | Widened `_EVIDENCE_MODES` to include `"deployed"` | RED on exactly the `deployed` parametrized row; other 6 rows stayed green |
| T14 | Disabled the exit/result agreement check (`if False:`) | RED on both `exit0-findings` and `exit1-clean` rows |
| T18 | Replaced `_is_regular_and_unsymlinked` with plain `path.is_file()` | RED on both `leaf-symlink` and `parent-symlink` rows |
| T21 | Added a `"...is CLEAN"` line to the NOT_APPLICABLE path | RED on the forbidden-wording assertion; T20 (exact-line assertion) unaffected |
| T44(b) | Made `_record_keys_ok` always return `None` | RED on the lockfile-record-side row only; T44(a)'s five construction-side rows unaffected |

**Not individually mutation-tested this session** (a stated completeness gap,
not a claim of coverage): T2, T3, T5, T6-T13, T15-T17, T19, T20, T22-T24,
T36-T40, T41, T44(a). Each is exercised by the suite's own green run against the
real hazard named in its own docstring (a real subprocess child, a real
lockfile record, a real symlink, etc. -- none is a mocked reimplementation of the
subject), but the mutate-run-revert-confirm cycle was not individually performed
and demonstrated for each. Completing the remaining ledger is unfinished work,
named here rather than implied by the green suite above.

**Known omissions.** Chunks B (universality / `_DEFAULT_ON_MODULES`), C
(non-silent install / `cli.py`), D (`SAFETY.md`, the `templates/modules/README.md`
row, `CHANGELOG.md`) are entirely untouched -- no file under those chunks was
created or edited. `api-web-security-modules` (the reciprocal plan) is entirely
untouched: its Chunk A (the shared `_security_net` engine -- URL normalization,
SSRF/DNS-rebinding defense, redirect policy, TLS) is the pair's own named
highest-risk surface and was not attempted in this session; every other chunk in
that plan depends on it.

## Maintainer ratification of the B3 living-state narrowing -- Anthony Kendall -- 2026-08-10

**Authorization, quoted verbatim and visually isolated:**

> Ratify

**What it answered, recorded so the record stands alone.** The one-word
authorization was given in direct answer to a question that named this narrowing,
summarised its effect, and closed *"Ratify, or want me to dig into anything
first?"* -- so the referent is the **B3 `policy_binding_mode: living_state`
admission fence** and nothing else. Scribed by Claude (Implementation). This block
is shared verbatim with the reciprocal plan and lands in both files in the same
commit, as the shared block requires.

**The narrowing, stated as what it drops.** The accepted proposal's revision
established parent-computed digest binding over *"the runner and policy"*.
`policy_binding_mode: living_state` keeps the runner digest binding and **drops the
policy content-digest comparison** for a declared class of records.

**Why the Maintainer accepted it -- the class is five human-edited coordination
documents, not "any policy."** `_LIVING_STATE_DSTS`
(`bootstrap/_scaffold/lockfile.py:84`) is a five-entry `frozenset`:
`dev/PLANNING.md`, `dev/NEXT_SESSION.md`, `dev/.cairn/cairn_foldback.md`,
`dev/collaboration_agreement.md`, `dev/.cairn/model-selection-mapping.yml`. Every
one is a file a human edits continuously; hash-pinning them would report ordinary
work as tampering. **The boundary is enforced by the verifier, not trusted from the
lockfile** -- `lockfile.py:80-83` records that `verify_integrity` honours
`living_state` only for a `dst` in that set and fails closed on any other record
asserting it, *"so a modified script cannot hide by flipping the flag."* A shipped
script therefore cannot opt itself into unverified status.

**The risk accepted, named rather than implied.**
`dev/collaboration_agreement.md` is in that set and it carries decision rights. An
unnoticed edit to it will not be caught by integrity checking; its protection is
git history and review, not a hash. The Maintainer was shown this specific
consequence before ratifying.

**What this unfences.** `F2` and **all of Chunk G** in
`dev/plans/api-web-security-modules.md`, and registry admission under
`"living_state"` in `dev/plans/security-verification-activation.md`. An
implementing agent may now admit such an entry and land the chunk that writes the
living-state record.

**What it does NOT do, enumerated so nothing further is read into it:**

* It does not widen `_LIVING_STATE_DSTS`. Adding a sixth entry is a separate
  change to an engine constant and carries its own Security Review.
* It does not relax `runner_binding_mode`, which remains the one-member set
  `{"immutable_digest"}`.
* It does not waive the four refusals already built and tested -- a record lacking
  `living_state: true`, a path outside the authoritative set, an
  `immutable_digest` declaration over a living record, and post-construction mode
  mutation all still fail closed at DEGRADED (20).
* It does not discharge any review tier, authorize a push, or open the AST
  re-anchor ceremony.
* It does not close the `verify_integrity.py:63-111` extra-key gap, which neither
  plan in this pair owns.
