# Plan: Person-facing documentation

**Source proposal**: `dev/proposals/archive/2026-11-08-terra-person-facing-documentation.md`
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-09
**In brief**: Make upgrade and session journeys usable through conversation while retaining agent duties in their authoritative homes.

## Build summary

Give people discoverable, accurate upgrade and session examples; audit the
existing documentation for misplaced agent instructions; and put an audience
judgment in the existing author and reviewer work. This addresses Issues #56
and #57 without a new automatic checker or a human trial prerequisite.

## Source proposal

The accepted person-facing documentation proposal, Decision `93be78b8`,
requires both journeys, the complete docs and upgrade audit, preservation and
discovery of installed duties, and the author/reviewer audience judgment. Its
usual and Security Reviews identify applicable home, clean-merge, manual skill,
and permission constraints. It authorizes no substantive new policy or checker.

## Scope

Audit the following finite committed pages, plus `bootstrap/UPGRADE.md`. The
list is the current `docs/` Markdown and HTML page set; assets are illustrations,
not pages. Reconcile any pages added before the audit against this set.

- `docs/`: `DOCUMENTATION_PLAN.md`, `README.md`, `agent-team-onboarding.md`,
  `build-a-board-view.md`, `code-map.md`, `dev-tour.md`, `further-reading.md`,
  `getting-started.md`, `glossary.md`, `index.html`, `plain-language.md`,
  `quickstart.md`, `related-practices.md`, `release-process.md`,
  `skills-compatibility.md`, `solo-legacy-recipe.md`, `tool-usage.md`,
  `vision.md`, `workflow-role.md`.
- `docs/methodology/`: `README.md`, `collaboration-stance.md`,
  `consolidation-review.md`, `coordination.md`, `doc-governance.md`,
  `dual-review.md`, `lifecycle-contract.md`, `lifecycle.md`, `onboarding.md`,
  `plans.md`, `proposals.md`, `rationale.md`, `roles.md`, `runtime-contract.md`,
  `session-routines.md`.

Read each page in context for agent-directed instructions and procedures lacking
a person-level decision. Record each page's disposition and each candidate's
applicability, current authority, outcome and, if moved, installed destination
and discovery route. Retain domain-local governance, technical how-to and
methodology explanation where appropriate; an imperative alone is not a reason
to move it. Preserve the complete upgrade operational reference and safeguards.
Resolve conflicts against current authoritative sources. A newly found policy
or trust-boundary change stops for reassessment.

Use `docs/README.md`, `docs/quickstart.md`, `docs/getting-started.md` and
`docs/tool-usage.md` as the first journey homes; assess fit before editing and
add a short page only if reuse obscures the journey. Compare examples against
`bootstrap/UPGRADE.md`, `templates/skills/session-start/SKILL.md` and
`templates/skills/session-end/SKILL.md` and actual tool availability.

**Reuse:** N/A: no code added. The existing index already links the upgrade
reference, quickstart defers session routines, and tool usage describes the
underlying commands; reuse these pages rather than create parallel references.

### Documentation / doctrine surface

Patch `docs/DOCUMENTATION_PLAN.md` and
`templates/modules/default-on/documentation_plan_template.md` for the audience
boundary. Put the author and ordinary-reviewer judgment at their existing
operative entry points in `AGENTS.md` and `dev/agent_collaboration.md`, with
corresponding installed sources and discovery routes verified during audit.
`docs/` describes; installed doctrine and applicable skills carry duties. An
optional module or skill cannot alone carry a cross-cutting duty. Keep slot and
copy correspondence. No new rule beyond the accepted audience judgment or
change to permissions, upgrade semantics, or skill behavior is authorized.

## Sequence

