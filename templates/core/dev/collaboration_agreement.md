<!-- claim-check-allow: dev/measurement/pilot-activation.md -->

# Collaboration agreement — {{project_name}}

This is the **working agreement** for {{project_name}}'s human + AI
development team. It is short by design: a handful of norms the
team commits to, which the rest of the `dev/` tree then operates.
Amending it is itself a proposal.

## The team

{{project_name}} is built by the **Human Maintainer** and one or
more **AI agents**. The Maintainer holds the project's direction,
its priorities, and final decision authority. Agents propose,
review, implement, and advise; they do not decide.

<!-- cairn:slot team-roster -->
(The bootstrap records the team here: the maintainer; the human
contributors and their roles; the agents and their types.
Refreshed when the team changes.)
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
* **The Maintainer decides.** Acceptance, rejection, and
  supersession are the Maintainer's call. An agent unsure whether
  something is a decision surfaces it rather than assuming.
* **Roles are named.** An agent names its role before substantive
  work (see `agent_collaboration.md`); guessing wrong wastes a
  turn.
* **Coordination is through artifacts.** The team coordinates by
  reading and updating the `dev/` tree, not through side channels
  that leave no durable record.

## Monitoring the review allocation

Cairn's default review allocation — an External proposal review that
settles a complete contract, followed by a fresh-context **Internal** plan
review, with External or Security Code review reserved for explicit
escalation — is this project's default too. `tools/lifecycle.py` ships
**monitoring-evidence** machinery (`pilot-report` derives and prints;
`pilot-record` is the ledger's only writer) for watching that default over
a bounded window, whenever this project wants the evidence: six distinct
plan stems reaching `ready-to-archive`, or 60 calendar days from
activation, whichever comes first. **This is not a permission gate** — the
allocation above is in force with or without an open monitoring window, and
no reader or writer of this evidence may treat an inactive window as the
policy being off. `promote` is not one of the outcomes; the only Decision
at the boundary is `retain | revise | retire`.

**Pause conditions.** One high-severity finding that escaped review because
of the allocation (a defect a heavier round would plausibly have caught)
pauses an open monitoring window immediately; two lower-severity examples
do the same. Record a pause — `pilot-record --kind pause-set --severity
high|low ...` — and clear it explicitly with `pause-cleared` once resolved.
A recorded escaped finding that meets a threshold with no matching pause
active is itself surfaced as incomplete, so a pause can't sit unrecorded.

**Reading the report.** `python tools/lifecycle.py pilot-report` derives
its output from the append-only ledger (`dev/measurement/pilot-events.md`)
and writes nothing itself. Exit `0` is a complete report; exit `3` is
**incomplete**, naming each missing dependency by name (most commonly: no
activation record yet, meaning no window has opened — never that the
allocation is off); exit `1` is a refusal (a malformed or unreadable
record — a data problem, never a policy signal). A complete report lists
every counted plan stem (date, source artifact, commit, assurance path),
splits them into **eligible** (`standard`) and **ineligible / outside the
sample** (anything else) — printing, whenever the sample holds an
ineligible stem, which of this project's own accepted contracts governs
whether such a stem should fill the quota — and closes with the window's
summed measures (review-input bytes, transitions removed, escaped findings
by severity, Maintainer prompts) and, once the boundary is reached, a line
naming the trigger and stating that the Maintainer's Decision is due.

<!-- cairn:slot monitoring-status -->
(State whether this project has ever opened a monitoring window on its
review allocation — i.e. whether `dev/measurement/pilot-activation.md`
exists — and if so, summarize the latest `python tools/lifecycle.py
pilot-report`: counted stems, active pauses, and whether the boundary has
been reached. If no window has been opened, mark `N/A: no monitoring
window opened` — this does not mean the review allocation above is
inactive, only that it has not yet been measured. Refresh this note
whenever the report's status changes. An unfilled slot is a review
finding.)
<!-- cairn:end monitoring-status -->

**The Decision at the boundary (the Maintainer's; describing it here is
not taking it).** At the boundary the Maintainer reads the report above
and chooses one of three dispositions:

* **`retain`** — the allocation stays exactly as it is: a no-op over an
  already-distributed policy, no second distribution change.
* **`revise`** — the allocation continues in a changed shape, executed
  against the evidence already gathered and this project's own
  changed-path, Boundary-B / Code-review, and ceremony classification: a
  fresh Boundary B and independent Code review if it touches governed
  bytes, a fresh Maintainer ceremony if it touches a frozen path.
* **`retire`** — the allocation is withdrawn. Same execution and evidence
  requirements as `revise`; the outcome differs, not the process that
  reaches it.

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
