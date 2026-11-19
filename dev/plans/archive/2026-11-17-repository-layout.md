# Plan: Repository layout and self-adoption

**Source proposal**: dev/proposals/archive/2026-11-09-claude-repository-layout.md
**Status**: archived
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

Place the native release-only checker at `release/security_check.py` and
Cairn's floor and security check dependencies at `tests/requirements-dev.txt`.
Keep the contained adopter installer and its coupled checks in `install/container/`.
The accepted documentation-audience proposal owns moving the release procedure
and count-maintenance guidance. The later release-without-dev plan owns
kept-file reference guidance and checks.

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

Add exact source-file overrides for the release checker and test requirements
before the generic bootstrap prefix. Preserve their modes. Update the
checker's committed-child launch, imports, roster and closure paths, and
operator commands. Follow the requirements consumers, including contributor,
floor and security guidance, and update container consumers only where they
read the moved file. In the contained recipe, use the absolute Dockerfile
path in the source context materialized from the verified commit. The pin verifier's
dirty and untracked checks cover `install/container/Dockerfile`,
`install/scaffold.py`, `install/_scaffold/`, `templates/` and `CITATION.cff`.
Acceptance archives that set from the selected commit into each source
context `$S` and builds it with `-f "$S/install/container/Dockerfile"`.
Keep its controlled upgrade changes. The developer floor check uses
the relocated engine and entry point for its existing compatibility exercise.
Preserve the old signed anchor, its closure, HOLDs and baselines.

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
Current tests and user commands resolve the relocated modules. The container
copies and launches the relocated installer. Its pinned route verifies
the Dockerfile and its COPY inputs, with acceptance building from the
recipe extracted alongside its inputs. Installed root skills invoke the
relocated tools, preserving local edits and refreshing only their affected
lock records through scoped finalization.

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

**C5.** Run the checks below on the final relevant bytes and remedy failures
before code review and archive. Audit actual folder contents and consumers
against their purpose: adopter inputs and tools, public methodology,
development records, verification and release. Remove empty legacy folders
and obsolete generated caches. Preserve intentional runtime directories,
historical evidence and harness-owned worktrees. Close #67 only when verified
installed destinations, named root exceptions and the omit-`dev/` archive
establish its full promise. Leave kept-file reference gaps visible for the
accepted follow-on and do not close an issue that still depends on it. Close
#90 only if fully satisfied. Close a satisfied issue at its fixing commit.
Record limitations, dispositions, changed-file burden and benefit versus cost.

## Scope delta

**Scope delta**: preserved

## Verification

Use the canonical Python and the reviewed range for governing text. Use
`python tests/tier_inventory.py for <changed paths>` to identify checks for
changed behavior. Reserve wider checks for changed public promises and
required certification.
Run the claim, link, snippet and neutrality prose gates. Exercise the named
promises through fresh install, v0.7 migration, real self-upgrade and the
disposable ceremony. Include one failing mutation for each layout rule.
The layout check joins certification. Test a negative search against a
known positive. Keep external-promise tests and protected guards.

Scan current Python syntax for stale imports and distinguish historical
fixtures from live paths. Run one collection-only pass over the relocated test
tree after repairing imports. In the single joined integration selection,
verify the moved release-checker entry and committed child, contained
installer entry, and the affected installed-skill paths and lock integrity.
Extend the existing `tests/test_verify_ref.py` and acceptance probes to show
refusal for a dirty Dockerfile and dirty or untracked engine inputs, and that
a live Dockerfile substituted after extraction cannot supply the build recipe.
These focused controls can run without an OCI engine. Record the actual
contained workflow result separately, including any unavailable runtime.
Use the unsigned transition on the final bound paths. Keep unmatched prior
records and signed or native certification evidence in the separate cut.

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

## Plan change -- Codex -- 2026-11-17

**Prior reviewed commit**: 0622d1ec5ce28c450755c9992403578c8e54cc92
**Replacement commit**: 2ba9f750c93bc67354691d9f3808e5d29ee29538
**Affected cells and dependencies**: Scope, Sequence, Acceptance criteria, Verification, C1, C3, C4, C5
**Change**: Complete the folder-purpose audit, relocate the two overlooked
Cairn-only files and verify the affected paths.
**Reason**: The current native checker records and joins release evidence.
The development dependency file enables Cairn's floor and security checks.
The audit also found a container copying the old engine paths, live test
imports of removed modules, and the self-installed skills calling retired
paths. The already reviewed migration design is recorded at
5036c3db3e49e4ac6b31533e1fc26310ffcbc57b. The parent anchor, protected tests
and Maintainer cut requirements remain unchanged.
**Required obligations**: Internal + Internal Security Review

Maintainer direction, chat, 2026-11-17:

> Make sure to clean up the folders when you're done

> I would audit all folders when you're done to make sure they belong. Follow on with a plan modification if not before you archive

> Think carefully about "intended layout" to mean what the intention is, not the list--in case we forgot to include something

