# Plan: Narrow the heavy-tier trigger, say how a tier is lowered, add the Windows path line

**Source proposal**: dev/proposals/archive/2026-11-16-claude-heavy-tier-trigger.md
**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`, Medium), plan author
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: A change that only touches a risky file stops getting a Security Review it cannot use, only the Maintainer can lower a plan's tier, and one line warns Windows users that a file path can name a network share.

## Build summary

After this plan, every place that says when a change gets a Security Review says the same thing: heavy applies when a change alters what a named high-risk surface does or accepts, or adds or widens a place where outside input enters. Editing, moving or calling the surface does not, while the limits it was reviewed under stay the same; doubt about a limit goes to Security Review. The two collaboration guides and the lifecycle page also say that only the Maintainer lowers a tier. The two Security Review module copies gain a limits sentence and one Windows network-share sentence. All of it is exact prose replacement in 21 files (31 places) by a Low-tier agent on `0.8-dev`. No code, test or frozen file changes, so no re-anchor is owed.

## Source proposal

The accepted proposal (heavy tier; Maintainer, 2026-11-16: "Let's accept all five as revised") chose three changes. A: a narrowed trigger with a reviewed-limits clause, in 31 places. B: only the Maintainer lowers a tier, and the plan records the words, what lapses and what remains. C: one sentence that a path can name a network share (UNC/SMB). The one-line engine rule and the security-verification rule stay stricter; `link_check.py` stays with the adopter-defects proposal. This plan adds no other outcome.

Proposed paths:
- dev/proposals/archive/2026-11-16-claude-heavy-tier-trigger.md

## Scope

**Result.** The 31 places state one narrowed trigger. The three governing homes (`dev/agent_collaboration.md`, its shipped twin, `docs/methodology/lifecycle.md`) carry the full reviewed-limits rule and the lowering rule. The shorter places carry the trigger itself; the module copies carry the limits sentence and the Windows sentence. This delivers the Decision: fewer Security Reviews that cannot find anything, none lost where an input, a guard's data or a boundary changes.

**Branch.** Every chunk runs on `0.8-dev` (`dev/PLANNING.md` > "Branches for v0.8": shipped-file changes for groups 2 to 5 stay off `master`). The coordinator creates `0.8-dev` from `master` when group 1 closes; no chunk starts before it exists (restart condition: `git branch --list 0.8-dev` shows it). This plan is a document and may be committed on `master` now.

**Surfaces.** The 21 files in the places table. None is a path in the gate manifest (`bootstrap/tests/fixtures/gate_manifest.json`; exact-path check of every path string in it, measured at `19b2d666`), so none is frozen.

**Non-work**, each with its reason:
- The proposal-path rule (a change touching a high-risk surface needs a proposal): `lifecycle.md` line 45, `proposals.md` line 148, both session-start `SKILL.md` line 124, both dev-tour copies line 107, the figure's lane label (`three-lanes-of-change.svg` line 93). The Decision keeps it; a touching change still opens a proposal and may be light.
- The one-line engine rule (`dev/rules/protected-surfaces.md` lines 5-7) and the security-verification text (module and `templates/modules/default-on/` twin, `run_security_verification.py` line 308, `bootstrap/SAFETY.md`, `session.py` line 50): the Decision keeps them stricter.
- `docs/methodology/dual-review.md` line 197: a review posture, not a trigger.
- `scripts/link_check.py`, any code or test: item 8 of the adopter-defects proposal; a test edit would be a frozen-file edit.
- Re-tiering past proposals, Cairn's own `AGENTS.md` (no trigger line), `dev/.cairn/cairn-lock.yml` (tool-owned), size caps in the Windows line (#89): not asked for.
- The changelog entry, `dev/PLANNING.md`, archiving the proposal: the coordinator. The entry the proposal names ("Changed: Security Review triggers", `CHANGELOG.md` line 115) sits under the released 0.6.0 section, not Unreleased; the coordinator extends an Unreleased entry or asks.

**Reuse.** N/A: no code added. Search: `git grep -n -i "high-risk"` outside archives found only these 21 files, the left-alone places above, and three descriptive mentions (`docs/related-practices.md`, `docs/vision.md`, `docs/methodology/doc-governance.md`).

### Documentation / doctrine surface

Doctrine in `docs/methodology/` (lifecycle, dual-review, roles), governing text in the shipped `templates/core/AGENTS.md` and collaboration guide, deliberation and rules in `dev/`, summaries in `README.md` and `docs/`.

## Sequence

Estimate: 3 to 5 Low-tier agent-hours for C1 to C7, about one day (my planning guess, not measured). Uncertain: how often another session holds an uncommitted edit on a shared file (the chunk then waits). `scripts/link_check.py` failed to import once while I worked (`git-read-binding-failed`, with another session's uncommitted edit on `tools/git_read.py`) and imported again later; if it fails, record "not run" and the reason, and never edit the tool.

**Order among group 2.** This plan runs first, then the template scan, release tests, template trim, staged modules and scientific run evidence. Files shared (read from their proposals' Documentation sections at `19b2d666`): template scan (plan unwritten): `dev/rules/protected-surfaces.md`, both proposal `_template.md`, `docs/release-process.md`. Release tests shipped-only: `docs/release-process.md` (its first block, the strict-evidence section, one release-notes line; this plan edits one bullet near line 64). Template trim: both collaboration guides, both proposal templates, `templates/core/AGENTS.md`, possibly `dev/rules/protected-surfaces.md`. Staged modules, scientific run evidence: none. The trim must keep every rule here and re-measure word counts: C1 adds about 275 words to each guide (settled text: F 172 and B 129, against 28 removed).

**Every chunk.** A Low-tier implementer; name the model at spawn. Check `git branch --show-current` is `0.8-dev`; stop otherwise. Claim the exact paths (`python tools/intent.py claim`). Run `git status` and `git log -5 -- <chunk paths>`: stop on another session's uncommitted edit to any of them, and stop if an old fragment below no longer matches exactly; never improvise a new one. Edit by exact replacement: old text copied from the file, replace only that fragment, keep every other byte, do not rewrap, let a longer line run long. If an old fragment occurs twice in a file, extend it by the unchanged text after it on that line until it is unique, and keep that text in the new string. Edit no test, script, `dev/PLANNING.md` or `CHANGELOG.md`. Commit once per chunk with explicit paths, never push, ending the message with the co-author line. The message lists each place as `path: label`, `wc -w` before and after per file, and each check's result ("not run" where so).

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Governing homes: full rule and lowering rule | plan reviews accepted; `0.8-dev` exists | both collaboration guides, `lifecycle.md` (3 places) |
| C2 | Security Review module: limits sentence, Windows sentence | C1 | both `security-review.md` copies (2 places) |
| C3 | Proposal templates | C2 | both `_template.md` (7 places) |
| C4 | Shipped `AGENTS.md`, under the word cap | C3 | `templates/core/AGENTS.md` (1) |
| C5 | Obligation sentences | C4 | model-selection pair, `roles.md`, `protected-surfaces.md`, `dual-review.md` (5) |
| C6 | Published summaries | C5 | `README.md`, `docs/index.html`, `getting-started.md`, `release-process.md`, `glossary.md` (8) |
| C7 | Tour pair, figure, final sweep | C6 | both dev-tour copies, the figure (5) |

The chunks edit different files but state one rule, so run them in order, never in parallel. **Red until the re-anchor: none expected.** No chunk edits a frozen file, so no ceremony follows; C7 is last. The six-word-run scan of tests, scripts, tools and skills for the old text found no pinning test (measured; only the twin pairs and session-start `SKILL.md`, whose matches are unchanged text). If an implementer finds one, stop: editing it is a frozen-file edit that must join the next re-anchor (release tests shipped-only), and the plan returns to `revising-plan`. `python scripts/repin.py status` already shows 24 FROZEN-MODIFIED files and an engine pin owed from group 1; none is this plan's, and none of the 21 files may join them.

**Places** (lines at `19b2d666`; find the old fragment by text, not line).

| Chunk | Label | Files | n |
|---|---|---|---|
| C1 | F | `dev/agent_collaboration.md` 371; `templates/core/dev/agent_collaboration.md` 362 | 2 |
| C1 | F′ | `docs/methodology/lifecycle.md` 72-73 | 1 |
| C1 | B | not counted: insert after the tier paragraph in the guides; after `See dual-review.md for review caps and obligations.` in lifecycle | 3 |
| C2 | L | both `security-review.md`, after `exempt because the code looks familiar.` | 2 |
| C2 | W | not counted: end of the `File and path handling` bullet in both | 2 |
| C3 | T1, T2, T3 | `dev/proposals/_template.md` 133, 350, 545; `templates/core/dev/proposals/_template.md` 116, 313, 493 | 6 |
| C3 | T4 | `dev/proposals/_template.md` 473 (the shipped slot is empty, no twin) | 1 |
| C4 | A | `templates/core/AGENTS.md` 107 | 1 |
| C5 | R | `dev/modules/model-selection.md` and `templates/modules/team-gated/model-selection.md` 63-64; `docs/methodology/roles.md` 196-197 | 3 |
| C5 | P, D | `dev/rules/protected-surfaces.md` 16; `docs/methodology/dual-review.md` 281 | 2 |
| C6 | S1 | `README.md` 52-53, 55; `docs/index.html` 168, 170; `docs/release-process.md` 64-65 | 5 |
| C6 | S2 | `docs/getting-started.md` 30 | 1 |
| C6 | G1, G2 | `docs/glossary.md` 22-23, 83-84 | 2 |
| C7 | S3 | `dev/modules/onboarding/dev-tour.md` 92; `docs/dev-tour.md` 92 | 2 |
| C7 | S1 | `docs/assets/three-lanes-of-change.svg` 10-11, 31 | 2 |
| C7 | N | `docs/assets/three-lanes-of-change.svg` 126 | 1 |

**Settled text.** Each line is verbatim; `old` is the whole fragment to replace. `/` marks a line break and whatever begins the next line (an indent or `> `). Punctuation that follows an old fragment in the file stays.

```
S   Heavy applies when a change substantively alters the behavior or inputs of a named high-risk surface, or adds or widens a trust boundary

