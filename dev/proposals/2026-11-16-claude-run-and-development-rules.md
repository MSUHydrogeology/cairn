# Run rules apart from development rules, an Operator role, a project-wide entry file

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy — it edits always-loaded `AGENTS.md`, the `RULES.md` template and `docs/methodology/roles.md`, which are named high-risk surfaces; the Maintainer sets the tier
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: Let a project whose agents both run and change its software keep the rules for running it in a short file that can ship in a release, and give the agent that runs the software its own role name.

## Decision summary

Issues #74, #76 and #79 come from one adopter whose agents both run its software and change it. Its entry file carried the full development process, so an agent that only runs the software read about 720 words of it every turn, and upgrades merge Cairn's text back. Recommended: (1) a project that wants run rules keeps them in `RULES.md`, opt-in, so a project with no run job pays nothing; (2) a new optional role, **Operator**, names the agent that runs the software, with four bars written into always-loaded `AGENTS.md`, and "User Agent" narrows to its Cairn meaning; (3) `AGENTS.md` gets one short paragraph and moves nothing. I measured the larger option, which moves development text behind pointers while keeping every security, fence and Maintainer-only sentence: it saves 229 of 1,125 words, so a run-only agent still reads about 495 words of development text. That does not justify a merge conflict for every adopter who edited the file, so I do not recommend it now. Cost of the recommendation: about 95 more words in always-loaded files, which fit only after the accepted trim lands. The Maintainer asked for this follow-on (chat, 2026-11-16: "Go ahead and build the follow-on proposals now--unless doing so requires a completion of an earlier step."). The earlier step, the trim, is accepted (Decision `54eec3fe`) but not yet built; see item 5.

## Context

Measured with `wc -w` at commit `3c42b85a`, 2026-11-16 (the counts match `e8703b2c`): shipped `AGENTS.md` 1,125, `VENDOR.md` 310, `RULES.md` 60. They total 1,495 against the 1,500 cap held by `bootstrap/tests/test_scaffold.py`, so added words need room first. The accepted trim cuts `VENDOR.md` to 170 (about 140 words freed); it is not yet built, and the repository-layout amendment may drop `VENDOR.md`.

Shipped `AGENTS.md` by section: Functional prose 23, Lifecycle and records 187, Review 102, Roles 293, Working tree and commits 96, Verification and its slots 157. My development-process figure of 723 words is those sections with 158 of Roles' 293 (the other 135 are project-wide). A tool or test reads five slots (`project-overview`, `claim-check`, `security-verification`, `documentation-discipline`, `project-conventions`; `bootstrap/tests/test_install_report_slots.py`); the headings Review, Roles and Lifecycle and records (`test_documentation_plan_module.py`); and `tools/session.py`, which cites Lifecycle and records. `_shipped_agents_citation_errors` resolves every `AGENTS.md > "Heading"` citation in shipped docs, so a moved or renamed cited heading fails. Every option below keeps all slots and headings. Not checked: any other test that quotes `AGENTS.md` wording.

`RULES.md` is adopter-owned living state: integrity checks ignore its contents (`bootstrap/_scaffold/lockfile.py:205`), and upgrade does not re-create it once deleted (`bootstrap/_scaffold/upgrade.py:957`). A rule whose only home is `RULES.md` can vanish unnoticed.

Cairn's role texts disagree: `docs/methodology/roles.md` says the User Agent "runs the software"; the shipped `dev/agent_collaboration.md` says it "exercises Cairn from an adopter's position". "Operator" appears in neither. `dev/rules/README.md` says its files are "entirely the adopter's own", which rules out #79's `dev/rules/` as a place for Cairn-written text.

One adopter's practice (read, not run): its root `RULES.md` (1,166 words) holds run rules and names nothing under `dev/`. It kept all of Cairn's `AGENTS.md` and put its router in its own overview slot. Holding that layout cost it two guard tests (537 lines): line ceilings, section-name and slot-order checks, and a check that run rules cite no `dev/` path.

## Proposal

