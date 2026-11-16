# Ship a rule against committing secrets

**Author**: Claude Opus 5.5 (`claude-opus-5-5`), Strategy
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: light — one sentence in two always-loaded files and no code; it edits `AGENTS.md`, a named high-risk surface, so it keeps a Security Review (the Maintainer sets the tier)
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-16
**In brief**: Every agent working in a Cairn project would read, every session, that it must never commit a credential or private data, and what to do if one is committed.

## Decision summary

No file an adopter's agent loads every session tells it not to commit secrets. The gap was found by the Security Review of the run-and-development-rules draft (`1a47ea4b`), which noted it is older than that draft; the board's group 1 row "Ship a rule against committing secrets" records it. Cairn's release secrets scan finds a secret only after it is in history, and only at Cairn's own release.

Proposed: one sentence in the shipped `AGENTS.md` and one bright line in Cairn's own `RULES.md`. Cost: about 30 words in each file. The shipped files have 5 words of room under their 1,500-word cap today, so the shipped sentence lands after the template-trim plan frees room. The Maintainer placed it on `0.8-dev` on 2026-11-16: "Go ahead and draft it, and we can put it in 0.8-dev".

## Context

Measured at `3bdfffd8`:

- Searched for a rule against committing secrets, credentials, tokens or keys in `templates/core/AGENTS.md`, `templates/core/RULES.md`, `templates/core/VENDOR.md`, the shipped skills and `templates/core/dev/agent_collaboration.md`, and in Cairn's own `AGENTS.md`, `RULES.md` and `dev/rules/`. None found. The only nearby text says the local next-session note is never committed.
- Word counts (`wc -w`): the shipped `AGENTS.md`, `VENDOR.md` and `RULES.md` total 1,495, against the 1,500 cap that `bootstrap/tests/test_scaffold.py` holds. Cairn's own three total 1,488, against its 2,000 cap.
- Neither `templates/core/AGENTS.md` nor Cairn's `AGENTS.md` or `RULES.md` is in `frozen_files` of `bootstrap/tests/fixtures/gate_manifest.json`, so no re-anchor follows.
- The accepted template-trim proposal rewrites the shipped `AGENTS.md`, and its plan (`dev/plans/2026-11-16-template-trim-and-rules.md`) is in plan review.

## Proposal

1. **Shipped `AGENTS.md`**, section "Working tree and commits", after the sentence on explicit paths, add:

   > Never commit a credential, key, token or private data. If one is committed, stop and tell the person: history keeps it, so it must be revoked, not just deleted.

2. **Cairn's own `RULES.md`**, under "Bright lines", add the same rule as one bullet.
3. **Order.** Both land on `0.8-dev`. The shipped sentence lands after the template-trim plan's edits to the shipped `AGENTS.md`, written against the trimmed text, and within that plan's word budget. Cairn's `RULES.md` line can land as soon as `0.8-dev` exists.
4. **What "private data" means** is left to each project's rules (unpublished data, personal information). The sentence names the category; it does not define it.
5. **Not proposed:** a commit-time scanner, a hook or a new check. The release scan stays as it is. A rule an agent reads every session is the cheapest earlier guard.

## Rationale

A secret in Git history cannot be removed by a later commit, and pushing publishes it. The fix after the fact is to revoke and replace it, which needs the person. So the agent's two duties are to not commit one and to stop and say so if it did.

## Alternatives considered

- **A commit-time scan.** Stronger, but a new tool on every commit; Cairn's tools warn and do not block process checks, and a scan cannot know what counts as private data. Revisit if a secret is ever committed.
- **Only Cairn's `RULES.md`.** Leaves every adopter without the rule.
- **Do nothing.** Relies on each agent's general caution.

## Documentation / doctrine surface

`templates/core/AGENTS.md` (governing text shipped to adopters) and Cairn's `RULES.md` (project rule). One `CHANGELOG.md` entry, Added. Adopters receive the sentence through the upgrade's three-way merge of `AGENTS.md`; a filled slot is not touched.

## Evidence / verification plan

### Tests required

No new test: Cairn does not pin rule wording. Run the tests that name the changed files (`python tools/test_tiers.py for templates/core/AGENTS.md RULES.md`), including the 1,500-word cap check in `bootstrap/tests/test_scaffold.py`, which must still pass after the trim. `scripts/claim_check.py` on both files.

### Security preflight

- S1: no new input; the change is text an agent reads.
- S2: it can fail only by being absent or by being cut later; the trim plan's rule ledger must list it as kept.
- S3: it applies to every commit an agent makes.
- S4: on doubt, the agent stops and asks; it never grants authority.
- S5: it does not replace the release secrets scan.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A secret or private data reaches a commit in a project that has the rule; or the sentence is cut in a later trim.

## Scope delta

N/A: opening proposal.

## Assurance path

**Assurance path**: standard. A named high-risk surface changes, so the Security Review checks that the sentence adds a duty and weakens nothing. No re-anchor follows.

## Decision -- Maintainer (scribed by Claude Opus 5.5) -- 2026-11-16

**Tier**: light

**ACCEPTED, to be implemented now.** After reading the draft, the Maintainer said in chat:

> "This is it? Yeah, just take care of it now."

Read with the Maintainer's earlier words on this row ("we can put it in 0.8-dev"), "now" means implement it immediately rather than wait for the template-trim plan. Because `0.8-dev` does not exist yet and this is a group 1 row, it lands on `master`. To fit under the 1,500-word shipped cap, the shipped sentence is shortened, and the room is freed from the explanatory comment in `templates/core/VENDOR.md`, which the trim plan replaces in full. The proposal's usual review and Security Review were not run before acceptance; the Security Review of the implementing commit still runs and is appended here.

**Elapsed:** under 1 minute. **Tokens:** unknown.

## Implementation verification -- Claude Opus 5.5 -- 2026-11-16

**Elapsed**: about 15 minutes. **Tokens**: unknown.

Implemented on `master` in the commit that adds this section, by exact replacement:
- `templates/core/AGENTS.md`, "Working tree and commits": "Never commit a credential, key, token or private data; if one is committed, stop and tell the person, because history keeps it." (22 words; shortened from the draft's 29 to fit the cap).
- `templates/core/VENDOR.md`: the explanatory HTML comment after `@AGENTS.md` shortened by 20 words to make room. The template-trim plan replaces this file in full, so its own text is unaffected.
- Cairn's `RULES.md`: the same rule as a bright line, telling the Maintainer.
- `CHANGELOG.md`: one Major "Added" entry.

Word counts (`wc -w`): shipped `AGENTS.md`, `VENDOR.md` and `RULES.md` 1,495 to 1,497, under the 1,500 cap; Cairn's three 1,488 to 1,511, under 2,000.

Checks, as the prose-only rule in `dev/agent_collaboration.md` (line 471) sets them, under `/Users/kendal30/conda_envs/lhm/bin/python3.13`: claim check on all four files, OK; link check, OK; snippet check, no drift; neutrality, 2 failures, both in `templates/skills/_lib/meter.py`, another session's uncommitted work, none in these files; the one test that reads the shipped files' word count (`test_full_install_seeds_rules_md_within_word_budget`), passed. No test pins this text. A selector-driven run of eight install and upgrade test files was started and stopped: those tests name the files but do not read the changed text.

Not run: the Security Review of this commit, which follows; Windows.
