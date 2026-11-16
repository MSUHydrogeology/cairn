# Plan: Narrow the heavy-tier trigger, say how a tier is lowered, add the Windows path line

**Source proposal**: dev/proposals/archive/2026-11-16-claude-heavy-tier-trigger.md
**Author**: Claude Sonnet 5.5 (`claude-sonnet-5-5`, Medium), plan author
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: A change that only touches a risky file stops getting a Security Review it cannot use, only the Maintainer can lower a plan's tier, and one line warns Windows users that a file path can name a network share.

## Build summary

After this plan, every place that says when a change gets a Security Review says the same short thing: a change gets the heavy tier when it alters what a high-risk surface does or accepts, or adds a place where outside input meets the system, and merely touching a surface does not. When in doubt, take the Security Review; stricter project rules still apply. The guides, the lifecycle page and most other places carry that rule in the same words; the four picture descriptions carry its first two sentences; `AGENTS.md` (word cap) and one figure note (drawing width) carry a compressed line; a place where an author picks a tier always says how doubt resolves. The guides and lifecycle also say that only the Maintainer lowers a tier, and the two Security Review module copies gain a limits sentence and one Windows network-share sentence. All of it is exact prose replacement in 21 files (31 places) by a Low-tier agent on `0.8-dev`. No code, test or frozen file changes, so no re-anchor is owed.

## Source proposal

The accepted proposal (heavy tier; Maintainer, 2026-11-16: "Let's accept all five as revised") chose three changes. A: a narrowed trigger in 31 places, with a reviewed-limits clause that the Maintainer later replaced by one short rule (Scope delta). B: only the Maintainer lowers a tier, and the plan records the words, what lapses and what remains. C: one sentence that a path can name a network share (UNC/SMB). The one-line engine rule and the security-verification rule stay stricter; `link_check.py` stays with the adopter-defects proposal. This plan adds no other outcome.

Proposed paths:
- dev/proposals/archive/2026-11-16-claude-heavy-tier-trigger.md

## Scope

**Result.** The 31 places state one narrowed trigger in the same words: the short rule (RC, RG, RT below; about 50 words) at 15 places; its first two sentences (R1) at the four picture descriptions; the trigger in each place's own grammar at 8 places, all but G2 with the doubt sentence and a pointer; a compressed line in `AGENTS.md` and in the figure note; and the limits sentence (L) in the two module copies. The guides and lifecycle also carry the lowering rule, the module copies the Windows sentence. That is less than the Decision's reviewed-limits clause; Scope delta records it with the Maintainer's allowance. Otherwise this delivers the Decision: fewer Security Reviews that cannot find anything, and doubt still goes to Security Review.

**Branch.** Every chunk runs on `0.8-dev` (`dev/PLANNING.md` > "Branches for v0.8": shipped-file changes for groups 2 to 5 stay off `master`). The coordinator creates `0.8-dev` from `master` when group 1 closes; no chunk starts before it exists (restart condition: `git branch --list 0.8-dev` shows it). This plan is a document and may be committed on `master` now.

**Surfaces.** The 21 files in the places table. None is a path in the gate manifest (`bootstrap/tests/fixtures/gate_manifest.json`; exact-path check of every path string in it, measured at `19b2d666`), so none is frozen; nor is `dev/.cairn/cairn-lock.yml` (same check).

**Non-work**, each with its reason:
- The proposal-path rule (a change touching a high-risk surface needs a proposal): `lifecycle.md` line 45, `proposals.md` line 148, both session-start `SKILL.md` line 124, both dev-tour copies line 107, the figure's lane label (`three-lanes-of-change.svg` line 93). The Decision keeps it; a touching change still opens a proposal and may be light.
- The one-line engine rule (`dev/rules/protected-surfaces.md` lines 5-7) and the security-verification text (module and `templates/modules/default-on/` twin, `run_security_verification.py` line 308, `bootstrap/SAFETY.md`, `session.py` line 50): the Decision keeps them stricter.
- `docs/methodology/dual-review.md` line 197: a review posture, not a trigger.
- `scripts/link_check.py`, any code or test: item 8 of the adopter-defects proposal; a test edit would be a frozen-file edit.
- Re-tiering past proposals, Cairn's own `AGENTS.md` (no trigger line), size caps in the Windows line (#89): not asked for. `dev/.cairn/cairn-lock.yml` is never edited by hand; C7 records the four lock-tracked files this plan changes with a scoped `upgrade --finalize`.
- The changelog entry, `dev/PLANNING.md`, archiving the proposal: the coordinator. The entry the proposal names (`CHANGELOG.md` line 115) sits under the released 0.6.0 section, not Unreleased; the coordinator extends an Unreleased entry or asks.

