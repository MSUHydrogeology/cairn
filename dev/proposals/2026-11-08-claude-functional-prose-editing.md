# Protect functional prose by how it is edited, not by text-pin tests

**Author**: Claude Opus 5.5 (`claude-opus-5-5`; Strategy)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy -- changes shipped methodology and templates, adds two shipped tools (one writes files) to the install set, and removes tests from a protected file
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-08
**In brief**: Edit prose that directs agents only by exact replacement, ask every review whether a rule weakened or disappeared, ship an exact text replacer and a tool that lists removed sentences, and retire Cairn's text-pin tests.

## Decision summary

**Functional prose** is text that directs an agent or a model:
- `AGENTS.md`;
- skills and rule files;
- prompt text inside source code.

Cairn ships a lot of it. The Maintainer expects other repositories to hold
more of it as they work with language models. When such text is rewritten, a
rule can silently disappear, and a lost rule changes behavior just as a lost
line of code does.

Cairn guards its own rules today with about 160 **text-pin tests**: tests that
assert a sentence is still present. They have to be updated with every
deliberate rewording, and no accidental loss is recorded as caught.

This proposal guards functional prose at the edit and at review instead:
1. **Edit only by exact replacement.** Functional prose changes only by
   exact-match replacement or a patch, never by regenerating or re-wrapping
   the file.
2. **One review question.** Every review of such a change answers: "does any
   rule weaken or disappear?"
3. **A shipped exact replacer,** `scripts/exact_replace.py`. It changes a
   file only where the old text appears exactly once, and writes atomically.
   Any agent or person can use it, whatever their editing tool.
4. **A shipped report tool** that lists the sentences a change removed or
   altered, ignoring re-wrapping, so the reviewer answers from evidence.
5. **Retire the pins.** Cairn retires its per-rule pin tests and keeps the
   checks that two copies of a file stay identical.

**Pins kept.** The Maintainer kept the drain-mode pin in chat on
2026-11-08: "I accept your drain mode pin argument." Every other pin retires,
as directed on 2026-11-06. Reviewers had recommended keeping three kinds,
because each can fail automatically where the tool only reports:
- **The drain-mode rules pin** (`test_session_start_drain_rules.py`,
  protected). It fails when text that writes to an issue appears in drain
  mode's untrusted-input rules without "never". That is added hostile text,
  which the tool lists but cannot judge. It changed in 3 commits.
- **The review-authority pins.**
- **"Old vocabulary stays out" pins.**

The drain-mode pin stays as a genuine safety property. The review-authority
and old-vocabulary pins retire unless the Decision says otherwise.
`test_default_security_stance.py` is no longer in this proposal: it tests
installer behavior, not text.

Costs:
- two small shipped tools to maintain;
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
| `contract/test_model_tier_rule_ships.py` | 11 |
| `contract/test_certifying_run_rule.py` | 7 |
| the remaining three files, one test each (one protected) | 3 |
| **Total** | **159** |

From the 2026-11-06 weight review
(`dev/strategy/2026-11-06-claude-v07-weight-review.md`, Findings > Text pins):
- 48 commits touched these files, almost all to add a pin with a new rule or
  to edit one after a deliberate rewording.
- The only recorded catches are a reviewer's deliberate mutation experiment
  and one design defect predicted in review.
- Failures during iteration are not recorded, so "no recorded catch" is
  weaker than "never fired".

`test_default_security_stance.py` (13 tests) was counted at opening and is
removed: it runs the installer, so it is a behavior test (Security Review
S1).

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
- **Defining functional prose.** Functional prose is two lists together:
  - **the content scanner's list,** `scripts/content_scan_roots.txt`, which
    every adopter already gets with defaults (`AGENTS.md`, `.agents/skills`,
    `dev` and the others in that file). It is read only, and its meaning is
    unchanged;
  - **an extra list,** `scripts/prose_roots.txt`, for anything else: source
    files that hold prompt text, or folders the scanner doesn't audit, such
    as Cairn's own `templates/`. It ships from
    `templates/modules/team-gated/prose_roots.txt` with its own header line,
    `# prose-roots v1`, and no roots, because the scanner's list supplies the
    defaults. An empty list is valid. (Security Review S2, S3; second pass
    N1.)
  - **How the list is read.** The text of each list comes from the base
    revision through git, not from disk, and each line uses the same path
    rules as the scanner's: repository-relative, no absolute paths, no `..`.
    A `!` line has no meaning in this list and is reported as invalid. Every
    root is optional.
