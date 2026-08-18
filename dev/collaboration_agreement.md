
# Collaboration agreement — Cairn

This is the **working agreement** for Cairn's human + AI
development team. It is short by design: a handful of norms the
team commits to, which the rest of the `dev/` tree then operates.
Amending it is itself a proposal.

## The team

Cairn is built by the **Human Maintainer** and one or
more **AI agents**. The Maintainer holds the project's direction,
its priorities, and final decision authority. Agents propose,
review, implement, and advise; they do not decide.

<!-- cairn:slot team-roster -->
* **Human Maintainer — Anthony Kendall** (MSU Hydrogeology). Holds
  product direction, priorities, and final Decision authority. The sole
  human contributor (the human-team axis is `solo`).
* **Agent contributors — a concurrent, multi-type roster.** More than
  one agent *type* works the tree, which is what makes Dual-Review's
  External tier structurally meaningful here: External review is a read
  from a *different* agent type than the author, not merely a
  fresh-session same-type pass. Agents propose, review, implement, and
  advise; they do not decide. Specific agent types and models are named
  in the deliberation record (each Review / Response names its reviewer
  for attribution) and mapped to capability tiers in
  `dev/.cairn/model-selection-mapping.yml` — not pinned in this
  vendor-neutral agreement, so the roster can evolve without amending
  it.

Refreshed when the team changes.
<!-- cairn:end team-roster -->

## The norms

* **Substantive change is deliberated.** A change worth a second
  opinion goes through a proposal — it is not committed because
  its author is confident. The lifecycle is in
  `proposals/_template.md`.
* **Review is honest.** A reviewer improves a change and, at the
  External tier, makes it prove it should land — reporting a real
  problem, and reporting honestly when there is none. Confidence
  proves itself.
* **The record is durable and append-only.** Deliberation is
  committed to `dev/`; a prior section is never rewritten, only
  revised by an appended one.
* **The Maintainer decides — and the list is finite.** Acceptance,
  rejection, and supersession are the Maintainer's call, as are:
  opening a new scope, overruling a reviewer or a drafting author,
  any ceremony where an agent must not bless its own verifier,
  pushing, and direction-setting about what the project is for.
  **Everything else is the agent's own call and escalating it is a
  defect, not caution** — dispositioning a review round, sequencing
  work, folding a correction, archiving an artifact whose
  preconditions are met, and choosing what to pick up next. An agent
  unsure whether something is on the Maintainer's list decides, acts,
  and records what it decided; the record is what makes the call
  reviewable, not a prior request for permission. This delegates
  judgment inside accepted scope and standing direction; it does not
  waive an approval, credential, Decision, or ceremony that another
  governing rule expressly reserves to the Maintainer.
* **Roles are named.** An agent names its role before substantive
  work (see `agent_collaboration.md`); guessing wrong wastes a
  turn.
* **Coordination is through artifacts.** The team coordinates by
  reading and updating the `dev/` tree, not through side channels
  that leave no durable record.

## Monitoring the review allocation

Cairn's default review allocation — an External proposal review that settles
a complete contract, followed by a fresh-context **Internal** plan review,
with External or Security Code review reserved for explicit escalation — is
**already the default now**, adopted at the Maintainer's direction in the
*Maintainer-directed contract revision* of
[`dev/plans/archive/review-efficient-lifecycle.md`](plans/archive/review-efficient-lifecycle.md)
(2026-08-11). `tools/lifecycle.py` ships **monitoring-evidence** machinery
(`pilot-report` derives and prints; `pilot-record` is the ledger's only
writer) that watches that default after the fact, over a bounded window: six
distinct plan stems reaching `ready-to-archive`, or 60 calendar days from
activation, whichever comes first. **This is not a permission gate** — the
allocation above needs no monitoring window to be in force, and no reader or
writer of this evidence may treat an inactive window as the policy being
off. `promote` is a retired token; the only Decision left at the boundary is
`retain | revise | retire`.

**Pause conditions.** One high-severity finding that escaped review because
of the allocation (a defect the removed External round would plausibly have
caught) pauses the monitoring window immediately; two lower-severity
examples do the same. Record a pause — `pilot-record --kind pause-set
--severity high|low ...` — and clear it explicitly with `pause-cleared` once
resolved. A recorded escaped finding that meets a threshold with no matching
pause active is itself surfaced as incomplete, so a pause can't sit
unrecorded.

