<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/lifecycle.md reason=published methodology citations -->
# Cairn — development roadmap

Current work and follow-ups, reviewed 2026-10-19. Plans and proposals own their
designs and evidence; this board names the remaining work and its next move.
Completed work leaves the board. The commit history retains earlier versions.

## Where the project stands

<!-- cairn:slot project-status -->
Cairn is at **v0.3.0**, self-hosting and used in LHM and modflow_tools.
**0.4 is the first public release**, after the batch below and the Maintainer's
release steps. The external correctness trial remains open, but was expressly
waived as a condition of publishing 0.4.

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

### 0.4 cut (Maintainer direction, 2026-10-19)

| Work | Remaining condition before the cut |
|---|---|
| Four security repairs: .gitignore seed guard, session-kernel writes, committed interpreter binding, engine copy fallback | Final review findings dispositioned; their repair and review records are the evidence. |
| `neutrality-and-upgrade-slots`, `independent-scientific-check`, `review-stance-and-lenses`, `board-as-basis` | Archived; retain their final-byte contributions in the ceremony register below. |
| `model-mapping-install-path` | Archived; retain its final-byte contributions in the ceremony register below. |
| README disclosure | State that 0.4 has not had an outside correctness trial. |
| Release assurance | Certify the final committed batch, perform the Maintainer's AST correction **before** the gate-manifest re-anchor, and complete the release sweeps in `docs/release-process.md`. |

**Archived alongside 0.4:** `stewardship-and-reuse`.
**After 0.4:** The draft strategy `dev/strategy/2026-10-19-codex-cairn-and-assai.md`.

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

### Re-anchor the gate manifest and AST baseline — at the 0.4 cut

This is **one Maintainer-only batch**, not a request for agents to repair the
fixtures. Follow `bootstrap/AST_BASELINE_RUNBOOK.md` and
`bootstrap/REANCHOR_RUNBOOK.md`. The AST correction writes frozen fixture
bytes, so it precedes the gate-manifest ceremony. Derive actual changed files,
symbols and collected node IDs from the final committed tree; old counts are
receipts, not acceptance pins. A green `test_gate_manifest.py` does not compare
the committed manifest and does not discharge this obligation.

**Waiting on Maintainer**: run the gate-manifest re-anchor

| Contribution | What the combined ceremony still must cover | Evidence/owner |
|---|---|---|
| Portable-sweep/scanner work and active-surfacing fix (Sep 2026) | Existing frozen executable/test changes. | `portable-sweeps-cannot-run`, `scanner-claim-scope` archived plans. |
| Adopter-path consolidation and Oct 17 issue repairs | Onboarding helper/test changes, dropped and added nodes, and later InitLock/claim-check/evolution/integrity additions. | `adopter-path-consolidation` archive verification; repair commits after `4edd7778`. |
| Verification practice | Newly frozen `bootstrap/tests/test_review_and_verification_rules_ship.py`; its final bytes are superseded by the review-stance record below. | `verification-practice`, then `review-stance-and-lenses`. |
| Maintainer attention | Frozen `bootstrap/tests/test_replacement_tools.py` and its five added maintainer-view nodes. | `maintainer-attention` archive; `72254d0e`. |
| Neutrality and upgrade slots | Sixteen frozen-file edits, new neutrality/integrity nodes, phase-mutable intent/launcher changes, and the sensitive verifier change. No engine-symbol delta from that plan. | `neutrality-and-upgrade-slots` archive, final bytes recorded at `1793f07e`. |
| Review stance and lenses | Deleted test_onboarding_review_tiers.py and its five pinned nodes; three newly frozen tests; cascade-mutable config comments plus frozen preset/scope-test edits. | `review-stance-and-lenses` archive; reviewed repair `6fd6687f`; final blob table below. |
| Board as basis | Newly frozen `bootstrap/tests/test_board_json_contract.py` and `bootstrap/tests/fixtures/board_json_v1_baseline.json`; 25 new nodes, none dropped. | `board-as-basis` archive verification. |
| .gitignore seed guard | Frozen security-leaf/skills-upgrade tests; phase-mutable intent tests; CHANGED main, seed_gitignore, _cmd_adopt_module, cmd_upgrade and create_dev_tree. | `dev/reviews/2026-10-18-code-review-gitignore-seed-guard.md`, GS-CR5; `b8a402c6` through `3ba6f230`. |
| Model mapping on every install path | Six changed existing frozen files, new model-selection/seed/security/upgrade tests, the deliberately dropped comment-placeholder test; CHANGED engine functions, five NEW functions, and REKEYED _commit_lock_and_caches. | `model-mapping-install-path` archive and reviewed commit `1b609e5c`. |
| Repository rename | Frozen `bootstrap/tests/test_lockfile_provenance.py` URL assertion; no node or engine-symbol change. | Rename commit `72248e15`. |
| Independent scientific check | Newly frozen `bootstrap/tests/test_scientific_check_guidance_ships.py`; its single node, no engine-symbol change. | `independent-scientific-check` archive; last test edit `02adb81f`. |
| Agreement removal | Nine changed existing frozen files, the eight-case retirement test, and revised stance test; assignment `_CORE_MAPPINGS` changed, no top-level engine function changed. | `remove-collaboration-agreement` archive and reviewed commit `5b7848c5`; final stance-test blob below supersedes its predecessor. |
| Stewardship and reuse | Newly frozen `bootstrap/tests/test_stewardship_rules_ship.py` (blob `ae4aaa79e51ae6992f234aa86320b1370baf7abe`, 1 node); no engine-symbol or manifest change. | `stewardship-and-reuse` archive; reviewed commit `1e4e979b`. |