The unresolved Security question is whether the exact mapping and launch paths
bind the relocated release checker and cover the executable container build
surface while preserving the prior authority and its HOLDs. The two prior
passes covered the earlier mapping with neither change. The review cap
requires express Maintainer authorization before this focused pass.

Elapsed and tokens: unknown.

## Plan amendment review -- Terra -- 2026-11-17

**Prior reviewed commit**: 0622d1ec5ce28c450755c9992403578c8e54cc92
**Replacement commit**: 2ba9f750c93bc67354691d9f3808e5d29ee29538
**Affected cells and dependencies**: Scope, Sequence, Acceptance criteria, Verification, C1, C3, C4, C5
**Obligation**: Internal
**Tier**: Internal
**Model basis**: GPT-6.1 Terra, Medium
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown. **Tokens**: unknown.

A purpose-based audit can complete the coherent layout while catching live
consumers omitted from the original move list.

**Foundations**

1. **Should this happen as framed?** Yes: the audit and route checks extend the accepted folder purposes while retaining migration and authority requirements. -- Accepted proposal, Decision summary and items 1–11; plan, Scope, C3–C5 and Verification.
2. **Best alternative.** Reuse the existing catalog, container and joined integration selection; a separate audit mechanism would add upkeep without another stated outcome. -- Plan, Reuse, Sequence and Verification.
3. **What would show it wrong?** A fresh install, contained build or relocated release entry that still reads an old live path would fail the promised layout; run the specified route checks on final bytes. -- Plan, C3 and Verification.

**Rule loss and audience:** The plan retains surgical prose edits, installed
duties and existing authority checks; the actual revised guidance must still
be read for its intended agent audience. -- Plan, Scope, documentation surface
and Layout transition.

**Coverage:** Compared the committed amendment with the prior operative plan,
accepted layout outcomes and template. The template targets 1,000 opening
words, 150 per criterion chunk and 300 per review; the previously reviewed
protocol already exceeded the opening target. No implementation tests, full
folder inventory, actual rewritten guidance or Security Review were performed.

## Maintainer authorization -- 2026-11-18

Maintainer, chat reply to the focused-review request:

> Authorize the focused review

This authorizes one additional Sol plan Security Review of the amendment's
release-checker mapping and container launch protections. Its question is
whether those paths bind the intended code and executable build inputs while
preserving the prior authority and HOLDs. The earlier two passes covered the
original paths; this pass covers only the correction, without rerunning test
suites. No further pass or trust operation is authorized.

Elapsed and tokens: unknown.

## Plan amendment review -- Sol -- 2026-11-18

**Prior reviewed commit**: 0622d1ec5ce28c450755c9992403578c8e54cc92
**Replacement commit**: 2ba9f750c93bc67354691d9f3808e5d29ee29538
**Affected cells and dependencies**: Scope, Sequence, Acceptance criteria, Verification, C1, C3, C4, C5
**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Model basis**: GPT-6.2 Sol, High
**Findings**: one blocking
**Verdict**: REVISE
**Elapsed**: focused reading about three minutes, recording and checks unknown.
**Tokens**: unknown.

The checker move fits the verified layout. The contained build also needs
to bind the recipe it executes to the selected commit.

**Foundations**

1. **Should this happen as framed?** Complete the checker move with exact overrides, mapped protected membership and the committed-child launch. The container's build recipe needs an explicit binding. -- Plan, Sequence and C3–C4, `release/repin.py:1803-1886`, `install/security_check.py:1814-1833`.
2. **Best alternative.** Extend the existing committed extraction to include the Dockerfile and point the documented build at the selected checkout's verified recipe. -- `install/container/acceptance.sh:127-153`, `install/container/recipe.md:81-90`.
3. **What would show it wrong?** The joined check should show that a substituted recipe cannot determine the pinned image and that the dirty relocated engine still refuses. -- Plan, Verification, `tests/test_verify_ref.py:741-757`.

**Blocking, C3 and Verification.** The guard checks COPY sources only.
Acceptance archives those sources and builds with a separate live `-f` file.
The adopter command likewise takes a relative `-f` path. A passing source
guard can miss the actual recipe. Bind the Dockerfile used by the pinned build
to the same commit as its relocated COPY inputs. Keep tracked-dirty and
untracked refusals and extend the focused check to the actual recipe. See
`install/container/verify-ref.sh:117-135`,
`install/container/acceptance.sh:33-36`, `install/container/acceptance.sh:127-153`.

**Rule loss and audience.** The old signed verifier, its HOLDs and the
Maintainer's separate cut remain required. The adopter needs the exact
verified recipe path in the build command. -- Plan, Layout transition and C4.

**Coverage.** Maintainer authorization at `80303622` limits this pass to
the checker and executable build inputs. Earlier passes preceded both changes.
Tracing the committed consumers exposed the recipe gap. No build, tests,
ceremony, migration or review of rewritten guidance.

