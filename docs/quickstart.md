# Try Cairn in one short sitting, with one AI agent

This page is a recipe, not a tour.  Follow it on a disposable repo
to watch one person and one AI agent take a single change through
Cairn's lifecycle, in your own terminal.  It will not teach you the
method in one sitting; [`getting-started.md`](getting-started.md) and
[`doctrine/`](../doctrine/) do that.

> **A note on the example.**  The change here is a one-line README
> tagline.  In real work that is a *trivial* change: you would make it
> and commit it with its test and one code review.  Cairn sorts changes
> into three lanes, and only the heaviest (a new feature, a contract change, a
> high-risk surface) needs a proposal.  This recipe sends the tagline
> down the full proposal path **on purpose**, so that you can see each
> record the heavy lane leaves behind.

> **How long it takes is not stated.**  It depends on how your agent is
> set up and how closely you read.  Cairn has not measured it, and a
> number nobody measured cannot be checked.

If you are evaluating Cairn for a real project, start here, then
return to the [on-ramp](../on-ramp/README.md) once you trust the
shape.

## What you need

* A POSIX shell (macOS / Linux / WSL).
* Python 3.13, the version Cairn is tested on.
* `git`.
* One AI coding agent, any that can read and write files in a folder.
  Cairn works with any such agent; the recipe uses prompts the agent
  reads, not calls Cairn makes.
* One uninterrupted sitting -- the steps are short, but do not start
  this one in the gaps between other things.

## What you will end up with

A **fresh, disposable repo** with:

* A `dev/` tree containing one proposal, with its review and
  decision, archived.
* One commit per lifecycle step (open, review, decision,
  implement-and-archive), plus the two setup commits (init, install).
* A `CHANGELOG.md > Unreleased` line for the change.
* A teardown step you can delete in one command.

You are *not* installing Cairn into a real project here.  This is a
shakedown.

The install itself is real, though: Steps 2 and 3 are the commands you
would run on a real project, with the smallest profile Cairn ships.
What makes this a shakedown is the throwaway target, the trust check
Step 1 lets you skip, and the teardown at the end.  *What to do next*
gives the real route.

## Step 1 -- clone Cairn and create a disposable target

<!-- cairn-accept: suspicious-url reason="Literal Cairn clone URL the adopter needs to copy" reviewer="Claude" date=2026-05-28 -->
```bash
# Anywhere you keep code:
git clone https://github.com/MSUHydrogeology/cairn.git cairn
cd cairn
export CAIRN="$(pwd)"   # the rest of this recipe refers to $CAIRN
```
<!-- cairn-accept-end: suspicious-url -->

> **This clone is the trust decision.** Everything below runs code from
> it.  Before you install Cairn into anything you care about, verify the
> release tag you checked out against a signing-key fingerprint you
> compared on two independent channels — the procedure is in
> `bootstrap/PROVENANCE.md` > "Verifying a release".  For this
> throwaway shakedown you can skip it; for a real project you should
> not.

```bash
# Create the disposable target repo somewhere else:
mkdir -p /tmp/cairn-quickstart && cd /tmp/cairn-quickstart
git init -q
echo "# quickstart" > README.md

# Cairn's lifecycle uses CHANGELOG.md but the scaffold does not
# create one (your real repo may already have one).  Touch a stub:
printf "# Changelog\n\n## Unreleased\n" > CHANGELOG.md

git add README.md CHANGELOG.md && git commit -q -m "init"
```

## Step 2 -- copy the `solo-greenfield` profile

The quickstart uses the smallest viable profile: one human + one
agent, new codebase, default-on modules only.  Copy the shipped
YAML literally:

```bash
cp "$CAIRN/bootstrap/profiles/solo-greenfield.yml" profile.yml
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

## Step 3 -- preview, then run the scaffold

**Preview first** (recommended -- this exits without writing
anything, so you can confirm the dimension profile and the module
roster Cairn would install):

```bash
python "$CAIRN/bootstrap/scaffold.py" \
    --config profile.yml \
    --target . \
    --summary
```

The `--summary` flag is **preview-only**: it prints the resolved
axes and the module roster, then exits without touching the target.
For the `solo-greenfield` profile you should see **6** modules listed <!-- verify: solo_greenfield_module_count -->
(the modules every install gets): `reflections`, `claim-check`,
`incident-trackers`, `documentation-plan`,
`content-security`, `security-verification`.

> **What the six axes are.** Cairn sizes the apparatus to your
> project along six axes: **age** (greenfield or legacy), **size**
> (small to large), **complexity** (simple to complex), **language**
> (one or several), **human_team** (solo to large team), and
> **agent_team** (one agent to several). `solo-greenfield` takes the
> smallest value on every axis, so it installs the least. Larger
> projects take larger values and get more modules; see
> [`dimensions/README.md`](../dimensions/README.md).

**Then install** (drop `--summary`):

```bash
python "$CAIRN/bootstrap/scaffold.py" \
    --config profile.yml \
    --target .
