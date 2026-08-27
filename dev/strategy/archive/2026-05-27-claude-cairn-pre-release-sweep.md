<!-- Migrated 2026-06-12 from modflow_tools dev/strategy/ (Cairn's development home before self-hosting). Authored from modflow_tools' vantage; some path cites and "current state" reflect that origin and are being adapted to Cairn. Preserved as Cairn's living deliberation record -- see dev/strategy/MIGRATION.md. -->
<!-- ^ `dev/.cairn-upgrade/` is the transient upgrade-staging dir `scaffold.py`
     creates during an upgrade; it does not exist in a normal checkout. Cairn-tree
     paths in this doc carry the `cairn/` prefix (first segment not a local dir,
     so unflagged); modflow_tools paths are written in full. -->

<!-- Archived 2026-08-26: the version-independent procedure lives in
     docs/release-process.md (extracted earlier; two remaining techniques
     hoisted at archive time). This file is the preserved provenance — the
     v0.2.0 instance, its findings, and the lessons that produced the
     roster. -->

# Cairn pre-release sweep — a version-independent release strategy

**Initiating author**: Claude (Strategy & Research Agent)
**Model**: Opus 4.7 (1M context) — strategy tier
**Date**: 2026-05-27 (initiated for the v0.2.0 cut; generalized 2026-06-06)
**Status**: living
**Type**: living-reference
This file is two things at once: a **version-independent framework** for any
Cairn pre-release sweep (the roster of typed sweeps in §2–3, the shared
method in §4, the cut gate in §5), and its **current instance**, v0.2.0
(§1.1 + the `[v0.2.0]`-tagged notes throughout). Each *sweep type* is its own
section, authored and owned by the agent running it. Not yet a commitment:
the sweeps run on the maintainer's go-ahead, and findings route through the
normal lifecycle. **Generalized (2026-06-06)**: exercised on the v0.2.0 cut,
this is now the **version-independent** pre-release-sweep playbook — v0.2.0
retained as the reference instance (per the reading convention below). The
framework parts remain a candidate to fold up into a `cairn/doctrine/`-level
"pre-release sweep" practice (Cairn lacks one), so a future cut inherits the
roster rather than reconstructing it.
**Subject**: the Cairn repository (`~/Code/cairn/`); reusable across cuts,
with v0.2.0 as the first instance.

**Reading convention**: framework prose is version-independent; anything
specific to the current cut is marked **`[v0.2.0]`** so a future sweep can
keep the framework and replace only the instance notes.

**Path convention**: `cairn/...` paths are relative to `~/Code/cairn/`;
modflow_tools paths are written in full. The `cairn/` prefix also keeps the
modflow_tools `claim-check` gate quiet (Cairn's top-level dir names collide
with modflow_tools' own).

External-repo paths: `cairn/scripts/check_cairn.py`, `cairn/bootstrap/`,
`cairn/doctrine/`, `cairn/dimensions/`, `cairn/templates/`,
`cairn/CHANGELOG.md`, `cairn/CITATION.cff`.

**Why this lives here**: Cairn has no `dev/` tree of its own, so per the
standing Cairn PR-flow the deliberation lives modflow_tools-side; the sweep
work and any fixes land in Cairn via PR-flow.

---

>  **The procedure now lives in [`docs/release-process.md`](../../docs/release-process.md).**
>  That page is what a Maintainer runs; this note is the provenance behind it —
>  the v0.2.0 instance, the per-sweep findings, and the reasoning that produced
>  the roster. Do not rediscover the release process here.

## 1. Why a pre-release sweep (version-independent)

Three structural forces make a whole-tree sweep worth running before *any*
Cairn release, not just a large one:

* **Fold-back is monotonic accretion.** Cairn's improvement loop appends
  proven doctrine inward; nothing in the lifecycle pushes back toward
  consolidation. Duplication, stale doctrine, overlapping modules, and dead
  code grow *by construction* between cuts (this is also why Sweep G exists
  as a standing counter-pressure, not a one-off).
* **Concurrent multi-agent authorship.** A release batch is landed by many
  agents and sessions; each change is reviewed in isolation, but no
  per-change review is scoped to whole-tree **coherence**, **currency**, or
  **adopter cold-start safety**.
* **The blast radius is downstream.** Cairn's templates become every
  adopter's governing instructions; an incoherence, stale pointer, or
  dangling reference shipped at a cut propagates to every adopter at once.

A comprehensive sweep before incrementing the version is therefore a
**standing Cairn practice**. The sweep is a **gate on the cut, not a blocker
on the work**: it surfaces findings and lets the maintainer triage what is
in-scope-for-cut vs. deferred — then the cut proceeds (§5).

### 1.1 Current instance — `[v0.2.0]`

v0.2.0 is a **large** first batch relative to v0.1.1 — the usability spine
(P1–P5: reference scripts, security four-layer, practice modules, governance
presets, intents tool), the **module upgrade** capability (3-way merge +
lockfile), **security-hardening**, and several **doctrine fold-backs** from
the reference deployment (remaining-ledger A–D, the doc-governance /
reviewer-scribing / fold-back-mechanism arc, and the process-hardening arc).
The `CHANGELOG > Unreleased` carries dozens of entries, landed by **many
concurrent agents in one day** — the textbook case for all three forces
above, which is why the maintainer called for the comprehensive sweep this
document coordinates.

## 2. The sweep program — a roster of typed sweeps

The pre-release sweep is **composed of typed sweeps**, each a focused pass
with its own lens, owner, and findings report. They are independent and can
run in parallel (different lenses, different agents); they converge on one
shared findings surface the maintainer triages before the cut.

| # | Sweep type | Distinct question (lens) | Owner | Status |
|---|------------|--------------------------|-------|--------|
| A | Documentation / doctrine-coherence | Do the docs/doctrine cohere, stay current, and read safely cold? | Claude (Strategy) | **run 2026-05-27** — clean L1–L2; 3 findings (A-1 doctrine-refs, A-2 stale catalog, A-3 nit), awaiting triage (§3 A) |
| B | Security & supply-chain | Is the agent-instruction supply chain + the executables safe, and is today's hardening complete? | tbd (Security Review) | scoped (§3 B) |
| C | Bootstrap & tooling integration | Does the *machinery* actually work end-to-end for a fresh adopter (not just the docs about it)? | Claude (Strategy) | **run 2026-05-27** — PASS (scaffold + lockfile + init-lock + non-clobbering 3-way merge all validated end-to-end); 2 nits (C-1, C-2) (§3 C) |
| D | Test & verification health | Does the suite actually *prove* what shipped (coverage, skips, determinism)? | Claude (Strategy) | **run 2026-05-27** — near-PASS (281/2; skips justified; surfaces covered); D-1/D-2 minor, D-3 order-independence unverified (§3 D) |
| E | Vendor / project neutrality | Do the shipped templates/doctrine leak any vendor or project name? | Claude (Strategy) | **run 2026-05-27** — prose PASS; **E-1 + E-3 → fix** (maintainer Decision: no provenance/dev-attribution in code), E-4 mechanize lint, E-2 low (§3 E) |
| F | Release-mechanics & provenance readiness | Can the cut itself proceed cleanly (version files, CHANGELOG, tag/provenance posture)? | Claude (Strategy) | **run 2026-05-27** — PASS (CITATION ready, version single-sourced, CHANGELOG renamable); F-1 nit (Added-vs-Changed split) (§3 F) |
| G | Redundancy / consolidation | Is there **duplicate or unnecessary functionality** across the whole tree — docs, code, *and* capabilities — to consolidate or remove? | Claude (Strategy) | **run 2026-05-27** — first-pass PASS (layer contract holds; no confirmed dup in churn surfaces); deep R1/R6/R7 gated on the G/E-4 linter (§3 G) |

This is the **recommended roster** — seven orthogonal lenses whose union
covers the tree without every agent re-reading everything. The roster is the
**reusable framework**; only the per-sweep *status* and the `[v0.2.0]`
instance notes change cut-to-cut. Ownership is **open**: the maintainer
assigns, and an agent planning a sweep slots into the matching row (refining
its section) or adds a new one via the **template at the end**. The lenses
overlap a little by design — E's neutrality lint is also a sub-check in A;
F's CHANGELOG readiness touches A's coherence layer; G's R1–R3 redundancy
categories overlap A's coherence pass (G owns the systematic technique, A
catches them in-pass for the cut) — but each **owns a distinct question** so
a finding has one home. If the roster reads as too granular for a given cut,
the natural consolidations are **E → A** (neutrality as an A sub-lens) and
**F → C** (release-readiness as part of tooling integration); keep them split
only when distinct owners run them. A, B, and G are the most-developed
lenses; B is also the most *advanced in execution* (its work is largely done
— see §3 B).

## 3. The sweeps

### Sweep A — Documentation / doctrine-coherence

**Owner**: Claude (Strategy). **Scope**: the Cairn tree only. **Output**: a
*findings report first* — survey, then a prioritized findings list the
maintainer triages, then fixes (so scope decisions happen before edits).

Four layers, cheapest-and-most-objective first:

**Layer 1 — mechanical gates (automated; catches *drift*).**
* `python scripts/check_cairn.py` — exit 0 over the whole tree (link/claim
  integrity).
* `python -m pytest bootstrap/tests/` — green.
* `python bootstrap/scaffold.py --manifest` — matches the shipped module set
  (e.g. the default-on roster, which gained `fold-back-ledger`).

*Baseline 2026-05-27 (pre-sweep): all green — check_cairn OK (69 files),
bootstrap 264 passed / 2 skipped. So nothing is **broken**; the value is in
layers 2–4.*

**Layer 2 — coherence / consistency (needs reading, not gates).** The real
work after a high-churn day:
* The new + edited doctrine surfaces cohere and cross-reference correctly:
  `cairn/doctrine/doc-governance.md`, `fold-back.md` (new), and the edits to
  `coordination.md`, `lifecycle.md`, `session-routines.md`, `roles.md`,
  `rationale.md`; `cairn/bootstrap/UPGRADE.md` (new).
* **One-canonical-home** is respected — no duplication drift (the rule
  `doc-governance.md` itself just shipped); each rule has one home, others
  point.
* **No contradictions** across surfaces (e.g. one module saying "deferred"
  while another says "shipped" — the class the process-hardening review
  caught).
* **Vendor-/project-neutrality**: no leaked modflow_tools paths or vocabulary
  in Cairn doctrine.
* `CHANGELOG > Unreleased` reads coherently across all v0.2 entries and is
  ready to rename to `0.2.0`.

**Layer 3 — currency (do the docs match what shipped?).**
* The install manifest vs. `_MODULE_MAPPINGS` / `_DEFAULT_ON_MODULES`.
* `PROVENANCE.md` + `fidelity-check.md` reflect the new lockfile + upgrade
  capability; the lockfile is the one-way authority the fidelity manifest
  cites.
* `BOOTSTRAP.md` Act I current (preset-aware); the case studies
  (`case-studies/modflow_tools.md`, `lhm.md`) current; module-roster docs
  match the default-on set.

**Layer 4 — adopter cold-start coherence (highest value, least automatable).**
* Walk the fresh-adopter path — on-ramp → `BOOTSTRAP.md` → doctrine →
  *installed* templates — for dangling pointers or contradictions. The
  concrete tool is a **scaffolded-target smoke check**: scaffold an adopter
  and confirm installed files contain no unresolved adopter-local references
  (the exact class the process-hardening code-review P2 caught — installed
  files pointing at a non-installed `doctrine/fold-back.md`). **Exclude the
  `dev/.cairn/base/` upgrade-ancestor cache from this scan** — it holds raw
  *pre-substitution* templates by design, so it floods the scan with
  expected `{{tokens}}` and base-copy references (lesson L1 below).

**Method**: survey produces a prioritized findings report (blocker /
should-fix-for-cut / defer); fixes then route by size — mechanical (broken
link, stale manifest line) as direct commits; substantive (a doctrine
contradiction, a missing surface) through the proposal/plan lifecycle.

**Timing note**: layers 2–4 run *after* the process-hardening change lands
(done 2026-05-27), so its surfaces are surveyed in final form.

#### Findings — 2026-05-27 run

Layer 1 **clean** (`check_cairn` OK, 69 files; `bootstrap/tests/` **281
passed / 2 skipped**; default-on roster correct incl. `fold-back-ledger`).
Layer 2 prose **clean** (no vendor/project leak in `doctrine/`/`templates/`
prose; the claim-check↔work-intent pre-commit-hook contradiction the
process-hardening review flagged is **resolved** — the distinction note
landed). Three findings:

* **[A-1] (should-fix-for-cut / maintainer call) — pervasive
  unqualified `doctrine/…` references in installed files.** Adopter-facing
  installed files — `AGENTS.md`, `dev/PLANNING.md`, `dev/agent_collaboration.md`,
  `dev/NEXT_SESSION.md`, `dev/modules/lifecycle-metrics.md`,
  `dev/proposals/_template.md` — reference `doctrine/<x>.md` paths, but the
  scaffold does **not** install `doctrine/` into adopters, and **no
  convention statement anywhere** says these mean "Cairn's *published*
  methodology doctrine, not a file in your tree." This is the
  process-hardening code-review **P2 generalized**: that review fixed the
  *fold-back* instance inline (and the claim-check module qualifies its
  ref), which now makes those two **inconsistent** with the bare core refs.
  *Recommended fix (cheapest, one-canonical-home):* a single statement in
  the installed `AGENTS.md` (or the on-ramp) — "`doctrine/…` references
  point to Cairn's published methodology doctrine, not files in this tree"
  — rather than qualifying every ref or installing `doctrine/`. Maintainer
  call: that single clarification vs. installing/linking `doctrine/`.
* **[A-2] (should-fix-for-cut, mechanical) — stale module catalog.**
  `cairn/templates/modules/README.md`'s "## The modules" table lists
  `lifecycle-metrics` / `claim-check` / `reflections` but **not** the new
  default-on `fold-back-ledger` module. One-row fix.
* **[A-3] (nit / defer) — dev-history attribution in shipped tooling.** The
  shipped `.py` tooling carries development-history comments (`Antigravity
  2026-05-26`, `code-review P2`, example names `Codex` / `Alice`). Cosmetic
  neutrality only; the harness-session-ID registry
  (`CLAUDE_CODE_SESSION_ID`, `CODEX_THREAD_ID`, `ANTIGRAVITY_TRAJECTORY_ID`
  in `intent.py`) is **functional and stays**.

Currency (Layer 3): `PROVENANCE.md` + `fidelity-check.md` reflect the
lockfile/upgrade; `BOOTSTRAP.md` is preset-aware. Disposition pending
maintainer triage (findings-report-first); A-1 likely wants a maintainer
call, A-2 is a mechanical direct-commit, A-3 defers.

#### Lessons learned — 2026-05-27 (carry forward)

* **L1 — the upgrade base-cache is survey noise.** `dev/.cairn/base/` holds
  raw pre-substitution templates (the upgrade ancestor), so any Layer-4
  token/reference scan must exclude it (`grep -v '/.cairn/base/'`) or it
  floods false positives. Folded into the Layer-4 check above. *(General
  to any sweep that scans a scaffolded tree — Sweep C/E should heed it.)*
* **L2 — a per-change review finding is often the tip of a class.** P2 was
  fixed in isolation; this sweep found the pattern is pervasive *and* that
  the inline fix created an inconsistency. The sweep's distinctive value is
  exactly this: **generalize a per-change finding across the tree** — the
  cross-cutting lens per-change reviews structurally cannot provide
  (validates §1). A method note for **all** sweeps: when a finding matches
  a shape a prior per-change review already touched, check whether the
  prior fix was *localized* and the shape is *systemic*.
* **L3 — gates-green ≠ coherent (confirmed).** Layer 1 was fully green while
  Layer 4 carried the headline finding. The framework's "the value is in
  layers 2–4" prediction held; do not let a green gate shorten a sweep.

### Sweep B — Security & supply-chain

**Owner**: Security Review (Claude, focused mode). **Scope**: the Cairn
executables + the agent-instruction supply chain. **Lens**: is the surface
safe, and is the release's security-hardening *complete and coherent* — not
just landed? **Output / status**: this is the **most-advanced sweep —
substantially executed**. Its plan, findings, *and* resolution already live
in the canonical security-review artifact
`dev/strategy/archive/2026-05-22-claude-cairn-security-review.md` (one-canonical-home:
this section **points**, it does not duplicate). Sweep B is the framework's
"security lens"; the security-review doc is its running instance.

**The plan — the four-layer control model** (the security review's frame,
which a security sweep re-validates each cut):
* **Layer 1 — Release provenance**: named release artifacts, signed tags /
  maintainer-approved release commits, the published install `--manifest`,
  "scaffold from releases, not branches" (`git_provenance_warning`,
  `PROVENANCE.md`).
* **Layer 2 — Source integrity**: scan + review *by file class*
  (`content_scan.py` composed by `check_cairn.py`; `cairn-accept` reasoned
  suppressions).
* **Layer 3 — Generated-output integrity**: scan what agents actually read
  (the *filled* templates), not just the source.
* **Layer 4 — Executable hardening**: containment guards, no shell-injection,
  fail-closed integrity (`_assert_safe_write`, `verify_integrity.py`).

Plus the **code-surface review** (deserialization / command-injection /
path-traversal / SSRF classes) and the **prompt-injection threat model**
(T1 upstream-template compromise, T2 profile-borne injection, T3 obfuscated
content) — the distinctively-Cairn risk a code scanner misses.

**`[v0.2.0]` status — largely complete.** The 2026-05-22 review *proposed*
the four layers; the **2026-05-27 follow-up full review** (post-P2, pre-cut,
maintainer-directed, full scope) verified they *shipped* and audited the
enlarged surface (1 file → **8 Python files, ~4,900 LoC**); the
**security-hardening arc** then closed the findings (SSRF guard on
`link_check --check-external`, a *derived* Bandit gate, the `content-security`
adopter module, fail-closed `verify_integrity.py`, public `SECURITY.md`,
`SAFETY.md` Rules 7–9) — recorded in that doc's Resolution section. Overall
posture: **strong** (no Critical; Important findings resolved).

**Residual for this cut** (the only open B items): the cross-type **confirm
pass** (a *different agent type* re-runs the audit — the security protocol's
make-it-prove-itself tier) and running the **Bandit gate in an env where
`bandit` is installed** (it was absent in the follow-up's env, so
`test_security_lint` was not exercised there). Both are named in the
security-review doc's "Coverage gaps".

**Timing / dependencies**: executed relative to the landed work; the confirm
pass + bandit-in-env are the gating residuals before the cut.

### Sweep C — Bootstrap & tooling integration

**Owner**: tbd. **Scope**: the bootstrap machinery, exercised end-to-end.
**Lens**: does an adopter's *machinery* actually work — scaffold, upgrade,
fidelity-check — not just the docs describing it? (Distinct from A's layer-4
cold-start *read*: this one **runs** the tools against a fixture tree.)

**Checks** (each **run** against a throwaway fixture tree, not read):
* **Fresh scaffold** of a clean target (`scaffold.py --config <profile>
  --target <tmp>`): exits 0; every manifest entry lands; tokens substituted
  (no stray `{{...}}` outside the documented doc-author placeholders); block
  slots present and unfilled; the default-on roster is correct (incl.
  `fold-back-ledger`); `--manifest` equals what landed. *Finding shape*: a
  manifest/disk mismatch, a substitution that left a token, or a write that
  escaped `target`.
* **Upgrade round-trip** on a fixture — the capability's first real exercise:
  install vN → **customize** (fill a slot, edit prose, tweak a verbatim
  script) → `upgrade --plan` (drift inventory correct) → `--stage` (a
  reviewable merge) → `--apply` (swap) → assert **filled slots survive**,
  **prose conflicts surface with markers** (not silently lost or clobbered),
  the **verbatim-script hash policy** fires (update-if-unmodified,
  flag-if-forked), and the **lockfile advances** only on a marker-free tree.
  Then `--init-lock` on a *pre-lockfile* tree → review-only fallback where
  base is unrecoverable. *Finding shape*: a customization clobbered, a
  conflict auto-resolved, or `--apply` advancing past unresolved markers.
* **Fidelity + completeness**: `fidelity-check` passes on the scaffolded
  target, and the core-completeness probe (6a module-merge / 6b tacit-rule)
  finds the install doctrine-complete.

**Disposition**: a broken install path or a clobbering upgrade is a
**blocker for the cut** (the upgrade capability is brand-new and adopter-
facing); a cosmetic manifest-ordering nit defers.

**Timing / dependencies**: after the upgrade capability + `fold-back-ledger`
module landed (done). This is the **highest-leverage untested surface** —
the upgrade machinery shipped this cut and has not yet been exercised
end-to-end on a real fixture outside its own unit tests.

#### Findings — 2026-05-27 run

The headline untested surface, **exercised end-to-end on real trees** (via
throwaway scaffolds + non-invasive `git worktree` bases) — and it **works**:
* **Fresh scaffold**: exit 0; the lockfile (`dev/.cairn/cairn-lock.yml`, per-file
  `src/dst/hash/base_cache`) + base-cache (`dev/.cairn/base/`) written
  correctly; default-on roster correct.
* **Same-version `--plan`**: classifies cleanly (14 clean / 2 verbatim
  up-to-date) and lists un-installed team-gated modules as "new available."
* **`--init-lock` migration** (pre-upgrade base `c0d48ef` → HEAD): migrates a
  pre-lockfile tree, hash-tracks verbatim scripts, classifies
  token-substituted files as **review-only** ("no recoverable base — install
  token values never recorded") with a re-install note — the R6 + Codex-P1
  contract, verbatim.
* **Clean 3-way merge** (base `b71fcc7` → HEAD, AGENTS.md drifted upstream
  **and** locally customized): the staged
  **`dev/.cairn-upgrade/files/AGENTS.md`** preserves the local customization
  **and** folds in the upstream change — **non-clobbering, as promised**.
  `new-base/` holds the next base-cache; `stage-metadata.json` records the
  stage (R7); on-disk untouched (`--stage` is non-destructive).

Two minor findings:
* **[C-1] (nit) — the `--plan`/`--stage` summary lumps
  locally-modified-but-clean-merge files into `clean`.** A customized file
  that merges without conflict is reported as `clean`, indistinguishable
  from an untouched one, so the adopter is not told their customizations were
  merged. Correctness is fine; a `locally-modified (merged clean): N`
  sub-count would improve transparency.
* **[C-2] (should-fix-low) — the staging layout isn't self-orienting.**
  `dev/.cairn-upgrade/` has `files/` (the merged result the adopter
  reviews/resolves) and `new-base/` (the next base-cache) with no in-dir
  orientation; the stdout says only "resolve any conflicts." I initially
  mis-read `new-base/` as the result (and an adopter would) — a one-line
  `dev/.cairn-upgrade/README` or clearer naming prevents editing the wrong
  dir. (Verify `UPGRADE.md` doesn't already cover it.)

Disposition: **C is a PASS** — the highest-leverage untested surface is
validated end-to-end. C-1 / C-2 are nits / should-fix-low for the batch.

#### Lessons learned — 2026-05-27 (carry forward)
* **L4 — exercising the tool on a *real* tree caught what unit tests can't.**
  Both nits are real-tree usability observations invisible to the
  synthetic-fixture unit suite — validates Sweep C's "run it, don't just
  read it" premise.
* **L5 — non-invasive two-version testing via `git worktree`.** A pre-churn
  `git worktree add <old-commit>` gives a real "vN" base without touching the
  shared multi-agent checkout — the reusable technique for any future cut's
  upgrade round-trip. **Corollary** (the near-false-positive this run):
  before judging a clobber, confirm *which* staged dir is the merged result
  (`files/`, not `new-base/`).

### Sweep D — Test & verification health

**Owner**: tbd. **Scope**: `cairn/bootstrap/tests/` + any other test
surface. **Lens**: does the suite actually *prove* what shipped — or are
there coverage gaps, unexplained skips, or order/flakiness hiding behind a
green bar?

**Checks**:
* **Green + counted**: `python -m pytest -p no:cacheprovider bootstrap/tests/`
  passes; record the count as a baseline (`[v0.2.0]` baseline: **264
  passed / 2 skipped**, pre-process-hardening; re-baseline after it lands).
* **Skips are justified, not silent gaps**: enumerate each `skip` and
  confirm a documented reason (e.g. an env-dependent gate like bandit) — a
  skip with no reason is a coverage hole hiding behind a green bar.
* **New-surface coverage**: each surface that landed this cut has a test —
  the **upgrade** path (lockfile, 3-way merge, `--apply`, `--init-lock`),
  the **work-intent pre-commit** hook, the **`fold-back-ledger`** module
  install, and the **security gates** (`test_security_lint`,
  `test_hardening`, `test_content_scan`, `test_generated_output_scan`). A
  shipped surface with no test is a finding.
* **Determinism**: a repeated run + a randomized-order / cache-disabled run
  agree — no order-dependence or hidden state behind the green bar.

**Disposition**: a missing test for a new adopter-facing surface is a
should-fix-for-cut; an undocumented skip is at least a *document-why*.

**Timing / dependencies**: independent; **run last** so it covers everything
that landed (it is the backstop that the other sweeps' fixes did not
regress the suite).

#### Findings — 2026-05-27 run

**Near-PASS — the suite is healthy.** `bootstrap/tests/` **281 passed /
2 skipped**; both skips are `bandit not installed` with a documented reason
**and the gate fails (not skips) in CI** — justified, not a silent hole.
New-surface coverage is strong: `test_upgrade.py` (28 tests), the
work-intent pre-commit hook (`test_intents_tool.py` → `TestPrecommitCheck`:
unclaimed/claimed/**other-session-even-with-own-claim**/**solo-suppresses-self-not-other**/unknown-identity-failsoft/identity-agrees-with-autorelease),
`test_fold_back_ledger_module.py`, `test_coordination_broad_intent.py`, and
the security gates (`test_security_lint`/`test_hardening`/`test_content_scan`/`test_generated_output_scan`/`test_verify_integrity`).
Three minor findings:
* **[D-1] (minor / verify) — path-scoped-commit discovery regression.** The
  pre-commit hook's core behaviors are well-covered, but the source
  contract's explicit *path-scoped-commit* regression (that `git diff
  --cached --name-only` during `git commit <path>` sees only the committed
  path, not unrelated staged files) is not obviously ported. Verify; add if
  absent. Low.
* **[D-2] (minor) — the plan-review-gate `Plan review:` template line is
  unpinned.** No test asserts the mandatory `Plan review: required/not`
  line is present in the installed proposal/plan templates, so a silent
  template regression would pass. A one-line install-assert would pin it.
* **[D-3] (should-fix-low) — order-independence is unverified.**
  `pytest-randomly` is not installed, so determinism is only spot-checked
  by repeated runs (two `281 / 2` runs agree); order-dependence could hide
  behind the green bar. Add `pytest-randomly` (or a randomized-order CI
  lane) so it can't.

Disposition: **D is a near-PASS**; D-1/D-2 minor, D-3 the one
should-fix-low (a method gap, not a defect).

#### Lessons learned — 2026-05-27 (carry forward)
* **L6 — map surfaces to test *functions/classes*, not file names.** The
  initial file-name surface-map flagged "pre-commit hook → no test file," a
  **false gap**: the hook is thoroughly tested *inside* `test_intents_tool.py`.
  A folded-back capability's tests often live in an existing file — grep
  test *functions*, not filenames. (Third verify-before-flag near-miss in
  three sweeps — see the meta-note below.)
* **L7 — read skip *reasons* (`pytest -rs`).** "2 skipped" looked like a
  coverage hole until `-rs` showed both are bandit-absent-locally +
  fail-closed-in-CI. Never accept a bare skip count.
* **Meta (across A/C/D) — the sweep keeps generating false-positive
  findings that verification catches** (base-cache noise in A; the
  `new-base/` "clobber" in C; the pre-commit "gap" in D). This is the
  framework *working*: a sweep surfaces candidates fast and the
  verify-before-asserting step filters them — so **never record a finding
  from the first cheap signal; confirm it.** Worth promoting to §4.

### Sweep E — Vendor / project neutrality

**Owner**: tbd (could fold into A). **Scope**: the shipped surfaces —
`templates/`, `doctrine/`, `dimensions/`, `bootstrap/` (excluding
`case-studies/` and deliberation attribution, which legitimately name
agents). **Lens**: do the shipped templates/doctrine leak any **vendor**
(Claude / Codex / a tool name) or **project** (modflow_tools) name?

**Checks**:
* **Vendor-name lint**: grep the shipped surfaces for tool/vendor tokens
  (`Claude`, `Codex`, `Anthropic`, `OpenAI`, `Gemini`, `GPT`, `Antigravity`,
  `Cursor`, …) — the R-G discipline in `BOOTSTRAP.md` Act II-5. Every hit
  must fall in one of the **three sanctioned exceptions**: (a)
  deliberation-artifact attribution (a Review/Decision naming its reviewer),
  (b) a filename citation, (c) the vendor-addendum reference (the thin
  `@AGENTS.md` wrapper). Any other hit is a finding.
* **Project-name lint**: grep for `modflow_tools` (path or vocabulary) in
  any shipped template/doctrine/`dimensions` file — Cairn's reference
  deployment must not leak into the generalized core. Case studies
  (`case-studies/*.md`) legitimately name it and are excluded.
* **Scope**: `templates/`, `doctrine/`, `dimensions/`, `bootstrap/` —
  *excluding* `case-studies/` and the `dev/`-style deliberation surfaces.

*Failure mode this guards*: a fold-back authored from the modflow_tools
instance carries a project path or a tool name into core, where it becomes
a confusing or non-portable instruction for a different adopter.

**Disposition**: a leaked name in a shipped surface is a should-fix-for-cut
(cheap to fix, high embarrassment downstream). **Overlap note**: this is A's
layer-2 neutrality check run as a *dedicated whole-tree lint*; keep E
separate only if a distinct owner runs it, else fold the grep into A.

**Timing / dependencies**: independent; cheap and mechanical (a grep), so
can run anytime.

#### Findings — 2026-05-27 run

**Prose vendor-neutrality is clean.** Every vendor-name hit in
`templates/`/`doctrine/`/`dimensions/`/`bootstrap/*.md` is a **sanctioned
exception** — the vendor-addendum filename examples (`CLAUDE.md`,
`GEMINI.md`, copilot-instructions in `VENDOR.md`/`AGENTS.md`/`SAFETY.md`/
`BOOTSTRAP.md`) or the lint/exception *definition* itself. No accidental
vendor leak in prose. Findings (all project-name, one nit):

* **[E-1] (should-fix / maintainer call) — pervasive `modflow_tools`
  provenance references in shipped scripts + a module.** A consistent,
  *deliberate* pattern — "**generalized from modflow_tools' `X`**" /
  "**modflow_tools-hosted `<plan>`**" — across `claim_check.py`,
  `lifecycle_metrics.py`, `check_cairn.py`, `scaffold.py`, and
  `cairn/templates/modules/default-on/lifecycle-metrics.md` ("The modflow_tools
  implementation it was generalized from…"). This is origin-attribution,
  **not** a sloppy leak — but it names the reference project in
  adopter-installed surfaces, which Cairn's own R-G stance
  (`fidelity-check.md`: "project-name leak … the same shape of structural
  violation") says to avoid. The neutral form is "generalized from **the
  reference implementation**". **Maintainer call**: accept as provenance
  attribution, or neutralize across the ~half-dozen sites. (A *class*, per
  the L2 lesson — not one instance.)
* **[E-2] (low / self-acknowledged) — `fidelity-check.md` names
  `modflow_tools` as the reference case study** (lines 5, 308). The doc
  itself acknowledges the tension (line 311: "project-name leak … a
  fidelity manifest is a *case-study artifact*"), and these are pointers to
  the case-study manifest. Acceptable as-is; lowest priority.
* **[E-3] (nit / defer — = A-3 generalized) — vendor-agent dev-history
  attribution in shipped `.py` comments.** `scaffold.py` especially is
  dense with `Codex C#` / `Antigravity A#` / `code-review P2` review-finding
  citations baked into comments; also `claim_check.py` / `lifecycle_metrics.py`.
  Cosmetic neutrality only. The functional harness-session-ID registry
  (`CLAUDE_CODE_SESSION_ID`, `CODEX_THREAD_ID`, `ANTIGRAVITY_TRAJECTORY_ID`)
  and the `CLAUDE.md` filename examples are **functional/sanctioned and
  stay**.
* **[E-4] (should-fix-low) — the R-G neutrality lint is manual.** There is
  no automated neutrality gate (only the `BOOTSTRAP.md` Act II-5 grep
  recipe); a leak can regress silently between cuts. Mechanize it as a
  `cairn/scripts/` linter / test (sibling of `check_cairn.py`, with the
  three sanctioned-exception allowances) — also the natural home for Sweep
  G's overlap-detector. Pairs with D-3 (both are "add a gate so it can't
  regress").

Disposition: **prose is a PASS**; E-1 is the headline (maintainer call,
accept-vs-neutralize a deliberate provenance class), E-4 the actionable
method gap, E-2/E-3 low/nit.

**Decision — Maintainer, 2026-05-27**: *"we shouldn't have provenance
statements in the code like that."* So **E-1 and E-3 are accepted-to-fix**
(not a judgment call after all): the batch **neutralizes** the
`modflow_tools` "generalized from … / modflow_tools-hosted …" provenance
across the shipped scripts + the `lifecycle-metrics.md` module (to "the
reference implementation" or simply dropped), **and removes** the
vendor-agent dev-history attribution (`Codex C#` / `Antigravity A#` /
`code-review P2`) from the shipped `.py` comments. The functional
harness-session-ID registry and the `CLAUDE.md` filename examples stay
(they are not provenance statements). **E-2** (the `fidelity-check.md`
case-study pointer — a *doc*, not code) and **E-4** (mechanize the lint)
are unaffected by this Decision.

#### Lessons learned — 2026-05-27 (carry forward)
* **L8 — distinguish an accidental *leak* from deliberate *provenance*;
  surface, don't auto-flag.** The `modflow_tools` references are intentional
  origin-attribution, so E-1 is a *maintainer judgment* (accept vs.
  neutralize), not a clear defect. A neutrality sweep should separate
  clear-fix leaks from judgment-call provenance and surface the latter
  (mirrors Cairn's surface-don't-scrub doctrine).

### Sweep F — Release-mechanics & provenance readiness

**Owner**: tbd / maintainer-adjacent (could fold into C). **Scope**: the
cut artifacts. **Lens**: can the cut itself proceed cleanly?

**Checks** (the cut readiness checklist):
* **Version files ready**: `CITATION.cff` has the fields to bump (`version`,
  `date-released`) and any `doi:` placeholder is in a known state; no other
  authoritative version string exists that the cut must also bump.
* **No stale version strings**: grep the tree for the *outgoing* version
  (`[v0.2.0]`: `0.1.1`) so nothing references the old release post-cut.
* **CHANGELOG rename is clean**: `## Unreleased` → `## <version> — <date>`
  with a fresh empty `Unreleased` above; entries coherent, grouped under
  `Added/Changed/Fixed`, each cross-linked (overlaps A's CHANGELOG coherence
  check — F owns the *rename mechanics*, A owns the *prose coherence*).
* **Provenance controls satisfiable** (`PROVENANCE.md` Layer 1): the release
  is a **signed tag or a maintainer-approved release commit** on the
  protected branch, and the published `--manifest` matches the tagged tree —
  so an adopter can verify what they install.

**`[v0.2.0]` instance**: **tag-only** — Zenodo / DOI minting is **not
wired**, so the cut is `CITATION.cff` bump + CHANGELOG rename + an annotated
tag + push; any "Zenodo mints the DOI" language in older notes is
aspirational, not the current procedure (see §5).

**Disposition**: anything here is a **blocker for the cut** by definition —
F *is* the cut's pre-flight checklist.

**Timing / dependencies**: **last** — it gates the cut itself, and it should
run after A–E so the tree it certifies is the one that ships.

#### Findings — 2026-05-27 run

**PASS — release mechanics are ready.**
* **`CITATION.cff`**: `version: "0.1.1"` + `date-released: "2026-05-21"` are
  present and ready to bump; the `doi:` is a commented placeholder with the
  tag-only stance ("cite by version + repository URL until issued") — fully
  consistent with the `[v0.2.0]` no-Zenodo cut.
* **No stale version strings**: `0.1.1` appears **only** in `CITATION.cff`
  (the field the cut bumps) — the version is single-sourced across the
  tree, so the bump can't leave a dangling old reference.
* **CHANGELOG**: the `## Unreleased` section holds 13 coherent, cross-linked
  top-level entries (links resolve — `check_cairn` clean in Sweep A) and is
  cleanly renamable to `## 0.2.0 — <date>` with a fresh empty `Unreleased`
  above.

One nit:
* **[F-1] (nit) — all 13 CHANGELOG entries sit under `### Added`,** but
  several are **Changes** to existing surfaces ("Module upgrade — installs
  are *no longer* one-directional"; "doc-drift-prevention *flips* from
  doctrine-only to doctrine + tooling"). A Keep-a-Changelog `### Changed`
  split would read more accurately. Cosmetic; the maintainer can split at
  the rename or accept.

**Cut pre-flight (maintainer actions at tag time)**: bump `CITATION.cff`
(version + date) → rename CHANGELOG `Unreleased` → `0.2.0 — <date>` (+
fresh empty `Unreleased`) → **signed / maintainer-approved annotated tag**
(PROVENANCE.md Layer 1) + push → **tag-only** (no DOI). The published
`--manifest` matches the tree (confirmed in Sweep C).

#### Lessons learned — 2026-05-27 (carry forward)
* **L9 — a tree-wide outgoing-version grep is a cheap, decisive currency
  check.** `0.1.1` appearing only in `CITATION.cff` proved the version is
  single-sourced in one command — the highest-confidence-per-effort check
  in the whole sweep. Make it the first F step every cut.

### Sweep G — Redundancy / consolidation

**Owner**: Claude (Strategy). **Scope**: the whole Cairn tree —
`cairn/doctrine/`, `cairn/templates/{core,modules}/`, the module `.py`
tooling, `cairn/dimensions/`, `cairn/bootstrap/`, supporting docs.
**Output**: findings report first (survey → prioritized list → triage →
fixes). **Status**: **design-only** for now (per maintainer 2026-05-27) — the
lens is specified here; the run happens on a clean **post-fold-back** snapshot.

**Lens**: is there **duplicate or unnecessary functionality** anywhere in the
tree — and crucially on the axes Sweep A's doc-coherence pass does not reach:
**code** (dead / unreachable paths) and **capabilities** (a module or doctrine
no adopter profile would invoke)? A's layer-2 catches doc one-canonical-home
*for the cut*; G owns the systematic, **reusable** consolidation technique
plus the code + capability axes.

**Why a standing lens, not just a cut-time pass**: Cairn's fold-back process
is *monotonic accretion* — proven doctrine flows in and is appended; nothing
in the lifecycle pushes back toward consolidation. Duplication, stale
doctrine, overlapping modules, and dead code therefore grow by construction.
G is the counter-pressure, **designed to harden into a reusable Cairn lens** (a
`cairn/doctrine/`-level consolidation / architecture-review doc Cairn lacks),
cadenced to release cuts + post-fold-back bursts — not a one-off.

**The layer contract** (so legitimate layering is not mistaken for dup): L1
`cairn/doctrine/` = the principle; L2 `cairn/templates/core/` = *installable*
governing docs that **legitimately restate** condensed doctrine to stay
self-contained (an adopter gets no `cairn/doctrine/`); L3
`cairn/templates/modules/` = optional capabilities, each owning a distinct
operational surface; L4 the module `.py` tooling; L5 supporting docs. The
load-bearing exception: L1→L2 condensed instantiation is *not* drift — flag
only same-layer duplication or cross-layer copies where a thin pointer would
do.

**The seven redundancy categories** (each its own detector + disposition): R1
verbatim / near-verbatim prose · R2 semantic restatement · R3 layer-violation
dup · R4 superseded / stale doctrine · R5 capability / surface overlap (e.g.
the `cairn/templates/modules/default-on/claim-check.md` deferred pre-commit
hook vs. the coordination-tiers work-intent pre-commit check — the P2#3
collision flagged in the process-hardening review) · R6 dead / unreachable
code · R7 unnecessary / over-engineered capability. R1–R3 overlap Sweep A's
coherence layer (shared finding-home by agreement: A catches them in-pass for
the cut; G supplies the systematic technique); **R4–R7 are G's exclusive
territory**.

**Checks** (cheapest / objective first):
* **Mechanical**: a shingle / n-gram overlap detector across the doc corpus (a
  candidate `cairn/scripts/` linter, sibling of `cairn/scripts/check_cairn.py`)
  emitting high-overlap passage pairs (R1); dead-code static analysis
  (vulture / coverage / unreferenced-def grep) over the L4 tooling (R6).
* **The rule→home index** (core technique): map every methodology rule → its
  file(s); a rule in >1 home that is *not* a canonical-home / thin-pointer
  pair (and not the L1→L2 exception) is an R1/R2/R3 finding. Generalizes
  `cairn/doctrine/doc-governance.md`'s "one canonical home" from the two-file
  adopter case to the whole tree.
* **The surface-ownership map** (R5): one row per operational surface → the
  module(s) touching it; >1 owner is an overlap finding.
* **The capability-necessity test** (R7), evaluated **per-dimension** against
  the `cairn/dimensions/` axes (size, age, complexity, language, agent-team,
  human-team), **never absolutely** — optionality is Cairn's value, so
  "unnecessary for profile X" ≠ "unnecessary": for each capability name the
  adopter profile that invokes it, the trigger, and what breaks on removal;
  "nothing, for any profile" + no portability story = R7.
* **Stale-doctrine scan** (R4): `cairn/CHANGELOG.md` + `cairn/doctrine/fold-back.md`
  history + a contradiction pass for a rule a newer fold-back superseded but
  left in place.

**Disposition rubric**: canonicalize (one home + thin pointers) / merge /
delete / keep + document-why; **bias to surface** when unsure between dup and
legitimate layering, or between unnecessary and per-dimension-necessary
(mirrors Cairn's scrub doctrine — surface, don't scrub silently).

**Timing / dependencies**: design-only now; **run on a clean post-fold-back
snapshot** (not mid-flight) so the just-accepted process-hardening A→B→C
surfaces are swept in final form. Overlaps Sweep A on R1–R3 (coordinate
finding-homes); independent otherwise. The full design notes live at
`.claude/notes/2026-05-27-cairn-redundancy-sweep-lens-design.md` (Claude
harness scratch, untracked).

**Findings — 2026-05-27 first pass** (the fold-back work being done met the
post-fold-back-snapshot precondition; run by Claude on the maintainer's
go-ahead):

**First-pass manual scan: clean — no confirmed redundancy in the
high-churn surfaces.** The obvious candidates today all resolve to
*legitimate* structure, filtered by the §4 verify-before-recording
principle + G's own **layer contract**:
* **R1/R3 (not dup)** — the **asymmetric-reward principle** and the **broad
  work-intent requirement** each appear in both `doctrine/coordination.md`
  (L1) and `coordination-tiers.md` / `intent.py` (L3). This is the
  **L1→L3 condensed instantiation the layer contract explicitly exempts**
  (an adopter installs no `doctrine/`), *not* duplication — confirmed it is
  restated/condensed, not verbatim-copied.
* **R5 (not overlap)** — the two `pre-commit` surfaces (claim-check's
  *deferred Markdown content-gate* hook vs. the *work-intent* pre-commit
  check) are the **resolved P2#3** distinction (claim-check.md carries the
  "not to be confused with" note), not an unresolved capability overlap.
* **R4 (not stale)** — claim-check's "deferred from v1" hook is a
  *different* hook (the Markdown gate) and genuinely still deferred; the
  work-intent hook shipping does not supersede it.

**Residual — the deep mechanical sweep needs the detector that doesn't
exist yet.** The systematic R1 (shingle/n-gram overlap), R6 (dead/unreachable
code), and exhaustive R7 (per-dimension capability necessity) checks require
the **candidate `cairn/scripts/` overlap+dead-code linter** G's design names
— which is **the same tool E-4 calls for** (mechanize the neutrality lint).
That linter is G's standing-mechanism deliverable; until it exists, G is
"clean by manual inspection for this cut, tool-gated for the standing run."
**Disposition: G first-pass PASS for the v0.2 cut**; build the G/E-4 linter
as the post-cut consolidation deliverable (a Cairn proposal of its own — the
`cairn/doctrine/`-level consolidation/architecture-review surface G was
designed to become).

**Lessons learned — 2026-05-27 (carry forward)**
* **L10 — the layer contract is the false-positive filter for a redundancy
  sweep.** Every L1-doctrine rule that an L3 module restates for
  self-containment *looks* like R1 dup and isn't; without the layer
  contract, G would mis-flag every condensed instantiation. The contract is
  load-bearing — keep it the first gate of any G run. (Same shape as the
  A/C/D/E verify-before-record near-misses: the cheap signal over-reports.)
* **L11 — three sweeps (D-3, E-4, G) converge on one missing tool.** A
  randomized-order test lane, a neutrality lint, and a redundancy/dead-code
  detector are all "a `cairn/scripts/` gate that doesn't exist yet." That
  convergence is the signal: the highest-leverage post-cut work is **one
  consolidated `cairn/scripts/` quality-gate suite**, not three separate
  asks.

## 4. Shared method (all sweeps)

* **Findings report first.** Survey → a prioritized, written findings list
  → maintainer triages in-scope-for-cut vs. deferred → fixes. No edits
  before the report unless trivially mechanical.
* **Fix routing by size.** Mechanical/obvious → direct commit (Cairn-side,
  per PR-flow). Substantive → the proposal/plan lifecycle. Deferred → a
  durable home (the fold-back ledger, a follow-up, or a `Future work` note).
* **One shared findings surface.** Each sweep reports under its own §; the
  maintainer reads the union. A sweep that finds nothing records an explicit
  "clean as of `<date>`" — an empty sweep is a successful sweep, not a
  skipped one.
* **Coordinate on the contended files.** Cairn is multi-agent right now;
  claim before editing, read the active set, path-scoped commits.
* **Verify before recording a finding.** A sweep surfaces candidate
  findings cheaply, and a large fraction are **false positives** that one
  more check dissolves — observed every sweep so far (the base-cache
  `{{token}}` noise in A; the `new-base/` "clobber" in C; the "pre-commit
  hook untested" file-name gap in D). Treat the first cheap signal as a
  *candidate*, confirm it (read the real file, the merged dir, the test
  *functions*), and only then record it. This is the verify-before-asserting
  discipline applied to the sweep itself — it is what keeps the findings
  report trustworthy rather than noisy.

## 5. The cut (what the sweep gates)

When the sweeps are green or their findings triaged, the maintainer cuts the
release. The cut is **maintainer-performed** and mechanical:

* `cairn/CITATION.cff` — bump `version` + `date-released`.
* `cairn/CHANGELOG.md` — rename `## Unreleased` to `## <version> — <date>`,
  start a fresh empty `Unreleased` above.
* An **annotated tag** — signed, or on a maintainer-approved release commit
  on the protected branch (`PROVENANCE.md` Layer 1) — + push.
* DOI / archival minting **when wired**.

**`[v0.2.0]` instance**: **tag-only** — Zenodo / DOI minting is **not wired**,
so this cut omits the DOI step; any "Zenodo mints the DOI" language in older
notes is aspirational, not the current procedure.

The sweep does not perform the cut; it produces the confidence (or the
triaged findings list) the cut rests on. **Gate condition**: every sweep in
the roster is either green or its findings triaged (in-scope-for-cut items
fixed; deferrals homed) — Sweep F's checklist is the final pre-flight.

---

## 6. Fix batch — 2026-05-27

The cut-focused fixes from the A–F findings, landed Cairn-side (mechanical
→ direct commit, per §4). All gated on `check_cairn` + affected tests.

**Fixed (in scope for the cut):**
* **A-1** — Cairn `AGENTS.md` template states the canonical convention: a
  `doctrine/<name>.md` reference is a citation to Cairn's *published*
  doctrine, not an adopter-local file (one statement, not per-site
  qualification). *(Cairn `8c5b8a2`, +fix `0f8a36a`.)*
* **A-2** — `cairn/templates/modules/README.md` catalog gains the default-on
  `fold-back-ledger` row. *(`8c5b8a2`.)*
* **E-1 + E-3** (maintainer Decision — no provenance/attribution in shipped
  code) — neutralized the `modflow_tools` provenance pattern and removed the
  vendor-agent dev-history review citations across `scaffold.py`,
  `check_cairn.py`, `claim_check.py`, `lifecycle_metrics.py`,
  `lifecycle-metrics.md`; kept the functional harness-session-ID registry +
  `CLAUDE.md` filename examples; restored two rationale fragments a perl
  over-removal had stripped (caught by diff inspection). *(Cairn `95c338e`.)*
* **C-2** — `UPGRADE.md` now orients the reviewer to the staging layout
  (`files/` = merged result; `new-base/` = next base-cache; metadata).
  *(`95c338e`.)*

**Deferred to follow-ups (not cut-blocking; each its own small task):**
* **D-3** — add `pytest-randomly` (or a randomized-order CI lane) so
  order-dependence can't hide.
* **E-4** — mechanize the R-G neutrality lint as a `cairn/scripts/` gate
  (pairs with D-3; also Sweep G's overlap-detector home).
* **Nits** — A-3 (dev-attribution — *subsumed by the E-3 fix where it
  overlapped*), C-1 (plan "clean" lumps locally-modified), D-1 (path-scoped
  regression test), D-2 (pin the `Plan review:` template line), F-1
  (CHANGELOG `Added` vs `Changed` split).

**Method lesson reaffirmed**: the perl over-removal on `scaffold.py`
(stripping a citation *and* the rationale wrapped in the same parenthetical)
was caught only by reading the staged diff — the §4 "verify before
recording / before committing" principle applies to *fixes* too, not just
findings.

---

## Sweep-type section template (for contributors)

Copy this block to add a sweep; fill the roster row in §2.

```
## Sweep <letter> — <name>

**Owner**: <agent / role>. **Scope**: <Cairn tree / subset>. **Output**:
findings report first (survey → prioritized list → triage → fixes).

**Lens**: <the one distinct question this sweep owns — what it checks that
the other sweeps do not>.

**Checks** (cheapest/objective first):
* <gate or read>
* <gate or read>

**Timing / dependencies**: <e.g. run after X lands; independent of Y>.

**Findings**: <filled in when the survey runs — prioritized
blocker / should-fix-for-cut / defer; or "clean as of <date>">.
```
