# Cairn's adopter-facing audit — what a skeptical outsider would find

**Author**: Claude (Strategy)
**Model**: Claude Fable 5
**Date**: 2026-07-08; merged with the 2026-06-12 adopter-friction audit and
cut to its live core 2026-08-26
**Status**: settled
**Type**: product-strategy
**Surfaces this feeds**: `2026-08-20-claude-adopter-path-consolidation` (the
adopter-path owner); `2026-08-05-codex-security-strategy.md` (the security
owner); the GitHub issues board; the eventual first-adopter probe protocol.

**Merge note, 2026-08-26.** This note now carries both of Cairn's
adopter-facing audits: the 2026-07-08 broad look and the 2026-06-12
adopter-friction audit (its full text is preserved at
`archive/2026-06-12-claude-adopter-friction-audit.md`). Per Maintainer
direction — *"Having it as some checklist is not important... we don't need
to keep the historically checked off stuff"* — the item-level inventories,
phase checklists, and findings that have since been implemented are dropped
rather than carried: git history, the archived plans under
`dev/plans/archive/`, and this file's own prior revisions record what was
found and what fixed it. What remains here is what is still live, and what
is worth keeping permanently.

## The two questions

The broad look asked: **if a skeptical, technically competent scientist
spent an afternoon poking at this repository — reading the claims,
re-running the checks, walking the install — what would they find, and
which findings would cost us the first adopter or the launch?**

The friction audit asked the complementary question: **can a solo scientist
move from curious, to trying Cairn, to using it on a real repository — and
explain what they have installed and agreed to — without an author beside
them?** Its four transitions (try → choose → install → understand) remain
the right frame for any future entry-path work: a project can have a good
README, a working installer, and a tested quickstart, and still lose the
adopter in the handoffs between them.

## How this was reviewed

The broad look ran ~150 independent reading passes in three waves — surface
mappers, skeptical reviewers from seven distinct angles, then verification
passes whose only job was to refute each finding (serious findings faced
three attackers); only survivors were reported, and the most surprising were
reproduced end-to-end. The friction audit did a measured cold install on the
canonical interpreter against an exact commit, running every published
command and comparing the documented state to the real one. Both notes
recorded later falsifications in dated corrections rather than silent edits;
the lessons from those corrections are kept below.

## What survived attack — still true

Calibration matters as much as findings, so the record of what *held*
stays:

* **"No dependencies" is true** — every shipped Python file is
  standard-library only.
* **The installer's core safety engineering is genuinely good** —
  containment and symlink defenses hold under direct attack; the
  security-minded reviewer would run it on their own machine.
* **The install contract has actually held** across releases.
* **When the deliberation process runs, it demonstrably works** — audited
  recommendations were implemented, and the review trail shaped real code.
* **The honest-voice branding is consistent**, including "slower at first."
* **The trial path works** — the quickstart's counts are guarded by live
  tests, and default-on security reports honestly rather than claiming
  success over nothing.

## The strategic insight, from both audits

The broad look's pattern was an inversion: **the machinery is better than
the paperwork describing it, and better than the record showcasing it** —
a strategic problem for a methodology whose product *is* the paperwork and
the record. The friction audit sharpened it one step later in the funnel:
**the trial works, but the handoff to real adoption does not** — the
recommended lightweight path had no executable recipe, while the working
installer was labeled as the heavier level. A path is not lightweight
merely because its automation was removed.

Both audits converge on the same root causes the 2026-08 refocus
(`2026-08-21-claude-nimbleness-recovery`) now attacks by subtraction:
hand-maintained descriptions of things that change, and comprehension load
outgrowing the path it governs. Less described surface drifts less; fewer
words are easier to hold.

## What is still live

* **The adopter path** — the merged headline. One installer for every
  non-zero adoption level, with levels distinguished by what the adopter
  must read, decide, and can reverse — not by whether bytes were copied by
  hand. Owner: `2026-08-20-claude-adopter-path-consolidation`
  (awaiting-review). The populated-repository install — both audits' most
  demanded rehearsal — has since been built and exercised
  (`dev/plans/archive/adopt-into-existing-tree.md`). Quickstart command
  hygiene (path-scoped commits; a staging list that matches the installed
  state) rides with the consolidation rather than as separate items.
