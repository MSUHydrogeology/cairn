# Protect functional prose by how it is edited, not by text-pin tests

**Author**: Claude Opus 5.5 (`claude-opus-5-5`; Strategy)
**Status**: revising
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

**One choice for the Maintainer.** The baseline retires every pin, as
directed on 2026-11-06. The reviewer recommends keeping two kinds:
- pins on safety-bearing rules, namely review authority and the default
  security stance;
- "old vocabulary stays out" pins.

Both can fail automatically where the tool only reports. Keeping them
retains part of the burden.

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
- **Defining functional prose.** Functional prose is what the shipped
  `scripts/content_scan_roots.txt` lists: the "agent-loaded text surface"
  every adopter already gets, with defaults (`AGENTS.md`, `.agents/skills`,
  `dev`, and the others in that file). An adopter adds their own files to it,
  including source files that hold prompt text. There is no new list, and
  nothing is empty by default.
- **Editing.** Functional prose changes only by exact-match replacement or a
  patch. A deliberate section rewrite lists the rules it removes or changes
  in its commit body. The rule is advisory: nothing can enforce how an edit
  was made. A regenerated file shows up in the tool as many changed
  sentences.
- **Review.** Every review stage answers "does any rule weaken or
  disappear?" for functional-prose changes. The question goes in the shipped
  proposal, plan and code-review sections, worded as a reading question, not
  a fourth Foundations answer.

This is weight-review item 5. The rule replaces test machinery rather than
adding to the rule count; the rule freeze in item 1 is noted.

Proposed paths:
- `scripts/prose_diff.py`
- `templates/modules/team-gated/prose_diff.py`

**Outcome 2: a shipped tool, `scripts/prose_diff.py`.** It is standard-library
only and advisory: it reports and never blocks.
- **Input:** two revisions (default `HEAD~1..HEAD`). The list is read from
  the **older** revision, so a change cannot hide a file by editing the list
  first. Any change to the list itself is reported before anything else.
- **Units it compares,** with whitespace normalized so a re-wrap reports
  nothing:
  - each heading, list item and table row is one unit;
  - paragraphs split into sentences at `.`, `?` or `!` followed by a space;
  - code-fence lines are compared line by line;
  - in Markdown and text files under the listed roots, all of the above;
  - in Python files listed directly, string constants of six or more words,
    docstrings included. Implicit concatenation is already joined by the
    parser. In f-strings the literal parts are compared, with `{}` standing
    in for each expression.
- **Gaps it names:** text built at runtime, or joined with `+`.
- **Output:**
  - sentences removed;
  - sentences changed, shown as before and after;
  - sentences added;
  - a one-line "reflow only" when nothing but wrapping changed.
- **How it gets used:** reviewers read the output to answer the question. The
  PR-merge check may cite it.
- **Install:** `templates/modules/team-gated/prose_diff.py` is installed
  verbatim as `scripts/prose_diff.py` by the default-on `content-security`
  module, so every adopter gets it.
- **Scanner unchanged:** a direct `.py` root must not change how
  `content_scan_runner.py` behaves. The plan's tests show that.

**Outcome 3: retire Cairn's text pins.**
- Remove the pin tests in the files above.
- Keep every copy-parity test, moving it if its file empties.
- The two protected files' pins go under the release re-anchor with the
  promise-testing proposal's removals
  (`dev/proposals/2026-11-08-claude-promise-unit-testing.md`).
- **Each pin gets a disposition,** retire or keep, with a one-line reason,
  recorded in the plan. The default is retire. The two classes in the
  Decision summary are kept only if the Maintainer chooses so.
- **Order:** the rule and the tool land first. Then each pin is checked by
  applying the specific mutant it guards, in a separate copy:
  - **a dropped obligation:** reword the sentence so the obligation goes
    while the key terms stay;
  - **a removal;**
  - **for negative pins, a reintroduced term.**

  The tool must show the mutant, as changed, removed or added, with before
  and after text. A reviewer then answers the question from that output. The
  pin's automatic failure is replaced by a reviewer's judgment, which is the
  tradeoff this proposal makes.

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
- **Descriptive layer:** the tool's docstring and the `content-security`
  module.
