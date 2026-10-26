# Plan: verification practice — a review reads a commit, mutation for set claims, a test scope for small fixes

**Source proposal**: `dev/proposals/archive/2026-10-17-claude-verification-practice.md`
**Status**: archived
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

## Implementation verification -- Claude (implementer) -- 2026-10-18

**Boundary B mode**: full — fixed by the plan, for the four reasons in
*Verification*. The plan edits `doctrine/` and templates, which `AGENTS.md`
names as a high-risk surface, so bounded mode refuses. The change also rewrites
Boundary B's own fence, 57 install-family tests read the shipped template, and
Revision 1 says "Boundary B: `full`".
**Tested commit**: `b712020d2f76187db729152cbf7921f010c41e29`
**Reviewed range**: `d1aacb8e..b712020d`. The base is the plan at
`ready-to-implement`. The range holds:
* **This plan's chunks:**
  * `296cdfad` C1, which also set the status to `implementing`;
  * `0a4becdb` C2;
  * `399d406d` C3;
  * `f4d4ff3c` C4.
* **Out of plan, Maintainer-directed:** `b712020d`, "AGENTS.md: code review
  is not External by default (Maintainer decision)". It rewords one sentence in
  the Review section of both `AGENTS.md` copies. It was routed to this
  implementer because the plan had `AGENTS.md` open, and committed separately,
  with the Maintainer's words quoted verbatim in its body. **It is not scope
  this plan added.** Review it as its own change.
* **Other sessions' commits.** These are in the tested tree but are not this
  plan's:
  * `c61da58b`, the maintainer-attention plan open (`dev/plans/`,
    `dev/proposals/` only);
  * `3ed57e72`, a `test_security_stack.py` fix;
  * `30ff0cd5`, a `dev/PLANNING.md` board edit.

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
Python 3.13.13, first on `PATH`.
**Pre-run state**: a detached `git worktree` at the tested commit, under this
session's scratchpad.
* `git status --porcelain` was empty, and `HEAD` equalled the tested commit.
* `refs/cairn/gate-anchor` was visible, since worktrees share refs.
* It deliberately ran neither in the shared tree, where other sessions'
  uncommitted files sit, nor in a `git archive` extraction, which lacks a
  repository.

**Post-run state**: the same `HEAD`, and `git status --porcelain` empty. The
run created only ignored caches (`.pytest_cache/`,
`bootstrap/tests/__pycache__/`). The worktree was then removed.

| Command | Exit | Outcomes | Elapsed |
|---|---:|---|---:|
| `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0 -rfEsxX` | 0 | 3347 passed; 0 failed, 0 errors, 0 skipped, 0 xfailed, 0 xpassed; 3 warnings | 614 s (617 s wall) |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 1 | neutrality fail=74 info=21; redundancy fail=0 info=0 | 1 s |
| `python scripts/check_cairn.py` | 1 | 3 issues, all pre-existing (below) | 2 s |
| `python scripts/claim_check.py <file>` on the six edited files and this plan | 0 | OK, no flags, each | under 1 s each |

`-rfEsxX` only lists any non-pass; it changes no outcome.

**Non-pass disposition**:
* **`quality_gate` exit 1: pre-existing.** All 74 neutrality failures are
  line-for-line the same set as at the base `d1aacb8e`, diffed after sorting.
  None is in a file this plan edits. Redundancy is clean.
* **`check_cairn` exit 1: pre-existing, and outside this plan.**
  * The three issues are in `dev/plans/archive/2026-08-27-code-review-c5-c6-removals.md`,
    at lines 380, 398 and 400.
  * They cite `dev/measurement/suite-runs.jsonl` and
    `dev/measurement/suite-cost.md`, which are gitignored local files
    (`.gitignore:18-19`).
  * They exist in the shared tree, where `check_cairn` reports 0, and not in a
    clean checkout of the commit. Neither the review nor `.gitignore` changes
    in the range.
  * This is the hazard rule 1 names: a figure is evidence only if it was
    measured on the commit's bytes.
* **The 3 warnings** are a deprecation inside the third-party `stevedore`
  package, not in this tree.

**Gate manifest, for the queued re-anchor (row M):**
* **Frozen files.** This plan's commits change none: each commit's files were
  checked against the manifest's `frozen_files` keys, with
  `test_verification_boundaries.py` as the known-present control. In the
  range, only another session's `3ed57e72` changes a frozen file,
  `bootstrap/tests/test_security_stack.py`.
* **Dropped nodes:** none.
* **Added nodes:** 93, all in the new, tracked
  `bootstrap/tests/test_review_and_verification_rules_ship.py`. None carries a
  skip or xfail marker.
  * `test_agents_md_carries_the_obligation[<label>-<shipped|own>]` and
    `test_removing_the_obligation_is_reported[<label>-<shipped|own>]`, for
    these 21 labels:
    * `review-reads-a-commit`, `reviewer-writes-only-its-own-record`,
      `no-reverting-commands-in-a-shared-tree`,
      `other-writes-go-to-a-separate-copy`,
      `figures-are-measured-on-the-commit`;
    * `set-claims-are-listed-from-the-tree-and-mutated`,
      `ledger-reports-each-mutant-against-a-control`,
      `ledger-never-reports-a-bare-count`,
      `equivalence-is-measured-not-argued`,
      `unmeasured-equivalence-is-a-survivor`,
      `mutation-is-otherwise-the-reviewers-choice`;
    * `boundary-b-governs-a-trivial-change`,
      `a-trivial-change-runs-before-its-commit`,
      `a-trivial-changes-record-is-its-commit-body`,
      `the-commit-body-carries-mode-and-interpreter`,
      `a-plan-appends-its-verification-section`,
      `owning-tests-are-found-by-search`,
      `bounded-record-names-touched-surfaces-and-tests`,
      `trust-ceremony-surface-is-defined`;
    * `substantive-surface-is-defined`, `pinned-prose-is-substantive`.

    That is 84 nodes.
  * `test_agents_md_omits_the_forbidden_phrasing[no-full-run-tied-to-a-reviewed-mapping-<shipped|own>]`
    and `test_inserting_the_forbidden_phrasing_is_reported[...-<shipped|own>]`:
    4 nodes.
  * `test_an_empty_file_carries_no_obligation`,
    `test_the_commit_rule_sits_in_the_review_section[shipped|own]`,
    `test_the_shipped_copy_makes_claiming_conditional` and
    `test_cairns_own_copy_claims_unconditionally`: 5 nodes.

**Plan-specific acceptance commands**:
* **Every chunk.** No chunk commit touches `test_verification_boundaries.py`,
  and it passes at each. The `{{`/`cairn:` marker check is clean for each
  chunk commit.
