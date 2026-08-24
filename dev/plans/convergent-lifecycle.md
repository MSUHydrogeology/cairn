# Plan: the convergent lifecycle

**Source proposals** — two, implemented simultaneously on Maintainer
direction, *"fold in to this plan the accepted retire-external... proposal.
Do them simultaneously."*:

* `dev/proposals/2026-08-21-claude-convergent-lifecycle.md` (accepted
  Revision 2, `47315b6`)
* `dev/proposals/2026-08-24-claude-retire-external-plan-review.md` (accepted
  Revision 1)

**Where the two conflict, `retire-external-plan-review` governs** — its own
"Relationship" section says so, and it is a strict subtraction from either
baseline.

**Status**: awaiting-plan-review
**Plan review**: required(**Internal**) — and under the rule this plan lands,
that is the only tier there is. **Basis corrected at the fold**: the External
floor was waived in `convergent-lifecycle`'s *own* Decision (`47315b6`), hours
before `retire-external`'s. That proposal's §4 claims its Decision is the
waiver; its own Decision preamble item 2 corrects it. Nothing here rests on §4.
**Last update**: 2026-08-24
**Opened**: 2026-08-24

## Why

The accepted proposal replaces the lifecycle container: three lanes chosen by a
closed triage, one design review and one code review each with a defined exit,
a change note that replaces proposal-plus-plan on the standard lane, tools that
warn instead of refusing, and the security suite moved to a release-only step in
the per-change loop.

`retire-external-plan-review` goes one step further on a single axis: a plan
review is an **Internal, fresh-context review — always**. External plan review
ceases to exist as a tier, requirement, recommendation slot, or escalation
target, and the proposal template's `Plan readiness` slot is deleted. Unchanged:
the External floor on deliberate-lane **proposal** review, the code-review floor,
Security Reviews wherever they attach, and the Maintainer's option to ask any
reader for anything — a choice is not a tier.

**This plan is written in the change note's own section order** — Why / What /
Approach / Verification / Risk — because §2a names "this proposal's own derived
plan" as the usability evidence for that grammar. It is nonetheless an ordinary
plan under the rules it replaces, as the proposal itself requires: the machinery
that would make it a note does not exist until Chunk C lands.

## What

Seven contract sections and four binding preamble items. The preamble is the
Maintainer's, recorded at the Decision and **binding on the implementer** — it
is not review commentary.

| chunk | surface | contract |
|---|---|---|
| **A** | `doctrine/lifecycle.md`, `doctrine/dual-review.md`, `doctrine/proposals.md`, `doctrine/plans.md` | §1 three lanes + the closed triage procedure and its defect-repair carve-out; §3 write-once-restate-never; §6's C0 risk-posture text entered **verbatim** into `dual-review.md` |
| **B** | `AGENTS.md` + twin, `doctrine/dual-review.md`, `doctrine/plans.md`, `doctrine/proposals.md`, `doctrine/lifecycle.md`, `doctrine/lifecycle-contract.md`, `doctrine/session-routines.md`, `dev/agent_collaboration.md` + twin, both `_template.md` pairs, `tools/lifecycle_planner.py` + twin, tests | **Abolish the External plan tier.** `retire-external` §1 governs over `convergent-lifecycle` §2: not "retire the trigger, keep the floor" but remove the tier entirely, and delete the `Plan readiness` slot. "Declared floor" thereafter means `required(Internal)` and Security Review only. |
| **G** | `tools/lifecycle_planner.py` + twin, `bootstrap/tests/test_lifecycle_contract.py` | `retire-external` §2 — the security-plan obligation, declared **`required(Internal + Internal Security Review)`**. Per that Decision's preamble item 1, **no new grammar**: `normalize_required_obligations` already reads `required(A + B)` as two obligations and two passes, and exists because that form once silently discarded its second. Satisfied only by an appended `## Security review (Internal)` from a fresh-context same-type session in the Security Review role — never by an ordinary Internal pass. |
| **H** | `tools/lifecycle_planner.py` + twin, `bootstrap/tests/test_lifecycle_contract.py`, `bootstrap/tests/test_pilot_evidence.py`, `bootstrap/tests/fixtures/gate_manifest.json` | `retire-external` §3 — removal is **type-scoped**: `External` stays valid for proposal reviews and archived records; only the plan-tier meaning retires. Three legacy classes, three behavioral oracles. |
| **C** | both `_template.md` pairs, `tools/lifecycle_planner.py` + twin, `bootstrap/tests/test_lifecycle_contract.py` | §2a the change note: header fields incl. `Lane: standard`, the five sections, the nine directed transitions, the four named warnings, the deliberate-lane refusal regression |
| **D** | `tools/lifecycle_planner.py` + twin, tests | §4 lifecycle checks on trivial/standard lanes warn, never refuse. Hard refusal survives for scaffold containment, release trust-root, and the deliberate lane's conformance checks |
| **E** | `bootstrap/tests/conftest.py`, a committed marker manifest, `docs/release-process.md` | §5 the `security` marker split. **Declared Security Review** — see Chunk E's fence |
| **F** | this plan; `dev/proposals/2026-08-21-claude-convergent-lifecycle.md` | preamble items 1 and 3 |

