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
`dev/proposals/2026-08-03-codex-security-verification-activation.md` and moves to
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
* **Admitted** — a registry entry that cleared the five-part admission rule in
  the proposal's revision (accepted capability proposal; reviewed plan with
  execution evidence for that exact mode; complete lockfile mapping group; schema
  and precedence tests; a Security Review of the registry change). At v1 nothing
  is admitted, so the registry is empty.
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

**Three things in this plan are not an implementing agent's to do.** They are
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
3. **The gate-manifest re-pin.** No file this plan edits is in the 164-entry
   `frozen_files` map (measured above), so no `FROZEN-MODIFIED` row is expected —
   but `bootstrap/tests/test_security_lint.py` and
   `bootstrap/tests/test_notice_install.py` carry the two `44` pins and **should be
   re-checked against the map at implementation**, because the map moves. If either
   turns out frozen, the implementing agent **records** the stale entry in the commit
   body and does not re-pin.

An additional standing rule for this plan: the Maintainer's serialization points
(`dev/PLANNING.md`, `CHANGELOG.md`) are edited at the defined moments only.

## Sequence

Chunk order is load-bearing. **A before B**: the dispatcher must be registered
and provably narrowing before it becomes universal, so that no intermediate
commit ships a default-on executable whose behavior is unpinned. **C after B**:
the install message names a command that must already install.

```
0. plan-open  -- this plan + the dev/PLANNING.md row-move            [commit pending]
   (plan review) -- required(External, security lens); NO code before it lands
1. Chunk A -- the dispatcher + its module, registered, not universal [commit pending]
   >>> MAINTAINER FENCE: AST re-anchor #1 (Assign:_MODULE_MAPPINGS)
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
| A1 | `templates/modules/default-on/run_security_verification.py` *(new)* | The dispatcher. Standard library only. Module-level `_REGISTRY: dict[str, RegistryEntry] = {}` — **empty**, with the nine admission fields as a frozen dataclass/`NamedTuple` (`module_id`, `runner_repository_path`, `argv_mode`, `policy_repository_path \| None`, `child_schema_version`, `capability_contract_version`, `evidence_mode`, `accepted_process_exits`, `result_to_aggregate_mapping`). `evidence_mode` constrained to `frozenset({"offline", "loopback"})` at construction. Aggregate constants reuse the ladder already in `templates/modules/team-gated/run_security_audit.py` (`0/5/10/20`) plus `NOT_APPLICABLE`. Child invocation: `[sys.executable, "-I", <registry runner path>, <registry argv_mode>]`, `shell=False`, explicit minimal `env`, `timeout`, byte cap, strict UTF-8, strict JSON. SPDX header, matching every other shipped twin. |
| A2 | `templates/modules/default-on/security-verification.md` *(new)* | Module doctrine: the registry rules, the five-part admission rule quoted from the proposal's revision, the aggregate ladder and its precedence, trusted-checkout scope, the local/deployed separation **and its explicit non-claim** (not actor authentication), and recovery from INCOMPLETE / DEGRADED. Carries the `<!-- cairn:merge-target: AGENTS.md > security-verification -->` directive and the paired content block holding the exact standing command. Substituted (`verbatim=False`), so the merge pass reads it. |
| A3 | `bootstrap/_scaffold/config.py` | One new key in `_MODULE_MAPPINGS`: `"security-verification": [InstallSpec("default-on/security-verification.md", "dev/modules/security-verification.md"), InstallSpec("default-on/run_security_verification.py", "scripts/run_security_verification.py", verbatim=True)]`. **The only engine edit in this chunk.** Symbol delta: `Assign:_MODULE_MAPPINGS`. |
| A4 | `templates/core/AGENTS.md` | A new `## Security verification` heading with the `<!-- cairn:slot security-verification -->` / `<!-- cairn:end security-verification -->` pair, placeholder text on the `claim-check` slot's exact model (*"If security-verification is not installed, replace with `N/A: security-verification not installed`. An unfilled slot is a review finding."*). Plus one line in the *Project-specific conventions* guidance naming the dispatcher, its registry, its child result schema, and every registry entry as **high-risk Security Review surfaces**. |
| A5 | `bootstrap/tests/test_security_verification.py` *(new)* | The dispatcher suite, T1–T24 below. |
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
| T5 | `test_every_admission_field_is_required` — a deletion mutant per field: nine synthetic entries, each missing one of the nine, each refused at construction with a message naming the field. | Give any field a default. That field's row fails. *Weakness stated:* this pins the **validator**; that the shipped registry is empty is T1's job, not this one's. |

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
| T17 | `test_runner_or_policy_digest_mismatch_is_degraded` — write the lockfile, then flip one byte of the runner (and, separately, of the policy); both `20`, no child launched. | Skip the comparison. Both rows fail. |
| T18 | `test_symlinked_runner_or_policy_is_refused` — three rows: symlinked leaf, symlinked parent directory, and a runner replaced by a symlink between the digest read and the launch (the latter asserted as a **named residual**, not as closed). | Open with plain `open()` and no `is_symlink()` / regular-file check. The first two rows fail; the third is documented as the accepted trusted-checkout race the proposal states rather than claims closed. |
| T19 | `test_missing_lockfile_record_for_a_registered_runner_is_degraded` — registry entry present, lockfile record absent; `20`. | Treat a missing record as "unlocked, proceed". Fails. |