## Plan change -- Codex -- 2026-11-18

**Prior reviewed commit**: 2ba9f750c93bc67354691d9f3808e5d29ee29538
**Replacement commit**: 3389c79f4097dab8762d309cbad74b69ba3e13fb
**Affected cells and dependencies**: Scope, Sequence, Acceptance criteria, Verification, C1, C3, C4, C5
**Change**: Bind the Dockerfile to the same selected source as its COPY
inputs. Extend the existing refusal and recipe selection checks.
**Reason**: The focused Security Review in e9c79955 found that acceptance
archives the COPY inputs but takes a live Dockerfile, and the adopter's
relative recipe path can resolve outside the verified checkout.
**Required obligations**: Internal + Internal Security Review

The checker move, prior verifier, HOLDs and Maintainer cut retain their
requirements. This successor records the correction for disposition.

Elapsed and tokens: unknown.

## Response -- Codex -- 2026-11-18

**Disposition**: ready-to-implement

The Maintainer accepted the recipe-binding correction at
3389c79f4097dab8762d309cbad74b69ba3e13fb and closed the remaining plan-review
obligation, replying in chat:

> Implement correction; close further plan reviews

This disposes of the focused finding in e9c79955 without another plan pass.
The exact corrected build-input requirements remain operative. Independent
ordinary and Security code reviews, focused checks, accepted scope, and the
separate Maintainer trust operation remain required. Earlier reviews retain
their original verdicts and coverage.

Elapsed and tokens: unknown.

## Implementation verification -- Codex -- 2026-11-18

Implementation through `5f9d0742` delivers the catalog, receipt-bound migration,
real self-adoption, source moves, current callers and unsigned transition.
C2's transaction passed its focused checks and an earlier native Windows
retry (Python 3.13.18, 21.98 seconds); that evidence covers the unchanged
transaction, not a certification of the final relocated tree.

Python 3.13.13: the joined selection passed 30 cases in 45.66 seconds with one
runner-fixture failure. The corrected record/join workflow passed at `56eff8ac`
in 23.08 seconds; six caller checks passed in 4.50 seconds. The final catalog's
unsigned transition passed separately in 13.74 seconds. Passing unaffected
results were reused. Discovery initially found five broken readers; their
collection-only retry found 590 cases without error. No whole suite ran.

The actual Podman workflow at `56eff8ac` passed contained two-version install,
upgrade, ownership, filesystem and offline controls. A fresh installation's
installed link checker passed 25 Markdown files. Layout and 70 installed-file
hashes pass. Live links, snippets and neutrality pass; seven released-changelog
links remain historical. Earlier review citations resolve in their reviewed
commits. Empty legacy folders, 470 old bytecode caches and the container's
disposable working tree were removed; purposeful folders remain.

The non-test inventory command is `tests/tier_inventory.py`; 135 test files
remain assigned once. Protected parameter labels remain stable. The existing
wrapper stays because a fresh wrapper-free desktop trial was unavailable.

Ordinary and Security code reviews remain owed. Real signing, certification,
the inherited HOLDs and base-cache limitations stay with the named cut wait.
Issue #67 also needs the accepted release-without-dev follow-on; #90's adopter
standard and check are not delivered by Cairn's test-root helper.

**Benefit versus cost**: worth it -- one adopted tool home and preserved local
work; cost 398 changed files including moves, 6,781 added and 3,588 removed
lines over `21923511..5f9d0742`; remaining burden one ownership catalog and
layout guard, ongoing maintenance cost unknown.

Always-loaded words: Cairn 1,483 (+14), shipped kernel 1,392 (+29). Installed
hash records remain 70 plus four living-state exclusions. Revisit if the
catalog or guard creates repeated manual work. Aggregate elapsed and tokens:
unknown.

## Code review -- Terra -- 2026-11-18

Reviewed commit: 9355e4453fd55b6e3d17f0202f615a24c3c3df3e

**Tier**: Internal
**Verdict**: ACCEPT
**Findings**: none

**Foundations**:

1. **Should this happen as framed?** Yes: the accepted layout and preserved local work are supported by the real self-upgrade, contained install/upgrade and unsigned transition evidence; migration tests cover interruptions, changed inputs and reconciliation through the scaffold entry -- Implementation verification above; `tests/test_upgrade_layout_migration.py`.
2. **Best alternative.** Retain the existing upgrade and historical source machinery rather than a parallel installer: the catalog separates source moves from adopter authority and the transaction reuses upgrade staging; I found no simpler alternative delivering all accepted outcomes -- `install/_scaffold/layout_catalog.py`, `install/_scaffold/upgrade.py`.
3. **What would show it wrong?** A modified file lost on retry, a historical revision read from today's path, or a substituted candidate accepted would falsify the promise. The public migration tests and recorded unsigned transition challenge these cases; a signed cut on the exact candidate remains a forward test, not a passed result -- `tests/test_upgrade_layout_migration.py`, Implementation verification above.