## Approach

**Chunk order is A → C → D → B → F, with E fenced.** B lands after C and D
because the readiness-parsing change touches the same planner functions the note
grammar and the warning demotion do; sequencing them together avoids three
rewrites of one file and three twin-parity commits.

**Preamble item 1 — resolved, and the resolution is already measured.** §2a says
notes "emit `cairn-event-v1` keyed by stem, so longitudinal metrics survive."
`retire-event-blocks` deleted that grammar. The replacement is the dated-heading
reader that proposal established, and it **already covers notes without
extension**: a change note lives at `dev/plans/<slug>.md`, `iter_plan_files`
already walks it, and a note carrying ordinary `## Plan review -- X -- <date>`
headings returns real counts. Verified 2026-08-24 against a note written to
§2a's own spec: `plan_review_rounds=1`, `code_review_rounds=1`. Chunk C states
this in the template rather than leaving two accepted contracts in
contradiction. **The justification is made true by the replacement mechanism, as
the preamble requires — not dropped.**

**Preamble item 2 — §2's justification leads with correctness, not cost.**
Chunk B's doctrine edit leads with the contradiction the Maintainer named: a
token that *forces* an External plan review is, by construction, apparatus a
solo single-agent adopter cannot staff, against `doctrine/dual-review.md`'s own
*"The bootstrap never installs more review apparatus than the team can staff."*
External's floor is "a different agent type, **or a human**", so the requirement
is always nominally satisfiable — which is why it is wrong: satisfying it bills
the Maintainer's reading time, the scarcest resource in a solo project.

**Preamble item 3 — three ledger violations.** `_LEDGER_HEADING` is an exact
string match, so `### Withdrawn / superseded commitments (cumulative with
Revision 1's)` fails it, and each `## THE COMPLETE CURRENT CONTRACT (Revision
N)` heading trips the contract-revision detector and is asked for its own
ledger. Chunk F fixes the wording. **It cannot be found by re-running the
scan**: `accepted` is terminal, `_is_immutable` short-circuits the contract
check, and the artifact now reports clean. The three sites are located by
reading, and the fix is verified by a scratch copy whose status is temporarily
non-terminal — the only way to make the checker speak. Whether the exact-match
rule is itself a defect is registered for a successor, not fixed here.

**Preamble item 4 — C0–C8 land here or nowhere.** They are carried by this
artifact, not cited as already in force. No chunk may cite C0, C1, C7 or C8 as
governing doctrine; each is *installed* by the chunk that needs it: C0 by A, C1
and C7 by C's transition table, C8's advisory-token reading by B. The correction
owed on `retire-event-blocks` was landed at `b812f28` before that proposal
archived — confirmed, not assumed.

## Scope fold -- both proposals, one plan -- 2026-08-24

Recorded because this plan was opened against one accepted proposal and now
implements two. Maintainer direction, verbatim:

> "I'd like for you to fold in to this plan the accepted retire-external...
> proposal. Do them simultaneously."

**Scope delta: widened.** Nothing from either accepted contract is dropped.