- **Editing.** Functional prose changes only by exact-match replacement or a
  patch. That means an agent tool that edits by exact match, or the shipped
  `scripts/exact_replace.py` (Outcome 4). A deliberate section rewrite lists
  the rules it removes or changes in its commit body. The rule is advisory:
  nothing can enforce how an edit was made. A regenerated file shows up in
  the tool as many changed sentences.
- **Trivial edits.** The trivial lane has no review, so the review question
  never fires there (Security Review S6). A trivial-lane edit to functional
  prose therefore puts the report tool's output in its commit body. If that
  output shows a removed or changed rule sentence, the edit is not trivial.
- **Review.** Every review stage answers "does any rule weaken or
  disappear?" for functional-prose changes. The question goes in the shipped
  proposal, plan and code-review sections, worded as a reading question, not
  a fourth Foundations answer.

This is weight-review item 5. The rule replaces test machinery rather than
adding to the rule count; the rule freeze in item 1 is noted.

Proposed paths:
- `scripts/prose_diff.py`
- `templates/modules/team-gated/prose_diff.py`
- `scripts/prose_roots.txt`
- `templates/modules/team-gated/prose_roots.txt`
- `scripts/exact_replace.py`
- `templates/modules/team-gated/exact_replace.py`

**Outcome 2: a shipped tool, `scripts/prose_diff.py`.** It is standard-library
only and advisory: it reports and never blocks.
- **Input:** two revisions. The default base is the merge base with the
  default branch, not `HEAD~1`. That way an earlier commit on the branch
  cannot have already dropped a root from the list. Both lists are read from
  the base revision. Changes to either list, or to the tool itself, are
  reported before anything else (Security Review S5).
- **Git access:** through the hardened `tools/git_read.py` helper only, the
  way the content scanner already does. Specifically (Security Review S4):
  - revision arguments starting with `-` are refused;
  - revisions resolve with `rev-parse --verify --end-of-options`;
  - no textconv;
  - size caps on each file and on the whole read.
- **Reported as "not compared," never as no change:**
  - files that fail to parse or decode;
  - submodules;
  - symbolic links;
  - listed files with other suffixes, such as `.yml`.
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
- **Gaps it names:**
  - text built at runtime, or joined with `+`;
  - the number of Python string constants under six words it skipped, so a
    short rule such as "Never push." is not dropped silently.
- **Output:**
  - sentences removed;
  - sentences changed, shown as before and after;
  - sentences added;
  - a one-line "reflow only" when nothing but wrapping changed.
- **How it gets used:** reviewers read the output to answer the question. The
  PR-merge check may cite it. If it does, it runs the merger's own trusted
  copy of the tool, never the branch's copy, as that check's S1 requires.
- **Install:** `templates/modules/team-gated/prose_diff.py` is installed
  verbatim as `scripts/prose_diff.py` by the default-on `content-security`
  module, so every adopter gets it.
- **Scanner unchanged:** the scanner's list and runner are not edited.

**Outcome 3: retire Cairn's text pins.**
- Remove the pin tests in the files above.
- Keep every copy-parity test, moving it if its file empties.
- The protected drain-mode pin, if the Maintainer retires it, goes under the
  release re-anchor with the promise-testing proposal's removals
  (`dev/proposals/2026-11-08-claude-promise-unit-testing.md`).
- **Each pin gets a disposition,** retire or keep, with a one-line reason,
  recorded in the plan. The default is retire. The three classes in the
  Decision summary are kept only if the Maintainer chooses so.
