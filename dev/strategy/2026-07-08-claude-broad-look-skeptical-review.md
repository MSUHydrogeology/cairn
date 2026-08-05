<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/dual-review.md doctrine/proposals.md doctrine/lifecycle.md doctrine/runtime-contract.md doctrine/doc-governance.md doctrine/README.md reason=doctrine/ citation convention -- references resolve locally in Cairn's self-hosted tree -->

# Cairn v0.3 broad look — what a skeptical outsider would find

**Author**: Claude (Strategy)
**Model**: Claude Fable 5
**Date**: 2026-07-08
**Status**: settled
**Type**: product-strategy
**Surfaces this would feed**: the tighten-up proposal series scoped in
the Recommendation below; the `dev/PLANNING.md` broad-look / 0.4-gate
items at the next serialization point; the R-H probe protocol.

## The question

We are about to hand Cairn to its first real outside user — a postdoc
in the lab, probably bringing an existing research codebase — and then
take the repository public at version 0.4. That first adoption doubles
as the third-party test that gates the public release, and it is
one-shot: there is exactly one candidate.

So the question this review answers is not "is Cairn good?" It is:
**if a skeptical, technically competent scientist spent an afternoon
poking at this repository — reading the claims, re-running the checks,
walking the install — what would they find, and which of those findings
would cost us the first adopter or the launch?**

