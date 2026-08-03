<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/doc-governance.md doctrine/runtime-contract.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see AGENTS.md, "Where doctrine/ references resolve") -->

# A documented gate names what runs it — the enforcement-claim ledger

**Author**: Claude (Strategy)
**Model**: Claude Opus 5
**Date opened**: 2026-08-03
**Status**: proposed
**Touches**: `bootstrap/SAFETY.md`, `bootstrap/DEPENDENCY_BUDGET.md`,
`bootstrap/container/recipe.md`, `bootstrap/container/floor-gate.sh`,
`bootstrap/fidelity-check.md`,
`doctrine/runtime-contract.md`, `doctrine/lifecycle.md`, `AGENTS.md`,
and (deferred — see *Sequencing*) `bootstrap/tests/test_security_lint.py`,
`bootstrap/tests/fixtures/skills/README.md`,
`bootstrap/tests/test_python_floor.py`
**Deliberately not touched**: `bootstrap/PROVENANCE.md`. The sweep **found** a
live instance there — the sharpest one in the tree — and **hands it off**
rather than editing it; see row E1 and *Cross-lineage collisions*. Recorded in
the header so a reader can tell a routing decision from an oversight without
reading to the ledger.
**Related**: the broad-look strategy note
(`2026-07-08-claude-broad-look-skeptical-review`), Theme 3 item 1 and its
2026-07-22 correction; the sibling Theme 3 item 2 proposal on the release
scan's target set (`scan-coverage`), which edits `bootstrap/SAFETY.md` as this
one does — see *Cross-lineage collisions*; `identity-not-name` (**superseded** 2026-08-03, Decision `6c6ce39`, split
into four successor scopes), whose successor scope 1 owns the
`bootstrap/PROVENANCE.md` remedy this proposal hands off; the
`gate-reanchor-preflight` plan, whose frozen-file manifest gates three of the
rows below
**Plan review**: required(Internal) — every disposition below *except the
hand-off* (E1) is a factual correction checkable by re-running one named
command against one quoted line, so a fresh-session same-type read can verify
the whole ledger rather than take it on the author's word. E1 is not verified
here beyond its evidence, because its remedy is another lineage's to design and
review. The one judgment call —
whether the re-worded `bootstrap/SAFETY.md` sentence still conveys the
obligation it currently overstates — falls inside the **Security Review
this proposal triggers by the letter of the triage list** (`bootstrap/SAFETY.md`
is a named bootstrap-safety / security-stack surface), so escalating the
whole proposal to External would duplicate that read rather than add
independence. Ratified at Decision.


**Vocabulary and when the collision constraint binds** (identical in every
proposal of this set, so the set does not disagree with itself). *Within-set* =
two Theme 3 proposals claim the same file. *Cross-lineage* = a Theme 3 proposal
and a successor scope of `identity-not-name` claim the same file; there are
exactly two, `tools/lifecycle_planner.py` and `bootstrap/PROVENANCE.md`. The
constraint binds at **plan-open and implementation, not at proposal-open** — an
open proposal edits no file, so all of this set may be open, reviewed and decided
concurrently. Nothing mechanical enforces the constraint; it is carried by these
tables and by the work-intent claim taken before editing.

## Context

Cairn's own prose describes checks in the vocabulary of **gates** — things
that fire, fail closed, and stop a change from landing. A reader who
looks for the trigger finds, in several cases, that there is none; in
eight cases finds a claim that names a **CI system this repository does not
have**; and in one case finds a shipped verifier that returns success without
checking the control its document promises.

This is Theme 3 item 1 of the broad-look note. That item shipped a
published correction on 2026-07-22 (the original said the Bandit scanner
"runs nowhere"; the canonical interpreter does have `bandit`, and the
Bandit-dependent tests do run and pass there). I re-verified the narrowed
claim at HEAD and it holds. I then swept for the pattern rather than the
instance, which is where the real finding is: it is not one sentence, it is a
**house style**.

**The first pass of that sweep was itself incomplete, and I have re-run it.**
A proposal whose pitch is *"the pattern is the finding, not the instance"* has
to say how it looked for the pattern, or the pitch is unfalsifiable. The
method, its two axes, and the four rows the first pass missed (A6, A7, A8 and
E1) are recorded under *How the sweep was run* below — before the ledger, so a
reader can judge the coverage before reading the findings it produced.

### What actually enforces anything, verified at HEAD `3292f21`, 2026-08-03

All measurements below are on the canonical interpreter (Python 3.13.13).

The re-run sweep and the Class E evidence were taken at `7639ec5`, three
commits later. The three intervening commits touch **only** `dev/` lifecycle
artifacts (`git diff --stat 3292f21..7639ec5` reports two files, both under
`dev/`), so every measurement in this section stands unchanged at the later
commit. Recording the two anchors rather than silently re-labelling one, since
this proposal is about not asserting what was not measured.

**There is no CI of any kind.** The GitHub metadata directory holds seven
files — five issue templates, one pull-request template, one label
definition — and no workflow:

```
$ find .github -type f | sort
.github/ISSUE_TEMPLATE/bug.md
.github/ISSUE_TEMPLATE/foldback.md
.github/ISSUE_TEMPLATE/friction.md
.github/ISSUE_TEMPLATE/gap.md
.github/ISSUE_TEMPLATE/wish.md
.github/PULL_REQUEST_TEMPLATE/foldback.md
.github/labels.yml
```

No other forge's pipeline file is tracked either — `git ls-files` matched
nothing for `workflow`, `Jenkinsfile`, `.circleci`, `.travis.yml`,
`.gitlab-ci.yml`, `azure-pipelines`, `woodpecker`, or `drone`.

**Two git hooks fire automatically, and neither runs a scanner.** They are
untracked files under the git directory, written per-clone by the
work-intent hook installer (`tools/_intent/hooks.py`), so a fresh clone
has none until someone installs them:

* `pre-commit` runs `tools/intent.py _precommit_check`. It checks
  **work-intent claim collisions only** — whether another live session has
  claimed a staged path. It can block (the shipped default enforce mode is
  `block`), so calling it purely advisory understates it; but it reads no
  Markdown, runs no scanner, and checks no claim, link, or Python source.
* `post-commit` runs `tools/intent.py _auto_release`, terminated with
  `|| true`. It can never fail anything.

**Everything else fires only when a person types the command.** The
repository's own honest inventory of those commands is committed, in the
`gate_commands` block of the gate manifest fixture
(`bootstrap/tests/fixtures/gate_manifest.json`): four entries — the
`pytest` suite, the AST attestation verify, `scripts/check_cairn.py`, and
`scripts/quality_gate.py --sub neutrality`. Each is a command a human
runs. The release checklist in `SECURITY.md` adds
`bootstrap/security_check.py`, and says so honestly: *"Before cutting a
release, run — and record the output in the release notes"*.

Measured today, so the cost of the alternative is on the record:

* `python -m pytest bootstrap/tests` — **1556 passed in 146 s**, as_of
  2026-08-03, Python 3.13.13.
* `python scripts/check_cairn.py` — clean, **163 Markdown files**
  scanned, as_of 2026-08-03.
* `bandit` 1.9.4 is installed in the canonical environment and
  `bootstrap/tests/test_security_lint.py` runs (not skips); `vermin`
  resolves on PATH and `bootstrap/tests/test_python_floor.py` runs (not
  skips). The 2026-07-22 correction is confirmed.
* Nothing in the suite or in `scripts/` invokes
  `bootstrap/container/acceptance.sh` or `bootstrap/container/floor-gate.sh`.

### How the sweep was run, and what the first pass missed

The first pass looked for **one lexical signal** — the token `CI` in Cairn's
own prose — and read each hit in context. That is how A1–A5 were found. It is
also why the enumeration was wrong, and the failure is instructive: *a
document can promise a mechanical control without ever using the word.*

**The first pass missed `bootstrap/PROVENANCE.md`**, which contains no CI
vocabulary at all and still carries the sharpest instance in the tree — a
published control whose shipped verifier exits `0` without checking it (row
E1, evidence below). A reviewer found it; I did not. I am recording that in
the artifact rather than quietly adding the row, because the gap is itself
evidence about the method, and a reader deciding how much of this ledger to
trust needs it.

The sweep now runs on **two axes**. I state both so the next reader can re-run
it rather than take it on my word — which is the whole argument of this
proposal, applied to the proposal.

**Axis 1 — lexical.** Every tracked Markdown file outside `dev/` and
`CHANGELOG.md`, grepped for the standalone token `CI`, every hit read in
context:

```
$ git ls-files '*.md' | grep -v '^dev/' | grep -v '^CHANGELOG.md' \
    | xargs grep -nE '(^|[^A-Za-z])CI([^A-Za-z]|$)'
```

17 files match, as_of 2026-08-03. Four carry a finding
(`bootstrap/DEPENDENCY_BUDGET.md`, `bootstrap/container/recipe.md` — twice —
`doctrine/runtime-contract.md`, and the one the first pass had not read,
`bootstrap/tests/fixtures/skills/README.md`, now row **A6**). The other 13 use
the word correctly: *"Cairn is **not** a … CI/CD tool"*, *"your CI gates
them"*, *"the adopter's **own** CI"*. They are dispositioned in Class D or in
the out-of-scope class below.

The equivalent grep over tracked source — `_` added to the boundary class so
identifiers like `CI_ENV` and `_in_ci` do not match as prose —

```
$ git ls-files '*.py' '*.sh' | grep -v '^dev/' \
    | xargs grep -nE '(^|[^A-Za-z_])CI([^A-Za-z_]|$)'
```

matches 24 files, as_of 2026-08-03, and yields two further findings —
`bootstrap/container/floor-gate.sh` (row **A7**) and
`bootstrap/tests/test_python_floor.py` (row **A8**) — plus A5, already in the
ledger. One near-miss is instructive enough to record: the
`"The drift gate for CI"` line in `scripts/sync_doc_snippets.py` is **not** a
finding, because that file is a byte-identical **verbatim** copy of the
adopter-facing `templates/modules/team-gated/sync_doc_snippets.py` (same
SHA-256 in the gate manifest, `as_of 2026-08-03`), where "CI" is correct — the
adopter has one. Cairn's copy is a mirror, not an independent claim, and
editing one side alone would break the verbatim-copy invariant. It is listed
with the out-of-scope prescriptions below.

**Axis 2 — behavioural.** For each document stating a control in the
indicative — *"is signed"*, *"fails closed"*, *"must pass"*, *"refuses"* —
find the artifact that would check it, and **run it**. This is the axis that
reaches E1, and it is strictly more expensive: it requires executing
something, not grepping. I ran it over all four "Controls" bullets in
`bootstrap/PROVENANCE.md`, over `bootstrap/SAFETY.md` Rule 7, and over the two
Class C claims. **I did not run it over the whole tree.**

So the honest coverage statement, replacing any implication that the ledger is
exhaustive: **axis 1 is complete and reproducible by the two commands above;
axis 2 is a sample, not an enumeration.** The sampled axis is the one that
produced the worst row, which is a reason to expect it holds more — see
*Known omissions*.

### Why this is a defect and not a style quibble

The postdoc is a scientist who codes, evaluating whether to trust an
apparatus. The failure is not that they run a check they thought was
automatic — it is the opposite. They read *"run in Cairn's CI"*, go
looking for the CI, find seven issue templates, and now have a calibrated
reason to discount **every other enforcement claim in the repository** —
including the true ones: the write-containment guard, the fail-closed
lockfile integrity check, the AST attestation, the dangling-reference
lens. One falsifiable overclaim is cheap to find and expensive to survive,
because a careful reader generalises from it correctly.

Cairn already knows this and already gets it right in five places (the
"Already honest" class below). The defect is that the house style is
inconsistent, not that it is unknown.

