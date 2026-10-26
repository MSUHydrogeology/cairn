# Adding a second (or third) agent type to your deployment

This doc walks the steps for adding another AI agent type to your
Cairn deployment. A second type is useful when the Maintainer wants
more distance on a piece of work: a different model has different
blind spots. No review requires one. For `collaborative-team` and
`high-rigor-legacy` profiles this is day-one work; for
`solo-greenfield` it is optional, because fresh sessions of your one
agent already do every review.

## Prerequisites

* A Cairn deployment past the first proposal-archive cycle (the
  apparatus has earned its keep; multi-agent is the next investment).
* A second AI agent type available to the team (a different tool, or
  a clearly different model from the first). Do not follow this doc
  for an agent you only plan to add; it applies once the agent is here.
* The team-roster slot in `dev/agent_collaboration.md` filled
  with the existing agent(s) so the new addition has a place to
  attach.

## Step 1 -- update the team-roster slot

Add the new agent's identifier to
`dev/agent_collaboration.md`'s `<!-- cairn:slot team-roster
-->` block. Use the same form your team uses for the existing agents
(tool and model name; the form matters less than being consistent).

Example (collaborative-team profile):

```markdown
<!-- cairn:slot team-roster -->
* <Maintainer name> (Maintainer)
* <Agent A: tool and model> -- author + reviewer
* <Agent B: tool and model> -- reviewer   # newly added
<!-- cairn:end team-roster -->
```

Commit the roster edit.

## Step 2 -- set up the agent's `Co-Authored-By:` trailer

Each agent commits with a trailer naming itself, so the commit log
shows who wrote what. The trailer is a pattern, so a model upgrade
never needs an edit here:

```
Co-Authored-By: <Agent Display Name> <noreply@<vendor-domain>>
```

Fill `<Agent Display Name>` with the model the agent is running now,
as its tool reports it. Configure the trailer in the agent's
commit template; how you do that depends on the tool. The trailer is
for people reading the log.

## Step 3 -- note how capable each agent is (optional)

No review requires a particular agent type. If you want a rough guide
for which agent takes which kind of work, note each agent's
capability in the roster using your own labels (high, medium or low
capability), as `doctrine/roles.md` in Cairn's
published doctrine describes. The labels guide you. They do not bind anyone, and the
Maintainer decides.

## Step 4 -- try one called read on a trivial proposal

Open a one-line proposal (for example a CHANGELOG note) and have the
**new** agent review it. You, the Maintainer, ask for this one read
and name the proposal; that is what makes it a read you called. The
first review by a second agent type is worth doing because it shows
how a called read goes in your team. One cycle of "the new agent found
nothing" or "the new agent caught something the author missed" sets
expectations.

Commit the review.

## Step 5 -- coordinate work-intents going forward

With two or more agents writing to the tree, the work-intent
mechanism (from the `coordination-tiers` module) starts to pay off.
Each agent claims the files it will edit:

```bash
python tools/intent.py claim --files <paths> --action "<short summary>"
```

If both agents try to edit the same file, the second sees the first's
claim and coordinates instead of colliding. The claims are recorded in
`dev/intents.jsonl`.

Release a claim by hand with `python tools/intent.py release <id>`, or
turn on the post-commit hook, which is opt-in: run
`python tools/intent.py install-hook` once, and each commit then
releases your claims on the paths it touched.

## Where to next

* If you haven't yet, walk `dev/modules/onboarding/dev-tour.md`
  together so the new agent gets the same dev-tree orientation the
  rest of the team has.
