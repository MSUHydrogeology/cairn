<!-- Migrated 2026-06-12 from modflow_tools dev/strategy/ (Cairn's development home before self-hosting). Authored from modflow_tools' vantage; some path cites and "current state" reflect that origin and are being adapted to Cairn. Preserved as Cairn's living deliberation record -- see dev/strategy/MIGRATION.md. -->
# Cairn adopter-friction audit -- prospective scientist lens

**Author**: Codex
**Role**: External Reviewer / prospective adopter
**Date**: 2026-05-27
**Status**: settled
**Type**: comparative-research

## Lens

Read Cairn as a new potential adopter: a scientist maintaining a codebase, or
starting one, who knows only that Cairn promises a way to build better
scientific software faster with AI agents than pure vibecoding. The question is
not "is the doctrine internally coherent?" but "does a scientist and one AI
agent know what to do, trust the apparatus, and get value before the process
feels heavier than the problem?"

## Summary

Cairn's core promise is credible on rigor: append-only decisions, explicit
Maintainer authority, review before code, dimensional adaptation, security
guardrails, and a real bootstrap path. It is less convincing, today, on
first-use speed. A cold adopter will likely see a serious methodology repo
before they see a guided adoption experience.

The main product move before `0.3` should be to make Cairn feel small at the
point of entry: one clear quickstart, one tiny scientific example, one
bootstrap-lite path, and one readiness artifact for legacy scientific code.
The deeper doctrine can remain available, but it should not be the first
surface a user has to metabolize.

## Where Cairn currently overachieves

* **The doctrine is real.** Cairn is not a prompt pack dressed up as process.
  The lifecycle, Dual-Review, session routines, and coordination model solve
  actual failures observed in modflow_tools and LHM.
* **The adaptation matrix is the right abstraction.** Scientific repositories
  differ wildly; the six-axis model prevents a one-size-fits-all process.
* **The bootstrap is careful.** Act I insists on profile acceptance before
  installation, Act II separates scaffold from customization, and the safety
  docs acknowledge target-repo privacy.
* **The security posture has teeth.** Content scanning, lockfile integrity,
  vendor-neutrality checks, and profile-trust warnings make Cairn more
  trustworthy than an informal "let the agent set up your repo" script.

## Main adoption gaps

1. **No true 15-minute quickstart.** The README points to adoption levels and
   getting-started docs, but there is no copy-paste path for trying Cairn on a
   disposable repo. A new user needs a minimal profile, the exact scaffold
   command, expected output, the first agent prompt, and the first dogfood
   change.
2. **The bootstrap is powerful but intimidating.** `bootstrap/BOOTSTRAP.md` is
   appropriate for a serious Level 2 adoption, but the first read asks the user
   to score axes, select modules, present a profile, scaffold, merge module
   content into slots, verify, and dogfood. That is right for high-rigor
   adoption and too much for first contact.
3. **Manual module merging is a likely failure point.** The "read `Adds to:`,
   copy `Merged into:`, paste into the slot" workflow is easy for a careful
   agent but fragile for a new adopter. A mistake can pass the unfilled-slot
   check while carrying the wrong prose.
4. **The "faster" claim is not yet explained honestly.** Cairn is slower for
   the first few changes. Its speed comes later: fewer repeated decisions,
   fewer forgotten assumptions, fewer agent collisions, and less rework after
   unreviewed scientific choices. That trade should be said plainly.
5. **Single-agent adoption needs stronger reassurance.** Cairn leads with
   Dual-Review, but many scientists will begin with one human and one agent.
   The docs should say directly that Cairn works with one agent: start with the
   kernel, use Maintainer review or fresh-session review, and add stronger
   independence only when the team can staff it.
6. **Legacy-code assessment needs a concrete artifact.** A maintainer of a
   legacy scientific codebase needs a "Codebase Readiness Report" before they
   need doctrine. It should cover tests, hidden state, scripts, notebooks,
   data I/O, generated outputs, public APIs, build/run commands,
   reproducibility, security boundaries, and scientific assumptions.
7. **Security guidance should appear earlier.** Cairn asks users to trust AI
   agents with repo-governance files. The README/on-ramp should surface a short
   trust statement: what the agent may read, what must not be exported, what
   private paths/data must not enter Cairn, and what checks are run.
8. **The minimal example is too toy-like for scientists.** The current
   minimal example
   teaches the lifecycle shape, but `greet.py` does not feel like scientific
   computing. A second minimal example should use a tiny scientific workflow:
   read a CSV, compute a result, write a figure or table, and test a scientific
   invariant.
9. **Release hygiene is a trust signal.** The current working tree had
   untracked cache artifacts under the minimal example directory. They are not
   tracked, but a public release should make the repo visibly pristine for
   first-time evaluators.

## Recommended pre-0.3 package

Treat this as an **adopter-friction package**, not a doctrine expansion:

External-repo path: `cairn/examples/minimal`
Proposed path: `cairn/docs/quickstart.md`

1. **Add a quickstart page.** "Try Cairn in 15 minutes with one AI agent."
   Include a minimal `profile.yml`, exact scaffold command, expected installed
   files, first prompt to the agent, first dogfood change, and teardown note.
2. **Add profile examples.** Provide copyable profiles such as
   `solo-greenfield.yml`, `collaborative-team.yml`, and
   `high-rigor-legacy.yml`, matching the governance presets.
3. **Add a bootstrap-lite prompt.** A short prompt a maintainer can paste into
   an AI agent: assess this repo, propose a profile, wait for my approval, then
   scaffold and dogfood one change.
4. **Add a legacy Codebase Readiness Report template.** Make this the first
   artifact for existing scientific codebases. It should be useful even if the
   team stops at Level 0 or Level 1.
5. **Add a scientific minimal example.** Keep `greet.py`, but add a small
   scientific workflow example that feels familiar to researchers.
6. **Add a README trust box.** Short, early security/trust posture for
   adopting with agents: privacy boundary, local-only assessment, no secrets
   in Cairn artifacts, and the core checks.
7. **Tighten onboarding language around speed.** Use a candid line:
   "Cairn adds friction before code; it pays back by preventing rework,
   forgotten decisions, and unreviewed AI changes."

## Product framing

The adoption promise should become:

> Start small. Use Cairn to make one AI-assisted change with a recorded
> decision and test. Keep the apparatus only as heavy as your codebase and team
> earn.

That framing makes Cairn legible to a scientist who wants better software
without signing up for a methodology course on day one.
