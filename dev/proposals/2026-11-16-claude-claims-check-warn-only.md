# Make the claims check warn only by default

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: accepted
**Review**: usual
**Proposed tier**: light -- a one-word default change with matching text and test edits, easy to undo, and the Maintainer has already chosen the direction
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-16
**In brief**: The optional commit-time check that refuses a commit when another session holds a claim on the same file will warn instead, because Cairn's tools warn and do not block process checks.

## Decision summary

Today, an adopter who installed the opt-in commit hook (`python tools/intent.py install-precommit`) has commits refused when a different live session holds a fresh claim on a staged file, unless they set `"enforce": "warn"`. On 2026-11-10 this refused a commit here, against the working agreement that process checks warn. The Maintainer decided on 2026-11-13: "Go with warn only on the claims check".

Proposed: when no `enforce` setting exists (or it is unreadable), the check warns and lets the commit through. An adopter who wants refusal sets `"enforce": "block"`; that keeps working. The change edits both copies of one engine file, the documents named in item 2, one test file and one board note. Cost: an adopter who relied on the old default and never wrote a setting loses the refusal on upgrade, and the check no longer records `prevented` incidents by itself for them.

## Context

Verified in the current tree:

- `_read_enforce_mode` (`tools/_intent/conflict.py` line 367) returns `"block"` for a missing config file, unreadable file, non-object file and unknown value (lines 380, 384, 386, 388). The comment above it (lines 357-363) and its docstring call `block` the shipped default.
- `templates/modules/team-gated/_intent/conflict.py` is byte-identical to the tool copy (checked with `diff`).
- The scaffold never installs the hook, so only adopters who ran `install-precommit` are affected. `block` refuses only when a different live session holds a claim younger than the four-hour limit and the committer has a session token; otherwise it warns (`docs/methodology/coordination.md` lines 259-270).
- `dev/rules/working-agreements.md` line 10 says the default "still refuses until roadmap item 28 changes it".

## Proposal

1. In both `conflict.py` files, change the four `"block"` returns in `_read_enforce_mode` to `"warn"`, and correct the comment and docstring. `confirm` and `block` stay valid settings.
2. Correct the documents that call `block` the default: `docs/methodology/coordination.md` lines 262 and 287; `templates/modules/team-gated/coordination-tiers.md` lines 109 and 153; `templates/modules/default-on/incident-trackers.md` lines 66 and 70, which say the auto-writer records `prevented` "under the shipped `block` default". The board names only two of these; I found the rest by searching. Cairn's own installed copies under `dev/modules/` (`coordination-tiers.md`, `incident-trackers.md`) repeat the same lines and follow by the usual module refresh. Also correct `dev/agent_collaboration.md` line 491 ("shipped `block` mode"), `coordination-tiers.md` lines 103-104 ("the default `block` mode", split across a line break) and the comments in `conflict.py` at lines 658-661, 1051 and 1087-1088, in one pass so the two engine copies stay identical. Update `working-agreements.md` line 10 and add one `Unreleased` CHANGELOG entry: a Major change, typed `**Changed:**` with a short title, as the CHANGELOG's own rules require. Not checked: whether `dev/modules/` is regenerated or edited by hand.
3. Tests in `bootstrap/tests/test_intents_tool.py`. After reading the file, these rely on the old default:
   - Replace `test_no_config_blocks_cross_claim_by_default` (it asserts refusal with no config) with `test_no_config_warns_on_cross_claim_by_default`: no config warns, exits 0 and still prints "HELD BY ANOTHER". The old name is a recorded test ID in the gate manifest, so the rename changes that list (see Assurance path).
   - Add an explicit `enforce=block` setting to `test_fresh_cross_claim_still_blocks`, `test_stale_cross_claim_warns_but_does_not_block`, `test_malformed_ts_does_not_crash_or_block`, `test_naive_offset_ts_does_not_crash`, `test_real_two_session_shared_index_sweep_is_blocked`, `test_block_records_prevented_real_commit`, `test_record_failure_does_not_break_the_block`, the `install-precommit` case of `test_metacharacter_paths_never_execute_in_hooks`, `test_static_identity_does_not_suppress_own` and `test_no_token_collision_records_no_incident`. The last two set no mode and assert the "WITHHELD" note, which the check writes (`conflict.py` line 1074) only after it has already returned for `warn` (line 1053), so without the setting they would fail (read from the code, not run). Without the setting the stale, malformed and naive-timestamp tests would still pass but stop testing their fail-safe.
   - Fix docstrings and comments that say "default block". `test_block_refuses_other_session` and `test_explicit_warn_never_blocks_but_surfaces` already set their mode and stay. Retire none: each pinned `block` still has a real promise once configured. Not checked: the rest of the file beyond a search for "enforce" and "block".
