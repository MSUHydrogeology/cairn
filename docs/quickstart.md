# Try Cairn through one small change, with one AI agent

This page is a recipe, not a tour.  You will take one small change
through Cairn's lifecycle on a throwaway project, working the way most
people work with an AI agent: **in its chat**, in the agent's own app or
in your editor.  The agent runs the commands; you make the decisions.

Every step also shows the commands, if you would rather type them
yourself in a terminal, with macOS / Linux and Windows side by side.
This recipe shows one change from proposal to archive. For fuller explanations,
read [`getting-started.md`](getting-started.md) and
[`docs/methodology/`](methodology/).

> **A note on the example.** The change here is a one-line README
> tagline. In real work, that is a *trivial* change: you would make it
> and commit it with its test, with no code review. Cairn sorts changes
> into three paths. Substantive work starts with a proposal; the Maintainer's
> Decision sets its tier. Light is the default and has no plan, while non-trivial standard
> and heavy work uses plan triage. This recipe takes the
> tagline through the proposal path as a light example **on purpose**, so you
> can see its review, decision, implementation check and archive without adding
> a plan. Normally, a one-line tagline takes the trivial lane above.

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
* **Python 3.12 or later** and **git**,
  installed on your computer.  The agent uses them.  On Windows, install
  Python from python.org; if `python` is not found afterwards, `py` works
  in its place.
* **A way to watch files appear**: your editor's file view, or your
  agent app's.
* Enough time to finish in one sitting. The recipe does not estimate a
  duration; it depends on your agent and how closely you read.

## What you will end up with

A **throwaway folder**, `cairn-try`, holding a copy of Cairn and a small
practice project with:

* a `dev/` tree containing one proposal, with its review and decision,
  archived;
* one commit per lifecycle step (open, review, decision, implementation,
  verification record, archive), plus the two setup commits (init, install);
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
> `quickstart`, turn it into a git repository, and add one file: a
> `README.md` containing `# quickstart`.  Commit it in `quickstart`
> with the message `init`.  Tell me what you did.

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
git add README.md
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
git add README.md
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

