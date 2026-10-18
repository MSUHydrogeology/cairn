# The board as the basis for richer views: a stable JSON output, and a guide to building on it

**Author**: Claude (Strategy)
**Status**: accepted
**Review**: required(Internal) — the Maintainer asked for this change, so "should it exist" is settled, and no high-risk surface is touched
**Plan review**: required(Internal) — one adopter-run tool, one guide and one test file; no security surface (see the preflight)
**Opened**: 2026-10-18
**In brief**: `python tools/board.py --json` prints every proposal and plan as data, with who holds its status and a one-sentence summary when the author wrote one; a guide shows how to turn that into a web page or table that is regenerated, never hand-kept; Cairn ships no view.

## What changes for you

You have used a shared web page with live status for two days. It is far more
usable than `python tools/board.py`, and it went stale several times in a day
because it is synced by hand. This keeps its usefulness and removes the hand-sync.

1. **`python tools/board.py --json`** prints the board as structured data: per
   proposal and plan, its status, who holds that status, a one-sentence summary if
   the author wrote one, and anything declared as waiting on you.
2. **A guide, `docs/build-a-board-view.md`,** names every field, states what Cairn
   promises will not change, and walks through a 40-line script (standard library
   only) that builds a web page grouped by who acts next, with counts. It says how
   to keep a page from going stale (regenerate it, never edit it), and that you can
   hand the guide to an AI agent for a richer page.
3. **Cairn ships no view.** The example script lives inside the guide.

Unchanged: the terminal board prints what it prints today, stays read-only, derives
everything from committed files, and judges nothing.

Proposed paths:
* `docs/build-a-board-view.md` — the guide
* `bootstrap/tests/test_board_json_contract.py` — the contract's tests

## Questions for the Maintainer

1. **Should the proposal and plan templates ask authors for the `**In brief**:`
   line?** *Recommended: not in this change.* The board reads it if present and a
   view falls back to the title. Two open plans and an accepted proposal are
   already editing the plan templates; adding a line later is one line, once you
   have seen how often it gets written.
2. **Should the guide be copied into every adopter's tree?** *Recommended: no.* It
   lives in Cairn's `docs/` with the other how-to pages, and `board.py --help`
   names it. A new installed file changes the install contract, Cairn's most
   guarded surface. Revisit if adopters cannot find it.
3. **Should the board read every roadmap row, or only rows that declare a wait?**
   *Recommended: only rows that declare a wait.* Every row means a status marker
   on about 26 rows of `dev/PLANNING.md`, a file edited only at set times.
4. **Should the terminal board also show the "who holds it" column?**
   *Recommended: no.* The data carries it, and the two sentences that describe the
   terminal board stay true (see "Why this is not a judgment").

## Context