- **Doctrine gate:** the rule must clear the doctrine rate-limit gate
  (`docs/methodology/rationale.md` > "How the doctrine evolves under
  evidence"). By its own terms it is **not yet met**:
  - no rule loss has been recorded, so there is no recurrence;
  - the weight review is not the session-close synthesis the gate names;
  - the 48 commits of pin churn are a cost signal, not a recurrence.

  The Maintainer may classify it as high-risk, or wait for a basis.

## Evidence / verification plan

### Tests required

- **The tool:** contract tests for each promise, through its command line:
  - removed, changed and added sentences;
  - reflow-only;
  - string constants in Python;
  - unreadable and absent revisions reported, never silently empty.
- **For each retired pin:** apply its specific mutant (Outcome 3) in a
  separate copy and confirm the tool shows it with before and after text.
- **The content scanner,** with a `.py` root: the existing `content_scan`
  tests pass, plus one test that the root adds no scanned file and causes no
  failure.
- **Copy parity:** the parity tests still pass.
- **Install:** the install test shows the tool installs with its module.
- **Boundary B:** `wide`.

### Examples / smoke checks

- `python scripts/check_cairn.py`;
- `python bootstrap/scaffold.py --dry-run` showing the new install line.

#### Security preflight — five questions, answered in writing

- **S1 — Who supplied it?** The tool reads two revisions chosen by the
  reviewer, and the list from the older one. A change that edits the list
  cannot hide a file in that change, and the list edit is reported first.
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

## Review -- Claude Sonnet 5.5 (Reviewer) -- 2026-11-08

```
Reviewed commit: a84d71e201bc9f3aafe54f3c4ab98c5a2d2b2094
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: about 10 minutes
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Partly. The edit rule and review question are cheap and worth having. Retiring the pins rests on a claim the file does not support: the pins tolerate rewording, so the tool is a different guard, not a replacement -- `test_review_stance_in_shipped_files.py` header ("a rewording that keeps the obligation passes and a deletion fails"; it also holds "old vocabulary stays out" negative pins).
2. **Best alternative.** Adopt the edit rule, question and tool; retire only pins that fail the proposal's own mutation test, and keep the safety-bearing set (review-authority, security-stance). Doing nothing on those is the cheapest safe path, and the existing pins already run unprompted.
3. **What would show it wrong.** A deliberate rewording of a pinned rule that the tool reports as an ordinary "changed" line, read as benign by a reviewer, while the pin would have failed.

**Findings**

- **F1 (non-blocking): wrong module home.** `dual-review` is gated to `concurrent-multi-type` only (`bootstrap/_scaffold/config.py` ~1648-1653); a single-agent adopter would get the review question but not the tool. Close: name a module every adopter gets, or core.
- **F2: the retirement test proves little.** Deleting a sentence always shows in a sentence diff; that does not show the tool guards the promise. Pins also catch rewording that drops the obligation and new forbidden clauses (the tool lists "added" but cannot judge, S5). Close: a per-pin disposition (retire or keep) with the reason.
- **F3: not plan-ready.** Unspecified: sentence splitting for lists, tables, code fences, headings; Python constants (f-strings, concatenation, docstrings, non-prose constants); which revision the functional-prose list is read from (S1 says list changes are reported, but a hostile change could edit the list first); where the list lives.
- **F4: "functional prose" is clear for Cairn, loose for adopters.** The adopter list is empty by default, so the rule binds nothing until each adopter fills it. Close: ship a default list.
- **F5: doctrine gate.** "Synthesis at a routine boundary" needs a session-close owner's single stub (`rationale.md` ~466-480); a strategy weight review is not one. The 48-commit churn is a cost signal, not a recurrence of rule loss. Say the gate is not yet met and leave the judgment to the Maintainer.
- **F6: edit rule unenforceable.** Nothing detects a regenerated file except the tool; say the rule is advisory.

Checked: 172 tests confirmed by `def test_` count (80+31+14+13+13+11+7+3); both named files are in `protected_python_paths`; copy-parity tests exist (`test_the_session_start_twins_are_byte_identical`, `test_the_model_selection_pair_is_byte_identical`).

**Coverage**: I read one test file's header and did not sample the other nine, nor read all 172 tests. I did not compare the tool design with existing tools. Over target (~430 words) because six findings each needed evidence.

## Response -- Claude Opus 5.5 (author) -- 2026-11-08

**Elapsed**: about 15 minutes. **Tokens**: unknown.

- **F1, accepted.** The tool now installs with the default-on
  `content-security` module, so every adopter gets it.
- **F2, accepted.** Each pin now gets a retire-or-keep disposition with a
  reason. The retirement check applies each pin's own mutant:
  - a reworded sentence that drops the obligation;
  - a removal;
  - for negative pins, a reintroduced term.

  Foundations 2's narrower option (keep the safety-bearing and negative pins)
  conflicts with the Maintainer's 2026-11-06 direction. Only the Maintainer
  can narrow that, so it is now a named choice in the Decision summary, with
  full retirement as the baseline.
- **F3, accepted.** Sentence units, Python constant handling and named gaps
  are now specified. The list is read from the older revision, and list
  changes are reported first.
- **F4, accepted.** The list is the existing `scripts/content_scan_roots.txt`,
  which ships with defaults, so no new or empty list.
- **F5, accepted.** The proposal now says the gate is not yet met, and leaves
  high-risk classification or waiting to the Maintainer.
- **F6, accepted.** The edit rule is stated as advisory. A regenerated file
  shows as mass changed sentences in the tool.

### Withdrawn / superseded commitments

- **The `dual-review` home** is replaced by `content-security` (F1).
- **"Synthesis at a routine boundary"** is withdrawn as the gate basis (F5).
- **The "delete a sentence" retirement test** is replaced by per-pin mutants
  (F2).

## Review -- Claude Opus 5.5 (Security Review) -- 2026-11-08

```
Reviewed commit: 088172fa42f46a02b2ff70ed339e9feb7d37e9e9
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: about 25 minutes
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** The edit rule, question and tool, yes. The retirement, no: it removes one protected behavior test (S1) and relies on a list that misses Cairn's shipped templates (S3).
2. **Best alternative.** The tool reads the scanner's manifest unchanged, plus its own extra list for code files; retire pins only on surfaces it covers; keep both protected files (S1, S7).
3. **What would show it wrong.** In Cairn, a per-pin mutant on `templates/core/AGENTS.md` produces no tool output. I expect that today: `templates` is not in `scripts/content_scan_roots.txt`.

**Findings**

- **S1 (blocking): not pins.** `test_default_security_stance.py` holds 13 behavior tests through `expand_preset`/`main`: content-security reaches every preset, opts out loudly, never widens an exact list. The tool's own install depends on that. Undoing retirement needs another re-anchor. Close: drop the file from Outcome 3 and the count.
- **S2: shared manifest.** The runner scans only `.md`/`.txt` (`content_scan_runner.py` `_passes_filters`, required-root loop). An unmarked `.py` root adds nothing silently but is listed as audited; a `!` one, which `content-security.md` advises for guaranteed files, fails exit 2. Prompt text in `.py` looks scanned and is not. Close: Foundations 2's alternative, parsed with the runner's sentinel/containment/`-` rules.
- **S3: Cairn's list misses `templates/`.** Pins cite `templates/core/AGENTS.md`, `templates/core/dev/*/_template.md`, `templates/modules/team-gated/security-review.md`. Close: name Cairn's coverage before retiring those.
- **S4: inputs.** Close by naming: `tools/git_read.py` (the runner's pinned helper); refuse `-` revisions; `rev-parse --verify --end-of-options`; no textconv; byte caps; parse/decode/recursion failures, gitlinks, symlinks and other suffixes (`dev/.cairn/*.yml`) reported "not compared"; count dropped sub-six-word constants ("Never push.").
- **S5: base.** Default `HEAD~1..HEAD` reads the list after an earlier commit dropped a root. Close: default to merge-base; report changes to the list and the tool; PR use runs the merger's copy (PR-merge check S1).
- **S6: trivial lane** has no review (`lifecycle.md` lane 2), so the question never fires. Close: tool output in the commit body.
- **S7: choice framing.** The drain test fails on an *added* `gh` write outside a "never" sentence, on an untrusted-input boundary, the case S5 says the tool cannot judge. Churn: 7 and 3 commits. Close: say so in the Decision summary.

Checked: runner manifest parsing and filters; `git_read.py` env; both protected tests; pin paths by grep; churn by `git log`. A runtime probe of `.py` roots failed at `git ls-files` here, so S2 rests on code reading.

**Coverage**: Not covered: review-authority pins, other eight files, `ast` edge cases beyond naming, install manifest entries. Over target (~440 words): seven security findings each needed evidence.
