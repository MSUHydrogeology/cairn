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

# Deferred command-tokens: an inline {{token}} legitimately left
# unfilled (a command whose script the adopter has not supplied yet).
# Each needs a reason; the token check (step 5) exempts these, so a
# deliberate deferral does not read as a dropped substitution.
deferred_tokens: []
# Example (the `module:` key ties the token to the module that owns
# it, for traceability — match the `deferred_default_on` pattern):
# deferred_tokens:
#   - token: test_command
#     module: <owning module, or omit for a kernel-level token>
#     reason: "Greenfield repo; no test suite yet."
#   - token: claim_check_command
#     module: claim-check
#     reason: "claim-check installed; reference script not yet adopted."

# Optional top-level templates installed beyond the kernel + modules
# (e.g. CONTRIBUTING.md), each with the dimension axis + value that
# selected it.  Recording the gate here makes the selection auditable:
# a reviewer can confirm the installed optional file matches the
# profile's axes.  Empty when the profile selects none (e.g. a solo
# maintainer installs no CONTRIBUTING.md).
optional_templates: []
# Example:
# optional_templates:
#   - file: CONTRIBUTING.md
#     gate: "human_team in {small-multi, large-multi}"
#     status: filled   # filled | deferred | na (same vocabulary as slots)
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

For each entry in `optional_templates`, confirm the named top-level
file (e.g. `CONTRIBUTING.md`) exists in the target **and** that its
recorded `gate` matches the profile's axes — the gate is what makes the
optional install auditable.  A profile whose axes select no optional
template carries an empty `optional_templates: []`.

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

Run the lint from BOOTSTRAP.md Act II-5 against the installed files —
**scoped to the doctrine / template files** (it excludes
`dev/proposals/` and `dev/plans/`, where Reviews / Responses /
Decisions name their reviewer for attribution).  Record the result
(`pass` / `fail` with matches), treating the three sanctioned classes
as allowed, not findings: deliberation-artifact attribution, filename
citations, and the `CLAUDE.md` vendor-addendum reference.

### 5. Token check

Run `grep -r '{{' <target>/AGENTS.md <target>/dev/`.  Every match must
be one of:

* a **document-author placeholder** kept unfilled by design —
  `{{Maintainer}}`, `{{author}}`, `{{reviewer}}` in the proposal
  template, `{{assessor}}` in the phase-0 templates;
* a token listed in the manifest's **`deferred_tokens:`** block (each
  with a reason) — a legitimately deferred command-token whose script
  the adopter has not supplied yet.

Any other `{{...}}` is an unfilled-token finding. (The deferral is an
adopter audit convention, not an automated gate: neither `scaffold.py`
nor `check_cairn.py` parses or acts on the `deferred_tokens:` block.
`scaffold.py` installs templates and does not read the manifest;
`check_cairn.py` is Cairn's *self*-check over template source, which
carries `{{tokens}}` by design — so the token check is run **by the
adopter, against the installed target**, not by Cairn's tooling over
Cairn's own tree.)

---

## Reference manifests

Project-specific reference manifests live alongside their case
studies, not in `bootstrap/`.  The current reference is:

* `modflow_tools` — see
  [`../case-studies/modflow_tools-fidelity-manifest.yml`](../case-studies/modflow_tools-fidelity-manifest.yml).

Keeping `bootstrap/` project-neutral mirrors the R-G vendor-neutral
discipline in spirit: project-name leak is not as serious as
vendor-name leak, but it is the same shape of structural violation.
A fidelity manifest is a *case-study artifact*, not a bootstrap
artifact.

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