This note is the "broad-look + tighten-up pass" that has been queued on
the roadmap since Cairn began running its own methodology on itself. It
deliberately skips ground already covered: the 2026-06-12 quickstart
friction audit (all of whose fixes have landed) and the two known
quality-check issues already filed on GitHub (#1 and #2).

## How this review was done

* **A large automated audit, built to be hard on itself.** About 150
  independent reading passes went over every part of the repository,
  organized in three waves. First, seven mappers each read one surface
  closely (the public-facing claims, the strategy documents, the
  methodology doctrine, the installer code, the shipped templates and
  examples, Cairn's own self-hosted `dev/` tree, and a live re-run of
  every quality check Cairn defines for itself). Second, seven
  skeptical reviewers each attacked from a different angle — a
  methodologist, a fact-checker, a program auditor, a research-software
  engineer with a security bent, a technical-writing editor, a
  journal-style reviewer, and a simulated version of the postdoc
  walking their first two weeks. Third — and this is the part that
  makes the findings trustworthy — **every finding was then handed to
  separate verification passes whose only job was to prove it wrong**:
  re-checking the cited evidence line by line, asking whether it
  actually matters at this stage of the project, and searching the
  repository for an existing answer the reviewer might have missed.
  Serious findings faced three independent attackers. A final
  "what did everyone miss?" critic then commissioned six follow-up
  sweeps (licensing, the code that runs every day in an adopter's
  repository, whether the multi-tool claims are tested, the upgrade
  path, Windows support, and the installed command-line tools).
* **Only findings that survived are reported.** Roughly one hundred
  did; three were successfully knocked down (and, encouragingly, all
  three died because the repository already had a good answer). A few
  of the most surprising ones were additionally reproduced end-to-end —
  actually running the installer with the problem input and watching it
  fail.
* **Everything was re-checked by hand against today's repository**
  (2026-07-08, commit `d789414`), because the automated audit ran
  before the recent quickstart fixes landed. Anything those fixes
  resolved was dropped.
* **Cairn's own quality checks, re-run today:** the test suite has
  **3 failures out of ~1,400 tests** (the two known baseline failures
  from issue #1, plus one brand-new failure explained in Theme 3); the
  documentation-integrity check passes; the vendor-neutrality check
  fails with 99 findings; the dead-code check fails with 10 findings.
  The newest release tag, `v0.3.0`, is now 20 commits behind the
  current code — including all the quickstart fixes.
* **How to check me:** every claim below names the file (and usually
  the line) where the evidence sits, or the command that reproduces it.
  This note itself passes Cairn's claim checker
  (`scripts/claim_check.py`).

## Corrections since publication

*This note asserted findings; where later evidence falsifies one, the correction
is recorded here rather than quietly edited away. A strategy note is
inline-revised, so the text above is corrected in place — this section says what
changed and why, so a reader who acted on the original knows.*

**2026-07-22 — the Bandit claim (Theme 3, finding 1) was wrong.** The original
text said the scanner "runs nowhere" because it "isn't installed locally". That
was measured on a **non-canonical interpreter**. The canonical development
environment (Python 3.13.13 — the version the gate manifest pins) has `bandit`
1.9.4 installed, and the Bandit-dependent tests **run and pass** there rather
than skipping. The finding is narrowed, not withdrawn: there is still no CI, so
nothing enforces the scan on a push — the guarantee rests on a human
remembering, which is a real gap, just a smaller one than published.

**The same measurement error inflated other numbers in this note.** Suite
baselines cited here (and in the proposals that quote them) were taken on Python
3.12.9. On one unchanged tree, measured 2026-07-22: the canonical 3.13.13 gives
**2 failed / 1435 passed / 0 skipped** with **3** real AST drifts, while 3.12.9
gives 2 failed / 1429 passed / 3 skipped plus *hundreds of spurious* AST
mismatches — `ast.dump` structure varies across Python minors, so the
attestation reports phantom CHANGED symbols off-canon. Treat any suite figure in
this note as approximate and interpreter-dependent unless it names its
interpreter.

*Root cause worth keeping:* the instruction agents follow (`python -m pytest
bootstrap/tests`) names no interpreter, so two honest agents on the same tree get
materially different results and both report them as fact. That is a
reproducibility defect in the instruction, not in anyone's diligence.

## The good news first

A skeptical review is only useful if it is calibrated, so here is what
*survived* attack:

* **"No dependencies" is true.** Every Python file Cairn ships to an
  adopter uses only the standard library — verified by listing every
  import. An adopter takes on nothing beyond Python itself.
* **The installer's core safety engineering is genuinely good.** Every
  file it writes into an adopter's repository goes through checks that
  refuse to write outside the repository or through symlink tricks; the
  parsing of template files stops rather than guesses when something
  looks wrong; the tests attack these defenses directly and the
  defenses hold. The security-minded reviewer's verdict: comfortably
  above typical research-software standards, and they would run it on
  their own machine.
* **The install contract has actually held.** The promise that the
  installer behaves identically across releases checks out: the only
  change to the engine since v0.3.0 is four lines of message text.
* **When the deliberation process actually runs, it works.** Every
  recommendation from the June complexity audit was demonstrably
  implemented. The two internal case studies are real, and the review
  trail in the reference project genuinely shaped the code.
* **The honest-voice branding is consistent** — the "this will be
  slower at first" admission appears everywhere it should, and the
  document explaining what Cairn is *not* (not a test framework, not
  CI, not a prompt library) is exactly right.

The pattern in everything that follows is therefore *not* "the
machinery is hollow." It is nearly the opposite: **the machinery is
better than the paperwork describing it, and better than the record
showcasing it.** For a methodology whose entire product *is* the
paperwork and the record, that inversion is the strategic problem.

## Findings — eight themes

### Theme 1. The record doesn't always match what actually happened

Cairn's core promise is a trustworthy record of decisions — the lab
notebook for AI-assisted development. The audit did what any careful
reader of a lab notebook does: checked whether the entries match the
dates and the data. In the showcase instances, they don't:

1. **The first worked example's history describes events that didn't
   happen that way.** The commit that "opened" Cairn's first self-run
   proposal (`17b7e5c`) already contained the two reviews that were
   supposed to come later — while the proposal's own status line still
   said "proposed." The next commit (`f4a8308`) says in its title that
   it adds the external review, but it adds no review at all (its
   entire content is a two-line bookkeeping edit). What probably
   happened is innocent — the discussion happened in a chat session and
   was written up afterwards in a batch — but the record doesn't say
   so, and an outside reader cannot distinguish "written up afterwards"
   from "fabricated." This is the first proposal a new adopter would
   study to learn the method.
2. **The v0.3.0 release notes claim checks passed that did not pass.**
   The release commit (`12ec2ad`) states that the quality gate passed
   cleanly. Re-running that exact gate on the exact released code —
   done independently three times during verification, and once more by
   hand today — produces 99 vendor-neutrality failures and 6 dead-code
   failures. In journal terms: the methods section says the calibration
   was verified, and the calibration log shows it wasn't.
3. **The release checklist we wrote for ourselves was skipped.** The
   strategy document that declares a comprehensive pre-release sweep "a
   standing Cairn practice"
   (`dev/strategy/2026-05-27-claude-cairn-pre-release-sweep.md`) has
   sweep records for v0.2.0 only. No sweep ran for v0.3.0 — and the
   exact kind of documentation staleness the sweep exists to catch is
   what shipped in v0.3.0 and had to be fixed afterwards.
4. **A pointer to a decision record leads nowhere.** Both the install
   record (`dev/.cairn/profile.yml`) and the roadmap say the reasoning
   behind Cairn's own adoption choices "lives in dev/strategy/". No
   such document exists there.
5. **We bent our own review rules within hours of adopting them, and
   nothing noticed.** One review was done in the same working session
   as the writing (our rule requires at least a fresh session); one
   required plan review was quietly waived without the sign-off the
   proposal promised. Neither event was recorded as an exception. If
   even the authors can't sustain the rules, either the rules are
   heavier than they need to be or compliance needs an automatic check
   — leaving it ambiguous teaches every future user that the rules are
   decorative.
6. **On the numbers we have, review has never said no.** Across the
   only measured record (51 proposals in the reference project): 49
   accepted, 0 rejected, 0 superseded, typical time-to-decision the
   same day. Review demonstrably *improves* things (about 8 findings
   per review, nearly every proposal revised) — but a skeptic reading
   "51 proposals, zero rejections, same-day approval" will say the
   adversarial part is theater, and today we cannot rebut that with
   data. (The honest explanation — bad ideas die in conversation before
   a proposal is ever written — is real, but it is written down only
   obliquely.)

None of this is expensive to fix. But every item is checkable in
minutes, sits in the exact place a skeptic will look first, and touches
the differentiator rather than the periphery.

### Theme 2. The documentation describes a repository that no longer exists

The same failure the quickstart audit found — documentation quietly
falling behind the tool — turns out to be repository-wide. A dozen
verified examples, all live today:

* **The published module lists are wrong.** The installer actually
  offers 20 modules (6 installed by default, 14 optional). The module
  catalog (`templates/modules/README.md`) documents 12 of them; another
  index lists 3; the two case studies give counts that contradict each
  other *and* the installer; and the bootstrap guide's worked example
  (`bootstrap/BOOTSTRAP.md`, Appendix B) still lists half the default
  set — and the installer accepts such a list silently, so a user
  copying that example loses half the method without knowing.
* **The doctrine's own table of contents covers half the doctrine.**
  `doctrine/README.md` maps 8 of 16 files — omitting, among others, the
  two documents a new adopter most needs (how proposals and plans
  work) — while stating the core "is small by design."
* **The documentation-placement guide is wrong about its own
  repository.** `docs/DOCUMENTATION_PLAN.md` — our showcase for the
  "keep docs from drifting" module — still says in five places that
  Cairn does not yet run its own methodology (it has since June), and
  misstates where three top-level files live. Because of a stylistic
  quirk (it prefixes paths with `cairn/`), the claim checker cannot see
  any of its path claims — the one document that polices placement is
  the one document the path checker cannot police.
* **The changelog announces a public release that never happened.**
  `CHANGELOG.md` line 2044 declares an "Initial public release" in May;
  the repository has never been public. The README calls v0.3.0
  "released" with no qualifier. Both contradict our own release plan.
* **The citation file misdescribes the project.** `CITATION.cff` — the
  metadata a postdoc would paste into a paper — titles Cairn "An
  Adaptable Framework," calls it software (the README's first claim is
  "a methodology, not software"), and omits one of our three licenses.
* **The security document over-promises.** `SECURITY.md` promises an
  integrity check of "every file in your tree"; the actual check covers
  only files listed in the install receipt, and our own install has
  files the receipt doesn't list.
* **A statistic we privately flagged as unverified ships in our
  evidence.** The LHM case study states that "the multi-agent-systems
  literature" attributes 35–57% of failures to coordination breakdowns
  — uncited. Our own internal strategy document carries the same
  numbers with an explicit warning that the primary sources were never
  verified and must be before publication. The case study *is* the
  publication.
* **The rationale document overreaches.** `doctrine/rationale.md`
  promises that "every practice traces to a reason here," but six
  doctrine files are never mentioned, and it cites a rules file that
  doesn't exist in this repository.
* **The vendor-neutrality claim is contradicted by what we ship.**
  Files installed into every adopter's repository carry named AI
  vendors in their comments, and the tracked issue (#2) mischaracterizes
  the problem — it says all 99 findings are in one directory of
  harness-integration files, when only 17 are; the rest are in shipped
  modules, docs, and the doctrine itself. A cleanup based on the issue
  as written would declare victory while the main problem remained.

The root cause is the same as the quickstart's: these are all
hand-maintained descriptions of things that change, with no automatic
check that fails when they fall behind. The drift-gate just built for
the quickstart is the right pattern — it currently protects two numbers
on one page.

### Theme 3. The security story is ahead of the security practice

**Superseded as a current work list on 2026-08-05.** The original findings stay
visible below, struck through so historical citations still resolve. Their
implemented, partial, and remaining dispositions now live in
[`2026-08-05-codex-security-strategy.md`](2026-08-05-codex-security-strategy.md)
under **Theme 3 migration**. A strike means *migrated*, not necessarily *fixed*.

1. ~~**A promised automatic check isn't wired to anything automatic.**
   *(Corrected 2026-07-22 — see the correction note below; the original
   claim, that the scanner "runs nowhere", was wrong.)* Several documents
   say the installer engine is guarded by a code-security scanner
   (Bandit), with tests that "fail in CI" if the scanner is missing.
   There is no CI — no automated checks run on this repository at all —
   so nothing enforces the check on a push. But the scanner **is**
   installed in the canonical development environment and the
   Bandit-dependent tests **do** run there; it also exists in the
   release script, run by hand. The real gap is narrower than first
   stated: the guarantee depends on a human remembering, not on the
   check being absent.~~
2. ~~**The release security scan misses the code that runs most often.**
   The scan builds its target list from two of the installer's three
   internal file lists. The third list — which ships the session
   tools that write into an adopter's repository *every single working
   day* — is not consulted. So the ~2,400 lines of code an adopter
   executes most frequently are exactly the lines the security gate
   never scans, while `SECURITY.md` says it covers "the shipped Python
   surface."~~
3. ~~**The one place the installer guesses instead of stopping.** The
   configuration file an adopter writes (the "profile") is the
   installer's main input, and it is the one input handled forgivingly:
   a misspelled keyword is silently ignored (a typo in `preset:` gets
   you a silently different installation), and on machines without the
   optional YAML library, the built-in fallback parser reads certain
   ordinary lines differently than the real parser would — including
   the example printed by the installer's own `--help`.~~
4. ~~**Our dead-code detector cries wolf.** All ten of its current
   alarms are false — it doesn't recognize one of Python's ordinary
   import styles, so it flags live, security-critical functions and
   advises deleting them. An alarm that is always false trains everyone
   to ignore it, which buries any real alarm.~~
5. ~~**A tools help-text says "read-only" about a command that writes.**
   The daily orientation command's help claims it only reads and that
   every writing command has a preview mode; in fact it repairs links,
   edits `.gitignore`, and moves files at startup, with no preview
   option.~~
6. ~~**New this session — the test suite now fails from the passage of
   time alone.** One test bakes in June 2026 dates and checks them
   against a 14-day window measured from *today's* clock
   (`templates/modules/default-on/evolution_infer.py:281` uses the real
   date with no way to override it). The test passed in June and fails
   now, with zero code changes. For a project preaching "run the tests
   after every change," a suite that turns red on its own is corrosive:
   a permanently red baseline teaches people to stop reading failures.
   (A ready-to-run fix task was spun off during this review.)~~

### Theme 4. Anyone who adopts Cairn ends up violating our own licenses

This one surprised me, it was verified from every angle, and it should
block the public release until fixed:

Cairn's code is MIT-licensed and its documents are CC-BY-licensed. Both
licenses have exactly one real requirement: *keep the notice / give
credit*. But the installer copies dozens of code files and a whole tree
of documents into the adopter's repository **with no license text, no
credit line, no link back, and no mention anywhere in any adopter-facing
document that an obligation exists.** It even keeps a hidden folder of
verbatim template copies in the adopter's repository. The install
receipt records file fingerprints but not who made the files, under
what license, or where they came from — and in our own installation,
the "which version of Cairn" field just says "unknown."

Concretely: the day the postdoc makes their repository public alongside
a paper — the normal, desired outcome — they are redistributing our
code with its required notice stripped and our prose with no
attribution. They'd be violating our licenses without any way of
knowing. It is the equivalent of shipping someone's dataset without
the citation their data-use agreement requires — done to every adopter,
by default, by our own installer.

The fix is small: install one notice file carrying both license blocks
(and record it in the receipt); add a standard two-line license label
to the top of each shipped code file, which then travels automatically;
add one "what you owe, and what you don't" paragraph to the bootstrap
guide; add one sentence accepting contributions under the same
licenses. And one genuine decision for the Maintainer: we could add a
clause to our license that says *keeping the notice file is all an
adopter ever owes us* — which converts a legal-compliance question a
scientist can't easily answer into "don't delete this one file."
(A follow-up sweep also noticed our license split covers code and
prose but never mentions the shipped configuration/data files — worth
one clarifying sentence.)

### Theme 5. The path we've built is not the path the postdoc will walk

The quickstart fixes polished the demonstration path: new empty
project, defaults, toy example. Our actual first adopter is a solo
scientist with an *existing* codebase, a second AI tool for reviews, a
deadline, and a PI (you) reading over their shoulder. That path has
verified gaps at nearly every step:

1. **No installation preset fits them.** The presets and the levels
   documentation disagree about the solo-scientist-with-existing-code
   case; a user who overrides settings to say "legacy codebase"
   silently *fails to get* the legacy-specific modules our own doctrine
   says that situation needs; and the documented fallback starts from
   the stale half-a-list example in Appendix B.
2. **The shipped starter guide teaches them to mislabel their reviews
   — corrupting the record from day one.** The solo onboarding file
   (`templates/onboarding/solo-greenfield.md:76`, and again at line
   115) says that re-checking your own work in a fresh session counts
   as the *External* (independent) review tier. Our doctrine says
   explicitly that it does not — external review requires a different
   model or a human. A record that labels self-checks as independent
   review overstates exactly the property we advertise. Three
   independent verifications confirmed this one word-for-word.
3. **The "when do I need a proposal?" checklist omits science.** The
   triage list names software triggers — interface changes, new
   abstractions, file moves — but never *changing a scientific
   assumption, a unit or sign convention, a default parameter, a
   calibration constant*. Yet the readiness assessment calls scientific
   assumptions "the question Cairn is most differentiated on." The
   postdoc's most likely first real change — adjusting a recharge
   default — triages, under our own shipped rule, to "just commit."
4. **The pressure valve isn't installed.** There is a sanctioned
   deadline escape ("urgent, reversible, or experimental changes may
   skip the proposal — just say why in the commit"), but it lives only
   in our doctrine, which adopters don't have locally. Their copy has
   only a pointer to a file that isn't there. In deadline week they
   *will* skip proposals; without the installed rule, those skips read
   as violations instead of the designed flex.
5. **Week one is all cost, and the early payoff we actually have is
   hidden.** The entry documents honestly say "slower at first" but
   never name a first concrete win. We *have* one — "make your first
   proposal a one-page `assumptions` document: signs, units, defaults,
   calibration constants; you, your agent, and your PI will use it
   immediately" — but it exists only as a conditional bullet in an
   appendix of the readiness report.
6. **Nothing addresses adopting under a boss's gaze.** The metrics and
   the readiness report both promise "this is not a scorecard" — but
   the deliberation record itself (rejected ideas, mistakes, review
   findings), fully readable by the PI who is also Cairn's maintainer,
   has no such statement anywhere. A rational postdoc sanitizes their
   record, which destroys the record's value. One honest paragraph
   fixes this.
7. **There's no way out.** The vision document promises "adoption is
   reversible," but nothing anywhere explains how to scale down, pause,
   or uninstall. Since the install receipt lists every installed file,
   a documented (even scripted) removal is cheap — and a visible exit
   lowers the cost of entry.
8. **The two-AI-tools story is untested where it matters.** The
   compatibility table lists every supported AI tool as
   "claimed-but-unverified" — including the two the postdoc will
   actually use. The one empirical confirmation we have was never
   written up as the test record our own protocol requires. The
   onboarding walk for adding a reviewer tool never mentions the one
   step that makes reviews informed — wiring up the file that tool
   reads so it actually loads the project rules — and the wrapper
   file's own example filename is one our upgrade machinery can't
   track.
9. **The one-shot test has no protocol, and we've never rehearsed it.**
   Nothing in the repository names the candidate, what they consent to,
   what we observe, or what pass/fail means; and no queued work
   installs Cairn into a *populated* repository even once before the
   real attempt. Meanwhile `SECURITY.md:25` tells adopters to install
   from a released tag — which currently means a version missing every
   quickstart fix.
10. **The first session breaks in ordinary environments** — verified,
    two of them reproduced end-to-end. If the adopter hasn't created
    the AI tool's config folder yet (the most likely first-session
    state), the session tools are silently skipped, the install report
    hides the skip, and its closing line invites running a command
    (`/good-morning`) that doesn't exist as a command anywhere
    (`bootstrap/_scaffold/cli.py:487`). If the adopter rebuilds their
    conda environment — routine lab life — the daily tools refuse to
    start at all, because the installer memorized the full path to the
    Python that ran it (`bootstrap/_scaffold/install.py:363`) and the
    tools treat "that Python is gone" as a fatal error instead of
    falling back to the current one. And the starter task list is
    copied by preset *name*, not by what actually got installed, so a
    customized install gets day-one instructions commanding tools that
    aren't there.

### Theme 6. We haven't answered the question every reviewer will ask

**"How is this different from things I already know?"** — the first
question from any journal reviewer, any experienced software engineer,
any skeptical PI. Specifically: engineers have kept decision records in
repositories for fifteen years (they're called Architecture Decision
Records); the Python and RFC communities run proposal-review-decision
processes; scientists keep lab notebooks and pre-register studies.
Nowhere — README, doctrine, docs — does Cairn mention *any* of these,
while the vision document calls our approach "genuinely uncommon."
The dismissive one-liner ("so it's decision records plus checklists
plus an installer") is the single most likely way Cairn dies on
contact with a skeptic, and it has real answers we never state: our
review happens *before the code is written*, across genuinely different
models; our verification plans are locked in advance like a registered
report; our record lives in the repository, not in a chat platform's
history. One "related practices" section closes this.

Related credibility items, all verified: the doctrine states the
key premise — that a different AI model brings independent errors — as
fact, without the caveat (which our own README already carries!) that
models trained on similar data share blind spots; the worked example
quotes an impressive cross-model catch-rate with no source or
denominator; "a methodology, not software" coexists with a runtime
contract (`doctrine/runtime-contract.md:122`) declaring the software
mandatory for any supported adoption, while the on-ramp calls the
software-free path "the natural home" for solo adopters
(`on-ramp/README.md:33`) — one of those three statements has to yield;
the "in active use in two real projects" claim offers a skeptic nothing
they can check; there are roughly forty coined house terms with no
glossary; the front page uses internal codes (R-A, R-H, G/M/P,
"chunk 5.3") that resolve nowhere a reader can follow; there is no
plain two-sentence pitch anywhere that a postdoc could repeat to their
PI; and there is no CONTRIBUTING file or support path — the first
thing journal-style software review checks for.

### Theme 7. Our own planning documents have fallen behind

The strategy corpus this review was asked to treat as the statement of
intent has its own housekeeping debt: the metrics document still
carries a review from May that our own rules say should have been
folded in and removed, and it defers to a roadmap section that no
longer exists; the guiding framework document still says "Cairn is at
v0.2.0"; the roadmap simultaneously records your decision to retire the
collaboration agreement *and* keeps a day-one task telling every new
team to invest in it (and the always-loaded rules file still lists it
as required reading); the doctrine cites section headings that don't
exist in the files it points to; the project charter has three
different "official homes" in three documents and no link from
anywhere a reader starts; about 900 words of lifecycle rules are
maintained in duplicate in two doctrine files against our own
one-home rule; and the strategy record still presents the completed
complexity-debt cleanup as pending — underselling a genuine success.

**The upgrade path deserves its own paragraph, because the final
verification pass confirmed all of it.** Upgrading an installed Cairn
across versions has never been rehearsed — not once, by anyone,
including us (our own installation is permanently in a degraded mode
that can't exercise the merge machinery: all 38 of its mergeable files
lack the saved originals the merge needs, and the receipt doesn't even
know which Cairn version installed them). The bootstrap guide actually
teaches the *wrong* upgrade method — a forced re-install
(`bootstrap/BOOTSTRAP.md:310-315`) — and no entry document mentions
that a real upgrade command exists. The first real test of the
"template removed upstream" case is already scheduled (retiring the
collaboration agreement before 0.4), and that case currently has no
tests, no user guidance, and no way to ever clear the leftover record.
The version-compatibility field in the install receipt is written but
never read, so nothing would notice a mismatch. None of this bites
today; all of it bites the first time an adopter tries to update — and
"you can update without losing your customizations" is a core promise.

### Theme 8. On Windows, the installer quietly breaks its own tamper-detection

Windows and Linux/macOS end each line of a text file with different
invisible characters. The installer writes files in a mode that adopts
whichever convention the local machine uses
(`bootstrap/_scaffold/install.py:272`) — but all of its integrity
fingerprints are computed on the Linux-style bytes. On a Windows
machine, the two disagree for *every installed file*. Verified
consequence: the install appears to finish, then quietly declines to
write the install receipt (one warning line the quickstart never
mentions) — and without the receipt there is no tamper-detection and no
upgrade path. Think of an instrument that silently records in different
units on one lab's computer: every subsequent QC comparison reads as
contamination.

It compounds: the runtime contract asserts the installer *doesn't*
adjust line endings (`doctrine/runtime-contract.md:107-109`) — the
opposite of its actual behavior on Windows; a single common git setting
(`core.autocrlf`) makes the integrity checker flag the *entire*
installation as tampered; and the only mention of any of this is one
bullet — "A POSIX shell (macOS / Linux / WSL)" (`docs/quickstart.md:21`)
— so a PowerShell user's first command fails with an error about the
shell, not the actual prerequisite. Given that lab members plausibly
run Windows, the current posture is *unsupported-but-never-said,
failing without explanation*. Either land the small fix (tell Python to
always write Linux-style endings, and have the installer drop a
one-line git settings file) or say "not supported on native Windows —
use WSL" clearly, in the contract and at the top of the quickstart.

## Options

1. **Do nothing; hand it to the postdoc now.** Rejected. The test is
   one-shot, and the current path teaches the adopter to mislabel
   their reviews from day one, leaves their public repo out of license
   compliance by default, and hands any skeptical reader the Theme-1
   record problems in their first hour.
2. **Fix only the documentation accuracy items (Theme 2) and stop.**
   Cheap and visible, but it polishes the description while leaving
   the record repairs, the licensing exposure, and the adopter path
   itself.
3. **The full tighten-up, sequenced by the two real deadlines**
   (recommended, below): the record and the adopter path before the
   postdoc installs; accuracy and security alignment before the 0.4
   release; the rest as rolling maintenance.
4. **Re-rank the existing 0.4 polish list.** The queued
   graphics-and-comment-cleanup items are worth less than any single
   theme above; they should sort behind Phases A and B.

## Recommendation — the tighten-up, in three phases

Each lettered item is one proposal-sized piece of work. Items marked
*(doctrine)* change methodology rules and so must clear the
doctrine-change bar on their own evidence.

**Strikethrough status, added 2026-08-05.** A struck item is **implemented and
code-reviewed**, established by one test rather than by recollection: a plan of
that name exists in `dev/plans/archive/`, and a plan cannot archive until a code
review has occurred (`doctrine/plans.md` > "The plan-archive precondition"). Four
items pass it: **A1**, **A3**, **A4**, **A7**.

**The unstruck items are not all outstanding — they are unverified**, and the
distinction matters more than a tidy page. Several have partial or probable
coverage that this pass deliberately did not claim:

* **B2** is *partly* done — `scan-coverage` archived, which is the
  derive-targets-from-the-installer's-file-lists half. Its other half is **not**:
  Cairn still has **no CI**, so every "fails in CI" claim B2 asked to either
  automate or reword remains live. Striking B2 would assert a security-story fix
  that has not happened.
* **A2**, **A6**, **B1** plausibly overlap `review-record-integrity` and
  `adopter-entry-doc-refresh` (both archived), but neither maps to the item
  one-to-one, and a name that merely *sounds* like a match is not the archived-plan
  test.
* **A5**, **B3**, **B4** have no corresponding proposal at all.

Anyone continuing this: apply the archived-plan test per item rather than
extending the strikethroughs by resemblance.

**Phase A — before the postdoc installs** *(days of work; highest stakes)*

* ~~**A1. Repair the record**~~ — **IMPLEMENTED**, `record-corrections` plan archived. (Theme 1): append a dated, honest
  correction to the showcase proposal explaining how those commits
  actually happened; publish a correction of the v0.3.0 release-notes
  claim; write the missing adoption-decision note (or repoint the two
  claims that reference it); log the two bent-review-rule incidents in
  the incident tracker; state the zero-rejections fact, with its honest
  explanation, wherever the metrics are shown.
* **A2. Stop the mislabeled reviews** (Theme 5.2): fix the three
  passages in the solo starter guide, and add an automated check that
  no shipped guide ever again equates fresh-session self-review with
  independent review.
* ~~**A3. Build the solo-legacy recipe**~~ — **IMPLEMENTED**, `solo-legacy-adopter-path` plan archived. (Theme 5.1, 5.3–5.5): a preset
  (or a documented path) that actually reaches the
  existing-codebase modules; the corrected Appendix B example plus a
  warning when a hand-written module list omits defaults; the
  scientific-assumption trigger added to the proposal checklist
  *(doctrine)*; the deadline escape hatch written into the installed
  template; "make an assumptions document your first proposal" promoted
  from appendix footnote to the standing recipe.
* ~~**A4. The licensing package**~~ — **IMPLEMENTED**, `adopter-licensing-compliance` plan archived. (Theme 4): notice file, license
  headers, the bootstrap-guide paragraph, the contributions sentence —
  plus your decision on the "keeping the notice file is all you owe"
  clause.
* **A5. Rehearse before the real thing** (Theme 5.8–5.9): one internal
  end-to-end install into a *populated* research repository; write up
  the two AI-tool compatibility confirmations we already have as proper
  test records; add the "wire up the reviewer tool's config file and
  confirm it loaded the rules" step to onboarding; write the test
  protocol (who, what's observed, what consent, what counts as pass);
  tag a v0.3.1 so tag-based installs include the quickstart fixes.
* **A6. The two honest paragraphs** (Theme 5.6–5.7): "your record is
  not a performance review" and "here is how to scale down or leave."
* ~~**A7. First-session survivability**~~ — **IMPLEMENTED**, `first-session-survivability` plan archived. (Theme 5.10): show the skipped
  session-tools step in the install report with its one-line remedy;
  remove the phantom command from the report; make a vanished Python
  path a warning-with-fallback instead of a fatal error; make the
  starter task list match what was actually installed.

**Phase B — before the 0.4 public release**

* **B1. One accuracy pass, made permanent** (Theme 2): fix the dozen
  documentation-vs-reality items and extend the drift-gate pattern so
  the module tables, doctrine index, and placement guide are checked
  automatically against the code from then on; re-scope issue #2 to
  the real distribution and disposition all 99 neutrality findings;
  fix the bootstrap guide's wrong upgrade advice and point "upgrading
  later" at the real upgrade documentation.
* **B2. Make the security story true** (Theme 3): have the release
  scan derive its targets from all three of the installer's file lists
  (and the test suites likewise); either stand up minimal automated
  checks (test suite + scanner on every push) or reword every
  "fails in CI" claim to match reality — recommend the former, it also
  makes A1's release-attestation discipline automatic; make the
  fallback config parser match the real one and warn on unknown
  keywords; fix the one write-before-check ordering; teach the
  dead-code detector about import aliases; fix the false "read-only"
  help text.
* **B3. Answer the reviewer's question** (Theme 6): the "related
  practices" section (decision records, RFC processes, lab notebooks,
  pre-registration — and the one-line delta from each); soften
  "genuinely uncommon" to the defensible claim; add the
  shared-blind-spots caveat to the doctrine *(doctrine)* and source or
  soften the catch-rate quote; write the two-sentence pitch and put it
  at the top of the README and the citation file — e.g.: *"Every
  AI-assisted change starts as a short written proposal that an
  independent reviewer — a different model, or a human — checks before
  code is written. The whole deliberation is committed to git, so you
  can always reconstruct why your model is the way it is."*; retitle
  the citation file to match the methodology identity and add the
  missing license; a one-page glossary; strip the internal codes from
  the README; a one-page CONTRIBUTING; resolve the
  methodology-vs-software contradiction *(doctrine)*.
* **B4. Decide the Windows question** (Theme 8): either the small
  always-Linux-endings fix plus a seeded git-settings file, or an
  explicit "not on native Windows — use WSL" in the contract; in both
  cases fix the backwards line-endings sentence and put the
  prerequisite warning above the quickstart's first command.

**Phase C — rolling maintenance** (Theme 7): fold in the stale review
and re-home the orphaned metrics plan; refresh the guiding framework's
version facts; retire the collaboration agreement cleanly (and use that
retirement as the first real test of the template-removal machinery,
with tests, *before* it ships); repoint the broken doctrine
cross-references; merge the duplicated doctrine text to one home; link
the vision document from the README; the upgrade-longevity package (one
real cross-version upgrade rehearsal added to the release checklist; a
realistic multi-file upgrade test; validate the receipt's version field
on read; a sync check between shipped and installed tool copies; either
restore our own installation to full upgrade capability or document
why it isn't); update the strategy record on the completed complexity
work; fix the time-bomb test (already spun off).

## Open questions — decisions only the Maintainer can make

1. **Licensing** (A4): add the "keep the notice file and you owe
   nothing else" clause (recommended — it turns a legal question into
   a one-file rule), or keep plain attribution mechanics?
2. **Solo-legacy** (A3): a fourth named preset, or smarter overrides?
   (The preset is easier to explain; the override fix is more general.)
3. **Automated checks** (B2): stand up minimal CI before 0.4
   (recommended), or reword the claims to "manual, at release"?
4. **Identity** (B3): is methodology-without-the-software a supported
   way to run Cairn (as the on-ramp says) or not (as the runtime
   contract says)? The README's "methodology, not software" line
   should follow whichever answer you pick.
5. **The construction history**: publish a digest of the private
   build-out record into `dev/plans/archive/`, or keep it private and
   say so explicitly where the citations now dangle?
6. **The probe**: is the postdoc formally the launch-gating test (with
   protocol and consent), or a friendly rehearsal that doesn't consume
   it?
7. **Windows** (B4): support it (small permanent fix) or explicitly
   require WSL? Your lab's actual machines should decide; either
   answer beats today's silent failure.

## Lessons worth keeping (fold-up candidates)

Four patterns from this review look general enough to become doctrine
eventually — each via its own proposal, under the usual
one-incident-isn't-doctrine restraint:

* **A claim that checks passed is a claim like any other** — release
  notes should carry the machine-generated output of the checks, never
  a summary written from memory (Theme 1.2 could not have happened).
* **Any scanner's target list should be generated from the same list
  the installer uses** — every coverage hole in Theme 3 was a
  hand-copied list that fell behind.
* **Tests must not depend on today's date** — a suite that reddens by
  itself (Theme 3.6) is the software equivalent of a standard that
  expires on the shelf.
* **A cheap automatic check that a commit's message matches its
  contents** (a commit claiming "adds review" must add a review) would
  have caught Theme 1.1 at commit time.

---

## Appendix — the verified finding inventory (~100 confirmed across all passes, 3 refuted)

*This index is deliberately telegraphic — it is the lookup table for
the proposals that implement the fixes. Every entry is explained in
plain terms in the themes above; severity in brackets ([H]igh,
[M]edium, [L]ow).*

**Concept (10):** [H] showcase-arc provenance misstated (T1.1) · [H]
runtime-contract vs on-ramp identity conflict (T6) · [H] ADR/RFC prior
art unharvested, "genuinely uncommon" unscoped (T6) · [H]
correlated-failure limit absent from doctrine; uncited catch-rate (T6)
· [M] review floors bent without waivers (T1.5) · [M] rationale
traceability overbroad; RULES.md misstated (T2) · [M] case study ships
internally-flagged statistic (T2) · [M] External gate never fired on
the record (T1.6) · [M] CI absence untracked while trust apparatus
grows (T3.1) · [M] second-agent-type graduation step unnamed (T6).

**Claims (12):** [H] module rosters 12/20 with contradictory counts
(T2) · [H] vendor-neutrality contradicted in shipped files (T2) · [M]
SECURITY.md "every file" overpromise (T2) · [M] CHANGELOG false public
release; README unqualified "released" (T2) · [M] doctrine index 8/16
(T2) · [M] DOCUMENTATION_PLAN misdescribes its tree (T2) · [M]
CITATION.cff identity/license mismatch (T2) · [M] LHM statistic
provenance upgraded without citation (T2) · [M] usage claim carries no
verifiability statement (T6) · [L] rationale Anchor-12 RULES.md error
(T2) · [L] README trust block over-absolute vs link_check external
probe (T2) · [L] adoption deliberation pointer resolves to nothing
(T1.4).

**Alignment (11):** [H] v0.3.0 gate-green attestation fails replay
(T1.2) · [H] pre-release sweep skipped at v0.3.0, unhomed for 0.4
(T1.3) · [H] R-H probe has no enrollment path (T5.9) · [M]
collaboration-agreement decision unserialized vs live seed task (T7) ·
[M] no existing-codebase rehearsal queued before the probe (T5.9) · [M]
metrics doc supersession pointers dangle (Goal 7 ghost) (T7) · [M]
metrics doc carries unfolded stale review (T7) · [M] guide-star release
facts stale; Sweep B baseline missing (T7) · [M] construction record
not publicly auditable; citations point out-of-tree (T6) · [M]
neutrality-gate triage basis misdescribes live distribution (T2) · [M]
strategy record still presents the completed complexity-debt program as
gated/pending (T7).

**Code (7):** [H] Bandit/CI postures presuppose CI that does not exist
(T3.1) · [M] YAML fallback diverges from PyYAML on documented schema
(T3.3) · [M] R6 false-flags live security code (T3.4) · [M] upgrade.py
mega-functions outside the debt ledger (T7) · [L] lockfile-write
guard-order inversion (T3) · [L] profile keys fail open (T3.3) · [L]
MergeResult status contract omits needs-value (T3).

**Docs (10):** [H] DOCUMENTATION_PLAN five stale self-host denials
(T2) · [H] doctrine map omits half the corpus incl. proposals/plans
contracts (T2) · [M] DOCUMENTATION_PLAN root-file placements wrong;
cairn/ prefix evades claim_check (T2) · [M] ~900-word doctrine
duplication proposals/plans (T7) · [M] plans.md cites nonexistent
anchors (T7) · [M] charter has three homes; vision.md orphaned (T7) ·
[M] descriptive-layer inventory 6/9 (T2) · [M] AGENTS.md git-section
accretion vs doc-governance (T7) · [L] doc-governance "forthcoming"
mechanism already shipped (T7) · [L] dev/README tree table omits two
installed dirs (T7).

**Formulation (8):** [H] skeptic compression unpreempted; comparables
unharvested (T6) · [H→M] ~40-term vocabulary, no glossary (T6) · [M]
README internal codes unexplained (T6) · [M] installed AGENTS.md
multi-agent-voiced for solo installs (T5) · [M] proposal template
preamble-before-skeleton ordering (T5) · [M] no two-sentence
mechanism+benefit pitch (T6) · [M] CITATION.cff Framework title, ND
omitted (T2/T6) · [M] no CONTRIBUTING/support path (T6).

**Postdoc (10):** [H] solo-legacy preset gap; silent age-gate skip
(T5.1) · [H] solo onboarding mislabels External tier (T5.2) · [H]
science trigger missing from canonical triage (T5.3) · [M] escape
hatch off-tree (T5.4) · [M] intent-claim referent uninstalled in solo
trees (T5) · [M] de-adoption undocumented vs "reversible" promise
(T5.7) · [M] adopting-under-observation unaddressed (T5.6) · [M] no
named week-one value moment (T5.5) · [M] Appendix B example 3/6 +
silent literal lists (T5.1) · [L] getting-started review step omits
solo floor (T5).

**Licensing gap (7, across two sweeps):** [H] MIT notice stripped from
installed copies · [H] no CC-BY attribution travels; no adopter-facing
mention · [M] base cache is hidden verbatim redistribution · [M]
lockfile carries no creator/license/URL · [M] no downstream-license
position · [M] shipped config/data files sit outside both declared
license families · [L] no inbound-license statement (all T4).

**Daily-loop runtime gap (5):** [H] release Bandit gate skips the
skills registry · [M] lifecycle_planner.py outside every security
hand-list · [M] "faithful port" has drifted, no parity check · [M]
lifecycle.py false read-only/--dry-run claims · [L] R6/debt-ledger
scope misses the daily-loop surface (all T3).

**Cross-harness gap (6):** [H] zero native-tested targets incl. both
harnesses the postdoc needs · [H] reviewer-harness onboarding never
wires the instruction file · [M] Antigravity confirmation never
serialized per its own protocol · [M] cli-backstop-only vocabulary
defined nowhere adopters read; matrix orphaned · [M] VENDOR.md rename
example unfollowable by the resolver · [M] "vendor-neutral throughout"
broader than the construction-level guarantee (all T5.8/T6).

**Upgrade gap (6):** [H] BOOTSTRAP.md teaches the `--force` re-run as
"to upgrade Cairn"; no entry doc points at UPGRADE.md · [H] no
cross-tag upgrade rehearsal ever run or queued at the 0.4 gate · [H]
the queued template retirement's removed-upstream class has zero test
coverage and no prune mechanism · [M] self-host lockfile permanently
review-only (38/38 mergeable records unrecoverable-base, no base cache,
cairn_commit "unknown") · [M] lockfile schema write-only, no read
validation · [M] no automated multi-file/multi-class upgrade-delta
test — plus, hand-verified: tag-only guidance (`SECURITY.md:25`) routes
to a v0.3.0 tag now 20 commits behind the entry-doc fixes (all
T7/T5.9).

**Platform/Windows gap (6):** [H] text-mode writes CRLF-translate on
Windows while hashes compare LF bytes — install completes, lockfile
silently refused · [H] byte-exact hashing + no shipped .gitattributes:
one core.autocrlf checkout reads as wholesale tampering · [H] no OS
matrix in the self-declared authoritative runtime contract · [M] the
runtime contract's "does not normalize line endings on write" is
backwards on Windows · [M] the PowerShell failure is never
self-explaining (quickstart dies at `export`) · [L] interpreter trust
root bakes a version-pinned resolved path and hard-refuses on drift
(all T8).

**Installed-executable gap (4):** [H] Claude Code skills silently
unreachable on the likeliest first-session state; install report
invites a phantom `/good-morning` · [M] stale interpreter binding
hard-fails session-start and the handoff (reproduced end-to-end) · [M]
onboarding seeds copied by preset name, not resolved roster
(reproduced) · [M] nothing automated keeps the 13 shipped/installed
payload copies from diverging (all T5.10/T3).

**Refuted (3, for the record):** a reading-burden framing that ignored
the minimal path the quickstart already names; a plan-open
board-row-move complaint mooted when the plan archived and the board
was scrubbed at that serialization point; and a sibling-entry-point
"bypasses the hardened loader" claim (the engine guard covers direct
imports; the residual case is documented out-of-threat-model).