**Where they conflict, `retire-external-plan-review` governs**, by its own
Relationship section. One conflict, and it reshapes a chunk rather than adding
one: `convergent-lifecycle` §2 retires the reviewer *trigger* while preserving
declared `required(External)` plan floors as non-downgradable;
`retire-external` §1 abolishes the tier. Chunk B was written to the first and is
rewritten to the second. Read after the fold, §2's floors-vs-trigger rule still
holds — "declared floor" simply denotes `required(Internal)` and Security
Review, which is what §1 leaves standing.

**Nine binding preamble items, across two Decisions.** Both preambles are the
Maintainer's own finding records, adopted into their Decisions and explicitly
binding on the implementer. `convergent-lifecycle`'s four are answered in
Approach above. `retire-external`'s five:

* **1 — no new grammar.** Chunk G declares
  `required(Internal + Internal Security Review)`, not the comma form §2
  proposed. `normalize_required_obligations` already reads `required(A + B)` as
  two obligations and two distinct passes; it exists *because that exact form
  once silently discarded its second obligation*, which is §2's own failure
  mode, already found and fixed once. If the `+` form turns out not to express
  something §2 needs, the implementation record says what and why — it does not
  revert silently to the comma form.
* **2 — no migration is performed, and none is owed.** §4 states this
  Decision *"is that recorded waiver"* for this plan's tier. It is not: the
  waiver already existed at `47315b6`, in `convergent-lifecycle`'s own
  Decision, hours earlier. Accepting `retire-external` therefore moves **no
  accepted commitment of any sibling artifact**. The header's basis is
  corrected accordingly. `convergent-lifecycle`'s separately declared Security
  Review for the marker/conftest work survives unchanged, and Chunk E now
  declares it in §2's form.
* **3 — stale `Related` header**, already corrected in that proposal's own
  commit. Nothing owed here.
* **4 — the gate-manifest fixture edit must be a consequence, not a cover.**
  `bootstrap/tests/fixtures/gate_manifest.json` is the **test fixture**, not
  the shipped manifest, so no fence attaches. Chunk H shows the edit falls out
  of the parser change: the fixture is regenerated *after* the parser change
  and its diff is confined to the lines the parser change explains, with any
  unexplained line called out rather than absorbed.
* **5 — the ledger exact-match rule is a standing defect.** Three artifacts in
  one day carry the same wording-artifact violation, each silenced at
  acceptance because `_is_immutable` short-circuits the contract check on a
  terminal status. Chunk F fixes the wording on all of them; the checker's
  exact-match rule itself is **registered for a successor proposal, not fixed
  here** — that is a change to a checker, on a plan whose thesis is
  subtraction.

**One consequence worth stating plainly.** After Chunk B, this plan's own
`required(Internal)` is not a waiver of anything — it is the only tier that
exists. The apparatus that made the waiver necessary is what the plan removes.

## Verification

**Boundary A (iteration, scoped).** Per chunk: `test_lifecycle_contract.py`,
`test_lifecycle_board.py`, `test_lifecycle_vocabulary.py` for A–D;
`test_security_lint.py`, `test_security_check.py`, `test_gate_preflight.py` for
E. Plus twin byte-parity on every pair touched, in the same commit.

**Boundary B mode: `full`.** Not a choice: Chunk E touches
`bootstrap/tests/conftest.py` (a gate-frozen contract surface) and Boundary-B
doctrine itself, and B touches `AGENTS.md` and the install-adjacent templates.
`AGENTS.md` refuses bounded mode on either condition. **Chunk E's own rule
applies to Chunk E**: installing the split runs the *pre-change* canonical
Boundary-B pair, with no `-m "not security"` deselection of the family under
test.

**Directed tests, by section, each required red under its own mutation:**

* §2a's grammar: malformed note; raised design review without closure; raised
  code review without closure; both clearing paths.
* §2a's four named warnings emit and do **not** refuse.
* **Deliberate-lane regression**: each of those same invalid advances still
  **refuses** on a deliberate plan, unchanged.
* §2's tier rule, both directions: a recorded `DISTINCT REVIEW REQUIRED`
  imposes nothing after the change; a declared `required(External)` or a
  standing Security Review survives every path that tries to lower it.
* §5 marker membership: manifest non-empty; `-m security` collects exactly its
  members; `-m "not security"` collects none; **unmark one member and the
  membership check must fail**.
