<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/lifecycle.md reason=published methodology citations -->
# Cairn — development roadmap

Current work and follow-ups, reviewed 2026-10-19. Plans and proposals own their
designs and evidence; this board names the remaining work and its next move.
Completed work leaves the board. The commit history retains earlier versions.

## Where the project stands

<!-- cairn:slot project-status -->
Cairn is at **v0.4.0**, its first public release (tagged 2026-10-20), self-hosting
and used in LHM and modflow_tools. The external correctness trial remains open;
it was expressly waived as a condition of publishing 0.4. **0.5 is laid out
below.**

Standing direction: **postdoc-first** and **fix defects, build nothing new**
(Maintainer, 2026-07-22). A new tool or mechanism needs its own go-ahead.
The broad-look and subtraction-sweep work is complete; their records are
`dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md` and
`dev/plans/archive/subtraction-sweep.md`.
<!-- cairn:end project-status -->

## Active

Use `python tools/board.py` for current plan/proposal status and
`python tools/board.py --maintainer` for declared waits. These read the
artifacts; this board does not maintain a second status table.

## Release path

### 0.5 (Maintainer direction, 2026-10-26)

**Theme: plain, short, and fits the install.** The Maintainer, on the theme:

> "I like the theme!"

| Work | Gate | Notes |
|---|---|---|
| **Cairn Plain Language 1.0** (17 rules) | Built and archived 2026-10-26 (`2026-10-26-claude-writing-for-the-reader`); its changelog entry is written | Maintainer: "We will be adding this Cairn Plain Language 1.0 as a feature". Lockfile `--finalize` for `AGENTS.md` and `dev/agent_collaboration.md`, and a neutrality check on any vendor name in `doctrine/rationale.md`, before it commits. |
| `check_cairn` deleted-file crash | Fixed 2026-10-26 (commit `9ec53a43`); its changelog entry is written | Defect; one commit. |
| **#32** board and `session-start` accept retired statuses | Maintainer direction, 2026-10-23 | Defect. Lands before drain mode, which reads the board. |
| **#31** "keep it short" in the plan and proposal templates | Prose | The adopter supplied the draft and the evidence. |
| **Model tiers: use the lowest tier that is safe** | Doctrine change: own proposal, clears the rate-limit gate | Maintainer direction, 2026-10-26: formalize a rule set for lower-tier models where possible. Scope below. Built and archived 2026-10-26 (`dev/plans/archive/model-tier-rules.md`); its one frozen-test edit and the new test file join the re-anchor owed at the cut. |
| **Security findings from the two 0.4 Security Reviews** | Built 2026-10-26: fixers answered, code reviews checked (no second Security Review); three older problems and later findings are queued below | LP-SR-1 to 8 and SW-SR-11 to 15, found after their repairs shipped in 0.4.0 and never fixed, plus three older problems the engine-batch Security Review found. Scope below. |
| **Engine batch: F8 and #8 engine half** | Own proposal, Security Review, one AST re-anchor | One batch so the review and the re-anchor are paid once. Maintainer: "Engine batch is in". Rows below. Built and archived 2026-10-26 (`dev/plans/archive/engine-batch-f8-slots.md`); its AST and gate re-anchor is owed at the cut. |
| **`repin`** | Built 2026-10-26 (`scripts/repin.py`; plan `dev/plans/repin-build.md`, ready-to-archive). Waiting on the Maintainer's steps in "The 0.5 cut" below. Its unbuilt items are the proposal `dev/proposals/archive/2026-10-27-claude-repin-ceremony-hardening.md`, awaiting review; its strategy note is archived (`dev/strategy/archive/2026-08-28-claude-repin-revitalization.md`) | Maintainer: "Repin is a build". Removes the re-anchor ceremony's manual corrections. |
| **Drain mode** | Built and archived 2026-10-26 (`dev/plans/archive/drain-mode.md`); its strategy note is archived (`dev/strategy/archive/2026-08-25-claude-drain-mode.md`) | `/session-start --drain [board \| issues \| <item>]`. Scope below. |
| **Onboarding happens at install** | Built and archived 2026-10-26 (`dev/plans/archive/install-time-onboarding.md`); its deletions and edits of frozen files join the re-anchor owed at the cut | Replace the delayed, trigger-based onboarding prompts with install-time onboarding. Maintainer words below. |
| **`NEXT_SESSION` becomes a local note** | Proposal first (`2026-10-26-claude-next-session-local-note`, being written by the Developer session's author; it touches the engine: `config.py` and `lockfile.py` mention the file) | Maintainer direction, 2026-10-26: "Also, NEXT_SESSION becoming a local note should happen in v0.5 too." Confirmed in this session's chat by the Maintainer (answer: "Yes, add it to 0.5 (Recommended)"). The queued row "Make NEXT_SESSION local and untracked" below holds the earlier scope: the ignore pattern, the scaffold seed, the session-routines doctrine, the goodnight wording in `AGENTS.md`, and the session-end description. Engine files change, so the AST re-anchor set grows and a Security Review is probably owed; the proposal's author sets the header from what it finds. Built and archived 2026-10-26 (`dev/plans/archive/next-session-local-note.md`); its frozen-file edits and the new test join the re-anchor owed at the cut. |
| **`upgrade` removes untouched copies of files Cairn stopped shipping** | Proposal first (to be written; engine change in `upgrade`, so a Security Review is probably owed) | Found by the onboarding proposal's usual review: that change leaves nine now-dead onboarding files in existing installs, and the `NEXT_SESSION` change leaves a stale copy too. Asked the Maintainer directly, 2026-10-26: add it to 0.5, queue it after, or skip it; answer: "Add it to 0.5". Order: it lands last, after the `NEXT_SESSION` and onboarding changes it cleans up after. Scope condition from the onboarding Security Review (its SR1): when a copy has been modified, `upgrade` must report it by name rather than fold it silently into the removed count. Built and archived 2026-10-27 (`dev/plans/archive/upgrade-removes-retired-files.md`); the Maintainer allowed its departures 5 and 7. Its re-anchor entries are in the plan (frozen edits, six new engine symbols, one renamed node in `test_agreement_retired.py`). |
| **`upgrade` stops running a repository's own programs when it checks for edits** | Proposal first (to be written after the twelfth row's; engine change, so a Security Review is owed) | Found by the twelfth-row Security Review: `upgrade --stage`, `--apply` and an unscoped `--finalize` call `_dirty_tracked_paths` (`bootstrap/_scaffold/upgrade.py`), a plain `git status`. Measured by that reviewer: an ordinary `upgrade --stage` ran a program named in a project's `.git/config` (`core.fsmonitor`), and the same helper reads an edited file as clean when the project sits in a subfolder of a larger repository. Not a simple fix (a sterile git call and a different dirty check). The Maintainer's answer, 2026-10-26, to where it goes: "A 0.5 row, after the twelfth (Recommended)". It reuses the sterile git helper the twelfth change builds. Reported by the reviewer, not reproduced by the planning session. Built and archived 2026-10-27 (`dev/plans/archive/upgrade-edit-check-no-repository-programs.md`); the code review found no blocking defect. Its re-anchor entries are in the plan. |
| **Re-anchor ceremony hardening** (the repin note's unbuilt items) | Proposal accepted 2026-10-27 (`dev/proposals/archive/2026-10-27-claude-repin-ceremony-hardening.md`, archived; `dev/plans/archive/repin-ceremony-hardening.md` opened 2026-10-27, awaiting plan review) | Maintainer, 2026-10-27, closing the repin strategy note: "Let's just go ahead and finish out the repin strategy note with any un-built items as a final proposal for v0.5" (relayed by Strategy). Decision 2026-10-27: build A (the launcher template joins the files the gate trusts) in the cut's ceremony, code-reviewed first; build B (narrowed control tests, new test file) and H (claim-only prose edit) before the cut; A2 after the cut and before M2; C, D, I deferred; E not built; F, G dropped; REL-1 stays deleted. A2 (the launcher equals the anchor's template; edits `scripts/repin.py` and its two test files) is a later row: it comes after the cut and before M2, and needs its own plan or an amendment of this one. |
| **Plain Language adoption docs** | Proposal accepted and built 2026-10-27 (`dev/proposals/archive/2026-10-27-antigravity-plain-language-adoption-docs.md`, commit `bd4f1953`) | Maintainer, 2026-10-27: "Can we decide `dev/proposals/2026-10-27-antigravity-plain-language-adoption-docs.md`? I would like to get this implemented here for 0.5 as well"; Decision conditions: "Accept and commit (Recommended)" and "Yes, check each one (Recommended)". Prose only (`docs/plain-language.md`, `doctrine/rationale.md` Anchor 16); no re-anchor owed. Reference check of 30 entries: 22 confirmed, 5 corrected, 3 partly verified (Budescu 2014's 27% to 40% figures, COPE, the Federal Plain Language Guidelines). No reviewer has read the new text; ISO clause numbers were not re-checkable. The old `Mandel & Irwin (2020)` year in Anchor 16 was corrected to 2021. |
| **Older installs fail the integrity check (kept edited ledger)** | Trivial defect repair (`doctrine/lifecycle.md` three conditions), by the Developer session; lands after the thirteenth plan's code review closes, because it edits `_cmd_finalize_lockfile` too | Maintainer, 2026-10-27, relayed by the Developer session (not yet confirmed in this chat): "And this 'Older installs fail the integrity check' item seems like something to take care of too". Measured by the Developer on clean v0.3.0 installs, Python 3.13.13: v0.3.0 records its foldback ledger (a file named cairn_foldback.md under dev/.cairn/, which v0.4.0 stopped shipping) with `living_state: true`; the engine no longer allows that path; the twelfth change fixes an untouched ledger, but an edited one is kept and `verify_integrity` exits 1, and `upgrade --finalize <path>` records it without dropping the flag, against what `bootstrap/UPGRADE.md` says. Fix: `--finalize <path>` drops a `living_state` flag outside the allowed set, so the file is checked like any kept file. Reported, not reproduced by the planning session. Built 2026-10-27 as a trivial defect repair by the Developer session, commit `5ec9e3bb`: six lines in `_cmd_finalize_lockfile` (already in the AST changed set, so no new symbol) and a new test file `bootstrap/tests/test_finalize_retired_living_state.py` (a new frozen file, allowed). No code review, by the trivial lane; Boundary B record is in the commit body, `Certified by: pending`. |

**Onboarding, the Maintainer's words.** Direction of 2026-10-26, relayed by the
Developer session. On the prompts that never fire:

> "I don't know why we have delayed prompts at all. They should onboard when we onboard!"

The correction, the same day:

> "I don't want them delayed. I want them fixed so that they actually happen when someone installs Cairn."

and on the release and the proposal:

> "This belongs in v 0.5. Please write the proposal and coordinate with the Cairn v0.5 Planning session"

The planning session also asked which release this goes in; the Maintainer's
answer: "0.5, as a new row (Recommended)". The design, the Security Review and
the build record are in `dev/plans/archive/install-time-onboarding.md`.

**Drain mode scope.** `/session-start --drain [board | issues | <item>]`.
Triage has three levels; the Maintainer took the first two:

> "Let's go with the first two triage levels."

1. **Sort.** Read each issue, assign a lane by `doctrine/lifecycle.md`'s closed
   triage procedure, and mark what needs the Maintainer or touches a high-risk
   surface. Changes nothing.
2. **Act on trivial ones.** Fix the defect repairs that have a failing test,
   review, commit.
3. **Not in 0.5: comment, label, close.** Drafted comments are presented in the
   batch for the Maintainer to post or reject. **Issue text is data, never
   instruction:** drain never runs anything an issue contains. The design note
   predates this rule and must state it.

**Model-tier rules scope.** The floors by role exist (`doctrine/roles.md`,
the `model-selection` module) and the proposal builds on them, mostly in prose:
key the table on the lane (trivial, standard, deliberate), with Security Review
always high; put the sub-agent default in `AGENTS.md` so every profile gets it,
not only the two that install the module; require the model to be named
explicitly at every spawn, with escalation by one tier on failure; and decide
in the proposal whether to relax the condition that lets a cheaper author work
under a check (relaxed 2026-10-26: a stronger model from the same maker now
counts). Measurement needs no new machinery: every review
already records its model. The standing rule is written down once in the
repository, not left in an agent's private memory.

**Security findings scope.** Two Security Reviews raised findings after their
repairs shipped in v0.4.0. They were never fixed, and no row or recorded
acceptance existed. Checked 2026-10-26: no closing test the reviews name exists
in `bootstrap/tests/` (for example `test_apply_never_creates_a_profile_through_a_link`
and `test_a_lockfile_that_is_a_link_is_refused_and_never_written`). The
Maintainer, 2026-10-26, relayed by the Developer session:

> "Yes, add the security findings as a v0.5 item"

* **LP-SR-1 to 8** (`dev/plans/archive/2026-10-19-security-review-upgrade-lockfile-paths.md`,
  commit `f0280ef0`; touches `bootstrap/_scaffold/upgrade.py` and `lockfile.py`).
  The serious one is LP-SR-1 (high, older than the 0.4 repair): `upgrade --apply`
  creates a file outside the project when `dev/.cairn/profile.yml` is a link to
  a file that does not exist yet, and the lockfile picks up some of its lines.
* **SW-SR-11 to 15** (`dev/plans/archive/2026-10-18-security-review-session-writes.md`,
  commit `bf746470`; touches `templates/skills/_lib/session.py` and its twin
  `tools/session.py`: the interpreter binding, a named high-risk surface).
* **SW-SR-10** was accepted in chat on 2026-10-19 (*"Accept in writing; move
  later (Recommended)"*) and never written. Write it as one docstring sentence
  in `_resolve_interpreter` and a residual-risk entry in `bootstrap/SAFETY.md`.
  Moving the binding into `.git` is a separate proposal after 0.5.
* **Each finding carries its exact fix and closing test in its review.** No
  second Security Review. The Maintainer, 2026-10-19: *"Let's just not iterate
  back and forth on the Security Review"* and *"For now let's just do the
  single-round Security Review for these"*. A fixer answers the findings and one
  code review checks the answer.
* **Three accepted residuals from the LP-SR fixes, 2026-10-26.** The fixer
  closed LP-SR-3, 4, 6, 7 and 8 fully and left three limits: LP-SR-5 got only
  the documentation answer, not the full split, because the split breaks a
  frozen pin; a linked lockfile on `--adopt-collisions` still ends in a
  traceback, because a frozen test expects an exception there; and the profile's
  preset, axis and module values are written unquoted, because quoting fails the
  frozen differential oracle's byte comparison (a printable value containing `: `
  or ` #` makes a profile the loader refuses, on that line only). Each is
  recorded in `bootstrap/_scaffold/SECURITY_MUTATIONS.md`. The Maintainer was asked
  whether to accept all three as documented residuals and answered:

  > "Accept all three (Recommended)"

  Nothing more is built for them in 0.5. The code review of the fixer's answer is
  still to land; a finding there can reopen one.
* **Three older problems found by the engine-batch Security Review**
  (`dev/proposals/2026-10-26-claude-engine-batch-f8-slots.md`, commit `e92ad324`).
  Reported by that review; the roadmap's author reproduced none of them. All
  three are outside the engine batch and in the same files as the rows above.
  Authorization to fold them in, verbatim:

  > "Yes, fold all three into the security row"

  1. **The upgrade does not check the saved base copy against its recorded hash**
     before the merge uses it (finding SR6). A crafted base copy can already
     silently drop an adopter's edit or a Cairn fix. Recommended fix: check the
     hash at plan, stage and apply, and on a mismatch make the file a by-hand
     merge.
  2. **Lockfile file names can carry invisible characters** that pass Python's
     `isprintable()`.
  3. **`bootstrap/_scaffold/install.py` prints unknown profile module names
     unescaped** (about line 1526).
  4. **The install report prints profile-supplied slot names raw**
     (`bootstrap/_scaffold/install.py` about line 1668, and `cli.py` about
     lines 359 and 590). Found by the engine-batch plan's Security Review: a
     profile's token value can add slot names. Only bidirectional and invisible
     characters get through, because the profile loader refuses control
     characters (`config.py` about lines 180-183). It predates the engine batch,
     which leaves it out on purpose. Authorization to queue it, verbatim:

     > "Queue it on the security row"
* **Overlap with the engine batch.** Both change functions in `upgrade.py` and
  `lockfile.py`. One fixer holds both, or they run in sequence, never in
  parallel on the same functions. Both add engine symbols to the single 0.5 AST
  re-anchor; derive the real set from the code. The planned names were
  `_self_heal_profile_config`, `_cmd_finalize_lockfile`, `_behind_by_n`,
  `_resolve_vendor_wrapper`, `_apply_upgrade`, `cmd_upgrade`,
  `_check_lockfile_paths`, `_lockfile_refusal` and `_contained_lockfile_path`,
  plus a new `_check_staged_names`; most exist already, so the re-anchor is
  derived, not carried. `session.py` is not the engine, so it owes no AST
  change, but it is a frozen-twin pair and its gate-manifest pins need
  checking.
* **The fixer's notes, kept from the old handoff file at `0c3a483b`, which is
  stale.** In `_behind_by_n` (LP-SR-3) the new hex check goes *after* the
  "missing or unknown" check, because frozen `test_drift_surfacing.py` pins that
  text. LP-SR-1's guard also refuses a `profile.yml` linked to a file inside the
  project: stricter than before, and belongs in `bootstrap/UPGRADE.md`. LP-SR-8's
  `.git` refusal keys on the project tree, not only the `dst` and `base_cache`
  fields, because the shape-table test calls the guard with four positional
  arguments and would not see a new keyword. LP-SR-5's split must still run the
  `files` and `modules` structure checks before the advisory, which crashes on a
  record that is not an object. LP-SR-4 is refused in `_check_lockfile_paths`
  through a new `_check_staged_names`, not escaped in `_print_upgrade_report`.
  New tests go in a new test file: `test_upgrade_lockfile_path_containment.py`
  is itself frozen (the gate manifest's `frozen_files` lists it; the glob
  `bootstrap/tests/**/*.py` freezes every test file), and the earlier note
  saying it was not frozen was wrong, found 2026-10-26 by the fixer.

**Order.** Cheap defects first (`check_cairn`, #32), then Plain Language, #31
and the model-tier prose, then the security findings, then the engine batch (the
two share `upgrade.py` and `lockfile.py`, so one fixer holds both or they run in
sequence), then `repin` and drain mode.

**Issues.** #31 and #32 are the only open issues in 0.5 (#8's engine half is a
row below; #19 is not in 0.5). Both carry a comment saying so.

**One re-anchor, at the cut.** The re-anchor owed since 2026-10-23 (the Queued
row below) is folded into the 0.5 cut, not paid twice. The AST correction
precedes the gate-manifest re-anchor, as at 0.4. Maintainer-only; follow
`bootstrap/REANCHOR_RUNBOOK.md`.

**Final list: the thirteen rows above.** **Not in 0.5**, and still queued below
unchanged: VER-5 (a new mechanism). Left out because 0.5 already carries an
engine batch, a ceremony and a build; it can join by the Maintainer's word. **Also not in 0.5, waiting on their
revival conditions:** #19, #13 and the deferred table.

**Changelog.** Each row lands with its entry under `## Unreleased` in
`CHANGELOG.md`, in the same commit or the next, in the file's entry shape (one
or a few lines, with a link to the durable record). At the cut the section is
renamed `## 0.5.0 — <date>` and a fresh `Unreleased` opened
(`docs/release-process.md`). The GitHub release notes are copied from that
section, not drafted in a separate file: the 0.4.0 draft kept as an untracked
file went stale, with wrong profile names and a wrong repository URL that also
reached the published notes. Those two errors are the Maintainer's to correct
on the published release. Entries so far: Plain Language 1.0 and the
deleted-file fix.

**Branch rule: one branch, and the intents board.** All 0.5 work happens
directly on `0.5-dev`, in the one shared checkout. There are no topic branches
and no worktrees for writing. `master` is frozen at `b70ee08f`: no commits to
it. Before editing a file, record a claim with
`python tools/intent.py claim --files <paths> --action "<what>"`; commit the
files by explicit path, which releases the claim. `python tools/intent.py list`
shows who holds what, and `python tools/board.py` shows every proposal and plan
on the branch. A reviewer who must mutate code does it in a throwaway
detached worktree of the reviewed commit and removes it afterward; it is not a
named branch, and the review itself is written and committed on `0.5-dev`.
Merging `0.5-dev` to `master`, and pushing either, are the Maintainer's. The
Maintainer, 2026-10-26:

> "No more edits in `master` in the Cairn repo"

> "Go ahead and move all new development to 0.5-dev"

> "I actually would prefer that all work happen in the 0.5-dev branch, and that
> we use the intents board. This has gotten to be too many branches for me to
> interact with properly."

**Standing direction.** The 2026-07-22 direction, *fix defects, build nothing
new*, applies to every row above; the choices on this page are the go-ahead for
these rows only.

### The 0.5 cut: what waits on the Maintainer

Written 2026-10-26 by the planning session (updated 2026-10-27: the twelfth plan's allowances and the thirteenth Decision are done), in the order to do it. Nothing in
this list has been run by an agent.

1. **Your `repin` steps** (`dev/plans/repin-build.md`). **Route chosen
   2026-10-27: an early hand re-anchor, then `repin`.** Measured that day,
   `repin` refuses at the current HEAD: `python scripts/repin.py status` stops at
   boot because `bootstrap/tests/_gate_manifest.py` no longer equals the anchor's
   entry (commit `fa86e2cb`). You asked: "Can we re-anchor the one changed file
   and then run repin?" and chose "Early hand ceremony, then repin". The order:
   (a) **done 2026-10-27:** the repin-hardening change (A: the launcher template
   joins the closure, plus H and B) is built and code-reviewed, because A edits
   `bootstrap/tests/_gate_preflight.py`, one of the ten files `repin` compares.
   Your launcher check, two commands that print `SAME` or `DIFFERENT`, is in
   step C7 of `dev/plans/archive/repin-ceremony-hardening.md`;
   (b) a certifying run on the clean tree; (c) **your hand ceremony** under
   `bootstrap/REANCHOR_RUNBOOK.md`, which re-signs the whole manifest and the AST
   pin at that HEAD, not one file; (d) then M2 (`--first-run`, naming a new
   reviewed commit: the last commit of A's code review), M1, R6a; (e) the cut's
   own re-anchor through `repin`. R6b edits `scripts/reanchor_ceremony.py`, so it
   forces one more hand step, and so would any other edit to the ten files after
   (c). A2 (the launcher equals the anchor's template) comes after the cut and
   before M2.
2. **The re-anchors, once, at the end**: the AST attestation and the gate
   manifest. Derive the lists with `_ast_attest.py verify` and
   `_gate_manifest.py verify` on Python 3.13.x, not from the rows below. Your
   authorization must name the differential oracle's sensitive-roster entries
   the 0.5 changes touch: `bootstrap/_scaffold/` (including `config.py`),
   `bootstrap/security_check.py` and `bootstrap/tests/_gate_manifest.py`.
3. **A certifying run** on the clean committed tree (the pair in `AGENTS.md`,
   Boundary B), before the push. Nothing in the tree is certified yet.
4. **Your push**, the merge of `0.5-dev` into `master`, the tag, and the
   release notes copied from the changelog section (rename `## Unreleased` to
   `## 0.5.0 — <date>`), with a short summary paragraph above it that I draft
   at release time once the section is final (`docs/release-process.md`, "The
   cut"). Before publishing, check the page's URL, profile names and commands
   against the tree.

### v0.6 (Candidate directions)

Theme candidates: **Nimbleness recovery, lightweight measurement, and unified doctrine.**

| Work | Gate | Notes |
|---|---|---|
| **Lightweight team measurement** | Proposal first | Strategy note: `dev/strategy/2026-10-27-antigravity-lightweight-team-measurement.md`. Three items: (1) upgrade `tools/gauge.py` to fix product bucketing and add `--pulse` (artifact words/tokens, review passes, model-tier mix, prompt tax); (2) update `tools/audit_report.py` and `tools/gauge.py` to attribute and sum standalone review side-files into their parent proposal/plan (closing the side-file length/pass loophole); (3) add an `archive/` subfolder to `dev/measurement/` and ship it with `.gitkeep` to adopters via `bootstrap/_scaffold/install.py` and the `incident-trackers` module. |
| **Nimbleness 1: Compress governing files and unfreeze prose-wording tests** | Doctrine change, AST/gate re-anchor | Strategy note: `dev/strategy/2026-08-21-claude-nimbleness-recovery.md` (Item 1). Strip tutorial commentary from proposal/plan templates into `doctrine/proposals.md` and `doctrine/plans.md`; rule-flush `AGENTS.md` and `dev/agent_collaboration.md`; relax regex tests in `bootstrap/tests/` to check core rule concepts rather than word-for-word paragraphs. |
| **Nimbleness 2: Single compact artifact for standard multi-step work** | Proposal first, lifecycle doctrine | Strategy note: `dev/strategy/2026-08-21-claude-nimbleness-recovery.md` (Item 2). Allow standard 2–3 chunk work to carry its compact chunk/test plan directly in the proposal (one file, one pre-code review, one Maintainer Decision -> `ready-to-implement`), ending double proposal+plan ceremony for routine changes. |
| **Nimbleness 3: Narrow gate-manifest freezing to security and trust tests** | Security Review, trust-apparatus change | Strategy note: `dev/strategy/2026-08-21-claude-nimbleness-recovery.md` (Item 3) and `dev/strategy/2026-08-05-codex-security-strategy.md` [TRU-4]. Name actual security and trust-apparatus test files explicitly in `bootstrap/tests/_gate_manifest.py` instead of freezing all 195 `bootstrap/tests/**/*.py` files, removing re-anchor debt from routine feature/doc test maintenance. |
| **Nimbleness 4: Return-on-Attention accounting** | Lifecycle doctrine | Strategy note: `dev/strategy/2026-08-21-claude-nimbleness-recovery.md` (Item 4). Add Maintainer steps & follow-ups spawned at Decision; add one sentence on whether the delivered outcome repaid review/ceremony cost at archive. |
| **Nimbleness 5: Move link-check and doctrine-ref allow comments to config** | Tooling | Strategy note: `dev/strategy/2026-08-21-claude-nimbleness-recovery.md` (Item 5). Move inline HTML `link-check-allow` and `cairn-internal-ref-allow` comments out of Markdown file headers into configuration, completing the August sweep pattern. |
| **`doctrine/` and `docs/`: examine how they relate** | Proposal first | Promoted from deferred follow-ups. Question for a proposal: which file is the single place each rule lives, and do the others only point at it? The four-layer model is stated in both `docs/DOCUMENTATION_PLAN.md` and `doctrine/README.md`; the defect-repair carve-out is restated across `doctrine/lifecycle.md`, `plans.md`, `proposals.md` and `AGENTS.md`; prescriptive rules sit in three places (`doctrine/`, `AGENTS.md`, `dev/agent_collaboration.md`) and `docs/plain-language.md` summarizes rules in `dev/agent_collaboration.md`. Check whether restatements disagree and provide clear single-source routing. Maintainer authorization, 2026-10-27: "Yes, queue it for v0.6 and fix the index". |
| **Extend coordinates rule to shipped prose, and scan for it** | Proposal first, rate-limit gate | Promoted from deferred follow-ups (deferred 2026-10-27 for next release planning). (1) One sentence in the durable-artifacts rule (`AGENTS.md`, reasoning in `doctrine/rationale.md`) so it covers shipped module docs, docs and release notes, using the test the ceremony scan already uses; (2) warning-only scan of shipped files against a named list of live ids in `scripts/check_cairn.py`. Maintainer: "Defer the new rule on coordinates for later bringing back up in PLANNING". |
| **Ceremony consolidation: shrink runbook to a page & cut second values reader** | Security Review, closure change | Promoted from deferred follow-ups (`dev/proposals/archive/2026-10-27-claude-repin-ceremony-hardening.md` items C and D). Shrink `bootstrap/REANCHOR_RUNBOOK.md` to a single page and cut the launcher's second values reader together, so the closure is re-pinned once. |
| **Unify shipped-executable discovery [VER-5]** | Proposal first | Promoted from queued work. One traversal for install, manifest, security scan and upgrade. |
| **Windows native support clarity** | Docs / front door | Maintainer confirmation, 2026-10-27: *"Yes, Windows support is native. I use it all the time on my projects"*. State native Windows support upfront in `README.md` and `docs/getting-started.md`. |
| **Document 0-rejections proposal optic** | Docs / lifecycle | Maintainer direction, 2026-10-27: *"Let's add the 0-rejected note somewhere in the docs for v0.6. It's not really a requirement, and other projects have rejected proposals. But yes, basically an idea only happens because of a chat leading to it and many never make it to proposals!"*. Add note to proposal docs/lifecycle explaining Cairn's 0-rejected archive history. |
| **Public-surface metadata alignment & CONTRIBUTING.md** | Front door / metadata | Strategy note: `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md`. Align `CITATION.cff` title ("methodology, not a framework") with `README.md` and `AGENTS.md`; ship a standard `CONTRIBUTING.md` for outside contributors. Maintainer authorization, 2026-10-27: *"Yes, add the public-surface metadata alignment + contributing items"*. |
| **Outside-adopter interview & testimonial (Stid)** | Adopter evidence | Prepare an interview question set and conduct a structured interview with outside adopter Stid to gather qualitative feedback, measure friction points, and capture a testimonial. Maintainer direction, 2026-10-27: *"I do have an outside adopter (Stid). Let's go ahead and get an interview set of questions for him, and he can give us a testimonial"*. |
| **Automate the work tracker from `board.py --json`** | Tooling / hosted sync | Strategy note: `dev/strategy/2026-10-26-claude-work-tracker-and-the-board.md`. Build a generator script to derive hosted tracker rows automatically from `tools/board.py --json`, `git`, and `gh` rather than hand-keeping 60 hosted rows, and optionally add a `passes` field to `cairn-board/1`. Maintainer authorization, 2026-10-27: *"Yes, let's put automating the work tracker on the v0.6 list"*. |
| **Security cluster strategic items** | Security Review, trust-apparatus | Strategy note: `dev/strategy/2026-08-05-codex-security-strategy.md`. Four items: (1) **Trust root ceremony tidy (`[TRU-4 / TRU-5 / TRU-7]`)**: sign anchor commit or align `AGENTS.md`, scrub `PYTEST_*`/`PYTHON*` in Stage A, and add `git push origin refs/cairn/gate-anchor` to runbook; (2) **Security dispatcher out-of-the-box (`[VER-3]`)**: admit `check_cairn.py` to `run_security_verification.py` runner registry; (3) **Private vulnerability reporting route (`[REL-6]`)**: enable GitHub Private Vulnerability Reporting, state it in `SECURITY.md`, and link in `README.md`; (4) **Terminal escaping hygiene (`[BND-4]`)**: escape module/slot names in install report, reject invisible Unicode in lockfile paths, and encode `tools/session.py` child output. Maintainer authorization, 2026-10-27: *"Let's add those security items to v0.6"*. |
| **Move interpreter binding into `.git`** | Proposal first | Promoted from queued work (SW-SR-10 follow-up). Move `.cairn/local-env.json` out of the working tree into `.git/`. Maintainer instruction, 2026-10-27: *"Do those three queued items as well"*. |
| **Fix `session-start` handoff marker mismatch** | Trivial defect fix | Promoted from queued work. Default marker in `tools/session.py` (and twin) is `Goodnight`, while Cairn handoff commits begin `Handoff`, printing a misleading 500+ commit range. Change default to match `Handoff`. Maintainer instruction, 2026-10-27: *"Do those three queued items as well"*. |
| **Handle directory collisions in `upgrade --plan`/`--stage`** | Defect fix, engine | Promoted from queued work. Report a clean conflict instead of crashing with `IsADirectoryError` when an adopter replaces a tracked file with a directory. Maintainer instruction, 2026-10-27: *"Do those three queued items as well"*. |

## Queued

### Re-anchor the gate manifest — frozen files changed

Owed since 2026-10-23: frozen `bootstrap/tests/test_quickstart_sequence.py`
changed so its scripted steps match `docs/quickstart.md` (an `awaiting-review`
proposal, a fresh-session review commit, a quoted Decision, six commits). No
node added or dropped; no engine symbol changed. Maintainer direction:

> "If I need to do a re-anchor, okay"

**Also owed from 0.5 work, 2026-10-26.** The #32 code review found frozen
`bootstrap/tests/test_board_json_contract.py` changed: its golden output gained
the advisory line. `bootstrap/tests/_gate_manifest.py verify` reports it as
modified, and the #32 commit is the only one that changed it. The same `verify`
lists five other modified frozen files that the review did not trace. More are
expected as 0.5 rows land (the model-tier proposal edits frozen
`test_review_stance_in_shipped_files.py`, the engine-batch work edits
`docs/quickstart.md`'s pinned count, and the security fixes may touch more).
The LP-SR fixes (2026-10-26) add eight engine symbols to the AST re-anchor
(derived with `_ast_attest.py verify` on Python 3.13.13): changed
`_apply_upgrade`, `_behind_by_n`, `_resolve_vendor_wrapper`,
`_self_heal_profile_config` and `cmd_upgrade`, and the known-new
`_check_lockfile_paths`, `_contained_lockfile_path` and `_lockfile_refusal`,
whose bodies changed. Two later engine edits add to that set: the repair of
`upgrade --init-lock` (commit `5e66c74d`) changed `_write_init_lock_profile_template`,
and engine-batch chunk C1 (commit `24400219`) changed `main` (`cli.py`) and
`print_report` (`install.py`); the repair of `--init-lock` and `--finalize`
over links (commit `091ec219`) changed `_cmd_init_lock`,
`_cmd_finalize_lockfile` and `cmd_upgrade` and added `_refuse_if_linked` and
`_linked_vendor_wrapper_names`, as the Developer session derived by comparing
the file's AST before and after; the batch's chunk C2 (commit `47366b20`) changed `merge_file` and
`_print_upgrade_report`. Reported by the sessions that made them and confirmed
by the engine batch's code reviewer with the read-only `_ast_attest.py verify`
listing (10 changed symbols, 3 known-new with changed bodies, no new symbol),
not derived by this edit. The engine batch's two new test files,
`test_install_report_slots.py` and `test_upgrade_added_slots.py`, are also
gate-root files the re-anchor must pin, as are the LP-SR test file. The
onboarding change (archived) deletes 15 frozen files and edits 13, and adds 19
engine symbols to the AST set (8 deleted, 11 changed, one of them the
docstring-only `FunctionDef:_render_onboarding_slot`); it needs 4 known-new keys
dropped and 4 rekeyed, and 4 baseline keys dropped and 6 changed. Its plan lists
them (`dev/plans/archive/install-time-onboarding.md`) and names the three oracle
sensitive-roster entries the Maintainer's authorization must name. Reported by
that plan, not re-derived here. The
`NEXT_SESSION` change (archived) edited frozen `test_notice_install.py`,
`test_upgrade.py` and both `verify_stems.py` twins (`test_quickstart_sequence.py`
was already owed), dropped one pinned node in
`test_review_stance_in_shipped_files.py`, and added `Assign:_CORE_MAPPINGS` to the
AST changed set (12 to 13); its new test `test_next_session_local_note.py` joins
the anchor. Reported by that plan's code review, not re-derived here. The edit-check change (archived 2026-10-27) adds one new frozen test file (`FROZEN-NEW`, allowed), edits no pinned test, and renames one node in the unpinned `test_upgrade_removes_retired_files.py`; its code review read the AST `verify` listing as 59 symbols, six more than the plan's list (`_GIT_NOT_STARTED`, `_GIT_NO_ANSWER`, `_git_in_project`, `_ask_git`, `_git_config_bool`, `_cannot_tell_refusal`), with `_dirty_tracked_paths` and `_writeset_dirty_collisions` newly changed and `_apply_upgrade`, `_cmd_finalize_lockfile` and `cmd_upgrade` edited again. Reported by the implementer and reviewer, not re-derived here. The repin-hardening change (archived 2026-10-27) edits three pinned files, `_gate_preflight.py`, `test_gate_preflight.py` and `test_reanchor.py`, and adds one new test file, `test_reanchor_driver_disclosures.py` (allowed); the AST list gains nothing; the packet at your hand ceremony has eleven rows, and M2's reviewed commit is `5293f570`. Reported by its implementer and reviewers, not re-derived here. The integrity fix for a kept fold-back ledger (`5ec9e3bb`) adds one frozen test file (`test_finalize_retired_living_state.py`, allowed) and edits `_cmd_finalize_lockfile`, which the AST list already carries. The Strategy
session reports more, counted by it and not
re-derived here: frozen `scripts/check_cairn.py`, `scripts/link_check.py` and
`scripts/sync_doc_snippets.py` with the two `templates/modules/team-gated/`
twins (commits `9ec53a43` and `dfdd0408`), and frozen
`bootstrap/tests/test_review_stance_in_shipped_files.py` (commit `cdffeb8a`; the
node id is unchanged, so no node is dropped). The Maintainer said of that last
edit: "Go ahead and edit the dual-review. We need to re-anchor anyway". New
unfrozen test files that join the next anchor include
`test_deleted_tracked_markdown.py`, `test_writing_rules_ship.py` and
`test_model_tier_rule_ships.py`. Two Security Reviews of the 0.5 proposals add a
condition for the re-anchor: the differential oracle's sensitive-roster list
(`bootstrap/tests/_oracle_activation.py` about lines 34-47) names
`bootstrap/_scaffold/`, `bootstrap/security_check.py` and
`bootstrap/tests/_gate_manifest.py`, and `bootstrap/_scaffold/config.py`, all
unchanged since the trust anchor `6f29519d`. The onboarding change touches the
first three and the `NEXT_SESSION` change touches `config.py`, so the
Maintainer's authorization for the cut must name them, or the gate stays shut
rather than passing. Both are reported by the reviewers and not re-derived here.
Do not
carry a list forward from this row: run `verify` on the final committed tree and
read what it prints.

This is Maintainer-only; follow `bootstrap/REANCHOR_RUNBOOK.md` and derive the
changed set from the final committed tree.

**Waiting on Maintainer**: run the gate-manifest re-anchor

### Other queued work (reviewed Oct 2026)

* **The session-start tool passes a child process's output through unescaped.**
  Three raw `proc.stderr` pass-throughs and the child's stdout in
  `tools/session.py` (and its twin `templates/skills/_lib/session.py`) are not
  encoded. Found by the code review of the session-write fixes; the Security
  Review's finding listed seven sites and the fix matched it, so this is a gap
  past the finding, not a miss in the fix. Authorization to queue it, verbatim:

  > "Yes, queue it (Recommended)"

* **The board's Maintainer list and the status advisory disagree on a status
  such as `awaiting-decision-x`.** The advisory flags it as unknown; the board's
  `--maintainer` view still lists it as a wait. Making the board strict would
  edit the frozen golden and the waits-recipe test (`test_board_json_contract.py`)
  and fold into the re-anchor owed at the cut. The Maintainer chose to leave it.
  Recorded so the disagreement is a known edge, not a surprise. Answer, verbatim:

  > "Leave the disagreement"

* **A nested `.git` folder is not refused in an upgrade review area.** A
  hand-built review area naming `sub/.git/hooks/post-merge` is applied; the
  written promises (`SECURITY_MUTATIONS.md`, `UPGRADE.md`) cover only the root
  `.git/`, so this is not a defect repair and needs a standard change note. A
  hook is a program that git runs in that nested repository. Found by the same
  code review (its F2).
  The Maintainer's authorization to queue this row (with two others that have
  since been built, commits `18511e42`, `091ec219` and `41bcd166`), verbatim:

  > "Yes, queue all three"

* **`session-start` prints a 508-commit range because its default marker does
  not match Cairn's handoff commits.** Promoted to `v0.6 (Candidate directions)`
  on Maintainer instruction (2026-10-27: *"Do those three queued items as well"*).
  The default marker in `tools/session.py` (about lines 2076-2080) is `Goodnight`,
  but Cairn's handoff commits begin `Handoff`. Edits the session kernel and its twin.

* **`upgrade --init-lock` records the digest of the file behind a linked
  tracked file.** A linked `AGENTS.md` puts the digest of its target into the
  new lockfile. Nothing is written outside the project, and `bootstrap/UPGRADE.md`
  and `SECURITY_MUTATIONS.md` state the limit. Not a simple fix: what a tracked
  link should record (the link, its target, or a refusal) is a design choice in
  the engine, so it needs a proposal and a Security Review. Found by the repair
  of `--init-lock` over links (commits `18511e42`, `091ec219`, `41bcd166`).
  Authorization to queue it: the Maintainer, 2026-10-26, "Queue them if it's not
  simple to fix them now. No need to generate more work for us later." (given for
  this finding and the `--plan`/`--stage` one, which is simple and is being
  fixed now).

* **`upgrade --plan` and `--stage` crash when a tracked file has been replaced
  by a folder.** Promoted to `v0.6 (Candidate directions)` on Maintainer
  instruction (2026-10-27: *"Do those three queued items as well"*). They end
  in an `IsADirectoryError` traceback (`upgrade.py` about line 540) instead of
  naming the file. Needs engine collision handling.

* **Three lessons kept from the old handoff file.** Found in the file the
  `NEXT_SESSION` change deleted (its migration record is in
  `dev/plans/archive/next-session-local-note.md`); they had no other home.
  (1) Every subagent in one session shares one work-intent agent id, so one
  commit releases the others' claims: check `git diff` before each commit.
  (2) Heavy test runs should take turns. (3) A review of a long plan is
  expensive, so give tight briefs. Kept as written there; the planning
  session's note, not doctrine (doctrine text takes the rate-limit gate).

* **The gate anchor has no signature.** `refs/cairn/gate-anchor` points to
  commit `6f29519d`, and git reports no signature on it (signature status `N`;
  `git verify-commit` exits 1; the control `git tag -v v0.4.0` exits 0, measured
  2026-10-26). `AGENTS.md` says the anchor is trustworthy because of "the
  signature on the commit it names", which is false for the current anchor. Two
  ways to close it: sign the anchor at the next key ceremony, or correct that
  sentence. Which is the Maintainer's call. Found by the repin Security Review
  (finding SR-8, in `dev/proposals/archive/2026-10-26-claude-repin-build.md`).
  Authorization to queue it, verbatim:

  > "Yes, add both as Queued rows"

* **The re-anchor ceremony passes inherited environment variables into the test
  run it pins.** Reported by the repin Security Review, not reproduced by the
  roadmap's author: an inherited `PYTEST_ADDOPTS` dropped 9 of 4,650 tests from
  the pinned set and the run still exited 0, and a pre-compiled Python file
  committed into the tree is covered by no pin. The ceremony's Stage A should
  clear `PYTEST_*` and `PYTHON*` before it collects. Same finding, same
  authorization as the row above. Maintainer-only ceremony code
  (`scripts/reanchor_ceremony.py`, `bootstrap/reanchor.sh`, the launcher
  template); the review did not examine those files, so a reproduction comes
  first.
* **Close GitHub #2 and #8 after their fixes are pushed.** The local
  neutrality/slot-note work and #8's engine half (`dev/plans/archive/engine-batch-f8-slots.md`)
  are archived; this is tracker follow-through, not permission to push or close
  issues now. #16 was already closed before its paragraph landed; changing its
  closure reason is the Maintainer's choice.
* **Cold bootstrap acceptance run against the pushed release tag.** Run the
  bootstrap block cold against the pushed tag using a machine and roster not
  supplied by this repository (`dev/plans/archive/release-authenticity.md`,
  `docs/release-process.md`).

## Deferred follow-ups (durable home)

Deferred candidates return to the queue when their revival condition is met.
Their earlier reproductions and deliberation remain in the named records and
this file's history.

| Follow-up | What remains / when to revisit | Evidence or owner |
|---|---|---|
| Agents taking their own review turns (#13) | After a recorded two-agent drive, propose a design meeting MA-2's four conditions; account for stale statuses and multiple holders. | `maintainer-attention` scope delta; issue #13 remains open. |
| Scientific-check doctrine and deliverable axis (#19) | Revisit when the third-party trial moves, or on Maintainer direction after about ten real non-N/A checks across two projects. Guidance shipped; the doctrine sentence, axis, disciplines and governance reframe did not. | `independent-scientific-check` C1 and archive; issue #19. Details below. |
| Watch the new review header | After ten proposal reviews, the goodnight scrub owner checks premise/alternative challenges, agent-selected outside reads, thin evidence and lost scope challenges. Put a concerning pattern to the Maintainer. | `review-stance-and-lenses` archive; quoted authority below. |
| Watch how far proposals written at medium hold up | After ten proposal reviews, the goodnight scrub owner compares proposals written at medium with those written at high. If fewer than three of the ten were written at high, report counts only and say the comparison is not available. Put a concerning pattern to the Maintainer. | `model-tier-rules` archive (R5); the Maintainer's 2026-10-26 answer lowered proposal authoring to medium. |
| Report only live slots after the module merge | The second form of the install-report change: print the report after the module-merge pass and drop the slots the install fills itself, so `solo-greenfield` shows 20 rather than 20 plus 2 listed apart. Not built because it moves output a frozen test pins; reason: over the cost bar. Revisit with the next change to that test. Authorization, verbatim: "Accept, leave 2 slots counted (Recommended)" | `engine-batch-f8-slots` archive, Scope delta. |
| Decision rights after agreement removal | Offering Cairn's unsure-case rule to adopters needs its own proposal. Revisit lifecycle escalation wording when a concrete conflict reaches a decision. Neither ships in the 0.4 removal. | `remove-collaboration-agreement` Decision Q3; authority quoted below. |
| Stable section identity and complete-set claims | A second actual rule needing section-set completeness would revive this; naming sections and proving all were handled are one scope. The retired lifecycle checker is not a promised future satisfier. | `2026-08-20-claude-review-loop-termination`, Deferred work. |
| Entry-page feature claims drift | A second stale feature list, or an adopter hitting one, may justify a doc-drift rule. | `dev/strategy/archive/2026-08-10-claude-documentation-enhancement.md` fold-up candidates. |
| Withdrawal ledgers can lose the reasoning | Synthesize on an independent recurrence or a Maintainer call; preserve the distinction between a corrected contract and a summary that re-derives its rejected argument. Also test invariants against their claimed space, not vacuous wording. | `scanner-claim-scope` revisions/reviews; original observations Aug 20. |
| Delegated verification multiplies broad runs | On the next fan-out plan or change to brief composition, reassess the working practice: the spawner verifies after joining; leaves receive scoped tasks. The run ledger was retired, so there is no promised collector. | `review-efficient-lifecycle` H1 observations, Aug 13–19; board history contains the 13-run count and its limits. |
| Pre-reviewing a revision | Revisit on a justified later proposal-review round or a Maintainer choice of workflow. Earlier probes found defects but one fix silently reduced accepted scope; every suggested fix still needs the purpose/scope check. | Aug 19 observations; no new review round or doctrine is authorized here. |
| Complete-contract revisions silently omit sections | A third instance or routine synthesis may justify carrying forward a section inventory. The omission ledger did not detect its own omissions; there is no live lifecycle checker to extend. | Aug 19 two-instance observation; the earlier local mitigation was a heading inventory. |
| Dispositions go stale between commits | An independent recurrence may justify recording the measured commit with a disposition. No doctrine change is authorized by the original one-session evidence. | Aug 19 figures/dispositions observation, formerly under first re-anchor ceremony. |
| Shared working-tree writes | Revisit on a second same-file collision: path-scoped commits protect the index but can still collect another session's uncommitted text in the same file. | Aug 12 observation; separate from index hygiene. |
| Re-anchor launcher check by the tool (A2), after the hand ceremony | Before M2, after the hand ceremony anchors the template: `repin ceremony` reads the template from the anchor's signed tree, fills the one slot with the packet's digest, and refuses unless the launcher in hand is byte-equal. Edits `scripts/repin.py` and both repin test files, so it needs its own plan and code review; M2's `--reviewed-commit` then names that review's last commit, not `5293f570`. | Maintainer, 2026-10-27, Decision on the repin-hardening proposal: "Accept all defaults (Recommended)" (build A2 after the cut and before M2). |
| The ceremony driver's three stale spots (R6b's writer) | With R6b, which edits `scripts/reanchor_ceremony.py`: the docstring at line 163 ("NOT itself a closure member" is false now), the undefined name `template` at line 176 (a latent `NameError`), and the "delivered out of band" print at line 743. None is a deletion-only fix, so each owes its own review; the Maintainer signs the driver with them until then. | Maintainer, 2026-10-27: "Accept all defaults (Recommended)" (the repin-hardening Decision defers C, D and I; the driver stays an operator path until D). |
| Edit-check test gaps and one fail-open window | Revive at the next edit to the edit check in `bootstrap/_scaffold/upgrade.py`, or when a project is reported to lose an edit. Three non-blocking findings from the edit-check code review: (1) a `git` that answers some calls and then stops starting reads as "no guard", so `--apply` overwrote an edited file in the reviewer's test; a project cannot cause it, a `git` earlier on `PATH` is already trusted, and the review treated it as not a deviation; (2) no test pins the `.git` file half of the repository look (a linked work tree or submodule); (3) no test pins a hang at `git --version` alone. Not simple: (2) and (3) are new tests with new stand-ins on a trust surface, and (1) is a design call. | Maintainer, 2026-10-26: "On those other issues, Queue them if it's not simple to fix them now. No need to generate more work for us later." |
| Last stray finding ids | Fix after the thirteenth change's code review closes, because that change is editing the file: `(R5)` in `bootstrap/_scaffold/SECURITY_MUTATIONS.md` line 70 (an id into an ended review). Left alone on purpose: `SR-1` as the name of the integrity preflight inside the frozen script `templates/modules/team-gated/run_security_audit.py` and a comment in `bootstrap/_scaffold/config.py` (live vocabulary the script itself defines; editing a frozen file owes a re-anchor entry). Six shipped module docs had `B3`, `SR-1`, `R1` or `P4`; corrected 2026-10-27 in `e24d9ebd`. | Maintainer, 2026-10-27: "Please correct those cases you've found". |
| Stage re-pins in a sterile temporary worktree | Revisit if the dirty-tree refusal blocks the Maintainer twice. At 5 protected-path commits since the last pin it was not a bottleneck. | Same proposal, item G; `repin-build` proposal, "What is not carried". |
| Warn at session start when a pin is stale | Revive if a stale gate manifest or AST baseline goes unnoticed again. Needs a threshold with evidence behind it (the proposal's 25 commits is a guess). Cairn's tools warn, they do not block. | Same proposal, item E. |
| Test the checker's internal messages that the launcher does not print (re-anchor ceremony) | Revive on the first ceremony refusal the operator's screen did not explain, or the next edit to `bootstrap/reanchor.sh` or the launcher template after the closure change and the claim deletion land. Reading the launcher against the checker's messages is a Security Review matter. | `dev/proposals/archive/2026-10-27-claude-repin-ceremony-hardening.md` item I (Q9); the archived repin note. |
| Context-aware quickstart | Propose a trimmed scaffold next-step path when the adopter need recurs. | `adopter-entry-doc-refresh` deferred follow-up (Jun 2026). |
| More adopter-facing count checks | Extend the existing verify-count guard beyond the quickstart's two counts when another live count needs it. | `adopter-entry-doc-refresh` deferred follow-up (Jun 2026). |

Authorizations for the first, second and fourth rows are in their archived
plans (`maintainer-attention`, `independent-scientific-check`,
`remove-collaboration-agreement`). Monitoring authority, verbatim:

> "Yes, we should keep watching."

> "Keep the monitoring row (Recommended)"

The surviving shared-working-tree observation came from the first-ceremony
batch, retained under this authorization:

> "Yes, go ahead and close everything else from these two plans out, including
> finding a permanent home for any remaining items"

### External correctness trial and scientific-check evidence

A consenting scientific repository that did not contribute the doctrine still
needs to run the bootstrap end to end. **It does not block 0.4 publication**
(waived 2026-10-19: *"Waive it for 0.4 — Go public once the batch lands. The
README says plainly that it hasn't yet had an outside test."*), and that
release waiver is not a completed trial. Revival: enroll a willing third
party. This also revives the scientific-check/axis review (#19).

The C1 blind trial covered two plans. One check targeted a different real risk;
the other was drafted with and without a data-status prompt. It did not
establish that the guidance catches later errors or validates the independent
basis. The Maintainer superseded the original stop result; the saved C1 and
archive records retain the drafts and scoring.

At revival, retain the six falsifiers: every failing check was already caught
elsewhere; most bases are an author's own expectation; assumption-changing
work claims N/A; failing runs are absent or irreproducible; checks only repeat
what code review catches; or a no-effect result has no positive control or
stated inability to supply one. No failure and no later error is inconclusive.
Watch for post-code checks, expectations changed to fit results, false
"data in hand" claims, ritual checks on tooling, new discipline lists, and
checks that neither need data nor say what evidence was opened. Nothing
counts these automatically; issue #19 and the Maintainer's review remain the
reminders.

## Onboarding

The original reading/tour seeds remain unconfirmed. The installed-hook task
is complete (`python tools/intent.py hooks-status`, 2026-10-19); the retired
signing seed is covered by the live agreement-removal plan and is no longer
a separate task here. These remaining seeds request no extra ceremony.

<!-- cairn:slot onboarding-tasks -->
<!-- preset: collaborative-team -->
* [seed; id: try-session-start-skill]
  Try the session-start skill; its implementation is `tools/session.py`.
* [seed; id: read-lifecycle-doctrine]
  Read `doctrine/lifecycle.md` for the proposal/plan lifecycle.
* [seed; id: read-coordination-doctrine]
  Read `doctrine/coordination.md` for shared-tree coordination.
* [seed; id: read-dual-review-module]
  Read `dev/modules/dual-review.md`; fresh independent review is the standing
  procedure, and an outside read is the Maintainer's call.
* [seed; id: walk-dev-tour]
  Read `dev/modules/onboarding/dev-tour.md` for the worked lifecycle example.
* [seed; id: agent-team-onboarding]
  Review capability tiers and commit attribution with
  `dev/modules/onboarding/agent-team-onboarding.md`.
<!-- cairn:end onboarding-tasks -->

## Security-cluster routing

Security residuals and their revival triggers live in
`dev/strategy/2026-08-05-codex-security-strategy.md`, under **Live residual
register**. Its Cluster map decides when findings are one scope; the owning
plan carries reproducers and evidence. Add a board task when a trigger fires,
rather than duplicating the residual register here.

## Archive preconditions (proposals and plans)

Board housekeeping follows `dev/plans/_template.md` > Dispositions and
`doctrine/lifecycle.md` > Archive precondition. Completed rows leave once their
record is durable; unresolved tasks keep a real live home. An archived plan
is evidence, not a place to hide work still owed. Deferrals retain the
Maintainer's quoted authorization and a named live home.

For the board's self-contained scope vocabulary: **a scope-cut removes no
work**; removing a baseline outcome **is a scope reduction**, tested against
the commitments as *opened* before Decision and as *accepted* afterwards.
It takes one **grouped scope-remainder record** and **only the Maintainer may
concede** that loss. Completed and duplicate entries leave the board.

## Status taxonomy

Use `queued` for work not started, `active` for in-flight work, `blocked` for
an actual named dependency, and `deferred` with a revival condition. Completed
work is removed after migration. Mark a Maintainer-only next move with the
literal header spelling `**Waiting on Maintainer**: <what>` inside its row;
the board command reads that declaration, not an inferred need for approval.

## Removal preconditions

Confirm completion and its durable record before removing a task. For the
full lifecycle rule, see `doctrine/lifecycle.md` > Removal preconditions for a
roadmap item. Keep current tasks here and evidence in the source records.
