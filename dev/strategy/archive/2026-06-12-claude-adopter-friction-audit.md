<!-- Merged 2026-08-26 into ../2026-07-08-claude-broad-look-skeptical-review.md
     (live core carried forward; this file is the preserved full record) and
     archived. -->

# Cairn adopter friction: make the smallest recommended path executable

**Author**: Claude (2026-06-12 audit); rebuilt by Codex (Strategy)
**Model**: GPT-5 (Codex)
**Date**: 2026-06-12, rebuilt 2026-08-11
**Status**: revised (External comprehension review folded in 2026-08-11)
**Type**: product-strategy
**Surfaces this would feed**: one adopter-path consolidation proposal; an
immediate quickstart correctness repair; a release-boundary adopter canary; a
small comprehension-floor placement proposal; and a downstream entry-doc
integration after `review-efficient-lifecycle`'s Maintainer promotion Decision.

## The question

Can a solo scientist move from **curious** to **trying Cairn** to **using it on
a real repository**, and explain what they have installed and agreed to,
without needing an author beside them to translate the path?

That is a narrower and more useful question than whether every entry document
is accurate in isolation. Cairn can have a good README, a working scaffold, a
tested quickstart, and still lose the adopter in the handoff between them. The
current audit therefore follows four transitions:

1. **Try** -- can the scientist run the disposable quickstart exactly as
   written and see the promised lifecycle?
2. **Choose** -- after the trial, can they tell which adoption level fits and
   what that choice changes?
3. **Install** -- can they execute the recommended real-adoption path without
   inventing file mappings or silently graduating to a different level?
4. **Understand** -- can they state in their own words what the apparatus does,
   what it will require of them, and when they must stop rather than approve?

## Executive judgment

The **trial works**, but the **handoff to real adoption does not**.

The June doc-refresh held where it was mechanically guarded: the current
quickstart's module and slot counts match a live install, the scientific example
is discoverable, Python 3.11+ is stated consistently, and the scaffold clearly
separates a throwaway shakedown from real-adoption next steps.

The dominant friction has moved one step later. Cairn tells its primary
audience -- a solo scientist with one agent -- to adopt at **Level 1**, defined
as hand-copying the kernel and selected modules. No runnable greenfield Level 1
recipe supplies those mappings. The only complete copy-paste route is
`scaffold.py`, which the docs define as Level 2. `bootstrap-lite` also ends by
running that scaffold while describing itself as a step short of the full
Level 2 procedure. The product has one functioning installer and two names for
the experience around it.

The recommendation is not another installer. It is to **make the existing
scaffold the single installation mechanism for Levels 1 and 2**, with the
levels distinguished by assessment and operating burden rather than by whether
files were copied manually. Preserve the accepted default-on security posture;
make the output and customization obligations progressive. Then test the path
an adopter actually runs.

Execution is not the whole adoption contract. The measured entry surfaces put
roughly 7,800 words of governing prose in front of the agent and project, while
no current canary asks whether a scientist understands the resulting
apparatus. The consolidated path must therefore reduce ambiguity in terms the
adopter recognizes -- required reading, decisions, consequences of skipping,
and reversibility -- and measure comprehension rather than infer it from a
completed command sequence.

## Method

Measured on 2026-08-11 against exact committed source
`0f09170ad65fa7e5ca46d0577465eac63d59727d`, using the canonical interpreter
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13).

I:

* read the front-door sequence in `README.md`, `docs/quickstart.md`,
  `docs/getting-started.md`, `on-ramp/README.md`,
  `bootstrap/prompts/bootstrap-lite.md`, and `bootstrap/BOOTSTRAP.md`;
* mapped the June audit to the archived `adopter-entry-doc-refresh` plan and
  rechecked its claimed durable guards;
* exported the exact Git tree, installed `solo-greenfield` into a new Git
  repository, and compared the terminal output and resulting tree with every
  documented Step 1-3 command;
* ran the published `git add` command and inspected the residual paths;
* ran `python scripts/run_security_verification.py local` in the installed
  tree to classify the new default-on dispatcher's first-run behavior;
* installed an explicit `modules: []` profile to test whether the existing
  scaffold already provides a clean mechanized Level 1; and