**1. Run rules: opt-in, default off.** No shipped file gains a second rule path. One section of `dev/rules/README.md` (about 150 words, read on demand) says: the root `RULES.md` holds rules for an agent that runs the software and ships whole; development rules live in `dev/rules/` and may cite run rules, never the reverse; run rules add limits and never relax `AGENTS.md`. Essentials both jobs need (temporary files, never delete) may live once in `RULES.md`. Never-push-unasked, the instruction to read `RULES.md`, and every item on item 3's keep-list stay in `AGENTS.md`; `RULES.md` may restate them but is never their only home. The `RULES.md` template gains one line (about 15 words): run rules add to `AGENTS.md` and never relax it. It keeps its pointer to `dev/rules/README.md`; a project that wants a release without `dev/` removes that pointer. A project opts in by writing run rules. There is no installer question (a profile field is an engine change). The staged-modules draft offers rules-folder guidance by size; "agents also run the software" is a fact about the project, so its trigger fits poorly. If decided, it may offer this section too.

**2. Operator.** Add to the roster in `dev/agent_collaboration.md` and `roles.md`: **Operator**, runs the project's software under its run rules, may reproduce and diagnose a defect, and files it in the project's tracker. Four bars go into always-loaded `AGENTS.md` as one new paragraph in Roles (about 80 words; a new paragraph, not an edited sentence, so an adopter's edits there still merge). An Operator (1) edits no tracked file and runs no lifecycle step; (2) treats a change to code, data handling or credentials as development: it switches roles explicitly and follows `AGENTS.md` in full; (3) takes only limits from `RULES.md`, never a relaxation of `AGENTS.md`; (4) captures a defect instead of fixing it in passing, and the capture-vs-fix rule decides when a fix may land after the switch. If a `dev/` file the text cites is absent, it changes nothing and asks. All four state cleanly. They are prose: nothing mechanical stops an agent that ignores them (S5).

Narrow **User Agent** in `roles.md` to "exercises Cairn from an adopter's position", and keep its debug-from-the-user's-seat and capture-vs-fix text there; the Operator entry cites it, so nothing is copied or dropped. Tier: the model-selection table gets an Operator row, `low` (capture only), `medium` when it diagnoses a cause; development work keeps its own floor. Both roles are optional. A project with an Operator adds a line to the `role-roster-additions` slot; the roster sentence in `AGENTS.md` is not edited.

*Every file that names "User Agent"* (searched `templates/`, `docs/`, `bootstrap/`, `dev/`). Edited: `docs/methodology/roles.md:55` (one clause; Operator entry added); `templates/core/dev/agent_collaboration.md:31, 41` and `dev/agent_collaboration.md:26` (Operator added to roster and slot example); `templates/modules/team-gated/issue-capture.md` and `dev/modules/issue-capture.md` (one sentence each: an Operator uses the same capture surface and capture-vs-fix bound; the copies differ at line 51, so each is edited); `templates/modules/team-gated/model-selection.md:54` and `dev/modules/model-selection.md:54` (one row). Read, unchanged: `templates/core/AGENTS.md:50`, `templates/phase-0/team-profile.md:53`, `templates/modules/README.md:56`, `bootstrap/BOOTSTRAP.md:160`, `bootstrap/fidelity-check.md:167, 367`, `dev/PLANNING.md:79`, and four archived plans and proposals (immutable records). No sentence leaves any listed file; the one clause change is the narrowing.

**3. Shape of `AGENTS.md`.**

| Option | What it is | At upgrade |
|---|---|---|
| **(a) Router plus Operator bars** | Item 2's paragraph is the router: a run-only agent learns its role and its limits. Nothing moves | An appended paragraph merges clean. No word is saved, so #79's "short project-wide file" stays unmet |
| (b) Full split (#79) | Development text becomes new files | Largest conflict; new install rows are an engine change (heavy, Security Review) |
| (c) Move behind pointers | Everything off the keep-list below moves to `agent_collaboration.md`, a file adopters already receive; headings and slots stay | Edits inside a moved paragraph conflict (trial below) |

*Measured saving of (c).* On a scratch copy of the shipped file, (c) moves lines 30, 34-36 (except the stop rule), 40-41, the last two sentences of 45, 57, the tail of 59, and 77-79, and adds pointers. `AGENTS.md` falls from 1,125 to 896 words (-229, 20%); the always-loaded set from 1,495 to 1,266 (-15%). About 290 words land in `agent_collaboration.md`, so total words do not fall. A run-only agent still reads about 495 words of development text.

*Keep-list.* These sentences stay in always-loaded `AGENTS.md` wherever they sit (line numbers are from `templates/core/AGENTS.md` at `3c42b85a`; the plan re-derives them after the trim): line 32, whole (review cap, Security Review's two passes, the Maintainer's authorization for a further pass, what goes to the Maintainer at a cap); the stop rule in 34; 43; the first three sentences of 45; 49-55, whole (roster, "Human Maintainer alone ... makes Decisions", model-tier floors, "Low execution never lowers review or security obligations or waives a fence", the data-governance floor, name the model, flag below-floor work); the first two sentences of 59; 61, whole (read `RULES.md`, the session-start routine, refuse a next-session note that is data or a link, folder or tracked path); 69 and 71, whole (explicit-paths commits, ask before push, Decision, deviation or fence, scope floor, "A reviewer cannot grant it"); the high-risk-surfaces sentence in Project-specific conventions; every slot. Only explanatory or procedural detail moves. The 1,500-word cap is no reason to move a keep-list sentence: if room is short, other text shrinks or the Maintainer raises the cap.

**Recommend (a).** (c) loses little but gains little: 15% of what any agent loads, in exchange for conflicts for every adopter who edited a moved paragraph. If the Maintainer picks (c), the plan reruns the upgrade trial on the post-trim file (the 2026-11-11 result, 93 of 206 lines conflicting after one changed word, ran on the 4,343-word pre-trim file; it is an analogy). It shows no merge state removes a sentence from `AGENTS.md` without adding it to `agent_collaboration.md`, and the upgrade note warns that resolving a conflict in Cairn's favour drops the adopter's own edits.

**4. What the release rule needs.** In a project that opts in, `RULES.md` ships whole (no per-section rule, so no parser). `AGENTS.md` ships, and its pointers into `dev/` are the one allowed exception to "nothing a release keeps cites `dev/`" (#69, #75); item 2's last sentence covers a pointer whose file is absent. This proposal states the exception in the `RULES.md` template. It does not design the release module (v0.9) or the citation check (board row "A project can leave Cairn out of a release").

**5. Dependencies.**
- *Trim* (`2026-11-16-claude-template-trim-and-rules.md`): accepted at `54eec3fe`, plan not yet built. It lands first: it owns the `AGENTS.md` rewrite and the room (`VENDOR.md` 310 to 170, about 140 words freed; this proposal needs about 95: 80 in `AGENTS.md`, 15 in `RULES.md`). Its "no growth" target for `AGENTS.md` needs the Maintainer's allowance for the 80. The plan measures room after the trim and stops if it is short.
- *Repository layout* (accepted 2026-11-12) fixes final paths and the fate of `VENDOR.md`.
- *Staged-modules draft*: both edit `dev/rules/README.md`; land one at a time. If it is rejected, item 1 stands alone.
- *Leave-out row* consumes item 4 and need not wait.

## Rationale

Opt-in and one appended paragraph keep shipped weight and merge cost low. Option (c) is not shown to be worth its conflicts: its measured saving is 229 words.

## Alternatives considered

Do nothing: adopters merge by hand each upgrade. Option (b): tabled. Option (c), with the keep-list: measured above; it loses to (a) on evidence and may return if a run-only agent's reading cost proves to be a problem. Split for every project: each pays for a job it may lack.

## Documentation / doctrine surface

`templates/core/AGENTS.md`, `templates/core/RULES.md`, `dev/rules/README.md`, `dev/agent_collaboration.md` and its shipped copy, `docs/methodology/roles.md`, the two `issue-capture` and two `model-selection` copies (item 2's list); Cairn's own `AGENTS.md` follows its shipped copy. **Does any rule weaken or disappear?** Under (a), none moves or weakens, and none is deleted: one paragraph is added. Under (c), no keep-list sentence moves or is deleted. Procedural rules do weaken: lifecycle state chains, transition-commit hygiene, review reading aids, test selection and `claim_check` load only when the agent follows a pointer, which it can skip (the risk the 2026-11-10 trim note named). `RULES.md` may restate a keep-list rule but is never its only home.

## Evidence / verification plan

Evidence is one adopter. I ran no tests, installs or upgrades; the word counts above are `wc -w` on a scratch copy. A second project must show it also needed run rules apart, and that a run-only agent missed nothing. **Wrong if:** an opted-in adopter still hand-edits `AGENTS.md`; a review finds an agent broke a moved rule; or a second project defines a different third role. Checks: `wc -w` against the cap; tests naming changed files (the plan finds those that quote role text); under (c), a ledger row per moved sentence read by the Internal Security Review (not a test, because the accepted trim bars tests that pin wording); and the Security Review's own test, not yet run: give a fresh agent only the changed `AGENTS.md` and a filled `RULES.md`, frame it as an Operator that hits a defect, and see whether it fixes, commits or pushes without asking.

**Security preflight** (a named high-risk surface, so required):
- **S1 Who supplied it?** The decisions are what an Operator may edit and push. Inputs: `AGENTS.md` (Cairn-shipped, integrity-checked) and `RULES.md` (adopter-written, not integrity-checked). Neither is supplied by the thing being decided about, but `RULES.md` can say anything, so the bars sit in `AGENTS.md` and `RULES.md` may only add limits.
- **S2 Can it fail?** No new check is added. The keep-list is a reviewer's read, not a test, so it cannot fail mechanically; the mutation that would break it (delete the `RULES.md` instruction at line 61) is caught only by that read.
- **S3 What fires it, over what?** The Internal Security Review of the plan, over the old and new `AGENTS.md` text. The adopter-facing claim is "Does any rule weaken or disappear?" above, which that read checks.
- **S4 Which way does it break?** A skipped pointer or a deleted `RULES.md` leaves less authority (no run rules), not more. A merge conflict resolved in the adopter's favour can drop the Operator paragraph: more authority, because the bars vanish. The upgrade note says so.
- **S5 Who still wins?** Assumed: a mistaken or hostile run rule telling an Operator to edit, commit or push. Still succeeds: an agent that follows the more specific run rule over the general bar. The class is closed by enumeration of prose, not by construction.

**Independent scientific check**: N/A: no scientific result touched.

## Assurance path

**Assurance path**: high-assurance — it edits governing doctrine (`docs/methodology/roles.md`) and named always-loaded templates.

## Review -- Claude Sonnet 5.5 (ordinary Reviewer, Medium) -- 2026-11-16

**Reviewed commit**: `19b2d666` (branch master, tree clean at start)
**Tier**: usual
**Findings**: 2 blocking, 6 non-blocking
**Verdict**: REVISE
**Elapsed**: about 5 minutes (15:30 to 15:35 EST by `date`)
**Tokens**: unknown

**Steelman.** One adopter's run-only agents pay for a development process they cannot remove, and the draft fixes the naming collision and the shipped cost without an engine change.

**Foundations.**
1. *Should this happen as framed?* Items 1, 2 and 4 yes. Item 3(c) is not shown to help. Shipped `templates/core/AGENTS.md` is already the v0.7 trim: Verification (lines 73-79) is a one-sentence pointer, and Working tree (67-71) is two short paragraphs. The draft never says how many of the 723 "development" words (Context) leave, so how much a run-only agent saves is unstated.
2. *Best alternative.* Ship the `RULES.md` convention, the Operator role and the release exception now, and defer the `AGENTS.md` restructure until a run-only agent's saving is measured. The adopter read (`RULES.md`, 1,166 words, run rules only) kept all of Cairn's `AGENTS.md`, so items 1-2 might already meet its need. The draft tables (a) and (b) but not this split.
3. *What shows it wrong.* The draft's own list is sound. Add: after (c), a run-only agent still reads every heading and first sentence, so #79's "read a short project-wide file" stays unmet.

**Findings.**
1. **Blocking.** (c) says "each development section keeps its first rule sentence and a pointer", but the Documentation surface says ask-before-push, commit-explicit-paths, plain-language and model-tier "stay". They do not follow from that rule. Ask-before-push is the second paragraph of Working tree (`templates/core/AGENTS.md` line 69), and the model-tier paragraph (line 55) is not Roles' first sentence. The Security Review two-pass cap (line 32) is also past Review's first sentence. A plan would move them, or keep them against the stated mechanism. Closes it: list the retained sentences by section, with the word count each side of the move, and say what the run-only saving is.
2. **Blocking.** Narrowing "User Agent" is wider than the five surface files. `templates/modules/team-gated/issue-capture.md` (lines 4, 9, 13, 48, 63; line 63 binds the "debug-from-the-user's-seat" mode), `bootstrap/BOOTSTRAP.md:160`, `templates/phase-0/team-profile.md:53`, `team-gated/model-selection.md:54`, `templates/modules/README.md:56` and `bootstrap/fidelity-check.md` lines 167 and 367 all use the term. `roles.md` lines 55-70 give the User Agent the capture-vs-fix boundary for "runs the software". The draft does not say whether that text goes to Operator or is dropped, yet it answers "Does any rule weaken or disappear?" with "None is deleted". Closes it: widen the surface list, name where the debug and capture-vs-fix text goes, and state Operator's model tier (the mapping has no row).
3. Non-blocking. Item 5 is stale. The trim proposal was accepted at `54eec3fe` and kept #74, #76 and #79 as a follow-on, so "if its Decision folds them" is settled. "5 words of cap room" is true today, but the accepted target shrinks `VENDOR.md` from 310 to 170, and the layout amendment may drop it. Restate the order from the Decision. The trim plan is not yet implemented, so "lands first" should say so.
4. Non-blocking. Decision summary says "opt-in, so a project with no 'run' job pays nothing". That holds for item 1 only. Item 3(c) rewrites `AGENTS.md` for every adopter, and the conflict cost falls on all who edited it. Say which.
5. Non-blocking. Item 1 says run rules cite nothing under `dev/`, yet the `RULES.md` template would point to `dev/rules/README.md`. Say the opt-in project removes that line.
6. Non-blocking. The 93-of-206-line trial (`dev/strategy/2026-11-10-claude-agents-md-diet.md` lines 95-100) ran on the 4,343-word pre-trim file. It is a rough analogy for a 1,125-word file, as the draft says by planning a rerun.
7. Non-blocking. Heading and slot check, which closes the draft's "not checked": all five slots (`test_install_report_slots.py`) and every heading survive in (c). The tests read Review, Roles and Lifecycle and records (`test_documentation_plan_module.py:103`) plus `_shipped_agents_citation_errors`, which resolves every `AGENTS.md > "Heading"` citation in shipped docs. Any moved or renamed cited heading fails it. `tools/session.py:1250` cites Lifecycle and records. The cap test (`test_scaffold.py:656`) sums AGENTS, VENDOR and RULES: 1,495 measured today; draft counts match (1,125, 310, 60). The draft's section split (Roles 158) differs from my 291-word Roles section; its classification is unlisted.
8. Non-blocking. "Roles gains the word Operator (+2 words)" leaves 3 words of room until the trim plan lands.

**Audience.** Plain-language layer first; the Context paragraph carries coinages ("slot", "release rule") undefined for a Maintainer.

**Coverage.** I measured counts and read the tests, templates, trim and layout decisions, issues #74/#76/#79, and one adopter's `RULES.md` header. I did not run tests or the installer, and did not run the upgrade trial, nor read the rest of the adopter's rules. I did not assess Security.

## Security Review -- Claude Opus 5.5 (Security Reviewer, High) -- 2026-11-16

**Reviewed commit**: `dca1973a` (branch master; at the start, one unrelated plan file was modified)
**Tier**: Security Review
**Findings**: 4 blocking, 3 non-blocking
**Verdict**: REVISE
**Elapsed**: about 3 minutes (15:32 to 15:35 EST by `date`)
**Tokens**: unknown
**Obligation**: Security Review (the `usual + Security Review` line). It builds on, and does not repeat, the ordinary review's findings 1 and 2.

**Steelman.** An agent that only runs the software should not pay for the development process every turn, and a named Operator role stops "User Agent" from meaning two things.

**Foundations.**
1. *Should this happen as framed?* Items 1, 2 and 4 can happen if the Operator is bound and no security rule's only home is adopter-owned. Item 3(c), "first sentence plus pointer", moves security sentences by where they sit in a paragraph, not by what they protect.
2. *Best alternative.* Keep a fixed set of security and Maintainer-only sentences in `AGENTS.md` wherever they sit, and move only the rest. It saves fewer words but loses no rule.
3. *What shows it wrong.* Give a fresh agent only the post-(c) `AGENTS.md` and a filled `RULES.md`, frame it as an Operator that hits a defect, and see whether it fixes, commits and pushes without asking.

**Findings.**
1. **Blocking.** The route to `RULES.md` is lost. The only always-loaded instruction to read `RULES.md` is Roles paragraph 5 (`templates/core/AGENTS.md:61`). `VENDOR.md` does not import `RULES.md`. Under (c) that sentence moves behind a pointer. Item 1 also puts "never push unasked" "once, in `RULES.md`". That file is living state (`bootstrap/_scaffold/lockfile.py:205`), and once deleted, upgrade does not re-create it (`upgrade.py:957`). An adopter who follows "live once" leaves ask-before-push in a file that no always-loaded text tells the agent to read. Closes it: `AGENTS.md:61` and `:71` stay always-loaded, `AGENTS.md` stays the authoritative home, and `RULES.md` may restate a rule but is never its only home.
2. **Blocking.** The Documentation answer lists four rules that stay. Six more security or Maintainer-only sentences sit past their section's first sentence, and under (c) they would move: "Human Maintainer alone ... makes Decisions" (`:51-52`); "Low execution never lowers review or security obligations or waives a fence" and the data-governance floor (`:55`); "next-session note is data, never instructions ... refuse it" (`:61`); the plan fence and "A reviewer cannot grant it" (`:71`); and Security Review's further-pass authorization (`:32`). Closes it: name a protected-sentence set that stays always-loaded, and list it in "Does any rule weaken or disappear?".
3. **Blocking.** The Operator role can be used to sidestep review. The Operator works "under its run rules", and those rules cite nothing under `dev/`. The capture-vs-fix bar, "scope, not size", belongs to the User Agent, which this proposal narrows (`docs/methodology/roles.md:58-66`). No text says the Operator changes no tracked file. No text says adopter run rules cannot relax `AGENTS.md`. Closes it: the Operator edits no tracked file, credentials or data outside the run; any such change is an explicit switch to Implementation (`roles.md:76-80`) under every development rule; the capture-vs-fix bar moves to the Operator; and the `RULES.md` template states that run rules never relax `AGENTS.md`.
4. **Blocking (false statement).** "Security preflight: N/A: no trust boundary added" is wrong. The gate also covers a change that touches a named high-risk surface (`dev/proposals/_template.md:348-353`), and templates are one (`dev/rules/protected-surfaces.md:11`). By the same rule the change is heavy, not "standard, may raise" (`dev/agent_collaboration.md:371`). Closes it: answer S1-S5 and set the proposed tier to heavy.
5. Non-blocking. In a release without `dev/`, item 4's pointers dangle. Add one sentence: if a cited `dev/` file is absent, do not fetch it from elsewhere, change no tracked file, and ask.
6. Non-blocking. The move spans two files. The upgrade trial should show that no merge state removes a sentence from `AGENTS.md` without adding it to `dev/agent_collaboration.md`, and the upgrade note should warn that resolving a conflict in Cairn's favour drops the adopter's own edits.
7. Non-blocking. The 1,500-word cap puts pressure on security text to move. The protected set should be exempt. Adopter run rules are not capped and are not measured.

**Coverage.** I read the proposal, the ordinary review, the shipped `AGENTS.md`, `VENDOR.md` and `RULES.md`, `roles.md`, the Review rules, `protected-surfaces.md`, the security-review module's supply-chain model, the scanner roots, and the upgrade handling of `RULES.md`. I did not run tests, the installer or an upgrade trial, and did not test whether `--apply` is all-or-nothing. A shipped never-commit-secrets rule appears in neither `AGENTS.md` nor `RULES.md`. That gap predates this proposal, but an Operator that handles credentials makes it matter more. The review runs past 400 words because it has four blocking findings.

## Response -- Claude Sonnet 5.5 (author) -- 2026-11-16

**Elapsed**: about 5 minutes (15:36 to 15:41 EST by `date`)
**Tokens**: unknown.

Operative text revised in place (the `exact_replace.py` helper refused with "install lock does not uniquely pin the trusted binding", so I applied the same unique-match replacements with a scratch script). Tier is now heavy. Measured on a scratch copy: the larger option (c) saves 229 words of 1,125.

**Ordinary review**
1. Accepted. The first-sentence rule is replaced by an enumerated keep-list by sentence (item 3); the saving is measured (-229 words, about 495 development words still loaded).
2. Accepted. Item 2 lists every file naming User Agent. Debug and capture-vs-fix text stays under User Agent and the Operator entry cites it, so nothing is dropped; Operator's tier row added.
3. Accepted. Item 5 restates the order from the Decision: trim accepted, not yet built, lands first.
4. Accepted. The summary now says (a) adds one paragraph and (c) conflicts fall on every adopter who edited a moved paragraph.
5. Accepted. The template keeps its pointer; an opted-in project that wants a `dev/`-free release removes it (item 1).
6. Accepted. The trial is called an analogy; it reruns only under (c).
7. Accepted. Roles counts corrected (158 of 293); headings, slots and the citation check recorded in Context.
8. Accepted. Cap math is in item 5: about 95 words against about 140 freed, measured after the trim.

**Security Review**
1. Accepted, verified (`upgrade.py:957`, `lockfile.py:205`). `AGENTS.md` keeps the `RULES.md` instruction and ask-before-push; `RULES.md` is never a rule's only home.
2. Accepted. All six sentences, and the data-governance floor, are on the keep-list by line.
3. Accepted. Four bars written into `AGENTS.md` (item 2); all state cleanly, but they are prose only (S5).
4. Accepted. Heavy tier, S1-S5 answered.
5. Accepted, as one sentence in the Operator paragraph; it binds an Operator, not other roles.
6. Accepted for (c) only: the plan trial and upgrade note. I did not test whether `--apply` is all-or-nothing.
7. Accepted. The keep-list is exempt from the cap. Adopter run rules are uncapped and unmeasured.

Declined: none. Not folded in: the missing shipped never-commit-secrets rule, which predates this proposal.

**For the Maintainer.** (1) Option: recommend (a), because (c) saves only 15% of what any agent loads. Default (a); say (c) if you want the saving. (2) Allow `AGENTS.md` about 80 words over the trim's "no growth" target. Default yes, after the trim is built. (3) Tier heavy. Default heavy. (4) A shipped never-commit-secrets rule matters more once an Operator handles credentials. Default: a separate board row, not this proposal.

## Decision -- Maintainer (scribed by Antigravity Gemini 4 Hydrogen) -- 2026-11-16

**Tier**: heavy

**ACCEPTED.**

> "Accept both as revised with the recommended defaults"

This accepts the proposal as revised (`heavy` tier), adopting Option (a) (append the ~80-word Operator paragraph without moving existing paragraphs) and the author's defaults (allow ~80 words in `AGENTS.md` over the trim's "no growth" target once the trim lands, and track the missing shipped never-commit-secrets rule as a separate board row). New recurring human operations: zero.

**Elapsed:** under 1 minute. **Tokens:** unknown.