```

> **A note on the provenance warning.**  Because Step 1 cloned Cairn's
> tip (not a tagged release), the scaffold prints a one-line provenance
> warning suggesting `--allow-dev`.  That is **expected** for a shakedown
> from the tip and never blocks the install.  (A real adoption scaffolds
> from a tagged release, where the warning does not appear.)

The scaffold prints **its own install report**, and *that report is the
authoritative list* of every file it wrote.  Read it rather than
matching against a list here, which would go stale.  For this recipe
you only need two things:

* `AGENTS.md` -- the rules your agent reads.  `VENDOR.md` is a template
  you rename to the file your agent tool loads automatically.
* the `dev/` tree -- where the record lives: the roadmap boards, the
  `proposals/` and `plans/` templates, and one doc per installed
  module.  `dev/.cairn/` holds the lockfile and install state that
  upgrades use; you never need to read it.

`tools/`, `scripts/` and `.agents/` hold helper tools and the
`session-start` / `session-end` routines.  They install into your
target repo, not into Cairn.  Ignore them for now.

The scaffold also reports **22 unfilled block slots** -- placeholders
your agent fills in a real adoption.  See
[`bootstrap/BOOTSTRAP.md`](../bootstrap/BOOTSTRAP.md) Act II-4 for the
filling pass.  This recipe leaves them: the tagline change does not
need them, and the scaffold's "Next steps **for a real adoption**" note
is for when you install into a real project.

Commit the install (path-scoped, since the scaffold touched many
files; `CHANGELOG.md` was already committed in Step 1):

```bash
git add AGENTS.md VENDOR.md NOTICE.md .gitignore dev/ tools/ scripts/ .agents/ docs/ && \
    git commit -q -m "Install Cairn kernel + default-on modules"
```

<!-- vendor-ok-begin: editor-name list -- illustrative options for adopters; not a vendor endorsement -->
> **Tip -- open the disposable repo in your editor now.** The
> next two steps ask your agent to read `AGENTS.md` and write a
> proposal under `dev/proposals/`; you will be following along
> by reading those files as they land. A side-by-side editor
> view (VS Code, Cursor, or your editor of choice) makes the
> lifecycle visible as it happens, instead of relying on
> `cat` + `git log` between steps.
<!-- vendor-ok-end -->

## Step 4 -- the first prompt to your AI agent

> **Where the agent will write.** A proposal is a Markdown file such
> as `dev/proposals/2026-XX-XX-<slug>.md`.  Its header has the fields
> `Author`, `Status`, `Review`, `Plan review`, `Opened` and `In brief`,
> and it starts at `Status: awaiting-review`.  Below the header come
> sections such as Context, Proposal, Alternatives considered and
> Evidence / verification plan.  A review and a decision are
> appended later, in order.  The whole file is the audit trail.  See
> [`dev/proposals/_template.md`](../templates/core/dev/proposals/_template.md)
> for the full shape.  For a one-line tagline most sections need only a
> sentence.

Paste this into your agent (verbatim is fine -- the prompt is
intentionally short; Cairn's `AGENTS.md` carries the doctrine):

> Read `AGENTS.md` in this repo to learn how proposals work.  Then
> propose a one-line addition to `README.md`: a brief project tagline.
> Open the proposal as
> `dev/proposals/2026-XX-XX-<your-name>-readme-tagline.md`, copying
> the shape of `dev/proposals/_template.md`, with Status
> `awaiting-review`.  Do not implement anything yet.

Watch the agent: it should read `AGENTS.md`, write the proposal file,
and stop.  In the heavy lane the proposal comes before the code.

Commit the proposal:

```bash
git add dev/proposals/ && git commit -q -m "Open proposal: README tagline"
```

Most of this step is the agent reading.

## Step 5 -- review, decide, implement, archive

**Review.** Start a **new session** of your agent, so the reviewer is
not the one that wrote the proposal, and paste:

> You did not write the proposal in `dev/proposals/`.  Read it and
> `AGENTS.md`, then append a `## Review` section in the shape the
> template gives.  Question whether the change should happen as
> framed, name the best alternative (doing nothing counts), and say
> what would show it wrong.  Commit only the proposal file.

The reviewer writes its own review and commits it; that is one
commit.  If it finds nothing blocking, it moves the header to
`Status: awaiting-decision`.  If it finds something blocking, the
status becomes `revising` and the first agent answers in an appended
section before the Maintainer sees it.

**Decide.** You are the Maintainer.  Append a `## Decision` section to
the proposal yourself, quoting your own words, set apart, and change
the header to `Status: accepted`:

```markdown
## Decision -- <your-name> -- 2026-XX-XX

**ACCEPTED.** The Maintainer's authorization, quoted verbatim:

> "Accepted.  Add the tagline and archive the proposal in one commit."
```

Commit the decision, then ask the agent that wrote the proposal:

> The proposal is accepted.  Implement the tagline, move the proposal
> to `dev/proposals/archive/`, and add a one-line entry to
> `CHANGELOG.md > Unreleased`.  Commit the whole thing as one
> implementing-and-archiving commit.

A small accepted proposal can be implemented and archived in one
commit with no plan.  You should see the agent:

* Edit `README.md` to add the tagline.
* `git mv` the proposal into `dev/proposals/archive/`.
* Add the CHANGELOG line.
* Commit all three with a single explicit-path commit.

## Step 6 -- look at what you have

```bash
git log --oneline
ls dev/proposals/archive/
cat CHANGELOG.md
```

You should see:

* Six commits with clear lifecycle boundaries (init, install,
  proposal-open, review, decision, implement-and-archive).
* The proposal in `archive/`, frozen, with its review and decision.
* A CHANGELOG line that records what changed.

That is the lifecycle.  A larger change adds a plan, with its own
review, but the mechanics are the same.

## Step 7 -- teardown

```bash
cd .. && rm -rf /tmp/cairn-quickstart
```

The disposable repo is gone.  Cairn (in your `cairn/` clone) is
untouched.

## What you saw

* **Proposal before code.**  The first commit was a proposal, not a
  feature.
* **Each transition is its own commit.**  Open, review, decision and
  implement-and-archive each landed separately.
* **A fresh reviewer.**  A new session that did not write the proposal
  questioned it in writing before the Maintainer decided.
* **The proposal is the audit trail.**  After archiving, you can read
  the file and reconstruct *why* the change happened, not just *what*.
* **The Maintainer decides.**  The agent proposed and implemented; you
  decided, in your own quoted words.

## What you did *not* see

* **The other two lanes.**  A trivial change (a typo or one-line fix)
  takes no proposal.  A change whose shape is already settled takes one
  short change note, reviewed, then the change and its test.  When
  unsure, take the heavier lane.  See
  [`doctrine/lifecycle.md`](../doctrine/lifecycle.md).
* **Extra distance in review.**  A fresh session of the same agent is
  enough.  When you want more distance, you can ask for another model
  or a person to review a particular piece of work (see
  [`doctrine/dual-review.md`](../doctrine/dual-review.md)).
* **Plans.**  A larger accepted proposal opens a plan
  ([`dev/plans/_template.md`](../templates/core/dev/plans/_template.md))
  that sequences the work and gets its own review.  This one did not
  need it.
* **The dimensional matrix.**  The minimal profile installed only the
  default modules.  A larger project picks more (see
  [`bootstrap/profiles/`](../bootstrap/profiles/) and
  [`dimensions/`](../dimensions/)).

## What to do next

The tagline was small so the *shape* of the lifecycle would be easy
to see.  The next step is to run the same shape on a **real change**:
one that touches several files, has a review worth writing down, and
needs a plan.  That is where the apparatus pays back.

In order:

* **Pick a real project to assess** -- use the
  [Codebase Readiness Report template](../templates/codebase-readiness-report.md)
  to surface the questions before you choose a profile.  Fill it
  locally first; the template's "What to check in" section names
  the safer default check-in posture.
* **Hand the assessment to your agent** -- the
  [bootstrap-lite prompt](../bootstrap/prompts/bootstrap-lite.md) has
  the agent score the six axes and recommend a profile, so you do not
  fill in the Act I templates by hand.  It keeps the same rule as this
  recipe: you, the Maintainer, accept the result before anything is
  installed.
* **Install Cairn into the real project** -- run Steps 2 and 3
  against your own repository, with the profile the assessment points
  to, from a release tag you have verified
  (`bootstrap/PROVENANCE.md` > "Verifying a release" -- not skippable
  for a real project).  Then do the four steps the installer prints
  for a real adoption (`bootstrap/BOOTSTRAP.md` Act II-3 to II-6).
  The [on-ramp](../on-ramp/README.md) has the profile table, and what
  to do if you copied the kernel in by hand.
* **Read the doctrine** -- [`doctrine/`](../doctrine/) explains
  *why* the lifecycle works as it does.  Start with
  [`lifecycle`](../doctrine/lifecycle.md) and
  [`dual-review`](../doctrine/dual-review.md).

## Honest framing

Cairn is **slower for the first few changes**.  Its speed comes
later: fewer repeated decisions, fewer forgotten assumptions, fewer
agent collisions, and less rework after unreviewed scientific
choices.  Keep the apparatus only as heavy as your codebase and team
earn -- the profile you choose is that calibration (see the
[on-ramp](../on-ramp/README.md)).