4. Lift the fence. The archived promise-testing plan's Dispositions addendum (2026-11-13) says: "the claims-family tests stay uncut until the Maintainer answers whether the claims tool's pre-commit check warns or blocks". Its 2026-11-12 clarification says claims-tool tests "remain fenced on their separate pre-commit-half Decision". The 2026-11-13 decision answers that question, so the claims-family tests become eligible for the plan's direct-pruning rules. This proposal prunes nothing; a later pass owns that. The Decision records the lift, because the plan is archived and stays unchanged.

Out of scope: issue #63 part 1 (the same hook on Windows).

## Rationale

The working agreement (2026-08-21) is that process checks warn and hard refusal is for safety such as scaffold containment. A refused commit under a stale or mistaken claim is a wedge for a one-developer repository. Warning still surfaces the overlap, and `block` stays available.

## Alternatives considered

- Keep `block` and document it: contradicts the Maintainer's 2026-11-13 decision.
- Remove `block` and `confirm`: removes a choice some adopters may use; nothing here asks for it.
- Do nothing: the next adopter hits the same refusal.

## Documentation / doctrine surface

`docs/methodology/coordination.md` is descriptive; the edit corrects the stated default and moves no doctrine. Not checked: whether the doctrine-evolution gate applies; I claim no trigger. Module text lands in the `templates/modules/` files and the descriptive layer.

## Evidence / verification plan

The claim is falsified if, with no setting, a commit under another session's fresh claim is still refused, or if `"enforce": "block"` stops refusing.

### Tests required

Promise: no setting means warn and exit 0; `"enforce": "block"` still refuses a fresh overlap and spares a stale one. Entry point: `_precommit_check` through the CLI, and a real `git commit` with the hook installed. Selected checks: `python tools/test_tiers.py for tools/_intent/conflict.py templates/modules/team-gated/_intent/conflict.py bootstrap/tests/test_intents_tool.py`, which lists the tests naming those files. No test was run for this proposal.

### Examples / smoke checks

`python scripts/claim_check.py` on the changed documents and the prose gates for the doc edits.

## Compatibility and adopter impact

Affected: only adopters who installed the opt-in hook. An adopter with an explicit `"enforce"` setting sees no change. One without a setting moves from refusal to warning when the upgrade replaces the engine file. The upgrade treats it as a hash-tracked verbatim engine file (`bootstrap/UPGRADE.md`); an adopter who edited the file gets a conflict listing, not a silent overwrite. The CHANGELOG entry tells adopters to add `"enforce": "block"` in `dev/.cairn/intent-config.json` (legacy `dev/intent-config.json`) to keep refusal. Not checked: whether `upgrade` prints a notice for a changed default.

## Assurance path

Only the shipped copy, `templates/modules/team-gated/_intent/conflict.py`, is a frozen file: `bootstrap/tests/fixtures/gate_manifest.json` lists it under `frozen_files`, and does not list `tools/_intent/conflict.py`. Neither is in the AST baseline, which covers `bootstrap/_scaffold/` only (`scaffold_ast_baseline.json` has no `_intent` entry). So the ceremony owed is the Maintainer's gate re-anchor (`bootstrap/REANCHOR_RUNBOOK.md`), not the AST baseline: it refreshes the frozen file's recorded hash and the manifest's list of test IDs, which changes because one test is renamed (item 3). Until then the gate-manifest tests report the mismatch, as expected for a reviewed change (`dev/rules/protected-surfaces.md`); only the Maintainer re-anchors. The 0.7 re-anchor is done, so this joins the 0.8 one. I did not run the gate tests.

**Tier check.** The template makes light the default, and says a light proposal gets no plan however wide the work. I agree with light; no Security Review is proposed, since the change relaxes a refusal and adds no trust boundary. Security: N/A: no new input, path or privilege.

**For the Maintainer.** The only open choice is the shape of the notice on upgrade. My default is the CHANGELOG entry alone, without a new upgrade message.

## Review -- Claude Sonnet 5.5 (ordinary Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: dae317c8e839ce14cf97b36b7039c68ea314ac79
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 4 minutes (11:54 to 11:58 EST, 2026-11-16)
**Tokens**: unknown