**Rules and audience**: The reviewed governing changes route commands to their new homes and retain the wrapper fallback and agent duties in installed instructions; no weakening found in the inspected functional-prose changes. The unavailable wrapper-free desktop trial is expressly held, not assumed passed -- `AGENTS.md`, `templates/core/AGENTS.md`, C3 above.

**Tests and cost**: No test files were deleted in the rename-aware range. The new migration tests exercise public outcomes, including refusal and retry, rather than pinning private wording; the layout guard preserves the set-wide promise. Their continuing cost is justified by preserving adopter work -- `tests/test_upgrade_layout_migration.py`, `tests/test_scaffold_substrate.py`.

**Bounding**: ACCEPTED after challenging the migration retry and historical-source promises against those tests and the recorded results. No implementation checks were rerun; this pass did not independently certify every moved reader, the signed cut, native final-tree certification or inherited HOLDs. Separate Security Review remains owed.

**Waiting-line check**: The reached plan-review authorization and correction disposition waits appear in plan history; the re-anchor is a separate board wait. No missing reached fence or deviation wait found -- `git log -p 21923511..9355e445 -- dev/plans/2026-11-17-repository-layout.md`, `dev/PLANNING.md`.

Elapsed: unknown; tokens: unknown.

## Code Security Review -- Sol -- 2026-11-18

Reviewed commit: 9355e4453fd55b6e3d17f0202f615a24c3c3df3e

**Obligation**: Internal Security Review
**Tier**: Internal, GPT-6.2 Sol High
**Verdict**: REVISE
**Findings**: S1 blocking, S2 nonblocking.

**Foundations**

1. **Should this happen as framed?** Yes. The catalog and receipt bind ownership and old bytes, and verified publication precedes retirement. Signed prior policy and the externally checked candidate identity precede candidate imports -- `install/_scaffold/upgrade.py:4282`, `install/_scaffold/layout_migration.py:401`, `release/repin.py:2439`.
2. **Best alternative.** Use the existing archived build input method for pinned builds to bind the recipe and files to one commit -- `install/container/acceptance.sh:138`.
3. **What would show it wrong?** An input outside the pin entering the build falsifies C3. The focused probe below found that gap. Receipt tampering and relocated helper substitution are covered by the existing public tests -- `tests/test_upgrade_layout_migration.py`, `tests/test_repin_ceremony.py`.

**S1, blocking (C3).** The documented pin command returned 3 with committed
inputs and with an extra inert, Git-ignored engine file in a disposable
checkout. An unignored extra returned 1. The documented build recursively
copies the live engine directory, so its labeled commit can omit copied bytes
(`install/container/verify-ref.sh:125`, `install/container/recipe.md:86`,
`install/container/Dockerfile:62`). Use the archived input set or refuse extra
copied bytes. Close with a focused ignored-input control.

**S2, nonblocking.** The safety guide still calls retired-file removal the
engine's sole deletion route. Describe both routes and the destination/receipt
checks governing layout retirement (`install/SAFETY.md:247`).

**Rules and audience**: `dev/rules/protected-surfaces.md`,
`dev/rules/working-agreements.md`. The tested gap affects the adopter's pinned
build. The two B102 allowances cover bounded reads of the fixed, digest-pinned
Git helper.

**Tests and cost**: Retain the public refusal and retry controls and exact
protected IDs. The inherited roster HOLDs stay with the cut.

**Bounding**: WIDER RUN REQUIRED for S1's focused check only. Used committed
evidence elsewhere. No suite, image build, signing or native certification ran.

**Waiting-line check**: Reached authorization waits are in plan history.
The v0.8 re-anchor remains a separate board wait. Link this plan there at
closeout (`dev/PLANNING.md`).

**Elapsed**: unknown. **Tokens**: unknown.

## Code Security Review -- Sol -- 2026-11-18 (pass 2)

Reviewed commit: 2e35a655d5a7c94fda868dd4970e99a30401672b

**Obligation**: Internal Security Review
**Tier**: Internal, GPT-6.2 Sol High
**Verdict**: ACCEPT
**Findings**: none.

**Foundations**

1. **Should this happen as framed?** Yes. One verified full commit supplies the archive and image label. Podman takes both inputs and recipe from the extracted tree. The existing pin guard is unchanged -- `install/container/recipe.md:89`, `install/container/verify-ref.sh:125`.
2. **Best alternative.** Reusing the acceptance archive pattern meets the exact-source requirement without adding an installer command or a release step -- `install/container/acceptance.sh:138`.
3. **What would show it wrong?** A local file reaching the builder or a builder starting after failed extraction would falsify the fix. The author's public check passed once in 0.69 seconds on Python 3.13.13, observing archived recipe and engine bytes and exclusion of the ignored file at the Podman command. The shell's success chain gates Podman on both archive and extraction -- `tests/test_verify_ref.py:1126`, `install/container/recipe.md:93`.