* §5 release-mode fixture: a skipped/xfailed security test makes
  `security_check.py` fail closed.

* **`retire-external` §5's falsification instrument**, literally:

      grep -rl 'Plan readiness\|required(External)' AGENTS.md doctrine templates \
        dev/proposals/_template.md dev/plans/_template.md tools scripts bootstrap \
        | grep -v archive

  **17 files pre-change** — run 2026-08-24 and independently confirmed at
  exactly 17, not carried forward from the proposal. **Empty post-change.** The
  pre-change list is committed as a fixture with the implementing change, and
  any unclassified path is printed rather than absorbed.

  **A grep cannot supply the behavioural half**, which is why §3's three oracles
  are separate acceptance criteria, each with a mutation the grep is blind to:
  (a) an archived External *proposal* review still parses in `scan` and in
  metrics — catches deleting the shared vocabulary instead of type-scoping it;
  (b) a `Plan readiness` line in an active proposal is reported as a
  recommendation and never as a plan declaration — catches grammar conflation;
  (c) a newly opened plan declaring `required(External)` draws the legacy
  warning — catches silent acceptance.

* **`retire-external` §2's directed pair**, on the `+` grammar: (a) a plan
  declaring `required(Internal + Internal Security Review)` satisfied by an
  ordinary Internal review record → the obligation reports **unmet**; (b) the
  same plan plus an appended `## Security review (Internal)` record → **clears**.
  Today mutation (a) *passes silently* — that is the defect the pair exists to
  make unreintroducible.

* **Active plans declaring `required(External)`: measured zero.** Run at the
  fold: `grep -H 'Plan review' dev/plans/*.md` reports no active plan carrying
  it, so §3's first legacy class is empty and no re-declaration is owed. The
  command is committed with the change. Should one appear before implementation,
  it is warned and the **Maintainer re-declares its tier at the next
  transition** — never silently rewritten.

**Confirm the instrument before trusting an absence.** Two traps already
measured in this repository, both of which produced false passes today:
`test_lifecycle_metrics_events.py` loads the **template** twin, not `tools/`, so
mutating `tools/` leaves tests green while the mutation is live; and a bare
`## Code review` template stub exists in 9 plans, so any heading count reporting
46/46 is counting placeholders.

## Risk

**C0 answer: yes for Chunk E, no for the rest.** E moves when security tests run
in the per-change loop — a change that is hard to undo quietly, because its
failure mode is silence: tests that stop running do not announce themselves.
A–D and F are doctrine, templates, and a planner that warns instead of refusing;
their failure mode is a noisy warning or a refused transition, both visible and
cheap to reverse.

### Chunk E — MAINTAINER-GATED

E does not execute without explicit authorization. It carries a **declared
Security Review** (`convergent-lifecycle` §5, on that proposal's own terms: it
touches `bootstrap/tests/conftest.py` and Boundary-B doctrine, both
trust-ceremony surfaces), and that floor is non-downgradable — including by
this plan.

**Declared in the obligation grammar, not as an annotation.** Per
`retire-external` §2 as corrected by its Decision preamble item 1, this chunk's
obligation is written **`required(Internal + Internal Security Review)`** and
satisfied **only** by an appended `## Security review (Internal)` record from a
fresh-context same-type session in the Security Review role. An ordinary
Internal review record does not clear it, however clean. That is the whole
point of the pair: today the wrong record clears it silently.

**The abolition in Chunk B does not touch this.** `retire-external` removes the
External plan *tier*; Security Reviews survive wherever they attach, and this
one attaches by a standing trigger on the surface, not by a reviewer's
recommendation. B and E are independent, and a reading in which B weakens E is
the hole §3's oracles exist to catch.

The reason the fence sits here and nowhere else: every other chunk fails loudly.
A marker split fails silently, and the thing that stops running is the security
suite. Chunks A–D and F implement without a gate.

### Known dependency

The gate re-anchor ceremony is already owed across the frozen files touched by
four changes landed 2026-08-21 through 2026-08-24. Chunk E adds
`bootstrap/tests/conftest.py` to that batch. This plan does not run it; it is
the Maintainer's, and it should run once after E settles rather than twice.
