<!-- claim-check-allow: scripts/transition_lint.py, templates/modules/default-on/_lifecycle_metrics/, templates/modules/default-on/lifecycle_metrics.py -->
<!-- The three paths above are cited only as evidence that they no longer
     exist -- all three were deleted by the 2026-08 subtraction sweep. -->

# PLANNING.md bankruptcy — queued-block issue drafts

Drafting-only working file. Nothing here has been filed as a GitHub issue;
that is a separate, human-approved step. Do not edit `dev/PLANNING.md` from
this file — this is a one-way extraction.

## Method

Read every row in `dev/PLANNING.md`'s `## Queued` block (skipping its two
lead-in bullets, which are notes about what already left) and in
`## Migrated Cairn roadmap (2026-06-12)`'s `### Queued` and
`### Deferred follow-ups (durable home)` subsections. That is **20
top-level rows**: 7 from `## Queued`, 5 from the migrated roadmap's
`### Queued`, 8 from its `### Deferred follow-ups`. One of the 20
(`## Queued`'s "Four deferred Maintainer questions") itself bundles four
distinct sub-questions, so the real count of individually-checkable claims
is 23.

Every claim about a file, symbol, tool, or proposal's status was checked
against the current tree before being repeated (`git grep`, `find`, or
opening the cited archive) rather than carried forward from the row's
original wording. That check changed the outcome for a large fraction of
the material: **9 of the 23 individual findings turned out to be already
resolved, already implemented, or to have lost their subject entirely** to
the recent subtraction sweep or to work that landed after the row was
written but before `dev/PLANNING.md` was updated to say so. One further row
duplicates content already tracked elsewhere and was not drafted as a new
issue. The rest consolidate into **4 issues** — grouped by what someone
would actually sit down and do, per the Maintainer's instruction to produce
"as few issues as possible," not by which row each finding happened to
arrive on.

**Result: 20 source rows -> 4 issues**, plus 1 duplicate-elsewhere note and
9 dead/resolved findings (listed at the end, with the measurement that
showed each one settled).

---

## Issue 1: Cairn's review-record mechanics let information silently go missing between revisions

Cairn's lifecycle requires proposals and plans to be append-only: each
Response appends one complete current-contract revision plus a mandatory
`Withdrawn / superseded commitments` ledger. Four independent, verified
observations show this mechanism has real gaps where content is lost or
left undecided, with nothing catching it until a reviewer notices by hand.

**1. A withdrawal ledger records the corrected value, but not the reasoning
that produced it.**
Filed 2026-08-20, from an adopter-issue proposal set. A proposal's contract
wrongly declared "no Security Review trigger" for a claim-scanner change; a
blocking review refuted it (the trigger is surface-based, and the proposal
template names the content scanner as a trigger). The contract was
corrected in Revision 2 and carried through Revision 4. A later
decision-support pass then independently re-derived a different, narrower
argument — that the change "strictly modifies report formatting" —
concluded no trigger applied, and that wrong conclusion made it into the
scribed Decision summary, which now contradicts the very contract the
Decision accepted.
What travelled forward was the corrected *value*; what didn't travel was
the *reasoning* that produced it. The withdrawal ledger records that a
claim was withdrawn and why — but only for a reader who opens it. A reader
who instead re-derives the claim from scratch has no way to know a
contradicting answer was already settled. This is dangerous precisely
because the rest of the artifact is correct — only the skimmed summary is
wrong.

**2. Complete-contract revisions have twice lost entire sections between
Response revisions, undetected for two review rounds.**
Two instances observed 2026-08-19 in the same proposal. (a) A field named
`by_file` silently changed meaning — from a per-file *cost* number to a
*node count* — between revisions, unlisted anywhere. (b) Two entire
sections (a reader contract and a security preflight section) were present
in Revisions 1 and 2, absent from Revisions 3 and 4, and neither the author
nor the External reviewer noticed for two full rounds.
The mechanism's blind spot: the `Withdrawn / superseded commitments` ledger
is populated from the author's memory of what they *consciously* changed.
An omission is, by definition, not something the author remembers
changing, so it never reaches the one instrument built to catch dropped
commitments.
A cheap mitigation was applied ad hoc in the two live proposals affected:
each revision now restates the prior revision's `###` section-heading
inventory and states explicitly that none is missing. That's mechanical
enough to standardize, either in `dev/proposals/_template.md` or as an
automated check. The automated route available when this was first written
— a lifecycle checker that parsed these headings — no longer exists:
`scripts/transition_lint.py` was removed by the recent subtraction sweep
(confirmed: the file is gone, and no `.py` file anywhere in the tree
currently parses the `Withdrawn / superseded commitments` heading). Today
only the template-convention route is viable; there is no existing tooling
to extend.

**3. No proposal or plan has a stable way to name "all of its sections,"
which blocks any rule that needs completeness.**
Registered 2026-08-21, from a proposal about ending open-ended code-review
loops (`review-loop-termination`, archived 2026-08-20). That proposal
wanted a rule saying "every finding raised in the preceding review round is
disposed of" — but an append-only artifact has no durable handle on its own
set of sections, so there was no way to state what the rule had to be
complete *over*. This gap made the proposal's original design unbuildable
and forced a withdrawal of that part of the change. The proposal did land a
narrower working substitute instead: a reviewer can now bind a finding's
closure evidence into the finding itself at the moment it's raised, so an
author's later Response carrying that evidence can close the finding
without a fresh review round (security-review findings are excluded and
always loop). That substitute sidesteps the identity problem rather than
solving it.
*Revival condition (from the source material):* a second rule that needs
set-completeness over an append-only artifact. The closure-binding
substitute above is itself a candidate — if a future change needs it to
reason about "the complete set of findings," that would be the second
instance the doctrine-evolution rate limit wants before this becomes its
own proposal.

**4. Whether the proposal template's `Touches` header line is append-only
or editable-in-place was raised and never actually decided.**
Raised during the `fork-advisory-semantics` proposal (archived 2026-08-03,
finding I5): a proposal's `Touches` line — which names the files it
affects, and which other proposals grep against to find related work —
pointed reviewers to the wrong artifact because a sibling proposal's
`Touches` line didn't list a file it needed to. Cairn's `Status` header
field is already treated as mutable even though the rest of a proposal is
append-only, so `Touches` plausibly should be too — but the proposal's
author explicitly declined to decide it alone and handed the Maintainer
three options: edit `Touches` in place going forward (the author's own
recommendation, since `Touches` is the discovery index other proposals
search against, and a stale index defeats the point); leave it frozen at
open-time and treat a restated line elsewhere as authoritative; or a third,
unstated alternative. The proposal's Decision record ("Accepted, as
revised") does not clearly pick one of the three, and `Touches` mutability
is not documented anywhere in current doctrine (`AGENTS.md`, `doctrine/`)
or in `dev/proposals/_template.md` — the field simply isn't discussed
there today.

**Suggested label:** `enhancement` (a lifecycle-mechanism gap; whichever
fix is chosen touches the proposal template and/or a checker script).

**Sources folded in:** `## Queued` > "[DOC] Candidate: a withdrawal ledger
records the correction, not the reasoning" (its first finding only — its
second finding, about invariants proven true by their own wording, is
folded into Issue 2 below); `## Queued` > "Complete-contract revisions lose
sections silently, and the ledger cannot see it"; `## Migrated Cairn
roadmap (2026-06-12)` > `### Deferred follow-ups` > "A stable section
identity for an append-only artifact, and a complete-set rule over it";
`## Queued` > "Four deferred Maintainer questions" (its `Touches`-header
sub-question only).

