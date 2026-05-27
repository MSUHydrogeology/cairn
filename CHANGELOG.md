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
    [`scripts/content_scan.py`](scripts/content_scan.py) — a **tripwire
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
