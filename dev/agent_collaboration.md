<!-- cairn-internal-ref-allow: doctrine/ reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Agent collaboration — Cairn

This file is the **process doctrine** for Cairn's human
+ AI team: the role roster, the review loop, and the coordination
mechanics. `AGENTS.md` carries the operational rules and points
here for the deeper *why*; the working norms are in
`collaboration_agreement.md`. The split between this file and
`AGENTS.md` follows the **doc-governance** routing rule
(`doctrine/doc-governance.md`): deliberation- and decision-process
doctrine lives here; build + operate-safely rules live in
`AGENTS.md`; each rule has one canonical home and the other file
only points.

**Where `doctrine/` references resolve.** A reference to a
`doctrine/<name>.md` file (here and across the `dev/` tree) points to
**Cairn's published methodology doctrine** — the repository you adopted
from — **not a file in your own tree**. The bootstrap installs your
`dev/` tree and the modules you selected, *not* Cairn's `doctrine/`
directory; the doctrine is the shared methodology you consult in the
Cairn repository (or its docs). Such a reference is a citation, never a
broken local link.

## Team roles

A **role** is a frame — a stance and a kind of output — not a
person. One agent fills several roles across a session; the role
is named before substantive work, and switching roles is explicit.

* **Human Maintainer** — holds product direction, priorities, and
  final Decision authority. Not interchangeable.
* **Strategy** — surveys the landscape, frames problems, drafts
  proposals.
* **Implementation** — carries an accepted proposal through its
  plan: the code, the tests, the docs.
* **Internal Reviewer** — the constructive second read.
* **External Reviewer** — the independent, make-it-prove-itself
  read.

<!-- cairn:slot role-roster-additions -->
Cairn's profile selects two roles beyond the base roster:

* **User Agent** (`issue-capture`) — exercises Cairn from an
  adopter's seat (running the bootstrap, the lifecycle, the tools)
  and **captures friction as issues** rather than fixing it inline
  mid-session, unless the fix is a genuinely one-line, on-path one.
  Bug / Gap / Friction / Wish are filed to GitHub Issues
  (`.github/ISSUE_TEMPLATE/`); when an issue graduates into a
  proposal or `PLANNING.md` entry the link is carried **both ways**
  (the durable artifact cites the issue; the closing comment names
  the durable home).
* **Security Review** (`security-review`) — a focused-mode pass over
  the surfaces where untrusted input meets the system (the scaffold /
  merge engine parsing module + profile files, path handling, YAML
  loading, subprocess). Not a standing implementation role; invoked
  on a recorded cadence and whenever a change adds, moves, or widens
  a trust boundary. Carries a **high-capability floor**. The
  trust-boundary checklist and injection-review procedure are in
  `dev/modules/security-review.md`; Cairn's own four-layer
  instruction-supply-chain controls (provenance, executable
  hardening, content scanning, doctrine) are named there too.

Both are **frames**, not people: any capable agent fills them, named
before the work. The **capability floor by role and risk** (below)
maps these roles onto Cairn's tier labels via
`dev/.cairn/model-selection-mapping.yml`.
<!-- cairn:end role-roster-additions -->

**The AI surface is bimodal.** The roles above are filled by
**agent-side AI** — a model acting as a named participant, with
lifecycle presence, attributed reviews, and decision rights by role.
Distinguish it from **inline-tier AI** — the editing tooling
(autocomplete, inline assist) a human invokes *while* hand-authoring.
Inline-tier AI carries no role, no attribution, and no decision rights;
its output belongs to the human author and is reviewed as theirs. Naming
the distinction keeps "an AI touched this" from being mistaken for "an
agent reviewed this."

## Collaboration stance

The team's agents act as **collaborative skeptics** — respectful and
aligned on the mission, but willing to challenge each other's
assumptions. Agreement is not the goal; a better-reasoned change is.
The working habits (the deeper *why* is in
`doctrine/collaboration-stance.md`):

* steelman the other agent's position before critiquing it;
* separate taste, evidence, inference, and uncertainty;
* prefer specific concerns over broad disagreement;
* ask "what would change your mind?";
* treat disagreement as a way to improve the change, not to win it;
* the Human Maintainer's goals are the final arbiter.

## The review loop

A substantive change moves `awaiting-review -> revising ->
awaiting-review -> awaiting-decision -> accepted` (see
`proposals/_template.md`). Review has two tiers:

* **Internal review** helps a change land — a constructive second
  read. Floor: the same agent type in a fresh session —
  independence by *time*, the mental model rebuilt from the
  artifacts.