- **Coverage first.** A pin retires only after the plan shows that every file
  it reads is covered by one of the two lists (Security Review S3). In Cairn
  that means adding the pinned `templates/` files to `prose_roots.txt`.
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

**Outcome 4: a shipped exact replacer, `scripts/exact_replace.py`.** The
Maintainer, in chat on 2026-11-08: "Yes I think we need an exact text
replaced to use". It is standard-library only, and it writes files.
- **Input** (second pass N3):
  - the target path;
  - the old and new text, each from a file or standard input, read as raw
    bytes, never from command-line arguments. Nothing is stripped or
    translated, so no trailing newline is added and no CRLF becomes LF;
  - or a JSON batch file of old/new pairs, applied in order, all or none.
- **"Exactly once"** means exactly one start position. Every position is
  counted, overlapping ones included, so `rule. rule. rule.` holds
  `rule. rule.` twice. Empty old text is refused. Line endings are matched as
  they are in the file's bytes.
- **It refuses, writing nothing:**
  - zero or several matches, reporting the count and line numbers;
  - a target that is a link, a reparse point, not a regular file, or has
    more than one hard link;
  - text that is not UTF-8;
  - **a target outside the root** (second pass N2). The root is the
    repository top level, from `tools/git_read.py`. The target's real path
    must lie under it, and every folder from the root down to the target is
    checked to be neither a link nor a junction;
  - any path inside the Git directory. A component that matches `.git` in
    any case, or a Windows short name such as `GIT~1`, is refused;
  - a component containing `:`, which on Windows names an alternate data
    stream.
- **It writes atomically:**
  - a temporary file in the same folder, flushed, then replaced over the
    target;
  - it changes no byte outside the match, and keeps the file mode;
  - just before the replace, it re-checks the target's hash and identity,
    and refuses if either changed;
  - on any refusal or failure it removes its temporary file, and the
    original is untouched.

  **The remaining window** (second pass N4): this narrows the race but does
  not close it. A write that lands after the final check, or through a handle
  already open on the file, can be lost, as `tools/_intent/record_io.py`
  already says of its own write. On Windows, a replace that fails because the
  file is open or read-only is a refusal.
- **Afterwards,** if the target is on either functional-prose list, it
  prints the report tool's sentence comparison for that edit, worked out in
  memory without git. If the edit touched either list itself, it says so
  first (second pass N1).
- **Exit codes** (second pass N5):
  - 0: applied;
  - 1: no match, or several;
  - 2: refused, nothing written;
  - 3: applied, but the report failed. A file it cannot parse is reported
    as "not compared".
- **Safe output** (second pass N6): both tools escape control characters,
  and show bidirectional and zero-width characters as visible escapes, so
  hidden text cannot slip past a reader.
- **Install:** from `templates/modules/team-gated/exact_replace.py`, with the
  same default-on `content-security` module, so every adopter gets it.
- **Vendor-neutral by construction.** It is a plain command any agent or
  person can run. The shipped rule says an agent tool that edits by exact
  match already meets the rule, and names no tool. The neutrality gate
  checks that wording.

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
- **No exact replacer, relying on agent tools.** Rejected at opening, then
  reversed. This session hand-wrote an exact replacer about six times
  because agent edit tools weren't enough. Shell edits went stale, and not
  every adopter's tool edits by exact match.

## Documentation / doctrine surface

- **Governing layer:** both `AGENTS.md` files.
- **Templates:** the shipped review sections.
- **Descriptive layer:** the tool's docstring and the `content-security`
  module.
