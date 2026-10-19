# Adding a second (or third) agent type to your deployment

This doc walks the steps for staffing your Cairn deployment with
an additional AI agent type -- the move that makes a different
model architecture available when the Maintainer asks for more
distance on a piece of work. For `collaborative-team` and
`high-rigor-legacy` profiles this is day-one work; for
`solo-greenfield`, it is optional: fresh sessions of your one agent
already do every review, and a second type is there for the days you
want it.

## Prerequisites

* A Cairn deployment past the first proposal-archive cycle (the
  apparatus has earned its keep; multi-agent is the next investment).
* A second AI agent type available to the team (a different
  vendor, or a sufficiently different model architecture from the
  first; an aspirational "future second agent" is not a
  prerequisite -- this doc applies when the agent is here).
* The team-roster slot in `dev/collaboration_agreement.md` filled
  with the existing agent(s) so the new addition has a place to
  attach.

## Step 1 -- update the team-roster slot

Add the new agent's identifier to
`dev/collaboration_agreement.md`'s `<!-- cairn:slot team-roster
-->` block. Use the canonical-id form your team has chosen for
the existing agents (vendor + model name + optional capability
tier suffix; the form matters less than the consistency).

Example (collaborative-team profile):

<!-- vendor-ok-begin: the roster example shows real model names in the slot's expected format -->
```markdown
<!-- cairn:slot team-roster -->
* Anthony (Maintainer)
* Claude Opus 4.7 (1M context) -- author + reviewer
* Codex GPT-5 -- reviewer (External cross-type)   # newly added
<!-- cairn:end team-roster -->
```
<!-- vendor-ok-end -->

Commit the roster edit. The team-roster slot is the explicit
state the goodnight activation helper reads to surface the
`second-agent-type` trigger; updating it is what makes the trigger
fire on the next goodnight.

## Step 2 -- set up the agent's `Co-Authored-By:` trailer

Each agent commits with a trailer naming itself, so the commit
log is the audit trail for who wrote what. The trailer convention
is a **pattern**, not a version frozen in this doc -- each agent
stamps its own *current* model identifier, so a model bump never
requires an edit here:

```
Co-Authored-By: <Agent Display Name> <noreply@<vendor-domain>>
```

Fill `<Agent Display Name>` with the agent's current model as its
harness reports it. Stamping the running model (rather than a
pinned version) keeps every trailer accurate with no doc
maintenance, and leaves git history attributing each commit to the
model that produced it. The examples below are illustrative
snapshots -- substitute whatever model you are currently running:
* `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` <!-- vendor-ok: illustrative trailer example naming a real model -->
* `Co-Authored-By: Codex GPT-5 <noreply@openai.com>` <!-- vendor-ok: illustrative trailer example naming a real model -->
* `Co-Authored-By: Antigravity GPT-5 <noreply@google.com>` <!-- vendor-ok: illustrative trailer example naming a real model -->

Configure the trailer in the agent's commit-template (the
mechanism varies by harness; the standing convention is that the
trailer is reliable enough to tell which agent type wrote what).

## Step 3 -- record capability tier in the roster

The `capability tier` is the rough strength bucket the team
assigns to each agent for purposes of choosing who does what:

* **Frontier** -- the strongest tier; load-bearing for proposal
  review and Security Review on substantive changes.
* **Standard** -- the team's working baseline; cover plan review,
  code review and Implementation by default.
* **Light** -- structural lifts where the higher-tier agents'
  attention is over-spent (mechanical follow-ups, label-only
  edits).

Tier mapping is the team's call; the assignment lives inline in
the team-roster slot. The mapping informs (it does not bind)
which agent the goodnight owner asks for which kind of work.

## Step 4 -- smoke a cross-type read on a trivial proposal

Open a one-line proposal (e.g., a typo fix or a CHANGELOG note),
and have the **new** agent type review it. The Maintainer asks for
this one read, naming the proposal; that is what makes it a read
they called. The first cross-type review is significant for two
reasons:

1. It validates the trailer is being parsed correctly (the
   `first-cross-type-review` activation trigger fires off this
   signal).
2. It establishes the team's working pattern for a called read
   -- one cycle of "the new agent reviewed this without surfacing
   problems" or "the new agent caught something the author missed"
   calibrates expectations.

Commit the review with the new agent's trailer. The next
goodnight run of `python scripts/onboarding_activate.py` will
fire the `first-cross-type-review` trigger and surface the
follow-up onboarding task (per the active-surfacing protocol).

## Step 5 -- coordinate work-intents going forward

With two or more agents now writing the tree, the work-intent
mechanism (the `coordination-tiers` module's seed) earns its keep
from the next session. Each agent claims intent before editing
shared files:

```bash
python tools/intent.py claim --files <paths> --action "<short summary>"
```

The post-commit hook auto-releases the claim. The intent log
(`dev/intents.jsonl`) is the agent-collision-prevention surface;
when both agents try to edit the same file the second one sees
the first's claim and coordinates rather than colliding.

## Where to next

* If you haven't yet, walk `dev/modules/onboarding/dev-tour.md`
  together so the new agent gets the same dev-tree orientation the
  rest of the team has.
* When your fold-back ledger acquires its first open candidate,
  the fold-back issue template
  (*.github/ISSUE_TEMPLATE/foldback.md*) is the next
  capability to exercise -- a read from a second agent type is
  useful there whenever the Maintainer asks for one.