* **Boundary A, per chunk.** The direct readers plus the new file gave 207,
  231, 267 and 275 passed (182 at the base). The five install-structure files
  gave 307 passed at each chunk and again after `b712020d`.
* **Mutation, per chunk.** Each ran in a `git archive` extraction of the base,
  with the chunk's files overlaid, never in the shared tree. Each mutant is
  reported against an unmutated control:

  | Chunk | Control | Killed | Survived | Equivalent |
  |---|---|---:|---:|---:|
  | C1 | 25 passed | 8 | 0 | 0 |
  | C2 | 49 passed | 6 | 0 | 0 |
  | C3 | 85 passed | 10 | 0 | 0 |
  | C4 | 93 passed | 2 | 0 | 0 |

  Each mutant was killed by the pin aimed at it, checked by node ID. That
  includes the touched surfaces dropped from the bounded record, the fallback
  tied back to a reviewed mapping, Review placement, and the claim clause
  flipped either way.
* **C3 counts.** "cannot be bounded confidently" occurs once in `AGENTS.md`.
  "trust-ceremony surface" occurs twice, with the raw and collapsed counts
  equal, so it is never wrapped. `no reviewed\s+mapping` matches 0 times in
  both copies and `doctrine/plans.md`. "no valid Boundary B record exists" and
  "**Reviewed range**" each still occur once. The prose-only paragraph carries
  "contract or high-risk surface".
* **C4 control.** "substantive code surface" went from 1/1/1 to 0/0/0 in
  `doctrine/plans.md` and both plan templates. Both slots keep "reviewed
  mapping" and "full suite".
* **New file.** The case-insensitive coordinate grep is clean, and a planted
  `test_c3_x … VP1` line matches it, which is the positive control.
* **Throughout.**
  * `python bootstrap/scaffold.py --manifest` is byte-identical between
    `d1aacb8e` and `b712020d` (98 lines).
  * `python bootstrap/verify_integrity.py --target .` reports the same 18
    findings as before C1, and none was finalized.
* **The falsifier, read from the shipped copy.**
  * (a) A trivial change on an ordinary surface runs its owning tests, found
    by search, before committing. It records the mode, the interpreter, the
    touched surfaces and the files with counts in its commit body, and takes a
    Bounding verdict.
  * (b) Code or pinned prose on a surface the file names as high-risk runs the
    full suite once, before code review.
  * (c) Unpinned prose runs the prose gates.
  * No sentence sends a trivial change to a plan section.
* **Size.** The `scripts/token_budget.py` figure for `AGENTS.md` went from
  5,824 to 6,472 tokens (+648). This is information only; no cap is
  configured.

**Known omissions**:
* The new pins cover the two `AGENTS.md` copies only, as Revision 1 scopes
  them. The doctrine edits are covered by `claim_check`, `check_cairn` and the
  frozen file's existing doctrine pins, not by new mutation.
* The falsifier reading is a human reading, not a test.
* Most of the install family ran only in this full run. Boundary A ran five of
  its files per chunk.
* `b712020d`'s reworded sentence is pinned by no test. Its coverage is the
  tree-wide search, both whitespace-collapsed and line-based, and the Review
  section tests, which pass.
* The Maintainer's words quoted in `b712020d` reached this session relayed by
  the coordinating session, not directly.
* Other sessions were active on the machine during the run, so elapsed times
  may be inflated; outcomes are unaffected.

## Code review -- Claude Sonnet 5.5 (fresh session, not the implementer) -- 2026-10-18

```
Reviewed commit: 739e3aba2f65035d60937d6702328c60256ed44a
Target: d1aacb8e..739e3aba -- this plan's chunks 296cdfad (C1), 0a4becdb (C2), 399d406d (C3), f4d4ff3c (C4) and the record commit 739e3aba (C5), plus b712020d (out of plan), reviewed as its own change. Not reviewed: c61da58b, 3ed57e72, 30ff0cd5, 7d9e1637 and 5bcfa9e1, which belong to other sessions.
Prior findings: none
```

**Obligation**: Code review (the floor: not the implementing agent)
**Tier**: Internal
**Bounding**: not applicable. The record is `full`; the field adjudicates a `bounded` record.
**Findings**: raised (0 blocking, 2 medium, 6 low)
**Verdict**: ACCEPT-WITH-FOLLOWUPS -> `ready-to-archive`