* ran `bootstrap/tests/test_quickstart_sequence.py` and inspected what each
  green assertion actually governs.

The External comprehension review rechecked the published module and slot
counts, bare commit shape, README route inventory, and comprehension-floor
placement against parent commit
`8c8a8b9c1940c4a1500930532e0bcade81ff697c`; it did not repeat the cold install.

The falsifier is straightforward: a documented, mechanized Level 1 route that
a fresh adopter can run today would overturn the headline. No such route was
found. This was not a human-subject usability study and did not execute Steps
4-6 through a fresh external AI agent; those are explicit limits, not evidence
that the prompts fail.

## What already works

The entry surface is much stronger than it was at first publication:

* **The front door names the right things.** The README names the audience, the
  cost, the safety boundary, the quickstart, the on-ramp, and both minimal
  examples without pretending Cairn is a package manager or CI system. It does
  not yet reduce those choices to one obvious trial and one obvious adoption
  route; the scientific example is discoverable from the repository map rather
  than carried through the adoption handoff.
* **The disposable install is mechanically real.** `solo-greenfield` resolved
  exactly 8 modules, advertised 72 file-install rows, and reported 22 unfilled
  slots in the clean cold walk. The two counts published by
  `docs/quickstart.md` -- modules and slots -- match the live output.
* **The count guard is non-vacuous within its scope.** The quickstart test reads
  the two prose numbers and compares them with live scaffold output; the module
  count is also registered under `scripts/measurements.py` for
  `check_cairn`.
* **The scary output is mostly explained.** The quickstart prepares the reader
  for the tip-checkout provenance warning, names the installed skills and
  onboarding layer, and explains why a shakedown skips the real-adoption slot
  pass.
* **Default-on security does not falsely report success.** With no selected API
  or web capability, the installed dispatcher returned `NOT_APPLICABLE`, exit
  0, with `evidence_count: 0`; the scaffold had already said that the route
  inspected nothing. This audit does not reopen the Maintainer's accepted
  default-on security decisions.
* **The scientific example is visible and recognizable.** The front door now
  links the mass-balance example instead of leaving the scientist with only a
  greeting CLI.

These are reasons to simplify around the existing path, not replace it.

## Findings

### F1 -- the recommended Level 1 has no executable greenfield path

`on-ramp/README.md` calls Level 1 the natural home for solo + one-agent
adopters and instructs them to copy `templates/core/`, add the modules their
profile selects, fill placeholders, and run the lifecycle by hand.
`docs/quickstart.md` says most teams start there. `docs/getting-started.md`
repeats the hand-copy instruction.

The kernel copy itself is discoverable: `templates/core/` contains 18 tracked
files and 22 slot markers at the measured commit. The selected-module step is
not. The default-on source directory contains module prose, renamed destination
documents, companion scripts, package directories, merge directives, state
files, and generated mappings. No Level 1 recipe tells a greenfield adopter
which source becomes which destination or how to apply the merge contributions.
The installer manifest knows; the human-facing Level 1 path does not expose it.

The solo-legacy recipe demonstrates the mismatch sharply. It uses
`scaffold.py --summary` as a roster oracle, then tells the adopter to hand-copy
10 modules without providing the install map. It is an exact *selection*
recipe, not an exact *installation* recipe.

This is the headline because it affects the audience Cairn most explicitly
claims to serve. A path is not lightweight merely because its automation was
removed.

### F2 -- `bootstrap-lite` and the on-ramp assign different levels to the same action

The quickstart's "What to do next" order is:

1. fill the readiness report;
2. use `bootstrap-lite` to produce a profile;
3. pick an adoption level.

But `bootstrap-lite` has the Maintainer run `scaffold.py --summary` and then
rerun it to install immediately after accepting the profile. The on-ramp
defines running the scaffold as Level 2. By the time the quickstart asks the
adopter to pick a level, the recommended helper has already selected the
Level 2 mechanism.

The distinction bootstrap-lite is reaching for is useful: a solo adopter needs
a shorter assessment than a large legacy team. The error is encoding that
difference as "hand copy versus scaffold." Assessment depth, module selection,
customization timing, and review staffing are the dimensions the adopter cares
about; the byte-copy mechanism is not a maturity level.

