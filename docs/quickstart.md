# Try Cairn in 15-25 minutes with one AI agent

This page is a recipe, not a tour.  Follow it on a disposable repo
to see one human + one AI agent move a single change through Cairn's
lifecycle.  You will not learn the doctrine in 25 minutes -- that is
what [`docs/getting-started.md`](getting-started.md) and
[`doctrine/`](../doctrine/) are for.  What you *will* see: the
apparatus in motion, in your own terminal, on your own machine.

> **Why the range.**  The 15-minute floor assumes your AI agent is
> already configured and you copy the profile YAML literally.  Adding
> agent setup, reading the rendered installed files, or pausing to
> understand the lifecycle pushes you toward the 25-minute ceiling.

If you are evaluating Cairn for a real project, start here, then
return to the [on-ramp](../on-ramp/README.md) once you trust the
shape.

## What you need

* A POSIX shell (macOS / Linux / WSL).
* Python 3.10+.
* `git`.
* One AI coding agent connected to a repo of your choice -- Claude
  Code, Codex CLI, Cursor, Aider, or anything else that can read
  and write files in a working tree.  Cairn is vendor-neutral; the
  recipe uses prompts the agent reads, not API calls Cairn makes.
* About 15 minutes.

## What you will end up with

A **fresh, disposable repo** with:

* A `dev/` tree containing one proposal, an archived form of that
  proposal, and a `PLANNING.md` line.
* One commit per lifecycle step (proposal-open, decision,
  implement-and-archive), plus the two setup commits (init,
  install).
* A `CHANGELOG.md > Unreleased` line for the change.
* A teardown step you can delete in one command.

You are *not* installing Cairn into a real project here.  This is a
shakedown.

## Step 1 -- clone Cairn and create a disposable target

```bash
# Anywhere you keep code:
git clone https://github.com/MSUHydrogeology/cairn-scientist-ai-teams.git cairn
cd cairn

# Create the disposable target repo somewhere else:
mkdir -p /tmp/cairn-quickstart && cd /tmp/cairn-quickstart
git init -q
echo "# quickstart" > README.md

# Cairn's lifecycle uses CHANGELOG.md but the scaffold does not
# create one (your real repo may already have one).  Touch a stub:
printf "# Changelog\n\n## Unreleased\n" > CHANGELOG.md

git add README.md CHANGELOG.md && git commit -q -m "init"
```

Time: ~2 minutes.

## Step 2 -- copy the `solo-greenfield` profile

The quickstart uses the smallest viable profile: one human + one
agent, new codebase, default-on modules only.  Copy the shipped
YAML literally:

```bash
cp /path/to/cairn/bootstrap/profiles/solo-greenfield.yml profile.yml
```

The file looks like this -- you can read it before continuing:

```yaml
# Inline token values (mechanical substitution into installed templates).
project_name: "Quickstart"
test_command: "pytest"

# Module selection: reference the named governance preset.  Scaffold
# expands it to the default-on set + the (empty) team-gated baseline.
preset: solo-greenfield
```

The full file carries an in-file comment header listing the six-axis
dimensional profile this preset expresses (age, size, complexity,
language, human-team, agent-team) and the resulting module roster.
Other shipped profiles
([`collaborative-team.yml`](../bootstrap/profiles/collaborative-team.yml),
[`high-rigor-legacy.yml`](../bootstrap/profiles/high-rigor-legacy.yml))
follow the same shape with different presets; you can compare them
to see how axis values drive the roster.

Time: ~1 minute.

## Step 3 -- preview, then run the scaffold

**Preview first** (recommended -- this exits without writing
anything, so you can confirm the dimension profile and the module
roster Cairn would install):

```bash
python /path/to/cairn/bootstrap/scaffold.py \
    --config profile.yml \
    --target . \
    --summary
```

The `--summary` flag is **preview-only**: it prints the resolved
axes and the module roster, then exits without touching the target.
For the `solo-greenfield` profile you should see four modules
listed (the default-on floor): `lifecycle-metrics`, `reflections`,
`claim-check`, `fold-back-ledger`.

**Then install** (drop `--summary`):

```bash
python /path/to/cairn/bootstrap/scaffold.py \
    --config profile.yml \
    --target .
```

The scaffold prints what it installed.  For the `solo-greenfield`
profile you will see roughly 15--17 files across the kernel +
module + tool directories (the exact count shifts slightly across
Cairn releases):

* `AGENTS.md` -- the kernel doctrine file every agent reads.
* `VENDOR.md` -- the vendor addendum template (Cairn is vendor-
  neutral; this file holds tool-specific notes if your team wants
  them).
* `dev/README.md`, `dev/PLANNING.md`, `dev/NEXT_SESSION.md` -- the
  coordination tree.
* `dev/collaboration_agreement.md`, `dev/agent_collaboration.md`
  -- the working norms.
* `dev/proposals/_template.md`, `dev/plans/_template.md` -- the
  lifecycle templates.
* `dev/modules/lifecycle-metrics.md`, `dev/modules/reflections.md`,
  `dev/modules/claim-check.md`, `dev/modules/fold-back-ledger.md`
  -- the default-on module docs.
* `dev/upstream/fold-back-ledger.md` -- the upstream fold-back
  ledger (you can ignore this for the quickstart).
* `tools/lifecycle_metrics.py`, `scripts/claim_check.py` -- the
  default-on tool scripts.