Distance: a fresh session of the implementer's agent type on a different model
(this pass Sonnet 5.5; the implementing commits carry Opus 5.5). It clears the
floor and is not an External review. I did not write or implement any of it.
Interpreter for every figure: `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
Python 3.13.13. Every figure below comes from new, empty copies of the reviewed
commits (`git archive` extractions and one detached worktree) under my own
scratchpad; my first extractions reused folders an earlier session had left, and
I discarded them (see [CR7]). The shared tree got this review and the claim,
nothing else.

### In plain terms

The work does what Revision 1 and the Maintainer's answers accepted. All four
rules are in both `AGENTS.md` copies, the doctrine files carry them, the two
copies agree except where the plan said they should differ, and the recorded
test run holds up: I re-measured every figure I could and each matched.

I then tried to break the new wording 30 different ways in a throwaway copy,
and the tests caught 13 and missed 17 (every one is listed below). Most of the
misses sit in places the plan chose not to guard. But five rules that the plan or the Maintainer cared about
most are guarded by nothing, so a later edit could undo them with every test
still green. And the mutation rule uses testing words ("killed", "survived")
that no file defines, which the repo's own comprehension rule forbids.

Nothing here could do damage that is hard to undo: each finding is a wording
or test addition that can land at any time. So none blocks, and the plan can
go to archive preparation with the eight follow-ups below.

### The Boundary B record, checked against the range

* **Tested commit.** `b712020d2f76187db729152cbf7921f010c41e29` is the right
  full SHA and is an ancestor of the reviewed head. It contains the whole
  implementation range `d1aacb8e..b712020d`; `d1aacb8e` is the plan at
  `ready-to-implement`.
* **Same bytes.** Nothing outside `dev/` changed between `b712020d` and
  `739e3aba` (`git diff --stat b712020d 739e3aba -- . ':!dev'` is empty), so the
  tested bytes are the reviewed implementation bytes. The tree has since moved
  to `8e5df0f0` through other sessions' `dev/` commits only.
* **Interpreter.** Python 3.13.13 at the recorded path, confirmed by running it.
* **3,347 passed.** I did not re-run the 11-minute suite (see *Fresh full
  run*). `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --collect-only
  --quality-gate-shuffle-seed=0` collects exactly 3,347 items at both
  `b712020d` and `739e3aba`. Collected equals passed, so nothing was skipped,
  xfailed or deselected. The implementer's raw log in the shared scratchpad
  agrees (3,347 passed, 3 warnings, 614 s); that is corroboration, not an
  independent measurement.
* **Pre and post state.** Not re-observable: the worktree was removed. The
  worktree list shows no leftover, and the log's rootdir is the recorded
  worktree.
* **The 74 neutrality failures are pre-existing.** The `FAIL` set is
  line-for-line identical at `d1aacb8e`, `b712020d` and `739e3aba`
  (74 failures, 21 info; redundancy 0 and 0). None of the 8 files this plan
  edits has a hit. The instrument can match: the same output has 14 hits under
  `docs/`.
* **`check_cairn` exit 1.** At `b712020d` in a clean worktree it reports exactly
  the 3 issues the record names, all in
  `dev/plans/archive/2026-08-27-code-review-c5-c6-removals.md`, citing two gitignored
  files. **At `739e3aba` it reports 6** (finding [CR5]).
* **Frozen files.** Each of the six commits checked against the manifest's 183
  `frozen_files`, with `test_verification_boundaries.py` present as the control:
  none touched. Only `3ed57e72` (another session) touches one, in
  `bootstrap/tests/test_security_stack.py`; the re-anchor that owes is that
  session's. The frozen test file is byte-identical across the range and its 40
  nodes pass.
* **Added nodes.** 93 collected in the new file, no skip or xfail marker, and
  the coordinate grep prints nothing.
* **Published manifest and integrity.** `scaffold.py --manifest` is
  byte-identical at `d1aacb8e`, `b712020d` and `739e3aba` (98 lines).
  `verify_integrity.py --target .` prints identical output (18 findings) at all
  three.
* **Marker check.** For all five implementation commits the
  `git diff -U0 ... | grep -E '^[+-].*(\{\{|cairn:)'` check prints nothing; a
  planted marker line matches it, so the pattern can fire.
* **Phrase counts behind the raw-text guards.** "cannot be bounded
  confidently": 1 in each copy. "trust-ceremony surface": 2 raw and 2 collapsed
  in each (never wrapped). `no reviewed\s+mapping`: 0 in both copies and in
  `doctrine/plans.md`. "no valid Boundary B record exists": 1 in
  `doctrine/dual-review.md`. "**Reviewed range**": 1 in `doctrine/plans.md`;
  "Reviewed range": 1 in `dev/plans/_template.md`. "substantive code surface":
  0 in `doctrine/plans.md` and both plan templates.
* **Boundary A counts.** The five direct readers: 182 passed at `d1aacb8e`, 275
  at `739e3aba`; the difference is the 93 new nodes. The four install-structure
  files other than `test_scaffold.py` pass 240 at `739e3aba`.
* **Not re-measured:** elapsed times, the token-budget figure (information
  only), and the implementer's per-chunk mutation runs.

### Scope fidelity

* Every accepted outcome landed (Revision 1 items 1 to 4; Q1, Q2, Q3; the tests
  and smoke checks). Nothing accepted was dropped, so the plan's *Scope delta*
  of `preserved` holds.
* Nothing beyond the plan except `b712020d`. The doctrine edits are exactly the
  planned ones, including the two plan-review additions (the validity sentence
  and "contract or high-risk surface").
* **Twins agree.** The diff of the two `AGENTS.md` diffs differs only in the
  planned claim clause ("claimed first" unconditional in Cairn's copy;
  "if the project uses file claims" in the shipped copy). Both plan templates
  carry the same one-word edit. `doctrine/dual-review.md` carries the shipped
  rule-1 wording, conditional included, plus the planned reason sentence.
* **Other carriers.** `git grep` over the tree for "reviewed mapping",
  "substantive code surface" and "External ... default" finds no remaining
  carrier of the old wording outside the deliberation record, the intended plan
  templates and the frozen test.
* **Adopter reality.** A scratch install of the reviewed commit into an empty
  repository puts every new rule in the installed `AGENTS.md`, with the
  conditional claim clause, and the new text adds no `doctrine/` reference.

### The out-of-plan commit b712020d, as its own change

* **Matches the decision.** The Maintainer's quoted words are "No external by
  default." The commit removes "Code review is External by default" from both
  copies and says code review's floor is "not the implementing agent" and that
  an External code review is an escalation, never the default.
* **Matches doctrine.** The new sentence restates
  `doctrine/dual-review.md:292-295` and `doctrine/plans.md:130-134`, which were
  already right. It adds no doctrine. Those two files still agree.
* **Consistent everywhere it matters.** A case-insensitive tree search finds no
  other statement that code review is External by default. The role roster in
  `dev/agent_collaboration.md` does not assign code review to the External tier.
* **Open points.** The quoted words reached the implementer second-hand,
  relayed by the coordinating session; the coordinating session should confirm
  they are the Maintainer's. The sentence carries no guard ([CR3]).

### Falsification ledger

**What I attacked, and why a ledger.** The plan claims each rule reaches every
carrier of the old wording and that its pins fail when a clause goes. Both are
"every member of a set" claims, so I listed the set from the tree (`git grep`,
not the diff) and mutated each member in a separate copy, as the rule under
review asks. I also attacked meaning, not only phrases: reversals and deletions
in clauses the plan had not pinned.

**Control.** A fresh `git archive` extraction of `739e3aba`: the five direct
readers plus the new file, 275 passed.

**Killed (13).**

| Mutant | Killed by |
|---|---|
| drop `clean` from the forbidden commands | `no-reverting-commands-in-a-shared-tree` |
| "before the commit, not after" -> "after the commit" | `a-trivial-change-runs-before-its-commit` |
| "A plan appends" -> "Append" | `a-plan-appends-its-verification-section` |
| put "no reviewed mapping" back in Boundary B | the forbidden-phrasing pin |
| shipped copy: "claimed first" made unconditional | `test_the_shipped_copy_makes_claiming_conditional` |
| drop "never as a bare N of M killed" | `ledger-never-reports-a-bare-count` |
| drop the "not measured is a survivor" sentence | `unmeasured-equivalence-is-a-survivor` |
| drop "and prose a test or manifest pins" | `pinned-prose-is-substantive` |
| drop "the test files or nodes" from the bounded record | `bounded-record-names-touched-surfaces-and-tests` |
| drop the interpreter from the commit-body record | `the-commit-body-carries-mode-and-interpreter` |
| move rule 1 out of `## Review` | `test_the_commit_rule_sits_in_the_review_section` |
| wrap "trust-ceremony surface" across a line | frozen `test_bounded_guard_detects_a_removed_fence` |
| a second "cannot be bounded confidently" | frozen `test_operational_guard_detects_removed_full_fallback` |

Each killing node was named by ID in the run output, for both copies where the
mutant touched both.

**Survived (17).** None is reported as equivalent: these are wording edits, and
no behaviour test measured any of them as harmless.

