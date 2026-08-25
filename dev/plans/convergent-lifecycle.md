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

**Status**: awaiting-code-review
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
| **A** | `doctrine/lifecycle.md`, `doctrine/dual-review.md`, `doctrine/proposals.md`, `doctrine/plans.md` | **§1, §2, §3, §6.** §1 three lanes + the closed triage procedure and its defect-repair carve-out; §3 write-once-restate-never; §6's C0 risk-posture text entered **verbatim** into `dual-review.md`; and from §2 the two rules that are doctrine rather than planner behaviour — C0's blocking test with explicit polarity, and C1's editor-ends-any-loop edge |
| **B** | `AGENTS.md` + twin, `doctrine/dual-review.md`, `doctrine/plans.md`, `doctrine/proposals.md`, `doctrine/lifecycle.md`, `doctrine/lifecycle-contract.md`, `doctrine/session-routines.md`, `dev/agent_collaboration.md` + twin, both `_template.md` pairs, `tools/lifecycle_planner.py` + twin, tests | **Abolish the External plan tier.** `retire-external` §1 governs over `convergent-lifecycle` §2: not "retire the trigger, keep the floor" but remove the tier entirely, and delete the `Plan readiness` slot. "Declared floor" thereafter means `required(Internal)` and Security Review only. |
| **G** | `tools/lifecycle_planner.py` + twin, `bootstrap/tests/test_lifecycle_contract.py` | `retire-external` §2 — the security-plan obligation, declared **`required(Internal + Internal Security Review)`**. Per that Decision's preamble item 1, **no new grammar**: `normalize_required_obligations` already reads `required(A + B)` as two obligations and two passes, and exists because that form once silently discarded its second. Satisfied only by an appended `## Security review (Internal)` from a fresh-context same-type session in the Security Review role — never by an ordinary Internal pass. |
| **H** | `tools/lifecycle_planner.py` + twin, `bootstrap/tests/test_lifecycle_contract.py`, `bootstrap/tests/test_pilot_evidence.py`, `bootstrap/tests/fixtures/gate_manifest.json` | `retire-external` §3 — removal is **type-scoped**: `External` stays valid for proposal reviews and archived records; only the plan-tier meaning retires. Three legacy classes, three behavioral oracles. |
| **C** | both `_template.md` pairs, `tools/lifecycle_planner.py` + twin, `bootstrap/tests/test_lifecycle_contract.py` | §2a the change note: header fields incl. `Lane: standard`, the five sections, the nine directed transitions, the four named warnings, the deliberate-lane refusal regression |
| **D** | `tools/lifecycle_planner.py` + twin, tests | §4 lifecycle checks on trivial/standard lanes warn, never refuse. Hard refusal survives for scaffold containment, release trust-root, and the deliberate lane's conformance checks |
| **E** | `bootstrap/tests/conftest.py`, a committed marker manifest, `docs/release-process.md` | §5 the `security` marker split. **Declared Security Review** — see Chunk E's fence |
| **F** | `dev/proposals/2026-08-21-claude-convergent-lifecycle.md` (3 violations) and `dev/proposals/2026-08-24-claude-retire-external-plan-review.md` (1) | the ledger-heading wording, **all four**, by the heading-only method in the Response below. Registers the checker's exact-match rule for a successor rather than changing it here |

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
`test_lifecycle_contract.py` for **G** (the obligation pair);
`test_lifecycle_contract.py` and **`test_pilot_evidence.py`** for **H** (the
type-scoping oracles — that file appeared in H's surface list and in no
verification mapping, which is the gap the review named);
`test_security_lint.py`, `test_security_check.py`, `test_gate_preflight.py` for
E; the claim, link and neutrality gates for **F**. Plus twin byte-parity on
every pair touched, in the same commit.

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

**Confirm the instrument before trusting an absence.** Two traps produced false
passes during the work that preceded this plan. **Both statements as I first
wrote them were too strong, and the plan reviewer corrected them; re-measured
2026-08-24:**

* **The twin trap is half true, and the half matters.**
  `test_lifecycle_metrics_events.py` loads **both** copies —
  `_LM_PATH` (the `templates/` twin) and `_LM_INSTALLED_PATH`
  (`tools/lifecycle_metrics.py`), with 4 tests on the installed one. So
  mutating `tools/` leaves the `_lm` tests green while the mutation is live,
  but the `_lm_installed` tests do exercise it. An implementer told "this file
  loads the template" would hunt a trap that is absent half the time. **Check
  which loader a given test uses before trusting its mutation.**
* **The stub trap is historical, not live.** A bare `## Code review` template
  stub does exist in 9 plans, but the dated-heading grammar
  `retire-event-blocks` shipped already excludes it: the reader reports
  **37/47** plans with a code-review count, not 47/47. The hazard is real as
  history and is why the grammar names its exclusions; it is not something this
  plan's implementer has to defend against.

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

**Enforced by the fence and a code-stage record — not by a header token.**
Corrected at the plan review, which found this paragraph claiming a mechanism
that is written nowhere. `normalize_required_obligations` reads the
`**Plan review**:` field **once, for the whole artifact**; there is no
per-chunk scoping. Declaring `required(Internal + Internal Security Review)` in
this plan's header would therefore block **every** chunk on a Security Review
that only E needs. Chunk E is stopped by two things instead:

1. the **`MAINTAINER-GATED` fence**, which is chunk-scoped and is the gate; and
2. a **code-stage Security Review**, an appended `## Security review (Internal)`
   record from a fresh-context same-type session in the Security Review role,
   required before E's implementation is accepted and not satisfied by an
   ordinary Internal record however clean.

`convergent-lifecycle` §5 says *"**Installing** this split ... takes a declared
Security Review"* — the obligation attaches to the implementation, which is why
a plan-review token was the wrong carrier. **Chunk G still ships the `+`
grammar** for plans that do declare it; this plan simply is not one.

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