**Reading the report.** `python tools/lifecycle.py pilot-report` derives its
output from the append-only ledger (`dev/measurement/pilot-events.md`) and
writes nothing itself. Exit `0` is a complete report; exit `3` is
**incomplete**, naming each missing dependency by name; exit `1` is a
refusal (a malformed or unreadable record — a data problem, never a policy
signal). A complete report lists every counted plan stem (date, source
artifact, commit, assurance path), splits them into **eligible**
(`standard`) and **ineligible / outside the sample** (anything else), and —
whenever the sample holds an ineligible stem — prints that the accepted
parent proposal ("high-assurance work … remains ineligible and does not
fill the sample") and the 2026-08-11 revision ("standard and high-assurance
proposals may both receive `READY`") disagree about whose plans should fill
the six. **That tension is printed, not resolved** — settling it, if it
ever needs settling, is the Maintainer's call, not an inference the report
is allowed to make. The report closes with the window's summed measures
(review-input bytes, transitions removed, escaped findings by severity,
Maintainer prompts) and, once the boundary is reached, a line naming the
trigger and stating that the Maintainer's Decision is due.

<!-- cairn:slot monitoring-status -->
**Current status** (verified 2026-08-18): **a monitoring window is open.** It was
opened by a data-only commit at the Maintainer's explicit instruction, after the
Boundary B2 verification it measures.

`python tools/lifecycle.py pilot-report` reports `complete` (exit 0):
`counted plan stems: 0 / 6`, `pauses: none active`, all measures zero, and the
window running **2026-08-18 .. 2026-10-16** (60 calendar days, both ends
inclusive). The activation date is *derived* — it is the author date of the
commit that first introduced the activation record's exact bytes, so the record
cannot move its own start — and the machinery it measures is bound to the
Boundary B2 evidence section, which is read at that commit and must genuinely
attest the named commit or activation refuses.

An open window measures the allocation; it does not authorize it. The allocation
has been in force since 2026-08-11 regardless, and neither an open nor a closed
window may be read as the policy being on or off. Refresh this note whenever a
pause is set or cleared, a stem is counted, or the boundary is reached.
<!-- cairn:end monitoring-status -->

**The Decision at the boundary (fence M6 — the Maintainer's; describing it
here is not taking it).** At the boundary the Maintainer reads the report
above and chooses one of three dispositions:

* **`retain`** — the allocation stays exactly as it is: a no-op over an
  already-distributed policy, no second distribution change.
* **`revise`** — the allocation continues in a changed shape. Executes
  Chunk P7 against the evidence already gathered, under P7's own
  changed-path, Boundary-B / Code-review, and ceremony classification: a
  fresh Boundary B and independent Code review if it touches governed
  bytes, a fresh Maintainer ceremony if it touches a frozen path.
* **`retire`** — the allocation is withdrawn. Same P7 execution and
  evidence requirements as `revise`; the outcome differs, not the process
  that reaches it.

## Amending this agreement

This agreement changes only through the proposal lifecycle — the
same discipline it asks of every other substantive change. A
proposal to amend it is reviewed and decided like any other.

**Optional: a signature log.** A team that wants "we agreed to these
norms" to be *auditable* rather than asserted can add a signature ritual —
opt-in, not a default (a solo project needs none):

* **Signature log.** Each participant signs the specific version they
  agreed to, with a short substantive sign-off comment — not just a name.
* **Re-signature on amendment.** Every accepted amendment re-opens the log;
  participants re-sign the new version, so a signature always attests the
  *current* text, never a superseded one.
* **Revision history.** Each amendment row ties the change to its
  triggering proposal / Decision.
* **Decision-time signature.** The Maintainer's Decision *is* the
  acceptance point; the amendment is in force from that row, and the log
  records the date it took effect.

This makes the agreement's authority traceable to who signed what, when —
the agreement analogue of the durable-record discipline Cairn already
prizes. Adopt it when the team is large enough that "everyone agreed" is
worth proving; skip it otherwise.
