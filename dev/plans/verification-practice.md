# Plan: verification practice — a review reads a commit, mutation for set claims, a test scope for small fixes

**Source proposal**: `dev/proposals/archive/2026-10-17-claude-verification-practice.md`
**Status**: implementing
**Plan review**: required(Internal)
**Assurance path**: high-assurance — inherited: the change edits `doctrine/` and
a shipped template.
**Opened**: 2026-10-18

## Source proposal

**In plain terms.** This plan writes four short rules into both copies of
`AGENTS.md` (Cairn's own and the one adopters install) and into the doctrine
behind them. A reviewer works from the author's commit, and in a shared folder
writes nothing except its own review. A review that claims "this value reaches
every place it must" proves it by breaking each place on purpose. A small fix
with no plan runs the tests that own what it touched, not the whole suite,
unless it touches risky code. And one phrase gets a definition.

Accepted 2026-10-18 at `e8ec34af`. Revision 1 binds, with every recommended
answer: Q1, a trivial change on a high-risk surface runs the full suite once
before its code review; Q2, mutation is required only when a finding or claim
names a set; Q3, the class "a reviewer's write reverts uncommitted work in a
shared tree" is a data-loss surface. Q3 is a recorded Maintainer decision in the
Decision block and needs no edit here; it lets item 1 land with the rest.

## Scope

Six existing files and one new test file:

* `AGENTS.md` and `templates/core/AGENTS.md` (the shipped copy): the Review
  section and Boundaries A, B and C. Edited in lockstep. The rules match; Cairn's
  copy keeps naming Cairn's commands, and the shipped copy stays project-general.
* `doctrine/dual-review.md`: "Asynchronous and commit-mediated" and "Boundary C".
* `doctrine/plans.md`: "Boundary A", "Boundary B" and "Code review — doctrine".
* `dev/plans/_template.md` and `templates/core/dev/plans/_template.md`: one word
  in the `verification-commands` slot.
* One new test file holding the new pins,
  `bootstrap/tests/test_review_and_verification_rules_ship.py`.

**Not touched:** `bootstrap/_scaffold/`, so **no AST impact**; every gate-manifest
frozen file, including `bootstrap/tests/test_verification_boundaries.py`, which
passes unedited; `doctrine/lifecycle.md`; Boundary B's default, fence list,
refusal rule and "uncertainty resolves to `full`"; the six fresh-run triggers;
the security preflight; the plan templates' bounded-record field (Revision 1
scopes item 3 to the two `AGENTS.md` copies and doctrine); and
`dev/agent_collaboration.md` with its shipped twin.

### Tests that pin the text this plan changes

Found by searching `bootstrap/tests/*.py` for every touched path, as both
literal paths and `Path` joins, not by expectation. Breaking one is a defect,
not a re-baseline.

* **`bootstrap/tests/test_verification_boundaries.py`** (frozen, 40 nodes,
  passes unedited). It pins tokens on all six files. **Five of its guards edit
  the raw text and then check it**, so an edit that adds a second copy of a
  phrase, or wraps one across a line, turns a green guard red:
  * `test_operational_guard_detects_removed_full_fallback`
    (`bootstrap/tests/test_verification_boundaries.py:73-76`): "cannot be
    bounded confidently" stays exactly once in `AGENTS.md`, on one line.
  * `test_bounded_guard_detects_a_removed_fence` (`:237-252`): it replaces every
    "trust-ceremony surface" in the raw text of `AGENTS.md`, then checks the
    whitespace-collapsed text. So every occurrence, the new definition included,
    stays on one physical line, never wrapped between "trust-ceremony" and
    "surface".
  * `test_review_reuse_guard_detects_unconditional_reuse` (`:321-324`): "no
    valid Boundary B record exists" stays once in `doctrine/dual-review.md`.
  * `test_record_schema_guard_detects_removed_reviewed_range` (`:156-159`) and
    `test_plan_template_guard_detects_removed_reviewed_range` (`:374-377`):
    "Reviewed range" stays once in `doctrine/plans.md` and in
    `dev/plans/_template.md`.

  It also pins these:
  * `test_full_run_required_routes_to_the_existing_first_trigger` (`:298-318`)
    parses the six-trigger list in `doctrine/dual-review.md`, from "six
    triggers applies:" to the paragraph opening "Review-only". Nothing is
    inserted in that span.
  * `test_installed_operational_rule_is_project_general` (`:79-89`): the
    shipped copy names no `bootstrap/tests`, `scripts/quality_gate.py` or
    "Python 3.13".
  * `test_bounded_boundary_b_contract_reaches_every_surface` (`:189-227`):
    "bounds the change's effects confidently", "contract surface",
    "trust-ceremony surface", "Uncertainty resolves to" and "Boundary B mode"
    stay on all five surfaces.
  * `test_boundary_c_adjudicates_a_bounded_record` (`:286-295`): "Bounding" and
    "FULL RUN REQUIRED" stay in both copies and in `doctrine/dual-review.md`.
  * `test_already_open_plans_keep_their_written_contract` (`:260-278`): its
    phrase stays in both copies and `doctrine/plans.md`.
* **`bootstrap/tests/test_comprehension_floor.py`** treats `## Review` as the
  text running to the next H2 heading (`bootstrap/tests/test_comprehension_floor.py:69`).
  Item 1's paragraph adds no H2 line.
* **`bootstrap/tests/test_scope_reduction_trap.py`** reads both copies, both plan
  templates and both doctrine files for scope-reduction obligations. None of
  them sits in a passage this plan edits.
* **`bootstrap/tests/test_documentation_plan_module.py`** checks the slot markers
  in the shipped `AGENTS.md` and plan template.
* **`bootstrap/tests/test_link_check_exclusions.py`** keeps `AGENTS.md` in the
  link checker's scanned set.

Measured at `07bd9950` under Python 3.13.13: these five files, 182 passed.

**The install family reads the shipped files too.** 57 test files drive a
scaffold install, which renders `templates/core/AGENTS.md` and
`templates/core/dev/plans/_template.md`. Five of them assert on those files'
structure:
* `bootstrap/tests/test_scaffold.py`: the install, and the plan-template clause
  parity at `:584-598`;
* `bootstrap/tests/test_upgrade.py`: a `cairn:if` region in the shipped copy;
* `bootstrap/tests/test_module_merge_lockfile.py` and
  `bootstrap/tests/test_security_verification.py`: slot merges into it;
* `bootstrap/tests/test_verify_integrity.py`: the finalize hint on `AGENTS.md`.

The `AGENTS.md` edits sit outside every slot and `cairn:if` region. C4's
one-word edit sits inside the plan templates' `verification-commands` slot,
which no module fills, so its default text ships as written. No edit adds a
`{{` token. The rest of the family should therefore see no change, and Boundary
B's full run checks that.

