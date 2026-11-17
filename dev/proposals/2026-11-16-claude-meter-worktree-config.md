# The safe origin reader accepts repositories that use worktrees

**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`), coordinator
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: light — a small, reversible defect repair, but it changes what a pinned protected helper accepts, so it keeps a Security Review (the Maintainer sets the tier).
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-16
**In brief**: The usage meter cannot run on any of the Maintainer's three projects, because Cairn's safe Git reader refuses a repository whose config has the worktree setting turned on. This lets it read the origin URL anyway.

## Decision summary

The meter checks which Git remote a project has before it reads any log. The helper that reads that remote (`read_origin_from_config`, pinned and shared by many tools) returns "unavailable" whenever the repository config contains `extensions.worktreeConfig`, the setting Git leaves behind once a repository has used worktrees. All three projects the Maintainer has consented to the meter have it, so `meter refresh` reports `unavailable: project_remote_unavailable` and reads nothing. I recommend dropping that one refusal and keeping every other. Cost: one small edit in the helper, a new helper pin, a Security Review, and the Maintainer's re-anchor for the pinned files. Maintainer direction, chat 2026-11-16: "get it working quickly".

## Context

Measured 2026-11-16 at `c559a76b`, reading no log and printing no remote URL. On Cairn's own `.git/config` the origin query exits 0 with two keys, `remote.origin.url` and `extensions.worktreeconfig`, and `_parse_origin_config_result` (`tools/git_read.py` about line 655) returns None because it refuses the `extensions.worktreeconfig` key, as it refuses any `include.*` or `includeif.*` key. A synthetic config holding only the origin URL, in https or SSH form, parses. All three consented projects have `extensions.worktreeConfig = true` (Cairn lists 80 worktrees, the others 5 and 1). The meter maps the failure to `git_parser_failed`, then `project_remote_unavailable` (`tools/meter.py` about line 5648). The reader was added on 2026-11-06 (`2da114e0`); the refusal is its deliberate "reject all other disclosure" rule, not a recent change.

## Proposal

In both copies of the helper (`templates/skills/_lib/git_read.py` and `tools/git_read.py`, byte-identical), remove `extensions[.]worktreeconfig` from `_ORIGIN_CONFIG_PATTERN` and delete the parser's special case for that key, so the query never returns it. Still refused: an `include.*` or `includeif.*` key (`--no-includes` would silently drop an included origin override), a missing origin URL, an empty value, more than one origin URL, a record with no newline, and output not ending in a null byte. The meter's own refusal of a `.git` that holds `commondir` or `config.worktree` (`tools/meter.py` about lines 5726 to 5731, Windows twin about 5796) stays. Then re-pin the helper's digest in the 23 tool files and the second-order digest in both `exact_replace.py`, as at defects C7 and C9, and run the scoped lockfile finalize.

**Not changed.** Per-worktree config (`config.worktree`) is not read; the meter takes the shared config's origin, and already refuses a project whose main `.git` has `config.worktree` (`project_layout_unsupported`). The Windows worker route and every other helper operation.

## Rationale

A `config.worktree` file lives inside the same `.git` folder as `config`. Whoever can write one can edit `config` itself, so refusing the extension protected nothing the config read does not already trust. The alternative, reading `config.worktree` through the same bounded buffer and requiring it not to set the origin, is more code and more review for a threat the folder permissions already cover. The meter already fails closed when the main `.git` holds `config.worktree` or `commondir`, and a linked worktree's own override applies only to that worktree, so no residual of note remains; the returned remote is only compared with the consented one, so a wrong remote is a mismatch.

## Documentation / doctrine surface

None. No governing layer, guide or shipped template changes. A CHANGELOG line (Minor, Fixed): the meter now works in a repository that uses Git worktrees.

## Evidence / verification plan

Tests, each failing first, through `read_origin_from_config` and the meter's `_verified_project_remote`, with synthetic config bytes (never the Maintainer's real config or logs): the extension plus an origin URL (https and SSH) completes with that URL; the extension plus an include key is still refused; the extension alone, two origin URLs, an empty origin value, and trailing garbage are still refused; and one test that the meter still refuses a project whose `.git` has `commondir` or `config.worktree`. Run only the files `python tools/test_tiers.py for` lists for the changed paths, no whole-suite run. After the pin cycle, `python scripts/repin.py status` shows the helper pin equal to the digest, and the Maintainer's `meter refresh --json` on the real projects is the first live evidence (counts and status only). Not run: Windows, since the worker route is unchanged.

## Signals the change is wrong

A refresh that reports `ok` for a project whose real origin differs from its consent; an include key accepted.

## Scope delta

N/A: opening draft.

## Assurance path

**Assurance path**: high-assurance — a pinned protected helper changes what it accepts.

## Security Review -- Claude Opus (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: 5debf8d21369129229a59e071397a8b64e4bc828
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: ACCEPT

**Elapsed**: about 1 minute (17:26:40 to 17:27:20 EST)
**Tokens**: unknown

Obligation: does skipping an `extensions.worktreeconfig` record, instead of refusing the read, open a disclosure or bypass?

Steelman: one skipped key restores the meter on every consented project while every other refusal stays.

**Foundations**

1. **Should this happen as framed?** Yes; the pattern and argv are unchanged, so only the origin URL, `include*` and that key reach the parser; include keys stay refused because `--no-includes` would silently drop an included origin override -- `tools/git_read.py` lines 81-84, 642-652, 664-666.
2. **Best alternative.** Read `config.worktree` and require it not to set the origin; unneeded, because the meter already refuses a project whose `.git` holds `config.worktree` or `commondir` -- `tools/meter.py` lines 5726-5731, 5796.
3. **What would show it wrong.** A second caller of the reader that lacks that file check; `git grep -l read_origin_from_config` finds only the meter and tests.

**Findings**

1. Non-blocking. The Rationale's residual ("a per-worktree origin override is invisible") overstates it: the meter fails closed with `project_layout_unsupported` when the main `config.worktree` exists, and a linked worktree's override applies only to that worktree. Cite this check and keep it. The returned remote is only compared with the consented remote (line 5701), so a wrong one is a mismatch, not misattribution. Synthetic repro: extension plus URL parses to None today (scratchpad script, `git config --file -`).

Coverage: did not check Windows, the pin-digest mechanics beyond the C7/C9 precedent, or any real project config.

## Review -- Claude Sonnet 5.5 (ordinary Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: 5debf8d21369129229a59e071397a8b64e4bc828
```