* `dev/cairn-lock.yml` plus the `dev/.cairn/base/` snapshot -- the
  upgrade-safety anchor; you do not need to read these.

The scaffold also reports **11 unfilled block slots** -- placeholders
your agent will fill during dogfood.  See
[`bootstrap/BOOTSTRAP.md`](../bootstrap/BOOTSTRAP.md) Act II-4 for the
full filling pass.  For this quickstart we leave them; the trivial
dogfood does not need them filled.

Commit the install (path-scoped, since the scaffold touched many
files; `CHANGELOG.md` was already committed in Step 1):

```bash
git add AGENTS.md VENDOR.md dev/ tools/ scripts/ && \
    git commit -q -m "Install Cairn kernel + default-on modules"
```

Time: ~2 minutes.

## Step 4 -- the first prompt to your AI agent

Paste this into your agent (verbatim is fine -- the prompt is
intentionally short; Cairn's `AGENTS.md` carries the doctrine):

> Read `AGENTS.md` in this repo to learn how proposals work.  Then
> propose a one-line addition to `README.md`: a brief project tagline.
> Open the proposal as
> `dev/proposals/2026-XX-XX-<your-name>-readme-tagline.md`, with
> Status `proposed`.  Wait for me to review and decide before
> implementing.

Watch the agent: it should read `AGENTS.md`, write the proposal file,
and stop.  This is the **lifecycle invariant** -- propose before
code.

Commit the proposal:

```bash
git add dev/proposals/ && git commit -q -m "Open proposal: README tagline"
```

Time: ~3 minutes (most of which is the agent reading).

## Step 5 -- review, decide, implement, archive

You are the Maintainer.  Append a `## Decision` section to the
proposal yourself:

```markdown
## Decision -- <your-name> -- 2026-XX-XX

Accept.  Trivial implementation; ship + archive in one commit.
```

Commit the decision, then ask the agent:

> The proposal is accepted (trivial).  Implement the tagline,
> move the proposal to `dev/proposals/archive/`, and add a one-line
> entry to `CHANGELOG.md > Unreleased`.  Commit the whole thing as
> the implementing-and-archiving commit.

You should see the agent:

* Edit `README.md` to add the tagline.
* `git mv` the proposal into `dev/proposals/archive/`.
* Add the CHANGELOG line.
* Commit all three with a single explicit-path commit.

Time: ~5 minutes.

## Step 6 -- look at what you have

```bash
git log --oneline
ls dev/proposals/archive/
cat CHANGELOG.md
```

You should see:

* Five commits with clear lifecycle boundaries (init, install,
  proposal-open, decision, implement-and-archive).
* The proposal in `archive/`, frozen.
* A CHANGELOG line that records what changed.

That is the lifecycle.  The same shape scales to a multi-day
proposal with reviews, plans, and large refactors -- but the
mechanics are identical.

## Step 7 -- teardown

```bash
cd .. && rm -rf /tmp/cairn-quickstart
```

The disposable repo is gone.  Cairn (in your `cairn/` clone) is
untouched.

Time: ~30 seconds.

## What you saw

* **Propose before code.**  The first commit was a proposal, not a
  feature.
* **Lifecycle transitions are commits.**  Open / decide /
  implement-and-archive each landed separately.
* **The proposal is the audit trail.**  After archiving, you can
  read the file and reconstruct *why* the change happened, not just
  *what*.
* **The Maintainer decides.**  The AI agent proposed and implemented;
  you decided.  That is Cairn's human authority gate.

## What you did *not* see

* **Dual-Review.**  A second reviewer (a different agent, or a
  second human) appends an independent `## Review` before the
  Decision.  Quickstart skipped it -- the change was trivial.  On a
  non-trivial change, the review is the lifecycle's second pillar
  (see [`doctrine/dual-review.md`](../doctrine/dual-review.md)).
* **Plans.**  Multi-commit changes open a plan
  ([`dev/plans/_template.md`](../templates/core/dev/plans/_template.md))
  that sequences the work and gets its own review.  The trivial
  accept above did not need one.
* **The dimensional matrix.**  The minimal profile picked
  default-on modules only.  A larger project picks more (see
  [`bootstrap/profiles/`](../bootstrap/profiles/) and
  [`dimensions/`](../dimensions/)).

## What to do next

* **Pick a real project to assess** -- use the
  [Codebase Readiness Report template](../templates/codebase-readiness-report.md)
  to surface the questions before you pick a level.
* **Hand the assessment to your agent (one-shot)** -- use the
  [bootstrap-lite prompt](../bootstrap/prompts/bootstrap-lite.md) if
  you would rather have the agent score the six axes and recommend
  a profile than fill the Act I templates yourself by hand.
* **Pick an adoption level** -- the [on-ramp](../on-ramp/README.md)
  describes Level 0 (read the doctrine), Level 1 (hand-copy the
  kernel), and Level 2 (full bootstrap).  Most teams start at
  Level 1.
* **Read the doctrine** -- [`doctrine/`](../doctrine/) is the
  invariant core; it explains *why* the lifecycle works the way it
  does.

## Honest framing

Cairn is **slower for the first few changes**.  Its speed comes
later: fewer repeated decisions, fewer forgotten assumptions, fewer
agent collisions, and less rework after unreviewed scientific
choices.  Keep the apparatus only as heavy as your codebase and team
earn -- the [on-ramp's maturity ladder](../on-ramp/README.md) is
the self-locate aid for that calibration.