### Found while planning

Revision 1 says "the plan fixes the bytes". Two byte-level choices deliver an
accepted outcome that the quoted wording would otherwise miss. Neither removes
anything, and both are named here so the plan reviewer can say otherwise.

* **Boundary B's second "no reviewed mapping" clause.** Revision 1 rewrites
  "unless the plan's reviewed mapping bounds" but leaves the clause after it:
  "if a substantive surface has no reviewed mapping … the full suite runs"
  (`AGENTS.md:197-199`, `templates/core/AGENTS.md:201-203`). A trivial
  change's mapping is reviewed only afterwards, by Bounding, so a literal
  reader still derives a full run for every trivial change. That is the
  proposal's own falsifier. The clause becomes "has no such mapping", matching
  Boundary A.
* **"Claimed first" in the shipped copy.** Claiming ships only with the
  team-gated `coordination-tiers` module
  (`templates/modules/team-gated/coordination-tiers.md:28`). The shipped
  `AGENTS.md` and `templates/core/dev/agent_collaboration.md` never mention it.
  An unconditional "claimed first" would be a rule an adopter without that
  module breaks on first use, which is VP1's failure again. The shipped copy
  says "claimed first if the project uses file claims", and so does
  `doctrine/dual-review.md`, because doctrine treats work intents as an
  optional tier (`doctrine/coordination.md:103-110`,
  `doctrine/session-routines.md:34-36`). Cairn's `AGENTS.md` stays
  unconditional (`dev/agent_collaboration.md:114`).

**Decided at plan review: a text-only fix on a high-risk surface.** "Boundary B
governs every implementation" meets "Prose-only work does not run the suite".
For a text-only fix to a surface the file names as high-risk, one rule said to
run the full suite and the other said to run none. The prose-only rule
already settles this for contract surfaces: no full suite unless a test or
manifest pins the prose's bytes. This plan extends that one sentence to
high-risk surfaces ("a contract or high-risk surface").
* Prose that nothing pins runs the prose gates on any surface. No test can fail
  on it, and on Cairn's one prose high-risk surface, vendor-neutrality, the
  neutrality gate is the check that matters.
* Prose that a test or manifest pins is a substantive surface (item 4). On a
  high-risk surface it runs the full suite once.

That is Q1's stated purpose: a missed pin must not reach adopters. So this
stays inside the Maintainer's answer to Q1 and is not put to the Maintainer.

Also noticed, and not widened:

* `doctrine/plans.md` already defines a trust-ceremony surface
  (`doctrine/plans.md:313-315`), so the in-place definition goes into the two
  `AGENTS.md` copies only.
* An accepted proposal implemented without a plan (`doctrine/plans.md:188-193`)
  is neither "a trivial change, with no proposal or plan" nor a plan. Under the
  new text it has no mapping, so it runs full. Where its record goes is unstated
  today and stays unstated. That is a pre-existing gap and not this plan's to
  fill. Plan review judged it owed to the archive batch (*Dispositions*).
* `bootstrap/verify_integrity.py --target .` already reports 18 findings,
  `AGENTS.md` and `dev/plans/_template.md` among them. The plan does not
  finalize, because that would re-attest earlier, unreviewed drift.

### Shared files with the sibling plans

The three other proposals accepted on 2026-10-18 will get their own plans.
**Whichever lands second rebases.**

* **`doctrine/plans.md`**: `maintainer-attention` edits "Mutability rule",
  "Accepted scope is a floor" and "Lasting-truth migration doctrine". This plan
  edits "Boundary A", "Boundary B" and "Code review — doctrine". The sections
  differ, so this is a textual rebase only.
* **Both plan templates**: `maintainer-attention` edits the header, *Scope
  delta* and *Dispositions*, and `independent-scientific-check` edits
  *Acceptance criteria*. This plan changes one word inside the
  `verification-commands` slot.
* **`AGENTS.md`, `templates/core/AGENTS.md` and `doctrine/dual-review.md`** are
  edited by this plan alone among the four accepted scopes.
  `maintainer-attention`'s `AGENTS.md` part left with its Part B cut.
  `neutrality-and-upgrade-slots` is "Governing: None". The
  `independent-scientific-check` lens-8 sentence in `doctrine/dual-review.md`
  was deferred by its Decision to a board row; if it revives, it rebases on
  this plan.
* **`scripts/quality_gate.py`** (frozen): `neutrality-and-upgrade-slots` makes
  the neutrality checker stricter (HTML comments, `.txt` and `.json` under
  `templates/`, four more names). This plan runs that checker but does not edit
  it. Its new text names no vendor anywhere, comments included, so it passes
  either version.
* **`dev/PLANNING.md` and `CHANGELOG.md`**: each plan adds to them at its own
  archive, a serialization point.

### Documentation / doctrine surface

**Governing:** both `AGENTS.md` copies. **Doctrine:** `doctrine/dual-review.md`
and `doctrine/plans.md`. **Templates:** one word in both plan templates. The
rate-limit grounds are the proposal's, ratified by the Decision; no
`docs/` page changes.

## Sequence

Each chunk lands its own pins in the new test file in the same commit, so the
suite is green at every chunk boundary. C1 creates the file.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **A review reads a commit.** A reviewer works from the author's commit and, in a shared folder, writes only its own review. Text: *Wording* > 1, added after "Review is asynchronous and commit-mediated" in both copies (`AGENTS.md:77-78`, `templates/core/AGENTS.md:81-82`) and to `doctrine/dual-review.md` > "Asynchronous and commit-mediated" (`:100-113`). Creates `bootstrap/tests/test_review_and_verification_rules_ship.py` with this rule's pins, the parametrized guard and the floor test. | `ready-to-implement` | one commit |
| C2 | **Mutation for set claims, and an honest ledger.** When a review claims a value must reach every place in a set, the reviewer breaks each place on purpose and reports every result. Text: *Wording* > 2, added to Boundary C in both copies (`AGENTS.md:214-227`, `templates/core/AGENTS.md:218-231`) and to `doctrine/dual-review.md` > "Boundary C" directly after its first paragraph (`:294-302`), outside the six-trigger span; one pointer bullet in the ledger shape of `doctrine/plans.md` > "Code review — doctrine" (`:886-891`), not a second copy of the rule. Adds pins. | C1 | one commit |
| C3 | **Boundary B reaches a trivial change.** A small fix with no plan runs the tests that own what it touched and names them in its commit message, the code reviewer rules on that choice, and on a contract or high-risk surface it runs the full suite once. Text: *Wording* > 3, in Boundaries A and B and the prose-only paragraph of both copies; in Boundaries A and B of `doctrine/plans.md` (`:285-298`, `:300-372`), its validity sentence included; and in the opening sentence of `doctrine/dual-review.md` > "Boundary C" (`:295-296`). Adds pins. | C2 | one commit |
| C4 | **One term.** Defines "substantive surface" once, so that code, tests and prose a test reads all count, and drops the narrower "substantive code surface". Text: *Wording* > 4, in Boundary A of both copies and `doctrine/plans.md` (`:291`, `:295-298`); "code" removed at `dev/plans/_template.md:151` and `templates/core/dev/plans/_template.md:145`. Adds the pin. | C3 | one commit |
| C5 | **Boundary B, then the record.** Runs the whole suite once on the finished work and writes down the result. Full mode (*Verification*), then `## Implementation verification`; status to `awaiting-code-review`. | C4 | one commit |
| M | **MAINTAINER-ONLY — no new ceremony.** No frozen file changes. The new test file and the nodes it adds join the gate-manifest re-anchor already queued on `dev/PLANNING.md`. **An implementing agent must not perform it.** The agent's part is the board note at archive. | code review cleared | Maintainer |

