# Edit list: one round of review at each stage

Companion to `dev/plans/2026-11-20-one-round-reviews.md`, which says why this file exists and how to apply it. Each edit gives the exact text to find and the exact text to put in its place. A `Find` block occurs exactly once in every target named for it (checked at `849eab4c`). Copy it byte for byte; a line break inside a block is a real line break. Shipped twins get the identical replacement.

## C1: governing text (`AGENTS.md` pair, collaboration guide pair)

### A1

Targets: `AGENTS.md`; `templates/core/AGENTS.md`

Find:

```text
Each review is one pass; add a second only for widened scope (proposal) or new defects (code). Security Review takes at most two passes. A further pass needs the Maintainer's explicit authorization and a specific unresolved security question; each later pass needs new authorization. At a cap, send only unresolved blocking findings or unmet accepted checks to the Maintainer.
```

Replace with:

```text
Each review stage is one round: one usual pass and, where the tier requires it, one Security Review pass. A blocking finding states what closes it: a failing test for code, exact words for a document. A further pass needs scope the Maintainer added, a substantive plan amendment, or the Maintainer's explicit authorization and a specific unresolved security question; each later pass needs new authorization. At a cap, send only unresolved blocking findings or unmet accepted checks to the Maintainer.
```

### G1

Targets: `dev/agent_collaboration.md`; `templates/core/dev/agent_collaboration.md`

Find:

```text
A fresh reviewer, not the author, reads a committed version. One review stance applies
```

Replace with:

```text
A fresh reviewer, not the author, reads a committed version, with one exception (scope the Maintainer adds, below). One review stance applies
```

### G2

Targets: `dev/agent_collaboration.md`; `templates/core/dev/agent_collaboration.md`

Find:

```text
Clean work and closed findings advance without a clearing review.
```

Replace with:

```text
Clean work and closed findings advance without a clearing review.

**Closing a blocking finding.** A reviewer who blocks code writes a failing developmental test (scratch work, deleted before archive) into the review, with its command and two or three cases where input regimes differ. The implementer runs it exactly as given before the fix and after it, and records both results with commit ids; a changed test counts as a decline. A test that guards a listed promise joins that promise's existing test. Where no test can express the finding, the reviewer names the exact lines to remove or replace. On a document, the reviewer gives the exact words and the author applies them. The implementer or author may decline, with a reason; a declined blocking finding stays open and goes to the Maintainer with that reason, as at a cap. A premise objection to a proposal or plan has no exact words and goes to the Maintainer with the author's reply. At code review, a design objection means the plan was wrong and takes the plan-amendment path, with its fresh non-author review. A passing test is not proof that a fix is right, so the later verification runs stay; no second read of the fix follows.

**Scope the Maintainer adds.** A further proposal or plan review happens only for scope the Maintainer adds. Its brief is the added text and the first review of the same kind. It goes to the first reviewer where the tool can resume that session, otherwise to a reviewer given only those two things, never to the author. An addition that alters what a high-risk surface does or accepts gets one Security Review pass on the same brief, and a Security reviewer may also read any file the addition touches.
```

### G3

Targets: `dev/agent_collaboration.md`; `templates/core/dev/agent_collaboration.md`

Find:

```text
A review fix larger than a failing test returns to the reviewer for a targeted look before Boundary B.
```

Replace with:

```text
A review fix is closed by the review's own test or exact words ("Review rules"), not by a second read before Boundary B.
```

### G4

Targets: `dev/agent_collaboration.md`; `templates/core/dev/agent_collaboration.md`

Find:

```text
A plan may group dependent chunks that deliver one independently finishable outcome; the coordinator decides connected-arc grouping.
```

Replace with:

```text
A plan may group dependent chunks that deliver one independently finishable outcome, in at most five chunks (a chunk is one row of its Sequence table); plan review checks this, and larger work becomes several plans sharing one joined integration run. Code is reviewed once, after the last chunk; a plan may name one earlier review point, at plan time, for a high-risk chunk that later chunks build on. The coordinator decides connected-arc grouping.
```

### G5

Targets: `dev/agent_collaboration.md`; `templates/core/dev/agent_collaboration.md`

Find:

```text
each exact obligation plus author disposition before
```

Replace with:

```text
each exact obligation (scope the Maintainer adds follows "Review rules") plus author disposition before
```

## C2: plan and proposal templates (each with its shipped twin)

### T1

Targets: `dev/plans/_template.md`; `templates/core/dev/plans/_template.md`

Find:

```text
and there is no second plan-review pass. Plan review and
```

Replace with:

```text
and there is no second plan-review pass, except for scope the Maintainer adds (`dev/agent_collaboration.md` > "Review rules"). Plan review and
```

### T2

Targets: `dev/plans/_template.md`; `templates/core/dev/plans/_template.md`

