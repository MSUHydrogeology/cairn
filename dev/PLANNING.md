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
| **Cairn Plain Language 1.0** (17 rules) | Accepted as revised, `2026-10-26-claude-writing-for-the-reader`; handed to an implementation agent | Maintainer: "We will be adding this Cairn Plain Language 1.0 as a feature". Lockfile `--finalize` for `AGENTS.md` and `dev/agent_collaboration.md`, and a neutrality check on any vendor name in `doctrine/rationale.md`, before it commits. |
| `check_cairn` deleted-file crash | Proposal `2026-10-26-claude-check-cairn-deleted-files`, awaiting review | Defect; one commit. |
| **#32** board and `session-start` accept retired statuses | Maintainer direction, 2026-10-23 | Defect. Lands before drain mode, which reads the board. |
| **#31** "keep it short" in the plan and proposal templates | Prose | The adopter supplied the draft and the evidence. |
| **Model tiers: use the lowest tier that is safe** | Doctrine change: own proposal, clears the rate-limit gate | Maintainer direction, 2026-10-26: formalize a rule set for lower-tier models where possible. Scope below. |
| **Engine batch: F8 and #8 engine half** | Own proposal, Security Review, one AST re-anchor | One batch so the review and the re-anchor are paid once. Maintainer: "Engine batch is in". Rows below. |
| **`repin`** | Proposal first, from `strategy/2026-08-28-claude-repin-revitalization.md` | Maintainer: "Repin is a build". Removes the re-anchor ceremony's manual corrections. |
| **Drain mode**, last | Settled design, `strategy/2026-08-25-claude-drain-mode.md` | Scope below. |

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
under a check, which today requires a different maker's model and so is closed
to a single-vendor adopter. Measurement needs no new machinery: every review
already records its model. The standing rule is written down once in the
repository, not left in an agent's private memory.