---

## Issue 2: Agent verification and delegation discipline — a synthesis pass is owed

This groups six related, independently-observed gaps in how agents (and
teams of agents) verify their own and each other's work. None individually
clears Cairn's doctrine-evolution rate limit on its own — several are
explicitly one incident, one day, one plan — but together they are the
backlog the rate-limit gate's own "synthesis at a routine boundary" escape
hatch exists for. The ask is not six separate doctrine changes; it is one
deliberate pass deciding which of these (if any) actually warrant an
`AGENTS.md` edit versus staying informal practice.

**1. A verification-boundary budget was blown roughly 6x over by delegated
subagents who never saw the budget — and this one has already been routed,
which matters so it isn't reopened by accident.**
Observed 2026-08-13 during the implementation of the `review-efficient-lifecycle`
plan (archived), raised by the Maintainer. `AGENTS.md`'s verification-boundary
rules say outright "do not pay for the same broad run at every one" and
budgeted exactly two full test-suite runs for that work. The chunk actually
ran the full suite **13 times** — roughly 2¼ hours of compute — because
**11 of the 13** were subagents independently reaching for
`pytest bootstrap/tests` (the obvious way to answer "did this break
anything") with nothing in their brief saying a budget existed or that a
far cheaper six-file scoped mapping (~70 seconds) was available. The
implementing agent held that mapping and never passed it down. The plan's
own recorded verification section shows only the two budgeted runs
(622.22s and 689.49s); its code reviewer states outright that zero full
suites were run under the reviewed verification boundaries — the 11 extra
runs are invisible to the plan's own record and were caught only because
the Maintainer happened to look.
*Already routed, 2026-08-19.* A six-agent analysis under three adversarial
lenses considered adding a delegation clause to `AGENTS.md` and rejected it
on three grounds: `AGENTS.md` already auto-loads in full into every spawned
session (measured directly), so the rule was never failing to *arrive*,
only failing to be *applied*, because the mapping that would have made it
actionable lived only in the spawning agent's head; a separate doctrine
file (`doctrine/roles.md`) already binds spawning agents on this and did
not prevent the incident; and a written clause would be read by the leaf
subagent too, whose only correct move on reading "verify thoroughly" is to
run the full suite — ratifying exactly the behavior it was meant to
prevent. The adopted rule instead moved verification off the leaf
entirely: **the spawner verifies once, after every subagent's work joins
back together, and no subagent verifies on its own.** That has been
working practice since 2026-08-19.
*What's still open* is only the durable half: there is still no written
doctrine rule for this, because a single day's evidence doesn't clear the
rate-limit gate alone (a cost surface, not security or data-loss, gets no
bypass). *One more fact for whoever picks this up:* the tool that would
have let anyone measure recurrence — a run-frequency ledger from the
`suite-run-diagnostics` plan (shipped 2026-08-21) — was itself retired on
2026-08-26 by the recent subtraction sweep, under that sweep's own accepted
scope allowance. There is currently no instrumentation for this at all;
checking whether the adopted rule is holding means reading plans by hand.

**2. Adversarially pre-reviewing a revision before submitting it catches
real defects — but has its own blind spot.**
Observed 2026-08-19 across two proposal revisions. Before answering an
External review, both revisions were run through four independent
adversarial passes, each instructed to try to find what the *next* review
round would find. Yield: **nine defects in one draft, six in the other,
four blocking each time** — and every one was later confirmed to be the
shape a real reviewer would actually raise (tautological falsifiers, an
unsound classifier, a sanitizer that raised errors on ordinary text, a
resolver that only worked by luck on its own test fixture). The saving is
real: a review round on a high-assurance proposal is one of the scarcest
resources in this method, and a contract that has already survived an
adversarial read is a materially different artifact from one that has only
survived its own author.
*The counter-observation, recorded because it's load-bearing:* a
pre-review optimizes for the specific defect it names, not for the
artifact's actual purpose. In one case, a pre-review "fixed" an undeclared
value-type problem by changing a cost field into a node count — silently
destroying what the field was *for* — and the next External review round
caught it as a scope regression. A pasted-in pre-review fix needs the same
"does this still do the job" sanity check as any other edit the author
writes.

**3. Three invariants were true by their own wording, not by the hazard
they claimed to cover — plausibly the same rule `AGENTS.md` already states
for automated checks, applied one level up to hand-written invariants.**
Observed 2026-08-20: an identity check over an empty set, a claim scoped to
"any path that a report-reading function refused" written for a path that
never actually called that function, and an oracle that projected away the
exact field it was supposed to be guarding. Each was only caught when
someone actually ran the falsifying mutation. The general shape — *state an
invariant over the whole space it claims to cover, and run its falsifying
mutation before trusting it* — reads as the same rule `AGENTS.md` already
states ("Confirm the instrument before trusting an absence," `AGENTS.md`
line 239), just applied to hand-written invariants instead of automated
tooling.

**4. Work-intent claims are advisory, not locking, and lost work when
treated otherwise.**
Same 2026-08-13 session. Two artifacts moved under a work-intent claim this
session was actively holding, one of them discarding an uncommitted edit in
the process. Every individual action was correct — a work-intent claim is a
coordination *signal*, not a lock — but an agent that reads "claim before
editing" without also reading "and re-check the file's actual content,
because the claim guarantees nothing" will eventually lose work exactly
this way.

**5. A figure is only true at the commit it was measured, and Cairn's
precision rule doesn't currently cover "dispositions."**
Filed 2026-08-19. `AGENTS.md`'s numeric-precision rule dates a published
*snapshot* claim, but says nothing about a *disposition*
(`accept`/`defer`/`wontfix`/etc.), which is also a time-sensitive claim
about state and currently carries no date convention at all. Three
instances landed in one plan: an AST-baseline symbol count written as 35
that was already 37 by the time someone read it (caught by the code
reviewer, not the author); undated corpus totals that had to be challenged
before anyone dated them; and a `Dispositions:` block that named three
artifacts `defer` after a re-anchor ceremony had already landed them —
caught only because the block happened to be re-measured immediately
before commit. If this recurs, the likely cheap fix is a convention that a
disposition names the commit it was measured at, the same way a snapshot
claim already names an `as_of`.

**6. The shared working tree — not just the git index — is a coordination
hazard nothing currently covers.**
Observed 2026-08-12: a concurrent session's path-scoped commit swept up
another agent's *uncommitted* review-section edit into its own commit; the
author noticed and corrected it by hand. `AGENTS.md`'s commit discipline
(commit with explicit paths, never a bare `git commit`) protects the shared
git *index* completely, by construction — but says nothing about two
sessions editing the same file's *working-tree* content at once. Recorded
once, so a second occurrence clears the doctrine rate-limit gate rather
than needing to be rediscovered from scratch.

**Suggested label:** `enhancement` (process/doctrine synthesis; may or may
not produce a code or template change depending on what the pass decides).

**Sources folded in:** `## Queued` > "[DOC] Candidate..." (its second
finding only — the three-invariants observation); `## Queued` >
"Agent-facing discipline does not survive delegation" (both its
verification-boundary and work-intent findings, plus its full routing
history); `## Queued` > "Adversarially pre-reviewing a revision before
submitting it"; `## Migrated Cairn roadmap (2026-06-12)` >
`### Deferred follow-ups` > "Doctrine candidate: a figure is true at a
commit, not in general" and "The shared *working tree* is an uncovered
coordination hazard".

---

## Issue 3: 0.4 release-readiness checklist

Four separate roadmap rows all gate on, or are scoped to, Cairn's 0.4
public release. Consolidated into one checklist since a maintainer
preparing for 0.4 would triage them together; urgency differs per item and
is called out below.

**Blocking the 0.4 public release:**
The 0.3 external correctness test (an "R-H third-party probe") is the
launch gate: a consenting third-party scientific repository — one that did
not contribute to Cairn's own doctrine — needs to run the bootstrap
procedure end-to-end. Confirmed still outstanding: `dev/PLANNING.md`'s own
"Where the project stands" section currently states "Phase 5 — launch and
governance — is in progress; the R-H third-party correctness probe (plan
chunk 5.3) is still outstanding, awaiting a consenting third-party
scientific repository that did not contribute to the doctrine." This blocks
0.4 and has no trigger other than successfully enrolling that third party.

**Required before 0.4 ships (not blocked on an external party, but
unactioned):**
The Maintainer decided on 2026-06-12 that Cairn no longer needs a
collaboration agreement as a concept — and that decision has not yet been
executed anywhere, over two months later. It requires retiring
`templates/core/dev/collaboration_agreement.md` (confirmed still present)
and re-homing or dropping every surface that currently points at it: the
`AGENTS.md` required-reading link, the `dev/agent_collaboration.md` /
`dev/README.md` pointers, the onboarding-tour step, `doctrine/plans.md`'s
citation of the External Review Norms it currently carries (those norms
need a new home if the file goes), the scaffold's expected-folder wiring,
and the bootstrap test suite. This is genuinely cross-cutting (doctrine +
templates + scaffold + tests) and was called out at the time as needing its
own proposal rather than a quick edit. Worth flagging: Cairn's *own*
current onboarding tasks still actively reference
`dev/collaboration_agreement.md` (a seed task asks a team to fill its
`team-roster` slot), and Cairn's own copy of the file
(`dev/collaboration_agreement.md`) is also still present — so this decision
has had no effect on Cairn's own tree either, yet.

**Non-blocking polish, queued for 0.4:**
Two related follow-ups on adopter-facing documentation:
- Add graphics/figures to the adopter-facing docs and quickstart to lower
  the "doctrine-heavy at first contact" friction a new adopter hits, plus a
  repo-wide comment-cleanup pass (strip blow-by-blow process commentary,
  keep only comments that explain *why* the code is the way it is) before
  public adopters fork the code. `AGENTS.md`'s current convention already
  states this rule ("Comments and docstrings explain the code, not the
  process," `AGENTS.md` line 264) — this item is the concrete pass that
  applies it everywhere before the code goes public.
- Give the scaffold a context-aware `--quickstart` mode: no such CLI flag
  currently exists in `bootstrap/scaffold.py` — the only related surface
  today is a static "Next steps for a real adoption" print block in
  `bootstrap/_scaffold/install.py`. The ask is a mode richer than that
  reframe, one that prints a trimmed next-step tailored to the
  trivial/throwaway-repo adoption path. Paired with this: extend the
  existing `verify:` count-guard drift mechanism (confirmed live at
  `scripts/verify_counts.py` and `scripts/measurements.py`) to cover more
  of the adopter-facing counts scattered through the docs, beyond the two
  the quickstart currently guards.

**Suggested label:** `enhancement`.

**Sources folded in:** `## Migrated Cairn roadmap (2026-06-12)` >
`### Queued` > "0.3 external correctness test (R-H third-party probe)",
"Remove the collaboration agreement", and "0.4 launch-surface polish";
`## Queued` > "Adopter-entry doc-refresh follow-ups".

---

## Issue 4: Doctrine candidate — an enumerated feature list is a claim surface that goes stale

Deferred 2026-08-20, folded up from an archived documentation-enhancement
note. Any hand-maintained list of capabilities on an entry-facing page (a
README, a landing doc) is exactly the class of problem Cairn's
doc-drift-prevention machinery exists to guard against: the list is a claim
about the current state of a moving system, written once and never
mechanically checked against reality again. The observation was made
against Cairn's own README but explicitly generalizes past it — any adopter
who writes an enumerated feature list on their own entry page inherits the
same risk.
This is a candidate line for the `doc-drift-prevention` module's doctrine
(confirmed still live at `dev/modules/doc-drift-prevention.md`, and shipped
to adopters at `templates/modules/team-gated/doc-drift-prevention.md`) —
not yet written up as an actual doctrine change.

*Revival condition (from the source material):* a second instance of an
entry-page feature claim actually going stale, or an adopter hitting this
problem themselves. One incident does not clear Cairn's doctrine-evolution
rate-limit gate on its own, and as of filing this was the only instance on
record.

**Suggested label:** `documentation`.

**Sources folded in:** `## Migrated Cairn roadmap (2026-06-12)` >
`### Deferred follow-ups` > "A feature list is a claim surface".

---

## Already tracked elsewhere — not drafted as a new issue

**Shipped-executable authority unification** (`## Migrated Cairn roadmap
(2026-06-12)` > `### Queued` > "[VER-5] Shipped-executable authority
unification"). Verified still open — but it already has a full entry in
`dev/strategy/2026-08-05-codex-security-strategy.md`'s Live residual
register, with three tracked sub-findings: a name-keyed census that's blind
to `_OPTIONAL_TEMPLATES` in `bootstrap/_scaffold/config.py` (a delivery
registry that never reaches the install manifest); an unguarded
union-vs-replacement monotonicity claim in `scan_targets()`; and Bandit
allowlist liveness, owned by a separately tracked item. Filing a duplicate
GitHub issue for this would recreate exactly the "same scope tracked in two
places" problem `dev/PLANNING.md`'s own security-cluster routing section
was written to prevent. Noted here only so this row's disappearance from a
future `dev/PLANNING.md` is traceable to something other than data loss.

---

## Dead — subject gone (verified; not drafted as issues)

1. **Stage-reader tier-semantics defects in `_lifecycle_metrics/gitmeta.py`**
   (`## Queued` > "Stage-reader tier-semantics defects, and the price of the
   ratified narrowing"). The entire `_lifecycle_metrics` module was removed
   by the recent subtraction sweep. Measurement: `find . -iname
   "*lifecycle_metrics*"` and `find . -iname "*gitmeta*"` both return
   nothing anywhere in the working tree; `CHANGELOG.md`'s own
   `claim-check-allow` comment lists
   `templates/modules/default-on/_lifecycle_metrics/` and
   `templates/modules/default-on/lifecycle_metrics.py` as historical-only
   paths expected not to exist.

2. **Broad-look + roadmap pass** (Migrated roadmap `### Queued` >
   "Broad-look + roadmap pass"). Already complete. Measurement:
   `dev/PLANNING.md`'s own "Where the project stands" section states "The
   broad-look pass is done (2026-07-08...)";
   `dev/strategy/2026-07-08-claude-broad-look-skeptical-review.md` exists
   on disk.

3. **The key-channel probe cannot see an agent-held key** (Migrated roadmap
   `### Deferred follow-ups`). Resolved by the archived `ceremony-as-code`
   plan (`dev/plans/archive/ceremony-as-code.md`, chunk A1: "Stage 1 stops
   receiving `SSH_AUTH_SOCK` at all"). Measurement:
   `bootstrap/tests/_gate_preflight.py` currently contains the comment "the
   stage-1 loader is invoked with NO `SSH_AUTH_SOCK` at all."

4. **The probe's "non-interactive" claim is false** (same source section).
   Resolved by the same plan (chunk A2: the docstring is corrected).
   Measurement: `bootstrap/tests/_gate_preflight.py`'s `probe_cannot_sign`
   docstring now reads "Timeout-bounded, and NOT non-interactive."

5. **Cairn's roster pins a general-purpose auth key** (same source
   section). Resolved by the same plan (chunk H1: commit a dedicated key's
   public half). Measurement: `dev/.cairn/allowed_signers` currently
   contains exactly one line, pinned to a dedicated key
   (`kendal30@msu.edu ssh-ed25519 ...`), not the Maintainer's general
   GitHub authentication key the row described.

6. **Opaque finding-IDs in code comments and docstrings** (Migrated roadmap
   `### Deferred follow-ups`). The row itself already read "DONE," closed
   2026-08-19 by the archived plan
   `dev/plans/archive/comprehension-outlives-the-artifact.md`. Confirmed
   still true; listed here only for completeness since it was one of the
   block's rows.

7. **The Class C security follow-on** (sub-item of `## Queued` > "Four
   deferred Maintainer questions," the "Class C orphan" question).
   Resolved. Measurement: `bootstrap/_scaffold/SECURITY_MUTATIONS.md`
   states directly, "Status of the follow-on, as of 2026-08-04 ... —
   OWNED, and R7 discharged... Trigger (a) fired: the ruling assigns it" —
   the Maintainer assigned it to the `fork-advisory-semantics` plan's scope
   on 2026-08-04, one day after the row that asked for it to be recorded.

8. **The proposed `AGENTS.md` governing-layer edit** ("name the trigger,
   and name what it checks," same "Four deferred Maintainer questions" row).
   Already implemented. Measurement: current `AGENTS.md` line 230 reads
   verbatim, "Name the trigger, check what it checks, and open it."

9. **The AST re-anchor runbook residual** (same "Four deferred Maintainer
   questions" row — the sub-item already marked RESOLVED in the source
   text, whose own residual asked whether the AST re-anchor procedure earns
   a runbook of its own). Resolved. Measurement:
   `bootstrap/AST_BASELINE_RUNBOOK.md` exists and its content explicitly
   documents the `scaffold_ast_baseline` / `test_ast_attest.py` re-anchor
   procedure the residual said was missing.