* **Comprehension over mechanics.** The comprehension floor now ships in
  the installed contract (`templates/core/AGENTS.md`, "Comprehension is a
  precondition of the Decision"). The live half is measurement: before the
  one-shot first-adopter test, one walk by someone who did not author the
  entry docs, recording elapsed time, warnings, undocumented interventions,
  every term they had to look up, and whether they can restate Cairn's
  purpose and their obligations *in their own words*. Completing the
  commands does not establish understanding, and no current canary asks.
* **Documentation drift is an undetected class, not a backlog.** No gate
  catches a dead exemption, a count fallen behind its source, or a claim
  contradicted by the file it cites — the class regenerates. The refocus's
  answer is structural, not another detector: shrink the described surface,
  keep the checkers de-scoped and quiet, sample with the warn-only audit
  reporter.
* **Security** — superseded wholesale into
  `2026-08-05-codex-security-strategy.md` (its "Theme 3 migration" table
  maps every original finding). That document owns all of it.
* **Windows** — still an undecided Maintainer question: support it (a small
  always-LF-endings fix plus a seeded git-settings file) or state "native
  Windows unsupported — use WSL" in the contract and quickstart. Today it
  fails silently, which is worse than either answer.
* **The reviewer's question** — "how is this different from decision
  records, RFC processes, lab notebooks, pre-registration?" The real
  answers (review *before* code is written, across genuinely different
  models; verification plans locked in advance; the record in the repo, not
  a chat log) still appear nowhere a skeptic looks first, and the
  two-sentence pitch still does not exist. Unowned; the natural next home
  is a Cairn issue when someone picks it up.
* **Upgrade reality.** A cross-version upgrade of an installed Cairn has
  still never been rehearsed end-to-end. The subtraction sweep's sister
  migrations will be the first forced, real exercise of adoption-surface
  change; what they teach should be captured then, not speculated now.
* **The zero-rejections optic** — "51 proposals, zero rejections, same-day
  approval" reads as theater to a skeptic. The record has since gained its
  rebuttal (4 supersessions, and review rounds that demonstrably block work
  as written — see `2026-05-20-claude-team-productivity-metrics.md`), but
  the honest explanation — bad ideas die in conversation before a proposal
  is written — should be stated wherever the numbers are shown.

## Decisions that were open then, and where they stand

* **CI** — decided by the refocus, in the opposite direction the broad look
  recommended: no CI; every trigger named at its real strength; the
  security suite is release-only, Maintainer-run. The honest-trigger
  doctrine in `AGENTS.md` is the durable form of this answer.
* **Identity** (methodology-without-the-software: supported or not), **the
  first-adopter probe** (formal gating test with protocol and consent, or
  friendly rehearsal), and **Windows** — still the Maintainer's, still
  open.
* **Level semantics, the accepted profile's durable home, and the timing
  claim** — to be settled at `adopter-path-consolidation`'s Decision.

## Lessons worth keeping (fold-up candidates, both audits)

* **A claim that checks passed is a claim like any other** — release notes
  carry the machine output of the checks, never a summary from memory.
* **Any scanner's target list derives from the list the installer uses** —
  every coverage hole found was a hand-copied list that fell behind.
* **Tests must not depend on today's date** — a suite that reddens by
  itself teaches people to stop reading failures.
* **A commit's message must match its contents** — a cheap check that
  "adds review" actually adds a review would have caught the worst
  record-integrity finding at commit time.
* **An adoption level should name human obligations, not whether bytes
  were copied by hand.**
* **Progressive installation and progressive attention are different** — a
  file may be present without demanding a day-one decision; report what is
  live now, not everything that exists.
* **A test that claims to exercise a published command must execute that
  command vector and assert its residual state** — testing adjacent output
  is coverage, not evidence the recipe works.
* **Name the interpreter with every suite figure** — two honest agents on
  one tree got materially different results because the instruction named
  no interpreter; the reproducibility defect was in the instruction, not
  anyone's diligence. (Now doctrine in `AGENTS.md`.)
* **A deferral names a future artifact, and nothing resolves those** — four
  artifacts each deferred the same core to a proposal that did not exist,
  by name, and no checker notices. Deferrals need owners that exist, which
  is why the refocus routes deferred work to the issues board.

## Corrections record

Both audits recorded their own falsifications in dated corrections rather
than silent edits — the Bandit "runs nowhere" claim (wrong: measured on a
non-canonical interpreter), the suite baselines inflated the same way, and
a documented test command that was red on any clean checkout (since fixed).
The full correction entries live in this file's git history and in the
archived friction audit; their durable lessons are in the list above. The
convention itself is the keeper: **a strategy note that asserts findings
owes a dated correction when one is falsified.**