| Mutant | Where | Matters? |
|---|---|---|
| S1 "passes under the mutation" -> "fails under the mutation" (reverses the equivalence test) | both copies | yes ([CR2]) |
| S4 prose-only rule back to "a contract surface" | both copies | yes ([CR2]) |
| S8 "unless the mapping bounds" -> "unless the plan's reviewed mapping bounds" | both copies | yes ([CR2]) |
| S9 trigger widened from set claims to "any defect" | both copies | yes ([CR2]) |
| S10 drop "the tests that own each touched surface" from Boundary A | both copies | yes ([CR2]) |
| S12 restore "Code review is External by default" | both copies | yes ([CR3]) |
| D3 `doctrine/plans.md`: restore "has no reviewed mapping" | doctrine | yes ([CR4]) |
| D4 `doctrine/plans.md`: delete the trivial-change paragraph | doctrine | yes ([CR4]) |
| S2 drop ", in a separate copy" from the mutation rule | both copies | minor |
| S3 drop "Boundary C's Bounding verdict reviews it afterwards" | both copies | minor |
| S5 drop "or a separate copy holding only it" | both copies | minor |
| S6 drop ", not a plan section" | both copies | minor |
| S7 drop "or release or security ceremony work" from the definition | both copies | minor |
| S11 drop rule 1's "The author commits ... names that commit" | both copies | minor |
| S16 drop "with counts" from the bounded record | both copies | minor |
| D1 `doctrine/dual-review.md`: drop rule 1's reason sentence | doctrine | minor |
| D2 `doctrine/dual-review.md`: reverse the equivalence test | doctrine | minor |

**Reading the ledger.** The implementer's per-chunk ledger (26 killed, 0
survived) is accurate for what it attacked: every mutant there aimed at a clause
the pins quote. The pins are obligation-level by design, and the plan says so.
What the plan's ledger cannot show is how much meaning sits just outside the
quoted phrases. Survivors S1, S4, S8, S9 and S10 are the clauses that carry
Q1, Q2, PR6 and the proposal's own falsifier, which is why [CR2] exists.

**Other falsification.**
* **The falsifier, read from the shipped copy alone.** (a), (b) and (c) of the
  plan's C3 criterion all derive as written, and no sentence sends a trivial
  change to a plan section. Two edges are left open ([CR8]).
* **Frozen guards under mutation.** The five raw-text guards behave as the plan
  says: a wrapped "trust-ceremony surface" and a second "cannot be bounded
  confidently" both turn them red.
* **Plan-reading tests at the head.** 17 test files that read `dev/plans` or the
  governing files, plus the new file and the comprehension test: 961 passed at
  `739e3aba`, no skip or xfail.

### Findings

None blocks. By the blocking test (*would shipping this cause damage that is
hard to undo?*) each is no: a wording or pin edit can land after archive.

#### [CR1] medium -- the mutation rule ships words nobody defines

**Plain.** The new rule tells a reviewer to report each "mutant" as "killed",
"survived" or "equivalent", next to an "unmutated control run". No file defines
those words, so an adopter's reviewer, and the Maintainer reading the ledger,
cannot tell what "killed" claims.

**Precision.** The rule is at `templates/core/AGENTS.md:260-269`,
`AGENTS.md:256-265`, `doctrine/dual-review.md:320-329` and the bullet at
`doctrine/plans.md:906`. A search of `AGENTS.md`, `templates/core`, `doctrine`
and `docs` for "killed", "mutant" and "survived" finds only these uses. The
shipped copy's own rule says to "define a specialist term the first time it
carries weight" (`templates/core/AGENTS.md:109-114`). "Equivalent" is half
defined by the next sentence; the other three are not.

**Closes when** each of the three places carries one parenthetical, such as "(a
mutant is a deliberate break; killed means some check fails on it, survived
means every check still passes, equivalent means the break changes no
behaviour)", with the pinned phrase "killed, survived or equivalent, beside an
unmutated control" left intact.

#### [CR2] medium -- the pins check that clauses exist, not what they say; five decisions have no guard

**Plain.** The new tests catch a deleted or reworded rule when a quoted phrase
goes. They do not catch an edit that keeps the phrase and flips its meaning, or
that removes a neighbouring clause. Five such clauses carry decisions that
people cared about, and today nothing would notice them changing back.

**Precision.** Survivors S1, S4, S8, S9, S10 in the ledger:
* **S8** is the weightiest. Revision 1's falsifier is that a reader can still
  derive "run the full suite" for a trivial change. The wording that prevents
  it is "unless the mapping bounds" (`templates/core/AGENTS.md:218`). The
  negative pin forbids only "no reviewed mapping", so putting back "unless the
  plan's reviewed mapping bounds", which a plan-less change cannot satisfy,
  passes.
* **S4** is plan review's PR6 decision (a text-only fix on a high-risk surface
  runs the prose gates), at `templates/core/AGENTS.md:276`. The plan's C3
  criterion checks it once by grep; no test holds it.
* **S9** is Q2 (mutation required only when a finding names a set): the trigger
  sentence at `templates/core/AGENTS.md:260` is unpinned although its last
  sentence ("mutation stays the reviewer's choice") is.
* **S1** reverses what "measured equivalence" means; only the heading words
  "Equivalence is measured, not argued" are pinned.
* **S10** removes Boundary A's new trivial-change mapping
  (`templates/core/AGENTS.md:206`); the pin quotes the clause after it.

**Closes when** the new file gains one entry per clause, for both copies, as
obligations or forbidden phrasings, such as: forbidden `plan's reviewed\s+mapping
bounds`; `contract or high-risk surface`; `When a finding or claim says a value
must reach every member of a set`; `passes under the mutation`; and `the tests
that own each touched surface`. Stable `ids=` as before. **This changes test
bytes, which is a Boundary C trigger; see *Fresh full run*.** A `wontfix` with a
rationale is also open if the Maintainer prefers obligation-level pins; I
recommend the pins, since the cost is five lines and one run.

#### [CR3] low -- the sentence `b712020d` fixed has no guard

**Plain.** The wrong claim "Code review is External by default" is exactly what
a careless sync of the two copies, or of an older copy, would bring back, and
no test would notice.

**Precision.** No file under `bootstrap/tests` pins "escalation", "not the
implementing agent" or "never the default" for `AGENTS.md` (searched); mutant
S12 survives. The commit body says as much, and so do *Known omissions*.

**Closes when** the new file carries an obligation `An External code review is
an escalation` and a forbidden `Code review is External by default`, for both
copies.

#### [CR4] low -- the doctrine copies of the rules are unguarded, so a drift from `AGENTS.md` goes unseen

**Plain.** The plan tests the two `AGENTS.md` files only. If someone edits the
doctrine wording later, or reverts it, no test compares the two.