* **External review** makes a change prove it should land — an
  independent read. Floor: a different agent type, or a human —
  independence by *structure*, a genuinely different set of
  failure modes.

Code review — the implementation-side pass, before a plan archives
— has its own floor: **not the implementing agent**.

**Where the deliberative weight sits, and why the plan does not pay twice.**
The proposal is the deliberative boundary. When an **External** proposal
review has read a *complete current contract* and recorded
`Plan readiness: READY`, the derived plan takes a **fresh-context Internal**
plan review, not a second different-agent-type round — the plan is
translating decisions an independent reviewer already tested, and a routine
cross-type reread of that translation buys little for what it costs in
elapsed time and hurdles. The plan records what it is inheriting, by commit,
so the reallocation is auditable rather than assumed.

Three boundaries this does **not** move, stated because each is easy to
assume away:

* **Code review is untouched.** Its floor is still *not the implementing
  agent*, and nothing here upgrades it to External or downgrades it to none.
* **An independent read is reallocated, never removed.** A plan claiming an
  inherited basis while declaring no plan review at all is the one
  combination the record exists to make impossible.
* **Escalation stays available and is explicit.** `DISTINCT REVIEW REQUIRED`
  is the proposal reviewer's finding that consequential design remains for
  planning; a declared expansion *or* a scope reduction invalidates
  inheritance; and `recommend-and-decide` lets any reviewer ask the
  Maintainer to spend a second independent pass. What went away is the
  *automatic* second round, not the option.

The honest trade: for high-assurance work that is not security or
trust-boundary — a scientific assumption, a destructive migration, a
doctrine or lifecycle-enforcement change — the fresh-context Internal
reviewer is now the only structurally guaranteed read of the sequencing
before implementation. Security and trust-boundary work keeps its backstop
outside this allocation, in the Security Review its surface triggers on its
own. See `doctrine/dual-review.md` > "Plan-readiness inheritance" for the
record's exact shape and the seven invalidators.