### F3 -- the quickstart teaches a commit command its installed rules forbid

Every literal commit in Steps 1, 3, and 4 uses this shape:

```bash
git add <paths> && git commit -m "..."
```

The `AGENTS.md` installed in Step 3 says never to issue a bare `git commit`,
requires explicit paths on the commit command, and explains the shared-index
reason. The quickstart therefore teaches the opposite habit moments before
installing the rule. A solo disposable repository lowers the immediate
collision risk, but the page presents these commands as the lifecycle pattern
the adopter should carry into real work.

The fix is mechanical: use the documented new-file form, `git add <paths> &&
git commit <paths> -m ...`, and use path-scoped commits for later tracked-file
transitions.

### F4 -- the documented install commit is incomplete, while the regression test stays green

The clean cold walk installed `NOTICE.md`. The quickstart's Step 3 staging list
does not include it. Running the exact published `git add` command leaves:

```text
?? NOTICE.md
?? profile.yml
```

`profile.yml` is adopter-created and may reasonably be deleted after a
throwaway install or moved to a durable project-owned profile location for a
real adoption. The page currently states neither disposition. `NOTICE.md` is
unambiguously present in the scaffold's 72-row report and must be committed.

That report is not the final authority the quickstart says it is. It is printed
before the module merge, `.gitignore` seeding, interpreter binding, and
lockfile/base-cache write complete; those later writes are not all in its
list, and `dev/PLANNING.md` appears twice. The durable oracle for a published
commit command is the resulting repository state, not the mid-install report.

`bootstrap/tests/test_quickstart_sequence.py` still reports 8 passing tests.
Its module docstring says Layer A drives the literal shell commands in Steps
1-3, but no test runs the documented Step 3 staging or commit command or
asserts its residual state. The Layer B helper stages an older, smaller set
(`AGENTS.md`, `VENDOR.md`, `dev`, `tools`, `scripts`) and also uses bare
commits. The gate proves counts and lifecycle shape, but its "literal shell
coverage" description overclaims and concealed this recurrence.

This is the same high-yield question Cairn applies to security controls: what
trigger actually executes the claimed check? The test must govern the command,
not merely the files around it.

### F5 -- the smallest scaffold output is not progressive yet

The current `solo-greenfield` scaffold result is not automatically too large:
a long install report can be cheap if the agent manages the tree and the
Maintainer sees only the decisions that matter. The terminal currently turns
file count into human burden, however, by printing 72 install rows and labeling
all 22 remaining slots as "requiring agent attention."

An explicit `modules: []` cold install tested whether the mechanism already
scales down. It still installed 32 files, installed lifecycle skills and the
progressive-onboarding helper, reported all 22 core slots, and told the adopter
to fill all of them. Several slots are contribution points for modules the
profile did not select. Therefore an empty module roster does not yield a
coherent kernel-only obligation set even though the config grammar admits it.

The product need not minimize file count. It needs to distinguish:

* mechanically filled and complete;
* project facts required before first real work;
* selected-module customization scheduled by progressive onboarding; and
* dormant contribution points that require no action under this profile.

That is the context-aware output already gestured at by the deferred
`--quickstart` follow-up, but it should govern real Level 1 too.

### F6 -- timing and comprehension have outgrown the measured path

The quickstart has changed repeatedly since its original pilot. Since v0.3.0,
the measured entry surfaces gained 222 lines and removed 71 across
`docs/quickstart.md`, the installed `AGENTS.md`, the installed proposal
template, the on-ramp, and the solo profile. The current installed
`AGENTS.md` is 2,676 words; the proposal and plan templates add 5,098 words.
The shakedown does not require the human to read all of them, but its agent is
explicitly asked to read `AGENTS.md` before acting.

No current canary records elapsed time, undocumented intervention, warning
interpretation, or whether a fresh agent follows the prompt correctly. The
15-25 minute range may still be right. It is not currently measured evidence.
A static test cannot answer that question.

The larger finding is comprehension load, not word count by itself. Those
roughly 7,800 words govern work for an adopter whose expertise may be hydrology,
ecology, or another scientific domain rather than software process. Completing
the commands does not establish that the adopter understands what Cairn will
ask them to review and decide. No current success criterion or release canary
asks them to restate the purpose and obligations in their own words, so the
project currently measures mechanics and assumes comprehension.

