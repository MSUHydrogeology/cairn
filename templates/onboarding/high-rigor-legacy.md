<!-- cairn-internal-ref-allow: doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- ^ Profile-conditional module files: present only in an adopter that installs them (this preset does); Cairn's own profile does not, so they don't resolve here. -->

<!-- Cairn onboarding task list: high-rigor-legacy preset. -->

# Onboarding tasks -- high-rigor-legacy

This file ships **one kind of content**: `[seed; id: <name>]`
lines, the day-one PLANNING entries. The scaffold inlines them into
`dev/PLANNING.md`'s `onboarding-tasks` slot at install time, and
nothing reads this file afterward.

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
  Try the `session-start` skill (`/session-start`): run
  `python tools/session.py session-start` to orient at the top of a
  session. The lifecycle routines are now invokable skills installed under
  `.agents/skills/`; the canonical doctrine is `doctrine/session-routines.md`.

* [seed; id: fill-readiness-report]
  Fill `templates/codebase-readiness-report.md` for your legacy
  tree BEFORE engaging the team apparatus. The eleven-section
  assessment surfaces hidden state, scientific assumptions, and
  security boundaries; the readiness scores decide how much of
  the apparatus to engage now (this profile, a smaller one, or
  reading the doctrine while gaps get fixed). Do not skip this; legacy codebases
  reward the pre-pass that greenfield does not need.

* [seed; id: confirm-maintainer-authority]
  Confirm the existing project maintainer's authority is
  reflected in `dev/agent_collaboration.md`'s `team-roster`
  slot. The legacy-codebase shape almost always has a de-facto
  Maintainer whose authority pre-dates the Cairn adoption; the
  apparatus should match the existing power structure, not
  invert it. A read from a different agent type is the Maintainer's call
  (`AGENTS.md` > Review); the usual review stays a fresh session.
<!-- cairn:if agent_team in concurrent-multi-type -->
  When you add another agent type, record it in the roster slot and walk
  `dev/modules/onboarding/agent-team-onboarding.md`.
<!-- cairn:endif -->

* [seed; id: read-security-review-module]
  Read `dev/modules/security-review.md`. The high-rigor-legacy
  preset installs the security-review module by default; legacy
  codebases carry security boundaries that the
  proposal-lifecycle's normal review does not necessarily
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

<!-- cairn:if agent_team in concurrent-multi-type,concurrent-single-type -->
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
<!-- cairn:endif -->

<!-- cairn:if agent_team in concurrent-multi-type -->
* [seed; id: agent-team-onboarding-legacy]
  Walk `dev/modules/onboarding/agent-team-onboarding.md` together. The
  high-rigor-legacy profile expects multi-agent staffing; the
  second agent type's capability tier should be calibrated
  against the security-review module's bar from day one.
<!-- cairn:endif -->

* [seed; id: walk-dev-tour]
  Walk `dev/modules/onboarding/dev-tour.md` as a final pre-engagement read; it
  carries the `dev/`-tree taxonomy + a worked example. After
  reading it, the team is ready to open the first proposal. Treat that
  first proposal as the diagnostic for calibrating the security-review,
  dual-language-tests and legacy-agent modules against your tree.

* [seed; id: walk-foldback-protocol]
  The fold-back practice: when the method itself improves, not
  just this legacy tree, that improvement belongs upstream.
  Notice it, then file a Cairn issue with the fold-back issue
  template (`.github/ISSUE_TEMPLATE/foldback.md`); the
  high-rigor-legacy profile installs the content-security scanner
  and the security-review checklist -- run `python
  scripts/content_scan.py` over the drafted filing body and walk
  the security-review checklist before it leaves the deployment.

<!-- cairn:if complexity in moderate,complex -->
* [seed; id: fill-model-selection-mapping]
  **Waiting on Maintainer**: fill the model mapping
  If `dev/.cairn/model-selection-mapping.yml` exists, ask the Maintainer which model
  family fills each tier (high, medium, low), record one row per tier (the family, never
  a version), and run `python scripts/check_model_selection.py`. Delete the Waiting line
  when it passes.
<!-- cairn:endif -->