**Precision.** Survivors D1 to D4. Disclosed in *Known omissions* and within
Revision 1's test scope, so this is a follow-up, not a defect. Doctrine is not
shipped, and the frozen file already pins the six-trigger tokens.

**Closes when** it takes a recorded disposition. I recommend `wontfix`, with
that rationale. `accept` (extending the new file to the labels that also appear
in the doctrine) is equally valid and adds more test bytes.

#### [CR5] low -- the record commit adds three hard `claim_check` flags and three `check_cairn` issues in a clean checkout

**Plain.** The record says `claim_check` is clean on this plan, and it is, in
the shared tree. In a clean copy of the committed plan it is not: the record
cites three paths that do not exist there. They exist only as ignored local
files in the shared tree. This is the hazard the record itself names, a figure
measured away from the commit's bytes.

**Precision.** At `b712020d`, `claim_check` on the plan is clean and
`check_cairn` reports 3 issues. At `739e3aba` in a detached worktree,
`claim_check` flags `dev/plans/verification-practice.md:975` (the tests'
cache folder), `:993` and `:994` (the gitignored suite-runs and suite-cost
files under `dev/measurement`), and `check_cairn` reports 6. In the shared
tree both pass, because those ignored files exist there. (This section names
them in words for the same reason.)

**Closes when** the three paths are written as plain words, not as backticked
paths (no meaning changes), or the correction is noted in an appended addendum
to the record. If a fresh run happens ([CR2]), the addendum is already due.

#### [CR6] low -- rule 1's "one write" does not cover the Status line the review must move

**Plain.** The rule says a reviewer's only write is its own review record,
"nothing else: no other edits". But the lifecycle has the reviewer move the
artifact's Status (this review does), which is an edit to a line that is not the
appended record.

**Precision.** `templates/core/AGENTS.md:35` ("A review moves a proposal to
`revising`") and `templates/core/dev/plans/_template.md:257` ("blocking findings
move the plan to `revising-code`") against `templates/core/AGENTS.md:87-90`. Test
runs also leave ignored caches in a tree, which "anything else that writes"
read literally forbids.

**Closes when** the sentence reads "its own review record, and the Status line
of the artifact it reviews, appended or created ..." (or equivalent) in both
copies and `doctrine/dual-review.md:118`. Pin phrase "makes one write: its own
review record" must stay.

#### [CR7] low -- the rule offers a `git archive` extraction and a worktree as equals, and they are not

**Plain.** An extraction has no repository in it, so any check that asks git a
question fails there for a reason unrelated to the code. Reusing a folder that
already holds files is also not "a copy of the reviewed commit".

**Precision.** The plan measured it (*Verification* > "Where": 34 nodes need a
repository). I reproduced it: `check_cairn.py` in an extraction dies with
`git ls-files` exit 128. In this review my first extractions went into folders
an earlier session had left; the neutrality leg read 85 failures instead of 74.
I discarded those figures and redid every measurement in new empty folders.

**Closes when** rule 1's parenthesis reads "(a fresh, empty `git archive`
extraction, or a separate worktree for anything that needs the repository)" in
both copies and `doctrine/dual-review.md`.

#### [CR8] low -- Boundary B's text still has two gaps for a change with no plan, and for an unpinned text-only fix

**Plain.** (i) The shipped copy says to name the project's interpreter and full
suite "in the plan's verification slot", which a plan-less change does not
have. (ii) A text-only fix to a high-risk surface that nothing pins is told to
run only the prose gates, yet B "governs every implementation" and a bounded
record must state "the explicit absence of any contract or trust-ceremony
surface", which is false for that fix. So it has no record it can truthfully
write.

**Precision.** (i) `templates/core/AGENTS.md:214-217`. (ii) `:226-229` and
`:231-237` against `:271-279`. The same tension existed for contract surfaces
before this plan; the PR6 phrase and the reach to trivial changes widen it.
Falsifier (c) is still met, because no sentence demands a full run; the gap is
the record.

**Closes when** (i) the sentence says where a plan-less change finds the
configured suite and interpreter (the plan template's verification slot, or the
project conventions), and (ii) one clause says a text-only fix's record is the
gates it ran and the search showing nothing pins the prose.

Nit, not numbered: three lines in the new `doctrine/plans.md` text run past 80
columns (`:300`, `:328` and `:381`); wrapping is free.

