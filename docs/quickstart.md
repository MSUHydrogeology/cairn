# Try Cairn in one short sitting, with one AI agent

This page is a recipe, not a tour.  You will take one small change
through Cairn's lifecycle on a throwaway project, working the way most
people work with an AI agent: **in its chat**, in the agent's own app or
in your editor.  The agent runs the commands; you make the decisions.

Every step also shows the commands, if you would rather type them
yourself in a terminal, with macOS / Linux and Windows side by side.
This page will not teach you the method in one sitting;
[`getting-started.md`](getting-started.md) and
[`doctrine/`](../doctrine/) do that.

> **A note on the example.**  The change here is a one-line README
> tagline.  In real work that is a *trivial* change: you would make it
> and commit it with its test, with no code review.  Cairn sorts changes
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

* **An AI coding agent** that can read and write files and run commands
  in a folder: in its own app, in your editor, or in a terminal.
  Cairn works with any such agent; the recipe uses prompts the agent
  reads, not calls Cairn makes.
* **Python 3.13** (the version Cairn is tested on) and **git**,
  installed on your computer.  The agent uses them.  On Windows, install
  Python from python.org; if `python` is not found afterwards, `py` works
  in its place.
* **A way to watch files appear**: your editor's file view, or your
  agent app's.
* One uninterrupted sitting.  The steps are short, but do not start
  this one in the gaps between other things.

## What you will end up with

A **throwaway folder**, `cairn-try`, holding a copy of Cairn and a small
practice project with:

* a `dev/` tree containing one proposal, with its review and decision,
  archived;
* one commit per lifecycle step (open, review, decision,
  implement-and-archive), plus the two setup commits (init, install);
* a `CHANGELOG.md > Unreleased` line for the change.

At the end you delete the folder.  You are *not* installing Cairn into a
real project, though the install is real: Steps 2 and 3 are what you
would run on a real project, with the smallest profile Cairn ships.

## Your three jobs

The agent does the typing.  Three things stay yours, here and in real
work:

1. **The trust decision.**  The agent will run code from the copy of
   Cairn it downloads.  For this throwaway you can accept that; for a
   real project, check the release first (see Step 1).
2. **Being the Maintainer.**  You decide whether the change goes ahead,
   in your own words.
3. **Choosing a fresh reviewer.**  You open a new chat, so the review is
   written by a session that did not write the proposal.

## Step 1 -- a throwaway folder, Cairn, and a practice project

Make an empty folder named `cairn-try` anywhere you like, and open your
agent in it (in its app, choose the folder as the project or
workspace).  Then paste:

<!-- cairn-accept: suspicious-url reason="Literal Cairn clone URL the adopter needs to copy" reviewer="Claude" date=2026-05-28 -->
> In this folder, clone https://github.com/MSUHydrogeology/cairn.git
> into a subfolder named `cairn`.  Then make a second subfolder named
> `quickstart`, turn it into a git repository, and add two files: a
> `README.md` containing `# quickstart`, and a `CHANGELOG.md` containing
> `# Changelog`, a blank line, and `## Unreleased`.  Commit both files
> in `quickstart` with the message `init`.  Tell me what you did.

<details>
<summary>Or do it yourself in a terminal</summary>

Start in the folder where you want `cairn-try` to live.

<table>
<tr><th>macOS / Linux (Terminal)</th><th>Windows (PowerShell)</th></tr>
<tr>
<td>

```bash
mkdir cairn-try
cd cairn-try
git clone https://github.com/MSUHydrogeology/cairn.git cairn
export CAIRN="$(pwd)/cairn"
mkdir quickstart
cd quickstart
git init -q
echo "# quickstart" > README.md
printf "# Changelog\n\n## Unreleased\n" > CHANGELOG.md
git add README.md CHANGELOG.md
git commit -q -m "init"
```

</td>
<td>

```powershell
New-Item -ItemType Directory cairn-try | Out-Null
Set-Location cairn-try
git clone https://github.com/MSUHydrogeology/cairn.git cairn
$CAIRN = Join-Path (Get-Location).Path "cairn"
New-Item -ItemType Directory quickstart | Out-Null
Set-Location quickstart
git init -q
Set-Content README.md "# quickstart"
Set-Content CHANGELOG.md "# Changelog`n`n## Unreleased"
git add README.md CHANGELOG.md
git commit -q -m "init"
```

