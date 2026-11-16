# Narrow the heavy-tier trigger, say how a tier is lowered, and add one Windows fetch line

**Author**: Claude Sonnet 5.5 (claude-sonnet-5-5)
**Status**: awaiting-review
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
- Published docs, 10 files, 14 places: `docs/methodology/lifecycle.md` (1), `docs/methodology/dual-review.md` (1), `docs/methodology/roles.md` (1), `README.md` (1), `docs/index.html` (2, one is image alt text), `docs/getting-started.md` (1, alt text), `docs/release-process.md` (1), `docs/glossary.md` (2), `docs/dev-tour.md` (1, a byte copy of the dev-tour above), `docs/assets/three-lanes-of-change.svg` (3).

Total 21 files, 29 places. Cairn's own `AGENTS.md` carries no trigger line (945 words; unchanged). The plan carries the exact replacements.

**Left alone on purpose:** the proposal-path rule that a change touching a high-risk surface needs a proposal (`docs/methodology/lifecycle.md` line 45, `docs/methodology/proposals.md` line 148, session-start `SKILL.md` line 124, in both copies) and the module `security-verification.md`, which defines which files are surfaces. A touching change still opens a proposal; it may simply be light.

## Proposal

**A. Trigger.** Replace each of the 29 places with this meaning: "Heavy applies when a change substantively alters the behavior or inputs of a named high-risk surface, or adds or widens a trust boundary. Editing, moving or calling a surface does not by itself. Reach counts as altering only when it changes what the guard assumes about its caller; a reviewer names the assumption and says whether it changed. A newly found boundary still stops work for reassessment." Add no author or reviewer obligation. `security-review.md` also gains the caller sentence next to its existing "not widening" paragraph.

Worked cases:
- *Stays heavy:* a change to how `bootstrap/scaffold.py` validates a path from a manifest. It alters a guard's behavior.
- *Drops:* renaming a function or fixing a comment in `bootstrap/_scaffold/`, or moving a guarded routine with its checks and their order unchanged. Nothing the guard accepts or does changes.
- *Marginal:* the #62 case, a new command running an already-guarded fetch unattended with a caller-chosen input file. The guard assumed a person at a keyboard; that assumption changed, so it counts as altering. If the guard never depended on who called it, it does not.

**B. Lowering a tier.** Add to `docs/methodology/lifecycle.md` and `dev/agent_collaboration.md` (and the shipped twin): only the Maintainer lowers a tier, in chat or a Decision; an author or reviewer may recommend it. The plan records, in one appended `Plan change`: the Maintainer's words, the cancelled chunks, the obligations that lapse (those whose only source was a cancelled chunk, such as a Security Review of code no longer written) and those that remain (fences, Maintainer-reserved steps, model floors, anything tied to remaining chunks), the new header values, and that the remaining scope does not alter a high-risk surface or widen a boundary. A review already held stays valid for the scope it covered and transfers to nothing else. A raise follows the same pattern.

**C. Windows.** One sentence in the "File and path handling" item of `security-review.md` and its twin: a `file:` URL or a path taken from a manifest or argument can name a network share (UNC path), which Windows opens over SMB and may offer the user's login hash to that host; refuse or normalize before any open, and do not count an HTTP-level guard as a network guard. Size caps stay out; #89 asks only that they be listed as open checks, and the board row asks for one line.

**Does any rule weaken or disappear?** Yes, deliberately: (1) "touches a high-risk surface" as a heavy trigger; (2) the surface-based Security Review obligation in `dev/rules/protected-surfaces.md` (last sentence), `roles.md` and both `model-selection.md` copies ("owes the Security Review that surface already requires"), which now follows the new trigger. Kept: the Maintainer sets the tier, stop on a newly found boundary, the two-pass cap, fences, and the proposal-path rule. Added: the caller sentence, the lowering rule, the Windows line.

## Rationale

One change made once beats 29 places drifting apart. The caller sentence turns a judgment call into a named assumption that a reviewer can check.

**Relation to `dev/proposals/2026-11-10-claude-template-scan-and-risk-list.md` (accepted):** it changes what is on the high-risk list (prose templates leave it); this changes what a change must do to a listed surface to trigger heavy. They edit some of the same files (`dev/rules/protected-surfaces.md`, both proposal templates), so the plans must be sequenced.

## Alternatives considered

1. **Do nothing.** Costs Security Reviews on changes that cannot use them and stop rules in agent briefs; I have no count.
2. **Edit only `lifecycle.md`.** Leaves 28 places contradicting it.
3. **Keep "touches" and list exemptions.** The lists grow; #37 already shows the pattern.

## Documentation / doctrine surface

The 21 files above, by layer: doctrine in `docs/methodology/`, governing text in the shipped `AGENTS.md`, deliberation in `dev/`. Add to the existing "Changed: Security Review triggers" entry in `CHANGELOG.md` (not new).

## Evidence / verification plan

After the edits, `git grep` for the old phrases finds no leftover; `python scripts/claim_check.py` on each edited document. Wording-pin tests: not checked; the plan finds them by reading, as `dev/rules/working-agreements.md` directs.

**Check of Cairn's own code for the #89 exposure (done, by reading; not run on Windows).** Searched shipped and Cairn-only tools for URL or path opens. `scripts/check_release_publication.py` requests a fixed GitHub host. `scripts/link_check.py` (identical copy in `templates/modules/team-gated/`) probes only http and https and skips `file://` links; but for a relative link target in a Markdown file it resolves and tests existence before its repo-root containment check, and I saw no refusal of a Windows network path. It could therefore reach a network share from a hostile link on Windows. The install and upgrade paths reject backslashes, drive colons and absolute paths (`bootstrap/_scaffold/lockfile.py` line 604, `upgrade.py` line 240). Not checked: Windows behavior, `run_portable_security_sweeps.py` origin handling, the interpreter-binding path, every argument parser. Recommend `link_check.py` be handled as its own defect, outside this plan. It is now item 8 of `dev/proposals/2026-11-16-claude-adopter-defects-0-7-0.md`.

### Security preflight

N/A: no trust boundary added or widened; the change narrows a review trigger, which the Security Review should examine below.

## Signals the change is wrong

A Security Review later finds a real boundary change that the narrowed wording let through at light or standard; a reviewer cannot name the caller assumption in a marginal case; an author lowers a tier without the Maintainer's words; or the 29 places disagree after the plan.

## Scope delta

N/A: opening proposal.

## Assurance path

**Assurance path**: high-assurance (governing doctrine and the authoring templates).

**What the Security Review should examine:** (a) apply the three worked cases and the #37 cases to the new wording and try to find a boundary change that now falls to light; (b) that the caller sentence cannot be read to excuse widened reach; (c) that the lowering rule gives an author or reviewer no way to lower a tier or drop a fence; (d) the 29 replacements agree, twins included; (e) the Windows line is accurate.

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