### F7 -- a known lifecycle change has an entry-doc integration gap

The executing `review-efficient-lifecycle` plan conditionally changes the
proposal/plan contract and status vocabulary after its pilot and Maintainer
promotion Decision. Its P7 names `docs/getting-started.md`,
`docs/workflow-role.md`, and `docs/tool-usage.md`; it does not name
`docs/quickstart.md`, `on-ramp/README.md`, or the two minimal examples that
teach the old lifecycle to a first adopter.

This strategy does not expand or de-scope that reviewed plan. It records a
downstream integration condition: if M6 promotes the new lifecycle, the entry
surface must be revised and cold-walked against it before the next release.
Doing that now would document a conditional contract as though it had shipped.

### F8 -- the comprehension floor is published but not installed

`doctrine/rationale.md` makes comprehension a precondition of Maintainer
authority: lead with plain language, preserve precision beneath it, and pause
when the decision-maker does not yet understand. The operational
`templates/core/AGENTS.md` every adopter receives does not state that rule, and
the published `doctrine/` tree is not installed into adopter repositories.

That is a placement gap, not an installer-design problem. Cairn operationalizes
structural independence, verification boundaries, and commit discipline in the
installed agent contract; the rule that makes those outputs reviewable by a
scientist should be there too. A small separate proposal should place the
settled norm in Cairn's and adopters' `AGENTS.md` files, with the existing
rationale remaining canonical in doctrine. It should not enlarge the
adopter-path consolidation proposal.

The related G17 idea -- a communication-calibration dimension or module -- is
not settled by this audit. It needs evidence about recurring communication
failure modes and stays out of the placement repair.

## Options

1. **Refresh the quickstart again and leave the level model alone.** Necessary
   for F3-F4, but it leaves the primary audience on an unexecutable adoption
   path and guarantees another drift round.
2. **Fully document manual Level 1 copying.** Generate a human-readable mapping
   from the install manifest and teach every merge/state step. This makes a
   second installation procedure out of the scaffold's internals and asks the
   least-resourced adopter to operate it manually.
3. **Retire Level 1 and call every install Level 2.** Mechanically honest, but
   throws away the valuable promise that adoption burden should grow with the
   project.
4. **Use one installer; let levels describe burden, not copying**
   (**recommended**). Level 0 remains read-only. Level 1 uses the scaffold with
   a named small-team profile, a short required-reading and acceptance pass,
   progressive customization, and no hand-maintained mappings. Level 2 asks
   for more preparation, project decisions, upgrade commitments, and review
   capacity. The adopter-facing definition answers four questions at each
   level: **what must I read, what must I decide, what does skipping a step
   cost, and can I reverse the choice?** Internal labels such as assessment
   depth, module set, upgrade posture, and review staffing may implement that
   model but should not be the chooser's only vocabulary.

## Recommendation

### 1. Repair the quickstart immediately

Treat F3-F4 as a bounded correctness change, not a product redesign:

* add `NOTICE.md` to the install commit;
* give the disposable `profile.yml` an explicit delete-or-commit disposition;
* make every example commit path-scoped in the exact form installed
  `AGENTS.md` teaches;
* make Layer A run the exact documented staging/commit vectors and assert the
  intended residual state; and
* narrow the test's claim where agent-mediated behavior remains a surrogate.

This closes a live contradiction while the shaping proposal is reviewed.

### 2. Open one adopter-path consolidation proposal

The proposal should settle one product contract: **the scaffold is Cairn's
single installer; Levels 1 and 2 differ in obligations and depth.** It should:

* rewrite the on-ramp, bootstrap-lite, quickstart handoff, profile comments,
  and getting-started route around that contract;
* define a canonical solo Level 1 invocation using the existing profile
  resolver rather than a second copy map;
* classify post-install slots by current profile and timing, so "not selected"
  is never reported as "fill this now";
* define each level in adopter-recognizable obligations: required reading,
  decisions, skip consequences, and reversibility;
* preserve all accepted default-on module and security decisions unless a
  separate proposal changes them on evidence;