</td>
</tr>
</table>

`CAIRN` holds the path to your copy of Cairn for the rest of the
commands.  It lasts only as long as this terminal window, so run the
remaining steps in the same window.

</details>
<!-- cairn-accept-end: suspicious-url -->

`quickstart` gets a stub `CHANGELOG.md` because Cairn's lifecycle writes
to a changelog and the installer does not create one: a real project
usually has its own.

> **This copy is the trust decision.** Everything below runs code from
> it.  Before you install Cairn into anything you care about, verify the
> release tag against a signing-key fingerprint you compared on two
> independent channels; the procedure is in `bootstrap/PROVENANCE.md` >
> "Verifying a release".  For this throwaway you can skip it; for a real
> project you should not.

> **Windows is new.**  The Windows commands were added in October 2026,
> and Cairn's own tests run on macOS.  The installer and tools are plain
> Python with no shell dependencies, so they are expected to work, but if
> a step fails on Windows, please
> [open an issue](https://github.com/MSUHydrogeology/cairn/issues) with
> what you ran and what it printed.

## Step 2 -- choose the profile

A profile tells the installer how much of Cairn your project needs.
This recipe uses the smallest one, `solo-greenfield`: one person, one
agent, a new codebase.  Paste:

> Copy `cairn/bootstrap/profiles/solo-greenfield.yml` into the
> `quickstart` folder as `profile.yml`, and show me what is in it.

<details>
<summary>Or do it yourself in a terminal</summary>

<table>
<tr><th>macOS / Linux (Terminal)</th><th>Windows (PowerShell)</th></tr>
<tr>
<td>

```bash
cp "$CAIRN/bootstrap/profiles/solo-greenfield.yml" profile.yml
```

</td>
<td>

```powershell
Copy-Item "$CAIRN\bootstrap\profiles\solo-greenfield.yml" profile.yml
```

</td>
</tr>
</table>

</details>

The settings look like this:

```yaml
# Inline token values (mechanical substitution into installed templates).
project_name: "Quickstart"
test_command: "pytest"

# Module selection: reference the named governance preset.  Scaffold
# expands it to the default-on set + the (empty) team-gated baseline.
preset: solo-greenfield
```

The full file starts with a comment listing the six-axis profile this
preset expresses and the modules it installs.  The other shipped
profiles
([`collaborative-team.yml`](../bootstrap/profiles/collaborative-team.yml),
[`high-rigor-legacy.yml`](../bootstrap/profiles/high-rigor-legacy.yml))
have the same shape with different presets.

## Step 3 -- preview, then install

**Preview first.**  Paste:

> In the `quickstart` folder, run
> `python ../cairn/bootstrap/scaffold.py --config profile.yml --target . --summary`
> and show me the list of modules it would install.  Do not install
> anything yet.

The `--summary` flag only previews: nothing is written.  For the
`solo-greenfield` profile you should see **6** modules listed <!-- verify: solo_greenfield_module_count -->
(the modules every install gets): `reflections`, `claim-check`,
`incident-trackers`, `documentation-plan`, `content-security`,
`security-verification`.

> **What the six axes are.** Cairn sizes the apparatus to your
> project along six axes: **age** (greenfield or legacy), **size**
> (small to large), **complexity** (simple to complex), **language**
> (one or several), **human_team** (solo to large team), and
> **agent_team** (one agent to several). `solo-greenfield` takes the
> smallest value on every axis, so it installs the least. Larger
> projects take larger values and get more modules; see
> [`dimensions/README.md`](../dimensions/README.md).

**Then install.**  Paste:

> Run the same command without `--summary` to install, and show me the
> report it prints.  Then commit what it installed (`AGENTS.md`,
> `VENDOR.md`, `NOTICE.md`, `.gitignore`, `dev/`, `tools/`, `scripts/`,
> `.agents/` and `docs/`) with the message
> `Install Cairn kernel + default-on modules`.  Leave `profile.yml`
> uncommitted.

<details>
<summary>Or do it yourself in a terminal</summary>

<table>
<tr><th>macOS / Linux (Terminal)</th><th>Windows (PowerShell)</th></tr>
<tr>
<td>

```bash
python "$CAIRN/bootstrap/scaffold.py" --config profile.yml --target . --summary
python "$CAIRN/bootstrap/scaffold.py" --config profile.yml --target .
```

</td>
<td>

```powershell
python "$CAIRN\bootstrap\scaffold.py" --config profile.yml --target . --summary
python "$CAIRN\bootstrap\scaffold.py" --config profile.yml --target .
```

</td>
</tr>
</table>

Then commit the install; the commands are the same in both terminals:

```text
git add AGENTS.md VENDOR.md NOTICE.md .gitignore dev/ tools/ scripts/ .agents/ docs/
git commit -q -m "Install Cairn kernel + default-on modules"
```

</details>

> **A note on the provenance warning.**  Because Step 1 copied Cairn's
> latest commit rather than a tagged release, the installer prints a
> one-line provenance warning suggesting `--allow-dev`.  That is
> **expected** here and never blocks the install.  A real adoption
> installs from a tagged release, where the warning does not appear.

The installer's report is the **authoritative list** of every file it
wrote.  Open the `quickstart` folder in your editor's file view now and
leave it open: from here on you watch the record grow as files appear.
For this recipe you only need two things:

* `AGENTS.md` -- the rules your agent reads.  `VENDOR.md` is a template
  you rename to the file your agent tool loads automatically.
* the `dev/` folder -- where the record lives: the roadmap boards, the
  `proposals/` and `plans/` templates, and one doc per installed
  module.  `dev/.cairn/` holds the lockfile and install state that
  updates use; you never need to read it.

`tools/`, `scripts/` and `.agents/` hold helper tools and the
`session-start` / `session-end` routines.  Ignore them for now.

The report also lists **19 unfilled block slots** -- placeholders
your agent fills in a real adoption (see
[`bootstrap/BOOTSTRAP.md`](../bootstrap/BOOTSTRAP.md) Act II-4) -- and
lists separately the 2 slots that belong to modules this profile did
not install.  This recipe leaves them: the tagline does not need them, and the report's
"Next steps **for a real adoption**" are for a real project.

## Step 4 -- the agent writes a proposal

> **Where the agent will write.** A proposal is a Markdown file such
> as `dev/proposals/2026-XX-XX-<slug>.md`.  Its header has the fields
> `Author`, `Status`, `Review`, `Plan review`, `Opened` and `In brief`,
> and it starts at `Status: awaiting-review`.  Below the header come
> sections such as Context, Proposal, Alternatives considered and
> Evidence / verification plan.  A review and a decision are
> appended later, in order.  The whole file is the record.  See
> [`dev/proposals/_template.md`](../templates/core/dev/proposals/_template.md)
> for the full shape.  For a one-line tagline most sections need only a
> sentence.

Paste this (the prompt is short on purpose; `AGENTS.md` carries the
rules):

> Work in the `quickstart` folder.  Read `AGENTS.md` to learn how
> proposals work.  Then propose a one-line addition to `README.md`: a
> brief project tagline.  Open the proposal as
> `dev/proposals/2026-XX-XX-<your-name>-readme-tagline.md`, copying
> the shape of `dev/proposals/_template.md`, with Status
> `awaiting-review`.  Do not implement anything yet.  Commit only the
> proposal, with the message `Open proposal: README tagline`.

Watch the file appear in `dev/proposals/`.  The agent should read
`AGENTS.md`, write the proposal, commit it and stop.  In the heavy lane
the proposal comes before the code.

<details>
<summary>Or commit it yourself in a terminal</summary>

The commands are the same in both terminals:

```text
git add dev/proposals/
git commit -q -m "Open proposal: README tagline"
```

</details>

## Step 5 -- review, decide, implement, archive

**Review, in a new chat.**  Start a **new chat** with your agent, in the
same `cairn-try` folder, so the reviewer is not the session that wrote
the proposal.  Paste:

> Work in the `quickstart` folder.  You did not write the proposal in
> `dev/proposals/`.  Read it and `AGENTS.md`, then append a `## Review`
> section in the shape the template gives.  Question whether the change
> should happen as framed, name the best alternative (doing nothing
> counts), and say what would show it wrong.  Commit only the proposal
> file.

The reviewer writes and commits its own review.  If it finds nothing
blocking, it moves the header to `Status: awaiting-decision`.  If it
finds something blocking, the status becomes `revising` and the first
chat answers in an appended section before you decide.

**Decide, in your editor.**  You are the Maintainer.  Open the proposal
in your editor, add a `## Decision` section at the end in your own
words, set apart as a quote, and change the header to
`Status: accepted`.  Save the file.

```markdown
## Decision -- <your-name> -- 2026-XX-XX

**ACCEPTED.** The Maintainer's authorization, quoted verbatim:

> "Accepted.  Add the tagline and archive the proposal in one commit."
```

Then go back to the **first** chat, the one that wrote the proposal, and
paste:

> I have accepted the proposal; my decision is in the file.  Commit my
> decision on its own, with the message `Decision: accept README tagline`.
> Then implement the tagline, move the proposal to
> `dev/proposals/archive/`, add a one-line entry to
> `CHANGELOG.md > Unreleased`, and commit those three together as one
> implementing-and-archiving commit.

A small accepted proposal can be implemented and archived in one commit
with no plan.  You should see the agent:

* commit your decision;
* edit `README.md` to add the tagline;
* move the proposal into `dev/proposals/archive/`;
* add the CHANGELOG line;
* commit those three together, naming each file.

<details>
<summary>Or commit your decision yourself in a terminal</summary>

The command is the same in both terminals:

```text
git commit -q -m "Decision: accept README tagline" dev/proposals/
```

</details>

## Step 6 -- look at what you have

Paste:

> Show me `git log --oneline`, the contents of `dev/proposals/archive/`,
> and `CHANGELOG.md`.

Or look for yourself: your editor's source-control or history view shows
the commits, and the file view shows the archive folder.

<details>
<summary>Or look in a terminal</summary>

<table>
<tr><th>macOS / Linux (Terminal)</th><th>Windows (PowerShell)</th></tr>
<tr>
<td>

```bash
git log --oneline
ls dev/proposals/archive/
cat CHANGELOG.md
```

</td>
<td>

```powershell
git log --oneline
Get-ChildItem dev\proposals\archive
Get-Content CHANGELOG.md
```

</td>
</tr>
</table>

</details>

You should see:

* six commits with clear lifecycle boundaries (init, install,
  proposal-open, review, decision, implement-and-archive);
* the proposal in `archive/`, frozen, with its review and decision;
* a CHANGELOG line that records what changed.

That is the lifecycle.  A larger change adds a plan, with its own
review, but the mechanics are the same.

## Step 7 -- clean up

Close the agent's chats, then delete the `cairn-try` folder in your file
manager.  Nothing outside it was touched.

<details>
<summary>Or delete it in a terminal</summary>

Run this from the folder that holds `cairn-try`.

<table>
<tr><th>macOS / Linux (Terminal)</th><th>Windows (PowerShell)</th></tr>
<tr>
<td>

```bash
rm -rf cairn-try
```

</td>
<td>

```powershell
Remove-Item -Recurse -Force cairn-try
```

</td>
</tr>
</table>

</details>

## What you saw

* **Proposal before code.**  The first commit after setup was a
  proposal, not a feature.
* **Each transition is its own commit.**  Open, review, decision and
  implement-and-archive each landed separately.
* **A fresh reviewer.**  A new chat that did not write the proposal
  questioned it in writing before you decided.
* **The proposal is the record.**  After archiving, you can read the
  file and reconstruct *why* the change happened, not just *what*.
* **You decided.**  The agent proposed and implemented; you decided, in
  your own quoted words.

## What you did *not* see

* **The other two lanes.**  A trivial change (a typo or one-line fix)
  takes no proposal and no code review.  A change whose shape is already settled takes one
  short change note, reviewed, then the change and its test.  When
  unsure, take the heavier lane.  See
  [`doctrine/lifecycle.md`](../doctrine/lifecycle.md).
* **Extra distance in review.**  A fresh chat with the same agent is
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
