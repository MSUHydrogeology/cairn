# The safe origin reader accepts repositories that use worktrees

**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`), coordinator
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: light — a small, reversible defect repair, but it changes what a pinned protected helper accepts, so it keeps a Security Review (the Maintainer sets the tier).
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-16
**In brief**: The usage meter cannot run on any of the Maintainer's three projects, because Cairn's safe Git reader refuses a repository whose config has the worktree setting turned on. This lets it read the origin URL anyway.

## Decision summary

The meter checks which Git remote a project has before it reads any log. The helper that reads that remote (`read_origin_from_config`, pinned and shared by many tools) returns "unavailable" whenever the repository config contains `extensions.worktreeConfig`, the setting Git leaves behind once a repository has used worktrees. All three projects the Maintainer has consented to the meter have it, so `meter refresh` reports `unavailable: project_remote_unavailable` and reads nothing. I recommend dropping that one refusal and keeping every other. Cost: one small edit in the helper, a new helper pin, a Security Review, and the Maintainer's re-anchor for the pinned files. Maintainer direction, chat 2026-11-16: "get it working quickly".

## Context

Measured 2026-11-16 at `c559a76b`, reading no log and printing no remote URL. On Cairn's own `.git/config` the origin query exits 0 with two keys, `remote.origin.url` and `extensions.worktreeconfig`, and `_parse_origin_config_result` (`tools/git_read.py` about line 655) returns None because any key other than the origin URL, an `include.*` key or an `includeif.*` key is refused. A synthetic config holding only the origin URL, in https or SSH form, parses. All three consented projects have `extensions.worktreeConfig = true` (Cairn lists 80 worktrees, the others 5 and 1). The meter maps the failure to `git_parser_failed`, then `project_remote_unavailable` (`tools/meter.py` about line 5648). The reader was added on 2026-11-06 (`2da114e0`); the refusal is its deliberate "reject all other disclosure" rule, not a recent change.

## Proposal

In both copies of the helper (`templates/skills/_lib/git_read.py` and `tools/git_read.py`, byte-identical), change `_parse_origin_config_result` so a record whose key is `extensions.worktreeconfig` is skipped instead of refusing the whole read. Keep refusing an `include.*` or `includeif.*` key, a missing origin URL, an empty value, more than one origin URL, and any output not ending in a null byte. The query pattern stays as it is, so nothing else can reach the reader. Then re-pin the helper's digest in the 23 tool files and the second-order digest in both `exact_replace.py`, as at defects C7 and C9, and run the scoped lockfile finalize.

**Not changed.** Per-worktree config (`config.worktree`) is not read; the meter takes the shared config's origin, as it does today for repositories without worktrees. The Windows worker route and every other helper operation.

## Rationale

A `config.worktree` file lives inside the same `.git` folder as `config`. Whoever can write one can edit `config` itself, so refusing the extension protected nothing the config read does not already trust. The alternative, reading `config.worktree` through the same bounded buffer and requiring it not to set the origin, is more code and more review for a threat the folder permissions already cover. The residual is that a deliberate per-worktree origin override is invisible to the meter, which could then match a project by the shared origin; counts would be attributed to the shared remote.

## Documentation / doctrine surface

None. No governing layer, guide or shipped template changes. A CHANGELOG line (Minor, Fixed): the meter now works in a repository that uses Git worktrees.

## Evidence / verification plan

Tests, each failing first, through `read_origin_from_config` and the meter's `_verified_project_remote`, with synthetic config bytes (never the Maintainer's real config or logs): the extension plus an origin URL (https and SSH) completes with that URL; the extension plus an include key is still refused; the extension alone, two origin URLs, an empty origin value, and trailing garbage are still refused. Run only the files `python tools/test_tiers.py for` lists for the changed paths, no whole-suite run. After the pin cycle, `python scripts/repin.py status` shows the helper pin equal to the digest, and the Maintainer's `meter refresh --json` on the real projects is the first live evidence (counts and status only). Not run: Windows, since the worker route is unchanged.

## Signals the change is wrong

A refresh that reports `ok` for a project whose real origin differs from its consent; an include key accepted.

## Scope delta

N/A: opening draft.

## Assurance path

**Assurance path**: high-assurance — a pinned protected helper changes what it accepts.