Find:

```text
`ready-to-archive`. A second code-review pass runs only when the revision
introduced new defects, never to re-confirm that the first round's findings were
addressed. Same basis block, with the range made explicit:
```

Replace with:

```text
`ready-to-archive`. Code review is one round after the plan's last chunk (a plan
may name one earlier review point for a high-risk chunk that later chunks build
on). A blocking finding closes with the reviewer's failing test or exact words
(`dev/agent_collaboration.md` > "Review rules"); no second pass re-reads a fix.
Same basis block, with the range made explicit:
```

### T3

Targets: `dev/plans/_template.md`; `templates/core/dev/plans/_template.md`

Find:

```text
One row per chunk: what it does, what gates it, roughly what it ships. Mark a
```

Replace with:

```text
One row per chunk, at most five (plan review checks this; larger work becomes several plans): what it does, what gates it, roughly what it ships. Mark a
```

### P1

Targets: `dev/proposals/_template.md`; `templates/core/dev/proposals/_template.md`

Find:

```text
proposal review and response suffice.  In the usual proposal
```

Replace with:

```text
proposal review and response suffice, unless the Maintainer adds scope (`dev/agent_collaboration.md` > "Review rules").  In the usual proposal
```

### P2

Targets: `dev/proposals/_template.md`; `templates/core/dev/proposals/_template.md`

Find:

```text
deliver one independently finishable outcome. Its required implementation,
```

Replace with:

```text
deliver one independently finishable outcome in at most five chunks; larger
work becomes several plans. Its required implementation,
```

## C3: methodology pages

### M1

Targets: `docs/methodology/dual-review.md`

Find:

```text
**Caps and closure.** A proposal gets one usual review and one author
response; a plan gets one review; code gets one review. A second proposal pass
is only for widened scope, a second code pass only for defects introduced by
the revision, and plan review never repeats. Security Review normally takes at
most two passes. A further pass requires its specific unresolved security
question or newly changed material, why earlier passes and evidence cannot
resolve it, expected value, the named artifact and scope, and explicit
Maintainer authorization for that pass. Another pass needs new authorization.
Without these, the cap stands.
```

Replace with:

```text
**Caps and closure.** Each stage is one round: one usual review and, where the
tier requires it, one Security Review. A proposal gets one usual review and one
author response; a plan gets one review; code gets one review, after the plan's
last chunk. A further proposal or plan review is only for scope the Maintainer
adds, on a brief of the added text and the first review of the same kind; code
gets no second usual pass, and plan review otherwise never repeats. A further
Security Review pass requires its specific unresolved security question or newly
changed material, why earlier passes and evidence cannot resolve it, expected
value, the named artifact and scope, and explicit Maintainer authorization for
that pass. Another pass needs new authorization. Without these, the cap stands.
```

### M2

Targets: `docs/methodology/dual-review.md`

Find:

```text
For example, if a second pass closes the finding and no accepted check remains
unmet, advance without a third read.
```

Replace with:

```text
For example, if the closing test passes or the exact words are applied and no
accepted check remains unmet, advance without another read.
```

### M3

Targets: `docs/methodology/dual-review.md`

Find:

```text
A proposal revision that widens scope gets a pass only
on the new material; code gets a second pass only when its revision introduced
a defect.
```

Replace with:

```text
A further pass on scope the Maintainer adds covers only the new material; code gets no second usual pass, because a blocking finding closes by the reviewer's failing test or exact words, or stays open and goes to the Maintainer if declined (`dev/agent_collaboration.md` > "Review rules").
```

### M4

Targets: `docs/methodology/dual-review.md`

Find:

```text
anything more, per artifact, never by tier.
```

Replace with:

```text
anything more, per artifact, never by tier. The one exception is scope the Maintainer adds, which follows `dev/agent_collaboration.md` > "Review rules".
```

### M5

Targets: `docs/methodology/plans.md`

Find:

```text
`awaiting-code-review` only when the revision introduced new defects.
```

Replace with:

```text
`awaiting-code-review` only for a further pass the caps allow (`dual-review.md` > "Caps and closure").
```

### M6

Targets: `docs/methodology/plans.md`

Find:

```text
may share a plan. Do not split work by default or lose accepted scope. A
```

Replace with:

```text
may share a plan, in at most five chunks; larger work becomes several plans. Do not split work by default or lose accepted scope. A
```

### M7

Targets: `docs/methodology/plans.md`

Find:

```text
A plan review has one round; the fold carries the plan forward and no
second plan-review pass is run. The only plan-stage pass that may recur
is a **Security Review**, which normally takes at most two passes to close the
obligation it was raised against. A further pass requires a specific unresolved
security question or newly changed material, why earlier passes and evidence
cannot resolve it, expected value, the named artifact and scope, and explicit
Maintainer authorization for that pass; each later pass needs new
authorization. Without these, the cap stands. An unresolved blocker or unmet
accepted criterion/check at the cap goes to the Maintainer by name and does not
clear automatically. Each pass gets its own dated subsection with a round
suffix:
```