**Rules and audience**: `dev/rules/protected-surfaces.md`,
`dev/rules/working-agreements.md`. The adopter follows the existing pin
checks. The safety guide now describes both guarded removal routes
(`install/SAFETY.md:272`).

**Tests and cost**: One public build-boundary check and no removed tests.
It executes the guide's commands and measures the build inputs.

**Bounding**: ACCEPTED for the new executable guide and safety correction.
The first pass predated this program. This pass inspected failure handling
and used the recorded focused run. No additional build, signing or native
certification ran.

**Waiting-line check**: The plan now links from the existing cut wait.
No fence became due in this correction -- `dev/PLANNING.md`.

**Elapsed**: unknown. **Tokens**: unknown.

## Response -- Codex -- 2026-11-18 (code findings)

S1 is fixed by the guide's verified-commit archive program (`3b95348b`), not
an added pin exception. Its public ignored-input check passed on Python
3.13.13 in 0.69 seconds. S2 is fixed by the separate descriptions of retired
file removal and verified layout retirement (`2e35a655`). The C3 wording still
requires the same commit-bound inputs. The focused second Security Review
accepted both corrections (`609e56be`); no clearing suite ran. The original
ordinary acceptance remains applicable to its unchanged implementation.

Elapsed and tokens: unknown.

## Implementation closeout -- Codex -- 2026-11-18

C1–C5 hold: tested roots and ownership mapping; receipt-bound, preserving
migration; purpose-correct source and tool homes; actual self-adoption and
unsigned transition; reviewed checks, current guidance and folder cleanup.
Both code-review obligations accept. All cheap findings were fixed. No plan
folder or review sidecar was created; historical evidence and harness
worktrees were preserved.

- Not run: real signed baseline operation and final native certification.
  Home: the grouped v0.8 cut wait in `dev/PLANNING.md`.
- Not covered: wrapper-free desktop trial. The existing wrapper is retained.
  Home: the accepted C3 conditional fence; no removal is claimed.
- Not covered: original ancestry for 31 slot bases and the inherited base
  mismatch. Current installed bytes pass; history was not fabricated.
  Home: accepted reconciliation limits in C2/C4. No historical repair is queued.
- Remaining: kept-file release references and the wider adopter root standard.
  Home: the accepted release-without-dev proposal and the existing conditional
  issue #90 queue in `dev/PLANNING.md`. These are not missing layout scope.

Dispositions: accept all code findings and folder repairs; guard layout
invariants with the existing five-case public check, and pinned build inputs
with the public archive checks. No accepted scope or required check deferred.

The earlier benefit/cost record covers the measured implementation; later
changes add the reviewed build program and its subsecond guard without new
tools, always-loaded text or installed files. Revisit on repeated catalog or
guard maintenance. Aggregate elapsed and tokens: unknown.

## Implementation verification -- final -- 2026-11-18

The reviewed source through `2e35a655` retains the earlier applicable results
and the additional 0.69-second build-input check. Both code-review obligations
accept, and all their findings are fixed.

**Benefit versus cost**: worth it -- one adopted tool home with preserved project work; cost 398 changed files including moves, 6,979 added and 3,600 removed lines over 21923511..2e35a655; remaining burden one ownership catalog and layout guard, ongoing maintenance cost unknown.

Revisit on repeated manual catalog or guard work. Aggregate elapsed and tokens:
unknown. No further suite or trust operation ran.

## Post-archive security review (re-anchor blocker repairs) -- Opus (Security Review, High) -- 2026-11-18

Reviewed commits: `042d1e43` (roster digest constant, runbook),
`d994fdcd` (meter parametrize ids), `91b02e21` (reflection prune).

**Obligation**: Internal Security Review, post-archive, one pass
**Model basis**: claude-opus-5-5-high (started on gemini-4-argon-high; the
Coordinator switched models at 0% quota, `dev/.cairn/model-selection-mapping.yml` high tier)
**Verdict**: ACCEPT
**Findings**: F1 nonblocking for these commits but open for the cut; F2 and F3 nonblocking.

**Foundations**

1. **Should this happen as framed?** Yes. Before `042d1e43`, the candidate
   could not admit its own relocated roster. At `91b02e21`, `tests/test_gate_manifest.py`
   gave 28 setup errors with "initial protected roster bytes do not match the
   approved roster". The new constant admits only the relocated bytes. Membership
   is unchanged, and that is independently enforced: `release/repin.py:1863-1876`
   requires `sorted(map(relocate, old))` to equal the candidate roster, where the old lists are bound by
   the signed anchor manifest -- `tests/_gate_manifest.py:80-81`, `:349`.
2. **Best alternative.** Raising the 8 MiB package and manifest caps would also have
   cleared the oversized manifest. Explicit ids keep the caps strict at no cost.
   No alternative to a new digest exists: relocation changes the roster bytes
   -- `release/repin.py:600`, `tests/_gate_preflight.py:2922`.
