# Clarify the pending tree-certification label

**Author**: Codex GPT-6.1
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Explain that pending tree certification does not mean a completed change needs another run now.

## Context

Issue #33 asks for scoped certification and a separate whole-suite check: the
label `Certified by: pending` can imply a full run is owed for every change.
The scoped-verification proposal and archived plan already distinguish the
change's Boundary B checks from tree certification. `AGENTS.md` retains the
pending label, while `doctrine/plans.md` says the later tree run is separate.
The decision master records the remaining terminology question. This is a
reported reading problem, not measured evidence of how often people misread it.

## Proposal

Keep the existing label, checks, triggers and certification meaning. Beside the
first instruction to record `Certified by: pending`, say that it tracks whether
a later authorized tree-certifying run covers the commit; it is not an unmet
change check or a request to run the whole suite now. A missing required change
check still keeps the work open. Apply that explanation consistently to the
self-hosted and installed governing rules, both plan templates,
`doctrine/plans.md`, and `docs/glossary.md`; retain the later append-only
certification entry and leave historical records unchanged. Preserve conditional
push, release, re-anchor and Maintainer-request triggers. Do not add scripts,
documents, generic model simulations, new review stages or evidence ledgers.

## Rationale

An adjacent explanation addresses the misleading to-do without changing a
recognized field or claiming scoped checks certify the whole tree. The existing
scope and trigger rules remain authoritative. Shipped templates are a protected
surface, so heavy review applies despite the small wording change.

## Alternatives considered

Rename or remove the field: this may read more naturally, but would require
changing consumers and reconciling older records. Redefine certification as
scoped checks: that answers the issue literally but changes an established
whole-tree claim. Make no change: lowest cost, but leaves the reported ambiguity
at the point readers encounter the label. The Maintainer may prefer that cost.

## Documentation / doctrine surface

Prescription belongs in `AGENTS.md` and `templates/core/AGENTS.md`; the plan
templates and `doctrine/plans.md` carry the corresponding record guidance.
`docs/glossary.md` describes the term. This proposal is deliberation in `dev/`.

## Evidence / verification plan

### Tests required

Search live readers, shipped copies, byte pins and actual triggers before
implementation. Existing `bootstrap/tests/test_certifying_run_rule.py` checks
for `Certified by` and the conditional push guard; `bootstrap/tests/test_verification_boundaries.py`
checks record vocabulary and both plan templates. Run mapped owners and installed
copy checks as selected by `tools/test_tiers.py`, including any additional
readers found. Do not change protected `bootstrap/tests/conftest.py`: its broad
run refusal already explains that tree certification is separate. If a required
consumer cannot accommodate the explanation without changing a protected file,
stop and reassess scope. Preserve all required checks and the independent review.

### Examples / smoke checks

Run claim, link, snippet and neutrality gates applicable to the changed prose.
Review the actual wording in both governing copies and templates: a reader should
be able to finish a change with all required checks passed while tree
certification remains pending. No whole-suite run is authorized by this proposal.

#### Security preflight — five questions, answered in writing

S1: A human records Boundary B results and the later certifying SHA from the
actual runs; the wording adds no deciding input or channel. S2: The existing
rule tests detect removal of named obligations; a changed-obligation mutation
has not been run for this proposal and must be assessed during implementation.
S3: Mapped pytest owners select the live rule surfaces; the prose gates check
changed documents. The statement above promises clarification, not automated
proof of reader comprehension. S4: No parser, default or fallback changes;
existing failed or missing checks still block completion. S5: A misleading
record or a reader misunderstanding the distinction can still succeed; wording
cannot authenticate a run or guarantee comprehension.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Withdraw or revise if the wording implies that a required check may be skipped,
changes an authorized certification trigger, conflicts with an actual consumer,
or the clarification costs more than the ambiguity warrants.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance. The proposed changes touch governing
doctrine and shipped authoring templates; no new trust boundary is intended.