Replace with:

```text
A plan review has one round; the fold carries the plan forward and no
second plan-review pass is run, except for scope the Maintainer adds. A
**Security Review** takes one pass to close the obligation it was raised
against. A further pass requires a specific unresolved
security question or newly changed material, why earlier passes and evidence
cannot resolve it, expected value, the named artifact and scope, and explicit
Maintainer authorization for that pass; each later pass needs new
authorization. Without these, the cap stands. An unresolved blocker or unmet
accepted criterion/check at the cap goes to the Maintainer by name and does not
clear automatically. A further pass, when one is allowed, gets its own dated
subsection with a round suffix:
```

### M8

Targets: `docs/methodology/lifecycle.md`

Find:

```text
A second pass is only for widened scope and covers only
```

Replace with:

```text
A further pass is only for scope the Maintainer adds and covers only
```

### M9

Targets: `docs/methodology/lifecycle.md`

Find:

```text
`awaiting-code-review` only when the revision introduced new defects.
```

Replace with:

```text
`awaiting-code-review` only for a further pass the caps allow (`dual-review.md` > "Caps and closure").
```

### M10

Targets: `docs/methodology/lifecycle-contract.md`

Find:

```text
**only when it widened scope** (material the review never saw)
```

Replace with:

```text
**only when the Maintainer added scope** (material the review never saw)
```

### M11

Targets: `docs/methodology/lifecycle-contract.md`

Find:

```text
**only when the revision introduced new defects**
```

Replace with:

```text
**only for a further pass the caps allow**
```

### M12

Targets: `docs/methodology/lifecycle.md`; `docs/methodology/lifecycle-contract.md`

Find:

```text
RV -. revision widened scope .-> AR
```

Replace with:

```text
RV -. Maintainer added scope .-> AR
```

### M13

Targets: `docs/methodology/lifecycle.md`; `docs/methodology/lifecycle-contract.md`; `docs/methodology/plans.md`

Find:

```text
RVC -. revision introduced new defects .-> ACR
```

Replace with:

```text
RVC -. further pass the caps allow .-> ACR
```

## C4: modules (each with its shipped twin)

### S1

Targets: `dev/modules/security-review.md`; `templates/modules/team-gated/security-review.md`

Find:

```text
normally stops after two passes. Each further pass requires a specific
```

Replace with:

```text
stops after one pass. Each further pass requires a specific
```

### TD1

Targets: `dev/modules/testing-discipline.md`; `templates/modules/team-gated/testing-discipline.md`

Find:

```text
> archive. Keep a test only for a listed external promise through a public entry
```

Replace with:

```text
> archive. A test a reviewer writes to close a blocking finding is scratch work
> too, unless it guards a listed promise; then it joins that promise's existing
> test. Keep a test only for a listed external promise through a public entry
```

## C5: records

### R1

Targets: `CHANGELOG.md`

Find:

```text
## Unreleased

## 0.8.0
```

Replace with:

```text
## Unreleased

### Major changes

- **Changed: One round of review.** Each review stage (proposal, plan, code) now gets one round, and a reviewer who blocks work supplies the failing test or the exact words that close the finding, so nobody reads the fix a second time. Security Review's normal limit drops from two passes to one, code is reviewed once after a plan's last chunk, and a plan has at most five chunks; the rules apply to proposals and plans opened after the upgrade. ([accepted proposal](dev/proposals/archive/2026-11-20-claude-one-round-reviews.md))

## 0.8.0
```

### R2

Targets: `dev/PLANNING.md`

Find:

```text
| **Attach a release `.zip` that leaves out Cairn's own `dev/` folder.**
```

Replace with:

```text
| **Recount review passes under the one-round rule.** (v0.9, at the end; the proposal's D6) | At the end of v0.9, repeat the proposal's heading count of review passes on plans opened after the one-round rules shipped, by the method in its appendix, and compare with that appendix's baseline of 73 plans (median 5 passes per plan; 43 of 73 plans with three or more code-stage passes). Each plan's verification record states how many test files the selector chose. Check the proposal's listed signals that the change is wrong. | [Proposal](proposals/archive/2026-11-20-claude-one-round-reviews.md) and its [appendix](proposals/archive/2026-11-20-claude-one-round-reviews--appendix.md) |
| **Attach a release `.zip` that leaves out Cairn's own `dev/` folder.**
```

This places the row in the roadmap's section 2 ("Cairn's own releases: simpler, and verified on three hosts") as that section stands on `0.9-dev`.
