# Make the claims check warn only by default

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-review
**Waiting on Maintainer**: release draft for review
**Review**: usual
**Proposed tier**: light -- a one-word default change with matching text and test edits, easy to undo, and the Maintainer has already chosen the direction
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-16
**In brief**: The optional commit-time check that refuses a commit when another session holds a claim on the same file will warn instead, because Cairn's tools warn and do not block process checks.

## Decision summary

Today, an adopter who installed the opt-in commit hook (`python tools/intent.py install-precommit`) has commits refused when a different live session holds a fresh claim on a staged file, unless they set `"enforce": "warn"`. On 2026-11-10 this refused a commit here, against the working agreement that process checks warn. The Maintainer decided on 2026-11-13: "Go with warn only on the claims check".

Proposed: when no `enforce` setting exists (or it is unreadable), the check warns and lets the commit through. An adopter who wants refusal sets `"enforce": "block"`; that keeps working. The change edits two engine files, five documents, one test file and one board note. Cost: an adopter who relied on the old default and never wrote a setting loses the refusal on upgrade, and the check no longer records `prevented` incidents by itself for them.

## Context

Verified in the current tree:

- `_read_enforce_mode` (`tools/_intent/conflict.py` line 367) returns `"block"` for a missing config file, unreadable file, non-object file and unknown value (lines 380, 384, 386, 388). The comment above it (lines 357-363) and its docstring call `block` the shipped default.
- `templates/modules/team-gated/_intent/conflict.py` is byte-identical to the tool copy (checked with `diff`).
- The scaffold never installs the hook, so only adopters who ran `install-precommit` are affected. `block` refuses only when a different live session holds a claim younger than the four-hour limit and the committer has a session token; otherwise it warns (`docs/methodology/coordination.md` lines 259-270).
- `dev/rules/working-agreements.md` line 10 says the default "still refuses until roadmap item 28 changes it".

## Proposal

1. In both `conflict.py` files, change the four `"block"` returns in `_read_enforce_mode` to `"warn"`, and correct the comment and docstring. `confirm` and `block` stay valid settings.
2. Correct the documents that call `block` the default: `docs/methodology/coordination.md` lines 262 and 287; `templates/modules/team-gated/coordination-tiers.md` lines 109 and 153; `templates/modules/default-on/incident-trackers.md` lines 66 and 70, which say the auto-writer records `prevented` "under the shipped `block` default". The board names only two of these; I found the rest by searching. Cairn's own installed copies under `dev/modules/` (`coordination-tiers.md`, `incident-trackers.md`) repeat the same lines and follow by the usual module refresh. Update `working-agreements.md` line 10 and add one `Unreleased` CHANGELOG entry. Not checked: whether `dev/modules/` is regenerated or edited by hand.
3. Tests in `bootstrap/tests/test_intents_tool.py`. After reading the file, these rely on the old default:
   - Replace `test_no_config_blocks_cross_claim_by_default` (it asserts refusal with no config) with a test that no config warns, exits 0 and still prints "HELD BY ANOTHER".
   - Add an explicit `enforce=block` setting to `test_fresh_cross_claim_still_blocks`, `test_stale_cross_claim_warns_but_does_not_block`, `test_malformed_ts_does_not_crash_or_block`, `test_naive_offset_ts_does_not_crash`, `test_real_two_session_shared_index_sweep_is_blocked`, `test_block_records_prevented_real_commit`, `test_record_failure_does_not_break_the_block` and the `install-precommit` case of `test_metacharacter_paths_never_execute_in_hooks`. Without the setting the stale, malformed and naive-timestamp tests would still pass but stop testing their fail-safe.
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

Both files are frozen engine files. Per `dev/rules/protected-surfaces.md` and `bootstrap/AST_BASELINE_RUNBOOK.md`, the edit leaves an expected AST mismatch that does not block plan archive, and only the Maintainer re-anchors. The change joins the next baseline ceremony. The 0.7 ceremony is done, so this lands in the 0.8 one.

**Tier check.** The template makes light the default, and says a light proposal gets no plan however wide the work. I agree with light; no Security Review is proposed, since the change relaxes a refusal and adds no trust boundary. Security: N/A: no new input, path or privilege.

**For the Maintainer.** The only open choice is the shape of the notice on upgrade. My default is the CHANGELOG entry alone, without a new upgrade message.