**Terms.** A *header line* is a bold `**Field**: value` line above the first `##`
heading; the board reads these and nothing else. A *holder* is whoever
`doctrine/lifecycle.md` says acts next on a status ("Each status names who holds
it next"). A *view* is any page, table or panel built from the board.

**Today.** `tools/board.py` is 128 lines. It prints five header fields per artifact
(`tools/board.py:33`), cuts cells at 48 characters and escapes `|` as `\x7c`
(`tools/board.py:42-62`). It has no holder, summary or machine form, so a view would
scrape a display format Cairn changes freely. The maintainer-attention plan
(`dev/plans/maintainer-attention.md`) is about to change it again: its C1 adds
`--maintainer` and a header field, `**Waiting on Maintainer**:`.

**The same failure, twice.** `dev/PLANNING.md` > "Active" once held a hand-kept
table. On 2026-08-27 it was emptied: all four entries were archived or delivered
work, and the block carried 204 lines describing them as in flight. The page you
reported this week went stale the same way. Both were a second copy of what the
artifacts already say.

**A precedent.** `python tools/intent.py list --format json` publishes a versioned
contract, `cairn-intent-list/1` (`tools/_intent/cli.py:107-113`): the schema string
is the fence, and a consumer reads that exact value or refuses. Intent records carry
an optional `stem` naming a proposal or plan.

## Proposal

### The output

`python tools/board.py --json` prints one JSON document; `--archive` adds archived
artifacts as today. `--json` with `--maintainer` is a usage error, since the
document already carries the Maintainer list.

| Top-level key | Holds | Why a view needs it |
|---|---|---|
| `schema` | `"cairn-board/1"` | the fence; present even when empty |
| `includes_archive` | true or false | so "no archived rows" is not read as "none exist" |
| `artifacts` | list of records | the board |
| `maintainer_waits` | list | what waits on you; the list `--maintainer` prints |
| `fences_without_wait` | list of ids | plans that mention a fence but declare no wait (the sibling plan's advisory), so a view does not reopen the miss that plan closes |

| Record key (`artifacts`) | Holds | Source | Why |
|---|---|---|---|
| `kind` | `"proposal"` or `"plan"` | the directory | grouping |
| `id` | text | file name without `.md` | the name artifacts are cited by; the join key |
| `path` | text | repo-relative, `/` separators | a link target |
| `archived` | true or false | under `archive/` | done versus in flight |
| `title` | text or null | first `# ` line above the first `##` | label when there is no summary |
| `in_brief` | text or null | `**In brief**:` header line | the one plain sentence; **optional** |
| `status` | text or null | `**Status**:`, as written | the raw fact |
| `status_holder` | `"maintainer"`, `"author"`, `"reviewer"`, `"implementer"` or null | lookup below | who acts next |
| `review`, `plan_review`, `opened`, `source_proposal` | text or null | lines the terminal board prints | unchanged facts |
| `waiting_on_maintainer` | text or null | the sibling plan's header line | a plan can wait on you while its status reads `implementing` |

A `maintainer_waits` record has `source` (`"artifact"` or `"roadmap"`), `id` (or
null), `line` (the `dev/PLANNING.md` line, or null), `reason`
(`"awaiting-decision"` or `"declared"`) and `text`. One function feeds `--maintainer`
as text and this list as data, so they cannot disagree. How an artifact that is
both at `awaiting-decision` and declaring a wait is listed, and whether `--archive`
changes either list (both should cover live artifacts only, as the sibling's plan
review asks of `--maintainer`), follow what the sibling's C1 lands; the plan reads
that code and pins it.

**The holder lookup** copies `doctrine/lifecycle.md`. It keys on the first word of
the status, matched exactly (real headers read `archived — C1-C9 all landed…`):

| Status | `status_holder` |
|---|---|
| `awaiting-decision` | `maintainer` |
| `revising`, `revising-plan` | `author` |
| `awaiting-review`, `awaiting-plan-review`, `awaiting-code-review` | `reviewer` |
| `ready-to-implement`, `implementing`, `revising-code` | `implementer` |
| `accepted`, `rejected`, `superseded`, `archived` | null: terminal |
| `ready-to-archive` | null: the doctrine says "whoever closes the loop" and names no role |
| anything else, including retired `proposed`, `reviewed`, `revised` | null |

**Why this is not a judgment.** Two sentences say the board does not answer this:
"The board judges nothing: who holds a row, what blocks it, and whether a review
cleared are read from the artifact itself" (`doctrine/session-routines.md:54-56`;
`templates/skills/session-start/SKILL.md:43-45`, the fix for issue #23).
`status_holder` is not who holds the *row*. It is who the lifecycle names for the
*status word*, and the sibling plan found the two differ for plans at a fence or a
deferral batch. So the board prints two facts and merges neither: the status's
holder, and the author's declared wait. Both sentences describe the terminal board,
which does not change (Question 4). **This is the first thing I ask the reviewer to
attack.** If the sentences cannot survive a `status_holder`, the fix is one clause
in each file, which makes this a doctrine change; the rate-limit gate would then be
met by the recurrence above.

### The promise (what "stable" means)

1. Within `cairn-board/1` the producer **only adds**: new keys on any object, new
   top-level keys, new values of `status_holder`, `source` and `reason`. It never
   removes or renames a key, changes a key's type, or changes what a key means.
2. Anything else is `cairn-board/2`, announced in `CHANGELOG.md`. The board emits
   one version, so a consumer built for `/1` meets `/2` as a refusal at the
   `schema` check, not a quiet misreading.
3. **Consumers** read `schema`, accept the version they were built for, refuse
   others, **ignore keys they do not know**, and treat an unknown enumerated value
   as "other".
4. Absent is `null`: never `""`, never inferred. A string is what the author wrote,
   whitespace-trimmed, and is **not escaped for any output**. It is untrusted text
   any contributor can edit; escaping for a page is the page-builder's job.
5. Same files in, same bytes out: no timestamp, commit id or machine path; keys
   sorted; ASCII-only JSON (as `cairn-intent-list/1`). Row order is **not**
   promised; sort it yourself.
6. On any failure nothing goes to standard output and the exit is nonzero, never a
   partial document. A script that regenerates a page must not overwrite it then.
7. **Not promised:** the terminal layout, that an optional field is present, or that
   `status_holder` is an instruction. It is a lookup.

### What each candidate became

| # | Candidate | Verdict | Reason |
|---|---|---|---|
| 1 | who acts next | **Keep**, as `status_holder` | one fixed table from the doctrine; named so it is not read as "who should act" |
| 2 | one plain sentence | **Keep, optional** | the board prints `in_brief` and `title` separately and never substitutes: a fallback in the board would read as authored text. The view writes `in_brief or title`. Header line only: the `## In brief` sections some proposals carry sit below the first `##`, and reading section bodies would widen what the board parses |
| 3 | `--json` | **Keep**: the deliverable | the contract above |
| 4 | grouping, summary line | **Drop** from the board | presentation belongs in the view; the guide shows both in six lines. Changing the terminal default would break the byte-for-byte check the sibling sets |
| 5 | roadmap rows | **Reshape**: only rows declaring a wait, inside `maintainer_waits` | `dev/PLANNING.md` has about 30 top-level bold rows; about 4 carry the status marker its "Status taxonomy" asks for (counted 2026-10-18 by a one-off script). Reading all means retrofitting ~26 rows, then holding authors to a convention most have not followed. Revival: you ask for roadmap items on a view, once the wait marker has had use |
| 6 | recently finished | **Drop**; recipe in the guide | the board runs no git. `--json --archive` lists what is finished; *when* is in git, which a view's script may run: `git log --diff-filter=A --name-status -- dev/plans/archive`, run on this tree before the guide cites it |
| 7 | active work intents | **Drop**; recipe in the guide | the intent log is gitignored and local to one working tree, so one commit would print different boards on different machines; it belongs to a team-gated module and the board is default-on; a dead session's claim reads "agent working" forever, the staleness being removed. The guide joins `intent.py list --format json` to the board on `stem`, as a hint, since `stem` is optional. Issue #23 asked for this column |

### The guide

`docs/build-a-board-view.md`, descriptive layer: it describes the tool and how to
extend it, and prescribes nothing cross-cutting. It holds the fields and the
promise above, and:

* a worked example (about 40 lines of standard-library Python) that runs
  `board.py --json` and writes a static HTML page grouped by holder with counts,
  escaping every value;
* **keeping a view honest:** regenerate from the board; treat the output as
  disposable; fix a wrong row in the artifact's header, then regenerate; stamp the
  page with the commit the script read (the script may run git; the board does not);
  never overwrite the page on failure;
* **what Cairn's data supports:** "needs you", "in flight by holder", "queued"
  (`accepted`, `ready-to-implement`) and "done" are derivable. **"Blocked" and "an
  agent is working right now" are not**; the guide says so and gives the two recipes;
* a short note that an AI agent can be handed the guide and asked for a richer page
  from the same output, regenerated rather than hand-edited. No vendor named.

**Why the example lives in the guide, not in `tools/`.** A script in the install set
is a view generator in the core, which you ruled out, and executable code every
adopter would carry through the lockfile, upgrades and the security lint. In the
guide it costs adopters nothing, and a test runs it so it cannot rot.

### Where it lands

* `tools/board.py` and its byte-identical twin `templates/skills/_lib/board.py`
  gain `--json`, the lookup, the title and `**In brief**:` reads, and a rule that a
  symlinked artifact is skipped (today the board follows symlinks; with free text
  now leaving the tool for other programs, a file outside `dev/` should not be able
  to supply it). The docstring gains the sentence that `status_holder` is the one
  derived value.
* The lockfile record for `tools/board.py` is reconciled by a scoped finalize of
  that one path, as the sibling plan does (precedent `2ea3f869`).
* `docs/build-a-board-view.md` is new; `docs/tool-usage.md` > "tools/board.py" gains
  `--json` and a link, after the sibling's revision edits the same entry.
* **Sequencing.** The plan's first implementation chunk starts only from a tree
  holding maintainer-attention's C1 commit: both change `board.py`, the twin and the
  lockfile record, and `maintainer_waits` is defined by that code. The plan may open
  earlier.
* **Frozen files: none.** `frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json`
  (183 entries) names none of the files above; checked against a known key
  (`bootstrap/tests/test_replacement_tools.py` is present). The sibling edits that
  file; this proposal does not, which is why its tests live in a new file. The pinned
  collection gains that file's nodes, which join the queued re-anchor row as the
  sibling's five do.
* **AST impact: none** (`bootstrap/_scaffold/` is untouched; `board.py` is not in it).
  **Install contract: unchanged** (same destination, source and mode, so
  `scaffold.py --manifest` is the same; the plan diffs it before and after).

## Rationale

Cairn already holds every fact the web page shows. What is missing is a way out of
the tool that does not mean scraping a display format. A data output removes the
second copy, and the second copy was the only cause of the staleness.

A contract, not a dump: people building on an output need to know what will not
break under them. "Only add" costs the producer almost nothing and gives every
consumer a safe default (ignore what you do not know). The one-way door is removal,
so v1 carries only what has a clear source and reason; roadmap rows, intents and
recents can arrive later with no version bump. Cost: roughly 80 to 100 lines in
`board.py` on top of the sibling's (an estimate, not a measurement), one guide, one
contract. A test pins the guide's field tables to the output, so keeping the guide
true does not rest on memory.

**Review tier.** `required(Internal)`: the template reserves External for a change
whose structure is in question, and no high-risk surface in `AGENTS.md` is touched.
`doctrine/dual-review.md` keeps an External floor on deliberate-lane proposals, which
you have waived before (`dev/PLANNING.md` > Queued, F8: "External floor waived"). I
have declared below it, for your Decision to ratify or override.

## Alternatives considered

* **Ship a view** (an `--html` flag or a separate view script). The strongest
  rejected alternative: it is one command from the page you use. Rejected, per your
  direction and for a reason of its own: a shipped view is one rendering for every
  team, and the first team that disagrees edits the output by hand, which brings the
  drift back. Cost of losing it: an adopter runs 40 lines they did not write.
* **Let views scrape the terminal output.** Rejected: cells are cut at 48 characters,
  `|` is escaped, and the layout is about to change for the sibling plan.
* **A JSON Schema file beside the guide, or roadmap rows, intents and recents in v1.**
  Rejected: a second statement of the contract can disagree with the first, and a
  larger contract before any consumer asks is a larger promise; fields can be added
  later without a version bump.
* **Do nothing.** The page keeps going stale and the next copy repeats August.

## Documentation / doctrine surface

| Layer | File | Change |
|---|---|---|
| Descriptive | `docs/build-a-board-view.md` (new) | the guide; routed to `docs/` because it describes current behavior and how to extend it (`docs/DOCUMENTATION_PLAN.md`) |
| Descriptive | `docs/tool-usage.md` | the board entry gains `--json` and a link |
| Governing, deliberation | none | no `doctrine/` or `AGENTS.md` change |

No doctrine changes, so the rate-limit gate in `doctrine/rationale.md` is not
engaged, unless review forces the two-sentence edit above. The guide names no AI
vendor or product (`docs/` is scanned by the neutrality gate); the page you use is
described there as a shared web page with live status.

## Evidence / verification plan

It worked if a view built only from the guide and `--json` regenerates from a clean
checkout with no hand edit, and its "needs you" group matches `board.py
--maintainer`. It failed if anyone must edit the generated file, or read the
terminal output, to get a correct page.

### Tests required

All in the new `bootstrap/tests/test_board_json_contract.py`, each seen failing
before the code exists:

* **Keys are exactly the documented keys:** the test reads the guide's tables and
  compares them with the emitted keys both ways.
* **The holder lookup matches the lifecycle:** every status word in
  `doctrine/lifecycle.md`'s two diagrams is in the table with the holder its node
  label gives; first-word matching on `archived — C1-C9…`; an unknown or retired
  status gives a null holder and a kept raw status.
* **Absent is null,** missing field and empty field alike; `title` and `in_brief`
  never stand in for each other. **Same files, same bytes;** ASCII, sorted keys,
  schema present on an empty tree.
* **`maintainer_waits` agrees with `--maintainer`;** the terminal board is
  byte-identical to the sibling plan's output on one tree.
* **A symlinked artifact is skipped;** an unreadable file gives no standard output
  and a nonzero exit.
* **The guide's example runs:** the test extracts the tagged Python block, runs it on
  a scratch tree whose title holds `<script>`, and asserts the escaped form and the
  grouped counts.

Boundary A adds `test_replacement_tools.py`, `test_security_lint.py`,
`test_skills_upgrade.py`, `test_skills_self_heal.py` and `test_verify_integrity.py`.
Boundary B is expected **full** (a tool adopters run changes, a lockfile record is
touched, uncertainty resolves to full); the plan fixes it.

### Examples / smoke checks

* `python tools/board.py --json | python -m json.tool` on the live tree.
* The guide's script on the live tree, then the page opened and read by a person; a
  person is the only check that it is useful.
* `python tools/intent.py list --format json` joined on `stem`, with a claim and without.
* `check_cairn.py`; `claim_check.py` on the guide; `quality_gate.py --sub neutrality`.

#### Security preflight — five questions, answered in writing

No network, subprocess or untrusted-input deserialization is added. The change adds
an output other programs read, and one file-handling rule.

* **S1 — Who supplied it?** Every value comes from artifact files any contributor can
  edit, so an artifact supplies its own `status` and therefore its own `status_holder`.
  The board authenticates nothing; the guide says a view is a reading aid, never an
  approval record. A symlink could let a file outside `dev/` supply a title; the
  symlink rule closes that.
* **S2 — Can it fail?** The lookup test fails if one entry changes (mutation:
  `awaiting-decision` to `author`); the key test on an undocumented key; the example
  test if `html.escape` is removed. Named now, run with results in the plan's record.
  The lookup test checks the table against the lifecycle document, not the code.
* **S3 — What fires it, over what?** `python -m pytest
  bootstrap/tests/test_board_json_contract.py` and the Boundary B full run, both
  started by a person (Cairn has no CI). The key test ties the guide's promise to the
  output.
* **S4 — Which way does it break?** An unknown status gives a null holder (nobody
  named: less authority). A failure gives no output, not a partial board. An unknown
  `schema` makes the consumer refuse. The hazard is human: reading null as "nothing to
  do"; the guide says null means the doctrine names no holder.
* **S5 — Who still wins?** A contributor who can edit a header can still put
  misleading, well-formed text on the board: claim `archived`, drop a
  `**Waiting on Maintainer**:` line, or put markup or direction-override characters in
  a title for a page-builder that forgets to escape. The escaping class is closed
  **by enumeration**, not construction: the board leaves strings raw (the terminal
  encoder would turn `A | B` into `A \x7c B`, wrong for data), so the duty falls on
  the page-builder, in the guide and the tested example.

## Signals the change is wrong

* A consumer needs a field we left out, and adding it means renaming or retyping one:
  the contract was fixed before its use was known.
* Authors rarely write `**In brief**:`, so pages show long titles and are no better than
  the terminal board. That argues for Question 1 becoming a yes.
* The page you use is still hand-edited beside the generated one: the guide failed.
* A view's "needs you" group disagrees with `--maintainer`.
* Requests for an `--html` flag mean the guide is not easy enough; by itself that is not
  a reason to ship a view.

## Scope delta

**Scope delta**: preserved. This is the opening text. The seven candidates are evaluated
in one table, each kept, reshaped or dropped with a reason; nothing was removed from an
earlier baseline.

## Assurance path

**Assurance path**: high-assurance

Mandatory under the template's own rule: `tools/board.py` is executed by every adopter,
and its output becomes a published contract. No other trigger applies: no `doctrine/`
change, no install-contract change, no engine change.

## Review -- Claude Sonnet 5.5 (External, fresh session) -- 2026-10-18

```
Reviewed commit: 5bcfa9e1dcba3386328eb728ccedd9b506e3e7f7
Target: the complete proposal (header through Assurance path), checked against doctrine/lifecycle.md, doctrine/session-routines.md, templates/skills/session-start/SKILL.md, tools/board.py, dev/plans/maintainer-attention.md (read at 739e3aba) and the tree
Prior findings: none
Assurance path: high-assurance
```

**Tier**: External
**Findings**: raised (3 blocking, 7 non-blocking)
**Verdict**: REVISE

Distance: a fresh session of the author's agent type, not a different type. The
header declares `required(Internal)`; this pass is External by stance, so it
meets the External floor on deliberate-lane proposals (`doctrine/dual-review.md`
> "The External floor on deliberate-lane proposal review"). The Decision should
record the floor as met by this pass, not waived. Interpreter for every figure
below: Python 3.13.13, read-only tools only; no suite run.

### In plain terms

**Should it land? Yes, in a narrower form.** The terminal board cannot be
scraped safely, so a data output plus a guide is the right answer to what you
asked for, and shipping no view is right. Three parts of the draft are promised
too early or conflict with what the board says about itself; each has a small
fix. The rest is checking.

1. **`status_holder` makes the board answer "whose move is it?"**, which two
   doctrine passages say the board does not do, and a third says it does. Nobody
   has chosen between them. (F1)
2. **Three of the contract's keys are defined by code that is not written** and
   whose plan is still being revised. You would be ratifying a promise whose
   content is undecided. (F2)
3. **The promise "only adds" has no test that could catch its breaking.** The
   planned key test passes a rename. (F3)

**Strongest rejected alternative.** The draft names "ship a view", but you ruled
that out, so it was never live. The live one is: `cairn-board/1` carries only
plain facts that exist today (kind, id, path, archived, title, status and the
other header fields, optional `in_brief`), with **no derived value**; the
holder lookup ships in the guide as a tested recipe beside the other three
recipes, and the wait keys arrive additively once the sibling plan's code
exists. The draft's own rule favours it: "the one-way door is removal" and
fields "can be added later without a version bump". Its cost is real: every view
carries an eight-line lookup, and a non-Python consumer (`jq`) must re-write it.
Its gain: it removes F1 and F2 together and leaves "the board judges nothing"
true without a doctrine edit. I would take it.

**What would falsify the central claim** ("a data output removes the second
copy, and the second copy was the only cause of the staleness", and the page
"keeps its usefulness"). Any of: (a) the generated page is older than `HEAD`
when you open it, because nothing regenerates it (F5); (b) the page is bland
because `in_brief` is empty on nearly every row (F4); (c) a `/1` consumer breaks
without a `/2` (F3). The draft's signals cover (c) and half of (b); (a) is
absent.

### The proposal at its strongest

The draft diagnoses the failure correctly and checkably. I verified it: the
`Active` block was emptied at `8f1399b9` with four archived entries and 204
stale lines, and `cairn-intent-list/1` exists with the properties described
(`tools/_intent/cli.py:112`, `ensure_ascii`, sorted records). Choosing a
versioned, additive, refuse-on-unknown-version contract over scraping is the
right shape. Declining a shipped view for a view that costs adopters nothing and
is regenerated is the right call. Keeping the example out of the install set is
right: it keeps the install contract untouched.

### What I checked and found true

* **Frozen files: none.** `bootstrap/tests/fixtures/gate_manifest.json` >
  `frozen_files` has 183 entries; none of `tools/board.py`,
  `templates/skills/_lib/board.py`, `docs/build-a-board-view.md`,
  `docs/tool-usage.md`, `bootstrap/tests/test_board_json_contract.py` is in it.
  The instrument works: `test_replacement_tools.py` and `test_security_lint.py`
  are present. Per `AGENTS.md`, a new test file does not redden the suite (the
  manifest test does not diff the committed fixture); I did not run it.
* **AST impact: none.** The only engine reference to the board is the install
  mapping at `bootstrap/_scaffold/config.py:584`, which the draft does not touch.
* **Install set unchanged.** `scaffold.py --manifest` lists `tools/board.py` from
  `skills/_lib/board.py` as verbatim, unconditional; the draft changes bytes, not
  that line. The twins are byte-identical today (`cmp`). `docs/` is not
  installed (only `docs/DOCUMENTATION_PLAN.md` is), which matters for F9.
* **The git recipe works today.** `git log --diff-filter=A --name-status --
  dev/plans/archive` yields 52 `A` rows for the 52 archived plans (the pathspec
  hides each rename's source, so it reads as an add).
* The intent log is gitignored (`.gitignore:12`) and `tools/_intent/` is
  team-gated in the manifest, as candidate 7 says. `id` is unique across all 130
  artifacts today.

### Findings

#### F1 -- blocking -- `status_holder` is a derived answer printed beside a fact

**Plain.** The board's one promise is that it shows what authors wrote and
decides nothing. A field saying who acts next is a decision, and the page you
want is grouped by it. The draft's distinction (the holder of the *status word*
versus the holder of the *row*) is real in the data, but it disappears the
moment a view groups on it.

**Precision.**

* **The draft attacks the wrong text and misses its best support.**
  `doctrine/lifecycle.md:144-146` already says "a reader -- or a board -- can
  tell from the status alone whose move it is", and the sibling plan's C2
  (`dev/plans/maintainer-attention.md:145`) rewrites that sentence to add the
  Waiting-line exception. So doctrine holds the lookup (lifecycle.md) and the
  prohibition (`session-routines.md:54-56`, `SKILL.md:43-45`), and they
  disagree about the same tool. The draft inherits that conflict and must say
  which text yields; it cites only one side.
* **"The two sentences describe the terminal board" does not hold.** They say
  "The board judges nothing". The module docstring (`tools/board.py:7-11`)
  disclaims "what should happen next" for the module, and
  `bootstrap/tests/test_replacement_tools.py:33-35` pins the reason: "a derived
  judgment printed beside a fact reads as a fact". In every record
  `status_holder` sits beside `status`. The accepted attention proposal called
  `awaiting-decision` to Maintainer "the board's one built-in mapping"; this
  makes nine statuses mapped to four holders.
* **The failure it invites has a Cairn precedent.**
  `dev/plans/archive/subtraction-sweep.md:10-19`: the plan's header read
  `awaiting-plan-review` for days after C1-C7 were built, and the board showed
  it. `status_holder` would have said `reviewer`, and a page grouped on it would
  file built work under "reviewer". Status is hand-set; a holder derived from it
  is exactly as stale.
* **The tested example inherits the problem.** It groups by holder. A plan at a
  fence (the sibling's case: status `implementing`, waiting on you) lands under
  "implementer" unless the example also applies `waiting_on_maintainer`, and the
  sibling's advisory exists because authors forget that line. The board
  "merges neither", so every view must perform the merge; the draft never says
  what the merge is.
* **The rate-limit gate is asserted, not met.** The recurrence cited (a hand-kept
  view goes stale) is the reason to publish data. It is not a recurrence of a
  failure the "judges nothing" sentences caused, and no tracker row records it
  (`dev/measurement/` holds none).

**Closes when:** either (A, recommended) `status_holder` leaves `cairn-board/1`
and the lookup moves into the guide's example, checked against
`doctrine/lifecycle.md` by the same test, with the precedence stated (a declared
wait overrides the status word); nothing in doctrine changes, and the field can
be added later at no version cost. Or (B) the Response keeps the field and makes
the doctrine edit now: both sentences, the docstring, the test-class docstring
and a pointer from `lifecycle.md:145`, with the gate's trigger recorded rather
than claimed.

#### F2 -- blocking -- three keys are specified by code that does not exist yet

**Plain.** `maintainer_waits`, `waiting_on_maintainer` and `fences_without_wait`
are defined as "whatever the sibling lands". A promise that can only add cannot
be walked back, and you decide on the proposal's text, not on the plan that
reads the code.

**Precision.** Lines 108-112 leave open whether an artifact that is both
`awaiting-decision` and declaring a wait is one record or two, and what
`--archive` does; the sibling plan is `revising-plan` with those very points
open (`[PR9]` pins `--archive`; `[PR4]` settles the row grammar). Separately,
`fences_without_wait` freezes a body-text token test (`MAINTAINER-GATED` /
`MAINTAINER-ONLY`) into a key the contract may never retype. The accepted
attention proposal says that kind of parse "fails the dangerous way"; an empty
list will read as "no fences". Improving the heuristic later changes what the
key means, which promise 1 forbids.

**Closes when:** the Response states, in the contract, (a) one record per
artifact or two, (b) live artifacts only or not under `--archive`, (c)
`fences_without_wait` as advisory with its membership explicitly unpromised, or
the three keys are held out of `/1` and added after the sibling's C1 is read.

#### F3 -- blocking -- nothing proposed can catch a breaking change within `/1`

**Plain.** The planned key test compares the guide with the output and demands
they match both ways. A rename or retype made in code and guide together passes.
So the one thing an adopter relies on, that what worked in `/1` keeps working,
has no test.

**Precision.** Tests required, first bullet (lines 285-286). Add a committed
`/1` baseline (key names and JSON types per object) tested with subset
semantics: every baseline key present, same type; new keys allowed once the
guide lists them. S2 then names its mutations: rename `status` to `state` in
code and guide, and change an absent field from `null` to `""`; both must turn
it red. Also state `id` uniqueness (true today, not promised) and that "same
bytes" holds for one producer version only. The precedent does not supply a
test: `git grep cairn-intent-list -- bootstrap/tests` returns nothing.

**Closes when:** the baseline test exists in the plan's acceptance criteria and
its two mutations are named in S2.

#### F4 -- non-blocking -- `in_brief` has no producer

**Plain.** The one-sentence summary is probably what makes your page "far more
usable". It will be empty. Of 130 artifacts under `dev/proposals` and
`dev/plans` (archives included), one carries an `**In brief**:` header line:
this proposal. Question 1 recommends not asking authors for it, so the page shows
titles.

**Precision.** The success test (regenerates with no hand edit; "needs you"
matches `--maintainer`) is met by a bare table and does not test what you asked
for. Not blocking, because the fallback is declared. **Closes when:** the
Response either takes Question 1 as a yes with a trial, or says plainly that the
page shows titles until authors write the line, adds a numeric signal (share of
live rows with `in_brief` after 30 days), and adds your reading the page as a
success criterion.

#### F5 -- non-blocking -- the guide says "regenerate" but not what regenerates

**Plain.** A generated page is still a snapshot. With nothing firing the script,
it is stale from the first commit after it was made, which is what happened to
the hand-kept one. "The second copy was the only cause of the staleness"
overstates.

**Precision.** `AGENTS.md` > "Name the trigger": a check whose only trigger is a
human remembering is described that way. The guide should name a trigger (the
adopter's own session-end step, or a post-commit hook) or say there is none, and
should have the page show its stamped commit. Add to Signals: stamped commit
older than `HEAD` when you open the page, more than once in the first fortnight.

#### F6 -- non-blocking -- the recipes that replace dropped features are untested

**Plain.** Candidates 6 and 7 become guide recipes. The commit message calls
them tested; Tests required covers one extracted Python block, and the git and
intent-join recipes are hand smoke checks.

**Precision.** The git recipe works (checked) but covers archived *plans*;
proposals archive at plan-open or at a Decision, a different event. The guide
offers nothing for roadmap rows beyond waits, which is the other half of what a
Maintainer page might show. **Closes when:** the recipes are tested (scratch git
repo; a fake intents file with and without `stem`) or labelled untested
sketches, and the Response says what the guide offers for the roadmap.

#### F7 -- non-blocking -- the board's description of itself becomes false in four places

**Plain.** Adding a sentence leaves the old sentence contradicting it. The
sibling plan's review found the same trap (`[PR10]`).

**Precision.** The draft's Terms say the board reads header lines "and nothing
else"; "Where it lands" adds the title (a `# ` line, not a header field). Header-
only statements live at `tools/board.py:7` (docstring), `:115-116` (help),
`:108-109` (footer) and `docs/tool-usage.md:117-120`. Also say which mode the
symlink rule applies to: in `_rows` it changes the terminal board on a tree with
symlinked artifacts, against "unchanged" and the byte-identical check.
**Closes when:** the Response lists the four places and states the rule's scope.

#### F8 -- non-blocking -- the neutrality check named in the plan is red today

**Plain.** Smoke checks list `quality_gate.py --sub neutrality` as if it could
read green. It reads `fail=74 info=21` (Python 3.13.13), with 14 of the fails under
`docs/` and 47 under `templates/`, where the board twin lives.

**Precision.** The plan must record "no new finding from the guide or either
board copy against the 74", or sequence after the accepted neutrality proposal's
Part 1 brings it to zero. The denylist includes Google, Microsoft, Meta and
Cursor, so a hosting recipe naming one fails. Both board copies are clean now.

#### F9 -- non-blocking -- adopters cannot find the guide, and an older board cannot run it

**Plain.** The goal is that adopters can build a view. They get `tools/board.py`
but not `docs/`, so a `--help` line naming `docs/build-a-board-view.md` points at
a path that does not exist in their tree. An adopter whose `board.py` predates
this change gets "unrecognized arguments" from `--json` (exit 2, nothing
printed).

**Precision.** Question 2's "no" is fine if `--help` names Cairn's published
location, and the guide states the minimum Cairn version and the upgrade step.

#### F10 -- non-blocking -- tier, preflight and figures

**Plain.** Small inconsistencies a reader will trip on.

**Precision.**

* The preflight is filled in (a path rule, a surviving hostile-text attacker) yet
  Plan review says "no security surface". Pick one. S2 names no mutation for the
  symlink rule, the one control the change adds, nor for "failure prints
  nothing".
* The guide teaches a subprocess call while the preflight says none is added.
  True of the tool, not of the example. The example should use `sys.executable`,
  not a `python` PATH lookup, near the interpreter-binding surface in
  `AGENTS.md`.
* "About 4" of about 30 roadmap rows carry the status marker: I count 7
  (`dev/PLANNING.md` lines 497, 651, 656, 661, 671, 676, 697), 8 with line 917.
  The conclusion survives; the figure does not, and the one-off script is not
  recorded.

### Maintainer questions

None new. Question 1 (`In brief` in the templates) interacts with F4: I would
answer it after you see how the page reads with titles only. Question 4 stays
"no" under either F1 route.

### Withdrawal ledger check

No earlier Response exists, so no withdrawal ledger is owed or checked.

## Response -- Claude (Strategy) -- 2026-10-18

This answers the External review at `fe0d093c` (reviewed commit `5bcfa9e1`).
Revision 1 follows with the complete current contract.

**In plain terms.** I accept the verdict and take the reviewer's alternative. The
board's data now carries only plain facts that an author wrote or that the file's
location gives. The "who holds it" lookup moves into the guide as a tested recipe,
so the board keeps saying nothing about whose move it is, and no doctrine changes.
The three keys that depended on unwritten code are dropped, except one that is just
another header line. The "only adds" promise now has a test that can catch a
break. The External floor on deliberate-lane proposals was **met** by `fe0d093c`,
not waived. My opening Rationale said I had declared below the floor and asked the
Decision to ratify or override; that sentence is withdrawn.

* **[F1]** accept, route A. I take the alternative and cannot beat it on the
  merits. Its cost is real: every view carries an eight-line lookup, and a
  `jq` consumer rewrites it. That is a smaller price than a doctrine conflict
  nobody has chosen, and the field can be added later at no version cost.
  Sub-points:
  * The opening cited one side of the doctrine's disagreement. Both sides now
    stand named: `doctrine/lifecycle.md:144-146` ("a reader -- or a board -- can
    tell from the status alone whose move it is", which the sibling plan's C2
    rewrites) and `doctrine/session-routines.md:54-56` with
    `templates/skills/session-start/SKILL.md:43-45` ("The board judges nothing:
    who holds a row"). That disagreement is older than this proposal. Route A
    leaves it where it is: the board takes neither side, and the guide's lookup
    cites `lifecycle.md` as its source.
  * "The two sentences describe the terminal board" is withdrawn. They say "the
    board".
  * The stale-status precedent (`dev/plans/archive/subtraction-sweep.md:10-19`)
    is accepted. The guide's example prints the raw status beside every group
    and stamps the page, so a stale status is visible as a stale status.
  * The example's grouping states its precedence rule, and a test pins it: **a
    declared wait overrides the status word.** That is why
    `waiting_on_maintainer` stays (see F2).
  * "The rate-limit gate would be met by the recurrence" is withdrawn. A hand-kept
    view going stale is a reason to publish data, not a failure the "judges
    nothing" sentences caused. With no doctrine edit, the gate is not engaged.
* **[F2]** accept. `maintainer_waits` and `fences_without_wait` leave `/1`.
  `fences_without_wait` froze a body-text token test into a key, and an empty list
  would read "no fences". Both can arrive later, additively, after the sibling's C1
  is landed and you have used `--maintainer`. `waiting_on_maintainer` stays, and I
  disagree that it is code-defined: it is one more header line, read like `review`
  by the same function, and its name and form are bound by the accepted attention
  proposal (Decision `e9043938`). The plan's first chunk reads the landed C1; if no
  header line of that name is read there, the key is dropped from `/1` through a
  recorded deviation, never renamed.
* **[F3]** accept. A committed `/1` baseline and a subset-semantics test; S2 names
  the two mutations. `id` uniqueness is stated as not promised, and "same bytes"
  as holding for one producer version.
* **[F4]** partly accept. I take the plain route: the page shows titles until
  authors write the line, there is a numeric signal, and your reading of the
  page is a success criterion. I decline making Question 1 a yes with a trial now:
  the plan templates are being edited by three other artifacts, and the reviewer
  and I agree you should see the titles-only page first.
* **[F5]** accept. The guide names its triggers (or says there is none), the page
  shows its stamped commit, and the overclaim "the only cause of the staleness" is
  withdrawn.
* **[F6]** accept. The git recipe and the intent join are tested; the roadmap
  statement is written down. The git recipe covers plans only, because a proposal
  archives at plan-open or at a Decision, which is a different event.
* **[F7]** accept. The four places and the Terms sentence are listed, and the
  symlink rule's scope is stated: it applies in both modes.
* **[F8]** accept. I re-ran the gate: `fail=74 info=21` at `8e5df0f0`, Python
  3.13.13. The smoke check compares against that and expects no new finding.
* **[F9]** accept. The guide is a citation in the form Cairn already uses for
  files adopters do not receive; `--help` carries it; the guide states how to
  tell an older board and how to upgrade it. Question 2 stays "no".
* **[F10]** accept all three. The plan review becomes `required(Internal +
  Internal Security Review)`; the example uses `sys.executable`; and the figure is
  7 of 30 rows, recounted, with the script recorded.

**Scope not widened.** Everything added is a closure the review specified: F3's
baseline, F5's trigger, F6's tests, F7's list, F8's baseline, F9's citation,
F10's obligation. Everything else narrows. The narrowing is a recorded Scope
delta that only your Decision can concede. The status therefore moves to
`awaiting-decision`.

## Revision 1 -- Claude -- 2026-10-18 -- the complete current contract

**Section inventory.** Every opening section carries forward, from In brief through
Assurance path. `status_holder`, `maintainer_waits` and `fences_without_wait` leave
the contract and are recorded under Scope delta. No other section is absent.

**Declarations.** **Review**: required(Internal); the External floor was met by
`fe0d093c`, not waived. **Plan review**: required(Internal + Internal Security
Review), changed from the opening's required(Internal) (F10); the header line is
left as opened, because earlier sections are append-only, and this declaration
binds. **Assurance path**: high-assurance.

Proposed paths:
* `bootstrap/tests/fixtures/board_json_v1_baseline.json` — the committed `/1` baseline
* `bootstrap/tests/test_board_json_contract.py::TestGuideLookupMatchesLifecycle` — the guard node for the lookup

### In brief

`python tools/board.py --json` prints every proposal and plan as plain data: what
its author wrote in the header block and its title, nothing derived. A guide,
`docs/build-a-board-view.md`, names every field, states what will not change, and
walks through a short script that builds a web page grouped by who acts next. The
"who acts next" lookup lives in the guide, tested against the lifecycle doctrine,
not in the board. Cairn ships no view.

### Questions for the Maintainer

1. **The "who acts next" lookup moves from the board to the guide. Is that
   acceptable?** *Recommended: yes.* It keeps the board's promise that it decides
   nothing and avoids a doctrine edit nobody has chosen. This is a recorded
   reduction in the Scope delta, and only you can allow it. If views drift on the
   lookup, the field can be added later with no version change.
2. **Should the proposal and plan templates ask authors for `**In brief**:`?**
   *Recommended: not now.* Read the page with titles only first. At 30 days I
   report the share of live rows that carry the line; under half is the signal to
   say yes.
3. **Should the guide be copied into every adopter's tree?** *Recommended: no.* It
   is cited in `--help` in the form Cairn already uses for files adopters do not
   receive. A new installed file changes the install contract.
4. **When should the board's data carry what waits on you from `dev/PLANNING.md`
   rows?** *Recommended: after the sibling's `--maintainer` has been in use for a
   few weeks.* Until then the page shows artifacts only, and says so on its face.

### Context

Terms and today's facts are as the opening states them, with these corrections.
The board reads header lines **and the title line**, not "nothing else". The
sibling plan's `--maintainer` also reads `dev/PLANNING.md` lines. The sibling is in
plan revision, so nothing here depends on its code except one header line (F2).

The doctrine disagrees with itself about the tool. `doctrine/lifecycle.md:144-146`
says a board can tell whose move it is from the status. `doctrine/session-routines.md:54-56`
and `templates/skills/session-start/SKILL.md:43-45` say the board decides nothing
about who holds a row. That disagreement predates this proposal; this one does not
take a side in the board. The failure being addressed is unchanged: a hand-kept
view (the `dev/PLANNING.md` "Active" table in August, the shared web page this
week) is a second copy that goes stale. `cairn-intent-list/1`
(`tools/_intent/cli.py:107-113`) is the precedent for a versioned contract, but no
test in `bootstrap/tests/` pins it, so this proposal supplies its own.

### Proposal

#### The output

`python tools/board.py --json` prints one JSON document; `--archive` adds archived
artifacts as today. `--json` with `--maintainer` is a usage error.

| Top-level key | Type | Why a view needs it |
|---|---|---|
| `schema` | string `"cairn-board/1"` | the fence; present even when empty |
| `includes_archive` | boolean | so "no archived rows" is not read as "none exist" |
| `artifacts` | list of records | the board |

| Record key | Type | Source | Why |
|---|---|---|---|
| `kind` | string: `"proposal"` or `"plan"` | the directory | grouping |
| `id` | string | file name without `.md` | the name artifacts are cited by; unique per `kind` |
| `path` | string | repo-relative, `/` separators | a link target |
| `archived` | boolean | under `archive/` | done versus in flight |
| `title` | string or null | first `# ` line above the first `##` | the label when there is no summary |
| `in_brief` | string or null | `**In brief**:` header line | the one plain sentence; **optional** |
| `status` | string or null | `**Status**:`, as written | the raw fact |
| `review`, `plan_review`, `opened`, `source_proposal` | string or null | lines the terminal board prints | unchanged facts |
| `waiting_on_maintainer` | string or null | `**Waiting on Maintainer**:` header line | a plan can wait on you while its status reads `implementing` |

Every key is a line an author wrote or a fact of where the file sits. **No value is
derived.** The terminal board is unchanged on a tree with no symlinked artifact.

**What a view does with it.** The guide carries the lookup the lifecycle doctrine
states, as a table and as a Python mapping in the example, and a test pins both to
`doctrine/lifecycle.md`. The key is the first word of `status`, matched exactly
(real headers read `archived — C1-C9 all landed…`):

| Status | Holder |
|---|---|
| `awaiting-decision` | Maintainer |
| `revising`, `revising-plan` | author |
| `awaiting-review`, `awaiting-plan-review`, `awaiting-code-review` | reviewer |
| `ready-to-implement`, `implementing`, `revising-code` | implementer |
| `accepted`, `rejected`, `superseded`, `archived`, `ready-to-archive`, anything else | none named |

**Precedence: a declared wait overrides the status word.** A record with a
non-null `waiting_on_maintainer` groups under the Maintainer whatever its status
says. The guide says the lookup is the doctrine's table, not a check that the
status is current or true, and that "none named" is not "nobody needed".

#### The promise

1. Within `cairn-board/1` the producer **only adds**: new keys on any object, new
   top-level keys. It never removes or renames a key, changes a key's type, or
   changes what a key means. Everything in the two tables above is in the baseline.
2. A breaking change is `cairn-board/2`, announced in `CHANGELOG.md`. The board
   emits one version, so a consumer built for `/1` meets `/2` as a refusal at the
   `schema` check.
3. **Consumers** read `schema`, accept the version they were built for, refuse
   others, and **ignore keys they do not know**.
4. Absent is `null`: never `""`, never inferred. A string is what the author wrote,
   whitespace-trimmed, and is **not escaped for any output**. It is untrusted text
   any contributor can edit; escaping for a page is the page-builder's job.
5. Same files, same bytes, **under one producer version**: no timestamp, commit id
   or machine path; keys sorted; ASCII-only JSON. Row order is **not** promised.
   `id` is unique within a `kind` today and the pair `(kind, id)` is what a consumer
   should key on; uniqueness across kinds is not promised.
6. On any failure nothing goes to standard output and the exit is nonzero, never a
   partial document. A script that regenerates a page must not overwrite it then.
7. **Not promised:** the terminal layout, that an optional field is present, or any
   meaning of free text.

**The test that can catch a break.** `bootstrap/tests/fixtures/board_json_v1_baseline.json`
commits every `/1` key with its JSON types. The test runs the board on a tree with
every field written and on one with every field absent, and requires each baseline
key present with its type (subset semantics). A new key passes only if the guide
lists it. A diff that removes or retypes a baseline line is a `/2` change and is
reviewed as one; the test cannot stop someone editing the baseline and the code
together, and S5 says so.

#### What each candidate became

| # | Candidate | Verdict | Reason |
|---|---|---|---|
| 1 | who acts next | **Reshape**: a tested lookup in the guide; no board field | the board stays "decides nothing"; no doctrine edit; the field can be added later, additively. Cost: every view carries about eight lines, and a non-Python consumer rewrites them |
| 2 | one plain sentence | **Keep, optional** | `in_brief` and `title` are separate; the view writes `in_brief or title`. Header line only |
| 3 | `--json` | **Keep**: the deliverable | the contract above |
| 4 | grouping, summary line | **Drop** from the board | presentation belongs in the view; the example shows both |
| 5 | roadmap rows | **Drop** from `/1` | no wait keys until the sibling's C1 is landed and used. Of 30 top-level bold rows in `dev/PLANNING.md`, 7 carry the status marker (rows matching `^\* \*\*`, marker `*(queued|active|blocked|deferred|completed` on the first line, at `8e5df0f0`), so reading all means retrofitting 23. Revival: Question 4 |
| 6 | recently finished | **Drop**; tested recipe in the guide | the board runs no git. `git log --diff-filter=A --name-status -- dev/plans/archive` lists plans by archive date |
| 7 | active work intents | **Drop**; tested recipe in the guide | the intent log is gitignored and local to one working tree, so one commit would print different boards on different machines; a dead session's claim reads "working" forever. The guide joins `intent.py list --format json` to the board on `stem` as a hint, since `stem` is optional |

#### The guide

`docs/build-a-board-view.md`, descriptive layer: it describes the tool and how to
extend it, and prescribes nothing cross-cutting. It holds:

* the fields, the promise, and the lookup table with its precedence rule;
* a worked example (about 50 lines of standard-library Python) that runs
  `[sys.executable, "tools/board.py", "--json"]` with no shell, groups by holder
  with counts, shows the raw status beside each row, escapes every value with
  `html.escape`, and stamps the commit it read. The page's footer says that
  advisories (plans that mention a fence without declaring a wait) are not shown,
  and to run `python tools/board.py --maintainer` for them;
* **when it regenerates (F5).** The only triggers are a person running the script
  (for example as a session-end step) or a post-commit hook the adopter installs;
  the scaffold never writes `.git/hooks`. With neither, the page is a snapshot and
  says so by its stamped commit;
* **what the data supports:** "needs you" (for artifacts), "in flight by holder",
  "queued" and "done". **"Blocked" and "an agent is working right now" are not
  derivable.** Roadmap rows and their waits are not in the data; the guide links
  `dev/PLANNING.md` and the `--maintainer` text instead (F6);
* two tested recipes: finished plans by date, and the intent join;
* **reaching and running it (F9).** Adopters do not receive `docs/`. `--help` ends
  with: "Field reference and worked example: Cairn's own
  `cairn/docs/build-a-board-view.md` (in the repository you adopted from, not in
  this tree)", the form modules already use for Cairn-owned docs. The guide says
  `--json` was added after Cairn 0.3.0, that `python tools/board.py --json` exiting
  2 with "unrecognized arguments" means an older board, and points to
  `bootstrap/UPGRADE.md` for the upgrade;
* a short note that an AI agent can be handed the guide and asked for a richer
  page from the same output, regenerated rather than hand-edited. No vendor named.

**Why the example lives in the guide, not in `tools/`.** A script in the install
set is a view generator in the core, which you ruled out, and executable code every
adopter would carry through the lockfile, upgrades and the security lint. In the
guide it costs adopters nothing, and a test runs it so it cannot rot.

#### Where it lands

* `tools/board.py` and its byte-identical twin `templates/skills/_lib/board.py` gain
  `--json`; the `title`, `In brief` and `Waiting on Maintainer` reads; the help
  citation; and a rule that a symlinked artifact is skipped. **The rule applies in
  both modes**, because it sits in the shared row reader, so the terminal board
  changes only on a tree that has symlinked artifacts. "Unchanged" and the
  byte-identical check hold for trees without them.
* **Four places say the board reads headers only, and the plan edits each (F7),
  after the sibling's own edits to them:** the docstring `tools/board.py:7-11`; the
  help text `:115-116`; the plain-mode footer `:108-109`, which stays byte-identical
  because plain mode still prints header fields only; and `docs/tool-usage.md:117-120`.
  The new docstring sentence says the board also reads the title line and, with
  `--json`, prints no derived value.
* The lockfile record for `tools/board.py` is reconciled by a scoped finalize of
  that one path (precedent `2ea3f869`).
* New: the guide, the test file, the baseline fixture.
* **Sequencing.** The first implementation chunk starts only from a tree holding
  maintainer-attention's C1 commit, because both change `board.py`, the twin and the
  lockfile record.
* **Frozen files: none.** `frozen_files` in `bootstrap/tests/fixtures/gate_manifest.json`
  (183 entries) names none of the files above, checked against a known key
  (`bootstrap/tests/test_replacement_tools.py`). The new tests join the pinned
  collection and the queued re-anchor row.
* **AST impact: none.** `bootstrap/_scaffold/` is untouched. **Install contract:
  unchanged** (same destination, source, mode; the plan diffs `scaffold.py
  --manifest` before and after).

### Rationale

Cairn already holds every fact the web page shows. What is missing is a way out of
the tool that does not mean scraping a display format. A derived page cannot
disagree with the artifacts at the moment it is generated. Whether it is generated
often enough is a separate cause, handled by a named trigger and a stamped commit.

A contract, not a dump: "only add" costs the producer almost nothing and gives every
consumer a safe default. The one-way door is removal, so `/1` carries only what an
author wrote or where the file sits, and each deferred item can arrive later with no
version bump. **The derived lookup was the draft's own strongest rival**: shipping
it in the tool saves every view eight lines, but it would make the board answer
"whose move is it" against two doctrine passages and force an edit nobody has chosen.
It comes back as a field if views drift on the lookup or a non-Python consumer needs
it. Cost of this version: about 60 to 80 lines in `board.py` on top of the sibling's
(an estimate, not a measurement), one guide, one fixture, one contract.

**Review tier.** `required(Internal)`, and the External floor was met by `fe0d093c`.

### Alternatives considered

* **Ship a view** (an `--html` flag or a separate view script). Rejected, per your
  direction and because a shipped view is one rendering for every team, edited by
  hand by the first team that disagrees, which brings the drift back.
* **Put the lookup in the board as `status_holder`.** The opening's choice;
  rejected by review (F1) for the doctrine conflict and the stale-status failure it
  invites. Revival condition above.
* **Let views scrape the terminal output.** Rejected: cells are cut at 48
  characters, `|` is escaped, and the layout changes freely.
* **A JSON Schema file beside the guide.** Rejected: a second statement of the
  contract can disagree with the first; one, pinned to the output, cannot.
* **Do nothing.** The page keeps going stale and the next copy repeats August.

### Documentation / doctrine surface

| Layer | File | Change |
|---|---|---|
| Descriptive | `docs/build-a-board-view.md` (new) | the guide; routed to `docs/` because it describes current behavior and how to extend it (`docs/DOCUMENTATION_PLAN.md`) |
| Descriptive | `docs/tool-usage.md` | the board entry gains `--json`, a link, and a corrected description |
| Governing, deliberation | none | no `doctrine/` or `AGENTS.md` change |

No doctrine changes, so the rate-limit gate in `doctrine/rationale.md` is not
engaged. The guide names no AI vendor or product, and no hosting service from the
neutrality denylist; the page you use is described there as a shared web page with
live status.

### Evidence / verification plan

It worked if you open the page the guide's script builds from this tree and can say
what needs you and what is in flight without opening an artifact (**your reading is
a success criterion**), and its artifact entries in "needs you" equal the artifact
lines `board.py --maintainer` lists. It failed if anyone must edit the generated
file or read the terminal output to get a correct page.

#### Tests required

All in the new `bootstrap/tests/test_board_json_contract.py`, each seen failing
before the code exists:

* **The `/1` baseline holds (F3):** every baseline key present with its type, on a
  full tree and on an all-absent tree; absent is `null`, never `""`; a new key
  passes only if the guide lists it.
* **The guide and the output agree:** the keys in the guide's tables equal the
  emitted keys, both ways.
* **The guide's lookup matches the lifecycle:** every status word in
  `doctrine/lifecycle.md`'s two diagrams is in the guide's table and in the
  example's mapping with the holder its node label gives; first-word matching;
  an unknown status gives "none named"; a declared wait overrides the status.
* **The guide's examples run:** the view example on a scratch tree whose title
  holds `<script>` (escaped form, grouped counts, stamp present); the finished-plans
  recipe in a scratch git repository; the intent join on canned input, with and
  without `stem`.
* **Same files, same bytes;** ASCII, sorted keys, schema on an empty tree.
* **A symlinked artifact is skipped; an unreadable file gives no standard output
  and a nonzero exit.**
* **The terminal board is byte-identical** on one tree without symlinks.

Boundary A adds `test_replacement_tools.py`, `test_security_lint.py`,
`test_skills_upgrade.py`, `test_skills_self_heal.py` and `test_verify_integrity.py`.
Boundary B is expected **full** (a tool adopters run changes, a lockfile record is
touched, uncertainty resolves to full).

#### Examples / smoke checks

* `python tools/board.py --json | python -m json.tool` on the live tree.
* The guide's script on the live tree, then the page opened and read by a person.
* **`python scripts/quality_gate.py --sub neutrality` is red today:** `fail=74
  info=21` at `8e5df0f0`, Python 3.13.13. The plan records those two figures before
  and after and shows no finding in the guide or either board copy. If the accepted
  neutrality proposal brings the figure to zero first, the baseline is zero.
* `check_cairn.py`; `claim_check.py` on the guide.

#### Security preflight — five questions, answered in writing

The tool adds no network access, subprocess or deserialization. It adds an output
other programs read and one file-handling rule; the guide's example runs two
fixed-argument subprocesses (the board, and `git rev-parse HEAD`), never through a
shell, and the guide says an adopter wiring it to a hook is adding a subprocess to
their own tree.

* **S1 — Who supplied it?** Every value comes from artifact files any contributor
  can edit. No value is derived, so the board makes no claim about whose move it is
  and authenticates nothing. A symlink could let a file outside `dev/` supply a
  title; the symlink rule closes that.
* **S2 — Can it fail?** Mutations, run with results in the plan's record:
  rename `status` to `state` in code **and** guide (the baseline test goes red);
  emit `""` for an absent field (red); delete the symlink skip (red); print a
  partial document before a nonzero exit (red); remove `html.escape` from the
  example (red); change one lookup entry (the lifecycle test goes red). The lookup
  test checks against the lifecycle document, not against the code it tests.
* **S3 — What fires it, over what?** `python -m pytest
  bootstrap/tests/test_board_json_contract.py` and the Boundary B full run, both
  started by a person (Cairn has no CI). The baseline test is what ties the
  guide's promise to the output.
* **S4 — Which way does it break?** An absent field is `null`, never a guess; a
  failure gives no output, not a partial board; an unknown `schema` makes the
  consumer refuse; an older board refuses `--json` with exit 2. The hazard is
  human: reading "none named" as "nothing to do", which the guide says it is not.
* **S5 — Who still wins?** A contributor who can edit a header can still put
  misleading, well-formed text on the board (claim `archived`, omit a
  `**Waiting on Maintainer**:` line) or put markup or direction-override characters
  in a title for a page-builder that forgets to escape. The escaping class is closed
  **by enumeration**, not construction: the board leaves strings raw (the terminal
  encoder would turn `A | B` into `A \x7c B`, wrong for data), so the duty falls on
  the page-builder, in the guide and the tested example. And someone who edits the
  baseline and the code together defeats the baseline test; only review reads that
  diff.

### Signals the change is wrong

* A consumer needs a field we left out, and adding it means renaming or retyping one.
* **Authors rarely write `**In brief**:`.** At 30 days, if under half of the live
  rows carry it, Question 2 becomes a yes; the page shows titles until then.
* **The stamped commit on the page is older than `HEAD` when you open it, more than
  once in the first fortnight:** the trigger is not firing, and the guide failed.
* The page you use is still hand-edited beside the generated one.
* Two views carry different lookups, or one disagrees with `doctrine/lifecycle.md`:
  the lookup belongs in the board after all.
* Requests for an `--html` flag mean the guide is not easy enough; by itself that is
  not a reason to ship a view.

### Scope delta

**Scope delta**: degraded. Against the opening, this revision removes three units.
The first is still delivered, by a weaker mechanism; the others are not delivered
now. Prefer specifying to cutting: specifying `status_holder` needed a doctrine
decision nobody has made (F1), and specifying the wait keys needed code that does
not exist (F2). Each removal below needs your allowance at the Decision.

* **`status_holder` in the board's data** (opening Proposal > The holder lookup, and
  opening Question 4). The outcome "a view can group by who acts next" is delivered
  by the guide's tested lookup.
  **disposition**: guard
  (`bootstrap/tests/test_board_json_contract.py::TestGuideLookupMatchesLifecycle`).
  Opening Question 4, a terminal column, is moot and is **wontfix**.
* **`maintainer_waits`, including roadmap-line waits** (opening top-level key, and
  candidate 5's "rows declaring a wait"). Views compute "needs you" for artifacts
  from `status` and `waiting_on_maintainer`; roadmap waits stay in the terminal
  `--maintainer` text. **disposition**: defer, to a later additive key; revival
  condition in Question 4.
* **`fences_without_wait`** (opening top-level key). A body-text heuristic whose
  membership could not be promised; the terminal `--maintainer` footer carries it,
  and the example's page footer says so. **disposition**: wontfix, with that reason.

### Assurance path

**Assurance path**: high-assurance. Mandatory under the template's own rule:
`tools/board.py` is executed by every adopter and its output becomes a published
contract. No other trigger applies: no `doctrine/` change, no install-contract
change, no engine change.

### Withdrawn / superseded commitments

* **`status_holder`**, its lookup in `board.py`, and opening Question 4: moved to
  the guide and the Scope delta (F1).
* **`maintainer_waits` and `fences_without_wait`**: removed from `/1` (F2).
* **"Both sentences describe the terminal board"**: withdrawn (F1).
* **"The rate-limit gate would be met by the recurrence above"**: withdrawn; no
  doctrine edit, so the gate is not engaged (F1).
* **"I have declared below that floor, for your Decision to ratify or override"**:
  withdrawn; the floor was met by `fe0d093c` (the Response).
* **"The second copy was the only cause of the staleness"**: withdrawn as an
  overstatement (F5).
* **"Tested recipes"** in the opening commit message: it was premature then and is
  made true by the F6 tests.
* **Plan review `required(Internal)`**: replaced by `required(Internal + Internal
  Security Review)` (F10).
* **"About 4 of about 30 rows carry the status marker"**: corrected to 7 of 30 (F10).
* **"Reads these and nothing else"** in Terms: corrected to header lines and the
  title line (F7).
* **The example's `python` PATH lookup**: replaced by `sys.executable` (F10).
* **The cut, per the reviewer's alternative**: wait keys wait for the sibling's C1.

## Decision -- Anthony Kendall (Maintainer) -- 2026-10-18

**ACCEPTED.** The Maintainer's authorization, quoted **verbatim and visually
isolated**:

> "accept both as descried"

*Scribe's note, separate from the quoted words.* "Both" names the board-as-basis
and review-stance proposals. "As described" refers to the scribe's summary
the Maintainer was answering, which recorded the Maintainer's answers to each
question (given in chat, 2026-10-18, partly through a multiple-choice prompt).
For this proposal they are:

* **Revision 1 binds, with these changes the Maintainer made at the Decision**
  (binding on the plan):
  * **"What waits on the Maintainer" becomes a recipe in the guide**, not a
    deferral. In the Maintainer's words: "For the board proposal, I'd put the
    what waits on my in the recipe, actually instead of deferring it."
  * **Roadmap rows that declare a wait go into the `/1` data now** (answer to
    Q4: "Yes, now"), so the recipe can list them.
  * **The `**In brief**:` prompt goes into the proposal and plan templates now**
    (answer to Q2: "Yes, add it now").
* **The fence warning stays in the terminal `--maintainer` view only** (answer:
  "Terminal view only"). It is not in the data, and not a recipe.
* **The guide is read in Cairn's published docs**, cited by `board.py --help`,
  and not copied into installs (answer to Q3).
* **The "who acts next" lookup lives in the guide** (Q1, accepted as recommended).
* **The Scope delta is allowed as revised.** `status_holder` becomes a guide
  recipe, and `fences_without_wait` is wontfix for the data. `maintainer_waits` is
  no longer deferred: it becomes the guide recipe above.
* **Review record.** The External-labelled pass at `fe0d093c` is read as the
  usual review, per the review-stance Decision's migration answer. The
  Maintainer did not call for an External read.

Scribed by Claude (claude-opus-5-5) on the Maintainer's explicit instruction.
Nothing else lands in this commit.
