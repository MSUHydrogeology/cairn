# Plan: the convergent lifecycle

**Source proposal**: `dev/proposals/2026-08-21-claude-convergent-lifecycle.md`
(accepted Revision 2, 2026-08-24)
**Status**: awaiting-plan-review
**Plan review**: required(**Internal**) — the Maintainer waived the External
floor at the Decision, on the record: *"No external plan review is required."*
The ordinary Internal review is unchanged.
**Last update**: 2026-08-24
**Opened**: 2026-08-24

## Why

The accepted proposal replaces the lifecycle container: three lanes chosen by a
closed triage, one design review and one code review each with a defined exit,
a change note that replaces proposal-plus-plan on the standard lane, tools that
warn instead of refusing, and the security suite moved to a release-only step in
the per-change loop.

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
| **B** | `AGENTS.md` + shipped twin, `doctrine/dual-review.md`, both templates' readiness slots, `tools/lifecycle_planner.py` + twin, tests | §2 floors-vs-trigger: retire the escalation **trigger** that converts a recorded `DISTINCT REVIEW REQUIRED` into a mandatory External plan review. **Declared floors stay non-downgradable.** |
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
Security Review** (§5, on the proposal's own terms: it touches
`bootstrap/tests/conftest.py` and Boundary-B doctrine, both trust-ceremony
surfaces), and that floor is non-downgradable under §2's own floors-vs-trigger
rule — including by this plan.

The reason the fence sits here and nowhere else: every other chunk fails loudly.
A marker split fails silently, and the thing that stops running is the security
suite. Chunks A–D and F implement without a gate.

### Known dependency

The gate re-anchor ceremony is already owed across the frozen files touched by
four changes landed 2026-08-21 through 2026-08-24. Chunk E adds
`bootstrap/tests/conftest.py` to that batch. This plan does not run it; it is
the Maintainer's, and it should run once after E settles rather than twice.