### Wording each chunk lands

The shipped copy's bytes are given here. Cairn's copy is identical except where
noted. Line wrapping is free, except that the frozen guards read these phrases
from raw text, so none may wrap or gain a second copy:
* "trust-ceremony surface" and "cannot be bounded confidently" in Cairn's
  `AGENTS.md`;
* "no valid Boundary B record exists" in `doctrine/dual-review.md`, and the
  opener "required when any of these six triggers applies:", which keeps its
  blank line before "Review-only";
* "**Reviewed range**" in `doctrine/plans.md`;
* "Reviewed range" in `dev/plans/_template.md`.

**1 — Review section, both copies.** Cairn's copy drops "if the project uses
file claims". `doctrine/dual-review.md` takes the shipped sentences, conditional
included, plus one of reason: git cannot bring back an uncommitted file that a
`restore` reverted.

> **A review reads a commit, never a shared working tree.** The author commits
> what is to be reviewed before handing it over (locally; committing is not
> pushing), and the review names that commit. In a working tree it shares with
> an author, a reviewer makes one write: its own review record, appended to the
> artifact or created as its own review file, claimed first if the project uses
> file claims, and committed by explicit path. Nothing else: no other edits,
> and no `restore`, `checkout`, `stash`, `reset` or `clean`. Anything else that
> writes, such as a mutation or a scratch install, runs in a separate copy of
> the reviewed commit (a `git archive` extraction or a separate worktree). A
> figure is evidence only if it was measured on that commit's bytes.

**2 — Boundary C, both copies and `doctrine/dual-review.md`.**

> **When a finding or claim says a value must reach every member of a set**
> (every call site, every rendering path), list the set from the tree, not the
> diff, and mutate each member, in a separate copy; reading the diff does not
> settle it. A mutation ledger reports each mutant as killed, survived or
> equivalent, beside an unmutated control run, never as a bare "N of M killed".
> Equivalence is measured, not argued: a behaviour test through the real entry
> point passes under the mutation, and where another site is said to recover
> the value, mutating that site fails. Any equivalence that was not measured is
> reported as a survivor. Outside that trigger, mutation stays the reviewer's
> choice.

The bullet in `doctrine/plans.md`'s ledger shape reads: "**Mutation**, when a
finding or claim names a set: each mutant killed, survived or equivalent beside
an unmutated control, never a bare count (`dual-review.md` > "Boundary C")."

**3 — Boundaries A and B, both copies.** Boundary A becomes:

> **A — Iteration (scoped).** During implementation, run the tests and probes
> the reviewed plan maps — or, for a trivial change, with no proposal or plan,
> the tests that own each touched surface, found by searching for what imports
> or reads the touched files rather than by expectation — plus standing gates
> for every touched surface. If a substantive surface has no such mapping, run
> the full suite.

In Boundary B:
* "unless the plan's reviewed mapping bounds" becomes "unless the mapping
  bounds".
* "if a substantive surface has no reviewed mapping" becomes "has no such
  mapping".
* The fence reads "or a **trust-ceremony surface** (any high-risk surface this
  file names, or release or security ceremony work)".
* In the record sentence, only "the mapping and gates run" changes, to "the
  test files or nodes and the gates run, with counts". The sentence then reads
  "on `bounded`, name the touched surfaces, the test files or nodes and the
  gates run, with counts, why the effects are bounded, and …".
* "Append the tested SHA/range" becomes "A plan appends the tested SHA/range".

Before "An already-open plan keeps…", add:

> **Boundary B governs every implementation, a trivial change included.** A
> trivial change's mapping is the owning tests Boundary A names, and Boundary
> C's Bounding verdict reviews it afterwards. It runs before the commit, not
> after, on exactly the bytes being committed: a tree clean apart from the
> change, or a separate copy holding only it. Its record is its commit body,
> not a plan section, and carries the mode, the interpreter, and on `bounded`
> every field the record sentence above names.

In the prose-only paragraph, "A prose change to a contract surface" becomes "A
prose change to a contract or high-risk surface".

`doctrine/plans.md` gets the same changes in its own sentences:
* **Boundary A:** the trivial-change mapping. "has no reviewed mapping" becomes
  "has no such mapping"; C3 leaves "code" for C4. The prose paragraph says it
  holds on any surface, a high-risk one included.
* **Boundary B:**
  * "a plan whose reviewed mapping bounds" becomes "work whose mapping bounds";
  * the paragraph above is added;
  * "the reviewed mapping and standing gates it ran" becomes "the test files or
    nodes and the standing gates it ran, with counts", keeping the touched
    surfaces;
  * "The record is valid only when…" (`:366-368`) becomes "A plan's record is
    valid only when…", since the new paragraph states a trivial change's.

In `doctrine/dual-review.md` > "Boundary C", "For a plan with a valid Boundary B
Implementation verification record" becomes "For work with a valid Boundary B
record (a plan's Implementation verification section, or a trivial change's
commit body, whose tested revision is that commit and whose clean state is a
tree clean apart from the change)".

**4 — Boundary A, both copies, after "run the full suite."** In
`doctrine/plans.md` this joins the "Work confined to ordinary prose" paragraph,
with "under the prose-only rule below" shortened to "under the prose-only rule",
since there it sits inside that rule.

> A **substantive surface** is anything that is not ordinary prose under the
> prose-only rule below: code, tests, executable templates and snippets,
> fixtures, manifests, and prose a test or manifest pins.

## Acceptance criteria

