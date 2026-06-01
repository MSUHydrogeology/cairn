<!-- Cairn progressive-onboarding task list: high-rigor-legacy preset.
     Authored under plan 2026-05-28-claude-cairn-progressive-onboarding
     (Chunk P1.6 fills the full legacy-pre-pass + security-review +
     dual-language-tests task list; P1.1 shipped a placeholder
     ahead of this). -->

# Onboarding tasks -- high-rigor-legacy

This file ships **three kinds of content**, segregated by tag
syntax so the scaffold + the activation helper can parse them
unambiguously:

* `[seed; id: <name>]` lines -- day-one PLANNING entries.
* `[trigger: <trigger-name>; id: <name>]` lines -- held until the
  named trigger fires.
* Active-surfacing prompt content blocks at the end -- per-row
  prompt content emitted to the terminal when the row's trigger
  fires.

The `high-rigor-legacy` preset assumes the heaviest shape: 5+
humans + multiple agent types on a legacy codebase with multi-
language modules + real domain logic + security boundaries that
matter. The tasks are calibrated for that scale -- the
codebase-readiness-report pre-pass shapes the first weeks of
adoption; the security-review + dual-language-tests modules are
load-bearing from day one; the existing-maintainer authority
needs explicit confirmation before any apparatus customization
goes live.

## Tasks

* [seed; id: try-session-start-skill]
  Try the `session-start` skill (`/good-morning`): run
  `python tools/lifecycle.py session-start` to orient at the top of a
  session. The lifecycle routines are now invokable skills installed under
  `.agents/skills/`; the canonical doctrine is `doctrine/session-routines.md`.

* [seed; id: fill-readiness-report]
  Fill `templates/codebase-readiness-report.md` for your legacy
  tree BEFORE engaging the team apparatus. The eleven-section
  assessment surfaces hidden state, scientific assumptions, and
  security boundaries; the readiness scores drive whether
  Level 2 adoption is actually right (vs. Level 1 or Level 0
  while gaps get fixed). Do not skip this; legacy codebases
  reward the pre-pass that greenfield does not need.

* [seed; id: confirm-maintainer-authority]
  Confirm the existing project maintainer's authority is
  reflected in `dev/collaboration_agreement.md`'s `team-roster`
  slot. The legacy-codebase shape almost always has a de-facto
  Maintainer whose authority pre-dates the Cairn adoption; the
  apparatus should match the existing power structure, not
  invert it.

* [seed; id: read-security-review-module]
  Read `dev/modules/security-review.md`. The high-rigor-legacy
  preset installs the security-review module by default; legacy
  codebases carry security boundaries that the
  proposal-lifecycle's normal review tier does not necessarily
  surface. Security-review is the explicit channel for that
  class of finding.

* [seed; id: read-dual-language-tests-module]
  Read `dev/modules/dual-language-tests.md`. Multi-language
  codebases (e.g., Python + Fortran, Python + C, Python + CUDA)
  need the dual-language-tests gate to keep both language
  surfaces honest; the preset installs the module by default.

* [seed; id: read-legacy-agent-module]
  Read `dev/modules/legacy-agent.md`. The legacy-agent module
  carries the apparatus for landing changes safely in a tree
  with existing operational dependencies -- a different
  discipline than greenfield development.

* [seed; id: install-work-intent-hooks]
  Install the work-intent git hooks, or record that you are skipping
  them. This preset is concurrent, so the scaffold *recommended* the
  hooks at install time but does **not** install them for you (it
  never mutates `.git/hooks`). Run `python tools/intent.py
  install-hook` + `install-precommit`, then `hooks-status` to confirm.
  Without them, `dev/intents.jsonl` stays empty and the coordination
  signal never fires. To opt out (now or later), re-run either command
  with `--uninstall`; note the choice here so the team's preference is
  on the record.

* [seed; id: agent-team-onboarding-legacy]
  Walk `dev/modules/onboarding/agent-team-onboarding.md` together. The
  high-rigor-legacy profile expects multi-agent staffing; the
  second agent type's capability tier should be calibrated
  against the security-review module's bar from day one.

* [seed; id: walk-dev-tour]
  Walk `dev/modules/onboarding/dev-tour.md` as a final pre-engagement read; it
  carries the `dev/`-tree taxonomy + a worked example. After
  reading it, the team is ready to open the first proposal.

* [trigger: first-proposal-archived; id: post-first-proposal-legacy]
  Now that the team has shipped one change through the lifecycle,
  the next focus is calibrating the security-review +
  dual-language-tests + legacy-agent modules against the actual
  rhythm of your tree. The first cycle is the diagnostic; the
  second through fifth shape the steady-state.

* [trigger: first-cross-type-review; id: post-first-cross-type-legacy]
  Your first cross-agent-type review just shipped. For
  high-rigor-legacy this is foundational -- the Dual-Review
  External tier is the structural check that legacy domain
  knowledge alone cannot supply. Make cross-type-review the
  default going forward.

* [trigger: first-foldback-candidate; id: walk-foldback-protocol]
  Your fold-back ledger has its first open candidate ready to
  surface upstream. The foldback active-surfacing prompt
  (`doctrine/fold-back.md > Active surfacing`) walks through
  filing; the high-rigor-legacy profile's content-security +
  security-review gates apply to the drafted filing body before
  it leaves the deployment.

## Active-surfacing prompt content (per-preset)

The four active-surfacing rows the high-rigor-legacy preset emits:

### Row 1 -- collab-agreement-signing prompt

Confirm the existing maintainer's authority is reflected in the
team-roster slot of `dev/collaboration_agreement.md`. Negotiate
review-tier floor for protected changes. Multi-stakeholder fill
is the expected shape; the team-roster slot is the surface
where pre-existing power structure gets made explicit to the
Cairn apparatus.

### Row 2 -- Level 1→2 graduation prompt

Your legacy-tree work has accumulated enough lifecycle activity
that the bootstrap's preset-driven installation would now match
your team-staffing gate's actual shape better than Level 1's
hand-copy approach. Walk `bootstrap/BOOTSTRAP.md` + the
`bootstrap/UPGRADE.md` pre-pass; the lockfile gives you the
integrity surface you currently lack.

### Row 3 -- second-agent-type spin-up prompt

Your high-rigor-legacy profile's review rigor depends on
multi-agent staffing. Walk `dev/modules/onboarding/agent-team-onboarding.md`; the
second agent type's capability tier should be calibrated against
your security-review module's bar -- a strong second agent
strengthens the External-tier review's structural independence
for the security-boundary class of finding that legacy
codebases carry.

### Row 4 -- upstream PR/issue walkthrough prompt

Your fold-back ledger carries a candidate ready for upstream
filing. The foldback active-surfacing prompt
(`doctrine/fold-back.md > Active surfacing`) walks through
filing; the high-rigor-legacy profile's content-security +
security-review gates apply to the drafted filing body before
it leaves the deployment. Run the scrub scanner on the draft
explicitly before submitting.