F1  Heavy applies when a change substantively alters the behavior or inputs of a named high-risk surface, or adds or widens a trust boundary (a place where outside input meets the system).
F2  Editing, moving, renaming or calling a surface does not by itself trigger heavy while the limits it was reviewed under stay the same: who supplies the data, what inputs are accepted, what validation runs before every protected operation, what the operation can do, and who can receive its output[ (the limits listed in `dev/modules/security-review.md`)].
F3  A change to any of them counts, even through an existing guard: a new untrusted source, or input moved from trusted-input (under repo control) to user-controlled (not authored by the Maintainer).
F4  Data a guard reads, such as gate fixtures, oracles, policy files and manifests, is an input: editing it counts.
F5  A reviewer names which limit, if any, changed.
F6  Doubt about a limit, or an assumption the reviewer cannot name, resolves to Security Review; ordinary uncertainty elsewhere takes the lighter lane, with the reason.
F7  A newly found boundary still stops work for reassessment.

F   old: Named high-risk surfaces and added or widened trust boundaries trigger heavy; a newly found boundary stops work for reassessment. Ordinary uncertainty takes the lighter lane, with the reason.
    new: F1 to F7 joined by single spaces. In `dev/agent_collaboration.md` keep the bracketed text in F2 without its square brackets; in the shipped guide drop it.