**How the pins are built.** Each pin is an obligation, asserted on both copies
as an alternation over whitespace-collapsed text, as
`test_comprehension_floor.py` does. A rewording passes and a deletion fails.
* **Stable IDs.** Parametrized node IDs come from the obligation labels
  (`ids=`), never from the pattern. Once the queued re-anchor pins this file,
  rewording a pattern then cannot drop a pinned node.
* **The guard.** One parametrized guard collapses whitespace, removes every
  match of each obligation (`re.sub`), and asserts that the obligation is
  reported. The new guards therefore carry none of the one-copy, one-line
  constraints of the frozen ones. The negative pin's guard inserts the
  forbidden phrase instead.
* **The floor.** One test asserts that an empty file reports every positive
  obligation.

* **Every chunk:**
  * `bootstrap/tests/test_verification_boundaries.py` passes, and no chunk
    commit touches it.
  * For each chunk commit,
    `git diff -U0 <commit>^ <commit> -- templates/core/AGENTS.md templates/core/dev/plans/_template.md | grep -E '^[+-].*(\{\{|cairn:)'`
    prints nothing: no token or marker line moves.
* **C1 — the rule and its carve-out.** Both copies carry every sentence of
  *Wording* > 1 inside `## Review`, and `test_comprehension_floor.py` passes.
  The shipped copy's claim clause is conditional and Cairn's is not. The pins:
  * reads a commit, not a shared tree;
  * the one write, its own review record;
  * the forbidden commands;
  * a separate copy for anything else that writes;
  * figures measured on the commit's bytes;
  * the rule sits inside `## Review`, located as
    `test_comprehension_floor_sits_in_the_review_section` locates it;
  * the claim clause both ways: the shipped copy carries "if the project uses
    file claims"; Cairn's carries "claimed first" without it.
* **C2 — the ledger.** Both copies and `doctrine/dual-review.md` carry
  *Wording* > 2. "no valid Boundary B record exists" still occurs once in
  `doctrine/dual-review.md`, and the six-trigger list still parses as 1 to 6.
  The pins:
  * the set trigger, from the tree, not the diff;
  * killed, survived or equivalent, beside an unmutated control;
  * never a bare count;
  * measured equivalence, with unmeasured equivalence reported as a survivor;
  * mutation stays the reviewer's choice outside the trigger.
* **C3 — the reach and the fence.** Both copies, `doctrine/plans.md` and
  `doctrine/dual-review.md` carry *Wording* > 3.
  * Phrase counts in `AGENTS.md`: "cannot be bounded confidently" occurs exactly
    once, and every "trust-ceremony surface" sits on one physical line.
  * On whitespace-collapsed text, `no reviewed\s+mapping` matches in neither
    copy and not in `doctrine/plans.md`. The plan templates keep "reviewed
    mapping", because they govern plans only.
  * "substantive code surface" still occurs once in `doctrine/plans.md` after
    C3, so C4's control holds.
  * Both copies' prose-only paragraph reads "a contract or high-risk surface".
  * The pins:
    * B governs a trivial change;
    * it runs before the commit, on the bytes being committed;
    * its record is its commit body, carrying the mode and the interpreter;
    * a plan appends the Implementation verification section;
    * the owning tests are found by search;
    * the bounded record names the touched surfaces and the test files or
      nodes;
    * the trust-ceremony definition;
    * negatively, no "no reviewed mapping" in either copy.
  * **The falsifier, read from the shipped copy alone.** A reader derives:
    * (a) a trivial change on an ordinary surface runs its owning tests before
      committing, records them in its commit body (the mode, the interpreter,
      the touched surfaces, the files and counts), and takes a Bounding
      verdict;
    * (b) a trivial change to code, or to prose a test pins, on a surface the
      file names as high-risk, runs the full suite once, before its code
      review;
    * (c) a text-only fix that nothing pins runs the prose gates, on any
      surface.

    No sentence in Boundaries A to C yields "run the full suite" for case (a)
    or (c). No sentence says a trivial change appends to a plan.
* **C4 — the term.** Both copies define "substantive surface" as in *Wording* >
  4, and the pin holds it.
  `grep -c "substantive code surface" doctrine/plans.md dev/plans/_template.md templates/core/dev/plans/_template.md`
  reports 1 in each before C4 (the positive control) and 0 in each after. Both
  plan templates' slot still carries "reviewed mapping" and "full suite".
* **The new file, by C5:**
  * no skip or xfail marker, because a newly marked node holds the gate;
  * names and docstrings state the property, with no finding id, chunk letter or
    issue number: `grep -inE "VP[0-9]|PR[0-9]|EA[0-9]|\bC[1-5]\b|_c[1-5]_|#1[27]\b|#25\b"`
    on it prints nothing.
* **Throughout:**
  * This plan adds no shipped file, so its commits leave
    `python bootstrap/scaffold.py --manifest` byte-identical.
  * `python bootstrap/verify_integrity.py --target .` reports no path it did
    not report before C1 (18 at `07bd9950`).
  * The neutrality gate reports no hit in any file this plan edits.

  <!-- cairn:slot acceptance-doc-tooling -->
  Cairn's doc surface is mostly hand-authored Markdown read on GitHub;
  the doc tooling is drift-prevention, not generation:
  - **Snippet-sync** — `python scripts/sync_doc_snippets.py` pulls
    fenced blocks from runnable example sources into docs; update the
    source, then run the sync (never hand-edit a synced block).
  - **Prose-integrity gate** — `python scripts/check_cairn.py` resolves
    every internal Markdown link / anchor and every claim-path; it is
    the doc smoke for any Markdown change.
  - **Link check** — `python scripts/link_check.py` for the broader
    cross-reference sweep.
  There is no schema-render generator; a plan that introduces one names
  its source + render command here.
  <!-- cairn:end acceptance-doc-tooling -->

### Scope fidelity

| Accepted outcome (Revision 1 and the Decision) | Chunk |
|---|---|
| Item 1: a review reads a commit; the one-write carve-out; a separate copy for writes; figures on the commit's bytes; both copies and dual-review | C1 |
| Item 2: the set trigger, mutation of each member, the ledger, measured equivalence; both copies, dual-review "Boundary C", the plans.md ledger shape | C2 |
| Item 3: Boundary A's trivial-change mapping; B governs every implementation; the commit-body record on the committed bytes; "unless the mapping bounds"; test files or nodes with counts; the in-place trust-ceremony definition; dual-review's Boundary C opening | C3 |
| Item 3: B's default, refusal and six triggers, and C's rule and verdict, unchanged | C3 acceptance; C5 |
| Item 4: the definition; "code" dropped from plans.md and both plan templates | C4 |
| Q1: a trivial change on a high-risk surface runs the full suite once, before code review | C3 (the reach plus the defined fence) |
| Q2: mutation required only when a set is named | C2 |
| Q3: the data-loss classification | the Decision block, landed at `e8ec34af`; item 1 lands in C1 |
| Tests: `test_verification_boundaries.py` unedited; new pins with guards for all five groups on both copies; every reader found by search | every chunk; C1–C4; *Verification* > Boundary A |
| Smoke: claim_check, check_cairn, quality_gate with no new hit; Boundary B `full` | every chunk; C5 |