All inputs and authority for this outcome are available now. Estimate two to
four working days including review and verification; corpus findings, paired
install surfaces and review availability make the estimate uncertain, not a
cutoff. No calendar observation, release ceremony or human trial is a plan
prerequisite.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | High: audit the listed corpus and authoritative homes; record dispositions and trace the documentation-change trigger and reviewer entry point. | Reviewed plan | Audit evidence and exact implementation mapping; stop for substantive policy or boundary changes. |
| C2 | Medium: write the two journeys, boundary and audience judgment in existing homes; Low may execute fully specified exact patches after C1. | C1 mapping and current sources | Reviewed documentation and paired installed guidance, preserving all duties and safeguards. |
| C3 | Fresh independent agent: walk both journeys from index and getting-started, and challenge the judgment with the seeded case. Implementation author records checks; independent ordinary and Security code reviews follow. | C2 committed | Usability evidence, review responses and final wide Boundary B on clean commit. |
| C4 | Record issue-specific resolution for #56 and #57 at their fixing commit after owed reviews and checks; update applicable roadmap and changelog at their serialization points. | C3 complete | Both issue closure work items and durable links; archive under existing rules. |

## Acceptance criteria

- C1 records every page in the finite set and every candidate's contextual
  disposition. For moved duties it demonstrates applicable installed authority
  and discovery, including cross-cutting coverage across profiles.
- C2 gives a discoverable upgrade journey from index and getting-started:
  when to consider it, an example request, staged review, clean merges and
  conflicts, person decisions and approvals, and the operational reference.
  It also gives worked session-start and session-end requests, outputs and
  decisions, including Decisions, tier, scope and push where relevant. It
  accurately states manual invocation, reflection-only end, untrusted next
  note and separate push authority. No safeguard or operative duty is lost.
- C2 places a documentation-change audience judgment for authors and, when
  review applies, ordinary reviewers where their existing duties are actually
  encountered. Trace each trigger and reader; optional drift automation alone
  is insufficient. No automated gate is added.
- C3's fresh independent agent follows both journeys from both entry points,
  reports the expected response and human decisions, and compares them to the
  actual sources. Seed a misplaced agent duty in a disposable audit sample;
  the audience judgment must identify it, and a person-facing example must
  not be misclassified. Record the method and result. An unreachable journey,
  missed seed, lost safeguard or invented approval fails the outcome.
- C4 names #56 and #57 separately, links each to its fixing commit and durable
  documentation, and completes the applicable issue closure work after checks
  and reviews. A later release is not the fixing event.

**Security preflight changes:** S2's seeded candidate and person-facing control
run in C3; the negative control is prospective, not yet measured. S3's C1 trace
identifies the actual author and reviewer entry points and installed readers;
C3 tests the trigger in context. Other proposal answers remain unchanged.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: under `/Users/kendal30/conda_envs/lhm/bin/python3.13`, run
`python tools/test_tiers.py for <changed paths>` before editing and its selected
tests while iterating; search direct readers, byte pins, slots and installed
consumers and record mapping and omissions. For changed `AGENTS.md` include the
reviewed range as the selector requires. Run claim checks on each document,
`python scripts/check_cairn.py`, `python scripts/link_check.py`,
`python scripts/sync_doc_snippets.py` on changed documents, and
`python scripts/quality_gate.py --sub neutrality`. Test negative searches
against a known positive. Run applicable install and upgrade fidelity paths for
changed installed sources, identified by the mapping; do not silently omit a
required check. Functional prose uses exact patches and records deliberate rule
changes in commit bodies.

Boundary C: independent ordinary and Security reviewers read the committed
implementation and iteration evidence and run tight falsification checks,
including journey and installed-duty evidence, without a suite. Fix findings
under the existing review rules.

Boundary B: after reviews and fixes, run wide on a clean, unchanged final
commit using canonical Python 3.13.x: the reviewed-range iteration selection,
matching tier-map integration/workflow paths, prose gates and C3 acceptance
checks. Record SHA/range, interpreter, pre/post state, commands, counts, elapsed
time, omissions and non-pass dispositions in the implementation record. Full
tree certification remains a separate authorized ceremony.

## Plan review -- GPT-6.1 Terra (Medium) -- 2026-11-09

