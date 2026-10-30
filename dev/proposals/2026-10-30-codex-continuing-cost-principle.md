# Make cost a continuing design constraint

**Author**: Codex (runtime model identifier unavailable; Strategy / proposal author)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Make accumulated cost and human comprehension govern ongoing work, and close four concrete sources of review and evidence overhead.

## Context

The Maintainer reports growth during work, not merely poor initial choices:
review rounds, documents, code, duplication, model use and tests.
Issues #36–39, linked below, supply adopter reports, not independently
reproduced measurements.
`doctrine/rationale.md` already favors restraint, but `AGENTS.md` still demands
per-mutant accounting and permits open Security Reviews to repeat.
The hypothesis: local completeness wins while accumulated cost has no owner.

## Proposal

Replace the existing search/reuse paragraph in both `AGENTS.md` copies with
this operating principle and the revised reuse sentence below:

> **Cost and complexity.** Deliver the agreed outcome with the least total
> burden consistent with correctness, security, scientific validity and human
> comprehension. Count delivery and continuing costs: time, tokens, compute,
> attention and maintenance. Complexity includes concepts, indirection,
> coupling, state, duplication and obligations in code, prose and process;
> fewer lines or files need not mean less complexity.
>
> Authors and reviewers own the work their choices induce. Added burden must
> serve a present requirement or credible material risk better than a simpler
> adequate alternative. Reconsider a growing approach; stop when the outcome
> and required evidence are adequate. Do not trade readability for brevity.
> Optional improvements need not become follow-ups. This grants no permission
> to skip safeguards, weaken evidence, silently reduce agreed scope or refactor
> unrelated work. Routine choices require judgment, not additional records.
>
> **Reuse.** Search before building; reuse or adapt when it lowers total
> burden. Generalize for current responsibilities, not hypothetical extensions.
> Keep the existing requirement to name the search in the plan or commit.

Apply that principle through these replacements, not additional cost fields:

- **Models and remedies:** retain task capability floors and required
  escalation. Higher-tier use answers a specific uncertainty or failure, not
  blanket insurance. In the existing review sweep, replace mandatory
  generalization with the lower-burden adequate remedy; require reviewers to
  distinguish defects from optional improvements. Clear explanatory code may
  be longer. Test cases must protect distinct properties or consequential
  faults, not exhaustively enumerate tokens.
- **[#36](https://github.com/MSUHydrogeology/cairn/issues/36):** at most two
  Security Review passes per obligation without further Maintainer authority.
  The second reads the revision and affected interactions. If unresolved,
  stop and give the Maintainer the remaining findings; the obligation remains
  open until their recorded disposition. A third pass requires their word. Revisions and reviewer changes do not
  reset the count. Lowering the security capability floor still requires a recorded Decision.
- **[#37](https://github.com/MSUHydrogeology/cairn/issues/37):** trigger on a new
  or widened trust exposure, including changed guards, authority, sources or
  execution paths. Another file handled by unchanged reviewed readers/writers,
  or a guarded relocation with unchanged exposure, is not automatically a new
  boundary. Named high-risk triggers remain; identify the actual affected
  boundary, not merely its containing file. Challenge necessity in existing
  review reasoning, with no new skeleton field. Correct mistaken declarations
  explicitly; uncertainty about a real exposure is not clearance. Ordinary
  use of an unchanged boundary is not itself trust-ceremony work; apply
  bounded/wide verification to the changed behavior.
- **[#38](https://github.com/MSUHydrogeology/cairn/issues/38):** “A review record
  lives in its artifact or beside it, never in a separate reviews folder.”
  Keep append-only history and existing attribution requirements.
- **[#39](https://github.com/MSUHydrogeology/cairn/issues/39):** replace exhaustive
  narrative evidence with a readable result, reviewed commit and reproducing
  test/script/command. Mutation summaries retain the control, total and killed
  counts, and every survivor/equivalent with its reason; equivalence remains
  measured. Reproducible methods live in versioned owning tests/scripts.
  No per-killed-mutant table, probe ledger or pasted output in lifecycle prose.
  Commit bodies have a 30-line ceiling, normally wrapped; summary values are
  not raw logs. Preserve material failures, uncertainty and coverage gaps.

## Rationale

Cost is continuing, not prepaid by approval. Human traceability is a
correctness control. This does not equate brevity with simplicity or substitute
a summary for doing the work.

## Alternatives considered

Existing restraint alone leaves these explicit growth permissions intact.
Scores, quotas, mandatory cost reports and periodic audits add maintenance and
reward compressed prose/code. Removing review or verification loses assurance.

## Documentation / doctrine surface

Governing: both `AGENTS.md` files and both agent-collaboration files.
Reconcile the corresponding lifecycle/review/verification passages under
`doctrine/`, the proposal/plan templates and their shipped copies, and
`templates/modules/team-gated/security-review.md`; extend rationale anchor 17,
not a new doctrine home. Preserve headings/fields consumed by tools.
Prospective only: do not rewrite archives. No new runtime machinery.
The existing doctrine-evolution gate remains applicable; issue reports do
not establish its recurrence count or a high-risk exception.

## Evidence / verification plan

### Tests required

The plan maps existing readers, especially `test_review_stance_in_shipped_files.py`,
`test_review_sweep_ships.py`, `test_verification_boundaries.py` and
`test_stewardship_rules_ship.py` under `bootstrap/tests/`.
Reuse those families and installation coverage; test properties, not each word.
Keep prescribed protected-file ceremonies and separate certification.

### Examples / smoke checks

Run `python scripts/claim_check.py`, scoped `python scripts/check_cairn.py`
and neutrality/redundancy sub-gates of `scripts/quality_gate.py`.
Reviews challenge the policy using an unnecessary abstraction,
an unreadable shortcut, a harmless new-format-instance and an unresolved
second security pass. No separate cost review or recurring measurement.

#### Security preflight

S1: authors classify exposure; reviewers challenge it; only the Maintainer
disposes unresolved security risk. Candidate claims are not proof.
S2: no new executable policy checker is claimed; prose tests cannot prove
sound judgment. Implementation checks must catch removed safety qualifiers.
S3: existing review stages apply these rules; no automatic enforcement promised.
S4: stopping repetition leaves unresolved work open, never passed.
S5: mistaken/colluding judgments remain possible; this is not authentication
or containment.

### Independent scientific check

N/A: no scientific assumption or result changed.

## Signals the change is wrong

More justification prose appears; unsafe exposure is called relocation;
survivors disappear into counts; humans cannot reconstruct the work;
or the Maintainer still routinely stops unjustified growth.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — governing doctrine and security-review rules.