**Order.** Cheap defects first (`check_cairn`, #32), then Plain Language, #31
and the model-tier prose, then the engine batch, then `repin` and drain mode.

**Issues.** #31 and #32 are the only open issues in 0.5 (#8's engine half is a
row below; #19 is not in 0.5). Both carry a comment saying so.

**One re-anchor, at the cut.** The re-anchor owed since 2026-10-23 (the Queued
row below) is folded into the 0.5 cut, not paid twice. The AST correction
precedes the gate-manifest re-anchor, as at 0.4. Maintainer-only; follow
`bootstrap/REANCHOR_RUNBOOK.md`.

**Final list: the eight rows above.** **Not in 0.5**, and still queued below
unchanged: making NEXT_SESSION local and untracked, and VER-5 (a new mechanism).
Left out because 0.5 already carries an engine batch, a ceremony and a build;
either can join by the Maintainer's word. **Also not in 0.5, waiting on their
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

### 0.4 cut (Maintainer direction, 2026-10-19)

| Work | Remaining condition before the cut |
|---|---|
| Four security repairs: .gitignore seed guard, session-kernel writes, committed interpreter binding, engine copy fallback | Final review findings dispositioned; their repair and review records are the evidence. |
| `neutrality-and-upgrade-slots`, `independent-scientific-check`, `review-stance-and-lenses`, `board-as-basis` | Archived; retain their final-byte contributions in the ceremony register below. |
| `model-mapping-install-path` | Archived; retain its final-byte contributions in the ceremony register below. |
| README disclosure | State that 0.4 has not had an outside correctness trial. |
| Release assurance | Certify the final committed batch, perform the Maintainer's AST correction **before** the gate-manifest re-anchor, and complete the release sweeps in `docs/release-process.md`. |

**Archived alongside 0.4:** `stewardship-and-reuse`.
**After 0.4:** a draft strategy on Cairn and Assai, removed from Cairn on 2026-10-26 (`6ea4d4d7`).

The release choices remain on record, verbatim:

> "The roadmap says Cairn goes public only after the external test: a
> consenting third-party science project runs the bootstrap end to end. That's
> blocked on finding the third party. What do you want to do?" — **"Waive it
> for 0.4"** ("Go public once the batch lands. The README says plainly that it
> hasn't yet had an outside test. The waiver goes on record in your words.")
>
> "You decided to remove the collaboration agreement 'before 0.4'. The template
> still ships it, and five shipped files reference it. Include that removal in
> this release?" — **"Yes, before the cut (Recommended)"**
>
> "Do the AST and gate-manifest re-anchors at the release cut, rather than
> once after model-mapping as you chose before?" — **"Yes, at the cut
> (Recommended)"**

The later change that added the two plans to the cut, verbatim:

> "I think the model_mapping_install_path should be implemented prior to 0.4"

Asked "Model-mapping into 0.4: you'd set board-as-basis to go before it. What
about board-as-basis?", the Maintainer chose **"Both into 0.4"** ("Keep your
order (board-as-basis, then model-mapping) and ship both."). He added:

> "But, I'll have another agent develop them"

### Public launch — Maintainer-gated

After the batch and release checks:

1. Check that the private mirror renders correctly.
2. Confirm the recorded signing-key fingerprint and two publication channels
   still agree **before the tag**. The release-authenticity record says both
   channels and the forge signing-key endpoint were established on 2026-08-04;
   this is revalidation, not an outstanding first publication. If a channel
   fails, follow the fallback in `bootstrap/PROVENANCE.md` before signing.
3. Make the repository public and set its template-repository flag, on the
   Maintainer's explicit go-ahead. Pushing remains separately authorized.
4. Create the signed `v0.4.0` tag (`git tag -s`).
5. Run the bootstrap block cold against the pushed tag, using a machine and
   roster not supplied by this repository. This is release-authenticity's
   acceptance check.
6. Only after that check, enable Zenodo integration and deposition.
7. Commit the issued DOI to `CITATION.cff`.
8. Archive the original `cairn_methodology_repo` construction plan through
   lasting-truth migration.

Before making the repository public, run the full-history secret scan and
review what the history and GitHub issues expose. Detailed release procedure:
`docs/release-process.md`; sequencing authority and rationale:
`dev/plans/archive/release-authenticity.md`. That plan released the tag, cold
run and Zenodo steps to this sequence before it archived; the cold run remains
owed. Hold the tag if its fingerprint/channel prerequisite is not met.

## Queued

### Re-anchor the gate manifest — one frozen test changed

The 0.4 batch this row used to list was discharged by the re-anchor at
`6f29519d` (2026-10-20) and the AST commits `b9a901f1` and `5cbd6583`; on
2026-10-23 `bootstrap/tests/_gate_manifest.py verify` reported the committed
tree intact (195 frozen files, 4612 pinned nodes) under Python 3.13.

Owed since 2026-10-23: frozen `bootstrap/tests/test_quickstart_sequence.py`
changed so its scripted steps match `docs/quickstart.md` (an `awaiting-review`
proposal, a fresh-session review commit, a quoted Decision, six commits). No
node added or dropped; no engine symbol changed. Maintainer direction:

> "If I need to do a re-anchor, okay"

This is Maintainer-only; follow `bootstrap/REANCHOR_RUNBOOK.md` and derive the
changed set from the final committed tree.

**Waiting on Maintainer**: run the gate-manifest re-anchor

### Other queued work (reviewed Oct 2026)

* **Make re-pinning usable. Targeted for 0.5, as a build.** Promote
  `dev/strategy/2026-08-28-claude-repin-revitalization.md` to a reviewed proposal
  before building `repin`. Until then corrections remain manual. A called
  outside read is the Maintainer's choice, not a standing requirement.
* **F8: make the post-install report match the selected profile. Targeted for 0.5, in the engine batch.** A minimal
  install is asked to fill slots for modules it does not install. Classify
  obligations by the accepted profile; this touches the scaffold engine and
  needs its own proposal and Security Review. Deferred from
  `adopter-path-consolidation` Revision 2, on:

  > "Accept Revision 2 as written. Defer the install-report fix (F8) to the
  > board. No second review round; External floor waived."

* **Name upgrade-added slots (#8, engine half). Targeted for 0.5, in the engine batch.** The integrity command's
  advisory note shipped; `upgrade` still does not distinguish newly added
  slots from all unfilled placeholders. Revival: an upgrade-engine change
  already owing a re-anchor, or an adopter missing a new slot. The current
  engine batch meets the first trigger: the Maintainer should choose at the
  cut whether this stays after 0.4 or joins an accepted plan. Keep the separate
  warning trigger: users filling slots reflexively with `cairn:customized`.
  Owner/evidence: `neutrality-and-upgrade-slots`, Decision Q2 and archive.
  Authorization is the A/B/C/D quote above and the archive instruction:

  > "Go ahead and archive those plans, provided follow-up has a permanent home."

* **Close GitHub #2 and #8 after their fixes are pushed.** The local
  neutrality/slot-note work is archived; this is tracker follow-through, not
  permission to push or close issues now. #8's engine suggestion remains the
  separate row above. #16 was already closed before its paragraph landed;
  changing its closure reason is the Maintainer's choice. Same archive
  authorization as above.
* **Make NEXT_SESSION local and untracked.** Keep durable state in plans,
  doctrine and this board; make the rewritten handoff an operator note like
  reflections. Scope: ignore pattern, scaffold seed, session-routines doctrine,
  AGENTS goodnight wording and session-end description. Own proposal before
  implementation. Maintainer instruction (2026-10-16):

  > "those docs should be, but maybe not NEXT_SESSION?" … "Let's put this up
  > on the board"

* **0.4 launch-surface polish.** Graphics and quickstart presentation; comments
  explain the work without finding IDs. Not a release blocker. Work is picked
  up under the existing change/review rules, not treated as already approved.
* **Unify shipped-executable discovery [VER-5].** One traversal for install,
  manifest, security scan and upgrade. A proposed build, not permission to
  introduce a new mechanism; take its proposal when prioritized.

## Deferred follow-ups (durable home)

Deferred candidates return to the queue when their revival condition is met.
Their earlier reproductions and deliberation remain in the named records and
this file's history.

| Follow-up | What remains / when to revisit | Evidence or owner |
|---|---|---|
| Agents taking their own review turns (#13) | After a recorded two-agent drive, propose a design meeting MA-2's four conditions; account for stale statuses and multiple holders. | `maintainer-attention` scope delta; issue #13 remains open. |
| Scientific-check doctrine and deliverable axis (#19) | Revisit when the third-party trial moves, or on Maintainer direction after about ten real non-N/A checks across two projects. Guidance shipped; the doctrine sentence, axis, disciplines and governance reframe did not. | `independent-scientific-check` C1 and archive; issue #19. Details below. |
| Watch the new review header | After ten proposal reviews, the goodnight scrub owner checks premise/alternative challenges, agent-selected outside reads, thin evidence and lost scope challenges. Put a concerning pattern to the Maintainer. | `review-stance-and-lenses` archive; quoted authority below. |
| Decision rights after agreement removal | Offering Cairn's unsure-case rule to adopters needs its own proposal. Revisit lifecycle escalation wording when a concrete conflict reaches a decision. Neither ships in the 0.4 removal. | `remove-collaboration-agreement` Decision Q3; authority quoted below. |
| Stable section identity and complete-set claims | A second actual rule needing section-set completeness would revive this; naming sections and proving all were handled are one scope. The retired lifecycle checker is not a promised future satisfier. | `2026-08-20-claude-review-loop-termination`, Deferred work. |
| Entry-page feature claims drift | A second stale feature list, or an adopter hitting one, may justify a doc-drift rule. | `2026-08-10-claude-documentation-enhancement` fold-up candidates. |
| Withdrawal ledgers can lose the reasoning | Synthesize on an independent recurrence or a Maintainer call; preserve the distinction between a corrected contract and a summary that re-derives its rejected argument. Also test invariants against their claimed space, not vacuous wording. | `scanner-claim-scope` revisions/reviews; original observations Aug 20. |
| Delegated verification multiplies broad runs | On the next fan-out plan or change to brief composition, reassess the working practice: the spawner verifies after joining; leaves receive scoped tasks. The run ledger was retired, so there is no promised collector. | `review-efficient-lifecycle` H1 observations, Aug 13–19; board history contains the 13-run count and its limits. |
| Pre-reviewing a revision | Revisit on a justified later proposal-review round or a Maintainer choice of workflow. Earlier probes found defects but one fix silently reduced accepted scope; every suggested fix still needs the purpose/scope check. | Aug 19 observations; no new review round or doctrine is authorized here. |
| Complete-contract revisions silently omit sections | A third instance or routine synthesis may justify carrying forward a section inventory. The omission ledger did not detect its own omissions; there is no live lifecycle checker to extend. | Aug 19 two-instance observation; the earlier local mitigation was a heading inventory. |
| Dispositions go stale between commits | An independent recurrence may justify recording the measured commit with a disposition. No doctrine change is authorized by the original one-session evidence. | Aug 19 figures/dispositions observation, formerly under first re-anchor ceremony. |
| Shared working-tree writes | Revisit on a second same-file collision: path-scoped commits protect the index but can still collect another session's uncommitted text in the same file. | Aug 12 observation; separate from index hygiene. |
| Context-aware quickstart | Propose a trimmed scaffold next-step path when the adopter need recurs. | `adopter-entry-doc-refresh` deferred follow-up (Jun 2026). |
| More adopter-facing count checks | Extend the existing verify-count guard beyond the quickstart's two counts when another live count needs it. | `adopter-entry-doc-refresh` deferred follow-up (Jun 2026). |

Authorizations for the first, second and fourth rows are the A/B/C/D Decision
and agreement-removal acceptance quoted above. Monitoring authority, verbatim:

> "Yes, we should keep watching."

> "Keep the monitoring row (Recommended)"

The surviving shared-working-tree observation came from the first-ceremony
batch, retained under this authorization:

> "Yes, go ahead and close everything else from these two plans out, including
> finding a permanent home for any remaining items"

### External correctness trial and scientific-check evidence

A consenting scientific repository that did not contribute the doctrine still
needs to run the bootstrap end to end. **It does not block 0.4 publication**:
the release waiver above is not a completed trial. Revival: enroll a willing
third party. This also revives the scientific-check/axis review (#19).

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
