# fidelity-check.md — bootstrap verification design (R-H)

<!-- vendor-ok-begin: this doc documents the fidelity-check practice with modflow_tools as the named case-study reference; the cites are legitimate doctrine, not vendor leak -->
This document specifies the **fidelity-check**: the machine-readable
manifest contract that verifies a bootstrap installation is correct
and complete, and a reference manifest for the `modflow_tools` case
study at a pinned commit.
<!-- vendor-ok-end -->

The fidelity-check answers: "Is what was installed what the profile
said should be installed?"  It is distinct from the R-F acceptance
gate (which answers "Is the installation structurally complete?").
The fidelity-check is reproducible — given the same manifest, the
same Cairn commit, and the same target state, it always produces the
same result.

## Core folder set (upstream/, rules/, strategy/)

As of the `core-dev-folder-set` proposal, three additional folders ship
default-on in every fresh scaffold: `dev/upstream/` (external-dep issue
drafts), `dev/rules/` (project-owned agent-discipline detail), and
`dev/strategy/` (Stage-0 exploration notes). Each carries a `README.md`
as the single source of lifecycle truth; `upstream/` and `strategy/` also
carry a `_template.md` and a tracked `archive/` (the `.gitkeep` in
`upstream/archive/` materializes the dir at adoption). These are
**customization-expected** files — a 3-way merge on upgrade — but they are
**tamper-detectable**: an adopter edit is surfaced by `verify_integrity` until
`upgrade --finalize` advances the hash, the same mechanism as `AGENTS.md` (they
are **not** living-state like `dev/PLANNING.md`, which is exempt from the check). A
fidelity check for the core folder set: confirm these files exist in the
installed target:

```
ls dev/upstream/README.md dev/upstream/_template.md dev/upstream/archive/
ls dev/rules/README.md
ls dev/strategy/README.md dev/strategy/_template.md dev/strategy/archive/
```

## The loop-fidelity gate (implementation→adoption)

A second, *pre-ship* fidelity check guards the **implementation→adoption**
checkpoint of the fold-back loop: the `check_cairn` self-check fails closed when
an **adopter-facing surface** (a `templates/` file the bootstrap install set
copies) references a **Cairn-internal-only path** (`doctrine/*`) that is neither
transplanted into the install set nor marked a deliberate citation. When run:
`python scripts/check_cairn.py` — at review time, and in the **maintainer-run**
release checklist (`bootstrap/security_check.py` invokes it, when a maintainer
runs that). Such a reference resolves in the Cairn source tree (so the generic
`link_check` passes it) but **dangles once installed** in an adopter — the
failure that produced fold-back #57 and the un-shipped 9-lens review roster.
The lens scans both backticked path tokens and raw Markdown link targets; a
deliberate deeper-why citation is exempted with a
`cairn-internal-ref-allow: <paths…>` (or `cairn-internal-ref: <paths…>`) marker
that names the specific path, so a *new* unlisted reference still fails closed.
This is the automatable flagship of the loop-fidelity discipline whose doctrine
home is [`doctrine/lifecycle.md`](../doctrine/lifecycle.md) > "Loop-fidelity
verification". <!-- cairn-internal-ref: doctrine/lifecycle.md reason=deeper-why pointer; fidelity-check.md is bootstrap-internal, not an installed adopter surface -->



## Relationship to the machine lockfile (`dev/.cairn/cairn-lock.yml`)

Once a tree is installed (or upgraded) with an upgrade-capable Cairn, it
also carries a **machine lockfile**, `dev/.cairn/cairn-lock.yml` (see
[`UPGRADE.md`](UPGRADE.md)). The two are **one-way**, not two competing
sources of truth:

* The **lockfile is the machine authority** for *what is installed* — the
  per-file source / destination / hash, the module roster, and the
  substituted token values. It is tool-owned (regenerate-only) and is the
  ancestor the `upgrade` 3-way merge reads.
* This **fidelity manifest is the human audit narrative** — the
  reproducible, reviewer-facing record of profile + slots + deferrals. It
  **cites** the lockfile's `cairn_version` / `cairn_commit` rather than
  re-listing the file/module inventory the lockfile already owns. It lives in
  **`dev/.cairn/`** beside the lockfile: both are Cairn adoption state (the
  lockfile machine-owned, the manifest human-readable), so they co-locate in the
  adoption-state home rather than scattering across `dev/`.

So the manifest does not need to carry merge state, and the two cannot
drift into disagreement over a second parsed inventory. The `upgrade`
command validates that the manifest's citation matches the current
lockfile and warns if it is stale. (A pre-lockfile tree has only this
manifest until `upgrade --init-lock` synthesizes a lockfile.)

### Scaffolded-script re-sync cadence (fold-back #35)