Every first-pass review — Internal or External — works through the
shared **review sweep** (a generic, change-agnostic lens roster) and
ends with a **two-part coverage line** (Covered, with falsifiable
citations + Not-covered / low-confidence) and an explicit
**second-round recommendation**. Whether to spend a second
structurally-independent (cross-type) pass is then the **Maintainer's
call**, informed by that recommendation — never an automatic default,
and never a downgrade of a tier the lifecycle already declared
`required` (see `doctrine/dual-review.md` > "Review expectations — the
clean-pass trap" and "Recommend-and-decide").

**The clean pass has a mirror: the scope-reduction trap.** Narrowing is
the path of least resistance in review — it costs the reviewer nothing,
reads as prudence, and can never be shown wrong, because the wider
version is never built. Treat a proposed reduction with the same
skepticism as a clean pass. A reviewer recommending one states **what is
lost** and **why the narrower change still reaches the cause**; "this is
too large" is not a finding. An author who resolves an *underspecified*
finding by removing the work says why specifying it was rejected.

Whether a narrowing is a reduction at all is judged on **outcome**,
against the baseline artifact's own commitments — the scope *as opened*
before a Decision, *as accepted* after it, never a summary of purpose
written afterwards by whoever is doing the narrowing. If every baseline
outcome is still delivered, nothing is owed; a lighter mechanism that
still delivers is what restraint asks for. If one is partly or wholly
lost, it takes a `**Scope delta**` declaration, one grouped
scope-remainder record per source artifact, and the **Maintainer's**
explicit allowance — neither author nor reviewer may concede a baseline
outcome. A stronger outcome proposed *only during review* was never in
the baseline, so declining it is not a reduction and owes no record
(see `doctrine/dual-review.md` > "Review expectations — the
scope-reduction trap").

A **Decision-support Round-2 review** is a Review section
appended *after* the author's Response and Revised proposal; it
feeds the Maintainer's Decision rather than triggering another
revision cycle (see `doctrine/dual-review.md` > "Decision-support
Round-2 review"). The Maintainer may close a mid-flight
**procedural gap** via an inline Decision on the live artifact,
subject to the three-criterion gate in `doctrine/lifecycle.md` >
"Procedural-gap inline Decisions".

Reviews are **asynchronous and commit-mediated**: a review is a
dated, attributed section appended to the artifact and committed.
No agent writes or commits a review attributed to another agent —
the named reviewer commits their own findings, or the maintainer
does.

**Capability floor by role and risk.** Each role has a minimum
capability floor (see `doctrine/roles.md` > "Capability floors").
At low complexity the floor is implicit; if this project sits at
moderate or complex on the Complexity axis, the
`model-selection` module is installed and the adopter-local
tier-to-model mapping is published in the case-studies surface
(or an adopter-local config) — never in core doctrine.

## Surfacing judgment calls to the Maintainer

Work usually divides into a large mechanical part and a few
**judgment calls** that need the Maintainer's direction. Surface those
as a structured kickoff rather than deciding silently: finish the
mechanical ~80% first and queue the calls; surface the queue in one
message *before* committing; give **3 options + a recommended pick +
plain rationale**, naming what each changes on disk; then fold the
dispositions into one commit with the work. Chat-mode preferences are
*input* that shapes a draft, not a Decision (see `doctrine/lifecycle.md`
> "Chat preferences are not a lifecycle Decision" and "Surfacing
judgment calls to the Maintainer").

**Lead with the domain, not the architecture.** When the Maintainer is
in a domain-expert frame, frame each call by *what it changes for the
user or the science*, not by the internal structure — the architecture
is supporting detail, not the headline. "This unblocks the analysis the
user is waiting on" lands; "this lets the internal contract surface
compose additively" does not, even when both describe the same choice.
Surface the decision in the domain's terms; reach for the implementation
only when the Maintainer asks how.

## Coordination

The team coordinates **stigmergically** — through the persistent
`dev/` tree, not by message-passing. The durable record is the
source of truth, and it survives context loss and contributor
handoff.

**Reading that record has an order: board, row, artifact.** A tree of
committed files is durable but not summarizable by inspection, and the
failure it invites is reading everything under `dev/` on every entry.
When the lifecycle checker/planner is installed, `python
tools/lifecycle_planner.py board --compact` derives one row per active
artifact — kind, artifact, status, owner role, active work-intent, review
obligation, evidence, what blocks it, and whether the row is still valid.
**Run the board, choose the row you need, then read that artifact and the
evidence it cites.** Only the third step is expensive, and it is now
targeted.

The board is a *derived view*, and it says so in its own footer: the
artifact is authoritative. A row that looks wrong is a reason to open the
artifact, not to trust the row — and the view's header names the `HEAD` it
was derived from, plus whether the lifecycle files on disk differ from it,
so a stale read is visible rather than silent. It mutates nothing.

**Model-agnostic by construction.** Because the coordination
channel is git-committed files — not a live vendor API — the
method depends on no specific AI tool. This project can run
several agent types at once, swap one vendor for another, or move
to a local open-weights model, and the `dev/` tree is unchanged:
the orchestration *is* the filesystem and git, which every tool
already speaks. The methodology outlives any single model or
vendor, and the project is never locked to the tool it started
with.

The baseline coordination discipline — always on — guards the
shared surfaces:

* **Shared communication files** (`PLANNING.md`, `NEXT_SESSION.md`,
  `agent_collaboration.md`, and the changelog) are edited only at
  defined serialization points, and reference proposals / plans
  by filename stem rather than path link.
* **The staged git index is shared.** Commit with explicit paths
  (`git commit <path> ...`), never a bare `git commit`; a
  path-scoped commit cannot absorb another agent's staged work.

For concurrent teams: the shared communication files above are
the natural starting set for the **required-signal-read** mode of
the work-intent protocol (`doctrine/coordination.md` > "Required
signal+read for coordination-surface files"). The team extends
the set as additional coordination-surface files emerge. The
*broader* Tier-2 work-intent obligation a concurrent team takes on
— covering edits beyond the coordination surfaces — is **not** part
of this always-on baseline; it arrives with the work-intent
convention filled into the slot below, so a solo or sequential team
is never held to it.

<!-- cairn:slot coordination-additions -->
Cairn runs a **concurrent multi-agent** team, so the higher
coordination tiers are on. Cairn ships the tool that implements them
(`tools/intent.py`, stdlib-only); the doctrine is here, the commands
are in `dev/modules/coordination-tiers.md`.

> **Tier 2 — work intents.** Before touching a collision-prone
> surface, an agent records a **claim** in the append-only
> `dev/intents.jsonl` log — who holds which paths, with what action —
> and the claim is **auto-released** when the work lands (a
> post-commit hook closes claims whose paths the commit touched). It
> is a courtesy signal, not a lock. An empty active set means "nobody
> declared", never "nobody is working" — version-control state stays
> the source of truth.
>
> **Required scope (this concurrent team).** A `claim` is required
> before every nontrivial edit (anything touching tracked files or
> altering behavior / doctrine / tests / docs). The
> **coordination-surface** subset — the roadmap boards, the changelog,
> the handoff and collaboration-norm docs — *additionally* requires a
> `list` read before editing (signal *and* read). Trivial read-only
> checks are exempt.
>
> **Tier 3 — typed activity events (high-concurrency / domain-agent
> teams).** An append-only log of typed events (`start`, `heads_up`,
> `query`, `handoff`, `ack`, `release`) — a typed channel, not a chat
> channel. The schema carries no free-form decision field: a
> decision-bearing exchange points an event *at* the proposal or plan
> where the decision is written. Cairn does not run domain agents, so
> Tier 3 stays available but dormant.

> **Collision log.** The team keeps a tracked file
> (`dev/measurement/collision_log.md`) recording staged-index events:
> **true-staged-index** (one session's commit sweeps another's work),
> **prevented-overlap**, and **parallel-non-conflict**. Only
> `true-staged-index` counts against the protocol-failure trigger:
> more than one such event on a shared-coordination file within the
> team's rolling window re-opens the coordination-architecture
> question.
>
> **Goodnight intent-hygiene.** The full-handoff owner's goodnight
> routine **prunes** completed claim/release pairs out of the live log
> and **migrates** any `true-staged-index` events from the day's
> reflections into the collision log — once per session-day, by one
> writer.
>
> **Per-session coordination identity.** The holder identity in the
> intent log is **per-session**, derived from the harness session ID
> (the whole ID hashed, never a prefix), so sibling sessions of the
> same agent type resolve distinct identities and auto-release closes
> only the committing session's own claims. A static `$CAIRN_AGENT`
> override is an escape hatch for tests / one-offs, not a setting.

**Enable the hooks (Day-1 step).** The hooks are opt-in — the scaffold
never mutates `.git/hooks`. Run once:
`python tools/intent.py install-hook` (post-commit auto-release),
`python tools/intent.py install-precommit` (pre-commit work-intent
check), `python tools/intent.py hooks-status` (confirm). This step is
on the onboarding board.
<!-- cairn:end coordination-additions -->

## Session reflections and handoff

<!-- cairn:slot reflections -->
**Reflections.** At the goodnight routine each agent writes a short,
per-agent reflection — what it shipped, what went well, what went wrong
and the lesson it leaves — to a per-session file in an untracked
`dev/reflections/` directory. Reflections are:

* **per-agent, per-session** — each agent writes its own, and each
  *session* writes a distinct file (`<date>-<agent>-<session>.md`) so
  concurrent same-agent sessions never clobber one another. `<session>`
  resolves, in order, to: the intent identity's session token
  (`python tools/intent.py whoami --session-token`); else the raw
  harness session id; else a short random token fixed at session start.
  No agent writes or edits another's.
* **ephemeral** — reflection files are untracked and periodically
  pruned (only the tracked `dev/reflections/README.md` persists);
  durable observations migrate to doctrine or the roadmap before they
  prune.
* **a cross-agent handoff surface** — the goodnight owner reads the
  day's reflections (glob `dev/reflections/<date>-*.md`) to understand
  each agent's experience before writing the next session's plan.

A reflection is a retrospective, not a decision surface — a point that
belongs in a proposal does not live in a reflection.
<!-- cairn:end reflections -->

**The handoff format.** However reflections are set up, a session-end
handoff names four things so the next session — agent or human — can
resume cold:

* **Shipped** — what landed (commits, files, decisions).
* **Verified** — what was checked, and how (tests / commands run, with
  their results).
* **Open threads** — what is in flight, blocked, or deliberately
  deferred.
* **Recommended next step** — the single best place to resume.

## Lifecycle metrics

<!-- cairn:slot lifecycle-metrics -->
**Lifecycle metrics.** The extractor `python tools/lifecycle_metrics.py`
walks the `dev/proposals/` + `dev/plans/` corpus and emits per-proposal
metrics — review rounds, revision counts, time-to-decision. Run it to
read the team's own discipline; the output is
derived and uncommitted (`--snapshot` persists a dated CSV under
`dev/measurement/snapshots/` when a citable record is wanted). A
measured baseline is the gating artifact for any claim Cairn makes
about its own method — run the extractor before asserting one.

All per-member / per-tier reading is bound by the **Measurement
Compact** (`dev/modules/lifecycle-metrics.md`): metrics serve system
learning, not member ranking; any externally-published artifact derived
from per-member or per-tier surfaces needs an explicit Maintainer
decision first.
<!-- cairn:end lifecycle-metrics -->
