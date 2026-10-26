# The on-ramp — two ways in

Adopting Cairn is **not** all-or-nothing. You can **read it** and let the
ideas shape how you already work, or you can **install it**. There is one
installer, and the profile you give it decides how much it installs, so start
small and grow.

![Two ways in: read the method and install nothing, or install it by choosing a profile, running the scaffold and doing the four steps the installer prints. An install then grows by adding modules as the work earns them; a profile is a starting point, not a rank.](../docs/assets/two-ways-to-adopt.svg)

> **Honest framing.** Cairn is **slower for the first few changes**:
> writing decisions down, reviewing them, and committing the trail adds
> friction *before* code. The payback is later — fewer repeated decisions,
> fewer forgotten assumptions, fewer agent collisions, and less rework after
> unreviewed scientific choices. Keep the apparatus only as heavy as your
> codebase and team earn; the profile you choose is that calibration.

## Read it

Adopt nothing mechanically. Read `doctrine/` as a handbook and let it inform
how the team already works — no `dev/` tree, no templates. The project takes
the *ideas* (recorded deliberation, the Dual-Review model) without the
apparatus. The Turing Way is the model for this mode.

## Install it

Run the scaffold with a profile. The route is the same for every project:

1. **Choose a profile** (below).
2. **Run the scaffold** against your repository.
3. **Do the four steps the installer prints** for a real adoption — confirm the
   installed files, fill the block slots, run the acceptance gate, and take one
   change through the lifecycle (`bootstrap/BOOTSTRAP.md` Act II-3 to II-6).

The profile decides which modules arrive; nothing else does. `team-gated` is
the name of a folder of modules, not a rank: a solo scientist on an existing
codebase installs some of them, and that is the right install.

**You do not need a second reviewer to start.** Every review's floor is a
fresh session, so one agent is enough: a new session of it reviews what an
earlier session wrote, and your own read as Maintainer counts too. A second
agent type, or a second human, adds more distance whenever you ask for it; it
is never required.

To try the whole thing on a throwaway repository first, run
[`../docs/quickstart.md`](../docs/quickstart.md). The commands it uses are a
real install with the smallest profile.

## Choosing a profile

| The project is... | Start with |
|-------------------|------------|
| exploring the ideas, not yet committed | reading the doctrine |
| a new project, one Maintainer | the `solo-greenfield` profile |
| an existing codebase, one Maintainer | the composed profile in [`../docs/solo-legacy-recipe.md`](../docs/solo-legacy-recipe.md) |
| a team, or a large codebase with several contributors | `collaborative-team` or `high-rigor-legacy`, or have an agent score your project |

Three ways to arrive at a profile, from least to most help:

* **Take a preset as it is** — the files in `bootstrap/profiles/`.
* **Have your agent assess the repository and recommend one** —
  [`../bootstrap/prompts/bootstrap-lite.md`](../bootstrap/prompts/bootstrap-lite.md).
* **Score the six axes together** — `bootstrap/BOOTSTRAP.md` Act I, which the
  dimensional matrix (`dimensions/`) informs.

**For an existing codebase, fill
[`../templates/codebase-readiness-report.md`](../templates/codebase-readiness-report.md)
first.** Its eleven sections surface hidden state, scientific assumptions, and
security boundaries, and its G/M/P scores tell you how small to start: mostly
Good, install the profile your axes give; mostly Mixed with one or two Poor,
start with the smallest profile that fits and fix the Poor sections first;
three or more Poor, read the doctrine while you fix the gaps.

The choice is always yours; the profile and the report inform it.

## Growing an install

Start with the smallest profile that fits, and add modules as the work earns
them — test tiers (`testing-discipline`), the doc-drift gate
(`doc-drift-prevention`), an examples gallery (`examples-gallery`), or the
coordination and dual-review modules once several people or agents work in the
tree at once. Add one to an existing install with:

```
python bootstrap/scaffold.py upgrade --target <repo> --adopt-module <name>
```

Growing is depth, not a promotion: there is no rung to reach. Act III of
`bootstrap/BOOTSTRAP.md` covers operating and improving the apparatus once it
is running.

## If you copied the kernel by hand

A tree whose kernel was copied in by hand is still a valid install, but it
lacks two things the installer provides, so it receives **no upgrades and no
day-one task list**: a lockfile (`dev/.cairn/cairn-lock.yml`), which upgrades
need, and the files the installer adds on top of the kernel — the session
tools, the skills, and the profile's day-one tasks in `dev/PLANNING.md`. To
bring it under the installer:

```
python bootstrap/scaffold.py upgrade --target <repo> --init-lock
```

The first run writes `dev/.cairn/profile.yml` with four placeholders and stops
without writing a lockfile. Fill the placeholders, then run the same command
again. Files whose tokens you filled in by hand upgrade as review-only diffs,
so you compare and merge them yourself; the details are in
`bootstrap/UPGRADE.md` > "Migrating a tree installed before upgrade support".
Once the lockfile exists, `scaffold.py upgrade --target <repo> --plan` lists
the missing installer files as additions, and the upgrade (`--stage`, then
`--apply` once the review-only diffs are merged) brings them in.

**Do not re-run the install with `--force`** to get there. It overwrites what
you wrote.

---

This page describes *how much* to adopt. For *how the lifecycle runs* — one
change traced end-to-end — see
[`../docs/getting-started.md`](../docs/getting-started.md), and for where
Cairn sits relative to your build/test/CI tooling,
[`../docs/workflow-role.md`](../docs/workflow-role.md).