*The universal no-capability contract — the E2 surface.*

| T | Test | Hazard perturbation → RED |
|---|---|---|
| T20 | `test_no_capability_prints_the_exact_not_applicable_line_and_exits_0` — stdout contains exactly `NOT APPLICABLE: no selected local security capability`, exit `0`, machine result `aggregate: NOT_APPLICABLE`, `legs: []`, a non-empty `reason`. | Make the no-capability path return `CLEAN`. Fails on both the literal and the machine field. *The hazard is the false-security claim, not the string* — a string-only perturbation would be a body edit and is not the one recorded. |
| T21 | `test_no_capability_output_uses_no_security_coverage_wording` — human **and** machine output scanned for `CLEAN`, `secure`, `passed security`, `no vulnerabilities`, `verified`; none present. | Same hazard as T20. Also fails if a later author adds a friendly *"all clear"* line. |
| T22 | `test_no_capability_opens_no_socket_and_does_no_dns` — `subprocess.run`, `socket.socket`, `socket.create_connection`, `socket.getaddrinfo`, `urllib.request.urlopen` all monkeypatched to raise; run; exit `0`. | Add a socket open on the no-capability path. Fails. |
| T23 | `test_dispatcher_source_reads_no_deployed_credential_variable` — an **AST scan of the dispatcher source file**, asserting every `os.environ` / `os.getenv` read resolves to the declared allowlist and no deployed-credential variable name appears as a literal. | Add `os.getenv("AWS_SECRET_ACCESS_KEY")` to A1. Fails. **Channel note**: the oracle is the source text; the subject is the runtime behavior. Independent — the dispatcher never reads its own source. |
| T24 | `test_a_socket_opening_child_is_excluded_by_admission_not_blocked_at_runtime` — the proposal's specific ask, in two halves. (a) A fixture child that calls `socket.socket()` and binds `("127.0.0.1", 0)` — no outbound traffic — cannot be admitted, because admission requires an accepted capability contract and the shipped registry is empty. (b) Force-injected into `_REGISTRY`, the parent **does** run it and **does not** prevent the bind; the test asserts that, documenting the residual honestly. | For (a): remove the admission check so an arbitrary path becomes reachable; (a) fails. For (b) there is deliberately **no** perturbation that makes the parent block the socket — that is the finding, and the test's docstring says so where a reader will find it. |

