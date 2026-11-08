# Protect functional prose by how it is edited, not by text-pin tests

**Author**: Claude Opus 5.5 (`claude-opus-5-5`; Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy -- changes shipped methodology and templates, adds a shipped tool to the install set, and removes tests from two protected files
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-08
**In brief**: Edit prose that directs agents only by exact replacement, ask every review whether a rule weakened or disappeared, ship a tool that lists removed sentences, and retire Cairn's text-pin tests.

## Decision summary

**Functional prose** is text that directs an agent or a model:
- `AGENTS.md`;
- skills and rule files;
- prompt text inside source code.

Cairn ships a lot of it. The Maintainer expects other repositories to hold
more of it as they work with language models. When such text is rewritten, a
rule can silently disappear, and a lost rule changes behavior just as a lost
line of code does.

Cairn guards its own rules today with about 170 **text-pin tests**: tests that
assert a sentence is still present. They have to be updated with every
deliberate rewording, and no accidental loss is recorded as caught.

This proposal guards functional prose at the edit and at review instead:
1. **Edit only by exact replacement.** Functional prose changes only by
   exact-match replacement or a patch, never by regenerating or re-wrapping
   the file.
2. **One review question.** Every review of such a change answers: "does any
   rule weaken or disappear?"
3. **A shipped tool** that lists the sentences a change removed or altered,
   ignoring re-wrapping, so the reviewer answers from evidence.
4. **Retire the pins.** Cairn retires its per-rule pin tests and keeps the
   checks that two copies of a file stay identical.

Costs:
- one small shipped tool to maintain;
- one review question per change to functional prose;
- the protected pin removals go under the release re-anchor already due.

No human operations are added.

## Context

The Maintainer, in chat on 2026-11-06:

> "anytime we edit something that is doctrinal as opposed to documentary,
> then we use exact text replacement period. That way we can discard the pin
> testing entirely."

and on 2026-11-08:

> "Cairn ships functional prose in ways that many repos may not. But this
> could become increasingly common with LLMs"

Measured at `176d2caf`, counting `def test_`:

| Test file | Tests |
|---|---|
| `test_review_stance_in_shipped_files.py` | 80 |
| `test_review_sweep_ships.py` | 31 |
| `contract/test_review_and_verification_rules_ship.py` | 14 |
| `contract/test_writing_rules_ship.py` | 13 |
| `test_default_security_stance.py` (protected) | 13 |
| `contract/test_model_tier_rule_ships.py` | 11 |
| `contract/test_certifying_run_rule.py` | 7 |
| the remaining three files, one test each (one protected) | 3 |
| **Total** | **172** |

From the 2026-11-06 weight review
(`dev/strategy/2026-11-06-claude-v07-weight-review.md`, Findings > Text pins):
- 48 commits touched these files, almost all to add a pin with a new rule or
  to edit one after a deliberate rewording.
- The only recorded catches are a reviewer's deliberate mutation experiment
  and one design defect predicted in review.
- Failures during iteration are not recorded, so "no recorded catch" is
  weaker than "never fired".

Some tests in these files are not pins. They check that two copies of a file
stay identical, such as
`test_review_stance_in_shipped_files.py::test_the_session_start_twins_are_byte_identical`.
Those catch real drift and stay.

The accepted PR-merge instruction check
(`dev/proposals/2026-11-03-claude-pr-merge-instruction-check.md`)
already judges a merged change's effect on agent behavior. This proposal
works earlier, at each edit and each review.

## Proposal

**Outcome 1: the rule,** in Cairn's `AGENTS.md` and the shipped
`templates/core/AGENTS.md`.
- **Defining functional prose.** Cairn's prescription layer
  (`docs/DOCUMENTATION_PLAN.md`) is the default: `AGENTS.md`, `VENDOR.md`,
  `RULES.md`, skills, rule modules and shipped templates. An adopter adds
  their own files, including source files that hold prompt text, to a list.
  The plan picks which existing Cairn config file holds that list; no new
  file.
- **Editing.** Functional prose changes only by exact-match replacement or a
  patch. A deliberate section rewrite lists the rules it removes or changes
  in its commit body.
- **Review.** Every review stage answers "does any rule weaken or
  disappear?" for functional-prose changes. The question goes in the shipped
  proposal, plan and code-review sections, worded as a reading question, not
  a fourth Foundations answer.

This is weight-review item 5. The rule replaces test machinery rather than
adding to the rule count; the rule freeze in item 1 is noted.

Proposed paths:
- `tools/prose_diff.py`

**Outcome 2: a shipped tool, `tools/prose_diff.py`.** It is standard-library
only and advisory: it reports and never blocks.
- **Input:** two revisions (default `HEAD~1..HEAD`) and the functional-prose
  list.
- **What it compares:** for Markdown and text files, the sentences in each
  revision, with whitespace normalized so a re-wrap reports nothing. For
  Python files on the list, the sentences inside string constants, read with
  `ast`, which covers prompts written in code.
- **Output:**
  - sentences removed;
  - sentences changed, shown as before and after;
  - sentences added;
  - a one-line "reflow only" when nothing but wrapping changed.
- **How it gets used:** reviewers read the output to answer the question. The
  PR-merge check may cite it.
- **Install:** it ships with the existing `dual-review` module (the plan
  confirms which module owns review guidance) and is installed by the
  scaffold.

**Outcome 3: retire Cairn's text pins.**
- Remove the pin tests in the files above.
- Keep every copy-parity test, moving it if its file empties.
- The two protected files' pins go under the release re-anchor with the
  promise-testing proposal's removals
  (`dev/proposals/2026-11-08-claude-promise-unit-testing.md`).
- **Order:** the rule and the tool land first, then a pin is removed only
  after the tool shows it reports the loss that pin guarded.

## Rationale

The pin model checks the wrong moment. Rule loss comes from rewriting, so
exact-replacement editing keeps diffs small and readable. The tool turns
"read the whole diff" into "read this list of removed sentences", and that
works for any repository, not only Cairn's own rules.

## Alternatives considered

- **Keep the pins.** Every rewording keeps costing a test edit, and adopters
  get nothing.
- **A registry of rules, each with an ID.** Precise, but it is a second copy
  of every rule to keep in sync. This is heavier than the problem.
- **Rely on the PR-merge check alone.** It runs once per merge over a large
  diff. Losses are easier to see at each small edit.
- **Ship an exact-edit script.** Agent tools already edit by exact match or
  patch, so the rule needs no script.

## Documentation / doctrine surface

- **Governing layer:** both `AGENTS.md` files.
- **Templates:** the shipped review sections.
- **Descriptive layer:** the tool's docstring and the `dual-review` module.
- **Doctrine gate:** the rule must clear the doctrine rate-limit gate
  (`docs/methodology/rationale.md` > "How the doctrine evolves under
  evidence"). The basis offered is synthesis at a routine boundary: the
  weight review, plus 48 commits of pin churn. The Maintainer judges it at
  the Decision.

## Evidence / verification plan

### Tests required

- **The tool:** contract tests for each promise, through its command line:
  - removed, changed and added sentences;
  - reflow-only;
  - string constants in Python;
  - unreadable and absent revisions reported, never silently empty.
- **For each retired pin:** mutate its sentence away in a separate copy, run
  the tool, and confirm it reports the loss.
- **Copy parity:** the parity tests still pass.
- **Install:** the install test shows the tool installs with its module.
- **Boundary B:** `wide`.

### Examples / smoke checks

- `python scripts/check_cairn.py`;
- `python bootstrap/scaffold.py --dry-run` showing the new install line.

#### Security preflight — five questions, answered in writing

- **S1 — Who supplied it?** The tool reads two revisions chosen by the
  reviewer and the project's own list. A change can edit the list to hide a
  file. The tool reports list changes first.
- **S2 — Can it fail?** Delete a sentence, and the tool must list it. That
  mutation is run for each retired pin.
- **S3 — What fires it, over what?** A reviewer runs it; it covers the
  listed files between two revisions. The shipped sentence describing it is
  checked against that.
- **S4 — Which way does it break?** A file it cannot parse is reported as
  "not compared", never as no change.
- **S5 — Who still wins?** A hostile rule added in well-formed prose. The
  tool lists it as added but cannot judge it; the review question and the
  PR-merge check must.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

- A rule loss reaches a release that a retired pin would have caught.
- Reviewers skip the question.
- The tool reports so much noise that no one reads it.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance
