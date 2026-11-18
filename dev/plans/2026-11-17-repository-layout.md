# Plan: Repository layout and self-adoption

**Source proposal**: dev/proposals/archive/2026-11-09-claude-repository-layout.md
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-17
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/development-environment.md
**In brief**: Put Cairn's installation, tests, release work and installed tools in clear homes while preserving adopters' changes.

## Build summary

Move Cairn's source and installed tools to the accepted homes, using its own upgrade for the installed copies. Preserve local work and the existing chain of trust during the move. The result includes the layout checks, updated guidance, and a reviewed candidate for the Maintainer's separate re-anchor; it does not claim that operation has passed.

## Source proposal

The accepted repository-layout proposal specifies twelve outcomes, destination migration and self-lock reconciliation, historical-source compatibility, and a verified old-to-new trust transition. Its Decision amendment removes the need for a Claude Code wrapper while retaining a fallback and root skills.

## Scope

Apply the proposal's items 1–12, including the root `.gitattributes` exception, root governing files and `.agents/skills/` and `.claude/skills/`. Preserve the installed method background from `templates/core/dev/method-background.md`, the scientific-testing module and the rules-folder offer. Keep `dev/architecture_review.md` and `dev/ceremony-record.md`: the proposal authorizes no move for either. Do not ship the separately queued `token_budget` and `verify_counts` additions here.

Move `bootstrap/tests/` to `tests/`, `bootstrap/` to `install/`, pre-install phase-0 and readiness inputs to `install/`, root `dimensions/` and `on-ramp/` to `install/`, onboarding guides into `templates/`, and `case-studies/` into `docs/case-studies/`. Move the two baseline and re-anchor runbooks, `reanchor.sh`, launcher and values templates from `bootstrap/`, and `repin.py`, `reanchor_ceremony.py`, `check_release_publication.py` and `check_release_test_members.py` from `scripts/` to `release/`. Place remaining Cairn-only scripts in `tests/`, keeping `audit_report.py` beside `gauge.py`; migrate the installed tools from `tools/` and `scripts/` to flat `dev/tools/` through upgrade. Move associated manifests and configuration alongside their readers. Machine-assisted path rewrites must be surgical: inspect each functional-prose patch, retain its duties and do not rewrap it.

**Reuse.** Extend the installer catalog, upgrade staging and historical reads in
`bootstrap/_scaffold/{config,install,upgrade}.py` and the ceremony in
`scripts/repin.py`. The self-hosted tool directory is flat at the command
level. Packages keep their internal module structure.

### Documentation / doctrine surface

Update both `AGENTS.md` files for commands, citations and `dev/` as records, state and tools; put folder roles in `docs/DOCUMENTATION_PLAN.md` and link from `README.md`. Update install guidance, module docs, skills, examples and path references in their current authoritative homes. Keep the vendor-neutrality exceptions limited to `docs/case-studies/`. Preserve the applicable rules in shipped instructions.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Discover roots and inventory source, destination and lock ownership | None | Shared test root helper; executable root fixes; reviewed mapping |
| C2 | Implement reconciliation and destination migration in upgrade | C1 | Upgrade transaction and provenance reconciliation |
| C3 | Relocate sources and update references | C1–C2 | New layout, compatibility entry and wrapper guidance |
| C4 | Reconcile Cairn's existing lock, run real self-upgrade and exercise the layout transition | C2–C3 | Self-adopted tools and verified candidate chain |
| C5 | Verify promises and close records | C1–C4 | Focused evidence, reviews and issue closure |

### Upgrade transaction

Extend `upgrade --plan` and `--stage` for catalogued moves. A reconciliation-only
`--stage --reconcile-layout REV` compares Cairn's existing lock and unlisted
copies with a named Cairn source revision. Reuse fork-record generation and
the lock-last cache writer. Proven rendered ancestors require actual source
or cache evidence and the original rendering inputs. A verified comparison
revision can identify a fork, with historical ancestry still marked unknown
where unproved. An absent base blocks a move that requires it. Apply the
reconciliation before staging Cairn's moves. At v0.7.0, `tools/code_map.py`
and `templates/modules/team-gated/code_map.py` have the current installed
blob. Restore its architecture-review ownership in Cairn's self-profile.

Stage one transaction under the existing upgrade staging directory ahead of
ordinary in-place updates. The durable receipt hashes the target identity,
source revisions, mapped actions and modes, old/new lock and profile bytes,
cache identities, and input/output bytes or their digests. Record keep, copy,
fork and clean merge actions. Keep an unfinished receipt across restaging.
`upgrade --apply --migration-receipt SHA256` takes the literal reported at stage
time, as collision adoption takes observed digests. Before writing, rederive
ownership and upstream provenance from the running installer's catalog and
trusted source. Compare the receipt and live files, locks, profile and caches.
An adopter-controlled stage or lock cannot supply a removal path or authorize
replacement. Keep the existing edit and containment guards, including for
retirement.

With the old lock live, publish and flush destinations and new caches without
clobbering. Replace the matched profile if needed, then atomically replace
the lock last. Keep referenced caches intact. With the new lock live, recheck
destinations, profile, caches and old path identities and bytes, then retire
only verified mapped old copies. On retry, accept an exact already-written
output or a pending output under the old lock. Only the exact new profile
matches the new lock. An absent old path counts only with the new lock and
matching destination. Keep the receipt until retirement finishes. Other
states refuse and name the path.

### Layout transition

The old signed anchor P supplies its manifest, signer roster, and verifier and
scanner closure at the old paths. Reuse prior-verifier extraction and signature
checks with the independently known fingerprint. The old scan command
requires C's roster at the old path. Invoke P's raw-object line scan with
P's verified roster and carry its decision classes to the relocated paths
through C1's mapping. Check C's mapped protected roster against that same
membership. Run P's unchanged static verifier on exact C before candidate
imports and preserve the scan digest and verifier HOLDs. The old launcher
fixes its artifact path and member list, so add a layout mode to the existing
transition.
The independent reader binds P, C and its tree, the standalone repin bootstrap,
launcher, packet and exact old/new path, mode, digest and import-name lists,
including both rosters and the artifact. Bind Python's resolved path and
digest to P's signed minor. Check the externally held bootstrap digest before
launching it in isolation. Its standard-library startup rechecks the binding
and all raw members before it loads any candidate helper or starts the artifact.
Reuse existing reader records, stage checks including E7, and fresh stage-two
extraction. Compare the stage report to P's bound scan digest.

The prior full verifier's collector hardcodes the old test directory and
plugin. Use its existing observer seam for a reviewed adapter limited to the
fixed relocated collection route. Capture actual C node and skip/xfail IDs,
translate file prefixes by C1's reviewed one-to-one map for P's comparisons,
and surface missing or ambiguous protected IDs. Leave P's verifier bytes,
static HOLDs and disposition rules intact. Exercise the transition through
collection in a disposable fixture with a test prior key and an unsigned
candidate. The real release verifier still requires the Maintainer's key-away
confirmation. Carry its bound report and existing HOLD handling into the
separate cut. A failed authority check stops and names the exact mismatch
for Maintainer disposition under the existing transition.

## Acceptance criteria

**C1.** One repository marker locates the test root. Installed commands and
configurations, including `content_scan_runner.py`, resolve their project
through misleading nested roots. Commit the revision-aware catalog of old
and new installer sources and destinations, source moves, selected modules
and unlisted self-hosted copies. Use exact Cairn revisions and regular blobs
for historical lookup. Assign one owner per destination. Inventory all lock
destinations, including `AGENTS.md`, `RULES.md`, `VENDOR.md` or its existing
wrapper alias, `.gitattributes`, `.agents/skills/`, `.claude/skills/`,
`CHANGELOG.md`, `NOTICE.md`, `docs/DOCUMENTATION_PLAN.md` and any other
selected exceptions. Record elapsed and tokens for each step, or `unknown`.

**C2.** Move verified bytes, preserve executable modifications as marked
forks, and merge prose against verified ancestors. Track installed and
upstream hashes separately and migrate cache references. Report unproved
ancestry and any old path requiring reconciliation. Keep those bytes and
withhold migration completion. Occupied, conflicting, linked or non-file
paths refuse without overwrite or traversal. Retain unrelated project files
under the old tool directories. Exercise interruption before and after
lock replacement, a changed input, and a tampered receipt. Write E resolves
the onboarding source for each revision separately and preserves existing
onboarding copies.

**C3.** The layout check proves the installer reads exactly the
`templates/` files, owns every `dev/tools/` file and leaves no Cairn root
`scripts/` or `tools/`. Inspect the lock exceptions and a test archive
excluding `dev/`. Hooks, imports, configuration, hashes and manifests follow
moves. Keep shipped twins byte-identical and module behavior intact.
`cairn/…` means Cairn source. Repair bare `bootstrap/` citations.
`bootstrap/scaffold.py` reports the new command until v1.0.

Keep `VENDOR.md` for other tools. Move wrapper duties to vendor-neutral
`AGENTS.md` and document the uncommitted `CLAUDE.md` fallback containing
`@AGENTS.md`. For an existing recorded or resolved wrapper, bypass merging
and replacement creation. Keep its path, bytes and base, using scoped
finalization for installed hash updates. Verify a customized alias by upgrade
and integrity checks. Remove Cairn's wrapper only after a fresh desktop session
demonstrates an instruction unique to `AGENTS.md` in a disposable wrapper-free
copy. If unavailable or unsuccessful, retain it and record the limit.

**C4.** Cairn's real upgrade uses C2, preserves adaptations and leaves no
competing commands. Use the layout transition above to bind the exact
relocated candidate to the old authority and interpreter. Refuse substituted
helpers, unauthorized candidate bytes and wrong interpreters before import.
Keep the Maintainer's exact authorization, real collection and re-anchor in a
separate linked board wait. The anchor remains unpassed until performed.
Plan archive attests to the reviewed machinery and unsigned exercise.
Activation and release require the signed cut.

**C5.** Run the checks below on the final relevant bytes; remedy failures before code review and archive. Close #67 when the destination inventory and root exceptions establish its promise. Close #90 only if its full issue scope is satisfied; the broader helper standard remains queued. Close a satisfied issue at its fixing commit, not release. Record limitations, review dispositions, changed-file burden and benefit versus cost.

## Scope delta

**Scope delta**: preserved

Proposed paths:
- `dev/tools/`
- `docs/case-studies/`

## Verification

Use the canonical Python and the reviewed range for governing text. Use
`python tools/test_tiers.py for <changed paths>` to identify checks for
changed behavior. Reserve wider checks for changed public promises and
required certification.
Run the claim, link, snippet and neutrality prose gates. Exercise the named
promises through fresh install, v0.7 migration, real self-upgrade and the
disposable ceremony. Include one failing mutation for each layout rule.
The layout check joins certification. Test a negative search against a
known positive. Keep external-promise tests and protected guards.

Run scaffold summary and dry-run, both example self-tests, prose gates at their new paths, and test-install link checking. In the separate authorized certification operation compare clean before/after pass, skip and node counts; counts alone establish neither behavior nor authority. Keep those results unpassed until the Maintainer runs it. The arc owner runs one joined integration selection at arc end, not a suite per chunk. Record covered bytes, inputs, platform, omissions and results. Scientific independent check: N/A, as in the proposal. Obtain fresh ordinary and Security code reviews; a review names what it did not cover. Unexpected drift, missing evidence or failed checks remain implementation work.

## Plan review -- Terra -- 2026-11-17

Reviewed commit: 0622d1ec5ce28c450755c9992403578c8e54cc92

**Obligation**: Internal plan review
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown. **Tokens**: unknown.

A coherent footprint exercised through the actual upgrade can simplify adoption while preserving local work and trust.

**Foundations**

1. **Should this happen as framed?** The Decision supports it, but C2 and C4 leave design decisions to the low-tier executor. -- Plan C2/C4; `dev/agent_collaboration.md`, Review rules.
2. **Best alternative.** Extend the existing staging and anchored loader, with a reviewed recovery protocol and transition design. -- `bootstrap/_scaffold/upgrade.py:1362`; `scripts/repin.py:635`.
3. **What would show it wrong?** An interrupted upgrade loses the only copy or relocated authority executes before verification. -- Proposal, Evidence / verification plan.

1. **Blocking: specify the migration and trust-transition designs.** C2 states safety outcomes but does not say how durable transaction progress, retry decisions and source-to-destination ownership are represented and ordered. Existing staging and recovery metadata do not specify that move protocol (`upgrade.py:1416`, `:1638`). C4 requires old authority to verify new paths but does not define how the old verifier accepts the new roster before import; the current loader freezes exact paths and module names (`scripts/repin.py:66`, `:635`). Provide concise designs identifying the authoritative records, state transitions and verification/authorization order, grounded in the existing mechanisms, so execution does not invent them.
2. **Blocking: resolve wrapper inventory conflict.** C1 omits renamed wrappers from root exceptions while C3 requires every lock destination to use an exception and also preserves adopter wrappers. Upgrade can record `CLAUDE.md` as the actual destination (`bootstrap/_scaffold/upgrade.py:3918`). Permit existing renamed project wrappers in the inventory and verify a customized wrapper survives upgrade with valid provenance; retain unrelated project-owned root tool files as the proposal requires.

**Audience and rule loss:** The intended audience can follow the summary; the plan requires duties to remain in installed instructions. Actual rewritten prose was unavailable.

**Coverage:** Read the committed plan, accepted proposal and amendment, template, rules, installer and anchored-loader excerpts; repeated the reuse search and searched wrapper resolution. Opening: 1,388 words; C3 exceeds the 150-word target. No implementation tests, full mapping inventory, migration, desktop check or Security Review were run.

## Plan review -- Sol -- 2026-11-17

Reviewed commit: 0622d1ec5ce28c450755c9992403578c8e54cc92

**Obligation**: Internal Security Review of migration, trust transition and wrapper preservation
**Tier**: Internal Security Review
**Model basis**: GPT-6.2 Sol, High
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: reading approximately three minutes; recording and checks unknown.
**Tokens**: unknown.

The real self-upgrade can demonstrate the same data-preserving move adopters use.

**Foundations**

1. **Should this happen as framed?** Yes, once C2 and C4 specify the mechanisms their criteria assume. -- `bootstrap/_scaffold/upgrade.py:1382`, `scripts/repin.py:2208`.
2. **Best alternative.** Extend staged upgrade and the maintained ceremony with independently checked transition inputs. -- `bootstrap/_scaffold/upgrade.py:1356`, `bootstrap/REANCHOR_RUNBOOK.md:84`.
3. **What would show it wrong?** Interrupt after a destination write and retry, or substitute a relocated authority member and observe an import before refusal. -- Proposal verification.

1. **Blocking, C2:** Staging deletes prior state and apply commits the lock after writing files. Specify durable phases, restaging and retries against independently derived mapping, live digests and lock/cache identities. Files or stage records controlled by a project checkout must confer no removal authority. Specify how the existing lock is reconciled, including unlisted copies such as `tools/code_map.py`; init-lock returns when a lock exists. -- `bootstrap/_scaffold/upgrade.py:1382`, `:1868`, `:3981`.
2. **Blocking, C4:** The anchor launcher requires the old member set and artifact path. Prior full collection also requires a human confirmation and calls the old test path. Specify which authenticated old checks run, how an independently reviewed exact new closure and interpreter bind before candidate imports, and where a disposable unsigned exercise ends before the separate Maintainer operation. -- `bootstrap/reanchor-launcher.template.sh:450`, `bootstrap/tests/_gate_manifest.py:513`, `scripts/repin.py:1939`.
3. **Blocking, C3:** The upgrade resolves and can merge a renamed `CLAUDE.md`. Specify byte-preserving treatment of recorded or resolved existing wrappers and check their lock/integrity behavior. -- `bootstrap/_scaffold/upgrade.py:823`, `:3918`.

**Rule loss:** Generalize wrapper duties in shared instructions to preserve vendor neutrality under `bootstrap/SAFETY.md:107`. Rewritten prose was unavailable.

**Coverage:** Read the proposal and amendment, plan and relevant engine and
ceremony paths. No implementation tests, migration, desktop or ceremony run.

## Plan response -- Sol -- 2026-11-17

**Role/model**: Strategy and revising plan author, GPT-6.2 Sol, High.
**Disposition**: revised for ordinary and focused Security plan review.
**Elapsed**: unknown. **Tokens**: unknown.

- **Terra 1 and Security 1.** Sequence and C1–C2 specify catalog ownership,
  reconciliation, and the receipt, lock-last publication and retry protocol.
  A project controlling its lock or stage cannot choose a path for removal
  or authorize changed bytes. The forged receipt check and interrupted move
  distinguish those cases. C2 preserves executable forks and records unknown
  ancestry. The v0.7.0 source and installed Code Map entries share blob
  `a6c597921b0ec19884201ca15706b30f1784361d`.
- **Terra 1 and Security 2.** Sequence and C4 bind the transition to P, C,
  the independently reviewed bootstrap, exact relocated closure and
  interpreter. The old raw scan needs explicit signed roster input once C
  moves its roster. P's verifier and HOLDs remain, with the reviewed
  collection adapter and a disposable unsigned exercise. Real collection
  and release authority remain in the separate Maintainer cut.
- **Terra 2 and Security 3.** C1 names wrapper aliases and the project-facing
  document exception. C2 preserves unrelated files. C3 preserves wrapper
  bytes, path and ancestry, checks integrity, and keeps shared instructions
  vendor-neutral.

**Coverage:** Read both reviews, the accepted outcomes, upgrade and lock
writers, and the signed anchor's verifier and scanner. The claim, link,
snippet and neutrality gates passed. The mapper selected zero test files.
Migration, ceremony and desktop evidence remain due. Opening: 1,831 words
before this response, over target for the two requested protocols.

## Plan review -- Terra -- 2026-11-17 (revision)

Reviewed commit: 5036c3db3e49e4ac6b31533e1fc26310ffcbc57b

**Obligation**: Internal plan review of the operative amendment
**Tier**: Internal
**Model basis**: GPT-6.1 Terra, Medium
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** The amendment specifies recovery, wrapper preservation and the authority handoff while retaining the accepted outcomes and separate human cut. -- Plan, Upgrade transaction, Layout transition and C1–C4; accepted proposal, Decision amendment.
2. **Best alternative.** Extend the existing staged upgrade and anchored verifier; the plan now defines their transition without replacing them. -- `bootstrap/_scaffold/upgrade.py` `_write_stage`; `scripts/repin.py` `load_listed`; plan, Reuse.
3. **What would show it wrong?** An interrupted retry losing a copy, or candidate code executing before authority and interpreter checks, would defeat the plan. -- Plan, C2, C4 and Verification.

**Rule loss:** C3 moves wrapper duties to shared instructions and preserves existing wrapper bytes; the rewritten instructions are not yet available to inspect.

**Coverage:** Compared the amendment with both prior reviews and the twelve accepted outcomes; read the cited staging, wrapper and loader paths. The 1,831-word opening exceeds the 1,000-word target; the added protocol addresses the prior findings. No implementation tests, migration, ceremony, desktop check, full mapping inventory or Security Review were run.

## Plan review -- Sol -- 2026-11-17 (revision)

Reviewed commit: 5036c3db3e49e4ac6b31533e1fc26310ffcbc57b

**Obligation**: Internal Security Review of the migration, wrapper and authority-transition amendments
**Tier**: Internal Security Review
**Model basis**: GPT-6.2 Sol, High
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: focused reading approximately two minutes; recording and checks unknown.
**Tokens**: unknown.

The revised design keeps a verified copy across interruptions and preserves
independent authority through the path change.

**Foundations**

1. **Should this happen as framed?** Yes. Catalog ownership, a separate reconciliation, and a receipt tied to old and new lock states make retirement conditional on verified publication. C3 keeps alias bytes and ancestry. -- Plan, Upgrade transaction and C3; `bootstrap/_scaffold/upgrade.py:2731`.
2. **Best alternative.** Keep the existing ceremony and use its prior-verifier observer seam for mapped collection. P's verified policy and an independent reader's exact bootstrap, closure and interpreter binding fix which code can start. -- Plan, Layout transition; `scripts/repin.py:85`, `:1884`.
3. **What would show it wrong?** Interrupt on either side of lock replacement, change a recorded input and retry. At the ceremony entry, substitute a relocated helper or interpreter. The design fails if the retry removes the old copy or a substitution reaches a candidate import. -- Plan, C2 and C4.

**Rule loss:** The design preserves static HOLDs and their cut disposition,
the Maintainer's key-away confirmation and signing authority, and existing
wrapper duties in vendor-neutral instructions. The unsigned exercise can
verify mechanics before archive. The real anchor remains unpassed.

**Coverage:** Focused on changes addressing the three findings in `958e31b8`.
No implementation tests, migration, desktop or ceremony runs.

## Implementation progress -- C1 -- 2026-11-17

C1 source work is committed: shared test roots (`62461f5d`, exact trailing-parent correction `33e0adeb`), scanner roots (`5d9cde98`), remaining command roots (`3cf3ac7f`), the ownership catalog (`cdfa8f4c`), and committed-history prose-tool lookup (`66c05be9`). Small public-entry and disposable relocated-layout checks passed; no mapped-family or suite rerun was made. The earlier scanner commit's literal newline escapes are formatting only.

The two standalone gate files and two `conftest.py` roots retain their pre-authentication behavior for C4's explicit transition. Relocated end-to-end Meter/network execution, lock finalization and final combined checks remain with C3–C5; C1 is not whole-tree certification.

C2 execution escalated to Sol after two Terra attempts ended at inspection without product edits or tests. The reviewed transaction and accepted scope remain unchanged. Luna is absent from the current model catalog; Terra is the available ordinary execution model. Elapsed and tokens: unknown.