**Reviewed commit:** `15242ca3`. **Obligation:** Internal.
**Verdict:** ACCEPT; no blocking findings. **Elapsed:** about 5 minutes.
**Tokens:** unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the finite audit, two journeys,
   installed-duty tracing and author/reviewer judgment cover the accepted
   outcomes while preserving safeguards and stopping policy changes -- Scope
   and Acceptance criteria; accepted proposal, Decision `93be78b8`.
2. **Best alternative.** Links alone would be cheaper but leave the audit and
   audience judgment undone; reuse of existing pages with a new page only when
   needed is the simpler path that retains those outcomes -- Sequence C1–C2;
   proposal Alternatives considered.
3. **What would show it wrong?** Walk both routes from both entry points and
   test the seeded duty and person-facing control; an unreachable journey, lost
   duty, missed seed or invented approval would falsify delivery -- C3 and its
   acceptance criterion.

C1 assigns the contextual design and exact mapping to High before Medium
writes, and Low is limited to fully specified patches. The plan preserves
existing functional rules and requires tracing each moved duty to applicable
installed authority; the actual corpus audit remains implementation work.

**Coverage:** Read the committed plan, accepted proposal and plan template,
including sequence, criteria and verification. Did not audit the corpus, run
implementation checks, verify installed profiles or perform Security Review.

## Plan review -- GPT-6.1 Sol (High, Security Review) -- 2026-11-09

**Reviewed commit:** `15242ca3`. **Obligation:** Internal Security Review.
**Model:** gpt-6.1-sol (High). **Verdict:** ACCEPT; no blocking findings.
**Elapsed:** about 6 minutes. **Tokens:** unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the plan preserves the accepted
   journeys and audit while requiring applicable installed authority, discovery
   and reassessment for policy or trust-boundary changes -- Scope,
   Documentation / doctrine surface; proposal Decision `93be78b8`.
2. **Best alternative.** Reuse the existing entry pages and operative homes,
   as planned; links alone cost less but cannot deliver the accepted audit or
   author/reviewer judgment, and a new checker adds unauthorized maintenance --
   Scope; C1–C2; proposal Alternatives considered.
3. **What would show it wrong?** C3 must walk both journeys from both entry
   points, compare actual sources, and distinguish the seeded duty from the
   person-facing control; a missed seed, lost installed duty or invented
   approval falsifies delivery -- Acceptance criteria; Security preflight
   changes.

The upgrade reference distinguishes clean text merges from semantic agreement,
retains staged review and protects saved ancestors; the plan preserves the
complete reference and forbids changing upgrade semantics --
`bootstrap/UPGRADE.md`, opening and review-only gate; Scope. Session examples
must retain manual invocation, reflection-only end, untrusted notes and separate
push authority, matching `templates/skills/session-start/SKILL.md` and
`templates/skills/session-end/SKILL.md`.

C1 assigns contextual routing and exact mapping to High. C2 permits Low only
fully specified patches, leaving no audience or authority design to execution.
The cross-cutting-duty clause prevents an optional documentation module from
becoming its sole home; installed-reader and fidelity evidence remain owed.
C4 closes each issue at its fixing commit after assurance, without a release
prerequisite. No existing rule is authorized to weaken or disappear.

**Coverage:** Read the committed plan, accepted proposal, plan template,
review stance, upgrade safeguards, session skills and documentation routing
sources. Confirmed the listed page set against the committed tree. Did not
audit page contents, walk implemented journeys, execute installs or run
implementation checks; those remain implementation evidence.

## Plan review response -- GPT-6.1 Terra -- 2026-11-09

Ordinary review `c260bfcc` and Security Review `9a3bd4a8` both accept without
findings. The plan is ready to implement with its assigned capability floors:
High maps audience/authority boundaries, Medium writes the journeys, and Low
may execute fully specified patches. Both issue closures, agent journey checks,
installed-duty preservation, code reviews and final verification remain owed.
No human trial or scheduled Maintainer action is a completion prerequisite.
**Elapsed:** about two minutes. **Tokens:** unknown.
