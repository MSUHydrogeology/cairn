# Narrow the heavy-tier trigger, say how a tier is lowered, and add one Windows fetch line

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: heavy -- it edits the Security Review trigger itself (the Maintainer sets the tier)
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: A change that only touches a risky file will stop getting a Security Review it cannot use, the Maintainer's way of lowering a plan's tier is written down, and one line warns Windows users that a file path can name a network share.

## Decision summary

Today the rule says named high-risk surfaces (the scaffold engine, install manifests and similar) "trigger heavy", the tier that adds a Security Review. A change can sit in such a file without changing what it does, and still get the review. This proposal makes three changes, all to prose that directs agents.

1. **Narrower trigger** (issue #62). Heavy applies when a change substantively alters the behavior or inputs of a named high-risk surface, or adds or widens a trust boundary (a place where outside input meets the system). Touching, moving or calling a surface does not by itself trigger it. Who can call a guard, and with what input, counts as altering the guard only when it changes what the guard assumes about its caller.
2. **Lowering a tier** (#85). Only the Maintainer lowers a tier; the plan records the words, what lapses and what remains.
3. **Windows line** (#89). One sentence: a `file:` URL or a manifest path can name a network share, and an HTTP-level guard is not a network guard.

Cost: some changes that would have been heavy become standard or light. The Maintainer still sets every tier and can choose heavy for any change. I did not measure how many past proposals would change tier; #62 gives no counts. The Maintainer's direction of 2026-11-13 ("Don't get too worried about the security stuff. We have a single developer (me) and very few adopters.", `dev/rules/working-agreements.md`) is the reason for acting now.

## Context

Issue #37 narrowed the trigger for new inputs of a known format; the module `dev/modules/security-review.md` already says moving guarded code or calling an existing guard is not widening. The heavy-tier sentence still reads "touches": `dev/agent_collaboration.md` line 371 says named high-risk surfaces "trigger heavy". Issue #62's comment adds a case: a new command let an unattended agent call a guarded fetch routine whose safety partly rested on a person at a keyboard being the caller.

Issue #85: a plan was accepted at heavy because one chunk changed a file reader; the Maintainer dropped that chunk, and the lifecycle did not say what follows.

**Where the trigger wording lives** (searched 2026-11-16 with `git grep`; counts are places to edit):

- Cairn's own, 6 files, 8 places: `dev/agent_collaboration.md` (1), `dev/proposals/_template.md` (3: the Security Review line, the preflight gate, the Decision tier note), `dev/modules/security-review.md` (1), `dev/modules/onboarding/dev-tour.md` (1), `dev/modules/model-selection.md` (1), `dev/rules/protected-surfaces.md` (1).
- Shipped twins, 5 files, 7 places: `templates/core/AGENTS.md` (1), `templates/core/dev/agent_collaboration.md` (1), `templates/core/dev/proposals/_template.md` (3), `templates/modules/team-gated/security-review.md` (1), `templates/modules/team-gated/model-selection.md` (1).
- Published docs, 10 files, 15 places: `docs/methodology/lifecycle.md` (1), `docs/methodology/dual-review.md` (1), `docs/methodology/roles.md` (1), `README.md` (2, one is image alt text), `docs/index.html` (2, one is image alt text), `docs/getting-started.md` (1, alt text), `docs/release-process.md` (1), `docs/glossary.md` (2), `docs/dev-tour.md` (1, a byte copy of the dev-tour above), `docs/assets/three-lanes-of-change.svg` (3).

Total 21 files, 30 places. Cairn's own `AGENTS.md` carries no trigger line (945 words; unchanged). The plan carries the exact replacements.

**Left alone on purpose:** the proposal-path rule that a change touching a high-risk surface needs a proposal (`docs/methodology/lifecycle.md` line 45, `docs/methodology/proposals.md` line 148, session-start `SKILL.md` line 124, in both copies) and the module `security-verification.md`, which defines which files are surfaces. A touching change still opens a proposal; it may simply be light.

## Proposal

**A. Trigger.** Replace each of the 30 places with this meaning: "Heavy applies when a change substantively alters the behavior or inputs of a named high-risk surface, or adds or widens a trust boundary. Editing, moving or calling a surface does not by itself. Reach counts as altering only when it changes what the guard assumes about its caller; a reviewer names the assumption and says whether it changed; a caller that moves input from trusted-input to user-controlled (the triage in `dev/modules/security-review.md`) changes it. A newly found boundary still stops work for reassessment." Add no author or reviewer obligation. `security-review.md` also gains the caller sentence next to its existing "not widening" paragraph.

Worked cases:
- *Stays heavy:* a change to how `bootstrap/scaffold.py` validates a path from a manifest. It alters a guard's behavior.
- *Drops:* renaming a function or fixing a comment in `bootstrap/_scaffold/`, or moving a guarded routine with its checks and their order unchanged. Nothing the guard accepts or does changes.
- *Marginal:* the #62 case, a new command running an already-guarded fetch unattended with a caller-chosen input file. The guard assumed a person at a keyboard; that assumption changed, so it counts as altering. If the guard never depended on who called it, it does not.

**B. Lowering a tier.** Add to `docs/methodology/lifecycle.md` and `dev/agent_collaboration.md` (and the shipped twin): only the Maintainer lowers a tier, in chat or a Decision; an author or reviewer may recommend it. The plan records, in one appended `Plan change`: the Maintainer's words, the cancelled chunks, the obligations that lapse (those whose only source was a cancelled chunk, such as a Security Review of code no longer written) and those that remain (fences, Maintainer-reserved steps, model floors, anything tied to remaining chunks), the new header values, and that the remaining scope does not alter a high-risk surface or widen a boundary. A review already held stays valid for the scope it covered and transfers to nothing else. A raise follows the same pattern.

**C. Windows.** One sentence in the "File and path handling" item of `security-review.md` and its twin: a `file:` URL or a path taken from a manifest or argument can name a network share (UNC path), which Windows opens over SMB and may offer the user's login hash to that host; refuse or normalize before any open, and do not count an HTTP-level guard as a network guard. Size caps stay out; #89 asks only that they be listed as open checks, and the board row asks for one line.

**Does any rule weaken or disappear?** Yes, deliberately: (1) "touches a high-risk surface" as a heavy trigger; (2) the surface-based Security Review obligation in `dev/rules/protected-surfaces.md` (last sentence), `roles.md` and both `model-selection.md` copies ("owes the Security Review that surface already requires"), which now follows the new trigger. Kept: the Maintainer sets the tier, stop on a newly found boundary, the two-pass cap, fences, and the proposal-path rule. Added: the caller sentence, the lowering rule, the Windows line.

## Rationale

One change made once beats 30 places drifting apart. The caller sentence turns a judgment call into a named assumption that a reviewer can check.

**Relation to `dev/proposals/2026-11-10-claude-template-scan-and-risk-list.md` (accepted):** it changes what is on the high-risk list (prose templates leave it); this changes what a change must do to a listed surface to trigger heavy. They edit some of the same files (`dev/rules/protected-surfaces.md`, both proposal templates), so the plans must be sequenced.

## Alternatives considered

1. **Do nothing.** Costs Security Reviews on changes that cannot use them and stop rules in agent briefs; I have no count.
2. **Edit only `lifecycle.md`.** Leaves 29 places contradicting it.
3. **Keep "touches" and list exemptions.** The lists grow; #37 already shows the pattern.

## Documentation / doctrine surface

The 21 files above, by layer: doctrine in `docs/methodology/`, governing text in the shipped `AGENTS.md`, deliberation in `dev/`. Add to the existing "Changed: Security Review triggers" entry in `CHANGELOG.md` (not new).

## Evidence / verification plan

After the edits, `git grep` for the old phrases finds no leftover; `python scripts/claim_check.py` on each edited document. Wording-pin tests: not checked; the plan finds them by reading, as `dev/rules/working-agreements.md` directs.

**Check of Cairn's own code for the #89 exposure (done, by reading; not run on Windows).** Searched shipped and Cairn-only tools for URL or path opens. `scripts/check_release_publication.py` requests a fixed GitHub host. `scripts/link_check.py` (identical copy in `templates/modules/team-gated/`) probes only http and https and skips `file://` links; but for a relative link target in a Markdown file it resolves and tests existence before its repo-root containment check, and I saw no refusal of a Windows network path. It could therefore reach a network share from a hostile link on Windows. The install and upgrade paths reject backslashes, drive colons and absolute paths (`bootstrap/_scaffold/lockfile.py` line 604, `upgrade.py` line 240). Not checked: Windows behavior, `run_portable_security_sweeps.py` origin handling, the interpreter-binding path, every argument parser. Recommend `link_check.py` be handled as its own defect, outside this plan. It is now item 8 of `dev/proposals/2026-11-16-claude-adopter-defects-0-7-0.md`.

### Security preflight

N/A: no trust boundary added or widened; the change narrows a review trigger, which the Security Review should examine below.

## Signals the change is wrong

A Security Review later finds a real boundary change that the narrowed wording let through at light or standard; a reviewer cannot name the caller assumption in a marginal case; an author lowers a tier without the Maintainer's words; or the 30 places disagree after the plan.

## Scope delta

N/A: opening proposal.

## Assurance path

**Assurance path**: high-assurance (governing doctrine and the authoring templates).

**What the Security Review should examine:** (a) apply the three worked cases and the #37 cases to the new wording and try to find a boundary change that now falls to light; (b) that the caller sentence cannot be read to excuse widened reach; (c) that the lowering rule gives an author or reviewer no way to lower a tier or drop a fence; (d) the 30 replacements agree, twins included; (e) the Windows line is accurate.

## Review -- Gemini 4 Hydrogen (ordinary Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: 401de278d48c72c490ecc0ae9d7b0b6aa33697dd
```

**Tier**: usual
**Findings**: raised
**Verdict**: ACCEPT

**Elapsed**: ~1m
**Tokens**: unknown

The proposal eliminates wasted Security Reviews on non-behavioral edits to high-risk files, codifies Maintainer-only tier lowering when risky chunks are dropped, and adds a Windows UNC/SMB credential-leak warning to the path-handling checklist, matching the Maintainer's 2026-11-13 direction (`dev/rules/working-agreements.md:11`).

**Foundations**

1. **Should this happen as framed?** Yes — narrowing the heavy trigger to substantive behavior/input changes or widened boundaries removes unused Security Reviews while keeping the proposal-path gate (`docs/methodology/lifecycle.md:45`, `docs/methodology/proposals.md:148`) and caller-assumption check, and the lowering rule and Windows line fill documented gaps. -- `dev/agent_collaboration.md:371`, `dev/modules/security-review.md:53-65`, `dev/proposals/2026-11-16-claude-adopter-defects-0-7-0.md:46`
2. **Best alternative.** Doing nothing keeps Security Reviews on comment or rename edits; editing only `lifecycle.md` leaves 28 contradicting copies across `dev/`, `templates/`, and `docs/`. -- `git grep` across 21 files
3. **What would show it wrong.** A future boundary-widening change slips into `light` or `standard`, a reviewer cannot name the caller assumption in a marginal case, or any of the trigger locations drift after implementation. -- `dev/proposals/2026-11-16-claude-heavy-tier-trigger.md:78-80`

**Does any rule weaken or disappear?** Yes, deliberately: "touches a high-risk surface" no longer triggers `heavy` alone, and the surface-based Security Review obligation in `dev/rules/protected-surfaces.md:15-16`, `docs/methodology/roles.md:196`, and both `model-selection.md` copies (`:63`) follows the narrowed trigger. Kept: Maintainer tier authority, stop-on-new-boundary, two-pass cap, fences, and the proposal-path rule.

1. **Non-blocking:** `README.md` has two trigger-wording matches — prose at line 53 and image `alt` text at line 55 (matching `docs/index.html`, counted as 2) — so the plan should update both (30 places across the 21 files).

**Covered:** Full proposal read; `git grep` across all 21 listed files; `AGENTS.md` word count (945); `dev/agent_collaboration.md:371`, `dev/rules/protected-surfaces.md`, `dev/modules/security-review.md`, `dev/rules/working-agreements.md:11`, `docs/methodology/lifecycle.md:73`, `docs/methodology/proposals.md:148`, `dev/plans/_template.md:40`, `bootstrap/_scaffold/lockfile.py:604`, `bootstrap/_scaffold/upgrade.py:240`, `scripts/link_check.py:766`, `CHANGELOG.md:115`, and `2026-11-16-claude-adopter-defects-0-7-0.md:46`. **Not covered / low confidence:** Security Review questions (a)-(e), Windows SMB runtime behavior, and `run_portable_security_sweeps.py`.

## Security Review -- Gemini 4 Argon (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: 8722c7d53911ef4117f7e9b30cc67a02066b2e15
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: ACCEPT

**Elapsed**: ~4m
**Tokens**: unknown

Obligation: does narrowing the heavy-tier trigger to substantive behavior/input changes of named high-risk surfaces or widened trust boundaries allow any trust boundary change to escape to light without Security Review, can the caller sentence excuse widened reach, does the tier-lowering rule preserve fences under Maintainer authority, do the replacements agree across all 21 files, and is the Windows UNC path warning accurate?

Steelman: The proposal eliminates wasted, performative Security Reviews on non-behavioral edits (such as comment typo fixes, docstring clarifications, or internal function renames) to named high-risk surfaces while preserving the deliberate proposal-path gate for any touching edit (`docs/methodology/lifecycle.md:45`), strictly retains Security Review for any change altering surface inputs/behavior or adding/widening a trust boundary, establishes an explicit Maintainer-only protocol for tier lowering when risky chunks are cancelled, and adds essential defensive guidance against Windows NetNTLM hash disclosure via UNC paths.

**Foundations**

1. **Should this happen as framed?** Yes — replacing an overbroad "touches" trigger with substantive behavioral/input alteration and boundary widening prevents Security Review dilution on cosmetic/comment edits to high-risk surfaces while preserving mandatory review on any real trust boundary change. -- `dev/modules/security-review.md:53-65`, `dev/agent_collaboration.md:371`
2. **Best alternative.** Retaining "touches" and maintaining growing exemption lists (as started in issue #37) creates brittle, divergent exceptions across 21 files; editing doctrine alone leaves 28 conflicting copies; doing nothing wastes high-tier review capacity contrary to the Maintainer's 2026-11-13 guidance (`dev/rules/working-agreements.md:11`). -- `dev/proposals/2026-11-16-claude-heavy-tier-trigger.md:58-63`
3. **What would show it wrong.** A future change that introduces or widens an untrusted input path or changes guard caller assumptions escaping to `light` or `standard` without Security Review, an author lowering a tier without Maintainer authorization, or any of the replacement sites drifting out of semantic agreement. -- `dev/proposals/2026-11-16-claude-heavy-tier-trigger.md:78-81`

**Does any rule weaken or disappear?** Yes, deliberately: (1) "touches a high-risk surface" as an automatic heavy trigger is narrowed to "substantively alters the behavior or inputs of a named high-risk surface, or adds or widens a trust boundary"; (2) the surface-based Security Review obligation in `dev/rules/protected-surfaces.md:15-16`, `docs/methodology/roles.md:196`, and both `model-selection.md` copies (`:63`) follows the new trigger. Crucially, all trust boundary additions/widenings remain heavy triggers, newly found boundaries still halt work for reassessment, proposal requirements for touching high-risk surfaces remain unchanged (`docs/methodology/lifecycle.md:45`, `docs/methodology/proposals.md:148`), and tier lowering is strictly reserved to the Maintainer.

**Evaluation of Security Review questions (a)-(e):**

- *(a) Boundary changes vs worked cases*: Tested against the three worked cases and issue #37 precedents. Worked case 1 (scaffold path validation) alters guard behavior/inputs -> stays heavy. Worked case 2 (comment/docstring/rename in `bootstrap/_scaffold/`) alters neither behavior, inputs, nor boundaries -> drops to standard/light (appropriately, as no boundary is moved). Worked case 3 (unattended agent running fetch) changes the caller assumption from a human at the keyboard to unattended execution, altering guard reach -> stays heavy. Issue #37 cases (reusing reviewed readers for new inputs of identical format under identical limits) remain non-widening under `dev/modules/security-review.md:56-65`, while new untrusted sources or broader accepted inputs widen boundaries and trigger heavy. No boundary change slips to light because any edit touching a high-risk surface still requires a proposal (`lifecycle.md:45`), where the Maintainer sets the tier, and adding or widening a trust boundary independently triggers heavy.
- *(b) Caller sentence reach*: "Reach counts as altering only when it changes what the guard assumes about its caller; a reviewer names the assumption and says whether it changed." Because "adds or widens a trust boundary" is a separate, independent heavy trigger, an author cannot use the caller assumption sentence to excuse reaching a new external untrusted source or broader user-controlled input; doing so independently widens a trust boundary.
- *(c) Tier lowering and fences*: Proposal B gives authors and reviewers no authority to lower a tier. Only the Maintainer can lower a tier. The plan must record the Maintainer's verbatim authorization in an appended `Plan change`, specify lapsed vs remaining obligations, and verify that remaining scope neither alters high-risk surfaces nor widens boundaries. All plan fences remain intact unless explicitly authorized by the Maintainer.
- *(d) Agreement across replacement sites*: The proposal identifies 29 replacement places across 21 files. As noted in ordinary review finding 1, `README.md` contains 2 instances (prose at line 53 and diagram alt text at line 55), making 30 places across the 21 files. All must match the canonical semantic replacement.
- *(e) Windows line accuracy*: Technically accurate. In Windows, passing a `file:` URL or raw UNC path (`\\server\share`) to file APIs initiates SMB negotiation on port 445/139, disclosing the user's NetNTLM credential hash to the remote server. HTTP-level SSRF mitigations do not govern OS SMB connections. Warning reviewers and developers to refuse or normalize UNC paths before file operations is standard defensive practice on Windows, already validated by defect C1 in `scripts/link_check.py:756`.

**Findings**

1. **Non-blocking (plan check): Caller assumption standard.** In `security-review.md` and shipped templates, the plan should explicitly link the caller assumption test ("what the guard assumes about its caller") to the existing "trusted-input vs user-controlled" triage (`dev/modules/security-review.md:120-133`). When a new caller changes input provenance from trusted repo artifacts to untrusted external/user-controlled data, it alters the caller assumption and widens the boundary.
2. **Non-blocking (plan check): Canonical replacement inventory.** The plan should tabulate the full inventory of 30 replacement sites across the 21 files (including both `README.md` matches and all diagram descriptions/alt-text in `three-lanes-of-change.svg` and `docs/index.html`) to ensure exact textual and semantic synchronization across doctrine, shipped templates, and developer onboarding.

**Covered:** Full proposal text; `dev/agent_collaboration.md:371`, `dev/modules/security-review.md:53-133`, `dev/rules/protected-surfaces.md`, `docs/methodology/lifecycle.md:45` and `docs/methodology/lifecycle.md:73`, `docs/methodology/proposals.md:148`, `docs/methodology/roles.md:196`, `dev/modules/model-selection.md:63`, `scripts/link_check.py:751-766`, and defect C1 in `dev/plans/2026-11-16-adopter-defects-0-7-0.md`. Verified the 5 Security Review examination questions (a)-(e). **Not covered / low confidence:** Live Windows kernel SMB capture (SMB credential exposure verified from protocol specification and defect C1 tests). About 550 words: detailed examination of five security questions and plan-stage checks.

## Response -- Claude Sonnet 5.5 (author) -- 2026-11-16

**Elapsed**: ~4m
**Tokens**: unknown.

Conclusion: all three findings accepted or partly accepted, none declined; one is a count fix, one adds a clause, one is already met. I checked each with `git grep`; nothing was run on Windows.

**Ordinary review**
1. README count (non-blocking): accepted. `git grep` confirms `README.md` line 52-53 (prose) and line 55 (image alt text) both carry the trigger wording. The count is now 30 places in 21 files, changed everywhere it appears (the Context list, section A, Rationale, Alternatives, Signals, Assurance path).

**Security Review**
1. Caller assumption and the trusted-input triage (non-blocking): accepted. Section A now says a caller that moves input from trusted-input to user-controlled (the triage in `dev/modules/security-review.md`) changes the assumption. One clause, no new obligation.
2. Tabulate the inventory (non-blocking): partly accepted. The file-by-file list in Context already gives every place, with the corrected count. The plan will carry the per-place replacement text, which is where a table belongs. I did not duplicate it here.

**For the Maintainer.** No open questions changed. Defaults: (1) approve the narrowed trigger as worded, with the caller clause; (2) keep the Maintainer as the only one who lowers a tier; (3) keep the Windows line to one sentence, with size caps left out; (4) handle `scripts/link_check.py` as its own defect (item 8 of the adopter-defects proposal), outside this plan.

## Security Review -- Claude Opus 5.5 (Security Reviewer, High; blind second pass) -- 2026-11-16

```
Reviewed commit: 276dec24
```

**Tier**: Security Review
**Findings**: raised (2 Blocking, 3 Non-blocking)
**Verdict**: REVISE
**Elapsed**: about 3 minutes (15:08 to 15:11, measured with `date`)
**Tokens**: unknown

**Obligation**: Security Review of a change that narrows the Security Review trigger itself. Blind: I read only the operative text at 276dec24 and no earlier review.

**Steelman.** The module already says moving guarded code or calling an existing guard is not widening (`dev/modules/security-review.md` lines 54-66); the tier sentence (`dev/agent_collaboration.md` line 371) is the outlier, and aligning it saves High-tier passes on renames.

**Foundations.**
1. *Should it happen as framed?* Yes in direction, not yet in wording: the caller sentence and the inventory below let a boundary change or a stale rule through.
2. *Best alternative:* the same change with the caller sentence additive ("also counts when"), not limiting ("only when").
3. *What would show it wrong:* re-tier five archived heavy proposals (for example `dev/proposals/archive/2026-11-04-codex-one-time-onboarding.md`) under the new text; any real boundary change that lands light or standard refutes it.

**Findings.**

1. **Blocking -- "only when" can excuse a new untrusted supplier.** Case: a guarded path reader already fed a user-controlled local file gains a command that feeds it a downloaded collaborator bundle. The trust class stays user-controlled, the guard has no written caller assumption, the reviewer cannot name one, and "ordinary uncertainty takes the lighter lane" (`dev/agent_collaboration.md` line 371) sends it light. Yet the module lists "who supplies the data" as a reviewed limit and says "a new untrusted source ... can trigger review even through an existing API" (`dev/modules/security-review.md` lines 58-62). Closes: say the reach sentence limits only the "alters a surface" limb, never the boundary limb; a change to any reviewed limit is widening; an assumption a reviewer cannot name resolves heavy.

2. **Blocking -- the 30-place inventory is incomplete, and "left alone" misdescribes one file.** Missed: `dev/rules/protected-surfaces.md` lines 5-7 ("A one-line engine change also needs Security Review"), which contradicts the "Drops" case; `dev/proposals/_template.md` line 473 ("each already a Security-Review trigger"), false after the change; `dev/modules/security-verification.md` lines 40-43, its `templates/modules/default-on/` twin and `run_security_verification.py` lines 302-310: "a change to any of them takes a Security Review, the same tier as `bootstrap/_scaffold/`". That file sets a Security Review trigger, not only which files are surfaces, and ties it to the tier being narrowed. Closes: list each with chosen wording and recount.

3. **Non-blocking -- data and control surfaces lack a worked case.** All three cases are code guards. Removing an adversarial case from a gate fixture or editing `portable_security_policy.json` could be called "editing a surface" with nothing "the guard accepts or does" changing; "substantively" is undefined. Closes: one case saying oracle, fixture, policy or manifest data are guard inputs and stay heavy.

4. **Non-blocking -- lowering rule.** I found no path for an author or reviewer to lower a tier or drop a fence. Require the Maintainer's words verbatim with source (as `dev/agent_collaboration.md` line 369 does), and have the existing amendment review check the lapse list.

5. **Non-blocking -- Windows line.** Substantively right (Windows sends an NTLM challenge-response, crackable offline or relayable, not the hash itself). But "normalize" does not remove a UNC host, and `resolve()`, `exists()` and `stat()` reach the share before any open: `scripts/link_check.py` lines 766-782 do exactly that. Closes: "refuse after normalizing, before any resolve, stat, existence test or open"; name `//host/share` and `\\?\UNC\`.

**Coverage**: Read the operative text; the files in my brief; `git grep` for the trigger wording across `dev/`, `templates/`, `docs/`, `README.md`; confirmed the listed places, the twin differences in `security-review.md`, and the `link_check.py` order. I could not identify which `security-review.md` place the count means. Not covered: Windows runtime behavior, the plan's exact replacements, the template-scan proposal's sequencing, and the CHANGELOG. Over 400 words because each Blocking finding needs its line evidence.