**Tier**: usual
**Findings**: raised (3, all non-blocking)
**Verdict**: ACCEPT

**Elapsed**: about 3 minutes (17:26:40 to Nov 16 17:28:05 EST 2026, 2026-11-16, quick pass)
**Tokens**: unknown

Steelman: one small, reversible edit lets the meter run on repositories that have used worktrees, and the extension line discloses nothing on the `--file -` buffer read.

**Foundations**:

1. **Should this happen as framed?** Yes. I reproduced the fault with a synthetic config (extension plus origin: `failed`, `origin-config-result-unavailable`; origin alone: completes) -- `/Users/kendal30/conda_envs/lhm/bin/python3.13 -I`, `tools/git_read.py` imported by path; the two helper copies are byte-identical (`cmp`).
2. **Best alternative.** Delete the `extensions[.]worktreeconfig` alternative from `_ORIGIN_CONFIG_PATTERN` and the matching `or key ==` clause (`tools/git_read.py` lines 81-84, 669-671) instead of adding a skip branch: two deletions, a narrower query, and the parser's `key != "remote.origin.url"` refusal still catches the key if it ever returned. Same pin cycle.
3. **What would show it wrong.** A refresh that still reports `project_layout_unsupported`, or a test where an include key survives -- `tools/meter.py` lines 5726-5731.

**Findings**:

1. Non-blocking. The meter already refuses a `.git` holding `commondir` or `config.worktree` (`_posix_project_config` and the Windows twin, `project_layout_unsupported`), and a linked worktree whose `.git` is a file. The proposal does not mention this guard: its Rationale residual (a per-worktree origin override invisible to the meter) is already closed for the main checkout, and the fix helps only projects with neither file. Cairn's own `.git` has neither (existence checked only). Add one test that the guard still fires with the extension present.
2. Non-blocking. Refusals the change keeps and the proposal does not name: a bare `worktreeConfig` line with no value (record has no newline, line 660), a non-ASCII key (667), and the catch-all for any other key (672). The skip applies to every value, `= false` included. Say so, or test it.
3. Non-blocking. Context sentence is garbled: include and includeif keys are refused, not exempt (lines 669-671).

Refusals kept: include.*, includeif.*, no origin, empty value, a second origin, missing trailing NUL, malformed framing.

**Coverage**: Not checked: the other two consented projects' `.git` layout (off limits), tests, pin cycle mechanics, Windows, Security questions, the live refresh.

## Response -- Claude Sonnet 5.5 (author) -- 2026-11-16

Both quick passes are ACCEPT with no blocking findings. Operative text revised in place; the reviews are unchanged.

- **Security 1** (residual overstated): accepted. Rationale now cites the meter's existing refusal of `config.worktree` and `commondir` and says no residual of note remains.
- **Ordinary 1** (guard not mentioned; add a test it still fires): accepted. Named in Proposal; the test is in the verification plan.
- **Ordinary 2** (simpler: remove the key from the pattern and the parser clause): accepted; the Proposal now says that. Same behavior, fewer lines.
- **Ordinary 3** (kept refusals unnamed, garbled Context sentence): accepted; both fixed.

**Elapsed**: about 4 minutes (17:29 to 17:33, `date`). **Tokens**: unknown.

## Decision -- Maintainer (recorded from chat by Claude Sonnet 5.5, not scribed by Antigravity) -- 2026-11-16

**Tier**: light

**ACCEPTED**, by the Maintainer's direction in chat, 2026-11-16: "Great, yeah get it working quickly and then we can do a full session handoff after." This accepts the recommended option (remove the refusal) with the review findings folded in. Recurring human operations added: none beyond the one re-anchor the pinned files already owe. If the Maintainer wants a different option, `git revert` of the implementation commits undoes it, followed by one more pin cycle.

## Implementation record -- Claude Sonnet 5.5 -- 2026-11-16

Built by a Sonnet implementer and the coordinator. The simpler form (remove the key from the query pattern) landed at `04be1505`; the scoped lockfile record at `3be80d14`. The implementer's tests: 9 helper tests (3 failing first) and 5 meter tests (2 failing first), 8 mutants all caught; the new helper digest is pinned in the 23 files and both `exact_replace.py` second-order digests. Red until the Maintainer's re-anchor: the gate-manifest digest tests and `test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`.

Live check, 2026-11-16 20:5x: `python tools/meter.py refresh --json` moved from `project_remote_unavailable` to a second refusal: the meter's strict claim parser raised on 1,565 older records in Cairn's own `dev/intents.jsonl` whose agent is a name (for example a coordinator title), not a session tag. Fixed as a defect repair at `b78b8fa3` (such a claim is skipped; a malformed files list is still refused; one failing-first test; `test_meter.py` 489 passed, 35 skipped; six more tier files 149 passed; not run: `test_session_routines.py` after that change). The refresh now reaches `source_budget_exceeded`, the known limit that meter plan chunks C5 to C8 remove; the proposal's aim (the meter gets past the project checks) is met, and the budget is the plan's.

Not run: Windows (the worker route is unchanged and the Windows twin of the `commondir` and `config.worktree` refusal has no fake); the other two projects' own claim ledgers (their layouts were not read). Owed before archive: the Maintainer's re-anchor and the joined targeted check.

**Benefit versus cost**: the project checks now pass for Cairn and the worktree-using projects, for two small edits and one pin cycle; the whole-log refresh stays unavailable until the plan's later chunks land.