A shipped **verbatim script** (`claim_check.py`, `intent.py`,
`lifecycle_metrics.py`, `link_check.py`) drifts silently when upstream
evolves and the adopter never re-checks — an adopter pulls a scaffolded
script forward only when it happens to look. (Observed: an adopter's
`claim_check.py` forked well behind upstream's exemption-directive support
and was only noticed when a cross-type review referenced the newer API.)

The detection **mechanism already exists** — it does **not** need building:
the lockfile hash-tracks every verbatim script, and `upgrade` flags a
drifted/forked one and does **not** clobber it (see
[`UPGRADE.md`](UPGRADE.md) > "Verbatim scripts use a hash check"). What was
missing is the **cadence**: run `upgrade` on a recurring schedule —
paralleling the doctrine-harvest cadence (`doctrine/rationale.md`) — so
script drift surfaces before it compounds. A natural moment is a periodic
goodnight or a release-prep pass; a pre-lockfile tree runs
`upgrade --init-lock` once first.

The benefit is gated on the adopter actually carrying the upgrade
machinery: a tree bootstrapped before upgrade support (no lockfile) gets
nothing from the hash-check until it runs `upgrade --init-lock`. So for
such a tree, adopting the upgrade
apparatus *is* the fix for #35, not a step alongside it.

---

## The manifest format

A fidelity manifest is a YAML file with the following structure:

```yaml
# fidelity-manifest.yml
# Generated at bootstrap time; committed to dev/.cairn/ in the target
# repo alongside the lockfile + the accepted dimension profile.

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
  - Reviewer
  - Security Review
  - User Agent

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

**Profile-conditional regions (`cairn:if`).** The core `AGENTS.md`
template (and any future core template) may carry
`<!-- cairn:if AXIS in val1,val2 -->` … `<!-- cairn:endif -->`
regions that are resolved by the installer using the lockfile's
embedded `profile.axes`.  An auditor comparing the raw template
against the installed file will see sections absent from the install
— this is correct and expected, not a gap.  To reproduce the
expected installed content, apply the strip with the profile's axes
(the `strip_conditional_regions` function in
`bootstrap/_scaffold/config.py`).  The strip runs consistently at
**every** materialization point (install, lockfile expected hash, and
the 3-way merge ancestor/`theirs` sides), so the lockfile's recorded
hash matches the *stripped* installed file for any given profile —
meaning `verify_integrity` stays consistent without code change.

The gated set is conservative and auditable: the **never-gate-a-bright-line
rule** holds that no IR1–IR13 safety rule (Git workflow, lifecycle,
review, verifying claims, session routines, roles) may ever be wrapped
in a `cairn:if` region.  Currently the only gated section in the core
`AGENTS.md` template is `## Human contributors` (`human_team in
small-multi,large-multi`), which is informational to a solo maintainer
who ships no `CONTRIBUTING.md`.  The test suite asserts this constraint
so an auditor can trust that a stripped install never omits a
bright-line rule.

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

**Optional-template slots count too.** An installed optional template
(an `optional_templates:` entry) carries block slots like any other —
e.g. `contributing-specifics` in `CONTRIBUTING.md`. Audit those slots
the same way, and let the entry's `status:` reflect them: `filled`
once the project's contributor specifics are written, `deferred` while
the placeholder stands (a visible deferral), `na` with a reason if the
section does not apply. An unfilled optional-template slot is a review
finding, exactly as for a core slot.

### 4. Vendor-neutrality check

Run the lint from BOOTSTRAP.md Act II-5 against the installed files —
**scoped to the doctrine / template files** (it excludes
`dev/proposals/` and `dev/plans/`, where Reviews / Responses /
Decisions name their reviewer for attribution).  Record the result
(`pass` / `fail` with matches), treating the three sanctioned classes
as allowed, not findings: deliberation-artifact attribution, filename
citations, and the `CLAUDE.md` vendor-addendum reference.

**Vendor-wrapper drift note.** If the adopter installed the thin
wrapper (`VENDOR.md`, renamed to the tool's file), confirm it stayed
thin: it should open by importing `AGENTS.md` (`@AGENTS.md`) and carry
*only* harness-specific habits. A wrapper that has grown to duplicate
canonical `AGENTS.md` content — the test command, the git rules, the
session routines, the required-reading list — has drifted into a fat
fourth doc; flag it to fold the duplicated content back to its single
source (`AGENTS.md` > "Vendor addendum").

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

### 6. Core-completeness probe

Steps 1–5 prove a **faithful install** — what was installed matches the
manifest. This step asks the question the fidelity gate is structurally
blind to: is the install **doctrine-complete**? It is bounded — **by
hard constraint** — to **exactly two** checks, and is **never a code
audit**: it does not evaluate the project's codebase quality, science,
test coverage as software health, performance, or maturity. If a check
here drifts toward the *software*, it is out of scope by construction.

**6a — Module-merge completeness (a faithfulness backstop).** For each
installed module, confirm its `Adds to:` content is actually present in
the target. The default-on merge targets are `cairn:slot`-marked, so
step 3 and the R-F unfilled-slot gate already cover them; this check's
**residual** is the **team-gated** modules, which merge their `Adds to:`
content into **prose** sections — `dual-review` into the review-loop
prose, `issue-capture` into the User Agent role note, `coordination-tiers`
into the coordination section — *not* into slots, so nothing else
verifies they landed. For each installed team-gated module: (1) read
its `Adds to:` line to **resolve the destination** — it names a target
*file* and a *location* within it (a section, a role-roster entry, a
note); the phrasings differ across modules (`dual-review` →
"the review section of `dev/agent_collaboration.md`";
`dual-language-tests` → "a `tests/` guide in the adopting repository"),
so resolve to the concrete file + place rather than matching a fixed
string; (2) confirm the module's **distinctive content** is present
there — the role's responsibilities, the rule the module adds — not
merely that the section exists. A declared-but-absent merge is a
finding. (This is faithfulness, not completeness — it strengthens the
gate; 6b is the novel axis.)

**Body-coverage dimension (the stub-subsets-the-body trap).** When a
module's stem matches an upstream `doctrine/<stem>.md`, the module file
is a kernel-merge *subset* of that doctrine body — so the "distinctive
content" to confirm is the **doctrine body's** load-bearing topics
reaching the adopter's live surfaces, **not** merely the module's own
short `Adds to:` stub. A stub that silently dropped a doctrine-body
topic (as happened with `dual-review`'s clean-pass-trap,
briefs-don't-telegraph, and restricted-verification content) otherwise
passes 6a unnoticed — the check is blind to body content the stub
never carried. For a module with **no** same-stem `doctrine/` file,
this dimension is skipped with an informational note. This sharpens
*what* "distinctive content" means; it is **not** a third step — the
two-check hard constraint holds.

**Mechanized.** The body-coverage dimension ships as
`bootstrap/check_module_body_coverage.py` (stdlib-only; same-stem
matching; a loose-substring heading-name proxy; graceful-fail on a
missing source). Run it from the adopter tree against a Cairn checkout:

    python <cairn>/bootstrap/check_module_body_coverage.py --target .

It flags, per installed module with a same-stem `doctrine/<stem>.md`,
the doctrine-body headings absent from the module file and the
kernel-fold target — the 6a body-coverage check, automated. It is a
**heading-name proxy, not semantic coverage** (it catches "topic named
upstream, absent from the adopter"; a paraphrased fold can false-flag),
so treat its output as a prompt for the 6a judgment, not a gate.
*Follow-up:* standardizing every module's `Adds to:` line to a
`<file> > <section>` shape would let the same mechanization cover the
merge-completeness dimension too — a fair harvest/fold-back candidate.

**6b — Tacit-rule capture (the completeness probe proper).** The novel
check: are operating rules the team follows *in practice* written into
`AGENTS.md`, or left tacit? Read `AGENTS.md` against how the team
actually works and flag operating doctrine that is lived but unwritten —
a commit habit everyone follows, a review step taken but not stated, a
coordination rule held only informally. This is a **doctrine-completeness**
judgment — capture of *rules*, never an audit of the *code*. A lived
rule absent from `AGENTS.md` is a finding; its fix is to write it down,
and if it generalizes, to carry it upstream as a fold-back.

Record the result (`pass` / findings). This adopter-side probe pairs
with the framework-side **doctrine harvest**
(`../doctrine/rationale.md` > "The reference-instance doctrine
harvest"): the harvest keeps *core* from lagging its best adopter;
this probe keeps an *install* from silently shipping incomplete.

---

## Reference manifests

<!-- vendor-ok-begin: case-study reference list; the modflow_tools cite is legitimate doctrine -->
Project-specific reference manifests live alongside their case
studies, not in `bootstrap/`.  The current reference is:

* `modflow_tools` — see
  [`../case-studies/modflow_tools-fidelity-manifest.yml`](../case-studies/modflow_tools-fidelity-manifest.yml).
<!-- vendor-ok-end -->

Keeping `bootstrap/` project-neutral mirrors the R-G vendor-neutral
discipline in spirit: project-name leak is not as serious as
vendor-name leak, but it is the same shape of structural violation.
A fidelity manifest is a *case-study artifact*, not a bootstrap
artifact.

---

## When to update the manifest

Update the manifest (and commit it to `dev/.cairn/` in the target
repo) when:

* A new module is installed.
* A module is removed.
* A slot status changes from `deferred` to `filled` or `na`.
* The Cairn reference commit is bumped (e.g., after a Cairn upgrade
  that adds new template content).

The manifest is a **living document** in the target repo, not a
one-time bootstrap artifact.