F′  old: Named / high-risk surfaces and added or widened trust boundaries trigger heavy.
    new: F1 to F5, then: Doubt about a limit, or an assumption the reviewer cannot name, resolves to Security Review.  (no bracket)

B   **Lowering a tier.** Only the Maintainer lowers a tier, in chat or a Decision; an author or reviewer may recommend it. The plan records it in one appended `Plan change`: the Maintainer's words verbatim with their source, the cancelled chunks, the obligations that lapse (those whose only source was a cancelled chunk, such as a Security Review of code no longer written) and those that remain (fences, Maintainer-reserved steps, model floors, anything tied to a remaining chunk), the new header values, and that the remaining scope does not alter a high-risk surface or widen a boundary. A review already held stays valid for the scope it covered and transfers to nothing else. A raise follows the same pattern. The amendment review checks the lapse list against the cancelled chunks.

L   The heavy-tier narrowing reaches no further than these limits: editing, moving or calling a guard drops out of Security Review only when none of them changes, and doubt about one resolves to Security Review.
W   On Windows, a `file:` URL or a path taken from a manifest or argument can name a network share (`\\host\share`, `//host/share` or `\\?\UNC\`), and any resolve, stat, existence test or open of it reaches that host over SMB and answers its login challenge with a response computed from the user's credentials (crackable or relayable, though not the hash itself); refuse such a path after normalizing and before any of those, because normalizing does not remove the host, and do not count an HTTP-level guard as a network guard.

T1  old: **A high-risk surface takes a Security Review.**
    new: **A change that substantively alters the behavior or inputs of a high-risk surface, or adds or widens a trust boundary, takes a Security Review.**
T2  old: or one that touches a
    new: or one that substantively alters the behavior or inputs of a
T3  old: named high-risk or added/widened boundaries require heavy.
    new: a substantive change to a named high-risk surface's behavior or inputs, or an added or widened boundary, requires heavy.
T4  old: each already a Security-Review trigger:
    new: each a Security-Review trigger when a change alters it, per the heavy-tier rule:
A   old: High-risk surfaces and added or widened trust boundaries require
    new: High-risk surface behavior or input changes, or added or widened trust boundaries, require
R   old: it also owes the Security Review / that surface already requires, at high.
    new: it also owes any Security Review / the heavy-tier rule requires for that edit, at high.
P   old: surfaces retain their proposal and Security Review obligations.
    new: surfaces retain their proposal obligation. They owe a Security Review where the heavy-tier rule (`dev/agent_collaboration.md` > "Review rules"), the one-line engine rule above, or `dev/modules/security-verification.md` requires one.
D   old: A high-risk surface named in `AGENTS.md` takes
    new: A change that substantively alters the behavior or inputs of a high-risk surface named in `AGENTS.md`, or adds or widens a trust boundary, takes
S1  old: Named high-risk surfaces and added or widened trust boundaries trigger heavy   new: S
    (a line break may fall between any two words in `README.md` 52-53, `docs/release-process.md` 64-65 and the figure's comment; `README.md` 53 follows it with a colon)
S2  old: Heavy is triggered by named high-risk surfaces and widened trust boundaries   new: S
S3  old: Named high-risk surfaces and widened trust boundaries trigger it   new: S
G1  old: Heavy adds Security Review; high-risk / surfaces and widened trust boundaries trigger it
    new: Heavy adds Security Review. S
G2  old: triggered by named high-risk surfaces rather than by / size.
    new: triggered by a substantive change to a named high-risk surface's behavior or inputs, or an added or widened trust boundary, rather than by / size.
N   old: Heavy adds Security Review; high-risk surfaces and new/widened boundaries trigger it.
    new: Heavy adds Security Review; high-risk behavior, input or boundary changes trigger it.
```

B is its own paragraph (blank line before and after): one line in the guides, wrapped at 80 columns in lifecycle. L goes on new lines, wrapped at 80, directly after the line ending `exempt because the code looks familiar.`; W goes on new lines, wrapped at 80 and indented two spaces, after `(escaping the intended directory)?`. Both security-review copies get the same text. In `model-selection.md` keep each line's `> ` prefix. A is short because the installed `AGENTS.md` has 5 words of room (C4); the full rule lives in the guide of every install.

## Acceptance criteria

**C1 (F, F′, B).** Each of the three places holds its settled text, whitespace-collapsed equal; B appears once in each of the three files. `git grep -c -F "Only the Maintainer lowers a tier, in chat or a Decision; an author or reviewer may recommend it."` gives 1 for each, and no other added sentence lets an author, reviewer or `Plan change` lower a tier. Lifecycle still holds `If an agent discovers a new boundary, it stops and reports it for reassessment.` and `No agent raises a tier on its own.` The two guides' F text matches word for word except F2's bracket. The commit message records the guides' word counts (expected about +275 each) for the template-trim plan. The selector's tests that read these files pass.

**C2 (L, W).** Both copies hold L once and W once. W is one sentence and contains `\\host\share`, `//host/share`, `\\?\UNC\`, `after normalizing and before any of those`, `not the hash itself` and `HTTP-level guard` (`git grep -c -F` gives 1 per fragment per file). The two copies still differ only where they did: `diff dev/modules/security-review.md templates/modules/team-gated/security-review.md` shows the same four hunks as before the edit (measured: line 1, the two-pass-cap paragraph as two hunks, the provenance bullet near line 194), and none in the added lines. `python scripts/check_cairn.py` on both reports no content-scan flag (I scanned W, F and B alone as a templates-class file with URL flagging on and off; nothing raised); if it flags, stop and report, adding no `cairn-accept` marker.

**C3 (T1 to T4).** Seven places hold their settled text. The shipped template's diff touches no line inside a `cairn:slot` block. Every other line of both files is unchanged, and the old fragments `or one that touches a` and `A high-risk surface takes a Security Review` are gone from both. The selector's tests pass, including `test_loop_fidelity_gate.py`, `test_review_stance_in_shipped_files.py` and `test_board_json_contract.py` where selected. Record both files' word counts.

**C4 (A).** One place holds A. The installed total of `AGENTS.md`, `VENDOR.md` and `RULES.md` is at most 1,500 words: `test_full_install_seeds_rules_md_within_word_budget` in `bootstrap/tests/test_scaffold.py` passes; measured before, 1,495 (a scratch install, same steps as the test), expected after 1,499. If the total would pass 1,500, stop; do not shorten other words. Cairn's own `AGENTS.md` is unchanged. After C4 is committed, run the selector as `python tools/test_tiers.py for --range <C3 commit>..HEAD templates/core/AGENTS.md` (it refuses an `AGENTS.md` path without a range).

**C5 (R, P, D).** Five places hold their settled text. The model-selection pair stays byte-identical (`cmp`; `test_the_model_selection_pair_is_byte_identical`), and `roles.md` reads as the module does once `> ` prefixes are removed. `dev/rules/protected-surfaces.md` diff is one hunk, at the last sentence of its first paragraph; lines 5-7 are unchanged word for word. `docs/methodology/dual-review.md` diff is one hunk at line 281.

**C6 (S1, S2, G1, G2).** Eight places hold their settled text. S appears, whitespace-collapsed, at the five S1 places and at `getting-started.md`; `docs/index.html` still parses as HTML (`python -c` with `html.parser`, no error) and S contains no quote or `<`. Each alt text keeps its unchanged tail (`Ordinary uncertainty takes the lighter lane with a reason; stop on a newly discovered trust boundary.` or the shorter forms already there). Glossary still reads `A new boundary stops work` after G1.

**C7 (S3, S1, N, sweep).** `cmp dev/modules/onboarding/dev-tour.md docs/dev-tour.md` is identical and `test_an_installed_onboarding_copy_equals_its_page` passes. The figure parses as XML, keeps its viewBox, and the lane label at line 93 is unchanged. N is 85 characters; measured in the Browser pane it is 618 px wide against 633 px for the line it replaces, in a 700-wide figure. Then the sweep (Verification), whose results go in the commit message.

## Scope delta

**Scope delta**: preserved

Readings the plan makes where the proposal is silent, for the plan review to confirm (none removes an outcome):
- "Replace each of the 31 places with this meaning": the three governing homes carry the full clause and doubt rule, the two module copies carry L, and the other 26 places state the narrowed trigger only, because alt text, a figure note and a 5-word `AGENTS.md` margin cannot hold a 170-word clause. The clause at every place would be new scope, for the Maintainer.
- Section A reads "does not by itself, when the limits ... stay the same", with no verb; F2 supplies "trigger heavy".
- The proposal counts one place per `security-review.md` copy without naming it; the plan reads it as L (the module "gains one sentence" beside its "not widening" paragraph). W is part C, not in the 31.
- The shipped guide and lifecycle define trusted-input and user-controlled inline (F3); the module is team-gated and may be absent.

## Verification

Promises: what an agent reads decides whether a change gets a Security Review (the guides, lifecycle, the templates), and that only the Maintainer lowers a tier. Entry points: those texts. Checks below, per chunk, on the chunk's files; everything uses `/Users/kendal30/conda_envs/lhm/bin/python3.13`.

1. **Exact text.** `git diff -U0` per file shows only the old fragments removed and the settled text added (line breaks collapsed). Anything else removed: revert that hunk and stop.
2. **Gates on each edited document.** `python scripts/claim_check.py <file>` (no hard flag), `python scripts/link_check.py <file>`, `python scripts/sync_doc_snippets.py --check <file>`, `python scripts/check_cairn.py <file>`, each on the chunk's `.md` files, and once per chunk `python scripts/quality_gate.py --sub neutrality`. Baseline: `sync_doc_snippets.py --check` passed on the whole tree at `0f85f3e8`.
3. **Tests.** `python tools/test_tiers.py for <chunk paths>` (40 files for the 20 non-`AGENTS.md` paths together, measured), run with `-m pytest`; nothing wider. Run the set before the edit and after. A test red both times with the same failure belongs to another plan (group 1's pending re-anchor leaves some gate tests red; `repin.py status` shows why): record it and go on. A test red only after the edit stops the chunk.
4. **Final sweep (C7).** (a) This returns no line:

```
git grep -n -E "Named high-risk|triggered by named high-risk surfaces|high-risk surfaces and (added or )?widened trust boundaries|high-risk surfaces and new/widened boundaries|named high-risk or added/widened|already a Security-Review trigger|A high-risk surface takes a Security Review|it also owes the Security Review|retain their proposal and Security Review obligations|A high-risk surface named in .AGENTS.md. takes|High-risk surfaces and added or widened|widened trust boundaries trigger it|or one that touches a" -- . ':!dev/proposals/2026-*' ':!dev/proposals/archive' ':!dev/plans' ':!*/archive/*' ':!CHANGELOG.md' ':!dev/reflections' ':!dev/PLANNING.md' ':!dev/strategy' ':!dev/measurement'
```

It returned 29 lines in 19 files at `19b2d666`; the two other places are the L insertions. (b) Each of the 31 places holds its settled text (collapse whitespace in the file, strip `> `, test the new text occurs). (c) `git diff --name-only <C1 parent>..HEAD` lists only the 21 files. (d) `python scripts/repin.py status` lists none of the 21 files under FROZEN-MODIFIED, and its list matches the one before C1 apart from other sessions' files.

**Does any rule weaken or disappear?** Yes, deliberately, as the proposal says: (1) "touches a high-risk surface" as a heavy trigger, at 24 places; (2) the surface-based Security Review obligation, at 5 (P, R three times, T4). Kept and not edited: the Maintainer sets the tier, a newly found boundary stops work (F7, lifecycle, G1, the alt texts), the two-pass cap, fences, the proposal-path rule, the one-line engine rule, the security-verification rule. Labels: F, F′, S1 to S3, G1, G2, N, T1 to T3, A and D are (1); P, R and T4 are (2); B, L and W add rules and remove none. The commit message records each place's label and that check 1 passed for it. Check 1 shows each hunk is exactly the settled text, so the implementer makes no weakening judgment; the reviews do.

**Security preflight S2, S3.** The negative control is the sweep: restore one old fragment in a scratch copy and check (a) must return that line. The gate that fires is the sweep plus `check_cairn.py`.

**Reviews after implementation.** Code review (fresh, Medium) and a Security Review (High) on the proposal's questions (a) to (e), applying its worked cases and the #62 case to F. Signals the change is wrong are the proposal's. Not run by this plan: Windows behavior, a whole-suite run.

Length (counted by script before this paragraph): Build summary 130, Source proposal 83, Scope 389, Sequence 1,921, Scope delta 165, Verification 577; Acceptance 597 across seven chunks (58 to 127 each, under 150). The opening body runs about 3,270 words against the 1,000 target. The overrun is exact text a Low-tier implementer must not have to decide: the settled text (about 940 words), the places table (about 240) and the sweep command (about 75). I cut repeatable prose first and cut no exact text.

## Plan review -- Claude Sonnet 5.5 (Plan Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: 443ae6e21c773d262017c9e5e9ca703b5ac87293
```

**Obligation**: Clear that a Low-tier implementer can run every chunk with no design left to them; that the plan delivers every outcome the 2026-11-16 Decision adopted; that no rule weakens or disappears except as the Decision narrows the trigger; and that the order, ownership and ceremony statements are true.
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 9 minutes (15:53 to 16:02, measured with `date`)
**Tokens**: unknown

Conclusion: two blocking findings; the plan is otherwise tight. Steelman: 29 of 31 places carry exact old and new text, a sweep finds every old place, and a word-cap stop and a branch gate leave a Low-tier agent little to decide.

**Foundations**

1. **Should this happen as framed?** Yes for the narrowed trigger, the lowering rule and the Windows line; not for the "preserved" label, because 26 of 31 places hold only the short trigger while the Decision names the reviewed-limits clause "across 31 places" -- proposal lines 39 and 237, plan lines 155-158.
2. **Best alternative.** Four chunks (C1+C2, C3 to C5, C6+C7) would do: all 29 old fragments match once per place and the sweep prints 29 lines in 19 files, so seven chunks add claims, test runs and commits, not safety -- my whitespace-tolerant match script and the plan's sweep, run at the reviewed commit.
3. **What would show it wrong.** C1's own check failing at lifecycle (finding 2), a sweep line left after C7, or `repin.py status` listing one of the 21 files; none is present now (24 FROZEN-MODIFIED, none of the 21) -- `python scripts/repin.py status`.

**Findings**

1. **Blocking, needs the Maintainer's allowance (C3 to C7).** "Scope delta: preserved" cannot stand. Proposal A says "Replace each of the 31 places with this meaning", and that meaning includes "doubt resolves to Security Review" and "guard data counts". Only the two guides, lifecycle and the module copies carry them. T1 to T3, R and D carry the short trigger with no pointer, so an author reading T1 could decide a fixture edit is not heavy. An author or reviewer cannot concede this (plan template, "Scope delta"). Closes: the Maintainer's quoted allowance with the label `degraded`, or a pointer to `dev/agent_collaboration.md` > "Review rules" at T1 to T3, R and D (A has 1 word of room; its line 43 already points there). The plan's other noted gaps stay inside the Decision: the Decision summary supplies the verb ("does not by itself trigger it", proposal line 15); L is the module sentence the proposal asks for; the figure's line 93 is already named in Non-work; CHANGELOG line 115 sits in 0.6.0 (lines 107-157) and Unreleased holds no such entry, so the coordinator adds a new entry or asks.
2. **Blocking, C1: two checks cannot pass as written.** B wraps at 80 columns in lifecycle, so its first sentence breaks after "Decision;" (78 characters; " an" makes 81) and `git grep -c -F` of the whole sentence gives 0 there. The anchor `See dual-review.md for review caps and obligations.` omits the backticks the file has. Missing decision: how lifecycle's B is found and checked. Closes: a whitespace-collapsed check for lifecycle and the exact anchor.
3. **Non-blocking, ownership.** `dev/agent_collaboration.md`, `dev/proposals/_template.md`, `dev/modules/security-review.md` and `dev/modules/model-selection.md` are lock-tracked. Group 1 plans and the trim plan's last chunk run a scoped `upgrade --finalize` and commit the lock alone (`0f85f3e8`, `39526388`). This plan files the lock under "not asked for". Name an owner (C7 or the coordinator).
4. **Non-blocking, plain language.** W is one 88-word sentence (rule 7) and never spells out SMB (rule 5). The Decision says one sentence, so splitting it is the Maintainer's call.
5. **Non-blocking, stale list.** The trim plan edits no `templates/core/AGENTS.md` and appends moved text to `dual-review.md` (this plan's D place). The order holds, and "Every chunk" re-reads `git status` and `git log -5`.
6. **Non-blocking.** F′ leaves lifecycle's "Ordinary uncertainty takes the lighter lane" without "elsewhere"; add the word.

**Does any rule weaken or disappear?** Only as the Decision narrows it: 24 places lose "touches a surface" as a heavy trigger and 5 lose the surface-based obligation (labels recounted: 24 and 5). Kept: lifecycle's "No agent raises a tier on its own" (line 77) and proposal-path rule (line 45); P keeps the one-line engine rule and security-verification; B adds a rule, and a grep found no text that lets an author or reviewer lower a tier today. The guides and lifecycle keep new suppliers, guard data and doubt at heavy; the short places omit them (finding 1).

**Coverage**: measured the word cap with a scratch install (1,125 + 310 + 60 = 1,495; A adds 4 words for 1,499, so the short form is not weaker than S); a 4-word scan of 320 tracked code and data files found no wording pin; 21 paths are not exact in the gate manifest; the selector lists 40 files. Not covered: the Security question (the High-tier Security Review owns it), Windows behavior and W's accuracy, `check_cairn.py` on W, N's pixel width, running any test or edit. Over target (about 850 words against 300): six findings, two of them blocking, each need their line evidence.