Final review-stance test receipts at `6fd6687f` (all three paths are under
`bootstrap/tests/`; later authorized edits must replace their receipt):

| File | Blob | Nodes at that commit |
|---|---|---|
| test_review_stance_in_shipped_files.py | `0064d10e1e2059e054928ce392022648194768e8` | 469 |
| test_review_sweep_ships.py | `fa71104f443d3181eaf9bf710ae43e7b2b3eae51` | 192 |
| test_review_and_verification_rules_ship.py | `5bb130d370259096d57b3c06cce0addc27830279` | 68 |

**Joined 2026-10-20** at the archive of
`dev/plans/archive/remove-collaboration-agreement.md`. At code-reviewed
commit `5b7848c5cea68e7d5afc49c3f6781fb592cb8b6c`, the final blob of
`bootstrap/tests/test_review_stance_in_shipped_files.py` is
`f51bf7eddde9ba77b04dd75f96dba7d032d3459c`. It replaces the
`0064d10e1e2059e054928ce392022648194768e8` review-stance receipt
above **for that file only**. The nine frozen-file changes, eight new
retirement-test cases and one assignment change are recorded in the
archived plan. Derive the ceremony's full set from the final tree; this
paragraph does not re-anchor it. The accepted Decision authorized the join:

> "Please scribe my acceptance as recommended."

**Joined 2026-10-20** at the archive of
`dev/plans/archive/model-mapping-install-path.md`. At code-reviewed
commit `1b609e5c03e18f7e156a33020f29f271d274d6d8`, the six existing
frozen files changed are:
`templates/modules/team-gated/check_model_selection.py`,
`templates/modules/team-gated/model_selection_mapping_stub.yml`,
`templates/modules/team-gated/model-selection.md`,
`bootstrap/tests/test_model_selection_stub.py`,
`bootstrap/tests/test_onboarding_seed_roster.py`, and
`bootstrap/tests/test_upgrade_module_additions.py`.
Engine functions changed: `main`, `_cmd_adopt_module`, `cmd_upgrade`,
`seed_gitignore`, `capture_model_selection_mapping`, `write_install_lockfile`,
`_cmd_init_lock`, `_cmd_finalize_lockfile`, `read_lockfile`, and
`_apply_upgrade` (digest updated from its earlier changed state).
Five new engine functions: `_mapping_is_unfilled`, `_read_regular_bytes`,
`_stage_exclusive`, `_write_by_replacing`, and `model_selection_notice_lines`.
One re-keyed known-new function: `_commit_lock_and_caches`.
Dropped pinned test: `TestFidelityCheck::test_fill_me_in_comment_fails`
(replaced by `TestCommentsAreNotPlaceholders`).
The accepted Decision authorized the join:

> "Yes, fold them into the plan"

The Maintainer's ceremony runs in this strict order: **the AST correction
first, then the gate-manifest re-anchor once.**

**Joined 2026-10-20** at the archive of
`dev/plans/archive/stewardship-and-reuse.md`. At code-reviewed commit
`1e4e979b9f3f10136c3a1953333f9947ead41c06`, the newly frozen test file is
`bootstrap/tests/test_stewardship_rules_ship.py` (blob
`ae4aaa79e51ae6992f234aa86320b1370baf7abe`, 1 node). No engine symbols,
contracts, or public manifests changed. The Maintainer authorized the join:

> "Okay, can you finish up both the plans, include stewardship-and-reuse?"

The older adopt-module/slot-empty AST debt was re-anchored at `b82b56d0`;
remaining symbol changes come from later repairs and the live plans. The old
known-new fixture's stale Import keys are bookkeeping for the same supervised
correction, not a separate agent repair. Sensitive-path/differential-oracle
checks cover changed engine files and `bootstrap/verify_integrity.py`.

Each contributing record carries its own exact file/node list and authority.
The authorizations that joined this batch, preserved verbatim:

> "If we don't need to re-anchor now, let's not. We've got a couple of big
> new features coming, one of which will be a better automation."

> "Accept Revision 2 as written. Defer the install-report fix (F8) to the
> board. No second review round; External floor waived."

> "Accept A, B, C and D as revised, with every recommended answer, including
> B’s scope cut and D’s scope delta."

> "accept both as descried"

> "I accept all five of your recommendations. Accept as recommended"

> "accept as answered"

> "Fold into this plan (Recommended)"

> "Yes, fix the .gitignore points"

> "Yes, fold them into the plan"

> "Please scribe my acceptance as recommended."

The cut-time instruction in Release path supersedes the older instruction
"One combined ceremony later" after the model-mapping archive. Stewardship's
new test belongs to a later batch unless the Maintainer changes the cut line.

### Other queued work (reviewed Oct 2026)

* **Make re-pinning usable.** Promote
  `dev/strategy/2026-08-28-claude-repin-revitalization.md` to a reviewed proposal
  before building `repin`. Until then corrections remain manual. A called
  outside read is the Maintainer's choice, not a standing requirement.
* **F8: make the post-install report match the selected profile.** A minimal
  install is asked to fill slots for modules it does not install. Classify
  obligations by the accepted profile; this touches the scaffold engine and
  needs its own proposal and Security Review. Deferred from
  `adopter-path-consolidation` Revision 2, on:

  > "Accept Revision 2 as written. Defer the install-report fix (F8) to the
  > board. No second review round; External floor waived."

* **Name upgrade-added slots (#8, engine half).** The integrity command's
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