3. **What would show it wrong?** The fix would be wrong if one roster path
   failed to map through the layout catalog, if a non-membership key changed, if
   the old or a tampered roster were admitted, or if either guard were edited.
   Each was checked below; none occurred.

**Verified evidence** (committed objects, Python 3.13.13 at
`$HOME/conda_envs/lhm/bin/python3.13`):

- The signed anchor `e5b7fd0a` (`refs/cairn/gate-anchor`) roster blob equals the
  archived C1c file, SHA-256 `188fa76d...`. Its manifest `protected_roster`
  lists equal that file's lists.
- `release/repin.py` `_layout_path_map`, applied to `install/_scaffold/layout_catalog.py`
  at `d994fdcd`, maps the anchor roster exactly to
  `tests/fixtures/protected_test_roster.json` (`098734196db5...`): 90/90
  protected Python paths, 7/7 fixtures, 57/57 preserved non-test frozen paths
  (29 relocated, 28 unchanged `templates/`), all sorted with no duplicates. The other 25
  keys are byte-equal in parsed form.
- `_roster_from_bytes(require_initial_approval=True)` admits the new bytes and refuses
  both the archived `188fa76d` bytes and a one-byte-appended copy.
- `git diff --stat 72435a0a d994fdcd` shows four files changed. `tests/_gate_manifest.py`
  changed one line, the constant. `release/repin.py`, `tests/_gate_preflight.py`
  and `check_stop_records` (`release/repin.py:2559`) are untouched, and both
  `8 * 1024 * 1024` caps remain.
- `d994fdcd` adds only `ids=` lists, with 7 and 5 labels that match their inputs.
  The 12 inputs and their assertions are unchanged; the 12 tests passed in 0.11 s and were collected
  under the readable ids. No other file or `tests/security_manifest.py` entry
  names either test. The file is not on the roster. Its native-only IDs in
  `tests/security_manifest.py:229-238` belong to other tests.
- The runbook hunk replaces runbook lines 203–206 with 203–208, and its digests
  are accurate. No `RA-` text is touched. `link_check.py` exited 0. `claim_check.py`
  flags only pre-existing lines 79 and 418.
- `91b02e21` removes the only tracked dated reflection. `dev/reflections/README.md`
  says reflections are ignored and only the README is tracked; Git history keeps the file.
  It contains no credentials and no trust records.