The strongest case: the Maintainer chose warn-only, so a four-line default flip plus matching text makes the tool obey the working agreement, with `block` still one setting away.

**Foundations**

1. **Should this happen as framed?** Yes, as a light change; the direction is decided, but the scope list is not yet complete (findings 1-3). -- `dev/rules/working-agreements.md` line 10; `tools/_intent/conflict.py` lines 380-388
2. **Best alternative.** None better: documenting `block` as the default contradicts the decision, and removing `block` is not asked for. The installed hook text needs no edit, because it only calls `_precommit_check` and states no default. -- `tools/_intent/conflict.py` `_precommit_hook_block`
3. **What would show it wrong.** After the edit, the `TestEnforceModeAndN1`, `TestClaimTTL` and `TestSensingWritePath` classes are not all green with only the listed test changes. -- `python tools/test_tiers.py for bootstrap/tests/test_intents_tool.py`

1. **Blocking.** Item 3 omits two tests that rely on the old default. `test_static_identity_does_not_suppress_own` (line 2103) and `test_no_token_collision_records_no_incident` (line 2851) set no `enforce` and assert the "WITHHELD" note. `_precommit_check_impl` returns 0 for `warn` at line 1053, before it writes that note at line 1074, so both fail after the flip (read from the control flow, not run). Add them to the `enforce=block` list. Closes: item 3 names them, or a green run of those three classes.
2. **Blocking.** The Assurance path is imprecise. Only `templates/modules/team-gated/_intent/conflict.py` is in `gate_manifest.json` `frozen_files` (and the protected roster); `tools/_intent/conflict.py` is in neither. `AST_BASELINE_RUNBOOK.md` covers `bootstrap/_scaffold/`, and `scaffold_ast_baseline.json` has no `_intent` entry. Also `test_no_config_blocks_cross_claim_by_default` is a `collection.node_ids` entry, so a rename changes collection identity. State which ceremony the Maintainer owes (or cite the text that sends `_intent` edits to the AST baseline), and either keep that test name or name the rename. Closes: corrected paragraph.
3. **Non-blocking.** The text sweep misses `dev/agent_collaboration.md` line 491 ("shipped `block` mode"), `coordination-tiers.md` lines 103-104 ("the default `block` mode", split by a line break), and `conflict.py` comments at lines 658-661, 1051 and 1087-1088. Fix them in one pass so both copies stay identical. Closes: items 1-2 name them.
4. **Non-blocking.** The adopter change is disclosed well. Add that the CHANGELOG entry is a Major change, typed `**Changed: ...**` with a title, per the CHANGELOG rules. No hook reinstall is needed.

**Audience / rule loss:** One rule weakens on purpose: a fresh cross-session claim no longer refuses by default. No rule disappears; `block` and `confirm` and their conditions stay.

**Coverage:** I ran no test and did not read all of `test_intents_tool.py`; I read the enforce, claim, hook and sensing sections. I did not check the upgrade path or `dev/modules/` regeneration. A scratch simulation of the flip did not run, so finding 1 rests on reading. The plan fence quotation matches. Over the 300-word target because findings 1-3 need their evidence.

## Response -- Claude Fable 5.2 (coordinator, for the Sonnet author) -- 2026-11-16

**Elapsed**: about 15 minutes. **Tokens**: unknown.

I checked each finding against the tree before accepting it. All four hold, and the operative text above is revised in place.

1. **Accepted (blocking).** Both tests are added to the `enforce=block` list in item 3, with the reason. I read the control flow the reviewer cites and agree; neither of us ran the tests.
2. **Accepted (blocking).** The Assurance path is rewritten. Checked in `gate_manifest.json`: only the shipped copy is under `frozen_files`, the AST baseline has no `_intent` entry, and the old test name is a recorded test ID. The ceremony owed is the Maintainer's gate re-anchor. Item 3 now names the rename.
3. **Accepted (non-blocking).** Item 2 adds the three places. The shipped copy of `dev/agent_collaboration.md` does not carry that sentence (searched), so only Cairn's own copy changes.
4. **Accepted (non-blocking).** Item 2 says the entry is a Major change, typed and titled.

The Decision summary's count of files is replaced by a pointer to item 2, since the list grew. Scope is otherwise unchanged, and the tier stays as proposed: light. Not checked, as before: whether the copies under `dev/modules/` are refreshed by a tool, and whether `upgrade` prints a notice for a changed default.