## Scope delta

**Scope delta**: preserved. Every Revision 1 outcome is mapped above and nothing
is dropped. The two byte-level choices in *Found while planning* deliver
outcomes that the quoted wording would have missed, and they remove nothing.
Plan review added two edits outside Revision 1's surface table, each answering
a finding:
* `doctrine/plans.md`'s validity sentence (PR2);
* "contract or high-risk surface" in the prose-only paragraph (PR6).

Neither moves B's default, its fence list or the six triggers.

## Verification

**Boundary A (iteration, scoped)**, the reviewed mapping:

* **Every chunk:** the five direct readers and the new file. That is
  `test_verification_boundaries.py`, `test_comprehension_floor.py`,
  `test_scope_reduction_trap.py`, `test_documentation_plan_module.py`,
  `test_link_check_exclusions.py` and the new file, plus:
  * `scripts/claim_check.py` on each edited file;
  * `scripts/check_cairn.py`;
  * `scripts/quality_gate.py --sub neutrality --sub redundancy`;
  * the marker check in *Acceptance criteria*.
* **C1 to C4** (each edits the shipped `AGENTS.md`), and **C4** (the shipped
  plan template): also `test_scaffold.py`, `test_upgrade.py`,
  `test_module_merge_lockfile.py`, `test_security_verification.py` and
  `test_verify_integrity.py`. The rest of the install family is exercised
  once, by Boundary B.
* **Before C5:** the published-manifest and `verify_integrity` comparisons in
  *Acceptance criteria*.

<!-- cairn:slot verification-commands -->
Before implementation, make Boundary A a **reviewed mapping**: for each changed
invariant and public path, name the exact affected test node/file and every
standing non-pytest gate for the touched surface. Run that scope while
iterating. There is no permanent fast tier; if a substantive code surface has
no reviewed mapping or cannot be bounded confidently, run the full suite.

After the final implementation commit, Boundary B runs once against a clean,
unchanged commit under the canonical interpreter. The default is the **full
suite**; a plan whose reviewed mapping **bounds the change's effects
confidently** may instead run that mapping plus every standing gate for every
touched surface. Bounded mode **refuses** — run full — when the change touches a
**contract surface** (install contract, fidelity or gate manifest, lockfile
schema, published `scaffold.py --manifest`) or a **trust-ceremony surface**
(any high-risk surface `AGENTS.md` names, or release/security ceremony work).
**Uncertainty resolves to `full`.** The commands:

* **Engine + seed-0 order coverage** — `python -m pytest bootstrap/tests
  --quality-gate-shuffle-seed=0`.
* **Static quality legs** — `python scripts/quality_gate.py --sub neutrality
  --sub redundancy` (does not dispatch pytest again).
* **Prose integrity** — `python scripts/check_cairn.py`.
* **Write-time claim check** — `python scripts/claim_check.py <file>` once for
  each authored proposal, plan, or doc.
* **Plan-specific acceptance commands** — the mapped tests, security budgets,
  doc-drift gates, public-path smokes, and other commands named above.

Only after that stable run, append a dated section named
`Implementation verification -- <agent> -- YYYY-MM-DD` at H2. Do not place an
empty heading in a new plan. The record uses these exact fields:

* **Boundary B mode** — `full` | `bounded`. On `bounded`, also name the touched
  surfaces, the reviewed mapping and standing gates run, why the effects are
  bounded, and the explicit absence of any contract or trust-ceremony surface.
* **Tested commit** — full SHA.
* **Reviewed range** — base and tested endpoint.
* **Interpreter/runtime** — canonical path and version.
* **Pre-run state** and **Post-run state** — clean tree and identical tested
  `HEAD`.
* A command table with **Command**, **Exit**, **Outcomes**, and **Elapsed**
  columns, including pass/fail/skip/xfail/xpass counts where applicable.
* **Non-pass disposition**, **Plan-specific acceptance commands**, and
  **Known omissions**.
<!-- cairn:end verification-commands -->

**Boundary B (integration): `full`, fixed.** Bounded mode refuses, for four
reasons, any one of which suffices:

1. **A trust-ceremony surface is touched.** `AGENTS.md` names vendor-neutrality
   of "doctrine and templates" as a high-risk surface (`AGENTS.md:324-325`), and
   this plan edits both.
2. **The change rewrites the rule that would bound it.** Judging bounded mode by
   the fence this plan rewrites is circular, and uncertainty resolves to
   `full`.
3. **The owning set is most of the suite.** 57 test files render the shipped
   template, so no bounded mapping is confident.
4. **Revision 1 accepted it:** "Boundary B: `full`".

On the contract fence: no frozen file changes, the published manifest is
unchanged and the lockfile schema is untouched. But the new file adds nodes
that the gate manifest's pinned collection will record. Whether that counts as
touching the gate manifest is uncertain, and uncertainty resolves to `full`
here too.