**F1 (open for the cut).** At `d994fdcd`, the protected
`tests/test_gate_manifest.py` gives 21 failed and 13 passed in 13.64 s. The
failures come from stale `bootstrap/` literals (42 occurrences), for example
`assert "bootstrap/tests/test_ast_attest.py" in frozen` and `FROZEN-MISSING`.
They were masked at `91b02e21` by the setup errors above, so "pre-existing"
(#47) is unproven. They come from the layout relocation, not these commits. Repairing them edits a
protected test and needs its own Security Review before the `bootstrap-suite`
gate can be green.

**F2.** The brief's "29 preserved" counted only the relocated paths; the list has 57.

**F3.** Lines 79 and 418 of `release/REANCHOR_RUNBOOK.md` still cite the
pre-layout bootstrap test folder.

**Trust note.** The constant lives in the candidate, so it is self-declared.
The authorizing checks remain two. The Maintainer confirms the out-of-checkout
copy of the `098734196db5...` bytes at the ceremony. The layout verifier binds
membership to the signed anchor. Neither has passed yet; both are forward checks.

**Coverage.** Not rerun: `tests/test_repin.py` (129 passed, 237.56 s) and
`tests/test_repin_ceremony.py` (139 passed); the Coordinator recorded both. Also
not rerun: the dry runs, total-manifest size and node counts (1,031,189 bytes, 5,861
nodes), signing, native certification and the full suite. A scratch
worktree at `91b02e21` gave the baseline. It was removed afterward.

**Elapsed**: about 7 minutes. **Tokens**: unknown.

## Post-archive security review (v0.8 closeout #1-#3 fixes) -- Opus (Security Review, High) -- 2026-11-19

Reviewed range: `6080af2d..fe54661c` (`210f94d4`, `7a027b04`, `5118dc2b`,
`865205b7`, `2285a921`, `fe54661c`; 35 files, 609 insertions, 380 deletions).

**Obligation**: Internal Security Review, post-archive, one pass
**Model basis**: claude-opus-5-5-high (Argon at 0% quota until 2026-11-25, dev/.cairn/model-selection-mapping.yml high tier) (commit and board report completed on gemini-4-neon-high after claude-opus-5-5-high hit 429 quota exhaustion)
**Verdict**: ACCEPT
**Findings**: none blocking; N1-N3 nonblocking.

**Conclusion.** No security check, symlink or parent-link containment check,
fail-closed refusal or protected-test promise was weakened. The protected-test
edits relocate paths to the current layout; the three semantic edits keep or
tighten what they check. No file under `install/` changed, so the
`install/_scaffold/` AST baseline is untouched. Its fixtures under
`tests/fixtures/` are also unchanged.

**Foundations**

1. **Should this happen as framed?** Yes. At `6080af2d` the shipped
   `templates/skills/_lib/board.py` resolved its root one level short for a
   `dev/tools/` install, and eight protected test files failed on stale
   pre-layout paths. A red protected gate certifies nothing. Repairing it by
   relocation restores the checks rather than relaxing them.
2. **Best alternative.** Skipping or quarantining the failing nodes would have
   been faster and would have removed coverage. Path relocation keeps every
   assertion. The one test that needed a new fixture (`caller-parent-link`) adds
   a case and keeps the old refusal case.
3. **What would show it wrong?** A dropped or loosened assertion, a refusal
   that now passes, a trust root moved to a caller-controlled location, or a
   changed engine or baseline file. Each was checked below; none occurred.

**Verified evidence** (committed objects at `fe54661c`):

- **`board.py` parity.** `cmp` shows `templates/skills/_lib/board.py` equal to
  `dev/tools/board.py`. The intent facade, intent engine and session kernel now
  load from `Path(__file__).resolve().parent` (`board.py:507-508`, `:799`). For
  both the `dev/tools/` and legacy `tools/` layouts that is the same physical
  folder as before, and it still never comes from `--root`. `_repo_root()`
  (`:791-793`) only sets the default `--root`; it guards nothing.
- **`run_security_audit.py:86`.** `_TOOL_PREFIX` only chooses which lockfile
  keys `integrity_preflight` requires. A missing record, symlink, non-file or
  hash mismatch still raises `AuditDegraded` (`:187-219`). The runner bytes are
  still hash-checked against the lockfile before execution (`:806-818`). A wrong
  prefix therefore refuses; it cannot pass. The `scripts/` legacy branch is
  unchanged.
- **`tests/quality_gate.py:477`.** Adding `""` makes the neutrality walk also
  scan extensionless files under `templates/`. Scanning widens; nothing is
  exempted. `python tests/quality_gate.py --sub neutrality` gave `fail=0
  info=42`.
- **Protected and route tests.** I normalized each hunk for the layout moves
  (`bootstrap/tests/` to `tests/`, `bootstrap/_scaffold/` to `install/_scaffold/`,
  `bootstrap/security_check.py` to `release/security_check.py`, `scripts/` to
  `dev/tools/` or `tests/`). After that, `test_board_json_contract.py`,
  `test_oracle_activation.py`, `test_security_stack.py`,
  `test_reference_scripts.py`, `test_replacement_tools.py` and
  `integration/test_gauge.py` have no remaining changes. `test_gate_reanchor.py`
  changes only `parents[2]` to `parents[1]`, which matches its move up one folder.
  Every relocated target exists (`release/security_check.py`, `release/repin.py`,
  `install/verify_integrity.py` and others).
- **Three semantic test edits.**
  - `tests/security/test_git_read_routes.py`: `returncode != 0` becomes
    `returncode == 2`, which is stricter.
  - `test_session_binding_gate_and_printing_hold.py:52`: I executed the old and
    new `NASTY` lines. Both give U+009B, U+202E, U+3164, so the value is
    unchanged and the raw bidi character is gone.
  - `test_ceremony_review_report.py:48-56`: the "nothing else under `tests/`
    rides along" check now also allows top-level non-test files directly in
    `tests/`. I listed `release.security_check.scan_targets()`: all 23
    top-level `tests/*.py` files are scanned, including the tools moved there
    (`gauge.py`, `measurements.py`, `verify_counts.py` and others). The check
    still rejects fixtures in subfolders and any `test_`, `_` or `conftest`
    file outside the closure, so scan coverage did not shrink.
- **`tests/test_verify_counts.py` binding fixtures.** `parent-link` stays in
  `_BINDING_MUTATIONS`. For a `tests/` caller it still makes the helper's
  `tools/` folder a directory link, and the refusal test still requires
  `git-read-binding-failed` and no helper execution (`:351-361`, `:472-497`).
  The new `caller-parent-link` mutation is used only by the positive
  linked-caller test (`:460-469`). It links the caller's own folder to an
  outside tree that holds the caller and a pinned helper. That was the original
  intent when callers lived in `tools/`. `tools/` callers still take the old
  branch unchanged. The POSIX-only skip moved from the shared route helper to a
  `skipif` on the one PATH-wrapper test. The other two route-helper callers
  (`test_replacement_tools.py`) wrap PATH the same way and now have no Windows
  skip; see N3.
- **Runbooks and rules.** `release/AST_BASELINE_RUNBOOK.md` and
  `dev/rules/certifying-runs.md` change only paths, to targets that exist.
  `release/REANCHOR_RUNBOOK.md` changes only line 418. Line 79 still cites
  `bootstrap/tests/` for the signed v0.7.0 predecessor, as it should.
- **Lockfile and self-install.** `dev/.cairn/cairn-lock.yml` changes 11 `hash`
  values and nothing else: 10 `dev/modules/*.md` and `dev/reflections/README.md`.
  None is code. `python install/verify_integrity.py --target .` reports `OK -- 70
  recorded file(s)`. The installed `dev/modules/security-review.md` now matches
  its template except the allow-comment header. Its Layer 1 provenance wording
  is the template's existing text, not new policy.
- **`dev/scratch/.gitignore`.** It ignores everything except `README.md` and
  itself. That makes accidental commits of scratch data less likely and
  protects nothing that must be tracked.
- **Cap disposition (`2026-11-18-outward-reports.md:266-270`).** The quoted
  words match the Maintainer's reply. In the Coordinator's closeout list
  shown to the Maintainer, the item those words approved recommended accepting
  `7ac42956` at the 2-pass cap. The scribed effect matches what was approved.

**N1 (nonblocking, traceability).** The committed disposition quotes
"#1, #2, and #3" but does not say what those numbers meant. The list lives only
in the Coordinator's local session artifact, so a later reader cannot follow
the quote to `7ac42956` from tracked files. Consider one sentence naming the
closeout item and its recommendation.

**N2 (nonblocking, coverage).** `_FUTURE_NON_TEST_FILES` in
`tests/test_gate_manifest.py` replaced `scripts/new_script.py` with
`release/new_script.py`. That leaves no `dev/tools/*.py` sample, even though
`dev/tools/*.py` is a frozen gate pattern (`tests/_gate_manifest.py:431-432`,
`:469-470`). The code promise is unchanged, but this test no longer
exercises that root. Adding a `dev/tools/` sample would restore it.

**N3 (nonblocking, Windows).** `test_legacy_ls_tree_refuses_target_local_path_git_route`
and `test_legacy_show_refuses_target_local_path_git_route` lost the shared
POSIX-only skip. If their PATH-wrapper route cannot run on native Windows,
they will fail there rather than skip. Not run on Windows in this pass.

**Test runs** (this pass, Python 3.12.9, `-p no:cacheprovider`):
`test_verify_counts.py`, `integration/test_gauge.py`,
`contract/test_test_tiers.py`, `test_board_json_contract.py`,
`test_security_stack.py`, `test_replacement_tools.py` and
`test_session_binding_gate_and_printing_hold.py` gave 642 passed and 1 skipped
in 137.69 s (the single skip was `tests/test_security_stack.py:1012`, `bandit` absent in Python 3.12.9). `test_gate_manifest.py`, `test_gate_reanchor.py`,
`test_oracle_activation.py`, `test_ceremony_review_report.py`,
`security/test_git_read_routes.py`, `test_reference_scripts.py`,
`test_quality_gate_neutrality.py` and `contract/test_board_closeout_warning.py`
gave 243 passed in 164.80 s. `test_verify_counts.py` also passed under Python
3.13.13 (39 passed).

**Coverage.** Not rerun: the Stage 2 17-file batch under Python 3.13.13
(`896 passed in 354.68s` recorded), `sync_doc_snippets`, claim and link checks
on the reconciled module texts, native Windows, signing, the full suite and the
forward re-anchor. I did not review the prose of the 10 reconciled
`dev/modules/*.md` files beyond the security-review module and lockfile hashes.
`release/security_check.py` and its unscanned `dev/tools/` twins are unchanged
in this range and were not assessed. The protected-test edits still need the
forward gate re-anchor ceremony; this pass does not replace it.

**Elapsed**: about 9 minutes for this pass. **Tokens**: unknown.

## Post-archive layout repair: ordinary code review -- Terra (Reviewer, Medium) -- 2026-11-19

**Verdict: ACCEPT. Findings: none.** The repair brings the installer instruction and protected dispatcher fixtures to the installed `dev/tools/` layout and preserves refusal of a hardlinked lock on apply.

**Should this happen as framed?** Yes. The command matches the destination in `install/_scaffold/config.py`; the fixture paths now address the installed dispatcher, helper and capabilities. C2 requires linked paths to refuse without overwrite, and C3 requires commands and tests to resolve relocated modules.

**Best alternative.** Leaving the old fixture paths would test missing files instead of the installed dispatcher. Keeping the old successful-apply assertion would conflict with the current preflight refusal; the separate finalize test still checks replacement without writing through the link.

**What would show it wrong?** A relocated dispatcher that launches a tampered child, an apply that changes the linked victim, or a printed command that does not name the installed dispatcher would falsify this review.

**Evidence and limits.** Read commit `2fdc2c2c`, C2 and C3, the affected public tests and installer mapping. The commit reports 23 focused dispatcher cases passed on Python 3.12.9 and two hardlink cases passed on Python 3.13.13; I did not rerun them. I did not review earlier layout changes or perform Security Review.

**Elapsed**: unknown. **Tokens**: unknown.
