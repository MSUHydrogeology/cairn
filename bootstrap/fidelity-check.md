# fidelity-check.md — bootstrap verification design (R-H)

This document specifies the **fidelity-check**: the machine-readable
manifest contract that verifies a bootstrap installation is correct
and complete, and a reference manifest for the `modflow_tools` case
study at a pinned commit.

The fidelity-check answers: "Is what was installed what the profile
said should be installed?"  It is distinct from the R-F acceptance
gate (which answers "Is the installation structurally complete?").
The fidelity-check is reproducible — given the same manifest, the
same Cairn commit, and the same target state, it always produces the
same result.

---

## The manifest format

A fidelity manifest is a YAML file with the following structure:

```yaml
# fidelity-manifest.yml
# Generated at bootstrap time; committed to dev/strategy/ in the
# target repo alongside the accepted dimension profile.

cairn_commit: "<7-char cairn commit hash>"
target_repo: "<repo name or slug>"
bootstrap_date: "<YYYY-MM-DD>"

# Six-axis dimension profile
profile:
  age:         "<greenfield | legacy>"
  size:        "<small | medium | large>"
  complexity:  "<simple | moderate | complex>"
  language:    "<single | multi>"
  human_team:  "<solo | small-multi | large-multi>"
  agent_team:  "<single | concurrent-single-type | concurrent-multi-type>"

# Installed modules
modules:
  kernel:
    # The invariant kernel is always present; list the key artifacts.
    - AGENTS.md
    - dev/README.md
    - dev/PLANNING.md
    - dev/NEXT_SESSION.md
    - dev/collaboration_agreement.md
    - dev/agent_collaboration.md
    - dev/proposals/_template.md
    - dev/plans/_template.md
  default_on:
    # List the installed default-on modules (omissions must be justified).
    - lifecycle-metrics   # dev/modules/lifecycle-metrics.md
    - reflections         # dev/modules/reflections.md
    - claim-check         # dev/modules/claim-check.md
  team_gated:
    # List the installed team-gated modules (empty list is valid for
    # a minimal installation).
    - dual-review         # dev/modules/dual-review.md
    # - domain-agents
    # - legacy-agent
    # - dual-language-tests
    - coordination-tiers  # dev/modules/coordination-tiers.md

# Role roster derived from the profile
roles:
  - Human Maintainer
  - Strategy
  - Implementation
  - Internal Reviewer
  - External Reviewer

# Customization-slot status
#   "filled"   — the slot has project-specific content
#   "deferred" — intentionally left for a future session
#   "na"       — explicitly marked N/A with a reason
slots:
  - file: AGENTS.md
    slot: project-overview
    status: filled
  - file: AGENTS.md
    slot: project-conventions
    status: filled
  - file: dev/agent_collaboration.md
    slot: role-roster-additions
    status: filled
  - file: dev/agent_collaboration.md
    slot: coordination-additions
    status: filled
  - file: dev/collaboration_agreement.md
    slot: team-roster
    status: filled

# Deferred default-on modules (must give a reason for each omission)
deferred_default_on: []
# Example:
# deferred_default_on:
#   - module: reflections
#     reason: "Solo single-agent project; no cross-agent handoff surface needed."
```

---

## Running the fidelity check

The check is a manual audit against the manifest.  For each section:

### 1. Cairn-commit check

Verify that the templates installed match the Cairn commit recorded
in the manifest.  Run in the Cairn repo:

```
git show <cairn_commit>:templates/core/AGENTS.md | head -5
```

Compare with the installed `AGENTS.md` header.  If the project has
customized the file (filled slots, added conventions), the comparison
is to the template structure and placeholder locations, not verbatim
content.

### 2. Module presence check

For each entry in `modules.default_on` and `modules.team_gated`,
confirm the corresponding file exists in the target:

```
ls -1 <target>/dev/modules/
```

All listed modules must be present.  Any module in
`deferred_default_on` must not be present.

### 3. Slot status check

For each slot listed as `filled`, confirm the installed file
contains substantive content between the slot's open and close
markers — not the placeholder text from the template.

For each slot listed as `deferred`, confirm the placeholder text
is still present (so the deferral is visible and not silently
unfilled).

For each slot listed as `na`, confirm there is an explicit
`N/A: <reason>` between the markers.

### 4. Vendor-neutrality check

Run the lint from BOOTSTRAP.md Act II-5 against the installed
files.  Record the result (`pass` / `fail` with matches).

### 5. Token check

Run `grep -r '{{' <target>/AGENTS.md <target>/dev/`.  Zero matches
expected.

---

## Reference manifest — modflow_tools case study

This is the fidelity manifest for the `modflow_tools` project,
representing the Cairn installation that informed the methodology.
It is a *descriptive* manifest — the `modflow_tools` repo predates
the Cairn bootstrap procedure and was not installed by `scaffold.py`;
this manifest captures the equivalent state.

**Cairn reference commit**: `d152cbb`
(the commit at which the Phase 2 templates were finalized)

```yaml
cairn_commit: "d152cbb"
target_repo: "modflow_tools"
bootstrap_date: "2026-05-19"

profile:
  age:         "legacy"
  size:        "medium"
  complexity:  "complex"
  language:    "single"
  human_team:  "solo"
  agent_team:  "concurrent-multi-type"

modules:
  kernel:
    - AGENTS.md
    - dev/README.md
    - dev/PLANNING.md
    - dev/NEXT_SESSION.md
    - dev/collaboration_agreement.md
    - dev/agent_collaboration.md
    - dev/proposals/_template.md
    - dev/plans/_template.md
  default_on:
    - lifecycle-metrics    # tools/lifecycle_metrics.py; dev/strategy/ output
    - reflections          # dev/reflections/ channel
    - claim-check          # scripts/claim_check.py
  team_gated:
    - dual-review          # dev/agent_collaboration.md Internal + External tiers
    - coordination-tiers   # dev/intents/ asynchronous work-intent tier

roles:
  - Human Maintainer   # Anthony Kendall
  - Strategy
  - Implementation
  - Internal Reviewer
  - External Reviewer

slots:
  - file: AGENTS.md
    slot: project-overview
    status: filled
  - file: AGENTS.md
    slot: project-conventions
    status: filled
  - file: dev/agent_collaboration.md
    slot: role-roster-additions
    status: na    # minimal team; no domain-agent additions
  - file: dev/agent_collaboration.md
    slot: coordination-additions
    status: filled    # work-intent tier doc
  - file: dev/collaboration_agreement.md
    slot: team-roster
    status: filled

deferred_default_on: []
```

**Notes on the modflow_tools reference manifest**:

* `claim-check` is implemented as a project-local script
  (`scripts/claim_check.py`) rather than a copied module file; the
  module template describes the discipline, and the working
  implementation is in the script.  The fidelity check for
  claim-check confirms the discipline is documented and wired into
  the workflow, not that the module file is present verbatim.

* `coordination-tiers` is the asynchronous work-intent tier;
  the real-time tier is not yet installed (team size does not
  warrant it).

* The `dual-review` module is operative: the proposal and plan
  lifecycles in `dev/` record both Internal and External review
  rounds with structural independence (different agent types for
  External tier).

---

## When to update the manifest

Update the manifest (and commit it to `dev/strategy/` in the target
repo) when:

* A new module is installed.
* A module is removed.
* A slot status changes from `deferred` to `filled` or `na`.
* The Cairn reference commit is bumped (e.g., after a Cairn upgrade
  that adds new template content).

The manifest is a **living document** in the target repo, not a
one-time bootstrap artifact.