**For the Maintainer.** One choice remains: how adopters learn of the change at upgrade. Default: the CHANGELOG entry alone.

## Decision -- Maintainer (scribed by Antigravity Gemini 4 Hydrogen) -- 2026-11-16

**Tier**: light

**ACCEPTED.**

> "I accept #1 - #4 with your recommendations. #5 I accept requiring the checks to be working on windows"

This accepts the proposal as revised (`light` tier, no plan), using the `CHANGELOG.md` Major-change entry alone to inform adopters of the default change from `block` to `warn`, and lifting the pruning fence on `bootstrap/tests/test_intents_tool.py` (which joins the v0.8 gate re-anchor alongside the frozen `conflict.py` twin). New recurring human operations: zero.

**Elapsed:** under 1 minute. **Tokens:** unknown.

## Implementation verification -- Claude Sonnet 5.5 (Implementer, Medium) -- 2026-11-16

**Commits**: `dc6e4ffb` (both `conflict.py` copies and `bootstrap/tests/test_intents_tool.py`), `dee3626a` (the five documents in item 2). Items 1-3 done as written; item 4 is a Decision-only record. **Elapsed**: about 14 minutes (12:21 to 12:35 EST). **Tokens**: unknown.

**Run (interpreter `/Users/kendal30/conda_envs/lhm/bin/python3.13`)**
- Test file before the code change: one failure, the new `test_no_config_warns_on_cross_claim_by_default` (exit 1, not 0), so the ten `enforce=block` edits did not break anything on the old default.
- Same file after: 199 passed, 1 skipped (127 s). The skip was not examined.
- Five tests that read the edited docs (`test_writing_rules_ship`, `test_review_stance_in_shipped_files`, `test_review_sweep_ships`, `test_incident_trackers_module`, `test_coordination_broad_intent`): 50 passed.
- `diff -q` on the two `conflict.py` copies: identical. `test_security_stack` conflict.py pin cases: 4 passed.
- `claim_check.py` on the five documents: no flags. `link_check.py` (five files): clean. `sync_doc_snippets.py --check`: no drift in 642 docs.
- `quality_gate.py --sub neutrality`: one FAIL, `bootstrap/PROVENANCE.md:122` (`Microsoft`), another agent's file; none in mine.

**Red or held, expected**
- `_gate_manifest.py verify --no-collect` HOLDs. Four of its nine lines are this change: `FROZEN-MODIFIED` and `FROZEN-OID` for `templates/modules/team-gated/_intent/conflict.py` and for `bootstrap/tests/test_intents_tool.py`. So the test file is itself a pinned frozen file, which the Assurance path did not say; the re-anchor covers it. The other five are other agents' uncommitted edits.
- `test_gate_manifest.py`: 10 failed, 24 passed; I traced the first failure to those other edits, not to mine.

**Not run**: the manifest collection check (it would flag the renamed test ID), `test_ast_attest` (the baseline has no `_intent` entry, `grep` count 0), any full suite, Windows, the upgrade path, `dev/modules/` refresh.

**Left for others**: `tools/_intent/cli.py` lines 455-456 and 658, and the identical `templates/modules/team-gated/_intent/cli.py`, still say `block` is the shipped default (`--help` text for `install-precommit`); not named in this proposal. CHANGELOG entry and the board note were not mine to edit.

**Benefit versus cost**: worth it -- the claims check now warns by default as the Maintainer decided and the tests pin both the new default and `block`; cost 2 commits, 8 files, +105/-83 lines, 127 s test run, about 14 minutes; remaining burden the Maintainer's v0.8 re-anchor (already owed), the CHANGELOG entry, the two stale `cli.py` help lines, and the `dev/modules/` refresh

## Implementation verification addendum -- Claude Sonnet 5.5 (coordinator) -- 2026-11-16

Found after the implementer's record: `tools/_intent/cli.py` and its twin still called `block` the shipped default, in the `_cmd_precommit_check` docstring and in the `install-precommit` help text that adopters see. Corrected in both copies, which stay identical (commit message "Correct the claims-check default in the intent CLI docstring and install-precommit help"). This is outside item 2's list but serves the same purpose; no behavior changed. Checked: `test_intents_tool.py` and `test_verify_ref.py`, 264 passed, 1 skipped. The templates copy of `cli.py` is a frozen file and joins the Maintainer's re-anchor. The Decision's quoted "#5 ... windows" belongs to the Windows route-check proposal and does not bear on this one.