**How it runs.** The pair, under
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13):
`CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0`,
then `python scripts/quality_gate.py --sub neutrality --sub redundancy`, with
`check_cairn.py` and `claim_check.py` on each edited file. The full suite takes
about 11 to 12 minutes here.
* **Where.** Run it in a separate worktree at the tested commit, which shares
  refs, so the gate anchor is present. This follows rule 1: other sessions'
  uncommitted files never enter the count. Do not run it in a `git archive`
  extraction, where 34 nodes that need a repository fail (measured in the
  proposal's Response).
* **Size.** Note `scripts/token_budget.py`'s `AGENTS.md` figure before and after
  (5,824 tokens at `07bd9950`). This is information only, since no cap is
  configured.

**Expected non-pass, to be disposed of rather than treated as noise:**
* The neutrality leg exits 1 on 74 failures already present at `07bd9950`, none
  in a file this plan edits. If the neutrality plan lands first, the figure is
  that plan's. The disposition is pre-existing, with no hit on an edited line.
* No expected failure from `test_gate_manifest.py`, because no frozen file
  changes or goes away.
* The record lists every node the new file adds, by node ID, for the re-anchor.

**Boundary C** is the code reviewer's. It is worth attacking:
* the shipped copy, read as an adopter with no doctrine and no claims module:
  is every rule followable and every term defined?
* the falsifier reading in C3;
* each new pin, by deleting its clause in a separate copy, as rule 1 requires
  of the reviewer too;
* the phrase counts behind the raw-text guards.

**Security preflight.** N/A, as in the proposal: no trust boundary is added,
moved, or widened. The chunking changes no answer.

## Dispositions

*Filled at archive-preparation.* Expected:
* The new test file and its added node IDs go into the queued re-anchor row in
  `dev/PLANNING.md` (row M). No frozen file changed.
* `CHANGELOG.md` > Unreleased gets one entry.
* **#12 by tooling** goes to the Maintainer's archive batch. The proposal
  declined it for now, with a revival condition ("build it if the rule fails in
  practice"), and the accepted text assigns it to no later plan.
* **The no-plan accepted proposal's record location** (*Found while planning*)
  goes to that batch. Plan review judged it owed there, not to this plan.
* Closing issues #12, #17 and #25 is a public action after a push, so it is the
  Maintainer's call.

## Plan review -- Claude Opus 5.5 (Internal, fresh session) -- 2026-10-18

```
Reviewed commit: 73284010a3d1d3711dc59b553b1f614b37346b76
Target: the whole plan (Source proposal through Dispositions), read against Revision 1 and the Decision of dev/proposals/archive/2026-10-17-claude-verification-practice.md and the tree at the reviewed commit
Prior findings: none
Assurance path: high-assurance — inherited
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised (3 blocking, 4 non-blocking)
**Verdict**: REVISE → `revising-plan`

Distance: a fresh session of the author's agent type. I did not write this plan
and will not implement it.

### In plain terms

The plan is sound and close to ready. Every outcome the Maintainer accepted has
a chunk. The two places where the author departed from Revision 1's wording are
both right. The test, frozen-file and lockfile claims check out. Three wording
gaps need fixing before work starts, and each takes a line or two:

* One rewrite would accidentally delete "which parts were touched" from what a
  reduced test run must record. That is the item the code reviewer is told to
  challenge.
* The plan says a small fix writes its test evidence into its commit message.
  But three nearby sentences still describe only a plan's record: when the run
  happens, where the record is written, and what it contains. A small fix
  cannot follow the text word for word, and Revision 1 makes that its test of
  success.
* The sentence that would send every small fix to the full test suite comes out
  of both `AGENTS.md` copies but stays in the doctrine file.

The other four findings are improvements the author may take or decline.

### The two wording choices

* **"has no such mapping" in Boundary B delivers the outcome.** Without it, B
  keeps "if a substantive surface has no reviewed mapping … the full suite
  runs" (`AGENTS.md:197-199`). A trivial change's mapping is reviewed only
  afterwards, by Bounding, so a literal reader derives a full run for every
  small fix, which is Revision 1's own falsifier. "Such mapping" is the phrase
  Revision 1 already uses in Boundary A, so A and B now name the same thing. The
  fallback still fires where it should: a trivial change whose owning tests
  cannot be named has no such mapping and runs full. Nothing is removed. [PR3]
  carries the same fix to the doctrine copy.
* **"claimed first if the project uses file claims" in the shipped copy
  delivers the outcome.** The shipped `AGENTS.md` and
  `templates/core/dev/agent_collaboration.md` never mention claims. The
  mechanism ships only with the team-gated `coordination-tiers` module
  (`templates/modules/team-gated/coordination-tiers.md:20-29`). The half of
  rule 1 that prevents data loss stays unconditional: no `restore`, `checkout`,
  `stash`, `reset` or `clean`, and every other write goes to a separate copy.
  An adopter who has claims still claims. An unconditional clause would repeat
  VP1's failure, a rule broken on first use. [PR5] suggests that the doctrine
  copy take this form too.

### Findings

#### [PR1] blocking — C3's rewrite drops "the touched surfaces" from the bounded record

**Plain.** When a change runs fewer than all the tests, the record must say
which parts were touched, which tests ran, and why that was enough. The plan's
rewrite of that list in the two `AGENTS.md` copies deletes "which parts were
touched". The code reviewer's step is built on that item. The doctrine file and
both plan templates would keep it, so the files would disagree.

**Precision.** *Wording* > 3 says that "on `bounded`, name the touched surfaces,
the mapping and gates run" becomes "the test files or nodes and the gates run,
with counts". Applied as written to `AGENTS.md:204-206` and
`templates/core/AGENTS.md:208-210`, it removes both "on `bounded`, name" and
"the touched surfaces". Boundary C in both copies has the reviewer challenge "at
least one named surface, mapped test, or stated omission" (`AGENTS.md:217-219`),
and the named surface comes from that list. The parallel `doctrine/plans.md`
edit replaces only "the reviewed mapping and standing gates it ran"
(`doctrine/plans.md:319-322`) and keeps the surfaces, as do both plan templates
(`dev/plans/_template.md:178-180`). Revision 1 adds the test files or nodes and
the counts. It removes nothing. No test pins "touched surfaces", so nothing
would catch the loss.

**Closes when** both copies read "on `bounded`, name the touched surfaces, the
test files or nodes and the gates run, with counts, why the effects are bounded,
…", or an equivalent that keeps the surfaces.

#### [PR2] blocking — a trivial change's record is its commit body, but three sentences around it still describe only a plan's record

**Plain.** The new paragraph says a small fix records its test evidence in its
commit message. The same section still says three things that do not fit:

* the run happens *after* the commit;
* the evidence is appended to a plan section, which a small fix does not have;
* the reviewer checks details, such as which Python ran it and whether the
  folder was clean, that the commit message is never told to carry.

An author who follows the text word for word cannot comply. A reviewer who
follows the doctrine can call every such record invalid, which sends the fix
back to a full run, the cost #25 removes.

**Precision.**
* B's opener (`AGENTS.md:191-193`, `templates/core/AGENTS.md:195-197`,
  `doctrine/plans.md:302-303`) runs B "after the final implementation commit …
  against a clean unchanged commit". The new paragraph measures the trivial
  record "on exactly the bytes being committed", that is, before the commit. A
  commit body is written before its commit exists.
* "Append the tested SHA/range, interpreter, clean pre/post state, … as
  `## Implementation verification -- …`" (`AGENTS.md:211-213`,
  `templates/core/AGENTS.md:215-217`) follows the new paragraph unqualified. A
  trivial change has no artifact to append to, and a commit body cannot name its
  own SHA.
* C3's `doctrine/dual-review.md` edit makes the commit body a record that
  Boundary C checks for the tested revision, "interpreter/runtime" and "clean
  pre/post state" (`doctrine/dual-review.md:295-299`). Neither `AGENTS.md` copy
  asks the commit body to carry the interpreter.

Revision 1 leaves these bytes to the plan ("the plan fixes the bytes"). Its
measure of success is that "the next trivial change and its review can follow
the text literally".

**Closes when** the Boundary B text says three things, either in the new
paragraph or by qualifying the old sentences:

* (a) a trivial change runs B before committing, on the bytes being committed;
* (b) a plan appends `## Implementation verification`, and a trivial change's
  commit body carries the record instead;
* (c) the commit body carries at least the mode, on `bounded` the touched
  surfaces and the test files or nodes and gates with counts, and the
  interpreter.

C3's falsifier criterion (a) then adds "and the interpreter". B's default, its
fence and the six triggers do not move.

#### [PR3] blocking — `doctrine/plans.md` keeps the "no reviewed mapping" fallback

**Plain.** The plan removes the sentence that would send every small fix to the
full suite, but only from the two `AGENTS.md` copies. The same sentence in the
doctrine file is not listed for change. The check that the sentence is gone
looks only at the two copies.

**Precision.** Revision 1 puts its Boundary A text, ending "If a substantive
surface has no such mapping, run the full suite", in "both copies and in
`doctrine/plans.md`". `doctrine/plans.md:291-293` reads "If a substantive code
surface has no reviewed mapping, or its effects cannot be bounded confidently,
the full project suite is the fail-closed fallback." For `doctrine/plans.md`,
*Wording* > 3 names "the trivial-change mapping in Boundary A" but not this
clause. C3's criterion that "has no reviewed mapping" occurs in neither copy
does not read `doctrine/plans.md`. C4 drops "code" from the same sentence, and
its positive control expects "substantive code surface" to still count 1 there
before C4.

**Closes when** three things hold:

* *Wording* > 3 names the change in `doctrine/plans.md`: "has no reviewed
  mapping" becomes "has no such mapping".
* C3's criterion also reads `doctrine/plans.md`.
* C3 leaves "code" for C4, so that C4's positive control still holds, or the
  control moves.

#### [PR4] non-blocking — pin what item 3 is for, plus two properties the criteria already assert

**Plain.** The new tests check that each new rule's wording is present. They do
not check that the old sentence sending small fixes to the full suite stays
gone. Nor do they check two things the acceptance criteria rely on: that rule 1
sits inside the Review section, and that the adopters' copy keeps "if the
project uses file claims" while Cairn's copy does not.

**Precision.**
* **A negative pin.** Neither copy may tie the full-suite fallback to a
  *reviewed* mapping, for example no match for `no reviewed\s+mapping`. Add a
  guard that inserting the phrase trips the pin. C3's criterion checks this once
  by grep; a pin holds it after C3.
* **Placement and asymmetry.** Pin C1's placement inside `## Review`, as
  `test_comprehension_floor_sits_in_the_review_section` does. Pin the claim
  clause in both directions, because syncing the twins could silently flip
  either one.
* **Stable node IDs.** Give the parametrized nodes stable `ids=` taken from the
  obligation labels. `test_comprehension_floor.py`'s node IDs embed the regex
  (`bootstrap/tests/fixtures/gate_manifest.json:253-261`). Once the queued
  re-anchor pins this file's IDs, rewording one pattern would drop a pinned node
  and the gate would report `COLLECTION-DROPPED`.
* **Robust guards.** Collapse whitespace before matching, and have the guard
  remove *every* match (`re.sub`). The new guards then avoid the
  once-and-one-line constraints the plan lists for the frozen ones.
* **Optional.** One assertion on an installed `AGENTS.md`, from a single
  scaffold install into a temp directory, would show that adopters receive the
  rules. That is the stated reason the rules go in `AGENTS.md`. The edits sit
  outside every slot and `cairn:if` region, so the template source is a fair
  proxy.

#### [PR5] non-blocking — the doctrine copy of rule 1 should take the conditional claim clause

**Plain.** The plan gives the doctrine file Cairn's unconditional "claimed
first". Doctrine is the published method that adopters cite, and its own
coordination chapter treats file claims as an optional tier for concurrent
teams.

**Precision.** `doctrine/coordination.md:103-110` introduces work intents as
"Tier 2", "for concurrent teams". `doctrine/session-routines.md:34-36` reads the
intent set only "if the `coordination-tiers` module is installed". An
unconditional claim in `doctrine/dual-review.md` would contradict both. Give
doctrine the shipped wording, and keep Cairn's `AGENTS.md` unconditional.

#### [PR6] non-blocking — say whether the prose-only rule governs a prose-only change on a named high-risk surface

**Plain.** The new sentence "Boundary B governs every implementation, a trivial
change included" meets an existing rule: "Prose-only work does not run the
suite." Take a text-only fix to a file the project names as high-risk. One rule
says to run the full suite, and the other says to run none.

**Precision.** B's fence refuses bounded mode on a trust-ceremony surface. The
prose-only rule already overrides the fence for contract surfaces, but it says
nothing about trust-ceremony surfaces (`AGENTS.md:229-236`). In Cairn's tree the
case is mostly unreachable, because a change on a named surface is deliberate
unless it is a test-reproduced defect repair (`doctrine/lifecycle.md:47-58`).
The shipped copy has no lanes, so the case is reachable for adopters. Plans
already face the same tension today; the new reach makes it the common case.

**Recommended default:** the prose-only rule governs prose-only work, as it
already does for contract surfaces. One clause in the new paragraph says so. I
do not read Q1 as reaching prose-only edits, because its example was the
scaffold engine. So either answer stays inside the Decision, but the text has to
give one.

#### [PR7] non-blocking — small corrections

* *Scope* > "The install family" says "The edits add prose outside every slot
  and `cairn:if` region". C4's plan-template edit is inside the
  `verification-commands` slot (`templates/core/dev/plans/_template.md:141-180`).
  No module fills that slot (I searched `templates/`, `bootstrap/_scaffold/`
  and `scripts/`), so its default ships and nothing breaks. The sentence needs
  correcting.
* In `doctrine/plans.md` the *Wording* > 4 definition joins the prose paragraph
  itself, so "under the prose-only rule below" points nowhere there. Drop
  "below".
* The coordinate grep on the new file is case-sensitive, so a name like
  `test_c3_…` passes it. Add `-i`.
* The "never wrap" exception names two tokens. The frozen file's other raw-text
  dependencies also need one line each: "no valid Boundary B record exists",
  "**Reviewed range**" and "Reviewed range", and the opener "required when any
  of these six triggers applies:" with its blank line before "Review-only". No
  edited line carries one, so this matters only if an implementer reflows a
  paragraph.

### Disposition question left to this review

The no-plan accepted proposal's record location (*Found while planning*) is
**owed to the archive batch, not to this plan**. The gap predates the plan, and
filling it here would widen scope. Left only in an archived plan, it is lost.

### Claims checked

These hold at the reviewed commit:

* **Raw-text guards.** The five guards are named correctly at the cited lines,
  and each guard's constraint is stated correctly. Each token occurs once today:
  "cannot be bounded confidently" in `AGENTS.md`, "no valid Boundary B record
  exists" in `doctrine/dual-review.md`, "**Reviewed range**" in
  `doctrine/plans.md`, and "Reviewed range" in `dev/plans/_template.md`. Every
  "trust-ceremony surface" in `AGENTS.md` sits on one line. The six-trigger span
  stays clear: C2 inserts after the first paragraph of Boundary C, before it.
* **Frozen files.** None of the six edited files, and not the new test file, is
  among `gate_manifest.json`'s 183 `frozen_files`;
  `test_verification_boundaries.py` is. Added nodes do not redden the gate:
  `test_verify_allows_added_test` reports them as `COLLECTION-ADDED` and passes.
* **AST.** Nothing under `bootstrap/_scaffold/` changes.
* **Lockfile.** `dev/.cairn/cairn-lock.yml` tracks `AGENTS.md` and
  `dev/plans/_template.md`, not the doctrine files. A read-only
  `verify_integrity.py --target .` reports 18 findings, and both tracked files
  are already among them. "No new path" can therefore hold without finalizing.
* **Published manifest.** `scaffold.py --manifest` prints paths and modes, not
  hashes, so prose edits leave it byte-identical.
* **Neutrality.** The neutrality leg reports 74 failures, none in an edited
  file.
* **Other carriers.** No tracked file outside the deliberation record and the
  six edited files carries the boundary text (`git grep`). `check_cairn.py`'s
  loop-fidelity leg would flag a `doctrine/` reference in the shipped copy; the
  planned wording has none.
* **Twins.** Both `AGENTS.md` copies and both plan templates are edited in
  lockstep. Doctrine has no shipped twin.
* **Siblings.** `maintainer-attention`'s Part B cut removed both `AGENTS.md`
  copies from its scope (its proposal, lines 833-834). The lens-8 sentence is
  deferred by `independent-scientific-check`'s Decision. Neither sibling edits
  the `verification-commands` slot.
* **Boundary B `full`.** Reason 1 holds at `AGENTS.md:324-325`, and reason 4 at
  Revision 1's "Boundary B: `full`". The mapping names the right families. The
  other tests that mention `dual-review` (`test_loop_fidelity_gate.py`,
  `test_onboarding_review_tiers.py`, `test_presets.py`) do not read the doctrine
  file.
* **Comprehension.** Each chunk opens with a plain sentence that a reader
  outside software can follow.

### Not covered

I ran no pytest node. I did not draft the edited text to measure its line
wrapping. I did not re-measure the 57-file install family or the 182-pass
figure; Boundary B's full run covers both.

Nothing here needs the Maintainer if the findings are folded as recommended.
[PR1] restores an obligation rather than removing one, and [PR6]'s default stays
inside the Decision.

## Response to plan review -- Claude (author) -- 2026-10-18

Every finding was checked against the tree before folding, at
`AGENTS.md:204-213`, `doctrine/plans.md:289-337` and `:366-368`,
`doctrine/coordination.md:103-110` and `doctrine/session-routines.md:34-36`.
All seven are accepted, one in part. Each is answered in an operative cell, and
this table points at them.

| Finding | Disposition | Where |
|---|---|---|
| [PR1] the rewrite drops "the touched surfaces" | accepted | *Wording* > 3: only "the mapping and gates run" changes, and the full resulting sentence is quoted. *Acceptance criteria* > C3 pins the touched surfaces, which no test pinned before. |
| [PR2] three sentences still describe only a plan's record | accepted, and carried one sentence further | *Wording* > 3: (a) the new paragraph runs a trivial change "before the commit, not after"; (b) "A plan appends"; (c) the commit body carries the mode, the interpreter and every bounded field; dual-review's check sentence names the commit as the tested revision. The same finding reaches `doctrine/plans.md:366-368` ("pre/post `HEAD` both equal the full tested revision"), which a commit body can never meet; it becomes "A plan's record is valid only when…". *Acceptance criteria* > C3 adds the pins and the interpreter to the falsifier. |
| [PR3] `doctrine/plans.md` keeps "no reviewed mapping" | accepted | *Wording* > 3, `doctrine/plans.md` > Boundary A. *Acceptance criteria* > C3 reads `doctrine/plans.md`, and "code" is left for C4 so its control holds. *Sequence* > C3. |
| [PR4] pin the negative, the placement and the asymmetry; stable IDs; robust guards | accepted, except the optional install assertion | *Acceptance criteria* > "How the pins are built", C1 and C3. **Declined:** the optional install assertion. The marker check shows no edit sits in a slot or `cairn:if` region, so the template source is the installed text. Asserting on an install would tie a prose-pin file to the engine's API for no added coverage. |
| [PR5] doctrine should take the conditional claim clause | accepted | *Wording* > 1; *Found while planning* |
| [PR6] the prose-only rule on a named high-risk surface | accepted; decided, not escalated | *Found while planning* > "Decided at plan review"; *Wording* > 3 (one phrase in the prose-only paragraph, "contract or high-risk surface"; `doctrine/plans.md`'s prose paragraph); *Acceptance criteria* > C3 falsifier (b) and (c). Prose that nothing pins runs the prose gates on any surface. Prose a test or manifest pins is a substantive surface and runs full on a high-risk surface. This is the reviewer's default, made exact by item 4's definition, and it keeps Q1's purpose: a missed pin never reaches adopters. |
| [PR7] small corrections | accepted, all four | *Scope* > install family (C4's edit is inside the slot no module fills); *Wording* > 4 ("below" dropped in doctrine); *Acceptance criteria* > the new file (`grep -i`, plus `PR` and `_c[1-5]_`, since `\b` does not split `test_c3_`); *Wording* > the never-wrap list, now all six raw-text dependencies |

**The disposition question** is folded. The no-plan record location goes to the
archive batch (*Dispositions*; *Found while planning*).

**Scope.** Nothing accepted is dropped. Two edits reach text that Revision 1's
surface table did not name, and both answer a finding:
* PR2's validity sentence in `doctrine/plans.md`;
* PR6's phrase in the prose-only paragraph of both copies.

Neither moves B's default, its fence list or the six triggers. *Scope delta*
stands at `preserved`.

There is no second plan-review round. Status `revising-plan` ->
`ready-to-implement`.