E1 sharpens the argument rather than merely adding to it. The Class A reader
goes looking for a trigger and finds none, which at least fails visibly. The
E1 reader runs the shipped verifier, sees `OK` and exit `0`, and concludes the
control holds — a **silent** false negative, which is strictly worse than a
missing one. That is the difference between a document that overstates and a
tool that agrees with it.

## Proposal

**One contract, stated once:** *a document that describes a check names
what runs it* — a command a person runs, a test inside the suite, a git
hook, or (if one ever exists) a CI job. A check with no trigger is not
described in the vocabulary of one.

That contract lands as one sentence in the governing layer, and is
applied to the current tree as a twelve-entry disposition ledger. Nothing
that executes changes. No new tool, no new file, no new command.

### The rule

In `AGENTS.md` > "Verifying claims", after the existing sentence *"The
checker is a **discipline aid, not a gate**"*, add:

> **Name the trigger, and check what it checks.** Any document that
> describes a check says what runs it — a command a person runs, a test in
> `bootstrap/tests`, a git hook, or a CI job. Cairn has no CI; do not write
> "in CI" for something no CI runs. A check whose only trigger is a human
> remembering is described that way. And when a named trigger exists, the
> document states what that trigger actually verifies: a tool that returns
> success without testing the claimed property is a worse defect than no
> tool, because it is silent.

That location is deliberate: the sentence it follows is already the
correct model, so the rule reads as a generalisation of existing practice
rather than a new imposition.

The second clause was added after the sweep's re-run, and it is load-bearing
rather than decorative. The first draft of the rule was purely lexical —
"name the trigger" — and a name-the-trigger rule alone would **not** have
caught E1. `bootstrap/PROVENANCE.md` states its signed-tag control without
naming any trigger, and the obvious way to satisfy a lexical rule would be to
point the sentence at `bootstrap/container/verify-ref.sh`, which declares in
its own header that it *"composes with bootstrap/PROVENANCE.md"* and which
returns `OK` on an unsigned tag. Complying with the first draft would have
made the document **more** wrong, not less. A governing sentence that can be
satisfied by citing a tool that does not perform the check is not worth
adding. The clause is one sentence and it prescribes nothing new to run.

### The ledger — twelve claims, five dispositions

**Class A — names a CI that does not exist. Disposition: correct the
fact.** These are false as written, not merely loose.

| # | Location | What it says | Disposition |
|---|---|---|---|
| A1 | `bootstrap/DEPENDENCY_BUDGET.md` line 101 | *"It runs only in Cairn's own CI (`bootstrap/tests/test_python_floor.py`)"* | Replace with "It runs only in Cairn's own test suite". Doubly wrong today: there is no CI, **and** the test runs locally — I ran it, 2 passed. |
| A2 | `bootstrap/container/recipe.md` line 141 | the floor gate and acceptance test *"run in **Cairn's CI**, not in an adopter's CI"* | Replace with "are run by the maintainer from a Cairn checkout, not in an adopter's CI." Nothing in the suite or `scripts/` invokes either script. |
| A3 | `bootstrap/container/recipe.md` line 136 | Rootless Linux + Podman/Docker is *"**Supported, tested** (the F4 acceptance gate runs here)"* | Change "runs here" to "is run here by hand", or date the last run. As written it implies a standing gate; it is a manual exercise. |
| A4 | `doctrine/runtime-contract.md` line 189 | the section heading *"Floor CI check"* (echoed at line 46 and line 185) | Rename to "Floor check" in all three places. The section body is already accurate — it correctly says the check is a test that skips gracefully — so only the name lies. |
| A5 | `bootstrap/tests/test_security_lint.py` lines 12 and 89 | *"a skipped security gate in CI is a missing one"*; the skip message *"Fails (not skips) in CI."* | **Defer** — see *Sequencing*. The `_in_ci()` branch at line 48 is dead code today; the docstring should say so ("the CI branch is provisioning for a CI that does not yet exist"). Keep the branch: it costs nothing and is correct the day CI lands. |
| A6 | `bootstrap/tests/fixtures/skills/README.md` lines 16 and 41 | the skills mechanism tiers are *"**CI**-proven here and in `test_skills_fanout.py` / `test_skills_install.py`"*; promoting a target is *"dominated by standing up the harness in CI"* | Replace "CI-proven" with "suite-proven". Same shape as A4 — only the name lies. The substance is true and I verified it: those three test modules exist and pass (18 passed, as_of 2026-08-03, Python 3.13.13). **Defer** — the file is frozen; see *Sequencing*. |
| A7 | `bootstrap/container/floor-gate.sh` line 5 | the header comment *"Runs in CAIRN's CI (not adopter CI)."* | Replace with "Run by the maintainer from a Cairn checkout (not adopter CI)." This is A2's claim restated inside the script A2 describes, so fixing only the prose would leave the code contradicting the corrected document. Comment-only; no executable line moves. |
| A8 | `bootstrap/tests/test_python_floor.py` line 1 | the module docstring opens *"Floor **CI** check: vermin-based Python minimum-version assertion."* | Drop "CI", matching A4's rename of the `doctrine/runtime-contract.md` heading this docstring echoes. **Defer** — the file is frozen; see *Sequencing*. |

**Class B — gate-phrased obligation with no trigger, and an internal
contradiction. Disposition: re-word to a review obligation.**

| # | Location | What it says | Disposition |
|---|---|---|---|
| B1 | `bootstrap/SAFETY.md` line 120 | every change to agent-loaded content *"must pass the content-integrity scanner (`content_scan.py`, run by `check_cairn.py`)"* | Re-word to name the trigger and the reviewer's obligation. |

B1 is the theme's original instance, and it is worse than "no trigger",
because three surfaces disagree about the same scanner:

* `bootstrap/SAFETY.md` line 120 — a change **"must pass"** it.
* `templates/modules/team-gated/content-security.md` line 79 — the shipped
  runner's exit contract calls a finding **"advisory"**, and says a
  composing orchestrator *"does **not** fail its aggregate on this alone —
  it is a human-review signal."*
