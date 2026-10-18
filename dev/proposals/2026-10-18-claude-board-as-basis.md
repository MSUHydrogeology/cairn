# The board as the basis for richer views: a stable JSON output, and a guide to building on it

**Author**: Claude (Strategy)
**Status**: awaiting-review
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
