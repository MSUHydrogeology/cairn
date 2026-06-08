<!-- claim-check-allow: scripts/onboarding_activate.py -->
<!-- The adopter-install path is cited verbatim in the
     progressive-onboarding entry; from Cairn's own checkout the path
     does not resolve (the source-of-truth lives at
     templates/modules/default-on/onboarding_activate.py).  Same
     pattern as the fold-back-active-surfacing entry's claim-check
     exemptions. -->
<!-- claim-check-allow: docs/developer/vision.md, docs/developer/style.md, docs/style.md -->
<!-- The doc-governance Chunk 2 + Chunk 7 entries quote example
     paths for vision + style conventions an adopter MIGHT use; these
     are the doctrine's enumeration of "common homes" without
     prescribing one.  None resolve in Cairn's own tree because
     Cairn itself doesn't host these documents at those locations --
     they're adopter examples per the M1 layer-prescriptiveness
     gradient (tier-RECOGNITION holds; tier-LEGISLATION drops). -->

# Changelog

Notable changes to Cairn.

Entry-shape: each entry is one line (sometimes 1-3 short
sentences for substantive doctrine landings), grouped by
category, with at least one cross-link to the durable substance
(an archived adopter proposal / plan / commit, or the Cairn-side
doctrine file). The methodology's bias is for the substance to
live in doctrine and case studies; the changelog curates and
points.

The `Unreleased` section accumulates pending entries; when a
release is cut, that section is renamed to the version + date
and a new empty `Unreleased` is started above.

## Unreleased

### Added

- **Gate-control tooling for unattended registry-cascade batches.**
  `bootstrap/tests/_ast_attest.py` gains a hardened `update-symbol` subcommand that
  surgically re-baselines exactly one allowlisted registry-mapping digest
  (`_MODULE_MAPPINGS` / `_SKILLS_MAPPINGS` / `_CORE_MAPPINGS`) — guarded by
  `--expect-old`, refuse-on-unrelated-drift, and a before/after attestation, so a
  one-key rebaseline cannot bless an unintended mutation. New
  `bootstrap/tests/_gate_manifest.py` freezes a pre-run gate-integrity manifest —
  byte hashes of every test / scanner / security-gate / oracle file (including the
  top-level `security_check.py` / `verify_integrity.py` gate modules), the pytest
  collection node-IDs plus skip/xfail identities, and the cascade-mutable set — with
  a verifier that HOLDs on any gate weakening and is externally anchored to an
  immutable git object. Built so a minimally-supervised multi-step batch is
  *risk-bounded by mechanism*, not instruction. Hardened after an external
  confirmation pass: `update-symbol` refuses a mapping change that smuggles a new
  top-level symbol — or an altered body, duplicate, or deletion of an allowed name
  (complete-set equality against a base set pinned by structural digest + multiplicity);
  the frozen set covers the shipped
  `templates/modules` scanner implementations; and the verifier takes an explicit
  `--target-repo` (trusted code, batch target) with a mandatory-anchor mode.