* state the durable home of the accepted profile for a real adoption; and
* disposition the old deferred `--quickstart` idea: absorb its context-aware
  output into the general installer rather than add a shakedown-only mode.

The proposal should measure Maintainer decisions and required customization,
not optimize raw file count. Files that need no human attention are cheap;
ambiguous obligations are not.

### 3. Add one release-boundary adopter canary

Before claiming the next release is adopter-ready, a different agent type or a
human who did not author the entry docs should follow the exact path from a
clean, tagged checkout into a disposable repository. Record:

* source tag and interpreter;
* commands actually run;
* elapsed time by step;
* every warning and whether the docs predicted it;
* every intervention not present in the page;
* final tracked/untracked state; and
* whether the agent stopped at each Maintainer gate;
* every term the walker had to look up or ask someone to explain; and
* whether the walker could restate, unprompted and in their own words, Cairn's
  purpose and the obligations they had accepted.

Keep deterministic tests for commands, counts, paths, and lifecycle shape.
Use the canary for comprehension and time. If no canary is run, replace the
15-25 minute claim with an unquantified "short walkthrough" rather than carry
an inherited number.

### 4. Integrate, do not race, the lifecycle pilot

Do not teach `review-efficient-lifecycle`'s conditional status contract before
M6. If the Maintainer promotes it, the adopter-path proposal's release check
must include the quickstart, on-ramp, both minimal examples, and any profile
comment that names lifecycle states. If it is revised or retired, those
surfaces remain on the current contract.

### 5. Place the settled comprehension floor in the operational contract

Open a small, separate proposal for F8. It should add an operational rule to
Cairn's own and `templates/core/AGENTS.md`: agents lead with a plain explanation
suited to the Maintainer's software familiarity, define unavoidable specialist
terms, keep technical precision available beneath the explanation, and treat
"I do not understand this yet" as a required pause before a Decision. The
proposal should preserve `doctrine/rationale.md` as the canonical explanation
and include the self-host/template parity check appropriate to an installed
rule.

Do not add a communication-calibration module or measurement dimension in that
proposal. Those are evidence-seeking extensions; the placement repair merely
makes an already-settled norm reachable where work is governed.

## Success criteria

The adopter path is coherent when all of these are true:

* the README offers one obvious trial and one obvious real-adoption next step;
* the recommended solo route contains no undefined "hand-copy the selected
  modules" operation;
* the same installer implements every non-zero adoption level;
* the post-install report asks only for work the accepted profile makes live;
* every published command is exercised by a governing test and leaves the
  documented repository state;
* the timing claim is backed by a current canary or removed; and
* a promoted lifecycle change cannot release with stale first-contact docs;
  and
* a canary adopter can state in their own words what Cairn does, what decisions
  it reserves to them, and what obligations the selected level creates, with
  every term they needed translated recorded as evidence rather than hidden.

The success measure is **undocumented decisions, interventions, and unresolved
terms**, not installed file count.

## Open questions for the Maintainer

1. **Level meaning.** May the consolidation proposal redefine Level 1 as a
   scaffolded, progressively customized adoption rather than a hand-copy path?
   *(Recommended: yes. One installer removes an entire drift surface without
   making Level 1 more demanding.)*
2. **Accepted profile home.** For a real adoption, should the reviewed profile
   live at `dev/.cairn/profile.yml` and be committed, with the quickstart's
   temporary `profile.yml` deleted after install? *(Recommended: yes, subject
   to checking the upgrade contract before the proposal fixes the path.)*
3. **Timing claim.** Keep 15-25 minutes only if the release canary reproduces
   it? *(Recommended: yes.)*

## Fold-up note

Three findings are methodology-general, but each needs evidence beyond this
single repository before becoming doctrine:

* **An adoption level should name human obligations, not whether bytes were
  copied by hand.** Removing automation from the smallest team can increase
  rather than reduce its burden.
* **Progressive installation and progressive attention are different.** A
  module may be present without demanding a day-one decision; tools should
  classify what is live now.
* **A test that claims to exercise a published command must execute that
  command vector and assert its residual state.** Testing adjacent output is
  useful coverage, not evidence that the recipe itself works.