**Acceptance criteria — Chunk A.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_security_verification.py bootstrap/tests/test_security_lint.py bootstrap/tests/test_notice_install.py -q` → all pass, 0 skipped.
* **Install-contract movement, as a contract change with its own criteria** — not
  a side effect:
  * `python bootstrap/scaffold.py --manifest` → **97** data rows (95 + 2).
    Diffed against a capture taken at the plan-open commit; the diff must be
    **exactly two added lines** and **zero modified or removed** lines. A modified
    row means an existing destination moved — stop and re-review.
  * The two rows are `dev/modules/security-verification.md` (substituted) and
    `scripts/run_security_verification.py` (verbatim), in that tab-separated
    format.
  * `duplicate_destinations` over the full manifest → empty. No existing adopter
    path is shadowed.
  * A fresh scaffold's lockfile records **both** files with hashes — the complete
    mapping group — verified by reading `dev/.cairn/cairn-lock.yml` in a
    `tmp_path` install, not by asserting the writer was called.
* `python bootstrap/security_check.py` → `PASS`, Bandit line reporting **75**
  files (74 + the dispatcher). **The dispatcher is newly scanned Layer-4 code**;
  if it produces a MEDIUM+ finding the gate goes red and the fix is the code, not
  the allowlist. Expect LOW `B404`/`B603` from the `subprocess` family, matching
  `run_security_audit.py`'s existing profile.
* The two `44 → 45` pins move **together**, in this commit.
* **AST**: `_ast_attest.py verify` reports exactly **one** CHANGED symbol,
  `Assign:_MODULE_MAPPINGS`, baseline `26957a8924042a0a` → measured value. Any
  second symbol is a stop-and-explain. **Then stop** — the fence.
* **Perturbation ledger in the commit body**: for each of T1–T24, the change made,
  the failure observed with its message, and `git diff <path>` empty after
  restore. T24(b)'s deliberate non-perturbation is recorded as such.
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
| B5 | `bootstrap/tests/test_security_verification.py` | T25–T33 below. |

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
| T33 | `test_the_dispatcher_runs_green_from_a_real_fresh_scaffold` — end-to-end: scaffold into `tmp_path`, run `python scripts/run_security_verification.py local` **as a subprocess** from that tree, assert exit `0` and the exact `NOT APPLICABLE` line. The public path, not an import. | Break the lockfile read path (point `_LOCKFILE` at a non-existent relative location). Fails with DEGRADED rather than 0 — proving the test exercises the real file layout, not a stub of it. |

**Acceptance criteria — Chunk B.**

* `~/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests -q` → green apart from
  the AST-attest pair, which is red **by design** until the fence clears. Record
  the exact node ids so a reviewer can see nothing else moved.
* [`bootstrap/tests/test_quickstart_sequence.py`](../../bootstrap/tests/test_quickstart_sequence.py)
  green — it asserts *prose == live*, so B3 is correct only if this passes.
  `python scripts/measurements.py` likewise, for the
  `solo_greenfield_module_count` invariant.
* `python scripts/check_cairn.py` → OK; **≥ 181** Markdown files (180 + B2), and
  the count may only grow.
* `python scripts/quality_gate.py --sub neutrality` → `fail` unchanged at **95**.
  `templates/modules/*.md` and `docs/*.md` are inside its scan roots, so B2/B3/B4
  pass through it and the figure moving is a finding.
* The new module doctrine passes the content scanner:
  `python templates/modules/team-gated/content_scan.py
  templates/modules/default-on/security-verification.md` → no flags. Already
  probed for the slot text; re-run over the full file.
* **AST**: exactly **one** new CHANGED symbol, `Assign:_DEFAULT_ON_MODULES`,
  baseline `2c8ef688f6865487`. Report; do not re-anchor.
* **Perturbation ledger** for T25–T33 in the commit body, T30's deletion mutant
  called out by name.

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
| D1 | `bootstrap/SAFETY.md` | The four recordings the proposal names, sited in Rule 7's Layer-4 discussion and the self-check: (a) the scaffold now ships a file that **executes a child process** in an adopter tree; (b) that dispatch is gated on lockfile integrity and parent-computed digests; (c) the child's environment is reduced from ambient, with proxies and credential-bearing variables stripped; (d) **command separation is not actor authentication** — a person or agent with shell access can invoke another script directly, and Cairn does not claim to distinguish a human process from an agent process. (d) is the sentence that must not be softened. |
| D2 | `templates/modules/README.md` | One `default-on` row. Re-read first — `default-security-stance` adds one too. |
| D3 | `CHANGELOG.md > Unreleased > Added` | One line: a default-on local security-verification dispatcher and its `AGENTS.md` standing rule; registry ships empty, so a no-capability install reports `NOT APPLICABLE` and gathers nothing. Cross-reference proposal and plan **by stem**. Written at its serialization point. |

**Acceptance criteria — Chunk D.**

* `python scripts/check_cairn.py` → OK.
* `python scripts/quality_gate.py --sub neutrality` → `fail=95`, unchanged.
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
    Maintainer's re-anchor**. Baseline `1744 passed, 2 failed`, `as_of 2026-08-04`,
    where the two failures are the AST pair caused by a concurrent scope's
    uncommitted edits — re-baseline before comparing. Collection grows by exactly
    the new nodes and drops none.
  * `bootstrap/tests/test_security_verification.py` — T1–T35, the plan's own
    surface. *(Forward reference: the file lands at Chunk A; registered under
    `Proposed paths:` above.)*
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
  → 97 rows, diffed to exactly two additions. `python bootstrap/security_check.py`
  → `PASS` over 75 files. A fresh `tmp_path` scaffold followed by `python
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
  Bandit line reporting **75** files. Baseline before Chunk A: 74.
* **The install-contract diff** — `python bootstrap/scaffold.py --manifest`
  captured at the plan-open commit into the session scratch directory, diffed
  after Chunk A. **Expected: exactly two added lines, zero modified, zero
  removed.** 95 → 97 data rows.
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
