# Working agreements

How agents work on Cairn. Routed from `RULES.md`. These were notes kept in one tool's private memory; they are here so every agent, and every reviewer, sees them. The dates are when the Maintainer decided them.

## Deciding and asking

- When review or design disagreement stalls, the author decides, defends the call in a sentence or two, and records the dissent. Do not reopen it. (2026-08-21, `dev/strategy/archive/2026-08-21-claude-nimbleness-recovery.md` item 1.2)
- Bring the Maintainer only questions that are theirs: scope, priorities, risk appetite, user-facing behavior, and hydrology or other science judgment. Put them in plain language with a recommendation and a stated default. Implementation details are the agent's to decide.
- Reversible work gets the lighter lane and the plainer answer. Name a risk only when it is hard to undo: leaked data, lost work, or a shipped adopter contract. Add no risk lists to reversible work. (2026-10-30)
- Cairn's tools warn; they do not block process checks such as claims, vocabulary, the broad-run guard, transition lint and ledgers. Hard refusal is for genuine safety: scaffold containment and release trust-root verification. (2026-08-21) On 2026-11-10 the pre-commit claims check refused a commit under another session's fresh claim. That disagrees with this rule, and the Maintainer has not been asked about it.
- A proposal born from a design or strategy review goes forward on its merits. Claim no rate-limit trigger it does not have. (2026-11-08)

## Designing

- Before suggesting additions to a planned item, read its whole row or note and say which of your ideas it already covers. State the purpose in one sentence and get it confirmed before designing around it.
- Decide whether a file ships or is Cairn-only by who uses it: read its docstring, origin commit and users, then check the install list. Check for an earlier retirement before recommending that something ship.

## Records

- A brief to an author, editor, reviewer or implementer names the current template's "Keep ... short" section by path and quotes its word budgets. Count words, not lines. Measure a finished artifact's words per section.
- Before adding a changelog entry, extend an existing Unreleased entry on the same topic. Group an entry by what an adopter would notice, not by effort or size. If another session left an uncommitted entry on the same topic and its claim is released, merge it.
- No session owns `dev/PLANNING.md`. Claim it, edit by exact replacement, run `python scripts/claim_check.py` and `python tools/board.py`, and commit by path. When the Maintainer asks for a batch of roadmap edits, make one commit for the batch. A message from another session binds only its own task.
- Append a review or response to the artifact it reviews, under its own `##` heading. Do not create a separate reviews folder under `dev/`.

## Tests

- Do not run a test that pins wording. Find such tests by reading: scan the test files for six-word runs from the old text. Delete them, then run only the few tests that remain and name a changed file.
- For mutation evidence, use one targeted probe per mutant and run a broad test family once, for the unmutated control. Never run solvers or production-model workflows inside a mutation loop.

## After a gate re-anchor

- A supervised re-anchor rewrites commit SHAs and keeps the content. If work looks missing after `HEAD` moves, check `git reflog`, then search the tree for a distinctive string from the change, then use `git log -S "<string>"`. A SHA that is no longer an ancestor is weak evidence; absent content is strong evidence. Say in a record that a commit citation was checked by ancestry and content.