* `scripts/check_cairn.py` — returns 1 on any flag, i.e. genuinely hard —
  but nothing runs it on a change. It runs at release time, invoked by
  `bootstrap/security_check.py`.

Note what the suite *does* cover, so the re-wording does not overcorrect:
`bootstrap/tests/test_generated_output_scan.py` scans the generated tree
from scaffolded profiles, and `bootstrap/tests/test_skills_security.py`
scans the canonical skills artifacts. So agent-loaded content that reaches
an adopter *through a scaffold* is scanned in the suite. What is **not**
scanned by any automatic trigger is `doctrine/*.md`, `docs/*.md`,
`case-studies/*.md`, the `bootstrap/*.md` documents, and module templates
outside the scaffolded profiles — precisely the prose a reader of Rule 7
would assume is covered.

Proposed replacement for the clause at `bootstrap/SAFETY.md` line 120
(the surrounding sentence and the by-file-class list are untouched):

> — and is scanned with the content-integrity scanner (`content_scan.py`).
> Two triggers exist and neither fires on a commit: the suite scans
> generated output and the skills artifacts on every `pytest` run, and
> `check_cairn.py` scans every tracked Markdown file when a person runs it
> (the release gate `security_check.py` runs it). Source prose that no
> scaffolded profile emits — `doctrine/`, `docs/`, `case-studies/`, this
> document — is reached **only** by that manual run. Running it is the
> reviewer's obligation, not a mechanism's guarantee.

**Class C — true behaviour, missing trigger. Disposition: add a clause,
keep the claim.** Both claims are accurate about what the command does;
both omit that a person must type it.

| # | Location | What it says | Disposition |
|---|---|---|---|
| C1 | `doctrine/lifecycle.md` line 218 | *"The `check_cairn` self-check **fails closed** when an adopter-facing `templates/` surface references a Cairn-internal-only path"* | Append: "when run — `python scripts/check_cairn.py`, at review time and in the release gate." |
| C2 | `bootstrap/fidelity-check.md` line 42 | the same gate, same phrasing | Same one-clause addition. |

**Class D — already honest. Disposition: no change; these are the
wording model the rule generalises.** Listed so the review can check that
the rule matches existing practice rather than inventing a new standard:

* `AGENTS.md` line 260 — *"The checker is a **discipline aid, not a
  gate**"*.
* `templates/modules/default-on/claim-check.md` line 119 (same phrase) and
  line 171, which explicitly reasons that *"a pre-commit hook would
  convert the checker from advisory into"* something else.
* `templates/modules/default-on/lifecycle-metrics.md` line 85 — the
  heading *"Doctrine and enforcement are separate"*, and the body's
  "a separate, optional choice".
* `SECURITY.md` line 61 — *"Before cutting a release, run — and record the
  output"*: names the trigger, the human, and the record.
* `bootstrap/container/recipe.md` lines 142–143 — *"records **SKIPPED**
  (never PASS) on a host with no OCI runtime — a missing gate is
  *degraded assurance*, not a silent green"*.

**Class E — a shipped verifier that does not check the control its document
promises. Disposition: hand off to the lineage that owns the remedy.** One
row, and it is the worst one in the ledger. It is recorded here — with its
evidence — rather than fixed here, because the fix belongs to another
in-flight proposal. **The sweep found this instance and is routing it. It did
not miss it, and it is not being dropped.**

| # | Location | What it says | Disposition |
|---|---|---|---|
| E1 | `bootstrap/PROVENANCE.md` lines 25–28 | *"A release tag is signed, or the release commit is a maintainer-authored commit on the protected default branch. The adopter can verify the tag rather than trusting an arbitrary commit."* | **Hand off** to `identity-not-name` successor scope 1, which already owns signed tags, `verify-ref.sh`, and out-of-band key distribution. No edit to `bootstrap/PROVENANCE.md` in this proposal. |

Why this is a different disposition and not just another Class A row: in every
Class A case there is **no** mechanism, and the document merely names one that
does not exist. Here the mechanism **exists, ships, and returns success**. The
sentence's first branch is false today; its second is checked by nothing that
ships. I established both by running the tools an adopter would run, rather
than by reading the code. Re-verified for this proposal at `7639ec5`,
2026-08-03:

```
$ bash bootstrap/container/verify-ref.sh . v0.3.0
verify-ref: OK — release tag 'v0.3.0' -> 12ec2ad28f22a7d3d9c19ce67e78d86cc625757a
$ echo $?
0
$ git verify-tag v0.3.0
error: no signature found
$ echo $?
1
```

* **Branch one — "a release tag is signed".** False for both existing
  releases. `git verify-tag` reports *"no signature found"* for `v0.3.0` and
  for `v0.2.0`. Both are annotated tags (`git for-each-ref` reports object
  type `tag`), which is what `verify-ref.sh` checks, and annotated is not
  signed.
* **Branch two — "or the release commit is a maintainer-authored commit on
  the protected default branch".** Not verified by anything shipped either.
  `git log --format='%G?'` returns `N` (no signature) for both release
  commits, so "maintainer-authored" rests on `%an`, a self-declared string a
  committer can set to anything; and "protected default branch" is a forge
  setting no Cairn tool reads. Note the timeline, because it is easy to
  misread: commits at HEAD *are* signed (`%G?` = `G`) — the signing epoch
  post-dates both releases, so this is a gap in what shipped, not a claim that
  signing is absent from the repository today.
* **What the verifier actually checks.** `git describe --exact-match --tags`
  — that *some* tag points at the commit. Not a signature, not authorship,
  not the branch. It then prints `OK` and exits `0`. Nothing automatic runs it
  either: its only caller in the tree is `bootstrap/container/acceptance.sh`,
  which row A2 establishes is itself run by hand.

**Why hand off rather than fix here.** Three reasons, in order of weight.
First, the remedy is not a wording change: `identity-not-name` successor scope
1 has to decide whether to keep the second branch at all, sign the `v0.4.0`
tag, add a signature check to `verify-ref.sh`, and solve out-of-band key
distribution — a security design with its own review tier. Second, this
proposal is a documentation-honesty ledger with an Internal plan review;
absorbing a signing design would drag a cryptographic-trust decision into a
review that is not scoped for it, which is the bundling mistake the External
Security Review on `identity-not-name` has already penalised once today.
Third, two proposals editing `bootstrap/PROVENANCE.md` concurrently is the
collision recorded below.