- **An adopter-facing security stack — folded up from a battle-tested
  reference implementation as a three-surface split.** `security-review`
  (doctrine) gains a generalized, tool-agnostic by-input-class injection-review
  procedure plus the v1 self-audit trust-model statement. `content-security`
  expands from "scanner only" to a complete, **standard-library-only**
  self-audit apparatus: `content_scan_runner.py` (an audited-roots manifest, a
  reviewed-residual multiset baseline, per-file symlink/special-file
  containment, resource budgets, and a `0/1/2/3` fail-closed exit contract with
  tripwire-not-proof output), plus the shipped roots manifest, residual
  baseline, and URL allowlist, and an RV5 narrow scientific-unit homoglyph
  allowance in `content_scan.py`. A new **`python-security`** module (team-gated,
  Python-only, opt-in) ships `run_security_audit.py` — a standalone orchestrator
  that runs an integrity preflight over its own apparatus, then composes the
  content-scan (when installed), bandit, an adopted-executable source gate, and
  pip-audit (network egress opt-in) under a distinct-space aggregate exit table.
  The scaffold gains a **selected-module required-token preflight** that fails an
  install/adopt/upgrade closed before any write when a selected module's
  required token (e.g. `python-security`'s `python_package`) is unfilled.
  `bootstrap/DEPENDENCY_BUDGET.md` records `bandit` + `pip-audit` as the first
  declared executable-dependency exception. The stack is a **self-audit gate on
  a trusted tree** — explicitly not a reviewer for untrusted PRs that can modify
  the apparatus; a clean result is a tripwire, not a proof.

### Changed

- **The 4865-line `scaffold.py` install/upgrade monolith is split into a thin
  fail-closed launcher + facade over a private `bootstrap/_scaffold/` engine
  package of eight owned modules** (`security`, `slotmerge`, `merge`, `config`,
  `lockfile`, `install`, `upgrade`, `cli`) plus the verifying loader `_guard.py`,
  arranged as an acyclic downward dependency DAG. Behavior-preserving, leaf-first,
  one gated commit per stage. The public surface is unchanged: the launcher
  `bootstrap/scaffold.py` reassigns `sys.modules[__name__]` to the engine, so
  `bootstrap.scaffold` **is** the engine object and `from bootstrap.scaffold
  import X` keeps working; the two release-trust anchors tighten their imports to
  the narrowest owner (`security_check` → `_scaffold.config._MODULE_MAPPINGS`,
  `verify_integrity` → `_scaffold.lockfile.read_lockfile`). Each extraction was
  gated by a four-part acceptance check committed alongside it — an AST
  source-motion attestation (every one of 164 baselined top-level symbols present
  exactly once, structurally unchanged, across the module set), the full bootstrap
  suite + `security_check` (Bandit recurses the new package) + `check_cairn`, a
  frozen-vs-current **differential oracle** (3 fresh installs + 3 privileged
  upgrade/refusal workflows, exact-byte equal modulo enumerated provenance), and a
  circular-import-clean check. One behavioral note for adopters who monkeypatch in
  tests: a symbol extracted into a submodule must be patched at its owning module
  (`bootstrap._scaffold.<m>`) for that module's internal callers to observe it —
  patching the `bootstrap.scaffold` facade re-export mutates only the engine
  namespace. Lands across `bootstrap/scaffold.py` + `bootstrap/_scaffold/*`;
  deliberation in the adopter plan `2026-06-05-claude-scaffold-split.md`.

- **The `claim_check` category-D count soft-flag is retired; numeric drift is now
  governed by a three-kind precision / `as_of` discipline.** The count soft-flag
  (a number adjacent to `lines`/`tests`/`commits`/…) and its
  `claim-check-allow-count` document directive are removed from `claim_check.py`:
  0 catches across the verify-before-asserting instance log, while the directive
  accreted multi-KB enumerated-count headers across the deliberation tree (the
  header bloat the nag itself generated). The checker keeps **all** hard checks
  (broken repo paths, out-of-bounds line citations) and the `claim-check-allow`
  *path* directive; the two-tuple `check_text` contract and `--fail-on-soft` are
  retained (the soft channel simply has no producer now), and a stray
  `claim-check-allow-count` comment in an archived doc is silently ignored.
  Doctrine replaces the nag: pick a count's **kind** — *approximate* a
  decision-irrelevant count, *date* a snapshot (`N, as_of YYYY-MM-DD`, never
  re-measured), *register* a live invariant (a code-side `verify_counts`
  registry, where the project ships one). Lands in the `claim-check` module
  (`claim_check.py`, `claim-check.md`), the core proposal + plan templates'
  "Count claims" sections + author tips, and `docs/tool-usage.md`. Adopter
  deliberation: modflow_tools `2026-06-05-claude-numeric-claim-verification`
  (Arm 1 + Arm 2).
- **All Cairn adoption state lives in `dev/.cairn/` (the fidelity manifest moves
  out of `dev/strategy/`).** The fidelity manifest is install bookkeeping — a
  record of *what is installed* — not a human-AI deliberation surface, so it
  joins the lockfile, base cache, profile, and fold-back ledger in `dev/.cairn/`;
  `dev/strategy/` stays for genuine project-strategy deliberation. Both scaffold
  `dev/strategy/` lookups (`_citation_ok`'s R10 citation check **and**
  `_cmd_init_lock`'s `cairn_commit` recovery) now search `dev/.cairn/` first with
  an indefinite legacy `dev/strategy/` fallback + migration advisory; the
  placement docs (`fidelity-check.md`, `UPGRADE.md`, `SAFETY.md`) move with it.
  Strategic *notes* (security-decision / profile-audit notes) stay in
  `dev/strategy/`. Drained from the LHM `cairn-adoption-state-home` proposal.
- **`init-lock` captures the full six-axis profile + the profile-representation
  model is documented.** `upgrade --init-lock` no longer synthesizes a
  gating-only stub: with no committed `dev/.cairn/profile.yml` it prefills the
  structurally-inferable axes (from installed modules / `CONTRIBUTING.md` /
  `legacy-agent.md`) and **fails with a template** the operator completes
  (validated against `_AXES`), then embeds the full profile + tokens in the
  lockfile. `upgrade` **self-heals** an already-`init-lock`'d adopter by
  materializing `dev/.cairn/profile.yml` from the lockfile (merging `tokens` +
  `profile`) when absent — composing with the #56 dirty-tree guard.
  `BOOTSTRAP.md` now documents the three-representation model (authoritative
  config → regenerated lockfile copy → human record) and the *edit-the-config →
  regenerate-the-lockfile* reconciliation. Drains fold-back #55 (the last
  candidate). Drained from the LHM `cairn-init-lock-full-profile` proposal.
- **Windowless-commit Tier-1 discipline (concurrent-session coordination, Layer
  1).** `doctrine/coordination.md` Tier 1 + the `templates/core/AGENTS.md`
  git-workflow checklist now make the **windowless commit** primary: for tracked
  files, `git commit <paths>` stages *and* commits atomically (no separate `git
  add`), and the staged set is **verified via the working tree** (`git status
  --short`, `git diff <paths>`) rather than the shared `git diff --cached` — which
  both manufactured the exposure window and read back other sessions' staged
  index. The structural path-scoped-commit rule is unchanged; the C1/C2/C3
  residual cases (failed-atomic-commit `restore`; rename via `git status
  --short`; untracked content via `git diff --no-index`) are baked in. Drained
  from the LHM `cairn-concurrent-session-coordination` plan (fold-back #53/#56;
  supersedes modflow_tools' concurrent-staging-discipline).
- **Intent enforce mode + own-claim matching (concurrent-session coordination,
  Layer 2; #53).** The `coordination-tiers` work-intent pre-commit check
  (`tools/intent.py`) gains a configurable `"enforce"` key in
  `dev/intent-config.json`: `warn` (default, surfaces only) / `confirm` (proceed
  on explicit acknowledgement; degrades to `block` with no controlling terminal)
  / `block` (refuse a commit touching a *different* active session's claimed
  path). The cry-wolf fix: the check recognizes the committer's **own** claims by
  the per-session token (`resolve_session_token()`) and warns only about
  genuinely different sessions — and, decisively, own-claim suppression is
  **gated on a resolvable token**, so two concurrent same-type sessions with no
  harness token never false-suppress each other (they stay on the warn path).
  `CAIRN_INTENT_ALLOW_UNCLAIMED=1` remains the per-commit bypass. Documented in
  `doctrine/coordination.md` > "Enforcing the coordination check".
- **Upgrade dirty-tree guard (concurrent-session coordination, Layer 3; #56).**
  `scaffold.py upgrade --apply` now **refuses** when its write-set would
  overwrite a **tracked** file the adopter has uncommitted edits in (a concurrent
  session's in-flight work), naming the colliding paths; `--force` overrides.
  Scoped to tracked paths, so benign untracked / gitignored dirt never trips it.
  `--apply` is the only refusing mode — `--stage` writes only the gitignored
  review surface, so it **completes** but emits an advisory when the staged set
  overlaps an uncommitted tracked path. Drained from the LHM
  `cairn-concurrent-session-coordination` plan (fold-back #53/#56).

### Added

- **Profile-sized `AGENTS.md` assembly via `cairn:if` conditional regions.**
  A new `<!-- cairn:if AXIS in val1,val2 -->` … `<!-- cairn:endif -->` directive
  (single-axis, comma-separated set-membership, no nesting) lets a template
  section be included only for profiles whose dimension axis matches. Semantics:
  keep-on-match; remove-otherwise; **keep-on-missing-axis** (safe default for the
  always-on file — the opposite of `select_optional_templates`); raise-on-unbalanced.
  **The never-gate-a-bright-line rule**: a `cairn:if` region may wrap only
  profile-optional content — no IR1–IR13 safety rule may ever be gated (the
  test suite asserts this). Currently the only gated section in the core
  `AGENTS.md` template is `## Human contributors` (`human_team in
  small-multi,large-multi`). The strip runs consistently at every
  template-materialization point — install, lockfile expected hash, and the
  3-way merge ancestor + `theirs` sides — so installed == cached == merged for a
  given profile; the base cache stays raw so a later profile change can
  re-include a stripped section. `verify_integrity` is unchanged (it compares
  on-disk against the now-stripped lockfile hash, so the check stays clean).
  Implementation: `bootstrap/_scaffold/config.py` (`strip_conditional_regions`);
  threading into install/lockfile/upgrade in `_scaffold/install.py` and
  `_scaffold/upgrade.py`. `doctrine/doc-governance.md` carries the right-size
  rule and the never-gate constraint. Source: LHM
  `dev/plans/cairn-profile-sized-assembly.md` (P1–P5).

- **`scripts/verify_counts.py` + `scripts/measurements.py` — the live-invariant
  leg of the three-kind numeric-claim discipline (Cairn-maintainer-only).** When
  `claim_check` retired its category-D count soft-flag, *decision-irrelevant* and
  *snapshot* counts moved to doctrine (approximate; date) — but a count cited as
  present fact and prone to drift is now **registered** in a code-side registry
  (`measurements.py`: `Invariant(root, fn, target)` / `Snapshot(value, as_of)`,
  `fn` from a closed allowlist `count_lines`/`count_files`/`count_defs`/
  `git_commits_in_range`) and **re-measured** by `verify_counts.py`. A doc
  annotates the number with `<!-- verify: <key> -->` immediately after it (RR1
  same-line window); an `Invariant` re-measures and flags drift, a `Snapshot` is
  never re-measured (value + ISO `as_of` only). **Security by construction**: the
  annotation carries only a registry key (no path, no command); every path
  measurement is root-contained (`resolve()` + `is_relative_to`, refusing a
  symlink/glob escape — IR3); `git` runs `shell=False` with a validated rev-range.
  An absent sibling root → a **visible** `SKIPPED` (RR2, distinct exit), never
  silent; an unregistered key is refused. No cache; ≤~10-key soft-cap registry
  (RR3 curation-tax kill-switch). **Not** in `_CORE_MAPPINGS` — never installed
  into adopters; it dogfoods on Cairn's own docs (seed invariant: the `claim_check`
  watch-file size). New `bootstrap/tests/test_verify_counts.py` (29 tests, incl.
  symlink-escape red-team). Adopter deliberation: modflow_tools
  `2026-06-05-claude-numeric-claim-verification` (Arm 3). **Wired into
  `check_cairn`** (a `_check_counts` lens): the self-check now re-measures every
  registered invariant on Cairn's docs, so a drifted annotated count or an
  unregistered key fails the gate (a visible absent-root skip never blocks a
  partial checkout). `check_cairn` is itself Cairn-only, so the verifier stays
  out of every adopter tree. New `bootstrap/tests/test_check_cairn_counts.py`.
- **Loop-fidelity gate (#58) — fail-closed dangling-reference check in
  `check_cairn`.** A new lens scans **only adopter-facing `templates/` surfaces**
  for references to Cairn-internal-only paths (`doctrine/*`) that would dangle
  once installed in an adopter (they resolve in the Cairn source, so `link_check`
  passes them, but break on adoption — the failure behind fold-back #57 and the
  un-shipped 9-lens review roster). Scans both backticked tokens and raw Markdown
  link targets; a deliberate citation is exempted with a path-specific
  `cairn-internal-ref-allow:` / `cairn-internal-ref:` marker (a *new* unlisted
  ref still fails closed). Companion content fix (#58a): the **9-lens review
  sweep roster is transplanted into the `dual-review` module body** so adopters
  carry the standard they're asked to run. The flagship of the loop-fidelity
  verification arc (fold-back #52/#54/#58); drained from the LHM
  `cairn-loop-fidelity-verification` plan.
- **Project-owned session-routine customization — the `custom_session_routines.md`
  convention.** The two lifecycle skills (`session-start` / `session-end`) now
  carry a **generic pointer** to a project-owned `dev/rules/custom_session_routines.md`
  (a single file with `## Session start` / `## Goodnight` headed sections,
  Cairn-never-templated like `RULES.md`); `doctrine/session-routines.md` documents
  the convention (no-bare-pointer, absent-file/section = no-op, the two-file
  fallback). This gives an adopter a real, installable home for its concrete
  routine steps so it can **slim its always-loaded `AGENTS.md` routine section to a
  pointer** (token-efficiency: procedures load on-demand), and replaces a
  reference that dangled in every adopter (the un-installed Cairn-internal
  `doctrine/session-routines.md`). A `test_skill_contract` assertion pins the
  pointer string. Drained from the LHM `cairn-session-routine-custom-home` plan
  (fold-back #57).
- **`dev/measurement/` — a standard self-instrumentation folder.** A new core
  scaffold dir (`templates/core/dev/measurement/`, carried by a `README.md` and
  registered in `_CORE_MAPPINGS`) gives every adoption a predictable home for the
  records it keeps to **measure its own process health** — aggregate lifecycle
  metrics + the operational ledgers that feed them (the collision log, the
  handoff-hazard log, the forthcoming signature log). The README states a
  two-sided **membership rule** (not an archive → `dev/**/archive/`; not
  framework-adopter state → `dev/.cairn/`) with concrete excluded examples (the
  work-intent log = active coordination state; `dev/reflections/` = ephemeral),
  and reserves a **structured metrics-store slot** + a `snapshots/` subdir (the
  store's name/format owned by the metrics tooling). The `lifecycle-metrics` and
  `incident-trackers` default-on modules now point at `dev/measurement/` as the
  home for the metrics store and live incident trackers.
- **Reviewer doctrine: the structured review sweep + recommend-and-decide.**
  `doctrine/dual-review.md` grows the clean-pass-trap standing checks into a
  generic, change-agnostic **9-lens review sweep** every reviewer works through
  and reports coverage on (probe forward/artifact claims like present-tense
  ones; the two true gaps — cross-document consistency and lifecycle/process
  placement — are named lenses), with falsifiable coverage, staged satisfiers,
  and a floor-not-ceiling / never-downgrade-a-required-tier rule. Each
  first-pass review closes with a **two-part coverage line** (Covered +
  Not-covered/low-confidence) and an explicit **second-round recommendation** —
  a second structurally-independent pass is a Maintainer decision, never an
  automatic default (composing with Decision-support Round-2). The core
  proposal/plan templates gain a **triage-gated author-accounting** block
  (invariants / failure modes / edge-case inventory / public-path→test mapping
  via relative links / known-omissions), reviewed as evidence not as a filled
  form. `claim-check.md` sharpens forward/future-tense claim probing;
  `lifecycle-metrics.md`'s Measurement Compact adds the **late-blocker
  reduction** bundle (homed in `dev/measurement/`). A standing sweep-going-ritual
  falsifier guards against hollow coverage.
- **`link_check.py`: skip `file://` targets + exclude vendored/tool-owned
  sources by default.** Three behavior changes folded up from the modflow_tools
  retire-`verify_doc_links` arc so every adopter's whole-tree doc-link gate is
  adoption-clean: (1) `file://`-scheme link targets are **skipped** (machine-
  specific reviewer links, not portably checkable — symmetric to the `http(s)`
  skip), so a reviewed proposal carrying `[text](file:///…)` links no longer
  reds the gate; (2) `dev/modules/` (vendored module docs whose links target the
  Cairn-install layout) and (3) `dev/.cairn/` (tool-owned machinery + the
  `base/` upgrade-ancestor template cache) are **excluded** by default — both
  **root-anchored** (first two path segments) so a `modules/` dir nested
  elsewhere is never over-excluded — with `--include-modules` / `--include-cairn`
  opt-ins. New `bootstrap/tests/test_link_check_exclusions.py`. Source:
  modflow_tools `dev/plans/archive/2026-06-04-claude-retire-verify-doc-links.md`
  (Part A) + the ER1/P2 plan-review.

- **Token-efficiency Phase 1 — measure + cap (A1) + the core-template router cut
  (A2.1).** `scripts/token_budget.py` measures the **always-on load manifest**
  (the files a harness auto-loads every turn — not invoked-on-demand skills),
  token-denominated via a real tokenizer when present (`tiktoken`) else a
  *labelled* `chars/4` proxy, with a soft cap (warn-not-block; `--strict` to
  gate). `doctrine/doc-governance.md` gains the **cache-stable load-order**
  convention (stable doctrine first, volatile boards out of the auto-loaded
  prefix; scoped to the adopter-controlled surface). The core
  `templates/core/AGENTS.md` Git-workflow section is **router-cut** — the verbose
  deliberation-commit-exception enumeration + untracked-artifact prose compressed
  to bright-line + pointer, every safety-critical rule kept operative-inline
  (template 363→281 lines, ~22% lighter). Source: LHM
  `dev/proposals/archive/2026-06-03-claude-cairn-doctrine-token-efficiency.md`
  + the `cairn-efficiency-rollout` plan (A1/A2.1).

- **Model-tier fan-out doctrine (model-selection module + roles).** The
  `model-selection` module gains an *Orchestrated work — the fan-out* section
  extending the role→tier table into a **task→tier** discipline: a fan-out leaf
  takes its floor from its own task (never inheriting the orchestrator's frontier
  tier — the largest model-cost multiplier), verification tiers by **claim-stakes**
  not post-hoc "decisiveness," an independent reviewer may lower a *generative*
  step's floor only under four conditions (reviewer strictly-more-capable **and**
  architecturally diverse; pre-declared criteria; falsifiable output;
  failed-review-escalates), bright-line tasks never downshift, **no downshift
  crosses a data-governance boundary**, and tier→model mappings bind to measured
  capability via a dated mapping-record schema (no model names in doctrine).
  `doctrine/roles.md`'s capability-floors section gains the matching doctrine
  hook. Source: LHM `dev/proposals/archive/2026-06-03-claude-cairn-model-tier-efficiency.md`
  + the `cairn-efficiency-rollout` plan (B1).

- **Session-start skills fan-out self-heal.** The `session-start` lifecycle
  backend (`tools/lifecycle.py`) now re-ensures every eligible, in-use
  symlink-tier skills read-path (today only Claude Code's `.claude/skills`)
  points at the canonical `.agents/skills/` source — so an adopter established
  by lockfile-copy, or whose harness was absent at install, self-heals on first
  run instead of silently having no skills in that harness. It is a faithful
  stdlib-only port of the installer's symlink-tier fan-out contract
  (path-containment, copy fallback + `.gitignore` seed where symlinks are
  unavailable, refuse-or-quarantine that never clobbers a divergent target),
  driven by the now-**installed** `_data/vendor_targets.yml` table so the
  runtime never needs a sibling Cairn checkout to know its targets. New
  `bootstrap/tests/test_skills_self_heal.py` exercises the real backend (the
  full `session-start` entry + a no-Cairn-checkout fixture). Source:
  modflow_tools `dev/proposals/archive/2026-06-04-claude-cairn-foldback-drain-7-candidates.md`
  (Chunk B1) + its drain plan.

- **Doctrine folded up from the modflow_tools reference adopter** (the
  fold-back-ledger drain). Four candidates the adopter proved out, lifted into
  the framework so every adopter inherits them: (1) a **worked-example
  case-study** in `doctrine/dual-review.md` — the different-agent-type floor
  repeatedly catching what the same-vendor pass missed (incl. the author's
  shared blind spot), across proposal / plan / code-review stages, with the
  portable lesson that *green unit tests don't clear the floor — exercise the
  integration path*; (2) the **verify-before-asserting A–E typology** in the
  `claim-check` module (code-shape / file-existence / tree-history / counts /
  API-behavior-under-invocation + the self-contradiction cross-check, framed
  write-time-not-review-time) — the single source of truth, the module that
  already ships the checker; (3) a **"lead with the domain, not the
  architecture"** line in `templates/core/dev/agent_collaboration.md`'s
  "Surfacing judgment calls" (frame a call by what it changes for the user /
  science when the Maintainer is in a domain-expert frame); (4) an **opt-in
  signature-log** Amending pattern in `templates/core/dev/collaboration_agreement.md`
  (signature log + re-signature-on-amendment + revision history +
  decision-time signature — opt-in, not a default). The fifth candidate
  ("briefs to other agents") was already present (`doctrine/dual-review.md` >
  "Briefs to reviewers — don't telegraph the lens"). Source: modflow_tools
  `dev/proposals/archive/2026-06-04-claude-cairn-foldback-drain-7-candidates.md` +
  its drain plan (`dev/plans/2026-06-04-claude-cairn-foldback-drain.md`).

- **`scaffold.py upgrade --finalize` makes a *customized* install verifiable.**
  `verify_integrity` checks on-disk bytes against the lockfile `hash`, but
  `write_install_lockfile` records the *clean-install* hash — so every slot an
  adopter fills, every `VENDOR.md → CLAUDE.md` wrapper rename, and every
  project-owned fork read as integrity tampering (the modflow_tools adopter saw
  19 spurious mismatches establishing its lockfile).  `--finalize` advances
  each record's `hash` to the committed on-disk content so the verifier attests
  the tree the adopter actually ships, while leaving the upgrade ancestor
  (`base_cache` / `base_hash`) untouched.  Verbatim records now carry a distinct
  **`base_hash`** (the as-shipped baseline) separate from `hash`, so
  `classify_verbatim` fork detection survives the `hash` advance — a forked
  verbatim script still classifies `verbatim-locally-modified`, never a clean
  `update` that would clobber the fork (finalize backfills `base_hash` from the
  old `hash` for records that predate the field).  `--apply` and `--finalize`
  both resolve a renamed wrapper's record `dst` to the real on-disk file so
  integrity checks `CLAUDE.md`, not the absent `VENDOR.md`.  Idempotent,
  fail-closed on a tracked file missing on disk.  Surfaced + validated by the
  modflow_tools adopter (the hardest-adopter test) during its Cairn-adoption
  Phase-2 lockfile establishment; Codex final-review findings P1 #1 / P1 #2.
  +3 regression tests (`test_finalize_makes_customized_install_verifiable`,
  `test_finalize_preserves_verbatim_fork_detection`,
  `test_renamed_wrapper_apply_advances_to_resolved_dst`).
- **Richer lifecycle templates, folded up from the modflow_tools adopter** —
  `templates/core/dev/proposals/_template.md` and
  `templates/core/dev/plans/_template.md` gained the generally-useful
  doctrine the modflow_tools deployment had developed inline: the
  `Proposed paths:` forward-reference marker doctrine; archive preconditions
  (every deferred follow-up needs a durable home + an auditable
  `Follow-ups migrated to:` commit body); the file-move / append-only /
  one-commit-per-transition detail; the plan triage rule + fast-multi-stage
  sub-pattern; the plan mutability rule; the full optional pre-implementation
  `## Plan review` apparatus (Format with LOAD-BEARING / important / nit
  labels, Sharpening, multi-round); the code-review falsification ledger; the
  lasting-truth evidence ledger; and the two disposition grammars. Cairn's own
  newer sections (Registered-Report framing, the count-claims mechanism-(3)
  guard, the doctrine-change rate-limit, the planning-handshake scope-fence)
  are preserved. Project-specific bits became five new adopter slots
  (`triage-extra-triggers`, `tests-tier-home`, `examples-smoke-home`,
  `acceptance-doc-tooling`, `verification-commands`); the post-scaffold
  block-slot count rose 15 -> 20 (`docs/quickstart.md` + the
  quickstart-sequence test updated to match). Folded up during the
  modflow_tools Cairn-adoption Phase-2 template reconciliation.
- **Vendor-neutral lifecycle-routine skills** — the session-start /
  session-end routines are now **invokable skills** (the agentskills.io
  `SKILL.md` pair under `.agents/skills/`, with friendly aliases
  `/good-morning` / `/goodnight`), backed by a stdlib-only deterministic CLI
  (`tools/lifecycle.py`).  The skill bodies orchestrate the mechanizable steps
  (gather git state, scaffold the reflection, prune, surface intents); the
  doctrine stays the source of truth.  **Manual-only** with a portable Layer-2
  fail-safe (`session-end` is reflection-only unless an explicit `--handoff`),
  and the destructive full handoff runs only behind a maintainer-designation
  marker **and** a fail-closed concurrent-handoff lock (the single-owner scrub
  invariant, enforced not just remembered).  Installs unconditionally like
  `core/` (the routines are invariant kernel); the canonical `.agents/skills/`
  rides the lockfile + base-cache 3-way-merge upgrade path, fanning out to each
  harness's read-path by tier (alias / verified-symlink / documented manual
  fallback) from a data-driven table.  Cross-vendor support is published by
  **matrix level** (`docs/skills-compatibility.md`), claimed-pending-fixture —
  not a flat "works everywhere" claim.  Security is a first-class gate
  (content-scan over rendered artifacts, no-network, path-containment,
  per-artifact integrity, generated-output leak test).  Source proposal +
  plan: `2026-06-01-claude-cairn-vendor-neutral-skills` (External cross-type
  plan-review + External Security Review + cross-type code review); Cairn
  commits `87078a8..9c5ae1d`.
- **`architecture-review` team-gated module** — a triggered remediation /
  on-ramp frame for an adopter whose architecture *accreted rather than
  was deliberately designed* (inherited legacy, merged prototypes,
  vibe-coded growth).  Ships the module doctrine
  (`templates/modules/team-gated/architecture-review.md`) plus a forkable
  rubric frame (`templates/modules/team-gated/architecture_review_template.md`
  → `dev/architecture_review.md`): five review lenses (Workflow Coherence,
  Data Contracts, Correctness / Provenance Trust, Extensibility,
  Operational Maturity), a "Biases to Challenge" meta-section, and program
  governance.  Opt-in — in no default-on set or governance preset;
  composes with `codebase-readiness-report` (the report says *whether* you
  carry architectural debt, the frame is *how* you examine it).
  Generalizes modflow_tools' `dev/architecture_review.md`; folded via the
  LHM reference deployment's `modflow-tools-doctrine-parity` plan.  +1 test
  class (`TestArchitectureReviewModule`, the 2-spec install contract).

### Changed

- **`verify_integrity` excludes adopter-authored living-state docs from the
  tamper check (the finalize-cadence fix).**  `verify_integrity` exists to
  attest the *shipped Cairn apparatus* (scripts, module/core doctrine,
  templates) was not swapped — a supply-chain check.  But the lockfile also
  tracks four **adopter-authored** files whose content is project state, not
  apparatus: `dev/PLANNING.md` (a living roadmap), `dev/NEXT_SESSION.md` (the
  per-goodnight handoff), `dev/.cairn/cairn_foldback.md` (the fold-back ledger),
  and `dev/collaboration_agreement.md` (the signed agreement).  These are the
  highest-churn files in a mature adopter, so the strict integrity check went
  **red on every routine edit** until a re-finalize — friction that says nothing
  about whether the scripts are trustworthy (surfaced immediately by the
  modflow_tools reference adopter the moment its own archive commit edited
  three of them).  Their lockfile records now carry `living_state: true`: they
  keep `base_cache` / `base_hash` so `upgrade` still 3-way-merges a Cairn
  template change into the adopter's customization, but `verify_integrity` skips
  them (and reports the count).  `write_install_lockfile` stamps the flag at
  install; `upgrade --finalize` stamps it too, migrating pre-`living_state`
  lockfiles.  Deliberately **not** paired with a goodnight auto-`--finalize`:
  blessing whatever is on disk on a schedule would *launder* a real apparatus
  swap — the very thing the check defends — so `--finalize` stays an explicit,
  deliberate re-attestation.  The opt-out is a **verifier policy, not a
  self-asserted lockfile escape hatch** (Codex review P1): `verify_integrity`
  honors `living_state` *only* for a `dst` in the authoritative
  `_LIVING_STATE_DSTS` set and **fails closed** on any other record that asserts
  it — so a modified script cannot hide from the tamper check by flipping one
  lockfile field (the boundary is enforced by the verifier, which validates
  dst-safety + hash-shape *before* honoring the flag).  +4 regression tests
  (`TestLivingStatePartition`, incl. the illegal-opt-out reproducer).
- **The forkable incident-log template no longer reads as `needs-value` on
  every adopter upgrade.**  `templates/modules/default-on/incident_log_template.md`
  is a *fork-on-demand* template (the default-on `incident-trackers` module
  ships it mostly-empty; adopters fork it to a live tracker), but its fill-me
  placeholders used the `{{token}}` install-substitution grammar.  `scaffold.py
  upgrade --plan` therefore flagged the file `needs-value` for *every* adopter
  of the module — raw template variables the upgrade treats as non-advancing,
  reading as "this adopter is not a clean upgrade target" when the file is
  working exactly as designed.  Switched the ten placeholders to the `<...>`
  angle-bracket grammar the other forkable `_template.md` files already use (the
  token resolver ignores it), so the template installs and upgrades cleanly and
  a forked tracker's filled rows are unaffected.  Surfaced by the modflow_tools
  adopter (Codex final-review P1 #3); no behavior change to the
  collision-log parser, which reads filled tracker instances, not the template.
- **Lockfile + adopter profile relocated to `dev/.cairn/` (machinery, not
  docs).**  The install lockfile moved `dev/cairn-lock.yml` →
  `dev/.cairn/cairn-lock.yml` (`_LOCKFILE_REL`), joining the base cache,
  `local-env.json`, the foldback ledger, and onboarding state under
  `dev/.cairn/`.  Reverses the original R2 "visible at the `dev/` root"
  placement: the file is tool-owned (only `scaffold.py` reads/writes it), so a
  `.cairn/` dotfolder is the honest home — it does not hide the file from
  agents, and it keeps the human-meaningful `dev/` listing uncluttered.  The
  committed adopter `profile.yml` similarly belongs under
  `dev/.cairn/profile.yml` (documented in `BOOTSTRAP.md`; `--config` accepts any
  path).  Install / `--init-lock` / `--adopt-module` now `mkdir` the
  `dev/.cairn/` parent before writing.  Existing adopters move the file in
  lockstep.  Full bootstrap suite green.
- **Renamed vendor wrappers now upgrade cleanly (#45 follow-up).**  An
  adopter that renames the thin `VENDOR.md` wrapper to their tool's file
  (`CLAUDE.md`, `GEMINI.md`, …) and removes `VENDOR.md` previously saw a
  spurious `review-only` "file missing on disk" for `VENDOR.md` on every
  `scaffold.py upgrade`: `write_install_lockfile` records the wrapper under
  its canonical `VENDOR.md` dst, and `_compute_upgrade` did not resolve the
  rename for that existing lockfile entry (resolution existed only on the
  `--init-lock` / new-core-file paths).  `_compute_upgrade` now reuses
  `_resolve_vendor_wrapper` so the wrapper classifies under its real on-disk
  name and 3-way-merges cleanly (the base cache stays keyed on `VENDOR.md`).
  Surfaced by the modflow_tools adopter (the hardest-adopter test) during its
  lockfile establishment.  Regression test:
  `test_renamed_vendor_wrapper_resolves_on_standard_upgrade`.
- **Reflections `<session>` and the intent log now share one session
  identity.**  `tools/intent.py` gains a `whoami` command — `whoami` prints
  the resolved per-session identity (the intent log's `agent` field);
  `whoami --session-token` prints just the per-session token (the 8-hex
  `sha256` of the harness session id, refactored into a shared
  `_session_digest` / exposed via `resolve_session_token`).  The
  `reflections` module redefines the filename `<date>-<agent>-<session>.md`
  so `<session>` reuses that token when the coordination/intent module is
  installed — making the `<agent>-<session>` tail reconstruct the intent
  log's `agent` field, so a reflection links to its session's
  `dev/intents.jsonl` entries (raw harness id, then a random token, remain
  the fallbacks; the default-on `reflections` module keeps working without
  the team-gated intent tool).  +4 tests (`TestSessionTokenLink`).

- **Review + collaboration doctrine sharpenings** (LHM
  `modflow-tools-doctrine-parity` plan, Stream 2).  `dual-review` now
  requires a clean code review to *show its work* — a four-part
  **falsification ledger** (probed edge cases / failure modes tested /
  verification run-or-consciously-not / residual risks) **or** a second
  independent different-agent-type pass; a bare "unconditional approval"
  clears no gate (synced from modflow_tools' accepted
  `clean-pass-code-review-gate`, 2026-05-27).  `core/dev/agent_collaboration.md`
  names the **bimodal AI surface** (agent-side roles vs inline-tier editing
  tooling — no role / attribution / decision rights) and a standard
  **session handoff format** (Shipped / Verified / Open Threads /
  Recommended Next Step).  `core/AGENTS.md` states the explicit
  **no-cross-attribution** review rule (the named reviewer commits their
  own findings).  `codebase-readiness-report.md` gains a `Status:` field
  (`draft` / `completed-baseline` / `archived-baseline`) so a filled report
  reads as a snapshot, not a live roadmap plan.

- **Upgrade flow surfaces + enforces the customized-file merge, and
  `init-lock` follows the vendor-wrapper rename** (fold-backs #44/#45 from
  the LHM reference deployment).  `review-only` files (a customized file with
  no recoverable base, or one missing on disk) now surface **per file** under
  a "manual merge owed" header and stage a `.theirs`/`.ours` review pair in a
  sibling `review-only/` dir (never under `files/`, so apply's exactness gate
  is untouched); `upgrade --apply` **fail-closes** on outstanding review-only
  files unless `--ack-review-only`, so a `--stage` → `--apply` can no longer
  silently advance the lockfile while customized doctrine never landed.
  `upgrade --init-lock` now resolves a renamed vendor wrapper (known-vendor-
  name set → `@AGENTS.md`-import content match → warn) and records it under
  its real dst (`CLAUDE.md`, …) instead of dropping it to untracked.
  `UPGRADE.md` documents the completion gate.  Drains the LHM plan
  `cairn-upgrade-flow-hardening`; +8 upgrade tests (incl. the file-missing
  review-only branch), suite 683 pass / `check_cairn` 0 issues.
- **`link_check` / `check_cairn` skip archive + ephemeral sources by
  default.**  The shipped `link_check.py` gains `filter_sources()` and a
  `--include-archives` flag: whole-tree scans now skip sources under any
  `dev/**/archive/` directory (historical records -- links rot by design)
  and under `dev/reflections/` (ephemeral, gitignored), unless
  `--include-archives` is passed.  The rule is anchored to `dev/` as the
  first path segment so `docs/` stays fully link-gated, and matches an
  `archive` segment at any depth (nested archive subdirs covered).  Filters
  *sources* only -- a live doc linking *to* an archived file is still
  validated.  `check_cairn` reuses the same filter for Cairn's self-check.
  Folds back modflow_tools' `verify_doc_links` posture (the reference
  deployment).  Explicit-file invocations are unaffected.
- **Module install now performs mechanical merge with conflict-
  prompt fallback** (Proposal B / audit gap #3).  Modules ship
  structured `<!-- cairn:merge-target: <dst> > <slot> -->`
  directives paired with `<!-- cairn:merge-content-start/end -->`
  block delimiters; `bootstrap/scaffold.py` runs a merge pass after
  module install that handles four cases: empty-slot insert,
  already-current skip, customized-marker preserve, and
  conflict-defer to `<target>.cairn-merge-pending` side-file.
  Adds a `--non-interactive` CLI flag (auto-detected from non-TTY
  stdin per Antigravity P1) that forces deferral; a
  `<!-- cairn:customized -->` slot marker (Antigravity P2) for
  intentionally-customized slots that the fidelity check skips; and
  parse-phase uniqueness validation (Antigravity P3) that raises
  `DuplicateSlotError` with line numbers if a target template
  carries two `cairn:slot` anchors of the same name.  Adds a
  `slot-content fidelity check` to BOOTSTRAP.md Step II-5 that
  catches the wrong-slot / partial-paste / stale-paste failure
  modes the original unfilled-slot check missed.  Existing modules
  without directives are silently skipped (transitional period).
  Tests: `bootstrap/tests/test_module_merge.py` (13 tests across
  6 classes).

- **Commit-permission exception extended to plan- and strategy-doc
  lifecycle commits** (Proposal A Bite 1).  `templates/core/AGENTS.md`'s
  `## Git and commit workflow` section: the "may proceed without
  per-commit approval" carve-out now covers `dev/proposals/` +
  `dev/plans/` + `dev/strategy/` (and any combination), with the
  three guard-rails preserved (push still needs approval; Decision
  commits stay Maintainer-only / Maintainer-scribed; bundling with
  non-lifecycle files loses the exception).  Ports the doctrine
  bite from the modflow_tools reference deployment commit `246ad13`.

- **"Untracked lifecycle artifacts" sub-section added to
  `templates/core/AGENTS.md`** (Proposal A Bite 3).  Names the third
  commit-discipline hazard in the family alongside the
  shared-comm-files arc + staged-index arc: writing a lifecycle-
  opening artifact without committing it the same turn.  Ships the
  doctrine bite + two corollaries + a cold-start recovery procedure
  (an agent starting cold checks for untracked lifecycle drafts +
  resolves ownership via the work-intent system rather than acting
  unilaterally).  Cross-references the `incident-trackers` module
  (lands in this release window) as the substrate.

### Security

- **Containment guards landed in the onboarding-activate helper**
  (plan
  `2026-05-28-claude-cairn-security-hardening-post-v0.2-followup`;
  Antigravity proposal-review I-3 + P1 + plan-review P2/P3).
  `templates/modules/default-on/onboarding_activate.py` now carries
  the same three-check fail-closed pattern that the scaffold's
  `_assert_safe_write` (in `bootstrap/scaffold.py`) established for
  the scaffold
  (`ScaffoldSecurityError` -> `OnboardingSecurityError`):
  every target-derived write site (`planning_path.write_text` in
  both `activate()` and `seed_existing_adopter()`; the
  `os.open(O_WRONLY|O_APPEND|O_CREAT)` log-append site with the
  `mkdir → assert` ordering per Antigravity plan-review P2-1) and
  read site (planning + source + log + changelog + collaboration-
  agreement + fold-back ledger) runs `_assert_safe_write` or
  `_assert_safe_read`.  Glob-loop sites in
  `_count_archived_proposals`, `_count_archived_plans`,
  `_list_proposal_files`, `_list_plan_files`, and
  `_has_cross_type_review_anywhere` use the parent-once +
  per-leaf `is_symlink()` pattern from Antigravity plan-review P2-2
  (security-equivalent to per-leaf `_assert_safe_read` at much
  lower cost on large archives).  Preset-name validation
  defense-in-depth: `_PRESET_META_RE`'s capture group is
  restricted to `[a-zA-Z0-9_-]+` (so traversal sequences are
  refused at the regex level), `extract_preset_from_slot`
  re-validates the captured name through the strict
  `_PRESET_NAME_RE`, and `seed_existing_adopter` validates the
  `--preset` CLI flag through `_PRESET_NAME_RE` BEFORE the
  `VALID_PRESETS` allowlist check so an attacker-controlled
  `--preset ../etc/passwd` surfaces a security error (exit code 2
  per Antigravity plan-review P3-1) rather than the operational
  "unknown preset" exit 1.  Tests:
  `bootstrap/tests/test_onboarding_activation_helper.py`
  (`TestContainmentGuards` 6 cases + `TestPresetNameValidation` 3
  cases) and `bootstrap/tests/test_hardening.py`
  (`TestCrossHelperContainment` 1 case asserting both helpers
  refuse the same planted-symlink tree).  Implementing commits:
  `3f78c0b` (P1.1 helper guard infrastructure + exit-code branch),
  `0294493` (P1.2 guards wired at every target-derived call site),
  `0c433cd` (P1.3 containment-guard tests + cross-helper
  integration).  Note (Internal-P3-#5): commit-subject prefixes
  use the plan-chunk identifier (`P1.1`, `P1.2`, `P1.3`) to
  disambiguate from earlier progressive-onboarding plan chunks
  that share the same `P1.<n>` numbering.

### Added

- **`documentation-plan` default-on module: placement-decision
  procedure + four-layer doc/doctrine vision + forkable
  `docs/DOCUMENTATION_PLAN.md`** (Proposal D, fast-tracked per
  maintainer 2026-05-28).  Ports modflow_tools' reference-deployment
  `docs/DOCUMENTATION_PLAN.md` doctrine to Cairn as a default-on
  module.  Ships:
  * **Module doctrine** at
    `templates/modules/default-on/documentation-plan.md` -- the
    `Selected when:` / `Adds to:` shape parallel to incident-trackers,
    with three explicit `Merged into:` blocks (Block 1 for AGENTS.md,
    Blocks 2-3 for the proposal + plan templates) carrying the
    paste-into-slot content.  Mechanical merge via Proposal B's
    `cairn:merge-target` directives is **deferred** for this module
    pending resolution of the merge-pass / install-lockfile
    interaction (the merge pass mutates files post-install, which
    currently makes the lockfile's clean-install divergence guard
    refuse to write -- tracked as a separate Cairn follow-up).
  * **Forkable template** at
    `templates/modules/default-on/documentation_plan_template.md`
    -- installs at adopter `docs/DOCUMENTATION_PLAN.md`; carries the
    four-layer vision (entry / governing / deliberation / descriptive),
    the decision procedure ("what is this artifact *doing*?"), voice
    rules, naming conventions, the `AGENTS.md` ↔
    `agent_collaboration.md` boundary doctrine, and a customizable
    descriptive-tier table.  All worked examples use adopter-relative
    paths (no `cairn/` prefix).
  * **Cairn self-hosted** at `docs/DOCUMENTATION_PLAN.md` -- Cairn's
    own dogfood instance, with cairn-prefixed worked examples
    discussing Cairn's actual file inventory (doctrine essays under
    `cairn/doctrine/`, the template-shipped `cairn/templates/core/`,
    the Goal-1 `cairn/dev/` substrate).
  * **Slot anchors** in three core templates:
    `templates/core/AGENTS.md` gains a `## Documentation discipline`
    section with the `documentation-discipline` slot;
    `templates/core/dev/proposals/_template.md` gains the
    `documentation-tier-home` slot inside its existing `###
    Documentation / doctrine surface` section;
    `templates/core/dev/plans/_template.md` gains a new `###
    Documentation / doctrine surface` subsection under `## Scope`
    with the same slot name.
  * **Bootstrap install**: `_DEFAULT_ON_MODULES` gains
    `"documentation-plan"`; `_MODULE_MAPPINGS` gains the entry
    installing the module doctrine to `dev/modules/` and the forkable
    directly to `docs/DOCUMENTATION_PLAN.md`.

  Three Antigravity findings dispositioned in the proposal Response:
  P1 broken adopter-template references -> all worked examples are
  adopter-relative (no `cairn/` prefix); P2-a worked-examples leakage
  -> two-artifact split (Cairn-self-hosted dogfood + adopter forkable);
  P2-b optional-adoption dead links -> module packaging (no hardcoded
  cross-reference; opt out via `modules: [-documentation-plan]`
  cleanly drops the slot fills); P3 link-check coverage ->
  `scripts/check_cairn.py`'s existing link check covers the new
  cross-reference automatically via Cairn's dogfood install.  The
  larger "programmatic placement-decision enforcement" follow-up
  (Antigravity P3's stretch suggestion) is deferred to
  modflow_tools-side PLANNING for after the procedure stabilizes
  through adopter use.

  Tests: `bootstrap/tests/test_documentation_plan_module.py`.

- **`incident-trackers` default-on module: forkable tracker
  template + goodnight migration sub-step; parse target for the
  adaptive-doctrine rate-limit gate** (Proposal C).  Ships:
  module doctrine at `templates/modules/default-on/incident-trackers.md`;
  forkable tracker template at
  `templates/modules/default-on/incident_log_template.md` carrying
  the canonical 7-column semantic-field schema
  (`Date | Event Class | Description | Recurrence-Window Match |
  Impact | Migrated From Reflection | Resolved By`); goodnight
  migration sub-step in `doctrine/session-routines.md`;
  cross-reference paragraph in `doctrine/rationale.md` naming the
  module as the rate-limit gate's substrate; `_DEFAULT_ON_MODULES`
  + `_MODULE_MAPPINGS` entries in `bootstrap/scaffold.py`.  Three
  Antigravity findings dispositioned in the proposal Response:
  P1 schema-divergence threat to Goal 7 → 7-column semantic-field
  contract (operates on field semantics, not column-header text);
  P2 missing audit-trail closure → `Resolved By` column accepting
  proposal stem / commit SHA / `pending`; P2 prevented incidents
  counted as occurrences → `Impact` column with three values
  (`occurred` / `prevented` / `non-conflict`).

- **"Count claims -- soft-flag clearance" template guidance added
  to both `templates/core/dev/proposals/_template.md` and
  `templates/core/dev/plans/_template.md`** (Proposal A Bite 2).
  Two additions per template: a 10-line `<!-- Author tip: -->`
  HTML comment block at file head summarizing the four clearance
  mechanisms, and a `## Count claims -- soft-flag clearance`
  section in the doctrine reference area carrying the six
  tree-nouns + four clearance mechanisms + the discipline
  antipattern warning + worked-example self-exemptions.
  Mechanism (3)'s description sharpened per Antigravity finding:
  "Reserved for prescriptive rules or historical quotes; never
  for live / mutable counts where mechanisms (1) delta or
  (2) cited command would be cleaner."  The mechanism (the
  `claim-check-allow-count` directive) already ships in
  `claim_check.py`; this lands the teaching that makes it usable.

- **Progressive onboarding: PLANNING-as-onramp + maturity/action
  trigger system + active-surfacing at relationship-changing
  transitions.**  Ships the post-install counterpart to the
  static entry-surface artifacts (quickstart + bootstrap-lite +
  profile examples + readiness-report); supersedes Goal 6 of
  the modflow_tools-side 0.3 roadmap.  Per the adopter
  proposal + plan at
  `dev/plans/archive/2026-05-28-claude-cairn-progressive-onboarding.md`
  (modflow_tools side).  L3 scope: three preset onboarding
  files + full trigger matrix + all four active-surfacing
  prompts + both tour docs.

  **Mechanism summary**:
  * **Preset-keyed PLANNING slot**
    (`templates/core/dev/PLANNING.md` +
    `bootstrap/scaffold.py`): new
    `<!-- cairn:slot onboarding-tasks -->` block between
    `## Where the project stands` and `## Queued`.  Scaffold
    inlines ONLY the preset's seed tasks + a
    `<!-- preset: <name> -->` metadata comment; deferred tasks
    stay in the installed source file at
    `dev/modules/onboarding/<preset>.md` (the authoritative
    reference the activation helper reads at goodnight).
  * **Three preset onboarding files** in
    `templates/onboarding/`: `solo-greenfield.md` (1 human + 1
    AI agent), `collaborative-team.md` (2-4 humans + 1-2 agent
    types), `high-rigor-legacy.md` (5+ humans + multi-agent +
    legacy + multi-language + security boundaries).  Each
    carries seed tasks + deferred tasks (with `[trigger: X;
    id: Y]` syntax) + four active-surfacing prompt content
    blocks (one per active-surfacing row, calibrated per
    preset).
  * **State file + activation helper**
    (`templates/modules/default-on/onboarding_activate.py` ->
    adopter `scripts/onboarding_activate.py`).  Activates
    deferred tasks into PLANNING + emits at most one
    active-surfacing prompt at goodnight; reads
    `<!-- preset: <name> -->` slot metadata to resolve the
    source file; appends one record per activation to the
    tracked `dev/.cairn/onboarding-activated.jsonl` log
    (parallel to `dev/intents.jsonl`'s atomic-append
    precedent).  Default mode + `--dry-run` + `--seed`
    (existing-adopter manual opt-in).
  * **Trigger matrix** (`evaluate_maturity_triggers` +
    `evaluate_action_triggers`).  Four maturity-ladder
    (`level-0-to-1`, `level-1-to-2`, `level-1-deepen`,
    `level-2-deepen`) + eight action triggers
    (proposal/plan/changelog firsts + `second-agent-type`
    (roster-based) + `first-cross-type-review` (file-content
    scan) + `first-foldback-candidate` (ledger scan) +
    `collab-agreement-signing` (roster-unfilled + prior
    proposal-archive precondition)).  Triggers observe
    EXPLICIT deployment state per the Codex External Review
    P2-3 disposition; no git archaeology for active prompts.
  * **Active-surfacing emission** with UX caps (<=1 prompt
    per goodnight; <=3 newly-inserted tasks per goodnight)
    and priority order (collab-agreement > Level-1->2 >
    second-agent-type > foldback-walkthrough); overflow
    defers to next goodnight via the derived held-task store.
  * **Doctrine doc** (`doctrine/onboarding.md`): full
    mechanism + state-file schema + trigger matrix + UX caps
    + priority order + existing-adopter manual-opt-in 4-step
    recipe + v1.x capability-pull-from-adopter follow-ups.
  * **Session-routines extension**
    (`doctrine/session-routines.md`): new subsection naming
    the activation helper as a standing goodnight step paired
    with foldback-capture.
  * **Tour docs** (`docs/dev-tour.md` day-one-accessible +
    `docs/agent-team-onboarding.md` second-agent spin-up
    checklist).

- **Fold-back active-surfacing: deployment-side machinery for
  issue/PR suggestions to Cairn.**  Ships the *active half* of the
  fold-back loop -- the bridge between existing passive-capture
  machinery and the eventual Cairn-side filing.  Five components
  (A doctrine extension + B GitHub templates + C agent prompt + D
  module merge + E optional helper) plus a plan-added scanner.

  **Mechanism summary**:
  * **Doctrine** (`doctrine/fold-back.md`): new "Active surfacing"
    section with the six-step protocol (Recap / Choose / Compose /
    Scrub / Submit / Record), the 5-machine-gated + 2-manual-
    affirmation no-export class taxonomy (IP addresses get the
    bright-line "BOTH deployment-internal AND remote-repo"
    treatment per maintainer directive), and the extended status
    vocabulary (`filed -> <#>` / `pr -> <#>` / `deferred-until`
    schema; migration rule guarantees existing ledgers stay valid).
  * **GitHub templates** (`.github/ISSUE_TEMPLATE/foldback.md` +
    `.github/PULL_REQUEST_TEMPLATE/foldback.md`): structured
    pre-fill with explicit maintainer-signed export-safety
    affirmation field.  Created Cairn's `.github/` directory.
  * **Agent prompt** (`templates/modules/default-on/fold-back-active-prompt.md`):
    vendor-neutral; carries the six-step protocol + 5+2 no-export
    checklist + fail-closed scrub-gate invocation +
    `--body-file <draft.md>` `gh` pattern + status-transition
    contract.
  * **Module merge** (`templates/modules/default-on/fold-back-ledger.md`):
    adds the goodnight foldback-surfacing step adjacent to the
    existing foldback-capture step.
  * **Export-scrub scanner** (`templates/modules/default-on/foldback_export_scan.py`):
    stdlib-only, 5 mechanical detector classes (credentials,
    private paths, IPs with RFC 5737/3849 documentation allowlist,
    internal hostnames, adopter-configurable proprietary tokens).
    Ships verbatim into adopter `scripts/`.  Replaces a plan-open
    assumption (`content_scan.py` would do this work) verified
    false at plan-review time.
  * **Optional surfacing helper** (`templates/modules/default-on/foldback_suggest.py`):
    stdlib-only ledger parser; lists open `candidate`-status rows
    eligible for surfacing (skips snoozed-via-`deferred-until` rows).
  * **`.gitignore` seed**: `_GITIGNORE_SEEDS` adds
    `dev/.cairn/.foldback-draft-*.md` so the protocol's drafted-
    body temp file pattern is never accidentally committed.

  Source proposal:
  `2026-05-28-claude-cairn-foldback-active-surfacing` (deliberated
  modflow_tools-side; accepted 2026-05-28).  Implementing plan:
  `2026-05-28-claude-cairn-foldback-active-surfacing` > Chunks 1-10.
  Cross-type Codex External plan-review landed + sharpened
  (5 findings: 2 P1 + 2 P2 + 1 P3; the load-bearing P1 N1 caused the
  Chunk 4 pivot from a `content_scan.py` wrapper to a new dedicated
  scanner).  ~60 new tests across `bootstrap/tests/test_foldback_*.py`
  + extensions.  Dogfood at Chunk 9 verified the protocol's machine
  half end-to-end against modflow_tools' current open candidates;
  binary outcome (per Codex plan-review P4): the existing ledger
  schema IS sufficient to draft a complete issue body via the
  protocol -- no schema-enrichment follow-up needed.

- **Docs architecture cleanup: `doctrine/doc-governance.md`
  expanded into a coherent two-half documentation-governance
  doctrine + team-gated module disambiguation.** Source proposal:
  `2026-05-28-claude-cairn-docs-architecture-cleanup` (deliberated
  modflow_tools-side because Cairn does not yet self-host
  `dev/proposals/`; accepted Anthony 2026-05-28). Implementing
  plan: `2026-05-28-claude-cairn-docs-architecture-cleanup`. Cairn
  commits: `42b4d73`, `7545f8f`, `86c266f`, `9d5ad4a`, `868834b`
  (Chunks 2, 3, 7, 8 + Antigravity-2/3 sharpening).

  * **`doctrine/doc-governance.md` opens with a two-half framing.**
    Governing-file routing (`AGENTS.md` vs `agent_collaboration.md`,
    the original scope) + descriptive-layer recognition (`docs/`,
    the new scope from this package).  Sub-heading levels demoted
    to reflect the structure; a reader scanning the table of
    contents now sees the two halves clearly.

  * **Tier recognition + common homes for vision** (Chunk 2).  The
    descriptive layer is recognized as conventionally tiered by
    audience (Quickstart / User Guide / Theory-Reference /
    Developer); the doctrine enumerates four typical homes for a
    project's vision / charter (`docs/developer/vision.md`,
    `README.md`, `docs/`-root vision page, `dev/vision.md`) without
    recommending among them.  Per the maintainer's M1 layer-
    prescriptiveness gradient: tier-RECOGNITION holds;
    tier-LEGISLATION drops.  The `templates/core/dev/README.md`
    template drops its `vision.md` mention -- the doctrine's
    common-homes section carries the dialogue surface (eventually
    wired into the interactive-onboarding `0.3` goal).

  * **Format-neutrality + module disambiguation** (Chunk 3).  An
    adopter's `docs/` format is the adopter's choice (Markdown /
    reStructuredText / Asciidoc / Quarto); Cairn's `.md`
    cross-references point INTO Cairn, not into the adopter's
    tree.  The three team-gated modules that reference Cairn's
    `further-reading` (`examples-gallery`, `doc-drift-prevention`,
    `testing-discipline`) carry the link-text disambiguation
    `Cairn's own cairn/docs/further-reading.md` (so the bracketed
    label inside any Markdown link reads as a Cairn-owned path)
    and the target is unambiguously Cairn-owned -- an adopter using
    a non-Markdown docs format is not implicitly steered toward
    `.md`.  Per Antigravity-3 plan-review finding option (i):
    link-text disambiguation, no URL hardcoding.

  * **Common homes for style conventions** (Chunk 7).  Style
    conventions are project-specific descriptive content rather
    than universal governing doctrine.  Four typical homes
    enumerated (`docs/developer/style.md`, `docs/style.md`,
    project-specific equivalent, `STYLE_GUIDE.md` at root) without
    recommending among them.  Per the maintainer's M2 chat-
    preference clarification.

  * **Coherence pass** (Chunk 8).  Opening intro rewritten to make
    the two-half structure explicit (governing-file routing +
    descriptive-layer recognition); subsection headings demoted;
    cross-references between the new sections + the pre-existing
    governing-file-routing content confirmed intact.

  * **Tests** -- `bootstrap/tests/test_doc_governance.py` (new
    file): 27 doctrine-presence cases covering tier-recognition,
    common-homes-for-vision, format-neutrality, module
    disambiguation, scaffold-rendered installed-adopter wording
    (Codex-3 of the proposal review), style-conventions location.

  * **Sharpening commits** addressing the External Code Review
    (Antigravity, 2026-05-28; 4 findings, all accepted):
    `868834b` (Cairn-side findings 2 + 3): `templates/core/dev/README.md`
    doc-governance link relative-depth fix + "Cairn's own"
    disambiguation; 6 team-gated module backtick-in-link-text
    removals per the style-guide rule.

### Changed

- **`upgrade --plan` / `--stage` summary distinguishes untouched
  files from locally-modified-but-merged-clean files.**  The
  `clean` summary row previously lumped together two situations
  with very different adopter meaning: files the adopter never
  touched (a pure upstream advance) and files the adopter
  customized that merged cleanly with the new upstream (their
  customizations rode through).  The summary now reports them
  separately as **`clean (untouched)`** and **`locally-modified
  (merged clean)`** so the adopter sees their customizations were
  preserved.  Internal kind name: `clean-locally-modified`
  (advances identically to `clean`; staged + applied the same
  way).  Source proposal:
  `2026-05-28-claude-cairn-0.2.x-sweep-and-ledger-followups`
  Chunk 3 (B-C-1 sweep nit).  Comparison uses
  `substitute_tokens(base_raw, tokens)` so a normally-installed
  file (where ours has `Demo` for `{{project_name}}`) is not
  flagged as locally-modified by virtue of the token substitution
  alone.  Tests: the `TestUpgradeModes` class in
  `bootstrap/tests/test_upgrade.py` gains 3 tests covering the
  locally-modified, untouched, and display-label paths.

### Added

- **`scripts/quality_gate.py` -- consolidated pre-cut quality-gate
  suite.**  Three stdlib-only sub-gates unified under one CLI:

  * **order-independence** (D-3) -- pytest invocation wrapper with a
    deterministic seed contract (`--seed`, `--seed-count`,
    `--seed-list`; default seed=[0]; every run echoes the seed; a
    failure surfaces with its seed for reproducibility).  Uses a
    stdlib `random.Random` shuffle hook in
    `bootstrap/tests/conftest.py` -- no pytest-randomly dependency.
  * **neutrality** (E-4) -- mechanized R-G vendor/project-token lint
    scoped to doctrine + dimensions + on-ramp + docs + examples +
    bootstrap `.md` files.  Three sanctioned-exception directives:
    `<!-- vendor-ok: reason -->` (line / next-line);
    `<!-- vendor-ok-begin: reason -->` / `<!-- vendor-ok-end -->`
    (block); `<!-- case-study -->` (whole-file, only valid under
    `cairn/case-studies/`).  ANY directive inside `cairn/templates/`
    fails the gate (templates ship to adopters; a leak there would
    propagate).  Rationale required on every directive; report
    exposes every applied exemption.
  * **redundancy** (G R1 + R6) -- R1 shingle/Jaccard overlap on the
    `.md` corpus (default 5-word shingles, Jaccard >= 0.75; tunable
    via `--shingle-size` / `--jaccard-threshold`); R6 stdlib AST
    unreferenced-def detector on production `.py` files with a
    sibling whitelist file (`scripts/quality_gate_unused_def_whitelist.py`)
    for static-dispatch callbacks (argparse `_cmd_*`, public-API
    exports).  R7 (capability necessity) and the R1 layer-contract
    filter stay manual -- checklist + dogfood disposition log in
    `doctrine/consolidation-review.md`.

  CLI: `--sub <name>` (repeatable; default all); `--report`
  (TAB-separated machine-readable); `--root <dir>`; exit codes
  ``0`` clean / ``1`` fail / ``2`` usage error.  Source proposal:
  `2026-05-28-claude-cairn-0.2.x-sweep-and-ledger-followups`
  Component A.  Tests: 48 new under `bootstrap/tests/test_quality_gate_*.py`.
  BOOTSTRAP.md Act II-5 R-G recipe now points at this sub-gate as
  the mechanized form.  First dogfood pass against Cairn `master`
  surfaced 8 neutrality + 1 redundancy real findings (all
  dispositioned in `doctrine/consolidation-review.md` > Dogfood
  disposition log) + ~60 R6 pytest-discovery false positives (fixed
  in-Chunk by scoping R6 out of `bootstrap/tests/` and skipping
  `Test*` / `test_*` names defensively).  Code-review sharpening
  (2026-05-28): the gate previously short-circuited template-file
  scans after the directive-forbidden check, silently letting
  vendor-token leaks through; the sharpening continues the token scan
  in templates (no exemption path applies), surfacing 4 pre-existing
  template-leak findings in `lifecycle_metrics.py` + `link_check.py`
  rephrased in this same arc.  `content_scan.py`'s
  instruction-bearing-HTML-comment heuristic now recognizes the
  `vendor-ok` / `vendor-ok-begin` / `vendor-ok-end` / `case-study`
  family as legitimate Cairn-owned directive syntax.  `--report`
  machine mode now escapes embedded newlines so multi-line failure
  messages stay one-finding-per-line.

- **`claim_check.py` document-scoped exemption directives -- the
  full allow-directive family.** Two new HTML-comment directives
  let an author exempt specific would-be-flags without disabling
  the heuristic across the rest of the document, complementing the
  existing per-line marker-line mechanism and the file-scoped
  `--external-allow` CLI flag:

  * **`<!-- claim-check-allow: <glob>[, <glob>...] -->`** -- a
    standalone HTML-comment declares one or more path-globs as
    consciously accepted; backticked tokens whose path part matches
    one are exempt from the hard path / line-bounds checks.  Globs
    must be specific (>= 2 literal path segments before any wildcard
    AND a literal filename stem in the final segment); a too-broad
    glob is itself a hard flag.  The directive exempts only
    *unresolved-path* flags: a glob match on a path that exists in
    the tree is ignored, so an out-of-range line-bounds citation
    into a real file still hard-flags.  Each suppressed token is
    reported in the run output for audit.
  * **`<!-- claim-check-allow-count: <count>[, <count>...] -->`** --
    the sibling for category-D count claims: comma-separated count
    tokens (e.g. `728 tests, 30 lines`) are declared consciously
    accepted, suppressing their soft flag document-wide.  Each
    accepted token must be named exactly (number + tree-noun); there
    is no wildcard form.  Each suppressed token is reported.

  Diff-driven port from modflow_tools' adopter-customized
  reference-deployment `claim_check.py` (commit `10751d6`); the
  structural unit is the allow-directive family because modflow_tools
  had built both directives as siblings sharing the `_scan` exemption
  surface and the CLI report block.  Source proposal:
  `2026-05-28-claude-cairn-0.2.x-sweep-and-ledger-followups`
  (deliberated modflow_tools-side; accepted 2026-05-28).
  Implementing plan: `2026-05-28-claude-cairn-0.2.x-sweep-and-ledger-followups`
  > Chunk 1.  Tests: `bootstrap/tests/test_claim_check_module.py`
  (25 new tests across glob-validation, path-directive, and
  count-directive surfaces).  Full Cairn suite stays green (331 passed
  post-port vs 306 pre-port).  Closes the only Open candidate in
  `dev/.cairn/cairn_foldback.md` going into the 0.2.x sweep window.

- **Adopter-friction package: seven entry-surface artifacts + a
  Cairn-side regression suite.** Source proposal:
  `2026-05-27-claude-cairn-adopter-friction-package` (deliberated
  modflow_tools-side because Cairn does not yet self-host
  `dev/proposals/`; accepted by Anthony 2026-05-28). Implementing
  plan: `2026-05-28-claude-cairn-adopter-friction-package`. Cairn
  commits: `867c321..<tip>` (Chunks 1, 2, 3, 5, 7, 8 + gate /
  pilot sharpenings). The seven items, by Cairn surface:

  * **`docs/quickstart.md`** -- copy-paste recipe for one human +
    one AI agent on a disposable repo, 15--25 minutes (pilot
    measured 12 minutes active / 40 minutes wall-clock).  Seven
    steps from `git init` through teardown; copies
    `bootstrap/profiles/solo-greenfield.yml` literally; Step 3
    splits preview-then-install; Step 6 documents five
    lifecycle-boundary commits.  Carries a six-axes glossary, an
    editor-orientation tip before Step 4, and a "where the agent
    will write" overview of `dev/proposals/` shape -- all surfaced
    by the literal pilot.  README pointer added at the top of
    "How to adopt".

  * **`bootstrap/profiles/`** -- three copyable governance-preset
    YAMLs (`solo-greenfield`, `collaborative-team`,
    `high-rigor-legacy`); each carries an in-file comment header
    naming the six-axis dimensional profile it expresses and
    references the matching named preset via `preset:`, so module-
    roster selection stays in `_PRESETS` (`bootstrap/scaffold.py`)
    rather than being duplicated in the YAML.

  * **`bootstrap/prompts/bootstrap-lite.md`** -- the short first-
    contact agent prompt for one-human + one-agent adopters who
    have a real repo.  Sits between the throwaway-repo quickstart
    and the full Level 2 procedure: the agent surveys the target
    repo, scores the six axes with reproducible reasons,
    recommends one of the three named presets, proposes a
    profile.yml, then **stops** for the Maintainer's acceptance.
    Preserves the load-bearing profile-acceptance gate; collapses
    only the manual axis-scoring step.  `bootstrap/BOOTSTRAP.md`
    carries a pointer paragraph near the top for readers who
    arrive there first.

  * **`templates/codebase-readiness-report.md`** -- eleven-section
    readiness template for legacy scientific codebases (Tests,
    Hidden state, Scripts, Notebooks, Data I/O, Generated outputs,
    Public APIs, Build/run commands, Reproducibility, Security
    boundaries, Scientific assumptions).  G/M/P self-score table;
    profile-mapping appendix with scaffold-block-recommendations
    for sections 10 (security) and 11 (scientific assumptions).
    **Default check-in posture is safer**: fill locally, then
    commit only a redacted summary or a scores-and-follow-ups
    decision to `dev/`; full report check-in is an explicit
    opt-in gated on a Maintainer affirmation in the commit body
    that the artifact contains no secrets, private paths, or
    proprietary detail.  Sections 5 and 11 sharpened by the pilot
    (external dataset provenance / calibration-parameter prompts).
    README + on-ramp pointers added.

  * **`examples/scientific-minimal/`** -- parallel to
    `examples/minimal/` with a CSV-in / mass-balance-invariant-
    tested / residual-table-out scientific workflow.  The toy
    science is a monthly water-budget reconciler
    (`precip - et - runoff - recharge = dS_storage`); the residual
    is tested as a mass-balance invariant
    (`max(|residual|) < RESIDUAL_TOL_MM`) with two parametrized
    falsification sentinels.  No third-party dependencies (`csv`
    + `pathlib`); runs anywhere Python 3.10+ runs; both
    repo-root-relative and example-dir-relative invocations
    documented and tested.  The example's
    `dev/proposals/archive/0001-add-mass-balance-invariant-test.md`
    traces the trivial-accept lifecycle on a scientific workflow.

  * **`README.md` trust box** (above "Who Cairn is for") -- ~200
    words: what the AI agent reads (the repo + the profile YAML),
    what must NOT enter Cairn-shipped artifacts (secrets,
    credentials, private paths, embargoed datasets), what
    scanners run on Cairn-shipped files (vendor-neutrality,
    `content_scan.py`, `link_check.py`, `claim_check.py`), and
    what the agent does *not* do (no exfiltration, no rewrites of
    unconsented files), with a cross-ref to `SECURITY.md`.

  * **Honest-framing callouts in `README.md`, `on-ramp/README.md`,
    and `docs/getting-started.md`** -- "Cairn is slower for the
    first few changes; it pays back later" stated explicitly in
    each file's voice, with a pointer to the on-ramp ladder as
    the self-locate aid.  Audit found no bare "faster" marketing
    claims to *rewrite* (the docs were already careful); the
    edits are ADDITIVE callouts, not in-place rewrites.

- **`bootstrap/tests/test_profiles_smoke.py`** (15 cases) +
  **`bootstrap/tests/test_quickstart_sequence.py`** (8 cases,
  Layer A shell + Layer B scripted-surrogate lifecycle-shape with
  sentinel `LAYER_B_IS_LIFECYCLE_SHAPE_ONLY = True`) +
  **scientific-minimal-example invariant test** (6 cases) -- the
  Cairn-side smoke suite the adopter-friction package committed
  to (per the proposal's Codex P2-A finding). 29 new test cases
  total; pytest count 285 → 314.

## 0.2.0 — 2026-05-27

### Added

- **Security hardening -- SSRF guard, derived Bandit gate, supply-chain
  tooling, and a public security contract
  (cairn-v0.2-security-hardening, 2026-05-27).** A single hardening cut from a
  full security review, before the v0.2.0 tag (External plan + code review:
  Codex; Antigravity approved the code unconditionally). The shipped
  executable surface is now defended end-to-end:
  * **SSRF-guarded external link probe.** `link_check.py --check-external`
    is http(s)-only with **per-hop host validation** (allow only
    `is_global` addresses -- loopback / private / link-local / CGNAT
    `100.64.0.0/10` / reserved / multicast refused, IPv4 + IPv6), manual
    redirects with a hop cap, no proxy/auth/netrc handlers, and an
    `--allow-host` opt-out; the DNS-rebind residual is documented.
  * **The Bandit gate stopped being blind.** `test_security_lint.py` now
    **derives** its scan set from `_MODULE_MAPPINGS` + the dev executables
    (`scripts/*.py`, `bootstrap/*.py`) as explicit files, so a newly-shipped
    script can't escape it (the prior hand-list missed three team-gated
    scripts and scanned `scripts/` as a non-recursing directory). The B613
    trojansource HIGH in `content_scan.py` was cleared (escape forms +
    a bytes-level guard); the post-commit `intent` hook quotes its baked-in
    paths with `shlex.quote`; `lifecycle_metrics` CSV output neutralizes
    formula-injection; the homoglyph check covers more confusable scripts.
  * **Adopter-facing supply-chain controls.** A new **`content-security`**
    team-gated module ships the content-integrity scanner
    (`content_scan.py`, single-sourced -- the same file Cairn's own
    `check_cairn.py` composes) so adopters can scan working-tree files / PRs
    for prompt-injection before agents ingest them; and
    `bootstrap/verify_integrity.py` is a **fail-closed, lockfile-backed**
    SHA-256 install-integrity check (path-contained against a tampered
    lockfile) that detects post-install file modification.
  * **Release + doctrine surface.** `bootstrap/security_check.py` is a
    fail-closed **release** gate (fails, never skips, when Bandit is absent);
    `SAFETY.md` Rule 7 enumerates the full executable surface + documented
    residual risks; and a public [`SECURITY.md`](SECURITY.md) states the
    threat model, supported versions, vuln reporting, and the release
    checklist. Source: the modflow_tools-hosted `cairn-v0.2-security-hardening`
    arc.

- **Fold-back: process hardening -- claim-marker carve-out, a
  plan-review entry gate, and work-intent adherence triggers
  (cairn-foldback-process-hardening, 2026-05-27).** The last three proven
  process-hardening fold-backs from the reference deployment, synced before
  the v0.2.0 cut (External proposal review: Codex).
  * **(A) Claim-marker maintenance is not authoring a review.**
    [`doctrine/lifecycle.md`](doctrine/lifecycle.md) (and both core
    proposal/plan templates) now carve out a bounded exception to
    append-only: inserting a `claim_check` marker line adjacent to a path
    token -- to clear a forward-reference / sibling-repo flag -- is
    mechanical maintenance, permitted even in another agent's section,
    bounded by four properties (additive-only / mechanical / auditable +
    unbundled / typo-guard). The `claim-check` module notes the distinction
    from its own deferred Markdown-content-gate hook.
  * **(B) A plan-review entry gate.** Symmetric to the plan-archive
    (review-before-close) precondition,
    [`doctrine/lifecycle.md`](doctrine/lifecycle.md) adds a
    *review-before-implement* precondition: the plan status taxonomy gains
    `awaiting-plan-review`, and every plan (and its source proposal) carries
    a mandatory **`Plan review: required(<tier>) | not required(<rationale>)`**
    line with no silent default. A `required` plan keeps its plan-open and
    first-implementation commits distinct; the tier follows the
    structural-independence framing
    ([`doctrine/dual-review.md`](doctrine/dual-review.md)).
  * **(C) Work-intent adherence triggers.** The `coordination-tiers`
    intent tool gains an opt-in **work-intent pre-commit check**
    (`install-precommit` + `hooks-status`; the post-commit `install-hook`
    is unchanged) that warns -- never blocks -- when a commit's staged set
    (`git diff --cached`) carries an unclaimed path or one held by another
    session. A per-commit `CAIRN_INTENT_ALLOW_UNCLAIMED` / tracked
    `dev/intent-config.json` `solo_mode` suppresses the self-directed
    warnings but never an other-session overlap. The session-start routine
    gains the *read* half (`intent list`). Source: the modflow_tools-hosted
    `cairn-foldback-process-hardening` arc.
- **Fold-back ledger candidates -- doc-governance boundary, reviewer
  decision-support + a Decision-scribing guard-rail, and a formalized
  fold-back mechanism (cairn-foldback-ledger-candidates, 2026-05-27).**
  Three generalizable-doctrine fold-backs from the reference deployment.
  **(A)** a new [`doctrine/doc-governance.md`](doctrine/doc-governance.md)
  names the three-bucket routing rule for the two governing-layer docs
  (build + operate-safely -> `AGENTS.md`; deliberation/decision process ->
  `agent_collaboration.md`), with a one-canonical-home / thin-pointer rule
  and a conciseness constraint on `AGENTS.md`'s operational-safety
  minimum. **(B)** the Internal Reviewer gains post-review
  **decision-support** ([`doctrine/roles.md`](doctrine/roles.md)), and the
  `AGENTS.md` template gains a **Decision-commit scribing guard-rail** --
  verbatim authorization, unambiguous-instruction-or-confirm, Decision-only
  commit ([`doctrine/lifecycle.md`](doctrine/lifecycle.md) cross-links it).
  **(C)** the deployment-side improvement channel is now formalized:
  [`doctrine/fold-back.md`](doctrine/fold-back.md) specifies the fold-back
  ledger mechanism, a default-on `fold-back-ledger` module ships a forkable
  ledger (carrying a `[SECURITY WARNING]` export-safety header) into
  `dev/.cairn/`, and the goodnight routine gains a foldback-capture step.
  Deliberated adopter-side; archived plan `cairn-foldback-ledger-candidates`.
- **Module upgrade -- a token- + slot-aware 3-way merge so adopters fold
  in new doctrine without losing local customizations
  (cairn-module-upgrade-3way-merge, 2026-05-27).** Cairn installs are no
  longer one-directional: a customized adopter tree can now pull new Cairn
  doctrine forward with a **non-clobbering** merge. The install writes two
  tracked artifacts -- a visible machine lockfile
  [`dev/cairn-lock.yml`](bootstrap/UPGRADE.md) (the upgrade ancestor +
  install-side provenance: version/commit, profile, per-file
  source/hash/token-values) and a scoped base-template cache
  (`dev/.cairn/base/`, raw templates for the mergeable `.md` only, so the
  merge needs no Cairn git history under any distribution mode). A new
  `scaffold.py upgrade` subcommand then offers `--plan` (read-only drift
  inventory), `--stage` (a reviewable staged merge), and `--apply` (swap,
  under a safety contract). The merge is **slot-aware** (your filled
  `cairn:slot` bodies are transplanted so they never conflict and are
  never clobbered), **token-aware** (the base re-substitutes recorded
  token values; new upstream tokens surface as "needs a value"), and emits
  standard conflict markers for genuine local-vs-upstream collisions -- it
  never auto-resolves. Verbatim reference scripts use a hash policy (update
  if unmodified; flag, never clobber, if forked). `--apply` advances the
  lockfile only for a resolved, marker-free tree; `--init-lock` migrates a
  pre-lockfile tree (token-substituted files become review-only since the
  original substituted values were never recorded). New: `bootstrap/UPGRADE.md`;
  `SAFETY.md` Rule 9 (no secret-bearing substitution tokens); the lockfile
  is the one-way machine authority the fidelity manifest cites. Source: the
  modflow_tools-hosted `cairn-module-upgrade-3way-merge` arc.
- **Fold-back: remaining ledger doctrine + goodnight roadmap-hygiene +
  doc-drift tooling (cairn-v0.2-foldback-remaining-ledger, 2026-05-27).**
  The last open fold-back candidates from Cairn's reference
  implementation, synced before the v0.2.0 cut:
  * **(A) Why the substrate earns adoption — signal-now, benefit-later.**
    [`doctrine/coordination.md`](doctrine/coordination.md) now states the
    general **asymmetric-reward** principle: a coordination signal whose
    cost is paid now but whose benefit accrues later (often to someone
    else) decays unless the substrate repays the **signaler at signal
    time** — the work-intent `claim` conflict-check is the worked
    instance, and the pattern generalizes to any signal-now /
    benefit-later protocol.
  * **(B) verify-before-asserting: what a call *does* vs. what a thing
    *is*.** The [`claim-check`](templates/modules/default-on/claim-check.md)
    module now names the costlier class of claim — runtime behavior
    (side-effects, ordering, atomicity, argument escaping, the artifact a
    call emits) — and states plainly that the installed checker **cannot**
    verify it: a signature read confirms what a thing is, not what a call
    does, so a behavioral claim needs an empirical probe or the library's
    contract. A one-line pointer threads it from
    [`dimensions/complexity.md`](dimensions/complexity.md).
  * **(E) goodnight roadmap-hygiene sub-mechanisms.**
    [`doctrine/lifecycle.md`](doctrine/lifecycle.md) gains an **archive
    precondition** (every deferred follow-up has a durable home outside
    the archived file; the migration record lives in a durable, auditable
    location per the team's workflow — commit body, PR description, or
    plan metadata) and **removal preconditions** (the three gates a
    roadmap item clears before deletion). The
    [`PLANNING.md`](templates/core/dev/PLANNING.md) template ports a
    Cairn-portable **Status taxonomy** + the archive / removal
    preconditions + a **date-marker convention** (`(Mon YYYY)`), and
    [`doctrine/session-routines.md`](doctrine/session-routines.md) gains
    the goodnight **staleness sweep** (adopter-tunable windows; sweep
    cross-cutting backlogs nightly; file-readable via the date markers).
  * **(C) broad work-intents, Tier-2-gated.** A `claim` is now
    **required before every nontrivial edit** (not only on
    coordination-surface files) — the *Tier-2-enabled* posture, gated to
    concurrency. The coordination-surface subset additionally requires
    the `list` read; a solo / sequential team keeps the courtesy framing;
    and even required, the claim stays a **courtesy signal, not a lock**.
    The obligation lands in
    [`doctrine/coordination.md`](doctrine/coordination.md) and the
    team-gated
    [`coordination-tiers`](templates/modules/team-gated/coordination-tiers.md)
    module — **not** the always-on
    [`agent_collaboration.md`](templates/core/dev/agent_collaboration.md)
    baseline (Internal I1 / External R1), which keeps only the narrow
    required-signal-read pointer. A generated-output regression
    (`bootstrap/tests/test_coordination_broad_intent.py`) pins the
    boundary: the broad obligation is absent from a minimal install and
    present in a coordination-tiers install.
  * **(D) doc-drift-prevention flips from doctrine-only to doctrine +
    stack-neutral tooling.** The
    [`doc-drift-prevention`](templates/modules/team-gated/doc-drift-prevention.md)
    module now scaffold-installs two stdlib-only, vendor-neutral scripts:
    [`link_check.py`](templates/modules/team-gated/link_check.py) (the
    link / anchor half — internal links and GitHub-slug anchors resolve)
    and
    [`sync_doc_snippets.py`](templates/modules/team-gated/sync_doc_snippets.py)
    (the snippet half — fenced doc blocks mirror a named source region via
    language-neutral `snippet-start:` / `snippet-end:` markers; `--check`
    is the drift gate, `--sync` rewrites only the directive-bearing doc,
    and absolute / `..`-escaping source paths are refused). The **claim
    half is composed, not duplicated** — the default-on `claim-check`
    module already ships `claim_check.py`, and
    [`scripts/check_cairn.py`](scripts/check_cairn.py) now imports the
    *shipped* `link_check.py` so Cairn runs the exact tool it hands an
    adopter (single source, the dogfood pattern). The **schema-doc
    generator is deferred** — it cannot ship stack-neutrally, so it is an
    adopter slot/hook, not a default install (External R2 / Internal I4).

- **Governance presets — the onboarding fast path
  (cairn-v0.2-p4-governance-presets, 2026-05-26).** An adopter can now pick
  a **named preset** instead of hand-deriving the module roster from the six
  axes. Three ship — `solo-greenfield`, `collaborative-team`,
  `high-rigor-legacy` — each a *named point in the six-axis dimension space*
  (not a parallel config system): the BOOTSTRAP.md I-5 gate table stays the
  single authoritative per-module rationale, and a preset is a set of axis
  scores fed into it. **Composable, not rigid**: `preset:` sets the baseline,
  then flat `modules_add:` / `modules_remove:` adjust on top (apply adds, then
  removes — **remove wins** on a conflict); an adopter overrides any of the six
  flat axis keys, and the **real team axes always win on staffability** (a
  preset never installs coordination apparatus the team can't run — an explicit
  `modules_add` of an unstaffable module installs with a surfaced warning, not a
  veto). The schema is **flat and stdlib-parseable** (no PyYAML dependency);
  `modules:` + `preset:` together is a hard error; wrong-type values and unknown
  enums / modules are friendly hard errors. `scaffold.py --summary` prints the
  resolved Act I-6 profile (preset + axes + roster + overrides + staffability
  warnings) **before** installing — the durable acceptance artifact. The I-5
  gate table also gained rows for the P3 practice modules. Slug uses US spelling
  (`high-rigor-legacy`). The v0.2 capstone; depends on P2/P3 (the settled module
  roster). Source: the modflow_tools-hosted `cairn-v0.2-p4-governance-presets`
  arc.
- **The work-intent tool, packaged for adopters
  (cairn-v0.2-p5-intents-tool, 2026-05-26).** The `coordination-tiers`
  module now ships a runnable tool, not just doctrine: selecting it
  installs [`tools/intent.py`](templates/modules/team-gated/intent.py)
  (verbatim, 1:many alongside the doctrine), a **stdlib-only** Tier-2
  work-intent CLI — `claim` (with a live conflict-check that gives the
  signaler immediate value), `list`, `release`, and a **folded-in**
  `install-hook` that writes a post-commit auto-release hook. The
  scaffold seeds `dev/intents.jsonl` into `.gitignore` (non-clobber,
  idempotent) and **prints** the hook command — hook install is
  **opt-in**, never an automatic scaffold side-effect. The generalized
  artifact carries zero modflow_tools-specific behavior: a `CAIRN_AGENT`
  override + an **adopter-extensible** harness-session registry (new
  harnesses register via `~/.cairn/agent.json`, no tool edit) + a
  per-session identity; the generated hook captures the install-time
  interpreter (no bare `python -m`); and the installer **refuses without
  modifying** a framework-managed / non-shell / non-executable existing
  hook (chain-not-clobber for a plain one). The
  [`coordination-tiers`](templates/modules/team-gated/coordination-tiers.md)
  doctrine is reconciled from the intent-*directory* model to the JSONL
  claim/release substrate the tool implements (the kernel
  [`doctrine/coordination.md`](doctrine/coordination.md) had already
  converged). Append atomicity is documented best-effort +
  filesystem-dependent (networked/overlay FS called out). Source: the
  modflow_tools-hosted `cairn-v0.2-p5-intents-tool` arc (P5 of the v0.2
  milestone), generalized from modflow_tools' `tools/intent.py`.
- **Practice-discipline modules + a maturity ladder
  (cairn-v0.2-p3-practice-modules, 2026-05-26).** Cairn now scaffolds the
  practice *around* the lifecycle, not just the lifecycle. Three new
  **team-gated** modules (doctrine, not tools — they exemplify how Cairn
  embodies a practice and signpost the craft literature, they do not
  re-teach it):
  * [`testing-discipline`](templates/modules/team-gated/testing-discipline.md)
    — the test-tier scheme (unit / contract / integration / workflow / …
    as one coherent scheme; tier-by-location not hand-label; contract
    tests pin stable schemas; negative tests prove the guards). The base
    discipline that [`dual-language-tests`](templates/modules/team-gated/dual-language-tests.md)
    specializes for the Language axis.
  * [`doc-drift-prevention`](templates/modules/team-gated/doc-drift-prevention.md)
    — the authoring-time drift gates (reference docs generated from a
    schema source; snippets pulled from runnable examples; a drift +
    link/claim gate). Doctrine-only; the generic scaffold-installed
    tooling is a named future follow-up.
  * [`examples-gallery`](templates/modules/team-gated/examples-gallery.md)
    — the runnable-gallery discipline (catalog in lockstep; every example
    run; smallest-first; disassemble/reassemble to learn).
  * A **maturity ladder** in [`on-ramp/README.md`](on-ramp/README.md)
    keyed to the three adoption levels — a self-locate aid, not a
    scorecard. All three modules are **team-gated** (a P4 governance
    preset turns them on per profile, rather than doubling the default-on
    set); each cross-links [`docs/further-reading.md`](docs/further-reading.md)
    for the craft Cairn points at. Source: the modflow_tools-hosted
    `cairn-v0.2-p3-practice-modules` arc (P3 of the v0.2 milestone).
- **Security: the four-layer agent-instruction-supply-chain model
  (cairn-v0.2-p2-security-four-layer, 2026-05-26).** Cairn now treats its
  own templates as what they are — *agent-executed instructions with a
  downstream blast radius* — and defends them in depth. Landed in two
  internally-gated phases.
  * **Layer 1 — release provenance.** New
    [`bootstrap/PROVENANCE.md`](bootstrap/PROVENANCE.md): named releases,
    signed tags / maintainer-approved release commits, and a **derived
    install manifest** (`scaffold.py --manifest`, emitted from the
    scaffold's own mappings so it cannot drift) — with adopter guidance to
    *scaffold from releases, not branches*, backed by a tool-side
    provenance warning (`--allow-dev` to silence).
  * **`SAFETY.md` Rules 7-8** —
    [`bootstrap/SAFETY.md`](bootstrap/SAFETY.md): templates are
    agent-executed instructions (reviewed for injected/hidden/unsafe
    content **by file class**); the bootstrap profile is
    operationally-trusted input (committed + reviewed as code, never
    pulled from chat at scaffold time).
  * **Layer 4 — executable hardening.**
    [`bootstrap/scaffold.py`](bootstrap/scaffold.py) refuses to write
    through a symlink or outside the target on **every** write
    (fail-closed), plus a Cairn-dev-only Bandit gate.
  * **Layers 2/3 — content integrity.** A new
    [`content_scan.py`](templates/modules/team-gated/content_scan.py) — a **tripwire
    that forces human review, not a safety proof** — composed by
    [`scripts/check_cairn.py`](scripts/check_cairn.py) over Cairn's source
    prose (by file class) and run over scaffolded *generated* output (the
    layer that closes the profile-borne injection path a source-only scan
    misses). Reviewed hits are cleared with a local, reasoned
    `cairn-accept` marker — never whole-directory allowlists.
  * The [`security-review`](templates/modules/team-gated/security-review.md)
    module now points at these real controls and carries the
    agent-instruction-supply-chain threat-model summary. A red-team
    fixture + `bootstrap/tests` (47 → 109 across P1+P2) keep the scanner
    honest. Source: the modflow_tools-hosted
    `cairn-v0.2-p2-security-four-layer` arc (P2 of the v0.2 milestone).
- **Runnable reference scripts on the default-on path
  (cairn-v0.2-p1-reference-scripts, 2026-05-26).** The two **default-on**
  discipline modules now ship as *installable, runnable tools* instead of
  doctrine pointing at a clone-and-adapt homework assignment — the single
  largest gap between "a methodology you read" and "a methodology you
  run", and the usability spine of the v0.2 milestone.
  * **Two packaged scripts** —
    [`templates/modules/default-on/claim_check.py`](templates/modules/default-on/claim_check.py)
    (verify-before-asserting tripwire) and
    [`templates/modules/default-on/lifecycle_metrics.py`](templates/modules/default-on/lifecycle_metrics.py)
    (proposal/plan lifecycle extractor, v1 core). Both vendor-neutral and
    **standard-library only**; generalized from the modflow_tools adopter
    implementations with a `--root` override so they run against any
    Cairn-bootstrapped tree.
  * **The scaffold installs them.**
    [`bootstrap/scaffold.py`](bootstrap/scaffold.py)'s module map went
    from 1:1 to **1:many** — a module installs its `.md` doctrine *and*
    its `.py` script — and scripts are copied **verbatim** (no token
    substitution / slot scan over code). The `{{claim_check_command}}` /
    `{{metrics_command}}` tokens default to the exact install paths, so
    the doc's "run it via …" line and the file cannot desync.
  * **Cairn runs the tool it ships.**
    [`scripts/check_cairn.py`](scripts/check_cairn.py) now *composes* the
    shipped claim-path checker (importing it from the packaged script)
    and retains its own link/anchor checker — the strongest dogfood, with
    no second copy to drift.
  * **External-path allowance (folds in the `check_cairn` case-study
    fix).** The claim-checker gains a file-scoped `--external-allow GLOB`:
    files that *describe* an external repo (`case-studies/*.md`) have
    their path-claims exempted from local resolution, generalizing the
    per-collision hand-patches that were applied as Cairn's top-level dir
    set grew.
  * Module docs rewritten to point at what ships
    ([`templates/modules/default-on/claim-check.md`](templates/modules/default-on/claim-check.md),
    [`templates/modules/default-on/lifecycle-metrics.md`](templates/modules/default-on/lifecycle-metrics.md));
    `bootstrap/tests` grew an install / generalization-gate / external-
    path / stdlib-only / VCS-robustness suite (47 → 61 passing). Source:
    the modflow_tools-hosted `cairn-v0.2-p1-reference-scripts` arc (P1 of
    the v0.2 milestone).
- **Self-application + adopter-orientation docs
  (cairn-self-application-and-docs, 2026-05-22).** Cairn now passes
  its own gate and orients a cold adopter.
  * **A self-check** — [`scripts/check_cairn.py`](scripts/check_cairn.py):
    a link + claim-path integrity gate over Cairn's own Markdown tree
    (GitHub slug rules; ported from the modflow_tools `claim-check`
    discipline). Cairn now runs the discipline it preaches; the
    baseline is clean and the checker is wired to fail on a future
    broken link/path.
  * **An adopter-orientation `docs/` layer** —
    [`docs/workflow-role.md`](docs/workflow-role.md) (where Cairn sits
    and what it does *not* do),
    [`docs/getting-started.md`](docs/getting-started.md) (one change
    traced through the lifecycle), and
    [`docs/further-reading.md`](docs/further-reading.md) (a curated
    signpost to the SE-craft literature Cairn relies on but does not
    re-teach).
  * **A minimal worked example** —
    [`examples/minimal/`](examples/minimal/): the whole lifecycle loop
    at the smallest scale, complementing the two full case studies.
  * Cross-linked from [`README.md`](README.md) and
    [`on-ramp/README.md`](on-ramp/README.md). Source: the
    modflow_tools-hosted `cairn-self-application-and-docs` arc.
- **Fidelity-gaps sync (cairn-fidelity-gaps, 2026-05-22).** Eleven
  generalizable mechanisms ported into Cairn ahead of its first use
  as the LHM bootstrap substrate — two governance landings from the
  `modflow_tools` adopter, nine from the LHM bootstrap proposal —
  each grounded by an evidence ledger in the case studies
  ([`case-studies/modflow_tools.md`](case-studies/modflow_tools.md)
  > "Governance-doctrine sync 2026-05-22"; and
  [`case-studies/lhm.md`](case-studies/lhm.md) > "Fidelity-gaps sync
  2026-05-22").

  * [`doctrine/rationale.md`](doctrine/rationale.md) > "How the
    doctrine evolves under evidence" + a goodnight-synthesis line in
    [`doctrine/session-routines.md`](doctrine/session-routines.md) —
    the **adaptive-doctrine rate-limit gate** (no doctrine change
    from a single incident unless high-risk; else recurrence or
    routine-boundary synthesis).
  * [`templates/modules/default-on/lifecycle-metrics.md`](templates/modules/default-on/lifecycle-metrics.md)
    > "The Measurement Compact" — five commitments + two-tier
    enforcement, with **doctrine decoupled from enforcement** (the
    optional wording gate parameterizes its banned-token list; no
    hardcoded identities).
  * [`templates/modules/team-gated/legacy-agent.md`](templates/modules/team-gated/legacy-agent.md)
    — "Ready" redefined for legacy scientific code + a per-surface
    **readiness schema**; the readiness map named a
    shared-communication surface with collision semantics; a
    single-file-registry concurrency warning.
  * [`doctrine/dual-review.md`](doctrine/dual-review.md) >
    "Restricted verification surfaces" — review is weaker when the
    reviewer cannot **execute** a surface (any asymmetrical
    execution environment, not just a second language);
    verification command + human-gated owner + pre-framework
    fallback. The multi-language case in
    [`templates/modules/team-gated/dual-language-tests.md`](templates/modules/team-gated/dual-language-tests.md)
    is one instance.
  * [`templates/modules/team-gated/domain-agents.md`](templates/modules/team-gated/domain-agents.md)
    — the **Cross-Domain Proposal** pattern (lead + co-author Domain
    Agents) and an **ownership-ledger** seed + partition-by-function.
  * NEW [`templates/modules/team-gated/security-review.md`](templates/modules/team-gated/security-review.md)
    (trust-boundary-first gate; tool-neutral checklist) and NEW
    [`templates/modules/team-gated/issue-capture.md`](templates/modules/team-gated/issue-capture.md)
    (tracker-agnostic capture surface) — both wired into
    `bootstrap/scaffold.py`'s module registry with scaffold tests
    (42 → 47 passing) and module-selection signals in the phase-0
    profiles.
  * [`bootstrap/BOOTSTRAP.md`](bootstrap/BOOTSTRAP.md) — a
    **plan-migration ledger** and **two-phase de-risking**, both
    legacy / existing-docs-conditional with a greenfield bypass.
  * [`templates/core/dev/proposals/_template.md`](templates/core/dev/proposals/_template.md)
    — a doctrine-change rate-limit checklist prompt (operationalizes
    the gate; explicitly does not re-apply to doctrine *syncs*).

  Codex External Review gated the framing matrix before the doctrine
  edits (Gate A; four findings absorbed — the load-bearing one
  reframed Restricted Verification Surfaces off the language axis).
  The full plan, the Gate-A review record, and per-chunk source
  provenance live in the modflow_tools-side accepted proposal
  `2026-05-22-claude-cairn-fidelity-gaps` and its executing plan
  `cairn-fidelity-gaps`.

- **Per-session coordination identity (ported from the
  `modflow_tools` adopter, 2026-05-21).**  New cross-tier section
  [`doctrine/coordination.md`](doctrine/coordination.md) >
  "Coordination identity — per-session, not per-agent": a
  coordination mechanism that records who holds a path must derive
  identity **per-session** (from the harness session id), not
  per-tool, or concurrent same-tool sessions collapse to one
  identity and one session's auto-release closes another's claims.
  Portable rules: derive from the harness session id; hash the
  *whole* id (time-ordered UUIDv7 ids share leading bytes); treat
  a global identity override as an escape hatch, not a setting;
  auto-release closes only the committing session's own claims
  (fail-soft on resolution failure).  Companion "Substrate
  convergence" note: Tier 2 and Tier 3 can share one append-only
  claim/release log.  Module extension in
  [`templates/modules/team-gated/coordination-tiers.md`](templates/modules/team-gated/coordination-tiers.md)
  > "Extension — Per-session identity for the claim/release log";
  adopter grounding (the JSONL substrate + the three harness
  session-id env vars `CLAUDE_CODE_SESSION_ID` / `CODEX_THREAD_ID`
  / `ANTIGRAVITY_TRAJECTORY_ID`, each supplied by that harness's
  own reviewer) in
  [`case-studies/modflow_tools.md`](case-studies/modflow_tools.md).
  Source: the adopter's accepted + reviewed
  `2026-05-21-claude-per-session-intent-identity` proposal (Codex
  + Antigravity reviewed), itself a follow-on to the JSONL
  work-intent substrate refresh.

## 0.1.1 — 2026-05-21

### Added

- **Doctrine sync 2026-05-19 → 2026-05-21 (cairn-doctrine-sync-may-19-21).**
  Nine doctrine landings ported from the `modflow_tools` adopter
  through a single multi-chunk plan; each Cairn-doctrine surface
  is grounded by the F9 evidence ledger in
  [`case-studies/modflow_tools.md`](case-studies/modflow_tools.md)
  > "Doctrine-sync 2026-05-19 → 2026-05-21 (F9 evidence ledger)".

  * [`doctrine/coordination.md`](doctrine/coordination.md) >
    Tier 2 — extended with a required-signal-read mode for the
    adopter-identified subset of coordination-surface files
    (handoff notes, planning indices, collaboration norms,
    change logs). The baseline courtesy framing is preserved for
    incidental shared files; the required mode applies to the
    adopter-named subset only.
  * [`templates/modules/team-gated/coordination-tiers.md`](templates/modules/team-gated/coordination-tiers.md)
    — two extensions added inside the existing module:
    a tracked **collision log** with a narrow event definition
    (three event kinds; only `true-staged-index` counts against
    the rolling-window trigger) and a **goodnight intent-hygiene**
    step (prune-intents + migrate-collisions, run once per
    session-day by the full-handoff owner).
  * [`doctrine/session-routines.md`](doctrine/session-routines.md)
    > Goodnight — new sub-section on the next-session starting
    plan: **rewrite-from-scratch each goodnight**, with
    durable-claim migration upstream of the rewrite.
  * [`doctrine/dual-review.md`](doctrine/dual-review.md) — new
    section naming the **Decision-support Round-2 review**
    pattern (three structural properties + bounding rules).
  * [`doctrine/lifecycle.md`](doctrine/lifecycle.md) — three
    new sections: **procedural-gap inline Decisions** (three-
    criterion gate); **deferred-follow-up revival** (deferred
    items re-enter the proposal lifecycle when revived);
    **the roadmap is a current-state index, not a historical
    log** (completed work migrates out of the roadmap into the
    durable record).
  * [`doctrine/roles.md`](doctrine/roles.md) — new section on
    the **capability-floor invariant** (each role has a minimum
    capability floor jointly determined by role and risk;
    adopter-local tier labels; default high/medium/low mapping).
  * NEW [`templates/modules/team-gated/model-selection.md`](templates/modules/team-gated/model-selection.md)
    module — conditionally installed at the moderate-or-complex
    end of the Complexity axis. Includes tier-by-role default
    mapping table + override discipline; adopter-local tier-to-
    model mappings live in case studies (the doctrine names the
    invariant; the case study identifies the models).
  * [`templates/core/dev/PLANNING.md`](templates/core/dev/PLANNING.md),
    [`templates/core/dev/NEXT_SESSION.md`](templates/core/dev/NEXT_SESSION.md),
    [`templates/core/dev/agent_collaboration.md`](templates/core/dev/agent_collaboration.md)
    updated to cross-reference the new doctrine and to align
    with the roadmap-no-history posture (PLANNING.md drops the
    "Completed recently" section) and the rewrite-from-scratch
    rule (NEXT_SESSION.md gains explicit rewrite language).
  * [`case-studies/modflow_tools.md`](case-studies/modflow_tools.md)
    — extended with the F9 evidence ledger linking each
    Cairn-doctrine surface to the adopter incident, file, and
    commit that grounded it, plus the modflow_tools tier-to-
    model mapping for the model-selection module.

  External Review (Antigravity / Gemini 2.5 Pro) of the
  abstraction drafts (Chunks 1 + 2) was absorbed via a single
  Sharpening commit. Three findings: vendor-neutrality
  violation in a draft (P1, fixed); module-directory taxonomy
  alignment — the new module goes under `team-gated/` per
  Cairn's catch-all convention, not a new `dimension-gated/`
  subdirectory (P2, fixed); typo/hedge cleanup (P3, fixed).
  The corrections preserved all structural-property abstractions
  intact.

  The full plan, including the External Review record and the
  per-chunk source-commit provenance, lives in the
  modflow_tools-side accepted proposal
  `2026-05-21-claude-cairn-doctrine-sync-may-19-21` and its
  executing plan `cairn-doctrine-sync-may-19-21` (under
  `modflow_tools/dev/plans/`, archiving after Chunk 11
  lasting-truth migration).

## 0.1.0 — 2026-05-20

Initial public release. See the launch commit (`4afcba8`),
which finalized README, CITATION, and licenses for v0.1.0.