**Recommended dispositions** (the implementer's to record at archive
preparation; any `defer` needs the Maintainer's quoted authorization): `accept`
[CR1], [CR5], [CR6], [CR7], [CR8]; `accept` as pins [CR2], [CR3]; `wontfix`
[CR4]. One commit for the wording edits and one for the pins, then one fresh
full run and a short addendum to the record, would close all of it.

### Fresh full run

**Not required by any Boundary C trigger as the plan stands.**
1. A valid record exists: right tested SHA, whole range inside it, interpreter
   confirmed, non-passes dispositioned (and re-measured above).
2. No unrecorded cross-surface dependency: the 17 plan-reading test files, the
   comprehension test and the install-structure files all pass at `739e3aba`
   (961 and 240).
3. No skip, xfail or xpass: 3,347 collected equals 3,347 passed.
4. No review sharpening has changed any bytes yet.
5. No trust ceremony requires one (no release in play).
6. No concrete reason to distrust the evidence: every figure I re-measured
   matched, and the two defects I found are in the record's prose, not its
   numbers.

**One consequence to plan for.** If [CR2] or [CR3] land before archive, they
change test bytes, and the rule says a change to test bytes invalidates the
record. The run then repeats (about 11 minutes of machine time, no Maintainer
time). The wording edits alone ([CR1], [CR6] to [CR8]) touch pinned prose but
no test, executable template or fixture: re-run the plan's Boundary A mapping.

### Comprehension

For the Maintainer: rule 1 (a review reads a commit) and rules 3 and 4 (a small
fix runs the tests that own what it touched; one defined term) read plainly,
and the plan's own opening paragraph carries all four rules in everyday words.
The one place a non-specialist cannot follow is rule 2's ledger vocabulary
([CR1]). Put plainly, the rule asks a reviewer to break each place on purpose and
report, for each break, whether any check noticed. That is the kind of
sensitivity test a hydrogeologist already runs on a model, and one sentence says
so.

### Not covered

I did not re-run the full suite, the elapsed times or the token-budget figure,
and I did not re-run the implementer's per-chunk mutation runs. I did not review
`dev/PLANNING.md` row M or `CHANGELOG.md`, which are archive-time edits. I
read the doctrine edits against `AGENTS.md` and the proposal but did not mutate
them beyond D1 to D4.

## Response to code review -- Claude Sonnet 5.5 (implementer of the follow-ups) -- 2026-10-18

I did not write, implement or review this plan; I picked up the eight follow-ups
after the review's commit `a0be1e2b`. All eight are answered: seven accepted
and one `wontfix`. The wording landed in `4f1b076f` and the pins in `f93eef04`.
Both are local; nothing is pushed. Status stays `ready-to-archive`, which the
review set, and this answer carries it there: the review found nothing that
blocks, so this section moves nothing. I did not archive.

**In plain terms.** The rule now defines its own testing words. It says a
reviewer's one write includes moving the Status line, and says which kind of
copy to read from. The two gaps for a change with no plan are closed with one
clause each. Meaning is now guarded in six more places: I broke each guarded
clause on purpose, in a scratch copy of the files, and the new tests caught
every break that the old ones let through.

| Finding | Disposition | Where |
|---|---|---|
| [CR1] undefined mutation words | accept (commit `4f1b076f`) | One sentence defines "mutant", "killed", "survived" and "equivalent", placed after the pinned ledger phrase, which is intact: `AGENTS.md`, `templates/core/AGENTS.md` and `doctrine/dual-review.md`. The ledger bullet in `doctrine/plans.md` is a pointer, so it carries each term as a few words in brackets. |
| [CR2] five clauses unguarded | accept, as pins (commit `f93eef04`) | `bootstrap/tests/test_review_and_verification_rules_ship.py`, both copies: five obligations (the set-claim trigger; the equivalence test; Boundary A's trivial-change mapping; bounded mode needs a mapping; unpinned prose on a high-risk surface) and one forbidden phrasing, "plan's reviewed mapping bounds", which backs the weightiest of them. The mutation table in the record below shows each one failing under its mutant. |
| [CR3] the "External by default" sentence | accept, as an absence pin (commit `f93eef04`) | The phrase is forbidden in both copies, in any case or line wrapping, hyphens allowed. I did not add the review's positive pin on "An External code review is an escalation". `dev/proposals/2026-10-18-claude-external-is-a-maintainer-stance.md` reworks the review vocabulary and may drop the word from the usual procedure. An absence pin survives that; a pin on today's sentence would not. |
| [CR4] doctrine copies unguarded | **wontfix** | The reviewer's rationale, adopted: doctrine is not shipped, so a drift between it and `AGENTS.md` reaches no adopter; the omission is disclosed in *Known omissions* and sits inside Revision 1's test scope; and the frozen `test_verification_boundaries.py` already pins the six triggers on both doctrine files. Eligibility: it does not reach an adopter, block a release or need a Decision, and no closed artifact names it. Cost accepted: a later doctrine edit can drift from `AGENTS.md` unseen. These follow-ups were applied to the doctrine by hand, in lockstep. |
| [CR5] record cites three gitignored paths | accept (this record's commit) | An addendum in the section below, with the three paths declared as untracked. The original record text is not edited. |
| [CR6] "one write" and the Status line | accept (commit `4f1b076f`) | "(plus the artifact's Status line, where the review moves it)" in both copies and `doctrine/dual-review.md`. The pinned phrase "makes one write: its own review record" is intact. |
| [CR7] extraction and worktree offered as equals | accept (commit `4f1b076f`) | A fresh, empty folder every time. A detached `git worktree` (a second checkout of the same repository) is the default; a `git archive` extraction (plain files, no repository) is only for checks that just read files. Both copies and `doctrine/dual-review.md`. |
| [CR8] Boundary B, two gaps | accept (commit `4f1b076f`) | (i) Shipped copy only, since Cairn's copy names its commands outright: a change with no plan names the configured interpreter and suite in its commit body, taking them from the plan template's slot or the project's conventions. (ii) Both `AGENTS.md` copies and `doctrine/plans.md`: when nothing pins the prose of a text-only fix, its record is the gates run and the search that found no pin, in place of a bounded record. |
| Nit: three lines over 80 columns | accept (commit `4f1b076f`) | Rewrapped in `doctrine/plans.md`; no word changed. |

**Scope: no deviation.** Nothing accepted was dropped and nothing was added, so
*Scope delta* stands at `preserved`. The two [CR8] clauses stay inside accepted
outcomes. (i) puts the existing "Name both" at the record Boundary B already
gives a trivial change, its commit body. (ii) gives the plan-review decision on
a text-only fix to a high-risk surface a record it can truthfully write,
instead of a bounded claim of "no contract or trust-ceremony surface" that
would be false for it.

**Not closed here, as before.** Where an accepted proposal that was implemented
with no plan records its result is still unstated. Plan review judged it owed
to the archive batch (*Dispositions*), and writing it would settle a third
class of work no accepted outcome covers. [CR8] (i) is about finding the
configured suite and interpreter; it does not touch that.

**A second code-review round is not owed.** The revision introduced no known
defect: the pins were run against their own mutants, and every reader passes
on the new bytes. The pins changed test bytes, so the earlier Boundary B record
no longer covers the tree; the new record below does.

For the archive-preparation `Dispositions:` line: [CR1] accept; [CR2] accept;
[CR3] accept; [CR4] wontfix; [CR5] accept; [CR6] accept; [CR7] accept; [CR8]
accept. None needs `dev/PLANNING.md` or a Maintainer quotation: no `defer`.

## Implementation verification -- Claude Sonnet 5.5 -- 2026-10-18 (follow-ups)

**This record replaces the earlier one for the code as it now stands.** The
pins in `f93eef04` changed test bytes, and a change to test bytes invalidates a
Boundary B record. The earlier record, tested at `b712020d`, stays as written;
it is no longer the valid record for the tree.

### Addendum to the earlier record

The earlier record cites three paths in backticks that exist only as ignored
local files in the shared tree: the tests' bytecode folder, and the two
measurement files that `.gitignore` excludes. A fresh checkout does not carry
them, so there `claim_check` flagged three paths in this plan and `check_cairn`
counted them. None of the record's figures is affected. The three paths are
declared below as untracked, and the checker honours a declaration anywhere in
the file, so the earlier text stands exactly as written.

Untracked paths: `bootstrap/tests/__pycache__/`, `dev/measurement/suite-runs.jsonl`, `dev/measurement/suite-cost.md`

Measured in fresh, detached worktrees at `f93eef04` with this file in place
(the two ignored measurement files absent in the fresh rows, and created empty in the "present" row to stand in for the shared tree):

| Check | Before the addendum | After the addendum |
|---|---|---|
| `claim_check` on this plan, fresh checkout | 3 hard flags | 0 hard flags; the three paths are reported as exempted by the declaration |
| `claim_check` on this plan, with the three files present | 0 | 0 hard flags |
| `check_cairn`, fresh checkout | 6 issues | 3 issues, none in this plan |

The 3 that remain are in a closed review,
`dev/plans/archive/2026-08-27-code-review-c5-c6-removals.md` (lines 380, 398 and 400),
which cites the same two ignored measurement files. They are older than this
plan and identical at its base, and the file is outside this work, so they are
untouched. With the ignored files present, as in the shared tree,
`check_cairn` reports no issues.

### The record

**Boundary B mode**: full. The follow-ups edit both `AGENTS.md` copies and
`doctrine/`, which `AGENTS.md` names as a high-risk surface through
vendor-neutrality, and they change test bytes. Bounded mode refuses on either.
**Tested commit**: `f93eef04b94f762e5234d7609e9c23eaff46f45e`
**Reviewed range**: `a0be1e2b..f93eef04`. The base is the code review's commit.
The range holds:
* **This work:**
  * `4f1b076f`, the wording edits;
  * `f93eef04`, the pins.
* **Other sessions' commits**, in the tested tree and not this work's:
  * `42fa6804`, a `dev/` edit for the maintainer-attention plan;
  * `22dabd45`, Cairn's own model-selection mapping under `dev/.cairn`;
  * `ef0e2893`, a newly opened proposal under `dev/proposals`.

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
Python 3.13.13, first on `PATH`.
**Pre-run state**: a new detached `git worktree` at the tested commit, under
this session's own scratchpad folder.
* `git status --porcelain` was empty and `HEAD` equalled the tested commit.
* `refs/cairn/gate-anchor` was visible, since worktrees share refs.
* It did not run in the shared tree, where other sessions' uncommitted files
  sit, nor in a `git archive` extraction, which holds no repository.

**Post-run state**: the same `HEAD`, and `git status --porcelain` empty. The run created only
ignored caches, as the earlier run did. The worktree was then removed.

| Command | Exit | Outcomes | Elapsed |
|---|---:|---|---:|
| `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0 -rfEsxX` | 0 | 3384 passed; 0 failed, 0 errors, 0 skipped, 0 xfailed, 0 xpassed; 3 warnings | 1066 s (1071 s wall) |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 1 | neutrality fail=74 info=21; redundancy fail=0 info=0 | 2 s |

`-rfEsxX` only lists any non-pass; it changes no outcome.

**Non-pass disposition**:
* **`quality_gate` exit 1: pre-existing.** All 74 neutrality failures are
  line-for-line the same set, sorted and diffed, as at the pre-work base
  `42fa6804` and at the code review's measured head `739e3aba`. None is in a
  file this work edits: the five edited files have no hit, and the same output
  does show hits elsewhere, so the check could have matched. Redundancy is
  clean.
* **The 3 warnings** are a deprecation inside the third-party `stevedore`
  package, not in this tree.
* **A first run was killed and discarded.** It received SIGTERM (exit 143) 274
  s in, from outside the run: the machine was at a load average near 240 with
  other sessions' suites running. Its partial log proves nothing and is not
  used. The figures above come from a second run, in a new worktree at the
  same commit.
* **The count.** 3,384 passed is the earlier record's 3,347, plus 5 tests
  another session added in `72254d0e`, plus this work's 32.

**Plan-specific acceptance commands**:
* **Boundary A, on the final bytes.** The five direct readers plus the pin file:
  307 passed (the readers' 182, plus the pin file's 125 nodes; it was 93). The
  five install-structure files: 307 passed. The wording commit alone, against
  the previous pin file: 275 passed.
* **The files that read plans, with this record in place.** The 17 test files
  that name `dev/plans`, plus the comprehension test and the pin file, run on a
  copy of the tree holding this record: 998 passed.
* **The frozen file.** `bootstrap/tests/test_verification_boundaries.py` is
  byte-identical to its state before this work, and its 40 nodes pass in the
  readers above.
* **Mutation, against an unmutated control.** Run in a private detached
  worktree. Control: the new pin file 125 passed, the previous one 93 passed.
  Each mutant was applied to one `AGENTS.md` copy at a time, and the table shows
  the failing nodes for that copy. Each one passes under the previous file:

  | Mutant | Killed by (new pins) | Survived under the previous pins |
  |---|---|---|
  | the equivalence test reversed, "passes" to "fails" under the mutation | `an-equivalent-mutant-passes-the-behaviour-test` | yes, both copies |
  | the prose-only rule back to "a contract surface" | `unpinned-prose-on-a-high-risk-surface-runs-the-prose-gates` | yes, both copies |
  | bounded mode tied to "the plan's reviewed mapping" | `bounded-mode-needs-a-mapping-not-a-plans-reviewed-mapping` and `bounding-is-not-tied-to-a-plans-reviewed-mapping` | yes, both copies |
  | the mutation trigger widened from a set claim to any defect | `a-set-claim-is-the-mutation-trigger` | yes, both copies |
  | Boundary A's "the tests that own each touched surface" dropped | `a-trivial-change-maps-to-the-tests-that-own-its-surface` | yes, both copies |
  | "Code review is External by default" restored | `code-review-is-not-external-by-default` | yes, both copies |

  That is 6 mutants times 2 copies: 12 killed, 0 survived, 0 equivalent. For
  each, the failing nodes were the matching copy's only: the "carries" and
  "removal is reported" pair for an obligation, the "omits" and "insertion is
  reported" pair for a forbidden phrasing. The pins are on the shipped copy and
  on Cairn's own, so a mutant in one copy cannot hide behind the other.
* **Throughout.**
  * `python bootstrap/scaffold.py --manifest` is byte-identical before and
    after (98 lines).
  * `python bootstrap/verify_integrity.py --target .` reports the same 18
    findings as before, and none was finalized, `AGENTS.md` and
    `dev/plans/_template.md` among them.
  * `claim_check` is clean on all four edited files.
  * `check_cairn` and `link_check` report the same issues as before the
    wording commit: none in an edited file.
  * The marker check, `git diff -U0` over `{{` and `cairn:` lines, prints
    nothing for either commit; a planted marker line matches it.
  * The case-insensitive coordinate grep over the pin file prints nothing, and
    a planted line matches it.
* **Added nodes for the queued re-anchor (row M).** 32, all in the tracked
  `bootstrap/tests/test_review_and_verification_rules_ship.py`, none with a skip
  or xfail marker. No frozen file changed, and no node was dropped:
  * `test_agents_md_carries_the_obligation[<label>-<shipped|own>]` and
    `test_removing_the_obligation_is_reported[<label>-<shipped|own>]` for 5
    labels: `a-set-claim-is-the-mutation-trigger`,
    `an-equivalent-mutant-passes-the-behaviour-test`,
    `a-trivial-change-maps-to-the-tests-that-own-its-surface`,
    `bounded-mode-needs-a-mapping-not-a-plans-reviewed-mapping` and
    `unpinned-prose-on-a-high-risk-surface-runs-the-prose-gates` (20 nodes);
  * `test_agents_md_omits_the_forbidden_phrasing[<label>-<shipped|own>]` and
    `test_inserting_the_forbidden_phrasing_is_reported[<label>-<shipped|own>]`
    for 2 labels: `bounding-is-not-tied-to-a-plans-reviewed-mapping` and
    `code-review-is-not-external-by-default` (8 nodes);
  * `test_the_external_by_default_pin_ignores_case_and_wrapping[plain|capitals|wrapped|hyphenated]`
    (4 nodes).

**Known omissions**:
* The new pins cover the two `AGENTS.md` copies only, as before. The doctrine
  copies are covered by `claim_check`, `check_cairn` and the frozen file's
  existing doctrine pins; that is the [CR4] `wontfix`.
* The wording added for [CR1], [CR6], [CR7] and [CR8] carries no pin of its own.
  Their coverage is the readers above and the `claim_check` and `check_cairn`
  runs; the review asked for pins on [CR2] and [CR3] only.
* `check_cairn` still exits 1 in a fresh checkout, on the 3 issues in the closed
  review named above. They are not this plan's, and the file that would close
  them, that review or `dev/.cairn/claim-check-allow.json`, is not one this
  work edits.
* Other sessions were active on the machine during the run, so elapsed times
  may be inflated; outcomes are unaffected.

## Archive -- 2026-10-18

`Dispositions: accept x5, wontfix x3, defer x0` — restated over
the whole record, since sections were appended after *Dispositions*. Status
`ready-to-archive` -> `archived`; the plan moves to `dev/plans/archive/`.

* **accept — Revision 1, items 1 to 4 and Q1 to Q3.** Delivered in C1 to C4
  (`296cdfad`, `0a4becdb`, `399d406d`, `f4d4ff3c`). Boundary B, mode `full`, at
  `739e3aba`, and again at `f93eef04` once the follow-ups changed test bytes:
  3,384 passed under Python 3.13.13. `b712020d` ("code review is not External
  by default") was a Maintainer-directed change outside the plan, reviewed as
  its own change and pinned by the follow-ups.
* **accept — plan review [PR1] to [PR7]**, folded into the operative cells before
  work began (*Response to plan review*).
* **accept — code review [CR1] to [CR3], [CR5] to [CR8] and the line-length
  nit.** Wording in `4f1b076f`, pins in `f93eef04`, the record and its
  addendum in `a0810700`.
* **accept — chunk M's board note.** No frozen file changed in any commit of the
  range, checked against the manifest's `frozen_files` keys with
  `bootstrap/tests/test_verification_boundaries.py` as the positive control.
  The 125 nodes of `bootstrap/tests/test_review_and_verification_rules_ship.py`
  join the queued re-anchor row on `dev/PLANNING.md` in the archive commit. The
  ceremony stays that row's: Maintainer-only, and not performed here.
* **wontfix — [PR4]'s optional install assertion.** No edit sits in a slot or
  `cairn:if` region, so the template source is the installed text; an assertion
  on an installed tree would tie a prose-pin file to the engine's API for no
  added coverage. It reaches no adopter, blocks no release and needs no
  Decision.
* **wontfix — [CR4]**, the doctrine copies carry no pins of their own. Doctrine
  is not shipped, so drift from `AGENTS.md` reaches no adopter, and the frozen
  `test_verification_boundaries.py` already pins the six triggers on both
  doctrine files. Reasoning in *Response to code review*.
* **wontfix — #12 by tooling**, a helper that extracts the reviewed commit or a
  hook that refuses `git restore`. The accepted proposal declined it with its
  reason and a revival condition ("build it if the rule fails in practice",
  Revision 1 > Alternatives considered), and the Decision accepted Revision 1.
  It reaches no adopter, blocks no release and needs no Decision, and no
  disposition block names it. If a reviewer's write again reverts an author's
  uncommitted work after this rule shipped, file a new issue citing #12.
* **accept — where an accepted proposal implemented with no plan records its
  Boundary B result.** Found at plan time (*Found while planning*) and owed to
  this archive by plan review; it is neither "a trivial change, with no
  proposal or plan" nor a plan, so the shipped text gave its record no home.
  It was outside the accepted scope, so the Maintainer's allowance widened the
  plan by one sentence instead of deferring it, and `941cb34d` landed it in both
  `AGENTS.md` copies and `doctrine/plans.md`: the record is the commit body, as
  for a trivial change, and if fewer than all the tests ran, the code
  reviewer's Bounding verdict rules on whether the tests chosen were enough.
  Prose only, with no new pin and no test that reads the new words:
  `test_verification_boundaries.py`, the pin file and four other direct readers
  307 passed, the five install-structure files 307 passed, and `claim_check`,
  `check_cairn` and the neutrality gate (74, unchanged) clean on the edited
  files. `doctrine/dual-review.md` was outside the allowance, and its Boundary C
  opening still names only "a trivial change's commit body". The Maintainer's
  allowance, relayed by the coordinating session, quoted verbatim, in answer to
  a recommendation to fix it in this plan (the recommendation's full text is in
  the body of `941cb34d`):

  > "Go with your instincts on plan A."

**Left to the Maintainer, and not deferred work.** Issues #12, #17 and #25 stay
open until the Maintainer closes them after the push; they are the live home
until then.

**Evidence shipped**: the wording in both `AGENTS.md` copies,
`doctrine/dual-review.md`, `doctrine/plans.md` and both plan templates; the 125
pins in `bootstrap/tests/test_review_and_verification_rules_ship.py`, with the
per-chunk and follow-up mutation runs recorded; both Boundary B records; and
the one-sentence record rule for a proposal built with no plan (`941cb34d`).
**Evidence deferred**: none was planned. The known omissions in the two records (unpinned doctrine
copies, and unpinned wording for [CR1], [CR6], [CR7], [CR8]) were never planned
checks; [CR4] is the `wontfix` above. **Deferred evidence home**: not
applicable.

**Fidelity sign-off.** The landed commits `296cdfad`, `0a4becdb`, `399d406d`
and `f4d4ff3c` match the accepted `## Revision 1` of
`dev/proposals/archive/2026-10-17-claude-verification-practice.md`, which
governs, as ratified by the Decision of 2026-10-18. Two byte-level choices
(*Found while planning*) and two additions from plan review ([PR2], [PR6])
deliver outcomes that Revision 1's wording would have missed, and `941cb34d`
is the one scope addition, allowed by the Maintainer as quoted above. *Scope
delta* stays `preserved`: nothing accepted was dropped.

**The lasting truth.** A rule is only as usable as its worst-served case: the
full-suite default priced a small fix out of the rule, and a record location
named for plans alone left the case beside them with none. Each was found by
reading the shipped text as an adopter would, with no plan and no doctrine
open.