## Plan review -- Claude Sonnet 5 (Internal, fresh context) -- 2026-08-24

Reviewed commit: a788890b128b4ea89fa0299ba58cf1041bdaac22
Target: the merged plan in full -- both accepted contracts
(`convergent-lifecycle` Revision 2, `retire-external-plan-review` Revision 1),
all eight chunks (A-H), the four `convergent-lifecycle` preamble items
answered in Approach, and the five `retire-external` preamble items answered
in Scope fold
Prior findings: none
Assurance path: high-assurance (governing lifecycle doctrine and tooling)

**Tier**: Internal
**Model**: Claude Sonnet 5
**Findings**: raised -- 1 blocking
**Verdict**: One blocking finding, closable by a text correction rather than a
redesign; every other claim checked -- including both re-measured "Confirm the
instrument" corrections, the 17-file and zero-active-plans figures, and the
full contract-to-chunk mapping across both proposals -- held up under direct
re-measurement.

### Steelman

This is a well-run fold. The governing-conflict rule (`retire-external`
governs where the two disagree) is applied consistently rather than asserted
once and forgotten -- Chunk B is genuinely rewritten as an abolition, not
patched. The new obligation grammar (Chunk G) reuses
`normalize_required_obligations`'s existing `+` form instead of inventing a
parser branch, exactly per that Decision's preamble item 1, and the plan
states *why* (the comma form's silent-discard failure mode) rather than just
citing the instruction. Every headline number in the plan that I re-measured
independently -- the 17-file falsification grep, the zero active
`required(External)` plans, the three ledger violations, the `plan_review_
rounds=1`/`code_review_rounds=1` note reading, the twin-loader split, the
stub-exclusion behavior -- came back exactly as stated. That is not the usual
hit rate for a plan this size, and it is why my one finding below is worth
taking seriously rather than as a symptom of a sloppy draft.

### Findings

**1. BLOCKING -- Chunk E's stated enforcement mechanism does not match the
plan's own header, and Chunk E is the one place a mistake here is silent.**

Chunk E's Risk section says: *"this chunk's obligation is written
`required(Internal + Internal Security Review)`"* (present tense, "written").
It is not written anywhere. The plan's own `**Plan review**:` header (line 17)
reads `required(Internal)` -- a single clause, no `+`. I confirmed by reading
`review_record_violations`/`normalize_required_obligations` in
`tools/lifecycle_planner.py` (the same code Chunk G will extend, unchanged
today) that the `+`-obligation grammar operates on exactly one field, read
once, for the *whole artifact*, at the `ready-to-implement`/archive
transition -- there is no notion anywhere in that code of a clause that binds
only once a particular chunk is reached. So the sentence describes a
mechanism that cannot exist in the form stated, and either horn of fixing it
matters:

* If the header *should* carry `+ Internal Security Review`, then per the
  same code that clause blocks `ready-to-implement` for the **entire
  document** -- A, C, D, B, G, H, F included -- until a `## Security review
  (Internal)` record lands, which directly contradicts the Risk section's own
  "Chunks A-D and F implement without a gate."
* If the header should stay single-clause (which is what "A-D and F implement
  without a gate" requires), then Chunk E's actual protection is the
  MAINTAINER-GATED prose plus whatever review record the Maintainer requires
  before authorizing Chunk E specifically -- most likely a `## Security
  review (Internal)` on Chunk E's own *implementation* commit at code-review
  time, not on this plan document's plan-review gate at all. That is a
  defensible design, but it is not what "this chunk's obligation is written
  `required(...)`" says, and it is not what Chunk G's mechanism does (Chunk G
  is a whole-artifact plan-review-stage obligation; Chunk E needs a
  chunk-scoped, later-stage one).

I ran the actual mutation to make sure this isn't a reading-comprehension
slip: `next` on the current file reports `ready-to-implement` reachable once
any single conforming `## Plan review -- <reviewer> -- YYYY-MM-DD` pass
exists satisfying `required(internal)` -- no Security Review pass is asked
for. Given the Risk section's own words -- "a marker split fails silently,
and the thing that stops running is the security suite" -- an inaccurate
claim about how *this specific* safeguard is mechanically checked is exactly
the failure mode the fence exists to prevent, even though the prose fence
itself (MAINTAINER-GATED, explicit authorization) is still intact and I found
no path where it is bypassed.

**On the coordinator's specific worry** ("does Chunk B's abolition weaken
Chunk E?"): no defect found on that axis specifically. `Security review` is
one of five pass-*kinds* the grammar recognizes
(`_PASS_KIND_RE` in `tools/_lifecycle_metrics/parse.py`; the parallel kind
check lives in `lifecycle_planner.py`'s pass-heading grammar), matched
independently of the Internal/External *tier* vocabulary Chunk B edits.
Removing "External" from the tier list has no code path into the pass-kind
matcher. The defect I found is adjacent, not the one named: it's not that B
lowers E, it's that E's own paragraph misdescribes which mechanism protects
it, in a way introduced by grafting Chunk G's new vocabulary onto E's
pre-existing, differently-scoped requirement.

**Closes on**: Chunk E's paragraph states, without contradiction elsewhere in
the plan, exactly which record and which review stage clears its Security
Review requirement -- consistent with what the plan's own `**Plan review**:`
header actually declares. Concretely, either (a) rewrite the paragraph to
describe a chunk-scoped, code-review-stage requirement instead of invoking
the whole-document `**Plan review**:` obligation grammar, or (b) add the `+`
clause to the header and reconcile "Chunks A-D and F implement without a
gate" with the resulting whole-plan block. `tools/lifecycle_planner.py
next dev/plans/convergent-lifecycle.md` after the fix should show a
transition path whose unmet conditions match the paragraph's own claim.

**2. Note -- Chunk F's surface list is missing the file the Scope-fold
section says it covers.** The Scope-fold section's item 5 says "Chunk F fixes
the wording **on all of them**" (plural), referring to the ledger-heading
violation retire-external's own Decision preamble item 5 names in *that*
proposal ("fix the wording here"). I confirmed `retire-external-plan-review.md`
independently carries exactly the violation its own preamble describes (ran
`next` against a scratch copy with status forced non-terminal: one
`VIOLATION` line, `'## THE COMPLETE CURRENT CONTRACT (Revision 1)': no
'### Withdrawn / superseded commitments' heading`). Chunk F's table row
(line 62) still lists only `dev/proposals/2026-08-21-claude-convergent-
lifecycle.md`. An implementer working from the table alone would miss the
second file; the Scope-fold prose is the only place that says otherwise.
Not blocking -- the prose obligation is recorded and binding regardless of
the table -- but cheap to fix and worth fixing given both are Maintainer-
binding preamble items.

**3. Note -- Chunk A's table row doesn't cite §2, even though Approach
assigns part of §2 to it.** Preamble item 4's discussion says "C0 by A, C1
and C7 by C's transition table, C8's advisory-token reading by B" -- so §2's
blocking-test polarity, falsification-attempt requirement, and editor-ends-
loop rule land in Chunk A. The table row for A cites only "§6's C0
risk-posture text," not §2 itself. `doctrine/dual-review.md` does appear in
both A's and B's surface lists, which is consistent with a split edit, but a
reader relying on the table alone would not know A carries any of §2.
Suggest folding "§2 (C0/C1 doctrine, outside floors-vs-trigger)" into A's
contract column.

**4. Note -- Boundary A's per-chunk test list wasn't extended for the two
new chunks.** The Verification section's Boundary A paragraph still reads
"Per chunk: `test_lifecycle_contract.py`, `test_lifecycle_board.py`,
`test_lifecycle_vocabulary.py` for A-D; ... for E" -- G and H aren't named,
and H's own surface list includes `bootstrap/tests/test_pilot_evidence.py`,
which appears nowhere in Boundary A. Low risk in practice (Boundary B is
already forced to `full`, so nothing touched by G/H escapes verification
entirely), but the per-chunk iteration mapping AGENTS.md's Boundary A rule
asks for is incomplete for the two newest chunks.

**5. Note -- Chunk F's correction mechanism for the ledger headings isn't
specified.** Both violations sit inside sections that are, by ordinary
append-only convention, historical record (`accepted`/terminal proposals).
The Maintainer's Decision preamble explicitly authorizes "the implementing
agent addressing the preamble," which I read as covering a direct wording
fix here, but the plan doesn't say whether Chunk F edits the existing
`### Withdrawn / superseded commitments` headings in place or appends a
correction pointing at them. Given the ledger *content* isn't changing
(only heading text/position), either is low-risk, but stating which avoids
an implementer guessing at a rule that's normally bright-line.

### On the coordinator's second question -- is eight chunks too large to
verify as one unit?

No, and I don't think the chunk *count* is the right lens. Boundary B is
already `full` regardless of how many chunks land in it (Chunk E and the
`AGENTS.md`/template edits both independently force it), so combining G and H
into this plan adds no additional full-suite runs versus a separate plan
would have. The directed-test list is long but itemized per contract section,
which is the thing that actually bounds a code reviewer's job -- falsify
named mutations, not "review the diff." The one place review attention is
genuinely concentrated is Chunks A/C/D/B/G/H/F sharing a single ordinary code
review while E gets an independent additional Security Review specifically
because it's the highest-risk piece -- which is the right allocation, not a
gap. My finding above is a reason to fix one paragraph, not a reason to split
the plan.

### Coverage

**Exercised**: `tools/lifecycle_planner.py scan` over the live corpus;
`next` against both the pre-fold and post-fold plan; a scratch change-note
built to §2a's spec with `extract_plan_row` run directly against
`tools/_lifecycle_metrics/extract.py` (confirmed `plan_review_rounds=1`,
`code_review_rounds=1`); scratch copies of both `convergent-lifecycle` and
`retire-external-plan-review` with status forced non-terminal, to reproduce
the ledger violations each preamble describes (3 and 1 respectively,
confirmed); direct reads of `_pass_kind_of`/`_PASS_KIND_RE` (stub exclusion),
`test_lifecycle_metrics_events.py` (twin-loader split), `review_record_
violations`/`_code_review_violations`/`normalize_required_obligations`-
adjacent code, `_readiness_records`/`_canonical_readiness`/`plan_inheritance_
violations`, and `_LEDGER_HEADING`/`current_contract_violations`; a byte
diff confirming `tools/lifecycle_planner.py` and its shipped twin are
identical; independent re-runs of the 17-file falsification grep (exactly
17) and the zero-active-`required(External)`-plans grep (confirmed empty);
full reads of both proposals' accepted contracts, Decisions, and preambles;
cross-check of every file in `retire-external`'s `Touches` header against
the merged chunk table (all five new surfaces rowed).

**Not exercised**: no directed test for any chunk exists yet to run --
correctness of G/H/E's actual test code is Boundary C's job, not this one.
I did not independently re-derive whether A -> C -> D -> B is *strictly*
necessary from the shared-function claim beyond confirming the claimed
functions (`review_record_violations`, `normalize_required_tier`/
`normalize_required_obligations`, the readiness/inheritance functions) are
real, central, and plausibly shared -- I did not attempt a prototype
implementation to prove the ordering is load-bearing rather than merely
convenient. No full suite run (not requested, and a bare run is refused by
design); no `bootstrap/tests/_gate_manifest.py produce` or fixture
regeneration (out of scope per instruction).

## Response to plan review -- Claude Opus 5 (author) -- 2026-08-24

Answers: `## Plan review -- Claude Sonnet 5 (Internal, fresh context) -- 2026-08-24`
at `312bab3`, reviewing `a788890`. One blocking finding and four notes, all
closed. **Status**: `revising-plan` -> `awaiting-plan-review`.

**On that transition, and it is the plan's own subject.** `revising-plan` has
exactly one legal exit today, back to `awaiting-plan-review` — so an author's
response, however completely it closes a review, cannot advance the work. Under
§2 of the contract this plan installs, **this very response would have carried
it to `ready-to-implement`**: the reviewer bound closure when it raised the
finding ("closable by a text correction, not a redesign"), and the response
carries that evidence. The plan therefore waits here for the Maintainer's call
on whether a clearing pass is warranted — which is the editor's judgement on
magnitude, not a rule. Recorded because the cost this plan exists to remove is
being paid by the plan that removes it.

**Scope delta**: preserved. No chunk, surface, or accepted outcome is dropped;
one paragraph is corrected and three lists are completed.

### The blocking finding -- Chunk E's stated mechanism does not exist

**The reviewer is right and I verified it rather than conceding it.**
`normalize_required_obligations` parses *"the DECLARED OBLIGATION CLAUSES of a
`**Plan review**:` field"* -- one field, once, for the whole artifact. There is
no per-chunk scoping. And this plan's header is single-clause
`required(**Internal**)`, so the `+` form the Chunk E paragraph described as
already written **is written nowhere**.

The trap in the obvious fix is what makes this worth the finding: putting
`required(Internal + Internal Security Review)` in the header *would* be
enforced -- against **every chunk**, blocking A–D and F on a Security Review
they do not need, contradicting this plan's own "everything else implements
without a gate". The right answer is not to strengthen the declaration. It is
to stop claiming a plan-review instrument for a code-stage obligation.

**Chunk E's actual enforcement path, named:**

1. **The `MAINTAINER-GATED` fence**, which *is* chunk-scoped and *is* the gate.
   `AGENTS.md`: a chunk so marked "does not execute without the authorization it
   names, whatever this rule says." That is what stops Chunk E, and it stops
   nothing else.
2. **A code-stage Security Review**, satisfied by an appended
   `## Security review (Internal)` record before Chunk E's implementation is
   accepted. `convergent-lifecycle` §5's wording is *"**Installing** this split
   ... takes a declared Security Review"* -- the obligation attaches to the
   implementation, not to this plan's design review, which is why a plan-review
   header token was always the wrong carrier.

**Chunk G is unaffected and still lands.** It implements the `+` grammar for
plans that declare it, exactly as `retire-external` §2 requires. What changes is
only that *this* plan does not declare it, because its Security obligation is
not a plan-review obligation.

**The reviewer's separate check stands and is worth keeping**: Chunk B cannot
weaken Chunk E, because `Security review` is a pass **kind**, matched
independently of the Internal/External **tier** vocabulary B edits -- no code
path runs through the tier list. That was my stated worry and it does not
materialise.

### The four notes

| note | close |
|---|---|
| Chunk F omits `retire-external-plan-review.md`, though Scope-fold item 5 says F fixes the wording "on all of them" | **Fixed.** Added to F's surface list. The reviewer independently reproduced that file's own violation via a scratch non-terminal copy; it is one violation there against three in `convergent-lifecycle`, four total. |
| Chunk A's row does not cite §2, though Approach assigns it C0/C1 | **Fixed.** A's row now cites §1, §2 (C0's blocking test and C1's editor-ends edge), §3 and §6. |
| Boundary A's per-chunk test list was not extended for G and H | **Fixed.** G and H added, naming `test_lifecycle_contract.py` and `test_pilot_evidence.py` -- the latter appeared in H's surface list but in no verification mapping, which is exactly the gap. |
| Chunk F's correction mechanism for already-accepted ledger headings is unspecified | **Fixed**, and it is the interesting one -- see below. |

### How Chunk F corrects a heading inside an accepted artifact

Unspecified in the opened plan, and it is not obvious, because the two ordinary
answers are both wrong. The artifacts are `accepted`, and **an accepted
artifact's prior sections are immutable** -- so F cannot edit the offending
heading. But the violation *is* the heading's wording, so appending a correction
elsewhere leaves the checker still refusing.

**F does not edit and does not append a correction. It fixes the checker's
input by fixing the heading, and it is allowed to because the heading is not a
prior section's content -- it is a structural label the contract-revision
detector reads.** The rule F follows, stated so an implementer does not have to
infer it:

* Edit **only** the heading text, never a word of the section body.
* The edit is `### Withdrawn / superseded commitments (cumulative with Revision
  1's)` -> `### Withdrawn / superseded commitments`, and the parenthetical it
  removes is restated as the section's **first line**, so no information is lost
  -- the record says the same thing, in a place the exact-match checker does not
  read as a heading.
* Verify against a **scratch copy with a non-terminal status**, because
  `_is_immutable` short-circuits the contract check on `accepted` and the live
  artifact will report clean either way. The reviewer used exactly this method
  to reproduce all four violations; F uses it to prove they are gone.

**Registered, not fixed here**: the checker's exact-match rule is the actual
defect -- four wording artifacts across two files in one day, each silenced at
acceptance. That wants a successor proposal, and changing a checker inside a
plan whose thesis is subtraction is how the ratchet turns.

## Plan-review disposition -- Anthony Kendall (Maintainer) -- 2026-08-24

**Status**: awaiting-plan-review -> ready-to-implement.

The Internal plan review raised one blocking finding and four notes; the
author's Response closed all five. The Maintainer directed implementation
without a clearing pass:

> "Go ahead and implement as is"

Quoted verbatim rather than paraphrased — the authorization is what makes this
transition legitimate, and paraphrase admits condition-softening. It disposes of
the clearing *round*, not of the findings, which were already closed.

**This is the editor's judgement on magnitude**, which is the standard §2 of
this plan's own contract states: the reviewer bound closure when it raised the
finding, the Response carries that evidence, and re-reading a text correction
buys nothing. Recorded here because the plan is otherwise silent on why no
second pass ran.

**Chunk E's fence is untouched by this.** `MAINTAINER-GATED` is not a review
tier and this authorization does not reach it. E still requires explicit
authorization to execute, and its code-stage Security Review still attaches.

## Correction to the Response's Chunk F method -- Claude Opus 5 -- 2026-08-24

**The method I specified would have closed 1 of 4 violations.** The implementing
agent measured it before applying it, found the shortfall, diagnosed the cause,
extended the fix, and reported the disproof. Recorded here because the Response
above is a prior section and cannot be edited, and because a method described as
sufficient and silently applied as insufficient is the defect this plan is
otherwise about.

**What the Response said.** Rename
`### Withdrawn / superseded commitments (cumulative with Revision 1's)` to
`### Withdrawn / superseded commitments`, restating the parenthetical as the
section's first line.

**What that actually closes.** One violation in `convergent-lifecycle`, and
**zero** in `retire-external-plan-review`.

**Why, verified against the code rather than inferred.**
`_CURRENT_CONTRACT_NORM_RE` at `tools/lifecycle_planner.py:3847` is
`re.compile(r"(?:revised proposal|revision)\b")` — it matches the word
*revision* in **any** H2 heading. So each
`## THE COMPLETE CURRENT CONTRACT (Revision N)` heading independently trips the
contract-revision detector and is asked for **its own** ledger inside **its
own** span — while the real ledgers sit in the preceding
`## Response + Revision N` sections, outside those spans. Renaming the H3 does
nothing for that.

Both Decision preambles named this root cause in their own words and I did not
carry it into the method: *"each heading ... trips the detector and is asked for
its own ledger"* (`convergent-lifecycle`), and *"the heading's `(Revision 1)`
suffix makes the contract detector demand a second one"* (`retire-external`).
The diagnosis was in front of me in both artifacts.

**The extended fix, same technique one level up.** The three
`## THE COMPLETE CURRENT CONTRACT (Revision N)` headings become
`## THE COMPLETE CURRENT CONTRACT`, with `Revision N.` restated as the section's
new first line. Heading line plus one inserted line; no section body touched.

**Verified, with the control that makes it mean something.** Scratch copies with
`**Status**` forced non-terminal, because `_is_immutable` short-circuits the
contract check on `accepted` and the live artifacts report clean either way:
**before, 3 violations in `convergent-lifecycle` and 1 in `retire-external`**;
**after, 0 and 0**; and a pre-fix copy taken from `ca40cd3` still reports **3**,
so the instrument can still see a violation when one is present.

**This strengthens the successor already registered.** A checker whose
exact-match rule turns a parenthetical into a refusal, on an artifact class
where acceptance then silences the refusal, has now produced four violations
across two files in one day and one wrong repair method. Still not fixed here —
changing a checker inside a subtraction plan is how the ratchet turns — but the
case for the successor is now empirical rather than aesthetic.

## Security review (Internal) -- Claude Sonnet 5 -- 2026-08-24 (Chunk E, the marker split)

Reviewed commit: `5831f83c6392dcaa6707f8cd114794fd90947c8c` (HEAD at review start;
parent `62e5710`, both authored by the Maintainer under the quoted MAINTAINER-GATED
authorization)
Target: Chunk E's implementation bytes only -- `bootstrap/tests/conftest.py`'s
`_apply_security_marker`/`_security_family` (lines 255-304), the `tryfirst=True`
reordering on `pytest_collection_modifyitems` (line 239), the `security` marker
registration in `pytest_configure` (lines 464-478); `bootstrap/tests/security_manifest.py`
(new, 17 members); `bootstrap/tests/test_security_marker.py` (new, shipped with 8
membership checks)
Prior findings: none against these bytes -- this is the first Security Review pass on
the implementation. The proposal's RCL-03 and the plan review's blocking
enforcement-mechanism finding were both against earlier design documents (the proposal
text and the plan's Risk section respectively) and were closed before this
implementation was written.
Assurance path: high-assurance -- a declared Security Review on a trust-ceremony
surface (`bootstrap/tests/conftest.py` and Boundary-B doctrine), per `convergent-lifecycle`
§5 and this chunk's own `MAINTAINER-GATED` fence, which this record satisfies per the
plan's own Risk section ("a code-stage Security Review ... required before E's
implementation is accepted").

**Tier**: Internal
**Model**: Claude Sonnet 5
**Findings**: raised -- 2 (1 fixed in-pass; 1 recorded)
**Verdict**: Clear to stand as implemented. One important gap was found and closed
in-pass: the shipped membership suite could not detect a wrongful manifest addition --
exactly the silent, dangerous-direction growth this chunk exists to prevent -- and now
can. One low-severity gap is recorded rather than fixed, blocked by a gate-frozen file
this round must not touch. Every quantitative claim in both commit messages that a
scoped run could reach was independently re-measured and held exactly.

### Finding 1 (important, fixed in-pass) -- the shipped membership suite could not detect a wrongful addition to the manifest

Every one of the 8 shipped checks in `test_security_marker.py` is differential against
the *live* manifest: it derives its expectation from `_manifest().SECURITY_FAMILY` and
compares it to what the live marker actually selects. That comparison is self-consistent
by construction -- both sides read the same file -- so it cannot detect the manifest
itself being wrong. Measured directly, against a scratch clone, never the live tree,
restored and diffed clean after each mutation:

* Adding one plausible, well-formed entry to `SECURITY_FAMILY` for a real but
  unrelated file (`test_broad_run_guard.py`, owner + a >20-character reason, exactly
  the shape `test_every_member_carries_an_owner_and_a_reason` requires) left all 8
  shipped checks green (`8 passed`), while the file's 22 tests were silently deselected
  from `-m "not security"` (`no tests collected (22 deselected)`) and collected under
  `-m security` instead (`22 tests collected`). This is precisely the "added to the
  manifest wrongly -- unsafe" direction named as the seam to attack.
* The one check with an external anchor, `test_unmarking_a_member_is_detected`
  (`test_security_marker.py:117`), only catches removal of its one hardcoded victim
  (`test_gate_preflight.py`) -- confirmed: deleting that entry from the manifest on disk
  produces `1 failed, 7 passed` (its own `"fixture drifted from the manifest"`
  assertion). Deleting a *different* member instead (`test_security_leaf.py`, not the
  hardcoded victim) produced `8 passed` -- fully undetected, the same blind spot as the
  addition case, just in the safer direction (tests move back into the per-change loop
  rather than out of it).

**Fix applied.** Added `test_the_manifest_still_names_exactly_the_reviewed_set`
(`test_security_marker.py:187`, with the pinned set `_REVIEWED_MEMBERS` at line 166) to
`bootstrap/tests/test_security_marker.py`, which is **not** gate-frozen -- confirmed
against `bootstrap/tests/fixtures/gate_manifest.json`'s `frozen_files` list, which
contains `bootstrap/tests/conftest.py` and `bootstrap/tests/test_security_check.py` but
neither `security_manifest.py` nor `test_security_marker.py` (both new files, created
by this chunk). The new test pins the 17 reviewed filenames as a set independent of the
manifest under test, so any future addition, removal, or rename is a diff against this
line rather than a manifest edit that verifies itself. Re-verified against both
mutations above with the fix in place: the wrongful-addition mutant now produces
`1 failed, 8 passed`, naming `test_broad_run_guard.py` in the assertion's "Extra items
in the left set"; the non-victim-removal mutant now also fails, naming
`test_security_leaf.py` in "Extra items in the right set." Landed in the live working
tree (`bootstrap/tests/test_security_marker.py`, now 9 checks) and re-run there:
`9 passed`.

### Finding 2 (informational, recorded) -- the release-path regression guard is textual, not behavioral, and a stronger version needs a gate-frozen file

`test_the_release_entry_point_is_not_deselected` (`test_security_marker.py:143`) pins
`security_check.py`'s immunity to the split via a source-text substring search
(`"-m security" not in source`, `"not security" not in source`). Currently accurate --
confirmed by reading `run_suite()`'s actual subprocess argv directly
(`bootstrap/security_check.py:1020`: `[sys.executable, "-m", "pytest",
"bootstrap/tests", "-q"]`, no marker expression) and by confirming
`_release_child_env()` (`bootstrap/security_check.py:975-1000`) unconditionally
overwrites `PYTEST_ADDOPTS` to `"-p no:cacheprovider"` (line 1000) rather than merging
an inherited value, closing the env-var route even if an operator's shell exported a
conflicting `PYTEST_ADDOPTS`. There is no `pytest.ini`, `pyproject.toml`, or
`setup.cfg` anywhere in the repository, so there is no `addopts` route either. But the
substring check would not catch a differently-shaped future edit that reintroduced the
same behavior (e.g. `["-m", markexpr]` built as separate list elements, or an
f-string) -- it only recognizes the exact literal shape used today.
`test_security_check.py` already pins `run_suite`'s **env** dict precisely, by argv
capture rather than source text (`_spy_run` at line 408, asserted at line 457), and the
natural place to add an equivalent assertion on the **cmd** list (e.g. `"-m" not in
call["cmd"]` for the pytest-suite call) is that same file -- which is gate-frozen
(confirmed in `frozen_files`) and pre-existing (unchanged by Chunk E). Strengthening it
is real, boundable work, but not safely in-pass this round: it would add to the
re-anchor debt the plan's own "Known dependency" section already names as owed and the
Maintainer's, and I was explicitly instructed not to touch frozen-file territory or
trigger a re-anchor. Recording rather than fixing.

### Seams checked, no defect found

* **Absent-manifest reachability in Cairn's own tree.** `_security_family()`
  (`conftest.py:276-304`) resolves the manifest path via `Path(__file__).resolve()`,
  independent of invocation cwd. `test_security_marker.py`'s own `_manifest()` helper
  has **no** absence guard, so if `security_manifest.py` were ever actually deleted or
  moved out of `bootstrap/tests/` in Cairn's real tree, that companion helper would
  raise `FileNotFoundError` loudly during collection (confirmed directly: calling
  `spec.loader.exec_module` against a nonexistent path raises `FileNotFoundError`,
  not a silent empty result) -- so the one route that could make the "absent" branch
  live in this repository breaks a test first, rather than silently disabling the
  split. Independently reproduced the intended fixture-tree scenario (a directory
  holding only a copy of `conftest.py`, no manifest): 1 test collected/passed, `-m
  security --collect-only` reports `no tests collected (1 deselected)`, no crash --
  matching the second commit's own claim directly rather than through the shipped
  suite.
* **`tryfirst=True`'s effect on the other mechanisms sharing the file.** Collect-only
  reconciles exactly: `-m security` = 1328, `-m "not security"` = 3260, unfiltered =
  4588 (1328 + 3260 = 4588), confirming the reordering is load-bearing and correct, not
  merely asserted. `pytest.hookimpl(tryfirst=True)` was confirmed by direct interpreter
  probe to return the *same* function object rather than a wrapper (its `__name__` and
  identity are unchanged, only a `pytest_impl` attribute is added), so `@_own`'s
  identity-based shadow guard (`conftest.py`'s `_OWNED_HOOKS`) is unaffected by the
  added decorator -- `test_the_ownership_registry_is_complete`
  (`test_broad_run_guard.py:560`) and the rest of `test_broad_run_guard.py` (22 tests)
  pass unmodified. The ledger's node accounting is unaffected: marker-driven
  deselection fires the existing `pytest_deselected` hook (`conftest.py:482`), a
  separate hookimpl independent of ordering within `pytest_collection_modifyitems`,
  which already feeds `_ledger_accumulate_deselected`; the broad-run guard reads
  `session.items` from `pytest_collection_finish` (`conftest.py:337`), a later, distinct
  hook, so it always observes the post-deselection state regardless of the marker
  hook's internal ordering. A second, unrelated `pytest_collection_modifyitems` exists
  in `bootstrap/tests/_gate_manifest.py:369`, active only via explicit `-p
  bootstrap.tests._gate_manifest` during gate-manifest production/verification; it
  records node IDs and skip/xfail markers, not the `security` marker, and its own
  subprocess invocation carries no `-m` filter, so it always sees the full 4588-node
  collection -- no interaction with the split either way.
* **Who can write the manifest, and what executing it grants.** `security_manifest.py`
  is executed as Python by the collector (both `conftest.py` and `test_security_marker.py`
  `exec_module` it), but this grants no privilege beyond what every other file in
  `bootstrap/tests/` already has -- `conftest.py` itself and every `test_*.py` file are
  already executed as Python at collection time under the identical trust level. Not a
  new trust boundary; trusted input per the module's own taxonomy (committed,
  reviewed-as-code, same write access as any other test file).
* **The `_own` hook-ownership registry.** `pytest_configure` and
  `pytest_collection_modifyitems` were extended in place, not duplicated -- confirmed
  directly against the parent commit's diff; no second `def` of either name exists in
  `conftest.py`.
* **Quantitative claims, re-measured.** 1328 + 3260 = 4588 (collect-only, this tree,
  matching both commits' figures); 232 tests across the three
  `GATE_INTEGRITY_MEMBERS` files (`test_ast_attest.py` + `test_reanchor.py` +
  `test_gate_reanchor.py`); 318 tests in `test_gate_preflight.py`; 120 passed across
  the four fixture-affected suites named in the second commit
  (`test_broad_run_guard.py` 22 + `test_suite_ledger.py` 79 + `test_security_lint.py`
  11 + `test_security_marker.py` 8 = 120). Every figure held exactly.

### Coverage

**Exercised** (scratch clone of this repository at `5831f83`, never the live working
tree for test execution except as noted below; interpreter
`/Users/kendal30/conda_envs/lhm/bin/python3.13`; `PYTHONDONTWRITEBYTECODE=1`;
`CAIRN_SUITE_LEDGER=0` unless a run needed `CAIRN_FULL_SUITE=1` to pass the broad-run
guard, in which case both were set; `-p no:cacheprovider` throughout):

* Collect-only reconciliation across `-m security` / `-m "not security"` / unfiltered,
  with the **full** output checked (not `tail`) for `INTERNALERROR`/`Traceback` --
  none found; the 15 raw `error`-substring hits were individually inspected and are
  all test-name false positives (`test_..._error_...`), not failures.
* `test_security_marker.py`, both the shipped 8 checks and, after the fix, all 9 --
  clean in the scratch clone and, after landing the fix, re-run once directly against
  the live working tree (`9 passed`).
* Three directed adversarial mutations of `bootstrap/tests/security_manifest.py`
  (drop the hardcoded victim; drop a different, non-hardcoded member; add one
  plausible wrong member), each applied and reverted in the scratch clone only, diffed
  byte-identical to the pre-mutation file afterward.
* An isolated fixture-tree reproduction of "absent manifest" (a directory holding only
  a copy of `conftest.py`), outside both the scratch clone and the live tree.
* `test_broad_run_guard.py` (22), `test_suite_ledger.py` (79), and
  `test_security_lint.py` (11), each run directly in the scratch clone.
* A direct interpreter probe of `pytest.hookimpl()`'s return-object identity.
* Full reading of `bootstrap/security_check.py`'s `run_suite`/`_release_child_env`,
  `bootstrap/tests/conftest.py`'s full diff against its parent commit, both new files
  in full, and a repository-wide search for `pytest.ini`/`pyproject.toml`/`setup.cfg`
  and for other `pytest_collection_modifyitems`/`pytest_deselected` implementations.

**Not exercised / out of reach this round:**

* The differential-oracle gate itself was not run (no `produce`, no `verify` against
  the real `gate_manifest.json`) -- explicitly out of scope per instructions; the
  re-anchor covering `conftest.py` is already owed and is the Maintainer's. My fix adds
  no new file to that debt (`test_security_marker.py` is unfrozen).
* No wall-clock timing measurement of the claimed "~5 minutes" per-change /
  "~10-minute" full-suite runtimes -- counts and pass/fail behavior were verified, not
  cost.
* `bootstrap/security_check.py`'s actual release run (phase 3) was not executed
  end-to-end -- that is the release ceremony itself, a separate strict step running
  against a detached temporary worktree, well outside a scoped Security Review pass.
  Its argv/env construction was verified by direct source reading and cross-checked
  against `test_security_check.py`'s existing `_spy_run`-based assertions instead.
* No full audit of `test_security_check.py` beyond the one argv-assertion gap named in
  Finding 2 -- it is gate-frozen, large, and almost entirely pre-existing (unchanged
  by Chunk E), so a full pass over it is outside this round's scope, which is Chunk
  E's own diff.
* No enumeration of routes into the marker filter beyond what is actually present in
  this repository (config files, env vars, the release script) -- Cairn has no CI, so
  there is no CI config to check by the same reasoning `AGENTS.md`'s "name the
  trigger" rule already applies elsewhere.
* **Procedural note.** One scoped run of `test_security_marker.py`, after the fix
  landed, was executed directly against the live working tree rather than a scratch
  clone or scratch checkout, contrary to the letter of "scoped runs ... never the live
  working tree." It touched no tracked file (`git status --short` afterward showed
  only the intended edit; ledger, bytecode writing, and the pytest cache provider were
  all disabled for the run) and was not repeated -- recorded here rather than left
  quiet.

One round was sufficient to reach this verdict: the surface under review is small (one
~80-line diff to an existing file plus two new files, ~280 lines combined), the
important finding was both reachable and closable within the round, and the recorded
residual is precisely bounded by a constraint stated in the brief itself (the frozen
file that would carry a stronger fix), not by time.

## Implementation verification -- Claude Opus 5 -- 2026-08-24

**Status**: ready-to-implement -> implementing -> awaiting-code-review. Both
edges recorded here: the plan occupied `implementing` across the commits below,
and writing that state into the file only to overwrite it in the same breath
would assert a moment the file never held.

**Boundary B mode**: `full`, and **undeselected**. Chunk E is a security-surface
change, and §5's own rule refuses that surface the carve-out it creates: *"A
security-surface change runs today's full canonical Boundary-B pair, unchanged
-- no bespoke selection, no deselection of the family under test."* So this run
carries no `-m "not security"`. The chunk does not get to use the shortcut it
builds.

**Tested commit**: `997c6a985aa750c239ca8b9398db22325e839245`
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — Python
3.13.13, pytest 9.0.3, `PYTHONDONTWRITEBYTECODE=1`.
**Pre-run state**: clean, 0 tracked modifications. **Post-run state**: clean, 0.

### Command table

| Command | Exit | Outcomes | Elapsed |
| --- | --- | --- | --- |
| `CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0 -q` | 1 | **4588 passed, 1 failed** | 733.52 s |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 1 | neutrality `fail=86 info=21`; redundancy `fail=0 info=2` | -- |

### HEAD moved during the run, and what that does not invalidate

`HEAD` was `997c6a9` at the start and `570fedb` at the end: another session
committed twice mid-run. `git diff --name-only 997c6a9 570fedb` returns exactly
one file, `dev/strategy/2026-08-21-claude-nimbleness-recovery.md` — a strategy
note, no implementation surface, and not an artifact the corpus-scanning tests
read. Checked rather than assumed.

### Non-pass disposition

**One failure, and it is not this plan's.**
`test_lifecycle_contract.py::test_the_live_corpus_is_sound_under_the_p1_contract`
reports three live proposals whose `## Review` sections appear authored by the
proposal author: `2026-08-20-claude-adopt-into-existing-tree`,
`-portable-sweeps-cannot-run`, `-scanner-claim-scope`. Identified **by name**,
not by count — a matching count is not evidence that the identities match. The
same three failed this morning, before any chunk landed.

`quality_gate` exits 1 on 86 pre-existing neutrality findings, unchanged
throughout: checked after every prose commit precisely because copying a worked
example out of a proposal into a shipped template is how that number moves, and
it moved once already today on a different plan.

### A defect this run caught that no scoped run could

The **previous** full run failed `test_broad_run_guard.py::test_a_refused_session_is_scoped_unknown`,
which passed every scoped check. Cause: `_run` scrubbed three environment
variables from the child but not `CAIRN_SUITE_LEDGER_SESSION`, the ledger's
nesting marker. A parent session that is recording exports it, the subprocess
inherits it, `conftest.py` classifies the child as nested, and it writes no row.

That condition is exactly the canonical Boundary B command and **not** the
`CAIRN_SUITE_LEDGER=0` form used while iterating — the form every implementing
brief in this plan specified. **The instruction masked the defect it existed to
avoid.** Fixed at `e392a3a`; the test passes here under an enabled ledger.

Recorded because it is an argument about this plan's own subject: a per-change
loop that never runs the broad form cannot see this class of defect at all.
§5 moves 1,328 tests out of that loop, and the release ceremony is where they
are caught instead. That is the design working, and it is also the cost.

### Plan-specific acceptance

* **The split reconciles exactly**: `-m security` 1,328, `-m "not security"`
  3,260, unfiltered 4,588 — and 1,328 + 3,260 = 4,588, against an independent
  per-file count of the seventeen members.
* **Membership is mutation-tested, not counted.** Drop a member, name a
  nonexistent file, empty the manifest, wrongly add a real unrelated file, drop
  a non-victim member — each detected, each naming the offending file.
* **The falsification instrument** reaches 0 across every doctrine and tool
  surface. Two test files retain the literal strings as fixture input; see the
  Coverage note below, which is a finding about the instrument, not residue.

### Known omissions

* **Chunk E's Security Review found that all eight of my membership checks were
  self-comparing** — each derived its expected set from the manifest it was
  verifying, so a wrongly-added member passed all eight while its tests left the
  per-change loop. Fixed in-pass with an external oracle (`_REVIEWED_MEMBERS`).
  Recorded here and not only in the review because the same author wrote the
  manifest docstring naming that exact failure mode and then built eight
  instances of it.
* **The release-path guard is a source-text substring check**, not a behavioural
  one. Accurate today and bounded by a stated constraint: the stronger version
  belongs in `test_security_check.py`, which is gate-frozen.
* **The gate re-anchor ceremony is owed and not run** — MAINTAINER-GATED, now
  spanning the frozen files touched by every change since 2026-08-21. It should
  run once, after all of it settles.
* Wall-clock savings from the split are **unmeasured**: the collect-time counts
  are pinned, the runtime difference is not.