**What "hand off" obliges, so it is not a way of doing nothing.** E1 stays an
open row in this ledger until the successor lands. If `identity-not-name`
successor scope 1 is rejected, deferred past v0.4.0, or narrowed so that
`bootstrap/PROVENANCE.md` is left unedited, **E1 reverts to this proposal as a
Class A-style wording downgrade** — the sentence is softened to state what is
actually true and checkable, and the aspiration moves to a "What this is not"
bullet beside the existing *"Not cryptographic attestation"* one. That
fallback is cheap and needs no new mechanism. Naming it now is what keeps the
hand-off from becoming a quiet drop, which is the standing failure mode of
routing a finding to somebody else.

**Urgency, stated once and not argued here.** `identity-not-name` already
makes the v0.4.0 timing argument: a DOI-minted release archives the byte
snapshot with the provenance claim attached and no repository controls
travelling with it. I record the dependency and do not re-litigate the
schedule.

**Out of scope, checked and left alone: adopter-facing prescription.**
Three claims use gate vocabulary correctly, because they tell the
*adopter* to build a gate in *their* CI, and do not assert Cairn has one:
`templates/modules/team-gated/doc-drift-prevention.md` line 42 (*"A drift
gate fails the build. A check in CI compares…"*),
`templates/modules/team-gated/security-review.md` line 62 (wire a linter
into the verification command so the boundary is *"checked automatically
on every change"*), and `doctrine/README.md` line 92 (the
`doc-drift-prevention` module *ships* the CI drift gate). These are
prescriptions, not claims. No change. I note only that a reader could
misread the third; a single word ("the CI drift gate an adopter wires up")
would settle it, and I would take that as a review amendment rather than
propose it.

A fourth, found by the re-run sweep and left alone for a different reason:
`scripts/sync_doc_snippets.py` line 43 calls its `--check` mode *"The drift
gate for CI"*. That file is a **verbatim** copy of the adopter-facing
`templates/modules/team-gated/sync_doc_snippets.py` — byte-identical, same
SHA-256 in the gate manifest, `as_of 2026-08-03` — where the sentence is
correct, because the adopter has a CI. Cairn's copy is a mirror of an
adopter-facing prescription, not an independent claim about Cairn, and
editing one side alone would break the verbatim-copy invariant the fidelity
tests assert. No change, and the reasoning is worth recording because "it says
CI, therefore it is a finding" would have been wrong here.

### Sequencing

**Three rows are frozen.** `bootstrap/tests/test_security_lint.py` (A5),
`bootstrap/tests/fixtures/skills/README.md` (A6) and
`bootstrap/tests/test_python_floor.py` (A8) are all in the **frozen set** of
the in-flight `gate-reanchor-preflight` batch: each path appears in
`frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json` (162
frozen entries, as_of 2026-08-03), and that manifest **HOLDs by default on
any modification to a frozen file** — deliberately, so an unattended actor
cannot decide an edit to a gate is "merely strengthening". A5, A6 and A8 are
therefore **deferred to a follow-up commit after that batch closes and its
manifest is retired**. A1–A4, A7, B1 and C1–C2 touch no frozen file and can
land now — I checked each path against `frozen_files` rather than assuming,
and `bootstrap/container/floor-gate.sh` (A7) is free.

That three of the eight Class A instances sit behind a frozen-file HOLD is
worth one sentence of interpretation: the surfaces most likely to describe a
gate dishonestly are the gate surfaces themselves, and those are exactly the
ones a live gate batch locks. The deferral is correct, and it is also a
standing reason this class of defect ages.

### Cross-lineage collisions — one proposal in flight per file

Two proposal lineages are live in this tree and they claim overlapping files.
Recording the overlap in the artifact, because a file claimed by two open
proposals is a merge conflict waiting to be discovered at implementation time
by whoever loses the race — and because the handling below has already been
agreed and should not be re-opened at review.

**The agreed handling: the proposals stay separate and are sequenced, not
merged.** Merging them is the bundling mistake that cost `identity-not-name` a
REVISE/SPLIT verdict from its External Security Review earlier today; a single
plan cannot hold several gate sets without the strictest one dominating the
rest. Separation is the correction, and this note is the cost of the
correction, paid explicitly.

| File | Claimed by | Resolution |
|---|---|---|
| `bootstrap/SAFETY.md` | **this proposal** (row B1) and the sibling Theme 3 item 2 proposal `scan-coverage` | **Only one may be in flight at a time.** Whichever is accepted second rebases its edit onto the landed text and re-quotes the line it replaces. |
| `bootstrap/PROVENANCE.md` | **this proposal** (row E1, evidence only) and `identity-not-name` successor scope 1 | **Successor scope 1 owns the remedy.** This proposal edits nothing there — see Class E. |

On `bootstrap/SAFETY.md` specifically: both proposals edit prose about the
same scanner, from different directions — this one re-words a *"must pass"*
that names no trigger (B1), while `scan-coverage` concerns the release scan's
target set. They are compatible in substance and incompatible in mechanics,
because both quote and replace text in the same document and B1's replacement
depends on the line numbers being what they were when it was quoted. A reader
of either proposal should treat the other's landed state as the baseline.

Three further overlaps exist elsewhere in the set and are recorded so a
reviewer sees the collision list as a set-level fact rather than a quirk of
this artifact. None of them touches this proposal:
`tools/lifecycle.py` with its `templates/skills/_lib/` twin, claimed by
`agent-context-scrub` and `planner-line-semantics`;
`tools/lifecycle_planner.py` with its twin, claimed by
`planner-line-semantics` and `identity-not-name` successor scope 2; and
`SECURITY.md`, claimed by `scan-coverage` and `agent-context-scrub`. Note
that the first and third are Theme 3 drafts colliding with **each other**,
not with the other lineage — parallel drafting produces intra-set collisions
as readily as cross-lineage ones, which is the more useful lesson.

Three of the colliding proposals share one root cause — raw external text
reaching an authority-bearing decision without normalization:
`agent-context-scrub`, `planner-line-semantics`, and `identity-not-name`
successor scope 2. They get one reviewer sitting, so the shared premise is
judged once rather than three times at three different depths.

### Documentation / doctrine surface

This proposal is almost entirely documentation surface, so the routing is
the substance rather than a footnote. Per `docs/DOCUMENTATION_PLAN.md`:

* **Governing layer (`AGENTS.md`)** — the one-sentence "Name the trigger"
  rule. Cross-cutting prescription every contributor follows; it belongs
  here, beside the existing "discipline aid, not a gate" sentence it
  generalises.
* **Descriptive layer** — A1, A2, A3, A5, A6, A7, A8, B1, C2: `bootstrap/`
  documents (and, for A5–A8, the comments and docstrings of `bootstrap/`
  scripts and tests) describing the software as it is. These are factual
  corrections.
* **Doctrine (`doctrine/`)** — A4 (`doctrine/runtime-contract.md`, a
  heading rename) and C1 (`doctrine/lifecycle.md`, one clause). Neither
  changes a rule.
* **No layer here — handed off** — E1. `bootstrap/PROVENANCE.md` is a
  descriptive-layer document, but this proposal contributes evidence to
  another lineage rather than an edit, so it moves no surface in this tree.
* **Deliberation layer** — this proposal.

No adopter-facing template changes, so the loop-fidelity lens is not
engaged and no install-set surface moves. The one candidate that would have
engaged it — `scripts/sync_doc_snippets.py`, a verbatim twin of a shipped
module file — is left alone for exactly that reason; see the out-of-scope
class above.

### Doctrine-change rate-limit

Two of the twelve rows touch `doctrine/`, and the `AGENTS.md`
sentence is a new governing rule, so the gate is addressed rather than
waved past — even though I argue below it does not strictly apply.

**Why it may not apply:** A4 and C1 are *factual corrections to
descriptions*, not changes to a rule, process, or contract. Renaming
"Floor CI check" to "Floor check" alters nothing anyone must do.

**Cleared anyway, on the recurrence arm** (`doctrine/rationale.md` > "How
the doctrine evolves under evidence"): the same failure shape — prose
asserting an enforcement trigger that does not exist — is present **eight
times across seven files** (A1–A8), all pre-dating this session. Eight
independent instances is well past the "≥2 in a rolling window" bar, and
the recurrence is what distinguishes this from a one-off typo worth
fixing silently. The gate is cleared on recurrence, not on the strength
of a single incident. (That count rose from five as a result of re-running
the sweep — see *How the sweep was run*. The gate cleared at five as well, so
nothing here turns on the correction; I record the movement because a figure
that changed should be visibly a measurement, not a rhetorical number.)

The high-risk arm is *also* available and I note it without relying on it:
`bootstrap/SAFETY.md` is a named security surface in the triage list, so
B1 is a security-document change by the letter.

## Rationale

* **Which user workflow does it improve?** The first external adopter's
  first two weeks. A scientist evaluating an apparatus reads the security
  and safety documents early, because that is where they decide how much
  to trust everything else. Today the second paragraph they read about
  the container gates tells them it runs in a CI that is not there.
* **What contract does it preserve?** The credibility of the enforcement
  claims that *are* true. Cairn's real controls are good — write
  containment, fail-closed lockfile integrity, AST attestation, the
  dangling-reference lens. Their value depends on a reader believing the
  document that describes them. This proposal spends eight small
  corrections now, defers three behind a frozen-file HOLD, and routes one
  to the lineage that owns it, to protect that.
* **What transparency does it improve?** It makes the apparatus
  *falsifiable in the reader's favour*: after this change, every
  enforcement sentence in Cairn names a command the reader can run and
  watch fail. That is a stronger position than a claim of automation.
* **Why now?** Pre-first-external-adopter, pre-v0.4.0, and the sweep
  evidence is fresh and reproducible. After the postdoc reads it, the
  correction is a retraction instead of a fix.

## Alternatives considered

1. **Do nothing.** The claims stay false; the reader who checks one of
   them discounts the rest. This is the alternative with the worst
   asymmetry: the cost of the fix is a handful of sentences, and the cost
   of not fixing it is the reader's calibrated distrust of controls that
   actually work.
2. **Add CI, so the claims become true.** Explicitly **not proposed
   here** — it is building something new against the standing "fix
   defects, build nothing new" direction, and it is the Maintainer's call,
   not mine. Cost estimate below so the decision is informed rather than
   deferred blind.
3. **Add a mechanical gate-honesty lens to `check_cairn.py`** — a lens
   that flags "in CI" in Cairn's own prose. Rejected twice over: it builds
   a new mechanism against the standing direction, and it is
   self-undermining — a gate that enforces gate-honesty is itself run only
   when a human remembers, so it would be the thirteenth entry in its own
   ledger. If CI ever lands, this becomes cheap and worth revisiting.
   Worth noting against it, too: a lexical checker would have found A6–A8
   and would **not** have found E1, which is the row that matters most.
4. **Delete the enforcement sentences rather than re-word them.**
   Rejected for Class C: `check_cairn` really does fail closed on a
   dangling adopter-facing reference, and that is worth documenting.
   Deleting a true claim to avoid an untrue implication loses information;
   naming the trigger keeps both.
5. **Wire the four `gate_commands` into the existing pre-commit hook.**
   Rejected on three counts: a 146-second pre-commit is a hostile
   pre-commit and will be bypassed within a day; the hook body is written
   by `tools/_intent/hooks.py`, so extending it changes a shipped
   installer's behaviour for every adopter, which is a much larger
   proposal than this one; and the hooks are per-clone and untracked, so
   even then the guarantee would hold only for whoever installed them.
6. **Re-word only the `bootstrap/SAFETY.md` sentence the theme named.**
   Rejected: the sweep found the pattern, and fixing one instance of a
   house style leaves the reader to find the other eleven. The theme's own
   instruction was "the pattern is the finding, not the instance".
7. **Fix `bootstrap/PROVENANCE.md` here, since the sweep found it.**
   Rejected — this is the Class E hand-off, and the reasoning is there
   rather than here because the disposition is the finding's own. In short:
   the remedy is a signing design with a different review tier, and a second
   proposal editing that file concurrently is the collision recorded above.
   The alternative is listed so the choice is visible as a choice.

### The CI decision — a cost estimate, explicitly *not* proposed

Recorded here so the Maintainer can decide it separately, on evidence,
without this proposal smuggling it in.

* **Scope.** One workflow running the four committed `gate_commands`
  under Python 3.13.13, plus `bootstrap/security_check.py` on release
  tags.
* **Runtime.** ~2.5 minutes per run (suite 146 s, as_of 2026-08-03), plus
  installing `bandit` and `vermin`. Both are already declared dev-only
  exceptions in `bootstrap/DEPENDENCY_BUDGET.md`, so no budget change.
* **A real safety constraint, already published by Cairn.**
  `templates/modules/team-gated/content-security.md` line 68 says **"Do
  not wire it into untrusted-PR / fork CI"** — *"a run from an attacker's
  checkout executes the attacker's scanner."* A naive `on: pull_request`
  workflow that ran `check_cairn.py` would therefore violate Cairn's own
  published guidance on the first fork PR. Any CI must be
  trusted-branch-push-only, or explicitly fork-PR-excluded. This is the
  main reason "just add CI" is not a five-minute task, and it is a good
  reason to decide it deliberately.
* **New coupling.** A workflow file couples Cairn to one forge. Cairn's
  neutrality doctrine is about AI vendors, not forges, so this is not a
  doctrine violation — but it is a new maintained surface that itself
  becomes a thing that can drift.
* **Already provisioned.** `bootstrap/tests/test_security_lint.py` line 48
  already has an `_in_ci()` branch that fails rather than skips when
  Bandit is missing. It costs nothing today and becomes live for free.
* **Recommendation.** Decide after v0.4.0, as its own proposal. If it
  lands, disposition A5 is rewritten rather than deferred, and
  alternative 3 becomes worth a second look.

## Evidence / verification plan

Every disposition is a quoted line plus a command that shows the claim
false. The full evidence is in *Context*; the verification of the change
itself is:

* `python scripts/claim_check.py <file>` on each edited file — one file
  per invocation (it exits 2 on more than one).
* `python scripts/check_cairn.py` — green; it is the prose-integrity smoke
  for any Markdown change and it re-checks every internal link the
  re-wordings touch.
* `python -m pytest bootstrap/tests` — green, under Python 3.13.13. Seven of
  the eight landing rows touch only Markdown and the eighth (A7) is a shell
  comment, so the suite is a no-change check rather than a real guard here.
  Worth stating plainly,
  because it is another instance of the finding: **no test asserts on
  `bootstrap/SAFETY.md`'s prose at all.** Grepping `bootstrap/tests/` for
  "SAFETY" returns exactly one hit, a comment in
  `bootstrap/tests/test_generated_output_scan.py` line 114 — not an
  assertion. The B1 re-wording has no automatic regression guard; its
  only check is `check_cairn.py`, run by hand, plus review.
* `python scripts/quality_gate.py --sub neutrality` — green; no vendor
  name is introduced ("GitHub Actions" appears in this proposal, i.e. the
  deliberation record, which is permitted, and in no shipped doctrine or
  template).

**Signal that would falsify the finding before the change lands:** a CI
configuration for any forge appearing in `git ls-files`. Re-run the
`find .github -type f` and `git ls-files` checks at implementation time;
if either now returns a pipeline, Class A collapses and only B1, C1–C2 and
E1 survive. E1 is independent of that signal: an unsigned tag stays unsigned
whether or not a pipeline exists, and adding CI would not make
`verify-ref.sh` check a signature.

**A second falsifying signal, specific to E1:** `git verify-tag v0.3.0`
succeeding, or a signature check appearing in
`bootstrap/container/verify-ref.sh`. Either means the successor landed and the
row is closed rather than handed off; re-run both commands quoted in Class E
at implementation time rather than trusting this artifact's snapshot.

### Author-accounting — invariants, failure modes, edge cases

Not a routine change — it edits a named security document — so the block
is filled rather than waived.

* **Invariants.**
  * *Nothing that executes changes behaviour.* Enforced by: of the twelve
    rows, eight edit only Markdown (A1–A4, A6, B1, C1–C2); A5 and A8 are a
    docstring, a skip message and a module docstring, all deferred, none
    touching a branch condition; A7 is a `#` comment in a shell script whose
    executable lines are untouched; E1 edits nothing at all. The suite is the
    enforcer.
  * *A handed-off row is tracked, not dropped.* Enforced by: E1 stays an open
    ledger row with a named fallback disposition (Class E), and the archive
    of this proposal cannot record it as resolved without either the
    successor landing or the fallback being applied. This is a review
    obligation, not a mechanism — which is the same admission B1 makes, one
    layer up.
  * *No file is edited by two open proposals at once.* Enforced by review and
    by the *Cross-lineage collisions* table, not by a mechanism. Nothing in
    the tree detects two proposals claiming one path; the work-intent hook
    catches concurrent *sessions*, not concurrent *proposals*. A reviewer
    holding both artifacts is the guard.
  * *No enforcement claim is weakened into an optional one.* Enforced by
    review, not by a mechanism — this is the row a reviewer should
    challenge. The B1 replacement text above deliberately keeps the word
    "obligation" and names who holds it.
  * *`bootstrap/SAFETY.md`'s by-file-class review threshold list is
    untouched.* Only the clause at line 120 moves.
* **Failure modes.**
  * *Open (degrades):* the re-worded B1 reads as permission to skip the
    scan. Mitigated by naming the reviewer's obligation explicitly, and
    by the Security Review this proposal triggers.
  * *Open, and this is the sharp one:* there is **no closed failure mode**
    for a bad B1 edit. No test asserts on `bootstrap/SAFETY.md`'s prose
    (verified: one "SAFETY" hit across `bootstrap/tests/`, and it is a
    comment). A reviewer is the entire guard. Naming that is more useful
    than pretending the suite covers it — and it is the same defect this
    proposal is about, one layer down.
  * *Open (deferred by design):* A5, A6 and A8 stay wrong until the
    `gate-reanchor-preflight` batch closes. Accepted and recorded rather
    than worked around, because working around a frozen-file HOLD is
    exactly the behaviour that manifest exists to prevent.
  * *Open (the hand-off's own failure mode):* E1 is routed to
    `identity-not-name` successor scope 1, and a routed finding can be lost
    at the seam — the successor is narrowed, `bootstrap/PROVENANCE.md` drops
    out of its scope, and both artifacts each believe the other has it. This
    is the one failure mode introduced by *this* correction rather than found
    by it, so it should be named rather than assumed away. Mitigated by the
    fallback disposition in Class E and by naming the file in the
    *Deliberately not touched* header field; **not** mitigated by any
    mechanism. A reviewer holding both proposals should confirm the row
    appears in exactly one of them as an obligation.
* **Edge cases.** Empty: none of the edited lines is generated or synced,
  so no drift gate re-derives them — and that was checked rather than
  assumed, because the re-run sweep did surface a candidate on a
  verbatim-synced file (`scripts/sync_doc_snippets.py`) and excluded it for
  exactly this reason. Mismatched: the three-way
  disagreement about the content scanner (B1) is itself the edge case,
  and is resolved by making `bootstrap/SAFETY.md` agree with the shipped
  runner's exit contract rather than the reverse.
* **Public-path → test mapping.** N/A — no public code path is added or
  changed. The two Python files in scope (A5, A8) are both deferred and both
  edits are docstrings or a skip message; the one shell file (A7) is a `#`
  comment.
* **Known omissions.** I did not sweep `CHANGELOG.md` (historical record;
  correcting past entries would falsify the record rather than the
  claim), the archived proposals under `dev/proposals/archive/`
  (immutable), or adopter-facing module templates beyond the four named
  above as out-of-scope prescriptions.

  **The behavioural axis is a sample, and this is the sharpest thing a
  reviewer should hold against the ledger.** Axis 2 — running the artifact
  that would check a stated control — was applied to
  `bootstrap/PROVENANCE.md`'s four "Controls" bullets, `bootstrap/SAFETY.md`
  Rule 7, and the two Class C claims. It was **not** applied to the rest of
  the tree. That axis is where E1 came from, and E1 is the worst row here, so
  the sample has already demonstrated a hit rate that argues for finishing
  it. A full behavioural audit of every *"fails closed"* / *"is signed"* /
  *"refuses"* claim is a different and larger piece of work — plausibly its
  own proposal — and I would rather name it as unfinished than let the
  lexical axis's completeness stand in for it. **The correct reading of this
  ledger is: complete for one axis, sampled for the other, and the sampled
  one is the one that matters more.**

### Tests required

**N/A — no new pytest test.** Adding a test that scans Cairn's own prose
for "in CI" is alternative 3, rejected above as building a new mechanism
against the standing direction. The regression guard is the existing
suite: if any test is coupled to the edited `bootstrap/SAFETY.md` wording,
it fails, which is the correct outcome. A7 has no coupled test either —
grepping `bootstrap/tests/` for `floor-gate` returns nothing, `as_of
2026-08-03` — so it is the same uncovered shape as B1, on a smaller surface.

### Examples / smoke checks

* `python scripts/check_cairn.py` — the prose-integrity smoke for any
  Markdown or doctrine change (internal link resolution, claim-path
  check, content scan by file class).
* `python scripts/claim_check.py <file>`, once per edited file.
* No scaffold surface changes, so `bootstrap/scaffold.py --summary` /
  `--dry-run` / `--manifest` are unaffected and are not needed here.

## Signals the change is wrong

* **A reviewer reads the new `bootstrap/SAFETY.md` clause as permission to
  skip the scan.** Recovery: restore the imperative and instead add a
  separate sentence naming the trigger, keeping "must" intact. The
  obligation was never the problem; the implied mechanism was.
* **The "Name the trigger" rule starts generating review findings on
  adopter-facing templates**, where gate vocabulary is correct because it
  prescribes what an adopter builds. Recovery: scope the rule explicitly
  to descriptions of *Cairn's own* checks. I have deliberately worded it
  for that, and the three out-of-scope prescriptions above are the test
  case; if the boundary still misfires, narrow it.
* **CI lands within a release or two.** Then A1–A4 will have been churned
  for nothing and A5's deferral was wasted. Recovery is cheap (re-instate
  the CI wording), and the claims were still false in the interval — but
  if the Maintainer already intends to add CI soon, the honest move is to
  say so at Decision and reduce this proposal to B1 and C1–C2 alone.
* **Someone proposes a gate-honesty checker on the strength of this
  ledger.** That would be this proposal causing the thing it argues
  against. Recovery: point at alternative 3.
* **E1 is still open when this proposal is archived.** A hand-off that
  outlives the artifact that made it is how a found defect becomes a lost
  one — and this proposal exists because the record over-promised, so
  over-promising a routing is the exact failure it would be embarrassing to
  repeat. Recovery: do not archive with E1 open. Either the successor has
  landed, or the fallback wording downgrade in Class E is applied here first.
* **The ledger is read as exhaustive.** It is exhaustive on the lexical axis
  and sampled on the behavioural one, and the first version of this draft
  blurred that — which is how it missed E1. Recovery: *How the sweep was run*
  states the boundary; if a reviewer finds a further instance on either axis,
  that is a coverage correction to record, not a reason to withdraw the
  pattern finding. A sweep that can absorb a new instance without changing
  its conclusion is behaving correctly; one that cannot was overfitted.