**Reuse.** N/A: no code added. Search: `git grep -n -i "high-risk"` outside archives found only these 21 files, the left-alone places above, and three descriptive mentions (`docs/related-practices.md`, `docs/vision.md`, `docs/methodology/doc-governance.md`).

### Documentation / doctrine surface

Doctrine in `docs/methodology/` (lifecycle, dual-review, roles), governing text in the shipped `templates/core/AGENTS.md` and collaboration guide, deliberation and rules in `dev/`, summaries in `README.md` and `docs/`.

## Sequence

Estimate: 3 to 5 Low-tier agent-hours for C1 to C7, about one day (my planning guess, not measured). Uncertain: how often another session holds an uncommitted edit on a shared file (the chunk then waits). If `scripts/link_check.py` fails to import (`git-read-binding-failed`, seen once with another session's uncommitted edit on `tools/git_read.py`), record "not run" and the reason; never edit the tool.

**Order among group 2.** This plan runs first, then the template scan, release tests, template trim, staged modules and scientific run evidence. Files shared (read from their proposals' Documentation sections at `19b2d666`): template scan (plan unwritten): `dev/rules/protected-surfaces.md`, both proposal `_template.md`, `docs/release-process.md`. Release tests shipped-only: `docs/release-process.md` (the strict-evidence section and one release-notes line; its first block is non-work there; this plan edits one bullet near line 64). Template trim: both collaboration guides, both proposal templates, `docs/methodology/dual-review.md` (it appends moved text), `templates/core/VENDOR.md` (it shares the 1,500-word cap with `templates/core/AGENTS.md`; the trim edits no `AGENTS.md`), possibly `dev/rules/protected-surfaces.md`. Staged modules, scientific run evidence: none. The trim must keep every rule here and re-measure word counts: C1 adds about 170 words to Cairn's guide and 169 to the shipped one (measured by script: the rule and its tail 69 and 68, B 129, against 28 removed).

**Every chunk.** A Low-tier implementer; name the model at spawn. Check `git branch --show-current` is `0.8-dev`; stop otherwise. Claim the exact paths (`python tools/intent.py claim`). Run `git status` and `git log -5 -- <chunk paths>`: stop on another session's uncommitted edit to any of them, and stop if an old fragment below no longer matches exactly; never improvise a new one. Edit by exact replacement: old text copied from the file, replace only that fragment, keep every other byte, do not rewrap, let a longer line run long. If an old fragment occurs twice in a file, extend it by the unchanged text after it on that line until it is unique, and keep that text in the new string. Edit no test, script, `dev/PLANNING.md` or `CHANGELOG.md`. Commit once per chunk with explicit paths (C7 also commits the lock alone, last), never push, ending the message with the co-author line. The message lists each place as `path: label`, `wc -w` before and after per file, and each check's result ("not run" where so).

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Governing homes: the rule and the lowering rule | plan reviews accepted; `0.8-dev` exists | both collaboration guides, `lifecycle.md` (3 places) |
| C2 | Security Review module: limits sentence, Windows sentence | C1 | both `security-review.md` copies (2 places) |
| C3 | Proposal templates | C2 | both `_template.md` (7 places) |
| C4 | Shipped `AGENTS.md`, under the word cap | C3 | `templates/core/AGENTS.md` (1) |
| C5 | Obligation sentences | C4 | model-selection pair, `roles.md`, `protected-surfaces.md`, `dual-review.md` (5) |
| C6 | Published summaries | C5 | `README.md`, `docs/index.html`, `getting-started.md`, `release-process.md`, `glossary.md` (8) |
| C7 | Tour pair, figure, final sweep, lock record | C6 | both dev-tour copies, the figure (5); then the lock |

The chunks state one rule, so run them in order, never in parallel. No chunk edits a frozen file, so no re-anchor follows (`python scripts/repin.py status` already shows 24 FROZEN-MODIFIED files and an engine pin owed from group 1; none is this plan's, and none of the 21 files may join them). A six-word-run scan of tests, scripts, tools and skills for the old text found no pinning test (measured; only the twin pairs and session-start `SKILL.md`, whose matches are unchanged text). If an implementer finds one, stop: editing it is a frozen-file edit that must join the next re-anchor, and the plan returns to `revising-plan`.

**Places** (lines at `19b2d666`; find the old fragment by text, not line). A name in the New column is defined in the block below the table; a name followed by text is joined to it by a single space. `/` marks a line break and whatever begins the next line (an indent or `> `). Punctuation that follows an old fragment in the file stays.

| Chunk | Label | Files | Old fragment (replace whole) | New | n |
|---|---|---|---|---|---|
| C1 | F | `dev/agent_collaboration.md` 371 | `Named high-risk surfaces and added or widened trust boundaries trigger heavy; a newly found boundary stops work for reassessment. Ordinary uncertainty takes the lighter lane, with the reason.` | RC TAIL | 1 |
| C1 | F | `templates/core/dev/agent_collaboration.md` 362 | the same | RG TAIL | 1 |
| C1 | F′ | `docs/methodology/lifecycle.md` 72-73 | `Named / high-risk surfaces and added or widened trust boundaries trigger heavy.` | RG | 1 |
| C1 | F′b | lifecycle line 75 | `Ordinary uncertainty` (once) | `Ordinary uncertainty elsewhere` | 0 |
| C1 | B | insert as its own paragraph after the tier paragraph in both guides, and after ``See `dual-review.md` for review caps and obligations.`` in lifecycle | none | B | not counted |
| C2 | L | both `security-review.md`, new lines after `exempt because the code looks familiar.` | none | L | 2 |
| C2 | W | both, end of the `File and path handling` bullet, after `(escaping the intended directory)?` | none | W | not counted |
| C3 | T1 | `dev/proposals/_template.md` 133; `templates/core/dev/proposals/_template.md` 116 | `**A high-risk surface takes a Security Review.**` | RT | 2 |
| C3 | T2 | the same files, 350; 313 | `or one that touches a / high-risk surface this project's `AGENTS.md` names.` | `or one that alters what a / high-risk surface this project's `AGENTS.md` names does or accepts. DP` | 2 |
| C3 | T3 | the same files, 545; 493 | `size; / named high-risk or added/widened boundaries require heavy.` | `size. RT` | 2 |
| C3 | T4 | `dev/proposals/_template.md` 473 (the shipped slot is empty, no twin) | `each already a Security-Review trigger:` | `each a Security-Review trigger when a change alters what it does or accepts DI:` | 1 |
| C4 | A | `templates/core/AGENTS.md` 107 | `High-risk surfaces and added or widened trust boundaries require / heavy review.` | `High-risk surface or boundary changes require heavy. Doubt resolves to Security Review (`dev/agent_collaboration.md` > "Review rules").` | 1 |
| C5 | O | `dev/modules/model-selection.md` and `templates/modules/team-gated/model-selection.md` 63-64; `docs/methodology/roles.md` 196-197 | `it also owes the Security Review / that surface already requires, at high.` | `it also owes any Security Review / the heavy-tier rule requires for that edit, at high. DP` | 3 |
| C5 | P | `dev/rules/protected-surfaces.md` 16 | `surfaces retain their proposal and Security Review obligations.` | `surfaces retain their proposal obligation. RG` | 1 |
| C5 | D | `docs/methodology/dual-review.md` 281 | `A high-risk surface named in `AGENTS.md` takes / a Security Review on its own trigger,` | `A change that alters what a high-risk surface named in `AGENTS.md` does or accepts takes / a Security Review on its own trigger DI,` | 1 |
| C6 | H | prose in `README.md` 52-53 (its fragment ends with `:`; replace the colon too), `docs/index.html` 168 (the one before `</p>`), `docs/release-process.md` 64-65 | `Named high-risk surfaces and added or widened trust boundaries trigger heavy.` | RG | 3 |
| C6 | H1 | picture descriptions in `README.md` 55 and `docs/index.html` 170 (the one inside `alt="..."`) | the same | R1 | 2 |
| C6 | H1 | `docs/getting-started.md` 30 | `Heavy is triggered by named high-risk surfaces and widened trust boundaries.` | R1 | 1 |
| C6 | G1 | `docs/glossary.md` 22-23 | `Heavy adds Security Review; high-risk / surfaces and widened trust boundaries trigger it.` | `Heavy adds Security Review. RG` | 1 |
| C6 | G2 | `docs/glossary.md` 83-84 | `triggered by named high-risk surfaces rather than by / size.` | `triggered by a change to what a named high-risk surface does or accepts, or a new place where outside input enters, rather than by / size.` | 1 |
| C7 | S3 | `dev/modules/onboarding/dev-tour.md` 92; `docs/dev-tour.md` 92 | `Named high-risk surfaces and widened trust boundaries trigger it.` | RG | 2 |
| C7 | H | `docs/assets/three-lanes-of-change.svg` 10-11 (the comment) | `Named high-risk surfaces and added or widened trust boundaries trigger heavy.` | RG | 1 |
| C7 | H1 | the same file 31 (`<desc>`) | the same | R1 | 1 |
| C7 | N | the same file 126 | `Heavy adds Security Review; high-risk surfaces and new/widened boundaries trigger it.` | `Heavy adds Security Review; high-risk behavior, input or boundary changes trigger it.` | 1 |
| C7 | lock | the four lock-tracked files (`dev/agent_collaboration.md`, `dev/proposals/_template.md`, `dev/modules/security-review.md`, `dev/modules/model-selection.md`) | none | scoped `upgrade --finalize` (C7) | 0 |

```
TR    A change gets the heavy tier when it alters what a high-risk surface does or accepts, or adds a place where outside input meets the system; merely touching a surface does not.
D     When in doubt, take the Security Review.
DP    When in doubt, take the Security Review (`dev/agent_collaboration.md` > "Review rules").
DI    (when in doubt, take the Security Review; `dev/agent_collaboration.md` > "Review rules")
K     A project rule that names its own Security Review still applies.
Kc    Stricter project rules, such as the engine rule in `protected-surfaces.md`, still apply.
TAIL  A newly found boundary stops work for reassessment. Ordinary uncertainty elsewhere takes the lighter lane, with the reason.

R1    TR D
RG    TR D K
RT    TR DP K
RC    TR D Kc    (Cairn's own guide only)

B     **Lowering a tier.** Only the Maintainer lowers a tier, in chat or a Decision; an author or reviewer may recommend it. The plan records it in one appended `Plan change`: the Maintainer's words verbatim with their source, the cancelled chunks, the obligations that lapse (those whose only source was a cancelled chunk, such as a Security Review of code no longer written) and those that remain (fences, Maintainer-reserved steps, model floors, anything tied to a remaining chunk), the new header values, and that the remaining scope does not alter a high-risk surface or widen a boundary. A review already held stays valid for the scope it covered and transfers to nothing else. A raise follows the same pattern. The amendment review checks the lapse list against the cancelled chunks.

L     The heavy-tier narrowing reaches no further than these limits: editing, moving or calling a guard drops out of Security Review only when none of them changes. When in doubt, take the Security Review.
W     On Windows, a `file:` URL or a path taken from a manifest or argument can name a network share (`\\host\share`, `//host/share` or `\\?\UNC\`), and any resolve, stat, existence test or open of it reaches that host over SMB (Windows file sharing) and answers its login challenge with a response computed from the user's credentials (crackable or relayable, though not the hash itself); refuse such a path after normalizing and before any of those, because normalizing does not remove the host, and do not count an HTTP-level guard as a network guard.
```

B is its own paragraph (blank line before and after): one line in the guides, wrapped at 80 columns in lifecycle (break only at spaces outside backtick spans). L goes on new lines, wrapped at 80; W goes on new lines, wrapped at 80 and indented two spaces. Both security-review copies get the same text. In `model-selection.md` keep each line's `> ` prefix. The rule (RG, RT, RC) fits at 15 places, and every place that picks a tier says how doubt resolves. It does not fit at six, measured: the four picture descriptions keep R1; `AGENTS.md` cannot hold even R1 (1,495 words now, 1,523 with R1, cap 1,500: the installed `AGENTS.md`, `VENDOR.md` and `RULES.md` together), so A keeps a stricter trigger and a short doubt sentence, which makes exactly 1,500 (measured on a scratch copy of the templates at HEAD); the figure note N cannot hold even TR (175 characters; the 85-character note measures 618 px of a 700 px figure). If the C4 total is above 1,500, restore A's old text byte for byte, keep every other place, and say so in the commit message (the sweep then lists that one line). Every other new text goes in whole, however long its line; if an old fragment no longer matches, stop.

## Acceptance criteria

**C1 (F, F′, F′b, B).** Each of the three places holds its new text, whitespace-collapsed equal; lifecycle holds `Ordinary uncertainty elsewhere` once and still holds `If an agent discovers a new boundary, it stops and reports it for reassessment.` and `No agent raises a tier on its own.` B appears once in each of the three files, counted after collapsing whitespace because B wraps in lifecycle and `git grep -c -F` would print 0 there: `python -c "import re,sys; print(re.sub(r'\s+',' ',open(sys.argv[1],encoding='utf-8').read()).count(sys.argv[2]))" <file> "Only the Maintainer lowers a tier, in chat or a Decision; an author or reviewer may recommend it."` prints 1 for each. No other added sentence lets an author, reviewer or `Plan change` lower a tier. The commit message records the guides' word counts (expected about +170 and +169) for the template-trim plan. The selector's tests that read these files pass.

**C2 (L, W).** Both copies hold L once and W once. W is one sentence and holds `\\host\share`, `//host/share`, `\\?\UNC\`, `SMB (Windows file sharing)`, `after normalizing and before any of those`, `not the hash itself` and `HTTP-level guard` (counted with the C1 command: W wraps, so `git grep -c -F` would print 0 for three of them, measured on a scratch wrap). The two copies still differ only where they did: `diff dev/modules/security-review.md templates/modules/team-gated/security-review.md` shows the same four hunks as before the edit (measured: line 1, the two-pass-cap paragraph as two hunks, the provenance bullet near line 194), none in the added lines. `python scripts/check_cairn.py` on both reports no content-scan flag; if it flags, stop and report, adding no `cairn-accept` marker.

**C3 (T1 to T4).** Seven places hold their new text. The shipped template's diff touches no line inside a `cairn:slot` block, and every other line of both files is unchanged. The selector's tests pass, including `test_loop_fidelity_gate.py`, `test_review_stance_in_shipped_files.py` and `test_board_json_contract.py` where selected. Record both files' word counts.

**C4 (A).** One place holds A. The installed total of `AGENTS.md`, `VENDOR.md` and `RULES.md` is at most 1,500 words: `test_full_install_seeds_rules_md_within_word_budget` in `bootstrap/tests/test_scaffold.py` passes; measured before, 1,495 (a scratch install, same steps as the test), and 1,500 with A as written. If the total would pass 1,500 (another session added words), restore A's old text byte for byte, change nothing else, and say so in the commit message; do not shorten other words. Cairn's own `AGENTS.md` is unchanged. After C4 is committed, run the selector as `python tools/test_tiers.py for --range <C3 commit>..HEAD templates/core/AGENTS.md` (it refuses an `AGENTS.md` path without a range).

**C5 (O, P, D).** Five places hold their new text. The model-selection pair stays byte-identical (`cmp`; `test_the_model_selection_pair_is_byte_identical`), and `roles.md` reads as the module does once `> ` prefixes are removed. `dev/rules/protected-surfaces.md` diff is one hunk and lines 5-7 are unchanged word for word. `docs/methodology/dual-review.md` diff is one hunk.

**C6 (H, H1, G1, G2).** Eight places hold their new text. `docs/index.html` still parses as HTML (`python -c` with `html.parser`, no error). Each picture description keeps its unchanged tail (`Ordinary uncertainty takes the lighter lane with a reason; stop on a newly discovered trust boundary.` or the shorter forms already there), and the glossary still reads `A new boundary stops work` after G1.

**C7 (S3, H, H1, N, sweep, lock).** `cmp dev/modules/onboarding/dev-tour.md docs/dev-tour.md` is identical and `test_an_installed_onboarding_copy_equals_its_page` passes. The figure parses as XML, keeps its viewBox, and the lane label at line 93 is unchanged. N is 85 characters; measured in the Browser pane it is 618 px wide against 633 px for the line it replaces, in a 700-wide figure. Then the sweep (Verification), whose results go in the commit message. Last, the lock: `python bootstrap/scaffold.py upgrade --target . --finalize <the four paths in the table>` (the command the template-trim plan's C9 uses; not run here), `python bootstrap/verify_integrity.py --target .` lists none of the four, and the second commit holds `dev/.cairn/cairn-lock.yml` (and any `dev/.cairn/base/` file the finalize wrote) and nothing else.

## Scope delta

**Scope delta**: degraded

**What changed from the Decision, in plain words.** The Decision put a reviewed-limits clause of about 213 words, with the narrowed trigger, in each of 31 places. At the Maintainer's direction that clause is replaced by one short rule of about 50 words, in the same words wherever the place can hold it. A reader loses the list of five limits (who supplies the data, what inputs are accepted, what validation runs, what the operation can do, who receives its output), the line that data a protection reads (a test fixture, a policy file) counts as an input, and the instruction that a reviewer names which limit changed. The five limits stay in `dev/modules/security-review.md`; the long clause survives only in the plan reviews. What stays: when in doubt take the Security Review, stricter project rules still apply, a newly found boundary stops work, and only the Maintainer lowers a tier.

- **U1, the long clause is replaced by the short rule at all 31 places.** Cost: no checklist of limits, so a change that alters a limit without touching the surface's own code is easier to call light; the doubt sentence is the guard. **disposition**: accept (allowed by the Maintainer, below).
- **U2, six places carry less than the whole rule**, because it does not fit (measured): the four picture descriptions carry its first two sentences; `AGENTS.md` carries a stricter trigger plus a doubt sentence and pointer (the first two sentences would make 1,523 words against a cap of 1,500); the figure note carries a compressed trigger with no doubt sentence (the first sentence is 175 characters, the note holds 85). The picture descriptions do not name the stricter project rules. **disposition**: accept (allowed by the Maintainer, below).

**Maintainer's allowance** (Maintainer chat, 2026-11-16, relayed by the coordinator): "I mean, that specification is far too detailed. This isn't building a fighter jet--it's scientific software. That 213 word specification"

The proposal counts one place per `security-review.md` copy without naming it; the plan reads it as L (the module "gains one sentence" beside its "not widening" paragraph). W is part C, not in the 31.

## Verification

Promises: what an agent reads decides whether a change gets a Security Review (the guides, lifecycle, the templates), and that only the Maintainer lowers a tier. Entry points: those texts. Checks below, per chunk, on the chunk's files; everything uses `/Users/kendal30/conda_envs/lhm/bin/python3.13`.

1. **Exact text.** `git diff -U0` per file shows only the old fragments removed and the new text added (line breaks collapsed). Anything else removed: revert that hunk and stop.
2. **Gates on each edited document.** `python scripts/claim_check.py <file>` (no hard flag), `python scripts/link_check.py <file>`, `python scripts/sync_doc_snippets.py --check <file>`, `python scripts/check_cairn.py <file>`, each on the chunk's `.md` files, and once per chunk `python scripts/quality_gate.py --sub neutrality`. Baseline: `sync_doc_snippets.py --check` passed on the whole tree at `0f85f3e8`.
3. **Tests.** `python tools/test_tiers.py for <chunk paths>` (40 files for the 20 non-`AGENTS.md` paths together, measured), run with `-m pytest`; nothing wider. Run the set before the edit and after. A test red both times with the same failure belongs to another plan (group 1's pending re-anchor leaves some gate tests red; `repin.py status` shows why): record it and go on. A test red only after the edit stops the chunk.
4. **Final sweep (C7).** (a) This returns no line:

```
git grep -n -E "Named high-risk|triggered by named high-risk surfaces|high-risk surfaces and (added or )?widened trust boundaries|high-risk surfaces and new/widened boundaries|named high-risk or added/widened|already a Security-Review trigger|A high-risk surface takes a Security Review|it also owes the Security Review|retain their proposal and Security Review obligations|A high-risk surface named in .AGENTS.md. takes|High-risk surfaces and added or widened|widened trust boundaries trigger it|or one that touches a" -- . ':!dev/proposals/2026-*' ':!dev/proposals/archive' ':!dev/plans' ':!*/archive/*' ':!CHANGELOG.md' ':!dev/reflections' ':!dev/PLANNING.md' ':!dev/strategy' ':!dev/measurement'
```

It returned 29 lines in 19 files at `19b2d666` (29 in 19 again today); the two other places are the L insertions. If C4 restored A's old text, (a) returns exactly that one line, in `templates/core/AGENTS.md`, and no other. (b) Each of the 31 places holds its new text (macros expanded, whitespace collapsed in the file, `> ` stripped). Negative control: delete the doubt sentence from one place in a scratch copy and (b) must fail there. (c) `git diff --name-only <C1 parent>..HEAD` lists only the 21 files, `dev/.cairn/cairn-lock.yml` and any `dev/.cairn/base/` file C7's finalize wrote. (d) `python scripts/repin.py status` lists none of the 21 files under FROZEN-MODIFIED, and its list matches the one before C1 apart from other sessions' files.

**Does any rule weaken or disappear?** Yes, deliberately, as the proposal says: (1) "touches a high-risk surface" as a heavy trigger, at 24 places; (2) the surface-based Security Review obligation, at 5 (P, O three times, T4). At the Maintainer's direction the five-limits clause is also gone (Scope delta). Kept and not edited: the Maintainer sets the tier, a newly found boundary stops work (TAIL, lifecycle, G1, the picture descriptions), the two-pass cap, fences, the proposal-path rule, the one-line engine rule, the security-verification rule; the rule's last sentence says a project rule naming its own Security Review still applies, and the 12 places where an author picks a tier say how doubt resolves. Labels: F, F′, H, H1, S3, G1, G2, N, T1 to T3, A and D are (1); P, O and T4 are (2); B, L and W add rules and remove none. The commit message records each place's label and that check 1 passed for it. Check 1 shows each hunk is exactly the new text, so the implementer makes no weakening judgment; the reviews do.

**Security preflight S2, S3.** The negative control is the sweep: restore one old fragment in a scratch copy and check (a) must return that line. The gate that fires is the sweep plus `check_cairn.py`.

**Reviews after implementation.** Code review (fresh, Medium) and a Security Review (High) on the proposal's questions (a) to (e), applying its worked cases and the #62 case to the short rule; a case that turned on the five limits is judged by the doubt sentence. Signals the change is wrong are the proposal's. Not run by this plan: Windows behavior, a whole-suite run.

Length (counted by script before this paragraph, after the plan review and the Maintainer's direction): Build summary 174, Source proposal 94, Scope 466, Sequence 2,075, Scope delta 355, Verification 670; Acceptance 640 across seven chunks. The opening body runs about 3,834 words against the 1,000 target (3,270 before review, 4,270 after the first revision; the short rule cuts it). The overrun is exact text a Low-tier implementer must not have to decide: the Places table and its definitions (about 1,241 words) and the sweep command (about 74). I cut repeatable prose first and cut no exact text.

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

## Plan review -- Claude Opus (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: a36f751310d12319d498c82c992b1280ef8b304b
```

**Obligation**: Internal Security Review: whether the narrowed trigger, as written into the 31 places, can let a needed Security Review be skipped, and what C1 to C7 must carry so a Low-tier implementer cannot weaken a kept protection.
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 3 minutes (16:03 to 16:06, measured with `date`)
**Tokens**: unknown

Steelman: F's five limits name the cases I tried (a one-line default flip, a threshold, a new data source, a fixture edit, a runbook step removed: each changes "what validation runs" or "who supplies the data"), so the governing homes fail safe.

**Foundations**

1. **Should this happen as framed?** Yes, if the places where a tier is chosen carry the doubt rule -- plan lines 87-132.
2. **Best alternative.** None simpler; a standing test is ceremony, the C7 sweep suffices -- plan line 176.
3. **What would show it wrong.** A touch-only edit to `bootstrap/_scaffold/` judged light from F alone (finding 1) -- `dev/rules/protected-surfaces.md` lines 5-7.

**Findings**

1. **Blocking, C1: F contradicts the rules the Decision kept stricter.** F2 says editing or calling a surface "does not by itself trigger heavy". An agent reading only the guide, editing one line of the scaffold engine or a security-verification registry entry, takes the light lane; `protected-surfaces.md` lines 5-7 and `dev/modules/security-verification.md` lines 39-43 still require Security Review, and F never points to them. Closes: one F clause saying a rule that names its own Security Review still applies (Cairn's guide names both files; the shipped guide says "a project rule").
2. **Blocking, joins Internal finding 1.** T1 to T4, A, R and D are where an author picks a tier; there, "substantively" with no doubt rule lets a fixture edit or a rename out of a `_gate_*` pattern be called light. Each must carry, in its own words, "doubt resolves to Security Review" and a pointer to `dev/agent_collaboration.md` > "Review rules"; if A cannot fit in the 1,500-word cap, A keeps its present stricter text and the sweep excludes it. Summaries (S1 to S3, G1, G2, N, alt text) decide no tier and may stay short. Doing that keeps the meaning in every place that decides a tier, but only the Maintainer can accept that reading for the summaries, so `degraded` plus their allowance is still owed.
3. **Non-blocking, B.** Say "lowers a tier or drops a required Security Review", and say a reviewer's "no limit changed" (F5) is a recommendation. The existing deviation rule already stops a skip, so this only makes the rule plain.
4. **Non-blocking, check.** Sweep (b) needs a negative control too: remove the doubt sentence from a scratch copy and (b) must fail.

Kept rules: P leaves lines 5-7 alone (C5 checks it); security-verification is in no chunk, and check (c) proves it is unchanged. None of the 21 paths is in the gate manifest (I checked each exact path against all 6,103 strings). `repin.py status` shows 24 FROZEN-MODIFIED, none of them these files. No signed procedure document is edited.

**Coverage**: I read the plan, the proposal's reviews and Decision, `protected-surfaces.md`, the security-verification paragraph, the tier text in the guides, lifecycle and shipped `AGENTS.md`. Not covered: W's accuracy, the remaining summary places line by line, any test run. The pass is about 520 words, over the 300 target, because both blocking findings need their cases.

## Response to plan review -- Claude Sonnet 5.5 (plan author, Medium) -- 2026-11-16

**Elapsed**: about 15 minutes (start estimated at the end of the Security Review, 16:06; end measured with `date`)
**Tokens**: unknown
**Disposition**: awaiting the Maintainer's allowance of the Scope delta; not `ready-to-implement`. Status becomes `revising-plan`. The plan moves to `ready-to-implement` only when the Maintainer's quoted allowance is in `## Scope delta`.

Conclusion: every finding is accepted except part of I4 and all of S3; both blocking findings are closed in the operative text. The plan can no longer say `preserved`: only the Maintainer can allow the shortfall. I checked each finding against the tree first. No second Security Review pass is asked for: the new sentences are the minimum text Security named, and the Maintainer may call one. No test added; none pins wording. Not run: any edit, Windows, a test, the `upgrade --finalize` command.

| Finding | Disposition | Where answered |
|---|---|---|
| I1 blocking | Accepted. `degraded`; fail-safe sentence and pointer at the 12 tier-choosing places. | Settled text (FS, FI, T1 to T4, A, R, D); Scope delta; Scope, Build summary |
| I2 blocking | Accepted, verified: B's first sentence ends at column 78 in lifecycle; its anchor has backticks. The same flaw hit W: 3 of 7 C2 fragments break across lines on a scratch wrap. | Places table (B row); C1, C2 (collapsed count) |
| I3 | Accepted. C7 records the four lock-tracked paths with a scoped finalize and commits the lock alone. | Places table, C7, Non-work, Verification 4(c) |
| I4 | SMB spelled out (W is now 91 words). One sentence stays: the Decision says one; splitting is the Maintainer's call. | W; C2 |
| I5 | Accepted, verified: the trim plan edits `VENDOR.md`, not `AGENTS.md`, and appends to `dual-review.md`. | Sequence, Order among group 2 |
| I6 | Accepted. | F′b; Places table; C1 |
| S1 blocking | Accepted, verified: `protected-surfaces.md` lines 5-7, `security-verification.md` lines 40-43. F8 added; the shipped guide and lifecycle say "a project rule". | F8, F, F′; C1; Verification weaken paragraph |
| S2 blocking | Accepted. A fits exactly (1,495 to 1,500, measured on a scratch copy); if over, A keeps its old text and the sweep lists that line. Summaries stay short, as the Scope delta says. | Settled text; C3 to C5; Verification 4(a), (b) |
| S3 | Declined: B's sentence is the Decision's wording, and dropping a required Security Review already needs the Maintainer's word (`dev/agent_collaboration.md` > "Plans and records" and "Review rules"); B already says a reviewer may recommend. | none |
| S4 | Accepted. | Verification 4(b) |

**Coverage**: about 480 words (counted by script) against a 300 target; ten findings each need a row. Additions beyond the findings: none; the C1 guide word counts were remeasured (+314 and +293) because F8 grew F.

## Response to plan review -- Claude Sonnet 5.5 (plan author, Medium) -- 2026-11-16 -- Maintainer's direction

**Elapsed**: about 10 minutes (start estimated, end measured)
**Tokens**: unknown
**Disposition**: ready-to-implement

Conclusion: at the Maintainer's direction (chat, 2026-11-16, quoted in Scope delta) one short rule of about 50 words replaces the 213-word clause, and the plan is shorter.

What changed: F1 to F8, the per-place sentence list and the Waiting line are gone; Acceptance and Verification match. The rule (trigger sentence; "when in doubt, take the Security Review"; "a project rule that names its own Security Review still applies") is the same words at 15 places and its first two sentences at the four picture descriptions. `AGENTS.md` and the figure note keep compressed lines because the rule does not fit (1,523 words against a 1,500 cap; 175 characters against 85). The five-limits list is dropped. B and W are unchanged; L uses the rule's doubt wording. Scope delta stays `degraded`; the Maintainer's words are the allowance.

No second Security Review pass is needed: the change only narrows the plan. The Security reviewer's two blocking points are met by the rule's last two sentences, and the 12 places where an author picks a tier keep a doubt sentence and pointer. The Maintainer may call one.