- **Doctrine gate:** the Maintainer chose the basis in chat on 2026-11-08:

  > "I think we should go forward with this on the basis that it is a good
  > idea, not on recurrence"

  The change goes forward on its merits. The rate-limit gate
  (`docs/methodology/rationale.md` > "How the doctrine evolves under
  evidence") limits rule changes made *from an incident*. This proposal
  comes from a design review, so no gate trigger is claimed. The Decision
  records that reading.

## Evidence / verification plan

### Tests required

- **The tool:** contract tests for each promise, through its command line:
  - removed, changed and added sentences;
  - reflow-only;
  - string constants in Python;
  - unreadable and absent revisions reported, never silently empty;
  - a revision starting with `-` refused;
  - git reached only through `tools/git_read.py`;
  - the merge-base default;
  - changes to either list, or to the tool, reported first;
  - each "not compared" case;
  - the count of skipped short constants.
- **For each retired pin:** apply its specific mutant (Outcome 3) in a
  separate copy and confirm the tool shows it with before and after text.
- **The content scanner:** its list and runner are untouched, and its
  existing tests still pass.
- **The replacer:** contract tests through its command line:
  - one match applied;
  - zero or several matches refused, with the file byte-identical
    afterwards;
  - a batch applied all or none;
  - overlapping matches counted;
  - empty old text refused;
  - standard-input bytes read unchanged;
  - a link, reparse point or out-of-root target refused;
  - a link in a parent folder refused;
  - a hard-linked target refused;
  - `.git` in any case, `GIT~1` and `:` components refused;
  - non-UTF-8 text refused;
  - bytes outside the match, and the mode, preserved;
  - a change before replace detected, and the temporary file removed;
  - exit code 3 when the report fails;
  - a notice when a list is edited;
  - escaped control, bidirectional and zero-width characters, in both tools.

  **Windows** (second pass N7): the plan runs these tests on the
  Maintainer's Windows VM over SSH, as agent work, the way the modflow_tools
  Windows calibration plan did. Windows behavior is claimed only once
  measured there. If the VM is unavailable, Windows stays unclaimed and
  `bootstrap/SAFETY.md` is not changed. No human operation is added.
- **Copy parity:** the parity tests still pass.
- **Install:** the install test shows both tools and `prose_roots.txt`
  install with the module.
- **Boundary B:** `wide`.

### Examples / smoke checks

- `python scripts/check_cairn.py`;
- `python bootstrap/scaffold.py --dry-run` showing the new install line.

#### Security preflight — five questions, answered in writing

- **S1 — Who supplied it?**
  - **The report tool:** two revisions, defaulting to the merge base, and
    both lists from the base. A branch that edits a list cannot hide a file,
    and list or tool edits are reported first. Under the PR-merge check, the
    merger's trusted copy runs.
  - **The replacer:** the caller supplies the target and both texts. It
    decides only "exactly one match", which is checked against the file as
    read.
- **S2 — Can it fail?** Delete a sentence, and the tool must list it. That
  mutation is run for each retired pin.
- **S3 — What fires it, over what?** A reviewer runs it; it covers the
  listed files between two revisions. The shipped sentence describing it is
  checked against that.
- **S4 — Which way does it break?**
  - **The report tool:** a file it cannot parse is "not compared", never no
    change.
  - **The replacer:** any refusal or failure leaves the original file
    untouched; the replace is the last step.
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

**Scope delta**: degraded

- **Retiring the drain-mode pin** (`test_session_start_drain_rules.py`) is
  removed from Outcome 3. **disposition**: accept. Maintainer, chat,
  2026-11-08: "I accept your drain mode pin argument."

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

## Response -- Claude Opus 5.5 (author, Security Review) -- 2026-11-08

**Elapsed**: about 20 minutes. **Tokens**: unknown.

- **S1, accepted (blocking).** `test_default_security_stance.py` leaves
  Outcome 3 and the count, which is now 159.
- **S2, accepted as recommended.** The scanner's list is read only and is
  unchanged. Code files and other folders go in a separate `prose_roots.txt`,
  parsed with the runner's `load_audit_roots` rules.
- **S3, accepted.** A pin retires only after every file it reads is covered.
  In Cairn that means adding the pinned `templates/` files to
  `prose_roots.txt`.
- **S4, accepted.** Outcome 2 names:
  - `tools/git_read.py` as the only route to git;
  - the `-` refusal, `rev-parse --verify --end-of-options` and no textconv;
  - size caps and the "not compared" cases;
  - a count of skipped short constants.
- **S5, accepted.** The default base is the merge base. Changes to either
  list, or to the tool, are reported first. Under the PR-merge check the
  merger's trusted copy runs.
- **S6, accepted.** A trivial-lane edit to functional prose puts the report
  in its commit body. A removed or changed rule sentence makes it
  non-trivial.
- **S7, accepted.** The Maintainer choice now names the drain-mode pin and
  why it matters, with its 3-commit churn. The author recommends keeping it.
  The baseline remains full retirement until the Maintainer narrows it.

**New material, by the Maintainer's direction:** Outcome 4, the exact
replacer, which writes files. Its preflight answers and tests are added.
Because it is new security-relevant material, Status returns to
`awaiting-review` for a second Security Review pass, the last under the cap.
That pass covers the replacer and the closure of S1-S7. No second usual pass
is planned, since the new tool's risks are security-shaped.

### Withdrawn / superseded commitments

- **Sharing `content_scan_roots.txt` for code roots** is replaced by a
  separate `prose_roots.txt` (S2).
- **The `HEAD~1..HEAD` default** is replaced by the merge base (S5).
- **The rejected "exact-edit script" alternative** is reversed: it is now
  Outcome 4.
- **`test_default_security_stance.py`** is removed from scope (S1).

## Review -- Claude Opus 5.5 (Security Review, second pass) -- 2026-11-08

```
Reviewed commit: bd4c5188f8a543b3126ab1ba576ab9d6481c1b73
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: about 30 minutes
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes. S1 and S3-S7 are closed by the revised text. S2 is closed in intent but not as written (N1). The replacer is worth shipping, but its safety promises are underspecified (N2-N5) -- Outcome 2 "Input" and Outcome 4 "It refuses".
2. **Best alternative.** Keep Outcome 4, but take its write path from `tools/prune_intents.py::_atomic_rewrite` (`O_EXCL|O_NOFOLLOW` temp with a random name, unlink in `finally`, recheck before replace). Accept only a repo-relative target, checked component by component from the repo root, as `tools/_intent/shared.py::_has_link_or_reparse` does.
3. **What would show it wrong.** On macOS, `exact_replace.py .GIT/hooks/pre-commit` succeeds. I expect that unless N2 is closed: `Path('.GIT/HEAD').resolve()` returned an existing file here.

**Findings** (none blocking; all are design to settle before the plan)

- **N1: `load_audit_roots` cannot parse this list as specified.** It raises an error on a comment-only file ("declares no roots") and accepts only the `# content-scan-roots v1` sentinel. It also reads a disk path and checks containment against the working tree, but both lists must come from the base revision (`scripts/content_scan_runner.py` 205-275). Close: give the list its own sentinel, allow it to be empty, parse the text from git with the same lexical rules, define `!`, and have the replacer print a notice when its edit touches either list.
- **N2: containment.** The design does not say which root, and does not cover links in parent folders, Windows junctions, `.git` written in any case or as a short name (`GIT~1`), or `:` streams. Close: anchor the root at the script's own location; walk each component with `lstat`; refuse `.git` components by casefold on the resolved path; refuse `:`. Test each case.
- **N3: what "exactly one match" means.** `str.count` misses overlapping matches: `'rule. rule. rule.'.count('rule. rule.')` is 1, but there are 2 start positions (probe). Empty old text, the trailing newline from stdin, and Windows text-mode stdin turning CRLF into LF are not defined. Close: read bytes, decode without newline translation or Unicode normalization, count every start position, refuse empty old text, count each batch pair against the running result, and use a JSON batch file.
- **N4: the change check narrows the race but does not close it.** A write between the recheck and `os.replace` is still lost, as is a write through a handle already open on the old file (`record_io.py` 576-586 states this). On Windows, replace fails when the file is open or read-only. Hard links get split. Close: state that residual, refuse with exit 2 and remove the temp file, and refuse or report `st_nlink>1`.
- **N5: exit code after the write.** If the report fails after the write, exit 2 would claim "writing nothing". Close: use a separate code, and treat parse failures (`RecursionError` included) as "not compared".
- **N6: printed text.** Both tools print repository text to a terminal. Close: escape control characters, and make bidirectional and zero-width characters visible, so that hidden rule text shows.
- **N7: Windows.** The repo has no CI, and `bootstrap/SAFETY.md` 289 does not claim reparse handling until it has been measured. Close: name who runs the Windows check, and count it as a human operation, or leave Windows unclaimed.
- **N8 (cheap):** Outcome 1 has two "Editing." bullets. Delete the second.

Vendor neutrality holds: it is a plain CLI, and the gate scans `templates/**.py` against its list of vendor names (`quality_gate.py` 468-476).

**Coverage**: Covered the S1-S7 text, the parser, the atomic-write precedents, the neutrality roots and CI presence. Not covered: the install manifest, `git_read.py` caps, and `prose_diff` `ast` edge cases. Over target (about 560 words): eight security-shaped findings each needed evidence.

## Response -- Claude Opus 5.5 (author, second Security Review) -- 2026-11-08

**Elapsed**: about 20 minutes. **Tokens**: unknown.

- **N1, accepted.** `prose_roots.txt` has:
  - its own header line;
  - a valid empty state;
  - text read from the base revision through git, with the scanner's path
    rules;
  - `!` reported as invalid.

  The replacer says when an edit touches either list.
- **N2, accepted.** The root is the repository top level from `git_read.py`.
  The checks cover the real path, every parent folder for links and
  junctions, `.git` in any case and short names, `:` components, and no
  writes inside the Git directory.
- **N3, accepted.** Raw bytes. Every start position counts, overlaps
  included. Empty old text is refused. Standard input is unchanged. Batches
  are JSON.
- **N4, accepted.** The proposal states the remaining window, removes the
  temporary file on any refusal or failure, refuses hard-linked targets, and
  treats a Windows replace failure as a refusal.
- **N5, accepted.** Exit code 3 means applied but the report failed.
- **N6, accepted.** Both tools escape control, bidirectional and zero-width
  characters.
- **N7, accepted.** The Windows tests run on the Maintainer's VM as agent
  work. Windows is unclaimed unless measured, and `SAFETY.md` is unchanged
  otherwise. No human operation is added.
- **N8, fixed.** The duplicate "Editing." bullet is deleted.

**The Maintainer's directions, 2026-11-08:**
- **Drain-mode pin kept:** recorded as a Scope delta with the quote.
- **Merit basis:** the doctrine-gate paragraph now quotes the Maintainer and
  claims no gate trigger.

The Security Review cap is reached. No blocker remains, so Status is
`awaiting-decision`.

### Withdrawn / superseded commitments

- **"Parsed with the runner's `load_audit_roots` rules"** is replaced by
  rules for the list's own header, read from the base revision (N1).
- **"It runs on macOS and Windows"** is replaced by "Windows claimed only once
  measured" (N7).
- **The gate paragraph** "not yet met; the Maintainer may classify" is
  replaced by the merit basis, per the Maintainer.

## Decision -- Maintainer -- 2026-11-08

Scribed by Claude Opus 5.5 (`claude-opus-5-5`) on the Maintainer's explicit
instruction in chat, 2026-11-08.

**Elapsed**: under 1 minute to scribe. **Tokens**: unknown.

**Tier**: heavy

**ACCEPTED.** The Maintainer's authorization, verbatim:

> "Accept both. Heavy tier. Add to v0.7. I will have the agent working on that in Codex take it from here."

The same chat recorded the merit basis ("I think we should go forward with
this on the basis that it is a good idea, not on recurrence"), quoted in
Documentation / doctrine surface.