The install creates `CHANGELOG.md` from Cairn's template, so the example
starts without one. On a real project, Cairn preserves an existing
`CHANGELOG.md` byte-for-byte. Because that file differs from the clean
template, the install cannot create an upgrade baseline; use the profile
and migration steps in [`UPGRADE.md`](../bootstrap/UPGRADE.md#the-workflow)
if you want Cairn to manage future upgrades. `upgrade --init-lock` needs a
complete profile, and files with customized text, including an existing
changelog, are marked for manual review on later upgrades rather than
automatically merged.

> **The commands below run code from this copy.** Before you install Cairn
> into anything you care about, the Maintainer should choose a release route
> before candidate code runs. For a stable official release, the ordinary
> route in `bootstrap/PROVENANCE.md` checks the official release selection and
> exact checkout without signing-key setup; it does not authenticate the
> publisher. The optional stronger route verifies the signed tag against
> independently checked fingerprints. For this throwaway you can skip those
> release checks; for a real project, follow its authorization rules. The
> Maintainer chooses the route and may authorize an agent to perform the
> install.

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

> **What the six axes are.** Cairn chooses installed modules based on six
> parts of your project: **age** (greenfield or legacy), **size**
> (small to large), **complexity** (simple to complex), **language**
> (one or several), **human_team** (solo to large team), and
> **agent_team** (one agent to several). `solo-greenfield` takes the
> smallest setting on every axis, so it installs the fewest modules. Larger
> projects take larger values and get more modules; see
> [`dimensions/README.md`](../dimensions/README.md).

**Then install.**  Paste:

> Run the same command without `--summary` to install, and show me the
> report it prints.  Then commit what it installed (`AGENTS.md`,
> `VENDOR.md`, `NOTICE.md`, `.gitignore`, `dev/`, `tools/`, `scripts/`,
> `.agents/`, `docs/` and `CHANGELOG.md`) with the message
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
git add AGENTS.md VENDOR.md NOTICE.md .gitignore dev/ tools/ scripts/ .agents/ docs/ CHANGELOG.md
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
`session-start` / `session-end` routines. After this exercise, see the
[session journey](tool-usage.md#starting-and-ending-a-session) and the
[upgrade journey](tool-usage.md#upgrading-an-existing-install).

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
> brief project tagline.  This is a light deliberate example; state that
> tier in the proposal and explain that the real one-line change would
> normally use the trivial lane.  Open the proposal as
> `dev/proposals/2026-XX-XX-<your-name>-readme-tagline.md`, copying
> the shape of `dev/proposals/_template.md`, with Status
> `awaiting-review`.  Do not implement anything yet.  Commit only the
> proposal, with the message `Open proposal: README tagline`.

Watch the file appear in `dev/proposals/`.  The agent should read
`AGENTS.md`, write the proposal, commit it and stop.  In every tier of the
proposal path, the proposal comes before the code. A non-trivial accepted
standard or heavy proposal also gets a plan, reviewed when required; light has
no plan.

<details>
<summary>Or commit it yourself in a terminal</summary>

The commands are the same in both terminals:

```text
git add dev/proposals/
git commit -q -m "Open proposal: README tagline"
```

</details>

## Step 5 -- review, decide, implement, check, archive

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

> "Accepted as a light example.  Implement the tagline, run the applicable final check, record its results and omissions in the proposal, then archive it in a later commit."
```

Then go back to the **first** chat, the one that wrote the proposal, and
paste:

> I have accepted the proposal; my decision is in the file.  Commit my
> decision on its own, with the message `Decision: accept README tagline`.
> Then implement the tagline and add a one-line entry to
> `CHANGELOG.md > Unreleased`; commit those two files as
> `Implement README tagline`.  On that clean commit, run the applicable
> bounded final integration check required by `AGENTS.md`.  Append the
> command, result and any omissions to the accepted proposal as an
> implementation verification record, and commit that record on its own.
> Finally move the proposal to `dev/proposals/archive/` in a later commit.

A light accepted proposal has no plan.  You should see the agent:

* commit your decision;
* edit `README.md` and add the CHANGELOG line, then commit both;
* run the bounded final check on that clean implementation commit;
* record its command, result and omissions in the proposal and commit it;
* archive the proposal in a later, separate commit.

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

You should see eight commits with clear lifecycle boundaries (init,
install, proposal-open, review, decision, implementation, verification
record and archive):

* the proposal in `archive/`, frozen, with its review, decision and
  implementation verification record;
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
* **Each transition is its own commit.**  Open, review, decision,
  implementation, verification record and archive each landed separately.
* **A fresh reviewer.**  A new chat that did not write the proposal
  questioned it in writing before you decided.
* **The proposal is the record.**  After archiving, you can read the
  file and reconstruct *why* the change happened, not just *what*.
* **You decided.**  The agent proposed and implemented; you decided, in
  your own quoted words.

## What you did *not* see

* **The other paths.** A trivial change (a typo or one-line fix) takes no
  proposal and no code review. Other substantive work starts with a proposal
  whose Decision sets its tier.
  Light records implementation and final verification on that proposal.
  Standard and heavy work retain plan triage and required reviews.  When
  unsure about ceremony, take the lighter lane with a reason; stop on a newly
  discovered trust boundary. See
  [`docs/methodology/lifecycle.md`](methodology/lifecycle.md).
* **Extra distance in review.**  A fresh chat with the same agent is
  enough.  When you want more distance, you can ask for another model
  or a person to review a particular piece of work (see
  [`docs/methodology/dual-review.md`](methodology/dual-review.md)).
* **Plans.** A non-trivial standard/heavy accepted proposal opens a
  [plan](../templates/core/dev/plans/_template.md) that sequences the work and
  gets its own review. Light has no plan even for multi-area work. This one
  did not need a plan.
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
  to, from the stable official tag selected under either route in
  `bootstrap/PROVENANCE.md` > "Choosing an adopter verification route".
  After integrity verification, record its URL, tag, version and full commit
  in the same target commit as the installed files and lockfile, and read that
  message back. Then do the four steps the installer prints
  for a real adoption (`bootstrap/BOOTSTRAP.md` Act II-3 to II-6).
  The [on-ramp](../on-ramp/README.md) has the profile table, and what
  to do if you copied the kernel in by hand.
* **Read the methodology** -- [`docs/methodology/`](methodology/) explains
  *why* the lifecycle works as it does.  Start with
  [`lifecycle`](methodology/lifecycle.md) and
  [`dual-review`](methodology/dual-review.md).

## Honest framing

Cairn is **slower for the first few changes**.  Its speed comes
later: fewer repeated decisions, fewer forgotten assumptions, fewer
agent collisions, and less rework after unreviewed scientific
choices.  Keep the apparatus only as heavy as your codebase and team
earn -- the profile you choose is that calibration (see the
[on-ramp](../on-ramp/README.md)).
